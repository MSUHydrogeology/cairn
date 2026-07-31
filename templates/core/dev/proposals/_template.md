<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/rationale.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Author tip: numeric claims follow the three-kind precision /
     `as_of` discipline -- approximate a decision-irrelevant count
     (`~4900 lines`), date a snapshot (`N, as_of YYYY-MM-DD`, never
     re-measured), register a live invariant; never quote one from
     memory.  See `doctrine/proposals.md` > "Count claims".  (The old
     `claim_check` count soft-flag + `claim-check-allow-count`
     directive were retired 2026-06-05 -- claim_check no longer flags
     counts.) -->

# Proposal template

> **This is the proposal template.** To open a proposal, copy the
> section template below the horizontal rule into
> `dev/proposals/<YYYY-MM-DD>-<author>-<short-slug>.md`, fill it,
> and commit it with status `proposed`. The lifecycle, triage,
> forward-reference-path, file-move, archive-precondition, count-claim,
> and Response-grammar doctrine above the rule live in
> `doctrine/proposals.md` — read it once, then work from the
> sections below.

## The lifecycle

See `doctrine/proposals.md` > "The proposal lifecycle" for the full
lifecycle diagram, the append-only rule, and the one-commit-per-transition
rule.

Two rules are bright-line: **append-only** (earlier sections are immutable;
append new content below the existing arc) and **one commit per transition**
(open, review, response, decision each land as their own commit).

The directory location encodes **work-status**; the `Status:` field encodes
**deliberation state**. Two orthogonal axes. See
[`dev/plans/_template.md`](../plans/_template.md) for the plan
counterpart and the trivial-vs-non-trivial triage rule.

## Triage: trivial vs. non-trivial

See `doctrine/proposals.md` > "Triage: trivial vs. non-trivial" for the full
triage rule and the escape hatch.

Open a proposal when the change touches a public API or config contract,
introduces a new abstraction, moves files, revives a proposal-worthy deferred
follow-up, or has implementation tradeoffs worth a second opinion. Everything
else — a new helper, a test, a typo fix, a self-contained refactor — just
commit.

**Escape hatch, local copy** (a short gloss alongside the pointer above, not
a substitute for it — see `doctrine/proposals.md` for the full rule): if a
change is urgent, clearly reversible, or explicitly experimental, it may
proceed without a proposal, but the commit or follow-up note should say why
the proposal step was skipped. *Sync note:* this gloss is a duplicate of
`doctrine/proposals.md`'s escape-hatch paragraph; if that doctrine text is
ever revised, re-sync this copy in the same change. *Port-exemption note:*
this text predates Cairn's own self-hosting (introduced 2026-06-08, four
days before the 2026-06-12 adoption) — there is no discrete `dev/` Decision
to cite for it.

<!-- cairn:slot triage-extra-triggers -->
(Adopter-specific triage triggers beyond the general list above — e.g.
a domain assumption class the project guards, or a protected-contract
registry. Fill with your project's extra "open a proposal when…"
bullets, or replace with `N/A: no project-specific triggers`. An
unfilled slot is a review finding.)
<!-- cairn:end triage-extra-triggers -->

## Forward-reference paths — `Proposed paths:` marker doctrine

See `doctrine/proposals.md` > "Forward-reference paths" for the full
marker mechanism, placement rules, and the two other marker keywords
(`Untracked paths:`, `External-repo paths:`).

Use the marker when the proposal cites paths it plans to create, future
test / fixture / documentation files, or a future archive path. Place it
near the top of the proposal; the marker exempts tokens on its own line
and any contiguous structured block immediately beneath it.

## File moves

See `doctrine/proposals.md` > "File moves" for the full rule on when the
archive move is decoupled from the Decision-status flip (accepted proposals
stay in `dev/proposals/` until plan-open or the trivial-implementing commit)
and when it is bundled (rejected / superseded proposals archive in the
Decision commit itself).

## Archive preconditions

See `doctrine/proposals.md` > "Archive preconditions" for the rule that every
deferred follow-up must have a durable home before archiving, the acceptable
homes, the required `Follow-ups migrated to:` commit-body form, and guidance
on deferred-follow-up wording.

## Count claims — the three-kind precision / `as_of` discipline

See `doctrine/proposals.md` > "Count claims" for the three-kind discipline
(decision-irrelevant / dated snapshot / live invariant) and the retired
`claim-check-allow-count` directive.

