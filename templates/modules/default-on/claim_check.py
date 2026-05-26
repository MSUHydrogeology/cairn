#!/usr/bin/env python3
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
subset (broken repo paths, out-of-bounds line citations, count claims).

**Hard checks** -- deterministic; a failure exits non-zero:

* **Repo-path claims.**  A backticked token whose first
  ``/``-separated segment is a real top-level entry of the
  repository (a top-level directory *or* a root file -- ``AGENTS.md``,
  ``CLAUDE.md``, ...) is resolved against the tree.  A cited path
  that does not exist is a hard flag.  The top-level set is derived
  by listing the repo root, so root landmark files are first-class
  and the set never goes stale.
* **Line-bounds claims.**  A backticked ``path:N`` / ``path:N-M``
  token is checked: the file must exist and have at least ``M``
  lines.  An out-of-range citation is a hard flag.  This is a
  *bounds* check only -- it does NOT verify the cited lines still
  contain the rule or API being claimed.

**Soft flags** -- advisory; printed but exit 0 unless
``--fail-on-soft``:

* **Count claims.**  A number adjacent to a tree-noun (``lines``,
  ``proposals``, ``plans``, ``tests``, ``commits``, ``files``) is
  flagged: compute it live or cite a delta; do not quote an absolute
  count from memory.

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

Tokens on a marker line are exempt from the hard checks; count
claims on the line still soft-flag.  When a marker line is followed
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
Link-checking and count soft-flags are unaffected -- only the
hard repo-path / line-bounds resolution is skipped for matched files.

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
module.  Generalized from the modflow_tools ``scripts/claim_check.py``
adopter implementation; see Cairn's CHANGELOG (v0.2) for provenance.
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]

# Tree-nouns that make an adjacent number a count claim (category D).
_COUNT_NOUNS = ('lines', 'proposals', 'plans', 'tests', 'commits', 'files')

# A backticked span.  Group 1 is the token text.
_BACKTICK_RE = re.compile(r'`([^`\n]+)`')

# A line-bounds citation: ``path:N`` or ``path:N-M``.
_LINE_CITATION_RE = re.compile(
    r'^(?P<path>[^:\s]+):(?P<start>\d+)(?:-(?P<end>\d+))?$'
)

# A count claim: a number directly followed by a tree-noun
# ("40 proposals", "1,294 lines", "1823 tests").
_COUNT_RE = re.compile(
    r'\b(\d[\d,]*)\s+(' + '|'.join(_COUNT_NOUNS) + r')\b',
    re.IGNORECASE,
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
#     repository (e.g., a Cairn-side path in modflow_tools' tree, or an
#     LHM path).  Added 2026-05-21 per the accepted cairn-doctrine-sync-
#     may-19-21 plan's Chunk 0 (plan-design choice resolving the F4
#     residual claim_check problem).
# Any keyword -- singular or plural, any case, optionally as a list
# item -- exempts the line's path / line-bounds tokens from the hard
# checks (count claims still soft-flag).  This is R8 of the work-
# intents proposal (``2026-05-19-codex-local-claim-system``) plus the
# 2026-05-21 External-repo paths extension.
_MARKER_LINE_RE = re.compile(
    r'^\s*(?:(?:[-*+]|\d+[.)])\s+)?'
    r'(?:proposed|untracked|external-repo)\s+paths?:',
    re.IGNORECASE,
)


@dataclass
class Flag:
    """One claim-check finding."""

    line: int
    kind: str        # 'path' | 'line-bounds' | 'count'
    severity: str    # 'hard' | 'soft'
    token: str
    message: str


@dataclass
class CheckResult:
    """The hard + soft flags found in one file."""

    path: Path
    hard_flags: list[Flag] = field(default_factory=list)
    soft_flags: list[Flag] = field(default_factory=list)


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
    hard checks.  Count claims on the line still soft-flag.  See
    ``_MARKER_LINE_RE`` and the module docstring's "Marker lines"
    paragraph.
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


def check_path_token(
    token: str, lineno: int, repo_root: Path, top_level: set[str],
) -> Flag | None:
    """Hard-check a backticked token that classifies as a repo path.

    Returns a hard flag when the token's first segment is a real
    top-level entry but the full path does not resolve; ``None`` when
    the token is not a repo-path claim or resolves cleanly.
    """
    first = token.split('/', 1)[0]
    if first not in top_level:
        return None  # not a repo-path claim -- nothing to check
    if (repo_root / token).exists():
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
    n_lines = len(
        target.read_text(encoding='utf-8', errors='replace').splitlines()
    )
    if end > n_lines:
        return Flag(
            lineno, 'line-bounds', 'hard', token,
            f'line-bounds citation `{token}` exceeds {path} '
            f'({n_lines} lines)',
        )
    return None


def find_count_flags(lineno: int, text: str) -> list[Flag]:
    """Soft-flag every count claim (a number adjacent to a tree-noun)."""
    flags: list[Flag] = []
    for match in _COUNT_RE.finditer(text):
        claim = f'{match.group(1)} {match.group(2)}'
        flags.append(Flag(
            lineno, 'count', 'soft', claim,
            f'count claim `{claim}` -- compute it live or cite a '
            f'delta; do not quote an absolute count from memory',
        ))
    return flags


def check_text(
    text: str, repo_root: Path, *, external_allowed: bool = False,
) -> tuple[list[Flag], list[Flag]]:
    """Scan *text* and return ``(hard_flags, soft_flags)``.

    Raises ``NotADirectoryError`` when *repo_root* is not a
    directory.  An unresolvable root yields an empty top-level set,
    which makes every backticked repo path read as "not a claim" --
    the scan would silently no-op and report a false clean result.
    The checker fails closed instead.

    ``external_allowed`` (the file-scoped external-path allowance, set
    by the caller from ``--external-allow`` globs): when True, the hard
    repo-path / line-bounds resolution is skipped for this file -- it
    describes an external repo whose relative paths must not be resolved
    against the local tree.  Count soft-flags still run (they are
    advisory).
    """
    if not repo_root.is_dir():
        raise NotADirectoryError(
            f'claim_check: repo root is not a directory: {repo_root}'
        )
    top_level = repo_top_level(repo_root)
    hard: list[Flag] = []
    soft: list[Flag] = []
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
                    hard.append(flag)
        soft.extend(find_count_flags(lineno, line))
        in_marker_block = marker_line or marker_continuation
        prev_lineno = lineno
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
    """
    external = file_is_external(path, repo_root, external_allow or [])
    text = path.read_text(encoding='utf-8', errors='replace')
    hard, soft = check_text(text, repo_root, external_allowed=external)
    return CheckResult(path=path, hard_flags=hard, soft_flags=soft)


def _format_flag(rel: Path, flag: Flag) -> str:
    return f'  {rel}:{flag.line}: [{flag.kind}] {flag.message}'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='claim_check',
        description=(
            'Write-time verify-before-asserting claim checker.  '
            'Hard-flags broken repo paths and out-of-bounds line '
            'citations; soft-flags count claims.'
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
        help='Exit non-zero on soft (count) flags too -- author / '
             'pre-commit use.',
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
    if not result.hard_flags and not result.soft_flags:
        print(f'claim_check: {rel} -- OK, no claim-check flags.')

    if result.hard_flags:
        return 1
    if result.soft_flags and args.fail_on_soft:
        return 1
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
