# Trimming AGENTS.md to about 1,000 words

**Author**: Claude (coordinating session, recording a proposed move list at the Maintainer's request)
**Model**: Sonnet 5.5 (`claude-sonnet-5-5`)
**Date**: 2026-11-10
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: the weight review (roadmap item 13); a doctrine edit to `AGENTS.md`; the wording-test retirements in the functional-prose-editing plan.

*Tier note.* Strategy work has a High floor and this was written at Sonnet. A High-tier agent should check the table before any rule moves. Nothing in `AGENTS.md` has been edited.

## Summary

`AGENTS.md` is 4,276 words, up from 3,058 at v0.6.1. The Maintainer wants about 1,000 or fewer. The table below keeps about 965 words and moves about 3,300 to homes that already exist. Each move would be an exact replacement checked by one question: does any rule weaken or disappear? Wording tests that fail are retired, not rewritten.

## The question / felt gap

Maintainer, 2026-11-10: "I don't want bloat there." "For AGENTS.md, I prefer something around 1,000 words or less." "We are not supposed to check doctrine files for wording anymore." Then, on this plan: "Please proceed."

## Method

Counted words per paragraph of `AGENTS.md` at commit `b0d9d3a8`. Checked that each proposed home file exists. I did not read the homes to see whether they already say the same thing, and did not read the 49 test files that name `AGENTS.md`.

## Findings

1. **Size.** Words by section: Verification 934, Review 897, Roles 815, Lifecycle and records 660, Working tree and commits 473, Project conventions 308, other 189. Fifteen paragraphs over 100 words hold 2,495 (58%).
2. **Most of it is procedure for one task**, read only when doing that task: plan authoring (212 and 174 words), the integration run (302, 230 and 68), the External read (214), the local development note (258), goodnight (111).
3. **What every session needs:** who decides; claim files and commit by path; never push or decide without approval; no full suite; the protected surfaces; plain language; where to look.
4. **Wording tests.** 49 of 150 test files name `AGENTS.md`, and the plans call 32 of them guarded readers. The accepted rule is not to check doctrine wording, so they are due for retirement and do not gate this trim. Retiring guarded tests needs the re-anchor already owed at the cut.
5. **Overlap.** The v0.8 template-scan proposal edits the high-risk sentence in paragraph 52. Sequence the two edits.
6. **Homes.** `AGENTS.md` says agent duties keep an installed home that agents read. Every move therefore leaves a one-line pointer.

## Proposed disposition

Paragraph numbers count blocks in the file, from 1.

| Paragraphs (words now) | Keep (words) | Move to |
|---|---|---|
| 1-4 purpose (88) | 60 | |
| 6, 9, 10 lifecycle and plan finishing (396) | 90, with 7-8 | `docs/methodology/lifecycle.md`, `docs/methodology/plans.md`, `dev/proposals/_template.md` |
| 7-8 plan goal, finish records (260) | 0 | `dev/plans/_template.md` |
| 12-13 functional prose (76) | 30 | `dev/agent_collaboration.md` |
| 15-20 review details (468) | 40 | `dev/agent_collaboration.md`, `docs/methodology/dual-review.md` |
| 21-23 External read, tiers, choices (427) | 40 | `docs/methodology/dual-review.md`, `dev/proposals/_template.md` |
| 25-29 roles, model tier, retries, plain language, session start (444) | 150 | retries to `docs/methodology/lifecycle.md` |
| 30-33 local note, goodnight (577) | 40 | `dev/reflections/README.md`, `dev/rules/custom_session_routines.md` |
| 35-39 working tree, approvals, defect fix (468) | 160 | `docs/methodology/coordination.md`, `docs/methodology/lifecycle.md` |
| 41-48 verification (932) | 150 | `dev/plans/_template.md` (integration run), `dev/modules/testing-discipline.md`, `docs/release-process.md` |
| 50-55 conventions, protected surfaces (302) | 190 | `bootstrap/SAFETY.md`, `docs/DOCUMENTATION_PLAN.md` |
| 56-57 vendor addendum (22) | 15 | |

Kept words add to about 965.

## Options

- **A. Leave it.** No risk; the bloat stays.
- **B. Move only the largest blocks** (integration run, choosing checks, External read, fresh reviewers, plan goal, local note). Reaches about 2,800 words.
- **C. Trim to about 1,000**, as asked, in two stages.
- **D. A short core plus task files** that skills load. A larger redesign.

## Recommendation

C, in two stages. Stage 1 moves Verification and Review (about 1,800 words) and retires their wording tests. Stage 2 does the rest. Each stage uses exact replacements, lists removed rules in the commit body, and answers the one review question. Residual risks: agents skip rules no longer loaded every session; a rule is lost in a move; 190 words may be too few for the protected-surface and safety rules.

## Open questions

Does the Maintainer's approval of this table count as the Decision? Which stage first? Should the shipped adopter `AGENTS.md` follow? This note does not cover it. Who runs it, given the credit pause?

## What I did not check

Whether each home already holds the moved text or can take it; the shipped template; which of the 49 test files truly pin wording.
