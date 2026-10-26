"""`upgrade` never writes, reads or prints outside what the project owns.

The project -- its lockfile, its profile file, its renamed vendor wrapper, and
the review area -- is data a cloned repository can carry, written by somebody
else.  `test_upgrade_lockfile_path_containment.py` pins the three record paths
(`src`, `dst`, `base_cache`).  This file pins the other doors an upgrade opens
on project data:

* **the profile file** -- `--apply` writes `dev/.cairn/profile.yml` when it is
  absent, and a link there (or on the way) used to carry the write, and some of
  the lockfile's text, outside the project;
* **the lockfile itself** -- a link at its name used to be read and written
  back through, and now stops the command before anything reads it;
* **the saved commit name**, which reached `git rev-list` as an option;
* **names that reach the terminal** -- the lockfile's module list and the names
  inside a review area the repository carries;
* **the refusal's own advice**, which must fit the cause;
* **a linked vendor wrapper**, which must not be taken for the wrapper;
* **Git's own folder**, which is not a project file.

Every command-line test drives the real `bootstrap/scaffold.py` as a
subprocess over a real install, with nothing patched.  The helpers come from
the sibling file, which pins the same kind of project and is not edited here.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_upgrade_refuses_hostile_project_data.py
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import ScaffoldSecurityError  # noqa: E402
from bootstrap._scaffold import lockfile as LF  # noqa: E402
from bootstrap._scaffold import upgrade as UP  # noqa: E402
from bootstrap.tests.test_upgrade_lockfile_path_containment import (  # noqa: E402
    LOCK_REL,
    STAGE_REL,
    World,
    _ACTIONS,
    _plant_stage,
    add_record,
    assert_nothing_left_the_tree,
    assert_refused,
    needs_links,
    pristine,  # noqa: F401  (a fixture: `world` asks for it by name)
    read_lock,
    record_for,
    snapshot,
    upgrade,
    world,  # noqa: F401  (a fixture)
    write_lock,
)

PROFILE_REL = "dev/.cairn/profile.yml"
_DUMMY_ADOPTION = ("--adopt-collisions", "x@" + "0" * 64 + "@" + "0" * 64)
#: Every action that starts from the lockfile, `--adopt-module` included.
_ALL_ACTIONS = _ACTIONS + (("--adopt-module", "dual-review"),)
needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="git is not available")
_GIT_ENV = {
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid",
    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
}


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                   env={**os.environ, **_GIT_ENV})


def assert_plain_refusal(proc: subprocess.CompletedProcess[str], *, code: int = 2) -> None:
    said = proc.stdout + proc.stderr
    assert proc.returncode == code, f"exit {proc.returncode}, expected {code}:\n{said[-900:]}"
    assert "Traceback" not in said
    assert "refus" in proc.stderr
    assert "\x1b" not in said


def link(target: Path | str, name: Path) -> None:
    try:
        os.symlink(target, name)
    except OSError:
        pytest.skip("symlinks are not available here")


# --- the profile file --------------------------------------------------------


def _profile_link_world(world: World, how: str, tmp_path: Path) -> World:
    """A project whose profile file is a link (or sits behind one) of kind *how*.
    Returns the world to run in: the clone, for the delivered-by-clone kind."""
    cairn = world.project / "dev" / ".cairn"
    profile = cairn / "profile.yml"
    profile.unlink(missing_ok=True)
    if how == "dangling-absolute":
        link(world.outside / "new-profile.yml", profile)
        return world
    if how == "existing-outside-file":
        (world.outside / "existing.yml").write_text("# not ours\n", encoding="utf-8")
        link(world.outside / "existing.yml", profile)
        return world
    if how == "cairn-folder-is-a-link":
        # The saved ancestors' names are dropped from the lockfile so that the
        # record check passes.  Through the command line the lockfile-name check
        # (which refuses a linked `dev/.cairn` too) answers first, so this case
        # does not isolate the profile guard; the direct call below does.
        lock = read_lock(world.project)
        for rec in lock["files"]:
            rec.pop("base_cache", None)
        write_lock(world.project, lock)
        moved = world.outside / "cairn-dir"
        shutil.copytree(cairn, moved, symlinks=True)
        shutil.rmtree(cairn)
        link(moved, cairn)
        return world
    assert how == "dangling-relative-delivered-by-clone"
    link("../../../outside/from-clone.yml", profile)
    git(world.project, "init", "-q")
    git(world.project, "add", "-A")
    git(world.project, "commit", "-q", "-m", "a project that carries a link")
    clone = tmp_path / "clone"
    git(tmp_path, "clone", "-q", str(world.project), str(clone))
    assert (clone / LOCK_REL).is_file(), "the clone must carry the lockfile"
    assert (clone / PROFILE_REL).is_symlink(), "the clone must carry the link"
    return world._replace(project=clone)


@needs_links
@pytest.mark.parametrize("how", [
    "dangling-absolute", "dangling-relative-delivered-by-clone",
    "existing-outside-file", "cairn-folder-is-a-link",
])
def test_apply_never_creates_a_profile_through_a_link(world, tmp_path, how):
    """`--apply` writes `dev/.cairn/profile.yml` when it is absent.  A name that
    is a link to a file not there yet counts as absent, and the write followed
    the link and created the file outside the project -- one command, no staged
    upgrade, delivered by an ordinary `git clone`."""
    if how == "dangling-relative-delivered-by-clone" and shutil.which("git") is None:
        pytest.skip("git is not available")
    world = _profile_link_world(world, how, tmp_path)
    outside_before = snapshot(world.outside)
    proc = upgrade(world.project, "--apply")
    assert_plain_refusal(proc)
    assert snapshot(world.outside) == outside_before, "something outside the project changed"
    if how == "cairn-folder-is-a-link":
        assert (world.project / "dev" / ".cairn").is_symlink()
    else:
        assert (world.project / PROFILE_REL).is_symlink(), "the link must be left as it was"


@pytest.mark.parametrize("where", ["preset", "axis", "token"])
def test_self_heal_writes_no_line_break_from_the_lockfile(world, where):
    """The profile file is built from the lockfile's text.  A line break in a
    value would start a line of its own in the file."""
    lock = read_lock(world.project)
    hostile = "solo-greenfield\nINJECTED_LINE: 1"
    if where == "preset":
        lock["profile"]["preset"] = hostile
    elif where == "axis":
        lock["profile"]["axes"]["size"] = hostile
    else:
        lock["tokens"]["project_name"] = hostile
    write_lock(world.project, lock)
    assert not (world.project / PROFILE_REL).exists()
    proc = upgrade(world.project, "--apply")
    assert "Traceback" not in proc.stdout + proc.stderr
    profile = world.project / PROFILE_REL
    if profile.exists():
        written = profile.read_text(encoding="utf-8")
        assert not any(line.startswith("INJECTED_LINE") for line in written.splitlines())


@pytest.mark.parametrize("value", [7, ["a"], {"a": 1}, "bad\u2028value", "esc\x1b[2J"])
def test_self_heal_writes_nothing_when_a_profile_value_is_not_plain_text(world, value):
    """A value that is not a plain printable string is never written."""
    lock = read_lock(world.project)
    lock["profile"]["axes"]["size"] = value
    write_lock(world.project, lock)
    proc = upgrade(world.project, "--apply")
    assert "Traceback" not in proc.stdout + proc.stderr
    assert not (world.project / PROFILE_REL).exists()


def test_self_heal_still_writes_a_profile_the_loader_reads_back(world):
    """What the refusals above leave alone: an ordinary lockfile heals, and the
    loader reads the written values back unchanged."""
    from bootstrap._scaffold.config import load_config
    lock = read_lock(world.project)
    assert UP._self_heal_profile_config(world.project, lock) is True
    cfg = load_config(world.project / PROFILE_REL)
    assert cfg["preset"] == lock["profile"]["preset"]
    for axis, value in lock["profile"]["axes"].items():
        assert cfg[axis] == value


@needs_links
def test_self_heal_refuses_a_linked_profile_called_directly(world):
    """The guard is in the writer, not only in the command that calls it."""
    link(world.outside / "new-profile.yml", world.project / PROFILE_REL)
    with pytest.raises(ScaffoldSecurityError):
        UP._self_heal_profile_config(world.project, read_lock(world.project))
    assert not (world.outside / "new-profile.yml").exists()


@needs_links
def test_self_heal_refuses_a_linked_cairn_folder_called_directly(world):
    """The same guard, for a link above the file rather than at it.  The command
    line answers this case with the lockfile-name check before the writer is
    reached, so only a direct call shows that the writer refuses it too."""
    cairn = world.project / "dev" / ".cairn"
    lock = read_lock(world.project)
    (cairn / "profile.yml").unlink(missing_ok=True)
    moved = world.outside / "cairn-dir"
    shutil.copytree(cairn, moved, symlinks=True)
    shutil.rmtree(cairn)
    link(moved, cairn)
    outside_before = snapshot(world.outside)
    with pytest.raises(ScaffoldSecurityError):
        UP._self_heal_profile_config(world.project, lock)
    assert snapshot(world.outside) == outside_before


@needs_links
def test_init_lock_never_creates_the_profile_template_through_a_link(world):
    """`upgrade --init-lock` writes a template `dev/.cairn/profile.yml` when none
    is there.  A link to a file not there yet counts as none, and the write
    created that file wherever the link led.  The command may stop with an error
    or with its usual "fill in the template" exit; it must write nothing
    outside the project and leave the link as it was."""
    (world.project / LOCK_REL).unlink()
    profile = world.project / PROFILE_REL
    profile.unlink(missing_ok=True)
    link(world.outside / "new-profile.yml", profile)
    outside_before = snapshot(world.outside)
    proc = upgrade(world.project, "--init-lock")
    said = proc.stdout + proc.stderr
    assert snapshot(world.outside) == outside_before, "something outside the project changed"
    assert not (world.outside / "new-profile.yml").exists()
    assert profile.is_symlink(), "the link must be left as it was"
    assert proc.returncode != 0, said[-600:]
    assert f"Wrote {PROFILE_REL}" not in said


def _no_lockfile_world(world: World) -> World:
    """A project that has been through an install but has no lockfile, which is
    the state `upgrade --init-lock` exists for."""
    (world.project / LOCK_REL).unlink()
    (world.project / PROFILE_REL).unlink(missing_ok=True)
    return world


def _complete_profile(name: str) -> str:
    return f"project_name: {name}\ntest_command: pytest\npreset: solo-greenfield\n"


@needs_links
@pytest.mark.parametrize("how", ["existing-outside-file", "existing-inside-file", "dangling"])
def test_init_lock_refuses_a_profile_that_is_a_link(world, how):
    """With no lockfile, `--init-lock` read `dev/.cairn/profile.yml` and wrote a
    lockfile carrying its values.  A link to an existing file was followed, so
    the values written into the project's lockfile were those of a file the
    project does not own.  Every link is refused, wherever it points: the rule
    is the same one `--apply` keeps for this file."""
    world = _no_lockfile_world(world)
    profile = world.project / PROFILE_REL
    if how == "existing-outside-file":
        target = world.outside / "existing.yml"
        target.write_text(_complete_profile(world.marker), encoding="utf-8")
    elif how == "existing-inside-file":
        target = world.project / "docs" / "profile-copy.yml"
        target.write_text(_complete_profile(world.marker), encoding="utf-8")
    else:
        target = world.outside / "new-profile.yml"
    link(target, profile)
    project_before, outside_before = snapshot(world.project), snapshot(world.outside)
    proc = upgrade(world.project, "--init-lock")
    assert_plain_refusal(proc)
    assert PROFILE_REL in proc.stderr, "the refusal must say which file it is about"
    assert "Replace it with a regular file" in proc.stderr, "the refusal must say what to do"
    assert world.marker not in proc.stdout + proc.stderr
    assert not (world.project / LOCK_REL).exists(), "no lockfile may be written"
    assert profile.is_symlink(), "the link must be left as it was"
    assert snapshot(world.project) == project_before, "a refusal must change nothing"
    assert snapshot(world.outside) == outside_before, "something outside the project changed"


@needs_links
@pytest.mark.parametrize("lockfile_behind_link", [True, False])
def test_init_lock_refuses_a_cairn_folder_that_is_a_link(world, lockfile_behind_link):
    """`dev/.cairn` is the folder the lockfile lives in.  Linked, `--init-lock`
    found the lockfile behind the link and said "already exists" with exit 0 --
    a read through the link, and a wrong answer about the project.  With
    nothing behind the link it went on to the profile and ended in a traceback.
    Both now stop with the one-line refusal `--plan` and `--apply` print."""
    cairn = world.project / "dev" / ".cairn"
    moved = world.outside / "cairn-dir"
    shutil.copytree(cairn, moved, symlinks=True)
    shutil.rmtree(cairn)
    link(moved, cairn)
    if not lockfile_behind_link:
        (moved / "cairn-lock.yml").unlink()
    project_before, outside_before = snapshot(world.project), snapshot(world.outside)
    proc = upgrade(world.project, "--init-lock")
    assert_plain_refusal(proc)
    assert LOCK_REL in proc.stderr, "the refusal must say which file it is about"
    assert "Replace it with a regular file" in proc.stderr, "the refusal must say what to do"
    assert "already exists" not in proc.stdout + proc.stderr
    assert cairn.is_symlink(), "the link must be left as it was"
    assert snapshot(world.project) == project_before, "a refusal must change nothing"
    assert snapshot(world.outside) == outside_before, "something outside the project changed"


def test_init_lock_with_no_profile_still_writes_the_template(world):
    """An ordinary run, no link anywhere, is as it was: the template is written,
    the command exits 2 and says no lockfile was written."""
    world = _no_lockfile_world(world)
    proc = upgrade(world.project, "--init-lock")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert proc.stdout == ""
    assert proc.stderr.startswith(f"Wrote {PROFILE_REL}: 4 axis(es) inferred, 4 placeholder(s) to fill")
    assert "No lockfile was written (fail-with-template)." in proc.stderr
    assert (world.project / PROFILE_REL).is_file()
    assert not (world.project / PROFILE_REL).is_symlink()
    assert not (world.project / LOCK_REL).exists()


def test_init_lock_with_a_complete_profile_still_writes_the_lockfile(world):
    """An ordinary run, no link anywhere, is as it was: the lockfile is written
    from the project's own profile and carries its values."""
    world = _no_lockfile_world(world)
    (world.project / PROFILE_REL).write_text(_complete_profile("OrdinaryName"), encoding="utf-8")
    proc = upgrade(world.project, "--init-lock")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    first_line = proc.stdout.splitlines()[0]
    assert first_line.startswith(f"Wrote migrated {LOCK_REL} (") and first_line.endswith(" files).")
    assert read_lock(world.project)["tokens"]["project_name"] == "OrdinaryName"


