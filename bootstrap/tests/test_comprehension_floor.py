"""The comprehension floor must reach the adopter, not only the doctrine.

`doctrine/rationale.md` states the floor and its grounding, but `doctrine/` is
**not installed into an adopter tree** -- so a rule that lives only there binds
nobody who adopts Cairn. The operational form therefore has to sit in
`templates/core/AGENTS.md`, the file every adopter receives and every agent
loads each session, and in Cairn's own root `AGENTS.md` so Cairn is bound by it
too.

This module asserts that parity. It checks for the load-bearing *elements* of
the rule rather than one exact sentence, so a rewording that preserves the
obligation passes and a deletion fails.

Run from the Cairn repo root:
    python -m pytest bootstrap/tests/test_comprehension_floor.py
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent

#: Both files carrying the operational rule. The shipped template is the
#: load-bearing one (adopters receive it); the root copy keeps Cairn bound by
#: the rule it ships.
_AGENTS_FILES = ("templates/core/AGENTS.md", "AGENTS.md")

#: The obligations the rule must express, each as an alternation so a
#: reworded-but-equivalent rule still passes. Presence of the phrase is not the
#: property under test -- presence of the *obligation* is.
_REQUIRED = {
    "comprehension is a precondition, not a courtesy":
        r"precondition of the Decision|precondition of the (human|Maintainer)",
    "lead plain, keep precision beneath":
        r"[Ll]ead plain.{0,60}precision",
    "an unmet understanding halts the Decision":
        r"mandatory pause|not decidable",
    "points at the rationale rather than restating it":
        r"doctrine/rationale\.md",
}


def _text(rel: str) -> str:
    return (CAIRN_ROOT / rel).read_text(encoding="utf-8")


@pytest.mark.parametrize("rel", _AGENTS_FILES)
@pytest.mark.parametrize("label,pattern", sorted(_REQUIRED.items()))
def test_comprehension_floor_obligation_present(rel: str, label: str,
                                                pattern: str) -> None:
    assert re.search(pattern, _text(rel)), (
        f"{rel} does not express the comprehension-floor obligation "
        f"{label!r}. The floor is stated in doctrine/rationale.md, which "
        f"adopters never receive; removing it here removes it for them."
    )


@pytest.mark.parametrize("rel", _AGENTS_FILES)
def test_comprehension_floor_sits_in_the_review_section(rel: str) -> None:
    """Placement is part of the rule: the floor is a property of review.

    A reader looking for review obligations must find it without already
    knowing it exists.
    """
    text = _text(rel)
    review = re.search(r"^## Review$(.*?)^## ", text, re.M | re.S)
    assert review, f"{rel} has no '## Review' section"
    assert re.search(r"mandatory pause|not decidable", review.group(1)), (
        f"{rel} states the comprehension floor outside its '## Review' "
        f"section; it is an obligation about review and belongs there."
    )
