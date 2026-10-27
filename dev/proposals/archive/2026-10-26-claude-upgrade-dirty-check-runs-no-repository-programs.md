# Make the upgrade edit check run no program from the project's git settings

**Author**: Claude Sonnet 5.5
**Status**: accepted
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review) -- the change edits the scaffold engine (`bootstrap/_scaffold/`), a named high-risk surface, next to the git call the twelfth change added
**Opened**: 2026-10-26
**Lane**: deliberate -- engine change on a high-risk surface; a Security Review is owed
**In brief**: `upgrade --stage`, `--apply` and a bare `--finalize` stop running programs that a project's git settings name when they check for unsaved edits, and they read a project that sits in a repository subfolder correctly.

## Context

Three commands ask "has the adopter edited this file and not committed it?" before they write or hash it. They all call `_dirty_tracked_paths` (`bootstrap/_scaffold/upgrade.py:2365`), which runs a plain `git status --porcelain`. The twelfth-row Security Review found two faults (`dev/PLANNING.md:51`; the review is in `dev/plans/upgrade-removes-retired-files.md`, section "Plan review -- Security Review"). The Maintainer put the fix in a 0.5 row after the twelfth: "A 0.5 row, after the twelfth (Recommended)".

**I reproduced both today** (git 2.53.0, Python 3.13.13, macOS; a scratch repository, never this one).
* **Programs run.** I set `core.fsmonitor` and a `filter.<name>.clean` command in a project's `.git/config`, each writing a marker file. One call of `_dirty_tracked_paths` wrote both markers.
* **Subfolder misread.** With the project in `proj/` of a larger repository and `proj/AGENTS.md` edited, the helper returned `proj/AGENTS.md` (named from the repository root). `_writeset_dirty_collisions(proj, ["AGENTS.md"])` returned `[]`, so `--apply` would overwrite the edit.

**What the three callers need** (read from the tree). Each already holds the names it cares about and asks about those names only:

| Caller | Names it holds | What it does with the answer |
|---|---|---|
| `_cmd_finalize_lockfile`, bare form (`upgrade.py:2244`) | the lockfile records | refuses and lists the dirty ones; `--force` skips the check |
| `_apply_upgrade`, step (f) (`upgrade.py:2689`, through `_writeset_dirty_collisions`) | the staged write-set | refuses and lists the overlap; `--force` skips the check |
| `upgrade --stage` (`upgrade.py:3240`, through the same function) | the staged write-set | prints an advisory and completes |

Today the check asks about the whole repository and the callers then intersect. None of them needs the whole-repository set except the bare `--finalize`, which prints it. Its stated reason is that finalize advances the hash of the records (`upgrade.py:2200-2206`).

**What exists to reuse.** The twelfth change (code review pending, `16930822`) added `_committed_copy_matches` (`upgrade.py:2434`): one `git cat-file blob HEAD:./<path>` with fixed overrides, a cleaned environment, a byte cap, a timeout and a git-version floor.

## Proposal

**1. One answer, asked of the names.** `_dirty_tracked_paths(target, names=None)` returns the subset of `names` (project-relative, `/`-separated) that have uncommitted changes. With `names=None` it uses the lockfile's recorded files, so the one existing direct call keeps working. `_writeset_dirty_collisions` passes its write-set. Bare `--finalize` passes its recorded files, using the on-disk name for a renamed vendor wrapper. It returns `None` ("no guard") exactly as today when git cannot start or the folder is not inside a work tree.

**2. Four read-only git commands, no `git status`.** All run through the twelfth change's launcher: `git -C <project>`, `-c core.fsmonitor=false -c core.hooksPath=<null device> -c core.useReplaceRefs=false`, every `GIT_*` variable removed, `GIT_OPTIONAL_LOCKS=0`, no input, the timeout, a byte cap, and `--literal-pathspecs` so a name is never a pattern:
* `rev-parse --is-inside-work-tree`, then `rev-parse --verify -q HEAD` (exit 1 means no commit yet).
* `ls-files -z -s -- <names>` gives what the index holds, with conflict entries.
* `diff-index --cached --raw -z --no-renames --no-ext-diff --no-textconv --relative HEAD -- <names>` gives what is staged against the last commit. `--relative` names paths from the project folder, which fixes the subfolder misread.
Names go in groups of at most 100, so one command line stays under Windows' 32,000-character limit.

**3. The engine reads the files itself.** For each name, Python hashes the file's bytes the way git hashes a blob (SHA-1 or SHA-256, chosen by the length of the index's id) and compares with the index. Git reads no working-tree file and no blob. The rule, which I checked against `git status --porcelain` (Evidence): a name is **dirty** if it is staged (added, changed, deleted or type-changed against the last commit), in conflict, missing on disk, not a regular file, or its bytes differ from the index. A name git does not track is **not dirty**, as today (`??` was excluded). That includes a recorded file not yet committed.

**4. When git is there but does not answer** (more than 10 s, an error after the folder was confirmed a work tree, output past the cap): the check says so in its own words and does not guess. `--apply` and bare `--finalize` refuse with the reason and `--force`. `--stage` completes and prints an advisory. Today this case is "no guard", silently.

**5. Reuse, not a copy.** The launcher inside `_committed_copy_matches` (environment, timeout, capped read) moves to a module-level helper that both functions call. `_committed_copy_matches` behaves as before. I do **not** call it per name (Alternatives).

**6. No git-version floor for this check.** The twelfth change's 2.45.0 floor exists because `cat-file blob` reads a blob that a partial clone may have to fetch, and the fetch can run a program. These four commands read no blob. I measured that on 2.53.0 (Evidence) and reasoned it for older git. This is my call: a reviewer who finds an older git reading an object here should restore the floor. Without it, hosts with older git (I believe RHEL 9 and Ubuntu 22.04 ship such versions; I did not check) keep the guard.

**7. Line endings.** A file whose bytes equal the index after turning every `\r\n` into `\n` counts as unchanged (Question 2).

**Not in scope.** No new action, flag or list change; no template, install row or lockfile field; the published `scaffold.py --manifest` is unchanged. `--force` still skips the check and now runs no git at all. The `--apply` refusal text stays byte-identical (the differential oracle compares it). The bare-finalize text names "recorded" files. The twelfth change's own behaviour is not widened.

## Rationale

The callers ask about names they already hold, so a check bounded by those names is enough and costs the same however large the repository is. Everything `git status` does that the callers do not need (whole-tree scan, clean filters, the monitor) is what runs the project's programs. Git's own plumbing (`ls-files`, `diff-index --cached`) gives the staged and index facts without touching the working tree, and the engine's own hash gives the rest. That is also what lets the check read a subfolder project by its own names.

## Alternatives considered

* **Doing nothing.** The first fault is an ordinary `upgrade --stage` running a program the project's `.git/config` names. The second is `--apply` overwriting an edit in any subfolder project, silently. Both are live in 0.5.
* **Call `_committed_copy_matches` per name** (the reuse the 0.5 row suggested). It misses a file staged and then reverted on disk (`git status` shows `MM`; the helper compares only with the last commit). It cannot tell an untracked file from an unreadable one, so it needs two more calls per differing name. It needs the 2.45.0 floor. It costs about 8 ms a name: 1.6 s for 200 names in a 50,000-file repository, against 0.14 s for the proposed check.
* **Check every tracked file, as today.** Hashing all 50,000 files (200 MB) took 4.0 s, against 0.14 s for 200 names. The callers do not need it (Context), and it would read every large data file a science repository tracks.
* **`git status` with more overrides.** A clean-filter program is named by an arbitrary key (`filter.<name>.clean`), so a fixed override list cannot cover it. Overrides age; not running the command does not.

## Documentation / doctrine surface

Descriptive layer only, per `docs/DOCUMENTATION_PLAN.md`: one sentence in `bootstrap/SAFETY.md` (the edit check runs no program the project names, and how), and a few words in `bootstrap/UPGRADE.md` near the `--finalize` paragraph (the check covers recorded files; a file with a clean filter or a line-ending-only edit; `--force`). The plan checks that no test or manifest pins their bytes. `CHANGELOG.md` is written at archive. Nothing under `doctrine/` and no `AGENTS.md` text changes. **Rate-limit gate: this is not a doctrine change, so the gate does not apply.**

## Evidence / verification plan

