# Plan: One-time onboarding tasks

**Source proposal**: dev/proposals/archive/2026-11-04-codex-one-time-onboarding.md
**Status**: archived
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**Author**: Codex Terra (MEDIUM)
**In brief**: Deliver useful module tasks once, then leave the board under project control.

## Source proposal

Decision `2a233544` accepts one-time delivery and only the named loss of
duplicate and stale-task guarantees. Inventory, useful first-use guidance,
board duties and independent installer safeguards remain. Manual copies need
explicit adoption; the existing lock roster, not board text, decides whether
an adoption is new. A valid lock is not an authenticated history.

## Scope

Change `bootstrap/_scaffold/` install and upgrade paths, their owning tests,
board and onboarding templates, and installed bootstrap/module documentation.
Initial preset, explicit and empty selections get one usable task per selected
module, with actual entry point, inputs and expected result; inventory reflects
selection, including removals. First new-module adoption appends only its task
block at EOF, retaining every original board byte as a prefix. No heading search
or tag reconciliation. Already-locked adoption, reinstall, repair and removal
never mutate, backfill or migrate board tasks, including legacy tags; inventory
may update independently. Only explicit `--force` retains existing whole-file
overwrite authority. Preserve root board human text from `af57fc99`.

**Reuse.** Searches at `0d6d2065` for `onboarding-tasks`, `cairn:module`,
`_reconcile_generated_blocks` and `_rendered_onboarding_overlay` found
`install.py`, `upgrade.py`, `slotmerge.py`, CLI, board/preset templates and
their tests, plus the AST fixture. Reuse selection, discovery metadata,
existing validators and the board/inventory/lock transaction, path/token and
cache safeguards; do not build a parallel upgrade engine. Map other spellings,
readers, pins and plan/stage/apply inputs before editing. Live and pristine
clean-lock board baselines must agree without making shared rendering the only
selection oracle.

The independent module universe is the 22 keys of `_MODULE_MAPPINGS` in
`bootstrap/_scaffold/config.py` at `0d6d2065`, not the discovery helper:
reflections, claim-check, incident-trackers, documentation-plan, dual-review,
domain-agents, legacy-agent, dual-language-tests, coordination-tiers,
security-review, issue-capture, model-selection, testing-discipline,
doc-drift-prevention, examples-gallery, content-security, python-security,
portable-security-sweeps, api-access-security, web-hosting-security,
architecture-review and security-verification. At implementation derive the
current complete set again from committed mapping bytes and audit each shipped
task, purpose, entry, inputs and result against installed artifacts; do not
inherit prior figures or infer coverage from the helper under change.

### Documentation / doctrine surface

Update installed `bootstrap/BOOTSTRAP.md` and `templates/modules/README.md`
delivery and the board template, preserving board duties and manual adoption
instructions. Update other mapped adopter-facing readers as needed; route
cross-cutting prescription only to `AGENTS.md` if actually needed under
`docs/DOCUMENTATION_PLAN.md`. No new recurring doctrine or execution authority.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Map committed consumers, pins, module/task inventory and pristine install/lock baseline; implement delivery, independent inventory and adoption validation using existing transaction and guards. | Both plan reviews and author response | Engine, focused tests and adopter documentation. |
| C2 | Run scoped iteration, required real-entry controls and separate mutations; obtain ordinary and Security code reviews, address findings, then run wide Boundary B. | C1 | Reviewed implementation and verification record. |

Maintainer-owned AST/gate trust operations remain the separate board 12 wait;
they are not a plan completion chunk or permission to release. Do not claim
arbitrary crash rollback or turn unrelated conflicts and failed writes into
success.

## Acceptance criteria

**C1.** Real `bootstrap/scaffold.py` installs cover every current mapped module,
preset, explicit and empty rosters, selected versus unselected tasks, usable
installed entry points and accurate inventory. A pristine board and lock
baseline agree independently of the selection oracle. Real adoption tests show
exact EOF prefix and one new task, then no board mutation for repeat, edits,
completion, deletion, removed tags, legacy text, repair, removal or normal
reinstall; force alone retains its existing overwrite behavior. Inventory keeps
its independent updates and conflict checks. Missing, malformed or unusable
locks refuse at the actual adoption entry with passing controls; JSON shape and
later `_check_lockfile_paths` do not suffice. Missing, unwritable or unsafe
board placement fails before lock success or adoption is recorded. Retain
`--init-lock`, token, linked-path, write, cache, stage/apply and unrelated
refusal safeguards; no new registry or historical backfill.

**C2.** Test the real install, `upgrade --adopt-module`, and applicable
plan/stage/apply entry paths, including manual-adoption documentation. Start
with `bootstrap/tests/test_onboarding_seed_roster.py::test_selected_modules_have_usable_tasks`,
`::test_reinstall_preserves_completion_and_refuses_loss`,
`bootstrap/tests/test_upgrade_module_additions.py::test_adoption_reconciles_tasks_and_inventory`,
`::test_already_recorded_adoption_repairs_missing_discovery`,
`::test_staged_module_discovery_refuses_changed_inputs`,
`::test_adoption_refuses_linked_discovery_destinations`, and
`bootstrap/tests/test_module_merge_lockfile.py::test_writer_still_refuses_when_a_merge_target_is_tampered`;
update obsolete expectations without dropping controls. Map and retain the
relevant `test_module_roster.py`, `test_upgrade_module.py`, install, lock and
stage/apply owners. Include `--summary`, `--dry-run` and `--manifest` with
representative profiles and installed-tree checks.

S2/S3: With passing real-entry controls, separately mutate omitted new tasks in
install and adoption, regenerated deleted repeat work, overwritten prior bytes,
linked targets, missing-token refusal and changed staged inputs; each relevant
check must fail. Also independently mutate an unselected task into output and
the clean lock baseline, and check failed writes. Derive each fixture from the
committed candidate and test each module independently; report outcomes and
omissions. Structured operator profile fields select initial modules; embedded
board/profile task prose grants neither selection nor execution authority.
Hostile project text remains unauthenticated. No scientific check applies.

## Scope delta

**Scope delta**: preserved relative to Decision `2a233544`; its explicit
duplicate/stale-task concession is not extended.

## Verification

Boundary A: use `python tools/test_tiers.py for <changed paths>` and run its
iteration list, named controls and applicable claim, link, snippet, content,
neutrality and redundancy gates. Map changed files, callers, readers, pins and
consumers to tests; name missing coverage and remedy it. Use the canonical
Python 3.13 interpreter and committed candidate bytes for fixtures and mutation
copies. Boundary C: independent ordinary and Security code reviews challenge
the implementation with targeted falsification, not a suite. Boundary B: after
review and fixes, run the required wide selection on a clean unchanged final
commit, including mapped iteration and integration/workflow tests, public paths,
standing gates and these acceptance checks. Record SHA/range, interpreter,
clean pre/post state, commands, counts, elapsed time, tokens or unknown,
non-passes, omissions and timing misses in the implementation verification
record. No routine full-tree certification is authorized by this plan.

## Plan review -- Codex Terra (MEDIUM) -- 2026-11-05

Reviewed commit: 4e75521290495179d1c3e637e13e799f25400be5

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: SHIP

**Foundations**

1. **Should this happen as framed?** Yes: the plan retains first-use delivery, board ownership, inventory and refusal safeguards, and tests them at the entry points required by the Decision -- Scope and C1; source Decision `2a233544`.
2. **Best alternative.** Reusing the lock roster, existing discovery transaction and selection machinery is the simplest identified route to the same outcomes; a stdout-only task would lose automatic delivery -- Scope and C1; `bootstrap/_scaffold/upgrade.py::_record_discovery_outputs`.
3. **What would show it wrong?** A real adoption that records success without a task, changes prior board bytes, or regenerates deleted work on repeat would falsify delivery or ownership; the planned separate mutations should make the corresponding checks fail -- C1 and C2.

The current repeat and first-adoption branches both call
`_prepare_module_discovery`, which reconciles board tasks and inventory;
the plan distinguishes their board behavior while retaining inventory checks.
The clean-lock baseline currently shares onboarding rendering with installation;
the independent roster and unselected-task mutation guard against shared error.
The plan correctly leaves the separate Security plan review and both code
reviews outstanding.

