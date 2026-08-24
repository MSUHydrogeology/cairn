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

## Response + Revision 1 -- Claude -- 2026-08-24

**Concurrency note, first.** The review's reviewed commit is `b0e78e8`. Commit
`0ebd3a7` ("reviewers recommend; the editor assigns", §2's last bullet) landed
while the review was being written — it is part of the operative contract below
but was not read by this reviewer. It responds to no finding; round 2 should
read it fresh. Inline revision ended the moment this review landed; everything
from here is append-only.

**All five findings are accepted; RCL-01 and RCL-03 were reproduced before
acceptance** (`pytest --collect-only -q -m security` → `no tests collected
(4623 deselected)`, exactly as stated). Two are accepted with modification:
the full detail RCL-02 and RCL-05 request is split between this contract
(the grammar, the authority rule) and the derived plan (the directed tests,
the per-artifact table), and the modification is named in each disposition.

| finding | disposition |
|---|---|
| RCL-01 (triage polarity) | **Accept.** Closed triage procedure in §1; C0 polarity defined (damage = yes → blocking; blocking on the standard lane forces escalation or an explicit Maintainer disposition); the "even on a named surface" clause is withdrawn and replaced by a three-condition defect-repair carve-out. |
| RCL-02 (note grammar) | **Accept with modification.** §2a adds the note schema and transition table, warning semantics, twin parity, and event survival. The directed test list (malformed note, missing design review, closure, deliberate-lane regression) is adopted verbatim as derived-plan chunks — enumerating test nodes is plan-level detail. |
| RCL-03 (vacuous marker) | **Accept.** §5 now requires a committed non-empty manifest with owner and reason per member, marker registration, membership checked against the manifest in both directions, a directed removal mutation that must fail, and exact commands. Release runs the **full** suite — stronger than a security-only selection and immune to an empty-set pass. |
| RCL-04 (missing preflight) | **Accept.** S1–S5 answered below against the accepted architecture. The implementation installing this split is verified under the **current** contract (full-suite Boundary B, pre-change definition) and takes a **Security Review** — declared in the contract, not left to the implementer. |
| RCL-05 (migration authority) | **Accept with modification.** The lane is prospective for newly opened work. The three candidates are named; each migrates only on recorded per-artifact Maintainer authorization, the accepted proposal remains the authoritative scope record, and dropped outcomes need explicit Maintainer allowance under the standing rule. The per-artifact table lives in the migration commit itself, not here. |

**On `Plan readiness: DISTINCT REVIEW REQUIRED`.** Recorded and preserved. This
proposal lands under the rules it replaces, so the token stands in the record;
under the Maintainer's direction of 2026-08-24 (and §2's operative rule), tier
assignment is the editor's at the Decision. Recommendation with default: the
derived plan takes **Internal** review — the contract below is small, its
enforcement changes are advisory demotions, and the security-relevant piece
carries its own declared Security Review, which is the stronger instrument.

### Withdrawn / superseded commitments

* *"even on a named surface, when it changes no contract"* (trivial lane) —
  withdrawn; replaced by the defect-repair carve-out in §1 (RCL-01).
* *"A finding failing that test is recorded as a note"* — withdrawn as
  ambiguous; polarity now explicit in §2 (RCL-01).
* The two-direction marker check as sufficient evidence — superseded by the
  manifest-anchored membership test with a directed mutation (RCL-03).
* Release-mode running a security-only selection — superseded: release runs
  the full suite (RCL-03).
* *"In-flight accepted proposals may elect the standard lane"* as written —
  superseded by the authorized-migration procedure in §6 (RCL-05).

---

## THE COMPLETE CURRENT CONTRACT (Revision 1)

Supersedes the opened Proposal section in full. Objective, Context, header
fields, and the review record above are unchanged.

### 1. Three lanes, chosen by a closed triage procedure

Evaluate in order; the first match assigns the lane.

