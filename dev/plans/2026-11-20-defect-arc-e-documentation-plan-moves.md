# Plan: Defect arc E, the documentation plan moves

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: The documentation plan file moves from `docs/` into `dev/` for new installs, for Cairn itself and, through one new upgrade command, for every project already installed, without touching what its owner wrote in it.

## Build summary

After this plan, a new install and Cairn's own tree keep the documentation plan at `dev/DOCUMENTATION_PLAN.md`. An existing project runs one new command, `upgrade --move-documentation-plan`, which moves the file as its owner left it, byte for byte, and records the new place in the install lockfile. `upgrade --plan` and `--apply` print one line telling the adopter to run it. Shipped texts that name the old place are corrected; nothing the adopter wrote is edited. Four chunks, in the installer engine and the install contract.

## Source proposal

The Maintainer accepted the defect arc at the heavy tier ("Go ahead on the defect arc.", chat, 2026-11-20). Plan E is its last part: the roadmap item from his words of 2026-11-19, "I think DOCUMENTATION_PLAN.md should be in dev/ Please put that as a defect to fix for v0.9". The plan executes it and reopens nothing. Exact messages, step order and edit lists are in the companion `dev/plans/2026-11-20-defect-arc-e-documentation-plan-moves-detail.md` ("Detail"), so a low-tier implementer has no design to invent. The companion is part of the plan.

## Scope

**Result.** New installs, Cairn itself and existing projects all keep the documentation plan at `dev/DOCUMENTATION_PLAN.md`, and an upgrade never loses or overwrites an adopter's copy.

Proposed paths:
- `dev/DOCUMENTATION_PLAN.md`
- `tests/test_upgrade_documentation_plan_move.py`

**Read, not run.** The installer was read in the plan B worktree (branch `arc-b-impl`, commit `029532a0`). This plan starts after plans B and C are merged into `0.9-dev`, when its work folder is cut.

**How existing installs get the move (the design question).** A new small step, not the planned layout move and not the heal. The layout move (`_layout_plan`) proves a file against its release in Git history and merges it with the new template (`_layout_merge`); it blocks on "unproved ancestry" or "overlapping edits", which an adopter's rewritten plan is. The heal (`--heal-layout`) repairs lock keys and tokens, not this. The new step is built from plan B's pieces and changes only the lock record's `dst`; every other key stays, so the saved ancestor still serves later ordinary merges, which carry template changes into the file at its new place. It never merges or re-renders. The 0.8 layout catalog row (old place equals new place there) is left as it is.

**Where the code differs from Strategy's defaults.** (1) Cairn's own record has no saved ancestor; the step needs none. (2) The gate manifest and roster do not name the old path; they go stale only because two protected tests change. (3) Three mentions name another project's file (the reference deployment) and are left. (4) One protected test used `docs/` as its example folder and needs another (Detail D5).

**The existing-install cases.** Messages are in Detail D2; ids and exit codes here.

| Case | Result |
|---|---|
| file at old place, nothing at new | moved, M13, 0 |
| a different file at new place | refused, nothing changed, M11, 1 |
| the same bytes at new place (an interrupted run) | finished, M14, 0 |
| missing from both | refused, M5, 1 |
| adopter moved it by hand | lock record updated only, M15, 0 |
| link, folder or hard link at either place, or a link above | refused, nothing written, M10, 2 |
| `docs/` holds other files / only this file | `docs/` kept / removed (that one folder), M13, 0 |
| lockfile has unsaved edits | refused, M12, 1 (`--force` goes on) |
| second run | M6, 0, writes nothing |
| project from 0.7, 0.8 layout move still ahead | refused, M4, 1; finish that move first |
| module not installed, or record not movable | M1, 0 / M2 or M3, 1 |

`upgrade --plan` prints, before anything is written, the line in Detail D3 whenever the file or its new copy is present and the record is at the old place.

**The adopter's links.** The step edits none of the adopter's files. It prints one line (`LINKS`, Detail D2) naming both places. Five shipped files that Cairn renders for adopters name the old place: the module document, the forkable plan, its scanner allow-list, and the plan and proposal templates. Adopters get their corrections through the ordinary merge. Text pasted into the `documentation-discipline` slot of `AGENTS.md` or the `documentation-tier-home` slots is the adopter's, is not rewritten, and the line tells them to search for it.

