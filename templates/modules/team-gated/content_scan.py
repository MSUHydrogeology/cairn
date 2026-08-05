#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

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
file safe.

**Dual role (single-sourced).**  This one file serves two callers: Cairn
composes it via ``scripts/check_cairn.py`` over its **own** source prose
(Layer 2) and scaffolded generated output (Layer 3); and the
``content-security`` module ships it **verbatim to adopters** (installed
as ``scripts/content_scan.py``) so an adopter's agents can scan
working-tree files / incoming PRs for these patterns before ingesting
them.  Same code, no second copy.  (Rule 8 carries the separate
adopter-side profile-trust obligation.)

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
  ignored there; it flags only *after* the first character.  **Meaning
  unchanged** by the ignorable/tag detectors below: a character this id
  owns is skipped by both of them, so an existing ``cairn-accept:
  unicode-zero-width`` marker and an existing residual fingerprint keep
  their exact prior effect.
* ``unicode-bidi`` -- bidirectional-control characters (U+202A-202E,
  U+2066-2069), the "innocent to a human, instruction to a parser"
  vector.  **Meaning unchanged**, on the same skip rule.
* ``unicode-tag`` -- a code point in the Unicode **Tag block**
  (U+E0000-U+E007F), a complete shadow ASCII alphabet that renders as
  nothing: re-encoding a sentence into it produces text a human cannot
  see, ``git diff`` does not show, and a model reads normally.  It has
  its **own** id rather than sharing ``unicode-ignorable`` so a
  good-faith acceptance written for a benign emoji variation selector
  cannot silence a shadow-alphabet payload in the same block.  Never
  benign in agent-loaded Markdown.  **Detects, never rewrites.**
* ``unicode-ignorable`` -- a code point in RFC 8264 (PRECIS) § 9.13
  ``PrecisIgnorableProperties``: ``Default_Ignorable_Code_Point`` union
  ``Noncharacter_Code_Point``, held as hard-coded numeric range tables
  and **minus** the Tag block above.  Covers the invisible channel the
  three ids above do not -- SOFT HYPHEN inside a word, the variation
  selectors, HANGUL FILLER (general category ``Lo``, so it sits inside a
  token without even splitting it), the noncharacters.  The flag names
  the **count and every distinct code point on the line**, not only the
  first.  *Declared limit*: the tables are a pinned snapshot of one
  Unicode version, not a live derivation -- a code point added by a
  later UCD is a silent gap until the tables move.  **Detects, never
  rewrites.**
* ``unicode-line-separator`` -- a raw U+2028 LINE SEPARATOR or U+2029
  PARAGRAPH SEPARATOR.  Both are ``White_Space=Yes`` and so are excluded
  by construction from the ignorable-code-point derivations; nothing else
  here catches them.  The detector **flags and never rewrites**.
  *Declared limit*: one separator flag per line, and the flag names the
  first separator on that line.  **Suppression is narrower for this id
  than for any other**, because it is the first detected code point for
  which a *file* line and a *display* line differ: (i) an acceptance is
  honoured only when the marker renders on the **same display line** as
  the separator it accepts -- in practice, the marker is written *before*
  that separator on the file line; and (ii) the **block form**
  (``cairn-accept`` ... ``cairn-accept-end`` spanning the hit) does
  **not** suppress this id.  An acceptance on the preceding file line, or
  later on the same file line, is refused rather than honoured -- it
  would annotate a hit a human reading rendered text never sees beside
  it.
