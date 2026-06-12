from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import MetricsConfig, load_config
from .extract import PROPOSAL_COLUMNS, PLAN_COLUMNS, iter_proposal_files, iter_plan_files, extract_proposal_row, extract_plan_row
from .subsystems import _load_all_annotations, _load_collision_log, _collision_count_in_window
from .gitmeta import _get_head_commit, _list_goodnight_commits
from .report import format_csv


# ------------------------------------------- output manifest subsystem


def _v2a_snapshot_csv_columns() -> List[str]:
    """Resolve the snapshot CSV's columns list at manifest-emit time
    (deferred so PROPOSAL_COLUMNS / PLAN_COLUMNS extensions don't require
    a manifest edit)."""
    return _snapshot_columns()


def output_manifest() -> List[Dict[str, object]]:
    """Return the output manifest as a list of dicts (one per emitted
    artifact).  Resolves the snapshot CSV's columns lazily so future
    PROPOSAL_COLUMNS / PLAN_COLUMNS extensions don't require a manifest
    edit.  Paths reflect the default ``snapshots_dir``
    (``dev/measurement/snapshots/``); a project that overrides
    ``snapshots_dir`` relocates the live outputs accordingly."""
    return [
        {
            'file': 'dev/measurement/snapshots/<date>-N.csv',
            'format': 'CSV',
            'stability_tier': 'contract',
            'columns': _v2a_snapshot_csv_columns(),
            'notes': (
                'One row per proposal or plan stem; same-day '
                'events coalesce by N suffix.  Audit-trail '
                'retention: snapshots stay indefinitely (no '
                'goodnight pruning).'
            ),
        },
        {
            'file': 'dev/measurement/snapshots/archive/<release>-rollup.csv',
            'format': 'CSV',
            'stability_tier': 'deferred',
            'columns': [],
            'notes': (
                'Release-boundary rollup; NOT part of core.  '
                'Filename + format pre-specified so future '
                'implementers do not drift.'
            ),
        },
        {
            'file': '<annotations_dir>/<name>-<date>.yml',
            'format': 'YAML',
            'stability_tier': 'best-effort',
            'columns': [
                'affected_artifacts',
                'expected_metrics',
                'hypothesized_direction',
                'minimum_observation_window',
                'known_confounders',
            ],
            'notes': (
                'Per-doctrine-intervention annotation files '
                '(default dir dev/metrics_annotations/).  Reader '
                'is forgiving (parse errors return {}); no schema '
                'contract test.'
            ),
        },
        {
            'file': 'stdout-summary',
            'format': 'text',
            'stability_tier': 'best-effort',
            'columns': [],
            'notes': (
                'One-line snapshot summary + corpus_commit + '
                'snapshot path.  Human-readable; not parsed by '
                'other tools.'
            ),
        },
    ]


#: Metric Contract -> emitted-column map.  Bidirectional source of truth:
#: every metric named in the reference doc's Metric Contract table maps to
#: either a concrete snapshot CSV column or to ``''`` (deferred --
#: documented but not emitted in core).  The contract test pair enforces
#: both directions.
METRIC_CONTRACT_MAP: Dict[str, str] = {
    # Layer 1 -- Flow metrics (per-stage)
    'proposal_stage_days_open_to_reviewed': 'days_open_to_reviewed',
    'proposal_stage_hours_open_to_reviewed': 'hours_open_to_reviewed',
    'proposal_stage_days_reviewed_to_revised': 'days_reviewed_to_revised',
    'proposal_stage_hours_reviewed_to_revised': 'hours_reviewed_to_revised',
    'proposal_stage_days_revised_to_decision': 'days_revised_to_decision',
    # Deferred / aggregate metrics (named for forward-pinning, mapped '').
    'proposal_stage_days_total': '',
    'proposal_lifecycle_cdf_p25': '',
    'proposal_lifecycle_cdf_p50': '',
    'proposal_lifecycle_cdf_p75': '',
    'proposal_lifecycle_cdf_p95': '',
    'proposal_count_by_status': '',
    'plan_count_by_status': '',
    # Per-proposal scalar columns
    'proposal_annotation_count': 'proposal_annotation_count',
    # Disposition / yield
    'proposal_review_yield_accept_count': 'review_yield_accept_count',
    'proposal_review_yield_reject_count': 'review_yield_reject_count',
    'proposal_review_yield_defer_count': 'review_yield_defer_count',
    # Role / tier / matrix (aggregator helpers; surfaced via the per-
    # proposal columns the helpers consume).
    'proposal_author_role_tier_tuple': 'author',
    'proposal_reviewer_role_tier_tuple': 'reviewer_agents',
    'proposal_author_reviewer_matrix_cell': 'reviewer_agents',
    # Collision (deferred siblings stay in map for two-way pinning)
    'collision_count_rolling_14d': 'corpus_collision_count_14d',
    'collision_count_prevented_overlap_rolling_14d': '',
    'collision_count_parallel_non_conflict_rolling_14d': '',
    # Meta-columns
    'corpus_commit': 'corpus_commit',
    'snapshot_event': 'snapshot_event',
    'snapshot_timestamp_utc': 'snapshot_timestamp_utc',
}


