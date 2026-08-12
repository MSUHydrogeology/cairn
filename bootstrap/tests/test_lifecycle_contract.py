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

import ast
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
                    body: str = "", assurance: str | None = "standard") -> Path:
    """A proposal on disk.

    P1 added `**Assurance path**:` to the default header for the same reason it
    was added to `_pass_block`: after P1 a *conforming* proposal declares one, so
    a fixture omitting it no longer means "a clean proposal".  `assurance=None`
    omits the line, which is how the new nodes exercise the refusal.
    """
    path = repo / "dev" / "proposals" / name
    declaration = "" if assurance is None else f"**Assurance path**: {assurance}\n"
    text = (
        f"# {name}\n\n"
        f"**Author**: {author} (Strategy)\n"
        f"**Date opened**: 2026-05-01\n"
        f"**Status**: {status}\n"
        f"{declaration}"
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
    """**This fixture is [R3-E1]'s executed bypass, and the node that pins it.**

    The plan declares `Plan review: not required(doc)`. Before Chunk C the
    Code-review obligation was carried by a separate `_has_kind` presence test,
    because `review_record_violations` sat behind `requires_review` and a `not
    required` plan never reached it -- so deleting that presence test (which
    R5'' does) would have made exactly this fixture archive **clean**. The
    message asserted below now comes from the one predicate, reached on the
    EFFECTIVE STATE alone.
    """
    repo = _make_repo(tmp_path)
    _write_plan(repo, "x.md", status="archived", plan_review="not required(doc)")
    monkeypatch.chdir(repo)
    rc = planner.main(["scan"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "no conforming '## Code review" in out


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
                response: bool = False,
                commit: str | None = "0123456789abcdef" * 2 + "01234567",
                target: str | None = "chunks A-C",
                prior: str | None = "none",
                assurance: str | None = "standard",
                bold_basis: bool = True,
                trailer: str = "") -> str:
    """One review pass in the S1/S2 shape, with each part independently
    omittable so a node can vary exactly one property.

    **P1 added the four basis fields to the DEFAULT output**, and that is a
    deliberate change to a shared fixture rather than a convenience: after P1 a
    conforming Plan-review pass *is* one that carries the basis, so a fixture
    whose default omitted it would no longer mean "a conforming pass" and the ~30
    nodes built on it would be asserting against a record the contract refuses.
    Each field stays independently omittable so the new nodes can vary exactly
    one, the same shape `_code_review_pass` uses for the Code-review record.
    """
    out = f"{level} Plan review -- {reviewer} -- {date}\n\n"
    mark = "**" if bold_basis else ""
    for name, value in (("Reviewed commit", commit), ("Target", target),
                        ("Prior findings", prior),
                        ("Assurance path", assurance)):
        if value is not None:
            out += f"{mark}{name}{mark}: {value}\n"
    if tier is not None:
        out += f"**Tier**: {tier}\n"
    if findings is not None:
        out += f"**Findings**: {findings}\n"
    out += "\nthe reading.\n\n"
    if trailer:
        out += trailer
    if sharpening:
        out += "### Sharpening\n\nthe disposition.\n\n"
    if response:
        out += "## Response to plan review -- A -- 2026-05-02\n\nthe reply.\n\n"
    return out


#: The four-field review basis, in the bolded house spelling.
#:
#: Added by P1 to the three hand-written pass bodies below.  Each of those nodes
#: tests exactly ONE property -- a synthesized Section's body, an unparseable
#: heading's boundary, the `_LEGACY_PASSES` count fence -- and the basis is
#: orthogonal to all three, so the fields are SUPPLIED rather than the
#: assertions loosened.  In the legacy-fence node that is more than convenience:
#: it makes the scoping of the two exemptions visible in the fixture itself, by
#: showing a pass that `_LEGACY_PASSES` exempts from Tier/Findings still owing
#: the basis its own separate manifest governs.
_BASIS_LINES = ("**Reviewed commit**: " + "0123456789abcdef" * 2 + "01234567\n"
                "**Target**: chunks A-C\n"
                "**Prior findings**: none\n"
                "**Assurance path**: standard\n")


def _plan_art(tmp_path: Path, body: str, *, status: str = "executing",
              plan_review: str = "required(External)",
              stem: str = _GATE_STEM, header_extra: str = ""):
    """Parse a plan fixture into an Artifact (the predicate's input).

    *header_extra* (P5) is one or more extra header lines, placed where a plan's
    metadata block lives -- above the first `##`.  Empty by default, and the
    interpolation is `\\n{header_extra}\\n`, so every pre-P5 caller writes the
    same bytes it always did.  P5 needs the *header* specifically: its trigger
    field is a header declaration, and a fixture that could only put the field in
    the body could not test that boundary.
    """
    d = tmp_path / "dev" / "plans"
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{stem}.md"
    path.write_text(
        f"# {stem}\n\n"
        f"**Status**: {status}\n"
        f"**Plan review**: {plan_review}\n{header_extra}\n"
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
           + _BASIS_LINES
           + "**Tier**: External\n**Findings**: none\n")
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
    # The basis lines are present and the Tier/Findings lines are not: that is
    # precisely the scoping this node now also witnesses.  `_LEGACY_PASSES`
    # exempts this pass from S2/S3/S7; it does NOT exempt it from P1's basis,
    # which has its own manifest and does not name this stem.
    legacy = (f"{heading}\n\n" + _BASIS_LINES
              + "\nan old-format record, no Tier/Findings lines.\n\n")
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
    assert planner._has_code_review_marker(_PLACEHOLDER_REVIEW) is False


def test_the_shipped_plan_template_itself_would_not_pass_the_gate():
    """Measured against the real template, not a hand-written imitation: if
    this ever passes, the placeholder has acquired a reviewer marker and the
    gate is back to being unfailable."""
    template = (CAIRN_ROOT / "dev" / "plans" / "_template.md").read_text(
        encoding="utf-8"
    )
    assert planner._has_code_review_marker(template) is False


def test_a_model_line_makes_a_code_review_substantive():
    body = "## Code review\n\n**Model**: some-model-id\n\nFindings.\n"
    assert planner._has_code_review_marker(body) is True


def test_a_dated_reviewer_heading_makes_a_code_review_substantive():
    body = "## Code review -- Reviewer A (External) -- 2026-08-10\n\nFindings.\n"
    assert planner._has_code_review_marker(body) is True


def test_every_code_review_section_is_examined_not_only_the_first():
    """A plan may carry the placeholder AND a real reviewer's section further
    down. Examining only the first section reports the real review as absent --
    the exact error made while measuring this defect's own blast radius."""
    body = (
        _PLACEHOLDER_REVIEW
        + "\n## Code review -- Reviewer A (External) -- 2026-08-10\n\nFindings.\n"
    )
    assert planner._has_code_review_marker(body) is True


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

#: A fully schema-conforming Code-review pass (Chunk C / R2', R2''), written in
#: the accepted parent's UNBOLDED basis spelling.  `_code_review_pass()` below
#: is the parameterized form; this constant is the clearing default, needed by
#: the archive-precondition pair above it.
_CODE_REVIEW_PASS = (
    "## Code review -- Reviewer A (External) -- 2026-08-10\n\n"
    "Reviewed commit: 0123456789abcdef0123456789abcdef01234567\n"
    "Target: dev/plans/some-plan.md chunks A-C\n"
    "Prior findings: none\n"
    "Assurance path: standard\n"
    "**Model**: some-model-id\n"
    "**Verdict**: SHIP\n"
    "**Findings**: none\n\n"
    "the reading.\n"
)


def test_an_archived_plan_with_only_the_placeholder_is_a_violation(tmp_path):
    """End to end through the reader, not just the helper.

    **Assertion changed by Chunk C (`code-review-blindness` R5'').** The
    property this node names is unchanged and is what it still pins: the shipped
    placeholder does not satisfy the archive obligation. What changed is which
    predicate says so. The marker check that produced the old `reviewer marker`
    wording was one of the two weak Code-review opinions R5'' deletes -- "presence
    becomes a consequence of the schema check rather than a second, weaker
    opinion" -- so the refusal now comes from the schema check, which is strictly
    stronger: `## Code review` is not a conforming pass at all.
    """
    art = _plan_on_disk(
        tmp_path,
        _ARCHIVED_HEAD + "**Dispositions:**\n\n* x -> accept\n\n"
        "Fidelity sign-off: someone\n\n" + _PLACEHOLDER_REVIEW,
    )
    assert art.has_code_review_marker is False
    joined = " ".join(planner._conformance_violations(art, planner.IdentityModel(frozenset(), frozenset())))
    assert "no conforming '## Code review" in joined, joined


def test_the_same_plan_conforms_once_a_real_review_is_appended(tmp_path):
    """The mutant for the test above: add a real review, the violation clears.
    Without this pair, a always-violating checker would look correct.

    **Strengthened by Chunk C.** As written, the appended section was a dated
    heading with a body of `Findings.` and the assertion was
    `"reviewer marker" not in joined` -- which the schema check makes *vacuously*
    true, so the node would have kept passing while testing nothing. The clearing
    fixture is now a schema-conforming pass, and the intermediate state (a dated
    heading with no fields) is asserted to still refuse, which is the half that
    keeps this pair honest.
    """
    dated_only = ("\n## Code review -- Reviewer A (External) -- 2026-08-10\n\n"
                  "Findings.\n")
    art = _plan_on_disk(
        tmp_path,
        _ARCHIVED_HEAD + "**Dispositions:**\n\n* x -> accept\n\n"
        "Fidelity sign-off: someone\n\n" + _PLACEHOLDER_REVIEW + dated_only,
    )
    assert art.has_code_review_marker is True
    joined = " ".join(planner._conformance_violations(art, planner.IdentityModel(frozenset(), frozenset())))
    assert "no conforming '## Code review" not in joined, joined
    assert "missing 'Reviewed commit:'" in joined, joined

    art = _plan_on_disk(
        tmp_path,
        _ARCHIVED_HEAD + "**Dispositions:**\n\n* x -> accept\n\n"
        "Fidelity sign-off: someone\n\n" + _PLACEHOLDER_REVIEW
        + "\n" + _CODE_REVIEW_PASS,
    )
    joined = " ".join(planner._conformance_violations(art, planner.IdentityModel(frozenset(), frozenset())))
    assert "Code review" not in joined, joined


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


class TestMessagesClaimOnlyTheRecordShape:
    """B2/B3: no operator-facing gate may say a review *occurred*.

    The predicate reads text. It cannot distinguish a review from a
    convincingly-shaped section, and the archive gate used to say it could.
    """

    def test_no_gate_description_claims_a_review_occurred(self, tmp_path):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "fx.md", status="review")
        art = planner._read_artifact(repo / "dev" / "plans" / "fx.md")
        identity = planner._load_identity_model(repo)
        said = []
        for target in ("archived", "review", "executing"):
            said += [d for _, d in planner._gating_preconditions(art, target, identity)]
        for d in said:
            assert "review has occurred" not in d, d
            assert "has occurred" not in d, d

    def test_the_predicate_name_does_not_claim_substance(self):
        src = _PLANNER_PATH.read_text(encoding="utf-8")
        assert "def _has_code_review_marker(" in src
        assert "def _has_substantive_code_review(" not in src


# ---------------------------------------------------------------------------
# Chunk C -- the gate inventory.  `[I3]`: enumerate EVERY gate in both `--to`
# lists with the predicate supplying it, so coverage is visible rather than
# inferred from the handful anyone happened to investigate.
# ---------------------------------------------------------------------------

#: Every unconditional (`True`) gate, keyed by a distinctive slice of its
#: description.  Two classes, and the distinction is the point:
#:
#:   INSTRUCTION -- tells the operator what to write next.  It is not a claim
#:   about the artifact, so there is nothing for it to test and `True` is
#:   correct.
#:
#:   UNCHECKED CLAIM -- asserts a property, and reports it met without testing
#:   it.  This is the defect class the plan exists to close.  One survives, and
#:   it is recorded rather than silently tolerated: the planner reads artifact
#:   text and cannot see git history, so closing it needs a contract this plan
#:   does not have.  Routed as a scope question, not widened here.
#:
#:
#: **Chunk E added exactly one row, and no new UNCHECKED CLAIM.**  That is the
#: property `test_only_one_unchecked_claim_survives` exists to hold, and it held
#: by construction: every new-vocabulary target's *substantive* gate goes through
#: `_r6_gate`, so it carries a predicate rather than a `True`.  The one new row is
#: an instruction about what to write next.
#:
#: The `implementing` target's commit-distinctness gate deliberately matches the
#: **existing** UNCHECKED CLAIM row rather than adding a second: it is the same
#: unverifiable claim (the planner reads artifact text and cannot see git
#: history), re-worded to carry the accepted combined fast path's exception.  One
#: claim, two targets, one row -- and the row's key is a prefix of both
#: descriptions so neither can drop out of the inventory unnoticed.
_UNCONDITIONAL_GATES = {
    "append a '## Review'": "INSTRUCTION",
    "append a '## Response'": "INSTRUCTION",
    "append a '## Decision'": "INSTRUCTION",
    "the Decision commit also moves the file": "INSTRUCTION",
    "append a '## Code review' pass": "INSTRUCTION",
    "execution may combine with plan-open": "INSTRUCTION",
    "plan-open and first-implementation commits stay distinct": "UNCHECKED CLAIM",
    # Chunk E -- the plan-side revision loop's disposition record.
    "append a '## Response to plan review'": "INSTRUCTION",
}


def _unconditional_gate_descriptions() -> list[str]:
    """Every `gates.append((True, ...)` description, read from the source."""
    src = _PLANNER_PATH.read_text(encoding="utf-8")
    body = src[src.index("def _gating_preconditions"):]
    body = body[: body.index("\ndef ", 1)]
    out, lines = [], body.split("\n")
    for i, line in enumerate(lines):
        if re.search(r"gates\.append\(\(True,\s*$", line):
            chunk = " ".join(l.strip() for l in lines[i + 1: i + 6])
            joined = "".join(re.findall(r'"([^"]*)"', chunk))
            out.append(re.sub(r"\s+", " ", joined).strip())
    return out


class TestGateInventory:

    def test_every_unconditional_gate_is_inventoried(self):
        # Perturbation: add a `gates.append((True, "something new"))` without an
        # inventory row.  Red.  This is what keeps the sweep swept.
        found = _unconditional_gate_descriptions()
        unlisted = [d for d in found
                    if not any(k in d for k in _UNCONDITIONAL_GATES)]
        assert not unlisted, (
            "unconditional gate(s) with no inventory row -- classify each as "
            f"INSTRUCTION or UNCHECKED CLAIM: {unlisted}"
        )

    def test_the_inventory_has_no_stale_rows(self):
        found = " || ".join(_unconditional_gate_descriptions())
        stale = [k for k in _UNCONDITIONAL_GATES if k not in found]
        assert not stale, f"inventory rows matching no gate: {stale}"

    def test_the_two_archive_gates_are_no_longer_unconditional(self):
        found = " || ".join(_unconditional_gate_descriptions())
        assert "deferred follow-up" not in found
        assert "loop-fidelity sign-off" not in found

    def test_only_one_unchecked_claim_survives(self):
        # If this count rises, a new claim is being reported met without a
        # predicate. If it falls, the remaining one was closed -- update the
        # inventory rather than deleting the guard.
        claims = [k for k, v in _UNCONDITIONAL_GATES.items()
                  if v == "UNCHECKED CLAIM"]
        assert len(claims) == 1, claims


def test_a_real_record_inside_a_fence_is_still_an_attestation():
    """Fences are NOT masked, and this is why.

    `board-drain-guards.md:1274` and `default-security-stance.md:2568` write
    their real disposition records inside a fence to hold column alignment.
    Masking fences -- which looks principled -- cost both of them their
    attestation. Measured, then reverted.
    """
    text = ("## Lasting-truth migration\n\n### Dispositions\n\n"
            "```\nDispositions:\n* [C1] the thing -> accept (commit a0fe4a3)\n```\n")
    assert planner._has_disposition_attestation(text) is True


def test_documentation_illustrates_the_form_with_inline_code():
    """Inline code IS masked, so prose may name the form without becoming it."""
    text = ("## Lasting-truth migration\n\nwrite `Dispositions: none` when "
            "there are no follow-ups.\n")
    assert planner._has_disposition_attestation(text) is False


# B1 -- one boundary set for every pass body, of either record kind.


class TestPassBodyBoundaries:
    """Chunk B, B1: a later pass heading terminates the pass above it **even
    when ``_HEADER_RE`` cannot parse that heading**.

    Before B1 only *synthesized* sections were sliced against the unified
    boundary set; a recognized pass kept whatever body ``_parse_sections`` gave
    it, and ``_parse_sections`` knows nothing about raw S1 lines.  So an
    unparseable later heading was invisible to it, the earlier pass's body ran
    through that heading, and the later pass's attestation lines were counted as
    **the earlier pass's duplicates** -- a silent misattribution that blamed a
    conforming record for its neighbour's shape.
    """

    #: Matches `_S1_PASS_RE` but NOT `_HEADER_RE`: `_HEADER_RE`'s `name` group
    #: is `[^()\n]+?`, so a reviewer carrying parentheses outside the single
    #: `(<role>)` position is rejected outright and produces no Section.
    UNPARSEABLE = "## Plan review -- Bob (a) (b) -- 2026-08-02"

    BODY = (
        "## Plan review -- Alice -- 2026-08-01\n\n"
        + _BASIS_LINES
        + "**Tier**: Internal\n"
        "**Findings**: none\n\n"
        + UNPARSEABLE + "\n\n"
        + _BASIS_LINES
        + "**Tier**: External\n"
        "**Findings**: none\n"
    )

    def test_the_unparseable_heading_is_still_seen_as_a_pass(self, tmp_path):
        """Precondition for the rest: the second heading is a *pass* with no
        Section.  If `_HEADER_RE` ever widens to parse it, this test stops
        exercising the swallowing case and must be re-pointed at a heading that
        still has no Section -- otherwise the nodes below would pass for a
        reason unrelated to what they claim."""
        art = _plan_art(tmp_path, self.BODY)
        passes = planner._pass_headings(art)
        assert [s.name for s, _ in passes] == ["Alice", "Bob (a) (b)"]
        assert not [s for s in art.sections
                    if s.level <= 2 and s.name == "Bob (a) (b)"]

    def test_an_earlier_pass_body_stops_at_an_unparseable_later_heading(
            self, tmp_path):
        art = _plan_art(tmp_path, self.BODY)
        bodies = {s.name: s.body for s, _ in planner._pass_headings(art)}
        assert planner._TIER_LINE_RE.findall(bodies["Alice"]) == ["Internal"]
        assert planner._TIER_LINE_RE.findall(bodies["Bob (a) (b)"]) == ["External"]

    def test_no_pass_is_blamed_for_its_neighbours_attestation_lines(
            self, tmp_path):
        """The observable defect: `duplicate Tier` / `duplicate Findings`
        reported against a record that declares each field exactly once."""
        assert _violations(tmp_path, self.BODY) == []

    def test_reslicing_does_not_mutate_the_shared_section_bodies(
            self, tmp_path):
        """`art.sections` is shared with `_has_disposition`, `_reviewers` and the
        Decision predicates.  B1 corrects the *pass view* only; narrowing a body
        in place would silently change what those consumers see."""
        art = _plan_art(tmp_path, self.BODY)
        before = {s.line_no: s.body for s in art.sections}
        planner._pass_headings(art)
        assert {s.line_no: s.body for s in art.sections} == before


# B3 -- Code-review disposition: exact `Answers:` binding, and the deliberate
# asymmetry against B2's Plan-review group rule.


_CR_HEAD = "## Code review -- Ann -- 2026-08-01\n\nbody\n\n"


def _cr(tmp_path, body, **kw):
    return planner.code_review_binding_violations(_plan_art(tmp_path, body, **kw))


class TestCodeReviewAnswersBinding:
    """Accepted `code-review-blindness` R2'' as sharpened by its Revision 3.

    Six refusal directions, each with its **own** message, because they send a
    reader to different places: an `unmatched` binding reads as "that reviewer
    never existed" while a `malformed` one means the value never parsed.
    Collapsing them would make the second look like the first.
    """

    def test_an_exact_binding_is_clean(self, tmp_path):
        assert _cr(tmp_path, _CR_HEAD + (
            "## Response to code review -- Bob -- 2026-08-02\n\n"
            "Answers: Ann -- 2026-08-01\n")) == []

    def test_a_missing_binding_refuses(self, tmp_path):
        out = _cr(tmp_path, _CR_HEAD + (
            "## Response to code review -- Bob -- 2026-08-02\n\nno field\n"))
        assert len(out) == 1 and "missing 'Answers:'" in out[0]

    def test_a_duplicate_binding_refuses(self, tmp_path):
        out = _cr(tmp_path, _CR_HEAD + (
            "## Response to code review -- Bob -- 2026-08-02\n\n"
            "Answers: Ann -- 2026-08-01\nAnswers: Ann -- 2026-08-01\n"))
        assert len(out) == 1 and "duplicate 'Answers:'" in out[0]

    def test_a_malformed_value_refuses_as_malformed(self, tmp_path):
        out = _cr(tmp_path, _CR_HEAD + (
            "## Response to code review -- Bob -- 2026-08-02\n\n"
            "Answers: Ann, sometime\n"))
        assert len(out) == 1 and "malformed 'Answers:'" in out[0]

    def test_an_unmatched_binding_refuses(self, tmp_path):
        out = _cr(tmp_path, _CR_HEAD + (
            "## Response to code review -- Bob -- 2026-08-02\n\n"
            "Answers: Zed -- 2026-08-01\n"))
        assert len(out) == 1 and "matches no Code-review pass" in out[0]

    def test_an_ambiguous_binding_refuses(self, tmp_path):
        """Revision 3: exactly one match. Two identical headings are legal
        markdown, so the binding -- not the heading -- is what refuses."""
        out = _cr(tmp_path, _CR_HEAD + _CR_HEAD + (
            "## Response to code review -- Bob -- 2026-08-02\n\n"
            "Answers: Ann -- 2026-08-01\n"))
        assert len(out) == 1 and "ambiguous" in out[0]

    def test_a_response_before_its_target_refuses(self, tmp_path):
        out = _cr(tmp_path, (
            "## Response to code review -- Bob -- 2026-08-02\n\n"
            "Answers: Ann -- 2026-08-03\n\n"
            "## Code review -- Ann -- 2026-08-03\n\nbody\n"))
        assert len(out) == 1 and "AFTER this Response" in out[0]

    def test_round_is_omitted_iff_the_target_omits_it(self, tmp_path):
        """R2'': `(round N)` omitted iff the target omits it. A round-less value
        must not bind a numbered pass, or one Response silently answers a pass
        it does not name."""
        out = _cr(tmp_path, (
            "## Code review -- Ann -- 2026-08-01 (round 2)\n\nbody\n\n"
            "## Response to code review -- Bob -- 2026-08-02\n\n"
            "Answers: Ann -- 2026-08-01\n"))
        assert len(out) == 1 and "matches no Code-review pass" in out[0]
        assert _cr(tmp_path, (
            "## Code review -- Ann -- 2026-08-01 (round 2)\n\nbody\n\n"
            "## Response to code review -- Bob -- 2026-08-02\n\n"
            "Answers: Ann -- 2026-08-01 (round 2)\n")) == []

    def test_a_mid_line_answers_in_prose_is_not_a_field(self, tmp_path):
        """The field is full-line anchored. Otherwise a Response discharges a
        pass by *talking about* answering it."""
        out = _cr(tmp_path, _CR_HEAD + (
            "## Response to code review -- Bob -- 2026-08-02\n\n"
            "He Answers: Ann -- 2026-08-01 eventually\n"))
        assert len(out) == 1 and "missing 'Answers:'" in out[0]


class TestTheTwoRecordTypesDisagreeOnPurpose:
    """B4's opposing falsifiers. A Plan review is answered as a **round** (one
    Response dispositions the group); a Code review's findings are answered
    **individually** (each Response names its pass). Identical document shapes,
    opposite correct answers -- so weakening either rule toward the other
    reddens here and not silently elsewhere.
    """

    TWO_PASSES_ONE_RESPONSE_CR = (
        "## Code review -- Ann -- 2026-08-01\n\nb\n\n"
        "## Code review -- Cid -- 2026-08-05\n\nb\n\n"
        "## Response to code review -- Bob -- 2026-08-06\n\n"
        "Answers: Cid -- 2026-08-05\n")

    TWO_PASSES_ONE_RESPONSE_PLAN = (
        "## Plan review -- Ann -- 2026-08-01\n\n"
        "**Tier**: Internal\n**Findings**: raised\n\n"
        "## Plan review -- Cid -- 2026-08-05\n\n"
        "**Tier**: Internal\n**Findings**: raised\n\n"
        "## Response to plan review -- Bob -- 2026-08-06\n\nanswered\n")

    def test_code_review_binds_only_the_named_pass(self, tmp_path):
        """Weakening B3 into B2's group rule reddens this node."""
        art = _plan_art(tmp_path, self.TWO_PASSES_ONE_RESPONSE_CR)
        got = {r: planner.code_review_pass_is_dispositioned(art, ln)
               for ln, r, _d, _n in planner._code_review_pass_lines(art)}
        assert got == {"Ann": False, "Cid": True}

    def test_plan_review_dispositions_the_whole_group(self, tmp_path):
        """Weakening B2 into B3's exact binding -- or back to the pre-286f07d
        positional ceiling -- reddens this node."""
        art = _plan_art(tmp_path, self.TWO_PASSES_ONE_RESPONSE_PLAN)
        got = {sec.name: planner._has_disposition(art, sec)
               for sec, _ in planner._pass_headings(art)}
        assert got == {"Ann": True, "Cid": True}

    def test_a_binding_defect_dispositions_nothing(self, tmp_path):
        """Fail-closed: the alternative is a malformed binding clearing a pass
        it may not even name."""
        art = _plan_art(tmp_path, _CR_HEAD + (
            "## Response to code review -- Bob -- 2026-08-02\n\n"
            "Answers: Ann, sometime\n"))
        assert planner.code_review_pass_is_dispositioned(art, 10) is False


# ---------------------------------------------------------------------------
# Chunk C -- the Code-review record schema.
#
# Contract: accepted `code-review-blindness`, whose **R2 is superseded**.  The
# operative clauses are R2' (the latest pass must CLEAR; there is no disposition
# branch), R2'' (document-order recency, the `(round N)` rules, the `Answers:`
# grammar), R3' (legacy keyed by digest + occurrence count against a named
# baseline commit) and R5'' (one predicate on an explicit EFFECTIVE STATE,
# reached by both callers regardless of the `Plan review:` declaration).
#
# Every node below carries a single-property falsifier -- a mutation applied to
# `templates/skills/_lib/lifecycle_planner.py`, which is the copy this module
# LOADS, then reverted -- recorded in the plan's implementation-verification
# section rather than asserted here.  The only thing that runs these nodes is a
# person typing `python -m pytest bootstrap/tests`; Cairn has no CI.
# ---------------------------------------------------------------------------

_CR_STEM = "code-review-fixture"    # deliberately NOT in either manifest


def _code_review_pass(*, reviewer: str = "Reviewer A (External)",
                      date: str = "2026-08-10", round_n: int | None = None,
                      commit: str | None = "0123456789abcdef" * 2 + "01234567",
                      target: str | None = "chunks A-C",
                      prior: str | None = "none",
                      assurance: str | None = "standard",
                      model: str | None = "some-model-id",
                      verdict: str | None = "SHIP",
                      findings: str | None = "none",
                      bold_basis: bool = False,
                      verdict_line: str | None = None,
                      trailer: str = "") -> str:
    """One Code-review pass, with every part independently omittable so a node
    can vary exactly one property."""
    tail = f" (round {round_n})" if round_n is not None else ""
    out = f"## Code review -- {reviewer} -- {date}{tail}\n\n"
    mark = "**" if bold_basis else ""
    for name, value in (("Reviewed commit", commit), ("Target", target),
                        ("Prior findings", prior), ("Assurance path", assurance)):
        if value is not None:
            out += f"{mark}{name}{mark}: {value}\n"
    if model is not None:
        out += f"**Model**: {model}\n"
    if verdict_line is not None:
        out += verdict_line + "\n"
    elif verdict is not None:
        out += f"**Verdict**: {verdict}\n"
    if findings is not None:
        out += f"**Findings**: {findings}\n"
    return out + "\nthe reading.\n\n" + trailer


def _cr_violations(tmp_path: Path, body: str, *, state: str = "archived",
                   stem: str = _CR_STEM,
                   plan_review: str = "not required(Chunk C fixture)") -> list:
    """The ONE predicate on an explicit effective state (R5'').

    `plan_review` defaults to `not required(...)` on purpose: that is [R3-E1]'s
    executed bypass shape, so every node here also asserts the Code-review half
    is reached without the declaration's help.
    """
    art = _plan_art(tmp_path, body, status=state, plan_review=plan_review,
                    stem=stem)
    return planner.review_record_violations(art, state)


class TestCodeReviewSchema:
    """R2's mandatory fields, read from the scope R2 names."""

    @pytest.mark.parametrize("field,kwargs", [
        ("Reviewed commit", {"commit": None}),
        ("Target", {"target": None}),
        ("Prior findings", {"prior": None}),
        ("Assurance path", {"assurance": None}),
        ("Model", {"model": None}),
        ("Verdict", {"verdict": None}),
        ("Findings", {"findings": None}),
    ])
    def test_each_mandatory_field_is_required_on_its_own(
            self, tmp_path, field, kwargs):
        v = _cr_violations(tmp_path, _code_review_pass(**kwargs))
        assert any(field in msg for msg in v), (field, v)

    def test_a_complete_clearing_pass_is_silent(self, tmp_path):
        """The mutant for every node above: with all seven fields and a clearing
        verdict the record is complete, so an always-violating check is caught."""
        assert _cr_violations(tmp_path, _code_review_pass()) == []

    def test_both_emphasis_spellings_of_the_basis_are_accepted(self, tmp_path):
        """The field NAME is the contract, the emphasis is not. Both spellings
        are live text: the accepted parent writes the basis unbolded, every real
        review in `dev/plans/` writes it bolded."""
        assert _cr_violations(tmp_path, _code_review_pass()) == []
        assert _cr_violations(
            tmp_path, _code_review_pass(bold_basis=True)) == []

    def test_a_duplicate_field_refuses_even_when_the_values_agree(
            self, tmp_path):
        """Agreement is a judgement a conformance backstop must not make."""
        body = _code_review_pass().replace(
            "Prior findings: none\n", "Prior findings: none\nPrior findings: none\n")
        v = _cr_violations(tmp_path, body)
        assert any("duplicate 'Prior findings:'" in m for m in v), v

    def test_an_empty_field_value_refuses(self, tmp_path):
        v = _cr_violations(tmp_path, _code_review_pass(target=""))
        assert any("empty 'Target:'" in m for m in v), v

    def test_fields_below_the_first_h3_do_not_count(self, tmp_path):
        """R2: the mandatory fields sit BEFORE the pass's first H3."""
        v = _cr_violations(tmp_path, _code_review_pass(
            commit=None, trailer="### Coverage\n\nReviewed commit: abc1234\n"))
        assert any("missing 'Reviewed commit:'" in m for m in v), v

    def test_a_repeated_verdict_below_an_h3_is_not_a_duplicate(self, tmp_path):
        """The reason the H3 scope exists rather than being tidiness: real passes
        carry a `### 4. Verdict & Archive Readiness` subsection that repeats the
        verdict, and reading the whole body reports the pass's own summary as a
        duplicate field."""
        assert _cr_violations(tmp_path, _code_review_pass(
            trailer="### 4. Verdict & Archive Readiness\n\n"
                    "**Verdict: SHIP.** Ready to archive.\n")) == []

    def test_an_out_of_vocabulary_assurance_path_refuses(self, tmp_path):
        v = _cr_violations(tmp_path, _code_review_pass(assurance="medium"))
        assert any("unrecognized Assurance path" in m for m in v), v

    def test_a_malformed_date_is_a_violation_before_any_exemption(self, tmp_path):
        v = _cr_violations(tmp_path, _code_review_pass(date="2026-02-30"))
        assert any("malformed date" in m for m in v), v


class TestCodeReviewBoundariesAreCanonical:
    """R4 -- ONE boundary set, of **both** record kinds.

    B1 built the set from `_S1_PASS_RE` alone, because the Code-review grammar
    did not exist yet; R4 asks for both kinds and C2 completes it. The witness
    has to be a heading `_HEADER_RE` cannot parse -- a reviewer field carrying
    parentheses outside the `(<role>)` position is enough -- because every
    heading it *can* parse is already a boundary via `art.sections`, so a
    fixture built from an ordinary heading cannot tell the two designs apart.
    """

    UNPARSEABLE = "Jane (Lab) Smith"

    def test_a_code_review_heading_terminates_the_plan_review_pass_above_it(
            self, tmp_path):
        body = _pass_block(reviewer="R", findings="none") + _code_review_pass(
            reviewer=self.UNPARSEABLE, findings="raised")
        art = _plan_art(tmp_path, body, stem=_CR_STEM,
                        plan_review="required(Internal)")
        plan_pass, = [sec for sec, _dig in planner._pass_headings(art)]
        assert "**Findings**: raised" not in plan_pass.body, plan_pass.body
        assert "**Verdict**" not in plan_pass.body, plan_pass.body
        # And the Plan-review pass keeps its OWN single Findings line, rather
        # than being reported for the later pass's duplicates.
        assert planner.review_record_violations(art, "executing") == []

    def test_the_unparseable_code_review_heading_is_still_a_pass(self, tmp_path):
        """The inverse direction: narrowing the body must not lose the record."""
        art = _plan_art(tmp_path, _code_review_pass(reviewer=self.UNPARSEABLE),
                        status="archived", stem=_CR_STEM,
                        plan_review="not required(Chunk C fixture)")
        assert [r for r in planner._code_review_pass_lines(art)
                if r[1] == self.UNPARSEABLE]
        assert planner.review_record_violations(art, "archived") == []


class TestCodeReviewVerdictClasses:
    """R2' -- two closed classes, and only one of them clears archive."""

    @pytest.mark.parametrize("verdict", planner.CODE_REVIEW_CLEARING_VERDICTS)
    def test_every_clearing_verdict_clears(self, tmp_path, verdict):
        assert _cr_violations(tmp_path, _code_review_pass(verdict=verdict)) == []

    @pytest.mark.parametrize("verdict", planner.CODE_REVIEW_BLOCKING_VERDICTS)
    def test_every_blocking_verdict_refuses(self, tmp_path, verdict):
        v = _cr_violations(tmp_path, _code_review_pass(verdict=verdict))
        assert any("BLOCKING verdict" in m for m in v), (verdict, v)

    @pytest.mark.parametrize("line", [
        "**Verdict: SHIP**",
        "**Verdict: SHIP.** The implementation is clean.",
        "**Verdict**: **SHIP** (0 blocking, 0 substantive)",
        "Verdict: Accept-with-followups, applying to the four commits",
    ])
    def test_the_house_forms_parse(self, tmp_path, line):
        """The label and the value share one bold span in 30 of the 38 corpus
        passes. A matcher anchored on `**Verdict**:` alone would miss almost
        every real record while appearing to work on the three others."""
        assert _cr_violations(
            tmp_path, _code_review_pass(verdict_line=line)) == []

    @pytest.mark.parametrize("line", [
        "**Verdict: REVISE / NOT CLEARED TO ARCHIVE.**",
        "**Verdict: REVISE.** I reviewed the implemented chunks.",
    ])
    def test_the_blocking_house_forms_parse_as_blocking(self, tmp_path, line):
        v = _cr_violations(tmp_path, _code_review_pass(verdict_line=line))
        assert any("BLOCKING verdict" in m for m in v), v

    @pytest.mark.parametrize("verdict", [
        "SHIP but actually BLOCK", "looks fine", "approved", "LGTM"])
    def test_an_out_of_vocabulary_verdict_refuses(self, tmp_path, verdict):
        """Trailing prose is tolerated only AFTER a clause break, never inside
        the token -- otherwise `SHIP but actually BLOCK` parses as `SHIP`."""
        v = _cr_violations(tmp_path, _code_review_pass(verdict=verdict))
        assert any("unrecognized Verdict value" in m for m in v), (verdict, v)

    def test_a_duplicate_verdict_in_scope_refuses(self, tmp_path):
        body = _code_review_pass().replace(
            "**Verdict**: SHIP\n", "**Verdict**: SHIP\n**Verdict**: PASS\n")
        v = _cr_violations(tmp_path, body)
        assert any("duplicate Verdict" in m for m in v), v

    def test_findings_raised_with_a_clearing_verdict_is_complete(self, tmp_path):
        """[A1]: the common case. A schema must not criminalise it -- a reviewer
        who raises findings and still ships has written a complete record."""
        assert _cr_violations(
            tmp_path, _code_review_pass(findings="raised")) == []

    def test_a_response_does_not_clear_a_blocking_verdict(self, tmp_path):
        """**R2', and the reason R2 was superseded.** [R2-E1]: letting an
        author's own Response convert `REVISE` into archive eligibility would
        weaken the accepted parent's independent-correction-review boundary --
        which this amendment exists to SUPPLY, not to weaken. The binding below
        is exact and correctly positioned, and it still does not clear."""
        body = _code_review_pass(verdict="REVISE") + (
            "## Response to code review -- Author -- 2026-08-11\n\n"
            "Answers: Reviewer A (External) -- 2026-08-10\n\n"
            "every finding corrected.\n")
        v = _cr_violations(tmp_path, body)
        assert any("BLOCKING verdict" in m for m in v), v
        assert not any("Answers" in m for m in v), v

    def test_a_later_independent_pass_is_what_clears_it(self, tmp_path):
        """The mutant for the node above: the correction loop's step 4."""
        body = _code_review_pass(verdict="REVISE") + (
            "## Response to code review -- Author -- 2026-08-11\n\n"
            "Answers: Reviewer A (External) -- 2026-08-10\n\n"
            "every finding corrected.\n\n"
        ) + _code_review_pass(reviewer="Reviewer B (External)",
                              date="2026-08-12", prior="CR1-CR3")
        assert _cr_violations(tmp_path, body) == []


class TestCodeReviewRecency:
    """R2'' -- document order is authoritative."""

    def test_a_clearing_pass_earlier_does_not_rescue_a_blocking_latest(
            self, tmp_path):
        body = _code_review_pass(date="2026-08-09") + _code_review_pass(
            reviewer="Reviewer B (External)", date="2026-08-10",
            verdict="BLOCK")
        v = _cr_violations(tmp_path, body)
        assert any("BLOCKING verdict" in m for m in v), v

    def test_only_the_latest_pass_is_held_to_the_schema(self, tmp_path):
        """A superseded earlier pass is history; the record that governs is the
        last one. Holding every pass to the schema would redden a plan for a
        record its own later review already replaced."""
        body = _code_review_pass(date="2026-08-09", commit=None, model=None,
                                 verdict=None) + _code_review_pass()
        assert _cr_violations(tmp_path, body) == []

    @pytest.mark.parametrize("rounds,ok", [
        ((1, 2), True), ((1, 3), True),
        ((2, 1), False), ((2, 2), False), ((1, 1), False),
    ])
    def test_rounds_on_one_date_must_be_unique_and_increasing(
            self, tmp_path, rounds, ok):
        body = "".join(
            _code_review_pass(reviewer=f"Reviewer {i}", round_n=n)
            for i, n in enumerate(rounds))
        v = [m for m in _cr_violations(tmp_path, body)
             if "strictly increasing" in m]
        assert (not v) is ok, (rounds, v)

    def test_an_unnumbered_and_a_numbered_pass_on_one_date_refuse(
            self, tmp_path):
        body = _code_review_pass() + _code_review_pass(
            reviewer="Reviewer B", round_n=2)
        v = _cr_violations(tmp_path, body)
        assert any("either every pass carries a round" in m for m in v), v

    def test_two_unnumbered_passes_on_one_date_are_allowed(self, tmp_path):
        """One archived plan has exactly this -- two reviewers on 2026-08-05 --
        and the ambiguity it creates is answered where it bites, in the
        `Answers:` exactly-one-match rule ([R3-E2]), not by refusing the passes.
        """
        body = _code_review_pass(verdict="Accept") + _code_review_pass(
            reviewer="Reviewer B (External)")
        assert _cr_violations(tmp_path, body) == []

    def test_rounds_on_different_dates_are_independent(self, tmp_path):
        body = _code_review_pass(date="2026-08-09", round_n=7) + \
            _code_review_pass(date="2026-08-10", round_n=1)
        assert _cr_violations(tmp_path, body) == []


class TestCodeReviewBindingReachesTheGate:
    """B3 built the `Answers:` predicate; C1 is what wires it in."""

    @pytest.mark.parametrize("answers,expected", [
        (None, "missing 'Answers:'"),
        ("Answers: nobody, sometime", "malformed 'Answers:'"),
        ("Answers: Ghost -- 2026-08-10", "matches no Code-review pass"),
    ])
    def test_a_binding_defect_surfaces_through_the_one_predicate(
            self, tmp_path, answers, expected):
        body = _code_review_pass() + (
            "## Response to code review -- Author -- 2026-08-11\n\n"
            + (answers + "\n" if answers else "") + "the reply.\n")
        v = _cr_violations(tmp_path, body)
        assert any(expected in m for m in v), (expected, v)

    def test_a_correct_binding_is_silent(self, tmp_path):
        body = _code_review_pass() + (
            "## Response to code review -- Author -- 2026-08-11\n\n"
            "Answers: Reviewer A (External) -- 2026-08-10\n\nthe reply.\n")
        assert _cr_violations(tmp_path, body) == []


class TestCodeReviewLegacyEnumeration:
    """R3' -- forward-only, keyed non-replayably against a named baseline."""

    def test_the_manifest_is_re_derived_by_the_generator(self):
        """The C4/C3 separation, checked in the only direction that is sound.

        Subset only, deliberately, for the reason the Plan-review manifest's own
        node states: a record appended after the baseline legitimately exists and
        legitimately is not in the manifest, so an equality check would redden on
        the next review that lands. This catches a FABRICATED or stale entry. It
        cannot catch a defect in the generator's own regex -- a producer cannot
        falsify its own output -- which is why the committed literal was ALSO
        derived by a second, unrelated path (`git ls-tree` / `grep -E` /
        `shasum -a 256` at the shell) and the two agreed byte-for-byte.
        """
        gen = _code_review_generator()
        live = gen.build_manifest(CAIRN_ROOT, gen.BASELINE_COMMIT)
        for stem, digests in sorted(
                planner._LEGACY_CODE_REVIEW_RECORDS.items()):
            for dig, count in sorted(digests.items()):
                found = live.get(stem, {}).get(dig, 0)
                assert found >= count, (
                    f"_LEGACY_CODE_REVIEW_RECORDS[{stem!r}][{dig!r}] admits "
                    f"{count} but the generator finds {found} at the baseline "
                    "-- a fabricated or stale manifest entry")

    def test_the_baseline_commit_is_the_one_the_manifest_records(self):
        """R3' requires the baseline pinned to ONE named commit recorded in the
        manifest. Two homes for one fact drift silently, so the planner's
        docstring and the generator's constant are compared rather than trusted.
        """
        gen = _code_review_generator()
        src = _PLANNER_PATH.read_text(encoding="utf-8")
        assert gen.BASELINE_COMMIT in src, (
            "the planner's manifest docstring does not record the generator's "
            f"baseline commit {gen.BASELINE_COMMIT}")

    def test_no_live_plans_placeholder_is_admitted(self):
        """**The safety boundary of rule 3, and the reason it is not tidiness.**

        Every live plan ships `## Code review` as a template placeholder.
        Admitting one would let a placeholder satisfy the archive presence
        obligation with no review at all -- the exact defect plan
        `archive-precondition-substance` closed after two plans archived on
        2026-08-11 with no code review while the gate reported success. So the
        container rule reaches only plans already past that gate.
        """
        gen = _code_review_generator()
        offenders = []
        for rel in gen.artifacts(CAIRN_ROOT, gen.BASELINE_COMMIT):
            stem = Path(rel).stem
            rec = gen.scan(gen.read_at(CAIRN_ROOT, rel, gen.BASELINE_COMMIT),
                           stem)
            if rec["status"] == "archived":
                continue
            for heading in rec["containers"]:
                dig = gen.digest(heading)
                if dig in planner._LEGACY_CODE_REVIEW_RECORDS.get(stem, {}):
                    offenders.append((stem, heading))
        assert not offenders, offenders

    def test_a_pass_outside_the_manifest_gets_no_exemption(self, tmp_path):
        assert _CR_STEM not in planner._LEGACY_CODE_REVIEW_RECORDS
        v = _cr_violations(tmp_path, _code_review_pass(
            commit=None, model=None, verdict=None, findings=None))
        assert v, "a non-manifest pass was exempted"

    def test_re_appending_an_admitted_heading_is_refused_at_count_plus_one(
            self, tmp_path):
        """The occurrence COUNT closes the duplicate-append hole. A set-valued
        manifest would admit an admitted digest forever, so copying a heading
        byte-identical to a legacy one would reopen the bypass."""
        stem = "content-scan-detectors"
        heading = "## Code review"
        dig = hashlib.sha256(heading.encode("utf-8")).hexdigest()[:16]
        n = planner._LEGACY_CODE_REVIEW_RECORDS[stem][dig]
        assert n >= 2, (
            "the fixture must exercise n + 1 on a count > 1, not the 1 -> 2 "
            f"edge; the manifest now admits {dig} {n} time(s) at {stem}")
        for k in range(1, n + 2):
            assert planner._is_legacy(
                stem, dig, {dig: k},
                planner._LEGACY_CODE_REVIEW_RECORDS) is (k <= n), k

    def test_a_legacy_pass_satisfies_presence_without_the_schema(self, tmp_path):
        """Grandfathering is the whole of R3': a record the Maintainer accepted
        before the schema existed is admitted as it stands."""
        stem = "review-record-integrity"
        heading, = [h for h in _real_headings(stem)
                    if h.startswith("## Code review -- ")]
        assert _cr_violations(
            tmp_path, heading + "\n\nan old-format record, no fields.\n",
            stem=stem) == []

    def test_a_legacy_blocking_pass_needs_its_named_disposition(self, tmp_path):
        """R3', final bullet: a blocking legacy pass is admitted only by NAMING
        the heading that completes it -- and naming it without checking it would
        be the silent-check failure `AGENTS.md` > *Verifying claims* describes.
        """
        stem = "record-corrections"
        pass_dig, disp_dig = next(iter(
            planner._LEGACY_CODE_REVIEW_DISPOSITIONS[stem].items()))
        pass_heading, = [h for h in _real_headings(stem) if _dig(h) == pass_dig]
        # The disposition heading occurs TWICE in this artifact, byte-identical
        # (its Plan review carries one too), so the digest matches more than
        # once. Positional: only an occurrence AFTER the pass completes it, and
        # the planner enforces that -- taking the first match here is enough to
        # reconstruct the text.
        heading = next(h for h in _real_headings(stem) if _dig(h) == disp_dig)
        naked = pass_heading + "\n\n**Verdict: Request changes**\n"
        v = _cr_violations(tmp_path, naked, stem=stem)
        assert any("is not present after it" in m for m in v), v
        answered = naked + f"\n{heading}\n\nthe disposition.\n"
        assert _cr_violations(tmp_path, answered, stem=stem) == []

    def test_every_named_disposition_is_present_in_its_real_artifact(self):
        """The four entries, checked against the tree rather than believed.

        Both sides are digests because the planner ships as a template and the
        neutrality gate admits no AI-vendor name under `templates/` -- and every
        real disposition heading in this tree carries its author's byline. So the
        readable form of each entry lives here, derived from the artifact.
        """
        for stem, entries in sorted(
                planner._LEGACY_CODE_REVIEW_DISPOSITIONS.items()):
            headings = _real_headings(stem)
            for pass_dig, disp_dig in sorted(entries.items()):
                assert any(_dig(h) == pass_dig for h in headings), (stem, pass_dig)
                assert any(_dig(h) == disp_dig for h in headings), (stem, disp_dig)


class TestCodeReviewIsReachedByBothPublicPaths:
    """S12 / R5'' -- [R3-E1]'s required satisfier, pinned through both paths."""

    def _both(self, tmp_path, body):
        art = _plan_art(tmp_path, body, status="review", stem=_CR_STEM,
                        plan_review="not required(Chunk C fixture)")
        scanned = planner.review_record_violations(art, "archived")
        gates = planner._gating_preconditions(
            art, "archived", planner.IdentityModel(frozenset(), frozenset()))
        record_gate = [met for met, text in gates
                       if "the review record conforms for archive" in text]
        assert len(record_gate) == 1, gates
        return scanned, record_gate[0]

    @pytest.mark.parametrize("body,why", [
        ("", "no Code review at all"),
        (_code_review_pass(verdict="REVISE"), "a blocking latest review"),
        (_code_review_pass(commit=None), "a malformed latest review"),
    ])
    def test_a_not_required_plan_refuses_on_both_paths(
            self, tmp_path, body, why):
        scanned, gate_met = self._both(tmp_path, body)
        assert scanned, why
        assert gate_met is False, why

    def test_a_conforming_clearing_review_passes_on_both_paths(self, tmp_path):
        scanned, gate_met = self._both(tmp_path, _code_review_pass())
        assert scanned == []
        assert gate_met is True

    def test_the_two_weak_presence_opinions_are_gone(self):
        """R5'': "presence becomes a consequence of the schema check rather than
        a second, weaker opinion". Read from the source, because the property is
        the ABSENCE of a call and no fixture can witness an absence."""
        body = _code_of(_PLANNER_PATH, "_conformance_violations")
        assert '_has_kind(art, "Code review")' not in body, body
        assert "has_code_review_marker" not in body, body
        gating = _code_of(_PLANNER_PATH, "_gating_preconditions")
        assert "has_code_review_marker" not in gating, gating
        # `_code_of` normalizes through `ast.unparse`, which rewrites string
        # literals to single quotes -- so the expected spelling is the
        # normalized one, not the source's.
        #
        # **Chunk E generalized the literal `'archived'` to `target`**, because R6
        # bullet 8 requires `ready-to-archive` and `archived` to be judged by the
        # *same* closeout predicate.  The property this node guards is unchanged
        # and now stated more strongly: the gate calls the ONE predicate with an
        # EXPLICIT effective state, and the two archive-effective targets share one
        # branch so neither can be softened alone.
        assert "review_record_violations(art, target)" in gating, gating
        assert "elif target in ('ready-to-archive', 'archived')" in gating, gating

    def test_the_two_archive_effective_targets_get_identical_gates(self, tmp_path):
        """R6 bullet 8, as behaviour rather than as source text.

        *"`archived` when the same closeout predicate would reject
        `ready-to-archive`"* is one rule required to be shared, so a plan cannot
        reach `ready-to-archive` on evidence that would not also let it reach
        `archived`.  Asserted on a fixture that FAILS both, and on one that passes
        both, so the node cannot be satisfied by two gates that happen to agree
        while both being vacuously true.
        """
        identity = planner.IdentityModel(frozenset(), frozenset())
        for body, expect_met in ((_code_review_pass(verdict="REVISE"), False),
                                 (_code_review_pass()
                                  + _LT + "Dispositions: none\n\n" + _REAL_SIGNOFF,
                                  True)):
            art = _plan_art(tmp_path, body, status="review", stem=_CR_STEM,
                            plan_review="not required(Chunk C fixture)")
            ready = planner._gating_preconditions(art, "ready-to-archive", identity)
            done = planner._gating_preconditions(art, "archived", identity)
            assert ready == done, (ready, done)
            assert all(met for met, _d in ready) is expect_met, ready

    def test_the_marker_predicate_still_has_a_consulted_home(self):
        """It is deleted as a *gate*, not as a predicate: inside the one
        predicate it is the substance floor a legacy CONTAINER heading must
        clear, which is the only thing it can still say that the schema cannot.
        """
        assert "art.has_code_review_marker" in _code_of(
            _PLANNER_PATH, "_code_review_violations")

    def test_a_non_archive_effective_state_does_not_evaluate_code_review(
            self, tmp_path):
        """The effective state is the key, and `review` is not archive-effective:
        a plan awaiting its code review is not in violation for not having one.
        """
        assert planner.CODE_REVIEW_EFFECTIVE_STATES == (
            "ready-to-archive", "archived")
        art = _plan_art(tmp_path, "", status="review", stem=_CR_STEM,
                        plan_review="not required(Chunk C fixture)")
        assert planner.review_record_violations(art, "review") == []
        assert planner.review_record_violations(art, "archived")


def _code_of(path: Path, function: str) -> str:
    """One function's **executable** source -- comments and docstring removed.

    The absence assertions above are about what the code *calls*, and a comment
    explaining why a call was deleted necessarily names that call. Scanning raw
    text makes the explanation trip the check, which would push a future author
    toward deleting the explanation rather than fixing the scan.
    """
    module = ast.parse(path.read_text(encoding="utf-8"))
    node, = [n for n in module.body
             if isinstance(n, ast.FunctionDef) and n.name == function]
    body = list(node.body)
    if (body and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)):
        body = body[1:]
    return "\n".join(ast.unparse(stmt) for stmt in body)


