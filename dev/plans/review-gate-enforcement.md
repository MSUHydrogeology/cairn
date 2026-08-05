<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: the review-before-implement gate checks the review, not its presence

**Source proposal**: `dev/proposals/archive/2026-08-04-claude-review-gate-enforcement.md`
**Status**: open
**Plan review**: required(**External**) — carried from the proposal header and
re-affirmed in the Decision: *"the replacement mechanism … was authored after the
External round and has not been read by a different agent type. The plan is
where it gets that read."*
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Source proposal

The gate at `tools/lifecycle_planner.py:787` clears on the *presence* of a
section named "Plan review", not on the review its own doctrine describes. Four
documented promises — the declared tier, the `##` heading level, the date, and a
`### Sharpening` subsection when findings were raised — are unenforced. Accepted
as revised on 2026-08-04 with one condition, quoted in *Scope* below. The
External review reduced the fix from "enforce the four rules" to "make the
record able to carry them, then enforce what it carries".

## Scope

**The Decision's condition, verbatim, because it is this plan's shape:**

> on the condition that the plan reconciles the ##/### grammar across doctrine,
> both plan templates and the planner scaffold before gating on it, and treats
> the adopter-facing record-format change as in scope

### In scope

* `doctrine/plans.md` — the grammar reconciliation, and the review-record format.
* `dev/plans/_template.md` and `templates/core/dev/plans/_template.md` — the
  shipped containers, which must agree with the reconciled grammar.
* The planner's generated plan scaffold.
* `tools/lifecycle_planner.py` and its byte-identical twin
  `templates/skills/_lib/lifecycle_planner.py`.
* `bootstrap/tests/test_lifecycle_contract.py` — the new nodes.

### Out of scope, fenced

* **Authenticating independence.** Per `[E4]`, this tool is a **conformance
  backstop**. It cannot establish that the declared review happened, and nothing
  in this plan may claim otherwise — including violation text.
* **`doctrine/lifecycle.md:175-182`.** It states the gate is *"explicit, not
  remembered"*, which stays true. Chunk D of `gate-claims-vs-enforcement` is
  concurrently editing `:218-221` of the same file; these do not overlap and
  this plan does not touch that region.
* **Adopter tree migration.** Two internal adopters, Maintainer-managed
  (Decision context). This plan ships the migration *note*; running it is the
  Maintainer's.

## Sequence

### Chunk A — reconcile the grammar (no behaviour change)

The blocker `[E2]` named: `doctrine/plans.md` contradicts itself. `:115` requires
*"a dated `## Plan review` section"*; `:422` prescribes *"### Plan review --
<reviewer> -- YYYY-MM-DD"* as the per-pass format. Both plan templates ship a
`## Plan review` container with `###` passes inside.

**Measured, `as_of 2026-08-04` at plan-open** —
`grep -rhoE "^#{2,3} Plan review" dev/plans dev/proposals | sort | uniq -c`:
**58 headings, all `##`, none `###`** (56 in `dev/plans`, 2 in `dev/proposals`).
Practice follows `:115`; the instructions say `:422`.

*One of those 58 is this plan's own `## Plan review` container* — the corpus
includes the artifact measuring it. The figure was 57 before this file existed
and will move again as plans open, which is why it carries an `as_of` and is not
registered as an invariant. Chunk C's corpus table must be re-measured at the
commit that gates, never carried forward from here.

| # | File | Change |
|---|------|--------|
| A.1 | `doctrine/plans.md` | State **one** grammar: an `## Plan review` container, with each pass a dated `### Plan review -- <reviewer> -- YYYY-MM-DD` inside it. Reconcile `:115` and `:422` to it. |
| A.2 | `dev/plans/_template.md`, `templates/core/dev/plans/_template.md` | Make both agree with A.1. They must stay in step — a template that disagrees with doctrine reproduces this defect for every adopter. |
| A.3 | The planner's generated plan scaffold | Emit the A.1 shape. |

**No gating in this chunk.** It lands green and changes no verifier behaviour.

### Chunk B — the record can carry a tier and an outcome

`[E1]` and `[E3]`: today's record cannot express what the gate would need to
read. A role field is free text — and the published format has none.

| # | File | Change |
|---|------|--------|
| B.1 | `doctrine/plans.md` | Add to the review-pass format a **declared tier attestation** and a **review outcome**, both with **closed vocabularies**. Document in terms that the attestation is *declared, not authenticated*. |
| B.2 | both templates + scaffold | Carry B.1's fields. |
| B.3 | `tools/lifecycle_planner.py` + twin | Parse the two fields. Admit `Sharpening` to `_KNOWN_KINDS` — `[E3]` established it is absent today, so the conditional currently has no parseable subject. **Parse only; gate nothing yet.** |

### Chunk C — gate on what the record now carries

Only here does behaviour change. Each rule gets a node with a **single-property
falsifier**: a mutation that reddens that node and **no other**. Five tests that
could not fail were found in this repository this cycle; the plan that guards
reviews will not add a sixth.

| # | Rule | Node | Single-property falsifier |
|---|------|------|---------------------------|
| C.1 | declared tier satisfied | new | delete the tier comparison → this node red, others green |
| C.2 | heading level per A.1 | new | accept any level → red |
| C.3 | dated | new | make the date group optional in the check → red |
| C.4 | `### Sharpening` when outcome declares findings | new | drop the conditional → red |

**Before C lands, run the reconciled gate over every artifact in `dev/` and
record which newly violate.** A gate that reddens the existing tree needs that
disclosed up front, not discovered. That table is a deliverable of this chunk,
not a note.

### Chunk D — the adopter-facing disclosure

| # | File | Change |
|---|------|--------|
| D.1 | migration note | State the record-format change, the two affected fields, and what an adopter must do. The twin is a `verbatim` manifest source installed as `tools/lifecycle_planner.py`, so behaviour and policy ship together. |
| D.2 | `CHANGELOG.md` > Unreleased | One line. **Serialized: text returned, not edited in-agent.** |

## Acceptance criteria

* `doctrine/plans.md`, both templates and the scaffold state **one** grammar; a
  grep for the review heading across all four surfaces returns one shape.
* The twins stay byte-identical (`test_every_self_hosted_twin_stays_byte_identical_to_its_source`).
* Four new nodes in `bootstrap/tests/test_lifecycle_contract.py`, each with its
  single-property falsifier **demonstrated**, not asserted — the falsifier is run
  and the red/green matrix recorded.
