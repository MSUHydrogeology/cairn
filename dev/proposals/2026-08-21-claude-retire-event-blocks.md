# Measure the record, not the act: retire the event-block machinery

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-21
**Status**: accepted
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
**Plan review**: **not required** — assigned by the editor at the Decision under
their ordinary authority over plan triage. Revision 1 carries the contract a
derived plan would restate; a plan would cost a round and add nothing, and with
no derived plan there is no tier for RTE-04's recorded token to bind. *(The
original wording justified this by C8 of `review-loop-termination`, which was
never implemented; corrected below — see "Correction to the Decision". The
routing itself is unchanged.)* See the Decision below, including the fence on
the install-contract re-pin.

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

## Response + Revision 1 -- Claude -- 2026-08-24

All five blocking findings are closed. Four were correct as written; the fifth
(RTE-03) is correct on its substance and its *number* is the proof of its own
point, which is worth more than the number would have been.

**Scope delta: widened, not narrowed.** The Maintainer's instruction was to meet
the objective without narrowing, and RTE-01 is where that bites: the answer to
"what happens to `reviewer_agents`, `external_tier_review`, `response_models`?"
is **all retained and restored from text**, not dropped from the schema. Those
are the publication-relevant columns; deleting them to satisfy a reviewer would
be the narrowing that costs nothing to propose and can never be shown wrong.

### Withdrawn / superseded commitments

* **`Plan review: not required`** -- **withdrawn.** It rested on the premise
  RTE-02 disproved: that this is a module deletion plus one function. It is a
  deletion across five source pairs, an install contract, two planner twins,
  four templates and three count pins. Routing returns to the editor.
* **The opened Evidence plan's single acceptance criterion** ("at least 37/46
  populated") -- **superseded** by the fixture oracle plus five directed
  mutations. RTE-03 is right that a coverage threshold passes on an
  implementation that assigns one review to every plan.
* **Nothing else.** No column, no deletion, and no part of the objective is
  dropped. RTE-01's answer widens the contract rather than narrowing it: all
  seven event-derived columns are retained and restored from text.

**Why this heading was missing, for the second time today.** The identical
defect was found and fixed on `2026-08-20-claude-review-loop-termination` a few
hours ago, and I wrote the note explaining it -- that a required section whose
value is often "None" is the one that gets dropped. Then I dropped it again,
here, where it is *not* None. The scanner caught it this time because this
artifact is live; on the other one `accepted` is terminal and `_is_immutable`
short-circuits the check, so the same defect sat unseen. A control that only
fires while nobody needs it is worth recording as its own small finding.

### Findings ledger

| finding | disposition |
|---|---|
| RTE-01 -- the replacement leaves the event-derived schema without a contract | **Closed.** Every event-derived column now has an explicit disposition below. All seven are **retained**, each with its exact parser and blank behavior. None is removed from the public schema. |
| RTE-02 -- deleting `events.py` is not a two-file removal | **Closed, and the finding is simply right.** My "module deletion plus one function" was false and I verified the reviewer's inventory rather than conceding it: `events` is imported by `cli.py` and `extract.py` in **both** twins; `bootstrap/_scaffold/config.py:763` installs it via `InstallSpec`; both planners carry 5 `cairn-event-v1` references each; all four templates teach the grammar; `test_notice_install.py` pins 57, 53 and 115. Full inventory below. |
| RTE-03 -- the acceptance criterion can pass while reporting the wrong history | **Closed.** Exact grammar specified, fixture oracle with per-artifact expected counts, directed false-positive and false-negative mutations. The count discrepancy is reconciled below. |
| RTE-04 -- the proposal cannot waive its derived plan | **Closed by supplying the contract, and the routing goes to the editor.** The `not required` claim rested on the false premise RTE-02 demolished, so it is withdrawn. See "Routing" below -- I am not re-asserting a waiver. |
| RTE-05 -- the required security preflight is absent | **Closed.** Five answers below. S5 is the one that changes the design. |

### RTE-03 reconciled -- two readers, two grammars, no spec

