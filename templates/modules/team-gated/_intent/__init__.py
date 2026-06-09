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



#: Highest-priority agent-identity override env var.  An explicit
#: escape hatch for tests / one-offs; a *global* export re-introduces
#: the shared-identity footgun (it shadows the per-session tier below),
#: so the auto-release path warns when it shadows an available session
#: var, and the doctrine flags global exports as not-recommended.
AGENT_ENV_VAR = "CAIRN_AGENT"

#: Optional override of the hook's Python interpreter at install time.
PYTHON_ENV_VAR = "CAIRN_PYTHON"

#: Default JSON identity-config path (stdlib JSON, no third-party dep).
#: Keys (all optional):
#:   * ``agent`` -- a static identity string (lowest-priority tier).
#:   * ``harness_session_vars`` -- a list of ``[tool_tag, env_var]``
#:     pairs **appended** to the built-in registry below, so an adopter
#:     on a different harness registers its session env var without
#:     editing this file.
DEFAULT_CONFIG_PATH = Path("~/.cairn/agent.json")

#: Built-in harness session-scoped env vars, in (tool_tag, env_var)
#: order.  Each identifies the *current session* of one agent harness;
#: the derived identity is per-session-unique, so concurrent same-tool
#: sessions get distinct identities and auto-release never cross-releases
#: between them.  Adopters extend this set via the JSON config's
#: ``harness_session_vars`` key (see :func:`effective_harness_vars`).
HARNESS_SESSION_VARS: Tuple[Tuple[str, str], ...] = (
    ("claude", "CLAUDE_CODE_SESSION_ID"),
    ("codex", "CODEX_THREAD_ID"),
    ("antigravity", "ANTIGRAVITY_TRAJECTORY_ID"),
)

#: Sentinel block markers for the post-commit hook.  Residue-free: no
#: project-specific naming leaks into an adopter's hook.
SENTINEL_BEGIN = "# >>> cairn/intent/post-commit BEGIN"
SENTINEL_END = "# <<< cairn/intent/post-commit END"

#: Sentinel markers wrapping the opt-in **pre-commit** work-intent-check
#: block.  Mirror the post-commit grammar so ``--uninstall`` and
#: ``hooks-status`` find / strip exactly the helper-managed lines.
PRECOMMIT_SENTINEL_BEGIN = "# >>> cairn/intent/pre-commit BEGIN"
PRECOMMIT_SENTINEL_END = "# <<< cairn/intent/pre-commit END"

#: Per-commit env override: when set non-empty, the pre-commit
#: work-intent check suppresses the *self-directed* warnings (no-claim +
#: unknown-identity) for this one commit.  An **other-session overlap**
#: warning is NEVER suppressed -- coordination is the payoff that must
#: always surface.  Deterministic exemption: no semantic auto-exemption.
ALLOW_UNCLAIMED_ENV_VAR = "CAIRN_INTENT_ALLOW_UNCLAIMED"

#: Optional tracked repo-local solo-mode config, read relative to the
#: repo root.  ``{"solo_mode": true}`` suppresses the self-directed
#: warnings repo-wide (a deliberate, tracked opt-out for a solo-agent
#: repo).  Absent / false / malformed = warn.
INTENT_CONFIG_RELPATH = "dev/intent-config.json"

#: Default claim TTL (hours) for the pre-commit block decision. A claim
#: older than this is **stale**: it still WARNS, but a stale cross-claim
#: never *blocks* a commit -- a crashed / abandoned session must not wedge a
#: live committer (foldback-drain Fold A / R1; the 4h value is Antigravity
#: R1's). Configurable via ``dev/intent-config.json`` ``"claim_ttl_hours"``.
DEFAULT_CLAIM_TTL_HOURS = 4.0

#: Sensing write-path (self-evolution-loop Part B): where the pre-commit hook
#: records a work-intent collision as an ``incident-trackers`` row, and the
#: adopter-defined event-class name for it. Both overridable in
#: ``dev/intent-config.json`` (``"incident_log_path"`` / ``"incident_event_class"``).
#: The default tracker is the staged-index / coordination collision log (the
#: D-IR3-cited surface). Recording is **best-effort & fail-safe**: it never
#: blocks, slows, or fails a commit (R1), and only ever *appends a row* -- never
#: a ``git reset`` or index mutation (N4).
INCIDENT_LOG_RELPATH_DEFAULT = "dev/measurement/collision_log.md"
INCIDENT_EVENT_CLASS_DEFAULT = "work-intent-claim-conflict"

#: Adopter-facing invocation hint for run-guidance strings.  The scaffold
#: installs this tool verbatim at ``<target>/tools/intent.py`` -- there is
#: no ``intent`` console entry point -- so every command we *suggest* an
#: adopter type uses the installed script shape, matching the
#: ``coordination-tiers`` doc and the session-start routine.  (Internal
#: docstrings keep the bare ``intent <subcommand>`` man-page label.)
INVOKE_HINT = "python tools/intent.py"