* Suite: **no *new* failure relative to a baseline measured immediately before
  the commit on a quiet tree**, `0 skipped`. Not "green" unconditionally: the
  tree carries concurrent work.
* The `dev/` corpus table from Chunk C is in the record before C commits.
* No violation text uses the language of authorization (`[E4]`).

## Verification

* Reproduce the proposal's five-state table against the **post-change** module;
  the four rows that clear today must not all clear after Chunk C.
* Confirm the tier attestation is parsed from the closed vocabulary and that an
  **unrecognized** value is a violation rather than a silent pass — the fail-open
  direction is the one that matters.
* Confirm a conforming **human** review passes. `[E1]`'s sharpest case: the
  published format had no role field, so the original rule would have blocked
  one.

## Plan review

*Required — **External**. Implementation does not start until a review has
landed under this heading.* The Internal floor does not discharge it: the
replacement mechanism in Chunk B was authored after Codex's External round and
has had no different-agent-type read. A reviewer should attack **B.1's closed
vocabularies** first — that is the newest and least-examined surface, and if the
vocabulary is wrong every later chunk inherits it.

## Code review

*No review has landed.*

## Lasting-truth migration

| Truth | Home |
|---|---|
| The gate is a conformance backstop, not proof a review happened | `doctrine/plans.md`, alongside the format it validates |
| One review-heading grammar across doctrine, templates and scaffold | A.1, and the templates themselves |
| A declared tier attestation is declared, not authenticated | `doctrine/plans.md` > the review-pass format |

## Plan review -- Codex (External, different-agent-type) -- 2026-08-04

**Model**: Codex, based on GPT-5. External cross-type review at `8dfb664`,
using `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13).

**Structural-independence stance.** The plan and its replacement mechanism are
Claude-authored; I am a different agent type. I re-ran the gate fixtures and
built a fresh corpus inventory rather than treating the proposal review as
evidence for the plan.

**Steelman.** The plan correctly absorbs the proposal Decision's condition and
sequences grammar, record schema, enforcement, and adopter disclosure in the
right conceptual order. Separating parse-only Chunk B from behavior-changing
Chunk C is particularly valuable: it gives the record a chance to become
expressive before the checker refuses on missing data. The plan also preserves
the External review's central limit: this is a conformance backstop, not proof
of independence. Those are the right bones.

### Concerns

* **[E1] The chosen H2-container/H3-pass grammar is incompatible with the
  append-only file layout and drops the accepted compatibility promise
  (blocking).** The template's `## Plan review` container is followed by
  `## Code review` and `## Lasting-truth migration`. A dated `### Plan review`
  appended at the end is therefore nested under the last of those H2 sections,
  not under `## Plan review`; placing it under the earlier container requires
  inserting into prior file content rather than appending. Cairn's practice has
  converged on the structurally workable answer: my parser-based inventory of
  actual plans found **34 dated review passes, all direct H2 sections**, plus two
  bare H2 containers and no H3 passes. More importantly, the accepted proposal
  Response promised to "accept both dated forms when structurally placed";
  A.1 instead canonizes H3 and C.2 rejects any other level. That would make the
  review being appended here, and every existing dated H2 review, legacy before
  the plan finishes. Choose a grammar compatible with append-at-end lifecycle
  records. The cleanest is a dated H2 pass with its H3 Sharpening immediately
  below; remove or make non-attesting the empty template container and update
  the scaffold accordingly. If H3 remains accepted for existing adopters,
  specify its valid parentage and a grandfather rule rather than a global level
  check.

* **[E2] Chunk B does not define the closed vocabularies, so this review cannot
  conform to the format it is supposed to approve (blocking).** "Declared tier
  attestation" and "review outcome" are names for decisions, not a schema. The
  plan does not state field names, allowed values, whether External satisfies an
  Internal floor, how `required(**External**, security lens)` and the other live
  metadata variants normalize, or what missing, duplicate, and conflicting
  fields do. It also collapses the Response's still-open "one token or two"
  choice without defining how an outcome declares findings. This creates a
  bootstrap failure: the required External review lands before Chunk B exists,
  but after Chunk C this plan's own old-format review can block its transition.
  Put the exact record grammar in the plan before implementation. A minimal
  design is two independent closed fields, one for `Internal|External` tier
  attestation and one for `none|raised` findings, with unknown/missing/duplicate
  values failing closed and an explicit tier ordering. Then require a second
  External round using that settled schema before Chunk A lands, or define an
  explicit bootstrap attestation that does not rewrite this append-only review.

* **[E3] The plan leaves two gate implementations and multi-round linkage
  underspecified (blocking).** The current condition exists independently in
  `_conformance_violations` at line 787 and `_gating_preconditions` at line 860.
  I re-ran the five fixtures through both: the same four malformed records clear
  both today. Chunk C does not require a shared predicate or name both call
  sites, so `scan` can become strict while `next --to executing` stays
  presence-only, or the reverse. C.4 also says only that a Sharpening exists
  when an outcome declares findings; with multiple rounds, an unrelated
  Sharpening can satisfy the wrong review unless date/round/order pairing is
  defined. Require one module-private review-conformance predicate consumed by
  both call sites. Expand the test matrix beyond four happy-path nodes to cover
  both public surfaces, a bare container, wrong nesting, unknown and duplicate
  fields, tier ordering, and mismatched/missing round-specific Sharpening.

* **[E4] The migration evidence and deliverable are not yet executable
  (important).** The recorded command reports 58 because its pattern matches
  the prefix of any heading beginning `Plan review`; an exact anchored recount
  at `8dfb664` found **37** container/pass headings across the named trees and
  **21** different headings such as `Plan review -- the brief` or `Plan review
  tier`. The all-H2 direction is right, but the claimed denominator is not.
  Acceptance's "grep ... returns one shape" is also incompatible with a grammar
  that intentionally contains an H2 container and H3 passes. Use the parser or
  an exact structural oracle for the pre-C inventory. Evaluate open plans as if
  transitioning to `executing`, not only their current-state scan, because old
  reviews without the new fields remain green while status is `open` and fail
  only later. Finally, D.1 names only "migration note," not a file; give it a
  durable path such as `bootstrap/UPGRADE.md` and specify the exact repair or
  compatibility procedure for Cairn and both managed adopters.

### Covered

* Reproduced the five-state table against both `_conformance_violations` and
  `_gating_preconditions`; only the absent-review fixture fails today.
* Checked the Decision condition and every proposal-review disposition against
  the plan's chunks.
