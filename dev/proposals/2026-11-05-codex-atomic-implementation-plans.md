# Independently finishable implementation plans

**Author**: Codex (inherited runtime; exact model identifier unavailable)
**Status**: awaiting-review
**Review**: usual
**Proposed tier**: standard -- one bounded doctrine/template change, with ordinary review as directed by the Maintainer
**Plan review**: required(Internal)
**Opened**: 2026-11-05
**In brief**: Give each plan a useful outcome it can finish independently, while proposals retain the full sequence of present and future work.

## Decision summary

A plan should be a finishable unit of delivery, not a waiting room for other
plans or human operations. Put the larger design and sequence in the proposal;
open each implementation plan when its prerequisites exist. One proposal may
authorize several plans, including work for later releases or capabilities.

Update existing templates and writing guides, not the lifecycle software.
The cost is more care in choosing delivery boundaries, not more forms,
reviews or tiny plans. Put this early in v0.7 so it guides remaining work.

## Context

Two current plans show the dependency shape: the architecture plan's C3
requires board 2d's safe Git helper, while suite consolidation's C4 requires
2b's shared reporting. Useful earlier delivery cannot complete those plans
independently. See `dev/plans/2026-11-05-architecture-and-reuse.md`, Sequence,
and `dev/plans/2026-11-04-suite-consolidation.md`, C4 and Security plan review.
These are two concrete occurrences, not a claim that their safeguards are wrong.

The accepted `implementation-plan-completion` policy already separates routine
human trust/release operations from plan completion. This extends that boundary
to other plans; it does not replace the policy. Writing guides already exist
at `docs/methodology/proposals.md` and `docs/methodology/plans.md`.

## Proposal

1. **One independently finishable outcome per plan.** Atomic means useful,
   coherent delivery whose implementation, required checks, reviews and archive
   can finish without another unfinished plan. It does not mean one file,
   function, commit or arbitrary size limit. Internal chunks may depend on each
   other. Combine inseparable work rather than create dependency-linked
   microplans or a parent plan that waits for child plans.
2. **Sequence at the proposal and board level.** A proposal may authorize
   multiple plans. In its existing Proposal section, name each delivery outcome,
   prerequisites and intended release or capability. Keep later work queued
   on the existing board with its source and revival condition; do not open an
   active implementation plan before its prerequisites are delivered. Archive
   the accepted proposal at the first plan opening under the existing rule;
   preserve the remaining authorized outcomes on the board, linked to that
   immutable source. Later plans cite the same proposal, not new Decisions
   for already authorized work. A changed design still needs existing authority.
3. **Depend on available capabilities, not future plan completion.** A shipped
   helper is a valid prerequisite. A plan promising that helper is not. A
   shared batch may save editing or testing, but no plan waits for another
   plan's review, archive or release label merely to complete its own evidence.
   Required integration evidence remains required; if the outcome cannot be
   verified without future work, queue it or include that work in the same
   coherent plan. Never substitute mocks for owed functional evidence.
4. **No scheduled Maintainer action to reach archive.** Preserve the existing
   separate human-operation waits, evidence and authorization boundaries.
   Helping decide whether or how to handle a deferral remains the Maintainer's.
   Unexpected scope/permission questions still stop for existing authority;
   they are not license to design a human-only final chunk. No failed check,
   defect, required review or missing scientific result becomes a board chore
   merely to finish a plan. Archive never authorizes signing or release.
5. **Preserve scope without a new tracker.** Splitting delivery does not concede
   an accepted outcome. Each authorized outcome must remain assigned to its
   plan or queued board entry; moving it later needs existing scope/scheduling
   authority. Early plan archive is not completion of the whole proposal.
   Use existing Scope, Sequence and Acceptance criteria, not new mandatory
   sections, statuses, sidecars or a dependency checker.

For example, deliver and verify a safe Git helper first; then open a visual
review plan using it. Do not open the visual plan with a final chunk waiting
for the helper's plan. Likewise, deliver cost reporting independently, then
schedule its use in a consolidation assessment.

Apply to newly opened plans after acceptance. Existing v0.7 plans are not
retroactively invalidated or silently narrowed. Any useful repartition uses
the existing scope-amendment authority and preserves every outcome and check;
no mass rewrite or extra clearing-review round is required.

## Rationale

This makes completion mean delivered work. Sequencing remains possible without
coupling every artifact's lifecycle. The proposal holds the whole objective;
the board keeps its later obligations visible.

## Alternatives considered

Keep today's broad plans: no writing changes, but delivered portions remain
mixed with external waits. Split every chunk into a plan: smaller records but
more reviews, board rows and integration risk. Prefer a few useful outcomes,
with internal sequencing where work genuinely belongs together.

## Documentation / doctrine surface

Update relevant passages in live and shipped `AGENTS.md`, both proposal and
plan templates, and `docs/methodology/proposals.md`,
`docs/methodology/plans.md` and `docs/methodology/lifecycle.md`.
Use the existing guides rather than create parallel how-to documents.
Keep point-of-use guidance in the shipped templates, since adopters do not
receive Cairn's methodology directory. Follow `docs/DOCUMENTATION_PLAN.md`;
leave unrelated legacy terminology alone. No engine, ceremony, parser,
security control or installed file inventory changes.

## Evidence / verification plan

### Tests required

Extend the existing source/installed guidance coverage in
`bootstrap/tests/test_review_sweep_ships.py`, including
`test_source_plan_completion_rule_and_surface_mutation` and
`test_installed_plan_completion_and_surface_mutation`. Mutate each required
surface separately to remove independent completion or permit a human-only
final task; the owning check must fail beside its passing control. Select
affected readers with `tools/test_tiers.py for`; do not add a runtime checker.

### Examples / smoke checks

Apply the guidance to an independent delivery, a helper-dependent outcome,
a later-version outcome and a missing-check/human-ceremony case. Show where
every original outcome remains and why archive is or is not allowed. Run
claim, content/link, snippet and neutrality gates on changed prose; preserve
installed wording and existing checks. No full-suite run is added.

### Security preflight

**S1:** Maintainer Decisions supply authority; authors supply plans and board
entries. Those records do not prove completion or authorize execution.
**S2:** Removing independent completion or permitting a human-only final task
must fail the proposed surface mutations. These mutations have not run yet.
**S3:** Existing affected readers and scaffold-installed guidance checks cover
the changed local/shipped surfaces; the intended rule is "Each plan can
implement, verify and archive independently."
**S4:** An unmet check or missing prerequisite remains unmet, not a successful
handoff. No parsing, fallback or runtime permission changes.
**S5:** This assumes cooperative authors and reviewers. Dishonest scope or
completion claims remain possible; prose is not enforcement or containment.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

More tiny plans and review handoffs; lost deferred scope; archive without
required evidence; or active plans still waiting for other plans to finish.

## Scope delta

Preserved. This proposal changes future delivery boundaries, not current
plans' accepted outcomes or any required safeguard.

## Assurance path

**Assurance path**: standard -- a narrow Maintainer-directed exception to the
governing/shipped-guidance trigger, not a change to runtime safeguards.
The Maintainer explicitly directs ordinary review without Security Review
for this change (chat, 2026-11-05):

> Please make sure that review of this happens at the right level (it does not need a Security review)

Use one ordinary Medium-capability proposal reviewer, not a Security or
External pass. No security-control change is authorized by this direction.
Future implementation follows the Decision and existing applicable checks.

**Elapsed**: approximately 20 minutes, including orientation and earlier
checkpoint bookkeeping; proposal-only time unknown. **Tokens**: unknown.
