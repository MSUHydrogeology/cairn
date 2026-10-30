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
* Shared-file commits are serialized before inspection. Tracked candidates are
  compared with `HEAD` including staged and unstaged bytes; changed bytes are
  reinspected, and foreign or uncertain content stops the commit.
* **A claim that a value reaches every member of a set is settled by
  mutation.** The missing member is a line that is not there, so reading a
  diff cannot see it. The ledger reports every mutant against an unmutated
  control, and an equivalence nobody measured counts as a survivor. Two
  clauses carry that meaning and are pinned for what they say, not only that
  they exist: the trigger is a claim about a set (not any defect), and an
  equivalent mutant is one a behaviour test *passes* under (a test that fails
  has killed it).
* **Boundary B governs a trivial change too.** Search for its owning tests
  and readers, then run those checks on the exact candidate bytes before
  commit, in an otherwise clean tree or separate copy. Its commit body records
  the mode, pending tree certification, search, commands, counts, interpreter,
  outcomes and omissions; the author owns the record and there is no Boundary
  C. A passing record may say `Implementation verified at <SHA>`; a known
  missing consumer, security check, or criterion keeps the work open. For
  planned work, Boundary B is `bounded` for mapped affected behavior and
  consumers, or `wide` for owning families, known integration and public paths,
  and standing gates when effects cannot be confidently bounded. Use `wide`
  for a contract or trust-ceremony surface. A full-tree certification is a
  separate authorized integration run and cannot close a missing change check.
* **"Substantive surface" is defined once.** It is anything that is not
  ordinary prose, and that includes prose a test or manifest pins. A narrower
  "code" reading misses exactly the template rewrite whose pinned prose broke
  tests its author never ran.
* **Code review is not External by default.** More distance on a review is
  the Maintainer's call on one named artifact, never a default and never
  something an agent applies. The usual procedure may be reworded, so this is
  pinned as an absence: the claim must not come back in either copy, in any
  capitalisation or line wrapping.

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
    "shared-paths-are-serialized-through-commit":
        r"agree with other writers to serialize those paths through the commit; a work claim alone is not agreement",
    "candidate-inspection-includes-staged-and-unstaged-bytes":
        r"Compare each tracked candidate with `HEAD`, including both staged and unstaged bytes",
    "changed-bytes-are-reinspected":
        r"Reinspect any bytes that change before the commit",
    "foreign-or-uncertain-content-stops-commit":
        r"Stop and coordinate if a candidate contains foreign or uncertain content",
    "failed-serialization-uses-separate-worktrees":
        r"use separate worktrees and integrate each author's commit",
    "noncooperating-writer-limit-is-explicit":
        r"noncooperating writer can still change a file after inspection and defeat this procedure",
    "no-reverting-commands-in-a-shared-tree":
        r"no `restore`, `checkout`, `stash`, `reset` or `clean`",
    "other-writes-go-to-a-separate-copy":
        r"separate copy of the reviewed commit",
    "figures-are-measured-on-the-commit":
        r"measured on (that|the reviewed) commit's bytes",
    # A set claim is settled by mutating every member, and reported in full.
    "set-claims-are-listed-from-the-tree-and-mutated":
        r"list the set from the tree, not the diff, and mutate each member",
    "ledger-reports-each-mutant-against-a-control":
        r"killed, survived,? or equivalent, beside an unmutated control",
    "ledger-never-reports-a-bare-count":
        r"never as a bare \"?N of M",
    "equivalence-is-measured-not-argued":
        r"[Ee]quivalence is measured, not argued",
    "a-set-claim-is-the-mutation-trigger":
        r"When a finding or claim says a value must reach every member of a set",
    "an-equivalent-mutant-passes-the-behaviour-test":
        r"through the real entry point passes under the mutation",
    "unmeasured-equivalence-is-a-survivor":
        r"(not|never) measured is reported as a survivor",
    "mutation-is-otherwise-the-reviewers-choice":
        r"mutation stays the reviewer's choice",
    # Boundary B reaches a trivial change, and its fence is defined in place.
    "boundary-b-governs-a-trivial-change":
        r"[Bb]oundary B governs every implementation, a trivial change included",
    "a-trivial-change-maps-to-the-tests-that-own-its-surface":
        r"for a trivial change, with no proposal or plan, "
        r"the tests that own each touched surface",
    "bounded-mode-covers-affected-behavior-and-consumers":
        r"`?bounded`? covers the mapped affected behavior and consumers",
    "wide-mode-covers-known-families-and-public-paths":
        r"`?wide`? covers the owning test families, known cross-surface integration and public paths",
    "contract-and-trust-surfaces-use-wide-mode":
        r"Use `?wide`? for a contract or trust-ceremony surface",
    "unpinned-prose-on-a-high-risk-surface-runs-the-prose-gates":
        r"prose change to a contract or high-risk surface does not trigger "
        r"the full suite unless a test or manifest pins its bytes",
    "a-trivial-change-runs-on-exact-candidate-bytes":
        r"run those checks on the exact candidate bytes before commit",
    "a-trivial-change-records-the-search-and-checks-in-its-commit-body":
        r"commit body records the mode,.*search, commands, counts, interpreter",
    "passing-known-checks-identifies-the-verified-commit":
        r"Implementation verified at <SHA>",
    "a-plan-appends-its-verification-section":
        r"[Aa] plan appends the tested SHA",
    "owning-tests-are-found-by-search":
        r"found by searching for what imports or reads the touched files",
    "bounded-record-names-touched-surfaces-and-tests":
        r"[Rr]ecord names the touched surfaces, the test files or nodes",
    "trust-ceremony-surface-is-defined":
        r"trust-ceremony surface is any high-risk surface this file names",
    # One term, defined where it is used.
    "substantive-surface-is-defined":
        r"substantive surface\*{0,2} is anything that is not ordinary prose",
    "pinned-prose-is-substantive":
        r"and prose a test or manifest pins",
}

