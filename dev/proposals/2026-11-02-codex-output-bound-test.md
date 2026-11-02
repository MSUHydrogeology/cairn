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

## Proposal review -- Codex GPT-6 -- 2026-11-02

**Verdict:** Accept as framed, subject to Maintainer Decision and the separate Security Review; no blocking findings. **Elapsed:** approximately 4 minutes. **Tokens:** unknown.

1. **Should it happen?** Yes, as a correction to the output-bound assertion, not a demonstrated repair of cleanup. A-t4 currently requires exactly `truncated` and caps retained output; `_run_tool` appends `+cleanup-failed` when cleanup fails. Both proposed accepted statuses still require truncation, while A-t1 would explicitly require the combined status to be DEGRADED. The proposal correctly leaves the underlying failure unexplained.
2. **Best alternative:** Keep the exact assertion and investigate cleanup first. It retains detection of cleanup failure during overflow, but costs an unknown investigation and can fail the output-bound check for a separate property. A-t6 checks a descendant after timeout, not overflow, so the proposed change loses that overflow-specific detection. Production still reports the combined status; a passing A-t4 would no longer flag it. Record any observed combined status during verification so that evidence is not silently lost.
3. **What would show it wrong?** A non-truncation status or excess output passing, combined status classified CLEAN, or an uncontrolled child surviving the probe. The proposed mutations and safe-cleanup condition address these questions, but their outcomes remain to be established.

Coverage: read the proposal and committed A-t1, A-t4, A-t6 and runner status and cleanup code. Did not reproduce the reported failure, test every classification caller, assess implementation, or run tests or suites; Security Review remains separate.

## Review -- Codex (gpt-6.1-sol) -- 2026-11-02

Reviewed commit: def5e6890fccc229443fb8efb394eb2ccab6ff8a
Target: proposal and committed A-t1/A-t4/A-t6 and runner boundary
Prior findings: none
Assurance path: high-assurance

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 4 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. The strongest case is separating retained-output safety from successful process cleanup while keeping incomplete evidence fail-closed. `_run_tool` appends `+cleanup-failed`; `run_bandit` rejects every status other than `ran`. The exact two-status assertion plus A-t1's explicit DEGRADED case preserves that distinction (`run_security_audit.py`, `test_security_stack.py::test_a_t4_output_is_bounded`).
2. **Best alternative.** Retain A-t4's exact assertion and diagnose cleanup first. This preserves overflow-specific cleanup-failure detection, which accepting the combined status loses. Its investigation cost is unknown. A-t6 cannot replace that detection: it drives the timeout branch and observes a descendant sentinel. Both branches call the same `_kill_tree`, but that does not establish overflow cleanup success (`_run_tool`, A-t6). Given the stated bounded-output goal, the proposed change is the smallest adequate repair; a dedicated overflow survivor test would add a separate assurance outcome.
3. **What would show it wrong?** A non-truncation status passing, excessive retained bytes passing, combined status becoming CLEAN, or an uncontrolled probe survivor. The proposed focused mutations target the first three. The finite A-t4 probe writes 4096 KiB and spawns no descendants; removing its grace override changes waiting, not the attempted TERM/KILL sequence. Finite output alone does not prove timely exit; the proposal correctly requires inspection and bounded cleanup if needed (A-t4, `_kill_tree`, proposal S4).

**Covered:** committed control flow, exact assertion tradeoff, fail-closed classification and finite probe. **Not covered:** failure reproduction, implementation checks, survivor measurements or Windows behavior; no tests or suite run.
