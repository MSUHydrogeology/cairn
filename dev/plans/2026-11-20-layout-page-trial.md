# Plan: trial of the code layout page on modflow_tools

**Source proposal**: `dev/proposals/archive/2026-11-20-claude-code-layout-page.md`
**Status**: implementing
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

**Who runs it.** A session that can read `F:\Users\kendal30\Code\modflow_tools` and write its scratch folder. After C1 the plan is `implementing`; C2 waits for his hour as an approved observation, which stays implementation across days. No Waiting line is written, since nothing is asked of him but that hour. The roadmap's trial subsection names the wait: owner the Maintainer, restart when he starts the correction. The Maintainer already has agents work on that code: the project has Cairn 0.8.0 installed, and an agent of this harness read it on 2026-11-20 for the testing assessment. The trial's agents run under the same vendor, so the code goes nowhere new.

**Data boundary.** Strategy measured on 2026-11-20 that the project's remote is a university GitLab, not known public; Cairn's is public. Nothing from the project enters Cairn: no code, name, page text or task text. The project is only read, plus one new folder, named layout-trial, in its Git-ignored scratch folder (the trial folder). It gets no commit, branch switch, lifecycle step or installer command, and no agent works in it. The session exports its committed files with `git archive` (read-only), deletes the hand-kept architecture account from the copy, and makes a one-commit repository under the machine's temp area, outside both repositories. A copy, not a clone, keeps the account's history out of agents' reach.

**Files.** Trial files stay in the trial folder, readable by the Maintainer, this plan's agents and the code reviewer (who copies nothing). After code review he decides whether to delete them; adopting the corrected page there is that project's decision. The session deletes the throwaway repositories at the end of C3, or at the closeout if C3 does not run. The commit that was copied is recorded in the trial folder only.

**Counts.** An entry is one line of a list, named by its first term. A script, not an agent, counts added (name only in `corrected.md`), removed (name only in `draft.md`) and changed (same name, text differs after whitespace is normalised); it is scratch, kept in the trial folder. The agent adds one number: how many changed entries alter what is said, not only how. The clock starts when `draft.md` is handed to him and stops when he says it is corrected; time he says he spent away is subtracted and both totals are recorded. His questions, asked after the stop and answered yes or no: "While correcting, did you open code or run anything?" and "Is there a kind of thing it should speak of that it does not?" A yes to the first, or his stopping unfinished, fires the rule; so does a corrected total over 60 minutes. A copy is a new function whose job a call to a listed central tool could do; the counter gives one reason per copy in the trial folder. Both counts zero is reported as no difference seen, not as a pass. A run that cannot do the task as instructed is marked incomplete and counted as written.

**Steps.**
1. *Draft.* A high-tier agent (model named at the spawn) reads only the throwaway copy and writes `draft.md`: three lists and nothing else. Folders: what belongs in each. State: each class, what it stores, what may change it. Central tools: each one's promise (one sentence), home and tests. At most 20 entries in each of the last two lists; it also writes `left-out.md`, naming each entry the limits cut. A separate medium agent, which reads the copy and never `draft.md`, writes `tasks.md` (three small, realistic tasks, each partly done by an existing central tool) and `task-key.md` (that tool), seen only by the session.
2. *Check.* A medium agent compares `draft.md` with the project's hand-kept account and writes counts only, per list, to `account-counts.md`: entries the account names, how many the draft also names, how many it names that the account does not. The account may be out of date: evidence, not a verdict. He does not see it before step 3.
3. *Correction.* He edits a copy as `corrected.md`, or tells the session what is wrong. The clock, the entry counts and his two questions follow "Counts" below. He is handed no list of functions. If the rule fires, the proposal returns to him, and step 4 still runs on the page as he left it. A task whose tool is not on the corrected page is dropped, and the closeout says whether the page lacked it or the limits cut it. From the tasks kept he picks the one most like his real work. If every task is dropped, step 4 uses task 1 and the closeout says its tool was not on the page.
4. *Pair.* Two medium agents on one model get the same task and instruction in separate throwaway repositories: edit files only, run no tests or model, never commit, read nothing outside it. One also holds `corrected.md`, renamed as the proposal's page, and is told to read it first as data that may be wrong. Medium, as the page serves whoever decides where code goes. A third medium agent, which ran neither, gets the two patches under random labels with the page's file name removed (the session checks first), plus the list of tool promises, and never the page or the key. It counts, for each, into `pair-counts.md`: new functions doing a job a listed central tool already does (exact or reworded), calls to listed central tools, and all new functions. Asked at the end which patch had the page, its guess is recorded.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Ignore check, copy, steps 1 and 2 | none | Draft, tasks, counts |
| C2 | Step 3 | none: an observation by him, up to 60 minutes | Corrected page, answers |
| C3 | Step 4 | C2 done | Patches, counts |
| C4 | Closeout, roadmap lines, cost rows | C3 done | Closeout |

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

