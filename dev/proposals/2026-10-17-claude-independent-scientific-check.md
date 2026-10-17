# One independent scientific check: the first step on scientific correctness

**Author**: Claude (Strategy)
**Status**: revising
**Review**: required(External)
**Plan review**: required(Internal) — prose edits to two authoring templates (each with its self-hosted twin), one doctrine lens, and three kernel sentences; no engine, install-contract or trust-boundary surface
**Opened**: 2026-10-17

## Context

Every scientific change answers two questions. **Is it well built?** The code
does what its author meant, its tests pass, its design holds up. Call that
*structural correctness*; every review Cairn ships asks it. **Is it right about
the world?** It conserves what must be conserved, its units and signs are
right, and it agrees with something the code did not produce. Call that
*scientific correctness*. Cairn has no doctrine for it. Review lens 8
(`doctrine/dual-review.md:386`) asks that methods be "grounded and documented",
and stops there. Issues #18 and #19 ask Cairn to fill the gap. They carry
fold-back candidate #59 and gap G11, a label the guide star's 2026-08-11
fold-down removed; the gap itself survives (line 278).

**Structural checks cannot reach it, because a model can be internally
consistent and physically wrong:**

* *Units.* Enter a recharge array in inches per year, in a model built in feet
  and days. The budget still closes, because the solver balances whatever
  fluxes it is given.
* *Calibration.* In steady state, heads alone often constrain little more than
  the ratio of recharge to conductivity. Double both and the fit barely moves.
  A flux observation, such as gauged baseflow, breaks the tie.
* *Signs.* Reverse the stream–aquifer exchange term and gaining reaches become
  losing ones. If the test was written from the same reading of the
  convention, code and test agree, and the budget still closes.

In each case the code, its tests, and a reviewer reading both all agree.
**Agreement establishes consistency, not correctness**
(`dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md:224`,
"the guide star"). Correctness needs a check whose expected value comes from
*outside* the implementation. The guide star asks for "one well-chosen
acceptance check, not another standing round" (line 232). It calls that "the
cheap first step" (lines 278–282).

**It has happened in a Cairn deployment.** LHM's plan
`stor-modflow-correctness` (archived 2026-08-28) relied on one independent
check: the unsaturated-zone residual against the model's own `unsatStorage`.
That array had never been saved, because it exceeded the MAT v7 size limit.
So at plan revision the check was replaced by a closed-mass test on synthetic
data, which holds by construction. The pipeline then "passed every test written
against it, and still had its unsaturated time axis wrong throughout". An
independent code review caught it by reading the as-executed model source. The
fix moved domain-mean storage by +14.75 kg m⁻², about 15 mm of water. Its
author drew one lesson: withdrawing an acceptance criterion should oblige
naming what now covers the same ground.

**What exists today** (each item a grep, re-run against a known hit):

* `dimensions/complexity.md:37` promises a complex project "a
  **scientific-trust review lens**". No module in the I-5 gate table
  (`bootstrap/BOOTSTRAP.md:96`) installs one. The phrase recurs only at
  `dimensions/README.md:29`, at `bootstrap/BOOTSTRAP.md:65`, and in a note in
  the architecture-review rubric, a whole-system review selected for accreted
  architecture rather than by complexity. **The promise points at nothing.**
* The readiness report (§11) and `docs/solo-legacy-recipe.md:112` ask adopters
  to write their assumptions down. Nothing tests a change against an
  independent basis.
* Security preflight S2 (`dev/proposals/_template.md:194`) names this failure,
  but only for security. The four disciplines the issues name exist, as
  disciplines, only in LHM's strategy note. The governance axis #19 would
  reframe is not in `dimensions/` at all; it is an unbuilt idea (guide star
  line 1136).

## Proposal

**The first step: each scientific change names one independent scientific
check.** This is no new axis, module or review round. It is four edits, and the
plan settles their wording.

