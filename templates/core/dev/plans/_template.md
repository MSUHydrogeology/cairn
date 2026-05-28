<!-- Author tip: if your plan cites count claims (numbers
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

# Plan template

> **This is the plan template.** A non-trivial accepted proposal
> opens a plan: copy the section template below the rule into
> `dev/plans/<short-slug>.md`. The doctrine above the rule is
> reference.

## The plan lifecycle

```
open -> [awaiting-plan-review] -> executing -> review -> archived
```

* **open** — the plan-open commit creates the plan and archives
  the source proposal.
* **awaiting-plan-review** — *(only for a review-required plan; see the
  plan-review precondition below)* the plan is open but implementation has
  not started, waiting for its plan-review section to land. A plan marked
  `Plan review: not required` skips this status and goes straight to
  `executing`.
* **executing** — implementation commits land.
* **review** — a code-review pass examines the implementation.
* **archived** — after review, lasting truth migrates to durable
  homes and the plan moves to `dev/plans/archive/`.

A plan is an *execution* artifact: its status, progress markers,
and commit hashes are updated in place. Review findings and the
archive record are append-only. *(One bounded exception to those
append-only sections: inserting a `claim_check` marker line —
`Proposed/Untracked/External-repo paths:` — adjacent to a path token is
**mechanical maintenance, not authoring a review** (additive-only, its own
labeled `claim-marker maintenance:` commit, typo-guarded). A task-checkbox
/ status update is ordinary mutable workflow, not this carve-out. See the
lifecycle doctrine.)*

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
that commit may combine — but only for a plan marked `Plan review: not
required` (see the plan-review precondition below); the plan-archive
commit still stands alone, after review.

Code review's reviewer is **not the implementing agent**.

## The plan-review precondition

Symmetric to the plan-archive precondition, at the *entry* boundary:
**a review-required plan does not start implementation until its
plan-review section has landed.** The plan-archive gate guards
*review-before-close*; this gate guards *review-before-implement*.

The gate is **explicit, not remembered**: the `**Plan review**` metadata
line above is mandatory — `required(<tier>)` or `not required(<rationale>)`,
with **no silent default**. The author states it; the Maintainer ratifies.
When `required`, the plan opens in **`awaiting-plan-review`** and its
plan-open and first-implementation commits stay **distinct** (implementation
cannot front-run the review); it advances to `executing` only once the
review section lands. When `not required`, the rationale is on the record
and the plan may combine plan-open with first implementation. The review
*tier* follows the structural-independence framing in `dual-review.md`. See
the lifecycle doctrine for the full statement.

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

# Plan: {{short title}}

**Source proposal**: {{link to dev/proposals/archive/...}}
**Status**: open
**Plan review**: {{required(<tier>) | not required(<rationale>)}}
**Last update**: {{YYYY-MM-DD}}

## Source proposal

A one-paragraph summary of what the proposal decided. The plan
executes the decision; it does not re-litigate it.

## Scope

What this plan executes — and, explicitly, what it does *not* (the
**scope fence**: work the proposal deferred to a follow-up, and
anything deliberately left untouched this pass). See "The planning
handshake" above for the convergence questions this section answers.

### Documentation / doctrine surface

What documentation, doctrine, or contract surface does this plan
touch? If none, say so explicitly — silent omission is a code-review
finding (the plan must name what doc state is mutated, not surface
it at review time).

<!-- cairn:slot documentation-tier-home -->
(Filled from the `documentation-plan` default-on module when installed
— paste content from `dev/modules/documentation-plan.md` > "Merged
into" > Block 3: dev/plans/_template.md. The merged content names
the per-layer routing rule for doc + doctrine changes, pointing at
`docs/DOCUMENTATION_PLAN.md`. If documentation-plan is not installed,
replace with `N/A: documentation-plan not installed`. An unfilled
slot is a review finding.)
<!-- cairn:end documentation-tier-home -->

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
