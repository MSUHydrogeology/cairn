# Principles for combining and trimming rules

**Author**: Claude Sonnet 5.5 (Cairn Developer); principles drafted by a Claude Opus 5.5 advisor agent
**Date**: 2026-11-16
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: the template-trim plan ([`dev/plans/archive/2026-11-16-template-trim-and-rules.md`](../plans/archive/2026-11-16-template-trim-and-rules.md)); the "Designing" section of [`dev/rules/working-agreements.md`](../rules/working-agreements.md)

## Summary

When Cairn's rules must fit a word budget, combine and cut rules; do not waive the budget and do not move the words to a folder adopters never receive. Nine principles say how. They keep the small set of rules that name who alone decides, stop conditions and refusals that protect data, and they cut the long tail. By the advisor's estimate both budgets in the template-trim plan are reachable this way.

## The question

The Maintainer, 2026-11-16, on the trim plan's request to allow the testing module at 1,619 words (target 1,400) and the guide at 5,507 (target 4,800): "I think that those three modules need to be trimmed, not waived. We need some principles for combining rules." They asked for the "not building a fighter jet, building scientific software" and 80/20 ideas, and for "delivering good software, not endlessly developing and never releasing perfect software". Later: "These principles would be relevant to our template trimming efforts later."

## Method

An Opus agent read the trim plan's cut rows, the testing-discipline module, the longest sections of the collaboration guide, the working agreements and the rules README. It wrote advice only and edited no file. Word counts are measured with whitespace-normalized counts of the current text; savings are estimates, because it did not replay the plan's rows. It did not read the guide's shorter sections or Cairn's own copy, did not mine the reflections beyond a keyword search, and did not check whether a test pins the wording of any span it names.

## Principles

1. **80/20: keep the rules that have prevented real harm.** If no reflection, review finding or Maintainer correction shows the rule stopped a real mistake, cut it to one clause or delete it.
2. **Scientific software, not a fighter jet.** If a sentence lists cases, fields or steps a competent agent would infer from the rule above it, replace the list with "use judgment" or delete it.
3. **One home, one pointer.** If two sentences in the shipped set state the same rule, keep the one in the file every adopter gets (the guide, not the optional module) and make the other a pointer of ten words or fewer.
4. **Do not restate what a tool enforces.** If a script, test or template field already checks it, give it one line naming the tool, or nothing.
5. **One short example, no history.** Keep an example only if it prevents a misreading; of two examples that teach one point, keep the shorter.
6. **A short list that is never cut.** A sentence that names an action only the Maintainer may take (push, sign, tag, release, a Decision, lowering a tier, a re-anchor, conceding accepted scope), a stop condition, or a refusal that protects adopters' data or the project's integrity keeps its meaning exactly. Its wording may still merge with a neighbour. The list is short because these are the failures that cannot be undone; everything else is reversible and takes the lighter lane.
7. **Ship; cut rather than waive or defer.** A rule not worth its words is deleted. Stop revising when a reviewer cannot name a real defect. A rule for doubt must be cheap to follow: one action, not a procedure.
8. **Each home has a word budget; a new rule swaps an old one out.** A revision that adds a rule to a file at its budget names the sentence it replaces.
9. **More reviewer detail means a shorter rule plus a pointer.** If two reviewers ask for detail on one rule, tighten the rule and point to the template or method document that holds the detail.

## Worked examples (suggestions; check each against the plan's keep-verbatim list)

- **Module, test paragraphs.** Two sentences say the same thing (delete private-helper, pinned and same-branch tests; never add a test file per plan, bug or finding). Combined: *Keep a permanent test only for a listed promise checked through a public entry point; delete scratch, private-helper, pinned and same-branch tests before archive.* The guide's Verification paragraph says it a third time; point there.
- **Guide, plan finishing, stated twice.** Keep the "Plans and records" version; Verification becomes: *A plan finishes as in "Plans and records"; the arc owner runs one integration selection after connected plans finish.*
- **Guide, External read.** Combined: *Only the Maintainer calls an External read, quoted verbatim; agents may name a risk but never request one, and the call grants no other authority.*

## Where the words are

| Category | Now (measured) | Estimated saving |
|---|---|---|
| Module: Pareto, Developmental and Promises paragraphs, which repeat each other and the guide | about 370 | 100 |
| Module: "Choose change checks", which repeats guide Verification | 155 | 60 |
| Module: Advisory report, which restates `--help`; the two mutation paragraphs merged | 60; 186 | 30; 40 |
| **Module total** (gap 219) | | **about 230** |
| Guide: External read | about 335 | 250 |
| Guide: nine review lenses as one-line names | 404 | 250 |
| Guide: plan-opening paragraph with six "waives no ..." lists, and duplicated plan-finishing text | about 514 | 200 |
| Guide: scope-reduction trap after the fifth guide cut | about 190 | 90 |
| **Guide total** (gap 707) | | **about 790** |

The module is the tight one. Its margin depends on merging the two mutation paragraphs, which includes the keep-verbatim paragraph on investigating surviving mutations. Without that merge the module ends about 30 words over. Closing the last 30 would mean shortening the "simulation models verify at three timescales" items, which the plan protects for the scientific-run-evidence plan. The Maintainer decides that, if it comes to it.

## What this does not settle

- The plan's keep-verbatim list was built by keyword search (`refus`, `hostile`, `negative`, `guard`), so it protects whole paragraphs that only mention those words. Principle 6 shrinks it; the plan author applies that.
- The exact wording. The Maintainer, 2026-11-16: "we'll finalize at template trimming". The template-trim plan applies these principles to its cuts, and the wording is settled then, against what the cuts show.

## Already in force

Two working agreements the Maintainer approved on 2026-11-16 (`fdba0cf3`, in `dev/rules/working-agreements.md`) already carry part of this: "Keep rules and specifications short" (Designing) matches principles 2 and 9, and "Size a review to the change" (Reviewing) is its counterpart for reviews. When the wording is final, those two lines and these nine principles become one short list in that file, one line each, and this note is archived as the reasoning behind it (principle 3: one home, one pointer).

Budget fact for principle 8: since the secrets rule landed (`c3f5c1d4`, `75f02e2d`), the shipped `AGENTS.md`, `VENDOR.md` and `RULES.md` total 1,499 of their 1,500 words, so any rule the trim adds to them must swap one out until the trim frees room.

## Next

The plan author revises the module and guide cut rows by these principles so both targets are met, with no waiver and no words moved to Cairn-only `docs/`; the plan then returns for a check. At the end of the trim, the principles are finalized and merged into the working agreements as above. Nothing here changes a shipped file.
