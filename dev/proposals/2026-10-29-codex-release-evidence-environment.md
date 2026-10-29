# Reconcile the release gate and evidence environment

**Author**: Codex (gpt-6.1-sol)
**Status**: revising
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


## Review -- GPT-6.1 Sol -- 2026-10-29

```
Reviewed commit: 9eff8888d1f0c7f20d2dde812f9f6e542adda2a9
Target: opening proposal
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Yes: the release command manufactures the value the evidence boundary refuses; the literal exception repairs that conflict without admitting selectors -- `bootstrap/security_check.py:1007-1013`, `bootstrap/tests/_gate_preflight.py:1920-1929`.
2. **Best alternative.** Put the option in the release suite and quality-gate pytest argument lists, retaining unconditional refusal. This avoids an environment exception but changes two launchers and propagation expectations; the proposed literal exception is smaller -- `bootstrap/security_check.py:1034-1037`, `scripts/quality_gate.py:158-175`.
3. **What would show it wrong.** A changed collected node set under the admitted value, or producer execution after an appended selector, defeats the safety claim; compare node identities, not counts -- `bootstrap/tests/_gate_manifest.py:498-523`, proposal Examples / smoke checks.

The strongest case is a narrow repair of a real release blocker. Doing nothing
preserves a refusal but leaves the release command unable to complete under
its own environment; the recorded waiver covers only 0.5.0
(`dev/PLANNING.md:125`). The trigger is the Maintainer running
`python bootstrap/security_check.py`, whose suite and quality-gate subprocesses
receive `_release_child_env`; `_run_order_independence` copies that environment
to pytest. This is not an automatic release check.

**R1 — blocking: supply the security preflight's failing experiment.** S2
explicitly says its mutation has not been run, whereas
`dev/proposals/_template.md` requires confirming the failing probe was run.
The recorded unset/exact conflict proves the defect, not that the selector
refusal still stops execution. Before Decision, record a scoped control and
an appended-selector refusal through `gather_evidence`, including the
producer-not-started observation. Existing
`bootstrap/tests/test_gate_preflight.py::TestEvidenceStage::test_a_variable_that_steers_collection_refuses_and_runs_no_producer`
shows an available marker-based instrument. The future implementation's
exception-specific mutation remains required; no whole-suite run is needed
to close this proposal finding.

**Non-blocking simplification.** The producer already supplies
`-p no:cacheprovider` explicitly in `_gate_manifest._collect`. Consider removing
the admitted literal from its child environment after validation rather than
forwarding it redundantly (`bootstrap/tests/_gate_manifest.py:518-522`). This
preserves every proposed outcome and confines compatibility handling to the
boundary; it does not justify accepting any additional value.

**Covered**: claims and production path (launch sites above); completeness and
fail-closed behavior (Proposal and R1); consistency and drift
(`dev/PLANNING.md:125`, `_gate_manifest._collect`); lifecycle placement
(Security preflight and pinning requirement); domain/scope (no scientific
change; literal exception only); satisfier (R1's recorded probe).
**Not covered / low confidence**: no independent execution or complete release
run; no implementation exists to assess. This usual pass does not clear the
separate Security Review obligation.
