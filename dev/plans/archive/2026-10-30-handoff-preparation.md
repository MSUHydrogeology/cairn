# Plan: Prepare handoff before user pruning

**Source proposal**: dev/proposals/archive/2026-10-29-codex-handoff-prune.md
**Status**: archived
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


## Implementation verification -- Codex gpt-6.1-sol -- 2026-10-30

**Boundary B mode**: wide
**Certified by**: pending
**Tested commit**: `986d2164ebaf1252267fceb81b991aaf7f5e2623`
**Reviewed range**: `bf0a253d56441838c364bfccca2cffe02d1af69d` .. `986d2164ebaf1252267fceb81b991aaf7f5e2623`
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13; pytest 9.0.3; macOS.
**Pre-run state**: clean detached worktree at the tested SHA; `git status --short` was empty.
**Post-run state**: same `HEAD`; `git status --short`, `git diff --check` and `git diff HEAD --stat` were empty/clean.

Wide was used because the changed CLI and installed procedure are contracts.
The run covered both CLI copies, the real command path, intent and reflection
pruning, containment and display, skill installation and upgrade consumers,
and the next-session reader.

**Boundary B test command**:

```text
/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_session_routines.py bootstrap/tests/test_session_failsafe.py bootstrap/tests/test_session_writes_contained.py bootstrap/tests/test_intents_tool.py::TestIntentSurfacePruning bootstrap/tests/test_prune_tools.py bootstrap/tests/test_skill_contract.py bootstrap/tests/test_skills_install.py bootstrap/tests/test_skills_upgrade.py bootstrap/tests/test_skills_security.py bootstrap/tests/test_next_session_local_note.py
```

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| Mapped pytest command above | 0 | 309 passed; 0 failed, skipped, xfailed or xpassed | 15.79 s |
| `scripts/claim_check.py` on the plan, doctrine, both session-end skills, and both coordination-tier copies | 0 | All six passed; no hard flags | 0.00 s each (tool timer rounded) |
| `scripts/check_cairn.py` | 0 | 199 Markdown files; no issues | 2.15 s |
| `scripts/link_check.py` | 0 | 199 Markdown files; no issues | 0.11 s |
| `scripts/sync_doc_snippets.py --check` on those six documents | 0 | Six documents; no drift | 0.00 s (tool timer rounded) |
| `scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | Both sub-gates had 0 failures; informational findings only | 1.08 s |
| `cmp -s` for both CLI, both session-end skill, and both coordination-tier copies | 0 | All three twin pairs were byte-identical | 0.00 s (tool timer rounded) |

**Plan-specific acceptance commands**: the mapped suite includes
`test_real_cli_preparation_preserves_targets_and_user_command_prunes`. It ran
the real CLI in a disposable repository: preparation preserved an old
reflection, a claim added after preparation appeared in the next listing, the
intent log stayed unchanged during preparation, and the user-run `--handoff`
command pruned the eligible reflection after the test released the claim. The
test also confirmed the command does not report owner judgment as unfinished.
No prune ran against Cairn's working repository.

**Mutation ledger**: each mutation used its own fresh detached worktree at the
tested commit. The unmutated control was
`test_handoff_preparation_never_calls_either_pruner`,
`test_handoff_without_marker_refuses_nonblocking`, and both parameter cases of
`test_pruning_never_deletes_through_a_linked_reflections_folder`: 4 passed.

| Mutant | Result | Evidence |
|---|---|---|
| Preparation calls `_prune_reflections(..., dry_run=True)` for the reflection preview | KILLED | `test_handoff_preparation_never_calls_either_pruner` failed at the forbidden helper call. |
| Preparation calls `_prune_intents(..., dry_run=True)` | KILLED | The same test failed at the forbidden helper call. |
| Bypass the `--handoff` designation-marker check | KILLED | `test_handoff_without_marker_refuses_nonblocking` returned 0 instead of refusing. |
| Remove reflection-folder containment from `_reflection_prune_candidates` | KILLED | Both linked-folder dry-run and write cases failed to refuse. |
| Remove lock-path containment from `HandoffLock.acquire` | KILLED | `test_the_handoff_lock_is_not_created_through_a_linked_folder` failed to refuse. |

All mutation writes and any deletion attempts were confined to the disposable
worktrees or pytest temporary fixtures. No mutant survived; none was classified
equivalent.

**Doctrine gate evidence**: I did not establish recurrence, a routine-boundary
synthesis, or a recorded Maintainer high-risk classification under
`doctrine/rationale.md` > “How the doctrine evolves under evidence”.
`dev/PLANNING.md:122` records one measured 2026-10-27 pruning event. The
Maintainer's allowance and exact answer are recorded above under
“Documentation / doctrine surface”; the implementation does not claim a gate
trigger was met.

**Non-pass disposition**: Boundary B and its gates had no non-passes. During
iteration, one obsolete completion-message assertion and a first version of
the disposable CLI fixture failed; the assertion was updated to the new message,
and the fixture now copies the intent tool/package into its disposable repo.
That first fixture version created one `late.py` claim in Cairn's intent log;
I released that exact claim immediately and confirmed it no longer appeared in
the active-intent list. No prune ran. The final mapped runs passed after both
corrections.

**Known omissions**: no full certification suite was authorized or run. An
intent listing cannot prove that no live appender exists or will start later;
the skill preserves that condition for the user's guarded command.

**Implementation verified at** `986d2164ebaf1252267fceb81b991aaf7f5e2623`.


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

## Code review -- Codex GPT-6 -- 2026-10-30

```text
Reviewed commit: 7ad4a37198a83f981e0e673bc23239582f86a3af
Target: bf0a253d56441838c364bfccca2cffe02d1af69d..986d2164ebaf1252267fceb81b991aaf7f5e2623 and implementation verification at 7ad4a371
Prior findings: none
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: none

