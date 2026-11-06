# Reconcile lifecycle guidance with the supported paths

**Author**: Codex (Strategy / proposal author, gpt-6.1-sol, High)
**Status**: awaiting-decision
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
   records without the obsolete standard-note contrast. Reconcile every current
   public and installed direction to that route, including the guides, diagram,
   accessibility text and session-start skill listed below; finding another
   live routing instruction makes its correction required, not merely mapped.
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
Alongside the three methodology pages and both plan templates, explicitly
reconcile current routing in `docs/dev-tour.md`, `docs/quickstart.md`,
`docs/glossary.md`, `docs/getting-started.md`, `docs/index.html`,
`docs/release-process.md`, `docs/vision.md`, `docs/workflow-role.md`, the current
instructions in `docs/solo-legacy-recipe.md`, and relevant discussion in
`docs/methodology/dual-review.md`. Update the rendered route, source description,
SVG title/description and embedding alt text of
`docs/assets/three-lanes-of-change.svg` together.

Reconcile section 4 routing and eligibility language in the installed
`templates/skills/session-start/SKILL.md` and its tracked local mirror
`.agents/skills/session-start/SKILL.md`; settled work must not start through an
unsupported note route. Preserve existing Decisions, plan fences and review
obligations when explaining eligible next actions. This edits guidance, not
session tooling or runtime authority.

Follow [documentation routing](../../docs/DOCUMENTATION_PLAN.md). Classify all
remaining current routing references found by search and correct contradictory
ones; retain historical records and clearly historical discussion unchanged.
The implementation record names classifications and any remaining uncertainty.

## Evidence / verification plan

### Tests required

Use `tools/test_tiers.py for` on the concrete changed paths. Existing readers
include review/verification contract tests, scope-reduction tests and status
advisory tests; distinguish real byte pins from incidental citations. Adjust
only checks of corrected prose, retaining required assurance assertions and
protected-test handling. Map readers of public prose, SVG/alt text and both
session-start skill copies as well as methodology/templates. Final Boundary B
is wide for these governing surfaces. No full certification or test execution
is requested for this opening draft.

### Examples / smoke checks

A fresh reader routes a trivial fix, multi-chunk light work, a settled high-risk
change and active work with chosen standard/heavy obligations from the revised
public guides and installed skill. Every required proposal, Decision, plan and
Security stage must remain. Search current prose, graphic source and all
accessibility/embedding text for obsolete parentless routing, not only missing
note-template promises, with known-positive controls. Record each reference's
current/historical classification and resolution. Render the revised SVG and
check its visible route and text alternatives agree with the guides and remain
legible under the documentation asset rules. Run claim, link, snippet and
neutrality gates; unchanged runtime needs no new workflow test machinery.

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

## Proposal review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed commit**: `4728c115`. **Verdict**: REVISE. **Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should it happen as framed?** Yes, once current public routing is included: `lifecycle.md` promises a parentless standard note, but both plan templates require a source proposal and `board.py` requires an accepted proposal join. The named loss needs the Maintainer's explicit Decision; light cannot replace selected standard/heavy assurance.
2. **Best alternative.** Correct the supported route across current guidance while preserving records and review obligations. Restoring the promised route retains a combined artifact but requires a designed authority and tooling contract; marking it unsupported costs less now but leaves conflicting instructions. Both alternatives and the loss are stated in the proposal.
3. **What would show it wrong?** A working parentless standard path, a current guide still directing readers to that retired route, or a standard/heavy change losing required review after reconciliation would falsify the proposal; use known-positive searches and fresh-reader routing checks.

**Blocking finding**: The named changes cover three methodology pages and both plan templates, while other current user-facing guidance also prescribes the route: `docs/dev-tour.md`, `docs/quickstart.md`, `docs/glossary.md`, `docs/getting-started.md` and `docs/assets/three-lanes-of-change.svg`, among others, and `templates/skills/session-start/SKILL.md` sends settled work to a change note. Mapping other readers alone does not require correcting their contradictory instructions; the proposed negative search covers note-template promises rather than all obsolete routing. Close by making reconciliation of current public and installed routing an explicit outcome and verifying all affected guides and graphics, while preserving historical records.

**Coverage**: Read the committed proposal, current template, lifecycle route, both plan templates, advisory join and searched current published and shipped guidance. Did not run tests or exhaustively classify every search hit; separate Security Review remains due.

## Security proposal review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Reviewed commit**: `ed8b0932`
**Obligation**: Internal Security Review
**Tier**: Security Review
**Verdict**: REVISE.
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should it happen as framed?** Yes, with complete current routing: retire the unsupported promise only by explicit Maintainer concession, preserving selected assurance. AGENTS requires heavy for high-risk surfaces; board plan joins require accepted proposal and Security obligations. Neither permits substituting light solely to avoid review. -- Proposal material loss; AGENTS tiers; board plan joins.
2. **Best alternative.** Reconcile the existing routes without new runtime machinery. Marking the parentless route unsupported costs less but leaves contradictory guidance; restoring it requires a separately designed authority contract. The proposed concession honestly names the lost combined standard/heavy artifact. -- Proposal alternatives and material loss; both plan templates require a source proposal.
3. **What would show it wrong?** Route a settled high-risk change and an active accepted standard/heavy artifact through revised installed guidance: any skipped required proposal, Decision, plan or Security stage falsifies preservation. Search current prose and graphic/accessibility text for remaining parentless routing, with known-positive controls. -- Shipped session-start section 4; three-lanes SVG; AGENTS review obligations.

**Blocking -- shared with ordinary review:** Mapping other readers does not require correcting them. The installed session-start skill still says settled standard work needs a change note and may start; the SVG depicts that route separately. Leaving these operative directions could steer adopters around the supported proposal/assurance path even after three methodology pages are fixed. Close by explicitly requiring reconciliation of all current public and shipped routing, including graphics/accessibility text, with preserved historical records and evidence that chosen obligations survive.

**Coverage**: Read committed proposal/usual review, current review template, governing tiers, board joins, installed drain guidance, lifecycle route and SVG. No implementation, tests or runtime trial; did not exhaustively classify historical references. No Decision or review obligation is waived by this pass.

## Response -- Codex GPT-6.1 Sol (High) -- 2026-11-06

- **Shared usual/Security finding accepted:** Operative outcome 1 now requires
  correcting all current public and installed routing. The documentation
  section names the identified guides, current recipe instructions, additional
  methodology discussion, diagram/source/accessibility/embedding text, and both
  tracked session-start skill copies. The verification section requires current
  versus historical classification, graphic rendering and routing checks from
  actual public/installed entry points, including settled high-risk and active
  standard/heavy work. This closes the incomplete coverage within the existing
  reconciliation outcome; it introduces no runtime or authority change.

The named parentless-note loss remains for the Maintainer's explicit Decision.
Both review records remain verbatim; all accepted assurance and historical
records remain protected. No clearing review is requested for this same-outcome
coverage correction. Opening author checks passed on a separate copy of
`4728c115` under Python 3.13.13: claim, link, content, snippet and neutrality
(zero failures, 43 informational entries). Named-reader selection returned zero;
the exact-stem search found no tests and an AGENTS search was a positive control.

**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

### Withdrawn / superseded commitments

None. The former five-surface listing is expanded to require all current
routing corrections; no baseline outcome or assurance is withdrawn.
