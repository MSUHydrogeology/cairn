"""Tests for the Cairn lifecycle CLI (session-routine skills backend).

Covers Chunk 1 of the executing plan
(`2026-06-01-claude-cairn-vendor-neutral-skills`):

* session-start: read-only gather of commits / tree-state / in-flight threads;
  the EP4 graceful fallback when no handoff-marker commit exists yet.
* session-start: optional intent.py is skipped-with-note (not a crash) when the
  coordination-tiers tool is not a sibling -- the default-on skill must not
  hard-require a team-gated module.
* session-end (reflection-only, the safe default): scaffolds the reflection
  file at `dev/reflections/<date>-<agent>.md`; surfaces open threads.
* `--dry-run`: the only side-effecting subcommand writes nothing.
* `--handoff`: refuses (the guarded full-handoff path lands in the next chunk),
  so the tool can never run an unguarded destructive step.
* loud-failure: running outside a git repo fails with an actionable message,
  not a stack trace.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_lifecycle_cli.py
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_PATH = CAIRN_ROOT / "templates" / "skills" / "_lib" / "lifecycle.py"

pytestmark = pytest.mark.skipif(
    not MODULE_PATH.exists(), reason="lifecycle.py template not available"
)


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cairn_lifecycle", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lifecycle = _load()


# --- git scratch-repo helpers ------------------------------------------------


def _run_git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args],
        cwd=str(root),
        check=True,
        capture_output=True,
        text=True,
    )


def _init_repo(root: Path) -> None:
    _run_git(root, "init", "-q")
    _run_git(root, "config", "user.email", "test@example.com")
    _run_git(root, "config", "user.name", "Test")
    _run_git(root, "config", "commit.gpgsign", "false")


def _commit(root: Path, subject: str, *, fname: str = "f.txt") -> None:
    (root / fname).write_text(subject, encoding="utf-8")
    _run_git(root, "add", fname)
    _run_git(root, "commit", "-q", "-m", subject)


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """A scratch git repo with a couple of ordinary commits."""
    root = tmp_path.resolve()
    _init_repo(root)
    _commit(root, "initial commit")
    _commit(root, "add a thing")
    return root


# --- session-start -----------------------------------------------------------


def test_session_start_lists_commits_since_handoff(repo, monkeypatch, capsys):
    _commit(repo, "Goodnight: prior session arc")
    _commit(repo, "work after the handoff")
    monkeypatch.chdir(repo)

    rc = lifecycle.main(["session-start"])

    out = capsys.readouterr().out
    assert rc == 0
    # The range is anchored at the Goodnight commit, so post-handoff work shows
    # and the pre-handoff commits do not.
    assert "work after the handoff" in out
    assert "initial commit" not in out
    assert "commits since last 'Goodnight' handoff" in out


def test_session_start_ep4_fallback_without_handoff(repo, monkeypatch, capsys):
    # No "Goodnight" commit exists -> EP4 graceful fallback, never a crash.
    monkeypatch.chdir(repo)

    rc = lifecycle.main(["session-start", "--fallback-commits", "5"])

    captured = capsys.readouterr()
    assert rc == 0
    assert "initial commit" in captured.out  # the fallback window shows history
    assert "no 'Goodnight' commit found" in captured.err  # the loud note


def test_session_start_surfaces_in_flight_threads(repo, monkeypatch, capsys):
    proposals = repo / "dev" / "proposals"
    proposals.mkdir(parents=True)
    (proposals / "2026-06-01-x-thing.md").write_text(
        "# Thing\n\n**Status**: proposed\n", encoding="utf-8"
    )
    (proposals / "_template.md").write_text("# template\n", encoding="utf-8")
    monkeypatch.chdir(repo)

    lifecycle.main(["session-start"])

    out = capsys.readouterr().out
    assert "2026-06-01-x-thing.md -- proposed" in out
    assert "_template.md" not in out  # the template is not an in-flight thread


def test_session_start_skips_absent_intent_tool(repo, monkeypatch, capsys):
    # intent.py is not a sibling of the template module, so the active-intent
    # read is skipped with a note rather than crashing.
    monkeypatch.chdir(repo)

    rc = lifecycle.main(["session-start"])

    assert rc == 0
    assert "intent.py" in capsys.readouterr().err


# --- session-end (reflection-only) -------------------------------------------


def test_session_end_writes_reflection_scaffold(repo, monkeypatch, capsys):
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    monkeypatch.setenv("CAIRN_SESSION", "sess01")  # deterministic <session> (#50)
    monkeypatch.chdir(repo)

    rc = lifecycle.main(["session-end"])

    assert rc == 0
    refl_dir = repo / "dev" / "reflections"
    written = list(refl_dir.glob("*-tester-sess01.md"))  # <date>-<agent>-<session>
    assert len(written) == 1
    body = written[0].read_text(encoding="utf-8")
    assert "Session reflection -- tester" in body
    assert "## What shipped" in body


def test_session_end_dry_run_writes_nothing(repo, monkeypatch, capsys):
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    monkeypatch.chdir(repo)

    rc = lifecycle.main(["session-end", "--dry-run"])

    assert rc == 0
    refl_dir = repo / "dev" / "reflections"
    assert not refl_dir.exists() or not list(refl_dir.glob("*-tester-*.md"))
    assert "[dry-run] would create" in capsys.readouterr().out


def test_session_end_does_not_clobber_existing_reflection(repo, monkeypatch, capsys):
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    monkeypatch.setenv("CAIRN_SESSION", "sess01")  # same session -> same path (#50)
    refl_dir = repo / "dev" / "reflections"
    refl_dir.mkdir(parents=True)
    existing = refl_dir / f"{lifecycle._today()}-tester-sess01.md"
    existing.write_text("MY HAND-WRITTEN REFLECTION", encoding="utf-8")
    monkeypatch.chdir(repo)

    lifecycle.main(["session-end"])

    assert existing.read_text(encoding="utf-8") == "MY HAND-WRITTEN REFLECTION"
    assert "leaving it untouched" in capsys.readouterr().out


def test_session_end_handoff_refuses_without_marker(repo, monkeypatch, capsys):
    # Full matrix lives in test_lifecycle_failsafe.py; this pins the headline
    # safety property: --handoff without the designation marker refuses
    # (non-interactively) before any destructive step.
    monkeypatch.delenv("CAIRN_HANDOFF_OWNER", raising=False)
    monkeypatch.chdir(repo)

    rc = lifecycle.main(["session-end", "--handoff"])

    assert rc == 1
    assert "no maintainer-designation marker" in capsys.readouterr().err


# --- loud failure ------------------------------------------------------------


def test_outside_git_repo_fails_actionably(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path.resolve())  # not a git repo

    rc = lifecycle.main(["session-start"])

    assert rc == 1
    assert "not inside a git repository" in capsys.readouterr().err


# --- reflection naming: per-session token (#50 / fold-back #46) ---------------


def test_reflection_filename_is_session_distinct(repo, monkeypatch, capsys):
    # The reflection filename must carry a <session> segment so two concurrent
    # same-agent sessions never scaffold the SAME path and clobber each other.
    monkeypatch.chdir(repo)
    monkeypatch.setenv("CAIRN_AGENT", "claude")
    monkeypatch.delenv("CAIRN_SESSION", raising=False)  # -> random per-run token

    lifecycle.main(["session-end"])
    out1 = capsys.readouterr().out
    lifecycle.main(["session-end"])
    out2 = capsys.readouterr().out

    pat = re.compile(r"dev/reflections/(\d{4}-\d{2}-\d{2}-claude-[A-Za-z0-9._-]+)\.md")
    m1, m2 = pat.search(out1), pat.search(out2)
    assert m1 and m2, "reflection path must be <date>-<agent>-<session>.md"
    assert m1.group(1) != m2.group(1), "two runs must resolve distinct sessions"


def test_resolve_session_honors_explicit_override(repo, monkeypatch):
    monkeypatch.setenv("CAIRN_SESSION", "deadbeef")
    assert lifecycle._resolve_session(repo) == "deadbeef"
