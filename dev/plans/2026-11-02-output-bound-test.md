# Plan: Separate output-bound and cleanup assertions

**Source proposal**: dev/proposals/archive/2026-11-02-codex-output-bound-test.md
**Status**: revising-code
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


## Plan review -- Codex (gpt-6.1-sol) -- 2026-11-02

Reviewed commit: d2153fece47f5f84060a41accd31750c055732c4
Target: operative plan against accepted proposal and runner/test boundary
Prior findings: none
Assurance path: high-assurance

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 3 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. C1 preserves the accepted safety controls: exact truncation statuses, a fixed output cap, explicit DEGRADED classification and bounded probe cleanup. It explicitly rejects finite output as proof of timely exit. The runner still appends cleanup failure and reports incomplete evidence; no production change is planned -- plan C1; accepted proposal Decision; `templates/modules/team-gated/run_security_audit.py::_run_tool`.
2. **Best alternative.** Keep the existing A-t4 harness and change only its assertions. That is smaller, but retains a 60-second grace and cannot deliver the accepted removal or bounded-cleanup inspection. Reusing the existing finite probe with a bounded cleanup arrangement, only if needed, delivers the same outcomes with less continuing burden than a separate harness -- plan Scope and C1; `bootstrap/tests/test_security_stack.py::test_a_t4_output_is_bounded`.
3. **What would show it wrong.** A non-truncation result or excess output passing A-t4, combined status classified CLEAN, or an uncontrolled survivor would defeat the plan. The required focused mutations target assertion failures; cleanup inspection remains required because A-t6 exercises timeout, not overflow. Recording any observed combined status prevents silently claiming cleanup success -- plan Acceptance criteria and Verification; A-t1/A-t4/A-t6; runner `_kill_tree`.

Covered: committed plan, accepted loss and focused-check authorization, test controls and production cleanup/status paths. Not covered: implementation, failure reproduction, measured survivor behavior or Windows; no tests or suites run.

## Plan review response -- Codex (GPT-6) -- 2026-11-02

**Elapsed**: approximately 1 minute. **Tokens**: unknown.

Both the Internal and Internal Security Review accepted the plan without findings. No operative changes are needed. Proceed with C1 and its focused verification.


## Implementation verification -- Codex (GPT-6) -- 2026-11-02

