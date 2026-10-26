"""`upgrade` never reads a path outside the tree the lockfile names it in.

A project's lockfile (`dev/.cairn/cairn-lock.yml`) is project data: a cloned
repository can carry one that somebody else wrote.  Each file record names
three paths, and `upgrade` reads all of them:

* `src` -- the upstream template, read from **Cairn's own `templates/` tree**;
* `dst` -- the project file, read from **the project**;
* `base_cache` -- the saved merge ancestor, read from **the project**.

None of them may lead out of its tree, by `..`, by an absolute name, or through
a link.  Before the fix a `src` of `../../..` made `upgrade --stage` copy any
file the user could read into the review area, and `--apply` then wrote that
text into a tracked project file.

Four groups of tests, because they ask different questions:

* **Project data alone.**  The real command line (`bootstrap/scaffold.py`, a
  subprocess) runs `upgrade` over a real install whose lockfile -- or whose
  folders -- were edited, with no patching.  Every action that reads the
  lockfile must refuse in fixed words, with a remedy, exit 2, and change
  nothing.  Nothing from outside the tree may reach the project, the review
  area, or the terminal.
* **The staged upgrade is project data too.**  `--apply` trusts the review area
  it finds; a link planted in it must be refused, not followed.
* **The guards themselves.**  The shapes the guard rules out, and the one
  property the command line cannot show: the upstream reader checks the path
  *before* it reads.
* **Wiring.**  Where each guard sits is pinned from the source, and the
  inventory of guards names each one.

Ordinary upgrade behaviour is pinned in `test_upgrade.py`; this file pins what
`upgrade` refuses.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_upgrade_lockfile_path_containment.py
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import ScaffoldSecurityError  # noqa: E402  (the facade loads the engine)
from bootstrap._scaffold import upgrade as UP  # noqa: E402

SCAFFOLD = CAIRN_ROOT / "bootstrap" / "scaffold.py"
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
UPGRADE_SOURCE = CAIRN_ROOT / "bootstrap" / "_scaffold" / "upgrade.py"
MUTATION_INVENTORY = CAIRN_ROOT / "bootstrap" / "_scaffold" / "SECURITY_MUTATIONS.md"
LOCK_REL = "dev/.cairn/cairn-lock.yml"
STAGE_REL = "dev/.cairn-upgrade"
BENIGN_NOTES = "notes the repository author committed\n"

#: Every upgrade action that reads the lockfile and so must refuse a bad record.
_ACTIONS = (
    ("--plan",),
    ("--stage",),
    ("--apply",),
    ("--finalize", "--force"),
    ("--adopt-collisions", "x@" + "0" * 64 + "@" + "0" * 64),
    ("--remove-retired",),
)

needs_links = pytest.mark.skipif(
    not hasattr(os, "symlink"), reason="symlinks are not available here")


# --- a real install, and the hostile data around it ---------------------------


@pytest.fixture(scope="module")
def pristine(tmp_path_factory) -> Path:
    """One real install through the real command line, copied for each test."""
    root = tmp_path_factory.mktemp("pristine")
    project = root / "proj"
    project.mkdir()
    profile = root / "profile.yml"
    profile.write_text(
        "project_name: LockPaths\ntest_command: pytest\npreset: solo-greenfield\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(SCAFFOLD), "--config", str(profile), "--target", str(project),
         "--cairn-root", str(CAIRN_ROOT), "--allow-dev", "--non-interactive"],
        capture_output=True, text=True, timeout=300,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert proc.returncode == 0, proc.stderr
    return project


class World(NamedTuple):
    project: Path
    outside: Path     # a folder beside the project: nothing in it may be read or changed
    secret: Path      # a file in it that holds the marker
    marker: str


@pytest.fixture
def world(pristine, tmp_path) -> World:
    project = tmp_path / "proj"
    shutil.copytree(pristine, project, symlinks=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    marker = "OUTSIDE-" + secrets.token_hex(8)
    secret = outside / "secret.md"
    secret.write_text(f"{marker}\nsecond line {marker}\n", encoding="utf-8")
    return World(project, outside, secret, marker)


def upgrade(project: Path, *flags: str) -> subprocess.CompletedProcess[str]:
    """The real command line, as a person runs it."""
    return subprocess.run(
        [sys.executable, str(SCAFFOLD), "upgrade", *flags,
         "--target", str(project), "--cairn-root", str(CAIRN_ROOT)],
        capture_output=True, text=True, timeout=300, cwd=str(project.parent),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def read_lock(project: Path) -> dict:
    lines = (project / LOCK_REL).read_text(encoding="utf-8").splitlines()
    return json.loads("\n".join(ln for ln in lines if not ln.lstrip().startswith("#")))


def write_lock(project: Path, lock: dict) -> None:
    path = project / LOCK_REL
    header = [ln for ln in path.read_text(encoding="utf-8").splitlines()
              if ln.lstrip().startswith("#")]
    path.write_text("\n".join(header) + "\n" + json.dumps(lock, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def record_for(lock: dict, dst: str) -> dict:
    return next(rec for rec in lock["files"] if rec["dst"] == dst)


def add_record(project: Path, *, src: str, dst: str, digest: str | None = None) -> None:
    """A new verbatim record.  *digest* is the hash both fields carry."""
    digest = digest or "sha256:" + "0" * 64
    lock = read_lock(project)
    lock["files"].append(
        {"src": src, "dst": dst, "verbatim": True, "hash": digest, "base_hash": digest})
    write_lock(project, lock)


def add_notes_record(project: Path, *, src: str, dst: str = "docs/notes.md") -> None:
    """A new record over a file the repository itself carries.  Its hashes match
    the file as committed, so the engine reads it as an untouched copy with an
    upstream change waiting -- the shape that is staged and applied without a
    word from anyone."""
    path = project / dst
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(BENIGN_NOTES, encoding="utf-8")
    add_record(project, src=src, dst=dst,
               digest="sha256:" + hashlib.sha256(path.read_bytes()).hexdigest())


def snapshot(root: Path) -> dict[str, tuple]:
    """Every file (bytes) and link (target) under *root*, with no link followed."""
    found: dict[str, tuple] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(dirpath)
        for name in dirnames + filenames:
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                found[rel] = ("link", os.readlink(path))
            elif path.is_file():
                found[rel] = ("file", path.read_bytes())
    return found


def from_templates(path: Path) -> str:
    """The `src` a lockfile would need to reach *path* from Cairn's templates folder."""
    return os.path.relpath(path, TEMPLATES_ROOT)


