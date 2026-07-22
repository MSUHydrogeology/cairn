#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

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

#: The live-invariant count verifier + its registry (Cairn-maintainer-only
#: dev tools, siblings of this script in ``scripts/``).  check_cairn runs
#: ``verify_counts`` over its own docs so a registered drift-prone count
#: (a doc number annotated ``<!-- verify: <key> -->``) is re-measured on
#: every self-check.  Both are deliberately NOT installed into adopters
#: (not in ``_CORE_MAPPINGS``), and check_cairn is itself Cairn-only, so
#: wiring them here keeps the verifier out of every adopter tree.
_VERIFY_COUNTS_SRC = Path(__file__).resolve().parents[1] / 'scripts' / 'verify_counts.py'
_MEASUREMENTS_SRC = Path(__file__).resolve().parents[1] / 'scripts' / 'measurements.py'


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
# Loaded as a pair: verify_counts.verify_text does isinstance() against
# measurements.Snapshot, so the registry and the verifier must share one
# measurements module object.
measurements = _load_module(
    'cairn_measurements', _MEASUREMENTS_SRC, 'measurement registry')
verify_counts = _load_module(
    'cairn_verify_counts', _VERIFY_COUNTS_SRC, 'count verifier')

#: File globs (relative to the repo root) whose backticked path-claims
#: describe an EXTERNAL repository and must not be resolved against the
#: Cairn tree.  Case studies write up other projects; folding this in is
#: ledger item E (Cairn v0.2 P1).
_EXTERNAL_ALLOW: list[str] = ['case-studies/*.md']

#: #58 loop-fidelity gate -- Cairn-internal-only path prefixes: directories
#: shipped in the Cairn source tree but NOT copied into an adopter's install
#: set, so an adopter-facing surface that references them dangles once
#: installed (the implementation->adoption failure: #57's session-routine
#: doctrine, the 9-lens review roster). ``doctrine/`` is the flagship and only
#: v1 member -- every observed failure referenced un-transplanted doctrine;
#: the set is intentionally narrow to hold down false positives. Extend only
#: with a verified not-installed prefix.
_CAIRN_INTERNAL_PREFIXES: tuple[str, ...] = ('doctrine/',)

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
    md: Path, root: Path, text: str,
    anchors_by_file: dict[Path, set[str]], result: Result,
    check_external: bool, allow_hosts: set[str] | None = None,
) -> None:
    """Delegate link / anchor checking to the shipped ``link_check`` tool
    and fold its flags + external-link count into ``result``.

    The link check honors ``link_check``'s two exemptions so a ``check_cairn``
    run treats quoted + cross-repo links the same as the standalone tool: each
    scannable line has its **balanced inline code spans stripped**
    (``strip_code_spans``), and the file-level ``link-check-allow`` directive is
    parsed + applied. It keeps ``check_cairn``'s own prose extraction
    (``claim_check.scannable_lines`` -- which drops blockquotes / fenced / indented
    code so *illustrative* links in quoted examples are not live-checked), so this
    wiring adds the exemptions without changing which lines count as prose.
    Importing the checker (rather than re-implementing it) keeps a single
    link-check implementation -- including its SSRF-guarded ``--check-external``
    probe."""
    scannable = [(lineno, link_check.strip_code_spans(line))
                 for lineno, line in claim_check.scannable_lines(text)]
    link_allow = link_check.parse_link_allow_directives(text)
    flags, n_external = link_check.check_links(
        md, root, scannable, anchors_by_file, check_external=check_external,
        allow_hosts=allow_hosts, link_allow=link_allow)
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


def _check_counts(md: Path, text: str, result: Result) -> None:
    """Re-measure registered live-invariant counts annotated in one file.

    Delegates to the shipped ``verify_counts`` verifier over the code-side
    ``measurements.REGISTRY``: a doc that annotates a number with
    ``<!-- verify: <key> -->`` is checked against today's measurement (an
    ``Invariant``) or its frozen value (a ``Snapshot``).  A file with no
    annotations is a no-op.

    Only *failures* — drift, an unregistered-key refusal, or a measurement
    error — become check_cairn flags.  A visible *skip* (an ``Invariant``
    whose sibling root is absent, RR2) is printed but does **not** fail the
    gate, so a contributor lacking a registered sibling checkout is not
    blocked; the seed registry's roots are local to the Cairn tree, so a
    skip is not normally reached here.
    """
    for r in verify_counts.verify_text(text, md, measurements.REGISTRY,
                                       measurements):
        if r.status in ('drift', 'refused', 'error'):
            result.flags.append(Flag(md, r.line, f'count-{r.status}', r.message))
        elif r.status == 'skipped':
            print(f'  {md}:{r.line}: [count-skip] {r.message}', file=sys.stderr)


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
# #58 loop-fidelity gate: dangling Cairn-internal references

#: Exemption markers (parallel to ``claim-check-allow`` / ``cairn-accept``):
#: assert a reference to a Cairn-internal path is a deliberate deeper-why
#: *citation*, not adopter-load-bearing content the install set must carry.
#: File-level ``cairn-internal-ref-allow: <paths…> reason=…`` exempts the
#: named paths for the whole file (like ``claim-check-allow``); inline
#: same-line ``cairn-internal-ref: <paths…> reason=…`` exempts that line.
_INTERNAL_REF_FILE_ALLOW_RE = re.compile(r'cairn-internal-ref-allow:\s*([^\n]*)')
_INTERNAL_REF_INLINE_RE = re.compile(r'(?<!-)cairn-internal-ref:\s*([^\n]*)')
_BACKTICK_PATH_RE = re.compile(r'`([^`\n]+)`')
_MD_LINK_TARGET_RE = re.compile(r'\]\(([^)\s]+)\)')


