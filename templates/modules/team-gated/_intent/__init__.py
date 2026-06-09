#!/usr/bin/env python3
"""Work-intent helper: append-only JSONL substrate for pre-edit
coordination signals on shared-communication files.

This is the Cairn reference tool for the ``coordination-tiers``
module's Tier-2 work-intent protocol.  It ships the whole surface in
one stdlib-only file:

* the record schema (``claim`` / ``release`` events),
* path normalization,
* a best-effort atomic append,
* the read-side helpers (active intents, conflict check),
* per-session agent-identity resolution (and a ``whoami`` command
  that prints it -- the link anchor for other per-session surfaces
  such as the reflections channel's ``<session>`` token),
* a **folded-in** ``install-hook`` that writes a post-commit
  auto-release hook (no separate shell installer to ship), and
* an opt-in **``install-precommit``** work-intent check (warn-by-
  default) plus a ``hooks-status`` reporter for both hooks.

It is **stdlib-only** (``argparse``, ``dataclasses``, ``datetime``,
``hashlib``, ``json``, ``os``, ``subprocess``, ``sys``, ``pathlib``,
``typing``) and uses only **3.8-era syntax** — comfortably within Cairn's
declared ``>=3.11`` supported floor (``doctrine/runtime-contract.md``).

## Substrate

The active intent log is a single JSON-lines file at
``dev/intents.jsonl`` (gitignored; the scaffold seeds the entry).
Each line is one record; two event types:

* ``claim``   -- recorded when an agent intends to edit a
                 collision-prone surface.  Fields: ``event``, ``id``,
                 ``ts``, ``agent``, ``files``, ``action``, optional
                 ``stem``.
* ``release`` -- recorded when the claim's work has landed.  Fields:
                 ``event``, ``id``, ``ts``, optional ``commit``.

Active intents = claims without a matching release event (matched by
shared ``id``).

## Atomicity -- best-effort, filesystem-dependent

Concurrent appenders rely on the **implementation shape**, NOT on a
POSIX guarantee:

* ``os.open(path, O_WRONLY | O_APPEND | O_CREAT)`` -- the kernel
  positions every write at current EOF.
* A single ``os.write(fd, bytes)`` call per record, payload < 512
  bytes (a conservative small-write floor).
* No buffered-writer layer (text-mode ``open(..., 'a')`` would emit
  multiple ``write(2)`` calls and break the atomicity).

This is **best-effort and filesystem-dependent**.  POSIX specifies
atomic appends for pipes/FIFOs under ``PIPE_BUF``, *not* for regular
files; the small single-``write`` shape is non-interleaving on the
**local** filesystems this tooling is exercised on (APFS, ext4, xfs,
btrfs).  It is **not** guaranteed on **networked or overlay**
filesystems -- **NFS, SMB/CIFS, Windows network shares, and container
overlay FS** can interleave or reorder appends.  A team running the
intent log on such a filesystem, or at very high concurrency, should
treat the append as advisory and prefer a local checkout for the
``dev/`` tree.  (A stronger advisory-lock path is a possible future
enhancement; v1 ships the best-effort contract.)
"""
from __future__ import annotations

import dataclasses
import datetime
import hashlib
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Dict, Iterator, List, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Module-level paths + constants

# Shared-core leaf (intent-split A2): repo-root anchor + cross-subsystem path
# helpers. Re-exported here so the facade and every internal reference are unchanged.
from .shared import (  # noqa: F401  (re-exported for the facade)
    INTENTS_LOG_PATH,
    _REPO_ROOT,
    _read_nul_delimited_paths,
    normalize_path,
)
from .record_io import (  # noqa: F401  (re-exported for the facade)
    ClaimRecord,
    RECORD_SIZE_CAP,
    ReleaseRecord,
    _record_bytes,
    active_intents,
    append_record,
    conflict_check,
    generate_id,
    iter_log,
    read_log,
    write_claim,
    write_release,
)
from .identity import (  # noqa: F401  (re-exported for the facade)
    AGENT_ENV_VAR,
    DEFAULT_CONFIG_PATH,
    HARNESS_SESSION_VARS,
    _load_config,
    _session_digest,
    _session_identity,
    effective_harness_vars,
    resolve_agent_identity,
    resolve_session_token,
)
from .conflict import (  # noqa: F401  (re-exported for the facade)
    ALLOW_UNCLAIMED_ENV_VAR,
    DEFAULT_CLAIM_TTL_HOURS,
    ENFORCE_MODES,
    INCIDENT_EVENT_CLASS_DEFAULT,
    INCIDENT_LOG_RELPATH_DEFAULT,
    INTENT_CONFIG_RELPATH,
    INVOKE_HINT,
    PRECOMMIT_SENTINEL_BEGIN,
    PRECOMMIT_SENTINEL_END,
    _claim_is_stale,
    _classify_existing_precommit,
    _compute_overlaps,
    _confirm_proceed,
    _confirm_tty,
    _describe_collision,
    _drop_stale_claims,
    _format_conflict_warning,
    _git_path,
    _git_toplevel,
    _incident_tracker_skeleton,
    _insert_incident_row,
    _other_session_warning,
    _precommit_check_impl,
    _precommit_hook_block,
    _precommit_shebang_is_shell,
    _read_claim_ttl_hours,
    _read_enforce_mode,
    _read_incident_config,
    _read_solo_mode,
    _record_incident,
    _rename_map_via_git,
    _staged_paths_via_git,
    _strip_precommit_block,
    _unclaimed_warning,
    _unknown_identity_warning,
    classify_precommit_warnings,
    other_session_overlaps,
    split_file_tokens,
)


