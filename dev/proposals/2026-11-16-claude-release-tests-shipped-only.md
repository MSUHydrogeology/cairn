# Release tests cover only what ships to adopters

**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy -- the change edits `bootstrap/security_check.py`, the protected test roster and the release process, all named protected surfaces; the Maintainer sets the tier
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: The release's whole-suite run stops testing Cairn's own signing and gate machinery, which adopters never receive; those tests run when their own files change, and the release record lists what it left out.

## Decision summary

Today the strict release check runs every test in `bootstrap/tests` on each host, including tests of the re-anchor and gate ceremonies that only the Maintainer runs. The Maintainer's direction (board row, 2026-11-13): *"A full run should only be done on what is shipped to adopters."* This proposal draws the line by what a test examines: if the thing under test reaches an adopter or is run by one, the test stays in the release run; if it is Cairn's own release machinery, it leaves.

From the board row (not re-measured): 20 files, 1,283 of 5,413 tests (24%) and 938 seconds (32% of a 49-minute run). That saves about a third, not most. Cost: the record no longer shows those tests passing at the release commit, so it says so; and a roster edit needing the Maintainer's re-anchor.

## Context

Checked in the current tree:

- `security_check.py` phase 3 runs `pytest bootstrap/tests` whole (`run_suite`); phase 4's `quality_gate.py` runs the same directory again in seed-0 order (`_DEFAULT_TEST_DIR`). `docs/release-process.md` repeats the whole run in its first block.
- `bootstrap/tests/security_manifest.py` names a 17-file security family; `scripts/check_release_test_members.py` requires every family file in the release report. Five family files are Cairn-side: `test_ast_attest`, `test_gate_preflight`, `test_gate_reanchor`, `test_reanchor`, `test_security_check`.
- The same file's `NATIVE_ONLY_NODE_IDS` has 713 rows (my count). 365 sit in Cairn-side files: `test_reanchor` 205, `test_repin_ceremony` 102, `test_repin` 45, `test_gate_preflight` 12, `test_reanchor_driver_disclosures` 1. Its identity hash `NATIVE_ONLY_POLICY_ID` must change with them.
- `python tools/test_tiers.py for <path>` selects tests that name a changed file. I ran it on 15 Cairn-side sources (`scripts/repin.py`, `bootstrap/reanchor.sh`, `bootstrap/security_check.py`, `scripts/quality_gate.py`, `scripts/check_release_publication.py` and the `_gate_*`, `_oracle*`, `_ast_attest` helpers); each selected its own test files (1 to 11). `bootstrap/scaffold.py` also selects `test_ast_attest`, `test_oracle*` and `test_security_check`.

## Proposal

**1. The boundary rule.** A test file is **shipped** if its subject is something an adopter receives or runs: the installer and upgrader (`bootstrap/scaffold.py`, `bootstrap/_scaffold/`), installed templates and module scripts, the install contract (manifests, profiles), and the checks adopters run (`bootstrap/verify_integrity.py`, `bootstrap/container/verify-ref.sh`, the bootstrap block in `PROVENANCE.md`). It is **Cairn-side** if its subject is machinery only Cairn's Maintainer runs. A file that covers both stays. A file no list names stays: the default is more testing.

**2. The Cairn-side list.** Counting by file name from the tree gives 19, not the row's 20: `test_repin`, `test_repin_ceremony`, `test_reanchor`, `test_reanchor_driver_disclosures`, `test_gate_reanchor`, `test_gate_preflight`, `test_gate_manifest`, `test_gate_transition`, `test_oracle`, `test_oracle_activation`, `test_oracle_trust`, `test_ast_attest`, `test_security_check`, `test_ceremony_review_report`, `security/test_check_release_publication`, `test_quality_gate_cli`, `test_quality_gate_neutrality`, `test_quality_gate_order_independence`, `integration/test_quality_gate_redundancy`. The row's twentieth was identified from the run's report on 2026-11-16 (by the coordinator): `test_session_binding_gate_and_printing_hold` (43 tests, 15 seconds), matched by the word "gate" in its name. Its subject is the shipped session reader, so it stays in the release run. The 19 files are 1,240 of 5,413 tests (23%) and 923 of 2,938 seconds (31%), summed from JUnit case times in the 2026-11-12 certifying run's report; the per-file table is committed at `dev/measurement/certification-run-2026-11-12-per-file.csv`.

