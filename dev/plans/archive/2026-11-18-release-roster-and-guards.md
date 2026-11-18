# Plan: Refresh release roster and held guards

**Author**: gpt-6.1-terra (Implementation, Medium)
**Source proposal**: dev/proposals/archive/2026-11-18-terra-release-roster-and-guards.md
**Status**: archived
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/development-environment.md
**In brief**: Refresh native release-test classifications and retire only guards whose protections remain demonstrably covered.

## Build summary

Reconcile the release roster with current native Mac and Windows behavior, repair the identified skip cases, and resolve the 28 held guards without losing their public protections. Assess eligible redundancy in the named claims-tool test file. Record the evidence and complete the required reviews before the separate release operations.

## Source proposal

The accepted heavy proposal selects Option B: retire only eligible held guards alongside the roster refresh, keeping any whose protection is not established. The Maintainer authorized one further focused Security Review of the old capped code in commit `8ac332b4`, for the precise question and scope below.

## Scope

Change `tests/security_manifest.py`, affected tests and fixtures, and existing shipped-source, parity or release-procedure references only as needed to carry out the accepted dispositions. The prepared `prep/windows-roster-refresh` commits are historical inputs, not current truth. Reconcile current collection and native outcomes, including deleted IDs, 20 now-Windows-capable Git route nodes, 15 previously missed Windows-only nodes, `test_rules_folder_offer.py::test_count_command_and_offer_text`, the illegal-filename call-phase skip in `contract/test_board_closeout_warning.py::test_warning_escapes_untrusted_name_and_never_shows_closeout`, four fixture skips in `test_upgrade_removes_retired_files.py`, and in-body symlink-privilege and POSIX skips. Only genuine opposite-platform setup skips belong in the roster. Account for Gitleaks, Bandit and Vermin availability; missing tools, unexpected skips, xfail and xpass cannot become a strict pass.

Recover the historical 28 rows from Git before `546959c1` and reconcile each to its current owner and named duties. Identify each public promise, distinct protection and proposed retained public witness; the authorized High-tier code review assesses those dispositions before any retirement is final. Restore an unproven guard. Resolve roster, shipped-source, parity and procedure references with each eligible retirement. Assess private-helper and same-branch redundancy only in `tests/test_intents_tool.py`, preserving public warn-default, explicit-block and distinct refusal classes. The claims Decision lifts that file's fence alone; it does not authorize other claims-family cuts.

**Reuse.** Inspect `tests/security_manifest.py`, `release/security_check.py` and existing tests and fixture owners for classifications, public witnesses and the outcome validator. Reuse those entries and `tests/tier_inventory.py`; no new permanent tool or mutation ledger. No doctrine surface changes. Documentation changes, if needed, stay in their existing shipped or release homes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Reconcile current native roster and repair named skip behavior | Reviewed plan; current native evidence | Roster and focused test/fixture repairs |
| C2 | Assess 28 holds and eligible claims tests; propose eligible redundancy and resolve references | C1; High-tier code review before final retirement | Retained public witnesses, eligible removals and references |
| C3 | Run focused native checks and independent reviews | C2 | Evidence and review dispositions |

The Maintainer's exact authorization was: “Accept both as revised, choosing Option B and authorizing the one scoped Security Review pass on #1, implemented in the plan.” The question is: “would removing the identified held guards leave a public path to unsafe writes, bypassed containment or a false release-gate pass without a retained check?” Scope: proposed guard removals, their retained public witnesses, and affected roster/reference changes. The formal Security code review must cover all applicable new protected changes, including roster repairs outside that question. Its record may cover those changes and the one authorized old-code question together, explicitly identifying each scope. This does not reset the old cap or authorize an informal preliminary old-code review. Any further capped-code pass requires new explicit Maintainer authorization and a specific unresolved security question. Independent ordinary and Security plan reviews remain required.

## Acceptance criteria

**C1.** Current native outcomes and collection identity support each roster classification. Each named case is resolved by actual behavior; unsupported setup, call-phase and in-body skips cannot be disguised as opposite-platform setup skips. Required nodes are not silently omitted; missing tools and unexpected skip, xfail or xpass outcomes leave the strict release record unpassed. The existing release outcome validator is the public gate.

**C2.** Each historical hold has a current disposition and named public promise; removals have an existing or focused public-entry witness for each distinct protection and correctly resolved named duties. Otherwise the guard stays. Claims pruning preserves default warning, explicit blocking and distinct public refusal classes. No unrelated claims fence is lifted.

**C3.** Native Mac and Windows evidence binds the exact inventory selections, public nodes, commands and input sets to the tested final candidate, and names interpreters, tool availability, outcomes and gaps. Focused public checks demonstrate passing behavior and one representative negative per changed refusal class. Independent ordinary and Security code reviews resolve findings; the Security record covers all applicable new protected changes and identifies the one authorized old-code scope. A failed or missing check remains unpassed.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation use `python tests/tier_inventory.py for <changed paths>` to select tests naming changed files and focused public-entry nodes. Record the exact inventory selections, public nodes, platform commands and input sets against the tested final candidate in existing evidence. Use current source inventory and known-positive controls for negative searches. Run the applicable checks on native Mac with `/Users/kendal30/conda_envs/lhm/bin/python3.13` and native Windows in the existing local UTM environment, including previously skipped paths; record exact commands, versions and results. Use existing scripts and readers, not a new ledger or one test per helper. For changed prose run claim, link, snippet, neutrality and prose-integrity gates, and inspect readers and byte pins. Independent scientific check: N/A, as accepted.

