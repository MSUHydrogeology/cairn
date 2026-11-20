# Appendix: the counts and the edit list behind "One round of review at each stage"

These tables back the proposal's numbers. They are counts from headings, taken at commit `effb7493` on 2026-11-20 over plan and proposal files whose names start with a date of 2026-11-01 or later (73 plans, 91 proposals).

**Method.** Count the level-2 headings whose subject (the text before the first " -- ") names a review and is not a response. One round at a stage is at most one usual pass and one Security Review pass, so three or more passes at a stage means a further pass. A pass counts as a *return visit* when its heading says revision, pass 2, second, targeted, return, look, follow-up or continuation. The return-visit figure is therefore a floor. The verdict classes come from reading each return visit's verdict line, not the whole review.

The counting scripts are scratch files and are not committed. The method above is enough to repeat the count. I re-ran the three scripts and every figure below matched the Strategy brief, except where noted.

## Plans: passes by stage

| Stage and kind | Passes | Plans with at least one | Plans with two or more | Marked as return visits |
|---|---|---|---|---|
| Code, usual | 144 | 73 | 40 | 34 |
| Code, Security | 101 | 62 | 21 | 23 |
| Plan, usual | 105 | 73 | 28 | 4 |
| Plan, Security | 40 | 38 | 2 | 1 |
| Plan amendment, usual | 9 | 5 | 2 | 0 |
| Plan amendment, Security | 3 | 3 | 0 | 0 |
| After archive, usual | 6 | 5 | 1 | 1 |
| After archive, Security | 5 | 2 | 1 | 0 |
| **Total** | **413** | | | **63** |

Median 5 passes per plan; 30 plans have six or more.

| Stage | Plans with three or more passes | Passes beyond two, summed |
|---|---|---|
| Plan | 5 of 73 | 8 |
| Code | 43 of 73 | 103 |
| Plan amendment | 1 of 5 | 2 |
| After archive | 1 of 5 | 4 |

Words: 110,339 in operative text and 346,646 in appended records (76% of 456,985). The median plan is 954 words as written and gains 2,889.

## Plans: the 63 return visits

Eight asked for more work (five usual, three Security). Two of the eight named a new defect made by the fix: `2026-11-06-safe-git-reads.md` ("Revise; one blocking new defect") and `2026-11-13-focused-verification.md` ("REVISE. This pass addresses a new repair defect"). The other 55 confirmed the fix, or I could not class them from the verdict line.

The script's own automatic bins differ from my reading. It puts 13 in "asks for more work" and 39 in "confirms the fix". Five of its 13 say ACCEPT or "closed" in the verdict, so I moved them. The Strategy brief gave "about 48 confirmed, 7 unclassified"; I count about 44 confirmed and 11 unclassified. The eight "more work" cases agree. Of the 24 Security return visits, 3 asked for more work.

## Proposals

91 files, 199 passes (115 usual, 84 Security), median 2 per file. 21 of 90 files with a review have three or more passes (31 beyond two). 70 files have a Security pass. 15 passes in 13 files are marked return visits. Words: 116,801 operative, 97,989 appended (46%).

## Plans: chunks and cost

72 of 73 plans have a readable Sequence table. I corrected one count by hand: the script reads 32 rows in `2026-11-16-heavy-tier-trigger.md`, but its chunks are C1 to C7.

| Chunks | Plans | Median passes | Median commits to the plan file |
|---|---|---|---|
| 1 to 3 | 58 | 5 | 15 |
| 4 or 5 | 9 | 6 | 22 |
| 6 or more | 5 | 6 | 26 |

The five plans with six or more chunks have 6, 7, 9, 10 and 10, and all opened on 2026-11-16. Median 3 chunks overall.

