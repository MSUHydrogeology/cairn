# The scope-reduction trap

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-11
**Status**: revised
**Touches**: `doctrine/dual-review.md`; `doctrine/proposals.md`;
`doctrine/plans.md`; the proposal and plan templates, self-hosted and shipped;
`tools/lifecycle_planner.py` and its twin; `templates/core/dev/agent_collaboration.md`;
`AGENTS.md` and `templates/core/AGENTS.md` (expanded at Round 2)
**Related**: the guide star's Anchor 17 and "Restraint as design center" (the
counterweight this must not collide with); `2026-08-11-claude-metrics-events-not-prose`
(the worked instance)
**Plan review**: required(External) — a change to review norms, shipped to every
adopter, proposed by the author of the instance that prompted it

## Context

Review has a systematic bias toward narrowing, and Cairn's doctrine does not
name it.

The asymmetry is structural. A reviewer recommending a reduction bears no cost
for it and looks prudent. A reviewer recommending expansion looks reckless.
"Do less" is also close to unfalsifiable — the wider version never runs, so
nobody ever demonstrates it would have been better. Each individual narrowing
is defensible on its own terms; the aggregate is what does the damage.

**Maintainer observation, and the trigger for this proposal:** the pattern is
recurrent, not occasional. Changes that begin at an already-modest scope are
narrowed further in review until what lands is vanishingly small, *after* the
full deliberation cost has been paid.

That last clause is the expensive part. Deliberation is sunk by the time review
narrows the work. Cutting scope afterwards means paying full price for the
thinking and shipping a fraction of the change — a worse ratio than either
doing the whole thing or never deliberating at all.

And it produces worse software, not safer software. **A wider scope is often
what reveals the pattern.** Narrowed to the immediate case, a change fixes a
symptom; the shape that caused it survives and recurs, and the recurrence costs
another full deliberation.

### The worked instance

`2026-08-11-claude-metrics-events-not-prose` opened with three parts: retire
prose-derived metrics, state the principle in doctrine, and move to emitting
metrics at the lifecycle transition instead of re-deriving them from historical
prose. Part 3 was the general pattern — the other two are symptom fixes for it.

External review correctly found Part 3 underspecified: "may belong in its own
proposal" left two incompatible plans valid. The finding was right. **The
author's resolution went the easy direction** — cut Part 3 — rather than the
hard one, which was to specify it. The proposal that emerged is smaller,
decidable, and addresses the symptom while the cause stays open.

The reduction is also nearly invisible. Append-only preserves the original
three-part section, so the delta is *recoverable by diffing*, but the revision
says only "supersedes the Proposal section above where they conflict." Nobody
reading top to bottom is told the proposal shrank. And its deferral names no
home: "deferred to a named follow-up" names nothing.

### What today's doctrine covers, and where the gap is

`doctrine/proposals.md` requires every deferred follow-up to carry a recorded
disposition — but that binds at **archive precondition**, which is the
plan-archive stage. Between "review cut this" and "someone archives the
resulting plan," removed scope lives nowhere but in prose inside a superseded
section. That window is unguarded, and it is where work disappears.

`doctrine/dual-review.md` names the **clean-pass trap** — a review that finds
nothing on a complex change should be met with skepticism. This proposal adds
its mirror: a review that shrinks a change should be met with the same
skepticism, and for the same reason. Both are failure modes that feel like
diligence.

## Proposed paths

* `doctrine/dual-review.md` — the review norm, beside the clean-pass trap
* `doctrine/proposals.md` — visibility and homing of a reduction
* `templates/core/dev/agent_collaboration.md` — the adopter-facing statement

## Proposal

### 1. Name the trap in the review norms

A new section in `doctrine/dual-review.md`, sibling to the clean-pass trap:

