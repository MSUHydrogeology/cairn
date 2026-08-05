"""Literal selection-contract pins for the default security stance."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import expand_preset, format_profile_summary, main  # noqa: E402
from bootstrap._scaffold.config import token_gated_modules  # noqa: E402

PRESETS = ("solo-greenfield", "collaborative-team", "high-rigor-legacy")


def _write_profile(path: Path, body: str) -> Path:
    path.write_text(
        "project_name: security-test\n"
        "test_command: pytest\n"
        + body,
        encoding="utf-8",
    )
    return path


def _install(tmp_path: Path, body: str) -> tuple[int, Path]:
    cfg = _write_profile(tmp_path / "profile.yml", body)
    target = tmp_path / "target"
    target.mkdir()
    rc = main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])
    return rc, target


@pytest.mark.parametrize("preset", PRESETS)
def test_content_security_is_in_every_shipped_preset_roster(preset: str) -> None:
    modules, _summary = expand_preset({"preset": preset})
    assert "content-security" in modules


def test_content_security_reaches_the_no_key_default_shape(tmp_path: Path) -> None:
    rc, target = _install(tmp_path, "")
    assert rc == 0
    assert (target / "scripts" / "content_scan.py").is_file()


def test_an_exact_modules_list_is_never_widened_by_the_default_on_module(
        tmp_path: Path) -> None:
    rc, target = _install(tmp_path, "modules:\n  - claim-check\n")
    assert rc == 0
    assert not (target / "scripts" / "content_scan.py").exists()
    assert not (target / "dev" / "modules" / "content-security.md").exists()


def test_modules_empty_list_opts_out_entirely(tmp_path: Path) -> None:
    rc, target = _install(tmp_path, "python_package: mypkg\nmodules: []\n")
    assert rc == 0
    assert not (target / "scripts" / "content_scan.py").exists()
    assert not (target / "scripts" / "run_security_audit.py").exists()


def test_python_security_is_selected_when_the_token_is_declared(
        tmp_path: Path) -> None:
    rc, target = _install(
        tmp_path, "preset: solo-greenfield\npython_package: mypkg\n")
    assert rc == 0
    assert (target / "scripts" / "run_security_audit.py").is_file()


def test_python_security_is_absent_without_the_token(tmp_path: Path) -> None:
    rc, target = _install(tmp_path, "preset: solo-greenfield\n")
    assert rc == 0
    assert not (target / "scripts" / "run_security_audit.py").exists()


def test_the_token_gate_does_not_override_modules_remove() -> None:
    modules, _summary = expand_preset({
        "preset": "solo-greenfield",
        "python_package": "mypkg",
        "modules_remove": ["python-security"],
    })
    assert "python-security" not in modules


def test_content_security_opts_out_loudly() -> None:
    modules, summary = expand_preset({
        "preset": "solo-greenfield",
        "modules_remove": ["content-security"],
    })
    assert "content-security" not in modules
    assert summary["removed_default_on"] == ["content-security"]


@pytest.mark.parametrize("value", ["{{python_package}}", "   "])
def test_an_unfilled_python_package_token_does_not_select(value: str) -> None:
    assert token_gated_modules({"python_package": value}) == []


def test_the_profile_summary_names_the_token_gated_addition() -> None:
    summary = format_profile_summary({
        "preset": "solo-greenfield", "python_package": "mypkg",
    })
    assert (
        "Token-gated (selected by a declared token): python-security"
        in summary
    )


def test_a_declared_token_never_conscripts_a_module_into_an_exact_list(
        tmp_path: Path) -> None:
    rc, target = _install(
        tmp_path,
        "python_package: mypkg\nmodules:\n  - claim-check\n",
    )
    assert rc == 0
    assert not (target / "scripts" / "run_security_audit.py").exists()


def test_a_new_default_on_module_stays_opt_in_for_an_existing_adopter(
        tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    rc, target = _install(tmp_path, "modules:\n  - claim-check\n")
    assert rc == 0
    capsys.readouterr()
    rc = main([
        "upgrade", "--plan", "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT),
    ])
    captured = capsys.readouterr()
    assert rc == 0
    output = captured.out + captured.err
    assert "new modules available (opt-in)" in output
    assert "content-security" in output
    assert not (target / "scripts" / "content_scan.py").exists()
