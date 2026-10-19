"""The session kernel does not run an interpreter binding that git tracks.

`dev/.cairn/local-env.json` names the program the kernel runs its sub-tools
with.  It is meant to be written on one machine and never committed.  Nothing
stops a project committing one, though: git checks it out like any other file,
and it can also replace a user's own ignored binding when a branch that tracks
it is checked out.  A checkout is data a reviewer reads as harmless, and a
binding that names `/usr/bin/make` next to a `Makefile` turns the unmodified
kernel into a launcher for the project's own command.

So a binding that git tracks is not trusted: the run goes on with the current
interpreter, says so on stderr, and names the fix.  The same goes for a binding
reached through a link, and for a binding git cannot be asked about.  A
malformed or missing binding behaves exactly as before.

These tests drive the real command (`tools/session.py`, as a subprocess) from a
fresh `git clone` of a repository built to be hostile, and use a stand-in
interpreter that only records that it ran.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_session_binding_untracked.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
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
    spec = importlib.util.spec_from_file_location("cairn_session_binding", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lifecycle = _load()

BINDING = "dev/.cairn/local-env.json"


# --- builders -----------------------------------------------------------------


def _git(cwd: Path, *args: str, env=None) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True, capture_output=True, env=env)


def _git_identity(root: Path) -> None:
    for key, value in (("user.email", "t@example.com"), ("user.name", "T"),
                       ("commit.gpgsign", "false")):
        _git(root, "config", key, value)


def _stand_in(tmp_path: Path) -> tuple:
    """An executable that only records that it ran; returns (program, marker)."""
    outside = tmp_path.resolve() / "outside"
    outside.mkdir(exist_ok=True)
    marker = outside / "RAN"
    program = outside / "fake-python"
    program.write_text(f'#!/bin/sh\nprintf ran >> "{marker}"\nexit 0\n', encoding="utf-8")
    program.chmod(program.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return program, marker


def _binding_text(program) -> str:
    return json.dumps({"interpreter": str(program)})


def _source_repo(tmp_path: Path, name: str = "src") -> Path:
    """A project with the kernel and an (empty) sibling intent tool installed."""
    src = tmp_path.resolve() / name
    (src / "tools").mkdir(parents=True)
    shutil.copy(MODULE_PATH, src / "tools" / "session.py")
    (src / "tools" / "intent.py").write_text("pass\n", encoding="utf-8")
    (src / ".gitignore").write_text(BINDING + "\n", encoding="utf-8")
    _git(src, "init", "-q")
    _git_identity(src)
    return src


def _commit(src: Path, message: str = "project", force=()) -> None:
    """Commit everything; `force` names ignored files that must be committed too."""
    _git(src, "add", "-A")
    for name in force:
        _git(src, "add", "-f", "--", name)
    _git(src, "commit", "-q", "-m", message)


def _write_binding(root: Path, text: str) -> Path:
    path = root / "dev" / ".cairn" / "local-env.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _clone(src: Path, tmp_path: Path, name: str = "clone") -> Path:
    clone = tmp_path.resolve() / name
    subprocess.run(["git", "clone", "-q", str(src), str(clone)], check=True, capture_output=True)
    _git_identity(clone)
    return clone


def _hostile_clone(tmp_path: Path):
    """A clone whose repository *tracks* a binding that names the stand-in."""
    program, marker = _stand_in(tmp_path)
    src = _source_repo(tmp_path)
    _write_binding(src, _binding_text(program))
    _commit(src, force=[BINDING])
    return _clone(src, tmp_path), marker, program


def _run(clone: Path, command: str, *extra, path_dir=None):
    env = {k: v for k, v in os.environ.items() if k not in ("CAIRN_AGENT", "CAIRN_SESSION")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if path_dir is not None:
        env["PATH"] = str(path_dir) + os.pathsep + env.get("PATH", "")
    return subprocess.run(
        [sys.executable, "tools/session.py", command, *extra],
        cwd=str(clone), capture_output=True, text=True, env=env, timeout=120,
    )


@pytest.fixture(autouse=True)
def _fresh_warning_state(monkeypatch):
    """The warnings are printed once per process; each in-process test starts fresh."""
    monkeypatch.setattr(lifecycle, "_UNTRUSTED_WARNED", False, raising=False)
    monkeypatch.setattr(lifecycle, "_STALE_WARNED", False)


# --- the real command, from a hostile clone ------------------------------------


def test_session_start_does_not_run_a_binding_the_repository_tracks(tmp_path):
    clone, marker, _program = _hostile_clone(tmp_path)
    assert (clone / BINDING).is_file()
    done = _run(clone, "session-start")
    assert not marker.exists(), "the tracked binding's program was run"
    assert done.returncode == 0
    assert "tracked by git" in done.stderr
    assert "git rm" in done.stderr  # the fix is named
    assert "(from fallback-untrusted)" in done.stdout


def test_a_plain_session_end_does_not_run_a_binding_the_repository_tracks(tmp_path):
    """The reflection-only goodnight is the path the kernel promises can at worst
    leave a stray reflection file."""
    clone, marker, _program = _hostile_clone(tmp_path)
    done = _run(clone, "session-end")
    assert not marker.exists(), "the tracked binding's program was run"
    assert done.returncode == 0
    assert "tracked by git" in done.stderr


def test_a_binding_written_on_this_machine_is_still_used(tmp_path):
    """The control: the same binding, untracked and ignored, is honoured."""
    program, marker = _stand_in(tmp_path)
    src = _source_repo(tmp_path)
    _commit(src)
    clone = _clone(src, tmp_path)
    _write_binding(clone, _binding_text(program))
    done = _run(clone, "session-start")
    assert marker.exists(), "an untracked binding should have been used"
    assert done.returncode == 0
    assert "(from local-env.json)" in done.stdout
    assert "tracked by git" not in done.stderr


def test_a_branch_that_tracks_a_binding_cannot_replace_the_users_own(tmp_path):
    """Git treats an ignored file as expendable: checking out a branch that tracks
    the binding overwrites the user's own without a word."""
    program, marker = _stand_in(tmp_path)
    own = Path(sys.executable).resolve()
    src = _source_repo(tmp_path)
    _commit(src)
    _git(src, "checkout", "-q", "-b", "tracks-a-binding")
    _write_binding(src, _binding_text(program))
    _commit(src, "a binding nobody should commit", force=[BINDING])
    _git(src, "checkout", "-q", "-")
    clone = _clone(src, tmp_path)

    mine = _write_binding(clone, json.dumps({"interpreter": str(own)}))
    before = _run(clone, "session-start")
    assert "(from local-env.json)" in before.stdout and not marker.exists()

    _git(clone, "checkout", "-q", "tracks-a-binding")
    assert json.loads(mine.read_text(encoding="utf-8"))["interpreter"] == str(program), (
        "the checkout was expected to overwrite the ignored binding")
    after = _run(clone, "session-start")
    assert not marker.exists(), "the overwritten binding's program was run"
    assert "tracked by git" in after.stderr
    assert "(from fallback-untrusted)" in after.stdout


