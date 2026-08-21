"""Fixtures for the `cairn-event-v1` grammar / history-diff / reconciliation
machinery (`metrics-events-not-prose` Parts 3, Chunks 4-7).

Loaded through the installed launcher facade
(`templates/modules/default-on/lifecycle_metrics.py`), the same surface an
adopter imports -- consistent with the other `bootstrap/tests/test_lifecycle_*`
files. This is a NEW test file (recorded as FROZEN-NEW by the gate manifest;
its node-IDs as COLLECTION-ADDED), so it adds coverage without a gate
re-anchor.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import List, Tuple

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
_LM_PATH = CAIRN_ROOT / "templates" / "modules" / "default-on" / "lifecycle_metrics.py"


def _load_lm() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cairn_lm_events", _LM_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["cairn_lm_events"] = module
    spec.loader.exec_module(module)
    return module


_lm = _load_lm()
events = _lm.events

_PROPOSAL_STATES = (
    "awaiting-review", "revising", "awaiting-decision",
    "accepted", "rejected", "superseded",
)
_PLAN_STATES = (
    "awaiting-plan-review", "revising-plan", "ready-to-implement",
    "implementing", "awaiting-code-review", "revising-code",
    "ready-to-archive", "archived",
)


# ---------------------------------------------------------------------------
# Chunk 4 -- grammar fixtures (pure, no git)
# ---------------------------------------------------------------------------


def _fence(kind: str, **fields: str) -> str:
    lines = ["<!-- cairn-event-v1", f"kind: {kind}"]
    lines.extend(f"{k}: {v}" for k, v in fields.items())
    lines.append("-->")
    return "\n".join(lines) + "\n"


def test_no_fence_at_all_returns_empty_list() -> None:
    """A document with no event fence at all is not an error -- nothing
    is wrong with a tree that has not yet recorded any events."""
    assert events.parse_event_blocks(
        "just ordinary proposal prose, no fence here\n",
        valid_states=_PROPOSAL_STATES,
    ) == []


def test_three_worked_examples_parse_cleanly() -> None:
    """The three block shapes reproduced verbatim from Round 7 §1.  The
    transition example's ``reviewed``/``revised`` tokens are the
    pre-vocabulary-migration HISTORICAL states (an archived artifact may
    still declare them; `_plan_status_enum()`/`_proposal_status_enum()`
    resolve current + historical together) -- included here alongside a
    current token so the fixture is not silently narrowed to the
    current-only vocabulary."""
    historical_and_current = _PLAN_STATES + ("proposed", "reviewed", "revised")
    transition = _fence("transition", from_state="reviewed", to_state="revised")
    review_pass = _fence(
        "review-pass", tier="External",
        reviewer="<reviewer name as written in the section heading>",
    )
    response = _fence(
        "response",
        model="<model identity as written in the Response's Model field>",
    )
    b1 = events.parse_event_blocks(transition, valid_states=historical_and_current)
    assert len(b1) == 1 and b1[0].kind == "transition"
    assert b1[0].from_state == "reviewed" and b1[0].to_state == "revised"

    b2 = events.parse_event_blocks(review_pass, valid_states=_PROPOSAL_STATES)
    assert len(b2) == 1 and b2[0].kind == "review-pass"
    assert b2[0].tier == "External"

    b3 = events.parse_event_blocks(response, valid_states=_PROPOSAL_STATES)
    assert len(b3) == 1 and b3[0].kind == "response"


def test_unknown_version_token_refuses() -> None:
    text = _fence("transition", from_state="revising", to_state="accepted").replace(
        "cairn-event-v1", "cairn-event-v2"
    )
    with pytest.raises(events.EventGrammarError, match="unknown event version"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_unknown_kind_refuses() -> None:
    text = "<!-- cairn-event-v1\nkind: bogus\n-->\n"
    with pytest.raises(events.EventGrammarError, match="unknown event kind"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_missing_required_key_per_kind_refuses() -> None:
    cases = [
        "<!-- cairn-event-v1\nkind: transition\nfrom_state: revising\n-->\n",
        "<!-- cairn-event-v1\nkind: review-pass\ntier: External\n-->\n",
        "<!-- cairn-event-v1\nkind: response\n-->\n",
    ]
    for text in cases:
        with pytest.raises(events.EventGrammarError, match="missing required"):
            events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_unknown_key_refuses() -> None:
    text = _fence(
        "transition", from_state="revising", to_state="accepted", bogus="x",
    )
    with pytest.raises(events.EventGrammarError, match="unknown key"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_reviewer_and_model_over_120_chars_refuses() -> None:
    long_value = "x" * 121
    reviewer_text = _fence("review-pass", tier="External", reviewer=long_value)
    with pytest.raises(events.EventGrammarError, match="exceeds 120"):
        events.parse_event_blocks(reviewer_text, valid_states=_PROPOSAL_STATES)

    model_text = _fence("response", model=long_value)
    with pytest.raises(events.EventGrammarError, match="exceeds 120"):
        events.parse_event_blocks(model_text, valid_states=_PROPOSAL_STATES)


def test_recorded_by_is_optional_and_informational() -> None:
    text = _fence(
        "transition", from_state="revising", to_state="accepted",
        recorded_by="Someone",
    )
    blocks = events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)
    assert blocks[0].recorded_by == "Someone"


def test_malformed_field_line_refuses() -> None:
    text = "<!-- cairn-event-v1\nkind transition\n-->\n"
    with pytest.raises(events.EventGrammarError, match="malformed event field"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_duplicate_key_refuses() -> None:
    text = (
        "<!-- cairn-event-v1\nkind: transition\nfrom_state: revising\n"
        "from_state: accepted\nto_state: accepted\n-->\n"
    )
    with pytest.raises(events.EventGrammarError, match="duplicate event key"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


def test_from_state_outside_valid_states_refuses() -> None:
    """Row 4-13: a `from_state`/`to_state` value outside the supplied
    `valid_states` refuses, using a small literal test vocabulary --
    this chunk's own fixtures stay pure-function and need no planner on
    disk (the integration-level fixture against the real loader is
    Chunk 6's row 6-3/6-4)."""
    text = _fence("transition", from_state="revising", to_state="nonexistent-state")
    with pytest.raises(events.EventGrammarError, match="not a declared lifecycle status"):
        events.parse_event_blocks(text, valid_states=("revising", "accepted"))


def test_bad_tier_refuses() -> None:
    text = _fence("review-pass", tier="Bogus", reviewer="Bob")
    with pytest.raises(events.EventGrammarError, match="tier"):
        events.parse_event_blocks(text, valid_states=_PROPOSAL_STATES)


# ---------------------------------------------------------------------------
# Chunk 5 -- history-diff reader fixtures, against a REAL scratch git repo
# (never a mocked history), reusing the `_git` helper pattern already
# present in `bootstrap/tests/test_lifecycle_contract.py` rather than
# inventing a second one.
# ---------------------------------------------------------------------------


def _git(args: List[str], cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True,
                    capture_output=True, text=True)


def _make_git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(["init", "-q"], repo)
    _git(["config", "user.email", "t@example.com"], repo)
    _git(["config", "user.name", "Test"], repo)
    return repo


def _commit_all(repo: Path, msg: str = "fixture") -> None:
    _git(["add", "-A"], repo)
    _git(["commit", "-q", "-m", msg], repo)


def _head_sha(repo: Path) -> str:
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(repo),
                        capture_output=True, text=True, check=True)
    return r.stdout.strip()


