# Plan: upgrade removes untouched copies of retired files

**Author**: Claude Sonnet 5.5 (Strategy)
**Source proposal**: [dev/proposals/archive/2026-10-26-claude-upgrade-removes-untouched-retired-files.md](../proposals/archive/2026-10-26-claude-upgrade-removes-untouched-retired-files.md)
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-26
**In brief**: A new `upgrade` step deletes retired Cairn files that a project never edited and clears the records of ones it already deleted, so tidying up no longer breaks `--finalize` or the integrity check.

The Internal Security Review is a separate pass from the ordinary plan review, and the ordinary pass never clears it. This is the first engine code that deletes a file in a project.

## Source proposal

Accepted 2026-10-26 as revised, with all five defaults. **Revision 2 is the contract** and supersedes Revision 1; it adopts the Security Review's conditions SR1 to SR5 and recommendations R1, R2. One new action, `upgrade --remove-retired`, and one engine list of 30 retired files with the SHA-256 digests (fingerprints) of every version Cairn shipped. A copy is removed only if its bytes match a digest and git's last commit holds the same bytes. Anything else is kept and named. `--plan`, the step and `--finalize` share one classifier.

## Scope

**In.** Revision 2's Proposals 1 to 8, as the chunks below. **Out.** The fix of `_dirty_tracked_paths` (the thirteenth 0.5 row, which reuses `_committed_copy_matches`), untracked leftovers, `verify_integrity.py`, the lockfile format, templates, the install, pushing, and `scaffold_ast_known_new.json`, the AST baseline, `bootstrap/tests/fixtures/gate_manifest.json` and `refs/cairn/gate-anchor` (the implementer never edits or moves them).

**Order.** This change lands third: after the NEXT_SESSION plan (`dev/plans/next-session-local-note.md`) and the onboarding plan, and before the thirteenth row. No chunk starts until both earlier plans' last implementation commits are in. **Red interval, accepted by the planning session:** once onboarding deletes Cairn's own nine files, `verify_integrity --target .` shows 9 `missing:` lines (21 `modified` and 9, against 23 and 0 before) until this lands. C7 records the counts. If this change misses the 0.5 cut, the Maintainer re-decides.

**Reuse.** Searched `git grep -n -E 'unlink|rmdir|rmtree|os\.remove' -- bootstrap/_scaffold` (finds only cleanup of the review area, temporary files and the skills link, none a tracked file, so no deleter exists; the pattern can match because those uses are hits) and `git grep -l 'removed-upstream' -- bootstrap tools scripts docs` (the engine, `UPGRADE.md`, two tests). Reused as they are: `_check_lockfile_paths`, `_assert_safe_write`, `_read_regular_bytes`, `_write_by_replacing`, `_sha256_hex`, and the rebuild calls in `_compute_upgrade` for a Markdown copy. New: the list, `_classify_retired_records`, `_committed_copy_matches`, `_cmd_remove_retired`, `_remove_unchanged_file`. `_dirty_tracked_paths` is not reused (SR1).

**Doctrine surface.** Descriptive layer only: `bootstrap/UPGRADE.md`, `bootstrap/SAFETY.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md`, `docs/release-process.md`, `CHANGELOG.md`. No governing doctrine. Rate-limit gate: not engaged (Decision, answer 5).

**Frozen files, derived** from the globs in `_frozen_files` (`bootstrap/tests/_gate_manifest.py:339`) and the `frozen_files` keys of `bootstrap/tests/fixtures/gate_manifest.json` on 2026-10-26. "Owes a re-anchor" means this plan adds an entry; the planning session re-derives every set at the cut with `python bootstrap/tests/_gate_manifest.py verify`.

| File | Chunk | Effect |
|---|---|---|
| `bootstrap/tests/test_upgrade_removes_retired_files.py` (new) | C1-C7 | glob match, no key: `FROZEN-NEW`, allowed |
| `bootstrap/tests/test_security_leaf.py` | C2 | keyed, edited: re-anchor owed |
| `bootstrap/tests/test_agreement_retired.py` | C3, C5 | keyed, edited (the two assertions the Decision names): re-anchor owed |
| `bootstrap/tests/test_upgrade_lockfile_path_containment.py` | C4 | keyed, edited (`_ACTIONS`): re-anchor owed |
| the tests the two earlier plans add (`test_next_session_local_note.py`, the onboarding test file) | C3, C7 | unkeyed until the cut: edits free; if a cut keyed them by then, re-anchor owed (check at landing) |
| `test_upgrade.py`, `test_upgrade_module.py`, `test_upgrade_module_additions.py`, `test_upgrade_side_door_parity.py`, `test_skills_upgrade.py`, `test_verify_integrity.py`, `test_review_stance_in_shipped_files.py` | all | keyed, not edited; scoped runs |
| `bootstrap/_scaffold/*.py` | C1-C5 | not frozen (subfolder); AST-attested; `config.py` is on the oracle roster (`bootstrap/tests/_oracle_activation.py:34-37`) |

