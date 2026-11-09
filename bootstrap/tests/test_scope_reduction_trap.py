"""The scope-reduction trap must reach the adopter, not only the doctrine.

`docs/methodology/dual-review.md` holds the canonical rule, but `docs/methodology/` is **not
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
import subprocess
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
_PROPOSAL_TEMPLATE = {
    "carries the declaration": r"\*\*Scope delta\*\*",
}

_PLAN_TEMPLATE = {
    "carries the declaration": r"\*\*Scope delta\*\*",
}

_DOCTRINE_CANONICAL = {
    "carries all three outcome values":
        r"preserved.{0,400}degraded.{0,200}lost",
}

_DOCTRINE_PROPOSALS = {
    "carries the declaration": r"\*\*Scope delta\*\*",
}

#: surface -> obligations for the declaration markers retained by this owner.
_SURFACES = {
    "dev/proposals/_template.md": _PROPOSAL_TEMPLATE,
    "templates/core/dev/proposals/_template.md": _PROPOSAL_TEMPLATE,
    "dev/plans/_template.md": _PLAN_TEMPLATE,
    "templates/core/dev/plans/_template.md": _PLAN_TEMPLATE,
    "docs/methodology/dual-review.md": _DOCTRINE_CANONICAL,
    "docs/methodology/proposals.md": _DOCTRINE_PROPOSALS,
}

_CASES = [
    (rel, label, pattern)
    for rel, obligations in _SURFACES.items()
    for label, pattern in sorted(obligations.items())
]


def _normalized(rel: str) -> str:
    """Collapse whitespace runs so patterns test the rule, not the wrapping."""
    return re.sub(r"\s+", " ", (CAIRN_ROOT / rel).read_text(encoding="utf-8"))


def test_scope_reduction_plan_template_installs_from_source(tmp_path: Path) -> None:
    """Both profiles install the shipped plan template without drift."""
    profiles = ("solo-greenfield.yml", "high-rigor-legacy.yml")
    source = (CAIRN_ROOT / "templates/core/dev/plans/_template.md").read_bytes()
    for profile_name in profiles:
        target = tmp_path / profile_name.removesuffix(".yml")
        target.mkdir()
        result = subprocess.run(
            [
                sys.executable,
                str(CAIRN_ROOT / "bootstrap/scaffold.py"),
                "--config", str(CAIRN_ROOT / "bootstrap/profiles" / profile_name),
                "--target", str(target),
                "--cairn-root", str(CAIRN_ROOT),
                "--non-interactive", "--allow-dev",
            ],
            cwd=CAIRN_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        installed = (target / "dev/plans/_template.md").read_bytes()
        assert installed == source, (
            f"{profile_name} installed a plan template that differs from its source"
        )


@pytest.mark.parametrize("rel,label,pattern", _CASES,
                         ids=[f"{r}::{l}" for r, l, _ in _CASES])
def test_scope_reduction_obligation_present(rel: str, label: str,
                                            pattern: str) -> None:
    assert re.search(pattern, _normalized(rel)), (
        f"{rel} no longer expresses the scope-reduction obligation {label!r}. "
        f"The canonical rule is in docs/methodology/dual-review.md, which adopters "
        f"never receive; removing it here removes it for them."
    )


def test_the_canonical_section_exists_and_sits_beside_its_mirror() -> None:
    """Placement is part of the rule.

    The scope-reduction trap is the mirror of the clean-pass trap -- both are
    failure modes that feel like diligence. A reader who finds one must find
    the other without already knowing it exists.
    """
    raw = (CAIRN_ROOT / "docs/methodology/dual-review.md").read_text(encoding="utf-8")
    headings = re.findall(r"^## (.+)$", raw, re.M)
    clean = [i for i, h in enumerate(headings) if "clean-pass trap" in h]
    scope = [i for i, h in enumerate(headings) if "scope-reduction trap" in h]
    assert clean, "docs/methodology/dual-review.md lost its clean-pass trap section"
    assert scope, (
        "docs/methodology/dual-review.md has no '## Review expectations -- the "
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
    "docs/methodology/proposals.md",
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


