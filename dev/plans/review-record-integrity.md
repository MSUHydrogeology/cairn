<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/lifecycle.md doctrine/dual-review.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: review-record integrity (Part A + Part B)

**Source proposal**: `dev/proposals/archive/2026-07-08-claude-review-record-integrity.md`
**Status**: awaiting-plan-review
**Plan review**: required(Internal) — ratified at Decision; touches a shipped
onboarding template read by every solo-greenfield adopter, and the plan pins
concrete specifics (exact reworded prose, the guard-test heuristic, the
incident-ledger schema, the `Impact=historical` wiring, the pointer placement)
that the proposal left to plan stage.
**Last update**: 2026-07-13
**Opened**: 2026-07-13

## Source proposal

The accepted, revised proposal (Part A + Part B; Part C split to its own
follow-up) fixes a live mislabel in the shipped `solo-greenfield` onboarding
(three passages call fresh-session same-vendor review the "External tier,"
contradicting `doctrine/dual-review.md:46-47`) and records, honestly and
durably, the provenance of the showcase arc's first proposal
(`dev/proposals/archive/2026-06-12-claude-check_cairn-self-host-compat.md`) —
including two review-floor deviations that were never logged as exceptions at
the time. The proposal cleared both review tiers (a 3-reviewer Internal panel,
12 critiques; a Gemini External SHIP with 3 accepted conditions E1-E3) and was
accepted 2026-07-09 with those conditions ratified into the plan.

## Proposed paths

Proposed paths:
- `dev/measurement/review-floor-deviations.md` — the incident ledger (Part B); forked from `dev/modules/incident_log_template.md` in the Part B implementation commit.
- `bootstrap/tests/test_onboarding_review_tiers.py` — the Part A guard test; lands with the Part A implementation commit.

## Scope

Implements the Revised proposal's Part A + Part B in full, plus the three
Gemini-conditions (E1-E3) the Decision ratified as binding on this plan.

**Scope fence (what this does NOT do):** Part C (the transition-lint script)
is explicitly out of scope — split to its own follow-up proposal per the
proposal's R4/R9/R10 dispositions, to be opened separately when its
heuristics are pinned against the real commit corpus. This plan does not
touch scripts/transition_lint.py (not yet created) or any commit-diff
tooling.

### Documentation / doctrine surface

Descriptive/adopter surface (`templates/onboarding/solo-greenfield.md`) +
deliberation/measurement layer (`dev/measurement/`, this plan's own
provenance record). No doctrine change — Part A syncs a template to
already-accepted doctrine (`doctrine/dual-review.md`); Part B is a record,
not a rule. Per the doc-tier home rule, neither routes to `AGENTS.md` or
`doctrine/`.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

**Correction-home judgment call (this plan's own reading of the Decision).**
The Decision resolved the proposal's open question as "correction home =
ledger + a prominent top-of-file pointer." Part B's own Response (R5,
accepted) had already split the *two* record types: the two review-floor
deviations are a schema-conformant incident ledger (`dev/measurement/`
membership is correct for those); the *one-time provenance narrative* is
explicitly **not** a measurement row (`dev/measurement/README.md:7-20`) and
was to be "homed as a strategy note or the plan/commit record." Reading the
Decision's "ledger" as governing the deviations (where a ledger is
unambiguously correct) and R5's "plan/commit record" alternative as governing
the narrative, this plan homes the narrative in **this plan document** (a
`## Showcase-arc provenance record` section below) rather than inventing a new
`dev/strategy/` note that doesn't cleanly fit any of that folder's five
`Type:` kinds (it is neither Stage-0 exploration nor a living reference — it
is a closed, dated record of what already happened). This reading is
flagged explicitly for the plan-review pass to confirm or correct.

## Sequence

```
1. Part A -- onboarding review-tier mislabel fix + guard test   [commit pending]
2. Part B -- incident ledger + provenance record                [commit pending]
3. Archived-file pointer (link-maintenance, done at plan-archive time -- see note) [commit pending]
```