Calls that are not obvious:
- `test_ast_attest` is Cairn-side by subject but its staleness check reads the live `scaffold.py`; the selector picks it on any engine edit (checked), so it leaves.
- The quality-gate tests test a tool. The tool itself still runs in the release (phase 4; neutrality and redundancy), so shipped bytes keep their check.
- Stay: `test_session_binding_gate_and_printing_hold` (name says gate; subject is the shipped session reader), `test_manifest` (the install manifest), `test_verify_integrity`, `test_verify_ref`, `test_security_lint` (Bandit over shipped code).
- Stay, though release-side: `test_security_marker` and `contract/test_release_members_contract`. They guard the roster and comparator the release run itself uses, and are cheap.
- `test_loop_fidelity_gate` guards shipped templates; it stays. Other Cairn-only dev-script tests were not classified (not checked); a later pass applies the rule.

**3. How they still run.** The selector already picks them when their own files change (Context). One addition: a contract test that every Cairn-side file is selected by at least one of its subject's source paths, so a rename cannot silently orphan one. The certifying run before re-anchor (`dev/rules/certifying-runs.md`) is left unchanged and still runs everything; the Cairn-side tests therefore still run in full before every ceremony.

**4. What the release record says.** The shipped-only list lives in `security_manifest.py` beside the family, with one reason per file. `conftest.py` leaves listed files out in release mode. Each local record carries the excluded file names and test count. `--join` refuses if the records disagree with the reviewed list, and prints a `NOT CERTIFIED` block with the names, the count and the sentence "run when their own files change". `docs/release-process.md` tells the Maintainer to paste that block into the release notes.

**5. Protected files that change.** `bootstrap/security_check.py` (phase 3 target and join output), `scripts/quality_gate.py` (seed-0 target), `security_manifest.py` (five family members out, list added, roster rows and identity hash), `conftest.py`, `test_security_marker.py`, `test_security_check.py`, `docs/release-process.md`. Lane: heavy, usual plus Security Review; the Maintainer re-anchors. Whether the signed gate manifest hashes each file: not checked; the plan confirms against `bootstrap/REANCHOR_RUNBOOK.md`.

**6. Order against the layout.** Recommended: this first. The board puts it in group 2 so the layout's many certifying runs cost a third less, and the layout plan runs alone. The layout then renames the files and can turn the rule into a path test (Cairn-side = subject under `release/`; shipped = subject under `install/` or `templates/`). The cost is that the roster paths change twice; if the Maintainer prefers one re-anchor, the layout goes first and this follows.

**7. Group 5 rows, not reopened.** The 28 kept guard tests: their row's own default retires them in a pass that already changes the roster; this change is such a pass, so the Maintainer may fold them in. I did not check which of the 28 sit in Cairn-side files. The Windows roster refresh: its 99 added rows were not checked against the Cairn-side list; rows for removed files would be dropped, so refresh after this.

## Rationale

The Maintainer's position (board row, 2026-11-13): *"I do not believe there is a real security threat from not testing something that our adopters don't use. We use it here."* That holds for adopters. The plain risk is ours: a defect in ceremony tooling would no longer be caught at release; it would surface at the next re-anchor, where its tests still run in full (item 3). The Maintainer's sentence *"We would find errors in what we run here when we run them."* is the same bet.

## Alternatives considered

- **Do nothing.** Keeps 938 seconds and 365 roster rows of ceremony tests in every release; the Maintainer has directed otherwise.
- **Drop only the heaviest files.** Smaller saving, same roster edit and re-anchor, and a boundary nobody can state.
- **Skip by file name, no list.** Name matching gave 19 of the row's 20 and misses `test_ast_attest`'s subject; a reviewed list with reasons is checkable.

## Documentation / doctrine surface

`docs/release-process.md` (first block, Strict release-security evidence, and a line for the release notes), the `bootstrap/security_check.py` header, the `security_manifest.py` docstring, this board row. `dev/rules/certifying-runs.md` unchanged. Nothing shipped to adopters changes; no doctrine moves.

## Evidence / verification plan

### Tests required

- Public entry `security_check.py --record` / `--join`: a record excluding an unlisted file, or listing a shipped file as excluded, is refused; a matching one prints the `NOT CERTIFIED` block. Negative control: remove one file from the list and watch `--join` fail.
- Contract test: every test file is shipped or Cairn-side, never both; the selector reaches each Cairn-side file from its subject path.
- `test_security_marker.py` mutation updated for the 12-file family; the family pin test and the roster identity test pass on the new values.

