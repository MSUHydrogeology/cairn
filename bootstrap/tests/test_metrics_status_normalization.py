"""The metrics status normalizer must keep resolving PRE-MIGRATION history.

Chunk H1 of ``review-efficient-lifecycle`` retired six lifecycle status tokens,
moving them out of ``PLAN_STATES`` / ``PROPOSAL_STATES`` and into the historical
tuples. R7 is explicit that this must not stop longitudinal metrics parsing the
commits that predate the migration, and this file is the guard on that clause.

**Why it exists at all: the regression it prevents is silent.**
``_normalize_plan_status`` resolves a free-text status by the FIRST enum whose
value the leading token *starts with*. When ``_plan_status_enum()`` returned
``PLAN_STATES`` alone, retiring ``review`` changed exactly one class of input:

    'reviewed; awaiting code review'   ->  'review'   became   'reviewed'

Every *exact* token (``review``, ``executing``, ``open``) is unaffected, because
the no-match fall-through returns the lead token unchanged -- which is the same
string. Only the **prefix** case moves, and it moves quietly: it splits one
longitudinal bucket into two while every existing test stays green. At the time
H1 landed, **no test in the suite referenced ``_normalize_plan_status`` or
``_plan_status_enum`` at all**, so the whole defect class was unobserved. That is
the "silent tool defect" ``AGENTS.md`` > *Verifying claims* forbids: a tool that
returns success without testing the claimed property.

This is a NEW test file (``FROZEN-NEW`` to the gate manifest, node-IDs
``COLLECTION-ADDED``), so it adds coverage without forcing a gate re-anchor.
"""
from __future__ import annotations

import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent


def _load_extract() -> ModuleType:
    """Load the repo-side metrics extractor.

    Deliberately the ``tools/`` copy rather than the shipped template: the
    contained loader resolves the vocabulary from a *sibling* planner, which
    exists under ``tools/`` and (by design) does not at the template source
    location. Twin parity between the two copies is asserted elsewhere.
    """
    tools = str(CAIRN_ROOT / "tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    from _lifecycle_metrics import extract  # noqa: PLC0415

    return extract


_extract = _load_extract()


class TestHistoricalTokensStayResolvable:
    """The retired tokens must remain in the enum metrics resolves against."""

    def test_the_enum_carries_both_the_current_and_the_historical_states(self):
        vocab = _extract._vocabulary()
        enum = _extract._plan_status_enum()
        for state in vocab.PLAN_STATES:
            assert state in enum, f"current state {state!r} missing from the enum"
        for state in vocab.HISTORICAL_PLAN_STATES:
            assert state in enum, (
                f"historical state {state!r} missing from the enum -- metrics can "
                "no longer parse pre-migration history, which R7 forbids"
            )

    def test_the_historical_group_comes_last_because_order_is_load_bearing(self):
        """Prefix resolution means a current token must win over a historical one.

        Not a style assertion: ``_normalize_plan_status`` returns the FIRST enum
        the lead token starts with, so ordering decides the answer whenever one
        token is a prefix of another.
        """
        vocab = _extract._vocabulary()
        enum = list(_extract._plan_status_enum())
        first_historical = min(
            enum.index(s) for s in vocab.HISTORICAL_PLAN_STATES
        )
        last_current = max(enum.index(s) for s in vocab.PLAN_STATES)
        assert last_current < first_historical, (
            "every current state must precede every historical one in the enum"
        )

    def test_no_current_token_is_a_prefix_of_a_historical_one_or_vice_versa(self):
        """The collision the ordering rule above would otherwise have to arbitrate."""
        vocab = _extract._vocabulary()
        for cur in vocab.PLAN_STATES:
            for hist in vocab.HISTORICAL_PLAN_STATES:
                assert not cur.startswith(hist), (cur, hist)
                assert not hist.startswith(cur), (hist, cur)


class TestNormalizationIsStableAcrossTheMigration:
    """The exact inputs whose resolution H1 could have changed."""

    @pytest.mark.parametrize(
        "raw,expected",
        [
            # THE regression case: a longer lead token resolving to a shorter
            # historical enum member by prefix. This is the only class that moves.
            ("reviewed; awaiting code review", "review"),
            ("reviewed", "review"),
            # Exact historical tokens -- stable either way, recorded so a future
            # reader can see which cases prove nothing on their own.
            ("review", "review"),
            ("executing", "executing"),
            ("open", "open"),
            # Trailing prose after a historical token.
            ("executing (chunk C)", "executing"),
            ("open -- since 2026-05-14", "open"),
            # Current vocabulary, unaffected.
            ("implementing", "implementing"),
            ("archived 2026-05-14 (superseded by x)", "archived"),
            ("awaiting-code-review", "awaiting-code-review"),
        ],
    )
    def test_a_free_text_status_resolves_to_its_enum_token(self, raw, expected):
        assert _extract._normalize_plan_status(raw) == expected

    def test_an_unknown_token_falls_through_to_the_raw_lead(self):
        """Fail-open is correct here: metrics describe history, they do not gate."""
        assert _extract._normalize_plan_status("not-a-state extra") == "not-a-state"

    def test_an_empty_status_is_empty_rather_than_a_neighbouring_token(self):
        assert _extract._normalize_plan_status("") == ""
        assert _extract._normalize_plan_status("   ") == ""


class TestTheGuardCanActuallyFail:
    """A test that cannot observe the defect is not a guard.

    Reproduces the exact pre-fix condition -- resolving against the current
    states alone -- and asserts it produces the wrong answer. If this ever stops
    failing, the defect class has changed shape and the parametrized cases above
    are no longer pinning what they claim to pin.
    """

    def test_dropping_the_historical_half_reintroduces_the_regression(self):
        vocab = _extract._vocabulary()
        current_only = tuple(vocab.PLAN_STATES)

        def normalize_against(value: str, enum) -> str:
            tokens = value.split()
            if not tokens:
                return ""
            lead = tokens[0].strip(" .,;:*").lower()
            for candidate in enum:
                if lead.startswith(candidate):
                    return candidate
            return lead

        assert normalize_against("reviewed; awaiting code review", current_only) == (
            "reviewed"
        ), "the pre-fix behaviour is no longer reproducible; re-derive this guard"
        assert (
            _extract._normalize_plan_status("reviewed; awaiting code review")
            == "review"
        )
