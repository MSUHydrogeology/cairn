# Take the pressure to test out of Cairn's texts

**Author**: Claude Fable 5.2 (Strategy)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/working-agreements.md, dev/rules/protected-surfaces.md
**In brief**: Cairn's rules, templates and shipped copies stop asking agents for tests, runs and controls at every step, so that a change is checked by the fewest tests that show it is right.

## Decision summary

**What you noticed.** One small fix took 5.4 machine-hours of tests. You wrote on 2026-11-21: "Excessive testing is driving me insane. It has been for months now." You set the rule: "Just do all of the changes we need. Then run the fewest tests possible to make sure it was right. Then we re-anchor, certify on all three platforms, and cut." And then: "And, right now, strip the test pressure out of basically everything."

**Why a new rule alone will not hold.** A reader listed every sentence in Cairn's texts that asks an agent for a test, a run, a control, or a list of what it did not run. There are 675, in 57 files. Your rule on tests is one sentence. Every new agent reads the 675 and rebuilds the same caution.

**The change.** One short rule on tests replaces them. Each of the 675 is then rewritten to agree with it, or removed. The same edit goes into every copy that ships to projects.

**What does not change.** When the whole suite runs for certification. Who reviews what, the Security Review included. Every sentence of the security modules and of the rule on protected surfaces. Checks of a model result against the world. Sentences that tell an agent to run a check tool, such as the claim check or the security verification. Sentences that keep people honest: a claim of tested, checked or covered is made only when it is true, a failing check is not weakened to make it pass, and what was not checked is said plainly.

**Left for your word.** The module on how a project tests its own science code, in both copies (46 sentences each). Your words were about Cairn's own work, and a reviewer asked that you decide whether that page changes too. It is not edited in this pass.

**What it costs.** A defect that a wider run would have caught is now found at certification, which is later. Fewer tests get written, so a later change can break something no test watches. The texts change in 57 files at once.

**Not in this proposal.** The test runner's own limit of 40 files is in a protected file. Lowering it is the next proposal.

**One thing still gets a run.** A new security check is shown once to refuse one bad input planted for the purpose. A check that silently lets everything through looks exactly like one that works, so words alone cannot show it.

## Context

Measured on 2026-11-21 by a reader agent, with exact lines: 675 entries in 57 of 118 files. By kind: 149 ask for a run, 117 for a new test, 93 have a reviewer ask for tests or records, 75 treat a run as the only evidence, 62 ask for a list of what was not run, 55 ask for a control, 36 pick tests by the files a change touches, 11 ask for runs before and after or on two hosts, and 77 are of other kinds. The heaviest files: the published page on plans (97), the published page on review (59), the collaboration file (53, and 57 in its shipped copy), the testing module (46 in each copy), the plan template (38 and 36) and the proposal template (33 and 22). `AGENTS.md` holds 9 in each copy. 411 of the 675 are one sentence present in two trees. Three test files compare copies of these texts and fail if a pair drifts apart.

## Proposal

**A. The rule on tests,** stated once in each file that needs it, in these words: "Run the fewest tests that show the change is right, once: the tests written for it, and at most five test files that can see it. Make no run before the change to compare with, no second host unless the code is specific to that host, and no wide run because a large file was touched. A direct check that proves the point replaces the tests. Something that would fail if the change were wrong must be read, run or checked once. The whole suite runs at certification, before a release is cut. More than this needs the Maintainer's word." Where another text differs, this rule governs. A run that a plan names for a security requirement still stands.

