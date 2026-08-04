<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: the review-before-implement gate checks the review, not its presence

**Source proposal**: `dev/proposals/2026-08-04-claude-review-gate-enforcement.md`
**Status**: open
**Plan review**: required(**External**) — carried from the proposal header and
re-affirmed in the Decision: *"the replacement mechanism … was authored after the
External round and has not been read by a different agent type. The plan is
where it gets that read."*
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Source proposal

The gate at `tools/lifecycle_planner.py:787` clears on the *presence* of a
section named "Plan review", not on the review its own doctrine describes. Four
documented promises — the declared tier, the `##` heading level, the date, and a
`### Sharpening` subsection when findings were raised — are unenforced. Accepted
as revised on 2026-08-04 with one condition, quoted in *Scope* below. The
External review reduced the fix from "enforce the four rules" to "make the
record able to carry them, then enforce what it carries".

## Scope

**The Decision's condition, verbatim, because it is this plan's shape:**

> on the condition that the plan reconciles the ##/### grammar across doctrine,
> both plan templates and the planner scaffold before gating on it, and treats
> the adopter-facing record-format change as in scope

### In scope

* `doctrine/plans.md` — the grammar reconciliation, and the review-record format.
* `dev/plans/_template.md` and `templates/core/dev/plans/_template.md` — the
  shipped containers, which must agree with the reconciled grammar.
* The planner's generated plan scaffold.
* `tools/lifecycle_planner.py` and its byte-identical twin
  `templates/skills/_lib/lifecycle_planner.py`.
* `bootstrap/tests/test_lifecycle_contract.py` — the new nodes.

### Out of scope, fenced

* **Authenticating independence.** Per `[E4]`, this tool is a **conformance
  backstop**. It cannot establish that the declared review happened, and nothing
  in this plan may claim otherwise — including violation text.
* **`doctrine/lifecycle.md:175-182`.** It states the gate is *"explicit, not
  remembered"*, which stays true. Chunk D of `gate-claims-vs-enforcement` is
  concurrently editing `:218-221` of the same file; these do not overlap and
  this plan does not touch that region.
* **Adopter tree migration.** Two internal adopters, Maintainer-managed
  (Decision context). This plan ships the migration *note*; running it is the
  Maintainer's.

## Sequence

### Chunk A — reconcile the grammar (no behaviour change)

The blocker `[E2]` named: `doctrine/plans.md` contradicts itself. `:115` requires
*"a dated `## Plan review` section"*; `:422` prescribes *"### Plan review --
<reviewer> -- YYYY-MM-DD"* as the per-pass format. Both plan templates ship a
`## Plan review` container with `###` passes inside.

**Measured, `as_of 2026-08-04` at plan-open** —
`grep -rhoE "^#{2,3} Plan review" dev/plans dev/proposals | sort | uniq -c`:
**58 headings, all `##`, none `###`** (56 in `dev/plans`, 2 in `dev/proposals`).
Practice follows `:115`; the instructions say `:422`.

*One of those 58 is this plan's own `## Plan review` container* — the corpus
includes the artifact measuring it. The figure was 57 before this file existed
and will move again as plans open, which is why it carries an `as_of` and is not
registered as an invariant. Chunk C's corpus table must be re-measured at the
commit that gates, never carried forward from here.

| # | File | Change |
|---|------|--------|
| A.1 | `doctrine/plans.md` | State **one** grammar: an `## Plan review` container, with each pass a dated `### Plan review -- <reviewer> -- YYYY-MM-DD` inside it. Reconcile `:115` and `:422` to it. |
| A.2 | `dev/plans/_template.md`, `templates/core/dev/plans/_template.md` | Make both agree with A.1. They must stay in step — a template that disagrees with doctrine reproduces this defect for every adopter. |
| A.3 | The planner's generated plan scaffold | Emit the A.1 shape. |

**No gating in this chunk.** It lands green and changes no verifier behaviour.

### Chunk B — the record can carry a tier and an outcome

