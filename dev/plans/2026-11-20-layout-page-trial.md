# Plan: trial of the code layout page on modflow_tools

**Source proposal**: `dev/proposals/archive/2026-11-20-claude-code-layout-page.md`
**Status**: awaiting-plan-review
**Plan review**: required(Internal)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/working-agreements.md, dev/rules/conventions.md
**In brief**: An agent drafts a plain three-list page about one of the Maintainer's own projects, he corrects it, and one pair of agent runs shows whether the page cuts one-off copies, before Cairn builds anything.

## Build summary

This plan ships nothing. A top-tier agent drafts a page of at most 900 words for modflow_tools: what each code folder holds, which classes store state, and which central tools (shared functions that do a common job) the rest relies on. The Maintainer corrects it as a description of his project, without opening code. He is asked for up to one hour, when he chooses: he edits a file or says what is wrong, picks one of three small tasks, and answers two one-word questions. Two agents then do that task, one given his corrected page and one not, and a third counts the new copies of a central tool each wrote. Cairn keeps numbers only.

## Source proposal

Accepted 2026-11-20 at the heavy tier; this plan runs its outcome F, with choices 1(a) and 2(a) (a trial now, on modflow_tools). Stop rule: if he cannot correct the page without reading code, or it takes over an hour, the check and the restructuring guidance are not built and the proposal returns to him.

## Scope

Result: two answers. (1) Can he correct the page without reading code within 60 minutes? That is the stop rule. (2) Does the agent given the page write fewer new copies of a central tool? One pair of runs is an observation, not a measurement. It cannot show the page works for other projects or people, or rule out chance.

**Who runs it.** A session that can read `F:\Users\kendal30\Code\modflow_tools` and write its scratch folder. The plan may wait at `ready-to-implement` for his hour. The Maintainer already has agents work on that code: the project has Cairn 0.8.0 installed, and an agent of this harness read it on 2026-11-20 for the testing assessment. The trial's agents run under the same vendor, so the code goes nowhere new.

**Data boundary.** Strategy measured on 2026-11-20 that the project's remote is a university GitLab, not known public; Cairn's is public. Nothing from the project enters Cairn: no code, name, page text or task text. The project is only read, plus one new folder, named layout-trial, in its Git-ignored scratch folder (the trial folder). It gets no commit, branch switch, lifecycle step or installer command, and no agent works in it. The session exports its committed files with `git archive` (read-only), deletes the hand-kept architecture account from the copy, and makes a one-commit repository under the machine's temp area, outside both repositories. A copy, not a clone, keeps the account's history out of agents' reach.

**Files.** Trial files stay in the trial folder, readable by the Maintainer, this plan's agents and the code reviewer (who copies nothing). After code review he decides whether to delete them; adopting the corrected page there is that project's decision. The session deletes the throwaway repositories at the end of C3.

**Steps.**
1. *Draft.* A high-tier agent (model named at the spawn) reads only the throwaway copy and writes `draft.md`: three lists and nothing else. Folders: what belongs in each. State: each class, what it stores, what may change it. Central tools: each one's promise (one sentence), home and tests. At most 20 entries in each of the last two lists, with a count of what was left out. It also writes `tasks.md` (three small, realistic tasks, each partly done by an existing central tool) and `task-key.md` (that tool), seen only by the session.
2. *Check.* A medium agent compares `draft.md` with the project's hand-kept account and writes counts only, per list: entries the account names, how many the draft also names, how many it names that the account does not. The account may be out of date: evidence, not a verdict. He does not see it before step 3.
3. *Correction.* He edits a copy as `corrected.md`, or tells the session what is wrong. The session notes the clock at his start and finish; a medium agent counts entries changed, added, removed. He is asked: could you correct it without opening code? Did it leave out a kind of thing it should speak of? He is handed no list of functions. Over 60 minutes, or his saying he read code, fires the rule: step 4 is skipped and the proposal returns to him. Otherwise he picks the task most like his real work; a task whose tool the corrected page lacks is dropped.
4. *Pair.* Two medium agents on one model get the same task and instruction in separate throwaway repositories: edit files only, run no tests or model, never commit, read nothing outside it. One also holds `corrected.md`, renamed as the proposal's page, and is told to read it first as data that may be wrong. Medium, as the page serves whoever decides where code goes. A third medium agent, which ran neither, sees the two patches under random labels and counts, for each: new functions doing a job a listed central tool already does (exact or reworded), calls to listed central tools, and all new functions.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Ignore check, copy, steps 1 and 2 | none | Draft, tasks, counts |
| C2 | Step 3 | MAINTAINER-ONLY: only he can judge his project's page | Corrected page, answers |
| C3 | Step 4 (skipped if the rule fires) | C2 passed | Patches, counts |
| C4 | Closeout, roadmap lines, cost rows | C3 or C2's stop | Closeout |

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

None. The closeout edits the roadmap's trial subsection and v0.10 layout row, and the cost record.

## Acceptance criteria

**C1.** `git check-ignore` names the trial folder. A file search of the copy finds no architecture account. `draft.md` is at most 900 words. `tasks.md` holds three tasks. Step 2 counts cover all three lists.

**C2.** Start and finish times give a minute count. `corrected.md` exists. Changed, added and removed counts are written per list, with his two answers. The stop rule's outcome is stated with the minutes. If it did not fire, the chosen task is recorded.

**C3.** Both agents ran the same model and task, differing only by the page. Both patches are saved. The counter's three counts per patch are written, labels revealed. The throwaway repositories are gone.

**C4.** The closeout holds: correction minutes; entries per list; entries changed, added, removed; his answers; step 2 and 4 counts; each agent step's model, tokens and minutes as the harness reported them (`unknown` if not); the stop rule result. Rule not fired: the v0.10 row stands and the trial's next step reads done, with numbers. Fired: the v0.10 row says the check and guidance are not built, and a roadmap line waits on him. Each step joins the cost record.

## Scope delta

**Scope delta**: preserved. If the rule fires, C3 is not run, as the accepted text provides.

## Verification

No test is added or required. Checks: the prose gates on this plan (`claim_check.py`, `link_check.py`, `tests/check_cairn.py`), then the code-stage recount. That reviewer recounts entries changed, added and removed from the two page files and the copies from the two patches, and searches Cairn's files this plan changed for each entry name in `corrected.md`, expecting no hit, after confirming the search finds a planted name. Not covered: whether the page is right (only he can say); the counter's call on a reworded copy, which a recount only repeats.