def test_init_lock_with_a_lockfile_already_there_still_changes_nothing(world):
    """An ordinary run, no link anywhere, is as it was: it says so and exits 0."""
    before = snapshot(world.project)
    proc = upgrade(world.project, "--init-lock")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout == ""
    assert proc.stderr == f"  [info] {LOCK_REL} already exists; nothing to migrate.\n"
    assert snapshot(world.project) == before


# --- the lockfile itself -------------------------------------------------------


@needs_links
@pytest.mark.parametrize("what", ["valid-lockfile-elsewhere", "json-that-is-no-lockfile", "dangling"])
def test_a_lockfile_that_is_a_link_is_refused_and_never_written(world, what):
    """The lockfile was read through whatever it was and written back through it
    by `--apply` and `--finalize`.  A link at its name stops every action before
    anything reads it."""
    lock_path = world.project / LOCK_REL
    outside_lock = world.outside / "lock.yml"
    if what == "valid-lockfile-elsewhere":
        lock = read_lock(world.project)
        lock["cairn_version"] = "0.0.1-outside"
        write_lock(world.project, lock)
        shutil.move(str(lock_path), str(outside_lock))
    elif what == "json-that-is-no-lockfile":
        lock_path.unlink()
        outside_lock.write_text('{"auths": {"registry": "token"}}\n', encoding="utf-8")
    else:
        lock_path.unlink()
    link(outside_lock, lock_path)
    outside_before = snapshot(world.outside)
    for action in _ALL_ACTIONS:
        proc = upgrade(world.project, *action)
        said = proc.stdout + proc.stderr
        if action[0] == "--adopt-collisions":
            # The reader's own refusal propagates as an exception here (a pinned
            # behaviour of that action); it must still read and write nothing.
            assert proc.returncode != 0 and "refusing to read a non-regular file" in said
            continue
        assert "Traceback" not in said, action
        assert proc.returncode in ((1, 2) if what == "dangling" else (2,)), (
            f"{action}: exit {proc.returncode}\n{said[-600:]}")
        if proc.returncode == 2:
            assert "refus" in proc.stderr, action
    assert snapshot(world.outside) == outside_before, "something outside the project changed"
    assert lock_path.is_symlink(), "the link must be left as it was"


