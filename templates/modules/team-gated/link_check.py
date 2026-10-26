#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Markdown link / anchor integrity checker -- stack-neutral, stdlib-only.

The ``doc-drift-prevention`` module installs this verbatim into an
adopting repo's ``scripts/`` directory. It is the **link half** of a
doc-drift gate: it confirms that every internal Markdown link, image,
and reference definition resolves -- relative file targets exist, and
intra-document heading **anchors** resolve under GitHub slug rules. It
does **not** check claim-paths or line citations (the ``claim-check``
module ships that half, ``claim_check.py``) and it carries none of
Cairn's own content-scan tripwires; this keeps the two gates
single-sourced and composable rather than duplicated.

Anchor rules follow GitHub's ``github-slugger``: lowercase; drop
punctuation except hyphen / underscore; spaces -> hyphens; **no**
hyphen collapse or trim; repeated headings dedupe with ``-1``, ``-2``.
External ``http(s)`` links are NOT fetched unless ``--check-external``.

**Inline code-span exemption.**  A Markdown file-link that appears
inside a *balanced* inline code span (backtick-delimited) is literal
text, not a live link -- it must not be checked.  Fenced code blocks
are already skipped by ``scannable_lines``; this checker additionally
strips balanced inline code spans from each scannable line *before*
link extraction.  Only *balanced* spans are stripped: the closing
backtick run must exactly match the opening run.  An unmatched backtick
leaves the rest of the line intact and still checked (safety contract
-- a greedy/naive strip could silently eat a real link).

**File-level ``link-check-allow`` directive.**  An HTML-comment
directive lets a file's author exempt specific link targets from the
broken-link check::

    <!-- link-check-allow: relative/path/one.md, relative/path/two.md -->

Listed targets (comma-separated, resolved relative to the file being
checked) are exempted from the ``broken link target`` check in that
file.  The directive is its own namespace (``link-check-allow``), with
no dependency on the sibling ``claim-check-allow`` directive -- an
adopter who disables claim_check but keeps link_check will not
accidentally inherit a claim_check-named directive.  Only
*explicitly-listed* targets are exempted; a genuinely-broken link that
is not listed is still flagged.

Usage::

    python scripts/link_check.py                  # whole tracked tree (files on disk)
    python scripts/link_check.py PATH ...          # specific files
    python scripts/link_check.py --check-external  # also probe http(s)

Exit codes: ``0`` clean; ``1`` at least one broken link / anchor;
``2`` usage error.

