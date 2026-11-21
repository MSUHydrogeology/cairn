# A consumer: a removal pass after each release, and plans that retire

**Author**: Claude (Strategy), drafted by Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — the pass removes tests and rules, some beside security guards; it changes the release process and files the gate manifest names; and one page protects a guard from removal.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md, dev/rules/conventions.md
**In brief**: After each release, one pass whose only job is to remove tests and rules that no longer earn their place, guarded by a page of what must stay, so Cairn stops only growing.

## Decision summary

**Conclusion.** Cairn only adds; nothing removes. I propose a "consumer": a pass after each release tag (the marked release commit) whose only verb is remove, guarded by one page, in your words, of what must stay. You see no test list. My pick for each choice below is marked.

**The problem you noticed.** Every role produces: an implementer adds tests, a reviewer adds findings, an incident adds a rule. You wrote (chat, 2026-11-20): "I personally love the idea of a consumer of rules and tests, because everything else is a producer of them." The release process answers with a sweep inside the release gate (the checks before a release) that hands you a list. Totals grew anyway, for your reasons (chat, 2026-11-20): the gate "takes most of a working day", and "I cannot review a list of tests to drop. It's not my role in this collaboration."

**The change, in five parts.**

- **A.** A finished plan's closeout (what shipped, checks run, what was dropped, where deferrals live) goes onto its proposal.
- **B.** After a tag, archived plans that the tag holds leave the tree. You said (chat, 2026-11-19): "Once we are done with plans at a release they are generally done. But the proposal is the project history."
- **C.** The consumer: a pass first after each tag, never inside the gate.
- **D.** One page, `dev/must-stay.md`, says what may never be removed. Four checks needing no judgment run after each sweep.
- **E.** The first pass, after the defect arc: the removing half of the tightening you asked for. You see three numbers: the gate's test run time, what left, what came back.

**Added:** one standing pass after each release (agent cost unknown), one page you own, one script, longer proposals. **Removed:** tests and rules that no longer earn their place, the gate's step for them, 210 archived plans (choice 1). **Risk left:** an agent misjudging a promise (what a test guards). Four guards: the page, the four checks, a second agent's review, and the tag, which still holds everything removed.

**Choices.**

1. **The 210 archived plans.** (a) Remove them in one step at the first pass, after each citing proposal gets a line naming the tag and path where its plan can be read (recommended). (b) Keep those; retire only plans archived from v0.9 on. (c) Keep all plans in the tree.
2. **How long may the gate's main test run take?** You set the number; the pass works toward it. I suggest 20 minutes (61 at 0.8).
3. **Does the consumer take over the rules-and-tests part of the seventh release sweep**, so the gate loses that step? (a) Yes (recommended). (b) Keep both for one release and compare.

The must-stay page is your statement. A first draft for Cairn is below; you may correct it at the Decision or any time after.

## Context

Measured by the strategy note (2026-11-19, from commit messages): the hand-run test cut of 8 to 13 November took test functions from 4,071 to 3,138 and put 34 back; seven days later the tree held about 270 more. Its plan ran to 26,430 words and 87 commits. The gate's main run took 61 minutes at 0.8.

Measured 2026-11-20 (`dev/measurement/agent-step-costs.md`, `dev/PLANNING.md`): the three files every installed project loads total 1,497 words against a limit of 1,500. Defect-arc plans B and C add two installer commands, a settings file and five test files and remove nothing.

Archived plans: 210 files, 53% of tracked Markdown words; none from an earlier release was edited later. Of the 0.8 window's proposals, 17 that a plan cites end at their Decision; their outcome sits only in the plan. 295 citations outside the archives name the plans archive (the note, idea 7).

## Proposal

All five outcomes are authorized; later ones wait on the board for their condition. Heavy: it removes tests beside security guards and changes the release process.

**A. Closeout on the proposal.** The plan and proposal templates tell the author to append a finished plan's closeout to its source proposal, as a light proposal does. The board and changelog then cite the proposal, not the plan. It ships to adopters in v0.9 and is B's prerequisite.

**B. Plans retire at the tag.** After a tag, each archived plan the tag holds, whose work has no open board row, is removed; a README in the archive folder names the tag. For today's 210, each citing proposal first gets one line naming the tag and path, then they go in one step, once. Two generator scripts, `tests/gen_legacy_passes.py` and `tests/gen_legacy_code_review_passes.py`, list both archives and the gate manifest names them: the plan for B treats them as protected files.

