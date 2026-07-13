<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/lifecycle.md doctrine/dual-review.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: review-record integrity (Part A + Part B)

**Source proposal**: `dev/proposals/archive/2026-07-08-claude-review-record-integrity.md`
**Status**: executing
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
| A1 | `templates/onboarding/solo-greenfield.md` | Reword the three passages (task-list item ~74-78; Row 1 ~94-101; Row 3 ~112-119) to the **pinned verbatim text** in the "Pinned replacement text" subsection below. Each reworded passage positively affirms fresh-session review as genuine Internal-tier value — grounded in `doctrine/dual-review.md:12-15`'s Internal-review purpose statement ("helps a change land... catch problems, sharpen the argument, surface what the author missed"), **not** the `:51-57` worked example (that section argues for the *External*/different-agent-type floor's differentiated value, corrected per plan-review R1) — and names its External staffing explicitly ("the human Maintainer's read" / "second agent type") in the same paragraph, satisfying E1's positive-form check. Preserves the warmth of the current `:99-101` phrasing per R7. |
| A2 | bootstrap/tests/test_onboarding_review_tiers.py (new; see Proposed paths) | Two independent guards, scoped per R8/E1's finding that bare co-occurrence false-positives on legitimate text elsewhere (see Author-accounting below): (1) a **curated forbidden-literal-phrase list**, case-insensitive (E1) — covering **both** false-predication wordings live in the pre-edit `solo-greenfield.md` (verified via `grep`, per plan-review R4): "external tier (currently filled by fresh-session same-vendor review)" (lines 76-77 and 115-116, identical, twice) and the word-order-reversed "fresh-session external review tier" (line 99) — scanned across **all** `templates/onboarding/*.md` (universal regression guard, safe because it is literal, not semantic); (2) a **positive-predication check scoped to `solo-greenfield.md`'s three corrected passages** — each paragraph naming "External" in relation to review/tier must also name a staffing token ("human Maintainer" / "different agent type" / "second agent type") in the same paragraph (E1). A synthetic positive fixture (a minimal string naming both tiers correctly) must also pass, independent of the live file, per R8. |

**Pinned replacement text (per plan-review R3).** Verbatim, so implementation and plan-review are checking the same text:

* **Task-list item** (replaces the current `[trigger: second-agent-type; id: spin-up-second-agent]` body):
  > You're at the point where a second agent type would meaningfully
  > strengthen Dual-Review. The External floor is already filled by
  > the human Maintainer's read; a second agent type adds a
  > structurally-independent agent to both tiers and eases how much
  > falls on you alone. Walk
  > `dev/modules/onboarding/agent-team-onboarding.md` for the spin-up
  > checklist.
* **Row 1 — collab-agreement-signing prompt** (replaces the current body, keeps the heading):
  > Fill in your own name + your agent's identifier in the team-roster
  > slot of `dev/collaboration_agreement.md`. No multi-party
  > negotiation needed; you're the team. The roster makes the
  > fresh-session Internal review tier reproducible — real value, not
  > a formality (the second session of your agent reviewing its own
  > prior work catches what the first session missed); the External
  > floor is filled by the human Maintainer's read.
* **Row 3 — second-agent-type spin-up prompt** (replaces the current body, keeps the heading):
  > Your solo deployment has matured to a point where a second agent
  > type would meaningfully strengthen Dual-Review. The External floor
  > is already filled by the human Maintainer's read; a second agent
  > type adds a structurally-independent agent option to both tiers
  > and eases how much falls on you alone. Walk
  > `dev/modules/onboarding/agent-team-onboarding.md` for the spin-up
  > checklist; the second agent's capability tier should match the
  > work Dual-Review carries.

### Chunk B — Part B: record the provenance honestly