* ``homoglyph`` -- a single token in which **a character imitates a Latin
  letter**.  Note what changed: a flag no longer means merely *this token
  contains Greek*, it means *something here has an ASCII-Latin
  look-alike*, so ordinary scientific notation (``λmax``, ``ΔG``,
  ``σy``) is no longer reported as a prompt-injection attempt.
  Evaluated **per contiguous alphanumeric token**, not per line, so a
  Latin word beside a Cyrillic word does not false-flag.  Four clauses,
  any one of which flags:

  0. two or more distinct non-Latin confusable scripts in one token;
  1. a **whole-script** confusable token -- **for Greek** (at least three
     letters, every one of them ASCII-confusable), plus a *separate*
     fullwidth-Latin arm (U+FF21-U+FF5A is a bijection onto ASCII, so it
     needs no confusability table and closes script-generally);
  2. a non-Greek confusable script mixed with Latin (Cyrillic, Armenian,
     Cherokee, Coptic, fullwidth) -- unchanged behaviour;
  3. Greek mixed with Latin where a Greek character is ASCII-confusable.

  A narrow, exact-token **scientific-unit allowance** (RV5) clears the
  micro / ohm unit shapes (``µs``, ``µmol``, ``kΩ``, ...) that are
  structurally mixed-script in scientific prose; a mixed-script
  *credential* token still flags.

  **Two declared limits, both priced rather than overlooked.**
  ``_NO_LATIN_TWIN`` is **reviewed curation, not a derivation**: no
  external oracle attests it and ``unicodedata`` exposes none.  The exact
  known false-negative boundary is a spoof the old script-blind rule caught
  being cleared **only** when every Greek character it contains lies in the
  32-code-point NFD-fold closure ``U+0394 U+03A9 U+03B2 U+03B8 U+03BB
  U+03BC U+03C3 U+03C6 U+03C8 U+03D1 U+03D5 U+03D6 U+038F
  U+1F68-U+1F6F U+1FA8-U+1FAF U+1FFA-U+1FFC``, **or** it is the
  two-character Latin-plus-Greek shape, **or** RV5 already cleared it.  NFD
  folding **widens clearing** under this denylist: the 20 capital-omega
  variants after the first twelve entries are reached only through the
  fold.  **Whole-script Cyrillic does not flag** -- a residual the accepted
  Decision priced explicitly, on the reasoning that the severe case
  (authority granting) is closed elsewhere and an arm here would cost
  international proper nouns.
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
import unicodedata
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

# Zero-width, bidi-control and line/paragraph-separator characters.
# Members are literal control chars (with a naming comment each), written as
# **escape forms** (\uXXXX) and never raw, so this scanner carries none of the
# invisible code points it detects (trojansource-safe, bandit B613); the
# per-char comment names each.  Coverage expanded per code-review P3 (word
# joiner U+2060; LRM U+200E / RLM U+200F).
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
# The two separators nothing else here detects: both carry
# White_Space=Yes, so every Default_Ignorable_Code_Point derivation
# excludes them by construction.
_LINE_SEPARATORS = {
    "\u2028",  # line separator
    "\u2029",  # paragraph separator
}

