# Plan: Ship a Git attributes file so line endings match on every machine

**Source proposal**: dev/proposals/archive/2026-11-16-claude-git-attributes-file.md
**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`, Medium), plan author
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: New Cairn installs add a root `.gitattributes` so text files keep the same line endings on every machine, which stops a Windows checkout from silently differing from the repository, and an existing `.gitattributes` is never replaced.

## Build summary

After this plan a fresh install writes a root `.gitattributes` (LF for text, CRLF for `.bat` and `.cmd`, binary patterns, commented project choices) and records it in the lockfile. A project with its own keeps it byte for byte through install, `--force` and upgrade: the install prints Cairn's lines to merge by hand, and `upgrade` shows a name collision until the owner adopts the file once. Where the repository already stores CRLF text, the install counts those files and points to renormalize steps. The guides say so, and one Windows VM run shows the checkout is clean.

## Source proposal

The accepted proposal (Decision 2026-11-16, standard tier with plan and Security Review) adopts option A with two defaults: a verbatim install with no copy under `dev/.cairn/base/`, and the `git_read`/`ident` item kept separate. Its Security Review's blocking finding is carried here: the lockfile exemption is keyed to the one path `.gitattributes`, never generalized. This plan carries out install steps 1 to 4, the brownfield count, the guide text and the Windows check.

## Scope

**Result.** A Windows checkout of a Cairn project stops differing silently from the repository, and nothing Cairn installs overwrites or hides an adopter's own attributes file. Windows is an equal partner (Maintainer, 2026-11-10).

**Branch.** This plan is a document on `master`. Every chunk lands on `0.8-dev` (`dev/PLANNING.md`, "Branches for v0.8"), created from `master` when group 1 is done; it does not exist yet, and no chunk starts before it does.

**One site differs from the proposal's text.** It says add the mapping to `_CORE_MAPPINGS`. Read in the tree: every row there installs substituted and cached under `dev/.cairn/base/` (`install_manifest` passes `False` at `bootstrap/_scaffold/install.py:2033`; so does `bootstrap/_scaffold/upgrade.py:1034`). The Decision's verbatim, no-copy install can only use `_SKILLS_MAPPINGS`, whose rows carry the flag (`bootstrap/_scaffold/config.py:914`) and which the install, manifest and upgrade code already read. The other route needs a third tuple element in four engine sites and the frozen `test_manifest.py`. The reviewers may overrule this.

**Edits** (line numbers checked at `c3f5c1d4`; each chunk re-reads):

| File | Site | Change | Chunk |
|---|---|---|---|
| `templates/core/gitattributes.txt` | new, a non-dot name so it does not apply in Cairn's own checkout | the file in C1 | C1 |
| `bootstrap/_scaffold/config.py` | `_SKILLS_MAPPINGS` (914) | one row | C1 |
| `bootstrap/_scaffold/lockfile.py` | `_LIVING_STATE_DSTS` (201); new `_KEPT_EXISTING_DSTS` beside it | one entry with the residual comment; a one-path set | C1 |
| `bootstrap/_scaffold/install.py` | import (64); `_install_one` (test at 367); `write_install_lockfile` (test at 2322) | keep the file; exempt it from the lockfile check | C1 |
| same | `print_report` (1876); new `_index_crlf_count` | count and print | C3 |
| `bootstrap/BOOTSTRAP.md`, `bootstrap/UPGRADE.md`, `docs/quickstart.md`, `bootstrap/tests/test_quickstart_sequence.py` | named in C4 | guide text; two test lines | C4 |
| `CHANGELOG.md`, `dev/PLANNING.md` | `## Unreleased`; section 1 | one entry; one row | C6 |

**Unchanged on purpose** (read, not run; C2 checks): `bootstrap/_scaffold/upgrade.py` (its collision route and `_record_fork_entry` at 2006 already record a verbatim fork with no cached copy and the living-state flag), `cli.py`, and the frozen `bootstrap/verify_integrity.py` (it reads `_LIVING_STATE_DSTS` by import). A needed change to `upgrade.py` is a Plan change.

**Frozen and protected.** No file above is in `frozen_files` of `bootstrap/tests/fixtures/gate_manifest.json` (exact-path check, measured). `bootstrap/_scaffold/` is a high-risk surface, hence the Security Review. The Maintainer's one 0.8-dev re-anchor (`bootstrap/AST_BASELINE_RUNBOOK.md`; Maintainer-run, never an agent) owes for this plan: AST baseline keys CHANGED `Assign:_SKILLS_MAPPINGS`, `FunctionDef:_install_one`, `FunctionDef:write_install_lockfile`, `Assign:_LIVING_STATE_DSTS`, `FunctionDef:print_report` (its second change; group 1 made the first); NEW `Assign:_KEPT_EXISTING_DSTS`, `FunctionDef:_index_crlf_count` (`scaffold_ast_baseline.json`, `scaffold_ast_known_new.json`). Report-only notes may appear for the `_SKILLS_MAPPINGS` mapping digest, the new test file (`FROZEN-NEW`) and `test_quickstart_sequence.py`. No agent edits those fixtures, and this plan does not wait for the re-anchor (`dev/rules/protected-surfaces.md`).