**B. What each kind of sentence becomes.**
1. *Asks for a run, picks tests by file, or asks for before and after or two hosts:* replaced by rule A where the file states its rule on tests; removed elsewhere.
2. *Asks for a new test:* a test is added only for a behaviour that no existing test covers, and then one. A fix needs none if an existing test would have caught the fault.
3. *A reviewer asks:* a review says what it read and what it checked directly. It does not ask for more runs, more tests, a control or a record of them. Where a changed behaviour has no test at all, it may name one. It names tests the change does not need. A blocking finding is closed by exact words or code; a failing test is given only when words cannot show the fault. The reviewer shows it failing; the implementer runs it once, unchanged, after the fix, and a changed test counts as a decline. This does not bind a Security Review, which may ask for one run or one planted case on the point it raises.
4. *A run as the only evidence:* evidence is what was read, reasoned or checked directly. A run is one kind and is not required.
5. *A control:* existing controls and the tests that hold them stay. A new security check, or a change to what one accepts, is shown once to refuse one planted bad input, with the command and result recorded; the planted case need not be kept as a test.
6. *A list of what was not run:* one line says what was not checked. Tests that were not run need no list and no home; they wait for certification.
7. *Other:* decided one by one. Every row's outcome, of every kind, is recorded in this proposal's appendix: kept under C, replaced by rule A, rewritten, or removed.

**C. Kept as they are, whatever their kind.** Section C wins over section B. Kept: the items under "What does not change" above; every sentence of the security modules (the files with `security` in their names under `dev/modules/` and `templates/modules/`) and of the protected-surfaces rule; a sentence that names a test as a guard; a sentence that says a claim of tested, checked or covered may be made only when it is true, or that an unsupported assertion does not clear a review; a sentence that keeps existing refusals, checks or negative controls, or says a failing check may not be weakened; a sentence that says a pass by finding nothing needs a known-positive case; and the review rules on declining a blocking finding and sending it to the Maintainer (`dev/agent_collaboration.md`, "Review rules", and its shipped twin), changed only as disposition 3 says.

**D. Where.** Every file the inventory names: `AGENTS.md`, `RULES.md`, the files under `dev/rules/`, the collaboration file, the plan and proposal templates, the modules other than the security modules and the testing module, the session skills, the published pages under `docs/methodology/`, and each shipped copy under `templates/`. Where two copies are identical today they stay identical. The testing module is left as it is in both trees until the Maintainer says whether it changes (Scope delta).

**E. How.** Agents make the edits by exact replacement, never rewrapping, working from the inventory's rows, and record for each row what it became. A fresh reviewer then reads the whole diff against section C before it merges, and a Security reviewer reads the changed review rules. Cairn's own lock is refreshed by the installer afterwards, alone in its commit. There is no plan.

## Rationale

The pressure is in the texts, so it has to be taken out of the texts. One sentence against 675 has lost each time it was tried.

## Alternatives considered

- **Add the rule and leave the rest.** That is what was done before; agents reverted.
- **Only lower the test runner's limit.** It caps runs but leaves the texts asking for tests, controls and records. It is the next step, not a substitute.
- **Leave it to the tightening.** The Maintainer asked for it now.

## Documentation / doctrine surface

The governing layer (`AGENTS.md`, `RULES.md`, `dev/rules/`), the deliberation layer's method files (the collaboration file, both templates, the modules), the published method (`docs/methodology/`), and the shipped templates. No code.

## Evidence / verification plan

It worked when the same reader search, run again, finds in the edited files only sentences on the kept list, and the three tests that compare copies pass.

### Tests required

None is added. The three test files that compare copies are run once; they show that each pair of copies still agrees, not that the words are right, which is the diff reader's job: `tests/contract/test_verification_boundaries.py`, `tests/contract/test_writing_rules_ship.py` and `tests/test_review_stance_in_shipped_files.py`.

### Examples / smoke checks

`python tests/check_cairn.py`, the claim check and the link check on each changed file.

#### Security preflight

- **S1.** This changes what the method asks of agents. After it, an author's own reasoning can stand as evidence, so the party judged supplies it; section C keeps the sentence that an unsupported assertion does not clear a review, and the reviewer still checks.
- **S2.** The three copy-comparison tests fail when a pair drifts. They do not judge the words; the diff reader does.
- **S3.** Agents edit the texts; the reader search and the three tests run after.
- **S4.** If an edit goes wrong it leaves a sentence still asking for a test, which is today's state, or removes one on the kept list, which the diff reader and the Security reader named in section E look for.
- **S5.** What still gets through: a change that needed a wider run and did not get one. Certification is the backstop, and it is later.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Certification finds several defects that one small test would have caught. A security check ships with no account of how it could fail. Agents ask the Maintainer for leave to run more tests on most plans, which would mean the rule is too tight.

