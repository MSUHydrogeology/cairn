#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Write-time claim checker -- proactive verify-before-asserting validation.

The Cairn ``claim-check`` module's reference implementation.  The
scaffold installs this script into an adopting repo's ``scripts/``
directory (verbatim -- no token substitution over code); the
``{{claim_check_command}}`` token in the adopter's ``AGENTS.md`` points
at it.  It is vendor-neutral and **standard-library only** -- nothing
here is specific to any one project's layout.

It scans a Markdown proposal / plan / doc an author is about to commit
and reports verify-before-asserting risks *before* they reach review:
the verify-before-asserting discipline is a *prompt* -- it tells an
author what to check; this checker *does* the mechanically-checkable
subset (broken repo paths, out-of-bounds line citations).

**Hard checks** -- deterministic; a failure exits non-zero:

* **Repo-path claims.**  A backticked token whose first
  ``/``-separated segment is a real top-level entry of the
  repository (a top-level directory *or* a root file -- ``AGENTS.md``,
  ``CLAUDE.md``, ...) is resolved against the tree.  A cited path
  that does not exist is a hard flag.  The top-level set is derived
  by listing the repo root, so root landmark files are first-class
  and the set never goes stale.
* **Node citations.**  A backticked ``path::node`` token -- the form
  ``doctrine/lifecycle.md`` > "Archive precondition" mandates for a
  ``guard`` disposition -- is resolved on its **path half only**.  The
  node half is **never verified**: this module does not collect tests,
  so a ``guard`` may name a node that does not exist and nothing here
  will notice.  A missing *path* is still a hard flag.
* **Line-bounds claims.**  A backticked ``path:N`` / ``path:N-M``
  token is checked: the file must exist and have at least ``M``
  lines.  An out-of-range citation is a hard flag.  This is a
  *bounds* check only -- it does NOT verify the cited lines still
  contain the rule or API being claimed.

**Soft flags** -- advisory; printed but exit 0 unless
``--fail-on-soft``.  The checker has **no active soft-flag producer**:
the category-D **count** soft-flag (a number adjacent to a tree-noun)
was **retired 2026-06-05** -- 0 catches across the verify-before-
asserting instance log, and the nag generated the ``claim-check-allow-
count`` header bloat it was meant to silence.  Numeric drift is now
governed by the three-kind precision / ``as_of`` discipline (approximate
a decision-irrelevant count, date a snapshot, register a live invariant)
and the code-side ``verify_counts`` registry, not by a write-time nag.
The ``soft_flags`` channel, the two-tuple :func:`check_text` contract,
and ``--fail-on-soft`` are retained (no behavior change for callers; the
channel simply has no producer today).  A stray
``claim-check-allow-count`` comment left in an archived doc is silently
ignored -- it matches no live directive.

**Out of scope** -- these stay reactive, caught in review:

