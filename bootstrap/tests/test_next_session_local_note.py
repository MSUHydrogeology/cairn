"""The next-session handoff is a local note, not a shipped file.

Cairn no longer installs ``dev/NEXT_SESSION.md``; the owner writes a local,
git-ignored note at ``dev/reflections/next-session.md`` instead. These nodes
pin the properties of that change, one per property, through the public entry
points (the scripts, the installer, ``upgrade``). A node that checks prose
lists its sources from the tree, so a new copy cannot be missed.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
HANDOFF = "dev/NEXT_SESSION.md"
PLANNING = "dev/PLANNING.md"

# Both copies of the script: Cairn's own and the one adopters receive.
VERIFY_STEMS_TWINS = (
    ROOT / "scripts" / "verify_stems.py",
    ROOT / "templates" / "modules" / "default-on" / "verify_stems.py",
)


NOTE = "dev/reflections/next-session.md"
DOCTRINE = ROOT / "doctrine" / "session-routines.md"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid",
         "-C", str(repo), *args],
        capture_output=True, text=True, check=False,
    )


def _tracked(*pathspecs: str) -> list[Path]:
    """Tracked files matching git pathspecs, listed from the tree."""
    out = _git(ROOT, "ls-files", "-z", "--", *pathspecs).stdout
    return [ROOT / name for name in out.split("\0") if name]


def _flat(text: str) -> str:
    """Collapse whitespace so a phrase matches across a line wrap."""
    return " ".join(text.split())


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


# --- the note's rules -------------------------------------------------------

# The doctrine paragraph and every session-end skill tell the writer what the
# note may hold and when the ignore line may be added.
WRITER_PHRASES = (
    "Do not copy text from an issue, a web page or a comment into the note",
    "exits 1 and git does not track the path",
    "exits any other way, stop",
)


def _writer_copies() -> list[Path]:
    return [DOCTRINE, *_tracked("*session-end/SKILL.md")]


def _missing(text: str, phrases: tuple[str, ...]) -> list[str]:
    flat = _flat(text)
    return [phrase for phrase in phrases if phrase not in flat]


def test_the_note_path_is_ignored_and_both_prunes_spare_it(
    tmp_path: Path,
) -> None:
    ignored = _git(ROOT, "check-ignore", "-q", NOTE)
    assert ignored.returncode == 0
    # Control: the folder's guide is tracked, so it is not ignored.
    assert _git(ROOT, "check-ignore", "-q",
                "dev/reflections/README.md").returncode == 1

    folder = tmp_path / "dev" / "reflections"
    folder.mkdir(parents=True)
    old_dated = "2020-01-01-000000-agent-role.md"
    kept_dated = "2099-01-01-000000-agent-role.md"
    for name in (old_dated, kept_dated, "README.md", "next-session.md"):
        (folder / name).write_text("x\n", encoding="utf-8")

    standalone = _load(
        "_nsl_prune_reflections",
        ROOT / "templates" / "modules" / "default-on" / "prune_reflections.py",
    )
    listed = {p.name for p in standalone.prune_reflections(
        folder, keep=1, dry_run=True)}
    assert listed == {old_dated}

    kernel = _load("_nsl_session_kernel", ROOT / "tools" / "session.py")
    pruned = {p.name for p in kernel._prune_reflections(
        tmp_path, 14, dry_run=True)}
    assert pruned == {old_dated}


def test_every_writer_copy_forbids_copying_outside_text_and_limits_the_ignore_remedy() -> None:
    copies = _writer_copies()
    assert len(copies) >= 3, copies
    for copy in copies:
        text = copy.read_text(encoding="utf-8")
        assert _missing(text, WRITER_PHRASES) == [], copy
        # Control: a copy with one phrase removed is reported, phrase by phrase.
        for phrase in WRITER_PHRASES:
            assert _missing(_flat(text).replace(phrase, ""), WRITER_PHRASES) == [
                phrase], (copy, phrase)


def _link_in_path(repo: Path, rel: str) -> bool:
    """True when the path, or any folder above it, is a link."""
    parts = Path(rel).parts
    return any((repo.joinpath(*parts[:n])).is_symlink()
               for n in range(1, len(parts) + 1))


def _clone_with_tracked_link(tmp_path: Path, linked: str) -> Path:
    """A clone of a repository that tracks *linked* as a link out of the tree."""
    source = tmp_path / "source"
    outside = tmp_path / "outside"
    (outside / "reflections").mkdir(parents=True)
    (source / "dev").mkdir(parents=True)
    assert _git(source, "init", "-q").returncode == 0
    (source / ".gitignore").write_text(
        "dev/reflections/*\n!dev/reflections/README.md\n", encoding="utf-8")
    if linked == "dev/reflections":
        (source / "dev" / "reflections").symlink_to(outside / "reflections")
    else:
        (source / "dev").rmdir()
        (source / "dev").symlink_to(outside)
    _git(source, "add", "-A")
    assert _git(source, "commit", "-q", "-m", "x").returncode == 0
    clone = tmp_path / "clone"
    assert subprocess.run(["git", "clone", "-q", str(source), str(clone)],
                          capture_output=True, check=False).returncode == 0
    return clone


@pytest.mark.parametrize("linked", ("dev/reflections", "dev"))
def test_a_linked_reflections_folder_defeats_check_ignore_so_the_rule_walks_the_path(
    tmp_path: Path, linked: str,
) -> None:
    clone = _clone_with_tracked_link(tmp_path, linked)
    note = clone / NOTE
    assert not note.is_symlink() and not note.is_dir()
    assert _git(clone, "ls-files", NOTE).stdout == ""
    assert _git(clone, "check-ignore", "-q", NOTE).returncode == 128
    assert _link_in_path(clone, NOTE)

    # Control: an ordinary clone with the ignore line exits 0 and walks clean.
    ordinary = tmp_path / "ordinary"
    (ordinary / "dev" / "reflections").mkdir(parents=True)
    assert _git(ordinary, "init", "-q").returncode == 0
    (ordinary / ".gitignore").write_text(
        "dev/reflections/*\n!dev/reflections/README.md\n", encoding="utf-8")
    assert _git(ordinary, "check-ignore", "-q", NOTE).returncode == 0
    assert not _link_in_path(ordinary, NOTE)


def test_no_shipped_python_file_names_the_note() -> None:
    """No tool reads or writes the note: a tool that did would turn text an
    earlier agent wrote into something a later one acts on."""
    sources = _tracked("tools/*.py", "scripts/*.py", "templates/*.py",
                       "bootstrap/_scaffold/*.py")
    assert len(sources) > 20, "the listing must reach the shipped sources"

    def naming(files: dict[Path, str]) -> list[Path]:
        return [p for p, body in files.items()
                if "next-session.md" in body.lower()]

    bodies = {p: p.read_text(encoding="utf-8", errors="replace")
              for p in sources}
    assert naming(bodies) == []
    planted = {**bodies, sources[0]: bodies[sources[0]] + f"\n# {NOTE}\n"}
    assert naming(planted) == [sources[0]]


def test_the_session_kernel_copies_are_identical_and_name_no_retired_file() -> None:
    kernel = (ROOT / "tools" / "session.py").read_bytes()
    assert kernel == (ROOT / "templates" / "skills" / "_lib" / "session.py").read_bytes()
    assert b"NEXT_SESSION" not in kernel
