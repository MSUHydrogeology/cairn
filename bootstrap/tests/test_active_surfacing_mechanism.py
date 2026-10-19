"""Tests for active-surfacing emission machinery.

Plan: 2026-05-28-claude-cairn-progressive-onboarding.

Covers the surfacing mechanism (NOT the per-preset content -- that
lives in test_active_surfacing_render.py):

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
    def test_surviving_prompt_is_selected(
        self, helper: ModuleType,
    ) -> None:
        """The remaining trigger still selects its active prompt."""
        chosen = helper.select_active_prompt_to_fire(
            {"second-agent-type"},
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
        assert helper.select_active_prompt_to_fire(
            {"second-agent-type"}, log_records=[],
        ) == "second-agent-type"
        log = [
            helper.ActivationRecord(
                "active-surface:second-agent-type",
                "2026-05-29T00:00:00Z", "agent-1", "solo-greenfield",
                "active-surface:second-agent-type",
            ),
        ]
        chosen = helper.select_active_prompt_to_fire(
            {"second-agent-type"},
            log_records=log,
        )
        assert chosen is None

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
        # Append two tasks so the two surviving trigger-gated tasks plus
        # these stand-ins exceed the three-task cap.
        source_path = (
            tmp_path / "dev" / "modules" / "onboarding"
            / "solo-greenfield.md"
        )
        source_path.write_text(
            source_path.read_text(encoding="utf-8")
            + "\n* [trigger: second-agent-type; id: extra-cap-test-task]\n"
              "  One extra deferred task.\n"
              "\n* [trigger: second-agent-type; id: another-cap-test-task]\n"
              "  Another extra deferred task.\n"
        )
        outcome = helper.activate(
            tmp_path,
            by_agent="claude-test",
            fired_triggers_override={
                "first-proposal-archived",
                "second-agent-type",
            },
        )
        assert len(outcome.pending) + len(outcome.deferred_over_cap) == 4
        assert len(outcome.pending) == helper.MAX_NEW_TASKS_PER_GOODNIGHT
        assert len(outcome.deferred_over_cap) == 1


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
                "second-agent-type",
            },
        )
        assert outcome.active_prompt_row == "second-agent-type"
        assert outcome.active_prompt_body is not None
        assert len(outcome.active_prompt_body) > 20

    def test_active_prompt_not_re_emitted_on_second_run(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """Re-running activate after the first emission does not
        re-fire the same prompt (idempotency via the log marker)."""
        assert _scaffold_solo(tmp_path) == 0
        first = helper.activate(
            tmp_path,
            by_agent="claude-test",
            fired_triggers_override={
                "first-proposal-archived",
                "second-agent-type",
            },
        )
        assert first.active_prompt_row == "second-agent-type"
        outcome_2 = helper.activate(
            tmp_path,
            by_agent="claude-test",
            fired_triggers_override={
                "first-proposal-archived",
                "second-agent-type",
            },
        )
        assert outcome_2.active_prompt_row is None
