# One round of review at each stage, and a closing test for each blocking finding

**Author**: Claude Sonnet 5.5
**Status**: awaiting-decision
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
- A blocking finding that is declined, or still open at the limit, reaches the Maintainer. That happened twice in the 73 plans, both times for Security; with one pass it may happen more often.
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

**D2. What closes a blocking finding.** On code, the reviewer writes a failing developmental test (Cairn's scratch test, deleted before archive) in the review, with its command and two or three cases where input regimes differ. Example: a tool crashes on an empty input file, so the review holds a test that feeds it one and fails today. The implementer runs the test, fixes the code, runs it again, and records both results with commit ids. The implementer runs the test exactly as the review gives it; a changed test counts as a decline. The implementer may decline a test as wrong, with a reason. No return visit follows. If the test guards a listed promise, it joins that promise's existing test (`dev/modules/testing-discipline.md:44`). Where no test can express the finding, the reviewer names the exact lines to remove or replace, as for dead code. On a document, the reviewer gives the exact words; the author applies them or declines with a reason. A declined blocking finding stays open and goes to the Maintainer with the reason, as at a cap. On a proposal or plan, a premise objection has no exact words; it goes to the Maintainer with the author's reply. At code review, a design objection means the plan was wrong and takes the amendment path, with its fresh non-author review. This replaces the "targeted look before Boundary B" (`dev/agent_collaboration.md:365`).

**D3. Code review once.** It follows the last chunk; a chunk is one row of a plan's Sequence table. A plan may name one earlier review point, at plan time, for a high-risk chunk that later chunks build on. That named point is the one exception to a single code review.

**D4. Scope the Maintainer adds.** A further proposal or plan review happens only for "maintainer additions that increase scope" (chat, 2026-11-20). It gets "a very limited brief": the added text and the first review of the same kind. It goes to the first reviewer where the tool can resume that session, otherwise to a reviewer given only those two things, and never to the author. An addition that alters what a high-risk surface does gets one Security pass on the same brief. A Security reviewer may also read any file the addition touches. On a plan this is one exception to the amendment rule's fresh reviewer (`dev/agent_collaboration.md:309`). Cairn already sends one limited look "to the same reviewer" (`docs/methodology/dual-review.md:342-343`).

**D5. At most five chunks.** The Maintainer asked that "plans are smaller, with fewer chunks", without more testing (chat, 2026-11-20). Five is a target that the plan review checks. Larger work is cut into smaller finishable outcomes, each its own plan under the one proposal, grouped as one arc: plans that share one joined run, the single wide test run after they finish. Two existing rules keep testing from rising: a plan runs only the tests that name its changed files, and an arc has one joined run. Today a plan costs about five review passes whatever its size (appendix), so the limit takes effect with D1 to D3, not before.

**D6. How we will know.** At the end of v0.9, repeat the heading count on plans opened under the new rule. Each plan's verification record also states how many test files the selector chose.

**D7. Unchanged.** When Security Review applies; tiers; fences; Decisions; model floors; required checks; the certifying run; the targeted look after a failed joined run; and the lifecycle's status names and edges, so no tool or test changes. The new rules apply to proposals and plans opened after the change ships.

## Rationale

Return visits mostly confirm a fix (about 44 of 63 by my count). A test from the reviewer, seen failing first, lets anyone check the fix without a second review. A passing test is still not proof, so the later test runs stay. This is not a single incident. It rests on a strategy review, the Maintainer's direction and a pattern counted in 73 plans, and I claim no rate-limit trigger it lacks.

## Alternatives considered

The options are in the Decision summary. B is about two-thirds of C's build. C is about 30 edits in 16 files; the nearest earlier sweep (`dev/plans/archive/2026-11-16-heavy-tier-trigger.md`) took 4 review passes and 17 commits to its plan file. I expect C to remove 15 to 25% of review passes, an estimate from the counts and not a measurement. Reviews get longer, because reviewers write tests. A cheaper variant has the reviewer only recommend a test that the implementer then writes. The Maintainer chose the reviewer (chat, 2026-11-20): "I think the reviewer should write the tests." That keeps the closing check independent of the fix. I recommend C: B leaves out the two limits the Maintainer asked for.

## Documentation / doctrine surface

Sixteen files change: the governing and collaboration text, the plan and proposal templates (each with a shipped twin), four methodology pages, and the security-review and testing-discipline modules (each with a shipped twin). The appendix lists each line and its change. Paired updates land together (`docs/DOCUMENTATION_PLAN.md:376`). Shipped text names no model or vendor.

## Evidence / verification plan

The implementation runs the prose gates (`tests/check_cairn.py`, `dev/tools/claim_check.py`, `dev/tools/link_check.py`), the neutrality gate, the governing-file word cap and `tests/tier_inventory.py for` over the reviewed range. Reviewers read each home for a rule that weakens or disappears. D6 is the forward check.

### Tests required

N/A: prose only; no code or caller-visible behaviour changes.

### Security preflight

- **S1, who supplies the check.** The reviewer supplies the closing test, and the implementer must run it unchanged; a changed test counts as a decline. The results are self-reported with commit ids, as is every check an implementer records today.
- **S2, can it fail.** The reviewer sees the test fail before the fix, and the implementer records it failing at the commit before the fix and passing after. Its expected value must not come from the fixed code.
- **S3, what runs it.** The reviewer's command fires it over the cases in the review.
- **S4, which way it breaks.** A weak test closes a finding wrongly: less protection.
- **S5, what still gets through.** A fix that passes the cases but leaves the fault, or adds a defect. The class is closed by enumeration, not construction.

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


## Review -- Claude Sonnet 5.5, Reviewer (usual) -- 2026-11-20

```
Reviewed commit: 2883024af3893c2dbfae3bfbb03fcbba6da44355
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

The proposal tries to stop paying for a second reader of each fix, by making the reviewer hand over a test that fails first and passes after. I re-ran `dev/scratch/review_rounds.py`: 413 plan passes, 144 code-usual and 101 code-Security, 63 return visits, 43 of 73 plans with three or more code passes. All match the appendix.

**Foundations**
1. **Should this happen as framed?** Yes, with one gap below. `AGENTS.md:19` already says one pass, and the counts show it is not followed. -- `review_rounds.py` output.
2. **Best alternative.** Option B plus a recommend-only test. It is weaker on independence, which the Maintainer chose against. -- Context quote, 2026-11-20.
3. **What would show it wrong.** After archive, defects that trace to a fix no reviewer re-read. The proposal's Signals section already names this; a recount at v0.9 (D6) is a real, owned check. -- D6.

**Does any rule weaken or disappear?** Yes, openly: the second Security pass and the new-defects code pass (`AGENTS.md:19`, `security-review.md:84`). Both are stated and the Maintainer is asked.

**Findings**
- **Blocking.** D2 lets the implementer or author decline a closing test or exact words "with a reason". Nobody reads that reason, so a blocker can be closed by its author alone. Add to D2 after "declines with a reason": "A declined blocking finding stays open and goes to the Maintainer with the reason, as at a cap."
- Non-blocking. D3 allows an earlier code review point, so "one round" has an exception; say so in the D1 sentence or D3.
- Non-blocking. A proposal or plan blocker that is a premise objection has no "exact words". Say it goes to the Maintainer.
- Non-blocking. Terms the Maintainer must learn: return visit, joined run, arc, S1 to S5. Define each once.
- Non-blocking. 1,833 words against the 1,000 target; the Wang study is cited from an abstract only (disclosed).

**Not covered:** the 16 files' line numbers beyond those I opened; the 2,000-word cap arithmetic; whether tests or tools match the changed phrases.

## Review -- Claude Opus 5.5, Security Review -- 2026-11-20

```
Reviewed commit: cd503a53bf6063522960d995337632063606491c
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: about 8 minutes
**Tokens**: unknown

At its strongest, the proposal swaps a second reader of each fix for a check written by someone other than the fixer, seen failing first. For security that keeps the independence that matters, if the check cannot be changed by the fixer.

**Foundations**
1. **Should this happen as framed?** Yes. The further-pass path stays: Maintainer authorization plus a specific question, or newly changed material -- D1; `dev/modules/security-review.md:84-88`.
2. **Best alternative.** Keep two Security passes, the change named by option B. Only 3 of 24 Security return visits asked for more work -- appendix line 38.
3. **What would show it wrong.** At the v0.9 recount (D6), a security defect after archive traced to a fix no Security reviewer read -- Signals.

**Does any rule weaken or disappear?** Yes, openly: the second Security pass (`security-review.md:84`) and the second look at a fix larger than a failing test (`dev/agent_collaboration.md:365`). The cap path to the Maintainer survives.

**Findings**
- **Blocking.** S1 says the implementer "supplies only results", but nothing stops the implementer from editing the reviewer's test until it passes. Add to D2 after "records both results with commit ids": "The implementer runs the test exactly as the review gives it; a changed test counts as a decline."
- **Blocking (concur with the usual review).** A declined Security finding is closed by its implementer alone. Apply the usual review's sentence; it covers this.
- Non-blocking. D4's limited brief can hide how an addition meets unchanged guards. Add: "A Security reviewer may also read any file the addition touches."
- Non-blocking. S2's "reverting the fix fails it again" has no owner; D2 records only before and after runs.

**Not covered:** the appendix's 16-file line table; the counts (not re-run); the Wang study; the three Security return visits that asked for more work.

## Response -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-20

Strategy made the design, so Strategy answers the findings. Each blocking finding is closed with the reviewer's own words, so no second pass is owed.

**Usual review**

1. Blocking, a declined finding closed by its own author: accepted. D2 carries the reviewer's sentence, and the Decision summary names declined findings among what reaches the Maintainer.
2. D3's exception: accepted. D3 says the named point is the one exception.
3. Premise objections: accepted. D2 sends them to the Maintainer with the author's reply.
4. Terms: accepted in part. "Joined run" is defined in D5 and each preflight question is named. "Return visit" and "arc" were already defined.
5. Length and the abstract-only study: accepted in part. The study is removed. The text stays above the target, at 1,926 words: five linked changes and a summary that reads alone did not fit in less, and the findings added about 90 words.

**Security Review**

1. Blocking, the implementer could edit the test: accepted. D2 and S1 carry the reviewer's sentence.
2. Blocking, a declined Security finding: accepted, by the sentence of usual finding 1.
3. D4's brief: accepted. A Security reviewer may read any file the addition touches, and the brief names the first review of the same kind.
4. S2's revert had no owner: accepted. S2 now rests on the recorded failing and passing runs.

The Security reviewer's report doubted the lines cited for `docs/methodology/dual-review.md`. I checked: the sentence is on lines 342 and 343, as cited.

**Elapsed**: about 10 minutes (estimate). **Tokens**: unknown. The harness reported 82,249 tokens and about 2.5 minutes for the usual review, and 79,388 tokens and about 1.7 minutes for the Security Review.

### Withdrawn / superseded commitments

- S2's "reverting the fix fails it again": replaced by the recorded failing run before the fix and passing run after it. No one owned the revert.
- The outside study in Rationale: removed. It had been read by abstract only.
