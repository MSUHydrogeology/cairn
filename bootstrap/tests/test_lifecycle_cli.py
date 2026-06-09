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


# --- reflection naming: <agent> tag resolves via the intent identity ----------


def test_resolve_agent_honors_explicit_override(repo, monkeypatch):
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    assert lifecycle._resolve_agent(repo) == "tester"


def test_resolve_agent_falls_back_to_intent_identity(repo, monkeypatch):
    # With CAIRN_AGENT unset, the <agent> tag is the intent identity's tool tag:
    # intent.py whoami -> "claude-e84b19df", digest stripped -> "claude", so the
    # <agent>-<session> tail reconstructs the full identity.
    monkeypatch.delenv("CAIRN_AGENT", raising=False)
    monkeypatch.setattr(lifecycle, "_intent_whoami",
                        lambda root, **kw: "claude-e84b19df")
    assert lifecycle._resolve_agent(repo) == "claude"


def test_resolve_agent_keeps_identity_without_digest_suffix(repo, monkeypatch):
    # Only a genuine 8-hex digest tail is stripped; a hyphenated tool tag (or a
    # digest-less identity) is left intact.
    monkeypatch.delenv("CAIRN_AGENT", raising=False)
    monkeypatch.setattr(lifecycle, "_intent_whoami",
                        lambda root, **kw: "claude-code")
    assert lifecycle._resolve_agent(repo) == "claude-code"


def test_resolve_agent_defaults_to_agent_without_identity(repo, monkeypatch):
    # No override and no intent tool -> the neutral default, never a crash (the
    # default-on skill must not hard-require the team-gated coordination tool).
    monkeypatch.delenv("CAIRN_AGENT", raising=False)
    monkeypatch.setattr(lifecycle, "_intent_whoami", lambda root, **kw: None)
    assert lifecycle._resolve_agent(repo) == "agent"


# --- fold-back surfacing gate (F5: --handoff only) ---------------------------

#: A minimal foldback_suggest.py stub that prints one aging candidate line.
_FOLDBACK_SUGGEST_STUB = """\
#!/usr/bin/env python3
import sys
print("Surfaceable candidates: 1")
print("  - MyAgingCandidate")
sys.exit(0)
"""

#: A minimal ledger with one candidate well past the 7-day grace.
_AGING_LEDGER = (
    "## Open candidates\\n\\n"
    "| Candidate | Type | Size | Status | Source |\\n"
    "|---|---|---|---|---|\\n"
    "| **AgingCandidate** | doctrine | small | candidate |"
    " captured: 2020-01-01 |\\n"
    "\\n## Already synced\\n\\n(empty)\\n"
)


@pytest.fixture()
def repo_with_foldback(tmp_path: Path) -> Path:
    """A scratch git repo with a seeded scripts/foldback_suggest.py stub
    and a fold-back ledger carrying one aging candidate."""
    root = tmp_path.resolve()
    _init_repo(root)
    _commit(root, "initial commit")

    # Seed the scripts/ directory with the stub.
    scripts = root / "scripts"
    scripts.mkdir()
    stub = scripts / "foldback_suggest.py"
    stub.write_text(_FOLDBACK_SUGGEST_STUB, encoding="utf-8")
    stub.chmod(0o755)

    # Seed the fold-back ledger (not required by the lifecycle CLI itself,
    # but makes the fixture realistic; the stub ignores it).
    cairn_dir = root / "dev" / ".cairn"
    cairn_dir.mkdir(parents=True)
    (cairn_dir / "cairn_foldback.md").write_text(
        _AGING_LEDGER, encoding="utf-8"
    )

    return root


def test_handoff_surfaces_foldback_candidates(
    repo_with_foldback, monkeypatch, capsys
):
    """(f) session-end --handoff surfaces aging fold-back candidates."""
    root = repo_with_foldback
    monkeypatch.setenv("CAIRN_HANDOFF_OWNER", "1")
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    monkeypatch.setenv("CAIRN_SESSION", "sessF")
    monkeypatch.chdir(root)

    rc = lifecycle.main(["session-end", "--handoff"])

    out, err = capsys.readouterr()
    assert rc == 0, f"rc={rc}\nstdout={out}\nstderr={err}"
    # The stub emits "Surfaceable candidates: 1"; it must appear in output.
    assert "Surfaceable candidates" in out or "MyAgingCandidate" in out, (
        f"fold-back surfacing output not found in:\n{out}"
    )
    # The standing capture prompt must appear.
    assert "scan today's doctrine activity" in out, (
        f"capture prompt not found in:\n{out}"
    )
    # The manifest line must appear (emitted before the marker check).
    assert "aging fold-back candidates" in out, (
        f"manifest line not found in:\n{out}"
    )


def test_session_end_without_handoff_does_NOT_surface_foldback(
    repo_with_foldback, monkeypatch, capsys
):
    """(g) session-end WITHOUT --handoff does NOT surface fold-back candidates
    and does NOT emit the capture prompt (the F5 gate).
    """
    root = repo_with_foldback
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    monkeypatch.setenv("CAIRN_SESSION", "sessG")
    monkeypatch.chdir(root)

    rc = lifecycle.main(["session-end"])  # no --handoff

    out, _err = capsys.readouterr()
    assert rc == 0
    # Must NOT surface fold-back candidates in the reflection-only path.
    assert "MyAgingCandidate" not in out
    assert "Surfaceable candidates" not in out
    # Must NOT emit the capture prompt.
    assert "scan today's doctrine activity" not in out


