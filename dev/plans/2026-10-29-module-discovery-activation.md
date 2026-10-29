# Plan: Module discovery and first use

**Source proposal**: dev/proposals/archive/2026-10-29-codex-module-discovery-activation.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Make installed modules discoverable and give each selected module a useful first task.

## Source proposal

The accepted proposal requires selection-specific inventory and first-use tasks on initial install and later adoption, preserving adopter work and reporting conflicts. Modules remain optional; architecture-review retains its existing scope.

## Scope

Change the scaffold install, upgrade, lock baseline and manifest paths, module metadata and onboarding templates, installed session pointers and bootstrap manual-adoption instructions. The 22-module task and entry-point design is in [inventory](2026-10-29-module-discovery-activation/inventory.md); validate each against the installed files, including required inputs and expected results. No new architecture rubric or recurring obligation is introduced.

**Reuse.** Searches `rg 'onboarding|render.*lock|adopt.module|MODULE' bootstrap/_scaffold/{install,upgrade,cli}.py` and `_MODULE_MAPPINGS` in `config.py` found `_rendered_onboarding_overlay`, shared with clean lock rendering, and the existing adoption and path guards. Generalize those paths rather than scan the target for authority or create a parallel installer. Search readers and callers of each changed surface before implementation and extend the map below for any found.

### Documentation / doctrine surface

Route installed inventory and manual-copy steps to module/bootstrap documentation, operational pointers to relevant shipped session templates, deliberation here; follow `docs/DOCUMENTATION_PLAN.md`. No new doctrine premise.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Audit mappings and entry points, implement shared selection-based rendering and install | Both plan reviews folded | Inventory, tasks and consistent lock baseline |
| C2 | Reconcile upgrades and later adoption, including existing installations; document manual path | C1 | Safe updates and actionable conflict recovery |
| C3 | Exercise public paths, mutations and documentation gates; record stable verification | C1–C2 | Evidence for code review |

## Acceptance criteria

**C1.** The actual resolved roster, including preset, exact list, empty list and add/remove, drives one inventory entry and distinct task per selected module. Each entry names purpose and a shipped usable entry point; each task gives inputs and observable result. No unselected task appears; no installer executes a task. The live output, manifest and clean lock baseline agree. Existing preset tasks remain intact without duplication. Session pointers discover the inventory without mandating use.

**C2.** Install and `upgrade --adopt-module` reconcile marked generated entries by module identity, preserving unrelated text, checked state and edits. An unchanged generated entry can be added or removed; an edited or completed entry whose removal or replacement would lose work causes a reported conflict with explicit manual steps and no partial inventory, planning or lock update. Legacy unmarked or ambiguous content is never guessed away: migrate only when unambiguous, otherwise report manual reconciliation. Repeat adoption, including already-adopted modules, repairs safely or reports conflict. Manual-copy instructions name the concrete inventory, task and lock steps; they do not claim detection. Validate all target paths and conflicts before writes; preserve existing upgrade safeguards.

**C3.** Public-entry tests independently compare selection to tasks, verify each shipped entry point, preservation, idempotence, removal, conflicts, linked destinations and clean baseline across install and upgrade plan/stage/apply. Four separate mutations remove a selected task, add an unselected task, alter preserved work, and change the baseline; each relevant check fails against an unmutated passing control. Record commands and outcomes. No scientific check applies.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A: run `bootstrap/tests/test_onboarding_seed_roster.py`, `test_module_roster.py`, `test_module_merge_lockfile.py`, `test_upgrade_module.py`, and `test_upgrade_module_additions.py` under `bootstrap/tests/`, plus new behavioral nodes in those owning files for the criteria above. Search `rg -n 'onboarding|_MODULE_MAPPINGS|adopt.module|rendered_onboarding' bootstrap/tests bootstrap/_scaffold templates` for consumers and add their owning tests. Exercise `bootstrap/scaffold.py --summary`, `--dry-run`, `--manifest` and temporary installs for representative preset, exact, empty and add/remove profiles; verify manual and automated later adoption. Run `python scripts/check_cairn.py`, `python scripts/claim_check.py` on changed prose, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check`, and applicable neutrality gate. Respect existing frozen-file and AST-pin ceremonies; if triggered, stop at their Maintainer fence.

Boundary B: **wide**, because installation and lockfile are contracts. On the clean final implementation commit under Python 3.13, run the mapped families, discovered consumers, public paths, mutation controls and standing gates; record tested SHA, range, interpreter, clean pre/post state, commands, counts, timings, non-pass dispositions and omissions, with `Certified by: pending`. Do not run the full suite absent an authorized certification point. Independent code review owns Boundary C falsification.