The reviewer measured **46/46** plans with a code-review heading; I measured
**37/46**. Neither of us misread the corpus. Measured 2026-08-24:

| pattern | plans matched |
|---|---|
| any `^## Code review` heading | **46** |
| a *dated* pass (`## Code review ... -- YYYY-MM-DD`) | **37** |
| carrying **only** the bare template stub | **9** |

`46 - 37 = 9`, exactly the stub-only plans -- every plan scaffolded from the
template inherits an empty `## Code review` placeholder. The reviewer's number
counts placeholders as passes. That is not a refutation of the table; it is a
live demonstration that an unstated grammar produces two confident, different
answers, which is precisely what RTE-03 said. The grammar is therefore specified
below rather than defended.

### RTE-01 -- disposition for every event-derived column

All **retained**. Each parses from text that already exists across the entire
history, so each moves from mostly-empty to mostly-populated retroactively.

| column | source | blank when |
|---|---|---|
| `review_rounds` | count of dated `## Review` passes | no dated pass |
| `plan_review_rounds` | count of dated `## Plan review` passes | no dated pass |
| `code_review_rounds` | count of dated `## Code review` passes | no dated pass (9 plans today, correctly) |
| `reviewer_agents` | the reviewer identity in each accepted heading, deduplicated, in document order | no dated pass |
| `cross_agent_type_review` | two or more distinct reviewer identities across accepted passes | fewer than two |
| `external_tier_review` | a `**Tier**: External` line inside an accepted pass's field block | no pass carries a tier line |
| `response_models` | the `**Model**:` field inside each `## Response ...` section, deduplicated | no Response carries one |

**Blank is never zero.** A column with no evidence renders empty, not `0` --
`code_review_rounds` reading `0` on artifacts that were simply never parsed is
the original defect (28 of 38), and reproducing it with a different parser would
be the same bug wearing new clothes.

**Adopter-facing schema migration: none.** Column names, order and count are
unchanged; only their population improves. The CSV header is byte-identical, so
an adopter parsing it sees more rows filled and nothing move.

### RTE-03 -- the accepted grammar, stated

A **pass** is an H2 matching, case-sensitively:

    ^##\s+(Review|Plan review|Code review|Security review|Security re-review)\b

and additionally containing ` -- ` and an ISO `YYYY-MM-DD` date on the heading
line. Everything else is excluded, and each exclusion is a named test case:

* **the bare template stub** -- no ` -- `, no date. 9 plans today.
* **a disposition** -- `disposition` anywhere in the heading. A Maintainer's
  `## Security review disposition` is a decision about a pass, not a pass.
* **a Response** -- `## Response to code review ...` answers a pass.
* **a correction** -- `## Correction to the Security review disposition ...`.
* **H3 and deeper** -- `### Blocking findings` sits inside a pass.

**Reviewer identity** is the text between the first and second ` -- ` on the
heading line, with a trailing parenthetical role stripped:
`## Code review -- Codex (External) -- 2026-08-21` yields `Codex`.

### RTE-02 -- the complete deletion inventory

**Source pairs** (twin rule, one commit, byte-identical): `events.py` deleted
from `tools/_lifecycle_metrics/` and `templates/modules/default-on/_lifecycle_metrics/`;
`extract.py`, `cli.py`, `__init__.py` and `snapshot.py` edited in both to drop
the import, the exception handling and the reconciliation types.

**Install contract**: remove the `InstallSpec` at `bootstrap/_scaffold/config.py:763`
and re-pin the three counts in `bootstrap/tests/test_notice_install.py` --
manifest sources 57 -> 56, on-disk templates 53 -> 52, manifest rows 115 -> 114.
Each pin carries a comment naming the change that moved it; these gain one
naming this proposal.

**Planner pair**: remove the 5 `cairn-event-v1` preview references from
`tools/lifecycle_planner.py` and its twin.

**Template pairs**: remove the grammar from `dev/proposals/_template.md`,
`dev/plans/_template.md` and both `templates/core/` twins, so no future edit is
invited to emit a block.