---

# {{proposal title}}

**Author**: {{name / role}}
**Model**: {{your actual running model — query and state it; don't copy a label from an old template or archive}}
**Date opened**: {{YYYY-MM-DD}}
**Status**: proposed
**Touches**: {{the files / surfaces this changes}}
**Related**: {{roadmap links, prior proposals, commits, issues}}
**Plan review**: {{if non-trivial — required(<tier>) | not required(<rationale>); ratified at Decision}}

## Context

What problem is being solved? What is the felt pain that triggered
this? Cite specific files, commits, or issues.

## Proposed paths

*(Optional. Populate as forward-reference paths accrue — files this
proposal would create, surfaces it would touch into existence — so
they don't trigger `claim_check` while the proposal is being authored.
Each entry is the path **and** a one-line note on what it is / when it
materializes. Remove the section if empty. Once a path resolves on
disk, drop its line.*

*Three structural rules for the marker to work: (a) the literal
`Proposed paths:` line below is the marker `claim_check` matches —
don't drop it while bullets remain; (b) **no blank line between
the marker line and the first bullet** — `claim_check`'s
continuation check uses original line numbers, so a gap breaks
adjacency; (c) **keep each bullet on a single physical line** —
wrapped/indented bullet continuations close the marker block and
re-expose subsequent paths to hard-check.)*

Proposed paths:
- `path/to/proposed/file.md` — what it is; when it lands.

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
improvement it delivers. Per the collaboration agreement's review
checklist:

* Which user workflow does it improve?
* What stable contract or module boundary does it preserve or clarify?
* What domain-specific transparency, reproducibility, or correctness
  does it improve? (if applicable)
* Why is now the right time?

## Alternatives considered

What else was on the table? Why does this win? Naming the alternatives
is more important than picking the best one — it forces the reviewer
to push back at the right level. Include "do nothing". If the draft
incorporates the Maintainer's chat-mode preferences, cite them here
(or in *Rationale*) as **"maintainer preference during drafting"**
with the quote or paraphrase — chat input shapes the draft but is not
the Decision (see `doctrine/lifecycle.md` > "Chat preferences are not
a lifecycle Decision").

## Evidence / verification plan

What proves the change works, and what signal would tell us it's
wrong?

The three things every change accounts for: the **tests** that prove
it, the **examples / smoke checks** that exercise it end-to-end, and
the **docs** it delivers (named earlier under `## Proposal >
Documentation / doctrine surface`). Name each, or give an explicit
"**N/A**: <reason>" — silent omission is a review finding.

### Author-accounting — invariants, failure modes, edge cases

<!-- Triage-gated. Fill this for a HIGH-STAKES change — a scientific /
modeling-assumption change, a public-API or config-contract change, a
protected-schema change, or a new abstraction. For a routine or mechanical
change, a one-line "N/A: no new contract / invariant / public path" is the
correct entry, not an empty table. -->

For a high-stakes change, account up front for what a reviewer would
otherwise have to *discover* — collapsing the review from "find the absence"
to "check this claim":

* **Invariants** — what must stay true (e.g. "the manifest's `schema_version`
  is always a known value"), and what *enforces* each (a validator, a test).
* **Failure modes** — how it fails, and whether each failure is *closed*
  (raises) or *open* (degrades) — and whether the open ones are intentional.
* **Edge-case inventory** — empty / None / zero / single / N≫1 / mismatched
  units or CRS: which are handled, which are out of scope.
* **Public-path → test mapping** — each public entry point this change adds
  or touches, mapped to the test that exercises it *through its public path*
  (not via a helper or a stub). Write the mapping as a **relative markdown
  link** to the test file — target relative to this document, e.g. a link
  whose target is `../../tests/contract/<your_test>.py` — so the link checker
  verifies the cited test exists. (Shown as a bare path here so this template
  itself stays link-clean; in a real proposal, write it as an actual relative
  markdown link to that test file.)
* **Known omissions / intentionally untested edges** — the one line that
  keeps this honest: what you did *not* cover, and why.

This block is **reviewed as evidence, not accepted as a filled form**: the
reviewer challenges at least one row (or names the row they sampled and
verified) — "which invariant has no enforcer? which public path has no
through-test?" — never "the table is present." An empty in-scope block is
itself a finding.

**Prospective only.** This accounting — and the review sweep that checks it
(`doctrine/dual-review.md`) — applies to active and future artifacts; an
archived proposal or plan is immutable and is never retro-fitted with it.

### Tests required

<!-- cairn:slot tests-tier-home -->
(Adopter-specific test-tier taxonomy — name the project's test
directories and speed / environment markers so the author can route
the required tests by tier and by name. Fill from the project's test
plan, or replace with `N/A: no tiered test layout`.)
<!-- cairn:end tests-tier-home -->

### Examples / smoke checks

<!-- cairn:slot examples-smoke-home -->
(Adopter-specific examples / smoke-check surfaces — the gallery, CLI
sanity commands, notebook smokes the change can exercise end-to-end.
Fill with the project's runnable checks, or replace with `N/A: no
end-to-end exercisable surface`.)
<!-- cairn:end examples-smoke-home -->

## Signals the change is wrong

The observations that would show this change should be reverted or
rethought — and the recovery for each.

## Review -- {{reviewer}} -- {{YYYY-MM-DD}}

**Model**: <your actual running model or tier when known; "unknown" if not. Do not copy-paste old model labels from past templates or archives; query and state your running model identity.>

Proposal reviews are written into the proposal file by default.
Chat comments can help the conversation, but they are not the durable
review record. Append the review as a new section in this file,
commit that lifecycle transition, and let the author's Response
answer the numbered critiques here.

**Steelman first** (per the review norms in
`dev/collaboration_agreement.md`). What's right about this proposal?

Then critique. Number each substantive concern so the response can
address them point-by-point. Use the project's review lenses where
relevant (workflow coherence, data contracts, extensibility,
operational maturity).

Critiques are prose-first. When a critique is *also* a specific edit
suggestion, attach it in one of two forms:

* **Inline suggested edit** — a fenced code block under the critique
  showing the proposed wording / code. Best for small fixes:

      * **[R2]** The triage rule reads as too narrow. Suggested edit:

          > Open a proposal only when the change ... **or when the
          > author wants a second opinion before baking it in.**

* **Review branch** — for substantive rewrites, create a branch
  named `<reviewer>/review-of-<original-slug>` with your edits as
  commits and reference the commit hash(es) in the critique. The
  author can cherry-pick or merge selectively. Push only with
  explicit Maintainer approval (per `AGENTS.md`'s "never commit or
  push without explicit user approval" rule).

      * **[R5]** Section X needs a stronger case. Suggested rewrite
        on branch `<reviewer>/review-of-<slug>` (commits `<sha>`).

Stick to prose-only when the critique isn't an edit — conceptual
concerns, questions, and steelmans don't fit in a diff.

* **[R1]** ...
* **[R2]** ...
* **[R3]** ...

**End with the coverage line + a second-round recommendation** (see
`doctrine/dual-review.md` > "Recommend-and-decide"). Two parts, then a call:

* **Covered** — the review-sweep lenses you swept, each with a falsifiable
  citation (file / test-node / line / command), not a bare "checked."
* **Not covered / low confidence** — the negative space: a lens you could not
  exercise, "same-type reviewer — no cross-type independence on this pass."

Then state an explicit **second-round recommendation** (recommended / not, with
reasons grounded in the negative space). Whether a second structurally-independent
pass runs is the Maintainer's call; a declared-`required` tier still runs
regardless.

## Response -- {{author}} -- {{YYYY-MM-DD}}

**Model**: <model or tier when known; "unknown" if not>

See `doctrine/proposals.md` > "Response — disposition grammars" for
the two-grammar vocabulary (Proposal-Response grammar when no
implementing commit exists; Code-review-Response grammar when
implementing commits are citable by sha).

For each numbered critique, write one disposition token from the
grammar above plus a one-sentence rationale. No silent dropping.
Brief is fine; precision matters more than length.

If accepted critiques substantially change the proposal, write a short
"## Revised proposal" section above this and update `Status:` to
`revised`.

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

Final call: accept, reject, or supersede. Brief reasoning. Optional:
link to the commit(s) that implemented the accepted version.

If accepted and the change touches the roadmap, add a corresponding
`dev/PLANNING.md` entry in the same commit.

*If an agent scribes this Decision at the Maintainer's instruction:
quote or clearly paraphrase the Maintainer's instruction, name the
scribe, and record whether commit permission was explicitly given or
separately confirmed (per `AGENTS.md`'s Decision-commit guard-rail).*
