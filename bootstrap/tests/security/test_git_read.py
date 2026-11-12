"""Component controls for the mirrored bounded Git read implementation.

Promises:
- A bounded git read refuses an executable changed during the read and runs only the verified bytes.
- A status read neutralises configured clean and smudge filters before it runs.
- A read never runs a git executable found inside the enclosing repository.
- A timed-out git read reports incomplete and kills its own process group.
- A remote lookup admits only the no-contact URL form and refuses other forms.
- A read of origin returns one record and refuses oversize or NUL-containing input.
"""
from __future__ import annotations

import ctypes
import errno
import hashlib
import importlib.util
import os
import shutil
import shlex
import signal
import stat
import subprocess
import sys
import threading
import time
import types
import uuid
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
HELPER_PATH = ROOT / "templates/skills/_lib/git_read.py"
SPEC = importlib.util.spec_from_file_location("_cairn_test_git_read", HELPER_PATH)
assert SPEC is not None and SPEC.loader is not None
git_read = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(git_read)


def _fake_git(directory: Path, body: str, name: str = "git") -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    exe = directory / name
    exe.write_text("#!/bin/sh\n" + body, encoding="utf-8")
    exe.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    return exe


def test_verified_module_executes_the_exact_pinned_buffer_without_cache_reuse(
        tmp_path: Path) -> None:
    source = tmp_path / "helper.py"
    source.write_bytes(b"VALUE = 'verified'\n")
    pin = hashlib.sha256(source.read_bytes()).hexdigest()
    module = git_read.load_verified_module(source, pin, "same-name")
    assert module.VALUE == "verified"
    assert module.__verified_source__ == b"VALUE = 'verified'\n"
    assert "same-name" not in __import__("sys").modules

    source.write_bytes(b"VALUE = 'substituted'\n")
    with pytest.raises(git_read.GitReadError, match="helper-pin-mismatch"):
        git_read.load_verified_module(source, pin, "same-name")


