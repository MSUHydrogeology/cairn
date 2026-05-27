#!/usr/bin/env python3
"""Content-integrity scanner -- a supply-chain prompt-injection tripwire.

Cairn distributes **agent-loaded instruction files**: its templates and
doctrine become an adopter's ``AGENTS.md`` + ``dev/`` tree, auto-loaded
by AI agents as governing instructions.  An upstream compromise has an
LLM blast radius -- it reaches every adopter's agents at once.  This
scanner is **Layer 2/3** of the four-layer model in
``bootstrap/SAFETY.md`` (Rules 7-8) and ``bootstrap/PROVENANCE.md``.

**It is a witness, not the trust model.**  A static pattern set is
high-noise and incomplete *by design* -- semantic, adversarial injection
evades any fixed pattern set.  So the scanner **forces human review**
(the composing caller fails the check on a match); it never *proves* a
template safe.  It is a Cairn-internal dev tool, composed by
``scripts/check_cairn.py`` over Cairn's own source prose (Layer 2) and
run over scaffolded generated output (Layer 3); it is **not** shipped to
adopters (Rule 8 carries the adopter-side profile-trust obligation).

What it flags (each a ``pattern_id`` usable in a suppression marker):

* ``imperative-override`` -- "ignore previous", "disregard the
  maintainer/instructions/above", "do not tell", "regardless of what
  ... says".
* ``egress`` -- an exfiltration verb (send/email/upload/post/...) near a
  destination (a URL or an ``@`` address).
* ``suspicious-url`` -- a non-allowlisted external ``http(s)`` URL, in
  files scanned with ``scan_urls=True`` (executed templates).  The
  allowlist is configurable (``scripts/content_scan_allowlist.txt``, one
  domain per line) so a legitimate domain is added without editing code.
* ``unicode-zero-width`` -- zero-width characters (U+200B-200D, U+FEFF).
  A leading U+FEFF at file index 0 is a benign byte-order mark and is
  ignored there; it flags only *after* the first character.
* ``unicode-bidi`` -- bidirectional-control characters (U+202A-202E,
  U+2066-2069), the "innocent to a human, instruction to a parser"
  vector.
* ``homoglyph`` -- a single token that mixes scripts (e.g. Latin +
  Cyrillic/Greek).  Evaluated **per contiguous alphanumeric token**, not
  per line, so a Latin word beside a Cyrillic word does not false-flag.
* ``instruction-html-comment`` -- an HTML comment carrying an imperative
  verb.  Cairn's own ``<!-- cairn:slot ... -->`` / ``cairn:end`` and the
  ``cairn-accept`` markers are recognized and exempt; the rest flag.

Suppressions are **local and reasoned, never whole-directory
allowlists**.  An inline marker quotes a dangerous string with a reason:

    <!-- cairn-accept: <pattern-id> reason="..." reviewer="..." date=... -->

* **Line-scoped by default** -- it suppresses a ``<pattern-id>`` hit on
  its **own line or the immediately-preceding line** only.
* **Block-scope requires an explicit end** -- ``<!-- cairn-accept-end:
  <pattern-id> -->``; the suppression then spans the open line through
  the end line.  An **unclosed** open suppresses nothing beyond its
  line-scope (fail-safe -- a dangling open never silences the rest of
  the file).
* A marker **without a non-empty ``reason=``** is invalid and suppresses
  nothing (so the hit still fires).
* Attribute values may be single/double-quoted to contain spaces.

Usage::

    python scripts/content_scan.py <file> [<file> ...]
    python scripts/content_scan.py <file> --no-urls   # skip URL flagging
    python scripts/content_scan.py <file> --allowlist <path>

Exit codes: ``0`` clean; ``1`` at least one (unsuppressed) flag; ``2``
usage error.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

_DEFAULT_ALLOWLIST = Path(__file__).resolve().parent / "content_scan_allowlist.txt"


# --------------------------------------------------------------------------
# Flags

@dataclass(frozen=True)
class Flag:
    pattern_id: str
    line: int
    message: str


@dataclass
class ScanResult:
    flags: list[Flag] = field(default_factory=list)
    files_scanned: int = 0


# --------------------------------------------------------------------------
# Detector patterns

_IMPERATIVE_OVERRIDE_RES = [
    re.compile(r"ignore\s+(all\s+)?previous", re.I),
    re.compile(r"disregard\s+(the\s+)?(maintainer|instructions?|above|previous)", re.I),
    re.compile(r"\bdo\s+not\s+tell\b", re.I),
    re.compile(r"regardless\s+of\s+what\s+.{0,40}?\s+says", re.I),
    re.compile(r"ignore\s+the\s+above", re.I),
]

# An egress verb followed (within a short window) by a destination: a
# URL or an @-address.
_EGRESS_RE = re.compile(
    r"\b(send|email|e-mail|upload|post|exfiltrate|transmit|leak)\b"
    r".{0,40}?"
    r"(https?://\S+|[\w.+-]+@[\w.-]+\.\w+)",
    re.I,
)

_URL_RE = re.compile(r"https?://([^/\s)\"'>]+)", re.I)

# Zero-width + bidi control characters.  Members are literal control
# chars (with a naming comment each), as **escape forms** (\uXXXX), never raw characters, so this scanner
# carries none of the invisible code points it detects (trojansource-safe,
# bandit B613); the per-char comment names each.  Coverage expanded per
# code-review P3 (word joiner U+2060; LRM U+200E / RLM U+200F).
_ZERO_WIDTH = {
    "\u200b",  # zero-width space
    "\u200c",  # zero-width non-joiner
    "\u200d",  # zero-width joiner
    "\u2060",  # word joiner
    "\ufeff",  # zero-width no-break space / BOM
}
_BIDI = (
    {chr(c) for c in range(0x202A, 0x202F)}    # U+202A-202E embeddings/overrides
    | {chr(c) for c in range(0x2066, 0x206A)}  # U+2066-2069 isolates
    | {"\u200e", "\u200f"}                    # LRM / RLM marks
)

# Script ranges for the per-token homoglyph check.
_CYRILLIC = (0x0400, 0x04FF)
_GREEK = (0x0370, 0x03FF)
_TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)  # contiguous alphanumeric run

# HTML comment + the recognized Cairn marker grammar (exempt).
_HTML_COMMENT_RE = re.compile(r"<!--(.*?)-->", re.S)
_CAIRN_MARKER_RE = re.compile(r"^\s*cairn(:slot|:end|-accept)\b", re.I)
_IMPERATIVE_IN_COMMENT_RE = re.compile(
    r"\b(ignore|disregard|send|email|upload|post|exfiltrate|execute|run|"
    r"delete|overwrite|reveal|leak|do\s+not\s+tell)\b",
    re.I,
)

# Suppression markers.
_ACCEPT_RE = re.compile(
    r"<!--\s*cairn-accept:\s*(?P<pid>[\w-]+)\s*(?P<attrs>.*?)-->", re.S
)
_ACCEPT_END_RE = re.compile(
    r"<!--\s*cairn-accept-end:\s*(?P<pid>[\w-]+)\s*-->", re.I
)
_ATTR_RE = re.compile(r"(\w+)=(\"[^\"]*\"|'[^']*'|\S+)")


# --------------------------------------------------------------------------
# URL allowlist (configurable -- plan-review P3.6)

def load_url_allowlist(path: Path | None = None) -> set[str]:
    """Load allowed URL domains, one per line (``#`` comments, blanks
    ignored).  Missing file -> empty set.  Lets a legitimate domain be
    added without editing the scanner."""
    target = path if path is not None else _DEFAULT_ALLOWLIST
    try:
        text = target.read_text(encoding="utf-8")
    except (OSError, FileNotFoundError):
        return set()
    out: set[str] = set()
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip().lower()
        if line:
            out.add(line)
    return out


def _domain_allowed(domain: str, allowlist: set[str]) -> bool:
    d = domain.lower().split(":", 1)[0]  # strip any port
    # Allow an exact domain or any subdomain of an allowlisted domain.
    return any(d == a or d.endswith("." + a) for a in allowlist)


# --------------------------------------------------------------------------
# Suppression parsing

def _attrs(attr_text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, val in _ATTR_RE.findall(attr_text):
        if val[:1] in ("\"", "'") and val[-1:] == val[:1]:
            val = val[1:-1]
        out[key.lower()] = val
    return out


def _parse_suppressions(lines: list[str]) -> dict[str, set[int]]:
    """Map ``pattern_id`` -> set of 1-based line numbers where a hit of
    that pattern is suppressed.

    Line-scope: a valid marker on line ``M`` suppresses its pattern on
    line ``M`` (an inline marker) and line ``M+1`` (the marker annotates
    the line just below it) -- equivalently, a hit is cleared by a marker
    on the hit's own line or the line immediately preceding it.
    Block-scope: a matching ``cairn-accept-end`` on line ``K`` extends
    suppression to ``[M, K]``.  An unclosed open keeps only its
    line-scope (fail-safe).  A marker missing a non-empty ``reason=`` is
    invalid and suppresses nothing.
    """
    suppressed: dict[str, set[int]] = defaultdict(set)
    open_blocks: dict[str, int] = {}
    for i, line in enumerate(lines, start=1):
        for m in _ACCEPT_RE.finditer(line):
            pid = m.group("pid")
            attrs = _attrs(m.group("attrs"))
            if not attrs.get("reason", "").strip():
                continue  # invalid marker -- no suppression
            suppressed[pid].update({i, i + 1})  # line-scope (own + following)
            open_blocks[pid] = i
        for m in _ACCEPT_END_RE.finditer(line):
            pid = m.group("pid")
            start = open_blocks.pop(pid, None)
            if start is not None:
                suppressed[pid].update(range(start, i + 1))
    return suppressed


# --------------------------------------------------------------------------
# Detectors (each yields (lineno, message))

def _scan_imperative_override(lines: list[str]):
    for i, line in enumerate(lines, start=1):
        for re_ in _IMPERATIVE_OVERRIDE_RES:
            if re_.search(line):
                yield i, "imperative-override phrase"
                break


def _scan_egress(lines: list[str]):
    for i, line in enumerate(lines, start=1):
        if _EGRESS_RE.search(line):
            yield i, "egress/exfiltration verb near a destination"


def _scan_urls(lines: list[str], allowlist: set[str]):
    for i, line in enumerate(lines, start=1):
        for m in _URL_RE.finditer(line):
            if not _domain_allowed(m.group(1), allowlist):
                yield i, f"non-allowlisted external URL: {m.group(0)}"


def _scan_unicode(lines: list[str], leading_bom: bool):
    for i, line in enumerate(lines, start=1):
        for idx, ch in enumerate(line):
            if ch in _ZERO_WIDTH:
                # A leading U+FEFF at the very start of the file (line 1,
                # col 0) is a benign BOM -- ignore it there only.
                if ch == "\ufeff" and i == 1 and idx == 0 and leading_bom:
                    continue
                yield i, f"zero-width character U+{ord(ch):04X}"
                break
        for ch in line:
            if ch in _BIDI:
                yield i, f"bidirectional-control character U+{ord(ch):04X}"
                break


def _token_scripts(token: str) -> set[str]:
    scripts: set[str] = set()
    for ch in token:
        o = ord(ch)
        if (("a" <= ch <= "z") or ("A" <= ch <= "Z")
                or (0x00C0 <= o <= 0x024F)):  # Latin + Latin Extended
            scripts.add("latin")
        elif _CYRILLIC[0] <= o <= _CYRILLIC[1]:
            scripts.add("cyrillic")
        elif _GREEK[0] <= o <= _GREEK[1]:
            scripts.add("greek")
    return scripts


def _scan_homoglyph(lines: list[str]):
    for i, line in enumerate(lines, start=1):
        for m in _TOKEN_RE.finditer(line):
            if len(_token_scripts(m.group(0))) > 1:
                yield i, f"mixed-script token (possible homoglyph): {m.group(0)!r}"
                break


def _scan_html_comments(text: str, lines: list[str]):
    # Map character offsets to line numbers for multi-line comments.
    for m in _HTML_COMMENT_RE.finditer(text):
        body = m.group(1)
        if _CAIRN_MARKER_RE.match(body):
            continue  # recognized cairn marker -- exempt
        if _IMPERATIVE_IN_COMMENT_RE.search(body):
            line = text.count("\n", 0, m.start()) + 1
            yield line, "instruction-bearing HTML comment"


# --------------------------------------------------------------------------
# scan_text / scan_file

def scan_text(
    text: str,
    *,
    scan_urls: bool = True,
    url_allowlist: set[str] | None = None,
) -> list[Flag]:
    """Scan *text* and return unsuppressed flags.

    ``scan_urls`` enables the ``suspicious-url`` detector (use for
    executed templates; off for discussion prose).  ``url_allowlist``
    overrides the default allowlist file.
    """
    allowlist = url_allowlist if url_allowlist is not None else load_url_allowlist()
    leading_bom = text[:1] == "\ufeff"
    lines = text.split("\n")
    suppressed = _parse_suppressions(lines)

    raw: list[Flag] = []
    for lineno, msg in _scan_imperative_override(lines):
        raw.append(Flag("imperative-override", lineno, msg))
    for lineno, msg in _scan_egress(lines):
        raw.append(Flag("egress", lineno, msg))
    if scan_urls:
        for lineno, msg in _scan_urls(lines, allowlist):
            raw.append(Flag("suspicious-url", lineno, msg))
    for lineno, msg in _scan_unicode(lines, leading_bom):
        pid = "unicode-bidi" if "bidirectional" in msg else "unicode-zero-width"
        raw.append(Flag(pid, lineno, msg))
    for lineno, msg in _scan_homoglyph(lines):
        raw.append(Flag("homoglyph", lineno, msg))
    for lineno, msg in _scan_html_comments(text, lines):
        raw.append(Flag("instruction-html-comment", lineno, msg))

    return [f for f in raw if f.line not in suppressed.get(f.pattern_id, set())]


def scan_file(
    path: Path,
    *,
    scan_urls: bool = True,
    url_allowlist: set[str] | None = None,
) -> list[Flag]:
    """Scan one file and return unsuppressed flags."""
    text = path.read_text(encoding="utf-8", errors="replace")
    return scan_text(text, scan_urls=scan_urls, url_allowlist=url_allowlist)


# --------------------------------------------------------------------------
# CLI

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="content_scan",
        description="Content-integrity tripwire over agent-loaded prose. "
                    "Forces human review on a match; not a safety proof.",
    )
    parser.add_argument("files", nargs="*", type=Path,
                        help="Markdown / text files to scan.")
    parser.add_argument("--no-urls", action="store_true",
                        help="Skip the suspicious-url detector (for "
                             "discussion prose that legitimately cites URLs).")
    parser.add_argument("--allowlist", type=Path, default=None,
                        help="URL-domain allowlist file (default: "
                             "scripts/content_scan_allowlist.txt).")
    args = parser.parse_args(argv)

    if not args.files:
        print("content_scan: no files given.", file=sys.stderr)
        return 2

    allowlist = load_url_allowlist(args.allowlist)
    result = ScanResult()
    for f in args.files:
        if not f.is_file():
            print(f"content_scan: not a file: {f}", file=sys.stderr)
            return 2
        flags = scan_file(f, scan_urls=not args.no_urls, url_allowlist=allowlist)
        result.files_scanned += 1
        for flag in flags:
            result.flags.append(flag)
            print(f"  {f}:{flag.line}: [{flag.pattern_id}] {flag.message}",
                  file=sys.stderr)

    if result.flags:
        print(
            f"content_scan: {len(result.flags)} flag(s) across "
            f"{result.files_scanned} file(s) -- human review required "
            f"(suppress a reviewed hit with a `cairn-accept` marker).",
            file=sys.stderr,
        )
        return 1
    print(f"content_scan: OK -- {result.files_scanned} file(s) scanned; "
          f"no flags.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
