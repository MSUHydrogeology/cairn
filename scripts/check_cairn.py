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
   up *other* projects and cite their relative
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

Source proposal / plan: the
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
_CONTENT_SCAN_SRC = (
    Path(__file__).resolve().parents[1]
    / 'templates' / 'modules' / 'team-gated' / 'content_scan.py'
)

#: The shipped generic link-checker (the doc-drift-prevention module's
#: link half).  Imported from the packaged tool the scaffold installs --
#: the same dogfood discipline used for claim_check below -- so Cairn runs
#: the exact link-checker it hands an adopter and there is no second copy.
_LINK_CHECK_SRC = (
    Path(__file__).resolve().parents[1]
    / 'templates' / 'modules' / 'team-gated' / 'link_check.py'
)


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
link_check = _load_module(
    'cairn_link_check', _LINK_CHECK_SRC, 'link-checker')

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
# Link-checking is delegated to the shipped generic ``link_check`` tool
# (composed above), so Cairn runs the exact link-checker it installs into
# an adopter.  ``check_cairn`` passes its own ``scannable_lines`` (from the
# claim-checker) so the link and claim checks see the same prose lines.

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
    check_external: bool, allow_hosts: set[str] | None = None,
) -> None:
    """Delegate link / anchor checking to the shipped ``link_check`` tool
    and fold its flags + external-link count into ``result``.

    Passing ``check_cairn``'s own ``scannable`` lines keeps the link and
    claim checks aligned to the same prose; importing the checker (rather
    than re-implementing it) keeps a single link-check implementation --
    including its SSRF-guarded ``--check-external`` probe."""
    flags, n_external = link_check.check_links(
        md, root, scannable, anchors_by_file, check_external=check_external,
        allow_hosts=allow_hosts)
    for f in flags:
        result.flags.append(Flag(md, f.line, f.kind, f.message))
    result.external_links += n_external


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


#: Canonical incident-tracker schema (per the incident-trackers
#: module, Cairn commit 4998abd).  An incident-tracker file's
#: Markdown table header MUST carry these column names (in any
#: order) for the cross-adopter harvest to parse it.  Per
#: Antigravity External code review C-P2: validate Cairn-side
#: tracker artifacts at check_cairn time so schema drift surfaces
#: locally rather than at upstream-harvest time.
_INCIDENT_TRACKER_CANONICAL_COLUMNS: tuple[str, ...] = (
    "Date",
    "Event Class",
    "Description",
    "Recurrence-Window Match",
    "Impact",
    "Migrated From Reflection",
    "Resolved By",
)

#: A file looks like an incident tracker if it cross-references
#: the rate-limit gate AND carries a Markdown table header line.
_TRACKER_SIGNAL_RE = re.compile(
    r"rate-limit\s+gate|adaptive-doctrine\s+rate-limit",
    re.IGNORECASE,
)


def _check_incident_tracker_schema(
    md: Path, root: Path, result: Result,
) -> None:
    """Per Antigravity C-P2: validate any file that looks like an
    incident tracker carries the canonical 7-column semantic-field
    schema.

    Detection (conservative): the file body references the
    rate-limit gate AND carries at least one Markdown table whose
    header includes "Date" or "Event Class".  Validation: every
    canonical column name must appear in the table's first header
    row (substring match; the canonical set is the contract).
    Adopters may append columns to the right of the canonical
    set; appended columns don't trigger flags.

    Files that don't match the tracker shape are silently skipped
    (no false positives on unrelated tables).
    """
    text = md.read_text(encoding="utf-8", errors="replace")
    if _TRACKER_SIGNAL_RE.search(text) is None:
        return
    # Find table header lines (the first `|`-separated line).
    in_table = False
    header_line: str | None = None
    header_lineno = 0
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            in_table = False
            continue
        if not in_table:
            # First `|...|` line of a table is the header.
            header_line = stripped
            header_lineno = i
            in_table = True
            break
    if header_line is None:
        return
    # Cheap "table looks like an incident tracker" check.
    if "Date" not in header_line and "Event Class" not in header_line:
        return
    # Validate canonical columns are present.
    missing = [
        col for col in _INCIDENT_TRACKER_CANONICAL_COLUMNS
        if col not in header_line
    ]
    if missing:
        result.flags.append(
            Flag(
                md, header_lineno, "content",
                "[incident-tracker-schema] table header is missing "
                "canonical column(s): " + ", ".join(missing)
                + " (see templates/modules/default-on/"
                + "incident-trackers.md for the canonical schema)",
            )
        )


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
               content_scan_enabled: bool = True,
               allow_hosts: set[str] | None = None) -> Result:
    allow = external_allow if external_allow is not None else _EXTERNAL_ALLOW
    anchors_by_file: dict[Path, set[str]] = {}
    result = Result()
    for md in files:
        text = md.read_text(encoding='utf-8', errors='replace')
        scannable = claim_check.scannable_lines(text)
        result.files_scanned += 1
        _check_links(md, root, scannable, anchors_by_file, result,
                     check_external, allow_hosts)
        _check_claims(md, root, result, allow)
        if content_scan_enabled:
            _check_content(md, root, result)
        _check_incident_tracker_schema(md, root, result)
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
                             'default). SSRF-guarded via the shipped '
                             'link_check (http(s) only, per-hop host '
                             'validation, non-public IPs refused).')
    parser.add_argument('--allow-host', action='append', dest='allow_hosts',
                        metavar='HOST', default=None,
                        help='Permit a specific internal hostname under '
                             '--check-external (repeatable).')
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
        allow_hosts=set(args.allow_hosts or []),
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
