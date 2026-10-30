# Plan: Prepare handoff before user pruning

**Source proposal**: dev/proposals/archive/2026-10-29-codex-handoff-prune.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance
**Opened**: 2026-10-30
**In brief**: Prepare and record the handoff before the user runs the guarded pruning command.

## Source proposal

The accepted proposal separates non-destructive preparation from the existing
user-run prune. It retains the marker, lock, containment and intent safeguards,
manual invocation, single ownership, and reflection-only default. A ledger
scan cannot establish that no session will append later.

## Scope

Change `tools/session.py` and its shipped twin, the canonical and shipped
session-end skills, `doctrine/session-routines.md`, their actual readers and
owning tests. Preserve the installation contract. The agent never prunes this
working repository; pruning tests use disposable repositories. No readiness
flag is persisted. No scientific check applies.

**Reuse.** Searching `tools/session.py` for handoff and prune found
`_do_reflection`, `_do_thread_survey`, `_surface_intents`, `_prune_reflections`,
`_prune_intents` and `_run_evolution_infer`; reuse their existing behavior and
preview/prompt paths. Search readers again before implementation, including
`rg -n 'session-end|session.py|handoff' bootstrap/tests scripts templates doctrine`.
The copies are intentional twins, not independent implementations.

### Documentation / doctrine surface

The skills prescribe the owner workflow; `doctrine/session-routines.md` is the
governing routine. Before changing doctrine, establish and record which trigger
in `doctrine/rationale.md` > How the doctrine evolves under evidence is met,
with its evidence. If none is established, stop and seek the Maintainer's
resolution; acceptance alone does not waive that gate. Update CLI description
and help and affected descriptive readers to match the implemented paths.

**Maintainer allowance -- 2026-10-30**: The team did not establish a doctrine-
evolution trigger. The Maintainer was asked whether implementation could
proceed under the approved handoff scope despite that missing evidence, with
the allowance recorded here. The answer authorizes proceeding; it does not
claim that a trigger was met or classify the change as high-risk.

> Proceed and record allowance (Recommended)

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Implement preparation and preserve pruning; add real-CLI tests | Plan reviews; doctrine gate before doctrine edit | Both CLI copies, skills, doctrine, affected readers and tests |
| C2 | Verify final committed implementation and hand to code review | C1 complete | Change-specific verification record and review handoff |

## Acceptance criteria

### C1

Preparation scaffolds and surveys, surfaces intents, emits capture and rate-limit
prompts and prune preview, and invokes neither prune helper nor changes either
prune target. Default remains reflection-only. `--handoff` remains guarded and
prunes eligible fixtures with marker, lock, containment and intent refusals
intact. Skills place reflection, scrub, note, custom steps and handoff commit
before checking recent unreleased claims and confirming no live appender, then
present the exact user command. If quiet is uncertain, attach the unresolved
condition to the command. Do not represent a ledger scan as proof of quiet;
user output must not imply owner judgment remains. Maintain twin parity,
interpreter resolution, terminal encoding and install/upgrade behavior.

S2: in disposable copies, independently mutate each preparation-to-pruner
boundary and marker and containment guards; record control and each mutant as
killed, survived or measured equivalent. S3: the mapped tests and gates below
run during C1 and C2. A survivor leaves the criterion open.

### C2

Record the exact clean tested commit, range, canonical interpreter and version,
pre/post state, commands, timings, counts, non-pass dispositions and omissions.
Run the disposable end-to-end sequence through the user command and record its
result. Hand the record and implementation to independent code review.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A runs the mapped tests while iterating; Boundary B repeats them at the
final clean commit in **wide** mode because the CLI and installed procedure are
contracts. Use the canonical Python 3.13 interpreter, record `Certified by:
pending`, and do not run the full certification suite here.

* CLI behavior and prompts: `bootstrap/tests/test_session_routines.py` and
  `bootstrap/tests/test_session_failsafe.py`, including new real-subprocess
  preparation, default, user-command, fresh-claim and changed-log tests.
* Containment, lock and display: `bootstrap/tests/test_session_writes_contained.py`;
  intent pruning and changed-log refusal: `bootstrap/tests/test_intents_tool.py::TestIntentSurfacePruning`;
  reflection pruning: `bootstrap/tests/test_prune_tools.py`.
* Installed paths, upgrades and consumers: `bootstrap/tests/test_skill_contract.py`,
  `bootstrap/tests/test_skills_install.py`, `bootstrap/tests/test_skills_upgrade.py`,
  `bootstrap/tests/test_skills_security.py`, `bootstrap/tests/test_next_session_local_note.py`,
  and any additional readers found by the search. Exercise both CLI copies and
  verify byte parity. Split pytest invocations within the guard's file limit and
  reconcile their union.
* Run `python scripts/claim_check.py` on changed documents,
  `python scripts/check_cairn.py`, `python scripts/link_check.py`, and
  `python scripts/quality_gate.py --sub neutrality --sub redundancy`; check
  applicable snippet synchronization. Record the doctrine gate evidence and
  mutation ledger, including unmutated controls, in the implementation record.

