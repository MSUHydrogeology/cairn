# Plan: Fault-centered testing

**Source proposal**: dev/proposals/archive/2026-11-02-codex-fault-centered-testing.md
**Status**: ready-to-archive
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
satisfied without running their check. The independent ordinary code reviewer
applies the prompts to both changes and records both trials in the existing
code review; this adds no review stage. Assess the outside-practices strategy's
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

## Plan review -- Codex Terra (MEDIUM) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. The plan preserves optional tools and prompts, required checks, independently grounded examples and the strategy's architecture disposition -- accepted proposal, Proposal 1-6 and Decision; plan, C1-C3.
2. **Best alternative.** Reuse the scientific-minimal example and existing module and boundary tests, as planned; a new framework adds maintenance without supplying an independent expectation -- `examples/scientific-minimal/test_water_budget.py`; plan, Reuse.
3. **What would show it wrong?** A balanced wrong input passing the purported independent check, or a candidate-derived expectation accepted as independent, would defeat the example -- accepted proposal, FT-1 response; plan, C2.

Reviewed commit: ed2a4ee7ad6a440998103ae51079ce2284aeb99f

**Obligation**: Internal
**Tier**: Internal
**Findings**: one non-blocking recommendation
**Verdict**: SHIP

**Assign the prompt trials.** The accepted proposal asks a reviewer to apply the prompts to a scientific change and an ordinary defect; C2 requires the applications but does not name the reviewer. Specify that owner in the existing review or evidence sequence so both trials are recorded, without adding a review stage -- accepted proposal, Examples / smoke checks; plan, C2-C3.

The independent numerical basis must precede results; a passing conservation check alone is not that basis. The declared separate Security plan review and wide final Boundary B remain owed.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

**Coverage**: Committed plan, accepted proposal, reviews, response and Decision, plan template, scientific example, module wording and named test triggers. **Not covered**: future examples or numerical validity, all readers, Security Review, test runs and full suite.

## Plan review -- Codex Sol (HIGH) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. C1-C2 retain all six accepted outcomes: trusted behavior, discriminating properties, targeted mutations, honest failures, observable criteria and test-first examples -- accepted proposal, Proposal 1-6/FT-1 response/Decision; plan, C1-C3.
2. **Best alternative.** Extend scientific-minimal, existing module tests and acceptance cells, as planned. A new framework, mandatory tool or criteria parser adds maintenance without supplying an independent expectation -- plan, Reuse/C1; accepted proposal, Alternatives and Proposal 5-6.
3. **What would show it wrong?** A balanced wrong input must pass conservation yet fail the independently grounded check; candidate-derived expectations and unexecuted acceptance checks must be rejected -- plan, C2; `examples/scientific-minimal/test_water_budget.py::TestMassBalanceInvariant`.

Reviewed commit: ed2a4ee7ad6a440998103ae51079ce2284aeb99f
Ordinary review read: 7f98d941.

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT -- plan only.

C1 preserves all-members mutation duties without a Cartesian-product or
per-function quota. Surviving mutations require investigation against confirmed
expectations, not frozen candidate output. Human confirmation remains for
reported faults, not every discarded candidate or ordinary change. Optional
properties, tools and EARS prompts create no grammar parser or waiver of
scientific, security or release checks.

The existing selected-module test calls the real scaffold; preservation and
mirrored-module guards have concrete test homes. Their success cannot establish
scientific validity. The current water-budget fixture is constructed to balance;
C2's predeclared independent basis and unmodified/fault runs are therefore
substantive evidence, not replaceable by another conservation assertion.

Bohr's prompt-trial ownership recommendation remains for the author to dispose
of within the existing sequence, not a new review stage. C2 also retains the
strategy's architecture disposition; testing alone cannot retire it. The
standard-tier Decision does not erase this separately declared Security plan
obligation. C3 retains both code reviews before wide Boundary B.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed plan, ordinary review, accepted source/reviews/response/
Decision, current review template, module overclaim, scientific example and
actual install/preservation/parity/boundary test bodies. **Not covered**: future
examples, numerical validity, exhaustive reader mapping or prompt-trial outcomes.
No implementation tests or suite run; shared mistaken assumptions remain possible.

## Author response -- Codex LunaLOW -- 2026-11-04

Accepted Terra's nonblocking recommendation: the C2 ordinary code reviewer
owns both prompt trials and records them in the existing code review. This
assigns the accepted work without adding a review stage or pass. Both required
plan-review obligations match and accept the plan; no other findings remain.