`[E1]` and `[E3]`: today's record cannot express what the gate would need to
read. A role field is free text — and the published format has none.

| # | File | Change |
|---|------|--------|
| B.1 | `doctrine/plans.md` | Add to the review-pass format a **declared tier attestation** and a **review outcome**, both with **closed vocabularies**. Document in terms that the attestation is *declared, not authenticated*. |
| B.2 | both templates + scaffold | Carry B.1's fields. |
| B.3 | `tools/lifecycle_planner.py` + twin | Parse the two fields. Admit `Sharpening` to `_KNOWN_KINDS` — `[E3]` established it is absent today, so the conditional currently has no parseable subject. **Parse only; gate nothing yet.** |

### Chunk C — gate on what the record now carries

Only here does behaviour change. Each rule gets a node with a **single-property
falsifier**: a mutation that reddens that node and **no other**. Five tests that
could not fail were found in this repository this cycle; the plan that guards
reviews will not add a sixth.

| # | Rule | Node | Single-property falsifier |
|---|------|------|---------------------------|
| C.1 | declared tier satisfied | new | delete the tier comparison → this node red, others green |
| C.2 | heading level per A.1 | new | accept any level → red |
| C.3 | dated | new | make the date group optional in the check → red |
| C.4 | `### Sharpening` when outcome declares findings | new | drop the conditional → red |

**Before C lands, run the reconciled gate over every artifact in `dev/` and
record which newly violate.** A gate that reddens the existing tree needs that
disclosed up front, not discovered. That table is a deliverable of this chunk,
not a note.

### Chunk D — the adopter-facing disclosure

| # | File | Change |
|---|------|--------|
| D.1 | migration note | State the record-format change, the two affected fields, and what an adopter must do. The twin is a `verbatim` manifest source installed as `tools/lifecycle_planner.py`, so behaviour and policy ship together. |
| D.2 | `CHANGELOG.md` > Unreleased | One line. **Serialized: text returned, not edited in-agent.** |

## Acceptance criteria

* `doctrine/plans.md`, both templates and the scaffold state **one** grammar; a
  grep for the review heading across all four surfaces returns one shape.
* The twins stay byte-identical (`test_every_self_hosted_twin_stays_byte_identical_to_its_source`).
* Four new nodes in `bootstrap/tests/test_lifecycle_contract.py`, each with its
  single-property falsifier **demonstrated**, not asserted — the falsifier is run
  and the red/green matrix recorded.
* Suite: **no *new* failure relative to a baseline measured immediately before
  the commit on a quiet tree**, `0 skipped`. Not "green" unconditionally: the
  tree carries concurrent work.
* The `dev/` corpus table from Chunk C is in the record before C commits.
* No violation text uses the language of authorization (`[E4]`).

## Verification

* Reproduce the proposal's five-state table against the **post-change** module;
  the four rows that clear today must not all clear after Chunk C.
* Confirm the tier attestation is parsed from the closed vocabulary and that an
  **unrecognized** value is a violation rather than a silent pass — the fail-open
  direction is the one that matters.
* Confirm a conforming **human** review passes. `[E1]`'s sharpest case: the
  published format had no role field, so the original rule would have blocked
  one.

## Plan review

*Required — **External**. Implementation does not start until a review has
landed under this heading.* The Internal floor does not discharge it: the
replacement mechanism in Chunk B was authored after Codex's External round and
has had no different-agent-type read. A reviewer should attack **B.1's closed
vocabularies** first — that is the newest and least-examined surface, and if the
vocabulary is wrong every later chunk inherits it.

## Code review

*No review has landed.*

## Lasting-truth migration

| Truth | Home |
|---|---|
| The gate is a conformance backstop, not proof a review happened | `doctrine/plans.md`, alongside the format it validates |
| One review-heading grammar across doctrine, templates and scaffold | A.1, and the templates themselves |
| A declared tier attestation is declared, not authenticated | `doctrine/plans.md` > the review-pass format |
