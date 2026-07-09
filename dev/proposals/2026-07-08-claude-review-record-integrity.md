<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/rationale.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Forward-reference paths this proposal plans to create; they materialize in the implementing plan. -->
<!-- claim-check-allow: scripts/transition_lint.py, bootstrap/tests/test_transition_lint.py, bootstrap/tests/test_onboarding_review_tiers.py, dev/measurement/review-floor-deviations.md -->

# Review-record integrity: fix the mislabeled-independence onboarding, record the showcase-arc provenance, and guard lifecycle transitions

**Author**: Claude (Strategy / Implementation)
**Model**: Claude Fable 5
**Date opened**: 2026-07-08
**Status**: proposed
**Touches**: `templates/onboarding/solo-greenfield.md`; a new test under `bootstrap/tests/`; a new advisory check `scripts/transition_lint.py` + its test; the incident record under `dev/measurement/`; a dated provenance note about the archived `2026-06-12-claude-check_cairn-self-host-compat` arc.
**Related**: the broad-look review `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md` (Themes 1.1, 1.5, 5.2, and fold-up candidate "transition lint"); this is proposal 1 of that note's Phase A ("Record & review integrity", items A1 + A2).
**Plan review**: required(Internal) — touches a shipped template, adds an advisory gate, and edits the deliberation record; Internal floor now (fresh-context subagent), with an External (cross-type) read available and recommended before the Decision because this proposal is *about* the record-integrity differentiator. Ratified at Decision.

## Context

The broad-look review's most consequential theme (Theme 1) is that
Cairn's own deliberation record — the thing the whole methodology sells
— has verifiable cracks exactly where a skeptical outsider looks first.
Three of those cracks are about **review and transition integrity**
specifically, and they form one coherent problem:

1. **The shipped solo onboarding teaches adopters to mislabel their
   reviews.** `templates/onboarding/solo-greenfield.md:76-77`, `:99`,
   and `:115-116`/`:119` tell a solo adopter that fresh-session
   same-vendor review "fills the External tier." Doctrine says the
   opposite: External review requires a different agent type or a human
   (`doctrine/dual-review.md:46-47`; the solo adaptation at
   `dual-review.md:434-442` names fresh-session review as the *Internal*
   floor and never claims it fills External). The first external
   adopter would, from day one, commit a record asserting a structural
   independence the doctrine says it does not have — corrupting the
   exact property Dual-Review is differentiated on.

2. **Our own showcase arc's commit history misstates what happened.**
   The first self-hosted proposal
   (`dev/proposals/archive/2026-06-12-claude-check_cairn-self-host-compat.md`)
   was opened by commit `17b7e5c` whose tree already contained both the
   Internal and the Gemini External review sections, while the
   proposal's Status line still read `proposed`; the next commit
   (`f4a8308`), whose message says it appends the Gemini review, adds no
   review content. The likely truth is innocent (a batched write-up of
   review done in chat), but the record does not say so, and an outside
   auditor cannot tell "written up afterward" from "fabricated." The
   two review-floor deviations of that same day (a same-session Internal
   read below the fresh-session floor; a `required(Internal)` plan-review
   line the Decision never addressed — Theme 1.5) were likewise never
   recorded as exceptions.

3. **Nothing mechanical would have caught either.** The
   one-commit-per-transition rule (`doctrine/lifecycle.md`; AGENTS.md's
   git workflow) is real doctrine, but it is enforced only by memory.

The fix follows the same shape as the accepted `adopter-entry-doc-refresh`
proposal: **fix the live instance, correct the record, and add a cheap
guard so the class cannot silently recur.**

## Proposed paths

Proposed paths:
- `scripts/transition_lint.py` — the advisory transition-lint check (Part C); lands in the plan's implementation.
- `bootstrap/tests/test_transition_lint.py` — its behavioral test; lands with it.
- `bootstrap/tests/test_onboarding_review_tiers.py` — the preset-review-tier guard test (Part A); lands with it.
- `dev/measurement/review-floor-deviations.md` — the incident ledger recording the 2026-06-12 deviations (Part B); the plan reconciles its exact name/format with the incident-trackers module's canonical ledgers.

## Proposal

Three parts, one argument (the review record must honestly represent
independence and transitions).

### Part A — fix the mislabeled-independence onboarding (the live instance)