### Chunk A — Part A: fix the mislabeled-independence onboarding

| # | File | Change |
|---|------|--------|
| A1 | `templates/onboarding/solo-greenfield.md` | Reword the three passages (task-list item ~74-78; Row 1 ~94-101; Row 3 ~112-119) to: the External floor is filled by the human Maintainer's read (or a second agent type); fresh-session agent review is the Internal floor, not the External tier. Each reworded passage positively affirms fresh-session review as genuine Internal-tier value (per the worked example at `doctrine/dual-review.md:51-57`) and names its External staffing explicitly ("the human Maintainer's read" / "second agent type") in the same paragraph — satisfying E1's positive-form check. Preserves the warmth of the current `:99-101` phrasing per R7. |
| A2 | bootstrap/tests/test_onboarding_review_tiers.py (new; see Proposed paths) | Two independent guards, scoped per R8/E1's finding that bare co-occurrence false-positives on legitimate text elsewhere (see Author-accounting below): (1) a **curated forbidden-literal-phrase list** — the exact false-predication wording being removed from `solo-greenfield.md` (normalized-whitespace substring match), scanned across **all** `templates/onboarding/*.md` (universal regression guard, safe because it is literal, not semantic); (2) a **positive-predication check scoped to `solo-greenfield.md`'s three corrected passages** — each paragraph naming "External" in relation to review/tier must also name a staffing token ("human Maintainer" / "different agent type" / "second agent type") in the same paragraph (E1). A synthetic positive fixture (a minimal string naming both tiers correctly) must also pass, independent of the live file, per R8. |

### Chunk B — Part B: record the provenance honestly

| # | File | Change |
|---|------|--------|
| B1 | dev/measurement/review-floor-deviations.md (new; see Proposed paths) | Fork `dev/modules/incident_log_template.md`. Define the `review-floor-deviation` event class (a review, or a stated plan-review requirement, that fell short of its doctrine floor without a waiver recorded at the time). Two dated rows for 2026-06-12: (i) the Internal review of the `check_cairn-self-host-compat` proposal was headed "same-session" (`17b7e5c`), below the fresh-session floor (`doctrine/dual-review.md:46`); (ii) the proposal's stated `Plan review: required(Internal)` was never addressed by the Decision ("Accepted — implement directly (no formal plan)") — no plan opened, no plan-review section landed. Both rows carry **`Impact: historical`** (never `occurred`) per E3 — `tools/evolution_infer.py:186-188` triggers the rate-limit gate purely on `Impact == "occurred"`, so `historical` structurally cannot trip it regardless of window config. `Resolved By: 2026-07-08-claude-review-record-integrity` (this proposal). |
| B2 | `dev/plans/review-record-integrity.md` (this file) | Add a `## Showcase-arc provenance record` section stating the accurate mechanism per R11: the Gemini External review section landed in `17b7e5c` (the open commit, alongside the Internal section, while Status still read `proposed`); `f4a8308` — messaged as "add Gemini External Review" — in fact added only two tokens to a `claim-check-allow` directive line (claim-marker maintenance, mislabeled, and not in its own labeled commit per `doctrine/lifecycle.md:91-114`). Verified directly against `git show 17b7e5c` / `git show f4a8308` in this session. |

### Chunk C — archived-file pointer (sequenced last, see note)

