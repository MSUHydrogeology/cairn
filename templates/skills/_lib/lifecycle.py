#!/usr/bin/env python3
"""Cairn lifecycle CLI -- deterministic backend for the session-routine skills.

This is the mechanizable half of Cairn's two session-lifecycle skills
(`session-start` / `session-end`).  The skills' `SKILL.md` bodies carry only
the irreducibly-judgment steps (what to reflect on, which in-flight threads
matter, how to frame the next session); the *mechanical* steps -- gathering git
state, surfacing open threads, scaffolding the reflection file -- live here, in
a tool, because a deterministic tool beats a prose checklist an agent can
misread, skip, or run one slow authorization at a time.  (The `tools/intent.py`
lesson, generalized.)

The scaffold installs this verbatim into an adopting repo's `tools/lifecycle.py`
(default-on, like the routines it backs).  It is **vendor-neutral** and
**standard-library only**; the canonical doctrine it executes is
`doctrine/session-routines.md`, never restated here.

Two safety properties are load-bearing and are *not* negotiable defaults:

* **No network.**  The CLI's surface is local git state, the reflections /
  handoff files, and (optionally) the intents log -- nothing else.
* **Reflection-only by default.**  `session-end` performs only non-destructive
  work (it *creates* a reflection scaffold and *reads* the board); the
  destructive full-handoff path (prune reflections, run metrics, surface
  intents) is gated behind an explicit `--handoff` plus a maintainer-designation
  marker and a fail-closed concurrent-handoff lock.  Without the marker
  `--handoff` refuses non-interactively; `--handoff --dry-run` prints a mutation
  manifest and changes nothing.  So even if a harness ignores
  `disable-model-invocation` and auto-fires `session-end`, the worst case is a
  stray reflection file, never a roadmap scrub.

Every side-effecting subcommand honors `--dry-run`: it prints the planned
writes and exits writing nothing.

Run:
    python tools/lifecycle.py session-start
    python tools/lifecycle.py session-end [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import secrets
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple

# --- tunable windows (adopter-overridable via flags) -------------------------

#: Reflections older than this are pruned at full-handoff (`session-routines.md`
#: makes reflections ephemeral; durable observations migrate out before then).
_REFLECTION_GRACE_DAYS = 14

#: A handoff lease is considered *expired* after this many seconds without a
#: heartbeat refresh.  Expiry alone never reclaims a lock -- it is one of two
#: conditions; the other is affirmative proof the holder is dead (S1).
_HANDOFF_LEASE_SECONDS = 900

#: Where machine-local lifecycle state lives (gitignored members).  Mirrors the
#: tracked ``dev/.cairn/base/`` cache convention -- ``dev/.cairn/`` is the
#: deployment's machine-state home.
_CAIRN_STATE_DIR = ("dev", ".cairn")

#: The canonical lifecycle-skills source (read directly by the alias-tier
#: harnesses).  Symlink-tier harnesses (today only Claude Code, ``.claude/
#: skills``) fan out to this dir; the session-start self-heal keeps those
#: read-paths in sync.
_AGENTS_SKILLS_DIR = (".agents", "skills")

#: The installed vendor fan-out table the self-heal reads at runtime (the
#: single source of which harness paths are eligible) -- propagated to adopters
#: alongside the canonical skills, so the routine never needs a sibling Cairn
#: checkout to know its targets.  A vendor refresh is a row edit there.
_VENDOR_TARGETS_REL = (".agents", "skills", "_data", "vendor_targets.yml")

# --- structured output -------------------------------------------------------
#
# Every line the agent's skill body relays is prefixed so the orchestrating
# body can distinguish lifecycle output from any sub-tool's output, and so a
# skipped/failed step is visible rather than silent (the "loud-failure"
# discipline).

_PREFIX = "lifecycle:"


def _emit(message: str) -> None:
    """Print a normal progress line to stdout."""
    print(f"{_PREFIX} {message}")


def _emit_section(title: str) -> None:
    """Print a section header so the relayed output is legibly grouped."""
    print(f"\n{_PREFIX} == {title} ==")


def _warn(message: str) -> None:
    """Print a non-fatal advisory to stderr (a skipped optional step, etc.)."""
    print(f"{_PREFIX} NOTE: {message}", file=sys.stderr)


class LifecycleError(RuntimeError):
    """A fatal, *actionable* failure -- never a silent skip.

    Raised when a step cannot proceed and the operator must act (e.g. the
    command is run outside a git repository).  `main` turns it into a non-zero
    exit with the message, not a stack trace.
    """


# --- environment resolution --------------------------------------------------


def _repo_root(start: Optional[Path] = None) -> Path:
    """Return the git repository root containing `start` (default: cwd).

    Resolved via `git rev-parse` so it is correct regardless of where the
    installed `tools/lifecycle.py` sits relative to the working directory.
    """
    cwd = str(start) if start is not None else None
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            env=_git_env(),
        )
    except FileNotFoundError as exc:  # git not on PATH
        raise LifecycleError(
            "git was not found on PATH; the lifecycle routines need git to "
            "gather session state."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise LifecycleError(
            "not inside a git repository -- run the lifecycle routines from "
            "within the project checkout."
        ) from exc
    return Path(out.stdout.strip())


def _git_env() -> dict:
    """A noninteractive, no-pager, no-remote-prompt git environment.

    Keeps git from blocking on a pager or a credential prompt inside a
    non-interactive agent subshell.  (The full subprocess allowlist + network
    block is a security-chunk concern; this is the minimal hygiene the gather
    steps need.)
    """
    env = dict(os.environ)
    env["GIT_PAGER"] = "cat"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _git(args: List[str], root: Path) -> str:
    """Run a read-only git command at `root` and return its stdout.

    Raises `LifecycleError` (actionable) rather than leaking a traceback.
    """
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=True,
            env=_git_env(),
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip() or f"git {' '.join(args)} failed"
        raise LifecycleError(detail) from exc
    return out.stdout


def _intent_whoami(root: Path, *, session_token: bool = False) -> Optional[str]:
    """Return ``intent.py whoami`` output, or ``None`` if unavailable.

    The coordination/intent tool is **optional** (team-gated): a missing or
    unusable tool is a clean ``None``, never a crash -- the default-on lifecycle
    skill must not hard-require it.  With ``session_token=True`` the bare
    per-session digest is returned (``whoami --session-token``); otherwise the
    full ``<tool_tag>-<digest>`` identity.
    """
    intent_tool = _sibling_tool("intent.py")
    if intent_tool is None:
        return None
    try:
        interpreter, _ = _resolve_interpreter(root)
    except LifecycleError:
        interpreter = sys.executable
    cmd = [interpreter, str(intent_tool), "whoami"]
    if session_token:
        cmd.append("--session-token")
    try:
        proc = subprocess.run(
            cmd, cwd=str(root), capture_output=True, text=True,
            check=False, env=_git_env(),
        )
    except OSError:
        return None  # intent tool unusable -> caller falls back
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def _resolve_agent(root: Path) -> str:
    """Resolve the agent identifier used in the reflection filename.

    Resolution order, parallel to ``_resolve_session`` so the
    ``<agent>-<session>`` tail reconstructs the intent log's identity:

    1. an explicit ``CAIRN_AGENT`` override;
    2. else the coordination/intent identity -- ``intent.py whoami`` -- with its
       trailing ``-<session_digest>`` stripped to leave the tool tag (so e.g.
       ``claude-e84b19df`` -> ``claude``), when that tool is installed;
    3. else the neutral default ``agent``.

    The value becomes part of a filename, so it is **sanitized to a safe slug**
    (`[A-Za-z0-9._-]` only): an unsanitized value such as ``../../etc/x`` must
    not be able to redirect the reflection write outside ``dev/reflections/``
    (path-containment, S3).  An empty / fully-stripped value falls back to
    ``agent``.
    """
    raw = os.environ.get("CAIRN_AGENT", "").strip()
    if not raw:
        identity = _intent_whoami(root)
        if identity:
            # intent identity is "<tool_tag>-<8-hex digest>"; strip a genuine
            # digest suffix so <agent> is the tool tag and <agent>-<session>
            # reconstructs the identity.  Strip only an exact 8-hex tail, so a
            # hyphenated tool tag or a digest-less identity is left intact.
            head, _, tail = identity.rpartition("-")
            raw = head if head and re.fullmatch(r"[0-9a-f]{8}", tail) else identity
    slug = re.sub(r"[^A-Za-z0-9._-]", "-", raw).strip(".-")
    return slug or "agent"


def _resolve_session(root: Path) -> str:
    """Resolve the per-session token in the reflection filename (fold-back #46).

    Without a session-distinct segment, two concurrent same-agent sessions
    scaffold the *same* ``<date>-<agent>.md`` and clobber each other -- the
    collision #46 fixed in the reflections doctrine but that this CLI had not
    yet honored (#50).  Resolution order, per the reflections doctrine:

    1. an explicit ``CAIRN_SESSION`` override (parallels ``CAIRN_AGENT``);
    2. else the coordination/intent per-session token -- ``intent.py whoami
       --session-token`` (the 8-hex digest of the harness session id) when that
       tool is installed, so the ``<agent>-<session>`` tail reconstructs the
       intent log's ``agent`` field;
    3. else a short **random** token.

    The fallback is random -- never a shared or persisted value -- so two
    concurrent same-agent sessions never resolve the same token (a persisted
    per-checkout token would re-introduce the very collision).  The trade is
    that re-running in one session may scaffold a *second* reflection rather
    than re-opening the first; a new file is recoverable, a clobber is not.
    Sanitized to a filename-safe slug (path-containment, S3).
    """
    raw = os.environ.get("CAIRN_SESSION", "").strip()
    if not raw:
        token = _intent_whoami(root, session_token=True)
        if token:
            raw = token
    if not raw:
        raw = secrets.token_hex(4)
    slug = re.sub(r"[^A-Za-z0-9._-]", "-", raw).strip(".-")
    return slug or secrets.token_hex(4)


def _today() -> str:
    """Today's date as ``YYYY-MM-DD`` (local)."""
    return _dt.date.today().isoformat()


def _sibling_tool(name: str) -> Optional[Path]:
    """Return an installed sibling tool (e.g. ``intent.py``) if present.

    The lifecycle CLI orchestrates other Cairn tools that may or may not be
    installed (they are separate modules).  A missing optional tool is a
    skip-with-note, never a crash -- the default-on lifecycle skill must not
    hard-require a team-gated module.
    """
    candidate = Path(__file__).resolve().parent / name
    return candidate if candidate.is_file() else None


def _state_dir(root: Path) -> Path:
    return root.joinpath(*_CAIRN_STATE_DIR)


def _assert_within(path: Path, base: Path) -> None:
    """Fail closed if `path` would resolve outside `base` (path-containment, S3).

    Defense in depth behind the agent-slug sanitization: every reflection /
    handoff write the CLI performs must land inside its declared surface, so a
    crafted input can never redirect a write elsewhere in (or out of) the repo.
    """
    resolved = (path.parent.resolve() / path.name)
    try:
        resolved.relative_to(base.resolve())
    except ValueError:
        raise LifecycleError(
            f"refusing to write outside {base}: {path}"
        )


def _has_symlink_component(path: Path) -> bool:
    """True if `path` or any of its parents is a symlink.

    The interpreter trust root must not be reachable through a symlink (leaf or
    parent), since a symlink can be retargeted out-of-band to redirect which
    binary runs (S2).
    """
    cur = path
    while True:
        if cur.is_symlink():
            return True
        if cur.parent == cur:
            return False
        cur = cur.parent


def _resolve_interpreter(root: Path) -> Tuple[str, str]:
    """Resolve the project interpreter the routines invoke sub-tools with.

    Resolve-don't-bake (Decision 6 / R3): the interpreter binding lives in an
    **untracked** ``dev/.cairn/local-env.json`` written at bootstrap, never
    baked into a tracked file.  Because that file is an *executable trust root*
    a local edit can silently redirect, it carries a **strict, tamper-aware
    contract** (S2): exactly one key ``interpreter`` mapping to an **absolute**
    path to an **existing executable file**, reached through **no symlinked leaf
    or parent**, with **no arguments / shell interpolation / relative segments**.
    Any violation **refuses before running anything** (a `LifecycleError`).

    Returns ``(interpreter_path, source)`` where source is ``"local-env.json"``
    or ``"fallback"``.  When the config is absent, the **runtime resolver
    fallback** is the interpreter currently running this CLI -- safe because the
    lifecycle tools are standard-library only -- and the caller surfaces install
    guidance so the hidden binding is never silently assumed.
    """
    cfg = _state_dir(root) / "local-env.json"
    if not cfg.is_file():
        return sys.executable, "fallback"

    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LifecycleError(
            f"{cfg} is not readable JSON: {exc}.  It must be "
            '{{"interpreter": "/abs/path/to/python"}}.'
        ) from exc

    # Strict single-key schema: a tamper-aware trust root should not silently
    # accept extra attacker-controlled fields (review-crispness, finding 4).
    if not isinstance(data, dict) or set(data) != {"interpreter"}:
        raise LifecycleError(
            f'{cfg} must be a JSON object with exactly one key, "interpreter".'
        )
    value = data["interpreter"]
    if not isinstance(value, str) or not value.strip():
        raise LifecycleError(f'{cfg}: "interpreter" must be a non-empty string.')
    # Reject NUL / control characters only.  We invoke as an explicit argv list
    # (never a shell), so shell metacharacters in a path are inert, and spaces
    # are legitimate in real filesystem paths (`My Drive`, OneDrive, profile
    # dirs).  An appended-argument string like "/usr/bin/python -c ..." is
    # caught by the is_file() check below, not by banning spaces (finding 1).
    if any(ord(ch) < 0x20 or ch == "\x7f" for ch in value):
        raise LifecycleError(
            f'{cfg}: "interpreter" must not contain control characters.'
        )
    interp = Path(value)
    if not interp.is_absolute():
        raise LifecycleError(f'{cfg}: "interpreter" must be an absolute path.')
    if _has_symlink_component(interp):
        raise LifecycleError(
            f'{cfg}: "interpreter" must not be reached through a symlink '
            "(leaf or parent)."
        )
    if not interp.is_file() or not os.access(interp, os.X_OK):
        raise LifecycleError(
            f'{cfg}: "interpreter" is not an executable file: {interp}.'
        )
    return str(interp), "local-env.json"


# --- in-flight thread survey -------------------------------------------------


def _status_of(path: Path) -> str:
    """Best-effort read of a proposal/plan ``**Status**:`` line for the survey."""
    try:
        for line in path.read_text(encoding="utf-8").splitlines()[:40]:
            stripped = line.strip()
            low = stripped.lower()
            if low.startswith("**status**:") or low.startswith("status:"):
                value = stripped.split(":", 1)[1].strip().strip("*").strip()
                return value or "(unspecified)"
    except OSError:
        pass
    return "(no status line)"


def _in_flight(root: Path) -> List[str]:
    """List open proposals/plans (live `dev/` files, excluding archives).

    These are the live multi-agent threads the session-start move surfaces and
    the reflection-only goodnight notes as open work.
    """
    lines: List[str] = []
    for kind in ("proposals", "plans"):
        base = root / "dev" / kind
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*.md")):
            if path.name == "_template.md":
                continue
            lines.append(f"{kind}/{path.name} -- {_status_of(path)}")
    return lines


# --- session-start skills fan-out self-heal ---------------------------------
#
# The canonical lifecycle skills live in ``.agents/skills/`` (read directly by
# the alias-tier harnesses).  A symlink-tier harness -- today only Claude Code,
# which reads ``.claude/skills`` -- needs that read-path fanned out to the
# canonical source.  The install-time fan-out (``scaffold.fan_out_skills``)
# runs only during a full ``scaffold.py`` install, so an adopter established by
# lockfile-copy, or whose symlink-tier harness was not present at install,
# silently has no skills in that harness.  This is the runtime self-heal: on
# session-start, ensure every eligible, in-use symlink-tier read-path exists --
# idempotently, and under the same writer-safety contract as the installer
# (path-containment, symlink->copy fallback, ``.gitignore`` seed for copy-mode,
# and refuse / quarantine -- never clobber -- a divergent existing target).
#
# It is a faithful stdlib-only port of the symlink-tier path of
# ``scaffold.fan_out_skills`` (the adopter has no ``bootstrap.scaffold``); the
# installed ``vendor_targets.yml`` table is the single source of which harness
# paths are eligible, so a vendor refresh is a data-row edit, never code here.


def _load_vendor_targets(root: Path) -> List[dict]:
    """Read the installed vendor fan-out table.  JSON-encoded (valid YAML 1.2)
    so it parses stdlib-only, like the lockfile.  Absent / unreadable / wrong
    shape -> ``[]`` (the self-heal simply does nothing -- it never crashes the
    orientation gather)."""
    path = root.joinpath(*_VENDOR_TARGETS_REL)
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    targets = data.get("targets") if isinstance(data, dict) else None
    return [r for r in targets if isinstance(r, dict)] if isinstance(targets, list) else []


def _skill_symlinks_available(root: Path) -> bool:
    """Probe whether ``os.symlink`` works under *root* (False on Windows
    without Developer Mode / Administrator -- the copy-fallback trigger)."""
    probe = root / ".cairn-skill-symlink-probe"
    try:
        if probe.is_symlink() or probe.exists():
            probe.unlink()
        os.symlink(".", probe)
        ok = probe.is_symlink()
        probe.unlink()
        return ok
    except (OSError, NotImplementedError):
        try:
            if probe.is_symlink() or probe.exists():
                probe.unlink()
        except OSError:
            pass
        return False


def _assert_fanout_contained(dst: Path, target: Path) -> None:
    """Refuse a fan-out destination reached through a **symlinked parent** or
    resolving **outside** *target* (S3).  ``dst`` itself may be the symlink we
    are about to (re)create, so only its parents are symlink-checked."""
    tr = target.resolve()
    for ancestor in dst.parents:
        if ancestor == tr:
            break
        try:
            ancestor.relative_to(tr)
        except ValueError:
            break
        if ancestor.is_symlink():
            raise LifecycleError(
                f"refusing skills fan-out through a symlinked parent: {ancestor}"
            )
    final = dst.parent.resolve() / dst.name
    try:
        final.relative_to(tr)
    except ValueError:
        raise LifecycleError(f"refusing skills fan-out outside the repo: {final}")


def _seed_skill_gitignore(root: Path, entry: str) -> None:
    """Append *entry* to ``<root>/.gitignore`` if absent (idempotent,
    non-clobber).  Copy-mode fan-out copies are generated, gitignored
    supply-chain artifacts -- the canonical ``.agents/skills/`` is the only
    tracked, editable copy.

    A **directory** ignore is matched ignoring a trailing slash, so an existing
    ``.claude/skills`` and a seeded ``.claude/skills/`` are the same entry -- a
    repo that already ignores the path (either spelling) is left byte-for-byte
    untouched, so session-start never dirties a tree it just reported clean."""
    gitignore = root / ".gitignore"
    text = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    norm = entry.rstrip("/")
    if norm in {ln.strip().rstrip("/") for ln in text.splitlines()}:
        return
    prefix = text if (not text or text.endswith("\n")) else text + "\n"
    gitignore.write_text(prefix + entry + "\n", encoding="utf-8")


def _heal_skill_symlink(dst: Path, canonical: Path) -> str:
    """Create / verify a relative symlink ``dst`` -> the canonical skills dir.
    Idempotent (``already-linked``); a wrong symlink is re-pointed
    (``relinked``); a non-symlink existing target is left untouched
    (``exists-nonsymlink``) -- never clobbered."""
    rel = os.path.relpath(canonical, dst.parent)
    if dst.is_symlink():
        if os.readlink(dst) == rel:
            return "already-linked"
        dst.unlink()
        dst.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(rel, dst, target_is_directory=True)
        return "relinked"
    if dst.exists():
        _warn(
            f"{dst} exists as a non-symlink; leaving it untouched "
            "(remove it to enable the skills symlink)."
        )
        return "exists-nonsymlink"
    dst.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(rel, dst, target_is_directory=True)
    return "linked"


def _heal_skill_copy(dst: Path, canonical: Path, target: Path) -> str:
    """Regenerate gitignored copies of the canonical skills under *dst* (used
    where symlinks are unavailable).  Idempotent: a copy already byte-equal to
    canonical is left alone; a **divergent** copy is quarantined to
    ``*.diverged.bak`` (preserved, never destroyed) and regenerated, so the
    active vendor-read path always carries the canonical, already-scanned
    bytes.  Returns ``current`` / ``copied`` / ``diverged-quarantined``."""
    import shutil

    quarantined: List[str] = []
    copied = 0
    for src_file in sorted(canonical.rglob("*")):
        if not src_file.is_file():
            continue
        rel = src_file.relative_to(canonical)
        out = dst / rel
        _assert_fanout_contained(out, target)
        if out.is_file():
            if out.read_bytes() == src_file.read_bytes():
                continue  # already current -- idempotent, no rewrite
            bak = out.with_name(out.name + ".diverged.bak")
            _assert_fanout_contained(bak, target)
            shutil.move(str(out), str(bak))
            quarantined.append(str(rel))
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_file, out)
        copied += 1
    if quarantined:
        _warn(
            f"copy-fallback divergence under {dst}: {', '.join(quarantined)} "
            "differed from the canonical .agents/skills/ source; each was "
            "quarantined to *.diverged.bak and the canonical bytes regenerated. "
            "Edit the canonical source, not the generated copy."
        )
        return "diverged-quarantined"
    return "copied" if copied else "current"


def _heal_skills_fanout(root: Path) -> List[Tuple[str, str, str]]:
    """Ensure every eligible, in-use symlink-tier skills read-path exists.

    Returns ``(target, tier_used, status)`` rows (empty when there is nothing
    to do).  Mirrors the symlink-tier path of ``scaffold.fan_out_skills``: an
    *alias*-tier harness reads ``.agents/skills/`` directly (skipped here); a
    *symlink*-tier harness gets a verified relative symlink (or, where symlinks
    are unavailable, a gitignored generated copy), emitted only when that
    harness's parent dir already exists -- the same light "is this harness in
    use?" gate the installer uses, so a repo is never littered with empty
    vendor dirs.  Every destination is containment-checked before any write."""
    canonical = root.joinpath(*_AGENTS_SKILLS_DIR)
    if not canonical.is_dir():
        return []  # no canonical source to fan out from -- not a skills adopter
    can_symlink = _skill_symlinks_available(root)
    results: List[Tuple[str, str, str]] = []
    for row in _load_vendor_targets(root):
        if row.get("tier") != "symlink":
            continue  # alias tier reads .agents/skills directly; manual is documented
        name = str(row.get("target", "?"))
        path = str(row.get("path", ""))
        if not path or path.startswith("/") or ".." in Path(path).parts:
            _warn(f"skills self-heal: unsafe vendor path for {name!r}: {path!r}; skipped.")
            continue
        dst = root / path
        if not dst.parent.exists():
            continue  # harness not in use here -- light detection, no empty dirs
        _assert_fanout_contained(dst, root)
        if can_symlink:
            results.append((name, "symlink", _heal_skill_symlink(dst, canonical)))
        else:
            status = _heal_skill_copy(dst, canonical, root)
            _seed_skill_gitignore(root, path.rstrip("/") + "/")
            results.append((name, "copy", status))
    return results


# --- subcommand: session-start ----------------------------------------------


def cmd_session_start(args: argparse.Namespace) -> int:
    """Orientation gather (read-only) + idempotent skills fan-out self-heal.

    The gather is purely informational -- commits, tree state, threads,
    intents, resolved interpreter.  The one write the routine performs is the
    **skills fan-out self-heal**: it ensures every eligible, in-use
    symlink-tier read-path (e.g. Claude Code's ``.claude/skills``) points at
    the canonical ``.agents/skills/`` source, idempotently and under the
    installer's writer-safety contract (a no-op when already linked; never
    clobbers a divergent target).  The skill body then performs the judgment
    steps (role confirmation, deciding which thread to pick up).
    """
    root = _repo_root()
    marker = args.handoff_marker
    fallback_n = args.fallback_commits

    # Skills fan-out self-heal FIRST -- the one write the routine performs.
    # Ensure every eligible, in-use symlink-tier read-path (e.g. .claude/skills)
    # points at the canonical .agents/skills/ source.  Idempotent + fail-soft (a
    # containment refusal warns and continues; it never aborts the gather).  It
    # runs *before* the working-tree status below so a copy-mode .gitignore seed
    # is reflected in the reported state -- the routine never dirties a tree it
    # has already reported clean (Codex code review P2 #1).
    _emit_section("skills fan-out self-heal")
    try:
        healed = _heal_skills_fanout(root)
    except LifecycleError as exc:
        _warn(f"skills self-heal refused: {exc}")
        healed = []
    if not healed:
        _emit("no symlink-tier harness in use here (nothing to fan out).")
    elif all(st in ("already-linked", "current") for _n, _t, st in healed):
        _emit("symlink-tier skills read-paths already current (no change).")
    else:
        for name, tier, st in healed:
            _emit(f"{name}: {tier} -> {st}")

    _emit_section(f"commits since last '{marker}' handoff")
    last_handoff = _git(
        ["log", f"--grep=^{marker}", "--format=%H", "-n", "1"], root
    ).strip()
    if last_handoff:
        rng = f"{last_handoff}..HEAD"
        log = _git(["log", rng, "--format=%h %an  %s"], root).strip()
        _emit(f"range {rng}")
    else:
        # EP4: a freshly-bootstrapped repo has no handoff commit yet -- fall
        # back to a sensible window rather than crashing on an empty range.
        log = _git(["log", f"-n{fallback_n}", "--format=%h %an  %s"], root).strip()
        _warn(
            f"no '{marker}' commit found in history; showing the last "
            f"{fallback_n} commits instead (likely a freshly-bootstrapped repo)."
        )
    print(log if log else f"{_PREFIX} (no commits in range)")

    _emit_section("working-tree state (git status --short)")
    status = _git(["status", "--short"], root).strip()
    print(status if status else f"{_PREFIX} (clean working tree)")

    _emit_section("in-flight threads (open proposals / plans)")
    threads = _in_flight(root)
    if threads:
        for line in threads:
            print(f"{_PREFIX}   {line}")
    else:
        print(f"{_PREFIX} (no open proposals or plans)")

    # Resolve the project interpreter (resolve-don't-bake); a tampered
    # local-env.json refuses here, before any sub-tool runs (S2).
    interpreter, interp_source = _resolve_interpreter(root)

    _surface_intents(root, interpreter)

    # S2: make the (otherwise hidden) interpreter trust root visible.
    _emit_section("resolved project interpreter")
    _emit(f"interpreter: {interpreter}  (from {interp_source})")
    if interp_source == "fallback":
        _warn(
            "no dev/.cairn/local-env.json -- using the current interpreter; "
            "bootstrap normally writes this binding so the routine resolves it "
            "directly instead of relying on shell activation."
        )

    _emit("session-start gather complete.")
    return 0


# --- full-handoff guards: marker, lock, destructive steps --------------------


def _designation_marker_present(root: Path) -> bool:
    """Whether the maintainer-designation marker is set (S6).

    The marker is an **anti-accidental-run / operating-mode gate, not an
    authorization boundary** -- it is trivially self-set, so it never proves the
    maintainer authorized the run; it only stops a routine full-handoff from
    firing unbidden.  Honored forms: ``CAIRN_HANDOFF_OWNER`` truthy, or a
    maintainer-created ``dev/.cairn/handoff-owner`` state file.
    """
    env = os.environ.get("CAIRN_HANDOFF_OWNER", "").strip()
    if env and env not in ("0", "false", "False", "no"):
        return True
    return (_state_dir(root) / "handoff-owner").exists()


def _pid_alive(pid: int) -> bool:
    """Best-effort host-local liveness check.

    ``os.kill(pid, 0)`` raising ``ProcessLookupError`` is the only affirmative
    proof of death.  ``PermissionError`` (exists, not ours) and any other error
    are treated as *alive* -- the conservative choice, so uncertainty never
    licenses a steal.  This is host-local only: a pid from another host says
    nothing, which is why cross-host locks are never reclaimed automatically.
    """
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except (OSError, OverflowError, ValueError):
        # PermissionError (exists, not ours) or an unrepresentable pid: treat as
        # alive so uncertainty never licenses a steal.
        return True
    return True


class HandoffLock:
    """A fail-closed, single-owner lock for the destructive full-handoff path.

    Implements the II2 disposition (R-i): a local atomic lockfile -- the only
    race-free mutual-exclusion primitive (an intents-log read carries a TOCTOU
    race).  Per S1 the stale-lock escape is **not age-only**: a held lock is
    reclaimed *only* when the lease has expired **and** the holder is provably
    dead (same host, pid gone).  Cross-host locks, live holders, and fresh
    leases all **fail closed**; a genuinely stuck lock needs manual cleanup.

    Used as a context manager so the lockfile is removed on **both clean exit
    and unexpected exception** (EP1).
    """

    def __init__(self, root: Path, agent: str) -> None:
        self.path = _state_dir(root) / "handoff.lock"
        self.agent = agent
        self._fd: Optional[int] = None

    def _payload(self) -> dict:
        now = time.time()
        return {
            "pid": os.getpid(),
            "host": socket.gethostname(),
            "agent": self.agent,
            "acquired_at": now,
            "heartbeat_at": now,
        }

    def acquire(self) -> "HandoffLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._fd = os.open(
                self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644
            )
        except FileExistsError:
            self._reclaim_or_refuse()
        os.write(self._fd, json.dumps(self._payload()).encode("utf-8"))
        return self

    def _reclaim_or_refuse(self) -> None:
        try:
            existing = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing = {}
        holder_pid = existing.get("pid")
        holder_host = existing.get("host")
        agent = existing.get("agent", "?")
        heartbeat = float(existing.get("heartbeat_at") or 0)

        same_host = holder_host == socket.gethostname()
        lease_expired = (time.time() - heartbeat) > _HANDOFF_LEASE_SECONDS
        provably_dead = (
            same_host and isinstance(holder_pid, int)
            and not _pid_alive(holder_pid)
        )

        if provably_dead and lease_expired:
            # The only sanctioned reclaim: proof of death AND an expired lease.
            _warn(
                f"reclaiming a stale handoff lock (dead pid {holder_pid}, agent "
                f"{agent}, lease expired)."
            )
            try:
                self.path.unlink()
            except OSError:
                pass
            self._fd = os.open(
                self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644
            )
            return

        raise LifecycleError(
            f"a full handoff is already in progress (agent {agent}, pid "
            f"{holder_pid} on {holder_host}) -- refusing a concurrent handoff to "
            "protect the single-owner roadmap-scrub invariant. If you are "
            f"certain the holder is dead, remove {self.path} manually and retry."
        )

    def heartbeat(self) -> None:
        """Refresh the lease so a long-running handoff is not deemed stale."""
        if self._fd is not None:
            self.path.write_text(json.dumps(self._payload()), encoding="utf-8")

    def release(self) -> None:
        if self._fd is not None:
            try:
                os.close(self._fd)
            finally:
                self._fd = None
            try:
                self.path.unlink()
            except OSError:
                pass

    def __enter__(self) -> "HandoffLock":
        return self.acquire()

    def __exit__(self, *exc_info) -> bool:
        self.release()  # EP1: released on clean exit AND exception
        return False