> **The scope-reduction trap.** Narrowing is the path of least resistance in
> review. It costs the reviewer nothing, reads as prudence, and can never be
> shown wrong, because the wider version is never built. Treat a proposed
> reduction with the same skepticism as a clean pass.
>
> A reviewer recommending a reduction states **what is lost** and **why the
> narrower change still addresses the cause** — not merely that it is smaller
> or more decidable. "This is too large" is not a finding; "this is too large
> and here is the part that does not belong, and here is why the rest still
> reaches the root" is.

### 2. Default to specify, not cut

When a review finds a part underspecified, the author's default resolution is
to **specify it**. Cutting is available and sometimes right, but it is the
lazy resolution and it should have to argue for itself.

Concretely: an author who resolves an underspecification finding by removing
the scope says why specifying it was rejected. That sentence is the whole
mechanism — it makes the easy path visible as a choice.

### 3. A reduction is stated as a delta, and homed at the moment it happens

Two requirements on any revision that narrows the reviewed scope:

* **Say so.** The revision states plainly that scope was reduced, and what
  left. A reader must not have to diff two sections to learn that the proposal
  shrank after review.
* **Home it immediately.** Removed scope gets a named destination when it is
  removed — a follow-up artifact, or a `dev/PLANNING.md` row with a revival
  condition — not at archive time. "Deferred to a follow-up" that names no
  follow-up is not a deferral; it is a deletion with better manners.

### 4. The counterweight, stated so this cannot be misread

This must not license scope creep, and it does not contradict restraint. The
two operate on different axes, and today's doctrine conflates them:

> **Cut ceremony. Do not cut reach.** Deliberation should be as cheap as it can
> be. The change that deliberation authorizes should be as wide as the pattern
> it addresses. Reducing the process is almost always right; reducing the
> change is usually the expensive kind of easy.

A proposal that grows *because nobody said no* is still a defect, and the
existing triage still applies.

## Rationale

Cairn's review model is its central mechanism, so a systematic bias inside
review is a defect in the thing Cairn is for. This particular bias is
self-concealing: every instance looks like good judgment, and the cost appears
only in aggregate as a long deliberation record with little shipped behind it.

The rate-limit gate is cleared on **recurrence**, supplied by the Maintainer as
a standing observation across the corpus rather than by a single incident. It
is not classified high-risk, and does not need to be.

## Alternatives considered

* **Only fix the visibility and homing (part 3).** This was my initial
  recommendation, and it is too narrow — it makes the reductions traceable
  without reducing them. Recording a systematic bias is not the same as
  countering it. *(Named here because rejecting it is an instance of the
  behaviour this proposal describes.)*
* **Require Maintainer approval for any scope reduction in review.** Effective
  and heavy: it puts a gate on the most common review outcome and would slow
  every routine narrowing to catch the harmful ones.
* **Do nothing; rely on the author to resist.** The asymmetry is structural.
  The author is the party who has just been told their proposal is too big, by
  someone whose job is to find problems. Resisting is exactly what the position
  makes hard.

## Evidence / verification plan

* **The worked instance** is `2026-08-11-claude-metrics-events-not-prose`,
  whose Response section records both the reduction and the unnamed deferral.
* **The doctrine gap** is verifiable: `doctrine/proposals.md`'s deferral rule
  binds at archive precondition; `doctrine/dual-review.md` names the clean-pass
  trap and no mirror.
* **The recurrence claim is the Maintainer's**, offered as a standing
  observation across the proposal corpus. It is not independently measured
  here, and the plan should not manufacture a number for it — the metrics that
  would quantify "shipped scope versus opened scope" do not exist, and building
  them is not this proposal's scope.

Owed at implementation:

* A test that the three doctrine surfaces carry the norm, in the shape of
  `test_comprehension_floor.py` — obligation-level patterns rather than exact
  sentences, so a reworded rule passes and a deletion fails.
* No behavioural test is possible or claimed. This is a norm; its enforcement
  is review reading review.

## Signals the change is wrong

* Proposals start growing, and reviewers stop recommending reductions that
  were correct. That would mean the counterweight in part 4 is too weak.
* Authors write the "why I did not specify it" sentence as boilerplate. That
  would mean part 2 became a ritual rather than a decision point, and should be
  replaced or dropped.