#: Split A2 (intent-split): this module is the *engine* loaded by the
#: ``intent.py`` facade (a runtime sibling). The facade re-derives
#: ``_REPO_ROOT`` / ``INTENTS_LOG_PATH`` from its own install path and threads
#: ``_FACADE_FILE`` (the launcher path the git hooks must invoke), overriding the
#: load-time values computed just above — which are one directory too deep when
#: measured from this submodule rather than from the facade. See ``intent.py``.
def _intent_tool_path() -> Path:
    """Filesystem path of the installed launcher/facade (``tools/intent.py``).

    The post-commit / pre-commit hooks must invoke the *facade*, not this engine
    submodule, so an installed hook keeps calling ``python tools/intent.py``. The
    facade threads its own path as ``_FACADE_FILE`` at load; absent that (e.g. a
    direct engine import), fall back to the sibling ``intent.py``.
    """
    facade = globals().get("_FACADE_FILE")
    if facade:
        return Path(facade).resolve()
    return Path(__file__).resolve().parent.parent / "intent.py"




#: Optional override of the hook's Python interpreter at install time.
PYTHON_ENV_VAR = "CAIRN_PYTHON"



#: Sentinel block markers for the post-commit hook.  Residue-free: no
#: project-specific naming leaks into an adopter's hook.
SENTINEL_BEGIN = "# >>> cairn/intent/post-commit BEGIN"
SENTINEL_END = "# <<< cairn/intent/post-commit END"












# ---------------------------------------------------------------------------
# Record schemas






# Path normalization -> extracted to _intent/shared.py (intent-split A2);
# re-exported via `from .shared import normalize_path` near the top of this module.


# ---------------------------------------------------------------------------
# Record serialization + atomic append






# ---------------------------------------------------------------------------
# Id generation




# ---------------------------------------------------------------------------
# High-level write helpers






# ---------------------------------------------------------------------------
# Read-side helpers










# ---------------------------------------------------------------------------
# Agent identity resolution (config-extensible registry)










# ---------------------------------------------------------------------------
# Conflict-warning formatting (the live signaler value)






# ---------------------------------------------------------------------------
# CLI command handlers


def _cmd_claim(args) -> int:
    """``intent claim`` -- append claim + emit conflict-warning."""
    log_path = (
        Path(args.log_path) if args.log_path is not None else INTENTS_LOG_PATH
    )
    agent = args.agent or resolve_agent_identity() or "unknown-agent"
    try:
        record = write_claim(
            agent=agent,
            files=split_file_tokens(args.files),
            action=args.action,
            stem=args.stem,
            log_path=log_path,
        )
    except ValueError as exc:
        sys.stderr.write(f"intent: {exc}\n")
        return 2
    overlap = [
        active for active in conflict_check(record.files, log_path=log_path)
        if active.get("id") != record.id
    ]
    if overlap:
        sys.stderr.write(_format_conflict_warning(record, overlap))
    else:
        sys.stderr.write(
            f"intent: claim recorded (id: {record.id}); no active overlaps "
            f"on your file set.\n"
        )
    sys.stdout.write(record.id + "\n")
    return 0


def _cmd_release(args) -> int:
    """``intent release`` -- append release record by id."""
    log_path = (
        Path(args.log_path) if args.log_path is not None else INTENTS_LOG_PATH
    )
    try:
        record = write_release(
            claim_id=args.id, commit=args.commit, log_path=log_path,
        )
    except ValueError as exc:
        sys.stderr.write(f"intent: {exc}\n")
        return 2
    sys.stderr.write(
        f"intent: release recorded (id: {record.id}"
        + (f", commit: {record.commit}" if record.commit else "")
        + ").\n"
    )
    return 0