1. **Proposal template** (`templates/core/dev/proposals/_template.md` and twin
   `dev/proposals/_template.md`). Add a gated block under *Evidence /
   verification plan*, shaped like the security preflight. Draft:

   > **Independent scientific check.** *Gated to a change that touches a
   > scientific assumption, or a result the project publishes or acts on.
   > That includes a governing equation, a unit or sign convention, a boundary
   > condition, a parameter default, a calibration setup, or a coupling
   > between models. Otherwise write "N/A: no scientific assumption or result
   > touched".* Name **one** check that could show the change is wrong about
   > the world, not only about itself:
   >
   > * **What it compares**: the quantity, the expected value, and the
   >   tolerance with its source.
   > * **Why the expectation is independent**: neither the proposed code nor a
   >   test written from the same understanding computes it. Its basis is an
   >   analytical or manufactured solution, a conservation law chosen against
   >   the error this change risks (a closed budget does not catch a wrong
   >   input), a trusted observation or benchmark, or a domain expert's
   >   expectation written down before the result is seen.
   > * **The error it would catch**: the plausible mistake (a reversed sign, a
   >   unit slip, a misplaced boundary) under which the check fails. Code
   >   review confirms that it does.
   >
   > If no independent basis exists, say so. The Maintainer weighs that at the
   > Decision; it is not a reason to invent one.

2. **Plan template** (`templates/core/dev/plans/_template.md` and twin),
   *Acceptance criteria*. The check becomes a criterion. Any replacement for
   it needs an independent basis too, or the plan says plainly that the result
   now rests on the implementation alone. When the check fails during
   implementation, one line records whether anything else would have shown
   the error. **This sentence answers the LHM incident.**
3. **Doctrine.** Lens 8 of `doctrine/dual-review.md` gains *agreement is not
   correctness*. Reviewers who agree, or a test written from the code's own
   understanding, establish consistency. So the reviewer confirms that the
   check's basis lies outside the implementation. At code review, the reviewer
   also confirms that the check fails under its named error.
4. **Make the existing promise true.** Repoint `dimensions/complexity.md:37`,
   `dimensions/README.md:29` and `bootstrap/BOOTSTRAP.md:65` at the check and
   lens 8. No axis, value or gate-table row changes.

**Who does what.** The author names the check. The Maintainer judges it at the
Decision, in their own scientific terms. The External reviewer challenges its
independence. Code review shows it failing under the named error. Hydrology
examples: a pumping well against Theis; stream depletion against
Glover–Balmer; an inversion that must recover a synthetic truth; recharge sent
equalling recharge received across a coupling seam, per stress period.

**Later work, recorded, not built.** The `deliverable` axis, its other three
disciplines and the governance reframe are revisited at the outside adoption
the guide star requires (line 66), or at ten real (non-N/A) checks across two
projects, whichever comes first. Those records supply what the axis lacks:
which bases recur for which kind of project.

## Rationale

* **It puts the Maintainer's domain attention where only they can give it.**
  Today science routes through the human reading everything. Here they answer
  one question in their own terms: is this the right check and expected value?
* **It is restrained, and triggered per change.** It costs a paragraph on a
  scientific proposal and a line elsewhere; the serious rival is lighter
  practice (guide star line 59). modflow_tools is mostly tooling, but its
  calibration work touches results, so a per-project switch would miss it.

## Alternatives considered

* **The whole `deliverable` axis now** (the strongest alternative): eight
  characters, four disciplines and the governance reframe, as both issues
  describe. It loses on four counts. *Evidence:* it would be designed from N=2
  under one Maintainer, which #19 itself calls "not enough to design the full
  value set from". *Substance:* none of its disciplines is prototyped. *Cost:*
  a seventh axis edits the engine's axis table
  (`bootstrap/_scaffold/config.py:1274`), the fidelity manifest's six-axis
  profile (an install contract), the presets and the AST baseline, so it is a
  Security-Review surface. *The guide star's own gate:* "Before any further
  expansion: one small outside adoption" (line 66). The check is the core every
  character shares, so the axis inherits it rather than undoing it. *What would
  change my mind:* checks coming back N/A, or resting on Maintainer judgment,
  because authors cannot tell which basis fits. That argues for presets sooner.