The arc owner joins integration once after connected work, independently of this plan’s completion. The Maintainer's re-anchor and actual certifying records are separate named board waits with their owner, required evidence and link to this implementation; they remain unpassed until their evidence exists. This plan neither performs nor signs a baseline, and routine release operations do not gate its final chunk. Elapsed: unknown; tokens: unknown.

## Plan review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: dcaef30b77eb008f209129aa9389c6a525c53f8e
**Obligation**: Internal
**Verdict**: REVISE
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** The conditional guard retirement and bounded extra security pass preserve the Decision, but verification and completion sequencing need correction (Scope; Sequence; C3).
2. **Best alternative.** Bind the actual selected checks and inputs to the tested candidate in the existing evidence, and leave joined integration to the arc owner after connected plans finish; neither needs a new ledger (accepted proposal S3; `dev/agent_collaboration.md`, Verification).
3. **What would show it wrong?** A check record whose selected nodes or inputs do not correspond to the candidate, or a completed plan held open solely for another plan's integration, would expose the gaps (C3; Verification).

**Findings**

- The accepted proposal S3 requires the plan to bind exact inventory selections, public nodes, platform commands and input sets to the final candidate. C3 names a candidate and commands but does not require the selected nodes and input sets to be bound to it. Add that requirement to Verification and C3, using existing records.
- C3 puts joined integration after connected work inside this plan's final chunk. Plans finish independently before later integration. Make the arc owner's joined integration a separate arc obligation while retaining this plan's own checks and reviews (Sequence; `dev/agent_collaboration.md`, Verification).

Coverage: read the committed plan, accepted proposal and Decision, current plan template and relevant collaboration rules. Did not collect or run tests, assess actual guard equivalence, inspect native results or perform Security Review. The separate Internal Security Review remains outstanding.

## Plan review -- gpt-6.2-sol (Security Review, High) -- 2026-11-18

Reviewed commit: dcaef30b77eb008f209129aa9389c6a525c53f8e

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown. **Tokens**: unknown.

**Steelman.** Use actual native outcomes to fix the roster and retire a held
guard only when its public protection and named duties are demonstrated.

**Foundations**

1. **Should this happen as framed?** The named skip repairs, conditional removals, and single-file claims fence deliver Option B, but C3 leaves part of required Security code coverage optional (Scope, C1–C3, Decision `8ac332b4`).
2. **Best alternative.** Let one formal review record cover applicable new protected changes and identify the separately authorized capped-code question as one bounded pass (Sequence, `dev/agent_collaboration.md`, Plans and records).
3. **What would show it wrong?** An affected required native node omitted from the outcome record or an ineligible setup or call-phase skip accepted by the release gate would falsify C1 (`release/security_check.py`, `_validate_outcome_rows`; proposal S2–S4).

**Blocking.** Sequence says the authorized old-code pass “may” cover new
roster changes, and C3 requires only the focused Security pass. Require the
Security code review record to cover every applicable new protected change,
including roster repairs outside the removal question. Identify the single
authorized old-code pass on removals, retained public witnesses and affected
roster or references. Preserve the existing requirement for fresh Maintainer
authorization before any further pass on that capped scope (`dev/rules/protected-surfaces.md`, proposal Assurance path, Decision `8ac332b4`).

**Coverage.** Read the committed plan and proposal, Decision, protected rules,
plan template and release outcome validator. No native outcomes, executable
checks or guard equivalence were assessed. The authorized code pass remains due
at its designated step.

## Response -- Terra (author) -- 2026-11-18

Both findings are accepted. Sequence and C3 require Security coverage of all applicable new protected changes and identify the one authorized old-code scope without resetting its cap. The same formal High-tier code review assesses proposed retirement dispositions before they become final; unproven guards are restored. C3 and Verification bind selected checks and inputs to the final candidate; the arc owner’s later joined integration no longer gates this plan. **Disposition**: ready-to-implement. Elapsed: unknown; tokens: unknown.

## C1 and C2 Implementation Checkpoint -- 2026-11-18

**Status**: C1 and C2 implementation committed at `84e4d9c8` and verified on Mac and Windows; awaiting independent ordinary and authorized High Security code reviews.

### C1 Roster and Skip-Marker Repairs (`84e4d9c8`)

- Moved remaining in-body platform/capability skips to setup-phase `@pytest.mark.skipif` / `pytest.param(..., marks=...)` across the 11 C1/C2 test files, split `TestSymlinkedSourcesAreNotRead::test_named_pipe_entry_fails_loudly_without_hanging` in `tests/test_board_json_contract.py`, and fixed the `tests/measurements.py` route path in `tests/test_verify_counts.py`.
- Updated the three `fchmod` skip markers (`tests/test_security_leaf.py` lines 134 and 259; `tests/test_session_writes_contained.py` line 740) to `os.name != "posix" or not hasattr(os, "fchmod")` so Windows does not execute POSIX-only descriptor mode tests even when `os.fchmod` exists.
- `tests/security_manifest.py` validated at **63 Windows / 362 POSIX** (`NATIVE_ONLY_POLICY_ID = sha256:de890081f7b98a2db4a6e2bcfad77db161ac99ceaccef9a477e7ec66b33a4466`); `tests/test_security_check.py` `_connected_runner_fixture` updated to `362` POSIX entries.

