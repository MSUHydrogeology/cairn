# Trimming AGENTS.md to about 1,000 words

**Author**: Claude (coordinating session, recording a proposed move list at the Maintainer's request)
**Model**: Sonnet 5.5 (`claude-sonnet-5-5`)
**Date**: 2026-11-10
**Status**: draft (stages 1 and 2 done 2026-11-10; no review gate beyond the lost-content check)
**Type**: design-exploration
**Surfaces this would feed**: the weight review (roadmap item 13); a doctrine edit to `AGENTS.md` and to the shipped `templates/core/AGENTS.md`; the wording-test retirements in the functional-prose-editing plan.

*Tier note.* Strategy work has a High floor and this was written at Sonnet. A High-tier agent should check the table before any rule moves. Nothing in `AGENTS.md` has been edited. *Revised 2026-11-10:* the first version named `docs/methodology/` files as homes. Adopters do not receive that folder, so the table now uses homes adopters do receive.

## Summary

`AGENTS.md` is 4,276 words, up from 3,058 at v0.6.1. The Maintainer wants about 1,000 or fewer, with `AGENTS.md` holding mostly what is important enough to ship, plus pointers to project-specific rules. The shipped adopter template is almost the same file: 3,812 of Cairn's words match it, and only 413 are Cairn-only. So the trim is mostly a change to what every adopter receives. The Cairn-only 413 words can move at once with no adopter effect. The shipped rest moves to files adopters already receive, one exact replacement at a time.

## The question / felt gap

Maintainer, 2026-11-10: "I don't want bloat there." "For AGENTS.md, I prefer something around 1,000 words or less." "We are not supposed to check doctrine files for wording anymore." "AGENTS.md can and should contain pointers to project-specific rules. What's in AGENTS.md should essentially mostly be the things that are important enough to ship with Cairn. Some localization is permitted, but most of that should live elsewhere." "Yes, the shipped template should be very lean." "In moving things to templates, I don't want plan and proposal templates to grow substantially. Consider that some details not relevant for Agent execution may need to go into documentation." "This does not need a Security Review ... It should only be review to assure that content is not lost, and that length targets are kept."

## Method

Counted words per paragraph of `AGENTS.md` at commit `69d62910`. Compared each paragraph with `templates/core/AGENTS.md` by text similarity (80% or more counts as matching). Read `bootstrap/_scaffold/config.py` install specs and the `templates/core` tree to see which homes adopters receive. I did not read the homes to see whether they already say the same thing, and did not read the 49 test files that name `AGENTS.md`.

## Findings

1. **Size.** Words by section: Verification 934, Review 897, Roles 815, Lifecycle and records 660, Working tree and commits 473, Project conventions 308, other 189. Fifteen paragraphs over 100 words hold 2,495 (58%).
2. **Shipped versus local.** The shipped template is 4,343 words. Of Cairn's 4,276, 3,812 match it, 51 partly, 413 are Cairn-only. The largest Cairn-only blocks: the proposal rule for doctrine and engine changes (97 words, with the high-risk surface list), the full-suite rule (82), the installer binding (58), the AST baseline rule (46), file naming (41), and two purpose lines (62).
3. **Most of it is procedure for one task**, read only when doing that task: plan authoring, the integration run, the External read, the local development note, goodnight.
4. **Homes adopters receive:** `dev/agent_collaboration.md`, `dev/plans/_template.md`, `dev/proposals/_template.md`, `dev/strategy/_template.md`, `dev/rules/README.md`, `dev/reflections/README.md`, and the installed modules (`dev/modules/dual-review.md`, `testing-discipline.md`, `security-review.md`). **Cairn-only, not installed:** `docs/methodology/`, `docs/release-process.md`, `bootstrap/SAFETY.md`, `dev/rules/custom_session_routines.md`.
5. **Wording tests.** 49 of 150 test files name `AGENTS.md`. Two Haiku agents sorted the 213 functions that touch it (spot-checked): 153 do not depend on its wording, 33 are helpers, 9 are copy-parity checks, 9 pin wording and 9 are unsure. Two of the pins are only tail lines of otherwise sound tests. Four guard the Verification text that stage 2 moves. The accepted rule is not to check doctrine wording, so the pins are retired first. Retiring guarded tests needs the re-anchor owed at the cut. These tests live only in Cairn's repository; adopters do not receive or run them.
6. **Overlap.** The v0.8 template-scan proposal edits the high-risk sentence in the Cairn-only block. Sequence the two.

## Proposed disposition

Paragraph numbers count blocks in the file, from 1.

| Paragraphs (words now) | Keep (words) | Move to |
|---|---|---|
| 1-4 purpose (88) | 60 | |
| 6, 9, 10 lifecycle, plan finishing (396) | 90, with 7-8 | `dev/agent_collaboration.md`, `dev/proposals/_template.md`, `dev/plans/_template.md` |
| 7-8 plan goal, finish records (260) | 0 | `dev/plans/_template.md` |
| 12-13 functional prose (76) | 30 | `dev/agent_collaboration.md` |
| 15-20 review details (468) | 40 | `dev/agent_collaboration.md`, `dev/modules/dual-review.md` |
| 21-23 External read, tiers, choices (427) | 40 | `dev/modules/dual-review.md`, `dev/proposals/_template.md` |
| 25-29 roles, tier, retries, plain language, session start (444) | 150 | retries to `dev/agent_collaboration.md` |
| 30-33 local note, goodnight (577) | 40 | `dev/reflections/README.md`; goodnight detail home to be chosen |
| 35-39 working tree, approvals, defect fix (468) | 160 | `dev/agent_collaboration.md` |
| 41-48 verification (932) | 150 | `dev/plans/_template.md`, `dev/modules/testing-discipline.md` |
| 50-55 conventions, protected surfaces (302) | 30 | Cairn-only text to `dev/rules/certifying-runs.md`, `protected-surfaces.md` and `conventions.md`, routed from a new `RULES.md`; not shipped |
| 56-57 vendor addendum (22) | 15 | |

Kept words add to about 965. The Cairn-only share (413 words) leaves first and needs no change to the shipped template.

## Options

- **A. Leave it.** No risk; the bloat stays.
- **B. Move only the Cairn-only 413 words** to `dev/rules/`. No adopter effect; reaches about 3,860.
- **C. B, then trim the shipped text to about 1,000**, in two stages, changing `templates/core/AGENTS.md` and Cairn's copy together.
- **D. A short core plus task files** that skills load. A larger redesign.

## Recommendation

C, starting with B now (done, commit `98a7e874`). Stage 2 trims the shipped template and Cairn's copy together, in this order for every block: 1) retire the tests that pin the wording of the text, 2) move it exactly, 3) rewrite the moved text more briefly, because much of it is too detailed to hold in an agent's memory. Detail that matters but is not doctrine goes to documentation. Stage 2 covers Verification and Review first (about 1,800 words), then the rest. Tests to retire first: those pinning `AGENTS.md` wording (done, `600dd986`) and those pinning plan, proposal or strategy template phrasing. A scan found 8 of 150 test files quoting template text; seven check structure (board-parser markers, installed equals source) and stay. One, `test_review_sweep_ships.py`, holds a 198-line table of required rule phrases, and some of its parity checks find their text by a lead phrase, so a rewrite would break them. Each move keeps a one-line pointer. Review asks two questions only: is any content lost, and are the length targets kept. There is no Security Review (Maintainer, 2026-11-10). Plan and proposal templates must not grow substantially. Haiku agents can carry out the moves once each has an exact destination (Maintainer, 2026-11-10). Residual risks: agents skip rules no longer loaded every session; a rule is lost in a move or a rewrite; adopters with edited `AGENTS.md` meet merge conflicts on a large deletion at upgrade; 190 words may be too few for the protected-surface and safety rules.

## Open questions

Answered 2026-11-10: the shipped template should be very lean (about 1,000 words), and no Security Review. Cairn adopts itself: its own `RULES.md` router plus theme files in `dev/rules/`, and every install gets a `RULES.md` stub (roadmap item 23). Still open: where goodnight detail lives; which documentation page takes the detail that agents do not need to execute; how an upgrade merges a large deletion.

## Stage 2 manifest and checks (2026-11-10, run before any move)

Paragraph numbers are blocks in the shipped `templates/core/AGENTS.md` (4,343 words, 63 blocks). Checks run on the committed tree with the project Python 3.13.

1. **Homes.** I installed all three profiles into scratch folders. Reached by all three: `dev/agent_collaboration.md`, the plan, proposal and strategy templates, `dev/reflections/README.md`, `dev/rules/README.md`, the session-start and session-end skills. **Not reached by `solo-greenfield`:** `dev/modules/dual-review.md`, `testing-discipline.md`, `model-selection.md`, `security-review.md`. This corrects the table above, which named module homes. Move to core homes only; the main destination is `dev/agent_collaboration.md`, not a template, so the plan and proposal templates do not grow.
2. **Already stated elsewhere?** Only block 47 (tree-certification record) is fully in a shipped file (the plan template, 100% of its six-word runs). The other blocks are 0 to 44% covered, so they move; they are not duplicates.
3. **Seven plans being implemented name `AGENTS.md` in their Scope:** `functional-prose-editing`, `promise-unit-testing` (its chunk C3 rewrites the Verification rule), `achievable-plan-prerequisites`, `local-development-notes`, `person-facing-documentation`, `metered-cost`, `safe-git-reads`. I read their Scope sentences only, not their chunk lists.

**Wave 1, no plan names these passages (to my reading):** blocks 20-23, 25-27 (Review), 31 (retries), 39, 40, 42, 43 (working tree and commits). 1,353 words move exactly to `dev/agent_collaboration.md`, each with a pointer; shipped `AGENTS.md` falls to about 3,000.
**Wave 2, after the owning plans finish or their owners agree:** 6-7 (functional prose), 14-16 (plan goal and finishing), 19, 34-37 (local note, goodnight), 45-52 (Verification; 47 is deleted as covered). 1,737 words; about 1,300 would remain.
**Then the rewrite pass** takes what remains to about 1,000, and rewrites the moved text shorter.

Open: whether moving text that an accepted plan delivered needs that plan's Scope delta; the Maintainer's call.

## Stage 2 result (2026-11-10)

Maintainer, 2026-11-10: "I authorize you to take charge of anything planned for v0.7 that touches AGENTS.md. I want it lean and mean." Commits: `c9c0b06d` (verbatim move), `c8be5796` (rewrite, three wording-pin tests deleted), `c48da8e4` (ten rules restored after the lost-content review).

Words, baseline `3fba07ca` (`len(text.split())`): shipped `AGENTS.md` 4,343 to 1,111; Cairn's 3,925 to 931. With `dev/agent_collaboration.md` and the reflections README, adopters 8,012 to 7,238 (-10%) and Cairn 7,714 to 7,179 (-7%). About 146 of the shipped 1,111 are install-slot placeholders. Not touched: the plan template (4,915), the proposal template (4,014), the testing-discipline module (2,148). Those, with `agent_collaboration.md` (now 5,556 shipped), are where the remaining bulk is.

Open: the Wave 2 plans (`promise-unit-testing` C3 and the others that name `AGENTS.md`) have not been told that the text moved; the Maintainer has not re-anchored; the upgrade merge of a large `AGENTS.md` deletion is untested; 14 heavy test files were not run.

## What I did not check

Whether each home already holds the moved text or can take it; how the upgrade merge treats a large deletion; which of the 49 test files truly pin wording.

## Upgrade trial for an adopter who edited AGENTS.md, 2026-11-11

Question left open after the trim: what does an upgrade do to an adopter who edited a long `AGENTS.md`? Measured in a scratch folder: a solo project installed from the pre-trim source (`98a7e874^`, shipped `AGENTS.md` 4,343 words), edited, committed, then planned and staged with today's Cairn (`upgrade --plan`, then `--stage`).
- **Trial A, a local rule appended at the end:** `AGENTS.md` is "locally-modified (merged clean)". The adopter's addition survives with no conflict.
- **Trial B, a one-word edit inside a paragraph the trim removed or rewrote:** `AGENTS.md` is a conflict. The staged merge has one conflict region of 93 of 206 lines, and `--apply` refuses until it is resolved. This is the documented review flow in `bootstrap/UPGRADE.md`, and the file is not broken.
- **Not tested:** `--apply` after resolving; the other two profiles; an adopter who edited several places; Windows.
