# The lifecycle

Cairn's central claim is that a change to scientific software
should leave a **durable, reviewable record of the reasoning
behind it** — not just the diff. The lifecycle is the mechanism:
every substantive change moves through a sequence of states, each
state transition is its own commit, and the deliberation is
append-only, so the record cannot be quietly rewritten after the
fact.

Two artifacts carry a change: a **proposal** (the deliberation —
what to do, and why) and, for non-trivial work, a **plan** (the
execution — how it was carried out, and that it was verified).
They have separate lifecycles.

## Why a recorded lifecycle

A scientific result is trusted because its derivation is open to
inspection. Scientific *software* deserves the same discipline: a
reviewer, a future maintainer, or a future agent should be able to
ask "why is it this way?" and find an answer that was not
reconstructed from memory. Three properties make the record
trustworthy:

* **Append-only.** A proposal is never edited to change what it
  said; a revising section is appended. The record preserves what
  was believed *at each point*, not a tidied final state.
* **One commit per transition.** Open, review, response, and
  decision each land as their own commit. Bundling hides who
  changed what, and when.
* **Commit-mediated.** The record lives in version control beside
  the code. It survives context loss and contributor handoff, and
  it is timestamped by the same history as the change it explains.

## The lifecycle as a Registered Report

Scientific publishing has a format for exactly this discipline —
the **Registered Report**, in which a study's design and analysis
plan are peer-reviewed and accepted *before* any data is collected
(Stage 1), and the results are later reviewed against that
pre-registered plan (Stage 2).

Cairn's lifecycle is the same shape. The **proposal** pre-registers
a change's design and its evidence / verification plan, and is
reviewed *before* any code is written — Stage 1. The **plan** and
its code review then check the implementation, and the evidence it
produced, against that locked plan — Stage 2.

What this buys is a defense against *metric p-hacking*. When the
verification plan is committed before the implementation exists,
the evidence is judged against a prior commitment — not chosen
after the fact to flatter whatever the code happened to do. An
agent (or a human) cannot quietly move the goalposts, because the
goalposts sit in an append-only commit that predates the work.

## The proposal lifecycle

A proposal is the deliberation artifact for a substantive change —
a new abstraction, a cross-cutting refactor, a contract change,
anything worth a second opinion before it is baked in.

```
proposed --> reviewed --> revised --> accepted
                                  --> rejected
                                  --> superseded
```

* **proposed** — the author opens the proposal: the context, the
  change, the alternatives considered, an evidence / verification
  plan, and the signals that would show the change is wrong.
* **reviewed** — a reviewer appends a Review section (see
  `dual-review.md`).
* **revised** — the author appends a Response and, where needed, a
  revised proposal. Review and revision may repeat.
* **accepted / rejected / superseded** — the Human Maintainer
  appends the Decision. Acceptance is a *decision*, not an
  instruction to a particular contributor; implementation follows
  as separate, tracked work.

A proposal file is **append-only**: never edit a prior section —
append a revising one. An accepted proposal is changed only by a
new proposal that amends or supersedes it; that keeps the
amendment itself open to review, which is the whole point of the
system.

### Trivial vs. non-trivial

Not every change needs the full apparatus. A **trivial** change —
a single commit, a single area, no deferred follow-ups — is
implemented and has its proposal archived in one commit. A
**non-trivial** change — landing across multiple commits, touching
multiple areas, carrying multi-stage sequencing, or leaving
deferred follow-ups — opens a plan.

## The plan lifecycle

A plan is the execution artifact for a non-trivial accepted
proposal. Where the proposal records *what and why*, the plan
records *how the work was carried out, and that it was verified*.

```
open --> executing --> review --> archived
```

* **open** — the plan-open commit creates the plan and archives
  the source proposal: the deliberation is closed and carried into
  an actionable execution artifact.
* **executing** — implementation commits land.
* **review** — a code-review pass examines the implementation.
* **archived** — after review, lasting truth migrates to durable
  homes (topic docs, the changelog, the roadmap) and the plan is
  archived.

