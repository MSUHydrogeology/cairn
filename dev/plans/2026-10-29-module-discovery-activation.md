# Plan: Module discovery and first use

**Source proposal**: dev/proposals/archive/2026-10-29-codex-module-discovery-activation.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Make installed modules discoverable and give each selected module a useful first task.

## Source proposal

The accepted proposal requires selection-specific inventory and first-use tasks on initial install and later adoption, preserving adopter work and reporting conflicts. Modules remain optional; architecture-review retains its existing scope.

## Scope

Change the scaffold install, upgrade, lock baseline and manifest paths, module metadata and onboarding templates, installed session pointers and bootstrap manual-adoption instructions. The 22-module task and entry-point design is in [inventory](2026-10-29-module-discovery-activation/inventory.md); validate each against the installed files, including required inputs and expected results. The [reconciliation design](2026-10-29-module-discovery-activation/reconciliation.md) fixes representation, migration, ordering and test inputs. No new architecture rubric or recurring obligation is introduced.

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

**C2.** Install and `upgrade --adopt-module` reconcile marked generated entries by module identity, preserving unrelated text, checked state and edits. An unchanged generated entry can be added or removed; an edited or completed entry whose removal or replacement would lose work causes a reported conflict with explicit manual steps and no partial inventory, planning or lock update. Legacy unmarked or ambiguous content is never guessed away: migrate only when unambiguous, otherwise report manual reconciliation. Repeat adoption, including already-adopted modules, repairs safely or reports conflict. Manual-copy instructions name the concrete inventory, task and lock steps; they do not claim detection. Prepare and preflight as specified in the reconciliation design before generated writes, the adoption loop and the already-recorded shortcut; revalidate staged inputs at apply. Refusal preserves inventory, planning and lock bytes, without claiming rollback of unrelated prior installer writes. Preserve existing upgrade safeguards.

**C3.** Public-entry tests independently compare selection to tasks, verify each shipped entry point, preservation, idempotence, removal, conflicts, linked destinations and clean baseline across install and upgrade plan/stage/apply. Four separate mutations remove a selected task, add an unselected task, alter preserved work, and change the baseline; each relevant check fails against an unmutated passing control. Record commands and outcomes. No scientific check applies.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A: execute the named nodes and input sets in the reconciliation design, then run `bootstrap/tests/test_onboarding_seed_roster.py`, `test_module_roster.py`, `test_module_merge_lockfile.py`, `test_upgrade_module.py`, and `test_upgrade_module_additions.py` under `bootstrap/tests/`, plus new behavioral nodes in those owning files for the criteria above. Search `rg -n 'onboarding|_MODULE_MAPPINGS|adopt.module|rendered_onboarding' bootstrap/tests bootstrap/_scaffold templates` for consumers and add their owning tests. Exercise `bootstrap/scaffold.py --summary`, `--dry-run`, `--manifest` and temporary installs for representative preset, exact, empty and add/remove profiles; verify manual and automated later adoption. Run `python scripts/check_cairn.py`, `python scripts/claim_check.py` on changed prose, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check`, applicable neutrality gate, and `bootstrap/tests/test_security_lint.py` (disposition any Bandit skip). Respect existing frozen-file and AST-pin ceremonies; if triggered, stop at their Maintainer fence.

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


## Plan review -- Codex Security (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: 3c19dcfc3c4d627f7504232952d92ef6c75fea03
Target: operative plan, inventory, accepted proposal and ordinary findings
Prior findings: none for this obligation; ordinary P1 and P2 remain open
Assurance path: required(Internal + Internal Security Review)
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** The plan preserves the accepted security boundaries, but needs an explicit integration order before its no-partial-update promise can guide implementation -- C2; `bootstrap/_scaffold/cli.py:563`; `bootstrap/_scaffold/upgrade.py:1764`.
2. **Best alternative.** Extend the existing shared renderer and guarded adoption path with a read-only reconciliation preparation step before committing generated changes; retain conservative manual recovery when legacy identity is uncertain -- `bootstrap/_scaffold/install.py:1122`; `bootstrap/_scaffold/security.py:110`.
3. **What would show it wrong.** A linked inventory destination or edited task discovered after another generated artifact or its lock record changes would defeat containment or conflict preservation -- C2; `bootstrap/tests/test_upgrade_module_additions.py::test_symlinked_destination_after_stage_blocks_apply`.

**S1 — Specify the security integration points and their checks.** This specializes ordinary P1/P2 rather than requesting a second mechanism. The current install CLI writes core and skills before onboarding, then installs modules; adoption creates missing module destinations inside its loop and commits lock/cache afterward, while an already-recorded module returns before that loop. C2 promises validation before writes and no partial inventory/planning/lock update, but does not locate preparation, refusal and commit relative to these paths or upgrade stage/apply. Appending reconciliation after adoption's loop or leaving its early return unchanged would break that promise. Specify which generated artifacts are prepared together, where each public path checks conflicts and containment, and when their lock/base changes commit. Define the scope of the no-partial-update guarantee without silently expanding it to rollback of every pre-existing installer write. For stage/apply, revalidate destinations and preservation assumptions at apply rather than relying solely on stage-time checks.

The satisfier is a folded ordering design plus named public-entry tests: initial/repeated install, new/already-recorded adoption, and staged upgrade with a destination or task changed after staging. Assert unchanged inventory, planning and lock bytes on refusal; include linked destination, dangling link and linked parent for the new inventory and planning writes. Extend the existing containment owners rather than creating a parallel guard (`bootstrap/tests/test_upgrade_lockfile_path_containment.py`, `bootstrap/tests/test_upgrade_module_additions.py`). Map the engine's standing security lint explicitly: `bootstrap/tests/test_security_lint.py` documents its Bandit trigger and missing-tool skip; disposition every non-pass under Boundary B. No broad-suite run is needed for this plan review.

**Evidence and sweep.** Selection remains resolved-profile/mapping authority, not inventory text; tasks do not execute during install, and optionality remains explicit (C1; accepted Security preflight S1–S5). Existing target/ancestor guards are reusable, not proof of coverage for new writes (`bootstrap/_scaffold/security.py:110`). The inventory retains legacy/new/mixed architecture choice and policy-input preparation without automatic network activity. No new scientific or doctrine premise is introduced. Ordinary P1/P2 cover representation, legacy migration and independent selection expectations; this pass adds failure ordering and containment satisfiers, not historical trust reconstruction.

**Coverage / gaps**: Read committed plan, inventory, accepted proposal, current template, install/adopt and stage/apply control paths and security-test owners. No prospective implementation, tasks or suites were executed. This records the required Security plan pass; the author must fold S1 with ordinary P1/P2 before implementation.


## Response to plan review -- Codex (gpt-6.1-sol) -- 2026-10-29

| Finding | Disposition |
|---|---|
| P1 | Accepted; Scope, C2 and reconciliation design specify authority, representation, prior bases, legacy migration and recovery. |
| P2 | Accepted; Verification and the design map name public paths, planned nodes and inputs. |
| S1 | Accepted; C2 and ordering design fix preflight, apply revalidation, refusal scope and containment tests, including security lint. |
