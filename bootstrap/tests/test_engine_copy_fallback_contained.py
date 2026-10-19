"""The installer's skills fan-out never writes through a link or outside the project.

An install often runs into a repository that already holds data nobody reviewed
as an install input: a folder, a link, a file with someone else's name on it.
The skills fan-out (`bootstrap/_scaffold/install.py`: `fan_out_skills`,
`_symlinks_available`, `_emit_skill_copy_fallback`) copies the canonical skills
into a harness folder where links are unavailable, and it must stay inside the
project and never follow a link, whatever that data says.

Three groups of tests, because they ask different questions:

* **Data alone.**  The real command line (`bootstrap/scaffold.py`, a
  subprocess) installs into a project holding only the hostile data, with no
  patching.  The outside folder and everything in it must come out as it went
  in.  Nothing here is told which path the fan-out takes: that is the point, a
  project's own files must not be able to choose it.
* **The copy path itself.**  On a platform where links can be made the copy path
  is only reached when the probe says "no links", so these tests make it say so
  (the stand-in for Windows without Developer Mode) and check what the copy path
  refuses, in what words, and that it refuses before it writes anything.
* **Order and last-name races.**  The whole set is checked before the first
  write, and a link that appears after its check is replaced, not followed.
  The probe's own name is pinned at the end.

Ordinary copy behaviour (what is copied, quarantined, left alone) is pinned in
`test_skills_fanout.py`; this file pins what the fan-out refuses.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_engine_copy_fallback_contained.py
"""
from __future__ import annotations

import os
import secrets
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import ScaffoldSecurityError, main  # noqa: E402  (the facade loads the engine)
from bootstrap._scaffold import install as INS  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"
SCAFFOLD = CAIRN_ROOT / "bootstrap" / "scaffold.py"

#: The fixed name the probe used before it was random.  A folder here used to
#: make the installer believe links were unavailable.
_OLD_PROBE_NAME = ".cairn-symlink-probe"

#: A date long before any test run, so "the file was rewritten" shows as a new time.
_LONG_AGO_NS = 946_684_800 * 10**9

_CLAUDE_ROW = {"target": "claude-code", "tier": "symlink", "path": ".claude/skills"}


def _needs_symlinks(directory: Path) -> None:
    try:
        os.symlink(".", directory / "can-link")
    except (OSError, NotImplementedError):
        pytest.skip("symlinks are not available here")
    (directory / "can-link").unlink()


def _hard_link(existing: Path, new: Path) -> None:
    try:
        os.link(existing, new)
    except (OSError, NotImplementedError):
        pytest.skip("hard links are not available here")


@pytest.fixture()
def links_work(tmp_path):
    _needs_symlinks(tmp_path)


#: For the tests that plant a link.  The ones that do not (a folder or file in the
#: wrong place, the divergence warning, a failed rename, the probe's name and its
#: no-links answer) run everywhere, and a machine that cannot make links is the
#: one where the copy path is the normal one.
needs_links = pytest.mark.usefixtures("links_work")


def _world(tmp_path: Path) -> tuple[Path, Path, Path]:
    """(project, a folder outside it, a profile file) with the harness folder present."""
    root = tmp_path.resolve()
    target = root / "proj"
    target.mkdir()
    (target / ".claude").mkdir()
    outside = root / "outside"
    outside.mkdir()
    profile = root / "profile.yml"
    profile.write_text(
        "project_name: CopyFallback\ntest_command: pytest\nmodules:\n"
        "  - coordination-tiers\n",
        encoding="utf-8",
    )
    return target, outside, profile


def _argv(target: Path, profile: Path) -> list[str]:
    return [
        "--config", str(profile), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ]


