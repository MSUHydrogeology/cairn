#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

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
  handoff files, and (optionally) the intents log -- nothing else.  Read versus
  write, stated because listing them together previously read as write access to
  all three: reflections and handoff files are *written*; the intents log is
  *read* everywhere except the full handoff, which **prunes released pairs** from
  it (see ``_prune_intents``).
* **Reflection-only by default.**  `session-end` performs only non-destructive
  work (it *creates* a reflection scaffold and *reads* the board); the
  destructive full-handoff path (prune reflections, run metrics, surface
  intents) is gated behind an explicit `--handoff` plus a maintainer-designation
  marker and a fail-closed concurrent-handoff lock.  Without the marker
  `--handoff` refuses non-interactively; `--handoff --dry-run` prints a mutation
  manifest and changes nothing.  So even if a harness ignores
  `disable-model-invocation` and auto-fires `session-end`, the worst case is a
  stray reflection file, never a roadmap scrub.

`session-end` honors `--dry-run`: it prints the planned writes and exits
writing nothing. `session-start` has no `--dry-run` -- it performs one
write regardless, the idempotent skills fan-out self-heal (never anything
else); see `cmd_session_start` below.  `pilot-record` also honors `--dry-run`
(it prints the event block it would append and writes nothing).

Two further subcommands carry the **monitoring-evidence** window for the
review allocation -- `pilot-report` (derives, writes nothing) and
`pilot-record` (the ledger's only writer).  They measure a policy that is
already in force; an absent activation record means *no evidence yet*, never
that the review policy is off.  See the section comment above
``_validated_planner_path`` for the whole contract.

Two further subcommands are the lifecycle's **read-only navigation** surface --
`review-brief` (extracts one artifact's review surface) and `closeout
--dry-run` (the plan archive completeness preflight).  Neither writes, moves,
commits, runs tests, or decides whether evidence is competent; both are
deterministic, offline, standard-library-only extractors whose output derives
only from repository bytes, git metadata and their arguments.  See the
section comment below.

Run:
    python tools/lifecycle.py session-start
    python tools/lifecycle.py session-end [--dry-run]
    python tools/lifecycle.py pilot-report
    python tools/lifecycle.py pilot-record --kind <kind> ... [--dry-run]
    python tools/lifecycle.py review-brief <artifact> [--format json]
    python tools/lifecycle.py closeout <plan> --dry-run [--format json]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util as _importlib_util
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

#: Released claim/release *pairs* older than this are pruned from the work-intent
#: coordination surface at full handoff.  Independent of the reflection window on
#: purpose: a reflection is a document, a claim is a lock.  Never applied to an
#: *unreleased* claim -- that is a session that died holding a lock, so it is
#: reported instead (proposal 2026-08-11-claude-intent-ledger-pruning).
_INTENT_GRACE_DAYS = 30

#: A handoff lease is considered *expired* after this many seconds without a
#: heartbeat refresh.  Expiry alone never reclaims a lock -- it is one of two
#: conditions; the other is affirmative proof the holder is dead.
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


#: How many *encoded* characters one field may contribute before the tail is
#: elided.  Counted after encoding, never before: the marker is unauthenticated
#: and a source-length cap would let one crafted character buy 10 columns.
_FIELD_LIMIT = 200


def _safe_field(value, *, limit=_FIELD_LIMIT):
    """Render one externally sourced single-line value inert for the stream.

    **The escaping rule is `tools/lifecycle_planner.py`'s `encode_display`, and
    this function no longer owns one.**  The encoder moved out of
    `dev/plans/review-efficient-lifecycle.md`: *"human output passes through the
    **same** terminal encoder as the board ... The existing `_safe_field` is **not**
    this rule -- it translates a fixed escape table and truncates; it applies
    neither `str.isprintable()` nor `_DISPLAY_UNSAFE_RANGES` -- and is replaced,
    not wrapped."*

    What that fixed table missed is not hypothetical: the combining grapheme
    joiner, the Hangul fillers, the variation selectors and the whole Tag block
    are `Mn`/`Lo`, so `str.isprintable()` calls them printable and the old table
    listed none of them -- they reached a terminal raw.  One encoder means there
    is no second, weaker path, and the board's directional drift test
    (`bootstrap/tests/test_lifecycle_board.py`) is what keeps the range table
    ahead of the content scanner for **both** consumers at once.

    **Elision is layered OUTSIDE the encoder, not folded into it** (the same
    cell).  It is a display concern with its own oracle -- a hostile
    4,000-character `**Status**:` value must not own the terminal -- and folding
    a length rule into a code-point rule is how one of them comes to be
    reasoned about as if it were the other.  So the encoder runs first over the
    whole value and the cut is taken from its output, which also makes the cut
    unable to split a *source* character into a half-escape that reads as
    something else.

    An unloadable vocabulary **refuses** (`VocabularyUnavailable`, a
    `LifecycleError` -> exit 1 with the reason).  That is the loader contract's
    own direction and it is deliberate here: the alternative -- falling back to
    a local escape table when the shared encoder cannot be reached -- is exactly
    the second, weaker path this change removes, and it would appear precisely
    when something is already wrong with the install.
    """
    text = _vocabulary().encode_display(str(value))
    if limit is not None and len(text) > limit:
        return text[:limit] + "...[+%d chars elided]" % (len(text) - limit)
    return text


def _safe_stream(text: str) -> str:
    """Render a multi-line relay inert while preserving its real line breaks."""
    # split("\n"), never splitlines(): the latter recognizes the separators
    # this helper escapes and would turn attacker-controlled data into lines.
    return "\n".join(_safe_field(line, limit=None) for line in text.split("\n"))


def _emit_section(title: str) -> None:
    """Print a section header so the relayed output is legibly grouped."""
    print(f"\n{_PREFIX} == {title} ==")


def _warn(message: str) -> None:
    """Print a non-fatal advisory to stderr (a skipped optional step, etc.)."""
    print(f"{_PREFIX} NOTE: {message}", file=sys.stderr)


_STALE_WARNED = False


def _warn_stale_once(message: str) -> None:
    """Emit a stale-interpreter warning at most once per process.

    The interpreter resolver is reached up to four times in one
    ``session-end --handoff`` (measured chain: ``_intent_whoami``,
    ``cmd_session_start``, ``_do_reflection``, ``_do_full_handoff``).
    Without this guard an adopter would see the remedy repeated up to four
    times, aggravating alarm fatigue on the one remaining detection signal
    for an absent-path tamper.
    """
    global _STALE_WARNED
    if _STALE_WARNED:
        return
    _STALE_WARNED = True
    _warn(message)


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
            check=True,
            env=_git_env(),
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or b"").decode("utf-8", "replace").strip()
        detail = detail or f"git {' '.join(args)} failed"
        raise LifecycleError(detail) from exc
    text = out.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    return _safe_stream(text)


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
    except LifecycleError as exc:
        _warn(
            f"interpreter binding refused ({exc}); running the optional "
            f"intent tool under the current interpreter instead."
        )
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
    (path-containment).  An empty / fully-stripped value falls back to
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
    Sanitized to a filename-safe slug (path-containment).
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
    """Fail closed if `path` would resolve outside `base` (path-containment).

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


_REBIND_REMEDY = (
    "To refresh the binding: delete dev/.cairn/local-env.json, THEN re-run the "
    "Cairn scaffold install against this repo.  Deletion is what makes the "
    "install write a fresh binding -- re-running with the file still present "
    "preserves the stale one, and --force is neither needed nor advised (it "
    "overwrites your whole customized tree).  A bare delete alone leaves the "
    "routines on the current-interpreter fallback."
)


def _probe_interpreter(interp: Path) -> str:
    """Classify a recorded path: "symlinked" / "absent" / "present".

    Every inspection step lives here so the caller wraps the whole
    classification in one ``except OSError``.  The symlink walk itself raises
    on an unreadable parent, so guarding only the ``stat()`` probe would leave
    that case an uncaught traceback.
    """
    if _has_symlink_component(interp):        # may raise OSError
        return "symlinked"
    try:
        interp.stat()
    except (FileNotFoundError, NotADirectoryError):
        return "absent"
    return "present"


def _resolve_interpreter(root: Path) -> Tuple[str, str]:
    """Resolve the project interpreter the routines invoke sub-tools with.

    Resolve-don't-bake (Decision 6 / R3): the interpreter binding lives in an
    **untracked** ``dev/.cairn/local-env.json`` written at bootstrap, never
    baked into a tracked file.

    **The trust-root contract, corrected on the record (S1).**
    ``dev/.cairn/local-env.json`` is an **operationally trusted executable
    binding**.  It is untracked, gitignored, mutable, and not
    lockfile-covered, so at read time it is user-controlled and carries no
    provenance or integrity signal.  ``_resolve_interpreter`` is a strict
    **shape validator, not an authenticator**: it enforces absoluteness, a
    single-key schema, control-char rejection, no parent-traversal (``..``)
    segment, symlink-freedom, existence, and the executable bit -- but it
    checks **neither Python identity nor binary provenance**.  Any absolute,
    present, non-symlinked, executable regular file is accepted and
    executed.

    A structurally-valid-but-absent path **degrades** with a warning
    (``"fallback-stale"``, below).  Every other violation **refuses before
    running anything** (a `LifecycleError`) at every call site **except**
    ``_intent_whoami``'s optional-tool fallback, which surfaces the refusal
    as a warning and continues under the current interpreter (the intent
    tool is optional and repository-controlled).

    Returns ``(interpreter_path, source)`` where source is ``"local-env.json"``
    or ``"fallback"``.  When the config is absent, the **runtime resolver
    fallback** is the interpreter currently running this CLI -- safe because
    *this* tool is standard-library only, a rationale scoped to this tool's
    own execution and not to whatever sub-tool the resolved interpreter is
    later used to run (R7) -- and the caller surfaces install guidance so the
    hidden binding is never silently assumed.
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
    # dirs).  An appended-argument string like "/usr/bin/python -c ..." is not
    # a real path (nothing exists there), so under the revised classifier it
    # DEGRADES as an absent path -- it is never executed, only named in a
    # warning -- not "caught" by any fatal check (finding 1; corrected R2/R6).
    if any(ord(ch) < 0x20 or ch == "\x7f" for ch in value):
        raise LifecycleError(
            f'{cfg}: "interpreter" must not contain control characters.'
        )
    interp = Path(value)
    if not interp.is_absolute():
        raise LifecycleError(f'{cfg}: "interpreter" must be an absolute path.')
    if ".." in interp.parts:
        raise LifecycleError(
            f'{cfg}: "interpreter" must not contain a parent-traversal '
            f"(..) segment: {interp}.  {_REBIND_REMEDY}"
        )
    try:
        shape = _probe_interpreter(interp)
    except OSError as exc:                     # EACCES / ELOOP / ENAMETOOLONG
        raise LifecycleError(
            f'{cfg}: "interpreter" could not be inspected ({exc}): {interp}.  '
            f"Refusing rather than guessing.  {_REBIND_REMEDY}"
        ) from exc
    if shape == "symlinked":
        raise LifecycleError(
            f'{cfg}: "interpreter" must not be reached through a symlink '
            f"(leaf or parent).  {_REBIND_REMEDY}"
        )
    if shape == "absent":
        _warn_stale_once(
            f'{cfg}: recorded interpreter "{interp}" no longer exists -- your '
            f"environment was likely rebuilt.  Using the current interpreter "
            f"({sys.executable}) for this run.  {_REBIND_REMEDY}"
        )
        return sys.executable, "fallback-stale"
    if not interp.is_file() or not os.access(interp, os.X_OK):
        raise LifecycleError(
            f'{cfg}: "interpreter" is not an executable file: {interp}.  '
            f"{_REBIND_REMEDY}"
        )
    return str(interp), "local-env.json"


# --- in-flight thread survey -------------------------------------------------

_LINE_ENDING_RE = re.compile(r"\r\n?|\n")


def _split_lines(text: str) -> List[str]:
    """Split on markdown line endings with ``str.splitlines`` tail semantics."""
    if not text:
        return []
    lines = _LINE_ENDING_RE.split(text)
    if lines[-1] == "":
        lines.pop()
    return lines


def _status_of(path: Path) -> str:
    """Best-effort read of a proposal/plan ``**Status**:`` line for the survey."""
    try:
        for line in _split_lines(path.read_text(encoding="utf-8"))[:40]:
            stripped = line.strip()
            low = stripped.lower()
            if low.startswith("**status**:") or low.startswith("status:"):
                value = stripped.split(":", 1)[1].strip().strip("*").strip()
                return value or "(unspecified)"
    except (OSError, UnicodeError):
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
            lines.append(
                f"{kind}/{_safe_field(path.name)} -- "
                f"{_safe_field(_status_of(path))}"
            )
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
    resolving **outside** *target*.  ``dst`` itself may be the symlink we
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
    # has already reported clean.
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
            _emit(f"{_safe_field(name)}: {tier} -> {st}")

    _emit_section(f"commits since last '{marker}' handoff")
    last_handoff = _git(
        ["log", f"--grep=^{marker}", "--format=%H", "-n", "1"], root
    ).strip()
    if last_handoff:
        rng = f"{last_handoff}..HEAD"
        log = _git(["log", rng, "--format=%h %an  %s"], root).strip()
        _emit(f"range {rng}")
    else:
        # A freshly-bootstrapped repo has no handoff commit yet -- fall
        # back to a sensible window rather than crashing on an empty range.
        log = _git(["log", f"-n{fallback_n}", "--format=%h %an  %s"], root).strip()
        _warn(
            f"no '{marker}' commit found in history; showing the last "
            f"{fallback_n} commits instead (likely a freshly-bootstrapped repo)."
        )
    print(log if log else f"{_PREFIX} (no commits in range)")

    _emit_section("working-tree state (git status --short)")
    status = _git(["-c", "core.quotePath=false", "status", "--short"], root).strip()
    print(status if status else f"{_PREFIX} (clean working tree)")

    _emit_section("in-flight threads (open proposals / plans)")
    threads = _in_flight(root)
    if threads:
        for line in threads:
            print(f"{_PREFIX}   {line}")
    else:
        print(f"{_PREFIX} (no open proposals or plans)")

    # Resolve the project interpreter (resolve-don't-bake); a tampered
    # local-env.json refuses here, before any sub-tool runs.
    interpreter, interp_source = _resolve_interpreter(root)

    _surface_intents(root, interpreter)

    # Make the (otherwise hidden) interpreter trust root visible.
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
    """Whether the maintainer-designation marker is set.

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

    A local atomic lockfile -- the only
    race-free mutual-exclusion primitive (an intents-log read carries a TOCTOU
    race).  The stale-lock escape is **not age-only**: a held lock is
    reclaimed *only* when the lease has expired **and** the holder is provably
    dead (same host, pid gone).  Cross-host locks, live holders, and fresh
    leases all **fail closed**; a genuinely stuck lock needs manual cleanup.

    Used as a context manager so the lockfile is removed on **both clean exit
    and unexpected exception**.
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
        self.release()  # released on clean exit AND exception
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


def _prune_intents(root: Path, interpreter: str, days: int, *,
                   dry_run: bool) -> None:
    """Prune released claim/release pairs from the intent log, if installed.

    Full-handoff only.  The intent log is a coordination surface, not an
    archive, and the tool that owns it does the pruning -- invoked as a
    subprocess exactly like :func:`_surface_intents`, so this module never
    imports the intent engine.  The command refuses on its own if any claim is
    still active, and it never deletes an unreleased claim or an unparseable
    line; both are reported.
    """
    _emit_section("pruning the work-intent surface")
    # Resolve against *root*, the way _surface_foldback_candidates does, not via
    # _sibling_tool -- which returns the copy beside THIS file regardless of the
    # target root.  That distinction is invisible in an adopter tree (the CLI is
    # installed in the tree it operates on) but it matters here: the intent
    # engine computes its ledger path from its OWN location, so a root-blind
    # lookup would rewrite the installing tree's ledger while reporting on the
    # target.  It also made this wiring untestable, which is why review could
    # replace the call with `pass` and see every suite stay green.
    intent_tool = root / "tools" / "intent.py"
    if not intent_tool.is_file():
        intent_tool = _sibling_tool("intent.py")
    if intent_tool is None or not intent_tool.is_file():
        _warn("intent.py (coordination-tiers) not installed -- skipping.")
        return
    argv = [interpreter, str(intent_tool), "prune", "--older-than-days",
            str(days)]
    if dry_run:
        argv.append("--dry-run")
    try:
        proc = subprocess.run(
            argv, cwd=str(root), capture_output=True, text=True, check=False,
            env=_git_env(),
        )
        sys.stdout.write(proc.stdout)
        if proc.returncode != 0 and proc.stderr:
            _warn(proc.stderr.strip())
    except OSError as exc:  # pragma: no cover -- defensive
        _warn(f"intent prune failed to run: {exc}")


def _surface_intents(root: Path, interpreter: str) -> None:
    """Read-only surface of active work-intents, if intent.py is installed.

    Used by both `session-start` (who holds which paths before the first edit)
    and the full handoff (a coordination-safety check: whether another session
    still has claimed work).  Skip-with-note when the optional coordination
    tool is absent -- the default-on skill never hard-requires it.  Invoked as
    an explicit argv list under the resolved interpreter, never a shell string
    (the interpreter-binding contract).
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

    Passes ``--snapshot`` so each full-handoff persists an indexed CSV
    snapshot to ``dev/measurement/snapshots/<YYYY-MM-DD>-<N>.csv`` (the
    unified proposal+plan schema; same-day runs coalesce by ``N`` rather
    than overwriting, preserving the audit trail).  Only runs in the
    ``--handoff`` full-handoff path (the caller in ``_do_full_handoff``
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
    _assert_within(target, refl_dir)  # never write outside dev/reflections/

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
    mutation manifest, (2) the maintainer-designation marker, and (3) the
    fail-closed concurrent-handoff lock.  The roadmap scrub +
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

    # Always emit the mutation manifest before any real run.
    _emit_section("full-handoff mutation manifest")
    would_prune = _prune_reflections(root, grace, dry_run=True)
    names = ", ".join(p.name for p in would_prune) or "(none)"
    _emit(f"would prune {len(would_prune)} reflection(s) older than {grace}d: "
          f"{names}")
    _emit("would run lifecycle-metrics (read-only) if installed")
    _emit("would surface active intents (read-only) if installed")
    _emit(f"would prune released work-intent pairs older than "
          f"{args.intent_grace_days}d (never an unreleased claim) if installed")
    _emit("would surface aging fold-back candidates (read-only) if installed")
    _emit("would run the rate-limit-gate / backlog check (read-only) if installed")

    if args.dry_run:
        _emit("[dry-run] manifest only -- nothing mutated, no marker required.")
        return 0

    # The marker is an anti-accidental-run gate (not an authorization
    # control).  Refuse non-interactively -- never block on input.
    if not _designation_marker_present(root):
        raise LifecycleError(
            "refusing the full handoff: no maintainer-designation marker. Set "
            "CAIRN_HANDOFF_OWNER=1 (or create dev/.cairn/handoff-owner) to run "
            "as the designated single owner. This is an anti-accidental-run "
            "gate, not an authorization control -- run with --dry-run to "
            "preview the manifest first."
        )

    interpreter, _ = _resolve_interpreter(root)

    # Fail-closed concurrent-handoff lock; released on clean exit AND
    # exception (the context manager's __exit__).
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

        # Destructive, and deliberately AFTER the read-only surface above so the
        # operator sees the live state before anything is removed.  Runs under
        # the handoff lock: the prune rewrites a file whose concurrent-append
        # atomicity is best-effort, so a live appender could otherwise lose a
        # claim (and a lost claim is a lost lock).
        _prune_intents(root, interpreter, args.intent_grace_days, dry_run=False)
        lock.heartbeat()

        # Fold-back surfacing -- gated behind --handoff: fires
        # only in the full-handoff path, never in the reflection-only goodnight.
        _surface_foldback_candidates(root, interpreter)
        lock.heartbeat()

        # Standing capture prompt: invite the owner to scan today's
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


# --- monitoring evidence: the review-allocation window -----------------------
#
# Chunk P6a of `dev/plans/review-efficient-lifecycle.md`, as revised by that
# plan's "Maintainer-directed contract revision -- 2026-08-11" (cell `P6-R`).
#
# **Direction first, because it is the one prohibition the revision states on
# this code.**  The proposal-centered review allocation is ALREADY the default.
# What these two subcommands measure is therefore a live policy, not a candidate
# waiting for permission from its own pilot:
#
#     no activation record  ==  no monitoring evidence yet
#     no activation record  !=  the review policy is disabled
#
# Nothing here may read the second line.  `P6-R`, verbatim: "No reader or writer
# may treat absent monitoring activation as disabling the review policy."  The
# token `promote` is retired (`M6-R`); the Decision at the monitoring boundary is
# `retain | revise | retire`.
#
# **Two records, and the split is the security property** (the plan's Security
# rounds 2 and 1).  A single mutable JSON state file
# -- the shape this replaces -- is last-writer-wins, and "six plans reached the
# boundary" is not a claim a last-writer-wins file can support:
#
#   * `dev/measurement/pilot-activation.md` -- an IMMUTABLE tracked activation
#     record.  It names `machinery_sha` (the reviewed Boundary-B2 commit) and
#     the evidence record that attests it.  It does **not** name the enabling
#     commit or the activation date: both are DERIVED from git as the commit
#     that first introduced this exact blob, and that commit's author date.
#     Storing either would be self-referential -- a commit cannot contain its
#     own id -- which is exactly the circularity that refused.
#   * `dev/measurement/pilot-events.md` -- an APPEND-ONLY tracked event ledger,
#     one block per counted plan stem or pause, each bound to its source
#     artifact and source commit.  Counts, pause state and the whole report are
#     DERIVED from it and never stored: a stored count is a second authority
#     that can disagree with the ledger.
#
# The quota and the window length are CONTRACT, so they are constants here.  A
# data file that could restate them would be a record rewriting its own rule.
#
# **This file introduces neither record.**  The ledger ships with P6a carrying
# zero events; the activation record is introduced later by P6d, the data-only
# commit at the Maintainer fence, because `machinery_sha` is the Boundary-B
# commit and that commit does not exist while P6a is being written.  Fabricating
# a placeholder SHA here would put a false attestation in the tracked record.
#
# ---------------------------------------------------------------------------
# The one runtime status vocabulary -- contained loader (third consumer)
# ---------------------------------------------------------------------------
#
# `lifecycle-status-vocabulary`, under its accepted "contained consumers and
# corpus boundary" replacement; the same loader
# contract `scripts/transition_lint.py` and `tools/_lifecycle_metrics/
# extract.py` implement.  The contract is restated here **per consumer** rather
# than inherited by implication, because the containment is the security
# property and a reader of this file must be able to check it without opening
# either of the other two.
#
# Why this file needs the vocabulary at all: the six-plan rule counts distinct
# plan stems that reached one named plan state.  Naming that state locally would
# fork the vocabulary Chunk A exists to keep single -- so the state is a lookup
# key validated against the planner, and `bootstrap/tests/
# test_lifecycle_vocabulary.py` audits this file's source for a local enum.
#
# The rules, each implemented below:
#   * the path is the SIBLING `lifecycle_planner.py`, derived from THIS file's
#     own **unresolved** location -- never from ambient `sys.path`, and no
#     `tools/__init__.py` is created to manufacture a package.  Unresolved is
#     load-bearing: a resolved path can never be a symlink, so a guard asking
#     that question of one is dead by construction (found by the loader matrix
#     in both existing consumers, fixed at `94bda8b`);
#   * before execution: refuse a missing or unreadable planner, a symlinked
#     planner, a symlinked containing directory, and any planner whose
#     resolution lands outside the expected root -- comparing **resolved** forms
#     on both sides, so a checkout under a symlinked ancestor (macOS's
#     `/tmp -> /private/tmp`) is not falsely refused;
#   * a fixed private module name, registered in `sys.modules` before
#     `exec_module` (some decorators resolve a loading module's own name
#     through it), and purged with every child on failure;
#   * cache only a FULLY initialized module carrying our completion sentinel --
#     presence in `sys.modules` is not initialization;
#   * a pre-existing entry under that name is never trusted merely for being
#     present -- it passes the same identity checks or it is replaced;
#   * every validation `OSError` is a clean refusal, never a traceback and
#     never a fallback to a local literal.
#
# Both installed copies satisfy the sibling requirement: `tools/lifecycle.py`
# beside `tools/lifecycle_planner.py`, and this file's byte-identical template
# twin `templates/skills/_lib/lifecycle.py` beside `templates/skills/_lib/
# lifecycle_planner.py`.  (Unlike `_lifecycle_metrics/extract.py`, whose twin
# has no planner at its source location and therefore refuses there.)


class VocabularyUnavailable(LifecycleError):
    """The single status vocabulary could not be loaded *safely*.

    A `LifecycleError` because it is actionable and fatal to whatever asked:
    the alternative -- falling back to a local status literal -- is the exact
    defect the single-vocabulary rule removes.
    """


class MonitoringIncomplete(RuntimeError):
    """A monitoring derivation cannot be completed, and says why.

    Distinct from `LifecycleError` on purpose.  `LifecycleError` is a refusal
    (bad bytes, an unsafe path, a race); this is *"the evidence is not there
    yet"* -- reported with its reason and a non-zero exit, and **never**
    rendered as a clean report or as "the policy is off".
    """


#: Fixed private name.  Fixed so a poisoned entry is *detectable* at a known
#: key; private so it cannot be mistaken for an importable module.
_PLANNER_MODULE_NAME = "_lifecycle_cli_lifecycle_planner"

#: Set by *this* loader only after `exec_module` returned AND every required
#: export is present.
_PLANNER_SENTINEL = "__cairn_vocabulary_loaded__"

#: What this consumer actually reads.  Checked before the module is cached, so a
#: planner that loads but has lost an export is a refusal, not an
#: `AttributeError` at the first counted plan.
#:
#: **Three names here are each a vocabulary this file must not
#: own.**  `review-efficient-lifecycle` requires a counted plan's
#: resolved assurance path on its event so the report can split eligible from
#: ineligible plans.  A plan carries no assurance declaration of its own -- the
#: pinned that absence -- so the value comes from P2-R's inheritance chain, which
#: the planner owns end to end: `ASSURANCE_PATHS` is the closed vocabulary,
#: `ASSURANCE_NOT_INHERITED` the resolved third answer for a plan that declares no
#: chain, and `resolve_plan_assurance_path` the resolver.  Reading all three
#: through this loader is what keeps the CLI from re-declaring either token --
#: the second vocabulary the single-source rule forbids, and the reason P6a
#: deliberately left this open rather than closing it early.
#:
#: **Six more, and the reason is the same rule read from the other
#: end.**  `encode_display` is the one terminal encoder; every human
#: line this file prints goes through it, so it is required *unconditionally*,
#: not only by the two new subcommands.  `read_artifact` is the one artifact
#: parser -- the contract requires that *"`scan`, `next`, and accepted closeout tooling
#: consume shared predicates rather than implement three interpretations of
#: readiness"*, and the four predicates below all take the object it builds.
#: `status_evidence_violations` is the closeout preflight itself (its own
#: docstring names this caller: *"`closeout --dry-run`"*);
#: `review_record_violations`, `blocked_by_violations` and
#: `plan_inheritance_violations` are the other three the same reports read.
#: Every one of them is *the planner's*, reached through this loader -- there is
#: no second parser and no second readiness reading in this file.
_REQUIRED_EXPORTS = ("PLAN_STATES", "ASSURANCE_PATHS",
                     "ASSURANCE_NOT_INHERITED", "resolve_plan_assurance_path",
                     "encode_display", "read_artifact",
                     "status_evidence_violations", "review_record_violations",
                     "blocked_by_violations", "plan_inheritance_violations")

_planner_cache = None


def _purge_planner_module() -> None:
    """Drop the private module and every child registered under its name."""
    prefix = _PLANNER_MODULE_NAME + "."
    for name in [n for n in sys.modules
                 if n == _PLANNER_MODULE_NAME or n.startswith(prefix)]:
        sys.modules.pop(name, None)


def _validated_planner_path() -> Path:
    """The sibling planner path, or a clean refusal.  Never raises `OSError`."""
    raw = Path(__file__).absolute()
    root = raw.parent
    path = root / "lifecycle_planner.py"
    try:
        if root.is_symlink():
            raise VocabularyUnavailable(
                f"the containing directory {root} is a symlink -- refusing to "
                f"load the status vocabulary through it")
        if path.is_symlink():
            raise VocabularyUnavailable(
                f"{path} is a symlink -- refusing to load the status "
                f"vocabulary through it")
        if not path.is_file():
            raise VocabularyUnavailable(
                f"no status vocabulary beside this tool at {path} -- the "
                f"lifecycle CLI reads the plan-state vocabulary from the "
                f"planner and keeps no local copy")
        if path.resolve().parent != root.resolve():
            raise VocabularyUnavailable(
                f"{path} resolves outside the expected {root} root")
        with path.open("rb"):
            pass
    except OSError as exc:
        raise VocabularyUnavailable(
            f"cannot read the status vocabulary at {path}: {exc}") from None
    return path


def _vocabulary():
    """The planner module, loaded under containment and cached when complete."""
    global _planner_cache
    if _planner_cache is not None:
        return _planner_cache
    path = _validated_planner_path()

    existing = sys.modules.get(_PLANNER_MODULE_NAME)
    if existing is not None:
        if (getattr(existing, _PLANNER_SENTINEL, False)
                and getattr(existing, "__file__", None) == str(path)
                and all(hasattr(existing, n) for n in _REQUIRED_EXPORTS)):
            _planner_cache = existing
            return existing
        _purge_planner_module()

    spec = _importlib_util.spec_from_file_location(_PLANNER_MODULE_NAME, path)
    if spec is None or spec.loader is None:
        raise VocabularyUnavailable(f"could not build an import spec for {path}")
    module = _importlib_util.module_from_spec(spec)
    sys.modules[_PLANNER_MODULE_NAME] = module
    try:
        spec.loader.exec_module(module)
    except BaseException as exc:
        _purge_planner_module()
        raise VocabularyUnavailable(
            f"the status vocabulary at {path} failed to load: {exc!r}") from None
    missing = [n for n in _REQUIRED_EXPORTS if not hasattr(module, n)]
    if missing:
        _purge_planner_module()
        raise VocabularyUnavailable(
            f"the status vocabulary at {path} is missing {missing}")
    setattr(module, _PLANNER_SENTINEL, True)
    _planner_cache = module
    return module


#: The plan state the six-plan rule counts.  A **lookup key into the one runtime
#: vocabulary, not a local vocabulary**: nothing uses it until
#: `_counted_plan_state` has confirmed the planner declares it, so this file can
#: never disagree with `tools/lifecycle_planner.py` about which states exist --
#: it can only fail to find the one it needs.
#:
#: **It is absent from the vocabulary as this lands** -- measured 2026-08-12,
#: `PLAN_STATES == ('open', 'awaiting-plan-review', 'executing', 'review',
#: 'archived')`.  `review-efficient-lifecycle` introduces it (the
#: row: the proposal and plan state tables).  Until then every counting
#: derivation refuses and names the dependency.  It must never quietly count
#: zero: a zero from an unavailable rule is indistinguishable from a working
#: rule that found no plans, which is the silent-tool defect `AGENTS.md`
#: forbids ("a tool that returns success without testing the claimed property
#: is a worse defect than no tool, because it is silent").
#:
#: Deliberately NOT substituted by the nearest current state.  `review` is
#: today's pre-`archived` state and would make the count *run*; it would also
#: be counting a different thing than the contract says, silently.
_COUNTED_PLAN_STATE = "ready-to-archive"


def _assurance_values() -> Tuple[str, ...]:
    """The closed set an event's `assurance_path` may carry, from the vocabulary.

    Two real assurance paths plus the resolved *not-inherited* answer, all three
    read from `tools/lifecycle_planner.py`.  **Never assembled here from
    literals** -- that would be the fork this exists to avoid, and it would
    silently disagree with the planner the moment either changed.
    """
    planner = _vocabulary()
    return tuple(planner.ASSURANCE_PATHS) + (planner.ASSURANCE_NOT_INHERITED,)


def _resolved_assurance_path(root: Path, rel: str) -> str:
    """The assurance path of the plan at *rel*, or a clean refusal.

    Derived, never typed.  The reason is the one the ledger's own record gives
    for `plan_state`: a governance field a human types is an author's claim, and
    the CLI is the only writer precisely so the claim can be replaced by a
    derivation.  A plan that declares an inheritance chain the planner cannot
    resolve **refuses** -- recording `not-inherited` for it would be a quiet lie
    about which population the sample came from.
    """
    planner = _vocabulary()
    path = root / rel
    try:
        if not path.is_file():
            raise LifecycleError(
                f"cannot resolve an assurance path: {rel} is not a file in this "
                f"working tree -- a counted plan's assurance path is DERIVED "
                f"from the plan, never supplied")
    except OSError as exc:
        raise LifecycleError(f"cannot inspect {rel}: {exc}") from None
    value, problems = planner.resolve_plan_assurance_path(path)
    if value is None:
        joined = "; ".join(_safe_field(p) for p in problems) or "unknown"
        raise LifecycleError(
            f"cannot resolve the assurance path of {rel}: {joined} -- refusing "
            f"to record a counted plan whose assurance basis does not resolve")
    return value


def _counted_plan_state() -> str:
    """The counted plan state, confirmed against the one runtime vocabulary.

    Raises `MonitoringIncomplete` (not a refusal, not a silent zero) while the
    vocabulary has no such state.
    """
    states = tuple(_vocabulary().PLAN_STATES)
    if _COUNTED_PLAN_STATE not in states:
        raise MonitoringIncomplete(
            f"the six-plan counting rule keys on plan state "
            f"'{_COUNTED_PLAN_STATE}', which the single runtime vocabulary does "
            f"not declare yet (PLAN_STATES = {states}).  Chunk E of "
            f"review-efficient-lifecycle introduces it; until it lands the plan "
            f"count is UNAVAILABLE, which is not the same as zero")
    return _COUNTED_PLAN_STATE


# --- the two records: paths, bounded schemas, safe access --------------------

_PILOT_ACTIVATION_REL = ("dev", "measurement", "pilot-activation.md")
_PILOT_EVENTS_REL = ("dev", "measurement", "pilot-events.md")

_ACTIVATION_FENCE = "cairn-pilot-activation"
_EVENT_FENCE = "cairn-pilot-event"
_ACTIVATION_SCHEMA = "cairn-pilot-activation/1"

#: **Bumped to /2 to close the carried-forward obligation.**  Provisioned exactly for this: *"Closing
#: either is a `cairn-pilot-event/2` schema bump; the version field exists for
#: that, and an unknown version refuses rather than being half-read."*  The bump
#: adds one mandatory `plan-counted` key, `assurance_path`, so the derived report
#: can split eligible from ineligible plans -- the accepted parent's requirement
#: that P6a could not meet because no field carried the basis for it.  A `/1`
#: block now refuses, which is safe *and measured*: the live ledger carries **zero
#: events** (its `cairn-pilot-event` occurrences are all prose or inert
#: in-fence examples), so nothing recorded is invalidated.
_EVENT_SCHEMA = "cairn-pilot-event/2"

#: Contract, not data.  "six eligible plans or 60 days, whichever comes first"
#: is the accepted proposal's own rule; a record that could restate it would be
#: a record rewriting its rule.
_PILOT_PLAN_QUOTA = 6
_PILOT_WINDOW_DAYS = 60

#: Pause thresholds, from the accepted proposal: "A high-severity escaped
#: finding attributable to inheritance pauses the pilot immediately; two
#: lower-severity examples do the same."  P6b authors the human contract; these
#: are the numbers, here only so recorded findings that *meet* a pause condition
#: cannot sit in the ledger with no pause surfaced.
_PAUSE_HIGH_THRESHOLD = 1
_PAUSE_LOW_THRESHOLD = 2

_ACTIVATION_KEYS = ("schema", "machinery_sha", "machinery_record_path",
                    "machinery_record_section")

_EVENT_KINDS = ("plan-counted", "pause-set", "pause-cleared")
_EVENT_COMMON_KEYS = ("schema", "kind", "date", "subject", "source_artifact",
                      "source_commit")
_EVENT_KEYS = {
    "plan-counted": _EVENT_COMMON_KEYS + (
        "plan_state", "assurance_path", "review_input_bytes",
        "transitions_removed",
        "escaped_findings_high", "escaped_findings_low", "maintainer_prompts",
        "note"),
    "pause-set": _EVENT_COMMON_KEYS + ("severity", "note"),
    "pause-cleared": _EVENT_COMMON_KEYS + ("note",),
}
#: Absent is legal; present-but-malformed still refuses.  Everything else in a
#: kind's key set is mandatory, and any key outside it refuses (closed schema).
_EVENT_OPTIONAL_KEYS = ("note",)
_EVENT_NUMERIC_KEYS = ("review_input_bytes", "transitions_removed",
                       "escaped_findings_high", "escaped_findings_low",
                       "maintainer_prompts")
_PAUSE_SEVERITIES = ("high", "low")

#: Bounds.  Every one of them refuses rather than truncates: a truncated
#: governance record is a quiet lie about what was recorded.
_PILOT_VALUE_LIMIT = 200
_PILOT_MAX_BLOCKS = 200
_PILOT_NUMERIC_MAX = 10 ** 9

_PILOT_KEY_RE = re.compile(r"\A[a-z][a-z0-9_]{0,39}\Z")
_PILOT_SHA_RE = re.compile(r"\A[0-9a-f]{40}\Z")
_PILOT_DATE_RE = re.compile(r"\A\d{4}-\d{2}-\d{2}\Z")
_PILOT_SUBJECT_RE = re.compile(r"\A[a-z0-9][a-z0-9._-]{0,79}\Z")
_PILOT_PATH_RE = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._/-]{0,159}\Z")
_PILOT_SECTION_RE = re.compile(r"\A[A-Za-z0-9][ -~]{0,159}\Z")
_PILOT_NUMBER_RE = re.compile(r"\A(0|[1-9][0-9]{0,11})\Z")

#: Values are printable ASCII only, and these three are excluded on top of that:
#: a backslash so a value cannot survive one round-trip through this CLI's
#: stream escaping as different bytes; a backtick so no value can open or close
#: a fence; a pipe so a value can never be mistaken for a table cell.
_PILOT_FORBIDDEN_IN_VALUE = ("\\", "`", "|")


def _pilot_value_ok(value: str) -> bool:
    """True if `value` is inside the bounded value grammar (never raises)."""
    if not value or len(value) > _PILOT_VALUE_LIMIT:
        return False
    if any(ch in value for ch in _PILOT_FORBIDDEN_IN_VALUE):
        return False
    return all(0x20 <= ord(ch) <= 0x7E for ch in value)


def _has_symlink_component_below(path: Path, root: Path) -> bool:
    """True if `path` or any parent *up to but excluding* `root` is a symlink.

    Root-bounded on purpose.  `_has_symlink_component` walks to the filesystem
    root, which is right for the interpreter trust root (an absolute path that
    may live anywhere) and wrong here: a legitimate checkout under a symlinked
    ancestor -- macOS's `/tmp -> /private/tmp` -- would be refused as a tamper.
    What must not be a symlink is the part of the path *this repository owns*.
    """
    root_resolved = root.resolve()
    cur = path
    while True:
        # `root` itself is tested for identity BEFORE symlink-ness, and never
        # for symlink-ness: a checkout reached through a symlinked ancestor is a
        # normal way to work, and refusing it would be a false refusal dressed
        # as a security check.
        if cur == root or cur.resolve() == root_resolved:
            return False
        if cur.is_symlink():
            return True
        if cur.parent == cur:  # ran off the filesystem root: not under `root`
            return False
        cur = cur.parent


def _evidence_path(root: Path, rel_parts: Tuple[str, ...], *,
                   must_exist: bool) -> Path:
    """A monitoring-record path, or a clean refusal.

    Every writer *and* reader passes through here: repository containment, a
    regular non-symlink leaf **and** parent, no symlink anywhere in the part of
    the path this repository owns.  A reader is held to the writer's checks
    because a redirected read is how a tampered record gets believed.
    """
    path = root.joinpath(*rel_parts)
    _assert_within(path, root)
    parent = path.parent
    try:
        if _has_symlink_component_below(path, root):
            raise LifecycleError(
                f"{path} is reached through a symlink -- refusing to read or "
                f"write a monitoring record through one")
        if not parent.is_dir():
            raise LifecycleError(
                f"{parent} is not a directory -- the monitoring records live "
                f"in a tracked directory this tool never creates")
        if path.exists() and not path.is_file():
            raise LifecycleError(
                f"{path} is not a regular file -- refusing")
        if must_exist and not path.is_file():
            raise LifecycleError(f"no such monitoring record: {path}")
    except OSError as exc:
        raise LifecycleError(f"cannot inspect {path}: {exc}") from None
    return path


def _read_text_strict(path: Path) -> str:
    """Read a monitoring record as strict UTF-8, or refuse cleanly."""
    try:
        return path.read_bytes().decode("utf-8")
    except OSError as exc:
        raise LifecycleError(f"cannot read {path}: {exc}") from None
    except UnicodeError as exc:
        raise LifecycleError(
            f"{path} is not valid UTF-8 ({exc}) -- refusing") from None


def _parse_fenced_records(text: str, fence: str, where: str) -> List[dict]:
    """Parse every ```<fence> block in `text` into a bounded key/value dict.

    Strict by construction: the opening line is exactly ```<fence> at column 0,
    the closing line is exactly ```, every body line is `key: value`, keys match
    a narrow grammar and never repeat, values match the bounded value grammar,
    and an unterminated block refuses.

    **Only top-level blocks are data.**  A record's own prose header has to be
    able to *document* the schema, and a documented example that the parser then
    reads as a real event would be a record inventing its own contents.  So an
    opening fence seen while inside any other fenced block is skipped: an
    example shown inside a ```text block is inert by construction rather than by
    the author remembering to disguise it.
    """
    open_line = "```" + fence
    records: List[dict] = []
    lines = _split_lines(text)
    i = 0
    while i < len(lines):
        if lines[i] != open_line:
            if lines[i].startswith("```"):
                # Some other fenced block: skip to its close, so nothing inside
                # it is ever read as data.  An unterminated one swallows the
                # remainder, which is the fail-closed direction.
                i += 1
                while i < len(lines) and lines[i] != "```":
                    i += 1
            i += 1
            continue
        start = i + 1
        j = start
        while j < len(lines) and lines[j] != "```":
            j += 1
        if j >= len(lines):
            raise LifecycleError(
                f"{where}: unterminated ```{fence} block opened at line {i + 1}")
        record: dict = {}
        for offset, line in enumerate(lines[start:j]):
            lineno = start + offset + 1
            if ": " not in line and not line.endswith(":"):
                raise LifecycleError(
                    f"{where}:{lineno}: not a `key: value` line in a "
                    f"```{fence} block")
            key, _, value = line.partition(":")
            value = value.strip()
            if not _PILOT_KEY_RE.match(key):
                raise LifecycleError(
                    f"{where}:{lineno}: bad key {key!r} in a ```{fence} block")
            if key in record:
                raise LifecycleError(
                    f"{where}:{lineno}: duplicate key {key!r} in one "
                    f"```{fence} block")
            if not _pilot_value_ok(value):
                raise LifecycleError(
                    f"{where}:{lineno}: value for {key!r} is outside the "
                    f"bounded schema (printable ASCII, 1..{_PILOT_VALUE_LIMIT} "
                    f"chars, no backslash / backtick / pipe)")
            record[key] = value
        record["_line"] = str(i + 1)
        records.append(record)
        if len(records) > _PILOT_MAX_BLOCKS:
            raise LifecycleError(
                f"{where}: more than {_PILOT_MAX_BLOCKS} ```{fence} blocks -- "
                f"refusing to derive from an unbounded record")
        i = j + 1
    return records


def _require_exact_keys(record: dict, expected: Tuple[str, ...],
                        optional: Tuple[str, ...], where: str) -> None:
    """Closed-schema check: no unknown key, no missing mandatory key."""
    present = {k for k in record if not k.startswith("_")}
    unknown = sorted(present - set(expected))
    if unknown:
        raise LifecycleError(
            f"{where}: unknown key(s) {unknown} -- the schema is closed, so an "
            f"unrecognized key refuses rather than being ignored")
    missing = sorted(k for k in expected if k not in present and k not in optional)
    if missing:
        raise LifecycleError(f"{where}: missing mandatory key(s) {missing}")


# --- git-derived facts (all through the one read-only `_git` helper) ----------


def _git_ok(root: Path, args: List[str]) -> Optional[str]:
    """`_git` output, or `None` when git exits non-zero.

    For the questions where a non-zero exit is an *answer* ("no such object",
    "not an ancestor") rather than a breakage.  Every caller turns `None` into
    an explicit refusal or an explicit report line -- never into a default.
    """
    try:
        return _git(args, root)
    except LifecycleError:
        return None


def _blob_oid_at(root: Path, ref: str, rel: str) -> Optional[str]:
    """The blob oid of `rel` at `ref`, or `None` if it is not there."""
    out = _git_ok(root, ["rev-parse", "--verify", "--quiet", f"{ref}:{rel}"])
    if out is None:
        return None
    out = out.strip()
    return out if re.fullmatch(r"[0-9a-f]{40}", out) else None


def _worktree_blob_oid(root: Path, path: Path) -> Optional[str]:
    """The blob oid git would store for the working-tree bytes of `path`.

    Compared against `_blob_oid_at` rather than comparing file *contents*: an
    oid is a fixed-width hex string, so the comparison is byte-exact and
    unaffected by the stream sanitizing `_git` applies to its output.
    """
    out = _git_ok(root, ["hash-object", "--", str(path)])
    if out is None:
        return None
    out = out.strip()
    return out if re.fullmatch(r"[0-9a-f]{40}", out) else None


def _commit_exists(root: Path, sha: str) -> bool:
    """True if `sha` names a commit object in this repository."""
    out = _git_ok(root, ["cat-file", "-t", sha])
    return bool(out) and out.strip() == "commit"


def _is_strict_ancestor(root: Path, older: str, newer: str) -> bool:
    """True if `older` is an ancestor of `newer` and not the same commit."""
    if older == newer:
        return False
    return _git_ok(root, ["merge-base", "--is-ancestor", older, newer]) is not None


def _introducing_commit(root: Path, rel: str, blob: str) -> Optional[str]:
    """The earliest commit whose blob at `rel` is exactly `blob`.

    This is the *enabling* commit, derived rather than stored: a commit cannot
    contain its own id, so an `activation_sha` field naming the commit that
    introduces the record is unsatisfiable.  The path's own history is
    walked oldest-first and the first exact-blob match wins, so the answer is
    stable under later edits (a later edit is a different blob) and under
    reverts to the same bytes (the *first* introduction is the activation).
    """
    log = _git_ok(root, ["log", "--reverse", "--format=%H", "--", rel])
    if log is None:
        return None
    for sha in log.split():
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            continue
        if _blob_oid_at(root, sha, rel) == blob:
            return sha
    return None


def _author_date(root: Path, sha: str) -> Optional[str]:
    """`sha`'s author date as `YYYY-MM-DD`, or `None`."""
    out = _git_ok(root, ["log", "-1", "--format=%ad", "--date=short", sha])
    if out is None:
        return None
    out = out.strip()
    return out if _PILOT_DATE_RE.match(out) else None


# --- the activation record ---------------------------------------------------


def _read_activation(root: Path) -> Optional[dict]:
    """The validated activation record, or `None` when there is not one yet.

    `None` means **no monitoring evidence yet** and nothing else.  Malformed
    bytes, an unknown schema version, an unsafe path, an uncommitted record or a
    binding that does not hold all raise -- so the one thing this function can
    never do is turn a broken record into "inactive".
    """
    rel = "/".join(_PILOT_ACTIVATION_REL)
    path = root.joinpath(*_PILOT_ACTIVATION_REL)
    if not path.exists() and not path.is_symlink():
        return None
    path = _evidence_path(root, _PILOT_ACTIVATION_REL, must_exist=True)
    where = rel
    records = _parse_fenced_records(_read_text_strict(path), _ACTIVATION_FENCE,
                                    where)
    if len(records) != 1:
        raise LifecycleError(
            f"{where}: expected exactly one ```{_ACTIVATION_FENCE} block, found "
            f"{len(records)} -- an activation record with none is malformed, and "
            f"one with several has no single authority")
    record = records[0]
    _require_exact_keys(record, _ACTIVATION_KEYS, (), where)
    if record["schema"] != _ACTIVATION_SCHEMA:
        raise LifecycleError(
            f"{where}: unknown schema {record['schema']!r} -- this tool reads "
            f"{_ACTIVATION_SCHEMA} and refuses anything else.  An unreadable "
            f"activation record is NOT an inactive monitoring window and is "
            f"NOT a disabled review policy")
    if not _PILOT_SHA_RE.match(record["machinery_sha"]):
        raise LifecycleError(
            f"{where}: machinery_sha must be a full 40-character lowercase hex "
            f"commit id, got {_safe_field(record['machinery_sha'])!r}")
    if not _PILOT_PATH_RE.match(record["machinery_record_path"]) \
            or ".." in record["machinery_record_path"].split("/"):
        raise LifecycleError(
            f"{where}: machinery_record_path must be a plain repository-"
            f"relative path")
    if not _PILOT_SECTION_RE.match(record["machinery_record_section"]):
        raise LifecycleError(
            f"{where}: machinery_record_section must be the exact heading text "
            f"of the Boundary-B2 evidence section")

    # Immutability is enforced against git, not asserted in prose: the tracked
    # bytes and the working-tree bytes must be the same object.
    head_blob = _blob_oid_at(root, "HEAD", rel)
    if head_blob is None:
        raise LifecycleError(
            f"{where}: not tracked at HEAD -- the activation record is an "
            f"immutable tracked record, and an uncommitted one has no enabling "
            f"commit to derive.  Commit it (fence M2) or remove it")
    live_blob = _worktree_blob_oid(root, path)
    if live_blob != head_blob:
        raise LifecycleError(
            f"{where}: the working-tree bytes differ from the bytes committed "
            f"at HEAD -- an immutable record was modified in place.  Refusing "
            f"to derive a monitoring window from it")

    enabling = _introducing_commit(root, rel, head_blob)
    if enabling is None:
        raise LifecycleError(
            f"{where}: no commit in this path's history introduces exactly "
            f"these bytes -- the enabling commit is derived, never stored, and "
            f"it must exist")
    date = _author_date(root, enabling)
    if date is None:
        raise LifecycleError(
            f"{where}: cannot read the author date of the enabling commit "
            f"{enabling}")

    machinery = record["machinery_sha"]
    if not _commit_exists(root, machinery):
        raise LifecycleError(
            f"{where}: machinery_sha {machinery} is not a commit in this "
            f"repository")
    if not _is_strict_ancestor(root, machinery, enabling):
        raise LifecycleError(
            f"{where}: machinery_sha {machinery} is not a strict ancestor of "
            f"the derived enabling commit {enabling} -- the reviewed machinery "
            f"must already be in history when the window opens")
    _assert_machinery_binding(root, record, enabling, where)

    return {
        "path": rel,
        "machinery_sha": machinery,
        "machinery_record_path": record["machinery_record_path"],
        "machinery_record_section": record["machinery_record_section"],
        "enabling_commit": enabling,
        "activation_date": date,
    }


def _assert_machinery_binding(root: Path, record: dict, enabling: str,
                              where: str) -> None:
    """Refuse a `machinery_sha` the named evidence record does not attest.

    Without this the field is unfalsifiable -- any 40-hex ancestor would pass --
    and the oracle ("a record whose `machinery_sha` is not the enabling commit
    refuses") would have nothing to observe.  So the record names the evidence
    section that *does* attest the commit, and the section is read **at the
    enabling commit**, where the record's own claim was fixed.
    """
    rel = record["machinery_record_path"]
    section = record["machinery_record_section"]
    body = _git_ok(root, ["show", f"{enabling}:{rel}"])
    if body is None:
        raise LifecycleError(
            f"{where}: {rel} does not exist at the enabling commit {enabling} "
            f"-- machinery_record_path must name a record that was in the tree "
            f"when the window opened")
    heading = "## " + section
    lines = _split_lines(body)
    try:
        start = lines.index(heading)
    except ValueError:
        raise LifecycleError(
            f"{where}: {rel} at {enabling} has no `{_safe_field(heading)}` "
            f"section -- machinery_record_section must be an exact heading") \
            from None
    end = len(lines)
    for offset, line in enumerate(lines[start + 1:], start=start + 1):
        if line.startswith("## "):
            end = offset
            break
    body_text = "\n".join(lines[start + 1:end])
    machinery = record["machinery_sha"]
    if machinery not in body_text and machinery[:12] not in body_text:
        raise LifecycleError(
            f"{where}: the `{_safe_field(section)}` section of {rel} at "
            f"{enabling} does not name machinery_sha {machinery} -- the "
            f"activation record claims a machinery commit its own cited "
            f"evidence record does not attest")


# --- the append-only event ledger --------------------------------------------


def _validate_event(record: dict, where: str, *, counted_state: Optional[str],
                    assurance_values: Optional[Tuple[str, ...]] = None) -> dict:
    """Schema-validate one event block.  No git, no cross-event state.

    `counted_state` is the vocabulary-confirmed counted plan state, or `None`
    when the vocabulary could not supply it -- in which case a `plan-counted`
    event refuses instead of being accepted against an unchecked token.

    `assurance_values` is the same arrangement for the `assurance_path`
    field: the closed set comes from the planner, is computed **once** by the
    caller, and `None` means the vocabulary could not supply it -- so a
    `plan-counted` event refuses rather than being admitted against an unchecked
    token.  Validation never re-DERIVES the value: the ledger is append-only
    history, and a read that recomputed the field would make a past event's
    meaning depend on the present working tree.
    """
    if record.get("schema") != _EVENT_SCHEMA:
        raise LifecycleError(
            f"{where}: unknown or missing event schema "
            f"{_safe_field(record.get('schema'))!r} -- this tool reads "
            f"{_EVENT_SCHEMA} and refuses anything else")
    kind = record.get("kind")
    if kind not in _EVENT_KEYS:
        raise LifecycleError(
            f"{where}: unknown event kind {_safe_field(kind)!r} -- the closed "
            f"set is {list(_EVENT_KINDS)}")
    _require_exact_keys(record, _EVENT_KEYS[kind], _EVENT_OPTIONAL_KEYS, where)
    if not _PILOT_DATE_RE.match(record["date"]):
        raise LifecycleError(f"{where}: date must be YYYY-MM-DD")
    try:
        _dt.date.fromisoformat(record["date"])
    except ValueError:
        raise LifecycleError(
            f"{where}: date {record['date']!r} is not a real calendar date") \
            from None
    if not _PILOT_SUBJECT_RE.match(record["subject"]):
        raise LifecycleError(
            f"{where}: subject must be a lowercase stem/token "
            f"([a-z0-9][a-z0-9._-]*), got {_safe_field(record['subject'])!r}")
    art = record["source_artifact"]
    if (not _PILOT_PATH_RE.match(art) or ".." in art.split("/")
            or art.startswith("/") or "//" in art):
        raise LifecycleError(
            f"{where}: source_artifact must be a plain repository-relative "
            f"path, got {_safe_field(art)!r}")
    if not _PILOT_SHA_RE.match(record["source_commit"]):
        raise LifecycleError(
            f"{where}: source_commit must be a full 40-character lowercase hex "
            f"commit id")
    for key in _EVENT_NUMERIC_KEYS:
        if key in record and not _PILOT_NUMBER_RE.match(record[key]):
            raise LifecycleError(
                f"{where}: {key} must be a bounded non-negative integer "
                f"(< 10^12, no sign, no leading zero)")
        if key in record and int(record[key]) > _PILOT_NUMERIC_MAX:
            raise LifecycleError(
                f"{where}: {key} exceeds {_PILOT_NUMERIC_MAX}")
    if kind == "pause-set" and record["severity"] not in _PAUSE_SEVERITIES:
        raise LifecycleError(
            f"{where}: severity must be one of {list(_PAUSE_SEVERITIES)}")
    if kind == "plan-counted":
        if counted_state is None:
            raise LifecycleError(
                f"{where}: a plan-counted event names plan_state "
                f"{_safe_field(record['plan_state'])!r}, and the single runtime "
                f"vocabulary cannot confirm it right now -- refusing to admit a "
                f"counted plan against an unchecked status token")
        if record["plan_state"] != counted_state:
            raise LifecycleError(
                f"{where}: plan_state must be {counted_state!r} (the state the "
                f"six-plan rule counts), got "
                f"{_safe_field(record['plan_state'])!r}")
        if assurance_values is None:
            raise LifecycleError(
                f"{where}: a plan-counted event names assurance_path "
                f"{_safe_field(record['assurance_path'])!r}, and the single "
                f"runtime vocabulary cannot confirm it right now -- refusing to "
                f"admit a counted plan against an unchecked assurance token")
        if record["assurance_path"] not in assurance_values:
            raise LifecycleError(
                f"{where}: assurance_path must be one of "
                f"{list(assurance_values)} (the planner's closed vocabulary plus "
                f"the resolved not-inherited answer), got "
                f"{_safe_field(record['assurance_path'])!r}")
    return record


def _assert_event_bindings(root: Path, event: dict, where: str) -> None:
    """Refuse an event whose source binding does not resolve in this repository.

    Checked on **every read**, not only at write time: the write-time check
    protects the writer, and a hand-added block never went through it.  An event
    citing a commit that does not exist, or an artifact that does not exist at
    that commit, is not evidence and must not be counted.
    """
    if not _commit_exists(root, event["source_commit"]):
        raise LifecycleError(
            f"{where}: source_commit {event['source_commit']} is not a commit in "
            f"this repository -- every event is bound to a real source commit")
    if _blob_oid_at(root, event["source_commit"],
                    event["source_artifact"]) is None:
        raise LifecycleError(
            f"{where}: {_safe_field(event['source_artifact'])} does not exist at "
            f"{event['source_commit'][:12]} -- every event is bound to its "
            f"source artifact AT its source commit")


def _cross_check_events(events: List[dict], where: str) -> None:
    """Reject duplicate/conflicting stems and impossible pause sequences.

    Order matters, so this is one forward pass over the ledger as written: the
    ledger is append-only, so its order *is* the history.
    """
    counted: dict = {}
    active: dict = {}
    for event in events:
        line = event.get("_line", "?")
        at = f"{where}:{line}"
        kind = event["kind"]
        subject = event["subject"]
        if kind == "plan-counted":
            prior = counted.get(subject)
            if prior is not None:
                detail = ("the same source commit" if prior == event["source_commit"]
                          else f"a different source commit ({prior})")
                raise LifecycleError(
                    f"{at}: plan stem {subject!r} is already counted with "
                    f"{detail} -- the six-plan rule counts DISTINCT stems, so a "
                    f"duplicate or conflicting event refuses")
            counted[subject] = event["source_commit"]
        elif kind == "pause-set":
            if subject in active:
                raise LifecycleError(
                    f"{at}: pause {subject!r} is already active (set at line "
                    f"{active[subject]}) -- refusing a duplicate pause-set")
            active[subject] = line
        else:  # pause-cleared
            if subject not in active:
                raise LifecycleError(
                    f"{at}: pause-cleared for {subject!r}, which is not active "
                    f"-- refusing to clear a pause that was never set")
            active.pop(subject)


def _read_events(root: Path, *, counted_state: Optional[str],
                 assurance_values: Optional[Tuple[str, ...]] = None
                 ) -> Tuple[List[dict], List[str]]:
    """The validated ledger, plus notes about its state.

    Returns `([], notes)` when the ledger file is absent -- that is a fact about
    an adopter tree (the ledger is Cairn's own record, not a shipped template),
    and it is *reported*, never silently equated with "no events happened".
    """
    rel = "/".join(_PILOT_EVENTS_REL)
    notes: List[str] = []
    path = root.joinpath(*_PILOT_EVENTS_REL)
    if not path.exists() and not path.is_symlink():
        notes.append(f"no event ledger at {rel} (nothing has been recorded here)")
        return [], notes
    path = _evidence_path(root, _PILOT_EVENTS_REL, must_exist=True)
    text = _read_text_strict(path)
    events = _parse_fenced_records(text, _EVENT_FENCE, rel)
    for event in events:
        _validate_event(event, f"{rel}:{event.get('_line', '?')}",
                        counted_state=counted_state,
                        assurance_values=assurance_values)
        _assert_event_bindings(root, event, f"{rel}:{event.get('_line', '?')}")
    _cross_check_events(events, rel)
    notes.extend(_assert_append_only(root, rel, text,
                                     counted_state=counted_state,
                                     assurance_values=assurance_values))
    return events, notes


def _assert_append_only(root: Path, rel: str, text: str, *,
                        counted_state: Optional[str],
                        assurance_values: Optional[Tuple[str, ...]] = None
                        ) -> List[str]:
    """Refuse a ledger whose committed events are not a prefix of the live ones.

    The altered-prior-event check, stated where it can actually be enforced:
    the committed version is the durable record, so every event it contains must
    still be present, in the same order, with the same fields.  Prose *around*
    the blocks is not authority and may be edited; an event may only be added
    after the last one.
    """
    head_text = _git_ok(root, ["show", f"HEAD:{rel}"])
    if head_text is None:
        return [f"{rel} is not tracked at HEAD yet -- the append-only check "
                f"against the committed record cannot run"]
    committed = _parse_fenced_records(head_text, _EVENT_FENCE, f"HEAD:{rel}")
    for event in committed:
        _validate_event(event, f"HEAD:{rel}:{event.get('_line', '?')}",
                        counted_state=counted_state,
                        assurance_values=assurance_values)
    live = _parse_fenced_records(text, _EVENT_FENCE, rel)
    if len(live) < len(committed):
        raise LifecycleError(
            f"{rel}: the working tree has {len(live)} event(s) where HEAD has "
            f"{len(committed)} -- events were removed from an append-only "
            f"ledger")
    for index, (old, new) in enumerate(zip(committed, live), start=1):
        old_fields = {k: v for k, v in old.items() if not k.startswith("_")}
        new_fields = {k: v for k, v in new.items() if not k.startswith("_")}
        if old_fields != new_fields:
            raise LifecycleError(
                f"{rel}: event {index} differs from the version committed at "
                f"HEAD -- a prior event was altered, and this ledger is "
                f"append-only")
    return []


def _render_event_block(record: dict) -> str:
    """One event block, keys in schema order.  Fixed order so appends diff."""
    order = [k for k in _EVENT_KEYS[record["kind"]] if k in record]
    lines = ["```" + _EVENT_FENCE]
    lines.extend(f"{key}: {record[key]}" for key in order)
    lines.append("```")
    return "\n".join(lines) + "\n"


def _append_event(root: Path, path: Path, text: str, block: str) -> None:
    """Append one block with an expected-old check, atomically or not at all.

    `os.replace` makes the *visible* transition atomic; the expected-old re-read
    immediately before it narrows the read-modify-write window rather than
    locking it.  Stated plainly because the honest claim matters: two writers
    racing inside that window is *detected* here (the loser refuses and its
    event is not recorded), and git is what makes the record durable.
    """
    expected_old = text.encode("utf-8")
    separator = "" if text.endswith("\n") or not text else "\n"
    new_text = text + separator + "\n" + block
    tmp = path.with_name(f"{path.name}.tmp-{os.getpid()}-{secrets.token_hex(4)}")
    try:
        try:
            with open(tmp, "xb") as handle:
                handle.write(new_text.encode("utf-8"))
                handle.flush()
                os.fsync(handle.fileno())
            current = path.read_bytes()
            if current != expected_old:
                raise LifecycleError(
                    f"{path} changed while this event was being prepared -- "
                    f"another writer got there first.  Nothing was written; "
                    f"re-run and the new state will be re-read")
            os.replace(tmp, path)
        except OSError as exc:
            raise LifecycleError(
                f"cannot append to {path}: {exc} -- nothing was written") \
                from None
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


# --- derivation: counts, pauses, the report ----------------------------------


def _window_bounds(activation_date: str) -> Tuple[_dt.date, _dt.date]:
    """The evidence window, inclusive on both ends.

    `_PILOT_WINDOW_DAYS` **calendar days counted inclusively from the derived
    activation date**, so the activation date is day 1 and the last day is
    `activation_date + (window - 1)`.  Spelled out because off-by-one here
    silently moves a Maintainer Decision by a day: with a 2026-01-01 activation
    and a 60-day window, 2026-03-01 is the last in-window day and 2026-03-02 is
    the first day past the deadline.
    """
    first = _dt.date.fromisoformat(activation_date)
    return first, first + _dt.timedelta(days=_PILOT_WINDOW_DAYS - 1)


#: The accepted parent's eligibility rule, quoted where it is applied: *"High
#: assurance work remains ineligible and does not fill the sample."*  The
#: eligible path is therefore `standard` -- but see `_eligibility_split` for the
#: reason the QUOTA denominator is deliberately left alone.
_ELIGIBLE_ASSURANCE_PATH = "standard"


def _eligibility_split(counted: List[dict], stems: List[str]) -> List[str]:
    """The eligible / ineligible split the accepted parent requires.

    The parent's report requirements include *"eligible and ineligible plans"*,
    and P6a could not derive it: no `plan-counted` field carried a plan's
    assurance path, because a plan HAS none until P2-R's inheritance chain
    resolves one.  With `cairn-pilot-event/2` recording the resolved value, the
    split is a grouping over the counted events.

    **The quota denominator is NOT changed here, and that restraint is the
    finding.**  The accepted parent says high-assurance work "does not fill the
    sample"; the 2026-08-11 Maintainer-directed revision says standard *and*
    high-assurance proposals may both receive `READY`, which makes high-assurance
    plans part of the population the policy now affects.  Those two sentences pull
    opposite ways on *whose* plans fill the six, and neither the revision nor
    The obligation resolves it -- it asks only that the report "split eligible from
    ineligible".  Re-deciding the quota would be an implementer choosing between
    two accepted texts, so the counted-stem count stays exactly as P6a landed it,
    the split is reported beside it, and the tension is printed rather than
    silently resolved.
    """
    by_path: dict = {}
    for stem in stems:
        event = next(e for e in counted if e["subject"] == stem)
        by_path.setdefault(event.get("assurance_path", "?"), []).append(stem)
    eligible = by_path.get(_ELIGIBLE_ASSURANCE_PATH, [])
    ineligible = sorted(
        stem for path, group in by_path.items()
        if path != _ELIGIBLE_ASSURANCE_PATH for stem in group)
    lines = [
        f"  eligible ({_ELIGIBLE_ASSURANCE_PATH}): {len(eligible)} "
        f"[{', '.join(_safe_field(s) for s in eligible) or 'none'}]",
        f"  ineligible / outside the sample: {len(ineligible)} "
        f"[{', '.join(_safe_field(s) for s in ineligible) or 'none'}]",
    ]
    for path, group in sorted(by_path.items()):
        if path == _ELIGIBLE_ASSURANCE_PATH:
            continue
        lines.append(
            f"    {_safe_field(path)}: "
            f"{', '.join(_safe_field(s) for s in sorted(group))}")
    if ineligible:
        lines.append(
            "  NOTE: the quota above counts DISTINCT stems, not eligible stems. "
            "The accepted parent says high-assurance work does not fill the "
            "sample; the 2026-08-11 revision lets high-assurance proposals "
            "inherit. That tension is a Maintainer's call, so it is reported "
            "here rather than resolved by the tool")
    return lines


def _derive_report(root: Path, *, today: Optional[_dt.date] = None
                   ) -> Tuple[List[str], List[str]]:
    """`(report_lines, incomplete_reasons)`.  Derives; stores nothing."""
    lines: List[str] = []
    incomplete: List[str] = []
    now = today or _dt.date.today()

    lines.append(
        "review policy: ACTIVE -- the proposal-centered review allocation is "
        "the default now")
    lines.append(
        "this report is monitoring EVIDENCE, not permission: it never gates "
        "the policy it measures")

    counted_state: Optional[str] = None
    assurance_values: Optional[Tuple[str, ...]] = None
    try:
        counted_state = _counted_plan_state()
        assurance_values = _assurance_values()
    except MonitoringIncomplete as exc:
        incomplete.append(str(exc))
    except VocabularyUnavailable as exc:
        incomplete.append(f"the status vocabulary is unavailable: {exc}")

    activation = _read_activation(root)
    events, notes = _read_events(root, counted_state=counted_state,
                                 assurance_values=assurance_values)
    for note in notes:
        lines.append(f"note: {note}")

    if activation is None:
        lines.append(
            f"activation: NONE -- no {'/'.join(_PILOT_ACTIVATION_REL)}")
        lines.append(
            "meaning: no monitoring evidence window has opened yet (it opens at "
            "P6d, the data-only commit at fence M2)")
        lines.append(
            "NOT meaning: the review policy is disabled.  Absent monitoring "
            "activation says nothing about the policy, which is already in "
            "force")
        incomplete.append(
            "no activation record, so there is no window, no counted plans and "
            "no boundary -- absence of evidence, not evidence of a disabled "
            "policy")
    else:
        first, last = _window_bounds(activation["activation_date"])
        lines.append(f"activation record: {activation['path']}")
        lines.append(
            f"enabling commit: {activation['enabling_commit']} (DERIVED as the "
            f"commit that first introduced this exact record)")
        lines.append(
            f"activation date: {activation['activation_date']} (DERIVED: that "
            f"commit's author date)")
        lines.append(
            f"machinery_sha: {activation['machinery_sha']} (attested by "
            f"{_safe_field(activation['machinery_record_path'])} > "
            f"{_safe_field(activation['machinery_record_section'])})")
        lines.append(
            f"window: {first.isoformat()} .. {last.isoformat()} "
            f"({_PILOT_WINDOW_DAYS} calendar days, both ends inclusive) -- "
            f"{'ELAPSED' if now > last else 'OPEN'}")

    in_window: List[dict] = []
    excluded: List[dict] = []
    for event in events:
        if activation is None:
            excluded.append(event)
            continue
        first, last = _window_bounds(activation["activation_date"])
        when = _dt.date.fromisoformat(event["date"])
        (in_window if first <= when <= last else excluded).append(event)

    counted = [e for e in in_window if e["kind"] == "plan-counted"]
    stems = sorted({e["subject"] for e in counted})
    if counted_state is None:
        lines.append(
            f"counted plan stems: UNAVAILABLE / {_PILOT_PLAN_QUOTA} -- the "
            f"counting rule's plan state is not in the vocabulary yet, so this "
            f"count is not computable.  It is NOT zero")
    else:
        lines.append(
            f"counted plan stems: {len(stems)} / {_PILOT_PLAN_QUOTA} "
            f"(distinct stems reaching '{counted_state}')")
        for stem in stems:
            event = next(e for e in counted if e["subject"] == stem)
            lines.append(
                f"  - {_safe_field(stem)}  {event['date']}  "
                f"{_safe_field(event['source_artifact'])}  "
                f"{event['source_commit'][:12]}  "
                f"{_safe_field(event.get('assurance_path', '?'))}")
        lines.extend(_eligibility_split(counted, stems))
    if excluded:
        lines.append(
            f"events outside the window (excluded from every count): "
            f"{len(excluded)}")

    active_pauses: dict = {}
    for event in events:  # pause state is ledger-wide, not window-scoped
        if event["kind"] == "pause-set":
            active_pauses[event["subject"]] = event
        elif event["kind"] == "pause-cleared":
            active_pauses.pop(event["subject"], None)
    if active_pauses:
        for subject, event in sorted(active_pauses.items()):
            lines.append(
                f"PAUSE ACTIVE: {_safe_field(subject)} (severity "
                f"{event['severity']}, set {event['date']}, "
                f"{_safe_field(event['source_artifact'])})")
    else:
        lines.append("pauses: none active")

    measures = {key: sum(int(e.get(key, "0")) for e in in_window)
                for key in _EVENT_NUMERIC_KEYS}
    lines.append(
        f"measures in window: review-input bytes {measures['review_input_bytes']}; "
        f"transitions removed {measures['transitions_removed']}; escaped "
        f"findings high {measures['escaped_findings_high']} / low "
        f"{measures['escaped_findings_low']}; Maintainer prompts "
        f"{measures['maintainer_prompts']}")

    if (measures["escaped_findings_high"] >= _PAUSE_HIGH_THRESHOLD
            or measures["escaped_findings_low"] >= _PAUSE_LOW_THRESHOLD):
        if not active_pauses:
            incomplete.append(
                f"recorded escaped findings meet a pause condition "
                f"(>= {_PAUSE_HIGH_THRESHOLD} high or "
                f">= {_PAUSE_LOW_THRESHOLD} low) but no pause is active -- "
                f"record the pause or explain why the condition does not apply")

    if activation is not None and counted_state is not None:
        first, last = _window_bounds(activation["activation_date"])
        quota_reached = len(stems) >= _PILOT_PLAN_QUOTA
        deadline_reached = now > last
        if quota_reached or deadline_reached:
            reason = "six distinct plan stems" if quota_reached else "the 60-day deadline"
            lines.append(
                f"monitoring boundary: REACHED via {reason} -- the Maintainer's "
                f"`retain | revise | retire` Decision is due (fence M6).  "
                f"`promote` is a retired token and is not one of the choices")
        else:
            lines.append(
                f"monitoring boundary: not reached "
                f"({len(stems)}/{_PILOT_PLAN_QUOTA} stems, window open through "
                f"{last.isoformat()})")
    return lines, incomplete


# --- subcommands: pilot-report / pilot-record --------------------------------


def cmd_pilot_report(args: argparse.Namespace) -> int:
    """Derive and print the monitoring-evidence report.  Writes nothing.

    Exit codes are part of the contract: `0` a complete report, `3` a report
    with at least one named unsatisfied dependency (no window yet, or a
    counting rule the vocabulary cannot supply), `1` a refusal.  A `3` is never
    "the policy is off" -- the reasons are printed, and each one is about
    *evidence*.
    """
    root = _repo_root()
    _emit_section("monitoring evidence -- review allocation")
    lines, incomplete = _derive_report(root)
    for line in lines:
        _emit(line)
    if incomplete:
        for reason in incomplete:
            _emit(f"INCOMPLETE: {reason}")
        _emit("report: INCOMPLETE (exit 3) -- evidence missing, policy "
              "unaffected")
        return 3
    _emit("report: complete")
    return 0


def cmd_pilot_record(args: argparse.Namespace) -> int:
    """Append one event to the ledger.  The ledger's only writer."""
    root = _repo_root()
    rel = "/".join(_PILOT_EVENTS_REL)
    counted_state: Optional[str] = None
    assurance_values: Optional[Tuple[str, ...]] = None
    assurance_path: Optional[str] = None
    if args.kind == "plan-counted":
        try:
            counted_state = _counted_plan_state()
        except MonitoringIncomplete as exc:
            raise LifecycleError(
                f"refusing to record a counted plan: {exc}") from None
        assurance_values = _assurance_values()
        assurance_path = _resolved_assurance_path(root, args.source_artifact)

    record = {
        "schema": _EVENT_SCHEMA,
        "kind": args.kind,
        "date": args.date or _today(),
        "subject": args.subject,
        "source_artifact": args.source_artifact,
        "source_commit": args.source_commit,
    }
    if args.kind == "plan-counted":
        record["plan_state"] = counted_state or ""
        # DERIVED, not supplied -- there is deliberately no `--assurance-path`
        # flag, for the reason there is none for `plan_state`: a governance field
        # a human types is an author's claim, and the whole point of the CLI being
        # the only writer is that the claim can be replaced by a derivation.
        record["assurance_path"] = assurance_path or ""
        record["review_input_bytes"] = str(args.review_input_bytes)
        record["transitions_removed"] = str(args.transitions_removed)
        record["escaped_findings_high"] = str(args.escaped_findings_high)
        record["escaped_findings_low"] = str(args.escaped_findings_low)
        record["maintainer_prompts"] = str(args.maintainer_prompts)
    elif args.kind == "pause-set":
        if not args.severity:
            raise LifecycleError("pause-set requires --severity high|low")
        record["severity"] = args.severity
    if args.note:
        record["note"] = args.note

    _validate_event(record, f"{rel} (new event)", counted_state=counted_state,
                    assurance_values=assurance_values)
    _assert_event_bindings(root, record, f"{rel} (new event)")

    path = _evidence_path(root, _PILOT_EVENTS_REL, must_exist=True)
    text = _read_text_strict(path)
    existing = _parse_fenced_records(text, _EVENT_FENCE, rel)
    for event in existing:
        _validate_event(event, f"{rel}:{event.get('_line', '?')}",
                        counted_state=counted_state,
                        assurance_values=assurance_values)
    _assert_append_only(root, rel, text, counted_state=counted_state,
                        assurance_values=assurance_values)
    _cross_check_events(existing + [dict(record)], rel)

    block = _render_event_block(record)
    _emit_section("monitoring evidence -- record one event")
    for line in _split_lines(block):
        _emit(line)
    if args.dry_run:
        _emit(f"--dry-run: nothing written to {rel}")
        return 0
    _append_event(root, path, text, block)
    _emit(f"appended to {rel} ({len(existing) + 1} event(s) now recorded)")
    _emit("commit it: the ledger is durable because it is tracked, not because "
          "it is on disk")
    return 0


# === review-brief and closeout --dry-run =====================================
#
# Implements the
# accepted parent's Revision 1 -- the operative revision; its own opening words
# are *"This section supersedes the operative requirements in the opening
# Proposal, Pilot, Evidence, and Signals sections"*, so the two field lists
# below are Revision 1's, not the opening Proposal's (they agree in substance;
# Revision 1 is the shorter spelling and is the one quoted here).
#
#     `python tools/lifecycle.py closeout <plan> --dry-run` reports plan/proposal
#     state, accepted commit and assurance path, plan-review satisfaction,
#     Boundary B binding, latest code-review result, unresolved findings,
#     unhomed follow-ups, and the exact archive/board paths.  It never edits,
#     moves, commits, runs tests, or decides whether evidence is competent.
#
#     `review-brief` reports the assurance path and tier, complete-current-
#     contract span, last reviewed commit, unresolved finding ids, paths changed
#     since that commit, and any Boundary B summary.  It does not summarize
#     prose, choose evidence, or grant authority.
#
#     `review-brief` and `closeout --dry-run` are deterministic, offline,
#     standard-library-only extractors.  They have no LLM, API, telemetry, or
#     network dependency.  Their output derives only from repository bytes, git
#     metadata, and explicit command arguments.
#
# **Three properties are structural, not promises.**
#
#   * **Read-only, and no artifact content is executed.**  Nothing below opens a
#     file for writing, and the only subprocess is the module's one read-only
#     `_git` helper.  An artifact is *parsed*, never imported or evaluated.
#   * **One readiness reading, not a second one.**  The contract requires that *"`scan`,
#     `next`, and accepted closeout tooling consume shared predicates rather than
#     implement three interpretations of readiness"*.  So the preflight below is
#     literally `status_evidence_violations(art, "ready-to-archive")` -- the
#     planner's own predicate, through the contained loader, exactly as `scan`
#     and `next` call it.  There is no local re-derivation to tighten or loosen.
#   * **The protected interpreter binding is untouched.**  `_resolve_interpreter`
#     is not called, not read, and not reachable from either command; neither
#     command spawns anything under the resolved path.  That is the Maintainer fence of
#     the plan, pinned by
#     `bootstrap/tests/test_lifecycle_brief.py::TestInterpreterFence`.
#
# **What is extracted here rather than asked of the planner, and why that is
# stated rather than hidden.**  The planner owns the artifact parser
# (`read_artifact`), the readiness predicates, the closed vocabularies and the
# terminal encoder, and all of them are reached through the one contained loader
# above.  What this file adds is *heading and field location* -- which lines a
# record occupies -- because the planner's public surface answers "is this
# record valid", not "where is it".  Those local rules are restatements of the
# planner's, and `bootstrap/tests/test_lifecycle_brief.py::TestNoGrammarDrift`
# compares them against the planner's own helpers over the live corpus so a
# restatement cannot quietly become a divergence.

#: Versioned machine contracts.  A consumer pins the version and a bump is
#: visible; there is no unversioned shape to fall back to.
_BRIEF_SCHEMA = "cairn-review-brief/1"
_CLOSEOUT_SCHEMA = "cairn-closeout/1"

#: Where an artifact may live, and the only directories a bare stem is searched
#: in.  A path outside them refuses: these two commands read the deliberation
#: record, and pointing them at an arbitrary file would make "status" and
#: "assurance path" answers about something that is not a lifecycle artifact.
_ARTIFACT_DIRS = (
    ("proposal", ("dev", "proposals")),
    ("proposal", ("dev", "proposals", "archive")),
    ("plan", ("dev", "plans")),
    ("plan", ("dev", "plans", "archive")),
)

#: The board a plan's archive transition must touch alongside the file move.
_BOARD_REL = ("dev", "PLANNING.md")

#: A real (unfenced) ATX heading.  Column 0 is markdown's own rule; the planner's
#: `_ATX_HEADING_RE` is the same expression, and `TestNoGrammarDrift` pins that.
_ATX_RE = re.compile(r"^(?P<hashes>#{1,6})[ \t]+(?P<text>.*?)[ \t]*$")

#: **Two normalizers, because the planner has two and they are not the same
#: rule.**  A field VALUE drops only the paired emphasis markers
#: (`_EMPHASIS_RE`); a HEADING drops every emphasis character including the
#: backtick (`_strip_emphasis_chars`), which is why `## check_cairn: ...`
#: normalizes to `checkcairn: ...`.  Collapsing the two into one would make this
#: file's heading recognition disagree with the planner's on every heading that
#: carries a code span -- measured, not hypothetical: the live corpus has them.
_EMPHASIS_SUB_RE = re.compile(r"\*\*|__")
_HEADING_EMPHASIS_CHARS = "*_`"
_ASCII_WS_SUB_RE = re.compile(r"[ \t\n\r\f\v]+")

#: The leading clause of a closed-vocabulary field value, the planner's own
#: expression.  `**Verdict: REVISE / NOT CLEARED TO ARCHIVE.**` is a real record,
#: so trailing prose must be tolerated -- but only after a break character, never
#: inside the token, so `SHIP but actually BLOCK` stays out-of-vocabulary rather
#: than parsing as `SHIP`.
_VERDICT_CLAUSE_SUB_RE = re.compile(r"^[^.,;(/]*")

#: Heading classes this file needs to *locate*.  Matched on the NORMALIZED
#: heading text (emphasis stripped, ASCII whitespace collapsed, casefolded), the
#: same normalization the planner's `_heading_records` applies, because the
#: corpus writes both `--` and em-dash separators and neither is a contract
#: difference.
_CONTRACT_NORM_RE = re.compile(r"(?:revised proposal|revision)\b")
_RESPONSE_NORM_SUB_RE = re.compile(r"response\b")
_REVIEW_HEADING_NORM_RE = re.compile(r"(?:review|plan review|code review)\b")

#: Boundary B's stable-evidence record, and the Code-review pass, in the exact
#: raw-line shapes the planner matches them in.
_STABLE_EVIDENCE_LINE_RE = re.compile(
    r"^## Implementation verification -- (?P<agent>[^\n]+?) -- "
    r"(?P<date>\d{4}-\d{2}-\d{2})(?P<rest>[^\n]*)$")
_CODE_REVIEW_LINE_RE = re.compile(
    r"^## Code review -- (?P<reviewer>[^\n]+?) -- "
    r"(?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<round>\d+)\))?$")

#: A bracketed finding id -- `[E1]`, `[S12]`, `[CF3]`, `[M6-R]`.  Deliberately
#: narrow: an arbitrary bracketed word is a citation, not a finding id, and
#: widening this would turn every markdown link into an "unresolved finding".
_FINDING_ID_RE = re.compile(r"\[(?P<id>[A-Z]{1,3}\d{1,3}(?:-[A-Z])?)\]")

#: A full commit id, the only shape a binding may carry.  An abbreviation is
#: reported as present-but-not-full rather than silently accepted: the accepted
#: contract writes `<full commit id>` and a 7-character prefix is not one.
_FULL_SHA_RE = re.compile(r"\A[0-9a-f]{40}\Z")

#: How many list members a report prints before it says how many it withheld.
#: Bounded output is a display property, not a security one -- but an unbounded
#: `git diff --name-only` over a wide range can bury the rest of the report.
_LIST_CAP = 40


def _field_pattern(name: str) -> "re.Pattern[str]":
    """One emphasis-optional full-line field matcher, by field name.

    The same expression as the planner's `_code_review_field_re`; both spellings
    are live text in this tree (the accepted contract writes the basis unbolded,
    every real review writes it bolded), so admitting only one would refuse
    correct records for no contract reason.
    """
    return re.compile(
        r"^(?:\*\*|__)?" + re.escape(name) + r"(?:\*\*|__)?:[ \t]*"
        r"(?P<value>.*?)[ \t]*$", re.M)


def _normalize_heading(text: str) -> str:
    """Emphasis characters deleted, ASCII whitespace collapsed, casefolded."""
    for char in _HEADING_EMPHASIS_CHARS:
        text = text.replace(char, "")
    return _ASCII_WS_SUB_RE.sub(" ", text).strip().casefold()


def _iter_unfenced(text: str):
    """``(line_no, line)`` for every line OUTSIDE a fenced code block.

    A `##` inside a fence is literal text, not a heading.  It matters on real
    bytes rather than in theory: this plan's own accepted contract quotes record
    headings inside ```text fences, and both authoring templates now do too, so a
    raw search would report a specification as a record.
    """
    in_fence = False
    for i, line in enumerate(_split_lines(text)):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield i + 1, line


def _headings(text: str) -> List[Tuple[int, int, str, str]]:
    """``(line_no, level, raw_heading, normalized)`` per real heading."""
    out: List[Tuple[int, int, str, str]] = []
    for line_no, line in _iter_unfenced(text):
        m = _ATX_RE.match(line)
        if m is None:
            continue
        out.append((line_no, len(m.group("hashes")), line.strip(),
                    _normalize_heading(m.group("text"))))
    return out


def _span_end(headings: List[Tuple[int, int, str, str]], index: int,
              total_lines: int) -> int:
    """The last line of `headings[index]`'s span: up to the next same-or-shallower
    heading, else end of file."""
    level = headings[index][1]
    for line_no, lvl, _raw, _norm in headings[index + 1:]:
        if lvl <= level:
            return line_no - 1
    return total_lines


def _header_region(text: str) -> str:
    """Every line above the first `## ` heading.

    Bounding the read is what stops an `**Assurance path**:` line quoted inside
    an appended review section from being read as the artifact's own
    declaration -- the same bound the planner's `_iter_header_lines` applies.
    """
    out: List[str] = []
    for line in _split_lines(text):
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out)