**C. The consumer.** An agent in the Implementation frame runs it first after each tag, never in the gate. It adds no text to `AGENTS.md` or `RULES.md`. Its licence is a new section "After the tag" in `release/RELEASE_PROCESS.md`, four lines:

1. It removes, merges, or moves a test to a later tier. It adds no rule and changes no behaviour.
2. It never removes a failing test, and never works on files an open plan is changing.
3. It never touches what a person has declared must stay.
4. It decides for itself and records each call: the item, the evidence, and what would show the removal was a mistake. A second agent reviews the sweep in one pass. The Maintainer is not shown a list of tests or rules.

A test whose promise still stands moves to a later tier first, so it still runs at release. Its searches and checks are low-tier work; a call on whether a promise still stands goes to a higher tier, as the testing guidance already says. Each removed item leaves one dated line; a restore adds one. It takes over the rules-and-tests part of the seventh release sweep (choice 3).

**D. Must-stay page and four checks.** `dev/must-stay.md` changes only by the Maintainer's Decision, plus a Security Review for a security guard. After each sweep: (1) every promise keeps a passing public check and every decision its sentence; (2) nothing still names a removed item as its guard, found by a script so it covers the same files each time; (3) nothing is gone that the sweep's record does not name, where "gone" is read from Git's comparison with the tag and not from the record; (4) one comparison on seeded faults (small deliberate breaks in the code) shows whether the new tests miss what the old caught. Checks 2 and 3 are one small script under `tests/`.

**E. First pass.** It runs on Cairn's tree in the v0.9 window, after the defect arc, first recording three starting numbers and its targets. A question reaches the Maintainer only when a promise looks out of date ("Does the model still need to reproduce this run?"). Adopter guidance, including a science project's page (reference runs, pass bands, checks against outside answers), waits for the first pass's result.

**Not covered.** The entering side (test ladder, rules that lapse unless renewed, smaller entry file) belongs to the tightening proposal after the defects (`dev/PLANNING.md`, "After the defects: a comprehensive tightening of the rules"); pruning alone cannot hold a total steady. The code-layout proposal is separate; this pass later folds copied code.

## Rationale

Agents decide because you cannot judge a list of tests; a sign-off you cannot judge is no control. Importance is written once, in your words. You asked (chat, 2026-11-10): "there should be a test AFTER the cuts."

## Alternatives considered