def _current_branch(repo: Path) -> str:
    r = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], cwd=str(repo),
                        capture_output=True, text=True, check=True)
    return r.stdout.strip()


def _artifact_text(status: str, body: str = "") -> str:
    return f"# p\n\n**Status**: {status}\n\n{body}"


def test_mutated_existing_block_refuses(tmp_path: Path) -> None:
    repo = _make_git_repo(tmp_path)
    p = repo / "p.md"
    p.write_text(
        _artifact_text(
            "revising",
            _fence("transition", from_state="awaiting-review", to_state="revising"),
        ),
        encoding="utf-8",
    )
    _commit_all(repo, "c1: transition")
    # Edit the existing block's own text in a later commit -- the value
    # changes, nothing is added.
    p.write_text(
        _artifact_text(
            "revising",
            _fence("transition", from_state="awaiting-review", to_state="awaiting-decision"),
        ),
        encoding="utf-8",
    )
    _commit_all(repo, "c2: mutate the block")
    with pytest.raises(events.ReconciliationError, match="mutated"):
        events.walk_history(repo, "p.md", valid_states=_PROPOSAL_STATES)


def test_reordered_or_deleted_block_refuses(tmp_path: Path) -> None:
    repo = _make_git_repo(tmp_path)
    p = repo / "p.md"
    p.write_text(_artifact_text("revising", _fence(
        "transition", from_state="awaiting-review", to_state="revising")),
        encoding="utf-8")
    _commit_all(repo, "c1")
    # Delete the existing block entirely.
    p.write_text(_artifact_text("revising"), encoding="utf-8")
    _commit_all(repo, "c2: delete the block")
    with pytest.raises(events.ReconciliationError, match="mutated"):
        events.walk_history(repo, "p.md", valid_states=_PROPOSAL_STATES)


