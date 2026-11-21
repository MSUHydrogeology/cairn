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

## Plan review -- Claude Sonnet 5.5 (Reviewer) -- 2026-11-21

```
Reviewed commit: f25447fa6634c47406eef7818ffa785b9169324e
```

**Obligation**: clears the usual plan review; the Security Review pass follows.
**Tier**: Internal
**Findings**: raised (2 blocking, 4 non-blocking)
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes. The plan removes what the Decision removes and keeps the reader, the consent file's content check, the shapes and the closed reasons -- detail file C and D; proposal A to F.
2. **Best alternative.** None simpler within the Decision; the one-flow rewrite of the four commands is the lightest way to one path -- detail C, "Rewritten".
3. **What would show it wrong.** A kept test failing on Windows for a reason the plan did not name, or a claims file read through a link -- `tests/integration/test_meter.py` lines 5371 to 5374 and detail D.

I checked by script, not by running any test: the detail file's sorted lists cover all 260 `test_meter.py` functions once each, with no name missing or invented. The 35 `nt` rows are all of deleted tests. The 52 `posix` rows split 21, 5, 22 and 4, so 314 is right. The 63 and 362 guard line is at `tests/security_manifest.py` line 689 and quoted at `tests/test_security_check.py` line 1306. The `exec` is only at `dev/tools/meter.py` line 5932, and the `B102` allowance is at `release/security_check.py` line 215. No other tool imports the meter. Both promises' tests are kept.

**Blocking**

- **B1. A kept test contradicts the lock rule.** `test_refresh_persists_normalized_history_and_claims_without_raw_inputs` (listed "marker off and patch removed") asserts after the run that `ledger.lock` still exists, is empty and has mode `0o600`, and that the ledger's mode is `0o600` (lines 5371 to 5374). D5 removes the lock at the end, and Windows has no such modes once the marker is off. Move it to "Other changes": delete the two lock lines, and make the two mode lines run only `if os.name == "posix"`. Change "103 changed" to match if the count moves.
- **B2. Work claims have no link rule.** Proposal B says `dev/intents.jsonl` is "not through a link". D and C1 say nothing of it. Add to D: "`_read_project_claims` refuses `dev` or `dev/intents.jsonl` if it is a link or reparse point, and reads it with the same size limits as now." Add to C1 a criterion and one made-up-folder check of it.

**Non-blocking**

- N1. `test_explicit_refresh_partial_receipt_is_closed_and_nonzero` is "kept as it is" but takes the deleted `native_windows_root` argument; it belongs under "Other changes".
- N2. The plan does not say the tree fails its tests between C1 and C4. Say so, and name `py_compile` as the check per chunk.
- N3. `_write_summary` and `_read_project_claims` are given only a line count. Name how the link is found (`lstat` of `dev`, then `dev/measurement`, each refused if a link or reparse point), the temporary file's name in the same folder, and its removal on failure.
- N4. Several call sites of `_verified_project_remote` exist besides `read_records` (lines 4563, 5498, 5639, 5705, 5857, 6703); say all go.
- N5. A run killed by `session.py` leaves its lock, so the next session-end sees `ledger_busy` for up to 15 minutes. Say so in the README sentence.

**Not covered**: running any test, real machines, the Security Review questions, the gate manifest's contents beyond its named lines.