def _code_review_generator():
    """The Chunk C legacy generator, loaded as the corpus oracle.

    It supplies the population; the planner is the code under test. Like its
    Plan-review sibling it deliberately does not import the gate, so the
    exempted population is not defined by the predicate that exempts it."""
    spec = importlib.util.spec_from_file_location(
        "cairn_gen_legacy_code_review_passes",
        CAIRN_ROOT / "scripts" / "gen_legacy_code_review_passes.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _dig(heading: str) -> str:
    """The 16-hex heading identity the manifests key on."""
    return hashlib.sha256(heading.strip().encode("utf-8")).hexdigest()[:16]


def _real_headings(stem: str) -> list[str]:
    """Every Code-review record heading of a real artifact, read off the tree.

    Fixtures for the legacy nodes must use the ACTUAL heading bytes: the digest
    is taken from the raw line, so a heading retyped by hand -- dropping a
    `(<role>)` parenthetical, say -- hashes to something else and the node would
    silently test the non-legacy path instead."""
    for rel in ("dev/plans", "dev/plans/archive"):
        path = CAIRN_ROOT / rel / f"{stem}.md"
        if path.is_file():
            return [line for line in path.read_text(encoding="utf-8").split("\n")
                    if line.startswith("## Code review")
                    or line.startswith("## Response to code review")
                    or line.startswith("### Sharpening")
                    or line.startswith("## Implementation disposition")
                    or line.startswith("## Archive record")]
    raise AssertionError(f"no artifact for stem {stem!r}")


# ===========================================================================
# P1 -- the four-field review basis across all three record kinds, the
# artifact-level `Assurance path:` declaration, and the immutability predicate
# that grandfathers pre-contract records.
#
# Contract: accepted `review-efficient-lifecycle`, "Bounded current contracts"
# (*"Every proposal, plan, and code review records"* the four fields) and
# "Assurance paths" (*"A proposal-worthy change declares `standard` or
# `high-assurance`"*, *"Uncertainty resolves to `high-assurance`"*).  Chunk C
# wired all four for the Code-review record; these nodes cover the two record
# kinds C did not reach plus the artifact-level declaration.
#
# Every node below was observed RED by mutating
# `templates/skills/_lib/lifecycle_planner.py` -- the copy this file LOADS --
# then restored byte-exactly.  The mutations and the observed failures are
# recorded in the plan's implementation-verification section, not asserted here.
# The only thing that runs these nodes is a person typing
# `python -m pytest bootstrap/tests`; Cairn has no CI.
# ===========================================================================

_P1_STEM = "p1-fixture"        # deliberately in NO manifest


def _prop_art(tmp_path: Path, body: str = "", *, status: str = "reviewed",
              assurance: str | None = "standard", stem: str = _P1_STEM,
              archived: bool = False, extra_header: str = ""):
    """A proposal on disk, parsed through the planner's own reader.

    `archived=True` writes it under `dev/proposals/archive/`, which is the
    location half of the immutability predicate.
    """
    d = tmp_path / "dev" / "proposals" / ("archive" if archived else "")
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{stem}.md"
    declaration = "" if assurance is None else f"**Assurance path**: {assurance}\n"
    path.write_text(
        f"# {stem}\n\n"
        f"**Author**: Author A (Strategy)\n"
        f"**Status**: {status}\n"
        f"{declaration}{extra_header}"
        f"\n## Context\n\nx\n\n{body}",
        encoding="utf-8")
    return planner._read_artifact(path)


def _prop_review(*, reviewer: str = "Reviewer A (External)",
                 date: str = "2026-08-11", suffix: str = "",
                 commit: str | None = "0123456789abcdef" * 2 + "01234567",
                 target: str | None = "the complete current contract",
                 prior: str | None = "none",
                 assurance: str | None = "standard",
                 bold_basis: bool = True, trailer: str = "") -> str:
    """One proposal `## Review` record, each field independently omittable."""
    out = f"## Review -- {reviewer} -- {date}{suffix}\n\n"
    mark = "**" if bold_basis else ""
    for name, value in (("Reviewed commit", commit), ("Target", target),
                        ("Prior findings", prior),
                        ("Assurance path", assurance)):
        if value is not None:
            out += f"{mark}{name}{mark}: {value}\n"
    return out + "\nthe reading.\n\n" + trailer


def _prop_basis(tmp_path: Path, body: str, **kw) -> list:
    return planner.proposal_review_basis_violations(
        _prop_art(tmp_path, body, **kw))


def _decl(tmp_path: Path, **kw) -> list:
    return planner.assurance_declaration_violations(_prop_art(tmp_path, **kw))


class TestPlanReviewBasis:
    """The basis on the **Plan-review** pass -- the record kind C did not reach.

    C wired the identical four fields to the Code-review pass only, and the
    accepted parent is explicit that the basis belongs to all three kinds.
    """

    @pytest.mark.parametrize("field,kwargs", [
        ("Reviewed commit", {"commit": None}),
        ("Target", {"target": None}),
        ("Prior findings", {"prior": None}),
        ("Assurance path", {"assurance": None}),
    ])
    def test_each_basis_field_is_required_on_its_own(
            self, tmp_path, field, kwargs):
        v = _violations(tmp_path, _pass_block(**kwargs))
        assert any(field in msg for msg in v), (field, v)

    def test_a_complete_pass_is_silent(self, tmp_path):
        """The mutant-catcher for every node above: with all four basis fields
        plus Tier and Findings the record is complete, so an always-violating
        check is caught rather than read as strictness."""
        assert _violations(tmp_path, _pass_block()) == []

    def test_both_emphasis_spellings_are_accepted(self, tmp_path):
        """The field NAME is the contract, the emphasis is not -- the accepted
        parent writes the basis unbolded, every real pass in `dev/plans/` bolds
        it, and refusing either spelling would refuse correct records."""
        assert _violations(tmp_path, _pass_block(bold_basis=True)) == []
        assert _violations(tmp_path, _pass_block(bold_basis=False)) == []

    def test_a_duplicate_basis_field_refuses_even_when_the_values_agree(
            self, tmp_path):
        body = _pass_block().replace(
            "**Target**: chunks A-C\n",
            "**Target**: chunks A-C\n**Target**: chunks A-C\n")
        v = _violations(tmp_path, body)
        assert any("duplicate 'Target:'" in m for m in v), v

    def test_an_empty_basis_value_refuses(self, tmp_path):
        v = _violations(tmp_path, _pass_block(prior=""))
        assert any("empty 'Prior findings:'" in m for m in v), v

    def test_basis_fields_below_the_first_h3_do_not_count(self, tmp_path):
        """The field scope is the record body up to its first H3, for the reason
        C measured on real records: a pass repeats its own attestations in a
        `### Coverage`-style subsection, so whole-body reading turns a pass's own
        summary into a duplicate.  The same cut means a field parked below an H3
        does not satisfy the obligation."""
        v = _violations(tmp_path, _pass_block(
            commit=None,
            trailer="### Coverage\n\n**Reviewed commit**: abc1234\n\n"))
        assert any("missing 'Reviewed commit:'" in m for m in v), v

    @pytest.mark.parametrize("value", ["medium", "high assurance", "Standard "])
    def test_an_out_of_vocabulary_assurance_path_refuses(self, tmp_path, value):
        """`Standard ` with a trailing space is INCLUDED on purpose: the matcher
        strips trailing whitespace, so this one must CLEAR -- it is the
        false-refusal direction of the same check."""
        v = _violations(tmp_path, _pass_block(assurance=value))
        if value.strip().casefold() in planner.ASSURANCE_PATHS:
            assert v == [], (value, v)
        else:
            assert any("unrecognized Assurance path" in m for m in v), (value, v)

    def test_the_legacy_passes_exemption_does_not_swallow_the_basis(
            self, tmp_path):
        """**The scoping property, and the reason a second manifest exists.**

        `_LEGACY_PASSES` exempts a pass from S2/S3/S7.  Every pass P1's basis
        newly reaches already satisfies S2/S3/S7, so folding those records into
        `_LEGACY_PASSES` would have *weakened* the gate while looking like
        grandfathering.  This node reproduces that: a pass whose heading IS in
        `_LEGACY_PASSES`, in a live (mutable) plan, is still refused for a
        missing basis field -- and the S2 exemption still holds for Tier.
        """
        stem = "review-gate-enforcement"
        heading = "## Plan review -- Codex (External) -- 2026-08-05"
        dig = hashlib.sha256(heading.encode("utf-8")).hexdigest()[:16]
        assert dig in planner._LEGACY_PASSES[stem], "fixture precondition"
        assert dig not in planner._LEGACY_UNDECLARED_BASIS.get(stem, {})
        body = f"{heading}\n\nno Tier, no Findings, and no basis.\n\n"
        v = _violations(tmp_path, body, stem=stem)
        assert any("missing 'Target:'" in m for m in v), v
        # ... and the S2/S3 exemption is untouched: no Tier violation is raised.
        assert not any("missing Tier" in m for m in v), v


class TestProposalReviewBasis:
    """The basis on the proposal `## Review` record -- the third record kind."""

    @pytest.mark.parametrize("field,kwargs", [
        ("Reviewed commit", {"commit": None}),
        ("Target", {"target": None}),
        ("Prior findings", {"prior": None}),
        ("Assurance path", {"assurance": None}),
    ])
    def test_each_basis_field_is_required_on_its_own(
            self, tmp_path, field, kwargs):
        v = _prop_basis(tmp_path, _prop_review(**kwargs))
        assert any(field in msg for msg in v), (field, v)

    def test_a_complete_record_is_silent(self, tmp_path):
        assert _prop_basis(tmp_path, _prop_review()) == []

    def test_a_proposal_with_no_review_record_owes_nothing(self, tmp_path):
        """The obligation attaches to a record that exists; it is not a second
        presence floor (`_conformance_violations` already owns that one)."""
        assert _prop_basis(tmp_path, "", status="proposed") == []

    @pytest.mark.parametrize("suffix", [
        " (Round 2)",                 # capital R -- `_HEADER_RE` cannot parse it
        " (round 4, closure read)",   # annotated round -- ditto
        "",
    ])
    def test_an_off_grammar_heading_is_still_a_record_and_owes_the_basis(
            self, tmp_path, suffix):
        """**The escape hatch this closes, measured on real headings.**

        A strict `-- <reviewer> -- YYYY-MM-DD` grammar (the `_S1_PASS_RE` shape)
        would make each suffix above a *near miss*: invisible to the basis check
        while still counted by `_reviewers()`, which is what satisfies the
        "status is 'reviewed' but no '## Review' section is present" floor.  Then
        writing the heading slightly off-grammar drops the basis obligation and
        keeps the presence floor.  All three suffixes occur in this repository's
        own proposals, so the permissive rule is not hypothetical.
        """
        v = _prop_basis(tmp_path, _prop_review(suffix=suffix, target=None))
        assert any("missing 'Target:'" in m for m in v), (suffix, v)

    def test_a_reviewer_brief_heading_is_not_a_review_record(self, tmp_path):
        """`## Reviewer brief` is a real heading in three proposals here. The
        required ` -- ` after `Review` is what keeps it out; without that the
        section would be handed an obligation it has no way to discharge."""
        assert _prop_basis(
            tmp_path, "## Reviewer brief\n\nwhat to attack first.\n\n") == []

    def test_a_response_heading_is_not_a_review_record(self, tmp_path):
        assert _prop_basis(
            tmp_path,
            "## Response -- Author A -- 2026-08-11\n\nthe reply.\n\n") == []

    def test_a_later_record_does_not_lend_its_basis_to_an_earlier_one(
            self, tmp_path):
        """The boundary half: P1 adds the proposal review heading to
        `_record_boundaries`, so an incomplete record's field scope stops at the
        next record instead of running through it and borrowing its fields.
        The second heading here carries `(Round 2)`, which `_HEADER_RE` cannot
        parse -- exactly the shape that was invisible as a boundary before."""
        body = (_prop_review(target=None, prior=None, assurance=None)
                + _prop_review(suffix=" (Round 2)"))
        v = _prop_basis(tmp_path, body)
        assert any("missing 'Target:'" in m for m in v), v
        assert any("missing 'Prior findings:'" in m for m in v), v
        assert any("missing Assurance path" in m for m in v), v

    def test_both_gate_surfaces_report_it(self, tmp_path):
        """S12 applied to the proposal side: `_conformance_violations` (what
        `scan` reports) and `_gating_preconditions` (what `next --to` reports)
        consume the SAME predicate.  Wiring only the first is the defect [R3-E1]
        executed on the Code-review half -- the loose surface is the one an
        author drives."""
        art = _prop_art(tmp_path, _prop_review(target=None))
        identity = planner.IdentityModel(frozenset(), frozenset())
        conformance = planner._conformance_violations(art, identity)
        assert any("missing 'Target:'" in m for m in conformance), conformance
        for target in planner._legal_transitions(art):
            gates = planner._gating_preconditions(art, target, identity)
            unmet = [desc for met, desc in gates if not met]
            assert any("four-field review basis" in d for d in unmet), (
                target, gates)


class TestAssurancePathDeclaration:
    """The artifact-level declaration, which **never defaults to `standard`**."""

    def test_a_missing_declaration_refuses_and_names_the_no_default_rule(
            self, tmp_path):
        v = _decl(tmp_path, assurance=None)
        assert len(v) == 1, v
        assert "no '**Assurance path**:' declaration" in v[0]
        # The message must carry the rule, not just the absence: an author told
        # only "missing field" will reach for the smaller of two values.
        assert "NO default" in v[0] and "high-assurance" in v[0]

    @pytest.mark.parametrize("value", ["standard", "high-assurance"])
    def test_both_declared_values_clear(self, tmp_path, value):
        assert _decl(tmp_path, assurance=value) == []

    @pytest.mark.parametrize("value", ["medium", "high assurance", "unknown",
                                       "standard | high-assurance"])
    def test_an_out_of_vocabulary_declaration_refuses(self, tmp_path, value):
        v = _decl(tmp_path, assurance=value)
        assert any("unrecognized Assurance path" in m for m in v), (value, v)

    def test_a_duplicate_declaration_refuses(self, tmp_path):
        v = _decl(tmp_path, assurance="standard",
                  extra_header="**Assurance path**: high-assurance\n")
        assert any("duplicate Assurance path" in m for m in v), v

    def test_a_duplicate_refuses_even_when_the_values_agree(self, tmp_path):
        """Agreement is a judgement a conformance backstop must not make -- and
        here it would be choosing which of two declarations governs review
        allocation."""
        v = _decl(tmp_path, assurance="standard",
                  extra_header="**Assurance path**: standard\n")
        assert any("duplicate Assurance path" in m for m in v), v

    def test_a_declaration_inside_a_review_record_does_not_satisfy_the_header(
            self, tmp_path):
        """The header region is bounded at the first `##`.  Without that bound,
        the `Assurance path:` line every review record now carries would satisfy
        the artifact's own declaration -- so the obligation would be discharged
        by a *reviewer's* record rather than by the author, and a proposal with
        no reviews yet could never be made to satisfy it at all.

        Measured on a real artifact while implementing P1: a first grep for
        `Assurance path` in `2026-08-11-claude-metrics-events-not-prose.md`
        matched line 186, inside its first `## Review` record, and read as a
        header declaration until the bound was checked.
        """
        v = _decl(tmp_path, assurance=None, body=_prop_review())
        assert any("no '**Assurance path**:' declaration" in m for m in v), v

    def test_a_plan_carries_no_artifact_level_declaration(self, tmp_path):
        """It is the **proposal** that declares: the accepted parent says *"A
        proposal-worthy change declares"*, and the plan carries the inheritance
        metadata instead (P2's cell).  Pinned as an absence so a later chunk that
        moves the obligation onto plans does so deliberately."""
        art = _plan_art(tmp_path, _pass_block())
        assert planner.assurance_declaration_violations(art) == []

    def test_both_gate_surfaces_report_it(self, tmp_path):
        art = _prop_art(tmp_path, _prop_review(), assurance=None)
        identity = planner.IdentityModel(frozenset(), frozenset())
        conformance = planner._conformance_violations(art, identity)
        assert any("Assurance path" in m for m in conformance), conformance
        for target in planner._legal_transitions(art):
            unmet = [desc for met, desc
                     in planner._gating_preconditions(art, target, identity)
                     if not met]
            assert any("Assurance path" in d for d in unmet), (target, unmet)


class TestImmutabilityGrandfather:
    """The predicate that keeps the enumeration at nine entries instead of ~72.

    Shape reused from Chunk D4's `scripts/claim_check.py` (accepted
    `claim-check-exemption-hygiene` R3): archived by **location**, or terminal by
    a **strictly parsed** status -- and everything it does not recognize falls
    through *into* the requirement rather than inheriting the exemption.
    """

    def test_an_archived_proposal_is_grandfathered_by_location(self, tmp_path):
        art = _prop_art(tmp_path, _prop_review(commit=None, target=None,
                                               prior=None, assurance=None),
                        assurance=None, archived=True, status="proposed")
        assert planner._is_immutable(art) is True
        assert planner.proposal_review_basis_violations(art) == []
        assert planner.assurance_declaration_violations(art) == []

    @pytest.mark.parametrize("status", ["accepted", "rejected", "superseded"])
    def test_a_terminal_proposal_is_grandfathered_by_status(
            self, tmp_path, status):
        art = _prop_art(tmp_path, _prop_review(target=None), assurance=None,
                        status=status)
        assert planner._is_immutable(art) is True
        assert planner.proposal_review_basis_violations(art) == []
        assert planner.assurance_declaration_violations(art) == []

    @pytest.mark.parametrize("status", ["proposed", "reviewed", "revised"])
    def test_a_live_proposal_is_not_grandfathered(self, tmp_path, status):
        art = _prop_art(tmp_path, _prop_review(target=None), assurance=None,
                        status=status)
        assert planner._is_immutable(art) is False
        assert planner.proposal_review_basis_violations(art) != []
        assert planner.assurance_declaration_violations(art) != []

    def test_an_archived_plan_is_grandfathered_by_status(self, tmp_path):
        """A plan's terminal token is `archived`, and the basis half must go
        silent even though the record is missing every field."""
        body = "## Plan review -- R -- 2026-05-01\n\n**Tier**: External\n" \
               "**Findings**: none\n"
        art = _plan_art(tmp_path, body, status="archived")
        assert planner._is_immutable(art) is True
        assert not [m for m in planner.review_record_violations(art)
                    if "review basis" in m or "Assurance path" in m]

    @pytest.mark.parametrize("header,why", [
        ("", "missing status"),
        ("**Status**: accepted\n**Status**: accepted\n", "duplicate status"),
        ("**Status**: acceptedish\n", "unrecognized token"),
        ("**Status**:accepted\n", "no space -- still a strict match"),
        ("Status: accepted\n", "unbolded -- not the header field"),
    ])
    def test_a_non_strict_status_does_not_gain_the_grandfather(
            self, tmp_path, header, why):
        """D4's fail-closed rule: *"A missing, duplicate, or unrecognized
        lifecycle status does not silently gain grandfathering."*  The set can
        only ever be too small, never too permissive.

        `**Status**:accepted` is the one case that DOES grandfather -- the strict
        matcher makes the space optional -- and it is parametrized here so the
        node states which direction each spelling falls in rather than asserting
        a blanket refusal.
        """
        d = tmp_path / "dev" / "proposals"
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{_P1_STEM}.md"
        path.write_text(f"# t\n\n{header}\n## Context\n\nx\n", encoding="utf-8")
        art = planner._read_artifact(path)
        expected = header.strip() == "**Status**:accepted"
        assert planner._is_immutable(art) is expected, why

    def test_a_status_line_below_the_first_h2_is_not_the_header_status(
            self, tmp_path):
        """An appended revision section restating `**Status**:` is historical
        text, not the artifact's current status -- so it cannot buy immunity."""
        d = tmp_path / "dev" / "proposals"
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{_P1_STEM}.md"
        path.write_text(
            "# t\n\n**Status**: reviewed\n\n## Revision 1\n\n"
            "**Status**: accepted\n", encoding="utf-8")
        art = planner._read_artifact(path)
        assert planner._strict_header_status(art.text) == "reviewed"
        assert planner._is_immutable(art) is False


class TestBasisLegacyEnumerations:
    """The two pinned enumerations: no fabricated entry, and no replay."""

    def test_the_baseline_commit_is_a_real_full_length_commit(self):
        """A pinned baseline nobody can resolve is a claim, not a pin."""
        sha = planner._BASIS_BASELINE_COMMIT
        assert re.fullmatch(r"[0-9a-f]{40}", sha), sha
        proc = subprocess.run(
            ["git", "-C", str(CAIRN_ROOT), "cat-file", "-t", sha],
            capture_output=True, text=True)
        assert proc.returncode == 0 and proc.stdout.strip() == "commit", proc

    def test_every_basis_manifest_entry_resolves_in_the_live_tree(self):
        """Subset direction: a fabricated or stale entry reddens.

        Not an equality check, deliberately, for the reason C's own manifest node
        states: a record appended after the baseline legitimately exists and
        legitimately is not in the manifest, so equality would redden on the next
        review that lands.
        """
        for stem, digests in sorted(planner._LEGACY_UNDECLARED_BASIS.items()):
            path = _p1_live_artifact(stem)
            assert path is not None, (
                f"_LEGACY_UNDECLARED_BASIS names {stem!r}, which is not a LIVE "
                "artifact -- an archived one is already covered by "
                "`_is_immutable`, so the entry would be dead weight")
            lines = path.read_text(encoding="utf-8").split("\n")
            seen: dict[str, int] = {}
            for raw in lines:
                if (planner._S1_PASS_RE.match(raw)
                        or planner._PROPOSAL_REVIEW_RECORD_RE.match(raw)):
                    d = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
                    seen[d] = seen.get(d, 0) + 1
            for dig, count in sorted(digests.items()):
                assert seen.get(dig, 0) >= count, (
                    f"_LEGACY_UNDECLARED_BASIS[{stem!r}][{dig!r}] admits "
                    f"{count} record(s); the tree has {seen.get(dig, 0)} -- a "
                    "fabricated or stale entry")

    def test_every_basis_manifest_entry_is_still_needed(self):
        """An entry whose record now carries the basis is dead weight, and the
        docstring says the enumerations only shrink.  Asserted as a *warning
        surface* rather than a hard requirement would be untestable, so it is
        asserted directly: if this reddens, delete the entry."""
        for stem, digests in sorted(planner._LEGACY_UNDECLARED_BASIS.items()):
            path = _p1_live_artifact(stem)
            assert path is not None, stem
            art = planner._read_artifact(path)
            assert planner._is_immutable(art) is False, (
                f"{stem} is now immutable -- `_is_immutable` covers it and the "
                "manifest entry is dead weight; delete it")
            lines = art.text.split("\n")
            bounds = planner._record_boundaries(art)
            still_needed = set()
            for i, raw in enumerate(lines):
                d = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
                if d not in digests:
                    continue
                if not (planner._S1_PASS_RE.match(raw)
                        or planner._PROPOSAL_REVIEW_RECORD_RE.match(raw)):
                    continue
                scope = planner._record_field_scope(lines, i + 1, bounds)
                if planner._review_basis_violations(scope, "x"):
                    still_needed.add(d)
            assert still_needed == set(digests), (
                f"{stem}: these entries no longer grandfather anything and are "
                f"dead weight -- delete them: "
                f"{sorted(set(digests) - still_needed)}")

    def test_the_declaration_exemption_names_only_live_undeclared_proposals(self):
        for stem in sorted(planner._LEGACY_UNDECLARED_ASSURANCE_PATH):
            path = CAIRN_ROOT / "dev" / "proposals" / f"{stem}.md"
            assert path.is_file(), (
                f"_LEGACY_UNDECLARED_ASSURANCE_PATH names {stem!r}, which is "
                "not a live proposal -- delete the entry")
            art = planner._read_artifact(path)
            assert planner._is_immutable(art) is False, (
                f"{stem} is terminal -- `_is_immutable` already covers it")
            header = "\n".join(planner._iter_header_lines(art.text))
            assert not planner._REVIEW_FIELD_RE["Assurance path"].search(header), (
                f"{stem} now declares an assurance path in its header -- the "
                "exemption is dead weight; delete it")

    def test_the_basis_exemption_is_refused_at_occurrence_count_plus_one(self):
        """The anti-replay half.  Re-appending a heading byte-identical to an
        admitted one is occurrence `n + 1` and is not admitted -- the same
        k-th-occurrence rule `_LEGACY_PASSES` uses, reached through
        `_is_legacy`'s `manifest` argument rather than a second implementation.
        """
        checked = 0
        for stem, digests in sorted(planner._LEGACY_UNDECLARED_BASIS.items()):
            for dig, n in sorted(digests.items()):
                for k in range(1, n + 2):
                    assert planner._is_legacy(
                        stem, dig, {dig: k},
                        planner._LEGACY_UNDECLARED_BASIS) is (k <= n), (
                            stem, dig, k)
                checked += 1
        assert checked == 4, (
            "the enumeration changed size; re-derive it against "
            "`_BASIS_BASELINE_COMMIT` and update this figure deliberately "
            f"(found {checked})")
        # 9 -> 8 -> 4 on 2026-08-12, deliberately, and TWICE for the same
        # reason: a Decision landing in another session flips a proposal to a
        # terminal status, `_is_immutable` starts covering it, and its entries
        # become dead weight.  First `boundary-b-bounding-clause` (8308fdc),
        # then `metrics-events-not-prose` (4 digests).  The enumeration is
        # inherently transient and liquidates itself as artifacts close; that
        # is the design, not drift.  Original note follows.
        # 9 -> 8 on 2026-08-12, deliberately.  `2026-08-12-claude-boundary-b-
        # bounding-clause` was `revised` at `_BASIS_BASELINE_COMMIT` and so
        # legitimately needed an entry; `df8478b` scribed its Decision to
        # `accepted`, which is terminal, so `_is_immutable` now covers it and the
        # entry became dead weight.  Deleting it is the maintenance this class
        # exists to force -- `test_every_basis_manifest_entry_is_still_needed`
        # reddened until it was gone, and this figure is the second half of the
        # same guard.  Entries only ever leave.


    def test_the_two_basis_manifests_are_not_the_same_table(self):
        """`_LEGACY_UNDECLARED_BASIS` must not become an alias for
        `_LEGACY_PASSES`: the two grandfather different obligations, and merging
        them would silently widen whichever is consulted."""
        assert planner._LEGACY_UNDECLARED_BASIS is not planner._LEGACY_PASSES
        assert planner._LEGACY_UNDECLARED_BASIS != planner._LEGACY_PASSES


def _p1_live_artifact(stem: str):
    """The LIVE artifact for *stem*, or None -- never the archived sibling."""
    for fam in ("proposals", "plans"):
        path = CAIRN_ROOT / "dev" / fam / f"{stem}.md"
        if path.is_file():
            return path
    return None


def test_the_live_corpus_is_sound_under_the_p1_contract():
    """The blast-radius assertion, as a standing node.

    P1's whole risk is reddening a live artifact nobody may edit.  `scan`
    (live-only) is the enforcement surface named in the plan's acceptance
    criteria, and it must stay at all-artifacts-sound with P1 landed -- which is
    what the immutability predicate plus the two enumerations buy.
    """
    identity = planner._load_identity_model(CAIRN_ROOT)
    bad = {}
    for fam in ("proposals", "plans"):
        for path in sorted((CAIRN_ROOT / "dev" / fam).glob("*.md")):
            if path.name in ("_template.md", "README.md"):
                continue
            art = planner._read_artifact(path)
            v = planner._conformance_violations(art, identity)
            if v:
                bad[path.name] = v
    assert bad == {}, bad


class TestP1AuthoringTemplates:
    """P1's template half, pinned per surface rather than assumed.

    The plan's acceptance criteria require each documentation surface to be
    *confirmed* updated: "drift gates catch drift, not absence."  These four
    files are where the contract is taught, and the tooling half is worthless
    without them -- an author who is refused by the gate and finds no instruction
    in the template has been handed a puzzle instead of a rule.
    """

    #: (path, obligation-name -> substring that must be present)
    SURFACES = {
        "dev/proposals/_template.md": {
            "the header declaration": "**Assurance path**:",
            "the mandatory trigger set": "`high-assurance` is **mandatory** when",
            "uncertainty resolves high": "Uncertainty resolves to `high-assurance`",
            "declarations are not inferences":
                "author declarations, not inferences",
            "the review basis in the Review section":
                "The four-field review basis is mandatory",
            "all four field names": "Prior findings: <ids being closed, or none>",
        },
        "dev/plans/_template.md": {
            "the basis in the plan-review pass scaffold":
                "Reviewed commit: <full commit id>",
            "the H3 scope rule": "does not count",
            "the basis in the Code-review section":
                "Target: <the code range this pass reviewed>",
        },
    }

    @pytest.mark.parametrize("rel", sorted(SURFACES))
    @pytest.mark.parametrize("shipped", [False, True])
    def test_each_surface_carries_the_contract(self, rel, shipped):
        """Both sides of every pair: the self-hosted copy under `dev/` and the
        shipped copy under `templates/core/`.  Chunk B of `scope-reduction-trap`
        edited a shipped source and not its installed twin, leaving the unsound
        text live in the copy Cairn itself reads -- checking one side is how that
        happens."""
        path = CAIRN_ROOT / (f"templates/core/{rel}" if shipped else rel)
        text = path.read_text(encoding="utf-8")
        missing = [name for name, needle in self.SURFACES[rel].items()
                   if needle not in text]
        assert not missing, (path, missing)

    def test_the_shipped_proposal_template_carries_an_unfilled_trigger_slot(self):
        """The two `_template.md` copies are **not** byte-identical twins, by
        design: the shipped copy carries fill-slots and Cairn's copy is the
        filled instance.  P1's new slot must follow that pattern rather than
        shipping Cairn's own protected-surface roster to every adopter.
        """
        shipped = (CAIRN_ROOT / "templates/core/dev/proposals/_template.md"
                   ).read_text(encoding="utf-8")
        ours = (CAIRN_ROOT / "dev/proposals/_template.md"
                ).read_text(encoding="utf-8")
        opener = "<!-- cairn:slot assurance-path-triggers -->"
        for text, label in ((shipped, "shipped"), (ours, "self-hosted")):
            assert text.count(opener) == 1, label
            assert text.count("<!-- cairn:end assurance-path-triggers -->") == 1, \
                label
        shipped_slot = shipped.split(opener, 1)[1].split("<!-- cairn:end", 1)[0]
        our_slot = ours.split(opener, 1)[1].split("<!-- cairn:end", 1)[0]
        assert "Fill with your" in shipped_slot, shipped_slot
        assert "An unfilled slot is a review finding" in shipped_slot
        # Cairn's copy is FILLED: no instruction text, and it names real surfaces.
        assert "Fill with your" not in our_slot, our_slot
        assert "bootstrap/_scaffold" in our_slot, our_slot

    def test_the_plan_template_placeholder_still_cannot_satisfy_the_gate(self):
        """P1 adds text to `## Code review` in the plan template, and the archive
        precondition is keyed on a *reviewer marker* inside that section.  Adding
        a `**Model**:` line at line start -- or a dated reviewer heading -- would
        make the shipped placeholder satisfy the gate, which is the exact defect
        `archive-precondition-substance` closed after two plans archived with no
        code review while the gate reported success.
        """
        for rel in ("dev/plans/_template.md",
                    "templates/core/dev/plans/_template.md"):
            text = (CAIRN_ROOT / rel).read_text(encoding="utf-8")
            assert planner._has_code_review_marker(text) is False, rel


# ---------------------------------------------------------------------------
# Chunk P5 -- the `Contract non-expansion` attestation.
#
# Contract, from BOTH governing sources.  The accepted
# `review-efficient-lifecycle` parent, "Standard-path plan-readiness
# inheritance": *"For an inherited plan, code review must include this exercised
# backstop"* -- `Contract non-expansion: VERIFIED | NOT VERIFIED` plus a `Basis:`
# line binding `proposal=`, `plan=` and `changed-paths=`; *"`NOT VERIFIED` is
# blocking. This remains a semantic human/agent review; the parser validates the
# record and bindings but does not pretend to prove prose equivalence."*  The
# amendment (`code-review-blindness`) bounds it: this chunk *"validates its
# presence and binding shape when the plan declares inheritance, and treats `NOT
# VERIFIED` as blocking. It does not attempt to validate the semantic claim"*,
# and its **R6** excludes "Semantic verification of `Contract non-expansion`".
#
# WHY THESE FIXTURES ARE SYNTHETIC, AND WHY THAT IS THE POINT.  The rule fires
# only when a plan declares `Inherited proposal basis:`, and that declaration is
# **P2-R's** deliverable, which `## Sequence` puts AFTER P5.  So the trigger set
# in this repository is empty (measured below, and asserted as a standing node),
# and a rule whose trigger set is empty is indistinguishable from a rule that
# works -- the silent-tool defect `AGENTS.md` > *Verifying claims* names: "a tool
# that returns success without testing the claimed property is a worse defect
# than no tool, because it is silent".  "No corpus plan triggers it and the suite
# is green" is therefore NOT evidence here.  Every refusal direction below is
# exercised against a plan fixture that DOES declare inheritance.
#
# Each node carries a single-property falsifier -- a mutation applied to
# `templates/skills/_lib/lifecycle_planner.py`, the copy this module LOADS, then
# reverted -- recorded in the plan's implementation-verification section rather
# than asserted here.  The only thing that runs these nodes is a person typing
# `python -m pytest bootstrap/tests`; Cairn has no CI.
# ---------------------------------------------------------------------------

_P5_STEM = "p5-fixture"          # deliberately in NEITHER legacy manifest

#: A plausible P2-R declaration value.  P5 never parses it -- the field's value
#: grammar is P2-R's -- so its only job here is to be present.
_P5_INHERITED = "review=" + "c" * 40 + "; proposal=" + "d" * 40
_P5_DECLARATION = f"**Inherited proposal basis**: {_P5_INHERITED}"

_P5_PROPOSAL_SHA = "a" * 40
_P5_PLAN_SHA = "b" * 40
_P5_BASIS = (f"proposal={_P5_PROPOSAL_SHA}; plan={_P5_PLAN_SHA}; "
             "changed-paths=abc1234^..def5678")
_P5_FIELD = "Contract non-expansion"


def _p5_backstop(*, value: str | None = "VERIFIED",
                 basis: str | None = _P5_BASIS,
                 attestation_line: str | None = None,
                 basis_line: str | None = None) -> str:
    """The two-line backstop, each half independently omittable or replaceable.

    `value=None` / `basis=None` omit that half; `attestation_line` /
    `basis_line` replace the whole rendered line, which is how the emphasis,
    fold and duplicate nodes vary exactly one property.
    """
    out = ""
    if attestation_line is not None:
        out += attestation_line + "\n"
    elif value is not None:
        out += f"{_P5_FIELD}: {value}\n"
    if basis_line is not None:
        out += basis_line + "\n"
    elif basis is not None:
        out += f"Basis: {basis}\n"
    return out


def _p5_violations(tmp_path: Path, *, trailer: str = "",
                   declaration: str | None = _P5_DECLARATION,
                   state: str = "archived", stem: str = _P5_STEM,
                   plan_review: str = "not required(P5 fixture)",
                   **pass_kw) -> list:
    """The one predicate over an inheritance-declaring plan at archive.

    `plan_review` defaults to `not required(...)` for the reason `_cr_violations`
    documents: that is [R3-E1]'s executed bypass shape, so every node here also
    asserts the Code-review half is reached without the declaration's help.
    """
    art = _plan_art(tmp_path, _code_review_pass(trailer=trailer, **pass_kw),
                    status=state, plan_review=plan_review, stem=stem,
                    header_extra="" if declaration is None else declaration)
    return planner.review_record_violations(art, state)


def _p5_field_violations(v: list) -> list:
    """Only the findings this chunk owns, so a node cannot pass on someone
    else's refusal.

    `Answers:` is excluded explicitly: `code_review_binding_violations` also
    says "binding", and a helper that counted its findings as P5's would let a
    node pass on a defect P5 never detected.
    """
    return [m for m in v
            if "Answers:" not in m
            and (_P5_FIELD in m or "Basis:" in m or "binding" in m)]


def test_p5_the_fixture_stem_is_in_neither_legacy_manifest():
    """The premise every node below rests on."""
    assert _P5_STEM not in planner._LEGACY_CODE_REVIEW_RECORDS
    assert _P5_STEM not in planner._LEGACY_PASSES
    assert _P5_STEM not in planner._LEGACY_UNDECLARED_BASIS


class TestP5InheritanceTrigger:
    """The ONE trigger: a plan header declaring `Inherited proposal basis:`."""

    def test_a_plan_declaring_no_inheritance_owes_no_attestation(self, tmp_path):
        """The parent's clause is "for an inherited plan".  A complete,
        clearing, NON-inherited pass carrying no backstop at all is silent --
        which is also the blast-radius property: every plan in this tree is this
        plan, so P5 reddens nothing that was green."""
        assert _p5_violations(tmp_path, declaration=None) == []

    def test_declaring_inheritance_makes_the_backstop_owed(self, tmp_path):
        """The rule FIRES.  Same pass, same state, one header line different."""
        v = _p5_violations(tmp_path)
        assert any(_P5_FIELD in m for m in v), v
        assert any("Basis:" in m for m in v), v

    @pytest.mark.parametrize("declaration", [
        f"**Inherited proposal basis**: {_P5_INHERITED}",
        f"Inherited proposal basis: {_P5_INHERITED}",
        f"__Inherited proposal basis__: {_P5_INHERITED}",
    ])
    def test_every_emphasis_spelling_of_the_declaration_triggers(
            self, tmp_path, declaration):
        """The field NAME is the contract; the emphasis is not.  The revision
        writes it unbolded, this tree's house style bolds every header field, and
        one matcher (`_code_review_field_re`) admits both -- so a plan is not
        exempted from the backstop by its author's markdown habits."""
        assert _p5_field_violations(
            _p5_violations(tmp_path, declaration=declaration)), declaration

    @pytest.mark.parametrize("value", ["", "garbage", "review=only-one-half",
                                       "proposal=" + "e" * 40])
    def test_a_malformed_or_empty_declaration_still_triggers(
            self, tmp_path, value):
        """**Presence, not well-formedness -- and the direction is deliberate.**
        Requiring a parseable value before the backstop is owed would let a
        half-written declaration buy silence on the backstop, which is the wrong
        way to fail.  The value's own grammar (both sub-fields, parseable commit
        ids) is P2-R's obligation and refuses there; P5 never reads it."""
        v = _p5_violations(
            tmp_path, declaration=f"**Inherited proposal basis**: {value}")
        assert _p5_field_violations(v), (value, v)

    def test_the_declaration_is_read_from_the_header_only(self, tmp_path):
        """Not tidiness -- a live artifact depends on it.  The plan that
        SPECIFIES this field quotes it inside an appended revision section, so a
        whole-text search would make that plan declare inheritance about itself
        and fire this gate on the artifact that defines it."""
        art = _plan_art(
            tmp_path,
            "## Maintainer-directed contract revision -- 2026-08-11\n\n"
            "```text\nInherited proposal basis: review=<commit>\n```\n\n"
            f"Inherited proposal basis: {_P5_INHERITED}\n\n"
            + _code_review_pass(),
            status="archived", plan_review="not required(x)", stem=_P5_STEM)
        assert planner._declares_inheritance(art) is False
        assert planner.review_record_violations(art, "archived") == []

    def test_the_plan_that_specifies_the_field_does_not_declare_it(self):
        """The live instance of the node above, asserted against the real tree:
        `review-efficient-lifecycle.md` writes the literal field name five times
        and must still not be an inherited plan."""
        path = CAIRN_ROOT / "dev" / "plans" / "review-efficient-lifecycle.md"
        text = path.read_text(encoding="utf-8")
        assert "Inherited proposal basis" in text, (
            "this node's premise moved -- the plan no longer quotes the field")
        assert planner._declares_inheritance(
            planner._read_artifact(path)) is False

    def test_the_retired_parent_spelling_is_not_the_trigger(self, tmp_path):
        """A RESIDUAL, pinned rather than hidden.  The accepted parent folded the
        fact into the plan-review field -- `Plan review: inherited(<review
        commit>; proposal=<accepted commit>)` -- and the 2026-08-11
        Maintainer-directed revision replaced that with the two-field shape.  P5
        keys on the field the revision names, so the retired spelling triggers
        nothing here.  Refusing the retired spelling AT the `Plan review:` field
        is the `Plan review` vocabulary's business (P2-R / Chunk E), not this
        block's; this node exists so that gap is visible in a test rather than
        discovered by an author who used the parent's wording."""
        art = _plan_art(
            tmp_path, _code_review_pass(), status="archived",
            plan_review=f"inherited({_P5_PLAN_SHA}; proposal={_P5_PROPOSAL_SHA})",
            stem=_P5_STEM)
        assert planner._declares_inheritance(art) is False
        assert not _p5_field_violations(
            planner.review_record_violations(art, "archived"))

    def test_a_proposal_is_never_an_inherited_plan(self, tmp_path):
        """"For an inherited *plan*".  A proposal has no plan-review basis to
        inherit, and its status vocabulary never reaches an archive-effective
        state, so the kind guard is stated rather than left to that accident."""
        repo = _make_repo(tmp_path)
        _write_proposal(repo, "p.md", status="proposed")
        path = repo / "dev" / "proposals" / "p.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "**Status**: proposed",
                f"**Status**: proposed\n{_P5_DECLARATION}", 1),
            encoding="utf-8")
        assert planner._declares_inheritance(
            planner._read_artifact(path)) is False

    def test_the_live_corpus_declares_no_inheritance(self):
        """**The empty trigger set, recorded as a measurement rather than left
        as an accident.**  Zero plans -- live or archived -- declare inheritance
        today, because P2-R has not shipped the declaration.  When it does, this
        node reddens, and that is the signal to check that the plan it lands on
        carries the backstop.  Until then it is the standing proof that P5's
        blast radius is exactly zero, and the reason every other node here is
        synthetic."""
        declaring = []
        for fam in ("plans", "plans/archive"):
            base = CAIRN_ROOT / "dev" / fam
            if not base.is_dir():
                continue
            for path in sorted(base.glob("*.md")):
                if path.name in ("_template.md", "README.md"):
                    continue
                if planner._declares_inheritance(planner._read_artifact(path)):
                    declaring.append(path.name)
        assert declaring == [], (
            "a plan now declares inheritance -- confirm its Code review carries "
            f"'{_P5_FIELD}' with a well-formed 'Basis:' line: {declaring}")


