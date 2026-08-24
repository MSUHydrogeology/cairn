"""Fixtures for the review-pass heading grammar (retire-event-blocks,
2026-08-24), which replaced the deleted `cairn-event-v1` block / history-
diff / reconciliation machinery (`metrics-events-not-prose` Parts 3,
Chunks 4-7).

Loaded through the installed launcher facade
(`templates/modules/default-on/lifecycle_metrics.py`), the same surface an
adopter imports -- consistent with the other `bootstrap/tests/test_lifecycle_*`
files. This file's collection stays at the SAME COLLECTION size the retired
event-block content set (retained-plus-fixture-oracle replaces
reconciliation-and-history-walk node for node); the gate manifest sees
CONTENT-CHANGED nodes, not new collection.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Dict, List

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
_LM_PATH = CAIRN_ROOT / "templates" / "modules" / "default-on" / "lifecycle_metrics.py"
#: The REAL installed location -- has a genuine `tools/lifecycle_planner.py`
#: sibling, unlike `_LM_PATH` above (the template source location, which
#: `_validated_planner_path()` deliberately refuses beside -- see that
#: function's own docstring). `extract_plan_row` reads a plan's `**Status**:`
#: through the real vocabulary loader, so plan-row fixtures load through
#: here instead of `_lm`; proposal-row fixtures need no vocabulary at all
#: (review-pass sourcing is now a pure text read) and load through `_lm`.
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


def _proposal_row(text: str, tmp_path: Path) -> Dict[str, object]:
    """`extract_proposal_row` over synthetic `text`, pure-logic (no git)."""
    p = tmp_path / "p.md"
    p.write_text(text, encoding="utf-8")
    return _lm.extract_proposal_row(p, include_git_timestamps=False)


def _plan_row(text: str, tmp_path: Path) -> Dict[str, object]:
    """`extract_plan_row` over synthetic `text`, through the installed
    engine (needs the real planner sibling for `**Status**:` normalization;
    review-pass sourcing itself is git-free either way)."""
    p = tmp_path / "p.md"
    p.write_text(text, encoding="utf-8")
    return _lm_installed.extract_plan_row(p, include_git_timestamps=False)


_HEADER = (
    "# t\n\n**Author**: Claude (Strategy)\n"
    "**Date opened**: 2026-01-01\n**Status**: revising\n\n"
)


# ---------------------------------------------------------------------------
# Fixture oracle -- named artifacts, expected per-artifact counts for all
# seven review-pass-sourced columns (RTE-03 / S2's own acceptance: an
# aggregate population table is a readable consequence, not the check).
# ---------------------------------------------------------------------------


def test_single_review_one_reviewer_external_tier(tmp_path: Path) -> None:
    """One dated `## Review` pass, one reviewer, an External tier line, one
    Response with a Model field -- the baseline shape most proposals in
    Cairn's own corpus carry."""
    text = (
        _HEADER
        + "## Review -- Codex (External) -- 2026-01-05\n\n"
        "**Tier**: External\n\n"
        "findings.\n\n"
        "## Response -- Claude -- 2026-01-06\n\n"
        "**Model**: claude-opus-5\n\n"
        "accepted.\n"
    )
    row = _proposal_row(text, tmp_path)
    assert row["review_rounds"] == 1
    assert row["reviewer_agents"] == "Codex"
    # One distinct reviewer identity is not "two or more" -- blank, not
    # True: review having happened at all is what review_rounds reports.
    assert row["cross_agent_type_review"] == ""
    assert row["external_tier_review"] is True
    assert row["response_models"] == "claude-opus-5"


def test_two_distinct_reviewers_flip_cross_agent_type(tmp_path: Path) -> None:
    """Two DIFFERENT reviewer identities across accepted passes -- the
    condition `cross_agent_type_review` actually claims."""
    text = (
        _HEADER
        + "## Review -- Codex (External) -- 2026-01-05\n\n"
        "**Tier**: External\n\nfindings.\n\n"
        "## Review -- Gemini (External) -- 2026-01-07\n\n"
        "**Tier**: External\n\nfindings, round 2.\n"
    )
    row = _proposal_row(text, tmp_path)
    assert row["review_rounds"] == 2
    assert row["reviewer_agents"] == "Codex|Gemini"
    assert row["cross_agent_type_review"] is True
    assert row["external_tier_review"] is True