**Non-work.** `git_read` and `ident` handling (Decision: separate). A count at upgrade time (the proposal names install only; `UPGRADE.md` carries the steps). A `.gitattributes` in Cairn's own checkout: none is added, so when Cairn next upgrades itself `upgrade --plan` should list one as new (expected from `bootstrap/_scaffold/upgrade.py:1034`, not run), for the Maintainer to take or adopt then. Folding line endings before hashing (rejected in the defects Decision).

**Reuse.** The verbatim path (`install_skills`, `_install_one(verbatim=True)`), `_LIVING_STATE_DSTS`, the `new-core-blocked` route with `_cmd_adopt_collisions`, `git_read`'s `run_git` as `git_provenance_warning` uses it, and the helpers of `bootstrap/tests/test_upgrade_side_door_parity.py` (each test file defines its own `_install`). Searched `skipped-exists` over `bootstrap/_scaffold/*.py` (five sites, none keeps a file under `--force`), `gitattributes` over `bootstrap`, `templates`, `scripts`, `tools` (fixtures and prose only; nothing installs one) and `ls-files` (no `--eol` use).

### Documentation / doctrine surface

Descriptive layer only: `bootstrap/BOOTSTRAP.md`, `bootstrap/UPGRADE.md`, `docs/quickstart.md`. The install table gains one row; `AGENTS.md` and `RULES.md` do not change.

Delivered paths:
- `templates/core/gitattributes.txt`
- `bootstrap/tests/test_gitattributes_install.py`
- `dev/measurement/windows-git-attributes-run.md`

## Sequence

Estimate 10 to 12 low-tier agent-hours, about a day and a half (a planning estimate). Uncertain: whether a file on the selector's list, none of which this author ran, goes red for a reason not foreseen here (stop and report); shell quoting on the VM; VM availability.

**Every chunk.** A Low-tier implementer, high-risk chunks included (`AGENTS.md`); name the model at spawn. Work on `0.8-dev` (`git branch --show-current`). Claim the exact paths first. At the start read `git status` and `git log -5` for each file the chunk edits: another session's uncommitted edit stops you and is never committed. Prose by exact replacement. Tests first: run them, see the stated failure, then change. Run tests with `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest`, never the whole suite; the list for changed paths is `python tools/test_tiers.py for <paths>`. One commit per chunk, explicit paths. If anything differs from the chunk, stop and report; decide nothing. No push.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Template, row, kept file, lockfile exemption, living-state entry; tests T1, T2, T4 | plan reviews; `git branch --list 0.8-dev` prints it | 4 files, new test file |
| C2 | Upgrade, integrity and pattern tests T3, T5, T6 | C1 | test file |
| C3 | Install-time CRLF count and print; test T7; the selector's list once | C2 | `install.py`, test file |
| C4 | Guides and quickstart | C3; no other session's uncommitted edit to the four files | 4 files |
| C5 | Windows run on `cairn-windows` | C4 | record |
| C6 | CHANGELOG, `dev/PLANNING.md`, plan entry | C5 | 3 files |

**Order against other work.** Group 1 (`dev/plans/archive/2026-11-16-adopter-defects-0-7-0.md`) lands first: it gates `0.8-dev` and edits `lockfile.py` (the helper pin line), `upgrade.py` and `UPGRADE.md`, so C1 and C4 start from what is committed. No other open plan edits `install.py` or `config.py`; the meter plan edits `tools/meter.py` and its lock record only. C4 waits for the template-trim plan if it has an open edit to `bootstrap/BOOTSTRAP.md`. This plan reaches `ready-to-archive` before the layout plan's first chunk (the proposal's dependency), and the layout plan must name `.gitattributes` a root exception and move this plan's paths.

