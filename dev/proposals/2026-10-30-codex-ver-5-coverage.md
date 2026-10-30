# Proposal: cover multi-script module installs

**Author**: Codex (gpt-6.1-terra), Strategy
**Status**: awaiting-review
**Review**: usual
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-10-30
**In brief**: Check that each existing multi-script module installs all its expected Python files.

## Context

The VER-5 board row in `dev/PLANNING.md` asks the Maintainer to decide the remaining scope. `bootstrap/_scaffold/install.py` derives `install_manifest()` from the core, skills, and module mappings; `bootstrap/security_check.py` uses that manifest and the lockfile derives from it. Install and upgrade also use the module mappings, with different selection and processing paths. This is shared data, not the single traversal originally requested in `dev/strategy/2026-08-05-codex-security-strategy.md` [VER-5]. No discovery mismatch has been demonstrated here.

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