def _one_field(body: str, name: str) -> Tuple[Optional[str], Optional[str]]:
    """``(value, problem)`` for one field: absent and duplicate are both problems.

    A duplicate is a problem **even when the two lines agree**: agreeing is a
    judgement, and there is no rule here for choosing between two lines that may
    not.
    """
    found = _field_pattern(name).findall(body)
    if not found:
        return None, f"no '{name}:' line"
    if len(found) > 1:
        return None, f"duplicate '{name}:' ({len(found)} lines)"
    value = _EMPHASIS_SUB_RE.sub("", found[0]).strip()
    # One pair of surrounding backticks is presentation, not value.  Measured
    # rather than assumed: every `Reviewed commit:` line in `dev/plans/` writes
    # the id inside a code span, so a shape check run on the raw value would
    # report every real binding as "not a full commit id" -- a checker refusing
    # the house form is the same defect class as one accepting an empty field.
    if len(value) > 1 and value.startswith("`") and value.endswith("`"):
        value = value[1:-1].strip()
    if not value:
        return None, f"empty '{name}:' value"
    return value, None


# --- locating the artifact ---------------------------------------------------


def _artifact_path(root: Path, spec: str) -> Path:
    """Resolve `<artifact>` to a real file under one of the four lifecycle dirs.

    Accepts a repository-relative path or a bare stem.  An **ambiguous** stem
    (the same name live and archived, which is exactly what an in-flight archive
    looks like) refuses and names both hits rather than picking one -- picking
    would answer the operator's question about a file they did not mean.
    """
    candidates: List[Path] = []
    if spec.endswith(".md") or "/" in spec or "\\" in spec:
        rel = spec.replace("\\", "/").strip("/")
        if not rel.endswith(".md"):
            raise LifecycleError(
                f"not a lifecycle artifact path: {_safe_field(spec)} -- expected "
                f"a '.md' file under dev/proposals/ or dev/plans/")
        path = root.joinpath(*rel.split("/"))
        parent_rels = {parts for _kind, parts in _ARTIFACT_DIRS}
        try:
            here = tuple(path.parent.relative_to(root).parts)
        except ValueError:
            here = ()
        if here not in parent_rels:
            raise LifecycleError(
                f"{_safe_field(rel)} is not under a lifecycle directory -- these "
                f"commands read the deliberation record, so the artifact must "
                f"live in dev/proposals/[archive/] or dev/plans/[archive/]")
        candidates = [path]
    else:
        stem = spec[:-3] if spec.endswith(".md") else spec
        for _kind, parts in _ARTIFACT_DIRS:
            candidate = root.joinpath(*parts, stem + ".md")
            if candidate.is_file():
                candidates.append(candidate)
        if not candidates:
            raise LifecycleError(
                f"no artifact named {_safe_field(stem)}.md under "
                f"dev/proposals/[archive/] or dev/plans/[archive/]")
        if len(candidates) > 1:
            named = ", ".join(
                _safe_field(c.relative_to(root).as_posix()) for c in candidates)
            raise LifecycleError(
                f"{_safe_field(stem)} is ambiguous -- it names {len(candidates)} "
                f"artifacts ({named}).  Pass the exact path; a stem that matches "
                f"both a live and an archived copy is what an in-flight archive "
                f"looks like, and choosing one would answer a different question")
    path = candidates[0]
    _assert_within(path, root)
    try:
        if _has_symlink_component_below(path, root):
            raise LifecycleError(
                f"{_safe_field(path.relative_to(root).as_posix())} is reached "
                f"through a symlink -- refusing to read a lifecycle artifact "
                f"through one")
        if not path.is_file():
            raise LifecycleError(f"no such artifact: {path}")
    except OSError as exc:
        raise LifecycleError(f"cannot inspect {path}: {exc}") from None
    return path