**Foundations**

1. **Does it do what it claims?** Yes: preparation gathers the preview and prompts without either prune helper; the skill puts the user command after owner judgment and calls out uncertain quiet -- `tools/session.py::_do_handoff_preparation`; `.agents/skills/session-end/SKILL.md` section 3.
2. **Best alternative.** The shared read-only candidate listing is simpler than a second preview implementation and preserves the existing guarded prune -- `tools/session.py::_reflection_prune_candidates`, `_prune_reflections`.
3. **What would show it wrong.** A preparation call reaching a pruner, an unguarded command, or contradictory mode flags reaching the CLI would break the separation -- see falsification ledger below.

**Falsification ledger** (fresh detached local clone of `986d2164`, Python 3.13.13; no current-repository prune):

* Preparation-to-pruner boundary and marker refusal: targeted `test_handoff_preparation_never_calls_either_pruner` and `test_handoff_without_marker_refuses_nonblocking` passed; the former fails if either helper is invoked. The skill argument plumbing test also passed: 3 passed in 0.23 s.
* Installed source CLI: `python templates/skills/_lib/session.py session-end --prepare-handoff --handoff` refused incompatible modes with exit 2. The recorded parity and install/upgrade tests cover propagation to the installed copy.
* Quiet and sequencing: the skill requires recent-claim checking and confirmation of no appender after the handoff commit, states a ledger scan cannot prove quiet, and attaches uncertainty to the command; the code's snapshot message agrees. The actual future quiet state cannot be established by this review.
* Evidence: the implementation record identifies the committed bytes, wide mapped consumers, guards, separate mutant results, canonical interpreter and clean state; the plan has no reached fence or deviation request requiring a Waiting line in the reviewed range.

**Bounding**: ACCEPTED -- challenged the installed CLI mode boundary and preparation-to-pruner tests; the wide record covers the named public paths and guards.

**Covered**: preparation and prune separation, workflow order and quiet caveat, CLI modes, recorded mutation and installation evidence. **Not covered / low confidence**: no full suite or actual current-repository prune; no assertion that a future intent log is quiet. The separate Security Review remains its own obligation.

## Code review -- Codex GPT-6 Security -- 2026-10-30

