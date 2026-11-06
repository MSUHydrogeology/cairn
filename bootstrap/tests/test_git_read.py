"""Component controls for the mirrored bounded Git read implementation."""
from __future__ import annotations

import hashlib
import importlib.util
import os
import stat
import time
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
HELPER_PATH = ROOT / "templates/skills/_lib/git_read.py"
SPEC = importlib.util.spec_from_file_location("_cairn_test_git_read", HELPER_PATH)
assert SPEC is not None and SPEC.loader is not None
git_read = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(git_read)


def _fake_git(directory: Path, body: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    exe = directory / "git"
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
    result = git_read.run_git(str(target), ("status", "--porcelain=v1"),
                              path_value=str(executable.parent))
    assert result.state == "completed" and result.returncode == 0
    argv = marker.read_text(encoding="utf-8")
    assert "filter.demo.clean=" in argv
    assert "filter.demo.smudge=" in argv
    assert "filter.demo.process=" in argv
    assert "filter.demo.required=false" in argv


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

