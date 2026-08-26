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

**Lifecycle archive resolution.**  A backticked token naming a
*missing* active lifecycle file in exactly one of these two forms:

* ``dev/proposals/<file>.md``; or
* ``dev/plans/<file>.md``,

is also checked against its exact same-family sibling under
``archive/`` (``dev/proposals/archive/<file>.md`` /
``dev/plans/archive/<file>.md``).  If that exact archived file
exists, it becomes the resolution target -- for the path-exists check
and, for a ``path:N`` / ``path:N-M`` citation, for the line-bounds
check too, which is checked against the **archived** file's actual
line count.  Moving a file to ``archive/`` does not waive a stale
line bound.

This is an identity rule, not a fuzzy search: it never searches by
partial stem, date, or author; it never crosses between the proposal
and plan families; and it never applies outside these two
directories.  The active path is always authoritative when it
exists.  When **both** the active file and its archived sibling exist
at once, that is a lifecycle-state violation this checker refuses to
silently normalize: it hard-flags rather than guess which candidate
is live.  The retired planner's ``scan`` once owned the
repository-state invariant (the same filename may not exist both
actively and archived within one family); this is claim-check's own
defense in depth when *consuming* a token that names one, per the
accepted ``claim-check-exemption-hygiene`` proposal (Section 1 /
Revision 1).

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
  *specific*: fully literal, or have at least two literal path
  segments before any wildcard, AND the final segment must carry a
  literal filename stem (no ``dir/sub/*`` or ``dir/sub/*.md`` -- those
  would silently exempt an entire subtree).  A too-broad glob is
  itself a hard flag and exempts nothing.  The directive exempts only
  **unresolved-path** flags: a glob match on a path that
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

**The typed-declaration registry (document-wide, exact).**  A marker
block is also a small **document registry**: each exact backticked path
*listed* in the block may recur anywhere else in the same document
without needing a second, document-wide HTML directive.  Registry
entries are **literal paths, never globs**, they exempt only the
**exact** path (never a sibling, a descendant, or a look-alike prefix),
and every token the registry exempts is reported together with the
declaration that authorized it.

What counts as an entry:

* on the **marker line itself**, every backticked token (the compact
  ``Proposed paths: `a.md`, `b.md``` form); and
* on a **continuation row**, the row's *first* backticked token only --
  a list or table row lists one path and then explains it, so a path
  named later in that row's prose is a reference, not a second
  declaration.

A token carrying a placeholder (``<slug>``, a brace) declares nothing --
it is an illustrative form, exactly as elsewhere in this checker.  A
path-shaped token carrying a **glob wildcard** is *malformed*: the
registry is literal by contract, so the entry grants no document-wide
authority (fail closed).  A path declared **twice inside one block** is
a duplicate and likewise grants nothing.  The same path declared in two
*different* blocks is not a duplicate -- an append-only record whose
revision section restates its proposed paths is doing the right thing.

**Liveness (lifecycle artifacts only).**  An exemption is meant to be
temporary debt, so on a **non-terminal proposal or plan** -- a file at
exactly ``dev/proposals/<name>.md`` or ``dev/plans/<name>.md`` (a
``_``-prefixed authoring template is not an artifact) -- each declaration
must still be doing work:

* a typed registry entry must authorize at least one exemption
  **outside its own block**; an entry whose path has materialized (or
  which nothing outside the block cites) is a hard finding;
* a ``claim-check-allow`` glob that suppresses at least one report is
  ``effective``; one that suppresses nothing is ``unused`` -- a hard
  directive finding.

Two classes are deliberately **non-failing migration diagnostics**
rather than hard findings, because their staleness was created by this
mechanism landing and not by the artifact's author:

* ``resolved-by-archive`` -- every occurrence the glob used to suppress
  now resolves through the exact lifecycle archive rule above; and
* ``resolved-by-registry`` -- every such occurrence is now authorized by
  a typed registry entry in the same document.

Each is reported with the artifact, the directive line, the glob, and
what now resolves it, so the migration that retires it has an exact
inventory -- and it exits clean.

**Grandfathering follows immutability, not directory.**  Liveness never
changes the exit code for an artifact nobody may rewrite: any file under
``dev/proposals/archive/`` or ``dev/plans/archive/``, a proposal whose
status is ``accepted`` / ``rejected`` / ``superseded``, or a plan whose
status is ``archived``.  Those still *receive* the diagnostics.  The
status is parsed strictly -- exactly one ``**Status**: <value>`` line in
the artifact's header (above its first ``##`` heading), naming a
terminal value -- and anything else (missing, duplicated, unrecognized)
**fails closed into liveness** rather than silently inheriting the
grandfather.

Every other Markdown surface -- doctrine, strategy, modules, the
changelog, templates, examples -- keeps its existing behavior: the
registry works there, and liveness does not run.  Those surfaces have
different mutability rules and are out of this contract's scope by
declaration.

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
#     may-19-21 plan's Chunk 0 (plan-design choice resolving the
#     residual claim_check problem).
# Any keyword -- singular or plural, any case, optionally as a list
# item -- exempts the line's path / line-bounds tokens from the hard
# checks.  This is a requirement of the work-
# intents proposal (``2026-05-19-codex-local-claim-system``) plus the
# 2026-05-21 External-repo paths extension.
_MARKER_LINE_RE = re.compile(
    r'^\s*(?:(?:[-*+]|\d+[.)])\s+)?'
    r'(?P<kind>proposed|untracked|external-repo)\s+paths?:',
    re.IGNORECASE,
)

#: Display form for each marker keyword, used when a report names the
#: declaration that authorized an exemption.
_MARKER_KIND_LABEL = {
    'proposed': 'Proposed paths',
    'untracked': 'Untracked paths',
    'external-repo': 'External-repo paths',
}

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
    kind: str        # 'path' | 'line-bounds' | 'directive' | 'declaration'
    #: ``'hard'`` (non-zero exit) | ``'soft'`` (advisory, no producer today)
    #: | ``'info'`` (a non-failing diagnostic -- migration items and the
    #: liveness reports a grandfathered artifact receives without failing).
    severity: str
    token: str
    message: str


@dataclass(frozen=True)
class Declaration:
    """One typed path declaration -- an entry in a document's registry.

    ``kind`` is the marker keyword (``'proposed'`` / ``'untracked'`` /
    ``'external-repo'``), ``path`` the exact literal repo-relative path as
    written, ``line`` the row that declared it, and ``block`` the line
    number of the governing marker line (so "an occurrence outside its own
    block" is decidable, and two blocks declaring the same path are not
    duplicates).
    """

    line: int
    block: int
    kind: str
    path: str
    #: True when the governing marker line has at least one continuation
    #: row -- i.e. the declaration is part of a *registry block*, the form
    #: the liveness obligation is written for.  A standalone marker line
    #: ("Proposed path: `x` -- because ...", mid-prose) is the mechanism's
    #: original line-local use: it exempts its own line and there is
    #: nothing about it to retire, so it carries no liveness obligation.
    registry_block: bool = False

    @property
    def label(self) -> str:
        """How a report names this declaration (exact reporting)."""
        kind = _MARKER_KIND_LABEL.get(self.kind, self.kind)
        return f'`{kind}:` declaration of `{self.path}` (line {self.line})'


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
    #: ``(token, declaration label)`` for each would-be-hard flag
    #: suppressed by a typed registry declaration -- every exempted token
    #: reported *with the declaration that authorized it*.
    declared: list[tuple[str, str]] = field(default_factory=list)
    #: Non-failing ``severity='info'`` findings: migration items
    #: (``resolved-by-archive`` / ``resolved-by-registry``) and the
    #: liveness reports a grandfathered artifact receives without failing.
    diagnostics: list[Flag] = field(default_factory=list)


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


def _marker_line_kind(text: str) -> str | None:
    """The marker keyword of a ``Proposed path:`` / ``Untracked path:`` /
    ``External-repo path:`` line, lowercased, or ``None``.

    A marker line's backticked repo-path and line-bounds tokens are
    deliberate forward / out-of-tree references -- exempt from the hard
    checks -- and, since the typed registry landed, they are also the
    document's declarations, which is why the *kind* is returned rather
    than a bare boolean.  See ``_MARKER_LINE_RE`` and the module
    docstring's "Marker lines" and "typed-declaration registry"
    paragraphs.
    """
    match = _MARKER_LINE_RE.match(text)
    return match.group('kind').lower() if match is not None else None


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


def _walk_marker_context(text: str):
    """Yield ``(lineno, line, kind, block, is_marker)`` per scannable line.

    ``kind`` is the marker keyword governing this line -- set on a marker
    line *and* on each of its continuation rows -- or ``None`` when the
    line is outside any marker block; ``block`` is the governing marker
    line's number (0 outside a block).

    This is the **single** implementation of the marker-block walk: both
    the scan (which exempts a block's own tokens) and the registry parser
    (which turns those tokens into document-wide declarations) consume it,
    so the two can never disagree about where a block starts and ends.
    """
    in_block = False
    kind: str | None = None
    block = 0
    prev_lineno: int | None = None
    for lineno, line in scannable_lines(text):
        marker_kind = _marker_line_kind(line)
        is_marker = marker_kind is not None
        contiguous = prev_lineno is not None and lineno == prev_lineno + 1
        continuation = (
            in_block and contiguous and _is_marker_block_continuation(line)
        )
        if is_marker:
            kind = marker_kind
            block = lineno
        elif not continuation:
            kind = None
            block = 0
        governing = kind if (is_marker or continuation) else None
        yield lineno, line, governing, (block if governing else 0), is_marker
        in_block = is_marker or continuation
        prev_lineno = lineno


def parse_typed_declarations(
    text: str,
) -> tuple[list[Declaration], list[Flag]]:
    """Parse *text*'s marker blocks into a document registry.

    Returns ``(entries, problems)``.  ``entries`` are the literal path
    declarations, each exempting *only* that exact path anywhere else in
    the document.  ``problems`` are the fail-closed cases, reported as
    ``declaration``-kind flags:

    * a **malformed** entry -- a path-shaped token carrying a glob
      wildcard, when the registry is literal by contract; and
    * a **conflicting** entry -- the same path declared under two
      different marker keywords, which asserts two incompatible reasons
      (a path that will be created is not a path that is never tracked).
      The path gets no registry authority at all: the checker refuses to
      pick a reason rather than guessing one.

    Re-declaring the same path under the **same** keyword is idempotent,
    not a duplicate: it grants exactly the authority the first entry
    already granted.  That is what an append-only record does when a
    revision section restates its proposed paths, and what prose does
    when a marker line's own sentence names its path again.

    Entry extraction: every backticked token on the marker line itself
    (the compact one-line list form), but only the *first* token of a
    continuation row, because such a row lists one path and then explains
    it -- a path named later in the row's prose is a reference, not a
    second declaration.  Placeholder tokens declare nothing.
    """
    entries: list[Declaration] = []
    problems: list[Flag] = []
    first_seen: dict[str, tuple[int, str]] = {}
    conflicted: set[str] = set()
    blocks_with_rows: set[int] = set()
    for lineno, line, kind, block, is_marker in _walk_marker_context(text):
        if kind is None:
            continue
        if not is_marker:
            blocks_with_rows.add(block)
        tokens = [m.group(1).strip() for m in _BACKTICK_RE.finditer(line)]
        if not is_marker:
            tokens = tokens[:1]
        for token in tokens:
            if not token:
                continue
            path = _token_path_part(token)
            if '/' in path and any(
                ch in path for ch in _GLOB_WILDCARD_CHARS
            ):
                problems.append(Flag(
                    lineno, 'declaration', 'hard', token,
                    f'malformed typed declaration `{token}`: a registry '
                    f'entry is a literal path, not a glob -- it exempts '
                    f'nothing beyond its own block',
                ))
                continue
            if _is_placeholder(token):
                continue  # illustrative form -- declares nothing
            prior = first_seen.get(path)
            if prior is not None:
                if prior[1] != kind:
                    conflicted.add(path)
                    problems.append(Flag(
                        lineno, 'declaration', 'hard', token,
                        f'conflicting typed declarations for `{path}`: '
                        f'`{_MARKER_KIND_LABEL.get(kind, kind)}:` here, '
                        f'`{_MARKER_KIND_LABEL.get(prior[1], prior[1])}:` at '
                        f'line {prior[0]} -- two incompatible reasons, so '
                        f'the path gets no registry authority',
                    ))
                continue  # same keyword: idempotent, already registered
            first_seen[path] = (lineno, kind)
            entries.append(
                Declaration(line=lineno, block=block, kind=kind, path=path)
            )
    kept = [
        Declaration(
            line=e.line, block=e.block, kind=e.kind, path=e.path,
            registry_block=e.block in blocks_with_rows,
        )
        for e in entries if e.path not in conflicted
    ]
    return kept, problems


# --- Lifecycle liveness scope and the immutability (grandfather) predicate ---

#: A liveness-scope artifact: exactly ``dev/proposals/<name>.md`` or
#: ``dev/plans/<name>.md``.  Nothing nested (``archive/...`` has a second
#: separator and does not match) and no ``_``-prefixed name -- ``_template.md``
#: is the authoring template, not an artifact with a lifecycle status.
_LIFECYCLE_DOC_RE = re.compile(
    r'^dev/(?P<family>proposals|plans)/(?P<name>(?!_)[^/]+\.md)$'
)

#: Anything at or under one of these prefixes is an immutable archived
#: artifact, grandfathered by *location* with no status parse at all.
_LIFECYCLE_ARCHIVE_PREFIXES = ('dev/proposals/archive/', 'dev/plans/archive/')

#: The **terminal** status token of each lifecycle family -- deliberately
#: *only* the terminal ones.  This is an immutability predicate, not a
#: status vocabulary: the state machine and the full recognized-state set
#: live in the lifecycle planner, and this shipped, standard-library-only
#: checker must not carry a second copy of them.  Everything this predicate
#: does not recognize -- a non-terminal status, a typo, a missing or
#: duplicated field -- fails closed *into* liveness rather than inheriting
#: the grandfather, so the set can only ever be too small, never too
#: permissive.
_TERMINAL_STATUS: dict[str, frozenset[str]] = {
    'proposals': frozenset({'accepted', 'rejected', 'superseded'}),
    'plans': frozenset({'archived'}),
}

_STATUS_LINE_RE = re.compile(
    r'^\*\*Status\*\*:\s*(?P<status>[A-Za-z][A-Za-z-]*)\s*$'
)
_H2_RE = re.compile(r'^##\s')


def parse_header_status(text: str) -> str | None:
    """The artifact's strictly-parsed header status, or ``None``.

    Strict means: **exactly one** ``**Status**: <value>`` line among the
    scannable lines of the *header* -- the region above the first ``##``
    heading, which is where both authoring templates put the field.  A
    ``**Status**:`` line inside an appended revision section is a
    historical restatement, not the artifact's current status, so it is
    not a candidate; and zero or several candidates in the header yield
    ``None`` (the caller treats that as "not grandfathered").
    """
    found: list[str] = []
    for _lineno, line in scannable_lines(text):
        if _H2_RE.match(line):
            break
        match = _STATUS_LINE_RE.match(line.strip())
        if match is not None:
            found.append(match.group('status').lower())
    return found[0] if len(found) == 1 else None


@dataclass(frozen=True)
class _LivenessScope:
    """Whether, and how, liveness applies to the document being scanned.

    ``family`` is ``'proposals'`` / ``'plans'``; ``grandfathered`` is True
    for an artifact nobody may rewrite (archived by location, or terminal
    by strictly-parsed status), in which case the liveness findings are
    reported as non-failing diagnostics instead of hard flags.
    """

    family: str
    grandfathered: bool


def liveness_scope(doc_rel: str | None, text: str) -> _LivenessScope | None:
    """The liveness scope for the document at *doc_rel*, or ``None``.

    ``None`` means liveness does not run at all: every Markdown surface
    that is not a lifecycle artifact keeps its existing behavior, by
    declaration (those surfaces have their own mutability rules and are
    out of this contract's scope).
    """
    if not doc_rel:
        return None
    rel = doc_rel.replace('\\', '/')
    for prefix in _LIFECYCLE_ARCHIVE_PREFIXES:
        if rel.startswith(prefix):
            return _LivenessScope(
                family=prefix.split('/')[1], grandfathered=True,
            )
    match = _LIFECYCLE_DOC_RE.match(rel)
    if match is None:
        return None
    family = match.group('family')
    status = parse_header_status(text)
    return _LivenessScope(
        family=family,
        grandfathered=status in _TERMINAL_STATUS[family],
    )


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


# Exact lifecycle active-to-archive resolution -- see the module
# docstring's "Lifecycle archive resolution" paragraph.  Matches only
# ``dev/proposals/<file>.md`` or ``dev/plans/<file>.md`` with no
# further path segments in ``<file>`` -- a token that already names an
# ``archive/`` path (or anything nested deeper) does not match and
# falls through to ordinary resolution unchanged.
_LIFECYCLE_ARCHIVE_RE = re.compile(
    r'^dev/(?P<family>proposals|plans)/(?P<name>[^/]+\.md)$'
)


@dataclass(frozen=True)
class _LifecycleResolution:
    """The outcome of resolving a ``dev/{proposals,plans}/<file>.md``
    token under the exact active/archive lifecycle rule.

    ``resolved`` is the ``Path`` to use for further existence / line-
    count checks: the active file when it exists (always
    authoritative), else its exact same-family archived sibling when
    *that* exists, else ``None`` (neither candidate exists).
    ``duplicate`` is True when both candidates exist at once -- a
    lifecycle-state violation the caller must hard-flag rather than
    silently resolve via the (still-authoritative) active path.
    """

    resolved: Path | None
    duplicate: bool


def _lifecycle_archive_resolve(
    path: str, repo_root: Path,
) -> _LifecycleResolution | None:
    """Resolve *path* under the exact lifecycle archive-fallback rule.

    Returns ``None`` when *path* is not in the exact
    ``dev/{proposals,plans}/<file>.md`` shape -- the caller falls
    through to ordinary resolution.  Never searches by partial stem,
    date, or author; never crosses between the proposal and plan
    families; never applies outside these two directories.
    """
    match = _LIFECYCLE_ARCHIVE_RE.match(path)
    if match is None:
        return None
    family = match.group('family')
    name = match.group('name')
    direct = repo_root / 'dev' / family / name
    archived = repo_root / 'dev' / family / 'archive' / name
    direct_exists = direct.is_file()
    archived_exists = archived.is_file()
    if direct_exists and archived_exists:
        return _LifecycleResolution(resolved=direct, duplicate=True)
    if direct_exists:
        return _LifecycleResolution(resolved=direct, duplicate=False)
    if archived_exists:
        return _LifecycleResolution(resolved=archived, duplicate=False)
    return _LifecycleResolution(resolved=None, duplicate=False)


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

    lifecycle = _lifecycle_archive_resolve(target, repo_root)
    if lifecycle is not None:
        if lifecycle.duplicate:
            return Flag(
                lineno, 'path', 'hard', token,
                f'lifecycle-state violation: `{target}` exists both at '
                f'its active path and its archived sibling -- duplicate '
                f'identity is not silently normalized',
            )
        if lifecycle.resolved is not None:
            return None
        return Flag(
            lineno, 'path', 'hard', token,
            f'cited path does not resolve: `{token}`',
        )

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

    lifecycle = _lifecycle_archive_resolve(path, repo_root)
    if lifecycle is not None:
        if lifecycle.duplicate:
            return Flag(
                lineno, 'line-bounds', 'hard', token,
                f'lifecycle-state violation: `{path}` exists both at '
                f'its active path and its archived sibling -- duplicate '
                f'identity is not silently normalized',
            )
        if lifecycle.resolved is None:
            return Flag(
                lineno, 'line-bounds', 'hard', token,
                f'line-bounds citation to a missing file: `{token}`',
            )
        target = lifecycle.resolved
    else:
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
    """Reject a too-broad ``claim-check-allow`` glob.

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


def _archive_resolution_target(path: str, repo_root: Path) -> str | None:
    """The archived file a resolving lifecycle token went *through*.

    ``None`` when *path* is not a lifecycle token, does not resolve, or
    resolves at its own active location -- so a caller can tell "this
    only resolves because of the exact archive rule" from "this resolves
    on its own".
    """
    resolution = _lifecycle_archive_resolve(path, repo_root)
    if resolution is None or resolution.duplicate:
        return None
    if resolution.resolved is None or (repo_root / path).is_file():
        return None
    try:
        return resolution.resolved.relative_to(repo_root).as_posix()
    except ValueError:  # pragma: no cover -- resolved is built from repo_root
        return resolution.resolved.as_posix()


def _is_checkable_claim(path: str, top_level: set[str]) -> bool:
    """True when *path* is something this checker could ever hard-flag.

    A declaration for a path the checker never resolves (its first
    segment is not a real top-level entry -- the ordinary genuine
    ``External-repo`` case -- or it is a default-exempt framework runtime
    path) can never be observed doing work, so liveness reports it rather
    than failing an author for a claim the tool does not check.
    """
    return (
        path.split('/', 1)[0] in top_level and not _is_default_exempt(path)
    )


def _as_info(flag: Flag) -> Flag:
    """The same finding as a non-failing diagnostic."""
    return Flag(flag.line, flag.kind, 'info', flag.token, flag.message)


def _scan(
    text: str, repo_root: Path, *, external_allowed: bool = False,
    doc_rel: str | None = None,
) -> tuple[
    list[Flag], list[Flag], list[tuple[str, str]],
    list[tuple[str, str]], list[Flag],
]:
    """Core scan -- ``(hard, soft, exempted, declared, diagnostics)``.

    A would-be-hard path / line-bounds flag is suppressed when either
    exemption mechanism authorizes it and the path does NOT resolve
    locally: a typed registry declaration of that **exact** path
    (recorded in ``declared`` with the declaration that authorized it),
    or a valid ``claim-check-allow`` glob (recorded in ``exempted`` as
    ``(token, glob)``).  The registry is consulted first, so a glob kept
    alive only by a path its own document already declares shows up as a
    migration item rather than as load-bearing.  A *too-broad* glob is
    itself a hard flag and exempts nothing.

    ``doc_rel`` is the document's repo-relative path, and is what makes
    liveness decidable (which artifact, and is it immutable).  Without it
    -- :func:`check_text` callers that pass only text -- liveness does not
    run and behavior is exactly as before.

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
    glob_lines: dict[str, int] = {}
    hard: list[Flag] = []
    for lineno, glob in parse_allow_directives(text):
        err = allow_glob_error(glob)
        if err is not None:
            hard.append(Flag(lineno, 'directive', 'hard', glob, err))
        else:
            allow_globs.append(glob)
            glob_lines.setdefault(glob, lineno)

    # The document registry: typed declarations, exact literal paths.
    # A malformed or duplicate entry is absent from ``registry`` -- it
    # fails closed, granting no document-wide authority -- and is
    # reported below.
    entries, decl_problems = parse_typed_declarations(text)
    registry: dict[str, Declaration] = {}
    for entry in entries:
        registry.setdefault(entry.path, entry)

    # ``soft`` has no producer since the category-D count flag was
    # retired; kept for the historical two-tuple ``check_text`` contract.
    soft: list[Flag] = []
    exempted: list[tuple[str, str]] = []
    declared: list[tuple[str, str]] = []
    diagnostics: list[Flag] = []
    # Liveness bookkeeping, collected while scanning so no second pass can
    # disagree with the first about what actually got suppressed.
    glob_effective: set[str] = set()
    glob_by_archive: dict[str, str] = {}
    glob_by_registry: dict[str, Declaration] = {}
    live_entries: set[str] = set()

    for lineno, line, block_kind, _block, _marker in _walk_marker_context(
        text
    ):
        # A marker block's own rows stay exempt from the hard checks (and
        # an occurrence there never makes its own declaration live).
        if block_kind is not None or external_allowed:
            continue
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
            path_part = _token_path_part(token)
            matched = next(
                (g for g in allow_globs
                 if fnmatch.fnmatchcase(path_part, g)),
                None,
            )
            if flag is None:
                # The token resolves on its own.  If a directive glob
                # still covers it, that glob no longer suppresses
                # anything -- and *why* decides its class below: an
                # occurrence the exact archive rule now resolves is a
                # redundancy this mechanism created, not stale debt.
                if matched is not None and matched not in glob_effective:
                    target = _archive_resolution_target(path_part, repo_root)
                    if target is not None:
                        glob_by_archive.setdefault(matched, target)
                continue
            # Neither mechanism may silence a failure on a path that
            # exists locally -- e.g. an out-of-range line-bounds citation
            # into a real file, exactly the stale-anchor class claim_check
            # is meant to catch.
            resolves = (repo_root / path_part).exists()
            entry = registry.get(path_part)
            if entry is not None and not resolves:
                declared.append((token, entry.label))
                live_entries.add(entry.path)
                if matched is not None:
                    glob_by_registry.setdefault(matched, entry)
                continue
            if matched is not None and not resolves:
                exempted.append((token, matched))
                glob_effective.add(matched)
                continue
            hard.append(flag)

    # --- Liveness -----------------------------------------------------
    # Scope: only a lifecycle artifact is evaluated, and an immutable one
    # (archived, or terminal by strictly-parsed status) receives the same
    # findings as non-failing diagnostics.  Every other Markdown surface
    # keeps its existing behavior by declaration.
    scope = liveness_scope(doc_rel, text)
    fails = scope is not None and not scope.grandfathered
    severity = 'hard' if fails else 'info'
    sink = hard if fails else diagnostics

    # A malformed / duplicate declaration has already failed closed (it
    # grants nothing).  It is reported on every surface -- an authoring
    # defect is not a scope question -- but only a mutable lifecycle
    # artifact fails on it, exactly as for the classes below.
    for problem in decl_problems:
        (hard if fails else diagnostics).append(
            problem if fails else _as_info(problem)
        )

    if scope is None:
        return hard, soft, exempted, declared, diagnostics

    grandfather_note = (
        '' if fails else
        ' (reported only: this artifact is immutable, so unused metadata '
        'does not change the exit code)'
    )
    # DEPRECATION WINDOW -- the judgement, stated where it is made.
    #
    # A glob can stop suppressing anything for two very different
    # reasons, and only one of them is the author's debt:
    #
    #   * the author's forward reference materialized, or the glob was
    #     never load-bearing -- `unused`, a hard finding, which is the
    #     staleness this contract exists to retire; or
    #   * THIS change set made it redundant -- the exact lifecycle
    #     archive rule now resolves the token, or the document's own
    #     typed registry now authorizes it.
    #
    # The second class is a scheduling artifact.  Hard-failing it would
    # turn every artifact that papered over an archive move red the
    # moment the resolver landed -- the interaction the accepted
    # proposal's round-1 review measured -- and would assign that debt to
    # whoever happens to own the citing document rather than to whoever
    # archived the cited one.  So both redundancy classes report as
    # non-failing migration items, naming the artifact, the directive
    # line, the glob, and what now resolves it: an exact inventory for
    # the metadata migration that retires them.
    #
    # The window is bounded by that migration, not by a clock.  Nothing
    # here expires on a date: a checker that turns red on a calendar day
    # with no change to the tree would be unreproducible, and this file
    # ships to adopters whose migrations are their own.  The accepted
    # contract names `resolved-by-archive`; `resolved-by-registry` is the
    # same argument applied to the registry landing in the same change
    # set, and is called out as such in the implementation record.
    seen_globs: set[str] = set()
    for glob in allow_globs:
        if glob in seen_globs:
            continue
        seen_globs.add(glob)
        lineno = glob_lines[glob]
        if glob in glob_effective:
            continue  # load-bearing -- its suppressions are reported above
        if glob in glob_by_archive:
            diagnostics.append(Flag(
                lineno, 'directive', 'info', glob,
                f'migration item: claim-check-allow glob `{glob}` is now '
                f'`resolved-by-archive` -- every occurrence it suppressed '
                f'resolves through the exact lifecycle archive rule '
                f'(`{glob_by_archive[glob]}`).  Retire the glob with the '
                f'metadata migration; this is not a stale-debt finding.',
            ))
            continue
        if glob in glob_by_registry:
            diagnostics.append(Flag(
                lineno, 'directive', 'info', glob,
                f'migration item: claim-check-allow glob `{glob}` is now '
                f'`resolved-by-registry` -- {glob_by_registry[glob].label} '
                f'authorizes every occurrence it suppressed.  Retire the '
                f'glob with the metadata migration; this is not a '
                f'stale-debt finding.',
            ))
            continue
        sink.append(Flag(
            lineno, 'directive', severity, glob,
            f'unused claim-check-allow glob `{glob}`: it suppresses no '
            f'report in this document{grandfather_note}',
        ))

    for entry in entries:
        if entry.path in live_entries:
            continue
        if not entry.registry_block:
            # A standalone marker line -- the mechanism's original
            # line-local use, mid-prose: "Proposed path: `x`, because ...".
            # Its declaration is load-bearing for its OWN line, so an
            # author cannot retire it, and demanding that the document
            # cite the path a second time to justify it is an obligation
            # with no legal discharge: deleting the marker hard-flags the
            # very line it explains.  The liveness obligation belongs to a
            # *registry block* -- the form the accepted contract writes it
            # for ("a compact marker block becomes a document registry")
            # -- so a bare marker line is reported, never failed.  Named as
            # a divergence from the literal contract text in the
            # implementation record, with the two measured instances.
            continue
        if not _is_checkable_claim(entry.path, top_level):
            diagnostics.append(Flag(
                entry.line, 'declaration', 'info', entry.path,
                f'{entry.label} authorizes nothing, and cannot: this '
                f'checker never resolves `{entry.path}`, so liveness is '
                f'not evaluable for it',
            ))
            continue
        archived = _archive_resolution_target(entry.path, repo_root)
        if archived is not None:
            diagnostics.append(Flag(
                entry.line, 'declaration', 'info', entry.path,
                f'migration item: {entry.label} is now '
                f'`resolved-by-archive` -- the exact lifecycle archive '
                f'rule resolves it (`{archived}`).  Retire the '
                f'declaration with the metadata migration; this is not a '
                f'stale-debt finding.',
            ))
            continue
        if (repo_root / entry.path).exists():
            sink.append(Flag(
                entry.line, 'declaration', severity, entry.path,
                f'{entry.label} is stale: the path has materialized, so '
                f'the declaration exempts nothing{grandfather_note}',
            ))
            continue
        sink.append(Flag(
            entry.line, 'declaration', severity, entry.path,
            f'{entry.label} is unused: nothing outside its own block '
            f'cites it{grandfather_note}',
        ))

    return hard, soft, exempted, declared, diagnostics


def check_text(
    text: str, repo_root: Path, *, external_allowed: bool = False,
    doc_rel: str | None = None,
) -> tuple[list[Flag], list[Flag]]:
    """Scan *text* and return ``(hard_flags, soft_flags)``.

    A thin wrapper over :func:`_scan` preserving the historical
    two-tuple contract.  The document-scoped ``claim-check-allow``
    exemptions (and the report of which tokens they cleared) are
    surfaced through :class:`CheckResult` via :func:`check_file`.

    ``doc_rel`` -- the document's repo-relative path -- is optional and
    defaults to ``None``, in which case liveness does not run: a caller
    holding only text cannot say which artifact it is, and liveness is
    defined per lifecycle artifact.  :func:`check_file` always supplies
    it.

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
    hard, soft, _exempted, _declared, _diagnostics = _scan(
        text, repo_root, external_allowed=external_allowed, doc_rel=doc_rel,
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


def _repo_relative(path: Path, repo_root: Path) -> str | None:
    """*path* as a POSIX path relative to *repo_root*, or ``None``.

    ``None`` for a file outside the root (or an unresolvable one): such a
    file cannot be a lifecycle artifact of *this* repository, so liveness
    must not run against it.
    """
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except (ValueError, OSError):
        return None


def check_file(
    path: Path, repo_root: Path, *, external_allow: list[str] | None = None,
) -> CheckResult:
    """Run the checker against one file.

    ``external_allow`` is the list of file globs whose path-claims
    describe external repos (see ``check_text``); when *path* matches
    one, the hard repo-path / line-bounds resolution is skipped.

    The result also carries any path tokens suppressed by the
    document-scoped ``claim-check-allow`` directive (``exempted``) or by a
    typed registry declaration (``declared``, each naming the declaration
    that authorized it), so the run can report exactly which would-be-flags
    were waived for audit -- plus the non-failing liveness ``diagnostics``.
    """
    external = file_is_external(path, repo_root, external_allow or [])
    text = path.read_text(encoding='utf-8', errors='replace')
    hard, soft, exempted, declared, diagnostics = _scan(
        text, repo_root, external_allowed=external,
        doc_rel=_repo_relative(path, repo_root),
    )
    return CheckResult(
        path=path, hard_flags=hard, soft_flags=soft, exempted=exempted,
        declared=declared, diagnostics=diagnostics,
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
    if result.declared:
        print(
            f'claim_check: {rel} -- {len(result.declared)} path(s) '
            f'exempted by a typed declaration:'
        )
        for token, label in result.declared:
            print(f'  {rel}: exempted `{token}` via {label}')
    if result.diagnostics:
        # Non-failing: migration items and the liveness reports an
        # immutable artifact receives without failing.  On STDOUT, for the
        # same auditability reason as the exemption report above.
        print(
            f'claim_check: {rel} -- {len(result.diagnostics)} '
            f'diagnostic(s) (reported, not failing):'
        )
        for flag in result.diagnostics:
            print(_format_flag(rel, flag))
    if not result.hard_flags and not result.soft_flags:
        print(f'claim_check: {rel} -- OK, no claim-check flags.')

    if result.hard_flags:
        return 1
    if result.soft_flags and args.fail_on_soft:
        return 1
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
