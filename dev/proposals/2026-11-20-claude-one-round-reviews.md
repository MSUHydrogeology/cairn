# One round of review at each stage, and a closing test for each blocking finding

**Author**: Claude Sonnet 5.5
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — it changes governing doctrine under `docs/methodology/` and lowers a Security Review limit.
**Plan review**: required(Internal + Internal Security Review) — about 30 edits in 16 files; the plan changes a Security limit.
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/working-agreements.md, dev/rules/protected-surfaces.md, dev/rules/conventions.md
**In brief**: Each review stage gets one round, and a reviewer who blocks work supplies the test or the exact words that close the finding, so fixes are not read a second time and plans stay smaller.

## Decision summary

**Conclusion.** Each review stage (proposal, plan, code) gets one round of review. A reviewer who blocks the work also supplies what closes the finding, so nobody reviews the fix a second time. I recommend option C.

**Measured.** In the 73 plans opened since 2026-11-01, a quarter of the 413 review passes were a third or later pass at the code stage (a pass is one review of one committed version). At least 63 passes were a reviewer coming back to check a fix, which this proposal calls a *return visit*. About 44 of those only confirmed the fix. The counts come from review headings at commit `effb7493`; the tables are in the [appendix](2026-11-20-claude-one-round-reviews--appendix.md).

**The five changes.**

1. One round per stage: one usual review and, where the tier requires it, one Security Review. Security Review's normal limit drops from two passes to one.
2. A reviewer who blocks work writes what closes the finding: a failing scratch test for code, exact words for a document.
3. Code is reviewed once, after the plan's last chunk of work.
4. A further proposal or plan review happens only when the Maintainer adds scope, and it gets a short brief.
5. A plan has at most five chunks. Larger work becomes several plans that share one wide test run.

**What the Maintainer is asked to accept.**

- Two of the 63 return visits caught a new defect made by the fix. Later test runs must now catch such defects.
- Three of the 24 Security return visits asked for more work. The reviewer's test must now carry that.
- A passing test is not proof that a fix is right.
- A blocking Security finding still open at the limit reaches the Maintainer as a question of risk. That happened twice in the 73 plans; with a limit of one pass it may happen more often.
- No human operation is added.

**Options.**

| Option | What changes | What is given up |
|---|---|---|
| A | Nothing. | Return visits and the growth of plan files continue. |
| B | All but the Security limit and the chunk limit. | The 24 Security return visits and the large plans continue. |
| C | All five changes. | The second look at a fix, at every stage. |

This proposal itself takes one usual review and one Security pass, because it changes the published review rules. The Maintainer may lower the tier.

**Not checked.** I did not measure tokens (most reviews record `unknown`), how many tests each plan ran, or whether cost will fall. The recount in D6 tests that.

## Context

The Maintainer asked for this (chat, 2026-11-20): "How about we limit plan reviews to one round? Same for security reviews in both plans and proposals?" Most of it is already written: `AGENTS.md:19` says "Each review is one pass", yet 43 of 73 plans have three or more code-stage passes. The standing directions it carries out are in `dev/rules/working-agreements.md` (entries of 2026-11-12, 2026-11-13 and 2026-11-16). A high-tier Strategy agent (Claude Fable 5.2) made the design, the security judgment and the counts on 2026-11-20. I re-ran the counts and wrote this up as the medium-tier author the Maintainer asked for; Strategy edited the wording before the opening commit.

## Proposal

**D1. One round.** Proposed paragraph for `AGENTS.md` and its shipped twin (80 words, 21 more than today; governing files 1,588 to 1,609 of 2,000):

> Each review stage is one round: one usual pass and, where the tier requires it, one Security Review pass. A blocking finding states what closes it: a failing test for code, exact words for a document. A further pass needs scope the Maintainer added, a substantive plan amendment, or the Maintainer's explicit authorization and a specific unresolved security question; each later pass needs new authorization. At a cap, send only unresolved blocking findings or unmet accepted checks to the Maintainer.

The second code pass, allowed today for "new defects (code)", goes.

