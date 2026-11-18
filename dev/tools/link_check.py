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
``2`` usage error, or the tracked-file list could not be read.

Vendor-neutral and standard-library only -- nothing to clone or port.
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import posixpath
import re
import socket
import stat
import struct
import sys
import types
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path, PureWindowsPath
from urllib.parse import urljoin, urlsplit
from typing import Any


_HERE = Path(__file__).resolve().parent
if (_HERE.name == "team-gated" and _HERE.parent.name == "modules"
        and _HERE.parent.parent.name == "templates"):
    _REPO_ROOT = _HERE.parents[2]
    _GIT_READ_REL = ("templates", "skills", "_lib", "git_read.py")
elif _HERE.name == "tools" and _HERE.parent.name == "dev":
    _REPO_ROOT = _HERE.parent.parent
    _GIT_READ_REL = ("dev", "tools", "git_read.py")
else:
    _REPO_ROOT = _HERE.parent
    _GIT_READ_REL = ("tools", "git_read.py")
_GIT_READ_SHA256 = "b67deb4e50eaee1e420d49af5ddac318aa110407bcd7c03d305091146cf15252"
_GIT_READ_MAX_BYTES = 256 * 1024


def _load_verified_git_read():
    """Execute only the fixed, caller-pinned helper buffer from this delivery."""
    path = os.path.abspath(os.path.join(_REPO_ROOT, *_GIT_READ_REL))
    chain = []
    current = os.path.splitdrive(path)[0] + os.sep
    for part in path[len(current):].split(os.sep):
        if not part:
            continue
        current = os.path.join(current, part)
        try:
            info = os.lstat(current)
        except OSError:
            raise RuntimeError("git-read-binding-failed") from None
        attrs = getattr(info, "st_file_attributes", 0)
        reparse = bool(attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))
        if stat.S_ISLNK(info.st_mode) or reparse:
            raise RuntimeError("git-read-binding-failed")
        if current != path and not stat.S_ISDIR(info.st_mode):
            raise RuntimeError("git-read-binding-failed")
        chain.append((current, info))
    try:
        before = chain[-1][1]
        if not stat.S_ISREG(before.st_mode) or before.st_size < 0 \
                or before.st_size > _GIT_READ_MAX_BYTES:
            raise RuntimeError("git-read-binding-failed")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        fd = os.open(path, flags)
        try:
            opened = os.fstat(fd)

            def key(row):
                return (
                    int(row.st_dev), int(row.st_ino), int(row.st_mode),
                    int(row.st_size), int(row.st_mtime_ns), int(row.st_ctime_ns),
                    int(getattr(row, "st_uid", 0) or 0),
                    int(getattr(row, "st_gid", 0) or 0),
                    int(getattr(row, "st_file_attributes", 0) or 0),
                    int(getattr(row, "st_reparse_tag", 0) or 0),
                )

            def opened_matches(path_info, descriptor_info):
                if (not stat.S_ISREG(path_info.st_mode)
                        or not stat.S_ISREG(descriptor_info.st_mode)):
                    return False
                opened_compare_key = list(key(descriptor_info))
                if os.name == "nt":
                    path_birth = getattr(path_info, "st_birthtime_ns", None)
                    descriptor_birth = getattr(
                        descriptor_info, "st_birthtime_ns", None)
                    if (type(path_birth) is not int
                            or type(descriptor_birth) is not int
                            or path_info.st_ctime_ns != path_birth
                            or path_birth != descriptor_birth):
                        return False
                    opened_compare_key[5] = descriptor_birth
                return tuple(opened_compare_key) == key(path_info)

            if not opened_matches(before, opened):
                raise RuntimeError("git-read-binding-failed")
            chunks = []
            remaining = _GIT_READ_MAX_BYTES + 1
            while remaining:
                part = os.read(fd, min(65536, remaining))
                if not part:
                    break
                chunks.append(part)
                remaining -= len(part)
            source = b"".join(chunks)
            after = os.fstat(fd)
            current_chain = [(name, os.lstat(name)) for name, _old in chain]
            if (key(after) != key(opened)
                    or tuple((name, key(row)) for name, row in current_chain)
                    != tuple((name, key(row)) for name, row in chain)
                    or len(source) != opened.st_size
                    or len(source) > _GIT_READ_MAX_BYTES):
                raise RuntimeError("git-read-binding-failed")
        finally:
            os.close(fd)
    except (OSError, IndexError):
        raise RuntimeError("git-read-binding-failed") from None
    if hashlib.sha256(source).hexdigest() != _GIT_READ_SHA256:
        raise RuntimeError("git-read-binding-failed")
    module = types.ModuleType("_cairn_verified_git_read")
    module.__file__ = "<verified tools/git_read.py buffer>"
    module.__verified_source__ = source
    module.__verified_sha256__ = _GIT_READ_SHA256
    try:
        exec(compile(source, module.__file__, "exec", dont_inherit=True), module.__dict__)
        module.bind_verified_source(source, _GIT_READ_SHA256)
    except Exception:
        raise RuntimeError("git-read-binding-failed") from None
    return module