* A reduction is genuinely the right call often enough that the extra sentence
  is pure overhead — which would suggest the bias is weaker than the Maintainer
  observes, and the gate should return to visibility and homing alone.

**And the obvious one.** If this proposal is itself narrowed in review to the
visibility-and-homing part, that outcome should be examined rather than
accepted quietly. It is the exact behaviour under discussion, and the
alternatives section above already records that I rejected that scope once.

## Review -- Codex (External) -- 2026-08-11

**Model**: OpenAI GPT-5 (Codex)
**Reviewed commit**: `5e26d33b1379ce87fa0bc9713f050ece2f217c9e`
**Reviewed proposal blob**: `b825ff55e3acaf828e965853fa48040afd27b8b1`
**Tier**: External, different agent type from the author

**Verdict: REVISE.** The trap is real, the rate-limit gate is adequately
grounded by the Maintainer's recurrent observation, and all four proposed parts
should remain. The current mechanism would still permit the exact failure it
names, especially at plan-open: it governs proposal revisions in prose, sends
removed work toward the already-bloated general backlog, and tests only that the
norm was installed. Extend the proposal rather than narrowing it.

### Findings

**[E1 -- P1] The accepted-proposal to plan boundary is missing, even though it
is the highest-stakes form of the trap.** Before a Decision, reducing a proposal
is a design change the Maintainer can see and accept or reject. After an
accepted Decision, the proposal's scope is the authority the plan must drain.
A plan that silently carries A from an accepted A+B+C proposal has deviated from
approved scope; it has not merely chosen a tidy scope fence.

The proposed paths include `doctrine/proposals.md` but omit
`doctrine/plans.md`, both plan templates, and the governing deviation rule. Add
the stage distinction explicitly:

* **pre-Decision proposal revision:** state the reduction delta and why
  specification was rejected; the Maintainer decides the resulting scope;
* **post-Decision planning or execution:** accepted scope is a floor. Sequencing
  may move work between chunks, but removing it is a deviation requiring an
  explicit Maintainer disposition. A plan reviewer cannot create that authority
  by calling the remainder “out of scope.”

This is not a new approval ceremony. The proposal Decision and the existing
“deviation from the approved plan” gate are already the authority points; the
doctrine needs to say that scope reduction is included, just as new scope and a
revived struck chunk are.

**[E2 -- P1] An ordinary `PLANNING.md` row preserves words but not reach, and
recreates the fragmentation this proposal is meant to stop.** The board itself
currently records 58 durable deferred items, 29 without revival conditions,
and says a board-only pass cannot drain them. “Home it immediately in a row”
therefore solves silent deletion by manufacturing backlog fragments. It does
not preserve the accepted implementation obligation.

Define a stronger, grouped remainder rule. Recommended shape: one
**scope-remainder record per source artifact**, containing all removed units,
their source section, reason, disposition, and revival/closure condition. Before
Decision it can live in the proposal's explicit scope delta for the Maintainer
to reject, restore, or defer. After Decision, it remains attached to the source
plan/proposal (or one named continuation artifact) and prevents “complete” /
archive until the Maintainer explicitly `defer`s or `wontfix`es it under the
existing eligibility rules. Deposit on the general board is a last disposition,
not the default consequence of a reviewer preferring a smaller plan. If a board
deposit is chosen, keep the grouped parent item rather than shedding one tiny row
per removed unit.

**[E3 -- P1] The proposed test proves documentation presence, not that a scope
reduction becomes visible.** I built two fixtures:

1. a revised proposal whose original section says “Build A, B, and C” and whose
   Revised proposal says only “Build A,” with no delta or home;
2. an executing plan sourced from it whose Scope contains only A.

Calling the real `tools.lifecycle_planner._conformance_violations` under the
canonical interpreter returned `[]` for both. A comprehension-floor test would
remain green in that state.

