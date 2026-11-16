# Plan: Release tests cover only what ships

**Source proposal**: dev/proposals/archive/2026-11-16-claude-release-tests-shipped-only.md
**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`, Medium), plan author
**Status**: awaiting-plan-review
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
1. **List.** `RELEASE_EXCLUDED_TESTS` in `security_manifest.py` maps a repo-relative path to `(subject paths, one reason)`. `release_excluded_files()` returns the keys as a frozenset; it raises `ValueError` on a malformed entry, a duplicate, or a key whose file name is in `SECURITY_FAMILY`; an empty list gives an empty set (whole suite).
2. **Hook.** `pytest_ignore_collect(collection_path, config)` in `conftest.py` (under `@_own`) returns `True` for a listed path (relative to the repository root, `/`-separated), else `None`, only when `_NATIVE_RUN_CONTEXT is not None`. That is the parsed strict pair: `_initialize_native_run_context` needs `CAIRN_RELEASE_GATE_ACTIVE=1` and then pops the five `CAIRN_NATIVE_RUN_*` variables, so the hook reads that state, not `os.environ`. `CAIRN_FULL_SUITE` is never read. The set is loaded once there. Measured (pytest 9.0.3, scratch tree): a directory argument drops an ignored file, an explicit file argument does not, so a hand-named file still runs.
3. **Record.** Key `excluded` = `{"files": sorted list, "count": int}`, the count from `pytest --collect-only -q` over the listed files in the detached checkout, run with `_release_child_env()` minus the release token and the `CAIRN_NATIVE_RUN_*` variables (it keeps the no-bytecode and no-cache settings that keep the checkout byte-exact). A nonzero exit or zero count refuses the record.
4. **Join.** Refuse unless each record's list equals the list in the `HEAD` manifest, the counts agree, no collected ID is in a listed file, and each order's collected files equal the tracked test files at `HEAD` (`test_*.py` or `*_test.py` under `bootstrap/tests/`, from `_committed_blobs`) minus the list. Output: `security_check: PASS (shipped-only) -- Mac and Windows evidence joined at <head>.`, then `NOT CERTIFIED (shipped-only release selection): <N> tests in <M> files were not run. They run when their own files change.` and the sorted names, two-space indent.
5. **Roster.** Delete the 365 rows of the five Cairn-side files that carry any (all POSIX, measured), leaving 348: 63 Windows, 285 POSIX. Otherwise the record would demand IDs it no longer collects. Update the count guard and `NATIVE_ONLY_POLICY_ID` (expected `sha256:02eb75b23f6856debcdacc9a15461a4e536606d3471983eaeacdfc7c05c5aab8`; recompute). A consequence the proposal did not state: run directly on Windows, those five files no longer skip their POSIX-only cases; nobody runs them there.

**The 16 files** (under `bootstrap/tests/`) and the subject paths the selector must reach each from: `test_repin.py`, `test_repin_ceremony.py` from `scripts/repin.py`; `test_reanchor.py`, `test_reanchor_driver_disclosures.py` from `bootstrap/reanchor.sh`; `test_gate_reanchor.py`, `test_gate_preflight.py`, `test_gate_manifest.py`, `test_gate_transition.py`, `test_oracle.py`, `test_oracle_activation.py`, `test_oracle_trust.py` each from the `_`-prefixed helper of the same name in `bootstrap/tests/`; `test_ceremony_review_report.py` from `_gate_preflight.py`; `security/test_check_release_publication.py` from `scripts/check_release_publication.py`; `test_quality_gate_cli.py`, `test_quality_gate_order_independence.py`, `integration/test_quality_gate_redundancy.py` from `scripts/quality_gate.py`. Each reason reads "Tests <subject>, which only Cairn's Maintainer runs; none of it is in the install manifest." (measured: `scaffold.py --manifest` names none of these subjects). Must stay, pinned in a test: `test_ast_attest`, `test_quality_gate_neutrality`, `test_security_check`, `test_security_marker`, `contract/test_release_members_contract`, `test_session_binding_gate_and_printing_hold`, `test_manifest`, `test_verify_integrity`, `test_verify_ref`, `test_security_lint`, `test_loop_fidelity_gate`.

**Security Review requirements and their proof.** Keep the three files in the run: C1 T2 and C2's real-tree test. Key on the strict pair, never `CAIRN_FULL_SUITE`: C2 cases 2 and 3. Certifying and standalone runs keep all tests: C2 case 3. The join checks tracked files at `HEAD` and counts from that tree: C3, C4. `PASS` says "shipped-only" and `SECURITY.md` is corrected: C4, C5. Contract pin 18 to 15 and docstring wording: C1, C2.

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

Estimate 12 to 16 Low-tier agent-hours over two elapsed days (a guess). Uncertain: other sessions' edits to the same files.

**Every chunk.** A Low-tier implementer (`AGENTS.md`); name the model at spawn. Work on `0.8-dev`. Claim the exact paths. Read `git status` and `git log -5` for each file at the start; another session's uncommitted edit stops you, never commit it. Write the failing test, see the stated failure, then change. Prose by exact replacement. Run only the named test files with `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest`; tests that read `HEAD` (the connected fixture runs `git archive HEAD`) run after you commit. If `python tools/test_tiers.py` (or T3, or `contract/test_test_tiers.py`) fails with `git-read-binding-failed`, another session has an uncommitted edit to `tools/git_read.py`: wait, do not fix. One commit per chunk, explicit paths, no push. If the code differs from the chunk, stop and report.

**Shared files.** `docs/release-process.md` is also edited by the accepted heavy-tier-trigger proposal (one place, the Security Review trigger line); C5 edits other passages and re-reads first. The staged-modules proposal edits none of these files; the template-trim proposal names `security_manifest.py` only as a protected exemption and may delete tests that pin template wording, so every chunk re-reads status for its test files. The meter plan and the paused Windows refresh read or edit `security_manifest.py` rows; C1 re-reads the roster.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | List, family, roster, pins | `0.8-dev` exists; plan reviews | `security_manifest.py`, 2 test files, 4 tests |
| C2 | Collection hook | C1 | `conftest.py`, `quality_gate.py` comment, 6 tests |
| C3 | Record side | C2 | `security_check.py`, 5 faults, connected test |
| C4 | Join side | C3 | `security_check.py`, 6 tests |
| C5 | Documents and joined check | C4 | 2 documents, evidence in the commit |

**Red until the re-anchor** (expected, not pass criteria). After C4 `python scripts/repin.py status` lists six more `FROZEN-MODIFIED` files (the six above) and no other; record it before C1 and after C4. Five parametrized IDs leave the collection (C1). The engine pin is already owed (`repin.py status`: six CHANGED symbols), so `test_ast_attest` is expected red; its baseline is not touched here.

Length: the opening body runs about 1,440 words against 1,000. Acceptance runs 110 to 160 words a chunk, except C5 at about 250 because it carries the exact public wording. The overrun is the settled design (about 350 words), the 16-file list (about 95) and that wording, which a Low-tier executor cannot decide itself and a reviewer must check.

## Acceptance criteria

**C1 -- list, family, roster, pins.**
- Before any edit save outside the repo `before-plain.txt` from `CAIRN_FULL_SUITE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests --collect-only -q -p no:cacheprovider` (5,528 IDs when measured on 2026-11-16, about 4 s).
- New tests in `test_security_marker.py`, each seen failing first: T1 the list equals a pinned copy of the 16 paths; T2 no listed file is in `SECURITY_FAMILY` or the pinned must-stay set, and every listed path is tracked; T3 `tests_for_paths` (loaded as `contract/test_test_tiers.py` does) selects each file from every subject path; T4 no roster row names a listed file.
- `_REVIEWED_MEMBERS` loses the three; family pin and roster identity tests pass; `GATE_INTEGRITY_MEMBERS` keeps only `test_ast_attest.py`; the contract test expects "15 required files" and "14 passed"; the `_connected_runner_fixture` count guard expects 63 and 285. The "seventeen" and "entire suite" wording in `security_manifest.py` and the `test_security_marker.py` promise line says shipped-only.
- `comm -23` of sorted before and after plain lists shows exactly five `test_join_refuses_each_native_identity_missing_from_all_host_orders[...]` IDs, named in the commit message.

**C2 -- collection hook.**
- Tests first in `test_security_check.py` beside `test_native_context_writes_external_report_for_actual_order`. Fixture manifest: the copied real one plus one appended `RELEASE_EXCLUDED_TESTS = ...` line naming a fixture file with a failing test. (1) Strict pair, both orders: the file is absent from `collection_input_ids` and `collected_ids`, others present, exit 0. (2) Same with `CAIRN_FULL_SUITE=1` exported: identical IDs. (3) Release token alone, `CAIRN_FULL_SUITE=1` alone (what the certifying pair and a standalone `quality_gate.py` run set), neither: file collected. (4) Empty list, no accessor, no manifest: nothing excluded, no error. (5) Malformed list under the pair: nonzero exit.
- One test in `test_security_marker.py` (`_collect` gains an env argument; skip off Mac and Windows): on the real tree the strict-pair IDs equal the plain IDs minus every ID in a listed file; the removed files are exactly the 16; the must-stay set is present.
- `conftest.py`'s "seventeen" docstring and marker text say shipped-only. `quality_gate.py` gets a comment only (the child inherits the pair; its `CAIRN_FULL_SUITE` must stay irrelevant).

**C3 -- record side.**
- `_synthetic_local_record` gains `excluded` (default the reviewed list, count 1020). Faults added to `test_join_main_refuses_mutated_native_records`, each refused: no `excluded`; a listed name missing; a shipped file added; count zero or a boolean; an order that collected a listed file.
- `_measure_excluded_tests(root)` as Settled design 3, called when the local record is built; `_validate_local_record` adds `excluded` to its exact key set and checks the files against `_RELEASE_EXCLUDED`.
- Connected test: the fixture manifest gets the appended list naming a fixture file with two tests, one failing; the test sets `security_check._RELEASE_EXCLUDED` to match. `--record` exits 5, `excluded` is that file and 2, and neither order collected it.
- The module docstring's phase 3 and 4 lines, the `run_suite` docstring and its printed line say shipped-only. `test_security_lint.py` passes.

**C4 -- join side.**
- `_tracked_test_files(head)` on a temporary repository returns only test files under `bootstrap/tests/` (a deep one, a helper, a fixture file, one under `docs/`).
- Existing `--join` tests call one helper that patches it to the record's collected files plus the list; the connected test uses the real one.
- New tests through `main(["--join", ...])`: matching records exit 0 with the `PASS (shipped-only)` line and the block (16 sorted names, count, sentence). Refused: `_RELEASE_EXCLUDED` minus one name (negative control); a tracked test file neither collected nor listed; a collected file not tracked; counts that differ.
- The connected join prints the block with the fixture file and 2.

**C5 -- documents, joined check.**
- Exact replacements of the phrases below; every other line keeps its wrapping. `SECURITY.md` item 3: "The full `bootstrap/tests` selection runs in release mode" becomes "The shipped-only `bootstrap/tests` selection runs in release mode: every test except the files in `RELEASE_EXCLUDED_TESTS` (`bootstrap/tests/security_manifest.py`), which the join prints in a `NOT CERTIFIED` block"; item 4: "seed-0 full-suite child" becomes "seed-0 child, which runs the same selection,"; after item 4's paragraph, "Certifying runs before a re-anchor run every test." `docs/release-process.md`: "both full-suite orders" becomes "both orders of the shipped-only selection (every test except the files in `RELEASE_EXCLUDED_TESTS`)"; after "Do not reuse an old report path." add "This block names neither strict variable, so it runs every test, including the files the strict run leaves out."; after the paragraph beginning "Only the join can print `PASS`." add "The join also prints a `NOT CERTIFIED` block with the left-out test files, their count and the sentence that they run when their own files change. Paste it into the release notes with the joined output. Certifying runs before a re-anchor (`dev/rules/certifying-runs.md`) still run every test." The first bash block is byte-identical.
- `claim_check.py`, `link_check.py`, `sync_doc_snippets.py --check` on both: no hard flag. `git grep -n -i -E 'full bootstrap/tests|full-suite child|whole engine suite'` over `SECURITY.md docs bootstrap scripts` finds none.
- The joined check (Verification), its evidence in this commit's message. `comm -23 before-plain.txt after-plain.txt` shows only the five IDs; with C2's real-tree test (release IDs equal plain IDs minus the 16 files), the release run lost nothing else.

## Scope delta

**Scope delta**: preserved. One lighter mechanism: the proposal lists `scripts/quality_gate.py` as changing, but its seed-0 child inherits the strict pair, so the file gets a comment, and C2 case 1 under seed 0 and C3's connected run prove the outcome. Nothing is dropped. The 28 guard tests are not in the baseline (the Decision's default is no fold).

## Verification

Promises and entry points: `security_check.py --record` and `--join` (C3, C4, the connected test); the conftest hook through real pytest collection (C2); the selector contract and the pinned list (C1). Controls: S1 the list is read from the manifest in the checkout under test; a record's own `excluded` is only checked against it. S2 the negative controls in C2 (five cases), C3 (five faults) and C4 (four refusals). S3 the Maintainer's `--record` and `--join`. S4 an empty or absent list means the whole suite; a malformed one refuses. S5 residual: a misclassified file, closed only by review of the 16 pins in T1.

Each chunk runs only the files `python tools/test_tiers.py for <the chunk's changed files>` lists, plus its new tests. After C5, once on the clean final revision: the selector over all changed files (24 files at plan time, 866 cases and about 330 case-seconds in the 2026-11-12 run; no whole suite), those files in one run, `python tools/test_tiers.py check`, and the before and after plain lists compared as in C1.

Not run, so unverified: a real-tree `--record` or `--join` (expectation about 4,508 tests, 5,528 minus 1,020, in about 70% of the time; the Maintainer's release run is the first evidence) and any Windows host. A refusal there returns the plan to `revising-code`.
