"""Session-start fixes for a first session (defect arc C, chunk C1).

Driven through ``session.py``'s ``main(["session-start"])`` on a disposable git
repository:

* a README in ``dev/proposals/`` or ``dev/plans/`` (any letter case) is not
  listed as open work; a real proposal or plan still is;
* on Windows the ``interpreter:`` line prints forward slashes, never ``\\x5c``;
* the ``.gitignore`` seed for the copy-mode skills folder is left alone when a
  broader rule already covers ``.claude/``, and still written otherwise, and
  when the file has a ``!`` line.

Run from the repository root:
    python -m pytest tests/test_session_first_session.py
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

from tests._repo_root import repository_root

CAIRN_ROOT = repository_root(Path(__file__))
MODULE_PATH = CAIRN_ROOT / "templates" / "skills" / "_lib" / "session.py"

pytestmark = pytest.mark.skipif(
    not MODULE_PATH.exists(), reason="session kernel template not available"
)


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cairn_lifecycle_c1", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lifecycle = _load()


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
    monkeypatch.delenv("CAIRN_HANDOFF_OWNER", raising=False)
    monkeypatch.setenv("CAIRN_AGENT", "owner")
    monkeypatch.chdir(root)
    return root


@pytest.fixture()
def copy_mode_repo(repo: Path, monkeypatch) -> Path:
    """A repository where the skills fan-out uses the copy tier, as on a host
    without symlink rights, with one symlink-tier row for ``.claude/skills``."""
    canonical = repo / ".agents" / "skills"
    (canonical / "session-start").mkdir(parents=True)
    (canonical / "session-start" / "SKILL.md").write_text("skill\n", encoding="utf-8")
    data = canonical / "_data"
    data.mkdir()
    (data / "vendor_targets.yml").write_text(
        '{"targets": [{"target": "claude", "tier": "symlink", '
        '"path": ".claude/skills"}]}\n',
        encoding="utf-8",
    )
    (repo / ".claude").mkdir()
    monkeypatch.setattr(lifecycle, "_skill_symlinks_available", lambda root: False)
    return repo


def _plan_lines(out: str) -> list[str]:
    return [ln for ln in out.splitlines()
            if "proposals/" in ln or "plans/" in ln]


# --- (a) README files are not open work --------------------------------------


@pytest.mark.parametrize("readme", ["README.md", "readme.md", "Readme.md"])
def test_readme_in_proposals_and_plans_is_not_listed(repo, readme, capsys):
    (repo / "dev" / "proposals").mkdir(parents=True)
    (repo / "dev" / "plans").mkdir(parents=True)
    (repo / "dev" / "proposals" / readme).write_text(
        "**Status**: awaiting-review\n", encoding="utf-8")
    (repo / "dev" / "plans" / readme).write_text(
        "**Status**: implementing\n", encoding="utf-8")
    real = repo / "dev" / "plans" / "2026-01-01-real-plan.md"
    real.write_text("**Status**: implementing\n", encoding="utf-8")

    rc = lifecycle.main(["session-start"])
    out = capsys.readouterr().out

    assert rc == 0
    lines = _plan_lines(out)
    assert any("2026-01-01-real-plan.md" in ln for ln in lines), out
    assert not any("readme" in ln.lower() for ln in lines), lines


# --- (b) Windows paths print with forward slashes -----------------------------


def test_encode_display_still_escapes_a_backslash_in_text(repo):
    # The encoder itself is unchanged: a backslash in child or table text
    # stays an escape on every platform.
    assert lifecycle.encode_display("a\\b") == "a\\x5cb"


@pytest.mark.skipif(os.name != "nt", reason="backslash path separators are Windows only")
def test_interpreter_line_prints_forward_slashes_on_windows(repo, capsys):
    rc = lifecycle.main(["session-start"])
    out = capsys.readouterr().out

    assert rc == 0
    line = next(ln for ln in out.splitlines() if "interpreter: " in ln)
    assert "\\x5c" not in line, line
    shown = line.split("interpreter: ", 1)[1].split("  (from", 1)[0]
    assert "\\" not in shown, line


# --- (c) the .gitignore seed for the copy-mode skills folder ------------------


def test_gitignore_already_covered_by_claude_rule_is_left_byte_identical(
        copy_mode_repo, capsys):
    gitignore = copy_mode_repo / ".gitignore"
    raw = b"*.log\r\n.claude/\r\n"
    gitignore.write_bytes(raw)

    rc = lifecycle.main(["session-start"])
    capsys.readouterr()

    assert rc == 0
    assert gitignore.read_bytes() == raw


def test_gitignore_with_unrelated_rule_gets_the_skills_line(copy_mode_repo, capsys):
    gitignore = copy_mode_repo / ".gitignore"
    gitignore.write_bytes(b"*.log\n")

    rc = lifecycle.main(["session-start"])
    capsys.readouterr()

    assert rc == 0
    assert gitignore.read_bytes() == b"*.log\n.claude/skills/\n"


def test_gitignore_with_negation_line_gets_the_skills_line(copy_mode_repo, capsys):
    gitignore = copy_mode_repo / ".gitignore"
    gitignore.write_bytes(b".claude/\n!.claude/skills/\n")

    rc = lifecycle.main(["session-start"])
    capsys.readouterr()

    assert rc == 0
    assert gitignore.read_bytes() == b".claude/\n!.claude/skills/\n.claude/skills/\n"