def test_same_reviewer_twice_stays_blank_not_true(tmp_path: Path) -> None:
    """The same reviewer identity across multiple rounds does NOT flip
    `cross_agent_type_review` -- this is the semantic this column changed
    under retire-event-blocks (previously: reviewer-differs-from-author;
    now: two-or-more-distinct-reviewers), pinned directly rather than left
    to be discovered by a stale assumption."""
    text = (
        _HEADER
        + "## Review -- Codex (External) -- 2026-01-05\n\n"
        "**Tier**: External\n\nfindings.\n\n"
        "## Review -- Codex (External) -- 2026-01-09 (round 2)\n\n"
        "**Tier**: External\n\nfindings, round 2.\n"
    )
    row = _proposal_row(text, tmp_path)
    assert row["review_rounds"] == 2
    assert row["reviewer_agents"] == "Codex"
    assert row["cross_agent_type_review"] == ""


def test_bare_template_stub_is_not_a_pass(tmp_path: Path) -> None:
    """A `## Review` heading with no ` -- ` and no date -- the installed
    template's own unfilled section -- is not a pass. 9 of 46 plans in
    Cairn's own corpus carry exactly this shape for `## Code review`."""
    text = _HEADER + "## Review\n\n<fill in reviewer, tier, findings>\n"
    row = _proposal_row(text, tmp_path)
    assert row["review_rounds"] == ""
    assert row["reviewer_agents"] == ""
    assert row["cross_agent_type_review"] == ""
    assert row["external_tier_review"] == ""


def test_disposition_heading_is_excluded_by_name(tmp_path: Path) -> None:
    """A Maintainer `disposition` about a pass is not itself a pass, even
    though it otherwise matches the grammar in full (kind word, ` -- `,
    date) -- Cairn's own corpus carries exactly this trap:
    `## Security review disposition -- Anthony Kendall (Maintainer) --
    2026-08-20`."""
    text = (
        _HEADER
        + "## Review disposition -- Anthony Kendall (Maintainer) -- 2026-01-05\n\n"
        "**Tier**: External\n\nruling.\n"
    )
    row = _proposal_row(text, tmp_path)
    assert row["review_rounds"] == ""
    assert row["reviewer_agents"] == ""
    assert row["external_tier_review"] == ""


def test_response_heading_is_not_a_pass_but_feeds_response_models(
    tmp_path: Path,
) -> None:
    """`## Response ...` never matches the pass kind group (its own first
    word is 'Response', not one of the five kinds) -- structurally
    excluded, not name-checked -- but its `**Model**:` field still
    populates `response_models` independent of any pass existing."""
    text = (
        _HEADER
        + "## Response to review -- Claude -- 2026-01-06\n\n"
        "**Model**: claude-opus-5\n\naccepted.\n"
    )
    row = _proposal_row(text, tmp_path)
    assert row["review_rounds"] == ""
    assert row["reviewer_agents"] == ""
    assert row["response_models"] == "claude-opus-5"


def test_correction_heading_is_not_a_pass(tmp_path: Path) -> None:
    """`## Correction to ...` never matches the pass kind group either,
    for the same structural reason as Response -- its own first word is
    'Correction'."""
    text = (
        _HEADER
        + "## Correction to the Security review disposition -- Claude -- 2026-01-07\n\n"
        "**Tier**: External\n\ncorrected.\n"
    )
    row = _proposal_row(text, tmp_path)
    assert row["review_rounds"] == ""
    assert row["reviewer_agents"] == ""
    assert row["external_tier_review"] == ""


def test_h3_or_deeper_review_heading_is_never_a_pass(tmp_path: Path) -> None:
    """`_split_h2_sections` only ever offers an H2 line as a section
    header, so an H3-or-deeper 'Review'-shaped heading is structurally
    invisible to the pass reader, never counted."""
    text = (
        _HEADER
        + "## Findings\n\n"
        "### Review -- Codex (External) -- 2026-01-05\n\n"
        "**Tier**: External\n\nnested, not a real pass.\n"
    )
    row = _proposal_row(text, tmp_path)
    assert row["review_rounds"] == ""
    assert row["reviewer_agents"] == ""


def test_quoted_example_inside_a_fence_is_never_a_pass(tmp_path: Path) -> None:
    """A worked example of the heading grammar, quoted verbatim inside a
    fenced code block while discussing it, is not a live pass -- Cairn's
    own `2026-08-10-claude-code-review-blindness` is exactly this shape:
    it quotes `## Code review -- Independent Human -- 2026-08-10` and
    `## Plan review -- Jane (Lab) Smith -- 2026-08-10` as illustrative
    examples while arguing a gate defect, and only its own real `##
    Review -- Codex -- ...` passes are genuine."""
    text = (
        _HEADER
        + "## Review -- Codex (External) -- 2026-01-05\n\n"
        "**Tier**: External\n\nfindings.\n\n"
        "## Context\n\n"
        "Reproduced directly:\n\n"
        "```\n"
        "## Code review -- Independent Human -- 2026-01-06\n\n"
        "**Tier**: External\n"
        "```\n\n"
        "discussion continues.\n"
    )
    row = _proposal_row(text, tmp_path)
    assert row["review_rounds"] == 1
    assert row["reviewer_agents"] == "Codex"
    assert "Independent Human" not in row["reviewer_agents"]


