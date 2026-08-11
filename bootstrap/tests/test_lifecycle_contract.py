"""Conformance + read-only + authority-contract tests for the lifecycle planner.

This guards the executable form of ``doctrine/lifecycle-contract.md`` --
the read-only checker/planner (``templates/skills/_lib/lifecycle_planner.py``).
It asserts:

* **Read-only by construction** -- every subcommand (``next`` / ``next
  --to`` / ``scan`` / ``guard``) leaves the tree and the git index
  byte-for-byte unchanged, and the module source carries no write/commit
  primitive (the only-reports invariant -- the planner's analogue of the
  inference tool's only-suggests test).
* **The authority contract's negatives** -- a generated review scaffold
  carries no reviewer attribution; a ``-> accepted`` scaffold emits an
  empty verbatim-authorization blockquote and disclaims authenticity; the
  tool reports a *missing* gating precondition rather than presenting a
  transition as ready.
* **The state machine** -- legal transitions match the contract's tables
  for both proposals and plans.
* **The three-way AI-vs-human identity model (R5 + Codex cross-phase)** --
  a vendor-neutral parse classifying known-AI / known-human-Maintainer
  (positive allowlist) / unknown; an unknown Decision author fails closed.
* **Structural conformance** -- the ``scan`` arm flags a corpus whose
  status is not supported by its documentary attestations.

The planner template is a required, always-present source artifact in this
repo, so it is loaded **unconditionally** (no skip guard) -- its absence is
a real failure to surface, and leaving these tests UNMARKED keeps their
node-IDs COLLECTION-ADDED-only for the gate manifest (no skip/xfail
re-anchor).
"""
from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
_PLANNER_PATH = (
    CAIRN_ROOT / "templates" / "skills" / "_lib" / "lifecycle_planner.py"
)


def _load_planner() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "cairn_lifecycle_planner", _PLANNER_PATH
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["cairn_lifecycle_planner"] = module
    spec.loader.exec_module(module)
    return module


planner = _load_planner()


# --- fixtures ----------------------------------------------------------------


def _git(args, cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True,
                   capture_output=True, text=True)


def _make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(["init", "-q"], repo)
    _git(["config", "user.email", "t@example.com"], repo)
    _git(["config", "user.name", "Test"], repo)
    (repo / "dev" / "proposals").mkdir(parents=True)
    (repo / "dev" / "plans").mkdir(parents=True)
    return repo


def _write_proposal(repo: Path, name: str, *, status: str, author: str = "Claude",
                    body: str = "") -> Path:
    path = repo / "dev" / "proposals" / name
    text = (
        f"# {name}\n\n"
        f"**Author**: {author} (Strategy)\n"
        f"**Date opened**: 2026-05-01\n"
        f"**Status**: {status}\n"
        f"**Plan review**: required — Internal\n\n"
        "## Context\n\nx\n"
        f"{body}"
    )
    path.write_text(text, encoding="utf-8")
    return path


def _write_plan(repo: Path, name: str, *, status: str,
                plan_review: str = "required(Internal)", body: str = "") -> Path:
    path = repo / "dev" / "plans" / name
    text = (
        f"# {name}\n\n"
        f"**Status**: {status}\n"
        f"**Plan review**: {plan_review}\n\n"
        "## Scope\n\nx\n"
        f"{body}"
    )
    path.write_text(text, encoding="utf-8")
    return path


def _commit_all(repo: Path) -> None:
    _git(["add", "-A"], repo)
    _git(["commit", "-q", "-m", "fixture"], repo)


def _tree_state(repo: Path) -> dict:
    """sha256 of every tracked-or-untracked file under repo (excluding .git)."""
    state = {}
    for p in sorted(repo.rglob("*")):
        if ".git" in p.parts or not p.is_file():
            continue
        state[str(p.relative_to(repo))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return state


def _porcelain(repo: Path) -> str:
    out = subprocess.run(["git", "status", "--porcelain"], cwd=str(repo),
                         capture_output=True, text=True, check=True)
    return out.stdout


# --- read-only by construction ----------------------------------------------


def test_module_source_has_no_write_or_commit_primitive() -> None:
    """Static proof: the planner source carries no write/stage/commit call."""
    src = _PLANNER_PATH.read_text(encoding="utf-8")
    # No file-write surfaces.
    assert ".write_text(" not in src
    assert ".write_bytes(" not in src
    assert "os.symlink(" not in src
    assert "shutil.move(" not in src and "shutil.copy" not in src
    # No mutating git invocation. The only git the planner runs is read-only
    # (rev-parse / diff --cached --name-only); never add/commit/mv.
    for forbidden in ('"commit"', "'commit'", '"add"', "'add'", '"mv"', "'mv'"):
        assert forbidden not in src, f"unexpected mutating git token {forbidden}"
    # open(...) is used nowhere; reads go through Path.read_text.
    assert "open(" not in src


@pytest.mark.parametrize("argv", [
    ["next", "dev/proposals/p.md"],
    ["next", "dev/proposals/p.md", "--to", "reviewed", "--date", "2026-06-01"],
    ["next", "dev/proposals/p.md", "--to", "accepted", "--date", "2026-06-01"],
    ["scan"],
    ["scan", "--include-archive"],
    ["guard"],
])
def test_every_subcommand_is_read_only(tmp_path, monkeypatch, capsys, argv) -> None:
    """Running any subcommand mutates neither the tree nor the git index."""
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="reviewed", body=(
        "## Review -- Codex (External Reviewer) -- 2026-05-02\n\nfindings\n"
    ))
    _commit_all(repo)
    monkeypatch.chdir(repo)

    before_tree, before_status = _tree_state(repo), _porcelain(repo)
    rc = planner.main(argv)
    capsys.readouterr()
    after_tree, after_status = _tree_state(repo), _porcelain(repo)

    assert isinstance(rc, int)
    assert before_tree == after_tree, "planner changed a file"
    assert before_status == after_status, "planner changed the git index"


# --- the state machine -------------------------------------------------------


def test_proposed_lists_reviewed_as_only_transition(tmp_path, monkeypatch, capsys):
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="proposed")
    monkeypatch.chdir(repo)
    planner.main(["next", "dev/proposals/p.md"])
    out = capsys.readouterr().out
    assert "-> reviewed" in out
    assert "-> accepted" not in out


def test_reviewed_lists_revised_and_decision_targets(tmp_path, monkeypatch, capsys):
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="reviewed", body=(
        "## Review -- Codex (External Reviewer) -- 2026-05-02\n\nx\n"
    ))
    monkeypatch.chdir(repo)
    planner.main(["next", "dev/proposals/p.md"])
    out = capsys.readouterr().out
    for target in ("-> revised", "-> accepted", "-> rejected", "-> superseded"):
        assert target in out


def test_plan_open_required_lists_awaiting_review(tmp_path, monkeypatch, capsys):
    repo = _make_repo(tmp_path)
    _write_plan(repo, "x.md", status="open", plan_review="required(Internal)")
    monkeypatch.chdir(repo)
    planner.main(["next", "dev/plans/x.md"])
    out = capsys.readouterr().out
    assert "-> awaiting-plan-review" in out
    assert "-> executing" not in out


def test_plan_open_not_required_lists_executing(tmp_path, monkeypatch, capsys):
    repo = _make_repo(tmp_path)
    _write_plan(repo, "x.md", status="open", plan_review="not required(doc sync)")
    monkeypatch.chdir(repo)
    planner.main(["next", "dev/plans/x.md"])
    out = capsys.readouterr().out
    assert "-> executing" in out
    assert "-> awaiting-plan-review" not in out


