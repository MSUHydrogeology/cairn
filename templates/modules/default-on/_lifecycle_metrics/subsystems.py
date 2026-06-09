from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .parse import _parse_date
from .config import _DEFAULT_MODEL_TIERS


# ------------------------------------------- annotation reader subsystem


def _load_annotation(path: Path) -> Dict[str, object]:
    """Parse one annotation YAML file into a dict.

    Returns an empty dict on parse error, missing PyYAML, or a non-mapping
    document -- the annotation reader is forgiving by design (best-effort
    stability tier).  Each annotation may name ``affected_artifacts`` (the
    proposal / plan stems an intervention is hypothesized to affect),
    ``expected_metrics``, ``hypothesized_direction``,
    ``minimum_observation_window``, and ``known_confounders``.  No schema
    enforcement -- the reader trusts the annotation-writing discipline.
    """
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        return {}
    try:
        text = path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return {}
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def _load_all_annotations(annotations_dir: Path) -> List[Dict[str, object]]:
    """Load every ``*.yml`` annotation under ``annotations_dir``.

    Returns a list of dicts (one per file).  Skips files that fail to
    parse; returns an empty list when the directory doesn't exist (the
    common case for a repo with no annotation activity).  Stable ordering
    by filename so snapshot row-population is deterministic.
    """
    if not annotations_dir.is_dir():
        return []
    out: List[Dict[str, object]] = []
    for entry in sorted(annotations_dir.iterdir()):
        if entry.suffix == '.yml' and entry.is_file():
            data = _load_annotation(entry)
            if data:
                out.append(data)
    return out


def _annotation_count_for_stem(
    stem: str, annotations: Sequence[Dict[str, object]],
) -> int:
    """Number of annotations naming ``stem`` under their
    ``affected_artifacts`` list.  Match is exact-string equality on the
    stem; an annotation with no (or a non-list) ``affected_artifacts``
    field contributes zero to every stem's count."""
    count = 0
    for annot in annotations:
        artifacts = annot.get('affected_artifacts')
        if isinstance(artifacts, list) and stem in artifacts:
            count += 1
    return count


# ------------------------------------------- disposition / review-yield


#: The normalized disposition buckets the Response grammars emit.  The
#: code-review-Response ``accept (...)`` variants collapse into the bare
#: ``accept`` bucket; ``wontfix`` (code-review-Response only) gets its own
#: bucket so the parser is lossless across both grammars, but is not
#: surfaced as a proposal-row column (proposals use the 4-token grammar).
_DISPOSITION_BUCKETS = (
    'accept',
    'accept_with_modification',
    'reject',
    'defer',
    'wontfix',
)

#: Disposition-bullet shape: ``* **[<id>]** <disposition> -- <rationale>``.
#: The ``[<id>]`` interior is permissive ([R1], [F2], etc.); the
#: disposition text runs to ``--`` or end-of-line.  Capture group 1 is the
#: disposition text.
_DISPOSITION_BULLET_RE = re.compile(
    r'^\s*\*\s+\*\*\[[^\]]+\]\*\*\s+(.+?)(?:\s+--\s+|\s*$)',
)


def _normalize_disposition_token(text: str) -> str:
    """Normalize a raw disposition string into a bucket name.

    Returns one of ``_DISPOSITION_BUCKETS`` plus ``''`` for an
    unrecognized token (caller drops those; the forgiving stance matches
    the rest of the parsers).  Both grammars covered: the proposal-Response
    4-token grammar (``accept`` / ``accept with modification`` / ``reject``
    / ``defer``) and the code-review-Response grammar whose ``accept
    (...)`` variants all collapse into ``accept`` plus a ``wontfix`` token.
    """
    t = text.strip().lower()
    t = t.rstrip(' .,;:')
    if t.startswith('accept with modification'):
        return 'accept_with_modification'
    if t.startswith('accept'):
        return 'accept'
    if t.startswith('reject'):
        return 'reject'
    if t.startswith('defer'):
        return 'defer'
    if t.startswith('wontfix'):
        return 'wontfix'
    return ''


