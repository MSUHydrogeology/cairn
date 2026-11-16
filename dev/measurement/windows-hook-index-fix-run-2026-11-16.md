# Windows re-run of the commit-hook repair (chunk C10), 2026-11-16

Evidence for chunk C10 of `dev/plans/2026-11-16-adopter-defects-0-7-0.md`. It
records, with output, whether the Windows commit hook (item 63.1) now reads the
staged file paths after chunk C9. Record only: no code, test or document was
changed. It is not a release record.

## Result

**Yes. On Windows the commit hook now reads the staged paths, and the plan does
not return to `revising-plan` for this item.** In a real `git commit` the fixed
tree no longer prints "staged path discovery is unavailable"; the control tree
still does. A direct read inside a real pre-commit hook returns the staged file
name for both allowed forms on the fixed tree and fails with
`worker-request-invalid` on the control.

| Item | What it checks | Result |
|---|---|---|
| (a) | `-k hook_index` in `test_git_read.py` | Pass. Tree under test: 7 passed, 1 skipped, 0 failed; T1 to T5 all passed (T1 passed, not skipped). Third folder (control plus C9's tests): 4 failed, 3 passed, 1 skipped; T1 failed with `worker-request-invalid` |
| (b) | A real `git commit` through the installed hook | Pass. Control printed `staged path discovery is unavailable`; tree under test did not (it printed the claims check's `UNKNOWN IDENTITY` message instead). Both commits exited 0 |
| (c) | Direct `read_hook_index`, both forms, in a real pre-commit hook | Pass. Tree under test: `completed`, return code 0, `c10-probe-direct.txt\0` and `A\0c10-probe-direct.txt\0`. Control: `failed`, `worker-request-invalid`, both forms |
| (d) | `test_git_read.py` and `test_git_read_routes.py` whole | One failure in both trees, the same test at the same line (not C9's). Tree under test 88 passed, control 83 passed (the five C9 tests are the difference) |

## What was measured, and what was only read

- **Measured on Windows:** every exit code, output line, reason code and count in
  the sections below.
- **Measured on macOS (Git 2.53.0):** one dry run of the scratch script
  `c10-direct.py` against an archive of the tree under test before it went to the
  VM (both forms completed with the same two outputs); the archives' SHA-256
  values; that the code of the lock commit `0f85f3e8` equals `cb060551`
  (`git diff --name-only cb060551 0f85f3e8` lists only `dev/.cairn/cairn-lock.yml`).
- **Read from the code, not run:** that the hook turns any failed read into the
  "staged path discovery is unavailable" warning and drops the reason
  (`_staged_paths_via_git` in `tools/_intent/conflict.py`; the C8 record read it
  the same way). That is why (c) calls the helper directly.
- **Not measured:** the claim-overlap logic of the hook itself (no agent identity
  was set, so the `UNKNOWN IDENTITY` branch ran); other Git versions, other
  Windows hosts, the ARM64 interpreter; a linked worktree; human time and tokens
  (`unknown`).

## Environment

- **Machine.** Windows 11 Pro `ver` 10.0.26300.9974, "ARM64-based PC" under UTM,
  SSH alias `cairn-windows`.
- **Interpreter.** x64 build, `C:\ProgramData\miniconda3\envs\lhm\python.exe`:
  Python 3.13.18 (conda-forge, MSC v.1944 64 bit (AMD64)), pytest 9.2.0, pluggy
  1.7.0.
- **Git.** 2.56.0.windows.4 (`git --version` over the same SSH login). The macOS
  side used Git 2.53.0 and Python 3.13.13.
- **Date and time.** 2026-11-16. The VM clock runs three hours behind EST: VM
  12:44 to about 12:54, which is 15:44 to about 15:54 EST.
- **Rules kept.** Four new folders under `C:\Users\cairn\`; nothing existing was
  overwritten or removed; no system setting changed; no package installed; the
  tests opened no network connection that I know of (not observed). The folders
  are left in place.

## Folders and trees

Each tree came from `git archive --format=tar <commit>` on the Mac (no `.git`
inside, nothing uncommitted, so another session's uncommitted edits could not
leak in), sent by `scp` and unpacked with `tar -xf`. The SHA-256 of each tar was
checked on the VM with `certutil` and matched the Mac's.

| Folder under `C:\Users\cairn\` | Commit | Use |
|---|---|---|
| `cairn-hookfix-20261116` | `0f85f3e8` (the lock commit after C9) | tree under test |
| `cairn-hookfix-control-20261116` | `08c333c9` (the parent of C9's first commit `cb060551`) | control; its helper is C7's |
| `cairn-hookfix-controltest-20261116` | `08c333c9`, with `bootstrap/tests/security/test_git_read.py` from `cb060551` copied over it | control with C9's tests, for (a) |
| `cairn-hookfix-work-20261116` | none | tar copies, the scratch script and scratch hooks of (c) |

- Tar SHA-256: `0f85f3e8` `d422fd935f8d2caeb488a43016f8aa04939f84974d614379d9db31c79131b32d`;
  `08c333c9` `70d32395966018e10a549342c9bfe6da3de3f4dca26b65abbcf9a49383c4f58a`;
  C9's test file `40fcc491776e09c27508e6135b3ae556c454d3fa7eccb0d15f6b2ac81f2d7e06`
  (the same at `cb060551` and `0f85f3e8`, measured with `cmp`).
- Helper `tools/git_read.py` SHA-256 on the VM: tree under test
  `7782c8b003767db0f44e777121d74a7c563caf47629f8fbde645c5dbf371c898`; both controls
  `b9f04cc22ec889dd7835c5f985fb910843b02142e6270c252b46090cb634bfb2`. Each equals the
  `_GIT_READ_SHA256` pin in `bootstrap/_scaffold/lockfile.py` at its own commit.
  The helper is unchanged between `31f5351b` (C7) and `08c333c9`.
- Order: (a) and (d) ran first in each folder, before any `git init`, with
  `PYTHONDONTWRITEBYTECODE=1` set for the process so the trees stayed equal to
  the archives. (b) and (c) then ran in the tree under test and the control, in
  control first within each of (b) and (c). The third folder was used for (a) only.
- The test repositories hold 1021 of the 1022 files of the archive. The one not
  committed, `dev/reflections/2026-11-02-codex-93c2a217.md`, is on disk but a fresh
  repository ignores it (`.gitignore:9 dev/reflections/*`, measured with
  `git check-ignore -v`). It does not touch any step.

## (a) The `hook_index` tests

Command (each folder; the exit code was read with `call echo exit=%^errorlevel%`):

```sh
ssh cairn-windows 'cd /d C:\Users\cairn\<folder> && set "PYTHONDONTWRITEBYTECODE=1" && C:\ProgramData\miniconda3\envs\lhm\python.exe -m pytest -p no:cacheprovider -rfsE -v bootstrap/tests/security/test_git_read.py -k hook_index'
```

79 tests collected, 71 deselected, 8 selected: the three older `hook_index` tests
and T1 to T5.

| Test | Tree under test (`0f85f3e8`) | Third folder (control plus C9 tests) |
|---|---|---|
| `test_hook_index_uses_private_snapshot_and_closed_child_environment` | SKIPPED | SKIPPED |
| `test_hook_index_rejects_wrong_commands_paths_and_malformed_indexes` | PASSED | PASSED |
| `test_hook_index_source_drift_discards_read_result` | PASSED | PASSED |
| T1 `..._reads_staged_paths_through_the_real_windows_worker` | **PASSED** | **FAILED**: `AssertionError: worker-request-invalid` |
| T2 `..._completes_through_the_windows_route_on_any_os` | PASSED | FAILED: `AssertionError: worker-request-invalid` |
| T3 `test_the_worker_hook_index_branch_never_probes_the_git_version` | PASSED | FAILED: result reason `worker-run-failed` |
| T4 `test_the_worker_refuses_hook_index_requests_that_widen_or_unlock_the_read` | PASSED | PASSED (a guard; it passes before the change, as the plan said) |
| T5 `test_only_the_worker_hook_index_call_may_skip_the_version_probe` | PASSED | FAILED: `TypeError: _argv() got an unexpected keyword argument 'skip_version_probe'` |
| Totals, exit | **7 passed, 1 skipped, 0 failed**, 7.30 s, exit 0 | 4 failed, 3 passed, 1 skipped, 5.86 s, exit 1 |

- The one skip is the one the plan names:
  `test_git_read.py:662`, "real Git 2.45 or newer is required for hook index reads".
  It skips on Windows before and after C9 (the diagnosis, measurement 6). No other
  skip occurred.
- The tree under test was run twice. The first run gave the same results (7 passed,
  1 skipped, 9.84 s); its exit code was not captured. The table is the second run.
- T1 is the Windows-only test that skipped on macOS. It ran and passed on Windows
  in the tree under test, and failed first in the third folder with
  `worker-request-invalid`: that is the failing-first evidence the macOS run could
  not give. T2, T3 and T5 failed and T4 passed in the third folder, as the plan
  predicted from reading; this run measured it.
- Not run: the diagnosis's intermediate case (only C9's first edit applied, which
  the plan says fails T1 with `verified-helper-buffer-unavailable`). No folder here
  holds that variant.

## (b) The real hook

Setup in each folder, every Git command carrying `-c user.name=t -c
user.email=t@example.test` (the `-c` options are left out of the lines below):

```sh
git init -q
git add .
git commit -q -m base
python tools\intent.py install-precommit
echo c10 probe> c10-probe.txt
git add c10-probe.txt
git commit -m c10-probe
```

`python` is the interpreter above. Each exit code was read with `call echo
exit=%^errorlevel%`. The installed `.git\hooks\pre-commit` holds `#!/usr/bin/env
bash`, the single-quoted interpreter and `tools\intent.py _precommit_check`, then
the exit-code lines (measured with `type` on the control).

| Step | Control (`08c333c9`, run first) | Tree under test (`0f85f3e8`) |
|---|---|---|
| `git init`, `git add .`, `git commit -q -m base` | exit 0 each; 1021 files staged, 0 after; 1 commit | the same |
| `install-precommit` | exit 0; "installed pre-commit work-intent check at C:\Users\cairn\cairn-hookfix-control-20261116\.git\hooks\pre-commit." | exit 0; the same line with `cairn-hookfix-20261116` |
| `git add c10-probe.txt` | exit 0; `A  c10-probe.txt` | the same |
| `git commit -m c10-probe` | **exit 0**, output below | **exit 0**, output below |

Control output:

```text
intent: WARNING -- staged path discovery is unavailable; pre-commit coordination is unknown (allowing under existing policy).
[master 5991449] c10-probe
 1 file changed, 1 insertion(+)
 create mode 100644 c10-probe.txt
```

Tree under test output:

```text
intent: PRE-COMMIT CHECK -- UNKNOWN IDENTITY: cannot resolve this session's agent identity
  (CAIRN_AGENT unset, no harness session var, and ~/.cairn/agent.json missing or unreadable).
  Cannot verify whether you hold claims on the staged paths; any active-claim overlaps are shown below.
[master eb82669] c10-probe
 1 file changed, 1 insertion(+)
 create mode 100644 c10-probe.txt
```

**Pass.** The control reproduced the C8 warning, so the absence of that warning in
the tree under test means something. The `UNKNOWN IDENTITY` message is the one the
diagnosis saw once (measurement 5); the hook prints it only after it has read the
staged paths. That is the same inference the diagnosis made; (c) is the direct
evidence. The commits exit 0 in both trees because the hook only warns.

One discarded first attempt: the control's first run used `%errorlevel%`, which
`cmd` expands before the line runs, so its exit codes were not real. I deleted
the control's own `.git` and `c10-probe.txt` (inside my folder), then redid the
whole control with the exit-code form above. The output was the same. All
numbers here come from the redo.

## (c) The direct read inside a real pre-commit hook

In the tree under test and the control (not the third folder), after (b). Stage one
second new file, `c10-probe-direct.txt` (`c10-probe.txt` was committed in (b), so
exactly this one path is staged), then commit with a scratch hook given on the
command line only, which fails the commit on purpose and leaves the file staged:

```sh
echo c10 direct probe> c10-probe-direct.txt
git add c10-probe-direct.txt
git -c core.hooksPath=C:/Users/cairn/cairn-hookfix-work-20261116/hooks-<tree|control> -c user.name=t -c user.email=t@example.test commit -m c10-direct
```

- **The scratch hook** (`hooks-tree\pre-commit` and `hooks-control\pre-commit` in
  the work folder, LF endings) holds `#!/bin/sh`, one line
  `'C:\ProgramData\miniconda3\envs\lhm\python.exe' 'C:\Users\cairn\cairn-hookfix-work-20261116\c10-direct.py' '<folder under test>'`,
  then `exit 1`. Neither file nor the script was committed or put in any tree.
- **The scratch script** (`c10-direct.py` in the work folder, SHA-256
  `aa726834269da1e6d5c909382ea653af274e10dbefca9188e4a30a0b5e035a23`) loads
  `<folder>\tools\intent.py` with `importlib.util.spec_from_file_location` under the
  name `tools.intent`, puts the module in `sys.modules` before `exec_module`, takes
  `sys.modules["tools._intent.conflict"]._git_read()` (the pinned loader the hook
  uses) and, for each form in `sorted(helper._HOOK_INDEX_READS)`, prints the form
  and the `state`, `returncode`, `reason` and `stdout` of
  `helper.read_hook_index(os.getcwd(), form, index_file=os.environ.get("GIT_INDEX_FILE"))`.
  On any `BaseException` it would print the exception type and a traceback to the
  console only. No exception occurred, so there was no traceback to withhold.
- `git status --short` after each run showed `A  c10-probe-direct.txt` only: the
  failed commit left the file staged, and nothing else was added. The commit exit
  code was 1 in both folders, as designed.

| Tree | Form | state | returncode | reason | stdout |
|---|---|---|---|---|---|
| tree under test `0f85f3e8` | `('diff', '--cached', '--name-only', '-z')` | `completed` | 0 | `None` | `b'c10-probe-direct.txt\x00'` |
| tree under test `0f85f3e8` | `('diff', '--cached', '--name-status', '-M', '-z')` | `completed` | 0 | `None` | `b'A\x00c10-probe-direct.txt\x00'` |
| control `08c333c9` | `('diff', '--cached', '--name-only', '-z')` | `failed` | `None` | `worker-request-invalid` | `b''` |
| control `08c333c9` | `('diff', '--cached', '--name-status', '-M', '-z')` | `failed` | `None` | `worker-request-invalid` | `b''` |

**Pass, and this is the positive evidence.** The tree under test returns exactly
the outputs the plan states, for both forms; the control fails with the reason
the C8 record printed for its C7 tree. No third defect showed.

## (d) The two whole files

Command (the tree under test and the control; before any `git init`):

```sh
ssh cairn-windows 'cd /d C:\Users\cairn\<folder> && set "PYTHONDONTWRITEBYTECODE=1" && C:\ProgramData\miniconda3\envs\lhm\python.exe -m pytest -p no:cacheprovider -rfsE -v bootstrap/tests/security/test_git_read.py bootstrap/tests/security/test_git_read_routes.py'
```

| Folder | Passed | Failed | Skipped | Time | Exit |
|---|---|---|---|---|---|
| tree under test `0f85f3e8` | 88 | 1 | 19 | 123.55 s | 1 |
| control `08c333c9` | 83 | 1 | 19 | 120.99 s | 1 |

The single failure is the same test in both:
`test_git_read.py::test_read_origin_uses_git_parser_for_quoted_and_continued_values`,
the same assertion at the same line (1275), `'failed' == 'completed'`. It is the
order-dependent failure the C8 record already found in both trees, so it is not
C9's. The 19 skips in each folder are the POSIX-only and Windows-refusal skips,
including the one hook-index skip named in (a); the count is the same in both
folders, so none is new. The five more passes in
the tree under test are T1 to T5. `test_git_read_routes.py` had no failure in
either folder.

## Not run

- No whole-suite run (forbidden), and no test file beyond the two named above.
- The pin test (`test_every_tool_pins_the_digest_of_the_helper_it_runs`) ran inside
  the whole-file run of (d) and passed in both folders; I did not run the four
  named fail-closed controls separately by `-k`.
- One Windows host, one Git version, the x64 interpreter only.
- `python scripts/claim_check.py` and `python scripts/link_check.py` over this file
  ran on the macOS checkout (see the commit).

## Left on the VM

Under `C:\Users\cairn\`, all new, all deletable by the Maintainer:
`cairn-hookfix-20261116` and `cairn-hookfix-control-20261116` (each now a Git
repository with the hook installed, two commits and one staged probe file),
`cairn-hookfix-controltest-20261116` (no `.git`), and `cairn-hookfix-work-20261116`
(the two tar copies, C9's test file, `c10-direct.py` and the two scratch hook
folders). pytest's own temporary folders under `%TEMP%` were written by the test
runs as usual and not touched. Nothing else was created or removed.

**Elapsed:** about 15 minutes on the VM (15:44 to about 15:55 EST), after about 5
minutes reading the plan and records; estimates.
**Tokens:** unknown.