def format_manifest_md() -> str:
    """Render the output manifest as a GitHub-flavored markdown table.
    Used by the ``--manifest`` CLI flag."""
    lines = [
        '| File | Format | Stability tier | Columns | Notes |',
        '|------|--------|----------------|---------|-------|',
    ]
    for entry in output_manifest():
        cols = entry['columns']
        if isinstance(cols, list) and cols:
            col_text = ', '.join(str(c) for c in cols)
        else:
            col_text = ''
        notes = str(entry.get('notes', '')).replace('\n', ' ')
        col_text = col_text.replace('|', r'\|')
        notes = notes.replace('|', r'\|')
        lines.append(
            f"| `{entry['file']}` | {entry['format']} | "
            f"{entry['stability_tier']} | {col_text} | {notes} |"
        )
    return '\n'.join(lines) + '\n'


# ------------------------------------------- snapshot layer (relocated)


#: The unified snapshot meta-columns appended after the proposal / plan
#: columns.  ``corpus_collision_count_14d`` carries the corpus-wide
#: rolling-window collision count (same value across every row of a
#: snapshot -- a property of the snapshot, not the row).
_SNAPSHOT_META_COLUMNS = (
    'corpus_commit',
    'snapshot_event',
    'snapshot_timestamp_utc',
    'corpus_collision_count_14d',
)


def _snapshot_columns() -> List[str]:
    """The full unified snapshot column list.  Computed once per call so a
    future PROPOSAL_COLUMNS / PLAN_COLUMNS extension folds in without
    further edits here."""
    cols: List[str] = ['kind']
    cols.extend(PROPOSAL_COLUMNS)
    for c in PLAN_COLUMNS:
        if c not in cols:
            cols.append(c)
    cols.extend(_SNAPSHOT_META_COLUMNS)
    return cols


def _next_snapshot_index(out_dir: Path, date_iso: str) -> int:
    """Next monotonic snapshot index for the given date.  Scans ``out_dir``
    for files matching ``<date_iso>-<N>.csv`` and returns the next
    integer; 1 when no prior snapshots exist for that date.  Same-day
    events thus coalesce into a sequence of dated files rather than
    overwriting."""
    if not out_dir.is_dir():
        return 1
    pattern = re.compile(r'^' + re.escape(date_iso) + r'-(\d+)\.csv$')
    max_n = 0
    for entry in out_dir.iterdir():
        m = pattern.match(entry.name)
        if m:
            try:
                max_n = max(max_n, int(m.group(1)))
            except ValueError:
                continue
    return max_n + 1


def _build_snapshot_rows(
    *,
    root: Path,
    config: MetricsConfig,
    event: str,
    corpus_commit: str,
    timestamp_utc: str,
    collision_count_14d: object = '',
    include_git_timestamps: bool = True,
) -> List[Dict[str, object]]:
    """Build the unified snapshot row list: proposals + plans, each row
    tagged with ``kind`` + the four meta-columns.  Proposals are ordered
    as ``proposal_rows()`` returns them; plans follow, sorted by ``stem``.
    ``collision_count_14d`` is threaded onto every row so downstream
    consumers can correlate per-proposal motion against the
    contemporaneous collision-rate envelope."""
    rows: List[Dict[str, object]] = []
    annotations = _load_all_annotations(config.annotations_dir)
    for p in iter_proposal_files(root):
        r = extract_proposal_row(
            p,
            include_git_timestamps=include_git_timestamps,
            repo_root=root,
            annotations=annotations,
        )
        r['kind'] = 'proposal'
        r['corpus_commit'] = corpus_commit
        r['snapshot_event'] = event
        r['snapshot_timestamp_utc'] = timestamp_utc
        r['corpus_collision_count_14d'] = collision_count_14d
        rows.append(r)
    rows.sort(key=lambda r: (str(r.get('date_opened', '')), str(r['stem'])))
    proposal_stems = [p.stem for p in iter_proposal_files(root)]
    plan_rows_list: List[Dict[str, object]] = []
    for p in iter_plan_files(root):
        r = extract_plan_row(p, proposal_stems)
        r['kind'] = 'plan'
        r['corpus_commit'] = corpus_commit
        r['snapshot_event'] = event
        r['snapshot_timestamp_utc'] = timestamp_utc
        r['corpus_collision_count_14d'] = collision_count_14d
        plan_rows_list.append(r)
    plan_rows_list.sort(key=lambda r: str(r['stem']))
    rows.extend(plan_rows_list)
    return rows


