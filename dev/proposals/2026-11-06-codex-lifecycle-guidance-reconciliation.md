# Reconcile lifecycle guidance with the supported paths

**Author**: Codex (Strategy / proposal author, gpt-6.1-sol, High)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Correct guidance that promises an unavailable standalone work note while keeping every required review in the supported paths.

## Decision summary

Published guidance tells contributors to use a standalone change note, but
neither current plan template supplies it and the board's next-step guide
requires a source proposal. Reconcile those instructions with the current
trivial path and proposal tiers. This asks the Maintainer to retire that
unsupported promise, rather than build another workflow. Ordinary light work
can already use one proposal across several chunks; light does not retain the
extra plan and code reviews of standard/heavy work. No existing work is
reclassified or loses accepted assurance.

## Context

The [nimbleness strategy, item 2](../strategy/2026-08-21-claude-nimbleness-recovery.md#2-merge-proposal--plan-into-a-single-compact-artifact-for-standard-multi-step-work)
sought one artifact for ordinary two/three-chunk work. Today's light tier
needs no plan regardless of areas or wide verification. Chunk count alone
neither selects light nor overrides a higher tier or required review.

A separate contradiction remains:

- [Lifecycle guidance](../../docs/methodology/lifecycle.md#three-lanes-chosen-by-a-closed-triage-procedure)
  promises a parentless standard change note with Why/What/Approach/Verification/Risk,
  saying its header, transitions and warnings are in the plan template. Its
  opening and “Write once” contrast repeat that route.
- [Plans guidance](../../docs/methodology/plans.md) repeats the parentless-note
  promise and its Waiting-line behavior; [proposal guidance](../../docs/methodology/proposals.md)
  routes remaining nontrivial work there.
- Both [local](../plans/_template.md) and [shipped](../../templates/core/dev/plans/_template.md)
  plan templates instead require a source proposal and contain no note
  skeleton, while retaining one change-note Waiting-line reference each.
- The actual [board helper](../../templates/skills/_lib/board.py) sends an
  accepted light proposal to implementation, but refuses the plan next-step
  recommendation without a readable accepted proposal join. This is advisory
  routing, not an implementation permission check.

These are inspected source facts, not a failed runtime trial. The existing
`test_next_light_proposal_continues_until_archived` in
`bootstrap/tests/test_board_json_contract.py` covers the supported light route;
its result was not rerun for this draft.

## Proposal

For v0.7, deliver one coherent documentation reconciliation before release:

1. Describe the existing trivial path and proposal Decision tiers consistently
   in lifecycle, proposal and plan guidance. Remove the unsupported parentless
   note route, template claims and remnant Waiting-line references from local
   and shipped templates. Retain in-place operative revision and append-only
   records without the obsolete standard-note contrast.
2. Explain that light keeps its accepted proposal as the single implementation
   record and records final verification there. Standard/heavy work keeps its
   current plan triage, required plan/code reviews, separate Security Reviews,
   checks, fences and archive rules. Preserve model floors and all high-risk
   triggers. Size, chunk count and ordinary uncertainty are not authority to
   discard a genuinely selected higher tier or review obligation.
3. Preserve historical notes, reviews and Decisions as records. Do not delete
   old notes, automatically downgrade active work, or reinterpret its accepted
   assurance. No new artifact, schema, status, registry, board branch or runtime
   behavior is authorized. Existing tools remain descriptive evidence.

**Material loss requiring the Maintainer's Decision:** retire the documented
ability to use a parentless standard change note. This also declines a new
single-file mechanism for work that genuinely requires standard/heavy stages;
light cannot supply those stages by substitution. The current templates and
advisory do not deliver that promise, but its written existence is still a
promise, not permission for an agent to erase it. Acceptance must explicitly
disposition this loss.

## Rationale

Correcting the contradictory instructions gives adopters a usable route now.
It avoids adding workflow machinery solely because an older description
promised it. That is a recommendation about the documented promise, not an
author determination that required assurance is unnecessary.

## Alternatives considered

- **Reconcile with supported paths.** A bounded documentation/template edit,
  reader mapping, affected checks and both reviews; no new recurring operation
  or data format. Future guidance maintains one supported account. It loses
  the parentless-note promise and adds no combined standard/heavy artifact.
- **Restore the promised contract.** Retains a parentless single-file path,
  but requires a separate design for review/Decision authority, template
  fields, advisory joins, compatibility and tests. Setup and continuing
  maintenance exceed a prose correction; exact effort is unknown. This
  proposal does not authorize that implementation.
- **Keep the text, clearly mark the route unsupported.** Smallest edit and
  useful temporary disclosure, but leaves readers choosing between a promise
  and its warning. Unmarked current text continues misleading guidance and
  does not remedy the defect.

**Recommendation:** reconcile with supported paths and explicitly accept the
named loss. Restore the contract only if its remaining benefit warrants the
additional workflow and maintenance cost.

## Documentation / doctrine surface

Prescription remains in AGENTS; the described existing rules are not changed.
Reconcile the three methodology pages and both plan templates named above,
following [documentation routing](../../docs/DOCUMENTATION_PLAN.md). Map any
other current readers/remnants before implementation; preserve historical
records rather than rewriting them to match new guidance.

## Evidence / verification plan

### Tests required

Use `tools/test_tiers.py for` on the concrete changed paths. Existing readers
include review/verification contract tests, scope-reduction tests and status
advisory tests; distinguish real byte pins from incidental citations. Adjust
only checks of corrected prose, retaining required assurance assertions and
protected-test handling. Final Boundary B is wide for methodology/templates.
No full certification or test execution is requested for this opening draft.

### Examples / smoke checks

A fresh reader routes a trivial fix, multi-chunk light work, and work with
chosen standard/heavy obligations using the revised guidance. The latter must
retain its plan/review requirements. Search active guidance for every old
note-template promise with known-positive controls. Run claim, link, snippet
and neutrality gates; unchanged runtime needs no new workflow test machinery.

#### Security preflight — five questions, answered in writing

- **S1 — Who supplied it?** Existing repository doctrine, Decisions and advisory
  source supply evidence; no candidate-derived approval input is added.
- **S2 — Can it fail?** A remaining nonexistent-template promise or a route
  that drops required review falsifies reconciliation. Existing light-tier
  contract tests have deletion controls; no mutation was run for this draft.
- **S3 — What fires it, over what?** Authors follow AGENTS and current
  templates; prose checks and mapped readers cover edited guidance. The
  offending promise is “standard-note contract carried in the plan template”;
  the supplied template instead requires a source proposal.
- **S4 — Which way does it break?** No runtime default, parser or fallback
  changes. Uncertain or newly found boundaries retain reassessment; wording
  must not create permission to skip a required stage.
- **S5 — Who still wins?** An agent can still ignore governing rules. Clearer
  prose supplies no mechanical enforcement or protection from hostile code.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Readers still seek a missing template, treat chunk count as tier authority,
downgrade accepted work, or lose a required review. Evidence that the promised
contract already exists and works would invalidate this proposal's premise.

## Scope delta

**Scope delta**: preserved against this opening proposal. The requested
concession above remains for the Maintainer; it has not been granted.

## Assurance path

**Assurance path**: high-assurance

Methodology and shipped templates require usual and separate Security Reviews,
including both plan obligations. This draft grants no implementation authority.

**Authoring record**: elapsed approximately 6 minutes; tokens unknown. Source
inspection only; no tests, ceremonies or private inputs used.
