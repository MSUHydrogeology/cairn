"""Tests for action triggers over explicit project state.

The roster reader must use the roles document and refuse linked paths before
reading; the removed signing trigger must not return.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_trigger_evaluation_action.py
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
        "_onboarding_activate_under_test_action", HELPER_SRC,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["_onboarding_activate_under_test_action"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def helper() -> ModuleType:
    return _load_helper()


def _empty_dev_tree(tmp_path: Path) -> Path:
    (tmp_path / "dev" / "proposals" / "archive").mkdir(parents=True)
    (tmp_path / "dev" / "plans" / "archive").mkdir(parents=True)
    return tmp_path


def _write_template_files(tmp_path: Path) -> None:
    """Write minimal `_template.md` placeholders in proposals + plans
    (so non-template-glob filtering can be exercised)."""
    (tmp_path / "dev" / "proposals" / "_template.md").write_text("# t\n")
    (tmp_path / "dev" / "plans" / "_template.md").write_text("# t\n")


def _write_team_roster(
    tmp_path: Path, roster_body: str,
) -> None:
    roles = tmp_path / "dev" / "agent_collaboration.md"
    roles.write_text(
        "# Agent collaboration\n"
        "\n"
        "<!-- cairn:slot team-roster -->\n"
        f"{roster_body}\n"
        "<!-- cairn:end team-roster -->\n"
    )


# ---------------------------------------------------------------------------
# first-proposal-opened / first-proposal-archived
# ---------------------------------------------------------------------------


class TestProposalTriggers:
    def test_first_proposal_opened_positive(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        (tmp_path / "dev" / "proposals" / "2026-05-29-x.md").write_text("# p\n")
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-proposal-opened" in fired

    def test_first_proposal_opened_negative_only_template(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        _write_template_files(tmp_path)
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-proposal-opened" not in fired

    def test_first_proposal_archived_positive(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        (tmp_path / "dev" / "proposals" / "archive" / "x.md").write_text("#\n")
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-proposal-archived" in fired


# ---------------------------------------------------------------------------
# first-plan-opened / first-plan-archived
# ---------------------------------------------------------------------------


class TestPlanTriggers:
    def test_first_plan_opened_positive(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        (tmp_path / "dev" / "plans" / "2026-05-29-x.md").write_text("# p\n")
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-plan-opened" in fired

    def test_first_plan_archived_positive(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        (tmp_path / "dev" / "plans" / "archive" / "x.md").write_text("#\n")
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-plan-archived" in fired


# ---------------------------------------------------------------------------
# first-changelog-entry
# ---------------------------------------------------------------------------


class TestChangelogTrigger:
    def test_unreleased_with_content_fires(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        (tmp_path / "CHANGELOG.md").write_text(
            "# Changelog\n\n"
            "## [Unreleased]\n\n"
            "* Added a thing.\n\n"
            "## [0.1.0]\n"
        )
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-changelog-entry" in fired

    def test_unreleased_empty_does_not_fire(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        (tmp_path / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [Unreleased]\n\n## [0.1.0]\n"
        )
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-changelog-entry" not in fired

    def test_missing_changelog_does_not_fire(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-changelog-entry" not in fired


# ---------------------------------------------------------------------------
# second-agent-type (roster scan)
# ---------------------------------------------------------------------------


class TestSecondAgentTypeTrigger:
    def test_fires_with_two_agents(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        _write_team_roster(
            tmp_path,
            "* Anthony (Maintainer)\n"
            "* Claude Opus 4.7 -- author\n"
            "* Codex GPT-5 -- reviewer\n",
        )
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "second-agent-type" in fired

    def test_no_fire_with_single_agent(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        _write_team_roster(
            tmp_path,
            "* Anthony (Maintainer)\n"
            "* Claude Opus 4.7 -- author + reviewer\n",
        )
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "second-agent-type" not in fired

    def test_no_fire_with_unfilled_roster(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        _write_team_roster(
            tmp_path,
            "(The bootstrap records the team here...)",
        )
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "second-agent-type" not in fired


# ---------------------------------------------------------------------------
# first-cross-type-review (file-content scan)
# ---------------------------------------------------------------------------


class TestCrossTypeReviewTrigger:
    def test_fires_when_cross_type_review_present(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        (tmp_path / "dev" / "proposals" / "2026-05-29-x.md").write_text(
            "# Proposal\n"
            "\n"
            "**Author**: Claude Opus 4.7\n"
            "\n"
            "## Review -- Codex (External) -- 2026-05-30\n"
            "\n"
            "Looks good.\n"
        )
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-cross-type-review" in fired

    def test_does_not_fire_for_same_type_review(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        (tmp_path / "dev" / "proposals" / "2026-05-29-x.md").write_text(
            "# Proposal\n"
            "\n"
            "**Author**: Claude Opus 4.7\n"
            "\n"
            "## Review -- Claude (Internal) -- 2026-05-30\n"
            "\n"
            "LGTM.\n"
        )
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-cross-type-review" not in fired


# ---------------------------------------------------------------------------
# Roster boundaries
# ---------------------------------------------------------------------------


class TestRosterReadBoundaries:
    def test_missing_roster_does_not_fire(self, helper: ModuleType, tmp_path: Path) -> None:
        _empty_dev_tree(tmp_path)
        assert "second-agent-type" not in helper.evaluate_action_triggers(tmp_path)

    def test_doubled_opening_marker_does_not_fire(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        _write_team_roster(
            tmp_path,
            "* Claude Opus -- author\n* Codex GPT -- reviewer\n"
            "<!-- cairn:slot team-roster -->\n",
        )
        assert "second-agent-type" not in helper.evaluate_action_triggers(tmp_path)

    @pytest.mark.parametrize("linked_part", ["leaf", "parent"])
    def test_linked_roster_path_is_refused_before_read(
        self, helper: ModuleType, tmp_path: Path, linked_part: str,
    ) -> None:
        project = tmp_path / "project"
        outside = tmp_path / "outside"
        project.mkdir()
        (outside / "dev").mkdir(parents=True)
        _write_team_roster(outside, "* Claude Opus\n* Codex GPT\n")
        if linked_part == "leaf":
            (project / "dev").mkdir()
            (project / "dev" / "agent_collaboration.md").symlink_to(
                outside / "dev" / "agent_collaboration.md"
            )
        else:
            (project / "dev").symlink_to(outside / "dev", target_is_directory=True)
        with pytest.raises(helper.OnboardingSecurityError):
            helper.evaluate_action_triggers(project)


# ---------------------------------------------------------------------------
# Mixed-state smoke test
# ---------------------------------------------------------------------------


class TestMixedAction:
    def test_full_collaborative_team_state_fires_many(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """Realistic fixture: multi-agent collaborative-team state
        with proposals, plans, and a changelog entry. Several
        triggers should fire together."""
        _empty_dev_tree(tmp_path)
        _write_team_roster(
            tmp_path,
            "* Anthony (Maintainer)\n"
            "* Claude Opus 4.7 -- author + reviewer\n"
            "* Codex GPT-5 -- reviewer\n",
        )
        (tmp_path / "dev" / "proposals" / "2026-05-29-x.md").write_text(
            "# P\n\n**Author**: Claude\n\n"
            "## Review -- Codex (External) -- 2026-05-30\n\nLGTM.\n"
        )
        (tmp_path / "dev" / "plans" / "2026-05-29-x.md").write_text("# P\n")
        (tmp_path / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [Unreleased]\n\n* Something.\n"
        )
        fired = helper.evaluate_action_triggers(tmp_path, log_records=[])
        assert "first-proposal-opened" in fired
        assert "first-plan-opened" in fired
        assert "first-changelog-entry" in fired
        assert "second-agent-type" in fired
        assert "first-cross-type-review" in fired
        assert "collab-agreement-signing" not in fired