| # | File | Change |
|---|------|--------|
| C1 | `dev/proposals/archive/2026-06-12-claude-check_cairn-self-host-compat.md` | A prominent blockquote directly under the title (E2), pointing to both B1 (the ledger) and B2 (this plan's provenance section, once archived). **Link-maintenance only** (`doctrine/proposals.md:136-140`) — no other edit to the closed file. |

**Sequencing note (why C1 is its own late step, not bundled into Chunk B):**
`doctrine/proposals.md:136-140` closes an archived proposal to everything but
link maintenance, and `check_cairn`'s claim-path checker would hard-fail a
citation to this plan's own eventual archive path before this plan has
actually archived there (the file would not yet exist there). C1 is
deferred to the plan-archive commit, when both cited paths (the
review-floor-deviations ledger and this plan's own dev/plans/archive/ path)
are real.

## Acceptance criteria

* **Tests that must pass** — the new `test_onboarding_review_tiers.py` (A2;
  both guards + the positive fixture); the full `python -m pytest
  bootstrap/tests` suite stays green modulo the two pre-existing failures this
  plan does not touch (`test_ast_attest`, the clock-expired
  `test_evolution_infer.py::TestGateEval::test_main_suggests_and_json`).
* **Doc updates that must land** — `templates/onboarding/solo-greenfield.md`
  (A1); the new review-floor-deviations ledger (B1); this plan's
  own `## Showcase-arc provenance record` (B2); the archived proposal's
  top-of-file pointer (C1). All hand-authored Markdown; no generator, no
  snippet-sync surface touched.
* **Examples / smoke checks required** — `python scripts/check_cairn.py`
  clean over the full tree after each commit (including the new ledger and
  the pointer); `python scripts/claim_check.py <changed files>` clean at
  write time; `python tools/lifecycle_planner.py scan` clean over
  `dev/proposals/` + `dev/plans/` after each lifecycle-transition commit
  (structural conformance — the same read-only checker used to validate this
  plan's own transitions).
* Inbound path-link updates: none required (`PLANNING.md` / `NEXT_SESSION.md`
  refer to plans by filename stem, not path link).

### Author-accounting — invariants, failure modes, edge cases

* **Invariant.** No shipped onboarding preset asserts that fresh-session /
  same-vendor review fills or staffs the External tier. *Enforcer:*
  `test_onboarding_review_tiers.py`'s forbidden-phrase guard (A2), run over
  all three `templates/onboarding/*.md` presets.
* **Failure mode avoided (the false-positive risk found while drafting this
  plan, not in the proposal).** A bare "External" + "fresh-session"
  co-occurrence rule — the proposal's original Part A test spec, before R8 —
  false-positives on **existing, correct** text in `collaborative-team.md`
  (`:79-82`, `:120-121`: "the roster is what makes ... External tier
  structurally meaningful ... teams without an explicit roster fall back to
  fresh-session same-vendor review") and would also flag
  `collaborative-team.md:61` and `high-rigor-legacy.md:111`, which correctly
  discuss the External tier without repeating a staffing token in the same
  sentence. Confirmed by reading both files in full during plan authoring.
  This is why A2 splits into a **literal** forbidden-phrase list (universal,
  safe) and a **positive-predication** check (semantic, but scoped only to
  the three passages this plan actually rewrites, where the wording is
  controlled and pre-verified not to false-positive).
* **Edge cases.** `collaborative-team.md:133-140`'s Row 3 ("the second agent
  type fills the External-review tier") is a **true positive** for the
  positive-predication *shape* but is pre-existing, correct doctrine — A2's
  positive-predication check is deliberately not applied to it (out of
  Part A's scope; the literal-phrase guard is the only universal check, and
  this text contains none of the forbidden phrases). The synthetic fixture
  in A2 pins this distinction with an explicit comment.
* **Known omissions.** This plan does not extend the guard test to
  `collaborative-team.md` / `high-rigor-legacy.md`'s wording generally (both
  already correctly staff External); a future edit to either could still
  introduce a *new* mislabel the literal-phrase list wouldn't catch if
  worded differently — an acknowledged residual, not a regression this plan
  introduces.

## Verification

```
python -m pytest bootstrap/tests
python -m pytest bootstrap/tests/test_onboarding_review_tiers.py -v
python scripts/check_cairn.py
python scripts/claim_check.py templates/onboarding/solo-greenfield.md dev/measurement/review-floor-deviations.md dev/plans/review-record-integrity.md
python scripts/quality_gate.py --sub neutrality
python tools/lifecycle_planner.py scan
```

## Plan review

*Filled in below once the fresh-context Internal pass lands.*

## Code review

*Filled in after implementation commits land.*

## Lasting-truth migration

*Filled in at archive time.*

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside
the plan.

This section is append-only once written.