**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Coverage**: Committed plan and template, accepted proposal and Decision,
install rendering and lock baseline references, adoption and transaction paths,
and named test locations. **Not covered**: implementation behavior, mutation
results, Security Review, full suite, or release and trust operations; no
implementation checks were rerun.

## Plan review -- Codex Sol (HIGH) -- 2026-11-05

Reviewed commit: 4e75521290495179d1c3e637e13e799f25400be5

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: one nonblocking recommendation
**Verdict**: ACCEPT -- Security plan only; no scope waiver.

**Foundations**

1. **Should this happen as framed?** Yes: EOF delivery and lock-roster repeat handling preserve the Decision's safety obligations while conceding only duplicate/stale tasks -- Decision `2a233544`; C1; `bootstrap/_scaffold/upgrade.py::_cmd_adopt_module`.
2. **Best alternative.** Separate board delivery from inventory reconciliation within the existing guarded transaction, retaining source verification rather than adding a registry or trusting task markers -- `bootstrap/_scaffold/upgrade.py::_prepare_module_discovery`, `_render_review_inventory` and `_commit_lock_and_caches`.
3. **What would show it wrong?** A passing real-entry control whose separate missing-task, prefix-overwrite, token-bypass or stale-stage mutation also passes would invalidate assurance; test valid existing locks alongside unusable-lock refusals -- C1/C2; `bootstrap/tests/test_upgrade_module_additions.py::test_staged_module_discovery_refuses_changed_inputs`.

**SP1 -- Nonblocking: distinguish profile fields from instructions.** C2 says
"Board/profile text cannot authorize selection", but structured operator profile
fields intentionally select initial modules. Close by distinguishing those
fields from embedded task prose, which grants neither selection nor execution
authority -- `bootstrap/_scaffold/cli.py:330`; source S1. This requests wording
precision, not a new permission or reduced safeguard.

Retain adoption's strict absent/blank/curly/angle-placeholder refusals and
lock-over-profile token precedence; the existing token tests distinguish these
cases (`bootstrap/tests/test_upgrade.py:2017`). Adoption dispatch precedes
`_check_lockfile_paths`; JSON-object parsing cannot establish usable state.
Valid migrated locks may lack recoverable bases; do not equate usability with
pristine bytes or authenticated history (`bootstrap/_scaffold/upgrade.py::_cmd_init_lock`).
Board failure must precede recording adoption. The existing transaction stages
outputs and moves the lock last; it does not guarantee arbitrary crash rollback.
C1/C2 retain these independent refusals and prospective real-entry controls.

Judgment formed before reading ordinary review `298ba178`.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed plan/template/Decision, cited prior contracts, selection,
source verification, placeholder, install/adoption/lock/cache and stage/apply
paths, and named test bodies. **Not covered**: future implementation or mutation
results, concurrent path-swap resistance, native-platform behavior, full suite,
release or trust operations. No implementation checks replayed.

## Plan review response -- Codex Terra (MEDIUM) -- 2026-11-05

Ordinary review: no findings. Security SP1: accepted; C2 now distinguishes
structured operator profile fields from embedded task prose. Scope, checks and
lock safeguards remain unchanged.

**Elapsed**: unknown. **Tokens**: unknown.

## Implementation log -- C1 candidate and AST accounting -- Codex Sol (HIGH) -- 2026-11-05

The first eleven-file candidate is preserved at `b8cb4cf5` on local branch
`codex/one-time-onboarding-candidate`; it is not merged into `0.7-dev`.
The working copy is `/private/tmp/cairn-one-time-onboarding`. Initial delivery
uses plain tasks, first adoption appends after the exact existing byte prefix
(including BOM/CRLF/no-final-newline controls), and repeat adoption separates
inventory updates from board ownership. The independently selected module
universe remains 22; all-module fault mutations are not yet complete.

Worker-reported Python 3.13.13 focused runs passed 129 and 28 cases separately;
overlap was not measured, so these are not a unique-node total or Boundary A.
Prose gates passed. The 75-file selector's combined invocation was refused by
the 40-file guard before executing tests; do not call it a completed mapped
run or set a full-suite override. The mapped selection still needs appropriately
bounded batches, including honest dispositions for non-passes.

**Read-only AST accounting, not a correction.** Using the runbook's helpers
on committed base `869c870c` and candidate bytes under Python 3.13.13 found
eight changed engine keys, no missing or new keys: `_cmd_adopt_module`,
`_module_task_blocks`, `_prepare_module_discovery`, `_render_onboarding_slot`,
`_rendered_onboarding_overlay`, `install_onboarding`, CLI `main` and
`write_install_lockfile`. The last includes a docstring-only change.
Against the existing baseline, the base has one changed key and the candidate
six; both have zero missing/duplicate and 143 new classifications. The
known-new manifest retains 105 keys; three bodies are rekeyed:
`_module_task_blocks`, `_prepare_module_discovery` and
`_rendered_onboarding_overlay`. No known-new key was dropped or added.
Two AST attestation tests remain unpassed; no baseline, known-new manifest,
gate record or anchor was changed or waived. These facts do not independently
approve the source or authorize a trust operation.

**Still open:** required per-module/negative-control mutations, mapped checks,
ordinary and Security code reviews and final wide Boundary B. Human trust
operations remain the separate board 12 work, not a new implementation fence.
Status stays `implementing`. **Elapsed**: worker approximately 27 minutes;
parent integration/accounting elapsed unknown. **Tokens**: unknown.

## Implementation verification -- Codex Luna (LOW) -- 2026-11-05

Boundary A measurement only; no review, Boundary B, or completion claim.
Tested candidate `b8cb4cf589c9c49ee1b631b28228cf33ed22bc7a`, base
`869c870c`, range `869c870c..b8cb4cf589c9c49ee1b631b28228cf33ed22bc7a`.
Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python
3.13.13). The candidate working copy and every check clone started and ended
clean at the candidate SHA; the repin-only retry used a temporary local branch
at that same SHA because its fixture requires symbolic `HEAD`. The candidate,
`0.7-dev`, source, trust records, pins, fixtures and shared parent files were
not changed by these checks.

Re-derived the eleven changed paths: `bootstrap/BOOTSTRAP.md`,
`bootstrap/_scaffold/cli.py`, `bootstrap/_scaffold/install.py`,
`bootstrap/_scaffold/upgrade.py`,
`bootstrap/tests/test_install_time_onboarding.py`,
`bootstrap/tests/test_onboarding_seed_roster.py`,
`bootstrap/tests/test_onboarding_slot_substitution.py`,
`bootstrap/tests/test_upgrade_module_additions.py`,
`docs/methodology/onboarding.md`, `templates/core/dev/PLANNING.md`, and
`templates/modules/README.md`. The all-path selector yielded 75 distinct
files (57 engine readers, 4 changed-test files, 39 documentation readers).
The prior combined 75-file pytest command was refused before execution by the
40-file guard. Exact selector groupings were:

```text
python tools/test_tiers.py for bootstrap/_scaffold/cli.py
python tools/test_tiers.py for bootstrap/_scaffold/install.py
python tools/test_tiers.py for bootstrap/_scaffold/upgrade.py
python tools/test_tiers.py for bootstrap/tests/test_install_time_onboarding.py bootstrap/tests/test_onboarding_seed_roster.py bootstrap/tests/test_onboarding_slot_substitution.py bootstrap/tests/test_upgrade_module_additions.py
python tools/test_tiers.py for bootstrap/BOOTSTRAP.md docs/methodology/onboarding.md templates/core/dev/PLANNING.md templates/modules/README.md
```

Each pytest invocation received the complete sorted selector output for its
group, with `--quality-gate-shuffle-seed=0`; each was below the 40-file limit.
The five groups' union is the following complete
75-file selector result (overlap between groups is intentional):