**Tests**: `bootstrap/tests/test_lifecycle_metrics_events.py` -- the
reconciliation, history-walk and activation-cutoff cases are **deleted** with
the code they cover; `test_an_unreconciled_act_empties_its_own_fields_and_never_refuses_the_run`
is **retained**, re-aimed at the heading reader, because the never-refuse
property outlives the mechanism. New cases for the grammar oracle land here.

**Doctrine**: `docs/glossary.md`'s Archive entry loses the `cairn-event-v1`
exception and returns to its prior rule.

### RTE-05 -- security preflight, five answers

**S1 -- Who supplied it?** The counter decides one thing: whether an H2 is a
review pass. Inputs are the artifact's own bytes (via `git show`/read) and
nothing else. **The thing being decided about supplies its own evidence** --
an artifact declares its own review count by carrying headings. That is inherent
to measuring a self-reported record and is why S5 lands where it does.

**S2 -- Can it fail?** Directed mutations, each required red: strip the date from
a dated pass (count must drop); add a bare `## Code review` stub (count must not
rise); rename a `disposition` heading to look like a pass (count must not rise);
add a second distinct reviewer (`cross_agent_type_review` must flip); remove a
`**Tier**: External` line (`external_tier_review` must clear). The oracle is a
named fixture table of expected per-artifact counts, so no check derives its
expectation from the object it checks.

**S3 -- What fires it, over what?** `python tools/lifecycle_metrics.py
{proposals,plans} --root .`, run by a human. **Cairn has no CI and nothing
schedules this.** No preset or profile selects it. It covers every `.md` under
`dev/proposals/` and `dev/plans/` including `archive/`.

**S4 -- Which way does it break?** Every failure path lands on **less**
authority: an unparseable heading is not counted, a missing tier line leaves
`external_tier_review` blank, an unreadable file yields an empty row rather than
aborting the walk. There is no path where a parse error *raises* a count or
refuses a run -- that direction is what `8416d9d` removed and what the retained
never-refuse test pins.

**S5 -- Who still wins?** The assumed capability is: write access to the
repository's own artifact files. Anyone with it **still wins completely** --
they can add five dated review headings and inflate their own review count, and
no parser can tell an authored heading from an honest one. The class is closed
by **neither** construction nor enumeration; it is open.

**That is the design consequence, not a caveat.** These metrics are
**self-reported and must never gate anything**. It is the same lesson the
enforcement incident taught from the other direction: a measurement that can
refuse is both a broken instrument and a forgeable control. The module's
doctrine gains one sentence saying so.

### Verification plan (replaces the opened one)

* **A fixture oracle**, not an aggregate: a named table of artifacts with
  expected per-artifact counts for all seven columns, plus the five directed
  mutations in S2, each required red.
* **Before/after population**, as a readable consequence rather than the check.
  Acceptance: no currently-populated column regresses, and the seven columns
  above move off zero.
* **Twin byte-parity** for all five source pairs, both template pairs and the
  planner pair, one commit each.
* **Install contract**: `scaffold.py --manifest` re-pinned at 56/52/114 with
  the scoped `upgrade --finalize`, and `test_notice_install.py` green.
* Scoped suites only. No broad run: the guard refuses one by design.

### Routing -- RTE-04, and it is the editor's

I withdraw the `not required` claim in the header. It rested on the premise
RTE-02 disproved, and a reviewer blocking on it is exactly the correction the
apparatus is for.

What I have done instead is **supply the contract a plan would carry** -- the
full file inventory, the parser spec, the fixture oracle, the count re-pins and
the sequencing -- inside this artifact, which is the shape
`2026-08-21-claude-convergent-lifecycle` proposes as the Standard lane.

**Recommendation, with a default:** implement directly from this Decision as a
single artifact. Nothing above is left to an implementer's discretion, and a
derived plan would restate it at the cost of another round. **Default if the
Maintainer prefers the two-stage lane:** open a change note carrying the
sections above verbatim.