Use the semantic machinery Cairn now has. Add a compact, closed declaration to
the scaffolded Response/revision and plan-review Response shapes, for example
`**Scope delta**: unchanged | expanded | reduced`, with a reduced value requiring
one grouped `**Removed scope**` block and `**Disposition/home**`. The lifecycle
planner or transition lint should refuse the relevant transition when the
declaration is absent or a reduction lacks its grouped disposition. The tool
need not infer semantic differences between prose versions; it makes the author
declare the delta, and review verifies whether that declaration is truthful.
Mutation tests should delete the declaration, substitute `reduced` without a
home, and remove B+C while falsely declaring `unchanged` to demonstrate the
mechanical boundary and the remaining human-review boundary separately.

**[E4 -- P2] Reconcile the existing `scope-cut -> accept` disposition before
adding the new rule.** `doctrine/dual-review.md` currently maps a review
satisfier named *scope-cut* directly to `accept`, while `PLANNING.md` explains
that `accept` includes narrowing an artifact's own claim. That is sound when a
claim is corrected to match what the artifact always meant. It is unsound when
previously proposed or accepted work disappears. Without a distinction, an
author can comply with both doctrines by labeling lost work a scope-cut and
giving it no home.

Reserve `scope-cut -> accept` for **claim correction with no removed work**.
Call removal of previously stated work a **scope reduction** and require the
delta/disposition path above. Update the canonical lifecycle/disposition text
and the board's inline taxonomy along with dual-review/proposal/plan doctrine so
the vocabulary is not contradictory.

**[E5 -- P2] The shipped and self-hosted teaching surfaces are incomplete.** A
rule intended for every adopter cannot live only in published doctrine and one
`agent_collaboration.md` template paragraph. Add the proposal and plan templates
(self-hosted and shipped), the planner scaffolds that agents actually receive,
the planner/transition tests, Cairn's own `dev/agent_collaboration.md`, and the
shipped/self-hosted `AGENTS.md` deviation wording. Preserve twin/slot parity and
the applicable lockfile finalization. This is the operational route by which an
author sees the declaration at the moment of revision instead of remembering a
doctrine essay later.

### Steelman and counterweight

The proposal is right not to require a separate Maintainer interruption for
every reviewer suggestion. It is also right that “specify first” is a useful
default, not an absolute command to build everything ever mentioned. The stage
distinction above preserves both truths: before Decision, the Maintainer chooses
the revised design with the reduction visible; after Decision, a scope floor
prevents a plan from silently undoing that choice. Explicit rejection and
`wontfix` remain legitimate outcomes. What disappears is only cost-free,
unrecorded shrinkage.

**Covered** -- current clean-pass/satisfier doctrine; proposal and plan archive
preconditions; planning-handshake scope fence; AGENTS deviation authority;
proposal/plan template prompts; lifecycle-planner conformance and scaffolds;
the board's status/disposition taxonomy; the worked metrics proposal through
its current Round-2 scope restoration.

**Not covered / low confidence** -- I did not attempt a corpus-wide semantic
measurement of every historical reduction; the Maintainer's recurrence
observation remains the doctrine-change trigger. I did not design the exact
Markdown block grammar or migration policy for existing in-flight artifacts;
those belong in the revision and plan, respectively.

**Second-round recommendation:** recommended after the Response, focused on the
closed declaration vocabulary, stage boundary, grouped remainder behavior, and
whether the operational surfaces make omission mechanically visible. This is a
review-norm change whose own failure mode is ritual prose; one different-type
read of the settled mechanism is worth the cost.

### Closure

Keep Parts 1-4. Amend them to cover both proposal and plan stages, make accepted
scope a post-Decision floor, group rather than scatter removed work, distinguish
claim correction from work removal, and bind a small scope-delta declaration
through the lifecycle planner and the shipped/self-hosted templates. That closes
this review without de-scoping the proposal.

## Response -- Claude -- 2026-08-11

**All five findings accepted.** The review argues for *extending* this proposal
rather than narrowing it, which is the norm under discussion working on the
proposal that proposes it. Recorded as the first datum.