* Code-object-shape claims ("``X`` has method ``Y``"; "returns type
  ``Z``") -- not extractable from prose at acceptable precision.
* Internal self-contradiction (two conflicting claims in one draft).
* Commit-hash / git-history claims ("commit ``X`` did ``Y``";
  "``Y`` has shipped").

**Markdown-context rule.**  Prose and Markdown table rows are
scanned; fenced code blocks, indented code blocks, HTML comments,
and blockquotes are skipped -- those carry illustrative paths
(``path/to/file.py``) and quoted historical mistakes, not live
claims.  The indented-code heuristic is deliberately conservative
(it never treats list content as code); see ``scannable_lines``.

**Marker lines / blocks.**  A scannable line that begins with one
of the three marker keywords (case-insensitive, optionally as a
list item) declares its backticked repo-path and line-bounds
tokens as deliberately unresolvable:

* ``Proposed path:`` / ``Proposed paths:`` -- a future path a
  proposal plans to create.
* ``Untracked path:`` / ``Untracked paths:`` -- a git-ignored
  path a fresh checkout will not carry.
* ``External-repo path:`` / ``External-repo paths:`` -- a path
  that resolves in a *sibling* repository, not the local tree.
  Gives cross-repo proposals / plans an escape hatch parallel to
  ``Proposed path:`` without forcing absolute-path rewrites that
  break the "backticked tokens are repo-relative" convention.

Tokens on a marker line are exempt from the hard checks.  When a
marker line is followed
immediately by a compact structured block -- Markdown table rows,
list rows, or bare backticked path-list rows -- those continuation
rows are exempt too until the next blank line, heading, or ordinary
prose line.  This is the narrow escape hatch a proposal needs to
cite paths that do not yet resolve (or never resolve locally) without
disabling path discipline.

**External-path allowance (file-scoped).**  Some files exist to
*describe other repositories* -- a ``case-studies/`` write-up of an
external project, a porting note -- and routinely cite that repo's
relative paths.  When such a path's first segment happens to collide
with a real local top-level directory name (``scripts/``, ``docs/``,
...), the hard repo-path check would false-flag it: the path is a
faithful reference to the *external* tree, not a broken local one.
The ``--external-allow GLOB`` option (repeatable) names file globs --
relative to ``--root`` -- whose backticked path-claims describe an
external repo and are therefore **not resolved against the local
tree**.  This is the file-scoped sibling of the per-line
``External-repo path:`` marker: use the marker for a stray external
path in an otherwise-local file; use ``--external-allow`` for a whole
class of files (``case-studies/*.md``) that are external by nature.
Link-checking is unaffected -- only the hard repo-path / line-bounds
resolution is skipped for matched files.

**Document-scoped exemption directive.**  An HTML-comment directive
lets a single file's author suppress specific would-be path flags
without disabling the heuristic across the rest of the document:

* ``<!-- claim-check-allow: <glob>[, <glob>...] -->`` -- a
  standalone HTML-comment line declares one or more **path-globs** as
  consciously accepted, suppressing the hard path / line-bounds flag
  on any backticked token whose path part matches one of the globs.
  The directive applies to the whole document.  Globs must be
  *specific* (R1): fully literal, or have at least two literal path
  segments before any wildcard, AND the final segment must carry a
  literal filename stem (no ``dir/sub/*`` or ``dir/sub/*.md`` -- those
  would silently exempt an entire subtree).  A too-broad glob is
  itself a hard flag and exempts nothing.  The directive exempts only
  **unresolved-path** flags (R2): a glob match on a path that
  *does* exist in the tree is ignored, so an out-of-range
  line-bounds citation into a real file still hard-flags.  Each
  suppressed token is reported in the run output for audit.

The directive is line-scoped: an HTML-comment line that *shows*
the directive (e.g. inside a paragraph quoting an example) but does
not stand alone is not parsed as live.  Use it for the legitimate
false-positive class the heuristic cannot tell from genuine drift: an
authored forward-reference the marker-line mechanism does not cover
(e.g., a single cross-document path citation).

(A retired sibling, ``<!-- claim-check-allow-count: ... -->``, once
suppressed the category-D count soft-flag.  The count soft-flag was
retired 2026-06-05; a stray ``claim-check-allow-count`` comment is now
silently ignored.)

Usage::

    python scripts/claim_check.py <file>                  # check one file
    python scripts/claim_check.py <file> --fail-on-soft    # soft flags exit non-zero too
    python scripts/claim_check.py <file> --root <dir>      # override the repo root
    python scripts/claim_check.py <file> \\
        --external-allow 'case-studies/*.md'               # treat matches as external

Exit codes: ``0`` clean (or only soft flags without
``--fail-on-soft``); ``1`` at least one hard flag (or a soft flag
under ``--fail-on-soft``); ``2`` usage error (file not found).

Reference implementation for Cairn's ``claim-check`` default-on
module.
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]

# A backticked span.  Group 1 is the token text.
_BACKTICK_RE = re.compile(r'`([^`\n]+)`')

# A line-bounds citation: ``path:N`` or ``path:N-M``.
_LINE_CITATION_RE = re.compile(
    r'^(?P<path>[^:\s]+):(?P<start>\d+)(?:-(?P<end>\d+))?$'
)

# Placeholder / glob characters: a token carrying any of these is
# illustrative (``dev/proposals/<slug>.md``, ``examples/*/ws/``),
# never a live claim.
_PLACEHOLDER_CHARS = ('<', '>', '*', '{', '}')

# A marker line: a line that explicitly declares its backticked
# repo-path / line-bounds tokens as deliberately unresolvable.
# Three marker keywords:
#   * ``Proposed path:`` cites a future path a proposal plans to create.
#   * ``Untracked path:`` cites a git-ignored path a fresh checkout will
#     not carry.
#   * ``External-repo path:`` cites a path that resolves in a sibling
#     repository (e.g., a path in another repo checked out alongside
#     this one).  Added 2026-05-21 per the accepted cairn-doctrine-sync-
#     may-19-21 plan's Chunk 0 (plan-design choice resolving the F4
#     residual claim_check problem).
# Any keyword -- singular or plural, any case, optionally as a list
# item -- exempts the line's path / line-bounds tokens from the hard
# checks.  This is R8 of the work-
# intents proposal (``2026-05-19-codex-local-claim-system``) plus the
# 2026-05-21 External-repo paths extension.
_MARKER_LINE_RE = re.compile(
    r'^\s*(?:(?:[-*+]|\d+[.)])\s+)?'
    r'(?:proposed|untracked|external-repo)\s+paths?:',
    re.IGNORECASE,
)

# Document-scoped path-exemption directive.  A standalone HTML-comment
# line `<!-- claim-check-allow: <glob>[, <glob>...] -->` declares one
# or more globs as consciously accepted; any backticked token whose
# path part matches one is exempt from the hard path / line-bounds
# checks.  The directive must stand alone on its line -- comment lines
# that merely *show* the syntax are not parsed as live directives.
_ALLOW_DIRECTIVE_RE = re.compile(
    r'^<!--\s*claim-check-allow:\s*(?P<globs>.*?)\s*-->$'
)
_GLOB_WILDCARD_CHARS = ('*', '?', '[')

# Note: the category-D count soft-flag and its sibling document-scoped
# `claim-check-allow-count` directive were retired 2026-06-05 (0 catches
# across the verify-before-asserting instance log; the nag generated the
# header bloat it was meant to silence).  No `_ALLOW_COUNT_DIRECTIVE_RE`
# remains, so a stray `claim-check-allow-count` comment matches no live
# directive and is silently ignored.


@dataclass
class Flag:
    """One claim-check finding."""

    line: int
    kind: str        # 'path' | 'line-bounds' | 'directive'
    severity: str    # 'hard' | 'soft'
    token: str
    message: str


@dataclass
class CheckResult:
    """The hard + soft flags found in one file."""

    path: Path
    hard_flags: list[Flag] = field(default_factory=list)
    #: Retained for the historical two-tuple contract; the only soft-flag
    #: producer (the category-D count flag) was retired 2026-06-05, so
    #: this list is currently always empty.
    soft_flags: list[Flag] = field(default_factory=list)
    #: ``(token, glob)`` for each would-be-hard path / line-bounds flag
    #: suppressed by a valid ``claim-check-allow`` directive glob.
    exempted: list[tuple[str, str]] = field(default_factory=list)


def _strip_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """Remove ``<!-- ... -->`` spans from *line*.

    Returns the comment-free text plus whether an unclosed comment
    runs past the end of the line.
    """
    out: list[str] = []
    i, n = 0, len(line)
    while i < n:
        if in_comment:
            end = line.find('-->', i)
            if end == -1:
                return ''.join(out), True
            i, in_comment = end + 3, False
        else:
            start = line.find('<!--', i)
            if start == -1:
                out.append(line[i:])
                return ''.join(out), False
            out.append(line[i:start])
            i, in_comment = start + 4, True
    return ''.join(out), in_comment


def scannable_lines(text: str) -> list[tuple[int, str]]:
    """Return ``(1-based line number, scannable text)`` for prose lines.

    Fenced and indented code blocks, HTML comments, and blockquotes
    are dropped -- they carry illustrative paths and quoted
    historical mistakes, not live claims.  Prose and Markdown table
    rows are kept.

    The indented-code heuristic is conservative: a line counts as
    indented code only when it is indented >= 4 columns, is preceded
    by a blank line (or continues an open code run), and is *not*
    inside a list -- list context stays open until a flush-left,
    non-marker line (a heading or paragraph) closes it.  This never
    misclassifies list-continuation text as code; at worst it scans
    a rare indented block that abuts a list, which only risks a
    flag, never a silent miss.
    """
    out: list[tuple[int, str]] = []
    in_fence = False
    in_html_comment = False
    in_indent_code = False
    list_active = False
    prev_blank = True
    for idx, raw in enumerate(text.split('\n'), start=1):
        line = raw.expandtabs(4)

        # --- fenced code block ---
        if re.match(r'^ {0,3}(```|~~~)', line):
            in_fence = not in_fence
            in_indent_code = False
            prev_blank = False
            continue
        if in_fence:
            in_indent_code = False
            prev_blank = False
            continue

        # --- HTML comments (may open / close mid-line or span lines) ---
        work, in_html_comment = _strip_html_comments(line, in_html_comment)

        indent = len(work) - len(work.lstrip(' '))
        stripped = work.strip()

        # --- blank line (or a line that was wholly an HTML comment) ---
        if stripped == '':
            prev_blank = True
            continue

        # --- blockquote ---
        if re.match(r'^ {0,3}>', work):
            in_indent_code = False
            prev_blank = False
            continue

        # --- list tracking (gates the indented-code heuristic) ---
        if re.match(r'^ *([-*+]|\d+[.)])\s', work):
            list_active = True
        elif indent == 0:
            # a flush-left heading / paragraph / table row closes
            # any open list context.
            list_active = False

        # --- indented code block (only outside lists) ---
        if in_indent_code:
            if indent >= 4:
                prev_blank = False
                continue
            in_indent_code = False
        elif not list_active and indent >= 4 and prev_blank:
            in_indent_code = True
            prev_blank = False
            continue

        out.append((idx, work))
        prev_blank = False
    return out


def repo_top_level(repo_root: Path) -> set[str]:
    """The set of real top-level entry names of the repository.

    Both directories and root files (``AGENTS.md``, ``CLAUDE.md``,
    ...).  A backticked token is a repo-path claim only when its
    first ``/``-separated segment is in this set, so the classifier
    never goes stale as the tree changes.

    **Dot-entries are excluded** (``.git`` and friends).  A cited
    ``.git/hooks/pre-commit`` is a VCS / runtime artifact, not a content
    path claim, and every checkout carries a ``.git``; resolving against
    it would false-flag such citations.  Trade-off: a claim into a
    *tracked* dotfolder (e.g. a future ``.github/``) is skipped rather
    than validated -- accepted to stay robust against ``.git/`` false
    positives.
    """
    if not repo_root.is_dir():
        return set()
    return {
        item.name for item in repo_root.iterdir()
        if not item.name.startswith('.')
    }


def _is_placeholder(token: str) -> bool:
    """A token that is illustrative, not a live claim."""
    return ' ' in token or any(ch in token for ch in _PLACEHOLDER_CHARS)


def _is_marker_line(text: str) -> bool:
    """True for a ``Proposed path:`` / ``Untracked path:`` marker line.

    A marker line's backticked repo-path and line-bounds tokens are
    deliberate forward / out-of-tree references -- exempt from the
    hard checks.  See ``_MARKER_LINE_RE`` and the module docstring's
    "Marker lines" paragraph.
    """
    return _MARKER_LINE_RE.match(text) is not None


def _is_marker_block_continuation(text: str) -> bool:
    """True for structured rows governed by a preceding marker line.

    Marker blocks intentionally stay narrow: table rows, list rows,
    and bare backticked path-list rows are allowed; headings and
    ordinary prose are not.  Blank lines are handled by ``check_text``
    via line-number adjacency because ``scannable_lines`` omits them.
    """
    stripped = text.strip()
    if not stripped or stripped.startswith('#'):
        return False
    if stripped.startswith('|'):
        return True
    if re.match(r'^([-*+]|\d+[.)])\s+', stripped):
        return True
    return stripped.startswith('`')


#: Standard framework runtime paths that are *gitignored or generated by
#: design* -- created at run time (or supplied per-adopter), never committed,
#: so they are legitimately absent from a clean checkout / fresh scaffold and
#: must never hard-flag, even though their first segment (``dev``) is a real
#: top-level dir.  Docs across the tree reference them (the work-intent log
#: appears in the onboarding doc, the concurrent presets, and the rendered
#: PLANNING slot; once a project *self-hosts* Cairn its own doctrine /
#: templates / changelog cite the machine-state tree too), so a per-document
#: exemption directive would not scale and would break on every fresh clone
#: (fold-back #42).  Scoped tightly: the *committed* lockfile / profile /
#: mapping under ``dev/.cairn/`` are NOT here -- they resolve and stay
#: checkable; only the generated / per-adopter-optional state is exempt.
#: Each entry is a *framework-defined* path the doctrine / modules reference
#: across many files but that a fresh scaffold does not contain -- a gitignored
#: runtime log, a per-adopter-optional config, or a doc file created on first
#: use.  Exact entries are safe by construction: a typo never collides with a
#: full literal path, so the gate stays sharp for real broken cites.  These are
#: framework paths *every* adopter that installs the relevant module may carry,
#: which is why they belong in the shipped tool, not in per-document directives.
_DEFAULT_EXEMPT_PATHS: frozenset[str] = frozenset({
    "dev/intents.jsonl",                        # work-intent log (gitignored)
    "dev/intent-config.json",                   # work-intent config (legacy path)
    "dev/.cairn/local-env.json",                # interpreter binding (gitignored)
    "dev/.cairn/intent-config.json",            # work-intent config (canonical)
    "dev/.cairn/metrics-config.json",           # lifecycle-metrics config (optional)
    "dev/.cairn/foldback_export_denylist.txt",  # foldback export-scan denylist (optional)
    "dev/measurement/incident_log.md",          # incident-trackers log (created on first use)
    "dev/measurement/collision_log.md",         # coordination collision log (created on first use)
    "dev/measurement/coordination_log.md",      # coordination event log (created on first use)
    "dev/measurement/coordination_incidents.md",  # coordination-incident log (created on first use)
    "dev/rules/custom_session_routines.md",     # optional adopter session-routine hooks
    "dev/vision.md",                            # optional project vision/charter home
})

#: Framework machine-state *directory prefixes*: generated / transient trees a
#: fresh scaffold does not contain, so a citation of the dir (or anything under
#: it) is not a broken claim.  Matching is ``/``-terminated -- a prefix exempts
#: the dir itself and its subpaths but NOT a sibling whose name merely *starts
#: with* it (``dev/.cairn-upgrade-bak`` is not exempted by
#: ``dev/.cairn-upgrade/``), and the exact set above is untouched (so
#: ``dev/intents.jsonl.bak`` is never exempted by ``dev/intents.jsonl``).
#: Scoped to generated subtrees -- never ``dev/`` or ``dev/.cairn/`` broadly,
#: so the committed lockfile / profile / mapping stay checkable.
_DEFAULT_EXEMPT_PREFIXES: tuple[str, ...] = (
    "dev/.cairn/base/",          # upgrade base cache (generated)
    "dev/.cairn-upgrade/",       # transient upgrade staging tree
    "dev/measurement/snapshots/",  # dated metrics CSV snapshots (generated)
)


def _is_default_exempt(token: str) -> bool:
    """True when *token* is a default-exempt framework runtime path: an exact
    member of ``_DEFAULT_EXEMPT_PATHS``, or at/under a ``/``-terminated
    ``_DEFAULT_EXEMPT_PREFIXES`` directory."""
    if token in _DEFAULT_EXEMPT_PATHS:
        return True
    norm = token.rstrip('/')
    return any(
        norm == p.rstrip('/') or norm.startswith(p.rstrip('/') + '/')
        for p in _DEFAULT_EXEMPT_PREFIXES
    )


def _node_citation_path(token: str) -> str | None:
    """The path half of a ``path::node`` citation, or ``None``.

    ``path::node`` is the citation form ``doctrine/lifecycle.md`` >
    "Archive precondition" mandates for a ``guard`` disposition -- the
    follow-up is homed in something that *executes*, and the entry names
    the node.  Only the **path** half is resolvable here: a static
    checker does not collect tests, so **the node half is never
    verified**.  A ``guard`` may cite a node that does not exist and
    nothing in this module notices.

    Splits on the *first* ``::`` (pytest node ids nest:
    ``t.py::Class::test``).  A token with an empty path half (``::x``) or
    an empty node half (``t.py::``) is not a node citation and falls
    through to the ordinary path check.
    """
    path_part, sep, node = token.partition('::')
    if sep and node and path_part:
        return path_part
    return None


def check_path_token(
    token: str, lineno: int, repo_root: Path, top_level: set[str],
) -> Flag | None:
    """Hard-check a backticked token that classifies as a repo path.

    Returns a hard flag when the token's first segment is a real
    top-level entry but the full path does not resolve; ``None`` when
    the token is not a repo-path claim, is a default-exempt runtime
    path, or resolves cleanly.
    """
    node_path = _node_citation_path(token)
    target = token if node_path is None else node_path
    first = target.split('/', 1)[0]
    if first not in top_level:
        return None  # not a repo-path claim -- nothing to check
    if _is_default_exempt(target):
        return None  # gitignored / generated framework runtime path; absent by design
    resolved = repo_root / target
    # A node citation names a test node, which lives in a FILE -- a
    # directory path half (``bootstrap/tests::test_x``) is not a valid
    # ``path::node`` and must still flag.  The bare-path branch keeps
    # ``.exists()``, because a directory IS a legitimate path claim.
    # Mirrors the line-bounds branch, which is ``.is_file()`` for the
    # same reason.
    if resolved.is_file() if node_path is not None else resolved.exists():
        return None
    return Flag(
        lineno, 'path', 'hard', token,
        f'cited path does not resolve: `{token}`',
    )


def check_line_citation(
    token: str, lineno: int, repo_root: Path, top_level: set[str],
) -> Flag | None:
    """Hard-check a backticked ``path:N`` / ``path:N-M`` line citation.

    A *bounds* check: the file must exist and have at least the cited
    line count.  It makes no claim about the cited lines' content.
    Returns ``None`` when the token is not a line citation, is not a
    repo path, or is within bounds.
    """
    match = _LINE_CITATION_RE.match(token)
    if match is None:
        return None
    path = match.group('path')
    if path.split('/', 1)[0] not in top_level:
        return None  # not a repo path -- not this checker's concern
    target = repo_root / path
    if not target.is_file():
        return Flag(
            lineno, 'line-bounds', 'hard', token,
            f'line-bounds citation to a missing file: `{token}`',
        )
    end = int(match.group('end') or match.group('start'))
    # Count lines by streaming the file rather than reading it whole --
    # a citation may point into a large data file / log present in the
    # repo, and only the line count is needed.
    with target.open(encoding='utf-8', errors='replace') as fh:
        n_lines = sum(1 for _ in fh)
    if end > n_lines:
        return Flag(
            lineno, 'line-bounds', 'hard', token,
            f'line-bounds citation `{token}` exceeds {path} '
            f'({n_lines} lines)',
        )
    return None


def parse_allow_directives(text: str) -> list[tuple[int, str]]:
    """Return ``(lineno, glob)`` for every glob declared in a
    document-scoped ``<!-- claim-check-allow: <glob>[, ...] -->``
    directive.  Globs are comma-separated; empty entries are skipped.
    """
    out: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.split('\n'), start=1):
        m = _ALLOW_DIRECTIVE_RE.match(line.strip())
        if m is None:
            continue
        for raw in m.group('globs').split(','):
            glob = raw.strip().strip('`').strip()
            if glob:
                out.append((lineno, glob))
    return out