## Scope delta

**Scope delta**: degraded

- The testing module, in both copies, is not edited in this pass. **disposition**: held for the Maintainer. The usual review found that his words were about Cairn's own work and that this page guides a project's tests of its own science code. It is asked of him on the roadmap; nothing is conceded.

## Assurance path

**Assurance path**: high-assurance

## Review -- Claude Sonnet 5.5 (Reviewer) -- 2026-11-21

```
Reviewed commit: 65115c65
```

**Tier**: usual
**Findings**: raised (3 blocking, 3 non-blocking)
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes in direction: the Maintainer's words ask for it and the 675 entries are real. The framing is too coarse: seven dispositions applied by kind, not by purpose, remove some sentences that guard honesty, not testing -- `dev/PLANNING.md` standing direction of 2026-11-21; inventory rows 103, 127, 193, 208, 283.
2. **Best alternative.** Same strip, but each disposition carries an exception list named by sentence purpose, so a medium agent has no row to guess on -- inventory section 2.
3. **What would show it wrong.** A later review finds a claim "passed" with nothing run, or an adopter's science tests dropped -- see findings 1 and 3.

**Does any rule weaken or disappear?** Yes, on purpose: reviewers stop asking for runs, controls and records (3, 5, 6); a run is no longer required evidence (4); a before run and a second host go (1). Beyond that, see finding 1.

The proposal's aim is sound and its counts check out against the inventory (675 rows; 411 with twins, 264 without; 57 files; the 40-file limit is `tests/conftest.py:114`).

**Finding 1 (blocking).** Rows kept by purpose, not by kind, that the dispositions would delete:
- Row 127 (testing-discipline line 71, "Do not weaken assertions... to make a failed check pass") is kind control; disposition 5 reads as removing it.
- Row 193 ("No defects found" only with the three answers evidenced and gaps named) and row 295 (the "Not covered" block): disposition 6 shrinks them.
- Row 208 ("Unknown dependencies are not claimed as covered") fights "need no list and no home".
- Row 103 (security-verification: a mode needs execution evidence) and row 283 ("forward behavior needs executable evidence") fall to disposition 4.
- Row 218 (a pass by finding nothing needs a positive control) is a scientific-check sentence with no clear home.

Add to C: "Sentences that say a claim of tested, checked or covered may be made only when it is true, that a failing check may not be weakened, that a security mode needing executed evidence keeps it, and that a pass by finding nothing needs a control."

**Finding 2 (blocking).** Rule A can be read as leave to run nothing: "a direct check that proves the point replaces the tests" has no floor. Add after it: "Something that would fail if the change were wrong must be read, run or checked once." "A handful" is vague; say "at most five test files". Say that rule A governs when the other texts differ, and that the plan's named runs for a security requirement still stand.

**Finding 3 (blocking, premise: for the Maintainer).** The shipped testing module is for adopters' own science code. Disposition 2 ("a fix needs none") and rule A reach their results. The Maintainer's words were about Cairn's own work. Choose: strip the shipped modules too, or strip only the process texts and leave the adopter testing module.

**Non-blocking.** (a) Row 2 (session-end smoke run) is "removed" with no rule A in that file; say that it is removed. (b) Disposition 7 "each recorded" needs one place; name it. (c) S2 relies on tests that compare copies; they check twins agree, not that the words are right.

**Not covered.** I read ten rows' sentences only; the other 665 not at all. I ran no test and read no `templates/modules/` file in full.

## Review -- Claude Opus 5.5 (Security Review) -- 2026-11-21

```
Reviewed commit: bbf6dcf9
```

**Tier**: Security Review
**Findings**: raised (3 blocking, 2 non-blocking)
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes: the texts, not one rule, carry the pressure, and stripping them is the Maintainer's direction. But the dispositions work by kind, and some sentences of each kind do security work -- `dev/PLANNING.md` line 106; `dev/agent_collaboration.md` lines 106-115, 283, 287.
2. **Best alternative.** The same strip with the security modules and the anti-persuasion sentences held whole -- `templates/modules/default-on/security-verification.md` lines 59-82.
3. **What would show it wrong.** A security check ships that has never refused anything, or a test loses protection because no shipped file names it as a guard any more -- `dev/rules/protected-surfaces.md` line 43.

