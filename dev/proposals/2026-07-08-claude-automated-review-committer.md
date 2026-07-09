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

## Review -- Claude (Internal, fresh-context subagent panel) -- 2026-07-08

**Model**: Claude Fable 5 (three fresh-context subagents — doctrine-coherence /
rate-limit, independence-integrity, adopter-simplicity — no access to the
authoring session; 22 source critiques consolidated to R1–R12, none dropped).

**Attribution / committer note.** These are the panel's findings, transcribed
faithfully; no finding was softened, reordered to bury, or dropped. Per the very
issue this proposal debates (and per the panel's own R2/R3): the raw source
currently lives in the harness workflow journal (run `wf_1a435c32-22a`), which is
**harness-private and not committed in-tree** — exactly the property-3 gap the
panel identifies. This section is committed under the Maintainer's git identity
(the solo tree's single identity); see R3 on why that collapses the
scribe-vs-Maintainer distinction. Disclosed, not hidden.

**Steelman.** A serious, well-argued proposal that dogfoods honestly and does not
hide its tensions. It identifies a real, recurring gap (a fresh-context subagent
meets the Internal floor yet cannot run git; the self-commit rule has no provision
for a reviewer that cannot commit), surfaces it as R6 rather than papering over
it, and opens a follow-up rather than improvising. The tier-purpose asymmetry is
correctly sourced (`dual-review.md:12-20`); refusing a carve-out at the External
gate (Alt #4) protects the differentiator; the four properties correctly name
attribution-laundering as the hazard; the fail-closed default is right; and it
subjects itself to `required(External)`.

**Critiques** (descending severity):

* **[R1] (blocking, unanimous)** The rate-limit clearance is invalid under the
  gate's own text. `doctrine/rationale.md:337-347` makes the high-risk
  single-incident bypass **exhaustive to two surfaces — security and data-loss —**
  and says any other importance framing "falls outside the bypass and obeys the
  recurrence requirement." "Review-record integrity is the differentiator,
  therefore high-risk" is precisely the excluded framing. The recurrence path also
  fails: one incident (`e31625c`) plus a *prediction* it will recur, not the
  counted (≥2) past recurrence the gate requires (`rationale.md:328-331,366`), and
  the tracker that would count it isn't established yet. Clearing the gate is the
  stated precondition (proposal:9), so this blocks. **Fix:** drop the
  differentiator=high-risk claim; clear the gate honestly via counted recurrence
  or as a gap-fill, or have the Maintainer record an explicit classification that
  acknowledges it is *widening* the two-surface list (itself rate-limited).
* **[R2] (blocking)** Of the four properties, only #3 (auditable source) makes
  laundering *checkable*; #2 ("nothing softened") is self-attestation by the party
  whose independence is in question — the assurance the self-commit rule refuses to
  rely on (`AGENTS.md:114-117`). And #3 is soft ("recoverable … workflow journal /
  transcript path"), not committed-or-linked, and the dogfood fails it: `e31625c`
  cites no source, and no panel transcript is tracked (`git ls-files | grep -iE
  'journal|transcript'` → none); the exemplar source is a harness-private artifact
  a cross-type auditor can't open and a plain-chat solo adopter never produces. So
  the carve-out **relabels** author-commits-review as "disclosed scribe." **Fix:**
  promote property 3 to a hard "raw output committed/linked in-tree at scribe
  time"; drop the harness-private exemplar; absent a committed source, fail closed
  to Maintainer-commit.
* **[R3] (blocking)** "Committer" is never defined (git identity vs. controlling
  agent-session), yet the whole rule turns on it. Read as git identity, the
  dogfood *refutes itself*: `git show -s e31625c` → **Anthony Kendall** (the
  Maintainer), i.e. Alternative 2 (rejected), not the carve-out. In a solo tree
  author==Maintainer==one git identity, so the distinction is invisible in the
  record and the candidate lint can't detect an author-committed External review —
  the "ironclad External committer" rule is asserted, not enforceable. **Fix:**
  define "committer" explicitly and reconcile `e31625c`; because git metadata
  can't distinguish the two in a solo tree, make the disclosure a required,
  machine-detectable **structured marker**, and state that External enforcement
  reduces to that marker + discipline, not committer identity.
* **[R4] (substantive)** The proposal rejects Alt #2 ("Maintainer commits") as a
  "human bottleneck" with no evidence it bites — and the one data point
  (`e31625c`) shows the Maintainer committing without friction, under their own
  identity anyway. For the solo audience (`dual-review.md:439-442`), Alt #2 is the
  honest *default*, not the fallback (the Maintainer already reads every review
  before Decision — the "bottleneck" is one commit they run while in the loop).
  The External branch is *already* Alt #2. The triggering predicate ("cannot itself
  commit") encodes a tool choice (the orchestrator withholds git access) as if
  structural; a harness granting the subagent a scoped identity moots it (Anchor
  13, the waist stays tool-independent). **Fix:** test a single unified rule first
  (any subagent review committed by the Maintainer, or by the author-session with
  the transcript committed alongside); demote disclosed-scribe to a
  dimension-gated advanced option, kept only if the bottleneck is shown real.
* **[R5] (substantive)** "Author-committed Internal review carries little
  integrity risk because the reviewer is non-adversarial" substitutes the tier's
  *purpose* for its *independence property*. `dual-review.md:28-32` grounds all
  review value in independence from the author's blind spots; the self-commit rule
  is tier-agnostic for that reason. And the Internal review isn't inert — it
  produces the second-round recommendation that gates whether External runs
  (`dual-review.md:289-323`); an author who shapes a clean panel can suppress the
  External-escalation (the clean-pass trap, `:189-206`). **Fix:** rest the
  carve-out on the disclosure/auditability properties, not "non-adversarial";
  require the disclosed-scribe review to carry its coverage line + second-round
  recommendation verbatim, and have the Maintainer weight an author-scribed clean
  pass with extra skepticism.
* **[R6] (substantive)** The doctrine already answers "reviewer lacks a
  capability" — `dual-review.md:379-415` (restricted verification surfaces) records
  a verification owner and defaults to Maintainer fallback. A subagent that can't
  commit is the same shape, and the existing answer is Maintainer-as-fallback
  (= Alt 2, which `e31625c` used). **Fix:** reconcile — either extend that pattern
  to the commit capability (the simpler, coherent route), or argue explicitly why
  committing warrants lighter treatment than executing; don't let two adjacent
  mechanisms answer the same shape differently.
* **[R7] (substantive)** The four properties govern only the commit *step*, not
  the panel's *inputs*. The author still chooses which subagents to spawn and
  writes their prompts; a narrowly-briefed panel ("check the citations") yields
  "nothing softened" truthfully because there were no adverse findings — the gaming
  vector sits upstream, unanchored to "brief on facts, not judgment"
  (`dual-review.md:342-358`, unreferenced). **Fix:** add a fifth property — the
  panel brief conforms to brief-on-facts, disclosed as the generic sweep, not a
  change-specific "what to push on."
* **[R8] (substantive)** The tier-split creates a perverse incentive to
  *under-label* independence: the cheap self-scribe path is unlocked only for
  "Internal," so an author is nudged to title a genuinely cross-type subagent read
  "Internal" to avoid pinging the Maintainer — the exact mislabel the *sibling*
  proposal's Part A is fixing. **Fix:** make model/type the determinant — a
  subagent whose type differs from the author is External by floor regardless of
  the section title; cross-check the disclosed model/type against the author's.
* **[R9] (substantive)** The four-property protocol lands as unconditional
  doctrine on every adopter (a `dual-review.md` subsection + an `AGENTS.md`
  sentence), so a solo adopter who will never orchestrate a panel still carries it
  — more apparatus than the lightest-review reservation (`dual-review.md:434-442`)
  and an always-loaded-prose correctness cost (Anchor 12). **Fix:** keep the
  `AGENTS.md` addendum to one sentence; dimension-gate the four-property detail
  behind the orchestrated-subagent configuration.
* **[R10] (minor)** Property 2 is partly unfalsifiable ("reordered … *to bury*" is
  an intent a third party can't verify) and the dogfood under-meets it (`e31625c`
  attests only "no finding softened," never disclaiming reordering). **Fix:**
  reword to falsifiable terms ("every source finding appears, at its source
  severity, wording preserved"); specify the exact attestation sentence.
* **[R11] (minor)** Routing splits one rule-family across two canonical homes: the
  amended rule ("Reviews are attributed and self-committed") lives canonically in
  `AGENTS.md:112-117`, but the proposal makes `dual-review.md` the canonical home
  for the amendment. **Fix:** decide deliberately — one canonical home for the
  operational "who commits" imperative, the other only points.
* **[R12] (minor)** No serialization point is named for verifying the four
  properties; enforcement is author self-certification at commit time. **Fix:**
  name the Maintainer's Decision (or goodnight scrub) as the property-verification
  point, and state plainly that until the lint exists the properties are
  honor-system + a Maintainer spot-check.

**Covered.** The rate-limit gate on both paths (`rationale.md:319-347`); the tier
purposes/floors + recommend-and-decide + clean-pass-trap + don't-telegraph-the-lens
(`dual-review.md:11-49,189-206,289-358`); the tier-agnostic self-commit rule
(`AGENTS.md:112-117`); the restricted-verification-surfaces parallel
(`dual-review.md:379-415`); solo framing + lightest-review reservation; the
always-loaded-prose correctness cost (`rationale.md:144-174`) and waist-minimality
(Anchor 13); the four properties checked against `e31625c` directly; git/fs
verification (`git show -s e31625c` → Maintainer; no tracked transcript). **Not
covered:** did not run `check_cairn`/`quality_gate` (final wording unwritten); no
committed transcript exists to check (that is R2's substance). **Overriding
limitation: a same-agent-type Internal read of a Claude-authored doctrine change
*about cross-type independence* — no cross-type independence on this pass, the
exact blind spot the External floor exists to cover.**

**Second-round recommendation: External is a floor here, not a choice** — the
proposal declares `required(External)`, which `dual-review.md:329` says the
Maintainer honors, not waives. But **sequencing:** because R1–R3 are blocking and
definitional, the author Responds/Revises *first* (or recommends withdrawal), so
the External reviewer reads a coherent artifact, not these cracks. Do **not** route
to Decision on the current text. Live-dogfood note for whoever reads next: this
Internal review is *itself* author-orchestrated subagent work committed under the
Maintainer's identity with no in-tree source — a second live instance of the very
mechanism under debate, and evidence for R2/R3.

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer, after the External read. No agent self-Decides; a
doctrine change is the Maintainer's to ratify.)*
