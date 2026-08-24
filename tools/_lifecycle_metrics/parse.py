# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

from __future__ import annotations

import datetime
import re
from typing import Dict, List, Optional, Sequence, Tuple

_DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')


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


# ------------------------------------------- review-pass heading grammar
#
# retire-event-blocks (2026-08-24): the accepted grammar for a review-pass
# heading, replacing the deleted `cairn-event-v1` block machinery.  A pass is
# an H2 matching, case-sensitively, one of five kind words, additionally
# carrying a ` -- `-delimited reviewer segment and an ISO date on the same
# line.  Four of the five named exclusions are structural rather than
# checked here: a bare template stub (no ` -- `), a Response or Correction
# heading (neither's own first word matches the kind group below), and an
# H3-or-deeper heading (`_split_h2_sections` never offers one as a header at
# all).  The sixth -- a Maintainer *disposition* about a pass, not a pass --
# is checked by name.
_PASS_KIND_RE = re.compile(
    r'^##\s+(Review|Plan review|Code review|Security review|Security re-review)\b'
)
_DASH_SEP = ' -- '


def _pass_kind_of(header: str) -> Optional[str]:
    """Which of the five pass kinds an H2 heading LINE names, under the
    accepted grammar, or ``None`` when it is not a dated pass at all.

    Returns the matched kind word verbatim (``'Review'``, ``'Plan
    review'``, ``'Code review'``, ``'Security review'``, or ``'Security
    re-review'``) so a caller can classify ``plan_review_rounds`` /
    ``code_review_rounds`` by exact kind without a second enum."""
    m = _PASS_KIND_RE.match(header)
    if not m:
        return None
    if _DASH_SEP not in header:
        return None
    if not _DATE_RE.search(header):
        return None
    if 'disposition' in header.lower():
        return None
    return m.group(1)


def _pass_reviewer_of(header: str) -> str:
    """Reviewer identity from a dated pass heading: the text between the
    first and second ` -- ` separator, with a trailing parenthetical role
    stripped (``## Code review -- Codex (External) -- 2026-08-21`` ->
    ``'Codex'``).  ``''`` when the heading carries no second separator to
    read between."""
    parts = header.split(_DASH_SEP)
    if len(parts) < 2:
        return ''
    return _strip_role(parts[1])


_MARKDOWN_CODE_FENCE_RE = re.compile(r'^(`{3,}|~{3,})')


def _blank_fenced_code_blocks(text: str) -> str:
    """Blank the CONTENTS of every triple-backtick/tilde fenced markdown
    code block, preserving line count and every non-blanked line verbatim
    (so line numbers and offsets within a kept line stay accurate against
    the original text).

    A proposal or plan routinely quotes another artifact's heading
    verbatim inside a fenced code block while discussing it --
    ``2026-08-10-claude-code-review-blindness`` is exactly this shape in
    Cairn's own corpus, quoting ``## Code review`` / ``## Plan review``
    examples while arguing a gate defect -- and a raw-text scan cannot
    otherwise tell that apart from a real, live pass or Response.  Applied
    before review-pass / Response section-splitting so a quoted example
    is never counted as one.  Ported from the deleted `cairn-event-v1`
    reader (`events.py`), which needed the identical guard for its own
    fence grammar."""
    lines = text.split('\n')
    out: List[str] = []
    fence_marker: Optional[str] = None
    for line in lines:
        stripped = line.strip()
        if fence_marker is None:
            m = _MARKDOWN_CODE_FENCE_RE.match(stripped)
            if m:
                fence_marker = m.group(1)[0] * len(m.group(1))
                out.append(line)
                continue
            out.append(line)
        else:
            if stripped.startswith(fence_marker):
                fence_marker = None
                out.append(line)
            else:
                out.append('')
    return '\n'.join(out)


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