def _artifact(root: Path, spec: str, *, require_kind: Optional[str] = None):
    """``(planner Artifact, repo-relative path)``, or a clean refusal."""
    planner = _vocabulary()
    path = _artifact_path(root, spec)
    rel = path.relative_to(root).as_posix()
    try:
        art = planner.read_artifact(path)
    except Exception as exc:                     # PlannerError / OSError / ValueError
        raise LifecycleError(
            f"cannot parse {_safe_field(rel)}: {_safe_field(exc)}") from None
    if require_kind is not None and art.kind != require_kind:
        raise LifecycleError(
            f"{_safe_field(rel)} is a {_safe_field(art.kind)}, not a "
            f"{require_kind} -- `closeout` is the plan archive preflight")
    return art, rel


# --- the extractors ----------------------------------------------------------


def _declared_assurance(root: Path, art, rel: str) -> Tuple[Optional[str],
                                                            List[str]]:
    """``(value, problems)``.  A plan INHERITS one; a proposal DECLARES one.

    The plan arm is the planner's `resolve_plan_assurance_path` -- the inheritance chain,
    not a second reading of it -- and the proposal arm reads the artifact's own
    header declaration against the planner's closed `ASSURANCE_PATHS`.
    """
    planner = _vocabulary()
    if art.kind == "plan":
        value, problems = planner.resolve_plan_assurance_path(art.path)
        return value, [_safe_field(p) for p in problems]
    value, problem = _one_field(_header_region(art.text), "Assurance path")
    if problem:
        return None, [problem]
    for canonical in planner.ASSURANCE_PATHS:
        if value.casefold() == canonical.casefold():
            return canonical, []
    return None, [f"'Assurance path: {_safe_field(value)}' is outside the closed "
                  f"vocabulary {tuple(planner.ASSURANCE_PATHS)} -- there is no "
                  f"default"]