# --------------------------------------------------------------------------
# The PRECIS ignorable set (RFC 8264 \u00a7 9.13 PrecisIgnorableProperties):
# Default_Ignorable_Code_Point union Noncharacter_Code_Point.
#
# Held as **numeric ranges, never raw characters**, so this scanner carries
# none of the invisible code points it detects (trojansource-safe; the
# TestSourceCarriesNoRawInvisibles invariant depends on it).
#
# `Default_Ignorable_Code_Point` is a **derived** property, NOT general
# category `Cf`: its members span `Cf`, `Mn`, `Lo` and `Cn`, so a `Cf` sweep
# reaches neither six of the rows below nor any noncharacter.  Verified
# against the authoritative DerivedCoreProperties-15.1.0.txt: the 17 rows
# below cover the property **exactly** -- 4174 code points, zero on either
# side of the difference.
_IGNORABLE_RANGES: tuple[tuple[int, int], ...] = (
    (0x00AD, 0x00AD),      # SOFT HYPHEN (Cf)
    (0x034F, 0x034F),      # COMBINING GRAPHEME JOINER (Mn)
    (0x061C, 0x061C),      # ARABIC LETTER MARK (Cf)
    (0x115F, 0x1160),      # HANGUL CHOSEONG/JUNGSEONG FILLER (Lo)
    (0x17B4, 0x17B5),      # KHMER VOWEL INHERENT AQ/AA (Mn)
    (0x180B, 0x180F),      # MONGOLIAN free variation selectors + vowel sep
    (0x200B, 0x200F),      # ZWSP..RLM (Cf)
    (0x202A, 0x202E),      # bidi embeddings / overrides (Cf)
    (0x2060, 0x206F),       # WJ, invisible operators, isolates, deprecated
    (0x3164, 0x3164),      # HANGUL FILLER (Lo -- does NOT split a token)
    (0xFE00, 0xFE0F),      # VARIATION SELECTOR-1..16 (Mn)
    (0xFEFF, 0xFEFF),      # ZERO WIDTH NO-BREAK SPACE / BOM (Cf)
    (0xFFA0, 0xFFA0),      # HALFWIDTH HANGUL FILLER (Lo)
    (0xFFF0, 0xFFF8),      # reserved (Cn)
    (0x1BCA0, 0x1BCA3),    # SHORTHAND FORMAT letters (Cf)
    (0x1D173, 0x1D17A),    # MUSICAL SYMBOL BEGIN BEAM..END PHRASE (Cf)
    (0xE0000, 0xE0FFF),    # tag block + variation selectors supplement +
                           # reserved.  The Tag block is carved OUT of this
                           # row by _TAG_RANGE below and gets its own id;
                           # the remainder (notably U+E0100-U+E01EF,
                           # VARIATION SELECTOR-17..256) stays here.
)

# Permanently-reserved code points, never assignable.  All are `Cn`, so the
# `Cf` sweep reaches none of them -- these 18 rows are guarded only here.
_NONCHARACTER_RANGES: tuple[tuple[int, int], ...] = (
    (0xFDD0, 0xFDEF),      # the Arabic Presentation Forms-A block reserve
    # U+nFFFE / U+nFFFF on every plane 0-16.
    (0x0FFFE, 0x0FFFF), (0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF),
    (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF), (0x5FFFE, 0x5FFFF),
    (0x6FFFE, 0x6FFFF), (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF),
    (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF), (0xBFFFE, 0xBFFFF),
    (0xCFFFE, 0xCFFFF), (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF),
    (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF),
)

#: The Unicode Tag block -- a complete shadow ASCII alphabet.  Carved out of
#: the U+E0000-U+E0FFF ignorable row above and given its **own** pattern id,
#: so a good-faith `cairn-accept: unicode-ignorable` written for an emoji
#: variation selector cannot silence a Tag-block payload inside its block.
_TAG_RANGE: tuple[int, int] = (0xE0000, 0xE007F)

#: Performance guard, and an **invariant**, not a heuristic: every code point
#: in every table above is >= this character, so skipping anything below it
#: can never skip a detected code point.  A naive per-character table walk
#: over the whole corpus is ~26x the cost of the pre-existing unicode pass;
#: with this guard it is *below* it, with an identical hit set.  The scanner's
#: composing caller runs under a fail-closed wall-clock budget, so this is a
#: correctness guard on a timeout, not a micro-optimisation.  Pinned by a
#: test that reads THIS constant, never a hard-coded literal.
_ASCII_GUARD = "\u00ad"  # SOFT HYPHEN -- the lowest covered code point

