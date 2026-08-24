# A convergent lifecycle: one artifact, one loop, a decider at every exit

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date opened**: 2026-08-21
**Status**: revising
**Assurance path**: high-assurance (governing doctrine and lifecycle)
**Supersedes**: `2026-08-20-claude-review-loop-termination` (accepted Revision 7,
superseded same day; its objective binds here, its scope does not)
**Touches**: `doctrine/lifecycle.md`, `doctrine/proposals.md`,
`doctrine/plans.md`, `doctrine/dual-review.md`, both `dev/` templates and their
shipped twins, `AGENTS.md` + shipped twin, `tools/lifecycle_planner.py` + twin
(refusals → warnings), lifecycle tests; `bootstrap/tests/conftest.py`
(security marker) and `docs/release-process.md` (the release-only run, §5)
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
inheritance granted 0 times in 19; six-round review chains. The weekly series
in `nimbleness-recovery` puts the composite figure at **~5% of all lines
written since July being functional product**, and splits the machinery three
ways: the adopter-facing capability layer (kept whole), the ~67k-line
deliberation complex (this proposal's target), and the security apparatus —
**which stays fully enabled, by Maintainer decision (2026-08-21)**; §5 moves
only *when* it runs. The superseded proposal softened the loop inside the
existing container. This one replaces the container, carrying forward its
three prizes: **C0** (risk posture), **C1** (editor authority), **C7**
(closure binding).

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
  surfaces `AGENTS.md` names, contract breaks, release/security ceremony, and
  **major new features** (Maintainer direction, 2026-08-21): a new user-facing
  capability, module, or subsystem takes a proposal before code, because the
  design space is wide, the commitment is durable, and the choice of *what to
  build* is a structure question — the Maintainer's lane. The change note
  covers work whose shape is already settled; a feature whose shape is the
  question deliberates first. Electable by author or Maintainer for anything
  else genuinely architectural. Existing review *floors* — who is independent
  enough to review — apply here untouched, including External where currently
  required; but a floor is not a reviewer's lever: tier assignment is the
  editor's (see §2). Uncertainty at triage resolves upward, as now.

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
* **Reviewers recommend; the editor assigns** (carrying the superseded
  proposal's extended C1). No reviewer sets a downstream review tier, demands
  an escalation, or prescribes the next round's scope — on either lane. A
  reviewer may *recommend* External review for a derived plan, on the record;
  the assignment is the editor's, made at the Decision, and a recorded
  recommendation never binds. The standing `AGENTS.md` trigger that converts a
  reviewer's `DISTINCT REVIEW REQUIRED` into a mandatory External plan review
  is retired with the token itself. Tier authority follows the same shape as
  the dissent rule above: the reviewer's view is preserved in the record, and
  the decision belongs to the role accountable for it.

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

### 5. The security suite becomes a release-only step

Maintainer decision, 2026-08-21, verbatim: *"The security suite should be a
release-only step."* The security apparatus — portable sweeps, content scan,
the differential-oracle gate and preflight, AST attestation — **stays enabled
with its full strength**; what moves is when its tests run. The security test
families (roughly half the suite's ~10-minute runtime; `test_gate_preflight`
alone is ~24%) are marked (`pytest -m security` / `-m "not security"`) and run
**in the release ceremony only**, where the supply-chain threat model bites.
The per-change loop runs the non-security suite (~5 minutes immediately,
falling as the deliberation complex's tests shrink). Boundary-B "full suite"
language reads accordingly: full = full non-security suite, with the security
families owned by the release ceremony that already exists as a separate
strict step. A change *to a security surface itself* still runs its own
family in the loop — the exclusion is temporal, not jurisdictional.

### 6. Transition

Prospective. In-flight accepted proposals may elect the standard lane: their
Decision summaries seed change notes (the three adopter-issue proposals are the
first candidates, at ≤150 lines each). C0's risk-posture text enters
`doctrine/dual-review.md` verbatim.

## What this deletes

The speed is mostly subtraction: the complete-restatement rule and its section
manifest; the `Plan readiness` vocabulary and the entire inheritance apparatus
(granted 0/19); constructibility as a named gate (it becomes a falsification
question); finding-class notation (C0's single test replaces four classes);
roughly half the lifecycle commits per change; and ~5 minutes from every
per-change verification run (§5 — moved to release, not deleted).

## Evidence / verification plan

Template and doctrine edits pass the claim, link, and neutrality gates;
planner demotion is covered by updating the existing lifecycle tests; the
security marker is verified in both directions (`-m security` collects the
named families; `-m "not security"` collects none of them) and the release
runbook names the full run as its step; the change-note path is exercised by
this proposal's own derived plan being written as one. Ongoing measurement is
staff gauges only, read at goodnight, no ledger: median artifact length,
rounds per artifact, open→archive days, adopter issue→fix sessions.

## Signals the change is wrong

* A shipped defect that a second design round would demonstrably have caught —
  audit each: was the miss brevity, or a missing measurement?
* Arcane escalations reach the Maintainer again — the lanes are misrouted.
* Change notes routinely exceed ~300 lines — the container was not the
  constraint, and the culture work (`nimbleness-recovery` 3.5) is the gap.
* Release-time security failures trace to changes that never touched a named
  security surface — §5's jurisdictional carve-out is drawn too narrow.

## Reviewer brief

One round expected. The load-bearing seam to attack: **triage** — construct a
change that causes hard-to-undo damage yet plausibly enters the standard lane.
The defense to test is that named high-risk surfaces force the deliberate lane
and triage uncertainty resolves upward. Second seam: in-place revision on the
standard lane — show a hazard `git log` does not already cover. Third seam:
§5's temporal exclusion — construct a non-security-surface change that
silently breaks a security family and is not seen until release; the defense
to test is the carve-out (security-surface changes still run their family in
the loop) plus the release run as the backstop.

## Review -- Codex (External) -- 2026-08-24

**Model**: GPT-5.6 (Codex)

Reviewed commit: b0e78e82ac4ce3a35e2613914665666ed3d7b613
Target: the complete opened contract, especially lane triage and C0, the standard-note lifecycle, the enforcement demotion, the security-suite split, and transition
Prior findings: none
Assurance path: high-assurance
**Tier**: External
**Findings**: raised (5 blocking)
**Plan readiness**: DISTINCT REVIEW REQUIRED

### Steelman

The proposal identifies a genuine operational cost and preserves the two parts
that matter most: an independent reader who tries to falsify the work, and a
durable decision record.  A short, deliberately scoped change note can be a
better tool than two long artifacts when its state, obligations, and escalation
boundary are equally explicit.  Separating security-family scheduling from
whether those tests exist is also a reasonable objective, provided the release
ceremony can prove it still owns the complete family.

### Findings

#### RCL-01 — BLOCKING: the triage rules do not give hard-to-undo work a determinate, safe lane

The two claimed defenses of the standard lane conflict.  Section 1 allows a
trivial change "even on a named surface" when it changes no contract, while the
next bullet makes every `AGENTS.md` high-risk surface deliberate.  Section 2
then asks whether shipping would cause hard-to-undo damage, but says that a
finding that fails that test is only a non-blocking note.  The polarity is not
defined: if the question's answer is yes, that is precisely the damage the
test names; if "fail" instead means no, the text still does not say what
answer requires escalation.  Either reading leaves the reviewer unable to
prevent the reviewer brief's own hard-to-undo standard-lane example.

Define a closed triage decision: the named high-risk set, the outcome of the
C0 question, the owner who may override it, and the resulting lane.  In
particular, a true hard-to-undo risk must force the deliberate lane (or an
explicit Maintainer disposition), not merely create a note.  Exercise the rule
with directed examples, including a no-public-contract release-ceremony edit,
so the trivial exception cannot silently swallow the mandatory lane.

#### RCL-02 — BLOCKING: the standard change note is not yet a constructible lifecycle artifact

The proposal names plan-status words but supplies no grammar for a parentless
change note: no required header fields, distinction from an ordinary plan,
review/response/decision record shape, next-owner table, event/metrics rule,
or exact meaning of a warning.  The existing plan machinery is not merely a
vocabulary list: `tools/lifecycle_planner.py`'s `PLAN_TRANSITIONS` and
`status_evidence_violations` bind `awaiting-plan-review` to plan-review
evidence, and its conformance check rejects a plan without a `**Plan review**:`
declaration.  Demoting that machinery to warnings without a separate grammar
means an incomplete note can look operationally complete while neither the
human nor the metrics reader can tell what review or closure it owes.

Add a compact standard-note schema and a transition table: state, next owner,
required record, evidence required to advance, whether the planner reports a
warning or refusal, and how deliberate plans retain the existing behavior.
Specify whether `cairn-event-v1` survives for notes and how a note is
distinguished from a deliberate plan in both self-hosted and shipped twins.
The lifecycle tests need directed malformed-note, missing-design-review,
closure, and deliberate-lane regression cases; writing this proposal's own
derived note is not evidence until that grammar and those transitions exist.

#### RCL-03 — BLOCKING: the proposed security-marker evidence can pass with no security tests selected

There is currently no registered or applied `security` pytest marker in the
repository.  The stated collection probe is therefore vacuous: at the reviewed
commit, `python -m pytest bootstrap/tests --collect-only -q -m security`
reported `no tests collected (4623 deselected)`.  A future check that merely
asserts the two marker expressions collect/omit the "named families" can keep
passing if the named set is empty, and the proposal never defines which nodes
belong to the security family, including cross-cutting tests whose failure
protects a security property.

Before changing Boundary B, publish a complete test-node or test-file
classification with its owner and the reason each member is security-only;
register the marker; and make the release command select that exact set in
release mode.  Pin both directions against a non-empty manifest and add
directed mutations that remove/reclassify a security node and prove the
membership test fails.  State the exact per-change and release commands,
including the release environment and broad-run guard, so "full" cannot mean
two incompatible collections.

#### RCL-04 — BLOCKING: the proposal omits the mandatory security preflight and its own transition assurance

This artifact has no `#### Security preflight` section at all.  The proposal
template requires either answers to S1--S5 for a security-touching/high-risk
change or an explicit N/A line; an absent answer is expressly a finding.  Here
the proposed work changes `bootstrap/tests/conftest.py`, whose release-mode
outcome rule and broad-run guard use environment-derived authority and whose
comments document a silent release-gate bypass if its hooks are shadowed.  It
also changes the release ceremony and makes current lifecycle refusals advisory.

Add the five answers against the accepted architecture, including the marker
classification/selection path, the release environment, failure direction,
and a mutation for every claimed enforcement point.  The derived plan must
also state how this change is verified under the *current* contract: a new
definition of non-security "full" cannot retroactively satisfy the current
release/trust-ceremony verification obligation for the implementation that
installs it.  Name the resulting Security Review and canonical pre-change
Boundary-B evidence explicitly rather than leaving their applicability to the
implementer.

#### RCL-05 — BLOCKING: the in-flight conversion has no authority or record-preserving migration

"In-flight accepted proposals may elect" does not name who elects, which
artifact statuses qualify, what happens to an already accepted scope and its
derived plan, or how the old and new records are linked.  The three alleged
first candidates are unnamed.  A Decision summary copied into a mutable
parentless note also loses the accepted artifact's explicit exclusions,
review basis, and any plan-review obligation unless the migration says exactly
which record remains authoritative.  This is a scope and audit migration, not
a formatting convenience.

Provide a per-artifact migration table with the source stem and commit,
current status, Maintainer authorization, target note/status, retained review
and verification obligations, link/archival treatment, and the commit that
effects the move.  Require a Maintainer allowance for any accepted outcome
that the condensed note does not retain.  Until that table exists, make the
new lane prospective for newly opened work only.

### Coverage and recommendation

**Covered**: the complete current contract at
`b0e78e82ac4ce3a35e2613914665666ed3d7b613`; current proposal and plan templates'
review, preflight, and event-block rules; the planner's plan transitions,
conformance, and shared status-evidence predicates; the release-mode and
broad-run hooks in `bootstrap/tests/conftest.py`; the current release command
in `docs/release-process.md`; and the collection-only marker falsifier above.

**Not covered / low confidence**: no implementation or revised contract exists,
so no proposed marker manifest, warning behavior, shipped-twin parity, or
release selection can yet be executed.  I did not run the full suite, as this
is a pre-implementation review and the request excludes it.

**Second-round recommendation**: recommended.  The revised contract should be
read again after it makes triage, the standard-note state machine, the
non-vacuous security selection, and the migration auditable.