The proposal's strongest form: Cairn's texts out-vote any one rule on tests, so the texts must change together. I agree with the usual review's findings 1 to 3 and non-blocking (c). Where we overlap, my words for C (block X below) govern, because they include the usual review's sentence.

**Finding S1 (blocking).** Section B does not say that C wins over B. A medium agent on row 594 (`content-security.md` line 37, the merge-time scan of a pull request, kind run-tests) reads disposition 1, "removed elsewhere". Rows 582 and 584 require "an executed run, never a design argument" for admitting a security check; disposition 4 says a run "is not required". Row 586 calls policy tests "required companion evidence"; disposition 2 weakens it. Rows 38, 43 and 47 keep a reviewer from being talked out of a finding. Words: block X.

**Finding S2 (blocking).** Disposition 5 is not enough. A written account of how a check could fail is a design argument; a check that fails open passes exactly like one that works. One planted bad input, run once, is the fewest test that shows it is right. Words: block Y.

**Finding S3 (blocking).** Disposition 3 forbids a Security Review the run that disposition 5 lets it ask for, and its last sentence drops line 283's guards: the test must be shown failing, and a changed test is a decline. A reviewer can still stop an unsafe change only through that decline path to the Maintainer. Words: block Z.

**Non-blocking.** (a) S1 of the preflight is not right: after disposition 4 the author's own reasoning is evidence, so the party judged supplies it; block X's "unsupported assertion" keeps the reviewer's check. (b) S4 names "the reviews of the diff", but a light proposal has no plan and no code review; say who reads the 57-file diff for kept sentences.

**Not covered.** I read the security rows of the inventory and six sources around them, not the other rows; I did not check whether a test is named as a guard only in a sentence that would be removed. I ran no test.

### Exact words

**X.** Replace C with: "**C. Kept as they are, whatever their kind.** Section C wins over section B. Kept: the items under "What does not change" above; every sentence of the security modules (the files with `security` in their names under `dev/modules/` and `templates/modules/`) and of the protected-surfaces rule; a sentence that names a test as a guard; a sentence that says a claim of tested, checked or covered may be made only when it is true, or that an unsupported assertion does not clear a review; a sentence that keeps existing refusals, checks or negative controls, or says a failing check may not be weakened; a sentence that says a pass by finding nothing needs a known-positive case; and the review rules on declining a blocking finding and sending it to the Maintainer (`dev/agent_collaboration.md` lines 283 and 287 and their twins), changed only as Z says."

**Y.** Replace disposition 5 with: "5. *A control:* existing controls and the tests that hold them stay. A new security check, or a change to what one accepts, is shown once to refuse one planted bad input, with the command and result recorded; the planted case need not be kept as a test."

**Z.** In disposition 3, replace the last sentence with: "A blocking finding is closed by exact words or code; a failing test is given only when words cannot show the fault. The reviewer shows it failing; the implementer runs it once, unchanged, after the fix, and a changed test counts as a decline. This does not bind a Security Review, which may ask for one run or one planted case on the point it raises."

## Response -- Claude Fable 5.2 (Strategy) -- 2026-11-21

Both reviews are folded once, in place. Status is now `awaiting-decision`.

Usual review:
1. Finding 1 (honesty and guard sentences would be deleted): taken, with the Security Review's block X, which holds the reviewer's sentence.
2. Finding 2 (rule A has no floor; "a handful" is vague): taken, in section A.
3. Finding 3 (the testing module, a premise for the Maintainer): the module is taken out of this pass and asked of him; see Scope delta.
4. Non-blocking (a), the session-end row: it is removed, and the appendix records it. (b), where "other" rows are recorded: the appendix, for every row. (c), what the copy tests show: taken, in Evidence and S2.

Security Review:
1. S1 (C must win over B): taken, block X replaces section C. Its question, keep the security modules whole or strip them row by row: whole.
2. S2 (a written account is not enough for a security check): taken, block Y replaces disposition 5.
3. S3 (disposition 3 dropped the decline guards): taken, block Z.
4. Non-blocking (a), preflight S1: reworded. (b), who reads the diff: section E names a diff reader and a Security reader.

