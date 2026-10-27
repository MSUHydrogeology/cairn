# Plan: the upgrade edit check runs no program from the project's git settings

**Author**: Claude Sonnet 5.5 (Strategy)
**Source proposal**: [dev/proposals/archive/2026-10-26-claude-upgrade-dirty-check-runs-no-repository-programs.md](../proposals/archive/2026-10-26-claude-upgrade-dirty-check-runs-no-repository-programs.md)
**Status**: awaiting-plan-review
**Waiting on Maintainer**: re-anchor at the cut (C8, MAINTAINER-ONLY)
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-27
**In brief**: `upgrade --stage`, `--apply` and a bare `--finalize` stop running programs that a project's git settings name when they check for unsaved edits, and they read a project that sits in a repository subfolder correctly.

The Internal Security Review is a separate pass from the ordinary plan review, and the ordinary pass never clears it. This is the second engine change that calls git on a project's behalf, and it reuses the first one's launcher.

## Source proposal

Accepted 2026-10-27 as revised. **Revision 2 is the complete contract** and supersedes Revision 1. The Maintainer's answers: bare `--finalize` asks git only about the files it hashes plus the lockfile; where git settings ask for CRLF, a line-ending-only difference counts as unchanged; when git does not answer, `--apply` and `--finalize` stop (naming the reason and `--force`) and `--stage` only warns. No new action, flag or list; `--force` runs no git; the `--apply` refusal text stays byte-identical.

## Scope

**In.** Revision 2's items 1 to 10, as the chunks below, all in `bootstrap/_scaffold/upgrade.py` plus prose. **Out.** `bootstrap/_scaffold/security.py` (no chunk edits it; its guards are only called), `install.py` near 1648 (its `git status` feeds a warning that never blocks), the lockfile format, templates, the published `scaffold.py --manifest`, pushing, and `scaffold_ast_known_new.json`, the AST baseline, `bootstrap/tests/fixtures/gate_manifest.json` and `refs/cairn/gate-anchor` (the implementer never edits or moves them).

**Order.** Starts from the tip after the twelfth change's archive (`98861a90`). C1 to C7 are in order; C5 and C6 land back to back, because between them a renamed vendor wrapper is asked about by its recorded name (never released; the reviewer reads C5 to C6 as one range).

**Reuse.** Searched `git grep -n 'subprocess\.\(run\|Popen\|check_output\)' -- bootstrap/_scaffold`: eight hits in four files; the one sterile launcher is the `run_git` inside `_committed_copy_matches` (`upgrade.py`), which C1 lifts to module level and C4 and C5 call. Searched `git grep -n -i 'autocrlf\|hash-object\|ls-files\|diff-index\|literal-pathspecs' -- bootstrap tools scripts templates/skills`: `scripts/repin.py` and `bootstrap/security_check.py` hash through `git hash-object` (reads the working file, so it can run a filter; and both sit outside the engine package, which is standard-library-only), and `scripts/content_scan_runner.py` already uses `--literal-pathspecs`; none is importable, so the blob hash is written in Python (`hashlib`). Reused as they are: `_read_regular_bytes` and `_assert_safe_write` (`security.py`; called, not edited), `_classify_retired_records`, `_LIVING_STATE_DSTS`, `_resolve_vendor_wrapper`, `_GIT_TIMEOUT_SECONDS`, the `.git` environment scrub. New: a module-level launcher and one floor cache, a working-file comparison, a prelude (steps a to e), a names helper for bare `--finalize`.

**Doctrine surface.** Descriptive layer only: `bootstrap/SAFETY.md`, `bootstrap/UPGRADE.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md`, and the `--help` text. `CHANGELOG.md` and `dev/PLANNING.md` are the planning session's, at archive. No `doctrine/` or `AGENTS.md` text; the rate-limit gate does not apply.

Proposed paths:
* `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py`