def _session_digest(raw_session_id: Optional[str]) -> Optional[str]:
    """The per-session token: the 8-hex ``sha256`` slice of a raw harness
    session id, or ``None`` when the raw id is missing / empty /
    whitespace-only.

    The id is **hashed in full**, never prefix-sliced: harness session
    ids may be time-ordered (e.g. UUIDv7, whose leading bytes are a
    timestamp shared by near-simultaneous sessions), so a prefix would
    collapse exactly the concurrent same-tool sessions this identity
    model exists to separate.  Hashing the whole id is harness-neutral
    and keeps the written token safe + bounded regardless of the raw
    id's shape.

    This token is the single per-session value the rest of the system
    keys on: :func:`_session_identity` tags it (``<tool_tag>-<token>``)
    for the intent log's ``agent`` field, and :func:`resolve_session_token`
    exposes it bare for any other per-session surface that wants to link
    back to the same session (e.g. the reflections channel's
    ``<session>`` filename token).
    """
    if not raw_session_id or not raw_session_id.strip():
        return None
    return hashlib.sha256(
        raw_session_id.strip().encode("utf-8"),
    ).hexdigest()[:8]


def _session_identity(
    tool_tag: str, raw_session_id: Optional[str],
) -> Optional[str]:
    """Form a bounded, per-session agent identity from a raw session id.

    Returns ``None`` when ``raw_session_id`` is missing / empty /
    whitespace-only, so the caller falls through to the next resolution
    tier.  Otherwise returns ``<tool_tag>-<token>``, where ``<token>`` is
    the :func:`_session_digest` per-session hash.
    """
    digest = _session_digest(raw_session_id)
    if digest is None:
        return None
    return f"{tool_tag}-{digest}"


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


def _load_config(config_path: Optional[Path] = None) -> Optional[dict]:
    """Load the JSON identity config; return a dict or ``None``.

    ``None`` on any failure (missing file, malformed JSON, non-object
    top level) -- identity resolution then falls through.
    """
    target = config_path
    if target is None:
        home = os.environ.get("HOME")
        if not home:
            # No HOME -- try the documented default literally so an
            # explicit override path still works on platforms without
            # HOME set.
            target = DEFAULT_CONFIG_PATH.expanduser()
        else:
            target = (Path(home) / ".cairn" / "agent.json")
    target = target.expanduser()
    if not target.exists():
        return None
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    return data


def effective_harness_vars(
    config: Optional[dict] = None,
) -> Tuple[Tuple[str, str], ...]:
    """Return the built-in registry plus any adopter extensions.

    Adopter extensions come from the JSON config's
    ``harness_session_vars`` key -- a list of ``[tool_tag, env_var]``
    pairs.  Malformed entries are skipped.  This is how an adopter on a
    new harness registers its session env var **without editing this
    file** (the portability contract).
    """
    extras: List[Tuple[str, str]] = []
    if config is not None:
        raw = config.get("harness_session_vars")
        if isinstance(raw, list):
            for entry in raw:
                if (
                    isinstance(entry, (list, tuple))
                    and len(entry) == 2
                    and isinstance(entry[0], str)
                    and isinstance(entry[1], str)
                    and entry[0].strip()
                    and entry[1].strip()
                ):
                    extras.append((entry[0].strip(), entry[1].strip()))
    return HARNESS_SESSION_VARS + tuple(extras)


def resolve_agent_identity(
    *,
    env_var: str = AGENT_ENV_VAR,
    config_path: Optional[Path] = None,
) -> Optional[str]:
    """Resolve the current agent identity.

    Resolution order:

    1. ``$CAIRN_AGENT`` (overrideable via ``env_var=``) -- explicit
       escape hatch.
    2. Harness session-derived identity from the **effective** registry
       (built-in + the JSON config's ``harness_session_vars`` adopter
       extensions): the first matching env var yields
       ``<tool_tag>-<8 hex of sha256(session_id)>``.
    3. The JSON config's top-level ``agent`` key (static identity).
    4. ``None``.

    Fail-soft: any resolution failure returns ``None``; the caller
    decides whether to fall back, warn, or skip.
    """
    env_val = os.environ.get(env_var)
    if env_val and env_val.strip():
        return env_val.strip()
    config = _load_config(config_path)
    for tool_tag, session_var in effective_harness_vars(config):
        derived = _session_identity(tool_tag, os.environ.get(session_var))
        if derived is not None:
            return derived
    if config is not None:
        agent = config.get("agent")
        if isinstance(agent, str) and agent.strip():
            return agent.strip()
    return None


def resolve_session_token(
    *, config_path: Optional[Path] = None,
) -> Optional[str]:
    """Resolve the bare per-session token -- the :func:`_session_digest`
    hash of the harness session id -- or ``None`` when no harness session
    var is exposed.

    This is the **token portion** of a harness-derived agent identity
    (``<tool_tag>-<token>``); :func:`resolve_agent_identity` returns the
    full identity.  Exposing the token lets a per-session surface *outside*
    the intent log reuse the same session identity: a reflections filename
    whose ``<agent>-<session>`` tail is ``<tool_tag>-<token>`` reconstructs
    the intent log's ``agent`` field exactly, so the two surfaces link.

    Resolves **only** the harness-session tier -- deliberately *not*
    ``$CAIRN_AGENT`` or the static config ``agent``.  Neither of those is
    per-session (both yield one identity shared across concurrent sessions,
    the very collision a per-session token exists to avoid), so neither
    can supply a collision-safe token; the caller falls back to a random
    token instead.
    """
    config = _load_config(config_path)
    for _tool_tag, session_var in effective_harness_vars(config):
        digest = _session_digest(os.environ.get(session_var))
        if digest is not None:
            return digest
    return None