def test_a_binding_git_cannot_be_asked_about_is_not_trusted(tmp_path):
    """When `git ls-files` fails, the kernel cannot tell, so it does not trust."""
    clone, marker, _program = _hostile_clone(tmp_path)
    # an untracked copy of the same binding: only git's answer separates the cases
    _git(clone, "rm", "-q", "--cached", BINDING)
    wrapper_dir = tmp_path.resolve() / "wrapper"
    wrapper_dir.mkdir()
    real_git = shutil.which("git")
    wrapper = wrapper_dir / "git"
    wrapper.write_text(
        '#!/bin/sh\ncase "$1" in\n  ls-files) echo "fatal: simulated failure" >&2; exit 128 ;;\nesac\n'
        f'exec "{real_git}" "$@"\n', encoding="utf-8")
    wrapper.chmod(0o755)
    done = _run(clone, "session-start", path_dir=wrapper_dir)
    assert not marker.exists(), "a binding git could not vouch for was run"
    assert done.returncode == 0
    assert "could not ask git" in done.stderr
    assert "(from fallback-untrusted)" in done.stdout


def test_without_git_the_command_refuses_before_running_anything(tmp_path):
    clone, marker, _program = _hostile_clone(tmp_path)
    no_git = tmp_path.resolve() / "no-git"
    no_git.mkdir()
    env = {"PATH": str(no_git), "PYTHONDONTWRITEBYTECODE": "1"}
    done = subprocess.run([sys.executable, "tools/session.py", "session-start"],
                          cwd=str(clone), capture_output=True, text=True, env=env, timeout=120)
    assert done.returncode == 1 and "git was not found" in done.stderr
    assert not marker.exists()


