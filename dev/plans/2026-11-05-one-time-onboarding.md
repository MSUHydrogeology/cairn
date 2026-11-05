# Plan: One-time onboarding tasks

**Source proposal**: dev/proposals/archive/2026-11-04-codex-one-time-onboarding.md
**Status**: implementing
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
