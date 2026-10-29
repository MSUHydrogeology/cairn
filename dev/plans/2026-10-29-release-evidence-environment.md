# Plan: Release evidence environment

**Source proposal**: dev/proposals/archive/2026-10-29-codex-release-evidence-environment.md
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Let release evidence run with the cache-only pytest setting while refusing settings that can steer collection.

## Source proposal

The Maintainer accepted the literal cache-only exception and its evidence requirements in the source proposal's Decision. The producer still trusts candidate collection and interpreter execution; this change does not contain candidate code.

## Scope

Change `bootstrap/tests/_gate_preflight.py` and its tests at the existing producer boundary. Preserve the release token, phases, cache suppression and other environment protections. Update affected descriptive text if the reader search finds it; no governing or doctrine surface changes. Carry the protected change through the existing pinning ceremony before release, with Maintainer actions reserved to the runbook.

**Reuse.** Search for `gather_evidence`, `PYTEST_ADDOPTS`, `_release_child_env`, and `_run_order_independence` across `bootstrap`, `scripts`, `docs`, and `dev` found the existing boundary, producer, release launcher, quality-gate grandchild, preflight and ceremony tests. Reuse the boundary and producer's explicit cache option; do not introduce an option parser or duplicate launcher.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Implement exact admission and tests; reconcile affected descriptions. | Plan review and Security Review | Boundary, targeted tests and evidence. |
| C2 | Prepare protected-change packet and independent read using `bootstrap/REANCHOR_RUNBOOK.md`. | C1 verification and code review | Ceremony inputs and reader record. |
| C3 | MAINTAINER-ONLY: verifier decisions, pinning and signing under the runbook. | Maintainer authorization and runbook prerequisites | Protected-file pinning before release. |

## Acceptance criteria

**C1.** At the existing launch boundary, absent or exactly `-p no:cacheprovider` permits producer launch; remove the exact value before launch. Empty, whitespace variants, `--ignore`, and an appended selector refuse before launch. Both plugin variables refuse by presence, including empty and in combination with the accepted cache value. Diagnostics identify offending names without values. Retain release-mode enforcement and direct and real quality-gate grandchild propagation. Compare actual pytest node identities with and without the cache value; a known node disappears under `--ignore` while the boundary refuses it. Record the appended-selector mutation and passing control through `gather_evidence` with producer marker. No scoped result claims release success.

**C2–C3.** Prepare and independently read the required protected-file packet at the reviewed candidate; the Maintainer performs the runbook's verifier decisions, pinning and signing. A HOLD remains a HOLD until the runbook's required human disposition. Do not move an anchor or sign as an agent. The separate release ceremony is not implied by this plan.

Security preflight S2 and S3: C1 runs the appended-selector mutation and control through the real evidence entry point, and the mapped tests below select the changed boundary. Existing preflight S1, S4 and S5 remain as corrected in the accepted proposal; candidate collection remains trusted.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A and B use Python 3.13.x and the owning families: `bootstrap/tests/test_gate_preflight.py`, `bootstrap/tests/test_security_check.py`, `bootstrap/tests/test_quality_gate_order_independence.py`, `bootstrap/tests/test_ceremony_review_report.py`, and `bootstrap/tests/test_gate_reanchor.py`. Exercise the actual evidence entry point, release environment and real grandchild, including the node-identity and selector controls above. Search readers and callers again after edits and add any affected consumer checks. Run applicable security gates and documentation checks (`python scripts/claim_check.py` on changed documents, `python scripts/check_cairn.py`, and `python scripts/link_check.py` when documentation changes); inspect their triggers and record outcomes. Split test invocations within the guard's file limit and reconcile their union.

Boundary B is **wide** for this trust ceremony: after the final implementation commit, run the reviewed mapping on a clean unchanged commit; record tested SHA, range, interpreter, pre/post state, commands, counts, timings, non-pass dispositions, omissions and `Certified by: pending`. No full-suite certification or release run is implied; those occur only at authorized integration points. The protected-file pinning follows the runbook, not an old-anchor reconciliation invented here. Boundary C is the independent code reviewer's targeted falsification, including the recorded mutation and control.


## Plan review -- Codex (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: 82bc87e4f6c0614c7437fd538f1c64d7368dc701
Target: scope, sequence, acceptance criteria and verification
Prior findings: none
Assurance path: Internal + Internal Security Review
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** The literal admission, removal before launch, refusal cases and collection controls deliver the accepted contract, subject to completing the verification map -- source proposal Current contract and plan C1.
2. **Best alternative.** Retain the existing boundary and producer cache option; moving the option to both launchers would add paths without improving the accepted outcome -- `bootstrap/tests/_gate_preflight.py:1900-1939`, `bootstrap/tests/_gate_manifest.py:514-523`.
3. **What would show it wrong.** A different collected node set under the admitted value, or a producer start after the appended selector, would defeat the plan's stated safety outcome -- plan C1 and source proposal Current contract.

