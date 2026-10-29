# Plan: Module discovery and first use

**Source proposal**: dev/proposals/archive/2026-10-29-codex-module-discovery-activation.md
**Status**: awaiting-code-review
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

## Implementation verification -- Codex -- 2026-10-29

**Implementation verified at eee603a6.**

**Boundary B mode**: wide
**Certified by**: pending

**Tested range**: `a6c151f1..eee603a6` (module discovery implementation and focused compatibility/coverage updates).
**Interpreter**: Python 3.13.13.
**Clean pre/post state**: detached worktree `/private/tmp/cairn-module-discovery-boundary-b-final3` at `eee603a6`; clean before and after the recorded commands.

**Mapped families and consumers**: `python -m pytest bootstrap/tests/test_scaffold.py bootstrap/tests/test_presets.py bootstrap/tests/test_onboarding_seed_roster.py bootstrap/tests/test_module_roster.py bootstrap/tests/test_module_merge_lockfile.py bootstrap/tests/test_upgrade_module.py bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_notice_install.py bootstrap/tests/test_install_time_onboarding.py bootstrap/tests/test_onboarding_slot_substitution.py bootstrap/tests/test_skills_onboarding.py bootstrap/tests/test_security_lint.py bootstrap/tests/test_security_verification.py bootstrap/tests/test_security_stack.py bootstrap/tests/test_security_capability_install.py bootstrap/tests/test_intents_tool.py` — 812 passed in 63.79 seconds. This covers install, exact/empty selection, adoption, repeat adoption, lock rendering, staged apply, containment, consumer tests and the security verification paths. `test_security_lint.py` ran 11 tests; none skipped.

**Public paths and gates**: `scripts/check_cairn.py` passed (188 Markdown files); `scripts/claim_check.py bootstrap/BOOTSTRAP.md` and `scripts/claim_check.py templates/modules/README.md` passed; `scripts/link_check.py` passed (188 Markdown files); `scripts/sync_doc_snippets.py --check` passed (436 documents); `scripts/quality_gate.py --sub neutrality` passed (0 failures, 43 informational findings). No full-suite run was made. Public `--summary`, `--dry-run` and `--manifest` smoke checks and representative preset, exact, empty and add/remove installs were run during Boundary A; the manifest reported 87 data rows.

**Mutation ledger** (four separate plain-file copies extracted from `eee603a6`; each mutant changed one behavior; each named test failed on the mutant):

| Mutation | Deliberate break | Check and outcome |
|---|---|---|
| Selected task removed | Explicit-roster renderer returns no tasks. | `test_selected_modules_have_usable_tasks` — killed (1 failed). |
| Unselected task added | Renderer uses the whole discovery catalog, ignoring the selected roster. | `test_unselected_modules_have_no_tasks_or_inventory_rows` — killed (1 failed). |
| Preserved work discarded | Removal conflict guard is bypassed for completed or edited entries. | `test_reinstall_preserves_completion_and_refuses_loss` — killed (1 failed). |
| Baseline changed | Inventory cache `base_hash` is replaced with an incorrect digest. | `test_selected_modules_have_usable_tasks` — killed (1 failed). |

**Unmutated control**: on the clean `eee603a6` worktree, the four corresponding control nodes (`test_selected_modules_have_usable_tasks`, `test_unselected_modules_have_no_tasks_or_inventory_rows`, `test_reinstall_preserves_completion_and_refuses_loss`, and `test_live_install_writes_a_lockfile_when_a_module_merge_lands`) passed 4/4. The full mapped run above then passed 812/812 on the same commit.

**Omissions**: no scientific check applies. The whole-tree certifying pair was not run; certification remains pending. External links were not probed by the local link gate. No behavior outside the mapped families and named public paths is claimed covered.


## Code review -- Codex (gpt-6.1-sol) -- 2026-10-29