Proposed paths:
* `bootstrap/tests/test_upgrade_removes_retired_files.py`

## Sequence

How to work: directly on `0.5-dev`, commit by explicit path. **Every chunk's first criterion:** `python tools/intent.py list` shows no other claim on the chunk's files; if one does, report to the planning session and wait. Order is C1 to C7; C8 is the Maintainer's. Test names state the property; all nodes are in the new test file unless named otherwise.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | The list: `_RETIRED_INSTALLS` in `config.py`; the release-line sentence in `docs/release-process.md` | none | 30 rows with digests, engine data |
| C2 | The two primitives: `_committed_copy_matches` and `_remove_unchanged_file`; the leaf test | none | git call, folder-handle delete |
| C3 | The classifier and `--plan`: `_classify_retired_records`, `_compute_upgrade`, `_KIND_DISPLAY_LABEL`, `_print_upgrade_report` | none | three kinds, `--plan` output |
| C4 | The step: `_cmd_remove_retired`, `cmd_upgrade` | none | `--remove-retired` |
| C5 | `--finalize`: `_cmd_finalize_lockfile` | none | clear, skip, count |
| C6 | `bootstrap/SAFETY.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md`, the `--help` text | none | descriptive prose |
| C7 | `bootstrap/UPGRADE.md` section and stale sentences; the run on Cairn's own tree | none | adopter guide, proof tree |
| C8 | AST attestation and gate-manifest re-anchors at the cut | **MAINTAINER-ONLY**, not for an agent | re-pinned checksums |

## Acceptance criteria

Each criterion names a test or command and has a control that passes. Mutants run each in its own copy of the tree beside an unmutated control (Revision 2, "Tests required", lists them); the code reviewer's ledger repeats them.

**C1.**
* The list has one row per pair in the published manifest of v0.3.0 or v0.4.0 whose `dst` the landing tree no longer ships, plus the ten files the two earlier plans retire. **Re-derive before editing, do not carry the 30, the 23 scripts, the 7 Markdown files or the 55 digests forward.** Pairs: `git archive` each tag into a fresh folder and run `python bootstrap/scaffold.py --manifest` there; drop the pairs the landing tree's manifest still has. Digests, for each template: `git cat-file blob <rev>:<template>` hashed with SHA-256, for `v0.3.0`, `v0.4.0` and the parent of the commit that deleted it (`git log --diff-filter=D -1 --format=%h -- <template>`; for the ten files, the commit the earlier plans made). Keep each distinct digest once, with the first revision that has it. Raw template bytes for Markdown, script bytes for scripts.
* `test_no_retired_row_is_still_shipped_and_every_row_has_digests` (no `src` under `templates/`, no `dst` among `install_manifest()` destinations, every digest 64 hex). Mutant: add a shipped row.
* `test_every_retired_digest_recomputes_from_git_history` (R1): each digest equals the hash of `git cat-file blob <its rev>:<template>` in Cairn's checkout; skipped, with the reason printed, where history lacks the revision. Mutant: corrupt a digest.
* `grep -n 'diff-filter=D' docs/release-process.md` finds the person's line under "Checks to run": run `git diff --name-status --diff-filter=D <previous-tag> <new-tag> -- templates` and add a row for each deleted template an install could have written. Control: that command from v0.3.0 to v0.4.0 lists 20 templates, the agreement among them. Nothing fires it but the person; the sentence says so.
* Boundary A: the new nodes; `test_manifest`, `test_scaffold`, `test_lockfile_module`; `check_cairn.py`, `claim_check.py` on the prose. Search `git grep -l '_CORE_MAPPINGS\|install_manifest' -- bootstrap/tests` for further owners.

