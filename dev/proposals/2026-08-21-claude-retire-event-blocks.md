# Measure the record, not the act: retire the event-block machinery

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-21
**Status**: revising
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

## Review -- Codex (External) -- 2026-08-24

**Model**: GPT-5.6 (Codex)

Reviewed commit: b586a3f45d2c9de6dfd656732b8ffe8233b52dd4
Target: the complete opened contract, especially the replacement schema, deletion surface, verification plan, and plan-review routing
Prior findings: none
Assurance path: high-assurance
**Tier**: External
**Findings**: raised (5 blocking)
**Plan readiness**: DISTINCT REVIEW REQUIRED

### Steelman

The core observation holds: the event reader cannot recover the historical
record it was installed after, and an instrument must not prevent the work it
observes. Returning to a bounded structural reader is a defensible direction.
The proposal also correctly distinguishes measurable lifecycle structure from
prose volume and commits to a non-enforcing reporting posture.

### Findings

#### RTE-01 — BLOCKING: the replacement leaves the event-derived output schema without a contract

The proposed replacement names only review-round counts. The current proposal
schema also sources `reviewer_agents`, `cross_agent_type_review`,
`external_tier_review`, and `response_models` from reconciled event blocks; the
plan schema separately sources `plan_review_rounds` and `code_review_rounds`.
Those identity, tier, and model fields are the very publication-relevant zeros
the Context identifies, but neither Proposal item 2 nor the verification plan
says whether each is restored from defined text, deliberately removed from the
public schema, or remains blank. “No column currently populated becomes less
so” cannot protect a column presently empty everywhere.

Give every current event-derived output column one explicit disposition:
retained with its exact parser and blank/unknown behavior, or removed with the
adopter-facing schema migration. Include it in the before/after table and in
the module doctrine. The Decision cannot leave an implementer to choose which
part of Dual-Review evidence Cairn retains.

#### RTE-02 — BLOCKING: deleting `events.py` is not a two-file removal or a one-function replacement

Both package initializers import `events`; both CLIs catch its exception types;
both extractors and snapshot modules use its reconciliation types; and the
scaffold's `lifecycle-metrics` InstallSpec installs it. The lifecycle planner
and its byte-identical twin still preview `cairn-event-v1` blocks, while both
shipped proposal/plan templates teach authors to emit them. The deletion also
changes the three install/count pins: the manifest-source count 57, manifest
row count 115, and on-disk template count 53 all explicitly include this file.

Add the complete source/template pair set, `bootstrap/_scaffold/config.py`,
the planner pair, both template pairs, all affected test homes and count pins,
and every live adopter-facing grammar reference to `Touches` and the execution
contract. State which event tests are deleted, replaced, or retained. Without
that inventory the promised one-commit twin rule cannot cover the installed
module, and the scaffold can ship an import of a file it no longer installs.

#### RTE-03 — BLOCKING: the heading-count acceptance criterion can pass while reporting the wrong history

“At least 37/46” populated rows tests coverage, not correctness: assigning one
review to every plan passes it. The two alleged false positives are unnamed and
their exclusion grammar is not specified. The Context also says its commands
are reproducible but supplies none. Against the unchanged corpus at the
reviewed commit, the repository's existing dated-heading patterns yield 43/46
plans with a plan-review heading and 46/46 with a code-review heading, not the
table's 45/46 and 37/46. A different intended grammar may be valid, but it must
be stated and tested rather than inferred from a hand-filtered aggregate.

Define the exact accepted heading grammar and exclusions, including responses,
containers, dispositions, security passes, and historical H2/H3 forms. Pin a
corpus oracle or named fixture table with expected per-artifact counts and
directed false-positive and false-negative mutations; the aggregate population
table is then a readable consequence, not the only check.

#### RTE-04 — BLOCKING: the proposal cannot waive its derived plan or its independent sequencing review

This implementation deletes a default-on installed file, rewires a public
metrics schema, changes scaffold manifest rows and count pins, replaces
extractor behavior, and updates templates, planner output, tests, and doctrine.
It therefore satisfies several independent plan-triage conditions (multiple
files/areas and multi-stage sequencing). The strategy note is not a Maintainer
Decision authorizing a `not required` plan review, and the opened header's
claim that this is a module deletion plus one function is contradicted by the
live imports and manifest.

Open a plan with the full implementation and verification mapping. This review
records `DISTINCT REVIEW REQUIRED`, so that plan must declare
`required(External)` rather than bypassing the independent sequencing read.

#### RTE-05 — BLOCKING: the required security preflight is absent

The proposal changes parsing behavior and the default-on install contract, a
high-risk surface named in `AGENTS.md`, but includes neither the five written
preflight answers nor the required explicit N/A statement. The absence matters
here: a heading parser must state what artifact text supplies it, how malformed
or ambiguous headings fail, which real command exercises the installed tool,
and how deleting the history reader changes the no-git and malformed-record
paths. Those are design decisions, not implementation commentary.

Add the applicable five-question preflight, with mutations that falsify the
new counter and the install outcome. If the author concludes no trust boundary
is touched, record the template's required N/A sentence and substantiate it
against the install-contract trigger.

### Coverage

Covered: the full opened proposal; the accepted `metrics-events-not-prose`
contract it supersedes; the live metrics extractor, package initializer, CLI,
snapshot reader, scaffold InstallSpec, planner previews, and their byte-identical
twins; the three manifest/count pins; the shipped proposal and plan templates;
and the existing event test module. Targeted probes: the read-only metrics
corpus walk and the dated-heading counter over all 46 plans; byte-parity checks
for the affected twins. Not covered: an implementation of the new heading
reader, because the proposal does not yet specify one. Second-round
recommendation: **recommended** after a complete revision closes RTE-01 through
RTE-05.
