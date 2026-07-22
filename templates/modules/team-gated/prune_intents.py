# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Goodnight compaction for the work-intent JSONL log.

Rewrites the active intent log at ``dev/intents.jsonl`` to keep only active
claims and recent (within the grace window) released claims; older released
claims are discarded in-place rather than archived.

The compaction step is invoked by the **full-handoff owner** during the
goodnight routine, at the same point where the roadmap scrub and reflections
read already run.  It is **single-writer at goodnight** -- the routine
serializes the shared communication surfaces; concurrent goodnight
compactions are not a concern.

Active-claim hygiene: claims that have no release event AND are older than
the grace window are *not* discarded.  They stay in the active log AND get
reported to the goodnight owner ("these claims were never released -- agent
died, forgot, or work is genuinely still in progress") so the owner can
decide whether to release them manually or leave them as indicators of
in-flight work.

This script is shipped with the ``coordination-tiers`` module (the module
whose doctrine prescribes the prune-intents goodnight step).  It is
stdlib-only: no imports from ``tools.intent``; the log is read directly.

CLI::

    python tools/prune_intents.py              # 24h grace window
    python tools/prune_intents.py --dry-run    # report; change nothing
    python tools/prune_intents.py --grace-hours 48  # override window
    python tools/prune_intents.py --log-path dev/intents.jsonl
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Constants

_REPO_ROOT = Path(__file__).resolve().parents[1]

#: Default path to the active intent log.
INTENTS_LOG_PATH = _REPO_ROOT / "dev" / "intents.jsonl"

#: Default grace window for released claims (hours).  Released claims younger
#: than this stay in the active log so a same-session reader can still see the
#: just-completed work; older ones are discarded in-place.
DEFAULT_GRACE_HOURS = 24


# ---------------------------------------------------------------------------
# Log reading (self-contained; does not import from tools.intent)


def _iter_log(log_path: Path) -> Iterator[Dict[str, object]]:
    """Yield records from a JSONL log, skipping malformed lines."""
    if not log_path.exists():
        return
    with log_path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                yield json.loads(stripped)
            except json.JSONDecodeError as exc:
                sys.stderr.write(
                    f"prune_intents: skipping malformed line {line_no} in "
                    f"{log_path}: {exc}\n"
                )
                continue


# ---------------------------------------------------------------------------
# Record partitioning


def _parse_ts(ts: str) -> Optional[datetime.datetime]:
    """Parse an ISO-8601 timestamp.  Returns ``None`` on any parse failure
    (forgiving stance -- a malformed timestamp is a data-quality issue
    downstream, not a reason to abort compaction).

    Normalizes to **naive** local-wallclock form by stripping tzinfo: records
    written by the intent tool include timezone offsets; test records may use
    naive iso strings.  Either way the grace-window comparison treats both
    sides as wallclock deltas.
    """
    if not isinstance(ts, str):
        return None
    try:
        parsed = datetime.datetime.fromisoformat(ts)
    except ValueError:
        return None
    if parsed.tzinfo is not None:
        parsed = parsed.replace(tzinfo=None)
    return parsed


def _now_local() -> datetime.datetime:
    """Naive local-wallclock now() to match :func:`_parse_ts`'s normalization."""
    return datetime.datetime.now()


def partition_records(
    records: List[Dict[str, object]],
    *,
    now: Optional[datetime.datetime] = None,
    grace: Optional[datetime.timedelta] = None,
) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    """Partition records into (keep_active, stale_active).

    * **keep_active** is the set of records that should remain in the active
      log after compaction: every active claim (claim without matching release)
      AND every claim/release pair whose release happened within the grace
      window AND the matching release event itself.
    * **stale_active** is a subset of keep_active: active claims whose ``ts``
      is older than ``grace``.  Returned separately so the CLI can surface
      them as warnings to the goodnight owner.
    """
    if now is None:
        now = _now_local()
    if grace is None:
        grace = datetime.timedelta(hours=DEFAULT_GRACE_HOURS)
    threshold = now - grace

    claims: Dict[str, Dict[str, object]] = {}
    releases: Dict[str, Dict[str, object]] = {}
    others: List[Dict[str, object]] = []
    for record in records:
        event = record.get('event')
        rid = record.get('id')
        if not isinstance(rid, str):
            others.append(record)
            continue
        if event == 'claim':
            claims[rid] = record
        elif event == 'release':
            releases[rid] = record
        else:
            others.append(record)

    keep_active: List[Dict[str, object]] = list(others)
    stale_active: List[Dict[str, object]] = []

    for cid, claim in claims.items():
        release = releases.get(cid)
        if release is None:
            # Active claim.  Check whether it's stale.
            claim_ts = _parse_ts(str(claim.get('ts') or ''))
            if claim_ts is not None and claim_ts < threshold:
                stale_active.append(claim)
            keep_active.append(claim)
            continue
        # Pair: partition by release ts.
        release_ts = _parse_ts(str(release.get('ts') or ''))
        if release_ts is None:
            # Malformed release ts -- be conservative, keep in active log.
            keep_active.append(claim)
            keep_active.append(release)
            continue
        if release_ts >= threshold:
            # Within grace window: keep both events in the active log.
            keep_active.append(claim)
            keep_active.append(release)

    # Orphan releases (release with no matching claim) -- pass through.
    for rid, release in releases.items():
        if rid not in claims:
            keep_active.append(release)

    return keep_active, stale_active


# ---------------------------------------------------------------------------
# Writing the compacted log


def _atomic_rewrite(target: Path, records: List[Dict[str, object]]) -> None:
    """Rewrite ``target`` with the given records atomically.

    Strategy: write to ``<target>.tmp`` then ``os.rename``.  On POSIX,
    ``rename`` is atomic within the same filesystem.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + '.tmp')
    chunks: List[bytes] = []
    for record in records:
        line = json.dumps(record, separators=(',', ':'), ensure_ascii=False) + '\n'
        chunks.append(line.encode('utf-8'))
    payload = b''.join(chunks)
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        written = 0
        while written < len(payload):
            written += os.write(fd, payload[written:])
    finally:
        os.close(fd)
    os.rename(str(tmp), str(target))


# ---------------------------------------------------------------------------
# Top-level compaction routine


def compact(
    *,
    log_path: Optional[Path] = None,
    grace_hours: float = DEFAULT_GRACE_HOURS,
    dry_run: bool = False,
    now: Optional[datetime.datetime] = None,
) -> Dict[str, object]:
    """Run goodnight compaction on the active intent log.

    Returns a dict carrying:

    * ``log_path``: the active log path
    * ``kept_active_count``: records preserved in the active log
    * ``pruned_count``: records discarded (not kept)
    * ``stale_active``: list of stale-active claim dicts surfaced to the
      caller for goodnight-owner warnings
    * ``dry_run``: whether the run only reported
    """
    target = log_path if log_path is not None else INTENTS_LOG_PATH
    grace = datetime.timedelta(hours=grace_hours)

    if not target.exists():
        return {
            'log_path': target,
            'kept_active_count': 0,
            'pruned_count': 0,
            'stale_active': [],
            'dry_run': dry_run,
        }

    records = list(_iter_log(target))
    keep_active, stale_active = partition_records(records, now=now, grace=grace)

    if dry_run:
        return {
            'log_path': target,
            'kept_active_count': len(keep_active),
            'pruned_count': len(records) - len(keep_active),
            'stale_active': stale_active,
            'dry_run': True,
        }

    _atomic_rewrite(target, keep_active)

    return {
        'log_path': target,
        'kept_active_count': len(keep_active),
        'pruned_count': len(records) - len(keep_active),
        'stale_active': stale_active,
        'dry_run': False,
    }


# ---------------------------------------------------------------------------
# CLI


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog='prune_intents',
        description=(
            'Goodnight compaction for dev/intents.jsonl.  '
            'Rewrites the active log keeping only active claims '
            'and recent (within grace window) released claims; '
            'older released claims are discarded in-place.'
        ),
    )
    parser.add_argument(
        '--log-path', default=None,
        help='Override active log path (default: dev/intents.jsonl).',
    )
    parser.add_argument(
        '--grace-hours', type=float, default=DEFAULT_GRACE_HOURS,
        help=(
            f'Grace window for released claims in hours '
            f'(default: {DEFAULT_GRACE_HOURS}). Released claims '
            f'younger than this stay in the active log.'
        ),
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Report what would be pruned; change nothing.',
    )
    args = parser.parse_args(argv)

    log_path = Path(args.log_path) if args.log_path else None
    result = compact(
        log_path=log_path,
        grace_hours=args.grace_hours,
        dry_run=args.dry_run,
    )

    verb = 'would keep' if args.dry_run else 'kept'
    pruned_verb = 'would discard' if args.dry_run else 'discarded'
    sys.stderr.write(
        f'prune_intents: {verb} {result["kept_active_count"]} '
        f'records in active log; '
        f'{pruned_verb} {result["pruned_count"]} '
        f'records past the grace window.\n'
    )
    if result['stale_active']:
        sys.stderr.write(
            f'prune_intents: WARNING -- '
            f'{len(result["stale_active"])} active '
            f'{"claim" if len(result["stale_active"]) == 1 else "claims"} '
            f'older than the grace window were never released. '
            f'Agent died, forgot to release, or work is still in '
            f'flight. Goodnight owner: review and release '
            f'manually if appropriate.\n'
        )
        for active in result['stale_active']:
            sys.stderr.write(
                f"  - id={active.get('id')!r} "
                f"agent={active.get('agent')!r} "
                f"ts={active.get('ts')!r} "
                f"action={active.get('action')!r}\n"
            )
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