### C2 Claims-Tool Inspection (`tests/test_intents_tool.py`)

- Only `tests/test_intents_tool.py` changed in the claims family (C2 fence lifted solely for this file); no unrelated claims fence was lifted.
- Changes convert two in-body `os.mkfifo` skips (`TestGitignoreSeedWritesByReplacing::test_pipe_refused_before_open` and `test_strict_claim_reader_refuses_leaf_swap_before_open[fifo]`) to decorator/parameter `skipif` markers while preserving warn-default, explicit blocking, and distinct public refusal checks with no tautology or over-mocking.

### C2 Disposition of 28 Historical `KEPT-BY-RULE` Guards

Recovered from `git -c core.fsmonitor=false show 546959c1~1:dev/measurement/promise-testing-worklist-2026-11-11.csv` (all 28 `KEPT-BY-RULE` rows):

| # | Current Test Node | Disposition | Named Public Promise / Witness |
|---|---|---|---|
| 1 | `tests/test_doc_drift_tools.py::TestLinkCheck::test_default_discovery_uses_all_tracked_markdown_with_literal_decoy` | Provisionally retired (`a61cec86`), pending authorized High Security code review | Public CLI witness `tests/test_doc_drift_tools.py::TestGitReadPhysicalBindings::test_real_discovery_cli_keeps_broken_file_with_decoy_and_catches_literal_mutant` (`link` param) proves tracked markdown discovery with literal `*.md` decoy and inherited `GIT_LITERAL_PATHSPECS`, plus wildcard negative control. |
| 2 | `tests/test_doc_drift_tools.py::TestSnippetSync::test_default_discovery_uses_all_tracked_markdown_with_literal_decoy` | Provisionally retired (`a61cec86`), pending authorized High Security code review | Public CLI witness `tests/test_doc_drift_tools.py::TestGitReadPhysicalBindings::test_real_discovery_cli_keeps_broken_file_with_decoy_and_catches_literal_mutant` (`snippet` param) proves tracked markdown discovery with literal `*.md` decoy and inherited `GIT_LITERAL_PATHSPECS`, plus wildcard negative control. |
| 3 | `tests/test_portable_security_sweeps.py::test_native_windows_worker_translates_a_bounded_version_timeout` | Retained | Native Windows worker translates bounded `git --version` timeouts into structured refusal rather than hanging or passing unverified. |
| 4 | `tests/test_security_check.py::test_the_conftest_recognizes_the_same_token_pair` | Retained (parity check) | `tests/conftest.py` and `release/security_check.py` recognize the exact same release-gate token pair. |
| 5 | `tests/test_security_leaf.py::TestWriteByReplacing::test_permissions_strip_execute_and_special_bits` | Retained | Atomic replace-write strips execute and special permission bits before publishing target files. |
| 6 | `tests/test_security_marker.py::test_the_manifest_still_names_exactly_the_reviewed_set` | Retained (release procedure) | Security manifest membership matches the exact reviewed release set. |
| 7 | `tests/test_security_net.py::test_channel_passthrough_is_empty_in_shipped_source` | Retained (shipped reference) | Shipped D-2 channel passthrough surface remains an empty frozen set with no writer. |
| 8 | `tests/test_session_binding_gate_and_printing_hold.py::test_raw_child_write_mutant_is_caught_by_real_child_contract` | Retained | Real child contract catches raw child-write mutations bypassing session binding gates. |
| 9 | `tests/test_session_binding_untracked.py::test_a_tracked_legacy_file_does_not_replace_the_git_admin_binding` | Retained | Tracked legacy binding files cannot override or replace the git-admin session binding. |
| 10 | `tests/test_session_binding_untracked.py::test_a_vanished_interpreter_keeps_the_stale_message` | Retained | Vanished bound interpreter refuses execution and preserves the specific stale-binding message. |
| 11 | `tests/test_session_binding_untracked.py::test_when_git_cannot_answer_the_binding_is_not_trusted` | Retained | Session binding is untrusted and refused whenever git cannot answer binding state. |
| 12 | `tests/test_session_writes_contained.py::test_the_temporary_file_mode_is_set_on_the_open_descriptor_not_by_name` | Retained | Temporary file mode is applied via open descriptor (`os.fchmod`) on POSIX, never by path name. |
| 13 | `tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_missing_or_untracked_name_is_handled_as_git_status_does` | Retained | Upgrade edit-check classifies missing or untracked paths consistently with `git status` without running project programs. |
| 14 | `tests/test_upgrade_edit_check_runs_no_project_programs.py::test_a_staged_then_reverted_file_counts_as_edited` | Retained | Staged-then-reverted files still register as edited in the upgrade dirty-tree guard. |
| 15 | `tests/test_upgrade_edit_check_runs_no_project_programs.py::test_an_untracked_recorded_name_is_not_returned_and_no_lockfile_gives_an_empty_set` | Retained | Untracked lockfile entries are excluded from tracked edit checks and absent lockfiles yield an empty set. |
| 16 | `tests/test_upgrade_edit_check_runs_no_project_programs.py::test_below_the_floor_a_project_with_no_partial_clone_setting_is_still_guarded` | Retained | Projects below the Git version floor without partial-clone settings remain guarded by the edit check. |
| 17 | `tests/test_upgrade_edit_check_runs_no_project_programs.py::test_core_filemode_false_makes_a_mode_only_edit_not_count` | Retained | `core.filemode=false` prevents mode-only changes from triggering false-positive dirty-tree refusals. |
| 18 | `tests/test_upgrade_edit_check_runs_no_project_programs.py::test_git_that_cannot_start_or_does_not_answer_at_any_step_is_no_guard_or_cannot_tell` | Retained | Unstartable or non-responsive git at any edit-check step fails closed as no-guard / cannot-tell. |
| 19 | `tests/test_upgrade_edit_check_runs_no_project_programs.py::test_names_go_in_groups_of_at_most_100` | Retained | Upgrade edit-check batches path arguments in groups of at most 100 to avoid command-line truncation. |
| 20 | `tests/test_upgrade_edit_check_runs_no_project_programs.py::test_with_no_names_the_lockfiles_recorded_names_are_asked_about` | Retained | When no explicit names are supplied, upgrade edit-check queries the lockfile's recorded paths. |
| 21 | `tests/test_upgrade_removes_retired_files.py::test_a_missing_file_counts_as_removed_and_a_folder_in_its_place_is_not` | Retained | Retired-file removal treats missing files as removed and refuses to treat a directory in its place as removed. |
| 22 | `tests/test_upgrade_removes_retired_files.py::test_an_unchanged_file_is_removed_and_its_emptied_folder_with_it` | Retained | Unchanged retired files are removed cleanly along with their emptied parent directories. |
| 23 | `tests/test_upgrade_removes_retired_files.py::test_committed_copy_matches_passes_only_on_exactly_the_bytes` | Retained | Committed-copy verification for retired-file removal passes only on an exact byte-for-byte match. |
| 24 | `tests/test_upgrade_removes_retired_files.py::test_committed_copy_matches_refuses_a_name_that_is_not_a_plain_project_path` | Retained | Committed-copy verification refuses non-plain or escaping project paths. |
| 25 | `tests/test_upgrade_removes_retired_files.py::test_confirming_that_nothing_is_at_the_name_removes_nothing` | Retained | Absence confirmation during retired-file cleanup performs no removal when nothing exists at the target path. |
| 26 | `tests/test_upgrade_removes_retired_files.py::test_git_version_is_read_once_per_process` | Retained | Retired-file cleanup reads `git --version` once per process rather than re-probing per file. |
| 27 | `tests/test_upgrade_removes_retired_files.py::test_the_walk_runs_only_when_open_unlink_rmdir_and_stat_all_take_dir_fd` | Retained | Directory-fd-confined retired-file walk runs only when `open`, `unlink`, `rmdir`, and `stat` all support `dir_fd`. |
| 28 | `tests/test_verify_ref.py::test_cairn_roster_names_one_principal` | Retained (shipped reference) | Cairn's internal gate roster names exactly one principal (`as_of 2026`). |

