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
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

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
        # work-intent convention).
        try:
            proc = subprocess.run(
                [sys.executable, str(intent_tool), "list"],
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

    _emit("session-start gather complete (read-only).")
    return 0


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


def cmd_session_end(args: argparse.Namespace) -> int:
    """Goodnight, reflection-only mode (the safe default).

    Creates the reflection scaffold and surfaces open threads -- both
    non-destructive.  The destructive full-handoff path (roadmap scrub, prune,
    lifecycle-metrics) is gated behind `--handoff`; in this chunk that path is
    not yet wired (it lands with the fail-safe default + designation marker +
    concurrent-handoff lock), so `--handoff` refuses rather than running an
    unguarded scrub.
    """
    if args.handoff:
        # Fail closed: the guarded path does not exist yet, so refuse loudly
        # rather than silently doing reflection-only work under a flag that
        # implies more.
        raise LifecycleError(
            "the full-handoff path is not available yet: it requires the "
            "fail-safe default, the maintainer-designation marker, and the "
            "concurrent-handoff lock, which land in the next implementation "
            "chunk.  Run `session-end` (reflection-only) for now."
        )

    root = _repo_root()
    refl_dir = _reflections_dir(root)
    agent = _resolve_agent()
    target = refl_dir / f"{_today()}-{agent}.md"

    _emit_section("reflection scaffold")
    if target.exists():
        _emit(
            f"reflection already exists: {target.relative_to(root)} "
            "-- leaving it untouched; edit it directly."
        )
    elif args.dry_run:
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

    _emit_section("open threads to note in your reflection")
    threads = _in_flight(root)
    if threads:
        for line in threads:
            print(f"{_PREFIX}   {line}")
    else:
        print(f"{_PREFIX} (no open proposals or plans)")

    _emit(
        "reflection-only goodnight complete.  The full handoff (roadmap "
        "scrub, NEXT_SESSION rewrite, prune, metrics, handoff commit) is a "
        "designated-owner action under `--handoff`."
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
        help="Run the full-handoff path (designated owner only).  Not "
             "available yet -- refuses until the fail-safe + lock land.",
    )
    p_end.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned writes and exit without writing anything.",
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