### Examples / smoke checks

`python tools/test_tiers.py check`; one Maintainer `--record` run: expect about 4,173 tests (5,413 minus 1,240) in about two-thirds of the time. That is an expectation until measured.

#### Security preflight

- **S1.** The excluded list comes from the reviewed manifest in the signed tree, not from the run or from a test file's own claim.
- **S2.** Can fail: removing a name from the list makes `--join` refuse (negative control above). The collected-ID check derives its expected set from collection; whether the plan's list is read independently is for the plan to show.
- **S3.** The Maintainer runs `--record` and `--join`; the input set is the committed tree at HEAD, as now.
- **S4.** An unreadable or empty list falls back to the whole suite (more testing).
- **S5.** A listed file edited to hide a real adopter-facing test: closed only by review of the list, enumeration, not construction. Residual: a misclassified file.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Any of these in the first two releases withdraws or narrows the list: a defect in a Cairn-side file that the removed run would have caught at the release commit, found later at a ceremony or by a person; a commit that changed a Cairn-side file with no selector run recorded; or an adopter-visible failure traced to a file the list called Cairn-side. I did not measure how often Cairn-side files change between releases (not checked).

## Scope delta

**Scope delta**: preserved. Nothing from the opening scope is dropped.

## Assurance path

**Assurance path**: high-assurance -- it edits the release gate (`security_check.py`), the signed roster and the release process.