Unlike a proposal, a plan is an execution artifact: status,
progress markers, and commit hashes are updated in place as work
proceeds. But review findings and archive decisions are
**append-only**, mirroring the proposal's contract.

### The plan-archive precondition

**A plan never archives until a code review has occurred.** This
is the bright line that makes review work end-to-end on the
implementation side, parallel to the proposal review that makes it
work on the deliberation side. Without it, a fast implementation
closes its own loop before any independent eye sees the code. The
plan-archive commit is therefore always **distinct** from the
implementing commits — it is the artifact of "review happened, and
the loop is closed."

### Fast multi-stage

When the implementation itself fits in one commit but the work
still touches multiple areas or carries follow-ups, the plan-open
and first-implementation commits may **combine**. The plan-archive
commit still stands alone, after review. The lifecycle compresses;
it does not collapse.

## Procedural-gap inline Decisions

Implementation discovers, mid-flight, that a specific procedural
step was not pre-specified by the proposal or plan — a missing
enumeration, an unanticipated sub-step, a clarification on how a
pre-specified rule applies to a specific case. The unmodified
lifecycle would route this through a new proposal cycle, which is
over-process for a procedural detail; the under-process failure is
symmetric — the implementer quietly makes the call, exceeding
delegated authority and diluting the Decision-of-record principle.

The Maintainer may close such a gap via a **procedural-gap inline
Decision** — a brief Decision section appended to the live
proposal or plan, recording the call and its reasoning — **only
when all three of these criteria hold**:

1. **Bounded mechanical gap.** The gap is a specific procedural
   detail, not a substantive scope hole or a competing-trade-off
   that requires deliberation.
2. **Resolution preserves substantive scope.** The inline Decision
   does not re-open the proposal's substance; it answers a "how"
   question, not a "whether" question. Read alongside the
   original Decision it *fills in*, not *amends*.
3. **Closure preserves the implementing agent's executable
   surface.** After the Decision lands, the implementer can
   continue executing — the gap is closed in the sense that the
   next step is now defined. The Decision does not introduce
   new prerequisites that themselves require deliberation.

The three criteria are co-load-bearing. Without (1) an inline
Decision could absorb substantive scope under the cover of
"procedural" and bypass review. Without (2) it could quietly
change the original Decision's substance, leaving the
append-only record misleading. Without (3) it could *introduce*
scope rather than close it, layering new prerequisites on top
of the gap. If a gap fails any criterion, the right response is
not an inline Decision but a fresh proposal that amends or
supersedes.

Inline Decisions are short — a paragraph naming the gap, the
call, and the reasoning — attached to the live artifact at the
natural place (a "Decision clarification" subsection, dated,
attributed to the Maintainer). They are not separate proposal
files; they are append-only additions to the executing
artifact. The pattern is the structural alternative to
deliberation-by-conversation: it converts what would otherwise be
a chat resolution into a durable Decision-of-record on the
artifact.

## Chat preferences are not a lifecycle Decision

Maintainer chat-mode preferences during a working session ("maybe X",
"I lean toward Y", "what if we tried Z") are **input** — useful for
shaping a proposal's draft — not **Decisions** on proposal-worthy
changes. A lifecycle Decision attaches to a *written* proposal another
agent has reviewed (see "The proposal lifecycle"). When an agent
receives chat preferences on a proposal-worthy change, the right move
is to fold them into a proposal draft — cited as **"maintainer
preference during drafting"** in *Rationale* or *Alternatives
considered*, not as the Decision — open it for review, and *then* wait
for the Maintainer's Decision.

**Bounded mechanical directives** are different: "revert this commit",
"fix this typo", "scribe the Decision on proposal X" proceed under the
triage escape hatches (`proposals/_template.md` > "Triage"). What chat
*cannot* do silently is convert an unreviewed, proposal-worthy design
choice into an accepted outcome. **When it is unclear whether a
directive authorizes action without a proposal, the triage rule is the
arbiter.**