def _declared_tier(art) -> Tuple[str, List[str]]:
    """The artifact's declared review obligation, verbatim, plus any problem.

    A plan declares `**Plan review**: required(<tier>[ + <tier>])`; a proposal
    declares none of its own, so the value reported is the *record's* -- the
    latest `## Review` pass's `Tier:` line -- and the difference is stated in the
    value rather than smoothed over.
    """
    if art.kind == "plan":
        declared = (art.plan_review or "").strip()
        if not declared:
            return "undeclared", ["no '**Plan review**:' line in the header"]
        return _safe_field(declared), []
    latest: Optional[Tuple[int, str]] = None
    for line_no, level, raw, norm in _headings(art.text):
        if level == 2 and norm.startswith("review "):
            latest = (line_no, raw)
    if latest is None:
        return "no-review-record", []
    body = _section_body(art.text, latest[0])
    value, problem = _one_field(body, "Tier")
    if problem:
        return "unreadable", [f"{_safe_field(latest[1])}: {problem}"]
    return _safe_field(value), []


def _section_body(text: str, line_no: int) -> str:
    """The body of the heading at `line_no`, up to the next same-or-shallower one."""
    headings = _headings(text)
    lines = _split_lines(text)
    for index, (start, _lvl, _raw, _norm) in enumerate(headings):
        if start == line_no:
            end = _span_end(headings, index, len(lines))
            return "\n".join(lines[start:end])
    return ""


