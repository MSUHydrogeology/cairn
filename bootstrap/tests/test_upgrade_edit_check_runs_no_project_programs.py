"""The upgrade edit check runs no program a project's git settings name.

`upgrade --stage`, `--apply` and a bare `--finalize` ask whether the files they
are about to overwrite or hash have unsaved edits. Asking `git status` would run
whatever the project's `.git/config` names (a file-system monitor, a clean
filter, a pager), so the engine asks git only for the index and the last commit,
through one launcher that removes every route a project has to run a program, and
reads the working files itself.

The tests call the helpers directly where the property is local, and drive the
real `scaffold.py upgrade` entry point where it is the callers' behaviour. A
stand-in `git` first on `PATH` logs every call, so a test can say which commands
ran, and which did not.
"""

from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import sys
import threading
import warnings
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap._scaffold import upgrade as U  # noqa: E402

posix_only = pytest.mark.skipif(
    os.name == "nt", reason="needs POSIX modes, links and shell stand-ins")


@pytest.fixture(autouse=True)
def _forget_the_git_version(monkeypatch: pytest.MonkeyPatch) -> None:
    """Read `git --version` afresh in every node (it is cached per process)."""
    monkeypatch.setattr(U, "_GIT_FLOOR_MET", None)


def _blob_id(data: bytes, algorithm: str = "sha1") -> str:
    header = b"blob %d\0" % len(data)
    if algorithm == "sha1":
        return hashlib.sha1(header + data, usedforsecurity=False).hexdigest()
    return hashlib.sha256(header + data).hexdigest()


# ---------------------------------------------------------------------------
# The working-file comparison
# ---------------------------------------------------------------------------

BODY = b"print('shipped')\n"


def _differs(project: Path, name: str = "f.py", *, mode: str = "100644",
             data: bytes = BODY, check_mode: bool = True,
             fold_crlf: bool = False) -> bool:
    return U._working_file_differs(
        project.resolve(), name, mode, _blob_id(data), check_mode, fold_crlf)


def test_an_unchanged_file_does_not_differ_and_one_changed_byte_does(
    tmp_path: Path,
) -> None:
    (tmp_path / "f.py").write_bytes(BODY)
    assert _differs(tmp_path) is False
    (tmp_path / "f.py").write_bytes(BODY + b"#")
    assert _differs(tmp_path) is True
    (tmp_path / "f.py").unlink()
    assert _differs(tmp_path) is True, "a missing file is an edit"
    (tmp_path / "f.py").mkdir()
    assert _differs(tmp_path) is True, "a folder at the name is an edit"


@posix_only
def test_a_link_in_the_path_counts_as_edited_and_a_fifo_does_not_block(
    tmp_path: Path,
) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "f.py").write_bytes(BODY)
    project = tmp_path / "project"
    project.mkdir()
    # Every file below holds exactly the indexed bytes, so only the link or the
    # special file can make the answer "edited".
    (project / "real.py").write_bytes(BODY)
    (project / "f.py").symlink_to(project / "real.py")
    assert _differs(project, "f.py") is True, "a link at the name"
    (project / "linked").symlink_to(outside)
    assert _differs(project, "linked/f.py") is True, "a linked parent folder"
    assert (project / "linked" / "f.py").read_bytes() == BODY, "the control reads through"
    os.mkfifo(project / "pipe.py")
    answers: list[bool] = []
    reader = threading.Thread(
        target=lambda: answers.append(_differs(project, "pipe.py")), daemon=True)
    reader.start()
    reader.join(5)
    if reader.is_alive():
        # Free the blocked reader before failing, so the node does not hang the run.
        fd = os.open(project / "pipe.py", os.O_WRONLY | os.O_NONBLOCK)
        os.close(fd)
        reader.join(5)
        pytest.fail("reading a FIFO blocked")
    assert answers == [True]


def test_a_file_is_hashed_the_way_git_hashes_a_blob(tmp_path: Path) -> None:
    data = b"one\ntwo\r\nthree"
    for number, (algorithm, init) in enumerate(
            (("sha1", ["init", "-q"]),
             ("sha256", ["init", "-q", "--object-format=sha256"]))):
        repository = tmp_path / algorithm
        repository.mkdir()
        made = subprocess.run(["git", "-C", str(repository), *init],
                              capture_output=True, text=True)
        if made.returncode != 0:
            assert number == 1, made.stderr
            warnings.warn(
                "this git has no --object-format=sha256; the SHA-256 arm did not run",
                stacklevel=1)
            continue
        (repository / "f.bin").write_bytes(data)
        expected = subprocess.run(
            ["git", "-C", str(repository), "hash-object", "--no-filters", "f.bin"],
            capture_output=True, text=True, check=True).stdout.strip()
        assert len(expected) == (40 if algorithm == "sha1" else 64)
        assert U._working_file_differs(
            repository.resolve(), "f.bin", "100644", expected, True, False) is False
        assert U._working_file_differs(
            repository.resolve(), "f.bin", "100644", "0" * len(expected), True, False) is True


@posix_only
def test_a_mode_only_edit_counts_unless_filemode_is_off(tmp_path: Path) -> None:
    path = tmp_path / "f.py"
    path.write_bytes(BODY)

    def answer(mode: str, bits: int, check_mode: bool = True) -> bool:
        path.chmod(bits)
        return _differs(tmp_path, mode=mode, check_mode=check_mode)

    assert answer("100755", 0o644) is True, "the entry says executable, the file is not"
    assert answer("100644", 0o755) is True, "the file is executable, the entry says not"
    assert answer("100755", 0o755) is False
    assert answer("100644", 0o644) is False
    assert answer("100644", 0o654) is False, "only the owner bit counts"
    assert answer("100755", 0o064) is True
    assert answer("100755", 0o644, check_mode=False) is False, "filemode is off"
    assert answer("100644", 0o755, check_mode=False) is False


def test_line_endings_difference_counts_as_unchanged_only_when_asked(
    tmp_path: Path,
) -> None:
    lf = b"a\nb\n"
    path = tmp_path / "f.py"
    path.write_bytes(b"a\r\nb\r\n")
    assert _differs(tmp_path, data=lf, fold_crlf=False) is True
    assert _differs(tmp_path, data=lf, fold_crlf=True) is False
    path.write_bytes(b"a\r\nb\r\nc\r\n")
    assert _differs(tmp_path, data=lf, fold_crlf=True) is True, "a real edit still counts"
    path.write_bytes(b"a\rb\r")
    assert _differs(tmp_path, data=lf, fold_crlf=True) is True, "a lone CR is not CRLF"
    path.write_bytes(b"a\r\nb\r\n")
    assert _differs(tmp_path, data=b"a\r\nb\r\n", fold_crlf=False) is False, "equal bytes"


def test_an_index_entry_that_is_not_a_plain_file_is_edited(tmp_path: Path) -> None:
    (tmp_path / "f.py").write_bytes(BODY)
    assert _differs(tmp_path) is False, "the control"
    for mode in ("120000", "160000", "100664", "040000", ""):
        assert _differs(tmp_path, mode=mode) is True, mode