### Verification Evidence

- **Defect fix (`cbdeca91`, separate post-archive fix from `b0aafcf8`)**: `tests/test_security_marker.py:29` (`CAIRN_ROOT = TESTS_DIR.parent`); `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q tests/test_security_marker.py` -> `29 passed in 28.64s`.
- **Mac focused C1/C2 set** (`/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest` on all 15 modified/split nodes across 10 files): `24 passed, 1 skipped in 16.41s` (skip is Windows-only `test_replacer_reads_rewritten_windows_fragment_after_creation`); `test_real_discovery_cli_keeps_broken_file_with_decoy_and_catches_literal_mutant` -> `2 passed, 79 deselected in 3.82s`.
- **Windows focused C1 set** (`C:/ProgramData/miniconda3/envs/lhm/python.exe -m pytest -q -p no:cacheprovider -rfsE` on the 15 modified/split nodes with `[fchmod]` in a disposable archive on `cairn-windows`): `11 passed, 13 skipped in 15.33s` (all 13 skips are setup-phase `skipif` policy skips).
- **Pre-existing out-of-scope Windows observation**: running unparametrized `test_public_seed_gitignore_staging_failure_preserves_destination_and_cleans_owned_temp` on `cairn-windows` failed `[write]` (`tests/test_security_leaf.py:296`) with `[WinError 32]` because `install/_scaffold/security.py:61-87` (`_stage_exclusive`) opens the temp stream with `closefd=False` and calls `tmp.unlink()` inside `except BaseException:` before `finally: os.close(fd)`. Kept unmasked and left untouched outside plan scope (high-risk AST-pinned surface) for Maintainer disposition.
- **Committed-HEAD connected gate fixture (`84e4d9c8`)**: `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q tests/test_security_check.py::test_committed_fixture_connects_real_record_and_join_entrypoints` in an isolated detached worktree of `84e4d9c8` -> `1 passed, 3 warnings in 26.65s`.

Elapsed: unknown. Tokens: unknown.


## Code review -- Hydrogen (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: 58aafbd4 (covering `4f3887e6`, `a61cec86`, `cbdeca91`, `84e4d9c8`, `58aafbd4`)
**Obligation**: Internal
**Verdict**: ACCEPT
**Elapsed**: ~1 minute. **Tokens**: unknown.

**Steelman.** Reconcile the native release-test roster and setup-phase skip markers with current Mac and Windows behavior, preserve public claims-tool protections under the single lifted fence, and resolve all 28 historical `KEPT-BY-RULE` guards without masking out-of-scope defects.

**Foundations**