def test_illegal_transition_is_refused(tmp_path, monkeypatch, capsys):
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="proposed")
    monkeypatch.chdir(repo)
    rc = planner.main(["next", "dev/proposals/p.md", "--to", "accepted"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "not a legal next transition" in out


# --- the authority contract (negatives) --------------------------------------


def test_review_scaffold_carries_no_reviewer_attribution(tmp_path, monkeypatch, capsys):
    """A generated review scaffold never attributes a reviewer identity."""
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="proposed", author="Claude")
    monkeypatch.chdir(repo)
    planner.main(["next", "dev/proposals/p.md", "--to", "reviewed",
                  "--date", "2026-06-01"])
    out = capsys.readouterr().out
    # The reviewer/role/model are placeholders the reviewer fills themselves.
    assert "## Review -- <reviewer> (<role>)" in out
    assert "fills their own" in out
    # The tool must not have injected a concrete known agent identity.
    for ident in ("Codex", "Antigravity", "Gemini", "Anthony"):
        assert ident not in out


def test_decision_scaffold_requires_verbatim_blockquote_and_disclaims(
        tmp_path, monkeypatch, capsys):
    """A -> accepted scaffold emits an EMPTY verbatim blockquote + a
    cannot-certify-authenticity disclaimer (R1/R2)."""
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="revised", body=(
        "## Review -- Codex (External Reviewer) -- 2026-05-02\n\nx\n\n"
        "## Response -- Claude (author) -- 2026-05-03\n\nx\n"
    ))
    monkeypatch.chdir(repo)
    planner.main(["next", "dev/proposals/p.md", "--to", "accepted",
                  "--date", "2026-06-01"])
    out = capsys.readouterr().out
    assert "Maintainer authorization (verbatim):" in out
    assert "paste the Maintainer's verbatim authorization here" in out
    assert "cannot certify" in out
    assert "Decision-only commit" in out


def test_accepted_gate_reports_missing_independent_review(
        tmp_path, monkeypatch, capsys):
    """When no independent review exists, -> accepted reports the MISSING
    gating precondition rather than presenting the transition as ready."""
    repo = _make_repo(tmp_path)
    # status=revised (so accepted is legal) but the only review is by the
    # author -> not an independent review.
    _write_proposal(repo, "p.md", status="revised", author="Claude", body=(
        "## Review -- Claude (author) -- 2026-05-02\n\nself\n"
    ))
    monkeypatch.chdir(repo)
    planner.main(["next", "dev/proposals/p.md", "--to", "accepted",
                  "--date", "2026-06-01"])
    out = capsys.readouterr().out
    assert "MISSING" in out
    assert "independent" in out
    assert "does NOT present it as ready" in out


# --- the identity model (R5) -------------------------------------------------


def test_identity_model_classifies_ai_agents_and_human_residual():
    reg = planner._AI_AGENT_REGISTRY
    assert planner._is_ai_agent("Antigravity (External Reviewer)", reg)
    assert planner._is_ai_agent("Codex", reg)
    assert planner._is_ai_agent("Gemini 1.5 Pro", reg)
    # The human Maintainer is the residual: a token NOT on the AI registry.
    assert not planner._is_ai_agent("Anthony", reg)
    assert not planner._is_ai_agent("Maintainer", reg)


def test_identity_registry_is_config_extensible_never_shrinks(tmp_path):
    repo = _make_repo(tmp_path)
    cfg = repo / "dev" / ".cairn"
    cfg.mkdir(parents=True)
    # A new vendor joins by configuration, not a code edit.
    (cfg / "agent-identities.json").write_text(
        '{"ai_agents": ["newvendor"]}', encoding="utf-8")
    reg = planner._load_ai_registry(repo)
    assert "newvendor" in reg
    # Built-ins are never removed by a config (cannot reclassify a known AI).
    assert "claude" in reg and "codex" in reg


def test_malformed_identity_config_falls_back_to_builtin(tmp_path):
    repo = _make_repo(tmp_path)
    cfg = repo / "dev" / ".cairn"
    cfg.mkdir(parents=True)
    (cfg / "agent-identities.json").write_text("{ not json", encoding="utf-8")
    reg = planner._load_ai_registry(repo)
    assert reg == planner._AI_AGENT_REGISTRY


# --- structural conformance / scan -------------------------------------------


def test_scan_clean_corpus_exits_zero(tmp_path, monkeypatch, capsys):
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="proposed")
    _write_plan(repo, "x.md", status="open", plan_review="not required(doc)")
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "structurally sound" in out


def test_scan_flags_accepted_without_decision(tmp_path, monkeypatch, capsys):
    repo = _make_repo(tmp_path)
    # Status says accepted, but there is no Decision section -> violation.
    _write_proposal(repo, "p.md", status="accepted", body=(
        "## Review -- Codex (External Reviewer) -- 2026-05-02\n\nx\n"
    ))
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "no '## Decision' section" in out


def test_scan_flags_review_authored_by_proposal_author(tmp_path, monkeypatch, capsys):
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="reviewed", author="Claude", body=(
        "## Review -- Claude (author) -- 2026-05-02\n\nself-review\n"
    ))
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "reviewer-authorship" in out


def test_scan_flags_decision_without_blockquote(tmp_path, monkeypatch, capsys):
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="accepted", author="Claude", body=(
        "## Review -- Codex (External Reviewer) -- 2026-05-02\n\nx\n\n"
        "## Decision -- Anthony (Maintainer) -- 2026-05-03\n\n"
        "Accepted. (no isolated blockquote here)\n"
    ))
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "no isolated" in out


def test_scan_flags_plan_archived_without_code_review(tmp_path, monkeypatch, capsys):
    repo = _make_repo(tmp_path)
    _write_plan(repo, "x.md", status="archived", plan_review="not required(doc)")
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "no '## Code review' section" in out


def test_decision_authored_by_ai_agent_is_flagged(tmp_path, monkeypatch, capsys):
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="accepted", author="Claude", body=(
        "## Review -- Codex (External Reviewer) -- 2026-05-02\n\nx\n\n"
        "## Decision -- Gemini (Maintainer) -- 2026-05-03\n\n"
        "Accepted.\n\n"
        "> some authorization\n"
    ))
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "AI agent" in out and "human Maintainer authority" in out


# --- Sharpening regressions (External review P2/P3) --------------------------


def test_decision_by_versioned_ai_name_is_flagged(tmp_path, monkeypatch, capsys):
    """P2: a versioned/punctuated AI byline (Claude-3.5) must not launder into
    the human residual and pass the Decision human-authority check."""
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="accepted", author="Claude", body=(
        "## Review -- Codex (External Reviewer) -- 2026-05-02\n\nx\n\n"
        "## Decision -- Claude-3.5 (Maintainer) -- 2026-05-03\n\n"
        "Accepted.\n\n> some authorization\n"
    ))
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "AI agent" in out
    # And the identity helper itself classifies the versioned bylines as AI.
    reg = planner._AI_AGENT_REGISTRY
    assert planner._is_ai_agent("Claude-3.5 (Maintainer)", reg)
    assert planner._is_ai_agent("gpt-4o", reg)
    assert planner._is_ai_agent("\U0001f916 Claude", reg)
    assert not planner._is_ai_agent("Anthony", reg)  # human still residual