# ---------------------------------------------------------------------------
# Conflict-warning formatting (the live signaler value)


def _format_conflict_warning(
    just_claimed: ClaimRecord,
    overlap: List[Dict[str, object]],
) -> str:
    """Build the conflict-warning string for the signaler.

    The warning fires when a fresh claim overlaps active claims from
    other agents (or other sessions of the same agent), giving the
    signaler immediate, actionable value at the moment of signaling.
    """
    if not overlap:
        return ""
    if len(overlap) == 1:
        header = (
            "intent: CONFLICT CHECK: 1 active claim overlaps your file set:"
        )
    else:
        header = (
            f"intent: CONFLICT CHECK: {len(overlap)} active claims overlap "
            f"your file set:"
        )
    lines = [
        f"intent: claim recorded (id: {just_claimed.id}).",
        header,
    ]
    just_claimed_set = set(just_claimed.files)
    for active in overlap:
        active_files = active.get("files") or []
        if not isinstance(active_files, list):
            active_files = []
        overlapping = [f for f in active_files if f in just_claimed_set]
        non_overlapping = [
            f for f in active_files if f not in just_claimed_set
        ]
        files_summary_parts: List[str] = []
        for f in overlapping:
            files_summary_parts.append(f"{f} (overlap)")
        files_summary_parts.extend(non_overlapping)
        files_summary = ", ".join(files_summary_parts) or "(none)"
        action = active.get("action") or ""
        lines.append(
            f"  - id: {active.get('id')}\n"
            f"    agent: {active.get('agent')}\n"
            f"    files: {files_summary}\n"
            f"    action: {action!r}"
        )
    lines.append("")
    lines.append(
        "Consider coordinating with the active claimants or waiting; their "
        "claims cover files you also need to edit."
    )
    return "\n".join(lines) + "\n"


def split_file_tokens(files: Sequence[str]) -> List[str]:
    """Flatten comma-separated ``--files`` / ``--conflicts-with`` tokens
    into individual paths.

    Both CLI options use ``nargs='+'`` (space-separated), but a single
    comma-joined string (``--files "a,b,c"``) is common.  Splitting on
    commas (dropping empties / whitespace) makes space-separated,
    comma-separated, and mixed forms all yield a flat path list.
    Idempotent on already-split input.
    """
    out: List[str] = []
    for token in files:
        for part in str(token).split(","):
            part = part.strip()
            if part:
                out.append(part)
    return out


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


