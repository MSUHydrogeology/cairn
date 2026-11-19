# Windows run of the safe-Git route checks, 2026-11-16

Evidence for the accepted proposal
`dev/proposals/2026-11-16-claude-windows-safe-git-route-checks.md`. It records
one native Windows run of `bootstrap/tests/security/test_git_read_routes.py`
and the checks that show those results are not empty. It is not a release
record.

## Result

All 20 checks ran and passed on Windows. None was skipped. The two Windows-only
changes to the file are a compiled `git.exe` stand-in and a scratch folder for
the meter check. The macOS result is unchanged (20 passed).

| Where | Interpreter | Passed | Failed | Skipped | Time |
|---|---|---|---|---|---|
| Windows VM, exact commit `6079e89e` | x64 Python 3.13.18 (`lhm`), pytest 9.2.0 | 20 | 0 | 0 | 72.94 s |
| Windows VM, earlier folder, same file bytes | same | 20 | 0 | 0 | 78.80 s |
| macOS | Python 3.13.13, pytest 9.0.3 | 20 | 0 | 0 | 31.01 s |

Measured, not assumed: the counts come from the pytest summary lines of the
runs above. Not measured: elapsed human time and tokens (`unknown`).

## What was run

- **Host.** Windows 11 ARM64 (build 10.0.26300) in UTM, SSH alias
  `cairn-windows`; the x64 (emulated) `lhm` interpreter
  `C:\ProgramData\miniconda3\envs\lhm\python.exe`; Git for Windows
  2.56.0.windows.4; the .NET Framework 4 compiler
  `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe`.
- **Folder.** A new folder, `C:\Users\cairn\cairn-winroutes-final-20261116`,
  unpacked from `git archive --format=tar 6079e89e` (no `.git` inside, nothing
  uncommitted). Nothing existing was overwritten and no system setting or
  package was changed.
- **Command.**

  ```sh
  ssh cairn-windows 'cd /d C:\Users\cairn\cairn-winroutes-final-20261116 && C:\ProgramData\miniconda3\envs\lhm\python.exe -m pytest -p no:cacheprovider -rfsE -v bootstrap/tests/security/test_git_read_routes.py'
  ```

- **Commits.** `bc590648` (the compiled stand-in; 18 checks passed on Windows
  from it) and `6079e89e` (the meter folder fix). The file's SHA-256 is
  `04de0b98e78f09e44fce2ce2011f27eb823f2af140f16d98153d3ce085c41dd0` at both the
  commit and the VM copy.
- **Frozen files.** `bootstrap/tests/fixtures/native_git_fixture.cs` was not
  edited. The route file compiles its own forwarding stand-in, so nothing joins
  the Maintainer's re-anchor.

## How the stand-in works

On Windows the reader selects only `git.exe`, and Windows starts a program by
its file format, so the POSIX `#!/bin/sh` wrapper cannot be used. The route file
now compiles one small program (C# 5, the compiler on the VM). Each copy reads a
sidecar file named like itself with a `.stub` extension:

- `forward` (the `git.exe` in `hostile-bin`): append the argument text to the
  call log, then run the real Git with the same arguments, standard streams and
  exit code. The forwarding is what lets the install and upgrade checks read a
  second repository through the same first `git` on `PATH`, as the POSIX wrapper
  does. That is the Maintainer's modification: those two routes run on Windows
  and are not skipped.
- `record` (the sweep's `gitleaks.exe`): append one line to a file and exit 0.

The call log is written before anything that can fail, and `arm()` now launches
the stand-in once and requires a launch record and Git's own `git version`
answer. If the stand-in ever stopped recording, `arm()` fails; it cannot turn
into a quiet pass.

## What changed on the way

The first Windows run (stopped at the first failure) passed 18 checks and failed
both meter checks. The safe leg returned `project_remote_unavailable`. Cause,
measured: the meter's project `.git/config` read walks every parent folder and
refuses one with an explicit non-owner entry, and pytest's own temp folders
carry one (`OWNER RIGHTS` full control; see
`dev/rules/development-environment.md`). The check now builds its repository
under a default-mode folder in `%TEMP%` on Windows (`tmp_path` elsewhere) and
removes it afterwards. The `OWNER RIGHTS` entry is the likely cause; I did not
isolate it.

## The checks are not empty

Three scratch-tree changes, each run on the whole file on both machines. The
scratch trees were `git archive` copies, never the repository. Every mutated
run also printed, after each route run, whether the stand-in left a launch
record and how many calls named the armed repository (`-C <repo>`), so the
first failing assertion cannot hide it.

- **M1, stand-in made selectable and clean.** `hostile-bin` is moved outside the
  repository, so the route may select and launch it.
- **M2, refusal removed.** The helper's `_assert_off_target` returns at once;
  the sweep's and the content-scan runner's own containment tests are removed
  too; every pin of a changed file is renewed until stable.
- **M3, offline guards removed** (for the one check that has no stand-in): the
  helper's lazy-fetch and protocol guards are switched off, pins renewed.

| Run | Windows | macOS |
|---|---|---|
| M1 | 19 failed, 1 passed (92.34 s) | 19 failed, 1 passed |
| M2 | 19 failed, 1 passed (95.32 s) | 19 failed, 1 passed |
| M3 | `test_upgrade_to_a_ref...` fails: "a program the repository's config names ran" | same |

The one check that passes under M1 and M2 is
`test_upgrade_to_a_ref_never_fetches_a_missing_object_through_a_source_program`.
It uses no stand-in; its guard is the offline settings, which M3 removes, and
it fails under M3 on both machines. (In M3 two exact-replacer checks also fail,
for a stale pin in my scratch tree, not for a launch; I do not count them.)

Under M1 and M2 every one of the other 19 checks fails and the hostile run left
a launch record:

| Route (checks) | Calls recorded about the armed repository |
|---|---|
| content-scan runner (2) | 2 each |
| prose report (2) | 9 each |
| exact replacer (2) | 4 each |
| link check and snippet check (4) | 1 each |
| portable sweep (2) | 2 each |
| intent commands (2) | 1 each |
| install (2) | 5 (Cairn source), 4 (target) |
| upgrade plan (1) | 1 (Cairn source) |
| meter (2) | the record exists and the route returned the remote (traced under M1 on both machines) |

The counts above are from the Windows runs; the macOS runs gave the same counts.
So the Windows path spelling in the call log matched the repository path on
every route. Where an earlier assertion failed first (for example a return
code), the trace still shows the stand-in was launched and recorded.

## What was not run

- No whole-suite run (forbidden), and no other test file on the VM.
- Only the x64 (emulated) Python on the ARM64 VM; no native ARM64 run and no
  physical Windows machine.
- One Windows host with one Git version; older Git was not tried.
- The `claim_check.py` result for this note and the proposal is in the
  proposal's verification section.

## Caveats

- The M1 and M2 scratch trees, the trace lines and the mutation script are not
  committed. They can be rebuilt from the descriptions above.
- The 20 node IDs and the file's hash in `gate_manifest.json` were not touched;
  the file's hash changed, so the report-only `UNPROTECTED-CHANGED` note appears
  until the Maintainer's re-anchor. The paused `prep/windows-roster-refresh`
  branch should drop its 20 POSIX-only rows for this file.