**Red until the re-anchor** (expected, not pass criteria). `bootstrap/tests/test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package` is already red (six CHANGED keys at `3bdfffd8`, from group 1); this plan adds the keys above. Save `python scripts/repin.py status` from the line `Engine pin` on before C1, after C1 and after C3, and report the differences. Any difference outside those seven keys and the report-only notes: stop and report. Before C1 also run the list for `config.py`, `install.py` and `lockfile.py` once (72 files at the plan's date) and save its failing node IDs as the control.

## Acceptance criteria

Length: the body outside Acceptance runs about 1,600 words against 1,000, and the chunks run past 150 words (C1 690, C2 240, C3 350, C4 610, C5 250, C6 160), because an engine change with a Security-reviewed exemption and a Windows run leave a Low-tier executor no design. The three shipped blocks (the template and two guide sections, 578 words) sit inside C1 and C4 and are extra.

**C1.** *Step 0.* Save the `repin.py status` block and run the control list, as Sequence says. *Step 1, tests first.* Create `bootstrap/tests/test_gitattributes_install.py`. Each test installs into `tmp_path` through `scaffold.main` as `test_upgrade_side_door_parity.py` does (profile `project_name: Demo`, `test_command: pytest`, `preset: solo-greenfield`, `--allow-dev`) into a plain folder, and runs `git init` only where it calls `git`; every `git` call sets `GIT_CONFIG_GLOBAL` to `os.devnull` and `GIT_CONFIG_NOSYSTEM=1`. **T1** `test_fresh_install_writes_the_file_and_records_it`: `.gitattributes` equals `templates/core/gitattributes.txt` byte for byte; the lockfile holds one record for it with `verbatim` true, `living_state` true, no `base_cache`, and `hash` the sha256 of that file. First run: fails, no such file. **T2** `test_an_existing_different_file_is_kept_byte_for_byte`, two cases: (`[]`, the template with each `\n` made `\r\n`) and (`["--force"]`, `b"# mine\n*.dat -text\n"`), written before the install. After it: exit 0; bytes unchanged; the lockfile exists with records for `AGENTS.md` and `tools/board.py` and none for `.gitattributes`; captured stderr holds every non-blank, non-comment template line. First run: the stderr line fails; the rest already pass, because nothing manages the file yet. **T4** `test_no_other_differing_file_gets_the_exemption`, planted path `tools/board.py` (a verbatim file) and `NOTICE.md` (a substituted one): the planted file (`b"planted\n"`) and a different `.gitattributes` exist before the install; exit 0; `dev/.cairn/cairn-lock.yml` is absent. It already passes; it is the Security Review's control.

*Step 2, the change.* (a) `config.py`: append `("core/gitattributes.txt", ".gitattributes", True),` after the last row of `_SKILLS_MAPPINGS`, under the comment `# Root line-ending rules: verbatim, so no cached copy lands under dev/.cairn/base/ (a live .gitattributes there would apply to that folder).` (b) `lockfile.py`: add `".gitattributes"` to `_LIVING_STATE_DSTS` under the comment `# Project-choice lines are the adopter's; Git review is the channel. Residual: a -diff, binary or linguist-generated line can hide a file's changes from diff review, this file's own included; no integrity check reads attributes, so Cairn files' hashes are unaffected.` Directly after the set add `_KEPT_EXISTING_DSTS: frozenset[str] = frozenset({".gitattributes"})` under `# Paths the installer never overwrites, even with --force, and whose differing copy does not stop the lockfile. One path only: any other differing file still withholds it.` (c) `install.py`: import `_KEPT_EXISTING_DSTS` in the `from .lockfile import (` block. In `_install_one` let `kept` be true when `dst.parent == target` and `dst.name in _KEPT_EXISTING_DSTS`; the test at line 367 becomes `dst.exists() and (kept or not force)`. When `kept`, `dst.is_file()` and its bytes differ from what this call would write, print to stderr `  [keep] <dst>: already exists and is never replaced, even with --force. Merge the lines you want by hand:` and the source text, each line indented four spaces; otherwise print the existing `[skip]` message. Return `skipped-exists` either way. In `write_install_lockfile`, immediately before the test at line 2322, add: when `dst_rel in _KEPT_EXISTING_DSTS` and `on_disk` is not `None` and differs from `would`, `continue` (no record, not in `diverged`).

*Step 3, mutants.* Each made in one file, run against one named node, restored with `cp` from a saved copy and `cmp` printing nothing: (M1) drop the `dst_rel in _KEPT_EXISTING_DSTS` condition from the exemption (T4 fails); (M2) drop `kept or` at line 367 (T2 `--force` case fails); (M3) delete the exemption (T2 fails: no lockfile); (M4) the row's `True` becomes `False` (T1 fails). *Step 4.* T1, T2, T4 pass; run `test_install_time_onboarding.py`, `test_core_dev_folders.py`, `test_manifest.py`, `test_upgrade_side_door_parity.py`, `test_verify_integrity.py` (the full list for these paths runs once, in C3). Commit the template, the three engine files and the test file.

The template, 154 words:

```
# Line endings. Text files are stored and checked out with LF on every machine,
# so a Windows checkout matches the repository and Cairn's recorded file hashes.
# Cairn installs this file only when the project has none, and never replaces
# yours. Edit the project choices below.
* text=auto eol=lf

# Windows scripts keep CRLF. Name only paths Cairn does not install, because
# Cairn records the hash of each installed file's LF bytes.
*.bat text eol=crlf
*.cmd text eol=crlf

# Binary files are never converted.
*.png binary
*.jpg binary
*.gif binary
*.pdf binary
*.zip binary
*.gz binary
*.tif binary
*.nc binary
*.h5 binary
*.npy binary

# Project choices: Cairn cannot know your paths. Uncomment and edit.
# Data and evidence that must stay byte for byte (raw instrument output):
# *.csv -text
# *.dat -text
# Files a Windows tool requires with CRLF:
# *.sln text eol=crlf
# *.reg text eol=crlf
```

**C2.** Add T3, T5, T6; C1 already makes them pass, and no engine file is edited. If one fails, stop and report; do not edit `upgrade.py`. **T3** `test_upgrade_keeps_it_blocked_until_adopted_and_adoption_saves_no_copy`: the pre-existing file is `b"# mine\n"`. `s._compute_upgrade(target, CAIRN_ROOT, TEMPLATES_ROOT, lock, None)` plans `.gitattributes` as `new-core-blocked`, `src` `core/gitattributes.txt`, `verbatim` true. `upgrade --stage` exits 0; `--apply` and `--apply --force` exit non-zero; bytes unchanged. Adopt with the `dst@observed@upstream` triple as `_adopt_args` builds it (copy that helper): exit 0, bytes unchanged, a record with `verbatim` true, `living_state` true, no `base_cache`, `hash` of the adopter's bytes, `base_hash` of the template's. Then no plan of kind `new-core-blocked` remains for it; re-stage and `--apply` exit 0 with bytes unchanged. Last, `git init`: `list((target / "dev").rglob(".gitattributes"))` is empty and `git check-attr -a -- dev/.cairn/base/AGENTS.md` prints nothing (a cached copy of Cairn's file there would print `text: auto`). **T5** `test_verify_integrity_accepts_an_edited_copy`: append `*.csv -text` to the installed file; `verify_integrity.verify(target)` is 0; the control, a line appended to `tools/board.py`, makes it non-zero (import `verify_integrity` as `test_core_dev_folders.py` does). **T6** `test_no_crlf_rule_matches_an_installed_path`: install with every module (the profile of `test_manifest_matches_actual_install`), `git init`, list every file except `.git`; `git check-attr --stdin -z eol` over them reports none as `crlf`, while a probe path `probe.bat` in the same call does, so a parse that finds nothing fails. Mutants: M4 also fails T3; (M5) remove the `_LIVING_STATE_DSTS` entry (T5 fails); (M6) change `*.bat` in the template to `*.py` (T6 fails). Run T1 to T6. Commit the test file.

**C3.** *Tests first.* **T7** `test_install_counts_crlf_files_in_the_index`, four cases, skipped with a stated reason when `git --version` is below 2.45 (the safe reader's floor). Each runs `git init`, writes two files with `\r\n`, adds them with `git -c core.autocrlf=false add` (no commit), installs, and reads stdout and stderr together. `crlf-in-index`: a line matches `\[note\] 2 [^\n]*i/crlf`. `lf-only`: files with `\n`; neither `i/crlf` nor `ls-files --eol` appears. `own-file-kept`: CRLF files and a different `.gitattributes` first; neither appears. `read-unavailable`: as `crlf-in-index`, with `run_git` on the helper module `install._git_read_helper()` returns, patched by `monkeypatch` to return `helper.ReadResult("failed", None, b"", "x")` for `("ls-files", "--eol")` and to pass other calls through; `ls-files --eol` appears, the count line does not. First run: fails. *Change.* `_index_crlf_count(target)` returns 0 when `target / ".git"` does not exist; otherwise runs `git_read.run_git(str(target), ("ls-files", "--eol"), timeout=30)` through `_git_read_helper()` as `git_provenance_warning` does, and returns the number of output lines whose first field is `i/crlf`, or `None` when the read did not complete or exited non-zero or the helper raised `OSError`, `RuntimeError` or `ValueError`. In `print_report`, just before the comment `# Unfilled inline tokens`, only when no row is `dry-run` and the row for `target / ".gitattributes"` has status `installed`: for `n > 0` print `  [note] {n} file(s) in the Git index have CRLF line endings (git ls-files --eol lists them as i/crlf).` then, indented nine spaces, `The new .gitattributes makes Git show them as modified until they are renormalized. Commit .gitattributes alone first, then follow bootstrap/BOOTSTRAP.md, II-2b. Do not renormalize while other work is uncommitted.`; for `None` print `  [note] Could not count CRLF files in the Git index. Run git ls-files --eol; if any line starts with i/crlf, follow bootstrap/BOOTSTRAP.md, II-2b before committing.` Also build `skipped` without the `target / ".gitattributes"` row, which `--force` cannot overwrite. Mutants: (M7) `i/crlf` becomes `i/lf` in the counter (`crlf-in-index` fails); (M8) drop the `installed` condition (`own-file-kept` fails). Then run the list for the three engine files once and compare with the control: a node failing only now is yours; a node red in both is recorded as red before. Commit `install.py` and the test file; report the `repin.py status` differences.

**C4.** Exact replacement. `bootstrap/BOOTSTRAP.md`: (1) in "The script:" list, after the optional-templates bullet: "Installs a root `.gitattributes` that stores and checks out text files with LF on every machine (`.bat` and `.cmd` keep CRLF). It never replaces an existing `.gitattributes`, even with `--force`; it prints the recommended lines to merge by hand (II-2b)." (2) at the end of "Safe-by-default re-runs": "`--force` never overwrites an existing `.gitattributes`; that file is yours." (3) a new `### II-2b Line endings in an existing repository` before `### II-3 Select (confirm)`:

```
> **A new repository with no history skips this step.** The installed
> `.gitattributes` is already right for it.

The installed `.gitattributes` sets `* text=auto eol=lf`. If the Git index
already holds CRLF text, Git shows those files as modified until they are
renormalized. The scaffold counts them (`git ls-files --eol` lists them as
`i/crlf`) and prints this step when it finds any.

1. Commit `.gitattributes` alone first.
2. Run `git ls-files --eol` and list the `i/crlf` files. A data or evidence
   file whose checksum you recorded must stay byte for byte: add `-text` for it
   to `.gitattributes` first, because renormalizing changes its stored bytes and
   hash. A Windows tool that needs CRLF (`.sln`, `.reg`) needs an `eol=crlf` line.
3. With no other work uncommitted, run `git add --renormalize .`, read
   `git diff --cached --stat`, and commit.
4. Make a fresh clone; it is the one safe way to refresh every working file.
   Do not run `git rm --cached -r . && git reset --hard`: it discards
   uncommitted work.

If you keep your own `.gitattributes`, the scaffold leaves it alone and prints
Cairn's lines; merge the ones you want by hand. Keep any `eol=crlf` line to
paths Cairn does not install: Cairn records the hash of the LF bytes, so a CRLF
checkout of an installed file fails the integrity check.
```

`bootstrap/UPGRADE.md`: after `### If \`RULES.md\` meets your project rules`, before `## Adopting a hand-placed module`:

```
### If `.gitattributes` meets your own

The core install adds a root `.gitattributes` (line-ending rules; see
`BOOTSTRAP.md` II-2b). It never replaces an existing one, even with `--force`,
and records nothing for yours. The first `upgrade --plan` therefore shows it as
`new-core-blocked`, and `--apply` refuses, until you remove your file and
re-stage (to take Cairn's) or run the `--adopt-collisions` command that
`upgrade --stage` prints, once, which keeps yours as a tracked fork. The stop repeats on every upgrade
until you do. Adoption saves no copy under `dev/.cairn/base/` (a live
`.gitattributes` there would apply to that folder), so a later change to
Cairn's file shows as your fork differing from upstream, not as a three-way merge.
With none of your own, upgrade adds Cairn's; if your repository stores CRLF text,
follow `BOOTSTRAP.md` II-2b. After `upgrade --init-lock` records an existing file
as Cairn's, a later change to Cairn's file would be applied over it; check the plan
before `--apply`.

`verify_integrity.py` does not flag edits to this file, so you can change the
project-choice lines. A `-diff`, `binary` or `linguist-generated` line can hide a
file's changes from review, this file's own included: read its changes in Git.
Cairn's own files stay hash-checked, and no check reads attributes.
```

`docs/quickstart.md`: at line 252, `NOTICE.md`, `.gitignore`, becomes `NOTICE.md`, `.gitattributes`, `.gitignore`,; in the `git add` line at 285, `NOTICE.md .gitignore` becomes `NOTICE.md .gitattributes .gitignore`. `bootstrap/tests/test_quickstart_sequence.py`, node `TestLayerAStepsOneThroughThree::test_step3_install_writes_expected_kernel_and_modules`: add `".gitattributes"` to `expected_paths` and, after the `CHANGELOG.md` assertion, `assert ".gitattributes" in committed_paths` with the message "quickstart's documented install commit must include .gitattributes". Run `claim_check.py`, `link_check.py` and `sync_doc_snippets.py --check` on the three documents, the list for the four paths once, and `quality_gate.py --sub neutrality` before and after (no new finding). Commit the four paths.

**C5.** On `cairn-windows` (`dev/rules/development-environment.md`, Windows VM; x64 `C:\ProgramData\miniconda3\envs\lhm\python.exe`; transfers authorized, Maintainer chat 2026-11-12). `git archive --format=tar <C4 commit>`, `scp`, `tar -xf` into new folders `C:\Users\cairn\cairn-gitattr-<date>` and `...-work-<date>`; nothing existing is overwritten, no setting or package changes. *(a)* From the tree run `... -m pytest -p no:cacheprovider -rfsE -v bootstrap/tests/test_gitattributes_install.py`. Pass: every node passes; none fails or skips (the VM has Git 2.56). *(b)* As (b) of `dev/measurement/windows-defects-run-2026-11-16.md`: make `proj` (`scaffold.py --config profile.yml --target proj --cairn-root <tree> --allow-dev`, `git init`, `git -c core.autocrlf=false add -A`, one commit) and `proj-own`, the same with `# none` written to `.gitattributes` first and a saved copy of it. Clone each with `git -c core.autocrlf=true clone` (`proj-attr`, `proj-own-crlf`); run `upgrade --plan` over both into files. **Pass**: `proj`'s `.gitattributes` matches the tree's template (`fc /b`: no differences); `proj-own`'s matches its saved copy and `findstr` finds no `.gitattributes` in its `dev\.cairn\cairn-lock.yml`; in `proj-attr`, `git status --porcelain` prints nothing, `git ls-files --eol` has at least one line with `attr/text=auto eol=lf` and none with `w/crlf`, and its plan has no line containing `line endings` or `review-only`. **Control**: `proj-own-crlf` has at least one `w/crlf` line and its plan at least one `line endings` line; otherwise record "not reproduced", which makes (b) prove nothing, and stop. Write `dev/measurement/windows-git-attributes-run.md` in the form of `dev/measurement/windows-route-checks-2026-11-16.md`: result table, environment (build, interpreter, Git version, the system `core.autocrlf`), folders and commit, commands, counts, and what was not run (the II-2b steps end to end, native ARM64 Python, older Git, a physical machine, any other file). Commit it alone.

**C6.** `CHANGELOG.md`, under `## Unreleased` > `### Minor changes`, after the last **Fixed**: "- **Fixed** — New installs add a root `.gitattributes` so text files keep the same line endings on every machine, which stops a Windows checkout from silently differing from the repository; an existing `.gitattributes` is never replaced, even with `--force`. If your repository already stores Windows (CRLF) text, the installer counts those files and points to the steps in `bootstrap/BOOTSTRAP.md`, II-2b." (Minor: it repairs the reported line-ending fault.) `dev/PLANNING.md`, section 1: set this plan's row to "implemented and verified, waits on the Maintainer's re-anchor", or add it after the `Fix what adopters hit in 0.7.0.` row if absent, and point that row's follow-on-draft sentence at the plan. The layout row also notes it must name `.gitattributes` a root exception and move this plan's paths. Append a plan `## Implementation` entry naming each chunk's commit and stating only departures. Run `claim_check.py` and `board.py`; commit the three paths.

## Scope delta

**Scope delta**: preserved

Every Decision outcome is delivered: option A as revised, standard tier with plan and Security Review, verbatim install with no copy under `dev/.cairn/base/`, and the `git_read`/`ident` item left separate. Changes the Maintainer may reverse: the row sits in `_SKILLS_MAPPINGS`, not `_CORE_MAPPINGS` (the verbatim flag lives there); a new one-path set `_KEPT_EXISTING_DSTS` and helper `_index_crlf_count`; a printed fallback when the count cannot be read; the quickstart's `git add` line and one existing test gain the new file. Declined as expansions, not reductions: an upgrade-time count, a `.gitattributes` in Cairn's own checkout.

## Verification

Promises and public entries: a fresh install writes and records the file; a different file survives install, `--force` and upgrade byte for byte with the lockfile still written (T1, T2: `scaffold.main`); any other differing file still withholds the lockfile (T4, the blocking finding's control); `upgrade --plan` blocks until adoption and adoption saves no copy (T3: `_compute_upgrade`, `upgrade`, `git check-attr`); `verify_integrity` accepts an edited copy (T5); no CRLF rule matches an installed path (T6); the install counts CRLF index files and says when it cannot (T7); the quickstart's commit includes the file; Windows shows a clean checkout (C5). No test asserts prose: they check bytes, exit codes, record fields, plan kinds, counts, Git's own labels and the template's own lines. S2: T4 with M1 and M3. S3: the new file and the C3 list. The eight mutants show the tests can fail.

Not run: the whole suite; any test (this author ran none); the Windows VM beyond C5's checks; native ARM64 Python; Git older than 2.45; the II-2b steps end to end; Cairn upgrading itself. Assumed, not measured: that `eol=lf` overrides `core.autocrlf` on Windows (Git's documentation; C5 measures it); that the listed files which write a `.gitattributes` into an installed project (`test_upgrade_edit_check_runs_no_project_programs.py`, `test_upgrade_removes_retired_files.py`) stay green.

## Plan review -- Claude Sonnet 5.5 (Plan Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: 0d0672c28b171c2c9e2e5d96be6b201926d9f353
```

**Obligation**: Clear that each chunk C1 to C6 can be run by a Low-tier implementer with no design left to them that matters, that the plan delivers every outcome the accepted Decision adopted (none lost or silently changed), and that its order, ownership, frozen-file and re-anchor statements are true. This Internal pass does not clear the Internal Security Review.
**Tier**: Internal
**Findings**: raised
**Verdict**: ACCEPT
**Elapsed**: about 13 minutes (16:38 to 16:52 EST)
**Tokens**: unknown

Strongest case: the skills table already carries the verbatim flag, so one row, one one-path set and one small branch deliver the no-copy install, and each chunk names its test, first failing run and mutants.

**Foundations**

1. **Should this happen as framed?** Yes. Core rows are always non-verbatim, so the `_SKILLS_MAPPINGS` route is a different mechanism that still delivers every adopted outcome (ships and recorded T1; kept even with `--force` T2; `new-core-blocked` until adoption, no `dev/.cairn/base/` copy T3; one-path exemption T4; living state T5). It is not a reduction, so no Maintainer allowance is owed under Scope delta. -- `bootstrap/_scaffold/install.py:2033`, `bootstrap/_scaffold/upgrade.py:1034-1035`, `bootstrap/_scaffold/upgrade.py:2006-2036`
2. **Best alternative.** Nothing simpler delivers the same outcomes: a third tuple element touches `install.py:396` and `2033`, `upgrade.py:643` and `1034`, and frozen `test_manifest.py:64`. Six chunks could be four (C2 into C1, C6 into C4); not worth a finding. -- `git grep -n _CORE_MAPPINGS bootstrap`
3. **What would show it wrong.** T4 still passing with M1 applied (exemption wider than one path), or C5's `proj-attr` showing `w/crlf` once its control `proj-own-crlf` has reproduced the fault. -- plan C1 step 3, C5

**Findings**

1. **Non-blocking, C4 (UPGRADE.md block).** The commonest upgrade, an adopter with no `.gitattributes`, gets `new-core` and a CRLF index that Git then shows as modified; the block names only the collision, though Non-work says "`UPGRADE.md` carries the steps". It also says `upgrade --plan` leads to "the displayed `--adopt-collisions` command"; only `--stage` prints it (`upgrade.py:1334`, `4480-4488`). Closes with: one sentence for the no-file case pointing to II-2b, and "run `upgrade --stage`" before the command.
2. **Non-blocking, C1 and C3 (what the skills row also changes).** A kept file returns `skipped-exists`, so under `--force` the report prints "Files skipped -- already exist, --force not set" and "Pass --force to overwrite" for it (`install.py:1909-1920`); the table's lead comment says lifecycle skills (`config.py:907-913`). The stderr `[keep]` line already explains. Closes with: one line in C3 saying leave both as they are, or the one-line change.
3. **Non-blocking, C5.** The proposal's Windows check says `upgrade --plan` has no review-only files; C5 checks only that no line contains `line endings`. Closes with: add "no `review-only` row" to `proj-attr`'s pass, or state the narrowing.
4. **Non-blocking, C6.** "The layout plan must name `.gitattributes` a root exception" has no home; the layout row (`dev/PLANNING.md:90`) does not mention it. Closes with: one clause on that row in C6.

No chunk is returned for missing design: C1 to C6 are specified enough, C5 included. The tests cover the Security findings (T4 with M1, T1 and T3, T6 with its `probe.bat`) and pin no wording; T7 pins a count and Git's own `i/crlf` label.

Frozen and order, measured: none of the eight edited paths is in `frozen_files`; `config.py` is `cascade_mutable` (note only); `repin.py status` already lists `print_report` among six CHANGED keys, so the plan adds four CHANGED and two NEW; digest notes never HOLD (`bootstrap/tests/_gate_manifest.py:872-890`), so "does not wait for the re-anchor" is true. Group 1 is committed (C10 record `530c922e`); no other open plan edits `install.py`, `config.py`, `lockfile.py` or `BOOTSTRAP.md`.

**Security, one line, not cleared here:** the Security Review should read `upgrade --init-lock` (`upgrade.py:1959-1974`), which records an existing `.gitattributes` as Cairn's own with no `base_hash`, so a later template change could classify it `update` (`upgrade.py:859`); and the `[keep]` branch's read of the destination before `_assert_safe_write`. Read, not run.

**Does any rule weaken or disappear?** No. One rule gains an exception: `--force` never overwrites `.gitattributes`, which C4 states beside "Safe-by-default re-runs" (`bootstrap/BOOTSTRAP.md:353-368`).

**Coverage**: Ran no test, installer or scratch install, and not the VM, so T1 to T7 and their first-run failures are read, not confirmed. Did not judge the security question, or whether `eol=lf` beats `core.autocrlf` on Windows (the plan assumes it; C5 measures it). The plan and every code file I read are unchanged from the Reviewed commit to HEAD `4684e848`. About 750 words by whitespace count (headings and the block included), over the 300 target: the mechanism check and the frozen-file check are measured claims the Obligation asked for.

## Plan review -- Claude Opus (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 7322586586693f89ed0207f1e8590240fb3137fe
```

**Obligation**: Decide whether a Cairn-installed, adopter-edited or planted `.gitattributes`, or this plan's installer changes, can make Cairn's checks run a program, hide a change from review, bypass a guard, or write outside the intended path.
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: ACCEPT
**Elapsed**: about 5 minutes (16:52 to 16:57 EST)
**Tokens**: unknown

Strongest case: the change only ever declines to write, and the one guard it relaxes is keyed to one root path with a test that fails if it widens.

**Foundations**

1. **Should this happen as framed?** Yes. Safe on (a), (b), (d), (e), (f); one non-blocking promise gap on (c).
2. **Best alternative.** None safer; a `_CORE_MAPPINGS` route has the same guards.
3. **What would show it wrong.** T4 passing under M1; a write at `.gitattributes` when a link or folder sits there.

**Measured (read, not run).** (a) The exemption tests `dst_rel in _KEPT_EXISTING_DSTS`, a one-path set, before the `diverged` test (`install.py:2321-2323`); T4 with M1 fails if it widens. (b) A skills row adds no write path: `install_skills` calls the same `_install_one` (`install.py:431-441`); the fan-out and symlinks touch only `.agents/skills`; `security_check.py:1276` scans `.py` only. A kept link or folder returns before `_assert_safe_write` and writes nothing; a dangling link still reaches it. (d) No check reads attributes (`git_read.py:607-620`); the plan states the residual in `lockfile.py` and `UPGRADE.md`. (e) `ls-files --eol` goes through `git_read.run_git` (argv list, hooks and fsmonitor off, allowed at Git 2.45 or later, `git_read.py:588-606`) and yields only a count. (f) C5 uses the authorized transfers and new folders, with `-c` settings only. Frozen: of the touched paths only `bootstrap/verify_integrity.py` is in `frozen_files`, and it is unedited; `repin.py status` shows `print_report` already CHANGED, so the re-anchor list is right.

**Findings**

1. **Non-blocking, (c).** `--init-lock` records an existing `.gitattributes` as Cairn's, with `hash` equal to its own bytes and no `base_hash` (`upgrade.py:1964-1967`). The next template change then classifies it `update` (`lockfile.py:486-491`), and `--apply` replaces the adopter's file. Every other path is attested the same way, and verify skips this file, so there is no trust gap. The gap is in the promise "never replaced". Closes with: one sentence in C4's `UPGRADE.md` block, or an accepted note.

**Coverage**: Ran no test, installer or VM. Did not read the upgrade apply writer, the stage folder's handling of dot-names, or hardlinked destinations. A folder at the path crashes the lockfile read for any path, as today. About 390 words: six obligation items each needed one cited line.

## Response -- Claude Sonnet 5.5 (plan author, Medium) -- 2026-11-16

**Elapsed**: about 6 minutes (start 16:50 estimated, end measured with `date`)
**Tokens**: unknown
**Disposition**: ready-to-implement

Conclusion: all five notes are non-blocking and all are folded in with 77 added words; I checked each against the tree first. No test added; none pins this wording. Not run: any test, a scratch install, the Windows VM.

| Note | Disposition | Where answered |
|---|---|---|
| I1 (no-file case; `--stage`) | Accepted. Only `--stage` prints the command (`upgrade.py:4480-4488`). | C4, UPGRADE.md block |
| I2 (`--force not set` for a kept file) | Accepted: `skipped` drops that row (`install.py:1898`). | C3 |
| I3 (C5 narrower than the proposal) | Accepted: `review-only` text prints only for real entries (`upgrade.py:1300`). | C5 |
| I4 (layout dependency) | Accepted: one clause on the layout row. | C6 |
| S1 (`--init-lock` records yours) | Accepted as one sentence, no code change (`upgrade.py:1964-1967`, `lockfile.py:486-491`). | C4, UPGRADE.md block |

Additions beyond the notes: none; the Length line's counts were remeasured.

## Implementation

Implementation began while this header still said `ready-to-implement`; these
status changes record the actual work afterward and are not backdated.

- **C1 — `ac76f0c8`:** template, verbatim mapping, one-path living-state and
  lockfile handling. T1, T2 and T4 passed; initial T1/T2 failures exposed the
  missing install behavior. Elapsed and tokens: unknown.
- **C2 — `1e527a17`:** T3, T5 and T6 passed with the C1 implementation.
  Elapsed and tokens: unknown.
- **C3 — `a38c32d1`:** bounded index count and report. The four T7 cases and
  T1–T6 passed; the first T7 run failed on the two expected missing notes.
  Elapsed and tokens: unknown.
- **C4 — `8bc30bc6`:** adopter guides and quickstart. The named quickstart
  node passed; claim, link and snippet checks passed. The 15-file selector
  output was recorded as candidate coverage and not run, pending the grouped
  verification disposition. Pre-edit neutrality was not run; the after-edit
  result was 0 failures and 43 informational findings. Elapsed and tokens:
  unknown.
- **C5 — `e24933cb`:** native Windows evidence is in
  `dev/measurement/windows-git-attributes-run.md`; its focused file passed
  10/10 with no skips and its control reproduced the CRLF checkout fault.
  Elapsed and tokens: unknown.

**Mutation controls.** In an isolated temporary snapshot, M1–M8 each made its
targeted public check fail: M1/T4; M2 and M3/T2; M4/T1; M5/T5; M6/T6; M7/T7
`crlf-in-index`; M8/T7 `own-file-kept`. Every changed source file was restored
from its saved copy and `cmp` passed. M1/T4 failed at the lockfile-presence
assertion when the exemption was broadened. The additional M4/T3 check failed
at `fp.verbatim is True` when the mapping flag was false. No mutant survived.

**Baseline and remaining work.** The post-C3 AST status adds the planned
changes to `_LIVING_STATE_DSTS`, `_SKILLS_MAPPINGS`, `_install_one`,
`print_report` and `write_install_lockfile`, and the new
`_KEPT_EXISTING_DSTS` and `_index_crlf_count` keys. The pre-existing Group 1
AST and frozen-file results remain unpassed; no agent re-anchored them. The
15-file mapped selection and its before/after controls remain pending the
Maintainer's grouped verification disposition. Ordinary and Security review
records are pending; the separate Maintainer re-anchor is not a plan blocker.

**Benefit versus cost**: worth it — fresh checkouts keep consistent text line
endings while adopter-owned attributes survive install, force and upgrade;
measured focused test runtimes were 11.79 seconds on the host, 2.30 seconds for
the quickstart node and 25.57 seconds on Windows, plus 12.6 seconds for M1–M8
and 2.6 seconds for M4/T3. Setup and agent time are unknown. Remaining burden:
grouped verification disposition and required reviews. Revisit after those
records are complete; the Maintainer re-anchor remains separate.
