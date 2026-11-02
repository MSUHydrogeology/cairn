# Plan: Align the quickstart lifecycle

**Source proposal**: dev/proposals/archive/2026-11-02-codex-quickstart-lifecycle-alignment.md
**Status**: ready-to-implement
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

## Plan review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: 5fca7a821552db1eeb8f63ec7eed54d42a64ba17  
Target: protected sequence assertions, verification order and scope boundary  
Prior findings: none  
Assurance path: high-assurance

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none

**Foundations**

1. **Should this happen as framed?** Yes. The two-file plan delivers the accepted light teaching route while retaining heavy assurance for the protected test. Implementation, checked clean commit, recorded evidence and later archive remain ordered. -- Source proposal, Decision and S1–S5; plan C1/C2; shipped AGENTS.md, Boundary B.
2. **Best alternative.** Extend the existing Step 5/6 disposable workflows, as planned. A prose-only fix leaves assertions endorsing the old order; an additional checker or heavy tagline exercise adds burden without improving this lesson. -- Existing test Step 5/6; proposal Alternatives; plan Reuse.
3. **What would show it wrong?** A missing/misplaced record passing the history assertion, malformed evidence counted as complete, or a recipe requiring full certification. The mutation and cold read target these failures; structural evidence cannot prove truthful adopter execution. -- Plan Verification and C1/C2; proposal S2–S5; test lifecycle-shape sentinel.

**Verdict**: Accept as framed; no blocking findings. Preserve S4's malformed-evidence rejection through the existing content/history assertions rather than adding apparatus. The stop-on-discovery boundary keeps gate manifests, baseline and release requirements outside this implementation's authority.

**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

Coverage: read committed plan, accepted proposal, current plan template, governing verification/archive rules, target prose and tests, protected roster and gate-manifest entries. Did not map all readers/pins, run mutations, exercise installation, compare an anchor or run suites.

## Plan review -- Codex GPT-6 (Reviewer) -- 2026-11-02

Reviewed commit: 4dee6507
Target: scope, sequence, criteria and verification against the accepted proposal
Prior findings: none
Assurance path: high-assurance

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT; the plan delivers the accepted scope. **Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The plan retains the light example, trivial-lane explanation, verification before archive, existing content checks and independent reviews. -- Accepted proposal, Proposal and Tests required; plan C1–C2.
2. **Best alternative.** Updating only the prose would leave the existing Step 5 and 6 tests endorsing the old order; extending those tests avoids adding a separate checker. -- Proposal Alternatives; committed sequence tests and plan Reuse.
3. **What would show it wrong?** A recipe that archives before verification or a constructed-history assertion that accepts an omitted or misplaced record would defeat the lesson. The plan requires a mutation and cold comparison with installed guidance. -- Plan C1 and Verification; proposal S2–S5.

Coverage: read the committed plan, accepted proposal, Security plan review, template, and relevant quickstart and sequence-test passages. Did not map all readers or pins, run the mutation or tests, or exercise the recipe; those checks remain implementation obligations.

## Response to plan reviews -- Codex GPT-6 -- 2026-11-02

Both reviews accept the plan without blocking findings. The Security review’s advice is accepted: reject malformed evidence through the existing content and history assertions. Reader and pin mapping, mutations, independent code reviews and wide final verification remain implementation obligations.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.