| Opened | Size | Plans | Median passes | Median commits | Passes per chunk | Commits per chunk |
|---|---|---|---|---|---|---|
| 2026-11-13 or later | 1 to 3 chunks | 13 | 5 | 14 | 1.67 | 5.7 |
| 2026-11-13 or later | 4 or more | 7 | 6 | 26 | 1.00 | 3.5 |
| Before 2026-11-13 | 1 to 3 chunks | 45 | 5 | 16 | 2.48 | 10.3 |
| Before 2026-11-13 | 4 or more | 6 | 6.5 | 22 | 1.84 | 8.4 |

Across all 73 plans the plan file is committed a median of 17 times (maximum 149). The wide run the records call Boundary B is named in all 51 plans opened before 2026-11-13 and in 5 of the 22 opened since.

Largest plans: `2026-11-17-repository-layout.md` has 5 chunks, 15 review passes and 39 commits. `2026-11-05-agent-continuation.md` has six usual code-stage passes.

## Not measured

Tokens (most reviews record `unknown`), how many tests each plan ran, and whether larger plans have smaller chunks.

## Where the rule text lives (16 files, about 32 edits)

Line numbers are at commit `effb7493`. Shipped twins change in the same commit as their source.

| File (and twin) | Line | What changes there |
|---|---|---|
| `AGENTS.md`; `templates/core/AGENTS.md` | 19; 32 | Replace the paragraph with the D1 text. |
| `dev/agent_collaboration.md`; `templates/core/dev/agent_collaboration.md` | 365; 372 | Replace the "targeted look before Boundary B" sentence with the closing-finding rule. |
| same | 281; 286 | Add the one exception to the fresh-reviewer rule for Maintainer-added scope. |
| same | 301; 306 | Add the five-chunk target beside "A plan may group dependent chunks". |
| same | about 306 to 313; 311 to 318 | Add the one exception to the amendment sentence for Maintainer-added scope. |
| `dev/plans/_template.md`; `templates/core/dev/plans/_template.md` | 448; 448 | Replace "A second code-review pass runs only when the revision introduced new defects". |
| same | 106; 108 | Plan review has one round: add the Maintainer-added-scope exception. |
| same | "Keep the plan short"; Sequence | State the five-chunk target the plan review checks. |
| `dev/proposals/_template.md`; `templates/core/dev/proposals/_template.md` | 52; 35 | "One usual proposal review and response suffice": add the Maintainer-added-scope exception. |
| same | 174; 157 | "Do not split work into plans by default": add that more than five chunks is cut into plans. |
| `docs/methodology/dual-review.md` | 211 to 245 | Caps and closure: Security Review one pass; drop the second code pass; add the closing-finding rule and the added-scope exception. |
| same | 247 | Plan review: the added-scope exception to freshness. |
| `docs/methodology/plans.md` | 69 | Drop "only when the revision introduced new defects". |
| same | 897 to 914 | Multi-round review: one Security pass; keep the authorized further pass; revise the "round 2" skeleton text. |
| same | 84 | Add the five-chunk target to "Do not split work by default". |
| `docs/methodology/lifecycle.md` | 170; 274 | Say a further proposal or code pass happens only on added scope or Maintainer authorization. |
| `docs/methodology/lifecycle-contract.md` | 153 | Same for the code-review transition row. |
| `dev/modules/security-review.md`; `templates/modules/team-gated/security-review.md` | 84; 84 | "Normally stops after two passes" becomes one pass. |
| `dev/modules/testing-discipline.md`; `templates/modules/team-gated/testing-discipline.md` | 44; 44 | One sentence: a reviewer-written closing test is a developmental test and is deleted before archive. |

Left unchanged on purpose: the lifecycle diagrams and status edges (`dev/plans/_template.md:22`, `docs/methodology/plans.md:35`, `lifecycle.md:243`, `lifecycle-contract.md:131`), and the targeted look after a failed joined run (`dual-review.md:343`, `plans.md:576`). I grepped `tests/` and `dev/tools/` for the changed phrases and found none; I did not search every shipped document for paraphrases.