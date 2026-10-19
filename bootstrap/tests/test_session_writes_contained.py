"""The session kernel never writes through a link or outside the project.

A checkout is data a reviewer reads as harmless: a link, a folder, a row in the
vendor table.  The kernel (`templates/skills/_lib/session.py`, installed as
`tools/session.py`) is Cairn's own unmodified code, so every write it makes has to
stay inside the project and must not follow a link, whatever those files say.
Each test here uses only such project data.  Every test builds a standalone
adopter tree under `tmp_path`, loads the template copy of the kernel, and checks
the files it must not have touched.

The ordinary behaviour of the skills fan-out self-heal (what is linked, copied,
quarantined, left alone) is pinned in `test_skills_self_heal.py`; this file pins
what the kernel refuses.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_session_writes_contained.py
"""
from __future__ import annotations

import ast
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_PATH = CAIRN_ROOT / "templates" / "skills" / "_lib" / "session.py"

pytestmark = pytest.mark.skipif(
    not MODULE_PATH.exists(), reason="session.py template not available"
)


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cairn_session_contained", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lifecycle = _load()

#: A minimal installed vendor table: one alias tier (free) + the one symlink tier.
_VENDOR_TABLE = {
    "targets": [
        {"target": "agents-native", "tier": "alias", "path": ".agents/skills"},
        {"target": "claude-code", "tier": "symlink", "path": ".claude/skills"},
    ]
}


def _adopter_tree(root: Path) -> Path:
    """A standalone adopter tree: canonical skills + installed vendor table."""
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


_STAND_IN_TEXT = "# a shell startup file, outside the project\n"


def _stand_in(tmp_path: Path) -> Path:
    """A file outside the project, standing in for a shell startup file."""
    outside = tmp_path.resolve() / "outside"
    outside.mkdir(exist_ok=True)
    path = outside / "startup-file"
    path.write_text(_STAND_IN_TEXT, encoding="utf-8")
    return path


def _project(tmp_path: Path, monkeypatch, rows=None, *, copy_mode: bool = True) -> Path:
    """An adopter tree under ``tmp_path/proj`` with the harness folder present.

    ``copy_mode`` forces the copy path directly; the tests that need the route a
    checkout really uses leave it off and plant the folder instead.
    """
    root = _adopter_tree(tmp_path.resolve() / "proj")
    (root / ".claude").mkdir()
    if rows is not None:
        (root / ".agents" / "skills" / "_data" / "vendor_targets.yml").write_text(
            json.dumps({"targets": rows}), encoding="utf-8"
        )
    if copy_mode:
        monkeypatch.setattr(lifecycle, "_skill_symlinks_available", lambda _r: False)
    return root


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(root), check=True, capture_output=True)


_CLAUDE_ROW = {"target": "claude-code", "tier": "symlink", "path": ".claude/skills"}

#: Text a vendor row could carry to make the appended line do something else:
#: a second line, a shell substitution, a glob, a comment, a negation.
_HOSTILE_VENDOR_PATHS = {
    "substitution": "$(touch MARKER)/skills",
    "backticks": "`touch MARKER`/skills",
    "semicolon": ".claude;touch/skills",
    "newline": ".claude\ntouch MARKER/skills",
    "carriage-return": ".claude\rtouch MARKER/skills",
    "config-stanza": "zz\n[core]\nfsmonitor = touch MARKER\n#/skills",
    "space": ".cl aude/skills",
    "glob": ".cl*/skills",
    "negation": "!.claude/skills",
    "comment": "#.claude/skills",
    "backslash": ".cl\\aude/skills",
    "escape-byte": ".claude\x1b[31m/skills",
    "current-dir": "./.claude/skills",
    "empty-part": ".claude//skills",
    "project-root": ".",
    "newline-only": ".claude/a\nb/skills",
    "carriage-return-only": ".claude/a\rb/skills",
    "leading-newline": "\n.claude/skills",
    "harness-folder-itself": ".claude",
    "one-name": "skills",
}


@pytest.mark.parametrize("name", sorted(_HOSTILE_VENDOR_PATHS))
def test_a_vendor_row_cannot_choose_the_text_appended_to_gitignore(
    tmp_path, monkeypatch, capsys, name
):
    path = _HOSTILE_VENDOR_PATHS[name]
    root = _project(tmp_path, monkeypatch, rows=[{**_CLAUDE_ROW, "path": path}])
    parent = (root / path).parent
    if parent != root:
        parent.mkdir(parents=True, exist_ok=True)  # the row's harness folder exists
    assert lifecycle._heal_skills_fanout(root) == []
    assert not (root / ".gitignore").exists()
    assert "unsafe vendor path" in capsys.readouterr().err


@pytest.mark.parametrize("name", sorted(_HOSTILE_VENDOR_PATHS))
def test_the_gitignore_writer_itself_refuses_a_hostile_entry(tmp_path, name):
    """The writer does not rely on its caller having validated the entry."""
    root = tmp_path.resolve()
    entry = _HOSTILE_VENDOR_PATHS[name].rstrip("/") + "/"
    with pytest.raises(lifecycle.LifecycleError):
        lifecycle._seed_skill_gitignore(root, entry)
    assert not (root / ".gitignore").exists()


@pytest.mark.parametrize(
    "path",
    [".git", ".claude", ".git/skills", ".claude/.GIT/skills", ".claude/.git./skills",
     ".claude/.git/skills", "dev/.cairn/skills", "Dev/.Cairn/skills", "dev/.cairn./skills"],
)
def test_a_vendor_row_cannot_aim_the_copy_at_a_place_the_project_must_not_fill(
    tmp_path, monkeypatch, capsys, path
):
    """Copy mode copies every canonical file into the row's folder.  A row that
    named ``.git`` would replace ``.git/config``; one that named ``dev/.cairn``
    would write the interpreter binding; one that named the harness folder itself
    could write its untracked local settings.  None of those is the project's to fill."""
    root = _project(tmp_path, monkeypatch, rows=[{**_CLAUDE_ROW, "path": path}])
    canon = root / ".agents" / "skills"
    for name in ("config", "local-env.json", "pre-commit", "settings.local.json"):
        (canon / name).write_text('{"planted": true}\n', encoding="utf-8")
    (root / ".git" / "hooks").mkdir(parents=True)
    (root / ".git" / "config").write_text("[core]\n", encoding="utf-8")
    (root / ".claude" / ".git").mkdir()
    (root / ".claude" / ".GIT").mkdir(exist_ok=True)
    (root / ".claude" / ".git.").mkdir(exist_ok=True)
    (root / ".claude" / "settings.local.json").write_text("{}\n", encoding="utf-8")
    (root / "dev" / ".cairn" / "x").mkdir(parents=True)
    before = sorted(str(p.relative_to(root)) for p in root.rglob("*") if ".agents" not in p.parts)
    assert lifecycle._heal_skills_fanout(root) == []
    after = sorted(str(p.relative_to(root)) for p in root.rglob("*") if ".agents" not in p.parts)
    assert after == before
    assert (root / ".git" / "config").read_text(encoding="utf-8") == "[core]\n"
    assert (root / ".claude" / "settings.local.json").read_text(encoding="utf-8") == "{}\n"
    assert "unsafe vendor path" in capsys.readouterr().err


