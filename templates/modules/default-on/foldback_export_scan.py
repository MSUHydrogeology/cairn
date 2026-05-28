#!/usr/bin/env python3
"""Export-scrub scanner for the fold-back active-surfacing protocol.

Stdlib-only.  Scans a drafted issue / PR body for **five mechanical
no-export classes** and exits non-zero on any finding (fail-closed).
The active-surfacing protocol (`cairn/doctrine/fold-back.md` >
"Active surfacing") invokes this as the Scrub step of the maintainer-
walkthrough; the scanner is the machine half of the two-gate export
boundary (the manual half is the maintainer-signed affirmation field
in the Cairn issue / PR template).

This scanner is **NOT** the prompt-injection / suspicious-content
tripwire that `content_scan.py` (the team-gated module) provides --
those gate different surfaces.  ``content_scan`` is a layer-2
agent-supply-chain integrity gate (egress / Unicode / homoglyph /
imperative-injection detection); ``foldback_export_scan`` is the
deployment-side export gate (credentials / paths / IPs / hostnames /
proprietary-token leak detection).  The two are complementary; an
active-surfacing flow may invoke both, but this scanner is the one
the protocol's bright-line gate-fail rule binds to.

The five mechanical detector classes:

* **credentials** -- assignment-pattern detectable secrets (e.g.
  ``password = "..."``, ``api_key = "..."``, ``secret = "..."``,
  ``token = "..."``, ``auth_*`` patterns).  Regex over the line.
* **private-path** -- user-scoped absolute paths (e.g. ``/Users/<name>/``,
  ``/home/<name>/``, ``C:\\Users\\<name>\\``, ``/private/``,
  ``/var/folders/``).
* **ip-address** -- IPv4 + IPv6 literals, with an **RFC 5737
  documentation-IP allowlist** (``192.0.2.0/24``, ``198.51.100.0/24``,
  ``203.0.113.0/24``) so legitimate documentation examples don't
  trigger.  Both deployment-internal IPs (RFC 1918) AND remote-repo
  IPs qualify -- the bright-line covers any literal that would
  expose deployment or contributor coordinate.
* **internal-hostname** -- ``.local``, ``.internal``, ``.lan`` TLD
  suffixes.  RFC 1918 IPs are already covered by the ip-address
  detector (they would qualify as internal hostnames if expressed as
  names instead of numbers).
* **proprietary-token** -- adopter-configurable denylist file
  (default: ``dev/upstream/foldback_export_denylist.txt``;
  ``--allowlist <path>`` overrides).  One token per line; blank
  lines and ``#``-comments skipped.  Case-sensitive substring match
  -- the deployment maintainer enumerates the project codenames /
  client names / domain-specific terms that should not leak.
  Empty / missing denylist file = detector silent (the other four
  detectors still run); the gate does not require the file to
  function.

Two no-export classes stay **out of this scanner's scope** because
no regex can reliably distinguish them from generic prose:

* **unpublished data hints** -- "the client's marina sediment data"
  vs. generic "sediment data."
* **proprietary domain detail** -- descriptive prose about
  client / project specifics.

Both are covered by the **maintainer-signed manual-affirmation field**
in the Cairn issue / PR template, per `cairn/doctrine/fold-back.md` >
"The export boundary -- scrub before anything goes up".

Usage::

    python scripts/foldback_export_scan.py <draft-path>
    python scripts/foldback_export_scan.py <draft-path> --allowlist <path>

Exit codes: ``0`` clean; ``1`` at least one finding; ``2`` usage
error (file not found, allowlist unreadable).
"""
from __future__ import annotations

import argparse
import ipaddress
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Finding shape
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """One export-scrub finding."""

    line: int
    detector: str    # 'credentials' | 'private-path' | 'ip-address'
                     # | 'internal-hostname' | 'proprietary-token'
    snippet: str     # the matched substring (truncated to ~80 chars)
    message: str


# ---------------------------------------------------------------------------
# Detector regexes + helpers
# ---------------------------------------------------------------------------


#: Credential assignment-pattern.  Common shapes:
#:   password = "..." | api_key = "..." | secret = "..." | token = "..."
#:   AUTH_TOKEN=... | ACCESS_KEY=... | bearer "..."
#: Case-insensitive.
_CREDENTIAL_KEY_RE = re.compile(
    r"\b("
    r"password|passwd|pwd|"
    r"api[_-]?key|access[_-]?key|secret[_-]?key|secret|"
    r"auth[_-]?token|access[_-]?token|bearer[_-]?token|token|"
    r"client[_-]?secret|private[_-]?key"
    r")\b\s*[:=]\s*[\"']?[^\s\"']{6,}",
    re.IGNORECASE,
)


