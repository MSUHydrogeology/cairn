#!/usr/bin/env python3
"""Cairn self-check -- prose-integrity gate over Cairn's own Markdown tree.

Cairn ships a ``claim-check`` *methodology module* and tells adopters to
"absorb tests, docs, and examples into every change."  This script makes
that true of Cairn itself: it runs Cairn's own discipline *on Cairn*, so
the repo visibly passes the gate it preaches.  It is deliberately thin --
a prose-integrity check, **not** a behavioral test suite (Cairn is
methodology, not software; behavioral tests stay scoped to
``bootstrap/tests/``).

Two checks, both deterministic and offline by default:

1. **Link check.**  Every internal Markdown link / image and reference
   definition resolves: relative file targets exist, and intra-document
   heading **anchors** resolve under **GitHub slug rules** (lowercase;
   drop punctuation except hyphen/underscore; spaces -> hyphens; dedupe
   repeats with ``-1``, ``-2`` ...).  This is the one documented target
   rendering convention -- Cairn is read on GitHub.  External
   ``http(s)`` links are NOT fetched unless ``--check-external``.
2. **Claim-path check.**  A backticked token whose first ``/``-segment
   is a real top-level entry of the Cairn repo is resolved against the
   tree (ported from modflow_tools' ``scripts/claim_check.py``).  Fenced
   / indented code, HTML comments, and blockquotes are skipped;
   ``Proposed path:`` / ``Untracked path:`` / ``External-repo path:``
   markers (and ``~/...`` / ``$HOME`` external paths) are exempt.

Scanned set: the whole tracked Markdown tree (``git ls-files '*.md'``).

Usage::

    python scripts/check_cairn.py                 # check the whole tree
    python scripts/check_cairn.py --check-external # also probe http(s) links
    python scripts/check_cairn.py PATH ...         # check specific files

Exit codes: ``0`` clean; ``1`` at least one broken link / anchor / path;
``2`` usage error.

Source proposal / plan: the modflow_tools-hosted
``cairn-self-application-and-docs`` arc (Chunk 1).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------
# Repo + file discovery


def repo_root() -> Path:
    try:
        out = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True, text=True, check=True,
            cwd=str(Path(__file__).resolve().parent),
        )
        return Path(out.stdout.strip())
    except (subprocess.CalledProcessError, OSError):
        return Path(__file__).resolve().parents[1]


def tracked_markdown(root: Path) -> list[Path]:
    out = subprocess.run(
        ['git', 'ls-files', '*.md'], cwd=str(root),
        capture_output=True, text=True, check=True,
    )
    return [root / line for line in out.stdout.splitlines() if line.strip()]


# --------------------------------------------------------------------------
# Markdown scanning (ported from modflow_tools' claim_check.scannable_lines)

_MARKER_LINE_RE = re.compile(
    r'^\s*(?:(?:[-*+]|\d+[.)])\s+)?'
    r'(?:proposed|untracked|external-repo)\s+paths?:',
    re.IGNORECASE,
)
_BACKTICK_RE = re.compile(r'`([^`\n]+)`')
_PLACEHOLDER_CHARS = ('<', '>', '*', '{', '}')
# Inline links + images: optional '!', [text](target "title").
_LINK_RE = re.compile(r'!?\[[^\]]*\]\(\s*([^)\s]+)(?:\s+"[^"]*")?\s*\)')
# Reference definitions: [id]: target  (optionally with a title).
_REFDEF_RE = re.compile(r'^\s*\[[^\]]+\]:\s*(\S+)')
_HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')


def _strip_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
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
    """``(1-based line number, text)`` for prose lines only.

    Fenced / indented code, HTML comments, and blockquotes are dropped
    (conservative indented-code heuristic that never treats list content
    as code).  Ported from modflow_tools' claim_check.
    """
    out: list[tuple[int, str]] = []
    in_fence = in_html_comment = in_indent_code = list_active = False
    prev_blank = True
    for idx, raw in enumerate(text.split('\n'), start=1):
        line = raw.expandtabs(4)
        if re.match(r'^ {0,3}(```|~~~)', line):
            in_fence = not in_fence
            in_indent_code = False
            prev_blank = False
            continue
        if in_fence:
            in_indent_code = False
            prev_blank = False
            continue
        work, in_html_comment = _strip_html_comments(line, in_html_comment)
        indent = len(work) - len(work.lstrip(' '))
        stripped = work.strip()
        if stripped == '':
            prev_blank = True
            continue
        if re.match(r'^ {0,3}>', work):
            in_indent_code = False
            prev_blank = False
            continue
        if re.match(r'^ *([-*+]|\d+[.)])\s', work):
            list_active = True
        elif indent == 0:
            list_active = False
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


# --------------------------------------------------------------------------
# GitHub slug + anchors


def github_slug(heading_text: str) -> str:
    """GitHub heading-anchor slug: lowercase; drop punctuation except
    hyphen/underscore; spaces -> hyphens.

    **Consecutive hyphens are intentionally NOT collapsed, and
    leading/trailing hyphens are NOT stripped** -- this matches GitHub's
    actual anchor generator, ``github-slugger``, whose core is
    ``value.toLowerCase().replace(regex, '').replace(/ /g, '-')``
    (Flet/github-slugger ``index.js`` line 76): it removes punctuation
    (its ``regex`` preserves the hyphen U+002D and space), replaces
    spaces with hyphens, and does no collapse/trim.  So a heading like
    ``Rule 1 — No private content`` slugs to ``rule-1--no-private-content``
    (double hyphen, from the spaces around the stripped em-dash) on
    GitHub, and this checker must expect the same.  Collapsing/stripping
    here would DIVERGE from GitHub and false-flag correct anchor links.
    (Verified against the canonical source for code-review finding P2,
    2026-05-22, which had the collapse behavior inverted.)
    """
    s = heading_text.strip().lower()
    s = s.replace('`', '')                       # inline code ticks
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)  # link -> its text
    s = re.sub(r'[^\w\s-]', '', s)               # drop other punctuation
    s = s.replace(' ', '-')
    return s


def file_anchors(text: str) -> set[str]:
    """Heading anchors for a file, with GitHub's repeat-dedupe (-1, -2)."""
    counts: Counter[str] = Counter()
    anchors: set[str] = set()
    in_fence = False
    for raw in text.split('\n'):
        if re.match(r'^ {0,3}(```|~~~)', raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = _HEADING_RE.match(raw)
        if not m:
            continue
        base = github_slug(m.group(2))
        n = counts[base]
        counts[base] += 1
        anchors.add(base if n == 0 else f'{base}-{n}')
    return anchors


# --------------------------------------------------------------------------
# Flags


@dataclass
class Flag:
    file: Path
    line: int
    kind: str        # 'link' | 'anchor' | 'path'
    message: str


@dataclass
class Result:
    flags: list[Flag] = field(default_factory=list)
    external_links: int = 0
    files_scanned: int = 0


def _is_placeholder(token: str) -> bool:
    return ' ' in token or any(c in token for c in _PLACEHOLDER_CHARS)


def _is_external_path(token: str) -> bool:
    return token.startswith(('~', '$HOME', '/Users/', '/home/'))


# --------------------------------------------------------------------------
# Per-file checks


def _check_links(
    md: Path, root: Path, scannable: list[tuple[int, str]],
    anchors_by_file: dict[Path, set[str]], result: Result,
    check_external: bool,
) -> None:
    targets: list[tuple[int, str]] = []
    for lineno, line in scannable:
        for m in _LINK_RE.finditer(line):
            targets.append((lineno, m.group(1)))
        rd = _REFDEF_RE.match(line)
        if rd:
            targets.append((lineno, rd.group(1)))

    for lineno, target in targets:
        target = target.strip()
        if target.startswith('#'):           # same-file anchor
            path_part, anchor = '', target[1:]
        elif '#' in target and not target.startswith(('http', 'mailto')):
            path_part, anchor = target.split('#', 1)
        else:
            path_part, anchor = target, ''

        low = target.lower()
        if low.startswith(('http://', 'https://')):
            result.external_links += 1
            if check_external:
                _probe_external(md, lineno, target, result)
            continue
        if low.startswith(('mailto:', 'tel:')) or target.startswith('<'):
            continue

        # Resolve the file part (if any).
        if path_part:
            if path_part.startswith('/'):
                tgt = root / path_part.lstrip('/')
            else:
                tgt = (md.parent / path_part)
            try:
                tgt = tgt.resolve()
            except OSError:
                tgt = None
            if tgt is None or not tgt.exists():
                result.flags.append(Flag(
                    md, lineno, 'link',
                    f'broken link target: `{target}`'))
                continue
            anchor_file = tgt if tgt.is_file() else None
        else:
            anchor_file = md  # pure same-file anchor

        # Resolve the anchor (if any) against the target file's headings.
        if anchor and anchor_file is not None and anchor_file.suffix == '.md':
            if anchor_file not in anchors_by_file:
                anchors_by_file[anchor_file] = file_anchors(
                    anchor_file.read_text(encoding='utf-8', errors='replace'))
            if anchor not in anchors_by_file[anchor_file]:
                result.flags.append(Flag(
                    md, lineno, 'anchor',
                    f'unresolved heading anchor: `{target}`'))


def _probe_external(md: Path, lineno: int, url: str, result: Result) -> None:
    import urllib.request
    req = urllib.request.Request(url, method='HEAD',
                                 headers={'User-Agent': 'cairn-check'})
    try:
        urllib.request.urlopen(req, timeout=10)  # noqa: S310 (opt-in only)
    except Exception as exc:  # noqa: BLE001 -- report any failure
        result.flags.append(Flag(
            md, lineno, 'link', f'external link failed ({exc}): {url}'))


def _check_paths(
    md: Path, root: Path, top_level: set[str],
    scannable: list[tuple[int, str]], result: Result,
) -> None:
    in_marker_block = False
    prev_lineno: int | None = None
    for lineno, line in scannable:
        marker_line = _MARKER_LINE_RE.match(line) is not None
        contiguous = prev_lineno is not None and lineno == prev_lineno + 1
        marker_cont = in_marker_block and contiguous and _marker_cont(line)
        if not (marker_line or marker_cont):
            for m in _BACKTICK_RE.finditer(line):
                token = m.group(1).strip()
                if (not token or _is_placeholder(token)
                        or _is_external_path(token)):
                    continue
                first = token.split('/', 1)[0]
                if first not in top_level:
                    continue
                if not (root / token).exists():
                    result.flags.append(Flag(
                        md, lineno, 'path',
                        f'cited path does not resolve: `{token}`'))
        in_marker_block = marker_line or marker_cont
        prev_lineno = lineno


def _marker_cont(text: str) -> bool:
    s = text.strip()
    if not s or s.startswith('#'):
        return False
    return s.startswith('|') or bool(re.match(r'^([-*+]|\d+[.)])\s+', s)) \
        or s.startswith('`')


# --------------------------------------------------------------------------
# Driver


def check_tree(root: Path, files: list[Path],
               check_external: bool = False) -> Result:
    # Claimable top-level entries are tracked *content*; dot-entries
    # (``.git`` and friends) are VCS / runtime internals, so a cited
    # ``.git/hooks/pre-commit`` is a runtime artifact, not a content
    # path claim -- exclude them.  Trade-off (code-review P3, 2026-05-22):
    # a path claim into a *tracked* dotfolder (e.g. a future ``.github/``)
    # is skipped rather than validated -- accepted to stay robust against
    # ``.git/`` false positives; revisit if tracked-dotpath claims appear.
    top_level = (
        {p.name for p in root.iterdir() if not p.name.startswith('.')}
        if root.is_dir() else set()
    )
    anchors_by_file: dict[Path, set[str]] = {}
    result = Result()
    for md in files:
        text = md.read_text(encoding='utf-8', errors='replace')
        scannable = scannable_lines(text)
        result.files_scanned += 1
        _check_links(md, root, scannable, anchors_by_file, result,
                     check_external)
        _check_paths(md, root, top_level, scannable, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='check_cairn',
        description="Cairn self-check: link / anchor / claim-path "
                    "integrity over Cairn's own Markdown tree.",
    )
    parser.add_argument('files', nargs='*', type=Path,
                        help='Specific Markdown files (default: whole tree).')
    parser.add_argument('--root', type=Path, default=None,
                        help='Repo root (default: git toplevel).')
    parser.add_argument('--check-external', action='store_true',
                        help='Also probe http(s) links (network; off by '
                             'default).')
    args = parser.parse_args(argv)

    root = args.root.resolve() if args.root else repo_root()
    if not root.is_dir():
        print(f'check_cairn: root is not a directory: {root}', file=sys.stderr)
        return 2
    files = [f.resolve() for f in args.files] if args.files \
        else tracked_markdown(root)
    if not files:
        print('check_cairn: no Markdown files found.', file=sys.stderr)
        return 2

    result = check_tree(root, files, check_external=args.check_external)

    for flag in result.flags:
        try:
            rel = flag.file.resolve().relative_to(root)
        except ValueError:
            rel = flag.file
        print(f'  {rel}:{flag.line}: [{flag.kind}] {flag.message}',
              file=sys.stderr)

    ext = (f'; {result.external_links} external link(s) not probed'
           if not args.check_external and result.external_links else '')
    if result.flags:
        print(f'check_cairn: {len(result.flags)} issue(s) across '
              f'{result.files_scanned} file(s){ext}.', file=sys.stderr)
        return 1
    print(f'check_cairn: OK -- {result.files_scanned} Markdown file(s) '
          f'scanned; no issues{ext}.')
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
