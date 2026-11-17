"""Public install and Git behavior for the shipped root attributes file."""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import scaffold as s  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"
ATTRS = TEMPLATES_ROOT / "core" / "gitattributes.txt"
EXPECTED_TEMPLATE = b"""# Line endings. Text files are stored and checked out with LF on every machine,
# so a Windows checkout matches the repository and Cairn's recorded file hashes.
# Cairn installs this file only when the project has none, and never replaces
# yours. Edit the project choices below.
* text=auto eol=lf

# Windows scripts keep CRLF. Name only paths Cairn does not install, because
# Cairn records the hash of each installed file's LF bytes.
*.bat text eol=crlf
*.cmd text eol=crlf

# Binary files are never converted.
*.png binary
*.jpg binary
*.gif binary
*.pdf binary
*.zip binary
*.gz binary
*.tif binary
*.nc binary
*.h5 binary
*.npy binary

# Project choices: Cairn cannot know your paths. Uncomment and edit.
# Data and evidence that must stay byte for byte (raw instrument output):
# *.csv -text
# *.dat -text
# Files a Windows tool requires with CRLF:
# *.sln text eol=crlf
# *.reg text eol=crlf
"""


def _install(target: Path, extra: list[str] | None = None) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: Demo\ntest_command: pytest\npreset: solo-greenfield\n",
        encoding="utf-8",
    )
    return s.main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev", *(extra or []),
    ])


def _git(target: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return subprocess.run(
        ["git", *args], cwd=target, env=env, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )


def test_fresh_install_writes_the_file_and_records_it(tmp_path: Path) -> None:
    target = tmp_path.resolve()
    assert _install(target) == 0
    content = ATTRS.read_bytes()
    assert content == EXPECTED_TEMPLATE
    assert (target / ".gitattributes").read_bytes() == content
    rows = [r for r in s.read_lockfile(target)["files"]
            if r["dst"] == ".gitattributes"]
    assert len(rows) == 1
    row = rows[0]
    assert row["verbatim"] is True
    assert row["living_state"] is True
    assert "base_cache" not in row
    assert row["hash"] == "sha256:" + hashlib.sha256(content).hexdigest()


def test_an_existing_different_file_is_kept_byte_for_byte(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    cases = [([], EXPECTED_TEMPLATE.replace(b"\n", b"\r\n")),
             (["--force"], b"# mine\n*.dat -text\n")]
    for index, (extra, existing) in enumerate(cases):
        target = (tmp_path / str(index)).resolve()
        target.mkdir(parents=True, exist_ok=True)
        (target / ".gitattributes").write_bytes(existing)
        assert _install(target, extra) == 0
        assert (target / ".gitattributes").read_bytes() == existing
        lock_path = target / "dev" / ".cairn" / "cairn-lock.yml"
        assert lock_path.is_file()
        destinations = {r["dst"] for r in s.read_lockfile(target)["files"]}
        assert {"AGENTS.md", "tools/board.py"} <= destinations
        assert ".gitattributes" not in destinations
        stderr = capsys.readouterr().err
        expected = [line for line in EXPECTED_TEMPLATE.decode("utf-8").splitlines()
                    if line.strip() and not line.lstrip().startswith("#")]
        assert all(line in stderr for line in expected)


def test_no_other_differing_file_gets_the_exemption(tmp_path: Path) -> None:
    target = tmp_path.resolve()
    target.mkdir(parents=True, exist_ok=True)
    (target / "tools").mkdir()
    (target / "tools" / "board.py").write_bytes(b"planted\n")
    (target / "NOTICE.md").write_bytes(b"planted\n")
    (target / ".gitattributes").write_bytes(b"# mine\n")
    assert _install(target) == 0
    assert (target / "tools" / "board.py").read_bytes() == b"planted\n"
    assert (target / ".gitattributes").read_bytes() == b"# mine\n"
    assert not (target / "dev" / ".cairn" / "cairn-lock.yml").exists()
