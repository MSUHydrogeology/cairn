"""`upgrade --remove-retired`: the engine's list of retired files, and what it removes.

Cairn deletes a project's copy of a file it stopped shipping only when two things
agree: the path is on the engine's own list (`_RETIRED_INSTALLS`), and the bytes
are a version Cairn shipped (a SHA-256 digest on that row). The project supplies
the file and the lockfile, so neither can add a name or vouch for the bytes.

The tests drive the real `scaffold.py` entry point over a real install, as
`test_agreement_retired.py` does. A project from an older Cairn is modelled by
adding the former records and files to a fresh scratch install; the bytes come
from Cairn's own git history, by the blob ids the list carries.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap._scaffold import config as C  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
EMPTY_FILE_DIGEST = hashlib.sha256(b"").hexdigest()
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")


# ---------------------------------------------------------------------------
# The list
# ---------------------------------------------------------------------------

def _shipped_destinations() -> set[str]:
    """Every destination the running tree can install, optional files included."""
    shipped = {dst for _src, dst, _verbatim in s.install_manifest(modules=None)}
    shipped.update(dst for _src, dst, _axis, _values in C._OPTIONAL_TEMPLATES)
    return shipped


def _row_problems(rows: object) -> list[str]:
    """What is wrong with a list of retired rows; empty when it is sound."""
    shipped = _shipped_destinations()
    shipped_sources = {src for src, _dst, _verbatim in s.install_manifest(modules=None)}
    problems: list[str] = []
    seen: set[str] = set()
    for src, dst, verbatim, digests in rows:  # type: ignore[attr-defined]
        if (ROOT / "templates" / src).exists() or src in shipped_sources:
            problems.append(f"{dst}: source {src} is still shipped")
        if dst in shipped:
            problems.append(f"{dst}: destination is still shipped")
        if dst in seen:
            problems.append(f"{dst}: listed twice")
        seen.add(dst)
        if not isinstance(verbatim, bool):
            problems.append(f"{dst}: verbatim is not a boolean")
        if not digests:
            problems.append(f"{dst}: no digest")
        for digest, commit, blob in digests:
            if not HEX64.fullmatch(digest):
                problems.append(f"{dst}: {digest!r} is not 64 lowercase hex")
            if digest == EMPTY_FILE_DIGEST:
                problems.append(f"{dst}: a digest is the empty file's")
            if not HEX40.fullmatch(commit) or not HEX40.fullmatch(blob):
                problems.append(f"{dst}: provenance is not full object ids")
    return problems


def test_no_retired_row_is_still_shipped_and_every_row_has_digests() -> None:
    assert _row_problems(C._RETIRED_INSTALLS) == []
    assert len(C._RETIRED_INSTALLS) > 0


def test_the_row_check_flags_a_shipped_row_and_a_renamed_template() -> None:
    # Instrument check: the same function must see both planted defects.
    src, dst, verbatim = s.install_manifest(modules=None)[0]
    digest = ("a" * 64, "b" * 40, "c" * 40)
    shipped = (src, dst, verbatim, (digest,))
    assert _row_problems((shipped,)), "a row for a shipped file went unnoticed"
    renamed = ("modules/default-on/a-template-nobody-ships.md", dst, False, (digest,))
    assert any("destination is still shipped" in p for p in _row_problems((renamed,)))
    empty = ("modules/default-on/gone.md", "dev/gone.md", False,
             ((EMPTY_FILE_DIGEST, "b" * 40, "c" * 40),))
    assert _row_problems((empty,)), "the empty file's digest went unnoticed"


def _git_blob(blob: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "blob", blob],
        capture_output=True, check=False, timeout=60,
    )


def test_every_retired_digest_recomputes_from_git_history() -> None:
    # Fails, never skips, when a blob is missing: a skip would hide a lost
    # object for good. The commit id is a label and is never read, so a
    # re-anchor that rewrites commit ids cannot turn this red.
    wrong: list[str] = []
    for _src, dst, _verbatim, digests in C._RETIRED_INSTALLS:
        for digest, _commit, blob in digests:
            result = _git_blob(blob)
            if result.returncode != 0:
                wrong.append(f"{dst}: git has no blob {blob}")
            elif hashlib.sha256(result.stdout).hexdigest() != digest:
                wrong.append(f"{dst}: blob {blob} does not hash to {digest}")
    assert wrong == []


# ---------------------------------------------------------------------------
# The git question: is the project's last commit holding exactly these bytes?
# ---------------------------------------------------------------------------

import os  # noqa: E402
import shutil  # noqa: E402
import stat  # noqa: E402
import time  # noqa: E402

from bootstrap._scaffold import security as SEC  # noqa: E402
from bootstrap._scaffold import upgrade as U  # noqa: E402

posix_only = pytest.mark.skipif(
    os.name == "nt", reason="the stand-in git programs here are shell scripts")


def _reset_git_floor(monkeypatch: pytest.MonkeyPatch) -> None:
    """Forget the once-per-process `git --version` answer."""
    monkeypatch.setattr(U._committed_copy_matches, "git_floor_met", None, raising=False)


def _stand_in_git(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *,
                  version: str = "git version 2.54.0 (Apple Git-157)",
                  cat_file: str = "printf '%s' \"$DATA\"",
                  name: str = "standin") -> Path:
    """Put a fake `git` first on PATH; it logs every call and answers by the script.

    Each call writes `<n>.argv` and `<n>.env` under the returned folder."""
    log = tmp_path / name / "log"
    log.mkdir(parents=True)
    bindir = tmp_path / name / "bin"
    bindir.mkdir()
    script = bindir / "git"
    script.write_text(
        "#!/bin/sh\n"
        f"n=$(ls '{log}'/*.argv 2>/dev/null | wc -l | tr -d ' ')\n"
        f"for a in \"$@\"; do printf '%s\\n' \"$a\"; done > '{log}'/$n.argv\n"
        f"env > '{log}'/$n.env\n"
        "case \"$1\" in\n"
        f"  --version) printf '%s\\n' '{version}'; exit 0;;\n"
        "esac\n"
        f"{cat_file}\n",
        encoding="utf-8",
    )
    script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    _reset_git_floor(monkeypatch)
    return log


def _logged_calls(log: Path) -> list[list[str]]:
    calls = []
    for argv in sorted(log.glob("*.argv"), key=lambda p: int(p.stem)):
        calls.append(argv.read_text(encoding="utf-8").splitlines())
    return calls


@posix_only
def test_committed_copy_matches_runs_git_with_fixed_overrides_and_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DATA", "payload")
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "elsewhere"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(tmp_path / "gitconfig"))
    monkeypatch.setenv("git_ssh_command", "lower-case spelling")
    monkeypatch.setenv("GIT_NO_LAZY_FETCH", "0")
    log = _stand_in_git(tmp_path, monkeypatch)
    assert U._committed_copy_matches(project, "scripts/x.py", b"payload") is True
    calls = _logged_calls(log)
    assert calls[0] == ["--version"]
    assert calls[1] == [
        "-C", str(project),
        "-c", "core.fsmonitor=false",
        "-c", f"core.hooksPath={os.devnull}",
        "-c", "core.useReplaceRefs=false",
        "cat-file", "blob", "HEAD:./scripts/x.py",
    ]
    for number in (0, 1):
        env = dict(
            line.split("=", 1)
            for line in (log / f"{number}.env").read_text(encoding="utf-8").splitlines()
            if "=" in line
        )
        git_vars = {k: v for k, v in env.items() if k.upper().startswith("GIT_")}
        assert git_vars == {
            "GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
        }, f"call {number} saw {git_vars}"


@posix_only
def test_committed_copy_matches_passes_only_on_exactly_the_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DATA", "payload")
    _stand_in_git(tmp_path, monkeypatch)
    assert U._committed_copy_matches(project, "a.py", b"payload") is True
    assert U._committed_copy_matches(project, "a.py", b"payloa") is False
    assert U._committed_copy_matches(project, "a.py", b"payload2") is False
    assert U._committed_copy_matches(project, "a.py", b"") is False


@posix_only
def test_committed_copy_matches_refuses_a_name_that_is_not_a_plain_project_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DATA", "payload")
    log = _stand_in_git(tmp_path, monkeypatch)
    for bad in ("", "/etc/passwd", "../x", "a/../b", "a//b", "a\nb", "a\0b", "./a", "a/."):
        assert U._committed_copy_matches(project, bad, b"payload") is False, bad
    assert _logged_calls(log) in ([], [["--version"]])


@pytest.mark.skipif(shutil.which("git") is None, reason="needs a real git")
def test_committed_copy_matches_ignores_a_replace_ref(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _reset_git_floor(monkeypatch)
    project = tmp_path / "project"
    project.mkdir()

    def git(*args: str, data: bytes | None = None) -> str:
        return subprocess.run(
            ["git", "-C", str(project), "-c", "user.name=t", "-c", "user.email=t@t",
             *args], input=data, capture_output=True, check=True,
        ).stdout.decode().strip()

    git("init", "-q")
    (project / "f.py").write_bytes(b"committed\n")
    git("add", "f.py")
    git("commit", "-q", "-m", "x")
    genuine = git("rev-parse", "HEAD:f.py")
    forged = git("hash-object", "-w", "--stdin", data=b"forged\n")
    git("replace", genuine, forged)
    assert git("cat-file", "blob", "HEAD:f.py") == "forged", "the replace ref must be live"
    if not U._committed_copy_matches(project, "f.py", b"committed\n"):
        pytest.skip("this git is older than the 2.45.0 floor")
    assert U._committed_copy_matches(project, "f.py", b"forged\n") is False


@posix_only
def test_a_git_that_does_not_finish_or_prints_too_much_keeps_the_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DATA", "payload")
    monkeypatch.setattr(U, "_GIT_TIMEOUT_SECONDS", 0.5)
    # Control: git prints exactly the bytes at once.
    _stand_in_git(tmp_path, monkeypatch, name="prompt")
    assert U._committed_copy_matches(project, "a.py", b"payload") is True
    # Sleeps, then prints exactly the bytes: too late.
    _stand_in_git(tmp_path, monkeypatch, name="slow",
                  cat_file="exec sleep 5; printf '%s' \"$DATA\"")
    started = time.monotonic()
    assert U._committed_copy_matches(project, "a.py", b"payload") is False
    assert time.monotonic() - started < 4, "the call must not wait for a hung git"
    # Sleeps in a child that outlives git and keeps the pipe open.
    _stand_in_git(tmp_path, monkeypatch, name="orphan",
                  cat_file="sleep 5 & printf '%s' \"$DATA\"; wait")
    started = time.monotonic()
    assert U._committed_copy_matches(project, "a.py", b"payload") is False
    assert time.monotonic() - started < 4
    # Prints without end: cut at one byte past the copy, well before the timeout.
    monkeypatch.setattr(U, "_GIT_TIMEOUT_SECONDS", 30)
    _stand_in_git(tmp_path, monkeypatch, name="endless", cat_file="yes payload")
    started = time.monotonic()
    assert U._committed_copy_matches(project, "a.py", b"payload") is False
    assert time.monotonic() - started < 4, "the output was not cut off"
    monkeypatch.setattr(U, "_GIT_TIMEOUT_SECONDS", 0.5)
    # Prints one byte more than the copy and stops.
    _stand_in_git(tmp_path, monkeypatch, name="plusone",
                  cat_file="printf '%s' \"${DATA}x\"")
    assert U._committed_copy_matches(project, "a.py", b"payload") is False


def _version_answer(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, version: str) -> tuple[bool, Path]:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DATA", "payload")
    log = _stand_in_git(tmp_path, monkeypatch, version=version)
    return U._committed_copy_matches(project, "a.py", b"payload"), log


@posix_only
def test_a_git_with_an_apple_suffix_at_2_54_0_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    ok, log = _version_answer(tmp_path, monkeypatch, "git version 2.54.0 (Apple Git-157)")
    assert ok is True and len(_logged_calls(log)) == 2


@posix_only
def test_a_git_with_an_apple_suffix_at_2_44_9_keeps_the_file_and_runs_no_cat_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    ok, log = _version_answer(tmp_path, monkeypatch, "git version 2.44.9 (Apple Git-1)")
    assert ok is False and _logged_calls(log) == [["--version"]]


@posix_only
@pytest.mark.parametrize("version, expected", [
    ("git version 2.45.0", True),
    ("git version 2.45.0.windows.1", True),
    ("git version 2.44.0", False),
    ("git version 1.99.99", False),
    ("git version 3.0.0", True),
    ("git version 2.100.0", True),
    ("2.54.0", False),
    ("", False),
    ("git version", False),
    ("git version two.five.zero", False),
])
def test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, version: str, expected: bool,
) -> None:
    ok, log = _version_answer(tmp_path, monkeypatch, version)
    assert ok is expected
    assert (len(_logged_calls(log)) == 2) is expected, _logged_calls(log)


@posix_only
def test_git_version_output_longer_than_the_cap_is_unreadable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    ok, log = _version_answer(
        tmp_path, monkeypatch, "git version 2.54.0 " + "x" * 5000)
    assert ok is False and _logged_calls(log) == [["--version"]]


@posix_only
def test_a_git_that_fails_or_is_missing_keeps_the_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DATA", "payload")
    _stand_in_git(tmp_path, monkeypatch, cat_file="exit 128")
    assert U._committed_copy_matches(project, "a.py", b"payload") is False
    _stand_in_git(tmp_path, monkeypatch, name="failing-output",
                  cat_file="printf '%s' \"$DATA\"; exit 1")
    assert U._committed_copy_matches(project, "a.py", b"payload") is False
    monkeypatch.setenv("PATH", str(tmp_path / "no-such-folder"))
    _reset_git_floor(monkeypatch)
    assert U._committed_copy_matches(project, "a.py", b"payload") is False


@posix_only
def test_git_version_is_read_once_per_process(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DATA", "payload")
    log = _stand_in_git(tmp_path, monkeypatch)
    for _ in range(3):
        assert U._committed_copy_matches(project, "a.py", b"payload") is True
    versions = [c for c in _logged_calls(log) if c == ["--version"]]
    assert len(versions) == 1 and len(_logged_calls(log)) == 4


# ---------------------------------------------------------------------------
# The delete: one guarded leaf, through folder handles where the platform has them
# ---------------------------------------------------------------------------

BODY = b"print('shipped')\n"
HANDLES = "folder handles"
BY_PATH = "by path"
handles_only = pytest.mark.skipif(
    not (hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")
         and {os.open, os.unlink, os.rmdir, os.stat} <= os.supports_dir_fd),
    reason="this platform has no folder-relative unlink (dir_fd); the by-path "
           "branch runs instead and the handle tests cannot",
)


@pytest.fixture(params=[HANDLES, BY_PATH])
def branch(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> str:
    """Run a test over both removal branches.

    `by path` is forced on POSIX by hiding `rmdir` from `os.supports_dir_fd`."""
    if request.param == BY_PATH:
        monkeypatch.setattr(os, "supports_dir_fd", set(os.supports_dir_fd) - {os.rmdir})
    elif not (hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")
              and {os.open, os.unlink, os.rmdir, os.stat} <= os.supports_dir_fd):
        pytest.skip("no folder-relative unlink on this platform")
    return request.param


def _project_file(tmp_path: Path, rel: str = "a/b/tool.py") -> tuple[Path, Path]:
    target = (tmp_path / "project").resolve()
    path = target / rel
    path.parent.mkdir(parents=True)
    path.write_bytes(BODY)
    return target, path


def _removal(path: Path, target: Path, expected: bytes = BODY, **kwargs: object) -> str:
    try:
        removed = SEC._remove_unchanged_file(path, target, expected, **kwargs)
    except SEC.ScaffoldSecurityError:
        return "refused"
    return "removed" if removed else "kept"


def test_an_unchanged_file_is_removed_and_its_emptied_folder_with_it(
    tmp_path: Path, branch: str,
) -> None:
    target, path = _project_file(tmp_path)
    assert _removal(path, target) == "removed"
    assert not os.path.lexists(path)
    assert not path.parent.exists(), "the file's own folder was left empty"
    assert path.parent.parent.is_dir(), "the folder above the file's own is never removed"
    assert target.is_dir()


def test_confirming_that_nothing_is_at_the_name_removes_nothing(
    tmp_path: Path, branch: str,
) -> None:
    target, path = _project_file(tmp_path)
    assert _removal(path, target, None) == "kept"
    assert path.read_bytes() == BODY and path.parent.is_dir()
    path.unlink()
    assert _removal(path, target, None) == "removed"
    assert path.parent.is_dir(), "a confirmation never removes the emptied folder"
    shutil.rmtree(path.parent)
    assert _removal(path, target, None) == "removed"
    path.parent.mkdir()
    path.mkdir()
    assert _removal(path, target, None) == "kept"
    assert path.is_dir()


def test_an_emptied_folder_goes_and_a_non_empty_one_stays(
    tmp_path: Path, branch: str,
) -> None:
    target, path = _project_file(tmp_path)
    (path.parent / "keep.txt").write_text("mine", encoding="utf-8")
    sub = path.parent / "nested"
    sub.mkdir()
    (sub / "deep.txt").write_text("mine too", encoding="utf-8")
    assert _removal(path, target) == "removed"
    assert not path.exists()
    assert (path.parent / "keep.txt").read_text(encoding="utf-8") == "mine"
    assert (sub / "deep.txt").is_file(), "nothing below the file's folder is touched"
    # A file in the project folder itself never takes the project folder with it.
    (target / "top.py").write_bytes(BODY)
    assert _removal(target / "top.py", target) == "removed"
    assert target.is_dir()


def test_a_missing_file_counts_as_removed_and_a_folder_in_its_place_is_not(
    tmp_path: Path, branch: str,
) -> None:
    target, path = _project_file(tmp_path)
    path.unlink()
    assert _removal(path, target) == "removed"
    target, path = _project_file(tmp_path / "second")
    path.unlink()
    path.mkdir()
    assert _removal(path, target) in ("kept", "refused")
    assert path.is_dir()


def test_a_link_a_linked_folder_and_a_folder_in_place_are_kept(
    tmp_path: Path, branch: str,
) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    victim = outside / "tool.py"
    victim.write_bytes(BODY)
    # a link at the name
    target, path = _project_file(tmp_path / "one")
    path.unlink()
    path.symlink_to(victim)
    assert _removal(path, target) in ("kept", "refused")
    assert victim.read_bytes() == BODY and path.is_symlink()
    # a linked folder above the name
    target, path = _project_file(tmp_path / "two")
    shutil.rmtree(path.parent)
    path.parent.symlink_to(outside, target_is_directory=True)
    assert _removal(path, target) in ("kept", "refused")
    assert victim.read_bytes() == BODY and path.parent.is_symlink()
    # a folder in place
    target, path = _project_file(tmp_path / "three")
    path.unlink()
    path.mkdir()
    (path / "inner").write_text("x", encoding="utf-8")
    assert _removal(path, target) in ("kept", "refused")
    assert (path / "inner").is_file()
    # a dangling link at the name
    target, path = _project_file(tmp_path / "four")
    path.unlink()
    path.symlink_to(tmp_path / "nowhere")
    assert _removal(path, target) in ("kept", "refused")
    assert path.is_symlink()
    # a name that is not inside the project
    target, _ = _project_file(tmp_path / "five")
    assert _removal(victim, target) == "refused"
    assert victim.read_bytes() == BODY


def test_bytes_changed_between_the_decision_and_the_removal_are_kept(
    tmp_path: Path, branch: str,
) -> None:
    target, path = _project_file(tmp_path)
    path.write_bytes(BODY + b"# edited\n")
    assert _removal(path, target) == "kept"
    assert path.read_bytes() == BODY + b"# edited\n"
    assert path.parent.is_dir()
    path.write_bytes(b"")
    assert _removal(path, target) == "kept"


def test_a_file_replaced_between_the_read_and_the_removal_is_kept(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, branch: str,
) -> None:
    target, path = _project_file(tmp_path)
    real_fstat = os.fstat
    swapped: list[bool] = []

    def replace_the_file_just_after_it_is_opened(fd: int) -> os.stat_result:
        info = real_fstat(fd)
        if not swapped:
            swapped.append(True)
            replacement = path.with_name("replacement")
            replacement.write_bytes(b"the project's own work\n")
            os.replace(replacement, path)
        return info

    monkeypatch.setattr(SEC.os, "fstat", replace_the_file_just_after_it_is_opened)
    assert _removal(path, target) == "kept"
    assert swapped, "the swap hook must have run"
    assert path.read_bytes() == b"the project's own work\n"


def test_the_removal_is_confirmed_by_looking_at_the_name_again(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, branch: str,
) -> None:
    target, path = _project_file(tmp_path)

    def does_nothing(*_args: object, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr(SEC.os, "unlink", does_nothing)
    if branch == HANDLES:
        monkeypatch.setattr(os, "supports_dir_fd", set(os.supports_dir_fd) | {does_nothing})
    assert _removal(path, target) == "kept"
    assert path.read_bytes() == BODY


@pytest.mark.skipif(os.name == "nt" or os.geteuid() == 0,
                    reason="a read-only folder stops unlink only for a non-root user on POSIX")
def test_a_folder_that_refuses_the_removal_keeps_the_file(
    tmp_path: Path, branch: str,
) -> None:
    target, path = _project_file(tmp_path)
    path.parent.chmod(0o555)
    try:
        assert _removal(path, target) == "kept"
        assert path.read_bytes() == BODY
    finally:
        path.parent.chmod(0o755)


@handles_only
def test_a_parent_swapped_for_a_link_between_the_check_and_the_removal_leaves_the_outside_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    target, path = _project_file(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    victim = outside / "tool.py"
    victim.write_bytes(BODY)
    real_guard = SEC._assert_safe_write
    swapped: list[bool] = []

    def swap_after_the_check(dst: Path, tgt: Path) -> None:
        real_guard(dst, tgt)
        if not swapped:
            swapped.append(True)
            moved = path.parent.with_name("b-moved")
            os.rename(path.parent, moved)
            path.parent.symlink_to(outside, target_is_directory=True)

    monkeypatch.setattr(SEC, "_assert_safe_write", swap_after_the_check)
    assert _removal(path, target) in ("kept", "refused")
    assert swapped
    assert victim.read_bytes() == BODY, "the file outside the project was removed"


@handles_only
@pytest.mark.parametrize("outside_holds", ["a file", "an empty folder"])
def test_a_parent_swapped_after_the_folders_are_open_leaves_the_outside_file_and_folder(
    tmp_path: Path, outside_holds: str,
) -> None:
    target, path = _project_file(tmp_path)
    outside = tmp_path / "outside"
    (outside / "b").mkdir(parents=True)
    if outside_holds == "a file":
        (outside / "b" / "tool.py").write_bytes(BODY)
    calls: list[bool] = []

    def swap_the_folder_above() -> None:
        calls.append(True)
        grandparent = target / "a"
        os.rename(grandparent, target / "a-moved")
        grandparent.symlink_to(outside, target_is_directory=True)

    assert _removal(path, target, _after_walk=swap_the_folder_above) == "removed"
    assert calls == [True]
    assert not (target / "a-moved" / "b" / "tool.py").exists(), \
        "the project's own copy, reached through the open folders, was removed"
    assert (outside / "b").is_dir(), "the folder outside the project was removed"
    if outside_holds == "a file":
        assert (outside / "b" / "tool.py").read_bytes() == BODY


@handles_only
def test_the_walk_runs_only_when_open_unlink_rmdir_and_stat_all_take_dir_fd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []
    target, path = _project_file(tmp_path)
    assert _removal(path, target, _after_walk=lambda: calls.append("walked")) == "removed"
    assert calls == ["walked"]
    for missing in (os.open, os.unlink, os.rmdir, os.stat):
        target, path = _project_file(tmp_path / missing.__name__)
        with monkeypatch.context() as patch:
            patch.setattr(os, "supports_dir_fd", set(os.supports_dir_fd) - {missing})
            calls.clear()
            assert _removal(path, target, _after_walk=lambda: calls.append("walked")) == "removed"
        assert calls == [], f"the folder-handle walk ran without {missing.__name__}"
    target, path = _project_file(tmp_path / "no-flag")
    with monkeypatch.context() as patch:
        patch.delattr(os, "O_NOFOLLOW")
        calls.clear()
        assert _removal(path, target, _after_walk=lambda: calls.append("walked")) == "removed"
    assert calls == []


# ---------------------------------------------------------------------------
# A project from an older Cairn
# ---------------------------------------------------------------------------

import functools  # noqa: E402
import json  # noqa: E402

from bootstrap._scaffold.config import strip_conditional_regions  # noqa: E402
from bootstrap._scaffold.slotmerge import substitute_tokens  # noqa: E402
from bootstrap.verify_integrity import verify  # noqa: E402

LOCK_REL = "dev/.cairn/cairn-lock.yml"
SCRIPT = "scripts/onboarding_activate.py"
SCRIPT_2 = "scripts/foldback_suggest.py"
NEXT_SESSION = "dev/NEXT_SESSION.md"
PLAIN_MARKDOWN = "dev/modules/fold-back-ledger.md"
ROWS = {row[1]: row for row in C._RETIRED_INSTALLS}
MATCHES_NONE = "matches none of the versions this Cairn knows"
CANNOT_TELL = "cannot show it is unchanged"
PROFILE = (
    "project_name: RetiredFilesTest\n"
    "test_command: pytest\n"
    "python_package: retired_test\n"
    "preset: solo-greenfield\n"
)


@functools.lru_cache(maxsize=None)
def _shipped_versions(dst: str) -> tuple[bytes, ...]:
    """Every version of the template for *dst* the list knows, oldest first."""
    versions = []
    for _digest, _commit, blob in ROWS[dst][3]:
        result = _git_blob(blob)
        assert result.returncode == 0, f"git has no blob {blob}"
        versions.append(result.stdout)
    return tuple(versions)


def _sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _git(project: Path, *args: str, check: bool = True) -> str:
    done = subprocess.run(
        ["git", "-C", str(project), "-c", "user.name=t", "-c", "user.email=t@t",
         "-c", "commit.gpgsign=false", *args],
        capture_output=True, text=True, check=check,
    )
    return done.stdout.strip()


def _commit_all(project: Path, message: str = "state") -> None:
    _git(project, "add", "-A")
    _git(project, "commit", "-q", "--allow-empty", "-m", message)


@pytest.fixture(scope="module")
def pristine_install(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A fresh install of this Cairn, committed in git; tests copy it."""
    base = tmp_path_factory.mktemp("pristine")
    target = base / "project"
    target.mkdir()
    profile = base / "profile.yml"
    profile.write_text(PROFILE, encoding="utf-8")
    assert s.main(["--config", str(profile), "--target", str(target),
                   "--cairn-root", str(ROOT), "--allow-dev"]) == 0
    _git(target, "init", "-q", "-b", "main")
    _commit_all(target, "install")
    return target


