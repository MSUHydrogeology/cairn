# Windows run of the adopter-defects plan (chunk C8), 2026-11-16

Evidence for chunk C8 of `dev/plans/2026-11-16-adopter-defects-0-7-0.md`. It
records, with output, which of the defects that plan fixed are fixed on a real
Windows machine. Record only: no code, test or document was changed. It is not a
release record.

## Result

Four of the five checks passed. The fifth, the Windows commit hook (63.1), did
not: the hook still cannot read the staged file paths on Windows. Chunk C7 now
names the reason, and the reason is not the one the plan predicted.

| Item | What it checks | Result |
|---|---|---|
| (a) | Every test added or changed by C1 to C7 | Pass. 37 tests, 88 cases: 70 passed, 18 skipped, 0 failed |
| (b) | 63.2, line endings after `core.autocrlf=true` | Pass. Both named texts appear over the CRLF copy, neither over the LF copy; the control shows the old text |
| (c) | 64.1, no `\x0d` in `session-start` output | Pass. Control shows 6 `\x0d`; the C7 tree shows 0 |
| (d) | 63.1, the commit hook reads staged paths | **Fail.** Reason printed: `worker-request-invalid` (the control printed `worker-incomplete`) |
| (e) | Item 8, network and drive targets refused | Pass. All 19 cases of the two item-8 tests passed; `link_check.py` took 0.23 to 0.29 s over `\\192.0.2.1\share\zz.md` |

Per the plan's Sequence section, a confirmed hook failure returns the plan to
`revising-plan` with a Plan change. That step is the coordinator's and the
Maintainer's. I did not fix, edit or diagnose further.

## What was measured, and what was only read

- **Measured on Windows:** every number, exit code, output line and reason code
  in the sections below.
- **Read from the code, not run:** where in `tools/git_read.py` the string
  `worker-request-invalid` can come from (see item (d)); what the hook does with
  a failed read (`tools/_intent/conflict.py`).
- **Not measured:** whether any network connection is opened (item (e)); elapsed
  human time and tokens (`unknown`); the cause of the hook failure.

## Environment

- **Machine.** Windows 11 Pro 10.0.26300 (`ver` reports 10.0.26300.9974),
  "ARM64-based PC" under UTM, SSH alias `cairn-windows`.
- **Interpreter.** x64 build, `C:\ProgramData\miniconda3\envs\lhm\python.exe`:
  Python 3.13.18 (`sys.version` says AMD64), pytest 9.2.0. (`platform.machine()`
  returned `AMD64` in one call and `ARM64` in another, so I rely on
  `sys.version` and `systeminfo`.)
- **Git.** 2.56.0.windows.4. The VM's system Git configuration sets
  `core.autocrlf` to `false` and `core.symlinks` to `false`.
- **Date and time.** 2026-11-16, 14:29 to about 14:52 EST.

## Folders and trees

