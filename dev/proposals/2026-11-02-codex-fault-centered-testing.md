# Make scientific tests and acceptance criteria catch meaningful faults

**Author**: Codex (runtime model identifier unavailable; Strategy)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy -- governing verification guidance and authoring templates
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Strengthen the existing testing module with trusted behavior checks, optional property and targeted mutation tests, and acceptance criteria that name observable outcomes.

## Decision summary

Scientists need tests that can reveal a wrong result, not just confirm what
an agent wrote. Improve the existing testing guidance and plan prompts
together. Add no new testing framework, mandatory dependency, review stage
or test-count target. The cost is maintaining a few clear worked examples
and preserving the distinction between scientific evidence and a green suite.

## Context

`templates/modules/team-gated/testing-discipline.md` covers regimes,
invariants, entry points, consolidation and benchmarks, but lacks explicit
expectation-laundering guidance. The plan template already has acceptance cells.

The [outside-practices study](../strategy/2026-11-02-claude-outside-practices-for-better-software.md)
proposes these additions. Its literature summaries are leads, not independent
validation by this author.

## Proposal

**1. Protect meaningful behavior.** For a function carrying a scientific
claim, identify trusted expected behavior and protect it through a local
check or a real workflow that exercises it. A characterization test records
established behavior; it is not proof that the behavior is scientifically
correct. State its source, units, tolerance and limitations. Do not generate
golden values from the candidate and call them independent evidence.
Unvalidated behavior stays explicitly uncertain.

**2. Add properties where they discriminate.** Explain optional property
tests that explore invariants across inputs, alongside analytical limits and
manufactured or convergence benchmarks where applicable. A conservation
check can pass with the wrong source term; pair checks with the plausible
faults they can actually detect. Replace the module's categorical claim
that conservation/convergence proves correct equation-solving: passing checks
support only their stated properties, not general correctness.
No optional library becomes an installed
Cairn dependency. No universal coverage percentage or test-per-function quota.

**3. Use targeted mutation carefully.** A mutation deliberately introduces a
fault to see whether a test notices. Start with relevant changed behavior
and its owning checks, not a Cartesian product of every token and the suite.
Existing all-members obligations still apply. A surviving mutation is a
lead, not automatically a bug or a request to freeze current output.
Confirm the expected behavior before changing tests or production code.
Preserve human confirmation of reported faults without sending every
discarded candidate or ordinary code change to a person.

**4. Preserve honest failures.** Explicitly warn against deleting assertions,
loosening tolerances, changing expected values, mocking the failing path or
leaving placeholder logic solely to make tests pass. A justified expectation
change states the changed promise and its independent basis. Use the
existing review and scope rules; introduce no separate policing process.

**5. Make criteria observable.** Add optional prompts to both plan templates:
condition, observable behavior, unchanged behavior, and the check that
demonstrates them. Offer the EARS-style sentence "WHEN condition THE SYSTEM
SHALL behavior" as an aid, not a required grammar or parser. A bug example
states current, expected and unchanged behavior. Extend the existing
acceptance cells; do not add another specification file or make checks optional.

**6. Demonstrate test-first.** Show useful, vacuous and broken checks for
scientific and ordinary changes. Include a balanced but wrong input or
compensating error, caught by an independently grounded check. Observe the
intended failure before implementation; distinguish established behavior
from physical validity. Reuse scientific-minimal; no new project.

## Rationale

Benefit: informative evidence with less redundant testing. Cost: example
upkeep and scientific judgment. Reuse existing records and modules.

## Alternatives considered

Doing nothing keeps good general guidance but leaves these specific traps
implicit. Requiring Hypothesis or a mutation platform adds dependencies and
triage obligations every adopter may not need. Separate acceptance-criteria
and testing programs would edit the same template contract twice; coordinate
them here.

## Documentation / doctrine surface