**Frozen files, derived** on 2026-10-27 from the globs in `_frozen_files` (`bootstrap/tests/_gate_manifest.py`), the 195 `frozen_files` keys of `bootstrap/tests/fixtures/gate_manifest.json`, and a read-only `python bootstrap/tests/_gate_manifest.py verify --no-collect`. "Owes a re-anchor" would mean this plan adds an entry; none does. The planning session re-derives at the cut.

| File | Chunk | Effect |
|---|---|---|
| `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py` (new) | C2-C6 | glob match, no key: `FROZEN-NEW`, allowed |
| `bootstrap/tests/test_upgrade_removes_retired_files.py` | C1, C6 | glob match, **not keyed** (it prints `FROZEN-NEW` today): edits free; if a cut keys it first, re-anchor owed (check at landing) |
| `test_upgrade.py` (`TestDirtyTreeGuard`, `TestFinalizeDirtyTreeGuard`, `test_self_heal_composes_with_dirty_tree_guard`), `_oracle.py`, `test_oracle.py`, `test_upgrade_side_door_parity.py`, `test_upgrade_module.py`, `test_upgrade_module_additions.py`, `test_agreement_retired.py`, `test_security_leaf.py`, `test_upgrade_lockfile_path_containment.py`, `test_security_lint.py`, `test_verify_integrity.py`, `test_review_stance_in_shipped_files.py` | all | keyed, **not edited** (read at this tree: each stays green under the contract; the one-argument helper call keeps working because `names` defaults); scoped runs only |
| `test_next_session_local_note.py`, `test_install_time_onboarding.py`, `test_upgrade_refuses_hostile_project_data.py`, `test_upgrade_added_slots.py` | C7 | unkeyed; edited only if C7 finds a pinned sentence (none found today) |
| `bootstrap/security_check.py`, `bootstrap/scaffold.py` | none | keyed; if the Bandit gate wants an allowlist edit there, stop and ask the Maintainer |
| `bootstrap/_scaffold/*.py` | C1-C6 | not frozen (subfolder); AST-attested; the whole directory is on the oracle roster |

## Sequence

How to work: directly on `0.5-dev`, commit by explicit path. **Every chunk's first criterion:** `python tools/intent.py list` shows no other claim on its files; if one does, report to the planning session and wait. Test names state the property; all new nodes are in the new test file unless named otherwise. Every node passes on the unmutated tree (the control); a **mutant** is one deliberate break in its own detached worktree beside that control, and a skipped node counts as survived (`pytest -rs`).

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Lift the launcher; one floor cache | none | refactor, no behaviour change |
| C2 | The working-file comparison `_working_file_differs` | none | bytes, mode, line endings, links |
| C3 | The "cannot tell" answer and the three callers' handling | none | stop / advise, `--force` |
| C4 | The prelude: `.git` look, version, work tree, config, partial clones | none | steps a to e |
| C5 | The check itself: `_dirty_tracked_paths(target, names=None)` | none | steps f and g, groups, verdict |
| C6 | Bare `--finalize` asks about what it hashes plus the lockfile | none | `_finalize_hash_names` |
| C7 | `SAFETY.md`, `SECURITY_MUTATIONS.md`, `UPGRADE.md`, `--help` | none | descriptive prose |
| C8 | AST attestation and gate-manifest re-anchors at the cut | **MAINTAINER-ONLY**, not for an agent | re-pinned checksums |

## Acceptance criteria