def test_proposal_hosted_code_review_pass_feeds_reviewer_agents_not_review_rounds(
    tmp_path: Path,
) -> None:
    """A real, dated `## Code review` pass recorded directly in a proposal
    (Cairn's own corpus carries this, e.g.
    `2026-08-11-claude-intent-ledger-pruning`) is a genuine accepted pass
    -- it populates `reviewer_agents`/`external_tier_review` -- but is not
    the bare `## Review` kind `review_rounds` counts, by the accepted
    grammar's own per-column definition."""
    text = (
        _HEADER
        + "## Code review -- Codex (External) -- 2026-01-05\n\n"
        "**Tier**: External\n\nverdict.\n"
    )
    row = _proposal_row(text, tmp_path)
    assert row["review_rounds"] == ""
    assert row["reviewer_agents"] == "Codex"
    assert row["external_tier_review"] is True


def test_internal_and_unknown_tier_values(tmp_path: Path) -> None:
    """`external_tier_review` is a genuine three-state read of the free-
    text `**Tier**:` field: True when an accepted pass's tier starts with
    'External', False when the best evidence is 'Internal', and
    ``'unknown'`` when a tier line exists but names neither."""
    internal_only = _proposal_row(
        _HEADER + "## Review -- Claude -- 2026-01-05\n\n"
        "**Tier**: Internal, same agent type as the author\n\nfindings.\n",
        tmp_path,
    )
    assert internal_only["external_tier_review"] is False

    unknown_tier = _proposal_row(
        _HEADER + "## Security review -- Codex -- 2026-01-05\n\n"
        "**Tier**: Security\n\nfindings.\n",
        tmp_path,
    )
    assert unknown_tier["external_tier_review"] == "unknown"


def test_plan_review_and_code_review_counted_separately(tmp_path: Path) -> None:
    """Cairn's own corpus baseline: a plan with one dated `## Plan
    review` pass and one dated `## Code review` pass counts each in its
    own column."""
    text = (
        "# t\n\n**Status**: archived\n\n"
        "## Plan review -- Claude (Internal) -- 2026-01-05\n\n"
        "**Tier**: Internal\n\nfindings.\n\n"
        "## Code review -- Codex (External) -- 2026-01-08\n\n"
        "**Tier**: External\n\nverdict.\n"
    )
    row = _plan_row(text, tmp_path)
    assert row["plan_review_rounds"] == 1
    assert row["code_review_rounds"] == 1


def test_plan_with_only_bare_stubs_is_blank_in_both_columns(tmp_path: Path) -> None:
    """Cairn's own corpus carries 9 plans with exactly this shape: both
    section headers present, neither carrying ` -- `/a date."""
    text = (
        "# t\n\n**Status**: archived\n\n"
        "## Plan review\n\n<fill in>\n\n"
        "## Code review\n\n<fill in>\n"
    )
    row = _plan_row(text, tmp_path)
    assert row["plan_review_rounds"] == ""
    assert row["code_review_rounds"] == ""


def test_plan_hosted_security_review_counts_toward_neither_column(
    tmp_path: Path,
) -> None:
    """A dated `## Security review` pass on a plan is grammatically legal
    but is neither `## Plan review` nor `## Code review` -- the accepted
    grammar's per-kind definition leaves it out of both counts."""
    text = (
        "# t\n\n**Status**: archived\n\n"
        "## Security review -- Codex (External Security) -- 2026-01-05\n\n"
        "**Tier**: External\n\nfindings.\n"
    )
    row = _plan_row(text, tmp_path)
    assert row["plan_review_rounds"] == ""
    assert row["code_review_rounds"] == ""


# ---------------------------------------------------------------------------
# S2 directed mutations -- each REQUIRED RED: a text transformation that
# must move the observed column in the stated direction.  Copied verbatim
# from the accepted proposal's security preflight (RTE-05, S2).
# ---------------------------------------------------------------------------


def test_mutation_1_stripping_the_date_drops_the_count(tmp_path: Path) -> None:
    dated = _HEADER + "## Review -- Codex (External) -- 2026-01-05\n\nfindings.\n"
    undated = _HEADER + "## Review -- Codex (External)\n\nfindings.\n"
    before = _proposal_row(dated, tmp_path)
    after = _proposal_row(undated, tmp_path)
    assert before["review_rounds"] == 1
    assert after["review_rounds"] == ""


