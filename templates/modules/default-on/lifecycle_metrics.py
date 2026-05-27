#!/usr/bin/env python3
"""Lifecycle-metrics extractor for the proposal / plan corpus.

The Cairn ``lifecycle-metrics`` module's reference implementation.  The
scaffold installs this script into an adopting repo's ``tools/``
directory (verbatim -- no token substitution over code); the
``{{metrics_command}}`` token in the adopter's ``dev/agent_collaboration.md``
points at it.  It is vendor-neutral and **standard-library only**.

It walks ``dev/proposals/`` and ``dev/plans/`` (live and archived),
parses the in-file lifecycle headers + section grammar that the Cairn
scaffold installs, and emits a tidy CSV (or markdown) table of
per-proposal / per-plan lifecycle metrics -- review rounds, revision
counts, time-to-decision, finding severities.  It turns a team's
discipline self-claims ("External review catches structural problems",
"revision counts spike when scope is too large") from unfalsifiable
assertions into quantified, checkable rows.

**No repo-mutation surface.**  The tool parses files, mutates nothing,
and touches no git state except an optional read-only ``git log`` for
sub-day commit timestamps.  It is read-only with respect to the source
corpus; the optional ``--out`` flag writes only the derived report file
(the same content otherwise sent to stdout).  The emitted CSV is a
derived artifact -- regenerable from the repo at any commit -- and is
therefore not committed.

**Generalized from modflow_tools' ``tools/lifecycle_metrics.py``.**
This is the **v1 core** extractor.  The modflow_tools implementation
also carries a *snapshot layer* (committed dated CSV snapshots, a
collision-log parser, a metrics-annotations reader, a ``Goodnight:``
commit backfill, per-tier model aggregation) that is specific to that
project's own instrumentation and is deliberately **not** shipped here.
An adopter who wants committed snapshots can add them; the v1 core is
the measurable spine the module promises.

Usage::

    python tools/lifecycle_metrics.py proposals             # default
    python tools/lifecycle_metrics.py plans
    python tools/lifecycle_metrics.py proposals --out m.csv
    python tools/lifecycle_metrics.py proposals --format md
    python tools/lifecycle_metrics.py proposals --root /path/to/repo

Reliability tiers (the source corpus is prose-structured, not
schema-structured):

* **Exact** -- header fields, section-header counts, reviewer agent
  type.
* **Good** -- ``total_findings`` (finding-heading bullet counts).
* **Best-effort** -- ``findings_p1/_p2/_p3`` severity (the
  ``[P1]/[P2]/[P3]`` tag convention); ``external_tier_review`` (role-
  label parse, ``unknown`` bucket for label-less headers);
  ``paired_proposal`` slug-match fallback.

Robust across VCS settings: when git is absent, the path is not a
checkout, or the default branch is named ``main`` rather than
``master``, the optional commit-timestamp augmentation degrades quietly
(empty hour-delta columns + a ``Best-effort`` reliability tier) rather
than raising.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import io
import re
import sys
from pathlib import Path
from typing import AbstractSet, Dict, List, Optional, Sequence, Tuple

#: Default repo root when ``--root`` is not given.  For the installed
#: script at ``<target>/tools/lifecycle_metrics.py`` this is ``<target>``
#: (``tools/`` -> repo root).  ``--root`` overrides it for any layout.
_REPO_ROOT = Path(__file__).resolve().parents[1]


def proposals_dir(root: Path) -> Path:
    """The proposals corpus root under *root*."""
    return root / 'dev' / 'proposals'


def plans_dir(root: Path) -> Path:
    """The plans corpus root under *root*."""
    return root / 'dev' / 'plans'


# Per-proposal schema (v1 core -- the generic lifecycle columns).
PROPOSAL_COLUMNS = [
    'stem',
    'author',
    'date_opened',
    'status',
    'decision_date',
    'days_to_decision',
    'review_rounds',
    'reviewer_agents',
    'cross_agent_type_review',
    'external_tier_review',
    'revised',
    'total_findings',
    'findings_p1',
    'findings_p2',
    'findings_p3',
    # Per-stage timestamps + deltas.  Header dates give day-level
    # precision; git commit timestamps add sub-day hour-level precision
    # when available (degrading to empty + Best-effort without git).
    'reviewed_date',
    'revised_date',
    'days_open_to_reviewed',
    'days_reviewed_to_revised',
    'days_revised_to_decision',
    'hours_open_to_reviewed',
    'hours_reviewed_to_revised',
    'hours_revised_to_decision',
    'stage_timestamp_reliability',
]

# Per-plan schema.
PLAN_COLUMNS = [
    'stem',
    'status',
    'plan_review_rounds',
    'code_review_rounds',
    'paired_proposal',
    'paired_proposal_reliability',
]

# The four enum tokens a plan status normalizes to.
_PLAN_STATUS_ENUM = ('open', 'executing', 'review', 'archived')

_DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
# A finding-heading bullet inside a Review section: ``* **[...`` --
# robust to the bracket interior (the corpus uses many bracket shapes).
_FINDING_BULLET_RE = re.compile(r'^\s*\*\s+\*\*\[')
# The bracket interior of a finding heading, for the severity scan.
_BRACKET_INTERIOR_RE = re.compile(r'\*\*\[([^\]]*)\]')
# A ``### ... code review`` / ``### ... plan review`` review-round
# subsection heading.  An optional single reviewer-name token before
# the phrase covers older headings (``### Codex code review -- DATE``);
# two tokens before the phrase (``### Response to code review``) is a
# response, not a round, and is correctly excluded.  A trailing ISO
# date is still required at the call site, so chunk labels and the
# literal ``YYYY-MM-DD`` placeholder do not count.
_CODE_REVIEW_HEADING_RE = re.compile(r'### (?:[a-z]+ )?code review\b', re.I)
_PLAN_REVIEW_HEADING_RE = re.compile(r'### (?:[a-z]+ )?plan review\b', re.I)


# --------------------------------------------------------------- corpus walk


def _iter_corpus_files(root: Path) -> List[Path]:
    """All ``.md`` files under ``root`` (live + ``archive/``,
    recursive), excluding ``_template.md``.  Returned unsorted; the
    row builders sort deterministically."""
    if not root.exists():
        return []
    return [p for p in root.rglob('*.md') if p.name != '_template.md']


def iter_proposal_files(root: Path) -> List[Path]:
    """Every non-template proposal file -- ``dev/proposals/*.md`` plus
    ``dev/proposals/archive/**/*.md``."""
    return _iter_corpus_files(proposals_dir(root))


def iter_plan_files(root: Path) -> List[Path]:
    """Every non-template plan file -- ``dev/plans/*.md`` plus
    ``dev/plans/archive/**/*.md``."""
    return _iter_corpus_files(plans_dir(root))


# ------------------------------------------------------------- parse helpers


def _header_field(text: str, name: str) -> str:
    """Return the value of a ``**<name>**:`` header line, or ``''``.

    Matches the proposal / plan header-block convention
    (``**Author**:``, ``**Date opened**:``, ``**Status**:``,
    ``**Source proposal**:``)."""
    pattern = re.compile(r'^\*\*' + re.escape(name) + r'\*\*:\s*(.*)$', re.M)
    m = pattern.search(text)
    return m.group(1).strip() if m else ''


def _strip_role(author: str) -> str:
    """``Claude (Strategy)`` -> ``Claude``; strip the role parenthetical
    so the author column carries the agent identity only."""
    return re.split(r'\s*\(', author, maxsplit=1)[0].strip()


def _agent_of(header: str) -> str:
    """Read the reviewer / author identity token from a section header.

    Header shape: ``## Review -- <Name> (<role>) -- <date>``.  Strips the
    ``## <Word>`` prefix and a leading ``--`` / em-dash separator, then
    takes the identity up to the next separator or parenthetical.
    Vendor-neutral -- no hardcoded agent names; empty / unparseable
    headers map to ``''``."""
    body = re.sub(r'^#+\s*\w+\b', '', header)          # drop '## Review'
    body = re.sub(r'^\s*(?:--|—)\s*', '', body)        # drop leading sep
    body = re.split(r'\s*(?:--|—|\()', body, maxsplit=1)[0].strip()
    return body


def _review_tier(header: str) -> str:
    """Best-effort External / Internal tier from a ``## Review`` header's
    role label.

    Matching is case-insensitive substring stems.  Headers with no role
    word fall to ``unknown``."""
    h = header.lower().replace('-', ' ')
    if 'external' in h or 'antagonistic' in h:
        return 'external'
    if 'internal' in h or 'friendly advers' in h or 'review agent' in h:
        return 'internal'
    return 'unknown'


def _parse_date(value: str) -> Optional[datetime.date]:
    """First ISO ``YYYY-MM-DD`` token in ``value`` as a ``date``, or
    ``None``.  The literal ``YYYY-MM-DD`` template placeholder does not
    match, so template lines parse to ``None``."""
    m = _DATE_RE.search(value or '')
    if not m:
        return None
    try:
        return datetime.date.fromisoformat(m.group(0))
    except ValueError:
        return None


def _split_h2_sections(lines: Sequence[str]) -> List[Tuple[str, List[str]]]:
    """Split a document into ``## ``-delimited top-level sections.

    A section spans from its ``## `` header to the next ``## `` line or
    end-of-file.  ``### `` subsection headers do NOT start a new section.
    Returns ``(header_line, body_lines)`` pairs; content before the
    first ``## `` header is dropped."""
    sections: List[Tuple[str, List[str]]] = []
    header: Optional[str] = None
    body: List[str] = []
    for line in lines:
        if line.startswith('## '):
            if header is not None:
                sections.append((header, body))
            header = line
            body = []
        elif header is not None:
            body.append(line)
    if header is not None:
        sections.append((header, body))
    return sections


