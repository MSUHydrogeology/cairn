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
  destructive full-handoff path (roadmap scrub, prune, metrics) is gated behind
  an explicit `--handoff` plus a designation marker and a concurrent-handoff
  lock.  In this chunk that gated path is not yet wired -- `--handoff` refuses
  -- so the tool can never run an unguarded destructive step.  (The fail-safe,
  the lock, and the interpreter-resolution binding land in the next chunk.)

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


def _resolve_agent() -> str:
    """Resolve the agent identifier used in the reflection filename.

    Chunk-1 scope: honor an explicit ``CAIRN_AGENT`` override, else fall back to
    a neutral default.  (The richer harness-session identity resolution lives in
    the optional `intent.py`; the reflection filename does not need it.)
    """
    return os.environ.get("CAIRN_AGENT", "agent").strip() or "agent"


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

    if not isinstance(data, dict) or "interpreter" not in data:
        raise LifecycleError(
            f'{cfg} must be a JSON object with a single "interpreter" key.'
        )
    value = data["interpreter"]
    if not isinstance(value, str) or not value.strip():
        raise LifecycleError(f'{cfg}: "interpreter" must be a non-empty string.')
    # No arguments / shell interpolation: a bare path only.
    if any(ch in value for ch in (" ", "\t", ";", "&", "|", "$", "`", "\n")):
        raise LifecycleError(
            f'{cfg}: "interpreter" must be a bare absolute path with no '
            "arguments or shell metacharacters."
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


# --- subcommand: session-start ----------------------------------------------


def cmd_session_start(args: argparse.Namespace) -> int:
    """Read-only orientation gather: commits, tree state, threads, intents.

    Purely informational -- writes nothing.  The skill body relays this output
    and then performs the judgment steps (role confirmation, deciding which
    thread to pick up) that a tool cannot make.
    """
    root = _repo_root()
    marker = args.handoff_marker
    fallback_n = args.fallback_commits

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

    _emit_section("active work-intents")
    intent_tool = _sibling_tool("intent.py")
    if intent_tool is None:
        _warn(
            "intent.py (coordination-tiers) not installed -- skipping the "
            "active-intent read; if your team uses work-intents, install it."
        )
    else:
        # Surface the active claims read-only so the starting session sees who
        # holds which paths before its first edit (the read half of the
        # work-intent convention).  Invoked as an explicit argv list under the
        # resolved interpreter -- never a shell string (S2/S5).
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

    # S2: make the (otherwise hidden) interpreter trust root visible.
    _emit_section("resolved project interpreter")
    _emit(f"interpreter: {interpreter}  (from {interp_source})")
    if interp_source == "fallback":
        _warn(
            "no dev/.cairn/local-env.json -- using the current interpreter; "
            "bootstrap normally writes this binding so the routine resolves it "
            "directly instead of relying on shell activation."
        )

    _emit("session-start gather complete (read-only).")
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


def _run_lifecycle_metrics(root: Path, interpreter: str) -> None:
    """Run the optional lifecycle-metrics tool read-only, if installed."""
    tool = _sibling_tool("lifecycle_metrics.py")
    if tool is None:
        _warn("lifecycle_metrics.py not installed -- skipping the metrics pass.")
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
        if proc.returncode == 0:
            _emit("lifecycle-metrics: ran (read-only).")
        else:
            _warn(f"lifecycle_metrics reported: {(proc.stderr or '').strip()}")
    except OSError as exc:
        _warn(f"could not run lifecycle_metrics.py: {exc}")


# --- subcommand: session-end -------------------------------------------------

_REFLECTION_SKELETON = """\
# Session reflection -- {agent} -- {date}

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
    """Scaffold the per-agent reflection file (non-destructive; both modes)."""
    refl_dir = _reflections_dir(root)
    agent = _resolve_agent()
    target = refl_dir / f"{_today()}-{agent}.md"

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
            _REFLECTION_SKELETON.format(agent=agent, date=_today()),
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
    with HandoffLock(root, _resolve_agent()) as lock:
        _emit_section("pruning reflections")
        pruned = _prune_reflections(root, grace, dry_run=False)
        _emit(f"pruned {len(pruned)} reflection(s) older than {grace}d.")
        lock.heartbeat()

        _emit_section("lifecycle metrics")
        _run_lifecycle_metrics(root, interpreter)
        lock.heartbeat()

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
        help="Goodnight.  Reflection-only by default; full handoff is gated "
             "behind --handoff (not yet wired).",
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
