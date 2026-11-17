# Finish the release-route documentation: a verify step in the installer's list, and a tested Windows route

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: light, because it is one printed line plus documentation and adds no behavior; the Maintainer sets the tier
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-16
**In brief**: The installer's closing checklist would tell you to run the integrity check before editing anything, and Windows adopters would get an install route that has actually been run on Windows.

## Decision summary

Two small gaps remain from the 0.7 release-route documentation repair. First, after an install the scaffold prints a "Next steps" list that never mentions `verify_integrity.py`, so a person who follows only that list edits files before the check can still tell their edits from tampering. Second, the two release routes (ordinary and signature-verified) are written for a POSIX shell, and `bootstrap/PROVENANCE.md` says PowerShell equivalents are "not yet documented". Windows adopters use Git Bash, but nobody has run the commands there beyond checking that `sh`, `mktemp` and `awk` exist.

Proposed: add one line to the printed list, and make Git Bash the documented, tested Windows route rather than writing PowerShell versions. The cost is one engine-file line (so a Security Review pass) and a Windows test run by the plan's implementer.

## Context

Measured in the current tree:

- `print_report` in `bootstrap/_scaffold/install.py` ends (lines 2000-2004) with "Next steps for a real adoption (BOOTSTRAP.md Act II):" and items 3 to 6. The numbers match the Act II steps (3 is II-3, 4 is II-4), so nothing is printed for II-2.
- `bootstrap/BOOTSTRAP.md` II-2 ("Official-release route: verify before you edit anything") says to run `python bootstrap/verify_integrity.py --target <path/to/target/repo>` right after the scaffold, before filling a slot or renaming `VENDOR.md`. `bootstrap/PROVENANCE.md` ("Record the selection in the target repository") says the same. The check keeps only a hash of each file, so it cannot tell your edit from tampering.
- `bootstrap/PROVENANCE.md` lines 98-100 say the commands suit a POSIX shell and that PowerShell equivalents are not documented. The ordinary route uses `curl`, `mktemp`, `/dev/null`, `test` and Git; the stronger route's block (lines about 349-461) adds `awk` and `ssh-keygen`. `bootstrap/tests/test_verify_ref.py` extracts and runs that block, on macOS only as far as I read; I did not check whether it runs on Windows.
- `docs/quickstart.md` already has PowerShell steps for the try-it shakedown, and says the Windows commands are new. The release routes have none.

Not checked: any command on Windows (the VM was not touched), and whether `/dev/null` as a `GIT_CONFIG_GLOBAL` value works under Git for Windows.

## Proposal

1. **Installer line.** In `print_report`, print one unnumbered line above item 3, such as: "Before you edit any file (official-release route): run `python bootstrap/verify_integrity.py --target <target>` from the verified checkout (II-2). Skip it if the install ends with `cairn-lock.yml NOT written`, and follow that message's remedy first." It is unnumbered so that the five places that say the installer prints "four steps" (`docs/quickstart.md`, `on-ramp/README.md`, `docs/solo-legacy-recipe.md`, `docs/index.html` and its figure) and the installer's own "shakedown skips 3-5" line stay true. It cannot refer to "the report above": `print_report` runs (`bootstrap/_scaffold/cli.py` line 665) before the lockfile is written (line 804), and the not-written warning prints afterwards. "From the verified checkout" is II-2's own wording and carries its limit: a pass ties the files to what the scaffold wrote, not to the release. The line prints a command and runs nothing.
2. **Windows route: Git Bash, tested.** Document Git Bash (shipped with Git for Windows) as the supported Windows shell for both routes, with a one-paragraph note on how to open it and which tools it supplies. The note says to start Git Bash from its Start-menu entry or by the full path to its `bash.exe`, not by a bare `bash`: on the VM no `bash`, `sh`, `awk` or `mktemp` is on the login `PATH`, and `ssh-keygen` there resolves to Windows' own copy (both reviewers looked; no route command was run). The plan's implementer runs both routes in Git Bash on the Windows VM described in `dev/rules/development-environment.md` (I did not connect), fixes any command that fails there in the shared text, and records the run, including the output of `command -v sh awk mktemp ssh-keygen git python`. Only if the run passes is the "PowerShell equivalents are not yet documented" sentence in `PROVENANCE.md` replaced by what was tested, with its date; otherwise it stays. If a fix would need `bootstrap/tests/test_verify_ref.py` to change, the implementer stops and reports: that file is frozen in the gate manifest, so changing it needs the Maintainer's gate re-anchor.
3. **Order against the layout.** This work is board group 1 and lands before the accepted repository layout (`dev/proposals/2026-11-09-claude-repository-layout.md`, which renames `bootstrap/` to `install/`). The layout plan must carry over: the printed path `bootstrap/verify_integrity.py` and its test, every command path in the Git Bash text (`bootstrap/container/verify-ref.sh`, `bootstrap/scaffold.py`), and the Windows run record, which becomes the layout's baseline for re-running the routes after the move.