# Declared exception (internal hook): Hook: monkeypatched git_read.os.read (module-internal os reference). Monkeypatches git_read.os.read (an internal seam) to change the executable mid-re.
def test_checked_bytes_refuses_descriptor_change_time_during_read(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "changing.py"
    source.write_bytes(b"VALUE = 'stable'\n")
    original = source.stat()
    identity = (original.st_dev, original.st_ino)
    real_read = git_read.os.read
    mutation: dict[str, int] = {}

    def change_native_change_time(fd: int, size: int) -> bytes:
        before = os.fstat(fd)
        data = real_read(fd, size)
        if (before.st_dev, before.st_ino) == identity and not mutation:
            current = source.stat()
            os.utime(source, ns=(current.st_atime_ns,
                                 current.st_mtime_ns + 4_000_000_000))
            after = os.fstat(fd)
            mutation["before_ctime"] = before.st_ctime_ns
            mutation["after_ctime"] = after.st_ctime_ns
        return data

    monkeypatch.setattr(git_read.os, "read", change_native_change_time)
    with pytest.raises(git_read.GitReadError, match="file-changed-during-read"):
        git_read._checked_bytes(str(source), git_read.HELPER_MAX_BYTES)
    assert mutation
    assert mutation["after_ctime"] != mutation["before_ctime"]


def test_verified_module_refuses_linked_components_and_oversize(tmp_path: Path) -> None:
    actual = tmp_path / "actual"
    actual.mkdir()
    source = actual / "helper.py"
    source.write_bytes(b"VALUE = 1\n")
    linked = tmp_path / "linked"
    linked.symlink_to(actual, target_is_directory=True)
    with pytest.raises(git_read.GitReadError, match="linked-path-component"):
        git_read.load_verified_module(linked / source.name,
                                      hashlib.sha256(source.read_bytes()).hexdigest(),
                                      "linked")
    source.write_bytes(b"x" * (git_read.HELPER_MAX_BYTES + 1))
    with pytest.raises(git_read.GitReadError, match="file-size-limit"):
        git_read.load_verified_module(source,
                                      hashlib.sha256(source.read_bytes()).hexdigest(),
                                      "oversize")


def test_enclosing_gitfile_and_bare_markers_are_excluded_before_probe(
        tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    nested = checkout / "nested" / "target"
    nested.mkdir(parents=True)
    (checkout / ".git").write_text("gitdir: /outside/admin\n", encoding="utf-8")
    assert str(checkout) in git_read.worktree_exclusions(str(nested))

    bare = tmp_path / "bare"
    (bare / "objects").mkdir(parents=True)
    (bare / "refs").mkdir()
    (bare / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (bare / "config").write_text("[core]\n bare = true\n", encoding="utf-8")
    below_bare = bare / "objects" / "target"
    below_bare.mkdir()
    assert str(bare) in git_read.worktree_exclusions(str(below_bare))


def test_relative_path_entries_are_not_selected(tmp_path: Path) -> None:
    assert git_read.select_git(str(tmp_path), path_value=".") is None
    assert git_read.select_git(str(tmp_path), path_value=os.pathsep) is None
    assert git_read.read_version(str(tmp_path), path_value=".").state == "absent"


def test_executable_inside_enclosing_repository_is_refused_before_version(
        tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    target = repo / "nested"
    target.mkdir(parents=True)
    (repo / ".git").mkdir()
    executable = _fake_git(repo / "bin", "printf 'git version 2.45.0\\n'\n")
    with pytest.raises(git_read.GitReadError, match="git-inside-inspected-repository"):
        git_read.select_git(str(target), path_value=str(executable.parent))


def test_host_git_runs_with_closed_input_and_reports_bounded_completion(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    body = (
        "if [ \"$1\" = \"--version\" ]; then printf 'git version 2.45.0\\n'; exit 0; fi\n"
        "if read value; then printf 'input-open'; else printf 'input-closed'; fi\n"
        "printf '|%s' \"${GIT_DIR-unset}\"\n"
    )
    executable = _fake_git(tmp_path / "bin", body)
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "hostile"))
    result = git_read.run_git(str(target), ("rev-parse", "--show-toplevel"),
                              path_value=str(executable.parent))
    assert result.state == "completed" and result.returncode == 0
    assert result.stdout == b"input-closed|unset"

    limited = git_read.run_git(str(target), ("rev-parse", "--show-toplevel"),
                               path_value=str(executable.parent), output_limit=3)
    assert limited.state == "failed" and limited.stdout == b""


def test_version_cache_is_bound_to_revalidated_executable_bytes(tmp_path: Path) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    marker = tmp_path / "versions"
    exe = _fake_git(tmp_path / "bin", (
        "if [ \"$1\" = \"--version\" ]; then printf x >> '" + str(marker) + "'; "
        "printf 'git version 2.45.0\\n'; exit 0; fi\n"
    ))
    first = git_read.read_version(str(target), path_value=str(exe.parent))
    second = git_read.read_version(str(target), path_value=str(exe.parent))
    assert first.state == second.state == "completed"
    assert first.stdout == second.stdout == b"git version 2.45.0\n"
    assert marker.read_text(encoding="ascii") == "x"

    exe.write_text(
        "#!/bin/sh\nif [ \"$1\" = \"--version\" ]; then printf x >> '"
        + str(marker) + "'; printf 'git version 2.46.0\\n'; exit 0; fi\n",
        encoding="utf-8")
    exe.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    changed = git_read.read_version(str(target), path_value=str(exe.parent))
    assert changed.state == "completed" and changed.stdout == b"git version 2.46.0\n"
    assert marker.read_text(encoding="ascii") == "xx"


def _component_stat_rows(path: Path) -> tuple[tuple[str, os.stat_result], ...]:
    names = git_read._component_chain(str(path))
    rows = git_read._lstat_chain(str(path), leaf_regular=True)
    return tuple(zip(names, rows))


def _changed_stat_fields(before: os.stat_result,
                         after: os.stat_result) -> tuple[str, ...]:
    names = ("st_dev", "st_ino", "st_mode", "st_size", "st_mtime_ns",
             "st_ctime_ns")
    return tuple(name for name in names
                 if getattr(before, name) != getattr(after, name))


# Declared exception (internal hook): Hook: monkeypatched git_read.os.read creates a sibling mid-read. Monkeypatches git_read.os.read (an internal seam) to change the executable mid-read; .
def test_executable_digest_refuses_an_unrelated_ancestor_change_during_read(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    exe = _fake_git(tmp_path / "bin", "printf 'git version 2.45.0\\n'\n")
    sibling = tmp_path / "unrelated-sibling"
    real_read = git_read.os.read
    executable_info = exe.stat()
    captured: dict[str, object] = {}
    created = False

    def create_sibling_after_executable_read(fd: int, size: int) -> bytes:
        nonlocal created
        is_executable = (os.fstat(fd).st_dev, os.fstat(fd).st_ino) == (
            executable_info.st_dev, executable_info.st_ino)
        before = _component_stat_rows(exe) if is_executable and not created else ()
        data = real_read(fd, size)
        if is_executable and not created:
            sibling.write_text("unrelated\n", encoding="utf-8")
            after = _component_stat_rows(exe)
            changes = {
                name: _changed_stat_fields(old, new)
                for (name, old), (_, new) in zip(before, after)
                if _changed_stat_fields(old, new)
            }
            captured["changes"] = changes
            created = True
        return data

    monkeypatch.setattr(git_read.os, "read", create_sibling_after_executable_read)
    selected = git_read.select_git(str(target), path_value=str(exe.parent))

    assert created and sibling.read_text(encoding="utf-8") == "unrelated\n"
    changes = captured["changes"]
    assert set(changes) == {str(tmp_path)}, changes
    changed_fields = set(changes[str(tmp_path)])
    assert {"st_mtime_ns", "st_ctime_ns"} <= changed_fields, changes
    assert changed_fields <= {"st_size", "st_mtime_ns", "st_ctime_ns"}, changes
    after_executable_info = exe.stat()
    assert (git_read._stat_key(executable_info)
            == git_read._stat_key(after_executable_info))
    assert (git_read._executable_component_key(executable_info)
            == git_read._executable_component_key(after_executable_info))
    assert selected is not None
    assert selected.digest == hashlib.sha256(exe.read_bytes()).hexdigest()


# Declared exception (internal hook): Hook: monkeypatched git_read.os.read replaces the executable mid-read. Monkeypatches git_read.os.read (an internal seam) to change the executable mid-.
def test_executable_digest_refuses_replacement_during_read(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    exe = _fake_git(tmp_path / "bin", "printf 'git version 2.45.0\\n'\n")
    replacement = tmp_path / "replacement-git"
    replacement.write_text("#!/bin/sh\nprintf 'different\\n'\n", encoding="utf-8")
    replacement.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    executable_info = exe.stat()
    real_read = git_read.os.read
    replaced = False
    sibling = tmp_path / "unrelated-sibling"

    def replace_after_executable_read(fd: int, size: int) -> bytes:
        nonlocal replaced
        is_executable = (os.fstat(fd).st_dev, os.fstat(fd).st_ino) == (
            executable_info.st_dev, executable_info.st_ino)
        data = real_read(fd, size)
        if is_executable and not replaced:
            sibling.write_text("unrelated\n", encoding="utf-8")
            os.replace(replacement, exe)
            replaced = True
        return data

    monkeypatch.setattr(git_read.os, "read", replace_after_executable_read)
    with pytest.raises(git_read.GitReadError,
                       match="executable-changed-during-read"):
        git_read.select_git(str(target), path_value=str(exe.parent))
    assert replaced and sibling.exists()


# Declared exception (internal hook): Hook: monkeypatched git_read.os.read causes directory churn mid-read. Monkeypatches git_read.os.read (an internal seam) to change the executable mid-r.
@pytest.mark.parametrize("change", ["bytes", "timestamp", "mode"])
def test_executable_change_still_refuses_with_directory_churn(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, change: str) -> None:
    if change == "mode" and os.name == "nt":
        pytest.skip("Windows chmod does not expose executable mode bits")
    target = tmp_path / "repo"
    target.mkdir()
    exe = _fake_git(tmp_path / "bin", "printf 'git version 2.45.0\\n'\n")
    sibling = tmp_path / "unrelated-sibling"
    executable_info = exe.stat()
    real_read = git_read.os.read
    changed = False

    def mutate_after_executable_read(fd: int, size: int) -> bytes:
        nonlocal changed
        is_executable = (os.fstat(fd).st_dev, os.fstat(fd).st_ino) == (
            executable_info.st_dev, executable_info.st_ino)
        data = real_read(fd, size)
        if is_executable and not changed:
            sibling.write_text("unrelated\n", encoding="utf-8")
            if change == "bytes":
                exe.write_text("#!/bin/sh\nprintf changed\n", encoding="utf-8")
            elif change == "timestamp":
                info = exe.stat()
                os.utime(exe, ns=(info.st_atime_ns, info.st_mtime_ns + 2_000_000_000))
            else:
                info = exe.stat()
                exe.chmod(info.st_mode ^ stat.S_IXUSR)
            changed = True
        return data

    monkeypatch.setattr(git_read.os, "read", mutate_after_executable_read)
    original_mode = executable_info.st_mode
    try:
        with pytest.raises(git_read.GitReadError,
                           match="executable-changed-during-read"):
            git_read.select_git(str(target), path_value=str(exe.parent))
    finally:
        if change == "mode" and exe.exists():
            exe.chmod(original_mode)
    assert changed and sibling.exists()


# Declared exception (internal hook): Hook: monkeypatched git_read.os.read changes an ancestor mode mid-read. Monkeypatches git_read.os.read (an internal seam) to change the executable mid.
@pytest.mark.skipif(os.name == "nt", reason="POSIX directory mode bits")
def test_executable_digest_refuses_persistent_ancestor_mode_change(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    exe = _fake_git(tmp_path / "bin", "printf 'git version 2.45.0\\n'\n")
    directory = exe.parent
    original_mode = stat.S_IMODE(directory.stat().st_mode)
    real_read = git_read.os.read
    changed = False

    def chmod_after_executable_read(fd: int, size: int) -> bytes:
        nonlocal changed
        is_executable = (os.fstat(fd).st_dev, os.fstat(fd).st_ino) == (
            exe.stat().st_dev, exe.stat().st_ino)
        data = real_read(fd, size)
        if is_executable and not changed:
            directory.chmod(original_mode ^ stat.S_IWUSR)
            changed = True
        return data

    monkeypatch.setattr(git_read.os, "read", chmod_after_executable_read)
    try:
        with pytest.raises(git_read.GitReadError,
                           match="executable-changed-during-read"):
            git_read.select_git(str(target), path_value=str(exe.parent))
    finally:
        directory.chmod(original_mode)
    assert changed


# Declared exception (internal hook): Hook: wraps _checked_digest to swap the parent directory after digest; public select_git cannot time that race. Distinct from file-replace test.
def test_executable_digest_refuses_directory_replacement(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    exe = _fake_git(tmp_path / "bin", "printf 'git version 2.45.0\\n'\n")
    directory = exe.parent
    replacement_directory = tmp_path / "bin-original"
    original_digest = git_read._checked_digest
    changed = False

    def replace_parent_after_digest(path: str, limit: int):
        nonlocal changed
        result = original_digest(path, limit)
        if not changed:
            os.rename(directory, replacement_directory)
            directory.mkdir()
            os.link(replacement_directory / exe.name, exe)
            changed = True
        return result

    monkeypatch.setattr(git_read, "_checked_digest", replace_parent_after_digest)
    try:
        with pytest.raises(git_read.GitReadError,
                           match="executable-path-changed"):
            git_read.select_git(str(target), path_value=str(exe.parent))
    finally:
        if exe.exists():
            exe.unlink()
        if directory.exists():
            directory.rmdir()
        if replacement_directory.exists():
            os.rename(replacement_directory, directory)
    assert changed


# Declared exception (internal hook): Hook: monkeypatched git_read.os.read retargets a symlink mid-read. Monkeypatches git_read.os.read (an internal seam) to change the executable mid-read.
def test_executable_path_refuses_lexical_symlink_retarget_during_read(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    first = _fake_git(tmp_path / "first-bin", "printf 'git version 2.45.0\\n'\n")
    second = _fake_git(tmp_path / "second-bin", "printf 'git version 2.46.0\\n'\n")
    bindir = tmp_path / "path"
    bindir.mkdir()
    lexical = bindir / "git"
    lexical.symlink_to(first)
    first_info = first.stat()
    real_read = git_read.os.read
    retargeted = False

    def retarget_after_executable_read(fd: int, size: int) -> bytes:
        nonlocal retargeted
        is_first = (os.fstat(fd).st_dev, os.fstat(fd).st_ino) == (
            first_info.st_dev, first_info.st_ino)
        data = real_read(fd, size)
        if is_first and not retargeted:
            lexical.unlink()
            lexical.symlink_to(second)
            retargeted = True
        return data

    monkeypatch.setattr(git_read.os, "read", retarget_after_executable_read)
    with pytest.raises(git_read.GitReadError, match="executable-path-changed"):
        git_read.select_git(str(target), path_value=str(bindir))
    assert retargeted


def test_old_git_never_receives_an_object_read(tmp_path: Path) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    marker = tmp_path / "object-read"
    body = (
        "if [ \"$1\" = \"--version\" ]; then printf 'git version 2.44.0\\n'; exit 0; fi\n"
        f"printf called > '{marker}'\n"
    )
    executable = _fake_git(tmp_path / "bin", body)
    result = git_read.run_git(str(target), ("show", "HEAD"),
                              path_value=str(executable.parent))
    assert result.state == "failed"
    assert result.reason == "git-version-below-read-floor"
    assert not marker.exists()


def test_old_git_admits_only_reviewed_metadata_config_and_index_list_forms(
        tmp_path: Path) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    marker = tmp_path / "called"
    executable = _fake_git(tmp_path / "bin", (
        "if [ \"$1\" = \"--version\" ]; then printf 'git version 2.44.0\\n'; exit 0; fi\n"
        f"printf called >> '{marker}'\n"
        "printf 'ok\\n'\n"
    ))
    allowed = (
        ("rev-parse", "--show-toplevel"),
        ("rev-parse", "--verify", "-q", "HEAD"),
        ("rev-parse", "--verify", "HEAD"),
        ("config", "--includes", "--null", "--list"),
        ("config", "--list", "--local", "--includes", "--show-origin", "-z"),
        ("config", "-z", "--get-regexp",
         r"core\.filemode|core\.autocrlf|core\.eol|promisor|partialclone"),
        ("ls-files", "-z", "--cached", "--stage"),
        ("ls-files", "-z", "--", "literal.md"),
    )
    for args in allowed:
        result = git_read.run_git(str(target), args, path_value=str(executable.parent))
        assert result.state == "completed", (args, result)
    assert marker.read_text(encoding="ascii") == "called" * len(allowed)
    marker.unlink()
    rejected = (
        ("diff", "--cached", "--name-only", "-z"),
        ("diff", "--cached", "--name-status", "-M", "-z"),
        ("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "-z", "HEAD"),
        ("rev-parse", "--verify", "-q", "HEAD^{commit}"),
        ("rev-parse", "--verify", "HEAD~1"),
        ("config", "-z", "--get-regexp",
         r"core\.filemode|remote[.]origin[.]url|partialclone"),
        ("for-each-ref", "--format=%(objectname)"),
        ("config", "--list", "--global", "--includes", "--show-origin", "-z"),
    )
    for args in rejected:
        result = git_read.run_git(str(target), args, path_value=str(executable.parent))
        assert result.state == "failed"
        assert result.reason == "git-version-below-read-floor"
    assert not marker.exists()


@pytest.mark.skipif(shutil.which("git") is None, reason="real Git unavailable")
def test_hook_index_uses_private_snapshot_and_closed_child_environment(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    git = shutil.which("git")
    assert git is not None
    path_value = str(Path(git).parent)
    monkeypatch.setenv("PATH", path_value)
    repo = tmp_path / "repo"
    repo.mkdir()
    env = {"PATH": path_value, "HOME": str(tmp_path),
           "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
           "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@example.invalid"}

    def git_run(*args: str) -> None:
        subprocess.run([git, "-C", str(repo), *args], env=env,
                       stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=True)

    git_run("init", "-q")
    (repo / "a.md").write_text("base\n")
    (repo / "b.md").write_text("base\n")
    git_run("add", "a.md", "b.md")
    git_run("commit", "-qm", "base")
    (repo / "a.md").write_text("staged a\n")
    (repo / "b.md").write_text("staged b\n")
    git_run("add", "a.md", "b.md")
    admin = repo / ".git"
    locator = admin / "next-index-123.lock"
    shutil.copyfile(admin / "index", locator)
    original = git_read._capture_posix_git
    seen: list[str] = []

    def capture(argv, child_env, cwd, timeout, stdout_limit, stderr_limit,
                input_data=None):
        if "diff" in argv:
            snapshot = Path(child_env["GIT_INDEX_FILE"])
            assert snapshot != locator
            assert snapshot.parent != admin
            assert snapshot.read_bytes() == locator.read_bytes()
            assert "GIT_DIR" not in child_env
            seen.append(str(snapshot))
        return original(argv, child_env, cwd, timeout, stdout_limit,
                        stderr_limit, input_data)

    monkeypatch.setattr(git_read, "_capture_posix_git", capture)
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "wrong-git-dir"))
    monkeypatch.chdir(repo)
    result = git_read.read_hook_index(
        str(repo), ("diff", "--cached", "--name-only", "-z"),
        index_file=str(locator))
    version = git_read.read_version(str(repo))
    parsed = git_read._parse_version(version.stdout)
    if version.state != "completed" or parsed is None or parsed < (2, 45, 0):
        pytest.skip("real Git 2.45 or newer is required for hook index reads")
    assert result.state == "completed" and result.returncode == 0
    assert result.stdout.split(b"\0")[:-1] == [b"a.md", b"b.md"]
    assert seen and not Path(seen[0]).exists()
    assert locator.exists()

    outside = tmp_path / "outside-index"
    shutil.copyfile(locator, outside)
    rejected = git_read.read_hook_index(
        str(repo), ("diff", "--cached", "--name-only", "-z"),
        index_file=str(outside))
    assert rejected.state == "failed"


@pytest.mark.skipif(shutil.which("git") is None, reason="real Git unavailable")
def test_hook_index_rejects_wrong_commands_paths_and_malformed_indexes(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    git = shutil.which("git")
    assert git is not None
    path_value = str(Path(git).parent)
    monkeypatch.setenv("PATH", path_value)
    repo = tmp_path / "repo"
    repo.mkdir()
    env = {"PATH": path_value, "HOME": str(tmp_path),
           "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
           "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@example.invalid"}
    subprocess.run([git, "-C", str(repo), "init", "-q"], env=env, check=True)
    (repo / "item").write_text("base\n")
    subprocess.run([git, "-C", str(repo), "add", "item"], env=env, check=True)
    subprocess.run([git, "-C", str(repo), "commit", "-qm", "base"],
                   env=env, check=True)
    admin = repo / ".git"
    malformed = admin / "index.lock"
    malformed.write_bytes(b"not-a-git-index")
    monkeypatch.chdir(repo)

    unsupported = git_read.read_hook_index(str(repo), ("status",))
    assert unsupported.state == "failed"
    assert unsupported.reason == "unsupported-hook-index-read"
    empty = git_read.read_hook_index(
        str(repo), ("diff", "--cached", "--name-only", "-z"), index_file="")
    assert empty.state == "failed" and empty.reason == "hook-index-locator-invalid"
    bad_header = git_read.read_hook_index(
        str(repo), ("diff", "--cached", "--name-only", "-z"),
        index_file=str(malformed))
    assert bad_header.state == "failed" and bad_header.reason == "hook-index-format-invalid"
    malformed.unlink()
    linked = admin / "next-index-1.lock"
    linked.symlink_to(admin / "index")
    linked_result = git_read.read_hook_index(
        str(repo), ("diff", "--cached", "--name-only", "-z"),
        index_file=str(linked))
    assert linked_result.state == "failed"
    linked.unlink()


# Declared exception (internal hook): Hook: monkeypatches the internal _capture_posix_git to drift the index source mid-read; no public route changes the source between snapshot and read.
@pytest.mark.skipif(shutil.which("git") is None, reason="real Git unavailable")
def test_hook_index_source_drift_discards_read_result(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    git = shutil.which("git")
    assert git is not None
    path_value = str(Path(git).parent)
    monkeypatch.setenv("PATH", path_value)
    repo = tmp_path / "repo"
    repo.mkdir()
    env = {"PATH": path_value, "HOME": str(tmp_path),
           "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
           "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@example.invalid"}
    subprocess.run([git, "-C", str(repo), "init", "-q"], env=env, check=True)
    (repo / "item").write_text("base\n")
    subprocess.run([git, "-C", str(repo), "add", "item"], env=env, check=True)
    subprocess.run([git, "-C", str(repo), "commit", "-qm", "base"],
                   env=env, check=True)
    (repo / "item").write_text("staged\n")
    subprocess.run([git, "-C", str(repo), "add", "item"], env=env, check=True)
    locator = repo / ".git" / "next-index-2.lock"
    shutil.copyfile(repo / ".git" / "index", locator)
    monkeypatch.chdir(repo)
    original = git_read._capture_posix_git

    def mutate_after_read(argv, child_env, cwd, timeout, stdout_limit,
                          stderr_limit, input_data=None):
        result = original(argv, child_env, cwd, timeout, stdout_limit,
                          stderr_limit, input_data)
        if "diff" in argv:
            locator.write_bytes(b"changed after snapshot")
        return result

    monkeypatch.setattr(git_read, "_capture_posix_git", mutate_after_read)
    result = git_read.read_hook_index(
        str(repo), ("diff", "--cached", "--name-only", "-z"),
        index_file=str(locator))
    assert result.state == "failed" and result.stdout == b""
    assert result.reason == "hook-index-source-changed"


def test_status_neutralizes_every_configured_filter_before_read(tmp_path: Path) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    marker = tmp_path / "status-argv"
    body = (
        "if [ \"$1\" = \"--version\" ]; then printf 'git version 2.45.0\\n'; exit 0; fi\n"
        "case \"$*\" in\n"
        "  *config*) printf 'filter.demo.clean\\nrun-clean\\000filter.demo.process\\nrun-process\\000filter.demo.required\\ntrue\\000';;\n"
        f"  *) printf '%s\\n' \"$@\" > '{marker}'; printf clean\\n;;\n"
        "esac\n"
    )
    executable = _fake_git(tmp_path / "bin", body)
    result = git_read.run_git(str(target), ("-c", "core.quotePath=false",
                                           "status", "--porcelain=v1"),
                              path_value=str(executable.parent))
    assert result.state == "completed" and result.returncode == 0
    argv = marker.read_text(encoding="utf-8")
    assert "filter.demo.clean=" in argv
    assert "filter.demo.smudge=" in argv
    assert "filter.demo.process=" in argv
    assert "filter.demo.required=false" in argv
    assert "core.quotePath=false" in argv


@pytest.mark.skipif(os.name != "posix", reason="POSIX Git filter command control")
def test_real_status_cannot_execute_a_mixed_case_clean_filter(tmp_path: Path) -> None:
    real_git = shutil.which("git")
    if not real_git:
        pytest.skip("git not available")
    repo = tmp_path / "repo"
    repo.mkdir()
    env = os.environ.copy()
    env.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_AUTHOR_NAME": "Cairn test", "GIT_COMMITTER_NAME": "Cairn test",
                "GIT_AUTHOR_EMAIL": "test@example.invalid",
                "GIT_COMMITTER_EMAIL": "test@example.invalid"})

    def git(*args: str) -> None:
        subprocess.run([real_git, "-C", str(repo), *args], env=env,
                       check=True, capture_output=True)

    git("init", "-q")
    (repo / ".gitattributes").write_text("*.dat filter=DeMo\n", encoding="ascii")
    data = repo / "tracked.dat"
    data.write_bytes(b"aaaa\n")
    git("add", ".gitattributes", "tracked.dat")
    git("commit", "-qm", "fixture")
    marker = tmp_path / "clean-filter-ran"
    git("config", "filter.DeMo.clean",
        f"sh -c 'printf x >> {marker}; cat'")
    git("config", "filter.DeMo.required", "true")
    data.write_bytes(b"bbbb\n")
    unsafe = subprocess.run([real_git, "-C", str(repo), "status", "--porcelain=v1"],
                            env=env, capture_output=True, check=False)
    assert unsafe.returncode == 0 and marker.exists()

    marker.unlink()
    result = git_read.run_git(
        str(repo), ("status", "--porcelain=v1"),
        path_value=str(Path(real_git).resolve().parent),
    )
    assert result.state == "completed" and result.returncode == 0
    assert not marker.exists()


def test_ls_remote_admits_only_the_no_contact_url_query(tmp_path: Path) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    marker = tmp_path / "git-argv"
    executable = _fake_git(
        tmp_path / "bin",
        "if [ \"$1\" = \"--version\" ]; then printf 'git version 2.45.0\\n'; exit 0; fi\n"
        f"printf '%s\\n' \"$@\" > '{marker}'\n"
        "printf 'ssh://example.invalid/repo\\n'\nexit 0\n",
    )
    result = git_read.run_git(
        str(target), ("ls-remote", "--quiet", "--get-url"),
        path_value=str(executable.parent), output_limit=128,
    )
    assert result.state == "completed" and result.returncode == 0
    assert result.stdout == b"ssh://example.invalid/repo\n"
    assert "ls-remote" in marker.read_text(encoding="utf-8")

    refused = git_read.run_git(
        str(target), ("ls-remote", "--quiet", "--get-url", "origin"),
        path_value=str(tmp_path / "no-git"),
    )
    assert refused.state == "failed"
    assert refused.reason == "unsupported-read-form"


@pytest.mark.skipif(os.name != "posix", reason="POSIX group ownership control")
def test_timeout_kills_the_owned_process_group_and_returns_incomplete(
        tmp_path: Path) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    marker = tmp_path / "surviving-child"
    body = (
        "if [ \"$1\" = \"--version\" ]; then printf 'git version 2.45.0\\n'; exit 0; fi\n"
        f"(/bin/sleep 0.5; printf leaked > '{marker}') &\nwait\n"
    )
    executable = _fake_git(tmp_path / "bin", body)
    started = time.monotonic()
    result = git_read.run_git(str(target), ("rev-parse", "--show-toplevel"),
                              path_value=str(executable.parent), timeout=0.2)
    elapsed = time.monotonic() - started
    assert result.state == "failed" and result.stdout == b""
    assert elapsed < 3.0
    time.sleep(0.7)
    assert not marker.exists()


@pytest.mark.skipif(os.name != "posix", reason="POSIX owned-group cleanup control")
def test_normal_git_exit_kills_a_quiet_term_ignoring_descendant(
        tmp_path: Path) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    pid_file = tmp_path / "quiet-child.pid"
    child = (
        "import os,signal,time; from pathlib import Path; "
        "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
        f"Path({str(pid_file)!r}).write_text(str(os.getpid())); "
        "time.sleep(60)"
    )
    executable = _fake_git(tmp_path / "bin", (
        "if [ \"$1\" = \"--version\" ]; then "
        "printf 'git version 2.45.0\\n'; exit 0; fi\n"
        f"{shlex.quote(sys.executable)} -c {shlex.quote(child)} "
        ">/dev/null 2>&1 &\n"
        f"while [ ! -f {shlex.quote(str(pid_file))} ]; do /bin/sleep 0.01; done\n"
        "printf 'clean\\n'\n"
    ))
    result = git_read.run_git(
        str(target), ("rev-parse", "--show-toplevel"),
        path_value=str(executable.parent), timeout=2,
    )
    assert result.state == "completed" and result.returncode == 0
    assert pid_file.is_file()
    pid = int(pid_file.read_text(encoding="ascii"))
    deadline = time.monotonic() + 1.0
    try:
        while time.monotonic() < deadline:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                break
            time.sleep(0.01)
        else:
            pytest.fail("the quiet owned-group descendant survived normal completion")
    finally:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


@pytest.mark.skipif(os.name != "posix", reason="POSIX bounded-overflow cleanup control")
def test_continuous_overflow_cannot_renew_owned_group_cleanup_budget(
        tmp_path: Path) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    pid_file = tmp_path / "flooding-git.pid"
    child = (
        "import os,signal,sys; from pathlib import Path; "
        "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
        f"Path({str(pid_file)!r}).write_text(str(os.getpid())); "
        "\nwhile True:\n os.write(1, b'x' * 65536)\n"
    )
    executable = _fake_git(tmp_path / "bin", (
        "if [ \"$1\" = \"--version\" ]; then "
        "printf 'git version 2.45.0\\n'; exit 0; fi\n"
        f"exec {shlex.quote(sys.executable)} -c {shlex.quote(child)}\n"
    ))
    outcome: dict[str, object] = {}

    def invoke() -> None:
        outcome["result"] = git_read.run_git(
            str(target), ("rev-parse", "--show-toplevel"),
            path_value=str(executable.parent), timeout=0.15, output_limit=32,
        )

    started = time.monotonic()
    caller = threading.Thread(target=invoke)
    caller.start()
    caller.join(timeout=2.5)
    pid = int(pid_file.read_text(encoding="ascii")) if pid_file.exists() else None
    try:
        assert not caller.is_alive(), "continuous overflow renewed cleanup indefinitely"
        elapsed = time.monotonic() - started
        assert elapsed < 2.5
        result = outcome["result"]
        assert result.state == "failed" and result.stdout == b""
        assert pid is not None
        with pytest.raises(ProcessLookupError):
            os.kill(pid, 0)
    finally:
        if caller.is_alive() and pid is not None:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            caller.join(timeout=2)


# Declared exception (internal hook): Hook: patched selector.select raises KeyboardInterrupt mid-read; Ctrl-C timing has no deterministic public route. Distinct from cancel-flag test.
@pytest.mark.skipif(os.name != "posix", reason="POSIX group ownership control")
def test_capture_cancellation_kills_and_reaps_its_owned_group(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    marker = tmp_path / "surviving-child"
    ready = tmp_path / "child-ready"
    executable = _fake_git(tmp_path / "bin", (
        f"printf ready > '{ready}'\n"
        f"(/bin/sleep 0.5; printf leaked > '{marker}') &\n"
        "wait\n"
    ))
    original_select = git_read.selectors.DefaultSelector.select

    def cancel_after_child_starts(selector, timeout=None):
        deadline = time.monotonic() + 2.0
        while not ready.exists() and time.monotonic() < deadline:
            time.sleep(0.005)
        assert ready.exists()
        raise KeyboardInterrupt

    monkeypatch.setattr(git_read.selectors.DefaultSelector, "select",
                        cancel_after_child_starts)
    with pytest.raises(KeyboardInterrupt):
        git_read._capture_posix_git([str(executable)], {}, str(tmp_path), 5.0,
                                    1024, 1024)
    monkeypatch.setattr(git_read.selectors.DefaultSelector, "select", original_select)
    time.sleep(0.7)
    assert not marker.exists()


@pytest.mark.skipif(os.name != "posix", reason="POSIX helper cancellation control")
def test_private_cancellation_flag_closes_a_live_git_descendant(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "repo"
    target.mkdir()
    marker = tmp_path / "surviving-child"
    ready = tmp_path / "child-ready"
    executable = _fake_git(tmp_path / "bin", (
        "if [ \"$1\" = \"--version\" ]; then printf 'git version 2.45.0\\n'; exit 0; fi\n"
        f"printf started > '{ready}'\n"
        f"(/bin/sleep 0.5; printf leaked > '{marker}') &\n"
        "wait\n"
    ))
    monkeypatch.setattr(git_read, "_CANCEL_CHECK", lambda: ready.exists())
    result = git_read.run_git(
        str(target), ("rev-parse", "--show-toplevel"),
        path_value=str(executable.parent), timeout=5,
    )
    assert result.state == "failed"
    time.sleep(0.7)
    assert not marker.exists()


# Declared exception (internal hook): Hook: monkeypatches the internal _kill_posix_group to force the EPERM fallback; no public route makes the OS return EPERM for the owned group.
def test_darwin_group_eperm_fallback_requires_exact_bounded_membership(
        monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeProcList:
        argtypes = None
        restype = None

        def __init__(self, byte_count: int, values: tuple[int, ...], error: int = 0):
            self.byte_count = byte_count
            self.values = values
            self.error = error

        def __call__(self, selector, group_id, output, capacity):
            assert selector == 2
            assert capacity == 2 * ctypes.sizeof(ctypes.c_int)
            target = ctypes.cast(output, ctypes.POINTER(ctypes.c_int))
            for index, value in enumerate(self.values):
                target[index] = value
            ctypes.set_errno(self.error)
            return self.byte_count

    class FakeLibrary:
        def __init__(self, proc_listpids):
            self.proc_listpids = proc_listpids

    class MissingLibrary:
        pass

    monkeypatch.setattr(git_read.sys, "platform", "darwin")
    monkeypatch.setattr(git_read.ctypes, "CDLL",
                        lambda path, use_errno: FakeLibrary(current))

    def deny_group_signal(group, sig):
        raise PermissionError(errno.EPERM, "denied")

    monkeypatch.setattr(git_read.os, "killpg", deny_group_signal)

    current = FakeProcList(4, (4321,))
    assert git_read._kill_posix_group(4321, leader_exited=True)
    current = FakeProcList(0, ())
    assert git_read._kill_posix_group(4321, leader_exited=True)
    current = FakeProcList(8, (4321, 4322))
    assert not git_read._kill_posix_group(4321, leader_exited=True)
    current = FakeProcList(4, (4321,), errno.EPERM)
    assert not git_read._kill_posix_group(4321, leader_exited=True)
    current = FakeProcList(0, (), errno.EPERM)
    assert not git_read._kill_posix_group(4321, leader_exited=True)
    current = FakeProcList(3, (4321,))
    assert not git_read._kill_posix_group(4321, leader_exited=True)
    current = FakeProcList(4, (4322,))
    assert not git_read._kill_posix_group(4321, leader_exited=True)
    current = FakeProcList(8, (4321, 4322))
    assert not git_read._kill_posix_group(4321, leader_exited=False)
    current = FakeProcList(4, (4321,))
    monkeypatch.setattr(git_read.sys, "platform", "linux")
    assert not git_read._kill_posix_group(4321, leader_exited=True)
    monkeypatch.setattr(git_read.sys, "platform", "darwin")
    monkeypatch.setattr(git_read.ctypes, "CDLL",
                        lambda path, use_errno: MissingLibrary())
    assert not git_read._kill_posix_group(4321, leader_exited=True)


@pytest.mark.skipif(os.name != "posix", reason="POSIX bounded input control")
def test_read_origin_from_config_uses_fixed_no_target_argv_and_exact_buffer(
        tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    argv_record = tmp_path / "argv"
    body = (
        "if [ \"$1\" = \"--version\" ]; then printf 'git version 2.45.0\\n'; exit 0; fi\n"
        f"printf '%s' \"$*\" > '{argv_record}'\n"
        "IFS= read -r first || exit 31\n"
        "IFS= read -r second || exit 32\n"
        "[ \"$first\" = '[remote \"origin\"]' ] || exit 33\n"
        "[ \"$second\" = ' url = https://example.invalid/repo.git' ] || exit 34\n"
        "if IFS= read -r extra; then exit 35; fi\n"
        "printf 'remote.origin.url\\nhttps://example.invalid/repo.git\\000'\n"
    )
    executable = _fake_git(tmp_path / "bin", body)
    config = b'[remote "origin"]\n url = https://example.invalid/repo.git\n'
    result = git_read.read_origin_from_config(
        config, target=target, path_value=str(executable.parent))
    assert result.state == "completed" and result.returncode == 0
    assert result.stdout == b"https://example.invalid/repo.git\0"
    argv = argv_record.read_text(encoding="utf-8")
    assert "config --file - --no-includes --null --get-regexp" in argv
    assert "-C " not in argv and str(target) not in argv


def test_read_origin_rejects_embedded_nul_and_oversize_before_git_probe(
        tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    marker = tmp_path / "version-probed"
    executable = _fake_git(tmp_path / "bin", (
        f"printf probed >> '{marker}'\n"
        "printf 'git version 2.45.0\\n'\n"
    ))
    for config in (b"[remote]\0origin", b"x" * (git_read.ORIGIN_CONFIG_MAX_BYTES + 1)):
        result = git_read.read_origin_from_config(
            config, target=target, path_value=str(executable.parent))
        assert result.state == "failed" and result.stdout == b""
    assert not marker.exists()


@pytest.mark.skipif(os.name != "posix", reason="POSIX bounded input control")
def test_read_origin_early_exit_cannot_claim_unwritten_input(
        tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    executable = _fake_git(tmp_path / "bin", (
        "if [ \"$1\" = \"--version\" ]; then printf 'git version 2.45.0\\n'; exit 0; fi\n"
        "printf 'remote.origin.url\\nhttps://example.invalid/repo.git\\000'\n"
        "exit 0\n"
    ))
    config = b"x" * git_read.ORIGIN_CONFIG_MAX_BYTES
    result = git_read.read_origin_from_config(
        config, target=target, path_value=str(executable.parent))
    assert result.state == "failed" and result.stdout == b""


@pytest.mark.skipif(os.name != "posix", reason="POSIX bounded input control")
def test_read_origin_discards_include_paths_and_origin_on_parser_refusal(
        tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    executable = _fake_git(tmp_path / "bin", (
        "if [ \"$1\" = \"--version\" ]; then printf 'git version 2.45.0\\n'; exit 0; fi\n"
        "/bin/cat > /dev/null\n"
        "printf 'include.path\\n/private/secret\\000remote.origin.url\\n"
        "https://example.invalid/repo.git\\000'\n"
    ))
    result = git_read.read_origin_from_config(
        b"[remote]\n", target=target, path_value=str(executable.parent))
    assert result.state == "failed" and result.stdout == b""
    assert b"secret" not in result.stdout and result.reason == "origin-config-result-unavailable"


@pytest.mark.skipif(os.name != "posix", reason="POSIX bounded input control")
def test_read_origin_bounds_input_while_draining_both_output_streams(
        tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    executable = _fake_git(tmp_path / "bin", (
        "if [ \"$1\" = \"--version\" ]; then printf 'git version 2.45.0\\n'; exit 0; fi\n"
        "/usr/bin/head -c 20000 /dev/zero | /usr/bin/tr '\\000' o\n"
        "/usr/bin/head -c 10000 /dev/zero | /usr/bin/tr '\\000' e >&2\n"
        "exit 0\n"
    ))
    result = git_read.read_origin_from_config(
        b"x" * git_read.ORIGIN_CONFIG_MAX_BYTES, target=target,
        path_value=str(executable.parent))
    assert result.state == "failed" and result.stdout == b""


@pytest.mark.skipif(shutil.which("git") is None, reason="real Git control unavailable")
def test_read_origin_uses_git_parser_for_quoted_and_continued_values(
        tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    git_path = shutil.which("git")
    assert git_path is not None
    path_value = str(Path(git_path).parent)
    version = git_read.read_version(target, path_value=path_value)
    parsed_version = git_read._parse_version(version.stdout)
    if version.state != "completed" or parsed_version is None \
            or parsed_version < (2, 44, 0):
        pytest.skip("real Git 2.44 or newer is required for the config control")
    for config, expected in (
            (b'[remote "origin"]\n url = "https://example.invalid/path with spaces.git"\n',
             b"https://example.invalid/path with spaces.git\0"),
            (b'[remote "origin"]\n url = https://example.invalid/\\\nrepo.git\n',
             b"https://example.invalid/repo.git\0")):
        result = git_read.read_origin_from_config(
            config, target=target, path_value=path_value)
        assert result.state == "completed" and result.returncode == 0
        assert result.stdout == expected


def test_read_origin_excludes_git_from_every_supplied_root(tmp_path: Path) -> None:
    target = tmp_path / "target"
    source = tmp_path / "source"
    target.mkdir()
    (source / ".git").mkdir(parents=True)
    marker = tmp_path / "version-probed"
    executable = _fake_git(source / "bin", (
        f"printf probed >> '{marker}'\n"
        "printf 'git version 2.45.0\\n'\n"
    ))
    result = git_read.read_origin_from_config(
        b"[remote]\n", target=target, excluded_roots=(source,),
        path_value=str(executable.parent))
    assert result.state == "failed" and result.stdout == b""
    assert not marker.exists()


NATIVE_GIT_FIXTURE = ROOT / "bootstrap/tests/fixtures/native_git_fixture.cs"
NATIVE_CSC = Path(r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe")


@pytest.fixture(scope="session")
def native_git_exe(tmp_path_factory: pytest.TempPathFactory) -> Path:
    if os.name != "nt":
        pytest.skip("native Windows worker controls")
    assert NATIVE_CSC.is_file(), "the authorized Windows compiler is unavailable"
    output = tmp_path_factory.mktemp("cairn-native-git") / "git.exe"
    compiled = subprocess.run(
        [str(NATIVE_CSC), "/nologo", "/out:" + str(output), str(NATIVE_GIT_FIXTURE)],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=30, check=False)
    assert compiled.returncode == 0, compiled.stderr.decode("utf-8", "replace")
    assert output.is_file()
    return output


def _native_git_case(tmp_path: Path, native_git_exe: Path, mode: str,
                     ready_event: str = "", release_event: str = ""):
    case = tmp_path / "case"
    case.mkdir()
    executable = case / "git.exe"
    shutil.copyfile(native_git_exe, executable)
    (case / "control.txt").write_text(
        f"{mode}\nready={ready_event}\nrelease={release_event}\n", encoding="ascii")
    target = tmp_path / "target"
    target.mkdir()
    source = HELPER_PATH.read_bytes()
    git_read.bind_verified_source(source, hashlib.sha256(source).hexdigest())
    git_read._VERSION_CACHE.clear()
    return case, target, executable


def _native_wait_for(path: Path, timeout: float = 5.0) -> None:
    deadline = time.monotonic() + timeout
    event = __import__("threading").Event()
    while not path.exists() and time.monotonic() < deadline:
        event.wait(0.01)
    assert path.is_file(), f"native fixture did not reach {path.name}"


def _native_process_handle(pid: int):
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    kernel.WaitForSingleObject.restype = ctypes.c_uint32
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel.CloseHandle.restype = ctypes.c_int
    kernel.TerminateProcess.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    kernel.TerminateProcess.restype = ctypes.c_int
    handle = kernel.OpenProcess(0x00100001, 0, pid)  # SYNCHRONIZE | PROCESS_TERMINATE
    assert handle, f"could not capture owned child handle for pid {pid}"
    return kernel, handle


def _native_named_event():
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateEventW.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                                    ctypes.c_wchar_p]
    kernel.CreateEventW.restype = ctypes.c_void_p
    kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    kernel.WaitForSingleObject.restype = ctypes.c_uint32
    kernel.SetEvent.argtypes = [ctypes.c_void_p]
    kernel.SetEvent.restype = ctypes.c_int
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel.CloseHandle.restype = ctypes.c_int
    name = "CairnGit-" + uuid.uuid4().hex
    handle = kernel.CreateEventW(None, 1, 0, name)
    assert handle, "could not create owned fixture synchronization event"
    return kernel, handle, name


@pytest.fixture
def native_pipe_threads(monkeypatch: pytest.MonkeyPatch):
    records = []
    if os.name == "nt":
        original = threading.Thread

        class RecordingThread(original):
            def __init__(self, *args, **kwargs):
                target = kwargs.get("target", args[0] if args else None)
                super().__init__(*args, **kwargs)
                if getattr(target, "__name__", "") in {"drain", "transmit"}:
                    records.append(self)

        monkeypatch.setattr(threading, "Thread", RecordingThread)
    yield records
    assert all(not thread.is_alive() for thread in records), \
        "a native helper reader or writer thread remained alive after the call"


def _native_wait_handle(kernel, handle, timeout_ms: int) -> int:
    return int(kernel.WaitForSingleObject(handle, timeout_ms))


@pytest.mark.skipif(os.name != "nt", reason="native Windows worker controls")
def test_native_git_fixture_compiles_and_runs_owned_control(
        tmp_path: Path, native_git_exe: Path) -> None:
    case = tmp_path / "smoke"
    case.mkdir()
    executable = case / "git.exe"
    shutil.copyfile(native_git_exe, executable)
    (case / "control.txt").write_text("ordinary\nready=\nrelease=\n", encoding="ascii")
    completed = subprocess.run(
        [str(executable), "--version"], cwd=case, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5, check=False)
    assert completed.returncode == 0
    assert completed.stdout == b"git version 2.53.0\n"
    assert (case / "launches.txt").read_text(encoding="utf-8").strip() == "--version"

    kernel, ready, ready_name = _native_named_event()
    _release_kernel, release, release_name = _native_named_event()
    direct_root = tmp_path / "direct"
    direct_root.mkdir()
    case, _target, executable = _native_git_case(
        direct_root, native_git_exe, "quiet-descendant", ready_name, release_name)
    direct = subprocess.Popen(
        [str(executable), "rev-parse"], cwd=case, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, close_fds=True)
    assert direct.stdout is not None and direct.stderr is not None
    output: dict[str, bytes] = {}
    stdout_done = threading.Event()
    stderr_done = threading.Event()

    def collect(stream, key: str, done: threading.Event) -> None:
        try:
            output[key] = stream.read()
        finally:
            done.set()

    stdout_reader = threading.Thread(target=collect,
                                     args=(direct.stdout, "stdout", stdout_done), daemon=True)
    stderr_reader = threading.Thread(target=collect,
                                     args=(direct.stderr, "stderr", stderr_done), daemon=True)
    stdout_reader.start()
    stderr_reader.start()
    child_kernel = None
    child_handle = None
    try:
        assert _native_wait_handle(kernel, ready, 5000) == 0
        child_pid = int((case / "child.pid").read_text(encoding="ascii"))
        child_kernel, child_handle = _native_process_handle(child_pid)
        assert _native_wait_handle(child_kernel, child_handle, 0) == 258
        _release_kernel.SetEvent(release)
        assert direct.wait(timeout=5) == 0
        assert _native_wait_handle(child_kernel, child_handle, 0) == 258
        stdout_closed = stdout_done.wait(2)
        stderr_closed = stderr_done.wait(2)
        assert stdout_closed and stderr_closed, \
            "quiet fixture descendant retained an original captured pipe"
        assert output["stdout"] == b"true\r\n" and output["stderr"] == b""
    finally:
        if child_kernel is not None and child_handle:
            if _native_wait_handle(child_kernel, child_handle, 0) == 258:
                child_kernel.TerminateProcess(child_handle, 1)
                _native_wait_handle(child_kernel, child_handle, 5000)
            child_kernel.CloseHandle(child_handle)
        if direct.poll() is None:
            direct.kill()
            direct.wait(timeout=5)
        for stream in (direct.stdin, direct.stdout, direct.stderr):
            if stream is not None:
                stream.close()
        stdout_reader.join(5)
        stderr_reader.join(5)
        kernel.CloseHandle(ready)
        _release_kernel.CloseHandle(release)


@pytest.mark.skipif(os.name != "nt", reason="native Windows worker controls")
def test_native_worker_positive_version_and_closed_input_eof(
        tmp_path: Path, native_git_exe: Path, native_pipe_threads) -> None:
    case, target, _executable = _native_git_case(tmp_path, native_git_exe, "ordinary")
    version = git_read.read_version(target, path_value=str(case))
    assert version.state == "completed" and version.stdout == b"git version 2.53.0\n"
    result = git_read.run_git(target, ("rev-parse", "--is-inside-work-tree"),
                              path_value=str(case), timeout=2)
    assert result.state == "completed" and result.returncode == 0
    assert result.stdout == b"true\r\n"
    assert (case / "ordinary-eof.txt").read_text(encoding="ascii") == "eof"
    assert "--version" in (case / "launches.txt").read_text(encoding="utf-8")


@pytest.mark.skipif(os.name != "nt", reason="native Windows worker controls")
def test_native_worker_origin_config_writes_exact_buffer_then_eof(
        tmp_path: Path, native_git_exe: Path, native_pipe_threads) -> None:
    case, target, _executable = _native_git_case(tmp_path, native_git_exe, "ordinary")
    config = b'[remote "origin"]\n url = https://example.invalid/repo.git\n'
    result = git_read.read_origin_from_config(
        config, target=target, path_value=str(case), timeout=3)
    assert result.state == "completed" and result.returncode == 0
    assert result.stdout == b"https://example.invalid/repo.git\0"
    assert (case / "config-eof.txt").read_text(encoding="ascii") == str(len(config))


@pytest.mark.skipif(os.name != "nt", reason="native Windows worker controls")
@pytest.mark.parametrize(("mode", "marker"), [
    ("stdout-flood", "stdout"), ("stderr-flood", "stderr"),
])
def test_native_worker_rejects_each_output_cap_overflow(
        mode: str, marker: str, tmp_path: Path, native_git_exe: Path,
        native_pipe_threads) -> None:
    case, target, _executable = _native_git_case(tmp_path, native_git_exe, mode)
    result = git_read.read_origin_from_config(
        b'[remote "origin"]\n url = https://example.invalid/repo.git\n',
        target=target, path_value=str(case), timeout=2)
    assert result.state == "failed" and result.stdout == b""
    assert (case / "ready.txt").read_text(encoding="ascii") == marker


@pytest.mark.skipif(os.name != "nt", reason="native Windows worker controls")
def test_native_worker_version_hang_is_not_absence_or_empty_success(
        tmp_path: Path, native_git_exe: Path, native_pipe_threads) -> None:
    case, target, _executable = _native_git_case(tmp_path, native_git_exe, "version-hang")
    result = git_read.read_origin_from_config(
        b'[remote "origin"]\n url = https://example.invalid/repo.git\n',
        target=target, path_value=str(case), timeout=1)
    assert result.state == "failed" and result.stdout == b""
    assert (case / "ready.txt").read_text(encoding="ascii") == "version"


@pytest.mark.skipif(os.name != "nt", reason="native Windows worker controls")
def test_native_worker_config_hang_is_not_absence_or_empty_success(
        tmp_path: Path, native_git_exe: Path, native_pipe_threads) -> None:
    case, target, _executable = _native_git_case(tmp_path, native_git_exe, "config-hang")
    result = git_read.read_origin_from_config(
        b'[remote "origin"]\n url = https://example.invalid/repo.git\n',
        target=target, path_value=str(case), timeout=1)
    assert result.state == "failed" and result.stdout == b""
    assert (case / "ready.txt").read_text(encoding="ascii") == "config"


@pytest.mark.skipif(os.name != "nt", reason="native Windows worker controls")
def test_native_worker_early_config_exit_cannot_claim_unwritten_input(
        tmp_path: Path, native_git_exe: Path, native_pipe_threads) -> None:
    case, target, _executable = _native_git_case(
        tmp_path, native_git_exe, "early-config-exit")
    config = b"x" * git_read.ORIGIN_CONFIG_MAX_BYTES
    result = git_read.read_origin_from_config(
        config, target=target, path_value=str(case), timeout=3)
    assert result.state == "failed" and result.stdout == b""
    assert (case / "ready.txt").read_text(encoding="ascii") == "early-config"


@pytest.mark.skipif(os.name != "nt", reason="native Windows worker controls")
def test_native_worker_timeout_kills_pipe_holding_git_descendant(
        tmp_path: Path, native_git_exe: Path, native_pipe_threads) -> None:
    kernel, ready, ready_name = _native_named_event()
    case, target, _executable = _native_git_case(
        tmp_path, native_git_exe, "hold-pipes", ready_name)
    outcome: dict[str, object] = {}

    def invoke() -> None:
        outcome["result"] = git_read.run_git(
            target, ("rev-parse", "--is-inside-work-tree"),
            path_value=str(case), timeout=1)

    caller = threading.Thread(target=invoke)
    caller.start()
    process_kernel = None
    handle = None
    try:
        assert _native_wait_handle(kernel, ready, 5000) == 0
        pid = int((case / "child.pid").read_text(encoding="ascii"))
        process_kernel, handle = _native_process_handle(pid)
        assert _native_wait_handle(process_kernel, handle, 0) == 258  # WAIT_TIMEOUT while owned
        caller.join(8)
        assert not caller.is_alive()
        result = outcome["result"]
        assert result.state == "failed" and result.stdout == b""
        assert _native_wait_handle(process_kernel, handle, 5000) == 0  # WAIT_OBJECT_0
    finally:
        if process_kernel is not None and handle:
            if _native_wait_handle(process_kernel, handle, 0) == 258:
                process_kernel.TerminateProcess(handle, 1)
                _native_wait_handle(process_kernel, handle, 5000)
            process_kernel.CloseHandle(handle)
        kernel.CloseHandle(ready)
        caller.join(5)


@pytest.mark.skipif(os.name != "nt", reason="native Windows worker controls")
def test_native_worker_job_close_kills_quiet_live_descendant(
        tmp_path: Path, native_git_exe: Path, native_pipe_threads) -> None:
    kernel, ready, ready_name = _native_named_event()
    _release_kernel, release, release_name = _native_named_event()
    case, target, _executable = _native_git_case(
        tmp_path, native_git_exe, "quiet-descendant", ready_name, release_name)
    outcome: dict[str, object] = {}

    def invoke() -> None:
        outcome["result"] = git_read.run_git(
            target, ("rev-parse", "--is-inside-work-tree"),
            path_value=str(case), timeout=4)

    caller = threading.Thread(target=invoke)
    caller.start()
    process_kernel = None
    handle = None
    try:
        assert _native_wait_handle(kernel, ready, 5000) == 0
        pid = int((case / "child.pid").read_text(encoding="ascii"))
        process_kernel, handle = _native_process_handle(pid)
        assert _native_wait_handle(process_kernel, handle, 0) == 258
        _release_kernel.SetEvent(release)
        caller.join(8)
        assert not caller.is_alive()
        result = outcome["result"]
        assert result.state == "completed" and result.stdout == b"true\r\n", result
        assert _native_wait_handle(process_kernel, handle, 5000) == 0
    finally:
        if process_kernel is not None and handle:
            if _native_wait_handle(process_kernel, handle, 0) == 258:
                process_kernel.TerminateProcess(handle, 1)
                _native_wait_handle(process_kernel, handle, 5000)
            process_kernel.CloseHandle(handle)
        kernel.CloseHandle(ready)
        _release_kernel.CloseHandle(release)
        caller.join(5)


@pytest.mark.skipif(os.name != "nt", reason="native Windows worker controls")
def test_native_worker_job_setup_failure_precedes_git_launch(
        tmp_path: Path, native_git_exe: Path, native_pipe_threads) -> None:
    case, target, _executable = _native_git_case(tmp_path, native_git_exe, "ordinary")
    positive = git_read.read_version(target, path_value=str(case))
    assert positive.state == "completed" and positive.stdout == b"git version 2.53.0\n"

    source = HELPER_PATH.read_bytes()
    old = (b"kernel.SetInformationJobObject(handle, 9, C.byref(limits), C.sizeof(limits))")
    new = (b"kernel.SetInformationJobObject(handle, 0x7fffffff, C.byref(limits), "
           b"C.sizeof(limits))")
    assert old in source
    mutated = source.replace(old, new, 1)
    git_read.bind_verified_source(mutated, hashlib.sha256(mutated).hexdigest())
    git_read._VERSION_CACHE.clear()
    (case / "launches.txt").unlink()
    result = git_read.read_version(target, path_value=str(case))
    assert result.state == "failed" and result.stdout == b""
    assert not (case / "launches.txt").exists()


@pytest.mark.skipif(os.name != "nt", reason="native Windows worker controls")
def test_native_worker_cancellation_cleans_worker_and_owned_threads(
        tmp_path: Path, native_git_exe: Path, monkeypatch: pytest.MonkeyPatch,
        native_pipe_threads) -> None:
    case, target, _executable = _native_git_case(tmp_path, native_git_exe, "version-hang")
    original_popen = git_read.subprocess.Popen
    owned_workers = []

    def record_popen(*args, **kwargs):
        process = original_popen(*args, **kwargs)
        owned_workers.append(process)
        return process

    def interrupt_supervision(_seconds: float) -> None:
        _native_wait_for(case / "ready.txt", timeout=5)
        raise KeyboardInterrupt

    monkeypatch.setattr(git_read.subprocess, "Popen", record_popen)
    monkeypatch.setattr(git_read.time, "sleep", interrupt_supervision)
    try:
        with pytest.raises(KeyboardInterrupt):
            git_read.read_version(target, path_value=str(case))
        assert (case / "ready.txt").read_text(encoding="ascii") == "version"
        assert owned_workers, "the native worker process was not created"
        assert all(process.poll() is not None for process in owned_workers), \
            "cancellation propagated before the isolated worker was stopped"
        assert native_pipe_threads and all(not thread.is_alive()
                                           for thread in native_pipe_threads), \
            "cancellation propagated with a worker reader or writer thread alive"
    finally:
        for process in owned_workers:
            if process.poll() is None:
                process.kill()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
        for thread in native_pipe_threads:
            thread.join(5)
        for process in owned_workers:
            for stream in (process.stdin, process.stdout, process.stderr):
                if stream is not None:
                    try:
                        stream.close()
                    except OSError:
                        pass
