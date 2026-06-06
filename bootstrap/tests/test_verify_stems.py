"""Tests for the ``verify_stems.py`` lifecycle-hygiene script (Fold 1).

``verify_stems.py`` is shipped as a default-on verbatim script alongside
``claim_check.py`` in the ``claim-check`` module family.  It verifies that
every backticked date-prefixed stem (``YYYY-MM-DD-author-slug``) in the
adopter's coordination files (``dev/PLANNING.md``, ``dev/NEXT_SESSION.md``)
resolves to exactly one work-item under ``dev/proposals/`` / ``dev/plans/``.

The key correctness property covered here is the **pair-tolerance fix**:
one proposal PLUS its implementing plan is the normal accepted-and-in-flight
state and must NOT be flagged as ambiguous.  Only >1 proposal OR >1 plan is
a genuine ambiguity.

Also covers:

* Install path -- the script lands verbatim at ``scripts/verify_stems.py``
  when the ``claim-check`` module is selected.
* Zero-match (typo / missing file) → issue reported.
* Ignore directive (``verify-stems-ignore``).
* Custom ``--scan`` to cover adopter-added coordination files.
* The genericized ``--root`` override.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_verify_stems.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
_DEFAULT_ON = TEMPLATES_ROOT / "modules" / "default-on"
VERIFY_STEMS_SRC = _DEFAULT_ON / "verify_stems.py"

pytestmark = pytest.mark.skipif(
    not VERIFY_STEMS_SRC.exists(),
    reason="Cairn verify_stems template not available",
)

sys.path.insert(0, str(CAIRN_ROOT))
from bootstrap.scaffold import _MODULE_MAPPINGS, main as scaffold_main  # noqa: E402


def _load_verify_stems() -> ModuleType:
    """Import the source ``verify_stems.py`` template by file path."""
    name = "_cairn_verify_stems_under_test"
    spec = importlib.util.spec_from_file_location(name, VERIFY_STEMS_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


vs = _load_verify_stems()


def _scaffold(target: Path, modules: list[str]) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: StemTest\ntest_command: pytest\nmodules:\n"
        + "".join(f"  - {m}\n" for m in modules)
    )
    return scaffold_main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    )


def _make_repo(root: Path) -> Path:
    """Create a minimal fake repo tree for verify_stems tests."""
    (root / "dev" / "PLANNING.md").parent.mkdir(parents=True, exist_ok=True)
    (root / "dev" / "NEXT_SESSION.md").write_text("# Next session\n")
    (root / "dev" / "proposals").mkdir(parents=True, exist_ok=True)
    (root / "dev" / "proposals" / "archive").mkdir(parents=True, exist_ok=True)
    (root / "dev" / "plans").mkdir(parents=True, exist_ok=True)
    (root / "dev" / "plans" / "archive").mkdir(parents=True, exist_ok=True)
    return root


# ---------------------------------------------------------------------------
# Install path
# ---------------------------------------------------------------------------

class TestInstallPath:
    """verify_stems.py lands verbatim when claim-check is selected."""

    def test_claim_check_module_ships_verify_stems(self) -> None:
        specs = _MODULE_MAPPINGS["claim-check"]
        dsts = {s.dst: s for s in specs}
        assert "scripts/verify_stems.py" in dsts, (
            "verify_stems.py is not registered in _MODULE_MAPPINGS['claim-check']"
        )
        assert dsts["scripts/verify_stems.py"].verbatim is True, (
            "verify_stems.py must be verbatim=True"
        )

    def test_verify_stems_installed_verbatim(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, ["claim-check"]) == 0
        installed = tmp_path / "scripts" / "verify_stems.py"
        assert installed.is_file(), "scripts/verify_stems.py was not installed"
        assert installed.read_bytes() == VERIFY_STEMS_SRC.read_bytes(), (
            "installed verify_stems.py differs from the template -- not verbatim"
        )


# ---------------------------------------------------------------------------
# Pair-tolerance fix (the key correctness property)
# ---------------------------------------------------------------------------

class TestPairTolerance:
    """One proposal + its implementing plan must NOT be flagged as ambiguous.

    The pair-tolerance fix: a stem is ambiguous only with >1 *proposal* OR
    >1 *plan*.  One proposal + one plan (the normal accepted-and-planned state)
    is NOT an ambiguity and must exit clean.
    """

    def test_one_proposal_one_plan_not_flagged(self, tmp_path: Path) -> None:
        """The canonical pair: one proposal file + one plan file."""
        _make_repo(tmp_path)
        stem = "2026-01-01-author-feature"
        (tmp_path / "dev" / "proposals" / f"{stem}.md").write_text("# proposal\n")
        (tmp_path / "dev" / "plans" / f"{stem}.md").write_text("# plan\n")
        (tmp_path / "dev" / "PLANNING.md").write_text(
            f"see `{stem}`\n"
        )
        issues = vs.check_stems(tmp_path)
        assert issues == [], (
            f"One proposal + one plan must NOT be flagged; got: {issues}"
        )

    def test_archived_proposal_plus_live_plan_not_flagged(
        self, tmp_path: Path
    ) -> None:
        """Archived proposal + live plan is the most common post-acceptance state."""
        _make_repo(tmp_path)
        stem = "2026-01-01-author-archived-plus-live"
        (tmp_path / "dev" / "proposals" / "archive" / f"{stem}.md").write_text(
            "# archived proposal\n"
        )
        (tmp_path / "dev" / "plans" / f"{stem}.md").write_text("# live plan\n")
        (tmp_path / "dev" / "PLANNING.md").write_text(f"see `{stem}`\n")
        issues = vs.check_stems(tmp_path)
        assert issues == [], (
            f"Archived proposal + live plan must NOT be flagged; got: {issues}"
        )

    def test_two_proposals_flagged(self, tmp_path: Path) -> None:
        """Two proposal files with the same stem IS a genuine ambiguity."""
        _make_repo(tmp_path)
        stem = "2026-01-01-author-dupe"
        (tmp_path / "dev" / "proposals" / f"{stem}.md").write_text("# p1\n")
        (tmp_path / "dev" / "proposals" / "archive" / f"{stem}.md").write_text(
            "# p2\n"
        )
        (tmp_path / "dev" / "PLANNING.md").write_text(f"see `{stem}`\n")
        issues = vs.check_stems(tmp_path)
        assert issues, (
            "Two proposal files with the same stem must be flagged as ambiguous"
        )
        assert "ambiguous" in issues[0]

    def test_two_plans_flagged(self, tmp_path: Path) -> None:
        """Two plan files with the same stem IS a genuine ambiguity."""
        _make_repo(tmp_path)
        stem = "2026-01-01-author-dupe-plan"
        (tmp_path / "dev" / "plans" / f"{stem}.md").write_text("# plan1\n")
        (tmp_path / "dev" / "plans" / "archive" / f"{stem}.md").write_text(
            "# plan2\n"
        )
        (tmp_path / "dev" / "PLANNING.md").write_text(f"see `{stem}`\n")
        issues = vs.check_stems(tmp_path)
        assert issues, (
            "Two plan files with the same stem must be flagged as ambiguous"
        )
        assert "ambiguous" in issues[0]

    def test_single_proposal_only_clean(self, tmp_path: Path) -> None:
        """A stem with only a proposal (no plan yet) is fine."""
        _make_repo(tmp_path)
        stem = "2026-01-01-author-proposal-only"
        (tmp_path / "dev" / "proposals" / f"{stem}.md").write_text("# p\n")
        (tmp_path / "dev" / "PLANNING.md").write_text(f"`{stem}`\n")
        issues = vs.check_stems(tmp_path)
        assert issues == [], f"Single proposal must resolve cleanly; got {issues}"

    def test_single_plan_only_clean(self, tmp_path: Path) -> None:
        """A stem with only a plan (orphan, perhaps proposal was archived
        under a slightly different name) is not flagged."""
        _make_repo(tmp_path)
        stem = "2026-01-01-author-plan-only"
        (tmp_path / "dev" / "plans" / f"{stem}.md").write_text("# plan\n")
        (tmp_path / "dev" / "PLANNING.md").write_text(f"`{stem}`\n")
        issues = vs.check_stems(tmp_path)
        assert issues == [], f"Single plan must resolve cleanly; got {issues}"


# ---------------------------------------------------------------------------
# Zero-match and other basic behaviours
# ---------------------------------------------------------------------------

class TestBasicBehaviours:
    """Basic resolution: zero-match, ignore directives, custom scan."""

    def test_zero_match_flagged(self, tmp_path: Path) -> None:
        """A stem that resolves to nothing is an error."""
        _make_repo(tmp_path)
        stem = "2026-01-01-author-nonexistent"
        (tmp_path / "dev" / "PLANNING.md").write_text(f"`{stem}`\n")
        issues = vs.check_stems(tmp_path)
        assert issues
        assert "resolves to no file" in issues[0]

    def test_ignore_directive_exempts_stem(self, tmp_path: Path) -> None:
        """A verify-stems-ignore directive exempts a non-artifact stem."""
        _make_repo(tmp_path)
        stem = "2026-01-01-other-repo-stem"
        (tmp_path / "dev" / "PLANNING.md").write_text(
            f"<!-- verify-stems-ignore: {stem} -- lives in LHM repo -->\n"
            f"`{stem}`\n"
        )
        # No file exists for this stem (it's in another repo)
        issues = vs.check_stems(tmp_path)
        assert issues == [], (
            f"Stem with ignore directive must not be flagged; got: {issues}"
        )

    def test_missing_scan_file_reported(self, tmp_path: Path) -> None:
        """A scanned file that does not exist is reported as an issue."""
        _make_repo(tmp_path)
        # Remove PLANNING.md
        (tmp_path / "dev" / "PLANNING.md").unlink(missing_ok=True)
        issues = vs.check_stems(tmp_path)
        assert any("PLANNING.md" in i and "not found" in i for i in issues), (
            f"Missing PLANNING.md must be reported; got: {issues}"
        )

    def test_custom_scan_file(self, tmp_path: Path) -> None:
        """--scan can point at an adopter-added coordination file."""
        _make_repo(tmp_path)
        stem = "2026-06-01-author-custom"
        (tmp_path / "dev" / "proposals" / f"{stem}.md").write_text("# p\n")
        # The stem is in a custom coordination file, not PLANNING.md
        (tmp_path / "dev" / "PLANNING.md").write_text("nothing here\n")
        custom = tmp_path / "dev" / "MYBOARD.md"
        custom.write_text(f"`{stem}`\n")
        issues = vs.check_stems(
            tmp_path,
            scanned=(Path("dev") / "MYBOARD.md",),
        )
        assert issues == [], (
            f"Custom scan file with a valid stem must be clean; got: {issues}"
        )

    def test_commit_hash_not_matched(self, tmp_path: Path) -> None:
        """A backticked commit hash does not match the stem pattern."""
        _make_repo(tmp_path)
        (tmp_path / "dev" / "PLANNING.md").write_text(
            "landed at `abc1234def`\n"
        )
        issues = vs.check_stems(tmp_path)
        # No stem match -> no issue about the hash
        assert all("abc1234def" not in i for i in issues)

    def test_clean_tree_exits_zero(self, tmp_path: Path, capsys) -> None:
        """main() exits 0 on a clean tree."""
        _make_repo(tmp_path)
        stem = "2026-01-01-author-clean"
        (tmp_path / "dev" / "proposals" / f"{stem}.md").write_text("# p\n")
        (tmp_path / "dev" / "PLANNING.md").write_text(f"`{stem}`\n")
        rc = vs.main(["--root", str(tmp_path)])
        assert rc == 0

    def test_issue_tree_exits_one(self, tmp_path: Path, capsys) -> None:
        """main() exits 1 when there are issues."""
        _make_repo(tmp_path)
        stem = "2026-01-01-author-typo"
        (tmp_path / "dev" / "PLANNING.md").write_text(f"`{stem}`\n")
        rc = vs.main(["--root", str(tmp_path)])
        assert rc == 1
