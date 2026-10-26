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
  one name, and the refusal names the entry git actually tracks, in the command
  it gives for removing it too;
* a disk that reports inode 0 for every file gives no identity to compare, and a
  disk that will not answer about the binding is a refusal worded for the disk,
  not for git;
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


TRACKED_OPENING = "dev/.cairn/local-env.json is tracked by git"


def _project_whose_other_branch_tracks_the_interpreter(tmp_path: Path, name: str):
    """A project on `main` where `env/bin/python3` is an ignored file; branch
    `other` tracks that path, so `git checkout other` overwrites the file in
    place.  Returns the project and the program as it stands on `main`."""
    root = _repo(tmp_path, name)
    (root / ".gitignore").write_text("env/\ndev/.cairn/\n", encoding="utf-8")
    (root / "f.txt").write_text("x", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    _git(root, "checkout", "-q", "-b", "other")
    _executable(root / "env" / "bin" / "python3")
    _git(root, "add", "-f", "--", "env/bin/python3")
    _git(root, "commit", "-q", "-m", "tracks the interpreter")
    _git(root, "checkout", "-q", "main")
    return root, _executable(root / "env" / "bin" / "python3")


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
    root, program = _project_whose_other_branch_tracks_the_interpreter(tmp_path, "project")
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


@pytest.mark.parametrize("respell", [str.lower, str.upper], ids=["lower", "upper"])
def test_a_checkout_is_noticed_when_the_binding_spells_the_project_folder_in_another_case(
        tmp_path, respell):
    """On a disk that opens `CaseProj` and `caseproj` as one folder, the binding
    can name the program with the folder spelled either way, while git reports
    the spelling on disk.  The in-project test must not depend on the spelling."""
    if not _disk_ignores_letter_case(tmp_path):
        pytest.skip("this disk tells letter cases apart")
    root, program = _project_whose_other_branch_tracks_the_interpreter(tmp_path, "CaseProj")
    spelled = tmp_path.resolve() / respell("CaseProj") / "env" / "bin" / "python3"
    assert spelled != program and spelled.is_file()
    _bind(root, str(spelled))

    assert lifecycle._resolve_interpreter(root) == (str(spelled), "local-env.json")

    _git(root, "checkout", "-q", "other")
    assert lifecycle._resolve_interpreter(root) == (sys.executable, "fallback-untrusted")


@pytest.mark.parametrize("entry", ["Env/bin/python3", "ENV/BIN/PYTHON3"])
def test_an_interpreter_is_found_whatever_case_the_index_spells_its_folder(tmp_path, monkeypatch, entry):
    """Both sides of the comparison are folded.  The folder is `Env` on disk, so a
    side left unfolded would not meet the folded index entry, even when the two
    are spelled alike."""
    root = _repo(tmp_path)
    program = _executable(root / "Env" / "bin" / "python3")
    cfg = _bind(root, str(program))
    _stub_listing(monkeypatch, f"100755 {entry}")
    assert lifecycle._binding_untrusted(root, cfg, program) == lifecycle._INTERPRETER_TRACKED


def test_an_in_project_interpreter_is_found_when_the_project_is_reached_through_a_link(
        tmp_path, monkeypatch):
    """The binding spells the program by its real path; the kernel is started in
    the project through a link.  The project's own path is resolved before the
    program is looked for under it."""
    real = _repo(tmp_path)
    program = _executable(real / "env" / "bin" / "python3")
    link = tmp_path.resolve() / "link"
    link.symlink_to(real, target_is_directory=True)
    _bind(real, str(program))
    _stub_listing(monkeypatch, "100755 env/bin/python3")

    assert lifecycle._resolve_interpreter(link) == (sys.executable, "fallback-untrusted")


def test_the_same_project_through_a_link_still_trusts_a_program_git_does_not_list(
        tmp_path, monkeypatch):
    real = _repo(tmp_path)
    program = _executable(real / "env" / "bin" / "python3")
    link = tmp_path.resolve() / "link"
    link.symlink_to(real, target_is_directory=True)
    _bind(real, str(program))
    _stub_listing(monkeypatch, "100755 env/bin/python3x")

    assert lifecycle._resolve_interpreter(link) == (str(program), "local-env.json")


def _disk_ignores_letter_case(tmp_path: Path) -> bool:
    (tmp_path / "CaseProbe").mkdir()
    return (tmp_path / "caseprobe").exists()


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
    assert reason is not None and reason.startswith(TRACKED_OPENING)
    assert "git tracks it as dev/.cairn/alias\\u3164.json" in reason
    assert "git rm dev/.cairn/alias\\u3164.json" in reason
    assert "git rm dev/.cairn/local-env.json" not in reason
    _assert_inert(reason)


def test_a_separate_file_of_the_same_folder_is_not_taken_for_the_binding(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    (cfg.parent / "alias.json").write_text("{}", encoding="utf-8")
    _stub_listing(monkeypatch, "100644 dev/.cairn/alias.json")
    assert lifecycle._binding_untrusted(root, cfg) is None


@pytest.mark.parametrize("folder, entry, shown", [
    (("dev",), "de\u200cv", "de\\u200cv"),
    (("dev", ".cairn"), "dev/.ca\u200cirn", "dev/.ca\\u200cirn"),
], ids=["dev", "dev-cairn"])
def test_a_submodule_entry_that_is_the_same_folder_by_identity_is_found(
        tmp_path, monkeypatch, folder, entry, shown):
    """A gitlink named so that a name fold cannot equate it with `dev` (one part)
    or `dev/.cairn` (two parts), but whose folder the disk says is that one."""
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    real_lstat = os.lstat
    held = real_lstat(root.joinpath(*folder))

    def lstat(path, *args, **kwargs):
        if Path(path) == root / entry:
            return held
        return real_lstat(path, *args, **kwargs)

    _stub_listing(monkeypatch, f"160000 {entry}")
    monkeypatch.setattr(lifecycle.os, "lstat", lstat)
    reason = lifecycle._binding_untrusted(root, cfg)
    assert reason is not None and reason.startswith(lifecycle._BINDING_IN_SUBMODULE)
    assert f"git tracks it as {shown}" in reason


def test_a_tracked_entry_deeper_than_three_parts_is_not_taken_for_the_binding_by_identity(
        tmp_path, monkeypatch):
    """Only an entry of exactly three parts can be a name of the binding's own
    folder; a hard link further down is another file that happens to share the
    bytes, and it cannot carry a checkout into the binding."""
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    deeper = cfg.parent / "sub" / "alias.json"
    deeper.parent.mkdir()
    os.link(cfg, deeper)
    _stub_listing(monkeypatch, "100644 dev/.cairn/sub/alias.json")
    assert lifecycle._binding_untrusted(root, cfg) is None


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
    assert reason is not None and reason.startswith(TRACKED_OPENING)
    assert "git tracks it as DEV/.Cairn/Local-Env.JSON" in reason
    assert "git rm DEV/.Cairn/Local-Env.JSON" in reason
    assert "git rm dev/.cairn/local-env.json" not in reason


def test_a_submodule_named_in_another_letter_case_is_named_in_the_reason(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    _stub_listing(monkeypatch, "160000 DEV")
    reason = lifecycle._binding_untrusted(root, cfg)
    assert reason is not None and reason.startswith(lifecycle._BINDING_IN_SUBMODULE)
    assert "git tracks it as DEV." in reason


# --- a disk that does not answer ------------------------------------------------


def _fail_once_the_link_check_has_passed(monkeypatch, function: str, target: Path) -> None:
    """Make `os.<function>(target)` raise, but only after `_assert_not_linked` has
    returned, so the failure falls where the binding's own identity is read."""
    checked = []
    real_check = lifecycle._assert_not_linked
    real = getattr(os, function)

    def check(*args, **kwargs):
        real_check(*args, **kwargs)
        checked.append(True)

    def failing(path, *args, **kwargs):
        if checked and Path(path) == target:
            raise PermissionError(13, "Permission denied", str(path))
        return real(path, *args, **kwargs)

    monkeypatch.setattr(lifecycle, "_assert_not_linked", check)
    monkeypatch.setattr(lifecycle.os, function, failing)


@pytest.mark.parametrize("function, parts", [
    ("stat", ("dev", ".cairn", "local-env.json")),
    ("lstat", ("dev",)),
    ("lstat", ("dev", ".cairn")),
], ids=["binding", "dev", "dev-cairn"])
def test_a_disk_that_cannot_be_asked_about_the_binding_is_a_refusal_worded_for_the_disk(
        tmp_path, monkeypatch, function, parts):
    """An unanswered question is not an answer of "no": the binding is not used.
    The words must not blame git, which was never asked."""
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    _stub_listing(monkeypatch)
    _fail_once_the_link_check_has_passed(monkeypatch, function, root.joinpath(*parts))

    reason = lifecycle._binding_untrusted(root, cfg)

    assert reason is not None, "a disk that gave no answer was taken for 'trusted'"
    assert not reason.startswith("could not ask git")
    assert reason == lifecycle._BINDING_DISK_UNANSWERED


def test_the_warning_for_a_disk_that_cannot_be_asked_says_so(tmp_path, monkeypatch, capsys):
    root = _repo(tmp_path)
    program = _executable(root / "env" / "bin" / "python3")
    _bind(root, str(program))
    _stub_listing(monkeypatch)
    _fail_once_the_link_check_has_passed(
        monkeypatch, "stat", root / "dev" / ".cairn" / "local-env.json")

    assert lifecycle._resolve_interpreter(root) == (sys.executable, "fallback-untrusted")
    err = capsys.readouterr().err
    assert "the disk would not answer" in err
    assert "could not ask git" not in err


# --- a disk that reports inode 0 ------------------------------------------------


def _report_inode_zero(monkeypatch) -> None:
    for name in ("stat", "lstat"):
        def zeroed(path, *args, _real=getattr(os, name), **kwargs):
            st = _real(path, *args, **kwargs)
            return os.stat_result((st.st_mode, 0, st.st_dev, st.st_nlink, st.st_uid,
                                   st.st_gid, st.st_size, int(st.st_atime),
                                   int(st.st_mtime), int(st.st_ctime)))
        monkeypatch.setattr(lifecycle.os, name, zeroed)


@pytest.mark.parametrize("record, make", [
    ("100644 a/b/c.txt", "file"),
    ("160000 x", "folder"),
    ("160000 x/y", "folder"),
], ids=["three-part-file", "one-part-gitlink", "two-part-gitlink"])
def test_a_disk_that_reports_inode_zero_gives_no_identity_to_match(tmp_path, monkeypatch, record, make):
    """Where every file has inode 0, an unrelated tracked path would otherwise
    "be" the binding.  Names are then the only test, and these names are not it."""
    root = _repo(tmp_path)
    cfg = _bind(root, "/usr/bin/true")
    entry = record.split(" ", 1)[1]
    if make == "file":
        (root / entry).parent.mkdir(parents=True)
        (root / entry).write_text("x", encoding="utf-8")
    else:
        (root / entry).mkdir(parents=True)
    _stub_listing(monkeypatch, record)
    assert lifecycle._binding_untrusted(root, cfg) is None   # real inodes: unrelated

    _report_inode_zero(monkeypatch)
    assert lifecycle._binding_untrusted(root, cfg) is None


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
