"""Tests for active-surfacing emission machinery (Chunk P1.10a).

Plan: 2026-05-28-claude-cairn-progressive-onboarding.

Covers the surfacing mechanism (NOT the per-preset content -- that
lives in test_active_surfacing_render.py, P1.10b):

* Priority order: when multiple rows would fire, the helper
  selects the highest-priority unmuted one.
* UX cap (<=1 active prompt per goodnight): tested via the
  selector + the activate() outcome.
* UX cap (<=3 newly-inserted tasks per goodnight): tested via
  activate()'s `deferred_over_cap`.
* Overflow-defer: tasks beyond the cap re-emerge at the next
  goodnight (the held-task store + log work this naturally).
* Idempotency: an active prompt that has previously fired
  (`active-surface:<row>` recorded in the log) does NOT re-fire.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_active_surfacing_mechanism.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import main  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
HELPER_SRC = (
    CAIRN_ROOT
    / "templates"
    / "modules"
    / "default-on"
    / "onboarding_activate.py"
)

pytestmark = pytest.mark.skipif(
    not HELPER_SRC.exists(), reason="onboarding_activate.py source missing",
)


def _load_helper() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "_onboarding_activate_under_test_surfacing_mech", HELPER_SRC,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["_onboarding_activate_under_test_surfacing_mech"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def helper() -> ModuleType:
    return _load_helper()


def _scaffold_solo(target: Path) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: T\ntest_command: pytest\npreset: solo-greenfield\n"
    )
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT)]
    )


# ---------------------------------------------------------------------------
# Priority selection
# ---------------------------------------------------------------------------


class TestPriorityOrder:
    def test_collab_agreement_wins_over_level_graduation(
        self, helper: ModuleType,
    ) -> None:
        chosen = helper.select_active_prompt_to_fire(
            {"collab-agreement-signing", "level-1-to-2"},
            log_records=[],
        )
        assert chosen == "collab-agreement-signing"

    def test_level_graduation_wins_over_second_agent(
        self, helper: ModuleType,
    ) -> None:
        chosen = helper.select_active_prompt_to_fire(
            {"level-1-to-2", "second-agent-type"},
            log_records=[],
        )
        assert chosen == "Level-1-to-2-graduation"

    def test_second_agent_wins_over_foldback(
        self, helper: ModuleType,
    ) -> None:
        chosen = helper.select_active_prompt_to_fire(
            {"second-agent-type", "first-foldback-candidate"},
            log_records=[],
        )
        assert chosen == "second-agent-type"

    def test_no_triggers_returns_none(self, helper: ModuleType) -> None:
        chosen = helper.select_active_prompt_to_fire(set(), log_records=[])
        assert chosen is None

    def test_unmatched_trigger_returns_none(
        self, helper: ModuleType,
    ) -> None:
        chosen = helper.select_active_prompt_to_fire(
            {"first-proposal-archived"},  # not an active-surfacing trigger
            log_records=[],
        )
        assert chosen is None


# ---------------------------------------------------------------------------
# Idempotency: an emitted prompt does not re-fire
# ---------------------------------------------------------------------------


class TestIdempotency:
    def test_prior_emission_in_log_suppresses_re_fire(
        self, helper: ModuleType,
    ) -> None:
        log = [
            helper.ActivationRecord(
                "active-surface:collab-agreement-signing",
                "2026-05-29T00:00:00Z", "agent-1", "solo-greenfield",
                "active-surface:collab-agreement-signing",
            ),
        ]
        chosen = helper.select_active_prompt_to_fire(
            {"collab-agreement-signing", "level-1-to-2"},
            log_records=log,
        )
        # Collab-agreement was emitted before; Level 1->2 is next.
        assert chosen == "Level-1-to-2-graduation"

    def test_all_emitted_returns_none(self, helper: ModuleType) -> None:
        log = [
            helper.ActivationRecord(
                f"active-surface:{row}",
                "2026-05-29T00:00:00Z", "agent-1", "solo-greenfield",
                f"active-surface:{row}",
            )
            for row, _ in helper._ACTIVE_SURFACING_ROWS
        ]
        chosen = helper.select_active_prompt_to_fire(
            {row[1] for row in helper._ACTIVE_SURFACING_ROWS},
            log_records=log,
        )
        assert chosen is None


# ---------------------------------------------------------------------------
# UX cap on newly-inserted tasks per goodnight
# ---------------------------------------------------------------------------


class TestTaskCap:
    def test_max_three_tasks_per_goodnight(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """A goodnight whose evaluation produces > MAX
        eligible activations: activates only MAX; the
        overflow lands in `deferred_over_cap`."""
        assert _scaffold_solo(tmp_path) == 0
        # Solo-greenfield has 4 deferred tasks; fire all 4 triggers
        # at once.  The cap is 3; the 4th should defer.
        outcome = helper.activate(
            tmp_path,
            by_agent="claude-test",
            fired_triggers_override={
                "first-proposal-archived",
                "collab-agreement-signing",
                "second-agent-type",
                "first-foldback-candidate",
            },
        )
        assert len(outcome.pending) == helper.MAX_NEW_TASKS_PER_GOODNIGHT
        assert len(outcome.deferred_over_cap) == (
            4 - helper.MAX_NEW_TASKS_PER_GOODNIGHT
        )


# ---------------------------------------------------------------------------
# Active prompt emission via activate()
# ---------------------------------------------------------------------------


class TestActivatePromptEmission:
    def test_active_prompt_in_outcome(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """activate() returns active_prompt_row + active_prompt_body
        when an active trigger has fired."""
        assert _scaffold_solo(tmp_path) == 0
        outcome = helper.activate(
            tmp_path,
            by_agent="claude-test",
            fired_triggers_override={
                "first-proposal-archived",
                "collab-agreement-signing",
            },
        )
        assert outcome.active_prompt_row == "collab-agreement-signing"
        assert outcome.active_prompt_body is not None
        assert len(outcome.active_prompt_body) > 20

    def test_active_prompt_not_re_emitted_on_second_run(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """Re-running activate after the first emission does not
        re-fire the same prompt (idempotency via the log marker)."""
        assert _scaffold_solo(tmp_path) == 0
        helper.activate(
            tmp_path,
            by_agent="claude-test",
            fired_triggers_override={
                "first-proposal-archived",
                "collab-agreement-signing",
            },
        )
        outcome_2 = helper.activate(
            tmp_path,
            by_agent="claude-test",
            fired_triggers_override={
                "first-proposal-archived",
                "collab-agreement-signing",
            },
        )
        assert outcome_2.active_prompt_row is None
