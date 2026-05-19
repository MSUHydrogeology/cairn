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

## The plan-archive precondition

**A plan never archives until a code review has occurred.** The
plan-archive commit is always distinct from the implementing
commits — it is the artifact of "review happened, and the loop is
closed". When the implementation fits in one commit, plan-open and
that commit may combine; the plan-archive commit still stands
alone, after review.

Code review's reviewer is **not the implementing agent**.

---

# Plan: {{short title}}

**Source proposal**: {{link to dev/proposals/archive/...}}
**Status**: open
**Last update**: {{YYYY-MM-DD}}

## Source proposal

A one-paragraph summary of what the proposal decided. The plan
executes the decision; it does not re-litigate it.

## Scope

What this plan executes — and, explicitly, what it does *not*
(work the proposal deferred to a follow-up).

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
