"""Tests for the lifecycle CLI's safety layer (Chunk 2 of the executing plan
`2026-06-01-claude-cairn-vendor-neutral-skills`).

Covers the load-bearing safety properties:

* **Layer-2 fail-safe.**  `session-end` defaults to
  reflection-only; `--handoff` without the designation marker refuses
  non-interactively (exits non-zero, never blocks on input); with the marker it
  proceeds.
* **`--handoff --dry-run` mutation manifest.**  Emits the manifest, mutates
  nothing, needs no marker.
* **The concurrent-handoff lock.**  A second handoff fails closed while a
  live holder holds the lock *even past the lease interval*; the lock is removed
  on an ordinary exception; a hard-killed (provably-dead) holder with an
  expired lease is reclaimable -- but an age-only-stale lock is **not** stolen.
* **Resolve-don't-bake: absent degrades, present-but-wrong refuses.**
  The interpreter is resolved from `dev/.cairn/local-env.json` and reported;
  a structurally-valid-but-absent path degrades to the current interpreter
  with a warning naming the stale path and the substitute, exactly once per
  process; every other tampered shape (relative, parent-traversal, wrong
  schema, present-but-non-executable, present-directory, symlinked leaf or
  parent, uninspectable) still refuses before running anything; with no
  config the runtime-resolver fallback is used and surfaced.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_lifecycle_failsafe.py
"""
from __future__ import annotations

import importlib.util
import inspect
import json
import os
import stat
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


@pytest.fixture(autouse=True)
def _reset_stale_warned_sentinel():
    """The module-level ``_STALE_WARNED`` sentinel persists across
    test *nodes* (the module loads once per session via `_load()` above), so
    without this reset the first stale-path test to run would trip the
    sentinel and every subsequent node would silently observe zero warnings.
    Reset before AND after, so a test's own leftover state never leaks either
    direction."""
    lifecycle._STALE_WARNED = False
    yield
    lifecycle._STALE_WARNED = False


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


# --- the concurrent-handoff lock ---------------------------------------------


def test_live_holder_blocks_even_past_lease(repo, monkeypatch):
    # A lock held by a LIVE pid (our own) blocks a second handoff regardless of
    # how old the lease is -- the age-only-stale path must never steal it.
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
    # Released on exception, not just clean exit.
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


# --- resolve-don't-bake: absent degrades, present-but-wrong refuses ---------


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


def _make_exe(path: Path, body: str = "#!/bin/sh\nexit 0\n") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


# The two absent-path values
# (`/usr/bin/python --foo`, `/no/such/python`) that used to live in this
# parametrize now DEGRADE, not refuse (see test_stale_interpreter_path_
# degrades_with_guidance below) -- replaced with a present-non-executable
# file and a present directory, materialized in the body via a
# non-id-representable sentinel dict (module-level parametrize values cannot
# use the `repo` fixture, and `_make_exe` is defined above but the file it
# writes needs a per-test tmp path). `ids=` pinned explicitly: an
# all-dict-except-one-string parametrize list silently drops a node from
# collection, verified empirically this session's plan-review.
@pytest.mark.parametrize("bad", [
    {"interpreter": "relative/python"},          # not absolute
    {"kind": "present-nonexec"},                  # present, not executable
    {"kind": "present-dir"},                      # present, a directory
    {"nope": "/usr/bin/python"},                  # wrong schema (no interpreter key)
], ids=["bad0", "bad1", "bad2", "bad3"])
def test_tampered_local_env_refuses(repo, bad):
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    if bad.get("kind") == "present-nonexec":
        if os.name != "posix":
            pytest.skip("present-non-executable case is POSIX-only pending S3")
        nonexec = repo / "nonexec"
        nonexec.write_text("not executable", encoding="utf-8")
        bad = {"interpreter": str(nonexec)}
    elif bad.get("kind") == "present-dir":
        adir = repo / "adir"
        adir.mkdir()
        bad = {"interpreter": str(adir)}
    (sd / "local-env.json").write_text(json.dumps(bad), encoding="utf-8")
    # Refuses before running anything: session-start resolves eagerly.
    rc = lifecycle.main(["session-start"])
    assert rc == 1


# Materialized from the test's resolved `repo` path, not hardcoded
# POSIX literals -- `/usr/bin/python --foo` / `/no/such/python` are not
# absolute under PureWindowsPath, so on Windows they would hit the
# "must be an absolute path" fatal branch instead of the accepted
# absent-path degrade.
@pytest.mark.parametrize("stale_kind", ["plain-absent", "appended-argument"],
                          ids=["plain-absent", "appended-argument"])
