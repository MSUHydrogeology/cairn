"""
Tests for the practice-discipline modules.

* Install-path: each new module installs to the modules tree on selection
  and respects skip-if-exists.
* Classification: the three modules are team-gated and NOT default-on
  (an omit-`modules:` install does not pull them in).

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
# Classification
# ---------------------------------------------------------------------------

class TestClassification:
    @pytest.mark.parametrize("module", _PRACTICE_MODULES)
    def test_registered_team_gated(self, module: str) -> None:
        assert module in _MODULE_MAPPINGS, f"{module} not registered"
        specs = _MODULE_MAPPINGS[module]
        # Every practice module installs its doctrine .md first.
        doctrine = specs[0]
        assert doctrine.src == f"team-gated/{module}.md"
        assert doctrine.dst == f"dev/modules/{module}.md"
        assert doctrine.verbatim is False
        if module == "doc-drift-prevention":
            # Cairn v0.2 foldback: this module flipped from doctrine-only
            # to doctrine + two verbatim stack-neutral tools.
            tools = {s.dst: s for s in specs[1:]}
            assert tools["scripts/link_check.py"].verbatim is True
            assert tools["scripts/sync_doc_snippets.py"].verbatim is True
            assert len(specs) == 3
        else:
            assert len(specs) == 1, "this practice module is doctrine-only"

    @pytest.mark.parametrize("module", _PRACTICE_MODULES)
    def test_not_default_on(self, module: str) -> None:
        # must not double the auto-installed default set -- the presets
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