All folders are new, under `C:\Users\cairn\`. Nothing existing was overwritten.
No system setting was changed and no package installed. Each tree came from
`git archive --format=tar` of one commit (no `.git` inside, nothing uncommitted)
sent by `scp` and unpacked with `tar -xf`.

| Folder | Commit | Use |
|---|---|---|
| `cairn-defects-c8-20261116` | `8722c7d5` (HEAD) | the tree under test; items (b) to (e) |
| `cairn-defects-c8-control-20261116` | `71b185df` | pre-plan control for items (c), (d) |
| `cairn-defects-c8-files-20261116` | `8722c7d5` | untouched copy for whole-file runs of item (a) |
| `cairn-defects-c8-controlfiles-20261116` | `71b185df` | untouched copy for the control runs of item (a) |
| `cairn-defects-c8-work-20261116` | none | the projects of item (b), scratch scripts, copies of the archives and outputs |

- **Why `8722c7d5`.** The coordinator asked for the committed tip. The last C7
  commit is `32f1546d`. `git diff --name-only 32f1546d 8722c7d5` lists no file
  outside `dev/`, so the code, scripts, templates and tests of the two trees are
  the same (measured).
- **Why `71b185df` for the control.** The plan says "the parent of the earliest
  C1 commit". The earliest of the plan's commits is C5 (`3afa1b91`, committed
  before C1's `3c6f7136`), so the parent of C1 already holds C5 and would not
  reproduce item (c). `71b185df` is the parent of `3afa1b91`: it holds none of
  C1 to C7.
- **Archive hashes (SHA-256).** HEAD tar `676722b6ebb8bd0f6b491df4742bd3e070e5daddecac9a6824393af3e1218390`;
  control tar `ab7f363549bfef00e66737dd23543e59d326ca1fe29ba146630ad5cdad5301e4`.

## (a) The changed tests

**Which tests.** I took the 9 test files that changed from `71b185df` to
`32f1546d` and kept each test function whose lines overlap the diff: 37 tests.
A function changed only through a shared helper edited elsewhere would be
missed; I did not look for one. The files are `test_link_check_exclusions.py`
(3), `security/test_git_read.py` (7), `test_claim_check_module.py` (1),
`test_content_scan.py` (1), `test_doc_drift_tools.py` (2),
`test_session_binding_gate_and_printing_hold.py` (2),
`test_session_routines.py` (2), `test_upgrade.py` (9) and
`test_upgrade_added_slots.py` (10), all under `bootstrap/tests/`.

**Run 1, the 37 tests by name** (fresh `cairn-defects-c8-20261116`, before any
`git init`):

```sh
ssh cairn-windows 'cd /d C:\Users\cairn\cairn-defects-c8-20261116 && C:\ProgramData\miniconda3\envs\lhm\python.exe -m pytest -p no:cacheprovider -rfsE -v @C:\Users\cairn\c8-nodes-20261116.txt'
```

Result: 88 cases collected, **70 passed, 18 skipped, 0 failed**, 72.60 s, exit 0.
All 18 skips are the two session-reader tests of C5 (`test_child_streams_...`
and `test_only_a_cr_directly_before_lf_is_folded_in_child_output`), skipped with
"the stand-in interpreter is a shell script". So C5's unit tests did not run on
Windows; item (c) is the Windows evidence for 64.1. The C1 item-8 cases (16
refused, 3 controls), the C3 tests that need Git 2.45 (`HEAD` and `--output=`
cases) and all C7 tests ran and passed.

**Run 2, the nine whole files** (fresh `cairn-defects-c8-files-20261116`, same
interpreter, `-q`): **15 failed, 664 passed, 82 skipped**, 506.93 s. None of the
15 is among the 37 tests of run 1. I compared each with the same test in the
control folder (fresh `cairn-defects-c8-controlfiles-20261116`, at `71b185df`):

| File | Failed on HEAD | Same test fails in control |
|---|---|---|
| `test_upgrade.py` | 7 | 7 of 7 |
| `test_session_routines.py` | 4 | 4 of 4 |
| `test_doc_drift_tools.py` | 3 | 3 of 3 |
| `security/test_git_read.py` | 1 (`test_read_origin_uses_git_parser_for_quoted_and_continued_values`) | yes, in a whole-file control run (1 failed, 32 passed, 19 skipped, 17.65 s) |

The 14 in the first three rows were re-run by name in the control folder: 14
failed, 1 skipped, 19.73 s. The `test_git_read.py` test skips when run alone, in
both folders ("real Git 2.44 or newer is required"), and fails when its whole
file runs, in both folders. So it depends on test order and is not new. I did
not diagnose the other 14 (two show `tracked Markdown discovery failed`).
Result: **no failure introduced by C1 to C7.** The 19 failures of
`test_git_read.py` recorded on 2026-11-13 are now 1.

## (b) 63.2: a project checked out with `core.autocrlf=true`

Tree `cairn-defects-c8-20261116`; folder `cairn-defects-c8-work-20261116`. The
profile holds `project_name: Demo`, `test_command: pytest`,
`preset: solo-greenfield`.

```sh
python bootstrap\scaffold.py --config profile.yml --target proj --cairn-root <tree> --allow-dev
git init; git -c core.autocrlf=false add -A; git -c core.autocrlf=false commit   # one commit, clean after
git -c core.autocrlf=true  clone proj proj-crlf
git -c core.autocrlf=false clone proj proj-lf
python bootstrap\scaffold.py upgrade --target proj-crlf --plan --cairn-root <tree>
python bootstrap\scaffold.py upgrade --target proj-lf   --plan --cairn-root <tree>
```

(`python` is the interpreter above; `git commit` also carried `-c user.name=t -c
user.email=t@example.test`.) The two plan runs and the two clones exited 0; the
install printed its normal completion output (it wrote the lock and the base
cache) and its exit code was not captured; the commit showed a clean status.
Carriage returns were checked byte by byte: `proj-crlf` holds `\r\n` in
`AGENTS.md`, `dev/.cairn/base/AGENTS.md` and `scripts/claim_check.py`; `proj` and
`proj-lf` hold none.

| Plan run | Saved-ancestor text | Script flag text |
|---|---|---|
| C7 tree over `proj-crlf` | 28 files: `saved ancestor differs only in line endings (core.autocrlf?); see UPGRADE.md (review-only diff)` | 19 files: `differs only in line endings (core.autocrlf?); see UPGRADE.md` |
| C7 tree over `proj-lf` | 0 (no `[warn]`, no `[flag]` line at all) | 0 |
| control tree over `proj-crlf` | 28 files: `saved ancestor is missing or invalid (review-only diff)` | 19 flags with empty text, 0 line-ending text |

**Pass.** The control run (`71b185df` tree over the same `proj-crlf`) shows the
old text, so the new text comes from the plan's change. `proj-lf` under the same
tree shows neither text.

## (c) 64.1: no `\x0d` in `session-start`

In each of the control and the C7 folder: `git init`, `git add -A`, one commit,
then

```sh
python tools\intent.py claim --files README.md --action probe --stem winprobe
python tools\session.py session-start > <file> 2>&1
```

| Tree | Literal `\x0d` in the output | Exit |
|---|---|---|
| control `71b185df` (run first) | **6** (the six lines of the claim record, each ending `\x0d`) | 0 |
| C7 tree `8722c7d5` | **0** | 0 |

The control reproduces the defect, so the zero is meaningful. **Pass.** The
output files also hold raw carriage-return bytes (45 and 46). I read these as
the line terminators Windows adds when a Python program writes `\n` to a file
(the counts match the line counts; I did not check them one by one). The check
is for the printed text `\x0d`.

## (d) 63.1: the hook that reads staged paths

**Setup, both folders.** `git init`, one commit, `python tools\intent.py
install-precommit` (exit 0; it wrote the usual hook: the interpreter, then
`tools\intent.py _precommit_check`), then a real commit of one staged new file:

```sh
git add c8-probe-hook2.txt
git -c user.name=t -c user.email=t@example.test commit -m probe2
```

| Tree | `git commit` exit | Output |
|---|---|---|
| control `71b185df` (run first) | 0 | `intent: WARNING -- staged path discovery is unavailable; pre-commit coordination is unknown (allowing under existing policy).` then the commit |
| C7 tree `8722c7d5` | 0 | the same warning, then the commit |

The commit exits 0 in both because the hook only warns. The warning shows the
hook did not read the staged paths before or after C7. **Item (d) fails.**

**The reason code.** The hook's own output never prints a reason: in
`tools/_intent/conflict.py`, `_staged_paths_via_git` returns `None` for any
failed read and drops the reason (read from the code). So the plan's "C8(d)
should now print that reason" does not hold for the hook itself. To read it I
ran a scratch script inside a real pre-commit run. It makes the exact call the
hook makes, `read_hook_index(<repository>, ("diff","--cached","--name-only","-z"),
index_file=<GIT_INDEX_FILE>)`, and prints the result. The scratch hook was given
on the command line only (`-c core.hooksPath=<scratch folder>`, so no repository
setting changed) and made the commit fail on purpose, so nothing was committed.
The script and hook live in `cairn-defects-c8-work-20261116` and are not
committed.

| Tree | state | returncode | reason |
|---|---|---|---|
| control `71b185df` | `failed` | `None` | `worker-incomplete` |
| C7 tree `8722c7d5` | `failed` | `None` | **`worker-request-invalid`** |

`GIT_INDEX_FILE` was `'.git/index'` in the run. The second hook read
(`diff --cached --name-status -M -z`) gave the same reasons.

**Not what the plan predicted.** The plan expected `verified-helper-buffer-unavailable`
(the worker bootstrap sets `__verified_source__` but not `_VERIFIED_SOURCE`). That
code did not appear. A supplementary read through the same loader and worker
route (`run_git(<repository>, ("rev-parse","--verify","HEAD"))`) **completed**
in both trees (state `completed`, returncode 0, the commit id returned). So the
worker route works for a plain read on Windows, and only the hook-index read
fails.

**Where the code can come from (read, not run).** In `tools/git_read.py`
`worker-request-invalid` is the starting value of the bootstrap's `stage`
variable and is also raised at nine sites in `_windows_worker_run`, including the
`hook-index` branch (its argument list, its snapshot of 8 fields, and the check
`_hook_snapshot_matches` run inside the worker). The printed reason cannot say
which site fired. I did not run `_windows_worker_run` from a scratch script: the
plan prescribes that only for `worker-run-failed`, and the coordinator told me
to stop this item. No code was edited.

## (e) Item 8: network and drive targets refused

**Tests.** The 16 refused cases (8 targets, each listed and not listed in
`link-check-allow`) and the 3 controls in
`test_link_check_exclusions.py` passed on Windows in run 1 of item (a). They
include the spy on `pathlib.Path.resolve` that sees no path ending in `zz.md`;
the spy covers `Path.resolve` only, not every filesystem call. The two other C1
tests in `test_doc_drift_tools.py` (absent and invalid scanner settings), the
changed test in `test_link_check_exclusions.py` and the hidden-character test in
`test_content_scan.py` also passed.

**Timing.** A one-line document `See [net](\\192.0.2.1\share\zz.md) for context.`
(192.0.2.1 is TEST-NET-1, not routed), with `--root` a scratch folder, three
runs of the C7 tree's `scripts\link_check.py` (scratch timer, wall-clock):

| Document | Run 1 | Run 2 | Run 3 | Exit | Output |
|---|---|---|---|---|---|
| `\\192.0.2.1\share\zz.md` | 0.286 s | 0.247 s | 0.229 s | 1 | `[link] link target is a network or drive path and is not checked` |
| `zz-missing-local.md` (baseline) | 0.218 s | 0.200 s | 0.215 s | 1 | `[link] broken link target` |

The refused target took about 0.04 s longer on average than a missing local
file (0.254 s against 0.211 s), a difference of the size of normal start-up
variation. I did **not** run the pre-plan `link_check.py` on the
network target: that could open a network connection, which the run rules
forbid. The claim "no connection is opened" stays unmeasured (the operating
system's file-sharing layer was not observed). **Pass** for the tests and the
timing.

## Not run

- No whole-suite run, and no test file beyond the nine named above.
- The 14 unchanged failures of item (a) were not diagnosed.
- One Windows host, one Git version, the x64 interpreter only.
- `python scripts/claim_check.py` and `python scripts/link_check.py` over this
  file ran on the macOS checkout (see the commit).

## Left on the VM

Under `C:\Users\cairn\`: the five folders in the table above. They hold a
`.git` in the first two, probe files `c8-probe-hook*.txt`, and the scratch
scripts. Nothing else was created or removed. The Maintainer may delete them.

**Elapsed:** about 25 minutes of agent time (14:29 to about 14:52 EST, plus reading the plan beforehand).
**Tokens:** unknown.