def _contract_spans(art) -> List[dict]:
    """Every complete-current-contract section, in document order, with its span.

    Located, never judged: whether the section really *is* complete is the
    reader's job, and the accepted contract assigns it to one ("A reviewer
    compares the complete revision to the previously reviewed contract").  That predicate's
    `current_contract_violations` is the predicate; this is the pointer.
    """
    headings = _headings(art.text)
    total = len(_split_lines(art.text))
    out: List[dict] = []
    for index, (line_no, level, raw, norm) in enumerate(headings):
        if level != 2 or not _CONTRACT_NORM_RE.match(norm):
            continue
        out.append({
            "line": line_no,
            "end_line": _span_end(headings, index, total),
            "heading": _safe_field(raw),
        })
    return out


def _review_records(art) -> List[Tuple[int, str, str]]:
    """``(line_no, raw_heading, normalized)`` for every H2 review record."""
    out: List[Tuple[int, str, str]] = []
    for line_no, level, raw, norm in _headings(art.text):
        if level == 2 and _REVIEW_HEADING_NORM_RE.match(norm):
            out.append((line_no, raw, norm))
    return out


def _last_reviewed_commit(art) -> dict:
    """The newest review record's `Reviewed commit:` binding, and its shape.

    Document order is authoritative -- the same rule the planner applies to the
    Code-review record ("the last record in the file is the current one").  An
    abbreviated id is reported as `full: false` rather than accepted: the
    accepted contract writes `<full commit id>`, and a report that quietly
    treated a 7-character prefix as the binding would be asserting something the
    record does not say.
    """
    records = _review_records(art)
    if not records:
        return {"record": None, "line": None, "value": None, "full": False,
                "problems": ["no review record in this artifact"]}
    line_no, raw, _norm = records[-1]
    value, problem = _one_field(_section_body(art.text, line_no),
                                "Reviewed commit")
    return {
        "record": _safe_field(raw),
        "line": line_no,
        "value": None if value is None else _safe_field(value),
        "full": bool(value and _FULL_SHA_RE.match(value)),
        "problems": [] if problem is None else [f"{_safe_field(raw)}: {problem}"],
    }