def _cmd_list(args) -> int:
    """``intent list`` -- print active intents (optionally filtered)."""
    log_path = (
        Path(args.log_path) if args.log_path is not None else INTENTS_LOG_PATH
    )
    if args.conflicts_with:
        actives = conflict_check(
            split_file_tokens(args.conflicts_with), log_path=log_path,
        )
    else:
        actives = active_intents(log_path=log_path)
    if not actives:
        sys.stdout.write("intent: no active intents.\n")
        return 0
    for active in actives:
        sys.stdout.write(
            f"id={active.get('id')!r}\n"
            f"  agent={active.get('agent')!r}\n"
            f"  ts={active.get('ts')!r}\n"
            f"  files={active.get('files')!r}\n"
            f"  action={active.get('action')!r}\n"
        )
        if active.get("stem"):
            sys.stdout.write(f"  stem={active.get('stem')!r}\n")
    return 0


def _cmd_whoami(args) -> int:
    """``intent whoami`` -- print the resolved per-session agent identity.

    The default output is exactly the ``agent`` field stamped on every
    claim/release record in ``dev/intents.jsonl`` -- so it is the link
    anchor between the intent log and any other per-session surface.

    ``--session-token`` prints just the per-session token (the 8-hex
    ``sha256`` slice of the harness session id) -- the value a per-session
    surface outside the intent log reuses to link back to the same
    session.  Concretely, the reflections channel's filename
    ``<date>-<agent>-<session>.md`` sets ``<session>`` to this token, so
    its ``<agent>-<session>`` tail reconstructs this command's default
    output.  Exits non-zero with no stdout when no harness session id is
    exposed, signalling the caller to fall back to a random token.
    """
    if args.session_token:
        token = resolve_session_token()
        if token is None:
            sys.stderr.write(
                "intent whoami: no harness session id exposed -- no "
                "per-session token (fall back to a random token).\n"
            )
            return 1
        sys.stdout.write(token + "\n")
        return 0
    identity = resolve_agent_identity()
    if identity is None:
        sys.stderr.write(
            "intent whoami: agent identity unresolved (no $CAIRN_AGENT, "
            "harness session id, or config 'agent').\n"
        )
        return 1
    sys.stdout.write(identity + "\n")
    return 0


# ---------------------------------------------------------------------------
# Folded-in post-commit hook installer




def _resolve_hook_interpreter(explicit: Optional[str]) -> str:
    """Pick the interpreter to bake into the generated hook.

    Order: explicit ``--python`` arg -> ``$CAIRN_PYTHON`` -> the current
    ``sys.executable`` (captured at install time).  Never a bare
    ``python`` -- a hook runs in Git's environment where ``python`` may
    not resolve to the intended interpreter.
    """
    if explicit and explicit.strip():
        return explicit.strip()
    env_python = os.environ.get(PYTHON_ENV_VAR)
    if env_python and env_python.strip():
        return env_python.strip()
    return sys.executable


def _build_hook_block(python_exe: str, intent_path: Path) -> str:
    """Build the sentinel-wrapped post-commit hook block.

    The hook writes committed paths NUL-delimited to a temp file (no
    shell word-splitting of paths with spaces / newlines), then invokes
    this tool's ``_auto_release`` by **file path** under the captured
    interpreter (no ``python -m`` PATH/package assumption).

    The baked-in interpreter and script paths are emitted with
    ``shlex.quote`` (single-quoted), so a path containing a space, a
    double-quote, or shell metacharacters (``$(...)`` / backticks) cannot
    break the hook or be evaluated by ``/bin/sh`` -- double-quoting would
    still expand ``$`` and command substitution (security-hardening R13).
    """
    py_q = shlex.quote(python_exe)
    path_q = shlex.quote(str(intent_path))
    body = (
        'COMMIT_SHA=$(git rev-parse HEAD)\n'
        # Portable mktemp: an explicit template path works identically on
        # BSD (macOS) and GNU mktemp, unlike `-t` (GNU-deprecated, and
        # BSD/GNU interpret it differently).
        'PATHS_TMP=$(mktemp "${TMPDIR:-/tmp}/intent-paths.XXXXXX")\n'
        # --root makes the very first (parentless) commit list its files
        # too; it is a no-op for ordinary commits with a parent.
        'git diff-tree --root --no-commit-id --name-only -r -z HEAD '
        '> "${PATHS_TMP}"\n'
        f'{py_q} {path_q} _auto_release '
        '--commit "${COMMIT_SHA}" --paths-from-file "${PATHS_TMP}" || true\n'
        'rm -f "${PATHS_TMP}"'
    )
    return f"{SENTINEL_BEGIN}\n{body}\n{SENTINEL_END}"