def test_merge_commit_introducing_a_block_refuses(tmp_path: Path) -> None:
    repo = _make_git_repo(tmp_path)
    p = repo / "p.md"
    p.write_text(_artifact_text("awaiting-review"), encoding="utf-8")
    _commit_all(repo, "base")
    base_branch = _current_branch(repo)

    _git(["checkout", "-b", "feature"], repo)
    (repo / "other.md").write_text("unrelated\n", encoding="utf-8")
    _commit_all(repo, "feature change")

    _git(["checkout", base_branch], repo)
    (repo / "another.md").write_text("also unrelated\n", encoding="utf-8")
    _commit_all(repo, "main change")

    _git(["merge", "--no-ff", "--no-commit", "feature"], repo)
    # Manual merge resolution that smuggles a new block into the merge
    # commit -- neither parent's own diff carries it.
    p.write_text(_artifact_text("revising", _fence(
        "transition", from_state="awaiting-review", to_state="revising")),
        encoding="utf-8")
    _git(["add", "-A"], repo)
    _git(["commit", "-q", "-m", "merge with a smuggled block"], repo)

    with pytest.raises(events.ReconciliationError, match="merge commit"):
        events.walk_history(repo, "p.md", valid_states=_PROPOSAL_STATES)


def test_identity_survives_the_archive_rename(tmp_path: Path) -> None:
    """The concrete correctness case R5-E1 found broken in the prior
    `(artifact path, block position)` identity scheme: the identity here
    is `(introducing commit, added-block index)`, and neither term names
    a path, so a `git mv` to `archive/` cannot discontinue the series."""
    repo = _make_git_repo(tmp_path)
    (repo / "dev" / "proposals").mkdir(parents=True)
    p = repo / "dev" / "proposals" / "p.md"
    p.write_text(_artifact_text("revising", _fence(
        "transition", from_state="awaiting-review", to_state="revising")),
        encoding="utf-8")
    _commit_all(repo, "open+transition")

    before = events.walk_history(repo, "dev/proposals/p.md", valid_states=_PROPOSAL_STATES)
    assert len(before.events) == 1
    identity_before = (before.events[0].commit, before.events[0].index)

    (repo / "dev" / "proposals" / "archive").mkdir(parents=True)
    _git(["mv", "dev/proposals/p.md", "dev/proposals/archive/p.md"], repo)
    _git(["commit", "-q", "-m", "archive move"], repo)

    after = events.walk_history(
        repo, "dev/proposals/archive/p.md", valid_states=_PROPOSAL_STATES)
    assert len(after.events) == 1
    identity_after = (after.events[0].commit, after.events[0].index)
    assert identity_after == identity_before


