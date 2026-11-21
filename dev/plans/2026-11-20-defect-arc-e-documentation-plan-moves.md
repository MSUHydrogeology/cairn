<!-- claim-check-allow: docs/DOCUMENTATION_PLAN.md, docs/notes.md -->
# Plan: Defect arc E, the documentation plan moves

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: revising-code
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: The documentation plan file moves from `docs/` into `dev/` for new installs and for Cairn itself; a project already installed moves it with one Git command, then runs one new upgrade command that only records the new place.

## Build summary

After this plan, a new install and Cairn's own tree keep the documentation plan at `dev/DOCUMENTATION_PLAN.md`. An existing project's owner moves the file with `git mv` and then runs `upgrade --documentation-plan-moved`, which checks the move and rewrites one field (`dst`) of one lock record. It creates, moves, deletes and overwrites no file of the owner's. `upgrade --plan` and `--apply` print the three steps in order. Shipped texts that name the old place are corrected; nothing the adopter wrote is edited. Four chunks, in the installer engine and the install contract.

## Source proposal

The Maintainer accepted the defect arc at the heavy tier ("Go ahead on the defect arc.", chat, 2026-11-20). Plan E is its last part: the roadmap item from his words of 2026-11-19, "I think DOCUMENTATION_PLAN.md should be in dev/ Please put that as a defect to fix for v0.9". After two reviews he chose the lighter design (Scope delta). Exact messages, steps, edit lists and the test table are in the companion `dev/plans/2026-11-20-defect-arc-e-documentation-plan-moves-detail.md` ("Detail"), so a low-tier implementer has no design to invent. The companion is part of the plan.

## Scope

**Result.** New installs, Cairn itself and existing projects all keep the documentation plan at `dev/DOCUMENTATION_PLAN.md`, and an upgrade never loses, moves or overwrites an adopter's copy.

Paths built: `dev/DOCUMENTATION_PLAN.md` and `tests/test_upgrade_documentation_plan_moved.py` (both exist since the build).

**Read, not run.** The installer this plan builds on is merged into `0.9-dev`. It was read in the main checkout on 2026-11-21 (HEAD `3fb798f5`); its files last changed in `029532a0`, the commit the plan first cited. Plans B and C are merged.

**How existing installs get the move.** The owner moves the file with Git; Cairn's command checks both places and writes only the lock record's `dst`. Every other key stays, so the saved ancestor still serves later ordinary merges, which carry template changes into the file at its new place, in either order. It never merges, re-renders, creates, deletes or moves a file, and removes no folder. The layout move (`_layout_plan`) is not used: it blocks on an adopter's rewritten plan. The 0.8 layout catalog row is left as it is. The cases, messages and exit codes are in Detail D2.