#: Markers that identify a hook managed by a third-party framework; we
#: refuse to touch these rather than corrupt a generated file.
_FRAMEWORK_MARKERS: Tuple[Tuple[str, str], ...] = (
    ("pre-commit framework", "generated by pre-commit"),
    ("pre-commit framework", "INSTALL_PYTHON"),
    ("husky", "husky.sh"),
    ("husky", "_/husky"),
)


def _detect_framework(hook_text: str) -> Optional[str]:
    """Return a framework label if the hook looks framework-managed."""
    for label, marker in _FRAMEWORK_MARKERS:
        if marker in hook_text:
            return label
    return None


def _first_shebang_is_shell(hook_text: str) -> bool:
    """True when the hook's first line is a POSIX-shell shebang (sh/bash)."""
    first = hook_text.splitlines()[0] if hook_text else ""
    if not first.startswith("#!"):
        # No shebang -- treat as shell (we append a shell block); the
        # common case is a plain hook the adopter wrote without one.
        return True
    return ("sh" in first) and ("python" not in first) and (
        "node" not in first
    ) and ("ruby" not in first) and ("perl" not in first)


def _cmd_install_hook(args) -> int:
    """``intent install-hook`` -- install / replace / uninstall the
    post-commit auto-release hook (opt-in; never run by the scaffold).

    Refusal-before-mutation: every refusal path returns **without
    writing a byte or changing a mode**, so a refused adopter-managed
    hook is byte-for-byte and mode unchanged.
    """
    toplevel = _git_path("rev-parse", "--show-toplevel")
    if toplevel is None:
        sys.stderr.write(
            "intent: not inside a git working tree; cannot install the "
            "post-commit hook.\n"
        )
        return 1
    hooks_rel = _git_path("rev-parse", "--git-path", "hooks")
    if hooks_rel is None:
        sys.stderr.write(
            "intent: could not resolve the git hooks directory.\n"
        )
        return 1
    hooks_dir = Path(toplevel) / hooks_rel if not Path(
        hooks_rel
    ).is_absolute() else Path(hooks_rel)
    hook_file = hooks_dir / "post-commit"

    if args.uninstall:
        return _uninstall_hook(hook_file)

    python_exe = _resolve_hook_interpreter(args.python)
    intent_path = _intent_tool_path()
    new_block = _build_hook_block(python_exe, intent_path)

    if not hook_file.exists():
        hooks_dir.mkdir(parents=True, exist_ok=True)
        hook_file.write_text(
            "#!/usr/bin/env bash\n" + new_block + "\n", encoding="utf-8"
        )
        hook_file.chmod(0o755)
        sys.stderr.write(
            f"intent: installed fresh post-commit hook at {hook_file}.\n"
        )
        return 0

    # Existing hook -- decide whether to touch it BEFORE any mutation.
    existing = hook_file.read_text(encoding="utf-8")

    if SENTINEL_BEGIN in existing:
        # Our own block -- safe to replace idempotently.
        replaced = _replace_block(existing, new_block)
        hook_file.write_text(replaced, encoding="utf-8")
        sys.stderr.write(
            f"intent: replaced the cairn sentinel block in {hook_file}.\n"
        )
        return 0

    framework = _detect_framework(existing)
    if framework is not None:
        sys.stderr.write(
            f"intent: REFUSING to modify {hook_file} -- it looks "
            f"{framework}-managed. Add the auto-release step through your "
            f"framework's config, or run the block below manually:\n\n"
            f"{new_block}\n\n"
            f"intent: no changes made.\n"
        )
        return 4

    if not _first_shebang_is_shell(existing):
        first = existing.splitlines()[0] if existing else ""
        sys.stderr.write(
            f"intent: REFUSING to modify {hook_file} -- its shebang "
            f"({first!r}) is not a POSIX shell, so appending a shell block "
            f"would not run. Add this step in your hook's language, or run "
            f"the block below in a shell hook manually:\n\n{new_block}\n\n"
            f"intent: no changes made.\n"
        )
        return 4

    if not os.access(str(hook_file), os.X_OK):
        sys.stderr.write(
            f"intent: REFUSING to modify {hook_file} -- it exists but is "
            f"not executable (an adopter-managed or disabled hook). Make it "
            f"executable and re-run, or add the block below manually:\n\n"
            f"{new_block}\n\nintent: no changes made.\n"
        )
        return 4

    # Plain executable shell hook with no cairn block -- chain (append),
    # preserving the existing content and mode.
    sep = "" if existing.endswith("\n") else "\n"
    hook_file.write_text(existing + sep + new_block + "\n", encoding="utf-8")
    sys.stderr.write(
        f"intent: appended the cairn sentinel block to existing "
        f"{hook_file} (existing content preserved).\n"
    )
    return 0


