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


@pytest.fixture(autouse=True)
def _links_must_work(tmp_path):
    try:
        os.symlink(".", tmp_path / "can-link")
    except (OSError, NotImplementedError):
        pytest.skip("symlinks are not available here")
    (tmp_path / "can-link").unlink()


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


def test_a_refusal_is_fixed_words_a_project_relative_name_and_a_remedy(
    tmp_path, copy_mode, capsys
):
    target, outside, profile = _world(tmp_path)
    _plant_dangling_link_to_a_startup_file(target, outside)

    code, err = _install_in_copy_mode(target, profile, capsys)

    assert code == 2
    assert ("refusing to write skill copies through a link or outside the "
            "project: .claude/skills/session-start/SKILL.md") in err
    assert "remove that link" in err and "then re-run" in err
    # where the link points is the project's data, and an absolute path is not ours to print
    refusal = err.split("skills fan-out refused", 1)[1]
    assert str(outside) not in refusal
    assert str(target) not in refusal


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
    assert "skills fan-out refused" in err and "then re-run" in err
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


def test_a_link_at_the_temporary_name_is_not_written_through(tmp_path, monkeypatch):
    """The temporary file is created exclusively, so even a name someone could
    guess (made guessable here) fails instead of writing through a link."""
    repo = _repo(tmp_path)
    nowhere = tmp_path.resolve() / "outside" / "not-created-yet"
    nowhere.parent.mkdir()
    monkeypatch.setattr(secrets, "token_hex", lambda _n=None: "guessed")
    skill = repo / ".claude" / "skills" / "session-start"
    skill.mkdir(parents=True)
    os.symlink(nowhere, skill / ".cairn-write-guessed")

    with pytest.raises(OSError):
        INS.fan_out_skills(TEMPLATES_ROOT, repo, targets=[_CLAUDE_ROW], allow_symlinks=False)

    assert not nowhere.exists()


def test_a_hard_link_to_an_outside_file_is_replaced_not_written_into(tmp_path):
    repo = _repo(tmp_path)
    keep = tmp_path.resolve() / "outside" / "keep.txt"
    keep.parent.mkdir()
    keep.write_text("someone else's bytes\n", encoding="utf-8")
    skill = repo / ".claude" / "skills" / "session-start"
    skill.mkdir(parents=True)
    os.link(keep, skill / "SKILL.md")

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


# --- the probe ----------------------------------------------------------------


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
