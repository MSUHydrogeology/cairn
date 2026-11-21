# Plan: Defect arc D1, gate narrowings and release control

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: archived
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: Win back two checks that the 0.8 file move weakened, let the release check read Windows test-report paths, and write down how to freeze history from a fresh clone; the older Windows test failures wait for a second plan that measures them on the Windows host first.

## Build summary

After this plan, the ceremony's review page again shows the lines a new tool file adds under `tests/`, from the first signing after v0.9's, the fork-advisory test again tells which lock record a refusal names, the release membership check reads the backslash paths pytest writes on Windows, and the release process says to freeze history from a fresh clone. Four chunks. The older Windows failures, the Windows tag check and the signing-ceremony tests go to a second plan, D2, because each needs a Windows measurement first.

## Source proposal

The Maintainer accepted the defect arc at the heavy tier ("Go ahead on the defect arc.", chat, 2026-11-20). Plan D is its gate-and-Windows part. Reviewers called it full, so it is cut in two; this is D1, the items that need no measuring. Exact code, texts and fixtures are in the companion `dev/plans/archive/2026-11-20-defect-arc-d-gate-and-windows-checks-detail.md` ("Detail"), part of this plan: it exists because they would double its length, and a low-tier implementer must not invent them. The plan reopens nothing.

## Scope

**Result.** Two narrowed gate checks work again without checking less than before, one release check works on Windows, and one release step is written down.

| Item | Chunk | Entry point |
|---|---|---|
| B3a new files under `tests/` unscanned | D1-1 | `python tests/_gate_preflight.py` range report (`range_review_report`) |
| B3b `test_fork_advisory.py` checks only exit 2 | D1-2 | `cmd_upgrade` refusal text |
| B2b checker refuses Windows `file=` paths | D1-3 | `python release/check_release_test_members.py` |
| History freeze fails on refs that point at trees | D1-4 | `python release/security_check.py --freeze-history` (documented, not changed) |

**Where the code differs from Strategy's defaults** (read, not run):
1. **B3a is smaller than "new files under `tests/`".** Before the move, the scan excluded the whole old test folder (bootstrap's tests), new tests included. What it lost is the former `scripts/` tools, now at the top of `tests/` (`tests/gauge.py` and others, per the layout plan's closing review). Restoring means scanning new non-test files under `tests/`; new `test_*.py` modules and `tests/fixtures/` stay out, as before, and an existing test pins that.
2. **B3b already names the field.** The test asserts `'src' is not a plain relative file name`. What is missing is which record. The refusal text carries `record <n>:` (`install/_scaffold/upgrade.py`, `_contained_lockfile_path`); the test will check that number. No word match is restored.
3. **B2b: accept, not "Mac only".** The checker already has a Windows host tag (`_host_tag`), and the roadmap row on verifying releases on three hosts asks for a Windows record. "Mac only" would also force a skip of its contract test on Windows. The change applies on Windows only, to one field.
4. **Freeze from a clean clone needs one more rule.** The join compares the live repository's location and refs with the frozen manifest (`release/security_check.py`, `_run_join`), so the Mac record and the join must run in the same clone. 0.8 waived those records, so a clone-based freeze has never been carried through to a join. D1-4 writes the rule; the 0.9 cut is the first proof.
5. **The Windows tag check moves to D2:** it runs only on a Windows host.
6. **The ceremony tests cannot simply be marked.** A skip marker on a protected node is a HOLD for that node at the signing (`tests/_gate_manifest.py`, `SKIP-XFAIL-NEW`). Marking 249 nodes gives the Maintainer 249 lines. D2 takes the item: first make the tests run, mark only what cannot.
7. **Pre-0.8 comments in frozen files.** D1 edits two frozen files (`tests/_gate_preflight.py`, `release/check_release_test_members.py`). Neither holds a comment naming an old folder (searched `bootstrap`: four hits, all live code or messages). Plans B and C left comments in seven other frozen tools (sixteen comment lines in eleven file copies); D1 edits none of them and does not take them. The accepted arc counts them, so leaving them is the Maintainer's to allow. Home: `dev/PLANNING.md`, section 1, "Comments in protected files", and the question under "Waiting on you".

**Defects found since.** (1) Ceremony tests on Windows: D2. (2) Fixed Mac tool paths in signing tests: left to the roadmap row "Verify every release on Linux and Windows alongside Mac"; the row needs the test setups to find tools by their real location, and a Linux host with Python 3.13 (the shared VM has 3.12.3). (3) Comments: item 7. (4) Windows Server socket, symbolic-link and gitleaks failures: D2.