def _replace_block(existing: str, new_block: str) -> str:
    """Replace the sentinel block (inclusive) in ``existing`` with
    ``new_block``; leave all other lines untouched."""
    out: List[str] = []
    in_block = False
    printed = False
    for line in existing.splitlines():
        if line == SENTINEL_BEGIN:
            in_block = True
            if not printed:
                out.extend(new_block.splitlines())
                printed = True
            continue
        if line == SENTINEL_END:
            in_block = False
            continue
        if not in_block:
            out.append(line)
    text = "\n".join(out)
    return text + "\n" if not text.endswith("\n") else text


def _uninstall_hook(hook_file: Path) -> int:
    """Strip the sentinel block; remove the file if nothing else remains."""
    if not hook_file.exists():
        sys.stderr.write(
            f"intent: no hook at {hook_file}; nothing to uninstall.\n"
        )
        return 0
    existing = hook_file.read_text(encoding="utf-8")
    if SENTINEL_BEGIN not in existing:
        sys.stderr.write(
            f"intent: no cairn sentinel block in {hook_file}; nothing to "
            f"uninstall.\n"
        )
        return 0
    out: List[str] = []
    in_block = False
    for line in existing.splitlines():
        if line == SENTINEL_BEGIN:
            in_block = True
            continue
        if line == SENTINEL_END:
            in_block = False
            continue
        if not in_block:
            out.append(line)
    remaining = [
        ln for ln in out if ln.strip() and not ln.startswith("#!")
    ]
    if remaining:
        text = "\n".join(out)
        hook_file.write_text(
            text + "\n" if not text.endswith("\n") else text,
            encoding="utf-8",
        )
        hook_file.chmod(0o755)
        sys.stderr.write(
            f"intent: removed the cairn sentinel block from {hook_file}.\n"
        )
    else:
        hook_file.unlink()
        sys.stderr.write(
            f"intent: removed the cairn sentinel block and the now-empty "
            f"{hook_file}.\n"
        )
    return 0


# _read_nul_delimited_paths -> extracted to _intent/shared.py (intent-split A2);
# re-exported via `from .shared import _read_nul_delimited_paths` near the top.


def _cmd_auto_release(args) -> int:
    """``intent _auto_release`` -- internal; called by the post-commit hook.

    Resolves identity (fail-soft), reads committed paths, and appends
    release records for the resolved agent's claims whose files
    intersect the commit.  Always exits 0 -- the commit has already
    landed; the hook must never be a nuisance.
    """
    log_path = (
        Path(args.log_path) if args.log_path is not None else INTENTS_LOG_PATH
    )
    try:
        agent = resolve_agent_identity()
        if agent is None:
            sys.stderr.write(
                "intent: agent identity not configured ($CAIRN_AGENT unset, "
                "no harness session var, and ~/.cairn/agent.json missing or "
                "unreadable); skipping auto-release for commit "
                f"{(args.commit or '')[:8]}.\n"
            )
            return 0

        # Override-shadow warning: a global CAIRN_AGENT export shadows the
        # per-session derivation, collapsing concurrent same-tool sessions
        # to one identity and risking cross-release of another session's
        # claims.  Warn (don't block) when the override is set AND an
        # effective harness session var is also present.
        env_override = os.environ.get(AGENT_ENV_VAR)
        if env_override and env_override.strip():
            config = _load_config()
            shadowed = None
            for _tag, sv in effective_harness_vars(config):
                if os.environ.get(sv):
                    shadowed = sv
                    break
            if shadowed is not None:
                sys.stderr.write(
                    f"intent: WARNING -- {AGENT_ENV_VAR}="
                    f"{env_override.strip()!r} is shadowing the per-session "
                    f"identity that would derive from ${shadowed}. A global "
                    f"{AGENT_ENV_VAR} export collapses concurrent same-tool "
                    f"sessions to one identity and can cross-release other "
                    f"sessions' claims; unset it to use per-session "
                    f"derivation (it is an escape hatch, not a profile "
                    f"setting).\n"
                )

        if args.paths_from_file is None:
            sys.stderr.write(
                "intent: _auto_release called without --paths-from-file; "
                "nothing to release.\n"
            )
            return 0
        committed_paths = _read_nul_delimited_paths(args.paths_from_file)
        if not committed_paths:
            return 0

        committed_set = {normalize_path(p) for p in committed_paths}
        actives = active_intents(log_path=log_path)
        released_count = 0
        for active in actives:
            if active.get("agent") != agent:
                continue
            active_files = active.get("files") or []
            if not isinstance(active_files, list):
                continue
            active_set = {normalize_path(str(f)) for f in active_files}
            if active_set & committed_set:
                claim_id = active.get("id")
                if isinstance(claim_id, str):
                    try:
                        write_release(
                            claim_id=claim_id,
                            commit=args.commit,
                            log_path=log_path,
                        )
                        released_count += 1
                    except (OSError, ValueError) as inner:
                        sys.stderr.write(
                            f"intent: auto-release failed for claim "
                            f"{claim_id}: {inner}\n"
                        )
        if released_count > 0:
            sys.stderr.write(
                f"intent: auto-released {released_count} "
                f"{'claim' if released_count == 1 else 'claims'} on commit "
                f"{(args.commit or '')[:8]}.\n"
            )
    except Exception as exc:  # noqa: BLE001 -- never block commits
        sys.stderr.write(
            f"intent: _auto_release internal error (commit already landed; "
            f"ignoring): {exc}\n"
        )
    return 0