**On the tier**: this review recorded `DISTINCT REVIEW REQUIRED`, which under
current doctrine forces `required(External)` on any derived plan. I am not
overriding that -- the editor assigns it, and the Maintainer has stated this is
the only review. Recorded so the decision is made knowingly rather than
inherited from a token.

### Length

This revision runs past the strategy note's ~150-line anchor. The anchor prices
an *opening* artifact; closing five blocking findings with a complete
implementation contract that replaces a derived plan is the trade the note's
2.2 asks for -- one artifact instead of two, not one artifact plus a short one.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-24

**ACCEPTED as revised (Revision 1).** Authorization, quoted verbatim and
visually isolated:

> "Okay, this looks ready to go to me. Please scribe my acceptance as revised."

**Summary of accepted terms (Revision 1)**:

- **Delete the event-block machinery.** `events.py` (1,017 lines per twin) with
  its reconciler, history walk and activation-marker resolution; the
  `cairn-event-v1` grammar removed from both planner twins, both template pairs
  and `docs/glossary.md`, so no future edit is invited to emit a block.
- **Count from section headings, retroactively.** A pass is an H2 matching
  `^##\s+(Review|Plan review|Code review|Security review|Security re-review)\b`
  carrying ` -- ` and an ISO date. Named exclusions, each a test case: the bare
  template stub, a `disposition`, a `Response`, a `Correction`, and H3-or-deeper.
- **All seven event-derived columns are retained**, each with its stated parser
  and blank behavior. None is removed from the public schema; the CSV header is
  byte-identical, so no adopter migration. **Blank is never zero.**
- **Enforcement does not return.** A measurement reports what it can and leaves
  the rest empty, pinned by the retained never-refuse test. Per RTE-05's S5,
  these metrics are self-reported and forgeable by anyone with write access to
  the artifacts, and must never gate anything.
- **Verification** is a fixture oracle of expected per-artifact counts plus five
  directed mutations each required red -- not the aggregate population table,
  which is a readable consequence.

**Routing, assigned by the editor.** Implement **directly from this Decision as
a single artifact**; no derived plan. Revision 1 supplies the complete file
inventory, the parser grammar, the fixture oracle, the count re-pins and the
sequencing, so a derived plan would restate a settled contract at the cost of a
round. RTE-04's `DISTINCT REVIEW REQUIRED` is advisory under C8 of
`review-loop-termination` and does not force an External tier.

**One fence, and it is where the risk actually is.** The install-contract
re-pin -- removing the `InstallSpec` at `bootstrap/_scaffold/config.py:763` and
moving the pins 57 -> 56, 53 -> 52, 115 -> 114 -- is **MAINTAINER-GATED**. It
does not execute without explicit authorization, and `scaffold.py --manifest`,
the scoped `upgrade --finalize` and `test_notice_install.py` must all be green
and shown before it is sought. Reason: C0 of `review-loop-termination` lowers
review calibration on ordinary work but retains full weight for the install
contract by name, and that is the one surface here where a silent error reaches
adopters. Everything else in this proposal implements without a gate.

*Scribe's note, separated from the authorization above:* the routing and the
fence are the recommendation put to the Maintainer immediately before the quoted
instruction, adopted by it. They are the editor's assignment under C1 as
extended, recorded here rather than deferred.

**Open item, named rather than left implied.** RTE-01's seven column parsers are
unverified at runtime -- no implementation exists, the same limit the reviewer
recorded as not covered. The fixture oracle is what settles it, and it is an
acceptance criterion above rather than a discovery for the implementer.

**Scribed by** Claude (claude-opus-5), this proposal's author, on explicit
Maintainer instruction. The scribe wrote no part of the authorization quoted
above.

## Correction to the Decision -- Claude -- 2026-08-24

Appended on Maintainer instruction. The Decision above stands as accepted; two
of its citations are wrong, and one downstream consequence was not visible when
it was written.

