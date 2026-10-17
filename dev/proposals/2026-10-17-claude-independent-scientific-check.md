# One independent scientific check: the first step on scientific correctness

**Author**: Claude (Strategy)
**Status**: awaiting-review
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