def _git_path(*args: str) -> Optional[str]:
    """Run ``git <args>`` and return stripped stdout, or ``None`` on
    failure (git absent / not a checkout)."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


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


def _git_toplevel() -> Optional[Path]:
    """Return the git working-tree root, or ``None`` outside a tree."""
    top = _git_path("rev-parse", "--show-toplevel")
    return Path(top) if top else None


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


def _read_solo_mode(repo_root: Path) -> bool:
    """Read the tracked solo-mode flag from ``dev/intent-config.json``.

    Returns ``True`` only when the file exists, parses as a JSON object,
    and carries ``"solo_mode": true``.  Absent / malformed / false all
    return ``False`` (warn).  A deterministic exemption -- no semantic
    auto-exemption.
    """
    cfg = repo_root / INTENT_CONFIG_RELPATH
    if not cfg.exists():
        return False
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return isinstance(data, dict) and data.get("solo_mode") is True


#: Enforce modes for the pre-commit coordination check (concurrent-session
#: coordination Layer 2 / #53). ``warn`` = surface, exit 0 (never blocks);
#: ``confirm`` = prompt, proceed on acknowledgement, degrade to ``block`` with
#: no TTY (R2); ``block`` = refuse (non-zero exit) a commit touching a
#: *different* active session's claimed path. **The shipped default (absent /
#: malformed / unrecognized config) is ``block``** -- warn-on-unclaimed +
#: block-on-cross-claim (foldback-drain Fold A / R2). An adopter opts back
#: into never-block with an explicit ``"enforce": "warn"``.
ENFORCE_MODES = ("warn", "confirm", "block")


def _read_enforce_mode(repo_root: Path) -> str:
    """Read ``"enforce"`` from ``dev/intent-config.json`` -- ``warn`` /
    ``confirm`` / ``block``. **Absent / malformed / unrecognized → ``block``**
    -- the shipped default: warn-on-unclaimed + block-on-cross-claim
    (foldback-drain Fold A / R2). An adopter opts back into never-block with an
    explicit ``"enforce": "warn"``. Parallel to :func:`_read_solo_mode`.

    Note: ``block`` is the *enforce-mode* default; it only refuses a commit
    when a **different live session** holds a **fresh** (within-TTL) claim on a
    staged path *and* the committer has a per-session token (see
    :func:`_precommit_check_impl`). An unclaimed staged path still only warns."""
    cfg = repo_root / INTENT_CONFIG_RELPATH
    if not cfg.exists():
        return "block"
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "block"
    if not isinstance(data, dict):
        return "block"
    mode = data.get("enforce")
    return mode if mode in ENFORCE_MODES else "block"


def _read_claim_ttl_hours(repo_root: Path) -> float:
    """Read ``"claim_ttl_hours"`` from ``dev/intent-config.json``.

    Returns the configured positive float, or :data:`DEFAULT_CLAIM_TTL_HOURS`
    (4.0) when absent / malformed / non-numeric / non-positive. **Fail-safe:**
    any read or parse error degrades to the default rather than raising -- this
    feeds the pre-commit hook, which must never crash (R1)."""
    cfg = repo_root / INTENT_CONFIG_RELPATH
    if not cfg.exists():
        return DEFAULT_CLAIM_TTL_HOURS
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return DEFAULT_CLAIM_TTL_HOURS
    if not isinstance(data, dict):
        return DEFAULT_CLAIM_TTL_HOURS
    raw = data.get("claim_ttl_hours")
    if raw is None:
        return DEFAULT_CLAIM_TTL_HOURS
    try:
        ttl = float(raw)
    except (TypeError, ValueError):
        return DEFAULT_CLAIM_TTL_HOURS
    if ttl <= 0:
        return DEFAULT_CLAIM_TTL_HOURS
    return ttl


def _claim_is_stale(
    claim: Dict[str, object],
    ttl_hours: float,
    *,
    now: Optional[datetime.datetime] = None,
) -> bool:
    """True when *claim*'s timestamp is older than *ttl_hours*.

    **N3 (BINDING -- a real pre-commit crash class).** Claims stamp an
    **offset-aware** ISO timestamp (``datetime.now().astimezone()``,
    :func:`write_claim`). This parses ``ts`` offset-aware
    (``datetime.fromisoformat``) and compares against an offset-aware *now*, so
    the subtraction never raises the ``TypeError`` an aware/naive mismatch
    would -- the failure mode that would otherwise wedge the git pre-commit
    hook. **Fail-safe:** any missing / non-string / unparseable /
    non-comparable ``ts`` returns ``True`` (treat as stale → excluded from the
    block decision, i.e. *do not block*) and NEVER raises -- a degraded
    timestamp must not wedge the commit (composes with the hook's never-wedge
    invariant, R1). A naive ``ts`` (no offset -- only from a hand-edited or
    foreign-writer log) is localized via ``astimezone()`` so the compare stays
    offset-aware-safe."""
    if now is None:
        now = datetime.datetime.now().astimezone()
    ts_raw = claim.get("ts")
    if not isinstance(ts_raw, str):
        return True
    try:
        claimed = datetime.datetime.fromisoformat(ts_raw)
        if claimed.tzinfo is None:
            # Naive ts: localize so the subtraction is aware-minus-aware.
            claimed = claimed.astimezone()
        return (now - claimed) > datetime.timedelta(hours=ttl_hours)
    except (ValueError, TypeError, OverflowError, OSError):
        # Fail-safe: an unparseable ts must not block (and must not crash).
        return True


def _drop_stale_claims(
    claims: List[Dict[str, object]],
    ttl_hours: float,
    *,
    now: Optional[datetime.datetime] = None,
) -> List[Dict[str, object]]:
    """The subset of *claims* still within *ttl_hours* (fresh enough to block).

    Stale claims are dropped from the **enforcement** set only -- they still
    surface as warnings (the warning path reads the full active set, so a stale
    cross-claim is *seen* but does not *block*). A non-positive *ttl_hours* is
    normalized to the default by :func:`_read_claim_ttl_hours`, so the filter
    always applies a real window."""
    if now is None:
        now = datetime.datetime.now().astimezone()
    return [
        claim for claim in claims
        if not _claim_is_stale(claim, ttl_hours, now=now)
    ]


# ---------------------------------------------------------------------------
# Sensing write-path -- record a work-intent collision as an incident row
# (self-evolution-loop Part B). Everything here is **best-effort & fail-safe**:
# a failure NEVER blocks, slows, or fails the commit (R1); the tool only ever
# *appends a markdown row* -- never a ``git reset`` / index mutation (N4).


def _read_incident_config(repo_root: Path) -> Tuple[str, str]:
    """``(incident_log_path, event_class)`` from ``dev/intent-config.json``.

    Fail-safe: absent / malformed / non-string values fall back to
    :data:`INCIDENT_LOG_RELPATH_DEFAULT` / :data:`INCIDENT_EVENT_CLASS_DEFAULT`.
    """
    log_path = INCIDENT_LOG_RELPATH_DEFAULT
    event_class = INCIDENT_EVENT_CLASS_DEFAULT
    cfg = repo_root / INTENT_CONFIG_RELPATH
    try:
        if cfg.exists():
            data = json.loads(cfg.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                lp = data.get("incident_log_path")
                ec = data.get("incident_event_class")
                if isinstance(lp, str) and lp.strip():
                    log_path = lp.strip()
                if isinstance(ec, str) and ec.strip():
                    event_class = ec.strip()
    except (OSError, ValueError):
        pass
    return log_path, event_class


def _describe_collision(other: Dict[str, List[Dict[str, object]]]) -> str:
    """A one-line, pipe-safe description of an other-session overlap."""
    paths = sorted(other.keys())
    agents = sorted({
        str(c.get("agent", "?"))
        for claims in other.values() for c in claims
    })
    return (
        f"work-intent collision: staged path(s) {', '.join(paths[:5])} "
        f"held by another session ({', '.join(agents[:5])})"
    )


def _incident_tracker_skeleton(event_class: str) -> str:
    """A minimal but machine-evaluable incident tracker (created when the
    configured log is absent -- the 'closed' failure mode: create the log,
    do not silently drop the incident)."""
    return (
        "# Coordination incident log (auto-created by the work-intent hook)\n\n"
        "**Rolling window**: 14 days.\n\n"
        "## What counts\n\n"
        f"* **Class name** -- `{event_class}` (auto-recorded by the "
        "work-intent pre-commit hook).\n"
        "* **Criteria for \"same shape\" recurrence** -- <define>; until you "
        "do, the rate-limit gate counts by event-class match within the "
        "rolling window.\n"
        "* **What does NOT count** -- `Impact = prevented` / `non-conflict` "
        "rows (base-rate visibility only).\n\n"
        "## Incidents\n\n"
        "| Date | Event Class | Description | Recurrence-Window Match "
        "| Impact | Migrated From Reflection | Resolved By |\n"
        "|------|-------------|-------------|------------------------"
        "|--------|-------------------------|-------------|\n"
    )


def _insert_incident_row(path: Path, row: str) -> None:
    """Insert *row* after the last data row of the ``## Incidents`` markdown
    table, atomically (write a temp file + ``os.replace``). Falls back to an
    EOF append if the table cannot be located -- the row is never dropped."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    insert_at: Optional[int] = None
    in_incidents = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## ") and stripped[3:].strip().lower().startswith(
            "incidents"
        ):
            in_incidents = True
            continue
        if in_incidents:
            if stripped.startswith("## "):
                break  # next section -- the table ended above
            if stripped.startswith("|"):
                insert_at = i + 1  # just after this table row
    if insert_at is None:
        new_text = text + ("" if text.endswith("\n") else "\n") + row
    else:
        new_text = "".join(lines[:insert_at]) + row + "".join(lines[insert_at:])
    tmp = path.with_name(path.name + ".intent-incident.tmp")
    tmp.write_text(new_text, encoding="utf-8")
    os.replace(tmp, path)


