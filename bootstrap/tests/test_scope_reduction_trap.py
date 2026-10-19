"""The scope-reduction trap must reach the adopter, not only the doctrine.

`doctrine/dual-review.md` holds the canonical rule, but `doctrine/` is **not
installed into an adopter tree** -- a rule that lives only there binds nobody
who adopts Cairn. The operational form therefore has to sit on the surfaces an
adopter actually receives: the governing `AGENTS.md`, the review-loop doc, the
proposal and plan templates, the board's disposition taxonomy, the team-gated
dual-review module, and the planner scaffolds an author reads while typing.

This module asserts that parity. It checks for the load-bearing *obligations*
rather than one exact sentence, so a rewording that preserves the obligation
passes and a deletion fails. Whitespace is normalized before matching, because
the obligations wrap across lines differently in each surface and a
newline-sensitive pattern would be testing the line width rather than the rule.

**What it deliberately does not test.** It does not test that a `Scope delta`
declaration is *truthful*. That property is semantic, the planner gate was
declined for exactly that reason (source proposal, Round 3), and the last test
in this module pins the *absence* of that gate so a later well-meaning change
does not quietly add it.

Source: `dev/plans/archive/scope-reduction-trap.md` (Chunk E), executing
`dev/proposals/archive/2026-08-11-claude-scope-reduction-trap.md`.

Run from the Cairn repo root:
    python -m pytest bootstrap/tests/test_scope_reduction_trap.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))


#: Each entry: surface -> {obligation label: alternation pattern}.
#:
#: Pairs are listed together where both copies must carry the same obligation:
#: the shipped `templates/` copy is the load-bearing one (adopters receive it),
#: and Cairn's own copy keeps Cairn bound by the rule it ships.
_GOVERNING = {
    "removing accepted scope is a deviation":
        r"accepted scope removed|removing accepted scope",
    "accepted scope is a floor":
        r"[Aa]ccepted scope is a \*{0,2}floor",
    "a reviewer cannot self-authorize the removal":
        r"cannot create that authority",
}

_REVIEW_LOOP = {
    # A review deleted the reviewer-duty and specify-default
    # sentences from BOTH copies and saw 105 green, because neither obligation
    # was named here. `names the trap` was additionally satisfied by the
    # trailing `doctrine/dual-review.md` citation alone, so the paragraph could
    # go while the pointer to it stayed.
    "names the trap in its own prose, not only in a citation":
        r"mirror: the scope-reduction trap|scope-reduction trap\.\*\*",
    "the reviewer must state what is lost and why the rest still reaches":
        r"what is\s+lost.{0,120}reaches the cause",
    "specify by default; say why if you cut instead":
        r"why specifying it was rejected|resolves an \*?underspecified\*? "
        r"finding by removing",
    "the test is bound to the baseline artifact, both stages":
        r"as opened.{0,120}as accepted",
    "preserved owes nothing":
        r"every baseline outcome is still delivered|nothing is owed",
    "only the Maintainer may concede a baseline outcome":
        r"neither author nor reviewer may concede|only the Maintainer may "
        r"concede|the \*{0,2}Maintainer'?.{0,4}s?\*{0,2} explicit allowance",
    "declining a reviewer's expansion is not a reduction":
        r"never in the baseline",
}

_PROPOSAL_TEMPLATE = {
    "carries the declaration":
        r"\*\*Scope delta\*\*",
    "baseline is the scope as opened":
        r"scope as opened",
    "the remainder is one grouped record":
        r"[Oo]ne grouped record|grouped remainder|Removed scope",
    "neither author nor reviewer may concede":
        r"neither may concede|may concede a baseline outcome",
    "declining a proposed expansion is not a reduction":
        r"proposed expansion is not a reduction|never in the baseline",
    "specify rather than cut, and say why if you cut":
        r"why specifying was rejected|why specifying it was rejected",
}

_PLAN_TEMPLATE = {
    "carries the declaration":
        r"\*\*Scope delta\*\*",
    "accepted scope is a floor":
        r"[Aa]ccepted scope is a \*{0,2}(FLOOR|floor)",
    "sequencing between chunks owes nothing":
        r"[Ss]equencing is free|moving work between chunks|Sequencing between "
        r"chunks owes nothing",
    "baseline is the scope as accepted":
        r"AS ACCEPTED|scope as accepted",
    "a reviewer cannot self-authorize the removal":
        r"cannot create that authority",
    # A later pass added the floor rule to the `## Scope` fence,
    # where plan-open happens. The whole paragraph was deletable and stayed
    # green -- the pre-existing plan-review comment matched the same patterns.
    # This one is specific to the fence's own framing.
    "the fence bounds this pass, not the accepted proposal":
        r"fence bounds this pass",
}

_BOARD_TAXONOMY = {
    "a scope-cut removes no work":
        r"scope-cut removes no work|scope-cut is claim correction",
    "removing work is a scope reduction instead":
        r"is a \*{0,2}scope reduction",
    # R2-E1: the authority rule. Without this the shipped board could lose
    # its self-contained statement and stay green -- demonstrated by the
    # a code review, which cut exactly that text and saw 51 passed.
    "only the Maintainer may concede a baseline outcome":
        r"only the Maintainer may concede|[Nn]either author nor reviewer may "
        r"concede",
    # The satisfier had two halves and only the authority
    # half landed. Each of these could be deleted from the shipped board while
    # the suite stayed green.
    "the baseline is the artifact's own commitments, both stages":
        r"as \*?opened\*?.{0,80}as \*?accepted\*?|outcome test in",
    "the remainder is one grouped record per source artifact":
        r"grouped\s+scope-remainder record",
}

#: The canonical rule requires each remainder entry to
#: carry FOUR things -- source section, reason, **a disposition**, and a revival
#: or closure condition. All four templates and both emitted scaffolds asked for
#: three, plus a group-level `Disposition/home` naming only a location. A home
#: is not a disposition, and `doctrine/lifecycle.md` blocks archive on each
#: entry independently, so the distributed record could not satisfy the gate it
#: was written to feed.
_PER_ENTRY_DISPOSITION_SURFACES = (
    "dev/proposals/_template.md",
    "templates/core/dev/proposals/_template.md",
    "dev/plans/_template.md",
    "templates/core/dev/plans/_template.md",
)


@pytest.mark.parametrize("rel", _PER_ENTRY_DISPOSITION_SURFACES)
def test_each_remainder_entry_asks_for_its_own_disposition(rel: str) -> None:
    text = _normalized(rel)
    assert re.search(r"disposition\*{0,2}:?\s*\(?<?accept", text), (
        f"{rel} no longer asks each removed unit for its own disposition. A "
        f"group-level home is a location, not a decision, and each entry blocks "
        f"archive independently -- an author following this shape would produce "
        f"a record that cannot satisfy the archive precondition."
    )


_DOCTRINE_CANONICAL = {
    "states the asymmetry that makes narrowing cheap":
        r"costs the reviewer nothing|never be shown wrong",
    "the reviewer must say what is lost":
        r"states \*{0,2}what is lost",
    "specify is the default, cutting must argue":
        r"[Dd]efault resolution is to specify|why specifying was rejected",
    "carries all three outcome values":
        r"preserved.{0,400}degraded.{0,200}lost",
    "the baseline is the artifact's own commitments, both stages":
        r"as opened.{0,120}as accepted",
    "the comparison term is not written by the narrowing party":
        r"never a summary of its purpose written afterwards|party being tested",
    "degraded and lost take the same authority path":
        r"[Dd]egraded and lost take the same path|never \*{0,2}who may concede",
    "a review-proposed stronger outcome is not in the baseline":
        r"not in the baseline",
    "the grouped remainder blocks archive":
        r"blocks\*{0,2}\s*\*{0,2}archive",
    # Codex deleted the words "a disposition" from this sentence and the whole
    # suite stayed green. It is the source every
    # author-facing shape derives from.
    "each entry carries four things, including a disposition":
        r"source section, the reason, a disposition, and a revival",
    "the counterweight against reading this as anti-restraint":
        r"[Cc]ut ceremony.{0,20}[Dd]o not cut reach",
    "states why it is not mechanized":
        r"could not confirm that it is \*{0,2}true|cannot establish semantic "
        r"truth|catch forgetting and not evading",
}

_DOCTRINE_PROPOSALS = {
    "pre-Decision baseline is the scope as opened":
        r"baseline is the scope as opened",
    "carries the declaration":
        r"\*\*Scope delta\*\*",
    "requires the grouped remainder and a named home":
        r"one record|Disposition/home",
    "the Maintainer allows the loss via the Decision":
        r"[Nn]either may concede|Maintainer, via the Decision",
    "declining a reviewer's expansion is not a reduction":
        r"not a reduction",
}

_DOCTRINE_PLANS = {
    # NOT r"accepted scope is a floor" -- that is the section HEADING at
    # doctrine/plans.md:342, so the obligation was satisfied by its own title
    # while the body could be emptied. Pin body prose instead.
    "accepted scope is a floor, stated in the body":
        r"proposal's scope is the authority the plan drains|deviated from "
        r"approved scope",
    "sequencing is free, removal is not":
        r"[Ss]equencing is free; removal is not|Sequencing may move work",
    "a plan reviewer cannot self-authorize":
        r"cannot create that authority",
    "post-Decision baseline is the scope as accepted":
        r"baseline is the scope as accepted",
}

_DOCTRINE_LIFECYCLE = {
    "the remainder record blocks archive per entry":
        r"each entry blocks archive",
    "it is one grouped record, not roadmap rows":
        r"[Nn]ot a set of roadmap rows|one grouped record",
    "nothing is owed for a declined suggestion":
        r"[Nn]ot owed for a declined suggestion",
    "scope-cut is claim correction only":
        r"scope-cut is\s+claim correction|A scope-cut is",
}

#: surface -> obligations. Every path here is one an adopter receives, except
#: the `doctrine/` entries, which are the canonical home the others point at
#: and were previously pinned only by their section heading.
_SURFACES = {
    "AGENTS.md": _GOVERNING,
    "templates/core/AGENTS.md": _GOVERNING,
    "dev/agent_collaboration.md": _REVIEW_LOOP,
    "templates/core/dev/agent_collaboration.md": _REVIEW_LOOP,
    "dev/proposals/_template.md": _PROPOSAL_TEMPLATE,
    "templates/core/dev/proposals/_template.md": _PROPOSAL_TEMPLATE,
    "dev/plans/_template.md": _PLAN_TEMPLATE,
    "templates/core/dev/plans/_template.md": _PLAN_TEMPLATE,
    "dev/PLANNING.md": _BOARD_TAXONOMY,
    "templates/core/dev/PLANNING.md": _BOARD_TAXONOMY,
    "doctrine/dual-review.md": _DOCTRINE_CANONICAL,
    "doctrine/proposals.md": _DOCTRINE_PROPOSALS,
    "doctrine/plans.md": _DOCTRINE_PLANS,
    "doctrine/lifecycle.md": _DOCTRINE_LIFECYCLE,
}

_CASES = [
    (rel, label, pattern)
    for rel, obligations in _SURFACES.items()
    for label, pattern in sorted(obligations.items())
]


def _normalized(rel: str) -> str:
    """Collapse whitespace runs so patterns test the rule, not the wrapping."""
    return re.sub(r"\s+", " ", (CAIRN_ROOT / rel).read_text(encoding="utf-8"))


@pytest.mark.parametrize("rel,label,pattern", _CASES,
                         ids=[f"{r}::{l}" for r, l, _ in _CASES])
def test_scope_reduction_obligation_present(rel: str, label: str,
                                            pattern: str) -> None:
    assert re.search(pattern, _normalized(rel)), (
        f"{rel} no longer expresses the scope-reduction obligation {label!r}. "
        f"The canonical rule is in doctrine/dual-review.md, which adopters "
        f"never receive; removing it here removes it for them."
    )


def test_the_canonical_section_exists_and_sits_beside_its_mirror() -> None:
    """Placement is part of the rule.

    The scope-reduction trap is the mirror of the clean-pass trap -- both are
    failure modes that feel like diligence. A reader who finds one must find
    the other without already knowing it exists.
    """
    raw = (CAIRN_ROOT / "doctrine/dual-review.md").read_text(encoding="utf-8")
    headings = re.findall(r"^## (.+)$", raw, re.M)
    clean = [i for i, h in enumerate(headings) if "clean-pass trap" in h]
    scope = [i for i, h in enumerate(headings) if "scope-reduction trap" in h]
    assert clean, "doctrine/dual-review.md lost its clean-pass trap section"
    assert scope, (
        "doctrine/dual-review.md has no '## Review expectations -- the "
        "scope-reduction trap' section; it is the canonical home every other "
        "surface points at."
    )
    assert scope[0] == clean[0] + 1, (
        f"the scope-reduction trap is not the section immediately after the "
        f"clean-pass trap (headings: {headings[clean[0]:scope[0] + 1]})"
    )


#: The two transitions whose scaffold an author meets when narrowing:
#: a proposal revision (pre-Decision) and a plan-review Sharpening
#: (post-Decision).
#:
#: The vocabulary migration retired `reviewed`/`revised` from the live proposal set and
#: re-homed the Scope-delta declaration onto the RETURN arm out of `revising`
#: -- `_response_template`, emitted by `_scaffold` for `revising ->
#: awaiting-review` -- so the proposal row is re-pointed there.
#:
#: The plan row is left UNCHANGED and STILL POINTS AT THE RETIRED `executing`
#: TOKEN. It did not re-home the plan-side scaffold: `_scaffold`'s plan branch
#: still only emits `**Scope delta**` for the literal string "executing",
#: which is no longer reachable from any state in `PLAN_TRANSITIONS` or
#: `PLAN_TRANSITIONS_REVIEW_NOT_REQUIRED` (checked by hand against
#: the retired lifecycle planner). There is currently NO live plan
#: transition that scaffolds the declaration -- not `ready-to-implement`
#: (the reviewer's clearing move, using the generic `_status_move_manifest`
#: with no declaration block) and not `revising-plan`'s return arm to
#: `awaiting-plan-review` (same). This row is kept exactly as it was --
#: neither invented a new live target nor dropped -- because the three
#: direct-`_scaffold`-call tests below still pass against it (they bypass
#: `_legal_transitions` entirely), and inventing a plausible-looking live
#: target here would assert a parity with the proposal side that does not
#: exist in the code today. A later chunk that re-homes the plan-side
#: scaffold should update this row alongside it.
#: The migration re-homed BOTH surfaces onto the arm where an AUTHOR answers a review,
#: which is the moment scope can quietly narrow -- and the two are deliberately
#: symmetric now, where before they were not (`reviewed -> revised` on one side,
#: `awaiting-plan-review -> executing` on the other, both legacy-only).
_SCAFFOLDED_TRANSITIONS = (
    ("proposal", "revising", "awaiting-review"),
    ("plan", "revising-plan", "awaiting-plan-review"),
)




#: The one declaration grammar, across every surface that prints it. A review
#: unified six surfaces on `preserved | degraded | lost`; the clearing pass
#: then found the (since-retired) planner scaffolds still telling the author to "omit
#: entirely when preserved" one line above a list offering `preserved`, and
#: NOTHING pinned the grammar -- reverting all six stayed green.
_DECLARATION_VALUES = "**Scope delta**: preserved | degraded | lost"

_GRAMMAR_TEMPLATES = (
    # The canonical statement FIRST -- it is the surface the other six were
    # unified onto, and it was the one the first version of this guard left
    # unpinned. Reverting it alone stayed green.
    "doctrine/proposals.md",
    "dev/proposals/_template.md",
    "templates/core/dev/proposals/_template.md",
    "dev/plans/_template.md",
    "templates/core/dev/plans/_template.md",
)


@pytest.mark.parametrize("rel", _GRAMMAR_TEMPLATES)
def test_every_template_prints_the_same_declaration_grammar(rel: str) -> None:
    assert _DECLARATION_VALUES in _normalized(rel), (
        f"{rel} no longer prints the agreed declaration grammar "
        f"{_DECLARATION_VALUES!r}. Six surfaces print this; if they drift, an "
        f"author meets one vocabulary while the doctrine defines another."
    )






# --- the `_declared_reduction` boundary contract lives with its owner --------
#
# This module used to carry five parametrised cases pinning `_declared_reduction`
# directly. They are gone, and their absence is the fix rather than a loss.
#
# An External review (2026-08-12) found those cases covered value
# recognition only -- not heading-bounded scope, allowance position, isolation,
# fence exclusion, or multiple declarations -- and they imported a private
# predicate owned by the executing `review-efficient-lifecycle` plan, so a
# correction there could redden this suite under the wrong owner while these
# cases silently constrained that design.
#
# That plan adopted the contract at `3c3f24f`: 25 table-driven nodes in
# `bootstrap/tests/test_lifecycle_contract.py::TestScopeDeltaParserContract`,
# covering the seven dimensions the review named, and encoding the Maintainer's
# 2026-08-12 boundary -- a presence check stays forbidden (`preserved`, absent
# and unfilled values yield nothing), an authorization check is permitted.
# Verified before removing these: `test_no_presence_check_exists_in_any_direction` (six values) and
# `test_an_absent_field_yields_nothing` pin the forbidden half there.
#
# What stays here is what this plan owns: that no transition refuses on a
# missing declaration.  The planner that once refused on it is gone; what
# survives here is the doctrine-text half, which is what adopters receive.






#: A proposal at `revising`, i.e. one transition BEFORE the `-> awaiting-review`
#: scaffold that carries the declaration (re-pointed by the migration, which retired
#: `reviewed`/`revised` and re-homed the declaration onto this return arm --
#: see `_SCAFFOLDED_TRANSITIONS` above). The source status matters: an
#: artifact already at `awaiting-review` has legal targets
#: `revising/awaiting-decision`, so sweeping `_legal_transitions`
#: from there covers every transition EXCEPT the one under test. That was the
#: defect in the first version of this fence -- the same
#: named-enforcer-that-does-not-enforce shape it was written to close.
_PROPOSAL_AWAITING_REVISION = """# Proposal: something