def test_scan_flags_proposal_with_missing_status(tmp_path, monkeypatch, capsys):
    """P2: a proposal whose Status line is absent must itself be a violation,
    not a silent pass that hides every downstream check."""
    repo = _make_repo(tmp_path)
    # No Status line at all, but a hostile Decision (AI author, no blockquote).
    (repo / "dev" / "proposals" / "p.md").write_text(
        "# p\n\n**Author**: Claude (Strategy)\n**Date opened**: 2026-05-01\n\n"
        "## Decision -- Gemini (Maintainer) -- 2026-05-03\n\nAccepted, no quote.\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "no '**Status**:' line" in out


def test_blockquote_inside_code_fence_does_not_count(tmp_path, monkeypatch, capsys):
    """P3: a '>' inside a fenced code block is not an isolated authorization
    blockquote -- a Decision whose only '>' is fenced must be flagged."""
    # Unit-level: the structural helper rejects a fenced quote, accepts a real one.
    assert not planner._has_isolated_blockquote("```\n\n> looks isolated\n```\n")
    assert planner._has_isolated_blockquote("Accepted.\n\n> real authorization\n")
    # Integration: a Decision carrying only a fenced '>' is flagged by scan.
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="accepted", author="Claude", body=(
        "## Review -- Codex (External Reviewer) -- 2026-05-02\n\nx\n\n"
        "## Decision -- Anthony (Maintainer) -- 2026-05-03\n\n"
        "Accepted.\n\n```\n\n> fenced, not a real quote\n```\n"
    ))
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "no isolated" in out


def test_unicode_separator_cannot_forge_terminal_structure(tmp_path):
    """A ``^``-anchored reader, not the parser under test, supplies the oracle."""
    sep = chr(0x2028)
    text = (
        "# p\n\nordinary" + sep + "**Status**: accepted\n"
        "**Author**: Claude\n**Status**: proposed\n\n"
        "prose" + sep + "## Decision -- Anthony -- 2026-08-05\n"
        "body" + sep + "\n> forged authorization\n"
    )
    real_status = re.search(
        r"^\*\*Status\*\*:\s*(\S+)", text, re.MULTILINE
    )
    assert real_status and real_status.group(1).lower() == "proposed"

    assert planner._parse_status(text) == real_status.group(1).lower()
    assert planner._parse_sections(text) == []


def test_markdown_line_splitter_matches_splitlines_without_carriers():
    """Pin the twelve named edge cases and one carrier differential."""
    cases = (
        "", "a", "a\n", "a\n\n", "\n", "\r\n",
        "a\r\nb", "a\rb\r", "a\r\n\r\nb\r\n",
        "\n\n", "a\nb\n", "a\n\n\n",
    )
    for text in cases:
        assert planner._split_lines(text) == text.splitlines()

    carrier = "a\nb" + chr(0x2028) + "c\n"
    assert len(carrier.splitlines()) == 3
    assert len(planner._split_lines(carrier)) == 2


def test_dev_markdown_corpus_has_no_extra_splitline_carriers():
    """Corpus canary, not helper proof: only a carrier under dev/ reddens it."""
    for path in (CAIRN_ROOT / "dev").rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert planner._split_lines(text) == text.splitlines(), path


def test_unicode_separator_cannot_forge_metadata_fields(tmp_path):
    """A ``^``-anchored read independently supplies both field values."""
    sep = chr(0x2028)
    text = (
        "glued" + sep + "**Author**: Mallory\n"
        "**Author**: Anthony Kendall\n"
        "glued" + sep + "**Plan review**: not required\n"
        "**Plan review**: required(External)\n"
    )
    for field, expected in (
        ("Author", "Anthony Kendall"),
        ("Plan review", "required(External)"),
    ):
        match = re.search(
            rf"^\*\*{re.escape(field)}\*\*:\s*(.+)$", text, re.MULTILINE
        )
        assert match and match.group(1) == expected
        assert planner._parse_field(text, field) == expected
    assert planner._parse_field(text, "Plan review").lower().startswith("required")


def test_unicode_separator_cannot_isolate_decision_blockquote(tmp_path):
    """A real-line oracle and end-to-end conformance reject fake isolation."""
    sep = chr(0x2028)
    body = "ordinary" + sep + "\n> authorization-shaped text\n"
    lines = re.split(r"\r\n?|\n", body)
    oracle = any(
        line.lstrip().startswith(">") and i > 0 and lines[i - 1].strip() == ""
        for i, line in enumerate(lines)
    )
    assert oracle is False
    assert planner._has_isolated_blockquote(body) is False

    repo = _make_repo(tmp_path)
    path = _write_proposal(
        repo, "p.md", status="accepted", author="Claude",
        body=(
            "## Review -- Codex -- 2026-08-04\n\nok\n\n"
            "## Decision -- Anthony Kendall -- 2026-08-05\n\n" + body
        ),
    )
    _write_identity_config(repo, humans=["Anthony Kendall"])
    art = planner._read_artifact(path)
    violations = planner._conformance_violations(
        art, planner._load_identity_model(repo)
    )
    assert any("no isolated authorization blockquote" in v for v in violations)


# --- Codex cross-phase finding #3: fail-OPEN identity (unknown -> human) ------


def _write_identity_config(repo, ai=None, humans=None):
    import json as _json
    cfg = repo / "dev" / ".cairn"
    cfg.mkdir(parents=True, exist_ok=True)
    body = {}
    if ai is not None:
        body["ai_agents"] = ai
    if humans is not None:
        body["human_maintainers"] = humans
    (cfg / "agent-identities.json").write_text(_json.dumps(body), encoding="utf-8")


def test_identity_model_is_three_way_positive_human(tmp_path):
    """Known-AI / known-human (positive allowlist) / unknown -- never a residual."""
    repo = _make_repo(tmp_path)
    # A roster entry is the COMPLETE display name as it appears in the byline
    # (byline-classification).  The prior form of this node rostered the
    # fragment ["Anthony"] and asserted that `classify("Anthony (Maintainer)")`
    # was human -- the over-match defect written down as an expectation, and
    # an input shape real parsing never produces (`_HEADER_RE` captures the
    # role separately from the name).  Corrected to the full-name roster.
    _write_identity_config(repo, humans=["Anthony Kendall"])
    im = planner._load_identity_model(repo)
    assert im.classify("Gemini (Maintainer)") == "ai"
    assert im.classify("Claude-3.5") == "ai"
    assert im.classify("Anthony Kendall") == "human"        # on the allowlist
    assert im.classify("Sage (Maintainer)") == "unknown"    # novel agent, NOT human
    # No config at all -> no human can be confirmed (fail-closed): all non-AI unknown.
    bare_root = tmp_path / "bare"; bare_root.mkdir()
    bare = planner._load_identity_model(bare_root)
    assert bare.classify("Anthony") == "unknown"
    assert bare.classify("Gemini") == "ai"


def test_decision_by_unknown_identity_is_flagged_fail_closed(tmp_path, monkeypatch, capsys):
    """The Codex reproducer: an accepted proposal with a quoted Decision by a
    NOVEL identity ('Sage') and NO configured Maintainer must NOT pass as human."""
    repo = _make_repo(tmp_path)
    _write_proposal(repo, "p.md", status="accepted", author="Claude", body=(
        "## Review -- Codex (External Reviewer) -- 2026-05-02\n\nx\n\n"
        "## Decision -- Sage (Maintainer) -- 2026-05-03\n\n"
        "Accepted.\n\n> a quoted authorization\n"
    ))
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "UNRECOGNIZED identity" in out and "'Sage'" in out