**C1.**
* The sterile launcher (environment scrub, `GIT_NO_LAZY_FETCH=1`, `GIT_TERMINAL_PROMPT=0`, `GIT_OPTIONAL_LOCKS=0`, no input, `_GIT_TIMEOUT_SECONDS`, a byte cap, no stderr) becomes one module-level function in `upgrade.py`, `_run_git_sterile(args, limit)`, and the version floor one module-level cache read by `_git_floor_met()` (2.45.0, unreadable version fails). `_committed_copy_matches` calls both and behaves as before.
* Control: `pytest bootstrap/tests/test_upgrade_removes_retired_files.py` passes before the move and after it, every git node unedited except the reset helper `_reset_git_floor`, which now resets the one cache (`monkeypatch.setattr(U, "_GIT_FLOOR_MET", None)`). `git grep -n 'git_floor_met' -- bootstrap` finds only the function name `_git_floor_met`; before the move it finds the attribute (control).
* `_version_answer` in that file also asserts that `--version` was the first logged call. Mutant: leave the old reset line (the cache is then not reset and the stand-in node goes red depending on order).
* `git grep -n 'subprocess.Popen' -- bootstrap/_scaffold/upgrade.py` finds one launcher. `pytest bootstrap/tests/test_security_lint.py` passes with no allowlist edit.
* Boundary A: that file, `test_security_lint`, `test_security_leaf`; owners by `git grep -l '_committed_copy_matches\|_GIT_TIMEOUT_SECONDS' -- bootstrap/tests`.

