"""Tests for the Cairn lifecycle CLI (session-routine skills backend).

Covers Chunk 1 of the executing plan
(`2026-06-01-claude-cairn-vendor-neutral-skills`):

* session-start: gather of commits / tree-state / in-flight threads, plus
  the one idempotent write it always performs (the skills fan-out
  self-heal -- see below); the graceful fallback when no
  handoff-marker commit exists yet.
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

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_PATH = CAIRN_ROOT / "templates" / "skills" / "_lib" / "session.py"

pytestmark = pytest.mark.skipif(
    not MODULE_PATH.exists(), reason="session kernel template not available"
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
    # No "Goodnight" commit exists -> graceful fallback, never a crash.
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


def test_status_reader_uses_markdown_line_boundaries(repo):
    """The expected status comes from an independent ``^``-anchored regex."""
    proposals = repo / "dev" / "proposals"
    proposals.mkdir(parents=True)
    sep = chr(0x2028)
    hostile = proposals / "hostile.md"
    hostile.write_text(
        "prefix" + sep + "**Status**: proposed -- glued text\n"
        "**Status**: open\n",
        encoding="utf-8",
    )
    benign = proposals / "benign.md"
    benign.write_text("**Status**: accepted\n", encoding="utf-8")

    text = hostile.read_text(encoding="utf-8")
    match = re.search(r"^\*\*Status\*\*:\s*(.+)$", text, re.MULTILINE)
    assert match and match.group(1) == "open"
    assert lifecycle._status_of(hostile) == match.group(1)
    assert lifecycle._in_flight(repo) == [
        "proposals/benign.md -- accepted",
        "proposals/hostile.md -- open",
    ]


def test_lifecycle_line_splitter_matches_splitlines_without_carriers():
    """Pin this deliberately duplicated helper independently of the planner."""
    cases = (
        "", "a", "a\n", "a\n\n", "\n", "\r\n",
        "a\r\nb", "a\rb\r", "a\r\n\r\nb\r\n",
        "\n\n", "a\nb\n", "a\n\n\n",
    )
    for text in cases:
        assert lifecycle._split_lines(text) == text.splitlines()
    carrier = "a\nb" + chr(0x2028) + "c\n"
    assert len(carrier.splitlines()) == 3
    assert len(lifecycle._split_lines(carrier)) == 2


def test_status_reader_treats_invalid_utf8_as_unavailable(repo):
    """One malformed artifact cannot suppress either lifecycle survey."""
    proposals = repo / "dev" / "proposals"
    proposals.mkdir(parents=True)
    path = proposals / "invalid.md"
    path.write_bytes(b"**Status**: open\n\xff")
    assert lifecycle._status_of(path) == "(no status line)"
    assert lifecycle._in_flight(repo) == [
        "proposals/invalid.md -- (no status line)"
    ]


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


# --- fold-back surfacing gate (--handoff only) -------------------------------

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




def test_session_end_without_handoff_does_NOT_surface_foldback(
    repo_with_foldback, monkeypatch, capsys
):
    """(g) session-end WITHOUT --handoff does NOT surface fold-back candidates
    and does NOT emit the capture prompt (the --handoff-only gate).
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








# --- session-start's self-description (first-session survivability) --------


def _subparser_help(parser: argparse.ArgumentParser, name: str) -> str:
    """Look up a subcommand's `help=` text from a built parser."""
    for action in parser._actions:  # noqa: SLF001 -- argparse has no public API for this
        if isinstance(action, argparse._SubParsersAction):
            for choice_action in action._choices_actions:
                if choice_action.dest == name:
                    return choice_action.help
    raise AssertionError(f"no subparser named {name!r} in {parser}")


def test_top_level_description_names_the_self_heal_write_not_read_only() -> None:
    description = lifecycle.build_parser().description
    assert "read-only" not in description.lower(), (
        f"top-level description overclaims read-only: {description!r}"
    )
    assert "self-heal" in description, (
        f"top-level description should name the self-heal write: {description!r}"
    )


def test_session_start_help_names_the_self_heal_write_not_read_only() -> None:
    help_text = _subparser_help(lifecycle.build_parser(), "session-start")
    assert "read-only" not in help_text.lower(), (
        f"session-start help overclaims read-only: {help_text!r}"
    )
    assert "self-heal" in help_text, (
        f"session-start help should name the self-heal write: {help_text!r}"
    )


