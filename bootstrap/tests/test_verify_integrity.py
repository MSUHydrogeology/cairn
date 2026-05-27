"""Tests for the lockfile-backed install-integrity check (security-hardening
Chunk 12 / R10).

``bootstrap/verify_integrity.py`` recomputes each lockfile-recorded file's
SHA-256 against the on-disk tree and **fails closed** on any mismatch /
missing file / absent lockfile -- detecting a post-install modification of a
shipped file without trusting the file to vouch for itself.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import verify_integrity  # noqa: E402
from bootstrap.scaffold import main, read_lockfile  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _install(target: Path) -> int:
    cfg = target / "profile.yml"
    cfg.write_text("project_name: VI\ntest_command: pytest\nmodules: []\n")
    return main(["--config", str(cfg), "--target", str(target),
                 "--cairn-root", str(CAIRN_ROOT), "--allow-dev"])


def test_clean_install_verifies(tmp_path: Path) -> None:
    assert _install(tmp_path) == 0
    assert (tmp_path / "dev" / "cairn-lock.yml").is_file()
    assert verify_integrity.verify(tmp_path) == 0


def test_tampered_file_fails_closed(tmp_path: Path) -> None:
    assert _install(tmp_path) == 0
    lock = read_lockfile(tmp_path)
    target_file = tmp_path / lock["files"][0]["dst"]
    target_file.write_text(
        target_file.read_text(encoding="utf-8") + "\n<!-- tampered -->\n",
        encoding="utf-8")
    assert verify_integrity.verify(tmp_path) == 1


def test_missing_file_fails_closed(tmp_path: Path) -> None:
    assert _install(tmp_path) == 0
    lock = read_lockfile(tmp_path)
    (tmp_path / lock["files"][0]["dst"]).unlink()
    assert verify_integrity.verify(tmp_path) == 1


def test_absent_lockfile_fails_closed(tmp_path: Path) -> None:
    # A target with no lockfile cannot attest integrity -> fail closed.
    assert verify_integrity.verify(tmp_path) == 1
