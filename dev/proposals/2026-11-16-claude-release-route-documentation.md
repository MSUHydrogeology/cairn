# Finish the release-route documentation: a verify step in the installer's list, and a tested Windows route

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
**Waiting on Maintainer**: release draft for review
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