Windows is an equal partner with macOS and Linux (Maintainer, 2026-11-10, on the board).

## Rationale

The verify line closes the gap where the printed list and the document disagree, at the moment an agent decides what to do next. A tested Git Bash route gives Windows adopters evidence now. The stronger route is a trust-root procedure; Windows evidence for it is worth more than a second, differently-bugged copy.

## Alternatives considered

- **PowerShell versions of both routes.** Matches the quickstart, but the stronger route's 70-line block is extracted and tested as one text; a PowerShell port needs its own tests, a second copy to keep in step, and redirect and Git-isolation behavior I have not checked. It lost on continuing burden. Revisit if Git Bash proves unusable on the VM, or on an adopter request.
- **Doing nothing.** Leaves a documented stop-and-check that the printed list lets people skip, and an untested Windows claim.

## Documentation / doctrine surface

Routes by layer: the installer line is engine code (`bootstrap/_scaffold/install.py`); the Windows route lands in `bootstrap/PROVENANCE.md` (and the one sentence in `bootstrap/BOOTSTRAP.md` II-2 only if the plan finds it needs a pointer); a short `CHANGELOG.md` Unreleased entry says what an adopter would notice.

## Evidence / verification plan

### Tests required

- The installer line is a caller-visible output. No test I found pins the "Next steps" text (a search of `bootstrap/tests` for the phrases found none). `bootstrap/tests/test_install_report_slots.py` runs `print_report`; the plan adds one promise there, that the report names `verify_integrity.py` before the slot step. `python tools/test_tiers.py for bootstrap/_scaffold/install.py` lists 36 test files; I did not run them and the plan runs only those that name the changed file.
- Windows: the implementer runs both routes' commands in Git Bash on the VM and records the interpreter, Git version and outcome. A failure there falsifies "tested Git Bash route".

### Security preflight

N/A: the installer line prints text and the Windows work is documentation; both go through the Security Review pass named in the header.

### Independent scientific check

N/A: no scientific content.

## Signals the change is wrong

A route command fails under Git Bash and no shared fix exists, or the printed line appears when no lockfile was written and sends a person to a check that cannot pass.

## Scope delta

N/A: baseline as opened.

## Assurance path

**Assurance path**: high-assurance

It touches the scaffold engine and the release trust-root documentation. An engine edit also leaves the AST baseline mismatched until the Maintainer's separate release baseline operation (`dev/rules/protected-surfaces.md`).

## Review -- Claude Sonnet 5.5 (ordinary Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: dae317c8e839ce14cf97b36b7039c68ea314ac79
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 4 minutes (11:54 to 11:58 EST)
**Tokens**: unknown

The strongest case: a person who follows only the installer's list should run the pre-edit check, and Windows adopters should get a route that was actually run.

**Foundations**

1. **Should this happen as framed?** Yes, once the wording is fixed. The order (verify before any slot or rename) agrees with the committed docs, and no test or second copy pins the printed text. -- `bootstrap/BOOTSTRAP.md` II-2 ("verify before you edit anything"); `bootstrap/PROVENANCE.md` "Record the selection"; `git grep "Next steps for a real adoption"` hits only `install.py:2000`
2. **Best alternative.** Print the line unnumbered, above item 3, rather than as item 2. -- finding 2
3. **What would show it wrong.** A fresh Windows run in Git Bash fails at a route command with no shared fix; or a fresh install prints the line and the lockfile write is then refused. -- `bootstrap/_scaffold/cli.py:665` and `:804`

1. **Blocking.** Item 1 says to skip "if the report above says the lockfile was NOT written". `print_report` runs at `cli.py:665`, before the lockfile write at `cli.py:804`; the warning prints afterward, on stderr, and `print_report` takes no lockfile argument. Say "if the install ends with `cairn-lock.yml NOT written`", unconditionally, or admit the conditional form moves the call (more than one line). Closes with: corrected wording.
2. **Non-blocking.** "One printed line" is not all. Five places say the installer prints "four steps" (`docs/quickstart.md:572`, `on-ramp/README.md:30`, `docs/solo-legacy-recipe.md:60`, `docs/index.html:274`, the SVG), and `install.py:2006` says the shakedown "skips 3-5". An unnumbered lead-in leaves all true. Also say it is for the official-release route, as II-2 does.
3. **Non-blocking.** I listed Git's `usr\bin` on the VM (read-only): `sh`, `awk`, `mktemp`, `ssh-keygen` are present, but none of `sh`, `bash`, `awk`, `mktemp` is on the SSH login `PATH`. The implementer must start Git Bash explicitly. No route command was run by me. If a fix needs the frozen `test_verify_ref.py` to change, that is a gate re-anchor; fence it in the plan.