def test_decision_by_configured_human_maintainer_is_accepted(tmp_path, monkeypatch, capsys):
    """A Decision authored by a CONFIGURED human Maintainer is structurally sound
    (the tool still does not authenticate the quote -- that is the operator's)."""
    repo = _make_repo(tmp_path)
    _write_identity_config(repo, humans=["Anthony"])
    _write_proposal(repo, "p.md", status="accepted", author="Claude", body=(
        "## Review -- Codex (External Reviewer) -- 2026-05-02\n\nx\n\n"
        "## Decision -- Anthony (Maintainer) -- 2026-05-03\n\n"
        "Accepted.\n\n> a quoted authorization\n"
    ))
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "structurally sound" in out
    assert "UNRECOGNIZED" not in out


# --- archive-precondition disposition block (deferral-discipline C1) ----------
#
# The planner's archive-precondition recognizer must accept BOTH the new
# `Dispositions:` spelling and the older `Follow-ups migrated to:` one.  The
# older spelling is load-bearing: artifacts archived under it are append-only
# and correct as they stand, so a hard rename would make the adopter-facing
# `scan` report historically-correct records as violations.

_ARCHIVED_PLAN_BODY = (
    "## Plan review -- R -- 2026-05-01\n\nok\n\n"
    "## Code review -- R -- 2026-05-02\n\nok\n\n"
    "## Lasting-truth migration\n\n"
    "**Fidelity sign-off** -- commit abc1234 matches the Revised section.\n\n"
)

_ARCHIVE_PRECONDITION_MSG = "archive precondition"


def _scan_archived_plan(tmp_path, monkeypatch, capsys, block: str) -> str:
    repo = _make_repo(tmp_path)
    _write_plan(repo, "x.md", status="archived",
                body=_ARCHIVED_PLAN_BODY + block)
    monkeypatch.chdir(repo)
    planner.main(["scan"])
    return capsys.readouterr().out


def test_archived_plan_with_dispositions_block_is_not_flagged(
        tmp_path, monkeypatch, capsys):
    """The new spelling satisfies the archive precondition."""
    out = _scan_archived_plan(
        tmp_path, monkeypatch, capsys,
        "Dispositions:\n* the thing -> wontfix (out of scope, no adopter reach)\n",
    )
    assert _ARCHIVE_PRECONDITION_MSG not in out


def test_archived_plan_with_legacy_followups_block_is_not_flagged(
        tmp_path, monkeypatch, capsys):
    """The older spelling still satisfies it -- already-archived records."""
    out = _scan_archived_plan(
        tmp_path, monkeypatch, capsys,
        "Follow-ups migrated to:\n* the thing -> dev/PLANNING.md > Queued\n",
    )
    assert _ARCHIVE_PRECONDITION_MSG not in out


def test_archived_plan_with_neither_block_is_flagged(
        tmp_path, monkeypatch, capsys):
    """Neither spelling present -- the precondition still fails closed."""
    out = _scan_archived_plan(tmp_path, monkeypatch, capsys, "")
    assert _ARCHIVE_PRECONDITION_MSG in out


# --- the review-record gate (review-gate-enforcement, Chunk C: C.1-C.9c) ------
#
# The gate used to clear on the PRESENCE of a section whose heading merely
# starts with "Plan review".  It now clears on the record's conformance to the
# schema in `doctrine/plans.md` (the plan's S1-S9), through ONE predicate,
# `review_record_violations`, consumed by BOTH call sites (S12).
#
# Each node below carries a single-property falsifier -- a mutation that
# reddens THAT node and no other -- demonstrated (applied, run, reverted) and
# recorded in the plan's implementation-verification section, not asserted
# here.  The only thing that runs these nodes is a person typing
# `python -m pytest bootstrap/tests`; Cairn has no CI.
#
# Conformance only, in every node: the gate attests that a tier was DECLARED,
# never that a review happened or that the declaration is true.

_GATE_STEM = "gate-fixture"   # deliberately NOT a key in `_LEGACY_PASSES`


def _pass_block(*, reviewer: str = "R", date: str = "2026-05-01",
                tier: str | None = "External", findings: str | None = "none",
                sharpening: bool = False, level: str = "##",
                response: bool = False) -> str:
    """One review pass in the S1/S2 shape, with each part independently
    omittable so a node can vary exactly one property."""
    out = f"{level} Plan review -- {reviewer} -- {date}\n\n"
    if tier is not None:
        out += f"**Tier**: {tier}\n"
    if findings is not None:
        out += f"**Findings**: {findings}\n"
    out += "\nthe reading.\n\n"
    if sharpening:
        out += "### Sharpening\n\nthe disposition.\n\n"
    if response:
        out += "## Response to plan review -- A -- 2026-05-02\n\nthe reply.\n\n"
    return out


def _plan_art(tmp_path: Path, body: str, *, status: str = "executing",
              plan_review: str = "required(External)",
              stem: str = _GATE_STEM):
    """Parse a plan fixture into an Artifact (the predicate's input)."""
    d = tmp_path / "dev" / "plans"
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{stem}.md"
    path.write_text(
        f"# {stem}\n\n"
        f"**Status**: {status}\n"
        f"**Plan review**: {plan_review}\n\n"
        f"## Scope\n\nx\n\n{body}",
        encoding="utf-8")
    return planner._read_artifact(path)


def _violations(tmp_path: Path, body: str, **kw) -> list:
    return planner.review_record_violations(_plan_art(tmp_path, body, **kw))


# C.1 -- S8 floor: at least one S1 pass must satisfy S5.


def test_c1_floor_requires_a_conforming_pass_that_meets_the_declared_tier(
        tmp_path):
    """S8: the floor is not cleared by presence, and not by a lower tier.

    Two directions, both of which the presence gate cleared: no S1 pass at all
    (only a bare container), and an S1 pass whose declared tier is BELOW the
    required floor.  The tier comparison is what separates the second from a
    clean record."""
    # (a) a conforming External pass on an External floor clears.
    assert _violations(tmp_path, _pass_block(tier="External")) == []
    # (b) no S1 pass at all -> the floor violation, quoting the near miss.
    only_container = _violations(tmp_path, "## Plan review\n\n(awaiting)\n")
    assert len(only_container) == 1
    assert "no conforming pass satisfies it" in only_container[0]
    # (c) an Internal pass does not satisfy an External floor.
    too_low = _violations(tmp_path, _pass_block(tier="Internal"))
    assert len(too_low) == 1
    assert "no conforming pass satisfies it" in too_low[0]
    # ... and the same pass on an Internal floor does clear, so (c) is the
    # comparison failing and not the pass being malformed.
    assert _violations(tmp_path, _pass_block(tier="Internal"),
                       plan_review="required(Internal)") == []


# C.2 -- S1 heading match: H2, `--` separators, an ISO-shaped date.


@pytest.mark.parametrize("near_miss", [
    "### Plan review -- R -- 2026-05-01\n\n**Tier**: External\n"
    "**Findings**: none\n",                      # H3: the wrong level
    "## Plan review -- R\n\n**Tier**: External\n**Findings**: none\n",  # undated
    "## Plan review\n\n(awaiting a reviewer)\n",                        # bare
    "## Plan review tier -- R -- 2026-05-01\n\n**Tier**: External\n"
    "**Findings**: none\n",                      # prefix collision
    "## Plan reviewers -- R -- 2026-05-01\n\n**Tier**: External\n"
    "**Findings**: none\n",                      # prefix collision
])
def test_c2_a_near_miss_heading_is_not_a_pass_and_fails_closed(
        tmp_path, near_miss):
    """S1/S8: each of these cleared the presence gate; none is a pass now.

    And the refusal is the FLOOR sentence -- "no conforming pass has landed" --
    never "a pass with problems": a near miss must not be parsed as a pass and
    then reported for missing fields it was never asked for.  The refusal
    quotes the offending heading so the author is not left guessing which
    near-miss shape they hit."""
    v = _violations(tmp_path, near_miss)
    assert len(v) == 1, v
    assert "no conforming pass satisfies it" in v[0]
    assert "near misses that do NOT count" in v[0]
    assert near_miss.splitlines()[0] in v[0]