Update the shipped and self-hosted testing-discipline module, both plan
templates, their first-use guidance where needed, and the corresponding
published explanation in `docs/methodology/plans.md`. Replace overlapping
advice rather than append a checklist. Testing guidance owns functional scope
versus runtime/cost; architecture/reuse owns corresponding rubric examples.
Keep scientific, security and release checks and triggers unchanged.

The implementation's closeout also assesses the outside-practices strategy:
archive it only after testing, acceptance and architecture recommendations
all have delivered outcomes or explicit dispositions. A testing-only archive
cannot silently close the architecture work.

## Evidence / verification plan

### Tests required

Extend `bootstrap/tests/test_practice_modules.py` installation/preservation
coverage and `bootstrap/tests/test_verification_boundaries.py` guards only
for new promises. Exercise selected-module installation through the real
scaffold. Preserve mirrored template meaning and existing required-check
clauses. Worked examples must fail for the fault they claim to detect and
pass unmodified; record the expected basis before the result.

### Examples / smoke checks

Run claim/link and neutrality/redundancy gates. Have a reviewer apply the
prompts to one scientific change and one ordinary defect; reject an
expectation copied from the candidate and a criterion satisfied by not
running its check. This is change evidence, not an outside adopter trial.

#### Security preflight

S1: authors supply criteria and evidence; reviewers challenge them, and the
Maintainer owns scientific judgments. Neither field authorizes a waiver.
S2: no new executable truth checker is proposed. Implementation must show
worked examples rejecting a weakened check; that experiment is not yet run.
S3: existing author/reviewer stages apply the guidance to selected modules.
Proposed wording: "A pass establishes only what its stated checks cover."
S4: missing evidence remains unknown, never automatically a pass.
S5: shared mistaken assumptions can survive all tests; scientific validity
is not established by syntax, coverage or reviewer agreement.

### Independent scientific check

N/A: this proposal changes guidance, not equations or published results.
Any new numerical worked example must supply its independent basis.

## Signals the change is wrong

More forms appear, snapshots are called scientific validation, optional tools
become mandatory, or tests grow without finding additional plausible faults.

## Scope delta

**Scope delta**: preserved -- testing quality and optional acceptance prompts
are one coordinated outcome.

## Assurance path

**Assurance path**: high-assurance -- governing verification guidance.

## Review -- Codex (fresh-context usual reviewer) -- 2026-11-02

**Model**: inherited Codex runtime; exact identifier unavailable; no downshift.
**Reviewed commit**: `9d5a69e524a2ab3a749b386dd67efe2861f2ecf0`
**Tier**: usual
**Target**: opening proposal. **Prior findings**: none.
**Assurance path**: high-assurance.

**Foundations**

1. **Should this happen as framed?** Yes: teach discriminating evidence and
   observable criteria together. Existing guidance covers properties and
   budgets, but not expectation laundering --
   `templates/modules/team-gated/testing-discipline.md`; `dev/plans/_template.md`,
   Acceptance criteria.
2. **Best alternative.** Module-only worked examples avoid editing the shared
   plan contract and reduce maintenance, but lose the board's optional
   acceptance prompts; existing falsifiability prose does not supply them --
   `dev/PLANNING.md`, testing/acceptance rows; `dev/plans/_template.md`.
3. **What would show it wrong?** Candidate-derived expectations pass as
   independent, characterization freezes an error, or optional tools become
   obligations -- Proposal 1-4; `examples/scientific-minimal/test_water_budget.py`,
   `TestMassBalanceInvariant`.

**Verdict**: ACCEPT. **Findings**: one non-blocking improvement; no blockers.

1. **FT-1 -- Replace the existing overclaim explicitly.** The testing module
   says passing conservation/convergence shows equations are solved correctly;
   passing selected checks cannot establish that general conclusion.
   The scientific example deliberately uses balanced synthetic inputs
   (`examples/scientific-minimal/water_budget.py`). Close by replacing that
   categorical sentence and making one worked example show a balanced but
   wrong input or compensating error, plus an independently grounded check
   that detects it. This sharpens promised examples, not a new validation
   framework.