* **Gate the block on complexity** (a `cairn:if` block). It drops the check
  silently on a mis-scored project, and buys little: most scientific software
  is complex anyway (`dimensions/complexity.md:52`).
* **Prove-then-fold in LHM first** (the issues' stated path). That is right
  for the domain disciplines, which is why they wait. The check has no domain
  content to prove: its bases are generic verification-and-validation
  categories (Anchor 15, guide star line 1241). Its failure has already
  occurred in LHM, and LHM pilots it at its next upgrade.
* **A standing domain-review round**, as in USGS's two-review release. That
  breaks one-round review, and a solo project cannot staff it. The
  Maintainer's Decision is already the domain half; the check gives it
  something falsifiable to judge.
* **Do nothing.** The LHM failure can recur unasked, and `dimensions/` keeps
  promising a lens nothing installs.

## Documentation / doctrine surface

These are governing-layer edits (doctrine, templates, `dimensions/`), routed
per `docs/DOCUMENTATION_PLAN.md`. At archive they also update the guide star's
open-gap entry (line 278) and add a CHANGELOG line. No `docs/` page changes.
**Kernel surfaces:** `doctrine/dual-review.md`, plus prose in one axis
position, one matrix row and one bootstrap sentence. Two proposals opened the
same day (`2026-10-17-claude-maintainer-attention`,
`2026-10-17-claude-verification-practice`) edit other sections of the plan
template and `doctrine/dual-review.md`; whichever plan lands second rebases.

**The doctrine rate-limit gate** (`doctrine/rationale.md:405`). One incident
would not clear it; the case rests on the gate's synthesis route, several
signals folded into one proposal. LHM's fold-back review raised the gap
(2026-06-05, row #59). The guide star's 2026-10-01 revision (`77bdcbc6`) folded
in an External assessment and added this one-check form. The LHM incident shows
the failure occurring. And the shape recurs outside science: S2 names it, and
LHM's `cedar-creek-test-dataset` plan found a mutation no test killed because
every manifest was internally consistent.

The fold-back harvest (`doctrine/rationale.md:451`) is a standing routine. The
reviewer should test whether it is the gate's "routine boundary". Cairn's own
trackers could never record this incident, because Cairn computes no science.
**Fallback** if the gate is judged uncleared: land edits 1, 2 and 4, and hold
the lens-8 sentence for a second recorded scientific incident.

## Evidence / verification plan

**Done when** both template pairs match outside their slots, lens 8 states the
rule, and the three promise sites name the check. The gates must pass with no
vendor named in any template: `scripts/claim_check.py` on each touched file,
`python scripts/check_cairn.py`, and
`python scripts/quality_gate.py --sub neutrality --sub redundancy`. The first
real use, in LHM or modflow_tools, is the guide star's "worked example" (line
1302).

**What would falsify it.** At the revisit point, a short retrospective reads
the check blocks, code reviews and one-line records. The step is wrong if:

* **F1. It catches nothing a careful scientist would have missed.** Every
  failing check's record names something else that already showed the error:
  an existing test, a crash, an obviously unphysical output, or the
  Maintainer's own flag.
* **F2. It relabels existing practice.** Most bases are "the Maintainer's
  expectation".
* **F3. N/A is the escape hatch.** Assumption-touching changes carry N/A.
* **F4. The checks cannot fail.** Code review rarely shows them failing under
  their named errors.

If nothing fails and no later error surfaces, the result is inconclusive, not
a pass.

### Tests required

These tests read the changed files, found by grep; the plan maps them.

* **The templates** are read by twelve files. One is
  `bootstrap/tests/test_scaffold.py`, whose security-preflight slice must not
  swallow the new block. Another is `test_scope_reduction_trap.py`, which runs
  over both twins.
* **`doctrine/dual-review.md`** is read by three: `test_loop_fidelity_gate.py`,
  `test_onboarding_review_tiers.py` and `test_presets.py`.

**One new test**, named for the property it pins, holds the block and the plan
sentence word-for-word identical across the twins. Test bytes change, so
**Boundary B runs the full suite** under Python 3.13.x.

### Examples / smoke checks

`python bootstrap/scaffold.py --summary --config <profile>` and `--dry-run` show
the block installing.

#### Security preflight — five questions, answered in writing

N/A: no trust boundary added, moved, or widened.

## Signals the change is wrong

* **Checks written after the code**: the expected value shifts at code review
  to match the result.
* **The gate misfires**: result-touching changes carry N/A, or tooling changes
  carry a ritual check.
* **Reviewers cite the check** to prescribe a "domain round".
* **The block grows discipline sub-lists**: the axis arriving by accretion.

## Scope delta

**Scope delta**: preserved. This is the opening scope; the wider vision in #18
and #19 was never accepted scope, and is deferred to a named revisit point,
not conceded.

## Assurance path

**Assurance path**: high-assurance. It touches the authoring templates and
`doctrine/`, both mandatory high-assurance surfaces.

## Questions for the Maintainer

1. **Does the evidence clear the doctrine rate-limit?** *Recommended: yes.*
   One occurred incident plus the synthesis backs a one-sentence edit. If not,
   edits 1, 2 and 4 land and the lens-8 sentence waits.
2. **What happens to the issues when this lands?** *Recommended:* close #18
   with a pointer, since its ask is met in narrow form. Keep #19 as the home
   for the axis, the other disciplines and the governance reframe. #18's
   export-safety affirmation stays yours either way.
3. **When do we revisit the axis?** *Recommended:* at the outside adoption or
   at ten real checks across two projects, whichever comes first.

## Review -- Claude Opus 5.5 (External, fresh session) -- 2026-10-17

```
Reviewed commit: 57dbce3b9706d05dd48200e5b53486997e6e327e
Target: the complete proposal (Context through Questions for the Maintainer), checked against issues #18 and #19, the tree at the reviewed commit, and the LHM plan records the Context cites
Prior findings: none
Assurance path: high-assurance
```

**Tier**: External
**Findings**: raised (3 blocking, 4 non-blocking)
**Verdict**: REVISE

Distance: a fresh session of the author's agent type, not a different type.

### In plain terms

This should happen. Asking each scientific change for one check whose expected
answer comes from outside the code is cheap. The guide star already calls it the
first step, and the proposal template carries it to every adopter. Deferring the
`deliverable` axis is right.

Three things are wrong as written. First, the LHM incident at the centre of the
proposal is a different failure from the one it describes. The plan-template
sentence said to "answer" it would not have changed the outcome, because the LHM
plan already said, almost word for word, what that sentence asks for. Second,
the reviewer's half of the rule goes into files adopters never receive. The
rewritten promise in `dimensions/` would point at a review list that a solo
scientist working with one agent does not get. Third, the case for clearing the
rule that stops doctrine changing on one incident uses a route that does not
fit. A route that does fit exists, but it supports a narrower claim. Each fix
takes a few sentences.

### Evidence read outside this repository

The LHM records are checked out on this machine, and I read them directly
rather than relying on the Context's summary.

External-repo paths: `dev/plans/archive/stor-modflow-correctness.md`, `dev/plans/archive/cedar-creek-test-dataset.md` (both in the LHM repository)

- `dev/plans/archive/stor-modflow-correctness.md:564-590` -- the unverified claim that the data existed; the withdrawal of criterion 4; "rests on the faithfulness of the port"
- `dev/plans/archive/stor-modflow-correctness.md:884-887` -- the code review tying both errors to the withdrawn check
- `dev/plans/archive/stor-modflow-correctness.md:1037-1052` -- the author: both errors were accepted plan items, not implemented
- `dev/plans/archive/stor-modflow-correctness.md:1146-1172` -- size and sign of the correction
- `dev/plans/archive/stor-modflow-correctness.md:1220-1229` -- the archive lesson
- `dev/plans/archive/cedar-creek-test-dataset.md:1833-1841` -- the mutation no test killed (2026-09-29)

The proposal's quotations from these records are accurate. Every Cairn-side
citation resolves at the reviewed commit. Two claims hold: no module in the
I-5 gate table installs a "scientific-trust review lens", and `dimensions/` has
no governance axis. All the guide-star lines cited say what the proposal says
they do.

### The proposal at its strongest

A model can be wrong about the world and still agree with itself. Reverse a
sign, and the code, a test written from the same understanding, and a reviewer
reading both will all pass it. Structural review cannot break that tie. Only an
expected value from outside the shared understanding can. One such check per
scientific change, shown to fail under the mistake it names, gives the
Maintainer one falsifiable question in their own field instead of a reading
load. It needs no axis, no engine change and no new round. It puts the guide
star's existing principle (guide star lines 223-232) at the front of the
template, and the axis can inherit it later.

I could not break that core. The list of bases is standard verification and
validation. "A closed budget does not catch a wrong input" is the right
warning. F1-F4 are honest falsifiers, and "inconclusive, not a pass" is correct.

### Findings

**[SC1] (blocking) The LHM incident is not the failure the Context describes,
and edit 2 would not have changed it.** When the LHM plan withdrew its check,
it wrote that the unsaturated term now "rests on the faithfulness of the port,
not on agreement with the model". That is edit 2's escape ("the plan says
plainly that the result now rests on the implementation alone"), met in
advance. The error still reached code review. So "This sentence answers the LHM
incident" is false on the record the proposal cites. The record also shows
three things the Context leaves out:

* **The errors were plan-to-code drift.** They were not a misunderstanding
  shared by the code and its tests. Both were Blocker items (priming the stack,
  the RAMP shift) that the plan's own Round-1 response had accepted. The
  implementation then left them out.
* **A structural check caught them.** An External code review compared the
  code with the accepted plan and the model's as-executed source, and it did
  so before archive. That is a counterexample to the headline "Structural
  checks cannot reach it". Here one did, later and at higher cost than the
  independent check would have.
* **The check was lost through two gaps that edit 2 does not touch.** The
  source proposal said the reference data existed. Across three responses
  nobody checked, and the array had never been saved. The withdrawal then
  happened at plan revision, after the Decision, with only an Internal plan
  reviewer. That is later than the point where the proposal has the Maintainer
  judge the check ("at the Decision").

The LHM author's own lesson names the fix: replace a withdrawn check's
*coverage*, not just its *claim*. Satisfier, in three parts:

* (a) **Edit 2.** A replacement must fail under the named error of the check
  it replaces, which is the block's own third field. The closed-mass test on
  synthetic data would not qualify, because it cannot fail under the priming
  or calendar errors that code review found. When nothing qualifies, the loss
  is a removal under the plan template's existing Scope-delta rule. That rule
  treats accepted scope as a floor and requires the Maintainer's quoted
  allowance. One line from the author would no longer settle it. This is
  lighter than a new rule, and it sends the decision to the person the
  proposal says judges the check.
* (b) **Edit 1.** "What it compares" states that the expected value's data is
  in hand and has been checked. Otherwise it says the check depends on data
  that does not exist yet, so the Maintainer sees that at the Decision. LHM's
  check rested on exactly this unchecked claim.
* (c) **Context.** Describe the incident as it happened: one occurred loss of
  an independent check, caught later by structural review. Fix the sign too.
  The record's +14.75 kg m⁻² is pre-fix minus corrected, so the fix *lowered*
  domain-mean storage by 14.75 kg m⁻². The full-series mean went from +13.5
  to -1.2, and +14.91 of the change is the cold-start priming offset. In a
  proposal whose lead example is a reversed sign, this sign should be right.

*Closed by:* the Response walks revised edits 1 and 2 through the LHM record
and shows where each would have stopped the withdrawal.

**[SC2] (blocking) The reviewer's half of the rule goes where adopters never
read it, and the repointed promise repeats the defect it fixes.** Edit 3
changes `doctrine/dual-review.md`. Adopters do not receive `doctrine/`. This
repository's own test says a rule that lives only there "binds nobody who
adopts Cairn" (`bootstrap/tests/test_scope_reduction_trap.py:3-5`). The lens
list adopters do receive is a copy inside the `dual-review` module
(`templates/modules/team-gated/dual-review.md:66`, self-hosted at
`dev/modules/dual-review.md:65`). That module installs only for a concurrent
multi-type agent team (`bootstrap/BOOTSTRAP.md:152`). Three consequences:

* **No adopter receives the new sentence.** As written, "agreement is not
  correctness" reaches nobody. That includes LHM and modflow_tools, even though
  both install the module.
* **The solo scientist gets half the rule.** A solo scientist with one agent
  type, the user the guide star's "serious alternative" describes, gets the
  template block but no instruction to the reviewer about independence.
* **The repointed promise is still false.** Edit 4 repoints the complexity
  promise at "the check and lens 8". The agent-team axis installs lens 8, not
  the complexity axis. So the complexity axis would still promise something it
  does not install, which is the original defect.

This also inverts the fallback. Holding back the lens-8 sentence withholds the
one edit adopters never receive, while the template block, which every adopter
must absorb, still lands. Edit 4 lands under the fallback too, although the
proposal template's own triage lists `dimensions/` with doctrine.

Satisfier:

* **Ship the reviewer duties in the block.** The block is core and reaches
  everyone. It should say that the External reviewer challenges the basis's
  independence and that code review verifies the check fails under its named
  error.
* **Keep the lens copies together.** If lens 8 changes, change all three
  copies and pin them together, the way `test_scope_reduction_trap.py` already
  pins the scope-reduction rule.
* **Repoint the promise at the check alone.**
* **Plan note.** Changing the module's merged text sends an adopter whose slot
  is customized to a merge-pending side file on upgrade. The plan should say
  so.

**[SC3] (blocking) The rate-limit case uses a route that does not fit, and the
route that does fit supports a narrower claim.** The gate defines synthesis as
the session-close routine owner pooling a period's signals into a single stub
at a routine boundary (`doctrine/rationale.md:414-417`). This proposal is a
Strategy opening, written the same day as two others. It is not a goodnight
synthesis. Of its four signals, only one is an occurred incident. The fold-back
row and the guide-star revision are assessments of a gap. The fold-back harvest
(`doctrine/rationale.md:451`) is a different loop: it records a gap as a
fold-back, which then enters the proposal cycle, and nothing in it says a
harvest finding clears the gate. So, to answer the proposal's invitation
directly: no, the harvest is not the gate's routine boundary.

**Recurrence** is the route that fits. The same shape occurred twice in LHM,
about a month apart: a check that could not fail under the error that mattered.

* **stor-modflow (2026-08-27).** The replacement test could not fail under
  the errors that code review later found.
* **cedar-creek (2026-09-29).** The per-member digest check "at first failed
  none" under mutation, because every test's manifest was internally
  consistent.

Both are the generic shape. Neither is a physical misunderstanding shared by
code and tests. Recurrence therefore clears the half of the block that the
record supports: name the error, and show that the check fails under it. That
half is S2 (`dev/proposals/_template.md:194-197`) extended beyond security.
The other half, the independent basis, is aimed at the shared-understanding
error in the Context's units, calibration and sign examples. The record has no
occurred instance of that error. That half rests on the guide star's argument
and the V&V literature.

Satisfier:

* **Restate the case.** Argue the gate on recurrence, citing both occurrences,
  and drop the synthesis claim.
* **Say what rests on argument.** State plainly that the independent-basis
  half rests on argument, not on incidents.
* **Choose a path for that half.** Either ask the Maintainer to accept it on
  those grounds, which is their call, or land it as template guidance that
  claims no doctrine weight.
* **Replace the fallback** (see [SC2]).

**[SC4] (non-blocking) The list of independent bases leaves out the basis the
incident actually used.** The check LHM lost compared the post-processor with
the model's own saved state. That is a reference implementation. It is not an
analytical solution, a conservation law, an observation, or an expert's prior.
For tooling, post-processing and coupling code (most of modflow_tools and much
of LHM) it is the most common basis there is. An author who cannot find their
basis in the list will write N/A or "the Maintainer's expectation", which are
the proposal's own failure signals F2 and F3. *Satisfier:* add "an independent
implementation, or the output of the model the code reads". Note that such a
basis is independent of the port, not of the model's physics.

**[SC5] (non-blocking) The implementer should demonstrate the failing check and
record it; the reviewer verifies the record.** Edit 3 and "Who does what" have
the code reviewer "confirm" or "show" that the check fails under its named
error. For a full LHM run, re-running that is not a reviewer's job: `AGENTS.md`
keeps verification with the implementation and its recorded evidence, and says
a reviewer "is not a second implementer". S2 already has the right form, where
the author states the mutation and confirms they ran it. *Satisfier:* the
implementer records the deliberate break and the check's failing output. The
code reviewer verifies that record and re-runs it when cheap.

**[SC6] (non-blocking) The revisit point has no trigger.** Nobody keeps the
count "ten real (non-N/A) checks across two projects". `AGENTS.md` says a
check whose only trigger is a human remembering must be described that way.
*Satisfier:* name what keeps the count, for example #19 kept open with a
running tally, or the roadmap scrub. Otherwise, say that the revisit depends on
the Maintainer remembering.

**[SC7] (non-blocking) The proposal applies the guide star's gate to its rival
and not to itself.** It defers the axis partly on "Before any further
expansion: one small outside adoption" (guide star line 66). But the guide
star's list of candidate moves says "None is queued. One gates the rest", and
it puts the worked example behind that gate (lines 1297-1305). This proposal
names the worked example as its own first real use. I think the proposal is
defensible: line 282 names the one-check form as the cheap first step for an
open gap, and a gated paragraph is not a new layer of apparatus. But the
proposal has to make that argument rather than leave it unstated.
*Satisfier:* add one sentence on why a template block is not "further
expansion", for the Maintainer to accept or reject.

### Verdict, strongest alternative, falsifier

**Should it happen?** Yes, revised per [SC1]-[SC3]. The check is the right
size. Doing nothing leaves a false promise in `dimensions/` and a failure
shape that has already occurred twice.

**The strongest rejected alternative** is not the whole axis. It is **ungating
S2's "Can it fail?" so it applies to every acceptance check**. That is a
one-sentence change that reuses a question Cairn already ships, and it would
have caught both occurrences the gate can count. It loses on substance. S2 asks
whether a check takes its expected value from the *same object* it checks.
A sign-reversed test can fail under mutation and still share the code's wrong
convention, and only an independent basis reaches that error. So keep the
block, but have it say that its "fails under the named error" half is S2
generalized, because that half is where its evidence lies ([SC3]).

**Deferring the axis is right.** It is not narrowing that drops accepted
scope. #18 and #19 are issues, and an issue is not accepted scope. Both issues
prescribe prove-then-fold, and #19 says N=2 is "not enough to design the full
value set from". A seventh axis would also reach the engine's axis table
(`bootstrap/_scaffold/config.py:1274`). What waits is three disciplines and the
governance reframe, and #19 keeps them.

**What would falsify the central claim.** The claim is that one named
independent check catches what structural review misses, and catches it
earlier and more cheaply.

* **A test that can run now.** Apply the revised block retroactively to LHM's
  archived scientific plans. If authors following the template would not have
  named a check that fails under the error code review later found, the block
  is ritual. As drafted, the block fails this test on stor-modflow ([SC1]).
* **At the revisit point.** F1-F4 stand, with one addition. If failing checks
  keep coinciding with errors that code review also catches, the block buys
  time, not coverage. That is still worth having, but it is a smaller claim
  than the Context makes.

### On the Questions

* **Q1.** Not by the route the proposal argues. Recurrence clears it, for the
  half of the block that the record supports ([SC3]).
* **Q2.** Close #18 as a duplicate of #19, not as "met". Three of #18's four
  disciplines and both of its sub-threads remain open.
* **Q3.** Agreed, once the trigger is named ([SC6]).
