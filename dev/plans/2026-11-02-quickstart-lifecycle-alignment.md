# Plan: Align the quickstart lifecycle

**Source proposal**: dev/proposals/archive/2026-11-02-codex-quickstart-lifecycle-alignment.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Correct the quickstart and its sequence test so the example records its final check before archive.

## Source proposal

The Maintainer accepted a light teaching example and a correction to its protected sequence test, with heavy assurance for the test change. The actual one-line tagline normally takes the trivial lane.

## Scope

Revise `docs/quickstart.md` and `bootstrap/tests/test_quickstart_sequence.py`. Preserve the review, Decision, tagline, changelog and clean history checks. No governing rule, gate, baseline or release requirement changes. Stop for reassessment if another protected surface or conflicting requirement proves necessary.

**Reuse.** The existing Step 5 and Step 6 tests construct the disposable lifecycle; searches for `Step 5`, `Step 6`, `archive` and `verification` in those files found the prose and assertions to revise. Extend those checks rather than add a checker.

### Documentation / doctrine surface

The quickstart describes existing practice; no doctrine surface changes. The plan and proposal hold deliberation.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Correct the recipe and existing sequence checks. | Both required plan reviews and author response | Updated example and disposable workflow assertions. |
| C2 | Independent ordinary and Security code reviews, response and final verification. | C1 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** The opening, proposal prompt and Maintainer Decision identify the deliberate example as light and retain the ordinary trivial-lane explanation. The recipe commits implementation, runs the applicable bounded final integration check on that clean commit, records results and omissions in the accepted proposal, then archives in a later commit. Prompts, expected history and explanation agree; no full suite or separate ceremony is introduced. Step 5 and Step 6 exercise this order and retain existing content and lifecycle assertions. A missing or misplaced verification record is rejected by an assertion on constructed history.

**C2.** Independent ordinary and Security code reviews precede passing wide Boundary B. The finished recipe is read cold against installed guidance; its commands and history match the exercised sequence. The surrogate does not claim to execute an adopter's agent.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation, map readers and byte pins for both changed files with `python tools/test_tiers.py for docs/quickstart.md bootstrap/tests/test_quickstart_sequence.py` and search, validating negative searches against a known positive. Run the mapped iteration checks, including Step 5 and Step 6, through the real disposable-repository workflow. Demonstrate that omitting or misplacing the verification record fails an assertion on the constructed history; report the mutation and result. This is the proposal's S2/S3 control; it cannot prove the record is truthful or that an adopter ran the recipe.

Run applicable claim, link, snippet and neutrality gates and `python scripts/check_cairn.py`. After independent ordinary and Security code reviews and fixes, run wide Boundary B on a clean unchanged final commit under canonical Python 3.13: mapped iteration and integration/workflow checks, owning families, known public paths and standing gates. Record SHA and range, interpreter, clean pre/post state, commands and counts, elapsed time, non-pass dispositions and omissions. Full certification and baseline work remain separate; do not run a full suite for implementation.
