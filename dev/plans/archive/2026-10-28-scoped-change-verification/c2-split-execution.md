# C2 split execution evidence

**Plan**: [`../2026-10-28-scoped-change-verification.md`](../2026-10-28-scoped-change-verification.md)
**Tested SHA**: `69b8bc7e4f86fd6c669fd765a1ffe7951e9e10d9`
**Base SHA**: `2ed8ddabc80c985ebc93171c7e628a7ec070459f`
**Copy**: detached worktree `/private/tmp/cairn-scope-worktree-69b8bc7e`; clean before and after; trust ref `refs/cairn/gate-anchor` present at `443de20f81169fabe36c4ca3cc620206f7850254`.
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — Python 3.13.13.
**Seed/markers**: `--quality-gate-shuffle-seed=0` preserved on every pytest selection; no `-m` marker selector was present in the original selection.

## Selection

The source-derived reader search was:

```sh
rg -l -e 'Boundary B' -e 'certifying run' -e 'FULL RUN REQUIRED' -e 'full suite' -e 'AGENTS\.md' -e 'dev/plans/_template' bootstrap/tests -g '*.py'
```

It found 48 modules. The five exact mapped guard nodes in `test_broad_run_guard.py` were exercised separately, so the other 47 modules were selected for the file-threshold split. The sorted 47-module selection was:

1. `test_agreement_retired.py`
2. `test_board_json_contract.py`
3. `test_certifying_run_rule.py`
4. `test_check_cairn_content.py`
5. `test_claim_check_module.py`
6. `test_comprehension_floor.py`
7. `test_core_dev_folders.py`
8. `test_doc_drift_tools.py`
9. `test_documentation_plan_module.py`
10. `test_fork_advisory.py`
11. `test_gate_manifest.py`
12. `test_gate_preflight.py`
13. `test_generated_output_scan.py`
14. `test_hardening.py`
15. `test_install_report_slots.py`
16. `test_install_time_onboarding.py`
17. `test_link_check_exclusions.py`
18. `test_lockfile_module.py`
19. `test_loop_fidelity_gate.py`
20. `test_model_tier_rule_ships.py`
21. `test_module_merge_lockfile.py`
22. `test_next_session_local_note.py`
23. `test_notice_install.py`
24. `test_oracle.py`
25. `test_quality_gate_neutrality.py`
26. `test_quickstart_sequence.py`
27. `test_replacement_tools.py`
28. `test_review_and_verification_rules_ship.py`
29. `test_review_stance_in_shipped_files.py`
30. `test_review_sweep_ships.py`
31. `test_scaffold.py`
32. `test_scaffold_substrate.py`
33. `test_scientific_check_guidance_ships.py`
34. `test_scope_reduction_trap.py`
35. `test_security_leaf.py`
36. `test_security_stack.py`
37. `test_security_verification.py`
38. `test_slotmerge_leaf.py`
39. `test_stewardship_rules_ship.py`
40. `test_upgrade.py`
41. `test_upgrade_edit_check_runs_no_project_programs.py`
42. `test_upgrade_lockfile_path_containment.py`
43. `test_upgrade_module_additions.py`
44. `test_upgrade_refuses_hostile_project_data.py`
45. `test_verification_boundaries.py`
46. `test_verify_integrity.py`
47. `test_writing_rules_ship.py`

## Commands and outcomes

Collection used all 47 explicit paths above, each prefixed `bootstrap/tests/`, in this invocation:

```sh
python3.13 -m pytest -q --collect-only \
  bootstrap/tests/test_agreement_retired.py bootstrap/tests/test_board_json_contract.py bootstrap/tests/test_certifying_run_rule.py bootstrap/tests/test_check_cairn_content.py bootstrap/tests/test_claim_check_module.py bootstrap/tests/test_comprehension_floor.py bootstrap/tests/test_core_dev_folders.py bootstrap/tests/test_doc_drift_tools.py bootstrap/tests/test_documentation_plan_module.py bootstrap/tests/test_fork_advisory.py \
  bootstrap/tests/test_gate_manifest.py bootstrap/tests/test_gate_preflight.py bootstrap/tests/test_generated_output_scan.py bootstrap/tests/test_hardening.py bootstrap/tests/test_install_report_slots.py bootstrap/tests/test_install_time_onboarding.py bootstrap/tests/test_link_check_exclusions.py bootstrap/tests/test_lockfile_module.py bootstrap/tests/test_loop_fidelity_gate.py bootstrap/tests/test_model_tier_rule_ships.py \
  bootstrap/tests/test_module_merge_lockfile.py bootstrap/tests/test_next_session_local_note.py bootstrap/tests/test_notice_install.py bootstrap/tests/test_oracle.py bootstrap/tests/test_quality_gate_neutrality.py bootstrap/tests/test_quickstart_sequence.py bootstrap/tests/test_replacement_tools.py bootstrap/tests/test_review_and_verification_rules_ship.py bootstrap/tests/test_review_stance_in_shipped_files.py bootstrap/tests/test_review_sweep_ships.py \
  bootstrap/tests/test_scaffold.py bootstrap/tests/test_scaffold_substrate.py bootstrap/tests/test_scientific_check_guidance_ships.py bootstrap/tests/test_scope_reduction_trap.py bootstrap/tests/test_security_leaf.py bootstrap/tests/test_security_stack.py bootstrap/tests/test_security_verification.py bootstrap/tests/test_slotmerge_leaf.py bootstrap/tests/test_stewardship_rules_ship.py bootstrap/tests/test_upgrade.py \
  bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_upgrade_refuses_hostile_project_data.py bootstrap/tests/test_verification_boundaries.py bootstrap/tests/test_verify_integrity.py bootstrap/tests/test_writing_rules_ship.py \
  --quality-gate-shuffle-seed=0
```