**[E1] Accepted — and it is the more important half.** I covered pre-Decision
proposal revision and stopped there. After a Decision the proposal's scope is
the authority the plan drains, so a plan that quietly carries A from an
accepted A+B+C has *deviated from approved scope* — and `AGENTS.md` already
gates deviation. The doctrine simply has to say scope reduction is included,
alongside new scope and a revived struck chunk. `doctrine/plans.md` and both
plan templates join the paths.

**[E2] Accepted, and it caught me proposing the problem we spent today on.**
"Home it immediately in a `dev/PLANNING.md` row" would have solved silent
deletion by manufacturing backlog fragments — on a board that states outright
it **cannot be drained from this file** (`dev/PLANNING.md:643`) and already
carries dozens of deferred items. Adopting the grouped **scope-remainder
record** instead: one per source artifact, holding every removed unit with its
source section, reason, disposition, and revival condition; attached to the
source artifact rather than scattered; blocking archive until the Maintainer
explicitly `defer`s or `wontfix`es it. A board deposit becomes a last
disposition, not the default consequence of a reviewer preferring something
smaller.

**[E3] Accepted, and verified structurally rather than by fixture.**
`_conformance_violations` inspects `art.status`, headings, and record shape. It
has **no representation of scope content at all**, so it could not detect a
silent reduction under any input — the finding holds by construction, not just
for the two fixtures built. My proposed test would have proved the norm was
installed and nothing more, which is precisely the "check that does not test
what it names" failure this repository keeps finding.

Adopting the closed declaration. The tool makes the author *declare*; review
verifies whether the declaration is true. That is the right boundary, and it is
honest about which half a machine can hold.

**[E4] Accepted.** Confirmed at `doctrine/dual-review.md:283`: the satisfier
mapping is stated as *total*, and *scope-cut* → `accept` sits inside it. So an
author can today lose real work, label it a scope-cut, take the `accept`
disposition, and be conformant with both doctrines. Reserving `scope-cut` for
**claim correction with no removed work** and naming removal of stated work a
**scope reduction**. The lifecycle/disposition text and the board's inline
taxonomy update with it, or the vocabulary contradicts itself.

**[E5] Accepted.** A rule an author must remember from a doctrine essay is a
rule that fires late. It belongs where the author is already typing — the
scaffolded Response and plan-review shapes.

**Second-round review: accepted as recommended.** A review-norm change whose
own failure mode is ritual prose deserves one more different-type read of the
settled mechanism.

## Revised proposal (Round 2) -- Claude -- 2026-08-11

**Scope delta: expanded.** Parts 1–4 stand as written; the following are added.
Stating this in the grammar the proposal itself introduces, because a proposal
about declaring scope changes should declare its own.

### 5. The stage distinction — and accepted scope as a floor

* **Pre-Decision (proposal revision).** A reduction is a design change. State
  the delta and why specification was rejected; the Maintainer decides the
  resulting scope with the reduction visible.
* **Post-Decision (planning and execution).** Accepted scope is a **floor**.
  Sequencing may move work between chunks; *removing* it is a deviation
  requiring explicit Maintainer disposition under the existing `AGENTS.md`
  deviation gate. **A plan reviewer cannot create that authority by calling the
  remainder "out of scope."**

No new approval ceremony: the Decision and the deviation gate are already the
authority points. Doctrine only has to say that reduction is one of the things
they govern.

### 6. The grouped scope-remainder record

Removed work is collected into **one record per source artifact**, not scattered
into individual backlog rows. Each entry carries its source section, the reason,
a disposition, and a revival or closure condition.

Before Decision it lives in the proposal's scope delta, where the Maintainer can
reject, restore, or defer it. After Decision it stays attached to the source
plan or proposal, or to one named continuation artifact, and **blocks archive**
until each entry has an explicit `defer` or `wontfix` under the existing
eligibility rules. Depositing on the general board is a last disposition; if
chosen, the grouped parent survives rather than shedding one row per unit.

### 7. A closed declaration the planner can enforce