def test_a_binding_reached_through_a_link_is_not_trusted(tmp_path):
    """Git lists nothing beyond a link, so a tracked folder behind a tracked link
    would otherwise look untracked."""
    program, marker = _stand_in(tmp_path)
    src = _source_repo(tmp_path)
    (src / "payload").mkdir()
    (src / "payload" / "local-env.json").write_text(_binding_text(program), encoding="utf-8")
    (src / "dev").mkdir()
    os.symlink("../payload", src / "dev" / ".cairn")
    _commit(src)
    clone = _clone(src, tmp_path)
    assert (clone / BINDING).is_file() and (clone / "dev" / ".cairn").is_symlink()
    done = _run(clone, "session-start")
    assert not marker.exists(), "a binding behind a link was run"
    assert "link" in done.stderr
    assert "(from fallback-untrusted)" in done.stdout


def test_a_binding_tracked_under_another_letter_case_is_not_trusted(tmp_path):
    """On a volume that ignores case the same file has several spellings in git."""
    probe = tmp_path.resolve() / "CaseProbe"
    probe.write_text("x", encoding="utf-8")
    if not (tmp_path.resolve() / "caseprobe").exists():
        pytest.skip("this volume is case-sensitive")
    program, marker = _stand_in(tmp_path)
    src = _source_repo(tmp_path)
    shifted = src / "DEV" / ".CAIRN"
    shifted.mkdir(parents=True)
    (shifted / "Local-Env.json").write_text(_binding_text(program), encoding="utf-8")
    _commit(src, force=["DEV/.CAIRN/Local-Env.json"])
    clone = _clone(src, tmp_path)
    done = _run(clone, "session-start")
    assert not marker.exists(), "a binding tracked under another spelling was run"
    assert "tracked by git" in done.stderr


# --- the resolver on its own ---------------------------------------------------


def _clone_with_untracked_binding(tmp_path: Path, monkeypatch=None):
    program, marker = _stand_in(tmp_path)
    src = _source_repo(tmp_path)
    _commit(src)
    clone = _clone(src, tmp_path)
    _write_binding(clone, _binding_text(program))
    return clone, program


def test_an_untracked_binding_resolves_and_a_tracked_one_falls_back(tmp_path, capsys):
    clone, program = _clone_with_untracked_binding(tmp_path)
    assert lifecycle._resolve_interpreter(clone) == (str(program), "local-env.json")
    _git(clone, "add", "-f", BINDING)
    interpreter, source = lifecycle._resolve_interpreter(clone)
    assert (interpreter, source) == (sys.executable, "fallback-untrusted")
    assert "tracked by git" in capsys.readouterr().err
    _git(clone, "rm", "-q", "--cached", BINDING)
    assert lifecycle._resolve_interpreter(clone) == (str(program), "local-env.json")


