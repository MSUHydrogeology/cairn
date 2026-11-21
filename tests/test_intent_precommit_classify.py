"""The pre-commit installer's refusal of an existing shell hook (defect arc C,
chunk C2).

Driven through ``intent.py install-precommit`` on a disposable git repository:
an existing shell pre-commit hook that is not ours is refused and left
unchanged (exit 4). The refusal label is ``non-executable`` where the file has
an execute bit to test (POSIX) and ``foreign`` on Windows, where Git for
Windows runs shell hooks through its own shell and files have no execute bit.

Run from the repository root:
    python -m pytest tests/test_intent_precommit_classify.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tests._repo_root import repository_root

CAIRN_ROOT = repository_root(Path(__file__))
INTENT_SRC = CAIRN_ROOT / "templates" / "modules" / "team-gated" / "intent.py"
ENGINE_SRC = CAIRN_ROOT / "templates" / "modules" / "team-gated" / "_intent"

pytestmark = pytest.mark.skipif(
    not INTENT_SRC.exists() or not ENGINE_SRC.is_dir(),
    reason="team-gated intent tool not available",
)


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(root), check=True,
                   capture_output=True, text=True)


@pytest.fixture()
def repo(tmp_path: Path, monkeypatch) -> Path:
    root = tmp_path.resolve()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@e.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    (root / "f.txt").write_text("x", encoding="utf-8")
    _git(root, "add", "f.txt")
    _git(root, "commit", "-q", "-m", "init")
    # Install the real intent tool beside a copy of its engine, in this
    # disposable repository, so its ledgers are confined here.
    tools = root / "tools"
    tools.mkdir()
    shutil.copy2(INTENT_SRC, tools / "intent.py")
    shutil.copytree(ENGINE_SRC, tools / "_intent")
    shutil.copy2(CAIRN_ROOT / "dev" / "tools" / "git_read.py", tools / "git_read.py")
    monkeypatch.setenv("CAIRN_AGENT", "owner")
    monkeypatch.chdir(root)
    return root


def test_existing_shell_hook_is_refused_and_left_unchanged(repo):
    hooks = repo / ".git" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    hook = hooks / "pre-commit"
    original = b"#!/bin/sh\necho hello\n"
    hook.write_bytes(original)
    hook.chmod(0o644)

    result = subprocess.run(
        [sys.executable, str(repo / "tools" / "intent.py"), "install-precommit"],
        cwd=repo, capture_output=True, text=True, check=False,
        env=os.environ.copy(),
    )

    assert result.returncode == 4, result.stderr
    assert hook.read_bytes() == original
    expected = "non-executable" if os.name != "nt" else "foreign"
    assert f"existing pre-commit hook looks {expected}" in result.stderr, result.stderr
    assert "no changes made" in result.stderr