def assert_refused(proc: subprocess.CompletedProcess[str], world: World, field: str) -> None:
    """Fixed words, a remedy, exit 2 -- and nothing from outside in what was said."""
    said = proc.stdout + proc.stderr
    assert proc.returncode == 2, f"expected a refusal (exit 2), got {proc.returncode}:\n{said[-900:]}"
    assert "Traceback" not in said
    assert f"{field!r}" in proc.stderr, "the refusal must name the field it refused"
    assert "refus" in proc.stderr
    assert "dev/.cairn/cairn-lock.yml" in proc.stderr, "the refusal must say where to look"
    assert world.marker not in said
    assert "\x1b" not in said


def assert_nothing_left_the_tree(world: World, outside_before: dict[str, tuple]) -> None:
    """The marker, and a digest of the outside file, are nowhere in the project,
    and the outside folder is exactly as it was."""
    digest = hashlib.sha256(world.secret.read_bytes()).hexdigest().encode()
    for path in world.project.rglob("*"):
        if path.is_file() and not path.is_symlink():
            data = path.read_bytes()
            assert world.marker.encode() not in data, f"outside text reached {path}"
            assert digest not in data, f"a digest of an outside file was recorded in {path}"
    assert snapshot(world.outside) == outside_before


# --- project data alone: the upstream side (`src`) ----------------------------