1. **Deliberate** if the change (a) touches a high-risk surface `AGENTS.md`
   names, (b) breaks or widens a contract, (c) is release or security
   ceremony, or (d) is a **major new feature** — a new user-facing capability,
   module, or subsystem (Maintainer direction, 2026-08-21: what-to-build is a
   structure question). One carve-out crosses rule 1: a **defect repair** —
   all three of (i) a failing-test reproduction, (ii) restores documented or
   intended behavior with no contract change, (iii) the touched surface's own
   test family runs in the loop — takes the trivial lane even on a named
   surface. An edit that changes what a ceremony or surface *does* is not a
   defect repair and stays deliberate, whether or not a public contract moved.
2. **Trivial — just commit** for defect repairs meeting the carve-out and for
   the existing just-commit class (typo, docstring, self-contained helper):
   code + test + one code review.
3. **Standard — the change note** for everything else.

The deliberate lane is today's two-stage, unchanged: review *floors* — who is
independent enough — stay as they are, including External where currently
required; a floor is not a reviewer's lever (§2). Election upward is open to
author or Maintainer; **uncertainty resolves upward**, and only the
Maintainer may override the procedure's result, on the record.

### 2. One design review, one code review, each with an exit

* **C0 is the blocking test, with explicit polarity**: *would shipping this
  cause damage that is hard to undo?* **Yes → blocking.** No → the finding is
  recorded as a `note` or `nit` and does not block. A blocking finding on a
  standard-lane artifact additionally forces one of: escalation to the
  deliberate lane, or an explicit recorded Maintainer disposition. Full
  review weight remains on the deliberate lane.
* **Every review includes at least one falsification attempt with its output
  pasted in.** A prose-only read is an incomplete review.
* **A blocking finding binds its closure evidence when raised** (C7,
  `Closes on: <evidence>`); the revision carrying that evidence closes it
  without a fresh full read.
* **Round 2 exists only to check round 1's closure evidence.** After round 2
  the author decides every open item — accept, or decline with a one- or
  two-sentence defense — dissent recorded, work proceeds. Questions travel to
  the Maintainer only by expertise routing: science in domain terms any time;
  structure as recommendation-with-default; implementation detail never.
* **The editor may end any loop at any time** over open findings by naming
  them (C1). A clearing verdict requires a whole-artifact read.
* **Reviewers recommend; the editor assigns.** No reviewer sets a downstream
  review tier, demands an escalation, or prescribes the next round's scope —
  on any lane. A recorded recommendation never binds; the `AGENTS.md` trigger
  converting `DISTINCT REVIEW REQUIRED` into mandatory External plan review
  retires with the token. The reviewer's view is preserved in the record; the
  decision belongs to the role accountable for it.

### 2a. The change note is a defined artifact (RCL-02)

**Header fields** (all required): `Author`, `Date opened`, `Status`,
`Lane: standard` (what distinguishes a note from a deliberate plan, in both
the self-hosted and shipped twins), `Risk` (the C0 answer, one sentence),
`Review` (who reads it), `Related`. **Sections**: Why / What / Approach /
Verification / Risk. Target ≤150 lines.

**Transitions** (state → next owner; evidence required to advance):

| state | next owner | to advance |
|---|---|---|
| `awaiting-plan-review` | reviewer | appended design review (§2) |
| `ready-to-implement` | author | author response to any blocking findings |
| `implementing` | author | implementation + verification record appended |
| `awaiting-code-review` | code reviewer (not the author) | appended code review |
| `revising-code` | author | closure evidence per C7 |
| `ready-to-archive` | editor/author | archive move |

**Warning semantics**: on the standard lane the planner reports a malformed or
unknown note as a **warning naming the missing element** — never a refusal
(§4). The deliberate lane keeps today's conformance behavior. **Events**:
change notes emit the same `cairn-event-v1` records as plans, keyed by stem,
so longitudinal metrics survive the merge. **Derived-plan tests** (adopted
from RCL-02 verbatim): directed cases for a malformed note, a missing design
review, closure binding, and a deliberate-lane regression.

