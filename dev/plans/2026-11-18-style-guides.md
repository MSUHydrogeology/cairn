# Plan: Style guides and onboarding

**Source proposal**: dev/proposals/archive/2026-11-12-claude-style-guides.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/working-agreements.md, dev/rules/protected-surfaces.md
**In brief**: Give people an explanatory code style guide, agents concise conventions, and new projects a task to create both.

## Build summary

Describe Cairn's actual practices for people and keep actionable agent conventions short. Install guidance and seed a suitable task for each new-project preset, preserving project-owned boards on reinstall. Expected work is one to three agent sessions; survey and install-check results are the main uncertainty. Target v0.8; layout and the RULES stub are present.

## Source proposal

The accepted heavy proposal specifies a human guide, operative agent extract, advisory synchronization, adopter guidance and three onboarding seeds. Its Decision retains ordinary and Security Review and no recurring human operation.

## Scope

Survey current `install/`, `dev/tools/` and applicable scripts read-only. Add `docs/style_guide.md`, revise `dev/rules/conventions.md`, the Cairn `RULES.md` route and both `dev/rules/README.md` copies. Update `templates/modules/default-on/documentation-plan.md` and all three preset seeds in `templates/onboarding/`. Update relevant public-install tests in `tests/`. Doctrine surface: project governing rules and shipped adopter guidance; descriptive explanation belongs in docs. No synchronization pin, generator, new installer behavior or backfill.

**Reuse.** N/A: no code added; extend existing public-install promise tests and seed machinery.

Proposed paths:
- `docs/style_guide.md`

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Survey practices and write guide and routed conventions | Accepted proposal | Human guide and agent rules |
| C2 | Add installed guidance and preset tasks | C1 | Module and onboarding prose, public-install checks |
| C3 | Verify and submit for independent code review | C1–C2 | Evidence and review-ready change |

## Acceptance criteria

**C1.** The guide begins with the advisory sync note, explains the authority distinction and links Cairn Plain Language. A why paragraph, quick-reference table and topical sections describe surveyed practice; introduce a rule only for a real inconsistency. About ten actionable agent entries retain dependency, standard-library, placement, naming, canonical-home, licensing and retry duties. Routed conventions govern coding decisions; report discrepancies and propose correction. Optional preference drift grants no security, dependency or license exception. Both README copies retain indexing and other exclusions. Remeasure Cairn's three-file 2,000-word cap and shipped 1,500-word cap.

**C2.** Installed `dev/modules/documentation-plan.md` has a Style guide section under 300 words that directs placement through the installed `docs/DOCUMENTATION_PLAN.md`. Fresh installs of greenfield, legacy and team presets each seed one appropriately tailored task to make both versions. Board-relative references reach that section; when the module is deselected, the task remains self-contained without a dangling link. Existing boards are not backfilled. Public scaffold checks in `tests/test_onboarding_slot_substitution.py` cover each preset and opt-out; `tests/test_onboarding_seed_roster.py` retains reinstall protection. No test pins wording or synchronization.

**C3.** Independent ordinary and Security code reviews cover all changes. Record the survey, checks, omissions and benefit versus cost; all findings and required evidence are dispositioned before archive.

## Scope delta

**Scope delta**: preserved

## Verification

Before implementation select named tests with `python tests/tier_inventory.py for <changed paths>`; for governing text include the reviewed range. Run selected tests and claim, link, snippet and neutrality prose gates using `/Users/kendal30/conda_envs/lhm/bin/python3.13`. Inspect readers and byte pins; remove wording pins under project rules. Use agent scenarios to assess prose and retained duties without freezing wording.

For the security preflight's S2/S3, demonstrate separately that removing a seed, breaking the installed reference, and enabling board reseeding each fails its targeted public-install check; run the unmutated selected install checks as positive control. Preserve existing filtering, safe writes, dry-run and board protections. Inputs are reviewed prose and project-controlled selections; a project writer can still introduce hostile prose. Review does not claim semantic synchronization or attacker detection. No scientific check applies. Tree certification and release operations retain their existing triggers.

## Plan review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: d706018df981761de24b595ceb7ae970f2c18b88
**Obligation**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the plan retains the two guide audiences, binding authority, all three onboarding seeds and the opt-out route without a synchronization pin. -- Scope, C1–C2, accepted Proposal
2. **Best alternative.** Existing conventions, module guidance and seed machinery deliver the same result without a generator or new installer. -- Scope, Reuse
3. **What would show it wrong?** A fresh preset missing its task, an inaccessible installed reference, or a reinstall overwriting a project board would falsify delivery. -- C2, Verification

The operative duties remain in routed conventions; the installed module and board references serve adopters. No planned rule loss found. Checks address public delivery and preservation rather than prose wording; parent-owned joined integration remains under the project verification rule. Coverage: compared committed plan with accepted proposal and review rules; did not run installation, mutations or scenarios, or assess the security boundary. Security Review remains separate.

## Plan review -- Codex Sol (Security Review, High) -- 2026-11-18

Reviewed commit: d706018df981761de24b595ceb7ae970f2c18b88

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Steelman.** Onboarding can teach both guide formats while existing binding rules continue to govern development.

**Foundations**

1. **Should this happen as framed?** Yes. C1 confines drift to optional preferences. The routed conventions retain the dependency-budget check, standard-library limit and licensing duties, and governing rules retain priority (C1, `dev/rules/conventions.md`, accepted Proposal items 2–5).
2. **Best alternative.** Use the installed documentation-plan guidance and existing Markdown seed renderer. C2 permits self-contained instructions with a reference used only if the module is installed (`install/_scaffold/install.py:1361-1393`, C2).
3. **What would show it wrong?** An opt-out pointing to an unavailable guide, or a reinstall replacing adopter board text. The existing public entry points cover task delivery, installed references and preservation, with a separate negative control for each promise (C2, Verification).

**Rule retention.** Both README edits retain root indexing. The plan keeps adopter authority in installed files, and the seeded task supplies guidance without granting implementation authority or exceptions (C1–C3, Proposal S1–S5).

**Coverage.** Compared the accepted scope with the committed plan, current conventions, seed rendering and module mapping. Implementation text, install results, mutation runs and agent behavior were outside this pass.
