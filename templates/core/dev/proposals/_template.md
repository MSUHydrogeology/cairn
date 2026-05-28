<!-- Author tip: if your proposal cites count claims (numbers
     adjacent to `lines` / `proposals` / `plans` / `tests` /
     `commits` / `files`), claim_check will soft-flag them.
     Four clearance paths -- see "Count claims" section below for
     details:
       1. Rephrase to a delta
       2. Cite the command that computed the count
       3. Add an inline `<!-- claim-check-allow-count: N noun -->`
          directive next to the claim
       4. Consciously accept in the implementing commit body
     -->

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
  one. `Status:` is the one mutable field. *(One bounded exception:
  inserting a `claim_check` marker line — `Proposed/Untracked/External-repo
  paths:` — adjacent to a path token is **mechanical maintenance, not
  authoring a review** (additive-only, mechanical, its own labeled
  `claim-marker maintenance:` commit, typo-guarded). See
  `dev/agent_collaboration.md` / the lifecycle doctrine.)*
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

For non-trivial work, the `**Plan review**` metadata line states the
anticipated plan-review tier — `required(<tier>)` or `not
required(<rationale>)`, with **no silent default** — which the Maintainer
ratifies in the Decision and which the opened plan inherits. A
`required` plan opens in `awaiting-plan-review` and does not start
implementation until its plan-review section lands (the
*review-before-implement* gate; see `../plans/_template.md` > "The
plan-review precondition").

## File moves

An **accepted** proposal stays in `dev/proposals/` after the
Decision; it moves to `dev/proposals/archive/` in the
trivial-implementing commit, or in the plan-open commit for
non-trivial work. A **rejected** or **superseded** proposal moves
to `archive/` in the Decision commit itself. An archived proposal
is closed — link maintenance only; to change an accepted decision,
open a new proposal that supersedes it.

## Count claims -- soft-flag clearance

`claim_check` soft-flags any **count claim** -- a number directly
adjacent to one of six tree-nouns: `lines`, `proposals`, `plans`,
`tests`, `commits`, `files`.  Example soft-flag triggers:

* "5-10 files at scale" (forward-looking range estimate)
* "281 tests" (live-computed from `pytest --collect-only`)
* "12,847 nodes" (-- **not** a tree-noun, doesn't flag)
* "13 CHANGELOG entries" (-- **not** a tree-noun, doesn't flag)

<!-- claim-check-allow-count: 10 files, 281 tests -->
<!-- ^ This template's own teaching examples are self-exempted
     here.  The inline directive form is mechanism (3) below;
     this section thus demonstrates its own recommended pattern. -->

The flag's job is to catch **memory-quoted absolute counts** that
should be deltas or live-computed; the scanner can't tell legitimate
counts from misremembered ones.  Four clearance mechanisms exist;
pick one per claim:

1. **Rephrase to a delta** -- "+5 files vs current N" rather than
   an absolute number.  Best when the claim is structurally a
   change-size.
2. **Cite the command that computed the count** -- "281 tests (per
   `pytest --collect-only`)."  Best for live-from-probe claims; the
   adjacent command names the cheap defense the reader can re-run.
3. **Inline `<!-- claim-check-allow-count: N noun, ... -->`
   directive** -- exempts specific count tokens on adjacent prose.
   Best for forward-looking range estimates ("at scale")
   where rephrasing would lose information.  **Reserved for
   prescriptive rules (e.g., doctrine wording like "5-10 commits")
   or historical quotes; never for live / mutable counts where
   mechanisms (1) delta or (2) cited command would be cleaner.**
   Multiple nouns per line; multiple directives per document.
   Example:

       The catalog will hold roughly a dozen theory files at scale.

       <!-- claim-check-allow-count: 12 files -->

4. **Consciously accept in the implementing commit body** -- name
   the count, name why the soft flag is acceptable (forward-looking
   estimate, live-probe, etc.), and the commit body becomes the
   audit trail.  Use sparingly -- (3) is usually cleaner; (4) is
   the fallback when inline-exempt would clutter the prose.

**Avoid the discipline antipattern**: do **not** rephrase by
substituting non-tree-nouns purely to avoid the flag (e.g., "five
theory documents" instead of "5 files").  The discipline targets
quoted absolute counts; substituting nouns hides the count rather
than grounding it.

<!-- claim-check-allow-count: 5 files -->
<!-- ^ The "+5 files" delta-example in mechanism (1) above and
     the "5 files" antipattern example are self-exempted here. -->

---

# {{proposal title}}

**Author**: {{name / role}}
**Date opened**: {{YYYY-MM-DD}}
**Status**: proposed
**Touches**: {{the files / surfaces this changes}}
**Plan review**: {{if non-trivial — required(<tier>) | not required(<rationale>); ratified at Decision}}

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

<!-- cairn:slot documentation-tier-home -->
(Filled from the `documentation-plan` default-on module when installed
— paste content from `dev/modules/documentation-plan.md` > "Merged
into" > Block 2: dev/proposals/_template.md. The merged content names
the per-layer routing rule for doc + doctrine changes, pointing at
`docs/DOCUMENTATION_PLAN.md`. If documentation-plan is not installed,
replace with `N/A: documentation-plan not installed`. An unfilled
slot is a review finding.)
<!-- cairn:end documentation-tier-home -->

### Doctrine-change rate-limit (if this proposal changes doctrine)

If this proposal **changes doctrine** — a rule, process, or
contract every contributor follows — it must clear the
doctrine-evolution gate (`doctrine/rationale.md` > "How the
doctrine evolves under evidence"). Link the justification here:

* the **recurrence** evidence (the same failure shape, ≥2 times in
  a rolling window), or
* the Maintainer's **high-risk classification** (a security or
  data-loss surface), or
* the **goodnight-time synthesis** that aggregated the signal into
  this proposal.

A single incident does not justify a doctrine change unless it is
the high-risk case. *This prompt applies to a proposal that
introduces a **new** doctrine change. A proposal that merely
**syncs or ports already-accepted doctrine** from one place to
another is not itself a new change — it cites the original
accepting Decision and the gate does not re-apply.*

## Rationale

Why this change, and why now — the user-facing or project-facing
improvement it delivers.

## Alternatives considered

The other options, and why each was not chosen — including "do
nothing". If the draft incorporates the Maintainer's chat-mode
preferences, cite them here (or in *Rationale*) as **"maintainer
preference during drafting"** with the quote or paraphrase — chat
input shapes the draft but is not the Decision (see `doctrine/lifecycle.md`
> "Chat preferences are not a lifecycle Decision").

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
