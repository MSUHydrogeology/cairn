# ast_pin.py handoff

**What it does.** Corrects the AST fixtures that `repin` refuses to pin because four baseline symbols
were deleted by commit fa86e2cb. In a throwaway detached git worktree it removes exactly those four
keys, commits that there, and lets `repin package` compute the corrected fixtures. It then holds
repin's transaction to what `repin status` lists in the real repo (same symbols, by name), confirms
each deletion (absent from the engine at HEAD; last touched by fa86e2cb; present in its parent), and
runs `_ast_attest verify --known-new` with the corrected files. It refuses, writing nothing, on any
mismatch. The dry run is the default. `--apply` writes only the two fixture files (atomic replace;
HEAD's bytes restored if the re-check fails), re-runs verify and `test_ast_attest.py`, and prints the
`git commit` command. It never commits, signs, or loads a key.

**Run.** From the repo: `python3.13 ast_pin.py` (dry run), then `python3.13 ast_pin.py --apply`.
`python3.13` is not on this machine's PATH; I used /Users/kendal30/conda_envs/lhm/bin/python3.13.

**Note.** `repin status` lists 21 CHANGED symbols, not 22 (counted by hand and by the script).
The scratch commit leaves one unreachable object in the real repo's `.git`; the worktree is removed.

**Tested (9 tests, scratch clones only, 24 s).** Untouched clone: dry run passes, nothing changes.
Fifth missing symbol: refused. Wrong deleting commit: refused. Transaction tampered (lockfile output,
extra known-new key, altered unrelated baseline entry): each refused. Control: the checker rejects
the old fixtures. Apply in a clone: exactly two modified files, verify reports 169 symbols OK,
printed digests equal the files', not committed. Apply refused when a fixture is already edited.
Real repo `git status` and worktree list are the same before and after.

**Not tested.** `--apply` on the real repo; the post-apply restore branch; full test suite; any
Python other than 3.13.13.

## Dry run against the real repo
```
Four baseline symbols were deleted from the engine, and each deletion checks out:
  Assign:_ONBOARDING_HELPER_DST_REL: absent from the engine at HEAD; last touched by fa86e2cb59, which removed it
  Assign:_ONBOARDING_HELPER_SRC_REL: absent from the engine at HEAD; last touched by fa86e2cb59, which removed it
  Assign:_ONBOARDING_LOG_HEADER: absent from the engine at HEAD; last touched by fa86e2cb59, which removed it
  Assign:_ONBOARDING_LOG_REL: absent from the engine at HEAD; last touched by fa86e2cb59, which removed it

Baseline keys: 173 before, 169 after (the four deleted ones removed).
Updated baseline entries (CHANGED): 21   known-new ADDED 23, REKEYED 7, DROPPED 4
These counts and the symbol names are IDENTICAL to what `repin status` lists: YES (checked by name).
  changed: Assign:_CORE_MAPPINGS, Assign:_KIND_DISPLAY_LABEL, FunctionDef:_apply_upgrade, FunctionDef:_behind_by_n, FunctionDef:_cmd_finalize_lockfile, FunctionDef:_cmd_init_lock, FunctionDef:_compute_upgrade, FunctionDef:_dirty_tracked_paths, FunctionDef:_print_upgrade_report, FunctionDef:_render_onboarding_slot, FunctionDef:_resolve_vendor_wrapper, FunctionDef:_self_heal_profile_config, FunctionDef:_write_init_lock_profile_template, FunctionDef:_writeset_dirty_collisions, FunctionDef:cmd_upgrade, FunctionDef:install_manifest, FunctionDef:install_onboarding, FunctionDef:main, FunctionDef:merge_file, FunctionDef:print_report, FunctionDef:write_install_lockfile
  rekeyed: Assign:_BLOCKED_ADDITION_KINDS, FunctionDef:_assert_mapping_ownership, FunctionDef:_check_lockfile_paths, FunctionDef:_cmd_adopt_collisions, FunctionDef:_contained_lockfile_path, FunctionDef:_lockfile_refusal, FunctionDef:duplicate_destinations
  added: Assign:_EDIT_CHECK_GROUP_SIZE, Assign:_GIT_FLOOR_MET, Assign:_GIT_NOT_STARTED, Assign:_GIT_NO_ANSWER, Assign:_GIT_TIMEOUT_SECONDS, Assign:_RETIRED_INSTALLS, ClassDef:_EditCheckCannotTell, FunctionDef:_ask_git, FunctionDef:_cannot_tell_refusal, FunctionDef:_classify_retired_records, FunctionDef:_cmd_remove_retired, FunctionDef:_committed_copy_matches, FunctionDef:_disk_dst, FunctionDef:_edit_check_prelude, FunctionDef:_finalize_hash_names, FunctionDef:_git_config_bool, FunctionDef:_git_floor_met, FunctionDef:_git_in_project, FunctionDef:_linked_vendor_wrapper_names, FunctionDef:_refuse_if_linked, FunctionDef:_remove_unchanged_file, FunctionDef:_run_git_sterile, FunctionDef:_working_file_differs
  dropped: Assign:_ALWAYS_ON_MAPPINGS, FunctionDef:_always_on_group_complete, FunctionDef:assert_always_on_complete, FunctionDef:missing_always_on_sources

Corrected fixtures (sha256):
  ce501a096e185592aeda8a1d15061fcf3d0b5da34939805daf5ca9ee4c2cbdfb  bootstrap/tests/fixtures/scaffold_ast_baseline.json
  6e8c03ddae6d1190f6baf74d0f22e249d410c0498b8e173f878307b341956872  bootstrap/tests/fixtures/scaffold_ast_known_new.json

In a scratch copy with these fixtures: AST attestation OK — 169 baselined symbol(s) accounted for, unchanged.

DRY RUN: nothing was written. Run again with --apply to write the two fixtures.
```