def _plant_gitignore_link(root: Path, stand_in: Path, kind: str) -> Path:
    """Make ``root/.gitignore`` a link; return the file the link ends at."""
    gitignore = root / ".gitignore"
    if kind == "absolute":
        os.symlink(stand_in, gitignore)
    elif kind == "relative":
        os.symlink(os.path.relpath(stand_in, root), gitignore)
    elif kind == "chain":
        os.symlink(stand_in, root / "hop")
        os.symlink("hop", gitignore)
    elif kind == "dangling":
        stand_in = stand_in.parent / "not-created-yet"
        os.symlink(stand_in, gitignore)
    elif kind == "inside-the-project":
        (root / "kept-ignore").write_text("*.log\n", encoding="utf-8")
        os.symlink("kept-ignore", gitignore)
        return root / "kept-ignore"
    else:  # pragma: no cover
        raise AssertionError(kind)
    return stand_in


@pytest.mark.parametrize(
    "kind", ["absolute", "relative", "chain", "dangling", "inside-the-project"]
)
def test_a_linked_gitignore_is_refused_before_anything_is_written(
    tmp_path, monkeypatch, kind
):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    target = _plant_gitignore_link(root, _stand_in(tmp_path), kind)
    before = target.read_bytes() if target.exists() else None
    with pytest.raises(lifecycle.LifecycleError, match="link"):
        lifecycle._heal_skills_fanout(root)
    assert (target.read_bytes() if target.exists() else None) == before
    assert (root / ".gitignore").is_symlink()
    # refused before the copy, so the tree is not left half-done
    assert not (root / ".claude" / "skills").exists()


def test_the_link_can_end_at_git_config_and_the_row_can_carry_a_config_stanza(
    tmp_path, monkeypatch
):
    """A line appended to ``.git/config`` makes git run a command, so the link may
    end there; and a folder name can hold newlines, so one row can write several
    lines.  Both together must still write nothing."""
    stanza = "zz\n[core]\n\tfsmonitor = touch MARKER\n#"
    root = _project(
        tmp_path, monkeypatch,
        rows=[_CLAUDE_ROW, {**_CLAUDE_ROW, "target": "other", "path": stanza + "/skills"}],
    )
    (root / stanza).mkdir()
    config = root / ".git" / "config"
    config.parent.mkdir()
    config.write_text("[core]\n\trepositoryformatversion = 0\n", encoding="utf-8")
    os.symlink(".git/config", root / ".gitignore")
    before = config.read_bytes()
    with pytest.raises(lifecycle.LifecycleError, match="link"):
        lifecycle._heal_skills_fanout(root)
    assert config.read_bytes() == before


def test_a_hard_linked_gitignore_is_replaced_not_written_into(tmp_path, monkeypatch):
    """A hard link is a second name for the same bytes; no check can see it, so the
    write has to leave the other name alone."""
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    stand_in = _stand_in(tmp_path)
    try:
        os.link(stand_in, root / ".gitignore")
    except (OSError, NotImplementedError):
        pytest.skip("hard links are not available here")
    lifecycle._heal_skills_fanout(root)
    assert stand_in.read_text(encoding="utf-8") == _STAND_IN_TEXT
    text = (root / ".gitignore").read_text(encoding="utf-8")
    assert text == _STAND_IN_TEXT + ".claude/skills/\n"


def test_the_gitignore_write_replaces_a_link_instead_of_following_it(tmp_path):
    """The check can pass and a link still appear before the write.  The write
    has to be one that cannot follow it, whatever the check did."""
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    stand_in = _stand_in(tmp_path)
    os.symlink(stand_in, root / ".gitignore")
    lifecycle._write_replacing(root / ".gitignore", b".claude/skills/\n")
    assert stand_in.read_text(encoding="utf-8") == _STAND_IN_TEXT
    assert not (root / ".gitignore").is_symlink()
    assert (root / ".gitignore").read_bytes() == b".claude/skills/\n"
    assert [p.name for p in root.iterdir()] == [".gitignore"]  # no temp file left


def test_a_link_swapped_in_after_the_check_is_not_followed(tmp_path, monkeypatch):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    stand_in = _stand_in(tmp_path)
    real = lifecycle._assert_not_linked

    def check_then_swap(dst, base):
        real(dst, base)
        if dst.name == ".gitignore" and not dst.is_symlink():
            dst.unlink(missing_ok=True)
            os.symlink(stand_in, dst)

    monkeypatch.setattr(lifecycle, "_assert_not_linked", check_then_swap)
    with pytest.raises((lifecycle.LifecycleError, OSError)):
        lifecycle._seed_skill_gitignore(root, ".claude/skills/")
    assert stand_in.read_text(encoding="utf-8") == _STAND_IN_TEXT
    # nor was the outside file's content read through the link and copied in
    assert (root / ".gitignore").is_symlink()


@pytest.mark.parametrize("kind", ["folder", "not-utf-8"])
def test_an_unreadable_gitignore_is_refused_not_a_traceback(tmp_path, monkeypatch, kind):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    gitignore = root / ".gitignore"
    if kind == "folder":
        gitignore.mkdir()
        (gitignore / "x").write_text("x", encoding="utf-8")
    else:
        gitignore.write_bytes(b"\xff\xfe not text\n")
    with pytest.raises(lifecycle.LifecycleError):
        lifecycle._heal_skills_fanout(root)
    assert not (root / ".claude" / "skills").exists()
    if kind == "not-utf-8":
        assert gitignore.read_bytes() == b"\xff\xfe not text\n"


def test_seeding_keeps_the_existing_bytes_and_line_endings(tmp_path):
    root = tmp_path.resolve()
    (root / ".gitignore").write_bytes(b"*.log\r\nbuild")  # CRLF, no final newline
    lifecycle._seed_skill_gitignore(root, ".claude/skills/")
    assert (root / ".gitignore").read_bytes() == b"*.log\r\nbuild\r\n.claude/skills/\r\n"
    lifecycle._seed_skill_gitignore(root, ".claude/skills/")  # idempotent
    assert (root / ".gitignore").read_bytes() == b"*.log\r\nbuild\r\n.claude/skills/\r\n"


def test_seeding_keeps_the_permission_bits_of_the_file_it_replaces(tmp_path):
    if os.name == "nt":
        pytest.skip("permission bits are not meaningful here")
    root = tmp_path.resolve()
    gitignore = root / ".gitignore"
    gitignore.write_text("*.log\n", encoding="utf-8")
    gitignore.chmod(0o640)
    lifecycle._seed_skill_gitignore(root, ".claude/skills/")
    assert (gitignore.stat().st_mode & 0o777) == 0o640


# --- copy mode: the files it writes inside the harness folder -----------------


def test_a_link_where_a_copy_would_go_is_refused_before_any_file_is_copied(
    tmp_path, monkeypatch
):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    stand_in = _stand_in(tmp_path)
    created_later = stand_in.parent / "not-created-yet"
    skill = root / ".claude" / "skills" / "session-start"
    skill.mkdir(parents=True)
    os.symlink(created_later, skill / "SKILL.md")  # a link to a file that is not there yet
    with pytest.raises(lifecycle.LifecycleError, match="link"):
        lifecycle._heal_skills_fanout(root)
    assert not created_later.exists()
    # `_data` sorts before `session-start`, so a file-by-file loop would have
    # copied it first; the refusal comes before the first copy.
    assert not (root / ".claude" / "skills" / "_data").exists()


def test_a_link_where_the_quarantine_copy_would_go_is_refused(tmp_path, monkeypatch):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    outside_dir = tmp_path.resolve() / "outside-dir"
    outside_dir.mkdir()
    skill = root / ".claude" / "skills" / "session-start"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("a local edit\n", encoding="utf-8")
    os.symlink(outside_dir, skill / "SKILL.md.diverged.bak")
    with pytest.raises(lifecycle.LifecycleError, match="link"):
        lifecycle._heal_skills_fanout(root)
    assert list(outside_dir.iterdir()) == []
    assert (skill / "SKILL.md").read_text(encoding="utf-8") == "a local edit\n"