class TestP5AttestationVocabulary:
    """Presence, uniqueness, the closed vocabulary, and the blocking value."""

    def test_a_complete_backstop_is_silent(self, tmp_path):
        """The mutant guard for every refusal node below: with the declaration,
        the attestation and a well-formed `Basis:` line the record is complete,
        so a check that always violates is caught here."""
        assert _p5_violations(tmp_path, trailer=_p5_backstop()) == []

    def test_the_attestation_is_required(self, tmp_path):
        v = _p5_violations(tmp_path, trailer=_p5_backstop(value=None))
        assert any(f"missing '{_P5_FIELD}:'" in m for m in v), v

    def test_a_duplicate_attestation_refuses_even_when_the_values_agree(
            self, tmp_path):
        """Agreement is a judgement a conformance backstop must not make --
        `_parse_one_field`'s rule, applied to this field."""
        v = _p5_violations(
            tmp_path, trailer=_p5_backstop() + f"{_P5_FIELD}: VERIFIED\n")
        assert any("duplicate" in m and _P5_FIELD in m for m in v), v

    @pytest.mark.parametrize("value", [
        "NOT VERIFIED", "not verified", "NOT VERIFIED.",
        "NOT VERIFIED, the plan added a public path",
    ])
    def test_not_verified_is_blocking(self, tmp_path, value):
        """*"`NOT VERIFIED` is blocking."*  Case-insensitive and tolerant of a
        trailing clause, because the reviewer writing this line is the same
        author writing `**Verdict: SHIP.**` four lines above it."""
        v = _p5_violations(tmp_path, trailer=_p5_backstop(value=value))
        assert any("BLOCKING" in m for m in v), (value, v)

    @pytest.mark.parametrize("value", [
        "MAYBE", "PARTIAL", "VERIFIED-ish", "verified with caveats",
        "VERIFIED but actually NOT VERIFIED", "SHIP", "",
    ])
    def test_an_out_of_vocabulary_value_refuses_and_never_defaults(
            self, tmp_path, value):
        """No condition yields a silent pass and there is no default.  An empty
        value is in this list on purpose: a bare `Contract non-expansion:` is the
        shape a half-written record has, and reading it as `VERIFIED` would
        invert the contract at the point it was written to protect."""
        v = _p5_violations(tmp_path, trailer=_p5_backstop(value=value))
        assert _p5_field_violations(v), (value, v)
        assert not any("BLOCKING" in m for m in v), (
            f"{value!r} was read as the blocking token rather than refused as "
            "out-of-vocabulary")

    @pytest.mark.parametrize("line", [
        f"**{_P5_FIELD}: VERIFIED.**",
        f"**{_P5_FIELD}**: VERIFIED",
        f"__{_P5_FIELD}: VERIFIED__",
    ])
    def test_the_house_bold_wrapped_form_is_accepted(self, tmp_path, line):
        """This tree's house form wraps the label AND the value in one bold span
        (`**Verdict: SHIP.**` -- 30 of the 38 corpus passes).  Emphasis is
        stripped from the field scope first, which is `_parse_verdict`'s existing
        rule, so the dominant spelling of a brand-new field is not refused."""
        assert _p5_violations(
            tmp_path, trailer=_p5_backstop(attestation_line=line)) == [], line

    def test_the_backstop_below_the_first_h3_does_not_count(self, tmp_path):
        """R2's field scope, unchanged: a field parked under an H3 is not a
        field.  That is what makes the scope a contract rather than a search --
        and it means a reviewer cannot satisfy the backstop from inside a
        `### Coverage` subsection."""
        v = _p5_violations(tmp_path,
                           trailer="### Coverage\n\n" + _p5_backstop())
        assert any(f"missing '{_P5_FIELD}:'" in m for m in v), v
        assert any("missing 'Basis:'" in m for m in v), v

    @pytest.mark.parametrize("state", ["open", "executing", "review"])
    def test_the_backstop_is_owed_only_at_an_archive_effective_state(
            self, tmp_path, state):
        """It is a CODE-review obligation, so it arrives when the Code-review
        half is consulted -- at `ready-to-archive` / `archived` -- not the moment
        a plan declares inheritance.  An inherited plan still executing owes
        nothing here."""
        assert _p5_violations(tmp_path, state=state,
                              trailer=_p5_backstop(value=None,
                                                   basis=None)) == []

    @pytest.mark.parametrize("state", ["ready-to-archive", "archived"])
    def test_both_archive_effective_states_owe_it(self, tmp_path, state):
        v = _p5_violations(tmp_path, state=state,
                           trailer=_p5_backstop(value=None, basis=None))
        assert _p5_field_violations(v), (state, v)


