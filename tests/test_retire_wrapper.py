"""`upgrade --retire-wrapper NAME` and its side in `verify_integrity` (defect arc
B, chunk C5).

A vendor wrapper such as `CLAUDE.md` is a file the adopter may delete on purpose.
Retiring it records that choice on the wrapper's lockfile record
(`adopter_deleted`), so Cairn treats the absence as intended. One rule decides
whether a record is a retired wrapper (`_wrapper_retired` in
`install/_scaffold/upgrade.py`, repeated inline in `install/verify_integrity.py`).

Promises:
- After `--retire-wrapper`, `--plan`, `--finalize` and `verify_integrity` pass,
  and the OK line says a wrapper record was retired.
- Before retiring, a deleted wrapper is a failure that names the command.
- A retired record whose file is restored is checked again; a modified restored
  wrapper fails.
- `--retire-wrapper` refuses a name that is not a wrapper, a wrapper file that is
  present, and a lockfile with no wrapper record. It changes nothing then.
- A lockfile edit cannot hide a deleted file: a shipped script, `AGENTS.md`, or
  two `core/VENDOR.md` records still fail the check and are not planned as
  `up-to-date`.

Run from the Cairn repo root:
    python -m pytest tests/test_retire_wrapper.py
"""
from __future__ import annotations

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
WRAPPER = "VENDOR.md"
SRC_WRAPPER = "core/VENDOR.md"
RETIRED_NOTE = "(1 vendor wrapper record retired by the adopter)"
DELETED_ON_PURPOSE = "vendor wrapper deleted on purpose"


