# Plan: A simple usage meter

**Source proposal**: dev/proposals/archive/2026-11-21-claude-simple-meter.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/custom_session_routines.md, dev/rules/development-environment.md
**In brief**: The usage meter loses the permission and anti-tamper checks that stopped it running on ordinary machines, and keeps its two real promises: it reads only the folders you list, and only counts leave a log.

## Build summary

The meter reads each listed log folder and writes its summary with ordinary file calls, the same on Mac, Linux and Windows. Its Windows layer, owner and access-list tests, re-checks during a read and reading of a project's Git settings are deleted. The reader, the consent file's checked content, the shapes of record and summary, the size limits and the closed reasons do not change. By function span, 2,427 of the file's 7,573 lines go outright and 1,386 more are rewritten (estimate, not measured: the file ends near 4,700 lines); 88 of 298 meter tests are deleted. The tables (tests sorted, functions removed, document sentences) are in the detail file, `dev/plans/2026-11-21-simple-meter-detail.md`.

## Source proposal

The accepted proposal (heavy, parts A to F) replaces plan I. This plan carries A to F out and adds no check the proposal removed.

Proposed paths:
- dev/proposals/archive/2026-11-21-claude-simple-meter.md

## Scope

Surfaces: `dev/tools/meter.py` and its shipped copy `templates/skills/_lib/meter.py`; the meter's three test files and `tests/security/test_git_read_routes.py`; `tests/security_manifest.py`, `tests/test_security_check.py`, `release/security_check.py`; four documents, `CHANGELOG.md`, Cairn's lock. Result: a refresh answers `ok` on the Windows Server machine, with the same totals.

**The plain layer** does exactly the jobs A to F list. The line stream keeps its class, arguments and attributes, so kept tests keep their set-up. The lock is taken over after 15 minutes, three times the session routine's limit.

**Choices this plan makes, for reviewers** (detail file, section D): the remote is the consent file's; the home is the account database on Mac and Linux (equal-UID refusal kept) and Python's home on Windows; a log that cannot be read is left for the next run and reported `catching_up`; the folder flush after rename goes; two path-spelling parsers named for Windows stay, since the reader needs them. `git_read.py` is untouched: it is frozen and about 20 files pin its hash.

**Reuse.** The reader, ledger code, `_claim_snapshot` and `_project_export_bytes` stay as they are. One-line link and reparse tests exist in `content_scan_runner.py` and `exact_replace.py`; shipped tools cannot import each other. A search of `dev/tools/`, `install/`, `tests/` and `templates/` found no user of what goes except meter tests.

### Documentation / doctrine surface

`dev/measurement/README.md` (meter section), `templates/core/dev/measurement/README.md`, `dev/rules/development-environment.md`, `dev/rules/custom_session_routines.md`, `CHANGELOG.md`. Exact sentences: detail file, section E.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Plain reading: home, consent, log walk, line stream, claims | none | meter and shipped copy |
| C2 | Plain writing and project identity: lock, ledger, summary; Git read deleted | C1 | both copies; allowance in `release/security_check.py` removed |
| C3 | One path: Windows layer, descriptor code, unused imports deleted | C2 | both copies |
| C4 | Tests, shared set-up, pinned list and counts | C3 | test and manifest files |
| C5 | Documents, changelog, Cairn's lock | C4 | prose; lock alone in its commit |

## Acceptance criteria

**C1.** `read_records` is unchanged. No reading code uses `dir_fd`, `O_NOFOLLOW` or an owner test. A made-up folder holding a linked file, a linked folder and a sub-folder yields exactly its real logs.

**C2.** No `exec` or `git_read` remains. `read_records` differs only in its remote call and two dropped arguments. On a made-up home and project: summary and record are written, user-only where modes exist; a missing or linked `dev` or `dev/measurement` gets no summary and nothing outside changes; an old lock is taken over and a fresh one gives `ledger_busy`; a failed rename leaves the old bytes and no temporary file. Errors carry only closed reasons.

**C3.** Left named for Windows: the two parsers and the `nt` branches of three functions. All four commands share one path. The file compiles.

**C4.** 88 tests deleted, 103 changed, 2 added (a full run on a made-up folder with a sub-folder, every platform; a link out of a log folder not followed, a junction too on Windows); a kept test covers the proposal's third. The 35 `nt` and 48 `posix` meter rows leave `tests/security_manifest.py`: counts 28 and 314, fingerprint recomputed by the validator's own formula, guard line changed there and where `tests/test_security_check.py` quotes it. `python tests/tier_inventory.py check` passes.

**C5.** Each document sentence is in place; `cmp` of the meter copies prints nothing; after the lock commit `python install/verify_integrity.py --target .` reports OK.

Security preflight S2: the two promises keep their tests (detail file); the added link test is the negative control.

## Scope delta

**Scope delta**: preserved

Nothing is dropped beyond the proposal's accepted `lost` list; a kept test delivers the omitted third test's outcome.

## Verification

Changed promises: `refresh`, `rebuild`, `refresh --report`, the bare status, and the consent file, record and summary. The build runs the three meter test files, plus `tests/test_security_check.py` and `tests/test_skills_install.py` where they can run, once on Windows and once in the Linux subsystem, after C5; none before. Tests of removed checks are cut only through a Security Review (protected-surfaces rule); this plan's Internal Security Review is that review. Strategy's checks, not the build's: after the merge a real refresh on the Windows Server machine answers `ok`, its totals equal an independent count and only counts are found in the summary and record; the same on the Mac at the cut. The gate manifest's lines for touched frozen and test files are the Maintainer's signing lines; the detail file lists them; none is edited here. Not checked: Windows tests of a real refresh cannot run on this machine.