# ---------------------------------------------------------------------------
# Pre-commit work-intent check (opt-in; warn-by-default)
#
# The opt-in pre-commit hook warns (never blocks -- block-mode is a
# deferred follow-up) when a commit's staged paths are unclaimed or held
# by another session.  Three pieces ship here:
#
#   * install-precommit -- the installer (narrow v1 composition: install
#                          only into an absent hook or one carrying our
#                          sentinel; refuse any foreign / framework hook).
#   * _precommit_check  -- the hook body's worker; reads the commit's
#                          staged set, classifies each path, warns.
#   * hooks-status      -- reports install state of BOTH hooks, so
#                          session-start points at one stable command.




def _resolve_hooks_dir() -> Optional[Path]:
    """Resolve the git hooks directory (worktree- and hooksPath-aware).

    Mirrors the post-commit installer's resolution so a custom
    ``core.hooksPath`` or a linked worktree lands the pre-commit hook in
    the same directory git actually consults.
    """
    toplevel = _git_path("rev-parse", "--show-toplevel")
    if toplevel is None:
        return None
    hooks_rel = _git_path("rev-parse", "--git-path", "hooks")
    if hooks_rel is None:
        return None
    return (
        Path(hooks_rel)
        if Path(hooks_rel).is_absolute()
        else Path(toplevel) / hooks_rel
    )














# ---------------------------------------------------------------------------
# Sensing write-path -- record a work-intent collision as an incident row
# (self-evolution-loop Part B). Everything here is **best-effort & fail-safe**:
# a failure NEVER blocks, slows, or fails the commit (R1); the tool only ever
# *appends a markdown row* -- never a ``git reset`` / index mutation (N4).




































def _cmd_install_precommit(args) -> int:
    """``intent install-precommit`` -- install / uninstall the opt-in
    pre-commit work-intent check.

    Narrow v1 composition: install only into an absent hook or one
    already carrying our sentinel block; refuse (without mutation) any
    framework-managed / non-shell / non-executable / foreign existing
    hook.  ``--uninstall`` removes only the sentinel block (and the file
    when nothing else remains)."""
    hooks_dir = _resolve_hooks_dir()
    if hooks_dir is None:
        sys.stderr.write(
            "intent: not inside a git working tree; cannot install the "
            "pre-commit hook.\n"
        )
        return 1
    hook_file = hooks_dir / "pre-commit"

    if args.uninstall:
        if not hook_file.exists():
            sys.stdout.write(
                f"intent: no hook at {hook_file}; nothing to uninstall.\n"
            )
            return 0
        text = hook_file.read_text(encoding="utf-8", errors="replace")
        if PRECOMMIT_SENTINEL_BEGIN not in text:
            sys.stdout.write(
                f"intent: {hook_file} carries no intent pre-commit sentinel "
                "block; leaving it untouched.\n"
            )
            return 0
        stripped = _strip_precommit_block(text)
        meaningful = [
            ln for ln in stripped.splitlines()
            if ln.strip() and not ln.strip().startswith("#!")
        ]
        if not meaningful:
            hook_file.unlink()
            sys.stdout.write(
                f"intent: removed sentinel block (and now-empty hook) at "
                f"{hook_file}.\n"
            )
        else:
            hook_file.write_text(
                stripped.rstrip("\n") + "\n", encoding="utf-8",
            )
            hook_file.chmod(0o755)
            sys.stdout.write(
                f"intent: removed sentinel block from {hook_file}; other "
                "content preserved.\n"
            )
        return 0

    # Install path.
    klass = _classify_existing_precommit(hook_file)
    if klass not in ("absent", "sentinel"):
        sys.stderr.write(
            f"intent: REFUSING to modify {hook_file} -- existing pre-commit "
            f"hook looks {klass}.\n"
            "intent: v1 installs only into an absent hook or one carrying "
            "the intent sentinel block. Move / inspect the existing hook, "
            "or chain the work-intent check manually:\n"
            f"  {INVOKE_HINT} _precommit_check\n"
            "intent: no changes made.\n"
        )
        return 4

    python_exe = _resolve_hook_interpreter(args.python)
    intent_path = _intent_tool_path()
    block = _precommit_hook_block(python_exe, intent_path)
    if klass == "absent":
        content = "#!/usr/bin/env bash\n" + block + "\n"
    else:  # sentinel -- replace the block, preserve other content
        stripped = _strip_precommit_block(
            hook_file.read_text(encoding="utf-8", errors="replace"),
        )
        lines = stripped.splitlines()
        if not (lines and lines[0].startswith("#!")):
            lines.insert(0, "#!/usr/bin/env bash")
        while lines and not lines[-1].strip():
            lines.pop()
        content = "\n".join(lines) + "\n" + block + "\n"
    hook_file.parent.mkdir(parents=True, exist_ok=True)
    hook_file.write_text(content, encoding="utf-8")
    hook_file.chmod(0o755)
    verb = "installed" if klass == "absent" else "updated"
    sys.stdout.write(
        f"intent: {verb} pre-commit work-intent check at {hook_file}.\n"
    )
    return 0