`test_agreement_retired.py`, `test_ast_attest.py`,
`test_board_json_contract.py`, `test_ceremony_review_report.py`,
`test_check_cairn_content.py`, `test_check_release_publication.py`,
`test_cli_module.py`, `test_coordination_broad_intent.py`,
`test_core_dev_folders.py`, `test_default_security_stance.py`,
`test_doc_governance.py`, `test_documentation_plan_module.py`,
`test_drift_surfacing.py`, `test_engine_copy_fallback_contained.py`,
`test_finalize_retired_living_state.py`, `test_fork_advisory.py`,
`test_gauge.py`, `test_git_interpreter_binding_portable.py`,
`test_hardening.py`, `test_install_module.py`,
`test_install_report_slots.py`, `test_install_time_onboarding.py`,
`test_intents_tool.py`, `test_link_check_exclusions.py`,
`test_lockfile_provenance.py`, `test_model_selection_stub.py`,
`test_module_merge.py`, `test_module_merge_lockfile.py`,
`test_module_roster.py`, `test_next_session_local_note.py`,
`test_notice_install.py`, `test_onboarding_seed_roster.py`,
`test_onboarding_slot_substitution.py`, `test_oracle.py`,
`test_oracle_activation.py`, `test_portable_security_sweeps.py`,
`test_presets.py`, `test_profile_grammar.py`, `test_prune_tools.py`,
`test_quality_gate_redundancy.py`, `test_quickstart_sequence.py`,
`test_reanchor.py`, `test_reference_scripts.py`, `test_repin.py`,
`test_replacement_tools.py`, `test_review_stance_in_shipped_files.py`,
`test_review_sweep_ships.py`, `test_scaffold.py`,
`test_scaffold_substrate.py`, `test_scientific_check_guidance_ships.py`,
`test_scope_reduction_trap.py`, `test_security_capability_install.py`,
`test_security_finding_confidentiality.py`, `test_security_leaf.py`,
`test_security_lint.py`, `test_security_stack.py`,
`test_security_verification.py`, `test_session_routines.py`,
`test_session_writes_contained.py`, `test_skills_onboarding.py`,
`test_skills_upgrade.py`, `test_slotmerge_leaf.py`, `test_test_tiers.py`,
`test_upgrade.py`, `test_upgrade_added_slots.py`,
`test_upgrade_edit_check_runs_no_project_programs.py`,
`test_upgrade_lockfile_path_containment.py`, `test_upgrade_module.py`,
`test_upgrade_module_additions.py`,
`test_upgrade_refuses_hostile_project_data.py`,
`test_upgrade_removes_retired_files.py`, `test_upgrade_side_door_parity.py`,
`test_verify_integrity.py`, `test_verify_stems.py`,
`test_web_hosting_security.py`.

Commands were `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest
--quality-gate-shuffle-seed=0 <sorted paths printed by the corresponding
selector command>` in separate disposable clones, one invocation per group
above. Pytest reported collected items and outcomes below; counts are per
invocation and are not unique-node totals. Times are pytest-reported elapsed
time.

| Group | Files / collected | Result | Elapsed |
|---|---:|---|---:|
| CLI owner | 14 / 498 | 490 passed, 8 skipped | 104.14s |
| Install owner | 35 / 1,862 | 1,850 passed, 9 skipped, 3 failed | 477.09s |
| Upgrade owner | 38 / 2,391 | 2,390 passed, 1 skipped | 480.71s |
| Changed test owners | 4 / 174 | 174 passed | 45.80s |
| Documentation owners | 39 / 2,465 | 2,461 passed, 1 skipped, 3 failed | 267.18s |
| Repin harness correction | 1 node | 1 passed | 35.01s |

The initial repin failure was harness-only: the detached disposable source made
`test_baseline_preparation_builds_exact_package_after_reader_binding` fail at
`git symbolic-ref HEAD`. Re-running only that node on a temporary branch at the
same SHA passed. The two remaining install-group failures are
`test_ast_gate_passes_over_the_full_scaffold_module_set` and
`test_committed_baseline_accounted_for_across_the_engine_package`; candidate
AST drift is already accounted for above and neither pin nor fixture was
changed. The three documentation-group failures are
`test_passive_session_start_pointer_seeded_once` for `solo-greenfield`,
`high-rigor-legacy`, and `collaborative-team`: each observed zero
`try-session-start-skill` pointers where the assertion expects one. These
mapped checks remain unmet; no source correction or waiver is made here.

Iteration timing target was 30 seconds: all five main groups exceeded it.
Per-file durations were not measured, so files exceeding the separate 10-second
target and the corresponding consolidation entries remain unknown. The check
results do not cover the per-module and negative-control mutations, ordinary
or Security code review, or final wide Boundary B; there are no mutation
outcomes to claim. The earlier prose-gate result remains as recorded in the C1
log. No full-tree certification or `CAIRN_FULL_SUITE` run was performed.
**Elapsed**: pytest-reported group times above; verification session elapsed
unknown. **Tokens**: unknown.

## Expected AST mismatch disposition -- 2026-11-05

The Maintainer clarified: “But the assertions are EXPECTED to fail. That
cannot be part of a plan, that it can't close without a test passing that
SHOULD fail.” The Maintainer further directed: “And the baseline happens at
release, and does not hold up plan closure”. Accordingly, a verified expected
AST-attestation mismatch caused by reviewed, planned engine changes remains
visibly unpassed for the separately owned release baseline operation, but by
itself does not hold plan archive. These directions do not declare the
mismatch or underlying code reviewed, passing, authorized or safe. Missing
source review, unexplained drift, new defects, and every other actionable
implementation check remain open. No release is authorized; no baseline or
anchor edit, waiver, or human-ceremony completion fence is created here.
**Elapsed**: unknown. **Tokens**: unknown.

## Implementation checkpoint -- pointer assertion correction -- 2026-11-05

Private candidate commit `c13e7bc2` updates only
`bootstrap/tests/test_skills_onboarding.py`: the three parameterized assertions
now check the usable `/session-start` task and its exact session-start command,
not the intentionally omitted source seed ID. From a clean archive of that
candidate, the three profile cases plus the passive-source control passed (4
passed). Separate disposable missing-pointer and duplicate-pointer mutations
each failed all three profile cases (3 + 3), at the `/session-start` count as
intended. The candidate SHA is recorded as supplied; no parent-ref update is
claimed.

The two expected AST attestations remain visibly unpassed for the separately
owned release baseline operation; they do not by themselves hold plan archive.
No baseline or trust edit, release authorization, review, or overall completion
is claimed. Remaining implementation work includes acceptance mutations,
ordinary and Security code reviews, and final wide Boundary B. **Elapsed**:
unknown. **Tokens**: unknown.

## Implementation checkpoint -- per-module mutations -- Codex Terra (gpt-6.1-terra, LOW) -- 2026-11-05

Candidate `c13e7bc218681acb0ea84f0ff2c2f69d5f3534a7`, Python
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13). A complete
Git-backed detached clone was clean and contained the tracked
`templates/modules/team-gated/_intent/` files. The earlier report that the
adoption test was skipped for a missing fixture was a scratch-input error;
the named test was also renamed. On the committed candidate the real-entry
`test_selected_modules_have_usable_tasks` and both cases of
`test_adoption_appends_task_preserving_exact_prefix_and_updates_inventory`
passed: 3 passed. The following controls also passed, 8 cases including
parameterizations: `test_empty_selection_has_no_module_tasks`,
`test_unselected_modules_have_no_tasks_or_inventory_rows`,
`test_repeat_adoption_does_not_restore_deleted_task_but_updates_inventory`,
`test_staged_module_discovery_refuses_changed_inputs`,
`test_adoption_refuses_linked_discovery_destinations`, and
`test_adopt_module_records_api_access_security_into_an_existing_lockfile`.
Their files are respectively `test_onboarding_seed_roster.py`,
`test_upgrade_module_additions.py`, and `test_security_capability_install.py`
under `bootstrap/tests/`. These are controls, not a suite.

An AST read of the committed `_MODULE_MAPPINGS` keys, independent of task
rendering, yielded: reflections, claim-check, incident-trackers,
documentation-plan, dual-review, domain-agents, legacy-agent,
dual-language-tests, coordination-tiers, security-review, issue-capture,
model-selection, testing-discipline, doc-drift-prevention, examples-gallery,
content-security, python-security, portable-security-sweeps,
api-access-security, web-hosting-security, architecture-review and
security-verification. In a separate clean clone per key, filtering that key
from `_module_task_blocks` made the selected-module install test fail at its
assertion for that exact missing task: 22 of 22. This tests the explicit
all-module installation path, not every preset or task's substantive quality.

