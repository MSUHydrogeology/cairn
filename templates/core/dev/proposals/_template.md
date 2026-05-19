# Proposal template

> **This is the proposal template.** To open a proposal, copy the
> section template below the horizontal rule into
> `dev/proposals/<YYYY-MM-DD>-<author>-<short-slug>.md`, fill it,
> and commit it with status `proposed`. The doctrine above the
> rule is reference — read it once, then work from the sections
> below.

## The lifecycle

A proposal moves through:

```
proposed -> reviewed -> revised -> accepted / rejected / superseded
```

* **proposed** — the author opens the proposal.
* **reviewed** — a reviewer appends a `## Review` section.
* **revised** — the author appends a `## Response` and, where
  needed, a `## Revised proposal`. Review and revision may repeat.
* **accepted / rejected / superseded** — the Maintainer appends
  the `## Decision`.

Two rules are bright-line:

* **Append-only.** Never edit a prior section — append a revising
  one. `Status:` is the one mutable field.
* **One commit per transition.** Open, review, response, and
  decision each get their own commit.

**A proposal is a Stage 1 Registered Report.** Scientific
publishing has the same shape: a study's design and analysis plan
are reviewed and accepted *before* any data is collected (Stage 1),
and the results are later reviewed against that pre-registered
plan (Stage 2). A proposal locks the change's design *and* its
evidence / verification plan before any code is written — that is
Stage 1. The plan and its code review (see `../plans/_template.md`)
then check the implementation against that lock — Stage 2. The
discipline is a defense against post-hoc *metric p-hacking*: the
verification plan exists before the implementation, so evidence is
judged against a commitment, not chosen after the fact to flatter
whatever the code happened to do.

## Triage — trivial vs. non-trivial

A trivial fix — a typo, a one-line bug, an obvious correction — is
just made; it needs no proposal. A *substantive* change — a new
abstraction, a cross-cutting refactor, a contract change, anything
worth a second opinion — gets a proposal.

Once accepted, the implementation is **trivial** (a single commit,
a single area, no follow-ups — implemented and the proposal
archived together) or **non-trivial** (multiple commits or areas,
multi-stage sequencing, or deferred follow-ups — it opens a plan;
see `../plans/_template.md`).

## File moves

An **accepted** proposal stays in `dev/proposals/` after the
Decision; it moves to `dev/proposals/archive/` in the
trivial-implementing commit, or in the plan-open commit for
non-trivial work. A **rejected** or **superseded** proposal moves
to `archive/` in the Decision commit itself. An archived proposal
is closed — link maintenance only; to change an accepted decision,
open a new proposal that supersedes it.

---

# {{proposal title}}

**Author**: {{name / role}}
**Date opened**: {{YYYY-MM-DD}}
**Status**: proposed
**Touches**: {{the files / surfaces this changes}}

## Context

What problem is being solved? What is the felt pain that triggered
this? Cite specific files, commits, or issues.

## Proposal

The change, concretely — name files, signatures, contracts. What
is added, changed, or removed.

### Documentation / doctrine surface

What documentation, doctrine, or contract surface does this change
touch? If none, say so explicitly — silent omission is a review
finding.

## Rationale

Why this change, and why now — the user-facing or project-facing
improvement it delivers.

## Alternatives considered

The other options, and why each was not chosen — including "do
nothing".

## Evidence / verification plan

The tests, documentation, and examples / smoke checks that will
prove the change. Name each, or give an explicit "N/A: <reason>".

## Signals the change is wrong

The observations that would show this change should be reverted or
rethought — and the recovery for each.

## Review -- {{reviewer}} -- {{YYYY-MM-DD}}

*(Appended by a reviewer; the author does not write this.)*

## Response -- {{author}} -- {{YYYY-MM-DD}}

*(Appended by the author: dispositions on the review's findings.)*

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Appended by the Maintainer: accepted / rejected / superseded,
with the reasoning.)*
