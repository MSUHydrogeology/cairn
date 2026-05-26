# Plan template

> **This is the plan template.** A non-trivial accepted proposal
> opens a plan: copy the section template below the rule into
> `dev/plans/<short-slug>.md`. The doctrine above the rule is
> reference.

## The plan lifecycle

```
open -> executing -> review -> archived
```

* **open** — the plan-open commit creates the plan and archives
  the source proposal.
* **executing** — implementation commits land.
* **review** — a code-review pass examines the implementation.
* **archived** — after review, lasting truth migrates to durable
  homes and the plan moves to `dev/plans/archive/`.

A plan is an *execution* artifact: its status, progress markers,
and commit hashes are updated in place. Review findings and the
archive record are append-only.

**The plan is the Stage 2 of the Registered Report.** Where the
proposal pre-registered the design and the verification plan
(Stage 1; see `../proposals/_template.md`), the plan and its code
review check the implementation and the evidence it produced
against that locked plan. This is the defense against metric
p-hacking the proposal's Stage 1 named: judged against a prior
commitment, not chosen after the fact.

## The plan-archive precondition

**A plan never archives until a code review has occurred.** The
plan-archive commit is always distinct from the implementing
commits — it is the artifact of "review happened, and the loop is
closed". When the implementation fits in one commit, plan-open and
that commit may combine; the plan-archive commit still stands
alone, after review.

Code review's reviewer is **not the implementing agent**.

## The planning handshake

Before heavy implementation, the team converges on a short set of
questions — a lightweight handshake for plan-shaped work below the
full-proposal bar (a proposal answers these at greater depth; a plan
draining an accepted proposal inherits most of them):

* What workflow or capability are we improving?
* What is the current pain or risk?
* What contract or module boundary is involved?
* What would success look like?
* What tests, docs, or examples prove the change?
* **What must explicitly *not* change in this pass** — the scope fence?

The `## Scope` section below is where these land: it names what the
plan executes *and* what it deliberately leaves alone. The scope fence
is the load-bearing one — an unstated "not this pass" is how a bounded
plan quietly grows.

---

# Plan: {{short title}}

**Source proposal**: {{link to dev/proposals/archive/...}}
**Status**: open
**Last update**: {{YYYY-MM-DD}}

## Source proposal

A one-paragraph summary of what the proposal decided. The plan
executes the decision; it does not re-litigate it.

## Scope

What this plan executes — and, explicitly, what it does *not* (the
**scope fence**: work the proposal deferred to a follow-up, and
anything deliberately left untouched this pass). See "The planning
handshake" above for the convergence questions this section answers.

## Sequence

The commit-by-commit execution order. For larger plans, break each
chunk into its own subsection with a file table.

## Acceptance criteria

The concrete deliverables that define "done": the tests that must
pass, the doc updates that must land, the examples / smoke checks
— each named, or an explicit "N/A: <reason>".

## Verification

The concrete commands the implementation must pass.

## Code review

*(Appended after the implementation commits land, by a reviewer
who is not the implementing agent.)*

## Lasting-truth migration

*(Filled at archive time: where each deferred follow-up now lives,
plus an evidence ledger — what shipped, what was deferred, and
where the deferred work is now tracked.)*