def _record_incident(
    repo_root: Path, *, impact: str, description: str,
) -> None:
    """Append one incident row to the configured tracker -- **best-effort,
    fail-safe, non-blocking** (R1). Creates a minimal tracker if absent
    ('closed': create, don't drop). On ANY error, writes a *visible* skip note
    to stderr (F4) and returns -- it never raises and never affects the
    commit's exit code. Only ever appends a row (N4)."""
    try:
        log_path, event_class = _read_incident_config(repo_root)
        today = datetime.datetime.now().astimezone().date().isoformat()
        desc = description.replace("|", r"\|").replace("\n", " ").strip()[:200]
        # ``direct`` = logged without passing through a reflection; ``pending``
        # = no resolution yet; ``auto`` = recurrence to be evaluated by the
        # inference tool, not computed in the fail-safe hot path.
        row = (
            f"| {today} | {event_class} | {desc} | auto | {impact} "
            "| direct | pending |\n"
        )
        path = repo_root / log_path
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(_incident_tracker_skeleton(event_class), encoding="utf-8")
        _insert_incident_row(path, row)
    except Exception as exc:  # noqa: BLE001 -- fail-safe; never wedge a commit
        sys.stderr.write(
            f"intent: could not record the coordination incident "
            f"({exc!r}); the commit is unaffected. Record it by hand if your "
            "team tracks recurrence.\n"
        )


def _precommit_shebang_is_shell(first_line: str) -> bool:
    """True when ``first_line`` is a shebang naming a POSIX shell.

    The pre-commit installer's narrow-composition guard: a hook whose
    shebang is not a shell (e.g. ``#!/usr/bin/env python``) is foreign
    and refused.  (Distinct from :func:`_first_shebang_is_shell`, which
    governs the post-commit *append* path and treats a missing shebang
    as shell.)
    """
    line = first_line.strip()
    if not line.startswith("#!"):
        return False
    return any(sh in line for sh in ("sh", "bash", "zsh", "dash"))


def _classify_existing_precommit(hook_file: Path) -> str:
    """Classify an existing ``pre-commit`` hook for install safety.

    Returns ``'absent'``, ``'sentinel'`` (carries our block -- safe to
    replace), ``'framework'`` (pre-commit.com / husky), ``'non-shell'``,
    ``'non-executable'``, or ``'foreign'``.  Only ``'absent'`` and
    ``'sentinel'`` are install targets; everything else is refused
    without mutation (narrow v1 composition).
    """
    if not hook_file.exists():
        return "absent"
    try:
        text = hook_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "foreign"
    if PRECOMMIT_SENTINEL_BEGIN in text:
        return "sentinel"
    framework_markers = (
        "generated by pre-commit",
        "pre-commit.com",
        "INSTALL_PYTHON",
        "husky.sh",
        "_/husky",
    )
    if any(marker in text for marker in framework_markers):
        return "framework"
    lines = text.splitlines()
    first = lines[0] if lines else ""
    if not _precommit_shebang_is_shell(first):
        return "non-shell"
    if not (hook_file.stat().st_mode & 0o111):
        return "non-executable"
    return "foreign"


