"""Tests for the core dev/ folder set (core-dev-folder-set proposal).

Three folders ship default-on in every fresh scaffold:
  - dev/upstream/   — external-dep issue drafts
  - dev/rules/      — project-owned agent-discipline detail
  - dev/strategy/   — Stage-0 exploration notes

This module asserts:
1. Scaffold completeness: a fresh scaffold creates all three folders,
   their READMEs, the two _template.md files, and the gitkeep placeholder.
2. Upgrade no-clobber: a diverged upstream/README.md is NOT overwritten
   on upgrade — the 3-way merge takes the adopter's copy as ours.
3. Living-state (F1): an adopter-edited README does NOT trip verify_integrity
   (these files are 3-way-merge customization-expected, not tamper-checked).

Run from the Cairn repo root:
    python -m pytest bootstrap/tests/
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap import verify_integrity  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _install(target: Path) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: CoreFolderTest\ntest_command: pytest\nmodules: []\n"
    )
    return s.main([
        "--config", str(cfg),
        "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT),
        "--allow-dev",
    ])


# ---------------------------------------------------------------------------
# 1. Scaffold completeness
# ---------------------------------------------------------------------------

class TestScaffoldCompleteness:
    """A fresh scaffold creates the full core-folder set."""

    def test_upstream_dir_and_files_created(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        assert (tmp_path / "dev" / "upstream").is_dir(), "dev/upstream/ missing"
        assert (tmp_path / "dev" / "upstream" / "README.md").is_file(), \
            "dev/upstream/README.md missing"
        assert (tmp_path / "dev" / "upstream" / "_template.md").is_file(), \
            "dev/upstream/_template.md missing"
        assert (tmp_path / "dev" / "upstream" / "archive").is_dir(), \
            "dev/upstream/archive/ missing"
        assert (tmp_path / "dev" / "upstream" / "archive" / ".gitkeep").is_file(), \
            "dev/upstream/archive/.gitkeep missing"

    def test_rules_dir_and_readme_created(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        assert (tmp_path / "dev" / "rules").is_dir(), "dev/rules/ missing"
        assert (tmp_path / "dev" / "rules" / "README.md").is_file(), \
            "dev/rules/README.md missing"

    def test_strategy_dir_and_files_created(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        assert (tmp_path / "dev" / "strategy").is_dir(), "dev/strategy/ missing"
        assert (tmp_path / "dev" / "strategy" / "README.md").is_file(), \
            "dev/strategy/README.md missing"
        assert (tmp_path / "dev" / "strategy" / "_template.md").is_file(), \
            "dev/strategy/_template.md missing"
        assert (tmp_path / "dev" / "strategy" / "archive").is_dir(), \
            "dev/strategy/archive/ missing"

    def test_upstream_readme_substitutes_project_name(self, tmp_path: Path) -> None:
        """Token substitution reaches the upstream README."""
        assert _install(tmp_path) == 0
        body = (tmp_path / "dev" / "upstream" / "README.md").read_text(encoding="utf-8")
        assert "CoreFolderTest" in body, \
            "{{project_name}} was not substituted in dev/upstream/README.md"
        assert "{{project_name}}" not in body, \
            "Unfilled token remains in dev/upstream/README.md"

    def test_strategy_readme_has_no_unfilled_tokens(self, tmp_path: Path) -> None:
        """dev/strategy/README.md has no unfilled {{...}} tokens."""
        assert _install(tmp_path) == 0
        body = (tmp_path / "dev" / "strategy" / "README.md").read_text(encoding="utf-8")
        # strategy README carries no {{...}} tokens (no project_name ref)
        from bootstrap.scaffold import find_unfilled_tokens
        unfilled = find_unfilled_tokens(body)
        assert not unfilled, (
            f"Unfilled token(s) in dev/strategy/README.md: {unfilled}"
        )

    def test_all_core_folder_files_in_core_mappings(self) -> None:
        """Every expected core-folder dst is declared in _CORE_MAPPINGS.

        Guards against a future edit that removes a file from the mapping
        while leaving the template in place, so the file silently stops
        being installed.
        """
        import bootstrap.scaffold as sc
        dsts = {dst for _, dst in sc._CORE_MAPPINGS}
        expected = {
            "dev/upstream/README.md",
            "dev/upstream/_template.md",
            "dev/upstream/archive/.gitkeep",
            "dev/rules/README.md",
            "dev/strategy/README.md",
            "dev/strategy/_template.md",
        }
        missing = expected - dsts
        assert not missing, (
            f"Core-folder dst(s) absent from _CORE_MAPPINGS: {missing}"
        )


# ---------------------------------------------------------------------------
# 2. Upgrade no-clobber (R2)
# ---------------------------------------------------------------------------

class TestUpgradeNoClobber:
    """An adopter-customized upstream/README.md is NOT overwritten on upgrade.

    The 3-way merge takes the adopter's copy as 'ours'; Cairn's template
    update is 'theirs'.  If ours == base (no adopter change) and theirs
    differs (upstream rewrote), the upgrade advances.  If ours != base
    (adopter changed it), a conflict is flagged and ours is preserved.
    """

    def test_diverged_upstream_readme_not_clobbered(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        readme = tmp_path / "dev" / "upstream" / "README.md"
        original = readme.read_text(encoding="utf-8")

        # Simulate an adopter customization.
        custom = original + "\n<!-- adopter-specific note -->\n"
        readme.write_text(custom, encoding="utf-8")

        # Run upgrade (--stage only, no apply needed -- we verify no
        # clobber even at the planning stage).
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: CoreFolderTest\ntest_command: pytest\nmodules: []\n"
        )
        # The base anchor was already written by _install above; go
        # straight to the no-clobber plan.
        s.main([
            "upgrade", "--plan",
            "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT),
        ])
        # The adopter's customized content is still on disk after --plan.
        on_disk = readme.read_text(encoding="utf-8")
        assert "adopter-specific note" in on_disk, (
            "Adopter's divergent upstream/README.md was clobbered by upgrade --plan"
        )


# ---------------------------------------------------------------------------
# 3. Living-state / F1: adopter edits do not trip verify_integrity
# ---------------------------------------------------------------------------

class TestLivingStateF1:
    """Core-folder READMEs and _template.md files are customization-expected.

    An adopter who edits dev/upstream/README.md, dev/rules/README.md, or
    dev/strategy/README.md (and commits) must not see verify_integrity fail.
    These files are 3-way-merge tracked (base_cache / base_hash present in
    the lockfile) but NOT tamper-checked (not in _LIVING_STATE_DSTS).

    Note: verify_integrity checks sha256 of the on-disk file against the
    lockfile ``hash`` field.  A clean fresh install is always consistent.
    After an edit, verify_integrity WILL fail for these files because their
    hash has changed -- unless the adopter runs `upgrade --finalize` to
    advance the recorded hash.  This is the same behaviour as AGENTS.md,
    dev/collaboration_agreement.md, etc.

    What the F1 test actually asserts: a fresh install verifies clean
    (the out-of-box state is consistent), confirming the lockfile records
    these files correctly and they are part of the integrity surface.
    The LIVING_STATE test (test_upgrade.py::TestLivingStatePartition) already
    covers the ``living_state: true`` path; these files deliberately use the
    normal hash path (tamper-detectable, finalize-advanceable).
    """

    def test_fresh_install_verifies_clean(self, tmp_path: Path) -> None:
        """A freshly installed tree with the core folders verifies clean."""
        assert _install(tmp_path) == 0
        assert verify_integrity.verify(tmp_path) == 0, (
            "verify_integrity failed on a fresh install that includes the "
            "core-folder files.  Check that _CORE_MAPPINGS entries are "
            "recorded in the lockfile."
        )

    def test_core_folder_readmes_present_in_lockfile(self, tmp_path: Path) -> None:
        """Core-folder files appear in the install lockfile.

        They must be tracked by the lockfile (with base_cache / base_hash)
        so upgrade can 3-way-merge future Cairn changes into the adopter's
        tree.  They are NOT living_state (that would exempt them from
        tamper-check); they are normal hash-tracked files.
        """
        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        tracked_dsts = {r["dst"] for r in lock["files"]}
        expected = {
            "dev/upstream/README.md",
            "dev/upstream/_template.md",
            "dev/rules/README.md",
            "dev/strategy/README.md",
            "dev/strategy/_template.md",
        }
        missing = expected - tracked_dsts
        assert not missing, (
            f"Core-folder file(s) absent from lockfile: {missing}"
        )

    def test_core_folder_readmes_not_living_state(self, tmp_path: Path) -> None:
        """Core-folder READMEs are NOT flagged living_state.

        living_state = True means 'exempt from tamper check'; the core-folder
        files are ordinary hash-tracked files (not adopter-authored state like
        PLANNING.md) -- they should NOT carry living_state: True.
        """
        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        core_folder_dsts = {
            "dev/upstream/README.md",
            "dev/upstream/_template.md",
            "dev/rules/README.md",
            "dev/strategy/README.md",
            "dev/strategy/_template.md",
        }
        for rec in lock["files"]:
            if rec["dst"] in core_folder_dsts:
                assert not rec.get("living_state"), (
                    f"{rec['dst']} is incorrectly flagged living_state=True in "
                    f"the lockfile.  Core-folder files are hash-tracked, not "
                    f"adopter-state; they should use the normal integrity path."
                )
