"""Check scaffold selection for the optional coordination-tiers doctrine.

The broad work-intent requirement belongs to the team-gated
``coordination-tiers`` surface, not the always-on baseline. These tests
check the install-selection behavior: a minimal install omits the module
doctrine file, and selecting the module writes that file. They do not check
the doctrine's wording or whether the generated tree carries the broad
obligation.

Promises:
- A minimal install with no modules does not write the coordination-tiers
  doctrine file.
- Installing the coordination-tiers module writes its doctrine file.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import main  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)

def _scaffold(target: Path, modules: list[str]) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: CoordBoundary\ntest_command: pytest\nmodules:\n"
        + "".join(f"  - {m}\n" for m in modules)
    )
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    )


class TestBroadIntentBoundary:
    def test_minimal_install_omits_coordination_tiers_module(
        self, tmp_path: Path
    ) -> None:
        """A kernel/default install does not include the optional module."""
        assert _scaffold(tmp_path, []) == 0
        # The module doctrine file is simply not installed.
        assert not (tmp_path / "dev" / "modules"
                    / "coordination-tiers.md").is_file()

    def test_coordination_tiers_install_writes_module(
        self, tmp_path: Path
    ) -> None:
        """Selecting coordination-tiers writes its doctrine file."""
        assert _scaffold(tmp_path, ["coordination-tiers"]) == 0
        module = tmp_path / "dev" / "modules" / "coordination-tiers.md"
        assert module.is_file(), "coordination-tiers doctrine not installed"
