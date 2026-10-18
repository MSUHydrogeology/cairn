"""The review and verification rules must reach the adopter, not only the doctrine.

`doctrine/` is **not installed into an adopter tree**, so a rule that lives
only there binds nobody who adopts Cairn. These rules therefore sit in
`templates/core/AGENTS.md`, the file every adopter receives and every agent
loads each session, and in Cairn's own root `AGENTS.md`, so that Cairn is bound
by the rules it ships.

The rules pinned here:

* **A review reads a commit, never a shared working tree.** In a working tree
  shared with an author, the reviewer's only write is its own review record;
  anything else that writes runs in a separate copy. A reverted, uncommitted
  file cannot be brought back with git, so this is the rule that prevents lost
  work.

Each obligation is an alternation matched against whitespace-collapsed text, so
a rewording that keeps the obligation passes and a deletion fails. Node IDs are
the obligation labels, never the patterns, so rewording a pattern does not
rename (and so drop) a collected test.

Run from the Cairn repo root:
    python -m pytest bootstrap/tests/test_review_and_verification_rules_ship.py
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent

#: The shipped copy is the load-bearing one: adopters receive it. Cairn's own
#: copy keeps Cairn bound by what it ships.
SHIPPED = "templates/core/AGENTS.md"
OWN = "AGENTS.md"
_AGENTS_FILES = (SHIPPED, OWN)
_FILE_IDS = {SHIPPED: "shipped", OWN: "own"}

#: label -> pattern. Every label must hold in both `AGENTS.md` copies.
_OBLIGATIONS = {
    # A review reads a commit, and writes only its own record in a shared tree.
    "review-reads-a-commit":
        r"[Aa] review reads a commit, (never|not) a shared working tree",
    "reviewer-writes-only-its-own-record":
        r"makes one write: its own review record",
    "no-reverting-commands-in-a-shared-tree":
        r"no `restore`, `checkout`, `stash`, `reset` or `clean`",
    "other-writes-go-to-a-separate-copy":
        r"separate copy of the reviewed commit",
    "figures-are-measured-on-the-commit":
        r"measured on (that|the reviewed) commit's bytes",
}


def _collapse(text: str) -> str:
    """Collapse whitespace runs so a pattern tests the rule, not the wrapping."""
    return " ".join(text.split())


def _text(rel: str) -> str:
    return (CAIRN_ROOT / rel).read_text(encoding="utf-8")


def _missing(text: str) -> list[str]:
    """Labels of the obligations absent from *text*."""
    collapsed = _collapse(text)
    return [label for label, pattern in _OBLIGATIONS.items()
            if not re.search(pattern, collapsed)]


@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_OBLIGATIONS))
def test_agents_md_carries_the_obligation(label: str, rel: str) -> None:
    assert label not in _missing(_text(rel)), (
        f"{rel} no longer carries the obligation {label!r}. The doctrine holds "
        f"the same rule, but adopters never receive doctrine/; removing it here "
        f"removes it for them."
    )


@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_OBLIGATIONS))
def test_removing_the_obligation_is_reported(label: str, rel: str) -> None:
    """The pin above can fail: strip every match and it must report the loss."""
    intact = _collapse(_text(rel))
    assert label not in _missing(intact)
    stripped = re.sub(_OBLIGATIONS[label], "", intact)
    assert label in _missing(stripped)


def test_an_empty_file_carries_no_obligation() -> None:
    """The floor: a guard that an empty file satisfies guards nothing."""
    assert sorted(_missing("")) == sorted(_OBLIGATIONS)


@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
def test_the_commit_rule_sits_in_the_review_section(rel: str) -> None:
    """Placement is part of the rule: it binds reviewers, so it lives in Review.

    A reader looking for what a review may do must find it there without
    already knowing it exists.
    """
    review = re.search(r"^## Review$(.*?)^## ", _text(rel), re.M | re.S)
    assert review, f"{rel} has no '## Review' section"
    assert re.search(_OBLIGATIONS["review-reads-a-commit"],
                     _collapse(review.group(1))), (
        f"{rel} states the review-reads-a-commit rule outside '## Review'."
    )


def test_the_shipped_copy_makes_claiming_conditional() -> None:
    """File claims ship only with an optional module.

    An adopter without it cannot claim a file, so an unconditional "claimed
    first" would be a rule every such reviewer breaks on first use.
    """
    assert re.search(r"claimed first if the project uses file claims",
                     _collapse(_text(SHIPPED)))


def test_cairns_own_copy_claims_unconditionally() -> None:
    """Cairn keeps a claim tool, so its own reviewers always claim first.

    Syncing the two copies could silently flip either one; each direction is
    pinned.
    """
    own = _collapse(_text(OWN))
    assert re.search(r"claimed first, and committed by explicit path", own)
    assert "if the project uses file claims" not in own
