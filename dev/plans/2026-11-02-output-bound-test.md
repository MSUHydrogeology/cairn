# Plan: Separate output-bound and cleanup assertions

**Source proposal**: dev/proposals/archive/2026-11-02-codex-output-bound-test.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Check the output limit separately from cleanup success while preserving degraded-status reporting.

## Source proposal

The accepted heavy proposal separates the output-bound assertion from cleanup success, adds explicit classification coverage, and preserves a safe bounded test cleanup arrangement. It makes no production change and does not establish why the reported cleanup failure occurred.

## Scope

Change `bootstrap/tests/test_security_stack.py`: update A-t4 and A-t1, inspect the effect of removing A-t4's cleanup grace override, and retain bounded cleanup if needed. Keep A-t6 unchanged. No doctrine surface or adopter-facing documentation changes.

**Reuse.** A search for `output_is_bounded`, `boundary_failure_status_is_degraded`, `descendants_do_not_outlive`, and `_kill_tree` found the existing A-t1, A-t4 and A-t6 tests and runner cleanup in `templates/modules/team-gated/run_security_audit.py`; extend those tests rather than add a parallel harness.

### Documentation / doctrine surface

No doctrine surface.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Make the focused test correction and establish safe bounded cleanup | Plan review: Internal and Internal Security Review | Test changes and focused iteration evidence |
| C2 | Independent code and Security Review, then final focused verification | C1 committed | Review and final verification records |

## Acceptance criteria

### C1

- A-t4 accepts only `truncated` and `truncated+cleanup-failed`, retains the 64 KiB output limit, and removes the 60-second grace override. Inspect survivor risk and retain a safe bounded cleanup arrangement if needed; finite output alone does not establish timely exit.
- A-t1 explicitly requires `truncated+cleanup-failed` to classify as DEGRADED; A-t6 remains unchanged. Production behavior is unchanged.
- Focused mutations in separate copies show A-t4 rejects a non-truncation status and excess output, and A-t1 rejects CLEAN classification of the combined status. Record outcomes and any observed combined status.

### C2

- Independent ordinary and Security Reviews address the committed implementation; the final focused run covers review fixes and records the result and omissions.

## Scope delta

**Scope delta**: preserved. The Decision accepts the proposal's stated loss: A-t4 no longer detects overflow-specific cleanup failure by its status; A-t6 tests timeout cleanup, not that overflow case. Maintainer allowance (chat, 2026-11-02): “Go ahead, I am okay with it. I want to move forward to repinning and release”.

## Verification

The Maintainer directed: “I think fixing the problem and testing it with a narrowly scoped run is sufficient. Then we move forward. We can't have stupid long testing ceremonies repeating for simple failures”. Run A-t1, A-t4 and A-t6 with the project Python and the focused mutations above, recording interpreter, outcomes, elapsed time and observed combined status. After review, repeat the focused nodes on a clean final implementation commit, recording pre/post state, tested SHA, reviewed range, command counts, non-passes and omissions. This is the authorized narrow selection, with no repeated full or wide suite for this correction. Reviewers run only targeted falsification checks. Applicable prose checks cover the plan and proposal.

## Plan review -- Codex (GPT-6), fresh reviewer -- 2026-11-02

Reviewed commit: d2153fec. **Obligation**: Internal. **Tier**: Internal.
**Verdict**: ACCEPT. **Findings**: none. **Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should it happen as framed?** Yes. C1 carries the accepted exact statuses, output cap, explicit DEGRADED classification and bounded-cleanup condition; C2 preserves both independent reviews. The Maintainer's Decision accepts the narrower verification and the overflow-specific coverage loss (proposal Decision; plan C1–C2 and Verification).
2. **Best alternative:** Keep the exact status and diagnose cleanup first. That preserves detection of overflow cleanup failure, but investigation cost is unknown and the Maintainer accepted its loss for this correction. A-t6 checks timeout descendants, not overflow (proposal Context and Decision; committed A-t4 and A-t6).
3. **What would show it wrong?** A non-truncation status or excess output passing, a combined status classifying CLEAN, or an uncontrolled probe survivor. C1 requires focused mutations for the first three and inspection with bounded cleanup if needed for the last; outcomes remain to be measured.

**Covered:** accepted scope, sequence, focused checks and stated coverage loss against the committed proposal, plan and test nodes. **Not covered:** executing tests, establishing the reported failure's cause, implementation results or the separate Internal Security Review.
