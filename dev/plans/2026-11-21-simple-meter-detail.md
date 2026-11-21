# Plan detail: A simple usage meter

This is the companion of `dev/plans/2026-11-21-simple-meter.md` and part of it. It holds the tables a reviewer needs and that would pass the opening body's word limit: every test sorted, every function removed and what replaces it, the choices the plan makes, the exact document sentences, and the pinned-list and gate-manifest lines. Section letters match the plan. Every code change lands in both copies of the meter (`dev/tools/meter.py` and `templates/skills/_lib/meter.py`); the second is made by copying the first (`cp`) in the same commit, then `cmp` of the two prints nothing. Function sizes below are measured spans of the file at commit `e54319bb`; sizes marked "est." or "about" are estimates, not measurements.

## A. Tests sorted

A test counts as **deleted** when it tests a check the proposal removes, **kept with set-up moved** when the test's own text must change (its `POSIX_ONLY` marker comes off because the end-to-end run is now one path on every platform, its patch of the Git read goes, or the note says otherwise), and **kept as it is** when its text does not change. Shared helpers that change are listed in A2 and are not counted as tests. Counts are of test functions; one function may be several pytest node ids.

### A1. Counts

| File | Tests before | Deleted | Kept with set-up moved | Kept as it is | Added |
|---|---|---|---|---|---|
| `tests/integration/test_meter.py` | 260 | 86 | 104 | 70 | 2 |
| `tests/test_meter_claude_usage.py` | 33 | 1 | 0 | 32 | 0 |
| `tests/test_meter_usage_free_records.py` | 4 | 0 | 0 | 4 | 0 |
| `tests/security/test_git_read_routes.py` (the meter's one function, 2 node ids) | 1 | 1 | 0 | 0 | 0 |
| Total | 298 | 88 | 104 | 106 | 2 |

After the change `tests/integration/test_meter.py` holds 176 test functions and `tests/test_meter_claude_usage.py` 32. No test file is added or removed, so `tests/test_tiers.json` is unchanged; `python tests/tier_inventory.py check` confirms it.

### A2. Shared set-up that changes (not counted above)

- `tests/integration/test_meter.py`: the module docstring loses its last promise line, "Native Windows path, profile, sharing, identity, and publication protections hold using only synthetic profiles."
- Deleted whole: `windows_config_bytes`; the classes `SyntheticWindowsConsent`, `SyntheticWindowsStreamAPI`, `SyntheticWindowsLedgerAPI`, `SyntheticWindowsProjectAPI`, `SyntheticWindowsExportAPI`, `SyntheticProfileAPI`; the native-Windows fixtures and helpers (`WINDOWS_ONLY`, `NATIVE_CSC`, `NATIVE_GIT_FIXTURE`, `NATIVE_METER_ROOT_MARKERS`, `native_meter_git_exe`, `native_windows_root`, `native_windows_status`, every `_native_meter_*` helper, `_NATIVE_METER_MAIN_WRAPPER`, `_synthetic_windows_transaction`, `_windows_directory_record`); imports they alone used (`ctypes`, `struct`, `subprocess` if unused).
- `c1_home`: the patch of `_verified_project_remote` goes. `c2_home`: the `.git/config` it writes goes; its mode calls stay (harmless on Windows). `run_main_with_synthetic_home`: the `_windows_config_status` and `_run_windows_refresh` overrides go. `_run_synthetic_meter_command` loses its `verified_remote` argument and its callers follow. `POSIX_ONLY` stays only for the four tests in A5.
- `tests/test_meter_claude_usage.py`: the autouse fixture `passing_remote` goes.
- `tests/security/test_git_read_routes.py`: from the banner "Meter: the approved project's remote" to the end of `test_meter_project_remote_read_refuses_a_git_inside_the_project`, including the fixture `plain_acl_base`; the docstring phrases "(or, for the meter, the one function its command calls)" and "the meter's project-remote read, " go; imports left unused go. This test guards a promise whose code is deleted (no program runs at all now); it is cut under the plan's Security Review.
- **Links on every host.** Kept tests that make a symbolic link (`test_posix_project_export_refuses_missing_or_linked_parents`, cases `dev-link` and `measurement-link`, and the added link test) list those cases at collection time only where the host can make one; on Windows a junction (`mklink /J`) takes the folder link's place. No in-body skip, so no pinned-list row is added.

### A3. Deleted (88)

**Windows-only layer (65 in `test_meter.py`).** These test the removed Windows consent, stream, walk, claim, lock, ledger, export and job code, or run it natively:

`test_windows_native_worker_process_cleanup_contract`, `test_windows_native_meter_lock_lifetime`, `test_windows_native_claude_resume_and_identity_on_a_spaced_root`, `test_windows_native_meter_source_metadata_mutations`, `test_windows_native_meter_candidate_sharing_contract`, `test_windows_native_meter_publication_fault_boundaries`, `test_windows_existing_directory_open_closes_unvalidated_handle`, `test_windows_read_config_tolerates_accessed_only_drift`, `test_windows_read_config_can_retain_and_revalidate_consent_handles`, `test_windows_writable_consent_reopen_changes_only_cairn_access`, `test_windows_owned_cairn_creation_allows_only_namespace_metadata`, `test_windows_owned_cairn_metadata_exception_keeps_other_roles_strict`, `test_windows_owned_cairn_metadata_exception_keeps_identity_proofs`, `test_windows_owned_cairn_metadata_exception_keeps_acl_checks`, `test_windows_owned_cairn_metadata_exception_keeps_exact_consent_bytes`, `test_windows_refresh_reopens_enabled_consent_before_private_io`, `test_windows_refresh_flush_failure_closes_both_consent_chains`, `test_windows_read_config_refuses_stable_metadata_changes`, `test_windows_read_config_refuses_short_file_read`, `test_windows_synthetic_sharing_is_symmetric_and_candidate_scoped`, `test_windows_meter_transaction_parent_shares_read_write_without_delete`, `test_windows_native_create_private_share_modes`, `test_windows_native_create_private_rejects_invalid_transaction_parent_modes`, `test_windows_meter_parent_open_or_create_selects_transaction_mode`, `test_windows_atomic_replace_publishes_complete_validated_candidate`, `test_windows_atomic_replace_failure_preserves_old_bytes_and_cleans_candidate`, `test_windows_atomic_replace_postpublication_flush_failure_is_uncertain`, `test_windows_refresh_disabled_paths_stop_before_source_or_ledger_access`, `test_windows_project_export_replaces_only_the_sanitized_ignored_file`, `test_windows_rename_creation_time_admission`, `test_windows_rename_prepublication_creation_time_drift_still_refuses`, `test_windows_project_export_rechecks_directory_acl_before_replace`, `test_windows_project_export_preserves_or_reports_uncertainty`, `test_windows_project_export_missing_directory_returns_fixed_unavailability`, `test_windows_project_export_missing_during_cleanup_returns_fixed_unavailability`, `test_windows_project_export_disappearance_after_publish_is_uncertain`, `test_windows_approved_stream_revalidates_and_excludes_access_time`, `test_windows_approved_stream_marks_a_partial_tail_unknown`, `test_windows_source_enumeration_reopens_and_matches_entry_identity`, `test_windows_source_enumeration_refuses_replaced_file_identity`, `test_windows_source_snapshot_detects_directory_changes_until_closed`, `test_windows_claim_capture_hashes_only_bounded_project_intents`, `test_windows_claim_capture_treats_missing_or_changed_file_as_unavailable`, `test_windows_claim_capture_enforces_complete_line_cap`, `test_windows_scan_normalizes_synthetic_source_without_project_proof`, `test_windows_directory_decoder_rejects_unsafe_component_names`, `test_windows_consent_status_is_closed_and_uses_only_fixed_profile`, `test_windows_native_status_reads_only_synthetic_profile`, `test_windows_native_status_refuses_config_hardlink`, `test_windows_native_status_refuses_permissive_config_dacl`, `test_windows_refresh_installs_job_only_after_enabled_config_and_retains_it`, `test_windows_disabled_refresh_never_installs_job_or_enters_collector`, `test_windows_job_failure_closes_config_and_stops_before_collector`, `test_windows_main_refresh_uses_only_injected_profile_and_closed_receipt`, `test_windows_native_refresh_rebuild_and_exports_use_only_synthetic_profile`, `test_windows_stream_supports_tail_resume_pieces_growth_and_reread`, `test_windows_reader_preserves_default_and_piece_parity`, `test_windows_fork_parent_context_passes_the_native_reader`, `test_windows_resume_failures_yield_no_lines`, `test_windows_piece_read_failures_are_unavailable_without_fresh_lines`, `test_windows_stream_reports_the_digest_of_its_last_line`, `test_windows_start_scan_bookmarks_existing_log_without_counting_it`, `test_windows_scan_preserves_bookmark_when_resume_window_exceeds_run_budget`, `test_windows_codex_scan_re_reads_from_bookmark_and_counts_only_growth`, `test_windows_profile_owner_may_be_system_or_administrators`

**Other deletions.**

| Test | What it tested |
|---|---|
| `test_verified_git_helper_compiles_admitted_bytes_without_inherited_flags` (test_meter.py) | checked Git helper |
| `test_config_file_must_be_private` (test_meter.py) | owner/mode test of consent file |
| `test_config_directory_must_be_private_and_link_free` (test_meter.py) | private-folder and link test of ~/.cairn |
| `test_config_refuses_linked_leaf_and_unverifiable_owner` (test_meter.py) | link and owner test of consent file |
| `test_private_config_open_revalidates_descriptor_identity` (test_meter.py) | descriptor re-check |
| `test_safe_reader_rejects_escape_links_nonregular_and_partial_lines` (test_meter.py) | descriptor walk (`_contained_file`, unused by the meter) |
| `test_safe_reader_rejects_oversized_line` (test_meter.py) | `_contained_file`, unused by the meter |
| `test_safe_reader_open_revalidates_descriptor_identity` (test_meter.py) | descriptor re-check |
| `test_stream_reader_revalidates_open_identity` (test_meter.py) | descriptor re-check |
| `test_project_remote_reader_requires_direct_private_layout` (test_meter.py) | project Git settings read |
| `test_project_remote_reader_accepts_a_config_that_turns_on_worktrees` (test_meter.py) | project Git settings read |
| `test_project_remote_reader_still_refuses_an_include_beside_the_worktree_setting` (test_meter.py) | project Git settings read |
| `test_project_remote_reader_refuses_a_git_folder_with_per_worktree_files` (test_meter.py) | project Git settings read |
| `test_meter_safe_git_adapter_accepts_only_one_bounded_origin` (test_meter.py) | checked Git helper |
| `test_meter_safe_git_adapter_closes_helper_failures` (test_meter.py) | checked Git helper |
| `test_unsupported_privacy_platform_fails_closed_but_missing_config_is_disabled` (test_meter.py) | `_PRIVATE_FS_SUPPORTED` gate |
| `test_posix_project_export_refuses_unsafe_existing_export` (test_meter.py) | owner, mode and link-count test of the old summary |
| `test_posix_project_export_detects_substitution_before_publication` (test_meter.py) | re-checks before publishing |
| `test_posix_project_export_postrename_recheck_failure_is_uncertain` (test_meter.py) | re-check after publishing |
| `test_refresh_directory_sync_failure_refuses_project_publication` (test_meter.py) | folder flush after rename (dropped) |
| `test_tail_stream_checks_the_file_is_unchanged_at_the_end` (test_meter.py) | re-check during a read |
| `test_failed_remote_check_gives_its_reason` (test_meter_claude_usage.py) | remote check's own reason (Git read) |
| `test_meter_project_remote_read_refuses_a_git_inside_the_project` (test_git_read_routes.py, 2 node ids) | project Git settings read; guard cut under the Security Review |

### A4. Kept with set-up moved (104)

**Marker off only (79).** Remove `@POSIX_ONLY`; the test then runs on all three platforms:

`test_report_freshness_public`, `test_public_refresh_repeat_and_rebuild_publish_distinct_project_exports`, `test_public_refresh_closes_failed_project_publication_receipt`, `test_copied_legacy_fork_reconciles_direct_usage_and_retains_lineage_proof`, `test_unproven_copied_fork_keeps_child_usage_unattributed`, `test_refresh_rejects_duplicate_old_ledger_and_preserves_its_bytes`, `test_disabled_refresh_does_not_create_ledger_directory_or_read_sources`, `test_start_bookmark_stops_after_the_last_complete_line`, `test_log_created_after_the_start_counts_only_events_not_before_it`, `test_a_source_added_later_gets_its_own_start_point`, `test_an_old_ledger_is_refused_and_never_overwritten`, `test_sub_agent_usage_counts_with_its_transcript_and_summary`, `test_summary_without_its_transcript_is_incomplete_until_it_is_read`, `test_hand_edited_ledger_is_refused_as_invalid`, `test_well_formed_daily_rows_and_horizon_load`, `test_a_retained_event_before_the_horizon_is_refused`, `test_tail_stream_finds_the_last_complete_line`, `test_tail_stream_crosses_read_blocks`, `test_tail_stream_refuses_a_line_or_torn_tail_over_the_line_limit`, `test_piece_stream_ignores_a_torn_tail_and_stops_at_the_line_limit`, `test_piece_stream_ends_at_the_last_whole_line_when_the_byte_budget_runs_out`, `test_piece_stream_ceilings_follow_the_reread_limits_not_the_batch_limits`, `test_stream_refuses_inconsistent_keywords`, `test_resume_stream_seeks_to_the_bookmark_after_checking_the_line_before_it`, `test_resume_stream_failures_yield_no_line_and_name_the_check`, `test_resume_stream_reports_a_closed_checks_order`, `test_reread_stream_reads_from_zero_and_checks_the_line_at_the_bookmark`, `test_stream_refuses_inconsistent_resume_keywords`, `test_resume_stream_fails_closed_when_it_cannot_seek`, `test_the_run_limit_is_never_below_the_reread_limit`, `test_a_grown_claude_log_counts_only_the_appended_lines`, `test_resumed_lines_equal_the_same_lines_read_as_a_new_log`, `test_an_unchanged_log_is_not_opened`, `test_a_failed_resume_check_restarts_and_records_why`, `test_a_torn_tail_is_left_for_the_next_run_and_counts_once`, `test_an_append_during_a_read_is_left_for_the_next_run`, `test_a_crlf_log_resumes_after_its_last_line`, `test_a_replys_repeated_usage_lines_count_once_across_runs`, `test_differing_usage_for_one_reply_is_a_conflict_as_in_a_full_read`, `test_a_small_batch_limit_ends_a_piece_on_a_line_boundary_and_later_runs_finish`, `test_a_small_event_limit_leaves_later_logs_for_later_runs`, `test_a_line_over_the_line_limit_is_still_source_budget_exceeded`, `test_the_start_run_counts_tail_and_first_line_bytes_and_defers_the_rest`, `test_a_start_bookmark_waits_for_its_full_read_reservation`, `test_a_run_with_no_budget_opens_no_log_and_keeps_its_cursors`, `test_a_resume_window_that_does_not_fit_the_piece_defers_the_log`, `test_a_fresh_read_drops_events_older_than_the_fold_window`, `test_a_grown_codex_log_counts_only_the_new_turn_and_equals_a_fresh_read`, `test_a_child_is_verified_against_a_parent_that_grew_since_the_start`, `test_a_parent_that_was_not_read_is_read_as_context_and_never_changed`, `test_a_child_is_dropped_when_the_run_cannot_pay_for_its_parent`, `test_a_parent_the_run_already_read_is_not_read_again_as_context`, `test_a_parent_cursor_without_an_owner_leaves_the_child_unverified`, `test_a_verified_child_that_gains_a_turn_stays_verified_with_one_proof`, `test_a_child_whose_earlier_sequence_is_edited_becomes_conflicting`, `test_a_failed_codex_check_restarts_and_counts_only_events_not_before_the_start`, `test_codex_logs_over_a_read_limit_are_skipped_and_the_others_count`, `test_a_codex_log_that_fits_the_limits_but_not_the_rest_of_the_run_is_deferred`, `test_a_codex_reread_ignores_the_claude_piece_limits`, `test_a_fresh_codex_file_drops_events_before_the_start`, `test_a_codex_torn_tail_is_left_for_the_next_run_and_counts_once`, `test_a_proof_may_name_an_event_the_ledger_does_not_hold`, `test_a_proof_naming_an_event_of_another_lineage_is_refused`, `test_folding_changes_no_aggregate_sum`, `test_a_rotated_copy_of_a_log_whose_days_were_folded_adds_nothing`, `test_a_fork_child_read_again_after_its_events_folded_adds_nothing_twice`, `test_sixty_thousand_events_over_twenty_days_leave_at_most_the_target`, `test_a_partly_folded_lineage_stays_and_loads`, `test_a_verified_lineage_whose_child_events_are_all_folded_is_dropped`, `test_a_wait_that_cites_a_lineage_keeps_it_when_the_events_fold`, `test_a_fork_wait_without_its_parent_proof_stays_unknown`, `test_a_conflicting_lineage_is_kept_when_its_events_fold`, `test_a_project_change_merges_folded_rows_into_the_unattributed_row`, `test_a_run_that_is_catching_up_raises_no_horizon_unless_the_ledger_is_very_large`, `test_a_reply_split_across_a_piece_boundary_counts_once_in_the_daily_rows`, `test_a_late_line_older_than_the_saved_horizon_still_counts_and_folds_the_same_run`, `test_the_event_cap_applies_after_folding_and_unknown_time_events_still_hit_it`, `test_events_of_unknown_time_count_toward_the_target_and_never_fold`, `test_events_of_the_clock_day_are_never_folded_even_above_the_target`

**Marker off and Git-read patch removed (13).** Remove `@POSIX_ONLY` and the `monkeypatch.setattr(meter, "_verified_project_remote", ...)` call:

`test_oversized_codex_refresh_publishes_partial_export_and_receipt`, `test_wait_rows_bind_dedupe_retain_and_export_sanitized_utc_totals`, `test_first_publication_canonicalizes_conflicted_binding_and_repeats_stably`, `test_stream_reader_caps_and_partial_tail_invalidate_batch`, `test_project_export_contains_only_sanitized_project_aggregates`, `test_public_refresh_exports_many_closed_claims_without_pairwise_work`, `test_refresh_deduplicates_rotation_and_partial_tail_keeps_prior_state`, `test_first_refresh_records_where_each_log_ends_and_counts_nothing`, `test_a_fresh_read_drops_waits_that_began_before_the_start`, `test_public_refresh_accepts_an_exact_8_mib_line_without_leaking_or_recounting`, `test_public_refresh_refuses_one_byte_over_8_mib_without_publication_changes`, `test_refresh_total_source_budget_is_all_or_unavailable`, `test_the_export_shows_folded_days_without_an_artifact_and_waits_are_unchanged`

**Git-read patch removed (3).** Remove the patch call only:

`test_requested_account_filter_is_unknown_without_source_account_evidence`, `test_combined_owner_headers_stay_unassociated_after_ledger_roundtrip`, `test_event_batches_drop_conflicting_project_binding`

**Other changes (9).**

| Test | Change |
|---|---|
| `test_explicit_refresh_commands_emit_closed_receipt_from_synthetic_home` | the `nt` branch and the `native_windows_root` fixture go; the one path runs everywhere |
| `test_explicit_refresh_partial_receipt_is_closed_and_nonzero` | drop the deleted `native_windows_root` argument |
| `test_codex_normalized_events_bind_only_exact_approved_local_projects` | Git-read patch off; drop the `project_remote_mismatch` assertion (the remote is the consent file's) |
| `test_refresh_persists_normalized_history_and_claims_without_raw_inputs` | POSIX_ONLY marker off; Git-read patch off; delete the two assertions that `ledger.lock` stays (it is removed at the end of a run); the two mode assertions run only `if os.name == "posix"` |
| `test_retained_wait_binding_is_sticky_across_refresh_and_rebuild` | POSIX_ONLY marker off; case `missing` deleted (needs the Git read to fail); `changed` and `unchanged` kept |
| `test_posix_project_export_refuses_missing_or_linked_parents` | POSIX_ONLY marker off; Git-read patch off; calls the new writer; link and missing-folder refusal kept in full |
| `test_posix_project_export_write_failures_preserve_or_report_state` | POSIX_ONLY marker off; Git-read patch off; case `replace` kept; cases `short-write`, `zero-write`, `cleanup`, `post-flush` deleted (they drive the removed descriptor write loop and folder flush) |
| `test_refresh_lock_busy_and_replace_failure_preserve_previous_ledger` | POSIX_ONLY marker off; Git-read patch off; busy lock made by a fresh lock file, not `flock` |
| `test_a_failing_seek_or_identity_read_is_unavailable_and_leaves_the_ledger` | POSIX_ONLY marker off; a failed read now leaves the log for the next run: result is `partial`/`catching_up`, ledger unchanged |

A kept test that needs more than the change named here stops the builder, who reports it instead of widening the test.

### A5. Kept as it is (106)

`tests/integration/test_meter.py` (70): `test_ledger_cursor_preserves_full_unsigned_windows_file_identity`, `test_windows_absolute_source_path_is_closed`, `test_codex_context_accepts_exact_native_windows_cwd_spelling`, `test_repeated_cumulative_checkpoints_are_not_summed`, `test_known_inherited_baseline_is_subtracted_once`, `test_checkpoint_partitions_match_full_arithmetic_when_baseline_is_retained`, `test_unavailable_invalid_or_decreasing_checkpoint_sequence_is_unknown`, `test_direct_pytest_command_classification`, `test_unsupported_pytest_command_classification_is_unknown`, `test_pytest_classification_returns_no_command_arguments`, `test_test_intervals_use_milliseconds_and_union_overlaps`, `test_test_intervals_count_distinct_repeats_and_unordered_nested_intervals`, `test_test_intervals_touching_and_zero_duration`, `test_invalid_test_intervals_are_unknown_without_partial_totals`, `test_timing_reader_extracts_only_transient_classification_and_times`, `test_timing_reader_copied_items_remain_observations_not_execution_totals`, `test_timing_reader_shell_wrapper_is_unknown_without_command_retention`, `test_timing_reader_invalid_endpoints_remain_unknown`, `test_wait_timing_requires_the_supported_root_context_binding`, `test_timing_reader_missing_fields_and_noncommand_items`, `test_codex_direct_response_not_running_totals_or_checkpoints`, `test_codex_per_turn_cwd_override_does_not_use_initial_or_latest_cwd`, `test_codex_inconsistent_or_unproven_cache_semantics_are_unknown`, `test_codex_explicit_zero_cache_write_is_distinct_from_absence`, `test_codex_canonical_direct_record_and_id_fallback_are_synthetic_only`, `test_codex_unproven_header_stays_unattributed`, `test_codex_context_root_fallback_and_explicit_root`, `test_codex_context_must_precede_response_and_duplicates_must_agree`, `test_codex_response_dedup_ignores_envelope_timestamp_but_conflicts_on_payload`, `test_codex_compaction_markers_are_not_extra_usage_records`, `test_codex_identical_header_repeats_are_harmless_but_owner_change_is_not`, `test_event_batches_deduplicate_and_drop_conflicting_time_or_usage`, `test_retained_partial_usage_survives_identical_rescan_and_json_roundtrip`, `test_retained_usage_conflict_is_sticky_unknown`, `test_normalized_event_count_limit_is_fail_closed`, `test_disabled_or_invalid_config_does_not_iterate_a_source`, `test_codex_snapshots_are_validated_but_never_counted`, `test_copied_usage_is_counted_once`, `test_conflicting_copies_are_unknown_not_maximized`, `test_inherited_codex_history_never_gets_a_directory_binding`, `test_codex_unproven_source_binding`, `test_claude_cache_kinds_and_ttl_are_disjoint_not_added_twice`, `test_requestless_claude_does_not_guess_lineage_from_directory`, `test_numeric_values_are_exact_bounded_integers`, `test_invalid_json_and_partial_or_oversized_lines_are_unknown`, `test_no_invented_observation_time`, `test_antigravity_transcript_and_live_payload_do_not_become_billed_usage`, `test_outputs_do_not_retain_ids_paths_body_remote_or_configuration`, `test_empty_batch_keeps_all_sources_unknown`, `test_default_cli_is_disabled_and_ignores_home_environment`, `test_closed_config_validates_aliases_paths_and_stripped_remote`, `test_requested_accounts_filter_is_optional`, `test_config_rejects_unknown_policy_wrong_types_and_bad_bindings`, `test_config_rejects_duplicate_keys_nonfinite_invalid_utf8_and_oversize`, `test_config_accepts_exact_byte_cap_and_rejects_one_byte_over`, `test_config_rejects_duplicate_aliases`, `test_config_rejects_directory_and_fifo_leaves`, `test_fixed_user_home_uses_posix_account_and_equal_uids`, `test_enabled_cli_stops_before_source_or_ledger_io`, `test_disabled_cli_does_not_open_configured_sources_or_ledger`, `test_session_digest_matches_existing_intent_identity_rule`, `test_claim_snapshot_retains_only_hashed_claim_and_safe_targets`, `test_claim_snapshot_skips_a_claim_whose_agent_is_not_a_session_tag`, `test_dated_reference_index_is_exact_and_not_actual_spend`, `test_reference_index_uses_source_reported_cache_ttl_and_keeps_unknown_partial`, `test_selected_codex_context_and_missing_write_do_not_make_a_weighted_total`, `test_documented_ssh_style_remote_is_accepted`, `test_malformed_ssh_style_remote_is_refused`, `test_the_empty_ledger_has_the_new_fields`, `test_resume_window_verdict_is_a_pure_check`

`tests/test_meter_claude_usage.py` (32): `test_record_in_project_folder_counts_as_proven`, `test_record_in_sub_folder_counts_as_proven`, `test_folder_that_is_not_inside_the_project_stays_unknown`, `test_windows_forms_that_are_not_proof`, `test_windows_sub_folder_is_proof`, `test_folder_inside_two_projects_is_not_proof`, `test_unapproved_source_root_is_not_proof`, `test_record_without_request_id_is_not_proven`, `test_one_message_under_two_sessions_is_one_unknown_event`, `test_same_message_twice_in_one_session_is_one_proven_event`, `test_one_message_under_two_folders_is_one_unknown_event`, `test_repeats_with_differing_usage_are_conflicting_usage`, `test_same_records_read_under_two_roots_are_one_event`, `test_proven_event_joins_the_one_claim_that_covers_it`, `test_proven_event_without_a_covering_claim_stays_unmapped`, `test_summary_is_not_usage_and_leaves_one_row`, `test_summary_shape_failure_is_incomplete_not_unsupported`, `test_one_good_and_one_bad_usage_in_one_record_is_incomplete`, `test_skipped_types_stay_skipped_whatever_they_hold`, `test_summary_without_session_is_incomplete`, `test_summary_run_reads_only_the_frame`, `test_transcript_record_registers_one_pair`, `test_transcript_mark_needs_true_and_a_text_agent_id`, `test_summary_then_its_transcript_clears_the_reason`, `test_summary_frames_decide_covered_or_incomplete`, `test_a_run_summarised_twice_is_covered_by_its_one_transcript`, `test_an_unclassified_record_keeps_the_reason_until_the_ledger_is_replaced`, `test_transcript_cap_cuts_the_excess_and_counts_it`, `test_caps_cut_the_excess_and_count_it_without_failing`, `test_the_ledger_round_trips_its_run_record`, `test_a_hand_edit_of_the_run_record_is_refused`, `test_the_export_reaches_the_pulse_as_an_incomplete_reason`

`tests/test_meter_usage_free_records.py` (4): `test_usage_free_record_is_skipped_silently`, `test_unknown_record_type_with_usage_is_flagged_incomplete`, `test_assistant_with_bad_usage_is_invalid_record`, `test_existing_record_names_are_skipped`

Four of these keep their `POSIX_ONLY` marker, because they make a FIFO or read the account database: `test_config_rejects_directory_and_fifo_leaves`, `test_enabled_cli_stops_before_source_or_ledger_io`, `test_disabled_cli_does_not_open_configured_sources_or_ledger`, `test_fixed_user_home_uses_posix_account_and_equal_uids`. Their pinned rows stay (F1).

### A6. Added (2)

1. `test_a_run_over_a_log_folder_with_a_sub_folder_counts_its_logs` (a suggested name): a made-up Claude log folder with one sub-folder holding a log; the helpers `start_counting` and `refresh_counted` run a full refresh; the counts equal those of the same log placed at the folder's top. Runs on every platform, no skip.
2. `test_a_link_out_of_a_log_folder_is_not_followed` (a suggested name): a log folder holding a link to a file and a link to a folder, both pointing outside it at a made-up log; a refresh counts neither. Cases: `symlink` where the host can make one, and `junction` on Windows, listed at collection time (A2).

The proposal's third addition, a summary not written through a link, is already delivered by the kept test `test_posix_project_export_refuses_missing_or_linked_parents` (cases `dev-link`, `measurement-link`, `missing`), which asserts the outside file is untouched.

## B. Tests of the two promises (all kept)

**Consent: nothing is read unless the consent file lists it** (all in `tests/integration/test_meter.py`): `test_default_cli_is_disabled_and_ignores_home_environment`, `test_disabled_cli_does_not_open_configured_sources_or_ledger`, `test_enabled_cli_stops_before_source_or_ledger_io`, `test_disabled_or_invalid_config_does_not_iterate_a_source`, `test_disabled_refresh_does_not_create_ledger_directory_or_read_sources`, `test_closed_config_validates_aliases_paths_and_stripped_remote`, `test_config_rejects_unknown_policy_wrong_types_and_bad_bindings`, `test_config_rejects_duplicate_keys_nonfinite_invalid_utf8_and_oversize`, `test_config_accepts_exact_byte_cap_and_rejects_one_byte_over`, `test_config_rejects_duplicate_aliases`, `test_config_rejects_directory_and_fifo_leaves`, `test_requested_accounts_filter_is_optional`, `test_fixed_user_home_uses_posix_account_and_equal_uids`, `test_explicit_refresh_commands_emit_closed_receipt_from_synthetic_home`.

**Counts only: nothing but counts, times and model names leaves a log** (`tests/integration/test_meter.py`): `test_outputs_do_not_retain_ids_paths_body_remote_or_configuration`, `test_project_export_contains_only_sanitized_project_aggregates`, `test_refresh_persists_normalized_history_and_claims_without_raw_inputs`, `test_public_refresh_accepts_an_exact_8_mib_line_without_leaking_or_recounting`, `test_claim_snapshot_retains_only_hashed_claim_and_safe_targets`, `test_numeric_values_are_exact_bounded_integers`, `test_invalid_json_and_partial_or_oversized_lines_are_unknown`, `test_antigravity_transcript_and_live_payload_do_not_become_billed_usage`, `test_wait_rows_bind_dedupe_retain_and_export_sanitized_utc_totals`, `test_codex_canonical_direct_record_and_id_fallback_are_synthetic_only`, `test_a_failing_seek_or_identity_read_is_unavailable_and_leaves_the_ledger`, `test_refresh_lock_busy_and_replace_failure_preserve_previous_ledger`. Also all of `tests/test_meter_claude_usage.py` and `tests/test_meter_usage_free_records.py` except the one deleted test: their records carry a `SECRET-BODY` sentinel that must not appear in an output.

## C. Functions removed, and what replaces each

A search of `dev/tools/`, `install/`, `tests/` and `templates/` for each name below found no user except `tests/integration/test_meter.py`, `tests/test_meter_claude_usage.py` and `tests/security/test_git_read_routes.py`. `session.py` runs the meter as a child process (`refresh --json`) and reads a receipt; `pulse.py` parses a summary; neither imports the meter. `git_read.py` (frozen, hash pinned in about 20 shipped and test files) is not edited: its `read_origin_from_config` and its tests in `tests/security/test_git_read.py` stay, with no meter caller.

| Removed | Lines | What replaces it |
|---|---|---|
| Windows layer: `_WindowsConsentAPI` (617), `_WindowsApprovedLineStream` (325), `_windows_atomic_write_project_export` (187), `_windows_atomic_replace` (95), `_refresh_ledger_windows` (87), `_enumerate_windows_jsonl` (76), `_windows_project_config` (60), `_capture_windows_project_claims` (59), `_windows_revalidate_private_state` (58), `_WindowsHeldConfig` (51), `_windows_open_root` (38), `_run_windows_refresh` (37), `_decode_windows_directory_entries` (36), `_WindowsDirectorySnapshot` (28), `_windows_open_meter_area`, `_windows_lock`, `_windows_read_old_ledger`, `_windows_directory_state`, `_windows_project_entry`, `_windows_config_decision`, `_windows_config_status`, `_windows_relative_parts`, `_windows_published_candidate_matches`, `_windows_rename_payload`, `_windows_stable_info`, `_WINDOWS_WORKER_JOBS` | 1,864 | Nothing: the plain layer serves Windows too. The kill-on-close job goes; `session.py` reaps its own meter child, and a lock left by a killed run is taken over after 15 minutes. |
| Owner and descriptor code: `_private_regular_file` (79), `_contained_file` (62, unused by the meter), `_revalidate_transaction` (53), `_open_private_leaf` (39), `_verify_private_home` (35), `_open_consent_area` (30), `_open_meter_area` (23), `_open_directory_chain` (21), `_read_ledger_fd_again` (12), `_require_private_fd` (9), `_posix_project_directory_snapshot` (6), `_read_optional_ledger` (4), `_MissingConfig` | 375 | `_read_consent` and `_read_old_ledger` (about 25 lines together) |
| Git settings read: `_posix_project_config` (71), `_safe_git_origin` (37), `_verified_project_remote` (34), `_git_helper_source` (28), `_verified_git_helper` (18); constants `SAFE_GIT_SOURCE_SHA256`, `MAX_GIT_BYTES`, `MAX_GIT_CONFIG_BYTES`, `MAX_GIT_HELPER_BYTES`, `_VERIFIED_GIT_HELPER` | 188 | The consent file's remote (D1). The `exec` the helper loader used goes with it. |
| **Gone outright** | **2,427** | |

| Rewritten | Old lines | New form (about lines) |
|---|---|---|
| `_ApprovedLineStream` and `_iter_approved_lines` | 345 | same class, arguments and attributes; opens by path with `os.open`, reads with `os.read` and `os.lseek`; no walk, no re-checks (230) |
| `_enumerate_jsonl` | 59 | `os.scandir` walk, skips links and reparse marks, same limits (35) |
| `_read_relative_bytes`, `_capture_project_claims` | 108 | `_read_project_claims` (25) |
| `_open_lock`, `_atomic_replace_ledger` | 86 | `_plain_lock`, `_write_beside_and_rename` shared by ledger and summary (55) |
| `_posix_atomic_write_project_export` | 216 | `_write_summary` (35) |
| `_refresh_ledger`, `_run_explicit_refresh`, `main` | 185 | one flow for all four commands (120) |
| `_fixed_user_home`, `load_config`, `_capture_all_claims` | 64 | 50 |
| `_scan_approved_sources` | 323 | drops the `windows` branches and the descriptor root checks (250) |
| `read_records`, `_start_bookmark`, `_read_codex_log`, `_read_fork_parents` | 811 | `read_records` loses its two `windows_*` arguments and changes its one remote call (D1); the other three lose the same two arguments |
| New: `_is_link` | 0 | a link or, on Windows, a reparse mark (8) |
| **Kept as written** | | `_windows_component` (16) and `_windows_absolute_parts` (12), pure text parsers for a Windows path as logged (D9) |

## D. Choices the plan makes

Each is within A to F; none adds a check the proposal removed. A reviewer who disagrees names the item.

1. **Remote.** Inside `read_records`, `verify_project` returns `(project["remote"], None)` and takes no excluded roots. `_capture_all_claims` fills `project_remotes` from the consent file. The comparison of a repository named by a Codex log with the remote stays. Every call of `_verified_project_remote` goes: in `read_records`, `_capture_all_claims`, `_posix_atomic_write_project_export` (deleted) and the Windows functions (deleted). No other line of `read_records` changes; the builder shows it with `git diff` of that function.
2. **Home.** `_fixed_user_home` keeps its name and its equal-UID refusal: on Mac and Linux the home comes from the account database for the real user id (the `HOME` variable still does not select it); on Windows, where there is no account database module, it is `Path.home()`, which follows `USERPROFILE`. The ancestor-folder walk goes. This is the one place Windows differs, and it means a process that can set `USERPROFILE` can name another consent file, which already means it can run code as the user.
3. **A log that cannot be opened or read.** The stream reports `source_read_unavailable` as before. In `_scan_approved_sources` that reason, for one log, keeps that log's old cursor (or none), adds `catching_up` to the run's reasons, and the run goes on to the next log. Budget reasons (`source_budget_exceeded`) still stop the run. `source_changed` is no longer produced.
4. **No folder flush after rename.** A flush of a folder is not portable. The file is flushed before rename, as now. `ledger_durability_uncertain` and `project_export_uncertain` stay in the closed list, which is not edited, and nothing raises them.
5. **Lock.** `ledger.lock` in `~/.cairn/meter/`, made with `O_CREAT | O_EXCL` and holding 32 random hex characters this run writes. If it exists and its modification time is under 900 seconds old (three times `session.py`'s 300-second limit) or more than 60 seconds ahead, `ledger_busy`. Otherwise the run reads its token, reads it again, and removes it only if unchanged; then it makes it afresh with `O_EXCL`, and a failed make is `ledger_busy`. In a `finally`, a run removes `ledger.lock` only if it made it and the file still holds its token. Two runs can still both take over one old lock; then the last rename wins and the other run's counts are read again next run. A run killed by `session.py` leaves its lock, so the next session-end can see `ledger_busy` for up to 15 minutes; the README says so.
6. **Modes.** Where `os.name == "posix"`: files are created `0o600` and the meter folder `0o700`. Elsewhere the defaults apply.
7. **Walk.** The root named in the consent file is followed as named; below it any link, any entry with the Windows reparse attribute and a symlink or mount-point tag (`st_reparse_tag` `0xA000000C` or `0xA0000003`; other tags are read as ordinary entries), and any entry that is neither a regular file nor a folder is skipped, not counted as a failure. Depth, entry and file limits are unchanged.
8. **Consent read.** `Path.is_file()` must hold (a folder or FIFO is refused, which keeps `test_config_rejects_directory_and_fifo_leaves`); a link is followed, as the proposal's Response decided; at most `MAX_CONFIG_BYTES` plus one byte is read from one open and a longer file is refused (the old ledger is read the same way against `MAX_LEDGER_BYTES`); content goes through `validate_config_bytes` unchanged.
9. **Two Windows-named parsers stay.** `_windows_component` and `_windows_absolute_parts` read a Windows path as written in a log record (`_codex_context`, `_project_for_folder`). They open nothing. The reader must not change, so they stay under their names.
10. **`release/security_check.py`.** Its `ALLOWLIST` entry `("templates/skills/_lib/meter.py", "B102")` excuses the helper loader's `exec`. With the `exec` gone, the checker reports the entry as stale and fails, so the entry is deleted in C2. The file is frozen: its gate-manifest hash changes (F2).
11. **Imports.** `struct` and `fcntl` go; `selectors`, `signal` and `subprocess` are already unused and go; `pwd` stays.
12. **Not taken.** The Security Review's optional N1 (refuse a consent file or `~/.cairn` that is a link) stays not taken, as the proposal's Response decided.
13. **No traceback.** `main` catches every `Exception` around each command and prints only the closed receipt (`unavailable`, `unavailable`) or, for the bare status, `unavailable`; no traceback, path or system text is printed.
14. **Project files and links.** `_read_project_claims` refuses `dev` or `dev/intents.jsonl` if it is a link or reparse point (`os.lstat`, then the symlink test, or on Windows the reparse attribute) and reads the file with the limits `MAX_CLAIM_BYTES` and `MAX_CLAIM_LINE` as now. `_write_summary` takes an `os.lstat` of `dev`, then of `dev/measurement`, and refuses each that is a link, a reparse point or not a folder; it writes `.meter-<32 hex>.tmp` in `dev/measurement`, flushes it, renames it over `meter.json`, and on any failure removes the temporary file. A run killed mid-write can leave a `.meter-*.tmp` that Git does not ignore; the next run removes any `.meter-*.tmp` it finds there before it writes. Leaf files may open with `getattr(os, "O_NOFOLLOW", 0)`.
15. **The write gap.** There is no re-check between the folder test and the rename on any platform; see the plan's Scope delta.

## E. Document sentences

Each edit is an exact replacement (`dev/tools/exact_replace.py`); the Old text is quoted from the files as they are at commit `e54319bb`.

### E1. `dev/measurement/README.md`, the meter's section

Two replacements; the example JSON between them is untouched. Words in the replaced text: 548 now, 546 after (counted with `wc -w`). The new text adds three disclosures the reviews asked for (what the consent file trusts, where the summary lands, who can read it) and drops the Windows owner, second-name and Git-settings sentences.

**R1 (lines 59 to 67). Old:**

```text
* **Opt-in Meter collection** — `tools/meter.py` reads consent from the fixed
  OS account home at `~/.cairn/meter.json`; environment home values do not
  select consent, and installation creates no configuration or ledger. The
  config is version 1 with `enabled`, `sources`, and `projects`. Each source
  names an alias, supported tool (`codex`, `claude`, or `antigravity`), and the
  absolute root the collector may scan. Each project names an alias, absolute
  project path, and its expected direct Git remote. For example, replace these
  paths and remote with the exact local locations you intend to include:

```

**New:**

```text
* **Opt-in Meter collection** — `tools/meter.py` reads consent from
  `~/.cairn/meter.json` in the account's home folder (not the `HOME` variable,
  on Mac and Linux); installation creates no configuration or ledger. It reads
  only what the file lists, and only counts leave a log. The file's content is
  checked, not who wrote it. The config is version 1 with `enabled`, `sources`,
  and `projects`. A source names an alias, a tool (`codex`, `claude`, or
  `antigravity`) and the absolute root to scan; a project names an alias, its
  absolute path and its Git remote, taken as written. For example, replace
  these paths and remote with the locations you intend to include:
```

**R2 (lines 85 to 123). Old:**

```text
  Keep the config and private ledger under the account's protected `.cairn`
  directory. On Windows the Meter runs only when `.cairn` and `meter.json` are owned by your own account; if you made them from an administrator shell, make your account their owner. The bare `python tools/meter.py --json` command checks only
  whether configuration is disabled or unavailable; it does not collect.
  `python tools/meter.py refresh --json` explicitly reads only configured
  source roots, verifies configured projects, updates the private ledger at
  `~/.cairn/meter/ledger.json`, and writes sanitized project aggregates to
  a sanitized `meter.json` aggregate under each project's `dev/measurement/`
  folder. `rebuild --json` uses the same
  explicit refresh path. These commands are not scheduled or background work.
  Counting starts when the Meter first runs for a source: it records where
  each existing log ends and counts nothing before that, and `rebuild` does
  not back-fill history. Each later run reads only what a log has gained;
  Codex logs are read again from their first line when they grow, because their
  lines depend on earlier lines. Individual usage events are kept for up to
  14 days (fewer when more than 50,000 would pile up); older ones are folded
  into daily totals, which lose the per-artifact split. A run that stopped at
  its read limit prints `meter partial: catching_up` and exits 5; run `refresh`
  again until it prints `ok`. A Codex log over 512 MiB is skipped each run and
  the run prints `meter partial: source_too_large`. While the receipt is not
  `ok` or `disabled`, `python tools/session.py session-end --handoff` skips
  both prunes and exits 5. The per-project summary lists `incomplete` among
  its coverage reasons and the pulse report prints `INCOMPLETE` beside the
  supplied usage. An older ledger is refused with `ledger_old_schema`; move
  `~/.cairn/meter/ledger.json` aside to start a new one.
  A Claude record counts toward a project when its own working folder is the
  project's or lies inside it, its log is under an approved root, and the
  project's remote checks out. On Windows a log may have a second name (the
  Claude desktop app keeps one for each background sub-agent); the Meter reads
  it once, and only when no other account may write it. A Claude reply logged
  in several pieces is dated by its earliest piece, unless the pieces fall in
  two refreshes. Summaries of finished sub-agents are not
  counted; a reading whose summaries cannot be tied to a read transcript prints
  INCOMPLETE. The runs are kept for every session under the approved roots, so
  one untied summary anywhere marks every project, and it clears only when the
  ledger is replaced (which loses history: a new ledger counts nothing before
  its first refresh).
  Missing configuration stays disabled, and invalid or unsupported privacy
  state fails closed as unavailable. Aggregate coverage remains globally
  unknown; the output does not claim complete project history.
```

**New:**

```text
  The bare `python tools/meter.py --json` command checks only whether
  configuration is disabled or unavailable; it does not collect.
  `python tools/meter.py refresh --json` reads only configured source roots
  (skipping links), updates the ledger at
  `~/.cairn/meter/ledger.json`, and writes a `meter.json` summary of counts,
  times, model names and plan names into each project's existing
  `dev/measurement/` folder. It never creates that folder or `dev`, and never
  writes through a link. Where the system has file modes only you can read the
  ledger and summary; on Windows the summary takes the project folder's access,
  so whoever may read that folder may read the counts. Each file is written
  beside its place and renamed in, and a lock left by a dead run is taken over
  after 15 minutes, so a run killed mid-way can make the next say `ledger_busy` until then. `rebuild --json` takes the same path; neither is scheduled.
  Counting starts at a source's first run: the Meter records where each log ends
  and counts nothing before that, and `rebuild` does not back-fill. Later runs
  read only what a log has gained, except Codex logs, which are read again from
  their first line when they grow. Usage events older than 14 days (or beyond
  50,000) are folded into daily totals, which lose the per-artifact split. A run
  that stopped at its limit or could not open a log prints `meter partial:
  catching_up` and exits 5; run `refresh` again until it prints `ok`. A Codex
  log over 512 MiB is skipped each run (`meter partial: source_too_large`).
  While the receipt is not `ok` or `disabled`, `python tools/session.py
  session-end --handoff` skips both prunes and exits 5. The summary lists
  `incomplete` among its coverage reasons and the pulse report prints
  `INCOMPLETE` beside the usage. An older ledger is refused with
  `ledger_old_schema`; move `~/.cairn/meter/ledger.json` aside to start a new one.
  A Claude record counts toward a project when its own working folder is the
  project's or lies inside it and its log is under an approved root. The Meter
  does not open the project's Git settings, so `current_local_verified` and
  `proven` mean that the folder matched; a Codex log that names its repository
  is still compared with the remote in the config. A Claude reply logged in
  several pieces is dated by its earliest piece, unless the pieces fall in two
  refreshes. Summaries of finished sub-agents are not counted; one that cannot
  be tied to a read transcript prints INCOMPLETE for every project until the
  ledger is replaced (a new ledger counts nothing before its first refresh).
  Missing configuration stays disabled, and invalid configuration is
  unavailable. Aggregate coverage remains globally unknown; the output does not
  claim complete project history.
```

### E2. `templates/core/dev/measurement/README.md`

**Old:**

```text
  consent in `~/.cairn/meter.json`. Its private ledger is
  `~/.cairn/meter/ledger.json`; each configured project receives a sanitized
  `meter.json` export in its `dev/measurement/` folder. The recurring work and cost depend on
```

**New:**

```text
  consent in `~/.cairn/meter.json`. Its private ledger is
  `~/.cairn/meter/ledger.json`; each configured project whose `dev/measurement/`
  folder already exists receives a sanitized `meter.json` export there, which on
  Windows takes that folder's access. The recurring work and cost depend on
```

### E3. `dev/rules/development-environment.md`

Delete the whole bullet (lines 132 to 141); it explains the meter's access-list refusal, which is gone, and its last sentence names the meter test that is cut. **Old:**

```text
- **pytest's temp folders are owner-only.** `icacls` on
  `%TEMP%\pytest-of-cairn` shows explicit entries (SYSTEM, Administrators and
  `OWNER RIGHTS`, all full control) instead of the folder above it, which
  inherits. The meter's project `.git/config` read (`dev/tools/meter.py`,
  `check_acl` with role `ancestor`) refuses a project under such a folder, so a
  real meter read there reports `project_remote_unavailable`. A folder made with
  the default mode under `%TEMP%` passes; a `tempfile.mkdtemp` folder failed the
  same way as pytest's. The `OWNER RIGHTS` entry is the likely cause; I did not
  isolate it. `test_git_read_routes.py` builds its meter repository under such a
  default-mode folder on Windows.
```

### E4. `dev/rules/custom_session_routines.md`

Replace `private consent file `~/.cairn/meter.json`` with `consent file `~/.cairn/meter.json`` (once, line 32). The word "private" stated an owner-only rule that no longer exists. The rule's other sentences stand.

### E5. `CHANGELOG.md`, under Unreleased

Delete these two entries, whose behaviour goes with the code (lines 47 and 49). **Old:**

```text
- **Fixed: Usage meter on a Windows administrator's account.** The meter now accepts a profile folder owned by the Administrators group or the system, which is what Windows makes for an administrator, instead of answering `unavailable`. ([plan](dev/plans/2026-11-21-defect-arc-g-meter-windows-admin.md))
- **Fixed: Usage meter reads a log with a second name once.** On Windows, a log that also has a second name (the Claude desktop app keeps one for each background sub-agent) is read once, when no other account may write it. ([plan](dev/plans/archive/2026-11-21-defect-arc-h-meter-real-log-folder.md))
```

Keep the entries on sub-folders (line 48) and on a reply's date (line 50): both are still true. Add one entry under **Major changes**, after the entry that begins "Added: Claude usage counts toward a project":

```text
- **Changed: A simpler usage meter.** The usage meter reads the log folders you list and writes its summary with ordinary file calls, the same on Mac, Linux and Windows, so it runs on machines where its permission checks used to stop it. It still reads only the folders you list, and only counts leave a log. ([plan](dev/plans/2026-11-21-simple-meter.md))
```

### E6. Sentences that stay

`.agents/skills/session-start/SKILL.md`, `.agents/skills/session-end/SKILL.md` and their templates say "private ledger" and "sanitized"; both remain true (the ledger is user-only where the system has modes). A search for "owned by your own account", "no other account may write", "check_acl", "verifies configured", "remote checks out", "second name" and "project's remote read" over `dev/`, `docs/`, `install/`, `release/`, `templates/` and the top-level files found only the places above, plans and proposals (history, not edited), and `tests/`.

## F. Pinned list and gate manifest

### F1. `tests/security_manifest.py`

- Delete every `('nt', 'tests/integration/test_meter.py::...')` row: 35 rows, all of deleted tests. `nt` goes from 63 to 28.
- Delete every `('posix', 'tests/integration/test_meter.py::...')` row except the four tests in A5 (`test_config_rejects_directory_and_fifo_leaves`, `test_enabled_cli_stops_before_source_or_ledger_io`, `test_disabled_cli_does_not_open_configured_sources_or_ledger`, `test_fixed_user_home_uses_posix_account_and_equal_uids`). Of the 52 posix meter rows, 21 are of deleted tests, 5 of deleted cases (`write_failures` cases `short-write`, `zero-write`, `cleanup`, `post-flush`, and `retained_wait` case `missing`), 22 of tests that now run on every platform, and 4 stay. 48 leave, so `posix` goes from 362 to 314.
- The two counts in the guard line, `if len(grouped["nt"]) != 63 or len(grouped["posix"]) != 362:`, become 28 and 314, in `tests/security_manifest.py` and in the string that `tests/test_security_check.py` quotes (the old line and its replacement in the same test).
- `NATIVE_ONLY_POLICY_ID`: recomputed by the validator's own formula, `"sha256:"` plus the SHA-256 of the concatenation of `host`, a tab, the node id and a newline for every remaining row in file order, ASCII encoded (the function above the guard line). The builder runs that formula and never copies a value from this plan.

### F2. Gate manifest lines for the Maintainer to sign (not edited by this plan)

`tests/fixtures/gate_manifest.json` (schema `cairn-gate-manifest/v2`) holds, for files this plan touches:

- `frozen_files`: the entries for `tests/security_manifest.py`, `tests/test_security_check.py` and `release/security_check.py` (the manifest stores each under a `bootstrap/` folder prefix, and `release/security_check.py` as `security_check.py` there). Their hashes change.
- `ordinary_test_files`: the entries for `tests/integration/test_meter.py` and `tests/security/test_git_read_routes.py`. Their hashes change.
- `collection.node_ids`: 366 ids from `test_meter.py` and 2 from `test_git_read_routes.py::test_meter...`; `collection.skip_xfail_marked`: 89 and 2 of the same. Deleted tests' ids leave; the two added tests' ids come; a test that loses `POSIX_ONLY` leaves `skip_xfail_marked`. `node_count` (5,433) changes.

The meter and `templates/skills/_lib/meter.py` are not in the manifest's frozen list, and `tests/test_meter_claude_usage.py` and `tests/test_meter_usage_free_records.py` have no ids in it. These counts were read from the file, not computed by a gate run.

## G. Direct checks the builder reports per chunk

Searches use the repository's search tool over `dev/tools/meter.py`; each is expected to find nothing unless it says otherwise.

- **C1.** `dir_fd`, `O_NOFOLLOW`, `_open_directory_chain`, `_private_regular_file`, `_verify_private_home`, `_contained_file`, `_WindowsApprovedLineStream`. A hand check on a made-up folder in the repository's ignored scratch folder: the walk lists its real logs and not its linked file or linked folder; a log read in three pieces equals `read_bytes()`.
- **C2.** `exec(`, `git_read`, `fcntl`, `_verified_project_remote`, `SAFE_GIT_SOURCE_SHA256`. `git diff` of `read_records` shows only the remote call and the two arguments. The `ALLOWLIST` entry is gone from `release/security_check.py`.
- **C3.** `windows` (any case) finds only the two parsers and comments about them; `os.name == "nt"` finds only `_is_link`, `_project_for_folder` and `_codex_context`. `python -m py_compile` on both copies passes. The line count is reported.
- **C4.** The test files hold the function counts in A1; no deleted name remains in any test file; `python tests/tier_inventory.py check` passes.
- **C5.** `cmp dev/tools/meter.py templates/skills/_lib/meter.py` prints nothing; `python dev/tools/claim_check.py`, `python dev/tools/link_check.py` and `python tests/check_cairn.py` pass on each changed document; `python install/verify_integrity.py --target .` reports OK after the lock commit, which holds only the lock (`upgrade --finalize`, as in the earlier lock commits).