def _prune_reflections(root: Path, days: int, *, dry_run: bool) -> List[Path]:
    """Prune reflections older than `days` (the goodnight ephemerality step).

    Returns the files pruned (or, under `dry_run`, the files that *would* be
    pruned).  Only dated `<YYYY-MM-DD>-*.md` files are considered; `README.md`
    and any non-dated file are left alone.
    """
    refl_dir = _reflections_dir(root)
    pruned: List[Path] = []
    if not refl_dir.is_dir():
        return pruned
    cutoff = _dt.date.today() - _dt.timedelta(days=days)
    for path in sorted(refl_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        try:
            file_date = _dt.date.fromisoformat(path.name[:10])
        except ValueError:
            continue  # not a dated reflection
        if file_date < cutoff:
            pruned.append(path)
            if not dry_run:
                try:
                    path.unlink()
                except OSError as exc:
                    _warn(f"could not prune {path.name}: {exc}")
    return pruned


def _surface_intents(root: Path, interpreter: str) -> None:
    """Read-only surface of active work-intents, if intent.py is installed.

    Used by both `session-start` (who holds which paths before the first edit)
    and the full handoff (a coordination-safety check: whether another session
    still has claimed work).  Skip-with-note when the optional coordination
    tool is absent -- the default-on skill never hard-requires it.  Invoked as
    an explicit argv list under the resolved interpreter, never a shell string
    (S2/S5).
    """
    _emit_section("active work-intents")
    intent_tool = _sibling_tool("intent.py")
    if intent_tool is None:
        _warn(
            "intent.py (coordination-tiers) not installed -- skipping the "
            "active-intent read; if your team uses work-intents, install it."
        )
        return
    try:
        proc = subprocess.run(
            [interpreter, str(intent_tool), "list"],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
            env=_git_env(),
        )
        sys.stdout.write(proc.stdout)
        if proc.returncode != 0 and proc.stderr:
            _warn(f"intent list reported: {proc.stderr.strip()}")
    except OSError as exc:
        _warn(f"could not run intent.py list: {exc}")


def _run_lifecycle_metrics(root: Path, interpreter: str) -> None:
    """Run the optional lifecycle-metrics tool with ``--snapshot``, if installed.

    Passes ``--snapshot`` so each full-handoff persists a dated CSV snapshot
    to ``dev/measurement/snapshots/<YYYY-MM-DD>-proposals.csv``.  Only runs
    in the ``--handoff`` full-handoff path (the caller in ``_do_full_handoff``
    gates it).  Skip-with-note when the tool is absent; never fails the
    handoff on a non-zero exit.
    """
    tool = _sibling_tool("lifecycle_metrics.py")
    if tool is None:
        _warn("lifecycle_metrics.py not installed -- skipping the metrics pass.")
        return
    try:
        proc = subprocess.run(
            [interpreter, str(tool), "proposals", "--snapshot"],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
            env=_git_env(),
        )
        if proc.returncode == 0:
            snap_note = (proc.stderr or "").strip()
            _emit(
                f"lifecycle-metrics: ran with --snapshot."
                + (f"  {snap_note}" if snap_note else "")
            )
        else:
            _warn(f"lifecycle_metrics reported: {(proc.stderr or '').strip()}")
    except OSError as exc:
        _warn(f"could not run lifecycle_metrics.py: {exc}")


def _run_evolution_infer(root: Path, interpreter: str) -> None:
    """Run the deterministic rate-limit-gate / fold-up-backlog checker
    (``evolution_infer.py``) read-only, if installed.

    Zero-token, deterministic decision-support (self-evolution-loop Part B):
    surfaces rate-limit suggestions + a fold-up-backlog alarm. Skip-with-note
    when absent; never fails the handoff. The checker emits suggestions only --
    it mutates nothing. A non-zero exit (a fail-closed tracker) is surfaced as a
    note, not a failure."""
    tool = _sibling_tool("evolution_infer.py")
    if tool is None:
        _warn(
            "evolution_infer.py not installed -- skipping the rate-limit-gate "
            "/ backlog check."
        )
        return
    try:
        proc = subprocess.run(
            [interpreter, str(tool)],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
            env=_git_env(),
        )
        if proc.stdout:
            sys.stdout.write(proc.stdout)
        if proc.returncode != 0 and proc.stderr:
            _warn(f"evolution_infer reported: {proc.stderr.strip()}")
    except OSError as exc:
        _warn(f"could not run evolution_infer.py: {exc}")


def _surface_foldback_candidates(root: Path, interpreter: str) -> None:
    """Surface aging fold-back candidates via foldback_suggest.py, if installed.

    Read-only: installed at ``scripts/foldback_suggest.py`` (the module
    installs into ``scripts/``, not ``tools/``).  Skip-with-note when absent
    so the full-handoff path is never blocked by an optional module.  Never
    crashes the handoff: both a missing tool and a nonzero exit code are
    surfaced as notes, not failures.
    """
    _emit_section("aging fold-back candidates")
    tool = root / "scripts" / "foldback_suggest.py"
    if not tool.is_file():
        _warn(
            "scripts/foldback_suggest.py not installed -- skipping the "
            "fold-back surfacing pass; install the fold-back-ledger module "
            "to enable it."
        )
        return
    try:
        proc = subprocess.run(
            [interpreter, str(tool)],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
            env=_git_env(),
        )
        sys.stdout.write(proc.stdout)
        if proc.returncode != 0 and proc.stderr:
            _warn(
                f"foldback_suggest reported: {proc.stderr.strip()}"
            )
    except OSError as exc:
        _warn(f"could not run scripts/foldback_suggest.py: {exc}")


# --- subcommand: session-end -------------------------------------------------

_REFLECTION_SKELETON = """\
# Session reflection -- {agent} -- {date} (session {session})

<!-- Per-agent, ephemeral, pruned.  Migrate durable observations out into
     doctrine or the roadmap before they are pruned.  See
     doctrine/session-routines.md > "The reflections channel". -->

## What shipped

## What went well

## What went wrong -- and the lesson

## Open threads / handoffs
"""


def _reflections_dir(root: Path) -> Path:
    return root / "dev" / "reflections"


def _do_reflection(root: Path, dry_run: bool) -> None:
    """Scaffold the per-session reflection file (non-destructive; both modes)."""
    refl_dir = _reflections_dir(root)
    agent = _resolve_agent(root)
    session = _resolve_session(root)
    # <date>-<agent>-<session>.md (#46/#50): the <session> segment keeps
    # concurrent same-agent sessions from clobbering one reflection; the
    # goodnight reader globs <date>-*.md to gather every session.
    target = refl_dir / f"{_today()}-{agent}-{session}.md"
    _assert_within(target, refl_dir)  # S3: never write outside dev/reflections/

    _emit_section("reflection scaffold")
    if target.exists():
        _emit(
            f"reflection already exists: {target.relative_to(root)} "
            "-- leaving it untouched; edit it directly."
        )
    elif dry_run:
        _emit(f"[dry-run] would create reflection scaffold: "
              f"{target.relative_to(root)}")
    else:
        if not refl_dir.is_dir():
            # The reflections dir is normally seeded at scaffold time; create it
            # defensively rather than failing the goodnight on a missing dir.
            refl_dir.mkdir(parents=True, exist_ok=True)
            _warn(f"created missing reflections directory: "
                  f"{refl_dir.relative_to(root)}")
        target.write_text(
            _REFLECTION_SKELETON.format(
                agent=agent, date=_today(), session=session),
            encoding="utf-8",
        )
        _emit(f"wrote reflection scaffold: {target.relative_to(root)} "
              "-- fill in what you shipped and learned.")


def _do_thread_survey(root: Path) -> None:
    _emit_section("open threads to note in your reflection")
    threads = _in_flight(root)
    if threads:
        for line in threads:
            print(f"{_PREFIX}   {line}")
    else:
        print(f"{_PREFIX} (no open proposals or plans)")


def cmd_session_end(args: argparse.Namespace) -> int:
    """Goodnight.  Reflection-only by default; full handoff under `--handoff`.

    Reflection-only (the safe default, the portable Layer-2 guarantee): scaffold
    the reflection + survey open threads -- both non-destructive, so even if a
    non-Claude harness ignores `disable-model-invocation` and auto-fires this,
    the worst case is a stray reflection file, never a roadmap scrub.

    Full handoff (`--handoff`): the mechanizable destructive steps (prune
    reflections, run metrics, surface intents) run **only** behind (1) a
    mutation manifest, (2) the maintainer-designation marker (S6), and (3) the
    fail-closed concurrent-handoff lock (II2/S1).  The roadmap scrub +
    NEXT_SESSION rewrite + handoff commit remain the owner's judgment steps.
    """
    root = _repo_root()

    # Reflection-only work runs in BOTH modes -- every agent reflects.
    _do_reflection(root, args.dry_run)
    _do_thread_survey(root)

    if not args.handoff:
        _emit(
            "reflection-only goodnight complete.  The full handoff (roadmap "
            "scrub, NEXT_SESSION rewrite, prune, metrics, handoff commit) is a "
            "designated-owner action under `--handoff`."
        )
        return 0

    return _do_full_handoff(root, args)


def _do_full_handoff(root: Path, args: argparse.Namespace) -> int:
    """The guarded destructive path: manifest -> marker -> lock -> steps."""
    grace = args.reflection_grace_days

    # S6: always emit the mutation manifest before any real run.
    _emit_section("full-handoff mutation manifest")
    would_prune = _prune_reflections(root, grace, dry_run=True)
    names = ", ".join(p.name for p in would_prune) or "(none)"
    _emit(f"would prune {len(would_prune)} reflection(s) older than {grace}d: "
          f"{names}")
    _emit("would run lifecycle-metrics (read-only) if installed")
    _emit("would surface active intents (read-only) if installed")
    _emit("would surface aging fold-back candidates (read-only) if installed")
    _emit("would run the rate-limit-gate / backlog check (read-only) if installed")

    if args.dry_run:
        _emit("[dry-run] manifest only -- nothing mutated, no marker required.")
        return 0

    # S6: the marker is an anti-accidental-run gate (not an authorization
    # control).  Refuse non-interactively -- never block on input (R5).
    if not _designation_marker_present(root):
        raise LifecycleError(
            "refusing the full handoff: no maintainer-designation marker. Set "
            "CAIRN_HANDOFF_OWNER=1 (or create dev/.cairn/handoff-owner) to run "
            "as the designated single owner. This is an anti-accidental-run "
            "gate, not an authorization control -- run with --dry-run to "
            "preview the manifest first."
        )

    interpreter, _ = _resolve_interpreter(root)

    # II2/S1: fail-closed concurrent-handoff lock; released on clean exit AND
    # exception (the context manager's __exit__, EP1).
    with HandoffLock(root, _resolve_agent(root)) as lock:
        _emit_section("pruning reflections")
        pruned = _prune_reflections(root, grace, dry_run=False)
        _emit(f"pruned {len(pruned)} reflection(s) older than {grace}d.")
        lock.heartbeat()

        _emit_section("lifecycle metrics")
        _run_lifecycle_metrics(root, interpreter)
        lock.heartbeat()

        # Coordination-safety check: whether another session still holds claimed
        # work (read-only).  Mirrors the manifest line above (finding 2).
        _surface_intents(root, interpreter)
        lock.heartbeat()

        # Fold-back surfacing -- gated behind --handoff (F5 binding): fires
        # only in the full-handoff path, never in the reflection-only goodnight.
        _surface_foldback_candidates(root, interpreter)
        lock.heartbeat()

        # Standing capture prompt (F5): invite the owner to scan today's
        # doctrine activity for Cairn-portable fold-back candidates.
        _emit(
            "scan today's doctrine activity for Cairn-portable fold-back "
            "candidates? (capture stays judgment -- an empty capture is "
            "success; never manufacture marginal candidates)"
        )

        # Rate-limit-gate + fold-up-backlog check -- deterministic, zero-token,
        # read-only decision-support (it emits suggestions only, mutates nothing).
        _emit_section("rate-limit gate + fold-up backlog")
        _run_evolution_infer(root, interpreter)

    _emit(
        "full-handoff mechanizable steps complete.  The roadmap scrub, "
        "NEXT_SESSION rewrite, and handoff commit are your judgment steps."
    )
    return 0


# --- argument parsing --------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lifecycle",
        description=(
            "Deterministic backend for Cairn's session-start / session-end "
            "skills.  Read-only orientation and reflection-only goodnight; "
            "no network."
        ),
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_start = sub.add_parser(
        "session-start",
        help="Read-only orientation gather (commits, tree state, threads, "
             "intents).",
    )
    p_start.add_argument(
        "--handoff-marker",
        default="Goodnight",
        help="Commit-subject prefix marking the last handoff. "
             "Default: 'Goodnight'.",
    )
    p_start.add_argument(
        "--fallback-commits",
        type=int,
        default=15,
        help="How many recent commits to show when no handoff marker exists "
             "in history (EP4 graceful fallback). Default: 15.",
    )
    p_start.set_defaults(func=cmd_session_start)

    p_end = sub.add_parser(
        "session-end",
        help="Goodnight.  Reflection-only by default; the full handoff is "
             "gated behind --handoff + a designation marker + a "
             "concurrent-handoff lock.",
    )
    p_end.add_argument(
        "--handoff",
        action="store_true",
        help="Run the full-handoff path (designated owner only): emits a "
             "mutation manifest, then -- with the designation marker and the "
             "concurrent-handoff lock -- runs the destructive steps. Refuses "
             "non-interactively without the marker.",
    )
    p_end.add_argument(
        "--reflection-grace-days",
        type=int,
        default=_REFLECTION_GRACE_DAYS,
        help=f"Full-handoff prune horizon for reflections. "
             f"Default: {_REFLECTION_GRACE_DAYS}.",
    )
    p_end.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned writes / a full-handoff mutation manifest and exit "
             "without writing anything.",
    )
    p_end.set_defaults(func=cmd_session_end)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except LifecycleError as exc:
        print(f"{_PREFIX} ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