Boundary C is independent targeted falsification against the reviewed range and
verification record; the reviewer challenges bounding and records its verdict.


## Plan review -- Codex gpt-6.1-sol -- 2026-10-30

```
Reviewed commit: 4bf7bbcd5692a51a124542a32791e037b32cac62
Target: Source proposal through Verification
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: none

**Foundations**

1. **Should this happen as framed?** Yes: the plan carries preparation, owner judgment, conditional readiness and the user-run prune into one sequence, while retaining the doctrine gate -- `dev/plans/2026-10-30-handoff-preparation.md`, C1 and Documentation / doctrine surface.
2. **Best alternative.** Reuse the existing survey, preview and prompt paths as planned; a prose-only change cannot expose the prompts before pruning because the current dry run returns first -- `tools/session.py::_do_full_handoff`.
3. **What would show it wrong.** A real preparation invocation touching either prune target, a user command losing a guard, or a sequence presenting a ledger scan as proof of quiet would show the plan cannot deliver -- `dev/plans/2026-10-30-handoff-preparation.md`, C1 and Verification.

The acceptance criteria preserve the accepted responsibility boundary: the agent
prepares and commits the handoff, and the user receives the command with any
unresolved quiet condition attached. The proposed CLI and disposable-repository
checks cover the failure cases, including both prune boundaries and guard
mutations. The mapping names owning test files and leaves discovery of additional
readers explicit. The doctrine trigger must be evidenced before changing doctrine;
acceptance of the proposal does not itself satisfy it.

**Covered**: accepted scope and sequencing (source proposal Current contract;
plan C1–C2); failure and security boundaries (`tools/session.py::_do_full_handoff`;
plan C1); verification and consumers (plan Verification); doctrine placement
(plan Documentation / doctrine surface).

**Not covered / low confidence**: no implementation, tests or mutation runs were
examined; this ordinary pass does not clear the separate Internal Security Review.


## Plan review -- Codex gpt-6.1-sol Security -- 2026-10-30

```
Reviewed commit: c5c574d360a4cdbf5455b78e6f4f59e256f9e457
Target: Source proposal through Verification; accepted proposal Current contract
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none

**Foundations**

1. **Should this happen as framed?** Yes: C1 separates preparation from user-run deletion, retains every existing refusal and attaches uncertain quiet to the command rather than persisting readiness -- `dev/plans/2026-10-30-handoff-preparation.md`, Scope and C1; source proposal Current contract.
2. **Best alternative.** Reuse survey, prompt and preview behavior without adding a readiness token or another prune interface; the current dry-run returns before capture, so prose alone cannot deliver the accepted sequence -- `tools/session.py::_do_full_handoff`.
3. **What would show it wrong.** Preparation reaching either pruner, a bypassed marker or containment guard escaping its tests, or wording treating an earlier ledger scan as future quiet would defeat the boundary -- plan C1, S2 and Verification; intent `record_io.py::prune_released_pairs`.

The plan preserves the accepted security boundary without claiming a stronger
one. The handoff lock serializes handoffs, not ordinary intent appenders; the
intent rewrite checks the snapshot size before replacement, leaving a later
append race. C1 requires recent-claim and changed-log coverage and makes the
remaining quiet judgment explicit at the user's later run. Neither the owner
marker nor a preparation result becomes permission to delete. The agent never
runs pruning against this repository; disposable repositories contain the
end-to-end and mutation checks.

The mutation criterion is appropriately concrete: independently break each
preparation-to-pruner boundary and the marker and containment guards, retain
controls, and leave survivors open. Preserve the distinction between preview
and mutation when reusing behavior: C1 forbids preparation invoking either prune
helper, even though today's manifest obtains its reflection preview through
that helper's dry-run path. Reusing preview behavior must respect that stated
boundary. This is implementable without weakening accepted outcomes.

**Covered**: claims, fail-closed boundaries and completeness (plan C1;
`tools/session.py::cmd_session_end`, `_do_full_handoff`; intent
`record_io.py::prune_released_pairs`); public-path tests (plan Verification;
`bootstrap/tests/test_session_failsafe.py::test_handoff_without_marker_refuses_nonblocking`);
reuse, drift and consistency (named helper search in committed CLI; existing
handoff/default tests in `bootstrap/tests/test_session_routines.py`); lifecycle
and scope (accepted Current contract and Decision; plan doctrine gate, C1–C2).
No finding needs a satisfier.

**Not covered / low confidence**: no implementation or test/mutation execution;
no certifying run was duplicated. This pass clears the plan's separate Security
Review obligation, not eventual code security or future session quiet. Installed
path behavior and actual guard sensitivity remain implementation evidence owed
by C1–C2.


## Response to plan review -- Codex gpt-6.1-sol -- 2026-10-30

| Pass | Disposition |
|---|---|
| Internal | No findings; proceed with C1 and the Verification mapping. |
| Internal Security Review | No findings; retain C1’s prohibition on either prune helper during preparation, including dry-run calls. |

Both obligations are cleared. The doctrine-evolution gate remains a prerequisite
to the doctrine edit; the review does not establish its trigger.