def _parse_allow_spec(spec: str) -> set[str]:
    """Path tokens listed before an optional ``reason=`` in a
    ``cairn-internal-ref`` marker. A token needs a path separator
    (``doctrine/dual-review.md``, or the bare prefix ``doctrine/``); a stray
    prose word is ignored. **R1:** a bare directory name that *matches a known
    internal prefix* (e.g. ``doctrine``) is normalized to ``doctrine/`` so an
    operator who omits the trailing slash is not silently dropped."""
    out: set[str] = set()
    for raw in re.split(r'[\s,]+', spec.split('reason=')[0]):
        tok = raw.strip().rstrip('.,;:')
        if not tok:
            continue
        if '/' in tok:
            out.add(tok)
        elif any(prefix == tok + '/' for prefix in _CAIRN_INTERNAL_PREFIXES):
            out.add(tok + '/')
    return out


def _ref_is_internal(tok: str) -> str | None:
    """The Cairn-internal path a backtick token / link target names (with a
    trailing anchor and leading ``./`` / ``../`` stripped), or None."""
    path = tok.split('#', 1)[0].strip().rstrip('.,;:)')
    norm = re.sub(r'^(?:\./|\.\./)+', '', path)
    if any(norm.startswith(p) for p in _CAIRN_INTERNAL_PREFIXES):
        return norm
    return None


def _check_dangling_internal_refs(md: Path, root: Path, result: Result) -> None:
    """#58 loop-fidelity gate. In an adopter-facing template surface, flag a
    reference to a Cairn-internal-only path (``doctrine/*``) that would dangle
    once installed in an adopter tree (the path is not in the install set).

    Scans BOTH backticked path tokens and raw Markdown link targets (N1: a
    relative ``[x](doctrine/..)`` link resolves in the Cairn source so
    ``link_check`` passes it, then breaks on adoption). Fail-closed. Exempt a
    deliberate deeper-why citation with a ``cairn-internal-ref-allow:
    <paths…> reason=…`` directive (parallel to ``claim-check-allow``) or a
    ``cairn-internal-ref: <paths…> reason=…`` marker. Both forms are collected
    **file-wide** and exempt the *named* paths anywhere in the file (robust to
    wrapped prose). Listing the **specific** paths (not a bare ``doctrine/``
    prefix) keeps the gate sharp -- a new reference to an unlisted internal
    path still fails closed."""
    text = md.read_text(encoding='utf-8', errors='replace')
    allowed: set[str] = set()
    for rx in (_INTERNAL_REF_FILE_ALLOW_RE, _INTERNAL_REF_INLINE_RE):
        for m in rx.finditer(text):
            allowed |= _parse_allow_spec(m.group(1))
    for i, line in enumerate(text.splitlines(), start=1):
        for rx in (_BACKTICK_PATH_RE, _MD_LINK_TARGET_RE):
            for m in rx.finditer(line):
                path = _ref_is_internal(m.group(1))
                if path is None:
                    continue
                if any(path == a or path.startswith(a) for a in allowed):
                    continue
                result.flags.append(Flag(
                    md, i, 'path',
                    f'[loop-fidelity] adopter-facing surface references '
                    f'Cairn-internal-only path `{path}` -- it dangles once '
                    f'installed (not in the adopter install set). Transplant '
                    f'the content into the install set, or mark a deliberate '
                    f'citation: file-level `cairn-internal-ref-allow: {path} '
                    f'reason=…` or inline `cairn-internal-ref: {path} '
                    f'reason=…`.'))


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
        result.files_scanned += 1
        _check_links(md, root, text, anchors_by_file, result,
                     check_external, allow_hosts)
        _check_claims(md, root, result, allow)
        _check_counts(md, text, result)
        if content_scan_enabled:
            _check_content(md, root, result)
        _check_incident_tracker_schema(md, root, result)
        try:
            rel = md.resolve().relative_to(root).as_posix()
        except ValueError:
            rel = md.name
        if _is_template_instruction(rel):
            _check_dangling_internal_refs(md, root, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='check_cairn',
        description="Cairn self-check: link / anchor / claim-path / "
                    "content-integrity / live-count-verify over Cairn's "
                    "own Markdown tree.",
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
    parser.add_argument('--include-archives', action='store_true',
                        help='Also scan sources under dev/**/archive/ and '
                             'dev/reflections/ (skipped by default -- '
                             'archived links rot by design). Mirrors the '
                             'shipped link_check default; ignored when '
                             'explicit files are named.')
    args = parser.parse_args(argv)

    root = args.root.resolve() if args.root else repo_root()
    if not root.is_dir():
        print(f'check_cairn: root is not a directory: {root}', file=sys.stderr)
        return 2
    if args.files:
        files = [f.resolve() for f in args.files]
    else:
        files = link_check.filter_sources(
            tracked_markdown(root), root,
            include_archives=args.include_archives,
        )
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
