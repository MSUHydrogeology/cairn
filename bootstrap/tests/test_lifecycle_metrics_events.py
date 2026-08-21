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
#: The REAL installed location -- has a genuine `tools/lifecycle_planner.py`
#: sibling, unlike `_LM_PATH` above (the template source location, which
#: `_validated_planner_path()` deliberately refuses beside -- see that
#: function's own docstring). The row-level `extract_proposal_row`/
#: `extract_plan_row` fixtures below need REAL vocabulary resolution (a
#: plan's own `**Status**:` normalization already depended on it before
#: this plan's own Chunk 6 added a second, independent dependency for the
#: event grammar's `valid_states` bound), so they load through here
#: instead of `_lm`.  The scratch git repos those fixtures build are
#: unrelated to and never confused with this real, installed location:
#: vocabulary is a static, well-known status-token set, not project data.
_LM_INSTALLED_PATH = CAIRN_ROOT / "tools" / "lifecycle_metrics.py"


def _load_lm() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cairn_lm_events", _LM_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["cairn_lm_events"] = module
    spec.loader.exec_module(module)
    return module


def _load_lm_installed() -> ModuleType:
    # The launcher's own engine loader caches the ENGINE PACKAGE under the
    # fixed canonical name "tools._lifecycle_metrics" regardless of which
    # PHYSICAL location it was loaded from -- so if some other test module
    # in the same pytest session already loaded the template-source engine
    # under that same key (test_lifecycle_metrics_config.py's `_load_lm()`
    # does exactly that), the launcher's own cache check would silently
    # hand back that wrong-location engine instead of loading a fresh one
    # from `tools/`. Purge the canonical key (and any registered children)
    # first so this load is genuinely independent.
    canonical = "tools._lifecycle_metrics"
    prefix = canonical + "."
    for name in [n for n in list(sys.modules)
                 if n == canonical or n.startswith(prefix)]:
        sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location(
        "cairn_lm_events_installed", _LM_INSTALLED_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["cairn_lm_events_installed"] = module
    spec.loader.exec_module(module)
    return module


_lm = _load_lm()
_lm_installed = _load_lm_installed()
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


# ---------------------------------------------------------------------------
# Chunk 6 -- fail-closed reconciliation (`events.reconcile`), the mandatory
# red fixtures (Round 6 / R4-E1 / R4-E2) plus the pre/post-activation split.
# ---------------------------------------------------------------------------


def _make_activated_repo(tmp_path: Path) -> Path:
    """A repo whose `dev/proposals/_template.md` carries the marker,
    committed on its OWN, so every later commit touching a proposal is
    strictly after the cutoff (never co-committed with the marker's own
    introduction, which would make it pre-cutoff by the exclusive
    reading -- see `test_act_in_markers_own_introducing_commit_shares_that_commit`
    above)."""
    repo = _make_git_repo(tmp_path)
    template = repo / "dev" / "proposals" / "_template.md"
    template.parent.mkdir(parents=True)
    template.write_text(f"guidance mentioning {events.VERSION_TOKEN}\n", encoding="utf-8")
    _commit_all(repo, "activate")
    return repo


def test_status_only_commit_with_no_block_is_incomplete(tmp_path: Path) -> None:
    """A file's own CREATION commit is exempt (there is no prior state to
    declare a transition FROM -- see the `is_creation` exemption in
    `walk_history`); the mandatory red fixture is a SUBSEQUENT status
    flip with no block, which is the ordinary shape Round 6 / R4-E2
    names."""
    repo = _make_activated_repo(tmp_path)
    p = repo / "dev" / "proposals" / "p.md"
    p.write_text(_artifact_text("awaiting-review"), encoding="utf-8")
    _commit_all(repo, "open, no block needed (creation)")
    p.write_text(_artifact_text("revising"), encoding="utf-8")
    _commit_all(repo, "status flip, no block")
    result = events.reconcile(
        repo, "dev/proposals/p.md", valid_states=_PROPOSAL_STATES,
        template_relpath="dev/proposals/_template.md",
    )
    assert result.incomplete
    assert any("transition" in r for r in result.incomplete_reasons)


def test_review_only_commit_with_no_block_is_incomplete(tmp_path: Path) -> None:
    repo = _make_activated_repo(tmp_path)
    p = repo / "dev" / "proposals" / "p.md"
    p.write_text(
        _artifact_text("awaiting-review")
        + "\n## Review -- Bob (External Reviewer) -- 2026-01-02\n\nfindings\n",
        encoding="utf-8",
    )
    _commit_all(repo, "review, no block")
    result = events.reconcile(
        repo, "dev/proposals/p.md", valid_states=_PROPOSAL_STATES,
        template_relpath="dev/proposals/_template.md",
    )
    assert result.incomplete
    assert any("review-pass" in r for r in result.incomplete_reasons)


def test_two_review_commits_no_status_change_yield_two_review_pass_events(
    tmp_path: Path,
) -> None:
    """Round 6 / R4-E1's mandatory taxonomy fixture: two review commits
    with no intervening status change produce TWO review-pass events."""
    repo = _make_activated_repo(tmp_path)
    p = repo / "dev" / "proposals" / "p.md"
    p.write_text(_artifact_text("revising"), encoding="utf-8")
    _commit_all(repo, "open")
    p.write_text(
        p.read_text(encoding="utf-8")
        + "\n## Review -- Bob (External Reviewer) -- 2026-01-02\n\nfindings\n"
        + _fence("review-pass", tier="External", reviewer="Bob"),
        encoding="utf-8",
    )
    _commit_all(repo, "review 1")
    p.write_text(
        p.read_text(encoding="utf-8")
        + "\n## Review -- Alice (Internal Reviewer) -- 2026-01-03\n\nmore findings\n"
        + _fence("review-pass", tier="Internal", reviewer="Alice"),
        encoding="utf-8",
    )
    _commit_all(repo, "review 2")
    result = events.reconcile(
        repo, "dev/proposals/p.md", valid_states=_PROPOSAL_STATES,
        template_relpath="dev/proposals/_template.md",
    )
    assert not result.incomplete
    review_events = [e for e in result.post_cutoff_events if e.kind == "review-pass"]
    assert len(review_events) == 2
    assert {e.block.reviewer for e in review_events} == {"Bob", "Alice"}


def test_pre_and_post_activation_review_pass_split(tmp_path: Path) -> None:
    """Chunk 6's pre/post-activation split fixture: a review pass before
    the artifact's activation cutoff (no block -- correct, not an
    error) and one after (with a block -- reconciled, not INCOMPLETE)."""
    repo = _make_git_repo(tmp_path)
    p = repo / "dev" / "proposals" / "p.md"
    p.parent.mkdir(parents=True)
    p.write_text(
        _artifact_text("revising")
        + "\n## Review -- Bob (External Reviewer) -- 2026-01-01\n\nfindings\n",
        encoding="utf-8",
    )
    _commit_all(repo, "pre-cutoff review, no block, no marker yet")

    template = repo / "dev" / "proposals" / "_template.md"
    template.parent.mkdir(parents=True, exist_ok=True)
    template.write_text(f"guidance mentioning {events.VERSION_TOKEN}\n", encoding="utf-8")
    _commit_all(repo, "activate")

    p.write_text(
        p.read_text(encoding="utf-8")
        + "\n## Review -- Alice (Internal Reviewer) -- 2026-01-03\n\nmore\n"
        + _fence("review-pass", tier="Internal", reviewer="Alice"),
        encoding="utf-8",
    )
    _commit_all(repo, "post-cutoff review, with block")

    result = events.reconcile(
        repo, "dev/proposals/p.md", valid_states=_PROPOSAL_STATES,
        template_relpath="dev/proposals/_template.md",
    )
    assert not result.incomplete, (
        "the pre-cutoff review has no block, which is correct -- not an error"
    )
    assert len(result.post_cutoff_events) == 1
    assert result.post_cutoff_events[0].block.reviewer == "Alice"


# ---------------------------------------------------------------------------
# Row-level wiring: extract_proposal_row / extract_plan_row actually source
# their retained fields from the reconciliation layer above, end to end.
# ---------------------------------------------------------------------------


def test_extract_proposal_row_sources_review_fields_from_reconciled_blocks(
    tmp_path: Path,
) -> None:
    repo = _make_activated_repo(tmp_path)
    p = repo / "dev" / "proposals" / "p.md"
    p.write_text(
        "# t\n\n**Author**: Claude (Strategy)\n"
        "**Date opened**: 2026-01-01\n**Status**: revising\n",
        encoding="utf-8",
    )
    _commit_all(repo, "open")
    p.write_text(
        p.read_text(encoding="utf-8")
        + "\n## Review -- Bob (External Reviewer) -- 2026-01-02\n\nfindings\n"
        + _fence("review-pass", tier="External", reviewer="Bob"),
        encoding="utf-8",
    )
    _commit_all(repo, "review 1")
    p.write_text(
        p.read_text(encoding="utf-8")
        + "\n## Response -- Claude -- 2026-01-03\n\n* accept\n"
        + _fence("response", model="Claude Opus 5"),
        encoding="utf-8",
    )
    _commit_all(repo, "response")

    row = _lm_installed.extract_proposal_row(p, repo_root=repo)
    assert row["review_rounds"] == 1
    assert row["reviewer_agents"] == "Bob"
    assert row["external_tier_review"] is True
    assert row["cross_agent_type_review"] is True
    assert row["response_models"] == "Claude Opus 5"


def test_extract_proposal_row_emits_empty_for_pre_cutoff_review(
    tmp_path: Path,
) -> None:
    """The one real, confirmed change EPR-06/row 7-3 names: a review-pass
    act that cannot be proven post-cutoff emits the literal `''`, never
    the retired heading-count value."""
    repo = _make_git_repo(tmp_path)
    p = repo / "dev" / "proposals" / "p.md"
    p.parent.mkdir(parents=True)
    p.write_text(
        "# t\n\n**Author**: Claude (Strategy)\n"
        "**Date opened**: 2026-01-01\n**Status**: revising\n"
        "\n## Review -- Bob (External Reviewer) -- 2026-01-02\n\nfindings\n",
        encoding="utf-8",
    )
    _commit_all(repo, "open + review, no marker anywhere")

    row = _lm_installed.extract_proposal_row(p, repo_root=repo)
    assert row["review_rounds"] == ""
    assert row["reviewer_agents"] == ""
    assert row["external_tier_review"] == ""
    assert row["cross_agent_type_review"] == ""
    assert row["response_models"] == ""


def test_extract_plan_row_sources_plan_and_code_review_rounds_separately(
    tmp_path: Path,
) -> None:
    """Rows 6-9..6-12: `plan_review_rounds`/`code_review_rounds` are
    reconciled-block-derived post-cutoff, classified by the matched
    HEADING (Plan review vs. Code review), not the block's own `tier`."""
    repo = _make_git_repo(tmp_path)
    template = repo / "dev" / "plans" / "_template.md"
    template.parent.mkdir(parents=True)
    template.write_text(f"guidance mentioning {events.VERSION_TOKEN}\n", encoding="utf-8")
    _commit_all(repo, "activate")

    p = repo / "dev" / "plans" / "myplan.md"
    p.write_text(
        "# myplan\n\n**Status**: revising-plan\n\n## Scope\n\nx\n",
        encoding="utf-8",
    )
    _commit_all(repo, "open plan")
    p.write_text(
        p.read_text(encoding="utf-8")
        + "\n## Plan review -- Bob -- 2026-01-02\n\nfindings\n"
        + _fence("review-pass", tier="Internal", reviewer="Bob"),
        encoding="utf-8",
    )
    _commit_all(repo, "plan review")
    p.write_text(
        p.read_text(encoding="utf-8")
        + "\n## Code review -- Alice -- 2026-01-04\n\nfindings\n"
        + _fence("review-pass", tier="Internal", reviewer="Alice"),
        encoding="utf-8",
    )
    _commit_all(repo, "code review")

    row = _lm_installed.extract_plan_row(p, repo_root=repo)
    assert row["plan_review_rounds"] == 1
    assert row["code_review_rounds"] == 1


def test_extract_plan_row_emits_empty_for_never_activated_tree(
    tmp_path: Path,
) -> None:
    repo = _make_git_repo(tmp_path)
    p = repo / "dev" / "plans" / "myplan.md"
    p.parent.mkdir(parents=True)
    p.write_text(
        "# myplan\n\n**Status**: revising-plan\n\n"
        "## Plan review -- Bob -- 2026-01-02\n\nfindings\n",
        encoding="utf-8",
    )
    _commit_all(repo, "open + plan review, no marker at all")

    row = _lm_installed.extract_plan_row(p, repo_root=repo)
    assert row["plan_review_rounds"] == ""
    assert row["code_review_rounds"] == ""


# ---------------------------------------------------------------------------
# Chunk 7 -- cross-cutting fixtures (rows 7-1, 7-2)
# ---------------------------------------------------------------------------


def test_cross_commit_contamination_is_structurally_unrepresentable(
    tmp_path: Path,
) -> None:
    """The R3-E1 property, re-expressed for the artifact-local design per
    Round 5 SS2: two artifacts transitioned concurrently, one commit
    path-scoped to the first artifact only, and the second artifact's
    block does not and cannot appear in that commit -- because there is
    no shared file for it to appear in. A confirmation of a STRUCTURAL
    property (git commits are per-path diffs; a path-scoped commit
    cannot touch a second file's content), not a vulnerability
    regression test -- it would still hold with events.py deleted
    entirely, since the property belongs to git and path-scoped commits,
    not to this reader's own logic. Writing it is still required
    (Round 5); it does not itself enforce the property."""
    repo = _make_git_repo(tmp_path)
    (repo / "dev" / "proposals").mkdir(parents=True)
    a = repo / "dev" / "proposals" / "a.md"
    b = repo / "dev" / "proposals" / "b.md"
    a.write_text(_artifact_text("awaiting-review"), encoding="utf-8")
    b.write_text(_artifact_text("awaiting-review"), encoding="utf-8")
    _commit_all(repo, "open both")

    # Transition BOTH artifacts "concurrently" in the working tree, but
    # commit them in two path-scoped commits -- exactly the discipline
    # AGENTS.md itself prescribes (`git commit <paths>`).
    a.write_text(_artifact_text("revising", _fence(
        "transition", from_state="awaiting-review", to_state="revising")),
        encoding="utf-8")
    b.write_text(_artifact_text("revising", _fence(
        "transition", from_state="awaiting-review", to_state="revising")),
        encoding="utf-8")
    _git(["add", "dev/proposals/a.md"], repo)
    _git(["commit", "-q", "-m", "a: transition only"], repo)
    a_only_commit = _head_sha(repo)
    _git(["add", "dev/proposals/b.md"], repo)
    _git(["commit", "-q", "-m", "b: transition only"], repo)

    result_a = events.walk_history(repo, "dev/proposals/a.md", valid_states=_PROPOSAL_STATES)
    result_b = events.walk_history(repo, "dev/proposals/b.md", valid_states=_PROPOSAL_STATES)
    assert len(result_a.events) == 1
    assert len(result_b.events) == 1
    # b's block is attributed to a LATER, DISTINCT commit -- it was
    # structurally impossible for it to land in a's path-scoped commit.
    assert result_a.events[0].commit == a_only_commit
    assert result_b.events[0].commit != a_only_commit


def test_recorded_by_never_affects_identity_reconciliation_or_refusal(
    tmp_path: Path,
) -> None:
    """Round 7's explicit bar: `recorded_by` is informational only,
    barred from authority, identity, and idempotency. A forged or
    duplicated value changes no identity, no reconciliation outcome, and
    no refusal disposition."""
    repo = _make_git_repo(tmp_path)
    p = repo / "p.md"
    p.write_text(
        "# proposal p -- padding text so this file's content is not "
        "near-identical to q.md's, which would make git's own --follow "
        "rename-similarity heuristic misattribute q's creation as a "
        "rename FROM p (a real git behavior discovered while building "
        "this fixture, not a defect in the reader under test)\n\n"
        + _artifact_text("revising", _fence(
            "transition", from_state="awaiting-review", to_state="revising",
            recorded_by="Someone Else Entirely",
        )),
        encoding="utf-8",
    )
    _commit_all(repo, "c1: transition, forged recorded_by")

    without = events.walk_history(repo, "p.md", valid_states=_PROPOSAL_STATES)
    assert len(without.events) == 1
    identity_with_forged = (without.events[0].commit, without.events[0].index)

    # A second, UNRELATED artifact -- deliberately distinct padding text
    # from p.md's (see the comment on p.md's own content above) -- with a
    # DUPLICATED recorded_by value shared across two otherwise-independent
    # blocks. Still no effect on identity or reconciliation outcome.
    q = repo / "q.md"
    q.write_text(
        "# proposal q -- an entirely different document from p.md, on "
        "purpose\n\n"
        + _artifact_text("revising", _fence(
            "transition", from_state="awaiting-review", to_state="revising",
            recorded_by="Duplicate Name",
        )),
        encoding="utf-8",
    )
    _commit_all(repo, "c2: q transition, duplicate recorded_by")
    q.write_text(
        q.read_text(encoding="utf-8")
        + "\n## Review -- Bob (External Reviewer) -- 2026-01-02\n\nfindings\n"
        + _fence("review-pass", tier="External", reviewer="Bob", recorded_by="Duplicate Name"),
        encoding="utf-8",
    )
    _commit_all(repo, "c3: q review, same duplicate recorded_by")

    result_q = events.walk_history(repo, "q.md", valid_states=_PROPOSAL_STATES)
    assert len(result_q.events) == 2
    assert result_q.unmatched_acts == []
    # Identity is (commit, index) -- recorded_by is not a component of
    # either, confirmed by re-deriving p's identity unchanged.
    again = events.walk_history(repo, "p.md", valid_states=_PROPOSAL_STATES)
    assert (again.events[0].commit, again.events[0].index) == identity_with_forged


def test_cli_exits_nonzero_and_names_the_unreconciled_artifact(
    tmp_path: Path, capsys: pytest.CaptureFixture,
) -> None:
    """Row 6-3's own acceptance, end to end through the CLI: a report run
    against a fixture tree containing a deliberately unreconciled act
    exits nonzero and names which artifact/commit/kind failed to
    reconcile -- never a shorter, silently-clean series."""
    repo = _make_activated_repo(tmp_path)
    p = repo / "dev" / "proposals" / "p.md"
    p.write_text(_artifact_text("awaiting-review"), encoding="utf-8")
    _commit_all(repo, "open")
    p.write_text(
        p.read_text(encoding="utf-8")
        + "\n## Review -- Bob (External Reviewer) -- 2026-01-02\n\nfindings\n",
        encoding="utf-8",
    )
    _commit_all(repo, "review, deliberately no block -- post-cutoff")

    rc = _lm_installed.main(["proposals", "--root", str(repo)])
    captured = capsys.readouterr()
    assert rc == _lm_installed.cli.EXIT_INCOMPLETE
    assert "INCOMPLETE" in captured.err
    assert "p.md" in captured.err
    assert "review-pass" in captured.err