Vendor-neutral and standard-library only -- nothing to clone or port.
"""
from __future__ import annotations

import argparse
import ipaddress
import re
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urljoin, urlsplit

# Inline links + images: optional '!', [text](target "title").
_LINK_RE = re.compile(r'!?\[[^\]]*\]\(\s*([^)\s]+)(?:\s+"[^"]*")?\s*\)')
# Reference definitions: [id]: target  (optionally with a title).
_REFDEF_RE = re.compile(r'^\s*\[[^\]]+\]:\s*(\S+)')
_HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
# Explicit Pandoc/kramdown-style anchor attribute at the end of a heading:
# ``{#some-id}``.  Group 1 is the id text (no leading #).  The pattern
# allows arbitrary whitespace before the ``{`` so ``### Title {#id}`` and
# ``### Title{#id}`` both match.
_EXPLICIT_ANCHOR_RE = re.compile(r'\s*\{#([^}]+)\}\s*$')

# Balanced inline code span: a run of one or more backticks, followed by
# any text (non-newline), closed by a backtick run of EXACTLY the same
# length.  The backreference ``\1`` alone is not enough -- it can match a
# *prefix* of a longer closing run (e.g. ``​``opener of 2 closed by a run
# of 3), silently eating a real link.  So the
# run is anchored on both sides: ``(?<!`)`` before the opener makes ``(`+)``
# capture the *whole* opening run (not a sub-run of a longer one), and
# ``(?!`)`` after ``\1`` requires the closing run to be exactly that length
# (not a prefix of a longer run).  An unmatched / mismatched run in EITHER
# direction therefore leaves the rest of the line intact and still checked
# (safety contract).  No re.DOTALL: we operate per-line.
_BALANCED_CODE_SPAN_RE = re.compile(r'(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)')

# File-level link-check-allow directive.  A standalone HTML-comment line
# ``<!-- link-check-allow: target1, target2 -->`` lists link targets that
# are consciously exempted from the broken-link check in this file.  The
# directive must stand alone on its line -- a comment line that *shows*
# the directive (e.g. inside a paragraph quoting an example) is not
# parsed as live.  This is its own namespace: it has NO dependency on the
# sibling ``claim-check-allow`` directive.
_LINK_ALLOW_DIRECTIVE_RE = re.compile(
    r'^<!--\s*link-check-allow:\s*(?P<targets>.*?)\s*-->$'
)


def strip_code_spans(line: str) -> str:
    """Strip balanced inline code spans from *line* before link extraction.

    Only *balanced* spans are removed: the closing backtick run must
    exactly match the opening run length.  An unmatched backtick (or a
    span whose closing run has a different length) leaves the rest of
    the line intact and still checked -- this is the safety contract,
    preventing a greedy/naive strip from silently eating a real link.

    Fenced code blocks are already skipped by ``scannable_lines``; this
    function handles the INLINE-span case only.
    """
    return _BALANCED_CODE_SPAN_RE.sub('', line)


def parse_link_allow_directives(text: str) -> set[str]:
    """Return the set of link targets declared exempt by
    ``<!-- link-check-allow: ... -->`` directives in *text*.

    Targets are comma-separated.  Each is stripped of surrounding
    whitespace.  Empty entries are skipped.  The directive must stand
    alone on its line (matching the ``claim-check-allow`` convention).
    This is its own namespace -- there is no dependency on, or
    inheritance from, the ``claim-check-allow`` directive.
    """
    exempt: set[str] = set()
    for raw_line in text.split('\n'):
        m = _LINK_ALLOW_DIRECTIVE_RE.match(raw_line.strip())
        if m is None:
            continue
        for raw in m.group('targets').split(','):
            target = raw.strip()
            if target:
                exempt.add(target)
    return exempt


@dataclass
class Flag:
    file: Path
    line: int
    kind: str        # 'link' | 'anchor'
    message: str


@dataclass
class Result:
    flags: list[Flag] = field(default_factory=list)
    external_links: int = 0
    files_scanned: int = 0


def github_slug(heading_text: str) -> str:
    """GitHub heading-anchor slug: lowercase; drop punctuation except
    hyphen / underscore; spaces -> hyphens.

    Consecutive hyphens are intentionally NOT collapsed and
    leading/trailing hyphens are NOT stripped -- this matches GitHub's
    ``github-slugger`` (``value.toLowerCase().replace(regex, '')
    .replace(/ /g, '-')``), so a heading like ``Rule 1 -- No content``
    slugs with the double hyphen the surrounding spaces produce.
    Collapsing/stripping here would diverge from GitHub and false-flag
    correct anchor links.
    """
    s = heading_text.strip().lower()
    s = s.replace('`', '')                            # inline code ticks
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)    # link -> its text
    s = re.sub(r'[^\w\s-]', '', s)                    # drop punctuation
    s = s.replace(' ', '-')
    return s


def scannable_lines(text: str) -> list[tuple[int, str]]:
    """Return ``(lineno, line)`` pairs outside fenced code and HTML
    comments -- the lines a link check should look at. Line numbers are
    1-based. (Blockquote and inline prose links *are* checked; a link in
    a blockquote still has a real target.)"""
    out: list[tuple[int, str]] = []
    in_fence = False
    in_comment = False
    for i, raw in enumerate(text.split('\n'), start=1):
        if re.match(r'^ {0,3}(```|~~~)', raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = raw
        if in_comment:
            if '-->' in line:
                in_comment = False
                line = line.split('-->', 1)[1]
            else:
                continue
        # Strip any complete <!-- ... --> on the line, then detect an
        # unterminated comment opener.
        line = re.sub(r'<!--.*?-->', '', line)
        if '<!--' in line:
            line = line.split('<!--', 1)[0]
            in_comment = True
        out.append((i, strip_code_spans(line)))
    return out


def file_anchors(text: str) -> set[str]:
    """Heading anchors for a file, with GitHub's repeat-dedupe (-1, -2).

    Recognises explicit Pandoc/kramdown-style anchor attributes
    (``{#custom-id}`` at the end of the heading text): when present, the
    **literal id** (stripped of leading ``#`` and surrounding whitespace)
    is registered directly, **and** the auto-slug of the heading text
    *without* the ``{#…}`` attribute is also registered (so both forms of
    reference resolve).  Without an explicit anchor the original GitHub-
    slug behaviour is unchanged.

    This prevents the double-slug bug where a heading ``### T {#t}``
    would previously be fed into ``github_slug`` as ``T {#t}``, producing
    ``t-t`` (the braces content got mixed in), while the intended anchor
    ``#t`` silently resolved to nothing.
    """
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
        heading_text = m.group(2)
        explicit_m = _EXPLICIT_ANCHOR_RE.search(heading_text)
        if explicit_m:
            explicit_id = explicit_m.group(1).strip()
            # Also register the auto-slug of the text *without* the
            # ``{#…}`` attribute so ``[link](#auto-slug)`` still resolves
            # even when the author added an explicit id.
            text_without_attr = heading_text[:explicit_m.start()]
            auto_base = github_slug(text_without_attr)
            if explicit_id:
                anchors.add(explicit_id)
            if auto_base:
                n = counts[auto_base]
                counts[auto_base] += 1
                anchors.add(auto_base if n == 0 else f'{auto_base}-{n}')
        else:
            base = github_slug(heading_text)
            n = counts[base]
            counts[base] += 1
            anchors.add(base if n == 0 else f'{base}-{n}')
    return anchors


_MAX_REDIRECTS = 5


class _NoFollowRedirect(urllib.request.HTTPRedirectHandler):
    """Disable urllib's automatic redirect-following so each hop can be
    host-validated before we choose to follow it (SSRF defense)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        return None


def _addr_blocked(addr: ipaddress._BaseAddress) -> bool:
    """True if *addr* is not a public, routable destination.

    The contract is **allow only globally-routable addresses** -- the
    literal ``not addr.is_global``. A denylist of individual flags
    (loopback / private / link-local / reserved / multicast) is *not*
    equivalent: it misses ranges that are non-global yet carry none of
    those flags, e.g. CGNAT shared space ``100.64.0.0/10`` -- a real SSRF
    target an allow-listed denylist would wave through (caught in
    review, finding 1). ``is_global`` covers IPv4 and IPv6 uniformly."""
    return not addr.is_global


def _host_is_public(host: str) -> bool:
    """True iff *host* resolves and **every** address it resolves to is a
    public destination. Unresolvable or any non-public address -> False
    (fail-closed). This is checked per hop, so a redirect to an internal
    address is refused even if the first hop was public."""
    if not host:
        return False
    try:
        infos = socket.getaddrinfo(host, None)
    except OSError:
        return False
    if not infos:
        return False
    for info in infos:
        ip = info[4][0]
        # Strip an IPv6 scope-id (e.g. fe80::1%eth0) before parsing.
        ip = ip.split('%', 1)[0]
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return False
        if _addr_blocked(addr):
            return False
    return True


def _host_allowed(host: str, allow_hosts: set[str] | None) -> bool:
    """A host passes if it is explicitly allow-listed (an adopter's known
    internal docs host) or resolves entirely to public addresses."""
    if allow_hosts and host in allow_hosts:
        return True
    return _host_is_public(host)


def _probe_external(md: Path, lineno: int, url: str, flags: list[Flag],
                    *, allow_hosts: set[str] | None = None) -> None:
    """HEAD-probe an external link, default-safe against SSRF.

    Contract: http(s) only; manual redirect handling with a hop cap; every
    hop's host validated (resolves entirely to public addresses, or is
    ``--allow-host``-listed) before it is contacted; no proxy / auth / netrc
    handlers and a minimal header set (no ambient credentials). Residual: a
    DNS-rebind TOCTOU remains between the resolution check and urllib's own
    connect; documented on the flag.
    """
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),   # no system/env proxy + no proxy auth
        _NoFollowRedirect(),               # manual, validated redirects only
    )
    current = url
    hops = 0
    while True:
        parts = urlsplit(current)
        if parts.scheme not in ('http', 'https'):
            flags.append(Flag(md, lineno, 'link',
                f'refused non-http(s) scheme in external probe: `{current}`'))
            return
        host = parts.hostname or ''
        if not _host_allowed(host, allow_hosts):
            flags.append(Flag(md, lineno, 'link',
                f'external link host refused by SSRF guard (non-public IP; '
                f'use --allow-host to permit a known internal host): `{current}`'))
            return
        req = urllib.request.Request(
            current, method='HEAD', headers={'User-Agent': 'link-check'})
        try:
            resp = opener.open(req, timeout=10)  # noqa: S310 (guarded, opt-in)
        except urllib.error.HTTPError as exc:
            if exc.code in (301, 302, 303, 307, 308):
                loc = exc.headers.get('Location')
                if not loc:
                    return  # redirect with no target; treat as resolved
                hops += 1
                if hops > _MAX_REDIRECTS:
                    flags.append(Flag(md, lineno, 'link',
                        f'external link exceeded {_MAX_REDIRECTS} redirects: '
                        f'`{url}`'))
                    return
                current = urljoin(current, loc)
                continue
            # A non-redirect HTTP status means the server answered -> the link
            # resolves; a 4xx/5xx is reported as a broken external link.
            flags.append(Flag(md, lineno, 'link',
                f'external link failed (HTTP {exc.code}): `{url}`'))
            return
        except Exception as exc:  # noqa: BLE001 -- report any failure
            flags.append(Flag(md, lineno, 'link',
                f'external link failed ({exc}): `{url}`'))
            return
        else:
            resp.close()
            return


def check_links(
    md: Path, root: Path, scannable: list[tuple[int, str]],
    anchors_by_file: dict[Path, set[str]], *, check_external: bool = False,
    allow_hosts: set[str] | None = None,
    link_allow: set[str] | None = None,
) -> tuple[list[Flag], int]:
    """Check one file's links / anchors against *scannable* lines.

    Returns ``(flags, n_external_links)``. *anchors_by_file* is a cache
    shared across a tree scan so each target file's headings are parsed
    once. This is the composable core: ``check_cairn.py`` calls it with
    its own scannable lines so Cairn runs the exact shipped tool.

    *link_allow* is the set of link target strings declared exempt by
    the file's ``<!-- link-check-allow: ... -->`` directive(s).  Only
    the ``broken link target`` check is suppressed for listed targets;
    anchor checks and containment checks are unaffected.
    """
    flags: list[Flag] = []
    n_external = 0
    root_resolved = root.resolve()
    _link_allow: set[str] = link_allow or set()
    targets: list[tuple[int, str]] = []
    for lineno, line in scannable:
        for m in _LINK_RE.finditer(line):
            targets.append((lineno, m.group(1)))
        rd = _REFDEF_RE.match(line)
        if rd:
            targets.append((lineno, rd.group(1)))

    for lineno, target in targets:
        target = target.strip()
        if target.startswith('#'):                  # same-file anchor
            path_part, anchor = '', target[1:]
        elif '#' in target and not target.startswith(('http', 'mailto')):
            path_part, anchor = target.split('#', 1)
        else:
            path_part, anchor = target, ''

        low = target.lower()
        if low.startswith(('http://', 'https://')):
            n_external += 1
            if check_external:
                _probe_external(md, lineno, target, flags,
                                allow_hosts=allow_hosts)
            continue
        if low.startswith('file://'):
            # Machine-specific absolute target (e.g. a reviewer's
            # `[text](file:///Users/.../x.py)` link). Not portably checkable --
            # it resolves only against the author's local filesystem and would
            # fail on CI -- so skip it, symmetric to the http(s) skip above.
            # *Relative* links in the same docs cite real repo paths and stay
            # checked; only the unportable absolute file:// scheme is skipped.
            continue
        if low.startswith(('mailto:', 'tel:')) or target.startswith('<'):
            continue

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
                if path_part in _link_allow:
                    continue  # consciously exempted via link-check-allow
                flags.append(Flag(md, lineno, 'link',
                                  f'broken link target: `{target}`'))
                continue
            # Containment: an "internal" link must stay under the repo
            # root. A relative target that resolves to a real file
            # *outside* the tree (e.g. `../outside.md`) would otherwise
            # pass and make a delivered tree look self-contained when it
            # is not.
            if tgt != root_resolved and root_resolved not in tgt.parents:
                flags.append(Flag(md, lineno, 'link',
                                  f'link target escapes the repo root: '
                                  f'`{target}`'))
                continue
            anchor_file = tgt if tgt.is_file() else None
        else:
            anchor_file = md  # pure same-file anchor

        if anchor and anchor_file is not None and anchor_file.suffix == '.md':
            if anchor_file not in anchors_by_file:
                anchors_by_file[anchor_file] = file_anchors(
                    anchor_file.read_text(encoding='utf-8', errors='replace'))
            if anchor not in anchors_by_file[anchor_file]:
                flags.append(Flag(md, lineno, 'anchor',
                                  f'unresolved heading anchor: `{target}`'))
    return flags, n_external


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
    # -z: NUL-separated, unquoted names.  Without it git prints a name with
    # non-ASCII characters quoted with octal escapes, which never resolves.
    out = subprocess.run(
        ['git', 'ls-files', '-z', '*.md'], cwd=str(root),
        capture_output=True, text=True, check=True,
    )
    listed = [root / name for name in out.stdout.split('\0') if name]
    present = [path for path in listed if path.is_file()]
    skipped = len(listed) - len(present)
    if skipped:
        print(f'skipped {skipped} tracked Markdown file(s) not present on '
              f'disk', file=sys.stderr)
    return present


#: Ephemeral source directories skipped by default (re-included with
#: ``--include-archives``).  ``dev/**/archive/`` is handled by the
#: path-segment rule in ``filter_sources`` directly, not this tuple.
EPHEMERAL_SOURCE_DIRS = (Path('dev') / 'reflections',)


def filter_sources(files: list[Path], root: Path, *,
                   include_archives: bool = False,
                   include_modules: bool = False,
                   include_cairn: bool = False) -> list[Path]:
    """Drop not-adopter-authored SOURCES from the whole-tree scan set.

    Four classes of source are skipped by default (each independently
    re-includable), because their links are *not* adopter-authored content the
    gate should hold green:

    * ``dev/**/archive/`` -- historical records; links rot by design
      (``--include-archives``).
    * ``dev/modules/`` -- **vendored** Cairn module docs whose internal links
      target the *Cairn-install layout* (``doctrine/…``, the module's own
      tooling), so they always false-positive in an adopter tree
      (``--include-modules``).
    * ``dev/.cairn/`` -- **tool-owned** machinery, including the ``base/``
      upgrade-ancestor cache of tracked templates (``--include-cairn``).
    * ``dev/reflections/`` -- ephemeral, gitignored, pruned.

    The exclusion filters *sources* only: a live doc linking *to* an archived /
    module / ``.cairn`` file is still validated by ``check_links``.

    Each rule is **root-anchored**: ``dev/modules`` and ``dev/.cairn`` match the
    first two path segments (``rel.parent.parts[:2]``), so a user dir named
    ``modules`` nested elsewhere (e.g. ``<package>/modules/``) is never
    over-excluded; ``archive`` matches the segment at any depth under ``dev/``
    so nested archive subdirs are covered.

    ``--include-archives`` is the **completeness escape hatch** (scan absolutely
    everything, the pre-existing behavior); ``--include-modules`` /
    ``--include-cairn`` re-include just their own class.
    """
    if include_archives:
        return files

    def _excluded(source: Path) -> bool:
        try:
            rel = source.relative_to(root)
        except ValueError:
            return False
        parent_parts = rel.parent.parts
        if parent_parts and parent_parts[0] == 'dev' and 'archive' in parent_parts:
            return True
        if not include_modules and parent_parts[:2] == ('dev', 'modules'):
            return True
        if not include_cairn and parent_parts[:2] == ('dev', '.cairn'):
            return True
        rel_parent = rel.parent
        return any(
            rel_parent == d or d in rel_parent.parents
            for d in EPHEMERAL_SOURCE_DIRS
        )

    return [s for s in files if not _excluded(s)]


def check_tree(root: Path, files: list[Path],
               *, check_external: bool = False,
               allow_hosts: set[str] | None = None) -> Result:
    anchors_by_file: dict[Path, set[str]] = {}
    result = Result()
    for md in files:
        text = md.read_text(encoding='utf-8', errors='replace')
        result.files_scanned += 1
        link_allow = parse_link_allow_directives(text)
        flags, n_ext = check_links(
            md, root, scannable_lines(text), anchors_by_file,
            check_external=check_external, allow_hosts=allow_hosts,
            link_allow=link_allow)
        result.flags.extend(flags)
        result.external_links += n_ext
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='link_check',
        description='Markdown link / anchor integrity check over a repo.',
    )
    parser.add_argument('files', nargs='*', type=Path,
                        help='Specific Markdown files (default: whole tree).')
    parser.add_argument('--root', type=Path, default=None,
                        help='Repo root (default: git toplevel).')
    parser.add_argument('--check-external', action='store_true',
                        help='Also probe http(s) links (network; off by '
                             'default). The probe is SSRF-guarded: http(s) '
                             'only, redirects validated per hop, and hosts '
                             'resolving to non-public IPs are refused. A '
                             'DNS-rebind race remains as a documented '
                             'residual.')
    parser.add_argument('--allow-host', action='append', dest='allow_hosts',
                        metavar='HOST', default=None,
                        help='Permit a specific internal hostname under '
                             '--check-external (repeatable). Reviewable '
                             'opt-out for a known internal docs host; there '
                             'is no blanket private-space allowance.')
    parser.add_argument('--include-archives', action='store_true',
                        help='Also scan sources under dev/**/archive/ '
                             '(historical records) and dev/reflections/ '
                             '(ephemeral, gitignored). Off by default: '
                             'archived links rot by design. Ignored when '
                             'explicit files are named.')
    parser.add_argument('--include-modules', action='store_true',
                        help='Also scan vendored module docs under dev/modules/ '
                             '(whose links target the Cairn-install layout). '
                             'Off by default. Ignored when explicit files are named.')
    parser.add_argument('--include-cairn', action='store_true',
                        help='Also scan tool-owned dev/.cairn/ (machinery + the '
                             'base/ upgrade-ancestor template cache). Off by '
                             'default. Ignored when explicit files are named.')
    args = parser.parse_args(argv)

    root = args.root.resolve() if args.root else repo_root()
    if not root.is_dir():
        print(f'link_check: root is not a directory: {root}', file=sys.stderr)
        return 2
    if args.files:
        files = [f.resolve() for f in args.files]
    else:
        files = filter_sources(
            tracked_markdown(root), root,
            include_archives=args.include_archives,
            include_modules=args.include_modules,
            include_cairn=args.include_cairn,
        )
    if not files:
        print('link_check: no Markdown files found.', file=sys.stderr)
        return 2

    result = check_tree(root, files, check_external=args.check_external,
                        allow_hosts=set(args.allow_hosts or []))

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
        print(f'link_check: {len(result.flags)} issue(s) across '
              f'{result.files_scanned} file(s){ext}.', file=sys.stderr)
        return 1
    print(f'link_check: OK -- {result.files_scanned} Markdown file(s) '
          f'scanned; no issues{ext}.')
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