def test_a_src_that_climbs_out_of_the_source_tree_never_reaches_the_project(world):
    """The reported defect, end to end: a new record whose `src` is `../../..` to a
    file outside Cairn made `--stage` copy that file and `--apply` write it into a
    tracked project file, every step exiting 0."""
    add_notes_record(world.project, src=from_templates(world.secret))
    before, outside_before = snapshot(world.project), snapshot(world.outside)
    for action in _ACTIONS:
        assert_refused(upgrade(world.project, *action), world, "src")
    assert snapshot(world.project) == before, "a refusal must change nothing"
    assert not (world.project / STAGE_REL).exists()
    assert (world.project / "docs/notes.md").read_text(encoding="utf-8") == BENIGN_NOTES
    assert_nothing_left_the_tree(world, outside_before)


def test_an_absolute_src_never_reaches_the_project(world):
    add_notes_record(world.project, src=str(world.secret))
    before, outside_before = snapshot(world.project), snapshot(world.outside)
    for action in _ACTIONS:
        assert_refused(upgrade(world.project, *action), world, "src")
    assert snapshot(world.project) == before
    assert_nothing_left_the_tree(world, outside_before)


def test_a_mergeable_records_src_cannot_be_pointed_outside_either(world):
    """The same door on the merged-text path rather than the verbatim path: the
    outside text would be the upstream side of a three-way merge."""
    lock = read_lock(world.project)
    record_for(lock, "NOTICE.md")["src"] = from_templates(world.secret)
    write_lock(world.project, lock)
    outside_before = snapshot(world.outside)
    for action in _ACTIONS:
        assert_refused(upgrade(world.project, *action), world, "src")
    assert_nothing_left_the_tree(world, outside_before)


# --- project data alone: the project side (`dst`, `base_cache`) ---------------


@pytest.mark.parametrize("how", ["dotdot", "absolute"])
def test_a_dst_that_leaves_the_project_is_refused_on_every_action(world, how):
    """`--stage` already refused to write there; the rest read the file first and
    `--finalize` recorded a digest of it in the lockfile."""
    target = world.outside / "target.md"
    target.write_text("outside file\n", encoding="utf-8")
    dst = str(target) if how == "absolute" else os.path.relpath(target, world.project)
    add_record(world.project, src="core/NOTICE.md", dst=dst)
    before, outside_before = snapshot(world.project), snapshot(world.outside)
    for action in _ACTIONS:
        assert_refused(upgrade(world.project, *action), world, "dst")
    assert snapshot(world.project) == before
    assert snapshot(world.outside) == outside_before


@needs_links
def test_a_dst_through_a_folder_link_that_leaves_the_project_is_refused(world):
    """The name is plain; a folder in it is a link out.  The refusal must not say
    where the link points."""
    (world.outside / "target.md").write_text("outside file\n", encoding="utf-8")
    try:
        os.symlink(world.outside, world.project / "docs" / "link")
    except OSError:
        pytest.skip("symlinks are not available here")
    add_record(world.project, src="core/NOTICE.md", dst="docs/link/target.md")
    outside_before = snapshot(world.outside)
    for action in _ACTIONS:
        proc = upgrade(world.project, *action)
        assert_refused(proc, world, "dst")
        assert str(world.outside) not in proc.stdout + proc.stderr, (
            "where a link points is not the project's business to print")
    assert snapshot(world.outside) == outside_before


@pytest.mark.parametrize("how", ["absolute", "dotdot"])
def test_a_base_cache_that_leaves_the_project_is_refused_on_every_action(world, how):
    """The saved merge ancestor is read from the project; a name that leads out of
    it is as bad as a `src` that does."""
    lock = read_lock(world.project)
    record_for(lock, "AGENTS.md")["base_cache"] = (
        str(world.secret) if how == "absolute"
        else os.path.relpath(world.secret, world.project))
    write_lock(world.project, lock)
    before, outside_before = snapshot(world.project), snapshot(world.outside)
    for action in _ACTIONS:
        assert_refused(upgrade(world.project, *action), world, "base_cache")
    assert snapshot(world.project) == before
    assert_nothing_left_the_tree(world, outside_before)


