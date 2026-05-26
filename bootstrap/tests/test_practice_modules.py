"""
Tests for the Cairn v0.2 P3 practice-discipline modules + maturity ladder.

* Install-path: each new module installs to the modules tree on selection
  and respects skip-if-exists.
* Classification (I2): the three modules are team-gated and NOT default-on
  (an omit-`modules:` install does not pull them in).
* Ladder correspondence (I5): the maturity ladder in on-ramp/README.md
  maps 1:1 onto the three on-ramp adoption levels -- dogfooding the
  doc-drift discipline P3 itself ships.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import (  # noqa: E402
    _DEFAULT_ON_MODULES,
    _MODULE_MAPPINGS,
    install_modules,
    main,
)

_PRACTICE_MODULES = (
    "testing-discipline",
    "doc-drift-prevention",
    "examples-gallery",
)

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


# ---------------------------------------------------------------------------
# Classification (I2)
# ---------------------------------------------------------------------------

class TestClassification:
    @pytest.mark.parametrize("module", _PRACTICE_MODULES)
    def test_registered_team_gated(self, module: str) -> None:
        assert module in _MODULE_MAPPINGS, f"{module} not registered"
        specs = _MODULE_MAPPINGS[module]
        assert len(specs) == 1, "practice modules are doctrine-only (one .md)"
        spec = specs[0]
        assert spec.src == f"team-gated/{module}.md"
        assert spec.dst == f"dev/modules/{module}.md"
        assert spec.verbatim is False

    @pytest.mark.parametrize("module", _PRACTICE_MODULES)
    def test_not_default_on(self, module: str) -> None:
        # I2: must not double the auto-installed default set -- P4 presets
        # turn them on per profile.
        assert module not in _DEFAULT_ON_MODULES

    def test_omit_modules_does_not_install_practice(
        self, tmp_path: Path
    ) -> None:
        """An omit-`modules:` install pulls in the default-on set only --
        none of the practice modules."""
        cfg = tmp_path / "profile.yml"
        cfg.write_text("project_name: T\ntest_command: pytest\n")
        rc = main([
            "--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
        ])
        assert rc == 0
        for module in _PRACTICE_MODULES:
            assert not (tmp_path / "dev" / "modules" / f"{module}.md").exists()


# ---------------------------------------------------------------------------
# Install-path
# ---------------------------------------------------------------------------

class TestInstallPath:
    def test_modules_install_on_selection(self, tmp_path: Path) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: T\ntest_command: pytest\nmodules:\n"
            + "".join(f"  - {m}\n" for m in _PRACTICE_MODULES)
        )
        rc = main([
            "--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
        ])
        assert rc == 0
        for module in _PRACTICE_MODULES:
            installed = tmp_path / "dev" / "modules" / f"{module}.md"
            assert installed.is_file(), f"{module} not installed"
            # Cross-links to the signpost layer survive the install.
            assert "further-reading.md" in installed.read_text()

    def test_skip_if_exists(self, tmp_path: Path) -> None:
        (tmp_path / "dev" / "modules").mkdir(parents=True)
        install_modules(TEMPLATES_ROOT, tmp_path, {}, ["testing-discipline"])
        target = tmp_path / "dev" / "modules" / "testing-discipline.md"
        edited = target.read_text() + "\n<!-- adopter note -->\n"
        target.write_text(edited)
        install_modules(TEMPLATES_ROOT, tmp_path, {}, ["testing-discipline"])
        assert target.read_text() == edited, "re-install clobbered an edit"


# ---------------------------------------------------------------------------
# Ladder <-> adoption-level correspondence (I5)
# ---------------------------------------------------------------------------

class TestLadderCorrespondence:
    def _onramp_text(self) -> str:
        return (CAIRN_ROOT / "on-ramp" / "README.md").read_text(
            encoding="utf-8")

    def test_ladder_levels_match_adoption_levels(self) -> None:
        text = self._onramp_text()
        # Adoption-level headings: "## Level N — ...".
        heading_levels = {
            int(m) for m in re.findall(r"^##\s+Level\s+(\d)", text, re.M)
        }
        assert heading_levels, "no adoption-level headings found"

        # The maturity-ladder section + its rung level references.
        ladder_match = re.search(
            r"^##\s+The maturity ladder\b(.*?)(?=^##\s|\Z)", text,
            re.M | re.S)
        assert ladder_match, "no maturity-ladder section found"
        rung_levels = {
            int(m) for m in re.findall(
                r"\*\*Level\s+(\d)", ladder_match.group(1))
        }
        assert rung_levels, "ladder has no level-keyed rungs"

        # 1:1 correspondence: every adoption level has a rung; every rung
        # maps to a real adoption level.
        assert rung_levels == heading_levels, (
            f"ladder rungs {sorted(rung_levels)} do not match adoption "
            f"levels {sorted(heading_levels)} -- the ladder drifted from "
            f"the on-ramp levels"
        )