def test_mutation_2_adding_a_bare_stub_does_not_raise_the_count(
    tmp_path: Path,
) -> None:
    text = (
        "# t\n\n**Status**: archived\n\n"
        "## Plan review -- Claude (Internal) -- 2026-01-05\n\n"
        "**Tier**: Internal\n\nfindings.\n"
    )
    text_plus_stub = text + "\n## Code review\n\n<fill in>\n"
    before = _plan_row(text, tmp_path)
    after = _plan_row(text_plus_stub, tmp_path)
    assert before["code_review_rounds"] == ""
    assert after["code_review_rounds"] == ""
    assert before["plan_review_rounds"] == after["plan_review_rounds"] == 1


def test_mutation_3_renaming_to_a_disposition_does_not_raise_the_count(
    tmp_path: Path,
) -> None:
    would_be_pass = (
        _HEADER + "## Review -- Anthony Kendall (Maintainer) -- 2026-01-05\n\n"
        "**Tier**: External\n\nruling.\n"
    )
    actual_disposition = (
        _HEADER + "## Review disposition -- Anthony Kendall (Maintainer) -- 2026-01-05\n\n"
        "**Tier**: External\n\nruling.\n"
    )
    before = _proposal_row(would_be_pass, tmp_path)
    after = _proposal_row(actual_disposition, tmp_path)
    assert before["review_rounds"] == 1
    assert after["review_rounds"] == ""


def test_mutation_4_a_second_distinct_reviewer_flips_cross_agent_type(
    tmp_path: Path,
) -> None:
    one_reviewer = (
        _HEADER + "## Review -- Codex (External) -- 2026-01-05\n\nfindings.\n"
    )
    two_reviewers = one_reviewer + (
        "\n## Review -- Gemini (External) -- 2026-01-09 (round 2)\n\nfindings.\n"
    )
    before = _proposal_row(one_reviewer, tmp_path)
    after = _proposal_row(two_reviewers, tmp_path)
    assert before["cross_agent_type_review"] == ""
    assert after["cross_agent_type_review"] is True


def test_mutation_5_removing_the_tier_line_clears_external_tier_review(
    tmp_path: Path,
) -> None:
    with_tier = (
        _HEADER + "## Review -- Codex (External) -- 2026-01-05\n\n"
        "**Tier**: External\n\nfindings.\n"
    )
    without_tier = (
        _HEADER + "## Review -- Codex (External) -- 2026-01-05\n\nfindings.\n"
    )
    before = _proposal_row(with_tier, tmp_path)
    after = _proposal_row(without_tier, tmp_path)
    assert before["external_tier_review"] is True
    assert after["external_tier_review"] == ""


# ---------------------------------------------------------------------------
# The never-refuse property outlives the mechanism it was written against.
# ---------------------------------------------------------------------------


def test_an_unreconciled_act_empties_its_own_fields_and_never_refuses_the_run(
    tmp_path: Path, capsys: pytest.CaptureFixture,
) -> None:
    """A measurement reports what it can and leaves the rest blank. It
    never refuses -- not on an ordinary artifact, and not on a heading
    that only partially matches the accepted grammar.

    This property was written against the deleted `cairn-event-v1`
    reconciler, where an act with no matching event block took the whole
    run's exit code with it (fixed 2026-08-21, `8416d9d`). The heading
    reader that replaced the reconciler has no exception type to raise in
    the first place -- an unparseable or partial heading is simply not
    counted -- but the property this test pins (every row still renders;
    the process still exits 0; nothing about a hard-to-parse artifact
    escalates into a refusal for the whole corpus) is the one the
    Decision named as outliving the mechanism, so it is re-aimed at the
    heading reader rather than dropped."""
    proposals_dir = tmp_path / "dev" / "proposals"
    proposals_dir.mkdir(parents=True)
    # Adversarial but not malformed at the OS/encoding level: an em-dash
    # separator instead of the accepted ` -- `, a heading missing its
    # second separator, and a non-ASCII reviewer name -- none of it is a
    # dated pass under the accepted grammar, and none of it may raise.
    (proposals_dir / "p.md").write_text(
        "# t\n\n**Author**: Claude (Strategy)\n"
        "**Date opened**: 2026-01-01\n**Status**: revising\n\n"
        "## Review — Bob — 2026-01-02\n\nfindings.\n\n"
        "## Review -- Étoile\n\nno second separator, no date.\n",
        encoding="utf-8",
    )
    rc = _lm_installed.main(["proposals", "--root", str(tmp_path)])
    captured = capsys.readouterr()
    assert rc == 0
    assert "INCOMPLETE" not in captured.err
    # The row still renders -- being unmeasurable is not being invisible.
    assert "revising" in captured.out
    assert len(captured.out.strip().splitlines()) == 2  # header + one row
