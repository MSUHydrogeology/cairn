# Detail for plan E of the defect arc: exact conditions, texts and edits

This file is part of `dev/plans/2026-11-20-defect-arc-e-documentation-plan-moves.md`. It exists because the plan must leave no design to a low-tier implementer, and the exact texts would push the plan well past its word target. The companion is part of the plan.

Proposed paths:
- `dev/DOCUMENTATION_PLAN.md`
- `tests/test_upgrade_documentation_plan_move.py`

Installer code was read in the Git worktree for plan B (branch `arc-b-impl`, commit `029532a0`). Line numbers below are from that commit and are guides; the function names are the contract.

## D1. Names used by the command

In `install/_scaffold/upgrade.py`, next to `_LAYOUT_LOCK_KEYS`, add three module constants:

- `_DOCPLAN_SRC = "modules/default-on/documentation_plan_template.md"` (the lock's `src` for the record).
- `_DOCPLAN_OLD = "docs/DOCUMENTATION_PLAN.md"`.
- `_DOCPLAN_NEW = "dev/DOCUMENTATION_PLAN.md"`.

No name from the lockfile, the project tree or the command line is ever used as a path to write. Only these two constants are. The record's `base_cache`, `base_hash`, `hash` and every other key stay exactly as they are; only `dst` changes. The saved ancestor file stays where it is (the lock names its path, so nothing else needs to move, and moving it would add a second write to a sequence that is safe because it has only three).

## D2. The command `upgrade --move-documentation-plan`

New function `_cmd_move_documentation_plan(target, templates_root, lock, force) -> int` in `install/_scaffold/upgrade.py`. It is built from plan B's own pieces: `_writeset_dirty_collisions`, `_cannot_tell_refusal`, `_commit_lock_and_caches`, `_stage_exclusive`, `_read_regular_bytes`, `_assert_safe_write`, `_remove_unchanged_file`, `_legacy_layout_paths`. `os` and `stat` are already imported there. Steps, in this order; the first that applies decides:

1. **Find the record.** `recs = [r for r in lock.get("files") or [] if isinstance(r, dict) and r.get("src") == _DOCPLAN_SRC]`.
   - 0 records: print M1, return 0.
   - more than 1: print M2 to stderr, return 1.
   - the one record `rec`: if `rec.get("dst") not in (_DOCPLAN_OLD, _DOCPLAN_NEW)` or `rec.get("verbatim")` is truthy: print M3 to stderr, return 1.
2. **Layout still ahead (only when `rec["dst"] == _DOCPLAN_OLD`).** `ahead = _legacy_layout_paths(target, templates_root)`. If it is not empty: print M4 with `{n}` = `len(ahead)` to stderr, return 1. (A project that came from 0.7 has the whole 0.8 move ahead, so this refuses; once that move is finished the list is empty.)
3. **Read both places.** For each of `target / _DOCPLAN_OLD` and `target / _DOCPLAN_NEW`: `_assert_safe_write(path, target)`, then `data = _read_regular_bytes(path, single_link=True)` (`None` when absent). Any link, folder, special file, or file with more than one hard link raises `ScaffoldSecurityError`; the caller prints the containment line (M10, exit 2) and nothing has been written. Name the results `old` and `new` (`bytes | None`).
4. **If `rec["dst"] == _DOCPLAN_NEW` (already recorded):**
   - `old is not None and new is not None and old == new`: `_remove_unchanged_file(target / _DOCPLAN_OLD, target, old, durable=True)`; if it returns true print M9 and return 0; if false print M8 to stderr and return 1.
   - `old is not None` otherwise: print M7, return 0.
   - else: print M6, return 0.
5. **Record is at the old place.**
   - `old is None and new is None`: print M5 to stderr, return 1.
   - `old is not None and new is not None and old != new`: print M11 to stderr, return 1.
6. **Unsaved edits in the lockfile (skipped by `--force`).** `dirty = _writeset_dirty_collisions(target, [_LOCKFILE_REL])`. `_EditCheckCannotTell`: print `_cannot_tell_refusal("--move-documentation-plan", exc.reason)` to stderr, return 1. If `dirty`: print M12 to stderr, return 1. The old file is not checked: its bytes are carried unchanged.
7. **Write.** In this order; a stop between two steps leaves a state the next run finishes (step 4 or step 5 with equal bytes):
   - (a) only when `new is None` (the move proper): `tmp = _stage_exclusive(target / _DOCPLAN_NEW, old, target)`; `os.chmod(tmp, stat.S_IMODE(os.lstat(target / _DOCPLAN_OLD).st_mode))`; in a `try`: `os.link(tmp, target / _DOCPLAN_NEW)`, catching `FileExistsError` and raising `ScaffoldSecurityError("a file appeared at the new place while the move ran")`; in the `finally`: `tmp.unlink(missing_ok=True)`. `os.link` fails when the name exists, so an adopter's file can never be overwritten, even if one appears after step 3.
   - (b) `rec["dst"] = _DOCPLAN_NEW`; `_commit_lock_and_caches(target, lock, [])`.
   - (c) only when `old is not None`: `_remove_unchanged_file(target / _DOCPLAN_OLD, target, old, durable=True)`. False: print M8 to stderr, return 1. That function removes a folder only if the removal leaves it empty, that one folder and none above it; so `docs/` stays when it holds anything else, and is removed when this file was all it held.
   - (d) print: M13 when (a) ran; M14 when (a) did not run and `old is not None`; M15 when `old is None`. Return 0.

Dispatch in `cmd_upgrade`: a `--to` given is refused with M16 (exit 2), exactly as `--heal-layout` refuses it. `ScaffoldSecurityError` is caught and printed as M10 (exit 2).

### Messages and exit codes

`LINKS` is the single line `Links in your own files are not changed: search them for docs/DOCUMENTATION_PLAN.md and point each at dev/DOCUMENTATION_PLAN.md.`

| Id | Case | Text | Exit |
|---|---|---|---|
| M1 | no record (module not installed) | `Nothing to move: the lockfile has no record of the documentation plan.` | 0 |
| M2 | record twice | `error: upgrade --move-documentation-plan refused: the lockfile records the documentation plan more than once. Nothing was changed.` | 1 |
| M3 | record not movable | `error: upgrade --move-documentation-plan refused: the lockfile's record of the documentation plan is not one this command moves (it names another place, or is marked verbatim). Nothing was changed.` | 1 |
| M4 | 0.8 layout move still ahead | `error: upgrade --move-documentation-plan refused: this project still has the 0.8 layout migration ahead of it ({n} file(s) at their old paths). Finish it first (run upgrade --plan and follow it), then run this again. Nothing was changed.` | 1 |
| M5 | file missing from both places | `error: upgrade --move-documentation-plan refused: neither docs/DOCUMENTATION_PLAN.md nor dev/DOCUMENTATION_PLAN.md exists. Nothing was changed. Restore the file from Git, then run this again.` | 1 |
| M6 | recorded at new, nothing to do | `Nothing to move: the lockfile already records dev/DOCUMENTATION_PLAN.md.` | 0 |
| M7 | recorded at new, an old file is also there and differs, or new is missing | M6 text, then ` A file is also at docs/DOCUMENTATION_PLAN.md and was left alone.` (one line) | 0 |
| M8 | old file changed while the move ran, kept | `error: upgrade --move-documentation-plan: dev/DOCUMENTATION_PLAN.md and the lockfile are in place, but docs/DOCUMENTATION_PLAN.md changed while the move ran and was kept. Compare the two files and delete the one you do not want.` | 1 |
| M9 | leftover old copy removed | `Removed the leftover copy docs/DOCUMENTATION_PLAN.md; dev/DOCUMENTATION_PLAN.md holds the same bytes. Commit both paths.` | 0 |
| M10 | link, folder, special file, hard link, or other containment refusal | `error: upgrade --move-documentation-plan refused (containment): {exc}` | 2 |
| M11 | a different file already at the new place | `error: upgrade --move-documentation-plan refused: dev/DOCUMENTATION_PLAN.md already exists and differs from docs/DOCUMENTATION_PLAN.md. Nothing was changed. Keep the copy you want at dev/DOCUMENTATION_PLAN.md and delete the other, then run this again.` | 1 |
| M12 | lockfile has unsaved edits | `error: refusing --move-documentation-plan: the lockfile has unsaved edits; commit them or pass --force` | 1 |
| M13 | moved | `Moved docs/DOCUMENTATION_PLAN.md to dev/DOCUMENTATION_PLAN.md. Commit both paths and dev/.cairn/cairn-lock.yml.` then `LINKS` | 0 |
| M14 | finished an interrupted move | `Finished the move of docs/DOCUMENTATION_PLAN.md to dev/DOCUMENTATION_PLAN.md. Commit both paths and dev/.cairn/cairn-lock.yml.` then `LINKS` | 0 |
| M15 | adopter already moved it by hand | `Recorded dev/DOCUMENTATION_PLAN.md as the documentation plan; docs/DOCUMENTATION_PLAN.md was already gone. Commit dev/.cairn/cairn-lock.yml. If you edited the file, run upgrade --finalize dev/DOCUMENTATION_PLAN.md.` then `LINKS` | 0 |
| M16 | `--to` given | `error: --move-documentation-plan runs against the running target tree; --to is not supported (run scaffold from the target tree).` | 2 |

A second run after M13, M14 or M15 prints M6, exit 0, and writes nothing. In M10 the text of `exc` names only the constant paths and folders above them (`docs`, `dev`); it never names a path from the lockfile.

## D3. Wiring and the plan line

Mirror plan B's `--heal-layout`, point by point:

1. `p.add_argument("--move-documentation-plan", action="store_true", help="Move docs/DOCUMENTATION_PLAN.md to dev/DOCUMENTATION_PLAN.md and record the new place in the lockfile. Commit both afterwards.")`.
2. Add `("--move-documentation-plan", args.move_documentation_plan)` to the `actions` list.
3. Add `args.move_documentation_plan` to both `any(...)` tuples in `_layout_command` (`mutable`, and the `return None` list) and to the profile-link refusal condition in `cmd_upgrade`.
4. Dispatch right after the `--heal-layout` block: `--to` gives M16; else `_cmd_move_documentation_plan(target, templates_root, lock, args.force)`.

New helper `_documentation_plan_move_lines(target) -> list[str]`: reads the lock with `read_lockfile(target)`; returns `[]` on any `OSError`, `ScaffoldSecurityError`, `ValueError` or when the lock is missing. Otherwise, when exactly one record has `src == _DOCPLAN_SRC`, its `dst == _DOCPLAN_OLD`, and `os.path.lexists(target / _DOCPLAN_OLD)` or `os.path.lexists(target / _DOCPLAN_NEW)` is true, it returns this one line: `The documentation plan moved to dev/ in 0.9. Run python install/scaffold.py upgrade --target <repo> --move-documentation-plan to move docs/DOCUMENTATION_PLAN.md to dev/DOCUMENTATION_PLAN.md. Links in your own files are not changed.` The helper writes nothing and never raises.

Print that line: (a) at the end of the plain `--plan` report, after the heal line; (b) after a successful `--apply`, after the model-selection lines. A project with the 0.8 layout move still ahead gets the layout plan first (`_layout_command` returns before the ordinary report), so it sees this line only after that move is finished. `--stage` prints nothing new.

Everything else in `_compute_upgrade`, `_apply_upgrade`, `_write_stage`, `_layout_plan`, `LAYOUT_INSTALLS`, `_LAYOUT_MOVES` and `verify_integrity.py` stays unchanged. The ordinary upgrade merges the template into whichever place the lock records, so the order of the move and an ordinary `--apply` does not matter.

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
    documentation placement and lives in `dev/`.  It is an
    operating map for the people and agents who write the
    project's documents, so it lives with the project's other
    operating files, and `docs/` holds only what describes the
    software.
```

The `this file in docs/` phrase becomes `this file in dev/`. Leave the test-plan entries in that list as they are.

## D5. Tests

Edited, all by exact replacement:

- `tests/test_documentation_plan_module.py`: `FORKABLE_DST` and its docstring lines name `dev/DOCUMENTATION_PLAN.md`; the "at the docs root" wording in the opening docstring says "under dev/". Ordinary test file.
- `tests/test_default_security_stance.py` (protected): the one sentinel `"documentation-plan": "dev/DOCUMENTATION_PLAN.md"`.
- `tests/integration/test_link_check_exclusions.py` (ordinary): the two assertions (target string and the message text) name `dev/DOCUMENTATION_PLAN.md`.
- `tests/test_upgrade_refuses_hostile_project_data.py` (protected), `test_init_lock_refuses_a_mapped_file_below_a_linked_parent`: after the move `docs/` may not exist in the installed test project, so the test uses a folder that does: `world.project / "dev" / "modules"` replaces `world.project / "docs"` (three lines: `rmtree`, the outside folder's file name `documentation-plan.md` replaces `DOCUMENTATION_PLAN.md`, and `link`), and the two assertions name `dev/modules/documentation-plan.md`. If the test then fails for any reason other than these names, stop and report: do not widen it. Other tests in that file create their own `docs` subfolders and are not edited.

New file `tests/test_upgrade_documentation_plan_move.py` (tier: `workflow`, pattern `test_upgrade_documentation_plan_move`). One fixture installs a small project with `scaffold.main`, then makes it look like a 0.8 install: it moves `dev/DOCUMENTATION_PLAN.md` to `docs/DOCUMENTATION_PLAN.md` and sets the lock record's `dst` to the old path (helpers as in plan B's retire-wrapper test file: `_install`, `_upgrade`, `_lock`, `_write_lock`). All tests call `scaffold.main(["upgrade", ...])` and read the exit code and captured output. One test per row; the control is what each refusal's test pins:

| Test | Setup | Expect (id, exit) | Control: fails if removed |
|---|---|---|---|
| moves an edited file | write extra bytes into the old file | M13, 0; new file equals the edited bytes; old gone; record `dst` new, `hash`, `base_hash`, `base_cache` unchanged; nothing else in the tree changed | the byte-for-byte move |
| second run | run twice | M6, 0, tree unchanged | idempotence |
| plan line | `--plan` before the move | line in D3, tree unchanged; after the move the line is gone | the plan line |
| different file at new place | write other bytes at new | M11, 1, both files and lock unchanged | the no-overwrite refusal |
| same bytes at new place | copy old to new | M14, 0, old gone | the resume |
| missing from both | delete both | M5, 1 | the missing-file refusal |
| moved by hand | delete old only (new exists) | M15, 0, record `dst` new | the record-only route |
| already recorded, leftover | record at new, old copy equal | M9, 0 | the tidy route |
| link at old or new, or `docs` or `dev` a link | `os.symlink`; skip if links are unavailable | M10, 2, nothing outside changed | the guard calls |
| hard link at old | `os.link` the old file | M10, 2 | `single_link=True` |
| other files in `docs/` | add another file in `docs/` | M13, 0, that file kept | the folder rule |
| `docs/` held only this file | default | M13, 0, `docs/` gone | the empty-folder rule |
| lock unsaved edits | in a Git repo, commit, edit the lock | M12, 1; with `--force` M13 | the dirty refusal |
| 0.8 layout ahead | add a legacy-path record (use the fixture in `tests/test_upgrade_layout_migration.py`) | M4, 1, nothing changed | the layout refusal |
| two records or a verbatim record | edit the lock | M2 or M3, 1 | the record checks |
| no record | module removed from the lock | M1, 0 | the no-op |
| `--to HEAD` | | M16, 2 | the refusal |
| verification after | after a move, `verify_integrity` and `run_security_verification.py local` pass | exit 0 | records still judged |
| ordinary upgrade after | `--stage` then `--apply` after a move | merges at the new place, exit 0 | order does not matter |

Edit-tests are permanent promise tests through the public command; there are no developmental probes. Add `test_upgrade_documentation_plan_move` to the `workflow` tier in `tests/test_tiers.json` in the same chunk, and run `python tests/tier_inventory.py check`.

## D6. Cairn's own tree (chunk C3) and the lock (chunk C4)

C3, by `git mv docs/DOCUMENTATION_PLAN.md dev/DOCUMENTATION_PLAN.md`, then exact replacements of `docs/DOCUMENTATION_PLAN.md` (the Cairn-prefixed form `cairn/docs/DOCUMENTATION_PLAN.md` becomes `cairn/dev/DOCUMENTATION_PLAN.md`) in:

- the moved file itself, at four places: the sentence saying the module ships a copy "to every adopter at `docs/DOCUMENTATION_PLAN.md`"; the placement paragraph (exact replacement below); the `this file in cairn/docs/` phrase; and the "Domain-governance maps" entry. Leave the two places that name the reference deployment's file (`that deployment's docs/DOCUMENTATION_PLAN.md`, in the header section and in the cross-reference list).
- `dev/modules/documentation-plan.md` (same edits as the shipped module file, minus its header comments, which this copy does not carry), `dev/plans/_template.md` and `dev/proposals/_template.md` (slot link and prose, `../../docs/...` becomes `../...`), `dev/.cairn/scanner-check-allow.json` (the target), `dev/rules/conventions.md`, `dev/README.md` (the link text and path become `dev/DOCUMENTATION_PLAN.md` and `DOCUMENTATION_PLAN.md`, relative to `dev/`), `README.md` and `docs/README.md` (link `../dev/DOCUMENTATION_PLAN.md`), and the accepted proposal `dev/proposals/2026-11-05-codex-budgeted-unattended-work.md` (path only; no other word).
- Left alone on purpose: `dev/.cairn/base/dev/.cairn/scanner-check-allow.json` (a saved ancestor; its hash is in the lock), archived plans, proposals and strategy files (134 files), older `CHANGELOG.md` entries, `docs/methodology/consolidation-review.md` (a dated table) and the 2026-10-28 ceremony report under `dev/measurement/`.

Exact replacement for the placement paragraph in Cairn's own file (the six lines starting `  * **This file**`):

```
  * **This file** (`cairn/dev/DOCUMENTATION_PLAN.md`) governs
    documentation placement and lives in `dev/`.  The Maintainer
    placed it there (chat, 2026-11-19): it is an operating map for
    the people and agents who write Cairn's documents, so it lives
    with Cairn's other operating files, and `docs/` holds only what
    describes the software.
```

C4: `python install/scaffold.py upgrade --target . --move-documentation-plan` on Cairn's own tree (the file was already moved by `git mv`, so this takes the record-only route, M15); then `python install/scaffold.py upgrade --target . --finalize <path>` once for each of `dev/DOCUMENTATION_PLAN.md`, `dev/modules/documentation-plan.md`, `dev/plans/_template.md`, `dev/proposals/_template.md`, `dev/.cairn/scanner-check-allow.json` and `dev/README.md` (the six records, other than the living `dev/PLANNING.md`, that name the old path and carry a hash). Commit `dev/.cairn/cairn-lock.yml` alone, in its own commit. Then `python install/verify_integrity.py --target .` must exit 0 on Cairn's own tree.
