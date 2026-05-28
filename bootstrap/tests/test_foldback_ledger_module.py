"""Module-merge presence tests for the `fold-back-ledger` default-on
module.

Pins the "Template content" merge block against silent regression --
specifically the active-surfacing extension that landed at Chunk 2 of
the `cairn-foldback-active-surfacing` arc.  The capture-side merge
(`Goodnight foldback-capture`) was the pre-active-surfacing baseline;
the surfacing-side merge (`Goodnight foldback-surfacing`) is the new
load-bearing addition.

Also covers the .gitignore-seed registry entry (Chunk 7): the
fold-back-ledger module seeds `dev/upstream/.foldback-draft-*.md`
into the adopter's `.gitignore` so the active-surfacing protocol's
drafted-body temp files are never accidentally committed.

These tests treat the module file as a textual artifact (read it,
assert sub-strings are present).  Behavioral coverage of the merged
session-routines doctrine is out of scope here -- the merge is a
human-and-agent-read prose surface, not an executable contract.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_PATH = (
    CAIRN_ROOT / "templates" / "modules" / "default-on" / "fold-back-ledger.md"
)

# Allow the bootstrap scaffold module to import for the gitignore-seed test.
sys.path.insert(0, str(CAIRN_ROOT))
from bootstrap.scaffold import _GITIGNORE_SEEDS  # noqa: E402

pytestmark = pytest.mark.skipif(
    not MODULE_PATH.exists(),
    reason="Cairn fold-back-ledger module template not available",
)


@pytest.fixture(scope="module")
def module_text() -> str:
    return MODULE_PATH.read_text(encoding="utf-8")


class TestTemplateContentMergeBlocks:
    """The "Template content" section must carry both merge blocks --
    the original capture-side block + the new surfacing-side block.
    Silent loss of either breaks the active-surfacing loop's
    standing-cadence trigger.
    """

    def test_capture_block_present(self, module_text):
        # The pre-arc baseline merge block stays intact.
        assert "Goodnight foldback-capture" in module_text, (
            "Capture merge block missing from module template"
        )

    def test_surfacing_block_present(self, module_text):
        # The new arc's surfacing merge block.
        assert "Goodnight foldback-surfacing" in module_text, (
            "Surfacing merge block missing from module template -- "
            "silent regression of the active-surfacing standing trigger"
        )

    def test_surfacing_block_names_grace_period_default(self, module_text):
        # The grace-period default (7 days) is part of the contract --
        # adopters tune it per deployment.
        assert "7 days" in module_text or "**7 days**" in module_text, (
            "Surfacing merge block must document the default grace period"
        )

    def test_surfacing_block_names_deferred_until_schema(self, module_text):
        assert "deferred-until" in module_text, (
            "Surfacing merge block must reference the deferred-until snooze "
            "field"
        )

    def test_surfacing_block_names_export_scan_invocation(
        self, module_text,
    ):
        # The scrub-gate invocation -- the load-bearing fail-closed step.
        assert "foldback_export_scan.py" in module_text, (
            "Surfacing merge block must name the export-scan scanner "
            "(the fail-closed scrub gate is the load-bearing safety step)"
        )

    def test_surfacing_block_names_body_file_invocation(self, module_text):
        # gh CLI invocation pattern (per VBA #25 / VBA #27).
        assert "--body-file" in module_text, (
            "Surfacing merge block must name the --body-file gh invocation "
            "pattern (the maintainer submits manually after agent draft)"
        )

    def test_surfacing_block_names_filed_pr_status_transition(
        self, module_text,
    ):
        assert "filed -> <issue-#>" in module_text or \
               "filed ->" in module_text, (
            "Surfacing merge block must reference the filed-status "
            "transition the protocol writes on submission"
        )
        assert "pr -> <pr-#>" in module_text or "pr ->" in module_text, (
            "Surfacing merge block must reference the pr-status "
            "transition the protocol writes for PR-shape filings"
        )

    def test_surfacing_block_cross_references_fold_back_doctrine(
        self, module_text,
    ):
        # The merge points at the doctrine surface so an adopter knows
        # where the full active-surfacing protocol lives.
        assert "fold-back.md" in module_text, (
            "Surfacing merge block must cross-link to "
            "doctrine/fold-back.md > Active surfacing"
        )

    def test_surfacing_block_names_maintainer_submits_bright_line(
        self, module_text,
    ):
        # The export-boundary structural guard: agent does NOT submit.
        # Phrasing may evolve; assert at the concept-level (the
        # "by hand" + "agent never submits" combination).
        assert "by hand" in module_text or "agent never" in module_text, (
            "Surfacing merge block must carry the bright-line: the "
            "maintainer submits, the agent does not"
        )


class TestGitignoreSeed:
    """The active-surfacing protocol writes drafted bodies to a
    gitignored temp file pattern; the scaffold's _GITIGNORE_SEEDS
    registry seeds that pattern when the fold-back-ledger module is
    selected, so adopters get the protection by default.
    """

    def test_foldback_ledger_seeds_draft_pattern(self):
        assert "fold-back-ledger" in _GITIGNORE_SEEDS, (
            "fold-back-ledger module missing from _GITIGNORE_SEEDS "
            "registry; the active-surfacing protocol's drafted-body "
            "temp file pattern is not seeded into adopters' .gitignore"
        )
        seeds = _GITIGNORE_SEEDS["fold-back-ledger"]
        assert "dev/upstream/.foldback-draft-*.md" in seeds, (
            f"foldback-draft pattern missing from fold-back-ledger "
            f"gitignore seeds: {seeds}"
        )
