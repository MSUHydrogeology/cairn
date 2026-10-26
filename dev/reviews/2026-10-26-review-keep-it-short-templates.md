# Code review (Internal) — "keep it short" in the plan and proposal templates (`3ba6aba1`) — Claude Sonnet 5.5 — 2026-10-26

**Obligation**: code review of a prose change that has no proposal or plan. It adds
a "Keep the plan short" and a "Keep the proposal short" section to the four
template files, plus a CHANGELOG entry, from the adopter's draft in issue #31. A
fresh session; the author was a different agent (Haiku). Internal pass, not External.
**Reviewed commit**: `3ba6aba1`, read as `git diff 0.5-dev...0.5-dev-keep-it-short`
(five files, +62 lines): `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`,
`dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`, `CHANGELOG.md`.
**Interpreter**: Python 3.13.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`).
Every run was in the detached worktree `/private/tmp/cairn-review-31` of `3ba6aba1`;
the mutants ran in a second detached copy that is now removed. I did not set
`CAIRN_FULL_SUITE=1` and ran no full suite.

**Verdict**: NO BLOCKING FINDINGS — 0 blocking, 5 non-blocking, 1 informational.

**In plain terms.** The change does what it says. The four sections are in the right
place, each pair is word-for-word the same, and the tests that read these files pass.
The wording has small faults the author can fix in a few minutes: two coined terms
an adopter cannot look up, one sentence that reads as stricter than the review rule,
and one dropped instruction.

## Foundations

1. **Does it really do what it claims?** Yes. The issue's draft asks for four rules,
   and the result carries all four, in 12 to 15 lines per copy. Placement and pair
   agreement are measured, and the ten test files that read these paths pass (800
   tests) — `git diff 0.5-dev...0.5-dev-keep-it-short`; the pair check in Q2; `pytest` in Q4.
2. **Best alternative.** None simpler. A prose edit with no tool and no test change
   is the smallest build. The draft taken verbatim would add about 8 lines per copy
   and restore the reasons; the condensed text is the better trade except for the
   clauses in KS-2 and KS-3 — `dev/plans/_template.md:126-140` against the issue's draft.
3. **What would show it wrong.** A heading-reading test failing, a pair that differs,
   or a shipped term an adopter cannot resolve. One of these was found (KS-1) — see
   the falsification ledger below.

## Q1 — Rule by rule against the draft

| Draft rule | Result | Verdict |
|---|---|---|
| Plan is one file; reviews, responses, records append "as the rules above say"; stay small "because every reviewer, archiver and agent reads it" | "The plan stays one file. Keep what goes in it small." | Reason dropped (fine). The append clause is gone; see KS-2. |
| Checker under `tests/` or `scripts/`, "where it is versioned and tested" | Kept, reason dropped | Fine, except KS-5 (the folder name). |
| Run brief is a short note or file, cited by path and commit; plan carries criterion and result, not code | Kept | Kept, but "run brief" is undefined (KS-1). |
| Log entry is a pointer; commit bodies carry "the facts and the counts"; adds only a decision, finding or departure | Kept (plan only; the proposal copy drops it, as the issue says) | Kept; "and the counts" dropped, no loss. |
| Pause note points at the handoff file | Dropped | Does not matter; see below. |
| Cite evidence by path | Heading kept | Kept. |
| "A review names the file, test, line or command behind a claim" | Dropped | Does not matter; see below. |
| Probe ledger is one line per probe, no output pasted | Kept | Kept, but "probe ledger" is a new name (KS-1). |
| Read by section: list headings with `grep -n '^## '` **and read only the sections the job needs** | Second half dropped | Matters a little; KS-3. |
| Headings: one pass, log or record per `##`, titled by what it holds and when written | Kept | Kept. It matches how plans are already headed (`dev/plans/archive/scope-reduction-trap.md`, `grep -n '^## '`: "Code review -- Claude (Internal) -- 2026-08-11"). |

**The pause-note sentence.** Losing it costs nothing. "Pause note" is not a record
type Cairn defines: `grep -rIl -i "pause note"` over the tree, archives excluded,
returns nothing, and the same search for "Keep the plan short" (the control) returns
the three files that hold it, so the search could have matched. It is the adopter's
own record, and the duplication it guards against is covered by "A log entry is a pointer".

**The first evidence sentence.** Losing it costs nothing. The rule is shipped twice
more: `templates/core/AGENTS.md:85` and the Foundations lines of both plan
templates (`templates/core/dev/plans/_template.md:79`, `:402`). The bullet now says
what to leave out (pasted output) and its heading says "by path", which is enough.