### Withdrawn / superseded commitments

- Disposition 5 as first written, a written account in place of a run. Withdrawn: one planted bad input is run once.
- "A handful" of tests. Replaced by "at most five test files".
- Editing the testing module in this pass. Held for the Maintainer.

**Elapsed**: unknown. **Tokens**: unknown.

## Decision -- Maintainer (scribed by Claude Fable 5.2) -- 2026-11-21

**Tier**: light

**ACCEPTED.** The Maintainer's instruction came before this proposal was written, and it is what the proposal carries out. He wrote (chat, 2026-11-21):

> "And, right now, strip the test pressure out of basically everything."

Just before, he had set the rule it serves: "Just do all of the changes we need. Then run the fewest tests possible to make sure it was right. Then we re-anchor, certify on all three platforms, and cut."

What this records, plainly:

- **He has not read this text.** Strategy told him in chat the same day what it holds: 675 sentences in 57 files, one short rule in their place, and what stays. He gave no further word on it, and none is claimed here.
- **Scope.** The proposal as revised after its two reviews. The testing module is outside it, held for his answer.
- **Tier: light,** as proposed; it was not put to him as a separate question. No plan. A fresh reviewer and a Security reader read the diff before it merges.
- **If he redirects,** every edit is a commit on the development branch and can be taken back.

**Elapsed**: unknown. **Tokens**: unknown.

## Decision, the testing module -- Maintainer (scribed by Claude Fable 5.2) -- 2026-11-21

**The testing module stays as it is.** One page was held out of this proposal for his word: the module that tells a project how to test its own science code, in both copies. Strategy asked whether it should change too, and recommended that it should. He wrote (chat, 2026-11-21):

> "Don't change the testing a project's own science code"

What that settles:

- **Neither copy of the testing module is edited,** now or under this proposal. Its 46 sentences in each copy stay.
- **The Scope delta's one item is closed:** disposition accept, by his words above.
- The one row in another file that was left undecided because it leans on that module stays as it is too.

**Elapsed**: unknown. **Tokens**: unknown.

## Read of the whole diff -- Claude Sonnet 5.5 (Reviewer) -- 2026-11-21

```
Reviewed commit: 38f5ba2b
```

**Range read**: `git diff 328325bb..HEAD`, 31 files of prose plus the appendix; every removed line read.

**Verdict**: ACCEPT. No blocking finding; two small wording mismatches, below.

**What I checked, by the brief's nine points**

1. **Kept list.** Every honesty sentence, the review rules on declining a blocking finding and sending it to the Maintainer, "unsupported assertion", known-positive controls, the claim check and Security Review sentences are still there. The only removed honesty lines ("a missing smoke is unavailable, not passed") belonged to the goodnight smoke run, which the proposal removes.
2. **Untouched files.** `git diff --stat` names no `security` file, no `protected-surfaces.md`, no `certifying-runs.md`, no `testing-discipline.md`.
3. **Pressure left.** I searched the 31 files for: Bounding, WIDER RUN, joined integration, tier_inventory, Not run, smoke, before and after, second host, failing test, widen, mutation, positive/negative control, rerun. What remains is on the kept list or is a permitted case.
4. **Agreement.** The rule is in full once in each collaboration copy and in `plans.md`, word for word; `AGENTS.md` has the short form. The section headings the pointers name all exist.
5. **Reads.** No half sentence, empty list item or rewrapped paragraph found. Slot and `{{` counts are unchanged in every file; `git diff --check` is clean.
6. **Copies.** All pairs identical before are identical now; the changed lines of the collaboration file and both templates match between trees.
7. **Words.** 1577 of 2000 and 1478 of 1500.
8. **Tests.** The three files: 49 passed, 0 failed.
9. **Beyond the proposal.** Nothing weakens beyond sections A to C.

**Non-blocking findings**

- **N1.** The two files that define a defect repair still say "failing-test reproduction", while both session-start copies now say "a test or a direct check".
- **N2.** `plans.md` and `dual-review.md` still say a new security check "needs a demonstrated failing case"; the collaboration file says one planted bad input, run once. They agree in effect.

