# The scope-reduction trap

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-11
**Status**: proposed
**Touches**: `doctrine/dual-review.md`; `doctrine/proposals.md`;
`templates/core/dev/agent_collaboration.md`
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
