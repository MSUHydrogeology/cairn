"""Session-start skills fan-out self-heal.

The runtime self-heal lives in the session kernel (`templates/skills/_lib/
session.py`, propagated to adopters as `tools/session.py`), *not* in the
SKILL.md prose -- a doc edit cannot make the routine self-heal.  These tests
exercise the **real backend** (`_heal_skills_fanout`, and the full
`session-start` entry point), never scaffold internals, and never a sibling
Cairn checkout: every fixture is a standalone adopter tree under `tmp_path`
carrying only the *installed* `.agents/skills/` + `_data/vendor_targets.yml`.

Matrix:
* absent symlink-tier read-path -> idempotently created;
* already-correct -> preserved (no rewrite);
* wrong symlink -> re-pointed; non-symlink target -> left untouched (never clobbered);
* symlinks unavailable -> gitignored generated copy; divergent copy -> quarantined;
* re-run -> no-op;
* no-Cairn-checkout -> the installed data file alone is sufficient.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_skills_self_heal.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_PATH = CAIRN_ROOT / "templates" / "skills" / "_lib" / "session.py"

pytestmark = pytest.mark.skipif(
    not MODULE_PATH.exists(), reason="session.py template not available"
)


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cairn_lifecycle_heal", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lifecycle = _load()

#: A minimal installed vendor table: one alias tier (free) + the one symlink
#: tier (Claude Code) that needs fan-out -- exactly the shipped shape.
_VENDOR_TABLE = {
    "targets": [
        {"target": "agents-native", "tier": "alias", "path": ".agents/skills"},
        {"target": "claude-code", "tier": "symlink", "path": ".claude/skills"},
    ]
}


def _adopter_tree(root: Path) -> Path:
    """A standalone adopter tree: canonical skills + installed vendor table.

    No sibling Cairn checkout exists -- this *is* the no-Cairn-checkout fixture.
    """
    canon = root / ".agents" / "skills"
    (canon / "session-start").mkdir(parents=True)
    (canon / "session-start" / "SKILL.md").write_text(
        "---\nname: session-start\n---\nbody\n", encoding="utf-8"
    )
    (canon / "_data").mkdir(parents=True)
    (canon / "_data" / "vendor_targets.yml").write_text(
        json.dumps(_VENDOR_TABLE), encoding="utf-8"
    )
    return root


def _claude_skills(root: Path) -> Path:
    return root / ".claude" / "skills"


# --- symlink tier ------------------------------------------------------------


def test_absent_read_path_is_created(tmp_path):
    root = _adopter_tree(tmp_path.resolve())
    (root / ".claude").mkdir()  # harness in use
    rows = lifecycle._heal_skills_fanout(root)
    assert rows == [("claude-code", "symlink", "linked")]
    link = _claude_skills(root)
    assert link.is_symlink()
    assert (link / "session-start" / "SKILL.md").is_file()  # resolves to canonical


def test_harness_not_in_use_is_a_noop(tmp_path):
    root = _adopter_tree(tmp_path.resolve())
    # no .claude/ dir -> light "is this harness in use?" gate says no
    assert lifecycle._heal_skills_fanout(root) == []
    assert not _claude_skills(root).exists()


def test_rerun_is_idempotent(tmp_path):
    root = _adopter_tree(tmp_path.resolve())
    (root / ".claude").mkdir()
    lifecycle._heal_skills_fanout(root)
    rows = lifecycle._heal_skills_fanout(root)
    assert rows == [("claude-code", "symlink", "already-linked")]


def test_wrong_symlink_is_repointed(tmp_path):
    root = _adopter_tree(tmp_path.resolve())
    (root / ".claude").mkdir()
    os.symlink("../somewhere-else", _claude_skills(root))
    rows = lifecycle._heal_skills_fanout(root)
    assert rows == [("claude-code", "symlink", "relinked")]
    assert os.readlink(_claude_skills(root)) == os.path.join("..", ".agents", "skills")


def test_nonsymlink_target_is_left_untouched(tmp_path):
    root = _adopter_tree(tmp_path.resolve())
    link = _claude_skills(root)
    link.mkdir(parents=True)
    (link / "local.txt").write_text("hand-made", encoding="utf-8")
    rows = lifecycle._heal_skills_fanout(root)
    assert rows == [("claude-code", "symlink", "exists-nonsymlink")]
    assert not link.is_symlink() and (link / "local.txt").read_text() == "hand-made"


# --- copy tier (symlinks unavailable: Windows-without-Developer-Mode) ---------


def test_copy_fallback_when_symlinks_unavailable(tmp_path, monkeypatch):
    root = _adopter_tree(tmp_path.resolve())
    (root / ".claude").mkdir()
    monkeypatch.setattr(lifecycle, "_skill_symlinks_available", lambda _r: False)
    rows = lifecycle._heal_skills_fanout(root)
    assert rows == [("claude-code", "copy", "copied")]
    copied = _claude_skills(root) / "session-start" / "SKILL.md"
    assert copied.is_file() and not copied.is_symlink()
    # copy-mode copies are gitignored supply-chain artifacts
    assert ".claude/skills/" in (root / ".gitignore").read_text()


def test_copy_seed_does_not_duplicate_an_existing_dir_ignore(tmp_path, monkeypatch):
    """A repo that already ignores the path (without a
    trailing slash) must not get a duplicate ``.claude/skills/`` appended -- the
    routine must never dirty a tree it just reported clean."""
    root = _adopter_tree(tmp_path.resolve())
    (root / ".claude").mkdir()
    (root / ".gitignore").write_text(".claude/skills\n", encoding="utf-8")
    monkeypatch.setattr(lifecycle, "_skill_symlinks_available", lambda _r: False)
    lifecycle._heal_skills_fanout(root)
    assert (root / ".gitignore").read_text() == ".claude/skills\n"  # byte-for-byte


def test_copy_rerun_is_current_noop(tmp_path, monkeypatch):
    root = _adopter_tree(tmp_path.resolve())
    (root / ".claude").mkdir()
    monkeypatch.setattr(lifecycle, "_skill_symlinks_available", lambda _r: False)
    lifecycle._heal_skills_fanout(root)
    rows = lifecycle._heal_skills_fanout(root)
    assert rows == [("claude-code", "copy", "current")]


def test_divergent_copy_is_quarantined_not_clobbered(tmp_path, monkeypatch):
    root = _adopter_tree(tmp_path.resolve())
    (root / ".claude").mkdir()
    monkeypatch.setattr(lifecycle, "_skill_symlinks_available", lambda _r: False)
    lifecycle._heal_skills_fanout(root)
    # tamper with the generated copy
    copied = _claude_skills(root) / "session-start" / "SKILL.md"
    copied.write_text("TAMPERED / locally edited\n", encoding="utf-8")
    rows = lifecycle._heal_skills_fanout(root)
    assert rows == [("claude-code", "copy", "diverged-quarantined")]
    # stray bytes preserved, canonical bytes regenerated as the active read-path
    bak = copied.with_name(copied.name + ".diverged.bak")
    assert bak.read_text() == "TAMPERED / locally edited\n"
    assert "name: session-start" in copied.read_text()


# --- containment --------------------------------------------------------------


def test_symlinked_parent_is_refused(tmp_path):
    root = _adopter_tree(tmp_path.resolve())
    outside = tmp_path.resolve() / "outside"
    outside.mkdir()
    # .claude is a symlink to an out-of-tree dir; fan-out through it must refuse
    os.symlink(outside, root / ".claude")
    with pytest.raises(lifecycle.LifecycleError):
        lifecycle._heal_skills_fanout(root)


# --- the real session-start entry point --------------------------------------


def _init_repo(root: Path) -> None:
    for args in (
        ("init", "-q"),
        ("config", "user.email", "t@example.com"),
        ("config", "user.name", "T"),
        ("config", "commit.gpgsign", "false"),
    ):
        subprocess.run(["git", *args], cwd=str(root), check=True, capture_output=True)
    (root / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "add", "f.txt"], cwd=str(root), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "initial"], cwd=str(root), check=True, capture_output=True
    )


def test_real_session_start_heals_read_path(tmp_path, monkeypatch, capsys):
    """The read-path appears from a real `session-start` run -- not a unit call
    of the writer, and with no sibling Cairn checkout present."""
    root = _adopter_tree(tmp_path.resolve())
    _init_repo(root)
    (root / ".claude").mkdir()
    monkeypatch.chdir(root)
    rc = lifecycle.main(["session-start"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "skills fan-out self-heal" in out
    link = _claude_skills(root)
    assert link.is_symlink() and (link / "session-start" / "SKILL.md").is_file()