**Not covered.** I did not read the appendix row by row, or the pressure that the diff left alone in the 26 files it never touched. I did not search the whole repository for sentences in files outside the diff. Elapsed and tokens: unknown.

### Exact fixes (optional)

- `docs/methodology/lifecycle.md`: "(i) a failing-test reproduction," becomes "(i) a reproduction by a test or a direct check,".
- `docs/methodology/plans.md`: "(a failing-test" becomes "(a test or direct-check".

## Security read of the changed review rules -- Claude Opus 5.5 (Security Review) -- 2026-11-21

```
Reviewed commit: f3bf60c8
```

**Range read**: `git diff 328325bb..f3bf60c8`, every removed and added line of `AGENTS.md`, `RULES.md`, `dev/agent_collaboration.md`, both templates, both session skills, their shipped twins, and `docs/methodology/` `dual-review.md`, `plans.md`, `lifecycle.md`, `proposals.md`.

**Verdict**: REVISE. Two blocking findings, each a few words; three non-blocking.

**The six points**

1. **Guards kept.** Still present: an ordinary pass never clears a Security Review; a declined blocking finding goes to the Maintainer; a changed test is a decline; an unsupported assertion does not clear a review; existing refusals and checks may not be weakened; `AGENTS.md` keeps the known-positive rule.
2. **New security check.** Present in both collaboration copies. `plans.md` and `dual-review.md` say "a demonstrated failing case": weaker, because it omits a change to what a check accepts and the recorded command. Use the collaboration words (N2 below).
3. **Rule A.** Blocking S-A. "Where another text differs, this rule governs" lets rule A override the kept security modules, a Security Review's one run, and the planted input. Only a plan-named run is saved.
4. **Defect-repair carve-out.** Blocking S-B. "A test or a direct check" as condition (i) is acceptable. But the edits also dropped condition (iii), the surface's own tests running. On a named high-risk surface this carve-out has no proposal and no review, so that run was its only remaining check. Restore it, bounded by rule A.
5. **Evidence from the party judged.** Both plan templates still say forward behavior needs only "what was read, reasoned or checked directly". The collaboration file asks for something that would fail. The plan template's "Preserve required security checks" line limits the gap. Non-blocking N3.
6. **Untouched files.** Confirmed: the stat names no `security` file, no `protected-surfaces.md`, no `certifying-runs.md`, no `testing-discipline.md`.

**Non-blocking N4.** Removed from the collaboration file and `plans.md`: "Search for readers and byte pins". A broken pin on a high-risk surface now fails at certification, not earlier. It fails closed, so I let it stand.

**Not covered.** I did not read the appendix row by row or the 15 other changed files. I did not check that the tier rules on when a Security Review is required are unchanged outside these files. I ran no test. Elapsed and tokens: unknown.

### Exact fixes

**S-A (blocking).** In `dev/agent_collaboration.md`, its twin `templates/core/dev/agent_collaboration.md`, and `docs/methodology/plans.md`, "A run that a plan names for a security requirement still stands." becomes "It does not override the security modules, the protected-surfaces rule, a run that a plan names for a security requirement, a Security Review's one run or planted case, or the planted bad input for a new security check."

**S-B (blocking).**
- Both session-start copies: "only when it meets both" becomes "only when it meets all three"; "or intended behavior with no contract change. A change" becomes "or intended behavior with no contract change; (iii) the surface's own tests, at most five files, run once after the fix and pass. A change".
- `lifecycle.md`: "a **defect repair** — both of" becomes "a **defect repair** — all three of"; "(i) a failing-test reproduction," becomes "(i) a reproduction by a test or a direct check,"; "intended behavior with no contract change — takes the trivial" becomes "intended behavior with no contract change, (iii) the touched surface's own tests, at most five files, run once after the fix and pass — takes the trivial".
- `plans.md`: "two conditions in `docs/methodology/lifecycle.md` (a failing-test" becomes "three conditions in `docs/methodology/lifecycle.md` (a test or direct-check"; "change). That repair" becomes "change; the touched surface's own tests run once and pass). That repair".
- `proposals.md` lines 178 and 335: "the lifecycle's two conditions" becomes "the lifecycle's three conditions".