1. **Should this happen as framed?** Yes. C1 converts remaining in-body platform and capability skips to setup-phase `@pytest.mark.skipif` / `pytest.param` across the affected test files, splits `test_named_pipe_entry_fails_loudly_without_hanging` in `tests/test_board_json_contract.py`, fixes `tests/measurements.py` routing in `tests/test_verify_counts.py`, and aligns `tests/security_manifest.py` (`63` `nt`, `362` `posix`, `sha256:de890081...`) and `tests/test_security_check.py`.
2. **Best alternative.** Retaining all 28 historical guards and keeping in-body skips would avoid provisional removals, but would leave native-only setup skips misclassified and omit the accepted Option B public-witness assessment.
3. **What would show it wrong?** A silent call-phase skip accepted as a pass, a widened claims-family fence, an unmapped `KEPT-BY-RULE` guard, or a masked Windows failure would falsify the record.

**Findings.** None. In `tests/test_intents_tool.py` (C2 single lifted fence), only the two `os.mkfifo` skips (`test_pipe_refused_before_open`, `test_strict_claim_reader_refuses_leaf_swap_before_open[fifo]`) move to `skipif` markers while warn-default, explicit-block, and distinct public refusal checks remain intact. All 28 historical `KEPT-BY-RULE` rows from `546959c1~1:dev/measurement/promise-testing-worklist-2026-11-11.csv` are accounted for (26 retained; 2 `test_doc_drift_tools.py` helper tests from `a61cec86` provisionally retired pending the separate authorized High Security code review). Recorded verification—including `cbdeca91` (`29 passed`), Mac (`24 passed, 1 skipped`; `2 passed, 79 deselected`), Windows `[fchmod]` (`11 passed, 13 skipped`), committed-HEAD fixture (`1 passed`), and the unmasked out-of-scope `install/_scaffold/security.py:61-87` `[WinError 32]` observation—is accurate and complete.

**Coverage.** Inspected committed plan `58aafbd4`, accepted proposal, historical CSV at `546959c1~1`, and committed diffs `4f3887e6`, `a61cec86`, `cbdeca91`, `84e4d9c8`, and `58aafbd4`. Did not execute tests or perform Security Review.


## Security code review -- Argon (Security Review, High) -- 2026-11-18

**Reviewed commit**: 86fad9b0 (covering `4f3887e6`, `a61cec86`, `cbdeca91`, `84e4d9c8`, `58aafbd4`, `86fad9b0`)
**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: ~4 minutes. **Tokens**: unknown.

**Steelman.** Reconcile the native release-test roster and setup-phase skip classifications with actual Mac and Windows behavior, preserve public claims-tool protections under the single lifted fence, and retire only the two doc-discovery helper guards whose distinct protections are fully preserved by a retained public CLI witness under the one authorized old-code pass (`Decision 8ac332b4`).

**Foundations**

1. **Should this happen as framed?** Yes. In Scope 1 (new protected changes across `4f3887e6`, `cbdeca91`, and `84e4d9c8`), converting in-body `pytest.skip` calls to setup-phase `@pytest.mark.skipif` / `pytest.param(..., marks=...)` markers and splitting the portable vs. named-pipe board test aligns collection and runtime phases with `release/security_check.py:329-381` (`_validate_outcome_rows`), while `tests/security_manifest.py` (`63` `nt`, `362` `posix`, `NATIVE_ONLY_POLICY_ID = sha256:de890081f7b98a2db4a6e2bcfad77db161ac99ceaccef9a477e7ec66b33a4466`) and `tests/test_security_check.py:1306` match. In Scope 2 (the single authorized old-code question from `Decision 8ac332b4`, commit `a61cec86`), retiring `TestLinkCheck::test_default_discovery_uses_all_tracked_markdown_with_literal_decoy` and `TestSnippetSync::test_default_discovery_uses_all_tracked_markdown_with_literal_decoy` leaves zero gap because the retained public CLI witness `tests/test_doc_drift_tools.py:480-546` (`test_real_discovery_cli_keeps_broken_file_with_decoy_and_catches_literal_mutant`, parametrized `[link-dev/tools/link_check.py]` and `[snippet-dev/tools/sync_doc_snippets.py]`) exercises every distinct protection while all other 26 historical `KEPT-BY-RULE` guards remain retained.
2. **Best alternative.** Retaining the two helper-level literal-decoy tests (`REVISE` to restore `a61cec86`) would avoid removing any historical `KEPT-BY-RULE` node, but would duplicate the public CLI witness (`test_real_discovery_cli_keeps_broken_file_with_decoy_and_catches_literal_mutant`) that already tests real subprocess invocation, physical `_GIT_READ_SHA256` helper binding, `GIT_LITERAL_PATHSPECS=1` inheritance, literal `*.md` decoy survival, broken link/snippet refusal, and the `--literal-pathspecs` wildcard negative-control mutant.
3. **What would show it wrong?** Any setup or call-phase skip that allows `_validate_outcome_rows` (`release/security_check.py:356-365`) to accept a same-host skip or mask an opposite-platform failure, any reduction of warn-default or explicit-block refusal coverage in `tests/test_intents_tool.py`, a missing protection or dangling roster/doc reference from `a61cec86`, or masking the pre-existing Windows `[WinError 32]` failure in `install/_scaffold/security.py:61-87` as a skip would require `REVISE`.

**Scope 1: All new protected changes (`4f3887e6`, `cbdeca91`, `84e4d9c8`, `58aafbd4`, `86fad9b0`).**

