# Achievable plans that finish

**Author**: Codex (inherited runtime; exact model identifier unavailable)
**Status**: accepted
**Review**: usual
**Proposed tier**: standard -- one bounded doctrine/template change, with ordinary review as directed by the Maintainer
**Plan review**: required(Internal)
**Opened**: 2026-11-05
**In brief**: Give each plan a specific, verifiable goal it can achieve with available capabilities and a realistic time estimate, without losing the larger objective.

## Decision summary

A plan needs a specific, measurable, achievable, relevant and time-bounded
goal: SMART. This is about making plans achievable, not splitting work into
more plans. Its implementation, evidence and archive must be within reach
using available capabilities, without waiting for other plans or human
operations. A proposal can retain a larger sequence across releases.

Update existing templates and writing guides, not the lifecycle software.
The cost is more care in choosing achievable goals. If several plans really
are needed, each carries its applicable reviews, checks and closeout cost;
do not multiply plans by default. Put this early in v0.7 to guide remaining work.

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

1. **Make the goal SMART in existing sections.** Scope states the specific
   useful result and its relevance to the accepted objective. Acceptance
   criteria make completion observable, not a count of files or checkboxes.
   Sequence demonstrates achievability with available capabilities, evidence
   and authority, and gives a realistic work-window estimate with uncertainty.
   That estimate bounds planning; it is not a deadline that waives unfinished
   work or creates another spending guard. Add no SMART form or score.
2. **One independently finishable outcome per plan.** Atomic means useful,
   coherent delivery whose implementation, required checks, reviews and archive
   can finish without another unfinished plan. It does not mean one file,
   function, commit or arbitrary size limit. Internal chunks may depend on each
   other. Combine inseparable work rather than create dependency-linked
   microplans or a parent plan that waits for child plans.
3. **Sequence at the proposal and board level.** A proposal may authorize
   multiple plans. In its existing Proposal section, name each delivery outcome,
   prerequisites and intended release or capability. Keep later work queued
   on the existing board with its source and revival condition; do not open an
   active implementation plan before its prerequisites are delivered. Archive
   the accepted proposal at the first plan opening under the existing rule;
   preserve the remaining authorized outcomes on the board, linked to that
   immutable source. Later plans cite the same proposal, not new Decisions
   for already authorized work. A changed design still needs existing authority.
4. **Depend on available capabilities, not future plan completion.** A shipped
   helper is a valid prerequisite. A plan promising that helper is not. A
   shared batch may save editing or testing, but no plan waits for another
   plan's review, archive or release label merely to complete its own evidence.
   Required integration evidence remains required; if the outcome cannot be
   verified without future work, queue it or include that work in the same
   coherent plan. Never substitute mocks for owed functional evidence.
5. **No scheduled Maintainer action to reach archive.** Preserve the existing
   separate human-operation waits, evidence and authorization boundaries.
   Helping decide whether or how to handle a deferral remains the Maintainer's.
   Unexpected scope/permission questions still stop for existing authority;
   they are not license to design a human-only final chunk. No failed check,
   defect, required review or missing scientific result becomes a board chore
   merely to finish a plan. Archive never authorizes signing or release.
6. **Preserve scope without a new tracker.** Choosing delivery boundaries never concedes
   an accepted outcome. Each authorized outcome must remain assigned to its
   plan or queued board entry; moving it later needs existing scope/scheduling
   authority. Early plan archive is not completion of the whole proposal.
   Use existing Scope, Sequence and Acceptance criteria, not new mandatory
   sections, statuses, sidecars or a dependency checker.

One plan may include a helper and its consumers when together they form an
achievable goal. If a visual-review goal instead requires a separately
authorized future Git capability, queue that goal until the capability exists;
do not open a plan already unable to finish. Neither choice drops the goal.

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

Apply the guidance to one coherent helper-and-consumer goal, a goal depending
on future capability, a later-version goal and a missing-check/human-ceremony
case. Show specificity, completion evidence, feasibility, relevance and a
bounded estimate, where every original outcome remains, and whether archive is allowed. Run
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

## Review -- Codex gpt-6.1-terra -- 2026-11-05

Reviewed commit: `df8faf54`

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: coherent, independently verifiable outcomes address real waits without mandating microplans or removing checks; a standard plan is worth coordinating the local and shipped wording and tests, although it adds a plan review -- Proposal 1, 3-5 and Documentation / doctrine surface; `dev/plans/2026-11-05-architecture-and-reuse.md`, Sequence.
2. **Best alternative.** Keep existing guidance and handle dependencies case by case: no doctrine rollout or extra plan-writing rule, but broad plans can remain open despite earlier useful delivery -- `dev/plans/2026-11-04-suite-consolidation.md`, C4 and Security plan review.
3. **What would show it wrong?** Trial the four proposed examples and track later outcomes through first archive to their next plan; lost scope, unmet evidence treated as complete, or multiplying tiny plans would challenge the design -- Proposal 2-5; Evidence / verification plan.

The Maintainer's narrow direction, from chat, 2026-11-05, was: "Please make sure that review of this happens at the right level (it does not need a Security review)". This is the ordinary pass, not a Decision or Security Review.

**N1 (non-blocking):** The summary says no more reviews, but multiple independently delivered plans can each require plan and code reviews. State that possible recurring cost alongside the saved waiting, without suggesting extra reviews for existing plans; the author can close this by clarifying the tradeoff. Evidence: Proposal 2 and `dev/plans/_template.md`, Lifecycle.

**Coverage:** Read the committed proposal, template, governing rules, both cited dependencies and existing archive guidance. Checked preservation of later scope, human-operation and authority stops, adopter guidance and no runtime machinery by inspection. Did not validate future implementation, exercise mutations, assess Security, or independently inventory every installed surface.

## Response -- Codex -- 2026-11-05

**N1: accept.** Decision summary now names each additional plan's recurring
review, check and closeout cost; multiple plans are an option, not the goal.

The Maintainer clarified in chat: "The idea isn't to \"split work\", it's to
make plans achievable. SMART goals". The opening and Proposal now organize
existing sections around a specific useful result, observable completion,
available capabilities, relevance and a realistic work estimate. One coherent
plan is preferred when it can achieve the goal. The examples include a helper
and its consumers together; none of the original scope, later-work visibility,
independent-completion or human-operation safeguards is removed. This clarifies
the requested purpose, not a wider feature or an implementation authorization.

The ordinary round is closed; awaiting the Maintainer's Decision. No Security
Review or further clearing pass is added. **Elapsed**: unknown. **Tokens**: unknown.

## Decision -- Maintainer (scribed by Codex gpt-6-luna) -- 2026-11-05

**Tier**: standard

**ACCEPTED.** The Maintainer's authorization, verbatim:

> "Okay, I accept the SMART-goals proposal. Go ahead and record the Decision and implement it, while keeping the other v0.7 work moving."

Plan review is `required(Internal)`; usual proposal, plan and code reviews
apply. No Security Review is required, as previously directed by the
Maintainer: "Please make sure that review of this happens at the right level
(it does not need a Security review)".

The accepted operative text is the revision at `093fda0c`. It makes plans
achievable through SMART goals, not splitting work by default; uses existing
guides and live/shipped templates; adds no checker or status; and preserves
scope, checks and separate human-operation waits. Each genuinely additional
plan carries its applicable reviews, checks and closeout; no new form or
checker is added.

**Elapsed**: unknown. **Tokens**: unknown.