Citing chat input keeps the source auditable without pretending chat
was the Decision: an accepted proposal's Decision section names *what
was decided*; the body's chat-input citations name *what shaped the
draft*. This is the input-side complement to the procedural-gap inline
Decision above — that rule says what the Maintainer *can* close on a
live artifact; this one says what chat *cannot* silently become.

## Surfacing judgment calls to the Maintainer

Much work divides into a large mechanical part and a smaller set of
**judgment calls** that need the Maintainer's direction — the ~20%
where acting silently is wrong because the choice turns on priorities,
history, or trade-offs the agent cannot see. Surface those as a
structured kickoff, not as silent decisions buried in the work:

* **Finish the mechanical part first, queue the judgment calls.**
  Complete the clearly-mechanical ~80%, accumulating the queue as you
  go; then stop and surface it in a single message before committing.
  Don't bundle judgment calls into mid-work commits.
* **Lead with what changes for the user, not the architecture.** If
  the Maintainer is reasoning about outcomes and real workflows, answer
  in those terms; the architectural framing follows as supporting
  structure, not the lead.
* **Give 3 options + a recommended pick + plain-English rationale.**
  The Maintainer's time is the bottleneck; pre-digesting the decision
  space with a *defensible recommendation* (not "it depends") is the
  agent's contribution. If you genuinely cannot choose without their
  input, say so rather than hedging.
* **Name what each option changes on disk** — in the roadmap board,
  the docs, the code. Concrete diffs ("this entry collapses to one
  line", "this gate is deleted") beat abstract framings ("we'd tighten
  the contract").
* **Wait for direction, then fold the dispositions into one commit**
  with the related work — not a separate "mechanical" and
  "judgment-call" commit.

The Maintainer brings framing the agent lacks (priorities, project
history, what users do); the agent brings structural surfacing the
Maintainer has not inspected (cross-references, doctrine implications,
downstream effects). Surfacing well is the agent's half of that
exchange.

## Deferred-follow-up revival

An accepted proposal may carry an **explicitly deferred**
item — a sub-question or sub-scope deferred to a later proposal.
When the time comes to revive that deferred follow-up, **the
revival is itself proposal-worthy** under the standard trigger
conditions: substantive scope, public-contract changes,
cross-cutting refactor, new abstractions, scientific assumptions.

A deferred follow-up does not become implementable just because
it is revisited. The proposal that originally deferred it named
the deferral as a recognition that the substance had not yet
been deliberated, not as an authorization to implement it later
without further review. Reviving the item re-enters the
proposal lifecycle from `proposed`.

This rule prevents the pattern where a deferred follow-up
accumulates implementation detail in side conversations between
the original Decision and its eventual revival, then lands
without ever returning to the deliberation surface. The
append-only record's value depends on every substantive change
having a recorded review; the revival rule is what keeps that
guarantee intact across the time gap a deferral introduces.

## The roadmap is a current-state index, not a historical log

The roadmap surface is **a current-state index**, not a record
of completed work. Open and in-flight items live there; items
that complete migrate **out** of the roadmap and into the
durable record — the archived proposals and plans, the
implementing commits, the changelog. Completed entries are
*removed*, not crossed off or struck through.

The failure mode this addresses: a roadmap that accumulates
"completed" entries gradually becomes the primary
where-did-this-happen surface, when in fact the archived
artifacts are where the truth lives. The roadmap's completed
entries are short, lossy, and out of date by definition; the
archived artifacts are full, durable, and dated to the
implementing commit. A reader who treats the roadmap as a
historical log reads from the worse surface.

The no-history posture forces the durable record to *be* the
durable record, rather than being shadowed by an incomplete
summary. It also keeps the roadmap usable: a roadmap that holds
only what is open or in flight reads quickly and answers
"what's live?" cleanly.

## Adaptation

The lifecycle is part of the **invariant kernel** — no adaptation
dimension removes it. What scales with the team is the *review*
applied within it (see `dual-review.md` and `dimensions/`): a
solo, single-agent team runs the lifecycle with a lighter review
tier; it still runs the lifecycle. The forkable proposal and plan
templates live in `templates/`; this document explains what they
are for and why their contracts are shaped as they are.