**Stage**: C1 focused iteration; Boundary B remains due after review.
**Boundary B mode**: bounded. Touched only A-t1 and A-t4 in
`bootstrap/tests/test_security_stack.py`; A-t6 exercised as the existing
cleanup consumer. No production code changed. The three focused nodes cover the
status mapping, output cap/status and timeout descendant cleanup.
**Tested commit**: `092712a69ccf8b9d6a58f8f286f90d66bb7d2001`.
**Reviewed range**: `4c482332`..`092712a6`.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13.
**Pre-run state**: clean detached copy at the tested commit.
**Post-run state**: clean detached copy; `HEAD` remained the tested commit.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_security_stack.py::test_a_t1_boundary_failure_status_is_degraded_never_clean bootstrap/tests/test_security_stack.py::test_a_t4_output_is_bounded bootstrap/tests/test_security_stack.py::test_a_t6_descendants_do_not_outlive_the_timeout` | 0 | 3 passed; 0 failed/skipped/xfail/xpass | 6.38 s | unknown |
| Separate A-t4 status mutation (`overflowed` never classifies as truncated) | 1 | Expected failure: status `ran` rejected | 0.14 s | unknown |
| Separate A-t4 cap mutation (read entire output file) | 1 | Expected failure: 4,194,304 bytes exceeded 65,536 | 0.42 s | unknown |
| Separate A-t1 tier mutation (combined status classified CLEAN) | 1 | Expected failure: `truncated+cleanup-failed` mapped to CLEAN | 0.12 s | unknown |
| Instrumented A-t4 observation on a separate clean copy | 0 | 1 passed; observed status `truncated` | 0.22 s | unknown |

**Non-pass disposition**: The three mutation failures are expected and show the
assertions reject those faults. The clean focused run had no non-passes.
**Plan-specific acceptance commands**: A-t1, A-t4 and A-t6 nodes above; all three
required mutations were detected.
**Prose gates**: `python scripts/claim_check.py dev/plans/2026-11-02-output-bound-test.md` and `python scripts/link_check.py dev/plans/2026-11-02-output-bound-test.md` passed. `python scripts/quality_gate.py --sub neutrality` passed with 0 failures and 43 informational findings; no snippet block was added.
**Known omissions**: The process-level run observed `truncated`; the
`truncated+cleanup-failed` status was exercised synthetically by A-t1 and allowed
by A-t4, but was not observed from a real overflow run. Boundary B must repeat
the focused nodes after review. No full suite or broad selection ran.

## Code review -- Codex (GPT-6), independent reviewer -- 2026-11-02

Reviewed implementation `092712a6` and evidence `81cb545b`. **Verdict**: REVISE. **Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should it happen as framed?** Yes, subject to C1's survivor-risk condition. A-t4 retains the cap and accepts exactly the two accepted statuses; A-t1 explicitly checks DEGRADED, and A-t6 and production are unchanged. Focused mutations reported in the implementation record reject the three named faults.
2. **Best alternative:** Retain the exact cleanup-status assertion and diagnose cleanup first; it detects overflow cleanup failure but costs an unknown investigation. The Maintainer accepted losing that detection, and A-t6 covers timeout rather than overflow (proposal Decision; A-t6).
3. **What would show it wrong?** A non-truncation status or excess output passing, combined status mapping CLEAN, or an uncontrolled probe survivor. The recorded mutations address the first three, while survivor safety remains unresolved below.

**R1 -- blocking: record and resolve survivor risk.** C1 requires inspection of the effect of removing the grace override and a safe bounded cleanup arrangement if needed; finite output alone does not establish timely exit. `_kill_tree` has bounded waits but can return false, and the focused run observed only `truncated`. The implementation record does not explain whether the probe can survive uncontrolled in that case or how it is bounded if so. Inspect the failure paths and record evidence supporting the safety conclusion; provide bounded cleanup if needed. This finding does not request a broad suite.

**Covered:** committed test diff, accepted criteria, runner cleanup path and implementation evidence. **Not covered:** independent test execution, Windows behavior, failure reproduction or separate Security Review. Final focused verification remains due after review.


## Code review -- Codex (gpt-6.1-sol), Security Reviewer -- 2026-11-02

Reviewed implementation: 092712a69ccf8b9d6a58f8f286f90d66bb7d2001
Evidence: 81cb545b. Prior finding: ordinary review R1 remains open for author disposition.
**Tier**: Security Review. **Verdict**: no additional findings; R1 remains open.
**Elapsed**: approximately 6 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Exact truncation statuses and the independent literal cap remain; A-t1 requires the combined status to be DEGRADED. Production and A-t6 are unchanged. The ordinary review correctly requires an author-owned survivor-risk disposition -- committed test diff; plan C1; implementation evidence.
2. **Best alternative.** Add a separate cleanup harness only if inspection finds it needed. This probe imports only `sys`, has no descendants or signal-handler changes, and writes to regular capture files. Existing `_kill_tree` retains bounded TERM/KILL phases. This supports keeping the existing arrangement for the cooperative probe, but does not prove every cleanup-failure path safe -- A-t4 probe; runner `_run_tool` and `_kill_tree`.
3. **What would show it wrong?** Uncontrolled survival or false acceptance would defeat it. On an isolated archive of the reviewed commit under Python 3.13.13, one real A-t4 call returned `truncated`, retained 65,536 bytes, and its sole captured subprocess was reaped with return code 0 at return (0.067 seconds). Six synthetic controls accepted both exact statuses at the cap and rejected `ran`, `timeout`, `truncated+arbitrary`, and 65,537 bytes. Author mutations also reject combined-status CLEAN classification -- A-t4; implementation evidence.

**Bounding**: ACCEPTED for the authorized focused selection; R1's required safety disposition remains outstanding.

Covered: exact controls, real cooperative-probe reaping, static spawn/signal behavior and reported mutations. Not covered: an actual `truncated+cleanup-failed` run, survivor behavior under failed signaling, Windows or reported-failure reproduction; no suite run. Final focused verification remains due.


## Code review response -- Codex (GPT-6) -- 2026-11-02

**R1**: addressed in `45fd24c4` and `95ecf237`. The A-t4 probe has no
children and now sleeps for two seconds after its fixed 4 MiB write loop, so
its direct process remains alive when overflow cleanup starts. A test-local
wrapper preserves `_kill_tree`'s boolean, then sends direct kill and waits at
most one second if the Popen is still alive. The test requires cleanup to run
and the process to be reaped. Returning `False` from the runner cleanup still
produces `truncated+cleanup-failed`; A-t4 accepts it and the A-t1 test checks
that it maps to DEGRADED. Production code and A-t6 are unchanged.

**Focused evidence**: on a clean detached copy at
`95ecf2373fce8b1ecab4d05e131d79867a64b760`, Python 3.13.13,
A-t1/A-t4/A-t6 passed (3 passed, 11.46 s). In a separate copy, a runner
mutation returned `False` without killing the direct child; A-t4 required and
observed `truncated+cleanup-failed`, passed in 0.28 s, and its reaping assertion
passed. The probe's source has no spawn or signal-handler calls. A real OS
signaling failure was not induced; Windows was not exercised. Tokens: unknown.

**Prose gates**: claim and link checks passed for this plan; neutrality reported 0 failures and 43 informational findings. No snippets changed.

**Next**: targeted code review of `95ecf237` and focused evidence, then repeat
the three nodes on the final clean reviewed commit for Boundary B.

## Targeted code review -- Codex (GPT-6), independent reviewer -- 2026-11-02

Reviewed fixes `45fd24c4` and `95ecf237` and response `93231bfb`. **Verdict**: ACCEPT; R1 closed. **Elapsed**: approximately 2 minutes. **Tokens**: unknown.

**Foundations**

1. **Should it happen as framed?** Yes. The test-local wrapper preserves the runner's cleanup boolean, and if the direct probe remains alive it kills and waits for it with a one-second bound. The test requires cleanup and a reaped process; production and A-t6 remain unchanged. The author reports a forced runner-cleanup failure that exercised the fallback and retained `truncated+cleanup-failed`.
2. **Best alternative:** Rely on the finite probe and existing runner alone. That adds no wrapper but does not establish timely exit on a failed cleanup; C1 requires the risk to be resolved. The test-local fallback addresses the direct child without adding production behavior.
3. **What would show it wrong?** A live probe after the fallback or a changed runner status would defeat the fix. The recorded forced-failure run checks reaping and the combined status; it did not induce a real OS signaling failure.

**Covered:** committed fix, R1 response, reported focused checks and retained status semantics. **Not covered:** independent execution, actual OS signaling failure, Windows or the separate Security Review. Final focused verification remains due.