class TestP5BasisBindingShape:
    """The three bindings' SHAPE -- never their truth (amendment R6)."""

    def test_the_basis_line_is_required(self, tmp_path):
        v = _p5_violations(tmp_path, trailer=_p5_backstop(basis=None))
        assert any("missing 'Basis:'" in m for m in v), v

    def test_a_duplicate_basis_line_refuses(self, tmp_path):
        """Two bindings in one record is an ambiguity a backstop must not
        resolve by picking one."""
        v = _p5_violations(
            tmp_path, trailer=_p5_backstop() + f"Basis: {_P5_BASIS}\n")
        assert any("duplicate 'Basis:'" in m for m in v), v

    def test_an_empty_basis_value_refuses(self, tmp_path):
        v = _p5_violations(tmp_path, trailer=_p5_backstop(basis_line="Basis:"))
        assert any("empty 'Basis:'" in m for m in v), v

    @pytest.mark.parametrize("dropped", ["proposal", "plan", "changed-paths"])
    def test_each_binding_is_required_on_its_own(self, tmp_path, dropped):
        basis = "; ".join(
            part for part in (f"proposal={_P5_PROPOSAL_SHA}",
                              f"plan={_P5_PLAN_SHA}",
                              "changed-paths=abc1234^..def5678")
            if not part.startswith(dropped + "="))
        v = _p5_violations(tmp_path, trailer=_p5_backstop(basis=basis))
        assert any(f"no '{dropped}=' binding" in m for m in v), (dropped, v)

    def test_a_duplicate_binding_refuses_even_when_the_two_agree(self, tmp_path):
        v = _p5_violations(
            tmp_path,
            trailer=_p5_backstop(basis=_P5_BASIS
                                 + f"; plan={_P5_PLAN_SHA}"))
        assert any("duplicate 'plan=' binding" in m for m in v), v

    @pytest.mark.parametrize("key", ["proposal", "plan"])
    @pytest.mark.parametrize("bad", [
        "abc1234", "0123456789abcdef", "A" * 40, "0123456789ABCDEF" * 2 + "0123",
        "g" * 40, "a" * 39, "a" * 41, "HEAD", "v1.2.3",
    ])
    def test_an_abbreviated_or_non_hex_commit_is_not_a_full_binding(
            self, tmp_path, key, bad):
        """The parent asks for a *full* commit twice ("accepted full commit",
        "reviewed full commit"), and an abbreviation is the one thing a BINDING
        may not be: abbreviations collide, and a colliding binding names two
        commits.  Deliberately stricter than the file's own `_COMMIT_ID_RE`,
        which admits 7-40 hex because it reads prose, not bindings."""
        basis = _P5_BASIS.replace(
            f"{key}=" + (_P5_PROPOSAL_SHA if key == "proposal"
                         else _P5_PLAN_SHA),
            f"{key}={bad}")
        v = _p5_violations(tmp_path, trailer=_p5_backstop(basis=basis))
        assert any("not a FULL commit id" in m for m in v), (key, bad, v)

    def test_a_backticked_commit_id_is_accepted(self, tmp_path):
        """The house style backticks commit ids -- `_COMMIT_ID_RE`'s own comment
        says "usually backticked" -- so refusing the tree's own spelling would be
        a gratuitous refusal of a correct binding."""
        basis = (f"proposal=`{_P5_PROPOSAL_SHA}`; plan=`{_P5_PLAN_SHA}`; "
                 "changed-paths=`abc1234^..def5678`")
        assert _p5_violations(tmp_path, trailer=_p5_backstop(basis=basis)) == []

    @pytest.mark.parametrize("changed", [
        "abc1234^..def5678", "286f07d^..286f07d",
        "dev/plans/x.md > manifest", "the 41 paths listed in section 3",
        "HEAD~4..HEAD",
    ])
    def test_changed_paths_is_free_text(self, tmp_path, changed):
        """The parent admits "reviewed range or manifest" -- two different
        notations -- so a pattern narrow enough to validate one would refuse the
        other.  Non-emptiness is the whole contract here."""
        basis = (f"proposal={_P5_PROPOSAL_SHA}; plan={_P5_PLAN_SHA}; "
                 f"changed-paths={changed}")
        assert _p5_violations(
            tmp_path, trailer=_p5_backstop(basis=basis)) == [], changed

    def test_an_empty_binding_value_refuses(self, tmp_path):
        basis = (f"proposal={_P5_PROPOSAL_SHA}; plan={_P5_PLAN_SHA}; "
                 "changed-paths=")
        v = _p5_violations(tmp_path, trailer=_p5_backstop(basis=basis))
        assert any("empty 'changed-paths=' binding" in m for m in v), v

    def test_the_parents_own_wrapped_rendering_is_accepted(self, tmp_path):
        """The contract as the parent RENDERS it -- wrapped, with
        `changed-paths=` on an indented second line.  A tool that refused the
        block it quotes would teach authors to distrust it."""
        trailer = _p5_backstop(basis=None) + (
            f"Basis: proposal={_P5_PROPOSAL_SHA}; plan={_P5_PLAN_SHA};\n"
            "       changed-paths=abc1234^..def5678\n")
        assert _p5_violations(tmp_path, trailer=trailer) == []

    def test_the_fold_absorbs_only_an_indented_binding_continuation(
            self, tmp_path):
        """Maximally tight, so the fold can only absorb what it is for.  An
        UNINDENTED continuation is a new line, not a fold, and the binding it
        carries is therefore missing -- which refuses rather than silently
        half-parsing."""
        trailer = _p5_backstop(basis=None) + (
            f"Basis: proposal={_P5_PROPOSAL_SHA}; plan={_P5_PLAN_SHA};\n"
            "changed-paths=abc1234^..def5678\n")
        v = _p5_violations(tmp_path, trailer=trailer)
        assert any("no 'changed-paths=' binding" in m for m in v), v

    def test_the_fold_cannot_swallow_the_next_field(self, tmp_path):
        """The continuation must begin with a binding key, so no other field,
        heading or prose line can be absorbed into the value -- the hazard a
        looser "any indented line" fold would create.

        **`proposal=` is written LAST on purpose, and the ordering is what makes
        this node a falsifier.**  The final binding absorbs everything to the end
        of the value, so it is the only position where a loosened fold becomes
        observable: swallowed text lands in a *commit* binding and refuses as
        "not a FULL commit id".  With `proposal=` first, the swallowed text would
        land in free-text `changed-paths=` instead, and this node would pass under
        both the tight and the loose pattern -- proving nothing while looking like
        a check.  (Measured: written that way, the loosening mutation survived.)
        """
        trailer = ("Basis: changed-paths=abc1234^..def5678; "
                   f"plan={_P5_PLAN_SHA}; proposal={_P5_PROPOSAL_SHA}\n"
                   f"    {_P5_FIELD}: VERIFIED\n")
        v = _p5_violations(tmp_path, trailer=trailer)
        # The indented attestation was NOT folded into `Basis:` -- but nor is an
        # indented line a field, so the attestation is still missing, and that
        # is the ONLY finding: the `Basis:` line itself parsed cleanly.
        assert len(v) == 1, v
        assert f"missing '{_P5_FIELD}:'" in v[0], v

    def test_a_missing_separator_between_bindings_still_parses_three(
            self, tmp_path):
        """Read with `finditer` rather than by splitting on `;`, so the likeliest
        real typo -- a separator lost at a line fold -- parses into three
        bindings instead of reporting `changed-paths` as absent and sending the
        author looking for a binding they wrote."""
        basis = (f"proposal={_P5_PROPOSAL_SHA} plan={_P5_PLAN_SHA} "
                 "changed-paths=abc1234^..def5678")
        assert _p5_violations(tmp_path, trailer=_p5_backstop(basis=basis)) == []

    def test_text_before_the_first_binding_refuses(self, tmp_path):
        v = _p5_violations(
            tmp_path,
            trailer=_p5_backstop(basis="see the manifest, " + _P5_BASIS))
        assert any("before its first binding" in m for m in v), v

    def test_a_basis_naming_none_of_the_bindings_refuses(self, tmp_path):
        v = _p5_violations(
            tmp_path, trailer=_p5_backstop(basis="the reviewed range"))
        assert any("names none of the three required bindings" in m
                   for m in v), v


def _p5_legacy_pass() -> tuple[str, str]:
    """A ``(stem, raw heading)`` pair the Code-review legacy manifest admits.

    Resolved from the live tree rather than hard-coded, which does two things: it
    proves the enumeration still points at a real record, and it keeps a
    reviewer's byline (every one of them a vendor name) out of this file.  Stems
    carrying a blocking legacy verdict are skipped --
    `_legacy_disposition_violations` adds findings of its own and would blur this
    node's single property.
    """
    for stem, digests in sorted(planner._LEGACY_CODE_REVIEW_RECORDS.items()):
        if stem in planner._LEGACY_CODE_REVIEW_DISPOSITIONS:
            continue
        for fam in ("plans", "plans/archive"):
            path = CAIRN_ROOT / "dev" / fam / f"{stem}.md"
            if not path.is_file():
                continue
            for raw in path.read_text(encoding="utf-8").split("\n"):
                dig = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
                if dig in digests and planner._CODE_REVIEW_PASS_RE.match(raw):
                    return stem, raw
    return "", ""


class TestP5Placement:
    """Where the check sits, and what it refuses to claim."""

    def test_the_backstop_is_checked_before_the_legacy_fence(self, tmp_path):
        """P1's ordering rule, applied to this obligation.
        `_LEGACY_CODE_REVIEW_RECORDS` grandfathers records written before the
        Code-review schema existed, and its `return` is an EARLY return -- so a
        check placed after it is swallowed for every admitted record.  A plan
        declaring `Inherited proposal basis:` necessarily post-dates P2-R, so no
        legacy record can honestly claim this exemption; putting the check first
        costs nothing today and removes a laundering path from the file."""
        stem, heading = _p5_legacy_pass()
        assert stem and heading, (
            "no legacy Code-review pass resolved from the manifest -- this "
            "node's premise is gone, re-derive `_LEGACY_CODE_REVIEW_RECORDS`")
        body = f"{heading}\n\nthe reading.\n\n"
        clean = planner.review_record_violations(
            _plan_art(tmp_path, body, status="archived",
                      plan_review="not required(x)", stem=stem), "archived")
        assert clean == [], (
            "the legacy fence no longer exempts this record, so the node cannot "
            f"isolate P5's placement: {clean}")
        inherited = planner.review_record_violations(
            _plan_art(tmp_path, body, status="archived",
                      plan_review="not required(x)", stem=stem,
                      header_extra=_P5_DECLARATION), "archived")
        assert _p5_field_violations(inherited), inherited

    def test_both_gate_surfaces_report_the_same_p5_finding(self, tmp_path):
        """S12 -- one predicate, both call sites.  `scan` (via
        `_conformance_violations`) and `next --to archived` (via
        `_gating_preconditions`) must reach the same finding: wiring only the
        first is the exact defect [R3-E1] executed on the Code-review half."""
        identity = planner.IdentityModel(frozenset(), frozenset())
        body = _code_review_pass(trailer=_p5_backstop(value=None))
        archived = _plan_art(tmp_path, body, status="archived",
                             plan_review="not required(x)", stem=_P5_STEM,
                             header_extra=_P5_DECLARATION)
        ready = _plan_art(tmp_path, body, status="ready-to-archive",
                          plan_review="not required(x)", stem=_P5_STEM,
                          header_extra=_P5_DECLARATION)
        expected = planner.review_record_violations(archived, "archived")
        assert _p5_field_violations(expected), expected
        # Containment, not equality: `_conformance_violations` on an `archived`
        # plan also reports the two archive preconditions (Dispositions, the
        # loop-fidelity sign-off), which are not review-record findings.  What
        # this node owns is that P5's findings reach BOTH surfaces verbatim.
        reported = planner._conformance_violations(archived, identity)
        for msg in expected:
            assert msg in reported, (msg, reported)
        gates = planner._gating_preconditions(ready, "archived", identity)
        record_gates = [g for g in gates if "the review record conforms" in g[1]]
        assert len(record_gates) == 1, gates
        met, desc = record_gates[0]
        assert met is False
        for msg in expected:
            assert msg in desc

    def test_a_verified_claim_is_accepted_without_any_semantic_check(
            self, tmp_path):
        """**The exclusion, asserted as behavior.**  The amendment's R6 excludes
        "Semantic verification of `Contract non-expansion`", and the parent is
        explicit that this "remains a semantic human/agent review; the parser
        validates the record and bindings but does not pretend to prove prose
        equivalence."

        So a `VERIFIED` naming two well-formed commit ids that exist in no
        repository, over a plan whose scope obviously expanded, is SILENT.  That
        is not a gap in P5 -- it is P5's contract, and this node exists so a
        later reader cannot mistake the silence for a check that ran.  The
        honest reach of the tool is: the record exists, its vocabulary is closed,
        and its bindings are shaped like bindings."""
        basis = ("proposal=" + "f" * 40 + "; plan=" + "0" * 40
                 + "; changed-paths=no/such/range")
        assert _p5_violations(tmp_path, trailer=_p5_backstop(basis=basis)) == []

    def test_the_full_commit_pattern_is_stricter_than_the_prose_pattern(self):
        """Two commit-id patterns in one file is a smell unless the difference is
        deliberate, so it is pinned: `_COMMIT_ID_RE` reads prose and admits an
        abbreviation; `_FULL_COMMIT_RE` reads a binding and does not."""
        assert planner._COMMIT_ID_RE.search("abc1234")
        assert planner._FULL_COMMIT_RE.match("abc1234") is None
        assert planner._FULL_COMMIT_RE.match("a" * 40)
        assert planner._FULL_COMMIT_RE.match("A" * 40) is None

    def test_the_p5_block_reaches_no_git_and_no_other_artifact(self):
        """A source-level fence on the exclusion above.  Semantic verification
        would need either git or the proposal's bytes; neither is reachable from
        this block, so a later widening has to add the reach explicitly rather
        than arrive by edit.

        **The end marker moved when P2-R landed, and the property did not.**  It
        was `def review_record_violations(`, which stopped being P5's boundary the
        moment P2's block was inserted between the two; it is now P2's own block
        header.  P2 *does* read one other artifact -- that is the inheritance
        chain the accepted parent asks for -- and it carries its own fence
        (`test_the_p2_block_reaches_no_git`).  Re-pointing this marker rather than
        deleting the node is what keeps P5's exclusion asserted instead of
        quietly absorbed into a looser one."""
        src = _PLANNER_PATH.read_text(encoding="utf-8")
        start = src.index("def _declares_inheritance(")
        end = src.index("# === P2-R -- plan-readiness inheritance")
        assert start < end, "the P5 block no longer precedes the P2 block"
        block = src[start:end]
        for forbidden in ("_git_readonly", "subprocess", "read_text",
                          "_repo_root", "Popen"):
            assert forbidden not in block, forbidden


