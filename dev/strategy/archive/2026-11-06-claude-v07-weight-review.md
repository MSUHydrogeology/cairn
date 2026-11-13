# v0.7 weight review: what to keep, shrink or stop

**Author**: Claude Opus 5.5 (Strategy)
**Model**: Claude Opus 5.5 (`claude-opus-5-5`)
**Date**: 2026-11-06
**Status**: archived
**Type**: product-strategy
**Surfaces this would feed**: one doctrine proposal (living plans, record targets, exact-replacement editing, review question, pin retirement); a meter rescoping Decision; a test-pruning proposal; `dev/PLANNING.md` v0.7 rows

## Summary

v0.7 has added a lot of weight in four days, and only part of it is earning
its keep. Recommended:

1. **Freeze new process rules** for the rest of v0.7.
2. **Make plans living documents** that are revised in place.
3. **Give appended records a target length.**
4. **Make the cost meter an opt-in module and rescope it.**
5. **Replace text-pin tests** with exact-replacement editing of doctrinal
   files, plus one review question.
6. **Prune tests that guard little.**
7. **Spend the remaining v0.7 effort on adopter-facing engineering.**

Disclosure: I wrote four of the v0.7 proposals assessed here (agent
continuation, leaner reviews, shared claims, PR-merge check). The
"budgets are targets" wording that let plans grow came from my
leaner-reviews proposal.

## The question

The Maintainer asked, on 2026-11-06:
- how much complexity v0.7 has added;
- whether it adds process machinery that will slow development;
- whether the changes seem worthwhile, as a judgment, not as a request for
  proof;
- why the cost-meter plan grew so large;
- why the tests grew while we were trying to shrink them;
- whether text-pin tests pay for themselves.

## Method

All figures were measured with `git` on `v0.6.0` → `0.7-dev` at `3bd9f8a7`
(2026-11-06), unless marked otherwise.
- Diff sizes, by `git diff --numstat`, grouped by folder.
- Commits classified as record-only when every file they touch is under
  `dev/`.
- Word counts, by `wc -w` on `git show <rev>:<path>`.
- Test functions, by counting `def test_` lines per file name, so folder
  moves don't count as growth.
- Per-file test times, as recorded on the v0.7 board from 2026-11-02 runs.
- The `AGENTS.md` diff and `_SKILLS_MAPPINGS` in
  `bootstrap/_scaffold/config.py`, read directly.
- Pin-test history, from `git log` on the ten pure text-pin files. A search
  of plans, proposals and reflections looked for a pin that caught a real
  loss.

Not done:
- I did not read every proposal or plan in full.
- I did not time the full suite.
- I did not check the new tools' behavior.

Failures during iteration are not recorded, so "no recorded catch" is
weaker than "never fired". What would show this note wrong: evidence that
the frozen rules or the retired pins were preventing real defects, or that
the meter's present design is what the cost question needs.

## Findings

**Volume.**
- 889 commits; 625 (70%) change only `dev/` records.
- 63,215 lines added, 24,925 of them under `dev/`.
- About 208,000 words added to plans and proposals.
- 27 new proposals and 20 plans.

**Decisions made in the Maintainer's absence.** On 2026-11-06 the
Maintainer authorized a Sol agent to decide reversible work in their stead.
Its "Decisions to review when you return" table in `dev/PLANNING.md` lists
eight accepted proposals. Reviewing those eight with this note's questions
is the natural first step.

**Always-loaded and template text.**

| File | Words, v0.6.0 → now |
|---|---|
| `AGENTS.md` | 3,058 → 3,806 (+24%) |
| Shipped `AGENTS.md` | +19% |
| Plan template | +15% |

The roughly ten new `AGENTS.md` rules are each defensible. Several add
points where the Maintainer's word is needed:
- deferring cheap follow-ups;
- extra Security Review passes;
- counting human operations in the Decision.

**New shipped code.** `meter.py` (5,861 lines) and `git_read.py` (1,808
lines) install **unconditionally** into every adopter project.

**The cost-meter plan**, `dev/plans/2026-11-04-metered-cost.md`, has 19,239
words across 48 commits:

| Part | Words |
|---|---|
| Acceptance criteria, 5 chunks (target 750) | 2,075 |
| 16 verification entries | 3,778 |
| Appended "Strategy" sections on 2026-11-06 | about 6,500 |

The appended sections designed the Windows backend, timing retention and
export checks during implementation. Records appended after review have no
length target, and the template's numbers are "targets, not trimming
triggers".

