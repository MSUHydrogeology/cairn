"""Tests for the Fold 5 model-selection stub mapping + fidelity gate.

Covers:
* Stub file is installed on scaffold of ``model-selection`` module.
* Check script is installed verbatim.
* Fidelity check: exits 0 on a filled (no ``FILL ME``) mapping.
* Fidelity check: exits 1 (non-zero) on an unfilled (``FILL ME``) mapping.
* Fidelity check: exits 2 when the mapping file is missing entirely.
* Seed-vs-gate: a fresh scaffold installs a stub that passes the gate.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_model_selection_stub.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
_TEAM_GATED = TEMPLATES_ROOT / "modules" / "team-gated"
_CHECKER_SRC = _TEAM_GATED / "check_model_selection.py"
_STUB_SRC = _TEAM_GATED / "model_selection_mapping_stub.yml"

sys.path.insert(0, str(CAIRN_ROOT))
from bootstrap.scaffold import _MODULE_MAPPINGS, main as scaffold_main  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _load_checker(name: str = "_cairn_check_model_sel_under_test") -> ModuleType:
    if not _CHECKER_SRC.exists():
        pytest.skip("check_model_selection.py template not available")
    spec = importlib.util.spec_from_file_location(name, _CHECKER_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _scaffold(target: Path) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: ModelSelTest\ntest_command: pytest\nmodules:\n"
        "  - model-selection\n"
    )
    return scaffold_main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    )


# ---------------------------------------------------------------------------
# Module registration
# ---------------------------------------------------------------------------

class TestModuleRegistration:
    def test_stub_registered(self) -> None:
        specs = _MODULE_MAPPINGS["model-selection"]
        dsts = {s.dst: s for s in specs}
        assert "dev/.cairn/model-selection-mapping.yml" in dsts, (
            "model-selection-mapping.yml stub not registered under "
            "'model-selection' module"
        )
        # The stub is a YAML template (substituted, not verbatim).
        assert dsts["dev/.cairn/model-selection-mapping.yml"].verbatim is False

    def test_checker_registered(self) -> None:
        specs = _MODULE_MAPPINGS["model-selection"]
        dsts = {s.dst: s for s in specs}
        assert "scripts/check_model_selection.py" in dsts, (
            "check_model_selection.py not registered under 'model-selection' module"
        )
        assert dsts["scripts/check_model_selection.py"].verbatim is True


# ---------------------------------------------------------------------------
# Install-path
# ---------------------------------------------------------------------------

class TestInstallPath:
    def test_stub_installed_on_scaffold(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path) == 0
        stub = tmp_path / "dev" / ".cairn" / "model-selection-mapping.yml"
        assert stub.is_file(), "model-selection-mapping.yml not installed"

    def test_checker_installed_on_scaffold(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path) == 0
        checker = tmp_path / "scripts" / "check_model_selection.py"
        assert checker.is_file(), "check_model_selection.py not installed"
        assert checker.read_bytes() == _CHECKER_SRC.read_bytes(), (
            "Installed check_model_selection.py differs from template"
        )


# ---------------------------------------------------------------------------
# Seed-vs-gate sequencing: fresh install passes the gate
# ---------------------------------------------------------------------------

class TestSeedVsGate:
    """A fresh scaffold seeds an unfilled FILL-ME stub that FAILS the gate
    (R1: forced, not silent) — while the scaffold install itself succeeds."""

    def test_fresh_scaffold_install_succeeds(self, tmp_path: Path) -> None:
        # "Not instantly red" = the install is not blocked.
        assert _scaffold(tmp_path) == 0
        stub = tmp_path / "dev" / ".cairn" / "model-selection-mapping.yml"
        assert stub.is_file()

    def test_fresh_scaffold_fails_gate_until_filled(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path) == 0
        stub = tmp_path / "dev" / ".cairn" / "model-selection-mapping.yml"
        assert stub.is_file()

        checker = _load_checker()
        # R1: a fresh, unfilled mapping carries FILL ME -> the gate FAILS,
        # forcing the adopter to record their assignments (not silent-empty).
        rc = checker.check_mapping(stub, quiet=True)
        assert rc == 1, (
            f"Fresh scaffold stub is unfilled (carries FILL ME) and MUST fail "
            f"the gate to force the adopter to complete it; got exit code {rc}"
        )


# ---------------------------------------------------------------------------
# Fidelity check: pass / fail / missing
# ---------------------------------------------------------------------------

class TestFidelityCheck:
    @pytest.fixture(scope="class")
    def checker(self) -> ModuleType:
        return _load_checker()

    def test_filled_mapping_passes(self, tmp_path: Path, checker) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "# Model selection mapping\n"
            "mapping:\n"
            "  - tier: high\n"
            "    model: vendor-a/flagship\n"
            "    date_verified: 2025-01-01\n"
            "    task_family: strategy\n"
            "    source: benchmark-jan-2025\n"
        )
        rc = checker.check_mapping(mapping, quiet=True)
        assert rc == 0, f"Fully filled mapping should pass; got {rc}"

    def test_unfilled_mapping_fails_nonzero(self, tmp_path: Path, checker) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "mapping:\n"
            "  - tier: high\n"
            "    model: FILL ME\n"
            "    date_verified: FILL ME\n"
            "    task_family: strategy\n"
            "    source: FILL ME\n"
        )
        rc = checker.check_mapping(mapping, quiet=True)
        assert rc != 0, "Mapping with FILL ME should fail the gate"
        assert rc == 1, f"Expected exit code 1, got {rc}"

    def test_missing_mapping_exits_2(self, tmp_path: Path, checker) -> None:
        missing = tmp_path / "no-such.yml"
        rc = checker.check_mapping(missing, quiet=True)
        assert rc == 2, f"Missing mapping file should exit 2, got {rc}"

    def test_partial_fill_still_fails(self, tmp_path: Path, checker) -> None:
        """A partially filled mapping that still contains one FILL ME fails."""
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "mapping:\n"
            "  - tier: high\n"
            "    model: vendor-a/flagship\n"
            "    date_verified: 2025-01-01\n"
            "    task_family: strategy\n"
            "    source: FILL ME\n"  # still unfilled
        )
        rc = checker.check_mapping(mapping, quiet=True)
        assert rc == 1, f"Partial fill with FILL ME should fail; got {rc}"

    def test_fill_me_in_comment_fails(self, tmp_path: Path, checker) -> None:
        """Even a FILL ME in a comment triggers the gate.

        This is intentional: the gate scans the whole file to catch any
        remaining placeholder, including commented-out examples the adopter
        left in.  An adopter who cleans up the comments will also pass.
        """
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "# TODO: FILL ME -- add medium-tier model here\n"
            "mapping:\n"
            "  - tier: high\n"
            "    model: vendor-a/flagship\n"
            "    date_verified: 2025-01-01\n"
            "    task_family: strategy\n"
            "    source: benchmark-jan-2025\n"
        )
        rc = checker.check_mapping(mapping, quiet=True)
        assert rc == 1, (
            "A FILL ME in a comment should still fail; "
            "the adopter must clean up placeholders."
        )

    def test_cli_failure_message_mentions_fill_me(
        self, tmp_path: Path, checker, capsys
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text("mapping:\n  - tier: high\n    model: FILL ME\n")
        rc = checker.main(["--mapping", str(mapping)])
        assert rc == 1
        err = capsys.readouterr().err
        assert "FILL ME" in err

    def test_cli_success_no_error_output(
        self, tmp_path: Path, checker, capsys
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "mapping:\n"
            "  - tier: high\n"
            "    model: vendor/flagship\n"
            "    date_verified: 2025-01-01\n"
            "    task_family: strategy\n"
            "    source: benchmark\n"
        )
        rc = checker.main(["--mapping", str(mapping)])
        assert rc == 0
        err = capsys.readouterr().err
        assert err == ""