def _parse_disposition_tokens(body: Sequence[str]) -> List[str]:
    """Extract disposition tokens from one Response section body.

    ``body`` is the list of lines inside a single ``## Response`` h2
    section.  Scans for disposition bullets, normalizes each, returns the
    list in encounter order.  Unrecognized tokens are dropped silently.
    """
    tokens: List[str] = []
    for line in body:
        m = _DISPOSITION_BULLET_RE.match(line)
        if not m:
            continue
        bucket = _normalize_disposition_token(m.group(1))
        if bucket:
            tokens.append(bucket)
    return tokens


def _review_yield_counts(
    sections: Sequence[Tuple[str, List[str]]],
) -> Dict[str, int]:
    """Aggregate disposition counts across every ``## Response`` section
    in one proposal.

    Returns a dict keyed by every entry in ``_DISPOSITION_BUCKETS``
    (zero-initialized so consumers can index without ``KeyError``)."""
    counts: Dict[str, int] = {bucket: 0 for bucket in _DISPOSITION_BUCKETS}
    for heading, body in sections:
        if not re.match(r'## Response\b', heading):
            continue
        for token in _parse_disposition_tokens(body):
            counts[token] = counts.get(token, 0) + 1
    return counts


# ------------------------------------------- Model field + tier classifier


#: ``**Model**:`` field shape: ``**Model**:`` followed by an arbitrary
#: value (the agent's self-disclosed model / tier string).  Files lacking
#: the field yield ``''`` for that Response.
_MODEL_FIELD_RE = re.compile(
    r'^\s*\*\*Model\*\*\s*:\s*(.+?)\s*$',
    re.MULTILINE,
)


def _extract_response_models(
    sections: Sequence[Tuple[str, List[str]]],
) -> List[str]:
    """Extract ``**Model**:`` strings from every ``## Response`` section's
    body.

    Returns the list of raw model strings in section-encounter order;
    sections missing the field contribute ``''``.  The
    list-length-equals-Response-section-count contract makes column
    emission a 1:1 join with the ``reviewer_agents`` list."""
    models: List[str] = []
    for heading, body in sections:
        if not re.match(r'## Response\b', heading):
            continue
        body_text = '\n'.join(body)
        m = _MODEL_FIELD_RE.search(body_text)
        models.append(m.group(1).strip() if m else '')
    return models


def _classify_model_to_tier(
    model: str, tiers: Optional[Sequence[Tuple[str, str]]] = None,
) -> str:
    """Classify a raw ``**Model**:`` string into a capability tier.

    ``tiers`` is the open ``[substring, label]`` list (from
    :data:`MetricsConfig.model_tiers`; defaults to
    :data:`_DEFAULT_MODEL_TIERS`).  First case-insensitive substring match
    wins; ``'tier-unknown'`` when no pattern matches (incl. empty input)."""
    if not model:
        return 'tier-unknown'
    table = tiers if tiers is not None else _DEFAULT_MODEL_TIERS
    lower = model.lower()
    for pattern, tier in table:
        if pattern in lower:
            return tier
    return 'tier-unknown'


def _per_role_per_tier_summary(
    rows: Sequence[Dict[str, object]],
    *,
    tiers: Optional[Sequence[Tuple[str, str]]] = None,
) -> List[Dict[str, object]]:
    """Aggregate proposal rows into one row per ``(agent, role, tier)``.

    Each input row contributes ``(author, 'author', 'tier-unknown')`` (the
    row schema carries no author Model field yet) plus
    ``(reviewer, 'reviewer', <reviewer-tier>)`` for each reviewer /
    response-Model pair (zipped 1:1 from the ``reviewer_agents`` +
    ``response_models`` columns).  Returns rows sorted by ``(agent, role,
    tier)`` with a ``count`` field."""
    counts: Dict[Tuple[str, str, str], int] = {}
    for r in rows:
        author = str(r.get('author') or '')
        if author:
            key = (author, 'author', 'tier-unknown')
            counts[key] = counts.get(key, 0) + 1
        reviewers = str(r.get('reviewer_agents') or '').split('|')
        models = str(r.get('response_models') or '').split('|')
        while len(models) < len(reviewers):
            models.append('')
        for reviewer, model in zip(reviewers, models):
            if not reviewer:
                continue
            tier = _classify_model_to_tier(model, tiers)
            key = (reviewer, 'reviewer', tier)
            counts[key] = counts.get(key, 0) + 1
    out: List[Dict[str, object]] = []
    for (agent, role, tier), n in sorted(counts.items()):
        out.append({
            'agent': agent, 'role': role, 'tier': tier, 'count': n,
        })
    return out