**Mentions of the old path (`git grep`, 2026-11-20).** Shipped: 5 template files, plus `config.py`. Cairn's own live files: 11, plus the lock and a saved ancestor. Tests: 4. Left alone: 134 archived files and four historical mentions (a changelog entry, a dated table, a 2026-10 report, the saved ancestor).

**Protected and counted files, and the reason the Maintainer will see at the signing.**
- `install/_scaffold/upgrade.py` (engine, AST baseline): a new command moves one named file safely.
- `install/_scaffold/config.py` (cascade-mutable, no HOLD): one install row and one table entry name the new place.
- `tests/test_default_security_stance.py` and `tests/test_upgrade_refuses_hostile_project_data.py` (protected, so each adds a line to the signing): one expected path names the new place; one test uses a folder that still exists after the move, and checks the same refusal.
- The always-loaded files name no path to change. Measured 2026-11-20 with `wc -w`: Cairn's 1,051 + 311 + 230 = 1,592 against 2,000; shipped 1,262 + 162 + 73 = 1,497 against 1,500. Re-measured after C3.
- Doctrine: the "this file lives in docs/" paragraph in both plan files (Detail D4 and D6) changes meaning, not only a path; it is functional prose, edited by exact replacement, and reviewers answer "does any rule weaken or disappear?".

**Stale records.** (1) The AST baseline: `Assign:_MODULE_MAPPINGS` changes, `cmd_upgrade` changes again, new functions join the known-new list; it stays red until the Maintainer's baseline step, and after C2 the implementer runs the runbook's Step 1 listing and records the counts. (2) The gate manifest's `mapping_symbols` digest and the roster's hashes for the two protected tests: refreshed at the signing. (3) Cairn's own lock: refreshed in C4 by the installer, alone in its commit.

**Reuse.** Plan B's guards and lock writer (named in Detail D2). Searched `install/_scaffold/` for `documentation`, `move` and `relocate`: only the layout table, which this does not extend.

### Documentation / doctrine surface

`install/UPGRADE.md` (this step, the 0.7 order, and the limit that a project with no lockfile, upgraded by `--init-lock`, is not moved), `CHANGELOG.md` (one entry), the roadmap row, and the shipped texts. No rule is added.

## Sequence

Code review once, after C4; no earlier review point. C4 needs C2 and C3 and the merged plans B and C, which edit the same `install/UPGRADE.md`, `CHANGELOG.md`, roadmap and lock.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | New installs and shipped text | plan review | `config.py` rows, 5 shipped templates, 4 tests |
| C2 | The upgrade step | C1 | `--move-documentation-plan`, the plan line, new test file and its tier |
| C3 | Cairn's own tree | C1 | `git mv`, 10 live files corrected |
| C4 | Records and Cairn's own lock | C2, C3 | notes, changelog, roadmap, lock commit |

## Acceptance criteria

**C1.** A default install through `scaffold.main` writes `dev/DOCUMENTATION_PLAN.md` and no file under `docs/`; its lock record names the new place; the module-discovery text names it. Each shipped text in Detail D4 names the new place, and the three references to another project's file are unchanged (`grep -c` before and after, as Detail D4 says). Entry point: `scaffold.main`. The four tests are edited as Detail D5 says; `tests/test_documentation_plan_module.py` fails if the install row is not changed, and the refusal test keeps checking that a linked parent of a mapped file is refused, in a folder that exists.

**C2.** `upgrade --move-documentation-plan` does what the table above says, with the messages of Detail D2, through `scaffold.main(["upgrade", ...])`. It writes nothing outside the project, follows no link, never overwrites a file, and uses no path from the lock. A tampered record is refused and changes nothing. After a move, `verify_integrity` and `run_security_verification.py local` pass, and an ordinary `--stage` and `--apply` merge at the new place. `--plan` and `--apply` print the one line. New `tests/test_upgrade_documentation_plan_move.py` has one test per row of Detail D5, each with the control named there. It is listed in `tests/test_tiers.json` in this chunk and `python tests/tier_inventory.py check` passes. `_compute_upgrade`, `_apply_upgrade`, `_layout_plan`, `layout_catalog.py` and `verify_integrity.py` stay unchanged.

**C3.** `dev/DOCUMENTATION_PLAN.md` exists by `git mv`, `docs/DOCUMENTATION_PLAN.md` does not, and the 10 other live files named in Detail D6 name the new place. `git grep DOCUMENTATION_PLAN` outside the left-alone set finds no `docs/` form except the two reference-deployment mentions in the moved file and the one in the module copy. The prose gates pass on each edited file, and the always-loaded word totals are unchanged.