```text
Reviewed commit: 7ad4a37198a83f981e0e673bc23239582f86a3af
Target: bf0a253d56441838c364bfccca2cffe02d1af69d..986d2164ebaf1252267fceb81b991aaf7f5e2623; verification at 7ad4a371
Prior findings: none
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none

**Foundations**

1. **Does it do what it claims?** Yes: preparation calls the read-only candidate collector and existing read-only subprocess adapters; deletion remains in the guarded user path -- `tools/session.py::_do_handoff_preparation`, `_do_full_handoff`.
2. **Best alternative.** Keep the shared candidate collector and explicit human quiet condition; a persisted readiness flag would become stale without protecting appenders -- `tools/session.py::_reflection_prune_candidates`; `.agents/skills/session-end/SKILL.md` section 3.
3. **What would show it wrong.** Reaching a poison pruner during preparation, altering a held lock, following a linked reflection directory, or emitting a raw terminal control would defeat its safety claims -- falsification ledger below.

**Falsification ledger**: all execution used a fresh detached worktree at
`986d2164` and disposable fixture directories, Python 3.13.13. No live prune
or full suite ran.

* Independent scratch probe called `main` with `session-end --prepare-handoff --dry-run`, replacing both prune helpers with exceptions. Neither fired; a pre-existing lock stayed byte-identical, no scaffold appeared, and an old dated symlink and its external sentinel target survived unchanged.
* The same probe put ESC and newline bytes in that dated filename. The preview emitted literal `\x1b` and `\x0a`, with no raw ESC. Replacing the reflection directory with a link made the public command refuse with exit 1. Initial scratch assertions incorrectly expected newline notation `\n` and refusal exit 2; correcting those expectations yielded a passing probe, without changing production bytes.
* `python -m pytest bootstrap/tests/test_intents_tool.py::TestIntentSurfacePruning -q`: 15 passed in 0.39 s. Its recent-claim and changed-log cases supplement the independent preparation probe. The ledger rewrite still has the documented append-after-recheck race; neither the handoff lock nor an earlier listing claims to close it.
* The implementation record's five separately killed mutants cover preparation boundaries, marker, reflection containment and lock containment. Reading the committed adapters confirmed captured child output still passes through the existing terminal encoder and subprocess argv stays explicit.

**Bounding**: ACCEPTED -- challenged preparation under an occupied lock,
linked paths and hostile filenames; the wide record covers the unchanged
prune guards and installed consumers. No additional required path was found.

The marker remains an accidental-run guard. The skill puts the owner judgment
and handoff commit before the command, asks for current quiet, and requires any
uncertainty beside that command. Preparation supplies evidence, not authority
or a durable readiness state. This clears the code Security Review obligation.

**Covered**: claims, production entry and failure boundaries (scratch probe;
`tools/session.py::main`); completeness and late append risk (intent pruning
family); reuse and drift (shared candidate collector and both CLI copies);
workflow, consistency and scope (skill section 3, doctrine manual-only and
single-owner invariants, plan C1). No finding needs a satisfier.
**Not covered / low confidence**: hostile concurrent filesystem replacement,
future appender quiet and executable provenance are not established here; the
existing trust assumptions remain. No full suite or current-repository prune.


## Response to code reviews -- Codex gpt-6.1-sol -- 2026-10-30

| Review | Disposition |
|---|---|
| Ordinary code review at `8aed53f7` | Accepted; no findings; `Bounding: ACCEPTED`. No revision was required. |
| Internal Security Review at `ac3716da` | Accepted; no findings; `Bounding: ACCEPTED`. No revision was required. |

Both reviews clear their obligations. The implementation record and the
reviews agree on the bounded evidence: preparation does not prune, deletion
remains behind the user's guarded command, and a ledger listing cannot prove
that a later appender will stay quiet. No new code-review pass was triggered.


## Dispositions

Dispositions: none

No deferred follow-up remains homeless. Full-suite certification and any
current-repository prune were outside this plan's authorized work and are not
claimed as completed outcomes.
