# Proposal: cover multi-script module installs

**Author**: Codex (gpt-6.1-terra), Strategy
**Status**: awaiting-decision
**Review**: usual
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-10-30
**In brief**: Check that each existing multi-script module installs all its expected Python files.

## Context

The VER-5 board row in `dev/PLANNING.md` asks the Maintainer to decide the remaining scope. `bootstrap/_scaffold/install.py` derives `install_manifest()` from the core, skills, and module mappings; `bootstrap/security_check.py` uses that manifest and the lockfile derives from it. Install and upgrade also use the module mappings, with different selection and processing paths. This is shared data, not the single traversal originally requested in `dev/strategy/2026-08-05-codex-security-strategy.md` [VER-5]. No discovery mismatch has been demonstrated here. The scanner additionally retains a registry loop by design. `bootstrap/tests/test_security_lint.py::test_every_manifest_verbatim_py_is_scanned_by_some_path` checks manifest-to-scan inclusion, while `test_every_templates_py_on_disk_is_release_scanned` independently checks on-disk Python scan coverage subject to named exclusions. These do not prove upgrade selection agrees with fresh installation for every module; that cross-path comparison was not found or tested in this limited inspection.

`bootstrap/tests/test_reference_scripts.py` exercises the real installer and compares installed bytes with the source, but its independent multi-script expectations name only `issue-capture`. The current mapping has six other modules with multiple verbatim Python files: `claim-check`, `coordination-tiers`, `doc-drift-prevention`, `content-security`, `api-access-security`, and `web-hosting-security`.

## Proposal

Recommend adding independent expected source/destination pairs for those six modules to the existing multi-script test, including package files, so the existing real-entry-point test checks each file. Keep `issue-capture`. Do not change discovery or install behavior. The Maintainer's Decision must explicitly decide whether this narrower outcome is sufficient for VER-5; the original single traversal remains undelivered by this proposal.

## Rationale

Explicit expectations can detect a file accidentally omitted from the mapping; generating expectations solely from that mapping cannot. The shared mapping already reduces drift, while replacing distinct traversals without a demonstrated defect adds machinery and changes protected engine or scanner surfaces.

## Alternatives considered

Implement one traversal across install, manifest, scanner and upgrade: this meets the original design objective but requires a protected-surface proposal and security review, and its benefit over the existing shared mapping is unproven. Leave the test as is: cheaper, but six currently known modules lack this independent all-files assertion.

## Documentation / doctrine surface

No shipped documentation or doctrine changes proposed. The board is updated at its defined serialization point after disposition; this proposal is deliberation in `dev/`.

## Evidence / verification plan

### Tests required

Run the scoped iteration selection for `bootstrap/tests/test_reference_scripts.py` from `tools/test_tiers.py`; its `TestMultiScriptModules::test_multi_script_module_installs_all_scripts` must exercise all seven modules through the scaffold entry point and verify each independently listed destination and bytes. A missing or altered installed file must fail the corresponding assertion. Apply Boundary B after review on the clean final commit, with the required evidence recorded here.

### Examples / smoke checks

Run the applicable prose gates on this proposal. No full-tree certification is requested.

#### Security preflight — five questions, answered in writing

N/A: no trust boundary added or widened.

## Signals the change is wrong

An existing independent test already proves the same files and behavior, or an observed discovery mismatch makes the test-only scope insufficient.

## Scope delta

**Scope delta**: preserved for this proposal. The separate original VER-5 single-traversal objective is not delivered; its disposition belongs to the Maintainer.

## Assurance path

**Assurance path**: standard. The change adds test expectations without changing the install contract, executable, or trust boundary.

## Proposal review -- Codex (gpt-6.1-terra) -- 2026-10-30

**Verdict: revise before Decision.** The proposed tests are useful, but their passing would not establish the board's consistent-discovery outcome across all four paths.

**Foundations.** Should it happen as framed? Not yet: the test at `bootstrap/tests/test_reference_scripts.py:125-153` exercises fresh installation and bytes only; it does not compare upgrade or scan discovery. The board's VER-5 row asks for consistency across install, manifest, security scan and upgrade. Best alternative: retain the small test-only change, and first assess existing cross-path tests or add the smallest independent behavior check that can expose an actual disagreement; the shared `_MODULE_MAPPINGS` already supplies install, manifest and upgrade, and `security_check.py` selects Python sources from `install_manifest()`. A new traversal could reduce duplicated selection logic but changes protected surfaces without a demonstrated mismatch. What would show this wrong? Evidence that existing checks already cover the relevant cross-path selection differences, or a mismatch showing that a shared traversal is needed.

**Finding (advice):** Make the loss and evidence for the Maintainer's choice concrete: identify which selection differences and paths are checked or remain unchecked, and whether a small behavior test covers them. The independent file list detects omissions in install mapping but cannot detect drift in upgrade selection or scanner filtering. The Maintainer alone can accept the loss of the original single traversal. No demonstrated mismatch makes this a blocking finding.

**Coverage:** Read the proposal, VER-5 strategy and board row, install and manifest loops, upgrade mapping uses, scanner manifest selection, and the existing multi-script test at `5aac7f02`. Did not run tests or audit all existing cross-path coverage. Elapsed: about 2 minutes; tokens: unknown.

## Author response -- Codex (gpt-6.1-terra) -- 2026-10-30

Accepted the advice to make coverage and its limits explicit. The existing scanner checks provide meaningful cross-path and independent disk evidence; the proposed independent install expectations address a different gap. An all-module upgrade comparison would add a new test without evidence of a mismatch, so it is not proposed. The Maintainer can instead choose the original traversal or request further comparison; the single-traversal outcome remains explicitly unfulfilled. Elapsed: about 2 minutes; tokens: unknown.
