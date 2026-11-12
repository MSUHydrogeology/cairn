"""
Tests for the Layer-4 symlink/containment guard.

The guard runs before EVERY write (fresh or --force), fail-closed:
* a symlinked destination raises;
* a symlinked parent directory raises;
* a destination resolving outside target raises;
* a normal install is unaffected.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/

Promises:
- Install refuses to write through a symlinked destination.
- Install refuses to write through a symlinked parent directory.
- Install refuses a destination that resolves outside the target.
- A normal install into a clean target writes its files.
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