* Reword the three passages in `templates/onboarding/solo-greenfield.md`
  (lines 76-77, 99, 115-116/119) so fresh-session review is named the
  **Internal floor**, and the **External tier is explicitly unstaffed**
  until a second agent type or a human reviewer exists — matching
  `doctrine/dual-review.md:434-442`. Name adding a second agent type as
  the recommended first graduation step (Theme 5's degradation
  finding), rather than implying the solo floor already delivers
  External independence.
* Add `bootstrap/tests/test_onboarding_review_tiers.py`: assert that no
  shipped onboarding preset pairs the token "External" with
  "fresh-session"/"same-vendor" review. This is the drift guard that
  keeps the mislabel from re-entering any preset.

### Part B — record the provenance honestly (correct the record)

* **Establish the incident ledger** `dev/measurement/review-floor-deviations.md`
  (Cairn's own `dev/measurement/` currently holds only a README — the
  incident trackers the default-on module prescribes are unpopulated).
  Record the two 2026-06-12 review-floor deviations as dated entries:
  the same-session Internal read, and the un-ratified plan-review
  requirement — each with what the floor is, what happened, and that no
  waiver was recorded at the time.
* **Record the showcase-arc provenance.** State, in a durable and
  auditable location, how commits `17b7e5c` / `f4a8308` actually came
  to carry / not-carry their review content, so the archived arc is no
  longer only refutable-looking. **Open question for review (below):**
  the archived proposal is immutable doctrine
  (`doctrine/lifecycle.md`: an archived proposal "is never
  retro-fitted"), so the correction's *home* is a real choice — the
  incident ledger, a short strategy note, or a clearly-marked
  out-of-lifecycle annotation. This proposal defaults to the incident
  ledger and asks the reviewer/Maintainer to confirm.

### Part C — guard lifecycle transitions (prevent recurrence)

* Add `scripts/transition_lint.py`: an **advisory** (exit-code, not
  fail-closed) check over a commit range that flags two shapes:
  (a) a commit whose subject/body claims a lifecycle transition
  ("open", "review", "response", "Decision") but whose diff adds no
  corresponding proposal/plan section; and (b) a proposal-**open**
  commit whose added file already contains `## Review` sections. It is
  a discipline aid in the same family as `scripts/quality_gate.py` — a
  heuristic that shifts a cheap mechanical check left, not a gate that
  blocks. Scope is deliberately narrow to keep false positives low; the
  plan pins the exact heuristics and the allowed-exception vocabulary.
* Add `bootstrap/tests/test_transition_lint.py` exercising both flag
  shapes and at least one benign case that must *not* flag (e.g. a
  claim-marker-maintenance commit).

### Documentation / doctrine surface

* **Part A** edits a shipped **template** (descriptive/adopter surface),
  not doctrine — it brings the template into line with existing
  doctrine (`doctrine/dual-review.md`), so no doctrine changes.
* **Part B** writes into the **deliberation/measurement layer**
  (`dev/measurement/`) — records, not rules.
* **Part C** is **tooling** that enforces the *existing*
  one-commit-per-transition rule; it introduces no new rule. Per the
  doc-tier home rule, none of the three routes to `AGENTS.md` or
  `doctrine/`.

### Doctrine-change rate-limit (if this proposal changes doctrine)

**N/A — no doctrine change.** Part A syncs a template to already-accepted
doctrine; Part C is enforcement tooling for an already-accepted rule
(`doctrine/lifecycle.md` one-commit-per-transition). The rate-limit gate
governs *new* doctrine; neither leg introduces one. (Should review
decide the transition-lint's exception vocabulary needs a doctrine home,
that becomes a separate, rate-limited proposal.)

## Rationale

* **Which user workflow does it improve?** The first external adopter's
  daily review loop: Part A stops them mislabeling their own reviews
  from session one, and names how to actually strengthen review.
* **What contract does it preserve/clarify?** The Dual-Review tier
  contract — the difference between Internal (same agent, fresh session)
  and External (different agent type or human), which is Cairn's
  headline differentiator.
* **Transparency / correctness improved?** Part B makes the showcase
  record honest where a skeptic checks first; Part C makes the
  transition-provenance class mechanically visible instead of
  memory-enforced.
* **Why now?** The postdoc install is imminent; they will fork the
  shipped onboarding and read the self-hosted archive as the worked
  example. Both must be honest *before* that read, not after.

## Alternatives considered

1. **Do nothing.** Rejected — Theme 1's findings stand; the mislabel
   ships into the first adopter's record and the showcase looks
   fabricated to a skeptic.
2. **Part A only (fix the template, skip the record + the guard).**
   Partial — fixes the instance but leaves the showcase uncorrected and
   the class free to recur; the audit explicitly flags recurrence as the
   deeper problem.
3. **Fold this into one big "Phase A" proposal.** Rejected — Phase A is
   a release-readiness bucket, not one coherent decision; bundling
   forces a single accept/reject over unrelated risk classes (licensing,
   engine robustness) and hands review an un-reviewable pile. This
   proposal is the coherent review-integrity slice.
4. **Make the transition-lint a fail-closed gate.** Deferred — an
   advisory check matches the "discipline aid, not a gate" posture Cairn
   already takes with `quality_gate.py`; a hard gate over `git log`
   heuristics risks exactly the false-positive nagging that trains
   people to ignore gates (the Theme 3.4 R6 lesson). Escalation to a
   gate is a later call if the advisory version proves reliable.
5. **Recommended: Part A (instance) + Part B (record) + Part C
   (prevention).**

**Maintainer preference during drafting:** the Maintainer directed that
Phase A be split by coherent decision rather than run as one proposal,
and that the lifecycle be exercised with subagents filling the
structurally-independent review roles — shaping this proposal's scope
and the review mechanism, not its Decision.

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** (i) No shipped onboarding preset equates
  fresh-session review with the External tier — *enforced by*
  `test_onboarding_review_tiers.py`. (ii) The transition-lint flags the
  two named shapes and not the named benign cases — *enforced by*
  `test_transition_lint.py`.
* **Failure modes.** The transition-lint is **fail-open** by design
  (advisory exit code + printed findings); a missed real case degrades
  to today's memory-enforced status quo, and a false positive is a
  printed line a human dismisses — neither blocks work. The preset test
  is **fail-closed** (a reintroduced mislabel turns the suite red).
* **Edge cases.** Transition-lint over: an empty range (no findings);
  a claim-marker-maintenance commit (must not flag); a squash/merge
  commit (documented out of scope for v1); a Decision commit that
  legitimately adds no new section on a rejected-in-place proposal
  (the heuristic must not flag — pinned by a test).
* **Public-path → test mapping.** `transition_lint.main()` →
  `bootstrap/tests/test_transition_lint.py`; the preset invariant →
  `bootstrap/tests/test_onboarding_review_tiers.py`. (Written as real
  relative links in the plan when the files exist.)
* **Known omissions.** v1 transition-lint does not understand rebased
  or squashed history and is advisory only; Part B does not retro-edit
  the immutable archived proposal (that is the open question).

### Tests required

* `bootstrap/tests/test_onboarding_review_tiers.py` (Part A) — the
  mislabel guard.
* `bootstrap/tests/test_transition_lint.py` (Part C) — both flag shapes
  + benign non-flags.
* The existing `python -m pytest bootstrap/tests` suite stays green
  (modulo the pre-existing issue-#1 and the separately-tracked
  clock-expired failures, which this proposal does not touch).

### Examples / smoke checks

* `python scripts/check_cairn.py` stays clean over the edited template
  and the new ledger.
* `python scripts/claim_check.py` clean over this proposal and the plan.
* `python scripts/transition_lint.py <range>` run over this very
  proposal's own commit series as a live dogfood: the open commit must
  not flag (no baked-in review), and the review/response commits must
  each add their section.

## Signals the change is wrong

* The transition-lint fires on benign commits often enough to be noise →
  it nags rather than guards; narrow the heuristics or retire it to a
  manual checklist item.
* The reworded onboarding leaves solo adopters thinking review is
  worthless (over-correction) → restore the "fresh-session review is
  real Internal-tier value" framing while keeping the External-tier
  honesty.
* Review/Maintainer judges the archived-proposal correction belongs
  *in* the archived file after all → the immutability reading was too
  strict; append a marked annotation instead.

## Review -- Claude (Internal, fresh-context subagent panel) -- 2026-07-08

*(Awaiting the Internal review. It will be produced by fresh-context
subagents with no access to the authoring session — the structural
realization of the Internal floor's "same agent, fresh session" — and
appended here as its own commit, attributed transparently to that
mechanism. An External cross-type read remains available before the
Decision if the Maintainer requires the differentiating tier.)*

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer. This is one of the near-automatic Decisions —
the fixes follow directly from the findings — but the accept/reject and
the Part-B home question are the Maintainer's to sign; no agent
self-Decides.)*
