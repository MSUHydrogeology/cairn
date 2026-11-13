# Slowest test files in the 0.7 certification run

Measured 2026-11-13. This record was moved here from the v0.7 section of
`dev/PLANNING.md` when that section was removed; the last copy there is in
commit `dbb83261`. It is a dated snapshot. For the longer account of what the
suite costs and why, read [suite-cost.md](suite-cost.md) first.

**Consolidation candidates, slowest first.** These are JUnit case-time sums from the single `072d82d2` certification run on Python 3.13.13, not whole-file wall times. All 51 owners above the 10-second diagnostic target are listed. The full run took 49m06s; this does not establish a speed improvement over earlier differently selected runs. This existing diagnostic list neither reopens completed plans nor adds another test run.

| Test owner | Case-time sum |
|---|---:|
| `bootstrap/tests/test_repin_ceremony.py` | 425.10 s |
| `bootstrap/tests/test_upgrade.py` | 239.96 s |
| `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py` | 161.77 s |
| `bootstrap/tests/test_gate_preflight.py` | 145.61 s |
| `bootstrap/tests/test_upgrade_module_additions.py` | 139.39 s |
| `bootstrap/tests/test_repin.py` | 135.37 s |
| `bootstrap/tests/test_intents_tool.py` | 125.94 s |
| `bootstrap/tests/test_portable_security_sweeps.py` | 120.63 s |
| `bootstrap/tests/security/test_prose_tools.py` | 84.85 s |
| `bootstrap/tests/test_security_stack.py` | 82.38 s |
| `bootstrap/tests/test_upgrade_removes_retired_files.py` | 75.71 s |
| `bootstrap/tests/test_reference_scripts.py` | 67.04 s |
| `bootstrap/tests/test_oracle.py` | 64.50 s |
| `bootstrap/tests/test_session_kernel.py` | 63.12 s |
| `bootstrap/tests/test_security_verification.py` | 52.09 s |
| `bootstrap/tests/test_reanchor.py` | 49.76 s |
| `bootstrap/tests/test_security_check.py` | 44.24 s |
| `bootstrap/tests/security/test_git_interpreter_binding_portable.py` | 42.24 s |
| `bootstrap/tests/test_install_time_onboarding.py` | 41.98 s |
| `bootstrap/tests/test_session_binding_untracked.py` | 41.52 s |
| `bootstrap/tests/test_session_writes_contained.py` | 40.69 s |
| `bootstrap/tests/test_session_failsafe.py` | 26.83 s |
| `bootstrap/tests/test_onboarding_seed_roster.py` | 24.83 s |
| `bootstrap/tests/security/test_code_map.py` | 22.70 s |
| `bootstrap/tests/test_security_net.py` | 22.60 s |
| `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py` | 22.23 s |
| `bootstrap/tests/test_onboarding_slot_substitution.py` | 20.72 s |
| `bootstrap/tests/test_profile_grammar.py` | 19.63 s |
| `bootstrap/tests/test_doc_drift_tools.py` | 19.50 s |
| `bootstrap/tests/test_upgrade_added_slots.py` | 17.68 s |
| `bootstrap/tests/test_gate_reanchor.py` | 17.49 s |
| `bootstrap/tests/test_ceremony_review_report.py` | 17.29 s |
| `bootstrap/tests/test_scaffold.py` | 17.25 s |
| `bootstrap/tests/test_security_finding_confidentiality.py` | 17.17 s |
| `bootstrap/tests/test_status_vocabulary_advisory.py` | 15.50 s |
| `bootstrap/tests/test_session_binding_gate_and_printing_hold.py` | 14.99 s |
| `bootstrap/tests/test_incident_trackers_module.py` | 14.56 s |
| `bootstrap/tests/test_engine_copy_fallback_contained.py` | 14.04 s |
| `bootstrap/tests/test_gate_manifest.py` | 13.77 s |
| `bootstrap/tests/test_model_selection_stub.py` | 13.62 s |
| `bootstrap/tests/security/test_git_read.py` | 12.82 s |
| `bootstrap/tests/test_web_hosting_security.py` | 12.22 s |
| `bootstrap/tests/test_upgrade_side_door_parity.py` | 11.84 s |
| `bootstrap/tests/test_skills_security.py` | 11.64 s |
| `bootstrap/tests/test_security_capability_install.py` | 11.54 s |
| `bootstrap/tests/contract/test_test_tiers.py` | 11.43 s |
| `bootstrap/tests/test_broad_run_guard.py` | 10.75 s |
| `bootstrap/tests/test_board_json_contract.py` | 10.70 s |
| `bootstrap/tests/test_upgrade_lockfile_path_containment.py` | 10.68 s |
| `bootstrap/tests/test_session_routines.py` | 10.51 s |
| `bootstrap/tests/integration/test_gauge.py` | 10.31 s |
