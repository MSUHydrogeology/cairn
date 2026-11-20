# Testing in LHM and modflow_tools: take the rules and three guards now, let the ledger prove itself first

**Author**: Claude Fable 5.2 (Strategy)
**Model**: claude-fable-5-2
**Date**: 2026-11-20
**Status**: settled
**Type**: comparative-research
**Surfaces this would feed**: the v0.9 rule-tightening proposal (not yet written); the roadmap row "Test records, so a release reuses current results" (#81, #92) in `dev/PLANNING.md`; the Maintainer's pending worktree question in LHM.

## Summary

The Maintainer asked for an assessment of LHM's testing rules and tools and of modflow_tools' strategy notes and proposals. Four conclusions:

1. **LHM's rules are the best asset either project has on testing.** Cairn should take the short ones in the v0.9 tightening.
2. **The two tools that remember passing tests are one idea built twice.** Neither is ready for Cairn. modflow_tools' design already says how it reaches Cairn: after it passes a measured gate.
3. **Both projects, and Cairn today, met the same three ways for a test run to look green when it is not.** Guarding them is cheap and belongs in v0.9.
4. **One LHM finding needs the Maintainer soon.** In most LHM worktrees a test may be checking the main checkout's code, not the worktree's.

## The question

The Maintainer (chat, 2026-11-20): "assess LHM's testing hierarchy tooling and ruleset, as well as the strategy/proposal docs in modflow_tools". The roadmap row on test records waits on evidence from both.

## Method

Two medium-tier agents (Claude Sonnet 5.5) inventoried both repositories, read-only. I then read the source of each claim below: LHM's testing rule file (2,511 words), the measurements in its test-records plan and one reflection; modflow_tools' test-ledger proposal and core strategy note (branch `test-ledger-proposal`) and its slow-test note. Nobody ran their tools or tests. Cairn's numbers are this session's, on the Windows host. The note is wrong if the ledger passes its gate and also pays on Cairn's own suite, which is unmeasured.

## Findings

**What each project has.**

| | LHM | modflow_tools | Cairn |
|---|---|---|---|
| Levels | default and slow, set by a hand-kept list of 120 files | six, by folder, plus a `slow` mark authors set | folders and a tier listing |
| Choosing tests for a change | trace what reaches the changed lines | tests that name the changed file | tests that name the changed file |
| Remembering a pass | built: one record for each test file | proposed: one record for each test, shared across worktrees | none |

**LHM's rules follow from its costs.** Preparing inputs takes days and a model run takes weeks. The short rules travel: "Run the narrowest set that can fail." "Never run the whole suite by default." "Measure a baseline once per commit and reuse it." "Never run a test file twice for one answer." "A test stays only if a promise or a named fault earns it."

**They are too long to ship as they are.** Single bullets run near 300 words, and the test README has 28,822 words. Two files disagree on who verifies a model change, and two on how a test gets its level.

**LHM's rules contradict a rule Cairn ships.** Cairn says to run the tests that name a changed file. LHM says not to search by name, because a name search finds tests that cannot reach the changed code. Cairn's own result today agrees with LHM. A one-paragraph edit to `AGENTS.md` selected 23 test files, 852 tests and 16 minutes, and held back 30 more files that read `AGENTS.md`. One test's result changed.

**The two memory tools.** A memory tool records that a test passed, with the files it depends on, and skips the test until one of those files changes.

- *LHM's is built* (1,728 lines). Replayed over 786 commits, the median commit leaves 22% of default tests and 30% of slow tests to rerun; the means are 46% and 49%, because commits are either small or sweeping. Its one timed run took 2.1 times the prediction. No release has used it, and 1 of 320 worktrees writes a record.
- *modflow_tools' is designed, not built.* It measured first: 6,720 tests take 3,690 seconds, and the 57 files that start another program hold 68% of that time. A tool that cannot see inside those programs "saves almost nothing". So the proposal builds one phase and stops unless at most 25% of run time must always run and a rerun after a one-file edit takes under 10% of a plain run. Estimated size: 2,500 to 4,500 lines. It awaits review, at top priority (Maintainer, 2026-11-18).
- *The design names Cairn as owner of the core*, as a file format and commands, not a Python library. The Maintainer (2026-11-17, quoted there): "it's core, should be language agnostic as much as possible." If the gate fails, nothing goes to Cairn.
- *Cairn's own suite may gain least.* 97 of its 135 test files mention `subprocess` (a name search, not a timing).

**Three ways a run looks green when it is not.**

1. *The test ran other code.* LHM is installed in "editable" mode: Python loads the package from one fixed folder, the main checkout. LHM measured that 319 of 320 worktrees import the frontend package from there. My inference, not tested: an agent who changes frontend code in such a worktree and runs the tests is testing the main checkout's copy. modflow_tools measured the same for programs its tests start. LHM's pending question (leave it, set up each worktree, or relax the check) and the ledger's check that the right code ran are one decision.
2. *The run ran nothing, or less than was chosen.* LHM: a merge gate passed with "no tests ran". modflow_tools: the tier tool picks a file, and the default settings then skip its slow tests without saying so. Cairn, in this session: my rerun of the 23 files ran no test and reported success, because the paths were malformed. I caught it only because 16 minutes had become one second.
3. *Old failures hide a new one.* Cairn, today: 127 failures on the branch, 126 of them present before the change. The implementer had no baseline and reported them as host failures. One was real: the installed rule files had passed their 1,500-word limit. LHM: 69 false baseline failures were reported as real for a day.

I found no rule for any of the three in Cairn's guide, entry file or testing module.

**Deleting tests saves upkeep, not time.** modflow_tools' first cut took a run from 213 to 196 seconds; its plan says deletion "gives the maintainability gain but little speed". Its roadmap (2026-11-18) records test code growing 3.5% over a stretch in which the package lost about 8,600 lines. A keep rule has to act when a test is written.

## Options

1. **Leave the roadmap row.** It no longer describes what the two projects are doing.
2. **Bring LHM's tool into Cairn now.** A new tool in a tightening release, and the one modflow_tools proposes to replace.
3. **Build the shared core in Cairn now.** Ahead of the evidence its own designers ask for.
4. **Take the rules and guards now; let the ledger pass its gate first.** Recommended.

## Recommendation

In the v0.9 tightening, as rules that replace existing words:

- **One short ladder in the guide**, built from the LHM rules quoted above, plus two more of its rules: a wider run states its reason, and a slow test is defended in its plan.
- **Three guard rules.** A run that executes no test, or fewer than were chosen, is a failure and says what it left out. A failure is called a host failure only against a baseline at the starting commit. A test run shows that the code under test came from the checkout it ran in.
- **Measure before changing how tests are chosen.** Find which of the tests that read `AGENTS.md` can fail from a wording change.

For the ledger, rewrite the roadmap row to match the facts: the modflow_tools proposal carries the work; Cairn receives the core only after the gate is passed and both projects have used it; LHM's tool is the baseline to beat on the same commits. Cairn builds nothing in v0.9.

For LHM, the Maintainer's call there: treat the worktree question as a question of correct results, not of records, and settle it once for both projects.

Residual risk: rules without a tool depend on agents following them. The guards would later want small tool changes, such as the tier tool failing on an empty run. Each needs its own go-ahead.

## Open questions

1. Answered on 2026-11-20: the Maintainer agreed with both. The roadmap row moved to v0.10 with the decision recorded, and the ladder and the three guards join the tightening proposal.
2. Is the worktree inference right? One changed line and one test in one LHM worktree would settle it. At the Maintainer's word the finding was passed to the LHM session on 2026-11-20; no result is known here.
3. Who measures how much of Cairn's own run time must always run, and when?
