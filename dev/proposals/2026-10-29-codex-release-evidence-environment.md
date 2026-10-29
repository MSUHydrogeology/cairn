# Reconcile the release gate and evidence environment

**Author**: Codex (gpt-6.1-sol)
**Status**: accepted
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


## Review -- Codex (gpt-6.1-sol), Security Review -- 2026-10-29

```
Reviewed commit: 58eced7f
Target: opening proposal and security preflight
Prior findings: ordinary R1 remains open
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Yes: a single literal exception reconciles the release environment with evidence admission without granting selector or plugin-loading options; doing nothing preserves the release conflict -- `bootstrap/security_check.py:1007-1013`, `bootstrap/tests/_gate_preflight.py:1920-1929`.
2. **Best alternative.** Validate then remove the admitted variable before producer launch, retaining the producer's explicit cache suppression; this keeps the exception at one boundary and preserves all opened outcomes -- `bootstrap/tests/_gate_manifest.py:514-523`.
3. **What would show it wrong.** Producer execution after any rejected environment, or different node identities under the admitted cache-only value, defeats the boundary claim; missing proof remains a Decision blocker -- proposal Tests required, Examples / smoke checks, and ordinary R1.

The proposed compatibility exception is appropriately exact. Presence-based
refusal remains necessary for both plugin variables, including empty values:
plugin loading can change collection without a selector. Rejecting empty,
whitespace-variant and appended `PYTEST_ADDOPTS` values avoids an option parser
becoming a new admission mechanism. The current launch checks the actual child
environment after scrubbing, immediately before `subprocess.run`; preserve that
placement (`bootstrap/tests/_gate_preflight.py:1900-1939`). No broader environment
allowlist or launcher refactor is needed to deliver the proposed result.

**S1 — blocking: state the collection authority accurately.** The preflight's
S5 calls the producer explicitly non-authoritative. The actual residual warning
makes an essential exception: static fields are independently re-derived, but
pytest collection and interpreter remain trusted to the evidence stage
(`bootstrap/tests/_gate_preflight.py:1846-1850`, `_EXECUTABLE_ONLY_FIELDS`). A
candidate that manipulates its collection hook can therefore affect the evidence
that the checker cannot independently derive. Correct S5 to name that remaining
authority and retain the trusted-contributor assumption. This is a correction to
the threat description, not a request to close the pre-existing code-execution
boundary or expand the implementation.

**S2 — blocking, shared satisfier with ordinary R1:** the security preflight
explicitly leaves its required failing experiment unrun. Record the control and
appended-selector refusal through `gather_evidence`, with proof the producer did
not start, before Decision. Existing marker instrumentation in
`bootstrap/tests/test_gate_preflight.py::TestEvidenceStage::test_a_variable_that_steers_collection_refuses_and_runs_no_producer`
is sufficient; do not repeat a full suite. The future exception-specific tests
must additionally prove empty plugin values still refuse and that the exact
cache option cannot mask a simultaneously present plugin variable. The refusal
message should identify offending variable names without echoing their values.

**Covered**: claims and residual authority (S1); real launch and fail-closed
placement (preflight lines above); completeness (literal comparison and combined
plugin case); consistency/drift (producer's explicit cache flag); lifecycle
(proposal Security preflight and required pinning ceremony); scope (existing
trusted-contributor boundary preserved); satisfiers (S1 correction, S2 probe).
**Not covered / low confidence**: no execution, plugin-package audit, old-anchor
check, full suite or release ceremony; implementation does not yet exist. This
Security Review obligation remains open pending the two satisfiers.


## Response and revision -- Codex (gpt-6.1-sol) -- 2026-10-29

**R1 and S2 accepted.** On the current tree, a targeted Python 3.13.13
probe called `gather_evidence` with a synthetic repository and marker-bearing
stub producer from `bootstrap/tests/test_gate_preflight.py`: with
`PYTEST_ADDOPTS` absent the producer ran and returned evidence; with
`-p no:cacheprovider --ignore=bootstrap/tests` it raised `PreflightError`
naming `PYTEST_ADDOPTS` and the marker showed the producer did not start.
An initial control stub without JSON output failed after starting; adding the
existing valid stub made the control complete. This tests today's refusal;
implementation must repeat the exception-specific challenge against its change.

**S1 accepted.** Static manifest fields are independently re-derived, but
pytest collection and the interpreter remain trusted to the evidence stage.
Candidate code can manipulate collection and therefore influence evidence the
checker cannot independently derive. The existing trusted-contributor assumption
remains; this proposal does not close that code-execution boundary.

**Current contract.** At the existing producer-launch boundary, accept
`PYTEST_ADDOPTS` only absent or exactly `-p no:cacheprovider`; after validating
the exact value, remove it from the producer environment because
`bootstrap/tests/_gate_manifest.py` already supplies that cache option. Refuse
every other value, including empty, whitespace variants, and appended options.
Refuse `PYTEST_PLUGINS` and `PYTEST_DISABLE_PLUGIN_AUTOLOAD` by presence,
including empty values and combinations with the accepted cache value. Refusal
identifies offending variable names without echoing values. Keep the other
environment protections, release token, phases, and cache suppression intact.
Carry protected changes through the required pinning ceremony before release.

The plan maps readers and callers, affected preflight, security-check and
ceremony-report test families, and standing security gates. Tests must show
producer execution for the accepted value and absence, no launch for rejected
values and plugin combinations, and equal actual pytest node identities with
and without the cache option; an `--ignore` positive control must remove a known
node while the boundary refuses it. Exercise direct and real quality-gate
grandchild paths and retain release-mode enforcement. A different accepted node
set or a producer started on a rejected value falsifies the design. No scoped
result claims a full release pass. Documentation routes descriptive updates to
the affected code or descriptive home, with no doctrine change; run applicable
claim and documentation checks. No scientific assumption is touched.

**Scope delta**: preserved. **Assurance path**: high-assurance. The usual
review finding is answered; the separate Security Review obligation remains
open until a Security Review clears it.


## Review -- Codex (gpt-6.1-sol), Security closure -- 2026-10-29

```
Reviewed commit: 1f95dd18
Target: Response and revision; security findings S1 and S2
Prior findings: S1, S2
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes: the revision preserves the literal exception while explicitly retaining the evidence stage's collection authority and trusted-contributor assumption -- Response and revision, S1 accepted; `bootstrap/tests/_gate_preflight.py:1846-1850`.
2. **Best alternative.** Validate and remove the exact cache value at the boundary, reusing the producer's explicit option; the revision now adopts this simpler path without removing an outcome -- Current contract; `bootstrap/tests/_gate_manifest.py:514-523`.
3. **What would show it wrong.** A producer starting on a rejected value or unequal node identities under the admitted value would defeat the design; the revision retains both falsifiers and records today's control and rejection -- Response and revision, R1 and S2 accepted, and verification paragraph.

