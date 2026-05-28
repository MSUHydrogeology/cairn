"""Tests for the maturity-ladder trigger evaluators (Chunk P1.9a).

Plan: 2026-05-28-claude-cairn-progressive-onboarding.

Each maturity-ladder trigger gets positive + negative fixture
tests against synthetic adopter-tree state.  The four triggers:

* ``level-0-to-1`` -- ``dev/proposals/_template.md`` exists.
* ``level-1-to-2`` -- ``dev/cairn-lock.yml`` exists.
* ``level-1-deepen`` -- archived-proposal + archived-plan count
  thresholds met AND ``level-1-to-2`` NOT yet fired.
* ``level-2-deepen`` -- archived-proposal + archived-plan count
  thresholds met AND ``level-1-to-2`` IS fired.

Mixed-state fixtures verify multiple triggers can fire together
(e.g., level-0-to-1 AND level-1-to-2 both present).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_trigger_evaluation_maturity.py
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
        "_onboarding_activate_under_test_maturity", HELPER_SRC,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["_onboarding_activate_under_test_maturity"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def helper() -> ModuleType:
    return _load_helper()


def _make_empty_tree(tmp_path: Path) -> Path:
    """Create an empty `dev/` subtree without _template.md or
    cairn-lock.yml (Level 0 baseline)."""
    (tmp_path / "dev" / "proposals" / "archive").mkdir(parents=True)
    (tmp_path / "dev" / "plans" / "archive").mkdir(parents=True)
    return tmp_path


def _archive_proposals(tmp_path: Path, count: int) -> None:
    archive = tmp_path / "dev" / "proposals" / "archive"
    archive.mkdir(parents=True, exist_ok=True)
    for i in range(count):
        (archive / f"2026-05-{i:02d}-author-slug.md").write_text("# x\n")


def _archive_plans(tmp_path: Path, count: int) -> None:
    archive = tmp_path / "dev" / "plans" / "archive"
    archive.mkdir(parents=True, exist_ok=True)
    for i in range(count):
        (archive / f"2026-05-{i:02d}-author-slug.md").write_text("# x\n")


# ---------------------------------------------------------------------------
# level-0-to-1
# ---------------------------------------------------------------------------


class TestLevel0to1:
    def test_fires_when_proposals_template_present(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _make_empty_tree(tmp_path)
        (tmp_path / "dev" / "proposals" / "_template.md").write_text("# t\n")
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert "level-0-to-1" in fired

    def test_does_not_fire_without_proposals_template(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _make_empty_tree(tmp_path)
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert "level-0-to-1" not in fired


# ---------------------------------------------------------------------------
# level-1-to-2
# ---------------------------------------------------------------------------


class TestLevel1to2:
    def test_fires_when_lockfile_present(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _make_empty_tree(tmp_path)
        (tmp_path / "dev" / "cairn-lock.yml").write_text("schema: 1\n")
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert "level-1-to-2" in fired

    def test_does_not_fire_without_lockfile(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _make_empty_tree(tmp_path)
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert "level-1-to-2" not in fired


# ---------------------------------------------------------------------------
# level-1-deepen
# ---------------------------------------------------------------------------


class TestLevel1Deepen:
    def test_fires_at_threshold_without_level_2(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _make_empty_tree(tmp_path)
        _archive_proposals(
            tmp_path, helper.LEVEL_1_DEEPEN_PROPOSALS_THRESHOLD,
        )
        _archive_plans(tmp_path, helper.LEVEL_1_DEEPEN_PLANS_THRESHOLD)
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert "level-1-deepen" in fired

    def test_suppressed_when_level_2_also_fires(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _make_empty_tree(tmp_path)
        (tmp_path / "dev" / "cairn-lock.yml").write_text("schema: 1\n")
        _archive_proposals(
            tmp_path, helper.LEVEL_1_DEEPEN_PROPOSALS_THRESHOLD,
        )
        _archive_plans(tmp_path, helper.LEVEL_1_DEEPEN_PLANS_THRESHOLD)
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert "level-1-deepen" not in fired
        assert "level-1-to-2" in fired

    def test_does_not_fire_below_threshold(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _make_empty_tree(tmp_path)
        _archive_proposals(
            tmp_path, helper.LEVEL_1_DEEPEN_PROPOSALS_THRESHOLD - 1,
        )
        _archive_plans(tmp_path, helper.LEVEL_1_DEEPEN_PLANS_THRESHOLD - 1)
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert "level-1-deepen" not in fired


# ---------------------------------------------------------------------------
# level-2-deepen
# ---------------------------------------------------------------------------


class TestLevel2Deepen:
    def test_fires_when_level_2_and_high_thresholds_met(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _make_empty_tree(tmp_path)
        (tmp_path / "dev" / "cairn-lock.yml").write_text("schema: 1\n")
        _archive_proposals(
            tmp_path, helper.LEVEL_2_DEEPEN_PROPOSALS_THRESHOLD,
        )
        _archive_plans(tmp_path, helper.LEVEL_2_DEEPEN_PLANS_THRESHOLD)
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert "level-2-deepen" in fired

    def test_does_not_fire_below_level_2(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _make_empty_tree(tmp_path)
        # No lockfile -> level-1-to-2 not fired -> level-2-deepen suppressed.
        _archive_proposals(
            tmp_path, helper.LEVEL_2_DEEPEN_PROPOSALS_THRESHOLD,
        )
        _archive_plans(tmp_path, helper.LEVEL_2_DEEPEN_PLANS_THRESHOLD)
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert "level-2-deepen" not in fired

    def test_does_not_fire_below_high_threshold(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _make_empty_tree(tmp_path)
        (tmp_path / "dev" / "cairn-lock.yml").write_text("schema: 1\n")
        # Only Level 1 deepen threshold met; not Level 2 deepen.
        _archive_proposals(
            tmp_path, helper.LEVEL_1_DEEPEN_PROPOSALS_THRESHOLD,
        )
        _archive_plans(tmp_path, helper.LEVEL_1_DEEPEN_PLANS_THRESHOLD)
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert "level-2-deepen" not in fired


# ---------------------------------------------------------------------------
# Mixed-state fixture: full Level 1 install with deepen threshold met
# ---------------------------------------------------------------------------


class TestMixedFixture:
    def test_level_1_install_with_deepen_threshold_fires_two(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """An adopter at full Level 1 (template + deepen threshold)
        fires both level-0-to-1 + level-1-deepen, NOT level-1-to-2
        (no lockfile yet) and NOT level-2-deepen."""
        _make_empty_tree(tmp_path)
        (tmp_path / "dev" / "proposals" / "_template.md").write_text("# t\n")
        _archive_proposals(
            tmp_path, helper.LEVEL_1_DEEPEN_PROPOSALS_THRESHOLD,
        )
        _archive_plans(tmp_path, helper.LEVEL_1_DEEPEN_PLANS_THRESHOLD)
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert fired == {"level-0-to-1", "level-1-deepen"}

    def test_template_does_not_count_as_archived_proposal(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """The proposals/_template.md placed in archive (an edge case
        if an adopter mistakenly archives the template) does not
        count toward the deepen threshold."""
        _make_empty_tree(tmp_path)
        (
            tmp_path / "dev" / "proposals" / "archive" / "_template.md"
        ).write_text("# t\n")
        fired = helper.evaluate_maturity_triggers(tmp_path)
        assert "level-1-deepen" not in fired