#: label -> pattern that must NOT occur in either copy. Matched against
#: whitespace-collapsed text, ignoring case: a sentence that restores a claim
#: at the start of a line or in capitals is still the claim.
_FORBIDDEN = {
    "no-full-run-tied-to-a-reviewed-mapping": r"no reviewed\s+mapping",
    "bounding-is-not-tied-to-a-plans-reviewed-mapping":
        r"plan's reviewed\s+mapping bounds",
    "code-review-is-not-external-by-default": r"external[- ]by[- ]default",
}

#: label -> the old wording each forbidden pattern exists to keep out.
_FORBIDDEN_EXAMPLES = {
    "no-full-run-tied-to-a-reviewed-mapping":
        "If a substantive surface has no reviewed mapping, run the full suite.",
    "bounding-is-not-tied-to-a-plans-reviewed-mapping":
        "Run the full suite unless the plan's reviewed mapping bounds the "
        "change's effects confidently.",
    "code-review-is-not-external-by-default":
        "Code review is External by default.",
}

#: label -> why the phrasing is wrong, shown when it comes back.
_FORBIDDEN_REASONS = {
    "no-full-run-tied-to-a-reviewed-mapping": (
        "ties the full-suite fallback to a reviewed mapping again. A trivial "
        "change has no reviewed mapping before it lands, so read literally "
        "this sends every small fix to the full suite."),
    "bounding-is-not-tied-to-a-plans-reviewed-mapping": (
        "makes bounded mode depend on a plan's reviewed mapping again. A "
        "trivial change has no plan, so it could never qualify and every "
        "small fix would run the full suite."),
    "code-review-is-not-external-by-default": (
        "says code review is External by default again. More distance on a "
        "review is the Maintainer's call on one named artifact, not a default "
        "an agent applies; as the default it adds a pass to every plan."),
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


def _present_forbidden(text: str) -> list[str]:
    """Labels of the forbidden phrasings present in *text*."""
    collapsed = _collapse(text)
    return [label for label, pattern in _FORBIDDEN.items()
            if re.search(pattern, collapsed, re.IGNORECASE)]


@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_FORBIDDEN))
def test_agents_md_omits_the_forbidden_phrasing(label: str, rel: str) -> None:
    assert label not in _present_forbidden(_text(rel)), (
        f"{rel} {_FORBIDDEN_REASONS[label]}"
    )


def test_forbidden_patterns_recognize_their_examples() -> None:
    """One example per pattern; the real-file pins separately cover both copies."""
    intact = _collapse(_text(SHIPPED))
    assert _present_forbidden(intact) == []
    for label, example in _FORBIDDEN_EXAMPLES.items():
        assert label in _present_forbidden(f"{intact} {example}"), label


@pytest.mark.parametrize("variant", [
    "Code review is External by default.",
    "code review is EXTERNAL BY DEFAULT.",
    "Code review is External\n  by   default.",
    "Code review is External-by-default.",
], ids=["plain", "capitals", "wrapped", "hyphenated"])
def test_the_external_by_default_pin_ignores_case_and_wrapping(variant: str) -> None:
    """The pin guards the claim, not one spelling of it.

    A sync from an older copy brings the sentence back as it was, but a
    reflow or a capital letter must not hide it from the check.
    """
    assert "code-review-is-not-external-by-default" in _present_forbidden(variant)


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


def test_coordination_doctrine_guards_same_file_commits() -> None:
    """Named paths still need agreement and inspection of all candidate bytes."""
    text = _collapse(_text("doctrine/coordination.md"))
    for phrase in (
        "agree with the other writers to serialize them through the commit",
        "including staged and unstaged changes",
        "inspect new files directly",
        "Reinspect bytes that change before committing",
        "Stop and coordinate if content is foreign or uncertain",
        "use separate worktrees and integrate each author's commit",
        "A noncooperating writer can still change a file after inspection",
    ):
        assert phrase in text