**Clear instructions are a criterion of their own** (the Maintainer's condition). The three steps are: `git mv docs/DOCUMENTATION_PLAN.md dev/DOCUMENTATION_PLAN.md`; `python install/scaffold.py upgrade --target <repo> --documentation-plan-moved`; then `git add dev/.cairn/cairn-lock.yml` and `git commit`. They come from one constant in the code, and one test fails if the report line, the refusal or `install/UPGRADE.md` words them differently.

**The adopter's links.** The command edits none of the adopter's files. After a record it prints one line naming both places, and the report line carries the same words. Five shipped files name the old place (the module document, the forkable plan, its scanner allow-list, the plan and proposal templates); adopters get their corrections through the ordinary merge. Text the adopter pasted into the `documentation-discipline` or `documentation-tier-home` slots is theirs and is not rewritten; the line tells them to search for it.

**A project upgraded by `--init-lock`** (no lockfile before) keeps the old file and gets the new template written beside it: two files. `install/UPGRADE.md` says so and tells the owner to keep one.

**Removal.** Remove `--documentation-plan-moved` and its tests in the release that stops supporting upgrades from 0.8 installs; the Maintainer names that release.

**Mentions of the old path (`git grep`, 2026-11-20).** Shipped: 5 template files, plus `config.py`. Cairn's own live files: 11. Tests: 4. Left alone: 134 archived files, four historical mentions and three that name another project's file. Detail D7 lists them.

**Protected and counted files, and the reason the Maintainer will see at the signing.**
- `install/_scaffold/upgrade.py` (engine, AST baseline): a new command records one file's place. `install/_scaffold/config.py` (cascade-mutable, no HOLD): one install row and one table entry.
- `tests/test_default_security_stance.py` and `tests/test_upgrade_refuses_hostile_project_data.py` (protected; each adds a line to the signing): one expected path; one test uses a folder that still exists after the move and checks the same refusal.
- The always-loaded files name no path to change (words measured 2026-11-20: Cairn's 1,592 of 2,000, shipped 1,497 of 1,500); re-measured after C3.
- Doctrine: the "this file lives in docs/" paragraph in both plan files (Detail D4, D6) changes meaning, not only a path. It is edited by exact replacement, and reviewers answer "does any rule weaken or disappear?".

**Stale records.** The AST baseline (`Assign:_MODULE_MAPPINGS` and `cmd_upgrade` change; new functions) stays red until the Maintainer's baseline step; after C2 the implementer runs the runbook's Step 1 listing and records the counts. The gate manifest's `mapping_symbols` digest and the roster's hashes for the two protected tests are refreshed at the signing. Cairn's own lock is refreshed in C4, alone in its commit.

**Reuse.** The guards and lock writer plan B built. Searched `install/_scaffold/` for `documentation`, `move` and `relocate`: only the layout table, which this does not extend.

**Documentation surface.** `install/UPGRADE.md`, `CHANGELOG.md` (one entry), the roadmap row, and the shipped texts. No rule is added.

## Sequence

Code review once, after C4. C4 needs C2 and C3, which share `install/UPGRADE.md`, `CHANGELOG.md`, the roadmap and the lock with the merged plans B and C.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | New installs and shipped text | plan review | `config.py` rows, 5 shipped templates, 4 tests |
| C2 | The recording command | C1 | `--documentation-plan-moved`, the report line, new test file and its tier |
| C3 | Cairn's own tree | C1 | `git mv`, 9 other live files corrected |
| C4 | Records and Cairn's own lock | C2, C3 | UPGRADE.md step, changelog, roadmap, lock commit |

## Acceptance criteria

**C1.** A default install through `scaffold.main` writes `dev/DOCUMENTATION_PLAN.md` and no file under `docs/`; its lock record and the module-discovery text name the new place. Each shipped text in Detail D4 names it, and the three references to another project's file are unchanged (`grep -c` before and after). The four tests are edited as Detail D5 says; `tests/test_documentation_plan_module.py` fails if the install row is not changed, and the refusal test keeps checking that a linked parent of a mapped file is refused, in a folder that exists.

**C2.** `upgrade --documentation-plan-moved` does what Detail D2 says in each case, through `scaffold.main(["upgrade", ...])`. It writes only the one `dst` field of the lock, follows no link and uses no path from the lock. After a record, `verify_integrity` and `run_security_verification.py local` pass, and an ordinary `--stage` and `--apply` merge at the new place, in either order with the command. `--plan` and `--apply` print the report line; its helper never raises. New `tests/test_upgrade_documentation_plan_moved.py` has one test per row of Detail D5, each with its control, and is listed in `tests/test_tiers.json` in this chunk (`python tests/tier_inventory.py check` passes). `_compute_upgrade`, `_apply_upgrade`, `_layout_plan`, `layout_catalog.py` and `verify_integrity.py` stay unchanged.

**C3.** `dev/DOCUMENTATION_PLAN.md` exists by `git mv`, `docs/DOCUMENTATION_PLAN.md` does not, and the 9 other live files named in Detail D6 name the new place. `git grep DOCUMENTATION_PLAN` outside the left-alone set finds no `docs/` form except the reference-deployment mentions. The prose gates pass on each edited file, and the always-loaded word totals are unchanged.

**C4.** `install/UPGRADE.md` has the three steps as a numbered step in the order an adopter follows (finish the 0.7 layout move; run `--plan`; the three steps; search for links), plus the `--init-lock` limit. `CHANGELOG.md` has one entry. The roadmap row is marked settled and plan E's share of the joined run is listed. Cairn's own lock is refreshed as Detail D6 says, with this command, in a commit that holds only the lockfile; `install/verify_integrity.py` exits 0 on Cairn's own tree. The instructions check (Verification) is run and recorded.

**Security (re-answered).** S1, who supplies the input: the lock, the project tree and the flag; none reaches a write as a path, because the command writes only the lockfile. S2, can it fail: each refusal has the control in Detail D5. S3, what runs it: the adopter, by the flag; `verify_integrity.py` and `run_security_verification.py local` then judge the result and are unchanged. S4, which way it breaks: refuse, name the file, write nothing; the one write is the lock, by the writer `--heal-layout` and `--retire-wrapper` already use, so it adds no new power. S5, what still gets through: someone who can write the lock can point the record's `dst` at the new place; a file planted there is caught by its recorded hash. Residuals: the whole-file read of both places has no size limit, as every upgrade read; on Windows a folder junction is caught only by the guard's last check, whose text can name where the junction leads.

## Scope delta

**Scope delta**: degraded

- The accepted arc says the upgrade moves the file for an existing project. This plan has the owner move it with Git and Cairn record the new place. **disposition**: accept. The end is the same (the file at `dev/DOCUMENTATION_PLAN.md`, its record updated, nothing of the owner's lost); the route is lighter and gives the installer no power to create or delete a file. The Maintainer allowed it (chat, 2026-11-21): "Let's go with your recommended plan E. But the instructions have to be clear."

## Verification

**Selector (`python tests/tier_inventory.py for <paths>`, main checkout, 2026-11-20; re-run at the starting commit).** C1 selects 68 test files, over the 40-file limit of `tests/conftest.py`, so it is not split: C1 runs the ten tests that guard the changed promise (Detail D7) and leaves the 68 to the arc's joined run. C2 selects 38, plus the new file: 39. C3 selects 41 and runs the prose gates and five named tests (Detail D7). C4 selects 9. Before each chunk, run its files once with `-rf` and keep each failing test id and first message line; after, a failure is a host failure only if both are on that list.

**The instructions check (developmental, C4).** A fresh low-tier agent gets a scratch project installed from 0.8.0 (tag `v0.8.0`) and only the text the upgrade prints, nothing from this plan. It passes only if, at the end, `dev/DOCUMENTATION_PLAN.md` exists, `docs/DOCUMENTATION_PLAN.md` does not, the lock's one documentation-plan record names `dev/DOCUMENTATION_PLAN.md`, `git status --porcelain -- dev/.cairn/cairn-lock.yml` prints nothing, and `python install/verify_integrity.py --target <project>` exits 0; otherwise it fails. The record says what it did, where it hesitated, and what text changed because of it. Not a permanent test.

**Hosts.** This Windows machine runs the selected tests; link tests skip without symbolic-link rights and run once in its Linux subsystem (development only). Nothing here certifies. **Prose gates**, one file per call: `claim_check.py`, `link_check.py`, `tests/check_cairn.py`, `git diff --check`. **Issues.** None to close.

**Not checked.** Nothing was run. Not measured: the 0.7 path end to end; the protected test with `dev/modules` as its folder. **Does any rule weaken or disappear?** One sentence of placement doctrine is reworded in two plan files (C1, C3); the rule that a domain's governance lives in that domain is kept.

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

## Security Review -- Claude Opus 5.5 -- 2026-11-21

Reviewed commit: f407a749706d9f6b3c3d5b7f87502fd28cc30a6c (installer read at `029532a0` in the plan B worktree)

**Obligation**: the Security Review the heavy tier adds at the plan stage
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**
1. **Should this happen as framed?** Yes. Every write and removal names one of two fixed paths, and the lock is written by the same guarded writer as `--heal-layout`. -- Detail D1; `install/_scaffold/upgrade.py` `_commit_lock_and_caches` (only the lock path is written when the cache list is empty).
2. **Best alternative.** The record-only command: the adopter's `git mv` moves the file and the installer writes only the lock, as `--retire-wrapper` does. -- `upgrade.py` `_cmd_retire_wrapper`.
3. **What would show it wrong.** A test that, between `_stage_exclusive` and `os.link`, swaps the temporary name for a link to a file outside the project and finds that file's mode changed or given a second name inside the project. -- Detail D2 step 7(a).

**The strongest case.** A hostile lock or tree cannot steer this step: it writes only at two fixed names, refuses links, folders and second hard links before reading, never overwrites, and removes only bytes it read and still finds. I checked each case below in the code at `029532a0`.

**Findings**
1. **Blocking.** Step 7(a) leaves a gap the installer's other writers close. Between staging and linking, `os.chmod` follows a link and `os.link` follows one by default; neither checks that the temporary file is still the one staged, as `_write_by_replacing` does. Someone who can write `dev/` while the move runs could change the mode of a file outside the project, or link one in. Exact words below; they govern the usual review's finding 4 on `os.chmod`.
2. Non-blocking. `_documentation_plan_move_lines` re-reads the lock; a `files` that is not a list, or a record that is not an object, raises despite "never raises". Add after "when the lock is missing": "It reads `files` only when it is a list, and skips any record that is not an object, as step 1 does."
3. Non-blocking. M10 prints `{exc}`. On Windows a folder junction is caught only by the last guard check, whose text names where the junction leads; the D2 sentence "names only the constant paths" is untrue there. No terminal escape can reach it. Also, an error from step 7(c) reaches M10 after the lock is written; the next run tidies (M9).
4. Non-blocking. Step 3 reads both files whole, with no size limit: the residual already recorded for upgrade reads.

**The usual review.** I agree with findings 1, 4 (my words govern on `os.chmod`), 5 and 6; 2, 3 and the doctrine have no security bearing; 3 keeps the same refusal.

**The S answers.** S1 to S5 hold once finding 1 is closed. The proposal's S4 lists heal and retire as the only added authority; plan E's S4 adds a third: one file removed and one record rewritten.

**For the Maintainer, security only.** The moving command gives the installer three new powers (create a file, delete a file, remove an empty folder) and the race, hard-link and Windows residuals above. The record-only command gives it one, rewriting one lock field, which heal and retire already have; Git does the move. What still goes wrong there: an adopter who never runs `git mv` gets a refusal, and a planted file at the new place is caught by its recorded hash.

**Not covered.** I ran no test, read only one of the four edited tests and none of the 134 archived files, and did not check the shipped-text edits or the AST baseline. One four-line probe of `os.link` on this Windows host's Python 3.13 (scratch folder) showed `follow_symlinks=False` is accepted and a hard link to an existing name fails with `FileExistsError`.

Elapsed time: unknown. Tokens: unknown.

**Verdict**: REVISE

### Exact words for the Security Review's blocking finding

**1. Detail D2 step 7(a)**, replace the whole bullet with: "(a) only when `new is None` (the move proper): `tmp = _stage_exclusive(target / _DOCPLAN_NEW, old, target)`; `staged = tmp.stat(follow_symlinks=False)`. In a `try`: `_assert_safe_write(target / _DOCPLAN_NEW, target)`; if `tmp.stat(follow_symlinks=False)` does not have the `st_dev` and `st_ino` of `staged`, raise `ScaffoldSecurityError("the staged copy changed before the move")`; then `os.link(tmp, target / _DOCPLAN_NEW, follow_symlinks=False)`, catching `FileExistsError` and raising `ScaffoldSecurityError("a file appeared at the new place while the move ran")`. In the `finally`: remove `tmp` only if `tmp.stat(follow_symlinks=False)` still has the identity of `staged`, ignoring `FileNotFoundError`, as `_write_by_replacing` does. There is no `os.chmod`: the new file gets the default mode, as every file the installer writes. `os.link` fails when the name exists, so an adopter's file can never be overwritten, even if one appears after step 3." The usual review's M17 catch of any other `OSError` from `os.link` follows the `FileExistsError` clause unchanged. Add to Detail D5 one row: "staged copy swapped | patch `upgrade._stage_exclusive` to call the real one, then replace the returned name with a link to a file outside the project; skip if links are unavailable | M10, 2; the outside file's bytes and mode unchanged; nothing at `dev/DOCUMENTATION_PLAN.md`; lock unchanged | the identity check and `follow_symlinks=False`".

## Plan response, first part: a choice for the Maintainer -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-21

Both reviews said revise. Their four blocking findings and the words that close them are accepted, and none is declined. They are not folded in yet: the reviews raised a choice that decides which steps this plan has, and the choice is the Maintainer's.

**The choice: how an installed project gets the move.**

- **(a) Cairn moves the file**, as the plan is written. One command copies the owner's file to the new place, records it and removes the old copy. The installer gains three powers in the owner's tree: create a file, delete a file, and remove an emptied folder. Two of the four blocking findings are about making those steps safe.
- **(b) The owner moves the file and Cairn records it.** The upgrade report prints one Git command, `git mv docs/DOCUMENTATION_PLAN.md dev/DOCUMENTATION_PLAN.md`. The owner runs it, then runs Cairn's command, which rewrites one field of one lock record and nothing else. The plan already holds that route (message M15). About half the messages and half the tests go, with the hard link, the delete and the folder rule.

**What the reviews said.** The usual review: a new command is the right delivery either way; (b) is lighter; the choice is the Maintainer's. The Security Review: (b) is strictly smaller. It gives the installer one power, which two existing commands already have, and that review's own blocking finding does not arise under it. Under (b) an owner who never runs the Git command gets a refusal, and a file planted at the new place is caught by its recorded hash.

**Strategy recommends (b).** Cairn then never moves or deletes a file its owner wrote, and the arc adds less. It costs the owner one more command, printed for them. It needs his word because the accepted arc says the upgrade moves the file; (b) reaches the same end by a lighter route.

**Next.** On his answer the plan is folded once, for the design he picks. If he picks (b), the changed steps get one short Security Review, because they replace steps that were reviewed.

**Elapsed**: unknown. **Tokens**: unknown.

## The Maintainer's choice -- recorded by Claude Fable 5.2 (Strategy) -- 2026-11-21

Asked "(a) Cairn moves the documentation plan file for a project's owner, or (b) the owner moves it with one Git command and Cairn only records it? I recommend (b).", the Maintainer wrote (chat, 2026-11-21):

> "Let's go with your recommended plan E. But the instructions have to be clear."

What that settles:

- **Design (b).** The owner moves the file with Git, and Cairn's command records the new place in the lock and does nothing else to the owner's files.
- **His condition.** The instructions an owner follows have to be clear. The fold makes that a criterion of its own: what the upgrade prints, what a refusal prints, and the step in `install/UPGRADE.md`.
- **Scope.** The accepted arc says the upgrade moves the file. Design (b) reaches the same end by a lighter route, and his words above allow it. The fold states this in the plan's Scope delta.

The Waiting line is removed. The plan is folded once, for design (b); the changed steps then get one short Security Review, as the first part of the response said.

**Elapsed**: unknown. **Tokens**: unknown.

## Plan response, second part -- Claude Sonnet 5.5 (for the author) -- 2026-11-21

The plan and its companion are folded once for the Maintainer's design: the owner moves the file with Git, and `upgrade --documentation-plan-moved` records the new place. Status stays `revising-plan`; the changed steps go to one short Security Review.

Usual review:
1. Blocking 1 (hard-link write): falls away; no file is written. The new file is named `tests/test_upgrade_documentation_plan_moved.py`.
2. Blocking 2 (order test, M4 setup): accepted, Detail D5 (two order rows, the layout-refusal record).
3. Blocking 3 (protected test): accepted, Detail D5, the `README.md` words.
4. Non-blocking 4: falls away (no hard link, no `chmod`).
5. Non-blocking 5 (removal condition): accepted, Scope.
6. Non-blocking 6 (`--init-lock` leaves two files; 10 against 9): accepted, Scope, C3, Detail D6.
7. For the Maintainer: closed by his choice.
8. Doctrine wording: accepted, Detail D4 and D6.

Security Review:
1. Blocking 1 (race between staging and link): falls away; nothing is staged or linked.
2. Non-blocking 2 (helper never raises): accepted, Detail D3, with a test.
3. Non-blocking 3: first half accepted (the junction text, Detail D2 and Security); second half falls away (no step c).
4. Non-blocking 4 (whole-file reads): accepted as a named residual.
5. The S answers are rewritten for the lighter design.

Code against brief: none differed. The command reads both places with no `single_link`, since it only reads.

**Elapsed**: unknown. **Tokens**: unknown.

## Plan amendment review -- Claude Opus 5.5 -- 2026-11-21

**Prior reviewed commit**: 54a0928a2e210545ddc6f0f15dfbb9cfa5cfe33b
**Replacement commit**: e190b86acbfe654d6d88b52a27457272dde8d561
**Affected cells and dependencies**: Build summary, Scope, Acceptance criteria, Scope delta, Verification, Detail D1, Detail D2, Detail D3, Detail D5, Detail D6, C2, C4
**Obligation**: Internal Security Review
**Verdict**: REVISE

**Foundations**
1. **Should this happen as framed?** Yes. Traced through `cmd_upgrade`, the command's only write is the lock, through `_commit_lock_and_caches` with no caches; no lock path reaches a write. -- `install/_scaffold/upgrade.py` lines 2223-2293, 4756-4815.
2. **Best alternative.** None smaller: `--retire-wrapper` already has this one power. -- `_cmd_retire_wrapper`.
3. **What would show it wrong.** A second record already at `dev/DOCUMENTATION_PLAN.md` (finding 3), or a project that passes the instructions check without moving (finding 1).

**Checked.** Every helper in D2 reads only fixed paths. `_read_regular_bytes` refuses links, folders and special files, and does not hang on a pipe. The gap between the reads and the lock write cannot write an owner's file; a later swap is caught by the hash. The report line and refusals print fixed text, except M9's guard text (residual named). Both checks still judge the record at every step. All first-round findings are closed or fall away as the response says. S1 to S4 hold; S5 holds after finding 2.

**Findings**
1. **Blocking.** The instructions check passes on a project that never moved the file: `verify_integrity` passes with the record still at `docs/` (my reasoning from the code, not run). Exact words below.
2. Non-blocking. M12 says "because it was edited" and sends the owner to `--finalize`, which accepts whatever bytes are there, a planted file included. Words below.
3. Non-blocking. If another record already names `dev/DOCUMENTATION_PLAN.md`, the command makes a duplicate destination, and the security verification then degrades with no message. Add to D2 step 1: "If any other record's `dst` is `_DOCPLAN_NEW`: print M3, return 1." Add a D5 row.
4. Non-blocking. The cannot-tell refusal has no D5 row. An `OSError` or `ValueError` from step 2 or the lock write gives a traceback. Catch both with ScaffoldSecurityError as M9, as `_layout_command`'s caller does.
5. Non-blocking. D5 makes a Git repository "only in the unsaved-edits test", yet both order rows commit. Name them too.

**Not covered.** No test or probe was run. I did not re-read C1, C3, D4, D7, the edited tests or the shipped texts, and I did not trace `_writeset_dirty_collisions` or `_read_layout_state`.

Elapsed time: unknown. Tokens: unknown.

### Exact words

**1. Verification, "The instructions check"**: replace "It must finish the move so that `python install/verify_integrity.py --target <project>` passes." with "It passes only if, at the end, `dev/DOCUMENTATION_PLAN.md` exists, `docs/DOCUMENTATION_PLAN.md` does not, the lock's one documentation-plan record names `dev/DOCUMENTATION_PLAN.md`, `git status --porcelain -- dev/.cairn/cairn-lock.yml` prints nothing, and `python install/verify_integrity.py --target <project>` exits 0; otherwise it fails."

**2. Detail D2, M12**: replace "The file differs from the version the lockfile recorded, because it was edited. Run python install/scaffold.py upgrade --target <repo> --finalize dev/DOCUMENTATION_PLAN.md, then do step 3." with "The file differs from the version the lockfile recorded. If the changes are yours, run python install/scaffold.py upgrade --target <repo> --finalize dev/DOCUMENTATION_PLAN.md, then do step 3; if not, restore the file from a copy you trust."

## Plan response, third part -- Claude Sonnet 5.5 (Implementation, for the author) -- 2026-11-21

The amendment review's findings are closed in the plan and its companion; status is now `ready-to-implement`.

1. Blocking 1 (the instructions check passes without a move): accepted; its exact words replace the pass condition in Verification.
2. Non-blocking 2 (M12 sends the owner to `--finalize` for any bytes): accepted; its exact words replace M12 in Detail D2.
3. Non-blocking 3 (another record already at the new place): accepted; one line added to D2 step 1 and one row to the D5 table.
4. Non-blocking 4 (cannot-tell refusal has no row, `OSError` and `ValueError` give a traceback): accepted; the dispatch sentence in D2 now catches both as M9, and D5 has a row.
5. Non-blocking 5 (the Git repo in the order tests): accepted; D5 names them.

**Elapsed**: unknown. **Tokens**: unknown.

## Implementation record -- Claude Sonnet 5.5 (Implementation, take-over) -- 2026-11-21

**Conclusion.** The four chunks are built and the plan's checks are met, with two exceptions: six link variants of the protected hostile-data test fail on both hosts after the change, which the plan did not foresee (Maintainer question below); and the Linux run found one more test the plan did not list, now fixed. Elapsed time and tokens: unknown, except the test run times below.

**Who built what.** A first Implementation agent (Claude Sonnet 5.5) did steps 1, 2 and 4 of the brief with Haiku execution agents and was stopped before it wrote a record. I treated every one of its commits as unverified: I read each diff against its chunk's criterion and Detail, and ran the tests afresh. None of its test output was used.

| Chunk | Commit | What it did |
|---|---|---|
| status | `0a7b2c9f` | `implementing` |
| C1 | `5d34f839` | install row, discovery text, 5 shipped files, 4 tests, as Detail D4 and D5 say |
| C2 | `031ef837` | `--documentation-plan-moved`, the report line, new test file (listed in the `workflow` tier) |
| C3 | `e4dced3a` | `git mv` and 9 other files; Cairn's own scanner allow-list names the new place |
| C4 | `1c46527d`, `08c30286` | UPGRADE.md step, changelog, roadmap, `claim-check-allow` comments |
| lock | `7217a3ce`, `472ec9bb` | Cairn's own lock, each commit holding only the lockfile; the second written by `--finalize` |
| fixes | `e6b7caae`, `f7b644c3`, `c52fc7ab`, `3434491f`, `1f20ec66` | below |

**What I corrected in the earlier agent's work.**
1. `08c30286` emptied Cairn's own `dev/.cairn/scanner-check-allow.json` as "unused". It is not: without the entry, `link_check` reports 3 broken links in `dev/modules/documentation-plan.md` (measured). The "unused links entry" line `check_cairn` prints is a note with exit 0, and it printed the same at the starting commit. Entry restored in `c52fc7ab`; lock refreshed in `472ec9bb`.
2. The roadmap line claimed runs that had not been recorded; it now says what ran.

**Scope the Maintainer added (chat, 2026-11-21).** He wrote that Cairn "is inside the package. It is the way that an owner interfaces with their code using Agents", and "Yeah no new tooling unless it's needed! Cairn is tooling light on purpose." So the agent that carries out an upgrade does the move and corrects the links by following the notes; the installer only records the new place and checks. Commit `f7b644c3` changed prose and the test that pins it, and added no code for correcting links. The one steps constant, the lines `--plan` and `--apply` print, the refusals and `install/UPGRADE.md` now give five numbered steps in this order: `git mv`; correct each link in the project's own files, leaving files Cairn installs alone; `--documentation-plan-moved`; `verify_integrity` and the project's link check; `git add` and `git commit`. M7, M11 and M12 name the new step numbers. The plan said "three steps"; this is the Maintainer's change to it.

**Where the build differs from the plan.**
- Five steps, not three (above); a one-line note after them replaces the plan's LINKS line.
- `3434491f`: the instructions check showed that step 4 names `dev/tools/link_check.py`, which only the opt-in doc-drift-prevention module installs, and the agent hesitated. Step 4 now says "if it has one".
- The plan said the other tests in the hostile-data file "create their own `docs` subfolders and are not edited". Four of them write into `docs/` without making it (lines 257, 338, 417, 525), and six cases fail. I stopped on that protected file (see the question).
- `tests/test_upgrade_lockfile_path_containment.py` (ordinary, not in the plan) wrote `docs/notes.md` without the folder; `1f20ec66` adds one `mkdir`. On Linux, 4 cases failed only after the change and passed alone at the starting commit; the file and the new test file pass at `1f20ec66` (82 passed, 1 skipped).
- Execution agents chose words where Detail was silent (test names, helpers in the new test file); I read them and found none that changes a message or a number.

**Question for the Maintainer (protected file).** `tests/test_upgrade_refuses_hostile_project_data.py` has six link cases (`existing-inside-file`) that put a file under `docs/`, which a default install no longer has. Choices: (a) make the folder first, `(world.project / "docs").mkdir(exist_ok=True)`, at the four sites (four more lines on the signing page); (b) point them at `dev/modules`, as the plan did for the other test. Strategy recommends (a). The refusal being tested does not change.

**Tests.** Each chunk's selection ran once at the starting commit `bd8fd8c9` (work folder `arc-e-base`) and once at the build, with `-rf --tb=line`, compared by test id and message. Windows Server, Python 3.13; Linux subsystem, Python 3.14, one run at a time. The build was `472ec9bb` for every run but the last Linux one (`1f20ec66`). The later commits changed one step's wording, one test file and one `mkdir`, so I did not rerun the Windows groups; the new test file's two wording tests passed after the wording commit.

| Group (files) | Windows before | Windows after | Linux before | Linux after |
|---|---|---|---|---|
| C1 (10) | 13 failed, 397 passed | 20 failed, 396 passed | 1 failed, 445 passed | 6 failed, 440 passed |
| C2 (39; 40 with the new file) | 268 failed, 1503 passed | 278 failed, 1527 passed | 6 failed, 2022 passed | 12 failed, 2042 passed |
| C3 (5) | 2 failed, 100 passed | 2 failed, 100 passed | 0 failed, 105 passed | 0 failed, 105 passed |
| C4 (10; 11 with the new file) | 160 failed, 430 passed | 160 failed, 454 passed | 1 failed, 637 passed | 1 failed, 664 passed |

Failing only after the change, after reruns alone: **6 ids, on both hosts**, all hostile-data cases above (they fail alone at the build; at the start they pass on Linux and skip on Windows, where that run had no link rights). Other ids that appeared only after: on Windows, besides the six, 1 in C1 and 8 in C2; on Linux 4 in C2 (the containment test, now fixed). Rerun alone, twice, at both commits on Windows: the intents, portable-sweeps and `test_scratch_install_and_upgrade_preserve_project_content` ids pass at both, so they are the host's; the containment ids skip at both, so they are shown fixed only on Linux. The ids that fail in the before run are the host's: the same message fails at the starting commit.

Elapsed seconds, Windows before and after (two groups at once): C1 1062 and 970, C2 3766 and 4025, C3 63 and 72, C4 1577 and 1858. Linux: C1 389 and 374, C2 1822 and 1881, C3 33 and 29, C4 696 and 786.

**Developmental checks.**
- Instructions check, run twice. A Haiku agent got a project installed from tag `v0.8.0` and upgraded, with a link to the old place added to its own `README.md`, and only the printed text. Run 1 (`472ec9bb`): it finished the move but could not run the link check (the file is not installed), hesitated, and committed anyway. Run 2 (`3434491f`, after the wording fix): all five pass conditions held (the new file exists; the old one does not; the lock's one record names the new place; `git status --porcelain` for the lock prints nothing; `verify_integrity` exits 0). One slip: its first edit of the link failed because it had not read the file, so it ran step 3 before step 2 and fixed the link at once; the command does not read the README. The Cairn-installed plan and proposal templates and the module README still held the old path afterwards, because their text sits in slots the ordinary upgrade does not rewrite; `install/UPGRADE.md` item 4 says so.
- Tier check: `python tests/tier_inventory.py check` passed (141 test files, each in one of 5 tiers).
- Changed installer symbols (`ast_step1.py`, read only): before the change 4 changed and 237 new; after, 5 changed and 244 new. The added change is `Assign:_MODULE_MAPPINGS`; the seven new symbols are `_DOCPLAN_SRC`, `_DOCPLAN_OLD`, `_DOCPLAN_NEW`, `_DOCPLAN_STEPS`, `_DOCPLAN_NOTE`, `_cmd_documentation_plan_moved` and `_documentation_plan_move_lines`. The other changed symbols come from merged plans B and C.
- Cairn's own tree: `verify_integrity` reports OK (70 files) after the lock refresh. The prose gates (`claim_check`, `link_check`, `check_cairn`, `git diff --check`) pass on `install/UPGRADE.md`, `dev/PLANNING.md` and this plan.

**Not run, with its home.** The 68-file C1 selection beyond the ten named tests, the Python 3.13 run on Linux, the link variants of the containment test on Windows, and the macOS run: all on the roadmap's joined run (`dev/PLANNING.md`, "What the joined run owes", plan E). The protected-file fix awaits the Maintainer. The AST baseline and the signing hashes stay with the Maintainer's baseline and signing steps.

## Code review -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-21

Reviewed commit: b09b55ee83e69930d2e8250bcee5bd56780af86c; range `bd8fd8c9..b09b55ee`.

**Obligation**: the usual code review; the Security Review follows
**Tier**: Internal
**Findings**: raised

**Foundations**
1. **Should this happen as framed?** Yes. The recording step writes one lock field, uses only fixed paths, and the five steps come from one constant. -- `install/_scaffold/upgrade.py` `_cmd_documentation_plan_moved`, `_DOCPLAN_STEPS`.
2. **Best alternative.** None smaller: no code edits links, as the Maintainer asked. -- `git diff bd8fd8c9..HEAD --stat` (one new command, one report helper).
3. **What would show it wrong.** Odd locks and trees. I ran 10 cases of my own through `scaffold.main` on a `git archive` copy: a junction as `docs`, as `dev` and as the new file; a list-valued `dst`; a missing `dst`; `dst` as `../evil.md`; a list `hash`; a 200 MB file; a second run; a record at the new place with an old copy. Each gave the expected exit, no traceback, and no write but the one `dst`. Mixed with `--plan`, `--apply`, `--heal-layout` or `--finalize` it refuses. The new test file passed (24 passed, 3 skipped, links unavailable here).

**Central claim.** It holds. `_compute_upgrade`, `_apply_upgrade`, `_layout_plan`, `layout_catalog.py` and `verify_integrity.py` are unchanged; `verify_integrity` reports OK (70 files) and `tier_inventory.py check` passes. Cairn's lock is refreshed in two commits holding only the lock. Both allow-list files change one `target`, no wider than before. Messages differ from Detail only in the five-step wording, which the record explains with the Maintainer's words (they are on the roadmap).

**Findings**
1. **Blocking (needs the Maintainer's allowance).** Six protected cases fail. They fail in setup, before any link exists (`FileNotFoundError` on `docs/`), so they test nothing now. **Option (a) is sound**: it recreates the original state (a folder holding one target file, linked from inside the project), so every case checks the same refusal, and none can pass for another reason. Option (b) would put stray files into an installed folder (`dev/modules`), which changes what "inside the project" means. In an outside copy with (a), the six now reach the link call and skip (no link rights here); I did not run Linux. Exact lines are below.
2. **Blocking.** The changelog says "nothing you wrote is edited". The five steps have the upgrading agent edit your own files' links. Replace that clause with "the command edits none of your files; the printed steps have your agent correct links in the files you wrote".
3. Non-blocking. Step 2 does not say how to tell a Cairn-installed file: add "(the files listed in `dev/.cairn/cairn-lock.yml`)". The wording test would then need the constant, `install/UPGRADE.md` and the test list changed together.
4. Non-blocking. The docstring of `test_the_steps_read_the_same_everywhere` still says it "is expected to fail until C4"; delete the sentence. `test_the_report_helper_never_raises` calls a private helper; the same promise is kept by `--plan` and could use it. The plan's body still says "three steps"; the record states the change.

**Tests.** Two protected tests edited: the stance sentinel (one path) and the below-linked-parent case, which now links `dev/modules` and still refuses the same thing. No removed caller-visible fault. The new tests guard external promises; the file runs about 106 s (install per test), acceptable. **Does any rule weaken or disappear?** No: the placement paragraph keeps "a domain's governance lives with the domain" and adds that `docs/` holds only what describes the software; the three other-project mentions are unchanged.

**Bounding**: heavy tier, so the Security Review follows. I ran no Linux, macOS or Python 3.13 run, no link-rights case, and not the 68-file C1 selection. I did not read the 134 archived files or judge the printed `{exc}` text (left to the Security Review).

Elapsed time: unknown. Tokens: unknown.

**Verdict**: REVISE

### Exact lines for finding 1, option (a)

In `tests/test_upgrade_refuses_hostile_project_data.py`, directly after each of the four lines `target = world.project / "docs" / "profile-copy.yml"` (lines 257, 417, 525) and `target = world.project / "docs" / "linked-agents.md"` (line 338), add at the same indent:

```
        target.parent.mkdir(exist_ok=True)
```