# Script ranges for the per-token homoglyph check. Mixing any two of these
# (or any of them with Latin) inside one token is a classic homoglyph
# vector. Curated, **not** exhaustive -- the scanner is a witness, not a
# proof; a hit is cleared with a `cairn-accept` marker. Expanded beyond the
# original Latin/Cyrillic/Greek per security-hardening Chunk 10 to cover the
# other common Latin-confusable scripts.
_SCRIPT_RANGES: tuple[tuple[str, int, int], ...] = (
    ("cyrillic", 0x0400, 0x052F),     # Cyrillic + Cyrillic Supplement
    ("greek", 0x0370, 0x03FF),        # Greek and Coptic block
    ("greek", 0x1F00, 0x1FFF),        # Greek Extended
    ("armenian", 0x0531, 0x058F),
    ("cherokee", 0x13A0, 0x13FF),
    ("cherokee", 0xAB70, 0xABBF),     # Cherokee Supplement
    ("coptic", 0x2C80, 0x2CFF),
    ("fullwidth-latin", 0xFF21, 0xFF5A),  # fullwidth A-Z / a-z
)
_TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)  # contiguous alphanumeric run

# HTML comment + the recognized Cairn marker grammar (exempt).
_HTML_COMMENT_RE = re.compile(r"<!--(.*?)-->", re.S)
_CAIRN_MARKER_RE = re.compile(
    r"^\s*(?:"
    r"cairn(?::slot|:end|-accept)"
    # The quality_gate.py neutrality-lint exemption family.  All are
    # Cairn-owned directive syntax intended to live in prose; they are
    # parsed by scripts/quality_gate.py and must not trip the
    # instruction-bearing-HTML-comment heuristic.
    r"|vendor-ok(?:-begin|-end)?"
    r"|case-study"
    # The claim_check.py document-scoped exemption family (ported into
    # Cairn 2026-05-28 from modflow_tools).  Same shape: Cairn-owned
    # directive syntax parsed by the default-on claim_check module.
    r"|claim-check-allow(?:-count)?"
    r")\b",
    re.I,
)
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
# Detectors (each yields (lineno, message); _scan_unicode is the one
# exception -- it yields (lineno, pattern_id, message), see its docstring)

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


def _in_ranges(o: int, ranges: tuple[tuple[int, int], ...]) -> bool:
    for lo, hi in ranges:
        if lo <= o <= hi:
            return True
    return False


def _codepoint_summary(counts: dict[str, int], what: str) -> str:
    """Render the flag message for a per-line ignorable/tag hit.

    Names the **count and every distinct code point on the line**, not only
    the first.  A benign variation selector earlier on a line must not mask
    a Tag-block payload later on it, and a reader who cannot see any of the
    characters has only this message to go on.

    ``unicodedata.name`` is called in its **two-argument** form: a reserved
    or unassigned code point has no name, and a missing name must never
    suppress a flag.
    """
    total = sum(counts.values())
    parts = []
    for ch, n in counts.items():
        label = f"U+{ord(ch):04X} ({unicodedata.name(ch, 'unnamed / reserved')})"
        parts.append(f"{label} x{n}" if n > 1 else label)
    return f"{total} {what} code point(s) on this line: " + ", ".join(parts)