def allow_glob_error(glob: str) -> str | None:
    """Reject a too-broad ``claim-check-allow`` glob (R1).

    Acceptable when the glob is **fully literal** (no wildcard) or has
    **>= 2 literal path segments before its first wildcard** -- so it
    cannot exempt a whole top-level directory (``dev/*``, ``scripts/*``)
    or everything (``*``).  Returns an error message, or ``None`` when
    the glob is acceptable.  (Note: a "N literal chars before a
    wildcard" rule would NOT reject ``dev/*``; the segment rule does.)

    Additional rule: the **final path segment must carry a literal
    filename stem** -- a wildcard-leading final segment (``.../*``,
    ``.../**``, ``.../*.md``) would exempt every broken path in that
    subtree even though it clears the >= 2-segment rule.
    """
    first_wild = next(
        (i for i, ch in enumerate(glob) if ch in _GLOB_WILDCARD_CHARS),
        None,
    )
    if first_wild is None:
        return None  # fully literal -- specific by construction
    literal_prefix = glob[:first_wild]
    segments = [s for s in literal_prefix.split('/') if s]
    if len(segments) < 2:
        return (
            f'claim-check-allow glob `{glob}` is too broad: a wildcard '
            f'must be preceded by at least two literal path segments '
            f'(or the glob must be a fully-literal path), so it cannot '
            f'exempt a whole top-level directory'
        )
    final_segment = glob.split('/')[-1]
    if not final_segment or final_segment[:1] in _GLOB_WILDCARD_CHARS:
        return (
            f'claim-check-allow glob `{glob}` is too broad: its final path '
            f'segment is a bare wildcard, so it would exempt a whole '
            f'directory; give a literal filename stem '
            f'(e.g. `dir/sub/name*.ext`) or a fully-literal path'
        )
    return None