@pytest.mark.parametrize("failure", ["git-missing", "timeout", "non-zero", "os-error"])
def test_when_git_cannot_answer_the_binding_is_not_trusted(tmp_path, monkeypatch, capsys, failure):
    clone, _program = _clone_with_untracked_binding(tmp_path)
    real_run = lifecycle.subprocess.run

    def broken(argv, *args, **kwargs):
        if argv[:2] == ["git", "ls-files"]:
            if failure == "git-missing":
                raise FileNotFoundError("git")
            if failure == "timeout":
                raise subprocess.TimeoutExpired(argv, 1)
            if failure == "os-error":
                raise PermissionError("denied")
            return subprocess.CompletedProcess(argv, 128, b"", b"fatal: not a git repository")
        return real_run(argv, *args, **kwargs)

    monkeypatch.setattr(lifecycle.subprocess, "run", broken)
    assert lifecycle._resolve_interpreter(clone) == (sys.executable, "fallback-untrusted")
    assert "could not ask git" in capsys.readouterr().err


def test_the_question_put_to_git_is_a_fixed_argument_list_with_no_shell(tmp_path, monkeypatch):
    clone, _program = _clone_with_untracked_binding(tmp_path)
    for name in ("GIT_DIR", "GIT_INDEX_FILE", "GIT_WORK_TREE", "GIT_CONFIG_COUNT", "git_dir"):
        monkeypatch.setenv(name, "set-by-the-caller")   # none of these may reach git
        # (the lower-case spelling is a different variable on POSIX and the same one
        # on Windows, where names are not case-sensitive; it is stripped either way)
    seen = []
    real_run = lifecycle.subprocess.run

    def spy(argv, *args, **kwargs):
        if isinstance(argv, list) and argv[:2] == ["git", "ls-files"]:
            seen.append((argv, kwargs))
            return real_run(argv, *args, **kwargs)
        return real_run(argv, *args, **kwargs)

    monkeypatch.setattr(lifecycle.subprocess, "run", spy)
    lifecycle._resolve_interpreter(clone)
    assert len(seen) == 1
    argv, kwargs = seen[0]
    assert argv == ["git", "ls-files", "-z", "--cached", "--stage"]
    assert not kwargs.get("shell")
    assert kwargs["cwd"] == str(clone)
    git_variables = {k for k in kwargs["env"] if k.upper().startswith("GIT_")}
    assert git_variables == {"GIT_PAGER", "GIT_TERMINAL_PROMPT"}
    assert kwargs["env"]["GIT_TERMINAL_PROMPT"] == "0" and kwargs["env"]["GIT_PAGER"] == "cat"
    assert kwargs["stdin"] == subprocess.DEVNULL
    assert kwargs.get("timeout")  # it cannot hang the session


def test_the_warning_is_printed_once_per_process(tmp_path, capsys):
    clone, _program = _clone_with_untracked_binding(tmp_path)
    _git(clone, "add", "-f", BINDING)
    lifecycle._resolve_interpreter(clone)
    lifecycle._resolve_interpreter(clone)
    assert capsys.readouterr().err.count("tracked by git") == 1


def test_a_malformed_binding_still_refuses_even_when_tracked(tmp_path):
    """The shape checks run first and are unchanged: a bad binding is an error,
    not a quiet fallback."""
    clone, _program = _clone_with_untracked_binding(tmp_path)
    _write_binding(clone, json.dumps({"interpreter": "python3"}))
    _git(clone, "add", "-f", BINDING)
    with pytest.raises(lifecycle.LifecycleError):
        lifecycle._resolve_interpreter(clone)


def test_a_tracked_binding_to_a_vanished_interpreter_keeps_the_stale_message(tmp_path, capsys):
    """Nothing is run in either case, and the stale-binding message is the older,
    more specific one."""
    clone, _program = _clone_with_untracked_binding(tmp_path)
    _write_binding(clone, json.dumps({"interpreter": "/nonexistent/python3"}))
    _git(clone, "add", "-f", BINDING)
    assert lifecycle._resolve_interpreter(clone) == (sys.executable, "fallback-stale")
    assert "no longer exists" in capsys.readouterr().err