**Protected files and the reason the Maintainer will see at the signing.**
- `tests/_gate_preflight.py` (frozen, in the authority closure): the range report again scans new non-test files under `tests/`; it scans more and accepts nothing new.
- `tests/test_ceremony_review_report.py` and `tests/test_fork_advisory.py` (protected roster): one node added; one assertion strengthened, none removed.
- `release/check_release_test_members.py` (frozen): on Windows only, the report's `file=` field may use backslashes; every other check stays.
- `tests/contract/test_release_members_contract.py` (ordinary test): four nodes added.
- `release/RELEASE_PROCESS.md`: prose, not frozen, not on the roster.

**Staleness (read; `python install/scaffold.py --manifest` listed none of these files).** The gate manifest already names the pre-0.8 paths and is regenerated at the one signing; D1 adds two HOLD lines (the two frozen files) and refreshes nothing. The AST baseline covers `install/_scaffold/`, untouched. The install lock covers shipped files; none changes. No changelog line.

**Reuse.** The scan keeps `_scan_range`, `SCAN_PATTERNS` and the existing test helpers `_make_range`, `_report`, `_hits`. A search for a second copy of the scan constants found only `release/repin.py` line 203, which reads the prior verifier's copy and is not edited.

### Documentation / doctrine surface

`release/RELEASE_PROCESS.md` gains one paragraph (D1-4). No rule text weakens or is removed.

**What D2 holds, and what it must measure first.** D2 is written after these are measured on the project's Windows guest (`cairn-windows`, reached from the Mac) and, for the last item, on this Windows Server machine, one record each: (a) B2a, the nine older failures in the release-members contract test, with Git Bash on `PATH`; (b) B2d, the Git-absent test in `tests/test_portable_security_sweeps.py` (it uses a shebang fake tool); (c) B2e, the fifteen failures of 2026-11-16, whether already repaired; (d) the published v0.8.0 tag through both routes in `install/PROVENANCE.md`, in Git Bash; (e) the ceremony tests' missing temporary-folder variable: whether adding it makes them run, and what still needs POSIX tools; (f) the socket, link and gitleaks failures: the host's or the shell's, or Cairn's. D2 then repairs what is Cairn's.

## Sequence

D1-1 to D1-4 touch disjoint files and may land in any order. Code review once after D1-4; no earlier review point, since nothing builds on a chunk. Each chunk is committed alone.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| D1-1 | New-file scan | plan review | scan restored; one new test node |
| D1-2 | Fork-advisory record | plan review | test names the record |
| D1-3 | Windows `file=` | plan review | one helper, four nodes |
| D1-4 | Freeze from a clone | plan review | one paragraph |

## Acceptance criteria

**D1-1.** `_scan_range` scans a file the range adds under `tests/` unless it is a test module (`_is_test_module`, Detail D1) or lies under `tests/fixtures/`. Changed files not added, the pattern list, size limits and report schema are untouched; `release/repin.py` is not edited. **Permanent**, `tests/test_ceremony_review_report.py`, through the range report on a throwaway repository: an added tests/new_tool.py and tests/sub/conftest.py carrying `import subprocess` each give one `process-start` hit; an added tests/test_new.py, tests/security/test_new.py and tests/fixtures/data.py give none and are counted as not scanned. The node fails at the starting commit, which is the control that it catches a new file. **Developmental:** restore `"tests/"` to the excluded constant; the node must fail.

**D1-2.** In the `{"src": "../../../../etc/hostname"}` branch of `test_node16_f5_parametric_no_lockfile_field_can_suppress_at_upgrade`, the test also asserts `record <n>: the lockfile's 'src' is not a plain relative file name`, with `<n>` the planted record's position in the lock (Detail D2). Nothing is removed; no wording such as "containment" is matched. **Permanent**, same node, through `cmd_upgrade`. **Developmental:** expect `n + 1`; a hostile `src` on another record; both must fail. If the refusal at the starting commit carries no `record <n>:` text, stop and return the plan to `revising-plan`.

**D1-3.** On Windows (`os.name == "nt"`) the checker reads the `file=` field with backslashes as forward slashes, then applies the existing `_file` checks and the comparison with the file the classname names (Detail D3). On other hosts, and for the policy list, `--required-files` and the classname, a backslash is refused as before. **Permanent**, through the checker's command line: off Windows, a backslash `file=` exits 1 with `invalid test-file identity`; on Windows, the same file exits 0; on every host, a `file=` naming another file exits 1 with `test file and classname identities disagree`, and one with `..` exits 1 with `not a canonical relative path`. The Windows node fails before the change, on Windows only.

**D1-4.** `release/RELEASE_PROCESS.md` says, in "Strict release-security evidence", to freeze from a fresh clone and to take the Mac record and run the join in that same clone (Detail D4, exact text). The `bash` block the contract test reads is byte-identical. **Developmental:** `git diff` shows one inserted paragraph; the contract test's `test_actual_pytest_identities_and_documented_sequence` still finds its block.