# CR1 -- the gate must match S1's exact RAW heading grammar, not merely a
# heading `_HEADER_RE` (the older, more permissive generic parser) happened
# to accept.  Two independent directions, both reproduced against
# `review_record_violations` with a fresh Codex External code review at
# `dd91ccb`..`fd296fb`: shapes `_HEADER_RE` tolerates but S1 does not (must
# NOT be passes), and a shape S1 accepts but `_HEADER_RE` could not even
# produce a Section for (must BE a pass).


@pytest.mark.parametrize("near_miss", [
    "##   Plan review -- R -- 2026-05-01\n\n**Tier**: External\n"
    "**Findings**: none\n",                       # extra spaces after `##`
    "## Plan review  --  R  --  2026-05-01\n\n**Tier**: External\n"
    "**Findings**: none\n",                       # doubled `--` separators
])
def test_cr1_header_re_whitespace_tolerance_is_not_s1_conformance(
        tmp_path, near_miss):
    """`_HEADER_RE`'s `\\s+` around `##` and `--` is looser than S1's single
    spaces.  Before CR1, `_pass_headings` trusted any Section `_HEADER_RE`
    produced and never checked the raw line against S1, so both of these
    cleared the presence gate despite matching no S1 regex."""
    v = _violations(tmp_path, near_miss)
    assert len(v) == 1, v
    assert "no conforming pass satisfies it" in v[0]
    assert "near misses that do NOT count" in v[0]
    assert near_miss.splitlines()[0] in v[0]


def test_cr1_trailing_whitespace_after_the_date_is_not_a_pass(tmp_path):
    """Same defect, isolated: `_HEADER_RE`'s trailing `\\s*` before `$`
    tolerated trailing spaces after the date; S1 has no such allowance.  The
    near-miss quote is right-stripped by `_near_miss_headings` (as it is for
    every other near miss), so the containment check compares the stripped
    form rather than the fixture's own trailing spaces."""
    near_miss = ("## Plan review -- R -- 2026-05-01   \n\n**Tier**: External\n"
                "**Findings**: none\n")
    v = _violations(tmp_path, near_miss)
    assert len(v) == 1, v
    assert "no conforming pass satisfies it" in v[0]
    assert "near misses that do NOT count" in v[0]
    assert near_miss.splitlines()[0].rstrip() in v[0]


def test_cr1_a_reviewer_field_with_literal_parens_is_still_a_conforming_pass(
        tmp_path):
    """The INVERSE mismatch: S1's reviewer group (`[^\\n]+?`) accepts literal
    parentheses, but `_HEADER_RE`'s `(?P<role>[^)\\n]*)` machinery cannot
    parse a line shaped like this at all -- so before CR1, `_parse_sections`
    produced no Section for it, and a conforming pass silently failed to
    count. A synthesized Section must carry a correct body: the `**Tier**:`
    and `**Findings**:` lines below must still be read from it."""
    body = ("## Plan review -- Jane (Lab) Smith -- 2026-05-01\n\n"
           "**Tier**: External\n**Findings**: none\n")
    assert _violations(tmp_path, body) == []


# C.3 -- S1 date: calendar-valid, not merely date-shaped.


@pytest.mark.parametrize("bad", ["2026-99-99", "2026-02-30", "0000-00-00"])
def test_c3_a_date_shaped_impossible_value_is_a_malformed_date(tmp_path, bad):
    """The heading regex accepts these; `date.fromisoformat` refuses them.

    A shape check is not a date contract, and the fail-closed direction is the
    one that matters: an impossible date must not pass silently."""
    v = _violations(tmp_path, _pass_block(date=bad))
    assert any("malformed date" in msg and bad in msg for msg in v), v


def test_c3_a_real_leap_date_is_accepted(tmp_path):
    """The parse is a real date parse, not a stricter regex: 2028-02-29 exists."""
    assert _violations(tmp_path, _pass_block(date="2028-02-29")) == []


# C.4 -- S7: the disposition pairing is POSITIONAL.


def test_c4_findings_raised_requires_a_disposition_in_that_pass(tmp_path):
    """S7, both house forms, and the positional bound.

    The tree uses both `### Sharpening` (inside the pass body) and
    `## Response to plan review` (after the pass, before the next one), so the
    gate accepts either; what it must not accept is a NEIGHBOURING round's
    disposition standing in for this one."""
    # (a) raised + a Sharpening inside its own body -> clean.
    assert _violations(
        tmp_path, _pass_block(findings="raised", sharpening=True)) == []
    # (b) raised + a `## Response to plan review` before the next pass -> clean.
    assert _violations(
        tmp_path, _pass_block(findings="raised", response=True)) == []
    # (c) raised with no disposition at all -> violation.
    bare = _violations(tmp_path, _pass_block(findings="raised"))
    assert len(bare) == 1
    assert "no disposition follows it" in bare[0]
    # (d) the sibling case: round 1 raised findings and has nothing of its own;
    # round 2's Sharpening sits in round 2's body and must not satisfy round 1.
    sibling = _violations(
        tmp_path,
        _pass_block(reviewer="R1", findings="raised")
        + _pass_block(reviewer="R2", date="2026-05-02", findings="raised",
                      sharpening=True))
    assert len(sibling) == 1
    assert "R1" in sibling[0] and "no disposition follows it" in sibling[0]


def test_c4b_one_response_dispositions_the_whole_group(tmp_path):
    """S7's group rule: one Response answers every pass above it.

    A plan declaring `required(A + B)` is reviewed by two obligations in
    sequence and answered once. Under the previous next-pass ceiling the first
    pass of every pair was overtaken before its Response landed, and append-only
    forbids inserting a disposition between two landed reviews -- so the
    artifact could never conform and no author action could fix it. The rule is
    now: a pass is dispositioned iff some `## Response to plan review` follows
    it, which is exactly "the group above this Response and after the last one".
    """
    # (a) two raised passes, ONE Response after both -> both clean.
    assert _violations(
        tmp_path,
        _pass_block(reviewer="R1", findings="raised")
        + _pass_block(reviewer="R2", date="2026-05-02", findings="raised")
        + "## Response to plan review -- A -- 2026-05-03\n\nanswers both.\n\n"
    ) == []
    # (b) arbitrary N: five raised passes, one Response -> all clean.
    five = "".join(
        _pass_block(reviewer=f"R{i}", date=f"2026-05-0{i}", findings="raised")
        for i in range(1, 6))
    assert _violations(
        tmp_path,
        five + "## Response to plan review -- A -- 2026-05-09\n\nanswers all.\n\n"
    ) == []
    # (c) the guard: a pass landing AFTER the Response still owes one.
    after = _violations(
        tmp_path,
        _pass_block(reviewer="R1", findings="raised")
        + "## Response to plan review -- A -- 2026-05-02\n\nanswered.\n\n"
        + _pass_block(reviewer="R2", date="2026-05-03", findings="raised"))
    assert len(after) == 1
    assert "R2" in after[0] and "no disposition follows it" in after[0]
    # (d) no Response anywhere -> every raised pass still violates.
    none = _violations(
        tmp_path,
        _pass_block(reviewer="R1", findings="raised")
        + _pass_block(reviewer="R2", date="2026-05-02", findings="raised"))
    assert len(none) == 2