def _author_reviewer_matrix(
    rows: Sequence[Dict[str, object]],
) -> List[Dict[str, object]]:
    """Build the author x reviewer matrix from proposal rows.

    One output row per ``(author, reviewer)`` pair with a count of how many
    proposals carry that pair.  Surfaces structural-independence patterns:
    a high same-identity count suggests inadequate cross-agent-type review
    coverage."""
    counts: Dict[Tuple[str, str], int] = {}
    for r in rows:
        author = str(r.get('author') or '')
        reviewers = str(r.get('reviewer_agents') or '').split('|')
        if not author:
            continue
        for reviewer in reviewers:
            if not reviewer:
                continue
            key = (author, reviewer)
            counts[key] = counts.get(key, 0) + 1
    out: List[Dict[str, object]] = []
    for (author, reviewer), n in sorted(counts.items()):
        out.append({
            'author': author, 'reviewer': reviewer, 'count': n,
        })
    return out


# ------------------------------------------- collision-log subsystem


def _parse_collision_log(text: str) -> List[Dict[str, str]]:
    """Parse the incident-log markdown table out of the collision log.

    The file's text-shape is a GitHub-flavored markdown table whose header
    row reads ``| Date | Type | File | Commit(s) | Note |``.  This parser
    is deliberately forgiving (best-effort tier): it locates the table by
    its header row, stops at the first non-table line, drops rows whose
    ``Date`` cell isn't a valid ISO date, and returns ``[]`` on any
    structural surprise.  Each parsed entry carries lowercased keys
    ``date`` / ``type`` / ``file`` / ``commits`` / ``note``."""
    entries: List[Dict[str, str]] = []
    lines = text.splitlines()
    header_idx: Optional[int] = None
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.split('|')]
        cells = [c for c in cells if c]
        if (
            len(cells) >= 5
            and cells[0].lower() == 'date'
            and cells[1].lower() == 'type'
            and cells[2].lower() == 'file'
        ):
            header_idx = i
            break
    if header_idx is None:
        return entries

    data_start = header_idx + 2
    for line in lines[data_start:]:
        if not line.strip().startswith('|'):
            break
        cells = [c.strip() for c in line.split('|')]
        cells = [c for c in cells if c]
        if len(cells) < 5:
            continue
        date_cell = cells[0]
        if _parse_date(date_cell) is None:
            continue
        entries.append({
            'date': date_cell,
            'type': cells[1],
            'file': cells[2],
            'commits': cells[3],
            'note': cells[4],
        })
    return entries


def _load_collision_log(path: Path) -> List[Dict[str, str]]:
    """Read + parse the collision log at ``path``.  Returns ``[]`` when
    the file is missing or unreadable -- the same forgiving stance the
    annotation reader takes."""
    try:
        text = path.read_text(encoding='utf-8')
    except (OSError, FileNotFoundError):
        return []
    return _parse_collision_log(text)


def _collision_count_in_window(
    entries: Sequence[Dict[str, str]],
    *,
    as_of: datetime.date,
    window_days: int = 14,
    kind: str = 'true-staged-index',
) -> int:
    """Count collision entries of ``kind`` whose ``date`` falls within the
    rolling ``window_days`` ending at ``as_of`` (inclusive both ends).

    Defaults match the canonical re-open trigger (14-day window,
    ``true-staged-index`` only); a project overrides both via the
    ``collision_window_days`` / ``collision_counted_kind`` config keys.
    Entries with malformed dates contribute 0."""
    window_start = as_of - datetime.timedelta(days=window_days - 1)
    count = 0
    for entry in entries:
        if entry.get('type') != kind:
            continue
        d = _parse_date(str(entry.get('date', '')))
        if d is None:
            continue
        if window_start <= d <= as_of:
            count += 1
    return count
