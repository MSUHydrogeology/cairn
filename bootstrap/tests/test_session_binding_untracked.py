"""The session kernel resolves its interpreter from per-worktree Git administration.

The tests distinguish the new authority from the legacy checkout file, which
is never read or migrated. They retain real session-start/session-end launches,
schema and encoding checks, and executable-selection controls. Path-link and
Git-layout cases live in
``bootstrap/tests/security/test_git_interpreter_binding_portable.py``.

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
from types import ModuleType, SimpleNamespace

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


def _git(cwd: Path, *args: str, env=None) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=str(cwd), check=True, capture_output=True,
        text=True, env=env,
    )
    return proc.stdout.strip()


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
    shutil.copy(MODULE_PATH.with_name("git_read.py"), src / "tools" / "git_read.py")
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
    path = Path(_git(root, "rev-parse", "--absolute-git-dir")) / "cairn" / "local-env.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _write_legacy_binding(root: Path, text: str) -> Path:
    path = root / BINDING
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
    _write_legacy_binding(src, _binding_text(program))
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
    monkeypatch.setattr(lifecycle, "_MISSING_BINDING_WARNED", False, raising=False)
    monkeypatch.setattr(lifecycle, "_STALE_WARNED", False)


# --- the real command, from a hostile clone ------------------------------------


def test_session_start_ignores_a_legacy_binding_in_checkout_content(tmp_path):
    clone, marker, _program = _hostile_clone(tmp_path)
    assert (clone / BINDING).is_file()
    done = _run(clone, "session-start")
    assert not marker.exists(), "the legacy checkout binding's program was run"
    assert done.returncode == 0
    assert "no per-worktree Git interpreter binding" in done.stderr
    assert "(from fallback)" in done.stdout


def test_a_plain_session_end_ignores_a_legacy_binding_in_checkout_content(tmp_path):
    """The reflection-only goodnight is the path the kernel promises can at worst
    leave a stray reflection file."""
    clone, marker, _program = _hostile_clone(tmp_path)
    done = _run(clone, "session-end")
    assert not marker.exists(), "the legacy checkout binding's program was run"
    assert done.returncode == 0
    assert "no per-worktree Git interpreter binding" in done.stderr


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


def test_a_branch_with_a_legacy_binding_cannot_replace_git_admin_choice(tmp_path):
    """A checkout can replace legacy content without changing Git administration."""
    program, marker = _stand_in(tmp_path)
    own = Path(sys.executable).resolve()
    src = _source_repo(tmp_path)
    _commit(src)
    _git(src, "checkout", "-q", "-b", "tracks-a-binding")
    _write_legacy_binding(src, _binding_text(program))
    _commit(src, "a binding nobody should commit", force=[BINDING])
    _git(src, "checkout", "-q", "-")
    clone = _clone(src, tmp_path)

    mine = _write_binding(clone, json.dumps({"interpreter": str(own)}))
    before = _run(clone, "session-start")
    assert "(from local-env.json)" in before.stdout and not marker.exists()

    _git(clone, "checkout", "-q", "tracks-a-binding")
    assert json.loads(mine.read_text(encoding="utf-8"))["interpreter"] == str(own), (
        "the project checkout changed the per-worktree Git binding")
    after = _run(clone, "session-start")
    assert not marker.exists(), "the overwritten binding's program was run"
    assert "tracked by git" not in after.stderr
    assert "(from local-env.json)" in after.stdout


def test_a_binding_git_cannot_be_asked_about_is_not_trusted(tmp_path):
    """When Git cannot verify the in-project executable, resolution refuses."""
    marker_program, marker = _stand_in(tmp_path)
    src = _source_repo(tmp_path)
    _commit(src)
    clone = _clone(src, tmp_path)
    _write_binding(clone, _binding_text(marker_program))
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
    assert done.returncode == 1
    assert "could not verify whether the project tracks" in done.stderr


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
    """A linked per-worktree binding folder refuses before a named tool runs."""
    program, marker = _stand_in(tmp_path)
    src = _source_repo(tmp_path)
    _commit(src)
    clone = _clone(src, tmp_path)
    git_dir = Path(_git(clone, "rev-parse", "--absolute-git-dir"))
    payload = tmp_path / "payload"
    payload.mkdir()
    (payload / "local-env.json").write_text(_binding_text(program), encoding="utf-8")
    (git_dir / "cairn").symlink_to(payload, target_is_directory=True)
    done = _run(clone, "session-start")
    assert not marker.exists(), "a binding behind a link was run"
    assert done.returncode == 1
    assert "link or reparse point" in done.stderr


def test_legacy_binding_spelling_never_controls_interpreter_selection(tmp_path):
    """Legacy path case-folding is irrelevant because that path is never read."""
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
    assert "no per-worktree Git interpreter binding" in done.stderr
    assert "(from fallback)" in done.stdout


# --- the resolver on its own ---------------------------------------------------


def _clone_with_untracked_binding(tmp_path: Path, monkeypatch=None):
    program, marker = _stand_in(tmp_path)
    src = _source_repo(tmp_path)
    _commit(src)
    clone = _clone(src, tmp_path)
    _write_binding(clone, _binding_text(program))
    return clone, program


def test_a_tracked_legacy_file_does_not_replace_the_git_admin_binding(tmp_path, capsys):
    clone, program = _clone_with_untracked_binding(tmp_path)
    assert lifecycle._resolve_interpreter(clone) == (str(program), "local-env.json")
    _write_legacy_binding(clone, _binding_text(_stand_in(tmp_path)[0]))
    _git(clone, "add", "-f", BINDING)
    interpreter, source = lifecycle._resolve_interpreter(clone)
    assert (interpreter, source) == (str(program), "local-env.json")
    assert "tracked by git" not in capsys.readouterr().err
    _git(clone, "rm", "-q", "--cached", BINDING)
    assert lifecycle._resolve_interpreter(clone) == (str(program), "local-env.json")


@pytest.mark.parametrize("failure", ["git-missing", "timeout", "non-zero", "os-error"])
def test_when_git_cannot_answer_the_binding_is_not_trusted(tmp_path, monkeypatch, capsys, failure):
    clone, _program = _clone_with_untracked_binding(tmp_path)
    real_reader = lifecycle._load_git_read_helper()

    class BrokenReader:
        def __getattr__(self, name):
            return getattr(real_reader, name)

        def run_git(self, target, args, **kwargs):
            if args[0] == "ls-files":
                state = "absent" if failure == "git-missing" else "failed"
                return SimpleNamespace(state=state, returncode=128, stdout=b"")
            return real_reader.run_git(target, args, **kwargs)

    monkeypatch.setattr(lifecycle, "_load_git_read_helper", lambda: BrokenReader())
    with pytest.raises(lifecycle.LifecycleError, match="could not verify"):
        lifecycle._resolve_interpreter(clone)
    assert "could not ask git" not in capsys.readouterr().err


def test_the_question_put_to_git_is_a_fixed_argument_list_with_no_shell(tmp_path, monkeypatch):
    clone, _program = _clone_with_untracked_binding(tmp_path)
    for name in ("GIT_DIR", "GIT_INDEX_FILE", "GIT_WORK_TREE", "GIT_CONFIG_COUNT", "git_dir"):
        monkeypatch.setenv(name, "set-by-the-caller")   # none of these may reach git
        # (the lower-case spelling is a different variable on POSIX and the same one
        # on Windows, where names are not case-sensitive; it is stripped either way)
    seen = []
    real_reader = lifecycle._load_git_read_helper()

    class SpyReader:
        def __getattr__(self, name):
            return getattr(real_reader, name)

        def run_git(self, target, args, **kwargs):
            if args[0] == "ls-files":
                seen.append((target, args, kwargs))
            return real_reader.run_git(target, args, **kwargs)

    monkeypatch.setattr(lifecycle, "_load_git_read_helper", lambda: SpyReader())
    lifecycle._resolve_interpreter(clone)
    assert len(seen) == 1
    target, args, kwargs = seen[0]
    assert target == str(clone)
    assert args == ("ls-files", "-z", "--cached", "--stage")
    assert kwargs["timeout"] == lifecycle._BINDING_GIT_TIMEOUT_SECONDS
    assert kwargs["output_limit"] == 64 * 1024 * 1024


def test_the_missing_binding_warning_is_printed_once_per_process(tmp_path, capsys):
    clone = _plain_repo(tmp_path, "missing")
    assert lifecycle._resolve_interpreter(clone) == (sys.executable, "fallback")
    assert lifecycle._resolve_interpreter(clone) == (sys.executable, "fallback")
    assert capsys.readouterr().err.count("no per-worktree Git interpreter binding") == 1


def test_a_malformed_binding_still_refuses(tmp_path):
    """The shape checks remain strict for a binding in Git administration."""
    clone, _program = _clone_with_untracked_binding(tmp_path)
    _write_binding(clone, json.dumps({"interpreter": "python3"}))
    with pytest.raises(lifecycle.LifecycleError):
        lifecycle._resolve_interpreter(clone)


def test_a_vanished_interpreter_keeps_the_stale_message(tmp_path, capsys):
    """Nothing is run in either case, and the stale-binding message is the older,
    more specific one."""
    clone, _program = _clone_with_untracked_binding(tmp_path)
    _write_binding(clone, json.dumps({"interpreter": "/nonexistent/python3"}))
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
    """Write the current per-worktree binding; *relative* is legacy call syntax."""
    path = lifecycle._git_binding_path(root)
    assert path is not None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_binding_text(program), encoding="utf-8")
    return path


def _commit_paths(root: Path, *paths: str, message: str = "project") -> None:
    _git(root, "add", "-f", "--", *paths)
    _git(root, "commit", "-q", "-m", message)


def _assert_trusted(root: Path, program) -> None:
    assert lifecycle._resolve_interpreter(root) == (str(program), "local-env.json")


@pytest.mark.parametrize("variable", ["GIT_DIR", "GIT_DIR+GIT_WORK_TREE", "GIT_INDEX_FILE",
                                      "GIT_LITERAL_PATHSPECS", "GIT_CEILING_DIRECTORIES"])
def test_the_callers_git_environment_cannot_redirect_binding_discovery(tmp_path, monkeypatch, variable):
    """Both root discovery and index checks ignore caller Git overrides."""
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "project")
    _binding_at(root, BINDING, program)
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
    _assert_trusted(root, program)


@pytest.mark.parametrize("failure", ["non-zero", "timeout", "os-error"])
def test_git_cannot_verify_a_selected_interpreter_so_resolution_refuses(tmp_path, monkeypatch, failure):
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "project")
    _binding_at(root, BINDING, program)
    real_reader = lifecycle._load_git_read_helper()

    class BrokenReader:
        def __getattr__(self, name):
            return getattr(real_reader, name)

        def run_git(self, target, args, **kwargs):
            if args[0] == "ls-files":
                if failure == "timeout":
                    return SimpleNamespace(state="failed", returncode=None, stdout=b"")
                if failure == "os-error":
                    return SimpleNamespace(state="failed", returncode=None, stdout=b"")
                return SimpleNamespace(state="failed", returncode=128, stdout=b"")
            return real_reader.run_git(target, args, **kwargs)

    monkeypatch.setattr(lifecycle, "_load_git_read_helper", lambda: BrokenReader())
    with pytest.raises(lifecycle.LifecycleError, match="could not verify"):
        lifecycle._resolve_interpreter(root)


@pytest.mark.parametrize("body", ["exit 128\n", "echo 'fatal: stub' >&2\nexit 1\n",
                                  "exit 0\n", "printf 'nonsense\\0'\nexit 0\n"],
                         ids=["exit-128", "exit-1", "silent-success", "bad-output"])
def test_git_index_answer_is_parsed_or_refused(tmp_path, monkeypatch, body):
    """Malformed or failed index answers refuse; a valid empty answer permits use."""
    program, _marker = _stand_in(tmp_path)
    root = _plain_repo(tmp_path, "project")
    _binding_at(root, BINDING, program)
    real_reader = lifecycle._load_git_read_helper()

    class BrokenReader:
        def __getattr__(self, name):
            return getattr(real_reader, name)

        def run_git(self, target, args, **kwargs):
            if args[0] == "ls-files":
                if body == "exit 0\n":
                    return SimpleNamespace(state="completed", returncode=0, stdout=b"")
                if body.startswith("printf"):
                    return SimpleNamespace(state="completed", returncode=0,
                                           stdout=b"nonsense\0")
                return SimpleNamespace(state="failed", returncode=128, stdout=b"")
            return real_reader.run_git(target, args, **kwargs)

    monkeypatch.setattr(lifecycle, "_load_git_read_helper", lambda: BrokenReader())
    if body == "exit 0\n":
        _assert_trusted(root, program)
    else:
        with pytest.raises(lifecycle.LifecycleError, match="could not verify"):
            lifecycle._resolve_interpreter(root)


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