def _finding_ids(art) -> dict:
    """Raised ids, ids a later Response names, and the difference.

    **Extraction, and the limit is stated in the output.**  A finding is counted
    *raised* when its bracketed id appears in a review record, and *answered*
    when the same id appears in a `## Response...` section **below** that
    record.  What this cannot see is whether the answer resolved anything --
    that is a reading, and the accepted contract keeps it with the reviewer.  So
    the field is named `unanswered`, never `unresolved-and-blocking`.
    """
    headings = _headings(art.text)
    lines = _split_lines(art.text)
    raised: List[Tuple[str, int]] = []
    answered: List[Tuple[str, int]] = []
    for index, (line_no, level, _raw, norm) in enumerate(headings):
        if level != 2:
            continue
        end = _span_end(headings, index, len(lines))
        body = "\n".join(lines[line_no:end])
        ids = [m.group("id") for m in _FINDING_ID_RE.finditer(body)]
        if _RESPONSE_NORM_SUB_RE.match(norm):
            answered.extend((i, line_no) for i in ids)
        elif _REVIEW_HEADING_NORM_RE.match(norm):
            raised.extend((i, line_no) for i in ids)
    unanswered = sorted({
        i for i, at in raised
        if not any(a == i and after > at for a, after in answered)
    })
    return {
        "raised": sorted({i for i, _at in raised}),
        "answered": sorted({i for i, _at in answered}),
        "unanswered": unanswered,
    }


