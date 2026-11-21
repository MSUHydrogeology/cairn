# Take the pressure to test out of Cairn's texts

**Author**: Claude Fable 5.2 (Strategy)
**Status**: awaiting-review
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

**What does not change.** When the whole suite runs for certification. Who reviews what, the Security Review included. The rule that a protected test is cut only through a Security Review. Checks of a model result against the world. Sentences that tell an agent to run a check tool, such as the claim check or the security verification. The duty to say plainly what was not checked.

**What it costs.** A defect that a wider run would have caught is now found at certification, which is later. Fewer tests get written, so a later change can break something no test watches. The texts change in 57 files at once.

**Not in this proposal.** The test runner's own limit of 40 files is in a protected file. Lowering it is the next proposal.

## Context

Measured on 2026-11-21 by a reader agent, with exact lines: 675 entries in 57 of 118 files. By kind: 149 ask for a run, 117 for a new test, 93 have a reviewer ask for tests or records, 75 treat a run as the only evidence, 62 ask for a list of what was not run, 55 ask for a control, 36 pick tests by the files a change touches, 11 ask for runs before and after or on two hosts, and 77 are of other kinds. The heaviest files: the published page on plans (97), the published page on review (59), the collaboration file (53, and 57 in its shipped copy), the testing module (46 in each copy), the plan template (38 and 36) and the proposal template (33 and 22). `AGENTS.md` holds 9 in each copy. 411 of the 675 are one sentence present in two trees. Three test files compare copies of these texts and fail if a pair drifts apart.

## Proposal

**A. The rule on tests,** stated once in each file that needs it, in these words: "Run the fewest tests that show the change is right, once: the tests written for it, and at most a handful that can see it. Make no run before the change to compare with, no second host unless the code is specific to that host, and no wide run because a large file was touched. A direct check that proves the point replaces the tests. The whole suite runs at certification, before a release is cut. More than this needs the Maintainer's word."

**B. What each kind of sentence becomes.**
1. *Asks for a run, picks tests by file, or asks for before and after or two hosts:* replaced by rule A where the file states its rule on tests; removed elsewhere.
2. *Asks for a new test:* a test is added only for a behaviour that no existing test covers, and then one. A fix needs none if an existing test would have caught the fault.
3. *A reviewer asks:* a review says what it read and what it checked directly. It does not ask for more runs, more tests, a control or a record of them. Where a changed behaviour has no test at all, it may name one. It names tests the change does not need. A blocking finding is closed by exact words or code; a failing test is given only when words cannot show the fault, and it is run once after the fix and deleted.
4. *A run as the only evidence:* evidence is what was read, reasoned or checked directly. A run is one kind and is not required.
5. *A control:* a new security check says in writing how it could fail. A run that makes it fail is made only when a Security Review asks for it. Existing controls stay.
6. *A list of what was not run:* one line says what was not checked. Tests that were not run need no list and no home; they wait for certification.
7. *Other:* decided one by one, each recorded.

**C. Kept as they are:** the items under "What does not change" above.

**D. Where.** Every file the inventory names: `AGENTS.md`, `RULES.md`, the files under `dev/rules/`, the collaboration file, the plan and proposal templates, the testing module and the other modules, the session skills, the published pages under `docs/methodology/`, and each shipped copy under `templates/`. Where two copies are identical today they stay identical.

**E. How.** Agents make the edits by exact replacement, never rewrapping, working from the inventory's rows, and record for each row what it became. Cairn's own lock is refreshed by the installer afterwards, alone in its commit. There is no plan.

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

None is added. The three test files that compare copies are run once: `tests/contract/test_verification_boundaries.py`, `tests/contract/test_writing_rules_ship.py` and `tests/test_review_stance_in_shipped_files.py`.

### Examples / smoke checks

`python tests/check_cairn.py`, the claim check and the link check on each changed file.

#### Security preflight

- **S1.** This changes what the method asks of agents, not a check that decides anything. No input is supplied by a party being judged.
- **S2.** The checks it relies on are the three copy-comparison tests, which fail when a pair drifts.
- **S3.** Agents edit the texts; the reader search and the three tests run after.
- **S4.** If an edit goes wrong it leaves a sentence still asking for a test, which is today's state, or removes one on the kept list, which the reviews of the diff are asked to look for.
- **S5.** What still gets through: a change that needed a wider run and did not get one. Certification is the backstop, and it is later.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Certification finds several defects that one small test would have caught. A security check ships with no account of how it could fail. Agents ask the Maintainer for leave to run more tests on most plans, which would mean the rule is too tight.

## Scope delta

**Scope delta**: preserved

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