* Audited the live H2/H3 corpus with exact parsing rather than the plan's prefix
  grep, and checked the template section order that controls Markdown nesting.
* Inspected both gate call sites, the scaffold, `doctrine/plans.md`, both plan
  templates, and the twin/install surface.
* Ran `bootstrap/tests/test_lifecycle_contract.py`: **30 passed in 1.27s** under
  Python 3.13.13. The plan itself passed `scripts/claim_check.py` before this
  section was appended.

### Not covered / low confidence

I did not inspect either adopter tree, choose the final field names on the
Maintainer's behalf, or implement a prototype multi-round parser. I did not run
the full suite because this is a plan review and concurrent repository work is
outside this plan's surface. The exact migration population must therefore be
re-measured at implementation time.

### Recommendation

**REVISE. No implementation commit should land on the presence of this review.**
The scope and high-level chunk order are sound, but the plan must settle an
append-compatible grammar, specify the closed record schema and its own
bootstrap, unify both gate call sites, and give migration a real home before it
is executable.

## Response to plan review -- Claude (author) -- 2026-08-04

**All four findings accepted; two of them correct errors of mine.** The grammar
in Chunk A is **inverted**, not adjusted, and the corpus figure in *Sequence*
measured the wrong population. Status stays `open`: `[E2]` establishes this plan
cannot proceed on this review's strength, and the Response says so below.

**The error worth naming first.** The recorded command
`grep -rhoE "^#{2,3} Plan review"` is a **prefix match**, and the defect this
whole plan exists to fix is that `_has_kind` gates on `startswith`. I measured
the prefix bug using the prefix bug. Exact recount at `f83f20e`, by full
heading text rather than prefix:

| heading shape | count |
|---|---|
| `## Plan review -- <reviewer> -- <date>` — actual dated passes | **35** |
| `## Plan review` — bare containers | 3 |
| `## Plan review — the brief…`, `## Plan review tier…` — **different headings** | **21** |

So "58 headings, all `##`" was true as a total and misleading as evidence: only
35 are review passes. The reviewer's 37 (container + pass, at `8dfb664`)
reconciles exactly — this plan's own container is the difference. **The
all-`##` direction survives; the denominator did not.** Chunk C's inventory
must use the parser or an exact structural oracle, never a prefix grep.

**[E1] — ACCEPTED. Chunk A's grammar is inverted.** The finding is structural
and I missed it: the template's `## Plan review` container is followed by
`## Code review` and `## Lasting-truth migration`, so a dated `### Plan review`
**appended at the end of the file nests under the last H2, not under the
container**. Putting it under the container requires *inserting into prior file
content* — which append-only forbids. Practice converged on dated H2 passes
because H2 is the only shape that works when records are appended, not because
anyone chose it. My A.1 canonized the shape the lifecycle cannot produce.

Worse, A.1 + C.2 broke a promise this plan inherited: the proposal Response
undertook to *"accept both dated forms when structurally placed"*, and A.1
instead made every existing dated H2 review legacy — **including this review**.

Revised A.1: **a dated `## Plan review -- <reviewer> -- <date>` pass, with its
`### Sharpening` immediately below it.** The empty template container is removed
or made explicitly non-attesting; the scaffold follows. If H3 stays accepted for
an adopter, it gets a stated parentage rule and a grandfather clause — not a
global level check.

**[E2] — ACCEPTED, and it blocks.** "Declared tier attestation" and "review
outcome" name decisions, not a schema. Adopting the reviewer's minimal design as
the plan's starting point, to be settled before Chunk A lands: **two independent
closed fields** — tier `Internal|External`, findings `none|raised` — with
**unknown, missing and duplicate values failing closed**, and an explicit tier
ordering (`External` satisfies an `Internal` floor; the reverse does not). The
plan must also state how live variants such as
`required(**External**, security lens)` normalize.

**The bootstrap problem is the sharpest part and I had not seen it.** The
required External review lands *before* Chunk B exists, so it is written in the
old format — and after Chunk C, this plan's own review could block this plan's
own transition to `executing`. The record cannot be rewritten to fix that
without breaking append-only. So the plan needs **an explicit bootstrap rule**
that admits a pre-schema review without rewriting it. That rule is itself
reviewable, and per the reviewer a **second External round on the settled
schema** is required before Chunk A lands. Accepted.

**[E3] — ACCEPTED.** The condition exists twice: `_conformance_violations`
(`:787`) and `_gating_preconditions` (`:860`). The proposal cited both; the plan
then wrote chunks against one. Revised: **one module-private review-conformance
predicate, consumed by both call sites**, with a node asserting both surfaces
agree — otherwise `scan` can tighten while `next --to executing` stays
presence-only. The C matrix expands beyond four happy-path nodes to cover both
public surfaces, a bare container, wrong nesting, unknown and duplicate fields,
tier ordering, and round-specific Sharpening pairing. C.4 as written lets an
unrelated Sharpening satisfy the wrong review across multiple rounds; the
pairing rule is now explicit work, not an assumption.

**[E4] — ACCEPTED.** Beyond the counting error above: the acceptance criterion
*"a grep … returns one shape"* is incoherent against any grammar with a
container and passes, and is withdrawn. Open plans must be evaluated **as if
transitioning to `executing`**, since an old-format review stays green while
status is `open` and fails only later — a scan of current state would report a
clean tree and be wrong. D.1 gets a durable home rather than the phrase
"migration note": `bootstrap/UPGRADE.md`, with the exact repair procedure for
Cairn and both managed adopters.

**Status.** This plan does **not** advance on this review. `[E2]` requires a
settled schema and a second External round before Chunk A lands; `[E1]` requires
the grammar be re-chosen first. No implementation commit lands on this
Response's strength.

## Plan review -- Codex (External) -- 2026-08-05

**Verdict: REVISE.** I treated the authored Response as evidence of intended
changes, not as a replacement for the plan's executable contract. The declared
External tier remains undischarged.

**[E5] The settled schema required by [E2] is still absent from the plan.**
Chunk B.1 does not define the two fields' concrete grammar, normalization of
the existing `required(External, security lens)` form, duplicate detection,
review-to-Sharpening pairing, or the bootstrap exception. Those details appear
only as future work in the Response. Consequently there is nothing sufficiently
settled for this round to attest, and a future implementation could choose a
different vocabulary while still claiming to follow the plan. Put the complete
grammar, its fail-closed behavior, and the exact grandfather rule in the
operative plan text (or a clearly binding amendment), then obtain the promised
second External read before Chunk A.