def test_missing_marker_returns_none_not_refuse(tmp_path: Path) -> None:
    repo = _make_git_repo(tmp_path)
    t = repo / "dev" / "proposals" / "_template.md"
    t.parent.mkdir(parents=True)
    t.write_text("no marker here\n", encoding="utf-8")
    _commit_all(repo, "no marker")
    assert events.activation_commit(repo, "dev/proposals/_template.md") is None


def test_multiply_introduced_marker_refuses(tmp_path: Path) -> None:
    repo = _make_git_repo(tmp_path)
    t = repo / "dev" / "proposals" / "_template.md"
    t.parent.mkdir(parents=True)
    t.write_text("no marker\n", encoding="utf-8")
    _commit_all(repo, "no marker")
    t.write_text(f"marker: {events.VERSION_TOKEN}\n", encoding="utf-8")
    _commit_all(repo, "add marker")
    t.write_text("no marker\n", encoding="utf-8")
    _commit_all(repo, "remove marker")
    t.write_text(f"marker: {events.VERSION_TOKEN}\n", encoding="utf-8")
    _commit_all(repo, "re-add marker")
    with pytest.raises(events.ReconciliationError, match="removed and re-added"):
        events.activation_commit(repo, "dev/proposals/_template.md")


def test_divergent_marker_refuses(tmp_path: Path) -> None:
    """This module's own design choice for a mechanism Round 7's text
    names ("the pair -- Cairn's own installed copy and the shipped
    template -- disagrees") but does not specify: `companion_relpath`
    is compared at HEAD only, and the check is vacuously skipped when no
    companion exists in the tree at all (the ordinary adopter case)."""
    repo = _make_git_repo(tmp_path)
    primary = repo / "dev" / "proposals" / "_template.md"
    primary.parent.mkdir(parents=True)
    primary.write_text(f"marker: {events.VERSION_TOKEN}\n", encoding="utf-8")
    companion = repo / "templates" / "core" / "dev" / "proposals" / "_template.md"
    companion.parent.mkdir(parents=True)
    companion.write_text("no marker\n", encoding="utf-8")
    _commit_all(repo, "divergent")
    with pytest.raises(events.ReconciliationError, match="divergent"):
        events.activation_commit(
            repo, "dev/proposals/_template.md",
            companion_relpath="templates/core/dev/proposals/_template.md",
        )


def test_no_companion_in_tree_skips_the_divergence_check(tmp_path: Path) -> None:
    """The ordinary adopter shape: no `templates/core/` tree at all, so
    the divergence check is vacuous rather than a spurious refusal."""
    repo = _make_git_repo(tmp_path)
    primary = repo / "dev" / "proposals" / "_template.md"
    primary.parent.mkdir(parents=True)
    primary.write_text(f"marker: {events.VERSION_TOKEN}\n", encoding="utf-8")
    _commit_all(repo, "no companion")
    result = events.activation_commit(
        repo, "dev/proposals/_template.md",
        companion_relpath="templates/core/dev/proposals/_template.md",
    )
    assert result == _head_sha(repo)


def test_act_in_markers_own_introducing_commit_shares_that_commit(
    tmp_path: Path,
) -> None:
    """The boundary case `test_main_branch_target_runs` (the real
    reference-scripts test, Chunk 7) exercises informally: the marker's
    own introducing commit and a co-committed lifecycle act resolve to
    the SAME commit SHA from both `activation_commit` and
    `walk_history`. Whether that shared commit counts as pre- or
    post-cutoff is Chunk 6's own comparison logic (the exclusive
    reading); this fixture pins the raw material that comparison
    needs."""
    repo = _make_git_repo(tmp_path)
    template = repo / "dev" / "proposals" / "_template.md"
    template.parent.mkdir(parents=True)
    p = repo / "dev" / "proposals" / "p.md"
    template.write_text(f"marker: {events.VERSION_TOKEN}\n", encoding="utf-8")
    p.write_text(_artifact_text("revising", _fence(
        "transition", from_state="awaiting-review", to_state="revising")),
        encoding="utf-8")
    _commit_all(repo, "marker + act together")

    cutoff = events.activation_commit(repo, "dev/proposals/_template.md")
    result = events.walk_history(
        repo, "dev/proposals/p.md", valid_states=_PROPOSAL_STATES)
    assert len(result.events) == 1
    assert result.events[0].commit == cutoff