def test_a_link_in_the_middle_of_a_copy_path_is_refused(tmp_path, monkeypatch):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    outside_dir = tmp_path.resolve() / "outside-dir"
    outside_dir.mkdir()
    (root / ".claude" / "skills").mkdir()
    os.symlink(outside_dir, root / ".claude" / "skills" / "session-start")
    with pytest.raises(lifecycle.LifecycleError, match="link"):
        lifecycle._heal_skills_fanout(root)
    assert list(outside_dir.iterdir()) == []


def test_a_refusal_names_the_path_without_putting_control_bytes_on_the_terminal(
    tmp_path, monkeypatch, capsys
):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    _init_repo(root)
    awkward = "\x1b]0;retitled\x07.md"
    (root / ".agents" / "skills" / "session-start" / awkward).write_text("x", encoding="utf-8")
    skill = root / ".claude" / "skills" / "session-start"
    skill.mkdir(parents=True)
    os.symlink(tmp_path.resolve() / "elsewhere", skill / awkward)
    monkeypatch.chdir(root)
    assert lifecycle.main(["session-start"]) == 0  # still fail-soft
    out, err = capsys.readouterr()
    assert "refused" in err
    assert "\x1b" not in out + err and "\x07" not in out + err
    assert "\\x1b" in err  # shown as an escape, so the reader can still see it


def test_a_copy_destination_that_is_a_folder_is_refused_not_a_traceback(
    tmp_path, monkeypatch
):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    (root / ".claude" / "skills" / "session-start" / "SKILL.md").mkdir(parents=True)
    with pytest.raises(lifecycle.LifecycleError):
        lifecycle._heal_skills_fanout(root)


# --- the symlink probe --------------------------------------------------------


def test_a_folder_at_the_old_probe_name_cannot_force_the_copy_path(tmp_path):
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    try:
        os.symlink(".", tmp_path / "can-link")
    except (OSError, NotImplementedError):
        pytest.skip("symlinks are not available here")
    folder = root / ".cairn-skill-symlink-probe"
    folder.mkdir()
    (folder / "keep").write_text("x", encoding="utf-8")
    assert lifecycle._skill_symlinks_available(root) is True
    assert (folder / "keep").read_text(encoding="utf-8") == "x"  # not touched
    assert [p.name for p in root.iterdir()] == [folder.name]  # its own probe is gone


# --- the route a checkout really takes: committed data, cloned, session-start ---


def _commit_all(root: Path) -> None:
    _git(root, "init", "-q")
    for key, value in (("user.email", "t@example.com"), ("user.name", "T"),
                       ("commit.gpgsign", "false")):
        _git(root, "config", key, value)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "hostile data only")


@pytest.mark.parametrize("link_to", ["a file outside the clone", ".git/config"])
def test_session_start_in_a_hostile_clone_writes_through_no_link(
    tmp_path, monkeypatch, capsys, link_to
):
    """Committed data only: a linked ``.gitignore``, a non-empty folder at the
    symlink probe's name, a harness folder, and a vendor row whose folder name
    carries config lines.  The kernel is run unmodified, as an agent would."""
    stand_in = _stand_in(tmp_path)
    src = _adopter_tree(tmp_path.resolve() / "src")
    stanza = "zz\n[core]\n\tfsmonitor = touch PWNED-MARKER\n#"
    (src / ".agents" / "skills" / "_data" / "vendor_targets.yml").write_text(
        json.dumps({"targets": [_CLAUDE_ROW, {**_CLAUDE_ROW, "target": "z", "path": stanza + "/skills"}]}),
        encoding="utf-8",
    )
    (src / ".claude").mkdir()
    (src / ".claude" / "keep").write_text("x", encoding="utf-8")
    (src / ".cairn-skill-symlink-probe").mkdir()
    (src / ".cairn-skill-symlink-probe" / "keep").write_text("x", encoding="utf-8")
    (src / stanza).mkdir()
    (src / stanza / "keep").write_text("x", encoding="utf-8")
    os.symlink("../outside/startup-file" if link_to != ".git/config" else ".git/config",
               src / ".gitignore")
    _commit_all(src)
    clone = tmp_path.resolve() / "clone"
    subprocess.run(["git", "clone", "-q", str(src), str(clone)], check=True, capture_output=True)
    assert (clone / ".gitignore").is_symlink()

    guarded = stand_in if link_to != ".git/config" else clone / ".git" / "config"
    before = guarded.read_bytes()
    monkeypatch.chdir(clone)
    rc = lifecycle.main(["session-start"])
    assert guarded.read_bytes() == before
    assert not (clone / "PWNED-MARKER").exists()
    assert rc == 0
    capsys.readouterr()


# --- session-end: the reflections and the handoff lock ------------------------


def _linked_reflections(tmp_path: Path):
    root = tmp_path.resolve() / "proj"
    (root / "dev").mkdir(parents=True)
    notes = tmp_path.resolve() / "notes"
    notes.mkdir()
    (notes / "2020-01-02-an-old-diary-entry.md").write_text("mine\n", encoding="utf-8")
    os.symlink(notes, root / "dev" / "reflections")
    return root, notes


@pytest.mark.parametrize("dry_run", [True, False])
def test_pruning_never_deletes_through_a_linked_reflections_folder(tmp_path, dry_run):
    root, notes = _linked_reflections(tmp_path)
    with pytest.raises(lifecycle.LifecycleError, match="link"):
        lifecycle._prune_reflections(root, 14, dry_run=dry_run)
    assert (notes / "2020-01-02-an-old-diary-entry.md").read_text(encoding="utf-8") == "mine\n"


def test_the_reflection_is_not_written_through_a_linked_folder(tmp_path, monkeypatch, capsys):
    root, notes = _linked_reflections(tmp_path)
    _init_repo(root)
    monkeypatch.chdir(root)
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    monkeypatch.setenv("CAIRN_SESSION", "abc12345")
    assert lifecycle.main(["session-end"]) == 1
    assert "link" in capsys.readouterr().err
    assert [p.name for p in notes.iterdir()] == ["2020-01-02-an-old-diary-entry.md"]


def test_the_handoff_lock_is_not_created_through_a_linked_folder(tmp_path):
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    elsewhere = tmp_path.resolve() / "elsewhere"
    elsewhere.mkdir()
    os.symlink(elsewhere, root / "dev")
    with pytest.raises(lifecycle.LifecycleError, match="link"):
        lifecycle.HandoffLock(root, "owner").acquire()
    assert list(elsewhere.iterdir()) == []


def test_the_handoff_heartbeat_writes_the_file_it_holds_open(tmp_path):
    """The heartbeat refreshes the lease through the descriptor the lock opened
    exclusively, so replacing the file by a link afterwards cannot redirect it."""
    root = tmp_path.resolve() / "proj"
    (root / "dev" / ".cairn").mkdir(parents=True)
    stand_in = _stand_in(tmp_path)
    lock = lifecycle.HandoffLock(root, "owner")
    lock.acquire()
    try:
        lock_file = root / "dev" / ".cairn" / "handoff.lock"
        lock_file.unlink()
        os.symlink(stand_in, lock_file)
        lock.heartbeat()
    finally:
        lock.release()
    assert stand_in.read_text(encoding="utf-8") == _STAND_IN_TEXT