- **Roster policy and gate validator alignment**: `tests/security_manifest.py:567-689` records `63` `nt` and `362` `posix` native-only setup-skip IDs (`NATIVE_ONLY_POLICY_ID = "sha256:de890081f7b98a2db4a6e2bcfad77db161ac99ceaccef9a477e7ec66b33a4466"`), removes the 7 deleted Meter IDs (`4f3887e6`), updates relocated tool paths (`dev/tools/link_check.py`, `dev/tools/sync_doc_snippets.py` in `tests/test_doc_drift_tools.py:117-120`, `tests/test_doc_drift_tools.py:152-153`, `tests/test_doc_drift_tools.py:452-453`, and `tests/test_doc_drift_tools.py:486-487`; `dev/tools/session.py` in `tests/security/test_git_interpreter_binding_portable.py:27-28`; `tests/measurements.py` in `tests/test_verify_counts.py:720-727`), and synchronizes `_connected_runner_fixture` in `tests/test_security_check.py:1306` (`len(grouped["posix"]) != 362`).
- **Setup-phase skip migrations**: Inspected all 11 modified test files across `4f3887e6` and `84e4d9c8`. Moving in-body skips to `@pytest.mark.skipif` or `pytest.param(..., marks=pytest.mark.skipif(...))` ensures skips occur in pytest `setup` rather than `call`, satisfying `release/security_check.py:356-365` (`_validate_outcome_rows` requires `set(phases) == {"setup", "teardown"}` and `expected_native != host_tag`). In particular:
  - `tests/test_security_leaf.py:134`, `tests/test_security_leaf.py:258-259`, and `tests/test_session_writes_contained.py:740` gate POSIX descriptor-mode tests on `os.name != "posix" or not hasattr(os, "fchmod")`, matching production POSIX-only descriptor-mode guards (`install/_scaffold/security.py:73`) so Windows Python builds exposing `os.fchmod` do not run POSIX mode-bit checks.
  - `tests/test_board_json_contract.py:609-631` splits `TestSymlinkedSourcesAreNotRead::test_non_regular_entries_fail_loudly_without_hanging` (portable directory-named-`x.md` and regular-file-`dev/plans` refusal checks now run on both Windows and POSIX) from `test_named_pipe_entry_fails_loudly_without_hanging` (`@pytest.mark.skipif(not hasattr(os, "mkfifo"), ...)` and enrolled in `tests/security_manifest.py:478`).
  - `tests/contract/test_board_closeout_warning.py:84`, `tests/test_upgrade_removes_retired_files.py:338`, `tests/security/test_git_read.py:378-379`, `tests/security/test_prose_tools.py:534`, `tests/test_session_failsafe.py:386-387`, `tests/test_session_writes_contained.py:267`, `tests/test_session_writes_contained.py:773-782`, `tests/test_upgrade.py:2800`, and `tests/test_verify_counts.py:718` restrict skips strictly to genuine opposite-platform or missing-FIFO setup conditions without masking opposite-platform failures.
- **Single lifted claims fence (`tests/test_intents_tool.py`, C2)**: Only `tests/test_intents_tool.py` was touched in the claims family (`84e4d9c8`), converting two `os.mkfifo` call-phase skips (`TestGitignoreSeedWritesByReplacing::test_pipe_refused_before_open` at line 708 and `test_strict_claim_reader_refuses_leaf_swap_before_open[fifo]` at lines 1376-1377, enrolled in `tests/security_manifest.py:479-480`) to setup-phase `skipif` markers. All public warn-default (`test_unclaimed_warns`, `test_no_config_warns_on_cross_claim_by_default`, `test_explicit_warn_never_blocks_but_surfaces`, `test_stale_cross_claim_warns_but_does_not_block`), explicit-block (`test_block_refuses_other_session`, `test_confirm_mode_without_a_terminal_blocks`, `test_fresh_cross_claim_still_blocks`, `test_real_two_session_shared_index_sweep_is_blocked`), and distinct refusal tests remain intact.
- **Post-archive defect fix (`cbdeca91`) and unmasked Windows `[WinError 32]` observation**: `cbdeca91` fixes `tests/test_security_marker.py:29` (`CAIRN_ROOT = TESTS_DIR.parent` after `b0aafcf8` relocated the test directory to `tests/`). The pre-existing Windows failure on `tests/test_security_leaf.py::test_public_seed_gitignore_staging_failure_preserves_destination_and_cleans_owned_temp[write]` (`[WinError 32]` in `install/_scaffold/security.py:61-87` `_stage_exclusive`, where `tmp.unlink()` runs in `except BaseException:` before `finally: os.close(fd)` closes the `closefd=False` descriptor) is honestly recorded in the plan (`58aafbd4`) and left unmasked (neither skipped nor added to `tests/security_manifest.py`).

**Scope 2: The ONE authorized old-code question (`Decision 8ac332b4`, commit `a61cec86`).**