In another clone, suppressing only the first-adoption board update for
`dual-review` made both prefix/task cases fail at the appended-task assertion.
Separate mutations injecting unselected `dual-review`, regenerating deleted
`dual-review` repeat work, and replacing the existing board prefix made their
respective controls fail (1, 1 and 2 cases). Suppressing the first-adoption
board update for `api-access-security` left its existing file-and-lock adoption
test green (1 passed): that test does not assert the task. No claim is made
that it detects this fault. The smallest useful remedy is a real-entry,
per-module first-adoption test that independently asserts each new task and
the original byte prefix, then separate omission mutations for all 22 keys.

Commands: the controls were run with `python3.13 -m pytest -q -p
no:cacheprovider` and the named nodes above; the temporary repeatable mutation
driver is `/private/tmp/cairn-onboarding-mutate-terra.py`, invoked with
`python3.13 /private/tmp/cairn-onboarding-mutate-terra.py` and again with
`negative`. It cloned the candidate afresh per mutation and ran the relevant
single test node with `--tb=short`; the API result is the surviving fault
above. Clone-plus-test times summed to approximately 27.0 and 4.5 seconds,
respectively; control pytest times were 0.44 and 1.23 seconds. Elapsed session
time and tokens: unknown.

Still open: adoption task mutations for the other 21 keys, independent clean
lock-baseline mutation, linked-target, missing-token, staged-input and failed
write mutations, remaining accepted checks, both code reviews and final wide
Boundary B. Passing linked/staged controls above are not mutation evidence.
No suite override, source/test commit, pin, anchor, release or trust operation
was made. The separately recorded expected AST mismatch disposition is
unchanged; unexpected drift and unmet implementation checks remain work.

## Implementation checkpoint -- first-adoption coverage -- Codex Terra (gpt-6.1-terra, LOW) -- 2026-11-05

Private branch `codex/one-time-onboarding-candidate` now ends at
`419731a5d18f51d52c0ad582560c96bbe1bd7ec7`, based on `c13e7bc2` via
test-only commits `5b072806` and `419731a5`. Only
`bootstrap/tests/test_upgrade_module_additions.py` changed. Its new
parameterized real-entry test uses the independently enumerated 22 names in
the preceding checkpoint and checks their equality to the committed mapping.
Each case installs an empty roster with a valid Python package token, confirms
the module is not locked, then adopts it. It asserts the complete original
board byte prefix (BOM, CRLF, human text and no final newline), one appended
module task, and nonempty purpose, action, result and entry-point text. The
previous prefix and inventory assertions remain unchanged.

On a complete clean detached clone of `419731a5`, Python
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) ran
`-m pytest -q -p no:cacheprovider` with
`bootstrap/tests/test_upgrade_module_additions.py::test_each_first_adoption_appends_its_task_after_original_board`,
`bootstrap/tests/test_upgrade_module_additions.py::test_adoption_appends_task_preserving_exact_prefix_and_updates_inventory`,
and `bootstrap/tests/test_onboarding_seed_roster.py::test_selected_modules_have_usable_tasks`:
25 passed in 1.25 seconds.

The temporary `/private/tmp/cairn-adoption-mutations-terra.py` independently
reads the 22 keys from committed config and makes a fresh clean clone of
`419731a5` for each. It suppresses the board update only for that named
first adoption, then runs the matching parameterized node. Each of the 22
failed at its missing-task assertion, including `api-access-security`; none
failed merely at setup or collection. Clone-plus-test elapsed times summed to
approximately 19.2 seconds. A separate fresh-copy prefix-overwrite mutation,
`/private/tmp/cairn-adoption-prefix-terra.py`, made the `dual-review` case
fail at `result.startswith(original)` (1 failed in 0.22 seconds). These
results close the prior checkpoint's per-module first-adoption omission gap;
they do not prove the task instructions are scientifically or operationally
correct, or substitute for the other accepted controls.

Independent clean-lock-baseline, linked-target, missing-token, staged-input
and failed-write mutations, any other unmet checks, both code reviews and
final wide Boundary B remain open. No full suite, source engine or trust edit,
merge, push or release occurred. Verified expected AST mismatches remain
unpassed until the separate release baseline operation and alone do not hold
plan archive; unexpected drift and other unmet checks remain work. Session
elapsed and tokens: unknown.

## Implementation checkpoint -- C2 negative controls -- Codex Terra (gpt-6.1-terra, LOW) -- 2026-11-05

Tested private candidate `706c9c0991a3a1162e869fb924bb4594b27d126e`,
parent `419731a5`. Its only new tracked change, in
`bootstrap/tests/test_upgrade_module_additions.py`, extends the existing
linked-discovery test to targets inside the project and asserts that refusal
precedes creation of `dev/modules/dual-review.md`. The old outside-target,
victim, lock and symlink assertions remain. This closes a demonstrated test
gap: on `419731a5`, both outside-link cases still passed after removing the
discovery preflight, because earlier containment refused them.

On a complete clean clone of `706c9c09`, Python
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) ran
`-m pytest -q -p no:cacheprovider` against these nodes:

- `bootstrap/tests/test_upgrade_module_additions.py::test_adoption_refuses_linked_discovery_destinations`
  and `::test_staged_module_discovery_refuses_changed_inputs`;
- `bootstrap/tests/test_upgrade.py::TestAdoptModule::test_adopt_required_token_absent_entirely_refuses_closed`,
  `::test_adopt_required_token_curly_placeholder_refuses_closed`,
  `::test_adopt_required_token_angle_placeholder_refuses_closed`, and
  `::test_adopt_refusal_names_a_remedy_that_works`;
- `bootstrap/tests/test_upgrade_module_additions.py::test_each_first_adoption_appends_its_task_after_original_board[python-security]`.

Those controls passed: 11 cases in 1.80 seconds, none skipped. Separate
success controls `test_pre_split_apply_records_package_in_lockfile`,
`test_each_first_adoption_appends_its_task_after_original_board[dual-review]`
(both in `test_upgrade_module_additions.py`), and
`TestAdoptModule::test_adopt_required_token_seeded_from_profile` (in
`test_upgrade.py`) passed: 3 in 0.65 seconds.

The temporary driver `/private/tmp/cairn-c2-negatives-terra.py`, run with the
same interpreter, made a fresh clean clone of `706c9c09` for each fault and
ran the named owning nodes with `-m pytest -q -p no:cacheprovider --tb=short
--show-capture=no`. Results, none skipped:

- Removing the discovery path preflight: the two new inside-link cases failed
  because a module document was written before refusal; both outside-link
  cases passed because the separate earlier containment check refused them.
- Changing containment refusal to success: both outside-link cases failed at
  the required refusal status; both inside-link cases still passed through
  the separate discovery preflight. This does not prove a write-through.
- Disabling missing-token detection: absent, curly-placeholder and
  angle-placeholder adoption cases each failed at the refusal status.
- Disabling the staged discovery-input comparison: both changed-board and
  changed-inventory cases failed when apply returned success.

These targeted faults do not cover blank-token variants, every link type or
parent-directory link, all write-failure modes, or independent clean-lock
baseline mutation. Those and other unmet accepted checks, both code reviews
and final wide Boundary B remain open. No full suite, engine or trust edit,
merge, push, release, board or changelog edit occurred. Verified expected AST
mismatches remain unpassed for the separate release baseline operation and
alone do not hold plan archive. Session elapsed and tokens: unknown.

## Implementation checkpoint -- remaining C2 controls -- Codex Terra (gpt-6.1-terra, LOW) -- 2026-11-05

Tested private candidate `8c7370c97209aa3268a7f72f149995d083c49c42`,
parent `706c9c09`. Its test-only commit extends the existing
`test_upgrade.py`, `test_onboarding_seed_roster.py` and
`test_upgrade_module_additions.py` homes: blank required tokens; refusal to
create a clean lock from a changed board; an in-project linked inventory
parent; hard-linked board and inventory victims; and an injected failed board
stage at the real adoption entry. No candidate engine, pin or trust file changed.

