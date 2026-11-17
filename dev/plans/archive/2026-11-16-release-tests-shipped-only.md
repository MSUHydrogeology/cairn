# Plan: Release tests cover only what ships

**Source proposal**: dev/proposals/archive/2026-11-16-claude-release-tests-shipped-only.md
**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`, Medium), plan author
**Status**: archived
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: The strict release check stops re-running 16 test files that cover only the Maintainer's own signing tools, saves about 30% of its time, and says in its output which files it left out.

## Build summary

After this plan the strict release check (`bootstrap/security_check.py --record`, then `--join`) runs every test that touches what adopters receive or run, and leaves out 16 test files (1,020 tests) that examine only Cairn's own re-anchor, oracle and quality-gate tools. The check refuses any record that does not name exactly the reviewed list. The join's `PASS` line says "shipped-only" and prints a `NOT CERTIFIED` block (the names, the count, "run when their own files change") for the release notes. Certifying runs and every other run keep all tests. `test_ast_attest`, `test_quality_gate_neutrality` and `test_security_check` stay in the release run. The work edits six signed files, one contract test and two public documents; the Maintainer's one re-anchor follows.

## Source proposal

The accepted heavy proposal (Decision 2026-11-16, "Let's accept all five as revised") adopts the 16-file split (measured in the 2026-11-12 run: 1,020 of 5,413 tests, 878 of 2,938 case-seconds), runs it before the repository layout, makes the one re-anchor the only human operation, and leaves the 28 kept guard tests to this plan.

## Scope

**Branch and order.** This plan is a document, committed on `master`. Every chunk lands on `0.8-dev` (`dev/PLANNING.md` > Working rules), created from `master` when v0.8 group 1 is done; it does not exist yet (`git branch --list '0.8*'` printed nothing), and no chunk starts before it does. This plan reaches `ready-to-archive` before the layout plan's first chunk (the Decision).

**Frozen files** (`frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json`, measured): `bootstrap/security_check.py`, `scripts/quality_gate.py`, and in `bootstrap/tests/` `security_manifest.py`, `conftest.py`, `test_security_marker.py`, `test_security_check.py`. `contract/test_release_members_contract.py` is an ordinary hashed test; `docs/release-process.md` and `SECURITY.md` are not hashed. All frozen edits are in C1 to C4 (C5 has none), so one ceremony covers them. An implementer never edits `gate_manifest.json`, `protected_test_roster.json` or the two `scaffold_ast_*.json` files, never runs `bootstrap/reanchor.sh`, never signs; `python scripts/repin.py status` reads only and is allowed. The re-anchor is the Maintainer's, a standalone board wait the coordinator opens, not a chunk.

**Settled design.** A Low-tier implementer decides none of it.
1. **List.** `security_manifest.py` gains, above the `NATIVE_ONLY_NODE_IDS` block (the connected fixture edits text below it): `RELEASE_EXCLUDED_TESTS`, a tuple of rows `(path, subjects, reason)` (rows, so a duplicate stays visible); `RELEASE_REQUIRED_FILES`, a frozenset of the 11 must-stay paths below; and `release_excluded_files()`, which returns the paths as a frozenset. It raises `ValueError` (message free) unless the list is a tuple of 3-tuples whose path matches `\Abootstrap/tests/(?:[A-Za-z0-9_]+/)*test_[A-Za-z0-9_]+\.py\Z`, whose `subjects` are a non-empty tuple of non-empty strings and whose reason is a non-empty string; and on a duplicate path, a path whose last segment is a key of `SECURITY_FAMILY`, or a path in `RELEASE_REQUIRED_FILES`. `()` is valid: the empty set (whole suite).
2. **Hook.** `pytest_ignore_collect(collection_path, config)` in `conftest.py` (under `@_own`) returns `True` for a listed path (relative to the repository root, `/`-separated), else `None`, only when `_NATIVE_RUN_CONTEXT is not None`. That is the parsed strict pair: `_initialize_native_run_context` needs `CAIRN_RELEASE_GATE_ACTIVE=1` and then pops the five `CAIRN_NATIVE_RUN_*` variables, so the hook reads that state, not `os.environ`. `CAIRN_FULL_SUITE` is never read. `_initialize_native_run_context` loads the set once, after it sets the context, into `_RELEASE_EXCLUDED_PATHS` (default `frozenset()`) from `release_excluded_files()` (no accessor: empty; a `ValueError`: `pytest.UsageError`). The hook compares by exact string equality, never a prefix or a name. Measured (pytest 9.0.3, scratch tree): a directory argument drops an ignored file, an explicit file argument does not, so a hand-named file still runs.
3. **Record.** Key `excluded` = `{"files": sorted list, "count": int}`. `security_check.py` sets `_RELEASE_EXCLUDED = release_excluded_files()` beside `_NATIVE_POLICY`, imported beside `validated_native_only_nodes`. `_measure_excluded_tests(root)` returns the mapping. An empty list gives `{"files": [], "count": 0}` and runs no pytest. Otherwise it runs `pytest --collect-only -q` over the listed paths only (with no file argument pytest collects everything) in `root`, using `_release_child_env()` minus the release token and the `CAIRN_NATIVE_RUN_*` variables (it keeps the no-bytecode and no-cache settings that keep the checkout byte-exact). Each listed path's count is its output lines that start with that path and `::`; the warning and summary lines are ignored. It raises `ValueError` on a nonzero exit or a listed path with no such line; the count is the sum. `_run_bound_phases` calls it and passes the result to `_build_local_record`, which gains an `excluded` argument. `_validate_local_record` requires the key, `files == sorted(_RELEASE_EXCLUDED)`, `type(count) is int`, `count >= len(files)`, `count == 0` only when `files` is empty, and no order that collected an ID in a listed file.
4. **Join.** `_tracked_test_files(head)` returns the paths in `_committed_blobs(CAIRN_ROOT, head)` (git at `HEAD`; pytest output cannot see an ignored file) that are under `bootstrap/tests/` and named `test_*.py` or `*_test.py`. After its existing checks `_join_local_records` refuses unless the two records' `excluded` agree (list and count), `_RELEASE_EXCLUDED` (the `HEAD` manifest: the join runs in a clean checkout of `HEAD`) is a subset of the tracked files, and each order's collected files (the part of each ID before `::`) equal the tracked files minus `_RELEASE_EXCLUDED`. It returns the `excluded` mapping; `_run_join` prints, after its postflight, the lines below. With an empty list it prints the existing `PASS` line and no block. Output with a list: `security_check: PASS (shipped-only) -- Mac and Windows evidence joined at <head>.`, then `NOT CERTIFIED (shipped-only release selection): <N> tests in <M> files were not run. They run when their own files change.` and the sorted names, two-space indent.
5. **Roster.** Delete the 365 rows of the five Cairn-side files that carry any (all POSIX, measured), leaving 348: 63 Windows, 285 POSIX. Otherwise the record would demand IDs it no longer collects. Update the count guard and `NATIVE_ONLY_POLICY_ID` (expected `sha256:02eb75b23f6856debcdacc9a15461a4e536606d3471983eaeacdfc7c05c5aab8`; recompute). A consequence the proposal did not state: run directly on Windows, those five files no longer skip their POSIX-only cases. Assumed, not measured: nobody runs them there. The VM runs file subsets (`dev/rules/development-environment.md`), and a subset run of them would now execute 365 POSIX-only cases; the coordinator tells the Maintainer at the re-anchor.

**The 16 files** (under `bootstrap/tests/`) and the subject paths the selector must reach each from: `test_repin.py`, `test_repin_ceremony.py` from `scripts/repin.py`; `test_reanchor.py`, `test_reanchor_driver_disclosures.py` from `bootstrap/reanchor.sh`; `test_gate_reanchor.py`, `test_gate_preflight.py`, `test_gate_manifest.py`, `test_gate_transition.py`, `test_oracle.py`, `test_oracle_activation.py`, `test_oracle_trust.py` each from the `_`-prefixed helper of the same name in `bootstrap/tests/`; `test_ceremony_review_report.py` from `_gate_preflight.py`; `security/test_check_release_publication.py` from `scripts/check_release_publication.py`; `test_quality_gate_cli.py`, `test_quality_gate_order_independence.py`, `integration/test_quality_gate_redundancy.py` from `scripts/quality_gate.py`. Each reason reads "Tests <subject>, which only Cairn's Maintainer runs; none of it is in the install manifest." (measured: `scaffold.py --manifest` names none of these subjects). Must stay (`RELEASE_REQUIRED_FILES`: each `bootstrap/tests/<name>.py`, the contract test under `contract/`; pinned in a test): `test_ast_attest`, `test_quality_gate_neutrality`, `test_security_check`, `test_security_marker`, `contract/test_release_members_contract`, `test_session_binding_gate_and_printing_hold`, `test_manifest`, `test_verify_integrity`, `test_verify_ref`, `test_security_lint`, `test_loop_fidelity_gate`.

**Security Review requirements and their proof.** Keep the 11 must-stay files in the run, refused by exact path if listed: C1 T2 and T5, and C2's real-tree test. Key on the strict pair, never `CAIRN_FULL_SUITE`: C2 cases 2 and 3. Certifying and standalone runs keep all tests: C2 case 3. The join checks tracked files at `HEAD` and counts from that tree: C3, C4. An empty list measures nothing and prints no block; a listed file with no tests refuses the record: C3, C4. `PASS` says "shipped-only" and `SECURITY.md` is corrected: C4, C5. Contract pin 18 to 15 and docstring wording: C1, C2.

**Non-work** (each with its reason).
- The 28 kept guard tests: none retired. The Decision's default is no fold, and no list of the 28 is in the tree, so which sit in Cairn-side files is unchecked. The board row stays the Maintainer's.
- `prep/windows-roster-refresh`: revived later, it drops the same five files' rows (its own work).
- `dev/rules/certifying-runs.md`: unchanged by the Decision; the certifying pair runs everything.
- `scripts/check_release_test_members.py` and the first bash block of `docs/release-process.md`: the block names neither strict variable, so it keeps the whole selection; the family shrinks by itself.
- Other Cairn-only dev-script tests (not classified in the proposal), layout renames (the layout plan), engine, AST baseline, `tools/test_tiers.py`: not this change.
- A whole-suite run: forbidden. CHANGELOG entries, `dev/PLANNING.md`, archiving the proposal: the coordinator at closeout, never implementers.

**Reuse.** Reused: `_security_manifest_module`, `_own`, `_initialize_native_run_context`, `validated_native_only_nodes` (the model for the accessor), `_committed_blobs`, `_synthetic_local_record`, `_connected_runner_fixture`, `_native_child_pytest`, `_collect`, `tests_for_paths`. Searched `git grep -E 'pytest_ignore_collect|collect_ignore|--ignore'` over `bootstrap scripts tools`: no collection hook exists; `--ignore` appears only in the gate's own tests.

### Documentation / doctrine surface

Descriptive layer only: `docs/release-process.md` and `SECURITY.md` (a public security claim). No governing text; nothing shipped to adopters.

## Sequence

Estimate 14 to 18 Low-tier agent-hours over two elapsed days (a guess). Uncertain: other sessions' edits to the same files.

**Every chunk.** A Low-tier implementer (`AGENTS.md`); name the model at spawn. Work on `0.8-dev`. Claim the exact paths. Read `git status` and `git log -5` for each file at the start; another session's uncommitted edit stops you, never commit it. Write the failing test, see the stated failure, then change. Prose by exact replacement. Run the named public controls and focused checks with `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest`; tests that read `HEAD` (the connected fixture runs `git archive HEAD`) run after you commit; if one is red, fix it in a second commit for the same chunk. If `python tools/test_tiers.py` (or T3, or `contract/test_test_tiers.py`) fails with `git-read-binding-failed`, another session has an uncommitted edit to `tools/git_read.py`: wait, do not fix. One commit per chunk, explicit paths, no push. If the code differs from the chunk, stop and report.

**Shared files.** `docs/release-process.md` is also edited by the accepted heavy-tier-trigger proposal (one place, the Security Review trigger line); C5 edits other passages and re-reads first. The staged-modules proposal edits none of these files; the template-trim proposal names `security_manifest.py` only as a protected exemption and may delete tests that pin template wording, so every chunk re-reads status for its test files. The meter plan and the paused Windows refresh read or edit `security_manifest.py` rows; C1 re-reads the roster.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | List, family, roster, pins | `0.8-dev` exists; plan reviews | `security_manifest.py`, 3 test files, 5 tests |
| C2 | Collection hook | C1 | `conftest.py`, `quality_gate.py` comment, 6 tests |
| C3 | Record side | C2 | `security_check.py`, 9 join cases, measurement test, connected test |
| C4 | Join side | C3 | `security_check.py`, 9 tests |
| C5 | Documents and joined check | C4 | 2 documents, evidence in the commit |

**Red until the re-anchor** (expected, not pass criteria). After C4, the last chunk that edits a frozen file, `python scripts/repin.py status` lists six more `FROZEN-MODIFIED` files (the six above) and no other; record it before C1 and after C4. The re-anchor opens after C5 and its code review. Five parametrized IDs leave the collection (C1). The engine pin is already owed (`repin.py status`: six CHANGED symbols), so `test_ast_attest` is expected red; its baseline is not touched here.

Length (counted after the plan review): Build summary, Source, Scope, Sequence and Verification run about 2,200 words against 1,000. Acceptance runs about 1,230: 290 for C1, 210 to 225 for each of C2 to C4, 270 for C5 (the exact public wording). The overrun is the settled design (about 640 words), the 16-file list (about 100), that wording, and the design the two plan reviews found missing (named in the Plan response). A Low-tier executor cannot decide any of it, and a reviewer must check it.

## Acceptance criteria

**C1 -- list, family, roster, pins.**
- Before any edit save outside the repo `before-plain.txt` from `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests --collect-only -q -p no:cacheprovider`, keeping only lines that start `bootstrap/tests/` and contain `::`, sorted under `LC_ALL=C` (the raw output also holds warning and summary lines). It held 5,533 IDs at the Internal review and 5,592 on 2026-11-16, about 4 s; the figure moves with other sessions' commits, so record yours.
- New tests in `test_security_marker.py`, each seen failing first: T1 `release_excluded_files()` on the real manifest equals a pinned copy of the 16 paths; T2 `RELEASE_REQUIRED_FILES` equals a pinned copy of the 11 paths, and every required and every listed path is tracked; T3 `tests_for_paths` (loaded as `contract/test_test_tiers.py` does) selects each file from every subject path; T4 no roster row names a listed file; T5 one parametrized test, a case per refusal in Settled design 1, each setting `RELEASE_EXCLUDED_TESTS` on a fresh `_manifest()` module and raising `ValueError`: not a tuple; a two-item row; a non-string path; an absolute path; a `..` path; a backslash path; a directory; a helper `_x.py`; `scripts/repin.py`; empty subjects; subjects not a tuple; an empty reason; a duplicate row; `bootstrap/tests/test_security_leaf.py` (a family name); `bootstrap/tests/test_security_marker.py` (a required path). Controls: one valid row returns its path; `()` returns the empty set.
- `_REVIEWED_MEMBERS` loses the three; family pin and roster identity tests pass; `GATE_INTEGRITY_MEMBERS` keeps only `test_ast_attest.py`; the contract test expects "15 required files" and "14 passed"; the `_connected_runner_fixture` count guard expects 63 and 285. The "seventeen" and "entire suite" wording in `security_manifest.py` and the `test_security_marker.py` promise line says shipped-only.
- After the edits make `after-plain.txt` the same way. `comm -23 before-plain.txt after-plain.txt` prints exactly five lines, all `test_join_refuses_each_native_identity_missing_from_all_host_orders[...]` IDs, named in the commit message; any other line stops the chunk (report it).

**C2 -- collection hook.**
- Tests first in `test_security_check.py` beside `test_native_context_writes_external_report_for_actual_order`, copying its environment setup (release token, the five `CAIRN_NATIVE_RUN_*` values, the external `report_dir`). Fixture manifest: the copied real one plus one appended line, `RELEASE_EXCLUDED_TESTS = (("bootstrap/tests/test_fixture_excluded.py", ("scripts/x.py",), "Fixture."),)`, and that file holding a failing test. (1) Strict pair, both orders: the file is absent from `collection_input_ids` and `collected_ids`, others present, exit 0. (2) Same with `CAIRN_FULL_SUITE=1` exported: identical IDs. (3) Release token alone, `CAIRN_FULL_SUITE=1` alone (what the certifying pair and a standalone `quality_gate.py` run set), neither (each with `--collect-only`): file collected. (4) Strict pair with the appended line `RELEASE_EXCLUDED_TESTS = ()` and `--collect-only`: file collected, exit 0. (5) Strict pair with a malformed appended list (`"/x.py"` as the path): nonzero exit.
- One test in `test_security_marker.py` (`_collect` gains an env argument, filled as the test above fills it with the policy id from `_manifest().NATIVE_ONLY_POLICY_ID` and a report folder outside the repository; skip off Mac and Windows): on the real tree the strict-pair IDs equal the plain IDs minus every ID in a listed file; the removed files are exactly the 16; the 11 `RELEASE_REQUIRED_FILES` are present.
- `conftest.py`'s "seventeen" docstring and marker text say shipped-only. `quality_gate.py` gets a comment only (the child inherits the pair; its `CAIRN_FULL_SUITE` must stay irrelevant).

**C3 -- record side.**
- `_synthetic_local_record` gains an `excluded` keyword (default `{"files": sorted(security_check._RELEASE_EXCLUDED), "count": 1020}`). Faults added to `test_join_main_refuses_mutated_native_records`, each refused: no `excluded`; a listed name missing; a shipped file added; count zero with a non-empty list; count a boolean; count below the number of files; an order that collected a listed file. With `_RELEASE_EXCLUDED` patched to `frozenset()`: `{"files": [], "count": 0}` is accepted and `{"files": [], "count": 1}` is refused.
- `_measure_excluded_tests`, `_build_local_record` and `_validate_local_record` as Settled design 3. One direct test of `_measure_excluded_tests` on a scratch tree, with `_RELEASE_EXCLUDED` patched, under a `# Declared exception (internal hook): ...` comment (no public route reaches it without a whole `--record` run). Cases: one file with two tests gives that path and 2; `frozenset()` gives `{"files": [], "count": 0}` and calls no subprocess; a listed file with no tests beside one with tests refuses (exit 0, so only the per-file rule catches it); a listed file with a syntax error refuses; a listed path that is not a file refuses.
- Connected test: the fixture manifest gets the appended list naming a fixture file with two tests, one failing; the test sets `security_check._RELEASE_EXCLUDED` to match. `--record` exits 5, `excluded` is that file and 2, and neither order collected it.
- The module docstring's phase 3 and 4 lines, the `run_suite` docstring and its printed line say shipped-only. `test_security_lint.py` passes.

