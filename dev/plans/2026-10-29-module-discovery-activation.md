# Plan: Module discovery and first use

**Source proposal**: dev/proposals/archive/2026-10-29-codex-module-discovery-activation.md
**Status**: revising-plan
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


## Plan review -- Codex (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: f56fe9bcae4220d9f0f19c950ba09256f7776986
Target: opening plan and module first-use inventory
Prior findings: none
Assurance path: required(Internal + Internal Security Review)
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** The accepted outcome is sound, but the plan leaves the reconciliation design and reviewed test mapping unresolved, so it cannot yet direct its implementation -- `dev/plans/2026-10-29-module-discovery-activation.md` C1–C3 and Verification.
2. **Best alternative.** Generalize the existing shared onboarding renderer and use the resolved roster as authority, with an explicit conservative migration and baseline strategy; this avoids a second installer while retaining the accepted outcomes -- `bootstrap/_scaffold/install.py:1122`, `bootstrap/_scaffold/upgrade.py:1764`.
3. **What would show it wrong.** A real existing installation whose edited or completed seed is lost or duplicated, or whose repeat adoption cannot produce matching inventory, tasks and baseline, would disprove delivery -- `bootstrap/_scaffold/install.py:1246`, `bootstrap/_scaffold/upgrade.py:1161`.

**P1 — Settle the reconciliation before implementation.** C2 states desirable outcomes but leaves unspecified where inventory is stored, how generated entries and their prior unedited versions are identified, how existing preset seeds map to module tasks without duplication, and how a legacy installation obtains the selection and baseline needed for later adoption. The existing slot is replaced as a whole and the upgrade reconstruction explicitly does not reproduce onboarding tasks. An implementer must invent the core migration and comparison contract after review. Recommend specifying the representation, authoritative selection and baseline sources, identity/migration rules, and conflict/commit ordering for install, upgrade and already-adopted cases, including concrete manual recovery. Preserve all accepted outcomes; conservative conflict is available when identity cannot be established.

**P2 — Complete the reviewed verification map.** The accepted proposal requires exact nodes and input sets; the plan names five starting families and postpones discovering consumers and new behavioral nodes until implementation. C3's aggregate checks do not assign selection, legacy migration, conflict atomicity, and stage/apply to specific public paths or tests. Recommend mapping each invariant and public path to existing or planned named test nodes and representative input sets now, including all 22 rows and both adoption paths; retain discovery during implementation for newly found readers. This allows review of whether each promised behavior has an independent check.

**Evidence and sweep.** The inventory lists 22 distinct modules and names a first action and expected result for each; C1 requires validating their shipped entry points and inputs. The plan retains optionality, architecture scope, no task execution, and four independent mutation controls. Its shared-renderer direction is simpler than another installation mechanism. The two findings address design completeness, production paths and the evidence trigger; no scientific result is changed.

**Coverage / gaps**: Read the committed plan, inventory, accepted proposal, template and relevant installer/upgrade entry points. Did not execute prospective tasks or enumerate every installed artifact; their validation remains an implementation criterion. This pass clears only the ordinary plan-review obligation; the separate Security Review remains open.
