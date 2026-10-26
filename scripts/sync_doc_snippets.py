#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Snippet-sync -- keep doc code blocks in lockstep with their source.

The ``doc-drift-prevention`` module installs this verbatim into an
adopting repo's ``scripts/`` directory. It is the **snippet half** of a
doc-drift gate: a fenced code block in a Markdown doc is *mirrored* from
a named region of a runnable source file, so the snippet cannot drift
from the thing it illustrates.

It is **stack-neutral**: the region markers are matched as plain
substrings, so they work inside *any* language's comment syntax
(``#``, ``//``, ``<!-- -->``, ``--`` ...).

Directive grammar
-----------------

In the **Markdown doc**, wrap a fenced block with an opener comment that
names ``source#region``::

    <!-- snippet: examples/quickstart.py#build -->
    ```python
    model = Model(config)
    model.build()
    ```

In the **source file**, delimit the region with language-neutral
markers (in whatever comment syntax the source uses)::

    # snippet-start: build
    model = Model(config)
    model.build()
    # snippet-end: build

The block between the fences must equal the lines between the markers.

Modes
-----

* ``--check`` (default): report every block that has drifted from its
  source, and exit ``1`` if any has. The drift gate for CI.
* ``--sync``: rewrite each drifted block to match its source. Only the
  **Markdown file that contains the directive** is rewritten; the source
  is never touched.

Path-safety contract
--------------------

The source path in a directive must be **repo-relative and contained**:
absolute paths and ``..`` escapes are rejected, and the resolved path
must stay under the repo root. A missing source file, a missing region,
or an ambiguous region (duplicate or unterminated markers) is a crisp
non-zero error in both modes -- never a silent pass or a partial write.

Usage::

    python scripts/sync_doc_snippets.py            # --check the whole tree
    python scripts/sync_doc_snippets.py --sync      # rewrite drifted blocks
    python scripts/sync_doc_snippets.py PATH ...     # specific docs

Exit codes: ``0`` clean (``--check``) or written (``--sync``); ``1``
drift (``--check``) or a path/region error; ``2`` usage error.

Vendor-neutral and standard-library only.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_OPENER_RE = re.compile(r'^<!--\s*snippet:\s*(\S+?)#(\S+?)\s*-->\s*$')
_FENCE_RE = re.compile(r'^(\s*)(```+|~~~+)(.*)$')


class SnippetError(Exception):
    """A directive could not be resolved (bad path, missing region)."""


@dataclass
class Directive:
    doc: Path
    opener_line: int          # 1-based line of the opener comment
    source: str               # raw source token from the directive
    region: str
    fence_indent: str
    fence_marker: str         # the exact ``` / ~~~ run
    fence_info: str           # info string after the fence (e.g. 'python')
    body_start: int           # 0-based index of first body line in doc lines
    body_end: int             # 0-based index of the closing-fence line
    current: list[str]        # current body lines (between the fences)


def _parse_directives(doc: Path, lines: list[str]) -> list[Directive]:
    """Find every snippet directive + its fenced block in *lines*."""
    directives: list[Directive] = []
    i = 0
    n = len(lines)
    while i < n:
        m = _OPENER_RE.match(lines[i])
        if not m:
            i += 1
            continue
        opener_idx = i
        source, region = m.group(1), m.group(2)
        # The next non-empty line must open a fenced block.
        j = i + 1
        while j < n and lines[j].strip() == '':
            j += 1
        if j >= n:
            raise SnippetError(
                f'{doc}:{opener_idx + 1}: snippet directive '
                f'`{source}#{region}` is not followed by a fenced block')
        fm = _FENCE_RE.match(lines[j])
        if not fm:
            raise SnippetError(
                f'{doc}:{opener_idx + 1}: snippet directive '
                f'`{source}#{region}` must be followed by a ``` fence, '
                f'found: {lines[j]!r}')
        indent, marker, info = fm.group(1), fm.group(2), fm.group(3)
        body_start = j + 1
        k = body_start
        while k < n:
            cm = _FENCE_RE.match(lines[k])
            # A CommonMark closing fence is the same character and at
            # least as long as the opener -- so a shorter same-character
            # fence appearing *inside* the body (a 3-tick literal within a
            # 4-tick block) is content, not the close.
            if (cm and cm.group(2)[0] == marker[0]
                    and len(cm.group(2)) >= len(marker)):
                break
            k += 1
        if k >= n:
            raise SnippetError(
                f'{doc}:{j + 1}: unterminated fenced block for snippet '
                f'`{source}#{region}`')
        directives.append(Directive(
            doc=doc, opener_line=opener_idx + 1, source=source, region=region,
            fence_indent=indent, fence_marker=marker, fence_info=info,
            body_start=body_start, body_end=k, current=lines[body_start:k]))
        i = k + 1
    return directives


def _safe_source_path(root: Path, doc: Path, token: str) -> Path:
    """Resolve a directive's source token to a contained, existing file.

    Rejects absolute paths and ``..`` escapes; requires the resolved path
    to stay under *root*; requires the file to exist."""
    p = Path(token)
    if p.is_absolute():
        raise SnippetError(
            f'{doc}: snippet source `{token}` is an absolute path '
            f'(must be repo-relative)')
    if '..' in p.parts:
        raise SnippetError(
            f'{doc}: snippet source `{token}` escapes the repo with `..`')
    resolved = (root / p).resolve()
    root_resolved = root.resolve()
    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise SnippetError(
            f'{doc}: snippet source `{token}` resolves outside the repo root')
    if not resolved.is_file():
        raise SnippetError(
            f'{doc}: snippet source `{token}` does not exist')
    return resolved


def _extract_region(source: Path, region: str, token: str,
                    doc: Path) -> list[str]:
    """Return the lines strictly between the region's start/end markers."""
    start_needle = f'snippet-start: {region}'
    end_needle = f'snippet-end: {region}'
    text = source.read_text(encoding='utf-8', errors='replace')
    src_lines = text.split('\n')
    starts = [i for i, ln in enumerate(src_lines) if start_needle in ln]
    ends = [i for i, ln in enumerate(src_lines) if end_needle in ln]
    if len(starts) == 0:
        raise SnippetError(
            f'{doc}: region `{region}` not found in `{token}` '
            f'(no line containing `{start_needle}`)')
    if len(starts) > 1 or len(ends) > 1:
        raise SnippetError(
            f'{doc}: region `{region}` is ambiguous in `{token}` '
            f'(multiple start/end markers)')
    if len(ends) == 0 or ends[0] < starts[0]:
        raise SnippetError(
            f'{doc}: region `{region}` in `{token}` is not terminated '
            f'(missing `{end_needle}` after the start)')
    return src_lines[starts[0] + 1:ends[0]]


@dataclass
class DocResult:
    doc: Path
    drifted: int = 0


def _process_doc(doc: Path, root: Path, *, sync: bool) -> DocResult:
    # Containment: never read -- and in --sync never *rewrite* -- a
    # directive-bearing document outside the repo root. The source path
    # is contained separately (_safe_source_path); this guards the write
    # target itself against a stray absolute / escaping doc argument.
    doc_resolved = doc.resolve()
    root_resolved = root.resolve()
    if doc_resolved != root_resolved and root_resolved not in doc_resolved.parents:
        raise SnippetError(
            f'{doc}: document is outside the repo root '
            f'(refusing to read/rewrite it)')
    text = doc.read_text(encoding='utf-8', errors='replace')
    lines = text.split('\n')
    directives = _parse_directives(doc, lines)
    res = DocResult(doc=doc)
    if not directives:
        return res
    # Apply from the bottom up so edits don't shift earlier indices.
    new_lines = list(lines)
    for d in sorted(directives, key=lambda x: x.body_start, reverse=True):
        source = _safe_source_path(root, doc, d.source)
        want = _extract_region(source, d.region, d.source, doc)
        if d.current != want:
            res.drifted += 1
            if sync:
                new_lines[d.body_start:d.body_end] = want
    if sync and res.drifted:
        doc.write_text('\n'.join(new_lines), encoding='utf-8')
    return res


def repo_root() -> Path:
    try:
        out = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True, text=True, check=True,
            cwd=str(Path(__file__).resolve().parent),
        )
        return Path(out.stdout.strip())
    except (subprocess.CalledProcessError, OSError):
        return Path.cwd()