# ===========================================================================
# Chunk E -- the accepted status vocabulary, its transitions, R3's
# multi-obligation plan review, R4's orthogonal `Blocked by`, and R6's eight
# status/evidence contradictions.
#
# Source contract: accepted proposal
# `dev/proposals/archive/2026-08-10-codex-lifecycle-status-vocabulary.md`,
# Revision 4 -- operative clauses R1 (as replaced by "R1 replacement"), R2, R3,
# R4 and R6.  Plan cell: `dev/plans/review-efficient-lifecycle.md` > Chunk E.
#
# **What Chunk E deliberately did NOT do, asserted here so it cannot drift into
# happening by accident.**  The accepted text says *"Replace `open`,
# `executing`, and `review`"*.  E made the new tokens legal and left the three
# old ones legal, because all three are declared by live plans -- two of them
# another session's -- and `scan` reporting every live artifact sound is one of
# the plan's acceptance criteria.  The retirement is Chunk H1's named job, and
# `TestTheLegacyTokensAreStillLegalUntilH1` is what makes the split visible
# rather than a silent narrowing.
# ===========================================================================

_E_STEM = "e-fixture"          # deliberately in NEITHER legacy manifest

#: A proposal `## Review` record in the post-P1 conforming shape, with the two
#: closed fields E2 reads.  Each part independently omittable so a node can vary
#: exactly one property.
def _prop_review_pass(*, reviewer: str = "Reviewer A (External)",
                      date: str = "2026-05-02", tier: str | None = "External",
                      findings: str | None = "none",
                      response: bool = False) -> str:
    out = f"## Review -- {reviewer} -- {date}\n\n" + _BASIS_LINES
    if tier is not None:
        out += f"**Tier**: {tier}\n"
    if findings is not None:
        out += f"**Findings**: {findings}\n"
    out += "\nthe reading.\n\n"
    if response:
        out += f"## Response -- Claude -- {date}\n\nthe reply.\n\n"
    return out


def _e_repo(tmp_path) -> Path:
    """`_make_repo`, but idempotent within one `tmp_path`.

    `_make_repo` hard-fails on a second call (`mkdir` without `exist_ok`), and
    several nodes below legitimately need two artifacts in one tree to compare
    them.  Reusing the tree is also closer to what the tool sees.
    """
    repo = tmp_path / "repo"
    return repo if repo.is_dir() else _make_repo(tmp_path)


def _e_prop(tmp_path, *, status: str, body: str = "", author: str = "Claude",
            name: str = "p.md"):
    path = _write_proposal(_e_repo(tmp_path), name, status=status, author=author,
                           body=body)
    return planner._read_artifact(path)


def _e_conf(art) -> list:
    return planner._conformance_violations(
        art, planner.IdentityModel(frozenset(), frozenset()))


def _e_gates(art, target) -> list:
    return planner._gating_preconditions(
        art, target, planner.IdentityModel(frozenset(), frozenset()))


class TestTheAcceptedVocabularyIsDeclared:
    """R1'/R2' -- the tokens themselves, as data (Chunk A1's seam, used)."""

    def test_every_accepted_proposal_state_is_legal(self):
        for state in ("awaiting-review", "revising", "awaiting-decision",
                      "accepted", "rejected", "superseded"):
            assert state in planner.PROPOSAL_STATES, state

    def test_every_accepted_plan_state_is_legal(self):
        for state in ("awaiting-plan-review", "revising-plan",
                      "ready-to-implement", "implementing",
                      "awaiting-code-review", "revising-code",
                      "ready-to-archive", "archived"):
            assert state in planner.PLAN_STATES, state

    def test_the_terminal_classification_did_not_move(self):
        """Every new state is non-terminal: the accepted tables add no terminal
        state, and mis-classifying one would silently strand an artifact."""
        assert planner.PROPOSAL_TERMINAL_STATES == (
            "accepted", "rejected", "superseded")
        assert planner.PLAN_TERMINAL_STATES == ("archived",)
        for new in ("awaiting-review", "revising", "awaiting-decision"):
            assert new in planner.PROPOSAL_NON_TERMINAL_STATES
        for new in ("revising-plan", "ready-to-implement", "implementing",
                    "awaiting-code-review", "revising-code",
                    "ready-to-archive"):
            assert new in planner.PLAN_NON_TERMINAL_STATES

    def test_shape_b_covers_every_current_non_terminal_state(self):
        """The accepted "R5 replacement": shape (b) *"considers every recognized
        current non-terminal status plus the historical opening statuses"*.  The
        set is derived, so this asserts the derivation rather than a literal."""
        for state in (planner.PROPOSAL_NON_TERMINAL_STATES
                      + planner.PLAN_NON_TERMINAL_STATES):
            assert state in planner.SHAPE_B_STATUSES, state
        for state in planner.PROPOSAL_TERMINAL_STATES + planner.PLAN_TERMINAL_STATES:
            assert state not in planner.SHAPE_B_STATUSES, state

    def test_every_declared_state_is_recognized_by_the_consumers(self):
        for state in planner.PROPOSAL_STATES + planner.PLAN_STATES:
            assert state in planner.RECOGNIZED_STATES, state


class TestTheLegacyTokensAreStillLegalUntilH1:
    """The sequencing decision, pinned as behaviour so it cannot drift silently.

    Both directions matter.  If a later change retires the three tokens *without*
    migrating the artifacts, the first two nodes redden.  When H1 *does* migrate
    them, the third node is what tells the implementer that retiring the tokens
    means moving them into the historical tuples -- not deleting them, because
    metrics must keep parsing pre-migration commits.
    """

    @pytest.mark.parametrize("state", ["open", "executing", "review"])
    def test_the_three_pending_retirement_plan_tokens_are_still_legal(self, state):
        assert state in planner.PLAN_STATES, state
        assert planner._legal_transitions.__module__  # the table is consulted

    @pytest.mark.parametrize("state", ["proposed", "reviewed", "revised"])
    def test_the_three_pending_retirement_proposal_tokens_are_still_legal(
            self, state):
        assert state in planner.PROPOSAL_STATES, state

    def test_the_historical_tuples_are_still_empty_and_that_is_the_seam(self):
        """A token becomes historical when the migration removes it from an active
        artifact, not when a newer name for it exists.  Listing `executing` here
        while a live plan declares it would make the planner contradict the tree
        it scans."""
        assert planner.HISTORICAL_PROPOSAL_STATES == ()
        assert planner.HISTORICAL_PLAN_STATES == ()

    def test_each_legacy_state_keeps_a_forward_path(self, tmp_path):
        """The concrete hazard: a live plan whose token is still legal but whose
        transition table lost its arm has no legal move at all."""
        repo = _e_repo(tmp_path)
        for state in ("open", "executing", "review"):
            path = _write_plan(repo, f"{state}.md", status=state)
            art = planner._read_artifact(path)
            assert planner._legal_transitions(art), state


class TestEveryLegalTransition:
    """R1/R2's cycles, exhaustively, through the public `next` path."""

    _PROPOSAL_CYCLE = [
        ("", ["awaiting-review"]),
        ("awaiting-review", ["revising", "awaiting-decision"]),
        ("revising", ["awaiting-review"]),
        ("awaiting-decision", ["accepted", "rejected", "superseded", "revising"]),
        ("accepted", []),
        ("rejected", []),
        ("superseded", []),
    ]

    @pytest.mark.parametrize("status,expected", _PROPOSAL_CYCLE)
    def test_the_proposal_cycle_matches_the_accepted_table(
            self, tmp_path, status, expected):
        art = _e_prop(tmp_path, status=status)
        assert planner._legal_transitions(art) == expected

    @pytest.mark.parametrize("status,expected", [
        ("", ["awaiting-plan-review"]),
        ("awaiting-plan-review", ["revising-plan", "ready-to-implement",
                                  "executing"]),
        ("revising-plan", ["awaiting-plan-review"]),
        ("ready-to-implement", ["implementing"]),
        ("implementing", ["awaiting-code-review"]),
        ("awaiting-code-review", ["revising-code", "ready-to-archive"]),
        ("revising-code", ["awaiting-code-review"]),
        ("ready-to-archive", ["archived"]),
        ("archived", []),
    ])
    def test_the_plan_cycle_matches_the_accepted_table(
            self, tmp_path, status, expected):
        repo = _make_repo(tmp_path)
        path = _write_plan(repo, "x.md", status=status)
        assert planner._legal_transitions(
            planner._read_artifact(path)) == expected

    def test_both_revision_loops_return_to_their_waiting_state(self, tmp_path):
        """The two loops R2 names *"deliberately specific"*: a plan's design loop
        and its implementation loop are distinct cycles, and neither exit leaks
        into the other."""
        repo = _e_repo(tmp_path)
        design = planner._read_artifact(
            _write_plan(repo, "d.md", status="revising-plan"))
        code = planner._read_artifact(
            _write_plan(repo, "c.md", status="revising-code"))
        assert planner._legal_transitions(design) == ["awaiting-plan-review"]
        assert planner._legal_transitions(code) == ["awaiting-code-review"]
        # And the proposal loop, which is the third and returns to review.
        prop = _e_prop(tmp_path, status="revising")
        assert planner._legal_transitions(prop) == ["awaiting-review"]

    def test_the_fast_path_opens_at_implementing_only_when_review_is_not_required(
            self, tmp_path):
        """R2's accepted fast path, and its fence.

        *"the plan-open commit may record `implementing` directly; it must contain
        the implementation evidence that makes the skipped `ready-to-implement`
        state true."*  Offered from the not-yet-created state for a plan that owes
        no distinct review -- and NEVER offered to a plan that declares
        `required(...)` and has not cleared it, which is R6's refusal case.
        """
        repo = _e_repo(tmp_path)
        free = planner._read_artifact(_write_plan(
            repo, "free.md", status="", plan_review="not required(doc sync)"))
        gated = planner._read_artifact(_write_plan(
            repo, "gated.md", status="", plan_review="required(External)"))
        assert planner._legal_transitions(free) == [
            "ready-to-implement", "implementing"]
        assert planner._legal_transitions(gated) == ["awaiting-plan-review"]
        assert "implementing" not in planner._legal_transitions(gated)

    def test_an_illegal_new_vocabulary_transition_is_refused(
            self, tmp_path, monkeypatch, capsys):
        repo = _e_repo(tmp_path)
        _write_plan(repo, "x.md", status="awaiting-plan-review")
        monkeypatch.chdir(repo)
        rc = planner.main(["next", "dev/plans/x.md", "--to", "ready-to-archive"])
        out = capsys.readouterr().out
        assert rc == 1
        assert "not a legal next transition" in out

    def test_every_legal_target_has_a_scaffold_and_no_fallback_is_reached(
            self, tmp_path, monkeypatch, capsys):
        """The `_scaffold` fallback line is unreachable *given* the transition
        table, and that claim is only true if every target has a branch.  Walked
        over the whole table rather than the handful anyone happened to try."""
        repo = _e_repo(tmp_path)
        monkeypatch.chdir(repo)
        for status in planner.PLAN_STATES + ("",):
            path = _write_plan(repo, "w.md", status=status,
                               plan_review="not required(x)")
            art = planner._read_artifact(path)
            for target in planner._legal_transitions(art):
                status_from, status_to, blocks = planner._scaffold(
                    art, target, "2026-05-01")
                assert blocks, (status, target)
                assert "no scaffold defined" not in " ".join(blocks), (
                    status, target)
                assert status_to == target or target in status_to, (status, target)
        for status in planner.PROPOSAL_STATES + ("",):
            art = _e_prop(tmp_path, status=status)
            for target in planner._legal_transitions(art):
                _f, _t, blocks = planner._scaffold(art, target, "2026-05-01")
                assert "no scaffold defined" not in " ".join(blocks), (
                    status, target)

    def test_a_status_only_flip_refuses_to_scaffold_an_empty_commit(self, tmp_path):
        """R4 -- *"Do not create empty commits merely to advance a label."*  Every
        transition that appends no new section says whose commit carries it, so the
        tool never hands an operator a section to paste that the contract forbids
        them to commit alone."""
        repo = _e_repo(tmp_path)
        art = planner._read_artifact(
            _write_plan(repo, "x.md", status="awaiting-code-review"))
        for target in ("revising-code", "ready-to-archive"):
            _f, _t, blocks = planner._scaffold(art, target, "2026-05-01")
            joined = " ".join(blocks)
            assert "NO new section is appended" in joined, target
            assert "empty commits merely to advance a label" in joined, target
            assert "CODE REVIEWER" in joined, target


class TestMultiObligationPlanReview:
    """R3 -- `required(A + B)` is two obligations and two distinct passes.

    The defect this closes was live and silent at Chunk E's parent:
    `normalize_required_tier('required(**External** + **External Security
    Review**)')` returned `('external', None)`, so the second obligation was
    *discarded* and one pass reported the floor satisfied.
    """

    _MULTI = "required(**External** + **External Security Review**)"

    def _pass(self, obligation, *, tier="External", date="2026-05-01",
              findings="none"):
        block = _pass_block(reviewer=f"R{date[-2:]}", date=date, tier=tier,
                            findings=findings)
        if obligation is None:
            return block
        return block.replace("**Tier**:", f"**Obligation**: {obligation}\n**Tier**:")

    def _v(self, tmp_path, body, review=None):
        return _violations(tmp_path, body, stem=_E_STEM,
                           plan_review=review or self._MULTI)

    def test_the_declaration_resolves_to_two_obligations(self):
        obligations, violation = planner.normalize_required_obligations(self._MULTI)
        assert violation is None
        assert obligations == (("External", "external"),
                               ("External Security Review", "external"))

    def test_the_single_obligation_schema_is_unchanged(self):
        """R3: *"The current one-obligation schema remains unchanged."*  So a
        one-clause plan needs no `**Obligation**:` line at all."""
        assert planner.normalize_required_obligations("required(Internal)") == (
            (("Internal", "internal"),), None)
        assert planner.normalize_required_tier(self._MULTI) == ("external", None)

    def test_one_pass_cannot_clear_two_clauses(self, tmp_path):
        """The property R3 exists for, stated as the sharpest possible fixture: a
        single pass whose `**Obligation**:` names *both* clauses verbatim."""
        v = self._v(tmp_path, self._pass("External + External Security Review"))
        assert len(v) == 2, v
        for clause in ("External", "External Security Review"):
            assert any(repr(clause) in m for m in v), (clause, v)

    def test_two_passes_one_per_clause_clear_the_floor(self, tmp_path):
        assert self._v(tmp_path, self._pass("External")
                       + self._pass("External Security Review",
                                    date="2026-05-02")) == []

    def test_two_passes_naming_the_same_clause_leave_the_other_outstanding(
            self, tmp_path):
        v = self._v(tmp_path, self._pass("External")
                    + self._pass("External", date="2026-05-02"))
        assert len(v) == 1, v
        assert "'External Security Review'" in v[0]

    def test_a_missing_obligation_line_clears_nothing(self, tmp_path):
        v = self._v(tmp_path, self._pass(None) + self._pass(None, date="2026-05-02"))
        assert len(v) == 2, v

    def test_a_duplicate_obligation_line_in_one_pass_clears_nothing(self, tmp_path):
        both = self._pass("External").replace(
            "**Obligation**: External\n",
            "**Obligation**: External\n**Obligation**: External Security Review\n")
        v = self._v(tmp_path, both + self._pass("External Security Review",
                                                date="2026-05-02"))
        assert len(v) == 1, v
        assert "'External'" in v[0]

    def test_an_undeclared_obligation_value_clears_nothing(self, tmp_path):
        v = self._v(tmp_path, self._pass("Internal")
                    + self._pass("External Security Review", date="2026-05-02"))
        assert len(v) == 1, v
        assert "'External'" in v[0]

    def test_the_declared_tier_must_satisfy_the_named_obligation(self, tmp_path):
        """R3: *"The existing `**Tier**:` value must satisfy the named
        obligation"* -- so an `External Security Review` clause is not cleared by
        an Internal-tier pass that names it."""
        v = self._v(tmp_path, self._pass("External")
                    + self._pass("External Security Review", tier="Internal",
                                 date="2026-05-02"))
        assert len(v) == 1, v
        assert "'External Security Review'" in v[0]

    def test_emphasis_and_whitespace_normalize_on_both_sides(self, tmp_path):
        """R3: matched *"after the same emphasis and whitespace normalization used
        by the tier parser"*.  One helper does both sides, so this is the node that
        would catch them drifting apart."""
        assert self._v(tmp_path, self._pass("**External**")
                       + self._pass("__External   Security  Review__",
                                    date="2026-05-02")) == []

    @pytest.mark.parametrize("field,expected", [
        ("required(External + )", "empty obligation clause"),
        ("required(External + External)", "duplicate obligation clause"),
        ("required(External + Bogus)", "unrecognized required tier"),
        ("required(not External + External)", "unrecognized required tier"),
    ])
    def test_a_malformed_plus_declaration_fails_closed(self, field, expected):
        obligations, violation = planner.normalize_required_obligations(field)
        assert obligations == ()
        assert expected in violation, violation

    def test_a_malformed_declaration_is_reported_and_clears_nothing(self, tmp_path):
        v = self._v(tmp_path, self._pass("External"),
                    review="required(External + External)")
        assert any("duplicate obligation clause" in m for m in v), v

    def test_this_plans_own_record_resolves_both_clauses(self):
        """**The live self-test.**  `review-efficient-lifecycle` declares exactly
        this two-obligation tier and carries real `**Obligation**:` lines, so the
        fix is evaluated against the record it was written for: both clearing
        passes resolve, the Internal review of the Maintainer-directed revision
        resolves to NO clause (its obligation names that revision section, not a
        declared clause), and the artifact stays sound."""
        path = CAIRN_ROOT / "dev" / "plans" / "review-efficient-lifecycle.md"
        art = planner._read_artifact(path)
        obligations, violation = planner.normalize_required_obligations(
            art.plan_review)
        assert violation is None
        assert len(obligations) == 2, obligations
        lines = art.text.split("\n")
        boundaries = planner._record_boundaries(art)
        bound = [planner._pass_obligation(
            planner._record_field_scope(lines, sec.line_no, boundaries),
            obligations) for sec, _dig in planner._pass_headings(art)]
        assert set(bound) == {"External", "External Security Review", None}
        assert bound.count(None) == 1, bound
        assert planner.review_record_violations(art) == []


class TestBlockedByIsNonAuthoritative:
    """R4 -- *"The field never changes the legal state machine and never
    substitutes for a status."*  Three negatives and two shape checks."""

    def _plan(self, tmp_path, blocked, *, status="implementing"):
        repo = _e_repo(tmp_path)
        extra = "" if blocked is None else f"**Blocked by**: {blocked}\n"
        path = repo / "dev" / "plans" / f"b{len(list((repo / 'dev' / 'plans').glob('*.md')))}.md"
        path.write_text(
            f"# b\n\n**Status**: {status}\n"
            f"**Plan review**: not required(fixture)\n{extra}\n"
            "## Scope\n\nx\n", encoding="utf-8")
        return planner._read_artifact(path)

    def test_absence_is_the_no_blocker_record_and_not_a_finding(self, tmp_path):
        assert planner.blocked_by_violations(self._plan(tmp_path, None)) == []

    def test_a_named_condition_is_accepted_without_being_verified(self, tmp_path):
        """The tool cannot tell a falsifiable condition from prose, and says so
        rather than pretending: any non-empty value passes the shape check."""
        art = self._plan(tmp_path, "the 2026-09 release ceremony")
        assert planner.blocked_by_violations(art) == []
        art = self._plan(tmp_path, "vibes")
        assert planner.blocked_by_violations(art) == []

    def test_a_duplicate_field_refuses(self, tmp_path):
        art = self._plan(tmp_path, "one\n**Blocked by**: two")
        v = planner.blocked_by_violations(art)
        assert len(v) == 1 and "duplicate" in v[0], v

    def test_an_empty_value_refuses(self, tmp_path):
        art = self._plan(tmp_path, "")
        v = planner.blocked_by_violations(art)
        assert len(v) == 1 and "empty" in v[0], v

    def test_it_changes_no_legal_transition(self, tmp_path):
        """The orthogonality, as behaviour: the same plan with and without a
        blocker has the identical legal set and the identical gate verdicts."""
        identity = planner.IdentityModel(frozenset(), frozenset())
        free = self._plan(tmp_path, None)
        blocked = self._plan(tmp_path, "waiting on another plan")
        assert planner._legal_transitions(free) == planner._legal_transitions(blocked)
        for target in planner._legal_transitions(free):
            assert (planner._gating_preconditions(free, target, identity)
                    == planner._gating_preconditions(blocked, target, identity))

    def test_it_never_reaches_the_transition_table(self):
        """A source fence, because the property is the ABSENCE of a read: a later
        edit that keys a transition on the blocker has to add the reach
        explicitly rather than arrive by accident."""
        for function in ("_legal_transitions", "_gating_preconditions"):
            assert "Blocked by" not in _code_of(_PLANNER_PATH, function)
            assert "blocked_by_violations" not in _code_of(_PLANNER_PATH, function)

    def test_a_proposal_carrying_the_field_is_not_read_as_a_plan(self, tmp_path):
        art = _e_prop(tmp_path, status="awaiting-review")
        assert planner.blocked_by_violations(art) == []


class TestR6ContradictionsThroughBothEntryPoints:
    """R6's eight refusals, each through `scan`'s surface AND `next`'s.

    R6: *"`scan`, `next`, and accepted closeout tooling consume shared
    predicates."*  Every node below asserts the contradiction on
    `_conformance_violations` (the current status, what `scan` reports) and on
    `_gating_preconditions` (the requested target, what `next --to` reports), so
    neither surface can be the loose one -- the defect [R3-E1] executed on the
    Code-review half.
    """

    def _both(self, art, state, *, gate_hint: str):
        """The predicate through both public surfaces, plus the shared function."""
        shared = planner.status_evidence_violations(art, state)
        scanned = [m for m in _e_conf(art) if m in shared]
        gates = [(met, desc) for met, desc in _e_gates(art, state)
                 if gate_hint in desc]
        assert len(gates) == 1, (gate_hint, _e_gates(art, state))
        return shared, scanned, gates[0]

    # --- R6 bullet 1: proposal `revising` without a blocking review ----------

    def test_revising_without_any_review_refuses(self, tmp_path):
        art = _e_prop(tmp_path, status="revising")
        shared, scanned, (met, desc) = self._both(
            art, "revising", gate_hint="LATEST '## Review' declares")
        assert any("no '## Review' record is present" in m for m in shared), shared
        assert scanned == shared
        assert met is False
        assert "no '## Review' record is present" in desc

    def test_revising_on_a_clearing_review_refuses(self, tmp_path):
        art = _e_prop(tmp_path, status="revising",
                      body=_prop_review_pass(findings="none"))
        shared, scanned, (met, _d) = self._both(
            art, "revising", gate_hint="LATEST '## Review' declares")
        assert any("'Findings: none'" in m for m in shared), shared
        assert scanned == shared and met is False

    def test_revising_on_a_blocking_review_is_sound(self, tmp_path):
        art = _e_prop(tmp_path, status="revising",
                      body=_prop_review_pass(findings="raised"))
        assert planner.status_evidence_violations(art, "revising") == []
        assert _e_conf(art) == []
        met = [m for m, d in _e_gates(art, "revising")
               if "LATEST '## Review' declares" in d]
        assert met == [True]

    def test_revising_with_no_readable_findings_field_fails_closed(self, tmp_path):
        art = _e_prop(tmp_path, status="revising",
                      body=_prop_review_pass(findings=None))
        assert planner.status_evidence_violations(art, "revising")

    # --- R6 bullet 2: proposal `awaiting-decision` ---------------------------

    def test_awaiting_decision_without_a_review_refuses(self, tmp_path):
        art = _e_prop(tmp_path, status="awaiting-decision")
        shared, scanned, (met, _d) = self._both(
            art, "awaiting-decision", gate_hint="LATEST '## Review' is a clearing")
        assert any("no '## Review' record is present" in m for m in shared), shared
        assert scanned == shared and met is False

    def test_awaiting_decision_on_a_blocking_review_refuses(self, tmp_path):
        art = _e_prop(tmp_path, status="awaiting-decision",
                      body=_prop_review_pass(findings="raised"))
        shared, scanned, (met, _d) = self._both(
            art, "awaiting-decision", gate_hint="LATEST '## Review' is a clearing")
        assert any("'Findings: raised'" in m for m in shared), shared
        assert scanned == shared and met is False

    def test_awaiting_decision_on_the_authors_own_review_refuses(self, tmp_path):
        """R1's replacement requires a review that *cleared the current
        contract*; a self-review is not an independent read, and the tool reads
        the byline (never the reviewer's identity)."""
        art = _e_prop(tmp_path, status="awaiting-decision", author="Claude",
                      body=_prop_review_pass(reviewer="Claude (Strategy)"))
        shared = planner.status_evidence_violations(art, "awaiting-decision")
        assert any("distinct from the proposal author" in m for m in shared), shared

    def test_awaiting_decision_on_a_clearing_independent_review_is_sound(
            self, tmp_path):
        art = _e_prop(tmp_path, status="awaiting-decision",
                      body=_prop_review_pass())
        assert planner.status_evidence_violations(art, "awaiting-decision") == []
        assert _e_conf(art) == []

    @pytest.mark.parametrize("kw", [{"tier": None}, {"findings": None}])
    def test_awaiting_decision_without_the_two_closed_fields_fails_closed(
            self, tmp_path, kw):
        art = _e_prop(tmp_path, status="awaiting-decision",
                      body=_prop_review_pass(**kw))
        assert planner.status_evidence_violations(art, "awaiting-decision")

    # --- R6 bullet 3: plan `revising-plan` ----------------------------------

    def _plan_at(self, tmp_path, status, body="",
                 plan_review="required(External)"):
        return _plan_art(tmp_path, body, status=status, stem=_E_STEM,
                         plan_review=plan_review)

    def test_revising_plan_without_a_pass_refuses(self, tmp_path):
        art = self._plan_at(tmp_path, "revising-plan")
        shared = planner.status_evidence_violations(art, "revising-plan")
        assert any("no conforming '## Plan review" in m for m in shared), shared
        assert [m for m in _e_conf(art) if m in shared] == shared
        gates = [met for met, d in _e_gates(art, "revising-plan")
                 if "LATEST conforming '## Plan review'" in d]
        assert gates == [False]

    def test_revising_plan_on_a_clearing_pass_refuses(self, tmp_path):
        art = self._plan_at(tmp_path, "revising-plan",
                            _pass_block(findings="none"))
        shared = planner.status_evidence_violations(art, "revising-plan")
        assert any("'Findings: none'" in m for m in shared), shared

    def test_revising_plan_on_a_blocking_pass_is_sound(self, tmp_path):
        art = self._plan_at(tmp_path, "revising-plan",
                            _pass_block(findings="raised", sharpening=True))
        assert planner.status_evidence_violations(art, "revising-plan") == []
        gates = [met for met, d in _e_gates(art, "revising-plan")
                 if "LATEST conforming '## Plan review'" in d]
        assert gates == [True]

    def test_revising_plan_does_not_demand_a_clearing_pass(self, tmp_path):
        """The fence that keeps the state reachable: `revising-plan` is where a
        blocking review puts a plan, so requiring the floor to be *cleared* there
        would make the state unreachable by construction."""
        assert "revising-plan" not in planner.PLAN_REVIEW_CLEARED_STATES
        assert "awaiting-plan-review" not in planner.PLAN_REVIEW_CLEARED_STATES

    # --- R6 bullet 4: `ready-to-implement` / `implementing` -----------------

    @pytest.mark.parametrize("state", ["ready-to-implement", "implementing"])
    def test_neither_implementation_state_survives_an_uncleared_floor(
            self, tmp_path, state):
        art = self._plan_at(tmp_path, state, "## Plan review\n\n(awaiting)\n")
        shared = planner.status_evidence_violations(art, state)
        assert any("no conforming pass satisfies it" in m for m in shared), shared
        assert [m for m in _e_conf(art) if m in shared] == shared
        gates = [met for met, d in _e_gates(art, state)
                 if "every declared plan-review obligation is cleared" in d]
        assert gates == [False]

    @pytest.mark.parametrize("state", ["ready-to-implement", "implementing"])
    def test_neither_implementation_state_survives_a_half_cleared_plus_floor(
            self, tmp_path, state):
        """The multi-obligation rule reaching R6 bullet 4: one External pass does
        not admit implementation under a two-clause declaration."""
        body = _pass_block(tier="External").replace(
            "**Tier**:", "**Obligation**: External\n**Tier**:")
        art = self._plan_at(
            tmp_path, state, body,
            plan_review="required(**External** + **External Security Review**)")
        shared = planner.status_evidence_violations(art, state)
        assert any("'External Security Review'" in m for m in shared), shared
        gates = [met for met, d in _e_gates(art, state)
                 if "every declared plan-review obligation is cleared" in d]
        assert gates == [False]

    @pytest.mark.parametrize("state", ["ready-to-implement", "implementing"])
    def test_a_cleared_floor_admits_both_implementation_states(
            self, tmp_path, state):
        art = self._plan_at(tmp_path, state, _pass_block(tier="External"))
        assert planner.status_evidence_violations(art, state) == []
        assert _e_conf(art) == []

    # --- R6 bullet 5: `awaiting-code-review` --------------------------------

    _EVIDENCE = ("## Implementation verification -- Claude -- 2026-05-03\n\n"
                 "the ledger.\n\n")

    def test_awaiting_code_review_without_stable_evidence_refuses(self, tmp_path):
        art = self._plan_at(tmp_path, "awaiting-code-review",
                            _pass_block(tier="External"))
        shared = planner.status_evidence_violations(art, "awaiting-code-review")
        assert any("Implementation verification" in m for m in shared), shared
        assert [m for m in _e_conf(art) if m in shared] == shared
        gates = [met for met, d in _e_gates(art, "awaiting-code-review")
                 if "Implementation verification" in d]
        assert gates == [False]

    def test_awaiting_code_review_with_stable_evidence_is_sound(self, tmp_path):
        art = self._plan_at(tmp_path, "awaiting-code-review",
                            _pass_block(tier="External") + self._EVIDENCE)
        assert planner.status_evidence_violations(
            art, "awaiting-code-review") == []

    @pytest.mark.parametrize("heading", [
        "## Implementation verification -- Claude\n\n",              # undated
        "### Implementation verification -- Claude -- 2026-05-03\n\n",  # H3
        "## Implementation verification -- Claude -- 2026-02-30\n\n",   # impossible
        "## Implementation verifications -- Claude -- 2026-05-03\n\n",  # prefix
    ])
    def test_a_near_miss_evidence_heading_is_not_a_record(self, tmp_path, heading):
        art = self._plan_at(tmp_path, "awaiting-code-review",
                            _pass_block(tier="External") + heading + "x\n\n")
        assert planner.status_evidence_violations(art, "awaiting-code-review")

    def test_a_stale_evidence_record_does_not_return_a_plan_from_revising_code(
            self, tmp_path):
        """R2's word *"replacement"*, made checkable: the record that returns a
        plan to `awaiting-code-review` must come AFTER the blocking pass, not be
        the one that pass already read."""
        stale = (_pass_block(tier="External") + self._EVIDENCE
                 + _code_review_pass(verdict="REVISE", date="2026-05-04"))
        fresh = stale + ("## Implementation verification -- Claude -- "
                         "2026-05-05\n\nthe replacement.\n\n")
        art_stale = self._plan_at(tmp_path, "awaiting-code-review", stale)
        shared = planner.status_evidence_violations(
            art_stale, "awaiting-code-review")
        assert any("predates the latest" in m for m in shared), shared
        art_fresh = self._plan_at(tmp_path, "awaiting-code-review", fresh)
        assert planner.status_evidence_violations(
            art_fresh, "awaiting-code-review") == []

    # --- R6 bullet 6: `revising-code` ---------------------------------------

    def test_revising_code_without_a_code_review_refuses(self, tmp_path):
        art = self._plan_at(tmp_path, "revising-code",
                            _pass_block(tier="External"))
        shared = planner.status_evidence_violations(art, "revising-code")
        assert any("no conforming '## Code review" in m for m in shared), shared
        gates = [met for met, d in _e_gates(art, "revising-code")
                 if "BLOCKING" in d]
        assert gates == [False]

    def test_revising_code_on_a_clearing_verdict_refuses(self, tmp_path):
        art = self._plan_at(tmp_path, "revising-code",
                            _pass_block(tier="External") + _code_review_pass())
        shared = planner.status_evidence_violations(art, "revising-code")
        assert any("CLEARING verdict" in m for m in shared), shared
        assert [m for m in _e_conf(art) if m in shared] == shared

    def test_revising_code_on_a_blocking_verdict_is_sound(self, tmp_path):
        art = self._plan_at(
            tmp_path, "revising-code",
            _pass_block(tier="External") + _code_review_pass(verdict="REVISE"))
        assert planner.status_evidence_violations(art, "revising-code") == []
        gates = [met for met, d in _e_gates(art, "revising-code")
                 if "BLOCKING" in d]
        assert gates == [True]

    def test_revising_code_with_no_readable_verdict_fails_closed(self, tmp_path):
        art = self._plan_at(
            tmp_path, "revising-code",
            _pass_block(tier="External") + _code_review_pass(verdict=None))
        assert planner.status_evidence_violations(art, "revising-code")

    # --- R6 bullets 7 + 8: the shared closeout predicate --------------------

    _CLOSEOUT = _LT + "Dispositions: none\n\n" + _REAL_SIGNOFF

    def test_ready_to_archive_needs_the_latest_clearing_code_review(self, tmp_path):
        art = self._plan_at(
            tmp_path, "ready-to-archive",
            _pass_block(tier="External")
            + _code_review_pass(verdict="REVISE") + self._CLOSEOUT)
        shared = planner.status_evidence_violations(art, "ready-to-archive")
        assert any("BLOCKING verdict" in m for m in shared), shared

    def test_ready_to_archive_needs_every_closeout_precondition(self, tmp_path):
        art = self._plan_at(tmp_path, "ready-to-archive",
                            _pass_block(tier="External") + _code_review_pass())
        shared = planner.status_evidence_violations(art, "ready-to-archive")
        assert any("Dispositions:" in m for m in shared), shared
        assert any("loop-fidelity sign-off" in m for m in shared), shared
        assert all("'ready-to-archive'" in m for m in shared
                   if "status is" in m), shared

    def test_ready_to_archive_and_archived_share_one_closeout_predicate(
            self, tmp_path):
        """R6 bullet 8 verbatim: *"`archived` when the same closeout predicate
        would reject `ready-to-archive`"*.  Asserted as message-for-message
        identity modulo the state name, so neither can be softened alone."""
        body = _pass_block(tier="External") + _code_review_pass()
        art = self._plan_at(tmp_path, "ready-to-archive", body)
        ready = planner.status_evidence_violations(art, "ready-to-archive")
        done = planner.status_evidence_violations(art, "archived")
        assert ready and done
        assert [m.replace("'ready-to-archive'", "'archived'") for m in ready] == done

    def test_a_complete_record_admits_both_archive_effective_states(self, tmp_path):
        body = (_pass_block(tier="External") + _code_review_pass()
                + self._CLOSEOUT)
        art = self._plan_at(tmp_path, "ready-to-archive", body)
        assert planner.status_evidence_violations(art, "ready-to-archive") == []
        assert planner.status_evidence_violations(art, "archived") == []


