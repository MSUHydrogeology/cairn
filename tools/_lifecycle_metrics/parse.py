from __future__ import annotations

import datetime
import re
from typing import Dict, List, Optional, Sequence, Tuple

_DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
# A finding-heading bullet inside a Review section: ``* **[...`` --
# robust to the bracket interior (the corpus uses many bracket shapes).
_FINDING_BULLET_RE = re.compile(r'^\s*\*\s+\*\*\[')
# The bracket interior of a finding heading, for the severity scan.
_BRACKET_INTERIOR_RE = re.compile(r'\*\*\[([^\]]*)\]')
# A ``### ... code review`` / ``### ... plan review`` review-round
# subsection heading.  An optional single reviewer-name token before
# the phrase covers older headings (``### <reviewer> code review --
# DATE``); two tokens before the phrase (``### Response to code
# review``) is a response, not a round, and is correctly excluded.  A trailing ISO
# date is still required at the call site, so chunk labels and the
# literal ``YYYY-MM-DD`` placeholder do not count.
_CODE_REVIEW_HEADING_RE = re.compile(r'### (?:[a-z]+ )?code review\b', re.I)
_PLAN_REVIEW_HEADING_RE = re.compile(r'### (?:[a-z]+ )?plan review\b', re.I)


def _header_field(text: str, name: str) -> str:
    """Return the value of a ``**<name>**:`` header line, or ``''``.

    Matches the proposal / plan header-block convention
    (``**Author**:``, ``**Date opened**:``, ``**Status**:``,
    ``**Source proposal**:``)."""
    pattern = re.compile(r'^\*\*' + re.escape(name) + r'\*\*:\s*(.*)$', re.M)
    m = pattern.search(text)
    return m.group(1).strip() if m else ''


def _strip_role(author: str) -> str:
    """``Alice (Strategy)`` -> ``Alice``; strip the role parenthetical
    so the author column carries the agent identity only."""
    return re.split(r'\s*\(', author, maxsplit=1)[0].strip()


def _agent_of(header: str) -> str:
    """Read the reviewer / author identity token from a section header.

    Header shape: ``## Review -- <Name> (<role>) -- <date>``, or with a
    round suffix ``## Review (Round N) -- <Name> (<role>) -- <date>``.
    Strips the ``## <Word>`` prefix, a leading ``(Round N)`` annotation,
    and a leading ``--`` / em-dash separator, then takes the identity up
    to the next separator or parenthetical.  Vendor-neutral -- no
    hardcoded agent names; empty / unparseable headers map to ``''``."""
    body = re.sub(r'^#+\s*\w+\b', '', header)          # drop '## Review'
    body = re.sub(r'^\s*\([^)]*\)', '', body)          # drop a leading '(Round N)' annotation
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
