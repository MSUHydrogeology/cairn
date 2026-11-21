"""External layout-upgrade promises through the scaffold command."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from install import scaffold
from install._scaffold import layout_migration as migration
from install._scaffold import upgrade


LOCK = "dev/.cairn/cairn-lock.yml"
RECEIPT = "dev/.cairn-upgrade/layout/receipt.json"
OLD = ("tools/board.py", "tools/pulse.py")
NEW = ("dev/tools/board.py", "dev/tools/pulse.py")
ORIGINAL = (b"# original board\n", b"# original pulse\n")
LATEST = (b"# latest board\n", b"# latest pulse\n")
FORK = b"# user's pulse\n"


def _put(root: Path, name: str, raw: bytes) -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return path


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "-c", "core.fsmonitor=false", "-c", "core.autocrlf=false",
         "-c", "user.name=Layout test", "-c", "user.email=layout@example.invalid",
         "-c", "commit.gpgsign=false", *args],
        stderr=subprocess.PIPE, timeout=20,
    ).decode("utf-8").strip()


def _commit(root: Path, message: str) -> str:
    _git(root, "add", "--all")
    _git(root, "commit", "-m", message)
    return _git(root, "rev-parse", "HEAD")


def _digest(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


@pytest.fixture
def layout(tmp_path):
    source = tmp_path / "source"
    target = tmp_path / "target"
    for root in (source, target):
        root.mkdir()
        _git(root, "init", "-q")
    names = tuple(f"skills/_lib/{Path(path).name}" for path in OLD)
    for paths, contents in ((OLD, ORIGINAL), (NEW, LATEST)):
        rows = tuple(zip(names, paths, (True, True)))
        _put(source, "bootstrap/_scaffold/config.py", (
            "_CORE_MAPPINGS: tuple = ()\n_MODULE_MAPPINGS: dict = {}\n"
            f"_SKILLS_MAPPINGS: tuple = {rows!r}\n"
        ).encode("utf-8"))
        for name, raw in zip(names, contents):
            _put(source, f"templates/{name}", raw)
        if paths == OLD:
            _put(source, "docs/dev-tour.md", b"Old tour\n")
        else:
            _put(source, "templates/onboarding/dev-tour.md", b"New tour\n")
        revision = _commit(source, str(paths))
        if paths == OLD:
            old_rev = revision
    lock = {"schema": 1, "cairn_commit": old_rev, "modules": [],
            "profile": {"preset": "solo-greenfield"}, "files": []}
    for name, path, base, installed in zip(names, OLD, ORIGINAL, (ORIGINAL[0], FORK)):
        _put(target, path, installed)
        lock["files"].append({"src": name, "dst": path, "verbatim": True,
                              "base_hash": _digest(base), "hash": _digest(installed)})
    _put(target, "tools/project.py", b"# unrelated project tool\n")
    _put(target, "CLAUDE.md", b"@AGENTS.md\nProject wrapper\n")
    lock["files"].append({"src": "core/VENDOR.md", "dst": "VENDOR.md", "verbatim": False})
    _put(target, "dev/modules/onboarding/agent-team-onboarding.md", b"Project onboarding\n")
    _put(target, LOCK, json.dumps(lock).encode("utf-8"))
    _commit(target, "pre-layout project")
    return source, target, old_rev


def _upgrade(layout, *args: str) -> int:
    source, target, _ = layout
    return scaffold.main(["upgrade", "--cairn-root", str(source), "--target", str(target), *args])


def _receipt(capsys) -> str:
    captured = capsys.readouterr()
    match = re.search(r"--migration-receipt ([0-9a-f]{64})", captured.out)
    assert match is not None, captured
    return match.group(1)


def test_layout_migration_resumes_on_either_side_of_lock(layout, capsys, monkeypatch):
    _, target, _ = layout
    old_lock = (target / LOCK).read_bytes()
    assert _upgrade(layout, "--plan", "--to", "HEAD") == 0
    assert not (target / RECEIPT).exists()
    assert _upgrade(layout, "--stage", "--to", "HEAD") == 0
    digest = _receipt(capsys)
    receipt = target / RECEIPT
    original_receipt = receipt.read_bytes()
    resume = ("--apply", "--migration-receipt", digest, "--to", "HEAD")

    receipt.write_bytes(original_receipt + b" ")
    assert _upgrade(layout, *resume) == 2
    receipt.write_bytes(original_receipt)
    assert (target / LOCK).read_bytes() == old_lock
    assert not (target / NEW[0]).exists()

    def stop(*_, **__):
        raise OSError("simulated interruption")

    with monkeypatch.context() as patch:
        patch.setattr(migration, "_replace", stop)
        assert _upgrade(layout, *resume) == 2
    assert (target / LOCK).read_bytes() == old_lock
    assert (target / NEW[0]).read_bytes() == LATEST[0]
    assert (target / OLD[0]).read_bytes() == ORIGINAL[0]
    assert _upgrade(layout, "--stage") == 0
    assert _upgrade(layout, "--finalize") == 2
    assert receipt.read_bytes() == original_receipt

    (target / OLD[0]).write_bytes(b"changed after stage\n")
    assert _upgrade(layout, *resume) == 2
    assert (target / OLD[0]).read_bytes() == b"changed after stage\n"
    (target / OLD[0]).write_bytes(ORIGINAL[0])

    retire = migration._remove_unchanged_file

    def stop_second(path, *args, **kwargs):
        if path.name == "pulse.py":
            stop()
        return retire(path, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(migration, "_remove_unchanged_file", stop_second)
        assert _upgrade(layout, *resume) == 2
    assert (target / LOCK).read_bytes() != old_lock
    assert not (target / OLD[0]).exists()
    assert (target / OLD[1]).read_bytes() == FORK

    (target / NEW[1]).write_bytes(b"changed output after the lock\n")
    assert _upgrade(layout, *resume) == 2
    assert (target / OLD[1]).read_bytes() == FORK
    (target / NEW[1]).write_bytes(FORK)
    assert _upgrade(layout, *resume) == 0
    assert not receipt.exists()
    assert not any((target / path).exists() for path in OLD)
    assert (target / NEW[1]).read_bytes() == FORK
    assert (target / "tools/project.py").read_bytes() == b"# unrelated project tool\n"
    assert (target / "CLAUDE.md").read_bytes() == b"@AGENTS.md\nProject wrapper\n"
    assert not (target / "VENDOR.md").exists()
    assert (target / "dev/modules/onboarding/dev-tour.md").read_bytes() == b"New tour\n"
    assert (target / "dev/modules/onboarding/agent-team-onboarding.md").read_bytes() == b"Project onboarding\n"
    records = {row["dst"]: row for row in scaffold.read_lockfile(target)["files"]}
    assert records[NEW[1]]["hash"] == _digest(FORK)
    assert records[NEW[1]]["base_hash"] == _digest(LATEST[1])
    for key in ("layout_ancestry", "layout_base_commit", "layout_fork"):
        assert key not in records[NEW[1]]
    assert records["CLAUDE.md"]["hash"] == _digest(b"@AGENTS.md\nProject wrapper\n")


@pytest.mark.parametrize("problem", ("occupied", "linked", "directory", "unknown"))
def test_layout_migration_refuses_or_reconciles(layout, capsys, problem):
    _, target, old_rev = layout
    destination = target / NEW[0]
    destination.parent.mkdir(parents=True)
    if problem == "occupied":
        destination.write_bytes(b"my board\n")
    elif problem == "linked":
        try:
            destination.symlink_to(target / "tools/project.py")
        except OSError as exc:
            pytest.skip(f"links unavailable: {exc}")
    elif problem == "directory":
        destination.mkdir()
    else:
        lock = scaffold.read_lockfile(target)
        lock["cairn_commit"] = "unknown"
        _put(target, LOCK, json.dumps(lock).encode("utf-8"))
        _commit(target, "legacy lock with unknown provenance")
    before = (target / LOCK).read_bytes()
    assert _upgrade(layout, "--stage", "--to", "HEAD") == 2
    assert not (target / RECEIPT).exists()
    assert (target / LOCK).read_bytes() == before
    assert (target / OLD[0]).read_bytes() == ORIGINAL[0]
    if problem != "unknown":
        return

    assert _upgrade(layout, "--stage", "--reconcile-layout", old_rev) == 0
    digest = _receipt(capsys)
    assert _upgrade(layout, "--apply", "--migration-receipt", digest) == 0
    records = {row["dst"]: row for row in scaffold.read_lockfile(target)["files"]}
    assert records[OLD[1]]["layout_ancestry"] == "unknown"
    assert records[OLD[1]]["layout_fork"] is True
    assert (target / OLD[1]).read_bytes() == FORK
    assert not destination.exists()
    assert _upgrade(layout, "--stage", "--to", "HEAD") == 0


def test_packaged_source_only_needs_history_for_legacy_paths(layout, capsys):
    source, target, _ = layout
    shutil.rmtree(source / ".git")
    assert _upgrade(layout, "--plan") == 2
    error = capsys.readouterr().err
    assert "Git checkout" in error and OLD[0] in error

    lock = scaffold.read_lockfile(target)
    for record in lock["files"]:
        if record["dst"] in OLD:
            old = record["dst"]
            record["dst"] = NEW[OLD.index(old)]
            destination = target / record["dst"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            (target / old).rename(destination)
    _put(target, LOCK, json.dumps(lock).encode("utf-8"))
    assert _upgrade(layout, "--plan") == 0
    assert not (target / RECEIPT).exists()


GIT_READ_CRLF = (
    "Cairn's copy of templates/skills/_lib/git_read.py has Windows line endings, "
    "so the installer cannot trust it. Git did this when it cloned Cairn with "
    "core.autocrlf=true. In the Cairn checkout run `git config core.autocrlf "
    "false`, delete that file, and run `git checkout -- "
    "templates/skills/_lib/git_read.py`. Then run this command again. A new clone "
    "made with `git clone -c core.autocrlf=false` also works."
)
GIT_READ_OTHER = (
    "Cairn's copy of templates/skills/_lib/git_read.py does not match the copy "
    "this installer is pinned to (it was edited, is a link, or is another "
    "version). Restore it from the Cairn release you are installing from, then "
    "run this command again."
)


@pytest.mark.parametrize("edited", (False, True), ids=("crlf-copy", "edited-copy"))
def test_unbound_git_reader_names_its_cause(layout, capsys, monkeypatch, tmp_path, edited):
    helper = Path(__file__).resolve().parents[1] / "templates/skills/_lib/git_read.py"
    raw = helper.read_bytes().replace(b"\n", b"\r\n")
    if edited:
        raw += b"# edited\r\n"
    copy = tmp_path / "git_read.py"
    copy.write_bytes(raw)

    def unbound():
        raise RuntimeError("Git read helper binding failed")

    monkeypatch.setattr(upgrade, "_git_read_helper", unbound)
    monkeypatch.setattr(upgrade, "_git_read_helper_path", lambda: str(copy))
    assert _upgrade(layout, "--plan") == 2
    error = capsys.readouterr().err
    assert (GIT_READ_OTHER if edited else GIT_READ_CRLF) in error


def test_exact_copy_is_not_called_line_endings(layout, capsys, monkeypatch, tmp_path):
    helper = Path(__file__).resolve().parents[1] / "templates/skills/_lib/git_read.py"
    copy = tmp_path / "git_read.py"
    copy.write_bytes(helper.read_bytes())

    def unbound():
        raise RuntimeError("Git read helper binding failed")

    monkeypatch.setattr(upgrade, "_git_read_helper", unbound)
    monkeypatch.setattr(upgrade, "_git_read_helper_path", lambda: str(copy))
    assert _upgrade(layout, "--plan") == 2
    error = capsys.readouterr().err
    assert GIT_READ_CRLF not in error
    assert GIT_READ_OTHER in error


@pytest.mark.parametrize("case", ("oversize", "missing", "linked"))
def test_a_helper_that_cannot_be_read_safely_is_not_called_line_endings(
        layout, capsys, monkeypatch, tmp_path, case):
    helper = Path(__file__).resolve().parents[1] / "templates/skills/_lib/git_read.py"
    crlf = helper.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    copy = tmp_path / "git_read.py"
    if case == "oversize":
        copy.write_bytes(crlf + b"#" * (upgrade._GIT_READ_MAX_BYTES + 1))
    elif case == "linked":
        real = tmp_path / "real.py"
        real.write_bytes(crlf)
        try:
            copy.symlink_to(real)
        except OSError:
            pytest.skip("links cannot be made on this host")

    def unbound():
        raise RuntimeError("Git read helper binding failed")

    monkeypatch.setattr(upgrade, "_git_read_helper", unbound)
    monkeypatch.setattr(upgrade, "_git_read_helper_path", lambda: str(copy))
    assert _upgrade(layout, "--plan") == 2
    error = capsys.readouterr().err
    assert GIT_READ_CRLF not in error
    assert GIT_READ_OTHER in error


def test_unbound_git_reader_names_its_cause_for_a_to_upgrade(layout, capsys, monkeypatch, tmp_path):
    helper = Path(__file__).resolve().parents[1] / "templates/skills/_lib/git_read.py"
    copy = tmp_path / "git_read.py"
    copy.write_bytes(helper.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))

    def unbound():
        raise RuntimeError("Git read helper binding failed")

    monkeypatch.setattr(upgrade, "_git_read_helper", unbound)
    monkeypatch.setattr(upgrade, "_git_read_helper_path", lambda: str(copy))
    code = _upgrade(layout, "--plan", "--to", "HEAD")
    error = capsys.readouterr().err
    assert GIT_READ_CRLF in error
    assert code == 1, (code, error)


def test_the_refusal_looks_at_the_pinned_helper_itself():
    raw = Path(upgrade._git_read_helper_path()).read_bytes()
    folded = raw.replace(b"\r\n", b"\n")
    assert hashlib.sha256(folded).hexdigest() == upgrade._GIT_READ_SHA256


def _keyed_moved_record(old_rev: str) -> dict:
    return {"src": "skills/_lib/board.py", "dst": NEW[0], "verbatim": True,
            "base_hash": _digest(LATEST[0]), "hash": _digest(LATEST[0]),
            "layout_ancestry": "verified", "layout_base_commit": old_rev,
            "layout_fork": False}


def test_heal_layout_removes_keys_from_moved_records_only(layout, capsys):
    _, target, old_rev = layout
    _put(target, NEW[0], LATEST[0])
    lock = scaffold.read_lockfile(target)
    lock["files"].append(_keyed_moved_record(old_rev))
    for row in lock["files"]:
        if row["dst"] == OLD[0]:
            row.update(layout_ancestry="verified", layout_base_commit=old_rev, layout_fork=False)
    _put(target, LOCK, json.dumps(lock).encode("utf-8"))
    _commit(target, "lock with layout keys on a moved record and an old path")
    expected = scaffold.read_lockfile(target)
    for row in expected["files"]:
        if row["dst"] == NEW[0]:
            for key in ("layout_ancestry", "layout_base_commit", "layout_fork"):
                row.pop(key)

    assert _upgrade(layout, "--heal-layout") == 0
    assert "Removed layout keys from 1 lock record(s). Commit dev/.cairn/cairn-lock.yml." \
        in capsys.readouterr().out
    assert scaffold.read_lockfile(target) == expected
    records = {row["dst"]: row for row in scaffold.read_lockfile(target)["files"]}
    assert records[OLD[0]]["layout_base_commit"] == old_rev

    assert _upgrade(layout, "--heal-layout") == 0
    assert "Nothing to heal." in capsys.readouterr().out


def test_heal_layout_refuses_a_dirty_lock(layout, capsys):
    _, target, old_rev = layout
    _put(target, NEW[0], LATEST[0])
    lock = scaffold.read_lockfile(target)
    lock["files"].append(_keyed_moved_record(old_rev))
    _put(target, LOCK, json.dumps(lock).encode("utf-8"))
    before = (target / LOCK).read_bytes()

    assert _upgrade(layout, "--heal-layout") == 1
    assert (target / LOCK).read_bytes() == before
    assert "unsaved edits" in capsys.readouterr().err


SHALLOW_TEXT = ("unproved ancestry; the Cairn checkout is shallow, so the release "
                "this copy came from is not in it")
SHALLOW_FETCH = ("Fetch the full history in the Cairn checkout (git fetch --unshallow "
                 "--tags), then run this again.")


def test_shallow_cairn_checkout_says_to_fetch_the_history(layout, capsys, tmp_path):
    source, target, _ = layout
    shallow = tmp_path / "shallow"
    _git(tmp_path, "clone", "--depth", "1", "file://" + source.as_posix(), str(shallow))

    assert scaffold.main(["upgrade", "--cairn-root", str(shallow), "--target", str(target),
                          "--plan", "--to", "HEAD"]) == 2
    error = capsys.readouterr().err
    assert f"{OLD[0]}: {SHALLOW_TEXT}" in error
    assert error.count(SHALLOW_FETCH) == 1


def test_stale_hash_with_crlf_base_is_planned_as_a_copy(layout, capsys):
    _, target, _ = layout
    lock = scaffold.read_lockfile(target)
    record = next(row for row in lock["files"] if row["dst"] == OLD[0])
    crlf = ORIGINAL[0].replace(b"\n", b"\r\n")
    record["hash"] = record["base_hash"] = _digest(crlf)
    _put(target, LOCK, json.dumps(lock).encode("utf-8"))
    _commit(target, "lock whose base hash is the CRLF form of the original")

    assert _upgrade(layout, "--plan", "--to", "HEAD") == 0
    assert "  copy: " + OLD[0] + " -> " + NEW[0] in capsys.readouterr().out


CHECK_DST = "dev/modules/claim-check.md"
CHECK_BASE = "dev/.cairn/base/" + CHECK_DST
CHECK_TEMPLATE = b"Run `{{claim_check_command}}` on a document.\n"
CHECK_OLD = b"Run `python scripts/claim_check.py` on a document.\n"
CHECK_NEW = b"Run `python dev/tools/claim_check.py` on a document.\n"
CHECK_EDITED = b"Run `python scripts/claim_check.py` on a document. Mine.\n"


def _claim_check_tree(layout, *, edited: bytes = CHECK_OLD, token: str = "python scripts/claim_check.py"):
    """A lock whose claim_check_command still names the pre-0.8 script, with the
    moved script's record and the rendered module doc as an adopter has it."""
    _, target, _ = layout
    _put(target, CHECK_BASE, CHECK_TEMPLATE)
    _put(target, CHECK_DST, edited)
    _put(target, "dev/tools/claim_check.py", b"# claim check\n")
    lock = scaffold.read_lockfile(target)
    lock["tokens"] = {"claim_check_command": token}
    lock["files"].append({"src": "modules/default-on/claim-check.md", "dst": CHECK_DST,
                          "verbatim": False, "base_cache": CHECK_BASE,
                          "base_hash": _digest(CHECK_TEMPLATE), "hash": _digest(edited)})
    lock["files"].append({"src": "modules/default-on/claim_check.py",
                          "dst": "dev/tools/claim_check.py", "verbatim": True,
                          "base_hash": _digest(b"# claim check\n"),
                          "hash": _digest(b"# claim check\n")})
    _put(target, LOCK, json.dumps(lock).encode("utf-8"))
    _commit(target, "pre-0.8 claim-check setting")


