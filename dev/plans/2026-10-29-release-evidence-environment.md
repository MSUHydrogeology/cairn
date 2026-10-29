# Plan: Release evidence environment

**Source proposal**: dev/proposals/archive/2026-10-29-codex-release-evidence-environment.md
**Status**: awaiting-plan-review
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
