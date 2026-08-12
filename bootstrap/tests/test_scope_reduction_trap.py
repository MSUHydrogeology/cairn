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

from tools import lifecycle_planner as planner  # noqa: E402

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
    "names the trap":
        r"scope-reduction trap",
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
    # D7 (clearing pass): C9 added the floor rule to the `## Scope` fence,
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
    # code review (C3), which cut exactly that text and saw 51 passed.
    "only the Maintainer may concede a baseline outcome":
        r"only the Maintainer may concede|[Nn]either author nor reviewer may "
        r"concede",
    # D2 (clearing pass): C3's satisfier had two halves and only the authority
    # half landed. Each of these could be deleted from the shipped board while
    # the suite stayed green.
    "the baseline is the artifact's own commitments, both stages":
        r"as \*?opened\*?.{0,80}as \*?accepted\*?|outcome test in",
    "the remainder is one grouped record per source artifact":
        r"grouped\s+scope-remainder record",
}

_TEAM_GATED_MODULE = {
    "scope-cut is reserved for claim correction":
        r"scope-cut.{0,80}claim correction",
    "names the trap":
        r"scope-reduction trap",
    "carries the three-way outcome test":
        r"preserved.{0,300}degraded",
    "declining a review-proposed expansion is not a reduction":
        r"never in the baseline",
    # R2-E1 again. The code review (C3) rewrote this module to say degraded
    # and lost "are for the author and reviewer to settle between them" --
    # the exact contradiction an External round was spent eliminating -- and
    # the suite stayed green.
    "only the Maintainer may concede a baseline outcome":
        r"only the Maintainer may concede|never who may concede it|the "
        r"\*{0,2}Maintainer'?.{0,4}s?\*{0,2} explicit allowance",
}

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
    # while the body could be emptied (D7). Pin body prose instead.
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
#: and were previously pinned only by their section heading (code review C7).
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
    "templates/modules/team-gated/dual-review.md": _TEAM_GATED_MODULE,
    # Cairn's OWN installed copy of the module above, paired to it by
    # `dev/.cairn/cairn-lock.yml`. Chunk B edited the shipped source and not
    # this one, leaving the unsound `scope-cut -> accept` mapping live in the
    # copy Cairn itself reads (code review C1). Listing it here is what makes
    # that drift a red test rather than a lucky catch.
    "dev/modules/dual-review.md": _TEAM_GATED_MODULE,
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
_SCAFFOLDED_TRANSITIONS = (
    ("proposal", "reviewed", "revised"),
    ("plan", "awaiting-plan-review", "executing"),
)


@pytest.mark.parametrize("kind,status,target", _SCAFFOLDED_TRANSITIONS,
                         ids=[f"{k}->{t}" for k, _, t in _SCAFFOLDED_TRANSITIONS])
def test_the_emitted_scaffold_carries_the_declaration(kind: str, status: str,
                                                      target: str) -> None:
    """Through `_scaffold`, not by grepping the source.

    The scaffold is built from adjacent string literals, so a source-text
    search tests the line wrapping rather than what an author is handed. What
    matters is the text that reaches STDOUT.
    """
    art = planner.Artifact(path=Path(f"some-{kind}.md"), kind=kind, text="")
    art.status = status
    _, _, blocks = planner._scaffold(art, target, "2026-08-11")
    emitted = "\n".join(blocks)

    assert "**Scope delta**" in emitted, (
        f"the {kind} -> {target} scaffold no longer offers the Scope-delta "
        f"declaration; this is the surface where an author meets the rule "
        f"while typing rather than recalling it from doctrine later."
    )
    assert "Removed scope" in emitted and "Disposition/home" in emitted, (
        f"the {kind} -> {target} scaffold offers the declaration without the "
        f"grouped remainder block it requires."
    )
    assert "DOES NOT CHECK" in emitted, (
        f"the {kind} -> {target} manifest no longer states that nothing "
        f"enforces the declaration. Saying so is the point: a scaffold that "
        f"looks like a gate invites the reader to trust it as one."
    )


#: The one declaration grammar, across every surface that prints it. C8
#: unified six surfaces on `preserved | degraded | lost`; the clearing pass
#: (D5) then found the planner scaffolds still telling the author to "omit
#: entirely when preserved" one line above a list offering `preserved`, and
#: NOTHING pinned the grammar -- reverting all six stayed green.
_DECLARATION_VALUES = "**Scope delta**: preserved | degraded | lost"