def _scan_unicode(lines: list[str], leading_bom: bool):
    """Yield ``(lineno, pattern_id, message)`` -- **not** ``(lineno,
    message)`` like the other detectors.

    This generator covers more than one ``pattern_id``, so it names its own
    id rather than leaving the caller to guess one from the message text.  A
    message is prose and prose is not a dispatch key: a caller that derives
    the id by substring-matching the message labels every hit with whichever
    branch the substring happens to select, and an adopter's suppression
    marker then names an id the scanner never emits.
    """
    for i, line in enumerate(lines, start=1):
        for idx, ch in enumerate(line):
            if ch in _ZERO_WIDTH:
                # A leading U+FEFF at the very start of the file (line 1,
                # col 0) is a benign BOM -- ignore it there only.
                if ch == "\ufeff" and i == 1 and idx == 0 and leading_bom:
                    continue
                yield i, "unicode-zero-width", f"zero-width character U+{ord(ch):04X}"
                break
        for ch in line:
            if ch in _BIDI:
                yield (i, "unicode-bidi",
                       f"bidirectional-control character U+{ord(ch):04X}")
                break
        for ch in line:
            if ch in _LINE_SEPARATORS:
                yield (i, "unicode-line-separator",
                       f"unicode line/paragraph separator U+{ord(ch):04X}")
                break
        # The Tag block -- its own id, per the id-split rule at _TAG_RANGE.
        tag_hits: dict[str, int] = {}
        for ch in line:
            # The ASCII short-circuit.  INVARIANT: every code point in
            # _IGNORABLE_RANGES, _NONCHARACTER_RANGES and _TAG_RANGE is
            # >= _ASCII_GUARD, so this can never skip a detected code point.
            # Pinned by a test that reads _ASCII_GUARD, not a literal.
            if ch < _ASCII_GUARD:
                continue
            if _in_ranges(ord(ch), (_TAG_RANGE,)):
                tag_hits[ch] = tag_hits.get(ch, 0) + 1
        if tag_hits:
            yield i, "unicode-tag", _codepoint_summary(tag_hits,
                                                       "unicode Tag-block")
        # The rest of the PRECIS ignorable set + the noncharacters.
        ign_hits: dict[str, int] = {}
        for ch in line:
            if ch < _ASCII_GUARD:
                continue
            # THE SKIP RULE.  A character an existing id already owns keeps
            # its exact current meaning: it is reported under that id and
            # never doubled here, so no existing `cairn-accept` marker and
            # no existing residual fingerprint is invalidated.  U+FEFF is a
            # member of _ZERO_WIDTH, so the leading-BOM exemption above is
            # preserved on this path too -- a BOM never reaches this loop.
            if ch in _ZERO_WIDTH or ch in _BIDI or ch in _LINE_SEPARATORS:
                continue
            o = ord(ch)
            if _in_ranges(o, (_TAG_RANGE,)):
                continue  # owned by unicode-tag above
            if _in_ranges(o, _IGNORABLE_RANGES) or _in_ranges(
                    o, _NONCHARACTER_RANGES):
                ign_hits[ch] = ign_hits.get(ch, 0) + 1
        if ign_hits:
            yield i, "unicode-ignorable", _codepoint_summary(
                ign_hits, "default-ignorable")


# RV5 -- narrow scientific-unit homoglyph allowance. A Greek micro sign
# (U+00B5 MICRO SIGN or U+03BC GREEK SMALL LETTER MU) prefixing a short Latin
# SI unit (µs, µm, µg, µL, µmol, ...) and a Latin-prefixed ohm (Ω, kΩ, MΩ)
# are structurally-unavoidable mixed-script tokens in scientific prose. The
# allowance is EXACT-TOKEN and tightly bounded: only a micro-prefixed short
# Latin run or an ohm-unit shape is cleared, so a mixed-script *credential*
# token (e.g. a Cyrillic-spoofed 'pаssword' -- Latin+Cyrillic) still flags.
# A clearing here is a fold-up of the modflow_tools accepted-residual class
# [sci-unit]; it does not weaken the detector for any non-unit token.
_MICRO_SIGNS = "µμ"          # MICRO SIGN, GREEK SMALL LETTER MU
_OHM_SIGNS = "ΩΩ"            # GREEK CAPITAL OMEGA, OHM SIGN
_SCI_UNIT_RE = re.compile(
    r"^(?:"
    r"[" + _MICRO_SIGNS + r"][A-Za-z]{1,4}"      # µs, µmol, µL, ...
    r"|[kKMGTmnpfu]?[" + _OHM_SIGNS + r"]"        # Ω, kΩ, MΩ
    r")$"
)


def _is_scientific_unit(token: str) -> bool:
    """RV5: True for the curated micro / ohm scientific-unit token shapes that
    are cleared from the homoglyph check. Exact-token, deliberately narrow."""
    return bool(_SCI_UNIT_RE.match(token))


