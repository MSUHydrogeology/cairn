#!/usr/bin/env python3
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

Usage::

    python scripts/link_check.py                  # whole tracked tree
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
        out.append((i, line))
    return out


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


_MAX_REDIRECTS = 5


class _NoFollowRedirect(urllib.request.HTTPRedirectHandler):
    """Disable urllib's automatic redirect-following so each hop can be
    host-validated before we choose to follow it (SSRF defense)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        return None


def _addr_blocked(addr: ipaddress._BaseAddress) -> bool:
    """True if *addr* is not a public, routable destination -- the SSRF
    block set: loopback / private / link-local / reserved / multicast /
    unspecified, for both IPv4 and IPv6."""
    return (
        addr.is_loopback or addr.is_private or addr.is_link_local
        or addr.is_reserved or addr.is_multicast or addr.is_unspecified
    )


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
) -> tuple[list[Flag], int]:
    """Check one file's links / anchors against *scannable* lines.

    Returns ``(flags, n_external_links)``. *anchors_by_file* is a cache
    shared across a tree scan so each target file's headings are parsed
    once. This is the composable core: ``check_cairn.py`` calls it with
    its own scannable lines so Cairn runs the exact shipped tool.
    """
    flags: list[Flag] = []
    n_external = 0
    root_resolved = root.resolve()
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
    out = subprocess.run(
        ['git', 'ls-files', '*.md'], cwd=str(root),
        capture_output=True, text=True, check=True,
    )
    return [root / line for line in out.stdout.splitlines() if line.strip()]


def check_tree(root: Path, files: list[Path],
               *, check_external: bool = False,
               allow_hosts: set[str] | None = None) -> Result:
    anchors_by_file: dict[Path, set[str]] = {}
    result = Result()
    for md in files:
        text = md.read_text(encoding='utf-8', errors='replace')
        result.files_scanned += 1
        flags, n_ext = check_links(
            md, root, scannable_lines(text), anchors_by_file,
            check_external=check_external, allow_hosts=allow_hosts)
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
    args = parser.parse_args(argv)

    root = args.root.resolve() if args.root else repo_root()
    if not root.is_dir():
        print(f'link_check: root is not a directory: {root}', file=sys.stderr)
        return 2
    files = [f.resolve() for f in args.files] if args.files \
        else tracked_markdown(root)
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