On a complete clean detached clone, Python
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) ran
`-m pytest -q -p no:cacheprovider` with these nodes and parameterizations:

- `bootstrap/tests/test_upgrade.py::TestAdoptModule::test_adopt_required_token_blank_refuses_closed`,
  plus the absent, curly-placeholder and angle-placeholder refusal nodes;
- `bootstrap/tests/test_upgrade.py::TestLockfile::test_round_trip` and
  `::test_base_cache_is_raw_mergeable_only`;
- `bootstrap/tests/test_onboarding_seed_roster.py::test_diverged_planning_board_does_not_become_clean_lock_baseline`
  and `::test_live_install_writes_a_clean_lockfile_under_agent_team_single`;
- `bootstrap/tests/test_upgrade_module_additions.py::test_adoption_refuses_linked_inventory_parent_before_writes`,
  `::test_adoption_replaces_hardlinked_discovery_without_changing_victim`,
  `::test_adoption_failed_board_stage_does_not_record_success`,
  `::test_adoption_refuses_linked_discovery_destinations`,
  `::test_pre_split_apply_records_package_in_lockfile`, and
  `::test_each_first_adoption_appends_its_task_after_original_board[python-security]`.

Result: 20 passed in 1.71 seconds, none skipped. The failure-injection case
raises a synthetic `PermissionError` while staging the board and verifies
the board and lock bytes remain unchanged and adoption is not recorded; it
does not claim no other file was written or exercise native permission bits.

`/private/tmp/cairn-onboarding-remaining-mutations-terra.py` used that
interpreter to make a fresh clean clone of `8c7370c9` per fault, then ran its
named node with `-m pytest -q -p no:cacheprovider --tb=short
--show-capture=no`. No mutated run skipped a test:

- Accepting blank tokens failed all three empty, space and tab cases.
- Ignoring a changed board in the clean-install comparison failed the
  divergent-board test because a lock was written.
- Corrupting only the expected rendered board baseline failed the clean-lock
  positive control; corrupting only its raw cached baseline failed the raw
  template comparison. Each fault was in a different copy.
- Disabling parent-link refusal failed the linked-parent adoption test.
- Replacing hard-linked discovery files in place failed both victim checks.
- Swallowing the injected board-stage failure failed the expected-exception
  check. These failures are mutation evidence, not product failures.

The runs cover the specific link locations and synthetic failure above, not
every link topology, platform permission mode or arbitrary crash. Other
unmet accepted checks, ordinary and Security code reviews, and final wide
Boundary B remain open. No full suite, merge, push, board/changelog change,
release or trust operation occurred. Verified expected AST mismatches remain
unpassed until the separate release baseline operation and alone do not hold
plan archive. Session elapsed and tokens: unknown.

## Code review -- Codex Terra -- 2026-11-05

**Foundations**

1. **Should this happen as framed?** Not yet: adoption accepts a malformed lock hash and records a module, contrary to C1's unusable-lock refusal -- `_cmd_adopt_module`, finding below.
2. **Best alternative.** Keep the one-time append and existing transaction, but validate the lock fields needed for a usable baseline before either adoption branch -- `_prepare_module_discovery`, `_commit_lock_and_caches`.
3. **What would show it wrong?** A real adoption with a corrupted baseline must refuse without recording delivery, while a valid lock succeeds; the corrupted-hash probe instead succeeded -- finding below.

Reviewed SHA: `8c7370c97209aa3268a7f72f149995d083c49c42`; merge base `869c870c958ff817915f7ecc2fa1768d4e0ae37c`.

**Verdict: REVISE.** **Blocking -- unusable lock accepted.** In a clean candidate copy, a real install followed by replacing the first lock record's `hash` with `broken` and invoking `upgrade --adopt-module dual-review` returned 0 and recorded `dual-review`, retaining the invalid hash. `_cmd_adopt_module` checks only that `hash` is a nonempty string; the existing unusable-lock test removes `dst` and does not cover malformed baseline hashes. This fails C1's refusal and retained lock/cache safeguards. Close with an appropriate usable-baseline validation and real-entry negative and valid controls; assess other required baseline fields too.

**Bounding: WIDER RUN REQUIRED.** Add the missing lock-baseline behavior to the mapped checks; final wide Boundary B remains required after review and fixes.

**Evidence.** In a clean candidate clone, Python 3.12.9 ran targeted unusable-lock, inventory-conflict, board-stage failure, changed staged-input and repeat-adoption nodes: 7 passed in 1.34 seconds. The malformed-hash probe above used the real install and adoption entry. The implementation record supplies per-module, token, link, board-prefix and independent mutation evidence; synthetic board-stage failure does not prove arbitrary crash rollback. The expected AST mismatch remains unpassed pending the separate release baseline operation and alone does not block archive.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Candidate delta, accepted proposal, plan and review template; install/adopt, inventory, token, containment and transaction paths; selected tests and implementation evidence. **Not covered**: exhaustive corrupt-lock variants, all link topologies, native permission failures, arbitrary crashes, Security Review, final Boundary B or full suite.

## Security review -- Codex Sol -- 2026-11-05

**Model**: gpt-6.1-sol (high). **Tier**: Security. **Findings**: one blocking defect already found by ordinary review; one nonblocking limit.

Reviewed commit: `8c7370c97209aa3268a7f72f149995d083c49c42` (candidate; not merged). Target: install/adopt read and write paths and their focused tests. Prior finding: ordinary code review at `e2d97a7e`.

**Foundations**

1. **Should this happen as framed?** Not yet: malformed lock data can pass adoption and be committed again, violating C1's usable-lock refusal -- real-entry probe below.
2. **Best alternative.** Retain the one-time append and existing transaction; validate required lock baselines before either adoption branch, without adding a board registry -- `_cmd_adopt_module`, `_commit_lock_and_caches`.
3. **What would show it wrong?** A damaged lock being accepted, or a selected module missing its task, falsifies the claimed safeguards -- probes below.

**Verdict: REVISE.** **SR-C1 (blocking, independently confirmed):** A clean real install with `reflections` succeeded. Changing the first lock record's `hash` to `broken`, then invoking real `upgrade --adopt-module dual-review`, returned 0, recorded `dual-review`, and retained the invalid hash under Python 3.13.13. This confirms the ordinary review's blocker; require a real-entry damaged-baseline refusal and valid-lock control before archive.

**SR-C2 (nonblocking):** Removing the onboarding slot from the source board template made a fresh install warn yet return 0 with a lock and no selected task. The existing `test_selected_modules_have_usable_tasks` failed on that same source mutation, so the required test detects it; the reviewed template retains the slot. A future runtime refusal would be stronger, but this is not a second unmet criterion on these bytes.

**Coverage:** Clean candidate archive, real scaffold baseline and two separate mutations; nine targeted tests passed on unmodified bytes under Python 3.13.13. **Not covered:** every corrupt-lock field, native permission and link topology, arbitrary crash rollback, full plan/stage/apply workflow, wide Boundary B, full suite, release or trust operation. **Elapsed**: unknown. **Tokens**: unknown.

## Implementation verification -- Codex Luna (gpt-6.1-terra, LOW) -- 2026-11-05

Review-fix candidate `9b37e3e24f659b546510daee1e6bbbab640ea6da` on
`codex/one-time-onboarding-candidate`, based on reviewed `8c7370c9`, addresses
the ordinary review `e2d97a7e` and Security review `59405941` finding. Commit
`92a3f65c` validates record `hash` and present `base_hash` using the existing
SHA-256 format predicate, validates applicable `base_cache`/`base_hash`
pairing before both adoption branches, and retains explicitly migrated
unrecoverable records and legacy verbatim records without `base_hash`.
`9b37e3e2` supplies a consistent cache and digest in the existing tracked-file
advisory fixture, retaining its advisory/count assertions. This is structural
lock validation, not authentication of history or a fresh read of every cache;
the existing upgrade path handles invalid saved ancestor bytes as review-only.