**N2.** `plans.md`: "a new security check needs a" / "demonstrated failing case." becomes "a new security check, or a change to what one accepts, is shown once to refuse one planted bad input, with the command and result recorded." `dual-review.md`: "demonstrate a failing case for a new security" / "check." becomes "show once that a new security check, or a change to what one accepts, refuses one planted bad input, with the command and result recorded."

**N3.** Both plan templates: "Forward behavior needs evidence before completion: what was" / "read, reasoned or checked directly; a run is one kind and is not required." becomes "Forward behavior needs a direct check before completion: something that would fail if it were wrong was read, run or checked; a run is one kind and is not required."

## Response to the two reads -- Claude Fable 5.2 (Strategy) -- 2026-11-21

The Security read's two blocking findings are closed in its exact words, and its two other fixes are taken as written.

Read of the whole diff:
1. N1 (the defect repair's first condition): taken in the Security read's wording, "a reproduction by a test or a direct check", together with the third condition (S-B below).
2. N2 (a new security check in the published pages): taken in the Security read's wording.

Security read:
1. S-A (the rule on tests could be read as overriding the security texts): taken, in both copies of the collaboration file and in `docs/methodology/plans.md`.
2. S-B (the defect repair that skips review had lost its third condition): taken, in both copies of the session-start skill, in `docs/methodology/lifecycle.md` and `docs/methodology/plans.md`, and at two places in `docs/methodology/proposals.md`. The edits had removed a guard that section C keeps. On a named surface this repair has no proposal and no review, and the surface's own tests were its one remaining check. They run once, at most five files.
3. N2 and N3: taken as written.
4. N4 (the search for readers and byte pins is gone): it stands, as the read says; a broken pin fails at certification.

Checked after the fixes: the three test files that compare copies, once, 49 passed; the claim check, the link check and `check_cairn` on each of the eleven changed files; `cmp` of the two copies of the session-start skill prints nothing; the always-loaded files hold 1,577 and 1,478 words against limits of 2,000 and 1,500. Not checked: the files that neither read covered.

**Elapsed**: unknown. **Tokens**: unknown.

## Implementation verification -- Claude Fable 5.2 (Strategy) -- 2026-11-21

The edits are merged into `0.9-dev` at `8067d2df`. Thirty-one text files changed, in Cairn's own tree and in the copies that ship.

**Who did what.** Five medium-tier agents made the edits by exact replacement, each on its own files, from the inventory's rows; the appendix records what each row became. Strategy made three edits for consistency and applied the Security read's fixes. A fresh reviewer read the whole diff against section C and accepted it. A Security reviewer read the changed review rules and found two faults, both closed in its exact words (the response above).

**Checked directly.**
- The three test files that compare copies, run once on the branch after it took in `0.9-dev`: 49 passed.
- `install/verify_integrity.py --target .` reports OK for 70 files on the merged tree. Seven installed files had changed, and Cairn's own lock was refreshed for them alone in `dace7d8d`.
- The claim check, the link check and `check_cairn` on each of the 33 text files the merge changed: no flag. `git diff --check` is clean.
- The always-loaded files hold 1,577 words against a limit of 2,000, and 1,478 against 1,500.
- The files that stay whole are untouched: no file with `security` in its name, nor `dev/rules/protected-surfaces.md`, `dev/rules/certifying-runs.md`, nor either copy of the testing module (the merge's list of files).
- One conflict arose when the branch took in `0.9-dev`, in this file: both sides had appended to it. The sections are kept in the order they were written.

**Not checked.** The reader's search was not run again over all 57 files. The diff read searched the 31 edited files for the old trigger words and did not read the appendix row by row. Neither read covered the 26 files of the inventory that the change did not touch.

**Still owed, each with its home.** Lowering the test runner's own limit of 40 files, which is in a protected file: the next proposal, `dev/PLANNING.md`, "Small fixes are tested for hours". The testing module is settled by the Maintainer's second Decision above; nothing is owed on it.

**Elapsed**: unknown. **Tokens**: unknown.