_GRAMMAR_TEMPLATES = (
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


@pytest.mark.parametrize("kind,status,target", _SCAFFOLDED_TRANSITIONS,
                         ids=[f"{k}->{t}" for k, _, t in _SCAFFOLDED_TRANSITIONS])
def test_the_scaffolds_print_the_same_declaration_grammar(
        kind: str, status: str, target: str) -> None:
    """Through `_scaffold`, because the block is built from adjacent literals."""
    art = planner.Artifact(path=Path(f"some-{kind}.md"), kind=kind, text="")
    art.status = status
    _, _, blocks = planner._scaffold(art, target, "2026-08-12")
    emitted = " ".join("\n".join(blocks).split())
    assert _DECLARATION_VALUES in emitted, (
        f"the {kind} -> {target} scaffold prints a different declaration "
        f"grammar than the templates do."
    )


@pytest.mark.parametrize("kind,status,target", _SCAFFOLDED_TRANSITIONS,
                         ids=[f"{k}->{t}" for k, _, t in _SCAFFOLDED_TRANSITIONS])
def test_the_scaffolds_do_not_contradict_the_offered_values(
        kind: str, status: str, target: str) -> None:
    """The exact D5 defect, pinned.

    A scaffold that offers `preserved` in its value list and tells the author
    to omit the block when preserved contradicts itself in adjacent lines. The
    author follows one or the other, so the field means different things in
    different records -- which is the failure the unified grammar removed.
    """
    art = planner.Artifact(path=Path(f"some-{kind}.md"), kind=kind, text="")
    art.status = status
    _, _, blocks = planner._scaffold(art, target, "2026-08-12")
    emitted = " ".join("\n".join(blocks).split()).lower()
    assert "omit entirely" not in emitted, (
        f"the {kind} -> {target} scaffold tells the author to omit the block "
        f"when preserved while offering `preserved` as a value. The templates "
        f"say `preserved` may be stated; the scaffold must not disagree."
    )


def test_the_two_planner_twins_stay_byte_identical() -> None:
    """The scaffold change had to land in both copies or adopters get neither."""
    a = (CAIRN_ROOT / "tools/lifecycle_planner.py").read_bytes()
    b = (CAIRN_ROOT / "templates/skills/_lib/lifecycle_planner.py").read_bytes()
    assert a == b, "lifecycle_planner twins have drifted"


#: A proposal at `reviewed`, i.e. one transition BEFORE the `-> revised`
#: scaffold that carries the declaration. The source status matters: an
#: artifact already at `revised` has legal targets
#: `reviewed/accepted/rejected/superseded`, so sweeping `_legal_transitions`
#: from there covers every transition EXCEPT the one under test. That was the
#: defect in the first version of this fence (clearing pass, D1) -- the same
#: named-enforcer-that-does-not-enforce shape it was written to close.
_PROPOSAL_AWAITING_REVISION = """# Proposal: something

**Author**: Someone
**Status**: reviewed

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
#: These targets are exactly `_SCAFFOLDED_TRANSITIONS` above -- the two places
#: the declaration is offered, and therefore the only two a gate could be
#: attached to and still bite. Deriving the sweep from `_legal_transitions`
#: instead is what let a real gate pass unnoticed.
_FENCE_FIXTURES = (
    ("proposal", "proposals", "2026-08-10-someone-something.md",
     _PROPOSAL_AWAITING_REVISION, "revised"),
    ("plan", "plans", "some-plan.md",
     _PLAN_AWAITING_EXECUTION, "executing"),
)


@pytest.mark.parametrize("kind,subdir,name,body,target", _FENCE_FIXTURES,
                         ids=[f"{k}->{t}" for k, _, _, _, t in _FENCE_FIXTURES])
def test_the_planner_does_not_gate_on_a_missing_declaration(
        tmp_path, kind: str, subdir: str, name: str, body: str,
        target: str) -> None:
    """The declined planner gate, pinned as an absence -- on the transitions
    that actually scaffold the declaration.

    Round 3 of the source proposal declined a transition gate and the
    Maintainer accepted that disposition. The reason is worth keeping in front
    of whoever reads this next: a formal check can confirm a declaration
    *exists*, never that it is *true*. It would catch forgetting and not
    evading -- and would make evading easier, by handing a quiet cut a green
    check to sit behind.

    So this asserts the *absence* of enforcement. If someone later adds the
    gate, this fails and sends them to the recorded revival condition rather
    than letting it arrive unremarked.
    """
    d = tmp_path / "dev" / subdir
    d.mkdir(parents=True)
    f = d / name
    f.write_text(body, encoding="utf-8")

    art = planner._read_artifact(f)
    assert art.kind == kind, f"fixture parsed as {art.kind!r}, not {kind!r}"
    identity = planner.IdentityModel(frozenset(), frozenset())

    # Both refusal surfaces. `_conformance_violations` reports structural
    # unsoundness; `_gating_preconditions` reports a transition as MISSING.
    # Pinning only the first left a gate on the second entirely green (C4);
    # pinning the second over the WRONG targets left it green again (D1).
    surfaces = {
        "_conformance_violations":
            planner._conformance_violations(art, identity),
        f"_gating_preconditions(-> {target})": [
            desc for _met, desc
            in planner._gating_preconditions(art, target, identity)
        ],
    }

    for surface, messages in surfaces.items():
        joined = " ".join(messages).lower()
        assert "scope delta" not in joined and "scope-remainder" not in joined, (
            f"the lifecycle planner now refuses the {kind} -> {target} "
            f"transition over the scope-delta declaration, via {surface}. "
            f"That gate was declined in the accepted proposal (Round 3) "
            f"because a presence check cannot establish semantic truth -- it "
            f"catches forgetting and not evading, and hands a quiet cut a "
            f"green check to sit behind. Reviving it takes a new proposal "
            f"against the recorded revival condition: authors omitting the "
            f"declaration in practice."
        )