**Status**: ready-to-implement. Implementation follows after this transition.


## Implementation log -- Codex (High) -- 2026-11-05

Sources: `b30adff0`, `bef11a3f`, `212be448`, `6b1785d3`, `05f4659f`,
`7d675b81`. The last repair names the optional dual-language module without a
location-dependent link in both copies. Their guidance is identical; no
assertion was relaxed. The real installation and parity nodes both passed
in 0.11 seconds on a matching Git-backed candidate, Python 3.13.13.

C2 scientific basis was declared before the fault results: synthetic depths
P=100, ET=30, runoff=20 and recharge=40 mm imply dS=10 mm by the stated
balance. `TestResidualWriter::test_compute_residuals_preserves_independent_inputs`
in `examples/scientific-minimal/test_water_budget.py` calls the real producer
and checks literal P=100 and dS=10. This is an independent input-preservation
check, not observational evidence, general physics validation or an invented
historical production bug; exact synthetic integers need no float tolerance.

Boyle's Medium execution report for `212be448` used Git-backed copies:
391 affected checks passed before and after the exact example patch. With
output P and dS each increased by 10, stored/recomputed closure remained zero
and the old six checks passed, but the independent check failed. Separate P
and dS faults each failed the reference assertion. A greeting producer ignoring
the name failed the named case while its default case passed; pristine examples
then passed all nine cases, including a clean committed replay. These are
controlled test-first demonstrations; the final affected run rechecks both
example files. Failed mutant outcomes are evidence, not green test totals.

Outside-practices testing and acceptance recommendations now have guidance and
examples. Architecture remains in the accepted architecture/reuse plan; the
strategy and grouped retirement row 12 stay live. Bohr still owns both
independent scientific/ordinary acceptance-prompt trials in the existing code
review; no extra review stage is added.

Superseded attempts remain non-final: `b30adff0` had 1,776 passed/8 failed;
`bef11a3f` 1,792/1; `6b1785d3` passed 1,793 but failed the separate link gate;
`05f4659f` had 1,792/1 after its link repair broke parity. No partial pass enters
the final green union. Full Boundary A, code reviews and Boundary B remain owed.

**Elapsed**: approximately 5 minutes recording; execution timings belong to
the cited run reports. **Tokens**: unknown.

## Implementation verification -- Codex Luna (Implementation verification executor, LOW) -- 2026-11-05

**Boundary A**: passed for the six source pairs and final implementation commit recorded in the Security Review pass-limit plan's `## Implementation verification -- Codex Luna (Implementation verification executor, LOW) -- 2026-11-05` section. That section contains the full changed-path inventory (including every pair's `CHANGELOG.md`), per-pair selector results and guarded omissions, commands, reports, clean-state evidence and non-pass disposition. Its final union is 1,793 unique pytest node IDs: 1,662 in the first segment and 131 in the disjoint supplement. The scientific water-budget and ordinary greeting examples were included in the first segment; the changed changelog was included in all applicable prose gates. No total includes an earlier failed attempt.

The nine example cases and affected checks establish controlled test behavior, not scientific truth. C2's independent ordinary code reviewer still owns the scientific and ordinary acceptance-prompt trials; Boundary B, both code reviews and those trials remain outstanding. No full suite or certification was run.

**Tested commit**: `7d675b815954ec2fe2c6e88184e51321d4da53d6`. **Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13. **Pre-run state** and **Post-run state**: clean Git-backed clone at the tested commit. **Non-pass disposition**: no non-passes in final A; 28 AGENTS readers were omitted by the documented selector guard. **Tokens**: unknown.

**Boundary B mode**: not run; pending code reviews and parent authorization.

## Code review -- Codex Terra (MEDIUM) -- 2026-11-05

**Foundations**

1. **Should this happen as framed?** Yes. The shipped and self-hosted guidance keeps tools and EARS optional, distinguishes independent expectations from characterization and retains honest failures -- `dev/modules/testing-discipline.md`; both plan templates; accepted proposal, Proposal 1-6.
2. **Best alternative.** Reuse the existing examples and test homes, as implemented; a new framework cannot provide an independent expectation -- `examples/scientific-minimal/test_water_budget.py::TestResidualWriter`; `bootstrap/tests/test_practice_modules.py`.
3. **What would show it wrong?** A balanced producer mutation passing the independent input check, or an ignored greeting argument passing the named expectation, would falsify the examples -- implementation log; `examples/minimal/test_greet.py`.