@needs_links
def test_a_lockfile_link_swapped_in_after_the_check_is_never_written_through(world):
    """The two lockfile writes check their own destination.  The command-level
    check ran earlier, so a link put in place after it must still be refused."""
    outside_lock = world.outside / "lock.yml"
    outside_lock.write_text(json.dumps({"a": 1}), encoding="utf-8")
    lock = read_lock(world.project)
    lock_path = world.project / LOCK_REL
    lock_path.unlink()
    link(outside_lock, lock_path)
    outside_before = snapshot(world.outside)
    with pytest.raises(ScaffoldSecurityError):
        UP._cmd_finalize_lockfile(world.project, lock, only=None, force=True)
    assert snapshot(world.outside) == outside_before


# --- the saved commit name -----------------------------------------------------


@needs_git
def test_a_saved_commit_name_that_is_an_option_never_reaches_git(tmp_path):
    """The lockfile's `cairn_commit` was handed to `git rev-list` unchecked, so
    `--output=<path>` made the read-only report create a file there."""
    outdir = tmp_path / "out"
    outdir.mkdir()
    said = LF._behind_by_n(CAIRN_ROOT, f"--output={outdir / 'x'}", "HEAD")
    assert "check unavailable" in said
    assert list(outdir.iterdir()) == [], "git ran with the lockfile's text as an option"