### 3. Write once, restate never

The change note's operative sections revise **in place** while in design;
reviews, responses, and decisions **append** and are never edited. No
complete-restatement requirement on this lane: at ≤150 lines, `git log`
preserves every prior state, and silent section loss cannot hide in two
pages. The deliberate lane keeps full append-only as today.

### 4. Tools advise, humans decide

All lifecycle checks on trivial and standard lanes **warn, never refuse**
(Maintainer direction, 2026-08-21). Hard refusal survives only for genuine
safety: scaffold containment and release trust-root verification. An artifact
the planner does not yet parse is a warning, not a stranded file.

### 5. The security suite becomes a release-only step (RCL-03 folded in)

Maintainer decision, 2026-08-21, verbatim: *"The security suite should be a
release-only step."* The security apparatus — portable sweeps, content scan,
the differential-oracle gate and preflight, AST attestation — **stays enabled
at full strength**; what moves is when its tests run.

* **Membership is manifest-anchored.** A committed manifest lists every
  security-family test file with an owner and a one-line reason; the `security`
  pytest marker is registered in `bootstrap/tests/conftest.py` and applied to
  exactly the manifest's members. The membership check asserts (a) the
  manifest is **non-empty**, (b) `-m security` collects exactly the manifest's
  files, (c) `-m "not security"` collects none of them. A directed mutation —
  removing the marker from one manifest member — must fail the check; the
  derived plan runs it and records the output.
* **Commands, exactly.** Per-change (Boundary B and the inner loop):
  `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests -m "not security"
  --quality-gate-shuffle-seed=0`. Release: the release ceremony runs the
  **entire suite, no deselection** — strictly stronger than a security-only
  selection and immune to an empty-set pass.
* **The carve-out is temporal, not jurisdictional**: a change to a security
  surface still runs that surface's family in the loop.
* **Installing this split is itself a current-contract change**: its
  implementation runs the **pre-change canonical Boundary B** (full suite,
  current definition) and takes a **Security Review** — it touches
  `bootstrap/tests/conftest.py`'s release-mode and broad-run hooks and the
  release ceremony, which are trust-ceremony surfaces today.

#### Security preflight (RCL-04)

* **S1 — Who supplied it?** The marker is applied inside the test files being
  classified — supplied by reference by the object under decision. That is why
  membership is cross-checked against the separately committed, separately
  reviewed manifest: neither alone admits a test to the release-only set. The
  release-mode selection is driven by the release environment supplied by the
  Maintainer running the ceremony, not by repository content.