**Author**: Someone
**Status**: revising

## Context

A revision is about to land that quietly drops an outcome, declaring nothing.

## Review -- Reviewer A (External) -- 2026-08-10

**[R1]** This is too large.
"""

#: The plan half. Round 3 declined the gate for BOTH scaffolded transitions,
#: so both need a fixture; the first version of this fence built no plan
#: artifact at all.
_PLAN_AWAITING_EXECUTION = """# Plan: something

**Status**: awaiting-plan-review
**Plan review**: required(Internal)

## Scope

Carries less than the accepted proposal, and declares nothing.

## Plan review -- Reviewer A -- 2026-08-10

**Tier**: Internal
**Findings**: none

### Sharpening -- Someone -- 2026-08-10

Narrowed chunk B away.
"""

#: (kind, subdirectory, filename, source status, scaffolded target).
#: The proposal row's target is exactly `_SCAFFOLDED_TRANSITIONS`' proposal
#: row -- the one place the declaration is offered live today.
#:
_PLAN_NO_REVIEW_REQUIRED = """# Plan: something

**Plan review**: not required(single commit, single area)

## Scope

Carries less than the accepted proposal, and declares nothing.
"""

_FENCE_FIXTURES = (
    ("proposal", "proposals", "2026-08-10-someone-something.md",
     _PROPOSAL_AWAITING_REVISION, "awaiting-review"),
    ("plan", "plans", "some-plan.md",
     _PLAN_AWAITING_EXECUTION, "ready-to-implement"),
    ("plan", "plans", "some-other-plan.md",
     _PLAN_NO_REVIEW_REQUIRED, "ready-to-implement"),
)


