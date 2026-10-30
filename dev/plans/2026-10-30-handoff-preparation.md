# Plan: Prepare handoff before user pruning

**Source proposal**: dev/proposals/archive/2026-10-29-codex-handoff-prune.md
**Status**: awaiting-plan-review
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