def emit_snapshot(
    *,
    root: Path,
    config: Optional[MetricsConfig] = None,
    event: str = 'manual',
    out_dir: Optional[Path] = None,
    timestamp_utc: Optional[datetime.datetime] = None,
    corpus_commit: Optional[str] = None,
    dry_run: bool = False,
) -> Tuple[Path, int]:
    """Emit a snapshot CSV under ``out_dir`` (default:
    ``config.snapshots_dir`` -> ``dev/measurement/snapshots/``).

    Returns ``(snapshot_path, row_count)``.  When ``dry_run=True`` the
    would-be path is returned without writing -- useful for the
    reproducibility contract (``git checkout <corpus_commit> && ...
    --snapshot --dry-run`` reproduces the data rows exactly).  ``event``
    is the trigger label; ``timestamp_utc`` defaults to now (UTC);
    ``corpus_commit`` defaults to the live ``HEAD`` short SHA.  Audit-trail
    retention: this writer does NOT prune older snapshots."""
    cfg = config if config is not None else load_config(root)
    target_dir = out_dir if out_dir is not None else cfg.snapshots_dir
    if timestamp_utc is None:
        ts = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    else:
        ts = (
            timestamp_utc.replace(tzinfo=None)
            if timestamp_utc.tzinfo is not None
            else timestamp_utc
        )
    ts_iso = ts.replace(microsecond=0).isoformat() + 'Z'
    date_iso = ts.date().isoformat()
    commit = (
        corpus_commit if corpus_commit is not None
        else _get_head_commit(repo_root=root)
    )

    collision_entries = _load_collision_log(cfg.collision_log)
    if collision_entries:
        collision_count_14d: object = _collision_count_in_window(
            collision_entries,
            as_of=ts.date(),
            window_days=cfg.collision_window_days,
            kind=cfg.collision_counted_kind,
        )
    else:
        collision_count_14d = ''

    rows = _build_snapshot_rows(
        root=root,
        config=cfg,
        event=event,
        corpus_commit=commit,
        timestamp_utc=ts_iso,
        collision_count_14d=collision_count_14d,
    )
    columns = _snapshot_columns()

    n = _next_snapshot_index(target_dir, date_iso)
    snapshot_path = target_dir / f'{date_iso}-{n}.csv'

    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
        text = format_csv(rows, columns)
        snapshot_path.write_text(text, encoding='utf-8')

    return snapshot_path, len(rows)


def backfill(
    *,
    root: Path,
    config: Optional[MetricsConfig] = None,
    since: datetime.date,
    max_days: Optional[int] = None,
    out_dir: Optional[Path] = None,
    dry_run: bool = False,
    today: Optional[datetime.date] = None,
) -> List[Tuple[Path, int]]:
    """Bounded-backfill smoke.  Emits one snapshot per ``Goodnight:``-tagged
    commit in the window ``[max(since, today - max_days), today]``.

    The window is capped at ``max_days`` (default
    ``config.backfill_max_days`` -> 14) regardless of ``since``; the cap is
    doctrine (smoke, not exhaustive backfill).  Each snapshot's
    ``snapshot_event='backfill'`` and ``corpus_commit=<commit-sha>``;
    ``snapshot_timestamp_utc`` matches the commit's committer-date.
    Returns a list of ``(snapshot_path, row_count)`` tuples."""
    cfg = config if config is not None else load_config(root)
    cap = max_days if max_days is not None else cfg.backfill_max_days
    today_d = today if today is not None else datetime.date.today()
    window_start = max(since, today_d - datetime.timedelta(days=cap))
    since_iso = window_start.isoformat()
    commits = _list_goodnight_commits(since_iso, repo_root=root)
    results: List[Tuple[Path, int]] = []
    for sha, committer_iso in commits:
        try:
            ts = datetime.datetime.fromisoformat(committer_iso)
        except ValueError:
            continue
        if ts.tzinfo is not None:
            ts = ts.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        path, n = emit_snapshot(
            root=root,
            config=cfg,
            event='backfill',
            out_dir=out_dir,
            timestamp_utc=ts,
            corpus_commit=sha,
            dry_run=dry_run,
        )
        results.append((path, n))
    return results