def _char_script(ch: str) -> str | None:
    """The script name for one character, or ``None`` for a non-letter (a
    digit) and for anything outside the curated ranges."""
    o = ord(ch)
    if (("a" <= ch <= "z") or ("A" <= ch <= "Z")
            or (0x00C0 <= o <= 0x024F)):  # Latin + Latin Extended
        return "latin"
    for name, lo, hi in _SCRIPT_RANGES:
        if lo <= o <= hi:
            return name
    return None


def _token_scripts(token: str) -> set[str]:
    # Written without an assignment expression on purpose: this file ships
    # verbatim to adopters, and the walrus form raises its measured syntactic
    # floor 3.7 -> 3.8 for no benefit.
    scripts: set[str] = set()
    for ch in token:
        name = _char_script(ch)
        if name is not None:
            scripts.add(name)
    return scripts


# --------------------------------------------------------------------------
# Confusability: which Greek letters actually have an ASCII-Latin look-alike.
#
# **Polarity is the whole design.**  This is a **denylist of NON-confusables**,
# not an allowlist of confusables.  An omission from an allowlist of
# confusables is a *silently missed spoof*; an omission from this denylist is
# a *visible false positive* an adopter reports.  One failure mode is
# discoverable and one is not, so erring toward the SMALLER set here is the
# safe direction -- a smaller denylist means more flagging.
#
# **This is reviewed curation, not a derivation.**  No external oracle
# attests it: `unicodedata` exposes no confusables, skeleton, script or
# identifier-status accessor, so the ASCII-twin judgments below are human
# judgment recorded per code point.  Membership is **never inherited from a
# base letter** -- each entry carries its own justification against the ASCII
# alphabet.  That single rule admits the theta/phi/pi *symbol* variants (none
# has an ASCII twin) and **refuses** the lunate sigma U+03F2, which is a
# variant of a seeded letter but reads as Latin `c`; inheritance would have
# admitted it and reopened a known bypass family.
# Members are **single-character `str` written as escape forms**.  Integer
# literals are forbidden: the int form invites `ord(normalize("NFD", ch))`,
# which raises on 217 of the 218 Greek Extended letters.  Escapes rather than
# raw letters because the raw forms of the entries below are mutually
# near-indistinguishable on screen -- U+03C6 vs U+03D5 is exactly the
# confusability this table is about, so a raw table is one a reviewer cannot
# audit.
_NO_LATIN_TWIN = frozenset({
    # -- Seeded, and pinned by a published figure: dropping any of these
    #    moves the published scientific-residual count, so each is checkable
    #    against the module doc rather than only asserted.
    "\u0394",  # GREEK CAPITAL LETTER DELTA -- no ASCII letter is a triangle
    "\u03bb",  # GREEK SMALL LETTER LAMDA -- no ASCII twin
    "\u03c3",  # GREEK SMALL LETTER SIGMA -- ASCII `o` has no descender/hook
    "\u03b8",  # GREEK SMALL LETTER THETA -- crossed bowl; no ASCII twin
    "\u03c6",  # GREEK SMALL LETTER PHI -- no ASCII twin
    "\u03c8",  # GREEK SMALL LETTER PSI -- trident; no ASCII twin
    "\u03b2",  # GREEK SMALL LETTER BETA -- reads as beta, not Latin `b`
               #   (ascender rises left of the bowl; it has a descender)
    "\u03a9",  # GREEK CAPITAL LETTER OMEGA -- no ASCII twin
    # -- Seeded, and figure-unconstrained: dropping it leaves both decisive
    #    published figures bit-identical, because the scientific token set's
    #    micro tokens are U+00B5 MICRO SIGN, not U+03BC.  Recorded as
    #    judgment, not as a figure-pinned entry, so nobody reads a
    #    reconciliation test as attesting it.  Its exposure is longer tokens
    #    such as U+03BC + "pload"; RV5 already clears the short unit shapes.
    "\u03bc",  # GREEK SMALL LETTER MU -- reads as micro, not Latin `u`
    # -- Admitted variants, each on its OWN justification (not inherited
    #    from the seeded base letter it resembles).  The same rule REFUSES
    #    U+03F2 GREEK LUNATE SIGMA SYMBOL, a variant of seeded U+03C3 that
    #    reads as Latin `c`.
    "\u03d1",  # GREEK THETA SYMBOL -- script theta; no ASCII twin
    "\u03d5",  # GREEK PHI SYMBOL -- no ASCII twin
    "\u03d6",  # GREEK PI SYMBOL -- no ASCII twin
})