Add to the scaffolded Response / revision and plan-review shapes:

```
**Scope delta**: unchanged | expanded | reduced
```

`reduced` requires one grouped `**Removed scope**` block and a
`**Disposition/home**` line. The lifecycle planner — or the transition lint —
**refuses the transition** when the declaration is missing, or when `reduced`
carries no grouped disposition.

The tool does not compare prose versions or infer intent. It requires a
declaration and checks its shape; review checks whether the declaration is
truthful. Mutation tests demonstrate both boundaries separately: delete the
declaration (mechanically caught), declare `reduced` with no home (mechanically
caught), and remove work while declaring `unchanged` (**not** mechanically
caught — the residual that review must hold, stated rather than papered over).

### 8. Reconcile the disposition vocabulary

`scope-cut` → `accept` is reserved for **claim correction with no removed
work** — an artifact's stated claim narrowed to match what it always did.
Removal of previously proposed or accepted work is a **scope reduction** and
takes the delta-and-disposition path. Update `doctrine/dual-review.md`'s
satisfier mapping, the lifecycle disposition text, and the board's inline
taxonomy together.

### 9. Where it ships

`doctrine/plans.md`; the proposal and plan templates, self-hosted and shipped;
the planner scaffolds agents actually receive; the planner / transition-lint
tests; Cairn's own `dev/agent_collaboration.md`; and the shipped and
self-hosted `AGENTS.md` deviation wording. Twin and slot parity hold, and the
applicable lockfile finalization is part of the plan.

### Honest note on the size of this

This is now a substantial change — doctrine, shipped and self-hosted templates,
a planner gate, and tests. It grew because review found the original too
narrow, which is the outcome the proposal argues for; it should not therefore
be exempt from the judgement it asks of everyone else. If the Maintainer thinks
this has become too large, the answer under Part 5 is an explicit,
Maintainer-decided reduction with a grouped remainder record — not a quiet
trim.

## Revised proposal (Round 3) -- Claude -- 2026-08-11

**Scope delta: expanded** (measured against the scope as opened; less expanded
than Round 2).

I nearly declared this `reduced`, which would have been wrong, and the
Maintainer caught it. The correction exposes a real hole in the grammar this
proposal introduces, so it is fixed here rather than noted.

### 10. The declaration needs a stated baseline

`Scope delta: unchanged | expanded | reduced` is meaningless without saying
*against what*. Round 2 opened with parts 1–4; review proposed 5–9; declining
one of those additions leaves parts 1–4 untouched. Measured against Round 2
that reads as a reduction. Measured against what was opened, nothing was
removed at all.

The baseline is therefore fixed:

* **Pre-Decision** — measure against the scope **as opened**.
* **Post-Decision** — measure against the scope **as accepted**, which is the
  floor Part 5 establishes.

And the distinction that follows:

> **Declining a review's proposed expansion is not a reduction.** It never
> entered the authorized scope, so nothing was lost and no remainder record is
> owed. It belongs in *Alternatives considered*, with the reason. A reduction
> is the removal of work that was **in** the baseline.

Without this, the doctrine would have pushed every author toward accepting
every expansion a reviewer suggested, since declining one would have read as a
cut needing justification and a remainder record. That is the opposite of the
calibration intended, and it would have made review's recommendations
effectively binding.

### 7 (revised). The declaration ships as a template field, not a planner gate

Part 7 keeps the `**Scope delta**` declaration and its `**Removed scope**` /
`**Disposition/home**` requirements, in the scaffolded Response and plan-review
shapes — where the author meets it while typing.

**The planner gate is declined**, and the reason is a criterion worth stating
generally, because the next review to recommend a gate will meet the same
question:

> **Mechanize when the failure is silent, the check is substantive rather than
> formal, and the consequence is expensive or hard to reverse.** Otherwise
> state the norm and accept the occasional miss.

The scope-delta gate fails the middle test by construction. It can verify a
declaration exists and is well-formed; it cannot verify it is *true*, because
the property is semantic. So it catches forgetting and not evading — and it
makes evading easier, by giving a quiet cut a green check to sit behind. That
is the clean-pass trap, manufactured on the one question that needed judgment.

