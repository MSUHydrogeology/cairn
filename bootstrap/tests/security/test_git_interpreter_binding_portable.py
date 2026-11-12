"""Portable checks for the per-worktree interpreter binding boundary.

Promises:
- Installing into a git worktree writes the interpreter binding only under that worktree's own git administration.
- Linked worktrees and separate git directories each get a distinct binding.
- Non-repository and nested targets install without a binding.
- A hostile git environment or legacy checkout file does not steer the binding.
- A symlinked .git, binding path or unreadable binding state refuses rather than being followed.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from bootstrap._scaffold import install
from bootstrap._scaffold.cli import main as scaffold_main


SESSION_PATH = Path(__file__).resolve().parents[3] / "tools" / "session.py"
SHIPPED_SESSION_PATH = Path(__file__).resolve().parents[3] / "templates" / "skills" / "_lib" / "session.py"


def _git(root: Path, *args: str, env=None) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=root, env=env, check=True,
        capture_output=True, text=True,
    )
    return proc.stdout.strip()


def _repo(root: Path) -> Path:
    root.mkdir(parents=True)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "user.name", "Test")
    return root


def _session_module(path: Path = SESSION_PATH):
    spec = importlib.util.spec_from_file_location("cairn_binding_session", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _admin_binding(root: Path) -> Path:
    git_dir = Path(_git(root, "rev-parse", "--absolute-git-dir"))
    return git_dir / "cairn" / "local-env.json"


def test_installer_writes_only_under_exact_worktree_git_admin(tmp_path):
    root = _repo(tmp_path / "project")
    result = install.write_local_env(root)
    binding = _admin_binding(root)

    assert result[3] == "installed"
    assert result[0] == binding
    assert json.loads(binding.read_text(encoding="utf-8")) == {
        "interpreter": str(Path(sys.executable).resolve())
    }
    assert not (root / "dev" / ".cairn" / "local-env.json").exists()


def test_linked_worktrees_get_distinct_bindings(tmp_path):
    main = _repo(tmp_path / "main")
    (main / "tracked.txt").write_text("x\n", encoding="utf-8")
    _git(main, "add", "tracked.txt")
    _git(main, "commit", "-m", "initial")
    linked = tmp_path / "linked"
    _git(main, "worktree", "add", "-q", "-b", "linked", str(linked))

    first = install.write_local_env(main)
    second = install.write_local_env(linked)

    assert first[3] == second[3] == "installed"
    assert first[0] == _admin_binding(main)
    assert second[0] == _admin_binding(linked)
    assert first[0] != second[0]
    assert (linked / ".git").is_file()  # regular Git pointer is supported


def test_separate_git_directory_and_submodule_install(tmp_path):
    separated = tmp_path / "separated"
    admin = tmp_path / "separated-admin"
    separated.mkdir()
    subprocess.run(
        ["git", "init", "--separate-git-dir", str(admin), str(separated)],
        check=True, capture_output=True,
    )
    assert (separated / ".git").is_file()
    assert install.write_local_env(separated)[0] == _admin_binding(separated)

    child = _repo(tmp_path / "child")
    (child / "tracked.txt").write_text("child\n", encoding="utf-8")
    _git(child, "add", "tracked.txt")
    _git(child, "commit", "-m", "child")
    parent = _repo(tmp_path / "parent")
    _git(parent, "-c", "protocol.file.allow=always", "submodule", "add", "-q",
         str(child), "nested")
    submodule = parent / "nested"

    assert install.write_local_env(submodule)[0] == _admin_binding(submodule)


def test_nonrepository_and_nested_targets_install_without_binding(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    assert install.write_local_env(outside)[3] == "skipped-no-worktree"

    parent = _repo(tmp_path / "parent")
    nested = parent / "nested"
    nested.mkdir()
    assert install.write_local_env(nested)[3] == "skipped-not-root"


@pytest.mark.parametrize("session_path", [SESSION_PATH, SHIPPED_SESSION_PATH], ids=["source", "shipped"])
def test_invalid_git_directory_refuses_handoff_before_subtool(tmp_path, monkeypatch, capsys, session_path):
    root = tmp_path / "project"
    root.mkdir()
    (root / ".git").mkdir()
    session = _session_module(session_path)
    monkeypatch.setattr(session, "_repo_root", lambda: root)
    monkeypatch.setattr(session, "_do_reflection", lambda *args: None)
    monkeypatch.setattr(session, "_do_thread_survey", lambda *args: None)
    launched = []
    monkeypatch.setattr(session, "_surface_intents", lambda *args: launched.append(True))

    assert session.main(["session-end", "--prepare-handoff", "--dry-run"]) == 1
    assert "git could not resolve the worktree root" in capsys.readouterr().err
    assert not launched


def test_discovery_ignores_hostile_git_environment(tmp_path, monkeypatch):
    root = _repo(tmp_path / "project")
    decoy = _repo(tmp_path / "decoy")
    expected = _admin_binding(root)
    monkeypatch.setenv("GIT_DIR", str(decoy / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(decoy))
    monkeypatch.setenv("GIT_INDEX_FILE", str(decoy / "missing-index"))

    result = install.write_local_env(root)

    assert result[0] == expected
    assert result[3] == "installed"
    assert not (decoy / ".git" / "cairn" / "local-env.json").exists()
    assert _session_module()._resolve_interpreter(root) == (
        str(Path(sys.executable).resolve()), "local-env.json"
    )


def test_index_question_uses_fixed_arguments_and_scrubbed_environment(tmp_path, monkeypatch):
    root = _repo(tmp_path / "project")
    binding = _admin_binding(root)
    binding.parent.mkdir(parents=True)
    binding.write_text(json.dumps({"interpreter": str(Path(sys.executable).resolve())}),
                       encoding="utf-8")
    session = _session_module()
    helper = session._load_git_read_helper()
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "decoy"))
    seen = []
    launched = []
    real_capture = helper._capture_process
    real_popen = helper.subprocess.Popen

    def record_capture(argv, env, cwd, timeout, stdout_limit, stderr_limit,
                       snapshot, target, input_data=None, exclusions=None,
                       hook_index_snapshot=None):
        if "ls-files" in argv:
            seen.append((argv, env, cwd, timeout, input_data))
        return real_capture(argv, env, cwd, timeout, stdout_limit, stderr_limit,
                            snapshot, target, input_data, exclusions,
                            hook_index_snapshot=hook_index_snapshot)

    def record_popen(argv, *args, **kwargs):
        if "ls-files" in argv:
            launched.append((argv, kwargs))
        return real_popen(argv, *args, **kwargs)

    monkeypatch.setattr(helper, "_capture_process", record_capture)
    monkeypatch.setattr(helper.subprocess, "Popen", record_popen)
    session._resolve_interpreter(root)

    assert len(seen) == 1
    argv, env, cwd, timeout, input_data = seen[0]
    assert tuple(argv[-4:]) == ("ls-files", "-z", "--cached", "--stage")
    assert argv[argv.index("-C") + 1] == str(root)
    assert argv[1:5] == ["--no-pager", "-C", str(root), "--no-optional-locks"]
    assert cwd == helper._neutral_cwd(str(root)) and cwd != str(root)
    assert timeout == session._BINDING_GIT_TIMEOUT_SECONDS
    assert input_data is None
    git_env_keys = {key for key in env if key.upper().startswith("GIT_")}
    fixed_git_keys = {
        "GIT_ALLOW_PROTOCOL", "GIT_CONFIG_COUNT", "GIT_CONFIG_GLOBAL",
        "GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_SYSTEM", "GIT_NO_LAZY_FETCH",
        "GIT_NO_REPLACE_OBJECTS", "GIT_OPTIONAL_LOCKS", "GIT_PAGER",
        "GIT_PROTOCOL_FROM_USER", "GIT_TERMINAL_PROMPT",
    }
    fixed_git_keys.update(
        f"GIT_CONFIG_{part}_{index}"
        for index in range(15) for part in ("KEY", "VALUE")
    )
    assert git_env_keys == fixed_git_keys
    assert not {"GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                "GIT_CONFIG_PARAMETERS"} & git_env_keys
    assert env["GIT_CONFIG_COUNT"] == "15"
    assert env["GIT_CONFIG_KEY_0"] == "protocol.allow"
    assert env["GIT_CONFIG_VALUE_0"] == "never"
    assert env["GIT_CONFIG_KEY_1"] == "core.hooksPath"
    assert env["GIT_CONFIG_VALUE_1"] == os.devnull
    assert env["GIT_TERMINAL_PROMPT"] == "0"
    assert env["GIT_PAGER"] == ""
    assert env["GIT_CONFIG_NOSYSTEM"] == "1"
    assert env["GIT_CONFIG_GLOBAL"] == os.devnull
    assert env["GIT_CONFIG_SYSTEM"] == os.devnull
    assert env["GIT_OPTIONAL_LOCKS"] == "0"
    assert env["GIT_NO_REPLACE_OBJECTS"] == "1"
    assert env["GIT_NO_LAZY_FETCH"] == "1"
    assert env["GIT_PROTOCOL_FROM_USER"] == "0"
    assert env["GIT_ALLOW_PROTOCOL"] == ""
    if os.name == "posix":
        assert len(launched) == 1
        launched_argv, kwargs = launched[0]
        assert launched_argv == argv
        assert kwargs["cwd"] == helper._neutral_cwd(str(root))
        assert kwargs["cwd"] != str(root)
        assert kwargs["env"] == env
        assert kwargs["stdin"] == subprocess.DEVNULL
        assert kwargs["shell"] is False


def test_legacy_checkout_file_is_never_read(tmp_path):
    root = _repo(tmp_path / "project")
    old = root / "dev" / ".cairn" / "local-env.json"
    old.parent.mkdir(parents=True)
    old.write_text("not valid JSON", encoding="utf-8")

    session = _session_module()
    interpreter, source = session._resolve_interpreter(root)

    assert interpreter == sys.executable
    assert source == "fallback"


def test_binding_path_link_and_wrong_type_refuse(tmp_path):
    root = _repo(tmp_path / "project")
    session = _session_module()
    binding = _admin_binding(root)
    outside = tmp_path / "outside"
    outside.mkdir()
    sentinel = outside / "sentinel"
    sentinel.write_text("keep", encoding="utf-8")
    binding.parent.parent.mkdir(exist_ok=True)
    binding.parent.symlink_to(outside, target_is_directory=True)

    with pytest.raises(session.LifecycleError, match="link or reparse point"):
        session._resolve_interpreter(root)
    with pytest.raises(install.ScaffoldSecurityError):
        install.write_local_env(root, force=True)
    assert sentinel.read_text(encoding="utf-8") == "keep"

    binding.parent.unlink()
    binding.parent.mkdir()
    binding.mkdir()
    with pytest.raises(session.LifecycleError, match="not a regular file"):
        session._resolve_interpreter(root)
    with pytest.raises(install.ScaffoldSecurityError):
        install.write_local_env(root, force=True)


def test_dangling_binding_link_and_unreadable_state_refuse(tmp_path, monkeypatch):
    root = _repo(tmp_path / "project")
    session = _session_module()
    binding = _admin_binding(root)
    binding.parent.mkdir(parents=True)
    binding.symlink_to(tmp_path / "missing-binding")
    with pytest.raises(session.LifecycleError, match="link or reparse point"):
        session._resolve_interpreter(root)
    with pytest.raises(install.ScaffoldSecurityError):
        install.write_local_env(root, force=True)

    binding.unlink()
    binding.write_text('{"interpreter": "/usr/bin/true"}\n', encoding="utf-8")
    real_lstat = os.lstat

    def unreadable(path, *args, **kwargs):
        if Path(path) == binding:
            raise PermissionError("denied")
        return real_lstat(path, *args, **kwargs)

    monkeypatch.setattr(session.os, "lstat", unreadable)
    with pytest.raises(session.LifecycleError, match="could not be inspected"):
        session._resolve_interpreter(root)


def test_safe_existing_binding_is_preserved_until_force(tmp_path):
    root = _repo(tmp_path / "project")
    binding = _admin_binding(root)
    binding.parent.mkdir(parents=True)
    original = '{"interpreter": "/usr/bin/true"}\n'
    binding.write_text(original, encoding="utf-8")

    assert install.write_local_env(root)[3] == "skipped-exists"
    assert binding.read_text(encoding="utf-8") == original
    assert install.write_local_env(root, force=True)[3] == "installed"
    assert json.loads(binding.read_text(encoding="utf-8"))["interpreter"] == str(
        Path(sys.executable).resolve()
    )


def test_dot_git_symlink_refuses_discovery(tmp_path):
    root = _repo(tmp_path / "project")
    real_admin = tmp_path / "admin"
    (root / ".git").rename(real_admin)
    (root / ".git").symlink_to(real_admin, target_is_directory=True)
    session = _session_module()

    with pytest.raises(session.LifecycleError, match=".git is a link"):
        session._resolve_interpreter(root)
    with pytest.raises(install.ScaffoldSecurityError, match=".git entry"):
        install.write_local_env(root, force=True)


def test_regular_git_pointer_to_linked_administration_refuses(tmp_path):
    root = _repo(tmp_path / "project")
    real_admin = tmp_path / "real-admin"
    (root / ".git").rename(real_admin)
    alias = tmp_path / "admin-link"
    alias.symlink_to(real_admin, target_is_directory=True)
    (root / ".git").write_text("gitdir: ../admin-link\n", encoding="utf-8")
    binding = _admin_binding(root)
    binding.parent.mkdir(parents=True, exist_ok=True)
    binding.write_text('{"interpreter": "/usr/bin/true"}\n', encoding="utf-8")
    session = _session_module()

    with pytest.raises(session.LifecycleError, match="link or reparse point"):
        session._resolve_interpreter(root)
    with pytest.raises(install.ScaffoldSecurityError, match="link or reparse point"):
        install.write_local_env(root, force=True)


def test_legacy_marker_control_and_mutant(tmp_path, monkeypatch):
    """The real optional-tool entry point ignores legacy state; a redirect is caught."""
    root = _repo(tmp_path / "project")
    tools = root / "tools"
    tools.mkdir()
    intent = tools / "intent.py"
    source = SESSION_PATH.read_text(encoding="utf-8")
    helper_source = (SESSION_PATH.parent / "git_read.py").read_bytes()
    (tools / "git_read.py").write_bytes(helper_source)
    original = tools / "session.py"
    original.write_text(source, encoding="utf-8")

    marker = tmp_path / "legacy-binding-ran"
    if os.name == "nt":
        # A copied interpreter makes the executable choice observable through
        # the real subprocess, without requiring a compiler or shell script.
        fake = tmp_path / "fake-python.exe"
        shutil.copy2(sys.executable, fake)
        for directory in {Path(sys.executable).parent, Path(sys.base_prefix)}:
            for dll in directory.glob("python*.dll"):
                shutil.copy2(dll, tmp_path / dll.name)
        # Conda's runtime DLLs (including zlib) live beside its interpreter.
        monkeypatch.setenv(
            "PATH", sys.base_prefix + os.pathsep + os.environ.get("PATH", ""))
        monkeypatch.setenv("PYTHONHOME", sys.base_prefix)
        intent.write_text(
            "import pathlib, sys\n"
            f"expected = pathlib.Path({str(fake)!r})\n"
            f"marker = pathlib.Path({str(marker)!r})\n"
            "if pathlib.Path(sys.executable).resolve() == expected.resolve():\n"
            "    marker.write_text('ran', encoding='utf-8')\n"
            "raise SystemExit(1)\n", encoding="utf-8",
        )
    else:
        intent.write_text("raise SystemExit(1)\n", encoding="utf-8")
        fake = tmp_path / "fake-python"
        fake.write_text(f'#!/bin/sh\nprintf ran > "{marker}"\nexit 0\n', encoding="utf-8")
        fake.chmod(fake.stat().st_mode | 0o111)
    legacy = root / "dev" / ".cairn" / "local-env.json"
    legacy.parent.mkdir(parents=True)
    legacy.write_text(json.dumps({"interpreter": str(fake)}), encoding="utf-8")

    control = _session_module(original)
    assert control._intent_whoami(root) is None
    assert not marker.exists()

    needle = "cfg = _git_binding_path(root)"
    assert needle in source
    mutant_source = source.replace(
        needle, 'cfg = _state_dir(root) / "local-env.json"', 1
    )
    mutant_path = tools / "session-mutant.py"
    mutant_path.write_text(mutant_source, encoding="utf-8")
    mutant = _session_module(mutant_path)
    assert mutant._intent_whoami(root) is None
    assert marker.read_text(encoding="utf-8") == "ran"


@pytest.mark.skipif(os.name != "nt", reason="requires native Windows junctions")
@pytest.mark.parametrize("location", ["dot-git", "admin", "binding-directory", "binding-leaf"])
@pytest.mark.parametrize("session_path", [SESSION_PATH, SHIPPED_SESSION_PATH], ids=["source", "shipped"])
def test_windows_reparse_points_refuse_binding_access(tmp_path, location, session_path, monkeypatch):
    root = _repo(tmp_path / "project")
    outside = tmp_path / "outside"
    outside.mkdir()
    sentinel = outside / "sentinel"
    sentinel.write_text("keep", encoding="utf-8")
    admin = root / ".git"
    if location == "dot-git":
        target = tmp_path / "real-admin"
        admin.rename(target)
        junction = admin
    elif location == "admin":
        target = tmp_path / "real-admin"
        admin.rename(target)
        junction = tmp_path / "admin-junction"
        admin.write_text("gitdir: ../admin-junction\n", encoding="utf-8")
    elif location == "binding-directory":
        target = outside
        junction = admin / "cairn"
    else:
        junction = admin / "cairn" / "local-env.json"
        junction.parent.mkdir()
        junction.symlink_to(sentinel)  # A privilege failure leaves this case open.
    if location != "binding-leaf":
        # mklink /J creates a junction without requiring symlink privileges.
        subprocess.run(["cmd", "/c", "mklink", "/J", str(junction), str(target)],
                       check=True, capture_output=True, text=True)
    session = _session_module(session_path)
    monkeypatch.setattr(session, "_repo_root", lambda: root)
    monkeypatch.setattr(session, "_do_reflection", lambda *args: None)
    monkeypatch.setattr(session, "_do_thread_survey", lambda *args: None)
    launched = []
    monkeypatch.setattr(session, "_surface_intents", lambda *args: launched.append(True))
    assert session.main(["session-end", "--prepare-handoff", "--dry-run"]) == 1
    assert not launched
    config = tmp_path / "profile.yml"
    config.write_text("project_name: Test\ntest_command: pytest\nmodules: []\n", encoding="utf-8")
    assert scaffold_main(["--config", str(config), "--target", str(root),
                          "--cairn-root", str(SESSION_PATH.parents[1]),
                          "--allow-dev", "--force"]) != 0
    assert sentinel.read_text(encoding="utf-8") == "keep"
