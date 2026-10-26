"""The default whole-tree Markdown scans survive tracked files that are not on disk.

``git ls-files '*.md'`` keeps listing a file whose deletion is not yet
committed, and a tracked symlink whose target is gone.  A scan that reads every
listed path then dies with ``FileNotFoundError`` instead of reporting findings,
which turns an ordinary state (a rename or cleanup in progress) into a
traceback and makes the ``check-cairn`` gate and the release security check
unusable until the tree is tidied.

Each test builds a throwaway git repository and runs a script's real command
line, so the path under test is the one a person or a hook runs.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_deleted_tracked_markdown.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = CAIRN_ROOT / "scripts"

_SCANS = ["link_check", "sync_doc_snippets", "check_cairn"]
# sync_doc_snippets reports snippet drift, not links, so it has no
# "link to a deleted file" finding to keep.
_LINK_REPORTING_SCANS = ["link_check", "check_cairn"]
_SKIP_LINE = "tracked Markdown file(s) not present on disk"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid",
         "-C", str(repo), *args],
        check=True, capture_output=True, text=True,
    )


def _make_repo(tmp_path: Path, *, with_dangling_symlink: bool) -> Path:
    """A repo with keep.md (links to gone.md), gone.md, and optionally a
    tracked symlink to nowhere; then gone.md is deleted from disk only."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "keep.md").write_text("# Keep\n\nSee [gone](gone.md).\n", encoding="utf-8")
    (repo / "gone.md").write_text("# Gone\n", encoding="utf-8")
    to_add = ["keep.md", "gone.md"]
    if with_dangling_symlink:
        os.symlink("nowhere.md", repo / "dangling.md")
        to_add.append("dangling.md")
    _git(repo, "add", *to_add)
    _git(repo, "commit", "-q", "-m", "seed")
    (repo / "gone.md").unlink()
    return repo


def _run(script: str, repo: Path, *extra: str) -> subprocess.CompletedProcess:
    argv = [sys.executable, "-B", str(SCRIPTS / f"{script}.py"),
            "--root", str(repo), *extra]
    return subprocess.run(argv, capture_output=True, text=True, cwd=str(repo))


@pytest.mark.parametrize("script", _SCANS)
def test_default_scan_completes_when_a_tracked_file_is_deleted_from_disk(
        tmp_path, script):
    repo = _make_repo(tmp_path, with_dangling_symlink=False)
    proc = _run(script, repo)
    assert "Traceback" not in proc.stderr, proc.stderr
    assert "FileNotFoundError" not in proc.stderr, proc.stderr
    assert proc.returncode in (0, 1), proc.stderr


@pytest.mark.parametrize("script", _LINK_REPORTING_SCANS)
def test_a_document_linking_to_the_deleted_file_is_still_flagged(
        tmp_path, script):
    """Skipping the deleted file must hide the file, not the finding."""
    repo = _make_repo(tmp_path, with_dangling_symlink=False)
    proc = _run(script, repo)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "keep.md" in proc.stderr and "gone.md" in proc.stderr, proc.stderr


@pytest.mark.parametrize("script", _SCANS)
def test_skipped_paths_are_counted_on_stderr_and_a_clean_tree_says_nothing(
        tmp_path, script):
    """A deleted file and a dangling symlink are both counted; nothing prints
    when no path is skipped.  The line carries no tool name because the shared
    function that prints it also serves check_cairn."""
    repo = _make_repo(tmp_path, with_dangling_symlink=True)
    proc = _run(script, repo)
    assert f"skipped 2 {_SKIP_LINE}" in proc.stderr, proc.stderr

    clean = tmp_path / "clean"
    clean.mkdir()
    _git(clean, "init", "-q")
    (clean / "ok.md").write_text("# Ok\n", encoding="utf-8")
    _git(clean, "add", "ok.md")
    _git(clean, "commit", "-q", "-m", "seed")
    quiet = _run(script, clean)
    assert "skipped" not in quiet.stderr + quiet.stdout, quiet.stderr


@pytest.mark.parametrize("script", ["link_check", "sync_doc_snippets"])
def test_an_explicitly_named_missing_file_still_fails_loudly(tmp_path, script):
    """Only the default tracked-tree scan tolerates absent files; a path the
    user typed that does not exist is a mistake worth a traceback."""
    repo = _make_repo(tmp_path, with_dangling_symlink=False)
    proc = _run(script, repo, str(repo / "gone.md"))
    assert proc.returncode != 0
    assert "FileNotFoundError" in proc.stderr, proc.stderr


@pytest.mark.parametrize("script", _SCANS)
def test_a_present_file_with_a_non_ascii_name_is_scanned_not_skipped(
        tmp_path, script):
    """Without ``-z``, git prints such a name quoted with octal escapes, so
    the path never resolves.  The scan must read the file, not report it as
    absent: here its broken link has to be found."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "café doc.md").write_text(
        "# Café\n\nSee [nothing](missing-target.md).\n", encoding="utf-8")
    _git(repo, "add", "--all")
    _git(repo, "commit", "-q", "-m", "seed")
    proc = _run(script, repo)
    assert "Traceback" not in proc.stderr, proc.stderr
    assert "skipped" not in proc.stderr, proc.stderr
    if script in _LINK_REPORTING_SCANS:
        assert proc.returncode == 1, proc.stdout + proc.stderr
        assert "missing-target.md" in proc.stderr, proc.stderr
    else:
        assert "1 doc(s) scanned" in proc.stdout + proc.stderr, proc.stdout


@pytest.mark.parametrize("script", _SCANS)
def test_a_tracked_path_that_is_now_a_directory_is_skipped_and_counted(
        tmp_path, script):
    """``exists()`` would let a directory through and the read would raise
    ``IsADirectoryError``; only a regular file (or a link to one) is scanned."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "keep.md").write_text("# Keep\n", encoding="utf-8")
    (repo / "was-a-file.md").write_text("# Was a file\n", encoding="utf-8")
    _git(repo, "add", "--all")
    _git(repo, "commit", "-q", "-m", "seed")
    (repo / "was-a-file.md").unlink()
    (repo / "was-a-file.md").mkdir()
    proc = _run(script, repo)
    assert "Traceback" not in proc.stderr, proc.stderr
    assert f"skipped 1 {_SKIP_LINE}" in proc.stderr, proc.stderr