**C2.**
* `_committed_copy_matches(project_root, rel_path, data)` is a function of its own, importable by the later row. It runs `git -C <project> -c core.fsmonitor=false -c core.hooksPath=<null device> -c core.useReplaceRefs=false cat-file blob HEAD:./<rel_path>` with every `GIT_*` variable removed and `GIT_NO_LAZY_FETCH=1`, `GIT_TERMINAL_PROMPT=0`, `GIT_OPTIONAL_LOCKS=0` added, no input, a timeout; it passes only on exit 0 and exactly `data`. `test_committed_copy_matches_runs_git_with_fixed_overrides_and_environment` captures argv and environment. Mutants: call `git status`; drop `GIT_NO_LAZY_FETCH`.
* `test_a_git_older_than_2_45_or_unreadable_keeps_the_file_and_runs_no_cat_file`: the step reads `git --version` once per run; below 2.45.0 or unreadable is "cannot tell". Control: 2.45.0 passes.
* `_remove_unchanged_file` calls `_assert_safe_write`, then, where `os.unlink` accepts `dir_fd`, opens the project folder and each folder down to the file one level at a time without following links, and reads, checks and unlinks by name through the last handle; an emptied-folder removal uses the same handles and never goes above the row's own folder. By path on Windows. Nodes: `test_a_parent_swapped_for_a_link_between_the_check_and_the_removal_leaves_the_outside_file` (the swap runs inside a patched guard call; mutant: remove by path; skipped where `dir_fd` is absent, and said so); `test_a_link_a_linked_folder_and_a_folder_in_place_are_kept`; `test_bytes_changed_between_the_decision_and_the_removal_are_kept` (mutant: skip the second read); `test_an_emptied_folder_goes_and_a_non_empty_one_stays` (mutant: remove recursively).
* `_cmd_remove_retired` and `_remove_unchanged_file` join `_GUARDED_WRITE_FUNCS` in `test_security_leaf.py`; `test_guarded_write_functions_still_call_a_containment_guard` passes and fails when either loses its direct guard call.
* Boundary A: the nodes, `test_security_leaf`, `test_upgrade_lockfile_path_containment`; search `git grep -l '_assert_safe_write\|_read_regular_bytes' -- bootstrap/tests` for owners.