def test_stale_interpreter_path_degrades_with_guidance(repo, stale_kind, capsys):
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    if stale_kind == "plain-absent":
        stale = str(repo / "no" / "such" / "python")
    else:
        stale = f"{repo / 'python'} --foo"
    (sd / "local-env.json").write_text(
        json.dumps({"interpreter": stale}), encoding="utf-8")

    rc = lifecycle.main(["session-start"])

    out, err = capsys.readouterr()
    assert rc == 0
    assert "(from fallback-stale)" in out
    assert lifecycle._REBIND_REMEDY in err
    # The Decision's binding condition requires both the stale value and
    # the substituted interpreter named in the warning, not merely a generic
    # remedy string.
    assert stale in err
    assert sys.executable in err


def test_stale_warning_fires_once_per_process(repo, tmp_path, monkeypatch, capsys):
    """A count fix, not presence: the resolver is reached up to four times
    in one `session-end --handoff` (`_intent_whoami`, `cmd_session_start`,
    `_do_reflection`, `_do_full_handoff`). CAIRN_AGENT/CAIRN_SESSION are left
    UNSET (unlike the `repo` fixture's default) so `_resolve_agent`/
    `_resolve_session` take the real multi-call path through `_intent_whoami`
    rather than short-circuiting on the env var."""
    monkeypatch.delenv("CAIRN_AGENT", raising=False)
    monkeypatch.delenv("CAIRN_SESSION", raising=False)
    fake_intent = _make_exe(
        tmp_path / "fake_intent.py",
        body="import sys; print('agent-77777777')\n",
    )
    monkeypatch.setattr(
        lifecycle, "_sibling_tool",
        lambda name: fake_intent if name == "intent.py" else None,
    )
    monkeypatch.setenv("CAIRN_HANDOFF_OWNER", "1")

    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    stale = str(repo / "no" / "such" / "python")
    (sd / "local-env.json").write_text(
        json.dumps({"interpreter": stale}), encoding="utf-8")

    lifecycle.main(["session-end", "--handoff"])

    err = capsys.readouterr().err
    assert err.count("no longer exists") == 1, err


def test_stale_binding_is_not_rewritten(repo):
    """The resolver contains no write path against `local-env.json`
    today -- this is a forward regression guard against the explicitly-
    rejected auto-rebind alternative, not a guard against a mechanism that
    presently exists."""
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    cfg = sd / "local-env.json"
    stale = str(repo / "no" / "such" / "python")
    payload = json.dumps({"interpreter": stale})
    cfg.write_text(payload, encoding="utf-8")
    before = cfg.read_bytes()

    lifecycle.main(["session-start"])

    assert cfg.read_bytes() == before


@pytest.mark.skipif(os.name != "posix" or os.geteuid() == 0,
                     reason="EACCES-parent case needs a non-root POSIX host")
def test_uninspectable_interpreter_path_refuses(repo):
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    blocked = repo / "blocked"
    blocked.mkdir()
    inner = blocked / "python"
    (sd / "local-env.json").write_text(
        json.dumps({"interpreter": str(inner)}), encoding="utf-8")
    os.chmod(blocked, 0o000)
    try:
        with pytest.raises(lifecycle.LifecycleError) as exc:
            lifecycle._resolve_interpreter(repo)
        assert "could not be inspected" in str(exc.value)
    finally:
        os.chmod(blocked, 0o755)


def test_parent_traversal_segment_refuses(repo):
    """A `..` component raises before ever reaching `_probe_interpreter`
    (the narrowed guard)."""
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    dotdot = str(repo / "a" / ".." / "python")
    (sd / "local-env.json").write_text(
        json.dumps({"interpreter": dotdot}), encoding="utf-8")
    with pytest.raises(lifecycle.LifecycleError) as exc:
        lifecycle._resolve_interpreter(repo)
    assert "parent-traversal" in str(exc.value)


def test_symlinked_parent_with_absent_leaf_still_refuses(repo):
    """The required probe ordering: the symlink walk runs before
    absence classification, so a symlinked parent whose leaf does not exist
    still refuses -- it does not degrade."""
    if not hasattr(os, "symlink"):
        pytest.skip("host cannot create symlinks")
    real_dir = repo / "realdir"
    real_dir.mkdir()
    link_dir = repo / "linkdir"
    try:
        link_dir.symlink_to(real_dir)
    except OSError:
        pytest.skip("host refused to create a symlink")
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    (sd / "local-env.json").write_text(
        json.dumps({"interpreter": str(link_dir / "python")}), encoding="utf-8")
    with pytest.raises(lifecycle.LifecycleError) as exc:
        lifecycle._resolve_interpreter(repo)
    assert "symlink" in str(exc.value)