@pytest.fixture
def project(pristine_install: Path, tmp_path: Path) -> Path:
    copy = tmp_path / "project"
    shutil.copytree(pristine_install, copy, symlinks=True)
    return copy


def _read_lock(project: Path) -> dict:
    lock = s.read_lockfile(project)
    assert lock is not None
    return lock


def _write_lock(project: Path, lock: dict) -> None:
    (project / LOCK_REL).write_text(s._emit_lock_yaml(lock), encoding="utf-8")


def _add_record(project: Path, record: dict) -> None:
    lock = _read_lock(project)
    lock["files"].append(record)
    _write_lock(project, lock)


def _script_record(dst: str, data: bytes, *, base: bytes | None = None) -> dict:
    return {"dst": dst, "src": ROWS[dst][0], "verbatim": True,
            "hash": _sha(data), "base_hash": _sha(data if base is None else base)}


def _add_script(project: Path, dst: str = SCRIPT, data: bytes | None = None, *,
                base: bytes | None = None, write: bool = True) -> Path:
    """Model a project that installed *dst* from an older Cairn."""
    data = _shipped_versions(dst)[-1] if data is None else data
    path = project / dst
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    _add_record(project, _script_record(dst, data, base=base))
    return path


def _rebuilt(project: Path, cache: bytes) -> bytes:
    """The text an install writes for a Markdown template: sized, then tokens."""
    lock = _read_lock(project)
    tokens = {str(k): str(v) for k, v in (lock.get("tokens") or {}).items()}
    axes = U._embedded_axes(lock.get("profile"))
    text = cache.decode("utf-8")
    text = strip_conditional_regions(text, axes) if axes else text
    return substitute_tokens(text, tokens).encode("utf-8")