#: Private filesystem paths.  Matches user-scoped absolute paths that
#: would identify the deployment maintainer or expose host structure.
_PRIVATE_PATH_PATTERNS = [
    # POSIX user-home: /Users/<name>/  /home/<name>/  /root/
    re.compile(r"/Users/[A-Za-z0-9_.-]+/"),
    re.compile(r"/home/[A-Za-z0-9_.-]+/"),
    re.compile(r"\broot/"),  # /root/ but also relative paths fine; tighten
    # POSIX system / sandbox paths
    re.compile(r"/private/"),
    re.compile(r"/var/folders/"),
    # /tmp/<specific-thing> -- bandit B108 false positive: this is a
    # detector REGEX that *matches* /tmp/... strings in a scanned draft,
    # not code that *uses* /tmp/ as its own tempfile path.  The whole
    # point of the detector is to catch leaked tempfile paths in drafts.
    re.compile(r"/tmp/[A-Za-z0-9_.-]+"),  # nosec B108
    # Windows user-home: C:\Users\<name>\  D:\Users\<name>\
    re.compile(r"[A-Z]:\\Users\\[A-Za-z0-9_.-]+\\"),
]


#: IP address regexes (literal numeric forms only -- internal-hostname
#: detector handles named forms).
_IPV4_RE = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\b"
)
#: IPv6 -- conservative regex that catches the common forms (full,
#: compressed-with-``::``, dual-with-IPv4-tail).  Not exhaustive but
#: covers the cases an export-scrub realistically sees.
_IPV6_RE = re.compile(
    r"\b(?:"
    r"(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}"  # full
    r"|"
    r"(?:[0-9a-fA-F]{1,4}:){1,7}:"               # ::-terminated
    r"|"
    r"(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}"
    r"|"
    r":(?::[0-9a-fA-F]{1,4}){1,7}"               # ::-prefixed
    r")\b"
)


#: RFC 5737 documentation-IP allowlist -- IPs explicitly reserved for
#: example use that should not trigger a leak finding even though they
#: are non-private.
_DOC_IP_NETWORKS = (
    ipaddress.IPv4Network("192.0.2.0/24"),
    ipaddress.IPv4Network("198.51.100.0/24"),
    ipaddress.IPv4Network("203.0.113.0/24"),
    # RFC 3849 IPv6 documentation block.
    ipaddress.IPv6Network("2001:db8::/32"),
)


