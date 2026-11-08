"""Focused safety and result-classification checks for the C2 replay helper."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "replay_ordinary_c2_mutants.py"
SPEC = importlib.util.spec_from_file_location("ordinary_c2_replay", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
replay = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = replay
SPEC.loader.exec_module(replay)


def _checkout(root: Path):
    path, chain = replay._chain(root, final_dir=True)
    return replay.Checkout(path, chain)


def _phases(call: dict | None = None, setup: dict | None = None,
            teardown: dict | None = None) -> dict:
    return {
        "node": {
            "setup": setup or {"outcome": "passed", "wasxfail": None},
            "call": call or {"outcome": "passed", "wasxfail": None,
                             "assertion_failure": False},
            "teardown": teardown or {"outcome": "passed", "wasxfail": None},
        }
    }


def test_manifest_rejects_duplicate_keys_and_noncanonical_fixture(tmp_path, monkeypatch):
    with pytest.raises(replay.ReplayError, match="duplicate JSON key"):
        replay._object_no_duplicates([("x", 1), ("x", 2)])
    alternate = tmp_path / "manifest.json"
    alternate.write_bytes(replay.DATA.read_bytes() + b" ")
    monkeypatch.setattr(replay, "DATA", alternate)
    with pytest.raises(replay.ReplayError, match="canonical fixture bytes"):
        replay._load_manifest()


@pytest.mark.parametrize(
    "edit, message",
    [
        (lambda data: data.update(extra=True), "unexpected fixture fields"),
        (lambda data: data["mutants"][0].update(id="../escape"), "unsafe or duplicate"),
        (lambda data: data["mutants"][1].update(id=data["mutants"][0]["id"]), "unsafe or duplicate"),
        (lambda data: data["mutants"][0].update(family="unknown"), "unsupported mutation family"),
        (lambda data: data["mutants"][0].update(family=[]), "unsupported mutation family"),
        (lambda data: data["mutants"][0].update(old=None), "invalid mutation text"),
        (lambda data: data["mutants"][0].update(source="../../outside.py"), "does not match fixed family"),
        (lambda data: data["mutants"][0].update(target="../../outside.py"), "does not match fixed family"),
        (lambda data: data["mutants"].append(copy.deepcopy(data["mutants"][0])), "exactly fifteen"),
        (lambda data: data["candidate_only_probe"].update(target="scripts/../outside.py"), "invalid candidate-only"),
    ],
)
def test_manifest_rejects_extra_unsafe_or_unsupported_metadata(edit, message):
    mutants, extra = replay._load_manifest()
    data = json.loads(replay.DATA.read_text(encoding="utf-8"))
    data["mutants"] = mutants
    data["candidate_only_probe"] = extra
    edit(data)
    with pytest.raises(replay.ReplayError, match=message):
        replay._validate_manifest(data)


@pytest.mark.skipif(not replay.HAS_SAFE_OPEN, reason="requires no-follow directory descriptors")
def test_root_preflight_refuses_overlap_self_and_nested_output(tmp_path):
    old = tmp_path / "old"
    new = tmp_path / "new"
    old.mkdir()
    new.mkdir()
    (old / "child").mkdir()
    with pytest.raises(replay.ReplayError, match="overlap"):
        replay._paths(old, old / "child", tmp_path / "logs")
    with pytest.raises(replay.ReplayError, match="overlap"):
        replay._paths(old, old, tmp_path / "logs")
    with pytest.raises(replay.ReplayError, match="own repository root"):
        replay._paths(replay.ROOT, new, tmp_path / "logs")
    with pytest.raises(replay.ReplayError, match="outside both checkouts"):
        replay._paths(old, new, old / "logs")


@pytest.mark.skipif(not replay.HAS_SAFE_OPEN, reason="requires no-follow directory descriptors")
def test_target_walk_rejects_linked_parent_and_hardlinked_leaf(tmp_path):
    root = tmp_path / "project"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (outside / "quality_gate.py").write_text("source\n")
    root_alias = tmp_path / "project-alias"
    root_alias.symlink_to(root, target_is_directory=True)
    with pytest.raises(replay.ReplayError, match="link"):
        replay._chain(root_alias, True)
    (root / "scripts").symlink_to(outside, target_is_directory=True)
    checkout = _checkout(root)
    try:
        with pytest.raises(replay.ReplayError, match="unsafe"):
            replay._read_target(checkout, "scripts/quality_gate.py")
    finally:
        checkout.close()

    linked_root = tmp_path / "linked-project"
    scripts = linked_root / "scripts"
    scripts.mkdir(parents=True)
    target = scripts / "quality_gate.py"
    target.write_bytes(b"source\n")
    os.link(target, scripts / "second-name.py")
    checkout = _checkout(linked_root)
    try:
        with pytest.raises(replay.ReplayError, match="unsafe replay target component"):
            replay._read_target(checkout, "scripts/quality_gate.py")
    finally:
        checkout.close()


def test_crlf_preimage_refuses_without_changing_bytes_or_mode(tmp_path):
    path = tmp_path / "target.py"
    original = b"if j >= jaccard_threshold:\r\n    run()\r\n"
    path.write_bytes(original)
    path.chmod(0o640)
    mode = stat.S_IMODE(path.stat().st_mode)
    with pytest.raises(replay.ReplayError, match="line endings differ"):
        replay._mutant_bytes(original, "if j >= jaccard_threshold:\n    run()", "pass", "r1")
    assert path.read_bytes() == original
    assert stat.S_IMODE(path.stat().st_mode) == mode


@pytest.mark.skipif(not replay.HAS_SAFE_OPEN, reason="requires no-follow directory descriptors")
def test_restore_keeps_exact_bytes_and_mode_and_replacement_is_never_overwritten(tmp_path):
    root = tmp_path / "project"
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    path = scripts / "quality_gate.py"
    original = b"line one\r\nline two\r\n"
    path.write_bytes(original)
    path.chmod(0o640)
    checkout = _checkout(root)
    try:
        before, mode, identity, chain = replay._read_target(checkout, "scripts/quality_gate.py")
        mutated = b"changed\r\n"
        replay._write_target(checkout, "scripts/quality_gate.py", mutated, mode, identity, chain, before)
        replay._write_target(checkout, "scripts/quality_gate.py", before, mode, identity, chain, None)
        restored, restored_mode, restored_identity, _restored_chain = replay._read_target(
            checkout, "scripts/quality_gate.py",
        )
        assert (restored, restored_mode, restored_identity) == (before, mode, identity)

        replacement_source = tmp_path / "replacement.py"
        replacement_source.write_bytes(b"unrelated replacement\n")
        path.unlink()
        os.replace(replacement_source, path)
        replacement = path.read_bytes()
        with pytest.raises(replay.ReplayError, match="target was replaced"):
            replay._write_target(checkout, "scripts/quality_gate.py", before, mode, identity, chain, None)
        assert path.read_bytes() == replacement
    finally:
        checkout.close()


@pytest.mark.parametrize(
    "process_exit, call, setup, teardown, collection_errors, changed, expected",
    [
        (1, {"outcome": "failed", "wasxfail": None, "assertion_failure": True}, None, None, [], [10], "caught"),
        (0, None, None, None, [], [10], "survived"),
        (1, {"outcome": "failed", "wasxfail": None, "assertion_failure": False}, None, None, [], [10], "inconclusive"),
        (1, {"outcome": "failed", "wasxfail": None, "assertion_failure": True}, {"outcome": "failed", "wasxfail": None}, None, [], [10], "inconclusive"),
        (1, {"outcome": "failed", "wasxfail": None, "assertion_failure": True}, None, {"outcome": "failed", "wasxfail": None}, [], [10], "inconclusive"),
        (1, {"outcome": "failed", "wasxfail": "reason", "assertion_failure": True}, None, None, [], [10], "inconclusive"),
        (1, {"outcome": "failed", "wasxfail": None, "assertion_failure": True}, None, None, [{"nodeid": "bad"}], [10], "inconclusive"),
        (1, {"outcome": "failed", "wasxfail": None, "assertion_failure": True}, None, None, [], [], "inconclusive"),
        (0, {"outcome": "failed", "wasxfail": None, "assertion_failure": True}, None, None, [], [10], "inconclusive"),
    ],
)
def test_mutant_result_requires_owning_assertion_and_changed_line(
    process_exit, call, setup, teardown, collection_errors, changed, expected,
):
    data = {
        "exit": process_exit,
        "process_exit": process_exit,
        "nodes": ["node"],
        "phases": _phases(call, setup, teardown),
        "collection_errors": collection_errors,
        "internal_errors": [],
        "changed_lines": changed,
        "changed_lines_by_node": {"node": changed},
    }
    outcome, _detail = replay._classify(data, ["node"], {10})
    assert outcome == expected


def test_child_records_genuine_reached_assertion(tmp_path):
    watched = tmp_path / "watched.py"
    watched.write_text("VALUE = 1\n")
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(
        "import watched\n\n"
        "def test_target_assertion():\n"
        "    assert watched.VALUE == 2\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", replay._CHILD, str(watched), str(test_file)],
        cwd=tmp_path, capture_output=True, text=True, check=False,
    )
    marker = "__C2_RESULT__"
    payload = json.loads(next(
        line[len(marker):] for line in reversed(result.stdout.splitlines())
        if line.startswith(marker)
    ))
    assert result.returncode == payload["exit"] == 1
    assert payload["collection_errors"] == []
    assert payload["changed_lines"] == [1]
    node = next(node for node in payload["nodes"] if node.endswith("test_probe.py::test_target_assertion"))
    assert payload["changed_lines_by_node"][node] == [1]
    assert payload["phases"][node]["call"] == {
        "outcome": "failed", "wasxfail": None, "assertion_failure": True,
    }
    assert replay._classify(
        payload | {"process_exit": result.returncode}, payload["nodes"], {1},
    )[0] == "caught"


def test_baseline_requires_nonempty_ordinary_all_pass_reports():
    rows = _phases()
    data = {
        "exit": 0, "process_exit": 0, "nodes": ["node"],
        "phases": rows, "collection_errors": [], "internal_errors": [],
    }
    assert replay._ordinary_baseline(data)[0]
    rows["node"]["call"]["wasxfail"] = "unexpected xfail"
    assert not replay._ordinary_baseline(data)[0]
    assert not replay._ordinary_baseline({**data, "nodes": [], "phases": {}})[0]


def test_timeout_and_missing_reports_are_inconclusive():
    timeout = {"timeout": True, "process_exit": None}
    assert replay._classify(timeout, ["node"], {10})[0] == "inconclusive"
    missing = {
        "exit": 1, "process_exit": 1, "nodes": ["node"], "phases": {},
        "collection_errors": [], "internal_errors": [], "changed_lines": [10],
    }
    assert replay._classify(missing, ["node"], {10})[0] == "inconclusive"


def test_unrelated_assertion_does_not_count_when_mutated_line_ran_in_another_node():
    data = {
        "exit": 1, "process_exit": 1, "nodes": ["failed", "reached"],
        "phases": {
            "failed": _phases({"outcome": "failed", "wasxfail": None,
                                "assertion_failure": True})["node"],
            "reached": _phases()["node"],
        },
        "collection_errors": [], "internal_errors": [], "changed_lines": [10],
        "changed_lines_by_node": {"failed": [], "reached": [10]},
    }
    assert replay._classify(data, ["failed", "reached"], {10})[0] == "inconclusive"