@pytest.mark.parametrize("name", [
    "-1", "HEAD", "main", "ABCDEF1", "abc", "a" * 41, "abc 123", "abc1234\n", 7, ["a"],
])
def test_only_a_short_or_full_hex_commit_name_reaches_git(monkeypatch, name):
    """The message for a name that is refused and for a name git cannot place is
    the same text, so the text cannot show that git was not run.  Git is
    replaced by a recorder instead, and it must never be called."""
    calls: list[tuple] = []

    def recorder(*args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args, 1, "", "")

    monkeypatch.setattr(subprocess, "run", recorder)
    said = LF._behind_by_n(CAIRN_ROOT, name, "HEAD")
    assert "check unavailable" in said
    assert calls == [], "git was run with a name that is not a short or full hex commit"


@pytest.mark.parametrize("name", ["abc1234", "a" * 40])
def test_a_short_or_full_hex_commit_name_does_reach_git(monkeypatch, name):
    """The control for the test above: the recorder sees a call that is made."""
    calls: list[tuple] = []

    def recorder(*args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, "3\n", "")

    monkeypatch.setattr(subprocess, "run", recorder)
    said = LF._behind_by_n(CAIRN_ROOT, name, "HEAD")
    assert [argv[0][-1] for argv in calls] == [f"{name}..HEAD"]
    assert "behind canonical by 3 commit" in said