**Reviewed commit**: f51b84b1 (implementation eee603a6)
**Obligation**: Internal
**Findings**: raised
**Bounding**: WIDER RUN REQUIRED

**Foundations**:

1. **Does it do what it claims?** Not yet: an unknown marked task crashes instead of reporting an actionable reconciliation conflict; the stable verification also omits its required public-path checks -- `bootstrap/_scaffold/install.py:1243`, verification above.
2. **Best alternative.** Treat an unrecognized task identity as an ambiguous edited entry and refuse with recovery guidance, retaining the existing shared reconciliation path -- `bootstrap/_scaffold/install.py:1265`.
3. **What would show it wrong?** A marked, completed task with an unknown identity breaks the reconciliation path; see the falsification ledger below.

**P1 -- Unknown marked task produces an uncaught exception.** The task renderer indexes the first result for any parsed identity, but the renderer returns an empty list for an identity absent from the current catalog. A retired module or edited marker therefore raises `IndexError` before the conflict handler can provide manual recovery. Guard unknown identities and report a `ModuleDiscoveryConflict`, preserving the existing artifacts; exercise the public adoption path.

**P2 -- Complete the final-commit public-path verification.** The plan requires the public summary, dry-run, manifest and representative install paths at Boundary B on the clean final commit. The record reports these only at Boundary A. Run and record those prescribed checks at the final implementation commit; the mapped test families do not replace the explicit public-path criterion.

**Falsification ledger** (plain-file archive of eee603a6, Python 3.13.13):

| Challenge | Result |
|---|---|
| Reconcile a completed task marked `retired-module`, absent from the catalog, with an empty roster | `IndexError` at `install.py:1243`; expected a reported conflict. |
| `test_upgrade_module_additions.py` in the archive | 21 passed, then `test_module_additions_under_explicit_to_are_hard_blocked` failed because the archive has no Git repository for its `HEAD` check; this is an environment limitation, not an implementation finding. |

**Evidence and sweep**: Reviewed the committed implementation diff, reconciliation path, acceptance criteria and Boundary B record. Existing checks cover selected and unselected entries, preservation and lock baselines; the archive probe challenges an identity outside the current catalog. The verification record identifies Python, counts, clean state and non-pass disposition; certification remains pending.

**Coverage / gaps**: This is the ordinary code review only; the separate Security Review remains open. I did not rerun the broad suite, inspect every module task, or independently exercise all public paths. The missing final-commit public checks require a new implementation verification record.


## Response to code review -- Codex (gpt-6.1-sol) -- 2026-10-29

P1 accepted: unknown marked identities now stop reconciliation with instructions to save and remove the entry manually, and a public adoption regression checks that planning, inventory and lock bytes remain unchanged. P2 accepted: the final candidate was checked through the required command-line paths below.

## Implementation verification -- Codex (gpt-6.1-sol) -- 2026-10-29

**Candidate tested at d83b0faf; verification remains open for manual-copy execution.**

**Boundary B mode**: wide
**Certified by**: pending

