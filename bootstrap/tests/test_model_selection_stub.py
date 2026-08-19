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
from bootstrap._scaffold.install import (  # noqa: E402
    capture_model_selection_mapping,
)

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
    (forced, not silent) — while the scaffold install itself succeeds."""

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
        # A fresh, unfilled mapping carries FILL ME -> the gate FAILS,
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


# ---------------------------------------------------------------------------
# Structural validity: yaml.safe_load + graceful
# degradation when PyYAML is absent.
# ---------------------------------------------------------------------------

class TestStructuralValidity:
    @pytest.fixture(scope="class")
    def checker(self) -> ModuleType:
        return _load_checker()

    def test_valid_filled_passes_structural(
        self, tmp_path: Path, checker
    ) -> None:
        """A filled, structurally valid mapping passes (the structural check
        runs and is satisfied)."""
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "mapping:\n"
            "  - tier: high\n"
            "    model: vendor-a/flagship\n"
            "    source: benchmark\n"
        )
        assert checker.check_mapping(mapping, quiet=True) == 0

    def test_malformed_yaml_filled_fails_3(
        self, tmp_path: Path, checker
    ) -> None:
        """A filled (no FILL ME) but malformed-YAML mapping passes the sentinel
        scan yet fails the structural check -- exit 3, not a silent pass that
        crashes the loader later."""
        mapping = tmp_path / "model-selection-mapping.yml"
        # Unbalanced flow sequence -> yaml.safe_load raises YAMLError. No
        # "FILL ME" present, so it clears the sentinel scan.
        mapping.write_text("mapping: [unclosed\n  - tier: high\n")
        rc = checker.check_mapping(mapping, quiet=True)
        assert rc == 3, f"Malformed YAML should exit 3, got {rc}"

    def test_non_mapping_top_level_fails_3(
        self, tmp_path: Path, checker
    ) -> None:
        """A filled file that parses but is not a top-level mapping (e.g. a bare
        list) fails structurally -- the loader expects a mapping."""
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text("- tier: high\n- tier: low\n")
        rc = checker.check_mapping(mapping, quiet=True)
        assert rc == 3, f"Non-mapping top level should exit 3, got {rc}"

    def test_malformed_message_is_clean(
        self, tmp_path: Path, checker, capsys
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text("mapping: [unclosed\n")
        rc = checker.main(["--mapping", str(mapping)])
        assert rc == 3
        err = capsys.readouterr().err
        assert "not valid YAML" in err
        assert "Traceback" not in err

    def test_pyyaml_absent_degrades_gracefully(
        self, tmp_path: Path, checker, capsys, monkeypatch
    ) -> None:
        """With PyYAML unavailable, structural validation is skipped (a clean
        note, not a ModuleNotFoundError traceback) and the sentinel-only result
        stands -- the gate never crashes a dependency-bare CI."""
        import builtins

        real_import = builtins.__import__

        def _no_yaml(name, *args, **kwargs):
            if name == "yaml":
                raise ImportError("simulated: PyYAML not installed")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", _no_yaml)

        mapping = tmp_path / "model-selection-mapping.yml"
        # A filled mapping that is ALSO malformed YAML: with PyYAML absent the
        # structural check is skipped, so this still PASSES (sentinel-only) --
        # proving the dependency is genuinely optional, not silently enforced.
        mapping.write_text("mapping: [unclosed\n")
        rc = checker.check_mapping(mapping, quiet=False)
        assert rc == 0, "PyYAML-absent must degrade to sentinel-only pass"
        err = capsys.readouterr().err
        assert "structural validation skipped" in err
        assert "PyYAML not installed" in err


# ---------------------------------------------------------------------------
# Interactive capture (foldback #2): fill the stub at install so the gate ships
# green; non-interactive / CI keeps the FILL ME stub fallback.
# ---------------------------------------------------------------------------

def _seed_stub(target: Path) -> Path:
    """Seed the FILL-ME stub at its install destination under *target*."""
    mapping = target / "dev" / ".cairn" / "model-selection-mapping.yml"
    mapping.parent.mkdir(parents=True, exist_ok=True)
    mapping.write_text(_STUB_SRC.read_text(encoding="utf-8"), encoding="utf-8")
    return mapping


class TestInteractiveCapture:
    def test_capture_fills_stub_and_greens_gate(self, tmp_path: Path) -> None:
        checker = _load_checker()
        mapping = _seed_stub(tmp_path)
        # high tier filled; medium + low skipped (blank model).
        answers = iter(["vendor-a/flagship", "2025-06-01", "strategy",
                        "bench Jun 2025", "", ""])
        wrote = capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: next(answers), interactive=True,
            today="2025-06-12")
        assert wrote is True
        assert "FILL ME" not in mapping.read_text()
        assert checker.check_mapping(mapping, quiet=True) == 0, (
            "captured mapping must pass the fidelity gate (green)"
        )

    def test_non_interactive_keeps_stub(self, tmp_path: Path) -> None:
        mapping = _seed_stub(tmp_path)
        assert capture_model_selection_mapping(
            tmp_path, interactive=False) is False
        assert "FILL ME" in mapping.read_text(), "non-interactive must keep stub"

    def test_idempotent_on_already_filled(self, tmp_path: Path) -> None:
        mapping = _seed_stub(tmp_path)
        answers = iter(["vendor/x", "2025-01-01", "general", "src", "", ""])
        assert capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: next(answers), interactive=True) is True
        before = mapping.read_text()
        # Second run sees no FILL ME -> no-op, never clobbers a real mapping.
        assert capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: "unused", interactive=True) is False
        assert mapping.read_text() == before

    def test_skip_every_tier_keeps_stub(self, tmp_path: Path) -> None:
        mapping = _seed_stub(tmp_path)
        assert capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: "", interactive=True) is False
        assert "FILL ME" in mapping.read_text()

    def test_missing_stub_is_noop(self, tmp_path: Path) -> None:
        # No stub seeded -- capture must no-op (never create one from nothing).
        assert capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: "x", interactive=True) is False

    def test_special_chars_quoted_and_valid(self, tmp_path: Path) -> None:
        """A model / source carrying YAML-special characters (':') is
        double-quoted, so the written mapping still parses + passes the
        structural gate."""
        checker = _load_checker()
        mapping = _seed_stub(tmp_path)
        answers = iter(["vendor:flagship-v2", "2025-06-01", "strategy: review",
                        "price: $15/1M", "", ""])
        wrote = capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: next(answers), interactive=True,
            today="2025-06-12")
        assert wrote is True
        assert checker.check_mapping(mapping, quiet=True) == 0

    def test_full_noninteractive_scaffold_keeps_stub(self, tmp_path: Path) -> None:
        """The CLI wiring: a full scaffold install in a non-TTY test run leaves
        the FILL ME stub (the gate then flags it)."""
        assert _scaffold(tmp_path) == 0
        mapping = tmp_path / "dev" / ".cairn" / "model-selection-mapping.yml"
        assert mapping.is_file() and "FILL ME" in mapping.read_text()
