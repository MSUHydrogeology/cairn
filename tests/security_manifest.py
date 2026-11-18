# SPDX-License-Identifier: MIT
"""The security test family, named file by file with an owner and a reason.

**Why a manifest rather than a marker written into each file.** A
``pytestmark = pytest.mark.security`` line in fourteen files has no single
place to read, no place to say *why* a file is a member, and no way to notice a
file that quietly stopped being one.  Worse, every one of those files is
gate-frozen, so marking them in place would put fourteen entries on the
re-anchor ceremony to express a fact about zero of them.  The membership lives
here; ``conftest.py`` applies the marker from it.

**What membership means.** A member does not run in the per-change loop. It
runs in the release ceremony, where ``release/security_check.py`` executes
the shipped-only selection under ``CAIRN_RELEASE_GATE_ACTIVE=1``. Only a fixed,
source-reviewed opposite-platform setup skip is eligible in the local record;
all other skips and every xfail or xpass fail closed. Nothing is deleted or
weakened; what moves is *when* it runs.

**The consequence of a wrong entry, stated plainly.** Adding a file here removes
it from every per-change run.  That failure is silent -- a test that stops
running does not announce itself -- which is why the membership check
(``test_security_marker.py``) is written as a mutation rather than a count: it
unmarks a member and requires the check to fail.  A check that merely asserted
"the marker collects something" would pass against an empty manifest.

A change to a security surface still runs the full canonical pair with no
deselection, per the accepted contract.  The carve-out is temporal for everyone
else and simply absent for the surface under test.
"""

from __future__ import annotations

#: ``filename -> (owner, reason)``.  Owner is the surface the file defends, not
#: a person: this repository has one maintainer, and naming them would date.
SECURITY_FAMILY: dict[str, tuple[str, str]] = {
    "test_api_access_security.py": (
        "api-access module",
        "Shipped module that mediates outbound API credentials in an adopter "
        "tree.",
    ),
    "test_ast_attest.py": (
        "scaffold engine attestation",
        "Pins the engine package against a committed AST baseline. A "
        "supply-chain control: it is what notices the engine changing shape "
        "without a re-anchor.",
    ),
    "test_default_security_stance.py": (
        "default posture",
        "Asserts what an adopter gets before they configure anything -- the "
        "stance that applies to every install that never tunes it.",
    ),
    "test_portable_security_sweeps.py": (
        "portable-sweep trust root",
        "Resolves and executes a host `gitleaks` binary; AGENTS.md names it a "
        "high-risk executable trust root.",
    ),
    "test_security_capability_install.py": (
        "capability install",
        "What security capabilities the scaffold grants a target tree.",
    ),
    "test_security_check.py": (
        "release gate entry point",
        "release/security_check.py itself -- the command the release ceremony "
        "runs. Unchanged by the split, and the reason the split is safe.",
    ),
    "test_security_finding_confidentiality.py": (
        "finding disclosure",
        "Governs what a security finding may reveal in a shared record.",
    ),
    "test_security_leaf.py": (
        "leaf module",
        "Smallest shipped security surface; included so the family is defined "
        "by kind and not by size.",
    ),
    "test_security_lint.py": (
        "Bandit gate",
        "The Bandit scan over the engine package and the shipped .py surface.",
    ),
    "test_security_net.py": (
        "security-net engine",
        "The four-member engine tree installed under two destination trees.",
    ),
    "test_security_stack.py": (
        "composed stack",
        "How the security modules compose when more than one is installed.",
    ),
    "test_security_verification.py": (
        "verification activation",
        "run_security_verification.py -- whether the shipped verification "
        "actually runs in an adopter tree.",
    ),
    "test_skills_security.py": (
        "skills read-path",
        "The skills fan-out symlink self-heal, which writes into the adopter's "
        "tree.",
    ),
    "test_web_hosting_security.py": (
        "web-hosting module",
        "Shipped module governing an adopter's hosting surface.",
    ),
}

#: A gate-integrity judgement recorded where it can be argued with.
#:
#: ``test_ast_attest.py`` tests *gate integrity* rather than a security property
#: of shipped code. It remains a security member because the gate anchor is a
#: supply-chain control: it exists so an unattended actor cannot weaken the
#: check that governs it. The re-anchor ceremony tests run when their own files
#: change instead.
GATE_INTEGRITY_MEMBERS = frozenset({
    "test_ast_attest.py",
})

#: Maintainer-only tests excluded from the shipped-only release selection.
#: Keep rows rather than a mapping so duplicate paths remain detectable.
RELEASE_EXCLUDED_TESTS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("tests/test_repin.py", ("release/repin.py",),
     "Tests release/repin.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_repin_ceremony.py", ("release/repin.py",),
     "Tests release/repin.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_reanchor.py", ("release/reanchor.sh",),
     "Tests release/reanchor.sh, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_reanchor_driver_disclosures.py", ("release/reanchor.sh",),
     "Tests release/reanchor.sh, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_gate_reanchor.py", ("tests/_gate_reanchor.py",),
     "Tests tests/_gate_reanchor.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_gate_preflight.py", ("tests/_gate_preflight.py",),
     "Tests tests/_gate_preflight.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_gate_manifest.py", ("tests/_gate_manifest.py",),
     "Tests tests/_gate_manifest.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_gate_transition.py", ("tests/_gate_transition.py",),
     "Tests tests/_gate_transition.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_oracle.py", ("tests/_oracle.py",),
     "Tests tests/_oracle.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_oracle_activation.py", ("tests/_oracle_activation.py",),
     "Tests tests/_oracle_activation.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_oracle_trust.py", ("tests/_oracle_trust.py",),
     "Tests tests/_oracle_trust.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_ceremony_review_report.py", ("tests/_gate_preflight.py",),
     "Tests tests/_gate_preflight.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/security/test_check_release_publication.py", ("release/check_release_publication.py",),
     "Tests release/check_release_publication.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_quality_gate_cli.py", ("tests/quality_gate.py",),
     "Tests tests/quality_gate.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/test_quality_gate_order_independence.py", ("tests/quality_gate.py",),
     "Tests tests/quality_gate.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
    ("tests/integration/test_quality_gate_redundancy.py", ("tests/quality_gate.py",),
     "Tests tests/quality_gate.py, which only Cairn's Maintainer runs; none of it is in the install manifest."),
)

