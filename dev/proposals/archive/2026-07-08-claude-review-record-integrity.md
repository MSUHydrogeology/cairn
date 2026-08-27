<!-- Forward-reference paths this proposal plans to create; they materialize in the implementing plan. -->

# Review-record integrity: fix the mislabeled-independence onboarding, record the showcase-arc provenance, and guard lifecycle transitions

**Author**: Claude (Strategy / Implementation)
**Model**: Claude Fable 5
**Date opened**: 2026-07-08
**Status**: accepted
**Touches**: `templates/onboarding/solo-greenfield.md`; a new test under `bootstrap/tests/`; a new advisory check `scripts/transition_lint.py` + its test; the incident record under `dev/measurement/`; a dated provenance note about the archived `2026-06-12-claude-check_cairn-self-host-compat` arc. *(Revised 2026-07-08: Part C — the transition-lint script + its test — is split out to its own follow-up proposal; the retained scope is Part A + Part B. See the Revised proposal below.)*
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

**Model**: Claude Fable 5 (three fresh-context subagents, distinct lenses —
doctrine-conformance, implementation-feasibility, scope-and-prose — each with
no access to the authoring session; findings consolidated, none dropped).

**Attribution / committer note (this itself is finding R6).** These are the
panel's findings, transcribed faithfully. The panel cannot run git, so the
author-session committed this section **as scribe**, disclosing the mechanism
in full rather than signing it as the author's own read. That the author
commits an independent panel's review is exactly the coupling AGENTS.md's
self-commit rule cautions against — surfaced here, not hidden, as R6, for the
Maintainer / External tier to resolve. No finding was softened in transcription.

**Steelman.** The diagnosis is real and verified across all three lenses.
Part A's mislabel is genuine (`solo-greenfield.md:76-77,:99,:113-119` call
fresh-session same-vendor review the "External tier," contradicting
`dual-review.md:46-47`). Part B's provenance claims check against git
(`git show 17b7e5c` = Status "proposed" already carrying both review sections;
`git show f4a8308` = a claim-check-allow marker edit, no review content). The
proposal dogfoods its own thesis — its open commit left the Review section an
empty placeholder rather than baking it in. The instance/record/prevention
triad is a recognized Cairn shape; the advisory posture, the append-only-
respecting ledger default, and the drift-guard test are well-judged; the
proposal names its own wrongness signals honestly.

**Critiques** (descending severity; each grounded in a command/citation the
reviewer ran):