**C4 -- join side.**
- `_tracked_test_files(head)` on a temporary repository returns only test files under `bootstrap/tests/` (a deep one, a `*_test.py` one, a helper, a fixture file, one under `docs/`). Its test carries a `# Declared exception (internal hook): ...` comment, as the file's other private-hook tests do; it is the only check of the filter.
- A helper `_track_synthetic_files(monkeypatch)` in `test_security_check.py` patches `security_check._tracked_test_files` to return the files of the synthetic record's IDs plus `_RELEASE_EXCLUDED`, computed when it is called (before a test patches the roster). Every existing `--join` test that does not use the real repository calls it (`git grep -n '"--join"' bootstrap/tests/test_security_check.py`; `test_public_join_accepts_real_git_object_formats` is one: its repository holds no test files); the connected test uses the real function.
- New tests through `main(["--join", ...])`: matching records exit 0 with the `PASS (shipped-only)` line and the block (16 sorted names, count, sentence). Refused: `_RELEASE_EXCLUDED` minus one name (negative control); a tracked test file neither collected nor listed; a collected file not tracked; a listed file not tracked; counts that differ. With `_RELEASE_EXCLUDED` patched to `frozenset()`: matching records exit 0 with the plain `PASS` line and no `NOT CERTIFIED`; records whose `files` are not empty are refused.
- The connected join builds its counterpart with `excluded=local["excluded"]` (`_synthetic_local_record`'s keyword) and prints the block with the fixture file and 2.

**C5 -- documents, joined check.**
- Exact replacements of the phrases below; every other line keeps its wrapping. `SECURITY.md` item 3: "The full `bootstrap/tests` selection runs in release mode" becomes "The shipped-only `bootstrap/tests` selection runs in release mode: every test except the files in `RELEASE_EXCLUDED_TESTS` (`bootstrap/tests/security_manifest.py`), which the join prints in a `NOT CERTIFIED` block"; item 4: "seed-0 full-suite child" becomes "seed-0 child, which runs the same selection,"; after item 4's paragraph, "Certifying runs before a re-anchor run every test." `docs/release-process.md`: "both full-suite orders" becomes "both orders of the shipped-only selection (every test except the files in `RELEASE_EXCLUDED_TESTS`)"; after "Do not reuse an old report path." add "The first block above names neither strict variable, so it runs every test, including the files the strict run leaves out."; after the paragraph beginning "Only the join can print `PASS`." add "The join also prints a `NOT CERTIFIED` block with the left-out test files, their count and the sentence that they run when their own files change. Paste it into the release notes with the joined output. Certifying runs before a re-anchor (`dev/rules/certifying-runs.md`) still run every test." The first bash block is byte-identical.
- `claim_check.py`, `link_check.py`, `sync_doc_snippets.py --check` on both: no hard flag. `git grep -n -i -E 'full bootstrap/tests|full-suite child|whole engine suite'` over `SECURITY.md docs bootstrap scripts` finds none.
- Run C5's focused checks and record their evidence in this commit; the joined Group 2 integration follows the Verification direction. Make a fresh `after-plain.txt` as in C1; `comm -23 before-plain.txt after-plain.txt` shows only the five IDs (any other line stops the chunk), so the plain run lost nothing else. C2's real-tree test is the proof that the release run lost only the 16 files' tests.

## Scope delta

**Scope delta**: preserved. One lighter mechanism: the proposal lists `scripts/quality_gate.py` as changing, but its seed-0 child inherits the strict pair, so the file gets a comment, and C2 case 1 under seed 0 and C3's connected run prove the outcome. A second: the proposal's Documentation surface names the first bash block of `docs/release-process.md`, but the block stays byte-identical. `contract/test_release_members_contract.py:75` pins its `CAIRN_FULL_SUITE=1` command, and it names neither strict variable, so it runs every test, which is what the Decision keeps for certifying runs; C5 adds the sentence that says so. Nothing is dropped. The 28 guard tests are not in the baseline (the Decision's default is no fold).

## Verification

**Maintainer verification direction** (chat, 2026-11-17): “Please re-write the plans to use focused checks and joined integration.” “Just do focused replacements”. Preserve T1–T5, all named security controls, collection and exclusion contracts, and both before/after collect-only listings; these measure public collection output. No real release record or join is claimed here. Use `python tools/test_tiers.py for <changed paths>` to identify candidate owning families, then select the smallest checks for changed public promises; it does not require running every listed case. Reuse evidence only for unchanged behavior and inputs, and run the prose gates for prose. The arc owner runs one joined Group 2 integration selection after connected plans finish, or earlier at a named critical shared boundary; record the combined revision, checks, results and omissions. Required code reviews remain.

Promises and entry points: `security_check.py --record` and `--join` (C3, C4, the connected test); the conftest hook through real pytest collection (C2); the selector contract and the pinned list (C1). Controls: S1 the list is read from the manifest in the checkout under test; a record's own `excluded` is only checked against it; the tracked set comes from git at `HEAD`, which no pytest hook can change. S2 the negative controls in C1 (T5, the accessor's refusals), C2 (five cases), C3 (seven faults, two empty-list controls, the measurement refusals) and C4 (five refusals, two empty-list cases). S3 the Maintainer's `--record` and `--join`. S4 an empty list (`()`) means the whole suite: `excluded` is `{"files": [], "count": 0}`, no pytest call, the plain `PASS` line, no block; a malformed one refuses. S5 residual: a misclassified file, closed only by review of the 16 pins in T1.

Select focused checks for changed public promises from the candidate families identified by `python tools/test_tiers.py for <the chunk's changed files>`, retaining the named tests and controls. After C5 run `python tools/test_tiers.py check` and compare the before and after plain collect-only lists as in C1.

Not run, so unverified: a real-tree `--record` or `--join` (expectation: the plain count minus 1,020, about 4,570 on 2026-11-16, in about 70% of the time; the Maintainer's release run is the first evidence) and any Windows host. A refusal there returns the plan to `revising-code`.

## Plan review -- Claude Sonnet 5.5 (Plan Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: 8a4b4407c8d69c856705b20c57de92b5064f76f9
```

**Obligation**: Clear that each chunk C1 to C5 can be run by a Low-tier implementer with no design left to them, that the plan delivers every outcome the accepted Decision adopted (none lost, none silently changed), that no required check leaves the release run, and that its order, ownership and ceremony statements are true. This Internal pass does not clear the Internal Security Review.
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 12 minutes (15:48 to 16:00 EST)
**Tokens**: unknown

Strongest case: one list in the signed manifest, one hook keyed on the parsed strict pair, a record that names what it left out and a join that recomputes "tracked files minus the list" at `HEAD` is the smallest design that cannot drop a test silently, and most of the plan is specified to the string.

**Foundations**

1. **Should this happen as framed?** Yes: each adopted outcome has a chunk (16 files, before the layout, three files stay, one re-anchor), and my recomputation matches the plan: the 16 files hold 1,020 tests, the five roster files carry 365 rows (205+102+45+12+1, all `posix`), 348 remain (63 and 285), and the new policy id is the plan's `sha256:02eb75b2...`. -- `bootstrap/tests/security_manifest.py:162-911`, `python tools/test_tiers.py for scripts/repin.py` and the ten other subject paths (each reaches its files)
2. **Best alternative.** Five chunks are about right. One thing to drop: the comment-only edit to the hash-signed (frozen) `scripts/quality_gate.py`, whose seed-0 child already copies the environment; it saves one frozen hash and 8 selected test files per run. The author decides. -- `scripts/quality_gate.py:166-186`
3. **What would show it wrong.** C2's real-tree test failing (strict-pair IDs differing from plain IDs minus the 16 files), or Mac and Windows measuring different excluded counts so every real join refuses. The strict-pair `--collect-only` already runs on the real tree (exit 0, 5,533 IDs). -- `bootstrap/tests/conftest.py:506-552`

1. **Blocking, C1 (returned to author: missing design).** The shape of `RELEASE_EXCLUDED_TESTS` is open. "Maps a path to (subject paths, one reason)" reads as a dict, but a dict silently collapses a duplicate key, so "raises on a duplicate" cannot fire (`NATIVE_ONLY_NODE_IDS` uses rows for this reason). "Malformed" is undefined, yet C2's appended fixture line and case 5 depend on it. Missing decisions: dict or rows, and the exact refusals (path not a `/`-separated relative string under `bootstrap/tests/` ending in `.py`; subjects not a non-empty tuple of strings; empty reason). Closes with the literal type line in Settled design 1 and one test per refusal.
2. **Blocking, C1 and C5 (acceptance cannot pass as written).** `--collect-only -q` also prints a warnings block and a summary line with elapsed time (my listing: 5,542 lines for 5,533 IDs), so `comm -23` cannot show "exactly five IDs". Closes with: keep only lines that start `bootstrap/tests/` and contain `::`, sort under `LC_ALL=C`, state the expected count (five). C2's real-tree test is the proof that no shipped test left the release run; say so in C5.
3. **Non-blocking: the five tree divergences stay inside the Decision, so no Maintainer allowance.** Verified: the 365 rows go and end those five files' Windows skips; `quality_gate.py` needs no code; the first block cannot change, because `bootstrap/tests/contract/test_release_members_contract.py:75` pins its `CAIRN_FULL_SUITE=1` command; no list of the 28 guard tests exists (`dev/PLANNING.md:115` only counts them); `0.8-dev` does not exist; the figure is 5,533 now, 4,513 after. Add the unchanged first block to the Scope delta beside `quality_gate.py`, so accepting the plan covers it; the heavy-tier plan (line 47) still says this plan edits that block.
4. **Non-blocking, C3 and C4: choices a Low-tier agent should not make.** (i) `_RELEASE_EXCLUDED` is used by tests but never defined: say it is `release_excluded_files()` imported beside `validated_native_only_nodes` (`bootstrap/security_check.py:102`). (ii) Say the count is the number of `::` lines (warnings also print). (iii) `_join_local_records` returns 0 and `_run_join` prints `PASS` after the postflight: say the first returns the excluded mapping, the second prints the block after `PASS`, and `_build_local_record` gains `excluded`. (iv) Name the seam helper, and say a red post-commit connected test gets a second commit. (v) C2's real-tree test must build the five `CAIRN_NATIVE_RUN_*` values as `test_native_context_writes_external_report_for_actual_order` does; say so.
5. **Non-blocking, bookkeeping.** C1's Ships row says 2 test files, but the count guard the connected fixture replaces by exact string is in `bootstrap/tests/test_security_check.py:1076-1082`, so C1 edits three (claim it). Name C4 the last frozen-file chunk and say the re-anchor opens after C5 and code review. "Nobody runs them there" is assumed: the VM runs file subsets (`dev/rules/development-environment.md`), and such a run now executes 365 POSIX-only cases; mark it assumed and tell the Maintainer at the re-anchor.
6. **Non-blocking, tests.** Permanent tests use public entries (`main`, real pytest) except C4's direct `_tracked_test_files` test. Keep it, as the only check of the filter, under the file's "Declared exception (internal hook)" comment.

Security, one line, not assessed: the hook keys on the parsed strict pair, never `CAIRN_FULL_SUITE`, and the join recomputes tracked-minus-list at `HEAD`; the Security Review owns both.

**Does any rule weaken or disappear?** Only the release run's coverage, as the Decision adopts, and it is disclosed (`SECURITY.md` items 3 and 4, the join's `NOT CERTIFIED` block); certifying runs keep every test. No governing rule is lost.

**Coverage**: Ran no test, `--record`, `--join` or Windows VM. My read-only measurements: the roster arithmetic and identity, `test_tiers.py for` on each subject, two `--collect-only` listings (plain and strict-pair), `repin.py status`, and a scratch hook probe (pytest 9.0.3 only; the VM's 9.2.0 is unmeasured). Not checked: whether Mac and Windows counts of the 16 files agree, which of the 28 guard tests sit in them, and which tests go red before the re-anchor beyond the plan's list. `HEAD` moved to `530c922e` during the pass; the plan file is unchanged. About 880 words against the 300 target: findings 1 and 2 carry the evidence the author needs to fold them, and 3 to 6 batch small fixes.

## Plan review -- Claude Opus (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 366f90ac2439d455b1ad62dfa0abd6ea750008d9
```

**Obligation**: Internal Security Review: decide whether the shipped-only split could drop a required check from the release run silently, weaken the strict record's honesty, or let an excluded file hide a regression in what ships, and state what C1 to C5 must carry so a Low-tier implementer cannot weaken a protection.
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 5 minutes (16:01 to 16:06 EST)
**Tokens**: unknown

Strongest case: the record already refuses a missing roster ID or an unrostered skip, so the new join check (tracked files at `HEAD` minus the list) closes the one new silent path, the ignore hook.

**Foundations**

1. **Should this happen as framed?** Yes. No excluded file has a shipped subject: `test_oracle` compares `HEAD` with `HEAD` (a harness check), `test_repin` copies `session.py` only as its encoder, `test_gate_manifest` asserts the frozen set. None of the 28 kept guards is in the 16. The roster figures recompute (365 rows out, 63 + 285 left, `sha256:02eb75b2...`). A roster ID not collected refuses the record, and a hook that misses on Windows yields unrostered skips, also refused. -- `655b9a68:dev/measurement/promise-testing-worklist-2026-11-11.csv`; `bootstrap/security_check.py:449` and `:498`
2. **Best alternative.** None simpler. Signed files are left to the Maintainer (Scope, line 22). -- `bootstrap/tests/fixtures/gate_manifest.json`
3. **What would show it wrong.** A tracked test file is neither collected nor listed, yet the join passes. -- C4 refusal test

1. **Blocking, Settled design 1, 3 and S4 contradict.** An empty list "means the whole suite", but a zero count refuses the record, and `pytest --collect-only` with no file arguments collects the whole directory. The result is either a whole-suite release that cannot record, or a record that labels the entire suite `NOT CERTIFIED` under `PASS (shipped-only)`. To close it, define both cases. Empty list: `{"files": [], "count": 0}`, no pytest call, the plain `PASS` line and no block. Non-empty list: explicit paths only, and refuse a nonzero exit or any listed file with zero IDs. Add a C3 fault and a C4 case for each.
2. **Blocking, folds into Internal finding 1.** At runtime only `SECURITY_FAMILY` is refused. `test_security_marker.py`, the file that holds T1 and T2, is not in the family (17 names), so listing it removes the only test guarding the other must-stay files. To close it, add a `RELEASE_REQUIRED_FILES` frozenset with the 11 must-stay paths. `release_excluded_files()` must refuse a path in that set or in the family, a duplicate, a directory, an absolute path, `..` or `\`, and anything that is not `bootstrap/tests/**/test_*.py`. The hook matches by exact path equality, never by prefix or name. Add one hand-edited-list test per refusal, plus one where a listed missing file makes `--record` refuse.
3. **Non-blocking.** `_NATIVE_INPUT_IDS` is snapshotted after collection (`conftest.py:281`), so it never sees an ignored file. The join's `_committed_blobs` set is therefore the only control. It must not be derived from pytest output, and it must also check that the list is a subset of the tracked files.

Not a threat: excluding files listed in `protected_test_roster.json` (14 of the 16). That roster is `proposed-not-approved` deliberation data, and refusing those files would reverse the Decision.

**Coverage**: Ran no tests. Read headers and searched the 16 files for shipped paths, but did not read every test body. Windows and pytest 9.2.0 were not checked. About 470 words: findings 1 and 2 carry the refusal sets.

## Plan response -- Claude Sonnet 5.5 (plan author, Medium) -- 2026-11-16

Every blocking finding in both reviews is closed in the operative cells by exact replacement. Nothing is dropped and the Scope delta stays `preserved`. I checked each claim against the tree at `c94eec50` with read-only scratch probes; no test, `--record`, `--join` or Windows step ran. Internal review (`366f90ac`):

1. **Accepted (blocking).** Settled design 1 now gives the type (a tuple of `(path, subjects, reason)` rows, so a duplicate shows), the path pattern and every refusal. C1 T5 has one case per refusal; C2 case 5 uses a concrete bad list.
2. **Accepted (blocking).** Confirmed: raw `--collect-only -q` output carries warning and summary lines (5,601 lines for 5,592 IDs today). C1 and C5 keep only lines that start `bootstrap/tests/` and contain `::`, sort under `LC_ALL=C`, expect five lines, stop on any other, and name C2's real-tree test as the proof. The ID figures now say they move.
3. **Accepted.** The Scope delta names the first bash block as unchanged (pinned at `test_release_members_contract.py:75`). C5 says "The first block above", which is the block it means. The heavy-tier plan's line 47 still says this plan edits that block; that is its author's to correct.
4. **Accepted.** (i) `_RELEASE_EXCLUDED` is defined (design 3). (ii) A path's count is its `path::` lines, stricter than any `::` line, which a warning could carry. (iii) The return and print roles are named (designs 3 and 4). (iv) The helper is `_track_synthetic_files`; a red test that reads `HEAD` gets a second commit. Found while doing this: the connected counterpart needs `excluded=local["excluded"]`, or the counts (1,020 and 2) disagree. (v) C2 copies the strict environment setup.
5. **Accepted.** C1 ships three test files; C4 is the last frozen chunk and the re-anchor opens after C5 and its review; the Windows consequence is marked assumed, for the coordinator to tell the Maintainer.
6. **Accepted.** C4's filter test carries the Declared exception comment. A second one, for `_measure_excluded_tests`, answers Security 1: no public route reaches it short of a whole `--record`.

Foundations 2 (drop the `quality_gate.py` comment) is **declined**. It sits beside the line that always sets `CAIRN_FULL_SUITE` on the seed-0 child, the one place a later edit could key the hook on it. The extra hash joins a re-anchor that runs anyway, and the proposal names the file.

Security review (`39026b9e`):

1. **Accepted (blocking).** Confirmed: pytest with no file argument collects the whole directory, and a listed file with no tests adds no line while the exit stays 0. Design 3: an empty list is `{"files": [], "count": 0}` with no pytest call, and the join prints the plain `PASS` (design 4). Otherwise only listed paths run, and a nonzero exit or a path with no line refuses. Proof: C3, C4, S4.
2. **Accepted (blocking).** `RELEASE_REQUIRED_FILES` holds the 11 paths (all exist). The accessor refuses them, and the hook matches by exact path (designs 1 and 2). Proof: C1 T2 and T5, C2's real-tree test.
3. **Accepted.** `_tracked_test_files` reads git at `HEAD`, and the list must be a subset of it (design 4, C4, S1). Today's 131 tracked test files equal the 131 collected files.

Not run: any test, a real-tree record or join, Windows, pytest 9.2.0. The roster figures (365 rows, 348 left, the new identity) recompute. About 580 words against the 300 target, because eleven findings each point to a corrected cell; the plan's own overrun is in its Length line.

**Disposition**: ready-to-implement
**Elapsed**: about 15 minutes (16:07 to 16:22 EST, start estimated). **Tokens**: unknown.

## Implementation

- **C1 — `97ff68ac`:** Added the pinned exclusion and required-file lists, updated the native roster and policy identity, and added selector controls. Focused controls: 31 passed. A later tier inventory check reported 132 test files assigned once.
- **C2 — `a7860d29`:** Added the strict-context collection filter and cases for strict, ordinary, broad-override and malformed-list behavior. Focused real-tree and fixture controls: 10 passed.
- **C3 — `fbb53ebb`:** Added excluded-file counts to records and validation. Focused record and refusal controls: 22 passed. The connected record/join fixture failed before record creation on existing Bandit B314 at `templates/skills/_lib/pulse.py:166`.
- **C4 — `45fe2fc2`:** Joined records now reconcile collected paths against tracked test files. Focused synthetic join and refusal controls: 61 passed. Its connected-output assertion remains unverified because the C3 fixture is blocked by B314.
- **C5 — `e1741407`:** Updated `SECURITY.md` and `docs/release-process.md`. Focused documentation checks (3), membership documentation checks (2), and documented invocation check (1) passed; claim, link, snippet and tier-inventory checks were clean.

Plain collect-only measurements, with the full-suite override unset, changed from 5,742 to 5,785 IDs. The difference contains exactly the five accepted native IDs from the excluded files. Collect-only was not test execution. No whole suite or mapped families were run. Elapsed time and token use: unknown. Ordinary and Security code review remain due; the connected C3/C4 evidence is not claimed as passing.

The Maintainer accepted the limited scanner-repair exception in Decision
`05e706b3`; repair commit `f436717b` adds the one explained Pulse B314
allowance and Windows-separator normalization. The named scanner, live-entry,
stale/unallowlisted and hostile-XML selection had 14 passes; its Windows case
failed against the old conversion. After correcting a test-fixture ID, the
affected public test passed. The previously blocked connected record/join test
then passed after the repair (1 passed, 3 warnings). Claim and link checks on
the proposal passed. No native Windows run or whole suite was performed.

The plan's claim check still reports the historical review citation as out of
bounds after the source file shrank. The original citation was restored in
`926d6026` and is not rewritten; this is a historical citation flag, not a
product-check failure.

**Benefit versus cost**: worth it — the strict release selection excludes the
16 pinned Cairn-only files and reports them, while ordinary collections and
full certifying runs still cover every test. The Pulse repair keeps the
scanner's targets, severity rules, parser guards and fail-closed liveness.
Runtime savings are expected but not measured; the release owner gets the
first real records and join from [the release process](../../../docs/release-process.md).
Implementation and check cost were not measured. Reassess at the first real
strict release and if Pulse's parser guards, call path or scanner path contract
change. Elapsed time and tokens: unknown.

## Code review -- Terra (Reviewer, Medium) -- 2026-11-17

**Steelman and verdict:** Deliver a release selection whose omissions are visible and whose records cannot silently omit other tracked test files, then unblock its scanner without removing Pulse's guards. **ACCEPT**, with the separate Security code review still required.

**Coverage:** Ordinary code review of C1–C5 (`97ff68ac`, `a7860d29`, `fbb53ebb`, `45fe2fc2`, `e1741407`) and the accepted Pulse allowance and Windows normalization (`f436717b`, Decision `05e706b3`).

1. **Should it ship?** Yes, subject to the remaining reviews and release checks. The manifest pins 16 exclusions and validates required files; `conftest.py` ignores exact paths only with parsed strict context. `_validate_local_record` checks the list, count and collected IDs; `_join_local_records` compares both records and each order against committed test files minus the list. The final security and release documents identify the shipped-only selection and certifying full run.
2. **Best alternative?** The existing manifest and scanner liveness mechanism avoid a second selection or suppression system. `_rel` changes only the successfully resolved relative path to `as_posix()`; its outside-root fallback stays. The Pulse allowance is path/rule-wide, so a future B314 call shares it.
3. **What would show it wrong?** A non-strict collection losing a listed file, a join accepting a missing tracked file, a stale allowance passing, or a forbidden XML input accepted would contradict the stated behavior. The implementation record reports focused controls, a failing-first Windows rendering case, 14 scanner/XML passes and the post-commit connected fixture passing; I did not rerun them.

**Audience and retained rules:** The release instructions address the operator and preserve the full certifying run; no installed authoritative duty is removed. **Limits:** No native Windows run, real release record/join, whole suite, independent security assessment or full audit of excluded files' subject classifications. The earlier historical citation flag remains as recorded above. Elapsed: approximately 9 minutes; tokens: unknown.

## Code Security Review -- Sol High -- 2026-11-17

```
Reviewed commit: f436717b47a2fa67d2564bd449c7d320710b3af3
```

**Scope**: C1–C5 (`97ff68ac`, `a7860d29`, `fbb53ebb`, `45fe2fc2`, `e1741407`) and Pulse repair (`f436717b`, Decision `05e706b3`). Evidence through `1615b295`.
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 1 minute
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. Only parsed strict context enables exact-path exclusion of the 16 files. The manifest refuses required and security-family exclusions. The byte-verified runner measures listed files by collection and refuses missing or empty files. An empty list returns zero without collecting. Join checks matching summaries and every order against committed test files minus the list. `bootstrap/tests/conftest.py:264`, `:522`; `bootstrap/tests/security_manifest.py:166`; `bootstrap/security_check.py:550`, `:639`.
2. **Best alternative.** Reuse the existing Bandit gate. Only the Pulse path and B314 pair is added. Input bounds and XML guards stay in place. Slash conversion follows resolution and repository relativity, with the existing fallback. Scanner errors, unallowlisted findings and stale entries still fail. `templates/skills/_lib/pulse.py:148`, `:703`; `bootstrap/security_check.py:213`, `:1370`, `:1528`.
3. **What would show it wrong?** Ordinary collection losing a listed file, a missing tracked file passing join, or a stale allowance passing would falsify it. Reported controls cover these cases. The Windows rendering control failed with the old code, and the connected fixture passed after repair. `bootstrap/tests/test_security_check.py:607`, `:1072`, `:1464`, `:1777`, `:1816`.

**Audience and rule loss.** Release operators see the excluded names and count. Full certification, required guards and scanner phases remain. The Pulse exception applies file-wide for B314.

**Coverage.** Read committed changes and reported evidence. No test reruns, native Windows run, full release or certification, baseline ceremony, or exhaustive exclusion-classification audit. Historical citation flag remains.

## Dispositions

No implementation scope is deferred or removed. The still-unpassed operations
have active homes outside this plan:

- The first full strict release records and join, including native Windows
  execution, follow [the release process](../../../docs/release-process.md)
  and the existing release-cut wait in `dev/PLANNING.md`; they do not gate
  this plan's archive.
- The post-C4 frozen-baseline update and grouped re-anchor remain at the
  existing Maintainer wait in `dev/PLANNING.md`. This plan's six frozen-file
  edits join that group and remain expected unpassed until the operation.
- The joined Group 2 integration belongs to the arc owner after connected
  plans finish, under `dev/agent_collaboration.md` > "Plans and records". It
  does not gate this plan's archive.

## Author disposition -- Luna Low -- 2026-11-17

**Disposition**: ready-to-archive. C1–C5 and the Maintainer-authorized Pulse
repair are complete; ordinary and Security code reviews ACCEPT with no
remaining findings. The earlier C3 B314 failure is closed by `f436717b`, and
the connected record/join fixture passes. Accepted scope is preserved. The
expected runtime saving is not measured; the first actual release run is its
home. No full suite or native Windows execution was run. The historical
claim-check citation flag remains unchanged.