def test_heal_layout_corrects_the_token_and_an_unedited_file(layout, capsys):
    _, target, _ = layout
    _claim_check_tree(layout)

    assert _upgrade(layout, "--heal-layout") == 0
    lock = scaffold.read_lockfile(target)
    assert lock["tokens"]["claim_check_command"] == "python dev/tools/claim_check.py"
    assert (target / CHECK_DST).read_bytes() == CHECK_NEW
    record = next(row for row in lock["files"] if row["dst"] == CHECK_DST)
    assert record["hash"] == _digest(CHECK_NEW)
    assert record["base_hash"] == _digest(CHECK_TEMPLATE)


def test_heal_layout_keeps_and_names_an_edited_file(layout, capsys):
    _, target, _ = layout
    _claim_check_tree(layout, edited=CHECK_EDITED)

    assert _upgrade(layout, "--heal-layout") == 0
    assert (f"kept {CHECK_DST}: you edited it, so it still names the old path; "
            "correct it by hand") in capsys.readouterr().out
    assert (target / CHECK_DST).read_bytes() == CHECK_EDITED
    lock = scaffold.read_lockfile(target)
    assert lock["tokens"]["claim_check_command"] == "python dev/tools/claim_check.py"
    record = next(row for row in lock["files"] if row["dst"] == CHECK_DST)
    assert record["hash"] == _digest(CHECK_EDITED)


def test_heal_layout_second_run_has_nothing_to_heal(layout, capsys):
    _claim_check_tree(layout)
    assert _upgrade(layout, "--heal-layout") == 0
    capsys.readouterr()

    assert _upgrade(layout, "--heal-layout") == 0
    assert "Nothing to heal." in capsys.readouterr().out


def test_heal_layout_leaves_a_custom_token_value_alone(layout, capsys):
    _, target, _ = layout
    _claim_check_tree(layout, token="python tools/my_check.py")
    before = (target / LOCK).read_bytes()

    assert _upgrade(layout, "--heal-layout") == 0
    assert "Nothing to heal." in capsys.readouterr().out
    assert (target / LOCK).read_bytes() == before
    assert (target / CHECK_DST).read_bytes() == CHECK_OLD