**C4.** `install/UPGRADE.md` explains the step in the order an adopter follows it (finish the 0.7 layout move first; run `--plan`; run the command; commit; search for links). `CHANGELOG.md` has one entry. The roadmap row for this file is marked settled and plan E's share of the joined run is listed. Cairn's own lock is refreshed as Detail D6 says, in a commit that holds only the lockfile, and `install/verify_integrity.py` exits 0 on Cairn's own tree.

**Security (re-answered).** S1, who supplies the input: the lock (`src`, `dst`, `verbatim`), the project tree and the flag; none reaches a write as a path, because only two constants do. S2, can it fail: each refusal has the control in Detail D5 (the no-overwrite test controls the exclusive create). S3, what runs it: the adopter, by `upgrade --move-documentation-plan`; `verify_integrity.py` and `run_security_verification.py local` then judge the result and are unchanged. S4, which way it breaks: refuse, name the file, write nothing; an interrupted run leaves a state the next run finishes. It adds one write route into the lock, for one record, and removes one file whose bytes it holds. S5, what still gets through: someone who can write the lock can make the step run for a record whose `src` is the plan template; that only moves `docs/DOCUMENTATION_PLAN.md` to `dev/DOCUMENTATION_PLAN.md` inside the project. No record leaves the integrity check, and the moved file is still judged by its recorded hash.

## Scope delta

**Scope delta**: preserved. Every outcome the proposal assigns to plan E is delivered: the move in Cairn's tree, the upgrade move, and the corrected shipped files.

## Verification

**Selector (`python tests/tier_inventory.py for <paths>`, run in the main checkout on 2026-11-20; re-run at the starting commit).** C1 selects 68 test files, over the 40-file limit of `tests/conftest.py`. The run is not split: C1 runs the ten tests that guard the changed promise (`test_documentation_plan_module`, `test_default_security_stance`, `test_upgrade_refuses_hostile_project_data`, `integration/test_link_check_exclusions`, `test_reference_scripts`, `test_upgrade_module_additions`, `test_config_module`, `test_presets`, `test_install_report_slots`, `test_onboarding_seed_roster`) and leaves the 68 to the arc's joined run. C2 selects 38 for `upgrade.py`, plus the new file: 39. C3 selects 41 for its prose files; it runs the prose gates and five tests (`test_documentation_plan_module`, `integration/test_link_check_exclusions`, `test_check_cairn_content`, `test_module_roster`, `test_core_dev_folders`). C4 selects 9. Before each chunk, run its files once with `-rf` and keep each failing test id and first message line; after, a failure is a host failure only if both are on that list.

**Hosts.** This Windows machine runs the selected tests; link tests skip without symbolic-link rights and run once in its Linux subsystem (development only). Nothing here certifies; the Python 3.13 run waits for the joined run. **Prose gates**, one file per call: `claim_check.py`, `link_check.py`, `tests/check_cairn.py`, `git diff --check`. **Issues.** None to close; the roadmap row is not an issue.

**Not checked.** Nothing was run. Not measured: the 0.7 path end to end; `os.link` and `chmod` on Windows; the protected test with `dev/modules` as its folder. **Does any rule weaken or disappear?** One sentence of placement doctrine is reworded in two plan files (C1, C3); the rule that a domain's governance lives in that domain is kept, and this file is stated as an operating file in `dev/`.

## Plan review -- Claude Sonnet 5.5 -- 2026-11-21

Reviewed commit: 78a718b38a87ffa176c1ba07a3664be6c8b7140e (installer read at `029532a0` in the plan B worktree)

**Obligation**: the usual plan review; the Security Review follows
**Tier**: Internal
**Findings**: raised

**Foundations**
1. **Should this happen as framed?** Yes. The proposal gives plan E "the upgrade move", and a command that moves one file without overwriting is the right shape; every function the companion names exists with the arguments it uses. -- `install/_scaffold/upgrade.py` (`_cmd_heal_layout`, `_cmd_retire_wrapper`, `_legacy_layout_paths`), proposal line 54.
2. **Best alternative.** A command that only records the new place, after the adopter runs `git mv`, drops the hard link, the delete, the folder rule and half the messages and tests. The plan already builds that route (M15). It is the Maintainer's call (finding 7). -- Detail D2 steps 4 to 7.
3. **What would show it wrong.** A test that runs an ordinary `--stage` and `--apply` against a real upstream change at the old place and then the move, and finds the change at the new place. The plan has none (finding 2). -- Detail D5.