def _precommit_hook_block(python_exe: str, intent_path: Path) -> str:
    """Build the sentinel-wrapped pre-commit hook block.

    The body writes the commit's staged set NUL-delimited to a temp file
    (``git diff --cached --name-only -z`` -- the **commit** surface, NOT
    ``git status`` / unstaged files) and hands it to ``_precommit_check``.
    Like the post-commit block, the interpreter + script paths are baked
    in via ``shlex.quote`` (no ``python -m`` PATH/package assumption, no
    shell expansion of a metacharacter-bearing path).  The check's exit code
    **propagates** (no ``|| true``) so the ``confirm`` / ``block`` enforce
    modes can refuse the commit; the check is fail-open by construction (an
    internal error returns 0). The shipped default is now ``block``-on-
    cross-claim (foldback-drain Fold A), so a forgotten claim on a path a
    *different live session* holds is refused; ``warn`` mode (opt-in), an
    exempt/no-token committer, and any clean (0) result exit 0 and fall
    through to any composed later hook content. The temp file is removed
    before the exit code is honored.
    """
    py_q = shlex.quote(python_exe)
    path_q = shlex.quote(str(intent_path))
    body = (
        # Portable mktemp template path (BSD/macOS + GNU identical),
        # matching the post-commit installer.
        'PATHS_TMP=$(mktemp "${TMPDIR:-/tmp}/intent-staged.XXXXXX")\n'
        'git diff --cached --name-only -z > "${PATHS_TMP}"\n'
        f'{py_q} {path_q} _precommit_check '
        '--paths-from-file "${PATHS_TMP}"\n'
        'INTENT_RC=$?\n'
        'rm -f "${PATHS_TMP}"\n'
        '[ "${INTENT_RC}" -eq 0 ] || exit "${INTENT_RC}"'
    )
    return f"{PRECOMMIT_SENTINEL_BEGIN}\n{body}\n{PRECOMMIT_SENTINEL_END}"


def _strip_precommit_block(text: str) -> str:
    """Return ``text`` with the pre-commit sentinel block removed
    (inclusive of the BEGIN/END marker lines)."""
    out: List[str] = []
    skip = False
    for line in text.splitlines():
        if line.strip() == PRECOMMIT_SENTINEL_BEGIN:
            skip = True
            continue
        if line.strip() == PRECOMMIT_SENTINEL_END:
            skip = False
            continue
        if not skip:
            out.append(line)
    return "\n".join(out)


def _unclaimed_warning(paths: Sequence[str]) -> str:
    """Self-directed warning: staged path(s) with no active claim."""
    lines = [
        "intent: PRE-COMMIT CHECK -- staged path(s) with no active claim:"
    ]
    lines.extend(f"  - {p}" for p in paths)
    lines.append(
        f"Consider `{INVOKE_HINT} claim --files <path> --action <summary>` "
        "before editing,"
    )
    lines.append(
        f"or set {ALLOW_UNCLAIMED_ENV_VAR}=1 for an intentional unclaimed "
        f'commit (or "solo_mode": true in {INTENT_CONFIG_RELPATH}).'
    )
    return "\n".join(lines) + "\n"


def _other_session_warning(
    overlaps: Dict[str, List[Dict[str, object]]],
) -> str:
    """Coordination warning: staged path(s) held by another active
    claim.  ALWAYS surfaced -- never suppressed by an exemption."""
    lines = [
        "intent: PRE-COMMIT CHECK -- staged path(s) HELD BY ANOTHER "
        "active claim:"
    ]
    for path in sorted(overlaps):
        for claim in overlaps[path]:
            lines.append(
                f"  - {path}  (claim {claim.get('id')!r} by "
                f"{claim.get('agent')!r}: {claim.get('action')!r})"
            )
    lines.append(
        "Another session has an active claim covering these paths; "
        "coordinate before committing."
    )
    return "\n".join(lines) + "\n"


def _unknown_identity_warning() -> str:
    """Self-directed warning: this session's agent identity is
    unresolvable, so a same-session claim cannot be proven."""
    return (
        "intent: PRE-COMMIT CHECK -- UNKNOWN IDENTITY: cannot resolve "
        "this session's agent identity\n"
        f"  ({AGENT_ENV_VAR} unset, no harness session var, and "
        "~/.cairn/agent.json missing or unreadable).\n"
        "  Cannot verify whether you hold claims on the staged paths; "
        "any active-claim overlaps are shown below.\n"
    )


def _compute_overlaps(
    staged_set: set,
    actives: List[Dict[str, object]],
    repo_root: Optional[Path],
    rename_map: Optional[Dict[str, str]],
) -> Dict[str, List[Dict[str, object]]]:
    """Map each staged path to the active claims covering it (rename-aware:
    a staged destination is covered when a claim covers the destination OR
    its rename source -- a `git mv` of a claimed file is the claimed edit)."""
    overlaps: Dict[str, List[Dict[str, object]]] = {}
    renames = rename_map or {}
    for claim in actives:
        claim_files = claim.get("files") or []
        if not isinstance(claim_files, list):
            continue
        claim_set = {
            normalize_path(str(f), repo_root=repo_root) for f in claim_files
        }
        for path in staged_set:
            source = renames.get(path)
            if path in claim_set or (source is not None and source in claim_set):
                overlaps.setdefault(path, []).append(claim)
    return overlaps