On a complete clean detached clone of `9b37e3e2`, Python
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) ran `-m pytest -q
-p no:cacheprovider` on the new damaged-baseline, migrated, legacy, unusable
lock, all-module adoption and repeat-adoption nodes in
`bootstrap/tests/test_upgrade_module_additions.py`, plus
`bootstrap/tests/test_upgrade.py::TestAdoptModule::test_adopt_advisory_and_count_when_destination_already_tracked`:
41 passed in 3.46 seconds. The damaged tests cover seven malformed or missing
field configurations on both first and repeat adoption, preserving lock,
board and inventory bytes. The migrated control uses the real `--init-lock`.
The temporary `/private/tmp/cairn-adoption-lock-faults-luna.py` used fresh
clean clones of `9b37e3e2` to remove each of five checks independently:
malformed `hash`, malformed `base_hash`, missing `base_hash`, missing
`base_cache`, and invalid `base_cache`. Each fault made both corresponding
real-entry cases fail at refusal (10 expected failures, none skipped).

Boundary A mapping: `python tools/test_tiers.py for` on
`bootstrap/_scaffold/upgrade.py`, `bootstrap/tests/test_upgrade_module_additions.py`
and `bootstrap/tests/test_upgrade.py` selects 40 files. Before the fixture-only
commit, the 38-file selection for the first two paths ran on clean `92a3f65c`
with `python3.13 -m pytest -q -p no:cacheprovider --durations=0 <selector
paths>`: 2,401 passed, 1 skipped, 36 failed in 523.28 seconds. The skip's
reason was not captured and is not a pass. Of the failures, 35 could not bind
local test sockets; exactly those nodes were retried with local socket access
on clean `9b37e3e2` and passed (35 in 24.46 seconds). The remaining failure
was the incomplete advisory fixture, corrected by `9b37e3e2` and included in
the 41-case rerun above. The two files newly selected by the fixture path,
`test_gate_reanchor.py` and `test_replacement_tools.py`, passed on `9b37e3e2`
(37 in 23.33 seconds). The full 40-file selection was not rerun as one batch
on `9b37e3e2`; no final Boundary B or full suite is claimed.

The 523.28-second iteration exceeded the 30-second diagnostic. Approximate
per-file sums of pytest setup/call/teardown durations over 10 seconds, slowest
first: `test_reanchor.py` 97.05s; `test_upgrade.py` 78.77s;
`test_upgrade_edit_check_runs_no_project_programs.py` 50.79s;
`test_upgrade_module_additions.py` 50.54s; `test_security_stack.py` 38.00s;
`test_upgrade_removes_retired_files.py` 25.62s; `test_gate_reanchor.py` 23.16s
(separate run); `test_upgrade_refuses_hostile_project_data.py` 20.94s;
`test_upgrade_added_slots.py` 18.73s; `test_upgrade_lockfile_path_containment.py`
17.52s; `test_oracle.py` 16.90s; `test_portable_security_sweeps.py` 16.39s;
`test_intents_tool.py` 13.42s; `test_security_verification.py` 12.43s; and
`test_reference_scripts.py` 10.03s. These observations need the parent-owned
test-consolidation list at its serialization point.

Status remains `revising-code`: the changed code requires the reviewers'
targeted follow-up and final wide Boundary B. One skipped mapped case remains
uncharacterized. No trust pin, anchor, baseline, merge, push or release was
changed. Expected AST mismatches remain unpassed for the separate release
baseline operation and alone do not hold archive; new engine bytes still need
the applicable accounting. Session elapsed and tokens: unknown.

## Targeted Code review follow-up -- Codex Terra -- 2026-11-05

Reviewed fix: `8c7370c97209aa3268a7f72f149995d083c49c42..9b37e3e24f659b546510daee1e6bbbab640ea6da`. This is the required same-reviewer look at the original ordinary finding, not a second full code-review pass. The fix changes only adoption lock validation and affected tests/fixture. No new defect was found in that delta; the malformed-baseline finding is closed by the validation change at `92a3f65c`, as tested on `9b37e3e2`.

The guard now rejects malformed or absent `hash`, malformed `base_hash`, and invalid/missing applicable `base_cache`/`base_hash` pairs before either first or repeat adoption. The damaged-baseline cases assert unchanged lock, board and inventory bytes. Real-entry controls retain `--init-lock` migrated unrecoverable records, legacy verbatim records without `base_hash`, and the tracked-destination advisory. On a clean detached copy of `9b37e3e2`, `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) ran the six named affected test nodes in `test_upgrade_module_additions.py` and `test_upgrade.py`: 20 passed in 5.15 seconds, none skipped. The copy remained clean. This targeted check does not authenticate lock history or verify every cache's bytes.

The author's mapped 40-file selection was not rerun here; its one skipped case remains uncharacterized, and its final-commit wide Boundary B and new-engine AST accounting remain owed. Expected reviewed AST mismatch remains unpassed pending the separate release baseline operation. Security Review of the fix is separate. No full suite, trust operation, merge or push was performed. **Elapsed**: unknown. **Tokens**: unknown.

## Targeted Security review follow-up -- Codex Sol -- 2026-11-05

**Model**: gpt-6.1-sol (high). **Tier**: Security. Reviewed fix: `8c7370c9..9b37e3e2` on the candidate branch. This is a targeted follow-up to SR-C1 at `59405941`, not a new full pass.

**Verdict: SR-C1 closed on these bytes.** `_cmd_adopt_module` now checks required digest syntax and applicable cache/digest pairs before either adoption branch. In a clean archive of `9b37e3e2`, canonical Python 3.13.13 ran the real-entry damaged-baseline cases plus migrated and legacy controls: 16 passed, none skipped. The damaged cases cover first and repeat adoption and assert that refusal leaves lock, board and inventory bytes unchanged. The malformed `hash` shape that previously returned success now returns refusal. The fix does not authenticate lock history or prove every cache's content; those are not claims of this structural check.

**Coverage:** Reviewed the source and test delta and ran the 16 named controls on committed candidate bytes. **Not covered:** the full mapped selection, the one uncharacterized mapped skip, native permission/link topologies, arbitrary crash rollback, final wide Boundary B, new-engine AST accounting, full suite, release or trust operations. Those remaining implementation obligations are not waived. **Elapsed**: unknown. **Tokens**: unknown.

## Implementation verification -- Codex gpt-6-sol -- 2026-11-05

**Candidate checkpoint, not final Boundary B.** On clean committed candidate
`9b37e3e24f659b546510daee1e6bbbab640ea6da` (range
`869c870c..9b37e3e2`), the 76-file `tools/test_tiers.py for` selection was
run in two 38-file batches under `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(3.13.13), with local loopback access. The copy was clean before and after;
the second batch used a local branch at the same SHA because a ceremony test
requires a symbolic HEAD. Commands: `python3.13 tools/test_tiers.py for
<13 changed paths>`; for each ordered half, `python3.13 -m pytest -q -rs -p
no:cacheprovider --tb=short --durations=20 <38 selector paths>`. Results:
1,194 passed, 9 skipped, 2 AST-attestation failures in 132.55s; then 2,963
passed, 1 unexpected failure in 583.79s. **Candidate B: NONPASS** (4,157
passed, 9 skipped, 3 failed; 716.34s across completed batches). The unexpected
failure was `test_upgrade_edit_check_runs_no_project_programs.py::test_apply_goes_on_with_no_git_and_stops_when_git_does_not_answer`: the test's expected
Git `--version` log was empty. A parent-reported fresh-clone rerun of that
exact node passed; this does not clear the batch failure. The 30s iteration,
10s-per-file and 3m integration timing targets were exceeded; file-level sums
for all 76 files were not measured. No full suite or certification was run.

**AST accounting (read-only):** The runbook helper `_ast_attest.digest_module`
under the same interpreter compared all ten engine modules at pre-plan
`869c870c` and candidate `9b37e3e2`. Baseline and known-new fixture bytes are
identical (169 and 105 keys). Both trees have zero missing/duplicate baseline
keys and the same 143 new classifications. Pre-plan already differs from the
older pinned baseline at `Assign:_MODULE_MAPPINGS`:
`3f868e8353a0a498 -> 9c83dfd22009e964`; candidate does not change it.
The eight candidate-changed named bodies, shown as pre-plan -> candidate, are:

