"""`upgrade --documentation-plan-moved` (defect arc E, chunk C2).

The documentation plan moved from docs/ to dev/ in 0.9. An installed project
(0.8) makes the owner's `git mv`; this command then records the new place in the
lockfile. Promises, one test per row of Detail D5 of the plan:

- It changes only the `dst` of the documentation-plan lock record, and writes
  nothing else; it creates, moves and deletes no file.
- It refuses, with the text of Detail D2 and an exit code, each state it cannot
  record: no move yet, a file at both places, a file at neither, links or
  folders where the file goes, unsaved lockfile edits, a 0.8 layout move still
  ahead, a duplicate or verbatim record, and a failure to read or write.
- Its report line, its refusals and install/UPGRADE.md give the same five steps.

Run from the Cairn repo root:
    python -m pytest tests/test_upgrade_documentation_plan_moved.py
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
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
sys.path.insert(0, str(CAIRN_ROOT))

from install import scaffold  # noqa: E402
from install import verify_integrity  # noqa: E402
from install._scaffold import upgrade  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)

LOCK = "dev/.cairn/cairn-lock.yml"
OLD = "docs/DOCUMENTATION_PLAN.md"
NEW = "dev/DOCUMENTATION_PLAN.md"
BASE_OLD = "dev/.cairn/base/docs/DOCUMENTATION_PLAN.md"
SRC = "modules/default-on/documentation_plan_template.md"
STEPS = [
    "  1. git mv docs/DOCUMENTATION_PLAN.md dev/DOCUMENTATION_PLAN.md",
    "  2. In the files you wrote yourself, change each link to docs/DOCUMENTATION_PLAN.md "
    "so it points at dev/DOCUMENTATION_PLAN.md. Leave files Cairn installed alone: "
    "the ordinary upgrade corrects them.",
    "  3. python install/scaffold.py upgrade --target <repo> --documentation-plan-moved",
    "  4. python install/verify_integrity.py --target <repo>, then the project's link "
    "check if it has one (python dev/tools/link_check.py, installed by doc-drift-prevention)",
    "  5. git add the files you changed and dev/.cairn/cairn-lock.yml, then git commit",
]
LINKS = ("If a check in step 4 names a file Cairn installed, do not edit it: the "
         "ordinary upgrade (upgrade --plan, then --stage and --apply) corrects it.")
MOVED = "--documentation-plan-moved"


def _install(target: Path) -> None:
    """A default install: the default-on documentation-plan module is installed
    (a pinned modules list without it would install neither file)."""
    cfg = target / "profile.yml"
    cfg.write_text("project_name: Moved\ntest_command: pytest\n", encoding="utf-8")
    assert scaffold.main(["--config", str(cfg), "--target", str(target),
                          "--cairn-root", str(CAIRN_ROOT), "--non-interactive"]) == 0


def _upgrade(target: Path, *args: str) -> int:
    return scaffold.main(["upgrade", "--target", str(target),
                          "--cairn-root", str(CAIRN_ROOT), *args])


def _verify(target: Path) -> int:
    return verify_integrity.main(["--target", str(target)])


def _lock(target: Path) -> dict:
    return scaffold.read_lockfile(target)


def _write_lock(target: Path, lock: dict) -> None:
    # Bytes, not text: on Windows write_text would add CRLF, which the edit check
    # then reads as an unsaved edit after a commit made from LF bytes.
    (target / LOCK).write_bytes(scaffold._emit_lock_yaml(lock).encode("utf-8"))


def _doc_record(lock: dict) -> dict:
    (rec,) = [row for row in lock["files"] if row["src"] == SRC]
    return rec


def _as_0_8(target: Path) -> None:
    """Make the installed project look like a 0.8 install: the file is at docs/,
    the record names docs/, and the saved ancestor sits beside it there."""
    lock = _lock(target)
    rec = _doc_record(lock)
    (target / "docs").mkdir(exist_ok=True)
    os.replace(target / NEW, target / OLD)
    if rec.get("base_cache"):
        cache = target / BASE_OLD
        cache.parent.mkdir(parents=True, exist_ok=True)
        os.replace(target / rec["base_cache"], cache)
        rec["base_cache"] = BASE_OLD
    rec["dst"] = OLD
    _write_lock(target, lock)


def _owner_moves(target: Path) -> None:
    """The owner's `git mv docs/DOCUMENTATION_PLAN.md dev/DOCUMENTATION_PLAN.md`."""
    os.replace(target / OLD, target / NEW)