**Tested range**: `a6c151f1..d83b0faf`; Python 3.13.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`). An independent local clone at `d83b0faf` was clean before and after. A detached worktree could not be created under the filesystem permissions.

**Mapped families and consumers**: repeated the 17 named test families in the preceding verification, including security lint: 812 passed and one failed in 64.57 seconds. The failure was `test_security_verification.py::TestNoCapabilityContract::test_a_socket_opening_child_is_excluded_by_admission_not_blocked_at_runtime`, whose loopback bind was denied in the restricted environment; the same node passed (1 passed in 0.05 seconds) with loopback access permitted. No skips. The new public adoption regression passed in the mapped run.

**Public paths**: `bootstrap/scaffold.py` with `--summary`, `--dry-run`, and a real temporary install each succeeded for preset `solo-greenfield`, exact `reflections` plus `dual-review`, empty roster, and `high-rigor-legacy` with `examples-gallery` added and `security-review` removed (12 successful invocations). `--manifest` succeeded with 87 data rows. The mapped adoption tests cover automated later adoption; manual-copy execution was not repeated in this run.

**Gates**: `scripts/check_cairn.py` passed (188 Markdown files), claim checks passed for `bootstrap/BOOTSTRAP.md` and `templates/modules/README.md`, `scripts/link_check.py` passed (188 files), `scripts/sync_doc_snippets.py --check` passed (436 documents), and `scripts/quality_gate.py --sub neutrality` passed (0 failures, 43 informational findings). External links were not probed.

**Mutation ledger**: four separate copies of the candidate, each with one deliberate break, killed by the corresponding test in `bootstrap/tests/test_onboarding_seed_roster.py`: remove selected tasks (`test_selected_modules_have_usable_tasks`); add unselected tasks (`test_unselected_modules_have_no_tasks_or_inventory_rows`); bypass preservation refusal (`test_reinstall_preserves_completion_and_refuses_loss`); corrupt the baseline hash (`test_selected_modules_have_usable_tasks`). The unmutated controls passed in the mapped run.

**Omissions**: no scientific check applies; whole-tree certification remains pending. Manual-copy execution remains an unmet final-commit check; no coverage outside the named mappings and public paths is claimed.


## Implementation verification addendum -- Codex (gpt-6.1-sol) -- 2026-10-29

**Implementation verified at d83b0faf.** The outstanding manual-copy check passed on the same clean candidate clone under Python 3.13.13. In a temporary project installed with `solo-greenfield`, copied `templates/modules/team-gated/dual-review.md` to `dev/modules/dual-review.md`, then ran the documented `bootstrap/scaffold.py upgrade --target <project> --cairn-root <candidate> --adopt-module dual-review`. The copied bytes remained intact; inventory, task and lock named the module. Repeating adoption left all three artifacts unchanged. An added completed unknown marked task caused exit 2 with manual guidance and preserved all three artifacts; saving and removing that block followed by retry succeeded. The candidate clone remained clean after the check. This completes the manual-copy omission stated above; certification remains pending.


## Code review -- Codex Security (gpt-6.1-sol) -- 2026-10-29

**Reviewed commit**: d83b0faf9e466aab924455a4e3f279b7fe072f8e
**Target**: module-discovery implementation and repair; verification through 1afdf46b.
**Prior findings**: ordinary P1/P2 answered; Security obligation previously open.
**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Bounding**: WIDER RUN REQUIRED — add public repeat-install coverage for a populated legacy placeholder slot, then record final-commit evidence.

**Foundations**:

1. **Does it do what it claims?** Adoption refuses unknown identities safely, but repeated installation can silently erase completed unrelated work, violating C2 — `bootstrap/_scaffold/install.py:1451` and ledger below.
2. **Best alternative.** Recognize only an exact unchanged empty-slot placeholder; send any populated slot through conservative reconciliation, preserving surrounding text — `bootstrap/_scaffold/install.py:1248` and `bootstrap/_scaffold/install.py:1451`.
3. **What would show it wrong?** Adding completed work beside the retained empty-slot hint before later module selection demonstrates loss through the public installer — falsification ledger below.

**S1 — A placeholder substring authorizes destructive replacement.** The unmarked-slot branch treats any occurrence of `(Empty at adoption` as proof that the entire slot is disposable. An adopter can retain that hint while adding a completed personal task. Selecting a module on a repeat install then replaces the slot wholesale, silently deleting that task. This violates preservation of unrelated text and completed work and bypasses the conservative legacy path. Recommend matching the complete pristine placeholder only; otherwise reconcile while retaining unrelated content, or refuse with recovery instructions. Add a public repeat-install regression that starts empty, adds completed work beside the hint, selects a module and asserts preservation or refusal with unchanged planning, inventory and lock. This restores accepted scope.

**Falsification ledger** — independent local clone detached at d83b0faf, Python 3.13.13; detached-worktree creation was refused by filesystem permissions:

| Challenge | Result |
|---|---|
| Public installer: initial profile uses `modules: []`; insert `(Empty at adoption)` plus `* [x] Preserve my completed research task` into the onboarding slot; repeat with a block-list selecting dual-review | Both calls exit 0; completed personal task disappears. Helper-level control reproduces the same loss. |
| Unknown marked completed task during public adoption | Existing targeted regression passes; guidance and all three byte snapshots preserved. |
| Linked discovery destinations during adoption | Existing targeted parametrized checks pass. |
| Change discovery input after stage | Existing targeted parametrized checks pass; apply refuses. |
| Already-recorded adoption repairs missing discovery | Existing targeted check passes. |

The last four rows ran as four explicit pytest nodes in `bootstrap/tests/test_upgrade_module_additions.py`: 6 passed in 0.75 seconds, no skips. These challenge containment, stale staging, repeat adoption and the repair independently of the author's broad command. No mutation was needed to expose S1.

**Evidence and sweep**: Read committed reconciliation, adoption preparation/commit ordering, apply input checks, plan and prior verification. The new identity guard precedes catalog indexing. Selection remains lock/profile authority and no task executes. The latest record supplies manual-copy evidence and dispositions its loopback restriction; certification remains pending. The shared renderer remains preferable to another installer. S1 names the missing preservation case and its satisfier.

**Coverage / gaps**: This pass covers the Security obligation only. Did not run the full suite, old-anchor verification, every module task, concurrent filesystem races or arbitrary crash recovery; those are not claimed certified. Existing checks passing do not settle S1. Independent ordinary review remains separate.


## Response to Security code review -- Codex (gpt-6.1-sol) -- 2026-10-29

S1 accepted. Only the complete unchanged placeholder or an empty slot may be replaced. A placeholder containing edits or other work is ambiguous and now refuses with instructions to save and reconcile it; the public repeat-install regression checks planning, inventory and lock bytes remain unchanged. Conservative refusal preserves the accepted legacy reconciliation scope.

## Implementation verification -- Codex (gpt-6.1-sol) -- 2026-10-29

**Implementation verified at 8ca130c6.**

**Boundary B mode**: wide
**Certified by**: pending

**Tested range**: `a6c151f1..8ca130c6`; Python 3.13.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`). An independent local clone at the candidate commit was clean before and after. The 17 mapped test families named in the previous verification, including security lint and the new public repeat-install regression, passed 814 tests in 62.14 seconds with loopback access allowed; no skips.

