"""
Tests for the Layer-4 symlink/containment guard.

The guard runs before EVERY write (fresh or --force), fail-closed:
* a symlinked destination raises;
* a symlinked parent directory raises;
* a destination resolving outside target raises;
* a normal install is unaffected.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    ScaffoldSecurityError,
    _assert_safe_write,
    install_core,
)

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"


# ---------------------------------------------------------------------------
# Unit: _assert_safe_write
# ---------------------------------------------------------------------------

class TestAssertSafeWrite:
    def test_normal_destination_is_allowed(self, tmp_path: Path) -> None:
        # A real (non-symlink) dst under target, parents real -> no raise.
        (tmp_path / "sub").mkdir()
        _assert_safe_write(tmp_path / "sub" / "file.md", tmp_path)
        # dst whose parent does not yet exist is also fine (mkdir creates
        # real dirs).
        _assert_safe_write(tmp_path / "new" / "deep" / "file.md", tmp_path)

    def test_symlinked_destination_raises(self, tmp_path: Path) -> None:
        outside = tmp_path / "outside"
        outside.mkdir()
        dst = tmp_path / "tgt" / "AGENTS.md"
        dst.parent.mkdir()
        dst.symlink_to(outside / "evil.md")  # dangling symlink at dst
        with pytest.raises(ScaffoldSecurityError):
            _assert_safe_write(dst, tmp_path / "tgt")

    def test_symlinked_parent_raises(self, tmp_path: Path) -> None:
        target = tmp_path / "tgt"
        target.mkdir()
        outside_dir = tmp_path / "outside_dev"
        outside_dir.mkdir()
        # target/dev is a symlink to a dir outside target.
        (target / "dev").symlink_to(outside_dir)
        with pytest.raises(ScaffoldSecurityError):
            _assert_safe_write(target / "dev" / "README.md", target)

    def test_escaping_destination_raises(self, tmp_path: Path) -> None:
        target = tmp_path / "tgt"
        target.mkdir()
        (tmp_path / "outside").mkdir()
        # A dst that resolves outside target via ``..``.
        escaping = target / ".." / "outside" / "x.md"
        with pytest.raises(ScaffoldSecurityError):
            _assert_safe_write(escaping, target)


# ---------------------------------------------------------------------------
# Integration: the guard is wired into the write path (fresh AND --force)
# ---------------------------------------------------------------------------

class TestGuardWiredIntoInstall:
    @pytest.mark.skipif(
        not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
    )
    @pytest.mark.parametrize("force", [False, True])
    def test_symlinked_dst_blocks_install(
        self, tmp_path: Path, force: bool
    ) -> None:
        """A planted symlink at a core destination makes the install
        raise -- fresh (force=False) AND --force -- and nothing is
        written through the link."""
        target = tmp_path / "tgt"
        target.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        evil = outside / "AGENTS.md"
        # Plant a symlink at the first core destination (AGENTS.md).
        (target / "AGENTS.md").symlink_to(evil)
        tokens = {"project_name": "T", "test_command": "pytest"}
        with pytest.raises(ScaffoldSecurityError):
            install_core(TEMPLATES_ROOT, target, tokens, force=force)
        # The write was refused -- nothing landed through the symlink.
        assert not evil.exists(), "install wrote through the planted symlink"


# ---------------------------------------------------------------------------
# A planted symlink in the adopter tree is rejected by the scaffold's write
# guard, not just by the install paths that call it.
# ---------------------------------------------------------------------------


class TestCrossHelperContainment:
    """One symlinked target tree, one refusal."""

    @pytest.mark.skipif(
        not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
    )
    def test_planted_symlink_refused_by_the_scaffold_helper(
        self, tmp_path: Path,
    ) -> None:
        # Adopter tree with a planted symlinked dev/ directory pointing
        # outside the target.
        target = tmp_path / "tgt"
        target.mkdir()
        outside_dev = tmp_path / "evil_dev"
        outside_dev.mkdir()
        (target / "dev").symlink_to(outside_dev, target_is_directory=True)

        # The scaffold's _assert_safe_write refuses a write that would
        # traverse the symlinked dev/.
        with pytest.raises(ScaffoldSecurityError):
            _assert_safe_write(target / "dev" / "PLANNING.md", target)