def _cmd_precommit_check(args) -> int:
    """``intent _precommit_check`` -- the pre-commit hook's worker.

    Emits classified warnings to stderr, then applies the configured enforce
    mode (#53): ``warn`` (exit 0), ``confirm`` (prompt; proceed on ack, else
    degrade to ``block`` with no TTY -- R2), ``block`` (exit non-zero; **the
    shipped default** -- foldback-drain Fold A) -- but a block only fires when a
    *different live session* holds a **fresh** (within-TTL) claim on a staged
    path **and** the committer has a per-session token. An unclaimed path still
    only warns; the bypass env var / solo mode always exempts. **Fail-open by
    construction:** any internal error returns 0 (the hook no longer carries
    ``|| true``, so a crash must not wedge commits)."""
    try:
        return _precommit_check_impl(args)
    except Exception as exc:  # noqa: BLE001 -- fail-open is the contract
        sys.stderr.write(
            f"intent: pre-commit check errored ({exc!r}); allowing the "
            "commit (fail-open).\n"
        )
        return 0




def _hook_installed(hook_file: Path, sentinel_begin: str) -> bool:
    """True when ``hook_file`` exists and carries ``sentinel_begin``."""
    if not hook_file.exists():
        return False
    try:
        return sentinel_begin in hook_file.read_text(
            encoding="utf-8", errors="replace",
        )
    except OSError:
        return False


def _cmd_hooks_status(args) -> int:
    """``intent hooks-status`` -- report install state of BOTH the
    post-commit auto-release hook and the pre-commit work-intent check.

    Human-readable + parseable: each hook prints on its own line with a
    stable ``installed`` / ``not-installed`` token, so session-start (and
    any script) can point at one stable command."""
    hooks_dir = _resolve_hooks_dir()
    if hooks_dir is None:
        sys.stderr.write(
            "intent: not inside a git working tree; cannot report hook "
            "status.\n"
        )
        return 1
    post = _hook_installed(hooks_dir / "post-commit", SENTINEL_BEGIN)
    pre = _hook_installed(hooks_dir / "pre-commit", PRECOMMIT_SENTINEL_BEGIN)
    post_tok = "installed" if post else "not-installed"
    pre_tok = "installed" if pre else "not-installed"
    sys.stdout.write(
        "intent hooks-status:\n"
        f"  post-commit (auto-release): {post_tok}\n"
        f"  pre-commit (work-intent check): {pre_tok}\n"
    )
    if not post:
        sys.stdout.write(
            f"  -> install post-commit: {INVOKE_HINT} install-hook\n"
        )
    if not pre:
        sys.stdout.write(
            f"  -> install pre-commit:  {INVOKE_HINT} install-precommit\n"
        )
    return 0


# ---------------------------------------------------------------------------
# Argument parser


