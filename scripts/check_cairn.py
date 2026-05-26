#!/usr/bin/env python3
"""Cairn self-check -- prose-integrity gate over Cairn's own Markdown tree.

Cairn ships a ``claim-check`` *methodology module* and tells adopters to
"absorb tests, docs, and examples into every change."  This script makes
that true of Cairn itself: it runs Cairn's own discipline *on Cairn*, so
the repo visibly passes the gate it preaches.  It is deliberately thin --
a prose-integrity check, **not** a behavioral test suite (Cairn is
methodology, not software; behavioral tests stay scoped to
``bootstrap/tests/``).

Three checks, all deterministic and offline by default:

1. **Link check.**  Every internal Markdown link / image and reference
   definition resolves: relative file targets exist, and intra-document
   heading **anchors** resolve under **GitHub slug rules** (lowercase;
   drop punctuation except hyphen/underscore; spaces -> hyphens; dedupe
   repeats with ``-1``, ``-2`` ...).  This is the one documented target
   rendering convention -- Cairn is read on GitHub.  External
   ``http(s)`` links are NOT fetched unless ``--check-external``.
2. **Claim-path check.**  Cairn *runs the exact tool it ships*: this
   script imports the claim-path checker from the packaged reference
   script (``templates/modules/default-on/claim_check.py``) -- the same
   file the scaffold installs into an adopter's ``scripts/`` -- rather
   than carrying a second, drift-prone copy.  A backticked token whose
   first ``/``-segment is a real top-level entry of the Cairn repo is
   resolved against the tree; fenced / indented code, HTML comments,
   and blockquotes are skipped; ``Proposed path:`` / ``Untracked path:``
   / ``External-repo path:`` markers are exempt.

   **Case studies describe external repos.**  ``case-studies/*.md`` write
   up *other* projects (modflow_tools, LHM) and cite their relative
   paths, which routinely collide with a Cairn top-level dir name
   (``scripts/``, ``docs/``).  Those files are passed to the checker's
   file-scoped **external-path allowance**, so their path-claims are not
   resolved against the Cairn tree -- the generalized, durable form of
   the per-collision patches that were applied by hand as Cairn grew.
3. **Content-integrity check (Layer 2).**  Composes the Cairn-internal
   ``content_scan.py`` over the prose **by file class** (templates ->
   instruction files strictest, with URL flagging on; doctrine / docs /
   case-study prose lighter).  A **tripwire that forces human review,
   not a safety proof** -- it flags imperative-override / egress /
   suspicious-URL / unicode-obfuscation / instruction-bearing-comment
   patterns; a reviewed hit is cleared with an inline ``cairn-accept``
   marker.  Disable with ``--no-content-scan``.

Scanned set: the whole tracked Markdown tree (``git ls-files '*.md'``).

Usage::

    python scripts/check_cairn.py                 # check the whole tree
    python scripts/check_cairn.py --check-external # also probe http(s) links
    python scripts/check_cairn.py PATH ...         # check specific files

Exit codes: ``0`` clean; ``1`` at least one broken link / anchor / path;
``2`` usage error.

Source proposal / plan: the modflow_tools-hosted
``cairn-self-application-and-docs`` arc (Chunk 1) established this
self-check; the Cairn v0.2 P1 ``reference-scripts`` arc unified its
claim-path half onto the packaged generic checker.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------
# Compose the *shipped* generic claim-checker (the dogfood: Cairn runs the
# exact claim-path tool it installs into adopters).  Imported from the
# packaged reference script rather than re-implemented here, so there is
# no second copy to drift.  Loading a module from a file path needs the
# module registered in sys.modules *before* exec, or its @dataclass
# definitions fail their cls.__module__ lookup.

_CLAIM_CHECK_SRC = (
    Path(__file__).resolve().parents[1]
    / 'templates' / 'modules' / 'default-on' / 'claim_check.py'
)


#: The content-integrity scanner (Layer 2/3), a sibling Cairn dev tool.
_CONTENT_SCAN_SRC = Path(__file__).resolve().parent / 'content_scan.py'


def _load_module(name: str, path: Path, what: str):
    """Import a Cairn helper module from a file path.  Registers it in
    sys.modules before exec so its @dataclass definitions resolve (the
    spec_from_file_location gotcha)."""
    if not path.is_file():
        raise FileNotFoundError(
            f'check_cairn: packaged {what} not found at {path} -- the '
            f'Cairn tree is incomplete.'
        )
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module          # required before exec_module
    spec.loader.exec_module(module)
    return module


# Compose the shipped claim-path checker (P1) and the content-integrity
# scanner (P2 Layer 2/3) -- check_cairn runs the exact tools, no copies.
claim_check = _load_module(
    'cairn_claim_check', _CLAIM_CHECK_SRC, 'claim-checker')
content_scan = _load_module(
    'cairn_content_scan', _CONTENT_SCAN_SRC, 'content scanner')

#: File globs (relative to the repo root) whose backticked path-claims
#: describe an EXTERNAL repository and must not be resolved against the
#: Cairn tree.  Case studies write up other projects; folding this in is
#: ledger item E (Cairn v0.2 P1).
_EXTERNAL_ALLOW: list[str] = ['case-studies/*.md']

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
# Link-checking (retained here; the shipped claim-checker is claim-only).
# Markdown scanning (scannable_lines) is shared from the claim-checker so
# the two checks see the same prose lines.

# Inline links + images: optional '!', [text](target "title").
_LINK_RE = re.compile(r'!?\[[^\]]*\]\(\s*([^)\s]+)(?:\s+"[^"]*")?\s*\)')
# Reference definitions: [id]: target  (optionally with a title).
_REFDEF_RE = re.compile(r'^\s*\[[^\]]+\]:\s*(\S+)')
_HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')


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
    kind: str        # 'link' | 'anchor' | 'path' | 'line-bounds'
    message: str


@dataclass
class Result:
    flags: list[Flag] = field(default_factory=list)
    external_links: int = 0
    files_scanned: int = 0


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


def _check_claims(
    md: Path, root: Path, result: Result, external_allow: list[str],
) -> None:
    """Run the *shipped* generic claim-path checker over one file and
    fold its hard flags into ``result``.

    Delegates to ``claim_check.check_file`` -- the exact tool the scaffold
    installs -- including its file-scoped external-path allowance (E).
    Soft (count) flags are advisory and not surfaced by the self-check.
    """
    cr = claim_check.check_file(md, root, external_allow=external_allow)
    for f in cr.hard_flags:
        result.flags.append(Flag(md, f.line, f.kind, f.message))


def _is_template_instruction(rel: str) -> bool:
    """True for *source template -> instruction* files (Rule 7's
    strictest class) -- the files that become an adopter's agent-loaded
    ``AGENTS.md`` / ``dev/`` tree.  These are scanned with URL flagging
    on (an executed template should carry no live egress target);
    doctrine / docs / case-study prose is the lighter class (URLs are
    legitimate references there)."""
    return rel.startswith('templates/')


def _check_content(md: Path, root: Path, result: Result) -> None:
    """Run the content-integrity scanner (Layer 2) over one file, by
    file class, and fold its flags into ``result``.

    Composes ``content_scan`` -- the exact Cairn-internal tool -- rather
    than re-implementing it (check_cairn stays a thin orchestrator).  A
    flag is a tripwire that forces human review; suppress a reviewed hit
    with an inline ``cairn-accept`` marker.
    """
    try:
        rel = md.resolve().relative_to(root).as_posix()
    except ValueError:
        rel = md.name
    scan_urls = _is_template_instruction(rel)
    for f in content_scan.scan_file(md, scan_urls=scan_urls):
        result.flags.append(
            Flag(md, f.line, 'content', f'[{f.pattern_id}] {f.message}'))


# --------------------------------------------------------------------------
# Driver


def check_tree(root: Path, files: list[Path],
               check_external: bool = False,
               external_allow: list[str] | None = None,
               content_scan_enabled: bool = True) -> Result:
    allow = external_allow if external_allow is not None else _EXTERNAL_ALLOW
    anchors_by_file: dict[Path, set[str]] = {}
    result = Result()
    for md in files:
        text = md.read_text(encoding='utf-8', errors='replace')
        scannable = claim_check.scannable_lines(text)
        result.files_scanned += 1
        _check_links(md, root, scannable, anchors_by_file, result,
                     check_external)
        _check_claims(md, root, result, allow)
        if content_scan_enabled:
            _check_content(md, root, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='check_cairn',
        description="Cairn self-check: link / anchor / claim-path / "
                    "content-integrity over Cairn's own Markdown tree.",
    )
    parser.add_argument('files', nargs='*', type=Path,
                        help='Specific Markdown files (default: whole tree).')
    parser.add_argument('--root', type=Path, default=None,
                        help='Repo root (default: git toplevel).')
    parser.add_argument('--check-external', action='store_true',
                        help='Also probe http(s) links (network; off by '
                             'default).')
    parser.add_argument('--no-content-scan', action='store_true',
                        help='Skip the Layer-2 content-integrity scan '
                             '(link + claim-path checks only).')
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

    result = check_tree(
        root, files, check_external=args.check_external,
        content_scan_enabled=not args.no_content_scan,
    )

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