# ------------------------------------------- per-stage section dates


def _stage_section_dates(
    sections: Sequence[Tuple[str, List[str]]],
) -> Dict[str, Optional[datetime.date]]:
    """Extract per-stage dates from the proposal's H2 section headers.

    Returns a dict with keys ``reviewed`` / ``revised`` / ``decision``.
    Each value is the first ISO date token in the matching section
    header, or ``None``.  For ``reviewed`` the *first* ``## Review``
    header's date wins (subsequent rounds are counted by
    ``review_rounds``).  Pure function -- no git, no other files."""
    out: Dict[str, Optional[datetime.date]] = {
        'reviewed': None,
        'revised': None,
        'decision': None,
    }
    for header, _ in sections:
        if out['reviewed'] is None and re.match(r'## Review\b', header):
            out['reviewed'] = _parse_date(header)
        if out['revised'] is None and header.startswith('## Revised'):
            out['revised'] = _parse_date(header)
        if out['decision'] is None and header.startswith('## Decision'):
            out['decision'] = _parse_date(header)
    return out


# ------------------------------------- optional git commit timestamps


# Per-stage commit-message patterns for the optional dual-extraction
# (header date + commit timestamp).  Stage -> regex matching the first
# line of a commit message for that lifecycle transition.
_STAGE_COMMIT_PATTERNS: List[Tuple[str, 're.Pattern[str]']] = [
    ('open', re.compile(
        r'^(?:Open proposal|proposal:\s*open|opening proposal)', re.I)),
    ('decision', re.compile(
        r'^(?:Decision\s*[:–—\-]|proposal:\s*Decision)', re.I)),
    ('revised', re.compile(
        r'^(?:proposal:\s*(?:respond to|revise)|Revised proposal)', re.I)),
    ('reviewed', re.compile(r'^Review\b(?!.*\bsharpening\b)', re.I)),
]


