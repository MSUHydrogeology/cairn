# Doctrine-sync draft — Chunk 2

**Scope.** Cairn-native abstractions for the three doctrine
surfaces Chunks 6, 7, and 8 will apply:

* Chunk 6 — `doctrine/dual-review.md` (the Decision-support
  Round-2 review pattern).
* Chunk 7 — `doctrine/lifecycle.md` (procedural-gap inline
  Decision; deferred-follow-up revival; the no-history
  posture for the roadmap surface).
* Chunk 8 — `doctrine/roles.md` and a new
  `templates/modules/<tier>/model-selection.md` (capability
  floor by role and risk).

**Module classification decision** (this draft, per Codex F2):
the model-selection module is **dimension-gated**, on the
complexity axis. Reasoning in §3 below; sub-decision (which
adopter signals trigger installation) deferred to Chunk 8.

**Discipline.** Cairn-native abstractions only — no adopter-
specific filenames, tier labels, or model names. Specific
adopter realizations live in `case-studies/modflow_tools.md`
(Chunk 10).

---

## 1. The **Decision-support Round-2 review** pattern (for Chunk 6)

### Failure mode

Cairn's lifecycle has a clean append-only shape:

```
proposed --> reviewed --> revised --> accepted / rejected / superseded
```

The Review and Response sections alternate; each round of
review can produce a revised proposal, and the cycle repeats
until the maintainer Decides.

This shape has a subtle structural gap: once the author has
Responded and produced a revised proposal, the proposal is
ready for Decision. But what if a *second* reviewer reads
the revised proposal and surfaces independent findings —
not findings the first reviewer missed, but findings that
the revision itself introduced or that a different
reviewer's blind-spot profile exposes?

Two failure modes follow from the unmodified lifecycle:

1. **The second reviewer's findings get treated as Round-1
   findings** — i.e., they trigger another revision cycle.
   The author writes another Response, possibly revises
   again, and the cycle starts again. With each round, the
   author's Response and the proposal diverge further from
   any one reviewer's read. The cycle no longer closes.

2. **The second reviewer's findings get dropped** — the
   author refuses to re-open the cycle, the findings live
   in a Review section that the author never responds to,
   and the Decision is taken in tension with that unanswered
   critique. The append-only record now contains a critique
   that the lifecycle did not metabolize.

Both failures share a root cause: the lifecycle as drawn
treats every Review section as an instance of the same
pattern (Review → Response → revision). It does not name
the case where a Review section *should not* feed
revision, but instead feed the Maintainer's Decision
directly.

### Invariant

> A Review section appended **after** the author's Response
> and Revised proposal — once the proposal is at status
> `revised` and substantively ready for Decision — is a
> **Decision-support Round-2 review**, not a Round-1
> review. It has three structural properties that
> distinguish it from a Round-1 review:
>
> 1. **The proposal's status stays `revised`.** The new
>    Review does not move status to `reviewed`.
> 2. **The Review is append-only against the proposal,
>    not against the cycle.** The author does not write
>    a Response section to it; the cycle has already
>    closed on the author's side.
> 3. **The Review feeds the Maintainer's Decision,
>    not another revision.** The Decision section, when
>    written, addresses both Round-1 and Round-2 findings
>    in one place.

### Why "Decision-support" is the load-bearing word

The first reviewer's job is to test the idea so the author
can revise it. The second-reviewer-after-Response is doing
something different: providing independent perspective to
the Maintainer, who is the only actor with authority to
weigh competing reviews and Decide. Naming the role
("Decision-support") makes the structural difference
visible; without the name, the second reviewer is mis-
modeled as "another Round-1 reviewer" and the lifecycle
breaks.

### When this pattern fires

Trigger conditions (illustrative, not exhaustive):

* A revised proposal produces a substantive change that
  the original reviewer didn't see; a fresh reviewer reads
  the revision and finds new failure modes.
* The original review was Internal-tier and an External
  reviewer subsequently reads the revised proposal — the
  External-tier read is by construction structurally
  independent of the Round-1 read, and its findings should
  not be conflated with Round-1 findings.
* The Maintainer asks for a second opinion before Deciding;
  the second reviewer is operating in support of that
  Decision, not in support of another author revision.

Cairn doctrine names the pattern; the adopter recognizes
the trigger.

### What the pattern does NOT permit

The pattern is bounded — it is not "the lifecycle allows
unlimited review rounds":

* It does not permit the author to skip Responding to a
  Round-1 review by labeling it Round-2. Round-1
  reviews remain author-Response-bound until the proposal
  reaches status `revised`.