**Public paths and gates**: `--summary`, `--dry-run`, and temporary installation passed for preset, exact, empty and add/remove profiles (12 invocations); `--manifest` passed with 87 data rows. Manual copy of dual-review, explicit adoption and repeat adoption passed, preserving copied bytes and checking inventory, task and lock. `check_cairn.py` and `link_check.py` passed on 186 Markdown files, claim checks passed for the two changed shipped documents, `sync_doc_snippets.py --check` passed on 436 documents, and the neutrality gate passed with 0 failures and 43 informational findings. External links were not probed.

**Mutation ledger**: in four separate candidate copies, the mapped checks killed each break: removed selected tasks (`test_selected_modules_have_usable_tasks`), added unselected tasks (`test_unselected_modules_have_no_tasks_or_inventory_rows`), bypassed completed-work refusal (`test_reinstall_preserves_completion_and_refuses_loss`), and corrupted the baseline hash (`test_selected_modules_have_usable_tasks`). Their unmutated controls passed in the mapped run.

**Omissions**: no scientific check applies. Whole-tree certification remains pending; no coverage outside the named mappings and public paths is claimed.


## Code review -- Codex Security (gpt-6.1-sol) -- 2026-10-29

**Reviewed commit**: 8ca130c68381a5c399357f41694d762ae3cd5a2f
**Target**: S1 repair and implementation evidence at 54783c0f.
**Prior findings**: Security S1.
**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none; S1 cleared.
**Bounding**: ACCEPTED for the module-discovery Security obligation.

