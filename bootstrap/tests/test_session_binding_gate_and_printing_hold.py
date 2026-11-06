"""Interpreter tracking, binding validation, and terminal output boundaries.

The binding is in per-worktree Git administration, while the executable it
names can still be tracked project content. This file checks that tracked
executables are refused, malformed administrative state never produces a
traceback, and project-controlled text is encoded before it reaches a terminal.

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
    monkeypatch.setattr(lifecycle, "_MISSING_BINDING_WARNED", False, raising=False)
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
    if not (root / ".git").exists():
        _git(root, "init", "-q", "-b", "main")
        _git(root, "config", "user.email", "t@example.com")
        _git(root, "config", "user.name", "T")
    cfg = lifecycle._git_binding_path(root)
    assert cfg is not None
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(json.dumps({"interpreter": interpreter}), encoding="utf-8")
    return cfg


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


def _disk_ignores_letter_case(tmp_path: Path) -> bool:
    probe = tmp_path / "CaseProbe"
    probe.mkdir(exist_ok=True)
    return (tmp_path / "caseprobe").exists()


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


@pytest.mark.parametrize("sibling, tail", [
    ("Proj2", "2"),
    ("PROJ2", "2"),
    ("Proj-other", "-other"),
    ("Proj.d", ".d"),
], ids=["digit", "upper-digit", "hyphen", "dot"])
def test_a_folder_beside_the_project_whose_name_starts_like_it_is_not_inside_the_project(
        tmp_path, monkeypatch, sibling, tail):
    """The project is `Proj`; `Proj2` next to it is another folder, though its path
    begins with the project's.  If the project's path were cut off at its name
    alone, `Proj2/env/bin/python3` would read as `2/env/bin/python3` inside the
    project, and a listing that tracks that name would make the gate refuse a
    program git has no say over.  The project's own program, in the same listing,
    is the control: it shows the listing can match."""
    root = _repo(tmp_path, "Proj")
    cfg = _bind(root, "/usr/bin/true")
    inside = _executable(root / "env" / "bin" / "python3")
    beside = _executable(tmp_path.resolve() / sibling / "env" / "bin" / "python3")
    _stub_listing(monkeypatch, "100755 env/bin/python3", f"100755 {tail}/env/bin/python3")

    assert lifecycle._binding_untrusted(root, cfg, inside) == lifecycle._INTERPRETER_TRACKED
    assert lifecycle._binding_untrusted(root, cfg, beside) is None


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


# The former inode/folded-name cases asked whether project index entries could
# alias ``dev/.cairn/local-env.json``. The binding has moved out of checkout
# content, so that index question no longer governs it. The replacement boundary
# is covered through installer and resolver entry points in
# ``bootstrap/tests/security/test_git_interpreter_binding_portable.py``: regular
# Git pointers are accepted, links and reparse points in administration are
# refused, and the legacy file is
# never read. The interpreter-tracking cases above remain here because the
# executable itself can still be checkout content.


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
        (root / ".git").mkdir()
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


_CHILD_STDOUT = (
    b"alpha\nbeta\\x1b\x1b]8;;https://example.test\x07link\x1b]8;;"
    b"\rbare\r\nlast\xc2\x9b\xe2\x80\xae\xe3\x85\xa4\xe2\x80\x8b"
)
_CHILD_STDERR = b"error\r\nnext\xc2\x9b"


def _child_tool(root: Path, *, returncode: int) -> Path:
    (root / ".git").mkdir()
    tool = root / "tools" / "intent.py"
    tool.parent.mkdir(parents=True, exist_ok=True)
    tool.write_text(
        "import sys\n"
        f"sys.stdout.buffer.write(bytes.fromhex('{_CHILD_STDOUT.hex()}'))\n"
        f"sys.stderr.buffer.write(bytes.fromhex('{_CHILD_STDERR.hex()}'))\n"
        f"raise SystemExit({returncode})\n",
        encoding="utf-8",
    )
    return tool


def _assert_child_display_contract(output: str) -> None:
    assert "alpha\nbeta\\x5cx1b" in output
    assert "\\x1b]8;;https://example.test\\x07link\\x1b]8;;" in output
    assert "\\x0dbare\\x0d\nlast" in output
    assert output.endswith("last\\x9b\\u202e\\u3164\\u200b\n")
    assert "\r" not in output and "\x1b" not in output


@pytest.mark.parametrize("helper", ["prune", "surface", "evolution"])
@pytest.mark.parametrize("returncode", [0, 1])
def test_child_streams_are_framed_and_encoded_through_real_subprocess(
    helper, returncode, tmp_path, monkeypatch, capsys
):
    root = tmp_path.resolve() / "child-project"
    root.mkdir()
    tool = _child_tool(root, returncode=returncode)
    monkeypatch.setattr(lifecycle, "_sibling_tool", lambda name: tool)
    # prune resolves from root first; the two other helpers use the sibling tool.
    if helper == "prune":
        lifecycle._prune_intents(root, sys.executable, 30, dry_run=True)
    elif helper == "surface":
        lifecycle._surface_intents(root, sys.executable)
    else:
        lifecycle._run_evolution_infer(root, sys.executable)
    print("parent-after-child")
    captured = capsys.readouterr()
    assert captured.out.endswith("parent-after-child\n")
    child_out, parent = captured.out.rsplit("parent-after-child\n", 1)
    assert parent == ""
    assert child_out.endswith("last\\x9b\\u202e\\u3164\\u200b\n")
    if helper != "evolution":
        assert child_out.startswith("\n")  # the helper's section heading precedes its stream
    _assert_child_display_contract(child_out)
    assert ("error\\x0d\nnext\\x9b" in captured.err) is (returncode != 0)
    assert "\\x9b" not in captured.err if returncode == 0 else True


@pytest.mark.parametrize("helper", ["prune", "surface", "evolution"])
def test_raw_child_write_mutant_is_caught_by_real_child_contract(
    helper, tmp_path, monkeypatch, capsys
):
    root = tmp_path.resolve() / "mutant-project"
    root.mkdir()
    tool = _child_tool(root, returncode=0)
    monkeypatch.setattr(lifecycle, "_sibling_tool", lambda name: tool)
    monkeypatch.setattr(lifecycle, "_encode_child_output", lambda value, **kwargs: value)
    if helper == "prune":
        lifecycle._prune_intents(root, sys.executable, 30, dry_run=True)
    elif helper == "surface":
        lifecycle._surface_intents(root, sys.executable)
    else:
        lifecycle._run_evolution_infer(root, sys.executable)
    output = capsys.readouterr().out
    assert "alpha\nbeta" in output
    with pytest.raises(AssertionError):
        _assert_child_display_contract(output)


@pytest.mark.parametrize("helper", ["prune", "surface", "evolution"])
def test_malformed_child_bytes_keep_strict_decode_failure(
    helper, tmp_path, monkeypatch
):
    root = tmp_path.resolve() / "malformed-project"
    root.mkdir()
    if helper == "prune":
        (root / ".git").mkdir()
    tool = root / "tools" / "intent.py"
    tool.parent.mkdir()
    tool.write_text("import sys\nsys.stdout.buffer.write(b'\\xff')\n", encoding="utf-8")
    monkeypatch.setattr(lifecycle, "_sibling_tool", lambda name: tool)
    with pytest.raises(UnicodeDecodeError):
        if helper == "prune":
            lifecycle._prune_intents(root, sys.executable, 30, dry_run=True)
        elif helper == "surface":
            lifecycle._surface_intents(root, sys.executable)
        else:
            lifecycle._run_evolution_infer(root, sys.executable)


@pytest.mark.parametrize("helper", ["prune", "surface", "evolution"])
def test_successful_child_stderr_is_decoded_strictly(helper, tmp_path, monkeypatch):
    root = tmp_path.resolve()
    if helper == "prune":
        (root / ".git").mkdir()
    tool = root / "tools" / "intent.py"
    tool.parent.mkdir()
    tool.write_text("import sys\nsys.stderr.buffer.write(b'\\xff')\n", encoding="utf-8")
    monkeypatch.setattr(lifecycle, "_sibling_tool", lambda name: tool)
    with pytest.raises(UnicodeDecodeError):
        if helper == "prune":
            lifecycle._prune_intents(root, sys.executable, 30, dry_run=True)
        elif helper == "surface":
            lifecycle._surface_intents(root, sys.executable)
        else:
            lifecycle._run_evolution_infer(root, sys.executable)


@pytest.mark.parametrize("helper", ["prune", "surface", "evolution"])
def test_child_decoding_respects_utf8_mode(helper, tmp_path):
    root = tmp_path.resolve()
    if helper == "prune":
        (root / ".git").mkdir()
    tool = root / "tools" / "intent.py"
    tool.parent.mkdir()
    tool.write_text("import sys\nsys.stdout.buffer.write(bytes.fromhex('c3a9'))\n", encoding="utf-8")
    script = (
        "import sys; from pathlib import Path; "
        f"sys.path.insert(0, {str(Path(lifecycle.__file__).parent)!r}); "
        "import session as s; "
        f"root=Path({str(root)!r}); tool=Path({str(tool)!r}); "
        "s._sibling_tool=lambda name: tool; "
        f"helper={helper!r}; "
        "s._prune_intents(root, sys.executable, 30, dry_run=True) if helper == 'prune' "
        "else s._surface_intents(root, sys.executable) if helper == 'surface' "
        "else s._run_evolution_infer(root, sys.executable)"
    )
    env = dict(os.environ, LC_ALL="C", PYTHONUTF8="1")
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, env=env)
    assert result.returncode == 0, result.stderr
    assert "é" in result.stdout.decode("utf-8")