#: Internal-hostname suffixes -- mDNS / corporate-network conventions.
_INTERNAL_HOSTNAME_RE = re.compile(
    r"\b[a-zA-Z0-9-]+\.(?:local|internal|lan|corp|home)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Per-line detectors
# ---------------------------------------------------------------------------


def _truncate(s: str, n: int = 80) -> str:
    return s if len(s) <= n else s[: n - 1] + "..."


def _detect_credentials(line: str, lineno: int) -> list[Finding]:
    out: list[Finding] = []
    for m in _CREDENTIAL_KEY_RE.finditer(line):
        out.append(Finding(
            line=lineno, detector="credentials",
            snippet=_truncate(m.group(0)),
            message=(
                f"credential-like assignment pattern detected: "
                f"`{_truncate(m.group(0))}` (key={m.group(1)!r}; "
                f"export-scrub: credentials must not ship to public Cairn)"
            ),
        ))
    return out


def _detect_private_paths(line: str, lineno: int) -> list[Finding]:
    out: list[Finding] = []
    for pat in _PRIVATE_PATH_PATTERNS:
        for m in pat.finditer(line):
            out.append(Finding(
                line=lineno, detector="private-path",
                snippet=_truncate(m.group(0)),
                message=(
                    f"private filesystem path detected: "
                    f"`{_truncate(m.group(0))}` "
                    f"(export-scrub: user-scoped paths leak deployment "
                    f"identity / host structure)"
                ),
            ))
    return out


def _ip_is_documentation(ip_str: str) -> bool:
    """True when *ip_str* falls in an RFC 5737 / RFC 3849
    documentation-IP allowlist range.  Documentation IPs are
    legitimate examples and must not trigger the leak finding.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    for net in _DOC_IP_NETWORKS:
        try:
            if ip in net:
                return True
        except TypeError:
            # IP / network family mismatch -- not in this net.
            continue
    return False


def _detect_ip_addresses(line: str, lineno: int) -> list[Finding]:
    out: list[Finding] = []
    for regex, family in ((_IPV4_RE, "IPv4"), (_IPV6_RE, "IPv6")):
        for m in regex.finditer(line):
            ip_str = m.group(0)
            if _ip_is_documentation(ip_str):
                continue  # RFC 5737 / 3849 doc-IP allowlist
            out.append(Finding(
                line=lineno, detector="ip-address",
                snippet=_truncate(ip_str),
                message=(
                    f"{family} address literal detected: `{ip_str}` "
                    f"(export-scrub: both deployment-internal AND "
                    f"remote-repo IPs are bright-line no-export; if this "
                    f"is a documentation example, use an RFC 5737 "
                    f"reserved range like 192.0.2.x / 198.51.100.x / "
                    f"203.0.113.x)"
                ),
            ))
    return out


def _detect_internal_hostnames(line: str, lineno: int) -> list[Finding]:
    out: list[Finding] = []
    for m in _INTERNAL_HOSTNAME_RE.finditer(line):
        out.append(Finding(
            line=lineno, detector="internal-hostname",
            snippet=_truncate(m.group(0)),
            message=(
                f"internal-hostname pattern detected: `{m.group(0)}` "
                f"(export-scrub: .local / .internal / .lan / .corp / "
                f".home are network-local conventions; not for public "
                f"export)"
            ),
        ))
    return out


def _detect_proprietary_tokens(
    line: str, lineno: int, denylist: list[str],
) -> list[Finding]:
    out: list[Finding] = []
    for token in denylist:
        if not token:
            continue
        # Case-sensitive substring match -- the adopter enumerates the
        # specific casing they care about.  Word-boundary regex to
        # avoid false positives on inner substrings.
        pattern = re.compile(rf"\b{re.escape(token)}\b")
        for m in pattern.finditer(line):
            out.append(Finding(
                line=lineno, detector="proprietary-token",
                snippet=_truncate(m.group(0)),
                message=(
                    f"adopter-configured proprietary token `{token}` "
                    f"detected (export-scrub: this token is in the "
                    f"deployment's foldback-export denylist)"
                ),
            ))
    return out


# ---------------------------------------------------------------------------
# Allowlist file
# ---------------------------------------------------------------------------


def load_denylist(path: Path) -> list[str]:
    """Read the adopter-configurable proprietary-token denylist.

    One token per line; blank lines and ``#``-comments are skipped.
    Returns an empty list if *path* does not exist (the detector goes
    silent; the other four detectors still run).
    """
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    out: list[str] = []
    for raw in text.split("\n"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out


# ---------------------------------------------------------------------------
# Whole-file scan + CLI
# ---------------------------------------------------------------------------


def scan_text(text: str, denylist: list[str]) -> list[Finding]:
    """Run all five detectors over *text* line-by-line.  Returns the
    concatenated findings ordered by (line, detector-class).
    """
    findings: list[Finding] = []
    for lineno, line in enumerate(text.split("\n"), start=1):
        findings.extend(_detect_credentials(line, lineno))
        findings.extend(_detect_private_paths(line, lineno))
        findings.extend(_detect_ip_addresses(line, lineno))
        findings.extend(_detect_internal_hostnames(line, lineno))
        findings.extend(_detect_proprietary_tokens(line, lineno, denylist))
    findings.sort(key=lambda f: (f.line, f.detector))
    return findings


def scan_file(path: Path, denylist: list[str]) -> list[Finding]:
    """Run :func:`scan_text` on *path*'s contents."""
    text = path.read_text(encoding="utf-8", errors="replace")
    return scan_text(text, denylist)


DEFAULT_DENYLIST_PATH = Path("dev/upstream/foldback_export_denylist.txt")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="foldback_export_scan",
        description=(
            "Export-scrub scanner for the fold-back active-surfacing "
            "protocol.  Five mechanical detector classes; non-zero exit "
            "on any finding (fail-closed)."
        ),
    )
    parser.add_argument(
        "file", type=Path,
        help="Markdown file (the drafted issue / PR body) to scan.",
    )
    parser.add_argument(
        "--allowlist", type=Path, default=DEFAULT_DENYLIST_PATH,
        metavar="PATH",
        help=(
            "Adopter-configurable proprietary-token denylist (one token "
            "per line; blank lines + #-comments skipped).  Default: "
            f"{DEFAULT_DENYLIST_PATH}.  Missing file = silent detector."
        ),
    )
    args = parser.parse_args(argv)

    if not args.file.is_file():
        print(
            f"foldback_export_scan: not a file: {args.file}",
            file=sys.stderr,
        )
        return 2

    denylist = load_denylist(args.allowlist)
    findings = scan_file(args.file, denylist)

    if not findings:
        print(f"foldback_export_scan: {args.file} -- OK; no findings.")
        return 0

    print(
        f"foldback_export_scan: {args.file} -- {len(findings)} finding(s):",
        file=sys.stderr,
    )
    for f in findings:
        print(
            f"  {args.file}:{f.line}: [{f.detector}] {f.message}",
            file=sys.stderr,
        )
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