**Tests.**
- Net +352 test functions, with no file shrinking.
- The meter accounts for 158 of them (45%): `test_meter.py` 127,
  `test_gauge.py` 31.
- Suite consolidation shared setup to save time. Its accepted design forbade
  removing tests that catch faults, and its measured win was one family going
  from about 60 s to 9 s. The full suite has not been re-timed since
  24 min 55 s.

**Text pins.**
- Ten files hold about 190 test functions that assert shipped rule text.
- 48 commits touched them: pins added with new rules, pins edited because a
  rule was deliberately reworded, or pins moved.
- The only recorded catches are a reviewer's deliberate mutation experiment
  and one design defect predicted in review. No accidental loss is recorded
  as caught.

**Slowest tests** (recorded times):

| File | Tests | Time |
|---|---|---|
| `test_gate_preflight.py` | 262 | 227 s |
| `test_upgrade.py` | 131 | 72 s |
| `test_reanchor.py` | 168 | 56 s |
| `test_security_marker.py` | 9 | 30 s |

**Judged worthwhile:**
- shared claims across worktrees;
- separating human trust and release operations from plan completion;
- the strict release runner and fast goodnight checks;
- safe Git reads (large, but it guards untrusted input);
- fault-centered testing guidance;
- `board.py --next`, with its loop deferred.

## Options

1. **Do nothing.** v0.7 ships with the meter installed everywhere, plans and
   records keep growing, and every agent carries the new rules every
   session.
2. **Targeted reductions,** the items below. One doctrine proposal, one
   Decision and one test proposal. Most effects are removals.
3. **Deeper reset:** also re-examine the ceremony machinery and the
   lifecycle's commit-per-transition rule. Larger payoff, much larger
   effort; better as v0.8 strategy.

## Recommendation

Option 2, as these items:

1. **Rule freeze.** No new `AGENTS.md` or template rules for the rest of
   v0.7 except the removals below. From v0.8, one in, one out, or a word
   ceiling on `AGENTS.md`.
2. **Living plans.**
   - Plans revise operative text in place for their whole life, with a short
     change log of one line per revision: commit, what changed, why.
   - Attributed records stay append-only and untouched: reviews, responses
     and anything quoting the Maintainer.
   - Changing scope or acceptance criteria after plan review gets a targeted
     plan-review look, and removing scope still needs the Maintainer.
   - Design found missing during implementation returns the plan to
     `revising-plan`; it is not appended as "Strategy" sections.
3. **Record targets.** A verification entry or log is about 150 words: the
   commit, interpreter, counts and gaps; the rest goes in the commit body. One
   current verification record replaces older ones, which Git keeps.
4. **Meter.**
   - Move `meter.py` out of the unconditional install into an opt-in module
     now.
   - Then decide whether a much smaller meter would answer the cost
     question, for example one that reads the tools' own logs on macOS
     first, before finishing the present design.
5. **Exact-replacement editing for doctrine.**
   - Doctrinal files are changed only by exact-match replacement or a patch,
     never by regenerating or re-wrapping them. These are `AGENTS.md`,
     `VENDOR.md`, `RULES.md`, the shipped templates and module rule text,
     skills and `docs/methodology/`, using the existing prescription line in
     `docs/DOCUMENTATION_PLAN.md`.
   - Every review of such a change answers one question: does any rule weaken
     or disappear?
   - A deliberate section rewrite lists the rules it removes or changes.
   - Retire the per-rule pin tests, but keep the copy-parity checks, which
     catch real drift between copies.
6. **Test pruning.**
   - Re-time the full suite first.
   - Cut tests for Cairn-only reporting tools (meter, gauge, test tiers,
     audit report) to a few smoke tests each.
   - Fix `test_security_marker.py`'s setup, at 3 s per test.
   - Ask, as v0.8 strategy, whether the ceremony scripts behind 430 tests and
     about 283 s are bigger than the risk they cover.
   - Give new features a stated runtime budget for their tests.
7. **Focus.** Finish architecture and reuse and the testing guidance before
   any further process work.

**Residual risks:**
- A reviewer may miss a quietly dropped clause. Exact replacement keeps diffs
  small enough that this should be rare, and an optional sentence-level diff
  script can help on large rewrites.
- Moving the meter delays the cost data the Maintainer asked for.

## Open questions