try:
    _GIT_READ = _load_verified_git_read()
except RuntimeError:
    if __name__ == '__main__' and '--release-boundary' in sys.argv:
        print('release-boundary: INCOMPLETE: Git helper binding failed')
        raise SystemExit(2) from None
    raise

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
# *prefix* of a longer closing run (e.g. an opener of 2 closed by a run
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

_SCANNER_CONFIG = Path('dev/.cairn/scanner-check-allow.json')


@dataclass(frozen=True)
class ScannerExemption:
    source: str
    target: str
    reason: str


@dataclass(frozen=True)
class ScannerReviewIdException:
    source: str
    id: str
    context: str
    reason: str


@dataclass(frozen=True)
class ScannerConfig:
    present: bool
    valid: bool
    links: tuple[ScannerExemption, ...] = ()
    internal_refs: tuple[ScannerExemption, ...] = ()
    diagnostic: str = ''
    review_ids: tuple[ScannerReviewIdException, ...] = ()


def _unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate key: {key}')
        result[key] = value
    return result


def _exact_source(value: object) -> bool:
    if not isinstance(value, str) or not value.endswith('.md'):
        return False
    parts = value.split('/')
    return (all(part not in ('', '.', '..') for part in parts)
            and not any(c in value for c in '*?[]\\\n\r\t'))


_REVIEW_ID_TOKEN = re.compile(
    r'(?:[RFN]\d{1,2}(?:\.r\d+)?|CR\d+(?:-\d+)*|SR(?:-(?:[A-Z])?\d+|\d+)(?:-\d+)*)'
)


def _exact_review_source(value: object) -> bool:
    if not isinstance(value, str) or not value.endswith(('.md', '.py')):
        return False
    parts = value.split('/')
    path_ok = (all(part not in ('', '.', '..') for part in parts)
               and not any(c in value for c in '*?[]\\\n\r\t'))
    return (path_ok and (value == 'CHANGELOG.md'
                         or value.startswith('docs/') and value.endswith('.md')
                         or value.startswith('templates/modules/')
                         and value.endswith(('.md', '.py'))))


def _exact_review_id(value: object) -> bool:
    return isinstance(value, str) and _REVIEW_ID_TOKEN.fullmatch(value) is not None


def _exact_target(value: object, *, internal: bool) -> bool:
    if not isinstance(value, str) or not value or value.endswith('/'):
        return False
    if (value.startswith('/') or '://' in value
            or any(c.isspace() or c in '*?[]\\#' for c in value)):
        return False
    parts = value.split('/')
    if any(part in ('', '.') for part in parts):
        return False
    if internal and ('..' in parts or not value.startswith(('docs/methodology/', 'doctrine/'))):
        return False
    return True


def load_scanner_config(root: Path) -> ScannerConfig:
    """Read exact, reasoned scanner exemptions; reject the entire invalid file.

    This reader does not apply exemptions. Consumers decide how to report
    absence, invalid input, stale entries, and compatibility with directives.
    """
    path = root / _SCANNER_CONFIG
    try:
        text = path.read_text(encoding='utf-8')
    except FileNotFoundError:
        if path.is_symlink():
            return ScannerConfig(True, False, diagnostic=f'{_SCANNER_CONFIG} is a dangling link')
        return ScannerConfig(False, True, diagnostic=f'{_SCANNER_CONFIG} is missing')
    except (OSError, UnicodeError) as exc:
        return ScannerConfig(True, False, diagnostic=f'{_SCANNER_CONFIG}: {exc}')
    try:
        data = json.loads(text, object_pairs_hook=_unique_json_object)
        if (not isinstance(data, dict)
                or set(data) not in ({'links', 'internal_refs'},
                                     {'links', 'internal_refs', 'review_ids'})):
            raise ValueError('expected links and internal_refs arrays, with optional review_ids')
        parsed = {}
        for name in ('links', 'internal_refs'):
            entries = data[name]
            if not isinstance(entries, list):
                raise ValueError(f'{name} must be an array')
            seen = set()
            values = []
            for entry in entries:
                if not isinstance(entry, dict) or set(entry) != {'source', 'target', 'reason'}:
                    raise ValueError(f'{name} entries need source, target and reason')
                source, target, reason = entry['source'], entry['target'], entry['reason']
                if (not _exact_source(source)
                        or not _exact_target(target, internal=name == 'internal_refs')
                        or not isinstance(reason, str) or not reason.strip()):
                    raise ValueError(f'{name} entry has invalid scope or reason')
                key = (source, target)
                if key in seen:
                    raise ValueError(f'{name} has a duplicate source and target')
                seen.add(key)
                values.append(ScannerExemption(source, target, reason))
            parsed[name] = tuple(values)
        review_ids = []
        seen_review_ids = set()
        review_id_entries = data.get('review_ids', [])
        if not isinstance(review_id_entries, list):
            raise ValueError('review_ids must be an array')
        for entry in review_id_entries:
            if (not isinstance(entry, dict)
                    or set(entry) != {'source', 'id', 'context', 'reason'}):
                raise ValueError('review_ids entries need source, id, context and reason')
            source, identifier = entry['source'], entry['id']
            context, reason = entry['context'], entry['reason']
            if (not _exact_review_source(source)
                    or not _exact_review_id(identifier)
                    or not isinstance(context, str) or not context
                    or '\n' in context or '\r' in context
                    or context.count(identifier) != 1
                    or not isinstance(reason, str) or not reason.strip()):
                raise ValueError('review_ids entry has invalid scope, context or reason')
            key = (source, identifier, context)
            if key in seen_review_ids:
                raise ValueError('review_ids has a duplicate source, id and context')
            seen_review_ids.add(key)
            review_ids.append(ScannerReviewIdException(
                source, identifier, context, reason))
        return ScannerConfig(True, True, parsed['links'], parsed['internal_refs'],
                             review_ids=tuple(review_ids))
    except (ValueError, TypeError, RecursionError) as exc:
        return ScannerConfig(True, False, diagnostic=f'{_SCANNER_CONFIG}: {exc}')


