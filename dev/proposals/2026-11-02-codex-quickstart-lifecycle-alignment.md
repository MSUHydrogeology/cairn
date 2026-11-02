# Align the quickstart example with the lifecycle

**Author**: Codex (GPT-6), Strategy
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Correct the quickstart and its sequence test so the example follows the light-tier review and verification steps it teaches.

## Decision summary

The quickstart describes its one-line example as heavy, but gives it one proposal review and archives it with the implementation. Make the teaching example explicitly light and show its final implementation check and record before archive. Update the existing sequence test to check that order. This adds a visible verification and archive step to the exercise, but no new process or standing checker.

## Context

`docs/quickstart.md` says the example is heavy near its opening; Step 5 gives one review, then implements and archives in one commit. The shipped `templates/core/AGENTS.md` says heavy adds Security Review and requires final implementation verification after the implementation commit; light work records that verification in its accepted proposal. `docs/methodology/lifecycle.md` says a light proposal archives only after that record. The existing `bootstrap/tests/test_quickstart_sequence.py` Step 5 and Step 6 nodes enact and assert the old combined commit and six-commit history.

The sequence test is in `bootstrap/tests/fixtures/protected_test_roster.json` and its nodes are listed in `bootstrap/tests/fixtures/gate_manifest.json`. Editing this protected test is high-risk and retains the separate Security Review obligation. No existing gate is waived or changed by this proposal.

## Proposal

Revise `docs/quickstart.md` to identify the deliberately non-trivial teaching route as light in the opening, proposal prompt and Maintainer Decision. Retain the explanation that an actual one-line tagline normally takes the trivial lane. Show the implementation committed first, then the applicable bounded final integration check on that clean commit, its results and omissions recorded in the accepted proposal, and a later archive commit. Update the prompts, expected history and explanation together. Keep the recipe short and usable by someone working through an agent; do not invent a separate ceremony or require a full suite.

Update the existing Step 5 and Step 6 sequence checks to exercise the revised ordering and verify the verification record precedes archive, while preserving their checks for the review, Decision, tagline, changelog and clean lifecycle history. Keep unrelated tests and protections intact. If discovery shows a necessary additional protected surface or a conflicting requirement, stop for reassessment instead of widening scope silently. The current Maintainer-controlled baseline and release requirements remain separate.

## Rationale

Light preserves the example's one ordinary proposal review and avoids imposing an unrelated Security Review on a tagline. Recording the final check before archive teaches the actual light workflow. The test should catch a regression in the order rather than simply assert a new commit count.

## Alternatives considered

* Leave it alone: no work now, but a first-time adopter is told to follow contradictory instructions.
* Keep the example heavy: it would need a separate Security Review and would teach extra work for a trivial tagline, with no added benefit to this example.
* Change the prose alone: fewer edits, but the existing protected sequence test would continue to endorse the incorrect history.

Recommendation: the light example and its existing test, with the fewest steps needed to meet the current rules.

## Documentation / doctrine surface

`docs/quickstart.md` describes existing behavior; no governing doctrine changes. The deliberation and decision stay in this proposal. The affected sequence test remains in `bootstrap/tests/`.

## Evidence / verification plan

### Tests required

Map readers and byte pins for both changed files with `python tools/test_tiers.py for` and a known-positive search before implementation. Run the mapped iteration checks, including the Step 5 and Step 6 nodes of `bootstrap/tests/test_quickstart_sequence.py`, through their real disposable-repository workflow. Confirm the checked implementation commit precedes the recorded verification and archive, and preserve the existing content and history assertions. Demonstrate a plausible missing or misplaced verification record is rejected by the revised sequence check; report the mutation and result. Independent ordinary and Security code reviews precede wide Boundary B on a clean final committed tree under Python 3.13, with commands, results and omissions recorded. Certification and any baseline work remain separate.

### Examples / smoke checks

Run the applicable claim, link, snippet and neutrality gates and `python scripts/check_cairn.py`. Read the finished recipe cold against the installed governing guidance; check that its commands and expected history match the exercised sequence. Do not run a full suite for implementation.

#### Security preflight — five questions, answered in writing