* It does not permit a Decision-support reviewer to demand
  another revision; if a Decision-support reviewer
  believes the revision is fundamentally wrong, the
  proper response is to recommend the Maintainer reject
  or supersede, not to require the author to revise
  again.
* It does not permit unbounded Round-2 reviews after a
  Round-2 review. The Maintainer's Decision closes the
  Decision-support phase; any further critique becomes a
  new proposal that amends or supersedes.

### Relationship to External review

This pattern lives entirely inside `dual-review.md` — it
extends the existing two-tier review framework with one
more shape (the Decision-support reviewer) rather than
adding a new tier. Internal / External / Code / Domain-
rotation review floors still apply.

---

## 2. The **procedural-gap inline Decision** pattern (for Chunk 7)

### Failure mode

A non-trivial accepted proposal carries an executing plan.
Implementation discovers — mid-flight — that a specific
procedural step was not pre-specified by the proposal or
plan. Two examples of the failure shape:

* The plan says "Chunk N retrofits package X to use the
  new abstraction"; mid-Chunk-N the implementer finds
  that package X has a second sub-package whose retrofit
  was not enumerated in the plan but is unavoidable to
  complete the Chunk N work.
* The proposal says "the new doctrine module is dimension-
  gated"; the bootstrap-test implementer finds the
  dimension-rubric scoring function has no entry for one
  of the existing dimensions, which neither the proposal
  nor the plan anticipated.

In both cases, the "correct" response under the
unmodified lifecycle is to open a new proposal. But that
is over-process: the gap is a procedural detail, not a
substantive scope question. Opening a proposal for it
multiplies cycles unnecessarily, and the implementing
agent's executable surface stalls while the deliberation
runs.

The under-process failure is symmetric: the implementer
quietly makes the procedural call themselves, which both
exceeds their delegated authority and dilutes the
Decision-of-record principle (decisions are Maintainer's
to take, recorded in artifacts).

### Invariant

> The Maintainer may close a procedural gap discovered
> during implementation via a **procedural-gap inline
> Decision** — a brief Decision section appended to the
> live proposal or plan, recording the procedural call
> and the reasoning — **only when all three of the
> following hold**:
>
> 1. **Bounded mechanical gap.** The gap is a specific
>    procedural detail (a missing enumeration, an
>    unanticipated sub-step, a clarification on how a
>    pre-specified rule applies to a specific case) —
>    not a substantive scope hole or a competing-trade-off
>    that requires deliberation.
> 2. **Resolution preserves substantive scope.** The
>    inline Decision does not re-open the proposal's
>    substance; it answers a "how" question, not a
>    "whether" question. Anyone reading the inline
>    Decision should be able to read it as "filling in"
>    the original Decision, not "amending" it.
> 3. **Closure preserves the implementing agent's
>    executable surface.** After the Decision lands,
>    the implementer can continue executing — the gap is
>    closed in the sense that the implementer's next
>    step is now defined. The Decision does not introduce
>    new prerequisites that themselves require
>    deliberation.

### Why the three-criterion gate matters

Without all three criteria, the inline-Decision pattern
becomes a back door for re-scoping under the cover of
"procedural." The criteria are not soft hints — they are
the structural floor. If a gap fails any one of them, the
right response is *not* an inline Decision but a fresh
proposal that amends or supersedes the original.

The criteria are co-load-bearing:

* Without (1), an inline Decision could absorb a
  substantive scope addition, and the proposal review
  cycle gets bypassed.
* Without (2), the inline Decision could quietly change
  the original Decision's substance, and the append-only
  record becomes misleading (the Decision-of-record now
  says something the reviewers never saw).
* Without (3), the inline Decision could *introduce*
  scope rather than close it, leaving the implementer
  in the same gap with new prerequisites layered on.

### Form

Inline Decisions are short — typically a paragraph naming
the gap, the call, and the reasoning — and attach to the
live artifact at the natural place (a "Decision
clarification" subsection, dated, attributed to the
Maintainer). They are not separate proposal files; they
are append-only additions to the executing artifact.

### Companion patterns

Two related lifecycle patterns warrant their own
abstractions in this section:

#### 2a. **Deferred-follow-up revival**

A proposal accepted at one point can carry an "explicitly
deferred" item — a sub-question or sub-scope deferred to
a later proposal. When the time comes to revive that
deferred follow-up, the revival is itself proposal-worthy
under the standard trigger conditions (substantive scope,
public contract changes, cross-cutting refactor, etc.).
The doctrine point: **deferred-follow-ups do not become
implementable just because they are revisited; they
re-enter the proposal lifecycle**.