def _git_log_for_path(
    path: Path, *, repo_root: Optional[Path] = None,
) -> List[Tuple[str, datetime.datetime, str]]:
    """Return commits touching ``path``, newest-first.

    Each tuple is ``(short_sha, committer_datetime, subject)``.  Returns
    an empty list when git is not available, the repo is not a git
    checkout, or the path has no history -- a deliberately quiet failure
    mode (the caller treats missing commit data as a reliability-tier
    downgrade, not an error).  ``--follow`` preserves history across
    file moves.  VCS-agnostic: no assumption about the default branch
    name (``main`` / ``master`` both work)."""
    import subprocess
    root = repo_root if repo_root is not None else _REPO_ROOT
    try:
        result = subprocess.run(
            ['git', 'log', '--format=%h%x00%cI%x00%s', '--follow',
             '--', str(path)],
            cwd=str(root), capture_output=True, timeout=30, check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return []
    if result.returncode != 0:
        return []
    out: List[Tuple[str, datetime.datetime, str]] = []
    for line in result.stdout.decode('utf-8', errors='replace').splitlines():
        if not line.strip():
            continue
        parts = line.split('\x00', 2)
        if len(parts) != 3:
            continue
        sha, iso_ts, subject = parts
        try:
            ts = datetime.datetime.fromisoformat(iso_ts)
        except ValueError:
            continue
        out.append((sha, ts, subject))
    return out


def _resolve_stage_commits(
    path: Path, *, repo_root: Optional[Path] = None,
) -> Dict[str, Optional[Tuple[str, datetime.datetime]]]:
    """Resolve each lifecycle stage to its first matching commit in the
    file's git history.  Returns a dict keyed ``open`` / ``reviewed`` /
    ``revised`` / ``decision``; each value is ``(sha, datetime)`` or
    ``None``.  When git is unavailable every stage resolves to
    ``None``."""
    log = _git_log_for_path(path, repo_root=repo_root)
    log_oldest_first = list(reversed(log))
    out: Dict[str, Optional[Tuple[str, datetime.datetime]]] = {
        'open': None, 'reviewed': None, 'revised': None, 'decision': None,
    }
    for sha, ts, subject in log_oldest_first:
        for stage, pattern in _STAGE_COMMIT_PATTERNS:
            if out[stage] is None and pattern.match(subject):
                out[stage] = (sha, ts)
                break
    return out


def _hour_delta(
    a: Optional[datetime.datetime], b: Optional[datetime.datetime],
) -> object:
    """Hours between two datetimes, rounded to 3 dp.  ``''`` when either
    is ``None``."""
    if a is None or b is None:
        return ''
    return round((b - a).total_seconds() / 3600.0, 3)


def _day_delta(
    a: Optional[datetime.date], b: Optional[datetime.date],
) -> object:
    """Integer days between two dates.  ``''`` when either is ``None``."""
    if a is None or b is None:
        return ''
    return (b - a).days


def _stage_reliability(
    present: AbstractSet[str], resolved: AbstractSet[str],
) -> str:
    """Stage-timestamp reliability label.

    ``'Exact'`` -- every stage present in the proposal resolved to a git
    commit.  ``'Good'`` -- some but not all present stages resolved.
    ``'Best-effort'`` -- no git commits resolved (day-level header dates
    only)."""
    if not resolved:
        return 'Best-effort'
    if present and present.issubset(resolved):
        return 'Exact'
    return 'Good'


# ----------------------------------------------------------- proposal rows


def extract_proposal_row(
    path: Path,
    *,
    include_git_timestamps: bool = True,
    repo_root: Optional[Path] = None,
) -> Dict[str, object]:
    """Parse one proposal file into a metrics row.

    Pure function of the file contents for the header-only columns.
    When ``include_git_timestamps`` is True (default), an additional
    read-only ``git log`` augments the per-stage data with commit
    timestamps for sub-day precision; disable it for pure-logic tests
    via ``include_git_timestamps=False``."""
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    sections = _split_h2_sections(lines)

    author = _strip_role(_header_field(text, 'Author'))
    date_opened = _parse_date(_header_field(text, 'Date opened'))
    status = _header_field(text, 'Status').split()[:1]
    status_token = status[0].strip(' .,;:').lower() if status else ''

    stage_dates = _stage_section_dates(sections)
    decision_date: Optional[datetime.date] = stage_dates['decision']
    days_to_decision: object = ''
    if date_opened is not None and decision_date is not None:
        days_to_decision = (decision_date - date_opened).days

    review_sections = [
        (h, b) for h, b in sections if re.match(r'## Review\b', h)
    ]
    reviewer_agents = [_agent_of(h) for h, _ in review_sections]
    tiers = [_review_tier(h) for h, _ in review_sections]

    # Generic, vendor-neutral signal: a review round whose reviewer
    # identity differs from the author exists.  (A sharper human/AI
    # split would need a per-team roster, which a shipped tool cannot
    # assume -- so no ``human_review`` column here.)
    cross_agent_type_review = any(
        a and author and a != author for a in reviewer_agents
    )

    if not tiers:
        external_tier_review: object = ''
    elif 'external' in tiers:
        external_tier_review = True
    elif 'internal' in tiers:
        external_tier_review = False
    else:
        external_tier_review = 'unknown'

    revised = any(h.startswith('## Revised') for h, _ in sections)

    total_findings = 0
    findings = {'P1': 0, 'P2': 0, 'P3': 0}
    for _, body in review_sections:
        for line in body:
            if not _FINDING_BULLET_RE.match(line):
                continue
            total_findings += 1
            m = _BRACKET_INTERIOR_RE.search(line)
            interior = m.group(1) if m else ''
            for tag in ('P1', 'P2', 'P3'):
                if re.search(r'\b' + tag + r'\b', interior):
                    findings[tag] += 1

    reviewed_date = stage_dates['reviewed']
    revised_date = stage_dates['revised']
    days_open_to_reviewed = _day_delta(date_opened, reviewed_date)
    days_reviewed_to_revised = _day_delta(reviewed_date, revised_date)
    days_revised_to_decision = _day_delta(revised_date, decision_date)

    if include_git_timestamps:
        stage_commits = _resolve_stage_commits(path, repo_root=repo_root)
    else:
        stage_commits = {
            'open': None, 'reviewed': None, 'revised': None, 'decision': None,
        }
    open_ts = stage_commits['open'][1] if stage_commits['open'] else None
    reviewed_ts = (
        stage_commits['reviewed'][1] if stage_commits['reviewed'] else None)
    revised_ts = (
        stage_commits['revised'][1] if stage_commits['revised'] else None)
    decision_ts = (
        stage_commits['decision'][1] if stage_commits['decision'] else None)
    hours_open_to_reviewed = _hour_delta(open_ts, reviewed_ts)
    hours_reviewed_to_revised = _hour_delta(reviewed_ts, revised_ts)
    hours_revised_to_decision = _hour_delta(revised_ts, decision_ts)
    stage_present = {s for s, d in stage_dates.items() if d is not None}
    stage_resolved = {
        s for s, ts in (
            ('open', open_ts), ('reviewed', reviewed_ts),
            ('revised', revised_ts), ('decision', decision_ts),
        ) if ts is not None
    }
    stage_timestamp_reliability = _stage_reliability(
        stage_present, stage_resolved)

    return {
        'stem': path.stem,
        'author': author,
        'date_opened': date_opened.isoformat() if date_opened else '',
        'status': status_token,
        'decision_date': decision_date.isoformat() if decision_date else '',
        'days_to_decision': days_to_decision,
        'review_rounds': len(review_sections),
        'reviewer_agents': '|'.join(reviewer_agents),
        'cross_agent_type_review': cross_agent_type_review,
        'external_tier_review': external_tier_review,
        'revised': revised,
        'total_findings': total_findings,
        'findings_p1': findings['P1'],
        'findings_p2': findings['P2'],
        'findings_p3': findings['P3'],
        'reviewed_date': reviewed_date.isoformat() if reviewed_date else '',
        'revised_date': revised_date.isoformat() if revised_date else '',
        'days_open_to_reviewed': days_open_to_reviewed,
        'days_reviewed_to_revised': days_reviewed_to_revised,
        'days_revised_to_decision': days_revised_to_decision,
        'hours_open_to_reviewed': hours_open_to_reviewed,
        'hours_reviewed_to_revised': hours_reviewed_to_revised,
        'hours_revised_to_decision': hours_revised_to_decision,
        'stage_timestamp_reliability': stage_timestamp_reliability,
    }


def proposal_rows(root: Path) -> List[Dict[str, object]]:
    """Every proposal row under *root*, sorted by ``date_opened`` then
    ``stem`` (deterministic order)."""
    rows = [
        extract_proposal_row(p, repo_root=root)
        for p in iter_proposal_files(root)
    ]
    rows.sort(key=lambda r: (str(r['date_opened']), str(r['stem'])))
    return rows


# --------------------------------------------------------------- plan rows


def _normalize_plan_status(value: str) -> str:
    """Normalize a free-text status to its leading enum token.
    ``archived 2026-05-14 (...)`` -> ``archived``; ``reviewed; ...`` ->
    ``review``."""
    tokens = value.split()
    if not tokens:
        return ''
    lead = tokens[0].strip(' .,;:*').lower()
    for enum in _PLAN_STATUS_ENUM:
        if lead.startswith(enum):
            return enum
    return lead


def _plan_status(text: str, sections: Sequence[Tuple[str, List[str]]]) -> str:
    """Read a plan's status from the ``**Status**:`` field, or the body
    of a ``## Status`` section for older plans."""
    field = _header_field(text, 'Status')
    if field:
        return _normalize_plan_status(field)
    for header, body in sections:
        if header.startswith('## Status'):
            for line in body:
                if line.strip():
                    return _normalize_plan_status(line.strip())
    return ''


def _proposal_slug(stem: str) -> str:
    """Drop the ``YYYY-MM-DD-<author>-`` prefix from a proposal stem,
    leaving the slug body for best-effort plan pairing.

    The author segment is a single dash-delimited token; it allows
    mixed case, digits, and underscores (``Codex``, ``Alice``,
    ``claude2``) -- not lowercase-only -- so an upper/mixed-case author
    name does not silently defeat plan<->proposal pairing.  It stays
    dash-free so the match stops at the first dash and the slug body is
    captured intact (code-review P2, Antigravity 2026-05-26)."""
    m = re.match(r'\d{4}-\d{2}-\d{2}-[A-Za-z0-9_]+-(.+)', stem)
    return m.group(1) if m else stem


def _normalize_slug(slug: str) -> str:
    """Canonicalize a slug for matching: lowercase, ``_`` -> ``-``,
    trailing ``-plan`` stripped."""
    s = re.sub(r'_', '-', slug.lower())
    return re.sub(r'-?plan$', '', s)


def extract_plan_row(
    path: Path, proposal_stems: Sequence[str] = (),
) -> Dict[str, object]:
    """Parse one plan file into a metrics row.

    ``proposal_stems`` feeds the slug-match fallback for
    ``paired_proposal``; pass the proposal corpus stems for the real
    walk, or a small set in unit tests."""
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    sections = _split_h2_sections(lines)

    status = _plan_status(text, sections)

    plan_review_rounds = 0
    code_review_rounds = 0
    for line in lines:
        if not _DATE_RE.search(line):
            continue
        if _CODE_REVIEW_HEADING_RE.match(line):
            code_review_rounds += 1
        elif _PLAN_REVIEW_HEADING_RE.match(line):
            plan_review_rounds += 1

    paired_proposal = ''
    reliability = 'none'
    source_line = _header_field(text, 'Source proposal')
    link_match = re.search(
        r'(\d{4}-\d{2}-\d{2}-[a-z0-9.-]+?)\.md', source_line)
    if link_match:
        paired_proposal = link_match.group(1)
        reliability = 'link'
    elif proposal_stems:
        slug_index = {
            _normalize_slug(_proposal_slug(s)): s for s in proposal_stems
        }
        match = slug_index.get(_normalize_slug(path.stem))
        if match:
            paired_proposal = match
            reliability = 'slug'

    return {
        'stem': path.stem,
        'status': status,
        'plan_review_rounds': plan_review_rounds,
        'code_review_rounds': code_review_rounds,
        'paired_proposal': paired_proposal,
        'paired_proposal_reliability': reliability,
    }


def plan_rows(root: Path) -> List[Dict[str, object]]:
    """Every plan row under *root*, sorted by ``stem``."""
    proposal_stems = [p.stem for p in iter_proposal_files(root)]
    rows = [
        extract_plan_row(p, proposal_stems) for p in iter_plan_files(root)
    ]
    rows.sort(key=lambda r: str(r['stem']))
    return rows


# --------------------------------------------------------------- formatting


def _csv_safe(value: object) -> str:
    """Neutralize spreadsheet formula-injection.

    A cell whose text begins with a formula trigger (``= + - @`` or a
    leading tab / carriage-return) is prefixed with a single quote so a
    spreadsheet treats it as literal text, not a formula. The metrics
    corpus is the team's own committed proposals, but in an adopter repo a
    proposal *title* (which flows into a cell) can carry untrusted
    contributor text, so the emitter neutralizes defensively
    (security-hardening, Chunk 9 / informational)."""
    s = '' if value is None else str(value)
    if s[:1] in ('=', '+', '-', '@', '\t', '\r'):
        return "'" + s
    return s


def format_csv(
    rows: Sequence[Dict[str, object]], columns: Sequence[str],
) -> str:
    """Render rows as CSV text (the default, machine-readable form).

    Data cells are passed through :func:`_csv_safe` to neutralize
    formula-injection; column headers are Cairn-defined and emitted as-is."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(columns)
    for row in rows:
        writer.writerow([_csv_safe(row.get(c, '')) for c in columns])
    return buf.getvalue()


def format_md(
    rows: Sequence[Dict[str, object]], columns: Sequence[str],
) -> str:
    """Render rows as a GitHub-flavored markdown table.  Pipe characters
    in cells are escaped so the table stays well-formed."""
    def _cell(value: object) -> str:
        return str(value).replace('|', r'\|')

    lines = [
        '| ' + ' | '.join(columns) + ' |',
        '| ' + ' | '.join('---' for _ in columns) + ' |',
    ]
    for row in rows:
        lines.append(
            '| ' + ' | '.join(_cell(row.get(c, '')) for c in columns) + ' |')
    return '\n'.join(lines) + '\n'


# -------------------------------------------------------------- entry point


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog='lifecycle_metrics',
        description=(
            'Extract lifecycle metrics from the proposal / plan corpus. '
            'Read-only; emits a derived CSV / markdown table.'
        ),
    )
    parser.add_argument(
        'kind', nargs='?', choices=['proposals', 'plans'],
        default='proposals',
        help='Which corpus to walk. Default: proposals.',
    )
    parser.add_argument(
        '--root', type=Path, default=_REPO_ROOT,
        help=f'Repo root for the dev/ corpus. Default: {_REPO_ROOT}.',
    )
    parser.add_argument(
        '--out', type=Path, default=None,
        help='Write the report to this file instead of stdout.',
    )
    parser.add_argument(
        '--format', choices=['csv', 'md'], default='csv',
        help='Output format. Default: csv.',
    )
    args = parser.parse_args(argv)

    if not args.root.is_dir():
        print(
            f'lifecycle_metrics: --root is not a directory: {args.root}',
            file=sys.stderr,
        )
        return 2

    if args.kind == 'proposals':
        rows = proposal_rows(args.root)
        columns = PROPOSAL_COLUMNS
    else:
        rows = plan_rows(args.root)
        columns = PLAN_COLUMNS

    text = (
        format_csv(rows, columns)
        if args.format == 'csv'
        else format_md(rows, columns)
    )

    if args.out is not None:
        args.out.write_text(text, encoding='utf-8')
        print(
            f'lifecycle_metrics: wrote {len(rows)} {args.kind} rows to '
            f'{args.out}',
            file=sys.stderr,
        )
    else:
        sys.stdout.write(text)

    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