Frozen check: `install.py` is not in `gate_manifest.json` `frozen_files` (only top-level `bootstrap/*.py`); the draft's cost, the AST baseline only, is correct (`print_report` is outside the self-service allowlist).

**Audience / rule loss:** No rule weakens. The sentence "PowerShell equivalents are not yet documented" must stay unless the Windows run passes; state that in item 2.

**Coverage:** Not run: any Windows command, any test beyond `test_ast_attest.py` (29 passed; it will fail after the edit until the Maintainer corrects the baseline). Did not read the 70-line block line by line or any issue (the draft cites none). Over the 300-word target to keep each finding's evidence. Security Review is separate and not cleared.

## Security Review -- Claude Opus (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 04921fc918bfe27535c8d2aecb1c6e6f39645ae0
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: ACCEPT
**Elapsed**: about 6 minutes (11:58 to 12:05 EST)
**Tokens**: unknown

Obligation: confirm the new step and the Git Bash route run nothing from the fetched tree before an adopter-chosen route verifies it, and claim no more than they prove.

The strongest case: the printed list should match II-2, and Windows adopters deserve a route someone ran.

**Foundations**

1. **Should this happen as framed?** Yes. The step adds no new trust: `verify_integrity.py` runs from the same checkout whose `scaffold.py` the adopter already ran after choosing a route, and the docs already say a pass ties files only to what the scaffold wrote, not to the release. -- `bootstrap/PROVENANCE.md` "Choosing an adopter verification route" ("before running candidate code") and "Record the selection" ("the checkout checks above are what tie them to the release"); `bootstrap/BOOTSTRAP.md` II-2 "from the verified checkout"
2. **Best alternative.** Word the printed line "from the verified checkout", as II-2 does, so it carries the same limit. -- `bootstrap/BOOTSTRAP.md:340`
3. **What would show it wrong.** A route step that runs a Cairn file before the checkout checks finish, or Git Bash resolving a route tool from outside Git's own folders. -- `bootstrap/PROVENANCE.md:89`, finding 1

Trust-on-first-use (a verifier shipped inside the tree it checks) is not a new threat here: an attacker who controls the fetched tree already controls `scaffold.py` and the printed list, and the stronger route never executes the tree (`PROVENANCE.md:268-271`). A planted file in the current folder does not win in bash, which does not search the current folder; an earlier PATH entry needs write access to the adopter's own account, outside Cairn's model.

1. **Non-blocking.** The Git Bash note should say to open Git Bash from its Start-menu entry or `C:\Program Files\Git\bin\bash.exe`, not a bare `bash`. Measured on the VM over SSH (`where bash`, `where ssh-keygen`): no `bash` on PATH, and `ssh-keygen` resolves to `C:\Windows\System32\OpenSSH\ssh-keygen.exe`, so tool choice depends on starting the right shell. Closes with: that sentence, plus `command -v sh awk mktemp ssh-keygen git python` in the recorded run.

(c) The `install.py` line prints text only; the draft's AST-baseline cost is stated correctly.

**Coverage:** Not covered: any route command on Windows, the 70-line block line by line, any test. The Git Bash PATH order (`/mingw64/bin`, `/usr/bin` first) is from Git for Windows' known profile, not measured. Ordinary review's REVISE findings stand; this ACCEPT is the security question only.

## Response -- Claude Fable 5.2 (coordinator, for the Sonnet author) -- 2026-11-16

**Elapsed**: about 10 minutes. **Tokens**: unknown.

Both reviews are answered here. I checked each code claim against the tree before accepting it. The operative text above is revised in place.

Ordinary review (REVISE):

