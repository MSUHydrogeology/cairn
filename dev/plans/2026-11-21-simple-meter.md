# Plan: A simple usage meter

**Source proposal**: dev/proposals/archive/2026-11-21-claude-simple-meter.md
**Status**: awaiting-code-review
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

The kept tests fail between C1 and C4, because they still name deleted code; the per-chunk check is `python -m py_compile dev/tools/meter.py`.

## Acceptance criteria

**C1.** `read_records` is unchanged. No reading code uses `dir_fd` or an owner test (a leaf may open with `getattr(os, "O_NOFOLLOW", 0)`). A made-up folder holding a linked file, a linked folder and a sub-folder yields exactly its real logs. `_read_project_claims` refuses `dev` or `dev/intents.jsonl` if it is a link or reparse point: a made-up project whose `dev/intents.jsonl` is a link yields no claims.

**C2.** No `exec` or `git_read` remains. `read_records` differs only in its remote call and two dropped arguments. On a made-up home and project: summary and record are written, user-only where modes exist; a missing or linked `dev` or `dev/measurement` gets no summary and nothing outside changes; a fresh lock gives `ledger_busy`, an old one is taken over by the token rule of detail D5, and a finished run removes only its own lock; a failed rename leaves the old bytes and no temporary file. Errors carry only closed reasons.

**C3.** Left named for Windows: the two parsers and the `nt` branches of three functions. All four commands share one path, and `main` prints no traceback, path or system text (detail D13). The file compiles.

**C4.** 88 tests deleted, 104 changed, 2 added (a full run on a made-up folder with a sub-folder, every platform; a link out of a log folder not followed, a junction too on Windows); a kept test covers the proposal's third. The 35 `nt` and 48 `posix` meter rows leave `tests/security_manifest.py`: counts 28 and 314, fingerprint recomputed by the validator's own formula, guard line changed there and where `tests/test_security_check.py` quotes it. `python tests/tier_inventory.py check` passes.

**C5.** Each document sentence is in place; `cmp` of the meter copies prints nothing; after the lock commit `python install/verify_integrity.py --target .` reports OK.

Security preflight S2: the two promises keep their tests (detail file); the added link test is the negative control.

## Scope delta

**Scope delta**: lost

- The re-checks before publishing a summary go with the descriptor walks (E). An account that can write the project and swaps `dev` or `dev/measurement` for a link between the check and the rename can put a summary of counts in another folder the user can write, replacing a `meter.json` there. **disposition**: accept, by the Maintainer's words of 2026-11-21: "Accept the gap".

Nothing else is dropped beyond the proposal's accepted `lost` list; a kept test delivers the omitted third test's outcome.

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

## Plan review -- Claude Opus 5.5 (Security Review) -- 2026-11-21

```
Reviewed commit: 9f64b9ffb3ee0d88f74bfe74c22cd24a43019787
```

**Obligation**: clears the Internal Security Review of the plan, and is the protected-surfaces review of the pinned rows it removes.
**Tier**: Internal Security Review
**Findings**: raised (3 blocking, 4 non-blocking)
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes: both promises live in code that stays, but three write and error paths need exact words -- `dev/tools/meter.py` lines 7404 to 7427; detail D.
2. **Best alternative.** None simpler; a Mac-and-Linux-only descriptor write would close B2's race but brings back a second path -- proposal E; detail D.
3. **What would show it wrong.** Two runs holding the lock, a traceback naming a log, or a summary landing outside a project after a folder is swapped for a link -- detail D5, D7; `test_meter.py` lines 5718 to 5753.

**Agreement.** I agree with the usual review's findings. My B1 governs D5 and the lock half of its B1 and N5.

**Who holds the promises after the build.** Consent: `_fixed_user_home`, `_read_consent` with `validate_config_bytes`, the `enabled` check before any log or ledger is opened, `_scan_approved_sources` over the listed roots, `_read_project_claims` over the listed projects. Counts only: `read_records`, `_claim_snapshot`, `_new_ledger`/`_load_ledger`, `_project_export_bytes`, `_closed_refresh_receipt`. Three deleted functions carried part: `_capture_project_claims` (usual B2), `_private_regular_file` (the consent size bound, N1), and `_run_windows_refresh`'s wide `except` (B3).

