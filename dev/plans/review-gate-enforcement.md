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