# --- the resolver, variant by variant ------------------------------------------------
#
# Each test builds a small repository with real git commands and asks the resolver
# itself -- it never runs anything the binding names.  The answer must be the
# untrusted fallback: the current interpreter, and no path from the binding.


def _plain_repo(tmp_path: Path, name: str) -> Path:
    root = tmp_path.resolve() / name
    root.mkdir(parents=True)
    _git(root, "init", "-q")
    _git_identity(root)
    (root / "f.txt").write_text("x", encoding="utf-8")
    return root


def _binding_at(root: Path, relative: str, program) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_binding_text(program), encoding="utf-8")
    return path


def _commit_paths(root: Path, *paths: str, message: str = "project") -> None:
    _git(root, "add", "-f", "--", *paths)
    _git(root, "commit", "-q", "-m", message)


def _assert_untrusted(root: Path, program, capsys=None) -> None:
    interpreter, source = lifecycle._resolve_interpreter(root)
    assert source == "fallback-untrusted", source
    assert interpreter == sys.executable and str(program) not in interpreter


def _assert_trusted(root: Path, program) -> None:
    assert lifecycle._resolve_interpreter(root) == (str(program), "local-env.json")


def test_the_binding_committed_under_another_letter_case_is_tracked(tmp_path):
    probe = tmp_path.resolve() / "CaseProbe"
    probe.write_text("x", encoding="utf-8")
    if not (tmp_path.resolve() / "caseprobe").exists():
        pytest.skip("this volume is case-sensitive")
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "case")
    _binding_at(root, "DEV/.CAIRN/Local-Env.json", program)
    _commit_paths(root, "f.txt", "DEV/.CAIRN/Local-Env.json")
    assert (root / BINDING).is_file()
    _assert_untrusted(root, program)


def test_the_binding_committed_under_a_spelling_the_volume_treats_as_the_same_name_is_tracked(tmp_path):
    """U+017F (long s) is a different character to git and the same letter to a
    volume that folds Unicode case.  The intended rule: any spelling the volume
    resolves to the binding counts as tracked; one it does not resolve to is a
    different file and is not the binding at all."""
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "lookalike")
    spelled = "dev/.cairn/local-env.jſon"
    _binding_at(root, spelled, program)
    _commit_paths(root, "f.txt", spelled)
    if (root / BINDING).is_file():          # this volume folds the character
        _assert_untrusted(root, program)
    else:                                   # it does not: no binding exists here
        assert lifecycle._resolve_interpreter(root) == (sys.executable, "fallback")


def test_a_compatibility_look_alike_is_a_different_file_and_not_second_guessed(tmp_path):
    """A full-width letter is not the same name on any volume, so an untracked
    binding of the right name next to it is still the user's own."""
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "fullwidth")
    decoy = "dev/.cairn/local-env.ｊson"      # full-width j
    _binding_at(root, decoy, program)
    _commit_paths(root, "f.txt", decoy)
    _binding_at(root, BINDING, program)           # the user's own, untracked
    assert (root / BINDING).read_text(encoding="utf-8") == _binding_text(program)
    _assert_trusted(root, program)


def test_a_binding_under_a_linked_folder_is_untrusted(tmp_path):
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "linked")
    _binding_at(root, "payload/local-env.json", program)
    (root / "dev").mkdir()
    os.symlink("../payload", root / "dev" / ".cairn")
    _commit_paths(root, "f.txt", "payload/local-env.json", "dev/.cairn")
    assert (root / BINDING).is_file()
    _assert_untrusted(root, program)