def _changed_paths(root: Path, base: Optional[str]) -> dict:
    """Repository paths changed since `base`, from git.  Read-only, no network.

    An unusable base is reported with its reason and an empty list -- never as
    "nothing changed", which is the same bytes and the opposite meaning.
    """
    if not base:
        return {"base": None, "available": False, "reason": "no reviewed commit "
                "to measure from", "count": 0, "paths": [], "withheld": 0}
    if _git_ok(root, ["cat-file", "-e", base + "^{commit}"]) is None:
        return {"base": _safe_field(base), "available": False,
                "reason": "not a commit in this repository", "count": 0,
                "paths": [], "withheld": 0}
    out = _git_ok(root, ["diff", "--name-only", base, "--"])
    if out is None:
        return {"base": _safe_field(base), "available": False,
                "reason": "git could not diff from that commit", "count": 0,
                "paths": [], "withheld": 0}
    paths = [p for p in _split_lines(out) if p.strip()]
    return {
        "base": _safe_field(base),
        "available": True,
        "reason": None,
        "count": len(paths),
        "paths": paths[:_LIST_CAP],
        "withheld": max(0, len(paths) - _LIST_CAP),
    }


def _boundary_b_records(art) -> List[dict]:
    """Every conforming `## Implementation verification` record, with its mode.

    `Boundary B mode` is `AGENTS.md`'s `full | bounded` field.  Absent is
    reported as absent, not as `full`: the rule's own direction is that
    *"uncertainty resolves to `full`"* for the *runner*, and a reader of a record
    that never stated a mode needs to see that it never stated one.
    """
    out: List[dict] = []
    headings = _headings(art.text)
    lines = _split_lines(art.text)
    for index, (line_no, level, raw, _norm) in enumerate(headings):
        if level != 2:
            continue
        m = _STABLE_EVIDENCE_LINE_RE.match(raw)
        if m is None:
            continue
        end = _span_end(headings, index, len(lines))
        body = "\n".join(lines[line_no:end])
        mode, _problem = _one_field(body, "Boundary B mode")
        out.append({
            "line": line_no,
            "heading": _safe_field(raw),
            "agent": _safe_field(m.group("agent")),
            "date": m.group("date"),
            "mode": None if mode is None else _safe_field(mode),
        })
    return out


def _code_review_result(art) -> dict:
    """The latest Code-review pass's verdict, classified by the planner's sets.

    The two verdict vocabularies are `tools/lifecycle_planner.py`'s, read through
    the contained loader.  A verdict outside both is `unreadable` and is
    **never** collapsed into either class -- a blocking pass that a reader cannot
    parse must not summarize as a clearing one.
    """
    planner = _vocabulary()
    passes = [(line_no, raw) for line_no, _lvl, raw, _norm in _headings(art.text)
              if _CODE_REVIEW_LINE_RE.match(raw)]
    if not passes:
        return {"record": None, "line": None, "verdict": None,
                "classification": "absent"}
    line_no, raw = passes[-1]
    body = _section_body(art.text, line_no)
    value, problem = _one_field(body, "Verdict")
    classification = "unreadable"
    verdict = None
    if value is not None:
        head = _VERDICT_CLAUSE_SUB_RE.match(
            _EMPHASIS_SUB_RE.sub("", value)).group(0).strip()
        verdict = head
        for known in planner.CODE_REVIEW_CLEARING_VERDICTS:
            if head.casefold() == known.casefold():
                classification = "clearing"
        for known in planner.CODE_REVIEW_BLOCKING_VERDICTS:
            if head.casefold() == known.casefold():
                classification = "blocking"
    return {
        "record": _safe_field(raw),
        "line": line_no,
        "verdict": None if verdict is None else _safe_field(verdict),
        "classification": classification,
        "problems": [] if problem is None else [problem],
    }


# --- rendering ---------------------------------------------------------------


def _predicate_text(value) -> str:
    """A planner predicate's own sentence, encoded but **not** elided.

    Encoded for the same reason everything else is -- a predicate quotes artifact
    bytes, so its message carries untrusted text.  Not elided because a preflight
    exists to say *what is missing*, and these sentences carry the remedy at the
    end: the field cap would cut every one of them mid-instruction and leave the
    operator with a diagnosis and no fix.  Bounding is instead the predicates'
    own job -- they are authored text, not attacker-chosen length.
    """
    return _safe_field(value, limit=None)


def _emit_list(label: str, values: List[str], *, empty: str) -> None:
    if not values:
        _emit(f"{label}: {empty}")
        return
    _emit(f"{label}:")
    for value in values:
        _emit(f"  - {value}")


def _print_json(payload: dict) -> None:
    """Deterministic, ASCII-safe machine output.

    `ensure_ascii=True` is the ASCII-safety clause; key order is the insertion
    order the builders write, which is fixed source order, so identical inputs
    give byte-identical output.  Printed raw -- the `lifecycle:` prefix is a
    human affordance and would make the stream unparseable.
    """
    print(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=False))


# --- subcommand: review-brief ------------------------------------------------


def _build_brief(root: Path, art, rel: str) -> dict:
    assurance, assurance_problems = _declared_assurance(root, art, rel)
    tier, tier_problems = _declared_tier(art)
    reviewed = _last_reviewed_commit(art)
    return {
        "schema": _BRIEF_SCHEMA,
        "artifact": rel,
        "kind": art.kind,
        "status": _safe_field(art.status) or None,
        "assurance_path": {"value": assurance, "problems": assurance_problems},
        "tier": {"value": tier, "problems": tier_problems},
        "current_contract": _contract_spans(art),
        "last_reviewed_commit": reviewed,
        "findings": _finding_ids(art),
        "changed_paths": _changed_paths(
            root, reviewed["value"] if reviewed["full"] else None),
        "boundary_b": _boundary_b_records(art),
    }


def cmd_review_brief(args: argparse.Namespace) -> int:
    """Extract and point at one artifact's review surface.  Writes nothing."""
    root = _repo_root()
    art, rel = _artifact(root, args.artifact)
    brief = _build_brief(root, art, rel)
    if args.format == "json":
        _print_json(brief)
        return 0

    _emit_section(f"review brief -- {rel}")
    _emit(f"kind: {brief['kind']}    status: {brief['status'] or '(none)'}")
    _emit(f"assurance path: {brief['assurance_path']['value'] or 'UNRESOLVED'}")
    for problem in brief["assurance_path"]["problems"]:
        _emit(f"  ! {problem}")
    _emit(f"tier: {brief['tier']['value']}")
    for problem in brief["tier"]["problems"]:
        _emit(f"  ! {problem}")

    _emit_section("complete-current-contract span")
    if not brief["current_contract"]:
        _emit("no revision section in this artifact")
    for span in brief["current_contract"]:
        _emit(f"L{span['line']}-{span['end_line']}  {span['heading']}")

    _emit_section("last reviewed commit")
    reviewed = brief["last_reviewed_commit"]
    if reviewed["record"] is None:
        _emit("no review record in this artifact")
    else:
        _emit(f"record: L{reviewed['line']}  {reviewed['record']}")
        _emit(f"Reviewed commit: {reviewed['value'] or '(absent)'}"
              + ("" if reviewed["full"] else "   [not a full 40-char commit id]"))
    for problem in reviewed["problems"]:
        _emit(f"  ! {problem}")

    _emit_section("finding ids")
    findings = brief["findings"]
    # Counts for the two historical sets, the full list for the one a reader
    # acts on.  An artifact with nine review rounds raises dozens of ids and
    # printing all of them buries the short list that matters; the machine
    # contract carries all three in full, so nothing is lost, only unstacked.
    _emit(f"raised: {len(findings['raised'])}    "
          f"named by a later Response: {len(findings['answered'])}")
    _emit_list("unanswered", findings["unanswered"], empty="none")
    _emit("(ids are extracted; whether an answer RESOLVED a finding is the "
          "reviewer's reading, not this tool's)")

    _emit_section("paths changed since the reviewed commit")
    changed = brief["changed_paths"]
    if not changed["available"]:
        _emit(f"UNAVAILABLE: {changed['reason']}")
    else:
        _emit(f"{changed['count']} path(s) since {changed['base']}")
        for path in changed["paths"]:
            _emit(f"  - {path}")
        if changed["withheld"]:
            _emit(f"  ... and {changed['withheld']} more")

    _emit_section("Boundary B records")
    if not brief["boundary_b"]:
        _emit("none")
    for record in brief["boundary_b"]:
        _emit(f"L{record['line']}  {record['date']}  {record['agent']}  "
              f"mode={record['mode'] or '(not stated)'}")

    _emit("brief: extraction only -- it points at records, grants no authority, "
          "and satisfies no gate")
    return 0