**The author's count.** "Two sentences" understates it: four clauses went as well
(the section's reason, the scripts reason, "and the counts", and "read only the
sections the job needs"). Three are reasons and cost nothing. The fourth is KS-3.

## Q2 — The two copies of each pair agree

Measured, not read. A script cut the section out of each file and compared the text:
the two plan sections are identical (15 lines) and the two proposal sections are
identical (12 lines). I also compared the added lines of each file's diff:
`cmp` returns equal for both pairs. The files differ elsewhere on purpose (adopter
slots), so the check is on the new section only.

## Q3 — Placement

Section line, next section line, and the rule (`---`) line, from
`grep -n -E '^## (Keep the|Forward-reference)|^---$'`:

| File | Keep section | Forward-reference paths | Rule |
|---|---|---|---|
| `dev/plans/_template.md` | 126 | 142 | 155 |
| `templates/core/dev/plans/_template.md` | 128 | 144 | 157 |
| `dev/proposals/_template.md` | 122 | 135 | 148 |
| `templates/core/dev/proposals/_template.md` | 104 | 117 | 130 |

All four sit before "Forward-reference paths" and above the rule. The file's own
header says authors copy only what is below the rule, so an author reads the section
and the text is not copied into each new plan.

## Q4 — Tests and gates

**What reads these four paths.** My search: `grep -rlE "plans/_template|proposals/_template"`
and `grep -rlE "_template(\.md)?['\"]" bootstrap/tests`, then a read of each hit.
Ten test files read the repository's four files by name: `test_certifying_run_rule`,
`test_board_json_contract`, `test_claim_check_module`, `test_documentation_plan_module`,
`test_scaffold`, `test_review_stance_in_shipped_files`, `test_scientific_check_guidance_ships`,
`test_scope_reduction_trap`, `test_verification_boundaries`, `test_quickstart_sequence`.
Two more name the paths but write their own copy in a temp folder (`test_replacement_tools`,
`test_trigger_evaluation_action`). I did not see the author's list. My ten-file set
reproduces their count: **800 passed** (control, unmutated).

Beyond those: the two temp-copy files (838 together), and a second ring of 21 files
that walk the templates tree or the installer (neutrality, doc governance, comprehension
floor, content scan, install, upgrade, lockfile and others): **833 passed**.
Scoped runs only; the per-file `pytest` calls name no directory.

**The heading-reading assertions.** `test_board_json_contract.py:2182` and `:2236` split
each template at `\n---\n` and at the first `\n## ` below it, and need `**In brief**:`
in that header block. The new section is above the rule and holds no `---` line, so it
cannot disturb them. The mutant below shows the assertion is live.

**Gates.** `python scripts/quality_gate.py --sub neutrality --sub redundancy`: fail=0 on
both. `python scripts/claim_check.py` on each of the four templates (one file per call;
it takes one): "OK, no claim-check flags" four times. That OK is weak evidence here: it
checks repo paths, and the new text names `tests/`, `scripts/` and a `grep` command in plain
prose, which it does not test. By hand: `scripts/` exists in an adopter's tree
(`bootstrap/_scaffold/config.py:751-752` installs `scripts/claim_check.py`);
`tests/` does not exist in Cairn's own tree (`ls tests`: no such file), see KS-5.
`python scripts/check_cairn.py`: one issue, a cached-bytecode folder cited in
`dev/reviews/2026-10-18-security-review-session-writes.md:131`, a file this change
does not touch.

**The command the text gives.** `grep -n '^## ' dev/plans/archive/scope-reduction-trap.md`
lists 18 headings with line numbers. Across the 61 archived plans, 2 `^## ` lines sit
inside a fenced code block, so the list is nearly exact. The scale the section answers is
real in this tree: the archived plans run up to 5,026 lines.

**The lockfile.** `dev/.cairn/cairn-lock.yml:204-216` pins hashes for the two installed
templates. They match neither this commit nor `0.5-dev` (lock `86275df0`/`20128471`;
`0.5-dev` `de8a36bc`/`e7ce5dbd`), so the lock was already out of date before this
change and this change adds no new drift. I did not check how `upgrade` treats it.

## Falsification ledger

Each mutant is one deliberate break, run in a separate detached copy of `3ba6aba1`
against the same ten test files, beside an unmutated control.

| Run | Break | Result |
|---|---|---|
| Control | none | 800 passed |
| M1 | the plan section moved below the rule in `dev/plans/_template.md` | **killed**: 1 failed, `test_board_json_contract.py::TestTemplatesAskForTheLineTheBoardReads::test_plan_templates_carry_in_brief_below_the_rule_and_keep_waiting_above_it` |
| M2 | the plan section deleted from `templates/core/dev/plans/_template.md` only | **survived**: 800 passed |
| M3 | the proposal section deleted from `templates/core/dev/proposals/_template.md` only | **survived**: 800 passed |

M2 and M3 are KS-6.

## Findings

### [KS-1] low, non-blocking — two names in the shipped text have no definition, and one duplicates an existing name

"Run brief" and "probe ledger" appear nowhere in Cairn except the new text and the
CHANGELOG (`grep -rIl`, archives and reviews excluded; the control for
"falsification ledger" returned 13 files, so the search works). An adopter who has
none of Cairn's files cannot look either up. Cairn Plain Language rule 5 (define a
specialist term where it first matters) and rule 4 ("do not coin a name for something
that already has one"). The plan template already has the second one: the
**falsification ledger**, in `templates/core/dev/plans/_template.md:432` and
`templates/core/AGENTS.md`. That term is missing from the proposal templates.

**Recommended fix.** In the run-brief bullet, say what it is in one clause: "A run brief
(the instructions you hand an agent that runs a test or job) is a short note or file…".
In the plan copies write "A falsification ledger has one line per attempt, with no output
pasted." In the proposal copies write "A review's list of what it tried has one line per
attempt…". Mirror the same two words in the CHANGELOG entry.

### [KS-2] low, non-blocking — "The plan stays one file" reads stricter than the review rule

The draft said "…reviews, responses and records are appended to it, as the rules
above say." The result keeps only "The plan stays one file." `templates/core/AGENTS.md:134`
lets a review be appended or "created as its own review file", and Cairn's own code reviews
are files under `dev/reviews/`. Read alone, the new sentence can be taken to forbid that.
The issue records "keep it as one file" as the adopter's Maintainer's ruling, not Cairn's.

**Recommended fix.** Restore the clause that ties it to the append rule: "Reviews,
responses and records are appended to the plan. Keep what goes in it small." The
Maintainer decides whether Cairn means to say "one file" without that qualifier.

### [KS-3] low, non-blocking — the instruction to read only what the job needs was dropped

The draft ends the reading rule with "and read only the sections the job needs". The
result tells readers how to list headings but never says to stop there. The title
"Read by section" carries it by implication. The issue's own cost evidence is that
readers read the whole file.

**Recommended fix.** Add one clause to the last bullet in all four copies: "Readers
list them with `grep -n '^## ' <plan>` and read only the sections the job needs."

### [KS-4] low, non-blocking — the CHANGELOG entry's shape and wording

Under `## Unreleased`, with a category heading in the file's pattern, so the placement is
right. Three small faults against the file's own entry shape and Plain Language:
(a) "Long files are read by their `##` headings" is passive and does not say who does what
(rule 7); (b) it names "run briefs" and "probe output" with no definition (KS-1);
(c) the one link goes to an issue that stays open, where the shape asks for a durable
target (a commit, plan, proposal or doctrine file), and the entry is one 222-character
line where its neighbours wrap at 80.

**Recommended fix.** "The plan and proposal templates now say what to keep out of the
file (checker scripts, run briefs and pasted test output) and how to read a long file one
`##` section at a time." Wrap it, and link the template section as well as the issue.

### [KS-5] nit — `tests/` is not a folder in Cairn's own tree

Cairn's tests live in `bootstrap/tests/`; there is no `tests/` (`ls tests`). For an adopter
`tests/` is a common convention and `scripts/` exists, so the shipped copy reads well. The
self-hosted copy points to a folder that does not exist, and `claim_check` cannot see it.

**Recommended fix.** "A checker lives in your test folder or `scripts/`" in both copies of
each file, or leave it; the author decides.

### [KS-6] informational — nothing pins the section's presence or the pair's agreement

M2 and M3 survived. Only the placement is guarded (M1). The pair is identical now by
measurement (Q2), kept so by hand. No document claims a check, so no claim is wrong. Other
parts of these templates have pair-parity tests because they are contracts; this is
guidance. I recommend leaving it unpinned. If the Maintainer wants it pinned, one
assertion that both plan copies and both proposal copies hold the same section is enough.

## Plain Language and length

The section is short itself: 15 lines in the plan copies, 12 in the proposal copies, the
bullets run to about 12 lines, and the conclusion is first ("Keep what goes in it small").
Sentences are short and each bullet has one topic; the `grep` command gives the example for
"read by section" (rule 6). "Small" has no number, but the issue deliberately proposes no
size cap, and each bullet below it is concrete. The faults are those in KS-1 to KS-4.

## Bounding

**Bounding**: ACCEPTED — The author's record is scoped (ten files, 800 tests, the gates).
I challenged two things. The named surface, placement, by M1: the board test killed it, so
the heading-reading assertions are live. The stated omission, that nothing checks the pair,
by M2 and M3: both survived, which supports the author's scoped claim and gives KS-6 rather
than a failure. The unmutated control reproduced the author's 800. A prose change that no
manifest pins does not trigger a full run.

## What I did not cover

- The author's own list of ten files and their exact commands; I rebuilt the set and matched
  the count, not the names.
- Whether `grep` is available to an adopter on Windows; I ran it on macOS only.
- How `upgrade` merges the changed templates into an existing install, and the stale lock
  hashes; I did not run an install or an upgrade.
- Whether the 3,000 to 4,900 line figures in issue #31 are true of the adopter's repo;
  I took them as the issue's, and checked only Cairn's own archive (up to 5,026 lines).
- Any test outside the 33 files I ran, and the full suite (not mine to run; the next
  certifying run covers it, `**Certified by**: pending`).
- Whether Cairn means "one file" as strictly as KS-2 reads; that is the Maintainer's.

**Disposition**: accept. No finding blocks. KS-1 to KS-3 are wording edits of a few words
each in the same four files; KS-4 is one CHANGELOG line.