@needs_git
def test_a_four_character_saved_commit_still_gets_its_behind_by_count(tmp_path):
    """Git's shortest abbreviation is 4 characters, and the lockfile records
    `git rev-parse --short`, so a real saved commit can be that short.  A scratch
    repository with fixed dates gives the same commit names on every run, so the
    4-character name is never ambiguous."""
    repo = tmp_path / "repo"
    repo.mkdir()
    env = {**os.environ, **_GIT_ENV, "GIT_AUTHOR_DATE": "2020-01-01T00:00:00+0000",
           "GIT_COMMITTER_DATE": "2020-01-01T00:00:00+0000"}

    def run(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True,
                              text=True, env=env).stdout.strip()

    run("init", "-q")
    run("commit", "-q", "--allow-empty", "-m", "one")
    run("commit", "-q", "--allow-empty", "-m", "two")
    older = run("rev-parse", "--short=4", "HEAD~1")
    assert len(older) == 4, "the scratch repository's commit name is ambiguous at 4 characters"
    assert "behind canonical by 1 commit" in LF._behind_by_n(repo, older, run("rev-parse", "HEAD"))


@needs_git
def test_a_real_saved_commit_still_gets_its_behind_by_count():
    head = subprocess.run(["git", "-C", str(CAIRN_ROOT), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    older = subprocess.run(["git", "-C", str(CAIRN_ROOT), "rev-parse", "HEAD~1"],
                           capture_output=True, text=True)
    if older.returncode != 0:
        pytest.skip("the checkout has no earlier commit")
    assert "behind canonical by 1 commit" in LF._behind_by_n(CAIRN_ROOT, older.stdout.strip(), head)
    assert "behind canonical by 1 commit" in LF._behind_by_n(CAIRN_ROOT, older.stdout.strip()[:7], head)
    assert "current" in LF._behind_by_n(CAIRN_ROOT, head, head)


def test_a_saved_commit_name_that_is_an_option_creates_nothing_through_the_command(world):
    marker = world.outside / "created-by-git"
    lock = read_lock(world.project)
    lock["cairn_commit"] = f"--output={marker}"
    write_lock(world.project, lock)
    outside_before = snapshot(world.outside)
    proc = upgrade(world.project, "--plan")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "check unavailable" in proc.stdout + proc.stderr
    assert snapshot(world.outside) == outside_before
    assert not list(world.outside.glob("created-by-git*"))


# --- names that reach the terminal -----------------------------------------------

_HOSTILE_NAME = "x\x1b[2J\x1b[31mFORGED\nforged: line"


def _assert_nothing_forged(proc: subprocess.CompletedProcess[str]) -> None:
    said = proc.stdout + proc.stderr
    assert "\x1b" not in said
    assert not any(line.startswith("forged") for line in said.splitlines())


@pytest.mark.parametrize("value", [
    _HOSTILE_NAME, "", 7, None, ["a"], "a\u2028b", "a\u202eb", "a\x00b", "a\x9bb",
])
def test_a_module_name_that_is_not_plain_text_is_refused_on_every_action(world, value):
    """The report prints each module name the lockfile lists; an escape sequence
    in one would be typed at the operator's terminal."""
    lock = read_lock(world.project)
    lock["modules"] = [*lock["modules"], value]
    write_lock(world.project, lock)
    before = snapshot(world.project)
    for action in _ACTIONS:
        proc = upgrade(world.project, *action)
        assert_refused(proc, world, "modules")
        _assert_nothing_forged(proc)
    assert snapshot(world.project) == before


@pytest.mark.parametrize("modules", ["claim-check", {"a": 1}, 7])
def test_a_module_list_that_is_not_a_list_is_refused(world, modules):
    lock = read_lock(world.project)
    lock["modules"] = modules
    write_lock(world.project, lock)
    assert_refused(upgrade(world.project, "--plan"), world, "modules")


def test_a_lockfile_with_ordinary_module_names_is_not_refused(world):
    proc = upgrade(world.project, "--plan")
    assert proc.returncode == 0, proc.stderr
    lock = read_lock(world.project)
    lock["modules"] = []
    write_lock(world.project, lock)
    assert upgrade(world.project, "--plan").returncode == 0
    del lock["modules"]
    write_lock(world.project, lock)
    assert "refus" not in upgrade(world.project, "--plan").stderr


def _project_with_a_profile(world: World) -> None:
    """So that no profile self-heal write sits between the project and a
    refusal: the project is then unchanged by a refused `--apply`."""
    (world.project / PROFILE_REL).write_text("project_name: x\n", encoding="utf-8")


def _plant(world: World, **changes: object) -> Path:
    stage = _plant_stage(world)
    meta_path = stage / "stage-metadata.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta.update(changes)
    meta_path.write_text(json.dumps(meta), encoding="utf-8")
    return stage


@pytest.mark.parametrize("field", [
    "review_only", "module_blocked", "expected_absent", "staged_files",
])
@pytest.mark.parametrize("name", [
    _HOSTILE_NAME, "../escape.md", "/etc/hosts", 7, ".git/description", ".GIT/hooks/post-merge",
])
def test_apply_refuses_a_review_area_that_names_an_unplain_file(world, field, name):
    """The review area is project data: a repository can carry one whose
    bookkeeping names whatever it likes, and `--apply` printed those names.  A
    name inside Git's own folder is refused here as it is in a lockfile record."""
    _project_with_a_profile(world)
    _plant(world, **{field: [name]})
    before = snapshot(world.project)
    proc = upgrade(world.project, "--apply")
    assert_plain_refusal(proc)
    _assert_nothing_forged(proc)
    assert snapshot(world.project) == before


@pytest.mark.parametrize("field", ["kinds", "new_entries"])
def test_apply_refuses_a_review_area_whose_keys_are_not_plain_names(world, field):
    _project_with_a_profile(world)
    _plant(world, **{field: {_HOSTILE_NAME: {"src": "core/NOTICE.md"}}})
    before = snapshot(world.project)
    proc = upgrade(world.project, "--apply")
    assert_plain_refusal(proc)
    _assert_nothing_forged(proc)
    assert snapshot(world.project) == before


@pytest.mark.parametrize("field", ["new_commit", "new_version"])
@pytest.mark.parametrize("value", [_HOSTILE_NAME, 7, ["a"], None])
def test_apply_refuses_a_review_area_whose_version_is_not_plain_text(world, field, value):
    """`new_commit` is printed on success; a hostile one must stop the apply
    before anything is swapped in."""
    _project_with_a_profile(world)
    _plant(world, **{field: value})
    before = snapshot(world.project)
    proc = upgrade(world.project, "--apply")
    assert_plain_refusal(proc)
    _assert_nothing_forged(proc)
    assert snapshot(world.project) == before


@pytest.mark.parametrize("field", ["staged_files", "review_only", "kinds"])
def test_apply_refuses_a_review_area_whose_bookkeeping_has_the_wrong_shape(world, field):
    _project_with_a_profile(world)
    _plant(world, **{field: 7})
    proc = upgrade(world.project, "--apply")
    assert_plain_refusal(proc)


@pytest.mark.parametrize("metadata", [[], ["staged_files"], 7, "text", None])
def test_apply_refuses_a_review_area_whose_metadata_is_not_an_object(world, metadata):
    """`stage-metadata.json` that parses but is not a JSON object has no names to
    judge; it is refused in the same plain words, not left to fail on `.get`."""
    _project_with_a_profile(world)
    stage = _plant_stage(world)
    (stage / "stage-metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
    before = snapshot(world.project)
    proc = upgrade(world.project, "--apply")
    assert_plain_refusal(proc)
    assert snapshot(world.project) == before


def test_apply_still_applies_a_review_area_of_plain_names(world):
    """What the refusals above leave alone: a stage of plain names applies."""
    _project_with_a_profile(world)
    (world.project / "docs").mkdir(exist_ok=True)
    (world.project / "docs" / "notes.md").write_text("old\n", encoding="utf-8")
    _plant_stage(world)
    proc = upgrade(world.project, "--apply")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (world.project / "docs" / "notes.md").read_text(encoding="utf-8") == "staged notes\n"


# --- the refusal's own advice ----------------------------------------------------


@needs_links
def test_a_linked_project_folder_is_told_to_replace_the_link_not_restore_the_lockfile(world):
    """The adopter whose `dev/modules` was moved beside the project and linked
    back is right to be refused at `--plan`; the advice must name the link."""
    moved = world.outside / "modules"
    shutil.move(str(world.project / "dev" / "modules"), str(moved))
    link(moved, world.project / "dev" / "modules")
    proc = upgrade(world.project, "--plan")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "is a link that leads out" in proc.stderr
    assert "Replace the link" in proc.stderr
    assert "dev/.cairn/cairn-lock.yml" in proc.stderr, "a changed record is still a cause"
    assert str(world.outside) not in proc.stdout + proc.stderr


def test_a_name_of_the_wrong_shape_keeps_the_restore_the_lockfile_advice(world):
    add_record(world.project, src="core/NOTICE.md", dst="../x.md")
    proc = upgrade(world.project, "--plan")
    assert_refused(proc, world, "dst")
    assert "restore it from a copy you trust" in proc.stderr
    assert "Replace the link" not in proc.stderr


# --- a linked vendor wrapper -----------------------------------------------------


@needs_links
def test_a_linked_vendor_wrapper_is_not_taken_for_the_wrapper_by_finalize(world):
    """With `VENDOR.md` gone and `CLAUDE.md` a link to a file outside, `--finalize`
    recorded a digest of that file in the lockfile and renamed the record."""
    (world.project / "VENDOR.md").unlink()
    link(world.secret, world.project / "CLAUDE.md")
    outside_before = snapshot(world.outside)
    proc = upgrade(world.project, "--finalize", "--force")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "missing on disk" in proc.stderr
    assert_nothing_left_the_tree(world, outside_before)
    assert record_for(read_lock(world.project), "VENDOR.md")["src"] == "core/VENDOR.md"


@needs_links
def test_finalize_over_a_linked_vendor_wrapper_names_the_link(world):
    """The wrapper is not found when its file is a link, so `VENDOR.md` is
    reported as missing -- true, and no help to someone whose `CLAUDE.md` is
    right there.  The message now names the link and says what to do; the exit
    code is still 1, and nothing is read through the link."""
    (world.project / "VENDOR.md").unlink()
    link(world.secret, world.project / "CLAUDE.md")
    outside_before = snapshot(world.outside)
    proc = upgrade(world.project, "--finalize", "--force")
    said = proc.stdout + proc.stderr
    assert proc.returncode == 1, said
    assert "missing on disk" in proc.stderr
    assert "CLAUDE.md is a link" in proc.stderr
    assert "Replace it with a regular file" in proc.stderr
    assert world.marker not in said
    assert "Traceback" not in said
    assert_nothing_left_the_tree(world, outside_before)


def test_finalize_over_an_absent_vendor_wrapper_keeps_its_plain_message(world):
    """No link: the message is the one it always was, word for word."""
    (world.project / "VENDOR.md").unlink()
    proc = upgrade(world.project, "--finalize", "--force")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert proc.stdout == ""
    assert proc.stderr == (
        "error: 1 tracked file(s) missing on disk -- cannot finalize "
        "(fix or re-install first):\n  VENDOR.md\n")


@needs_links
@pytest.mark.parametrize("name", ["CLAUDE.md", "my-wrapper.md"])
def test_a_wrapper_that_is_a_link_is_never_resolved(tmp_path, name):
    """Both tiers: a known vendor file name, and a custom name that imports
    `@AGENTS.md`."""
    real = tmp_path / "elsewhere.md"
    real.write_text("@AGENTS.md\n", encoding="utf-8")
    project = tmp_path / "proj"
    project.mkdir()
    link(real, project / name)
    assert UP._resolve_vendor_wrapper(project, set()) is None


@pytest.mark.parametrize("name", ["CLAUDE.md", "my-wrapper.md"])
def test_a_wrapper_that_is_a_regular_file_is_still_resolved(tmp_path, name):
    (tmp_path / name).write_text("@AGENTS.md\n", encoding="utf-8")
    assert UP._resolve_vendor_wrapper(tmp_path, set()) == name


# --- Git's own folder --------------------------------------------------------------


@pytest.mark.parametrize("value", [
    ".git/config", ".GIT/hooks/pre-commit", ".Git/description", ".git", ".git/",
    "./.git/config",
])
@pytest.mark.parametrize("field", ["dst", "base_cache"])
def test_the_guard_refuses_a_name_inside_gits_own_folder(tmp_path, value, field):
    with pytest.raises(ScaffoldSecurityError):
        UP._contained_lockfile_path(tmp_path, value, field, "the project")


@pytest.mark.parametrize("value", [
    ".gitignore", ".github/workflows/x.yml", ".gitattributes", "docs/.git-notes.md",
    "gitconfig", ".gi/t",
])
def test_the_guard_lets_names_that_only_look_like_gits_folder_through(tmp_path, value):
    assert UP._contained_lockfile_path(tmp_path, value, "dst", "the project") == tmp_path / value


@needs_git
@pytest.mark.parametrize("field", ["dst", "base_cache"])
def test_a_record_that_names_a_file_inside_git_is_refused_on_every_action(world, field):
    """A record whose `dst` is `.git/description`, verbatim, with the hashes of
    the bytes `git init` writes there, made `--apply` replace that file with a
    template."""
    git(world.project, "init", "-q")
    description = world.project / ".git" / "description"
    assert description.is_file()
    if field == "dst":
        digest = "sha256:" + hashlib.sha256(description.read_bytes()).hexdigest()
        add_record(world.project, src="core/NOTICE.md", dst=".git/description", digest=digest)
    else:
        lock = read_lock(world.project)
        record_for(lock, "AGENTS.md")["base_cache"] = ".git/description"
        write_lock(world.project, lock)
    before = description.read_bytes()
    for action in _ACTIONS:
        assert_refused(upgrade(world.project, *action), world, field)
    assert description.read_bytes() == before
    assert not (world.project / STAGE_REL).exists()
