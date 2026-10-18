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
    "semicolon": ".claude/skills; touch MARKER",
    "newline": ".claude/skills\ntouch MARKER",
    "carriage-return": ".claude/skills\rtouch MARKER",
    "config-stanza": "zz\n[core]\nfsmonitor = touch MARKER\n#/skills",
    "space": ".claude/sk ills",
    "glob": ".claude/*",
    "negation": "!.claude/skills",
    "comment": "#.claude/skills",
    "backslash": ".claude\\skills",
    "escape-byte": ".claude/\x1b[31mskills",
    "current-dir": "./.claude/skills",
    "empty-part": ".claude//skills",
    "project-root": ".",
    "newline-only": ".claude/a\nb",
    "carriage-return-only": ".claude/a\rb",
    "trailing-newline": ".claude/skills\n",
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
    [".git", ".claude/.GIT", ".git/hooks", ".claude/.git.", ".claude/.git", "dev/.cairn",
     "Dev/.Cairn", "dev/.cairn/x", ".claude"],
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