Testing, optional property/mutation guidance, test-first and acceptance
outcomes remain represented. The outside-practices strategy cannot retire
until architecture outcomes also have dispositions; release closeout owns
the grouped assignment.

**Elapsed**: approximately 7 minutes, including shared source inspection.
**Tokens**: unknown.

**Covered**: module/template promises, installation/preservation assertions,
verification guards, scientific example, board scope and retirement links.
**Not covered / low confidence**: no example execution, mutation or
implementation reruns; outside literature was not independently validated.
This pass does not discharge Security Review.

## Review -- Codex (independent Security Reviewer) -- 2026-11-02

**Model**: inherited Codex runtime; exact identifier unavailable; no downshift.
**Reviewed commit**: `9d5a69e524a2ab3a749b386dd67efe2861f2ecf0`
**Target**: opening proposal. **Prior findings**: none.
**Assurance path**: high-assurance. **Tier**: Security Review.

**Foundations**

1. **Should this happen as framed?** Yes: strengthen evidence without another
   framework; current snapshot/property guidance lacks the explicit
   candidate-expectation warning --
   `templates/modules/team-gated/testing-discipline.md:53-63`; Proposal 1-6.
2. **Best alternative.** Extend existing module guidance and acceptance cells,
   keeping tools optional -- Proposal 5;
   `dev/plans/_template.md:222-243`.
3. **What would show it wrong?** Candidate-derived expectations count as
   independent evidence, or expectation changes bypass accepted scope --
   Examples / smoke checks; `dev/plans/_template.md:231-243`.

**Verdict**: ACCEPT. **Findings**: none; no numbered findings require closure.

The proposal distinguishes established behavior from physical validity,
requires an independent basis for changed expectations, and treats surviving
mutations as investigation leads. Author-supplied criteria and reviewer
agreement grant no waiver authority. Optional criterion syntax does not make
required checks optional.

S3 has existing author/reviewer and selected-module installation owners
(`bootstrap/tests/test_practice_modules.py:92-117`). Rejection exercises remain
future implementation evidence, not executed safeguards. S4 preserves unknown
evidence; S5 correctly leaves shared mistaken assumptions unresolved.

Two existing negative guards passed: removal of the wide-surface fence and
reviewed-range requirement (`bootstrap/tests/test_verification_boundaries.py`).
Python 3.13.13; combined eight-check scratch run: 0.26 seconds. These do not
validate the proposed examples. Retirement retains the outside-practices
strategy's architecture outcome (Documentation / doctrine surface).

**Elapsed**: shared approximately six-minute review window; per-file split
unmeasured; recording approximately two minutes. **Tokens**: unknown.

**Covered**: S1-S5, expectation provenance, waiver boundaries, installation
owners and retirement scope. **Not covered / low confidence**: future examples,
scientific correctness, prompt trials or external literature validation.

## Response -- Codex (author) -- 2026-11-02

**Model**: Codex (runtime model identifier unavailable).

- **FT-1 accepted:** The operative contract now replaces the module's
  categorical equation-solving claim with evidence limited to the properties
  checked. The worked examples must include a balanced-but-wrong input or
  compensating error and an independently grounded check that detects it.
- **Security Review:** Accepted with no findings. The candidate-derived
  expectation prohibition, no-waiver boundary, honest uncertainty and
  source-strategy retirement conditions remain unchanged.

Testing guidance owns the functional-scope versus runtime/cost distinction;
architecture/reuse owns its contrasting rubric examples. This specifies
existing coordinated scope, not another testing framework or review stage.

The proposal is ready for the Maintainer's Decision. Worked-example
experiments remain implementation obligations; no scientific result is
claimed from these prose changes.

**Elapsed**: approximately 7 minutes shared revision design; per-file split
unmeasured. **Tokens**: unknown.

### Withdrawn / superseded commitments

None. The scope is preserved; the existing overclaim is expressly targeted
for replacement, not silently retained.