class TestAReviewThatLeavesAnObligationOpenMovesNothing:
    """R4/R6: *"A pass that leaves another obligation outstanding appends its
    review record without manufacturing a status transition."*

    The no-op case, which is the one an author is most likely to get wrong: the
    first of two required passes has landed, the record legitimately grew, and the
    status must stay where it is.
    """

    _MULTI = "required(**External** + **External Security Review**)"

    def _one_of_two(self):
        return _pass_block(tier="External").replace(
            "**Tier**:", "**Obligation**: External\n**Tier**:")

    def test_the_waiting_state_stays_sound_with_one_of_two_passes(self, tmp_path):
        """`awaiting-plan-review` is not a violation while an obligation is
        outstanding -- that is precisely what the state means."""
        art = _plan_art(tmp_path, self._one_of_two(),
                        status="awaiting-plan-review", stem=_E_STEM,
                        plan_review=self._MULTI)
        assert _e_conf(art) == []

    def test_but_the_forward_transition_is_still_withheld(self, tmp_path):
        art = _plan_art(tmp_path, self._one_of_two(),
                        status="awaiting-plan-review", stem=_E_STEM,
                        plan_review=self._MULTI)
        for target in ("ready-to-implement", "executing"):
            gates = _e_gates(art, target)
            assert gates, target
            assert not all(met for met, _d in gates), (target, gates)

    def test_and_the_second_pass_is_what_moves_it(self, tmp_path):
        body = self._one_of_two() + _pass_block(
            reviewer="S", date="2026-05-02", tier="External").replace(
            "**Tier**:", "**Obligation**: External Security Review\n**Tier**:")
        art = _plan_art(tmp_path, body, status="awaiting-plan-review",
                        stem=_E_STEM, plan_review=self._MULTI)
        gates = _e_gates(art, "ready-to-implement")
        assert all(met for met, _d in gates), gates


class TestTheR6PredicateIsShared:
    """R6: *"consume shared predicates rather than implement three
    interpretations of readiness."*  Asserted structurally, because the property
    is that no second interpretation EXISTS."""

    def test_the_conformance_arm_delegates_rather_than_re_deciding(self):
        body = _code_of(_PLANNER_PATH, "_conformance_violations")
        assert "status_evidence_violations(art, s)" in body, body
        # The two checks it used to make inline now live inside the shared
        # predicate; a copy left behind here is the drift this asserts against.
        assert "has_disposition_attestation" not in body, body
        assert "has_fidelity_signoff" not in body, body
        assert "review_record_violations(art)" not in body, body

    def test_every_new_target_reaches_the_gate_through_one_helper(self):
        gating = _code_of(_PLANNER_PATH, "_gating_preconditions")
        for state in ("revising", "awaiting-decision", "revising-plan",
                      "awaiting-code-review", "revising-code"):
            assert f"_r6_gate(art, '{state}'" in gating, state

    def test_the_closeout_predicate_has_exactly_one_definition(self):
        src = _PLANNER_PATH.read_text(encoding="utf-8")
        assert src.count("def _closeout_violations(") == 1
        assert src.count("def status_evidence_violations(") == 1

    def test_scan_reports_the_shared_predicate_verbatim(self, tmp_path):
        """Not a re-worded summary: `scan`'s output must be the predicate's own
        sentences, or an operator reading `scan` and an operator reading `next`
        are told two different things about one record."""
        art = _plan_art(tmp_path, _pass_block(tier="External"),
                        status="ready-to-archive", stem=_E_STEM,
                        plan_review="required(External)")
        shared = planner.status_evidence_violations(art, "ready-to-archive")
        assert shared
        assert _e_conf(art) == shared


# ===========================================================================
# Chunk P2-R -- plan-readiness inheritance, the two-field shape.
#
# Source contract, in the order it binds:
#   * accepted `dev/proposals/archive/2026-08-10-codex-review-efficient-lifecycle.md`
#     > "Standard-path plan-readiness inheritance";
#   * `dev/plans/review-efficient-lifecycle.md` > `## Maintainer-directed
#     contract revision -- 2026-08-11` (cell **P2-R** + "Required test matrix"),
#     which supersedes the original P2 cell where they conflict; and
#   * that plan's `## Response to plan review -- Claude -- 2026-08-11`
#     Amendments **A**-**D**.
#
# The matrix these nodes discharge, verbatim from the revision, plus the two
# amendments that add to it:
#   1. External proposal `READY` + exact Decision binding + Internal plan review
#      clears, **for both standard and high-assurance fixtures**;
#   2. the same proposal with no Internal plan review refuses;
#   3. an Internal proposal review cannot supply the inherited External basis;
#   4. changed review or accepted-proposal SHA refuses;
#   5. `DISTINCT REVIEW REQUIRED` cannot be satisfied by the Internal plan pass;
#   6. every declared expansion dimension still invalidates readiness;
#   7. [Amendment B] a declared scope REDUCTION refuses, and a Maintainer-recorded
#      `Scope delta` allowance is the only thing that admits it; and
#   8. [Amendment D] a malformed or partially-specified `Inherited proposal basis`
#      -- one sub-field, an unparseable id, or a wrong field name -- refuses and
#      never defaults to `READY`.
#
# **What these nodes deliberately do NOT assert**, because the block does not
# claim it: that `review=` names the commit the External review landed in (no
# repository byte carries it -- see `test_the_p2_block_reaches_no_git`), that the
# Internal pass was performed in a fresh context, or that an UNDECLARED expansion
# or reduction is detected.  The last is the honest limit Amendment B lives with:
# the trigger is an author declaration, exactly as P2's own cell requires of every
# semantic trigger, and `doctrine/dual-review.md` > "The counterweight" already
# says a formal check "would catch forgetting and not evading".
# ===========================================================================

_P2_PROPOSAL_STEM = "2026-08-01-author-p2-source"
_P2_PLAN_STEM = "p2-fixture"
#: Both fixture ids carry hex LETTERS, not only digits, so that the
#: uppercase-refusal node below actually varies something -- a digits-only
#: fixture makes `.upper()` a no-op and the node asserts nothing.
_P2_PROPOSAL_SHA = "1a" * 20     # the reviewed-and-accepted proposal commit
_P2_REVIEW_SHA = "2b" * 20       # the commit the External review landed in


def _p2_tree(tmp_path: Path, *, readiness: str | None = "READY",
             tier: str = "External", reviewed: str | None = _P2_PROPOSAL_SHA,
             assurance: str = "standard",
             extra_reviews: str = "",
             inherited: str | None = None,
             plan_review: str = "required(Internal)",
             plan_header: str = "", plan_body: str = "",
             source_line: str | None = None,
             status: str = "implementing"):
    """A proposal + a plan derived from it, both on disk, parsed -> the plan.

    One helper for both sides because the contract is a *chain*: every node below
    varies exactly one link of it.  `readiness=None` omits the finding,
    `inherited=None` writes the well-formed declaration, `inherited=""` omits it.
    """
    props = tmp_path / "dev" / "proposals"
    plans = tmp_path / "dev" / "plans"
    props.mkdir(parents=True, exist_ok=True)
    plans.mkdir(parents=True, exist_ok=True)
    readiness_line = "" if readiness is None else f"**Plan readiness**: {readiness}\n"
    commit_line = "" if reviewed is None else f"**Reviewed commit**: {reviewed}\n"
    (props / f"{_P2_PROPOSAL_STEM}.md").write_text(
        f"# {_P2_PROPOSAL_STEM}\n\n"
        "**Author**: Author A (Strategy)\n"
        "**Status**: accepted\n"
        f"**Assurance path**: {assurance}\n\n"
        "## Context\n\nx\n\n"
        "## Review -- Reviewer A (External) -- 2026-08-05\n\n"
        f"{commit_line}"
        "**Target**: the complete current contract\n"
        "**Prior findings**: none\n"
        f"**Assurance path**: {assurance}\n"
        f"**Tier**: {tier}\n"
        "**Findings**: none\n"
        f"{readiness_line}\n"
        f"{extra_reviews}"
        "## Decision -- Ada Lovelace (Maintainer) -- 2026-08-06\n\n"
        "**Accepted**.\n\n> Accept as revised.\n",
        encoding="utf-8")
    if inherited is None:
        inherited = (f"**Inherited proposal basis**: review={_P2_REVIEW_SHA}; "
                     f"proposal={_P2_PROPOSAL_SHA}\n")
    source = (f"**Source proposal**: [`src`](../proposals/{_P2_PROPOSAL_STEM}.md)\n"
              if source_line is None else source_line)
    path = plans / f"{_P2_PLAN_STEM}.md"
    path.write_text(
        f"# {_P2_PLAN_STEM}\n\n"
        f"{source}"
        f"**Status**: {status}\n"
        f"**Plan review**: {plan_review}\n"
        f"{inherited}{plan_header}\n"
        f"## Scope\n\nx\n{plan_body}",
        encoding="utf-8")
    return planner._read_artifact(path)


def _p2(tmp_path: Path, **kw) -> list:
    """The one public predicate over the built chain."""
    return planner.plan_inheritance_violations(_p2_tree(tmp_path, **kw))


class TestP2TheChainClears:
    """Matrix 1 -- the positive case, and the mutant guard for every refusal."""

    @pytest.mark.parametrize("assurance", ["standard", "high-assurance"])
    def test_external_ready_plus_exact_binding_clears_on_both_paths(
            self, tmp_path, assurance):
        """**Both fixtures, and the high-assurance one is the Maintainer's
        decision made executable.**  The original P2 cell required a
        high-assurance REFUSAL; the 2026-08-11 revision removed it in the
        Maintainer's quoted words -- *"Standard and high-assurance proposals may
        both receive `READY` when their External review settled the complete
        contract."*  So this node is red against the pre-revision contract by
        construction, which is the point: re-adding the assurance branch reddens
        it."""
        assert _p2(tmp_path, assurance=assurance) == []

    def test_a_plan_declaring_no_inheritance_is_silent(self, tmp_path):
        """Blast radius.  Every plan in this tree is this plan."""
        assert _p2(tmp_path, inherited="") == []

    def test_a_proposal_is_never_an_inherited_plan(self, tmp_path):
        art = _prop_art(tmp_path, extra_header=_P5_DECLARATION + "\n")
        assert planner.plan_inheritance_violations(art) == []

    def test_the_folded_declaration_parses(self, tmp_path):
        """The revision's own rendering of the field WRAPS, putting `proposal=`
        on an indented second line.  A reviewer who copies that block verbatim
        must not be refused by the tool that quotes it."""
        folded = (f"**Inherited proposal basis**: review={_P2_REVIEW_SHA};\n"
                  f"    proposal={_P2_PROPOSAL_SHA}\n")
        assert _p2(tmp_path, inherited=folded) == []

    @pytest.mark.parametrize("spelling", [
        "**Inherited proposal basis**", "Inherited proposal basis",
        "__Inherited proposal basis__",
    ])
    def test_every_emphasis_spelling_is_the_same_field(self, tmp_path, spelling):
        line = (f"{spelling}: review={_P2_REVIEW_SHA}; "
                f"proposal={_P2_PROPOSAL_SHA}\n")
        assert _p2(tmp_path, inherited=line) == []


class TestP2TheReadinessFinding:
    """Matrix 3 and 5 -- whose finding may be inherited, and which value."""

    def test_distinct_review_required_refuses(self, tmp_path):
        """Matrix 5.  *"`DISTINCT REVIEW REQUIRED` still requires a separate plan
        review at the tier named by the proposal/Decision."*  A fresh-context
        Internal pass does not satisfy it, so the plan refuses even though it
        carries one."""
        v = _p2(tmp_path, readiness="DISTINCT REVIEW REQUIRED")
        assert any("DISTINCT REVIEW REQUIRED" in m and "cannot inherit" in m
                   for m in v), v

    def test_an_internal_proposal_review_cannot_supply_the_basis(self, tmp_path):
        """Matrix 3.  What inheritance *spends* is the different-agent-type read;
        an Internal proposal review has none to spend."""
        v = _p2(tmp_path, tier="Internal")
        assert any("only an External proposal review" in m for m in v), v

    def test_an_absent_finding_is_not_ready(self, tmp_path):
        v = _p2(tmp_path, readiness=None)
        assert any("records no 'Plan readiness:'" in m for m in v), v
        assert any("never defaults to 'READY'" in m for m in v), v

    @pytest.mark.parametrize("value", [
        "ready", "READY-ish", "PROBABLY", "",
        "READY but actually DISTINCT REVIEW REQUIRED",
    ])
    def test_an_unreadable_finding_refuses_and_never_defaults(
            self, tmp_path, value):
        """`ready` lowercase is admitted (case-insensitive, like every other
        closed field here) -- the rest are not, and an empty value is in the list
        on purpose: a bare `Plan readiness:` is the shape a half-written record
        has, and reading it as `READY` would invert the contract."""
        v = _p2(tmp_path, readiness=value)
        if value == "ready":
            assert v == []
        else:
            assert v, value

    def test_the_latest_declaring_review_is_operative(self, tmp_path):
        """A later review supersedes an earlier one, so an early `READY` cannot
        be resurrected after a later pass withdrew readiness.  The parent:
        *"A later review does not silently inherit an earlier"* basis."""
        later = (
            "## Review -- Reviewer B (External) -- 2026-08-07\n\n"
            f"**Reviewed commit**: {_P2_PROPOSAL_SHA}\n"
            "**Target**: the complete current contract\n"
            "**Prior findings**: none\n"
            "**Assurance path**: standard\n"
            "**Tier**: External\n"
            "**Findings**: none\n"
            "**Plan readiness**: DISTINCT REVIEW REQUIRED\n\n")
        v = _p2(tmp_path, extra_reviews=later)
        assert any("DISTINCT REVIEW REQUIRED" in m for m in v), v

    def test_a_duplicate_finding_in_one_record_refuses(self, tmp_path):
        v = _p2(tmp_path, readiness="READY\n**Plan readiness**: READY")
        assert any("2 times" in m or "duplicate" in m for m in v), v


class TestP2TheExactBinding:
    """Matrix 4 -- and the honest boundary of what "exact" can mean here."""

    def test_a_changed_accepted_proposal_sha_refuses(self, tmp_path):
        """The mechanical half of matrix 4.  `proposal=` must equal the
        `Reviewed commit:` of the review that recorded `READY`: the Decision
        *"binds the same proposal commit without changing its contract"*, so a
        mismatch means the plan inherits readiness for bytes nobody declared
        ready."""
        v = _p2(tmp_path, reviewed="9" * 40)
        assert any("must name the EXACT proposal commit" in m for m in v), v

    def test_the_review_sha_is_shape_checked_not_identified(self, tmp_path):
        """**The residual, asserted as behavior rather than left in prose.**  A
        DIFFERENT well-formed `review=` clears, because no repository byte says
        which commit a review landed in -- a commit cannot contain its own id.
        This node exists so a later reader cannot mistake the silence for a check
        that ran; closing it needs either git (rejected: silent degradation) or a
        new record that carries the review's own commit."""
        other = (f"**Inherited proposal basis**: review={'7' * 40}; "
                 f"proposal={_P2_PROPOSAL_SHA}\n")
        assert _p2(tmp_path, inherited=other) == []

    def test_the_two_bindings_must_be_distinct(self, tmp_path):
        """The one exactness property `review=` DOES carry: a review lands after
        the commit it reviews, so one commit cannot be both."""
        same = (f"**Inherited proposal basis**: review={_P2_PROPOSAL_SHA}; "
                f"proposal={_P2_PROPOSAL_SHA}\n")
        v = _p2(tmp_path, inherited=same)
        assert any("SAME commit" in m for m in v), v

    def test_a_review_record_with_no_readable_reviewed_commit_refuses(
            self, tmp_path):
        v = _p2(tmp_path, reviewed=None)
        assert v, "an unbindable readiness record must not clear"


class TestP2AmendmentDMalformedNeverMeansReady:
    """Matrix 8 -- every shape Amendment D names, in its own words."""

    @pytest.mark.parametrize("value", [
        "review=" + _P2_REVIEW_SHA,                    # only one sub-field
        "proposal=" + _P2_PROPOSAL_SHA,                # only the other
        "review=zzz; proposal=" + _P2_PROPOSAL_SHA,    # unparseable id
        "review=" + _P2_REVIEW_SHA + "; proposal=abc1234",   # abbreviated id
        # UPPERCASE hex: git emits lowercase, and `_FULL_COMMIT_RE` is lowercase
        # for the reason the file's other commit pattern is.  Spelled with a hex
        # LETTER on purpose -- `_P2_REVIEW_SHA.upper()` would be a no-op, since
        # the fixture sha is all digits, and the node would silently assert
        # nothing.
        "review=" + _P2_REVIEW_SHA + "; proposal=" + _P2_PROPOSAL_SHA.upper(),
        "",                                            # present but empty
        "garbage",                                     # names no binding
        "see the proposal; review=" + _P2_REVIEW_SHA
        + "; proposal=" + _P2_PROPOSAL_SHA,            # text before the first
        "review=" + _P2_REVIEW_SHA + "; review=" + _P2_REVIEW_SHA
        + "; proposal=" + _P2_PROPOSAL_SHA,            # duplicate binding
    ])
    def test_a_malformed_declaration_refuses(self, tmp_path, value):
        v = _p2(tmp_path, inherited=f"**Inherited proposal basis**: {value}\n")
        assert v, value
        assert all("never defaults to 'READY'" in m for m in v), v

    def test_a_duplicate_declaration_refuses(self, tmp_path):
        line = (f"**Inherited proposal basis**: review={_P2_REVIEW_SHA}; "
                f"proposal={_P2_PROPOSAL_SHA}\n")
        v = _p2(tmp_path, inherited=line + line)
        assert any("duplicate" in m for m in v), v

    @pytest.mark.parametrize("label", [
        "Inherited basis", "Inherited proposal", "inherited proposal basis",
        "Inherited-proposal-basis",
    ])
    def test_a_wrong_field_name_refuses_rather_than_declaring_nothing(
            self, tmp_path, label):
        """Amendment D's third shape, and the one that needed a *detector*: a
        near-miss field name is silent by construction, because a plan that fails
        to declare inheritance simply is not an inherited plan.  Detected the way
        S8 detects a near-miss review heading -- recognize the neighbourhood, then
        quote the line that did not count."""
        line = (f"**{label}**: review={_P2_REVIEW_SHA}; "
                f"proposal={_P2_PROPOSAL_SHA}\n")
        v = _p2(tmp_path, inherited=line)
        assert any("near miss" in m for m in v), (label, v)

    def test_an_unrelated_header_field_is_not_a_near_miss(self, tmp_path):
        """The false-refusal direction of the node above."""
        assert _p2(tmp_path, inherited="",
                   plan_header="**Blocked by**: nothing\n") == []

    def test_the_retired_parent_spelling_refuses(self, tmp_path):
        """P5 filed this gap at P2-R by name.  It is a live bypass, not a
        tidiness item: the plan-review floor is evaluated only for a value
        beginning `required`, so the accepted parent's own wording bought a plan
        NO plan-review obligation at all."""
        v = _p2(tmp_path, inherited="",
                plan_review=f"inherited({_P2_REVIEW_SHA}; "
                            f"proposal={_P2_PROPOSAL_SHA})")
        assert any("RETIRED spelling" in m for m in v), v

    def test_inheritance_cannot_buy_no_plan_review(self, tmp_path):
        """`not required(...)` beside an inheritance declaration is the one
        combination that would leave a plan with no independent read.
        Inheritance REALLOCATES the plan review; it does not remove it."""
        v = _p2(tmp_path, plan_review="not required(doc-only)")
        assert any("REALLOCATES" in m for m in v), v


class TestP2TheSourceProposalChain:
    """The chain out to the proposal, every link of which refuses when broken."""

    @pytest.mark.parametrize("line,expect", [
        ("", "no '**Source proposal**:' line"),
        ("**Source proposal**: `some-bare-stem`\n", "names no '<stem>.md' file"),
        ("**Source proposal**: ../proposals/no-such-file.md\n",
         "in neither 'dev/proposals/'"),
    ])
    def test_an_unresolvable_pointer_refuses(self, tmp_path, line, expect):
        v = _p2(tmp_path, source_line=line)
        assert any(expect in m for m in v), (line, v)

    def test_a_duplicate_pointer_refuses(self, tmp_path):
        one = f"**Source proposal**: [`s`](../proposals/{_P2_PROPOSAL_STEM}.md)\n"
        v = _p2(tmp_path, source_line=one + one)
        assert any("duplicate '**Source proposal**:'" in m for m in v), v

    def test_an_archived_proposal_resolves(self, tmp_path):
        """The normal case in this tree: a plan's proposal is archived by the
        time the plan executes, so both locations are searched."""
        art = _p2_tree(tmp_path)
        props = tmp_path / "dev" / "proposals"
        archive = props / "archive"
        archive.mkdir(parents=True, exist_ok=True)
        (props / f"{_P2_PROPOSAL_STEM}.md").rename(
            archive / f"{_P2_PROPOSAL_STEM}.md")
        assert planner.plan_inheritance_violations(
            planner._read_artifact(art.path)) == []

    def test_a_symlinked_proposal_refuses(self, tmp_path):
        art = _p2_tree(tmp_path)
        props = tmp_path / "dev" / "proposals"
        real = props / "elsewhere.md"
        (props / f"{_P2_PROPOSAL_STEM}.md").rename(real)
        (props / f"{_P2_PROPOSAL_STEM}.md").symlink_to(real)
        v = planner.plan_inheritance_violations(planner._read_artifact(art.path))
        assert any("symlink" in m for m in v), v


