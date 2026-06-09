#!/usr/bin/env python3
"""Work-intent engine — conflict-check subsystem (intent-split phase A2).

Pre-commit conflict detection: claim-TTL / stale-claim policy, the
staged-path-vs-other-claim decision, incident-tracker recording, and the
warn/confirm/block enforcement (incl. the no-TTY confirm degrade-to-block). Its
fail-open TTL/stale fallback (`_claim_is_stale` errors -> treat-as-stale ->
dropped from the block set) is preserved verbatim across the move.

Depends on the shared, record-I/O, and identity leaves. A few cross-subsystem
primitives are co-located here, at their earliest consumer, to keep the package
acyclic (the later git-hook-install + CLI layers import them from here):
PRECOMMIT_SENTINEL_BEGIN / PRECOMMIT_SENTINEL_END, _git_path, _git_toplevel, INVOKE_HINT.
"""
from __future__ import annotations

import datetime
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .shared import (
    INTENTS_LOG_PATH,
    _REPO_ROOT,
    _read_nul_delimited_paths,
    normalize_path,
)
from .record_io import ClaimRecord, active_intents
from .identity import (
    AGENT_ENV_VAR,
    resolve_agent_identity,
    resolve_session_token,
)


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


def _git_toplevel() -> Optional[Path]:
    """Return the git working-tree root, or ``None`` outside a tree."""
    top = _git_path("rev-parse", "--show-toplevel")
    return Path(top) if top else None


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