# --- the guard and the write helpers, one property each -----------------------


def test_a_link_to_a_folder_inside_the_project_is_refused_too(tmp_path, monkeypatch):
    """The check does not judge where a link ends: a link in the middle of the
    path is refused even when it points at another folder of the same project."""
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    (root / "elsewhere-in-the-project").mkdir()
    (root / ".claude" / "skills").mkdir()
    os.symlink("../../elsewhere-in-the-project", root / ".claude" / "skills" / "session-start")
    with pytest.raises(lifecycle.LifecycleError, match="link"):
        lifecycle._heal_skills_fanout(root)
    assert list((root / "elsewhere-in-the-project").iterdir()) == []


def test_a_destination_that_climbs_out_of_the_project_is_refused(tmp_path):
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    with pytest.raises(lifecycle.LifecycleError, match="outside the project"):
        lifecycle._assert_not_linked(root / ".." / "elsewhere", root)
    with pytest.raises(lifecycle.LifecycleError, match="outside the project"):
        lifecycle._assert_not_linked(tmp_path.resolve() / "elsewhere", root)
    lifecycle._assert_not_linked(root / "dev" / "reflections" / "x.md", root)  # no error


def test_a_quarantine_name_held_by_a_folder_is_refused_and_nothing_moves(tmp_path, monkeypatch):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    skill = root / ".claude" / "skills" / "session-start"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("a local edit\n", encoding="utf-8")
    (skill / "SKILL.md.diverged.bak").mkdir()
    with pytest.raises(lifecycle.LifecycleError):
        lifecycle._heal_skills_fanout(root)
    assert (skill / "SKILL.md").read_text(encoding="utf-8") == "a local edit\n"
    assert list((skill / "SKILL.md.diverged.bak").iterdir()) == []


def test_the_temporary_file_is_never_a_name_that_is_already_taken(tmp_path, monkeypatch):
    """Whatever already sits at the temporary name -- a link or a plain file -- is
    left alone and the write fails, instead of being opened and written."""
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    stand_in = _stand_in(tmp_path)
    monkeypatch.setattr(lifecycle.secrets, "token_hex", lambda n: "0" * (2 * n))
    taken = root / (".cairn-write-" + "0" * 16)
    os.symlink(stand_in, taken)
    with pytest.raises(OSError):
        lifecycle._write_replacing(root / ".gitignore", b"x\n")
    assert stand_in.read_text(encoding="utf-8") == _STAND_IN_TEXT
    taken.unlink()
    taken.write_text("planted\n", encoding="utf-8")
    with pytest.raises(FileExistsError):
        lifecycle._write_replacing(root / ".gitignore", b"x\n")
    assert taken.read_text(encoding="utf-8") == "planted\n"
    assert not (root / ".gitignore").exists()


def test_a_new_file_is_created_exclusively_never_through_a_link_or_over_a_file(tmp_path):
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    stand_in = _stand_in(tmp_path)
    os.symlink(stand_in, root / "linked.md")
    with pytest.raises(OSError):
        lifecycle._create_text_exclusive(root / "linked.md", "x\n")
    assert stand_in.read_text(encoding="utf-8") == _STAND_IN_TEXT
    (root / "plain.md").write_text("mine\n", encoding="utf-8")
    with pytest.raises(FileExistsError):
        lifecycle._create_text_exclusive(root / "plain.md", "x\n")
    assert (root / "plain.md").read_text(encoding="utf-8") == "mine\n"
    lifecycle._create_text_exclusive(root / "new.md", "fresh\n")
    assert (root / "new.md").read_text(encoding="utf-8") == "fresh\n"


def test_a_link_swapped_in_at_a_copy_destination_after_the_check_is_not_followed(
    tmp_path, monkeypatch
):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    (root / ".claude" / "skills" / "session-start").mkdir(parents=True)
    not_there = _stand_in(tmp_path).parent / "not-created-yet"
    real = lifecycle._assert_not_linked

    def check_then_swap(dst, base):
        real(dst, base)
        if dst.name == "SKILL.md" and not dst.is_symlink() and not dst.exists():
            os.symlink(not_there, dst)

    monkeypatch.setattr(lifecycle, "_assert_not_linked", check_then_swap)
    try:
        lifecycle._heal_skills_fanout(root)
    except (lifecycle.LifecycleError, OSError):
        pass  # failing closed is allowed; writing outside is not
    assert not not_there.exists()


def test_a_link_swapped_in_at_the_quarantine_name_after_the_check_is_not_followed(
    tmp_path, monkeypatch
):
    """The quarantine move is a rename: it replaces a link that appeared at the
    new name instead of moving the file into the folder the link points at."""
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    outside_dir = tmp_path.resolve() / "outside-dir"
    outside_dir.mkdir()
    skills = root / ".claude" / "skills"
    (skills / "_data").mkdir(parents=True)
    (skills / "_data" / "vendor_targets.yml").write_text("a local edit\n", encoding="utf-8")
    real = lifecycle._assert_not_linked

    def check_then_swap(dst, base):
        real(dst, base)
        # `_data/...` sorts first, so by the time the next file is checked the
        # quarantine name for the first one has already passed its own check
        if dst.name == "SKILL.md":
            late = skills / "_data" / "vendor_targets.yml.diverged.bak"
            if not late.is_symlink() and not late.exists():
                os.symlink(outside_dir, late)

    monkeypatch.setattr(lifecycle, "_assert_not_linked", check_then_swap)
    try:
        lifecycle._heal_skills_fanout(root)
    except (lifecycle.LifecycleError, OSError):
        pass
    assert list(outside_dir.iterdir()) == []


def test_the_divergence_warning_carries_no_raw_control_bytes(tmp_path, monkeypatch, capsys):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    awkward = "\x1b]0;retitled\x07.md"
    (root / ".agents" / "skills" / "session-start" / awkward).write_text("canonical\n", encoding="utf-8")
    skill = root / ".claude" / "skills" / "session-start"
    skill.mkdir(parents=True)
    (skill / awkward).write_text("a local edit\n", encoding="utf-8")
    assert lifecycle._heal_skills_fanout(root) == [("claude-code", "copy", "diverged-quarantined")]
    err = capsys.readouterr().err
    assert "diverged" in err
    assert "\x1b" not in err and "\x07" not in err
    assert "\\x1b" in err


def test_a_failed_write_leaves_no_temporary_file_and_keeps_the_old_bytes(tmp_path, monkeypatch):
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    (root / "target").write_bytes(b"old\n")

    def refuse(src, dst):
        raise OSError("replace refused")

    monkeypatch.setattr(lifecycle.os, "replace", refuse)
    with pytest.raises(OSError, match="replace refused"):
        lifecycle._write_replacing(root / "target", b"new\n")
    monkeypatch.undo()
    assert (root / "target").read_bytes() == b"old\n"
    assert [p.name for p in root.iterdir()] == ["target"]


def test_the_fan_out_guard_messages_carry_no_raw_control_bytes(tmp_path):
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    awkward = "n\x1b[31m\x07"
    (root / "real").mkdir()
    os.symlink("real", root / awkward)
    with pytest.raises(lifecycle.LifecycleError) as parent_link:
        lifecycle._assert_fanout_contained(root / awkward / "skills", root)
    with pytest.raises(lifecycle.LifecycleError) as climbs:
        lifecycle._assert_fanout_contained(root / ".." / awkward, root)
    for caught in (parent_link, climbs):
        assert "\x1b" not in str(caught.value) and "\x07" not in str(caught.value)
        assert "\\x1b" in str(caught.value)