# --- subcommand: closeout ----------------------------------------------------


def _source_proposal(root: Path, art) -> dict:
    """The plan's declared source proposal, resolved to a real artifact if it is
    one.  A declaration that does not resolve is reported, never guessed at."""
    value, problem = _one_field(_header_region(art.text), "Source proposal")
    out: dict = {"declared": None if value is None else _safe_field(value),
                 "path": None, "status": None,
                 "problems": [] if problem is None else [problem]}
    if value is None:
        return out
    stem = value.strip()
    # The corpus writes this field as a markdown link, a bare stem, or a path;
    # take the last path-ish token and drop any extension.
    for token in reversed(re.split(r"[\s()\[\]<>|]+", stem)):
        token = token.strip().rstrip(",.;")
        if not token:
            continue
        candidate = token.split("/")[-1]
        if candidate.endswith(".md"):
            candidate = candidate[:-3]
        for _kind, parts in _ARTIFACT_DIRS[:2]:
            path = root.joinpath(*parts, candidate + ".md")
            if path.is_file():
                planner = _vocabulary()
                try:
                    proposal = planner.read_artifact(path)
                except Exception as exc:
                    out["problems"].append(
                        f"cannot parse {_safe_field(candidate)}.md: "
                        f"{_safe_field(exc)}")
                    return out
                out["path"] = path.relative_to(root).as_posix()
                out["status"] = _safe_field(proposal.status) or None
                return out
        break
    out["problems"].append(
        f"'Source proposal: {_safe_field(stem)}' names no artifact under "
        f"dev/proposals/[archive/]")
    return out


def _accepted_binding(art) -> dict:
    """The plan's `Inherited proposal basis:` bindings, or the absence of them.

    Absence is **not** a violation -- the 2026-08-11 revision makes inheritance a
    declaration, and a plan that took a distinct review declares none -- so it is
    reported as `not-declared` and the shape check runs only on what is written.
    The planner's `plan_inheritance_violations` is the predicate; this is the
    value.
    """
    value, problem = _one_field(_header_region(art.text),
                                "Inherited proposal basis")
    if value is None:
        return {"declared": False, "bindings": {}, "problems": []}
    bindings: dict = {}
    problems: List[str] = [] if problem is None else [problem]
    for clause in value.split(";"):
        if "=" not in clause:
            continue
        key, _, raw = clause.partition("=")
        bindings[_safe_field(key.strip())] = _safe_field(raw.strip())
    for key, sha in bindings.items():
        if not _FULL_SHA_RE.match(sha):
            problems.append(f"'{key}={sha}' is not a full 40-character commit id")
    return {"declared": True, "bindings": bindings, "problems": problems}


def _archive_paths(root: Path, rel: str) -> List[dict]:
    """The exact files a plan's archive transition must touch."""
    source = Path(rel)
    destination = source.parent / "archive" / source.name
    board = Path(*_BOARD_REL)
    return [
        {"role": "move-from", "path": source.as_posix(),
         "exists": (root / source).is_file()},
        {"role": "move-to", "path": destination.as_posix(),
         "exists": (root / destination).is_file()},
        {"role": "board-row", "path": board.as_posix(),
         "exists": (root / board).is_file()},
    ]


def _build_closeout(root: Path, art, rel: str) -> dict:
    planner = _vocabulary()
    assurance, assurance_problems = _declared_assurance(root, art, rel)
    # THE shared predicate.  `closeout` evaluates the state it is a preflight
    # FOR, exactly as `next --to <target>` does -- not `art.status`, which would
    # ask whether the plan is validly *where it is* rather than whether it may
    # move (the contract's own split, and the reason the state is a parameter).
    target = "ready-to-archive"
    preflight = [_predicate_text(v)
                 for v in planner.status_evidence_violations(art, target)]
    review = [_predicate_text(v)
              for v in planner.review_record_violations(art, target)]
    review += [_predicate_text(v) for v in planner.plan_inheritance_violations(art)]
    review += [_predicate_text(v) for v in planner.blocked_by_violations(art)]
    findings = _finding_ids(art)
    return {
        "schema": _CLOSEOUT_SCHEMA,
        "plan": rel,
        "status": _safe_field(art.status) or None,
        "target_state": target,
        "source_proposal": _source_proposal(root, art),
        "accepted_binding": _accepted_binding(art),
        "assurance_path": {"value": assurance, "problems": assurance_problems},
        "plan_review": {"declared": _safe_field(art.plan_review or "")
                        or None, "problems": review},
        "boundary_b": _boundary_b_records(art),
        "code_review": _code_review_result(art),
        "unanswered_findings": findings["unanswered"],
        "followups": {
            "dispositions_block": bool(art.has_disposition_attestation),
            "loop_fidelity_signoff": bool(art.has_fidelity_signoff),
        },
        "archive_paths": _archive_paths(root, rel),
        "preflight": {"violations": preflight, "clean": not preflight},
    }


def cmd_closeout(args: argparse.Namespace) -> int:
    """The archive completeness preflight.  Read-only; `--dry-run` is the only mode.

    Exit codes are the module's existing contract: `0` a clean preflight, `3`
    outstanding items (each printed with its reason), `1` a refusal.  A `3` is a
    statement about *completeness*, never about whether the evidence is good --
    the accepted contract keeps that with the reviewer, and this command "never
    edits, moves, commits, runs tests, or decides whether evidence is competent".
    """
    if not args.dry_run:
        raise LifecycleError(
            "closeout has no writing mode: pass --dry-run.  The accepted "
            "contract makes it a completeness preflight -- it never edits, "
            "moves, commits, runs tests, or decides whether evidence is "
            "competent -- so a mode that omitted --dry-run would be promising "
            "an action this command does not have")
    root = _repo_root()
    art, rel = _artifact(root, args.plan, require_kind="plan")
    report = _build_closeout(root, art, rel)
    if args.format == "json":
        _print_json(report)
        return 0 if report["preflight"]["clean"] else 3

    _emit_section(f"closeout preflight (dry run) -- {rel}")
    _emit(f"plan status: {report['status'] or '(none)'}    "
          f"evaluated against: {report['target_state']}")
    source = report["source_proposal"]
    _emit(f"source proposal: {source['path'] or source['declared'] or '(none)'}"
          f"    proposal status: {source['status'] or '(unresolved)'}")
    for problem in source["problems"]:
        _emit(f"  ! {problem}")
    binding = report["accepted_binding"]
    if not binding["declared"]:
        _emit("accepted proposal commit: not declared (this plan declares no "
              "inherited proposal basis)")
    else:
        for key, sha in binding["bindings"].items():
            _emit(f"accepted binding: {key}={sha}")
    for problem in binding["problems"]:
        _emit(f"  ! {problem}")
    _emit(f"assurance path: {report['assurance_path']['value'] or 'UNRESOLVED'}")
    for problem in report["assurance_path"]["problems"]:
        _emit(f"  ! {problem}")

    _emit_section("plan-review satisfaction")
    _emit(f"declared: {report['plan_review']['declared'] or '(undeclared)'}")
    _emit_list("reported by the shared predicates",
               report["plan_review"]["problems"], empty="nothing reported")

    _emit_section("Boundary B binding")
    if not report["boundary_b"]:
        _emit("no '## Implementation verification' record in this plan")
    for record in report["boundary_b"]:
        _emit(f"L{record['line']}  {record['date']}  {record['agent']}  "
              f"mode={record['mode'] or '(not stated)'}")

    _emit_section("latest code review")
    review = report["code_review"]
    if review["record"] is None:
        _emit("no conforming '## Code review -- <reviewer> -- <date>' pass")
    else:
        _emit(f"L{review['line']}  {review['record']}")
        _emit(f"verdict: {review['verdict'] or '(absent)'}  "
              f"[{review['classification']}]")
        for problem in review.get("problems", []):
            _emit(f"  ! {problem}")

    _emit_section("unanswered finding ids")
    _emit_list("unanswered", report["unanswered_findings"], empty="none")

    _emit_section("deferred follow-ups")
    followups = report["followups"]
    _emit(f"Dispositions block present: {followups['dispositions_block']}")
    _emit(f"loop-fidelity sign-off present: {followups['loop_fidelity_signoff']}")
    _emit("(presence is mechanical; whether each follow-up has a DURABLE home is "
          "a reading this tool does not make)")

    _emit_section("archive / board paths this transition must touch")
    for entry in report["archive_paths"]:
        _emit(f"{entry['role']}: {entry['path']}"
              f"   ({'present' if entry['exists'] else 'absent'})")

    _emit_section("preflight")
    if report["preflight"]["clean"]:
        _emit("CLEAN -- every mechanically checkable archive precondition holds")
        _emit("closeout: preflight only -- it never edits, moves, commits, runs "
              "tests, or decides whether evidence is competent")
        return 0
    for violation in report["preflight"]["violations"]:
        _emit(f"OUTSTANDING: {violation}")
    _emit(f"preflight: OUTSTANDING (exit 3) -- "
          f"{len(report['preflight']['violations'])} item(s)")
    _emit("closeout: preflight only -- it never edits, moves, commits, runs "
          "tests, or decides whether evidence is competent")
    return 3


# --- argument parsing --------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lifecycle",
        description=(
            "Deterministic backend for Cairn's session-start / session-end "
            "skills.  Orientation gather (plus one idempotent skills-fan-out "
            "self-heal write) and reflection-only goodnight, plus the "
            "monitoring-evidence report for the review allocation and its "
            "append-only event recorder; no network."
        ),
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_start = sub.add_parser(
        "session-start",
        help="Orientation gather (commits, tree state, threads, intents) "
             "plus one idempotent skills-fan-out self-heal write.",
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
        "--intent-grace-days",
        type=int,
        default=_INTENT_GRACE_DAYS,
        help=f"Full-handoff prune horizon for RELEASED work-intent pairs. Never "
             f"applies to an unreleased claim. Default: {_INTENT_GRACE_DAYS}.",
    )
    p_end.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned writes / a full-handoff mutation manifest and exit "
             "without writing anything.",
    )
    p_end.set_defaults(func=cmd_session_end)

    p_report = sub.add_parser(
        "pilot-report",
        help="Derive the monitoring-evidence report for the review allocation "
             "from the tracked activation record and event ledger. Writes "
             "nothing. Exit 3 means evidence is missing -- never that the "
             "review policy is off.",
    )
    p_report.set_defaults(func=cmd_pilot_report)

    p_record = sub.add_parser(
        "pilot-record",
        help="Append one event (a counted plan stem, or a pause set/cleared) "
             "to the append-only monitoring event ledger. The ledger's only "
             "writer.",
    )
    p_record.add_argument(
        "--kind", required=True, choices=list(_EVENT_KINDS),
        help="Which event to record.",
    )
    p_record.add_argument(
        "--subject", required=True,
        help="The plan stem (for plan-counted) or the pause identifier (for "
             "pause-set / pause-cleared).",
    )
    p_record.add_argument(
        "--source-artifact", required=True,
        help="Repository-relative path of the artifact this event is derived "
             "from. Must exist at --source-commit.",
    )
    p_record.add_argument(
        "--source-commit", required=True,
        help="Full 40-character commit id this event is bound to.",
    )
    p_record.add_argument(
        "--date", default=None,
        help="Event date as YYYY-MM-DD. Default: today.",
    )
    p_record.add_argument(
        "--severity", default=None, choices=list(_PAUSE_SEVERITIES),
        help="Pause severity (pause-set only).",
    )
    p_record.add_argument(
        "--review-input-bytes", type=int, default=0,
        help="Measured review-input bytes for a counted plan.",
    )
    p_record.add_argument(
        "--transitions-removed", type=int, default=0,
        help="Lifecycle transitions the allocation removed on this plan.",
    )
    p_record.add_argument(
        "--escaped-findings-high", type=int, default=0,
        help="High-severity findings that escaped to a later boundary.",
    )
    p_record.add_argument(
        "--escaped-findings-low", type=int, default=0,
        help="Lower-severity findings that escaped to a later boundary.",
    )
    p_record.add_argument(
        "--maintainer-prompts", type=int, default=0,
        help="Maintainer decision prompts this plan required.",
    )
    p_record.add_argument(
        "--note", default=None,
        help="Optional one-line note (bounded, printable ASCII).",
    )
    p_record.add_argument(
        "--dry-run", action="store_true",
        help="Print the event block that would be appended and write nothing.",
    )
    p_record.set_defaults(func=cmd_pilot_record)

    p_brief = sub.add_parser(
        "review-brief",
        help="Extract one artifact's review surface -- assurance path and "
             "tier, complete-current-contract span, last reviewed commit, "
             "finding ids, paths changed since that commit, and Boundary B "
             "records. Read-only; it points at records and grants no authority.",
    )
    p_brief.add_argument(
        "artifact",
        help="Repository-relative path, or a bare stem searched under "
             "dev/proposals/[archive/] and dev/plans/[archive/].",
    )
    p_brief.add_argument(
        "--format", choices=("text", "json"), default="text",
        help="'text' for the human report; 'json' for the versioned, "
             f"ASCII-safe machine contract ({_BRIEF_SCHEMA}).",
    )
    p_brief.set_defaults(func=cmd_review_brief)

    p_closeout = sub.add_parser(
        "closeout",
        help="Archive completeness preflight for a plan. Read-only: --dry-run "
             "is the only mode. Exit 3 means outstanding items -- never that "
             "the evidence is bad, which is the reviewer's reading.",
    )
    p_closeout.add_argument(
        "plan",
        help="Repository-relative path, or a bare stem searched under "
             "dev/plans/[archive/].",
    )
    p_closeout.add_argument(
        "--dry-run", action="store_true",
        help="Required. The command has no writing mode; the flag is explicit "
             "so the read-only contract is visible at the call site.",
    )
    p_closeout.add_argument(
        "--format", choices=("text", "json"), default="text",
        help="'text' for the human report; 'json' for the versioned, "
             f"ASCII-safe machine contract ({_CLOSEOUT_SCHEMA}).",
    )
    p_closeout.set_defaults(func=cmd_closeout)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except LifecycleError as exc:
        print(f"{_PREFIX} ERROR: {exc}", file=sys.stderr)
        return 1
    except MonitoringIncomplete as exc:
        # Exit 3, uniformly, wherever it is raised: an unsatisfied monitoring
        # dependency is neither a crash nor a clean run, and it is never
        # "the review policy is disabled".
        print(f"{_PREFIX} INCOMPLETE: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