def scanner_targets(config: ScannerConfig, md: Path, root: Path,
                    *, internal: bool = False) -> set[str]:
    """Return exact configured targets for one source, never for invalid input."""
    if not config.valid:
        return set()
    try:
        source = md.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return set()
    entries = config.internal_refs if internal else config.links
    return {entry.target for entry in entries if entry.source == source}


def scanner_link_allow(config: ScannerConfig, md: Path, root: Path,
                       text: str) -> set[str]:
    """Combine legacy and exact configured targets only for valid input."""
    if not config.valid:
        return set()
    return (parse_link_allow_directives(text)
            | scanner_targets(config, md, root))


def scanner_source(md: Path, root: Path) -> str | None:
    try:
        return md.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def report_scanner_entries(config: ScannerConfig, root: Path, kind: str,
                           checked: dict[str, set[str]], tool: str) -> None:
    """Report missing sources and unused entries only for scanned sources."""
    if not config.valid:
        return
    entries = config.links if kind == 'links' else config.internal_refs
    for entry in entries:
        if not (root / entry.source).is_file():
            status = 'stale source'
        elif entry.source in checked and entry.target not in checked[entry.source]:
            status = 'unused'
        else:
            continue
        print(f'{tool}: {_SCANNER_CONFIG}: {status} {kind} entry '
              f'{entry.source} -> {entry.target}', file=sys.stderr)


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
    used_link_allow: set[str] | None = None,
) -> tuple[list[Flag], int]:
    """Check one file's links / anchors against *scannable* lines.

    Returns ``(flags, n_external_links)``. *anchors_by_file* is a cache
    shared across a tree scan so each target file's headings are parsed
    once. This is the composable core: ``check_cairn.py`` calls it with
    its own scannable lines so Cairn runs the exact shipped tool.

    *link_allow* is the set of link target strings declared exempt for
    the source by directives or validated configuration. Only
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
            # The text that ``root /`` or ``md.parent /`` joins below. A
            # Windows network or drive path is refused by its text, on every
            # operating system, before anything touches the disk. A target
            # listed in link-check-allow is refused too.
            operand = path_part.lstrip('/')
            if PureWindowsPath(operand).drive:
                flags.append(Flag(md, lineno, 'link',
                                  'link target is a network or drive path '
                                  'and is not checked'))
                continue
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
                    if used_link_allow is not None:
                        used_link_allow.add(path_part)
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
        result = _GIT_READ.run_git(
            str(_HERE), ("rev-parse", "--show-toplevel"))
        if result.state == "completed" and result.returncode == 0:
            value = os.fsdecode(result.stdout).strip()
            if value:
                return Path(value)
    except (RuntimeError, OSError):
        pass
    try:
        return Path.cwd()
    except OSError:
        return Path.cwd()


def _tracked_index_paths(root: Path) -> list[str]:
    result = _GIT_READ.run_git(
        str(root), ("ls-files", "-z", "--cached", "--stage"))
    if result.state != "completed" or result.returncode != 0:
        raise RuntimeError("tracked Markdown discovery failed")
    if result.stdout and not result.stdout.endswith(b"\0"):
        raise RuntimeError("tracked Markdown discovery was incomplete")
    paths = set()
    for record in result.stdout.split(b"\0")[:-1]:
        metadata, separator, path = record.partition(b"\t")
        fields = metadata.split()
        if (not separator or len(fields) != 3
                or len(fields[0]) != 6
                or any(byte not in b"01234567" for byte in fields[0])
                or len(fields[1]) not in (40, 64)
                or any(byte not in b"0123456789abcdefABCDEF" for byte in fields[1])
                or fields[2] not in (b"0", b"1", b"2", b"3") or not path):
            raise RuntimeError("tracked Markdown discovery was malformed")
        paths.add(os.fsdecode(path))
    return sorted(paths)


def tracked_markdown(root: Path) -> list[Path]:
    """Tracked ``*.md`` paths that exist on disk.

    ``git ls-files`` still lists a file whose deletion is not yet committed
    (and a tracked symlink whose target is gone); reading either raises, so
    both are dropped and counted.  The note on stderr names no tool on
    purpose: ``check_cairn`` calls this same function, so a tool-name prefix
    here would sometimes name the wrong tool."""
    # -z: NUL-separated, unquoted names.  Without it git prints a name with
    # non-ASCII characters quoted with octal escapes, which never resolves.
    listed = [root / name for name in _tracked_index_paths(root)
              if name.endswith(".md")]
    present = [path for path in listed if path.is_file()]
    skipped = len(listed) - len(present)
    if skipped:
        print(f'skipped {skipped} tracked Markdown file(s) not present on '
              f'disk', file=sys.stderr)
    return sorted(present, key=lambda path: path.as_posix())


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
      target the *Cairn-install layout* (``docs/methodology/…``, the module's own
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
    config = load_scanner_config(root)
    if config.present and config.diagnostic:
        print(f'link_check: {config.diagnostic}', file=sys.stderr)
    checked: dict[str, set[str]] = {}
    for md in files:
        text = md.read_text(encoding='utf-8', errors='replace')
        result.files_scanned += 1
        link_allow = scanner_link_allow(config, md, root, text)
        used: set[str] = set()
        flags, n_ext = check_links(
            md, root, scannable_lines(text), anchors_by_file,
            check_external=check_external, allow_hosts=allow_hosts,
            link_allow=link_allow, used_link_allow=used)
        source = scanner_source(md, root)
        if source is not None:
            checked.setdefault(source, set()).update(used)
        result.flags.extend(flags)
        result.external_links += n_ext
    report_scanner_entries(config, root, 'links', checked, 'link_check')
    return result


_BOUNDARY_MAX_READ = (1 << 63) - 1


class _WindowsUnavailable(ValueError):
    pass


class _WindowsLimit(ValueError):
    pass


class _WindowsAPI:
    """Lazily bind the small, fixed set of Windows system APIs we need."""

    def __init__(self) -> None:
        import ctypes as C
        from ctypes import wintypes as W

        if C.sizeof(C.c_void_p) != 8:
            raise _WindowsUnavailable("unsupported-pointer-layout")
        try:
            nt = C.WinDLL("ntdll.dll", winmode=0x800, use_last_error=True)
            kernel = C.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
        except (AttributeError, OSError):
            raise _WindowsUnavailable("system-api-unavailable") from None

        HANDLE = C.c_void_p
        ULONG_PTR = C.c_size_t
        NTSTATUS = C.c_int32

        class UNICODE_STRING(C.Structure):
            _fields_ = [("Length", W.USHORT), ("MaximumLength", W.USHORT),
                        ("Buffer", C.c_void_p)]

        class OBJECT_ATTRIBUTES(C.Structure):
            _fields_ = [("Length", W.ULONG), ("RootDirectory", HANDLE),
                        ("ObjectName", C.POINTER(UNICODE_STRING)),
                        ("Attributes", W.ULONG), ("SecurityDescriptor", C.c_void_p),
                        ("SecurityQualityOfService", C.c_void_p)]

        class IO_STATUS_UNION(C.Union):
            _fields_ = [("Status", NTSTATUS), ("Pointer", C.c_void_p)]

        class IO_STATUS_BLOCK(C.Structure):
            _fields_ = [("u", IO_STATUS_UNION), ("Information", ULONG_PTR)]

        class BY_HANDLE_INFO(C.Structure):
            _fields_ = [("attributes", W.DWORD), ("created", W.FILETIME),
                        ("accessed", W.FILETIME), ("written", W.FILETIME),
                        ("volume", W.DWORD), ("size_high", W.DWORD),
                        ("size_low", W.DWORD), ("links", W.DWORD),
                        ("id_high", W.DWORD), ("id_low", W.DWORD)]

        class BASIC_LIMIT(C.Structure):
            _fields_ = [("process_time", C.c_int64), ("job_time", C.c_int64),
                        ("flags", W.DWORD), ("minimum", C.c_size_t),
                        ("maximum", C.c_size_t), ("processes", W.DWORD),
                        ("affinity", C.c_size_t), ("priority", W.DWORD),
                        ("scheduling", W.DWORD)]

        class IO_COUNTERS(C.Structure):
            _fields_ = [(name, C.c_uint64) for name in
                        ("read_ops", "write_ops", "other_ops", "read_bytes",
                         "write_bytes", "other_bytes")]

        class EXTENDED_LIMIT(C.Structure):
            _fields_ = [("basic", BASIC_LIMIT), ("io", IO_COUNTERS),
                        ("process_memory", C.c_size_t), ("job_memory", C.c_size_t),
                        ("peak_process_memory", C.c_size_t),
                        ("peak_job_memory", C.c_size_t)]

        sizes = (C.sizeof(UNICODE_STRING), C.sizeof(OBJECT_ATTRIBUTES),
                 C.sizeof(IO_STATUS_BLOCK), C.sizeof(BY_HANDLE_INFO),
                 struct.calcsize("<II6qIIIbx24s2xq"), C.sizeof(BASIC_LIMIT),
                 C.sizeof(EXTENDED_LIMIT))
        if sizes != (16, 48, 16, 52, 104, 64, 144):
            raise _WindowsUnavailable("unsupported-windows-abi-layout")

        try:
            nt.NtCreateFile.argtypes = [C.POINTER(HANDLE), W.ULONG,
                C.POINTER(OBJECT_ATTRIBUTES), C.POINTER(IO_STATUS_BLOCK), C.c_void_p,
                W.ULONG, W.ULONG, W.ULONG, W.ULONG, C.c_void_p, W.ULONG]
            nt.NtCreateFile.restype = NTSTATUS
            kernel.QueryDosDeviceW.argtypes = [W.LPCWSTR, W.LPWSTR, W.DWORD]
            kernel.QueryDosDeviceW.restype = W.DWORD
            kernel.GetFileType.argtypes = [HANDLE]
            kernel.GetFileType.restype = W.DWORD
            kernel.GetFileInformationByHandle.argtypes = [HANDLE, C.POINTER(BY_HANDLE_INFO)]
            kernel.GetFileInformationByHandle.restype = W.BOOL
            kernel.GetFileInformationByHandleEx.argtypes = [HANDLE, C.c_int, C.c_void_p, W.DWORD]
            kernel.GetFileInformationByHandleEx.restype = W.BOOL
            kernel.GetVolumeInformationByHandleW.argtypes = [HANDLE, W.LPWSTR, W.DWORD,
                C.POINTER(W.DWORD), C.POINTER(W.DWORD), C.POINTER(W.DWORD), W.LPWSTR, W.DWORD]
            kernel.GetVolumeInformationByHandleW.restype = W.BOOL
            kernel.ReadFile.argtypes = [HANDLE, C.c_void_p, W.DWORD,
                C.POINTER(W.DWORD), C.c_void_p]
            kernel.ReadFile.restype = W.BOOL
            kernel.CloseHandle.argtypes = [HANDLE]
            kernel.CloseHandle.restype = W.BOOL
            kernel.CreateJobObjectW.argtypes = [C.c_void_p, W.LPCWSTR]
            kernel.CreateJobObjectW.restype = HANDLE
            kernel.SetInformationJobObject.argtypes = [HANDLE, C.c_int, C.c_void_p, W.DWORD]
            kernel.SetInformationJobObject.restype = W.BOOL
            kernel.GetCurrentProcess.argtypes = []
            kernel.GetCurrentProcess.restype = HANDLE
            kernel.AssignProcessToJobObject.argtypes = [HANDLE, HANDLE]
            kernel.AssignProcessToJobObject.restype = W.BOOL
        except (AttributeError, OSError):
            raise _WindowsUnavailable("system-api-unavailable") from None

        self.C = C
        self.W = W
        self.nt = nt
        self.kernel = kernel
        self.HANDLE = HANDLE
        self.UNICODE_STRING = UNICODE_STRING
        self.OBJECT_ATTRIBUTES = OBJECT_ATTRIBUTES
        self.IO_STATUS_BLOCK = IO_STATUS_BLOCK
        self.BY_HANDLE_INFO = BY_HANDLE_INFO
        self.EXTENDED_LIMIT = EXTENDED_LIMIT

    def close(self, handle: int | None) -> None:
        if handle:
            self.kernel.CloseHandle(self.HANDLE(handle))

    def open(self, name: str, parent: int | None = None, *, file_read: bool = False) -> int:
        C, W = self.C, self.W
        if parent is not None and (not name or name in {".", ".."}
                                   or any(char in name for char in "\\/:\x00")
                                   or len(name.encode("utf-16-le")) > 510):
            raise _WindowsUnavailable("not-one-component")
        text = C.create_unicode_buffer(name)
        byte_length = len(name.encode("utf-16-le"))
        unicode_name = self.UNICODE_STRING(byte_length, byte_length + 2,
                                            C.cast(text, C.c_void_p))
        attributes = self.OBJECT_ATTRIBUTES(
            C.sizeof(self.OBJECT_ATTRIBUTES), parent, C.pointer(unicode_name), 0, None, None)
        io_status = self.IO_STATUS_BLOCK()
        handle = self.HANDLE()
        status = self.nt.NtCreateFile(
            C.byref(handle), 1 | 0x80 | 0x100000, C.byref(attributes),
            C.byref(io_status), None, 0, 1 if file_read else 3, 1,
            0x00200000 | 0x20, None, 0)
        if status != 0:
            self.close(handle.value)
            raise _WindowsUnavailable(f"open-status-0x{status & 0xffffffff:08X}")
        return int(handle.value)

    def info(self, handle: int) -> dict[str, Any]:
        C, W = self.C, self.W
        value = self.BY_HANDLE_INFO()
        if (self.kernel.GetFileType(handle) != 1
                or not self.kernel.GetFileInformationByHandle(handle, C.byref(value))):
            raise _WindowsUnavailable("not-verifiable-disk-object")
        attributes = int(value.attributes)
        if attributes & (0x400 | 0x40):
            raise _WindowsUnavailable("reparse-or-device")
        return {
            "identity": (int(value.volume), (int(value.id_high) << 32) | int(value.id_low)),
            "size": (int(value.size_high) << 32) | int(value.size_low),
            "directory": bool(attributes & 0x10),
            "written": (int(value.written.dwHighDateTime) << 32)
                       | int(value.written.dwLowDateTime),
        }

    def admit_root(self, path: str) -> tuple[list[int], str]:
        import ntpath
        import re

        if not isinstance(path, str) or path.startswith("\\\\"):
            raise _WindowsUnavailable("unsupported-root-form")
        drive, tail = ntpath.splitdrive(path)
        if not re.fullmatch(r"[A-Za-z]:", drive) or not tail.startswith("\\"):
            raise _WindowsUnavailable("unsupported-root-form")
        parts = tail[1:].split("\\")
        if parts == [""]:
            parts = []
        for part in parts:
            if (not part or part in {".", ".."} or any(c in part for c in "/:\x00")
                    or len(part.encode("utf-16-le")) > 510):
                raise _WindowsUnavailable("unsupported-root-component")
        targets = self.C.create_unicode_buffer(32768)
        if not self.kernel.QueryDosDeviceW(drive, targets, len(targets)):
            raise _WindowsUnavailable("drive-map-unavailable")
        target = targets.value
        if not re.fullmatch(r"\\Device\\HarddiskVolume[0-9]+", target):
            raise _WindowsUnavailable("unsupported-drive-alias")
        handles: list[int] = []
        try:
            volume = self.open(target + "\\")
            handles.append(volume)
            if not self.info(volume)["directory"]:
                raise _WindowsUnavailable("volume-not-directory")
            fs_name = self.C.create_unicode_buffer(64)
            serial, name_limit, flags = self.W.DWORD(), self.W.DWORD(), self.W.DWORD()
            if not self.kernel.GetVolumeInformationByHandleW(
                    volume, None, 0, self.C.byref(serial), self.C.byref(name_limit),
                    self.C.byref(flags), fs_name, len(fs_name)):
                raise _WindowsUnavailable("volume-info-unavailable")
            if fs_name.value != "NTFS":
                raise _WindowsUnavailable("unsupported-volume")
            for part in parts:
                child = self.open_child(handles[-1], part)
                handles.append(child)
                if not self.info(child)["directory"]:
                    raise _WindowsUnavailable("root-component-not-directory")
            return handles, fs_name.value
        except BaseException:
            for handle in reversed(handles):
                self.close(handle)
            raise

    def open_child(self, parent: int, entry: dict[str, Any] | str,
                   *, file_read: bool = False) -> int:
        name = entry if isinstance(entry, str) else entry["name"]
        before = self.info(parent)
        if not before["directory"]:
            raise _WindowsUnavailable("parent-not-directory")
        handle = self.open(name, parent, file_read=file_read)
        try:
            child = self.info(handle)
            after = self.info(parent)
            if after["identity"] != before["identity"]:
                raise _WindowsUnavailable("parent-changed")
            if child["identity"][0] != before["identity"][0]:
                raise _WindowsUnavailable("volume-changed")
            if isinstance(entry, dict) and (
                    child["identity"][1] != entry["file_id"]
                    or child["directory"] != entry["directory"]
                    or child["size"] != entry["size"]):
                raise _WindowsUnavailable("enumerated-identity-or-type-changed")
            return handle
        except BaseException:
            self.close(handle)
            raise

    def read(self, handle: int, allowance: int, counted: list[int]) -> bytes:
        before = self.info(handle)
        if before["directory"]:
            raise _WindowsUnavailable("source-not-file")
        if before["size"] > _BOUNDARY_MAX_READ:
            raise _WindowsLimit("per-file source limit")
        if before["size"] > allowance:
            raise _WindowsLimit("total read budget would be exceeded")
        chunks: list[bytes] = []
        remaining = min(_BOUNDARY_MAX_READ + 1, allowance)
        while remaining:
            buffer = self.C.create_string_buffer(min(65536, remaining))
            count = self.W.DWORD()
            ok = self.kernel.ReadFile(handle, buffer, len(buffer), self.C.byref(count), None)
            counted[0] += int(count.value)
            if not ok:
                raise _WindowsUnavailable("read-failed")
            if count.value > len(buffer):
                raise _WindowsUnavailable("invalid-read-count")
            if not count.value:
                break
            chunks.append(buffer.raw[:count.value])
            remaining -= count.value
        after = self.info(handle)
        if after != before:
            raise _WindowsUnavailable("source-changed")
        data = b"".join(chunks)
        if len(data) != before["size"]:
            raise _WindowsUnavailable("source-size-changed")
        if len(data) > _BOUNDARY_MAX_READ:
            raise _WindowsLimit("per-file source limit")
        if len(data) > allowance:
            raise _WindowsLimit("total read budget would be exceeded")
        return data


def _boundary_read(root: Path, rel: str) -> str:
    """Read a contained file through bound, no-follow directory handles."""
    parts = rel.split('/')
    if not parts or any(p in ('', '.', '..') or '\\' in p or ':' in p or '\0' in p for p in parts):
        raise ValueError("unsafe path component")
    if os.name == 'nt':
        api = _WindowsAPI()
        handles, _ = api.admit_root(str(root))
        try:
            for part in parts:
                handle = api.open_child(handles[-1], part, file_read=True)
                handles.append(handle)
            data = api.read(handles[-1], _BOUNDARY_MAX_READ + 1, [0])
        finally:
            for handle in reversed(handles):
                api.close(handle)
    else:
        if os.open not in os.supports_dir_fd or not hasattr(os, 'O_NOFOLLOW') or not hasattr(os, 'O_DIRECTORY'):
            raise ValueError("safe directory binding unavailable")
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        handles = []
        try:
            handles.append(os.open('/', flags))
            for part in root.parts[1:]:
                handles.append(os.open(part, flags, dir_fd=handles[-1]))
            for part in parts[:-1]:
                handles.append(os.open(part, flags, dir_fd=handles[-1]))
            fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | getattr(os, 'O_NONBLOCK', 0), dir_fd=handles[-1])
            handles.append(fd)
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_size > _BOUNDARY_MAX_READ:
                raise ValueError("nonregular or oversized file")
            chunks = []
            remaining = _BOUNDARY_MAX_READ + 1
            while remaining:
                chunk = os.read(fd, min(65536, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            data = b''.join(chunks)
            after = os.fstat(fd)
            if (len(data) != info.st_size or (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns) != (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)):
                raise ValueError("file changed while reading")
        finally:
            for handle in reversed(handles):
                os.close(handle)
    if b'\0' in data:
        raise ValueError("non-text file")
    return data.decode('utf-8', 'strict')


def _boundary_index(root: Path) -> dict[str, list[tuple[bytes, bytes]]]:
    top = _GIT_READ.run_git(str(root), ('rev-parse', '--show-toplevel'))
    if top.state != 'completed' or top.returncode != 0 or Path(os.fsdecode(top.stdout.strip())).resolve() != root:
        raise ValueError("Git worktree root unavailable or different")
    result = _GIT_READ.run_git(str(root), ('ls-files', '-z', '--cached', '--stage'))
    if result.state != 'completed' or result.returncode != 0 or (result.stdout and not result.stdout.endswith(b'\0')):
        raise ValueError("Git index unavailable or incomplete")
    entries = {}
    for row in result.stdout.split(b'\0')[:-1]:
        meta, sep, name = row.partition(b'\t')
        fields = meta.split()
        if (not sep or len(fields) != 3 or len(fields[0]) != 6
                or any(c not in b'01234567' for c in fields[0])
                or len(fields[1]) not in (40, 64)
                or any(c not in b'0123456789abcdefABCDEF' for c in fields[1])
                or fields[2] not in (b'0', b'1', b'2', b'3') or not name):
            raise ValueError("malformed Git index")
        path = os.fsdecode(name)
        entries.setdefault(path, []).append((fields[0], fields[2]))
    return entries


def _boundary_selector(value: object) -> str:
    if not isinstance(value, str) or not value or '\\' in value or any(c in value for c in '*?['):
        raise ValueError("invalid selector")
    parts = value.rstrip('/').split('/')
    if value.startswith('/') or any(p in ('', '.', '..') for p in parts) or ':' in parts[0]:
        raise ValueError("unsafe selector")
    return value


def release_boundary(root: Path, scope_path: Path) -> int:
    """Report literal release references and tracked folder hygiene, offline."""
    from urllib.parse import unquote
    findings, incomplete, exempt = [], [], 0
    try:
        rel = scope_path if not scope_path.is_absolute() else scope_path.relative_to(root)
        scope = json.loads(_boundary_read(root, rel.as_posix()))
        if not isinstance(scope, dict) or set(scope) != {'kept', 'development'}:
            raise ValueError('scope must contain exactly kept and development')
        selectors = {}
        for key in ('kept', 'development'):
            if not isinstance(scope[key], list):
                raise ValueError('scope classes must be arrays')
            selectors[key] = [_boundary_selector(x) for x in scope[key]]
        index = _boundary_index(root)
    except (OSError, ValueError, UnicodeError, json.JSONDecodeError) as exc:
        print(f'release-boundary: INCOMPLETE: {exc}')
        return 2
    paths = sorted(index)
    def matches(path, selector):
        return path.startswith(selector) if selector.endswith('/') else path == selector
    for group, choices in selectors.items():
        for selector in choices:
            if not any(matches(path, selector) for path in paths):
                incomplete.append(f'unmatched {group} selector: {selector}')
    kept = []
    for path in paths:
        if path.startswith('dev/'):
            if any(matches(path, x) for x in selectors['kept']):
                incomplete.append(f'overlapping classification: {path}')
            continue
        classes = [key for key in selectors if any(matches(path, x) for x in selectors[key])]
        if len(classes) != 1:
            incomplete.append(f'unclassified or overlapping: {path}')
        elif classes[0] == 'kept':
            kept.append(path)
    if 'AGENTS.md' not in kept:
        incomplete.append('AGENTS.md must be tracked and kept')
    directories = set()
    for path in paths:
        if path.startswith('dev/'):
            bits = path.split('/')[:-1]
            directories.update('/'.join(bits[:i]) for i in range(1, len(bits) + 1))
        if path.startswith('dev/scratch/') and path not in ('dev/scratch/README.md', 'dev/scratch/.gitignore'):
            findings.append(f'tracked scratch: {path}')
    def regular(path):
        return index.get(path) in ([(b'100644', b'0')], [(b'100755', b'0')])
    for directory in sorted(directories):
        if not regular(directory + '/README.md'):
            findings.append(f'missing folder README: {directory}')
    table = None
    if regular('dev/README.md'):
        try:
            text = _boundary_read(root, 'dev/README.md')
            section = re.search(r'(?ms)^## The tree\s*\n(.*?)(?=^## |\Z)', text)
            if section is None:
                raise ValueError('missing tree section')
            table = set(re.findall(r'(?m)^\|\s*`([^`/]+/)`\s*\|', section.group(1)))
        except (OSError, ValueError, UnicodeError) as exc:
            incomplete.append(f'dev/README.md: {exc}')
    else:
        incomplete.append('dev/README.md lacks a regular stage-zero index entry')
    if table is not None:
        for directory in sorted(d for d in directories if d.count('/') == 1):
            if directory.split('/')[1] + '/' not in table:
                findings.append(f'unlisted top folder: {directory}')
    literal = re.compile(r'(?<![\w/])dev[\\/][\w.\-/\\]*')
    for path in kept:
        if not regular(path):
            incomplete.append(f'nonregular kept index entry: {path}')
            continue
        try:
            text = _boundary_read(root, path)
        except (OSError, ValueError, UnicodeError) as exc:
            incomplete.append(f'{path}: {exc}')
            continue
        for number, line in enumerate(text.splitlines(), 1):
            targets = [m.group(1) for m in _LINK_RE.finditer(line)]
            ref = _REFDEF_RE.match(line)
            if ref:
                targets.append(ref.group(1))
            hit = bool(literal.search(line))
            for target in targets:
                try:
                    parsed = urlsplit(target)
                except ValueError:
                    incomplete.append(f'malformed link: {path}:{number}')
                    continue
                if parsed.scheme or parsed.netloc:
                    continue
                pathpart = unquote(parsed.path).replace('\\', '/')
                if pathpart.startswith('/'):
                    resolved = posixpath.normpath(pathpart.lstrip('/'))
                else:
                    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), pathpart))
                if resolved == 'dev' or resolved.startswith('dev/'):
                    hit = True
            if hit:
                if path == 'AGENTS.md':
                    exempt += 1
                else:
                    findings.append(f'dev reference: {path}:{number}')
    for item in sorted(findings):
        print(f'  FINDING {item}')
    for item in sorted(incomplete):
        print(f'  INCOMPLETE {item}')
    status = 'INCOMPLETE' if incomplete else ('WITH FINDINGS' if findings else 'CLEAN')
    print(f'release-boundary: {status}; {len(findings)} finding(s), {len(incomplete)} incomplete, {exempt} AGENTS.md pointer(s) exempt')
    return 2 if incomplete else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='link_check',
        description='Markdown link / anchor integrity check over a repo.',
    )
    parser.add_argument('--release-boundary', type=Path, default=None, metavar='SCOPE')
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
    if args.release_boundary is not None:
        if args.files or args.check_external or args.allow_hosts or args.include_archives or args.include_modules or args.include_cairn:
            print('link_check: release-boundary cannot combine with scanner options', file=sys.stderr)
            return 2
        return release_boundary(root, args.release_boundary)
    if args.files:
        files = [f.resolve() for f in args.files]
    else:
        try:
            tracked = tracked_markdown(root)
        except RuntimeError as exc:
            print(f'link_check: {exc}', file=sys.stderr)
            return 2
        files = filter_sources(
            tracked, root,
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