def _add_markdown(project: Path, dst: str = NEXT_SESSION, *,
                  cache: bytes | None = None, file: bytes | None = None,
                  write_cache: bool = True, write_file: bool = True,
                  base_cache: str | None = None) -> tuple[Path, Path]:
    """Model a project that installed the Markdown file *dst* from an older Cairn."""
    cache = _shipped_versions(dst)[-1] if cache is None else cache
    file = _rebuilt(project, cache) if file is None else file
    cache_rel = f"dev/.cairn/base/{dst}"
    path, cache_path = project / dst, project / cache_rel
    if write_file:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file)
    if write_cache:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_bytes(cache)
    record = {"dst": dst, "src": ROWS[dst][0], "verbatim": False,
              "hash": _sha(file), "base_hash": _sha(cache),
              "base_cache": base_cache or cache_rel}
    if dst in s._LIVING_STATE_DSTS:
        record["living_state"] = True
    _add_record(project, record)
    return path, cache_path


def _upgrade(capsys: pytest.CaptureFixture[str], project: Path, *flags: str,
             ) -> tuple[int, str, str]:
    code = s.main(["upgrade", "--target", str(project), *flags,
                   "--cairn-root", str(ROOT)])
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _kind_names(report: str, label: str) -> list[str]:
    """The names a report line `<label>  N: a, b` carries; [] if there is none."""
    found = re.search(rf"^\s*{re.escape(label)}\s+\d+: (.*)$", report, re.M)
    return [] if found is None else [n.strip() for n in found.group(1).rstrip(".").split(",")]