1. **Accepted (blocking).** Confirmed in `cli.py`: the report prints before the lockfile is written. Item 1's wording no longer refers to "the report above"; it names the message the install ends with.
2. **Accepted (non-blocking).** The line is now unnumbered and says it is for the official-release route, so the "four steps" statements stay true. I confirmed three of the five places and the "skips 3-5" line; I did not open `docs/index.html` or the figure.
3. **Accepted (non-blocking).** Item 2 says how to start Git Bash and adds the stop for the frozen test file (checked: `test_verify_ref.py` is in the gate manifest's frozen files; `install.py` is not).

Security Review (ACCEPT on the security question):

1. **Accepted (non-blocking).** Item 2 names the Start-menu entry or the full path, and the recorded run includes the `command -v` line. Item 1 also takes the reviewer's "from the verified checkout" wording.

Also folded: the PowerShell sentence stays unless the Windows run passes. Scope and proposed tier are unchanged (light, with the Security Review now held). Still unrun: every route command on Windows.

**For the Maintainer.** Git Bash, not PowerShell, as the tested Windows route? Default: yes.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-16

**Tier**: light

**ACCEPTED.**

> "I accept #1 - #4 with your recommendations. #5 I accept requiring the checks to be working on windows"

This accepts the proposal as revised (`light` tier, with the completed Security Review held; no plan), adding the unnumbered `verify_integrity.py` line to `print_report` and adopting Git Bash (tested on `cairn-windows`) as the documented Windows route in `bootstrap/PROVENANCE.md`. Touches the `install.py` AST baseline for the v0.8 release baseline update. New recurring human operations: zero.

**Elapsed:** under 1 minute. **Tokens:** unknown.

## Implementation verification -- Claude Sonnet 5.5 (Implementer, Medium) -- 2026-11-16

**Commits**: `449fecc6` (installer line in `print_report`, four lines of text, unnumbered, above item 3, wording as revised); `8512e134` (Git Bash note and dated sentence in `bootstrap/PROVENANCE.md`, plus the run record `dev/measurement/windows-git-bash-release-route-2026-11-16.md`); this record. The five "four steps" places and the "skips 3-5" line are unedited and still true. I added no pointer to `BOOTSTRAP.md`, `UPGRADE.md`, `docs/quickstart.md` or `dev/rules/development-environment.md`: II-2 already sends the reader to `PROVENANCE.md`.

**Windows run (Git Bash, ARM64 VM, 2026-11-16).** Both routes ran to the end with no command changed: ordinary route against the real `v0.7.0` (200, 200, matching commit, clean checkout); stronger route with the real signature (`PROVENANCED`), and a wrong-key roster refused (exit 1). `/dev/null` isolation worked. Git Bash was started by full path. One failure: a bare `python` is the Microsoft Store stub (exit 49); the note says to use the real interpreter's path. Because the run passed, the "not yet documented" sentence was replaced. `command -v` results and gaps are in the record file.

**Commands run on the Mac (lhm Python 3.13)**: `test_install_report_slots.py` 6 passed; `test_verify_ref.py` 65 passed (it extracts and runs the PROVENANCE block, macOS only); `test_ast_attest.py` 28 passed, 1 failed (expected): `FunctionDef:print_report` differs from the baseline, awaiting the Maintainer's baseline operation; `claim_check.py` and `link_check.py` on the two prose files: no flags.

**Not run or not done**: the promise the Tests-required section adds to `test_install_report_slots.py` ("the report names `verify_integrity.py` before the slot step") is not added; that file is hash-pinned in the protected test roster and gate manifest, so it needs the Maintainer's re-anchor. The other 34 files `test_tiers.py` lists for `install.py`; Start-menu Git Bash; Windows' own `ssh-keygen.exe`; `test_verify_ref.py` on Windows; the two-channel fingerprint comparison (the run used one channel).

**Benefit versus cost**: worth it -- the printed list now matches II-2 and Windows adopters have a route that was run end to end; cost 2 commits, 4 files and about 4 minutes of VM time, tokens unknown; remaining burden: one stale AST baseline entry, one missing test promise needing a re-anchor, and a Windows re-run after the layout rename

## Implementation verification addendum -- Claude Sonnet 5.5 (Implementer, Medium) -- 2026-11-16

**Commit**: `87ea501b` adds `test_next_steps_name_verify_integrity_before_the_slot_step` to `bootstrap/tests/test_install_report_slots.py`, the promise the record above left out. It runs the real scaffold and checks that `verify_integrity.py` appears in the next-steps list before the slot step.

**Evidence**: on a throwaway worktree of `449fecc6^` (no installer line) it failed: the text before the slot step held no `verify_integrity.py`; the other 6 tests passed. In this tree the file runs 7 passed. I ran only that file.

**Re-anchor**: the file is hash-pinned, so it joins the Maintainer's re-anchor with `install.py`'s `print_report` baseline.

## Implementation verification addendum 2 -- Claude Sonnet 5.5 (coordinator) -- 2026-11-16

After the implementer's record, the neutrality sub-gate (`python scripts/quality_gate.py --sub neutrality`) failed on `bootstrap/PROVENANCE.md:122`: the Git Bash note named a vendor that shipped text must not name. Reworded to "Windows Store"; the gate now reports `fail=0`. The earlier record said only that the gate checks it ran were clean, so this was not run before.

## Implementation closeout -- Codex Terra, coordinator -- 2026-11-17

Complete on the recorded focused results, reusing evidence for unchanged
behavior. The combined revision includes the reviewed Windows receipt/ledger
repairs (`63d0704a`, `7c77da3d`; reviews `f8d171fd`, `aa1aeeba`). No suite
is repeated for this Boundary B record. Existing skips and omissions remain
unpassed; the grouped re-anchor stays a separate Maintainer wait on
`dev/PLANNING.md`, not an archive prerequisite.

Elapsed: approximately ten minutes for the grouped closeout; tokens unknown.
