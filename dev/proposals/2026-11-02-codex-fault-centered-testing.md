# Make scientific tests and acceptance criteria catch meaningful faults

**Author**: Codex (runtime model identifier unavailable; Strategy)
**Status**: revising
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

At `4d29b2ef`, `templates/modules/team-gated/testing-discipline.md` already
covers regimes, invariants, public entry points, consolidation and simulation
benchmarks. It does not explicitly develop characterization of trusted
scientific behavior or address agents changing expectations to obtain a pass.
The plan template already has acceptance and verification sections.

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
faults they can actually detect. No optional library becomes an installed
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
acceptance cells; do not add another specification file.

**6. Demonstrate test-first.** Show scientific and ordinary software examples:
a useful oracle, vacuous check and deliberate fault. Observe the intended
failure before implementing new behavior. Distinguish established behavior
from physical validity. Reuse the scientific-minimal example where suitable;
do not build another project.

## Rationale

The benefit is more informative evidence and less redundant testing. The
recurring cost is example upkeep and human judgment on genuine scientific
questions. Reuse existing records, readers and modules.

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
advice rather than append a second checklist. Keep scientific, security and
release checks and their existing triggers unchanged.

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