def other_session_overlaps(
    overlaps: Dict[str, List[Dict[str, object]]],
    identity: Optional[str],
    token_resolved: bool,
) -> Dict[str, List[Dict[str, object]]]:
    """The subset of *overlaps* held by a **different active session**.

    **N1 (the cry-wolf / false-suppress fix):** own-claim suppression runs
    **only** when the committer has a resolvable per-session token
    (*token_resolved*) AND a known identity. Without a token, the identity is
    the bare agent name (shared by every concurrent same-type session), so
    matching on it would *false-suppress* a genuinely different session's
    claim -- a silent coordination miss. In that case every overlap is treated
    as other-session (fail-safe: over-warn, never silently drop)."""
    own_match = (
        token_resolved and bool(identity) and identity != "unknown-agent"
    )
    if not own_match:
        return dict(overlaps)
    out: Dict[str, List[Dict[str, object]]] = {}
    for path, claims in overlaps.items():
        others = [c for c in claims if c.get("agent") != identity]
        if others:
            out[path] = others
    return out


def classify_precommit_warnings(
    staged_set: set,
    actives: List[Dict[str, object]],
    identity: Optional[str],
    *,
    exempt: bool,
    repo_root: Optional[Path] = None,
    rename_map: Optional[Dict[str, str]] = None,
    token_resolved: bool = True,
) -> List[str]:
    """Classify a commit's staged set into ordered warning strings.

    Warning precedence:

    * **Other-session overlap** -- a staged path covered by a *different*
      active session's claim. ALWAYS surfaced -- never suppressed by
      ``exempt``. This is the coordination payoff. Own vs other is gated on
      ``token_resolved`` (N1): no per-session token → every overlap is
      other-session (own cannot be proven without a token).
    * **Unclaimed** -- identity known, staged path covered by no claim at
      all.  Suppressed when ``exempt``.
    * **Unknown identity** -- identity unresolved.  Emits the loud
      unknown-identity warning **plus** any visible overlaps (suppressed
      identity line when ``exempt``).
    """
    identity_known = bool(identity) and identity != "unknown-agent"
    overlaps = _compute_overlaps(staged_set, actives, repo_root, rename_map)

    warnings: List[str] = []
    if not identity_known:
        if not exempt:
            warnings.append(_unknown_identity_warning())
        if overlaps:
            warnings.append(_other_session_warning(overlaps))
        return warnings

    other_overlaps = other_session_overlaps(overlaps, identity, token_resolved)
    if other_overlaps:
        warnings.append(_other_session_warning(other_overlaps))
    # Unclaimed = staged paths covered by no claim at all.
    unclaimed = sorted(p for p in staged_set if p not in overlaps)
    if unclaimed and not exempt:
        warnings.append(_unclaimed_warning(unclaimed))
    return warnings


def _staged_paths_via_git(repo_root: Path) -> List[str]:
    """Fallback path discovery: read the commit's staged set directly via
    ``git diff --cached --name-only -z`` (used when the hook did not pass
    ``--paths-from-file``).  The commit surface, not ``git status``."""
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "-z"],
            cwd=str(repo_root), capture_output=True, check=False,
        )
    except OSError:
        return []
    if out.returncode != 0 or not out.stdout:
        return []
    parts = out.stdout.split(b"\x00")
    if parts and parts[-1] == b"":
        parts = parts[:-1]
    return [b.decode("utf-8", errors="replace") for b in parts]


def _rename_map_via_git(repo_root: Path) -> Dict[str, str]:
    """Return ``{normalized_destination: normalized_source}`` for staged
    renames (``git diff --cached --name-status -M -z``).

    Lets the pre-commit check credit a claim on a rename's *source* to its
    staged *destination*, so a ``git mv`` of a claimed file is not flagged
    unclaimed (the claim sits on the source). ``-M`` detects renames (not
    ``-C`` copies). Both sides are normalized with the same
    ``normalize_path`` the claim/staged sets use, so they match. Empty on
    any git error -- rename-awareness degrades to the prior behavior."""
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-status", "-M", "-z"],
            cwd=str(repo_root), capture_output=True, check=False,
        )
    except OSError:
        return {}
    if out.returncode != 0 or not out.stdout:
        return {}
    tokens = out.stdout.split(b"\x00")
    if tokens and tokens[-1] == b"":
        tokens = tokens[:-1]
    rename_map: Dict[str, str] = {}
    i = 0
    while i < len(tokens):
        status = tokens[i].decode("utf-8", errors="replace")
        if status[:1] == "R":
            # name-status -z renames: ``R<score>\0<source>\0<dest>``.
            if i + 2 < len(tokens):
                source = tokens[i + 1].decode("utf-8", errors="replace")
                dest = tokens[i + 2].decode("utf-8", errors="replace")
                rename_map[normalize_path(dest, repo_root=repo_root)] = (
                    normalize_path(source, repo_root=repo_root)
                )
            i += 3
        else:
            # ``<status>\0<path>`` for A / M / D / T.
            i += 2
    return rename_map


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


def _confirm_tty():
    """An open ``r+`` handle to the controlling terminal, or ``None``.

    ``confirm`` mode prompts here -- not via ``sys.stdin``, which a git hook
    redirects to ``/dev/null``. No controlling terminal (a headless / CI
    agent) → ``None`` → ``confirm`` degrades to ``block`` (R2). Factored for
    test injection."""
    try:
        return open("/dev/tty", "r+")  # noqa: SIM115
    except OSError:
        return None