**R1 -- blocking: make standing security gates reviewable before implementation.** Verification says to run applicable security gates and inspect their triggers, but names neither the gates nor their commands or properties. The template requires the reviewed mapping to identify every standing non-pytest gate for each touched surface before implementation; leaving discovery until execution prevents this review from checking whether the map covers the protected boundary. Identify the applicable gates, their triggers and properties, or record a supported N/A after inspecting the relevant triggers. Keep the mapped tests and scoped wide Boundary B; this does not call for a full suite. -- `dev/plans/_template.md`, Verification; plan Verification.

**Covered**: accepted scope and refusal cases (source proposal Current contract and plan C1); sequencing and Maintainer fence (plan C2-C3 and `bootstrap/REANCHOR_RUNBOOK.md`); consumer and verification mapping (plan Verification and R1); reuse and residual collection authority (plan Scope and source proposal Response); lifecycle and doctrine placement (plan header and Scope). The plan follows the runbook for pinning and does not require a separate historical-anchor reconciliation.

**Not covered / low confidence**: no independent execution, complete inventory of security gates, packet preparation, release run or Security Review. This pass clears only the ordinary plan-review obligation.


## Plan review -- Codex (gpt-6.1-sol), Security Review -- 2026-10-29

```
Reviewed commit: cb949cd25fb356b93ac5a8e4923a0cdf10e4d88a
Target: security boundary, acceptance criteria and verification mapping
Prior findings: ordinary R1
Assurance path: Internal + Internal Security Review
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** Yes, subject to the standing-gate mapping below: exact admission followed by removal preserves the accepted exception without admitting option parsing or collection selectors -- source proposal Current contract; plan C1; `bootstrap/tests/_gate_preflight.py:1900-1939`.
2. **Best alternative.** Keep compatibility handling at the existing launch boundary and reuse the producer's explicit cache flag; changing the release and grandchild launchers adds surfaces without delivering another accepted outcome -- `bootstrap/tests/_gate_manifest.py:514-523`, `bootstrap/security_check.py:983-1058`, `scripts/quality_gate.py:148-177`.
3. **What would show it wrong.** A producer marker after refusal, a different admitted node-identity set, or lost release enforcement in the real grandchild defeats the plan; its criteria name these experiments -- plan C1; `bootstrap/tests/test_gate_preflight.py:858-870`; `bootstrap/tests/test_security_check.py:785-829`.

The plan keeps the security-sensitive distinctions intact: empty ADDOPTS is
refused rather than treated as absent; both plugin variables refuse by
presence, including empty and combined cache/plugin cases; diagnostics disclose
names without values. Removing only the admitted literal before launch avoids
passing redundant inherited options to the producer. The guard remains on the
actual child environment immediately before execution, after scrubbing. Scope
explicitly retains trusted candidate collection and interpreter execution;
there is no new containment claim or widened environment authority.

**S1 -- blocking, shared satisfier with ordinary R1: name the standing security
checks before implementation.** The mapped pytest families cover the named
boundary and release propagation, but “applicable security gates” still leaves
the non-pytest map unspecified. This matters concretely:
`bootstrap/security_check.py` includes the changed preflight in
`_CEREMONY_CLOSURE_PY`, and `run_bandit()` scans the derived executable surface
and refuses missing/error evidence. Name the scoped command that invokes this
check and its property without invoking the entire release runner, together
with the other applicable standing gates or evidenced N/A dispositions.
Retain C2–C3's runbook prerequisites and prior-verifier checks; do not substitute
a green pytest selection for protected-file pinning. Satisfier: fold that exact
command/property/trigger map into Verification, answering ordinary R1 and this
finding together -- `bootstrap/security_check.py:683-696`,
`bootstrap/security_check.py:856-875`; `bootstrap/REANCHOR_RUNBOOK.md`,
“Run the maintained verifier and ceremony”; `dev/plans/_template.md`, Verification.

**Covered**: claims, completeness and fail-closed cases (plan C1 and launch
boundary); real public-path and release consumers (mapped preflight,
security-check and quality-gate tests); reuse and drift (reader search for
`gather_evidence`, `PYTEST_ADDOPTS`, `_release_child_env` and
`_run_order_independence` across bootstrap, scripts and docs, confirmed against
the known preflight and release launch sites); lifecycle and scope (accepted
contract, plan C2–C3 and runbook); satisfier (S1).
**Not covered / low confidence**: no implementation execution, mutation run,
complete standing-gate inventory, candidate packet, plugin-package audit,
full-suite certification or release ceremony. This is the fresh-context
Security plan pass; the author's operative-cell fold must resolve S1 before
implementation.
