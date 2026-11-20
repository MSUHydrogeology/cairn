# Plan: Defect arc D1, gate narrowings and release control

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: Win back two checks that the 0.8 file move weakened, let the release check read Windows test-report paths, and write down how to freeze history from a fresh clone; the older Windows test failures wait for a second plan that measures them on the Windows host first.

## Build summary

After this plan, the ceremony's review page again shows the lines a new tool file adds under `tests/`, from the first signing after v0.9's, the fork-advisory test again tells which lock record a refusal names, the release membership check reads the backslash paths pytest writes on Windows, and the release process says to freeze history from a fresh clone. Four chunks. The older Windows failures, the Windows tag check and the signing-ceremony tests go to a second plan, D2, because each needs a Windows measurement first.

## Source proposal

The Maintainer accepted the defect arc at the heavy tier ("Go ahead on the defect arc.", chat, 2026-11-20). Plan D is its gate-and-Windows part. Reviewers called it full, so it is cut in two; this is D1, the items that need no measuring. Exact code, texts and fixtures are in the companion `dev/plans/2026-11-20-defect-arc-d-gate-and-windows-checks-detail.md` ("Detail"), part of this plan: it exists because they would double its length, and a low-tier implementer must not invent them. The plan reopens nothing.

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