class TestP2ExpansionInvalidatesReadiness:
    """Matrix 6 -- every dimension the accepted parent names."""

    @pytest.mark.parametrize("dimension", [
        "scope item", "invariant", "public path", "failure disposition",
        "trust boundary", "ceremony",
    ])
    def test_every_declared_expansion_dimension_refuses(self, tmp_path, dimension):
        v = _p2(tmp_path,
                plan_header=f"**Contract expansion**: {dimension}\n")
        assert any("INVALIDATES inheritance" in m for m in v), (dimension, v)

    def test_the_dimension_list_is_the_parents_six(self):
        """Pinned against the accepted text, so a later edit that quietly drops
        a dimension is a failing node rather than a narrower gate."""
        assert planner._EXPANSION_DIMENSIONS == (
            "scope item", "invariant", "public path", "failure disposition",
            "trust boundary", "ceremony")

    def test_a_declared_none_clears(self, tmp_path):
        assert _p2(tmp_path, plan_header="**Contract expansion**: none\n") == []

    def test_several_dimensions_in_one_declaration_refuse(self, tmp_path):
        v = _p2(tmp_path,
                plan_header="**Contract expansion**: invariant; public path\n")
        assert any("invariant; public path" in m for m in v), v

    def test_a_dimension_with_a_trailing_explanation_still_refuses(self, tmp_path):
        v = _p2(tmp_path,
                plan_header="**Contract expansion**: ceremony -- a second "
                            "re-anchor\n")
        assert any("INVALIDATES inheritance" in m for m in v), v

    @pytest.mark.parametrize("value", ["vibes", "", "scope item; vibes"])
    def test_an_unreadable_expansion_declaration_refuses(self, tmp_path, value):
        """Present-but-unreadable is the one shape that must not buy silence."""
        v = _p2(tmp_path, plan_header=f"**Contract expansion**: {value}\n")
        assert v, value

    def test_a_duplicate_expansion_declaration_refuses(self, tmp_path):
        v = _p2(tmp_path, plan_header="**Contract expansion**: none\n"
                                      "**Contract expansion**: none\n")
        assert any("duplicate" in m for m in v), v

    def test_the_declaration_is_header_bounded(self, tmp_path):
        """Not tidiness, and the fixture shape is what makes it a falsifier.

        The field matcher is full-line anchored, so a mention *inside* a sentence
        was never a candidate -- quoting one would have tested nothing.  The real
        hazard is a line-start restatement inside an appended section, which is
        exactly how P5's identical bound became load-bearing: the plan that
        specifies these fields quotes one at line start in an appended revision
        section, and a whole-text read would make that plan declare an expansion
        about itself.  So the fixture puts a conforming field line in the BODY."""
        assert _p2(tmp_path,
                   plan_body="\n## Response to plan review -- A -- 2026-08-08\n\n"
                             "**Contract expansion**: invariant\n") == []


class TestP2AmendmentBScopeReduction:
    """Matrix 7 -- the seventh trigger, in the vocabulary that already exists."""

    _SHARPENING = "\n### Sharpening -- Author A -- 2026-08-07\n\n"

    @pytest.mark.parametrize("value", ["degraded", "lost"])
    def test_a_declared_reduction_with_no_allowance_refuses(self, tmp_path, value):
        """The asymmetry Amendment B closes.  The parent's six all guard a
        translation that ADDS; this one guards the direction an Internal
        reviewer's own charter ("it does not reopen the accepted design") makes
        invisible -- a quiet narrowing reading as faithful translation."""
        v = _p2(tmp_path,
                plan_body=self._SHARPENING + f"**Scope delta**: {value}\n")
        assert any("accepted scope is a FLOOR" in m for m in v), (value, v)

    @pytest.mark.parametrize("value", ["degraded", "lost"])
    def test_a_maintainer_recorded_allowance_admits_it(self, tmp_path, value):
        """*"a recorded `Scope delta` allowance is the only thing that admits
        it."*  Recorded the way every other Maintainer authority in this file is:
        a visually-isolated verbatim blockquote, through the identical predicate a
        `## Decision` uses.  Structure only -- the committing operator remains the
        guarantor that the words were said (R1)."""
        assert _p2(tmp_path,
                   plan_body=self._SHARPENING + f"**Scope delta**: {value}\n\n"
                             "> Drop chunk F; file the remainder.\n") == []

    def test_the_allowance_must_sit_in_the_DECLARING_record(self, tmp_path):
        """A blockquote somewhere else in the plan is not an allowance for this
        reduction -- otherwise any quoted authorization anywhere would admit
        every later cut."""
        body = ("\n### Something else -- Author A -- 2026-08-06\n\n"
                "> An authorization about an unrelated thing.\n"
                + self._SHARPENING + "**Scope delta**: lost\n")
        v = _p2(tmp_path, plan_body=body)
        assert any("no Maintainer allowance in that record" in m for m in v), v

    def test_preserved_owes_nothing(self, tmp_path):
        """*"preserved -- every baseline outcome is still delivered.  No
        declaration, no allowance, nothing owed."*"""
        assert _p2(tmp_path,
                   plan_body=self._SHARPENING
                             + "**Scope delta**: preserved\n") == []

    def test_the_templates_unfilled_prompt_is_inert(self, tmp_path):
        """Both authoring templates and both planner scaffolds print
        `**Scope delta**: preserved | degraded | lost` as a PROMPT.  A scaffolded
        plan carrying the unfilled line must not refuse -- and
        `doctrine/dual-review.md` > "The counterweight" is explicit that no tool
        refuses on a missing or malformed declaration."""
        assert _p2(tmp_path,
                   plan_body=self._SHARPENING
                             + "**Scope delta**: preserved | degraded | lost\n"
                   ) == []

    def test_an_absent_declaration_is_silent_and_that_is_the_honest_limit(
            self, tmp_path):
        """**The residual, asserted as behavior.**  A plan that quietly drops an
        accepted outcome and declares nothing is INVISIBLE here.  That is not a
        defect in this node -- it is the reach of an author-declared trigger, and
        the reason `AGENTS.md` and `doctrine/dual-review.md` both put the
        enforcement in review.  Recorded so nobody reads the silence as a check
        that ran."""
        assert _p2(tmp_path, plan_body="\n## Chunks\n\n(one chunk, quietly "
                                       "dropping an accepted outcome)\n") == []


class TestP2TheInternalPlanReviewIsStillRequired:
    """Matrix 2 -- inheritance reallocates the read; it does not remove it."""

    def test_no_conforming_internal_pass_refuses_at_an_implementing_state(
            self, tmp_path):
        art = _p2_tree(tmp_path, status="implementing")
        v = planner.status_evidence_violations(art, "implementing")
        assert any("no conforming pass satisfies it" in m for m in v), v

    def test_a_conforming_internal_pass_clears_the_floor(self, tmp_path):
        art = _p2_tree(tmp_path, status="implementing",
                       plan_body="\n" + _pass_block(tier="Internal"))
        assert planner.status_evidence_violations(art, "implementing") == []
        assert planner.plan_inheritance_violations(art) == []

    def test_an_external_pass_also_satisfies_the_internal_floor(self, tmp_path):
        """Tiers are non-cumulative and `External >= Internal`; inheritance does
        not forbid a stronger read than the default allocates."""
        art = _p2_tree(tmp_path, status="implementing",
                       plan_review="required(External)",
                       plan_body="\n" + _pass_block(tier="External"))
        assert planner.status_evidence_violations(art, "implementing") == []
        assert planner.plan_inheritance_violations(art) == []


class TestP2BothGateSurfacesAgree:
    """S12 -- one predicate, two call sites, verbatim."""

    def test_scan_and_next_report_the_same_finding(self, tmp_path):
        identity = planner.IdentityModel(frozenset(), frozenset())
        art = _p2_tree(tmp_path, readiness="DISTINCT REVIEW REQUIRED",
                       status="ready-to-implement")
        expected = planner.plan_inheritance_violations(art)
        assert expected
        reported = planner._conformance_violations(art, identity)
        for msg in expected:
            assert msg in reported, (msg, reported)
        gates = planner._gating_preconditions(art, "implementing", identity)
        chain = [g for g in gates
                 if "the inherited proposal basis binds" in g[1]]
        assert len(chain) == 1, gates
        met, desc = chain[0]
        assert met is False
        for msg in expected:
            assert msg in desc

    def test_no_inheritance_gate_is_offered_for_a_non_inherited_plan(
            self, tmp_path):
        identity = planner.IdentityModel(frozenset(), frozenset())
        art = _p2_tree(tmp_path, inherited="", status="ready-to-implement")
        gates = planner._gating_preconditions(art, "implementing", identity)
        assert not [g for g in gates
                    if "the inherited proposal basis binds" in g[1]]

    def test_the_proposal_side_shape_reaches_both_surfaces(self, tmp_path):
        identity = planner.IdentityModel(frozenset(), frozenset())
        art = _prop_art(
            tmp_path,
            _prop_review(trailer="**Plan readiness**: PROBABLY\n"),
            status="awaiting-decision")
        expected = planner.plan_readiness_violations(art)
        assert expected
        assert all(m in planner._conformance_violations(art, identity)
                   for m in expected)
        gates = planner._gating_preconditions(art, "accepted", identity)
        assert any(not met and any(m in desc for m in expected)
                   for met, desc in gates), gates


class TestP2LiveCorpusAndSourceFences:
    """The measured blast radius, and the fences that keep it that way."""

    def test_the_live_corpus_is_sound_under_the_p2_contract(self):
        """Zero of the tree's artifacts declare inheritance, so P2 adds zero
        findings.  Measured here rather than asserted in prose: when the first
        real inherited plan lands, this node is where its chain is checked."""
        offenders = {}
        for fam in ("plans", "plans/archive", "proposals", "proposals/archive"):
            base = CAIRN_ROOT / "dev" / fam
            if not base.is_dir():
                continue
            for path in sorted(base.glob("*.md")):
                if path.name in ("_template.md", "README.md"):
                    continue
                art = planner._read_artifact(path)
                found = (planner.plan_inheritance_violations(art)
                         + planner.plan_readiness_violations(art))
                if found:
                    offenders[path.name] = found
        assert offenders == {}, offenders

    def test_the_p2_block_reaches_no_git(self):
        """The fence the block's own docstring promises.  P2 legitimately reads
        ONE other artifact -- the source proposal, through `_read_artifact` --
        because that chain is what the accepted parent asks for.  It reaches no
        git, no subprocess and no raw `read_text`, so the `review=` residual
        cannot be closed by an edit that nobody reviews."""
        src = _PLANNER_PATH.read_text(encoding="utf-8")
        start = src.index("# === P2-R -- plan-readiness inheritance")
        end = src.index("def review_record_violations(")
        block = src[start:end]
        for forbidden in ("_git_readonly", "subprocess", "_repo_root", "Popen",
                          "read_text", "write_text", "open("):
            assert forbidden not in block, forbidden
        assert "_read_artifact(" in block, (
            "the chain must resolve through the planner's own reader")

    def test_one_binding_shape_rule_serves_both_fields(self):
        """P5's `Basis:` line and P2's `Inherited proposal basis` are the same
        grammar, so there is ONE implementation with the keys as a parameter --
        the shape `_is_legacy` already uses for its three manifests.  A sibling
        copy would put two implementations of one rule in the file."""
        src = _PLANNER_PATH.read_text(encoding="utf-8")
        assert src.count("def _basis_binding_violations(") == 1
        assert src.count("def _basis_value(") == 1

    def test_the_p5_default_messages_are_unchanged_by_that_refactor(self):
        """The guard on the generalization: P5's three-binding messages must read
        exactly as they did before the keys became a parameter, or the refactor
        silently rewrote a landed contract's refusals."""
        v = planner._basis_binding_violations("nothing here", "L")
        assert v == ["L: 'Basis: nothing here' names none of the three required "
                     "bindings (proposal=, plan=, changed-paths=)"]
        v = planner._basis_binding_violations("proposal=" + "a" * 40, "L")
        assert any("all three are required" in m for m in v), v


class TestP2CarriedForwardObligationCF1:
    """[CF1] -- the plan-side assurance path the monitoring report needs."""

    def test_the_vocabulary_is_public_and_unchanged(self):
        """P6a's record: closing the split *"needs a **public** single source for
        the assurance-path vocabulary -- `tools/lifecycle_planner.py` declares it
        privately today, and a second declaration in the CLI would fork a
        vocabulary."*  Published without changing a value."""
        assert planner.ASSURANCE_PATHS == ("standard", "high-assurance")
        assert not hasattr(planner, "_ASSURANCE_PATHS")
        assert planner.ASSURANCE_NOT_INHERITED == "not-inherited"
        assert planner.ASSURANCE_NOT_INHERITED not in planner.ASSURANCE_PATHS

    @pytest.mark.parametrize("assurance", ["standard", "high-assurance"])
    def test_the_chain_resolves_the_proposals_declaration(self, tmp_path,
                                                          assurance):
        art = _p2_tree(tmp_path, assurance=assurance)
        assert planner.resolve_plan_assurance_path(art.path) == (assurance, [])

    def test_a_plan_declaring_no_inheritance_resolves_to_not_inherited(
            self, tmp_path):
        """A POSITIVE answer, not a default: the plan declares no chain, so there
        is no proposal declaration to inherit.  A plan carries no artifact-level
        assurance path of its own -- P1 pinned that absence deliberately."""
        art = _p2_tree(tmp_path, inherited="")
        assert planner.resolve_plan_assurance_path(art.path) == (
            planner.ASSURANCE_NOT_INHERITED, [])

    def test_a_broken_chain_yields_no_value_and_the_reasons(self, tmp_path):
        art = _p2_tree(tmp_path, readiness="DISTINCT REVIEW REQUIRED")
        value, problems = planner.resolve_plan_assurance_path(art.path)
        assert value is None
        assert problems

    def test_a_proposal_with_no_declaration_yields_no_value(self, tmp_path):
        art = _p2_tree(tmp_path)
        proposal = tmp_path / "dev" / "proposals" / f"{_P2_PROPOSAL_STEM}.md"
        proposal.write_text(
            proposal.read_text(encoding="utf-8").replace(
                "**Assurance path**: standard\n\n## Context", "\n## Context", 1),
            encoding="utf-8")
        value, problems = planner.resolve_plan_assurance_path(art.path)
        assert value is None
        assert any("no default" in m for m in problems), problems

    def test_a_proposal_is_not_a_plan(self, tmp_path):
        art = _prop_art(tmp_path)
        value, problems = planner.resolve_plan_assurance_path(art.path)
        assert value is None
        assert any("is not a plan" in m for m in problems), problems


class TestP2AuthoringTemplates:
    """P2's template half, pinned per surface in P1's idiom.

    The plan's acceptance criteria require each documentation surface to be
    *confirmed* updated ("drift gates catch drift, not absence"), and the reason
    is sharper for this chunk than for most: every refusal P2 adds is one an
    author can only avoid by knowing a grammar, and an author refused by a gate
    who finds no instruction in the template has been handed a puzzle instead of
    a rule.

    **Both sides of every pair.**  Chunk B of `scope-reduction-trap` edited a
    shipped source and not its installed twin, leaving unsound text live in the
    copy Cairn itself reads -- checking one side is how that happens.
    """

    SURFACES = {
        "dev/proposals/_template.md": {
            "the readiness field": "**Plan readiness**: READY | DISTINCT REVIEW "
                                   "REQUIRED",
            "it is optional and has no default": "it has no default",
            "distinct is a finding": "is a finding, not a fallback",
            "only External may supply it": "Only an External pass may supply it",
            # Needles are chosen to sit inside ONE physical line: the templates
            # are hard-wrapped, so a phrase that reads continuously on the page
            # can still straddle a newline, and a straddling needle would fail
            # for a formatting reason rather than a contract one.
            "assurance does not decide it": "does *not* decide this",
        },
        "dev/plans/_template.md": {
            "the two-field shape": "**Inherited proposal basis**: review=",
            "paired with an Internal floor": "**Plan review**: required(Internal)",
            "which commit proposal= names":
                "the proposal commit the Decision binds",
            "full ids only": "full 40-character",
            "reallocates rather than removes":
                "reallocates the plan review; it never",
            "the expansion declaration": "**Contract expansion**: none |",
            "the seventh trigger": "a **scope reduction** relative to the",
            "declarations are not inferences": "author declarations",
        },
    }

    @pytest.mark.parametrize("rel", sorted(SURFACES))
    @pytest.mark.parametrize("shipped", [False, True])
    def test_each_surface_carries_the_contract(self, rel, shipped):
        path = CAIRN_ROOT / (f"templates/core/{rel}" if shipped else rel)
        text = path.read_text(encoding="utf-8")
        missing = [name for name, needle in self.SURFACES[rel].items()
                   if needle not in text]
        assert not missing, (path, missing)

    def test_the_doctrine_teaches_the_record_and_names_its_limits(self):
        """`doctrine/dual-review.md` is P2's cell's own third surface.  The limits
        are asserted alongside the mechanism on purpose: a doctrine section that
        taught the record without naming what a checker cannot reach would invite
        exactly the over-reading `AGENTS.md` > *Verifying claims* warns about."""
        text = (CAIRN_ROOT / "doctrine/dual-review.md").read_text(encoding="utf-8")
        for needle in (
                "## Plan-readiness inheritance",
                "Plan readiness: READY | DISTINCT REVIEW REQUIRED",
                "Inherited proposal basis: review=",
                "is a finding,\nnot a default",
                "### What invalidates readiness",
                "Assurance path does not decide plan-review independence",
                "which commit a review landed in",
                "whether the Internal pass was fresh-context"):
            assert needle in text, needle

    def test_the_plan_template_placeholder_still_cannot_satisfy_the_gate(self):
        """P2 adds text near `## Plan review` in the plan template.  A stray
        `**Model**:` line or a dated reviewer heading would make the shipped
        placeholder satisfy the archive precondition -- the exact defect
        `archive-precondition-substance` closed."""
        for rel in ("dev/plans/_template.md",
                    "templates/core/dev/plans/_template.md"):
            text = (CAIRN_ROOT / rel).read_text(encoding="utf-8")
            assert planner._has_code_review_marker(text) is False, rel

    def test_the_scaffolded_plan_template_declares_no_inheritance(self):
        """The template teaches the field by QUOTING it, so the quoted grammar
        must not make a scaffolded plan an inherited one.  The declaration is
        header-bounded and the template's examples are indented inside prose --
        this node is what keeps that true as the template is edited."""
        for rel in ("dev/plans/_template.md",
                    "templates/core/dev/plans/_template.md"):
            path = CAIRN_ROOT / rel
            assert "Inherited proposal basis" in path.read_text(encoding="utf-8")
            art = planner.Artifact(path, "plan",
                                   path.read_text(encoding="utf-8"))
            assert planner._declares_inheritance(art) is False, rel


# ---------------------------------------------------------------------------
# Chunk P3 -- the complete current contract and its withdrawal ledger.
#
# Contract, verbatim from the accepted `review-efficient-lifecycle` parent,
# "Bounded current contracts" (Revision 1 -- the operative revision; the archived
# proposal carries no later `R*` section that replaces it):
#
#     After a proposal review Response, the author appends one complete current
#     contract containing scope, exclusions, invariants, failure dispositions,
#     public paths, evidence, omissions, deferred work, and the heading below:
#
#         ### Withdrawn / superseded commitments
#         * <earlier commitment, replacement or withdrawal, and reason>
#
#     The heading is mandatory even when its value is `None`.  A reviewer compares
#     the complete revision to the previously reviewed contract and verifies this
#     ledger.  The newest reviewed complete revision is operative for Decision and
#     implementation; all earlier sections remain immutable history.
#
# WHY THESE FIXTURES ARE SYNTHETIC, AND WHY THAT IS THE POINT.  Measured at this
# chunk's implementation parent: 53 proposals in this tree carry a `## Response`
# or a revision section, exactly **one** carries the ledger, and **all 52 that do
# not are already immutable** -- so the live trigger set is EMPTY.  A rule whose
# trigger set is empty is indistinguishable from a rule that does nothing: the
# silent-tool defect `AGENTS.md` > *Verifying claims* names ("a tool that returns
# success without testing the claimed property is a worse defect than no tool,
# because it is silent").  "No corpus proposal triggers it and the suite is green"
# is therefore not evidence here.  Every refusal direction below is exercised
# against a synthetic proposal that DOES carry a Response, plus two nodes that
# hold the emptiness itself: `test_the_live_corpus_owes_no_ledger_today` reddens
# the day a real proposal first triggers, and
# `test_every_pre_ledger_proposal_is_covered_by_immutability_alone` re-derives the
# claim that no legacy manifest is needed instead of trusting it.
#
# Each node carries a single-property falsifier -- a mutation applied to
# `templates/skills/_lib/lifecycle_planner.py`, the copy this module LOADS, then
# reverted -- recorded in the plan's implementation-verification section rather
# than asserted here.  The only thing that runs these nodes is a person typing
# `python -m pytest bootstrap/tests`; Cairn has no CI.
# ---------------------------------------------------------------------------

_P3_LEDGER = "### Withdrawn / superseded commitments"
_P3_ENTRY = "* the earlier six-plan pilot -- superseded by six-or-60-days; reason"
_P3_REVISION = "## Revised proposal -- Revision 2"
_P3_RESPONSE = "## Response -- Author A (Strategy) -- 2026-08-11"


def _p3_prop(tmp_path: Path, body: str, *, status: str = "revised",
             stem: str = "p3-fixture", archived: bool = False):
    """A live proposal carrying *body* below its header -> the parsed artifact.

    `archived=True` puts it under `dev/proposals/archive/` instead, which is the
    other half of `_is_immutable` and is exercised as such.
    """
    base = tmp_path / "dev" / "proposals"
    if archived:
        base = base / "archive"
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{stem}.md"
    path.write_text(
        f"# {stem}\n\n"
        "**Author**: Author A (Strategy)\n"
        f"**Status**: {status}\n"
        "**Assurance path**: standard\n\n"
        "## Context\n\nWhy.\n\n"
        f"{body}",
        encoding="utf-8")
    return planner._read_artifact(path)


def _p3_body(*, response: str | None = _P3_RESPONSE,
             revision: str | None = _P3_REVISION,
             ledger: str | None = _P3_LEDGER,
             value: str | None = _P3_ENTRY,
             revision_first: bool = False,
             trailer: str = "") -> str:
    """One Response + one revision + its ledger, each part independently removable.

    Every refusal node below varies exactly one of them, so no node can pass for
    a reason a sibling node's fixture happens to supply.
    """
    resp = "" if response is None else f"{response}\n\n**[R1]** accept.\n\n"
    rev = ""
    if revision is not None:
        rev = f"{revision}\n\nThe complete current contract.\n\n"
        if ledger is not None:
            rev += f"{ledger}\n\n"
            if value is not None:
                rev += f"{value}\n\n"
    parts = (rev, resp) if revision_first else (resp, rev)
    return "".join(parts) + trailer


def _p3(tmp_path: Path, **kw) -> list:
    """The one public predicate, over a body built by `_p3_body`."""
    prop_kw = {k: kw.pop(k) for k in ("status", "stem", "archived")
               if k in kw}
    return planner.current_contract_violations(
        _p3_prop(tmp_path, _p3_body(**kw), **prop_kw))


class TestP3TheContractClears:
    """The positive cases -- and the mutant guard for every refusal below."""

    def test_a_response_with_a_complete_revision_and_a_ledger_clears(
            self, tmp_path):
        """The guard that catches a predicate which always violates.  If this
        node ever fails, no refusal node below is evidence of anything."""
        assert _p3(tmp_path) == []

    @pytest.mark.parametrize("value", [
        "* None", "* none", "None", "none.", "* **None** -- nothing withdrawn.",
    ])
    def test_a_ledger_whose_value_is_none_clears(self, tmp_path, value):
        """*"The heading is mandatory even when its value is `None`."*  Written
        `None` is the whole point: it distinguishes "nothing was withdrawn" from
        "nobody checked", so the spellings an author actually reaches for all
        clear."""
        assert _p3(tmp_path, value=value) == []

    def test_a_revision_placed_ABOVE_its_response_clears(self, tmp_path):
        """Order-agnostic, and this is a measured restraint rather than laziness.
        The proposal template's own long-standing instruction was *"write a short
        '## Revised proposal' section above this"*, 6 archived proposals follow it,
        and the accepted contract fixes no order.  A position rule here would
        refuse correct records for a reason no contract states."""
        assert _p3(tmp_path, revision_first=True) == []

    @pytest.mark.parametrize("heading", [
        "## Response -- Author A -- 2026-08-11",
        "## Response — Author A (author) — 2026-08-11",
        "## Response to review -- Author A -- 2026-08-11",
        "## Response to the External security review -- A -- 2026-08-11",
        "## Response and revision -- Author A (author) -- 2026-08-11",
        "## Response + Revised proposal (Round 4) -- Author A -- 2026-08-11",
    ])
    def test_every_live_response_spelling_is_the_same_record(
            self, tmp_path, heading):
        """All six shapes are real corpus headings, including the em-dash
        separator and the two COMBINED forms that are a Response and a revision in
        one section.  Matching is on the normalized heading text, so an em-dash is
        not a contract difference -- and the combined forms satisfy the revision
        obligation from the same line, which is why they are here rather than in
        the refusal class."""
        combined = "revis" in heading.lower()
        assert _p3(tmp_path, response=heading,
                   revision=None if combined else _P3_REVISION,
                   ledger=None if combined else _P3_LEDGER,
                   trailer=(f"{_P3_LEDGER}\n\n{_P3_ENTRY}\n" if combined else "")
                   ) == []

    @pytest.mark.parametrize("spelling", [
        "### Withdrawn / superseded commitments",
        "### Withdrawn/superseded commitments",
        "###   Withdrawn  /  superseded   commitments",
        "### **Withdrawn / superseded commitments**",
        "### withdrawn / superseded commitments",
    ])
    def test_formatting_variation_in_the_heading_is_tolerated(
            self, tmp_path, spelling):
        """Tolerant on FORMATTING, strict on WORDS and LEVEL.  Slash spacing,
        emphasis, run-together whitespace and case are not contract differences;
        refusing them would be this checker inventing a house style."""
        assert _p3(tmp_path, ledger=spelling) == []

    def test_a_proposal_that_has_answered_nothing_is_silent(self, tmp_path):
        """The obligation ARRIVES with the Response.  A proposal still awaiting
        its first review owes no contract revision, and this is the whole reason
        the gate can be unconditional on status."""
        assert _p3(tmp_path, response=None, revision=None,
                   status="awaiting-review") == []

    def test_a_plan_is_silent_because_its_rule_is_the_opposite(self, tmp_path):
        """The contract's very next paragraph gives the plan the inverse rule:
        *"Its appended Response is a finding-disposition table that ... does not
        reproduce replacement cells in an amendment ledger."*  A plan carrying a
        `## Response to plan review` must therefore not be asked for a ledger."""
        plans = tmp_path / "dev" / "plans"
        plans.mkdir(parents=True, exist_ok=True)
        path = plans / "p3-plan.md"
        path.write_text(
            "# p3-plan\n\n**Status**: executing\n"
            "**Plan review**: required(Internal)\n\n"
            "## Scope\n\nx\n\n"
            "## Response to plan review -- Author A -- 2026-08-11\n\n"
            "**[R1]** accept, folded into the chunk row.\n",
            encoding="utf-8")
        art = planner._read_artifact(path)
        assert planner.current_contract_violations(art) == []


class TestP3TheRevisionIsMandatory:
    """Obligation A -- a Response without a complete current contract refuses."""

    def test_a_response_with_no_revision_refuses(self, tmp_path):
        v = _p3(tmp_path, revision=None)
        assert len(v) == 1, v
        assert "carries no complete current-contract revision" in v[0], v

    def test_the_refusal_quotes_the_response_it_answered(self, tmp_path):
        """The author is told WHICH record created the obligation, not that
        'something is missing' -- S8's rule, reused."""
        v = _p3(tmp_path, revision=None)
        assert _P3_RESPONSE in v[0], v

    def test_the_refusal_names_the_eight_contents_of_a_complete_contract(
            self, tmp_path):
        """A refusal that says 'add a revision' without saying what a complete
        contract contains hands the author a puzzle instead of a rule."""
        v = _p3(tmp_path, revision=None)
        for named in ("scope", "exclusions", "invariants",
                      "failure dispositions", "public paths", "evidence",
                      "omissions", "deferred work"):
            assert named in v[0], named

    @pytest.mark.parametrize("heading", [
        "## Revised proposal",
        "## Revised proposal -- 2026-08-11",
        "## Revised proposal, round 2 -- content-free findings -- 2026-08-11",
        "## Revised proposal (Round 5) -- expiry mechanics -- 2026-08-11",
        "## Revision 1 -- complete current contract",
        "## Revision after the [I2] direction -- Author A -- 2026-08-11",
    ])
    def test_every_live_revision_spelling_satisfies_the_obligation(
            self, tmp_path, heading):
        """Six real corpus spellings.  Measured across the 53 proposals that carry
        a Response or a revision: 44 distinct H2 headings match this matcher and
        every one of them is genuinely a revision record -- no false positive in
        the tree -- which is what makes a `revision`-anywhere match safe here."""
        assert _p3(tmp_path, revision=heading) == []

    def test_a_similar_but_different_word_is_not_a_revision(self, tmp_path):
        """Word-anchored: `## Revisiting the loader` is prose, not a contract."""
        v = _p3(tmp_path, revision="## Revisiting the loader contract")
        assert any("no complete current-contract revision" in m for m in v), v


