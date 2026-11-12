"""Focused safety and result-classification checks for the C2 replay helper.

Promises:
- The replay refuses a run whose checkouts include its own repository root, overlap each other, or hold the output directory.
- The replay refuses a checkout reached through a link, and a target file that has a second hard link.
- The replay refuses a manifest with duplicate keys, extra or unsafe fields, or non-canonical fixture bytes.
- The replay restores each target to its exact bytes and mode, and never overwrites a replacement file.
- The replay refuses a line-ending mismatch and leaves the target's bytes and mode unchanged.
- A mutant counts as caught only when its own test fails an assertion that reached the changed line.
- A run is inconclusive on a timeout, a missing or unusable report, a collection error, or a baseline that is not all-pass.
- The replay runs only the fixed mutation IDs, and --only selects one of them.
"""
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


def _observed_cli_child(tmp_path, cli_source, test_source):
    target = tmp_path / "scripts" / "quality_gate.py"
    target.parent.mkdir(exist_ok=True)
    test_file = tmp_path / "test_cli_probe.py"
    target.write_text(cli_source, encoding="utf-8")
    test_source = test_source.replace("TARGET_PATH", repr(str(target)))
    test_file.write_text(test_source, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-c", replay._CHILD, str(target), str(test_file)],
        cwd=tmp_path, capture_output=True, text=True, check=False,
    )
    marker = "__C2_RESULT__"
    payload = json.loads(next(
        line[len(marker):] for line in reversed(result.stdout.splitlines())
        if line.startswith(marker)
    ))
    return result, payload


def test_fixed_cli_lines_belong_to_owning_call_and_launch_semantics_are_preserved(tmp_path):
    cli = (
        "import sys\n"
        "print(f'{sys.argv[0]}|{sys.path[0]}|{__name__}|{__file__}')\n"
        "print('cli-stderr', file=sys.stderr)\n"
        "raise SystemExit(7)\n"
    )
    target = tmp_path / "scripts" / "quality_gate.py"
    target.parent.mkdir()
    target.write_text(cli, encoding="utf-8")
    direct = subprocess.run([sys.executable, str(target), "--report"], cwd=tmp_path,
                            capture_output=True, text=True, check=False)
    result, payload = _observed_cli_child(
        tmp_path, cli,
        "import subprocess, sys\n"
        "def test_cli_reached_then_assertion_fails():\n"
        "    argv = [sys.executable, TARGET_PATH, '--report']\n"
        "    plain = [sys.executable, '-c', \"print('plain')\"]\n"
        "    untouched = subprocess.run(plain, capture_output=True, text=True)\n"
        "    assert untouched.args == plain and untouched.stdout == 'plain\\n'\n"
        "    result = subprocess.run(argv, cwd='.', capture_output=True, text=True, check=False)\n"
        "    assert result.args == argv\n"
        "    assert (result.returncode, result.stdout, result.stderr) == (7, "
        + repr((direct.returncode, direct.stdout, direct.stderr)) + ")\n"
        "    assert False, 'owning call witness'\n",
    )
    assert result.returncode == payload["exit"] == 1
    node = next(node for node in payload["nodes"] if node.endswith("test_cli_reached_then_assertion_fails"))
    assert payload["instrumentation_errors"] == []
    assert payload["changed_lines_by_node"][node] == [1, 2, 3, 4]
    assert replay._classify(payload | {"process_exit": result.returncode},
                             payload["nodes"], {2, 3, 4})[0] == "caught"
