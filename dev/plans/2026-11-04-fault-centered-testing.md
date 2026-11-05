# Plan: Fault-centered testing

**Source proposal**: dev/proposals/archive/2026-11-02-codex-fault-centered-testing.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**Author**: CodexTerra (gpt-6.1-terra), ordinary plan author
**In brief**: Help scientists choose checks that expose plausible faults and criteria that describe observable outcomes.

## Source proposal

The accepted standard proposal joins meaningful scientific checks, honest
failures, optional acceptance prompts and test-first examples without a new
framework, mandatory dependency, review stage or test quota. Its declared
ordinary and Security plan-review obligations remain separate.

## Scope

Update `dev/modules/testing-discipline.md` and its shipped counterpart, both
plan templates, first-use guidance where needed, and `docs/methodology/plans.md`.
Reuse `examples/scientific-minimal/`, its water-budget tests and the existing
test homes. Shared core guidance for sequence items 4-6 has one writer,
Herschel; coordinate the editing and verification window without changing
plan 4. Testing owns functional scope versus runtime/cost; the accepted
architecture work owns its contrasting rubric examples.

**Reuse**: N/A: no new framework or project. The scientific-minimal example
and `bootstrap/tests/test_practice_modules.py` installation and preservation
checks, plus `bootstrap/tests/test_verification_boundaries.py` mirrored-module
and boundary guards, are existing homes; search their readers and near-duplicate
examples before extending them.

### Documentation / doctrine surface

Extend existing adopter and self-hosted guidance and acceptance cells, and
the published explanation; replace overlapping advice rather than add a form.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Map readers and fault coverage; revise testing and acceptance guidance in the shared writer window. | Both independent plan reviews and dispositions. | Mirrored guidance, optional prompts and focused guards. |
| C2 | Adapt existing examples, demonstrate failures and selected-module installation; assess strategy outcomes. | C1 | Worked evidence and strategy disposition assessment. |
| C3 | Obtain ordinary and Security code reviews, then wide Boundary B. | C2 | Recorded change evidence. |

## Acceptance criteria

**C1.** For scientific claims, identify trusted expected behavior and protect
it locally or through a real workflow; characterization records established
behavior, its source, units, tolerance and limits, not physical validity.
Candidate-derived values are not independent evidence. Explain optional
properties and analytical, manufactured or convergence checks where useful;
conservation alone can miss a wrong source and no selected checks prove general
correctness. Target mutations to relevant behavior and owning checks, retain
existing all-members obligations, investigate survivors against confirmed
expectations, and retain human confirmation of reported faults without routing
discarded candidates or ordinary changes to a person. Warn against weakening
assertions, tolerances, expectations, mocks or logic merely to pass; justified
expectation changes state the promise and independent basis. No universal
per-function rule or mandatory optional tool is added.

Both plan templates offer condition, observable behavior, unchanged behavior
and demonstrating check as optional prompts; EARS is optional. A defect example
names current, expected and unchanged behavior. Required checks remain required.

**C2.** Scientific and ordinary examples distinguish useful, vacuous and
broken checks and observe the intended failure before implementation. A
balanced-but-wrong input or compensating error passes conservation but fails
an independently grounded check; state its basis before results. Run the
unmodified and fault cases. Exercise selected-module installation via the real
scaffold and preservation via existing tests. Apply the prompts to a scientific
change and ordinary defect; reject candidate-derived expectations and criteria
satisfied without running their check. Assess the outside-practices strategy's
testing, acceptance and architecture recommendations: archive only when all
have delivered outcomes or explicit dispositions; testing alone cannot close it.

**C3.** Independent ordinary and Security code reviews precede wide Boundary B.
No syntax, coverage or reviewer agreement claims scientific truth; shared
mistaken assumptions remain possible.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: use `python tools/test_tiers.py for <changed paths>`, inspect
readers and pins with known-positive searches, run selected tests and claim,
link, snippet, neutrality and redundancy gates. Extend the existing practice
module and verification-boundary guards only for plausible uncovered faults;
exercise `test_modules_install_on_selection`, `test_skip_if_exists`, mirrored
module checks and the relevant scientific-minimal cases. Record each example's
expected basis and observed failure, including the independent check. Boundary C:
reviewers use targeted falsification, not a suite. Boundary B: wide after both
code reviews, on a clean final commit under canonical Python 3.13; include the
reviewed-range iteration selection, mapped integration/workflow consumers and
standing gates. Record SHA, range, interpreter, clean pre/post state, commands,
counts, elapsed time, non-passes and omissions. No full certification is implied.