class TestP3TheLedgerIsMandatory:
    """Obligation B -- every revision carries exactly one ledger, with a value."""

    def test_a_revision_with_no_ledger_refuses(self, tmp_path):
        v = _p3(tmp_path, ledger=None)
        assert len(v) == 1, v
        assert f"no '{_P3_LEDGER}' heading" in v[0], v
        assert "MANDATORY" in v[0] and "'None'" in v[0], v

    def test_the_refusal_quotes_the_revision_that_owes_it(self, tmp_path):
        v = _p3(tmp_path, ledger=None)
        assert _P3_REVISION in v[0], v

    def test_a_bare_ledger_heading_refuses(self, tmp_path):
        """The empty-label defect, closed here as `_has_disposition_attestation`
        closed it for the archive block: a heading with nothing under it is a
        check passing on its own scaffold.  *"Mandatory even when its value is
        `None`"* means the `None` is WRITTEN, not inferred from silence."""
        v = _p3(tmp_path, value=None)
        assert len(v) == 1, v
        assert "carries no written value" in v[0], v

    def test_a_duplicate_ledger_in_one_revision_refuses(self, tmp_path):
        """Two ledgers cannot both be the complete account of one revision --
        `_parse_one_field`'s rule (a duplicate refuses even when the values
        agree), applied to a heading."""
        v = _p3(tmp_path, trailer=f"{_P3_LEDGER}\n\n* None\n")
        assert len(v) == 1, v
        assert "duplicate" in v[0], v

    def test_each_revision_needs_its_OWN_ledger(self, tmp_path):
        """Per-revision, not per-artifact: the contract attaches the heading to
        the complete contract, so an earlier revision's ledger cannot serve a
        later one.  Both refusals are reported, each quoting its own revision."""
        body = (_p3_body()
                + "## Revised proposal -- Revision 3\n\nThe next contract.\n\n"
                + "## Revised proposal -- Revision 4\n\nAnd the next.\n")
        art = _p3_prop(tmp_path, body)
        v = planner.current_contract_violations(art)
        assert len(v) == 2, v
        assert any("Revision 3" in m for m in v), v
        assert any("Revision 4" in m for m in v), v
        assert not any("Revision 2" in m for m in v), v


class TestP3WhatIsNotAHeading:
    """The false-CLEAR channels -- each measured on real bytes, not imagined."""

    def test_a_ledger_quoted_inside_a_fence_does_not_satisfy_it(self, tmp_path):
        """**The channel that exists in this tree.**  The accepted contract
        quotes the ledger heading inside a ```text fence *in the same section as
        its real one*, so a raw byte search finds two headings in that artifact
        where markdown has one.  A fenced `###` is literal text; counting it would
        let a proposal satisfy the requirement by QUOTING the specification."""
        fenced = ("```text\n" + _P3_LEDGER + "\n* <entry>\n```")
        v = _p3(tmp_path, ledger=None, trailer="")
        assert len(v) == 1, v
        art = _p3_prop(tmp_path, _p3_body(ledger=None) + fenced + "\n")
        v2 = planner.current_contract_violations(art)
        assert len(v2) == 1, v2
        assert f"no '{_P3_LEDGER}' heading" in v2[0], v2

    def test_an_indented_ledger_does_not_satisfy_it(self, tmp_path):
        """Both authoring templates teach the heading in a 4-space indented
        block, which is a code block rather than a heading.  That is what keeps a
        scaffolded proposal from clearing the requirement it teaches -- the
        column-0 rule is markdown's own."""
        art = _p3_prop(tmp_path,
                       _p3_body(ledger=None) + "    " + _P3_LEDGER + "\n")
        v = planner.current_contract_violations(art)
        assert len(v) == 1, v
        assert f"no '{_P3_LEDGER}' heading" in v[0], v

    def test_prose_discussing_the_ledger_is_not_the_ledger(self, tmp_path):
        """P2 proved the header bound is load-bearing rather than cosmetic: this
        plan and the archived contract both DISCUSS the heading in prose, and a
        whole-text search makes the artifact that specifies a field declare it
        about itself.  A heading match needs the hashes at the margin."""
        prose = (f"The revision owes a `{_P3_LEDGER}` heading, and its value may "
                 f"be None.\n")
        art = _p3_prop(tmp_path, _p3_body(ledger=None) + prose)
        v = planner.current_contract_violations(art)
        assert len(v) == 1, v


class TestP3NearMisses:
    """S8's rule reused: quote the heading that did not count."""

    @pytest.mark.parametrize("heading", [
        "## Withdrawn / superseded commitments",
        "#### Withdrawn / superseded commitments",
    ])
    def test_a_wrong_LEVEL_heading_is_quoted_as_a_near_miss(
            self, tmp_path, heading):
        v = _p3(tmp_path, ledger=heading)
        assert len(v) == 1, v
        assert "nearest heading is" in v[0] and heading in v[0], v
        assert "the ledger is an H3" in v[0], v

    @pytest.mark.parametrize("heading", [
        "### Withdrawn / superseded commitment",
        "### Superseded / withdrawn commitments",
        "### Withdrawn and superseded work",
    ])
    def test_a_WORD_variant_is_quoted_as_a_near_miss(self, tmp_path, heading):
        """Keyed on the two words every plausible misspelling retains, the trick
        `_INHERITANCE_NEAR_MISS_RE` already uses: recognize the neighbourhood,
        then quote the line, instead of leaving a bare 'missing' behind."""
        v = _p3(tmp_path, ledger=heading)
        assert len(v) == 1, v
        assert "nearest heading is" in v[0] and heading in v[0], v

    def test_an_unrelated_heading_produces_no_near_miss_hint(self, tmp_path):
        """The hint must not fire on every H3 in the revision, or it stops
        pointing at anything."""
        v = _p3(tmp_path, ledger="### Evidence and omissions")
        assert len(v) == 1, v
        assert "nearest heading is" not in v[0], v


class TestP3Grandfathering:
    """`_is_immutable`, in both directions and in the fail-closed direction."""

    @pytest.mark.parametrize("status", ["accepted", "rejected", "superseded"])
    def test_a_terminal_proposal_is_silent(self, tmp_path, status):
        """The 52 pre-ledger proposals are append-only: a requirement that
        reached them would be a permanent red on text nobody may edit.  The one
        LIVE member of that population is grandfathered by exactly this arm -- its
        status is `accepted` while it still sits in `dev/proposals/`."""
        assert _p3(tmp_path, revision=None, ledger=None, status=status) == []

    def test_an_archived_proposal_is_silent(self, tmp_path):
        """The other 51, grandfathered by location."""
        assert _p3(tmp_path, revision=None, status="revised",
                   archived=True) == []

    @pytest.mark.parametrize("header", [
        "",                                       # no Status line at all
        "**Status**: revised\n**Status**: accepted",   # duplicate
        "**Status**: whatever-this-is",           # unrecognized
    ])
    def test_a_missing_duplicate_or_UNKNOWN_status_falls_INTO_the_rule(
            self, tmp_path, header):
        """`_strict_header_status` returns None for all three, and None means NOT
        grandfathered.  The direction matters: an artifact whose status cannot be
        read must owe the obligation, never inherit the exemption -- otherwise
        deleting a Status line is how you escape the gate."""
        base = tmp_path / "dev" / "proposals"
        base.mkdir(parents=True, exist_ok=True)
        path = base / "p3-status.md"
        path.write_text(
            f"# p3-status\n\n{header}\n\n## Context\n\nx\n\n"
            + _p3_body(revision=None),
            encoding="utf-8")
        v = planner.current_contract_violations(planner._read_artifact(path))
        assert len(v) == 1, (header, v)

    def test_p3_ships_no_legacy_manifest(self):
        """The fence on the claim in the block's own comment.  P1 and C needed
        enumerated grandfather manifests; P3 does not, because immutability covers
        the whole pre-ledger population (re-derived by the node below).  If a
        later change needs one, it has to add it deliberately rather than
        arrive by edit -- and a manifest that appears here without a re-derivation
        is exactly the stale-data defect [CF4] recorded."""
        src = _PLANNER_PATH.read_text(encoding="utf-8")
        start = src.index("# === P3 -- the complete current contract")
        end = src.index("def review_record_violations(")
        block = src[start:end]
        for forbidden in ("_LEGACY", "_is_legacy(", "hashlib", "_git_readonly",
                          "subprocess", "read_text", "write_text", "open("):
            assert forbidden not in block, forbidden


def _p3_all_proposals():
    """Every proposal artifact in this tree, live and archived."""
    for fam in ("proposals", "proposals/archive"):
        base = CAIRN_ROOT / "dev" / fam
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*.md")):
            if path.name in ("_template.md", "README.md"):
                continue
            yield planner._read_artifact(path)


def test_the_live_corpus_owes_no_ledger_today():
    """**The empty trigger set, recorded as a measurement rather than left as an
    accident.**  No artifact in this tree -- live or archived -- is refused by
    this contract today: the one proposal that carries a ledger conforms, and
    every proposal that does not is immutable.  When a live proposal first lands a
    Response, this node reddens, and that is the signal to check that the
    revision it landed with carries its ledger.  Until then it is the standing
    proof that P3's blast radius is exactly zero, and the reason every other node
    above is synthetic."""
    flagged = {art.path.name: planner.current_contract_violations(art)
               for art in _p3_all_proposals()
               if planner.current_contract_violations(art)}
    assert flagged == {}, flagged


def test_every_pre_ledger_proposal_is_covered_by_immutability_alone(
        monkeypatch):
    """The claim P3 ships on, re-derived instead of trusted.

    With grandfathering switched off, the obligation is measured over the whole
    corpus; every artifact it reaches must be immutable.  Written as a monkeypatch
    of the one predicate rather than as a second implementation of the rule,
    because a hand-written second oracle is free to drift from the shipped one --
    which is the failure mode a "measured" claim is supposed to prevent.
    """
    arts = list(_p3_all_proposals())
    owing, uncovered = [], []
    monkeypatch.setattr(planner, "_is_immutable", lambda art: False)
    for art in arts:
        if planner.current_contract_violations(art):
            owing.append(art.path.name)
    monkeypatch.undo()
    for name in owing:
        art = next(a for a in arts if a.path.name == name)
        if not planner._is_immutable(art):
            uncovered.append(name)
    assert uncovered == [], (
        "a MUTABLE proposal owes a ledger it cannot have -- P3 would need a "
        f"legacy manifest, or that artifact needs the heading: {uncovered}")
    assert len(owing) >= 40, (
        "the pre-ledger population collapsed, which means the obligation stopped "
        f"reaching the records it was measured against: {len(owing)}")


class TestP3BothGateSurfacesAgree:
    """[R3-E1]'s rule: a predicate wired to one surface leaves the other loose,
    and the loose surface is the one an author drives."""

    def test_scan_reports_the_refusal(self, tmp_path):
        art = _p3_prop(tmp_path, _p3_body(ledger=None))
        identity = planner._load_identity_model(tmp_path)
        v = planner._conformance_violations(art, identity)
        assert any(f"no '{_P3_LEDGER}' heading" in m for m in v), v

    @pytest.mark.parametrize("target", ["awaiting-review", "revised",
                                        "awaiting-decision", "accepted"])
    def test_every_forward_transition_reports_it_unmet(self, tmp_path, target):
        """Reported on EVERY forward transition, because the obligation does not
        begin at some later state: an author who met the refusal only at the
        Decision would already have asked a reviewer to read a contract that was
        never restated."""
        art = _p3_prop(tmp_path, _p3_body(ledger=None), status="revised")
        identity = planner._load_identity_model(tmp_path)
        gates = planner._gating_preconditions(art, target, identity)
        hits = [d for met, d in gates if not met and "ledger" in d]
        assert hits, (target, [d for _m, d in gates])

    def test_the_same_predicate_object_serves_both(self):
        """One implementation, two call sites -- S12's rule.  A sibling copy is
        how the two surfaces end up disagreeing about the same record."""
        src = _PLANNER_PATH.read_text(encoding="utf-8")
        assert src.count("def current_contract_violations(") == 1
        assert src.count("current_contract_violations(art)") == 2


class TestP3TheRealContractIsTheORACLE:
    """The strongest available oracle: the accepted contract's own bytes."""

    def test_the_accepted_contract_clears_when_it_is_made_live(self, tmp_path):
        """`2026-08-10-codex-review-efficient-lifecycle.md` is the one artifact in
        the tree that satisfies this rule, and it satisfies it while ALSO quoting
        the heading inside a fence four lines above the real one.  Re-homed as a
        live proposal it must clear -- which tests the fence discrimination and
        the whole predicate against real prose rather than a fixture built to
        pass."""
        src = (CAIRN_ROOT / "dev" / "proposals" / "archive"
               / "2026-08-10-codex-review-efficient-lifecycle.md")
        text = src.read_text(encoding="utf-8")
        assert text.count(_P3_LEDGER + "\n") == 2, (
            "the fixture's premise moved: the source no longer carries one fenced "
            "quote of the heading and one real one")
        base = tmp_path / "dev" / "proposals"
        base.mkdir(parents=True, exist_ok=True)
        path = base / src.name
        path.write_text(
            text.replace("**Status**: accepted", "**Status**: revised", 1),
            encoding="utf-8")
        art = planner._read_artifact(path)
        assert planner._is_immutable(art) is False
        assert planner.current_contract_violations(art) == []
        found = [h for _n, lvl, h, norm in planner._heading_records(art.text)
                 if planner._is_ledger_heading(lvl, norm)]
        assert found == [_P3_LEDGER], found


class TestP3AuthoringTemplates:
    """P3's template half, pinned per surface in P1's and P2's idiom.

    The plan's acceptance criteria require each documentation surface to be
    *confirmed* updated ("drift gates catch drift, not absence"), and an author
    refused by a gate who finds no instruction in the template has been handed a
    puzzle instead of a rule.  **Both sides of every pair**, for the reason
    `scope-reduction-trap`'s Chunk B established the hard way.
    """

    SURFACES = {
        "dev/proposals/_template.md": {
            # Needles sit inside ONE physical line: the templates are hard-wrapped,
            # so a phrase that reads continuously on the page can straddle a
            # newline, and a straddling needle fails for a formatting reason.
            "the revision is mandatory, not conditional":
                "one complete current contract with the Response, every time",
            "the ledger heading, verbatim": _P3_LEDGER,
            "None must be written": "only a written `None` distinguishes",
            "the newest revision is what binds": "newest reviewed",
            "earlier sections stay history": "immutable history",
            "the H3-at-the-margin rule": "at the left margin",
            "the reviewer verifies the ledger": "verify its withdrawal ledger",
            "what the checker cannot do": "it never verifies that the ledger is",
        },
        "dev/plans/_template.md": {
            "the plan's rule is the opposite":
                "not in a contract revision",
            "no ledger on a plan": "ledger; a plan does not",
            "corrections fold into the cells":
                "fold plan-review corrections straight into the mutable",
            "and stop folding once a chunk starts":
                "execution of a chunk begins",
        },
    }

    @pytest.mark.parametrize("rel", sorted(SURFACES))
    @pytest.mark.parametrize("shipped", [False, True])
    def test_each_surface_carries_the_contract(self, rel, shipped):
        path = CAIRN_ROOT / (f"templates/core/{rel}" if shipped else rel)
        text = path.read_text(encoding="utf-8")
        missing = [name for name, needle in self.SURFACES[rel].items()
                   if needle not in text]
        assert not missing, (path, missing)

    @pytest.mark.parametrize("rel", ["dev/proposals/_template.md",
                                     "templates/core/dev/proposals/_template.md"])
    def test_the_scaffolded_proposal_template_carries_no_real_ledger(self, rel):
        """The template teaches the heading by QUOTING it, so the quoted grammar
        must not become a heading in every proposal copied from it.  This node is
        what keeps the example indented as the template is edited -- un-indent it
        and a scaffolded proposal would clear a requirement it never met."""
        path = CAIRN_ROOT / rel
        text = path.read_text(encoding="utf-8")
        assert _P3_LEDGER in text, rel
        found = [h for _n, lvl, h, norm in planner._heading_records(text)
                 if planner._is_ledger_heading(lvl, norm)]
        assert found == [], (rel, found)

    def test_the_emitted_revised_scaffold_clears_its_own_gate(self, tmp_path):
        """A scaffold that emits text its own checker refuses is worse than no
        scaffold: the tool would hand the author a violation.  The `revised`
        block previously said the revision was *optional* -- the pre-contract
        wording -- and this node is why that could not survive."""
        art = _p3_prop(tmp_path, "", status="reviewed")
        _f, _t, blocks = planner._scaffold(art, "revised", "2026-08-11")
        pasted = _p3_prop(tmp_path, blocks[0] + "\n", status="revised",
                          stem="p3-scaffolded")
        assert planner.current_contract_violations(pasted) == []
        joined = " ".join(blocks)
        assert "optional '## Revised proposal'" not in joined, joined
        assert _P3_LEDGER in blocks[0], blocks[0]


class TestClosedVocabularyValuesTolerateHouseStyle:
    """A closed-vocabulary field reads the **value** the way the tree writes it.

    Found by a live refusal, not by review: another session opened
    `2026-08-12-claude-ceremony-handshake-and-first-use.md` declaring
    `**Assurance path**: **high-assurance** -- <reason>`, adopting P1's new field
    correctly in spirit, and the gate refused it.  Two parsers in one file
    disagreed about one documented house style -- `_parse_verdict` strips
    emphasis ("the house form ... wraps the label AND the value in one bold
    span ... 30 of the 38 corpus passes") while `_parse_one_field` did not.
    """

    def _p(self, line, vocab=None, field="Assurance path"):
        return planner._parse_one_field(
            line, planner._REVIEW_FIELD_RE[field],
            vocab or planner.ASSURANCE_PATHS, field)

    def test_the_documented_house_style_clears(self):
        """`**field**: **value**` is how this tree writes attestations."""
        assert self._p("**Assurance path**: **high-assurance**") == (
            "high-assurance", None)

    def test_a_trailing_rationale_clears(self):
        """Refusing it teaches authors to delete the reason rather than record
        it.  Both dash forms, because both are Cairn's normal clause break."""
        for line in ("**Assurance path**: **high-assurance** — a trust ceremony",
                     "**Assurance path**: high-assurance -- a trust ceremony",
                     "**Assurance path**: standard -- routine translation"):
            value, problem = self._p(line)
            assert problem is None, line
            assert value in planner.ASSURANCE_PATHS

    def test_a_rationale_naming_the_other_value_refuses(self):
        """The **whole** reason truncation is guarded rather than free.

        Truncating at a clause break alone is asymmetrically unsafe: it would
        read `standard -- actually high-assurance` as `standard`, the direction
        the accepted contract explicitly forbids ("uncertainty resolves to
        `high-assurance`").  This is the same guard `_parse_verdict` reaches for
        so `SHIP but actually BLOCK` cannot clear.
        """
        value, problem = self._p("**Assurance path**: standard -- actually high-assurance")
        assert value is None
        assert "contradictory" in problem and "high-assurance" in problem

    def test_an_out_of_vocabulary_value_still_refuses(self):
        """The vocabulary stays closed; only its presentation loosened."""
        value, problem = self._p("**Assurance path**: mostly-fine")
        assert value is None and "unrecognized" in problem

    def test_the_rule_is_the_shared_one_not_an_assurance_special_case(self):
        """`Findings` gets the identical treatment, including the guard -- the
        fix belongs to every closed vocabulary this file reads, not to one."""
        assert self._p("**Findings**: none -- nothing came up",
                       planner._FINDINGS, "Findings") == ("none", None)
        value, problem = self._p("**Findings**: none -- but raised two concerns",
                                 planner._FINDINGS, "Findings")
        assert value is None and "contradictory" in problem


# Amendment B's parser contract.  Owned HERE because P2 created
# `_declaration_record`, `_declared_reduction` and `plan_inheritance_violations`;
# the owner of a predicate owns its contract test.


def _sd_art(tmp_path, body: str, *, status: str = "implementing", stem: str = "sd"):
    d = tmp_path / "dev" / "plans"
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{stem}.md"
    path.write_text(
        f"# Plan: {stem}\n\n**Status**: {status}\n"
        f"**Plan review**: required(Internal)\n\n{body}",
        encoding="utf-8")
    return planner._read_artifact(path)


_ALLOWANCE = "> Maintainer: go ahead and drop chunk D.\n"


class TestScopeDeltaParserContract:
    """Amendment B's `Scope delta` reader, table-driven.

    **Why this class exists.** The behaviour shipped with no contract test. An
    External review of the sibling `scope-reduction-trap` plan changed
    `_declaration_record` in **both** twins to begin at the declaration line
    instead of its preceding heading -- silently revoking the authority of every
    allowance written *above* its field -- and **745 tests passed**. Reproduced
    here before writing this class. The only test that touched the predicate
    lived under the sibling plan, which owns neither the symbol nor the risk.

    **The policy this encodes is settled and is not re-opened here** (Maintainer
    decision, 2026-08-12, recorded in `dev/plans/scope-reduction-trap.md`):

    * a **presence** check is forbidden -- nothing may refuse because the
      declaration is absent, unfilled or unrecognised. A tool sees whether the
      box is ticked, never whether the tick is honest, so it catches forgetting,
      misses evasion, and *supplies cover* for evasion by turning the transition
      green. `doctrine/dual-review.md` > "The counterweight".
    * an **authorization** check is permitted -- a declaration that exists and
      declares a loss without a Maintainer allowance refuses, because *who may
      concede an outcome* is the part that cannot be recovered afterwards.
    """

    # -- dimension 1 + 2: accepted spellings, and what must yield NOTHING ------

    @pytest.mark.parametrize("value", ["degraded", "lost", "**lost**", "Lost",
                                       "degraded.", "  lost  "])
    def test_a_reduction_is_recognized_in_every_accepted_spelling(
            self, tmp_path, value):
        art = _sd_art(tmp_path, f"## R\n\n**Scope delta**: {value}\n")
        assert [(v, a) for _l, v, a in planner._declared_reduction(art)] == [
            (value.strip().rstrip(".").strip("*").casefold(), False)]

    @pytest.mark.parametrize("value", [
        "preserved", "", "preserved | degraded | lost", "mostly fine",
        "PRESERVED", "none",
    ])
    def test_no_presence_check_exists_in_any_direction(self, tmp_path, value):
        """The forbidden half. `preserved`, unfilled, the template's own prompt
        line, and any unrecognised token all yield **nothing** -- so no
        transition can refuse for a missing or malformed declaration."""
        art = _sd_art(tmp_path, f"## R\n\n**Scope delta**: {value}\n")
        assert planner._declared_reduction(art) == []

    def test_an_absent_field_yields_nothing(self, tmp_path):
        art = _sd_art(tmp_path, "## R\n\nno declaration at all\n")
        assert planner._declared_reduction(art) == []

    # -- dimension 3: allowance position relative to the field ----------------

    def test_an_allowance_ABOVE_the_field_authorizes_it(self, tmp_path):
        """The exact case the sibling's mutation revoked. The record is
        heading-bounded, so position within it does not matter."""
        art = _sd_art(tmp_path, f"## R\n\n{_ALLOWANCE}\n**Scope delta**: lost\n")
        assert [a for _l, _v, a in planner._declared_reduction(art)] == [True]

    def test_an_allowance_BELOW_the_field_authorizes_it(self, tmp_path):
        art = _sd_art(tmp_path, f"## R\n\n**Scope delta**: lost\n\n{_ALLOWANCE}")
        assert [a for _l, _v, a in planner._declared_reduction(art)] == [True]

    # -- dimension 4: neighbouring heading records ----------------------------

    def test_an_allowance_IN_A_NEIGHBOURING_RECORD_DOES_NOT_REACH(self, tmp_path):
        """Both directions. "The record the declaration sits in" is the whole
        rule: an allowance one heading away authorizes a different record, and
        letting it leak would make any quoted Maintainer sentence anywhere in a
        plan authorize every later reduction in it."""
        below = _sd_art(tmp_path, f"## A\n\n**Scope delta**: lost\n\n## B\n\n{_ALLOWANCE}")
        assert [a for _l, _v, a in planner._declared_reduction(below)] == [False]
        above = _sd_art(tmp_path, f"## A\n\n{_ALLOWANCE}\n## B\n\n**Scope delta**: lost\n",
                        stem="sd2")
        assert [a for _l, _v, a in planner._declared_reduction(above)] == [False]

    @pytest.mark.parametrize("heading", ["# H1", "### H3", "###### H6"])
    def test_every_heading_level_bounds_the_record(self, tmp_path, heading):
        art = _sd_art(tmp_path, f"## A\n\n{_ALLOWANCE}\n{heading}\n\n**Scope delta**: lost\n")
        assert [a for _l, _v, a in planner._declared_reduction(art)] == [False]

    # -- dimension 5: attached / non-isolated quotes ---------------------------

    def test_a_quote_not_visually_isolated_does_not_authorize(self, tmp_path):
        """`_has_isolated_blockquote` requires a blank line before the `>`. An
        attached quote reads as continuing prose, not as a set-apart
        authorization -- the same idiom `## Decision` uses."""
        art = _sd_art(tmp_path, "## R\n\nsome prose\n> Maintainer: fine.\n\n"
                                "**Scope delta**: lost\n")
        assert [a for _l, _v, a in planner._declared_reduction(art)] == [False]

    # -- dimension 6: fenced examples ------------------------------------------

    def test_a_fenced_example_quote_does_not_authorize(self, tmp_path):
        """A `>` inside a fence is a shell prompt, a diff or a doc example. This
        matters on real bytes: the authoring templates and this plan both show
        the allowance idiom inside fences."""
        art = _sd_art(tmp_path, "## R\n\n```text\n\n> Maintainer: go ahead.\n```\n\n"
                                "**Scope delta**: lost\n")
        assert [a for _l, _v, a in planner._declared_reduction(art)] == [False]

    def test_a_fenced_declaration_is_still_read(self, tmp_path):
        """Stated as the honest limit, not asserted as a virtue: the field
        matcher is line-based and does not skip fences, so a documented example
        of the FIELD is read as a declaration. Harmless while the value shown is
        the template's own unfilled prompt (which yields nothing), and recorded
        here so a future reader is not surprised by it."""
        art = _sd_art(tmp_path, "## R\n\n```text\n**Scope delta**: lost\n```\n")
        assert [v for _l, v, _a in planner._declared_reduction(art)] == ["lost"]

    # -- dimension 7: multiple declarations ------------------------------------

    def test_two_declarations_in_one_record_share_its_allowance(self, tmp_path):
        art = _sd_art(tmp_path, f"## R\n\n{_ALLOWANCE}\n**Scope delta**: lost\n\n"
                                "**Scope delta**: degraded\n")
        assert [(v, a) for _l, v, a in planner._declared_reduction(art)] == [
            ("lost", True), ("degraded", True)]

    def test_declarations_in_separate_records_are_judged_separately(self, tmp_path):
        art = _sd_art(tmp_path, f"## A\n\n{_ALLOWANCE}\n**Scope delta**: lost\n\n"
                                "## B\n\n**Scope delta**: degraded\n")
        assert [(v, a) for _l, v, a in planner._declared_reduction(art)] == [
            ("lost", True), ("degraded", False)]

    # -- the consumer, and the dormancy fact ----------------------------------

    def test_the_refusal_is_dormant_today_and_that_is_recorded_not_hidden(
            self, tmp_path):
        """`plan_inheritance_violations` returns `[]` for a non-plan and is
        otherwise gated on `_declares_inheritance`, which measures **zero of the
        live corpus**. So nothing refuses today on either plan's side. Not a
        defect -- but a sibling manifest string once claimed otherwise and had to
        be corrected, so the dormancy is pinned here rather than described."""
        art = _sd_art(tmp_path, f"## R\n\n**Scope delta**: lost\n")
        assert not planner._declares_inheritance(art)
        assert planner.plan_inheritance_violations(art) == []
        found = planner._declared_reduction(art)
        assert [(v, a) for _l, v, a in found] == [("lost", False)]
        # the reported line is the field's own, derived rather than hardcoded
        lines = planner._split_lines(art.text)
        assert lines[found[0][0] - 1].startswith("**Scope delta**:")