- **Authorized question**: *"would removing the identified held guards leave a public path to unsafe writes, bypassed containment or a false release-gate pass without a retained check?"*
- **Direct comparison of `a61cec86` against retained public CLI witness**:
  - Commit `a61cec86` retires `tests/test_doc_drift_tools.py::TestLinkCheck::test_default_discovery_uses_all_tracked_markdown_with_literal_decoy` and `tests/test_doc_drift_tools.py::TestSnippetSync::test_default_discovery_uses_all_tracked_markdown_with_literal_decoy` (lines 666-688 and 838-861 in `a61cec86~1`) and removes their two `posix` entries from `tests/security_manifest.py`.
  - In `tests/test_doc_drift_tools.py:480-546` at `86fad9b0`, the retained module-level public CLI witness `test_real_discovery_cli_keeps_broken_file_with_decoy_and_catches_literal_mutant` (parametrized `[link-dev/tools/link_check.py]` and `[snippet-dev/tools/sync_doc_snippets.py]`, both enrolled in `tests/security_manifest.py:532-533`; note that the plan's C2 prose table at lines 132-133 prefixes the function name with `TestGitReadPhysicalBindings::`, whereas the code and manifest use the exact module-level node IDs) exercises every distinct protection of both retired helper tests through the public CLI entrypoint:
    1. *Tracked Markdown discovery only*: invokes `dev/tools/link_check.py --root <root>` and `dev/tools/sync_doc_snippets.py --root <root> --check` (plus the scaffold-installed copy at lines 513-524) with no explicit file paths, driving default `tracked_markdown(root)` -> `_tracked_index_paths(root)` (`dev/tools/link_check.py:828-869`, `dev/tools/sync_doc_snippets.py:367-408`).
    2. *Literal `*.md` pathspec decoy preserved and unexpanded*: `_markdown_discovery_tree(tmp_path, literal_decoy=True)` (lines 313-328) commits both `broken.md` and a literal `*.md` file; the witness verifies both tracked files are scanned (`"across 2 file(s)"` at line 496; `"2 doc(s) scanned"` / `"2 Markdown file(s) scanned"` after repair at lines 537 and 545).
    3. *`GIT_LITERAL_PATHSPECS` and real `git ls-files` binding*: `_discovery_cli_env` (lines 331-340) exports `GIT_LITERAL_PATHSPECS=1` into the real child process running against the SHA-256-pinned `git_read.py` helper (`_bound_cli_tree`, lines 143-171), and lines 500-510 execute a negative-control mutant (`literal_wildcard=True`, mutating `("ls-files", "-z", "--cached", "--stage")` to append `"*.md"` under `--literal-pathspecs`) and prove the mutant falsely scans only 1 file (`*.md`) and exits `0`.
    4. *Broken link and drifted snippet refusal*: `_assert_discovery_finding(candidate, kind)` (lines 405-410) verifies `returncode == 1` and `"broken.md"` with `"broken link"` (`link`) or `"snippet(s) drifted"` (`snippet`) on `stderr`.
- **Roster, docs, and remaining 26 `KEPT-BY-RULE` guards**: `tests/security_manifest.py`, `dev/rules/protected-surfaces.md`, `install/SAFETY.md`, and shipped templates contain no dangling references to `test_default_discovery_uses_all_tracked_markdown_with_literal_decoy` (pre-relocation historical entries exist only in `tests/fixtures/gate_manifest.json`, which belongs to the separate Maintainer re-anchor ceremony). All remaining 26 historical `KEPT-BY-RULE` guards from `546959c1~1:dev/measurement/promise-testing-worklist-2026-11-11.csv` are verified present in `tests/` at `86fad9b0` with their roster, parity, shipped-source, and release-procedure duties preserved.
- **Disposition and cap preservation**: **ACCEPT** applies to both Scope 1 (all new protected changes) and Scope 2 (the one authorized old-code question in `Decision 8ac332b4`); `REVISE` (restoring the 2 retired guards) is not required. Per `Decision 8ac332b4`, this single scoped pass does not reset the old-code Security Review cap; any further pass on capped old code requires fresh explicit Maintainer authorization and a specific unresolved security question.

**Findings.** None.

**Coverage.** Inspected committed revisions `4f3887e6`, `a61cec86`, `cbdeca91`, `84e4d9c8`, `58aafbd4`, and `86fad9b0`; read full committed sources at `86fad9b0` for `dev/plans/2026-11-18-release-roster-and-guards.md`, `dev/proposals/archive/2026-11-18-terra-release-roster-and-guards.md`, `tests/security_manifest.py`, `release/security_check.py`, `tests/test_doc_drift_tools.py`, `dev/tools/link_check.py`, `dev/tools/sync_doc_snippets.py`, `tests/test_intents_tool.py`, `tests/test_security_marker.py`, `install/_scaffold/security.py`, `dev/rules/protected-surfaces.md`, and `install/SAFETY.md`; verified all 28 historical `KEPT-BY-RULE` rows from `546959c1~1:dev/measurement/promise-testing-worklist-2026-11-11.csv` against `86fad9b0`. Did not re-execute the test suite or touch uncommitted working-tree files.

## Implementation verification

**Mac canonical Python 3.13.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`):**
- `pytest -q tests/test_security_marker.py` (at `cbdeca91`): `29 passed in 28.64s`.
- 15 modified/split roster nodes across 10 files (at `84e4d9c8`): `24 passed, 1 skipped in 16.41s` (skip is Windows-only `test_replacer_reads_rewritten_windows_fragment_after_creation`).
- `tests/test_doc_drift_tools.py` public CLI witness (`test_real_discovery_cli_keeps_broken_file_with_decoy_and_catches_literal_mutant`, parametrized `[link-dev/tools/link_check.py]` and `[snippet-dev/tools/sync_doc_snippets.py]`): `2 passed, 79 deselected in 3.82s`.
- Detached committed-HEAD fixture `tests/test_security_check.py::test_committed_fixture_connects_real_record_and_join_entrypoints` (at `84e4d9c8`): `1 passed, 3 warnings in 26.65s`.
- Post-fix joined `tests/test_security_check.py tests/test_portable_security_sweeps.py` (at `7b502666`): `345 passed, 2 skipped, 3 warnings in 183.44s`; `tests/test_security_lint.py` (at `d7c94919`): `4 passed in 3.13s`.
- Remaining mapped `tests/tier_inventory.py` Boundary B check (at `d7c94919`, `task-8346`): `295 passed, 92 failed, 28 errors in 73.50s` — `test_broad_run_guard.py`, `test_config_module.py`, `test_core_dev_folders.py`, `test_lockfile_provenance.py`, `test_python_floor.py`, `test_scaffold_substrate.py`, and `test_upgrade_lockfile_path_containment.py` passed; the `92 failed` + `28 errors` across `test_gate_manifest.py` (`28 errors, 2 failed`), `test_gate_reanchor.py` (`15 failed`), `test_oracle_activation.py` (`12 failed`), `test_ceremony_review_report.py` (`41 failed`), `test_replacement_tools.py` (`10 failed`), `integration/test_gauge.py` (`11 failed`), and `contract/test_test_tiers.py` (`1 failed, 39 passed`) are pre-existing pre-re-anchor baseline mismatches (`_APPROVED_INITIAL_ROSTER_SHA256`), pre-relocation `bootstrap/`/`tools/`/`scripts/` path references, or pre-existing `tier_inventory.py` linked-tools fixture drift (`git-read-binding-failed`), and pre-existing `tests/test_security_stack.py` (`18 failed, 203 passed` in `task-8084`) also reflects pre-relocation `scripts/`/`tools/` paths.

**Native Windows (`cairn-windows`, Python 3.13.18):**
- 15 modified/split nodes with `[fchmod]` (at `84e4d9c8`): `11 passed, 13 skipped in 15.33s` (all 13 skips are setup-phase `@pytest.mark.skipif` policy skips).
- Pre-existing out-of-scope defect left unmasked/untouched: unparametrized `test_public_seed_gitignore_staging_failure_preserves_destination_and_cleans_owned_temp[write]` failed with `[WinError 32]` because `install/_scaffold/security.py:61-87` (`_stage_exclusive`) calls `tmp.unlink()` in `except BaseException:` before `finally: os.close(fd)`. Note also that Argon (`7bfb2c10`) observed the C2 prose table prefixes `TestGitReadPhysicalBindings::` whereas `tests/security_manifest.py` and `tests/test_doc_drift_tools.py` use module-level node IDs.

**Benefit versus cost**: worth it -- reconciled the 63 nt / 362 posix native release roster, fixed three POSIX fchmod markers and split non-FIFO board checks, preserved the claims fence, and retired 2 redundant helper guards without losing public CLI decoy coverage; cost implementation across 11 files, Mac + cairn-windows verification, Hydrogen Ordinary review, and one authorized Argon Security review pass; remaining burden grouped v0.8 re-anchor, strict release record/join at cut, and the unmasked pre-existing Windows `[WinError 32]` staging defect in `install/_scaffold/security.py:61-87`.

## Implementation closeout -- Coordinator (Antigravity) -- 2026-11-18

C1 (reconciled `63 nt / 362 posix` roster, setup-phase `skipif` conversions, split board checks, `tests/measurements.py` routing), C2 (28 `KEPT-BY-RULE` dispositions verified: 26 retained, 2 `test_doc_drift_tools.py` helper retirements covered by retained public CLI witness; `tests/test_intents_tool.py` single lifted fence preserved), and C3 (Mac, Windows, detached committed-HEAD fixture, Ordinary `86fad9b0` ACCEPT, and Argon Security `7bfb2c10` ACCEPT covering both new changes and Decision `8ac332b4` scope) all held.

- Remaining: Maintainer grouped v0.8 re-anchor of `tests/security_manifest.py` (`sha256:de890081...`) and release baseline (`test_gate_manifest.py` / `test_gate_reanchor.py`); strict Mac/Windows record/join with Windows `gitleaks`/`bandit`/`vermin` installed; pre-existing `[WinError 32]` staging defect in `install/_scaffold/security.py:61-87`. Home: `dev/PLANNING.md` ("Completed repairs awaiting the trust operation" and release preparation rows).
- Not run: Whole-suite certification (`CAIRN_FULL_SUITE=1`) and pre-existing relocation/baseline test repairs (`tests/test_security_stack.py`, `test_oracle_activation.py`, `test_ceremony_review_report.py`, `test_replacement_tools.py`, `test_gauge.py`, `test_reference_scripts.py`, `test_git_read_routes.py`, `test_quality_gate_neutrality.py`). Home: separate release cut and relocation backlog in `dev/PLANNING.md`.

Dispositions: `accept` (26 retained guards + 2 verified retirements under `8ac332b4`; single claims fence intact); `guard (tests/test_security_marker.py:29)` (fixed `CAIRN_ROOT` in `cbdeca91`). Pre-existing out-of-scope `[WinError 32]` in `install/_scaffold/security.py:61-87` left untouched/unmasked for Maintainer disposition in `dev/PLANNING.md`.

**Elapsed**: unknown
**Tokens**: unknown