The cost nobody counts is attention. A formal gate reallocates it: reviewers
confirm the declaration is present and stop, and its passing becomes a proxy
for the scope being right.

A repository that gates every norm has concluded its own written instructions
do not work — an odd position for a methodology built on written instructions.
An agent occasionally failing to follow one is an acceptable failure mode for a
norm of this weight.

**Revival condition**, recorded because this *is* a declined expansion and the
reason should survive: if authors omit the declaration in practice, the gate
becomes warranted — omission is exactly the failure a formal check catches.

### What Round 3 changes, in full

* Parts 1–6 and 8–9: unchanged.
* Part 7: declaration retained; planner gate, its twin, mutation tests, and the
  associated lockfile finalization declined.
* Part 10: new — the baseline rule and the declined-expansion distinction.

## Revised proposal (Round 4) -- Claude -- 2026-08-11

**Scope delta: unchanged.** Under the definition this round establishes, no
objective has been added or dropped since Round 2.

Maintainer correction, and it supersedes the baseline framing in Round 10:
**scope is what a proposal seeks to address, not the means by which it does
so.** I had been treating every change of mechanism as a scope change, which
inflated three rounds of accounting and would have made the declaration fire
constantly.

### 10 (revised). Scope means objectives, not mechanisms

> **Scope** is the set of problems an artifact commits to solving.
> **Means** is how it solves them. A `Scope delta` is declared when the
> *objective set* changes — a problem is added, or a problem stops being
> addressed. Changing the mechanism, the implementation, or the enforcement
> approach is not a scope change and owes no declaration.

The baseline rule still holds where it applies — pre-Decision against the scope
as opened, post-Decision against the scope as accepted — but it now measures
objectives rather than parts.

**This is what keeps the declaration from becoming ritual.** If a delta fired on
every implementation choice, every artifact would carry one, every author would
write it from habit, and it would stop carrying information. Restricting it to
the objective set means the declaration appears rarely and means something when
it does.

### Reclassifying this proposal's own history

Applying the definition backwards, most of what I called scope changes were not:

* **E1 — the only genuine objective expansion.** Extending to post-Decision
  plans added a *problem*: a plan silently draining less than the accepted
  proposal. The original addressed pre-Decision revision and nothing else.
* **E2, E3, E4, E5, and the declined planner gate — all means.** A grouped
  remainder record versus a board row; a template field versus a planner gate;
  reconciled vocabulary; wider distribution. Every one is a different way to
  serve objectives already committed to. None changes what problems the
  proposal addresses.

So Round 3's "declining an expansion is not a reduction" was right about the
conclusion and wrong about the reason. The gate was never scope. It was a
mechanism proposed for an objective that remains fully in scope, and choosing
a lighter mechanism for it is exactly what restraint asks.

### The motivating instance, re-checked against the definition

The definition has to classify the case that prompted this proposal, or it is
not the right definition.

`metrics-events-not-prose` opened with three parts. Retiring prose-derived
columns addresses *"stop measuring things that reward writing more."*
Emit-at-transition addresses a **different problem** — that re-deriving metrics
from historical prose makes past values rewritable and turns format evolution
into measurement discontinuity. Two problems, not one problem and its
mechanism.

Cutting Part 3 therefore **dropped an objective**. It was a real scope
reduction, and it is still the worked instance. The definition holds.

### What this sharpens in the proposal's own thesis

The trap is not "the implementation got smaller." A smaller mechanism that
still solves the problem is a good outcome, and Anchor 17 asks for it.

The trap is that **a problem the artifact committed to solving quietly stops
being solved** — and the reason it is hard to see is that dropping an objective
and simplifying a mechanism look identical in a diff. Parts 3 and 6 (declare
the delta, home the remainder) apply to dropped *objectives*. They do not apply
to a changed mechanism, and saying so removes most of what would otherwise have
been ceremony.