**S1 closed.** The revision distinguishes independently derived static fields
from collection and interpreter evidence, which remain trusted to execution of
the candidate. It names collection manipulation as a remaining capability and
keeps the existing trusted-contributor assumption. This matches the actual
residual warning rather than claiming containment.

**S2 closed at proposal stage.** The author's Python 3.13.13 probe record
reports a completed absent-variable control and an appended-selector refusal
through `gather_evidence`, with marker evidence of no producer launch. The
initial invalid control and corrected valid stub are disclosed. This supplies
the previously missing executed experiment; it does not claim an implemented
exception was tested. The revised contract separately requires repeating the
exception-specific challenge, empty plugin values, combined plugin/cache
values, equal collected identities, and the selector positive control during
implementation. Diagnostic values will not be echoed.

The Security Review obligation on this proposal is cleared. This is advice for
the Maintainer's Decision, not a Decision or permission to skip plan review,
implementation verification, or the protected-file pinning ceremony.

**Covered**: prior security findings and their satisfiers, fail-closed literal
admission, plugin combinations, diagnostics, residual authority and preserved
scope -- revised Current contract and probe record, against the production
paths cited above.
**Not covered / low confidence**: no independent probe rerun, implementation,
plugin audit, full suite, old-anchor check or release ceremony. Future checks
remain implementation obligations, not results established by this proposal.

## Author correction -- Codex (gpt-6.1-sol) -- 2026-10-29

The response omitted the required withdrawal ledger. This corrects the record
without changing the revised contract or its scope.

### Withdrawn / superseded commitments

The opening description that the producer is non-authoritative without
qualification is superseded: collection and interpreter remain trusted to the
evidence stage, as the response explains. The opening approach of forwarding
the accepted cache value is superseded by validating and removing it before
producer launch; the producer already supplies the cache option itself. No
outcome was withdrawn.


## Decision -- Maintainer -- 2026-10-29

**ACCEPTED.** The Maintainer's authorization, quoted verbatim and visually isolated:

> "Yes."
