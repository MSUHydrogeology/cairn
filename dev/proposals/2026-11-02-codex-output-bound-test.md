# Separate output-bound and cleanup assertions

**Author**: Codex (GPT-6)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — the test protects a security boundary
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Check the output limit without requiring cleanup to succeed in the same test, while retaining separate cleanup and degraded-status checks.

## Decision summary

A certification run reported that the output-bound test received `truncated+cleanup-failed` rather than `truncated`. Both report truncation, but the test currently accepts only the latter. Accept exactly those two statuses, keep the output-size assertion, and explicitly check that the former is classified as DEGRADED. This removes the assertion that cleanup succeeded in this particular output test; a separate test still checks descendant cleanup after a timeout. The reason for the reported cleanup failure is not established, and this proposal does not claim to fix it.

## Context

`bootstrap/tests/test_security_stack.py::test_a_t4_output_is_bounded` writes a flood of output and asserts both an exact status and a 64 KiB limit. Its comment records an earlier loaded-machine failure with the same combined status and adds a 60-second cleanup grace. The current certification failure is reported by the Maintainer's work session; its underlying cause has not been reproduced or established. The runner in `templates/modules/team-gated/run_security_audit.py` appends `+cleanup-failed` when cleanup fails, and its `ToolRun` contract treats that result as DEGRADED. A-t6 independently checks a descendant's sentinel after timeout; it does not prove cleanup in A-t4's overflow case.

## Proposal

In `bootstrap/tests/test_security_stack.py`, let A-t4 accept only `truncated` and `truncated+cleanup-failed` and retain its output cap assertion. Add `truncated+cleanup-failed` to A-t1's explicit status-to-DEGRADED cases. Remove A-t4's 60-second grace override so a failed cleanup does not wait a minute; the finite-output probe and the runner's normal cleanup still apply. A failed cleanup can leave a child alive, so implementation must inspect that risk and retain a safe bounded cleanup arrangement if removing the override would create an uncontrolled survivor. Keep A-t6 unchanged. No production behavior changes.

## Rationale

The status encodes two facts: truncation and whether cleanup succeeded. Requiring only the two exact truncation variants still rejects a missing truncation signal, while the explicit classification case guards against treating incomplete output as clean. The tradeoff is that A-t4 no longer detects failed cleanup by its status. A-t6 covers a different timeout scenario, not every overflow cleanup failure.

## Alternatives considered

Keep the exact assertion and diagnose or change production cleanup: this preserves that extra assertion but needs evidence of the cause and may entail a larger security change. Do nothing: no work or new risk, but certification can fail on a cleanup result even when the output bound holds. The proposed focused repair leaves any actual cleanup defect unresolved and visible in the status.

## Documentation / doctrine surface

No doctrine or adopter-facing documentation change is proposed; this deliberation stays in `dev/`, and the test stays in `bootstrap/tests/`.

## Evidence / verification plan

### Tests required

Run the focused A-t1, A-t4 and A-t6 nodes using the project Python; record interpreter, outcomes and elapsed time. A-t4 must reject statuses without truncation and output above the cap; A-t1 must reject a clean classification of the combined status. Check these with focused mutations in separate copies and record outcomes. A-t6 exercises descendant cleanup through the real runner. The Maintainer directed: “I think fixing the problem and testing it with a narrowly scoped run is sufficient. Then we move forward. We can't have stupid long testing ceremonies repeating for simple failures”. This proposes focused change verification, not another full-tree certification. The plan must resolve the applicable final integration selection against the existing Boundary B rules; this proposal does not waive a required check.

### Examples / smoke checks

Run the applicable prose checks for this proposal. The focused test nodes invoke the actual runner; no scaffold example is changed.

#### Security preflight

S1: The test supplies the probe and status cases; the runner supplies observed status and output. The output being tested supplies the observed bytes, not the expected cap or accepted statuses.

S2: Mutate the accepted truncation status or force output above the cap, and map the combined status to CLEAN; the respective tests should fail. These mutations are proposed, not yet run.

S3: The three named pytest nodes select the cases above; A-t6 covers the timeout descendant scenario only. The runner's `ToolRun` contract says “any `"...+cleanup-failed"` variant are DEGRADED”; A-t1 will exercise the proposed combined variant, not every possible variant.

S4: The production fallback remains DEGRADED when cleanup fails; this change grants no additional authority. Removing the test grace override may expose a failed cleanup sooner and must not leave a test child uncontrolled.

S5: A malicious subprocess can produce excessive output or resist termination. A cleanup failure during overflow can still leave a descendant alive; the timeout sentinel does not establish otherwise.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw or revise if a non-truncation status passes A-t4, output exceeds the cap without failure, the combined status can classify as CLEAN, or the revised test leaves an uncontrolled child. A reproducible production cleanup defect needs separate diagnosis and disposition.

## Scope delta

None; this is the opening scope.

## Assurance path

**Assurance path**: high-assurance