# CR2 -- S7's second house form is EXACTLY `## Response to plan review`, not
# any kind that merely starts with "response".  Reproduced by a fresh Codex
# External code review at `dd91ccb`..`fd296fb`: an unrelated `## Response`
# or `## Response to proposal review` cleared a raised finding it never
# addressed.


@pytest.mark.parametrize("unrelated_kind", [
    "Response",
    "Response to proposal review",
])
def test_cr2_an_unrelated_response_kind_does_not_satisfy_raised_findings(
        tmp_path, unrelated_kind):
    """A kind that only shares the `response` PREFIX with the documented
    house form must not discharge S7 -- before CR2, `_has_disposition`'s
    `.startswith("response")` let it."""
    body = (
        _pass_block(findings="raised")
        + f"## {unrelated_kind} -- Author -- 2026-05-02\n\nunrelated.\n\n")
    v = _violations(tmp_path, body)
    assert len(v) == 1, v
    assert "no disposition follows it" in v[0]


def test_cr2_the_documented_house_form_still_satisfies_raised_findings(
        tmp_path):
    """The positive control for CR2's fix: the EXACT documented kind, spelled
    with different case, still clears -- S3/S7's field reads stay
    case-insensitive; only the kind-prefix bug is repaired."""
    body = (
        _pass_block(findings="raised")
        + "## response TO plan review -- Author -- 2026-05-02\n\nreply.\n\n")
    assert _violations(tmp_path, body) == []


# C.5 -- S3's three fail-closed directions, on both fields.


@pytest.mark.parametrize("field,body,expected", [
    ("Tier", _pass_block(tier="Reviewer"), "unrecognized Tier value"),
    ("Tier", _pass_block(tier=None,
                         reviewer="Anthony Kendall (Maintainer)"),
     "missing Tier"),
    ("Tier", _pass_block(tier="External")
     + "", "duplicate Tier"),           # body patched below
    ("Findings", _pass_block(findings="some"), "unrecognized Findings value"),
    ("Findings", _pass_block(findings=None), "missing Findings"),
    ("Findings", _pass_block(findings="none"), "duplicate Findings"),
])
def test_c5_each_s3_direction_is_a_violation_not_a_silent_pass(
        tmp_path, field, body, expected):
    """Unrecognized, missing and duplicate each fail closed, per field.

    Unrecognized alone would leave the other two silent, which is the
    fail-open direction that matters.  The DUPLICATE fixtures use two
    **agreeing** occurrences: agreement is a judgement a conformance backstop
    must not make, so agreeing duplicates are still refused.

    The `missing Tier` fixture carries a `(Maintainer)` role parenthetical and
    a human byline, which pins S4 as well: the tier is read from the
    `**Tier**:` line and from NOWHERE else -- not the byline, not the role."""
    if expected.startswith("duplicate"):
        line = f"**{field}**: " + ("External" if field == "Tier" else "none")
        body = body.replace(line + "\n", line + "\n" + line + "\n", 1)
    v = _violations(tmp_path, body)
    assert any(expected in msg for msg in v), (expected, v)


# C.6 -- S6 normalization of the required tier.


