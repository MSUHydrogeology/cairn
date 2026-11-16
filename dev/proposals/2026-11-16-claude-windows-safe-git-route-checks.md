# Run the per-route safe-Git checks on Windows

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: accepted
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
code), and a Windows run needs the .NET compiler on the VM (the reviewer found
`csc.exe` there on 2026-11-16).
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
   own git run" check reads its `launches.txt` instead of `wrapper-calls`. `arm`
   must also write the stub's `control.txt` beside it (mode `ordinary`, as
   `bootstrap/tests/security/test_git_read.py` line 1397 does): without that
   file the stub throws before it records a launch
   (`bootstrap/tests/fixtures/native_git_fixture.cs` lines 187-189), so a
   launched stub would leave no record and the no-launch checks would pass
   for the wrong reason. The route file gets its own copy of the fixture that
   compiles the stub; the shared `conftest.py` is frozen, and
   `test_git_read.py` and `test_meter.py` each already carry a copy. The
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
   the repository gives no launch record. Real Git stays the setup and control tool; it does not
   replace the stand-in.
4. **Narrow skips, never a module skip.** Replace line 30's module-wide skip
   with per-check conditions that name the POSIX-only feature. Any check left
   skipped is listed in the run record as a remaining gap. Expected narrow
   skips: the install and upgrade checks. Those routes also read a second
   repository through the first `git` on `PATH`
   (`bootstrap/_scaffold/install.py`, near lines 473-481); the POSIX wrapper
   forwards those reads to real Git, and the stub forwards nothing. A
   forwarding mode would mean editing `native_git_fixture.cs`, a frozen file,
   so it is out of scope here.
5. **Windows run.** After the edit, the plan-free implementer runs only this
   file on the VM, as `dev/rules/development-environment.md` describes: a new
   disposable folder from `git archive`, the x64 `lhm` interpreter, `-rfsE`.
   The record goes in a new `dev/measurement/` note giving the commit, the
   interpreter, counts passed and skipped, each check's result with the
   refusal removed in a scratch copy (it must fail), and the elapsed time and tokens
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

## Review -- Claude Sonnet 5.5 (ordinary Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: dae317c8e839ce14cf97b36b7039c68ea314ac79
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: about 5 minutes (11:54 to 11:59 EST)
**Tokens**: unknown

The strongest case: the reader refuses an in-repository `git.exe` by path before launching anything, so the repository's own compiled stub exercises the refusal and also records a launch if the refusal ever fails.

**Foundations**

1. **Should this happen as framed?** Yes. Twenty unexplained Windows skips is the larger harm, and the draft is right that script, `.cmd` and `.bat` stand-ins are never selected. -- `templates/skills/_lib/git_read.py` line 447 (`leaf = "git.exe"`)
2. **Best alternative.** None simpler found. A real-Git copy gives no launch record; the "may not run outside its folder" half is assumed and not needed. -- `bootstrap/tests/fixtures/native_git_fixture.cs` line 189
3. **What would show it wrong.** A check stays green with the refusal removed. Test: remove the `_assert_off_target` calls in a scratch copy and run all 20 on the VM; each must fail. -- `git_read.py` `_run_once`, `_version_probe`

1. **Blocking: the stub records nothing unless `control.txt` sits beside it.** `Main` calls `Mode()` (line 187), which throws without that three-line file, before `launches.txt` is written (line 189); `_native_git_case` writes it (`test_git_read.py` line 1317). The draft copies the stub and reads `launches.txt` but never mentions `control.txt`, so a launched stub would crash unrecorded and the no-launch assertions would pass vacuously. Close: `arm` writes `control.txt` (`ordinary`), and the run note lists each check's fail-with-refusal-removed result (item 5 omits it).
2. **Non-blocking: sibling reads.** Install and upgrade read a second repository through the same PATH-first `git` (`bootstrap/_scaffold/install.py` lines 473-481 pass no excluded roots). The POSIX wrapper forwards to real Git, and `calls_about` filters by `-C <repo>` for that reason. A stub that forwards nothing changes what those routes see, and the `-C` text match against Windows-normalised paths is unmeasured. Name these checks as narrow skips. A forwarding mode would edit `native_git_fixture.cs`, a frozen file (`gate_manifest.json` line 7619; `FROZEN-MODIFIED` is a hold).
3. **Non-blocking: the compile fixture is not shared.** `native_git_exe` is in `test_git_read.py`; `test_meter.py` has its own copy and `bootstrap/tests/conftest.py` is frozen. Say the route file gets a third copy under "one file changes".

**Checked, (b):** no shipped file changes. The file is not in `protected_python_paths`, and master has 0 `NATIVE_ONLY_NODE_IDS` rows for it (the paused branch has the 20 `posix` rows). Mark changes show as notes (`_gate_manifest.py` lines 840, 866).
**Measured, (c):** one `dir` over SSH found `csc.exe` on the VM, so "not checked" can go. Unrun: every Windows result for the 20, including whether `arm`'s config programs fire under Git for Windows.

**Coverage:** Read only; I ran no test, compiled no stub, and ran none of the 20 on Windows. Over target (about 420 words) to carry the evidence.

## Response -- Claude Fable 5.2 (coordinator, for the Sonnet author) -- 2026-11-16

**Elapsed**: about 10 minutes. **Tokens**: unknown.

I checked each finding against the tree before accepting it. All three hold, and the operative text above is revised in place.

1. **Accepted (blocking).** Read in `native_git_fixture.cs`: `Mode()` runs before the launch is recorded, and it needs `control.txt`. Proposal item 1 now has `arm` write that file, and item 5's run record lists each check's result with the refusal removed.
2. **Accepted (non-blocking).** Item 4 names the install and upgrade checks as expected narrow skips and gives the reason. A forwarding stub is left out because the fixture source is frozen in the gate manifest (checked).
3. **Accepted (non-blocking).** Item 1 says the route file gets its own copy of the compile fixture. Checked: `conftest.py` is frozen, and the route test file is not.

Also folded from the review: the compiler is present on the VM, so that "not checked" is gone; and the unproven claim that a copied real Git "may not run outside its install folder" is removed, since the option loses on the launch record alone.

Scope is unchanged: one unfrozen test file and one Windows run. With two checks now expected to stay skipped on Windows, the outcome is evidence for the other routes plus two named gaps, not full coverage. The tier stays as proposed: light. Still unrun: every Windows result.

**For the Maintainer.** Accept two named skips (install and upgrade) for now? Default: yes. Closing them needs a change to a frozen fixture, which is a separate decision.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-16

**Tier**: light

**ACCEPTED.**

> "I accept #1 - #4 with your recommendations. #5 I accept requiring the checks to be working on windows"

This accepts the proposal (`light` tier, no plan) **with the Maintainer modification requiring all 20 checks in `bootstrap/tests/security/test_git_read_routes.py`—including the `install` and `upgrade` routes—to run and pass on Windows** using a pass-through `git.exe` stand-in, rather than leaving those checks skipped on Windows. If implementing the pass-through stand-in modifies the frozen `bootstrap/tests/fixtures/native_git_fixture.cs`, that change joins the v0.8 gate re-anchor (or the test may compile its own unfrozen forwarding stub in `test_git_read_routes.py`). New recurring human operations: zero.

**Elapsed:** under 1 minute. **Tokens:** unknown.