@pytest.mark.parametrize("flag", ["--assume-unchanged", "--skip-worktree"])
def test_a_tracked_binding_still_counts_as_tracked_when_git_is_told_to_ignore_changes(tmp_path, flag):
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "flagged")
    _binding_at(root, BINDING, program)
    _commit_paths(root, "f.txt", BINDING)
    _git(root, "update-index", flag, BINDING)
    _assert_untrusted(root, program)


def test_a_binding_inside_a_submodule_of_the_project_is_untrusted(tmp_path):
    program, _marker = _stand_in(tmp_path)
    inner = _plain_repo(tmp_path, "inner")
    _binding_at(inner, ".cairn/local-env.json", program)
    _commit_paths(inner, "f.txt", ".cairn/local-env.json")
    root = _plain_repo(tmp_path, "outer")
    _git(root, "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(inner), "dev")
    _git(root, "commit", "-q", "-m", "a submodule named dev")
    assert (root / BINDING).is_file()
    _assert_untrusted(root, program)


def test_a_tracked_binding_is_found_when_the_project_is_a_linked_worktree(tmp_path):
    program, _marker = _stand_in(tmp_path)
    main = _plain_repo(tmp_path, "main")
    _binding_at(main, BINDING, program)
    _commit_paths(main, "f.txt", BINDING)
    linked = tmp_path.resolve() / "linked-worktree"
    _git(main, "worktree", "add", "-q", "-b", "other", str(linked))
    assert (linked / ".git").is_file()
    _assert_untrusted(linked, program)


def test_an_untracked_binding_is_still_used_in_a_linked_worktree(tmp_path):
    program, _marker = _stand_in(tmp_path)
    main = _plain_repo(tmp_path, "main")
    _commit_paths(main, "f.txt")
    linked = tmp_path.resolve() / "linked-worktree"
    _git(main, "worktree", "add", "-q", "-b", "other", str(linked))
    _binding_at(linked, BINDING, program)
    _assert_trusted(linked, program)


def _submodule_project(tmp_path: Path, tracked: bool):
    program, _marker = _stand_in(tmp_path)
    inner = _plain_repo(tmp_path, "inner")
    if tracked:
        _binding_at(inner, BINDING, program)
        _commit_paths(inner, "f.txt", BINDING)
    else:
        _commit_paths(inner, "f.txt")
    outer = _plain_repo(tmp_path, "outer")
    _git(outer, "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(inner), "proj")
    _git(outer, "commit", "-q", "-m", "the project is a submodule")
    project = outer / "proj"
    assert (project / ".git").is_file()
    if not tracked:
        _binding_at(project, BINDING, program)
    return project, program


def test_a_tracked_binding_is_found_when_the_project_is_itself_a_submodule(tmp_path):
    project, program = _submodule_project(tmp_path, tracked=True)
    _assert_untrusted(project, program)


def test_an_untracked_binding_is_still_used_when_the_project_is_itself_a_submodule(tmp_path):
    project, program = _submodule_project(tmp_path, tracked=False)
    _assert_trusted(project, program)


@pytest.mark.parametrize("variable", ["GIT_DIR", "GIT_DIR+GIT_WORK_TREE", "GIT_INDEX_FILE",
                                      "GIT_LITERAL_PATHSPECS", "GIT_CEILING_DIRECTORIES"])
def test_the_callers_git_environment_cannot_point_the_question_elsewhere(tmp_path, monkeypatch, variable):
    """The question is about the project folder.  A caller's GIT_* variables may
    point git at a different repository or index, or change how paths match; none
    of them reaches the query."""
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "project")
    _binding_at(root, BINDING, program)
    _commit_paths(root, "f.txt", BINDING)
    elsewhere = _plain_repo(tmp_path, "elsewhere")
    _commit_paths(elsewhere, "f.txt")
    empty_index = tmp_path.resolve() / "empty-index"
    for name in variable.split("+"):
        if name == "GIT_DIR":
            monkeypatch.setenv("GIT_DIR", str(elsewhere / ".git"))
        elif name == "GIT_WORK_TREE":
            monkeypatch.setenv("GIT_WORK_TREE", str(elsewhere))
        elif name == "GIT_INDEX_FILE":
            monkeypatch.setenv("GIT_INDEX_FILE", str(empty_index))
        elif name == "GIT_LITERAL_PATHSPECS":
            monkeypatch.setenv("GIT_LITERAL_PATHSPECS", "1")
        else:
            monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(root.parent))
    _assert_untrusted(root, program)