RELEASE_REQUIRED_FILES = frozenset({
    "tests/test_ast_attest.py",
    "tests/test_quality_gate_neutrality.py",
    "tests/test_security_check.py",
    "tests/test_security_marker.py",
    "tests/contract/test_release_members_contract.py",
    "tests/test_session_binding_gate_and_printing_hold.py",
    "tests/test_manifest.py",
    "tests/test_verify_integrity.py",
    "tests/test_verify_ref.py",
    "tests/test_security_lint.py",
    "tests/test_loop_fidelity_gate.py",
})


def release_excluded_files() -> frozenset[str]:
    """Validate and return the exact Maintainer-only release exclusions."""
    import re

    if type(RELEASE_EXCLUDED_TESTS) is not tuple:
        raise ValueError("release exclusions must be a tuple")
    pattern = re.compile(
        r"\Atests/(?:[A-Za-z0-9_]+/)*test_[A-Za-z0-9_]+\.py\Z"
    )
    seen: set[str] = set()
    paths: set[str] = set()
    for row in RELEASE_EXCLUDED_TESTS:
        if type(row) is not tuple or len(row) != 3:
            raise ValueError("malformed release exclusion row")
        path, subjects, reason = row
        if type(path) is not str or not pattern.fullmatch(path):
            raise ValueError("malformed release exclusion path")
        if (type(subjects) is not tuple or not subjects
                or any(type(subject) is not str or not subject for subject in subjects)):
            raise ValueError("malformed release exclusion subjects")
        if type(reason) is not str or not reason:
            raise ValueError("malformed release exclusion reason")
        if path in seen:
            raise ValueError("duplicate release exclusion path")
        if path.rsplit("/", 1)[-1] in SECURITY_FAMILY:
            raise ValueError("security-family file cannot be excluded")
        if path in RELEASE_REQUIRED_FILES:
            raise ValueError("required release file cannot be excluded")
        seen.add(path)
        paths.add(path)
    return frozenset(paths)

