# Measure the record, not the act: retire the event-block machinery

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-21
**Status**: awaiting-review
**Assurance path**: high-assurance (a `default-on` module adopters install)
**Supersedes**: `2026-08-11-claude-metrics-events-not-prose` (accepted;
implemented and archived 2026-08-21 as plan `metrics-events-not-prose`). Its
**objective** binds here — Cairn must be able to examine itself and produce
evidence. Its **mechanism** does not.
**Touches**: `tools/_lifecycle_metrics/` and its shipped twin
`templates/modules/default-on/_lifecycle_metrics/`,
`bootstrap/tests/test_lifecycle_metrics_events.py`, `docs/glossary.md`, the
`cairn-event-v1` grammar wherever templates and doctrine teach it
**Related**: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md`
**Plan review**: not required — this deletes a module and replaces one
function. Implement directly from the Decision, per that note's 1.4.

## Objective

Keep self-examination. Cairn's differentiators are empirical claims — that
recorded deliberation and Dual-Review produce better outcomes — and an
empirical claim needs numbers, both to improve the codebase and to support
publishing Cairn. This proposal does not retreat from that. It changes the
instrument, because the current one measures almost nothing.

## Context — what the instrument actually produces

Measured 2026-08-21 against Cairn's own corpus, `lifecycle_metrics.py`:

| column | populated |
|---|---|
| `review_rounds` | 9 / 68 |
| `cross_agent_type_review` | 9 / 68 |
| `reviewer_agents` | **0 / 68** |
| `external_tier_review` | **0 / 68** |
| `response_models` | **0 / 68** |
| `plan_review_rounds` | **0 / 46** |
| `code_review_rounds` | **0 / 46** |

There are **4 `cairn-event-v1` blocks in the entire proposal and plan corpus**
(instrument control: the token is findable in 19 files repo-wide, mostly
templates — the grep works).

**It is currently worse than what it replaced, by its own stated measure.** The
prose-scraping path was retired because `code_review_rounds` read 0 on **28 of
38** artifacts — a real defect, cited in `extract.py`'s own comments. The event
path reads 0 on **46 of 46**.

**This is structural, not a bug or a bedding-in period.** Event blocks are
paired with acts *in their own introducing commit*, and only after an
activation cutoff. So the machinery can only ever measure forward from the day
it was installed. The evidence a publication needs is Cairn's development
history — precisely the period the event path cannot see, permanently. A paper
cannot say "our data begins the day we decided to collect it."

The columns a publication would most want are exactly the zeros:
`reviewer_agents`, `external_tier_review`, `response_models` — the Dual-Review
differentiator, the part that is actually novel.

**What heading-counting yields instead**, measured the same day over the same
corpus, filtering the two false positives found by hand (an empty template
stub, and a Maintainer *disposition* section which is not a review pass):

| | event path | heading count |
|---|---|---|
| plans with a review-round count | 0 / 46 | **45 / 46** |
| plans with a code-review count | 0 / 46 | **37 / 46** |
| proposals with a review count | 9 / 68 | **56 / 68** |

37 rather than 46 is not scraper failure: nine plans genuinely have no code
review. That is the true answer, available retroactively over the whole
history, today.

**And the machinery has already cost more than it produced.** On 2026-08-21 a
routine `**Status**` flip landed without an event block and the reconciler
refused the *entire* corpus walk — exit 3 — with no repair short of rewriting
published history. A measurement had become a gate on the thing it measured.
That enforcement is already removed (`8416d9d`); this proposal is about the
1,710 lines that remain.

**The strategy note supplies the motivation and the existence proof.** Its
ratchet 1 (every incident becomes a rule, no rule leaves), ratchet 2 (agents
write armor because verbosity is indistinguishable from rigor), and Tier 2.1's
**park** disposition — machinery defending hazards no current adopter has —
describe this module exactly. And the note itself is the proof that the
objective survives without the machinery: it produced roughly fifteen
defensible figures about Cairn's own process (166,000 lines of deliberation,
~8 lifecycle commits per proposal, 45 of 45 findings accepted, 4,468 tests at
~10 minutes) using greps and hand counts. Every figure that moved a decision
on 2026-08-21 came that way. None came from this module.

## Proposal

1. **Delete `events.py`** (1,017 lines) from both twins, with its reconciler,
   history walk, activation-marker resolution, and the `cairn-event-v1`
   grammar. Remove the grammar from templates and doctrine so no future edit is
   invited to emit a block.
2. **Count review rounds from section headings**, filtered for the two known
   false positives above. Retroactive over the full corpus.
3. **Keep every git- and text-derived column unchanged.** `date_opened`,
   `decision_date`, `days_to_decision`, the stage timings, `revised`,
   `proposal_annotation_count` are populated 55–68 of 68 today, cost nothing,
   and already support real claims: time-to-decision distributions, revision
   rates, how long artifacts sit at each stage.
4. **Enforcement does not come back.** A measurement reports what it can and
   leaves the rest blank. Pinned by
   `test_an_unreconciled_act_empties_its_own_fields_and_never_refuses_the_run`.

## What this deletes

~1,017 lines of `events.py` per twin, its test module's reconciliation half,
the activation-marker doctrine, and a standing obligation on every future
lifecycle edit. Net: the module keeps producing the columns that work and stops
carrying machinery for columns that are empty.

## Evidence / verification plan

* **Before/after population table**, the one above, regenerated. Acceptance:
  plan review-round coverage moves from 0/46 to at least 37/46, and no column
  currently populated becomes less so.
* **The two known false positives are pinned by test** — a template stub and a
  disposition section must not count as review passes. Both were found by hand
  on 2026-08-21 and both are why a naive count is not sufficient.
* Twins byte-identical, one commit. Scoped suites green.

## Signals the change is wrong

* Heading counts turn out to disagree with hand counts on a *material* claim —
  not on a placeholder, but on a figure someone would publish.
* Someone needs per-act precision that a heading cannot give: which model
  reviewed, at what tier. If that becomes load-bearing, the right answer is
  probably a field in the section header, not a git-history reconciler.
* An adopter asks for the event grammar. The current adopter's four filed
  issues were all "your tool doesn't run."

## Reviewer brief

The load-bearing question is not whether heading-counting is elegant — it is
not. It is whether **retrospective coverage of the real history beats
forward-only precision over data that does not exist**. Attack that. The
measurement tables are reproducible with the commands in Context; re-run them
rather than trusting them, and if the 28/38-versus-46/46 comparison is unfair
in a way I have not seen, that is the finding worth having.