def _token_path_part(token: str) -> str:
    """The path portion of a token, dropping a ``:N`` / ``:N-M``
    line-bounds suffix, for glob matching."""
    m = _LINE_CITATION_RE.match(token)
    return m.group('path') if m else token


def _scan(
    text: str, repo_root: Path, *, external_allowed: bool = False,
) -> tuple[list[Flag], list[Flag], list[tuple[str, str]]]:
    """Core scan -- returns ``(hard, soft, exempted)``.

    A would-be-hard path / line-bounds flag whose token matches a valid
    ``claim-check-allow`` glob (and whose path does NOT resolve locally)
    is suppressed and recorded in ``exempted`` as ``(token, glob)``.  A
    *too-broad* glob is itself a hard flag and exempts nothing.

    ``soft`` is always empty: the only soft-flag producer (the category-D
    count flag) was retired 2026-06-05.  The list is kept so the
    historical two-tuple :func:`check_text` contract is unchanged.

    Raises ``NotADirectoryError`` when *repo_root* is not a directory --
    fail-closed, since an unresolvable root would read every repo path
    as "not a claim" and silently report a false clean result.
    """
    if not repo_root.is_dir():
        raise NotADirectoryError(
            f'claim_check: repo root is not a directory: {repo_root}'
        )
    top_level = repo_top_level(repo_root)

    # Document-scoped exemption globs (validated; bad ones hard-flag).
    allow_globs: list[str] = []
    hard: list[Flag] = []
    for lineno, glob in parse_allow_directives(text):
        err = allow_glob_error(glob)
        if err is not None:
            hard.append(Flag(lineno, 'directive', 'hard', glob, err))
        else:
            allow_globs.append(glob)

    # ``soft`` has no producer since the category-D count flag was
    # retired; kept for the historical two-tuple ``check_text`` contract.
    soft: list[Flag] = []
    exempted: list[tuple[str, str]] = []
    in_marker_block = False
    prev_lineno: int | None = None
    for lineno, line in scannable_lines(text):
        marker_line = _is_marker_line(line)
        contiguous = prev_lineno is not None and lineno == prev_lineno + 1
        marker_continuation = (
            in_marker_block
            and contiguous
            and _is_marker_block_continuation(line)
        )
        if not (marker_line or marker_continuation or external_allowed):
            for match in _BACKTICK_RE.finditer(line):
                token = match.group(1).strip()
                if not token or _is_placeholder(token):
                    continue
                if _LINE_CITATION_RE.match(token):
                    flag = check_line_citation(
                        token, lineno, repo_root, top_level)
                else:
                    flag = check_path_token(
                        token, lineno, repo_root, top_level)
                if flag is not None:
                    path_part = _token_path_part(token)
                    matched = next(
                        (g for g in allow_globs
                         if fnmatch.fnmatchcase(path_part, g)),
                        None,
                    )
                    # The document-scoped directive exempts only
                    # *unresolved-path* flags (the external / proposed
                    # case it exists for).  It must NOT silence a failure
                    # on a path that exists locally -- e.g. an out-of-range
                    # line-bounds citation into a real file, which is
                    # exactly the stale-anchor class claim_check is meant
                    # to catch.
                    resolves = (repo_root / path_part).exists()
                    if matched is not None and not resolves:
                        exempted.append((token, matched))
                    else:
                        hard.append(flag)
        in_marker_block = marker_line or marker_continuation
        prev_lineno = lineno
    return hard, soft, exempted