- Should item 5's review question also cover non-doctrinal changes that alter
  agent behavior, as the PR-merge check does?
- What word ceiling, if any, should `AGENTS.md` have from v0.8?
- Is the meter's cost question better answered by an external tool or a
  manual export than by Cairn code?

## Fold-up note

Items 2, 3 and 5 are methodology-general and would ship to adopters; they
need a doctrine proposal with the rate-limit gate.

## Measurements, 2026-11-10

`AGENTS.md`: +40% since v0.6.1 (3,058 to 4,276 words); Maintainer target, about 1,000 words or less. Test cases: +21% (5,913 to 7,165); Maintainer: keep promise tests, cut development-time pins. Details: the commit that added this section.

## Decision on recommendation 1, 2026-11-10

Asked about the rule freeze, the Maintainer replied "I don't think a rule freeze is necessarily the right thing to do", after a scan of the roadmap showed accepted work that adds or changes rules (rows 7d, 7e, 14 and 22, and several v0.8 rows). Then: "Okay, now for this item we are working on, no freeze, just a cap between AGENTS/VENDOR(CLAUDE)/RULES of 1500 words." So recommendation 1 is replaced by a combined cap of 1,500 words on `AGENTS.md`, the vendor wrapper and `RULES.md`. On 2026-11-10 Cairn's three files total 1,441 words (now 1,453 with the cap line in `RULES.md`) and the shipped pair 1,421. On 2026-11-12 the Maintainer raised the cap to 2,000 words: "I don't think we can really keep the cap on every session to 1,500. Let's up that to 2,000." Recommendations 2, 3, 4 and 7 are still open; 5 is done and 6 is under way.

## Decision on recommendation 2 and where to resume, 2026-11-10

Living plans: the Maintainer accepted them ("Accept the living plans. That should really help.") and asked to pause the rest ("queue this for resumption on Thursday, please. Just record the decision."). Accepted as written in the Recommendation above: operative text of a plan is revised in place for the plan's whole life with a one-line change log per revision; reviews, responses and quotations of the Maintainer stay append-only; a scope or acceptance change after plan review gets a targeted plan-review look, and removing scope still needs the Maintainer; design found missing during implementation returns the plan to `revising-plan`.

Not done: the doctrine edit (the plan template and `dev/agent_collaboration.md`); no rule text has changed yet. Resume on Thursday 2026-11-12 at recommendation 3 (record targets), then 4 (opt-in meter) and 7 (focus). Recommendation 5 is done and 6 is under way.

## Discussion on recommendation 3 (record targets), 2026-11-11 (open)

Status: discussed 2026-11-11; direction agreed with the Maintainer 2026-11-12 (see "Agreed direction, 2026-11-12" at the end of this section); not yet a Decision. Nothing in the plan template, `dev/agent_collaboration.md` or `AGENTS.md` has changed. Do not edit the template until the doctrine proposal is accepted.

**The question.** What the plan template asks of a plan's verification records (the notes an agent appends after running checks), and how long they may be.

**Measured on 2026-11-11** with a word-count script over plan headings that contain "verification" (the script was not saved; rerun it before relying on these numbers):
- All 174 plans, archived ones included: 572 such sections, 194,944 words, about 10.5% of plan text. Median 250 words; 452 run over 150; the longest is 3,240.
- The 8 open v0.7 plans hold 67 appended "Implementation verification" records, 15,682 words in all (average 234).
- The template's Verification block was 592 words at v0.5.0, 853 at v0.6.0, 695 after the 2026-10-30 "cut the apparatus" commit (`3cceb2c0`), 852 by v0.6.1, 898 with the benefit sentence (`831d0e3b`, 2026-11-06) and 885 now. The whole template went from 4,004 words at v0.6.1 to 4,832.
- The template requires about ten fields, a command table (Command, Exit, Outcomes, Elapsed, Tokens) and a closing sentence on benefit versus effort. `tools/audit_report.py` only warns when the heading is missing; no tool reads the contents.
- The benefit sentence came from Decision `036a0495` (the human-useful ceremony proposal) on 2026-11-06. Of ten plans archived since, eight closed that same day; the one that closed later (`2026-11-06-adopter-execution-retries`) wrote it. So it is untested, not ignored.

**What the Maintainer said, 2026-11-11:**

> Well, I like limiting the length, but the benefit-vs-cost is intended for us to start evaluating that globally. Can we instead of dropping it, strengthen its use?

> Definitely, this should only be once per plan. I like your suggestions.