def _cli(target: Path, profile: Path) -> subprocess.CompletedProcess[str]:
    """The real command line, as a person runs it."""
    return subprocess.run(
        [sys.executable, str(SCAFFOLD), *_argv(target, profile)],
        capture_output=True, text=True, cwd=str(target.parent), timeout=180,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def _snapshot(root: Path) -> dict[str, tuple]:
    """Everything under *root* -- files (bytes and modification time), folders and
    links (what they point at) -- with no link followed."""
    found: dict[str, tuple] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(dirpath)
        for name in dirnames + filenames:
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                found[rel] = ("link", os.readlink(path))
            elif path.is_dir():
                found[rel] = ("dir",)
            else:
                found[rel] = ("file", path.read_bytes(), path.stat().st_mtime_ns)
    return found


def _canonical(target: Path, skill: str, name: str, text: str) -> Path:
    """The project's own canonical skill file.  The install never clobbers it."""
    path = target / ".agents" / "skills" / skill / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _copy_dir(target: Path, skill: str) -> Path:
    path = target / ".claude" / "skills" / skill
    path.mkdir(parents=True, exist_ok=True)
    return path


# --- the hostile data, one function per shape ---------------------------------


def _plant_dangling_link_to_a_startup_file(target: Path, outside: Path) -> None:
    """The project's skill holds a shell line, and its copy name is a link to a
    startup file that does not exist yet."""
    _canonical(target, "session-start", "SKILL.md", "touch STARTUP_MARKER\n")
    os.symlink(outside / ".zshenv", _copy_dir(target, "session-start") / "SKILL.md")


def _plant_quarantine_name_linked_to_a_folder(target: Path, outside: Path) -> None:
    """A copy that differs from the canonical one, and the name it would be moved
    to is a link to a folder outside."""
    folder = _copy_dir(target, "session-end")
    (folder / "SKILL.md").write_text("a local edit\n", encoding="utf-8")
    os.symlink(outside, folder / "SKILL.md.diverged.bak", target_is_directory=True)


def _plant_copy_name_linked_to_an_equal_file(target: Path, outside: Path) -> None:
    """The copy name is a link to an outside file that already holds exactly the
    canonical bytes, so nothing about the content looks wrong."""
    text = "the canonical bytes\n"
    _canonical(target, "session-start", "SKILL.md", text)
    keep = outside / "keep.txt"
    keep.write_text(text, encoding="utf-8")
    os.utime(keep, ns=(_LONG_AGO_NS, _LONG_AGO_NS))
    os.symlink(keep, _copy_dir(target, "session-start") / "SKILL.md")


def _plant_folder_on_the_way_linked(target: Path, outside: Path) -> None:
    """The skill's own folder under the harness folder is a link to a folder outside."""
    (target / ".claude" / "skills").mkdir()
    os.symlink(outside, target / ".claude" / "skills" / "session-start",
               target_is_directory=True)


def _plant_quarantine_name_linked_to_a_missing_file(target: Path, outside: Path) -> None:
    """A copy that differs from the canonical one, and the name it would be moved
    to is a link to a file outside that does not exist yet."""
    folder = _copy_dir(target, "session-end")
    (folder / "SKILL.md").write_text("a local edit\n", encoding="utf-8")
    os.symlink(outside / "not-created-yet", folder / "SKILL.md.diverged.bak")


def _plant_harness_folder_linked(target: Path, outside: Path) -> None:
    """The harness folder itself (`.claude`) is a link to a folder outside."""
    (target / ".claude").rmdir()
    os.symlink(outside, target / ".claude", target_is_directory=True)


def _plant_harness_skills_folder_linked(target: Path, outside: Path) -> None:
    """The harness folder's `skills` is itself a link to a folder outside."""
    os.symlink(outside, target / ".claude" / "skills", target_is_directory=True)


#: Each shape, with the exit code a plain install over it (links available)
#: ends with: 0, except where the link is on the way to the harness folder
#: itself, which the install refuses whichever way it fans out.
_HOSTILE = {
    "dangling-link-to-a-startup-file": (_plant_dangling_link_to_a_startup_file, 0),
    "quarantine-name-linked-to-a-folder": (_plant_quarantine_name_linked_to_a_folder, 0),
    "quarantine-name-linked-to-a-missing-file": (
        _plant_quarantine_name_linked_to_a_missing_file, 0),
    "copy-name-linked-to-an-equal-file": (_plant_copy_name_linked_to_an_equal_file, 0),
    "folder-on-the-way-linked": (_plant_folder_on_the_way_linked, 0),
    "harness-skills-folder-linked": (_plant_harness_skills_folder_linked, 0),
    "harness-folder-linked": (_plant_harness_folder_linked, 2),
}


# --- data alone, through the real command line --------------------------------


@needs_links
def test_a_folder_at_the_old_probe_name_does_not_make_the_install_copy(tmp_path):
    target, _outside, profile = _world(tmp_path)
    folder = target / _OLD_PROBE_NAME
    folder.mkdir()
    (folder / "keep").write_text("a committed file", encoding="utf-8")

    result = _cli(target, profile)

    assert result.returncode == 0, result.stderr
    skills = target / ".claude" / "skills"
    assert skills.is_symlink(), "a project's own folder chose the copy path"
    assert "symlinks unavailable" not in result.stderr
    assert (folder / "keep").read_text(encoding="utf-8") == "a committed file"


@needs_links
@pytest.mark.parametrize("shape", _HOSTILE, ids=list(_HOSTILE))
def test_hostile_project_data_alone_cannot_make_the_install_write_outside(
    tmp_path, shape
):
    plant, exit_code = _HOSTILE[shape]
    target, outside, profile = _world(tmp_path)
    # the one extra step that used to force the copy path from project data
    (target / _OLD_PROBE_NAME).mkdir()
    (target / _OLD_PROBE_NAME / "keep").write_text("x", encoding="utf-8")
    plant(target, outside)
    before = _snapshot(outside)

    result = _cli(target, profile)

    assert _snapshot(outside) == before, (
        "the install wrote to, through, or into something outside the project:\n"
        + result.stderr
    )
    assert result.returncode == exit_code, result.stderr


# --- the copy path itself -----------------------------------------------------


@pytest.fixture()
def copy_mode(monkeypatch):
    """Make the probe say links are unavailable: the Windows-without-Developer-Mode case."""
    monkeypatch.setattr(INS, "_symlinks_available", lambda _target: False)


def _install_in_copy_mode(target: Path, profile: Path, capsys) -> tuple[int, str]:
    capsys.readouterr()
    code = main(_argv(target, profile))
    return code, capsys.readouterr().err


@needs_links
@pytest.mark.parametrize("shape", _HOSTILE, ids=list(_HOSTILE))
def test_copy_mode_refuses_before_writing_anything_and_touches_nothing_outside(
    tmp_path, copy_mode, capsys, shape
):
    plant, _exit_code = _HOSTILE[shape]
    target, outside, profile = _world(tmp_path)
    plant(target, outside)
    outside_before = _snapshot(outside)
    harness_before = _snapshot(target / ".claude")

    code, err = _install_in_copy_mode(target, profile, capsys)

    assert code == 2, err
    assert "skills fan-out refused" in err
    assert _snapshot(outside) == outside_before
    assert _snapshot(target / ".claude") == harness_before, (
        "the refusal came after some copies had been written"
    )


@needs_links
@pytest.mark.parametrize("linked", ["harness-folder", "skills-folder"])
def test_a_linked_folder_above_the_link_to_make_is_refused_before_the_link_is_made(
    tmp_path, linked
):
    """With links available the fan-out makes a link, and it must not make it
    through a link: the harness folder (or the vendor folder's parent) can be a
    link to a folder outside, and the new link would land there."""
    repo = _repo(tmp_path)
    outside = tmp_path.resolve() / "outside"
    outside.mkdir()
    if linked == "harness-folder":
        (repo / ".claude").rmdir()
        os.symlink(outside, repo / ".claude", target_is_directory=True)
        row = _CLAUDE_ROW
    else:
        os.symlink(outside, repo / ".github", target_is_directory=True)
        row = {"target": "x", "tier": "symlink", "path": ".github/skills"}

    with pytest.raises(ScaffoldSecurityError, match="symlinked parent"):
        INS.fan_out_skills(TEMPLATES_ROOT, repo, targets=[row], allow_symlinks=True)

    assert list(outside.iterdir()) == [], "a link was made at the far end of a link"


@needs_links
def test_a_refusal_is_fixed_words_a_project_relative_name_and_a_remedy(
    tmp_path, copy_mode, capsys
):
    target, outside, profile = _world(tmp_path)
    _plant_dangling_link_to_a_startup_file(target, outside)

    code, err = _install_in_copy_mode(target, profile, capsys)

    assert code == 2
    assert ("refusing to write skill copies through a link or outside the "
            "project: .claude/skills/session-start/SKILL.md") in err
    assert "remove that link" in err
    # not "re-run": an upgrade that adds the skills does not redo the fan-out when
    # run again; session-start does, and so does installing again
    assert "re-run" not in err.split("skills fan-out refused", 1)[1]
    assert "python tools/session.py session-start` (or install again)" in err
    # where the link points is the project's data, and an absolute path is not ours to print
    refusal = err.split("skills fan-out refused", 1)[1]
    assert str(outside) not in refusal
    assert str(target) not in refusal


@needs_links
def test_a_refusal_puts_no_raw_control_bytes_on_the_terminal(tmp_path, copy_mode, capsys):
    target, outside, profile = _world(tmp_path)
    awkward = "\x1b]0;retitled\x07.md"
    _canonical(target, "session-start", awkward, "x")
    os.symlink(outside / "nothing", _copy_dir(target, "session-start") / awkward)

    code, err = _install_in_copy_mode(target, profile, capsys)

    assert code == 2
    assert "\x1b" not in err and "\x07" not in err
    assert "\\x1b" in err  # shown as an escape, so the reader can still see it


@pytest.mark.parametrize(
    "what",
    ["a-folder-at-the-copy-name", "a-folder-at-the-quarantine-name",
     "a-file-where-a-folder-must-go"],
)
def test_something_that_is_not_a_plain_file_is_refused_and_nothing_is_copied(
    tmp_path, copy_mode, capsys, what
):
    """A folder or a file in the wrong place made the copy crash part-way, after
    earlier files had been written.  It is a refusal now, decided up front."""
    target, outside, profile = _world(tmp_path)
    folder = _copy_dir(target, "session-start")
    if what == "a-folder-at-the-copy-name":
        (folder / "SKILL.md").mkdir()
    elif what == "a-folder-at-the-quarantine-name":
        (folder / "SKILL.md").write_text("a local edit\n", encoding="utf-8")
        (folder / "SKILL.md.diverged.bak").mkdir()
    else:
        folder.rmdir()
        folder.write_text("a file, not a folder", encoding="utf-8")
    harness_before = _snapshot(target / ".claude")

    code, err = _install_in_copy_mode(target, profile, capsys)

    assert code == 2, err
    assert "skills fan-out refused" in err
    assert "move or remove it" in err
    assert "python tools/session.py session-start` (or install again)" in err
    assert "Traceback" not in err
    assert _snapshot(target / ".claude") == harness_before
    assert _snapshot(outside) == {}


def test_a_divergent_copy_is_still_quarantined_and_regenerated(tmp_path, copy_mode, capsys):
    target, _outside, profile = _world(tmp_path)
    canonical = _canonical(target, "session-start", "SKILL.md", "the canonical bytes\n")
    copy = _copy_dir(target, "session-start") / "SKILL.md"
    copy.write_text("a local edit\n", encoding="utf-8")

    code, err = _install_in_copy_mode(target, profile, capsys)

    assert code == 0, err
    assert copy.read_bytes() == canonical.read_bytes()
    assert copy.with_name("SKILL.md.diverged.bak").read_text(encoding="utf-8") == (
        "a local edit\n"
    )
    assert "divergence" in err
    assert not list((target / ".claude").rglob(".cairn-write-*"))


def test_a_copy_that_is_already_current_is_left_alone(tmp_path):
    repo = _repo(tmp_path)
    INS.fan_out_skills(TEMPLATES_ROOT, repo, targets=[_CLAUDE_ROW], allow_symlinks=False)
    copy = repo / ".claude" / "skills" / "session-start" / "SKILL.md"
    os.utime(copy, ns=(_LONG_AGO_NS, _LONG_AGO_NS))

    rows = INS.fan_out_skills(
        TEMPLATES_ROOT, repo, targets=[_CLAUDE_ROW], allow_symlinks=False
    )

    assert rows == [("claude-code", "copy", "copied")]
    assert copy.stat().st_mtime_ns == _LONG_AGO_NS, "an unchanged copy was rewritten"


# --- the guard runs for the whole set, then the writes cannot follow a link ---


def _after_each_check(monkeypatch, then) -> None:
    """Run *then(dst)* right after every containment check the fan-out makes,
    whichever of the two guards it uses: the moment a link can appear that the
    check did not see."""
    for name in ("_assert_safe_write", "_assert_fanout_contained"):
        real = getattr(INS, name)

        def wrapped(dst, base, _real=real):
            _real(dst, base)
            then(dst)

        monkeypatch.setattr(INS, name, wrapped)


def _repo(tmp_path: Path) -> Path:
    """A target holding the canonical skills (as an install writes them) and the harness folder."""
    root = tmp_path.resolve() / "repo"
    for skill, text in (("session-start", "start\n"), ("session-end", "end\n")):
        path = root / ".agents" / "skills" / skill / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(text, encoding="utf-8")
    data = root / ".agents" / "skills" / "_data" / "vendor_targets.yml"
    data.parent.mkdir(parents=True)
    data.write_text("{}", encoding="utf-8")
    (root / ".claude").mkdir()
    return root


@needs_links
def test_a_link_in_the_last_name_refuses_before_the_first_copy(tmp_path):
    repo = _repo(tmp_path)
    nowhere = tmp_path.resolve() / "outside" / "not-created-yet"
    nowhere.parent.mkdir()
    skill = repo / ".claude" / "skills" / "session-start"
    skill.mkdir(parents=True)
    os.symlink(nowhere, skill / "SKILL.md")

    with pytest.raises(ScaffoldSecurityError, match="link"):
        INS.fan_out_skills(TEMPLATES_ROOT, repo, targets=[_CLAUDE_ROW], allow_symlinks=False)

    assert not nowhere.exists()
    # `_data` and `session-end` sort before `session-start`, so a file-by-file
    # loop would have copied them first
    assert not (repo / ".claude" / "skills" / "_data").exists()
    assert not (repo / ".claude" / "skills" / "session-end").exists()


@needs_links
def test_a_link_swapped_in_at_a_copy_name_after_its_check_is_replaced_not_followed(
    tmp_path, monkeypatch
):
    repo = _repo(tmp_path)
    nowhere = tmp_path.resolve() / "outside" / "not-created-yet"
    nowhere.parent.mkdir()
    (repo / ".claude" / "skills" / "session-start").mkdir(parents=True)

    def swap(dst):
        if dst.parent.name == "session-start" and not dst.is_symlink() and not dst.exists():
            os.symlink(nowhere, dst)

    _after_each_check(monkeypatch, swap)
    INS.fan_out_skills(TEMPLATES_ROOT, repo, targets=[_CLAUDE_ROW], allow_symlinks=False)

    assert not nowhere.exists(), "the copy was written through a link that appeared late"
    copy = repo / ".claude" / "skills" / "session-start" / "SKILL.md"
    assert not copy.is_symlink() and copy.read_text(encoding="utf-8") == "start\n"


@needs_links
def test_a_link_swapped_in_at_the_quarantine_name_after_its_check_is_replaced_not_followed(
    tmp_path, monkeypatch
):
    """The quarantine is a rename that replaces a link at the new name; it must
    not move the file *into* the folder that link points at."""
    repo = _repo(tmp_path)
    outside_dir = tmp_path.resolve() / "outside-dir"
    outside_dir.mkdir()
    skills = repo / ".claude" / "skills"
    (skills / "_data").mkdir(parents=True)
    (skills / "_data" / "vendor_targets.yml").write_text("a local edit\n", encoding="utf-8")

    def swap(dst):
        # `_data/...` sorts first: by the time the next file is checked, the
        # quarantine name for the first one has already passed its own check
        if dst.parent.name == "session-end":
            late = skills / "_data" / "vendor_targets.yml.diverged.bak"
            if not late.is_symlink() and not late.exists():
                os.symlink(outside_dir, late)

    _after_each_check(monkeypatch, swap)
    INS.fan_out_skills(TEMPLATES_ROOT, repo, targets=[_CLAUDE_ROW], allow_symlinks=False)

    assert list(outside_dir.iterdir()) == [], "the divergent file was moved into the link's folder"
    bak = skills / "_data" / "vendor_targets.yml.diverged.bak"
    assert not bak.is_symlink() and bak.read_text(encoding="utf-8") == "a local edit\n"


@pytest.mark.parametrize("planted", ["symbolic-link", "hard-link", "regular-file"])
def test_anything_at_the_temporary_name_is_refused_not_written_into(
    tmp_path, monkeypatch, planted
):
    """The temporary file is created exclusively, so a name someone could guess
    (made guessable here) fails instead of being opened.  Exclusive creation is
    what refuses a hard link or a plain file there; the no-follow flag alone
    refuses only a symbolic link, so each shape is planted in turn."""
    if planted == "symbolic-link":
        _needs_symlinks(tmp_path)
    repo = _repo(tmp_path)
    outside = tmp_path.resolve() / "outside"
    outside.mkdir()
    target_file = outside / "someone-elses.txt"
    original = "someone else's bytes, longer than the skill\n"
    monkeypatch.setattr(secrets, "token_hex", lambda _n=None: "guessed")
    skill = repo / ".claude" / "skills" / "session-start"
    skill.mkdir(parents=True)
    temporary = skill / ".cairn-write-guessed"
    if planted == "symbolic-link":
        os.symlink(outside / "not-created-yet", temporary)
        target_file = outside / "not-created-yet"
    elif planted == "hard-link":
        target_file.write_text(original, encoding="utf-8")
        _hard_link(target_file, temporary)
    else:
        temporary.write_text(original, encoding="utf-8")
        target_file = temporary

    with pytest.raises(OSError):
        INS.fan_out_skills(TEMPLATES_ROOT, repo, targets=[_CLAUDE_ROW], allow_symlinks=False)

    if planted == "symbolic-link":
        assert not target_file.exists()
    else:
        assert target_file.read_text(encoding="utf-8") == original, (
            "the copy was written into a file that was already at the temporary name"
        )
    assert not (skill / "SKILL.md").exists() or (skill / "SKILL.md").read_text(
        encoding="utf-8") == "start\n"


def test_a_hard_link_to_an_outside_file_is_replaced_not_written_into(tmp_path):
    repo = _repo(tmp_path)
    keep = tmp_path.resolve() / "outside" / "keep.txt"
    keep.parent.mkdir()
    keep.write_text("someone else's bytes\n", encoding="utf-8")
    skill = repo / ".claude" / "skills" / "session-start"
    skill.mkdir(parents=True)
    _hard_link(keep, skill / "SKILL.md")

    rows = INS.fan_out_skills(TEMPLATES_ROOT, repo, targets=[_CLAUDE_ROW], allow_symlinks=False)

    assert rows == [("claude-code", "copy", "diverged-quarantined")]
    assert keep.read_text(encoding="utf-8") == "someone else's bytes\n"
    assert (skill / "SKILL.md").read_text(encoding="utf-8") == "start\n"


def test_a_failed_rename_leaves_no_temporary_file(tmp_path, monkeypatch):
    repo = _repo(tmp_path)

    def refuse(_src, _dst):
        raise OSError("replace refused")

    monkeypatch.setattr(os, "replace", refuse)
    with pytest.raises(OSError, match="replace refused"):
        INS.fan_out_skills(TEMPLATES_ROOT, repo, targets=[_CLAUDE_ROW], allow_symlinks=False)
    monkeypatch.undo()

    assert not list((repo / ".claude").rglob(".cairn-write-*"))


# --- the warnings and the upgrade route ---------------------------------------


def test_the_divergence_warning_names_files_escaped_and_relative_to_the_project(
    tmp_path, copy_mode, capsys
):
    """A quarantined copy is announced by name, and the names are project data:
    a file name with an escape and a bell in it must not reach the terminal as
    those bytes, and the folder is named relative to the project."""
    target, _outside, profile = _world(tmp_path)
    awkward = "x\x1b]0;retitled\x07.md"
    _canonical(target, "session-start", awkward, "canonical\n")
    (_copy_dir(target, "session-start") / awkward).write_text("a local edit\n", encoding="utf-8")

    code, err = _install_in_copy_mode(target, profile, capsys)

    assert code == 0, err
    assert "\x1b" not in err and "\x07" not in err
    (warning,) = [line for line in err.splitlines() if "copy-fallback divergence" in line]
    assert "\\x1b" in warning, "the name was dropped instead of shown as an escape"
    assert "under .claude/skills:" in warning
    assert str(target) not in warning


_SKILL_DSTS = {
    ".agents/skills/session-start/SKILL.md",
    ".agents/skills/session-end/SKILL.md",
    "tools/session.py",
}


@needs_links
def test_an_upgrade_that_adds_the_skills_warns_and_finishes_when_the_fan_out_is_refused(
    tmp_path, copy_mode, capsys
):
    """`upgrade --apply` fans the new skills out as a last, best-effort step: a
    refusal there is a warning, and the upgrade it follows still finishes
    (exit 0, skills recorded, stage removed), not an error that leaves the
    stage folder behind after the lockfile has already moved on."""
    import shutil

    from bootstrap.scaffold import _emit_lock_yaml, read_lockfile

    target, outside, profile = _world(tmp_path)
    assert main(_argv(target, profile)) == 0
    # the state of an adopter whose lockfile predates the skills
    lock = read_lockfile(target)
    lock["files"] = [r for r in lock["files"] if r["dst"] not in _SKILL_DSTS]
    (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
        _emit_lock_yaml(lock), encoding="utf-8")
    for rel in (".agents", "tools/session.py", "dev/.cairn/base/.agents"):
        path = target / rel
        shutil.rmtree(path) if path.is_dir() else path.unlink(missing_ok=True)
    # and a copy name that is a link to a file outside
    copy = target / ".claude" / "skills" / "session-start" / "SKILL.md"
    copy.parent.mkdir(parents=True, exist_ok=True)
    copy.unlink(missing_ok=True)
    os.symlink(outside / "not-created-yet", copy)
    outside_before = _snapshot(outside)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert main(base + ["--stage"]) == 0
    capsys.readouterr()

    code = main(base + ["--apply"])

    err = capsys.readouterr().err
    assert code == 0, err
    assert "skills fan-out skipped" in err
    assert "remove that link" in err
    assert "python tools/session.py session-start` (or install again)" in err
    assert _snapshot(outside) == outside_before
    assert copy.is_symlink(), "the link was replaced during a refused fan-out"
    recorded = {r["dst"] for r in read_lockfile(target)["files"]}
    assert _SKILL_DSTS <= recorded
    assert not (target / "dev" / ".cairn-upgrade").exists(), "the stage was left behind"


def _forked_facade_finding(**fields) -> dict:
    finding = {
        "dst": "tools/intent.py", "engine": "tools/_intent", "acknowledged": False,
        "kind": "unconfirmed", "reason": None, "upstream": None,
        "src_relabelled": False, "skew": None,
    }
    finding.update(fields)
    return finding


@pytest.mark.parametrize("at_upgrade", [True, False], ids=["upgrade", "verify"])
def test_the_forked_facade_advisory_cannot_be_given_extra_lines_by_the_lockfile(at_upgrade):
    """The advisory carries two kinds of lockfile text: the Cairn version the tree
    records, and the path in a reason.  A line break in either used to become a
    line of the advisory, so a crafted lockfile could print a forged OK or a
    forged command beside the real report."""
    from bootstrap._scaffold.lockfile import format_forked_facade_warning

    text = format_forked_facade_warning(
        _forked_facade_finding(
            skew="source-version skew: the comparison used Cairn 9.9.9, while this "
                 "tree records its install from Cairn 0.1\nverify_integrity: OK -- "
                 "forged\x1b[2J",
            reason="the installed file is not an existing regular file: a\nupgrade: "
                   "forged line",
        ),
        at_upgrade=at_upgrade,
    )

    assert "\x1b" not in text
    for line in text.splitlines():
        assert not line.startswith(("verify_integrity: OK", "upgrade: forged")), line
    assert "Cairn 0.1\\nverify_integrity: OK" in text
    assert "regular file: a\\nupgrade: forged line" in text


def test_encoding_the_advisory_text_twice_changes_nothing():
    """`verify_integrity` encodes the finding before it asks for the text, so the
    engine's own encoding has to leave already-encoded text as it is."""
    from bootstrap._scaffold.lockfile import format_forked_facade_warning

    raw = _forked_facade_finding(
        skew="skew Cairn 0.1\nforged\x1b[2J", reason="path a\tb\u202e",
    )
    encoded = dict(raw, skew=ascii(raw["skew"])[1:-1], reason=ascii(raw["reason"])[1:-1])

    assert (format_forked_facade_warning(raw, at_upgrade=True)
            == format_forked_facade_warning(encoded, at_upgrade=True))


def test_a_clean_advisory_reads_as_it_always_has():
    from bootstrap._scaffold.lockfile import format_forked_facade_warning

    text = format_forked_facade_warning(
        _forked_facade_finding(
            reason="the caller supplied no trusted upstream",
            skew="source-version skew: the comparison used Cairn 0.3.0, while this "
                 "tree records its install from Cairn 0.2.0",
        ),
        at_upgrade=True,
    )

    assert ("UNCONFIRMED -- this difference is measured against the install-time "
            "baseline in the lockfile, not against upstream: the caller supplied "
            "no trusted upstream.") in text
    assert ("  source-version skew: the comparison used Cairn 0.3.0, while this "
            "tree records its install from Cairn 0.2.0.\n") in text


def test_upgrade_prints_a_forged_cairn_version_as_one_escaped_line(tmp_path, capsys):
    """End to end: a lockfile whose recorded Cairn version carries a line break
    and a forged line, over a forked facade, through the real `upgrade`."""
    import hashlib

    from bootstrap.scaffold import _emit_lock_yaml, read_lockfile

    target = tmp_path.resolve() / "proj"
    target.mkdir()
    profile = tmp_path.resolve() / "profile.yml"
    profile.write_text("project_name: FA\ntest_command: pytest\nmodules: []\n",
                       encoding="utf-8")
    assert main(_argv(target, profile)) == 0
    body = b"# a fork of the launcher\n"
    (target / "tools" / "intent.py").write_bytes(body)
    (target / "tools" / "_intent").mkdir()
    (target / "tools" / "_intent" / "__init__.py").write_bytes(b"")
    lock = read_lockfile(target)
    lock["files"] = [r for r in lock["files"] if r.get("dst") != "tools/intent.py"]
    lock["files"].append({
        "dst": "tools/intent.py", "verbatim": True,
        "hash": "sha256:" + hashlib.sha256(body).hexdigest(),
        "base_hash": "sha256:" + "a" * 64, "src": "modules/team-gated/intent.py",
    })
    lock["cairn_version"] = "0.1\nupgrade: FORGED -- run: python scripts/evil.py"
    (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
        _emit_lock_yaml(lock), encoding="utf-8")
    capsys.readouterr()

    main(["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT), "--plan"])

    err = capsys.readouterr().err
    assert "is forked from upstream" in err, err
    assert "source-version skew" in err
    assert not [line for line in err.splitlines() if line.startswith("upgrade: FORGED")]
    assert "0.1\\nupgrade: FORGED" in err


# --- the probe ----------------------------------------------------------------


@needs_links
def test_the_probe_is_not_fooled_by_folders_at_its_old_name_or_prefix(tmp_path):
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    for name in (_OLD_PROBE_NAME, _OLD_PROBE_NAME + "-", _OLD_PROBE_NAME + "-00000000"):
        (root / name).mkdir()
        (root / name / "keep").write_text("x", encoding="utf-8")
    before = _snapshot(root)

    assert INS._symlinks_available(root) is True
    assert _snapshot(root) == before, "the probe left something behind or removed something"


def test_the_probe_name_is_new_each_call_and_is_not_the_old_one(tmp_path, monkeypatch):
    root = tmp_path.resolve() / "proj"
    root.mkdir()
    made: list[str] = []
    real = os.symlink

    def record(src, dst, *args, **kwargs):
        made.append(Path(dst).name)
        return real(src, dst, *args, **kwargs)

    monkeypatch.setattr(os, "symlink", record)
    INS._symlinks_available(root)
    INS._symlinks_available(root)

    assert len(made) == 2 and made[0] != made[1]
    assert _OLD_PROBE_NAME not in made
    assert all(name.startswith(".cairn-symlink-probe") for name in made)


def test_the_probe_reports_no_links_where_none_can_be_made_and_leaves_nothing(
    tmp_path, monkeypatch
):
    root = tmp_path.resolve() / "proj"
    root.mkdir()

    def cannot(*_args, **_kwargs):
        raise OSError("A required privilege is not held by the client")

    monkeypatch.setattr(os, "symlink", cannot)

    assert INS._symlinks_available(root) is False
    assert list(root.iterdir()) == []