# --- a new writer of .gitignore must be looked at -----------------------------

#: The shipped files that build the path ``.gitignore`` as a literal, and why each
#: is allowed.  A new entry is a new writer of a file whose bytes other tools run:
#: it needs the same containment before its first write.
_GITIGNORE_PATH_LITERAL_FILES = {
    "bootstrap/_scaffold/install.py": "seed_gitignore, guarded by _assert_safe_write",
    "templates/skills/_lib/session.py": "_seed_skill_gitignore, guarded here",
    "tools/session.py": "the self-hosted twin of the one above",
    "tools/gauge.py": "a classification table; writes nothing",
}


def test_every_shipped_file_that_names_gitignore_as_a_path_is_accounted_for():
    """A discipline aid, not a gate: it finds a string literal ``".gitignore"`` in
    shipped Python, which is how every writer of the file so far has named it.  A
    writer that builds the name some other way is not seen."""
    found = set()
    for top in ("bootstrap/_scaffold", "scripts", "tools", "templates"):
        for path in sorted((CAIRN_ROOT / top).rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            if any(isinstance(n, ast.Constant) and n.value == ".gitignore"
                   for n in ast.walk(tree)):
                found.add(path.relative_to(CAIRN_ROOT).as_posix())
    assert found == set(_GITIGNORE_PATH_LITERAL_FILES), (
        "a shipped file now names .gitignore as a path (or one stopped): "
        f"{sorted(found ^ set(_GITIGNORE_PATH_LITERAL_FILES))}"
    )


# --- a vendor row names a skills folder, and nothing else ----------------------


@pytest.mark.parametrize(
    "path",
    [".venv/bin/python", ".venv/bin", "dev/reflections", ".claude/commands",
     ".claude/skills-extra", ".claude/skill", ".claude/skills/nested", ".claude/myskills"],
)
@pytest.mark.parametrize("copy_mode", [False, True], ids=["links", "copies"])
def test_a_vendor_row_cannot_replace_or_fill_a_folder_that_is_not_a_skills_folder(
    tmp_path, monkeypatch, capsys, path, copy_mode
):
    """A row is a harness's read-path for skills.  One that names the user's own
    virtual-environment link or reflections link would have it replaced (links) or
    filled with the project's bytes (copies)."""
    root = _project(tmp_path, monkeypatch, rows=[{**_CLAUDE_ROW, "path": path}], copy_mode=copy_mode)
    elsewhere = tmp_path.resolve() / "users-own-folder"
    elsewhere.mkdir()
    (root / ".venv" / "bin").mkdir(parents=True)
    os.symlink(sys.executable, root / ".venv" / "bin" / "python")
    (root / "dev").mkdir(exist_ok=True)
    os.symlink(elsewhere, root / "dev" / "reflections")
    (root / ".claude" / "commands").mkdir()
    (root / ".claude" / "skills-extra").mkdir()
    (root / ".claude" / "skill").mkdir()
    (root / ".claude" / "myskills").mkdir()
    (root / ".claude" / "skills").mkdir(exist_ok=True)
    (root / ".agents" / "skills" / "python").write_text("the project's bytes\n", encoding="utf-8")
    links = {p: os.readlink(p) for p in (root / ".venv" / "bin" / "python", root / "dev" / "reflections")}
    before = sorted(str(p.relative_to(root)) for p in root.rglob("*") if ".agents" not in p.parts)
    assert lifecycle._heal_skills_fanout(root) == []
    assert {p: os.readlink(p) for p in links} == links
    assert list(elsewhere.iterdir()) == []
    assert sorted(str(p.relative_to(root)) for p in root.rglob("*") if ".agents" not in p.parts) == before
    assert not (root / ".gitignore").exists()
    assert "unsafe vendor path" in capsys.readouterr().err


def test_a_cloned_vendor_table_cannot_replace_the_users_virtual_environment(tmp_path):
    """Through the real command, from a clone: a table row for `.venv/bin/python`
    leaves the user's own link alone and the real row still works."""
    src = _adopter_tree(tmp_path.resolve() / "src")
    (src / ".agents" / "skills" / "_data" / "vendor_targets.yml").write_text(
        json.dumps({"targets": [_CLAUDE_ROW, {**_CLAUDE_ROW, "target": "venv", "path": ".venv/bin/python"}]}),
        encoding="utf-8",
    )
    (src / ".claude").mkdir()
    (src / ".claude" / "keep").write_text("x", encoding="utf-8")
    (src / "tools").mkdir()
    shutil.copy(MODULE_PATH, src / "tools" / "session.py")
    _commit_all(src)
    clone = tmp_path.resolve() / "clone"
    subprocess.run(["git", "clone", "-q", str(src), str(clone)], check=True, capture_output=True)
    (clone / ".venv" / "bin").mkdir(parents=True)
    os.symlink(sys.executable, clone / ".venv" / "bin" / "python")
    done = subprocess.run(
        [sys.executable, "tools/session.py", "session-start"], cwd=str(clone),
        capture_output=True, text=True, timeout=120,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert done.returncode == 0
    assert os.readlink(clone / ".venv" / "bin" / "python") == sys.executable
    assert "unsafe vendor path" in done.stderr
    assert (clone / ".claude" / "skills").is_symlink()  # the real row was healed


# --- what the refusals say -----------------------------------------------------


def test_a_refused_folder_link_is_named_with_the_fix(tmp_path, monkeypatch, capsys):
    root, notes = _linked_reflections(tmp_path)
    _init_repo(root)
    monkeypatch.chdir(root)
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    monkeypatch.setenv("CAIRN_SESSION", "abc12345")
    assert lifecycle.main(["session-end"]) == 1
    err = capsys.readouterr().err
    assert "dev/reflections is a link" in err
    assert "replace it with a real folder" in err
    assert "2020-01-02" not in err  # the destination file is not what is named


def test_a_refused_file_link_is_named_with_the_fix(tmp_path):
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    os.symlink(tmp_path.resolve() / "elsewhere", root / ".gitignore")
    with pytest.raises(lifecycle.LifecycleError) as caught:
        lifecycle._assert_not_linked(root / ".gitignore", root)
    assert ".gitignore is a link" in str(caught.value)
    assert "replace it with a real file" in str(caught.value)


def test_after_a_refused_copy_session_start_does_not_claim_there_was_nothing_to_do(
    tmp_path, monkeypatch, capsys
):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    _init_repo(root)
    os.symlink(tmp_path.resolve() / "elsewhere", root / ".gitignore")
    monkeypatch.chdir(root)
    assert lifecycle.main(["session-start"]) == 0
    out, err = capsys.readouterr()
    assert "self-heal refused" in err
    assert "nothing to fan out" not in out


# --- a read-only .gitignore is the owner's "not by a tool" ----------------------


@pytest.mark.skipif(getattr(os, "geteuid", lambda: 1)() == 0, reason="root ignores permission bits")
def test_a_read_only_gitignore_is_refused_not_replaced(tmp_path):
    root = tmp_path.resolve()
    gitignore = root / ".gitignore"
    gitignore.write_text("*.log\n", encoding="utf-8")
    gitignore.chmod(0o444)
    with pytest.raises(lifecycle.LifecycleError, match="read-only"):
        lifecycle._seed_skill_gitignore(root, ".claude/skills/")
    assert gitignore.read_bytes() == b"*.log\n"
    assert (gitignore.stat().st_mode & 0o777) == 0o444
    # an entry that is already there needs no write, so nothing to refuse
    gitignore.chmod(0o644)
    gitignore.write_text(".claude/skills/\n", encoding="utf-8")
    gitignore.chmod(0o444)
    lifecycle._seed_skill_gitignore(root, ".claude/skills/")
    assert gitignore.read_bytes() == b".claude/skills/\n"


# --- a file where a folder must go, and a harness folder that is a file ----------


def test_a_file_where_a_copy_folder_must_go_is_refused_before_anything_is_copied(
    tmp_path, monkeypatch
):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    skills = root / ".claude" / "skills"
    skills.mkdir()
    (skills / "session-start").write_text("a file, not a folder\n", encoding="utf-8")
    with pytest.raises(lifecycle.LifecycleError, match="not a folder"):
        lifecycle._heal_skills_fanout(root)
    assert not (skills / "_data").exists()  # sorts before `session-start`
    assert (skills / "session-start").is_file()


def test_a_file_further_up_the_copy_path_is_refused_too(tmp_path, monkeypatch):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    deeper = root / ".agents" / "skills" / "nested" / "deeper"
    deeper.mkdir(parents=True)
    (deeper / "SKILL.md").write_text("x", encoding="utf-8")
    skills = root / ".claude" / "skills"
    skills.mkdir()
    (skills / "nested").write_text("a file, two folders above the copy\n", encoding="utf-8")
    with pytest.raises(lifecycle.LifecycleError, match="not a folder"):
        lifecycle._heal_skills_fanout(root)
    assert not (skills / "_data").exists()  # sorts first; nothing was copied


def test_session_start_goes_on_when_a_copy_folder_is_blocked(tmp_path, monkeypatch, capsys):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    _init_repo(root)
    skills = root / ".claude" / "skills"
    skills.mkdir()
    (skills / "session-start").write_text("x", encoding="utf-8")
    monkeypatch.chdir(root)
    assert lifecycle.main(["session-start"]) == 0
    assert "self-heal refused" in capsys.readouterr().err


@pytest.mark.parametrize("copy_mode", [False, True], ids=["links", "copies"])
def test_a_plain_file_where_the_harness_folder_should_be_means_the_harness_is_not_in_use(
    tmp_path, monkeypatch, copy_mode
):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW], copy_mode=copy_mode)
    shutil.rmtree(root / ".claude")
    (root / ".claude").write_text("a file named like the folder\n", encoding="utf-8")
    assert lifecycle._heal_skills_fanout(root) == []
    assert (root / ".claude").read_text(encoding="utf-8") == "a file named like the folder\n"


