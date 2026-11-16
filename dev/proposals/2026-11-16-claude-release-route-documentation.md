# Finish the release-route documentation: a verify step in the installer's list, and a tested Windows route

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
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

1. **Installer line.** In `print_report`, print a line numbered 2 before item 3, such as: "2. Before you edit any file, run `python bootstrap/verify_integrity.py --target <target>` from the Cairn checkout you installed from (II-2)." The plan decides whether to print it only when the lockfile was written; the simplest form adds "(skip if the report above says the lockfile was NOT written; follow its remedy first)". The line prints a command and runs nothing.
2. **Windows route: Git Bash, tested.** Document Git Bash (shipped with Git for Windows) as the supported Windows shell for both routes, with a one-paragraph note on how to open it and which tools it supplies. The plan's implementer runs both routes in Git Bash on the Windows VM described in `dev/rules/development-environment.md` (I did not connect), fixes any command that fails there in the shared text, and records the run. Then the "PowerShell equivalents are not yet documented" sentence in `PROVENANCE.md` is replaced by what was tested, with its date.
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