| # | File | Change |
|---|------|--------|
| B1 | dev/measurement/review-floor-deviations.md (new; see Proposed paths) | Fork `dev/modules/incident_log_template.md`. Define the `review-floor-deviation` event class (a review, or a stated plan-review requirement, that fell short of its doctrine floor without a waiver recorded at the time). Two dated rows for 2026-06-12: (i) the Internal review of the `check_cairn-self-host-compat` proposal was headed "same-session" (`17b7e5c`), below the fresh-session floor (`doctrine/dual-review.md:46`); (ii) the proposal's stated `Plan review: required(Internal)` was never addressed by the Decision ("Accepted — implement directly (no formal plan)") — no plan opened, no plan-review section landed. Both rows carry **`Impact: historical`** (never `occurred`) per E3 — `tools/evolution_infer.py:186-188` triggers the rate-limit gate purely on `Impact == "occurred"`, so `historical` structurally cannot trip it regardless of window config. `Resolved By: 2026-07-08-claude-review-record-integrity` (this proposal). **Schema note (per plan-review R2):** `historical` is a fourth value beyond the three documented in `dev/modules/incident_log_template.md` / `dev/modules/incident-trackers.md:108-109` (`occurred`/`prevented`/`non-conflict`). Rather than editing the shipped module's canonical enum (that ripples to every future adopter and would be a small doctrine change the proposal's own "Doctrine-change rate-limit" section says N/A applies — out of scope here), this local fork's own "What counts" section documents the extension at the point of use: `historical` = retroactively-logged, dated-before-this-tracker-existed rows that must never count toward the rate-limit gate, verified never counted since `evolution_infer.py`'s gate only counts `Impact == "occurred"`. |
| B2 | `dev/plans/review-record-integrity.md` (this file) | Add a `## Showcase-arc provenance record` section stating the accurate mechanism per R11: the Gemini External review section landed in `17b7e5c` (the open commit, alongside the Internal section, while Status still read `proposed`); `f4a8308` — messaged as "add Gemini External Review" — in fact added only three path tokens to a `claim-check-allow` directive line (claim-marker maintenance, mislabeled, and not in its own labeled commit per `doctrine/lifecycle.md:91-114`; token count corrected per plan-review R6). Verified directly against `git show 17b7e5c` / `git show f4a8308` in this session. |

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
are real. **Accepted residual (per plan-review R8):** between the Chunk B
commit and the eventual plan-archive commit, the archived proposal carries
no pointer at all — not even to the already-real B1 ledger. E2's prominence
ask is best served by a single, closed-file-compliant edit rather than two
touches to a file `doctrine/proposals.md:136-140` closes to everything but
link maintenance; the interim gap is accepted as the cost of that choice,
not overlooked.

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
  fresh-session same-vendor review"), confirmed via `grep -n -i
  "fresh-session\|same-vendor" templates/onboarding/collaborative-team.md`.
  (Corrected per plan-review R5: `high-rigor-legacy.md` was **not** a second
  example of this risk — `grep -n -i "fresh-session\|same-vendor\|vendor"
  templates/onboarding/high-rigor-legacy.md` returns zero matches, so no
  co-occurrence rule could ever fire there; the file's `:111` "External tier"
  mention carries no false-positive risk under this rule at all, only under a
  *different*, stricter rule this plan does not adopt — see the Edge cases
  note below.) This is why A2 splits into a **literal** forbidden-phrase list
  (universal, safe) and a **positive-predication** check (semantic, but
  scoped only to the three passages this plan actually rewrites, where the
  wording is controlled and pre-verified not to false-positive).
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

## Plan review -- Claude (Internal, fresh-context) -- 2026-07-13

**Attribution / committer note.** This is a fresh-context subagent's
independent read of this plan (Internal floor: same agent type, fresh
session). The subagent cannot commit; the author-session commits this
section as a **disclosed scribe** — the same accepted deviation model the
source proposal's own Decision ratified for its Internal panel ("this run's
disclosed-scribe accepted as adequate"). No finding below is softened or
dropped in transcription.

**Model**: Claude Sonnet 5 (fresh-context read of the repo; no access to any authoring session for this plan). Verified every citation below against the actual files/commits, not against the plan's own paraphrase of them.

**Steelman.** The plan correctly scopes itself to Part A + Part B of the *Revised* proposal (not the superseded original), fences Part C out explicitly, and threads all three Gemini conditions (E1–E3) into concrete plan items rather than leaving them as loose commitments. The two-part guard-test design (a universal literal-phrase list + a positive-predication check scoped only to the three rewritten passages) is well-judged and its stated rationale checks out: `grep -n -i "external\|fresh-session\|same-vendor" templates/onboarding/collaborative-team.md` confirms real, correct, pre-existing text at `:79-82` ("the roster is what makes Dual-Review's External tier structurally meaningful; teams without an explicit roster fall back to fresh-session same-vendor review") and `:120-121` ("Without it, External-tier review falls back to fresh-session same-vendor") that a bare co-occurrence rule would indeed false-positive on. The E3 rate-limit claim is exactly right: `tools/evolution_infer.py:187` reads `if inc["impact"] == "occurred" and inc["date"] >= cutoff:` — any non-`"occurred"` string, including `historical`, structurally cannot trip the gate, regardless of window. The B2 provenance mechanism is independently reproducible: `git show 17b7e5c:...check_cairn-self-host-compat.md | grep -n "^## \|Status"` shows `**Status**: proposed` at line 10 while `## Review -- Claude (Internal, same-session)` (line 177) and `## Review -- Gemini (External, different-agent-type)` (line 253) are *already in the tree*; `git show f4a8308` touches only the `claim-check-allow` comment line plus a blank line, no review content. B1's two ledger-row facts also check out against the actual archived file: `**Plan review**: required(Internal)` is present, and the Decision literally reads "**Accepted — implement directly (no formal plan).**" — no plan was ever opened. The plan-review pass caught real, verifiable gaps (below), which is what this tier is for; the underlying design is sound enough to land once these are fixed.

**Critiques** (descending severity; each grounded in a command/citation run this session):

* **[R1] (blocking)** Chunk A1's grounding citation supports the wrong claim. A1 requires each reworded passage to "positively affirm that fresh-session review is genuine Internal-tier value (per the worked example at `doctrine/dual-review.md:51-57`)." I read `doctrine/dual-review.md:1-90` in full and confirmed via `grep -n -i "worked example" doctrine/dual-review.md` that there is exactly **one** "Worked example" section in the file, at line 51, headed "the floor pays its way" — and its entire content is about the **different-agent-type (External) floor**: *"The different-agent-type floor is not a formality; in the reference deployment it repeatedly caught what the same-vendor pass missed, including the blind spots the same-vendor reviewer shared with the author"* (`:53-55`), followed by three External-tier catches and the line *"a rate a same-vendor reviewer... does not match"* (`:76-77`). This passage argues for External's differentiated value **over** same-vendor (which includes fresh-session Internal review) — it is not evidence for, and arguably cuts against, an affirmation of fresh-session/Internal value. The doctrine's actual definition of Internal review's purpose is lines 12-15 ("helps a change land... catch problems, sharpen the argument, surface what the author missed"), never cited. This mis-citation originates in the proposal's R7/Response, survived the Revised proposal, Gemini's E1 pass, and the Decision unchanged, and the plan now carries it forward verbatim as the design spec an implementer will draft prose against — a second citation-accuracy defect in a proposal whose entire subject is citation/record integrity, of the same class as the original R1 misquote. **Fix:** repoint A1's citation to `doctrine/dual-review.md:12-15` (the actual Internal-review purpose statement), or drop the "per the worked example" framing entirely since no dedicated Internal-tier worked example exists in the doctrine.

* **[R2] (substantive)** B1's `Impact: historical` is not a sanctioned enum value. `dev/modules/incident_log_template.md`'s column contract states Impact is "one of three values: `occurred` / `prevented` / `non-conflict`" (closed enumeration, three bullets, no "adopters may extend" language — contrast with the columns note two paragraphs later, which *does* explicitly permit extension: "Adopters may append columns to the right of `Resolved By`"). `dev/modules/incident-trackers.md:108-109` independently confirms the same closed set: *"The migrated entry MUST populate the `Impact` column (`occurred` / `prevented` / `non-conflict`)."* `historical` appears nowhere in either doctrine file. It correctly satisfies E3 (never trips the gate, per R1's verified read of `evolution_infer.py`), but it breaks R5(i)'s explicit requirement that the deviations go into a "**schema-conformant** tracker" — a fourth, undocumented enum value is not schema-conformant, and a future cross-adopter harvest tool built against the documented three-value contract could mishandle it. Note this tension is inherited from the Decision's own ratified wording ("tagged `Impact = historical`"), so the plan can't simply pick a different word unilaterally. **Fix:** in Chunk B1's commit, also add one line to `dev/modules/incident_log_template.md`'s (and/or `incident-trackers.md`'s) Impact documentation formally admitting `historical` as a fourth value ("retroactively logged; never counts, same as `prevented`/`non-conflict`") — low-risk, in-scope since B1 already forks this template — rather than silently deviating from the documented contract.

* **[R3] (substantive)** Chunk A1 gives no verbatim replacement text. The proposal's Response to R7 made "postdoc-readability of the reworded prose... an explicit plan-review criterion" specifically because the negative-only drift test can't mechanize it — implying *this* review pass should be able to assess it. But A1 only paraphrases the target meaning ("the External floor is filled by the human Maintainer's read (or a second agent type); fresh-session agent review is the Internal floor, not the External tier") and applies it uniformly to three passages with materially different surrounding voice and context (a task-list trigger row at `:74-78`, a collab-agreement prompt at `:94-101`, a spin-up prompt at `:112-119`). Without pinned text, this plan-review pass cannot actually exercise the readability/warmth criterion the Response committed to — it necessarily punts to implementation + code review, which is a materially weaker check than "plan review." **Fix:** either pin the exact replacement text for all three passages in this plan (even as a same-turn append before implementation lands), or explicitly note in Scope that the postdoc-readability check is deferred past this review and get that deferral confirmed rather than silently carrying it forward.

* **[R4] (substantive)** Chunk A2 undercounts the wordings its own forbidden-phrase list must cover. `grep -n -i "external\|fresh-session\|same-vendor" templates/onboarding/solo-greenfield.md` shows **two non-identical** false-predication phrasings currently live: "External tier (currently filled by fresh-session same-vendor review)" (lines 76-77 and 115-116, identical wording, twice) and the word-order-reversed "fresh-session External review tier" (line 99). A2 describes "the exact false-predication wording being removed from `solo-greenfield.md`" in the singular. A literal-substring implementation built against only one of these two strings would miss the other's shape — and, notably, would not have caught the line-99 variant had it existed in isolation, which is precisely the drift class this guard exists to prevent. **Fix:** A2 should explicitly enumerate both wordings (or specify a phrase-family, not a single string) so an implementer captures the full lexical variety being removed.

* **[R5] (substantive)** The Author-accounting section's `high-rigor-legacy.md:111` false-positive claim doesn't hold up. It states a bare co-occurrence rule "would also flag `collaborative-team.md:61` and `high-rigor-legacy.md:111`, which correctly discuss the External tier without repeating a staffing token in the same sentence," and claims this was "Confirmed by reading both files in full during plan authoring." I ran `grep -n -i "fresh-session\|same-vendor\|vendor" templates/onboarding/high-rigor-legacy.md` and got **zero matches** — the word "fresh-session" (or "same-vendor"/"vendor" in any form) does not appear anywhere in that file. No co-occurrence rule, at any granularity (sentence, paragraph, or whole-file), could ever flag line 111 there, because there is nothing in the file for "External" to co-occur *with*. (The `collaborative-team.md:61` half of the claim is more defensible under a whole-file interpretation, since that file *does* contain "fresh-session" elsewhere at `:81`/`:120`.) This doesn't change the guard-test's actual design correctness, but it's a verifiable inaccuracy in the plan's own evidence trail — worth catching precisely because this proposal's thesis is that unverified claims corrupt the record. **Fix:** drop the `high-rigor-legacy.md:111` half of the claim, or replace it with a real example (none currently exists in that file — the honest statement is that `high-rigor-legacy.md` carries no false-positive risk under a bare co-occurrence rule at all, only `collaborative-team.md` does).

* **[R6] (minor)** B2 miscounts f4a8308's diff. B2 states f4a8308 "added only two tokens to a claim-check-allow directive line." `git show f4a8308 -- dev/proposals/2026-06-12-claude-check_cairn-self-host-compat.md` shows the diff appends **three** comma-separated path tokens (dev/intents.jsonl.bak, dev/…, dev/proposals/archive/… — illustrative ellipsis tokens quoted verbatim from that commit's diff, not real paths) to the existing `claim-check-allow` line, plus one blank line. The "not in its own labeled commit per `doctrine/lifecycle.md:91-114`" half of the claim is accurate (`doctrine/lifecycle.md:105-106` requires "its own labeled `claim-marker maintenance:` commit," and f4a8308's subject is "add Gemini External Review," not that). **Fix:** correct "two tokens" to "three tokens" before this lands in the plan's committed provenance record — small, but this section exists specifically to be scrupulously accurate about this exact commit.

* **[R7] (minor)** A2 doesn't explicitly commit to case-insensitive matching. E1 asked for "a case-insensitive regex pattern or a list of semantic equivalence tokens." A2's description — "normalized-whitespace substring match" — normalizes whitespace but never states case-insensitivity. E1 is a Decision-ratified binding condition on the plan; the plan should say so explicitly rather than leave it to implementer discretion. **Fix:** add "case-insensitive" to A2's match spec.

* **[R8] (minor, name as residual)** Deferring all of Chunk C to plan-archive time leaves the archived proposal with **zero** discoverable pointer during the interim between the Part A/B commits and the eventual plan-archive commit — not even a pointer to B1 (the review-floor-deviations ledger), whose path is real and stable from the moment Part B lands. E2 asked for prominence specifically "so any reviewer auditing the showcase arc immediately sees the erratum pointer" — during this window, they see nothing. The plan's single-deferred-edit approach is arguably the *correct* call given `doctrine/proposals.md:136-140`'s "closed... no edits beyond link maintenance" (a partial-pointer-now-augmented-later approach risks two edits to a closed file, only the first plausibly defensible as pure link-maintenance), so this isn't a design flaw so much as an unavoidable trade-off — but it should be named as a residual explicitly, not silently absorbed. **Fix:** add one sentence to the Sequencing note acknowledging the interim discoverability gap and that it is accepted as unavoidable under the closed-file constraint.

* **[R9] (informational — the plan's own flagged question)** On the Correction-home judgment call: the plan's reading (deviations → ledger; one-time narrative → this plan document, not `dev/measurement/` or a new `dev/strategy/` note) is **defensible**. It tracks R5(ii)'s explicit "not a measurement row" instruction and `dev/measurement/README.md`'s two-sided membership exclusion ("a file that is neither an aggregate metric nor a measurement-feeding operational ledger does not belong here" — a closed narrative record is neither), and the Decision's "ledger + pointer" phrasing most naturally resolves R5(iv)'s narrowed open question (ledger+pointer vs. in-file erratum-append), not R5(ii)'s separate record-type split. I don't see a clearly *better* home: embedding the narrative as extra prose inside `review-floor-deviations.md` itself would still sit inside a file whose whole charter is measurement rows, in tension with R5(ii)'s same instruction. On durability: `dev/plans/archive/` is git-permanent, so "durable" is satisfied; "auditable" is weaker than a `dev/measurement/`-native home would be, since a future reader auditing process integrity wouldn't instinctively check a plan document — but this is exactly why the plan already flags the question for confirmation rather than asserting it unilaterally, which is the right move. No fix required beyond the Maintainer's explicit confirm/correct, which the plan already solicits.

**Coverage.** Verified directly: all three onboarding presets' line ranges and false-predication/false-positive text via `grep` (solo-greenfield.md, collaborative-team.md, high-rigor-legacy.md — all three read in full); `doctrine/dual-review.md:1-90` read in full (the citation-mismatch finding, R1); `doctrine/proposals.md:110-149` and `doctrine/lifecycle.md:70-114` (closed-file, append-only, and claim-marker-maintenance rules); `dev/modules/incident_log_template.md` and `dev/modules/incident-trackers.md:108-109` (Impact enum, R2) and `dev/measurement/README.md` (membership rule) read/grepped in full; `tools/evolution_infer.py:150-193` read (E3 mechanism, confirmed exactly at `:187`); `git show 17b7e5c` and `git show f4a8308` run directly against the proposal file (tree contents, diff, and commit messages — B2's mechanism claim confirmed, the token-count sub-claim corrected); the archived `check_cairn-self-host-compat` proposal's `Plan review:` line and Decision text read directly (B1's row-ii claim confirmed exactly, including the "(no formal plan)" wording); `python -m pytest bootstrap/tests` run to completion (confirms the plan's named pre-existing failures: `test_ast_attest.py` — 2 sub-failures — and `test_evolution_infer.py::TestGateEval::test_main_suggests_and_json`, 3 failed / 1403 passed / 3 skipped); `python scripts/claim_check.py dev/plans/review-record-integrity.md` run clean. **Not covered / low confidence:** did not run the not-yet-written `test_onboarding_review_tiers.py` (doesn't exist yet — A2 findings are static reasoning against the described design, not executed code); did not draft or evaluate actual replacement prose for A1 (none exists yet, per R3); did not check `doctrine/plans.md`'s archive rules in depth beyond what the plan itself cites; did not run `scripts/check_cairn.py` or `scripts/quality_gate.py --sub neutrality` (plan cites these but they apply post-implementation, not to plan text); this is a single same-agent-type pass — no cross-type independence on this Internal review, consistent with the Internal floor this plan-review requirement calls for.

### Sharpening -- Claude (author) -- 2026-07-13

Every finding disposed, none dropped. All nine accepted; the plan is edited
above (Chunk A1, A2, B1, B2, Author-accounting, Sequencing note) to fold
each fix in directly, so this table is a pointer to where, not a duplicate
of the prose.

* **[R1] accept.** Chunk A1's citation now reads `doctrine/dual-review.md:12-15`
  (the actual Internal-review purpose statement) instead of the `:51-57`
  worked example, with an explicit note on why `:51-57` was wrong (it argues
  External's case, not Internal's).
* **[R2] accept with modification.** Rejected the literal fix (editing the
  shipped `dev/modules/incident_log_template.md` / `incident-trackers.md`
  enum) as out of scope — that ripples to every future adopter and is a
  small doctrine change the proposal's own rate-limit section says N/A
  applies to. Instead: B1's row now carries a "Schema note" committing the
  local fork's own "What counts" section to document `historical` as a
  fourth, locally-scoped value, at the point of use, rather than the shared
  module.
* **[R3] accept.** Chunk A1 now carries a "Pinned replacement text"
  subsection with verbatim text for all three passages (task-list item,
  Row 1, Row 3) — the same text Chunk A1's implementation commit will use.
* **[R4] accept.** A2 now names both wordings explicitly (the
  "currently filled by fresh-session same-vendor review" clause, twice, and
  the reversed "fresh-session External review tier reproducible" at line 99).
* **[R5] accept.** The Author-accounting section's false-positive example is
  corrected: `high-rigor-legacy.md` carries no "fresh-session"/"same-vendor"
  text at all (verified zero matches), so it was never a real false-positive
  risk under this rule; only `collaborative-team.md` is.
* **[R6] accept.** B2 corrected: "two tokens" → "three tokens."
* **[R7] accept.** A2 now states "case-insensitive" explicitly as part of
  the literal-phrase match spec.
* **[R8] accept.** The Sequencing note now names the interim
  discoverability gap explicitly as an accepted residual of the
  closed-file constraint, not an oversight.
* **[R9] noted — no action required.** The reviewer independently confirmed
  the Correction-home reading is defensible and found no clearly better
  alternative; the plan's existing "flagged for confirm/correct" framing
  stands into Maintainer/code-review sight, unchanged.

**Status: awaiting-plan-review → executing.** All findings disposed;
implementation (Chunk A, then Chunk B) begins next.

## Code review

*Filled in after implementation commits land.*

## Lasting-truth migration

*Filled in at archive time.*

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside
the plan.

This section is append-only once written.