**D2. What closes a blocking finding.** On code, the reviewer writes a failing developmental test (Cairn's scratch test, deleted before archive) in the review, with its command and two or three cases where input regimes differ. Example: a tool crashes on an empty input file, so the review holds a test that feeds it one and fails today. The implementer runs the test, fixes the code, runs it again, and records both results with commit ids. The implementer may decline a test as wrong, with a reason. No return visit follows. If the test guards a listed promise, it joins that promise's existing test (`dev/modules/testing-discipline.md:44`). Where no test can express the finding, the reviewer names the exact lines to remove or replace, as for dead code. On a document, the reviewer gives the exact words; the author applies them or declines with a reason. A design objection means the plan was wrong and takes the amendment path, with its fresh non-author review. This replaces the "targeted look before Boundary B" (`dev/agent_collaboration.md:365`).

**D3. Code review once.** It follows the last chunk; a chunk is one row of a plan's Sequence table. A plan may name one earlier review point, at plan time, for a high-risk chunk that later chunks build on.

**D4. Scope the Maintainer adds.** A further proposal or plan review happens only for "maintainer additions that increase scope" (chat, 2026-11-20). It gets "a very limited brief": the added text and the first review. It goes to the first reviewer where the tool can resume that session, otherwise to a reviewer given only those two things, and never to the author. An addition that alters what a high-risk surface does gets one Security pass on the same brief. On a plan this is one exception to the amendment rule's fresh reviewer (`dev/agent_collaboration.md:309`). Cairn already sends one limited look "to the same reviewer" (`docs/methodology/dual-review.md:342-343`).

**D5. At most five chunks.** The Maintainer asked that "plans are smaller, with fewer chunks", without more testing (chat, 2026-11-20). Five is a target that the plan review checks. Larger work is cut into smaller finishable outcomes, each its own plan under the one proposal, grouped as one arc: plans that share one joined test run. Two existing rules keep testing from rising: a plan runs only the tests that name its changed files, and an arc has one joined run. Today a plan costs about five review passes whatever its size (appendix), so the limit takes effect with D1 to D3, not before.

**D6. How we will know.** At the end of v0.9, repeat the heading count on plans opened under the new rule. Each plan's verification record also states how many test files the selector chose.

**D7. Unchanged.** When Security Review applies; tiers; fences; Decisions; model floors; required checks; the certifying run; the targeted look after a failed joined run; and the lifecycle's status names and edges, so no tool or test changes. The new rules apply to proposals and plans opened after the change ships.

## Rationale

Return visits mostly confirm a fix (about 44 of 63 by my count). A test from the reviewer, seen failing first, lets anyone check the fix without a second review. A passing test is still not proof: in one study, 29.6% of test-passing agent patches behaved differently from the developers' fix (Wang, Pradel and Liu 2026, doi:10.1145/3744916.3764576; the Strategy agent read the abstract only, and I did not open the paper). So the later test runs stay. This is not a single incident. It rests on a strategy review, the Maintainer's direction and a pattern counted in 73 plans, and I claim no rate-limit trigger it lacks.

## Alternatives considered

The options are in the Decision summary. B is about two-thirds of C's build. C is about 30 edits in 16 files; the nearest earlier sweep (`dev/plans/archive/2026-11-16-heavy-tier-trigger.md`) took 4 review passes and 17 commits to its plan file. I expect C to remove 15 to 25% of review passes, an estimate from the counts and not a measurement. Reviews get longer, because reviewers write tests. A cheaper variant has the reviewer only recommend a test that the implementer then writes. The Maintainer chose the reviewer (chat, 2026-11-20): "I think the reviewer should write the tests." That keeps the closing check independent of the fix. I recommend C: B leaves out the two limits the Maintainer asked for.

## Documentation / doctrine surface

Sixteen files change: the governing and collaboration text, the plan and proposal templates (each with a shipped twin), four methodology pages, and the security-review and testing-discipline modules (each with a shipped twin). The appendix lists each line and its change. Paired updates land together (`docs/DOCUMENTATION_PLAN.md:376`). Shipped text names no model or vendor.

## Evidence / verification plan

The implementation runs the prose gates (`tests/check_cairn.py`, `dev/tools/claim_check.py`, `dev/tools/link_check.py`), the neutrality gate, the governing-file word cap and `tests/tier_inventory.py for` over the reviewed range. Reviewers read each home for a rule that weakens or disappears. D6 is the forward check.

### Tests required

N/A: prose only; no code or caller-visible behaviour changes.

### Security preflight

- **S1.** The reviewer supplies the closing test; the implementer supplies only results, which are self-reported with commit ids, as is every check an implementer records today.
- **S2.** The reviewer sees the test fail before the fix; reverting the fix fails it again; its expected value must not come from the fixed code.
- **S3.** The reviewer's command fires it over the cases in the review.
- **S4.** A weak test closes a finding wrongly: less protection.
- **S5.** A fix that passes the cases but leaves the fault, or adds a defect, still gets through; the class is closed by enumeration, not construction.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

- After archive, more than a few defects trace to a fix that no reviewer read again.
- More than one joined run per arc.
- Plans are cut into more pieces and total review passes rise.
- Reviewers' tests are often declined as wrong.
- Security findings reach the Maintainer often.

## Scope delta

**Scope delta**: preserved. This is the opening proposal; the rules it removes are the proposed change.

## Assurance path

**Assurance path**: high-assurance. The change alters governing doctrine and lowers a Security Review limit.
