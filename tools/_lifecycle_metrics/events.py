# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""The ``cairn-event-v1`` grammar: closed-schema HTML-comment blocks a
lifecycle-artifact edit appends alongside the act it records (a status
transition, a review pass, a Response), read back by the history-diff
algorithm this module also carries.

This module is the ``metrics-events-not-prose`` Part 3 replacement for
prose-parsing the retained event-shaped fields (``review_rounds``,
reviewer identity/tier, ``response_models``, the stage-timing columns):
instead of scraping section headings and regex-matched fields out of
file text, the same edit that performs a lifecycle act appends a small,
closed-vocabulary block declaring what it just did, and the extractor
reads those blocks back rather than re-deriving the act from prose.

Three block shapes, reproduced verbatim from the accepted proposal's
Round 7 §1 as the binding contract this module pins:

    <!-- cairn-event-v1
    kind: transition
    from_state: reviewed
    to_state: revised
    -->

    <!-- cairn-event-v1
    kind: review-pass
    tier: External
    reviewer: <reviewer name as written in the section heading>
    -->

    <!-- cairn-event-v1
    kind: response
    model: <model identity as written in the Response's **Model** field>
    -->

**No import of ``.extract``.**  ``extract.py`` imports THIS module for
reconciliation (wiring the retained fields to reconciled blocks); a
loader call the other direction would be circular.  Every function here
that needs the runtime status vocabulary (the ``from_state``/``to_state``
bound) takes it as an explicit ``valid_states`` parameter instead of
loading it itself -- the caller (``extract.py``, which already owns the
contained vocabulary loader) supplies it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Optional, Sequence, Tuple


# --------------------------------------------------------------- grammar


#: The literal version token, as it appears in the fence (``<!--
#: cairn-event-v1``).  Any other token after ``cairn-event-`` is a
#: recognized-but-unsupported fence and refuses (never silently ignored
#: -- an adopter who upgrades to a v2 grammar someday must not have
#: their v2 blocks silently vanish from a v1-only reader).
VERSION_TOKEN = "cairn-event-v1"

#: The suffix ``_FENCE_RE`` captures after the shared ``cairn-event-``
#: prefix -- compared against directly so the prefix is not double-
#: counted (``VERSION_TOKEN`` names the whole fence word for messages
#: and docs; this is the bare suffix the regex group actually yields).
_VERSION_SUFFIX = "v1"

#: The three event kinds the closed grammar admits.
KIND_TRANSITION = "transition"
KIND_REVIEW_PASS = "review-pass"
KIND_RESPONSE = "response"
VALID_KINDS: Tuple[str, ...] = (KIND_TRANSITION, KIND_REVIEW_PASS, KIND_RESPONSE)

#: Required keys per kind, beyond the universal ``kind`` itself.
_REQUIRED_KEYS: Dict[str, Tuple[str, ...]] = {
    KIND_TRANSITION: ("from_state", "to_state"),
    KIND_REVIEW_PASS: ("tier", "reviewer"),
    KIND_RESPONSE: ("model",),
}

#: Every key a given kind admits -- ``kind`` and the optional
#: ``recorded_by`` are legal on all three; anything else is scoped to
#: its own kind.  An unknown key refuses rather than being silently
#: dropped.
_ALLOWED_KEYS: Dict[str, frozenset] = {
    kind: frozenset({"kind", "recorded_by"}) | frozenset(_REQUIRED_KEYS[kind])
    for kind in VALID_KINDS
}

#: ``tier``'s closed bound (``review-pass`` only).
VALID_TIERS: Tuple[str, ...] = ("Internal", "External", "Security", "Code")

#: ``reviewer`` / ``model`` / ``recorded_by`` share one bound: at most
#: 120 characters, single line (already guaranteed by the line-based
#: parser below -- a value can never itself contain a newline).
_MAX_FIELD_LEN = 120

#: One ``key: value`` body line.  The key is a bare identifier; the value
#: is everything after the first ``:`` on the line, stripped.
_FIELD_LINE_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$')

#: The fence itself: an HTML comment opening with ``cairn-event-<token>``.
#: Captures the version token and the body between the opening line and
#: the closing ``-->``, across the whole document (``re.DOTALL``).
_FENCE_RE = re.compile(
    r'<!--\s*cairn-event-(?P<version>\S+)\s*\n(?P<body>.*?)-->',
    re.DOTALL,
)


class EventGrammarError(ValueError):
    """A ``cairn-event-*`` fence exists but fails to validate the closed
    grammar above.  Raised rather than returned so a caller cannot
    accidentally treat a partially-parsed, invalid block as clean data --
    refuses, never ignores, never defaults, per Round 7 §1's own text."""