def _moved_project(target: Path) -> None:
    """A 0.8 install whose owner has made the move, ready for the command."""
    _as_0_8(target)
    _owner_moves(target)


def _tree(root: Path) -> dict[str, bytes]:
    """Every file, folder and link under root, by relative path."""
    out: dict[str, bytes] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames + filenames:
            path = Path(dirpath) / name
            key = path.relative_to(root).as_posix()
            if path.is_symlink():
                out[key] = b"link:" + os.readlink(path).encode("utf-8")
            elif path.is_dir():
                out[key + "/"] = b"dir"
            else:
                out[key] = path.read_bytes()
    return out


def _link_or_skip(link: Path, target: Path, *, directory: bool = False) -> None:
    try:
        os.symlink(target, link, target_is_directory=directory)
    except (OSError, NotImplementedError):
        pytest.skip("symbolic links are unavailable on this host")


def _git(target: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(target), "-c", "user.name=test",
                    "-c", "user.email=test@example.invalid", *args],
                   check=True, capture_output=True)


def _commit_all(target: Path) -> None:
    _git(target, "add", "-A")
    _git(target, "commit", "-q", "-m", "snapshot")


def _cut_last_line(target: Path) -> bytes:
    """Cut the last line of the project file and of its saved ancestor, so the
    current template has one line the project lacks. The record's hashes follow
    the cut. Returns the cut line, which the template still carries."""
    lock = _lock(target)
    rec = _doc_record(lock)
    cut = b""
    for path in (target / rec["dst"], target / rec["base_cache"]):
        lines = path.read_bytes().splitlines(keepends=True)
        cut = lines[-1]
        path.write_bytes(b"".join(lines[:-1]))
    rec["base_hash"] = "sha256:" + upgrade._sha256_hex(
        (target / rec["base_cache"]).read_bytes())
    rec["hash"] = "sha256:" + upgrade._sha256_hex((target / rec["dst"]).read_bytes())
    _write_lock(target, lock)
    return cut


def _report_lines(out: str) -> list[str]:
    """The output as lines, the step indent kept, so each step is compared whole."""
    return out.splitlines()