# --- the write helpers, again -----------------------------------------------------


def test_the_temporary_file_mode_is_set_on_the_open_descriptor_not_by_name(tmp_path, monkeypatch):
    if not hasattr(os, "fchmod"):
        pytest.skip("this platform has no fchmod")
    root = tmp_path.resolve()
    target = root / "target"
    target.write_bytes(b"old\n")
    target.chmod(0o640)

    def forbidden(*args, **kwargs):
        raise AssertionError("the mode was set by name, which follows a link")

    monkeypatch.setattr(lifecycle.os, "chmod", forbidden)
    lifecycle._write_replacing(target, b"new\n")
    assert target.read_bytes() == b"new\n"
    assert (target.stat().st_mode & 0o777) == 0o640


def test_each_write_gets_its_own_random_temporary_name(tmp_path, monkeypatch):
    root = tmp_path.resolve()
    seen = []
    real_open = lifecycle.os.open

    def spy(path, *args, **kwargs):
        if Path(path).name.startswith(".cairn-write-"):
            seen.append(Path(path).name)
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(lifecycle.os, "open", spy)
    lifecycle._write_replacing(root / "a", b"1")
    lifecycle._write_replacing(root / "a", b"2")
    assert len(seen) == 2 and seen[0] != seen[1]
    assert all(re.fullmatch(r"\.cairn-write-[0-9a-f]{16}", name) for name in seen)


def test_the_heartbeat_leaves_a_whole_current_payload_each_time(tmp_path):
    root = tmp_path.resolve() / "proj"
    (root / "dev" / ".cairn").mkdir(parents=True)
    lock = lifecycle.HandoffLock(root, "an-agent-name-that-is-fairly-long-indeed")
    lock.acquire()
    try:
        lock_file = root / "dev" / ".cairn" / "handoff.lock"
        first = json.loads(lock_file.read_text(encoding="utf-8"))
        lock.agent = "short"
        lock.heartbeat()
        second = json.loads(lock_file.read_text(encoding="utf-8"))  # valid JSON, no leftovers
    finally:
        lock.release()
    assert second["agent"] == "short" and second["pid"] == first["pid"]
    assert second["heartbeat_at"] >= first["heartbeat_at"]


def test_a_named_pipe_where_gitignore_should_be_is_refused_not_waited_on(tmp_path):
    if not hasattr(os, "mkfifo"):
        pytest.skip("no named pipes here")
    root = tmp_path.resolve()
    os.mkfifo(root / ".gitignore")
    result = _call_with_timeout(lifecycle._seed_skill_gitignore, root, ".claude/skills/")
    assert isinstance(result, lifecycle.LifecycleError)


def test_a_named_pipe_swapped_in_just_before_the_read_is_refused_not_waited_on(
    tmp_path, monkeypatch
):
    """The check has passed; the name becomes a pipe before the file is opened.
    Opening a pipe for reading waits for a writer, so the open must not wait."""
    if not hasattr(os, "mkfifo"):
        pytest.skip("no named pipes here")
    root = tmp_path.resolve()
    (root / ".gitignore").write_text("*.log\n", encoding="utf-8")
    real_open = lifecycle.os.open

    def swap_then_open(path, flags, *args, **kwargs):
        if Path(path).name == ".gitignore" and not (flags & (os.O_WRONLY | os.O_RDWR)):
            Path(path).unlink()
            os.mkfifo(path)
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(lifecycle.os, "open", swap_then_open)
    result = _call_with_timeout(lifecycle._seed_skill_gitignore, root, ".claude/skills/")
    assert isinstance(result, lifecycle.LifecycleError)


def _call_with_timeout(function, *args, seconds: float = 5.0):
    """Run `function` in a thread; return what it raised.  A call that is still
    waiting after `seconds` fails the test (and is released so it does not leak)."""
    import threading

    box = {}

    def runner():
        try:
            function(*args)
            box["raised"] = None
        except BaseException as exc:  # the test inspects the exception itself
            box["raised"] = exc

    thread = threading.Thread(target=runner, daemon=True)
    thread.start()
    thread.join(seconds)
    if thread.is_alive():
        for path in Path(args[0]).glob(".gitignore"):
            try:
                fd = os.open(path, os.O_WRONLY | getattr(os, "O_NONBLOCK", 0))
                os.close(fd)
            except OSError:
                pass
        thread.join(2)
        pytest.fail(f"{function.__name__} was still waiting after {seconds} s")
    return box["raised"]