#: Fullwidth Latin.  A **bijection** onto ASCII A-Z/a-z by construction, so it
#: needs no confusability table at all, and it carries no legitimate
#: proper-noun cost in an English tree -- a pure-loss vector, closable
#: script-generally at zero natural-language cost.
_FULLWIDTH_LATIN = (0xFF21, 0xFF5A)


def _is_confusable_greek(ch: str) -> bool:
    """True when *ch* has an ASCII-Latin look-alike, i.e. it is NOT in the
    curated no-twin denylist.

    NFD-folds first, so an accented or breathed form is judged by its base
    letter.  **The arity is pinned**: ``normalize("NFD", ch)`` of a Greek
    Extended letter is a *multi-character* string, so the ``[0]`` is
    load-bearing -- an ``ord(normalize(...))`` form raises ``TypeError`` on
    217 of the 218 Greek Extended letters.

    *Named consequence of the polarity*: under a **denylist** the fold
    **widens clearing** rather than closing a bypass.  It reaches 20 further
    code points, all capital-omega variants -- U+038F, U+1F68-U+1F6F,
    U+1FA8-U+1FAF, U+1FFA-U+1FFC -- which makes the effective no-twin closure
    32 code points, not 12.  Re-derived against this table, not carried.
    """
    return unicodedata.normalize("NFD", ch)[0] not in _NO_LATIN_TWIN


def _has_two_non_latin_scripts(scripts: set[str]) -> bool:
    """CLAUSE 0 -- two or more distinct non-Latin confusable scripts in one
    token, Latin excluded from the count.

    Extracted as its own named predicate so it can be disabled *by itself*
    in a test.  A test that only shows a token flagging cannot distinguish
    "clause 0 caught it" from "some other clause caught it"; disabling this
    one function and re-running is what makes that attributable.
    """
    return "latin" not in scripts and len(scripts - {"latin"}) >= 2


def _token_is_confusable(token: str) -> bool:
    """The four-clause confusability rule.  A token flags when ANY holds.

    A flag now means *a character here imitates a Latin letter*, not merely
    *this token contains Greek* -- which is why ordinary scientific notation
    stops being reported as a prompt-injection attempt.
    """
    scripts = _token_scripts(token)
    has_latin = "latin" in scripts
    non_latin = scripts - {"latin"}

    # CLAUSE 0, evaluated first.  This is the pre-existing script-blind rule
    # restricted to the no-Latin case, so it removes no flag and adds none:
    # measured zero-cost, because all 37 published scientific false
    # positives carry exactly ONE non-Latin script.
    if _has_two_non_latin_scripts(scripts):
        return True

    letters = [ch for ch in token if ch.isalpha()]

    # CLAUSE 1 -- whole-script confusable, **for Greek**, plus a separate
    # fullwidth arm.  Whole-script CYRILLIC is deliberately NOT an arm: it is
    # a declared residual, priced by the accepted Decision.  The severe
    # consequence of a Cyrillic homoglyph in a Cairn tree is *authority
    # granting* (a byline flipping `ai` to `human`), and that path is closed
    # independently by byline classification; an arm here would add prose
    # detection at a real cost to international proper nouns.  A future
    # change to this is a Decision, not a code tidy-up.
    if (not has_latin and non_latin == {"greek"} and len(letters) >= 3
            and all(_is_confusable_greek(ch) for ch in letters)):
        return True
    # The fullwidth arm, separate and script-general (see _FULLWIDTH_LATIN).
    if len(letters) >= 3 and all(
            _FULLWIDTH_LATIN[0] <= ord(ch) <= _FULLWIDTH_LATIN[1]
            for ch in letters):
        return True

    # CLAUSE 2 -- a non-Greek confusable script mixed with Latin always
    # flags (Cyrillic, Armenian, Cherokee, Coptic, fullwidth).  Unchanged
    # behaviour for any token containing a Latin character; the no-Latin
    # case is clause 0's, and without clause 0 this sentence is false.
    if has_latin and (non_latin - {"greek"}):
        return True

    # CLAUSE 3 -- Greek mixed with Latin, where a Greek character actually
    # has an ASCII twin.
    if has_latin and "greek" in non_latin:
        greek = [ch for ch in letters if _char_script(ch) == "greek"]
        latin = [ch for ch in letters if _char_script(ch) == "latin"]
        # The declared two-character carve-out: exactly one Latin letter,
        # exactly one Greek letter, total length two.  This is the shape
        # scientific variable-plus-subscript notation takes, and a
        # two-character token cannot carry an instruction on its own.
        if len(latin) == 1 and len(greek) == 1 and len(token) == 2:
            return False
        if any(_is_confusable_greek(ch) for ch in greek):
            return True
    return False


