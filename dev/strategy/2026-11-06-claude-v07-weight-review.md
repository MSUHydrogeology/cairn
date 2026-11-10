# v0.7 weight review: what to keep, shrink or stop

**Author**: Claude Opus 5.5 (Strategy)
**Model**: Claude Opus 5.5 (`claude-opus-5-5`)
**Date**: 2026-11-06
**Status**: draft
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