**Foundations**:

1. **Does it do what it claims?** The repaired branch refuses populated placeholders before generated writes, preserving all three artifacts; pristine placeholders still initialize successfully — `bootstrap/_scaffold/install.py:1451` and public probes below.
2. **Best alternative.** Exact pristine-placeholder recognition with conservative manual reconciliation is the smallest safe repair; it retains the shared reconciliation path and accepted preservation contract — `bootstrap/_scaffold/install.py:1451`.
3. **What would show it wrong?** Silent loss on the previously breaking input, or refusal of the pristine control, would defeat the repair — falsification ledger below.

**Falsification ledger** — fresh independent local clone detached at 8ca130c6; Python 3.13.13. Each public probe created its own temporary project and called the installer through `bootstrap.scaffold.main`:

| Challenge | Result |
|---|---|
| Install explicit empty roster; retain the shipped placeholder and append a completed personal research task; repeat selecting dual-review | Initial exit 0, repeat exit 2, manual reconciliation guidance present; planning, inventory and lock byte snapshots all unchanged. |
| Same initial install and selection change with the untouched shipped placeholder | Both calls exit 0; selected dual-review task appears. |

**Evidence and sweep**: Read the committed repair and its public regression alongside the appended response and final-candidate verification. The exact comparison removes the substring-based deletion authority; the refusal occurs before inventory or planning writes. The latest record reports 814 mapped passes under Python 3.13.13, including security lint and the new regression, with no skips, and records public and manual-copy paths. Those author measurements were inspected rather than rerun. No new scope or mechanism is introduced; no additional defects were found in this repair.

**Coverage / gaps**: This pass clears the previously open Security S1 obligation only, relying on the preceding Security pass for unchanged paths. No broad suite, old-anchor check, concurrent filesystem-race probe or full module-task audit was run. Whole-tree certification remains pending and ordinary review remains separate.

## Code review -- Codex (gpt-6.1-sol) -- 2026-10-29

**Reviewed commit**: 54783c0f (implementation 8ca130c6)
**Obligation**: Internal revision review
**Findings**: no new defects found
**Bounding**: ACCEPTED

**Foundations**:

1. **Does it do what it claims?** The revision refuses a populated placeholder before replacing it, and unknown task identities now produce actionable conflicts; the final verification records the mapped families and public paths at the candidate -- `bootstrap/_scaffold/install.py:1265`, `bootstrap/_scaffold/install.py:1452`, verification above.
2. **Best alternative.** Retaining the existing reconciliation path with conservative refusal is simpler than inferring whether edited placeholder content is disposable -- `bootstrap/_scaffold/install.py:1452`.
3. **What would show it wrong?** A repeat install that discards work or an unknown task that escapes conflict handling would break the claim -- falsification ledger below.

**Falsification ledger** (fresh archive of `8ca130c6`, Python 3.13.13):

| Challenge | Result |
|---|---|
| Run the onboarding roster family, including populated-placeholder preservation and completed-work removal | 18 passed in 0.81 seconds. |
| Reconcile a completed task marked `retired-module` against an empty roster | Raised `ModuleDiscoveryConflict` with instructions to save and remove the marked entry; no uncaught `IndexError`. |

**Evidence and sweep**: Read the revision, prior findings and response, C2, and the final verification record. The record covers the previously missing final-commit public paths and manual-copy adoption, the named owning families and security lint; certification is pending. The independent probe challenges the prior unknown-identity failure; the roster family exercises the changed placeholder branch. No broader run was made.

**Coverage / gaps**: This ordinary revision pass addresses the changed code and prior ordinary findings. It does not re-review unchanged implementation, exercise every module task, external links, concurrent races or crash recovery; the separate Security Review addresses its own obligation.
