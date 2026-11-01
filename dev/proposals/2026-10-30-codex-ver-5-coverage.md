# Proposal: compare multi-script module discovery paths

**Author**: Codex (gpt-6.1-terra), Strategy
**Status**: awaiting-decision
**Review**: usual
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-10-30
**In brief**: Compare expected module scripts across installation, lock records, upgrade additions and scan targets.

## Context

The VER-5 row in `dev/PLANNING.md` asks for consistent discovery across installation, manifest, security scan and upgrade. `bootstrap/_scaffold/install.py::install_manifest` uses shared core, skills and module mappings; the lock writer uses that manifest. Upgrade has a separate new-module-file selection loop in `bootstrap/_scaffold/upgrade.py`; `bootstrap/security_check.py::scan_targets` unions registry and manifest results. No mismatch is known. The Maintainer directed on 2026-11-01: “Prepare broader behavior checks” for v0.6, without a new traversal; this is direction to prepare a proposal, not a Decision.

`bootstrap/tests/test_reference_scripts.py::TestMultiScriptModules::test_multi_script_module_installs_all_scripts` checks real installation and source bytes, but independently names only `issue-capture`. Six other modules currently have multiple verbatim Python files: `claim-check`, `coordination-tiers`, `doc-drift-prevention`, `content-security`, `api-access-security`, and `web-hosting-security`. `bootstrap/tests/test_security_lint.py::test_every_manifest_verbatim_py_is_scanned_by_some_path` uses the manifest as its expectation; `test_every_templates_py_on_disk_is_release_scanned` uses an independent disk inventory with named exclusions. Neither establishes upgrade additions against the independent install expectations.

## Proposal

For all seven named modules, maintain explicit source/destination pairs for every currently shipped verbatim Python file, including package files. Establish the list by inspecting the shipped templates and intended destinations, not by deriving expected values from the mapping, manifest, lockfile, upgrade result or scanner result. Reuse the existing list and test home where practical. Exercise each module separately through the scaffold entry point and compare each expected file's installed bytes and its lock record's source and destination. Check each expected source is in `scan_targets()`; it is an inclusion check because that set intentionally contains other executables.

For upgrade, construct an older-install fixture for each selected module with the expected files and corresponding lock records absent, while preserving the selected module in the profile and lock. Run the real upgrade stage and apply entry points against current templates; compare every expected destination and bytes, and resulting lock source/destination records, with the independent list and fresh install. This tests additions to an already selected module, not opt-in of a newly available module. Use temporary projects and preserve normal collision and review safeguards.

Do not change discovery or production behavior. This is an enumerated check of seven current modules and their listed files, not proof for all modules, future files, non-Python templates, every upgrade state or scanner execution. The disk scanner test provides separate broader scan evidence, with its exclusions. The original single-traversal objective remains undelivered; only the Maintainer can decide whether this outcome is sufficient for VER-5.

## Rationale

Independent expectations expose a shared omission that a comparison derived solely from the mapping cannot. Separate behavior checks can reveal selection drift in the four paths while leaving protected engine and scanner behavior unchanged. The list needs maintenance as shipped files change.

## Alternatives considered

One traversal would meet the original design objective but changes protected engine or scanner surfaces without a demonstrated mismatch. The previous install-only expansion costs less but leaves upgrade selection and lock records untested against the independent list. Doing nothing leaves those gaps.

## Documentation / doctrine surface

No shipped documentation, doctrine or install contract changes proposed. This proposal is deliberation in `dev/`; update the board only at its defined serialization point.

## Evidence / verification plan

### Tests required

In `bootstrap/tests/test_reference_scripts.py`, extend the existing installation node and add focused behavior nodes for lock records, upgrade stage/apply and scan inclusion using the independent pairs. Run the iteration selection from `python tools/test_tiers.py for` the changed test files. In separate copies of the final commit, falsify a representative omission in each distinct selection path, including both scanner input routes together, and exercise wrong destination, bytes and record cases as needed. Report the measured mutations and their limits; do not claim every listed member was mutation-tested or that a value reaches every member. The normal behavior assertions still compare every independently listed pair. Missing records, wrong destinations or changed installed bytes must fail. Record the clean-final-commit Boundary B selection after code review here, including its mode and required evidence. If the tests expose a real mismatch, stop for reassessment rather than silently change protected production surfaces.

### Examples / smoke checks

Run the applicable prose gates on this proposal. No full-tree certification is requested.

#### Security preflight — five questions, answered in writing

N/A: no trust boundary added or widened; no high-risk surface changes proposed.

## Signals the change is wrong

An existing independent check already proves the same paths and files, the fixture cannot represent upgrade additions faithfully, or an observed mismatch requires a different scope.

## Scope delta

**Scope delta**: preserved. The original seven-module install assertion remains; the separate original VER-5 traversal remains for the Maintainer to disposition.

## Assurance path