def test_records_a_moved_file(tmp_path, capsys):
    _install(tmp_path)
    _moved_project(tmp_path)
    before_lock = _lock(tmp_path)
    before = _tree(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 0
    out = capsys.readouterr().out
    assert f"Recorded {NEW} as the documentation plan." in out
    assert "Now do steps 4 and 5: run the two checks, then commit." in out
    assert LINKS in out

    after_lock = _lock(tmp_path)
    rec_before = _doc_record(before_lock)
    rec_after = _doc_record(after_lock)
    assert rec_after["dst"] == NEW
    assert {k: v for k, v in rec_after.items() if k != "dst"} == {
        k: v for k, v in rec_before.items() if k != "dst"}
    assert [r for r in after_lock["files"] if r["src"] != SRC] == [
        r for r in before_lock["files"] if r["src"] != SRC]

    after = _tree(tmp_path)
    changed = {key for key in before if before[key] != after.get(key)}
    assert changed == {LOCK}


def test_records_an_edited_file(tmp_path, capsys):
    _install(tmp_path)
    _moved_project(tmp_path)
    (tmp_path / NEW).write_bytes((tmp_path / NEW).read_bytes() + b"\nedited\n")
    edited = (tmp_path / NEW).read_bytes()
    recorded_hash = _doc_record(_lock(tmp_path))["hash"]
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 0
    out = capsys.readouterr().out
    assert "The file differs from the version the lockfile recorded." in out
    assert "--finalize dev/DOCUMENTATION_PLAN.md" in out
    assert "restore the file from a copy you trust" in out
    assert LINKS in out

    assert (tmp_path / NEW).read_bytes() == edited
    assert _doc_record(_lock(tmp_path))["hash"] == recorded_hash
    assert _verify(tmp_path) == 1
    capsys.readouterr()

    assert _upgrade(tmp_path, "--finalize", NEW) == 0
    capsys.readouterr()
    assert _verify(tmp_path) == 0


def test_a_second_run_changes_nothing(tmp_path, capsys):
    _install(tmp_path)
    _moved_project(tmp_path)
    assert _upgrade(tmp_path, MOVED) == 0
    capsys.readouterr()
    before = _tree(tmp_path)

    assert _upgrade(tmp_path, MOVED) == 0
    assert "Nothing to record: the lockfile already records dev/DOCUMENTATION_PLAN.md." \
        in capsys.readouterr().out
    assert _tree(tmp_path) == before


def test_still_at_the_old_place_refuses_and_gives_the_steps(tmp_path, capsys):
    _install(tmp_path)
    _as_0_8(tmp_path)
    before = _tree(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 1
    err = capsys.readouterr().err
    assert "the file is still at docs/DOCUMENTATION_PLAN.md" in err
    for step in STEPS:
        assert step in _report_lines(err)
    assert _tree(tmp_path) == before


def test_a_file_at_both_places_refuses(tmp_path, capsys):
    _install(tmp_path)
    _as_0_8(tmp_path)
    shutil.copyfile(tmp_path / OLD, tmp_path / NEW)
    before = _tree(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 1
    assert "a file is at both docs/DOCUMENTATION_PLAN.md and dev/DOCUMENTATION_PLAN.md" \
        in capsys.readouterr().err
    assert _tree(tmp_path) == before


def test_a_file_missing_from_both_places_refuses(tmp_path, capsys):
    _install(tmp_path)
    _as_0_8(tmp_path)
    (tmp_path / OLD).unlink()
    before = _tree(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 1
    err = capsys.readouterr().err
    assert "neither docs/DOCUMENTATION_PLAN.md nor dev/DOCUMENTATION_PLAN.md" in err
    for step in STEPS:
        assert step in _report_lines(err)
    assert _tree(tmp_path) == before


def test_a_recorded_file_with_an_old_copy_left_is_kept(tmp_path, capsys):
    _install(tmp_path)
    _moved_project(tmp_path)
    assert _upgrade(tmp_path, MOVED) == 0
    (tmp_path / OLD).parent.mkdir(exist_ok=True)
    shutil.copyfile(tmp_path / NEW, tmp_path / OLD)
    before = _tree(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 0
    out = capsys.readouterr().out
    assert ("Nothing to record: the lockfile already records dev/DOCUMENTATION_PLAN.md. "
            "A file is also at docs/DOCUMENTATION_PLAN.md and was left alone.") in out
    assert (tmp_path / OLD).exists()
    assert _tree(tmp_path) == before


@pytest.mark.parametrize("kind", ["folder-at-new", "folder-at-old"])
def test_a_folder_where_the_file_goes_is_refused(tmp_path, capsys, kind):
    _install(tmp_path)
    _as_0_8(tmp_path)
    if kind == "folder-at-new":
        (tmp_path / NEW).mkdir(parents=True)
    else:
        (tmp_path / OLD).unlink()
        (tmp_path / OLD).mkdir()
    before = _tree(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 2
    assert "refused (containment)" in capsys.readouterr().err
    assert _tree(tmp_path) == before


@pytest.mark.parametrize("kind", ["link-at-new", "link-at-old", "docs-is-a-link"])
def test_a_link_where_the_file_goes_is_refused(tmp_path, tmp_path_factory, capsys, kind):
    outside = tmp_path_factory.mktemp("outside")
    (outside / "DOCUMENTATION_PLAN.md").write_bytes(b"outside\n")
    _install(tmp_path)
    _as_0_8(tmp_path)
    if kind == "link-at-new":
        _link_or_skip(tmp_path / NEW, outside / "DOCUMENTATION_PLAN.md")
    elif kind == "link-at-old":
        (tmp_path / OLD).unlink()
        _link_or_skip(tmp_path / OLD, outside / "DOCUMENTATION_PLAN.md")
    else:
        os.replace(tmp_path / OLD, outside / "moved.md")
        (tmp_path / "docs").rmdir()
        _link_or_skip(tmp_path / "docs", outside, directory=True)
    before = _tree(tmp_path)
    outside_before = _tree(outside)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 2
    assert "refused (containment)" in capsys.readouterr().err
    assert _tree(tmp_path) == before
    assert _tree(outside) == outside_before


def test_unsaved_lockfile_edits_refuse_unless_forced(tmp_path, capsys):
    if shutil.which("git") is None:
        pytest.skip("git is not available")
    _install(tmp_path)
    _moved_project(tmp_path)
    _git(tmp_path, "init", "-q")
    _commit_all(tmp_path)
    (tmp_path / LOCK).write_text((tmp_path / LOCK).read_text(encoding="utf-8")
                                 + "# an unsaved edit\n", encoding="utf-8")
    before_lock = (tmp_path / LOCK).read_bytes()
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 1
    assert "the lockfile has unsaved edits; commit them or pass --force" \
        in capsys.readouterr().err
    assert (tmp_path / LOCK).read_bytes() == before_lock
    assert _doc_record(_lock(tmp_path))["dst"] == OLD

    assert _upgrade(tmp_path, MOVED, "--force") == 0
    assert "Recorded dev/DOCUMENTATION_PLAN.md" in capsys.readouterr().out
    assert _doc_record(_lock(tmp_path))["dst"] == NEW


def test_a_0_8_layout_move_still_ahead_refuses(tmp_path, capsys):
    _install(tmp_path)
    _moved_project(tmp_path)
    lock = _lock(tmp_path)
    lock["files"].append({"src": "core/x.md", "dst": upgrade._LAYOUT_MOVES[0][2],
                          "verbatim": True, "hash": "sha256:" + "0" * 64})
    _write_lock(tmp_path, lock)
    before = _tree(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 1
    assert "still has the 0.8 layout migration ahead of it (1 file(s)" \
        in capsys.readouterr().err
    assert _tree(tmp_path) == before


@pytest.mark.parametrize("case", ["two-records", "verbatim"])
def test_two_records_or_a_verbatim_record_refuse(tmp_path, capsys, case):
    _install(tmp_path)
    _moved_project(tmp_path)
    lock = _lock(tmp_path)
    rec = _doc_record(lock)
    if case == "two-records":
        lock["files"].append({"src": SRC, "dst": "docs/OTHER.md",
                              "hash": "sha256:" + "0" * 64})
        expected = "more than once"
    else:
        rec["verbatim"] = True
        expected = "is marked verbatim"
    _write_lock(tmp_path, lock)
    before = _tree(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 1
    assert expected in capsys.readouterr().err
    assert _tree(tmp_path) == before


def test_another_record_already_at_the_new_place_refuses(tmp_path, capsys):
    _install(tmp_path)
    _moved_project(tmp_path)
    lock = _lock(tmp_path)
    lock["files"].append({"src": "core/x.md", "dst": NEW,
                          "hash": "sha256:" + "0" * 64})
    _write_lock(tmp_path, lock)
    before = _tree(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 1
    assert "not one this command records" in capsys.readouterr().err
    assert _tree(tmp_path) == before


@pytest.mark.parametrize("failing", ["lock-write", "layout-read"])
def test_a_failure_to_read_or_write_is_refused_without_a_traceback(
        tmp_path, capsys, monkeypatch, failing):
    _install(tmp_path)
    _moved_project(tmp_path)
    if failing == "lock-write":
        def boom(*_args, **_kwargs):
            raise OSError("simulated write failure")
        monkeypatch.setattr(upgrade, "_commit_lock_and_caches", boom)
    else:
        def boom(*_args, **_kwargs):
            raise ValueError("simulated read failure")
        monkeypatch.setattr(upgrade, "_legacy_layout_paths", boom)
    before_lock = (tmp_path / LOCK).read_bytes()
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 2
    err = capsys.readouterr().err
    assert "refused (containment)" in err
    assert "Traceback" not in err
    assert (tmp_path / LOCK).read_bytes() == before_lock


def test_no_record_is_a_no_op(tmp_path, capsys):
    _install(tmp_path)
    lock = _lock(tmp_path)
    lock["files"] = [row for row in lock["files"] if row["src"] != SRC]
    _write_lock(tmp_path, lock)
    before = _tree(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED) == 0
    assert "Nothing to record: the lockfile has no record of the documentation plan." \
        in capsys.readouterr().out
    assert _tree(tmp_path) == before


def test_to_is_refused(tmp_path, capsys):
    _install(tmp_path)
    _moved_project(tmp_path)
    before = _tree(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, MOVED, "--to", "HEAD") == 2
    assert ("error: --documentation-plan-moved runs against the running target tree; "
            "--to is not supported") in capsys.readouterr().err
    assert _tree(tmp_path) == before


def test_the_report_line_is_printed_before_the_move_and_gone_after(tmp_path, capsys):
    _install(tmp_path)
    _as_0_8(tmp_path)
    capsys.readouterr()

    assert _upgrade(tmp_path, "--plan") == 0
    plan_before = _report_lines(capsys.readouterr().out)
    for step in STEPS:
        assert step in plan_before
    assert LINKS in plan_before

    assert _upgrade(tmp_path, "--stage") == 0
    capsys.readouterr()
    assert _upgrade(tmp_path, "--apply") == 0
    apply_out = _report_lines(capsys.readouterr().out)
    for step in STEPS:
        assert step in apply_out
    assert LINKS in apply_out

    _owner_moves(tmp_path)
    assert _upgrade(tmp_path, MOVED) == 0
    capsys.readouterr()
    assert _upgrade(tmp_path, "--plan") == 0
    plan_after = _report_lines(capsys.readouterr().out)
    assert not any(step in plan_after for step in STEPS)
    assert LINKS not in plan_after


def test_the_report_helper_never_raises(tmp_path):
    _install(tmp_path)
    _as_0_8(tmp_path)
    lock = _lock(tmp_path)
    rec = _doc_record(lock)
    assert upgrade._documentation_plan_move_lines(tmp_path)  # the lines do print here

    lock["files"] = "not a list"
    _write_lock(tmp_path, lock)
    assert upgrade._documentation_plan_move_lines(tmp_path) == []

    lock["files"] = [1, "two", rec]
    _write_lock(tmp_path, lock)
    assert upgrade._documentation_plan_move_lines(tmp_path)  # skips the non-objects

    (tmp_path / LOCK).write_text("{ not json", encoding="utf-8")
    assert upgrade._documentation_plan_move_lines(tmp_path) == []


def test_the_steps_read_the_same_everywhere(tmp_path):
    """The report, the refusal and install/UPGRADE.md give the same five steps.
    The UPGRADE.md check is expected to fail until its step is written (chunk C4)."""
    _install(tmp_path)
    _as_0_8(tmp_path)
    assert list(upgrade._DOCPLAN_STEPS) == STEPS
    report = upgrade._documentation_plan_move_lines(tmp_path)
    assert report[1:6] == STEPS
    upgrade_md = (CAIRN_ROOT / "install" / "UPGRADE.md").read_text(encoding="utf-8")
    for step in STEPS:
        assert step.strip() in upgrade_md


@pytest.mark.parametrize("order", ["upgrade-first", "record-first"])
def test_an_ordinary_upgrade_and_the_record_agree_in_either_order(tmp_path, capsys, order):
    if shutil.which("git") is None:
        pytest.skip("git is not available")
    _install(tmp_path)
    _as_0_8(tmp_path)
    _git(tmp_path, "init", "-q")
    # The project file and its ancestor lack the template's last line, so an
    # ordinary upgrade has one line to add: the cut line, which the template has.
    cut = _cut_last_line(tmp_path)
    _commit_all(tmp_path)
    capsys.readouterr()

    if order == "upgrade-first":
        assert _upgrade(tmp_path, "--stage") == 0
        assert _upgrade(tmp_path, "--apply") == 0
        capsys.readouterr()
        assert cut in (tmp_path / OLD).read_bytes()
        assert not (tmp_path / NEW).exists()
        _commit_all(tmp_path)
        _owner_moves(tmp_path)
        assert _upgrade(tmp_path, MOVED) == 0
        assert "Recorded dev/DOCUMENTATION_PLAN.md" in capsys.readouterr().out
    else:
        _owner_moves(tmp_path)
        assert _upgrade(tmp_path, MOVED) == 0
        assert "Recorded dev/DOCUMENTATION_PLAN.md" in capsys.readouterr().out
        _commit_all(tmp_path)
        assert _upgrade(tmp_path, "--stage") == 0
        assert _upgrade(tmp_path, "--apply") == 0
        capsys.readouterr()
        assert cut in (tmp_path / NEW).read_bytes()
        assert not (tmp_path / OLD).exists()
    assert _doc_record(_lock(tmp_path))["dst"] == NEW
    assert _verify(tmp_path) == 0


def test_verification_still_judges_the_record_after_the_move(tmp_path, capsys):
    if shutil.which("git") is None:
        pytest.skip("git is not available")
    _install(tmp_path)
    _moved_project(tmp_path)
    assert _upgrade(tmp_path, MOVED) == 0
    capsys.readouterr()
    # The content-security leg needs tracked text, so the project is a Git repo.
    _git(tmp_path, "init", "-q")
    _commit_all(tmp_path)
    assert _verify(tmp_path) == 0

    installed = [row["dst"] for row in _lock(tmp_path)["files"]
                 if row["src"].endswith("run_security_verification.py")]
    assert installed, "the default-on security verification module is not installed"
    result = subprocess.run([sys.executable, str(tmp_path / installed[0]), "local"],
                            cwd=str(tmp_path), capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