Outcome: 2,700 node IDs collected in 1.33s. The guard permits collection because it executes no test bodies.

Split 1 used the first 40 explicit paths above, each prefixed `bootstrap/tests/`; its command was the same invocation as collection with `-vv` and without `--collect-only`, omitting files 41–47.

Outcome: exit 1, 2,129 passed and 3 failed in 234.85s. Each failure was an environment denial while tests created a disposable `ssh-agent` socket or bound loopback; the failures were not contract assertion failures. The exact three nodes passed in the separate elevated local rerun below.

Split 2 used files 41–47 above, each prefixed `bootstrap/tests/`, in this invocation:

```sh
python3.13 -m pytest -vv \
  bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py \
  bootstrap/tests/test_upgrade_lockfile_path_containment.py \
  bootstrap/tests/test_upgrade_module_additions.py \
  bootstrap/tests/test_upgrade_refuses_hostile_project_data.py \
  bootstrap/tests/test_verification_boundaries.py \
  bootstrap/tests/test_verify_integrity.py \
  bootstrap/tests/test_writing_rules_ship.py \
  --quality-gate-shuffle-seed=0
```

Outcome: exit 0, 568 passed in 71.31s.

The mapped guard nodes ran separately:

```sh
python3.13 -m pytest -q \
  bootstrap/tests/test_broad_run_guard.py::test_a_run_over_the_file_threshold_is_refused_regardless_of_selector \
  bootstrap/tests/test_broad_run_guard.py::test_the_file_threshold_boundary_is_exact \
  bootstrap/tests/test_broad_run_guard.py::test_collect_only_is_exempt_from_the_guard \
  bootstrap/tests/test_broad_run_guard.py::test_the_guard_refusal_follows_a_late_deselection \
  bootstrap/tests/test_broad_run_guard.py::test_a_run_at_or_under_the_file_threshold_is_never_refused \
  --quality-gate-shuffle-seed=0
```

Outcome: 5 passed in 3.44s. This verifies the existing >40 refusal and its boundary behavior; no guard behavior was changed.

The three environment-sensitive mapped security nodes were rerun with elevated local permissions, at the same SHA and interpreter:

```sh
python3.13 -m pytest -q \
  bootstrap/tests/test_gate_preflight.py::TestCandidateCodeCannotSignFromStageOne::test_the_candidate_position_cannot_sign_through_a_live_agent \
  bootstrap/tests/test_gate_preflight.py::TestCandidateCodeCannotSignFromStageOne::test_the_same_key_signs_when_the_socket_is_present \
  bootstrap/tests/test_security_verification.py::TestNoCapabilityContract::test_a_socket_opening_child_is_excluded_by_admission_not_blocked_at_runtime \
  --quality-gate-shuffle-seed=0
```

Outcome: 3 passed in 0.61s.

The source-derived selection was reconciled by comparing the original collected IDs with the concatenated IDs from both executed split logs. Original collected: 2,700 IDs. Executed union: 2,700 unique IDs. Missing: 0. Extra: 0. Both normalized ID lists have SHA-256 `56be3c2e7c2507e68c3faac1f93dd28f6f65946f1cb11cd291a6cb7f28ca3052`.

## Known cross-family and public paths

- Shipped adopter obligation: `bootstrap/tests/test_review_and_verification_rules_ship.py::test_agents_md_carries_the_obligation` ran in the selected family; focused rule group outcome was 129 passed in 0.17s.
- Installed and governing rule checks: `bootstrap/tests/test_verification_boundaries.py`, `bootstrap/tests/test_certifying_run_rule.py`, and `bootstrap/tests/test_review_and_verification_rules_ship.py` — 129 passed in 0.17s.
- Pinned statement in doctrine: `bootstrap/tests/test_review_stance_in_shipped_files.py` — 480 passed in 1.16s after restoring the established accepted-plan/trivial-review evidence sentence in `doctrine/dual-review.md`.
- Security and gate paths: the three security nodes listed above passed; no gate-manifest, anchor, or AST re-anchor file was changed.
- Documentation gates: `python3.13 scripts/check_cairn.py` — 184 Markdown files, no issues; `python3.13 scripts/link_check.py` — 184 files, no issues; `python3.13 scripts/quality_gate.py --sub neutrality --sub redundancy` — zero failures; 13 authored-document claim checks passed.

No whole suite was run and `CAIRN_FULL_SUITE=1` was not set. Whole-tree certification remains pending at an authorized integration point. Frozen-file ceremony/re-anchor remains pending. The initial three sandbox failures are disposed of by the same-SHA elevated rerun; no unresolved execution failures remain in this mapped selection.