* **S2 — Can it fail?** Mutation: remove the `security` marker from one
  manifest member → the membership check fails (must be run and recorded by
  the derived plan; not yet run — no marker exists at this commit, which is
  RCL-03's finding). The empty-manifest case fails closed via the non-empty
  assertion. The check compares two independently supplied sets, so it does
  not derive its expectation from the object it checks.
* **S3 — What fires it, over what?** The two commands above; the per-change
  form is selected by Boundary B, the full run by the release runbook step in
  `docs/release-process.md`, whose prose the derived plan updates and quotes
  so command and description agree.
* **S4 — Which way does it break?** An unmarked or newly added test defaults
  into the per-change set — it runs *more* often, not less. Omission from the
  manifest cannot reduce coverage below today at release, because release
  runs everything.
* **S5 — Who still wins?** Assumed attacker: cannot land commits on trunk. An
  attacker who can commit may edit marker and manifest together; that class
  is closed by **enumeration** (review of manifest diffs), not by
  construction — stated plainly. Release-artifact integrity remains bound by
  the gate anchor, which this change does not touch.

### 6. Transition (RCL-05)

**Prospective: the standard lane applies to newly opened work.** The three
named migration candidates are `2026-08-20-claude-portable-sweeps-cannot-run`,
`2026-08-20-claude-adopt-into-existing-tree`, and
`2026-08-20-claude-scanner-claim-scope` (accepted, plans not yet opened). Each
may migrate **only** on a per-artifact Maintainer authorization recorded in
the artifact, via a migration commit that names the source stem and accepted
commit, the retained obligations (each proposal's declared Security Review
and plan-review requirements carry unchanged), and the link back. **The
accepted proposal remains the authoritative scope record**; the note
implements it, and any accepted outcome the note does not retain requires the
Maintainer's explicit allowance under the standing scope-reduction rule.
C0's risk-posture text enters `doctrine/dual-review.md` verbatim.

### What this deletes

The complete-restatement rule and its section manifest; the `Plan readiness`
vocabulary and inheritance apparatus (granted 0/19); constructibility as a
named gate (it becomes a falsification question); finding-class notation
(C0's single test replaces four classes); roughly half the lifecycle commits
per change; and ~5 minutes from every per-change verification run (moved to
release, not deleted).

### Evidence / verification plan

Template and doctrine edits pass the claim, link, and neutrality gates.
Planner demotion and the change-note grammar are covered by updating the
lifecycle tests plus the four directed cases in §2a. The security-marker
membership test and its removal mutation run with output recorded (§5). The
release runbook names the full-suite run as its step. The change-note path is
exercised by this proposal's own derived plan being written as one — as
evidence of usability only; the grammar and transitions of §2a are the
contract it is checked against. Ongoing measurement stays staff gauges read
at goodnight: median artifact length, rounds per artifact, open→archive days,
adopter issue→fix sessions.

### Signals the change is wrong

* A shipped defect a second design round would demonstrably have caught —
  audit: was the miss brevity, or a missing measurement?
* Arcane escalations reach the Maintainer again — the lanes are misrouted.
* Change notes routinely exceed ~300 lines — the container was not the
  constraint; the culture work (`nimbleness-recovery` 3.5) is the gap.
* Release-time security failures trace to changes that never touched a named
  security surface — the temporal carve-out is drawn too narrow.
* The migration path is used without its recorded authorization — §6's
  procedure is too heavy for practice and is being routed around.

### Reviewer brief (round 2)

Read the complete contract above, plus §2's final bullet (`0ebd3a7`, unread
in round 1). Seams: (1) triage — construct a hard-to-undo change that still
lands standard under the closed procedure; (2) §2a — is the transition table
executable as written; (3) §5 — the manifest/marker cross-check and its
mutation; (4) §6 — can a migration lose an obligation without tripping the
allowance rule.

## Review -- Codex (External) -- 2026-08-24 (round 2)

**Model**: GPT-5.6 (Codex)

Reviewed commit: c2bc3d340f767773d4600c3689e13846a22c7311
Target: the complete current contract (Revision 1), including the concurrent `0ebd3a7` review-tier expansion, the standard-note state machine, security selection, and transition
Prior findings: RCL-01–RCL-05 (closure read)
Assurance path: high-assurance
**Tier**: External
**Findings**: raised (3 blocking)
**Plan readiness**: DISTINCT REVIEW REQUIRED

### Steelman

Revision 1 meaningfully improves the earlier contract.  C0 now has a usable
polarity; the note has a declared lane discriminator and minimum fields; and
the marker proposal no longer accepts an empty security selection.  Retaining
the accepted proposal as the migration's authoritative scope record is also
the right direction.  The remaining problems are at the seams where the new
rules must determine an actual transition or release outcome.

### Findings

#### RCL-02 — BLOCKING, not closed: §2a has no valid path through a blocking design review

The table sends `awaiting-plan-review` directly to `ready-to-implement` when a
design review is appended, then says the author response to blocking findings
is what advances `ready-to-implement`.  It supplies neither a
`revising-plan`-equivalent state nor a condition that the design review cleared
before the note becomes ready.  The code-review half has the same omission:
`awaiting-code-review` lists an appended code review, but no branch from a
raised review to revision or from a clearing review to `ready-to-archive`.
This contradicts C7's closure binding and makes the proposed
missing-design-review test too weak: a note can carry a raised review, declare
itself ready, and have no defined record that closes it.  "Warn, never refuse"
changes the disposition of a detected violation; it does not supply the
missing state and evidence rule.

Replace the table with complete directed transitions, including the from/to
states, clearing versus raised-review conditions, the response/closure record
shape, and the next owner at each branch.  The standard-note tests must then
falsify a raised design review without closure and a raised code review without
closure, as well as the clearing paths.  State explicitly which warnings are
emitted for each invalid advance and prove a deliberate plan still refuses the
same invalid advance.

#### RCL-03 — BLOCKING, not closed: the release-only split still lacks the release command and the security-surface branch

Section 5 labels its commands "exactly," but it gives only the ordinary
`-m "not security"` command.  "The release ceremony runs the entire suite" is
not a command and omits the release environment that makes skips, xfails, and
xpasses fail closed.  The current release runner is
`bootstrap/security_check.py`: it sets `CAIRN_RELEASE_GATE_ACTIVE=1`, runs the
whole suite, and also owns the Bandit, repository, and quality-gate phases.
Replacing that executable release path with an unqualified full pytest command
would weaken the ceremony while still meeting the prose.  Conversely, the
stated security-surface carve-out cannot use the one supplied per-change
command, because that command deselects the very family it says must run.

Name the exact release entry point and environment, and state whether it
remains the current security-check runner or a replacement with every phase
accounted for.  Add the exact alternate per-change command/mapping for a
security-surface change.  Exercise a release-mode skipped/xfail fixture and a
security-surface change so both paths demonstrate the claimed fail-closed and
carve-out behavior.  This closes the exact-command part of RCL-03 rather than
leaving it for the implementer to infer.

#### RCL-06 — BLOCKING: the concurrent tier-authority expansion is unaccounted and tries to retire the review that bounds this plan

Commit `0ebd3a7` is a material extension of the opened contract, not merely a
clarification: it retires the current `AGENTS.md`/`doctrine/dual-review.md`
rule that turns an External reviewer's `DISTINCT REVIEW REQUIRED` into a
mandatory External plan review.  That is the same rule this External review
already invoked.  Revision 1 repeats the retirement at §2, but its withdrawal
ledger does not name the earlier commitment that deliberate-lane review floors
were "untouched," nor does the verification plan map the affected doctrine,
template, planner, and shipped-twin behavior.  Calling the result an editor
assignment also conflates two distinct decisions: the Maintainer's ordinary
choice to spend an optional extra pass, and a lifecycle-declared independent
review floor.

Treat this as a scope expansion in the current contract: add its withdrawn
commitment and rationale to the ledger; enumerate every rule and twin whose
meaning changes; and provide directed tests for both sides (a recorded
`DISTINCT REVIEW REQUIRED` no longer imposes External only if the accepted new
rule says so, while an independently declared `required(External)` and every
Security Review remain non-downgradable).  Until that change is accepted, the
current rule still binds this proposal's derived plan, so this review's
`DISTINCT REVIEW REQUIRED` cannot be reclassified to Internal by the proposal
it is reviewing.

### Coverage and recommendation

**Covered**: Revision 1 and its response/withdrawal ledger; the concurrent
`0ebd3a7` diff; current plan lifecycle and event grammar in
`dev/plans/_template.md`; planner transition and evidence predicates in
`tools/lifecycle_planner.py`; current review-floor and
recommend-and-decide rules in `AGENTS.md` and `doctrine/dual-review.md`; and
the actual release-mode entry point in `bootstrap/security_check.py`.

**Not covered / low confidence**: no implementation, marker manifest, or
change-note parser exists yet, so the proposed warning, membership, release,
and twin-parity behavior cannot be executed.  This is a closure read by the
same External reviewer, not a new structurally independent pass.  I did not
run the full suite.

**Second-round recommendation**: recommended after a complete revision closes
the three findings.  The tier-authority widening particularly needs an
independent read because it changes the mechanism that allocates that read.
