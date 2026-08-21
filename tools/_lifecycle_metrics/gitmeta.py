# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import AbstractSet, Dict, List, Optional, Tuple

from .config import _REPO_ROOT


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
    ('reviewed', re.compile(r'^Review\b(?!-)(?!.*\bsharpening\b)', re.I)),
]


_STAGE_SCOPE_PREFIX_RE = re.compile(r'^(?:dev/)?proposals?\s*:\s*', re.I)

_STAGE_PHRASE_SEP_RE = re.compile(r'\s+(?:--|–|—)\s+')

#: Consulted ONLY for a subject carrying the scope prefix above.  The
#: looser word-boundary forms are safe there and unsafe anywhere else.
_SCOPED_STAGE_PATTERNS: List[Tuple[str, 're.Pattern[str]']] = [
    ('open', re.compile(r'^open(?:ing)?\b', re.I)),
    ('decision', re.compile(
        r'^(?:maintainer\s+)?decision\b'
        r'|(?<!-)\bmaintainer\s+decision\b(?!-)', re.I)),
    ('revised', re.compile(
        r'(?<!-)\b(?:response|responses|revised|revise|respond\s+to)\b(?!-)',
        re.I)),
    ('reviewed', re.compile(r'(?<!-)\breview\b(?!-)', re.I)),
]

_HEAD_ANCHORED_STAGES = frozenset({'open', 'decision'})


def _stage_for_subject(subject: str) -> Optional[str]:
    """Classify a commit subject as AT MOST ONE lifecycle stage."""
    text = subject.strip()
    for stage, pattern in _STAGE_COMMIT_PATTERNS:   # shipped, unchanged
        if pattern.match(text):
            return stage
    match = _STAGE_SCOPE_PREFIX_RE.match(text)
    if match is None:
        return None
    body = text[match.end():]
    parts = _STAGE_PHRASE_SEP_RE.split(body, maxsplit=1)
    phrase = parts[1] if len(parts) > 1 else body
    for stage, pattern in _SCOPED_STAGE_PATTERNS:
        target = body if stage in _HEAD_ANCHORED_STAGES else phrase
        if pattern.search(target):
            return stage
    return None


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
        stage = _stage_for_subject(subject)
        if stage is not None and out[stage] is None:
            out[stage] = (sha, ts)
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


def _get_head_commit(*, repo_root: Optional[Path] = None) -> str:
    """Return the short SHA of ``HEAD`` in the repo at ``repo_root``, or
    ``''`` when git is unavailable / the path isn't a git checkout.  Used
    to anchor a snapshot's ``corpus_commit`` column to the state it
    measured (a reproducibility contract)."""
    import subprocess
    root = repo_root if repo_root is not None else _REPO_ROOT
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            cwd=str(root), capture_output=True, timeout=10, check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ''
    if result.returncode != 0:
        return ''
    return result.stdout.decode('utf-8', errors='replace').strip()