@needs_links
def test_a_saved_ancestor_folder_that_is_a_link_out_is_refused_with_a_clean_lockfile(world):
    """No record was edited: the folder of saved ancestors is a link to a folder
    outside, which a checkout can carry."""
    cache = world.project / "dev" / ".cairn" / "base"
    shutil.copytree(cache, world.outside / "base")
    shutil.rmtree(cache)
    try:
        os.symlink(world.outside / "base", cache)
    except OSError:
        pytest.skip("symlinks are not available here")
    outside_before = snapshot(world.outside)
    for action in _ACTIONS:
        proc = upgrade(world.project, *action)
        assert_refused(proc, world, "base_cache")
        assert str(world.outside) not in proc.stdout + proc.stderr
    assert snapshot(world.outside) == outside_before


@pytest.mark.parametrize("hostile", [
    "AGENTS.md\x1b[2J\x1b[31mDONE", "docs/a\nforged: line", "docs/a\x00b", "docs/a\rb",
    "docs/a\x9b31mb", "docs/a\u2028forged: line", "docs/a\u202eb",
])
def test_a_control_character_in_a_record_never_reaches_the_terminal(world, hostile):
    """The report prints each `dst`; an escape sequence in one would be typed at
    the operator's terminal, and a line break would forge a line of the report."""
    add_record(world.project, src="core/NOTICE.md", dst=hostile)
    for action in _ACTIONS:
        proc = upgrade(world.project, *action)
        assert_refused(proc, world, "dst")
        said = proc.stdout + proc.stderr
        assert not any(ln.startswith("forged") for ln in said.splitlines())
        assert "\r" not in said and "\x00" not in said


@needs_links
def test_a_pristine_lockfile_and_a_link_that_stays_inside_the_project_are_not_refused(world):
    """The rule rules out leaving the tree, not links: an install that is untouched
    reports normally, and so does one whose notes file is a link to another file
    inside the project."""
    proc = upgrade(world.project, "--plan")
    assert proc.returncode == 0, proc.stderr
    assert "refus" not in proc.stderr
    add_notes_record(world.project, src="core/NOTICE.md")
    notes, real = world.project / "docs" / "notes.md", world.project / "docs" / "real.md"
    real.write_text("real\n", encoding="utf-8")
    notes.unlink()
    try:
        os.symlink(real, notes)
    except OSError:
        pytest.skip("symlinks are not available here")
    proc = upgrade(world.project, "--plan")
    assert proc.returncode == 0, proc.stderr
    assert "refus" not in proc.stderr


# --- the staged upgrade is project data too -----------------------------------