None. The closeout edits the roadmap's trial subsection and v0.10 layout row, and the cost record.

## Acceptance criteria

**C1.** `git check-ignore` names the trial folder. A file search of the copy finds no architecture account. `draft.md` is at most 900 words. `tasks.md` holds three tasks. Step 2 counts cover all three lists.

**C2.** Start and finish times give a minute count, with time away subtracted and both totals written. `corrected.md` exists. The script's added, removed and changed counts are written per list, with his two answers. The stop rule's outcome is stated with the minutes. The chosen task's number (1 to 3) is recorded; its text stays in the trial folder.

**C3.** Both agents ran the same model and task, differing only by the page. Both patches are saved. The counter's three counts per patch are written, labels revealed, with its guess of which had the page. The throwaway repositories are gone.

**C4.** The closeout holds: correction minutes; entries per list; entries changed, added, removed; his answers; step 2 and 4 counts; each agent step's model, tokens and minutes as the harness reported them (`unknown` if not); the stop rule result. Rule not fired: the v0.10 row stands and the trial's next step reads done, with numbers. Fired: the v0.10 row says the check and guidance are not built, and a roadmap line waits on him. Each step joins the cost record; its "Work" cells read "Layout trial, step N". Cairn's records hold only counts, yes or no answers, minutes, model names, tokens and a task's number.

## Scope delta

**Scope delta**: preserved. The paired runs are accepted scope and the stop rule does not release them, so C3 runs on whatever page he produced even if the rule fires, and the closeout says so. C3 is skipped only on his quoted word in chat, which is then recorded here as degraded, disposition accept.

## Verification

No test is added or required. Checks: the prose gates on this plan (`claim_check.py`, `link_check.py`, `tests/check_cairn.py`), then the code-stage recount. That reviewer recounts entries changed, added and removed from the two page files and the copies from the two patches, and searches every Cairn file this plan changed, every commit message in the range and the cost rows for each entry name in `draft.md` and `corrected.md`, each name in `tasks.md` and each file name in the patches, expecting no hit; the search is first run with a planted name in each of those places and must find each. Not covered: whether the page is right (only he can say); the counter's call on a reworded copy, which a recount only repeats.

## Plan review -- Claude Sonnet 5.5 -- 2026-11-20