def _stub_git(tmp_path: Path, monkeypatch, body: str) -> None:
    stub_dir = tmp_path.resolve() / "stub-bin"
    stub_dir.mkdir(exist_ok=True)
    stub = stub_dir / "git"
    stub.write_text("#!/bin/sh\n" + body, encoding="utf-8")
    stub.chmod(0o755)
    monkeypatch.setenv("PATH", str(stub_dir) + os.pathsep + os.environ.get("PATH", ""))


@pytest.mark.parametrize(
    "body",
    ["exit 128\n", "echo 'fatal: stub' >&2\nexit 1\n", "exit 0\n", "printf 'nonsense\\0'\nexit 0\n"],
    ids=["exit-128", "exit-1", "silent-success", "output-not-understood"],
)
def test_a_git_that_fails_leaves_the_binding_untrusted(tmp_path, monkeypatch, capsys, body):
    """A non-zero exit is no answer.  (A success that prints nothing is an answer:
    nothing is tracked, so that case is the one that must *not* be refused.)"""
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "project")
    _binding_at(root, BINDING, program)
    _stub_git(tmp_path, monkeypatch, body)
    if body == "exit 0\n":
        _assert_trusted(root, program)
    else:
        _assert_untrusted(root, program)
        assert "could not ask git" in capsys.readouterr().err


def test_a_submodule_whose_name_only_starts_like_the_folder_does_not_count(tmp_path):
    """The submodule rule is about a submodule that *holds* the binding's path, not
    one whose name begins the same way (`de` is not `dev`)."""
    program, _marker = _stand_in(tmp_path)
    inner = _plain_repo(tmp_path, "inner")
    _commit_paths(inner, "f.txt")
    root = _plain_repo(tmp_path, "outer")
    _git(root, "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(inner), "de")
    _git(root, "commit", "-q", "-m", "a submodule named de")
    _binding_at(root, BINDING, program)
    _assert_trusted(root, program)


def test_a_tracked_file_named_like_the_folder_is_not_taken_for_a_submodule(tmp_path):
    """Only a submodule entry (mode 160000) makes the files below it another
    repository's.  A plain entry called `dev` is not one."""
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "project")
    _commit_paths(root, "f.txt")
    blob = subprocess.run(["git", "hash-object", "-w", "f.txt"], cwd=str(root), check=True,
                          capture_output=True, text=True).stdout.strip()
    _git(root, "update-index", "--add", "--cacheinfo", f"100644,{blob},dev")
    _binding_at(root, BINDING, program)
    _assert_trusted(root, program)


def test_a_git_that_hangs_leaves_the_binding_untrusted(tmp_path, monkeypatch, capsys):
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "project")
    _binding_at(root, BINDING, program)
    _stub_git(tmp_path, monkeypatch, "exec sleep 60\n")
    monkeypatch.setattr(lifecycle, "_BINDING_GIT_TIMEOUT_SECONDS", 1)
    _assert_untrusted(root, program)
    assert "could not ask git" in capsys.readouterr().err


# --- binding text reaches the screen only encoded -----------------------------------

#: A C1 control (8-bit CSI) and a right-to-left override.  The earlier check
#: rejects only C0 controls and DEL, so both get past it.
_NASTY = "\u009b‮"


def _assert_inert(text: str) -> None:
    assert "\u009b" not in text and "‮" not in text
    assert "\\x9b" in text and "\\u202e" in text