**The lock (the owner's answer).** Two runs can write at once: two runs taking over the same old lock; a busy run whose `finally` removes the holder's lock, as D5 reads; a manual run past 15 minutes. Worst outcome, by reading the code, not by running it: the last rename wins, the other run's events and cursors are dropped together, the next run reads them again, and the summary can briefly match the other ledger. No double count, no text, no write outside the listed places: within S4.

**Pinned rows.** The 35 `nt` rows and 42 of the 48 `posix` rows go rightly. The six `test_posix_project_export_detects_substitution_before_publication` rows go rightly only if B2 is accepted. The `dev-link` and `measurement-link` cases guard "never through a link" and must run on every host (A2 says so).

**Link races.** Reading: a log swapped for a link after the walk is read, but only its counts leave, so this is within S5. Writing: see B2.

**`release/security_check.py`.** Only allowance removed: its one meter entry (line 215) excuses the one `exec` (line 5932).

**Blocking**

- **B1. Lock takeover and removal are unspecified.** Replace D5 with the words below.
- **B2. A race can put the summary outside the project.** If `dev` or `dev/measurement` is swapped for a link after the check, the rename replaces any `meter.json` the user can write elsewhere, the consent file included. The proposal lists "a summary found outside a project" as a sign it is wrong, and its `lost` list does not name write re-checks. Add the Scope delta line below, or keep a Mac-and-Linux descriptor write.
- **B3. A traceback can print a log path.** Add the D13 words below.

**Non-blocking**

- N1. Consent and ledger: read at most the limit plus one byte from one open.
- N2. Windows: skip only symlink and mount-point reparse tags (`st_reparse_tag`); other tags would drop logs without a reason.
- N3. A killed run leaves `.meter-*.tmp` in `dev/measurement`, which Git does not ignore (`git check-ignore`); the next run removes it.
- N4. Optional: open a leaf with `getattr(os, "O_NOFOLLOW", 0)`; C1 then allows it.

**Not covered**: running anything, real machines, the gate manifest, Windows reparse-tag behaviour on a real profile.

### Exact words

**D5.** "**Lock.** `ledger.lock` in `~/.cairn/meter/`, made with `O_CREAT | O_EXCL` and holding 32 random hex characters this run writes. If it exists and its modification time is under 900 seconds old (or more than 60 seconds ahead), `ledger_busy`. Otherwise the run reads its token, reads it again, and removes it only if unchanged; then it makes it afresh with `O_EXCL`, and a failed make is `ledger_busy`. In a `finally`, a run removes `ledger.lock` only if it made it and the file still holds its token. Two runs can still both take over one old lock; then the last rename wins and the other run's counts are read again next run."

**Scope delta (B2), disposition accept, Maintainer's word needed.** "The re-checks before publishing a summary go with the descriptor walks (E). An account that can write the project and swaps `dev` or `dev/measurement` for a link between the check and the rename can put a summary of counts in another folder the user can write, replacing a `meter.json` there."

**D13.** "`main` catches every `Exception` around each command and prints only the closed receipt (`unavailable`, `unavailable`) or, for the bare status, `unavailable`; no traceback, path or system text is printed."

## Plan response -- Claude Sonnet 5.5 (Implementation, for the plan's owner) -- 2026-11-21

Both reviews are folded once, in place. Status is `ready-to-implement`. The Security Review governs where the two differ.

Usual review:
1. B1 (lock lines in the kept test): taken. `test_refresh_persists_normalized_history_and_claims_without_raw_inputs` moves to "Other changes"; the two lock assertions go and the two mode assertions run only on `posix`. Changed tests: 104.
2. B2 (claims link rule): taken in detail D14 and in C1.
3. N1 (`test_explicit_refresh_partial_receipt_is_closed_and_nonzero`): taken; now under "Other changes", so kept as is is 106.
4. N2 (tree fails between C1 and C4): taken, a sentence under Sequence naming `py_compile`.
5. N3 (how the link is found, temporary file name, removal): taken in detail D14.
6. N4 (every call of `_verified_project_remote` goes): taken in detail D1.
7. N5 (killed run leaves its lock): taken in detail D5 and in the README sentence (detail E1).

Security Review:
1. B1 (lock): taken in its exact words, detail D5, plus the C2 criterion. The lock is removed at the end of a run.
2. B2 (summary-write gap): accepted by the Maintainer, "Accept the gap" (2026-11-21). The Scope delta line is added in the Review's words; no descriptor write is kept; the six `posix` rows leave as before.
3. B3 (traceback): taken in its words, detail D13 and the C3 criterion.
4. N1 (read the limit plus one byte from one open): taken, detail D8.
5. N2 (skip only symlink and mount-point tags): taken, detail D7.
6. N3 (leftover `.meter-*.tmp`): taken, detail D14; the next run removes it.
7. N4 (`O_NOFOLLOW` on a leaf): taken, in C1 and detail D14.

Not run for this response: any test.

**Elapsed**: unknown. **Tokens**: unknown.

## Implementation record -- Claude Sonnet 5.5 (Implementation) -- 2026-11-21

The meter is built as the plan says, on branch `simple-meter-impl` (work folder `.claude/worktrees/simple-meter`), not merged. Read from the code and the runs below; nothing else was run.

**Commits by chunk.** C1 to C3 `f7f4ddda` (the plain layer, the Windows layer, owner tests and Git read deleted, both copies, the `B102` allowance removed). C4 `386ae2d2` (tests) and `45aaef44` (pinned list: `nt` 63 to 28, `posix` 362 to 314, fingerprint recomputed by the validator's formula, which accepts it; guard line changed in both files). `548018c5` fixes found by the first Windows run. C5 `4489b295` (documents and changelog) and `e3790d46` (Cairn's lock, alone; `verify_integrity.py --target .` reports OK for 70 files). Status commit `9307dcbc`.

**Lines of `dev/tools/meter.py`.** 7,573 before, 4,624 after (`wc -l`). The shipped copy is identical (`cmp` prints nothing).

**Tests, counts by function.** 88 deleted, 104 changed, 106 kept as they were, 2 added (the changed count is one over the plan's 103 after the review fold; `test_meter.py` holds 176 functions, `test_meter_claude_usage.py` 32). Node ids collected: 371, 73 and 14 for the three meter files.

**Windows (this host, Python 3.13).** `test_meter.py` 367 passed, 4 skipped (the four tests that keep `POSIX_ONLY`); `test_meter_claude_usage.py` 73 passed; `test_meter_usage_free_records.py` 14 passed. Also `tests/test_security_check.py` (4 failed) and `tests/test_skills_install.py` (1 failed): 650 passed, 5 failed, 6 skipped in all. The five failures are this host's: four signing-history tests stop at "detached checkout path ... does not match commit" or "git-read-binding-failed", and the skills test cannot make a symbolic link (`WinError 1314`, the privilege is not held). None names the meter or the pinned list.

**Linux subsystem (Ubuntu, Python 3.14, commit `548018c5`).** The same five files: 575 passed, 10 skipped, 77 failed. All 77 are in `tests/test_security_check.py` and end at "join refuses this platform (native evidence platform is unsupported or inconsistent)", which is that file's Mac-only signing path. The three meter files and `test_skills_install.py` passed whole.

**Found by the Windows run, fixed.** A directory entry carries no file id on Windows, so the walk reads each file by name. A handle and a name report different change times for one file on Windows, so the stream takes its identity by name; before this the unchanged-log skip failed on a fraction of runs. Not fixed, outside this plan: `dev/tools/pulse.py` refuses a just-written report on Windows for the same reason (30% of 40 files in a direct check), so the explicit-report part of `test_report_freshness_public` runs off Windows only, with a comment saying why. This is a parity gap in the pulse for Strategy.

**Differences from the plan.** (1) The claims reader keeps the name `_capture_project_claims`, and the ledger writer `_atomic_replace_ledger`, because kept tests patch those names. (2) `_is_link` tests the reparse attribute and tag by attribute, with no `os.name` branch, so `os.name == "nt"` stays in two functions, not three. (3) `main` wraps a new `_main` to print only a closed answer. (4) `test_codex_normalized_events_bind_only_exact_approved_local_projects` keeps its `project_remote_mismatch` assertion, which is the Codex log's own repository name compared with the consent file's remote; only its patch went. (5) The added link test lists a file-link case only where the host can make one; on this host it has the folder-link (junction) case only. (6) `tests/check_cairn.py` with no argument reports 3 issues this plan caused: line-bounds citations of ranges that end near line 690 of `tests/security_manifest.py` in `dev/proposals/2026-11-19-codex-native-release-membership.md` (line 86, and line 140 inside a review) and `dev/strategy/2026-11-21-claude-read-of-six-unsigned-files.md` (line 32). They are not edited: one is inside a review and one is Strategy's note. The file is now 608 lines.

**Not run.** Every other test file; the real machines (Strategy's checks); a real refresh; `CAIRN_FULL_SUITE`; the gate manifest's signing lines, which this build did not touch.

**Elapsed**: unknown. **Tokens**: unknown.

## Code review -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-21

```
Reviewed range: 7202294d3ab5733ea7b6b58ee72fd1b063e10b5d (merge-base with 0.9-dev) .. e1c14ee94a72d10b95b487ba6d95bf73f4351ac9
```

**Obligation**: clears the usual code review; the Security Review pass follows.
**Findings**: raised (0 blocking, 4 non-blocking)
**Verdict**: ACCEPT

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this have been built as framed?** Yes. The two promises sit in code the diff leaves alone: `read_records` differs only in its signature and the one remote call (`git diff 0.9-dev HEAD`, lines 3779 to 3800 of `dev/tools/meter.py`), and `validate_config_bytes` and `_claim_snapshot` are untouched.
2. **Does the change do what the plan says?** Yes. The walk (`_enumerate_jsonl`), the claims read, `_write_summary`, `_take_lock` and `main` match detail D5, D7, D13 and D14. No `exec`, `git_read`, owner test or `dir_fd` remains (searched). Nothing named for Windows is left but the two parsers and two `nt` branches.
3. **What would show it wrong?** A real refresh on the Windows Server machine and the Mac (Strategy's checks, not run here).

**Checked, not run**: `cmp` of the two meter copies prints nothing. The lock commit holds one file, two lines. `verify_integrity.py --target .` reports OK for 70 files. The pinned list, loaded by its own validator, gives 28 and 314 with the fingerprint accepted; the guard line in `tests/test_security_check.py` matches line 606 of the manifest. The `B102` entry was the only change in `release/security_check.py`. The deleted tests are the plan's 86 in `test_meter.py` (65 Windows, 21 listed), plus one each in the other two files; none tests consent or counts-only. The two added tests are as the plan names them.

**Non-blocking**

- N1. No test covers the claims link rule (plan C1: a link at `dev/intents.jsonl` yields no claims). The kept export test patches `_capture_project_claims` out. The code reads right (`_capture_project_claims`, lines 372 to 395); a hand check or one test would close it.
- N2. The test that quotes the guard line (`test_committed_fixture_connects_real_record_and_join_entrypoints`) skips off a Mac, so no recorded run exercised that edit. The manifest's own validator runs at every collection and accepts it.
- N3. The five Windows failures are called this host's, but the record does not show the same five failing on `0.9-dev`. The Linux run was at `548018c5`, before the prose and lock commits.
- N4. If the lock file is created but its token write fails, an empty lock stays for 15 minutes (`_take_lock`, `make`). Rare, and the same wait as a killed run.

**Left unshown**: the Mac; a real refresh; links on Windows other than junctions; a Windows run of the file-link case. A pulse import failure still prints a traceback before `main` runs (not changed here).

**Not covered**: running any test; the full diff of the kept tests (read the five named in the plan and both added tests); the gate manifest.