def check_text(
    text: str, repo_root: Path, *, external_allowed: bool = False,
) -> tuple[list[Flag], list[Flag]]:
    """Scan *text* and return ``(hard_flags, soft_flags)``.

    A thin wrapper over :func:`_scan` preserving the historical
    two-tuple contract.  The document-scoped ``claim-check-allow``
    exemptions (and the report of which tokens they cleared) are
    surfaced through :class:`CheckResult` via :func:`check_file`.

    Raises ``NotADirectoryError`` when *repo_root* is not a
    directory.  An unresolvable root yields an empty top-level set,
    which makes every backticked repo path read as "not a claim" --
    the scan would silently no-op and report a false clean result.
    The checker fails closed instead.

    ``external_allowed`` (the file-scoped external-path allowance, set
    by the caller from ``--external-allow`` globs): when True, the hard
    repo-path / line-bounds resolution is skipped for this file -- it
    describes an external repo whose relative paths must not be resolved
    against the local tree.
    """
    hard, soft, _exempted = _scan(
        text, repo_root, external_allowed=external_allowed,
    )
    return hard, soft


def file_is_external(
    path: Path, repo_root: Path, external_allow: list[str],
) -> bool:
    """True when *path* matches one of the ``external_allow`` globs.

    Globs are matched against the file's path relative to *repo_root*
    (POSIX-style, so ``case-studies/*.md`` matches regardless of OS).
    A path outside *repo_root* (or an unresolvable one) is matched
    against its bare name as a fallback so an explicitly-listed file
    still resolves.
    """
    if not external_allow:
        return False
    try:
        rel = path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        rel = path.name
    return any(
        fnmatch.fnmatch(rel, glob) or fnmatch.fnmatch(path.name, glob)
        for glob in external_allow
    )


