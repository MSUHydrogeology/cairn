# A convergent lifecycle: one artifact, one loop, a decider at every exit

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date opened**: 2026-08-21
**Status**: awaiting-review
**Assurance path**: high-assurance (governing doctrine and lifecycle)
**Supersedes**: `2026-08-20-claude-review-loop-termination` (accepted Revision 7,
superseded same day; its objective binds here, its scope does not)
**Touches**: `doctrine/lifecycle.md`, `doctrine/proposals.md`,
`doctrine/plans.md`, `doctrine/dual-review.md`, both `dev/` templates and their
shipped twins, `AGENTS.md` + shipped twin, `tools/lifecycle_planner.py` + twin
(refusals → warnings), lifecycle tests
**Related**: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md`
**Plan review**: required(Internal) — this lands under the rules it replaces

## Objective

The Maintainer's charge, verbatim: *"make the
proposal->review->plan->review->code->review->archive process faster and more
convergent. Keeping in mind the balance this whole project is trying to
achieve."* Faster means fewer artifacts, rounds, and restatements. Convergent
means every loop has a termination rule and a named decider. Balance means
independent review with real falsification stays, and recorded decisions stay.

## Context

The costs are measured and recorded elsewhere (`nimbleness-recovery`; the
superseded proposal): ~90 lines of prose per shipped line of code across the
recent corpus; median proposal ~900 lines and median plan ~1,800; readiness
inheritance granted 0 times in 19; six-round review chains. The superseded
proposal softened the loop inside the existing container. This one replaces the
container, carrying forward its three prizes: **C0** (risk posture), **C1**
(editor authority), **C7** (closure binding).

## Proposal

### 1. Three lanes, chosen at triage

* **Trivial — just commit.** The existing rule, re-armed: a bug fix with a
  failing-test reproduction is code + test + one code review, even on a named
  surface, when it changes no contract.
* **Standard — the change note (new default).** One artifact replaces
  proposal + plan: a file in `dev/plans/<slug>.md` opening with *Why / What /
  Approach / Verification / Risk*, target ≤150 lines. It reuses the existing
  plan status vocabulary (`awaiting-plan-review → ready-to-implement →
  implementing → awaiting-code-review ↔ revising-code → ready-to-archive →
  archived`) and needs no parent proposal.
* **Deliberate — today's two-stage, unchanged.** Mandatory for the high-risk
  surfaces `AGENTS.md` names, contract breaks, and release/security ceremony;
  electable by author or Maintainer for anything genuinely architectural.
  Existing review floors (including External) apply here untouched. Uncertainty
  at triage resolves upward, as now.

### 2. One design review, one code review, each with an exit

* **The blocking test is C0's**, carried verbatim: *would shipping this cause
  damage that is hard to undo?* A finding failing that test is recorded as a
  note and does not block. Full weight remains on the deliberate lane.
* **Every review includes at least one falsification attempt with its output
  pasted in.** One measurement outranks a page of argument; a prose-only read
  is an incomplete review.
* **A blocking finding binds its closure evidence when raised** (C7:
  `Closes on: <evidence>`). The revision carrying that evidence closes it
  without a fresh full read.
* **Round 2 exists only to check round 1's closure evidence.** After round 2
  the author decides every open item — accept, or decline with a one- or
  two-sentence defense — dissent is recorded, work proceeds. Questions travel
  to the Maintainer only by expertise routing: science in domain terms any
  time; structure as a recommendation with a stated default; implementation
  detail never.
* **The editor may end any loop at any time** over open findings by naming
  them (C1). A clearing verdict requires a whole-artifact read — cheap at two
  pages, which is the point.

### 3. Write once, restate never

The change note's operative sections are revised **in place** while the note is
in design; reviews, responses, and decisions **append** and are never edited.
No complete-restatement requirement exists on this lane: at ≤150 lines, `git
log` preserves every prior state at zero authoring cost, and the
silent-section-loss failure that restatement caused cannot hide in two pages.
The deliberate lane keeps full append-only as today.

### 4. Tools advise, humans decide

All lifecycle checks on trivial and standard lanes **warn, never refuse**
(Maintainer direction, 2026-08-21). Hard refusal survives only for genuine
safety: scaffold containment and release trust-root verification. This also
makes the migration safe — an artifact the planner does not yet parse is a
warning, not a stranded file.

### 5. Transition

Prospective. In-flight accepted proposals may elect the standard lane: their
Decision summaries seed change notes (the three adopter-issue proposals are the
first candidates, at ≤150 lines each). C0's risk-posture text enters
`doctrine/dual-review.md` verbatim.

## What this deletes

The speed is mostly subtraction: the complete-restatement rule and its section
manifest; the `Plan readiness` vocabulary and the entire inheritance apparatus
(granted 0/19); constructibility as a named gate (it becomes a falsification
question); finding-class notation (C0's single test replaces four classes);
and roughly half the lifecycle commits per change.

## Evidence / verification plan

Template and doctrine edits pass the claim, link, and neutrality gates;
planner demotion is covered by updating the existing lifecycle tests; the
change-note path is exercised by this proposal's own derived plan being
written as one. Ongoing measurement is staff gauges only, read at goodnight,
no ledger: median artifact length, rounds per artifact, open→archive days,
adopter issue→fix sessions.

## Signals the change is wrong

* A shipped defect that a second design round would demonstrably have caught —
  audit each: was the miss brevity, or a missing measurement?
* Arcane escalations reach the Maintainer again — the lanes are misrouted.
* Change notes routinely exceed ~300 lines — the container was not the
  constraint, and the culture work (`nimbleness-recovery` 3.5) is the gap.

## Reviewer brief

One round expected. The load-bearing seam to attack: **triage** — construct a
change that causes hard-to-undo damage yet plausibly enters the standard lane.
The defense to test is that named high-risk surfaces force the deliberate lane
and triage uncertainty resolves upward. Second seam: in-place revision on the
standard lane — show a hazard `git log` does not already cover.
