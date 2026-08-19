"""Tests for derived held / completed task state.

Plan: 2026-05-28-claude-cairn-progressive-onboarding.

Per the Codex P2-5 disposition, held-tasks + completed-tasks are
**derived state** -- not persisted directly.  The activation log
(``dev/.cairn/onboarding-activated.jsonl``) is the only durable
state; "what's currently held" and "what's been completed" are
computed each goodnight from:

* the source-of-truth deferred-task list in the installed preset
  file (``dev/modules/onboarding/<preset>.md``),
* the activation log, and
* the current PLANNING slot body.

Covered:

* ``derive_held_task_ids``: source-file deferred ids minus
  log-recorded activation ids = the tasks awaiting their trigger.
* ``derive_completed_task_ids``: log-recorded activation ids whose
  body is no longer present in PLANNING's slot = the tasks the
  maintainer has marked done by removal (the standard
  ``doctrine/lifecycle.md`` "remove when complete" pattern).
* Derivation re-computes correctly across goodnight cycles
  (held → activated → completed).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_deferred_task_store.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

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
        "_onboarding_activate_under_test_deferred", HELPER_SRC,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["_onboarding_activate_under_test_deferred"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def helper() -> ModuleType:
    return _load_helper()


# ---------------------------------------------------------------------------
# Fixture source files used across the derivation tests
# ---------------------------------------------------------------------------

_PRESET_SOURCE_WITH_THREE_DEFERRED = """\
# Onboarding tasks -- test preset

* [seed; id: seed-alpha]
  Day-one task alpha body.

* [trigger: first-proposal-archived; id: deferred-beta]
  Body for deferred-beta.

* [trigger: second-agent-type; id: deferred-gamma]
  Body for deferred-gamma.

* [trigger: first-foldback-candidate; id: deferred-delta]
  Body for deferred-delta.
"""


# ---------------------------------------------------------------------------
# Held-task derivation
# ---------------------------------------------------------------------------


class TestHeldDerivation:
    def test_all_deferred_held_when_log_empty(
        self, helper: ModuleType,
    ) -> None:
        held = helper.derive_held_task_ids(
            _PRESET_SOURCE_WITH_THREE_DEFERRED, [],
        )
        assert set(held) == {
            "deferred-beta", "deferred-gamma", "deferred-delta",
        }

    def test_activated_id_drops_from_held(
        self, helper: ModuleType,
    ) -> None:
        rec = helper.ActivationRecord(
            "deferred-beta",
            "2026-05-29T00:00:00Z",
            "agent-1",
            "test-preset",
            "first-proposal-archived",
        )
        held = helper.derive_held_task_ids(
            _PRESET_SOURCE_WITH_THREE_DEFERRED, [rec],
        )
        assert "deferred-beta" not in held
        assert "deferred-gamma" in held
        assert "deferred-delta" in held

    def test_all_activated_means_no_held(
        self, helper: ModuleType,
    ) -> None:
        records = [
            helper.ActivationRecord(
                tid, "2026-05-29T00:00:00Z", "agent-1",
                "test-preset", trig,
            )
            for tid, trig in [
                ("deferred-beta", "first-proposal-archived"),
                ("deferred-gamma", "second-agent-type"),
                ("deferred-delta", "first-foldback-candidate"),
            ]
        ]
        assert helper.derive_held_task_ids(
            _PRESET_SOURCE_WITH_THREE_DEFERRED, records,
        ) == []


# ---------------------------------------------------------------------------
# Completed-task derivation (the PLANNING-removal pattern)
# ---------------------------------------------------------------------------


class TestCompletedDerivation:
    def test_log_entry_in_planning_is_not_completed(
        self, helper: ModuleType,
    ) -> None:
        """A log-recorded activation whose body still appears in
        PLANNING is in-flight, not completed."""
        rec = helper.ActivationRecord(
            "deferred-beta", "2026-05-29T00:00:00Z", "agent-1",
            "test-preset", "first-proposal-archived",
        )
        planning_slot_body = (
            "<!-- preset: test-preset -->\n"
            "\n"
            "* [seed; id: seed-alpha]\n"
            "* [trigger: first-proposal-archived; id: deferred-beta]\n"
            "  Body still in planning.\n"
        )
        completed = helper.derive_completed_task_ids(
            [rec], planning_slot_body,
        )
        assert completed == []

    def test_log_entry_absent_from_planning_is_completed(
        self, helper: ModuleType,
    ) -> None:
        """A log-recorded activation whose body is GONE from PLANNING
        (maintainer removed it after completing the task) shows up
        as completed."""
        rec = helper.ActivationRecord(
            "deferred-beta", "2026-05-29T00:00:00Z", "agent-1",
            "test-preset", "first-proposal-archived",
        )
        planning_slot_body = (
            "<!-- preset: test-preset -->\n"
            "\n"
            "* [seed; id: seed-alpha]\n"  # no `id: deferred-beta` anymore
        )
        completed = helper.derive_completed_task_ids(
            [rec], planning_slot_body,
        )
        assert completed == ["deferred-beta"]


# ---------------------------------------------------------------------------
# Lifecycle: held -> activated -> completed across two goodnight cycles
# ---------------------------------------------------------------------------


class TestLifecycleAcrossCycles:
    def test_held_then_activated_then_completed(
        self, helper: ModuleType,
    ) -> None:
        # Initial state: empty log, no PLANNING activations.
        held_1 = helper.derive_held_task_ids(
            _PRESET_SOURCE_WITH_THREE_DEFERRED, [],
        )
        assert set(held_1) == {
            "deferred-beta", "deferred-gamma", "deferred-delta",
        }
        # Cycle 1: deferred-beta activates.
        rec_beta = helper.ActivationRecord(
            "deferred-beta", "2026-05-29T00:00:00Z", "agent-1",
            "test-preset", "first-proposal-archived",
        )
        held_2 = helper.derive_held_task_ids(
            _PRESET_SOURCE_WITH_THREE_DEFERRED, [rec_beta],
        )
        assert "deferred-beta" not in held_2
        # deferred-beta still in PLANNING -> not completed yet.
        planning_with_beta = (
            "* [trigger: first-proposal-archived; id: deferred-beta]\n"
            "  body\n"
        )
        assert helper.derive_completed_task_ids(
            [rec_beta], planning_with_beta,
        ) == []
        # Cycle 2: maintainer removes deferred-beta from PLANNING
        # (the task is done; the doctrine.lifecycle removal pattern).
        planning_without_beta = "* [seed; id: seed-alpha]\n"
        assert helper.derive_completed_task_ids(
            [rec_beta], planning_without_beta,
        ) == ["deferred-beta"]