def tracked_markdown(root: Path) -> list[Path]:
    """Tracked ``*.md`` paths that exist on disk.

    ``git ls-files`` still lists a file whose deletion is not yet committed
    (and a tracked symlink whose target is gone); reading either raises, so
    both are dropped and counted.  The note on stderr names no tool on
    purpose: ``check_cairn`` calls this same function, so a tool-name prefix
    here would sometimes name the wrong tool."""
    out = subprocess.run(
        ['git', 'ls-files', '*.md'], cwd=str(root),
        capture_output=True, text=True, check=True,
    )
    listed = [root / line for line in out.stdout.splitlines() if line.strip()]
    present = [path for path in listed if path.is_file()]
    skipped = len(listed) - len(present)
    if skipped:
        print(f'skipped {skipped} tracked Markdown file(s) not present on '
              f'disk', file=sys.stderr)
    return present


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='sync_doc_snippets',
        description='Keep doc code blocks in lockstep with source regions.')
    parser.add_argument('files', nargs='*', type=Path,
                        help='Specific Markdown docs (default: whole tree).')
    parser.add_argument('--root', type=Path, default=None,
                        help='Repo root (default: git toplevel).')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true',
                      help='Report drift and exit 1 if any (default).')
    mode.add_argument('--sync', action='store_true',
                      help='Rewrite drifted blocks from their source.')
    args = parser.parse_args(argv)

    root = args.root.resolve() if args.root else repo_root()
    if not root.is_dir():
        print(f'sync_doc_snippets: root is not a directory: {root}',
              file=sys.stderr)
        return 2
    files = [f.resolve() for f in args.files] if args.files \
        else tracked_markdown(root)
    if not files:
        print('sync_doc_snippets: no Markdown files found.', file=sys.stderr)
        return 2

    total_drift = 0
    synced = 0
    try:
        for doc in files:
            res = _process_doc(doc, root, sync=args.sync)
            if res.drifted:
                total_drift += res.drifted
                try:
                    rel = doc.resolve().relative_to(root)
                except ValueError:
                    rel = doc
                if args.sync:
                    synced += res.drifted
                    print(f'  synced {res.drifted} block(s) in {rel}')
                else:
                    print(f'  {rel}: {res.drifted} snippet(s) drifted from '
                          f'source', file=sys.stderr)
    except SnippetError as exc:
        print(f'sync_doc_snippets: {exc}', file=sys.stderr)
        return 1

    if args.sync:
        print(f'sync_doc_snippets: synced {synced} block(s).')
        return 0
    if total_drift:
        print(f'sync_doc_snippets: {total_drift} drifted snippet(s) -- run '
              f'with --sync to update.', file=sys.stderr)
        return 1
    print(f'sync_doc_snippets: OK -- {len(files)} doc(s) scanned; no drift.')
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