**Central claim.** It holds in the code: `_compute_upgrade` and `_apply_upgrade` work from the record's `dst`, and the new-file branch skips a source the lock already tracks, so `--plan`, `--stage` and `--apply` act in whichever place the lock names. A stage made before the move is refused afterward, because the whole-lock identity changes. A hand-moved file with `--finalize` fails closed. `--init-lock` leaves two files: finding 6.

**Findings**
1. **Blocking.** The hard-link write has no message or exit code when the file system refuses it, and no test fails if `os.link` is swapped for an overwriting call. Exact words below.
2. **Blocking.** The order is not pinned. "Ordinary upgrade after" runs against an unchanged template, so it merges nothing. The M4 setup names a fixture that cannot be reused. Exact words below.
3. **Blocking.** The edited protected test would fail: the refusal names the first mapped path under the link, and the folder's `README.md` sorts before `documentation-plan.md`. Exact words below.
4. Non-blocking. A stop between the link and removing its temporary name leaves a second link, so the next run refuses (M10). Say so in S4. Drop the `os.chmod`: a read-only old file on Windows would block that removal.
5. Non-blocking. No removal condition. Add to Scope: "Remove `--move-documentation-plan` and its tests in the release that stops supporting upgrades from 0.8 installs; the Maintainer names that release."
6. Non-blocking. UPGRADE.md must say that `--init-lock` leaves the old file in place and adds the new template beside it. C3 says 10 other files; D6 names 9.
7. For the Maintainer. Choose the record-only command or the moving command.

**Doctrine.** The reworded paragraph still sits under "Domain-local governance" yet no longer shows that rule; wording below, non-blocking.

**Not covered.** No test, no Windows run. Security questions left to the Security Review. The 134 archived files, the other five tests and the AST baseline steps were not read. The pass is over 300 words because three blocking findings carry their exact words.

Elapsed time: unknown. Tokens: unknown.

**Verdict**: REVISE

### Exact words for the blocking findings

**1. Detail D2 step 7(a)**, after "raising `ScaffoldSecurityError(...)`" add: "Catch any other `OSError` from `os.link` (the file system refuses hard links): print M17 to stderr and return 1. Nothing was written, and the `finally` removes `tmp`." Add **M17**, exit 1: `error: upgrade --move-documentation-plan: this file system does not allow the hard link the move relies on. Nothing was changed. Run git mv docs/DOCUMENTATION_PLAN.md dev/DOCUMENTATION_PLAN.md yourself, then run this command again to record the new place.` Add to D5 two rows. "Hard link refused": `monkeypatch.setattr(os, "link", ...)` raises `OSError(errno.EPERM, "no")`; expect M17, 1, tree and lock unchanged, no `*.tmp` in `dev/`. "File appears during the move": patch `upgrade._stage_exclusive` to call the real one, then write other bytes at `dev/DOCUMENTATION_PLAN.md`; expect M10, 2, the planted bytes kept, lock unchanged; control: `os.link` never overwrites.

**2. Detail D5.** Add to the fixture: set the record's `base_cache` to `dev/.cairn/base/docs/DOCUMENTATION_PLAN.md` and move the cache file there. Replace the "ordinary upgrade after" row with two. "Upgrade first, then move": cut the last line from the cache file and the project file, set `base_hash` to the new cache's hash, commit, run `--stage` and `--apply`, commit, then the move; expect the template's last line in the file at `docs/` after `--apply` and nothing at `dev/`, then M13 and `dev/DOCUMENTATION_PLAN.md` holding those bytes. "Move first, then upgrade": same setup, the move first; expect the line at `dev/` and nothing at `docs/`. Replace the M4 setup with: add a lock record `{"src": "core/x.md", "dst": <old path of the first row of upgrade._LAYOUT_MOVES>, "verbatim": True, "hash": "sha256:" + "0" * 64}`.

**3. Detail D5, last edited-test bullet:** the two assertions name the `README.md` inside the installed `dev/modules` folder (written with that folder's name in front), not `documentation-plan.md`, and the file the outside folder holds is `README.md`. Reason: the refusal names the first mapped path below the link in destination order, and that `README.md` sorts first.

**Doctrine (non-blocking), replacing the last three lines of the placement paragraph in D4 and D6:** "...lives in `dev/`.  Where documents go is an operating question for the people and agents who write them, so this file's domain is the project's operating files and the rule above holds: it lives with them, and `docs/` holds only what describes the software."
