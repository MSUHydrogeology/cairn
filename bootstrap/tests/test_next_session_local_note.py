"""The next-session handoff is a local note, not a shipped file.

Cairn no longer installs ``dev/NEXT_SESSION.md``; the owner writes a local,
git-ignored note at ``dev/reflections/next-session.md`` instead. These nodes
pin the properties of that change, one per property, through the public entry
points (the scripts, the installer, ``upgrade``). A node that checks prose
lists its sources from the tree, so a new copy cannot be missed.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
HANDOFF = "dev/NEXT_SESSION.md"
PLANNING = "dev/PLANNING.md"

# Both copies of the script: Cairn's own and the one adopters receive.
VERIFY_STEMS_TWINS = (
    ROOT / "scripts" / "verify_stems.py",
    ROOT / "templates" / "modules" / "default-on" / "verify_stems.py",
)


def _run_verify_stems(
    script: Path, repo: Path, *args: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-I", str(script), "--root", str(repo), *args],
        capture_output=True, text=True, check=False,
    )


def _planning_only_repo(root: Path) -> Path:
    """A repository with a board file and no handoff file."""
    (root / "dev" / "proposals").mkdir(parents=True)
    (root / "dev" / "plans").mkdir(parents=True)
    (root / PLANNING).write_text("# Board\n", encoding="utf-8")
    return root


def test_the_two_verify_stems_copies_are_byte_identical() -> None:
    first, second = (path.read_bytes() for path in VERIFY_STEMS_TWINS)
    assert first == second


@pytest.mark.parametrize("script", VERIFY_STEMS_TWINS, ids=lambda p: p.parent.name)
def test_verify_stems_skips_an_absent_default_file_and_says_so(
    script: Path, tmp_path: Path,
) -> None:
    repo = _planning_only_repo(tmp_path)
    result = _run_verify_stems(script, repo)
    assert result.returncode == 0, result.stderr
    assert f"verify_stems: skipped {HANDOFF} (absent)" in result.stdout
    ok_line = next(
        line for line in result.stdout.splitlines()
        if line.startswith("verify_stems: OK")
    )
    assert PLANNING in ok_line
    assert HANDOFF not in ok_line


@pytest.mark.parametrize("script", VERIFY_STEMS_TWINS, ids=lambda p: p.parent.name)
def test_verify_stems_flags_a_stem_in_a_present_handoff_file(
    script: Path, tmp_path: Path,
) -> None:
    repo = _planning_only_repo(tmp_path)
    (repo / HANDOFF).write_text(
        "See `2026-01-01-nobody-nothing`.\n", encoding="utf-8",
    )
    result = _run_verify_stems(script, repo)
    assert result.returncode == 1
    assert "2026-01-01-nobody-nothing" in result.stderr
    assert "skipped" not in result.stdout


@pytest.mark.parametrize("script", VERIFY_STEMS_TWINS, ids=lambda p: p.parent.name)
@pytest.mark.parametrize(
    "scan",
    ([HANDOFF], [PLANNING, HANDOFF]),
    ids=("handoff-alone", "both-default-files-named"),
)
def test_verify_stems_refuses_an_explicit_scan_of_a_missing_file(
    script: Path, scan: list[str], tmp_path: Path,
) -> None:
    repo = _planning_only_repo(tmp_path)
    result = _run_verify_stems(script, repo, "--scan", *scan)
    assert result.returncode == 1
    assert f"{HANDOFF}: file not found" in result.stderr
    assert "skipped" not in result.stdout


@pytest.mark.parametrize("script", VERIFY_STEMS_TWINS, ids=lambda p: p.parent.name)
@pytest.mark.parametrize("kind", ("folder", "dangling-link"))
def test_verify_stems_refuses_a_folder_or_dangling_link_at_the_default_path(
    script: Path, kind: str, tmp_path: Path,
) -> None:
    repo = _planning_only_repo(tmp_path)
    if kind == "folder":
        (repo / HANDOFF).mkdir()
    else:
        (repo / HANDOFF).symlink_to(tmp_path / "nowhere.md")
    result = _run_verify_stems(script, repo)
    assert result.returncode == 1
    assert f"{HANDOFF}: file not found" in result.stderr
    assert "skipped" not in result.stdout


@pytest.mark.parametrize("script", VERIFY_STEMS_TWINS, ids=lambda p: p.parent.name)
def test_verify_stems_still_refuses_an_absent_planning_file(
    script: Path, tmp_path: Path,
) -> None:
    repo = _planning_only_repo(tmp_path)
    # Control: with the board file present, the absent handoff file is skipped.
    assert _run_verify_stems(script, repo).returncode == 0
    (repo / PLANNING).unlink()
    result = _run_verify_stems(script, repo)
    assert result.returncode == 1
    assert f"{PLANNING}: file not found" in result.stderr
