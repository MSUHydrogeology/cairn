"""Tests for the lifecycle CLI's safety layer (Chunk 2 of the executing plan
`2026-06-01-claude-cairn-vendor-neutral-skills`).

Covers the load-bearing safety properties:

* **Layer-2 fail-safe (Decision 2 / R5).**  `session-end` defaults to
  reflection-only; `--handoff` without the designation marker refuses
  non-interactively (exits non-zero, never blocks on input); with the marker it
  proceeds.
* **`--handoff --dry-run` mutation manifest (S6).**  Emits the manifest, mutates
  nothing, needs no marker.
* **II2 + S1 concurrent-handoff lock.**  A second handoff fails closed while a
  live holder holds the lock *even past the lease interval*; the lock is removed
  on an ordinary exception (EP1); a hard-killed (provably-dead) holder with an
  expired lease is reclaimable -- but an age-only-stale lock is **not** stolen.
* **R3/S2 resolve-don't-bake.**  The interpreter is resolved from
  `dev/.cairn/local-env.json` and reported; a tampered config refuses before
  running anything; with no config the runtime-resolver fallback is used and
  surfaced.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_lifecycle_failsafe.py
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_PATH = CAIRN_ROOT / "templates" / "skills" / "_lib" / "lifecycle.py"

pytestmark = pytest.mark.skipif(
    not MODULE_PATH.exists(), reason="lifecycle.py template not available"
)


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cairn_lifecycle_fs", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lifecycle = _load()


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(root), check=True,
                   capture_output=True, text=True)


@pytest.fixture()
def repo(tmp_path: Path, monkeypatch) -> Path:
    root = tmp_path.resolve()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@e.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    (root / "f.txt").write_text("x", encoding="utf-8")
    _git(root, "add", "f.txt")
    _git(root, "commit", "-q", "-m", "init")
    monkeypatch.delenv("CAIRN_HANDOFF_OWNER", raising=False)
    monkeypatch.setenv("CAIRN_AGENT", "owner")
    monkeypatch.chdir(root)
    return root


# --- Layer-2 fail-safe -------------------------------------------------------


def test_session_end_default_is_reflection_only(repo, capsys):
    # No flag: writes a reflection, runs no destructive/handoff step.
    rc = lifecycle.main(["session-end"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "reflection-only goodnight complete" in out
    assert "mutation manifest" not in out


def test_handoff_without_marker_refuses_nonblocking(repo, capsys):
    rc = lifecycle.main(["session-end", "--handoff"])
    assert rc == 1  # refuses, does not block on input
    assert "no maintainer-designation marker" in capsys.readouterr().err


def test_handoff_dry_run_emits_manifest_no_marker_no_writes(repo, capsys):
    # A stale reflection that *would* be pruned by a real handoff.
    refl = repo / "dev" / "reflections"
    refl.mkdir(parents=True)
    old = refl / "2000-01-01-someone.md"
    old.write_text("old", encoding="utf-8")

    rc = lifecycle.main(["session-end", "--handoff", "--dry-run"])

    out = capsys.readouterr().out
    assert rc == 0
    assert "mutation manifest" in out
    assert "would prune 1 reflection" in out
    assert old.exists()  # dry-run mutated nothing


def test_handoff_with_marker_runs_and_prunes(repo, monkeypatch, capsys):
    refl = repo / "dev" / "reflections"
    refl.mkdir(parents=True)
    old = refl / "2000-01-01-someone.md"
    old.write_text("old", encoding="utf-8")
    monkeypatch.setenv("CAIRN_HANDOFF_OWNER", "1")

    rc = lifecycle.main(["session-end", "--handoff"])

    out = capsys.readouterr().out
    assert rc == 0
    assert "pruned 1 reflection" in out
    assert not old.exists()  # the stale reflection was pruned
    assert not (lifecycle._state_dir(repo) / "handoff.lock").exists()  # released


def test_handoff_marker_via_state_file(repo, capsys):
    (lifecycle._state_dir(repo)).mkdir(parents=True)
    (lifecycle._state_dir(repo) / "handoff-owner").write_text("", encoding="utf-8")
    rc = lifecycle.main(["session-end", "--handoff"])
    assert rc == 0
    assert "full-handoff mechanizable steps complete" in capsys.readouterr().out


# --- II2 + S1 concurrent-handoff lock ---------------------------------------


def test_live_holder_blocks_even_past_lease(repo, monkeypatch):
    # A lock held by a LIVE pid (our own) blocks a second handoff regardless of
    # how old the lease is -- the age-only-stale path must never steal it (S1).
    lock_path = lifecycle._state_dir(repo)
    lock_path.mkdir(parents=True)
    import socket
    (lock_path / "handoff.lock").write_text(json.dumps({
        "pid": __import__("os").getpid(),  # alive (this process)
        "host": socket.gethostname(),
        "agent": "other",
        "acquired_at": 0.0,
        "heartbeat_at": 0.0,  # lease long expired
    }), encoding="utf-8")
    monkeypatch.setenv("CAIRN_HANDOFF_OWNER", "1")

    lock = lifecycle.HandoffLock(repo, "owner")
    with pytest.raises(lifecycle.LifecycleError) as exc:
        lock.acquire()
    assert "already in progress" in str(exc.value)


def test_lock_released_on_exception(repo):
    lock = lifecycle.HandoffLock(repo, "owner")
    with pytest.raises(RuntimeError):
        with lock:
            assert (lifecycle._state_dir(repo) / "handoff.lock").exists()
            raise RuntimeError("boom")
    # EP1: released on exception, not just clean exit.
    assert not (lifecycle._state_dir(repo) / "handoff.lock").exists()


def _dead_pid() -> int:
    """A pid that is reliably dead: spawn a trivial process and reap it."""
    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.wait()
    return proc.pid


def test_dead_holder_with_expired_lease_is_reclaimed(repo, capsys):
    import socket
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    (sd / "handoff.lock").write_text(json.dumps({
        "pid": _dead_pid(),            # a reaped pid -> provably dead
        "host": socket.gethostname(),  # same host, so the pid check is valid
        "agent": "crashed",
        "acquired_at": 0.0,
        "heartbeat_at": 0.0,          # lease expired
    }), encoding="utf-8")

    lock = lifecycle.HandoffLock(repo, "owner")
    lock.acquire()  # should reclaim, not raise
    try:
        assert (sd / "handoff.lock").exists()
        assert "reclaiming a stale handoff lock" in capsys.readouterr().err
    finally:
        lock.release()


def test_dead_holder_but_fresh_lease_not_stolen(repo):
    # Proof-of-death alone is not enough: a fresh lease fails closed (no steal).
    import socket
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    (sd / "handoff.lock").write_text(json.dumps({
        "pid": _dead_pid(),
        "host": socket.gethostname(),
        "agent": "x",
        "acquired_at": time.time(),
        "heartbeat_at": time.time(),  # fresh lease
    }), encoding="utf-8")

    with pytest.raises(lifecycle.LifecycleError):
        lifecycle.HandoffLock(repo, "owner").acquire()


# --- R3/S2 resolve-don't-bake ------------------------------------------------


def test_interpreter_resolved_from_local_env_and_reported(repo, capsys):
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    # A real, absolute, non-symlinked executable: the running interpreter,
    # resolved to defeat any /var -> /private/var symlink on the leaf path.
    interp = str(Path(sys.executable).resolve())
    (sd / "local-env.json").write_text(
        json.dumps({"interpreter": interp}), encoding="utf-8")

    rc = lifecycle.main(["session-start"])

    out = capsys.readouterr().out
    assert rc == 0
    assert f"interpreter: {interp}  (from local-env.json)" in out


def test_absent_local_env_uses_fallback_with_guidance(repo, capsys):
    rc = lifecycle.main(["session-start"])
    captured = capsys.readouterr()
    assert rc == 0
    assert "(from fallback)" in captured.out
    assert "no dev/.cairn/local-env.json" in captured.err


@pytest.mark.parametrize("bad", [
    {"interpreter": "relative/python"},          # not absolute
    {"interpreter": "/usr/bin/python --foo"},     # arguments
    {"interpreter": "/no/such/python"},           # not an executable file
    {"nope": "/usr/bin/python"},                  # wrong schema
])
def test_tampered_local_env_refuses(repo, bad):
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    (sd / "local-env.json").write_text(json.dumps(bad), encoding="utf-8")
    # Refuses before running anything (S2): session-start resolves eagerly.
    rc = lifecycle.main(["session-start"])
    assert rc == 1