def test_symlinked_leaf_refuses(repo):
    if not hasattr(os, "symlink"):
        pytest.skip("host cannot create symlinks")
    real = _make_exe(repo / "realpy")
    link = repo / "linkpy"
    try:
        link.symlink_to(real)
    except OSError:
        pytest.skip("host refused to create a symlink")
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    (sd / "local-env.json").write_text(
        json.dumps({"interpreter": str(link)}), encoding="utf-8")
    with pytest.raises(lifecycle.LifecycleError) as exc:
        lifecycle._resolve_interpreter(repo)
    assert "symlink" in str(exc.value)


def test_space_in_interpreter_path_accepted(repo):
    # Finding 1: a space is legitimate in a real path (`My Drive`, OneDrive).
    # argv-based invocation makes it harmless; the file check guards args.
    exe = _make_exe(repo / "env with space" / "python")
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    (sd / "local-env.json").write_text(
        json.dumps({"interpreter": str(exe)}), encoding="utf-8")

    interp, source = lifecycle._resolve_interpreter(repo)

    assert source == "local-env.json"
    assert interp == str(exe)


def test_extra_key_in_local_env_refused(repo):
    # Finding 4: the single-key contract is enforced, not just documented.
    exe = _make_exe(repo / "bin" / "python")
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    (sd / "local-env.json").write_text(
        json.dumps({"interpreter": str(exe), "evil": "x"}), encoding="utf-8")

    with pytest.raises(lifecycle.LifecycleError):
        lifecycle._resolve_interpreter(repo)


def test_full_handoff_surfaces_intents(repo, tmp_path, monkeypatch, capsys):
    # Finding 2: the real (non-dry-run) handoff actually runs the active-intent
    # read its manifest promises -- not just session-start.
    fake_intent = _make_exe(
        tmp_path / "fake_intent.py",
        body="import sys; print('INTENT-LIST-RAN', ' '.join(sys.argv[1:]))\n",
    )
    monkeypatch.setattr(
        lifecycle, "_sibling_tool",
        lambda name: fake_intent if name == "intent.py" else None,
    )
    monkeypatch.setenv("CAIRN_HANDOFF_OWNER", "1")

    rc = lifecycle.main(["session-end", "--handoff"])

    out = capsys.readouterr().out
    assert rc == 0
    assert "INTENT-LIST-RAN list" in out  # invoked as [interp, intent, "list"]


def test_tampered_binding_warns_in_intent_whoami(repo, monkeypatch, capsys):
    """A present-but-wrong binding does NOT make
    `_intent_whoami` return `None` when a valid sibling tool exists -- the
    fallback actually runs the sibling under `sys.executable` and returns
    its real output. The only remaining signal is the original refusal
    surfaced on stderr before the fallback runs."""
    fake_intent = _make_exe(
        repo / "intent.py",
        body="import sys; print('agent-99999999')\n",
    )
    monkeypatch.setattr(
        lifecycle, "_sibling_tool",
        lambda name: fake_intent if name == "intent.py" else None,
    )
    sd = lifecycle._state_dir(repo)
    sd.mkdir(parents=True)
    nonexec = repo / "nonexec"
    nonexec.write_text("not executable", encoding="utf-8")
    (sd / "local-env.json").write_text(
        json.dumps({"interpreter": str(nonexec)}), encoding="utf-8")

    result = lifecycle._intent_whoami(repo)

    err = capsys.readouterr().err
    assert "interpreter binding refused" in err
    assert result == "agent-99999999"


def test_resolver_source_has_no_write_primitive():
    """Static proof the resolver carries no write/stage/commit call
    against the state directory (a forward regression guard, matching
    test_lifecycle_contract.py's `_PLANNER_PATH` source-scan pattern -- that
    file scans the *planner*, not this module, so it is a pattern to copy,
    not an existing guard covering this module)."""
    src = inspect.getsource(lifecycle._resolve_interpreter)
    assert ".write_text(" not in src
    assert ".write_bytes(" not in src
    assert "os.symlink(" not in src
    assert "shutil.move(" not in src and "shutil.copy" not in src