def _plant_stage(world: World) -> Path:
    """A review area as `--stage` would have left it, built from scratch -- what a
    repository that force-added the (normally ignored) folder would carry.  Its
    bookkeeping matches the lockfile, so the apply takes it for its own."""
    lock = read_lock(world.project)
    stage = world.project / STAGE_REL
    (stage / "files" / "docs").mkdir(parents=True)
    (stage / "files" / "docs" / "notes.md").write_text("staged notes\n", encoding="utf-8")
    meta = {
        "lock_commit": lock.get("cairn_commit"), "lock_version": lock.get("cairn_version"),
        "to_ref": None, "tokens": lock.get("tokens"), "modules": lock.get("modules"),
        "new_version": "9.9.9", "new_commit": "0" * 40, "staged_files": ["docs/notes.md"],
        "kinds": {"docs/notes.md": "clean"}, "ours_hashes": {}, "expected_absent": [],
        "review_only": [], "module_blocked": [], "new_entries": {}, "verbatim_rehash": [],
        "new_profile": None,
    }
    (stage / "stage-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    return stage


@needs_links
@pytest.mark.parametrize(
    "where", ["staged-file", "new-base-file", "staged-folder", "metadata-file"])
def test_apply_refuses_a_staged_upgrade_that_holds_a_link(world, where):
    """`--apply` read the staged copy through whatever the link named and wrote it
    over a project file -- or into the saved ancestors -- saying `Applied 1 file(s)`."""
    notes = world.project / "docs" / "notes.md"
    notes.write_text(BENIGN_NOTES, encoding="utf-8")
    stage = _plant_stage(world)
    try:
        if where == "staged-file":
            (stage / "files" / "docs" / "notes.md").unlink()
            os.symlink(world.secret, stage / "files" / "docs" / "notes.md")
        elif where == "new-base-file":
            (stage / "new-base" / "docs").mkdir(parents=True)
            os.symlink(world.secret, stage / "new-base" / "docs" / "notes.md")
        elif where == "metadata-file":
            (stage / "stage-metadata.json").unlink()
            os.symlink(world.secret, stage / "stage-metadata.json")
        else:
            shutil.rmtree(stage / "files" / "docs")
            (world.outside / "notes.md").write_text(f"{world.marker}\n", encoding="utf-8")
            os.symlink(world.outside, stage / "files" / "docs")
    except OSError:
        pytest.skip("symlinks are not available here")
    outside_before = snapshot(world.outside)
    proc = upgrade(world.project, "--apply")
    said = proc.stdout + proc.stderr
    assert proc.returncode == 2, said[-900:]
    assert "Traceback" not in said
    assert "refus" in proc.stderr
    assert world.marker not in said
    assert notes.read_text(encoding="utf-8") == BENIGN_NOTES
    assert_nothing_left_the_tree(world, outside_before)


def test_a_hand_built_review_area_cannot_make_apply_record_a_path_outside_the_project(world):
    """A new file's saved ancestor is named in the staged record.  The apply read
    that name, hashed whatever file it led to, and wrote both into the lockfile."""
    stage = _plant_stage(world)
    meta_path = stage / "stage-metadata.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["kinds"] = {"docs/notes.md": "new-core"}
    meta["expected_absent"] = ["docs/notes.md"]
    meta["new_entries"] = {"docs/notes.md": {
        "src": "core/NOTICE.md", "verbatim": False, "base_cache": str(world.secret)}}
    meta_path.write_text(json.dumps(meta), encoding="utf-8")
    outside_before = snapshot(world.outside)
    proc = upgrade(world.project, "--apply")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert_nothing_left_the_tree(world, outside_before)
    assert str(world.secret) not in (world.project / LOCK_REL).read_text(encoding="utf-8")
    added = record_for(read_lock(world.project), "docs/notes.md")
    assert added["base_cache"] == "dev/.cairn/base/docs/notes.md"


@needs_links
def test_apply_refuses_a_review_area_that_is_itself_a_link(world):
    """The whole staging folder can be the link."""
    elsewhere = world.outside / "stage-elsewhere"
    shutil.move(str(_plant_stage(world)), str(elsewhere))
    try:
        os.symlink(elsewhere, world.project / STAGE_REL)
    except OSError:
        pytest.skip("symlinks are not available here")
    proc = upgrade(world.project, "--apply")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "refus" in proc.stderr and "Traceback" not in proc.stderr


# --- the guards themselves ------------------------------------------------------


@pytest.mark.parametrize("value", [
    "../x.md", "a/../../x.md", "a/../x.md", "/etc/hosts", "./", ".", "", "a\\b.md",
    "C:/x.md", "C:x.md", "dir:name/x.md", "a/b\x00c", "a/b\nc", "a/b\x1bc", "a/b\x7fc",
    "a/b\rc", "a/b\x9bc", "a/b\x85c", "a/b\u2028c", "a/b\u202ec", "a/b\u00a0c",
    None, 7, ["a"], {"a": 1},
])
def test_the_guard_rules_out_every_shape_that_is_not_a_plain_relative_name(tmp_path, value):
    with pytest.raises(ScaffoldSecurityError):
        UP._contained_lockfile_path(tmp_path, value, "dst", "the project")


@pytest.mark.parametrize("value", [
    "AGENTS.md", "a/b/c.md", ".agents/skills/x/SKILL.md", "dev/.cairn/base/AGENTS.md",
    "a b/c d.md", "a/./b.md", "a//b.md", "a..b/c.md", "..a/b.md", "a/b..",
])
def test_the_guard_lets_a_plain_relative_name_through_and_returns_the_joined_path(tmp_path, value):
    assert UP._contained_lockfile_path(tmp_path, value, "dst", "the project") == tmp_path / value


@needs_links
def test_the_guard_follows_a_link_to_judge_where_the_name_really_leads(tmp_path):
    root = tmp_path / "root"
    (root / "real").mkdir(parents=True)
    out = tmp_path / "out"
    out.mkdir()
    os.symlink(out, root / "to-out")
    os.symlink(root / "real", root / "to-real")
    os.symlink(out / "missing", root / "dangling-out")
    with pytest.raises(ScaffoldSecurityError):
        UP._contained_lockfile_path(root, "to-out/x.md", "dst", "the project")
    with pytest.raises(ScaffoldSecurityError):
        UP._contained_lockfile_path(root, "dangling-out", "dst", "the project")
    assert UP._contained_lockfile_path(root, "to-real/x.md", "dst", "the project") == (
        root / "to-real" / "x.md")


def test_a_refusal_is_fixed_words_the_escaped_name_and_a_remedy(tmp_path):
    hostile = "a/\x1b[31m../" + "x" * 400
    with pytest.raises(ScaffoldSecurityError) as caught:
        UP._contained_lockfile_path(tmp_path, hostile, "src", "the Cairn source tree")
    text = str(caught.value)
    assert "\x1b" not in text and "\n" in text, "one line of fact, one line of remedy"
    assert "'src'" in text and "dev/.cairn/cairn-lock.yml" in text
    assert len(text) < 600, "the lockfile's own text is cut, not echoed whole"
    assert str(tmp_path) not in text


def test_a_refusal_stays_short_whatever_the_value_is(tmp_path):
    for value in ("/" + "\U0001f600" * 500, "\x00" * 500, "../" + "x" * 100000,
                  list(range(100000)), {"k": "v" * 100000}):
        with pytest.raises(ScaffoldSecurityError) as caught:
            UP._contained_lockfile_path(tmp_path, value, "dst", "the project")
        assert len(str(caught.value)) < 600


def test_the_upstream_reader_checks_the_path_before_it_reads_anything(tmp_path):
    """A directory where the outside file would be: a read that ran first would
    fail with the OS's own error instead of the guard's refusal.  Nothing at the
    command line can see this -- the lockfile check refuses first there -- so the
    reader is called directly, for both of its entry points."""
    outside = tmp_path / "outside"
    outside.mkdir()
    for to_ref in (None, "HEAD"):
        for reader in (UP._theirs_bytes, UP._theirs_text):
            with pytest.raises(ScaffoldSecurityError):
                reader(CAIRN_ROOT, TEMPLATES_ROOT, from_templates(outside), to_ref)
            with pytest.raises(ScaffoldSecurityError):
                reader(CAIRN_ROOT, TEMPLATES_ROOT, "/", to_ref)
    assert UP._theirs_bytes(CAIRN_ROOT, TEMPLATES_ROOT, "core/NOTICE.md", None) == (
        (TEMPLATES_ROOT / "core" / "NOTICE.md").read_bytes())
    assert UP._theirs_text(CAIRN_ROOT, TEMPLATES_ROOT, "core/NOTICE.md", None) == (
        (TEMPLATES_ROOT / "core" / "NOTICE.md").read_text(encoding="utf-8"))
    assert UP._theirs_bytes(CAIRN_ROOT, TEMPLATES_ROOT, "core/no-such-template.md", None) is None


def test_the_lockfile_check_judges_what_is_there_and_invents_no_requirement(tmp_path):
    """A record with no path to read is left to the code that needs it."""
    project = tmp_path / "proj"
    project.mkdir()
    UP._check_lockfile_paths({}, project, TEMPLATES_ROOT)
    UP._check_lockfile_paths({"files": None}, project, TEMPLATES_ROOT)
    UP._check_lockfile_paths({"files": []}, project, TEMPLATES_ROOT)
    UP._check_lockfile_paths({"files": [{"dst": "a.md"}, {"src": "core/NOTICE.md"}]},
                             project, TEMPLATES_ROOT)
    for bad in ({"files": {"a": 1}}, {"files": 7}, {"files": ["a.md"]}, {"files": [{"dst": 3}]},
                {"files": [{"dst": "a.md", "base_cache": ""}]},
                {"files": [{"src": "../x"}]}, {"files": [{"dst": "../x"}]}):
        with pytest.raises(ScaffoldSecurityError):
            UP._check_lockfile_paths(bad, project, TEMPLATES_ROOT)


def test_the_lockfile_check_names_the_record_it_refused(tmp_path):
    project = tmp_path / "proj"
    project.mkdir()
    files = [{"src": "core/NOTICE.md", "dst": "a.md"}, {"src": "core/NOTICE.md", "dst": "b.md"},
             {"src": "core/NOTICE.md", "dst": "../c.md"}]
    with pytest.raises(ScaffoldSecurityError) as caught:
        UP._check_lockfile_paths({"files": files}, project, TEMPLATES_ROOT)
    assert "record 3" in str(caught.value)


# --- wiring: pinned from the source --------------------------------------------


def _functions() -> dict[str, ast.FunctionDef]:
    tree = ast.parse(UPGRADE_SOURCE.read_text(encoding="utf-8"))
    return {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}


def _calls(fn: ast.FunctionDef, name: str) -> list[ast.Call]:
    return [n for n in ast.walk(fn)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name]


_READS = {"read_bytes", "read_text", "exists", "is_file", "open", "stat", "iterdir", "rglob"}


def _first_read_line(fn: ast.FunctionDef) -> int | None:
    lines = [n.lineno for n in ast.walk(fn)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and n.func.attr in _READS]
    return min(lines) if lines else None


@pytest.mark.parametrize("name", ["_theirs_text", "_theirs_bytes"])
def test_each_upstream_reader_calls_the_guard_before_its_first_read(name):
    """The pinned set: the functions that build an upstream path from a bare `src`
    string.  A later change that drops the call, or reads first, fails here."""
    fn = _functions()[name]
    guards = _calls(fn, "_contained_lockfile_path")
    assert guards, f"{name} no longer calls the containment guard"
    first_read = _first_read_line(fn)
    assert first_read is not None and min(g.lineno for g in guards) < first_read, (
        f"{name} reads before it checks the path")


def test_the_upgrade_command_checks_the_lockfile_before_anything_acts_on_it():
    fn = _functions()["cmd_upgrade"]
    checks = _calls(fn, "_check_lockfile_paths")
    assert len(checks) == 1, "the lockfile is checked in exactly one place"
    line = checks[0].lineno
    later = ("_cmd_finalize_lockfile", "_cmd_adopt_collisions", "_apply_upgrade",
             "_compute_upgrade", "_write_stage", "_self_heal_profile_config",
             "_print_upgrade_report", "_cmd_remove_retired")
    seen = 0
    for name in later:
        for call in _calls(fn, name):
            seen += 1
            assert call.lineno > line, f"{name} runs before the lockfile is checked"
    assert seen >= 6, "the list of later steps no longer matches the command"


def test_the_lockfile_check_guards_all_three_path_fields():
    fn = _functions()["_check_lockfile_paths"]
    fields = sorted(
        c.args[2].value for c in _calls(fn, "_contained_lockfile_path")
        if len(c.args) >= 3 and isinstance(c.args[2], ast.Constant))
    assert fields == ["base_cache", "dst", "src"]


def test_apply_checks_the_staged_upgrade_for_links_before_it_reads_it():
    fn = _functions()["_apply_upgrade"]
    checks = _calls(fn, "_assert_stage_has_no_links")
    assert checks, "--apply no longer checks the staged upgrade for links"
    first_read = _first_read_line(fn)
    assert first_read is not None and min(c.lineno for c in checks) < first_read


@pytest.mark.parametrize("name", [
    "_contained_lockfile_path", "_check_lockfile_paths", "_assert_stage_has_no_links",
])
def test_the_inventory_of_guards_names_each_one(name):
    assert name in MUTATION_INVENTORY.read_text(encoding="utf-8")