@dataclass(frozen=True)
class EventBlock:
    """One validated ``cairn-event-v1`` block.

    ``fields`` carries every key present in the block (including
    ``kind`` itself and ``recorded_by`` when present), already bounds-
    checked.  ``raw`` is the exact verbatim text of the block, from the
    opening ``<!--`` through the closing ``-->`` -- used by the history
    reader (below / Chunk 5) for byte-exact mutation detection: a block
    edited in ANY way, including whitespace, no longer compares equal to
    its earlier self, which is the maximally sensitive reading of "an
    existing block was mutated" from Round 7 §2 step 2."""

    kind: str
    fields: Mapping[str, str] = field(default_factory=dict)
    raw: str = ""

    @property
    def from_state(self) -> str:
        return self.fields.get("from_state", "")

    @property
    def to_state(self) -> str:
        return self.fields.get("to_state", "")

    @property
    def tier(self) -> str:
        return self.fields.get("tier", "")

    @property
    def reviewer(self) -> str:
        return self.fields.get("reviewer", "")

    @property
    def model(self) -> str:
        return self.fields.get("model", "")

    @property
    def recorded_by(self) -> str:
        """Informational only -- explicitly barred from authority,
        identity, and idempotency (Round 7's closed key table)."""
        return self.fields.get("recorded_by", "")


def _line_of(text: str, offset: int) -> int:
    """1-indexed line number of ``offset`` within ``text`` -- for
    refusal messages a human can act on without re-deriving it."""
    return text.count("\n", 0, offset) + 1


def parse_event_blocks(
    text: str, *, valid_states: Sequence[str],
) -> List[EventBlock]:
    """Parse every ``cairn-event-*`` fence in ``text`` into validated
    :class:`EventBlock` objects, in document order.

    ``valid_states`` bounds ``from_state``/``to_state`` -- the caller
    (``extract.py``) supplies the real runtime vocabulary (current +
    historical, per artifact kind); this function performs no loading of
    its own.  Text carrying no fence at all returns an empty list
    (nothing is wrong with a document that has not yet recorded any
    events).  A fence that fails to validate -- unknown key, unknown
    kind, unknown version token, missing required key, or a value
    outside its bounds -- raises :class:`EventGrammarError` naming the
    line and the reason; the whole call refuses rather than silently
    skipping the one bad block and returning the rest."""
    blocks: List[EventBlock] = []
    for m in _FENCE_RE.finditer(text):
        line_no = _line_of(text, m.start())
        version = m.group("version")
        if version != _VERSION_SUFFIX:
            raise EventGrammarError(
                f"line {line_no}: unknown event version token "
                f"'cairn-event-{version}' -- only '{VERSION_TOKEN}' is "
                f"recognized"
            )
        body = m.group("body")
        raw = m.group(0)

        parsed: Dict[str, str] = {}
        for body_line in body.splitlines():
            stripped = body_line.strip()
            if not stripped:
                continue
            fm = _FIELD_LINE_RE.match(stripped)
            if not fm:
                raise EventGrammarError(
                    f"line {line_no}: malformed event field line "
                    f"{stripped!r} -- expected 'key: value'"
                )
            key, value = fm.group(1), fm.group(2).strip()
            if key in parsed:
                raise EventGrammarError(
                    f"line {line_no}: duplicate event key '{key}'"
                )
            parsed[key] = value

        if "kind" not in parsed:
            raise EventGrammarError(
                f"line {line_no}: event block is missing the required "
                f"'kind' key"
            )
        kind = parsed["kind"]
        if kind not in VALID_KINDS:
            raise EventGrammarError(
                f"line {line_no}: unknown event kind '{kind}' -- expected "
                f"one of {', '.join(VALID_KINDS)}"
            )

        allowed = _ALLOWED_KEYS[kind]
        unknown = sorted(set(parsed) - allowed)
        if unknown:
            raise EventGrammarError(
                f"line {line_no}: unknown key(s) for kind '{kind}': "
                f"{', '.join(unknown)}"
            )
        missing = [k for k in _REQUIRED_KEYS[kind] if k not in parsed]
        if missing:
            raise EventGrammarError(
                f"line {line_no}: event kind '{kind}' is missing required "
                f"key(s): {', '.join(missing)}"
            )

        if kind == KIND_TRANSITION:
            for state_key in ("from_state", "to_state"):
                value = parsed[state_key]
                if value not in valid_states:
                    raise EventGrammarError(
                        f"line {line_no}: {state_key} {value!r} is not a "
                        f"declared lifecycle status for this artifact type"
                    )
        if kind == KIND_REVIEW_PASS and parsed["tier"] not in VALID_TIERS:
            raise EventGrammarError(
                f"line {line_no}: tier {parsed['tier']!r} is not one of "
                f"{', '.join(VALID_TIERS)}"
            )
        for len_bound_key in ("reviewer", "model", "recorded_by"):
            if len_bound_key in parsed and len(parsed[len_bound_key]) > _MAX_FIELD_LEN:
                raise EventGrammarError(
                    f"line {line_no}: {len_bound_key} exceeds "
                    f"{_MAX_FIELD_LEN} characters"
                )

        blocks.append(EventBlock(kind=kind, fields=dict(parsed), raw=raw))
    return blocks