def test_two_commits_each_adding_one_block_get_distinct_stable_identities(
    tmp_path: Path,
) -> None:
    repo = _make_git_repo(tmp_path)
    p = repo / "p.md"
    p.write_text(_artifact_text("revising", _fence(
        "transition", from_state="awaiting-review", to_state="revising")),
        encoding="utf-8")
    _commit_all(repo, "c1: transition")
    result1 = events.walk_history(repo, "p.md", valid_states=_PROPOSAL_STATES)
    assert len(result1.events) == 1

    review_section = (
        "\n## Review -- Bob (External Reviewer) -- 2026-01-02\n\nfindings\n"
    )
    p.write_text(
        p.read_text(encoding="utf-8") + review_section
        + _fence("review-pass", tier="External", reviewer="Bob"),
        encoding="utf-8",
    )
    _commit_all(repo, "c2: review pass")
    result2 = events.walk_history(repo, "p.md", valid_states=_PROPOSAL_STATES)
    assert len(result2.events) == 2
    ids = [(e.commit, e.index) for e in result2.events]
    assert len(set(ids)) == 2, "two distinct commits must yield two distinct identities"
    assert result2.events[0].commit == result1.events[0].commit, (
        "the first identity is stable across the later commit"
    )
    assert result2.events[1].kind == "review-pass"
    assert result2.events[1].section_kind == "review"


def test_root_commit_introducing_a_block_is_attributed_not_refused(
    tmp_path: Path,
) -> None:
    """Step 5 refuses on AMBIGUOUS multi-parent attribution; a root
    commit has ZERO parents, which is not ambiguity -- its empty parent
    sequence is trivially a prefix of its own block sequence."""
    repo = _make_git_repo(tmp_path)
    p = repo / "p.md"
    p.write_text(_artifact_text("revising", _fence(
        "transition", from_state="awaiting-review", to_state="revising")),
        encoding="utf-8")
    _commit_all(repo, "root commit with a block")
    head = _head_sha(repo)

    r = subprocess.run(["git", "rev-list", "--parents", "-n", "1", head],
                        cwd=str(repo), capture_output=True, text=True, check=True)
    assert len(r.stdout.strip().split()) == 1, "fixture assumption: HEAD must be a root commit"

    result = events.walk_history(repo, "p.md", valid_states=_PROPOSAL_STATES)
    assert len(result.events) == 1
    assert result.events[0].commit == head


def test_uncommitted_edit_is_invisible_to_both_sides(tmp_path: Path) -> None:
    """The act list the reconciler checks is read from the same
    committed history it reads blocks from, not from the live
    working-copy file (EPR-15's resolution) -- an uncommitted lifecycle
    act is invisible to BOTH sides symmetrically, neither refused nor
    counted, until it is committed."""
    repo = _make_git_repo(tmp_path)
    p = repo / "p.md"
    p.write_text(_artifact_text("revising", _fence(
        "transition", from_state="awaiting-review", to_state="revising")),
        encoding="utf-8")
    _commit_all(repo, "c1")
    before = events.walk_history(repo, "p.md", valid_states=_PROPOSAL_STATES)
    assert len(before.events) == 1 and before.unmatched_acts == []

    # An uncommitted review-pass act, written to disk but never committed.
    p.write_text(
        p.read_text(encoding="utf-8")
        + "\n## Review -- Bob (External Reviewer) -- 2026-01-02\n\nfindings\n",
        encoding="utf-8",
    )
    during = events.walk_history(repo, "p.md", valid_states=_PROPOSAL_STATES)
    assert len(during.events) == 1 and during.unmatched_acts == [], (
        "an uncommitted act must be neither refused nor counted"
    )

    _commit_all(repo, "c2: commit the review act without its block")
    after = events.walk_history(repo, "p.md", valid_states=_PROPOSAL_STATES)
    assert len(after.events) == 1
    assert len(after.unmatched_acts) == 1
    assert after.unmatched_acts[0].kind == "review-pass"