**Measured** (scratch repositories under the scratchpad folder; a prototype of the four commands outside the tree; git 2.53.0, Python 3.13.13):
* **Agreement with `git status --porcelain`**, project in a subfolder: modified, staged, staged then reverted (`MM`), deleted, staged delete, staged add, type change to a link, a file named `glob[1]*.md`, a merge conflict, and a repository with no commit. The prototype and `git status` flagged the same names in all ten; the untracked file was not flagged.
* **No program ran**: with `core.fsmonitor` and a clean filter configured, the prototype wrote no marker. Plain `git status` did.
* **No blob read**: in a blobless clone with `remote.origin.uploadpack` naming a program and the blobs absent, the prototype ran no program, with and without `GIT_NO_LAZY_FETCH`. `git cat-file -p` of a missing blob ran it.
* **Cost**: 50,000 tracked files, 200 names: `git status` 92 ms, proposed check 136 ms, per-name helper 1.6 s, hash-everything 4.0 s. With 62 names (Cairn's own record count; a solo install has 39) it took 61 ms.
* **Where it disagrees with `git status`, both over-reporting**: a clean filter (git says clean, the raw bytes differ from the index, so we say dirty), and a CRLF checkout (dirty unless rule 7 applies).

**Reasoned, not run**: git older than 2.53.0 (rule 6); Windows; SHA-256 repositories; sparse checkouts, submodules and linked work trees; a hung git; a name beyond a link (git exits 128, which is "cannot tell"). I ran no test suite and no in-tree mutant.

### Tests required

Behaviour is driven through `scaffold.py upgrade --stage|--apply|--finalize`. New file (new files are allowed under the gate manifest).

Proposed paths:
* `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py`

Nodes in `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py`: `test_git_config_programs_never_run_during_stage_apply_or_finalize` (monitor, clean filter, textconv, pager; mutant: call `git status`); `test_a_subfolder_project_sees_its_own_edits` (mutant: drop `--relative`); `test_the_check_agrees_with_git_status_on_each_edit_state` (the ten states; git's own answer is the independent expectation); `test_pattern_characters_in_a_name_match_literally` (mutant: drop `--literal-pathspecs`); `test_a_staged_then_reverted_file_counts_as_edited` (mutant: skip `diff-index`); `test_a_missing_or_untracked_name_is_handled_as_git_status_does`; `test_line_endings_only_difference_counts_as_unchanged`; `test_a_git_that_does_not_answer_stops_apply_and_finalize_and_only_advises_on_stage` (stand-in `git` that sleeps; mutant: treat it as clean); `test_force_runs_no_git`; `test_bare_finalize_looks_only_at_recorded_files`; `test_a_blobless_clone_with_missing_blobs_runs_no_upload_program`; `test_the_launcher_is_shared_with_the_committed_copy_check` (mutant: a second copy of the argument list).

**Frozen tests that pin today's behaviour.** Derived from `bootstrap/tests/fixtures/gate_manifest.json` (`frozen_files`, 195 keys) and the glob in `bootstrap/tests/_gate_manifest.py`. `bootstrap/tests/test_upgrade.py` is keyed: `TestDirtyTreeGuard` (5 nodes), `TestFinalizeDirtyTreeGuard` and `test_self_heal_composes_with_dirty_tree_guard`, which calls `s._dirty_tracked_paths(tmp_path)` with one argument. I read all of them: each stays green **unedited** under this contract (the one-argument call is why `names` defaults). `bootstrap/tests/_oracle.py` and `bootstrap/tests/test_oracle.py` are keyed: scenario `dirty_tree_refusal` must stay `match` against the trusted ref (rule: the `--apply` refusal block does not change). `test_upgrade_side_door_parity.py` is keyed and not about the guard (grep). I found no keyed test to edit, so no edit owes a re-anchor. The twelfth change's git nodes in `test_upgrade_removes_retired_files.py` (not keyed) must keep passing after the launcher moves.

### Examples / smoke checks

`python scripts/claim_check.py` and `python scripts/check_cairn.py` over the changed Markdown; `python scripts/quality_gate.py --sub neutrality`. No example or scaffold output changes. Boundary B is `full` (engine, a high-risk surface); `Certified by: pending` until the certifying run.

**AST symbols** (read-only `python bootstrap/tests/_ast_attest.py verify` with `--known-new`, Python 3.13, run today; it already exits non-zero with 158 lines from earlier 0.5 work). `_dirty_tracked_paths` and `_writeset_dirty_collisions` match the baseline today and would become CHANGED. `_cmd_finalize_lockfile`, `_apply_upgrade` and `cmd_upgrade` are already CHANGED, and `_committed_copy_matches` is already NEW. This change edits them again (callers, the can't-tell reply, the lifted launcher). It adds one launcher helper and one group-size constant (names are the plan's). None is on `_UPDATE_ALLOWLIST`, so the baseline correction is Maintainer-run, once, at the cut.

#### Security preflight

* **S1 -- Who supplied it?** The verdict ("dirty") is decided from the index and last commit (project data, read by sterile git commands), the file's bytes (project data) and the names (lockfile and stage metadata, checked by the existing containment code). The project supplies all of it, but a wrong "clean" can only make the engine write where the operator's own edit sits; "dirty" only refuses.
* **S2 -- Can it fail?** Mutants named per node above; each flips one line and one node goes red. The agreement node's expectation is `git status` on a repository with no config programs, so it does not derive from the code under test. I have run none in-tree.
* **S3 -- What fires it, over what?** `upgrade --stage`, `--apply` and bare `--finalize`, over the names in the table. `--force` and scoped `--finalize <path>` skip it. The adopter-facing sentence (`UPGRADE.md`) is written from this section by the plan and checked against it.
* **S4 -- Which way does it break?** Git unreadable after confirmation: refuse (less authority). Git absent or not a work tree: no guard, as today. Clean filter or CRLF: over-reports (refuses). Rule 7: a line-ending-only edit is not protected (more authority, small).
* **S5 -- Who still wins?** Assumed: the project controls `.git/config`, attributes, hooks, the index. Still wins: a project that rewrites its own index to look clean (the guard protects the operator from the tool, not from the project), and a `git` placed earlier on `PATH` (as for the twelfth change). No program runs by construction (no command reads a blob or working file); the override list guards by enumeration.

#### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A program from `.git/config` runs under any of the three commands. The check calls a file clean that `git status` calls edited, apart from the two stated over-reports. An older git reads a blob or fetches here (restore the floor). A repository with a large tracked tree makes `--apply` visibly slower than today. Windows checkouts refuse every file (line-ending rule fails).

## Scope delta

**Scope delta**: preserved. The baseline is this text. The one narrowing against today's behaviour is disclosed, not hidden: bare `--finalize` stops looking at tracked files Cairn does not record (Question 1).

## Assurance path

**Assurance path**: high-assurance (the scaffold engine, and the twelfth change's trust-root launcher).

## Questions for the Maintainer

1. **Bare `--finalize` and files Cairn does not manage.** Today it refuses when any tracked file in the repository has an uncommitted edit, including your own source code, though finalize hashes only recorded files. Checking everything cannot be done without running filters or hashing every file. **Default: check recorded files only.**
2. **A change that only alters line endings.** Count a file as unchanged if it differs from the index only by CRLF versus LF? This keeps Windows checkouts (where git often rewrites line endings) from being refused on every file. Cost: such an edit is not protected. **Default: yes, count it unchanged.**
3. **Git is there but does not answer.** Stop (`--apply` and `--finalize` refuse, naming the reason and `--force`; `--stage` warns), or carry on unguarded as today? **Default: stop.**

## Sequence

Lands after the twelfth change's code review clears (this moves its launcher), before the 0.5 cut. It needs a plan (more than one commit; Boundary B `full`). One baseline re-anchor at the cut, Maintainer-run, covers the twelfth change and this one.

## Review -- Proposal reviewer (Internal) -- 2026-10-26

```
Reviewed commit: a8e4f85d
Target: the whole proposal, except Security preflight S1 to S5 (left to the Security Review pass, which is still owed after the answer)
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Internal
**Model**: Sonnet 5.5, fresh session
**Findings**: raised (2 blocking, 6 non-blocking)
**Verdict**: REVISE. The change should happen and the design is sound for git 2.45 and later. Two things need an answer first: the dropped version floor is unsafe in one case I measured, and the set of names bare `--finalize` asks about is not pinned down.

**Foundations**
1. *Should it exist as framed?* Yes. Both faults reproduce on the current tree, and doing nothing leaves a live program run and a silent overwrite. The names-only check is a better design than a sterile `git status`. -- scratch repository: `core.fsmonitor` and a clean filter wrote markers under `_dirty_tracked_paths` (`bootstrap/_scaffold/upgrade.py:2365`); `_writeset_dirty_collisions(proj, ["AGENTS.md"])` returned `[]` for an edited file in a subfolder project.
2. *Best alternative?* The proposal's own, with the floor restored (B1). A batched `cat-file --batch` over the names is the one cheaper-than-per-name option the Alternatives omit (N5). -- `upgrade.py:2434-2524`; cost row below.
3. *What would make the author withdraw?* A program run by the four commands, or an edit read as clean. I found no program (13 config keys, below). I did find an older git running one (B1). -- ledger P1, P3.

**Falsification ledger** (scratch folder `rev-dirtycheck` under the scratchpad; git 2.53.0, Python 3.13.13; a prototype of the four commands outside the tree; no test run)
* P1. Programs: config named a monitor, clean, smudge, textconv, external diff, pager, ssh command, alternate-refs command, ask-pass, pack hook, credential helper, proxy and editor, plus `post-index-change` and `reference-transaction` hooks. Prototype ran none; plain `git status` ran the monitor and the hook.
* P2. Agreement with `git status`: staged then edited then reverted, file to folder, intent-to-add, `autocrlf=true` CRLF file: same answers. Assume-unchanged and skip-worktree edits: prototype flags, `git status` does not (the safe direction). Chmod only: prototype clean, git dirty (N1). Tracked unchanged link: prototype dirty, git clean. Case-insensitive repository, name in other spelling: clean (N2).
* P3. Treeless clone (`--filter=tree:0`, no checkout), `remote.origin.uploadpack` naming a program, `diff-index --cached HEAD`: with `GIT_NO_LAZY_FETCH=1` on 2.53.0 it stops ("bad tree object") and no program runs; without that variable (what git before 2.45 does) it fetched and ran the program.
* P4. Cost: 50,000 tracked files, 62 names 55 ms, 200 names 85 ms, `git status` 99 ms. The proposal's rows hold.
* P5. Read from the tree: the three callers, `_cmd_finalize_lockfile` (2182-2362), `test_upgrade.py` `TestDirtyTreeGuard` and `TestFinalizeDirtyTreeGuard`, oracle `_dirty_tree_refusal_scenario`; `_ast_attest.py verify` on 3.13 gives 158 lines with the two helpers matching the baseline today, as stated.

**Findings**
* **B1 -- blocking. The floor is not safe to drop (Proposal 6).** "These four commands read no blob" is true, but `diff-index --cached HEAD` reads trees, and a treeless clone fetches them (P3). On git before 2.45 that runs the project's upload-pack program, the same hole the twelfth change closed. The author measured only a blobless clone. Fix: keep the floor in the shared launcher. Below it, do not give up the guard: first read `extensions.partialclone` and `remote.*.promisor` (a config read runs no program) and run the four commands only when neither is set; otherwise answer "cannot tell" (Proposal 4). Add a node with a stand-in older `git` and a treeless clone. I did not run the config-read idea; the plan should measure it.
* **B2 -- blocking. Pin the names bare `--finalize` asks about (Proposal 1, Question 1).** Finalize hashes only records that are not living state and not retired-and-gone (`upgrade.py:2285-2305`), then rewrites the lockfile. "Recorded files" as written includes the installed NEXT_SESSION and PLANNING notes (living state, usually edited) and a hand-deleted retired file, so the guard would still refuse on exactly the cases the twelfth change's guide sentence is wrong about (`bootstrap/UPGRADE.md:102`). It also drops today's protection for the lockfile itself, which finalize rewrites and no record names. Fix: define the set as the records finalize will hash, plus the lockfile path, and say in Question 1 what is lost (own source files) and gained (no refusal for a living-state edit). Add a node for each of living state, a gone retired file and a dirty lockfile.
* **N1 -- non-blocking. The Signals line is false for a mode-only edit (P2).** `git status` flags an executable-bit change; the engine hashes bytes only. Cairn ships executable scripts. Overwrite keeps the mode, so little is lost. Fix: compare the index mode with the file's executable bit, or list it beside the two stated over-reports.
* **N2 -- non-blocking. A name in another letter case is read as untracked on a case-insensitive repository (P2).** `--literal-pathspecs` is case-exact. Today's set intersection has the same gap, so this is not new; the Context says the fix makes subfolder projects "read by their own names", so say so or add the node.
* **N3 -- non-blocking. A frozen test goes quiet.** `test_self_heal_composes_with_dirty_tree_guard` stays green but its assertion ("profile.yml not in the result") becomes true by construction once `names=None` means recorded files. `names=None` also changes the helper from the whole repository to the records, hidden behind the default. Fix: say what `names=None` returns with no lockfile, and carry the property in a new node (an untracked recorded name is not returned).
* **N4 -- non-blocking. Question 2 is framed as protecting Windows.** `git status` already calls a CRLF checkout clean (P2, `autocrlf=true`); rule 7 exists only because the engine compares raw bytes instead of asking git. The Maintainer should hear that, and that Windows is unmeasured. Say so in the question.
* **N5 -- non-blocking. Alternatives omit the batched form.** One `git cat-file --batch` over the names costs one process, not 8 ms a name, but needs the same floor and cannot see a staged-then-reverted index. One line saying so makes the rejection of "call the helper per name" fair.
* **N6 -- non-blocking. Two edges to name.** (a) Sequence: the twelfth change's code review N2 rewrites the guide sentence at `UPGRADE.md:102`, the one B2 changes; the plan should list that line and say which change owns it. (b) `bootstrap/_scaffold/install.py:1648` is another `git status --porcelain`, run on the Cairn source checkout; list it under "Not in scope" with the reason (the person already runs that checkout's code), so a later reader does not call it missed.

**Checked, no defect.** Frozen tests: `TestDirtyTreeGuard` and `TestFinalizeDirtyTreeGuard` call the entry points or the one-argument helper and read stderr text, so they stay green under the contract; the oracle block is built from `collide` in `_apply_upgrade` (`upgrade.py:2689-2697`), which the change does not touch. AST symbols match the proposal. The cost rows hold (P4).

**Coverage.** Not covered: git below 2.53.0 (emulated by omitting `GIT_NO_LAZY_FETCH`, not run on an old build); Windows; SHA-256; submodules, sparse checkouts, merge conflict, no-commit and glob names (the author's agreement run, not repeated); an index replaced by a link; a hung git; the Security preflight S1-S5; the plan's test nodes beyond reading their titles. No test suite run. The Security Review is still owed after the author's answer.

## Response -- Claude Sonnet 5.5 (author) -- 2026-10-26

Answers to the review at `2c1d82cd`. The complete contract is `## Revision 1` below; where the two differ, Revision 1 binds. I re-measured the cheap claims in a scratch repository (folder `dirtycheck-resp` under the scratchpad; git 2.53.0, Python 3.13.13, macOS); the numbers are in Revision 1, "Evidence". No engine code, test or suite was written or run.

* **B1** accept with modification -- the 2.45.0 floor stays in the shared launcher. Below it, one plain `git config` read of `extensions.partialclone` and `remote.*.promisor` (measured: it ran no program) gates the four commands, and "cannot tell" answers when either key is set. I reproduced the treeless case and the design runs nothing in it. The modification: a treeless clone on a git at or above the floor also answers "cannot tell" (exit 128), a case the first text did not consider.
* **B2** accept -- bare `--finalize` asks about the records the loop goes on to hash (living-state files and retired records that are not `untouched` are out, a renamed wrapper by its on-disk name) plus the lockfile. Question 1 now says what is lost and gained. A side effect I own: a bare finalize no longer waits for the commit of a hand-deleted retired file.
* **N1** accept -- a mode-only edit counts: the index mode against the owner-execute bit, as git does, skipped when `core.fileMode` is false. The upgrade's replacement write keeps the old mode but strips the execute bits (`bootstrap/_scaffold/security.py:71-72`, read, not run), so a chmod-only edit would not survive an overwrite.
* **N2** accept with modification -- disclosed as a gap, no new node: pinning a gap would pin a defect. Measured on this machine (`core.ignorecase` true): asked as `agents.md`, the check calls an edited `AGENTS.md` clean. Today's set intersection has the same gap.
* **N3** accept -- `names=None` is the lockfile's recorded files, or an empty set with no readable lockfile; a new node carries the "untracked recorded name is not returned" property.
* **N4** accept -- Question 2 now says it. One correction to the review's premise: `git status` calls a CRLF file clean when git wrote the checkout; for a file converted by hand it says modified with an empty `git diff` (measured).
* **N5** accept -- one line added to the Alternatives.
* **N6** accept -- (a) this change owns the `UPGRADE.md` "Deleting by hand" sentence as the twelfth change left it (`0f395af5`), and the twelfth change's bare-finalize node whose bare arm now exits 0; (b) `install.py` near 1648 is listed under Not in scope with its reason.

## Revision 1 -- Claude Sonnet 5.5 (author) -- 2026-10-26 -- the complete current contract

This replaces the Proposal, Rationale, Alternatives, Documentation, Evidence, Questions and Sequence above in full. The Context stands as written.

### Contract

1. **One answer, asked of the names.** `_dirty_tracked_paths(target, names=None)` returns the subset of `names` (project-relative, `/`-separated) with uncommitted changes, or `None` ("no guard") exactly as today when git cannot start or the folder is not in a work tree. `names=None` means the lockfile's recorded `dst` values, and an empty set when there is no readable lockfile. No production caller passes `None`; it keeps the frozen one-argument call working, and the plan greps for any other. `_writeset_dirty_collisions` passes the write-set.
2. **The names for bare `--finalize`** are the records the loop at `upgrade.py:2285-2305` goes on to hash, plus `dev/.cairn/cairn-lock.yml`, which finalize rewrites. That is every record with a string `dst`, the vendor wrapper by its on-disk name (one helper shared with the loop, so the two cannot disagree), minus living-state files (`_LIVING_STATE_DSTS`; never hashed) and minus retired records that are not `untouched` (`gone` is cleared; `matches-none` and `cannot-tell` stay unrecorded; `blocked` the loop refuses in its own words). A recorded file missing on disk stays in. Effect: a dirty living-state file, a hand-deleted retired file and an edited kept retired file no longer stop a bare finalize; an edited hashed record and a modified lockfile still do.
3. **Commands**, all through the twelfth change's launcher (moved to one module-level helper): `git -C <project>`, `-c core.fsmonitor=false -c core.hooksPath=<null device> -c core.useReplaceRefs=false`, every `GIT_*` variable removed, `GIT_NO_LAZY_FETCH=1`, `GIT_TERMINAL_PROMPT=0`, `GIT_OPTIONAL_LOCKS=0`, no input, the timeout, a byte cap, `--literal-pathspecs`. In order: `--version`; `rev-parse --is-inside-work-tree`; one `config -z --get-regexp '^(core\.filemode|extensions\.partialclone|remote\..*\.promisor)$'`; `rev-parse --verify -q HEAD` (exit 1: no commit yet); `ls-files -z -s -- <names>`; `diff-index --cached --raw -z --no-renames --no-ext-diff --no-textconv --relative HEAD -- <names>`. Names go in groups of at most 100.
4. **The floor stays.** A git older than 2.45.0, or one whose version cannot be read, may fetch a missing object from a remote the project names, and that fetch can run the project's `uploadpack` program. Below the floor, if the config read finds `extensions.partialclone` or any `remote.*.promisor` key (any scope, any value), the answer is "cannot tell" and none of the later commands runs. With neither key, an ordinary repository has no remote to fetch from lazily, and the commands run. At or above the floor `GIT_NO_LAZY_FETCH` stops the fetch; a treeless clone (the commit history without its folder listings) then makes `diff-index` exit 128, which is "cannot tell". A blobless clone (file contents absent) is read normally.
5. **The engine reads the files itself.** A name is **dirty** if any of these holds: it is staged against the last commit (added, changed, deleted, type-changed); it is in conflict; it is missing on disk or not a regular file; its index entry is not mode 100644 or 100755; its bytes, hashed the way git hashes a blob (SHA-1 or SHA-256 by the id's length), differ from the index; or its mode differs, meaning index 100755 against the owner-execute bit, checked on POSIX and only when `core.fileMode` is not false (git's own rule: group and other bits are ignored). A name git does not track is **not dirty**, as today.
6. **Git there but not answering** (over 10 s, an error after the work tree was confirmed, output past the cap, a treeless clone, a partial clone below the floor): the check says so in its own words and does not guess. `--apply` and bare `--finalize` refuse with the reason and `--force`; `--stage` completes with an advisory. Today this case is silent "no guard".
7. **Line endings.** A file whose bytes equal the index after turning every `\r\n` into `\n` counts as unchanged (Question 2).
8. **Over-reports, both in the refusing direction, disclosed in the guide:** a clean filter (git says clean, the raw bytes differ), a tracked symbolic link (the engine cannot write through one anyway), and a CRLF file if Question 2 is answered no. **Gap, same as today:** on a case-insensitive repository a name in another letter case reads as untracked, so an edit is not seen.
9. **Not in scope.** No new action, flag or list change; no template, install row or lockfile field; `scaffold.py --manifest` unchanged. `--force` still skips the check and runs no git. The `--apply` refusal text stays byte-identical (the differential oracle compares it); the bare-finalize text and `--finalize` help say "recorded". The twelfth change's behaviour changes in one place only: a bare finalize no longer waits for the commit of a hand-deleted retired file (item 2). `bootstrap/_scaffold/install.py` near 1648 (`git status --porcelain` on the Cairn source checkout) stays: it feeds a warning that never blocks, and that checkout's code is what the person is already running, so its git settings carry no authority the code lacks.

### Rationale and alternatives

The callers ask about names they hold, so a check bounded by those names is enough and costs the same however large the repository is. The programs `git status` runs (whole-tree scan, clean filters, the monitor) are what it does beyond that. Rejected: **doing nothing** leaves a program run and a silent overwrite, both live in 0.5. **A call per name to `_committed_copy_matches`** misses a file staged then reverted on disk (`git status` says `MM`), needs two more calls per differing name, and costs 8 ms a name (1.6 s for 200 names, against 0.14 s). **One batched `git cat-file --batch`** costs one process, but it also compares with the last commit only, so it misses the same staged-then-reverted file, and it needs the same floor. **Checking every tracked file** took 4.0 s for 50,000 files and reads every large data file. **`git status` with more overrides** cannot name `filter.<name>.clean`, whose key is arbitrary. **Dropping the floor** (the first text) runs a program in a treeless clone on an older git (measured below).

### Documentation / doctrine surface

Descriptive layer only (`docs/DOCUMENTATION_PLAN.md`). `bootstrap/SAFETY.md`: one sentence, the edit check runs no program the project names. `bootstrap/UPGRADE.md`: this change owns the "Deleting by hand is fine" sentence near line 102 as the twelfth change's code-review fix left it (a bare finalize "refuses while the deletion is uncommitted"; now false) and the finalize paragraph (the check covers the files finalize hashes and the lockfile; clean filter, link and line-ending notes; partial clones; `--force`). The twelfth change's node `test_a_hand_deleted_file_is_cleared_by_the_step_or_a_scoped_finalize_and_a_bare_finalize_waits_for_the_commit` (not keyed in the gate manifest: grep finds 0) has its bare arm rewritten here. The plan checks that no test or manifest pins the changed bytes. `CHANGELOG.md` at archive. No `doctrine/` or `AGENTS.md` text; the rate-limit gate does not apply.

### Evidence / verification plan

**Measured** (scratch repositories; a prototype of the commands outside the tree; git 2.53.0; Python 3.13.13). From the first round: agreement with `git status --porcelain` on ten edit states; fsmonitor and clean filter ran no program under the prototype; a blobless clone ran none; cost at 50,000 files: `git status` 92 ms, proposed 136 ms, per name 1.6 s, everything 4.0 s. Added this round:
* **The config read runs nothing.** On a repository whose config names `core.fsmonitor`, a clean filter, `core.pager`, an `uploadpack` program and the promisor keys, the `config` call exited 0, printed nothing to stderr and wrote no marker; `git status` there wrote one (control). It found `Remote.Other.Promisor` spelled in mixed case.
* **Treeless case reproduced.** `--filter=tree:0`, `remote.origin.uploadpack` naming a program: `rev-parse --verify HEAD` and `ls-files -s` ran nothing; `diff-index --cached HEAD` ran the program without `GIT_NO_LAZY_FETCH` and exited 128 with it. Blobless: none of the three ran it.
* **The design runs nothing.** A stand-in `git` reporting 2.44.0 and ignoring `GIT_NO_LAZY_FETCH` (a real old build was not available): treeless and blobless clones answered "cannot tell", no program. Gate removed (the mutant): the treeless clone ran the program. At 2.53.0 the treeless clone answered "cannot tell" (128), no program. An ordinary repository with a tree object deleted and `uploadpack` named: no program.
* **Mode.** `chmod u+x`: git and the prototype both dirty; mode check removed: the prototype misses it (the mutant is killed by this case). Group-execute only, and `core.fileMode=false` plus `chmod`: both clean.
* **Line endings.** A CRLF file git checked out: git clean; prototype clean with Question 2's rule, dirty without. A file converted by hand: git says modified with an empty `git diff` (it trusts the changed size); the prototype with the rule says clean.
* **Link and letter case.** An unchanged tracked link: prototype dirty, git clean. On this machine (`core.ignorecase` true), `agents.md` asked for an edited `AGENTS.md`: prototype clean, git dirty.

**Reasoned, not run:** the names set of item 2 (read from `upgrade.py:2285-2305` in the current tree; no engine code written); the stripped execute bit on replacement (`security.py:71-72`); any real git older than 2.53.0; Windows; SHA-256; submodules, sparse and linked work trees; a hung git; the time of the one extra `config` process (not timed). No test suite and no in-tree mutant were run.

### Tests required

Behaviour is driven through `scaffold.py upgrade --stage|--apply|--finalize`. New file (new files are allowed under the gate manifest).

Proposed paths:
* `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py`

Nodes: `test_git_config_programs_never_run_during_stage_apply_or_finalize` (monitor, clean filter, textconv, pager; mutant: call `git status`); `test_a_subfolder_project_sees_its_own_edits` (mutant: drop `--relative`); `test_the_check_agrees_with_git_status_on_each_edit_state` (git's own answer is the independent expectation); `test_pattern_characters_in_a_name_match_literally`; `test_a_staged_then_reverted_file_counts_as_edited`; `test_a_missing_or_untracked_name_is_handled_as_git_status_does`; `test_an_untracked_recorded_name_is_not_returned_and_no_lockfile_gives_an_empty_set` (carries the frozen test's property); `test_a_mode_only_edit_counts_unless_filemode_is_off` (mutant: skip the mode); `test_line_endings_only_difference_counts_as_unchanged`; `test_a_git_that_does_not_answer_stops_apply_and_finalize_and_only_advises_on_stage`; `test_force_runs_no_git`; `test_bare_finalize_asks_about_the_records_it_hashes_and_the_lockfile` (living-state edit proceeds; gone retired file proceeds; kept retired edit proceeds; edited hashed record, renamed wrapper and dirty lockfile refuse; mutants: all records; drop the lockfile); `test_a_partial_clone_runs_no_upload_program_at_or_above_the_floor` (blobless and treeless); `test_below_the_floor_a_partial_clone_answers_cannot_tell_and_runs_no_program` (stand-in older `git`; mutant: remove the config gate); `test_the_launcher_is_shared_with_the_committed_copy_check`.

**Frozen tests.** As in the first text (re-read at this tree): `TestDirtyTreeGuard`, `TestFinalizeDirtyTreeGuard` (edits `AGENTS.md`, a hashed record, so it still refuses) and `test_self_heal_composes_with_dirty_tree_guard` stay green unedited; oracle scenario `dirty_tree_refusal` stays `match`; no keyed test is edited, so no re-anchor is owed for tests.

### Examples / smoke checks

`python scripts/claim_check.py` and `python scripts/check_cairn.py` over the changed Markdown; `python scripts/quality_gate.py --sub neutrality`. Boundary B is `full` (engine, high-risk surface); `Certified by: pending`. AST symbols as in the first text; the baseline correction is Maintainer-run, once, at the cut.

#### Security preflight

* **S1 -- Who supplied it?** Index and last commit, file bytes and `.git/config` are all project data. The config read is used only to refuse (a promisor key means "cannot tell"); a wrong "clean" can only let the engine write where the operator's edit sits, and "dirty" only refuses.
* **S2 -- Can it fail?** Mutants per node above; the gate-removed and mode-skipped mutants were each shown to change the prototype's answer (Evidence). None run in-tree. The agreement node's expectation is `git status` itself.
* **S3 -- What fires it?** `upgrade --stage`, `--apply`, bare `--finalize`, over the write-set or item 2's names. `--force` and scoped `--finalize <path>` skip it. The guide sentence is written from this section by the plan.
* **S4 -- Which way does it break?** An unreadable git, a partial clone below the floor, a treeless clone: refuse (less authority). No git or not a work tree: no guard, as today. Clean filter, link: refuse. Rule 7, a case mismatch: not protected (more authority, small).
* **S5 -- Who still wins?** Assumed: the project controls `.git/config`, hooks, attributes and the index. Still wins: a project that rewrites its own index to look clean, and a `git` earlier on `PATH`. At or above the floor no program runs because lazy fetch is switched off and no command reads a working file; below it, that rests on one fact about git (lazy fetch needs a configured promisor remote), shown on 2.53.0 with a stand-in and not on a real older git.

#### Independent scientific check

N/A: no scientific assumption or result touched.

### Signals the change is wrong

A program from `.git/config` runs under any of the three commands, including on a treeless clone. The check calls a file clean that `git status` calls edited, apart from the disclosed gaps. A bare finalize refuses on a living-state or retired file, or runs on a modified lockfile. `--apply` is visibly slower on a large tracked tree. Windows checkouts refuse every file.

**Scope delta**: preserved. The baseline is the first text. Against today's behaviour the guard narrows in one place, bare `--finalize` (Question 1); the floor, dropped in the first text, is kept.

**Assurance path**: high-assurance (the scaffold engine and the twelfth change's trust-root launcher). **Plan review**: required(Internal + Internal Security Review). **Sequence**: lands after the twelfth change's code review clears, before the 0.5 cut; it needs a plan; one Maintainer-run baseline re-anchor at the cut covers both.

### Questions for the Maintainer

1. **Bare `--finalize` and files Cairn does not hash.** Today it refuses when any tracked file in the repository has an uncommitted edit, your own source code included. Finalize hashes only the recorded files and rewrites only the lockfile. New: it asks about the files it will hash, plus the lockfile. Lost: the refusal for an unrelated edit, which finalize never reads. Gained: no refusal for an edit to a living-state note (`NEXT_SESSION`, `PLANNING`) or for a retired file you deleted by hand, and no program run. **Default: ask about the files finalize hashes, plus the lockfile.**
2. **A change that only alters line endings.** `git status` calls a CRLF file clean when git wrote the checkout, but the engine compares raw bytes, so without a rule every such file would read as edited. Count a file as unchanged if it differs from the index only by CRLF versus LF? Cost: a line-ending-only edit is not protected. I measured this on macOS and did not run Windows. **Default: yes.**
3. **Git is there but does not answer, or cannot be read safely** (a treeless clone, or any partial clone with git older than 2.45.0). Stop (`--apply` and `--finalize` refuse, naming the reason and `--force`; `--stage` warns), or carry on unguarded as today? **Default: stop.**

### Withdrawn / superseded commitments

* Proposal 6, "no git-version floor for this check": withdrawn. A treeless clone on a git before 2.45.0 ran the project's program in `diff-index` (measured), so the floor stays, with a config-read gate below it that keeps the guard instead of giving it up.
* Proposal 1, bare `--finalize` "passes its recorded files": replaced by item 2, the records the loop hashes plus the lockfile; living-state and kept retired files are out.
* Proposal 3, "the rule ... bytes differ from the index": extended with the owner-execute bit (item 5), because a chmod-only edit would not survive the replacement write.
* Proposal 4, "git does not answer": widened to name the treeless and below-floor partial-clone cases.
* The Signals sentence "the check calls a file clean that `git status` calls edited, apart from the two stated over-reports": reworded; the over-reports and the case gap are now listed (item 8).
* Question 2's premise that line-ending handling protects Windows: replaced by the engine comparing raw bytes (N4).
* Not in scope, "the twelfth change's own behaviour is not widened": narrowed. A bare finalize no longer waits for the commit of a hand-deleted retired file, so this change rewrites the guide sentence near `UPGRADE.md:102` and the bare arm of the twelfth change's node for it.

## Security Review -- Security Reviewer (fresh session) -- 2026-10-26

```
Reviewed commit: 0320b94b
Target: Revision 1 (the complete current contract), against the security risks of the change it proposes
Prior findings: usual review B1, B2, N1-N6 (answered; not redone)
Assurance path: high-assurance
```

**Tier**: Security Review
**Obligation**: the Security Review that `**Review**: usual + Security Review` names: does this proposal, as revised, close the security risks of the change it proposes.
**Model**: Opus 5.5, fresh session
**Reviewed commit**: 0320b94b
**Findings**: raised (1 blocking, 5 non-blocking)

**Verdict: revising.** The design holds. With lazy fetch switched off, the six commands ran none of the more than 30 programs, hooks and file writers I planted, and the check either agreed with `git status` or refused. One hole: below the floor, the config gate misses a key that also turns the fetch on, and with it the project's program ran (B1). The fix is a wider key match and one node. This pass clears the obligation once the Response adopts B1 as written; no second round.

**Foundations**
1. *Does it close the risk?* Yes for programs at or above the floor and for the subfolder misread; not below the floor, where `remote.<name>.partialclonefilter` alone starts a fetch the gate does not see. -- ledger L1, L4.
2. *Simpler, safer alternative?* "Cannot tell" for every git below 2.45.0 is safer, but it makes `--force` routine on every host with an older git. The widened match keeps the guard there. -- Revision 1 item 4; L4.
3. *What would show it fails?* A planted program running under the six commands (L4 is one), or "clean" for a file `git status` calls edited outside the disclosed gaps (L3, three non-blocking cases). -- ledger.

**Falsification ledger** (scratch folder `secrev-dirty-7q3x` under the scratchpad, removed afterwards; git 2.53.0, Python 3.13, macOS; my own prototype of items 3 and 5 outside the tree, environment cleaned as at `bootstrap/_scaffold/upgrade.py:2470-2471`; no test or suite run)
* L1. Project in a subfolder; `.git/config` naming a monitor, required clean/smudge/process filters, textconv, diff command, external diff, order file, pager and per-command pagers, a hooks folder with eight hooks, `sshCommand`, `askPass`, `alternateRefsCommand`, `gitProxy`, editor, credential helper, an `ext::` remote, `uploadpack`, `receivepack`, `packObjectsHook`, `include.path`, `includeIf`, trace2 file targets, `gc.auto`, `maintenance.auto`. The six commands wrote no marker and no trace file; plain `git status` ran the monitor and the filter (control). Through a `.git` file plus `core.worktree`: the same.
* L2. A replace ref making HEAD equal the index hid a staged edit from a plain `diff-index`; with `core.useReplaceRefs=false` it was found. Index linked to a FIFO: 10 s timeout, "cannot tell"; to `/dev/zero`: exit 128, "cannot tell". A 600,000-entry (52 MB) index: 0.1 s.
* L3. "Clean" where git says edited: (a) a script given CRLF endings, no `core.autocrlf` (git `M`; rule 7 clean); (b) `sub/` swapped for a link to an outside folder with the same bytes (git `D`; a reader that follows the link: clean); (c) git's dubious-ownership refusal (`GIT_TEST_ASSUME_DIFFERENT_OWNER=1`) and `core.bare=true`: the first `rev-parse` exits 128 or says false, so "no guard", silently.
* L4. Partial clones of a local `origin.git`, `uploadpack` naming a marker that then runs the real upload-pack. Blobless and treeless clones with a checkout: answered, no program, lazy fetch on or off. Treeless after `fetch` and `reset --soft` (HEAD's folder listings absent): `GIT_NO_LAZY_FETCH=1` gave "cannot tell", no program; without it (as git before 2.45) the program ran, and the config read shows `remote.origin.promisor`, so the gate holds. **With `promisor` and `extensions.partialclone` removed and only `remote.origin.partialclonefilter` left, the config read returned only `core.filemode`, and `diff-index` fetched and ran the program.** With all three removed: exit 128, no program.
* L5. Read from the tree: `_dirty_tracked_paths` (`upgrade.py:2365`), `_writeset_dirty_collisions` and its callers (`2689`, `3240`), `_cmd_finalize_lockfile` (`2182-2362`), `_check_lockfile_paths` before it (`3079`), `--force` (`2674`, `2688`), `_committed_copy_matches` (`2434-2524`), `bootstrap/_scaffold/security.py:29, 110`, `bootstrap/tests/test_upgrade.py:1884, 2072, 2101`, `bootstrap/tests/_oracle.py:359`, `bootstrap/tests/test_upgrade_removes_retired_files.py:132`.

**Findings**
* **B1 -- blocking. The below-floor gate misses `remote.<name>.partialclonefilter` (item 4).** Git treats a remote with that key as a promisor and fetches through it (L4, on 2.53.0 with lazy fetch left on; not run on a real older build). So on git before 2.45.0, a project that sets the filter and no `promisor` key runs its `uploadpack` program under `--stage`. Fix: below the floor, "cannot tell" when any config key contains `promisor` or `partialclone` (regexp `core\.filemode|promisor|partialclone`, which also covers older git's `core.partialclonefilter`), not three exact names. One case per key in `test_below_the_floor_a_partial_clone_answers_cannot_tell_and_runs_no_program`; mutant: the item-3 regexp.
* **N1 -- non-blocking. A refusal at git's first question still reads as "no guard".** Dubious ownership (an upgrade run as another user, for example root in a container over a mounted checkout) and `core.bare=true` both end at the first `rev-parse` (L3c), so `--apply` overwrites edits silently, as today. Fix: if a `.git` file or folder exists at the project or above it (a filesystem look, no git) and git does not confirm a work tree, answer "cannot tell"; a node with `core.bare=true`.
* **N2 -- non-blocking. Rule 7 reads a CRLF-only edit as clean where git does not (L3a).** A bare finalize then records those bytes, and in a shell script a `\r` at each line end changes what runs. Fix: apply rule 7 only when the same config read finds `core.autocrlf` true or `core.eol` crlf (a `.gitattributes` `eol=crlf` file then over-reports, the refusing direction). Say so in Question 2, and list the gap in item 8.
* **N3 -- non-blocking. Name the reader in item 5.** A plain `open` follows a linked parent folder (L3b) and blocks with no timeout on a FIFO swapped in after the type check. `--apply`'s write guard refuses the linked parent (`security.py:110`), but finalize's loop reads through it (`upgrade.py:2293, 2315`; pre-existing). Fix: read with `_read_regular_bytes` (`O_NOFOLLOW`, `O_NONBLOCK`, `fstat`), and count a link between the project and the name as dirty, as `_assert_safe_write` checks.
* **N4 -- non-blocking. Say how the config answer is read.** `git config --get-regexp` exits 1 when no key matches; read as an error, a repository with no `core.filemode` line refuses every time. Say: exit 1 is "no keys", other non-zero is "cannot tell"; `core.filemode` follows git's boolean rules, last value wins.
* **N5 -- non-blocking. Moving the floor cache silences a test.** `test_upgrade_removes_retired_files.py:132` forgets the floor through `U._committed_copy_matches.git_floor_met` with `raising=False`. If the cache moves to the shared launcher, that line sets an attribute nothing reads, and the stand-in older-`git` nodes depend on test order. Fix: one cache, that line updated (the file is not keyed), and each below-floor node resets it.

**Checked, no defect.** Names (3): the set comes from the engine's own lists (`_LIVING_STATE_DSTS`, the retired list), not a record's flags, so a lockfile edit shrinks it only by deleting a record, which also stops finalize hashing that file, and the lockfile is itself in the set; an outside name is refused before finalize (`upgrade.py:3079`); a huge lockfile adds two git processes per 100 names to finalize's own hashing. DoS (4): "cannot tell" blocks only the project's own upgrade, `--force` on `--apply` skips only the dirty guard (`upgrade.py:2674, 2688`), and a treeless clone with a checkout answers normally (L4). Frozen (5): the oracle block comes from `collide` on a plain edited `AGENTS.md`, unchanged under the contract; `TestDirtyTreeGuard`, `TestFinalizeDirtyTreeGuard` and the one-argument call stay valid. Sequence (6): the twelfth plan is `revising-code` waiting on the Maintainer's two allowances (`dev/plans/upgrade-removes-retired-files.md:5-7`); this proposal waits for it and owns `bootstrap/UPGRADE.md:99-104`.

**Coverage.** Not covered: a real git older than 2.53.0 (below-floor behaviour emulated by leaving lazy fetch on); Windows (`nul` hooks path, CRLF, bare-`git` lookup); SHA-256; submodules, sparse index and linked work trees beyond the `.git` file case; case, mode-only, intent-to-add, assume-unchanged and skip-worktree edits (the usual review's P2, not repeated); the AST symbol list (not run); the plan's nodes beyond their titles. No test suite or in-tree mutant run.

## Response -- Claude Sonnet 5.5 (author, Security Review) -- 2026-10-26

Answers to the Security Review at `0e4bfc42`. The complete contract is `## Revision 2` below; where the two differ, Revision 2 binds. I re-measured the cheap claims in a scratch repository (folder `dc-resp2-k4m9` under the scratchpad; git 2.53.0, Python 3.13.13, macOS). I wrote no engine code, test or suite. **Measured:** the key matches and the program runs (B1), the `git` answers at a refused repository (N1), the CRLF cases and the config output (N2, N4), the file readers (N3), the cost of the two extra processes (7 ms and 6 ms, mean of 30). **Reasoned, not run:** any real git older than 2.53.0, Windows, the cache move (N5, read from the tree).

* **B1** accept as written -- below the floor, "cannot tell" when any config key contains `promisor` or `partialclone`. Reproduced: a treeless clone (history without its folder listings) with only `remote.origin.partialclonefilter` set and lazy fetch left on ran the program once; the three-name read returned only `core.filemode`; the widened read returns the key. `extensions.partialclone` alone and `remote.origin.promisor` alone each ran it too; with no key, exit 128 and no program; lazy fetch off, exit 128 and no program. One test case per key, four, with `core.partialclonefilter` (older git's name: matched, its effect on a real older git not measured).
* **N1** accept -- if a `.git` file or folder exists at or above the project and git does not confirm a work tree, answer "cannot tell". Measured: dubious ownership exits 128 with no output; `core.bare=true` prints `false`, exit 0; a bad config line exits 128; no `.git` anywhere exits 128 ("no guard", as today). A stray empty `.git` folder also exits 128, so it would read "cannot tell": I kept the simple rule and disclose it.
* **N2** accept -- the CRLF rule applies only where `core.autocrlf` is true or `core.eol` is `crlf`, read in the same config call (measured: both keys appear in it). Measured: no setting and a hand-converted file, git says modified, the rule is off, dirty; `autocrlf=true` and `eol=crlf` with `* text`, git clean, rule on, clean. With only `.gitattributes` `eol=crlf` git is clean and the engine says dirty (over-report, refusing). Question 2 says so.
* **N3** accept -- bytes are read with `_read_regular_bytes` and a link between the project and the name counts as dirty, through `_assert_safe_write`. Measured on the tree's helpers: a link in the path was read through by the first alone and refused by the second; a FIFO and a folder at the name refused at once, no block.
* **N4** accept -- config exit 1 is "no keys", other non-zero is "cannot tell"; booleans follow git's rules, last value wins. Measured: exit 1 with no key; a valueless key prints `key` then NUL; last value wins in the print order; `filemode = banana` reads with exit 0 but `git status` dies, so it is "cannot tell".
* **N5** accept -- one cache, in the shared launcher; `test_upgrade_removes_retired_files.py:130` is re-pointed (the file is not keyed: 0 hits in the gate manifest). Revision 2 lists the nodes that reset it, and one new autouse reset covers the new file.

**Status moves to `awaiting-decision`.** The Security Review obligation (the `usual + Security Review` clause in the header) is cleared by the pass at `0e4bfc42` once these answers are in: it asked for one round and said no second round, and B1 is adopted as written (the same config read also carries the two N2 keys). Calls the Maintainer may overrule: a stray empty `.git` folder reads "cannot tell" (N1); a `.gitattributes`-only CRLF checkout refuses (N2); `core.eol=native` counts as CRLF only on Windows, unmeasured (N2); any key containing the two words, even in a remote's name, refuses below the floor only (B1). The three Questions stay three; 2 and 3 are reworded.

## Revision 2 -- Claude Sonnet 5.5 (author, Security Review) -- 2026-10-26 -- the complete current contract

This replaces Revision 1 in full, and with it the Proposal, Rationale, Alternatives, Documentation, Evidence, Questions and Sequence above. The Context stands as written.

### Contract

1. **One answer, asked of the names.** `_dirty_tracked_paths(target, names=None)` returns the subset of `names` (project-relative, `/`-separated) with uncommitted changes, or `None` ("no guard", as today) when git cannot start or no `.git` exists at or above the project. `names=None` means the lockfile's recorded `dst` values, empty with no readable lockfile; no production caller passes it. `_writeset_dirty_collisions` passes the write-set. Bare `--finalize` passes the records its loop at `upgrade.py:2285-2305` goes on to hash (the vendor wrapper by its on-disk name, one helper shared with the loop; minus living-state files; minus retired records that are not `untouched`; a recorded file missing on disk stays in) plus `dev/.cairn/cairn-lock.yml`.
2. **Steps**, in this order, all through the twelfth change's launcher (moved to one module-level helper): `git -C <project>`, `-c core.fsmonitor=false -c core.hooksPath=<null device> -c core.useReplaceRefs=false`, every `GIT_*` variable removed, `GIT_NO_LAZY_FETCH=1`, `GIT_TERMINAL_PROMPT=0`, `GIT_OPTIONAL_LOCKS=0`, no input, the timeout, a byte cap, `--literal-pathspecs`. (a) A filesystem look, no git: does a `.git` file or folder exist in the project folder or any folder above it? (b) `--version`. (c) `rev-parse --is-inside-work-tree`. (d) one `config -z --get-regexp 'core\.filemode|core\.autocrlf|core\.eol|promisor|partialclone'`. (e) `rev-parse --verify -q HEAD` (exit 1: no commit yet). (f) `ls-files -z -s -- <names>`. (g) `diff-index --cached --raw -z --no-renames --no-ext-diff --no-textconv --relative HEAD -- <names>`. Names go in groups of at most 100.
3. **Does git confirm a work tree?** Exit 0 and `true`: go on. Anything else (dubious ownership, a bad config line, `core.bare=true`): "cannot tell" if (a) found a `.git`, "no guard" if not.
4. **Reading the config answer.** Exit 1 is "no keys". Other non-zero, a timeout or a capped output is "cannot tell". Output is `key`, newline, `value`, NUL; a key with no value is `key`, NUL, and means true. The last value of a key wins. Booleans follow git: no value, `true`, `yes`, `on` or a non-zero integer is true; empty, `false`, `no`, `off` or `0` is false; any other value is "cannot tell" (git itself dies on it). `core.filemode` defaults to true. `core.autocrlf=input` is not CRLF. `core.eol` is read as `crlf`, `lf` or `native` (`native` counts as CRLF on Windows only); any other value is "cannot tell".
5. **The floor stays.** Below 2.45.0, or with an unreadable version, git may fetch a missing object from a remote the project names, and that fetch can run the project's `uploadpack` program. Then, if any config key contains `promisor` or `partialclone` (any scope, any value; this covers `extensions.partialclone`, `remote.<name>.promisor`, `remote.<name>.partialclonefilter` and older git's `core.partialclonefilter`), the answer is "cannot tell" and steps (e) to (g) do not run. With none, the commands run. At or above the floor, `GIT_NO_LAZY_FETCH` stops the fetch and a treeless clone makes step (g) exit 128, which is "cannot tell". The floor cache is one module-level value in the shared launcher, read by both this check and `_committed_copy_matches`.
6. **A name is dirty** if it is staged against the last commit (added, changed, deleted, type-changed); in conflict; missing on disk; not a regular file; a link, or under a linked folder, anywhere between the project and the name (`_assert_safe_write` refuses it); its index entry is not mode 100644 or 100755; its bytes differ from the index; or its owner-execute bit differs from the index mode (POSIX only, and not when `core.filemode` is false). Bytes are read with `_read_regular_bytes` (no link followed, no blocking on a FIFO) and hashed the way git hashes a blob (SHA-1 or SHA-256 by the index id's length). A name git does not track is not dirty, as today.
7. **Line endings.** Only when `core.autocrlf` is true or `core.eol` asks for CRLF: a file whose bytes equal the index after turning every `\r\n` into `\n` counts as unchanged (Question 2). Otherwise a CRLF-only difference is an edit, as git says.
8. **Cannot tell** (over 10 s, git refusing after a `.git` was found, an error after the work tree was confirmed, output past the cap, a treeless clone, a partial clone below the floor, an unreadable config answer): the check says so in its own words and does not guess. `--apply` and bare `--finalize` refuse with the reason and `--force`; `--stage` completes with an advisory. Today this case is a silent "no guard".
9. **Over-reports (refusing direction), disclosed in the guide:** a clean filter; a tracked symbolic link; a CRLF checkout set only by `.gitattributes`; a stray empty `.git` folder; a CRLF file when Question 2 is answered no. **Gap, same as today:** a name in another letter case on a case-insensitive repository reads as untracked.
10. **Not in scope.** No new action, flag, list change, template, install row or lockfile field; `scaffold.py --manifest` unchanged. `--force` runs no git. The `--apply` refusal text stays byte-identical (the differential oracle compares it); the bare-finalize text and `--finalize` help say "recorded". A bare finalize no longer waits for the commit of a hand-deleted retired file. `bootstrap/_scaffold/install.py` near 1648 (`git status --porcelain` on the Cairn source checkout) stays: its warning never blocks, and that checkout's code is what the person already runs.

### Rationale and alternatives

The callers ask about names they hold, so a check bounded by those names is enough and costs the same in any repository. Rejected: **doing nothing** (a program run and a silent overwrite, both live in 0.5); **a call per name to `_committed_copy_matches`** (misses a file staged then reverted, needs more calls, 8 ms a name against 0.14 s for 200 names); **one batched `git cat-file --batch`** (same blind spot, same floor); **checking every tracked file** (4.0 s for 50,000 files); **`git status` with more overrides** (`filter.<name>.clean` has an arbitrary key); **"cannot tell" for every git below 2.45.0** (safer, but makes `--force` routine on older hosts; the key match keeps the guard there).

### Documentation / doctrine surface

Descriptive layer only (`docs/DOCUMENTATION_PLAN.md`). `bootstrap/SAFETY.md`: one sentence. `bootstrap/UPGRADE.md`: this change owns "Deleting by hand is fine" near line 102 and the finalize paragraph (files covered, the disclosed over-reports, partial clones, refused repositories, `--force`). The twelfth change's node `test_a_hand_deleted_file_is_cleared_by_the_step_or_a_scoped_finalize_and_a_bare_finalize_waits_for_the_commit` has its bare arm rewritten here. The plan checks that no test or manifest pins the changed bytes. `CHANGELOG.md` at archive. No `doctrine/` or `AGENTS.md` text; the rate-limit gate does not apply.

### Evidence / verification plan

**Measured, earlier rounds** (git 2.53.0): agreement with `git status --porcelain` on ten edit states; no program from fsmonitor, a clean filter or the config read; blobless clones run none; a stand-in `git` reporting 2.44.0 answers "cannot tell" on treeless and blobless clones; mode and CRLF cases; cost at 50,000 files (`git status` 92 ms, proposed 136 ms, per name 1.6 s, everything 4.0 s). **Measured this round** (scratch folder `dc-resp2-k4m9`): the rows of the Response, B1 to N4. **Reasoned, not run:** git older than 2.53.0 (the stand-in is not a real old build), Windows (`native`, `.gitattributes`), SHA-256, submodules, sparse and linked work trees, a hung git. No test suite and no in-tree mutant were run.

### Tests required

New file, driven through `scaffold.py upgrade --stage|--apply|--finalize`.

Proposed paths:
* `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py`

Nodes: all those of Revision 1 (programs never run; subfolder; agreement with `git status`; pattern characters; staged then reverted; missing or untracked; untracked recorded name and empty set; mode-only; git does not answer; `--force` runs no git; bare-finalize names; partial clones at or above the floor; launcher shared), with these changes and additions. `test_below_the_floor_a_partial_clone_answers_cannot_tell_and_runs_no_program` takes one case per key (`extensions.partialclone`, `remote.origin.promisor`, `remote.origin.partialclonefilter` on a treeless clone with lazy fetch left on, `core.partialclonefilter`); mutant: the exact-name match of Revision 1. `test_a_repository_git_will_not_confirm_is_cannot_tell_and_no_repository_is_no_guard` (`core.bare=true`; a stand-in `git` exiting 128; no `.git` anywhere; mutant: treat the refusal as no guard). `test_line_endings_rule_applies_only_when_settings_ask_for_crlf` (`autocrlf` true, `eol=crlf`, neither, `input`; mutant: always apply). `test_a_link_in_the_path_counts_as_dirty_and_a_fifo_does_not_block` (mutant: a plain `open`). `test_the_config_answer_is_read_as_git_reads_it` (no key, valueless, last wins, a bad value, a failing config; mutant: exit 1 as error). **Floor cache:** the old reset in `test_upgrade_removes_retired_files.py:130` sets an attribute of `_committed_copy_matches` with `raising=False`, so after the move it would set something nothing reads. It is re-pointed at the one cache. It runs through `_stand_in_git` (six nodes and the four reached by `_version_answer`) and directly in `test_committed_copy_matches_ignores_a_replace_ref` and `test_a_git_that_fails_or_is_missing_keeps_the_file`. The new file has one autouse reset, and each stand-in node asserts that `--version` was the first call logged (mutant: leave the old reset line).

**Frozen tests.** `TestDirtyTreeGuard`, `TestFinalizeDirtyTreeGuard` and `test_self_heal_composes_with_dirty_tree_guard` stay green unedited; oracle scenario `dirty_tree_refusal` stays `match`; no keyed test is edited. Boundary B is `full` (engine, high-risk surface); `Certified by: pending`. Smoke: `python scripts/claim_check.py`, `python scripts/check_cairn.py`, `python scripts/quality_gate.py --sub neutrality`. The AST baseline correction is Maintainer-run, once, at the cut.

#### Security preflight

* **S1 -- Who supplied it?** Index, last commit, file bytes, `.git/config` and the folder layout above the project are project data. The config answer only refuses or switches a byte-folding rule; a wrong "clean" lets the engine write over the operator's edit, and "dirty" only refuses.
* **S2 -- Can it fail?** One mutant per node above; the gate-removed, mode-skipped and exact-name mutants each changed the prototype's answer. None run in-tree. The agreement node's expectation is `git status` itself.
* **S3 -- What fires it?** `upgrade --stage`, `--apply`, bare `--finalize`, over the write-set or item 1's names; `--force` and scoped `--finalize <path>` skip it. The guide sentence is written from this section by the plan.
* **S4 -- Which way does it break?** Unreadable git, refused repository, partial clone below the floor, treeless clone, unreadable config: refuse. No git, no `.git`: no guard, as today. A case mismatch, and a CRLF-only edit under a setting asking for CRLF: not protected (more authority, small).
* **S5 -- Who still wins?** Assumed: the project controls `.git/config`, hooks, attributes and the index. Still wins: a project that rewrites its own index to look clean, and a `git` earlier on `PATH`. Below the floor, safety rests on one fact about git (lazy fetch needs a promisor remote, named by a key containing the two words), shown on 2.53.0 and a stand-in, not on a real older git.

#### Independent scientific check

N/A: no scientific assumption or result touched.

### Signals the change is wrong

A program from `.git/config` runs under any of the three commands, including on a treeless clone with any single partial-clone key below the floor. A refused repository (another owner, `core.bare=true`) is treated as unguarded. The check calls a file clean that `git status` calls edited, apart from the disclosed gaps. A bare finalize refuses on a living-state or retired file, or runs on a modified lockfile. `--apply` is visibly slower on a large tree. Windows checkouts refuse every file.

**Scope delta**: preserved. The baseline is the first text. Against today's behaviour the guard narrows in one place, bare `--finalize` (Question 1). **Assurance path**: high-assurance (the scaffold engine and the twelfth change's trust-root launcher). **Plan review**: required(Internal + Internal Security Review). **Sequence**: lands after the twelfth change's code review clears, before the 0.5 cut; it needs a plan; one Maintainer-run baseline re-anchor at the cut covers both.

### Questions for the Maintainer

1. **Bare `--finalize` and files Cairn does not hash.** Today it refuses when any tracked file in the repository has an uncommitted edit, your own source code included. Finalize hashes only the recorded files and rewrites only the lockfile. New: it asks about the files it will hash, plus the lockfile. Lost: the refusal for an unrelated edit. Gained: no refusal for an edit to a living-state note (`NEXT_SESSION`, `PLANNING`) or a retired file you deleted by hand, and no program run. **Default: ask about the files finalize hashes, plus the lockfile.**
2. **A change that only alters line endings.** `git status` calls a CRLF file clean when git wrote the checkout, but the engine compares raw bytes. Count a file as unchanged if it differs from the index only by CRLF versus LF, but only where your git settings ask for CRLF (`core.autocrlf=true` or `core.eol=crlf`)? Cost: there, a line-ending-only edit is not protected (in a shell script it can change what runs). Where you set CRLF only in `.gitattributes`, every such file reads as edited. I measured this on macOS and did not run Windows. **Default: yes.**
3. **Git is there but does not answer, or cannot be read safely** (a treeless clone, a partial clone with git older than 2.45.0, or a repository git refuses, such as one owned by another user). Stop (`--apply` and `--finalize` refuse, naming the reason and `--force`; `--stage` warns), or carry on unguarded as today? **Default: stop.**

### Withdrawn / superseded commitments

* Revision 1 item 4, the below-floor gate on three exact key names: replaced by any key containing `promisor` or `partialclone`, because `remote.<name>.partialclonefilter` alone also starts the fetch (measured).
* Revision 1 item 1, "no guard" whenever git does not confirm a work tree: narrowed to "no `.git` found"; a refused repository is "cannot tell".
* Revision 1 item 7, the CRLF rule always on: now on only where `core.autocrlf` or `core.eol` asks for CRLF.
* Revision 1 item 5, "not a regular file" and a plain file read: now `_read_regular_bytes` plus a linked-path check.
* Revision 1 item 3, the config read as pass or fail: exit 1 is "no keys"; booleans follow git's rules.
* The floor cache on `_committed_copy_matches` and its test reset: replaced by one cache in the shared launcher.
* Question 2 reworded (CRLF only where settings ask) and Question 3 widened (a refused repository). Item 8's gap list gained a `.gitattributes`-only checkout and a stray `.git` folder.

## Decision -- Anthony Kendall (Maintainer) -- 2026-10-27

**ACCEPTED, as revised.** The Maintainer's authorization, quoted **verbatim and visually isolated**. He was asked three questions (each with its default) and then, separately, whether to accept Revision 2 as it stands and scribe the Decision now. He answered:

> "Yes, recorded files + lockfile (Recommended)"  (Question 1: bare `--finalize` asks git only about the files it hashes plus the lockfile)

> "Yes (Recommended)"  (Question 2: where git settings ask for CRLF, a line-ending-only difference counts as unchanged)

> "Stop (Recommended)"  (Question 3: when git does not answer or cannot be read safely, `--apply` and `--finalize` stop, naming the reason and `--force`; `--stage` only warns)

> "Accept and commit (Recommended)"  (disposition)

*Scribe's note, separate from the quoted words.* "As revised" means Revision 2, the complete current contract, which supersedes Revision 1 and answers the usual review and the Security Review (obligation cleared by the pass at 0e4bfc42). The plan review stays `required(Internal + Internal Security Review)`. The implementer does not edit `scaffold_ast_known_new.json`, the AST baseline, the gate manifest or the gate anchor; the Maintainer's one re-anchor at the cut covers this change and must name the oracle-sensitive files (`bootstrap/_scaffold/`, including `config.py`). A plan is opened in a separate commit, which archives this proposal.
