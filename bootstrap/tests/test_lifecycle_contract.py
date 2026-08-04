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
