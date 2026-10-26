"""The session kernel's interpreter-binding gate and its terminal output hold at
their edges.

`dev/.cairn/local-env.json` names the program the kernel runs sub-tools with.
The kernel does not run a binding that git tracks (see
`test_session_binding_untracked.py`).  This file pins what that gate must also
cover, and what the kernel prints about a binding and about the folders it
works in:

* an interpreter the binding names *inside the project* is not run when git
  tracks it, because a branch checkout silently replaces an ignored file;
* "the same file" is decided by asking the disk (device and inode), not only by
  comparing folded names, because disks differ in which spellings they treat as
  one name, and the refusal names the entry git actually tracks;
* a binding whose bytes are not text, or whose interpreter text cannot be a
  path, is a refusal and never a Python traceback;
* every value a project can choose (a folder name, a file name, text inside an
  exception) reaches the terminal only through `encode_display`.  The test text
  includes U+3164 (Hangul filler) because `repr()` already escapes control
  characters but leaves that one invisible and printable.

Every case drives the resolver or the printing function directly, with real git
where git is involved.  Nothing a binding names is run.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_session_binding_gate_and_printing_hold.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_PATH = CAIRN_ROOT / "templates" / "skills" / "_lib" / "session.py"

pytestmark = [
    pytest.mark.skipif(not MODULE_PATH.exists(), reason="session.py template not available"),
    pytest.mark.skipif(os.name == "nt", reason="the stand-in interpreter is a shell script"),
]


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cairn_session_gate_edges", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lifecycle = _load()

#: A C1 control, a bidi override and a printable invisible filler.
NASTY = "\u009b‮ㅤ"


@pytest.fixture(autouse=True)
def _fresh_warning_state(monkeypatch):
    monkeypatch.setattr(lifecycle, "_UNTRUSTED_WARNED", False, raising=False)
    monkeypatch.setattr(lifecycle, "_STALE_WARNED", False)


# --- builders -----------------------------------------------------------------


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True, capture_output=True)


def _repo(tmp_path: Path, name: str = "project") -> Path:
    root = tmp_path.resolve() / name
    root.mkdir(parents=True)
    _git(root, "init", "-q", "-b", "main")
    for key, value in (("user.email", "t@example.com"), ("user.name", "T"),
                       ("commit.gpgsign", "false")):
        _git(root, "config", key, value)
    return root


def _executable(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return path


def _bind(root: Path, interpreter: str) -> Path:
    cfg = root / "dev" / ".cairn" / "local-env.json"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(json.dumps({"interpreter": interpreter}), encoding="utf-8")
    return cfg


def _stub_listing(monkeypatch, *entries: str) -> None:
    """Make the one `git ls-files` question answer with these entries
    (`<mode> <path>`); anything else still runs for real."""
    real = subprocess.run
    body = b"".join(f"{mode} {'0' * 40} 0\t{path}".encode("utf-8") + b"\0"
                    for mode, path in (e.split(" ", 1) for e in entries))

    def fake(argv, *args, **kwargs):
        if list(argv[:2]) == ["git", "ls-files"]:
            return subprocess.CompletedProcess(argv, 0, stdout=body, stderr=b"")
        return real(argv, *args, **kwargs)

    monkeypatch.setattr(lifecycle.subprocess, "run", fake)


def _assert_inert(text: str) -> None:
    for char in NASTY:
        assert char not in text, f"raw U+{ord(char):04X} reached the terminal"


# --- an interpreter inside the project ---------------------------------------


def test_a_checkout_that_replaces_an_in_project_interpreter_makes_it_untrusted(tmp_path, capsys):
    """An ignored `env/bin/python3` is expendable to git: checking out a branch
    that tracks that path overwrites it without a word.  Before the checkout the
    untracked program is used (the control); after it, git vouches for the
    path and the kernel falls back."""
    root = _repo(tmp_path)
    (root / ".gitignore").write_text("env/\ndev/.cairn/\n", encoding="utf-8")
    (root / "f.txt").write_text("x", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    # the branch "other" tracks env/bin/python3; on main it is an ignored file
    _git(root, "checkout", "-q", "-b", "other")
    _executable(root / "env" / "bin" / "python3")
    _git(root, "add", "-f", "--", "env/bin/python3")
    _git(root, "commit", "-q", "-m", "tracks the interpreter")
    _git(root, "checkout", "-q", "main")
    program = _executable(root / "env" / "bin" / "python3")
    _bind(root, str(program))

    assert lifecycle._resolve_interpreter(root) == (str(program), "local-env.json")

    _git(root, "checkout", "-q", "other")
    assert lifecycle._resolve_interpreter(root) == (sys.executable, "fallback-untrusted")
    assert "interpreter" in capsys.readouterr().err


def test_an_interpreter_inside_a_submodule_of_the_project_is_untrusted(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    program = _executable(root / "vendor" / "py" / "bin" / "python3")
    cfg = _bind(root, str(program))
    _stub_listing(monkeypatch, "160000 vendor/py")
    reason = lifecycle._binding_untrusted(root, cfg, program)
    assert reason == lifecycle._INTERPRETER_TRACKED


def test_an_interpreter_that_git_does_not_list_is_still_trusted(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    program = _executable(root / "env" / "bin" / "python3")
    cfg = _bind(root, str(program))
    _stub_listing(monkeypatch, "100644 env/bin/python3x", "160000 en")
    assert lifecycle._binding_untrusted(root, cfg, program) is None


def test_an_interpreter_outside_the_project_is_not_looked_up(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    program = _executable(tmp_path.resolve() / "elsewhere" / "python3")
    cfg = _bind(root, str(program))
    _stub_listing(monkeypatch, "100755 python3", "100755 elsewhere/python3")
    assert lifecycle._binding_untrusted(root, cfg, program) is None


# --- "the same file" is decided by the disk -----------------------------------


def _alias_beside(cfg: Path, name: str) -> Path:
    alias = cfg.parent / name
    os.link(cfg, alias)
    return alias


def test_a_tracked_entry_that_is_the_same_file_under_another_name_is_found_by_identity(tmp_path, monkeypatch):
    """`alias.json` is a hard link to the binding, so the disk opens both names as
    one file.  A name comparison sees two different names; the file's identity
    (device and inode) does not."""
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    _alias_beside(cfg, "aliasㅤ.json")
    _stub_listing(monkeypatch, "100644 dev/.cairn/aliasㅤ.json")
    reason = lifecycle._binding_untrusted(root, cfg)
    assert reason is not None and reason.startswith(lifecycle._BINDING_TRACKED)
    assert "git tracks it as dev/.cairn/alias\\u3164.json" in reason
    _assert_inert(reason)


def test_a_separate_file_of_the_same_folder_is_not_taken_for_the_binding(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    (cfg.parent / "alias.json").write_text("{}", encoding="utf-8")
    _stub_listing(monkeypatch, "100644 dev/.cairn/alias.json")
    assert lifecycle._binding_untrusted(root, cfg) is None


def test_a_submodule_entry_that_is_the_same_folder_by_identity_is_found(tmp_path, monkeypatch):
    """A gitlink named so that a name fold cannot equate it with `dev`, but whose
    folder the disk says is `dev`."""
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    real_lstat = os.lstat
    dev = real_lstat(root / "dev")

    def lstat(path, *args, **kwargs):
        if Path(path) == root / "de‌v":
            return dev
        return real_lstat(path, *args, **kwargs)

    _stub_listing(monkeypatch, "160000 de‌v")
    monkeypatch.setattr(lifecycle.os, "lstat", lstat)
    reason = lifecycle._binding_untrusted(root, cfg)
    assert reason is not None and reason.startswith(lifecycle._BINDING_IN_SUBMODULE)
    assert "git tracks it as de\\u200cv" in reason


def test_the_exact_name_gives_the_reason_without_a_second_name(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    _stub_listing(monkeypatch, "100644 dev/.cairn/local-env.json")
    assert lifecycle._binding_untrusted(root, cfg) == lifecycle._BINDING_TRACKED


def test_a_name_that_only_a_fold_equates_is_named_in_the_reason(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    _stub_listing(monkeypatch, "100644 DEV/.Cairn/Local-Env.JSON")
    reason = lifecycle._binding_untrusted(root, cfg)
    assert reason is not None and reason.startswith(lifecycle._BINDING_TRACKED)
    assert "git tracks it as DEV/.Cairn/Local-Env.JSON" in reason


# --- a binding that is not text, an interpreter that is not a path -------------


def test_a_binding_that_is_not_utf8_is_a_refusal_not_a_traceback(tmp_path):
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    cfg.write_bytes(b'{"interpreter": "/usr/bin/\xff"}')
    with pytest.raises(lifecycle.LifecycleError, match="not readable JSON"):
        lifecycle._resolve_interpreter(root)


def test_an_interpreter_holding_a_lone_surrogate_is_a_refusal_not_a_traceback(tmp_path):
    root = _repo(tmp_path)
    _bind(root, "/x\ud800y")
    with pytest.raises(lifecycle.LifecycleError, match="could not be inspected"):
        lifecycle._resolve_interpreter(root)


# --- exception text in refusals is printed encoded -----------------------------


@pytest.mark.skipif(hasattr(os, "geteuid") and os.geteuid() == 0,
                    reason="root reads a file whatever its mode")
def test_the_text_of_a_read_error_is_printed_encoded(tmp_path):
    """The error text names the file by `repr()`, which leaves U+3164 raw."""
    root = _repo(tmp_path, "p" + "ㅤ")
    cfg = _bind(root, "/usr/bin/true")
    cfg.chmod(0o000)
    try:
        with pytest.raises(lifecycle.LifecycleError, match="not readable JSON") as caught:
            lifecycle._resolve_interpreter(root)
    finally:
        cfg.chmod(0o644)
    _assert_inert(str(caught.value))


def test_the_text_of_an_inspect_error_is_printed_encoded(tmp_path):
    root = _repo(tmp_path)
    _bind(root, "/tmp/" + "a" * 300 + "ㅤ" + "/python")
    with pytest.raises(lifecycle.LifecycleError, match="could not be inspected") as caught:
        lifecycle._resolve_interpreter(root)
    _assert_inert(str(caught.value))


# --- the folder's name and operator paths reach the terminal encoded -----------


def _nasty_root(tmp_path: Path) -> Path:
    root = tmp_path.resolve() / ("p" + NASTY)
    root.mkdir()
    return root


def _site_assert_within(tmp_path, monkeypatch, capsys) -> str:
    root = _nasty_root(tmp_path)
    with pytest.raises(lifecycle.LifecycleError) as caught:
        lifecycle._assert_within(tmp_path.resolve() / ("elsewhere" + NASTY) / "x.md",
                                   root / "dev" / "reflections")
    return str(caught.value)


def _site_heal_skill_symlink(tmp_path, monkeypatch, capsys) -> str:
    root = _nasty_root(tmp_path)
    (root / ".claude" / "skills").mkdir(parents=True)
    (root / ".agents" / "skills").mkdir(parents=True)
    assert lifecycle._heal_skill_symlink(root / ".claude" / "skills",
                                         root / ".agents" / "skills") == "exists-nonsymlink"
    return capsys.readouterr().err


def _site_handoff_lock(tmp_path, monkeypatch, capsys) -> str:
    root = _nasty_root(tmp_path)
    (root / "dev" / ".cairn").mkdir(parents=True)
    (root / "dev" / ".cairn" / "handoff.lock").write_text("{}", encoding="utf-8")
    with pytest.raises(lifecycle.LifecycleError, match="already in progress") as caught:
        lifecycle.HandoffLock(root, "agent").acquire()
    return str(caught.value)


def _site_stale_message(tmp_path, monkeypatch, capsys) -> str:
    root = _nasty_root(tmp_path)
    _bind(root, "/nonexistent/python")
    monkeypatch.setattr(sys, "executable", "/opt/" + NASTY + "/python")
    lifecycle._resolve_interpreter(root)
    return capsys.readouterr().err


def _exec_format_error(*args, **kwargs):
    raise OSError(8, "Exec format error", "/opt/" + NASTY + "/python")


def _run_site(call):
    def site(tmp_path, monkeypatch, capsys) -> str:
        root = _nasty_root(tmp_path)
        tool = root / "tools" / "tool.py"
        tool.parent.mkdir()
        tool.write_text("pass\n", encoding="utf-8")
        monkeypatch.setattr(lifecycle, "_sibling_tool", lambda name: tool)
        monkeypatch.setattr(lifecycle.subprocess, "run", _exec_format_error)
        call(root)
        return capsys.readouterr().err
    return site


SITES = {
    "assert_within": _site_assert_within,
    "heal_skill_symlink": _site_heal_skill_symlink,
    "handoff_lock_refusal": _site_handoff_lock,
    "stale_message_names_the_running_interpreter": _site_stale_message,
    "intent_list_run_failure": _run_site(lambda root: lifecycle._surface_intents(root, "/x/python")),
    "intent_prune_run_failure": _run_site(
        lambda root: lifecycle._prune_intents(root, "/x/python", 30, dry_run=True)),
    "evolution_infer_run_failure": _run_site(lambda root: lifecycle._run_evolution_infer(root, "/x/python")),
}


@pytest.mark.parametrize("site", sorted(SITES))
def test_a_value_the_project_chooses_is_printed_encoded(site, tmp_path, monkeypatch, capsys):
    text = SITES[site](tmp_path, monkeypatch, capsys)
    assert text, "the site printed nothing, so the test did not reach it"
    _assert_inert(text)
    assert "\\u3164" in text