**Assurance path**: standard. The proposal adds behavior tests without changing the install contract, executable, or trust boundary.

## Proposal review -- Codex (gpt-6.1-terra) -- 2026-10-30

**Verdict: revise before Decision.** The proposed tests are useful, but their passing would not establish the board's consistent-discovery outcome across all four paths.

**Foundations.** Should it happen as framed? Not yet: the test at `bootstrap/tests/test_reference_scripts.py:125-153` exercises fresh installation and bytes only; it does not compare upgrade or scan discovery. The board's VER-5 row asks for consistency across install, manifest, security scan and upgrade. Best alternative: retain the small test-only change, and first assess existing cross-path tests or add the smallest independent behavior check that can expose an actual disagreement; the shared `_MODULE_MAPPINGS` already supplies install, manifest and upgrade, and `security_check.py` selects Python sources from `install_manifest()`. A new traversal could reduce duplicated selection logic but changes protected surfaces without a demonstrated mismatch. What would show this wrong? Evidence that existing checks already cover the relevant cross-path selection differences, or a mismatch showing that a shared traversal is needed.

**Finding (advice):** Make the loss and evidence for the Maintainer's choice concrete: identify which selection differences and paths are checked or remain unchecked, and whether a small behavior test covers them. The independent file list detects omissions in install mapping but cannot detect drift in upgrade selection or scanner filtering. The Maintainer alone can accept the loss of the original single traversal. No demonstrated mismatch makes this a blocking finding.

**Coverage:** Read the proposal, VER-5 strategy and board row, install and manifest loops, upgrade mapping uses, scanner manifest selection, and the existing multi-script test at `5aac7f02`. Did not run tests or audit all existing cross-path coverage. Elapsed: about 2 minutes; tokens: unknown.

## Author response -- Codex (gpt-6.1-terra) -- 2026-10-30

Accepted the advice to make coverage and its limits explicit. The existing scanner checks provide meaningful cross-path and independent disk evidence; the proposed independent install expectations address a different gap. An all-module upgrade comparison would add a new test without evidence of a mismatch, so it is not proposed. The Maintainer can instead choose the original traversal or request further comparison; the single-traversal outcome remains explicitly unfulfilled. Elapsed: about 2 minutes; tokens: unknown.

## Author response -- Codex (gpt-6.1) -- 2026-11-01

The Maintainer directed broader checks, so the prior advice on cross-path evidence is accepted in the revised scope. This widens the proposal and returns it for a second usual review. Elapsed: approximately 7 minutes; tokens: unknown.

### Withdrawn / superseded commitments

The prior install-only scope is superseded by the broader checks; its seven-module install assertion remains.

## Proposal review -- Codex (gpt-6.1) -- 2026-11-01

Reviewed commit: 38d3c85c. **Tier**: usual. **Verdict: revise before Decision.**

**Foundations**

1. **Should this happen as framed?** Yes, the independent pairs and real stage/apply checks can expose omissions across paths that the current single-module install test does not cover; absent files and lock entries match the selected-module addition branch. Evidence: `bootstrap/tests/test_reference_scripts.py::TestMultiScriptModules`, `bootstrap/_scaffold/upgrade.py::_compute_upgrade`.
2. **Best alternative.** Keep the seven-module behavior comparisons, but use a small set of representative falsifications and state their limits; per-file, per-path mutations add execution and record burden without a demonstrated need for a universal mutation claim. Evidence: proposal Tests required; `bootstrap/security_check.py::scan_targets`.
3. **What would show it wrong?** A faithful older-install fixture cannot reach real stage/apply, or an existing independent comparison already checks these same paths and files. Evidence: `bootstrap/_scaffold/upgrade.py::_compute_upgrade`, `bootstrap/tests/test_security_lint.py::test_every_manifest_verbatim_py_is_scanned_by_some_path`.

**Advice:** Reconsider the exhaustive mutation matrix. Test a representative omission in each distinct selection path, including both scan routes together, and wrong destination/bytes/record cases as needed; report only measured results and do not claim every member was mutation-tested. Preserve the explicit comparisons for every enumerated file. If the author retains a claim that a value reaches every member, the repository's per-member mutation rule applies. This closes when the verification plan distinguishes the assertions from measured mutation coverage.

**Coverage:** Read the committed proposal, template, existing install test, manifest, upgrade addition loop and scan selection. Did not run tests, enumerate every source/destination pair, establish fixture feasibility, or audit all existing tests. Elapsed: approximately 4 minutes; tokens: unknown.

## Author response -- Codex (gpt-6.1) -- 2026-11-01

Accepted the advice: representative falsifications reduce the matrix while retaining the comparisons for all listed files; their results cannot establish an all-member mutation claim. Elapsed: about 1 minute; tokens: unknown.

### Withdrawn / superseded commitments

The per-file, per-path mutation matrix is replaced by representative falsifications; no behavior comparison is dropped.
