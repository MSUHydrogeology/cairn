# Plan: One round of review at each stage

**Source proposal**: dev/proposals/archive/2026-11-20-claude-one-round-reviews.md
**Status**: archived
**Plan review**: required(Internal)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/working-agreements.md, dev/rules/protected-surfaces.md, dev/rules/conventions.md
**In brief**: Each review stage gets one round, and a reviewer who blocks work supplies the test or the exact words that close the finding, so fixes are not read a second time and plans stay smaller.

## Build summary

After this plan, the review rules say five things in every place that now says otherwise: each stage (proposal, plan, code) gets one round; a reviewer who blocks work supplies the failing test or exact words that close the finding; Security Review normally takes one pass, not two; code is reviewed once, after the last chunk; and a plan has at most five chunks. The change is exact text replacement in 16 prose files (26 replacements, 42 applications counting shipped twins), plus a changelog entry, one roadmap row and a refreshed install lock. No code, test, status name or lifecycle edge changes.

## Source proposal

The Maintainer accepted option C of the one-round proposal as revised, at the standard tier ("Accept at Standard Tier.", chat, 2026-11-20): one usual plan review and one usual code review, and no Security Review pass. The design is settled in its D1 to D7 and its appendix lists the rule homes. This plan carries it out and re-opens nothing.

## Scope

**Result.** Cairn's governing text, its shipped twins and the published methodology pages state one rule set in the same words. Fewer second reads of fixes follow, and plans stay at five chunks or fewer. The wording of the governing paragraph is the proposal's D1; the other homes are written from D1 to D7.

**Where the new rules start (D7).** They apply to proposals and plans opened after the change ships. This plan runs under today's rules.

**Edit list.** The exact Find and Replace text for all 28 replacements is in `dev/plans/archive/2026-11-20-one-round-reviews-edits.md`. A separate file is needed because the text is about 2,300 words, over twice this plan's body target, and a Low-tier implementer must not design any of it. Each Find text was checked to occur exactly once in every target at `849eab4c`, and the list as first written was applied in a scratch checkout without error. The coordinator then added M12 and M13 (the diagram labels) and moved R2 to the roadmap as it stands on `0.9-dev`; those three were checked for a single match and have not been rehearsed. Shipped twins get identical replacements and the shipped text names no model or vendor.

**Must not change.** The status names and edges of the lifecycle: no node or edge is added or removed, and only the five edge labels that state the removed conditions are reworded (M12, M13); the targeted look after a failed joined integration run (`docs/methodology/dual-review.md` lines 342-343, `docs/methodology/plans.md` lines 575-576); when a Security Review applies; tiers; fences; Decisions; model floors; required checks; the certifying run. No Python, installer structure or functional configuration is touched. No file is in the gate manifest, so no re-anchor is owed.

**Home the appendix missed.** `docs/methodology/lifecycle-contract.md` line 98 ("only when it widened scope") says when a proposal returns for a further review; edit M10 aligns it with D1.

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

Governing text (`AGENTS.md` and its shipped twin, the collaboration guide pair), the plan and proposal template pairs, four pages under `docs/methodology/`, and the security-review and testing-discipline module pairs.

## Sequence

Estimate: 1 to 2 hours of Low-tier work for C1 to C5 (my guess, not measured). Uncertain: another session may hold an uncommitted edit on a shared file, which makes the chunk wait.

