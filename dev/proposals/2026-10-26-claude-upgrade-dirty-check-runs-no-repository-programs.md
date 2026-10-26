# Make the upgrade edit check run no program from the project's git settings

**Author**: Claude Sonnet 5.5
**Status**: awaiting-review
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
