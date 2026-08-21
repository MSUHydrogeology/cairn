"""Fixtures for the `cairn-event-v1` grammar / history-diff / reconciliation
machinery (`metrics-events-not-prose` Parts 3, Chunks 4-7).

Loaded through the installed launcher facade
(`templates/modules/default-on/lifecycle_metrics.py`), the same surface an
adopter imports -- consistent with the other `bootstrap/tests/test_lifecycle_*`
files. This is a NEW test file (recorded as FROZEN-NEW by the gate manifest;
its node-IDs as COLLECTION-ADDED), so it adds coverage without a gate
re-anchor.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import List, Tuple

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
_LM_PATH = CAIRN_ROOT / "templates" / "modules" / "default-on" / "lifecycle_metrics.py"


def _load_lm() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cairn_lm_events", _LM_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["cairn_lm_events"] = module
    spec.loader.exec_module(module)
    return module


_lm = _load_lm()
events = _lm.events

_PROPOSAL_STATES = (
    "awaiting-review", "revising", "awaiting-decision",
    "accepted", "rejected", "superseded",
)
_PLAN_STATES = (
    "awaiting-plan-review", "revising-plan", "ready-to-implement",
    "implementing", "awaiting-code-review", "revising-code",
    "ready-to-archive", "archived",
)


# ---------------------------------------------------------------------------
# Chunk 4 -- grammar fixtures (pure, no git)
# ---------------------------------------------------------------------------


def _fence(kind: str, **fields: str) -> str:
    lines = ["<!-- cairn-event-v1", f"kind: {kind}"]
    lines.extend(f"{k}: {v}" for k, v in fields.items())
    lines.append("-->")
    return "\n".join(lines) + "\n"


def test_no_fence_at_all_returns_empty_list() -> None:
    """A document with no event fence at all is not an error -- nothing
    is wrong with a tree that has not yet recorded any events."""
    assert events.parse_event_blocks(
        "just ordinary proposal prose, no fence here\n",
        valid_states=_PROPOSAL_STATES,
    ) == []


def test_three_worked_examples_parse_cleanly() -> None:
    """The three block shapes reproduced verbatim from Round 7 §1.  The
    transition example's ``reviewed``/``revised`` tokens are the
    pre-vocabulary-migration HISTORICAL states (an archived artifact may
    still declare them; `_plan_status_enum()`/`_proposal_status_enum()`
    resolve current + historical together) -- included here alongside a
    current token so the fixture is not silently narrowed to the
    current-only vocabulary."""
    historical_and_current = _PLAN_STATES + ("proposed", "reviewed", "revised")
    transition = _fence("transition", from_state="reviewed", to_state="revised")
    review_pass = _fence(
        "review-pass", tier="External",
        reviewer="<reviewer name as written in the section heading>",
    )
    response = _fence(
        "response",
        model="<model identity as written in the Response's Model field>",
    )
    b1 = events.parse_event_blocks(transition, valid_states=historical_and_current)
    assert len(b1) == 1 and b1[0].kind == "transition"
    assert b1[0].from_state == "reviewed" and b1[0].to_state == "revised"

    b2 = events.parse_event_blocks(review_pass, valid_states=_PROPOSAL_STATES)
    assert len(b2) == 1 and b2[0].kind == "review-pass"
    assert b2[0].tier == "External"

    b3 = events.parse_event_blocks(response, valid_states=_PROPOSAL_STATES)
    assert len(b3) == 1 and b3[0].kind == "response"


def test_unknown_version_token_refuses() -> None:
    text = _fence("transition", from_state="revising", to_state="accepted").replace(
        "cairn-event-v1", "cairn-event-v2"
    )
    with pytest.raises(events.EventGrammarError, match="unknown event version"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_unknown_kind_refuses() -> None:
    text = "<!-- cairn-event-v1\nkind: bogus\n-->\n"
    with pytest.raises(events.EventGrammarError, match="unknown event kind"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_missing_required_key_per_kind_refuses() -> None:
    cases = [
        "<!-- cairn-event-v1\nkind: transition\nfrom_state: revising\n-->\n",
        "<!-- cairn-event-v1\nkind: review-pass\ntier: External\n-->\n",
        "<!-- cairn-event-v1\nkind: response\n-->\n",
    ]
    for text in cases:
        with pytest.raises(events.EventGrammarError, match="missing required"):
            events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_unknown_key_refuses() -> None:
    text = _fence(
        "transition", from_state="revising", to_state="accepted", bogus="x",
    )
    with pytest.raises(events.EventGrammarError, match="unknown key"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_reviewer_and_model_over_120_chars_refuses() -> None:
    long_value = "x" * 121
    reviewer_text = _fence("review-pass", tier="External", reviewer=long_value)
    with pytest.raises(events.EventGrammarError, match="exceeds 120"):
        events.parse_event_blocks(reviewer_text, valid_states=_PROPOSAL_STATES)

    model_text = _fence("response", model=long_value)
    with pytest.raises(events.EventGrammarError, match="exceeds 120"):
        events.parse_event_blocks(model_text, valid_states=_PROPOSAL_STATES)


def test_recorded_by_is_optional_and_informational() -> None:
    text = _fence(
        "transition", from_state="revising", to_state="accepted",
        recorded_by="Someone",
    )
    blocks = events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)
    assert blocks[0].recorded_by == "Someone"


def test_malformed_field_line_refuses() -> None:
    text = "<!-- cairn-event-v1\nkind transition\n-->\n"
    with pytest.raises(events.EventGrammarError, match="malformed event field"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_duplicate_key_refuses() -> None:
    text = (
        "<!-- cairn-event-v1\nkind: transition\nfrom_state: revising\n"
        "from_state: accepted\nto_state: accepted\n-->\n"
    )
    with pytest.raises(events.EventGrammarError, match="duplicate event key"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_from_state_outside_valid_states_refuses() -> None:
    """Row 4-13: a `from_state`/`to_state` value outside the supplied
    `valid_states` refuses, using a small literal test vocabulary --
    this chunk's own fixtures stay pure-function and need no planner on
    disk (the integration-level fixture against the real loader is
    Chunk 6's row 6-3/6-4)."""
    text = _fence("transition", from_state="revising", to_state="nonexistent-state")
    with pytest.raises(events.EventGrammarError, match="not a declared lifecycle status"):
        events.parse_event_blocks(text, valid_states=("revising", "accepted"))


def test_bad_tier_refuses() -> None:
    text = _fence("review-pass", tier="Bogus", reviewer="Bob")
    with pytest.raises(events.EventGrammarError, match="tier"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)