**C2.**
* `_working_file_differs(project, name, index_mode, index_id, check_mode, fold_crlf)` returns whether the working file counts as edited, reading nothing through git: `_assert_safe_write` first (a link at the name or above it counts as edited, never followed), then `_read_regular_bytes` (no link, no blocking on a FIFO). Edited if: missing, not a regular file, index mode not 100644 or 100755, bytes (hashed as git hashes a blob, SHA-1 or SHA-256 by the id's length) differ from the id, or the owner-execute bit differs from the index mode (POSIX only, only when `check_mode`). With `fold_crlf`, bytes equal after turning `\r\n` into `\n` count as unchanged.
* `test_a_link_in_the_path_counts_as_edited_and_a_fifo_does_not_block` (a link at the name, a linked parent, a FIFO bounded by a watchdog in the node). Mutant: read with `Path.read_bytes`.
* `test_a_file_is_hashed_the_way_git_hashes_a_blob` (the expectation is `git hash-object` on the same bytes, SHA-1, and SHA-256 in a repository made with `--object-format=sha256`; a git without that option skips the second arm and says so). Mutant: always SHA-1.
* `test_a_mode_only_edit_counts_unless_filemode_is_off` (index 100755 against the bit; group-execute only; `check_mode` false). Mutant: skip the mode.
* `test_line_endings_difference_counts_as_unchanged_only_when_asked` (mutant: always fold). `test_an_index_entry_that_is_not_a_plain_file_is_edited` (mode 120000 and 160000; mutant: accept any mode).
* Boundary A: the new nodes, `test_security_leaf`, `test_upgrade_lockfile_path_containment`; owners by `git grep -l '_assert_safe_write\|_read_regular_bytes' -- bootstrap/tests`.

**C3.**
* `_EditCheckCannotTell(reason)` (an exception; the reason is a fixed engine sentence, never git's output) is what the check raises for Revision 2 item 8. The three callers handle it: `_apply_upgrade` step (f) and bare `--finalize` print the reason, name `--force`, and exit 1 without writing; `upgrade --stage` completes (exit 0) with an `[advisory]` line on stderr. The known-dirty `--apply` refusal block is unchanged byte for byte. `_writeset_dirty_collisions` lets the exception through.
* `test_each_caller_stops_or_advises_when_the_check_cannot_tell` (the helper patched to raise, driven through `scaffold.py upgrade`; asserts exit code, the reason text, the word `--force`, and for `--stage` exit 0 plus the advisory). Mutants, one per caller: apply treats it as clean; finalize treats it as clean; stage refuses instead of advising.
* `test_force_runs_no_git` (a stand-in `git` logs; `--apply --force` and `--finalize --force` log no `ls-files`, `diff-index`, `status` or `--is-inside-work-tree` call). Mutant: run the check under `--force`.
* Control: `TestDirtyTreeGuard` and `TestFinalizeDirtyTreeGuard` pass unedited; the oracle node `test_oracle.py::test_oracle_privileged_workflows_preserved` result is recorded before C1 and again here (it must not get worse).
* Boundary A: the nodes, `test_upgrade.py`, `test_oracle.py`, `test_upgrade_module_additions`, `test_upgrade_side_door_parity`, `test_upgrade_lockfile_path_containment`.

**C4.**
* `_edit_check_prelude(target)` runs, through the C1 launcher with `git -C <project> -c core.fsmonitor=false -c core.hooksPath=<null device> -c core.useReplaceRefs=false`: (a) a filesystem look for a `.git` file or folder in the project folder or any folder above it (no git); (b) the floor; (c) `rev-parse --is-inside-work-tree`; (d) `config -z --get-regexp 'core\.filemode|core\.autocrlf|core\.eol|promisor|partialclone'`; (e) `rev-parse --verify -q HEAD`. It returns `None` ("no guard": git cannot start, or step c fails and (a) found no `.git`), or the facts (`filemode`, `fold_crlf`, whether HEAD exists), or raises `_EditCheckCannotTell`. The config answer follows Revision 2 items 4 and 5 exactly; the plan restates none of its rules.
* `test_a_repository_git_will_not_confirm_is_cannot_tell_and_no_repository_is_no_guard` (`core.bare=true`; a stand-in `git` exiting 128; no `.git` anywhere). Mutant: treat the refusal as no guard.
* `test_the_config_answer_is_read_as_git_reads_it` (no key, valueless, last wins, `filemode = banana`, `eol` other than crlf/lf/native, a config call that fails). Mutant: read exit 1 as an error.
* `test_below_the_floor_a_partial_clone_answers_cannot_tell_and_runs_no_program`: one case per key (`extensions.partialclone`, `remote.origin.promisor`, `remote.origin.partialclonefilter` on a treeless clone with lazy fetch left on, `core.partialclonefilter`), a stand-in `git` reporting 2.44.0 and ignoring `GIT_NO_LAZY_FETCH`; no marker file, and no `rev-parse --verify`, `ls-files` or `diff-index` call logged. Mutants: the three exact key names of Revision 1; remove the config gate.
* `test_the_launcher_is_shared_with_the_committed_copy_check` (argv prefix and environment of the `cat-file` call and of the prelude's calls are equal; mutant: a second copy of the override list in the prelude with `core.useReplaceRefs=false` dropped).
* Boundary A: the nodes and the C1 set.

**C5.**
* `_dirty_tracked_paths(target, names=None)` returns the subset of `names` that is edited, `None` for no guard, or raises. `names=None` is the lockfile's recorded `dst` values, an empty set with no readable lockfile; `git grep -n '_dirty_tracked_paths(' -- bootstrap tools scripts` shows the one-argument call only in `test_upgrade.py` (and `_cmd_finalize_lockfile` until C6). `_writeset_dirty_collisions` passes its write-set. After the prelude: `ls-files -z -s -- <names>` and `diff-index --cached --raw -z --no-renames --no-ext-diff --no-textconv --relative HEAD -- <names>`, with `--literal-pathspecs`, in groups of at most `_EDIT_CHECK_GROUP_SIZE` (100); no HEAD means every tracked name is staged; staged, in conflict, or `_working_file_differs` means edited; a name git does not track is not. Exit 128 from step g (a treeless clone), a timeout, or output past the cap raises. `git status` is no longer called anywhere in `upgrade.py` (`git grep -n "'status'\|\"status\"" -- bootstrap/_scaffold/upgrade.py` prints nothing; control: it prints the old call).
* Nodes, driven through `scaffold.py upgrade --stage|--apply|--finalize` unless a direct call is named: `test_git_config_programs_never_run_during_stage_apply_or_finalize` (monitor, clean filter, textconv, pager; mutant: `status --porcelain` in place of `ls-files`). `test_a_subfolder_project_sees_its_own_edits` (mutant: drop `--relative`). `test_the_check_agrees_with_git_status_on_each_edit_state` (the ten states: modified, staged, staged then reverted, deleted, staged delete, staged add, type change to a link, a name with pattern characters, merge conflict, no commit, plus untracked; git's own `status --porcelain` on a repository with no programs is the expectation; mutant: ignore conflict stages). `test_pattern_characters_in_a_name_match_literally` (mutant: drop `--literal-pathspecs`). `test_a_staged_then_reverted_file_counts_as_edited` (mutant: skip `diff-index`). `test_a_missing_or_untracked_name_is_handled_as_git_status_does`. `test_an_untracked_recorded_name_is_not_returned_and_no_lockfile_gives_an_empty_set` (direct call; carries the property the frozen self-heal node now holds by construction). `test_names_go_in_groups_of_at_most_100` (250 names, a logging stand-in; mutant: one call for all). `test_core_filemode_false_makes_a_mode_only_edit_not_count` (mutant: ignore the key). `test_line_endings_rule_applies_only_when_settings_ask_for_crlf` (`autocrlf` true, `eol=crlf`, neither, `input`; mutant: always fold). `test_a_replace_ref_cannot_hide_a_staged_edit` (mutant: drop `core.useReplaceRefs=false` from the shared prefix).
* `test_a_partial_clone_runs_no_upload_program_at_or_above_the_floor` (blobless and treeless clones with `remote.origin.uploadpack` naming a marker program; treeless answers "cannot tell"; no marker). Mutant: drop `GIT_NO_LAZY_FETCH` from the launcher environment.
* `test_a_git_that_does_not_answer_stops_apply_and_finalize_and_only_advises_on_stage` (a stand-in `git` that sleeps, `_GIT_TIMEOUT_SECONDS` patched to 0.5; the end-to-end partner of C3's node). Mutant: treat the timeout as clean.
* Cost, recorded not gated: 62 names in a scratch repository of 5,000 tracked files, wall time of the check before and after, in the verification record.
* Boundary A: the nodes, the C1 and C3 sets, `test_upgrade_refuses_hostile_project_data`, `test_next_session_local_note`, `test_install_time_onboarding`, `test_agreement_retired`, `test_skills_upgrade`; owners by `git grep -l 'upgrade.*--apply\|--finalize' -- bootstrap/tests`. Oracle: `pytest bootstrap/tests/test_oracle.py::test_oracle_privileged_workflows_preserved`, scenario `dirty_tree_refusal` stays `match`.

**C6.**
* `_finalize_hash_names(target, lock, retired)` returns the names bare `--finalize` asks about: every record with a string `dst`, the vendor wrapper by its on-disk name, minus living-state files, minus retired records not `untouched`, plus `dev/.cairn/cairn-lock.yml`; a recorded file missing on disk stays in. The on-disk-name rule is one helper (`_disk_dst`) called by this function and by the hashing loop in `_cmd_finalize_lockfile`, so the two cannot disagree. The bare call passes these names; the refusal says "recorded" (and the lockfile), not "tracked"; the `--finalize` help text says "recorded".
* `test_bare_finalize_asks_about_the_records_it_hashes_and_the_lockfile`: a dirty living-state file, a hand-deleted retired file and an edited kept retired file each leave the finalize running (exit 0); an edited hashed record, an edited renamed wrapper and a modified lockfile each refuse (exit 1). Mutants, one each: ask about all records; drop the lockfile; name the wrapper by its recorded name.
* In `test_upgrade_removes_retired_files.py` the bare arm of `test_a_hand_deleted_file_is_cleared_by_the_step_or_a_scoped_finalize_and_a_bare_finalize_waits_for_the_commit` now expects exit 0 and a cleared record, and the node is renamed to say so (a collected node id in an unkeyed file; told to the Maintainer at C8).
* `git grep -n '_dirty_tracked_paths(' -- bootstrap tools scripts` shows no production caller that omits `names` (control: it shows `upgrade.py` bare finalize before this chunk).
* Boundary A: the nodes, the C5 set, `test_upgrade_removes_retired_files`, `test_verify_integrity`.

**C7.**
* `bootstrap/SAFETY.md` gets one sentence: the edit check runs no program the project names, and how (fixed overrides, no `git status`, the engine reads the files itself, lazy fetch off). `SECURITY_MUTATIONS.md` Class D gains a `_dirty_tracked_paths` row (what it reads: the index, the last commit, the config through git; each file through `_assert_safe_write` and `_read_regular_bytes`) and the `_committed_copy_matches` row notes the shared launcher and the one floor cache.
* `bootstrap/UPGRADE.md`: the "Deleting by hand is fine" sentence (it says a bare finalize refuses while a deletion is uncommitted; now false), the `--apply` and "Recording an edit you made" paragraphs gain what the check covers (the write-set; for a bare finalize the files it hashes plus the lockfile), its disclosed over-reports (a clean filter, a tracked link, a CRLF checkout set only in `.gitattributes`, a stray empty `.git` folder), its gap (a name in another letter case on a case-insensitive disk), what "cannot tell" means (a partial clone below git 2.45.0, a treeless clone, a repository git refuses, a slow git) and `--force`. `upgrade.py`'s module and function docstrings are brought in line.
* `git grep -n -i 'dirty-tree\|uncommitted\|refuses while' -- bootstrap/UPGRADE.md bootstrap/SAFETY.md` is read sentence by sentence against the code; `git grep -l 'UPGRADE.md' -- bootstrap/tests` lists the pinned readers and each is run (none pins the changed bytes today: measured by `git grep -n 'Deleting by hand\|dirty-tree' -- bootstrap/tests`, which finds only `test_upgrade.py` comments). Boundary A: `check_cairn.py`, `claim_check.py`, `link_check.py`, `quality_gate.py --sub neutrality --sub redundancy`, `test_upgrade_removes_retired_files`, `test_next_session_local_note`, `test_install_time_onboarding`, `test_verify_integrity`, `test_review_stance_in_shipped_files`.

**C8 fence.** The Maintainer's authorization at the cut must name `bootstrap/_scaffold/upgrade.py` and every `bootstrap/_scaffold/` file changed since the anchor (`git diff --name-only refs/cairn/gate-anchor HEAD -- bootstrap/_scaffold/`; the roster entry is the whole directory, so the list is checked, not assumed). Expected AST changed set, from the read-only `python bootstrap/tests/_ast_attest.py verify --known-new bootstrap/tests/fixtures/scaffold_ast_known_new.json bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py` (43 lines today apart from `note:` lines; `_dirty_tracked_paths` and `_writeset_dirty_collisions` match the baseline now): newly CHANGED `_dirty_tracked_paths`, `_writeset_dirty_collisions`; already CHANGED and edited again `_apply_upgrade`, `_cmd_finalize_lockfile`, `cmd_upgrade`; already NEW and edited `_committed_copy_matches`; new `_run_git_sterile`, `_git_floor_met`, `Assign:_GIT_FLOOR_MET`, `_working_file_differs`, `_EditCheckCannotTell`, `_edit_check_prelude`, `_finalize_hash_names`, `_disk_dst`, `Assign:_EDIT_CHECK_GROUP_SIZE`, plus any small helper the implementer splits out. The planning session re-derives this from the verify output at the cut and takes the authorization from that, not from this list. No `_ast_attest` re-anchor is run by an agent. **Guards stay out of the changed set.** `test_ast_attest` is already red, which could hide an edit to a guard. The implementer saves the verify output (without `note:` lines) before C1 and again after C1, C3, C5 and the last commit; the lines naming `_assert_safe_write`, `_read_regular_bytes`, `_stage_exclusive`, `_write_by_replacing`, `_commit_lock_and_caches` and `_check_lockfile_paths` must be identical each time (only `_check_lockfile_paths` appears today), and any other change to them is a deviation. The gate-manifest set is the owed set plus the new test file (`FROZEN-NEW`). Tell the Maintainer at C8: the renamed node in `test_upgrade_removes_retired_files.py` (C6) and the new symbols above. When work reaches C8 the Waiting line stays as written.

**Security Review concerns of the proposal, where each lands.**

| Concern (proposal) | Chunk | Test |
|---|---|---|
| No project program runs (monitor, filters, textconv, pager) | C4, C5 | the programs node; the below-floor and at-floor partial-clone nodes |
| Below-floor key match, any key with `promisor` or `partialclone` | C4 | the below-floor node, four cases |
| Refused repository is "cannot tell", not "no guard" | C3, C4 | the repository-git-will-not-confirm node |
| Line-ending rule only where settings ask | C2, C5 | the fold node; the settings node |
| Reads go through `_read_regular_bytes`; links count as edited | C2 | the link and FIFO node |
| One floor cache; stand-in nodes reset it | C1 | `_version_answer`'s first-call assert |
| Bare finalize asks about its hashed records and the lockfile | C6 | the names node |

## Scope delta

**Scope delta**: preserved. Every outcome of Revision 2 and the Maintainer's three answers is delivered by a chunk above. Against today's behaviour the guard narrows in one place, bare `--finalize` (Question 1, answered by the Maintainer): it no longer refuses on an edit to a file finalize does not hash.

## Verification

**Boundary A** is the mapping under each chunk; the implementer re-finds owners at the landing tree with the `git grep -l` named there, and says so when a surface has none. Standing gates for the engine: `test_security_lint` (the Bandit gate over `bootstrap/_scaffold`; expected: no new finding class, since the launcher moves and `subprocess.run` leaves `_dirty_tracked_paths`), `test_gate_manifest` and `test_ast_attest` (red as before; compared by the guard-lines rule, not by green). Prose chunks run `check_cairn.py`, `claim_check.py`, `link_check.py` and the neutrality and redundancy gates.

**Boundary B mode: `full`.** The change edits the scaffold engine (a high-risk surface), extends the git launcher the twelfth change pinned (a trust-ceremony surface) and changes `cmd_upgrade`'s help and refusal behaviour, so bounded mode refuses. The record is scoped: `**Certified by**: pending` until the next certifying run on a clean committed tree under Python 3.13.x (`/Users/kendal30/conda_envs/lhm/bin/python3.13`). **Nobody sets `CAIRN_FULL_SUITE=1`.** After the last implementation commit the implementer appends `## Implementation verification -- <agent> -- <date>` with the template's fields, the AST guard-lines comparison, the gate-manifest list, the cost smoke and the oracle result, and the interpreter beside every figure. The implementer never runs a re-anchor.

**Not measured by this plan, so named for the reviewer:** a real git older than 2.53.0 (the below-floor nodes use a stand-in that lies about its version and ignores `GIT_NO_LAZY_FETCH`), Windows (null device, CRLF checkouts, bare-`git` lookup), SHA-256 beyond the one hash node, submodules, sparse checkouts and linked work trees, a hung git beyond the stand-in.

**What the code reviewer should attack.** Anything that makes git read a blob, a tree or a working file it did not before (a treeless clone on a real git; a config key the regexp misses); a "clean" answer where `git status` says edited outside the disclosed gaps (staged then reverted, mode-only, a replace ref, a name with pattern characters, a link above the name); "no guard" where the answer should be "cannot tell" (a repository owned by another user, `core.bare=true`); `--force` running any git; the bare-finalize name set (list it from the tree: every `rec` kind the loop skips or hashes) against what the loop does; byte-identical `--apply` refusal; the guard-lines comparison. Each mutant in its own copy beside a control; list each set (call sites of the launcher, the three callers) from the tree, not the diff.

The archive commit (the planning session) writes the `CHANGELOG.md` entry and updates the `dev/PLANNING.md` row, which still cites the proposal's old path.