def _flag(report: str, dst: str) -> str | None:
    found = re.search(rf"^\s*\[flag\] {re.escape(dst)}: (.*)$", report, re.M)
    return None if found is None else found.group(1)


def _tree_state(root: Path) -> dict[str, str]:
    """Every file and link under *root* (git's own folder included) with its bytes."""
    state: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            state[rel] = "link->" + os.readlink(path)
        elif path.is_file():
            state[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            state[rel] = "dir"
    return state


# ---------------------------------------------------------------------------
# The classifier, through `--plan`
# ---------------------------------------------------------------------------

def test_a_planted_record_for_a_plain_project_file_is_never_retired(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    analysis = project / "analysis.py"
    analysis.write_text("print('mine')\n", encoding="utf-8")
    _add_record(project, {
        "dst": "analysis.py", "src": "modules/default-on/nothing-here.py",
        "verbatim": True, "hash": _sha(analysis.read_bytes()),
        "base_hash": _sha(analysis.read_bytes())})
    # A record one letter off a real row, and one with another source, are not rows.
    other_case = SCRIPT.replace("scripts", "Scripts", 1)
    (project / other_case).parent.mkdir(exist_ok=True)
    (project / other_case).write_bytes(_shipped_versions(SCRIPT)[-1])
    _add_record(project, {**_script_record(SCRIPT, b"x"), "dst": other_case})
    other_source = {**_script_record(SCRIPT_2, b"y"), "src": ROWS[SCRIPT_2][0] + "x"}
    (project / SCRIPT_2).write_bytes(_shipped_versions(SCRIPT_2)[-1])
    _add_record(project, other_source)
    _commit_all(project)
    code, out, _err = _upgrade(capsys, project, "--plan")
    assert code == 0, out
    assert sorted(_kind_names(out, "removed-upstream")) == sorted(
        ["analysis.py", other_case, SCRIPT_2])
    assert "retired," not in out


def test_an_edit_after_init_lock_and_a_bare_finalize_is_kept(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    edited = _shipped_versions(SCRIPT)[-1] + b"# local change\n"
    # --init-lock records the disk as `hash` and a bare --finalize then copies it into
    # `base_hash`, so the record itself vouches for the edit.
    _add_script(project, data=edited)
    _commit_all(project)
    code, out, _err = _upgrade(capsys, project, "--plan")
    assert code == 0, out
    assert _kind_names(out, "retired, kept") == [SCRIPT]
    assert _flag(out, SCRIPT) == MATCHES_NONE
    assert _kind_names(out, "retired, untouched") == []


def test_an_untouched_script_is_untouched_in_every_version_the_list_carries(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    versions = _shipped_versions(SCRIPT)
    assert len(versions) == len(set(versions)) >= 2, "the row should carry two versions"
    for number, data in enumerate(versions):
        fresh = project.parent / f"v{number}"
        shutil.copytree(project, fresh, symlinks=True)
        _add_script(fresh, data=data)
        _commit_all(fresh)
        code, out, _err = _upgrade(capsys, fresh, "--plan")
        assert code == 0, out
        assert _kind_names(out, "retired, untouched") == [SCRIPT], out


def test_an_untouched_markdown_copy_is_untouched_an_added_line_matches_none_and_a_migrated_lockfile_cannot_tell(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    def judged(name: str, setup) -> tuple[str, str | None]:
        copy = tmp_path / name
        shutil.copytree(project, copy, symlinks=True)
        setup(copy)
        _commit_all(copy)
        code, out, _err = _upgrade(capsys, copy, "--plan")
        assert code == 0, out
        for label in ("retired, untouched", "retired, kept", "retired, already deleted"):
            if _kind_names(out, label) == [NEXT_SESSION]:
                return label, _flag(out, NEXT_SESSION)
        raise AssertionError(out)

    assert judged("untouched", _add_markdown) == ("retired, untouched", None)

    def added_line(copy: Path) -> None:
        _add_markdown(copy, file=_rebuilt(copy, _shipped_versions(NEXT_SESSION)[-1]) + b"mine\n")
    assert judged("added", added_line) == ("retired, kept", MATCHES_NONE)

    def migrated(copy: Path) -> None:
        _add_markdown(copy)
        lock = _read_lock(copy)
        lock["migrated"] = True
        _write_lock(copy, lock)
    assert judged("migrated", migrated) == ("retired, kept", CANNOT_TELL)

    def cache_not_a_shipped_version(copy: Path) -> None:
        _add_markdown(copy, cache=b"# a cache nobody shipped\n")
    assert judged("unlisted-cache", cache_not_a_shipped_version) == ("retired, kept", CANNOT_TELL)

    def no_cache(copy: Path) -> None:
        _add_markdown(copy, write_cache=False)
    assert judged("no-cache", no_cache) == ("retired, kept", CANNOT_TELL)

    # A second Markdown row classifies on its own, as the first does.
    copy = tmp_path / "second-row"
    shutil.copytree(project, copy, symlinks=True)
    _add_markdown(copy, PLAIN_MARKDOWN)
    _commit_all(copy)
    code, out, _err = _upgrade(capsys, copy, "--plan")
    assert code == 0 and _kind_names(out, "retired, untouched") == [PLAIN_MARKDOWN], out


def test_a_base_cache_that_is_not_the_rows_is_cannot_tell(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    elsewhere = "dev/.cairn/base/somewhere-else.md"
    _add_markdown(project, base_cache=elsewhere)     # the row's own cache is there too
    (project / elsewhere).write_bytes(_shipped_versions(NEXT_SESSION)[-1])
    _commit_all(project)
    code, out, _err = _upgrade(capsys, project, "--plan")
    assert code == 0, out
    assert _kind_names(out, "retired, kept") == [NEXT_SESSION]
    assert _flag(out, NEXT_SESSION) == CANNOT_TELL


def test_a_base_cache_another_record_also_names_is_cannot_tell(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    _add_markdown(project)
    _add_record(project, {
        "dst": "docs/other.md", "src": "modules/default-on/nothing.md", "verbatim": False,
        "hash": _sha(b"x"), "base_hash": _sha(b"x"),
        "base_cache": f"dev/.cairn/base/{NEXT_SESSION}"})
    _commit_all(project)
    code, out, _err = _upgrade(capsys, project, "--plan")
    assert code == 0, out
    assert _kind_names(out, "retired, kept") == [NEXT_SESSION]
    assert _flag(out, NEXT_SESSION) == CANNOT_TELL


def test_plan_to_an_older_ref_never_labels_a_shipped_file_retired(
    project: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    notice = ("core/NOTICE.md", "NOTICE.md")
    assert (ROOT / "templates" / notice[0]).is_file()
    old = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"v0.3.0:templates/{notice[0]}"],
                         capture_output=True)
    if old.returncode == 0:
        pytest.skip("v0.3.0 shipped NOTICE.md; the control needs a ref without it")
    # A list row for a template that the running tree still ships is not retired,
    # whatever an older ref says.
    monkeypatch.setattr(U, "_RETIRED_INSTALLS", (
        (notice[0], notice[1], False, ((hashlib.sha256(b"x").hexdigest(), "a" * 40, "b" * 40),)),
        *C._RETIRED_INSTALLS))
    code, out, _err = _upgrade(capsys, project, "--plan", "--to", "v0.3.0")
    assert code == 0, out
    assert "NOTICE.md" in _kind_names(out, "removed-upstream"), out
    assert "retired," not in out


def test_a_dangling_link_a_folder_and_a_linked_parent_are_blocked_not_gone(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    def blocked(name: str, setup) -> None:
        copy = tmp_path / name
        shutil.copytree(project, copy, symlinks=True)
        dst = setup(copy)
        _commit_all(copy)
        code, out, _err = _upgrade(capsys, copy, "--plan")
        assert code == 0, out
        assert _kind_names(out, "retired, already deleted") == [], (name, out)
        assert _kind_names(out, "retired, kept") == [dst], (name, out)
        assert "link" in (_flag(out, dst) or ""), (name, out)

    def dangling(copy: Path) -> str:
        _add_script(copy, write=False)
        (copy / SCRIPT).symlink_to(copy / "dev" / "nowhere")
        return SCRIPT

    def folder(copy: Path) -> str:
        _add_script(copy, write=False)
        (copy / SCRIPT).mkdir()
        return SCRIPT

    def linked_parent(copy: Path) -> str:
        dst = "scripts/_onboarding/cli.py"
        _add_script(copy, dst, write=False)
        (copy / "dev" / "real-folder").mkdir()
        (copy / "scripts" / "_onboarding").symlink_to(copy / "dev" / "real-folder")
        return dst

    blocked("dangling", dangling)
    blocked("folder", folder)
    blocked("linked-parent", linked_parent)


def test_plan_names_each_retired_state_in_fixed_words(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    _add_script(project, SCRIPT)                                    # untouched
    _add_markdown(project, NEXT_SESSION, write_file=False, write_cache=False)  # gone
    _add_script(project, SCRIPT_2, data=_shipped_versions(SCRIPT_2)[-1] + b"#\n",
                base=_shipped_versions(SCRIPT_2)[-1])               # matches none
    _add_markdown(project, PLAIN_MARKDOWN, cache=b"# unlisted\n")   # cannot tell
    _add_record(project, {                                          # not on the list
        "dst": "docs/old.md", "src": "modules/default-on/old.md", "verbatim": False,
        "hash": _sha(b"x"), "base_hash": _sha(b"x")})
    _commit_all(project)
    code, out, _err = _upgrade(capsys, project, "--plan")
    assert code == 0, out
    assert _kind_names(out, "retired, untouched") == [SCRIPT]
    assert _kind_names(out, "retired, already deleted") == [NEXT_SESSION]
    assert sorted(_kind_names(out, "retired, kept")) == sorted([SCRIPT_2, PLAIN_MARKDOWN])
    assert _flag(out, SCRIPT_2) == MATCHES_NONE
    assert _flag(out, PLAIN_MARKDOWN) == CANNOT_TELL
    assert _flag(out, SCRIPT) is None and _flag(out, NEXT_SESSION) is None
    assert _kind_names(out, "removed-upstream") == ["docs/old.md"]
    assert "differs from every version" not in out


def test_plan_writes_nothing_and_a_folder_at_a_retired_name_does_not_crash_it(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    _add_script(project, SCRIPT)
    _add_script(project, SCRIPT_2, write=False)
    (project / SCRIPT_2).mkdir()
    (project / SCRIPT_2 / "inner").write_text("x", encoding="utf-8")
    _add_markdown(project, NEXT_SESSION, write_file=False, write_cache=False)
    _commit_all(project)
    before = _tree_state(project)
    code, out, err = _upgrade(capsys, project, "--plan")
    assert code == 0, (out, err)
    assert "Traceback" not in err
    assert _tree_state(project) == before
    assert _kind_names(out, "retired, kept") == [SCRIPT_2]


def test_stage_and_apply_leave_retired_files_and_records_alone(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    _add_script(project, SCRIPT)
    _add_script(project, SCRIPT_2, data=_shipped_versions(SCRIPT_2)[-1] + b"#\n")
    _add_markdown(project, NEXT_SESSION, write_file=False, write_cache=False)
    _commit_all(project)
    lock_before = _read_lock(project)
    files_before = {d: (project / d).read_bytes() for d in (SCRIPT, SCRIPT_2)}
    for flag in ("--stage", "--apply"):
        code, out, err = _upgrade(capsys, project, flag)
        assert code == 0, (flag, out, err)
    retired = {SCRIPT, SCRIPT_2, NEXT_SESSION}
    after = {r["dst"]: r for r in _read_lock(project)["files"] if r["dst"] in retired}
    before = {r["dst"]: r for r in lock_before["files"] if r["dst"] in retired}
    assert after == before
    assert {d: (project / d).read_bytes() for d in (SCRIPT, SCRIPT_2)} == files_before


def test_an_uncommitted_or_ignored_copy_is_kept(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    def kept_words(copy: Path, dst: str = SCRIPT) -> tuple[str, str | None]:
        code, out, _err = _upgrade(capsys, copy, "--plan")
        assert code == 0, out
        if dst in _kind_names(out, "retired, untouched"):
            return "retired, untouched", None
        assert dst in _kind_names(out, "retired, kept"), out
        return "retired, kept", _flag(out, dst)

    # Control: committed and untouched.
    _add_script(project)
    _commit_all(project)
    assert kept_words(project) == ("retired, untouched", None)
    # Untracked: never committed.
    other = project.parent / "untracked"
    shutil.copytree(project, other, symlinks=True)
    _git(other, "rm", "-q", "--cached", SCRIPT)
    _git(other, "commit", "-q", "-m", "stop tracking the file")
    assert (other / SCRIPT).is_file()
    assert kept_words(other) == ("retired, kept", CANNOT_TELL)
    # Ignored.
    ignored = project.parent / "ignored"
    shutil.copytree(project, ignored, symlinks=True)
    _git(ignored, "rm", "-q", "--cached", SCRIPT)
    with (ignored / ".gitignore").open("a", encoding="utf-8") as stream:
        stream.write(f"\n{SCRIPT}\n")
    _commit_all(ignored)
    assert kept_words(ignored) == ("retired, kept", CANNOT_TELL)
    # The last commit holds another version of the file than the disk does.
    changed = project.parent / "committed-edit"
    shutil.copytree(project, changed, symlinks=True)
    (changed / SCRIPT).write_bytes(_shipped_versions(SCRIPT)[0])
    _commit_all(changed)
    (changed / SCRIPT).write_bytes(_shipped_versions(SCRIPT)[-1])
    assert kept_words(changed) == ("retired, kept", CANNOT_TELL)
    # A Markdown copy whose cached template was never committed.
    markdown = project.parent / "markdown-cache"
    shutil.copytree(project, markdown, symlinks=True)
    _add_markdown(markdown)
    _commit_all(markdown)
    assert kept_words(markdown, NEXT_SESSION) == ("retired, untouched", None)
    _git(markdown, "rm", "-q", "--cached", f"dev/.cairn/base/{NEXT_SESSION}")
    _git(markdown, "commit", "-q", "-m", "stop tracking the cached template")
    assert kept_words(markdown, NEXT_SESSION) == ("retired, kept", CANNOT_TELL)
    # No git at all.
    no_git = project.parent / "no-git"
    shutil.copytree(project, no_git, symlinks=True)
    shutil.rmtree(no_git / ".git")
    assert kept_words(no_git) == ("retired, kept", CANNOT_TELL)


# ---------------------------------------------------------------------------
# The step: `upgrade --remove-retired`
# ---------------------------------------------------------------------------

def _step(capsys: pytest.CaptureFixture[str], project: Path, *flags: str,
          ) -> tuple[int, str, str]:
    return _upgrade(capsys, project, "--remove-retired", *flags)


def _records(project: Path) -> dict[str, dict]:
    return {r["dst"]: r for r in _read_lock(project)["files"]}


def _old_project(project: Path) -> tuple[Path, Path]:
    """An untouched script and an untouched Markdown copy, committed."""
    script = _add_script(project, SCRIPT)
    markdown, _cache = _add_markdown(project, NEXT_SESSION)
    _commit_all(project)
    return script, markdown


def test_an_untouched_script_is_removed_its_record_cleared_and_integrity_passes(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    script = _add_script(project, SCRIPT)
    nested = _add_script(project, "scripts/_onboarding/cli.py")
    sibling = project / "scripts" / "_onboarding" / "keep.txt"
    sibling.write_text("mine", encoding="utf-8")
    _commit_all(project)
    assert verify(project) == 0
    others = {d: r for d, r in _records(project).items() if d not in (SCRIPT, "scripts/_onboarding/cli.py")}
    code, out, err = _step(capsys, project)
    assert code == 0, (out, err)
    assert not script.exists() and not nested.exists()
    assert sibling.is_file(), "a file the project added next to it stays"
    assert (project / "scripts").is_dir()
    records = _records(project)
    assert SCRIPT not in records and "scripts/_onboarding/cli.py" not in records
    assert {d: r for d, r in records.items()} == others
    assert verify(project) == 0
    assert re.search(rf"removed\s+{re.escape(SCRIPT)}", out), out
    assert "ommit" in out.splitlines()[-1] or "ommit" in out, "the step says to commit the removal"
    # Rerun: nothing to do, exit 0.
    code, out, _err = _step(capsys, project)
    assert code == 0 and "nothing" in out.lower(), out


def test_an_untouched_markdown_copy_goes_with_its_cache_and_a_gone_one_removes_a_leftover_cache(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    markdown, cache = _add_markdown(project, NEXT_SESSION)
    _gone_file, leftover = _add_markdown(project, PLAIN_MARKDOWN, write_file=False)
    _commit_all(project)
    code, out, err = _step(capsys, project)
    assert code == 0, (out, err)
    assert not markdown.exists() and not cache.exists()
    assert not leftover.exists(), "the cached template of an already deleted file went too"
    records = _records(project)
    assert NEXT_SESSION not in records and PLAIN_MARKDOWN not in records
    assert verify(project) == 0


def test_base_cache_pointed_at_another_file_removes_nothing(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    other = project / "dev" / "my-notes.md"
    other.write_bytes(_shipped_versions(NEXT_SESSION)[-1])
    markdown, cache = _add_markdown(project, NEXT_SESSION, base_cache="dev/my-notes.md")
    assert cache.is_file(), "the row's own cache is there too"
    _commit_all(project)
    before = _tree_state(project)
    code, out, _err = _step(capsys, project)
    assert code == 0, out
    assert _tree_state(project) == before
    assert NEXT_SESSION in _records(project)
    assert re.search(rf"kept\s+{re.escape(NEXT_SESSION)}: {re.escape(CANNOT_TELL)}", out), out


def test_a_record_is_cleared_only_after_absence_is_confirmed(
    project: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    script = _add_script(project, SCRIPT)
    _commit_all(project)

    def does_nothing(*_args: object, **_kwargs: object) -> None:
        return None

    with monkeypatch.context() as patch:
        patch.setattr(SEC.os, "unlink", does_nothing)
        patch.setattr(os, "supports_dir_fd", set(os.supports_dir_fd) | {does_nothing})
        code, out, _err = _step(capsys, project)
    assert code == 0, out
    assert script.is_file(), "the removal did nothing, so the file is still there"
    assert SCRIPT in _records(project), "a record was cleared for a file that is still there"
    assert re.search(rf"kept\s+{re.escape(SCRIPT)}", out), out
    # Control: the same project, nothing patched.
    code, out, _err = _step(capsys, project)
    assert code == 0 and not script.exists() and SCRIPT not in _records(project)


@pytest.mark.skipif(os.name == "nt" or os.geteuid() == 0,
                    reason="a read-only folder stops a removal only for a non-root user on POSIX")
def test_a_folder_that_will_not_let_the_file_go_keeps_its_record(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    nested = _add_script(project, "scripts/_onboarding/cli.py")
    _commit_all(project)
    nested.parent.chmod(0o555)
    try:
        code, out, _err = _step(capsys, project)
    finally:
        nested.parent.chmod(0o755)
    assert code == 0, out
    assert nested.is_file() and "scripts/_onboarding/cli.py" in _records(project)


def test_a_cached_template_that_will_not_go_keeps_the_record_so_a_rerun_finishes(
    project: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    markdown, cache = _add_markdown(project, NEXT_SESSION)
    _commit_all(project)
    real = SEC._remove_unchanged_file

    def refuse_the_cache(path: Path, target: Path, expected: bytes | None, **kw: object) -> bool:
        if Path(path) == cache:
            return False
        return real(path, target, expected, **kw)

    monkeypatch.setattr(U, "_remove_unchanged_file", refuse_the_cache)
    code, out, _err = _step(capsys, project)
    assert code == 0, out
    assert not markdown.exists() and cache.is_file()
    assert NEXT_SESSION in _records(project)
    monkeypatch.undo()
    code, out, _err = _step(capsys, project)
    assert code == 0, out
    assert not cache.exists() and NEXT_SESSION not in _records(project)


def test_a_stop_before_the_lockfile_write_heals_on_rerun(
    project: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    script, markdown = _old_project(project)
    lock_before = (project / LOCK_REL).read_bytes()

    def stop(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("stopped before the lockfile was written")

    monkeypatch.setattr(U, "_commit_lock_and_caches", stop)
    with pytest.raises(RuntimeError):
        _step(capsys, project)
    assert not script.exists() and not markdown.exists(), "files go first"
    assert (project / LOCK_REL).read_bytes() == lock_before, "the lockfile goes last"
    monkeypatch.undo()
    assert verify(project) == 1, "records for files already gone show as missing"
    code, out, _err = _step(capsys, project)
    assert code == 0, out
    assert SCRIPT not in _records(project) and NEXT_SESSION not in _records(project)
    assert verify(project) == 0


def test_remove_retired_refuses_to_and_force_with_exit_2(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    script, markdown = _old_project(project)
    before = _tree_state(project)
    for flags in (("--to", "v0.3.0"), ("--force",)):
        code, out, err = _step(capsys, project, *flags)
        assert code == 2, (flags, out, err)
        assert _tree_state(project) == before
    code, _out, err = _upgrade(capsys, project, "--remove-retired", "--plan")
    assert code == 2 and "mutually exclusive" in err


def test_plan_names_exactly_the_files_the_step_removes(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    _add_script(project, SCRIPT)                                              # untouched
    _add_script(project, SCRIPT_2, data=_shipped_versions(SCRIPT_2)[-1] + b"#\n")   # matches none
    _add_script(project, "scripts/_onboarding/cli.py", write=False)           # gone
    _add_markdown(project, NEXT_SESSION)                                      # untouched
    _add_markdown(project, PLAIN_MARKDOWN, cache=b"# unlisted\n")             # cannot tell
    _commit_all(project)
    _code, plan, _err = _upgrade(capsys, project, "--plan")
    promised = set(_kind_names(plan, "retired, untouched"))
    deleted = set(_kind_names(plan, "retired, already deleted"))
    kept = set(_kind_names(plan, "retired, kept"))
    assert promised == {SCRIPT, NEXT_SESSION} and kept == {SCRIPT_2, PLAIN_MARKDOWN}
    before = {d: (project / d).exists() for d in promised | deleted | kept}
    before_records = set(_records(project))
    code, out, _err = _step(capsys, project)
    assert code == 0, out
    removed = {d for d, existed in before.items() if existed and not (project / d).exists()}
    cleared = before_records - set(_records(project))
    assert removed == promised
    assert cleared == promised | deleted
    assert all((project / d).exists() for d in kept)


def test_plan_ends_with_the_command_the_step_runs(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    _old_project(project)
    code, out, _err = _upgrade(capsys, project, "--plan")
    assert code == 0
    assert "--remove-retired" in out
    assert out.index("retired, untouched") < out.index("--remove-retired")


def test_plan_names_no_command_when_the_step_would_do_nothing(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    _add_script(project, SCRIPT, data=_shipped_versions(SCRIPT)[-1] + b"# mine\n")
    _commit_all(project)
    code, out, _err = _upgrade(capsys, project, "--plan")
    assert code == 0 and "retired, kept" in out
    assert "--remove-retired" not in out


def test_the_step_with_nothing_to_do_exits_0_and_writes_nothing(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    before = _tree_state(project)
    code, out, _err = _step(capsys, project)
    assert code == 0 and "nothing" in out.lower(), out
    assert _tree_state(project) == before


def test_a_kept_file_is_not_an_error_and_is_named_in_fixed_words(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    _add_script(project, SCRIPT, data=_shipped_versions(SCRIPT)[-1] + b"# mine\n")
    _add_script(project, SCRIPT_2)
    (project / "scripts" / "_onboarding").mkdir()
    _add_script(project, "scripts/_onboarding/cli.py", write=False)
    (project / "scripts" / "_onboarding" / "cli.py").mkdir()
    _commit_all(project)
    code, out, _err = _step(capsys, project)
    assert code == 0, out
    assert re.search(rf"kept\s+{re.escape(SCRIPT)}: {re.escape(MATCHES_NONE)}", out), out
    assert re.search(r"kept\s+scripts/_onboarding/cli.py: a link, a folder", out), out
    assert {SCRIPT, "scripts/_onboarding/cli.py"} <= set(_records(project))
    assert SCRIPT_2 not in _records(project)
    assert (project / SCRIPT).is_file()


def test_remove_retired_refuses_a_linked_profile_and_reads_nothing(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    _old_project(project)
    outside = tmp_path / "outside-profile.yml"
    outside.write_text("project_name: elsewhere\n", encoding="utf-8")
    profile = project / "dev" / ".cairn" / "profile.yml"
    profile.unlink(missing_ok=True)
    profile.symlink_to(outside)
    before = _tree_state(project)
    code, out, err = _step(capsys, project)
    assert code == 2, (out, err)
    assert "link" in err
    assert _tree_state(project) == before


def test_an_uncommitted_or_ignored_copy_is_kept_by_the_step_too(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    _add_script(project, SCRIPT)
    _add_script(project, SCRIPT_2, data=_shipped_versions(SCRIPT_2)[0])
    _commit_all(project)
    # SCRIPT: no longer tracked. SCRIPT_2: the commit holds an earlier shipped version.
    _git(project, "rm", "-q", "--cached", SCRIPT)
    _git(project, "commit", "-q", "-m", "stop tracking")
    (project / SCRIPT_2).write_bytes(_shipped_versions(SCRIPT_2)[-1])
    code, out, _err = _step(capsys, project)
    assert code == 0, out
    assert (project / SCRIPT).is_file() and (project / SCRIPT_2).is_file()
    assert {SCRIPT, SCRIPT_2} <= set(_records(project))
    for dst in (SCRIPT, SCRIPT_2):
        assert re.search(rf"kept\s+{re.escape(dst)}: {re.escape(CANNOT_TELL)}", out), out


def test_a_subfolder_project_keeps_an_edited_tracked_file(
    tmp_path: Path, pristine_install: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    repo = tmp_path / "repo"
    sub = repo / "inner"
    shutil.copytree(pristine_install, sub, symlinks=True)
    shutil.rmtree(sub / ".git")
    _git(repo, "init", "-q", "-b", "main")
    _add_script(sub, SCRIPT)
    _add_script(sub, SCRIPT_2)
    _commit_all(repo)
    # SCRIPT_2: a later shipped version on disk, the earlier one committed.
    (sub / SCRIPT_2).write_bytes(_shipped_versions(SCRIPT_2)[0])
    _commit_all(repo)
    (sub / SCRIPT_2).write_bytes(_shipped_versions(SCRIPT_2)[-1])
    code, out, _err = _step(capsys, sub)
    assert code == 0, out
    assert not (sub / SCRIPT).exists(), "the committed, untouched copy goes, judged by project names"
    assert (sub / SCRIPT_2).is_file() and SCRIPT_2 in _records(sub)


def _spy(path: Path, marker: Path) -> str:
    path.write_text(f"#!/bin/sh\necho ran >> '{marker}'\nexit 1\n", encoding="utf-8")
    path.chmod(0o755)
    return str(path)


@posix_only
def test_git_config_programs_never_run_during_plan_or_the_step(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    marker = tmp_path / "ran.txt"
    spy = _spy(tmp_path / "spy.sh", marker)
    _add_script(project, SCRIPT)
    _commit_all(project)
    _git(project, "config", "core.fsmonitor", spy)
    _git(project, "config", "filter.spy.clean", spy)
    _git(project, "config", "filter.spy.smudge", spy)
    _git(project, "config", "core.sshCommand", spy)
    (project / ".gitattributes").write_text(f"{SCRIPT} filter=spy\n", encoding="utf-8")
    for flags in (("--plan",), ("--remove-retired",)):
        code, out, err = _upgrade(capsys, project, *flags)
        assert code == 0, (flags, out, err)
    assert not marker.exists(), "a program named in the project's git settings ran"
    assert not (project / SCRIPT).exists(), "control: the untouched copy still went"


@posix_only
def test_a_blobless_clone_with_an_upload_pack_program_runs_none_and_keeps_the_copy(
    tmp_path: Path, pristine_install: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    origin = tmp_path / "origin"
    shutil.copytree(pristine_install, origin, symlinks=True)
    _add_script(origin, SCRIPT)
    _commit_all(origin)
    _git(origin, "config", "uploadpack.allowFilter", "true")
    _git(origin, "config", "uploadpack.allowAnySHA1InWant", "true")
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", "--no-checkout", "--filter=blob:none",
                    f"file://{origin}", str(clone)], check=True, capture_output=True)
    for path in origin.rglob("*"):
        rel = path.relative_to(origin)
        if rel.parts[0] == ".git" or not path.is_file():
            continue
        (clone / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, clone / rel)
    marker = tmp_path / "ran.txt"
    _git(clone, "config", "remote.origin.uploadpack", _spy(tmp_path / "spy.sh", marker))
    lazy_off = {**os.environ, "GIT_NO_LAZY_FETCH": "1"}
    assert subprocess.run(
        ["git", "-C", str(clone), "cat-file", "-e", "HEAD:" + SCRIPT],
        env=lazy_off, capture_output=True).returncode != 0, "the blob must be missing here"
    for flags in (("--plan",), ("--remove-retired",)):
        code, out, err = _upgrade(capsys, clone, *flags)
        assert code == 0, (flags, out, err)
    assert not marker.exists(), "the upload-pack program ran"
    assert (clone / SCRIPT).is_file() and SCRIPT in _records(clone)


def _swap_for_link_after_the_decision(
    monkeypatch: pytest.MonkeyPatch, project: Path, folder: str, outside: Path,
) -> None:
    """After the step has decided what to remove, put a link where *folder* was."""
    real = U._classify_retired_records

    def decide_then_swap(*args: object, **kwargs: object) -> list:
        decided = real(*args, **kwargs)
        moved = project / (folder + "-moved")
        os.rename(project / folder, moved)
        (project / folder).symlink_to(outside, target_is_directory=True)
        return decided

    monkeypatch.setattr(U, "_classify_retired_records", decide_then_swap)


@pytest.mark.parametrize("site", ["the file", "a copy's cached template", "a leftover cached template"])
def test_a_folder_swapped_for_a_link_after_the_decision_leaves_the_outside_copy(
    project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str], site: str,
) -> None:
    outside = tmp_path / "outside"
    if site == "the file":
        dst = "scripts/_onboarding/cli.py"
        _add_script(project, dst)
        folder = "scripts/_onboarding"
        (outside).mkdir()
        (outside / "cli.py").write_bytes(_shipped_versions(dst)[-1])
        victims = [outside / "cli.py"]
    else:
        cache_dst = NEXT_SESSION if site == "a copy's cached template" else PLAIN_MARKDOWN
        _add_markdown(project, cache_dst, write_file=(site == "a copy's cached template"))
        folder = "dev/.cairn/base"
        (outside / "dev" / "modules").mkdir(parents=True)
        for rel in (NEXT_SESSION, PLAIN_MARKDOWN):
            (outside / rel).write_bytes(_shipped_versions(rel)[-1])
        victims = [outside / cache_dst]
    _commit_all(project)
    _swap_for_link_after_the_decision(monkeypatch, project, folder, outside)
    code, out, err = _step(capsys, project)
    assert code in (0, 2), (out, err)
    for victim in victims:
        assert victim.is_file(), f"{victim} outside the project was removed"


@pytest.mark.parametrize("base_links_to", ["outside", "inside"])
def test_a_linked_base_cache_folder_removes_nothing_outside_the_project(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str], base_links_to: str,
) -> None:
    outside = tmp_path / "outside"
    for rel in (NEXT_SESSION, PLAIN_MARKDOWN):
        (outside / rel).parent.mkdir(parents=True, exist_ok=True)
        (outside / rel).write_bytes(_shipped_versions(rel)[-1])
    # An untouched copy whose record names the row's cache, and a deleted file whose
    # record names none; both find a linked folder where the cache folder should be.
    _add_markdown(project, NEXT_SESSION, write_cache=False)
    _add_markdown(project, PLAIN_MARKDOWN, write_file=False, write_cache=False)
    lock = _read_lock(project)
    for rec in lock["files"]:
        if rec["dst"] == PLAIN_MARKDOWN:
            rec.pop("base_cache")
    _write_lock(project, lock)
    base = project / "dev" / ".cairn" / "base"
    shutil.rmtree(base, ignore_errors=True)
    if base_links_to == "outside":
        base.symlink_to(outside, target_is_directory=True)
        expect_refused = True
    else:
        real = project / "dev" / "real-base"
        shutil.copytree(outside, real)
        base.symlink_to(real, target_is_directory=True)
        expect_refused = False
    _git(project, "add", "-A", "-f")
    _git(project, "commit", "-q", "--allow-empty", "-m", "state")
    before = _tree_state(outside)
    before_inside = _tree_state(project / "dev" / "real-base") if not expect_refused else {}
    code, out, err = _step(capsys, project)
    assert _tree_state(outside) == before
    if expect_refused:
        assert code == 2, (out, err)
        assert NEXT_SESSION in _records(project)
        return
    assert code == 0, (out, err)
    assert _tree_state(project / "dev" / "real-base") == before_inside, "a cache behind a link was removed"
    assert (project / NEXT_SESSION).is_file() and NEXT_SESSION in _records(project)
    assert re.search(rf"kept\s+{re.escape(NEXT_SESSION)}: {re.escape(CANNOT_TELL)}", out), out


def test_a_name_that_is_taken_after_the_decision_keeps_its_record(
    project: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    _add_script(project, SCRIPT, write=False)
    _commit_all(project)
    real = U._classify_retired_records

    def decide_then_a_file_appears(*args: object, **kwargs: object) -> list:
        decided = real(*args, **kwargs)
        (project / SCRIPT).write_bytes(b"new work\n")
        return decided

    monkeypatch.setattr(U, "_classify_retired_records", decide_then_a_file_appears)
    code, out, _err = _step(capsys, project)
    assert code == 0, out
    assert (project / SCRIPT).read_bytes() == b"new work\n"
    assert SCRIPT in _records(project)



# ---------------------------------------------------------------------------
# `upgrade --finalize` over retired records
# ---------------------------------------------------------------------------

def _finalize(capsys: pytest.CaptureFixture[str], project: Path, *flags: str,
              ) -> tuple[int, str, str]:
    return _upgrade(capsys, project, "--finalize", *flags)


def test_a_gone_retired_record_is_cleared_by_bare_finalize(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    _add_script(project, SCRIPT, write=False)
    _add_markdown(project, NEXT_SESSION, write_file=False, write_cache=False)
    _commit_all(project)
    assert verify(project) == 1
    code, out, err = _finalize(capsys, project)
    assert code == 0, (out, err)
    records = _records(project)
    assert SCRIPT not in records and NEXT_SESSION not in records
    assert SCRIPT in out and NEXT_SESSION in out, "the cleared records are named"
    assert verify(project) == 0


def test_a_blocked_name_still_refuses_bare_finalize_with_exit_1(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    def refused(name: str, setup) -> None:
        copy = tmp_path / name
        shutil.copytree(project, copy, symlinks=True)
        dst = setup(copy)
        _commit_all(copy)
        code, _out, err = _finalize(capsys, copy)
        assert code == 1, (name, err)
        assert dst in err and dst in _records(copy), name

    def dangling(copy: Path) -> str:
        _add_script(copy, write=False)
        (copy / SCRIPT).symlink_to(copy / "dev" / "nowhere")
        return SCRIPT

    def folder(copy: Path) -> str:
        _add_script(copy, write=False)
        (copy / SCRIPT).mkdir()
        return SCRIPT

    def linked_parent(copy: Path) -> str:
        dst = "scripts/_onboarding/cli.py"
        _add_script(copy, dst)
        (copy / "dev" / "real-folder").mkdir()
        shutil.move(str(copy / "scripts" / "_onboarding"), str(copy / "dev" / "real-folder" / "x"))
        (copy / "scripts" / "_onboarding").symlink_to(copy / "dev" / "real-folder" / "x")
        return dst

    refused("dangling", dangling)
    refused("folder", folder)
    refused("linked-parent", linked_parent)


def test_a_missing_unlisted_file_and_a_deleted_shipped_file_still_refuse(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    mine = project / "analysis.py"
    mine.write_text("print('mine')\n", encoding="utf-8")
    _add_record(project, {
        "dst": "analysis.py", "src": "modules/default-on/nothing-here.py", "verbatim": True,
        "hash": _sha(mine.read_bytes()), "base_hash": _sha(mine.read_bytes())})
    _commit_all(project)
    mine.unlink()
    code, _out, err = _finalize(capsys, project)
    assert code == 1 and "analysis.py" in err
    assert "analysis.py" in _records(project)
    mine.write_text("print('mine')\n", encoding="utf-8")
    (project / "NOTICE.md").unlink()
    _commit_all(project)
    code, _out, err = _finalize(capsys, project)
    assert code == 1 and "NOTICE.md" in err
    assert "NOTICE.md" in _records(project)


@pytest.mark.parametrize("force", [(), ("--force",)])
def test_a_copy_that_matches_none_or_cannot_be_shown_unchanged_is_skipped_by_bare_and_force_finalize(
    project: Path, capsys: pytest.CaptureFixture[str], force: tuple[str, ...],
) -> None:
    shipped = _shipped_versions(SCRIPT)[-1]
    edited = _add_script(project, SCRIPT, data=shipped + b"# mine\n", base=shipped)
    _add_markdown(project, PLAIN_MARKDOWN, cache=b"# a cache nobody shipped\n")
    fine = _add_script(project, SCRIPT_2)
    lock = _read_lock(project)
    next(r for r in lock["files"] if r["dst"] == SCRIPT_2)["hash"] = _sha(b"stale")
    _write_lock(project, lock)
    _commit_all(project)
    before = _records(project)
    code, out, err = _finalize(capsys, project, *force)
    assert code == 0, (out, err)
    after = _records(project)
    assert after[SCRIPT]["hash"] == before[SCRIPT]["hash"], "an edited retired copy was recorded"
    assert after[PLAIN_MARKDOWN]["hash"] == before[PLAIN_MARKDOWN]["hash"]
    assert after[SCRIPT_2]["hash"] == _sha(fine.read_bytes()), "an untouched copy is recorded as today"
    assert re.search(rf"{re.escape(SCRIPT)}: {re.escape(MATCHES_NONE)}", out), out
    assert re.search(rf"{re.escape(PLAIN_MARKDOWN)}: {re.escape(CANNOT_TELL)}", out), out
    assert "now attests this tree" not in out, "the closing line must not claim that"
    assert re.search(r"2 retired .*not recorded", out), out
    assert edited.is_file()


def test_scoped_finalize_records_it_and_says_so(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    shipped = _shipped_versions(SCRIPT)[-1]
    _add_script(project, SCRIPT, data=shipped + b"# mine\n", base=shipped)
    _commit_all(project)
    (project / SCRIPT).write_bytes(shipped + b"# mine, edited again\n")
    code, out, err = _finalize(capsys, project, SCRIPT)
    assert code == 0, (out, err)
    assert _records(project)[SCRIPT]["hash"] == _sha(shipped + b"# mine, edited again\n")
    assert re.search(rf"recorded .*{re.escape(SCRIPT)}", out), out


def test_an_edited_living_state_copy_is_neither_counted_nor_recorded(
    project: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    agreement = "dev/collaboration_agreement.md"
    _add_markdown(project, agreement, file=b"# Project-owned agreement\nLocal terms.\n")
    _add_markdown(project, NEXT_SESSION, file=b"# my notes\n")
    _commit_all(project)
    before = _records(project)
    code, out, err = _finalize(capsys, project)
    assert code == 0, (out, err)
    after = _records(project)
    for dst in (agreement, NEXT_SESSION):
        assert after[dst]["hash"] == before[dst]["hash"]
        assert dst not in out, f"{dst} is living state: finalize neither counts nor names it"
    assert "now attests this tree" in out


def test_finalize_never_reaches_committed_copy_matches(
    project: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    _add_script(project, SCRIPT)
    _add_script(project, SCRIPT_2, write=False)
    _commit_all(project)

    def never(*_args: object, **_kwargs: object) -> bool:
        raise AssertionError("--finalize asked git about a committed copy")

    monkeypatch.setattr(U, "_committed_copy_matches", never)
    for flags in ((), ("--force",), (SCRIPT,)):
        code, out, err = _finalize(capsys, project, *flags)
        assert code == 0, (flags, out, err)