def _scan_homoglyph(lines: list[str]):
    for i, line in enumerate(lines, start=1):
        for m in _TOKEN_RE.finditer(line):
            token = m.group(0)
            if _is_scientific_unit(token):
                continue  # RV5: curated scientific-unit allowance
            if _token_is_confusable(token):
                yield i, f"mixed-script token (possible homoglyph): {token!r}"
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

def _separator_accept_is_associable(line: str) -> bool:
    """True when *line* carries a valid ``unicode-line-separator``
    acceptance that renders on the **same display line** as the first
    separator on it -- i.e. the marker is written *before* that separator.

    Suppression line-scope is *file*-line scope.  U+2028 / U+2029 are the
    first detected code points for which a file line and a display line
    differ, so an acceptance on the preceding file line, or later on the
    same file line, annotates something a human reading rendered text never
    sees beside the hit.  Such an acceptance is refused -- the caller
    re-emits the flag -- and so is the block form, which is even less
    reliably associable.  The marker that works goes before the separator.

    Validity is the same rule ``_parse_suppressions`` applies: the marker
    must name this ``pattern_id`` and carry a non-empty ``reason=``.
    """
    sep_idx = min(
        (line.index(ch) for ch in _LINE_SEPARATORS if ch in line),
        default=None,
    )
    if sep_idx is None:
        return False
    for m in _ACCEPT_RE.finditer(line):
        if m.end() > sep_idx:
            continue  # not before the separator -- different display line
        if m.group("pid") != "unicode-line-separator":
            continue
        if _attrs(m.group("attrs")).get("reason", "").strip():
            return True
    return False


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
    # This generator yields its own pattern id because a message is prose
    # and prose is not a dispatch key.
    for lineno, pid, msg in _scan_unicode(lines, leading_bom):
        raw.append(Flag(pid, lineno, msg))
    for lineno, msg in _scan_homoglyph(lines):
        raw.append(Flag("homoglyph", lineno, msg))
    for lineno, msg in _scan_html_comments(text, lines):
        raw.append(Flag("instruction-html-comment", lineno, msg))

    out: list[Flag] = []
    for f in raw:
        if f.line not in suppressed.get(f.pattern_id, set()):
            out.append(f)
            continue
        # Suppressed by the per-id file-line scope.  For every pattern id but
        # one, that is the whole rule.  `unicode-line-separator` is narrower:
        # the acceptance must render on the same *display* line as the
        # separator it accepts, so an unassociable acceptance is refused and
        # the flag is re-emitted.  No other id's path changes here.
        if (f.pattern_id == "unicode-line-separator"
                and not _separator_accept_is_associable(lines[f.line - 1])):
            out.append(f)
    return out


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