#: Fixed platform-only test identities, reconciled from committed source
#: and protected collection evidence. The host is os.name: ``nt`` cases
#: are Windows-native; ``posix`` cases require POSIX. Never derive this
#: policy from the current host's observed skips.
#: Base source review: C1 Security Review follow-up at 73aaf88d; candidate
#: SHA-256 13cd64a497f5bd2b0aada8fdfe826032337c8d65039b3aa0763b52d2deff833c.
#: Meter source delta reviewed at 45b071c9 and transferred at 70abbb92;
#: delta JSON SHA-256 7e2f37ebc97017386b299ede8dbe861f9e6668b308becb461c63dd3f4d554be0.
#: Canonical policy identity hashes sorted ASCII ``host\tNodeID\n`` rows.
#: Code-map additions reviewed at 1edccec6; delta JSON SHA-256
#: ad4099c458000a49e99faa88fec1d8e0aece755eaa6e590f0d698665f24ca9c5.
#: Final code-map and interpreter-binding path-fold policy ID:
#: sha256:25572c7fb58892ff5fe233c2e30e1c7dea4a06b2f3da564b14e45666616e28a3.
#: Meter C1 source classification by High review at 2f5022f24f9b80dd61037be7378db3d697d143c952f261d7e301408a79acf7df,
#: comparing committed Meter source 9db91884 with 5c37ac38: 11 new POSIX-only
#: IDs, no removals or renames. Classification is source-based, not inferred
#: from runtime skips.
#: High classification at f01b7850 for Meter native synthetic route source
#: 55435cc9: 7 Windows-only IDs, no existing row removals or renames.
#: High source classification at 4f7be4f6 for the native Git-worker controls:
#: 12 exact Windows-only IDs. Each exercises Windows PE execution, kernel Job,
#: handle, or event behavior unavailable on the portable host.
#: High source classification at the Meter native handoff for 28 exact Windows
#: worker, lock, source, sharing, and publication controls on synthetic roots.
#: High classification at 68972c2c for 14 POSIX-only session Git route controls.
#: Delta JSON SHA-256 e9537364ac246bddc15404f8889c3380e8cb69f81171d732bcd0ad5e19375034.
#: High classification at f845c4b2 for two POSIX leaf controls; at 6c35637d
#: for four POSIX generated-postcommit route controls.
#: High source classification at bce74c6e for two NT reduced-runner controls
#: and four POSIX Git-cleanup/admission controls.
NATIVE_ONLY_NODE_IDS: tuple[tuple[str, str], ...] = (
    ('nt', 'tests/integration/test_meter.py::test_windows_native_refresh_rebuild_and_exports_use_only_synthetic_profile'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_status_reads_only_synthetic_profile[disabled]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_status_reads_only_synthetic_profile[enabled]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_status_reads_only_synthetic_profile[invalid-json]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_status_reads_only_synthetic_profile[missing]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_status_refuses_config_hardlink'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_status_refuses_permissive_config_dacl'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_worker_process_cleanup_contract[normal-exit]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_worker_process_cleanup_contract[nested-job]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_worker_process_cleanup_contract[forced-timeout]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_lock_lifetime'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_source_metadata_mutations[append-and-replace-held]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_source_metadata_mutations[replace-after-enumeration]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_source_metadata_mutations[creation-time-drift]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_source_metadata_mutations[hardlink]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_source_metadata_mutations[file-to-directory]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_source_metadata_mutations[entry-and-parent-reparse]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_source_metadata_mutations[rejected-attribute]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_source_metadata_mutations[dacl-drift-restored-times]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_source_metadata_mutations[enumeration-bound]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_source_metadata_mutations[read-bound]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_source_metadata_mutations[unsupported-filesystem-response]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_candidate_sharing_contract'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[ledger-candidate-write]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[ledger-candidate-flush]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[ledger-rename]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[ledger-old-reopen]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[ledger-directory-flush]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[ledger-target-reopen]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[export-candidate-write]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[export-candidate-flush]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[export-rename]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[export-old-reopen]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[export-directory-flush]'),
    ('nt', 'tests/integration/test_meter.py::test_windows_native_meter_publication_fault_boundaries[export-target-reopen]'),
    ('nt', 'tests/security/test_code_map.py::test_windows_native_cli_enforces_per_source_budget'),
    ('nt', 'tests/security/test_code_map.py::test_windows_native_cli_modes_succeed_with_job_and_do_not_execute_targets'),
    ('nt', 'tests/security/test_code_map.py::test_windows_native_cli_refuses_reparse_entries_and_held_reparse_parent'),
    ('nt', 'tests/security/test_code_map.py::test_windows_native_worker_job_kills_child_on_forced_timeout'),
    ('nt', 'tests/security/test_git_read.py::test_native_git_fixture_compiles_and_runs_owned_control'),
    ('nt', 'tests/security/test_git_read.py::test_native_worker_positive_version_and_closed_input_eof'),
    ('nt', 'tests/security/test_git_read.py::test_native_worker_origin_config_writes_exact_buffer_then_eof'),
    ('nt', 'tests/security/test_git_read.py::test_native_worker_rejects_each_output_cap_overflow[stdout-flood-stdout]'),
    ('nt', 'tests/security/test_git_read.py::test_native_worker_rejects_each_output_cap_overflow[stderr-flood-stderr]'),
    ('nt', 'tests/security/test_git_read.py::test_native_worker_version_hang_is_not_absence_or_empty_success'),
    ('nt', 'tests/security/test_git_read.py::test_native_worker_config_hang_is_not_absence_or_empty_success'),
    ('nt', 'tests/security/test_git_read.py::test_native_worker_early_config_exit_cannot_claim_unwritten_input'),
    ('nt', 'tests/security/test_git_read.py::test_native_worker_timeout_kills_pipe_holding_git_descendant'),
    ('nt', 'tests/security/test_git_read.py::test_native_worker_job_close_kills_quiet_live_descendant'),
    ('nt', 'tests/security/test_git_read.py::test_native_worker_job_setup_failure_precedes_git_launch'),
    ('nt', 'tests/security/test_git_read.py::test_native_worker_cancellation_cleans_worker_and_owned_threads'),
    ('nt', 'tests/security/test_git_interpreter_binding_portable.py::test_windows_reparse_points_refuse_binding_access[shipped-admin]'),
    ('nt', 'tests/security/test_git_interpreter_binding_portable.py::test_windows_reparse_points_refuse_binding_access[shipped-binding-directory]'),
    ('nt', 'tests/security/test_git_interpreter_binding_portable.py::test_windows_reparse_points_refuse_binding_access[shipped-binding-leaf]'),
    ('nt', 'tests/security/test_git_interpreter_binding_portable.py::test_windows_reparse_points_refuse_binding_access[shipped-dot-git]'),
    ('nt', 'tests/security/test_git_interpreter_binding_portable.py::test_windows_reparse_points_refuse_binding_access[source-admin]'),
    ('nt', 'tests/security/test_git_interpreter_binding_portable.py::test_windows_reparse_points_refuse_binding_access[source-binding-directory]'),
    ('nt', 'tests/security/test_git_interpreter_binding_portable.py::test_windows_reparse_points_refuse_binding_access[source-binding-leaf]'),
    ('nt', 'tests/security/test_git_interpreter_binding_portable.py::test_windows_reparse_points_refuse_binding_access[source-dot-git]'),
    ('nt', 'tests/test_intents_tool.py::test_windows_drive_case_normalization_for_pointer_chain'),
    ('nt', 'tests/security/test_prose_tools.py::test_replacer_reads_rewritten_windows_fragment_after_creation'),
    ('nt', 'tests/test_portable_security_sweeps.py::test_native_windows_reduced_entry_runs_version_and_current_tree'),
    ('nt', 'tests/test_portable_security_sweeps.py::test_native_windows_worker_translates_a_bounded_version_timeout'),
    ('posix', 'tests/integration/test_meter.py::test_config_directory_must_be_private_and_link_free'),
    ('posix', 'tests/integration/test_meter.py::test_config_file_must_be_private[416]'),
    ('posix', 'tests/integration/test_meter.py::test_config_file_must_be_private[420]'),
    ('posix', 'tests/integration/test_meter.py::test_config_refuses_linked_leaf_and_unverifiable_owner'),
    ('posix', 'tests/integration/test_meter.py::test_config_rejects_directory_and_fifo_leaves'),
    ('posix', 'tests/integration/test_meter.py::test_disabled_cli_does_not_open_configured_sources_or_ledger'),
    ('posix', 'tests/integration/test_meter.py::test_enabled_cli_stops_before_source_or_ledger_io'),
    ('posix', 'tests/integration/test_meter.py::test_fixed_user_home_uses_posix_account_and_equal_uids'),
    ('posix', 'tests/integration/test_meter.py::test_private_config_open_revalidates_descriptor_identity'),
    ('posix', 'tests/integration/test_meter.py::test_project_remote_reader_requires_direct_private_layout'),
    ('posix', 'tests/integration/test_meter.py::test_safe_reader_open_revalidates_descriptor_identity'),
    ('posix', 'tests/integration/test_meter.py::test_safe_reader_rejects_escape_links_nonregular_and_partial_lines'),
    ('posix', 'tests/integration/test_meter.py::test_safe_reader_rejects_oversized_line'),
    ('posix', 'tests/integration/test_meter.py::test_stream_reader_caps_and_partial_tail_invalidate_batch'),
    ('posix', 'tests/integration/test_meter.py::test_stream_reader_revalidates_open_identity'),
    ('posix', 'tests/security/test_code_map.py::test_interrupted_reads_count_against_total_budget'),
    ('posix', 'tests/security/test_code_map.py::test_race_substituting_a_file_for_a_link_is_refused'),
    ('posix', 'tests/security/test_code_map.py::test_real_cli_refuses_a_linked_root'),
    ('posix', 'tests/security/test_code_map.py::test_real_cli_refuses_fifo'),
    ('posix', 'tests/test_board_json_contract.py::TestSymlinkedSourcesAreNotRead::test_non_regular_entries_fail_loudly_without_hanging'),
    ('posix', 'tests/test_intents_tool.py::TestGitignoreSeedWritesByReplacing::test_pipe_refused_before_open'),
    ('posix', 'tests/test_intents_tool.py::test_strict_claim_reader_refuses_leaf_swap_before_open[fifo]'),
    ('posix', 'tests/test_security_finding_confidentiality.py::test_d3_report_file_mode_is_private[clean]'),
    ('posix', 'tests/test_security_finding_confidentiality.py::test_d3_report_file_mode_is_private[findings]'),
    ('posix', 'tests/test_security_leaf.py::TestReadRegularBytesRefusesAnythingElse::test_posix_special_files_refused_without_blocking'),
    ('posix', 'tests/test_security_leaf.py::TestWriteByReplacing::test_permissions_strip_execute_and_special_bits'),
    ('posix', 'tests/test_security_leaf.py::TestWriteByReplacing::test_swapped_temp_cannot_change_victim_mode'),
    ('posix', 'tests/test_security_net.py::test_a9_report_directory_and_file_modes_are_private'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_binding_that_is_not_utf8_is_a_refusal_not_a_traceback'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_checkout_is_noticed_when_the_binding_spells_the_project_folder_in_another_case[lower]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_checkout_is_noticed_when_the_binding_spells_the_project_folder_in_another_case[upper]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_checkout_that_replaces_an_in_project_interpreter_makes_it_untrusted'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_folder_beside_the_project_whose_name_starts_like_it_is_not_inside_the_project[digit]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_folder_beside_the_project_whose_name_starts_like_it_is_not_inside_the_project[dot]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_folder_beside_the_project_whose_name_starts_like_it_is_not_inside_the_project[hyphen]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_folder_beside_the_project_whose_name_starts_like_it_is_not_inside_the_project[upper-digit]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_value_the_project_chooses_is_printed_encoded[assert_within]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_value_the_project_chooses_is_printed_encoded[evolution_infer_run_failure]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_value_the_project_chooses_is_printed_encoded[handoff_lock_refusal]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_value_the_project_chooses_is_printed_encoded[heal_skill_symlink]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_value_the_project_chooses_is_printed_encoded[intent_list_run_failure]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_value_the_project_chooses_is_printed_encoded[intent_prune_run_failure]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_a_value_the_project_chooses_is_printed_encoded[stale_message_names_the_running_interpreter]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_an_in_project_interpreter_is_found_when_the_project_is_reached_through_a_link'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_an_interpreter_holding_a_lone_surrogate_is_a_refusal_not_a_traceback'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_an_interpreter_inside_a_submodule_of_the_project_is_untrusted'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_an_interpreter_is_found_whatever_case_the_index_spells_its_folder[ENV/BIN/PYTHON3]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_an_interpreter_is_found_whatever_case_the_index_spells_its_folder[Env/bin/python3]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_an_interpreter_outside_the_project_is_not_looked_up'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_an_interpreter_that_git_does_not_list_is_still_trusted'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_child_decoding_respects_utf8_mode[evolution]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_child_decoding_respects_utf8_mode[prune]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_child_decoding_respects_utf8_mode[surface]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_child_streams_are_framed_and_encoded_through_real_subprocess[0-evolution]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_child_streams_are_framed_and_encoded_through_real_subprocess[0-prune]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_child_streams_are_framed_and_encoded_through_real_subprocess[0-surface]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_child_streams_are_framed_and_encoded_through_real_subprocess[1-evolution]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_child_streams_are_framed_and_encoded_through_real_subprocess[1-prune]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_child_streams_are_framed_and_encoded_through_real_subprocess[1-surface]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_malformed_child_bytes_keep_strict_decode_failure[evolution]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_malformed_child_bytes_keep_strict_decode_failure[prune]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_malformed_child_bytes_keep_strict_decode_failure[surface]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_raw_child_write_mutant_is_caught_by_real_child_contract[evolution]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_raw_child_write_mutant_is_caught_by_real_child_contract[prune]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_raw_child_write_mutant_is_caught_by_real_child_contract[surface]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_successful_child_stderr_is_decoded_strictly[evolution]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_successful_child_stderr_is_decoded_strictly[prune]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_successful_child_stderr_is_decoded_strictly[surface]'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_the_same_project_through_a_link_still_trusts_a_program_git_does_not_list'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_the_text_of_a_read_error_is_printed_encoded'),
    ('posix', 'tests/test_session_binding_gate_and_printing_hold.py::test_the_text_of_an_inspect_error_is_printed_encoded'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_binding_git_cannot_be_asked_about_is_not_trusted'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_binding_reached_through_a_link_is_not_trusted'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_binding_written_on_this_machine_is_still_used'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_branch_with_a_legacy_binding_cannot_replace_git_admin_choice'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_could_not_inspect_refusal_names_the_path_only_in_encoded_form'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_malformed_binding_still_refuses'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_not_executable_refusal_names_the_path_only_in_encoded_form'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_parent_traversal_refusal_names_the_path_only_in_encoded_form'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_plain_session_end_ignores_a_legacy_binding_in_checkout_content'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_refusal_names_the_binding_file_only_in_encoded_form[not-an-object]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_refusal_names_the_binding_file_only_in_encoded_form[not-json]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_tracked_legacy_file_does_not_replace_the_git_admin_binding'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_vanished_interpreter_is_named_only_in_encoded_form'),
    ('posix', 'tests/test_session_binding_untracked.py::test_a_vanished_interpreter_keeps_the_stale_message'),
    ('posix', 'tests/test_session_binding_untracked.py::test_git_cannot_verify_a_selected_interpreter_so_resolution_refuses[non-zero]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_git_cannot_verify_a_selected_interpreter_so_resolution_refuses[os-error]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_git_cannot_verify_a_selected_interpreter_so_resolution_refuses[timeout]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_git_index_answer_is_parsed_or_refused[bad-output]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_git_index_answer_is_parsed_or_refused[exit-128]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_git_index_answer_is_parsed_or_refused[exit-1]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_git_index_answer_is_parsed_or_refused[silent-success]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_legacy_binding_spelling_never_controls_interpreter_selection'),
    ('posix', 'tests/test_session_binding_untracked.py::test_session_start_ignores_a_legacy_binding_in_checkout_content'),
    ('posix', 'tests/test_session_binding_untracked.py::test_session_start_prints_the_resolved_interpreter_only_in_encoded_form'),
    ('posix', 'tests/test_session_binding_untracked.py::test_the_callers_git_environment_cannot_redirect_binding_discovery[GIT_CEILING_DIRECTORIES]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_the_callers_git_environment_cannot_redirect_binding_discovery[GIT_DIR+GIT_WORK_TREE]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_the_callers_git_environment_cannot_redirect_binding_discovery[GIT_DIR]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_the_callers_git_environment_cannot_redirect_binding_discovery[GIT_INDEX_FILE]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_the_callers_git_environment_cannot_redirect_binding_discovery[GIT_LITERAL_PATHSPECS]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_the_missing_binding_warning_is_printed_once_per_process'),
    ('posix', 'tests/test_session_binding_untracked.py::test_the_optional_tool_fallback_repeats_a_refusal_only_in_encoded_form'),
    ('posix', 'tests/test_session_binding_untracked.py::test_the_question_put_to_git_is_a_fixed_argument_list_with_no_shell'),
    ('posix', 'tests/test_session_binding_untracked.py::test_when_git_cannot_answer_the_binding_is_not_trusted[git-missing]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_when_git_cannot_answer_the_binding_is_not_trusted[non-zero]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_when_git_cannot_answer_the_binding_is_not_trusted[os-error]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_when_git_cannot_answer_the_binding_is_not_trusted[timeout]'),
    ('posix', 'tests/test_session_binding_untracked.py::test_without_git_the_command_refuses_before_running_anything'),
    ('posix', 'tests/test_session_failsafe.py::test_tampered_local_env_refuses[bad1]'),
    ('posix', 'tests/test_session_failsafe.py::test_uninspectable_interpreter_path_refuses'),
    ('posix', 'tests/test_session_writes_contained.py::test_a_named_pipe_swapped_in_just_before_the_read_is_refused_not_waited_on'),
    ('posix', 'tests/test_session_writes_contained.py::test_a_named_pipe_where_gitignore_should_be_is_refused_not_waited_on'),
    ('posix', 'tests/test_session_writes_contained.py::test_seeding_keeps_the_permission_bits_of_the_file_it_replaces'),
    ('posix', 'tests/test_session_writes_contained.py::test_the_temporary_file_mode_is_set_on_the_open_descriptor_not_by_name'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_failure_in_a_later_group_is_cannot_tell[comparison-hang]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_failure_in_a_later_group_is_cannot_tell[comparison-non-zero exit]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_failure_in_a_later_group_is_cannot_tell[comparison-over the cap]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_failure_in_a_later_group_is_cannot_tell[index-hang]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_failure_in_a_later_group_is_cannot_tell[index-non-zero exit]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_failure_in_a_later_group_is_cannot_tell[index-over the cap]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_link_in_the_path_counts_as_edited_and_a_fifo_does_not_block'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_missing_or_untracked_name_is_handled_as_git_status_does'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_mode_only_edit_counts_unless_filemode_is_off'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_partial_clone_runs_no_upload_program_at_or_above_the_floor'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_replace_ref_cannot_hide_a_staged_edit'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_repository_git_will_not_confirm_is_cannot_tell_and_no_repository_is_no_guard'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_staged_then_reverted_file_counts_as_edited'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_subfolder_project_sees_its_own_edits'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_an_untracked_recorded_name_is_not_returned_and_no_lockfile_gives_an_empty_set'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_apply_goes_on_with_no_git_and_stops_when_git_does_not_answer'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_bare_finalize_asks_about_the_records_it_hashes_and_the_lockfile'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_below_the_floor_a_partial_clone_answers_cannot_tell_and_runs_no_program[core.partialclonefilter]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_below_the_floor_a_partial_clone_answers_cannot_tell_and_runs_no_program[extensions.partialclone]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_below_the_floor_a_partial_clone_answers_cannot_tell_and_runs_no_program[remote.origin.partialclonefilter]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_below_the_floor_a_partial_clone_answers_cannot_tell_and_runs_no_program[remote.origin.promisor]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_below_the_floor_a_project_with_no_partial_clone_setting_is_still_guarded'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_core_filemode_false_makes_a_mode_only_edit_not_count'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_each_caller_stops_or_advises_when_the_check_cannot_tell'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[comparison-hang]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[comparison-non-zero exit]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[comparison-over the cap]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[index-hang]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[index-non-zero exit]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[index-over the cap]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[last commit-hang]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[last commit-non-zero exit]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[last commit-over the cap]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[settings-hang]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[settings-non-zero exit]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_every_git_step_that_fails_is_cannot_tell[settings-over the cap]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_force_runs_no_git'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_git_config_programs_never_run_during_stage_apply_or_finalize'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_git_output_that_cannot_be_read_is_cannot_tell[comparison]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_git_output_that_cannot_be_read_is_cannot_tell[index]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_git_that_cannot_start_or_does_not_answer_at_any_step_is_no_guard_or_cannot_tell[config]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_git_that_cannot_start_or_does_not_answer_at_any_step_is_no_guard_or_cannot_tell[rev-parse --is-inside-work-tree]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_git_that_cannot_start_or_does_not_answer_at_any_step_is_no_guard_or_cannot_tell[rev-parse --verify]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_git_that_will_not_start_is_no_guard_and_git_that_does_not_answer_is_cannot_tell'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_line_endings_rule_applies_only_when_settings_ask_for_crlf[settings0-False]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_line_endings_rule_applies_only_when_settings_ask_for_crlf[settings1-True]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_line_endings_rule_applies_only_when_settings_ask_for_crlf[settings2-True]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_line_endings_rule_applies_only_when_settings_ask_for_crlf[settings3-False]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_line_endings_rule_applies_only_when_settings_ask_for_crlf[settings4-False]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_names_go_in_groups_of_at_most_100'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_names_not_in_git_normal_form_or_naming_a_folder_are_matched_exactly'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_pattern_characters_in_a_name_match_literally'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_check_agrees_with_git_status_on_each_edit_state'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[autocrlf false]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[autocrlf input is not crlf]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[autocrlf input with eol crlf]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[autocrlf maybe]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[autocrlf true]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[autocrlf valueless is true]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[eol crlf]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[eol lf]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[eol native follows the platform]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[eol unknown]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[eol valueless]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[filemode banana]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[filemode empty is false]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[filemode false]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[filemode non-zero number]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[filemode valueless is true]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[filemode zero]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[last filemode wins, false]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[last filemode wins, true]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[no key at all]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[the config call fails with 2]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_config_answer_is_read_as_git_reads_it[the config call fails]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_launcher_is_shared_with_the_committed_copy_check'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_the_unfailing_stand_in_lets_the_check_find_the_edit'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_with_no_names_the_lockfiles_recorded_names_are_asked_about'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_blobless_clone_with_an_upload_pack_program_runs_none_and_keeps_the_copy'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_file_replaced_between_the_read_and_the_removal_is_kept[folder handles]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_folder_that_refuses_the_removal_keeps_the_file[by path]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_folder_that_refuses_the_removal_keeps_the_file[folder handles]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_folder_that_will_not_let_the_file_go_keeps_its_record'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file[-False]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file[2.54.0-False]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file[git version 1.99.99-False]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file[git version 2.100.0-True]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file[git version 2.44.0-False]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file[git version 2.45.0-True]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file[git version 2.45.0.windows.1-True]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file[git version 3.0.0-True]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file[git version two.five.zero-False]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file[git version-False]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_that_does_not_finish_or_prints_too_much_keeps_the_file'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_that_fails_or_is_missing_keeps_the_file'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_with_an_apple_suffix_at_2_44_9_keeps_the_file_and_runs_no_cat_file'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_git_with_an_apple_suffix_at_2_54_0_passes'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_link_a_linked_folder_and_a_folder_in_place_are_kept[folder handles]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_missing_file_counts_as_removed_and_a_folder_in_its_place_is_not[folder handles]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_parent_swapped_after_the_folders_are_open_leaves_the_outside_file_and_folder[a file]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_parent_swapped_after_the_folders_are_open_leaves_the_outside_file_and_folder[an empty folder]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_parent_swapped_for_a_link_between_the_check_and_the_removal_leaves_the_outside_file'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_an_emptied_folder_goes_and_a_non_empty_one_stays[folder handles]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_an_unchanged_file_is_removed_and_its_emptied_folder_with_it[folder handles]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_bytes_changed_between_the_decision_and_the_removal_are_kept[folder handles]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_committed_copy_matches_passes_only_on_exactly_the_bytes'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_committed_copy_matches_refuses_a_name_that_is_not_a_plain_project_path'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_committed_copy_matches_runs_git_with_fixed_overrides_and_environment'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_confirming_that_nothing_is_at_the_name_removes_nothing[folder handles]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_git_config_programs_never_run_during_plan_or_the_step'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_git_version_is_read_once_per_process'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_git_version_output_longer_than_the_cap_is_unreadable'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_the_removal_is_confirmed_by_looking_at_the_name_again[folder handles]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_the_walk_runs_only_when_open_unlink_rmdir_and_stat_all_take_dir_fd'),
    ('posix', 'tests/test_verify_integrity.py::test_a_file_swapped_for_a_symlink_after_the_path_walk_is_refused'),
    ('posix', 'tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base_cache-a-fifo]'),
    ('posix', 'tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[living-a-fifo]'),
    ('posix', 'tests/contract/test_test_tiers.py::test_tiers_governing_diff_refuses_target_local_path_git_route'),
    ('posix', 'tests/integration/test_gauge.py::test_gauge_numstat_refuses_target_local_path_git_route'),
    ('posix', 'tests/integration/test_gauge.py::test_gauge_snapshot_date_refuses_target_local_path_git_route'),
    ('posix', 'tests/test_check_cairn_content.py::TestContentComposition::test_default_selfcheck_uses_verified_index_reads_with_literal_decoy'),
    ('posix', 'tests/test_check_cairn_content.py::TestContentComposition::test_selfcheck_cli_keeps_broken_file_with_decoy_and_catches_literal_mutant'),
    ('posix', 'tests/test_doc_drift_tools.py::TestLinkCheck::test_default_discovery_uses_all_tracked_markdown_with_literal_decoy'),
    ('posix', 'tests/test_doc_drift_tools.py::TestSnippetSync::test_default_discovery_uses_all_tracked_markdown_with_literal_decoy'),
    ('posix', 'tests/test_doc_drift_tools.py::test_each_markdown_owner_refuses_hostile_git_and_catches_path_route_mutant[dev/tools/link_check.py]'),
    ('posix', 'tests/test_doc_drift_tools.py::test_each_markdown_owner_refuses_hostile_git_and_catches_path_route_mutant[dev/tools/sync_doc_snippets.py]'),
    ('posix', 'tests/test_doc_drift_tools.py::test_each_markdown_owner_refuses_hostile_git_and_catches_path_route_mutant[templates/modules/team-gated/link_check.py]'),
    ('posix', 'tests/test_doc_drift_tools.py::test_each_markdown_owner_refuses_hostile_git_and_catches_path_route_mutant[templates/modules/team-gated/sync_doc_snippets.py]'),
    ('posix', 'tests/test_doc_drift_tools.py::test_real_discovery_cli_keeps_broken_file_with_decoy_and_catches_literal_mutant[link-dev/tools/link_check.py]'),
    ('posix', 'tests/test_doc_drift_tools.py::test_real_discovery_cli_keeps_broken_file_with_decoy_and_catches_literal_mutant[snippet-dev/tools/sync_doc_snippets.py]'),
    ('posix', 'tests/test_intents_tool.py::test_generated_precommit_hook_refuses_target_local_git_routes[template-rename]'),
    ('posix', 'tests/test_intents_tool.py::test_generated_precommit_hook_refuses_target_local_git_routes[template-staged]'),
    ('posix', 'tests/test_intents_tool.py::test_generated_precommit_hook_refuses_target_local_git_routes[tools-rename]'),
    ('posix', 'tests/test_intents_tool.py::test_generated_precommit_hook_refuses_target_local_git_routes[tools-staged]'),
    ('posix', 'tests/test_replacement_tools.py::test_legacy_ls_tree_refuses_target_local_path_git_route'),
    ('posix', 'tests/test_replacement_tools.py::test_legacy_show_refuses_target_local_path_git_route'),
    ('posix', 'tests/test_replay_ordinary_c2_mutants.py::test_restore_keeps_exact_bytes_and_mode_and_replacement_is_never_overwritten'),
    ('posix', 'tests/test_replay_ordinary_c2_mutants.py::test_root_preflight_refuses_overlap_self_and_nested_output'),
    ('posix', 'tests/test_replay_ordinary_c2_mutants.py::test_target_walk_rejects_linked_parent_and_hardlinked_leaf'),
    ('posix', 'tests/test_verify_counts.py::test_git_commits_in_range_refuses_target_local_path_git_route'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[templates-skills-_lib-session.py-binding-gitdir]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[templates-skills-_lib-session.py-binding-root]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[templates-skills-_lib-session.py-binding-version]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[templates-skills-_lib-session.py-history]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[templates-skills-_lib-session.py-repo-root]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[templates-skills-_lib-session.py-status]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[templates-skills-_lib-session.py-tracked-interpreter]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[tools-session.py-binding-gitdir]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[tools-session.py-binding-root]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[tools-session.py-binding-version]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[tools-session.py-history]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[tools-session.py-repo-root]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[tools-session.py-status]'),
    ('posix', 'tests/test_session_kernel.py::test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass[tools-session.py-tracked-interpreter]'),
    ('posix', 'tests/test_security_leaf.py::test_public_seed_gitignore_rejects_hardlink_swap_during_staging_without_deleting_unowned_name'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_retired_fifo_is_refused_in_a_bounded_owned_child'),
    ('posix', 'tests/test_intents_tool.py::test_generated_postcommit_hook_refuses_target_local_git_routes[tools-head]'),
    ('posix', 'tests/test_intents_tool.py::test_generated_postcommit_hook_refuses_target_local_git_routes[template-head]'),
    ('posix', 'tests/test_intents_tool.py::test_generated_postcommit_hook_refuses_target_local_git_routes[tools-paths]'),
    ('posix', 'tests/test_intents_tool.py::test_generated_postcommit_hook_refuses_target_local_git_routes[template-paths]'),
    ('posix', 'tests/security/test_git_read.py::test_normal_git_exit_kills_a_quiet_term_ignoring_descendant'),
    ('posix', 'tests/security/test_git_read.py::test_continuous_overflow_cannot_renew_owned_group_cleanup_budget'),
    ('posix', 'tests/test_portable_security_sweeps.py::test_verify_version_support_emits_a_complete_record'),
    ('posix', 'tests/test_portable_security_sweeps.py::test_admission_requires_a_new_history_read_for_each_history_scenario'),
    ('posix', 'tests/contract/test_board_closeout_warning.py::test_warning_escapes_untrusted_name_and_never_shows_closeout'),
    ('posix', 'tests/integration/test_meter.py::test_copied_legacy_fork_reconciles_direct_usage_and_retains_lineage_proof'),
    ('posix', 'tests/integration/test_meter.py::test_disabled_refresh_does_not_create_ledger_directory_or_read_sources'),
    ('posix', 'tests/integration/test_meter.py::test_first_publication_canonicalizes_conflicted_binding_and_repeats_stably'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_detects_substitution_before_publication[candidate]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_detects_substitution_before_publication[config]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_detects_substitution_before_publication[dev-parent]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_detects_substitution_before_publication[measurement-parent]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_detects_substitution_before_publication[old-leaf]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_detects_substitution_before_publication[remote]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_postrename_recheck_failure_is_uncertain'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_refuses_missing_or_linked_parents[dev-link]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_refuses_missing_or_linked_parents[measurement-link]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_refuses_missing_or_linked_parents[missing]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_refuses_unsafe_existing_export[hardlink]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_refuses_unsafe_existing_export[permissive]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_refuses_unsafe_existing_export[symlink]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_write_failures_preserve_or_report_state[cleanup]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_write_failures_preserve_or_report_state[post-flush]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_write_failures_preserve_or_report_state[replace]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_write_failures_preserve_or_report_state[short-write]'),
    ('posix', 'tests/integration/test_meter.py::test_posix_project_export_write_failures_preserve_or_report_state[zero-write]'),
    ('posix', 'tests/integration/test_meter.py::test_project_export_contains_only_sanitized_project_aggregates'),
    ('posix', 'tests/integration/test_meter.py::test_public_refresh_closes_failed_project_publication_receipt'),
    ('posix', 'tests/integration/test_meter.py::test_public_refresh_repeat_and_rebuild_publish_distinct_project_exports'),
    ('posix', 'tests/integration/test_meter.py::test_refresh_deduplicates_rotation_and_partial_tail_keeps_prior_state'),
    ('posix', 'tests/integration/test_meter.py::test_refresh_directory_sync_failure_refuses_project_publication'),
    ('posix', 'tests/integration/test_meter.py::test_refresh_lock_busy_and_replace_failure_preserve_previous_ledger'),
    ('posix', 'tests/integration/test_meter.py::test_refresh_persists_normalized_history_and_claims_without_raw_inputs'),
    ('posix', 'tests/integration/test_meter.py::test_refresh_rejects_duplicate_old_ledger_and_preserves_its_bytes'),
    ('posix', 'tests/integration/test_meter.py::test_retained_wait_binding_is_sticky_across_refresh_and_rebuild[changed]'),
    ('posix', 'tests/integration/test_meter.py::test_retained_wait_binding_is_sticky_across_refresh_and_rebuild[missing]'),
    ('posix', 'tests/integration/test_meter.py::test_retained_wait_binding_is_sticky_across_refresh_and_rebuild[unchanged]'),
    ('posix', 'tests/integration/test_meter.py::test_unproven_copied_fork_keeps_child_usage_unattributed[changed_child_root]'),
    ('posix', 'tests/integration/test_meter.py::test_unproven_copied_fork_keeps_child_usage_unattributed[changed_child_snapshot]'),
    ('posix', 'tests/integration/test_meter.py::test_unproven_copied_fork_keeps_child_usage_unattributed[changed_copied_usage]'),
    ('posix', 'tests/integration/test_meter.py::test_unproven_copied_fork_keeps_child_usage_unattributed[missing_marker]'),
    ('posix', 'tests/integration/test_meter.py::test_wait_rows_bind_dedupe_retain_and_export_sanitized_utc_totals'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[shipped-admin]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[shipped-binding-dangling]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[shipped-binding-directory]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[shipped-binding-leaf]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[shipped-binding-unreadable]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[shipped-binding-wrong-type]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[shipped-control]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[shipped-dot-git]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[source-admin]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[source-binding-dangling]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[source-binding-directory]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[source-binding-leaf]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[source-binding-unreadable]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[source-binding-wrong-type]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[source-control]'),
    ('posix', 'tests/security/test_git_interpreter_binding_portable.py::test_posix_links_and_wrong_types_refuse_binding_access[source-dot-git]'),
    ('posix', 'tests/security/test_git_read.py::test_capture_cancellation_kills_and_reaps_its_owned_group'),
    ('posix', 'tests/security/test_git_read.py::test_darwin_group_eperm_fallback_requires_exact_bounded_membership'),
    ('posix', 'tests/security/test_git_read.py::test_executable_digest_refuses_persistent_ancestor_mode_change'),
    ('posix', 'tests/security/test_git_read.py::test_executable_digest_refuses_replacement_during_read'),
    ('posix', 'tests/security/test_git_read.py::test_host_git_runs_with_closed_input_and_reports_bounded_completion'),
    ('posix', 'tests/security/test_git_read.py::test_native_wait_observer_refuses_unavailable_or_invalid_results[layout]'),
    ('posix', 'tests/security/test_git_read.py::test_native_wait_observer_refuses_unavailable_or_invalid_results[library]'),
    ('posix', 'tests/security/test_git_read.py::test_native_wait_observer_refuses_unavailable_or_invalid_results[observation]'),
    ('posix', 'tests/security/test_git_read.py::test_private_cancellation_flag_closes_a_live_git_descendant'),
    ('posix', 'tests/security/test_git_read.py::test_read_origin_bounds_input_while_draining_both_output_streams'),
    ('posix', 'tests/security/test_git_read.py::test_read_origin_discards_include_paths_and_origin_on_parser_refusal'),
    ('posix', 'tests/security/test_git_read.py::test_read_origin_early_exit_cannot_claim_unwritten_input'),
    ('posix', 'tests/security/test_git_read.py::test_read_origin_from_config_uses_fixed_no_target_argv_and_exact_buffer'),
    ('posix', 'tests/security/test_git_read.py::test_real_status_cannot_execute_a_mixed_case_clean_filter'),
    ('posix', 'tests/security/test_git_read.py::test_timeout_kills_the_owned_process_group_and_returns_incomplete'),
    ('posix', 'tests/test_issue_capture_bootstrap.py::test_label_script_without_credential_exits_2_naming_the_token_variable[github]'),
    ('posix', 'tests/test_issue_capture_bootstrap.py::test_label_script_without_credential_exits_2_naming_the_token_variable[gitlab]'),
    ('posix', 'tests/test_rules_folder_offer.py::test_count_command_and_offer_text'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_post_confirmation_git_startup_loss_stops_writes_or_advises_stage[--apply-config]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_post_confirmation_git_startup_loss_stops_writes_or_advises_stage[--apply-rev-parse --verify]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_post_confirmation_git_startup_loss_stops_writes_or_advises_stage[--finalize-config]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_post_confirmation_git_startup_loss_stops_writes_or_advises_stage[--finalize-rev-parse --verify]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_post_confirmation_git_startup_loss_stops_writes_or_advises_stage[--stage-config]'),
    ('posix', 'tests/test_upgrade_edit_check_runs_no_project_programs.py::test_post_confirmation_git_startup_loss_stops_writes_or_advises_stage[--stage-rev-parse --verify]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_leaf_read_error_is_refused_in_each_removal_branch[folder handles-fstat]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_a_leaf_read_error_is_refused_in_each_removal_branch[folder handles-open]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_confirmation_only_stat_denial_does_not_claim_absence[folder handles]'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_opening_the_removal_target_directory_is_refused'),
    ('posix', 'tests/test_upgrade_removes_retired_files.py::test_post_unlink_stat_denial_does_not_claim_absence[folder handles]'),
)

NATIVE_ONLY_POLICY_ID = "sha256:1089b44337ae08905517169a51658ee51c23bca7043530fa39fc717e0fe9408b"


def validated_native_only_nodes() -> dict[str, frozenset[str]]:
    """Validate the fixed policy before deriving host lookup sets.

    Duplicate IDs are rejected before any mapping can collapse them. The
    canonical identity is checked over the complete ordered policy bytes.
    """
    import hashlib

    if type(NATIVE_ONLY_NODE_IDS) is not tuple:
        raise ValueError("native-only policy must be a tuple")
    seen: set[str] = set()
    canonical_rows: list[str] = []
    grouped: dict[str, list[str]] = {"nt": [], "posix": []}
    for entry in NATIVE_ONLY_NODE_IDS:
        if type(entry) is not tuple or len(entry) != 2:
            raise ValueError("malformed native-only policy entry")
        host, nodeid = entry
        if type(host) is not str or host not in grouped:
            raise ValueError("unknown native-only host")
        if type(nodeid) is not str or not nodeid or not nodeid.isascii():
            raise ValueError("malformed native-only node ID")
        if "\n" in nodeid or "\r" in nodeid or nodeid in seen:
            raise ValueError("duplicate or malformed native-only node ID")
        seen.add(nodeid)
        grouped[host].append(nodeid)
        canonical_rows.append(f"{host}\t{nodeid}\n")
    canonical = "".join(canonical_rows).encode("ascii")
    identity = "sha256:" + hashlib.sha256(canonical).hexdigest()
    if identity != NATIVE_ONLY_POLICY_ID:
        raise ValueError("native-only policy identity mismatch")
    if len(grouped["nt"]) != 63 or len(grouped["posix"]) != 361:
        raise ValueError("native-only policy member count mismatch")
    return {host: frozenset(nodeids) for host, nodeids in grouped.items()}
