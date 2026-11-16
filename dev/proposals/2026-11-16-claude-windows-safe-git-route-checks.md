# Run the per-route safe-Git checks on Windows

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
**Review**: usual
**Proposed tier**: light -- one ordinary test file changes and no shipped code does; the Maintainer sets the tier
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-16
**In brief**: Cairn's checks that each tool refuses a hostile `git` hidden inside a repository never run on Windows, so this swaps in a Windows-runnable stand-in and runs them on the Windows VM.

## Decision summary

Twenty checks in `bootstrap/tests/security/test_git_read_routes.py` skip on
Windows. Each one hides a fake `git` inside a repository and shows that a tool
(scan runner, prose report, link check, sweep, intent commands, meter, install,
upgrade) refuses it instead of running it. Today the only Windows evidence is
for the shared Git reader (`tools/git_read.py`) itself, not for these callers.

I propose giving those checks a small compiled `git.exe` stand-in on Windows,
reusing one the repository already has, then running the file once on the
Windows VM and recording the result. Cost: one test file changes (no shipped
code), and a Windows run needs the .NET compiler on the VM (not checked).
Where a check cannot fit Windows, it gets a narrow skip that says why, so a
remaining gap is named rather than hidden.

## Context

Measured in the current tree:

* The file defines 11 test functions that expand to 20 checks (the 20 node IDs
  are listed in `bootstrap/tests/fixtures/gate_manifest.json`, lines 842-861).
* Line 30 skips the whole module when `os.name == "nt"`. The reason given is
  that the stand-in is an extensionless script. `Lab.arm` (lines 136-142) writes
  `hostile-bin/git` as `#!/bin/sh` and calls `chmod(0o755)`. The sweep check
  (line 361) writes a second shell stand-in, for `gitleaks`.
* On Windows the reader looks for exactly `git.exe` on `PATH`
  (`tools/git_read.py` line 447; `test_git_read.py` line 52 does the same). So
  a `.py`, `.cmd` or `.bat` file named `git` is never even selected: the
  reader would report no Git, and a "refused" result would be for the wrong
  reason.
* `dev/measurement/windows-native-rerun-2026-11-13.md` ran `test_git_read.py`
  and other files, never this one (it does not name it); the board row says the
  reruns did not cover these routes.
* `test_git_read.py` already builds a compiled stand-in
  (`bootstrap/tests/fixtures/native_git_fixture.cs`, compiled by the .NET
  `csc.exe` named at line 1293 as `native_git_exe`). It prints a fixed
  `git version 2.53.0` and appends each call to `launches.txt` beside itself.
* `tools/git_read.py` and `templates/skills/_lib/git_read.py` are
  byte-identical (checked with `cmp`).

Not checked: whether the 20 checks would pass on Windows beyond the stand-in
(for example the hard-coded `/usr/bin` and `/bin` `PATH` entries, or the
`.git` `chmod`); that is what the run shows.

## Proposal

1. **Stand-in form: the compiled `git.exe`.** On Windows, `Lab.arm` copies the
   existing compiled stub to `hostile-bin\git.exe` and the "did the repository's
   own git run" check reads its `launches.txt` instead of `wrapper-calls`. The
   `gitleaks` stand-in gets the same treatment, or that one leg takes a narrow
   skip. Real Git is still used for setup and for the "plain Git does run the
   hostile config" control, as today.
2. **Why not the others.** A Python launcher or a `.cmd`/`.bat` shim cannot
   imitate how this reader finds and starts Git: it matches only `git.exe`, and
   Windows starts a program through its executable format, not a `#!` line. A
   script would need a `.exe` wrapper anyway. A compiled stub cannot imitate
   Git's real behavior (it forwards nothing, and always reports 2.53.0), but
   these checks only need "was it launched, and was it refused".
3. **Real Git instead (the row's other option).** Copying real `git.exe` into
   the repository gives no launch record, and the copy may not run outside its
   install folder. Real Git stays the setup and control tool; it does not
   replace the stand-in.
4. **Narrow skips, never a module skip.** Replace line 30's module-wide skip
   with per-check conditions that name the POSIX-only feature. Any check left
   skipped is listed in the run record as a remaining gap.
5. **Windows run.** After the edit, the plan-free implementer runs only this
   file on the VM, as `dev/rules/development-environment.md` describes: a new
   disposable folder from `git archive`, the x64 `lhm` interpreter, `-rfsE`.
   The record goes in a new `dev/measurement/` note giving the commit, the
   interpreter, counts passed and skipped, and the elapsed time and tokens
   (`unknown` if unavailable). The author of this proposal did not connect to
   the VM.

## Rationale

The routes are the callers a user actually runs; the reader's own Windows
controls do not show that each caller refuses a hostile `git`. Windows is an
equal partner (Maintainer, 2026-11-10). Reusing the existing stub adds no new
compiler step and keeps the .NET dependency already pinned at one place.

## Alternatives considered

Do nothing: the gap stays, and a strict Windows release record would have to
carry 20 unexplained skips. Script stand-ins and real-Git-only: see Proposal
items 2 and 3.

## Documentation / doctrine surface

Descriptive layer only: the new measurement note. Dev-layer line: the board
row closes. No `AGENTS.md`, methodology or shipped-template change.

## Evidence / verification plan

### Tests required

Promise: each route refuses a `git` found inside the repository and runs none
of the repository's config programs, on Windows as on POSIX. Public entry: the
20 existing checks in this file. Run only this file, on macOS and on the
Windows VM; no whole-suite run (`python tools/test_tiers.py for <path>` lists
the selection). Fault that would show the change wrong: a route that executes
the stub and the check still passing. The implementer must confirm each check
fails when the refusal is removed or the stub is made selectable and clean.

**Lane and roster.** The file is not on the protected roster
(`bootstrap/tests/fixtures/protected_test_roster.json` does not name it) and is
not in `SECURITY_FAMILY` in `bootstrap/tests/security_manifest.py`. It is an
"ordinary test file" pinned by hash in the gate manifest; a change shows as a
report-only `UNPROTECTED-CHANGED` note (`bootstrap/tests/_gate_manifest.py`
lines 840-842), not a hold. Refreshing that pin is a Maintainer re-anchor and
is not part of this change.

**Paused roster refresh (not reopened).** The local branch
`prep/windows-roster-refresh` lists these 20 nodes as POSIX-only. If this
change lands first, the revived refresh must drop those 20 rows (any that stay
skipped keep a row); until then a strict Windows record would count the 20 as
unexplained skips. I read the branch's diff; I did not edit it.

### Examples / smoke checks

`python scripts/claim_check.py` on this file.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A route check passes on Windows only because the repository's `git` was never
selected (wrong stand-in name or location); or the compiler is missing on the
VM, so the checks error rather than run.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: standard -- test-only; no scaffold, install contract,
binding or sweep trust root changes. Uncertain: the file defends a trust
boundary, so the reviewer may raise it.