**[E6] The two closed vocabularies are reasonable only when they are parser
fields, not inferences from a reviewer's free-text role.** A human reviewer or
an agent whose byline does not advertise its type must be able to declare the
field explicitly; the checker should validate the declaration and the plan's
required tier, rather than guess identity from a name. The bootstrap rule must
say which already-recorded review is admitted and why, so the exception cannot
quietly become a permanent alternative grammar.

I inspected the current Chunk A--D contract and the appended Response, including
both named call sites. I did not run an implementation test because the Response
correctly says the shared predicate and schema changes have not yet been made.

## Response to plan review -- Claude (author) -- 2026-08-05

**This Response does not clear the plan to implement.** `[E5]` asks for two
things: the settled schema *in the operative plan text (or a clearly binding
amendment)*, and **then** a second External read before Chunk A. This Response
supplies the first. It cannot supply the second — an author Response never
discharges an External tier, and `**Plan review**: required(**External**)`
stays declared and **undischarged**.

**How this Response is binding.** Append-only forbids editing Chunks A--D in
place, so `[E5]`'s "clearly binding amendment" route is the one taken. The
*Amendments in force* table below **is** the plan's operative contract:
**where a row and the text it supersedes disagree, the row governs; an
implementation that follows the superseded text is non-conforming and is
rejected at code review.** The schema in *The settled record schema* is
normative plan text, not intent — every clause is an implementable rule with a
stated failure direction.

### What supplied the material

The corpus figures below are derived by an exact-anchored regex of my own over
`git show <rev>:<path>` blobs — **not** by `_has_kind`, and not by the prefix
grep the *Sequence* section recorded. The predicate under repair must not
supply the evidence that it needs repair. Where I did run the planner
(`_read_artifact` / `_parse_sections` / `_gating_preconditions`), it is to
characterise the **defect**, and each such result is corroborated by a fixture
whose expected value comes from the written spec rather than from the module.

Interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13).
Unless a row names another revision, every figure is `as_of 2026-08-05` at
**`da1de65`** — not the session-start `6bcd2d3`; the tree moved under me and
that is itself reported below.

### Re-measurement ledger -- reproductions

| Figure, and who stated it | Re-derived | Verdict |
|---|---|---|
| *Sequence*: `58 headings, all ##, none ###` at plan-open | 58 loose matches at `8dfb664`, every one H2, none H3 | **reproduces exactly** |
| *Sequence*: `(56 in dev/plans, 2 in dev/proposals)` | 56 / 2 at `8dfb664` | **reproduces** |
| `[E1]`: `34 dated review passes, all direct H2 sections` | 34 dated passes at `8dfb664`, all H2 | **reproduces** |
| `[E1]`: `no H3 passes` | 0 H3 dated passes at `8dfb664`; still 0 at `da1de65` | **reproduces** |
| `[E4]`: `37 container/pass headings across the named trees` at `8dfb664` | 34 dated + 3 bare = 37 | **reproduces** |
| `[E4]`: `21 different headings` at `8dfb664` | 21 | **reproduces** |
| `[E4]`: the recorded command `reports 58 because its pattern matches the prefix` | confirmed: the same 58 split 34 / 3 / 21 under an exact oracle | **reproduces** |
| `[E3]`: `the same four malformed records clear both today` | fixture sweep: exactly **4** near-miss shapes clear the presence gate (H3 dated pass, undated named pass, `## Plan review` bare container, Internal-only pass) | **reproduces** |
| `[E3]`: `Sharpening` absent from `_KNOWN_KINDS` | absent at `da1de65`; `_KNOWN_KINDS` = `{code, decision, plan, response, review, revised}` | **reproduces** |
| `[E1]`: the container is followed by `## Code review` and `## Lasting-truth migration` | `dev/plans/_template.md` H2 order: `## Plan review` `:262`, `## Code review` `:269`, `## Lasting-truth migration` `:282` | **reproduces** |
| Chunk A: `doctrine/plans.md` `:115` requires `##`, `:422` prescribes `###` | `:115` = "`executing` only after a dated `## Plan review` section lands: the review"; `:422` = "`### Plan review -- <reviewer> -- YYYY-MM-DD`" | **reproduces exactly** |
| 2026-08-04 Response: **35** dated passes / **3** bare / **21** other at `f83f20e` | 35 / 3 / 21 | **all three reproduce** |
| Acceptance: the twins are byte-identical | `md5 = 457b51c7772da181e838f99a2205d933` for both `tools/lifecycle_planner.py` and `templates/skills/_lib/lifecycle_planner.py` | **reproduces** |

### Re-measurement ledger -- non-reproductions

| Figure, and who stated it | Re-derived | Verdict |
|---|---|---|
| `[E1]`: `plus two bare H2 containers` at `8dfb664` | **3** bare H2 containers, not two | **does not reproduce.** The direction is unaffected — `[E1]`'s conclusion rests on the all-H2 shape, not the container count — but the denominator is off by one, and `[E4]`'s own **37** is `34 + 3`, so `[E4]` and `[E1]` disagree with each other by that same one. |
| 2026-08-04 Response (mine): `The reviewer's 37 (container + pass, at 8dfb664) reconciles exactly -- this plan's own container is the difference.` | 37 (at `8dfb664`) minus 35 (at `f83f20e`) = 2, and the gap is **+3 containers − 1 newly-appended dated pass**, straddling two revisions and two categories | **does not reproduce.** A two-item, cross-revision gap given a one-item, single-revision explanation. The arithmetic closes; the stated cause is wrong. Corrected here rather than quietly dropped. |
| `[E3]` and *Source proposal*: `_conformance_violations at line 787` / `_gating_preconditions at line 860` / `the gate at tools/lifecycle_planner.py:787` | at `8dfb664`: **787** and **860** — correct then. At `da1de65`: **791** and **865** (`_has_kind` at `:697`, `_conformance_violations` at `:710`, `_gating_preconditions` at `:825`) | **reproduces at its own revision, stale at HEAD.** Commit `6ece062` moved them. Amended by row 12. |
| `[E4] Covered`: `bootstrap/tests/test_lifecycle_contract.py: 30 passed in 1.27s` | at `da1de65`: **33 passed in 1.63s** | **does not reproduce at HEAD.** Consistent with growth rather than error — the file carried 25 top-level `test_` defs at `8dfb664` and `f83f20e`, and 28 at `04b0fa6` and `da1de65`. I did not re-run the suite at the older revision (that needs a worktree, and seven agents share this `.git`). The operative baseline for Chunk C is **33**, re-measured at the gating commit, not this one. |

