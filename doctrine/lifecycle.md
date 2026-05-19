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

## Adaptation

The lifecycle is part of the **invariant kernel** — no adaptation
dimension removes it. What scales with the team is the *review*
applied within it (see `dual-review.md` and `dimensions/`): a
solo, single-agent team runs the lifecycle with a lighter review
tier; it still runs the lifecycle. The forkable proposal and plan
templates live in `templates/`; this document explains what they
are for and why their contracts are shaped as they are.
