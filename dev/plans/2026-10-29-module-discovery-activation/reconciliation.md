# Reconciliation and verification design

## Representation and migration

The installed inventory is dev/modules/README.md (in the installed tree). It contains a clearly
marked generated block, with a stable module ID on each entry. The existing
`onboarding-tasks` slot contains individually marked module task blocks with
the same IDs. Other slot text and preset seed tasks remain outside those
blocks. The shipped module metadata is the single source of purpose, entry
point and task text; its keys must equal `_MODULE_MAPPINGS`. On install the
resolved profile roster is authority; on upgrade the recorded lock `modules`
roster is authority, augmented only by the explicitly requested valid adoption.
Neither inventory nor task text selects modules or authorizes commands.

The clean rendering for that roster, including both generated blocks, is
recorded through the lock's existing clean-base mechanism, distinct from live
adopter bytes. Reconciliation compares each marked entry with its prior clean
entry, accepting a checkbox-only completion as a preserved state. Unchanged
entries update or disappear with the roster; completed or edited entries remain
byte-for-byte if still selected. Duplicate IDs, malformed markers, changed
entries that must disappear, and conflicts in surrounding text refuse with a
named path, module and manual action. A changed entry is never silently
replaced. Fresh output and clean base use the same renderer; independent tests
check roster correctness rather than merely comparing the two.

For a legacy installation, derive selection from the lock roster; never infer it
from files. For each preset seed, recognize only exact shipped historical seed
text (also with its checkbox checked), using an explicit seed-to-module mapping.
A matching seed counts as that module's task and keeps its text and checkbox;
remove it from the new generated set to prevent duplication. Unrelated and
unmatched seeds remain untouched. If a seed plausibly represents a module task
but cannot be identified unambiguously, report a conflict rather than duplicate
or erase it. Where no trustworthy prior base or roster exists, refuse automatic
migration and direct the operator to establish a lock, inspect selection, and
manually reconcile the slot and inventory; retry only after they agree. For an
edited block requiring removal, the remedy is to save its work elsewhere, then
manually remove that block and rerun. Manual copying requires the operator to
add the module with `upgrade --adopt-module`, then follow any reported manual
reconciliation, not merely copy files and assume discovery updated.

## Ordering and containment

Prepare proposed inventory, slot, clean bases, lock and caches together in
memory before their first write. Check marker validity, preservation, target
and parent containment, dangling links and existing write guards first. Initial
and repeated install preflight these artifacts before their generated writes;
this guarantee does not roll back unrelated core or skills writes that occurred
before preflight. Adoption preflights before the module-destination loop and
before the already-recorded shortcut, and commits generated outputs and lock
only after successful preparation. Conflict or containment refusal leaves the
inventory, planning and lock bytes unchanged; it does not promise rollback of
unrelated pre-existing installer writes. Preserve existing commit and cache
safety and report write failures rather than claiming arbitrary crash atomicity.

Upgrade plan and stage carry the proposed changes and their observed input
bytes; apply rechecks containment and compares the current slot, inventory,
lock and relevant destinations with the staged inputs before writing. A change
or conflict after stage refuses and leaves all three generated surfaces
unchanged. Apply existing guarded path and staging mechanisms; no task is run.

## Reviewed public-path map

The following new test names are planned nodes in the named existing files; they
must be implemented and run. The table's sets are minimum inputs, not a claim
that other readers cannot exist.

| Path and invariant | Test home and planned node | Inputs |
|---|---|---|
| Install roster and usable tasks | `bootstrap/tests/test_onboarding_seed_roster.py::test_selected_modules_have_usable_tasks` | preset, explicit all 22, explicit empty, add/remove; independently expected IDs and every inventory row |
| Repeat and historical seeds | `bootstrap/tests/test_onboarding_seed_roster.py::test_repeat_install_preserves_legacy_and_completed_tasks` | pristine, checked, edited and ambiguous seed; repeated install |
| Clean baseline and manifest | `bootstrap/tests/test_module_merge_lockfile.py::test_module_inventory_and_onboarding_match_clean_baseline` | same rosters, live bytes, manifest, lock clean base |
| New and already-recorded adoption | `bootstrap/tests/test_upgrade_module_additions.py::test_adoption_reconciles_tasks_without_losing_edits` | new, repeated, recorded, edited, checked, missing legacy base and manual recovery |
| Upgrade stage/apply and conflict | `bootstrap/tests/test_upgrade_module_additions.py::test_staged_module_discovery_refuses_changed_inputs` | plan/stage/apply, change task or inventory after stage; all three byte snapshots unchanged on refusal |
| Linked and unsafe new destinations | `bootstrap/tests/test_upgrade_lockfile_path_containment.py::test_discovery_paths_refuse_links_on_public_entry` | install, adoption and apply; inventory and planning destination, dangling link and linked parent; snapshots unchanged |
| Manual copy | `bootstrap/tests/test_upgrade_module_additions.py::test_manual_copy_then_adoption_updates_discovery` | copy mapped files, explicit adopt, repeat and conflict remedy |
| Roster metadata completeness | `bootstrap/tests/test_module_roster.py::test_every_module_has_discovery_metadata` | exact mapping keys and every task's installed path/input |

Existing tests in those homes remain mapped, especially
`test_symlinked_destination_after_stage_blocks_apply`, the onboarding live-lock
nodes and `test_a_dst_through_a_folder_link_that_leaves_the_project_is_refused`.
The separate four mutations and their passing controls are run against the
corresponding behavioral tests, with outcomes recorded. Run
`bootstrap/tests/test_security_lint.py` for the engine; its Bandit dependency
and any skip or other non-pass receive a disposition in Boundary B. Search
readers and callers again during implementation and add discovered checks.