Reviewed source: `b30adff0`, `bef11a3f`, `212be448`, `6b1785d3`, `05f4659f`, `7d675b815954ec2fe2c6e88184e51321d4da53d6`; source-pair ranges and iteration evidence at `c06d69ca`. Status: `617080fe3`.

**Tier**: Internal
**Bounding**: ACCEPTED
**Findings**: none
**Verdict**: ACCEPT

**Prompt trials.** Scientific: given synthetic P=100, ET=30, runoff=20, recharge=40 mm, preserve P=100 and dS=10; unchanged, the stated balance closes. The real producer's independent literal-input check fails the reported paired output fault even though closure and six old checks pass. This is input preservation, not physical validation. Ordinary defect: when a name is supplied, return `Hello, Ada!`; unchanged, the default returns `Hello, world!`. The reported named test fails an ignored-name mutant while the default passes. I reject deriving the expected values from the candidate output, and reject an acceptance criterion that claims success without executing its named check.

Boundary A reports 1,793 distinct passes; earlier failures remain recorded, not included. Separate Security review and final wide Boundary B remain owed.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed source, accepted proposal and plan, test and installed-output guard bodies, worked-case and final iteration records; trials apply the optional prompts to the two recorded examples. **Not covered**: independent execution of mutants or suite, real-world scientific validity, Security Review or Boundary B.

## Code review -- Codex Sol (HIGH) -- 2026-11-05

**Foundations**

1. **Should this happen as framed?** Yes. All six accepted outcomes remain: trusted expectations, optional properties, targeted mutations, honest failures, observable criteria and test-first contrasts -- module/template diff; accepted Proposal 1-6; worked cases and Bohr's prompt trials.
2. **Best alternative.** Extend the existing examples and guards, as implemented; another framework or criteria parser adds maintenance without an independent oracle -- scientific-minimal and greeting examples; both templates' optional prompts.
3. **What would show it wrong?** Actual guidance-file faults or an aliasing producer corrupting both input and output must fail their owning checks. Three controls passed and all five faults were caught -- `/private/tmp/cairn-sol-code56.nbJqIF/testing-probe.py` and `testing-report.json`.

Reviewed commit: 7d675b815954ec2fe2c6e88184e51321d4da53d6
Owned source pairs/inventory: c06d69ca, including b30adff0, bef11a3f, 212be448 and the three recorded repairs.
Worked cases: 8731e741; ordinary review/trials: ee623c62; submitted status: 17080fe3.

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Bounding**: ACCEPTED
**Findings**: none open; F6-1 closed
**Verdict**: ACCEPT -- reviewed source; final wide Boundary B remains owed.

**F6-1 closure:** the installed assertion now matches capitalization without
weakening its requirement. Final module copies are identical and name the
optional language module without a broken relative link. Python 3.13.13:
real installation and parity nodes passed, 2 in 0.12 seconds.

I mutated both module carriers and both plan templates on separate copies;
actual entry-point guards rejected each fault. In the real numerical producer,
shifting aliased input and output P/dS by +10 kept stored/recomputed closure
zero, yet the literal P=100 assertion failed. The predeclared
100-30-20-40=10 mm basis protects two synthetic quantities, not all fields,
observations or model physics. No tested mutation survived.

Bohr's existing-stage trials reject candidate-derived expectations and
unexecuted criteria. Tools/EARS stay optional; required checks and human
confirmation of reported faults remain. Final A reports 1,793 unique passes;
superseded failed runs contribute nothing to that total.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Frozen source/accepted contract, actual carrier/producer probes,
named fix, prompt trials and final A. **Not covered**: physical validity,
every possible fault, dishonest metadata, 28 guarded reader omissions or final
wide Boundary B. No mapped-suite replay or full suite; no new review stage.

## Boundary B pointer -- Codex High -- 2026-11-05

The [shared wide verification](2026-11-04-implementation-plan-completion.md#implementation-verification----codex-high----2026-11-05) on `573da3f4` passed 2,471 tests with one Windows-only skip;
both examples passed all nine cases. Both code reviews accept the source,
including the ordinary reviewer's two prompt trials. This is change evidence,
not scientific validation. No A totals were added. Elapsed is in the shared
record; tokens unknown.