**Every chunk.** A Low-tier implementer, the model named at spawn. Work in the Git worktree and on the branch the coordinator names, made from `0.9-dev` (the roadmap's working rules allow a worktree for implementation); stop if `git branch --show-current` prints `0.9-dev` or `master`. The coordinator merges the branch into `0.9-dev` once the code review has passed; the implementer never merges or pushes. Claim the chunk's files with `dev/tools/intent.py claim` before editing and release the claim after the commit. Run `git status` and `git log -5 -- <chunk files>` and stop on another session's uncommitted edit to any of them. Apply each edit of the chunk, in order, to each target it names: write the Find block and the Replace block to two scratch files with no added final newline, then run `C:\ProgramData\Anaconda3\python.exe dev/tools/exact_replace.py <target> --old-file <find> --new-file <replace>`. Expected: `Applied exactly one replacement sequence.` If it says `No write: match count 0`, stop and tell the coordinator; never improvise text. If it says `Refused without write: input path changed while reading` (seen once when two edits hit one file within a second), run that edit again. Do not rewrap or regenerate text. Then `git diff -U0` shows only Find text removed and Replace text added. Commit once per chunk with explicit paths, never push; the message lists the edit ids and each check's result.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Governing text | plan review accepted | `AGENTS.md`, `templates/core/AGENTS.md`, both collaboration guides (A1, G1 to G5) |
| C2 | Templates | C1 | both plan templates, both proposal templates (T1 to T3, P1, P2) |
| C3 | Methodology pages | C2 | `dual-review.md`, `plans.md`, `lifecycle.md`, `lifecycle-contract.md` under `docs/methodology/` (M1 to M13) |
| C4 | Modules | C3 | both `security-review.md`, both `testing-discipline.md` (S1, TD1) |
| C5 | Records, install lock, selected tests | C4 | `CHANGELOG.md`, `dev/PLANNING.md` (R1, R2); then the lock alone |

The chunks state one rule, so run them in order.

## Acceptance criteria

**C1.** `AGENTS.md` and `templates/core/AGENTS.md` carry the D1 paragraph less one sentence (see Scope delta), 63 words replacing 59. `AGENTS.md`, `CLAUDE.md` and `RULES.md` total 1,592 words, at most 2,000; the shipped `AGENTS.md`, `VENDOR.md` and `RULES.md` total 1,497, at most 1,500. (Amended 2026-11-20 after code review: as opened, this cell said 80 words, 1,609 and 1,441, and counted two of the three installed files.) Each guide holds the closing-finding paragraph, the Maintainer-added-scope paragraph, the five-chunk and code-once sentence, and the amendment pointer. `git grep -n -F "to the reviewer for a targeted look" -- dev/agent_collaboration.md templates/core/dev/agent_collaboration.md` prints nothing. The two guides' added and removed lines are identical.

**C2.** Neither plan template says "A second code-review pass runs only when". The plan template's Sequence line names five rows; the proposal template says "unless the Maintainer adds scope". Each twin pair's added and removed lines are identical, and no changed line sits inside a `cairn:slot` block.

**C3.** None of the four pages keeps "at most two passes", "code pass only for defects", "only when the revision introduced new defects" or "only when it widened scope". Lines 342-343 of `dual-review.md` and 575-576 of `plans.md` are untouched. Each diagram keeps every node and edge; only the five edge labels are reworded (M12, M13).

**C4.** Both `security-review.md` copies say "stops after one pass" and keep the sentences that need a named question and Maintainer authorization for a further pass. Both `testing-discipline.md` copies say a reviewer-written closing test is scratch work unless it guards a listed promise. Each pair's added and removed lines are identical.

**C5.** `CHANGELOG.md` has one entry under `## Unreleased` and `dev/PLANNING.md` one v0.9 row. `verify_integrity` reports OK for 70 files. The lock commit holds `dev/.cairn/cairn-lock.yml` alone, six hash lines changed. The selected tests pass, and the sweep below prints nothing.

## Scope delta

**Scope delta**: degraded, by one sentence in one home. Every home in the appendix is covered, plus one the appendix missed (M10) and the five diagram labels that state the same removed conditions (M12, M13). The checks D6 sets (recount at the end of v0.9) get a roadmap row (R2).

- Removed from edit A1, in `AGENTS.md` and `templates/core/AGENTS.md`: "A blocking finding states what closes it: a failing test for code, exact words for a document." With it, the installed `AGENTS.md`, `VENDOR.md` and `RULES.md` total 1,514 words against the standing limit of 1,500 that `tests/test_scaffold.py` holds. The sentence was cut, not reworded: Strategy's shorter drafts of the paragraph each weakened the wording of the Security Review cap. The rule stays in force in both guides ("Closing a blocking finding") and in the plan template. The Maintainer (chat, 2026-11-20): "Fix this one now by dropping the sentence." **disposition**: accept

## Verification

**Promises.** Agents reading these rules get one consistent set; adopters upgrading get the same text in the shipped twins. Entry points: the edited texts and the lock check. No caller-visible behavior changes.

**Selector.** `C:\ProgramData\Anaconda3\python.exe tests/tier_inventory.py for <the 19 changed paths> --range <BASE>..HEAD`, where BASE is the commit before C1. At opening, with a stand-in range, it selects 23 test files (30 more `AGENTS.md` readers are omitted above its guard; do not widen). C5 runs exactly the selected files with `C:\ProgramData\Anaconda3\python.exe -m pytest -q -p no:cacheprovider <files>`, once, after the lock commit; no baseline was measured, so a failure that names none of the edited text is reported, not fixed. Record the count of selected files in the C5 commit message (D6). Never set `CAIRN_FULL_SUITE=1`.

**Prose gates, per changed `.md` file after each chunk** (one file per call; each prints OK and exits 0): `dev/tools/claim_check.py <file>`, `dev/tools/link_check.py <file>`, `tests/check_cairn.py <file>`, `dev/tools/sync_doc_snippets.py --check <file>`. Once per chunk: `tests/quality_gate.py --sub neutrality` (expect `fail=0`). Also `git diff --check` (no output). All were clean in the scratch checkout.

**Twin parity.** For each pair, the added and removed lines match: `$a = git diff -U0 <BASE>..HEAD -- <source> | Where-Object { $_ -match '^[+-]' -and $_ -notmatch '^(\+\+\+|---)' }`, the same for the twin as `$b`, then `Compare-Object $a $b` prints nothing.

**Sweep (C5).** This prints nothing (no match, exit 1):

```
git grep -n -E "A second code-review pass runs only|to the reviewer for a targeted look|at most two passes|stops after two passes|code pass only for defects|A second pass is only for widened scope|add a second only for widened scope|only when the revision introduced new defects|only when it widened scope|advance without a third read|code gets a second pass only|revision introduced new defects|revision widened scope" -- . ':!dev/proposals' ':!dev/plans' ':!*/archive/*' ':!CHANGELOG.md' ':!dev/PLANNING.md' ':!tests' ':!dev/reflections' ':!dev/measurement' ':!dev/strategy'
```

Known-positive control: run it with `-c` and `<BASE>` placed after the pattern (`git grep -c -E "<pattern>" <BASE> -- ...`); it lists 11 files. No test or tool names the old phrases (searched `tests`, `dev/tools`, `install`, `templates`, `release`).

**Lock (C5).** After C1 to C4, `C:\ProgramData\Anaconda3\python.exe install/verify_integrity.py --target .` lists six modified files (`AGENTS.md`, `dev/agent_collaboration.md`, `dev/modules/security-review.md`, `dev/modules/testing-discipline.md`, `dev/plans/_template.md`, `dev/proposals/_template.md`); that is expected. Run `C:\ProgramData\Anaconda3\python.exe install/scaffold.py upgrade --target . --finalize AGENTS.md dev/agent_collaboration.md dev/plans/_template.md dev/proposals/_template.md dev/modules/security-review.md dev/modules/testing-discipline.md`. Expected: `advanced 6 hash(es) (scoped to 6 path(s))`; then `verify_integrity` prints `OK -- 70 recorded file(s)`. Commit the lock alone. Precedent: `d9e7629a` and `093d7951`. Measured in a scratch checkout; not yet run on the real tree.

**Does any rule weaken or disappear?** Yes, openly, as the proposal says: the second Security Review pass, the second code pass for new defects, and the second read of a fix larger than a failing test. Kept: the further-pass path with Maintainer authorization and a named question, the cap path to the Maintainer, and the targeted look after a failed joined run. Code review follows (fresh, Medium).

Length: the opening body runs about 1,600 words against the 1,000 target. The overrun is the commands and expected results a Low-tier implementer needs; all replacement text is in the edit list.


## Plan review -- Claude Sonnet 5.5, Reviewer -- 2026-11-20

Reviewed commit: e410191aeaab5439ff4afa36a19fc9d9315876f3

**Obligation**: the required Internal plan review in the header.
**Tier**: Internal
**Findings**: raised (non-blocking only)

The plan aims to put the accepted one-round rules into every home as exact text, so a Low-tier implementer designs nothing. It does. I applied all 28 edits in a throwaway detached worktree: every Find matched once in every target, the old-phrase sweep printed nothing, and `verify_integrity` listed the six expected files, then the finalize step advanced 6 hashes and it reported OK for 70 files. The prose gates, the neutrality gate (`fail=0`) and `git diff --check` were clean. M12, M13 and R2 matched once; R2 is a three-cell row in section 2.

**Foundations**
1. **Should this happen as framed?** Yes; the Decision set option C at standard tier and the edits carry D1 to D7 -- compare the archived proposal's D1 to D7 with `dev/plans/2026-11-20-one-round-reviews-edits.md`.
2. **Best alternative.** None simpler: edits are single-paragraph replacements; the extra edit list is justified by size -- `wc -w` on the plan body.
3. **What would show it wrong.** The old-phrase `git grep` sweep printing any hit after C4, or `Compare-Object` on a twin pair printing a line -- both run and clean in rehearsal.

**Does any rule weaken or disappear?** Only what the Decision named. The joined-run targeted look stays (`dual-review.md` 342-343, `plans.md` 575-576).

- N1 (non-blocking): the edit id `D1` (testing discipline) shares a name with the proposal's D1 (the governing paragraph), and C1's criteria and C4 use both. Rename it, for example `TD1`, if convenient.
- N2 (non-blocking): G3 drops the guide's general "targeted look" sentence while the two methodology pages keep the joined-run one. The appendix asked for this; code review should confirm the two read as compatible.
- N3 (non-blocking): M1 and T1 omit "a substantive plan amendment", a further-pass ground in A1. Amendment review is separate (`plans.md` 353), so no rule is lost.

**Not covered** (this pass runs over the 300-word target to carry the rehearsal evidence): I did not run the test selector (needs commits), the selected tests, or the C5 commands on the real tree; I did not read every shipped document for paraphrases beyond one broader grep.

**Verdict**: ACCEPT; fold N1 to N3 as the author sees fit.

**Elapsed**: about 15 minutes (estimate). **Tokens**: unknown.

## Plan response -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-20

The review accepted the plan with three non-blocking notes. Strategy made the design, so Strategy answers them.

1. **N1, the edit id `D1`**: accepted. The testing-discipline edit is now `TD1` in the edit list and in the Sequence table, so `D1` means only the proposal's governing paragraph.
2. **N2, the general "targeted look" sentence**: no change. The proposal's D2 replaces it and D7 keeps the look after a failed joined run. The code review confirms that the two read as compatible.
3. **N3, "a substantive plan amendment" is not named in M1 and T1**: no change. Amendment review is its own path in `docs/methodology/plans.md`, and A1 names it in the text every agent reads.

One operative sentence changed with this fold, on the Maintainer's direction of 2026-11-20 as recorded in the roadmap's working rule: the coordinator merges the implementation branch into `0.9-dev` once the code review has passed.

The plan is ready to implement.

**Elapsed**: about 5 minutes (estimate). **Tokens**: unknown. The harness reported 112,010 tokens and about 4 minutes for the plan review, and 238,417 tokens and about 19 minutes for writing the plan.

## Implementation verification -- Claude Haiku 5.5 (Implementation, Low) -- 2026-11-20

**BASE**: `76347908`. Branch `one-round-reviews-impl` (checked before any edit: branch, base commit and both plan files were present).

**Commits**:
- `5398b059` Step 0: header set to `implementing`, alone.
- `622fa357` C1 (A1, G1 to G5). Checks: claim_check, link_check, check_cairn and sync_doc_snippets --check OK on the four files; neutrality `fail=0`; `git diff --check` clean; "to the reviewer for a targeted look" absent; word counts 1,609 (AGENTS.md, CLAUDE.md, RULES.md) and 1,441 (templates/core AGENTS.md and VENDOR.md); twin parity identical.
- `87adc861` C2 (T1 to T3, P1, P2). Gates OK on the four files; neutrality `fail=0`; diff check clean; old phrase absent; changed hunks lie outside every `cairn:slot` block; twin parity identical.
- `d7c330c4` C3 (M1 to M13). Gates OK on the four pages; neutrality `fail=0`; diff check clean; old phrases absent; no hunk touches dual-review.md 342-343 or plans.md 575-576; arrow-line counts in the three diagram files unchanged from HEAD.
- `c8c6bb8d` C4 (S1, TD1). Gates OK on the four files; neutrality `fail=0`; diff check clean; "stops after two passes" absent; twin parity identical.
- `a14c3409` C5(a) (R1, R2). Gates OK on CHANGELOG.md and dev/PLANNING.md; neutrality `fail=0`; diff check clean. The apply tool printed `NOT COMPARED` for CHANGELOG.md (outside the functional-prose roots); this is informational, not a failure.
- `0426db19` C5(b) lock, alone. Before finalize, `verify_integrity` listed exactly the six expected files. `scaffold.py upgrade --finalize` printed `advanced 6 hash(es) (scoped to 6 path(s))`. Then `verify_integrity` printed `OK -- 70 recorded file(s)`. Diff: six hash lines changed.

**Selector (C5(c))**: `tests/tier_inventory.py for` with the 19 changed paths and `--range 76347908..HEAD` selected **23 test files**, the same count as the plan's stand-in.

**Test run**: `python -m pytest -q -p no:cacheprovider` on those 23 files, once, without `CAIRN_FULL_SUITE`: **127 failed, 715 passed, 10 skipped** (1001.81 s). Failures by file: `test_portable_security_sweeps.py` 105, `test_upgrade_module_additions.py` 11, `test_board_json_contract.py` 7, `test_replacement_tools.py` 2, `test_install_report_slots.py` 1, `test_scaffold.py` 1. Observed causes in the output (not verified against a baseline): 13 failures show `OSError: [WinError 10106]` from socket setup; many sweep failures mention the gitleaks adapter; several failures are symlink tests on this Windows host. Not fixed, per the plan. The plan's C5 criterion "the selected tests pass" is therefore **not met**; no baseline was measured, so I cannot say which failures predate this change.

**Mistake during the run**: my first pytest command built its file list with a bad grep, so pytest received no file arguments and collected the whole tree. It stopped after 18.9 s on a collection error (`templates/modules/team-gated/test_coupling.py`, import file mismatch) before any test ran. That run did not use the selector's list. I then ran the correct 23-file command once. No other test was run.

**Sweep (C5)**: the plan's `git grep` command printed nothing (exit 1).

**Did not match the plan**: none in the edit text. The one deviation is the mis-run above. Status is set to `awaiting-code-review` as the plan's last step requires, but the test criterion is unmet, so the reviewer should read the failure list above.

**Skipped**: no baseline test run at `76347908`; no full-suite run (not allowed).

**Elapsed**: about 45 minutes of implementation plus the 16 min 41 s test run (from the pytest summary). **Tokens**: unknown.

## Code review -- Claude Sonnet 5.5 (Reviewer, Medium) -- 2026-11-20

Reviewed commit: fe52e1c6 (range `76347908..fe52e1c6`)

**Obligation**: the usual code review the Decision set (standard tier); no Security Review pass.
**Findings**: one blocking (open check, not a text defect), two non-blocking.

The change aims to state one round per stage in every home, in identical words across shipped twins. It does. A script applied all 28 edits to the base text of each of the 18 target files and compared the result with the head text: all identical, every Find matched once, nothing added or lost. The lock commit touches only `dev/.cairn/cairn-lock.yml`, six hash lines. Shipped twin text names no model or vendor. The plan's old-phrase sweep prints nothing.

**Foundations**
1. **Should this happen as framed?** Yes; it carries D1 to D7 as exact text -- the script above against the edit list.
2. **Best alternative.** None simpler -- exact replacement is the lightest mechanism.
3. **What would show it wrong.** A selected test failing on head but passing at base -- the coordinator's two-tree run.

**Does any rule weaken or disappear?** Only what the Decision named (second Security pass, second code pass, second read of a fix). The further-pass path, cap path and named-question rule remain.

- **B1 (blocking, open check)**: "the selected tests pass" is unmet: 127 failed with no baseline. It closes when the same 23 files at base and head fail the identical set of tests and counts. A test failing only at head is a defect: fix the edited text, not the test. A difference confined to host failures (sockets, symlinks, gitleaks) at both ends settles it; record that in the plan.
- **N1 (non-blocking)**: `dev/agent_collaboration.md` 283 says "no second read of the fix follows", while `dual-review.md` 342 and `plans.md` 576 keep a targeted look after a failed joined run. Compatible in practice (separate trigger), but the guide never says so. Optional: add "except after a failed joined integration run" at 283.
- **N2 (non-blocking)**: implementer's mis-run test command is recorded honestly; no action.

**Not covered**: no test run; no read of every methodology page beyond the edited passages and a phrase search.

**Verdict**: REVISE until B1 is recorded; text is otherwise ACCEPT.

**Elapsed**: about 20 minutes (estimate). **Tokens**: unknown.

## Code-review response -- Claude Fable 5.2 (Strategy, acting as implementer) -- 2026-11-20

Strategy coordinated this plan and ran the comparison the review asked for, so Strategy answers. The implementing session (Claude Haiku 5.5) had ended.

- **B1, the selected tests: closed, after one defect was found and fixed.** The same 23 files ran once each on this Windows host. At the starting commit `76347908`: 126 failed, 716 passed, 10 skipped. At `fe52e1c6`: 127 failed, 715 passed, 10 skipped. One test failed only after the edits, `tests/test_scaffold.py::TestRulesMdStarter::test_full_install_seeds_rules_md_within_word_budget`: edit A1 took the installed `AGENTS.md`, `VENDOR.md` and `RULES.md` to 1,514 words against a limit of 1,500. As the review directed, the text was fixed and the test left alone. One sentence came out of both `AGENTS.md` copies (`e1b3f0b8`; lock `54672430`), on the Maintainer's word (Scope delta). Rerun at `54672430`: 126 failed, 716 passed, 10 skipped. The failing set is identical to the starting commit's: no test fails at only one end, and the word-limit test passes. The failures common to both ends are this host's (sockets, symlinks, the gitleaks adapter); their home is the Windows item in section 1 of `dev/PLANNING.md`.
- **N1: accepted.** Both guides now end that sentence "except after a failed joined integration run." (`91dee1d2`; lock `26c3af13`).
- **N2: no action.**

Three plan cells were amended to match what shipped: C1's word counts, the Scope delta, and edit A1 in the edit list. The prose gates, the neutrality gate, twin parity for the two `AGENTS.md` copies and the C5 phrase sweep were rerun after the fix and pass.

Not run: the selected tests on the canonical runtime. Not rechecked: the other 18 changed files, which no commit touched after the review.

**Elapsed**: about 75 minutes, of which about 48 were three background test runs. **Tokens**: unknown.

## Implementation closeout -- Claude Fable 5.2 (Strategy) -- 2026-11-20

C1 held as amended: both `AGENTS.md` copies carry the paragraph at 63 words; Cairn's own three files total 1,592 words and the installed three 1,497, measured on the merged tree at `4bc4f90e`. C2, C3 and C4 held (implementation verification at `fe52e1c6`; code review `023ee592`). C5 held except its test criterion, which is settled by comparison and not by a clean pass: the 23 selected files fail the identical 126 tests at the starting commit and at `54672430`. The lock was refreshed three times, each in a commit of its own (`0426db19`, `26c3af13`, `54672430`), and `verify_integrity` reports OK for 70 files on the merged tree. The branch, 15 commits changing 21 files, merged into `0.9-dev` at `4bc4f90e`.

Not run: the selected tests on the canonical runtime. Home: `dev/PLANNING.md`, section 1, the paragraph "Accepted on 2026-11-20", which names the defect arc's one joined run.
Not covered: the 126 selected tests that fail on the Windows host before and after the change. Home: `dev/PLANNING.md`, section 1, "Windows".
Remaining: the recount of review passes at the end of v0.9 (D6). Home: `dev/PLANNING.md`, section 2, row "Recount review passes under the one-round rule".
Remaining: the sentence removed from `AGENTS.md` may be restored. Home: `dev/PLANNING.md`, "After the defects: a comprehensive tightening of the rules".

Dispositions: the Scope delta's one entry is `accept`, with the Maintainer's words quoted there. No other follow-up is deferred.

**Benefit versus cost**: unknown -- one round of review at each stage, stated in every rule home; cost: 15 commits and one merge, two review passes and no return visit, three background test runs of 16 to 17 minutes each, about 1.14 million subagent tokens across the proposal and this plan as the harness reported them (Strategy's own use is unknown), and 4 more always-loaded words in each rule set; remaining burden: no code and no test added. Revisit at the D6 recount at the end of v0.9.

**Elapsed**: one working day from the proposal's opening to the merge. **Tokens**: unknown beyond the subagent figure above.