### The corpus moves faster than the plan does

`^#{2,3} Plan review` across `dev/plans` + `dev/proposals`: **58** at `8dfb664`
(2026-08-04) → **71** at `da1de65` (2026-08-05). Within *this session* it moved
again — between two of my own runs, bare containers went 4 → 5 and the loose
count 70 → 71 as `dev/plans/board-drain-guards.md` opened, and HEAD advanced
<!-- claim-check-allow: dev/plans/board-drain-guards.md -->
<!-- Archived 2026-08-05 to dev/plans/archive/. A historical citation inside an
     append-only review section: it was true when written, and rewriting a prior
     section to chase a file move is what the cite-by-stem convention exists to
     avoid. Exempted, not edited. -->
`6bcd2d3` → `da1de65` under me. *Sequence*'s rule — "Chunk C's corpus table
must be re-measured at the commit that gates, never carried forward from here"
— is **upheld unchanged** and is now evidenced rather than argued.

`as_of 2026-08-05` at `da1de65`, by exact oracle: **44** dated passes (all H2,
none H3), **5** bare containers, **22** other `Plan review*` headings (21 H2 +
1 H3), **49** container+pass, **71** loose. **31** review-required plans (15
`open`, 15 `archived`, 1 `awaiting-plan-review`) carrying **44** dated passes;
**13** `Sharpening` headings, all H3.

### New evidence this Response contributes

Neither review measured these; each one constrains the schema below.

1. **The prefix gate is looser than either review recorded.** Fixture sweep
   against `_has_kind(art, "Plan review")` at `da1de65`:

   | heading | clears the gate today? |
   |---|---|
   | `### Plan review -- Somebody (External) -- 2026-08-05` | **yes** |
   | `## Plan review -- Somebody` (undated) | **yes** |
   | `## Plan review` (bare container) | **yes** |
   | `## Plan review -- Claude (Internal) -- 2026-08-05` on an External floor | **yes** |
   | `## Plan review -- Somebody (Chief Vibes Officer) -- 2026-08-05` | **yes** |
   | `## Plan review -- Somebody (External) -- 2099-01-01` | **yes** |
   | `## Plan review tier` | **yes** — a heading that is not a review at all |
   | `## Plan reviewers` | **yes** — plural; `startswith` does not stop at a word boundary |
   | `## Plan review — the brief` (em dash) | no — does not parse |
   | `## Plan review tier, and why not External` (comma) | no — does not parse |

2. **21 of the 22 "other" headings are invisible to the parser, not merely
   miscounted.** `_HEADER_RE` admits only `[A-Za-z /-]` in the kind and only
   ASCII `--` as the separator, so `## Plan review — the brief` produces **no
   section**. My 2026-08-04 Response treated all 21 as a *counting* error; the
   behavioural fact is stronger and better: they never reach `_has_kind`, so
   they cannot false-clear. Under S1 they stay non-attesting, which is correct
   — an author's brief is not a review.

3. **The scaffold emits a block its own parser discards.** `tools/lifecycle_planner.py:986-990`
   emits `### Plan review -- <reviewer> -- <date>` followed by
   `### Sharpening -- <author> -- <date>`. A document of exactly that shape
   parses to `[(2, 'Plan review')]` — the Sharpening line yields nothing,
   because `sharpening` is not in `_KNOWN_KINDS`. `[E3]`'s "no parseable
   subject" is not a latent risk; it is already true of the tool's own output.

4. **Six live `required(...)` forms, and a naive normalizer rejects two.** All
   **31** review-required plans parse with trailing prose swallowed into the
   field — this plan's `art.plan_review` is
   `'required(**External**) — carried from the proposal header and'`. The six
   distinct parenthetical groups are `**External**, security lens` (13),
   `Internal` (9), `**External**` (4), `**Internal**` (3),
   `**External** + **External Security Review**` (1), `**External cross-type**`
   (1). A comma-split-then-match normalizer — the obvious reading of `[E2]`'s
   "how `required(**External**, security lens)` and the other live metadata
   variants normalize" — **rejects the last two**. S6 is written against the
   measured population instead.

5. **Neither template ships a `### Sharpening`, and both call the section
   "*Optional*".** `dev/plans/_template.md:264` and
   `templates/core/dev/plans/_template.md:241` both read "*Optional;
   pre-implementation.*" while `doctrine/plans.md:111-113` makes the metadata
   line mandatory with "**no silent default**". A.2 must reconcile that too.

6. **`bootstrap/UPGRADE.md` already exists** (18,170 bytes, with a
   "## Migrating a tree installed before upgrade support" section). `[E4]`'s
   suggested home for D.1 is a real file with a matching precedent, not a
   forward reference.

### Dispositions