def _build_parser():
    import argparse

    parser = argparse.ArgumentParser(
        prog=INVOKE_HINT,
        description=(
            "Work-intent helper: append-only JSONL substrate for pre-edit "
            "coordination signals. See the coordination-tiers module for "
            "the doctrine."
        ),
    )
    parser.add_argument(
        "--log-path",
        default=None,
        help=(
            "Override the active intent log path (default: "
            "dev/intents.jsonl in the repo root). Mainly for tests."
        ),
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_claim = sub.add_parser(
        "claim",
        help=(
            "Record a new claim. Runs an immediate conflict-check against "
            "active claims; warns to stderr on overlap. Prints the new "
            "claim id to stdout."
        ),
    )
    p_claim.add_argument(
        "--files", nargs="+", required=True,
        help=(
            "One or more files this claim covers. Space- or comma-separated "
            "(or a mix)."
        ),
    )
    p_claim.add_argument(
        "--action", required=True, help="Short verb-phrase naming the work.",
    )
    p_claim.add_argument(
        "--stem", default=None,
        help=(
            "Optional short topic key. Use when long --files lists + verbose "
            "--action would blow the 512-byte record cap."
        ),
    )
    p_claim.add_argument(
        "--agent", default=None,
        help=(
            "Override agent identity (default: $CAIRN_AGENT, a harness "
            "session id, ~/.cairn/agent.json, or 'unknown-agent')."
        ),
    )
    p_claim.set_defaults(func=_cmd_claim)

    p_release = sub.add_parser(
        "release", help="Record a release event for an existing claim.",
    )
    p_release.add_argument(
        "id", help="The claim id (as returned by `intent claim`).",
    )
    p_release.add_argument(
        "--commit", default=None,
        help=(
            "Optional short SHA of the releasing commit (populated by the "
            "post-commit hook; omit for manual release)."
        ),
    )
    p_release.set_defaults(func=_cmd_release)

    p_list = sub.add_parser(
        "list", help="Print active intents (claims without matching releases).",
    )
    p_list.add_argument(
        "--conflicts-with", nargs="+", default=None,
        help=(
            "Filter to active intents whose file sets intersect these paths. "
            "Space- or comma-separated (or a mix)."
        ),
    )
    p_list.set_defaults(func=_cmd_list)

    p_whoami = sub.add_parser(
        "whoami",
        help=(
            "Print the resolved per-session agent identity (the intent "
            "log's `agent` field). --session-token prints just the "
            "per-session hash token, the value the reflections channel "
            "reuses as <session> so the two surfaces link."
        ),
    )
    p_whoami.add_argument(
        "--session-token", action="store_true",
        help=(
            "Print only the per-session token (8-hex sha256 of the harness "
            "session id), not the full <tool_tag>-<token> identity. Exits "
            "non-zero with no output when no harness session id is exposed."
        ),
    )
    p_whoami.set_defaults(func=_cmd_whoami)

    p_install = sub.add_parser(
        "install-hook",
        help=(
            "Install (or uninstall) the post-commit auto-release hook. "
            "Opt-in: the scaffold never runs this for you."
        ),
    )
    p_install.add_argument(
        "--uninstall", action="store_true",
        help="Remove the previously-installed sentinel block.",
    )
    p_install.add_argument(
        "--python", default=None,
        help=(
            "Interpreter to bake into the generated hook (default: "
            "$CAIRN_PYTHON or this run's interpreter). Never a bare 'python'."
        ),
    )
    p_install.set_defaults(func=_cmd_install_hook)

    p_install_pre = sub.add_parser(
        "install-precommit",
        help=(
            "Install (or uninstall) the opt-in pre-commit work-intent "
            "check (warn-by-default). The scaffold never runs this for you."
        ),
    )
    p_install_pre.add_argument(
        "--uninstall", action="store_true",
        help="Remove the previously-installed sentinel block.",
    )
    p_install_pre.add_argument(
        "--python", default=None,
        help=(
            "Interpreter to bake into the generated hook (default: "
            "$CAIRN_PYTHON or this run's interpreter). Never a bare 'python'."
        ),
    )
    p_install_pre.set_defaults(func=_cmd_install_precommit)

    p_status = sub.add_parser(
        "hooks-status",
        help=(
            "Report install state of BOTH the post-commit auto-release "
            "and the pre-commit work-intent-check hooks."
        ),
    )
    p_status.set_defaults(func=_cmd_hooks_status)

    p_precheck = sub.add_parser(
        "_precommit_check",
        help="Internal: called by the pre-commit work-intent-check hook.",
    )
    p_precheck.add_argument(
        "--paths-from-file", default=None,
        help="Path to a NUL-delimited file listing the staged paths.",
    )
    p_precheck.set_defaults(func=_cmd_precommit_check)

    p_auto = sub.add_parser(
        "_auto_release", help="Internal: called by the post-commit hook.",
    )
    p_auto.add_argument(
        "--commit", default=None, help="SHA of the just-landed commit.",
    )
    p_auto.add_argument(
        "--paths-from-file", default=None,
        help="Path to a NUL-delimited file listing the committed paths.",
    )
    p_auto.set_defaults(func=_cmd_auto_release)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
