"""`upgrade --finalize <path>` on a retired file whose record says "living state".

An install from v0.3.0 records the fold-back ledger (`dev/.cairn/cairn_foldback.md`)
with `living_state: true`. `verify_integrity` honours that flag only for the paths
it lists, and the ledger is no longer one of them, so it fails the whole tree as a
tamper attempt. `bootstrap/UPGRADE.md` tells a project that keeps an edited retired
file to run `upgrade --finalize <path>`, and says a kept file is not an error. The
finalize has to leave the file checked like any other kept file, or the guide's
route ends in a failed integrity check.

The tests drive the real `scaffold.py` entry point and the real integrity check
over a real install; a project from v0.3.0 is modelled by adding the former record
to a fresh scratch install.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap._scaffold import config as C  # noqa: E402
from bootstrap.verify_integrity import verify  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
LOCK_REL = "dev/.cairn/cairn-lock.yml"
LEDGER = "dev/.cairn/cairn_foldback.md"
ROWS = {row[1]: row for row in C._RETIRED_INSTALLS}
SHIPPED_LEDGER = b"# Fold-back ledger\n"
EDITED_LEDGER = SHIPPED_LEDGER + b"\n## Candidate\n\nAn entry the project wrote.\n"
PROFILE = (
    "project_name: FinalizeLivingStateTest\n"
    "test_command: pytest\n"
    "python_package: finalize_living_state_test\n"
    "preset: solo-greenfield\n"
)

assert LEDGER in ROWS, "the ledger is no longer on the retired list; update this file"
assert LEDGER not in s._LIVING_STATE_DSTS, "the ledger is living state again; the defect is gone"


def _sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _git(project: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(project), "-c", "user.name=t", "-c", "user.email=t@t",
         "-c", "commit.gpgsign=false", *args],
        capture_output=True, text=True, check=True)


def _commit_all(project: Path) -> None:
    _git(project, "add", "-A")
    _git(project, "commit", "-q", "--allow-empty", "-m", "state")


def _lock(project: Path) -> dict:
    lock = s.read_lockfile(project)
    assert lock is not None
    return lock


def _record(project: Path, dst: str) -> dict:
    return next(r for r in _lock(project)["files"] if r["dst"] == dst)


def _edit_records(project: Path, edit) -> None:
    lock = _lock(project)
    edit(lock["files"])
    (project / LOCK_REL).write_text(s._emit_lock_yaml(lock), encoding="utf-8")


@pytest.fixture(scope="module")
def pristine_install(tmp_path_factory: pytest.TempPathFactory) -> Path:
    base = tmp_path_factory.mktemp("pristine")
    target = base / "project"
    target.mkdir()
    profile = base / "profile.yml"
    profile.write_text(PROFILE, encoding="utf-8")
    assert s.main(["--config", str(profile), "--target", str(target),
                   "--cairn-root", str(ROOT), "--allow-dev"]) == 0
    _git(target, "init", "-q", "-b", "main")
    _commit_all(target)
    return target


@pytest.fixture
def project(pristine_install: Path, tmp_path: Path) -> Path:
    """A project from v0.3.0: its lockfile records an edited fold-back ledger."""
    copy = tmp_path / "project"
    shutil.copytree(pristine_install, copy, symlinks=True)
    (copy / LEDGER).write_bytes(EDITED_LEDGER)
    _edit_records(copy, lambda files: files.append({
        "dst": LEDGER, "src": ROWS[LEDGER][0], "verbatim": False,
        "hash": _sha(SHIPPED_LEDGER), "base_hash": _sha(SHIPPED_LEDGER),
        "living_state": True}))
    _commit_all(copy)
    return copy


def _finalize(capsys: pytest.CaptureFixture[str], project: Path, *paths: str) -> int:
    code = s.main(["upgrade", "--target", str(project), "--finalize", *paths,
                   "--cairn-root", str(ROOT)])
    capsys.readouterr()
    return code


def _integrity(capsys: pytest.CaptureFixture[str], project: Path) -> tuple[int, str]:
    code = verify(project)
    captured = capsys.readouterr()
    return code, captured.out + captured.err


def test_the_scratch_project_fails_the_integrity_check_before_any_finalize(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    code, text = _integrity(capsys, project)
    assert code == 1
    assert f"illegal living_state opt-out: {LEDGER}" in text


def test_finalizing_an_edited_retired_ledger_by_name_leaves_a_tree_the_check_accepts(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    assert _finalize(capsys, project, LEDGER) == 0
    record = _record(project, LEDGER)
    assert "living_state" not in record
    assert record["hash"] == _sha(EDITED_LEDGER)
    code, text = _integrity(capsys, project)
    assert code == 0, text
    assert "illegal living_state" not in text


def test_a_finalized_ledger_is_checked_like_any_kept_file(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    assert _finalize(capsys, project, LEDGER) == 0
    (project / LEDGER).write_bytes(EDITED_LEDGER + b"one more line\n")
    code, text = _integrity(capsys, project)
    assert code == 1
    assert f"modified (hash mismatch): {LEDGER}" in text


def test_a_bare_finalize_leaves_an_edited_retired_ledger_and_its_flag_alone(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    before = _record(project, LEDGER)
    assert _finalize(capsys, project) == 0
    assert _record(project, LEDGER) == before
    assert before["living_state"] is True


def test_the_flag_stays_on_a_path_the_integrity_check_still_lists(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    allowed = "dev/PLANNING.md"
    assert allowed in s._LIVING_STATE_DSTS
    assert _finalize(capsys, project, allowed) == 0
    assert _record(project, allowed)["living_state"] is True


def test_a_stray_flag_on_a_file_that_is_not_retired_stays_and_still_fails_the_check(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    plain = "dev/README.md"
    assert plain not in ROWS and plain not in s._LIVING_STATE_DSTS

    def flag(files: list) -> None:
        for record in files:
            if record["dst"] == plain:
                record["living_state"] = True

    _edit_records(project, flag)
    assert _finalize(capsys, project, plain) == 0
    assert _record(project, plain)["living_state"] is True
    code, text = _integrity(capsys, project)
    assert code == 1
    assert f"illegal living_state opt-out: {plain}" in text
