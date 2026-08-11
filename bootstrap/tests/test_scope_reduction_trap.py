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
}

_BOARD_TAXONOMY = {
    "a scope-cut removes no work":
        r"scope-cut removes no work|scope-cut is claim correction",
    "removing work is a scope reduction instead":
        r"is a \*{0,2}scope reduction",
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
}

#: surface -> obligations. Every path here is one an adopter receives, except
#: `doctrine/dual-review.md`, which is the canonical home the others point at.
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


def test_the_two_planner_twins_stay_byte_identical() -> None:
    """The scaffold change had to land in both copies or adopters get neither."""
    a = (CAIRN_ROOT / "tools/lifecycle_planner.py").read_bytes()
    b = (CAIRN_ROOT / "templates/skills/_lib/lifecycle_planner.py").read_bytes()
    assert a == b, "lifecycle_planner twins have drifted"


_REVISED_PROPOSAL_WITHOUT_A_DECLARATION = """# Proposal: something

**Author**: Someone
**Status**: revised

## Context

A revision landed that quietly dropped an outcome, and declared nothing.

## Review -- Reviewer A (External) -- 2026-08-10

**[R1]** This is too large.

## Response -- Someone -- 2026-08-10

* **[R1]** accept -- removed the second half.

## Revised proposal -- Someone -- 2026-08-10

Build only the first half.
"""


def test_the_planner_does_not_gate_on_a_missing_declaration(tmp_path) -> None:
    """The declined planner gate, pinned as an absence.

    Round 3 of the source proposal declined a transition gate on the
    declaration and the Maintainer accepted that disposition. The reason is
    worth keeping in front of whoever reads this next: a formal check can
    confirm a declaration *exists*, never that it is *true*. It would catch
    forgetting and not evading -- and would make evading easier, by giving a
    quiet cut a green check to sit behind.

    So this asserts the *absence* of enforcement, not its presence. If someone
    later adds the gate, this test fails and sends them to the proposal's
    recorded revival condition instead of letting it arrive unremarked.
    """
    d = tmp_path / "dev" / "proposals"
    d.mkdir(parents=True)
    f = d / "2026-08-10-someone-something.md"
    f.write_text(_REVISED_PROPOSAL_WITHOUT_A_DECLARATION, encoding="utf-8")

    art = planner._read_artifact(f)
    identity = planner.IdentityModel(frozenset(), frozenset())
    joined = " ".join(planner._conformance_violations(art, identity)).lower()

    assert "scope delta" not in joined and "scope-remainder" not in joined, (
        "the lifecycle planner now refuses a transition over the scope-delta "
        "declaration. That gate was declined in the accepted proposal "
        "(Round 3) because a presence check cannot establish semantic truth. "
        "Reviving it takes a new proposal against the recorded revival "
        "condition -- authors omitting the declaration in practice."
    )
