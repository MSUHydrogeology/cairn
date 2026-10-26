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
    # Prints without end: cut at one byte past the copy.
    _stand_in_git(tmp_path, monkeypatch, name="endless", cat_file="yes payload")
    started = time.monotonic()
    assert U._committed_copy_matches(project, "a.py", b"payload") is False
    assert time.monotonic() - started < 4
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