**C3.**
* `_classify_retired_records` sorts each record into untouched, gone, matches none, cannot tell, blocked (Revision 2, Proposal 3), for `--plan`, the step and `--finalize`, and never reads through a link. A record is retired only if its `src` and `dst` equal a row and its template is absent from the running tree.
* `test_a_planted_record_for_a_plain_project_file_is_never_retired` (mutant: delete the list check). `test_an_edit_after_init_lock_and_a_bare_finalize_is_kept` (mutant: use `base_hash`). `test_an_untouched_markdown_copy_is_untouched_one_added_line_or_a_migrated_lockfile_is_cannot_tell` (mutant: skip the digest check). `test_a_base_cache_that_is_not_the_rows_is_cannot_tell` (SR3; mutant: use the record's value). `test_a_dangling_link_a_folder_and_a_linked_parent_are_blocked_not_gone` (SR4; mutant: `is_file()` as the test).
* `test_plan_names_each_retired_state_in_fixed_words`: `--plan` prints *retired, untouched*, *retired, already deleted*, *retired, kept* in place of `removed-upstream` for list records; each kept file has its own `[flag]` line ("matches none of the versions this Cairn knows" or "cannot show it is unchanged", R2); unlisted `removed-upstream` records print as today; the report ends with the command; names are the row's, never the record's or git's output. `test_plan_writes_nothing_and_a_folder_at_a_retired_name_does_not_crash_it`.
* `--stage` and `--apply` treat the new kinds as they treat `removed-upstream` (`_ADVANCING_KINDS` unchanged): `test_stage_and_apply_leave_retired_files_and_records_alone`.
* The two assertions in `test_agreement_retired.py` and the `removed-upstream 1:` assertion in the NEXT_SESSION plan's test file change to the new kinds. In `test_agreement_retired.py` the first becomes one *retired, kept* line for the agreement (no cached template: "cannot show it is unchanged"); the second, which now gets exit 0 and a cleared record, lands with C5.
* Boundary A: the nodes above, `test_agreement_retired`, `test_upgrade`, `test_upgrade_module`, `test_upgrade_module_additions`, `test_upgrade_side_door_parity`, `test_skills_upgrade`, `test_upgrade_added_slots`, `test_upgrade_refuses_hostile_project_data`; search `git grep -l '_compute_upgrade\|_KIND_DISPLAY_LABEL\|_print_upgrade_report' -- bootstrap/tests`.

**C4.**
* `test_an_untouched_script_is_removed_its_record_cleared_and_integrity_passes`; `test_an_untouched_markdown_copy_goes_with_its_cache_and_a_gone_one_removes_a_leftover_cache` (file first, cache at `dev/.cairn/base/<row dst>`).
* `test_base_cache_pointed_at_another_file_removes_nothing` (SR3). `test_a_record_is_cleared_only_after_absence_is_confirmed` (SR5a: a removal made to fail, a read-only folder, keeps the record; mutant: clear from the classification). `test_a_stop_before_the_lockfile_write_heals_on_rerun` (mutant: write the lockfile first).
* `test_remove_retired_refuses_to_and_force_with_exit_2` (mutant: accept them); `--remove-retired` joins the mutually exclusive actions (`test_upgrade_lockfile_path_containment.py` `_ACTIONS` gains it, so a hostile record is refused as for the other actions). `test_plan_names_exactly_the_files_the_step_removes` (mutant: let the step remove one more).
* `test_git_config_programs_never_run_during_plan_or_the_step` (SR1): a project whose `.git/config` names a monitor, a clean filter and, in a blobless clone, an upload-pack program runs none, and the copy is kept where git cannot answer. Also `test_a_subfolder_project_keeps_an_edited_tracked_file` and `test_an_uncommitted_or_ignored_copy_is_kept` (mutant: skip the git check).
* One line per record, summary last, says to commit the removal; exit 0 when nothing to do; a kept file is not an error. Boundary A: the nodes, `test_upgrade_lockfile_path_containment`, `test_security_leaf`, `test_verify_integrity`, `test_agreement_retired`.

**C5.**
* `test_a_gone_retired_record_is_cleared_by_bare_finalize` (mutant: restore the refusal). `test_a_blocked_name_still_refuses_bare_finalize_with_exit_1`. `test_a_missing_unlisted_file_and_a_deleted_shipped_file_still_refuse` (mutant: clear any missing record).
* `test_a_copy_matching_no_digest_is_skipped_by_bare_and_force_finalize` (exit 0, `hash` unchanged, name with its state's words; the closing line counts the records not recorded instead of "now attests this tree"; mutants: let `--force` record; keep the old line). `test_scoped_finalize_records_it_and_says_so`. `test_finalize_makes_no_git_call` (a stand-in for the git call fails the node if reached).
* The second assertion in `test_agreement_retired.py` becomes: a bare `--finalize` over a deleted agreement exits 0, clears its record, and `verify_integrity` passes; the node's later steps are rewritten to match.
* Boundary A: the nodes, `test_agreement_retired`, `test_upgrade` (the finalize classes), `test_verify_integrity`, `test_upgrade_lockfile_path_containment`.

**C6.**
* `bootstrap/SAFETY.md` names the delete beside the write in the Layer-4 residual (the Windows by-path window) and names `upgrade --remove-retired` wherever the onboarding change wrote "until the 12th row removes it" (`grep -n '12th row' bootstrap/SAFETY.md` prints nothing afterwards; control: it prints the line before). `SECURITY_MUTATIONS.md` gets the delete in Class A and the classifier's reads and the git call in Class D. One paragraph in `SAFETY.md`; no new rule text beyond the proposal's.
* Boundary A: `check_cairn.py`, `claim_check.py`, `quality_gate.py --sub neutrality --sub redundancy`; `git grep -l 'SECURITY_MUTATIONS\|SAFETY.md' -- bootstrap/tests` for owners (the mutation inventory is read by `test_upgrade_lockfile_path_containment.py` and `test_security_leaf.py`).

**C7.**
* `bootstrap/UPGRADE.md` gets one section, "Files Cairn stopped shipping", in place of the agreement section and the sections the two earlier plans wrote: what `--plan` shows, what the step does, what stays, that a leftover folder holding only `__pycache__` is safe to delete (not tested that Python ignores stale bytecode, and the guide says so), `git restore <path>` brings a file back. It no longer says "do not delete" or "run `verify_integrity` before `--finalize`" for retired files, and the NEXT_SESSION wording about the later cleanup now says what ships. `test_the_upgrade_guide_and_the_printed_line_name_the_same_flag` (S3). The tests that pinned the replaced sentences (the onboarding test file and `test_next_session_local_note.py`; find them with `git grep -l 'UPGRADE.md' -- bootstrap/tests`) are rewritten to match.
* **Own-tree run, a person's check; no test or script runs it.** Before: `python bootstrap/verify_integrity.py --target .` and record the counts (expected 21 `modified`, 9 `missing:`; derived, not carried). Then `upgrade --target . --plan` (expect Cairn's 11 retired records as *already deleted*, or NEXT_SESSION as *kept* if its copy still exists), `--remove-retired`, and commit the lockfile by path. After: the nine `missing:` lines are gone and `modified` is unchanged. Record both counts in the verification record.
* Boundary A: the new node, `test_review_stance_in_shipped_files`, `test_verify_integrity`, `check_cairn.py`, `link_check.py`, `claim_check.py`.

**C8 fence.** The Maintainer's authorization at the cut must name `bootstrap/_scaffold/config.py` (oracle-sensitive roster; the entry is the whole `bootstrap/_scaffold/` directory) and every `bootstrap/_scaffold/` file changed since the anchor, listed at the cut with `git diff --name-only refs/cairn/gate-anchor HEAD -- bootstrap/_scaffold/`; a missed file keeps the gate shut. This plan's AST changed set is the owed set at the landing tree plus `_compute_upgrade`, `_KIND_DISPLAY_LABEL`, `_print_upgrade_report`, `cmd_upgrade`, `_cmd_finalize_lockfile`; new are `Assign:_RETIRED_INSTALLS`, `_classify_retired_records`, `_committed_copy_matches`, `_cmd_remove_retired`, `_remove_unchanged_file`; none dropped or rekeyed. The gate-manifest set is the owed set plus the frozen-files table's "re-anchor owed" rows and the new test file. The implementer never edits the AST fixtures. When work reaches C8, write `**Waiting on Maintainer**: re-anchor at the cut`. `test_ast_attest` is red until then, by design.

**Security Review findings, where each lands.**

| Finding | Chunk | Test |
|---|---|---|
| SR1 sterile git call | C2, C4 | the argv-and-environment node; `test_git_config_programs_never_run_during_plan_or_the_step` |
| SR2 delete through folder handles | C2 | the parent-swapped-for-a-link node; the leaf test |
| SR3 cache path from the row | C3, C4 | `test_a_base_cache_that_is_not_the_rows_is_cannot_tell`; `test_base_cache_pointed_at_another_file_removes_nothing` |
| SR4 "gone" is nothing at the name | C3, C5 | the blocked-not-gone node; `test_a_blocked_name_still_refuses_bare_finalize_with_exit_1` |
| SR5 clear on what happened; `--force` | C4, C5 | the absence-confirmed node; the `--force` nodes; the closing-line node |
| R1 digests recompute | C1 | `test_every_retired_digest_recomputes_from_git_history` |
| R2 words say only what is known | C3 | `test_plan_names_each_retired_state_in_fixed_words` |

## Scope delta

**Scope delta**: preserved. No outcome of Revision 2 is removed. The proposal's Question 1 narrower cut-off (11 files) was offered and not chosen.

## Verification

**Boundary A** is the mapping under each chunk; the implementer re-finds owners at the landing tree by `git grep -l` on the names the chunk touches. A mapped surface with no owner found is said so in the record.

**Boundary B mode: `full`.** The change edits the scaffold engine (a high-risk surface), a contract surface (it extends `cmd_upgrade`'s actions; the lockfile schema, `--manifest` and the fidelity manifest stay unchanged) and a trust-ceremony surface, so bounded mode refuses. The record is scoped: `**Certified by**: pending` until the next certifying run on a clean committed tree under Python 3.13.x. **Nobody sets `CAIRN_FULL_SUITE=1`.** After the last implementation commit the implementer appends `## Implementation verification -- <agent> -- <date>` with the template's fields, the AST and gate-manifest lists C8 names (`test_ast_attest` red until C8, `test_gate_manifest` green), the own-tree counts from C7, and a smoke of `upgrade --plan` and `--remove-retired` over a scratch project. The implementer never runs the re-anchor, and records the interpreter beside every figure.

**What the code reviewer should attack** (one code-review loop). The delete primitive and its race (swap a parent folder for a link; swap the file between the two reads; a link at the name); what the project controls (a lockfile naming another path, a planted `base_cache`, a record whose `src` or `dst` differs from a row by one character or one letter case); the git call (a `.git/config` that names a monitor, a filter or an upload pack; git below 2.45.0; a project in a subfolder); the digest list (a wrong digest keeps a file; a still-shipped row; the re-derivation command run again); record clearing and crash order (a removal that fails; a stop before the lockfile write); `--finalize` (a blocked name, `--force`, the closing line); and that `--plan` and the step agree. Each mutant in its own copy beside a control; list each set (rows, call sites of the classifier) from the tree, not the diff.

The archive commit (the planning session) writes the `CHANGELOG.md` entry, saying what is true at landing.

## Plan review -- Plan reviewer (fresh session, Internal) -- 2026-10-26

**Tier**: Internal
**Model**: Sonnet 5.5, fresh session
**Reviewed commit**: 2ba86e21
**Verdict**: revising-plan. Two blocking findings, nine non-blocking. The Internal Security Review is a separate pass, still owed; this one does not discharge it.

**Foundations**
1. *Does the plan deliver the settled premise?* Yes once B1 and B2 are fixed. Every Revision 2 requirement and SR1-SR5, R1, R2 maps to a chunk and a test with a mutant (plan lines 61-116). The 30 rows check out: archiving v0.3.0 and v0.4.0 and running `scaffold.py --manifest` in each, compared with `HEAD`, drops 21 pairs (20 deleted templates, listed by `git diff --name-status --diff-filter=D v0.3.0 v0.4.0 -- templates`, plus the NEXT_SESSION handoff file); 21 + 9 onboarding = 30.
2. *Simpler path to the same outcomes?* None that keeps every outcome. The list, the delete leaf, the shared classifier and the finalize change are each owed by Decision answers 1-3. I recommend no cut; the one saving is N7 (reuse `_commit_lock_and_caches`, `upgrade.py:1554`, for the lockfile write instead of a second committer).
3. *What result would show it cannot deliver?* `test_guarded_write_functions_still_call_a_containment_guard` red at C2 (B1); `test_next_session_local_note.py` red from C3 to C7 (B2); a row holding the empty-file digest (N2); `verify_integrity --target .` still listing nine `missing:` lines after C7 (`python bootstrap/verify_integrity.py --target .`).

**Findings**
* **B1 -- blocking. C2's guard-set criterion cannot pass at C2.** It adds `_cmd_remove_retired` to `_GUARDED_WRITE_FUNCS` (`test_security_leaf.py:32`), but that function lands in C4, and the test asserts every listed name exists (`test_security_leaf.py:238-240`, "not found in the engine package"). The test also needs a *direct* call by name to `_assert_safe_write` or `_assert_fanout_contained` (`:225-235`); the plan only says the lockfile is written by `_write_by_replacing`, which `_cmd_finalize_lockfile` uses with no direct guard (`upgrade.py:2033`; it is not in the set). Fix: C2 adds only `_remove_unchanged_file`; C4 adds `_cmd_remove_retired` and says it calls `_assert_safe_write` on the lockfile path itself, as `_cmd_adopt_collisions` does.
* **B2 -- blocking. C3's output change breaks tests it does not name.** C3 names one `removed-upstream 1:` assertion in the NEXT_SESSION test file. The tree has three sites there: `test_next_session_local_note.py:426`, `:539` and `:543` (`git grep -n 'removed-upstream' -- bootstrap/tests`; positive control: `test_agreement_retired.py:96` shows). The `:539-543` node also reads the guide, so it fails from C3 until C7 rewrites the guide. The onboarding plan adds a `removed-upstream 9` node too (`dev/plans/install-time-onboarding.md:107`, still a draft). C3's Boundary A lists neither file. Fix: C3 rewrites every hit of that grep at the landing tree, edits the guide's one quoted line in the same commit, and adds both test files to C3's mapping.
* **N1 -- non-blocking. C1 counts the NEXT_SESSION handoff file twice.** It is already in the manifest comparison (the NEXT_SESSION plan's C1 stopped shipping it, `8e6d7484`), so "plus the ten files" adds a duplicate row. Say "plus the nine onboarding files"; the control is 21 + 9 = 30 pairs, 23 scripts, 7 Markdown (measured here).
* **N2 -- non-blocking. A missing blob hashes as the empty file.** For the 20 templates, `git cat-file blob v0.4.0:<template>` fails, and a shell pipeline then hashes nothing: `e3b0c442...`, a real digest that would pass an empty file as Cairn's. The C1 command must stop on a nonzero exit; `test_every_retired_digest_recomputes_from_git_history` must assert exit 0 (add a mutant: a digest for a revision where the template is absent). Also use `%H` (full id), not `%h`, in the deleting-commit command, and make the test fail, not skip, when a tag revision is missing; a rewritten commit id (a re-anchor) would otherwise skip the check forever.
* **N3 -- non-blocking. The release line misses two cases.** `git diff --name-status --diff-filter=D` pairs a delete with an add as a rename by default, and it cannot see a template that stays while its mapping `dst` is dropped. Add `--no-renames` and, as a second line, the C1 manifest comparison. The control stays 20 for v0.3.0 to v0.4.0 (measured).
* **N4 -- non-blocking. The git floor sits outside the reusable function.** The 2.45.0 check is in the step, so the later row's callers of `_committed_copy_matches` can skip the `GIT_NO_LAZY_FETCH` floor SR1 needs. Put the version read inside the function (once per process) and name the file (`upgrade.py` or `security.py`) for each C2 primitive, since the later row imports it.
* **N5 -- non-blocking. The shared classifier's git split and C5(c) are loose.** `--finalize` makes no new git call, so the classifier must return its state before the git gate, with `--plan` and the step adding the gate; say so. C5(c) says "matches no digest", which means nothing for a Markdown copy (its digest is of the cached template): key it on the classifier's state. Rename `test_finalize_makes_no_git_call`: bare `--finalize` already runs `git status` through `_dirty_tracked_paths`; the node should pin that `_committed_copy_matches` is not reached.
* **N6 -- non-blocking. The red-interval figures disagree across plans.** Scope says 23/0 to 21/9; the onboarding plan says 20/0 to 18/9 (its line 26). I measured 20 `modified`, 0 `missing:` today. Drop the figures from Scope; keep "nine `missing:` lines appear", and let C7 record both counts.
* **N7 -- non-blocking. Reuse misses `_commit_lock_and_caches`.** It guards the lock path and writes the lockfile and caches atomically (`upgrade.py:1554`); name it as reused or give the reason it is not. Also add `_cmd_remove_retired` to the `later` tuple in `test_the_upgrade_command_checks_the_lockfile_before_anything_acts_on_it` (`test_upgrade_lockfile_path_containment.py:586`), a file C4 already edits, so a call before the lockfile check fails.
* **N8 -- non-blocking. Two small gaps in C3.** The agreement node's cache exists but is unlisted (`test_agreement_retired.py:45-47`), so the reason is "unlisted cache", not "no cached template" (same words printed). Rule 1's "a cache another record also names" has no node; add one.
* **N9 -- non-blocking. `--plan --to <ref>` is silent.** `removed-upstream` is decided against the ref (`_theirs_bytes`, `upgrade.py:538`); say that "absent" means the running tree for list records and add a node. Also split C2's first bullet; it is one very long sentence for a reader who must check it.

**Checked, no defect.** Frozen derivation: the three edited tests are keyed in `gate_manifest.json`; the new file and the NEXT_SESSION test are unkeyed and match the glob (`_gate_manifest.py:339`, `FROZEN-NEW` at `:669`). The oracle roster entry is `_oracle_activation.py:36-37` (plan says 34-37). C8 is MAINTAINER-ONLY with the files named at the cut. The `12th row` phrase matches the onboarding plan's C6. C7 keeps the heading `test_verify_integrity.py:1439` pins. Reuse search re-run: `unlink` hits are temporary files, the skills link (`install.py:540`) and stage cleanup, so no file deleter exists.

**Coverage.** Covered: lens 1 (probes of tags, manifests, digests, cited lines), 2 (tests drive `scaffold.py main`), 3 (N5, N9), 4 (N2, N4), 5 (B2, N1, N6, N7), 6 (N6), 7 (order, fence), 8 (scope delta preserved), 9 (each finding names its fix). Not covered: no test run; the onboarding plan was read only where it cites this one (still a draft, untracked); the blobless-clone and `dir_fd` race tests were reasoned about, not built; Windows not probed; git behaviour measured on 2.53.0 only; digests recomputed for five templates, not all 55; the Internal Security Review (SR1-SR5 built) is not done here and stays owed.