def check_file(
    path: Path, repo_root: Path, *, external_allow: list[str] | None = None,
) -> CheckResult:
    """Run the checker against one file.

    ``external_allow`` is the list of file globs whose path-claims
    describe external repos (see ``check_text``); when *path* matches
    one, the hard repo-path / line-bounds resolution is skipped.

    The result also carries any path tokens suppressed by the
    document-scoped ``claim-check-allow`` directive (``exempted``), so
    the run can report exactly which would-be-flags were waived for audit.
    """
    external = file_is_external(path, repo_root, external_allow or [])
    text = path.read_text(encoding='utf-8', errors='replace')
    hard, soft, exempted = _scan(
        text, repo_root, external_allowed=external,
    )
    return CheckResult(
        path=path, hard_flags=hard, soft_flags=soft, exempted=exempted,
    )


def _format_flag(rel: Path, flag: Flag) -> str:
    return f'  {rel}:{flag.line}: [{flag.kind}] {flag.message}'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='claim_check',
        description=(
            'Write-time verify-before-asserting claim checker.  '
            'Hard-flags broken repo paths and out-of-bounds line '
            'citations.'
        ),
    )
    parser.add_argument(
        'file', type=Path, help='Markdown file to check.')
    parser.add_argument(
        '--root', type=Path, default=_REPO_ROOT,
        help=f'Repo root for path resolution. Default: {_REPO_ROOT}.',
    )
    parser.add_argument(
        '--fail-on-soft', action='store_true',
        help='Exit non-zero on soft flags too -- author / pre-commit '
             'use.  (Retained for contract stability; there is no active '
             'soft-flag producer since the count flag was retired.)',
    )
    parser.add_argument(
        '--external-allow', action='append', default=None, metavar='GLOB',
        help='File glob (relative to --root) whose backticked path-claims '
             'describe an EXTERNAL repo and are not resolved against the '
             'local tree (repeatable). Example: case-studies/*.md.',
    )
    args = parser.parse_args(argv)

    if not args.file.is_file():
        print(f'claim_check: not a file: {args.file}', file=sys.stderr)
        return 2
    if not args.root.is_dir():
        print(
            f'claim_check: --root is not a directory: {args.root}',
            file=sys.stderr,
        )
        return 2

    result = check_file(
        args.file, args.root, external_allow=args.external_allow,
    )

    rel: Path = args.file
    try:
        rel = args.file.resolve().relative_to(args.root.resolve())
    except ValueError:
        pass

    if result.hard_flags:
        print(
            f'claim_check: {rel} -- {len(result.hard_flags)} hard '
            f'flag(s):',
            file=sys.stderr,
        )
        for flag in result.hard_flags:
            print(_format_flag(rel, flag), file=sys.stderr)
    if result.soft_flags:
        print(
            f'claim_check: {rel} -- {len(result.soft_flags)} soft '
            f'flag(s) (must resolve or consciously accept):'
        )
        for flag in result.soft_flags:
            print(_format_flag(rel, flag))
    if result.exempted:
        # Name the exact exempted tokens (not just a count) on STDOUT --
        # the primary success artifact -- so an exemption stays auditable
        # even in tooling that captures only stdout on an otherwise-clean
        # (exit 0) run.
        print(
            f'claim_check: {rel} -- {len(result.exempted)} path(s) '
            f'exempted by claim-check-allow:'
        )
        for token, glob in result.exempted:
            print(
                f'  {rel}: exempted `{token}` via claim-check-allow '
                f'glob `{glob}`'
            )
    if not result.hard_flags and not result.soft_flags:
        print(f'claim_check: {rel} -- OK, no claim-check flags.')

    if result.hard_flags:
        return 1
    if result.soft_flags and args.fail_on_soft:
        return 1
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
