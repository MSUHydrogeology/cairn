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