def _bound_project(tmp_path: Path, value: str, name: str = "project") -> Path:
    root = _plain_repo(tmp_path, name)
    _commit_paths(root, "f.txt")
    _write_binding(root, json.dumps({"interpreter": value}))
    return root


def test_a_vanished_interpreter_is_named_only_in_encoded_form(tmp_path, capsys):
    root = _bound_project(tmp_path, "/nonexistent/" + _NASTY + "/python")
    assert lifecycle._resolve_interpreter(root) == (sys.executable, "fallback-stale")
    _assert_inert(capsys.readouterr().err)


def test_a_parent_traversal_refusal_names_the_path_only_in_encoded_form(tmp_path):
    root = _bound_project(tmp_path, "/tmp/" + _NASTY + "/../python")
    with pytest.raises(lifecycle.LifecycleError, match="parent-traversal") as caught:
        lifecycle._resolve_interpreter(root)
    _assert_inert(str(caught.value))


def test_a_not_executable_refusal_names_the_path_only_in_encoded_form(tmp_path):
    plain = tmp_path.resolve() / ("not-" + _NASTY + "-executable")
    plain.write_text("x", encoding="utf-8")
    plain.chmod(0o644)
    root = _bound_project(tmp_path, str(plain))
    with pytest.raises(lifecycle.LifecycleError, match="not an executable file") as caught:
        lifecycle._resolve_interpreter(root)
    _assert_inert(str(caught.value))


def test_a_could_not_inspect_refusal_names_the_path_only_in_encoded_form(tmp_path):
    root = _bound_project(tmp_path, "/tmp/" + "a" * 300 + _NASTY + "/python")
    with pytest.raises(lifecycle.LifecycleError, match="could not be inspected") as caught:
        lifecycle._resolve_interpreter(root)
    _assert_inert(str(caught.value))


@pytest.mark.parametrize("text", ["{", "[]"], ids=["not-json", "not-an-object"])
def test_a_refusal_names_the_binding_file_only_in_encoded_form(tmp_path, text):
    """The folder the project sits in can be named by someone else (a clone's
    default folder name), so the binding file's path is printed encoded too."""
    root = _plain_repo(tmp_path, "p" + _NASTY)
    _commit_paths(root, "f.txt")
    _write_binding(root, text)
    with pytest.raises(lifecycle.LifecycleError) as caught:
        lifecycle._resolve_interpreter(root)
    _assert_inert(str(caught.value))


def test_the_optional_tool_fallback_repeats_a_refusal_only_in_encoded_form(tmp_path, monkeypatch, capsys):
    """`_intent_whoami` prints the resolver's refusal as a warning and goes on."""
    root = _bound_project(tmp_path, "/tmp/" + _NASTY + "/../python")
    quiet = tmp_path.resolve() / "quiet-tool.py"
    quiet.write_text("print('claude-00000000')\n", encoding="utf-8")
    monkeypatch.setattr(lifecycle, "_sibling_tool", lambda name: quiet)
    assert lifecycle._intent_whoami(root) == "claude-00000000"
    _assert_inert(capsys.readouterr().err)


def test_session_start_prints_the_resolved_interpreter_only_in_encoded_form(tmp_path, monkeypatch, capsys):
    """A valid binding whose program has an unusual name: the line that reports it
    is printed after every check has passed, and still goes through the encoder."""
    named = tmp_path.resolve() / ("py" + _NASTY)
    named.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    named.chmod(0o755)
    src = _source_repo(tmp_path)
    _commit(src)
    clone = _clone(src, tmp_path)
    _write_binding(clone, json.dumps({"interpreter": str(named)}))
    monkeypatch.chdir(clone)
    assert lifecycle.main(["session-start"]) == 0
    out = capsys.readouterr().out
    assert "(from local-env.json)" in out
    interpreter_line = next(line for line in out.splitlines() if "interpreter:" in line)
    _assert_inert(interpreter_line)