# --- lifecycle-metrics v2 snapshot layer -------------------------------------

#: The lifecycle_metrics template source (loaded directly, no scaffold needed).
_LM_PATH = CAIRN_ROOT / "templates" / "modules" / "default-on" / "lifecycle_metrics.py"


def _load_lm() -> ModuleType:
    """Load lifecycle_metrics.py directly from the template source."""
    spec = importlib.util.spec_from_file_location("cairn_lm_snapshot", _LM_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["cairn_lm_snapshot"] = module
    spec.loader.exec_module(module)
    return module


_lm = _load_lm() if _LM_PATH.exists() else None

_SAMPLE_PROPOSAL = (
    "# Sample proposal\n\n"
    "**Author**: Alice (Strategy)\n"
    "**Date opened**: 2026-05-01\n"
    "**Status**: accepted\n\n"
    "## Review -- Bob (External Reviewer) -- 2026-05-02\n\n"
    "* **[P1]** a finding\n\n"
    "## Decision -- Carol -- 2026-05-03\n\n"
    "Accept.\n"
)


@pytest.fixture()
def lm_repo(tmp_path: Path) -> Path:
    """A minimal scratch repo with one proposal, for snapshot tests."""
    root = tmp_path.resolve()
    proposals = root / "dev" / "proposals"
    proposals.mkdir(parents=True)
    (proposals / "2026-05-01-alice-thing.md").write_text(
        _SAMPLE_PROPOSAL, encoding="utf-8"
    )
    return root


@pytest.mark.skipif(_lm is None, reason="lifecycle_metrics.py template not available")
def test_emit_snapshot_creates_indexed_csv(lm_repo: Path) -> None:
    """emit_snapshot() persists an indexed ``<date>-1.csv`` under
    dev/measurement/snapshots/ carrying the unified ``kind,...`` snapshot
    schema.  The injected ``timestamp_utc=`` makes the path deterministic."""
    import datetime

    snap_path, row_count = _lm.emit_snapshot(
        root=lm_repo, timestamp_utc=datetime.datetime(2026, 6, 1)
    )

    assert snap_path == (
        lm_repo / "dev" / "measurement" / "snapshots" / "2026-06-01-1.csv"
    )
    assert snap_path.exists(), "snapshot file was not created"
    assert row_count == 1, "the one sample proposal should yield one row"

    content = snap_path.read_text(encoding="utf-8")
    header = content.splitlines()[0]
    # Unified snapshot schema: a leading ``kind`` column plus the snapshot
    # meta-columns appended after the proposal/plan columns.
    assert header.startswith("kind,"), f"unexpected CSV header: {header!r}"
    assert "snapshot_event" in header
    # The sample proposal row must appear.
    assert "2026-05-01-alice-thing" in content


@pytest.mark.skipif(_lm is None, reason="lifecycle_metrics.py template not available")
def test_emit_snapshot_same_day_coalesces_by_index(lm_repo: Path) -> None:
    """A same-day re-run does NOT overwrite: it coalesces into the next
    monotonic index (``<date>-2.csv``), preserving the audit trail."""
    import datetime

    fixed = datetime.datetime(2026, 6, 1)
    snap_path, _ = _lm.emit_snapshot(root=lm_repo, timestamp_utc=fixed)
    assert snap_path.name == "2026-06-01-1.csv"
    snap_path.write_text("stale content", encoding="utf-8")  # sentinel

    snap_path2, _ = _lm.emit_snapshot(root=lm_repo, timestamp_utc=fixed)
    assert snap_path2 != snap_path, "same-day re-run must not reuse the path"
    assert snap_path2.name == "2026-06-01-2.csv"
    assert snap_path2.exists()
    # The first snapshot is left untouched (audit-trail retention).
    assert snap_path.read_text(encoding="utf-8") == "stale content", (
        "same-day re-run must not overwrite the prior snapshot"
    )


@pytest.mark.skipif(_lm is None, reason="lifecycle_metrics.py template not available")
def test_snapshot_flag_via_main(lm_repo: Path, capsys) -> None:
    """main([..., '--snapshot']) writes an indexed snapshot file under
    dev/measurement/snapshots/ and reports the write on stderr.  The
    snapshot is the only write surface on this path -- no report CSV is
    emitted to stdout."""
    import datetime

    rc = _lm.main(["proposals", "--root", str(lm_repo), "--snapshot"])
    assert rc == 0

    out, err = capsys.readouterr()
    # The --snapshot path is snapshot-only: nothing is written to stdout.
    assert out == "", f"unexpected stdout on --snapshot path: {out!r}"
    # The write is reported on stderr (row count + default event label).
    assert "wrote" in err and "rows to" in err
    assert "event='manual'" in err

    # An indexed snapshot file must have been written for today's UTC date
    # (emit_snapshot stamps the path from datetime.now(UTC)).
    today_str = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    snap_path = (
        lm_repo / "dev" / "measurement" / "snapshots"
        / f"{today_str}-1.csv"
    )
    assert snap_path.exists(), (
        f"snapshot file not found at {snap_path}"
    )
