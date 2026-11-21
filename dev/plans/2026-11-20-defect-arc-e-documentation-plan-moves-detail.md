<!-- claim-check-allow: docs/DOCUMENTATION_PLAN.md -->
# Detail for plan E of the defect arc: exact conditions, texts and edits

This file is part of `dev/plans/2026-11-20-defect-arc-e-documentation-plan-moves.md`. It exists because the plan must leave no design to a low-tier implementer, and the exact texts would push the plan well past its word target. The companion is part of the plan.

Paths built: `dev/DOCUMENTATION_PLAN.md` and `tests/test_upgrade_documentation_plan_moved.py` (both exist since the build).

The installer code is merged into `0.9-dev` and was read in the main checkout on 2026-11-21 (HEAD `3fb798f5`; the installer files last changed in `029532a0`, the commit the plan first cited). Line numbers are guides; the function names are the contract.

## D1. Names used by the command

In `install/_scaffold/upgrade.py`, next to `_LAYOUT_LOCK_KEYS`, add module constants:

- `_DOCPLAN_SRC = "modules/default-on/documentation_plan_template.md"` (the lock's `src` for the record).
- `_DOCPLAN_OLD = "docs/DOCUMENTATION_PLAN.md"`.
- `_DOCPLAN_NEW = "dev/DOCUMENTATION_PLAN.md"`.
- `_DOCPLAN_STEPS`, the three step lines below, exactly. The report line (D3), message M6 and the tests use this one constant; `install/UPGRADE.md` carries the same three lines (checked by a test, D5).

```
  1. git mv docs/DOCUMENTATION_PLAN.md dev/DOCUMENTATION_PLAN.md
  2. python install/scaffold.py upgrade --target <repo> --documentation-plan-moved
  3. git add dev/.cairn/cairn-lock.yml, then git commit
```

`<repo>` is the project folder, as in the other upgrade lines; `install/UPGRADE.md` says so. Nothing from the lockfile, the tree or the command line is used as a path to write: the command writes only the lockfile, through `_commit_lock_and_caches`. Only `dst` changes. `base_cache`, `base_hash`, `hash` and every other key stay; the saved ancestor stays where it is.

## D2. The command `upgrade --documentation-plan-moved`

New function `_cmd_documentation_plan_moved(target, templates_root, lock, force) -> int` in `install/_scaffold/upgrade.py`. It is built from plan B's pieces: `_writeset_dirty_collisions`, `_cannot_tell_refusal`, `_commit_lock_and_caches`, `_read_regular_bytes`, `_assert_safe_write`, `_legacy_layout_paths`, `_sha256_hex`. It calls nothing that creates, moves or removes a file or folder. Steps, in this order; the first that applies decides:

1. **Find the record.** `recs = [r for r in lock.get("files") or [] if isinstance(r, dict) and r.get("src") == _DOCPLAN_SRC]` (read `files` only when it is a list).
   - 0 records: print M1, return 0.
   - more than 1: print M2 to stderr, return 1.
   - the one record `rec`: if `rec.get("dst") not in (_DOCPLAN_OLD, _DOCPLAN_NEW)` or `rec.get("verbatim")` is truthy: print M3 to stderr, return 1.
   - If any other record's `dst` is `_DOCPLAN_NEW`: print M3, return 1.
2. **Layout still ahead (only when `rec["dst"] == _DOCPLAN_OLD`).** `ahead = _legacy_layout_paths(target, templates_root)`. If not empty: print M4 with `{n}` = `len(ahead)` to stderr, return 1. (A project from 0.7 has the whole 0.8 move ahead; once finished the list is empty.)
3. **Read both places.** For `target / _DOCPLAN_NEW` then `target / _DOCPLAN_OLD`: `_assert_safe_write(path, target)`, then `data = _read_regular_bytes(path)` (`None` when absent). A link, folder, special file or link above raises `ScaffoldSecurityError`; the caller prints M9 (exit 2) and nothing has been written. Name the results `new` and `old` (`bytes | None`). `single_link` is not set: the command only reads, and a second hard link changes no outcome. Both files are read whole, with no size limit, as every upgrade read (a residual the plan names).
4. **Recorded at the new place (`rec["dst"] == _DOCPLAN_NEW`).** Print M8 (with its second sentence when `old is not None`), return 0. Write nothing.
5. **Recorded at the old place.**
   - `new is None and old is None`: M5, return 1.
   - `new is None` (old only): M6, return 1.
   - `new is not None and old is not None`: M7, return 1.
   - `new is not None and old is None`: continue.
6. **Unsaved edits in the lockfile (skipped by `--force`).** `dirty = _writeset_dirty_collisions(target, [_LOCKFILE_REL])`. `_EditCheckCannotTell`: print `_cannot_tell_refusal("--documentation-plan-moved", exc.reason)` to stderr, return 1. If `dirty`: print M10 to stderr, return 1.
7. **Record.** `matches = ("sha256:" + _sha256_hex(new) == rec.get("hash"))`; `rec["dst"] = _DOCPLAN_NEW`; `_commit_lock_and_caches(target, lock, [])`; print M11 when `matches`, else M12; return 0.

Dispatch in `cmd_upgrade`, right after the `--heal-layout` block: a `--to` given is refused with M13 (exit 2), as `--heal-layout` refuses it; `ScaffoldSecurityError`, and any `OSError` or `ValueError` from step 2, step 3 or the lock write, are caught and printed as M9 (exit 2), as `_layout_command`'s caller does. Exits: 0 for M1, M8, M11, M12; 1 for M2 to M7 and M10; 2 for M9 and M13.

### Messages

`LINKS` is the single line `Links in your own files are not changed: search them for docs/DOCUMENTATION_PLAN.md and point each at dev/DOCUMENTATION_PLAN.md.` `STEPS` is the three lines of D1.

| Id | Case | Text | Exit |
|---|---|---|---|
| M1 | no record (module not installed) | `Nothing to record: the lockfile has no record of the documentation plan.` | 0 |
| M2 | record twice | `error: upgrade --documentation-plan-moved refused: the lockfile records the documentation plan more than once. Nothing was changed.` | 1 |
| M3 | record not usable | `error: upgrade --documentation-plan-moved refused: the lockfile's record of the documentation plan is not one this command records (it names another place, or is marked verbatim). Nothing was changed.` | 1 |
| M4 | 0.8 layout move still ahead | `error: upgrade --documentation-plan-moved refused: this project still has the 0.8 layout migration ahead of it ({n} file(s) at their old paths). Finish it first (run upgrade --plan and follow it), then run the three steps. Nothing was changed.` | 1 |
| M5 | missing from both places | `error: upgrade --documentation-plan-moved refused: the documentation plan is at neither docs/DOCUMENTATION_PLAN.md nor dev/DOCUMENTATION_PLAN.md. Nothing was changed. Restore it with Git, then run these steps in order:` then `STEPS` | 1 |
| M6 | still at the old place only | `error: upgrade --documentation-plan-moved refused: the file is still at docs/DOCUMENTATION_PLAN.md. This command records a move you make with Git; it does not make it. Nothing was changed. Run these steps in order:` then `STEPS` | 1 |
| M7 | a file at both places | `error: upgrade --documentation-plan-moved refused: a file is at both docs/DOCUMENTATION_PLAN.md and dev/DOCUMENTATION_PLAN.md. Nothing was changed. Keep one: compare them, delete the one you do not want (git rm -f <that path>), and make sure the one you keep is at dev/DOCUMENTATION_PLAN.md. Then run step 2 again.` | 1 |
| M8 | already recorded at the new place | `Nothing to record: the lockfile already records dev/DOCUMENTATION_PLAN.md.` and, when a file is also at the old place, ` A file is also at docs/DOCUMENTATION_PLAN.md and was left alone.` | 0 |
| M9 | link, folder, special file or other containment refusal | `error: upgrade --documentation-plan-moved refused (containment): {exc}` | 2 |
| M10 | lockfile has unsaved edits | `error: refusing --documentation-plan-moved: the lockfile has unsaved edits; commit them or pass --force` | 1 |
| M11 | recorded, bytes match the record's hash | `Recorded dev/DOCUMENTATION_PLAN.md as the documentation plan. Now do step 3: git add dev/.cairn/cairn-lock.yml, then git commit.` then `LINKS` | 0 |
| M12 | recorded, bytes differ from the record's hash | the M11 first sentence, then ` The file differs from the version the lockfile recorded. If the changes are yours, run python install/scaffold.py upgrade --target <repo> --finalize dev/DOCUMENTATION_PLAN.md, then do step 3; if not, restore the file from a copy you trust.` then `LINKS` | 0 |
| M13 | `--to` given | `error: --documentation-plan-moved runs against the running target tree; --to is not supported (run scaffold from the target tree).` | 2 |

A second run after M11 or M12 prints M8, exit 0, and writes nothing. In M9, `{exc}` is the installer's own guard text. On Windows a folder junction is caught only by the guard's last check, whose text can name where the junction leads; no control character can reach it. The plan accepts this residual.

## D3. Wiring and the report line

Mirror plan B's `--heal-layout`, point by point:

1. `p.add_argument("--documentation-plan-moved", action="store_true", help="Record that you moved docs/DOCUMENTATION_PLAN.md to dev/DOCUMENTATION_PLAN.md with git mv. Changes only the lockfile.")`.
2. Add `("--documentation-plan-moved", args.documentation_plan_moved)` to the `actions` list.
3. Add `args.documentation_plan_moved` to both `any(...)` tuples in `_layout_command` and to the profile-link refusal condition in `cmd_upgrade`.
4. Dispatch as in D2.

New helper `_documentation_plan_move_lines(target) -> list[str]`. It never raises, whatever the lock holds. It reads the lock with `read_lockfile(target)`; returns `[]` on any `OSError`, `ScaffoldSecurityError` or `ValueError`, or when the lock is missing. It reads `files` only when it is a list and skips any record that is not an object, as D2 step 1 does. When exactly one record has `src == _DOCPLAN_SRC` and its `dst == _DOCPLAN_OLD`, it returns these lines, and otherwise `[]`:

```
The documentation plan moves to dev/ in 0.9. To move it, run these steps in order:
<STEPS, three lines>
Links in your own files are not changed: search them for docs/DOCUMENTATION_PLAN.md and point each at dev/DOCUMENTATION_PLAN.md.
```

The helper writes nothing. Print the lines (a) at the end of the plain `--plan` report, after the heal line; (b) after a successful `--apply`, after the model-selection lines. A project with the 0.8 layout move still ahead gets the layout plan first (`_layout_command` returns before the ordinary report), so it sees the lines only after that move is finished. `--stage` prints nothing new.

Everything else in `_compute_upgrade`, `_apply_upgrade`, `_write_stage`, `_layout_plan`, `LAYOUT_INSTALLS`, `_LAYOUT_MOVES` and `verify_integrity.py` stays unchanged. The ordinary upgrade merges the template into whichever place the lock records, so the order of the ordinary upgrade and this command does not matter (tested, D5).

## D4. Shipped-text edits (chunk C1)

Replace `docs/DOCUMENTATION_PLAN.md` with `dev/DOCUMENTATION_PLAN.md` (and a relative link `../../docs/DOCUMENTATION_PLAN.md` with `../DOCUMENTATION_PLAN.md`) at exactly these places, by exact replacement of the line, never by regenerating the file:

- `install/_scaffold/config.py`: the `InstallSpec("default-on/documentation_plan_template.md", "docs/DOCUMENTATION_PLAN.md")` row; the `_MODULE_DISCOVERY["documentation-plan"]` second element; the one comment line above the module that says `cairn/docs/DOCUMENTATION_PLAN.md` (it becomes `cairn/dev/DOCUMENTATION_PLAN.md`). Only the `_MODULE_MAPPINGS` row changes what the code does; the other two are a string in a table and a comment.
- `templates/modules/default-on/documentation-plan.md`: every occurrence except the one in the "Cross-reference to the reference deployment" section that says `its docs/DOCUMENTATION_PLAN.md` (that is another project's file; leave it). That is: the header comment, the "Selected when", "Adds to", "Forking the procedure" and "Style guide" mentions, and the three Blocks (text and link target); and the one that says `cairn/docs/DOCUMENTATION_PLAN.md` becomes `cairn/dev/DOCUMENTATION_PLAN.md`. Count before and after with `grep -c`; the edited count is every occurrence minus the one left.
- `templates/modules/default-on/documentation_plan_template.md`: the paragraph in the "Domain-local governance" list (exact replacement below); the `this file in docs/` phrase in the placement list; and the "Domain-governance maps" entry.
- `templates/modules/default-on/scanner-check-allow.json`: `"target": "docs/DOCUMENTATION_PLAN.md"` becomes `"target": "dev/DOCUMENTATION_PLAN.md"` (the allow entry still excuses the module's links, which are meant for the project root).
- `templates/core/dev/plans/_template.md` (the prose in the slot placeholder) and `templates/core/dev/proposals/_template.md` (the slot's own link and the placeholder text): `docs/DOCUMENTATION_PLAN.md` becomes `dev/DOCUMENTATION_PLAN.md`, and `../../docs/DOCUMENTATION_PLAN.md` becomes `../DOCUMENTATION_PLAN.md`. Leave `(`docs/`)` in the layer sentences: it names the descriptive layer's folder.

Exact replacement for the placement paragraph in the forkable (the six lines starting `* **This file** (`):

```
  * **This file** (`dev/DOCUMENTATION_PLAN.md`) governs
    documentation placement and lives in `dev/`.  Where documents
    go is an operating question for the people and agents who write
    them, so this file's domain is the project's operating files
    and the rule above holds: it lives with them, and `docs/` holds
    only what describes the software.
```

The `this file in docs/` phrase becomes `this file in dev/`. Leave the test-plan entries in that list as they are.

## D5. Tests

Edited, all by exact replacement:

- `tests/test_documentation_plan_module.py`: `FORKABLE_DST` and its docstring lines name `dev/DOCUMENTATION_PLAN.md`; the "at the docs root" wording in the opening docstring says "under dev/". Ordinary test file.
- `tests/test_default_security_stance.py` (protected): the one sentinel `"documentation-plan": "dev/DOCUMENTATION_PLAN.md"`.
- `tests/integration/test_link_check_exclusions.py` (ordinary): the two assertions (target string and the message text) name `dev/DOCUMENTATION_PLAN.md`.
- `tests/test_upgrade_refuses_hostile_project_data.py` (protected), `test_init_lock_refuses_a_mapped_file_below_a_linked_parent`: after the move `docs/` may not exist in the installed test project, so the test uses a folder that does: `world.project / "dev" / "modules"` replaces `world.project / "docs"` (three lines: `rmtree`, the outside folder's file, and `link`). The two assertions name the `README.md` inside the installed `dev/modules` folder (written with that folder's name in front), not `documentation-plan.md`, and the file the outside folder holds is `README.md`. Reason: the refusal names the first mapped path below the link in destination order, and that `README.md` sorts first. If the test then fails for any reason other than these names, stop and report: do not widen it. Other tests in that file create their own `docs` subfolders and are not edited.

New file `tests/test_upgrade_documentation_plan_moved.py` (tier: `workflow`, pattern `test_upgrade_documentation_plan_moved`). One fixture installs a small project with `scaffold.main` and makes it look like a 0.8 install: it moves `dev/DOCUMENTATION_PLAN.md` to `docs/DOCUMENTATION_PLAN.md`, sets the lock record's `dst` to the old path, sets the record's `base_cache` to `dev/.cairn/base/docs/DOCUMENTATION_PLAN.md` and moves the cache file there (helpers as in plan B's retire-wrapper test file: `_install`, `_upgrade`, `_lock`, `_write_lock`). The owner's `git mv` is simulated by `os.replace` of the file to `dev/` (a Git repo is made only in the unsaved-edits test and the two order tests, which commit). All tests call `scaffold.main(["upgrade", ...])` and read the exit code and captured output. One test per row; the control is what the test pins, so the test fails if that behaviour is removed.

| Test | Setup | Expect (id, exit) | Control |
|---|---|---|---|
| records a moved file | move the file; snapshot the tree | M11, 0; record `dst` new, every other key unchanged; the lock is the only file that changed (byte-compare every other file) | the one-field write; no other write |
| records an edited file | append bytes, then move | M12, 0; file bytes untouched; record `hash` unchanged; `verify_integrity` fails until `--finalize dev/DOCUMENTATION_PLAN.md`, then passes | the hash comparison; a planted file is caught |
| second run | record, then run again | M8, 0, tree unchanged | idempotence |
| still at the old place | no move | M6, 1; tree and lock unchanged; the output holds the three `STEPS` lines | the refusal; the steps text |
| a file at both places | copy to `dev/` and keep `docs/` | M7, 1, both files and lock unchanged | the refusal |
| missing from both | delete both | M5, 1 | the missing-file refusal |
| recorded, old copy left | record at new, a file also at `docs/` | M8 with its second sentence, 0; `docs/` file kept | nothing is removed |
| link, folder or special file at new or old, or `docs` or `dev` a link | folder at either place always; `os.symlink` cases skip if links are unavailable | M9, 2; nothing outside changed; lock unchanged | the guard calls |
| unsaved lockfile edits | in a Git repo, commit, edit the lock, move the file | M10, 1; with `--force` M11 | the dirty refusal |
| 0.8 layout ahead | add a lock record `{"src": "core/x.md", "dst": <old path of the first row of upgrade._LAYOUT_MOVES>, "verbatim": True, "hash": "sha256:" + "0" * 64}` | M4, 1, nothing changed | the layout refusal |
| two records, or a verbatim record | edit the lock | M2 or M3, 1 | the record checks |
| another record already at the new place | add a lock record whose `dst` is `dev/DOCUMENTATION_PLAN.md` | M3, 1, nothing changed | the duplicate-destination check |
| cannot tell | make step 2 or the lock write raise `OSError` (monkeypatch) | M9, 2, no traceback, nothing changed | the catch of `OSError` and `ValueError` |
| no record | module removed from the lock | M1, 0 | the no-op |
| `--to HEAD` | | M13, 2 | the refusal |
| the report line | `--plan` before the move; after `--apply`; after the move | `STEPS` and `LINKS` lines printed before, gone after | the report line |
| the report line never raises | lock with `files` a string; with a non-object record; with a bad lock | `--plan` or the helper gives no line and no traceback | the helper's guards |
| one wording | read the report line, M6 and `install/UPGRADE.md` | the three `STEPS` lines are identical in all three | the clear-instructions criterion |
| upgrade first, then record | cut the last line from the cache file and the project file, set `base_hash` to the new cache's hash, commit, run `--stage` and `--apply`, commit; then move and run the command | after `--apply` the template's last line is in the file at `docs/` and nothing at `dev/`; then M11 and `dev/DOCUMENTATION_PLAN.md` holds those bytes | a real template change merges before the move |
| record first, then upgrade | same setup; move and run the command first, then `--stage` and `--apply` | the template's last line is in `dev/DOCUMENTATION_PLAN.md`, nothing at `docs/` | the merge follows the lock's `dst` |
| verification after | after a record, `verify_integrity` and `run_security_verification.py local` | exit 0 | records still judged |

Controls are checked by deleting the behaviour in a scratch copy and seeing the test fail, or by reasoning recorded in the code review if that cannot be done. There are no developmental probes in the test file. Add `test_upgrade_documentation_plan_moved` to the `workflow` tier in `tests/test_tiers.json` in the same chunk, and run `python tests/tier_inventory.py check`.

## D6. Cairn's own tree (chunk C3) and the lock (chunk C4)

C3, by `git mv docs/DOCUMENTATION_PLAN.md dev/DOCUMENTATION_PLAN.md`, then exact replacements of `docs/DOCUMENTATION_PLAN.md` (the Cairn-prefixed form `cairn/docs/DOCUMENTATION_PLAN.md` becomes `cairn/dev/DOCUMENTATION_PLAN.md`) in:

- the moved file itself, at four places: the sentence saying the module ships a copy "to every adopter at `docs/DOCUMENTATION_PLAN.md`"; the placement paragraph (exact replacement below); the `this file in cairn/docs/` phrase; and the "Domain-governance maps" entry. Leave the two places that name the reference deployment's file (`that deployment's docs/DOCUMENTATION_PLAN.md`, in the header section and in the cross-reference list).
- `dev/modules/documentation-plan.md` (same edits as the shipped module file, minus its header comments, which this copy does not carry), `dev/plans/_template.md` and `dev/proposals/_template.md` (slot link and prose, `../../docs/...` becomes `../...`), `dev/.cairn/scanner-check-allow.json` (the target), `dev/rules/conventions.md`, `dev/README.md` (the link text and path become `dev/DOCUMENTATION_PLAN.md` and `DOCUMENTATION_PLAN.md`, relative to `dev/`), `README.md` and `docs/README.md` (link `../dev/DOCUMENTATION_PLAN.md`), and the accepted proposal `dev/proposals/2026-11-05-codex-budgeted-unattended-work.md` (path only; no other word).
- Left alone on purpose: `dev/.cairn/base/dev/.cairn/scanner-check-allow.json` (a saved ancestor; its hash is in the lock), archived plans, proposals and strategy files (134 files), older `CHANGELOG.md` entries, `docs/methodology/consolidation-review.md` (a dated table) and the 2026-10-28 ceremony report under `dev/measurement/`.

Exact replacement for the placement paragraph in Cairn's own file (the six lines starting `  * **This file**`):

```
  * **This file** (`cairn/dev/DOCUMENTATION_PLAN.md`) governs
    documentation placement and lives in `dev/`.  The Maintainer
    placed it there (chat, 2026-11-19).  Where documents go is an
    operating question for the people and agents who write them,
    so this file's domain is Cairn's operating files and the rule
    above holds: it lives with them, and `docs/` holds only what
    describes the software.
```

C4: `python install/scaffold.py upgrade --target . --documentation-plan-moved` on Cairn's own tree (C3 already moved the file with `git mv`, the owner-moved case; the moved file was edited in C3, so the output is M12); then `python install/scaffold.py upgrade --target . --finalize <path>` once for each of `dev/DOCUMENTATION_PLAN.md`, `dev/modules/documentation-plan.md`, `dev/plans/_template.md`, `dev/proposals/_template.md`, `dev/.cairn/scanner-check-allow.json` and `dev/README.md` (the six records, other than the living `dev/PLANNING.md`, that name the old path and carry a hash). Commit `dev/.cairn/cairn-lock.yml` alone, in its own commit. Then `python install/verify_integrity.py --target .` must exit 0 on Cairn's own tree. Then write `install/UPGRADE.md`'s numbered step with the three `STEPS` lines of D1 word for word, a sentence saying `<repo>` is the project folder, and the `--init-lock` limit (the old file stays and the new template is written beside it; keep one, then run the steps). Then run the instructions check named in the plan's Verification and write its record into the plan.


## D7. Counts and test lists moved out of the plan body

**Mentions of the old path (`git grep`, 2026-11-20).** Shipped: 5 template files, plus `config.py`. Cairn's own live files: 11, plus the lock and a saved ancestor. Tests: 4. Left alone: 134 archived files and four historical mentions (a changelog entry, a dated table, a 2026-10 report, the saved ancestor). Three mentions name another project's file (the reference deployment) and are left.

**Tests each chunk runs (the plan's Verification gives the selector counts).** C1 runs the ten tests that guard the changed promise: `test_documentation_plan_module`, `test_default_security_stance`, `test_upgrade_refuses_hostile_project_data`, `integration/test_link_check_exclusions`, `test_reference_scripts`, `test_upgrade_module_additions`, `test_config_module`, `test_presets`, `test_install_report_slots`, `test_onboarding_seed_roster`. C3 runs the prose gates and five tests: `test_documentation_plan_module`, `integration/test_link_check_exclusions`, `test_check_cairn_content`, `test_module_roster`, `test_core_dev_folders`.
