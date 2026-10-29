# Reconcile the release gate and evidence environment

**Author**: Codex (gpt-6.1-sol)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Allow the release gate's cache setting through evidence collection without allowing options that narrow the tests.

## Context

The release gate sets `PYTEST_ADDOPTS=-p no:cacheprovider` for its suite and quality-gate children in `bootstrap/security_check.py`. The order-independence check passes that environment to its pytest grandchild in `scripts/quality_gate.py`. The evidence stage in `bootstrap/tests/_gate_preflight.py` refuses any presence of that variable before starting its producer. The release failure and 0.5.0-only waiver are recorded in `dev/PLANNING.md`.

On the current tree, Python 3.13.13 running `bootstrap/tests/test_gate_preflight.py::TestEvidenceStage::test_environment_is_scrubbed_for_the_producer` passed with `PYTEST_ADDOPTS` unset and failed with exactly the gate's value, reporting the refusal. This targeted reproduction establishes the conflict; it does not establish that the complete release gate now passes.

## Proposal

At the evidence producer boundary, accept `PYTEST_ADDOPTS` only when absent or exactly `-p no:cacheprovider`; keep refusing every other value, including empty and appended options, and keep refusing `PYTEST_PLUGINS` and `PYTEST_DISABLE_PLUGIN_AUTOLOAD` by presence. Do not change the release token, release phases, cache suppression, or the producer's other environment protections. Update the refusal explanation to distinguish the accepted cache setting from collection-steering options. Carry the protected-file changes through the required pinning ceremony before release.

## Rationale

The exact value disables pytest's cache provider, which avoids release checkout byproducts; it does not select tests. A literal comparison avoids parsing or accepting a broader set of options. This leaves the release gate's existing direct-child and grandchild propagation intact and changes only the conflicting boundary.

## Alternatives considered

Passing the cache option on each pytest command instead would require changing both direct and grandchild launch paths and their propagation tests. Doing nothing leaves the release gate refusing its own valid test runs; the recorded waiver applies only to 0.5.0.

## Documentation / doctrine surface

Update the evidence-stage explanation in the affected code and any descriptive documentation found by the plan's reader search. No governing or doctrine change is proposed; deliberation stays here under `dev/` in accordance with `docs/DOCUMENTATION_PLAN.md`.

## Evidence / verification plan

### Tests required

In `bootstrap/tests/test_gate_preflight.py`, exercise the real evidence entry point with the exact value, unset value, empty value, `--ignore`, and the exact value with an appended selector; prove refused cases do not launch the producer. Retain explicit tests for both plugin variables. Exercise `bootstrap/tests/test_security_check.py` release environment and real quality-gate grandchild paths, plus the affected ceremony report tests. The plan must search all readers and callers and map the full affected test families and standing security gates. A successful collection that omits a test under an accepted environment falsifies the proposal.

### Examples / smoke checks

Use a small real pytest collection to compare node sets with the exact cache setting and without it, and demonstrate that `--ignore` removes a known node while the evidence boundary refuses it. Run applicable claim and documentation checks. The release ceremony remains a separate authorized integration point; do not claim release success from scoped tests.

#### Security preflight

* **S1:** The operator's inherited environment supplies the value; it can be controlled by the same caller whose collection is being measured. The boundary admits only one literal value, before producer launch.
* **S2:** Append `--ignore` to the accepted value: the evidence stage must refuse before launch. This prospective mutation has not yet been run; implementation must record it and the unmutated control.
* **S3:** Direct `gather_evidence` calls and the ceremony launcher reach this check before the candidate manifest producer. `bootstrap/tests/test_gate_preflight.py` exercises the refusal; the existing code's message directs the operator to unset the variable. No adopter-facing sentence is introduced by this proposal; the implementation must reconcile any existing description found by its reader search.
* **S4:** Missing or exact cache-only value proceeds; every other specified variable value refuses, so parsing failures or unexpected values gain no collection authority.
* **S5:** A caller who controls the environment can attempt to narrow collection; this blocks these named variables except the literal cache option. A caller who controls candidate test code can still alter collection; the producer is explicitly non-authoritative and independent review remains necessary.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Scope

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance
