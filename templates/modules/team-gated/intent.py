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
* per-session agent-identity resolution, and
* a **folded-in** ``install-hook`` that writes a post-commit
  auto-release hook (no separate shell installer to ship).

It is **stdlib-only** (``argparse``, ``dataclasses``, ``datetime``,
``hashlib``, ``json``, ``os``, ``subprocess``, ``sys``, ``pathlib``,
``typing``) and **Python 3.8-safe**, matching Cairn's bootstrap floor.

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

#: Repo root: this file installs to ``<repo>/tools/intent.py``, so the
#: repo root is one directory above ``tools/``.
_REPO_ROOT = Path(__file__).resolve().parents[1]

#: Default location of the active intent log (gitignored).
INTENTS_LOG_PATH = _REPO_ROOT / "dev" / "intents.jsonl"

#: Conservative per-record size cap.  Records at or below this size stay
#: inside the small-write window local filesystems respect for
#: non-interleaved concurrent appends; larger records are rejected with
#: a precise diagnostic.
RECORD_SIZE_CAP = 512

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


def _session_identity(
    tool_tag: str, raw_session_id: Optional[str],
) -> Optional[str]:
    """Form a bounded, per-session agent identity from a raw session id.

    Returns ``None`` when ``raw_session_id`` is missing / empty /
    whitespace-only, so the caller falls through to the next resolution
    tier.

    Otherwise returns ``<tool_tag>-<8 hex of sha256(raw_session_id)>``.
    The id is **hashed in full**, never prefix-sliced: harness session
    ids may be time-ordered (e.g. UUIDv7, whose leading bytes are a
    timestamp shared by near-simultaneous sessions), so a prefix would
    collapse exactly the concurrent same-tool sessions this identity
    model exists to separate.  Hashing the whole id is harness-neutral
    and keeps the written identity string safe + bounded regardless of
    the raw id's shape.
    """
    if not raw_session_id or not raw_session_id.strip():
        return None
    digest = hashlib.sha256(
        raw_session_id.strip().encode("utf-8"),
    ).hexdigest()[:8]
    return f"{tool_tag}-{digest}"


# ---------------------------------------------------------------------------
# Record schemas


@dataclasses.dataclass(frozen=True)
class ClaimRecord:
    """A ``claim`` event in the intent log."""

    id: str
    ts: str
    agent: str
    files: List[str]
    action: str
    stem: Optional[str] = None
    event: str = "claim"

    def to_dict(self) -> Dict[str, object]:
        d: Dict[str, object] = {
            "event": self.event,
            "id": self.id,
            "ts": self.ts,
            "agent": self.agent,
            "files": list(self.files),
            "action": self.action,
        }
        if self.stem is not None:
            d["stem"] = self.stem
        return d


@dataclasses.dataclass(frozen=True)
class ReleaseRecord:
    """A ``release`` event in the intent log."""

    id: str
    ts: str
    commit: Optional[str] = None
    event: str = "release"

    def to_dict(self) -> Dict[str, object]:
        d: Dict[str, object] = {
            "event": self.event,
            "id": self.id,
            "ts": self.ts,
        }
        if self.commit is not None:
            d["commit"] = self.commit
        return d


# ---------------------------------------------------------------------------
# Path normalization


def normalize_path(path: str, *, repo_root: Optional[Path] = None) -> str:
    """Normalize ``path`` to repo-root-relative, forward-slash, no
    leading ``./`` or trailing slashes.

    Absolute paths inside the repo are rewritten repo-root-relative;
    paths outside are preserved as absolute (POSIX-style).  Forward
    slashes on every platform; leading ``./`` and trailing ``/``
    stripped; backslashes converted.
    """
    if not path:
        return ""
    root = repo_root if repo_root is not None else _REPO_ROOT
    cleaned = path.replace("\\", "/").strip()
    while cleaned.startswith("./"):
        cleaned = cleaned[2:]
    cleaned = cleaned.rstrip("/")
    if not cleaned:
        return ""
    abs_candidate = Path(cleaned)
    if abs_candidate.is_absolute():
        try:
            rel = abs_candidate.resolve().relative_to(root.resolve())
        except ValueError:
            return PurePosixPath(abs_candidate).as_posix()
        return PurePosixPath(rel).as_posix()
    return PurePosixPath(cleaned).as_posix()


# ---------------------------------------------------------------------------
# Record serialization + atomic append


def _record_bytes(record_dict: Dict[str, object]) -> bytes:
    """Serialize a record dict to a single JSON line + ``\\n``, UTF-8.

    Raises ``ValueError`` when the encoded record meets or exceeds
    :data:`RECORD_SIZE_CAP`, with a diagnostic naming the cap, the
    actual size, and a remediation.
    """
    line = json.dumps(record_dict, separators=(",", ":"), ensure_ascii=False)
    payload = (line + "\n").encode("utf-8")
    if len(payload) >= RECORD_SIZE_CAP:
        files = record_dict.get("files") or []
        files_bytes = len(json.dumps(files).encode("utf-8"))
        action = record_dict.get("action") or ""
        action_bytes = len(json.dumps(action).encode("utf-8"))
        dominant = "paths" if files_bytes >= action_bytes else "action"
        raise ValueError(
            f"intent record is {len(payload)} bytes; cap is "
            f"{RECORD_SIZE_CAP} bytes. Dominant contributor: "
            f"{dominant} ({files_bytes} bytes paths / "
            f"{action_bytes} bytes action). Consider a shorter --action "
            f"and/or passing --stem <topic> to substitute a short topic "
            f"key for verbose action text."
        )
    return payload


def append_record(
    record_dict: Dict[str, object],
    *,
    log_path: Optional[Path] = None,
) -> None:
    """Append one record to the active intent log (best-effort atomic).

    Uses ``os.open(O_WRONLY | O_APPEND | O_CREAT)`` + a single
    ``os.write`` of a < cap payload, no buffered-writer layer.  Raises
    ``ValueError`` for over-cap records; raises ``IOError`` on the
    should-never-happen partial-write case so the failure surfaces
    loudly.
    """
    target = log_path if log_path is not None else INTENTS_LOG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = _record_bytes(record_dict)
    fd = os.open(str(target), os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        written = os.write(fd, payload)
        if written != len(payload):
            raise IOError(
                f"partial write to {target}: wrote {written} of "
                f"{len(payload)} bytes (atomicity contract broken; "
                f"investigate filesystem / platform interaction)"
            )
    finally:
        os.close(fd)


# ---------------------------------------------------------------------------
# Id generation


def generate_id(agent: str, ts: datetime.datetime) -> str:
    """Build a claim id: ``<agent>-<YYYYMMDD>T<HHMMSS>-<microsecond>``.

    The microsecond suffix guarantees per-call uniqueness within one
    agent's same-second issuances.
    """
    safe_agent = agent.replace("/", "-").replace(" ", "-").lower()
    return (
        f"{safe_agent}-{ts.strftime('%Y%m%dT%H%M%S')}-"
        f"{ts.microsecond:06d}"
    )


# ---------------------------------------------------------------------------
# High-level write helpers


def write_claim(
    *,
    agent: str,
    files: Sequence[str],
    action: str,
    stem: Optional[str] = None,
    ts: Optional[datetime.datetime] = None,
    log_path: Optional[Path] = None,
    repo_root: Optional[Path] = None,
) -> ClaimRecord:
    """Append a claim record; return the :class:`ClaimRecord`."""
    if ts is None:
        ts = datetime.datetime.now().astimezone()
    normalized_files = [normalize_path(p, repo_root=repo_root) for p in files]
    claim_id = generate_id(agent, ts)
    record = ClaimRecord(
        id=claim_id,
        ts=ts.isoformat(),
        agent=agent,
        files=normalized_files,
        action=action,
        stem=stem,
    )
    append_record(record.to_dict(), log_path=log_path)
    return record


def write_release(
    *,
    claim_id: str,
    ts: Optional[datetime.datetime] = None,
    commit: Optional[str] = None,
    log_path: Optional[Path] = None,
) -> ReleaseRecord:
    """Append a release record; return the :class:`ReleaseRecord`."""
    if ts is None:
        ts = datetime.datetime.now().astimezone()
    record = ReleaseRecord(id=claim_id, ts=ts.isoformat(), commit=commit)
    append_record(record.to_dict(), log_path=log_path)
    return record


# ---------------------------------------------------------------------------
# Read-side helpers


def read_log(log_path: Optional[Path] = None) -> List[Dict[str, object]]:
    """Read every record; skip malformed lines with a stderr warning."""
    target = log_path if log_path is not None else INTENTS_LOG_PATH
    if not target.exists():
        return []
    records: List[Dict[str, object]] = []
    with target.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                sys.stderr.write(
                    f"intent: skipping malformed line {line_no} in "
                    f"{target}: {exc}\n"
                )
                continue
    return records


def active_intents(log_path: Optional[Path] = None) -> List[Dict[str, object]]:
    """Return the claim records that lack a matching release (by id)."""
    records = read_log(log_path=log_path)
    released_ids = set()
    claims_by_id: Dict[str, Dict[str, object]] = {}
    for record in records:
        event = record.get("event")
        rid = record.get("id")
        if not isinstance(rid, str):
            continue
        if event == "release":
            released_ids.add(rid)
        elif event == "claim":
            claims_by_id[rid] = record
    return [
        claim for cid, claim in claims_by_id.items()
        if cid not in released_ids
    ]


def conflict_check(
    files: Sequence[str],
    *,
    log_path: Optional[Path] = None,
    repo_root: Optional[Path] = None,
) -> List[Dict[str, object]]:
    """Return active intents whose file set intersects ``files``."""
    query = {normalize_path(p, repo_root=repo_root) for p in files}
    if not query:
        return []
    hits: List[Dict[str, object]] = []
    for claim in active_intents(log_path=log_path):
        claim_files = claim.get("files") or []
        if not isinstance(claim_files, list):
            continue
        claim_set = {
            normalize_path(str(f), repo_root=repo_root) for f in claim_files
        }
        if claim_set & query:
            hits.append(claim)
    return hits


def iter_log(log_path: Optional[Path] = None) -> Iterator[Dict[str, object]]:
    """Yield records one at a time; same forgiveness as :func:`read_log`."""
    target = log_path if log_path is not None else INTENTS_LOG_PATH
    if not target.exists():
        return
    with target.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                yield json.loads(stripped)
            except json.JSONDecodeError as exc:
                sys.stderr.write(
                    f"intent: skipping malformed line {line_no} in "
                    f"{target}: {exc}\n"
                )
                continue


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
    intent_path = Path(__file__).resolve()
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


def _read_nul_delimited_paths(path: str) -> List[str]:
    """Read a NUL-delimited path file (``git diff-tree ... -z`` output)."""
    p = Path(path)
    if not p.exists():
        return []
    raw = p.read_bytes()
    if not raw:
        return []
    parts = raw.split(b"\x00")
    if parts and parts[-1] == b"":
        parts = parts[:-1]
    return [b.decode("utf-8", errors="replace") for b in parts]


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
# Argument parser


def _build_parser():
    import argparse

    parser = argparse.ArgumentParser(
        prog="intent",
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