* **[R1] (blocking)** Part B's load-bearing citation misquotes and
  misattributes: `'an archived proposal "is never retro-fitted"'` is presented
  as a `doctrine/lifecycle.md` quote, but the phrase appears nowhere there
  (`grep -c retro-fit doctrine/lifecycle.md` → 0); it lives only in the
  `_template.md` files. The governing rule is `doctrine/proposals.md:136-140`
  ("Archived proposals … the file is **closed**. No edits beyond link
  maintenance") plus append-only at `lifecycle.md:85-88`. A proposal about
  verifiable record cracks carries one on its own turf, and `claim_check`
  can't catch it (doctrine refs are citation-exempt). The *conclusion*
  (default to a ledger; don't annotate the archived file) is correct and in
  fact better-supported by the accurate citation. **Fix:** correct the
  citation (via the append-only Response/Revised, since the proposal is
  committed).
* **[R2] (blocking)** Part C flag-shape (b) ("a proposal-open commit whose
  added file already contains `## Review`") false-positives on essentially
  every **plan-open** commit, because plan-open renames the fully-reviewed
  proposal into `archive/`. Rename detection is not uniform: `git show -M`
  reports R100, but the natural stdlib plumbing
  `git diff-tree --no-commit-id --name-status -r <c>` is rename-blind and
  reports the archived proposal as an **added** file containing `## Review`
  and `## Decision` (verified on `0d24fec`). This is the dominant lifecycle
  commit shape, and the proposal's edge-case list omits it. **Fix:** add the
  rename-to-archive case as a must-not-flag test; require the plan to enumerate
  changes with `-M`/`--find-renames` (reuse the pattern at
  `templates/modules/team-gated/_intent/conflict.py:749-776`).
* **[R3] (substantive)** Flag-shape (a) ("message claims a transition but diff
  adds no section") has a large false-positive surface in Cairn's own log: it
  flags the deliberation-carve-in commits (`AGENTS.md:150-160`: goodnight
  handoff, the one-line `PLANNING.md` row-move) and trips on "open/review/
  Decision" as ordinary English (`18707e9`, `d0ba903`, `ebb1d6e`, `d789474`,
  `0d24fec` all carry the words, touch only `dev/strategy/` or bundle a
  row-move, add no proposal/plan section). The load-bearing narrowing — fire
  only on commits that touch `dev/proposals/` or `dev/plans/` — is unstated.
  Relatedly, "N/A — no doctrine change" is unverifiable while the exception
  vocabulary is deferred to the plan without binding it to the carve-in.
  **Fix:** state the narrowing; name the carve-in as the exemption source of
  truth; bound the vocabulary to restating it; dogfood over ~30 real commits.
* **[R4] (substantive)** Part C (a new tool) is a different risk class and
  effort than the near-automatic A+B, yet is folded in under a "near-automatic"
  Decision framing. Its rules, exception vocabulary, and home are all deferred.
  Its natural home may be a `quality_gate.py --sub transition` sub-gate, not a
  fourth standalone script. This is the proposal's own anti-bundling logic
  (its Alt #3) applied one level down. **Fix:** split Part C into its own
  proposal/plan whose heuristics are pinned against the real commit corpus.
* **[R5] (substantive)** Part B routes two different record types into one
  ledger: the two measurable review-floor deviations *and* a one-time
  provenance narrative. `dev/measurement/README.md:7-20` restricts the folder
  to metrics + feeding ledgers, and `incident-trackers.md:40-42,136-156` makes
  any such tracker a rate-limit-gate substrate `evolution_infer.py` parses
  (≥2 "occurred" rows in a window → suggests a doctrine proposal) — so
  back-filling two same-class deviations could trip the gate, and a narrative
  is not a measurement row at all. Also, defaulting the correction into a
  ledger a skeptic auditing the archived file would never see *undercuts Part
  B's own goal*. Append-only disfavors in-place edits but does not forbid a
  marked, dated erratum-**append**. **Fix:** separate the two records; make "the
  archived file carries a discoverable dated pointer to the correction" a firm
  requirement; reframe the open question as ledger+pointer vs. marked in-file
  erratum-append (both append-only-safe) — largely settleable now.
* **[R6] (substantive)** The subagent-review committer model is unpinned (see
  the attribution note above): a subagent can't commit, so if the author-session
  commits, that is the author committing the review — the coupling
  `AGENTS.md:112-113` forbids. **Fix:** name the committer explicitly and
  reconcile the model (Maintainer commits, or a documented, disclosed
  deviation) — the record must pin this, not leave it implicit.
* **[R7] (substantive)** Part A's proposed "the External tier is explicitly
  unstaffed until a second agent type or a human reviewer exists" is wrong:
  solo-greenfield is "one human Maintainer + one AI agent"
  (`solo-greenfield.md:25-28`), and `dual-review.md:47` names *a human* as a
  full External floor — the Maintainer **already staffs External**. The
  "unstaffed" wording is exactly the over-correction the proposal flags as a
  wrongness signal. It also specifies only what to *remove*, never positively
  affirming that fresh-session review is genuine Internal-tier value. **Fix:**
  reword to "the External floor is filled by the human Maintainer's read (or a
  second agent type); fresh-session agent review is the Internal floor, not
  External," keep the warmth of the strongest source passage
  (`solo-greenfield.md:99-101`), and make postdoc-readability a plan-review
  criterion.
* **[R8] (substantive)** The Part-A guard test as specified (assert no preset
  pairs "External" with "fresh-session"/"same-vendor") would flag Part A's own
  *corrected* text, which must name both tiers in one passage. A co-occurrence
  assertion either red-flags the fix or catches nothing. **Fix:** detect the
  specific false predication (fresh-session review *fills/staffs* External) via
  a curated forbidden-phrase list, and add a positive fixture (the corrected
  text) that must PASS.
* **[R9] (substantive)** Part C's pre-registered verification is speculative,
  not corpus-driven: the "live dogfood" over this proposal's own commits
  exercises only easy paths (the plan-open rename that would stress it is
  excluded), and one enumerated edge case ("a Decision commit that adds no
  section on a rejected-in-place proposal") is premised on a false model — per
  `proposals.md:80-83` a reject/supersede Decision *does* append a `## Decision`
  section. **Fix:** derive edge cases from the real corpus (plan-open rename,
  plan-archive+PLANNING bundle, strategy/goodnight carve-in commits:
  `0d24fec`, `d789474`, `18707e9`); drop the false edge case.
* **[R10] (minor)** "Same family as `quality_gate.py` … not a gate that blocks"
  is imprecise: `quality_gate.py` is fail-closed (`:819`, `return 1 if failed`);
  only its `info` tier is advisory. "Advisory exit code" is self-contradictory
  (nonzero blocks CI). transition_lint would also be Cairn's first check
  reasoning over commit diffs+messages, and the real R6/Theme-3.4 lesson is the
  *suppression infrastructure* (exclusion roots + whitelist + info downgrade),
  unspecified here. **Fix:** recast the analogy to the info tier; pin exact exit
  behavior (advisory = always exit 0); commit to a suppression mechanism.
* **[R11] (minor)** Part B undersells f4a8308: `git show` shows it added only
  claim-check-allow marker tokens — it was claim-marker maintenance *mislabeled*
  as a review-append (and per `lifecycle.md:91-114` such maintenance must land
  in its own labeled commit, which it did not). **Fix:** record the accurate
  mechanism (the Gemini section landed in `17b7e5c`; `f4a8308` was mislabeled
  marker maintenance).
* **[R12] (minor)** Scope-label over-claim: the header says "items A1 + A2," but
  this delivers A2 in full and only the review/transition slice of A1 (the
  v0.3.0 release-notes correction, the adoption-decision note, and the
  zero-rejections explanation are absent), and Part C is a fold-up candidate,
  not an A1/A2 item. A Maintainer tracking Phase A would mark A1 done at ~40%.
  **Fix:** relabel to "A2 in full + the review/transition-independence slice of
  A1 + the transition-lint fold-up."

**Covered.** Doctrine-conformance (`dual-review.md`, `lifecycle.md`,
`proposals.md`, `incident-trackers.md`, `dev/measurement/README.md`, the
`AGENTS.md` carve-in + attribution rules); implementation-feasibility (git
plumbing rename semantics run empirically on `0d24fec`; the shape-(a) FP surface
against the real last-~15-commit corpus; `quality_gate.py` posture and R6
suppression infra; rename-aware fixture pattern at `_intent/conflict.py`);
scope-and-prose (the reworded passages, Part-C precedent, Phase-A scope mapping).
**Not covered / low confidence:** did NOT run transition_lint or its tests (they
don't exist yet — all Part-C findings are static reasoning); did not run the
pytest suite; no real goodnight-handoff commit exists to test FP behavior
against; linear history precluded exercising squash/merge/rebase; **all three
passes are same-agent-type — no cross-type independence on this Internal panel.**

**Second-round recommendation: an External (cross-type) pass is recommended
before the Decision.** Four reasons: (1) the proposal is about the
record-integrity differentiator, so it should clear the differentiating tier it
advocates; (2) the blocking misquote (R1) is a doctrine-recall failure a
same-type reviewer sharing the author's priors may miss and a different agent
type is likelier to catch; (3) Part C as written would ship a check that
false-positives on the dominant lifecycle commit shape (R2) and its home is a
genuine design fork (R4); (4) the subagent-committer model (R6) is novel and
deserves an independent read before it becomes precedent. Sequencing option the
panel flags: accept A+B now (near-automatic once R1 is fixed) and split Part C
into its own evidence-pinned proposal.

## Response -- Claude (author) -- 2026-07-08

**Model**: Claude Fable 5. Proposal-Response grammar (no implementing commit
exists yet). Every critique disposed; none dropped. The review was strong —
it caught a real citation crack (R1) in a proposal about citation cracks, and
proved (R2) that the transition-lint would misfire on the dominant lifecycle
commit shape. Two dispositions are structural: **Part C is split out** (R4),
and the correction-home question is **narrowed** (R5).

* **[R1] accept.** Corrected in the Revised proposal: the governing rule is
  `doctrine/proposals.md:136-140` (archived files are closed, link maintenance
  only) plus append-only at `doctrine/lifecycle.md:85-88`; the "is never
  retro-fitted" phrase is from the `_template.md` files, not `lifecycle.md`,
  and is dropped. (This original Proposal section keeps the misquote — it is
  the append-only record of what was believed at open; the Revised section is
  the correction.)
* **[R2] accept → carried into the split-out Part C proposal.** The finding is
  correct (plan-open renames the reviewed proposal into `archive/`;
  `git diff-tree` is rename-blind). It becomes a pre-registered must-not-flag
  constraint of the Part C follow-up, which will enumerate changes with
  `-M`/`--find-renames`.
* **[R3] accept → Part C proposal.** The narrowing (fire only on commits
  touching `dev/proposals/`|`dev/plans/`, excluding archive moves) and the
  deliberation-carve-in exemption become pre-registered constraints there.
* **[R4] accept.** This proposal narrows to **Part A + Part B**. Part C (the
  transition-lint) becomes its own proposal, whose heuristics are pinned
  against the real commit corpus the review supplied as fixtures (`0d24fec`,
  `d789474`, `18707e9`), and which evaluates a `quality_gate.py --sub transition`
  home versus a standalone script. This applies the proposal's own
  anti-bundling logic one level down — correctly.
* **[R5] accept with modification.** Part B is rewritten (Revised proposal):
  (i) the two review-floor deviations go to a schema-conformant tracker whose
  event class and rate-limit-gate treatment (including whether retroactive rows
  count toward `evolution_infer`'s window) are defined, not back-filled blindly;
  (ii) the one-time provenance narrative is homed as a strategy/plan-record
  note, not a measurement row; (iii) a **discoverable dated pointer on the
  archived file** (link-maintenance only, which `proposals.md:136-140` permits)
  is a firm requirement under any home; (iv) the open question narrows to
  *ledger+pointer vs. marked in-file erratum-append* — both append-only-safe.
* **[R6] accept.** Pinned in the Revised proposal and disclosed in this run's
  Review header: the panel cannot commit, so the author-session scribe-committed
  the review **as a disclosed deviation**. That deviation is itself a candidate
  row for the Part B ledger. The *permanent* model is a Maintainer choice —
  (a) the Maintainer commits subagent-panel reviews, or (b) a sanctioned
  disclosed-scribe mechanism is written into doctrine (a separate, rate-limited
  proposal). Defer the permanent choice to the Decision; this run stays honest
  by full disclosure.
* **[R7] accept.** Revised Part A rewords to: *"the External floor is filled by
  the human Maintainer's read (or a second agent type); fresh-session agent
  review is the Internal floor, not the External tier,"* and positively affirms
  fresh-session review as real Internal-tier value (citing `dual-review.md:51-57`),
  keeping the warmth of `solo-greenfield.md:99-101`. Postdoc-readability becomes
  a plan-review criterion.
* **[R8] accept.** The guard test is re-specified to detect the false
  *predication* (fresh-session/same-vendor review *fills/staffs* External) via a
  curated forbidden-phrase list, with a **positive fixture** (the corrected
  text) that must pass — so the test cannot pass by flagging its own fix.
* **[R9] accept → Part C proposal.** The corpus-driven edge-case set (plan-open
  rename, plan-archive+PLANNING bundle, strategy/goodnight carve-in commits)
  replaces the speculative dogfood; the false "rejected-in-place adds no section"
  edge case is dropped (`proposals.md:80-83`).
* **[R10] accept → Part C proposal.** The info-tier analogy, the exact
  exit-behavior (advisory = always exit 0), and an explicit suppression
  mechanism are pinned there.
* **[R11] accept.** Revised Part B records the accurate mechanism: the Gemini
  section landed in `17b7e5c`; `f4a8308` was claim-marker maintenance mislabeled
  as a review-append (and not in its own labeled commit per `lifecycle.md:91-114`).
* **[R12] accept.** Relabeled (Revised proposal header note): *"A2 in full + the
  review/transition-independence slice of A1; the transition-lint fold-up is
  split to its own proposal."* Phase-A tracking must not mark A1 complete.

**On the second-round recommendation (External before Decision): accept, and
surfaced to the Maintainer.** I cannot produce the External tier myself — it
requires a different agent type (the cross-type reviewer in the project's
workflow), not a fresh Claude subagent (which is Internal). Recommendation to
the Maintainer: route this revised proposal to the cross-type External reviewer
before the Decision, or waive with rationale on the record. R1 is corrected
regardless.

## Revised proposal -- 2026-07-08

**Scope (relabeled per R12):** A2 in full + the review/transition-independence
slice of A1. **Part C (the transition-lint) is split out** to its own follow-up
proposal (per R4), where its heuristics are pinned against real commits. This
proposal is now **two parts**, and its Decision is genuinely near-automatic.

### Part A — fix the mislabeled-independence onboarding (corrected per R7, R8)

* Reword the passages in `templates/onboarding/solo-greenfield.md` (76-77, 99,
  115-119) to: **the External floor is filled by the human Maintainer's read
  (or a second agent type); fresh-session agent review is the Internal floor,
  not the External tier.** The reworded prose must *positively affirm* that
  fresh-session review is genuine Internal-tier value (per the worked example
  at `doctrine/dual-review.md:51-57`), preserving the warmth of the current
  `solo-greenfield.md:99-101` phrasing — not read as bureaucratic subtraction.
  This corrects the earlier draft's wrong "External tier unstaffed until a human
  exists": in a solo Maintainer+agent setup the human **already** staffs
  External (`dual-review.md:47`).
* Add `bootstrap/tests/test_onboarding_review_tiers.py`: assert against a
  **curated forbidden-predication list** (fresh-session / same-vendor review
  *fills / staffs / is* the External tier), **not** bare token co-occurrence,
  and include a **positive fixture** (the corrected passage) that must pass.
* Postdoc-readability of the reworded prose is an explicit **plan-review
  criterion** (the negative-only drift test cannot mechanize it).

### Part B — record the provenance honestly (rewritten per R5, R11)

* **Separate the two record types.** (i) The two 2026-06-12 review-floor
  deviations go to a schema-conformant incident tracker; the plan defines the
  review-floor-deviation event class and its rate-limit-gate treatment —
  explicitly whether retroactively back-filled rows count toward
  `evolution_infer`'s rolling window (default: mark them non-counting /
  historical so a retroactive log cannot trip a doctrine-proposal suggestion).
  (ii) The one-time showcase-arc provenance narrative is homed as a strategy
  note or the plan/commit record — **not** a measurement row
  (`dev/measurement/README.md:7-20` membership rule).
* **Accurate provenance (R11):** record that the Gemini External section landed
  in `17b7e5c` (the open commit, alongside the Internal section, while Status
  read `proposed`), and that `f4a8308` — messaged as appending the Gemini review
  — was in fact claim-marker maintenance, mislabeled and not in its own labeled
  commit (`doctrine/lifecycle.md:91-114`).
* **Discoverable pointer (firm requirement under any home):** the archived
  proposal carries a dated pointer to the correction — **link maintenance only**,
  which `doctrine/proposals.md:136-140` permits on a closed file — so a skeptic
  auditing the archived arc reaches the correction.

### Correct citation (R1)

The rule governing an archived proposal is `doctrine/proposals.md:136-140`
("Archived proposals … the file is **closed**. No edits beyond link
maintenance") plus append-only at `doctrine/lifecycle.md:85-88`. The earlier
draft's `"is never retro-fitted"` attribution to `lifecycle.md` was wrong (the
phrase is in the `_template.md` files) and is withdrawn.

### Narrowed open question (R5, R6)

* **Correction home:** ledger+pointer vs. a marked, dated in-file erratum-append
  — both append-only-safe; the Maintainer's call, but no longer the wide-open
  three-way of the original draft.
* **Subagent-review committer (R6):** does the Maintainer prefer (a) committing
  subagent-panel reviews themselves, or (b) a sanctioned disclosed-scribe
  mechanism (a separate doctrine proposal)? This run used disclosed-scribe as a
  logged deviation.

### Unchanged

Rationale, the "why now," and the instance/record/prevention shape stand
(prevention now lands via the split-out Part C proposal). `Plan review:
required(Internal)` still holds for the retained A+B; the External-before-Decision
recommendation is on the record above.

## Review -- Gemini (External, different-agent-type) -- 2026-07-09

**Model**: Gemini Pro 1.5 / Antigravity
**Verdict**: SHIP (conditional on plan ratification of the specific test/heuristic details)

### Steelman
The revised proposal (Part A + Part B) addresses critical gaps in how the repository represents review independence and historical record accuracy. Specifically, Part A eliminates the false claim in the solo-greenfield preset that same-vendor fresh-session review fulfills the External tier, bringing the templates into alignment with `doctrine/dual-review.md`. Part B retroactively documents the showcase-arc review deviations of 2026-06-12 without altering the closed proposal file itself, maintaining the integrity of the archived log. The separation of the transition-lint tool (Part C) into a follow-up proposal is well-reasoned and prevents high-risk doctrine changes from being bundled with routine template/record updates.

### Critiques

* **[E1] (Advisory) Curved forbidden-predication test logic**
  The drift guard test `test_onboarding_review_tiers.py` checks that "fresh-session / same-vendor review fills / staffs / is the External tier". To ensure this test is robust against minor phrasing changes in the template, it should use a case-insensitive regex pattern or a list of semantic equivalence tokens. It should also verify that when the term "External" is used in relation to reviews, it is explicitly paired with "human Maintainer" or "different agent type".
* **[E2] (Advisory) Prominence of the archived-file pointer**
  The discoverable pointer in the archived proposal `archive/2026-06-12-claude-check_cairn-self-host-compat.md` should be placed at the very top of the file (e.g., as a prominent frontmatter alert or a blockquote directly below the main title). This ensures any reviewer auditing the showcase arc immediately sees the erratum pointer rather than having to scroll through the entire file.
* **[E3] (Substantive) Incident log impact-tagging design**
  The design for back-filling the two 2026-06-12 deviations must explicitly map their `Impact` to a value other than `occurred` (such as `historical` or `non-conflict`). Because `tools/evolution_infer.py` determines the adaptive-doctrine gate trigger purely based on `Impact = occurred` (lines 186-188), using a distinct impact level guarantees that retroactive entries can never inadvertently trigger the rate-limit gate, regardless of how far the rolling window is configured.

### Coverage

* **Covered**:
  * Verification of corrected citations: checked `doctrine/proposals.md:136-140` and `doctrine/lifecycle.md:85-88` for closed file rules; checked `doctrine/dual-review.md:46-47` for review floor tiers. All citations are accurate.
  * Evaluation of Part A's template prose warmth and correctness against `templates/onboarding/solo-greenfield.md`.
  * Analysis of `tools/evolution_infer.py` to verify that retroactive ledger rows do not trip the rate-limit gate.
* **Not covered**:
  * The implementation details of `test_onboarding_review_tiers.py` and the incident tracker schema (which will be defined during execution).
  * The automated committer proposal `2026-07-08-claude-automated-review-committer.md` (read for context only).

## Response -- Claude (author, to External review) -- 2026-07-09

**Model**: Claude Fable 5. Proposal-Response grammar (no implementing commit
yet). The External read returned SHIP and independently re-verified the R1
citation fix — the two-tier loop did its job. All three critiques are plan-level
and accepted; none requires a further proposal revision (Status stays `revised`),
so they are carried as pre-registered constraints of the implementing plan.

* **[E1] accept.** The Part-A guard test (already re-specified per R8 to detect
  the false *predication*, not token co-occurrence) additionally: matches
  case-insensitively / by semantic-equivalent tokens, and asserts the positive
  form — where "External" is used of review it is paired with "human Maintainer"
  or "different agent type." Folded into the plan's test spec.
* **[E2] accept.** The archived-file pointer goes at the **very top** of
  `archive/2026-06-12-claude-check_cairn-self-host-compat.md` — a prominent
  blockquote/alert directly under the title — so an auditor sees the erratum
  before scrolling. This remains "link maintenance" (a pointer, not a content
  edit), consistent with `doctrine/proposals.md:136-140`.
* **[E3] accept — the sharpest refinement.** The two back-filled deviation rows
  are tagged with an `Impact` value **other than `occurred`** (`historical` /
  `non-conflict`), since `tools/evolution_infer.py:186-188` triggers the
  adaptive-doctrine gate purely on `Impact = occurred`. This *guarantees*
  retroactive rows cannot trip the rate-limit gate regardless of window config —
  concretizing the Revised proposal's "define the rate-limit-gate treatment" into
  a specific, verifiable value. Folded into the plan's incident-ledger schema.

Net: External SHIP with three accepted plan-level conditions. The proposal is
ready for the Decision; E1–E3 bind the plan, not the proposal text.

## Decision -- Anthony Kendall (Maintainer) -- 2026-07-09

**Accepted.** Scribed by Claude (Strategy) at the Maintainer's explicit,
unambiguous instruction; commit permission given in the same instruction.

Maintainer's authorization (verbatim):

> Accept `review-record-integrity` as reviewed, scribe, and commit my decision.

The revised **Part A + Part B** are accepted as reviewed. The proposal cleared
both review tiers: a fresh-context Internal panel (12 critiques, 2 blocking)
reshaped it, and the Gemini External read returned SHIP after independently
re-verifying the corrected citations.

**Resolved open questions** (Maintainer's calls, 2026-07-09): correction home =
ledger + a prominent top-of-file pointer on the archived file (link-maintenance
only, per `doctrine/proposals.md:136-140`); Part C (transition-lint) split to its
own follow-up; the R6 subagent-review committer question handled by the separate
`2026-07-08-claude-automated-review-committer` proposal (Decision: superseded),
with this run's disclosed-scribe accepted as adequate.

**Plan conditions, ratified here (bind the plan):** E1 — the guard test detects
the false predication (with the positive-form fixture); E2 — the archived-file
pointer is placed at the very top; E3 — the back-filled deviation rows are tagged
`Impact = historical` (never `occurred`), so they cannot trip
`evolution_infer`'s rate-limit gate. `Plan review: required(Internal)` stands.

**Next (separate commits):** open the plan (which archives this proposal),
execute Part A + Part B, a non-implementing agent runs the code review, then
archive.