| AST key | Pre-plan digest | Candidate digest |
| --- | --- | --- |
| `FunctionDef:_cmd_adopt_module` | `0d20a0a8e2f5f4c3` | `490e4479aa7a813d` |
| `FunctionDef:_module_task_blocks` | `8aee3b0a99cbc17e` | `5ae02067b5d23a8d` |
| `FunctionDef:_prepare_module_discovery` | `7cf8a49b692cac89` | `b3e6831c357551fb` |
| `FunctionDef:_render_onboarding_slot` | `71a9c13997ec8898` | `474e6dd2def0341a` |
| `FunctionDef:_rendered_onboarding_overlay` | `b8ef5f39cadbf79d` | `ec0bc82f0a3b324a` |
| `FunctionDef:install_onboarding` | `e9564a51f22f6390` | `287250ab14359c7c` |
| `FunctionDef:main` | `9d09abee8dc5c707` | `9b3f41cfafdf118c` |
| `FunctionDef:write_install_lockfile` | `31cb06bccc8c3f62` | `82aceb51e58f8778` |

Five of those are changed baselined bodies; three are the already-named
known-new bodies whose unchanged manifest still pins the pre-plan digests.
There are no added/dropped named keys or unaccounted new named bodies. One
structural import key was added and one dropped (`Import:5b4d4def050d`,
`Import:b2423c08e882`); imports are per-module necessities exempted by the
helper. The two AST tests remain **unpassed** pending the separate Maintainer
baseline operation; this read-only accounting does not repin or approve them.

**Skip characterization:** All nine first-batch skips require Windows on this
macOS host. Eight are
`test_git_interpreter_binding_portable.py::test_windows_reparse_points_refuse_binding_access`
for `source` and `shipped`, each with `dot-git`, `admin`,
`binding-directory` and `binding-leaf` parameters (reason: `requires native
Windows junctions`). The ninth is
`test_intents_tool.py::test_windows_drive_case_normalization_for_pointer_chain`
(reason: `Windows drive normalization requires Windows`). These nodes were
collected by name and matched to the batch's `-rs` summary; they were not run
on Windows. **Final unchanged integration-commit Boundary B: NOT RUN.** No
merge, source edit, repin, push or trust/release operation occurred. **Elapsed**:
candidate completed batches 716.34s; AST/skip accounting time not separately
measured. **Tokens**: unknown.

## Maintainer exception and verification -- Codex gpt-6.1-terra -- 2026-11-05

**Maintainer chat, 2026-11-05:** "Go ahead and waive tests that are failing, and proceed". The Maintainer was told the onboarding wide run had intermittent Git failures under heavy load. The follow-up limits this exception to the two cases below in the last onboarding wide run only. It does not waive security controls, future failures, other required checks, or claim either test passed.

**Candidate wide checkpoint:** Clean unchanged candidate `9b37e3e24f659b546510daee1e6bbbab640ea6da`, range `869c870c..9b37e3e2`, in a disposable clone on a local branch at that SHA, clean before and after. Interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13; loopback was permitted. The 76-file `tools/test_tiers.py for` selection for the 13 changed paths ran in two serial 38-file batches with `python3.13 -m pytest -q -rs -p no:cacheprovider --tb=short --durations=20 <38 selected paths>`. Batch 1: 1,157 passed, nine skipped, two AST failures in 187.45s. Batch 2: 2,962 passed, two failures in 941.48s. Total: 4,119 passed, nine skipped, four failed; 1,128.93s pytest time. This is a non-pass, not a passing Boundary B.

**Named exception, UNPASSED:** `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_failure_in_a_later_group_is_cannot_tell[index-hang]` and `::test_a_failure_in_a_later_group_is_cannot_tell[comparison-non-zero exit]`. Both failed in batch 2 because the expected counter file was missing. A subsequent targeted invocation of those two exact nodes passed two in 2.03s; it does not change the batch result. Earlier, the owner file passed 82 in 71.08s. On pre-plan `869c870c`, the two nodes and the previously reported `test_apply_goes_on_with_no_git_and_stops_when_git_does_not_answer` passed three in 5.73s. The latter previously failed in isolation with an empty stand-in log, then passed on retry; the prior checkpoint also recorded its batch failure and targeted pass. The fixture and Git launcher are unchanged in the candidate range; a timing-sensitive fixture is plausible, but cause is not proven. No security control is waived.

The two AST checks remain **UNPASSED**, with the existing read-only accounting above and the separate Maintainer baseline operation still owed. All nine skips require native Windows and were not executed there; whether native evidence is independently required remains to be determined against the applicable contract. Ordinary and Security code-review follow-ups above cover the candidate fix. A clean final integration commit containing the candidate and this separately scribed record has not been checked; this record does not authorize merge, archive, release, repin or trust changes.

The four changed Markdown files passed `scripts/check_cairn.py` and `scripts/sync_doc_snippets.py --check`; `scripts/quality_gate.py --sub neutrality --sub redundancy` reported zero failures. The integration timing target was exceeded; complete per-file duration sums were not measured. No full suite or `CAIRN_FULL_SUITE` run was performed. One malformed initial batch command was interrupted during collection with no tests run. **Elapsed:** batch figures above; total session unknown. **Tokens:** unknown.

## Focused integration code review -- Codex GPT-5 (MEDIUM) -- 2026-11-05

**Reviewed commit:** `b1fb9eae0d7f006cd4f1ddf7ac3627ddc7236692`; range `30a227809e5270cce8b985286bd5f0effa91af42..b1fb9eae0d7f006cd4f1ddf7ac3627ddc7236692`. **Verdict:** no new blocking finding in this focused pass. **Bounding:** final wide Boundary B remains required and has not passed.

**Foundations**

1. **Should this happen as framed?** Yes, subject to outstanding checks: install seeds selected tasks and adoption appends without replacing prior board bytes; the targeted real-entry controls below passed.
2. **Best alternative.** Retain the existing transaction and independent inventory update; a separate task registry adds maintenance without an identified need -- `_prepare_module_discovery` and the plan's Scope.
3. **What would show it wrong?** A real install missing a selected task, or adoption changing existing board bytes, would falsify delivery or ownership; the selected-module and exact-prefix controls below are forward tests.