def _generator():
    """The legacy-pass generator, loaded as the corpus oracle.

    It supplies the population; the planner is the code under test.  The
    generator deliberately does not import the gate (its own anchored regex),
    so the forms are not enumerated by the predicate that must resolve them."""
    spec = importlib.util.spec_from_file_location(
        "cairn_gen_legacy_passes", CAIRN_ROOT / "scripts" / "gen_legacy_passes.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_c6_every_live_required_form_resolves_to_exactly_one_tier():
    """The live invariant, re-enumerated at every run rather than pinned.

    The count of distinct `required(...)` forms moves with the tree (it was 6,
    then 7, then 9 inside three days); what does not move is that **every**
    review-required artifact resolves to exactly one of `internal` /
    `external`, and none resolves by accident."""
    gen = _generator()
    forms = set()
    for path in gen.artifacts(CAIRN_ROOT):
        rec = gen.scan(path)
        value = str(rec["required"])
        if value.lower().startswith("required"):
            forms.add(value)
    assert forms, "no review-required artifact found -- the oracle is not reading"
    for value in sorted(forms):
        tier, violation = planner.normalize_required_tier(value)
        assert violation is None, (value, violation)
        assert tier in ("internal", "external"), (value, tier)


@pytest.mark.parametrize("field", [
    "required(not External)",   # a negation must not read as its own opposite
    "required()",              # nothing inside the group
    "required",                # no group at all
])
def test_c6_a_form_that_does_not_name_a_tier_fails_closed(field):
    """S6 fails closed: no default tier, and no accidental resolution."""
    tier, violation = planner.normalize_required_tier(field)
    assert tier is None
    assert violation


# C.7 -- S5 ordering: the order is an ORDER, not an equality.


def test_c7_external_satisfies_an_internal_floor_and_a_human_declares_it(
        tmp_path):
    """`declared >= required`, so External clears an Internal floor.

    This also runs `[E1]`'s sharpest case: the published format had no role
    field, so a rule keyed on one would have blocked a human review.  Under S4
    a human declares `**Tier**: External` in the same line-shape an agent does,
    and the gate reads that line and nothing else."""
    assert planner.tier_satisfies("External", "internal") is True
    assert planner.tier_satisfies("Internal", "internal") is True
    assert planner.tier_satisfies("Internal", "external") is False
    human = _pass_block(reviewer="Anthony Kendall (Maintainer)", tier="External")
    assert _violations(tmp_path, human, plan_review="required(Internal)") == []
    assert _violations(tmp_path, human, plan_review="required(External)") == []


# C.8 -- S12: one predicate, both call sites, no drift.


@pytest.mark.parametrize("body", [
    _pass_block(tier="External", findings="none"),
    "## Plan review\n\n(a bare container)\n",
    _pass_block(tier="Internal"),
    _pass_block(findings="raised"),
])
def test_c8_scan_and_the_executing_gate_agree_on_the_same_record(
        tmp_path, body):
    """`scan` cannot tighten while `next --to executing` stays presence-only.

    The same record is put to both public surfaces: `_conformance_violations`
    (what `scan` reports for a plan already `executing`) and
    `_gating_preconditions(..., "executing")` (what `next --to executing`
    requires of a plan still `awaiting-plan-review`).  Status is the only
    difference between the two fixtures.

    **This node asserts AGREEMENT, never a particular verdict.**  Deliberately:
    a node that also pinned what the verdict should be would redden whenever
    any *other* rule changed, so its falsifier would stop being single-property
    and the drift it exists to catch would be buried in the noise.  What the
    verdict should be is C.1-C.9c's business; that the two surfaces reach the
    same one is this node's."""
    identity = planner.IdentityModel(frozenset(), frozenset())
    art_executing = _plan_art(tmp_path, body, status="executing")
    art_awaiting = _plan_art(tmp_path, body, status="awaiting-plan-review")
    expected = planner.review_record_violations(art_executing)
    # The record reads the same whatever the status -- status selects WHEN the
    # predicate is consulted, never WHAT it finds.
    assert planner.review_record_violations(art_awaiting) == expected
    # `scan` reports exactly the predicate's list -- not a subset, not a
    # re-worded summary.
    assert planner._conformance_violations(art_executing, identity) == expected
    gates = planner._gating_preconditions(art_awaiting, "executing", identity)
    review_gates = [g for g in gates if "Plan review" in g[1]]
    assert len(review_gates) == 1, gates
    met, desc = review_gates[0]
    assert met is (expected == [])
    # And the gate names what it withheld the transition for, so the operator
    # is not sent to `scan` to find out why.
    for msg in expected:
        assert msg in desc


# C.9a/b/c -- S9: the legacy population is ENUMERATED, not dated.


@pytest.mark.parametrize("date", ["2020-01-01", "0000-00-00", "2026-05-01"])
def test_c9a_a_pass_outside_the_manifest_gets_no_exemption_whatever_its_date(
        tmp_path, date):
    """The S11 finding, pinned closed.

    Under the replaced design a pass dated before an epoch was exempt from
    S2/S3/S7 **and** satisfied the floor by presence -- so appending
    `## Plan review -- Any Name -- 2020-01-01` bought a permanent exemption by
    typing a smaller number, and `0000-00-00` sorts below every achievable
    epoch.  There is no date comparison left in the gate: admission is
    membership in a committed enumeration, and this stem is not in it."""
    assert _GATE_STEM not in planner._LEGACY_PASSES
    v = _violations(tmp_path, _pass_block(date=date, tier=None, findings=None))
    assert v, f"a non-manifest pass dated {date} was exempted"


def test_c9b_re_appending_an_admitted_heading_is_refused_at_count_plus_one(
        tmp_path):
    """The occurrence COUNT closes the duplicate-append hole.

    A set-valued manifest would admit an admitted digest forever, so copying a
    heading byte-identical to a legacy one would reopen the bypass.  The
    multiset admits exactly the passes that existed when it was generated.
    This plan's own record is the worked example: the same
    `## Plan review -- Codex (External) -- 2026-08-05` heading appears twice,
    byte-identical, so the boundary exercised is `n + 1` rather than the
    `1 -> 2` edge."""
    stem = "review-gate-enforcement"
    admitted = planner._LEGACY_PASSES[stem]
    heading = "## Plan review -- Codex (External) -- 2026-08-05"
    dig = hashlib.sha256(heading.encode("utf-8")).hexdigest()[:16]
    n = admitted[dig]
    assert n >= 2, (
        "the fixture must exercise n + 1 on a count > 1, not the 1 -> 2 edge; "
        f"the manifest now admits {dig} {n} time(s) at {stem}")
    # The fence itself, at the boundary: occurrences 1..n are admitted and
    # n + 1 is not.  Asserted directly on `_is_legacy` so the count property
    # has a check that no change to the S2/S3 messages can move.
    for k in range(1, n + 2):
        assert planner._is_legacy(stem, dig, {dig: k}) is (k <= n), k
    legacy = f"{heading}\n\nan old-format record, no Tier/Findings lines.\n\n"
    # Exactly n occurrences: all admitted, and they satisfy the floor by
    # presence exactly as they did before the schema existed.
    assert _violations(tmp_path, legacy * n, stem=stem) == []
    # One more: occurrence n + 1 is not admitted and must conform.  Its
    # refusal is CARRIED BY S3's missing-field violation -- there is no other
    # signal a non-admitted duplicate can produce, since the n admitted passes
    # already satisfy the floor by presence.  So silencing S3 also silences
    # this half; the boundary assertion above is the part that cannot be.
    over = _violations(tmp_path, legacy * (n + 1), stem=stem)
    assert any("missing Tier" in msg for msg in over), over


def test_c9c_every_manifest_entry_is_re_derived_by_the_generator():
    """S9(c)/(f): the manifest is generated, not hand-editable.

    Subset direction ONLY, deliberately: a pass appended after the manifest was
    generated legitimately exists and legitimately is not in it, so an equality
    check would redden the suite on the next review that lands.  So this node
    catches a FABRICATED entry and manifest drift; it does not catch an entry
    added for a real new pass, and it cannot catch a defect in the generator's
    own regex -- a producer cannot falsify its own output.  Those two residual
    risks are covered by review of a code diff, which is the actual control."""
    live = _generator().build_manifest(CAIRN_ROOT)
    for stem, digests in sorted(planner._LEGACY_PASSES.items()):
        for dig, count in sorted(digests.items()):
            found = live.get(stem, {}).get(dig, 0)
            assert found >= count, (
                f"_LEGACY_PASSES[{stem!r}][{dig!r}] admits {count} pass(es) but "
                f"the generator finds {found} in the tree -- a fabricated or "
                "stale manifest entry")


# ---------------------------------------------------------------------------
# The archive preconditions must test the property they name (2026-08-11).
#
# Two defects, in opposite directions, both found after two plans archived with
# no code review while the gate reported success:
#   * `## Code review` was satisfied by the section's PRESENCE. Every plan
#     scaffolded from dev/plans/_template.md ships that section pre-written as a
#     placeholder, so the gate could never fail.
#   * `Dispositions:` was matched by an unbolded-only pattern, so the
#     repository's own `**Dispositions:**` house style was reported ABSENT --
#     falsely flagging 12 archived plans that each carried a block.
# A precondition that cannot fail and one that fails a correct record are the
# same defect: neither tests the property it names.
# ---------------------------------------------------------------------------

_PLACEHOLDER_REVIEW = (
    "## Code review\n\n*Filled in after implementation commits land.*\n"
)


def test_the_template_placeholder_code_review_is_not_substantive():
    """The exact section dev/plans/_template.md ships must NOT satisfy the
    archive precondition -- otherwise the gate is impossible to fail."""
    assert planner._has_substantive_code_review(_PLACEHOLDER_REVIEW) is False


def test_the_shipped_plan_template_itself_would_not_pass_the_gate():
    """Measured against the real template, not a hand-written imitation: if
    this ever passes, the placeholder has acquired a reviewer marker and the
    gate is back to being unfailable."""
    template = (CAIRN_ROOT / "dev" / "plans" / "_template.md").read_text(
        encoding="utf-8"
    )
    assert planner._has_substantive_code_review(template) is False


def test_a_model_line_makes_a_code_review_substantive():
    body = "## Code review\n\n**Model**: some-model-id\n\nFindings.\n"
    assert planner._has_substantive_code_review(body) is True


def test_a_dated_reviewer_heading_makes_a_code_review_substantive():
    body = "## Code review -- Reviewer A (External) -- 2026-08-10\n\nFindings.\n"
    assert planner._has_substantive_code_review(body) is True


def test_every_code_review_section_is_examined_not_only_the_first():
    """A plan may carry the placeholder AND a real reviewer's section further
    down. Examining only the first section reports the real review as absent --
    the exact error made while measuring this defect's own blast radius."""
    body = (
        _PLACEHOLDER_REVIEW
        + "\n## Code review -- Reviewer A (External) -- 2026-08-10\n\nFindings.\n"
    )
    assert planner._has_substantive_code_review(body) is True


def _plan_on_disk(tmp_path, body: str):
    """A real plan file, read through the planner's own reader -- so these
    tests exercise the parse path the CLI uses, not a hand-built object."""
    d = tmp_path / "dev" / "plans"
    d.mkdir(parents=True, exist_ok=True)
    f = d / "some-plan.md"
    f.write_text(body, encoding="utf-8")
    return planner._read_artifact(f)


_ARCHIVED_HEAD = (
    "# Plan: some-plan\n\n**Status**: archived\n**Author**: Someone\n\n"
)


def test_an_archived_plan_with_only_the_placeholder_is_a_violation(tmp_path):
    """End to end through the reader, not just the helper."""
    art = _plan_on_disk(
        tmp_path,
        _ARCHIVED_HEAD + "**Dispositions:**\n\n* x -> accept\n\n"
        "Fidelity sign-off: someone\n\n" + _PLACEHOLDER_REVIEW,
    )
    assert art.has_substantive_code_review is False
    joined = " ".join(planner._conformance_violations(art, planner.IdentityModel(frozenset(), frozenset())))
    assert "reviewer marker" in joined, joined


def test_the_same_plan_conforms_once_a_real_review_is_appended(tmp_path):
    """The mutant for the test above: add the marker, the violation clears.
    Without this pair, a always-violating checker would look correct."""
    art = _plan_on_disk(
        tmp_path,
        _ARCHIVED_HEAD + "**Dispositions:**\n\n* x -> accept\n\n"
        "Fidelity sign-off: someone\n\n" + _PLACEHOLDER_REVIEW
        + "\n## Code review -- Reviewer A (External) -- 2026-08-10\n\nFindings.\n",
    )
    assert art.has_substantive_code_review is True
    joined = " ".join(planner._conformance_violations(art, planner.IdentityModel(frozenset(), frozenset())))
    assert "reviewer marker" not in joined, joined


def test_dispositions_is_recognized_in_the_repository_house_style(tmp_path):
    """`**Dispositions:**` is what every plan in dev/plans/archive/ actually
    writes; an unbolded-only pattern reported 6 of them as having no block.

    **Assertion changed by plan `archive-precondition-substance`, Chunk A.**
    As `da3e296` wrote it, each form was a bare label with no body and was
    asserted `True` -- which is the presence-for-substance defect that plan
    exists to close, encoded as a test. The house-style intent is preserved and
    is what this still pins: every emphasis form is *recognized*. Each form now
    carries substance, because a bare label must now refuse (see
    `TestArchiveAttestationGrammar`).
    """
    for form in (
        "**Dispositions:** none",
        "Dispositions:\n* x -> accept",
        "*Dispositions:*\n* x -> wontfix (why)",
        "**Follow-ups migrated to:** dev/PLANNING.md",
        "Follow-ups migrated to: dev/PLANNING.md",
    ):
        d = tmp_path / "dev" / "plans"
        d.mkdir(parents=True, exist_ok=True)
        f = d / "p.md"
        f.write_text(f"# Plan\n\n**Status**: archived\n\n{form}\n", encoding="utf-8")
        art = planner._read_artifact(f)
        assert art.has_disposition_attestation is True, f"rejected: {form!r}"


def test_dispositions_absence_is_still_detected(tmp_path):
    """The loosened pattern must not become unfailable in its turn."""
    for form in ("no block here", "Dispositions are recorded elsewhere"):
        d = tmp_path / "dev" / "plans"
        d.mkdir(parents=True, exist_ok=True)
        f = d / "p.md"
        f.write_text(f"# Plan\n\n**Status**: archived\n\n{form}\n", encoding="utf-8")
        art = planner._read_artifact(f)
        assert art.has_disposition_attestation is False, f"accepted: {form!r}"


# ---------------------------------------------------------------------------
# Archive preconditions that test what they name (plan `archive-precondition-
# substance`, Chunk A).  Every gate below used to be a literal `True`, or a
# presence test the shipped template satisfied by itself.
# ---------------------------------------------------------------------------

_LT = "## Lasting-truth migration\n\n"

#: The exact fixture measured against the pre-change tree, where it set BOTH
#: `has_followups_migrated` and `has_fidelity_signoff` to True: an empty label
#: and a sentence promising the work is owed.
_FALSE_PASS = _LT + "**Dispositions:**\n\nLoop-fidelity sign-off is owed at archive.\n"

_REAL_SIGNOFF = ("**Loop-fidelity sign-off.** Commits `3a1b879` match the "
                 "accepted Revised section.\n")


class TestArchiveAttestationGrammar:
    """A1-A4: presence is never enough, and a real record is never refused."""

    def test_the_measured_false_pass_refuses_under_both_gates(self):
        assert planner._has_disposition_attestation(_FALSE_PASS) is False
        assert planner._has_fidelity_signoff(_FALSE_PASS) is False

    def test_explicit_none_is_an_accepted_disposition(self):
        text = _LT + "**Dispositions:** none\n\n" + _REAL_SIGNOFF
        assert planner._has_disposition_attestation(text) is True

    @pytest.mark.parametrize("verb", ["accept", "guard", "wontfix", "defer"])
    def test_each_vocabulary_entry_is_accepted(self, verb):
        text = _LT + f"Dispositions:\n* the thing -> {verb} (why)\n\n" + _REAL_SIGNOFF
        assert planner._has_disposition_attestation(text) is True

    def test_the_legacy_mid_line_block_is_accepted(self):
        # The `^`-anchored predicate rejected this real block; closing that
        # false-fail is A3.  Shape taken from
        # dev/plans/archive/adopter-entry-doc-refresh.md:173.
        text = (_LT + "Archived 2026-06-12. **Follow-ups migrated to:** "
                "`dev/PLANNING.md` > Queued\n\n" + _REAL_SIGNOFF)
        assert planner._has_disposition_attestation(text) is True

    def test_prose_merely_discussing_the_label_refuses(self):
        # Five archived plans carry exactly this shape.  Masking inline code is
        # what separates them from a real block without re-anchoring.
        text = (_LT + "carries the literal `Follow-ups migrated to:` block "
                "naming where each deferred item went, and a `Dispositions:` "
                "label.\n")
        assert planner._has_disposition_attestation(text) is False

    def test_an_empty_label_cannot_borrow_substance_from_a_later_section(self):
        text = (_LT + "**Dispositions:**\n\n## Archive\n\n* thing -> accept\n")
        assert planner._has_disposition_attestation(text) is False

    def test_a_signoff_without_a_commit_id_refuses(self):
        text = _LT + ("Dispositions:\n* x -> accept\n\n"
                      "**Loop-fidelity sign-off.** The chain holds.\n")
        assert planner._has_fidelity_signoff(text) is False

    def test_a_signoff_outside_the_lasting_truth_section_refuses(self):
        text = ("## Scope\n\n**Loop-fidelity sign-off.** `3a1b879` matches the "
                "accepted Revised section.\n\n" + _LT + "**Dispositions:** none\n")
        assert planner._has_fidelity_signoff(text) is False

    def test_the_appended_dated_section_is_read_not_only_the_first(self):
        # A plan carries the template's empty stub and appends the real dated
        # section below it.  Reading only the first match reported the
        # placeholder and rejected 5 real archived sign-offs.
        text = (_LT + "*Filled in at archive time.*\n\n"
                "## Lasting-truth migration -- 2026-08-11\n\n"
                "**Dispositions:** none\n\n" + _REAL_SIGNOFF)
        assert planner._has_fidelity_signoff(text) is True
        assert planner._has_disposition_attestation(text) is True

    def test_the_shipped_plan_template_refuses_its_own_gates(self):
        # A template that satisfies its own precondition is the original defect.
        text = (CAIRN_ROOT / "dev" / "plans" / "_template.md").read_text(
            encoding="utf-8")
        assert planner._has_disposition_attestation(text) is False
        assert planner._has_fidelity_signoff(text) is False


class TestArchiveGatesConsultTheirPredicates:
    """The two `--to archived` gates were literal `True` and always reported met."""

    def test_no_archive_gate_is_hardcoded_true(self, tmp_path):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "fx.md", status="review")
        art = planner._read_artifact(repo / "dev" / "plans" / "fx.md")
        gates = planner._gating_preconditions(
            art, "archived", planner._load_identity_model(repo))
        assert gates, "the archived target must declare gates"
        met = [g for g, _ in gates]
        assert not all(met), (
            "every archived gate reports met on a plan with no dispositions "
            "and no sign-off -- the hardcoded-True defect has returned"
        )