**The C8 citation is false.** The Decision's routing paragraph says RTE-04's
`DISTINCT REVIEW REQUIRED` "is advisory under C8 of `review-loop-termination`",
and the header repeats it. Measured 2026-08-24:
`2026-08-20-claude-review-loop-termination` carries `**Status**: superseded`, it
has no derived plan, and `ORDINARY` -- the third token C8 introduces -- occurs
**0 times** in `AGENTS.md`, `doctrine/dual-review.md` and
`doctrine/proposals.md`. The escalation trigger it would have retired is still
live in `AGENTS.md`. C0-C8 were accepted and superseded the same day without
being implemented, so **nothing in that proposal was in force when this Decision
cited it.** The error is mine as scribe: I trusted an acceptance without
checking whether it had landed, which is the same defect this repository's own
verify-before-asserting rule exists to prevent.

**What does not change, and why.** The routing -- implement directly from the
Decision, no derived plan -- is unaffected: with no derived plan there is no
plan-review tier for the token to bind, so the token was never reached. Its
correct basis is the Maintainer's ordinary Decision authority over plan triage,
not C8. The **MAINTAINER-GATED fence on the install-contract re-pin also stands
unchanged**: `AGENTS.md` names the install contract a high-risk surface
directly, so the fence never depended on C0. Both outcomes were right; one
citation was not.

**Where the rule now actually comes from.** On 2026-08-24 the Maintainer waived
the External floor on `2026-08-21-claude-convergent-lifecycle` and recorded the
reasoning: a binding `required(External)` is apparatus a single-agent adopter
cannot staff, which contradicts `doctrine/dual-review.md`'s own commitment that
"the bootstrap never installs more review apparatus than the team can staff."
That proposal is accepted and is where C0, C1 and C7 now land. Cite it, not C8.

**A downstream consumer of this deletion exists.** This proposal removes the
`cairn-event-v1` grammar from both planner twins, both template pairs and
`docs/glossary.md`. `convergent-lifecycle` §2a -- accepted the same day --
requires change notes to *emit* that grammar, "so longitudinal metrics
survive." **The implementing agent of this proposal must not treat the grammar's
removal as unobserved.** The agreed resolution is recorded as item 1 of that
proposal's Decision preamble: change notes are counted by the dated-heading
grammar this proposal establishes, extended to the note lane. Whichever
implementation lands first, the heading reader must cover change notes, or the
note lane ships with no measurement story.

**Nothing else in the Decision is altered**, and its accepted terms are
unchanged.

## Implementation note -- the note lane's measurement story -- Claude -- 2026-08-24

Closes the open item the Maintainer's Correction (`b812f28`) named: *"this
proposal deletes the `cairn-event-v1` grammar that convergent-lifecycle 2a
requires for change notes. The implementer must extend the heading reader to the
note lane ... or the note lane ships with no measurement story."*

**No extension was needed, and the item is closed by measurement rather than by
argument.** `convergent-lifecycle` section 1 puts a change note at
`dev/plans/<slug>.md` -- the same directory as plans, with no `dev/notes/`
created anywhere. `iter_plan_files` already walks `dev/plans/*.md` plus
`dev/plans/archive/**/*.md`, and a note carries the same `## Plan review -- X --
<date>` and `## Code review -- X -- <date>` headings every other artifact does.

Verified against a change note written to that section's own spec (Why / What /
Approach / Verification / Risk, plan status vocabulary, no parent proposal):

    stem                 'tighten-dotted-branch-fence'
    status               'awaiting-code-review'
    plan_review_rounds   1
    code_review_rounds   1

**The lane is better off than its accepted text assumed.** That text says notes
"emit the same `cairn-event-v1` records as plans ... so longitudinal metrics
survive the merge" -- which placed an emission obligation on every note author at
every act, and made the lane's measurability depend on nobody forgetting. The
heading reader charges nothing: a note is measured because of headings it
already carries for human readers. The obligation that the enforcement incident
proved unrepairable never attaches to the new lane at all.

**The one condition, stated so it is not rediscovered.** This holds *because*
notes live under `dev/plans/`. If the note lane is ever given its own directory,
`iter_plan_files` must be widened in the same change -- otherwise notes become
invisible to the walk silently, which is the failure mode this whole proposal
exists to remove. That is a one-line change plus a test, not a redesign.