**Security (re-answered, only where chunking changes an answer).** S1: the report's `file=` field and the new files in the range come from the thing judged; the first is compared with an independent source (the classname) and the second is read from raw objects. S2: the negative controls are the off-Windows refusal, the other-file and `..` cases, and the test-module and fixture exclusions. S3: the ceremony range report and the release block fire the checks; D1-4 is read at the cut. S4: nothing accepts more by default except, on Windows, the backslash spelling of a `file=` value the checker already accepts with forward slashes, absolute paths inside the checkout included; the field can only refuse a case. S5: a forged `file=` that names the same file passes, as before; the classname is the authority. D1 does not run the freeze, join or any signing.

## Scope delta

**Scope delta**: preserved. B3a, B3b and B2b are delivered as the proposal words them. Two items of plan D move to D2 (the tag check and the ceremony tests); the proposal assigns them to plan D, and D2 is plan D's remainder. The freeze item takes the proposal's default: a documented clean clone.

## Verification

**Selector** (`C:\ProgramData\Anaconda3\python.exe tests/tier_inventory.py for <paths>`, at the opening commit): D1-1 selects 9 files (`test_ceremony_review_report`, `test_gate_preflight`, `test_gate_reanchor`, `test_oracle_activation`, `test_reanchor`, `test_reanchor_driver_disclosures`, `test_repin`, `test_repin_ceremony`, `test_security_marker`); D1-2 selects 1; D1-3 selects 2 (the contract test and `test_security_marker`); D1-4 selects 1 (the contract test). All are under the 40-file guard. For each chunk, run its selected files once at the starting commit and keep each failure's test id and message; run them again after; a failure is a host failure only if both are on the first list. On this machine the ceremony files fail in large numbers before any change (measured 2026-11-20: 249 of 286 in three of them), so the baseline run comes first. The Mac session runs D1-1's nine files once, where the ceremony belongs.