## Review -- Gemini 4 Hydrogen (ordinary Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: 401de278d48c72c490ecc0ae9d7b0b6aa33697dd
```

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: ~2m
**Tokens**: unknown

The proposal cleanly implements the Maintainer's direction to limit release-gate runs to adopter-shipped code: it defines a falsifiable boundary (defaulting to keeping unlisted or mixed files), preserves full-suite coverage in pre-reanchor certifying runs, adds selector-reachability and `--join` negative controls, and records exclusions explicitly in the release notes.

**Foundations**

1. **Should this happen as framed?** Yes: the 19 Cairn-side files account for 1,240 of 5,413 cases (22.9%) and 922.8s of 2,937.3s (31.4%) in the certifying CSV, while `tools/test_tiers.py for` already selects them (plus `test_ast_attest.py` from `bootstrap/scaffold.py`) on source edits -- `dev/measurement/certification-run-2026-11-12-per-file.csv`, `tools/test_tiers.py for bootstrap/scaffold.py`.
2. **Best alternative.** Ordering after the layout refactor (item 6) would avoid moving roster paths twice, but running this first saves ~31% across layout's certifying runs; both options are surfaced cleanly to the Maintainer -- `dev/proposals/2026-11-16-claude-release-tests-shipped-only.md:45`.
3. **What would show it wrong.** A Cairn-side defect missed at release and caught at ceremony, a Cairn-side edit without a recorded selector run, or an adopter-visible failure in an excluded file -- `dev/proposals/2026-11-16-claude-release-tests-shipped-only.md:89`.

**Findings**

1. **Non-blocking (for plan/Security Review):** `bootstrap/tests/security_manifest.py:12-17` and `bootstrap/tests/test_security_marker.py:15` promise that the release check runs the entire suite with no deselection; update those docstrings alongside the 12-file `SECURITY_FAMILY` split.
2. **Non-blocking (for plan):** `scripts/quality_gate.py:145` (`_DEFAULT_TEST_DIR = "bootstrap/tests"`) serves both `security_check.py` phase 4 and standalone/certifying runs; scope release-mode exclusion to `CAIRN_RELEASE_GATE_ACTIVE=1` in `conftest.py` so certifying runs (`dev/rules/certifying-runs.md`) still run all 5,413 tests.

**Functional prose / audience check:** No `AGENTS.md` or `docs/methodology/` rule weakens or disappears; `docs/release-process.md` changes are Maintainer-facing release-notes instructions.

**Coverage:** Checked proposal counts against `bootstrap/tests/security_manifest.py` (17 `SECURITY_FAMILY`, 713 `NATIVE_ONLY_NODE_IDS` with 365 in Cairn-side files), `dev/measurement/certification-run-2026-11-12-per-file.csv`, `scripts/check_release_test_members.py`, `bootstrap/security_check.py`, `scripts/quality_gate.py`, and `tools/test_tiers.py for` outputs. Did not run `pytest` or inspect `bootstrap/REANCHOR_RUNBOOK.md` (deferred to plan/Security Review).

## Security Review -- Gemini 4 Argon (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 62cb0aafd7b8e1fecff746ef21679ca5c8a2fd85
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: ~4m
**Tokens**: unknown

Obligation: does excluding the 19 Cairn-side test files from the strict release-gate run weaken the security assurance of shipped adopter artifacts or expose adopters to silent regressions in supply-chain/integrity controls?

Steelman: what an adopter receives or runs is completely preserved and tested in full under both collection orders on both native platforms; Cairn-side ceremony and gate machinery is never delivered to adopters, remains fully tested whenever its source files change via the test selector, and runs in full during every certifying run before re-anchor.

**Foundations**

1. **Should this happen as framed?** Yes: the 19 Cairn-side test files examine developer and Maintainer ceremony tools (`scripts/repin.py`, `bootstrap/reanchor.sh`, `bootstrap/security_check.py`, `scripts/quality_gate.py`, etc.), none of which appears in the shipped install manifest; all installer/upgrader code, templates, and runtime integrity checks continue to run in both collection orders on native platforms. -- `bootstrap/scaffold.py --manifest`, `bootstrap/tests/security_manifest.py:35-114`, `dev/measurement/certification-run-2026-11-12-per-file.csv`
2. **Best alternative.** Retaining all tests in release mode costs ~31% of execution time across every candidate run with zero coverage benefit for adopters; dropping files ad-hoc without manifest tracking lacks auditability; the reviewed manifest with reasons, `--join` validation, and release notes disclosure is the safest path. -- `dev/proposals/2026-11-16-claude-release-tests-shipped-only.md:53-58`, `docs/release-process.md:170-189`
3. **What would show it wrong.** A Cairn-side defect missed at release and caught later at a ceremony or in production, an edited Cairn-side file without a selector run recorded, or an adopter-visible failure traced to an excluded test file. -- `dev/proposals/2026-11-16-claude-release-tests-shipped-only.md:87-90`

**Findings**

1. **Non-blocking (for plan): Include `bootstrap/tests/contract/test_release_members_contract.py` in section 5.** Line 96 currently asserts `"release membership: PASS: 18 required files"`. With the 5 Cairn-side members removed from `SECURITY_FAMILY` (17 -> 12), the expected count drops from 18 to 13 (12 family + `test_security_marker.py`). Section 5 ("Protected files that change") should explicitly list this contract test alongside `test_security_marker.py`.
2. **Non-blocking (for plan): Exclusion enforcement mechanism in `conftest.py`.** To avoid tripping `security_check.py`'s fail-closed deselection detector, release-mode exclusions should be enforced during collection (e.g. via `pytest_ignore_collect` keyed on `CAIRN_RELEASE_GATE_ACTIVE=1`) rather than deselecting collected items via `pytest_collection_modifyitems`.
3. **Non-blocking (for plan): Certifying run invariance.** Ensure that `CAIRN_FULL_SUITE=1` unconditionally bypasses any release-mode exclusion hook in `conftest.py` and `quality_gate.py`, guaranteeing that pre-reanchor certifying runs (`dev/rules/certifying-runs.md`) always execute the complete suite (all 5,413 tests) without exclusions.
4. **Non-blocking (for plan): Gate manifest hash confirmation.** Section 5 notes "Whether the signed gate manifest hashes each file: not checked". Confirmed during this review: `bootstrap/tests/fixtures/gate_manifest.json:7674` hashes `bootstrap/tests/security_manifest.py` and all tests under `bootstrap/tests/`. Any edit to the manifest or test roster invalidates the gate and requires the Maintainer's signed re-anchor.

**Functional prose / audience check:** No rule in `AGENTS.md` or `docs/methodology/` is weakened or deleted; the release process edits in `docs/release-process.md` provide Maintainer instructions for release note disclosures (`NOT CERTIFIED` block) and preserve the fail-closed join requirement.

**Coverage:** Checked proposal against `bootstrap/security_check.py`, `scripts/quality_gate.py`, `bootstrap/tests/security_manifest.py`, `scripts/check_release_test_members.py`, `bootstrap/tests/contract/test_release_members_contract.py`, `bootstrap/tests/conftest.py`, `docs/release-process.md`, `bootstrap/tests/fixtures/gate_manifest.json`, `bootstrap/scaffold.py --manifest`, and `tools/test_tiers.py for bootstrap/scaffold.py`. Did not execute full `pytest` suite or run on Windows host (deferred to implementation/certifying run).