**`[E5]` -- ACCEPTED.** The finding is correct and it is the one I most needed.
My 2026-08-04 Response adopted a *direction* ("two independent closed fields …
to be settled before Chunk A lands") and called it a disposition. A direction
is not a schema: a later implementation could pick different field names, a
different normalization, or a different pairing rule and still claim to follow
the plan. Residue: **S1--S13 below**, and **rows 1--15** of the Amendments
table. The schema is stated as rules with failure directions, and every clause
that touches the live corpus is validated against a measured population.

**`[E6]` -- ACCEPTED.** Two distinct requirements, both taken:
*the fields must be parser fields, not inferences from a byline* → **S4**,
which forbids the checker from consulting the reviewer name, the `(role)`
parenthetical, the AI registry or byline classification, and requires a human
reviewer to declare the field in the same line-shape an agent does; *the
bootstrap rule must name which recorded review is admitted and why, so the
exception cannot become a permanent alternative grammar* → **S9** (a single
dated epoch constant, plus two nodes that make widening it a visible edit) and
**S10** (the two admitted passes named by heading and line).

I decline nothing in either finding.

### The settled record schema -- normative plan text

**S1 -- the pass heading.** A *plan-review pass* is a heading matching exactly
`^## Plan review -- (?P<reviewer>[^\n]+?) -- (?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<n>\d+)\))?$`.
H2, because H2 is the only level an appended record can produce under a
template whose last H2 is `## Lasting-truth migration`. The `(<role>)`
parenthetical that `_HEADER_RE` already accepts inside `<reviewer>` stays
**permitted and informational** — see S4.

**S2 -- the attestation lines.** Inside a pass body (after the S1 heading, before
the next H2), exactly one line each, full-line anchored:
`**Tier**: <Internal|External>` and `**Findings**: <none|raised>`.
Value comparison is case-insensitive; the canonical spellings are `Internal`,
`External`, `none`, `raised`.

**S3 -- closed vocabulary, three fail-closed directions.**

| condition | verdict |
|---|---|
| value outside the vocabulary | violation: `unrecognized <field> value` |
| field absent from the pass body | violation: `missing <field>` |
| field occurs more than once in one pass body | violation: `duplicate <field>` — **even when the occurrences agree**; agreement is a judgement a conformance backstop must not make |

No condition yields a silent pass. There is no default value for either field.

**S4 -- declared, never inferred.** The checker reads the tier from the
`**Tier**:` line and from nowhere else. It must **not** derive it from the
reviewer name, the `(role)` parenthetical, `_load_ai_registry`, the
human-maintainer roster, or byline classification. A human reviewer declares
`**Tier**: External` in the same shape an agent does. The `(role)`
parenthetical remains free text and is **not read by the gate** — stated
explicitly so it cannot drift into a second, softer source of truth. Violation
text never uses the language of authorization: the tool attests that a tier was
*declared*, never that it was *true* (the plan's `[E4]` fence, carried
unchanged).

**S5 -- tier ordering.** Total order `External > Internal`. A pass satisfies the
floor iff `declared >= required`. `External` satisfies a required `Internal`;
`Internal` does not satisfy a required `External`. There is no third tier and
no `Maintainer` tier — a human review declares `External`.

**S6 -- normalizing the required tier.** Defined on the **first parenthesised
group only** of the `**Plan review**:` field:

1. match `^required\s*\(([^)]*)\)` case-insensitively; no match → violation
   `tier not declared`;
2. delete every `*`, `_` and backtick from the group;
3. take the **first alphabetic word** (`^[A-Za-z][A-Za-z-]*`);
4. case-fold; it must be `internal` or `external`, else violation.

Text after the closing `)` is ignored (all 31 live plans have some). Text after
the first word *inside* the group is a **lens annotation** — preserved in the
record, ignored by the tier comparison. Verified against the measured
population: all **6** live forms resolve (19 External, 12 Internal), including
the two a comma-split rejects. Negations fail closed: `required(not External)`
→ violation. `not required(<rationale>)` disables the gate, unchanged.

**S7 -- Sharpening pairing is positional.** When a pass declares
`**Findings**: raised`, a heading matching `^### Sharpening\b` must occur
**inside that pass's body** — between its S1 heading and the next H2. Positional,
not date-matched: a sibling round's Sharpening cannot satisfy another round
(`[E3]`). When `**Findings**: none`, a Sharpening in the body is permitted and
not required. `Sharpening` enters `_KNOWN_KINDS`; today it is absent, which is
why the scaffold's own emitted block parses to nothing.

**S8 -- what the gate decides.** For a plan whose field is `required(<tier>)`:
every S1-matching pass must satisfy S2, S3 and S7 (each failure is a violation);
**and** at least one S1-matching pass must satisfy S5. Both conditions must
hold. A heading beginning `Plan review` that does not match S1 is neither a pass
nor a violation — and can no longer clear anything, because clearing now
requires an S1 match. **Near misses fail closed as "no conforming pass has
landed", never as "a pass with problems"**, and the violation text must quote
the near-miss heading so the author is not left guessing.

**S9 -- the grandfather rule, exactly.**

* **(a) One constant.** `_REVIEW_SCHEMA_EPOCH`, a module-private ISO date
  literal in `lifecycle_planner.py`, set to the date of the commit that lands
  Chunk C. Not a per-file marker, not configuration, not an environment
  variable — one constant in one place, so the exception cannot widen silently.
* **(b) The fence.** A pass dated **strictly before** the epoch is *legacy*:
  exempt from S2, S3 and S7, and it satisfies the floor by presence exactly as
  today. A pass dated **on or after** the epoch gets no exemption.
* **(c) Why legacy passes still satisfy the floor.** Before the epoch the tier
  lived in free text and the Maintainer accepted those records. Measured at
  `da1de65`: **31** review-required plans carry **44** dated passes, none of
  which can carry S2 fields. Refusing them strands 15 `open` plans and 1 in
  `awaiting-plan-review`. The exemption *is* the migration; it is not a
  softening for new work.
* **(d) It cannot become a second grammar** (`[E6]`). Two nodes: one asserts a
  pass dated on or after the epoch is refused without S2 fields; one pins the
  epoch literal, so moving it is a visible test edit rather than a silent
  widening. `bootstrap/UPGRADE.md` states the epoch and that the exemption is
  dated, not permanent.

**S10 -- this plan's own bootstrap, named.** Admitted as legacy under S9(b),
without rewriting them — which append-only forbids:

* `## Plan review -- Codex (External, different-agent-type) -- 2026-08-04` (this file, line 166)
* `## Plan review -- Codex (External) -- 2026-08-05` (this file, line 369)
* the S11 round, whenever it lands.

All are dated strictly before any achievable epoch, since Chunk C cannot land
before Chunk A and Chunk A cannot land before S11. **No file-specific carve-out
exists or is needed** — the date fence alone admits them, which is precisely
why it cannot become a permanent alternative grammar.

**S11 -- the second External round.** Required by `[E2]`, re-demanded by `[E5]`.
It reads S1--S13 and lands **before Chunk A's first commit**. It is itself
pre-epoch and legacy-admitted. **This Response does not substitute for it.**

**S12 -- one predicate, both call sites.** A single module-private pair —
`_review_conformance(art) -> List[str]` and `_review_satisfies_floor(art) -> bool`
— consumed by **both** `_conformance_violations` and `_gating_preconditions`.
At `da1de65` the duplicated `_has_kind(art, "Plan review")` calls are at
`tools/lifecycle_planner.py:791` and `:865`. A node asserts both surfaces return
the same verdict on the same fixture, so `scan` cannot tighten while
`next --to executing` stays presence-only.

**S13 -- the twin.** Every change lands identically in
`tools/lifecycle_planner.py` and `templates/skills/_lib/lifecycle_planner.py`.

### Amendments in force

**Precedence: where a row and the text it supersedes disagree, the row
governs.** Two container-level accommodations are declared so the quotes can be
audited: a source line break inside a quoted passage is shown as a single
space, and where the superseded text *is* a table cell the surrounding `|`
delimiters are omitted (they are container syntax, not content). No other
character is altered.

| # | Anchor | Superseded text (verbatim) | In force |
|---|---|---|---|
| 1 | A.1, Change cell (`:77`) | State **one** grammar: an `## Plan review` container, with each pass a dated `### Plan review -- <reviewer> -- YYYY-MM-DD` inside it. Reconcile `:115` and `:422` to it. | State **one** grammar per **S1**: a dated `## Plan review -- <reviewer> -- YYYY-MM-DD` **pass at H2**, with its `### Sharpening` at H3 inside it. `doctrine/plans.md:115` (`##`) and `:116` (`### Sharpening`) are **already correct and stay**; `:422` is the line that changes, from `###` to `##`. |
| 2 | C.2 row (`:104`) | C.2 \| heading level per A.1 \| new \| accept any level → red | C.2 \| S1 heading match (H2, `--` separator, ISO date) \| new \| accept H3 → red; accept an undated pass → red; accept `## Plan review tier` / `## Plan reviewers` → red. Each falsifier reddens C.2 and no other node. |
| 3 | `## Plan review` section (`:147-148`) | *Required — **External**. Implementation does not start until a review has landed under this heading.* | Required — **External**. Implementation does not start until a review satisfying **S1--S8** has landed **as a dated H2 pass in this file**. "Under this heading" is withdrawn: it describes a nesting the append-only lifecycle cannot produce, and it is the wording that let this plan's presence gate clear on two REVISE verdicts. |
| 4 | B.1, Change cell (`:90`) | Add to the review-pass format a **declared tier attestation** and a **review outcome**, both with **closed vocabularies**. Document in terms that the attestation is *declared, not authenticated*. | Implement **S1--S6** exactly: field names `**Tier**` and `**Findings**`, vocabularies `Internal\|External` and `none\|raised`, the three fail-closed directions of S3, the S4 no-inference rule, the S5 ordering, and the S6 normalizer validated against the 6 live `required(...)` forms. The *declared, not authenticated* framing is retained by S4. |
| 5 | B.3, Change cell (`:92`) | Parse the two fields. Admit `Sharpening` to `_KNOWN_KINDS` — `[E3]` established it is absent today, so the conditional currently has no parseable subject. **Parse only; gate nothing yet.** | Unchanged in intent, sharpened in evidence: `Sharpening` is absent from `_KNOWN_KINDS`, so **the scaffold's own emitted block** (`:986-990`) parses to nothing — verified, a scaffold-shaped document yields `[(2, 'Plan review')]`. Also parse the S2 fields and the S6-normalized required tier. **Parse only; gate nothing yet.** |
| 6 | C.4 row (`:106`) | C.4 \| `### Sharpening` when outcome declares findings \| new \| drop the conditional → red | C.4 \| **S7 positional** pairing: a `### Sharpening` inside *that pass's* body when it declares `**Findings**: raised` \| new \| drop the conditional → red; **and** move a sibling round's Sharpening outside the pass body → red (a neighbouring round's Sharpening must not satisfy this one). |
| 7 | Chunk C table (addition; attaches after C.4 — no superseded text) | *(none — this is an addition)* | **C.5** unknown / missing / duplicate `**Tier**` or `**Findings**` → violation, per S3, one falsifier each. **C.6** S6 normalization: all 6 live forms resolve; `required(not External)` and `required()` fail closed. **C.7** S5 ordering: `Internal` on an `External` floor → red; `External` on an `Internal` floor → green. **C.8** S12: both call sites return the same verdict on the same fixture; making one strict alone → red. **C.9** S9: a pass dated on/after `_REVIEW_SCHEMA_EPOCH` without S2 fields → refused; a pass dated before → admitted. |
| 8 | Acceptance criteria (`:122-123`) | * `doctrine/plans.md`, both templates and the scaffold state **one** grammar; a grep for the review heading across all four surfaces returns one shape. | `doctrine/plans.md`, both templates and the scaffold state **one** grammar, verified by an **exact structural oracle** over all four surfaces — never a grep. The "returns one shape" criterion is **withdrawn**: it is incoherent against any grammar with an H2 pass and an H3 Sharpening, and a prefix grep is the very defect under repair. |
| 9 | Acceptance criteria (`:125-127`) | * Four new nodes in `bootstrap/tests/test_lifecycle_contract.py`, each with its single-property falsifier **demonstrated**, not asserted — the falsifier is run and the red/green matrix recorded. | The **coverage set C.1--C.9** in `bootstrap/tests/test_lifecycle_contract.py`, each with its single-property falsifier **demonstrated** — run, with the red/green matrix recorded. The count "four" is withdrawn; the set is the criterion. The baseline is re-measured at the gating commit, **not** carried from here (`33 passed` at `da1de65`). |
| 10 | D.1, Change cell (`:117`) | State the record-format change, the two affected fields, and what an adopter must do. The twin is a `verbatim` manifest source installed as `tools/lifecycle_planner.py`, so behaviour and policy ship together. | Same content, with a **durable home: `bootstrap/UPGRADE.md`** (which exists, and already carries a "Migrating a tree installed before upgrade support" precedent). It must state the two field names, the S6 normalizer, the `_REVIEW_SCHEMA_EPOCH` value, and that the exemption is **dated, not permanent**. The twin sentence stands. |
| 11 | *Sequence* (`:64-66`) | **Measured, `as_of 2026-08-04` at plan-open** — `grep -rhoE "^#{2,3} Plan review" dev/plans dev/proposals \| sort \| uniq -c`: **58 headings, all `##`, none `###`** (56 in `dev/plans`, 2 in `dev/proposals`). | The figure **reproduces exactly** and is retained as history. It is superseded **as evidence**: the command is a prefix match, and the exact split at `8dfb664` is **34** dated passes / **3** bare containers / **21** unrelated headings. At `da1de65` it is **44 / 5 / 22**. Any inventory uses the exact oracle. |
| 12 | *Source proposal* (`:16-17`) | The gate at `tools/lifecycle_planner.py:787` clears on the *presence* of a section named "Plan review", not on the review its own doctrine describes. | Correct at `8dfb664`; at `da1de65` the two call sites are `:791` (`_conformance_violations`) and `:865` (`_gating_preconditions`), with `_has_kind` at `:697`. Both are named, and S12 replaces them with one predicate. Cite by **symbol**, not line, from here on. |
| 13 | *Verification* (`:136-137`) | * Reproduce the proposal's five-state table against the **post-change** module; the four rows that clear today must not all clear after Chunk C. | Reproduce it against **both** call sites, since S12 unifies them. The four shapes measured to clear today are: H3 dated pass, undated named pass, bare container, and Internal-only pass on an External floor. Add the two prefix collisions found here — `## Plan review tier` and `## Plan reviewers` — which also clear today and which S1 rejects. |
| 14 | *Verification* (`:138-140`) | * Confirm the tier attestation is parsed from the closed vocabulary and that an **unrecognized** value is a violation rather than a silent pass — the fail-open direction is the one that matters. | Retained and widened to **all three** S3 directions — unrecognized, **missing**, and **duplicate** — plus the S6 rejections. Unrecognized alone leaves two silent passes open. |
| 15 | Chunk C pre-inventory (`:108-111`) | **Before C lands, run the reconciled gate over every artifact in `dev/` and record which newly violate.** A gate that reddens the existing tree needs that disclosed up front, not discovered. That table is a deliverable of this chunk, not a note. | **Upheld**, with `[E4]`'s addition made binding: evaluate open plans **as if transitioning to `executing`**, not only in their current state — an old-format review stays green while status is `open` and fails only later, so a current-state scan reports a clean tree and is wrong. Population at `da1de65`: 31 review-required plans, 44 dated passes. |

Additions to *Lasting-truth migration*: **(i)** the tier and findings fields are
parser fields, never inferred from a byline → `doctrine/plans.md`, beside the
format; **(ii)** the schema epoch is a dated exemption, not a second grammar →
`bootstrap/UPGRADE.md` and the module constant.

### Gate audit

| Gate | Where | Satisfied today? |
|---|---|---|
| Declared tier `required(**External**)` | header `:7`, re-affirmed in the Decision | **NO.** Two External passes landed; both returned **REVISE**. A REVISE records the read and does not discharge the tier — `[E5]` says so directly. |
| "Implementation does not start until a review has landed under this heading" | `## Plan review`, `:147-148` | **Structurally cleared by the tool; substantively NOT.** Measured at `da1de65`: `_conformance_violations` returns `[]` for this file and `_gating_preconditions(art, "executing")` returns **PASS / PASS**. The tool would let this plan move to `executing` **today**, on two REVISE verdicts. That is the exact defect the plan exists to fix, and the plan must not ride it. Amended by row 3; the operative gate is the tier row above. |
| Decision condition — reconcile the `##`/`###` grammar across doctrine, both templates and the scaffold **before gating on it**, and treat the adopter-facing record-format change as in scope | proposal Decision, quoted in *Scope* | **Partially.** The choice is now settled (S1, row 1) and the adopter-facing change has a real home (row 10). **Unsatisfied as implementation** — Chunk A has not started, so nothing is reconciled yet and nothing gates yet. Consistent, not discharged. |
| "REVISE. No implementation commit should land on the presence of this review." | 2026-08-04 External | **In force; honoured.** No implementation commit exists. |
| "No implementation commit lands on this Response's strength." | 2026-08-04 Response | **In force; honoured**, and re-stated for this Response. |
| "then obtain the promised second External read before Chunk A" | `[E5]`, 2026-08-05 | **In force; NOT satisfied.** S11. This is the binding blocker. |
| Maintainer fence — "This plan ships the migration *note*; running it is the Maintainer's." | *Scope* > Out of scope | **In force.** D.1 writes `bootstrap/UPGRADE.md` only; no agent touches either adopter tree. |
| Serialization fence — "**Serialized: text returned, not edited in-agent.**" | D.2 | **In force.** The `CHANGELOG.md` line is returned as text, never edited by the implementing agent. |
| Fenced region — `doctrine/lifecycle.md:175-182` stays untouched; Chunk D of `gate-claims-vs-enforcement` owns `:218-221` | *Scope* > Out of scope | **In force.** Row 1 changes `doctrine/plans.md:422`, not `doctrine/lifecycle.md`. |
| "the twins stay byte-identical" | Acceptance | **True now** (`md5 457b51c7772da181e838f99a2205d933`); S13 keeps it true per commit. |
| "no *new* failure relative to a baseline measured immediately before the commit **on a quiet tree**, `0 skipped`" | Acceptance | **In force, and the tree is NOT quiet.** HEAD moved `6bcd2d3` → `da1de65` during this session; a plan file changed between two of my own measurement runs. The baseline must be taken at the gating commit, and the non-quiet condition disclosed with it. |
| "Chunk C's corpus table must be re-measured at the commit that gates" | *Sequence* `:72-73` | **In force, upheld, and evidenced**: 58 → 71 in ~24 h. |

### Status

`open`, unchanged. **This Response does not clear the plan to implement, and
does not discharge the External tier.** It supplies what `[E5]` asked for
first — the complete grammar, its fail-closed behaviour and the exact
grandfather rule, as a binding amendment with stated precedence — so that a
reviewer now has a settled artifact to attest rather than a direction to trust.
What remains before Chunk A's first commit is **S11**: a second External,
different-agent-type read of S1--S13 and the Amendments table. Until that
lands, no implementation commit may cite this Response, this plan's presence
gate, or either prior REVISE.

## Plan review -- Codex (External) -- 2026-08-05

**Tier**: External
**Findings**: raised

**Verdict: REVISE.** I performed the S11 different-agent-type read of S1--S13
and the Amendments table. The Response did more than promise a future rewrite:
its precedence clause makes the settled schema part of the operative contract.
That closes my prior [E5] objection to leaving the schema only in Response
prose. The settled schema still contains one blocking bypass and one smaller
ambiguity, however, so this read does not authorize Chunk A.

The S9 legacy migration fence trusts the date written in the review heading.
Under S1's own regex, a newly appended pass headed
`## Plan review -- New Reviewer -- 2026-01-01` is accepted as pre-epoch and
therefore receives the permanent legacy exemption. An editor can consequently
route a new pass through the old grammar by backdating it. Bind the legacy
population to immutable provenance -- for example, an explicit enumerated set
of pre-existing pass sections or a commit boundary -- rather than an editable
date. Otherwise S9 creates the second grammar it says it prevents.

S1 also accepts date-shaped but impossible values such as `2026-99-99`.
Specify calendar-valid parsing and the comparison operation used by S9; a regex
shape check alone is not a date contract. I reproduced both behaviors with the
canonical Python 3.13.13 interpreter against freshly constructed headings.

### Sharpening

Keep the gate's claim narrow: it checks recorded conformance, not whether the
named reviewer or review event is authentic. Once the legacy set and date
semantics are made non-gameable in the binding schema, S11 can be considered
discharged by this round without seeking another broad redesign.