**Hosts.** This Windows Server machine: all chunks and new tests, including the Windows node of D1-3 (not the project's guest, so not Windows-record evidence). The Mac session: D1-1's selection, and optionally a disposable fresh-clone freeze and Mac record to prove D1-4 before the cut. The project's Windows guest: nothing in D1. The signing refreshes the manifest on the Mac.

**Owners.** The Mac run of D1-1's nine files is the Maintainer's, taken by the Mac session that takes the re-anchor plan; D1's closeout records that run's failures by test id and message, or states it was not run. If the new node cannot run on the Windows Server machine, the closeout says so. The D2 measuring list is copied into `dev/PLANNING.md` section 1, under 'Windows', with the Maintainer's launch of a Mac session that reaches `cairn-windows` listed under 'Waiting on you'. D1 does not reach `ready-to-archive` until both edits are committed.

**Prose gates**, one file per call, on this plan, the companion and `release/RELEASE_PROCESS.md`: `dev/tools/claim_check.py`, `dev/tools/link_check.py`, `tests/check_cairn.py`, and `git diff --check`.

**Roadmap entries.** D1 settles "Narrowings from the layout move", the `file=` clause of "Windows", and "The history freeze in a live repository". No GitHub issue is touched; nobody closes or comments on one without the Maintainer's word. The closeout names those added files (test modules and `tests/fixtures/` aside) in `dev/PLANNING.md` section 1 under 'Narrowings from the layout move', and asks under 'Waiting on you' whether the Maintainer reads their added lines before he signs.

**Not checked.** No code or test was run for this plan. Not run: any freeze, record, join or signing; the Windows node of D1-3; whether `git clone` leaves out refs that point at trees (assumed from Git's default); the v0.9 signing's page: as a layout transition it shows the anchor's own scan (`release/repin.py`, the layout scan script), which skips files added under `tests/` or `dev/tools/` since the move; D1-1 cannot change it; macOS. **Does any rule weaken or disappear?** No: D1 scans more, asserts more, and accepts, on Windows, the backslash spelling of one field.

## Plan review -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-20

Reviewed commit: bd11372cb8c9ced611380b238a04ecd48807c813

**Obligation**: the usual plan review the heavy tier requires.
**Tier**: Internal
**Findings**: raised

The plan restores two narrowed checks, lets the release check read Windows paths, and documents the clone freeze, in four disjoint chunks a low-tier model can follow. I read the code at every cited place; I ran nothing.

**Foundations**

1. **Should this happen as framed?** Yes. The history supports the narrower claim: before the move only the old bootstrap test folder was excluded, and `scripts/` tools were scanned; the move put them at `tests/` (`git show c139612b -M`). The restored scan checks at least what it did before. -- `git log -S_SCAN_NEW_FILE_EXCLUDED`, `tests/_gate_preflight.py:1346`
2. **Best alternative.** Scanning every new test was the other option; the plan's exclusion of `test_*.py` and fixtures matches the old behavior. -- `tests/_gate_preflight.py:1442`
3. **What would show it wrong.** Forward test: an added tool file under the tests folder with `import subprocess` gives no hit. The plan's new node covers it and fails at the starting commit. The `record <n>:` text is printed on this path from either caller. -- `install/_scaffold/upgrade.py` lines 251, 320, 4141, 4655

**Findings**

1. **Blocking.** Two runs have no owner: the Mac run of D1-1's nine files, and D2's Windows measurements. Nothing in `dev/PLANNING.md` names either. The ceremony files fail 249 of 286 here, so the new node's own result may exist only on the Mac. Exact words below.
2. Non-blocking. D1-3's Windows spelling also lets through a drive-letter path inside the tree and mixed separators. The classname comparison stays the authority; the Security Review should judge it, and "one spelling" understates it.
3. Non-blocking. D1-4's paragraph needs the clone fully prepared before the freeze: a fresh clone lacks `refs/cairn/gate-anchor` (`dev/rules/protected-surfaces.md`), and a ref added after the freeze makes the join refuse.
4. Non-blocking. The `_scan_range` docstring (line 1423) still names three roots; update it. The D1-3 nodes should start from the `evidence` fixture and rewrite the report, as `test_report_refusals` does.
5. Non-blocking, for the Maintainer. D2 makes six plans; the Decision named five.

The cut loses no accepted item: B2a, B2d, B2e and the tag check sit in D2's list.

**Not covered**: no test run; the Windows `file=` spelling and clone behavior are unmeasured. Elapsed about 30 minutes; tokens unknown.

**Verdict**: REVISE

### Exact words closing finding 1

Add to "Verification", after "Hosts": "**Owners.** The Mac run of D1-1's nine files is the Maintainer's, taken by the Mac session that takes the re-anchor plan; D1's closeout records that run's failures by test id and message, or states it was not run. If the new node cannot run on the Windows Server machine, the closeout says so. The D2 measuring list is copied into `dev/PLANNING.md` section 1, under 'Windows', with the Maintainer's launch of a Mac session that reaches `cairn-windows` listed under 'Waiting on you'. D1 does not reach `ready-to-archive` until both edits are committed."

Add to finding 3's chunk (Detail D4), at the end of the paragraph: "Before freezing, fetch `refs/cairn/gate-anchor` into the clone if the record needs it; no ref may be added after the freeze."

## Plan review -- Claude Opus 5.5 (Security Review) -- 2026-11-20

```
Reviewed commit: 30dd90bb4d68c736b84842e19c67f8491f4c2c22
```

**Obligation**: the Security Review the heavy tier adds at the plan stage.
**Tier**: Internal Security Review
**Findings**: raised (two blocking)

The plan's aim is sound: win back what the move narrowed, accept nothing new except Windows path spelling, and write down a freeze route. I read the code at each cited place; I ran nothing.

**Foundations**

1. **Should this happen as framed?** Yes, but D1-1 only takes effect for signings after v0.9's -- `release/repin.py:175-207`, `3040-3045`.
2. **Best alternative.** Also changing the transition's scan script; that is `release/repin.py`, the re-anchor proposal's file, not D's -- `release/repin.py:203`.
3. **What would show it wrong.** Forward test: at the v0.9 transition, a new tests/new_tool.py holding `import subprocess` gets no hit on the page -- `tests/_gate_preflight.py` `_layout_stage`.

**Findings**

1. **Blocking.** At the v0.9 signing (a layout transition) the page's scan comes from the anchor's own scanner, and the signing refuses unless the report's digest equals it. That scanner does not scan new files under `tests/` or `dev/tools/`. The Build summary promises otherwise. Exact words below.
2. **Blocking.** In an untouched clone the join cannot see the working checkout move, so it can pass while that checkout's `master` carries commits the freeze never scanned. Exact words below.
3. I agree with the usual review's finding 1; its words stand. For its finding 3, my words govern (below).
4. Non-blocking, agreeing with usual finding 2. Off Windows nothing changes. On Windows the field can still only cause a refusal: `compare` requires it to equal the file the classname names. My S4 words govern (below).
5. Non-blocking, for the Maintainer. A new test module or a conftest.py under `tests/fixtures/` still runs at collection unscanned. The old test folder was excluded in the same way. Other names fail towards scanning (`*_test.py`, `Fixtures/`).
6. Non-blocking. Spell the `..` node's `file=` with the host's separator, so on Windows it exercises the conversion.

The fork-advisory assertion fails if upgrade stops refusing or names another record; `read_lockfile` does no validation (`install/_scaffold/lockfile.py:450`).

**Not covered**: no run; files added since the anchor not counted (no local `refs/cairn/gate-anchor`); whether the record's tests read that ref. About 380 words: two blocking findings carry their evidence. Elapsed about 25 minutes; tokens unknown.

**Verdict**: REVISE

### Exact words from the Security Review

Finding 1, plan. In "Build summary", after "under `tests/`" insert ", from the first signing after v0.9's". Replace the "Not checked" item beginning "whether the ceremony's scan digest" with: "the v0.9 signing's page: as a layout transition it shows the anchor's own scan (`release/repin.py`, the layout scan script), which skips files added under `tests/` or `dev/tools/` since the move; D1-1 cannot change it." Add to "Roadmap entries": "The closeout names those added files (test modules and `tests/fixtures/` aside) in `dev/PLANNING.md` section 1 under 'Narrowings from the layout move', and asks under 'Waiting on you' whether the Maintainer reads their added lines before he signs."

Finding 2, Detail D4, end of the paragraph: "The join's `PASS` covers only the commit it names. Push only that commit as `master`: where you push from, `git rev-parse master` must print it; if not, stop and freeze again."

Usual finding 3, Detail D4, in place of its words: "Before the freeze, fetch `refs/cairn/gate-anchor` into the clone from the trusted origin and verify its signed commit; fetch nothing after the freeze."

Finding 4, plan, S4: "S4: nothing accepts more by default except, on Windows, the backslash spelling of a `file=` value the checker already accepts with forward slashes, absolute paths inside the checkout included; the field can only refuse a case."

## Plan response -- Claude Sonnet 5.5 (`claude-sonnet-5-5`, for the author) -- 2026-11-20

Both reviews said REVISE. Every blocking finding is applied with its reviewer's words; where the two touch the same point, the Security Review governs.

**Usual review**

1. Blocking: the "Owners." paragraph added to Verification after "Hosts".
2. Non-blocking: replaced by the Security Review's S4 words; the matching "one spelling on one host" phrase in "Not checked" now reads "accepts, on Windows, the backslash spelling of one field".
3. Non-blocking: the Security Review's fetch sentence added to Detail D4 before the freeze instructions end; the usual review's sentence not used.
4. Non-blocking, first part: Detail D1 now gives the exact `_scan_range` docstring lines to write. Second part: Detail D3 says the four nodes start from the `evidence` fixture and rewrite the report; `evidence` and `test_report_refusals` both exist in `tests/contract/test_release_members_contract.py`.
5. For the Maintainer: six plans where the Decision named five. No change; Strategy carries it to the Maintainer through `dev/PLANNING.md`. The split follows the rule that a plan has at most five chunks.

**Security Review**

1. Blocking: Build summary insertion, the "Not checked" replacement and the "Roadmap entries" sentence applied.
2. Blocking: the push-only-that-commit sentences added at the end of Detail D4.
3. Agrees with usual findings 1 and 3; applied as above.
4. Non-blocking: S4 replaced (see usual 2).
5. For the Maintainer: new test modules or a `conftest.py` under `tests/fixtures/` still run unscanned. No change; Strategy carries it to the Maintainer through `dev/PLANNING.md`.
6. Non-blocking: Detail D3's `..` node writes its `file=` with the host's path separator.

**Disposition**: ready-to-implement

**Not checked**: no code or test was run. The roadmap edits in `dev/PLANNING.md` are Strategy's and are not made here. The two edits the "Owners" paragraph names must be committed before archive.

Elapsed about 10 minutes; tokens unknown.

## Implementation record -- Claude Haiku 5.5 (Implementation, Low) -- 2026-11-20

BASE: ecc1a913. Status left at implementing.

Commits: 29121797 Step 0 (header); 9c20accb D1-1 (new-file scan, one node); b2286566 D1-2 (record number asserted); 8feca392 D1-3 (_report_file, one changed line, four nodes); c9220e61 D1-4 (one paragraph).

Nodes (this Windows host):
- D1-1 new node: fails before and after with "the ssh-keygen path /usr/bin/ssh-keygen is not absolute". Every test using this helper fails the same way here, so the scan is not exercised; the Mac run is the check.
- D1-2 node: BASE refusal holds "record <n>:", so no stop. 6 of 6 pass after.
- D1-3 Windows node: "invalid test-file identity" before, passes after. The other-file and ".." nodes fail before (the same backslash refusal) and pass after. The off-Windows node is skipped here.

Probes (undone): D1-1 tests/ excluded: host message, inconclusive. D1-2 number + 1: fails. D1-2 hostile src on record 1, planted record valid: fails (scratch copy). D1-3 _report_file values: as Detail says.

Whole files, against BASE:
- test_ceremony_review_report.py: 75 failed, 1 passed; BASE 74 and 1. The extra id is the new node; all host messages.
- test_fork_advisory.py: 2 failed, 12 passed; BASE 3 and 11. The two symlink cases are WinError 1314 on both. BASE's extra failure (test_node11) passed on repeat.
- test_release_members_contract.py: 8 or 9 failed; BASE 8. The extra id, test_minimal_report_passes, is timing and failed once at BASE too.

Differences from the plan: none in code. The planted record is the last in the lock, so D1-2 probe 2 put the hostile src on record 1.

Not run: the other selected files (test_gate_preflight, test_gate_reanchor, test_oracle_activation, test_reanchor, test_reanchor_driver_disclosures, test_repin, test_repin_ceremony, test_security_marker); the Mac run; any freeze, record, join or signing. Not confirmed here: the D1-1 node and the D1-3 off-Windows node.

Elapsed about 20 minutes (18:55 to 19:15, host clock). Tokens: unknown.

## Coordinator verification -- Claude Fable 5.2 (Strategy) -- 2026-11-20

The four chunks match Detail. The tests that cannot run on the Windows Server host ran in its Linux subsystem (Ubuntu, Python 3.14.4): a development check, not the canonical runtime.

- **One defect found and fixed** (`52cc8095`, under the rule for a cheap defect fix). On Linux, three of D1-3's new nodes failed with "report is stale" before reaching their own check. The `evidence` fixture read the clock and then wrote the report; a file system stamps a new file from a coarser clock, which read earlier than the clock on 200 of 200 new files on Linux (by up to 4.7 ms) and on 129 of 200 on Windows (up to 0.7 ms), measured. `test_minimal_report_passes` failed the same way on Linux at the starting commit; on Windows this is the "timing flake" on the roadmap. The fixture now takes the start from the report's own time. The checker is unchanged.
- **Linux.** The four edited test files: 257 passed, 2 skipped. D1-1's control: with `tests/_gate_preflight.py` put back to the starting commit the new node fails (it finds no hit in the two tool files); with the change it passes. D1-1's nine selected files: the same 120 failures by id and message before and after, all in the signing tests, and one more pass, the new node.
- **Windows Server host.** D1-1's nine files: 372 failed and 156 errors before; after, the only new failing id is the new node, which cannot run here (`the ssh-keygen path /usr/bin/ssh-keygen is not absolute`). D1-2's file: the same 2 failures. D1-3's two files, after the fixture fix: 8 failed against 9, none new; `test_minimal_report_passes` failed before and passes now.

Not run: the Mac. Home: `dev/PLANNING.md`, "Waiting on you", the Mac session's second job. Not run: any freeze, record, join or signing. Found on the way and listed for plan D2 in `dev/PLANNING.md`, section 1, "Windows", items (g) to (j) (committed on `0.9-dev` at `f9c02db2`, so not in this branch's copy until the merge): the fixture race, a refusal test that asserts only "FAIL", stray files the ceremony tests leave on Windows, and an unstable gauge test file.

**Elapsed**: 53 minutes from the implementer's record (19:16) to this one, most of it test runs. **Tokens**: unknown.

## Code review -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-20

Reviewed commit: 1e729c4ee4c91928e0d1fd944b0c7f1cf076f88c; range `ecc1a913..HEAD` on `arc-d-impl`.

**Obligation**: the usual code review the heavy tier requires; the Security Review pass follows.
**Findings**: none blocking, three non-blocking.

The change gives the review page back a scan of new tool files under `tests/`, makes one test name the record it refuses, lets the release checker read pytest's Windows `file=` spelling, and writes down the clean-clone freeze. All four chunks match Detail word for word: the code blocks, the node names and cases, the one changed checker line, the docstring lines, and the single inserted paragraph (`git diff` shows one added line in `release/RELEASE_PROCESS.md`; the `bash` block is untouched).

**Foundations**

1. **Should this happen as framed?** Yes. It scans more and accepts nothing new except, on Windows, one spelling of a field that `compare` still checks against the classname. -- `tests/_gate_preflight.py:1450-1454`, `release/check_release_test_members.py:240` and `:281`
2. **Best alternative.** For the fixture fix, keep `time.time_ns()` and stamp the report with `os.utime`, as the file's other helper does (finding 2). Otherwise none simpler. -- `tests/contract/test_release_members_contract.py:418`
3. **What would show it wrong.** I tried names near the edge on the `_is_test_module` rule and the `tests/fixtures/` exclusion; `conftest.py`, `Test_a.py`, `tests_tool.py`, `test_a.pyi`, `test_a.sh`, and a `run.py` in a folder named `test_data` or `Fixtures` are all scanned; `test_*.py` at any depth and `tests/fixtures/` (any file) are not, as designed. A rename is `modified`, not `added`, so it is never new-file scanned, as before. I also ran the D1-3 nodes and the fork-advisory node here. -- `C:\ProgramData\Anaconda3\python.exe -m pytest tests/contract/test_release_members_contract.py -k "file_field or minimal_report or test_report_refusals"`: 26 passed, 1 skipped (the off-Windows node), 1 failed (symlink, host privilege, fails at BASE); `tests/test_fork_advisory.py -k node16_f5_parametric_no_lockfile`: 6 passed.

**Findings**

1. Non-blocking. D1-1's node cannot run on this host (record: `ssh-keygen` path). Its control ran only in the Linux subsystem; the Mac run is open and has a home in `dev/PLANNING.md`, "Waiting on you". I did not run it.
2. Non-blocking, advice. The `evidence` fixture fix is within the cheap defect rule: it restores a promise in an edited file (`test_minimal_report_passes`), adds no file or name, and carries the `Defect fix:` line. The "stale" case still stamps the report one nanosecond before the start (`:194`), and "future" is unchanged, so both refusals are still tested. Taking the start from the report's own time cannot make a checker that ignores or inverts the start comparison pass: a `<=` mistake fails the minimal report, and an ignored start fails "stale". Safer form, not required: keep `time.time_ns()` and `os.utime` the report just after writing it. Then the start does not depend on the file system clock.
3. Non-blocking. A new `conftest.py` under `tests/fixtures/` still runs unscanned; the plan reviews already sent this to the Maintainer.

**Removed caller-visible faults?** None; the fork-advisory assertion only gains a line, and no test is removed. **Permanent tests worth their runtime?** Yes: four small contract nodes, one range-report node, one added assertion; no probe was left. **Does any rule weaken or disappear?** No; the paragraph adds a rule and the checker still refuses backslashes everywhere except that one Windows field.

**Not covered**: the Mac and Linux runs, and the other seven D1-1 files; any freeze, join or signing. Whether the paragraph's statements are true of `release/security_check.py` is left to the Security Review. **Bounding**: no protected, frozen or fixture file beyond the two frozen files and two roster tests the plan names is touched, and no manifest is refreshed. Elapsed: unknown. Tokens: unknown.

**Verdict**: APPROVE

## Code review -- Claude Opus 5.5 (Security Review) -- 2026-11-20

```
Reviewed commit: 4cf6af350c90579cbf699c4d66b6979bf0203f4c
```

Range `ecc1a913..HEAD` on `arc-d-impl`; the code is unchanged since `52cc8095`.

**Obligation**: the Security Review the heavy tier adds at the code stage.
**Findings**: none blocking, three non-blocking.

The change puts new tool files under `tests/` back on the review page, makes one refusal test name its record, lets the checker read pytest's Windows `file=` spelling, and writes down a clean-clone freeze. Nothing in it accepts a case the checker refused before for another file.

**Foundations**

1. **Should this happen as framed?** Yes. On Windows, every spelling that newly passes (`tests\x.py`, an absolute path in the checkout, a case, trailing-dot or `::$DATA` variant) already passed with forward slashes and resolves to the classname's file; another file, `..`, `\?\`, drive-relative and root-relative spellings are refused. The classname stays the authority. -- `release/check_release_test_members.py:57-74`, `:281`; direct calls of `_file(_report_file(...))` on this host
2. **Best alternative.** None safer for the scope. -- `tests/_gate_preflight.py:1350-1354`
3. **What would show it wrong.** I tried 19 names against the scan rule and 16 `file=` spellings, both hosts' branches, and ran the D1-3, minimal, stale and future nodes: 7 passed, 1 skipped (off-Windows node). -- `python -m pytest tests/contract/test_release_members_contract.py -k "file_field or dotdot or minimal_report or stale or future"`

**Findings**

1. I agree with the usual review's three findings. On the fixture fix: it is within the cheap-fix rule and strengthens the file. Before it, on Linux every `test_report_refusals` case could pass on "stale", since that test asserts only `FAIL`; now each reaches its own check, and "stale" and "future" are still refused.
2. Non-blocking; my words govern over the usual review's Foundations 3. A rename is not `modified`: the range is read with `--no-renames` (`tests/_gate_preflight.py:1207`) and `_scan_range` keys on path (`:1446-1448`), so the new name is `added` and scanned. The error points the safe way.
3. Non-blocking, for the Maintainer, older than D1. An added `Tests/conftest.py` (any case variant of a root) is not scanned; on a case-insensitive checkout (the Mac's default, Windows) it lands in `tests/` and runs at collection. It is still named on the page by class.
4. Non-blocking, older than D1. On Windows a `file=` naming a network share (`//host/share/x.py`, possible before D1) is resolved before it is refused, so the checker may contact that host. The report's author is test code already running there, so no new exposure. Fix later: refuse a leading `//` before `resolve`.

**Paragraph.** Each statement holds against `release/security_check.py`: the peel refusal (`:2094-2098`), the join's location and ref comparison (`:2606-2611`), the Windows record comparing refs only in the frozen checkout (`:2459-2462`), and `PASS` naming one commit (`:2639`, `:2648`). The anchor sentence matches `dev/rules/protected-surfaces.md:37-38`. **Does any rule weaken or disappear?** No. **Removed caller-visible faults?** None removed. **Permanent tests worth their runtime?** Yes; no probe left. Security S1 to S5 hold as built.

**Waiting-line check**: no fenced chunk in the range. **Bounding**: ACCEPTED; no protected, frozen or fixture file beyond the plan's four is touched, and no manifest is refreshed.

**Not covered**: the D1-1 node (cannot run here) and its Mac run; the other D1-1 files; any freeze, join or signing; whether `git clone` leaves tree refs out. About 520 words: two findings correct the record. Elapsed: unknown. Tokens: unknown.

**Verdict**: APPROVE

## Code-review response -- Claude Fable 5.2 (Strategy, acting as implementer) -- 2026-11-20

Strategy coordinated this plan and answers; the implementing session (Claude Haiku 5.5) had ended. Neither code review raised a blocking finding, and no code changed after the reviews.

Usual review:

- **1, the new D1-1 node cannot run on the Windows host: no change.** It ran in the Linux subsystem (coordinator's record). The Mac run stays open. Home: `dev/PLANNING.md`, "Waiting on you", the Mac session's second job.
- **2, another form for the fixture fix: declined.** Stamping the report inside the fixture, as the file's other helper does, would not hold for D1-3's nodes: they rewrite the report after the fixture returns, and the rewrite takes a fresh stamp from the coarse clock. Taking the start from the report's own time also covers a rewrite.
- **3, a `conftest.py` under `tests/fixtures/` is not scanned: no change.** Already with the Maintainer (`dev/PLANNING.md`, section 1, "Narrowings from the layout move").

Security Review:

- **1: agreed.**
- **2, renames: that review corrects the record.** A renamed file shows as added and is scanned. No change.
- **3 and 4: queued for plan D2.** A root spelled with other capitals (`Tests/conftest.py`) is not line-scanned, and on Windows a `file=` value that names a network share is resolved before it is refused. Both are older than D1. By the security strategy's test for a new finding (`dev/strategy/2026-08-05-codex-security-strategy.md`, "Decision test for new security findings") they are queued on the roadmap for the next batch on the same boundary, which is plan D2. Neither is reproduced on the canonical runtime yet. Home: `dev/PLANNING.md` on `0.9-dev`, section 1, "Narrowings from the layout move" and "Windows", item (k).

Both reviews wrote the verdict as APPROVE where the skeleton's word is ACCEPT; the meaning is the same.

**Elapsed**: under ten minutes after the Security Review's commit (20:14 on the host clock). **Tokens**: unknown.

## Implementation closeout -- Claude Fable 5.2 (Strategy) -- 2026-11-20

Every criterion held; one could be shown only off Windows. D1-1: the restored scan matches Detail. Its new node passes in the Linux subsystem and fails there when the scan file is put back to the starting commit; it cannot run on the Windows host. D1-2: the node asserts the record's number and passes (6 of 6 on Windows). D1-3: the Windows node fails before the change and passes after, on Windows; the other three nodes pass in the Linux subsystem. D1-4: one paragraph inserted and the `bash` block untouched; both code reviews read it against `release/security_check.py`. One cheap defect fix rode along (`52cc8095`, the contract fixture's race with the file system's clock). The branch, 11 commits changing 7 files, merged into `0.9-dev` at `5642228e` with no conflict.

Not run: the Mac run of D1-1's nine files. Home: `dev/PLANNING.md`, "Waiting on you", the Mac session's second job.
Not run: anything on the canonical runtime; the new scan node and the off-Windows contract node passed only under Python 3.14.4 in the Linux subsystem. Home: `dev/PLANNING.md`, section 1, "What the joined run owes".
Not run: a freeze from a fresh clone carried through to a join. Home: `dev/PLANNING.md`, section 1, "The history freeze in a live repository".
Not covered: the v0.9 signing page, which shows the last signed version's own scan; six new files are not on it. Home: `dev/PLANNING.md`, section 1, "Narrowings from the layout move", and its row under "Waiting on you".
Remaining: plan D2, the Windows measurements and repairs, with the four test defects and the two older security findings found here. Home: `dev/PLANNING.md`, section 1, "Windows" (the measuring list and items (g) to (k)) and "Narrowings from the layout move".
Remaining: two HOLD lines at the signing, for `tests/_gate_preflight.py` and `release/check_release_test_members.py`; the gate manifest is regenerated there. Home: `dev/PLANNING.md`, section 1, "The re-anchor".

Dispositions: no follow-up of this plan is deferred without a home above. The two older security findings are not this plan's follow-ups: they are new findings, queued by the security strategy's rule and reported to the Maintainer at this milestone.

**Benefit versus cost**: unknown -- from the first signing after v0.9's, a new tool file under `tests/` is back on the Maintainer's review page, and the release check reads Windows test reports; cost: 11 commits and one merge, four review passes with no return visit, 1,071,086 subagent tokens in seven runs as the harness reported them (Strategy's own use is unknown), and about an hour of machine time for tests on two hosts; remaining burden: one small function in each of two gate files and five test nodes. Revisit at the D6 recount at the end of v0.9.

**Elapsed**: 1 hour 54 minutes from the plan's opening (18:24) to the merge (20:18), by commit times. **Tokens**: unknown beyond the subagent figure above.