def _confirm_proceed() -> bool:
    """Prompt the controlling terminal for explicit acknowledgement.
    No TTY → ``False`` (caller degrades to ``block``, R2)."""
    tty = _confirm_tty()
    if tty is None:
        return False
    try:
        tty.write(
            "intent: a DIFFERENT active session claims a staged path. "
            "Proceed with this commit? [y/N] "
        )
        tty.flush()
        ans = (tty.readline() or "").strip().lower()
    except OSError:
        return False
    finally:
        try:
            tty.close()
        except OSError:
            pass
    return ans in ("y", "yes")


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


def _precommit_check_impl(args) -> int:
    log_path = (
        Path(args.log_path) if args.log_path is not None else INTENTS_LOG_PATH
    )
    top = _git_toplevel() or _REPO_ROOT
    if args.paths_from_file:
        staged = _read_nul_delimited_paths(args.paths_from_file)
    else:
        staged = _staged_paths_via_git(top)
    if not staged:
        return 0
    staged_set = {normalize_path(p, repo_root=top) for p in staged}
    # Self-derive the rename map regardless of how the staged set arrived
    # (hook --paths-from-file or the fallback) -- the hook body stays
    # --name-only, so the rename info comes from this dedicated call.
    rename_map = _rename_map_via_git(top)
    identity = resolve_agent_identity()
    # N1: own-claim suppression requires a real per-session token, not the
    # static agent-name fallback (which collides across same-type sessions).
    token_resolved = resolve_session_token() is not None
    exempt = bool(
        (os.environ.get(ALLOW_UNCLAIMED_ENV_VAR) or "").strip()
    ) or _read_solo_mode(top)
    actives = active_intents(log_path=log_path)
    for warning in classify_precommit_warnings(
        staged_set, actives, identity, exempt=exempt, repo_root=top,
        rename_map=rename_map, token_resolved=token_resolved,
    ):
        sys.stderr.write(warning)

    # Enforce decision (Layer 2 / #53). Only a *different live session's*
    # fresh (within-TTL) claim can block; warn-mode and any bypass always
    # proceed. The shipped default is now ``block`` (foldback-drain Fold A).
    mode = _read_enforce_mode(top)
    if mode == "warn" or exempt:
        return 0
    # Stale-claim safety (R1 / N3): a claim past the TTL still WARNS (above)
    # but cannot block -- a crashed / abandoned session must not wedge a live
    # committer. The TTL parse/compare is fail-safe (never crashes the hook).
    ttl_hours = _read_claim_ttl_hours(top)
    fresh_actives = _drop_stale_claims(actives, ttl_hours)
    overlaps = _compute_overlaps(staged_set, fresh_actives, top, rename_map)
    other = other_session_overlaps(overlaps, identity, token_resolved)
    if not other:
        return 0  # no different-session live claim -> nothing to enforce
    # A no-token committer cannot establish "a *different* live session" (N1:
    # a static identity is shared across same-type sessions, so ownership of an
    # overlapping claim cannot be proven). We do NOT escalate an
    # unprovable-ownership overlap to a block -- the warning already surfaced
    # above (R2 keys the block on a different *live session*; blocking a
    # possibly-own claim is the misfire the proposal's risk section names). But
    # we emit a one-line note so a no-token team sees enforcement was
    # *downgraded*, not that nothing was held -- the proposal's "warn-only with
    # a louder signal" fallback. The real cure (worktree isolation) is in the
    # commit-hygiene doctrine note.
    if not token_resolved:
        sys.stderr.write(
            "intent: cross-claim block WITHHELD -- no per-session token, so "
            "ownership of the overlapping claim cannot be proven (a static "
            "identity is shared across same-type sessions). The overlap is "
            "warned above but not enforced; provide a session token, or use "
            "per-agent worktree isolation (the durable cure).\n"
        )
        # No-token ownership is unprovable -> not classifiable as a different
        # session's collision, so we record NO incident (tagging it would
        # over-count the rate-limit gate -- the named mis-tag failure).
        return 0
    # A provably-different live session's fresh claim overlaps a staged path
    # (S4: the incident's Impact bakes in the enforce decision under P4's
    # block-default). The recording is best-effort & fail-safe (R1) -- it never
    # changes the return value below.
    incident_desc = _describe_collision(other)
    if mode == "block":
        sys.stderr.write(
            "intent: enforce=block -- refusing this commit (a different "
            f"active session claims a staged path). Override: set "
            f"{ALLOW_UNCLAIMED_ENV_VAR}=1 to commit anyway.\n"
        )
        # Blocked -> the collision was *prevented* by the structural gate.
        _record_incident(top, impact="prevented", description=incident_desc)
        return 1
    # confirm: proceed only on explicit acknowledgement; no TTY -> block (R2).
    if _confirm_proceed():
        # Proceeded past a confirmed different-session claim -> *occurred*
        # (a knowing override; the signal the rate-limit gate counts).
        _record_incident(top, impact="occurred", description=incident_desc)
        return 0
    sys.stderr.write(
        "intent: enforce=confirm -- not acknowledged (or no TTY); refusing "
        f"(degraded to block). Override: set {ALLOW_UNCLAIMED_ENV_VAR}=1.\n"
    )
    # Degraded to block -> *prevented*.
    _record_incident(top, impact="prevented", description=incident_desc)
    return 1


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