S1: The checked sequence is supplied by repository test and documentation; the expected order comes from the shipped governing rule, not the example under test alone.

S2: Removing or moving the verification record before the implementation commit should fail the revised sequence check. This control is proposed, not yet run.

S3: The named pytest nodes select the disposable quickstart lifecycle; human comparison checks the prose against the shipped Boundary B and light-archive rule. Neither proves a real adopter executed the steps.

S4: Missing or malformed evidence must fail the check rather than be counted as a completed verification; this behavior remains to be tested.

S5: A misleading or fabricated record could still satisfy a structural test; independent review and actual recorded check results remain necessary.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The recipe still asks for heavy work without its review, archives before the final check record, needs a full suite for the example, or the test passes when the required verification record is omitted.

## Scope delta

None; opening scope.

## Assurance path

**Assurance path**: high-assurance

**Authoring elapsed**: approximately 5 minutes. **Tokens**: unknown.

## Security Review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: d647c2a4d5d4bd248d2abcf38c1ccf740c3fbdce  
Target: light teaching route, verification-before-archive ordering and protected sequence test  
Prior findings: none  
Assurance path: high-assurance

**Tier**: Security Review  
**Findings**: none  
**Verdict**: ACCEPT as framed; recommendation, not a Maintainer Decision.  
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The current heavy-labelled exercise omits heavy's separate Security Review, and its Step 5/6 tests combine implementation with archive. A light teaching example plus verification on the committed implementation matches existing governing and archive rules. The protected-test correction retains heavy assurance. -- Quickstart opening; sequence tests Step 5/6; shipped Boundary B; lifecycle archive rule; protected roster.
2. **Best alternative.** Keep the teaching example heavy, but that adds a Security Review unrelated to the tagline's risk and further lengthens onboarding. Making it trivial would remove the proposal/review/Decision lesson. Light retains that lesson with the least applicable ceremony, while prose-only correction leaves the test endorsing wrong ordering. -- Proposal, Alternatives and Rationale; accepted cut-the-apparatus, cut 2.
3. **What would show it wrong?** Archive still preceding final verification, a fabricated count-only history check, or the example demanding a full suite. The planned real disposable sequence and omitted/misplaced-record mutation address order; cold reading against installed guidance checks the recipe without claiming adopters actually executed it. -- Proposal, Tests required, S2–S5 and Signals.

No blocking finding. Preserve the ordinary-trivial explanation and the existing content, Decision and clean-history assertions. Updating the two existing files is proportionate; no new lifecycle rule, checker, review ceremony or trust mechanism is necessary. S5 correctly limits structural assurance.

Coverage: read committed proposal, target quickstart passages, sequence assertions, protected roster, current proposal template, governing verification and archive rules, and accepted cut 2. Did not map every reader/pin, run the proposed mutation, exercise the recipe or execute suites. No anchor comparison.

## Proposal review -- Codex GPT-6 -- 2026-11-02

**Verdict:** Accept as framed; no blocking findings. **Elapsed:** approximately 5 minutes. **Tokens:** unknown.

1. **Should it happen?** Yes. The quickstart calls its example heavy but shows one review, then combines implementation and archive. Its existing sequence tests explicitly reproduce that order. The proposed light example and verification record align the lesson with the shipped rules while preserving the real tagline's trivial lane.
2. **Best alternative:** Correcting the prose alone is smaller, but leaves the existing tests teaching the old sequence. Keeping a heavy example adds a Security Review to a simple lesson. Updating the two existing files retains the lesson without adding a checker.
3. **What would show it wrong?** A recipe that archives before verification, requires a full suite, or a sequence check that cannot detect an absent or misplaced verification record. The proposed disposable-repository check and negative control address those cases; an agent should also read the resulting instructions as a newcomer.

The two existing tests construct a surrogate lifecycle rather than execute the prose. Keep that distinction clear: their negative control should exercise a real assertion on the constructed history, not imply that the test executes an adopter's agent.

Coverage: read the committed proposal, affected quickstart and sequence tests, and the independent Security review. Did not run tests, inspect every consumer, or execute the recipe.