> I would like to make this planning template decision with you though

On Tokens: "I think we are retiring the tokens section soon."

**The proposal the Maintainer liked (a recommendation, not a Decision):**
1. Keep the receipt: commit, Python version, commands with counts, non-passes, omissions.
2. Aim for about 700 words in the template's Verification block, and write that target into the v0.8 template-trim row.
3. Strengthen the benefit-versus-cost line. It is due once per plan, in the final verification record, as one labeled line: `**Benefit versus cost**: <verdict> — <benefit>; cost <measured>; remaining burden <measured>`. The verdict is `worth it`, `partly`, `not worth it` or `unknown` (with a revisit condition). Cost comes from measured sources: commits (from Git), elapsed time, Maintainer decisions asked for, and burden in the weight review's units (words added to shipped or always-loaded text, tests added and their seconds, files installed in adopter projects). `tools/audit_report.py` would list each plan's line and count the verdicts in one table at release verification (row 12). Optionally the code reviewer adds a few words agreeing or disagreeing. A verdict word loosens the "not a score" wording of Decision `036a0495`; it is a label, not a number.
4. Do not adopt "one current record replaces older ones". Evidence builds across commits: row 17's three tests passed on a different commit than the joined run.
5. Tokens: the metered-cost plan retires the Tokens column only after every meter check passes, including two real comparisons. Elapsed stays unless timestamps prove it is the same quantity, and `97a0eab3` says to keep both until then. The meter records separately, in a private per-user ledger and a gitignored project file named dev/measurement/meter.json, and ties usage to a plan only when claim timestamps map it reliably. Drop the Tokens column in the change that meets those conditions.

**To settle in the morning:** a final yes on the verdict word and the reviewer's second opinion (the agent's default is yes); the block's word target; where `audit_report.py` gets its pointer; and the order. The edit joins the living-plans edit (accepted 2026-11-10) as one doctrine proposal that changes the plan template and "Plans and records" in `dev/agent_collaboration.md`. It ships to adopters, and row 13 puts it after promise-unit-testing chunk C3.

**Not checked:** whether `audit_report.py` ships to adopters; whether any plan has read its own verdict back later; whether the Decision cost sentence from `036a0495` is used.

### Agreed direction, 2026-11-12 (not a Decision)

The agent put the five-point proposal above to the Maintainer, with a default for each open item. The Maintainer answered:

> Yes to all of it.

**Agreed:**
1. Keep the receipt: commit, Python version, commands with counts, non-passes, known omissions.
2. Target about 700 words for the template's Verification block (885 on 2026-11-11). Write the target into the v0.8 template-trim row.
3. One labeled line per plan, in the final verification record: `**Benefit versus cost**: <verdict> — <benefit>; cost <measured>; remaining burden <measured>`. Verdicts: `worth it`, `partly`, `not worth it`, `unknown` (with a revisit condition). The code reviewer may add a few words agreeing or disagreeing.
4. The label itself is the pointer. `tools/audit_report.py` would find that line in each archived plan's last verification record and count the verdicts in one table at release verification (roadmap row 12). A plan archived before the change counts as "no line", with no warning.
5. Not adopted: "one current record replaces older ones". The Tokens column stays until the metered-cost plan's conditions are met, then goes in that same change.

**Checked 2026-11-12 (answers the first "Not checked" item):** `audit_report.py` and `gauge.py` exist only in Cairn's own `tools/`. The tools an adopter project receives are listed at `bootstrap/_scaffold/config.py` lines 914 to 917: `git_read`, `session`, `meter` and `board`. The folder `templates/modules/default-on/measurement-archive/` holds only a `.gitkeep`. So the verdict table is a Cairn release check; adopters get the line in their template and no roll-up. Whether to ship a roll-up to adopters was not decided. The agent's default is no: each shipped tool adds weight, and nothing reads an adopter's plans. The opt-in meter is the existing route if that is wanted later.

**Next:** one doctrine proposal that changes the plan template and "Plans and records" in `dev/agent_collaboration.md`, joined with the living-plans edit (accepted 2026-11-10). It goes through review and then to the Maintainer for the Decision. Roadmap row 13 orders it after promise-unit-testing chunk C3; whether C3 is finished was not checked. Recommendations 4 (opt-in meter) and 7 (focus) follow.

**Still not checked:** whether any plan has read its own verdict back later; whether the Decision cost sentence from `036a0495` is used.