def _install(target: Path) -> None:
    cfg = target / "profile.yml"
    cfg.write_text("project_name: Retire\ntest_command: pytest\nmodules: []\n",
                   encoding="utf-8")
    assert scaffold.main(["--config", str(cfg), "--target", str(target),
                          "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]) == 0


def _upgrade(target: Path, *args: str) -> int:
    return scaffold.main(["upgrade", "--target", str(target),
                          "--cairn-root", str(CAIRN_ROOT), *args])


def _verify(target: Path) -> int:
    return verify_integrity.main(["--target", str(target)])


def _lock(target: Path) -> dict:
    return scaffold.read_lockfile(target)


def _write_lock(target: Path, lock: dict) -> None:
    (target / LOCK).write_text(scaffold._emit_lock_yaml(lock), encoding="utf-8")


def _wrapper_record(lock: dict) -> dict:
    (rec,) = [row for row in lock["files"] if row["src"] == SRC_WRAPPER]
    return rec


def _script_record(lock: dict) -> dict:
    return next(row for row in lock["files"]
                if row["dst"].startswith("dev/tools/") and row["dst"].endswith(".py"))


def _plans(target: Path) -> list:
    """The engine's own plan rows for the tree (what ``--plan`` prints from)."""
    plans, _ = upgrade._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, _lock(target), None)
    return plans


def test_retired_wrapper_passes_plan_finalize_and_verify(tmp_path, capsys):
    _install(tmp_path)
    (tmp_path / WRAPPER).unlink()
    capsys.readouterr()

    assert _verify(tmp_path) == 1
    assert ("missing: VENDOR.md (deleted on purpose? "
            "upgrade --retire-wrapper VENDOR.md)") in capsys.readouterr().err

    assert _upgrade(tmp_path, "--retire-wrapper", WRAPPER) == 0
    assert _wrapper_record(_lock(tmp_path))["adopter_deleted"] is True
    capsys.readouterr()

    assert _upgrade(tmp_path) == 0
    capsys.readouterr()
    assert [p.kind for p in _plans(tmp_path) if p.dst == WRAPPER] == ["up-to-date"]
    assert _upgrade(tmp_path, "--finalize") == 0
    capsys.readouterr()

    assert _verify(tmp_path) == 0
    assert RETIRED_NOTE in capsys.readouterr().out


def test_review_only_text_for_a_missing_wrapper_names_the_command(tmp_path, capsys):
    _install(tmp_path)
    (tmp_path / WRAPPER).unlink()
    capsys.readouterr()

    assert _upgrade(tmp_path) == 0
    assert "upgrade --retire-wrapper VENDOR.md" in capsys.readouterr().out


def test_a_retired_wrapper_restored_is_checked_again(tmp_path):
    _install(tmp_path)
    original = (tmp_path / WRAPPER).read_bytes()
    (tmp_path / WRAPPER).unlink()
    assert _upgrade(tmp_path, "--retire-wrapper", WRAPPER) == 0

    (tmp_path / WRAPPER).write_bytes(original + b"\nedited\n")
    assert _verify(tmp_path) == 1

    (tmp_path / WRAPPER).write_bytes(original)
    assert _verify(tmp_path) == 0


def test_retire_refuses_a_name_that_is_not_a_wrapper(tmp_path):
    _install(tmp_path)
    (tmp_path / WRAPPER).unlink()
    before = (tmp_path / LOCK).read_bytes()

    assert _upgrade(tmp_path, "--retire-wrapper", "AGENTS.md") == 2
    assert (tmp_path / LOCK).read_bytes() == before


def test_retire_refuses_a_wrapper_file_that_is_present(tmp_path):
    _install(tmp_path)
    before = (tmp_path / LOCK).read_bytes()

    assert _upgrade(tmp_path, "--retire-wrapper", WRAPPER) == 1
    assert (tmp_path / LOCK).read_bytes() == before


def test_retire_refuses_a_known_wrapper_name_that_is_present(tmp_path):
    _install(tmp_path)
    (tmp_path / WRAPPER).unlink()
    (tmp_path / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    before = (tmp_path / LOCK).read_bytes()

    assert _upgrade(tmp_path, "--retire-wrapper", "CLAUDE.md") == 1
    assert (tmp_path / LOCK).read_bytes() == before


def test_retire_refuses_a_lockfile_with_no_wrapper_record(tmp_path):
    _install(tmp_path)
    lock = _lock(tmp_path)
    lock["files"] = [row for row in lock["files"] if row["src"] != SRC_WRAPPER]
    _write_lock(tmp_path, lock)
    before = (tmp_path / LOCK).read_bytes()

    assert _upgrade(tmp_path, "--retire-wrapper", WRAPPER) == 1
    assert (tmp_path / LOCK).read_bytes() == before


def test_tampered_record_on_a_shipped_script_still_fails(tmp_path, capsys):
    _install(tmp_path)
    lock = _lock(tmp_path)
    lock["files"] = [row for row in lock["files"] if row["src"] != SRC_WRAPPER]
    script = _script_record(lock)
    script.update(src=SRC_WRAPPER, adopter_deleted=True)
    script.pop("verbatim", None)
    _write_lock(tmp_path, lock)
    (tmp_path / script["dst"]).unlink()
    capsys.readouterr()

    assert _verify(tmp_path) == 1
    assert f"missing: {script['dst']}" in capsys.readouterr().err
    assert all(p.detail != DELETED_ON_PURPOSE for p in _plans(tmp_path))


def test_tampered_record_on_agents_md_still_fails(tmp_path, capsys):
    _install(tmp_path)
    lock = _lock(tmp_path)
    lock["files"] = [row for row in lock["files"] if row["src"] != SRC_WRAPPER]
    agents = next(row for row in lock["files"] if row["dst"] == "AGENTS.md")
    agents.update(src=SRC_WRAPPER, adopter_deleted=True)
    agents.pop("verbatim", None)
    _write_lock(tmp_path, lock)
    (tmp_path / "AGENTS.md").unlink()
    capsys.readouterr()

    assert _verify(tmp_path) == 1
    assert "missing: AGENTS.md" in capsys.readouterr().err
    assert all(p.detail != DELETED_ON_PURPOSE for p in _plans(tmp_path))


def test_two_wrapper_records_do_not_hide_a_deleted_file(tmp_path, capsys):
    _install(tmp_path)
    lock = _lock(tmp_path)
    wrapper = _wrapper_record(lock)
    wrapper["adopter_deleted"] = True
    script = _script_record(lock)
    script.update(src=SRC_WRAPPER, adopter_deleted=True)
    script.pop("verbatim", None)
    _write_lock(tmp_path, lock)
    (tmp_path / WRAPPER).unlink()
    (tmp_path / script["dst"]).unlink()
    capsys.readouterr()

    assert _verify(tmp_path) == 1
    err = capsys.readouterr().err
    assert "missing: VENDOR.md" in err
    assert f"missing: {script['dst']}" in err
    assert all(p.detail != DELETED_ON_PURPOSE for p in _plans(tmp_path))