```
Reviewed commit: f7ae7539688e00410c64841bbef7d7a84c288f2c
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the plan is outcome F with its stop rule, and the data boundary is mostly right (`git check-ignore` confirms the scratch path is ignored in the other project); the gaps are in how the numbers are fixed -- findings 1 to 5, `_template.md` "Sequence", `dev/agent_collaboration.md` "Plans and records".
2. **Best alternative.** The same trial with tasks written by an agent that has not seen the page, and a script for the entry counts -- finding 4.
3. **What would show it wrong.** Forward test: both agents write no copy, or the task's tool was cut by the 20-entry limit; the plan would then report a pass or a failure for the wrong reason -- finding 4.

The plan tries to learn, cheaply and with one scientist's hour, whether a plain page can be corrected without reading code and whether it changes what agents write. That is sound.

**Findings**

1. **Blocking.** His hour is an approved observation, not a decision or permission, so C2 takes no fence, and the plan is `implementing` after C1, not waiting at `ready-to-implement`. Block 1.
2. **Blocking.** Leak search covers only `corrected.md` names in Cairn files the plan changed. It misses commit messages, cost rows, task text and patch file names, and C2 records "the chosen task". Block 2.
3. **Blocking.** "Skipped if the rule fires, as the accepted text provides": the accepted text says no such thing, so "preserved" is unsupported. Block 3.
4. **Blocking.** Counts decided on the day: changed entry, copy, clock start and stop, the wording of his first question (the plan's version asks what he could do, not what he did), both-zero and impossible tasks. Block 4.
5. **Blocking.** Fairness: the draft's author also writes the tasks and key, so tasks fit the page; the 20-entry cap can hide the task's tool; the counter may see the page file in a patch. Block 5.
6. Non-blocking. Throwaway copies are deleted only at C3's end, so they stay if C3 never runs; each count step names no output file; the project's commit used is unrecorded; the opening text is 1,296 words against 1,000. Say each.

**Not covered**: I read the other project's folder list and its ignore rule only; no test run; whether sending that code to the vendor suits the university's terms is assumed by the plan and not checked by me.

### Closing words (plan review of 2026-11-20)

1. Sequence, C2 gate cell: replace "MAINTAINER-ONLY: only he can judge his project's page" with "none: an observation by him, up to 60 minutes". Scope, "Who runs it": replace "The plan may wait at `ready-to-implement` for his hour." with "After C1 the plan is `implementing`; C2 waits for his hour as an approved observation, which stays implementation across days. No Waiting line is written, since nothing is asked of him but that hour. The roadmap's trial subsection names the wait: owner the Maintainer, restart when he starts the correction."
2. C2: replace "the chosen task is recorded" with "the chosen task's number (1 to 3) is recorded; its text stays in the trial folder". Verification: replace "searches Cairn's files this plan changed for each entry name in `corrected.md`, expecting no hit, after confirming the search finds a planted name" with "searches every Cairn file this plan changed, every commit message in the range and the cost rows for each entry name in `draft.md` and `corrected.md`, each name in `tasks.md` and each file name in the patches, expecting no hit; the search is first run with a planted name in each of those places and must find each. Cairn's records hold only counts, yes or no answers, minutes, model names, tokens and a task's number." Cost-row "Work" cells read "Layout trial, step N".
3. Scope delta: replace the text with "**Scope delta**: preserved. The paired runs are accepted scope and the stop rule does not release them, so C3 runs on whatever page he produced even if the rule fires, and the closeout says so. C3 is skipped only on his quoted word in chat, which is then recorded here as degraded, disposition accept." Step 3: delete "step 4 is skipped and". C3 gate: "C2 done".
4. Add to Scope: "Counts. An entry is one line of a list, named by its first term. A script, not an agent, counts added (name only in `corrected.md`), removed (name only in `draft.md`) and changed (same name, text differs after whitespace is normalised); the agent adds one number, how many changed entries alter what is said, not only how. The clock starts when `draft.md` is handed to him and stops when he says it is corrected; time he says he spent away is subtracted and both totals are recorded. His questions, asked after the stop and answered yes or no: 'While correcting, did you open code or run anything?' and 'Is there a kind of thing it should speak of that it does not?' A yes to the first, or his stopping unfinished, fires the rule. A copy is a new function whose job a call to a listed central tool could do; the counter gives one reason per copy in the trial folder. Both counts zero is reported as no difference seen, not as a pass. A run that cannot do the task as instructed is marked incomplete and counted as written."
5. Step 1: move the tasks and key to a medium agent that reads the copy and not `draft.md`; the draft agent also writes `left-out.md` naming each entry the limits cut. A task whose tool is not on the corrected page is dropped, and the closeout says whether the page lacked it or the limits cut it. The counter gets the two patches under random labels with the page's file name removed (the session checks first), plus the list of tool promises, and never the page or the key; asked at the end which patch had the page, its guess is recorded.
6. Throwaway copies: "deleted at the end of C3, or at the closeout if C3 does not run." Each count step: name its input files and its one output file in the trial folder. Record the copied commit in the trial folder only.

## Plan response -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-20

The review said revise, with five blocking findings and the words that close each. All are accepted and folded into the cells above. Nothing is declined.

- **1, his hour is an observation, not a fence: closed.** C2 carries no fence, the plan is `implementing` after C1, and the roadmap's trial subsection names the wait and its owner.
- **2, what could leak: closed.** Cairn records a task by its number only. The leak search covers the changed files, the commit messages and the cost rows, and is first shown to find a planted name in each. C4 lists what Cairn's records may hold.
- **3, the paired runs are accepted scope: closed.** Strategy's brief set the default that the runs were skipped when the stop rule fired; the accepted text does not say that. They now run either way, and only the Maintainer's quoted word skips them.
- **4, numbers decided on the day: closed.** A new paragraph, "Counts", fixes what an entry is, that a script counts the changes, when the clock runs, his two questions as asked, what a copy is, and how two zeros and an undoable task are reported.
- **5, fairness: closed.** A separate agent that never sees the draft writes the tasks; the draft agent lists what its limits cut; the counter gets patches with the page's name removed and its guess is recorded.
- **6: accepted.** Throwaway copies go at the closeout if C3 does not run; each count step names its output file; the copied commit is recorded in the trial folder only. The text stays over the 1,000-word target because five findings added conditions.

Two additions of mine, for gaps the closing words left. If every task is dropped because its tool is not on the corrected page, step 4 uses task 1 and the closeout says so; otherwise the accepted runs could not happen. And a corrected total over 60 minutes fires the rule, stated beside the other two ways it fires.

Not checked by anyone: whether a 900-word page with 20 entries a list can describe a project of this size; the trial itself will show it.

**Elapsed**: unknown. **Tokens**: unknown.
