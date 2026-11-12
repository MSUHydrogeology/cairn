# Plan: Restore supported Python 3.12 workflows

**Source proposal**: dev/proposals/archive/2026-11-12-sol-python312-support.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Restore Python 3.12 operation while retaining safe process cleanup on Mac, Linux and Windows.

## Build summary

Add the missing macOS exit-observation binding inside the existing Git helper,
update its trusted callers, and check shipped workflows on Python 3.12. Keep
the current supervisor and public interfaces. Update runtime guidance; Cairn's
own final certification continues to use Python 3.13.

## Source proposal

The Maintainer accepted the heavy proposal with “Accept and prepare the plan,”
scribed at `d658b574`. Its independent ordinary and Security reviews accepted
the specified native binding. This is new compatibility work; it does not
reopen the accepted capped SafeGit fixes or replace their evidence.

## Scope

Implement the accepted proposal's complete observer specification in
`tools/git_read.py` and its byte-identical
`templates/skills/_lib/git_read.py`. Select the observer before spawning:
prefer complete `os.waitid`; otherwise use the fixed Darwin system-library
binding with the specified 104-byte structure, PID offset 12, exact owned
PID, fresh zeroed storage and flags `0x25`. Check the ABI/library/symbol before
launch. Validate signal, PID, error and child-code results; unexpected results
fail. Route all three observation sites through it. Final bounded wait alone
supplies the exit status. Preserve every ownership, group-signal, pipe, input,
cancellation, timeout and cleanup guarantee in the accepted source.

Linux keeps its existing waitid backend; Windows keeps its Job worker. Update
existing caller literals, verified bindings and installed source records
through their current delivery mechanisms. No target-selected library, fallback
that reaps before signalling, new runner or dependency is allowed.

**Reuse.** The existing helper already imports ctypes for Darwin cleanup and
owns the full supervisor. The official install manifest identifies shipped
Python files; existing public Git, session, install and module checks exercise
their callers. Reuse those instead of a compatibility framework.

### Documentation / doctrine surface

Correct README and affected runtime descriptions, including
`bootstrap/SAFETY.md` and `docs/tool-usage.md` where applicable; extend the
existing changelog topic. Preserve the distinct 3.13 certification requirement.
No new governing procedure or routine Maintainer action is introduced.

## Sequence

The native design and macOS 3.12.9 interpreter are available. The Maintainer
authorized a local Linux UTM VM and is booting the existing Windows VM; agents
prepare disposable 3.12 test environments as part of C1, with SSH and no
changes to existing project checkouts. Estimate one to two agent workdays;
environment downloads and newly discovered API incompatibilities are material
uncertainties. No passive trial or human signing step is planned.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Implement observer and restore source/installed delivery | Ordinary and Security plan reviews | Helper twins, current pins and public refusal/cleanup checks |
| C2 | Audit shipped files and exercise actual 3.12 workflows | C1 | Platform evidence, any in-scope compatibility repairs and runtime guidance |
| C3 | Review and finish | C1–C2, ordinary and Security code reviews, wide Boundary B | Fixed findings, complete release records, archived plan |

Luna executes the reviewed design. A newly needed boundary or ABI design goes
to High before implementation; a required failure remains work, not a deferral.

## Acceptance criteria

**C1.** Actual macOS 3.12 runs complete ordinary Git reads and clean up on
timeout, quiet-descendant exit, output overflow and cancellation. Unavailable
binding, invalid observation and failed cleanup never report success or leave
an owned child alive. Linux/Windows retain their backends and equivalent
affected controls on actual 3.12. Helper twins, caller pins and installed
bindings agree; untrusted executables and mismatched helper bytes still refuse.

**C2.** Audit every shipped Python file from the final manifest for 3.12 syntax
and API compatibility. Real installed public workflows cover each entry point;
imports or help output alone do not count. Session startup in a disposable Git
checkout succeeds with the intended interpreter. Fix discovered 3.12-only
failures within accepted interfaces. Record actual platform/interpreter versions
and any non-pass; none is silently replaced with simulated evidence.

**C3.** Required reviews and final checks pass; fix cheap findings, remove
scratch tests, update board/changelog and archive source/plan with links repaired.
No issue is currently assigned exclusively to this plan. Repin, re-anchor and
publication remain separate, unpassed release operations.

## Verification

The published `scaffold.py --manifest` at `db8e9fa9` lists 41 Python files and
26 main-guard carriers. `tools/_intent/__init__.py` is an internal package;
its supported facade is `tools/intent.py`. Re-enumerate the final manifest.
The public entry points to cover are:

- Under `scripts/`: api_access_security.py, bootstrap_github_labels.py,
  bootstrap_gitlab_labels.py, check_model_selection.py, claim_check.py,
  content_scan.py, content_scan_runner.py, exact_replace.py, link_check.py,
  prose_diff.py, run_portable_security_sweeps.py, run_security_audit.py,
  run_security_verification.py, sync_doc_snippets.py, test_coupling.py,
  verify_stems.py, web_hosting_security.py.
- Under `tools/`: board.py, code_map.py, evolution_infer.py, intent.py,
  meter.py, prune_intents.py, prune_reflections.py, session.py.

Use existing public workflow owners `test_reference_scripts.py`,
`test_replacement_tools.py`, `test_content_scan.py`, `test_api_access_security.py`,
`test_web_hosting_security.py`, `test_model_selection_stub.py`,
`test_board_json_contract.py`, the matching integration owners, and
`security/test_prose_tools.py` under `bootstrap/tests/`. Select one relevant
existing public workflow per entry point; use fixture policies/transports,
never real service credentials or external mutations. Document that mapping
before execution and add only an uncovered promise class.

In `bootstrap/tests/security/test_git_read.py`, retain the existing public
timeout and quiet-descendant controls, native worker positive/input, overflow,
timeout and Job-cleanup controls, and declared cancellation/refusal controls.
Extend a parameterized public refusal check for native binding/observation
failures. Keep `test_a_binding_written_on_this_machine_is_still_used` in
`bootstrap/tests/test_session_binding_untracked.py` and real session startup.
Primitive probes and debugging tests remain scratch evidence.

Run scoped iteration on actual 3.12 platforms. After independent code review,
one clean-commit **wide Boundary B** under canonical Python 3.13.13 joins mapped
helper producers/consumers, installed workflows and standing prose gates.
Coordinate shared source-pin edits and the final union with overlapping plans;
do not repeat full suites per platform or small fix. Security preflight remains
the accepted proposal's; C1 owns ABI/error/cleanup falsifiers. Scientific check:
N/A. Full release certification remains separate.