@pytest.mark.parametrize("swap", ["a link", "another file"])
def test_without_a_no_follow_flag_the_read_still_refuses_a_file_swapped_in_after_the_check(
    tmp_path, monkeypatch, swap
):
    """Where the platform has no `O_NOFOLLOW` (Windows), the read compares the file
    it opened with the file that was checked, by device and inode."""
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    stand_in = _stand_in(tmp_path)
    (root / ".gitignore").write_text("*.log\n", encoding="utf-8")
    monkeypatch.setattr(lifecycle, "_OPEN_NO_LINK", 0)
    real_open = lifecycle.os.open
    swapped = []

    def swap_then_open(path, flags, *args, **kwargs):
        if Path(path).name == ".gitignore" and not (flags & (os.O_WRONLY | os.O_RDWR)) and not swapped:
            swapped.append(True)
            Path(path).unlink()
            if swap == "a link":
                os.symlink(stand_in, path)
            else:
                Path(path).write_text("*.tmp\n", encoding="utf-8")
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(lifecycle.os, "open", swap_then_open)
    with pytest.raises(lifecycle.LifecycleError):
        lifecycle._seed_skill_gitignore(root, ".claude/skills/")
    assert swapped
    assert stand_in.read_text(encoding="utf-8") == _STAND_IN_TEXT
    text = (root / ".gitignore").read_text(encoding="utf-8")
    assert ".claude/skills/" not in text


# --- no message carries raw control bytes from project data -----------------------

_ESC = "\x1b]0;PWNED\x07"


def _text_of(call, *args):
    with pytest.raises(lifecycle.LifecycleError) as caught:
        call(*args)
    return str(caught.value)


def _bare_project(tmp_path):
    root = tmp_path.resolve() / "proj"
    (root / "real").mkdir(parents=True)
    return root


def _site_guard_folder_link(tmp_path, monkeypatch, capsys):
    root = _bare_project(tmp_path)
    os.symlink("real", root / ("n" + _ESC))
    return _text_of(lifecycle._assert_not_linked, root / ("n" + _ESC) / "x.md", root)


def _site_guard_file_link(tmp_path, monkeypatch, capsys):
    root = _bare_project(tmp_path)
    os.symlink("real", root / ("n" + _ESC + ".md"))
    return _text_of(lifecycle._assert_not_linked, root / ("n" + _ESC + ".md"), root)


def _site_guard_outside(tmp_path, monkeypatch, capsys):
    root = _bare_project(tmp_path)
    return _text_of(lifecycle._assert_not_linked, root / ".." / ("n" + _ESC), root)


def _site_guard_not_under_root(tmp_path, monkeypatch, capsys):
    root = _bare_project(tmp_path)
    return _text_of(lifecycle._assert_not_linked, tmp_path.resolve() / ("n" + _ESC), root)


def _site_fanout_parent_link(tmp_path, monkeypatch, capsys):
    root = _bare_project(tmp_path)
    os.symlink("real", root / ("n" + _ESC))
    return _text_of(lifecycle._assert_fanout_contained, root / ("n" + _ESC) / "skills", root)


def _site_fanout_outside(tmp_path, monkeypatch, capsys):
    root = _bare_project(tmp_path)
    return _text_of(lifecycle._assert_fanout_contained, root / ".." / ("n" + _ESC), root)


def _site_unsafe_entry(tmp_path, monkeypatch, capsys):
    return _text_of(lifecycle._seed_skill_gitignore, tmp_path.resolve(), _ESC + "/skills/")


def _site_not_a_plain_file(tmp_path, monkeypatch, capsys):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    (root / ".agents" / "skills" / "session-start" / ("f" + _ESC)).write_text("x", encoding="utf-8")
    (root / ".claude" / "skills" / "session-start" / ("f" + _ESC)).mkdir(parents=True)
    return _text_of(lifecycle._heal_skills_fanout, root)


def _site_quarantine_not_a_plain_file(tmp_path, monkeypatch, capsys):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    name = "f" + _ESC
    (root / ".agents" / "skills" / "session-start" / name).write_text("canonical", encoding="utf-8")
    folder = root / ".claude" / "skills" / "session-start"
    folder.mkdir(parents=True)
    (folder / name).write_text("a local edit", encoding="utf-8")
    (folder / (name + ".diverged.bak")).mkdir()
    return _text_of(lifecycle._heal_skills_fanout, root)


def _site_not_a_folder(tmp_path, monkeypatch, capsys):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    name = "d" + _ESC
    (root / ".agents" / "skills" / name).mkdir()
    (root / ".agents" / "skills" / name / "SKILL.md").write_text("x", encoding="utf-8")
    (root / ".claude" / "skills").mkdir()
    (root / ".claude" / "skills" / name).write_text("a file", encoding="utf-8")
    return _text_of(lifecycle._heal_skills_fanout, root)


def _site_divergence_warning(tmp_path, monkeypatch, capsys):
    root = _project(tmp_path, monkeypatch, rows=[_CLAUDE_ROW])
    name = "f" + _ESC
    (root / ".agents" / "skills" / "session-start" / name).write_text("canonical", encoding="utf-8")
    folder = root / ".claude" / "skills" / "session-start"
    folder.mkdir(parents=True)
    (folder / name).write_text("a local edit", encoding="utf-8")
    lifecycle._heal_skills_fanout(root)
    return capsys.readouterr().err


def _site_divergence_warning_in_a_folder_named_with_escapes(tmp_path, monkeypatch, capsys):
    """The folder the copy sits in is printed too; the project's own folder name
    is data when someone else chose it (a clone's default folder name)."""
    holder = tmp_path.resolve() / ("p" + _ESC)
    holder.mkdir()
    root = _adopter_tree(holder / "proj")
    (root / ".claude" / "skills" / "session-start").mkdir(parents=True)
    (root / ".claude" / "skills" / "session-start" / "SKILL.md").write_text("a local edit", encoding="utf-8")
    monkeypatch.setattr(lifecycle, "_skill_symlinks_available", lambda _r: False)
    lifecycle._heal_skills_fanout(root)
    return capsys.readouterr().err


def _site_unsafe_vendor_path_warning(tmp_path, monkeypatch, capsys):
    root = _project(tmp_path, monkeypatch, rows=[{**_CLAUDE_ROW, "target": "t" + _ESC, "path": "p" + _ESC + "/skills"}])
    lifecycle._heal_skills_fanout(root)
    return capsys.readouterr().err


def _site_handoff_manifest(tmp_path, monkeypatch, capsys):
    root = tmp_path.resolve() / "proj"
    (root / "dev" / "reflections").mkdir(parents=True)
    (root / "dev" / "reflections" / ("2020-01-01-" + _ESC + ".md")).write_text("x", encoding="utf-8")
    _init_repo(root)
    monkeypatch.chdir(root)
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    monkeypatch.setenv("CAIRN_SESSION", "abc12345")
    assert lifecycle.main(["session-end", "--handoff", "--dry-run"]) == 0
    return capsys.readouterr().out


def _lock_file(root: Path, **fields) -> None:
    folder = lifecycle._state_dir(root)
    folder.mkdir(parents=True)
    payload = {"pid": 1, "host": "elsewhere", "agent": "x", "acquired_at": 0.0, "heartbeat_at": 0.0}
    payload.update(fields)
    (folder / "handoff.lock").write_text(json.dumps(payload), encoding="utf-8")


def _site_lock_refusal(tmp_path, monkeypatch, capsys):
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    _lock_file(root, pid=_ESC, host=_ESC, agent=_ESC)
    return _text_of(lifecycle.HandoffLock(root, "owner").acquire)


def _site_lock_reclaim_warning(tmp_path, monkeypatch, capsys):
    import socket

    root = tmp_path.resolve() / "proj"
    root.mkdir()
    dead = subprocess.Popen([sys.executable, "-c", "pass"])
    dead.wait()
    _lock_file(root, pid=dead.pid, host=socket.gethostname(), agent=_ESC)
    lock = lifecycle.HandoffLock(root, "owner")
    lock.acquire()
    lock.release()
    return capsys.readouterr().err


