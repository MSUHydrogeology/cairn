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
    assert records[NEW[1]]["layout_fork"] is True
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