This rule prevents the pattern where a deferred follow-up
accumulates implementation detail in side conversations
and lands without ever returning to the deliberation
surface.

#### 2b. **The roadmap surface is no-history**

The roadmap surface (the project's tracked "what is
planned / in flight / completed" file) is **a current-
state index, not a historical log**. Completed work
migrates out of the roadmap and into the durable record —
the archived proposals, the archived plans, the
changelog. The roadmap holds only what is open or in
flight; "completed" entries are removed, not crossed off.

The failure mode this addresses: a roadmap that
accumulates "completed" entries becomes the primary
where-did-this-happen surface, when in fact the archived
artifacts (proposals, plans, commits, changelog) are
where the truth lives. The no-history posture forces the
durable record to *be* the durable record, rather than
being shadowed by an incomplete summary in the roadmap.

### Relationship to chat-vs-Decision

A related anti-pattern, worth flagging in `lifecycle.md`:
deliberation that happens in conversation and never reaches
an artifact does not happen. Inline Decisions are the
right response to a real procedural gap precisely because
they convert what would otherwise be a chat resolution
into a durable Decision-of-record. The pattern is
strictly stronger than "the Maintainer answered in chat";
it requires the answer to land on the artifact.

---

## 3. **Capability floor by role and risk** (for Chunk 8)

### Failure mode

Multi-model agent teams face a structural question every
session: which model fills which role? The unmodified
roster (`roles.md`) lists role frames — Strategy /
Research, Implementation, Internal Reviewer, External
Reviewer, User Agent, Security Review — without
prescribing a capability floor per role.

That under-specification produces two failures:

1. **Capability over-spend.** A high-capability model
   fills every role, including roles where lower-
   capability models would suffice. Cost is wasted; more
   importantly, the high-capability model develops a
   monopoly on context that erodes the structural-
   independence floor when it later fills a Review role.

2. **Capability under-spend.** A lower-capability model
   fills a role where the capability gap produces
   structural failures — e.g., an under-capable External
   Reviewer misses the very findings that justify the
   External tier. The reviewer-floor is met nominally
   ("a different agent type") but the floor's purpose
   ("independent reasoning genuinely does not share the
   author's blind spots") is violated.

### Invariant

> Each role has a **capability floor**: the minimum
> capability required to fill the role responsibly given
> the project's risk profile. The floor is named in
> doctrine using **adopter-local capability tier labels**
> (e.g., "high-capability tier", "medium-capability tier",
> "low-capability tier"); the adopter maps those tiers
> to its specific model lineup in its own configuration.
>
> Specifically:
>
> * **High-stakes roles** — Strategy / Research, External
>   Review, Security Review, Maintainer scribing —
>   require the **high-capability tier** by default,
>   absent an explicit Maintainer-Decision lowering the
>   floor for a specific session or sub-domain.
> * **Standard-stakes roles** — Implementation for
>   non-trivial work, Internal Review, Code Review —
>   accept the **medium-capability tier**; high-tier is
>   permitted when available.
> * **Low-stakes roles** — Implementation of trivial
>   chunks, User Agent for routine workflow exercise,
>   non-substantive doc tweaks — accept the **lower-
>   capability tier**; higher tiers are not required.

### Why "by role and risk" is the load-bearing phrasing

The floor is jointly determined by role *and* risk. A
role does not have a single floor across projects: an
Implementation role on a greenfield experimental codebase
has a lower capability floor than the same role on a
high-stakes scientific codebase under regulatory review.
Cairn's doctrine names the *invariant* (a capability
floor exists, by role and risk); the adopter's project-
specific complexity placement (via the complexity axis)
determines the actual numerical mapping.

### What the doctrine names vs. what stays adopter-local

Doctrine names:

* The capability-floor invariant.
* The three tier labels (high / medium / low capability).
* The high-stakes-role default-to-high-tier rule.
* The adopter-local tier-to-model mapping requirement
  (i.e., adopters must publish their own mapping
  somewhere — typically in their `case-studies/<adopter>.md`
  or an adopter-local config file).

Doctrine does NOT name:

* Specific model names.
* Specific model versions.
* Specific vendor / API choices.
* Specific tier-to-cost ratios.
* Specific "risk" thresholds in numerical terms.

Those are all adopter-local. Cairn updates its doctrine
on the *shape* of the floor; adopters update their
mapping as models evolve.

### Companion pattern: **diversity within tier**

Where multiple models meet a tier's floor, structural-
independence is stronger when the Reviewer is a different
*model architecture* than the author at the same tier —
e.g., if the author is on one vendor's high-capability
tier, the External Reviewer is on a different vendor's
high-capability tier (rather than another instance of the
author's model). This is a *strengthening* of the floor,
not a replacement; the floor is necessary, model-
architecture diversity is the additional independence
gradient.

### What goes in the role doctrine vs. the module

The capability-floor invariant lives in `doctrine/roles.md`
— it is part of how roles work. The mechanism that
operationalizes the floor (a tier rubric, a per-role
default mapping template, a worked example) lives in a
new `templates/modules/<tier>/model-selection.md`. The
doctrine names the invariant; the module instruments it.

---

## 4. Module-classification decision for `model-selection.md`

Per Codex F2, the model-selection module is **not** default-on
— it is gated. The remaining question (named in the source
plan, deferred from Chunk 2) is: **team-gated or
dimension-gated?**

### Recommendation: **dimension-gated**, on the complexity axis

The capability-floor question is fundamentally about
**stakes** — about how badly a structural-independence
failure or a capability under-spend hurts the project.
Stakes is what Cairn's complexity axis already measures:

> *Complexity (`complexity.md`)*: simple ↔ complex —
> Review weight and verification depth — how often
> External review is mandatory, whether a scientific-
> trust review lens is in the roster.

The complexity axis already drives Review-weight; adding
"per-role capability floor" to the same axis is a clean
extension of an existing gradient. A greenfield
experimental project sits at low complexity and does not
need the per-role capability discipline; a high-stakes
scientific codebase sits at high complexity and does.

### Why not team-gated

Team-shape (the `agent-team.md` axis) drives the *roster*
— which roles exist, who fills them — but it does not
drive the capability floor for any given role. A solo-
agent team filling the External Review role still needs
to know that role has a capability floor; the floor is
about the role's purpose, not about how many agents the
team has.

Team-gating would mis-place the module: a multi-agent team
of all-low-capability models would receive the module
(because they are "concurrent agents"), but the floor
question — "do any of these meet the External Review
capability floor?" — is exactly what the team needs to
ask. Team-gating tells them the question is relevant;
it does not name the floor. Dimension-gating on
complexity does both.

### Edge case: low-complexity multi-agent teams

A low-complexity adoption with multiple agents does not
install the model-selection module by default. They run
the standard role doctrine; capability-floor questions
do not bite them because the stakes are low. If their
complexity placement moves up later, the bootstrap
re-evaluates and installs the module then. This is the
standard Cairn dimension-gated pattern.

### What Chunk 8 still decides

Chunk 8 picks the **trigger threshold** on the complexity
axis — at what complexity-score does the bootstrap
install the module? — and the **module's installation
location** (`templates/modules/dimension-gated/
model-selection.md` if Cairn has a `dimension-gated/`
subdirectory, or another path if not). The sub-decision
is bounded; the dimension-gated classification is
settled here.

---

## Cross-cutting notes

### What stays in this draft vs. what stays in the case study

Same as Chunk 1: abstraction-only here, adopter-specific
realizations in `case-studies/modflow_tools.md`. Model
names, tier-to-model mappings, specific roadmap-surface
filenames, specific procedural-gap incidents, specific
Decision-support-Round-2 instances — all case-study
territory.

### Discipline check (Codex F5)

Same self-test as Chunk 1: if a draft sentence references
a specific model name, file name, tier number, plan stem,
or adopter-specific procedure, that sentence belongs in
the case study, not in core doctrine. A useful additional
check for Chunk 2's surfaces: if a sentence names a
"specific incident" rather than a "structural pattern,"
move it out — Cairn doctrine names patterns; the case
study names incidents.

### External Review checkpoint after Chunks 1 + 2 land

Per Codex F6, this draft and the Chunk 1 draft both land
before Chunks 3-8 apply them. An External Reviewer reads
both drafts side-by-side and tests the structural-
independence floor against the Cairn-native abstraction
discipline. Their findings (if any) revise the drafts
before chunks 3-8 consume them; if both drafts pass, the
implementing chunks proceed.

### What this draft does NOT cover

* The coordination-side abstractions — those are
  Chunk 1's draft.
* The session-routines-side abstractions (next-session
  handoff document, prune-intents goodnight step) —
  those are Chunk 1's draft (the prune-intents step
  lives in the coordination-tiers module per Codex F2).
* The case-study evidence ledger — that is Chunk 10.
* The Cairn `CHANGELOG.md` + version-bump wording —
  that is Chunk 10.
