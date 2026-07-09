<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/rationale.md doctrine/proposals.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Committer independence for automated reviews: a disclosed-scribe carve-out for the Internal tier, ironclad committer for the External tier

**Author**: Claude (Strategy)
**Model**: Claude Fable 5
**Date opened**: 2026-07-08
**Status**: proposed
**Touches**: `doctrine/dual-review.md` (the committer-independence doctrine + rationale) and the review-attribution rule in `AGENTS.md` / `templates/core/AGENTS.md` (the operational addendum). **This is a doctrine change** — it clears the rate-limit gate below.
**Related**: raised as finding **R6** in the Internal review of `2026-07-08-claude-review-record-integrity` (this proposal is that finding's promised follow-up); Maintainer directed opening it (2026-07-08). Rule family: `doctrine/dual-review.md` tier floors; the "Reviews are attributed and self-committed" rule in `AGENTS.md`.
**Plan review**: required(External) — a doctrine change to the review-integrity contract should itself clear the differentiating (cross-type External) tier it governs. Ratified at Decision.

## Context

Running Cairn's own lifecycle with **fresh-context subagents filling the
review roles** (Maintainer-directed, 2026-07-08) surfaced a real gap in
the attribution contract. `AGENTS.md` states: *"the named reviewer commits
their own findings, or the Maintainer does … a structurally-independent
read is only independent if its author is its committer."* But an automated
fresh-context reviewer — a subagent with no shared context, which cleanly
satisfies the Internal floor's *"same agent type, fresh session"*
(`doctrine/dual-review.md:46`) — **cannot run git**. So its review must be
committed by someone else. If the **orchestrating author-session** commits
it, that is the author committing the review of their own change — precisely
the coupling the self-commit rule exists to prevent.

This is not hypothetical: it occurred in the review-record-integrity
proposal's own Internal review (committed `e31625c`), where the author-session
scribe-committed the panel's findings with full disclosure, and flagged the
tension as R6 rather than papering over it. The pattern will **recur on every
proposal** in the broad-look tighten-up series, so the contract needs a rule,
not a per-case improvisation.

The gap has a natural resolution once the two tiers' **purposes** are taken
seriously (`doctrine/dual-review.md:16-22`):

* **Internal review *wants the change to succeed*** — it is the *helping*
  tier; author and Internal reviewer are already aligned toward improving the
  change. Here, an author-committed review carries little integrity risk,
  because the reviewer is not adversarial to the author in the first place.
* **External review *makes the change prove it should land*** — it is the
  *adversarial gate*, the differentiator. Here, the author must **not** control
  the review pipeline; committer independence must be ironclad, or the gate is
  hollow.

## Proposal

Add a **committer-independence** rule to `doctrine/dual-review.md`, tiered to
match the two tiers' purposes, plus a one-line operational addendum to the
review-attribution rule in `AGENTS.md`.

### The rule

* **External tier (the gate): ironclad committer independence.** An External
  review is committed by its author (the different agent type or human
  reviewer) or by the Maintainer — **never** by the change's author-session.
  No automated-scribe carve-out. If the External reviewer cannot commit, the
  Maintainer commits it. This preserves the adversarial gate's independence
  exactly as today.
* **Internal tier (the helper): a disclosed-scribe carve-out.** An Internal
  review produced by a **fresh-context automated reviewer that cannot itself
  commit** (e.g. a subagent panel) MAY be committed by the orchestrating
  author-session **as a disclosed scribe**, bounded by four mandatory
  properties — absent any one, the carve-out does not apply and the Maintainer
  must commit:
  1. **Disclosed mechanism** — the Review section names that it was produced by
     a fresh-context automated reviewer, the reviewer's model/type, and that the
     committer is the author-session acting as scribe.
  2. **Faithful transcription** — an explicit on-the-record statement that no
     finding was softened, reordered by severity to bury, or dropped.
  3. **Auditable source** — the raw reviewer output is recoverable (e.g. the
     workflow journal / transcript path), so the transcription can be checked
     against the source by a third party.
  4. **Internal tier only** — the carve-out never applies to an External review
     (see the gate rule above).

### Documentation / doctrine surface

* **`doctrine/dual-review.md`** — the canonical home: a new "Committer
  independence" subsection carrying the tiered rule and the purpose-based
  rationale (the *why* lives with the review doctrine).
* **`AGENTS.md` / `templates/core/AGENTS.md`** — the operational addendum: the
  existing "Reviews are attributed and self-committed" paragraph gains one
  sentence naming the Internal disclosed-scribe carve-out and the External
  ironclad-committer rule, pointing at `dual-review.md` for the full rule
  (per the doc-governance routing: operational imperative here, rationale in
  the doctrine).

No other surface changes. The rule is vendor-neutral ("a fresh-context
automated reviewer that cannot itself commit"), naming no specific harness.

### Doctrine-change rate-limit

This **is** a new doctrine rule, so it clears the gate
(`doctrine/rationale.md` > "How the doctrine evolves under evidence"):

* **Maintainer high-risk classification.** The Maintainer classified the
  subagent-review committer question as worth codifying (2026-07-08, choosing
  "open the doctrine proposal") — and the surface is **review-record
  integrity**, Cairn's load-bearing differentiator, which is the high-risk /
  high-value class the rate-limit reserves for single-incident doctrine change.
* **Pre-empts a recurring practice, not a one-off.** Subagent-filled review is
  now the standing mechanism for the tighten-up series; the rule governs a
  practice about to repeat many times, not a lone incident.

## Rationale

* **Which workflow does it improve?** Every Cairn adopter running review with
  subagents (a common configuration) now has a clear, honest rule for who
  commits the review — instead of either a human bottleneck at every review or
  an undisclosed author-commits-review coupling.
* **What contract does it preserve?** The External gate's independence is
  preserved *exactly* as today (no carve-out). The Internal tier gains a
  scalable, auditable mechanism whose disclosure requirements defeat the actual
  hazard the self-commit rule targets: attribution laundering.
* **Correctness/transparency improved?** The disclosed-scribe requirements
  (disclosure + faithful-transcription statement + auditable source) make the
  transcription *checkable* by a third party — arguably a stronger integrity
  guarantee than an unaudited human reviewer's self-commit.
* **Why now?** The pattern is live and recurring in Cairn's own tree; codifying
  it before the tighten-up series (and before the first external adopter forks
  the review doctrine) prevents an undisclosed-coupling precedent from setting.

## Alternatives considered

1. **Do nothing (per-case improvisation).** Rejected — leaves the coupling
   unruled; each proposal re-decides it, and an adopter has no guidance.
2. **Maintainer commits every subagent review.** Clean under the letter of the
   current rule, but reintroduces a human bottleneck at every review transition
   — defeating much of the point of subagent-filled review, and disproportionate
   for the *helping* tier. Retained as the fallback when a disclosed-scribe
   property is unmet.
3. **Forbid subagent-produced reviews entirely.** Rejected — throws away a
   genuinely strong independence mechanism (a fresh-context subagent has *zero*
   context bleed, arguably cleaner than a human's "fresh session") to avoid a
   committer-attribution technicality.
4. **Disclosed-scribe for both tiers.** Rejected — the External tier is the
   adversarial gate; letting the author-session control the pipeline of the
   review meant to kill their change hollows out the differentiator. The
   tier-split is the point.
5. **Recommended: disclosed-scribe carve-out for Internal only; ironclad
   committer for External.**

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

* **Invariant.** No External review is ever author-session-committed; every
  author-scribed Internal review carries all four disclosed-scribe properties.
  *Enforced by:* review discipline + (optionally, a follow-up) a lint that flags
  an External Review section whose committer equals the proposal author, and an
  author-committed Internal review section missing the disclosure/faithful-
  transcription statement. (The enforcement lint is **not** in this proposal —
  it is a candidate follow-up, to avoid the "invent a mechanism" over-reach the
  sibling proposal's review flagged.)
* **Failure modes.** A disclosed-scribe Internal review missing any property
  fails *closed* to "the Maintainer commits it." There is no silent-degrade
  path.
* **Edge cases.** A mixed panel (some human, some subagent) → treat as the
  strictest member. A subagent *External* review (a genuinely different model
  type run as a subagent) → still needs a non-author committer (the Maintainer),
  since the carve-out is Internal-only. A human Internal reviewer → unaffected;
  they commit their own.
* **Known omission.** This proposal writes the *rule*; the optional enforcement
  lint is deferred to a follow-up so the doctrine change is not entangled with
  new tooling.

### Tests required

* **N/A for the doctrine text itself** (prose doctrine has no pytest surface).
  `scripts/check_cairn.py` and `scripts/quality_gate.py --sub neutrality` must
  stay clean over the edited `dual-review.md` and `AGENTS.md` (the rule names no
  vendor).

### Examples / smoke checks

* `python scripts/check_cairn.py` clean over the doctrine + AGENTS.md edits.
* `python scripts/quality_gate.py --sub neutrality` shows no new findings from
  the added text.
* The rule is dogfooded immediately: the sibling review-record-integrity
  proposal's Internal review (`e31625c`) is re-read against the four properties
  as the worked example — it should satisfy them (it discloses the mechanism,
  states nothing was softened, and its source is the workflow journal).

## Signals the change is wrong

* Adopters read the disclosed-scribe carve-out as a license to author-commit
  *External* reviews → the tier-split wording was too weak; tighten the External
  gate language.
* The four properties prove unfalsifiable in practice (no one can actually check
  "nothing was softened") → strengthen property 3 (auditable source) into a hard
  requirement that the raw reviewer output is committed or linked, not merely
  "recoverable."
* The rule is never used because subagent review doesn't recur → it was
  premature; but the tighten-up series already exercises it repeatedly.

## Review -- {{reviewer}} -- {{YYYY-MM-DD}}

*(Awaiting Internal review — fresh-context subagent panel, same mechanism this
proposal governs, committed under the very disclosed-scribe carve-out it
proposes, as the live dogfood. Then an External cross-type read before the
Decision, per the required(External) plan-review line — this doctrine change
should clear its own External bar.)*

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer, after the External read. No agent self-Decides; a
doctrine change is the Maintainer's to ratify.)*