**Evidence.** Inspected the integration diff, current board and module templates, relocated-test changes, board utility scope, and the exception record above. On the clean candidate, `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) ran `pytest -q -p no:cacheprovider` on `test_onboarding_seed_roster.py::test_selected_modules_have_usable_tasks`, `test_upgrade_module_additions.py::test_adoption_appends_task_preserving_exact_prefix_and_updates_inventory`, and `test_skills_onboarding.py`: 7 passed in 0.49s; the tree remained clean. An initial invocation used the plan's now-renamed `test_adoption_reconciles_tasks_and_inventory` and collected no tests; the successor passed in the corrected invocation. Use its current name in the final selection.

The exception record quotes the Maintainer and confines the named exception to two unpassed cases in the prior wide run, not later failures or security controls. It does not establish a passing final integration check. The AST checks remain unpassed pending the separate Maintainer baseline operation.

**Elapsed:** unknown. **Tokens:** unknown.

**Coverage:** Focused integration interactions and the exception record. **Not covered:** a fresh Security Review, exhaustive review of the newer base or all relocated tests, native Windows behavior, load-sensitive failures, final Boundary B, full suite, or trust operations.

## Implementation verification -- Codex gpt-6.1-terra (LOW) -- 2026-11-05

**Boundary B mode:** wide. **Tested commit:** `072495248f4e2065a60dd59ebfda17bb665cbc51`; reviewed integration range `30a227809e5270cce8b985286bd5f0effa91af42..072495248f4e2065a60dd59ebfda17bb665cbc51`. Canonical interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13. A disposable clone on a local branch started and ended clean at that SHA; local loopback was permitted. No benchmark was launched by this task; a pre-run process check found no active pytest or benchmark, but does not prove exclusive machine use throughout.

The selector `python3.13 tools/test_tiers.py for <14 paths from git diff --name-only 30a22780..07249524>` returned 76 files, including the changed install, adoption and lock consumers, owning families and mapped workflow/integration paths. In two serial sorted halves of 38, `env -u CAIRN_FULL_SUITE python3.13 -m pytest -q -rs -p no:cacheprovider --tb=short --durations=20 --junitxml=<temporary report> <38 selector paths>` produced:

| Batch | Exit | Outcomes | Pytest elapsed | Tokens |
|---|---:|---|---:|---|
| 1 | 1 | 1,054 passed, 9 skipped, 2 failed | 98.83s | unknown |
| 2 | 0 | 3,184 passed | 497.36s | unknown |

Total: 4,238 passed, 9 skipped, 2 failed; 596.19s summed pytest time. End-to-end elapsed is unknown. This is not an all-pass result. The two failures are `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package` and `::test_ast_gate_passes_over_the_full_scaffold_module_set`: **UNPASSED** pending the separate Maintainer baseline operation. Their reported nine changed or mismatched symbols match the earlier read-only accounting above; engine and AST fixture bytes are unchanged from `9b37e3e2`. No trust record was changed. Eight skipped native Windows binding junction/reparse cases and one Windows drive-normalization case were not executed here; historical native passes were at older commits, not this SHA.

The two earlier excepted `test_a_failure_in_a_later_group_is_cannot_tell[index-hang]` and `[comparison-non-zero exit]` cases and `test_apply_goes_on_with_no_git_and_stops_when_git_does_not_answer` each passed in this run. The prior exception applies only to the earlier run and was not applied here. Selected-module, both exact-prefix adoption variants, and tampered merge-target controls passed. The selection includes the plan's summary, dry-run and manifest consumers; prior separate mutation evidence is recorded above and was not rerun as part of this boundary.

Standing gates, all under Python 3.13.13: individual `scripts/claim_check.py` calls for the four changed Markdown files and this plan, `scripts/check_cairn.py` on the five, and `scripts/sync_doc_snippets.py --check` on the five passed. `scripts/quality_gate.py --sub neutrality --sub redundancy` had zero failures (43 and 2 informational findings respectively). External links and native Windows were not run. No full suite, certification, merge, repin, release or baseline operation occurred. The 3min integration diagnostic target was exceeded; iteration was not separately timed.

JUnit testcase totals including setup and teardown, summed by file above 10s, slowest first: `test_repin.py` 155.89s; `test_reanchor.py` 56.12s; `test_upgrade.py` 34.80s; `test_upgrade_module_additions.py` 33.61s; `test_upgrade_edit_check_runs_no_project_programs.py` 28.43s; `test_security_stack.py` 26.52s; `test_upgrade_removes_retired_files.py` 24.50s; `test_portable_security_sweeps.py` 21.64s; `test_ceremony_review_report.py` 20.57s; `test_security_finding_confidentiality.py` 20.30s; `test_gate_reanchor.py` 20.15s; `test_upgrade_refuses_hostile_project_data.py` 19.98s; `test_web_hosting_security.py` 14.77s; `test_oracle.py` 14.48s; `test_intents_tool.py` 13.78s. These belong to the parent-owned test-consolidation list at its serialization point. Temporary JUnit reports: `/private/tmp/cairn-onboarding-07249524-b1.xml` and `/private/tmp/cairn-onboarding-07249524-b2.xml`.

## Native Windows follow-up -- Rawls (gpt-6-luna, LOW) -- 2026-11-05

Rawls reported to the coordinator that the nine cases skipped on macOS above passed on Windows 11 ARM64: **9 passed, 0 skipped in 3.32s**, using `C:\ProgramData\miniconda3\python.exe` (Python 3.13.17; pytest 9.2.0). The agent reported transferring a `git archive` of tested commit `072495248f4e2065a60dd59ebfda17bb665cbc51` into `C:\cairn-validation-07249524` and running:

```text
python.exe -m pytest -q -rs -p no:cacheprovider --tb=short bootstrap/tests/test_git_interpreter_binding_portable.py::test_windows_reparse_points_refuse_binding_access bootstrap/tests/test_intents_tool.py::test_windows_drive_case_normalization_for_pointer_chain
```

The first selector expands to the eight combinations of `source` and `shipped` with `dot-git`, `admin`, `binding-directory` and `binding-leaf`; the second is the single drive-case normalization node. The first invocation used paths without `bootstrap/tests/`, exited 4 and ran no tests; the corrected invocation produced the result above. The report does not provide an archive digest or post-run byte comparison, so it is not independent proof of every extracted byte or a clean Git checkout. These native results supplement, not alter, the recorded Mac skips and are not results for a later integration SHA. The two AST checks remain unpassed; no full Windows suite, trust operation or release is claimed. **Elapsed:** pytest 3.32s; session 98s as reported by the coordination record. **Tokens:** unknown.


## Promotion evidence status -- Codex Luna (gpt-6-luna, LOW) -- 2026-11-05

The preceding review and verification records are carried from the private onboarding candidate and retain their original authorship and tested commits. In particular, the Boundary B record for `072495248f4e2065a60dd59ebfda17bb665cbc51` is candidate evidence against its recorded range; it is not the final Boundary B for the current shared `0.7-dev` integration. Final wide Boundary B on the clean integrated commit remains owed. The separately named AST mismatches remain unpassed for the release baseline operation and alone do not block plan archive. No source review, trust operation, release or archive is authorized by this note.

**Elapsed**: unknown. **Tokens**: unknown.

## Implementation verification -- Codex (coordination) -- 2026-11-05 -- joined final check

**Boundary B: wide.** Tested clean committed integration
`88679232404f5e5ec72aab8f5f9799710f10d483`, scoped range
`787df691..88679232` for this plan's 13 implementation paths, fast-goodnight's
nine paths and the serialized board/changelog updates. Both plans' independent
reviews and required follow-ups precede this check. The 12 non-overlap
onboarding paths match the reviewed promotion; the combined adoption-test file
retains the reviewed collision fixtures and onboarding controls.

Canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13), disposable
clone on a local branch, clean before and after every batch; loopback allowed.
`python tools/test_tiers.py for --range 787df691..88679232 <24 scoped paths>`
selected 86 files, omitting 15 governing-only readers under its existing guard.
Add the accepted reviewed-set pin node and `test_profiles_smoke.py`: 88 distinct
target files. The initial combined invocation was refused by the 40-file guard:
exit 4, no tests executed. Maintainer chat authorized **"Run the exact selection
in batches (Recommended)"**. No full-suite override was set.

Run command in each ordered 30/30/28-target batch:
`python -m pytest -q -rs -p no:cacheprovider --tb=short --durations=20
--junitxml=<temporary report> <batch targets>`. Outcomes:

| Batch | Exit | Passed | Skipped | Failed | Pytest seconds |
|---|---:|---:|---:|---:|---:|
| 1 | 1 | 866 | 9 | 2 | 79.16 |
| 2 | 0 | 2,255 | 0 | 0 | 352.18 |
| 3 | 0 | 1,338 | 0 | 0 | 187.66 |

Total **4,459 passed, nine skipped, two failed**, 619.00 pytest seconds;
621.02 seconds wall. XML has 4,470 distinct classname/name pairs, no errors.
The two failures are the already-accounted engine AST checks in
`test_ast_attest.py`: `test_committed_baseline_accounted_for_across_the_engine_package`
and `test_ast_gate_passes_over_the_full_scaffold_module_set`. They remain
**UNPASSED** pending the separate release baseline; Cairn's current expected-AST
rule permits archive without treating them as passed. No new functional failure
appeared and no earlier Git-test exception was used.

The nine Mac skips are the eight native Windows binding reparse parameters
and the drive-case normalization case already named above. Prior native evidence
remains at `07249524`, not a fresh Windows run at this SHA; 21 relevant case,
reader/twin and intent-helper files were byte-identical between those commits.
This is not whole-tree or release certification.

`check_cairn.py` and `sync_doc_snippets.py --check` passed on the twelve changed
Markdown surfaces; neutrality and redundancy reported zero failures. External
links were not probed. The integration timing target was missed; measured
files over ten seconds go to the existing suite-consolidation record, not a
new evidence folder. Raw temporary reports are not durable implementation.

Accepted delivery, safeguards, reviews and change verification are complete;
no additional functional follow-up is deferred. Baseline/signing/release remain
the existing separate board waits. **Status: ready-to-archive.** No full suite,
repin, anchor change, push or release. Elapsed: 621.02 seconds for the batches;
total coordination unknown. Tokens: unknown.