def _site_prune_warning(tmp_path, monkeypatch, capsys):
    root = tmp_path.resolve() / "proj"
    folder = root / "dev" / "reflections"
    folder.mkdir(parents=True)
    (folder / ("2020-01-01-" + _ESC + ".md")).write_text("x", encoding="utf-8")
    real_unlink = Path.unlink

    def failing(self, *args, **kwargs):
        if self.name.startswith("2020-01-01-"):
            raise OSError("cannot remove " + self.name)
        return real_unlink(self, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", failing)
    lifecycle._prune_reflections(root, 14, dry_run=False)
    return capsys.readouterr().err


_MESSAGE_SITES = {
    "guard-folder-link": _site_guard_folder_link,
    "guard-file-link": _site_guard_file_link,
    "guard-outside": _site_guard_outside,
    "guard-not-under-root": _site_guard_not_under_root,
    "fan-out-parent-link": _site_fanout_parent_link,
    "fan-out-outside": _site_fanout_outside,
    "unsafe-ignore-entry": _site_unsafe_entry,
    "copy-not-a-plain-file": _site_not_a_plain_file,
    "quarantine-not-a-plain-file": _site_quarantine_not_a_plain_file,
    "copy-folder-is-a-file": _site_not_a_folder,
    "divergence-warning": _site_divergence_warning,
    "divergence-warning-folder-name": _site_divergence_warning_in_a_folder_named_with_escapes,
    "unsafe-vendor-path-warning": _site_unsafe_vendor_path_warning,
    "handoff-manifest": _site_handoff_manifest,
    "lock-refusal": _site_lock_refusal,
    "lock-reclaim-warning": _site_lock_reclaim_warning,
    "prune-warning": _site_prune_warning,
}


@pytest.mark.parametrize("site", sorted(_MESSAGE_SITES))
def test_no_message_site_puts_raw_control_bytes_from_project_data_on_the_terminal(
    tmp_path, monkeypatch, capsys, site
):
    text = _MESSAGE_SITES[site](tmp_path, monkeypatch, capsys)
    assert text.strip(), "the site printed nothing"
    assert "\x1b" not in text and "\x07" not in text
    assert "\\x1b" in text  # shown escaped, so the reader can still see something was there


# --- the second reflection pruner ---------------------------------------------------

PRUNE_TOOL = CAIRN_ROOT / "templates" / "modules" / "default-on" / "prune_reflections.py"
PRUNE_TOOL_INSTALLED = CAIRN_ROOT / "tools" / "prune_reflections.py"


def _load_prune_tool(path: Path = PRUNE_TOOL):
    spec = importlib.util.spec_from_file_location("cairn_prune_reflections_contained", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_two_copies_of_the_reflection_pruner_are_identical():
    assert PRUNE_TOOL.read_bytes() == PRUNE_TOOL_INSTALLED.read_bytes()


def _old_reflections(folder: Path) -> list:
    names = ["2020-01-01-101010-claude-reviewer.md", "2020-01-02-101010-claude-reviewer.md"]
    for name in names:
        (folder / name).write_text("mine\n", encoding="utf-8")
    return [folder / name for name in names]


@pytest.mark.parametrize("dry_run", [False, True])
def test_the_pruner_never_deletes_through_a_linked_reflections_folder(tmp_path, dry_run):
    tool = _load_prune_tool()
    notes = tmp_path.resolve() / "notes"
    notes.mkdir()
    kept = _old_reflections(notes)
    project = tmp_path.resolve() / "proj"
    (project / "dev").mkdir(parents=True)
    os.symlink(notes, project / "dev" / "reflections")
    tool._REPO_ROOT = project
    with pytest.raises(tool.RefusedDirectory, match="link"):
        tool.prune_reflections(project / "dev" / "reflections", keep=1, dry_run=dry_run)
    assert all(path.read_text(encoding="utf-8") == "mine\n" for path in kept)


def test_the_pruner_never_deletes_through_a_linked_parent_of_the_folder(tmp_path):
    tool = _load_prune_tool()
    elsewhere = tmp_path.resolve() / "elsewhere"
    (elsewhere / "reflections").mkdir(parents=True)
    kept = _old_reflections(elsewhere / "reflections")
    project = tmp_path.resolve() / "proj"
    project.mkdir()
    os.symlink(elsewhere, project / "dev")
    tool._REPO_ROOT = project
    with pytest.raises(tool.RefusedDirectory):
        tool.prune_reflections(project / "dev" / "reflections", keep=1)
    assert all(path.exists() for path in kept)


def test_the_pruner_command_exits_with_a_plain_refusal_for_a_linked_folder(tmp_path):
    notes = tmp_path.resolve() / "notes"
    notes.mkdir()
    kept = _old_reflections(notes)
    project = tmp_path.resolve() / "proj"
    (project / "tools").mkdir(parents=True)
    (project / "dev").mkdir()
    shutil.copy(PRUNE_TOOL, project / "tools" / "prune_reflections.py")
    os.symlink(notes, project / "dev" / "reflections")
    done = subprocess.run(
        [sys.executable, "tools/prune_reflections.py", "--keep", "1"], cwd=str(project),
        capture_output=True, text=True, timeout=60, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert done.returncode == 2 and "link" in done.stderr and "Traceback" not in done.stderr
    assert all(path.exists() for path in kept)


def test_the_pruner_finds_a_link_below_the_outermost_spelling_of_the_project(tmp_path):
    """A link back into the project must not hide the project's boundary: the link
    itself is inside the project and is refused."""
    tool = _load_prune_tool()
    project = tmp_path.resolve() / "proj"
    folder = project / "dev" / "reflections"
    folder.mkdir(parents=True)
    kept = _old_reflections(folder)
    os.symlink(project, project / "loop")
    tool._REPO_ROOT = project
    with pytest.raises(tool.RefusedDirectory, match="loop"):
        tool.prune_reflections(project / "loop" / "dev" / "reflections", keep=1)
    assert all(path.exists() for path in kept)


def test_a_linked_folder_the_operator_names_outside_the_project_is_not_second_guessed(tmp_path):
    tool = _load_prune_tool()
    project = tmp_path.resolve() / "proj"
    project.mkdir()
    real = tmp_path.resolve() / "real-notes"
    real.mkdir()
    old = _old_reflections(real)
    chosen = tmp_path.resolve() / "chosen-link"
    os.symlink(real, chosen)
    tool._REPO_ROOT = project
    assert [path.name for path in tool.prune_reflections(chosen, keep=1)] == [old[0].name]
    assert not old[0].exists() and old[1].exists()


def test_the_pruner_still_prunes_an_ordinary_reflections_folder(tmp_path):
    tool = _load_prune_tool()
    project = tmp_path.resolve() / "proj"
    folder = project / "dev" / "reflections"
    folder.mkdir(parents=True)
    old = _old_reflections(folder)
    tool._REPO_ROOT = project
    assert tool.prune_reflections(folder, keep=1) == [old[0]]
    assert not old[0].exists() and old[1].exists()


def test_a_folder_the_operator_names_outside_the_project_is_the_operators_choice(tmp_path):
    tool = _load_prune_tool()
    project = tmp_path.resolve() / "proj"
    project.mkdir()
    folder = tmp_path.resolve() / "chosen"
    folder.mkdir()
    old = _old_reflections(folder)
    tool._REPO_ROOT = project
    assert tool.prune_reflections(folder, keep=1) == [old[0]]
