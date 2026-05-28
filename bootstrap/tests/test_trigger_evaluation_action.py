"""Tests for action-trigger evaluators (Chunk P1.9b).

Plan: 2026-05-28-claude-cairn-progressive-onboarding.

Per Codex External Review P2-3: action triggers observe **explicit**
deployment state (filesystem + roster slot + ledger + file-content
parsing) wherever possible, NOT git archaeology.  The
``collab-agreement-signing`` trigger explicitly named in P2-3
consults the activation log to confirm the
``first-proposal-archived`` precondition has previously fired.

Each trigger gets positive + negative fixture tests; the
``collab-agreement-signing`` trigger gets four fixtures per the
plan's P1.9b spec.

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


def _write_collab_agreement(
    tmp_path: Path, roster_body: str,
) -> None:
    coll = tmp_path / "dev" / "collaboration_agreement.md"
    coll.write_text(
        "# Collaboration agreement\n"
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
        _write_collab_agreement(
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
        _write_collab_agreement(
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
        _write_collab_agreement(
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
# first-foldback-candidate (ledger scan)
# ---------------------------------------------------------------------------


class TestFoldbackCandidateTrigger:
    def test_fires_with_candidate_row(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        (tmp_path / "dev" / "upstream").mkdir()
        (tmp_path / "dev" / "upstream" / "fold-back-ledger.md").write_text(
            "# Fold-back ledger\n"
            "\n"
            "| ID | Title | Status |\n"
            "|----|-------|--------|\n"
            "| F1 | thing | candidate |\n"
        )
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-foldback-candidate" in fired

    def test_does_not_fire_without_candidate_row(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        _empty_dev_tree(tmp_path)
        (tmp_path / "dev" / "upstream").mkdir()
        (tmp_path / "dev" / "upstream" / "fold-back-ledger.md").write_text(
            "# Fold-back ledger\n"
            "\n"
            "| ID | Title | Status |\n"
            "|----|-------|--------|\n"
            "| F1 | thing | synced |\n"
        )
        fired = helper.evaluate_action_triggers(tmp_path)
        assert "first-foldback-candidate" not in fired


# ---------------------------------------------------------------------------
# collab-agreement-signing (4 fixtures per plan P1.9b spec)
# ---------------------------------------------------------------------------


class TestCollabAgreementSigningTrigger:
    def test_positive_roster_unfilled_and_proposal_archived(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """Roster unfilled + first-proposal-archived just fired (in
        the current state) -> trigger fires."""
        _empty_dev_tree(tmp_path)
        _write_collab_agreement(
            tmp_path, "(The bootstrap records the team here...)",
        )
        (tmp_path / "dev" / "proposals" / "archive" / "x.md").write_text("#\n")
        fired = helper.evaluate_action_triggers(tmp_path, log_records=[])
        assert "collab-agreement-signing" in fired

    def test_positive_roster_unfilled_and_prior_log_fired(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """Roster unfilled + log carries a prior `first-proposal-
        archived` activation -> trigger fires (the log is the
        explicit-state-of-prior-fires record)."""
        _empty_dev_tree(tmp_path)
        _write_collab_agreement(
            tmp_path, "(The bootstrap records the team here...)",
        )
        # No proposal in archive at the moment; the log has it.
        prior_log = [
            helper.ActivationRecord(
                "post-first-proposal",
                "2026-05-29T00:00:00Z", "agent-1", "solo-greenfield",
                "first-proposal-archived",
            ),
        ]
        fired = helper.evaluate_action_triggers(
            tmp_path, log_records=prior_log,
        )
        assert "collab-agreement-signing" in fired

    def test_negative_roster_filled(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """Roster filled -> trigger suppressed even if proposal
        archive has fired."""
        _empty_dev_tree(tmp_path)
        _write_collab_agreement(
            tmp_path,
            "* Anthony (Maintainer)\n* Claude Opus 4.7 -- author\n",
        )
        (tmp_path / "dev" / "proposals" / "archive" / "x.md").write_text("#\n")
        fired = helper.evaluate_action_triggers(tmp_path, log_records=[])
        assert "collab-agreement-signing" not in fired

    def test_negative_proposal_never_archived(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """Roster unfilled BUT first-proposal-archived has never fired
        -> trigger suppressed (deployment hasn't earned the prompt)."""
        _empty_dev_tree(tmp_path)
        _write_collab_agreement(
            tmp_path, "(The bootstrap records the team here...)",
        )
        # No archived proposals; empty log.
        fired = helper.evaluate_action_triggers(tmp_path, log_records=[])
        assert "collab-agreement-signing" not in fired


# ---------------------------------------------------------------------------
# Mixed-state smoke test
# ---------------------------------------------------------------------------


class TestMixedAction:
    def test_full_collaborative_team_state_fires_many(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """Realistic fixture: multi-agent collaborative-team state
        with proposals, plans, changelog entry, foldback candidate.
        Several triggers should fire together."""
        _empty_dev_tree(tmp_path)
        _write_collab_agreement(
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
        (tmp_path / "dev" / "upstream").mkdir()
        (tmp_path / "dev" / "upstream" / "fold-back-ledger.md").write_text(
            "| ID | T | Status |\n|--|--|--|\n| F1 | x | candidate |\n"
        )
        fired = helper.evaluate_action_triggers(tmp_path, log_records=[])
        assert "first-proposal-opened" in fired
        assert "first-plan-opened" in fired
        assert "first-changelog-entry" in fired
        assert "second-agent-type" in fired
        assert "first-cross-type-review" in fired
        assert "first-foldback-candidate" in fired
        # Roster is FILLED, so collab-agreement-signing must NOT fire.
        assert "collab-agreement-signing" not in fired