- **Keep the sweep inside the gate, with a list for you.** Totals grew; you cannot judge the list; the gate is most of a day.
- **Another one-off campaign.** The tree regrew within a week.
- **A "what can go?" question in every review.** A cue naming only removal draws more removal ideas than one naming both (the note's sources 20 to 22).
- **Limits alone.** A word limit forced a sentence out of `AGENTS.md` without anyone choosing the least useful one.

## Documentation / doctrine surface

Proposed paths:
- `dev/must-stay.md` — the must-stay page; lands with the first plan.

Edited in plans: `release/RELEASE_PROCESS.md`, the plan and proposal templates, `docs/methodology/plans.md`, the plans archive and its README, `tests/test_tiers.json` (the file that assigns each test file to a tier), the two generators.

## Evidence / verification plan

### Tests required

The script must find a planted removed test that a document still names as a guard, and a removal the record omits. The first pass records counts before and after (test functions, guidance words, gate minutes), the four checks' results, and next-window restores.

### Examples / smoke checks

A first draft of Cairn's must-stay page, for you to correct:

- Tests that security and release records name as guards.
- Refusal tests and hostile-state tests.
- Steps only the Maintainer takes: push, re-anchor, merge to master, Decisions.
- Refusals that protect data.

#### Security preflight

- **S1.** The pass reads the tree, the page and the sweep record, and changes tests, rules and archived plans. The record is written by the agent whose removals it describes, so the script does not take its word: it reads what is gone from Git's comparison with the tag and then looks for each item in the record.
- **S2, S3.** The script is shown failing on a planted removed test still named as a guard, and on a removal absent from the record. The agent that runs the pass runs the script after each sweep, over the same files, and the second agent reads its output.
- **S4.** It breaks toward keeping: an unreadable record or page stops the pass. It may not remove or weaken a security or release guard, a refusal test or a hostile-state test, and never edits the gate manifest, the baselines or anything the Maintainer signs. Only he changes the page. A removal shows afterward in the dated lines, script and tag.
- **S5.** Assumed: an agent that misjudges a promise. Still succeeds: a silent loss no declared promise covers. Closed by enumeration, not construction.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A defect traces to a removed test or rule. Restores stay zero for three releases (too timid) or are many in one (too bold). The gate's main run is no shorter after two passes. Questions to the Maintainer exceed a few a pass. Calls lack recorded evidence.

## Scope delta

**Scope delta**: preserved. Nothing accepted is dropped; two things move: the seventh sweep's rules-and-tests part, from the gate to after the tag, and archived plans, from the tree to the tag.

## Assurance path

**Assurance path**: high-assurance. The pass removes tests and rules beside security guards.

## Review -- Claude Sonnet 5.5 (`claude-sonnet-5-5`) -- 2026-11-20

```
Reviewed commit: 033cc5ca
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes in aim: a removal pass after the tag, outside the gate, with no list shown to the Maintainer, answers a measured regrowth. The framing misses that Cairn already has a rule for cutting tests (finding 1), and that moving a closeout breaks a tool (finding 2). -- `dev/rules/protected-surfaces.md` ("Tests exempt from the promise-only cut"); `dev/tools/board.py` lines 22-23.
2. **Best alternative.** Doing nothing keeps the gate's sweep, which grew anyway. The strongest alternative is to run the same pass but reuse the existing Security Review cut route for guards. -- `release/RELEASE_PROCESS.md` lines 19-22.
3. **What would show it wrong.** Forward test: after the first pass, replant one removed guard-named test and one record omission; the script must fail on both. Also a defect traced to a removed item, or a gate run no shorter after two passes (the proposal's signals). -- "Signals the change is wrong".

**Does any rule weaken or disappear?** Possibly: the existing rule says a test that a release document names as a guard is cut only through a Security Review. The proposal's one-pass second agent is weaker (finding 1).

The strongest version of the proposal: one removing role, run after the tag so the gate stays a day long, protected by a page the Maintainer owns and by checks that do not trust the remover. Conditions met: no list reaches the Maintainer, and the gate does not grow (choice 3 removes a step).

**Findings**

1. **Blocking.** The proposal does not mention the existing cut rule: tests of protected surfaces, the security-family files, tests named as guards, and refusal or hostile-state tests may be cut only through a Security Review. Licence line 4 sends the sweep to "a second agent ... in one pass". Replace licence line 4's last two sentences with: "It records each call. A removal or merge of any test or rule that `dev/rules/protected-surfaces.md` ("Tests exempt from the promise-only cut") names goes only through a Security Review, as today; the second agent's pass covers the rest. The Maintainer is not shown a list of tests or rules." Also add `dev/rules/protected-surfaces.md` to the doctrine surface, to say how the page and that rule relate.
2. **Blocking.** Part A moves the closeout, but `dev/tools/board.py` warns on ready-to-archive plans by reading the plan's closeout for items without a Home, and `docs/methodology/lifecycle.md` ("Archive precondition") ties archiving to it. Add to the doctrine surface: "`dev/tools/board.py` and `docs/methodology/lifecycle.md` change so that Home and Dispositions lines and the Benefit versus cost line are read from the proposal; no closeout item loses its Home requirement." Add `dev/tools/board.py` and `lifecycle.md` to the "Edited in plans" list.
3. **Blocking.** Part B removes archived plans but the proposal gives no check that nothing breaks. About 122 files outside the archive name the plans archive, and ten manifest lines name the generators. Add under Tests required: "After B, `link_check` and the board pass over the whole tree, and the two generators run or are changed to skip removed files, before the plan is archived."
4. Non-blocking. Count: the archive holds 208 plan files plus 8 folders (236 tracked files), not 210; the manifest names the generators by installed paths under `scripts/`, not `tests/`. State the count as measured at the plan.
5. Non-blocking. Check 4 (seeded faults) has no set, size or cost; the plan must specify them. Page draft is four categories of prose; an agent can place a test only where a release document names it. Ask the plan to list the document that names each.
6. Non-blocking. First pass has numbers but no pass or fail line before starting (for example, restores above N). Length: cut Context and the Alternatives bullet on word limits first.
7. Non-blocking. Decision summary: "promise", "tier", "seeded faults" and "guard" need a one-line gloss; choice 3 is clear.

**Checked myself**: archive count; gate manifest names both generators; always-loaded words (`AGENTS.md` 1,051 plus `RULES.md` 230, third file not counted); closeout text in `dev/plans/_template.md`; board reading of closeout; archive citations (file count, not the note's 295 citations).

**Not covered**: tier choice was read only against the protected-surfaces rule and found right; the note's outside studies; the Maintainer's chat quotes; the second proposal's overlap with code layout; no test run.