def test_module_docstring_scopes_dry_run_claim_to_session_end() -> None:
    doc = lifecycle.__doc__ or ""
    assert "`session-end` honors `--dry-run`" in doc, (
        "module docstring should scope the --dry-run claim to session-end "
        f"explicitly: {doc!r}"
    )
    # The blanket "every side-effecting subcommand honors --dry-run" claim
    # this replaces would have been false for session-start;
    # it must not have come back.
    assert "every side-effecting subcommand honors" not in doc.lower()


# ---------------------------------------------------------------------------
# The shipped full-handoff path must actually invoke the intent prune.
# The External review replaced the `_prune_intents(...)` call with `pass` and
# every relied-on suite still reported 145 passed -- so a regression could
# silently delete the feature. This test fails if the call is removed, moved
# outside the lock, or disconnected from dry-run.
# ---------------------------------------------------------------------------

def _intent_repo(tmp_path: Path) -> Path:
    """A scratch repo with the intent tool staged and a ledger holding one old
    RELEASED pair (prunable) and one old UNRELEASED claim (must survive)."""
    import datetime as dt
    import json as _json
    import shutil
    root = tmp_path.resolve()
    _init_repo(root)
    _commit(root, "initial commit")
    cairn_root = Path(__file__).resolve().parent.parent.parent
    src = cairn_root / "templates" / "modules" / "team-gated"
    tools = root / "tools"
    tools.mkdir(exist_ok=True)
    (tools / "intent.py").write_bytes((src / "intent.py").read_bytes())
    shutil.copytree(src / "_intent", tools / "_intent")
    old = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=60)).isoformat()
    dev = root / "dev"
    dev.mkdir(exist_ok=True)
    (dev / "intents.jsonl").write_text("".join(
        _json.dumps(r) + "\n" for r in [
            {"event": "claim", "id": "gone", "ts": old, "agent": "a",
             "files": ["x.md"], "action": "old released work"},
            {"event": "release", "id": "gone", "ts": old},
            {"event": "claim", "id": "kept", "ts": old, "agent": "b",
             "files": ["y.md"], "action": "died holding this"},
        ]), encoding="utf-8")
    return root


def test_handoff_prunes_the_intent_surface(tmp_path, monkeypatch, capsys):
    """The real --handoff removes an old released pair and keeps an
    unreleased claim. Replacing the _prune_intents call with `pass` must fail
    this."""
    root = _intent_repo(tmp_path)
    monkeypatch.setenv("CAIRN_HANDOFF_OWNER", "1")
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    monkeypatch.setenv("CAIRN_SESSION", "sessP")
    monkeypatch.chdir(root)

    rc = lifecycle.main(["session-end", "--handoff"])
    out, err = capsys.readouterr()
    assert rc == 0, f"rc={rc}\nstdout={out}\nstderr={err}"

    body = (root / "dev" / "intents.jsonl").read_text(encoding="utf-8")
    assert '"gone"' not in body, (
        f"the old released pair survived the handoff -- prune not invoked?\n{out}"
    )
    assert '"kept"' in body, "an UNRELEASED claim must never be pruned"
    assert "NEVER RELEASED" in out, (
        f"the unreleased claim must be reported at handoff:\n{out}"
    )


def test_handoff_dry_run_does_not_touch_the_intent_surface(
    tmp_path, monkeypatch, capsys,
):
    """The dry-run manifest must describe the prune without performing it."""
    root = _intent_repo(tmp_path)
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    monkeypatch.setenv("CAIRN_SESSION", "sessD")
    monkeypatch.chdir(root)
    before = (root / "dev" / "intents.jsonl").read_bytes()

    rc = lifecycle.main(["session-end", "--handoff", "--dry-run"])
    out, _ = capsys.readouterr()
    assert rc == 0
    assert "would prune released work-intent pairs" in out, out
    assert (root / "dev" / "intents.jsonl").read_bytes() == before


def test_reflection_only_session_end_does_not_touch_the_intent_surface(
    tmp_path, monkeypatch, capsys,
):
    """The non-destructive default must remain non-destructive."""
    root = _intent_repo(tmp_path)
    monkeypatch.setenv("CAIRN_AGENT", "tester")
    monkeypatch.setenv("CAIRN_SESSION", "sessR")
    monkeypatch.chdir(root)
    before = (root / "dev" / "intents.jsonl").read_bytes()

    lifecycle.main(["session-end"])
    capsys.readouterr()
    assert (root / "dev" / "intents.jsonl").read_bytes() == before
