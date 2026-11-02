# Plan: Prepare a forward AST correction

**Source proposal**: dev/proposals/archive/2026-11-02-codex-forward-ast-preparation.md
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Prepare and review current code fingerprints for a Maintainer-approved forward baseline without reconstructing prior history.

## Source proposal

The Maintainer accepted the heavy proposal and its explicit loss of historical AST certification. It authorizes implementation, not a correction, baseline installation or signing.

## Scope

Extend the explicit forward path in `scripts/repin.py`, its `bootstrap/tests/test_repin.py`, `bootstrap/tests/test_repin_ceremony.py` and `bootstrap/tests/test_ast_attest.py` coverage, and `bootstrap/AST_BASELINE_RUNBOOK.md` and `bootstrap/REANCHOR_RUNBOOK.md`. Clarify `AGENTS.md` only if its correction rule conflicts. Preserve ordinary historical correction, release certification and baseline-install requirements. Add no trust store, ledger or manual JSON workflow.

**Reuse.** Search `scripts/repin.py` for `baseline_reader_inputs`, `build_transaction`, `apply_reviewed_pin` and `commit_reviewed_pin`: the existing classification, transaction, binding and exact-path commands are the starting point. Extend their mechanisms in explicit forward mode; identify only fields needed to bind two independent reviews and exact inputs.

### Documentation / doctrine surface

Runbooks describe the maintained ceremony; any necessary governing permission belongs in `AGENTS.md`. The existing Maintainer authority and fences remain.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Implement forward preparation, review binding and one documented resumable guided entry point with focused tests. | Both required plan reviews and author response | Maintained commands, documentation and disposable workflow evidence. |
| C2 | Independent code and Security Reviews, response and final integration. | C1 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** Explicit preparation reads one committed candidate without loading or comparing a historical anchor, preserves baseline membership, and writes only a new external evidence directory. The packet binds candidate, canonical interpreter, tool and fixture hashes, changed bodies/locations, proposed digest replacements and known-new delta; it states that history is not certified. Missing or duplicate symbols and lockfile correction refuse. Fresh ordinary and Security reviewers examine current behavior, protection machinery and checks; their records and the exact transaction are bound before application. One documented, resumable guided entry point presents concrete approval, revalidates inputs, applies only reviewed fixture paths, separately confirms the exact-path commit, and directs the Maintainer to the existing final baseline approval and signing. It resumes after independent reviews without manual JSON or undocumented commands. No manual JSON or repository write occurs during preparation; no baseline is installed or signed by preparation. Ordinary paths stay strict.

**C2.** Ordinary and separate Security Reviews assess the committed implementation; the machinery checks pass, including wide Boundary B within the baseline exclusions below. Hashes identify bytes, not reviewer independence or safety.

Actual correction approval, exact-path commit and later baseline approval/signing are Maintainer-only steps outside this implementation; they require their own concrete approvals and existing ceremony controls. This plan authorizes none of them.

## Scope delta

**Scope delta**: The Maintainer directed: “Plans complete BEFORE v0.6 is ready”, “They can each build the machinery, the new baseline does not need to be part of their plans. It can be a work board item for v0.6”, and “Remove those requirements from the plans”. The Maintainer also directed no old-anchor checks. The four baseline/real-anchor-dependent nodes named in the implementation verification below are outside this plan’s completion checks and remain unpassed; the existing v0.6 baseline work-board item is their home. This does not authorize a baseline, correction, signing or historical certification. Other accepted machinery outcomes and checks remain in scope.

## Verification

`python tools/test_tiers.py for scripts/repin.py bootstrap/tests/test_repin.py bootstrap/tests/test_repin_ceremony.py bootstrap/tests/test_ast_attest.py bootstrap/AST_BASELINE_RUNBOOK.md bootstrap/REANCHOR_RUNBOOK.md` selects ten files, including the three named command and AST tests, re-anchor, gate and review consumers. Remap all final paths, including any governing change with its reviewed range; inspect readers and byte pins. Run mapped iteration checks and applicable claim, link, snippet, neutrality and `python scripts/check_cairn.py` gates.

C1 exercises the documented guided entry point end to end in disposable repositories, including a pause and resume after independent reviews, correction approval, exact-path commit confirmation and handoff to the existing baseline approval/signing without signing or moving real refs. It also exercises real commands for: no prior anchor, unchanged ordinary refusal, missing/duplicate and lockfile-debt refusal, no preparation writes, unreviewed packet refusal, and reviewed-path-only apply/commit. Separately mutate candidate, transaction/packet, review binding and target fixture; each must refuse. The in-scope `bootstrap/tests/test_ast_attest.py` checks exercise membership and digest handling; the two committed-baseline nodes are excluded as named below. These tests are S2/S3; report outcomes and omissions concisely. No real refs move and no signing occurs in tests.

Boundary C is independent ordinary and Security code review, examining affected engine behavior and protection machinery as well as the packet. After fixes, wide Boundary B on a clean unchanged final commit under canonical Python 3.13 covers mapped iteration and integration/workflow tests, owning families, public command paths, standing gates and the disposable workflow, except the four baseline/real-anchor-dependent nodes identified in Scope delta and the implementation verification. Record SHA/range, interpreter, pre/post state, commands, counts, timing, tokens, non-pass dispositions and omissions. Combine overlapping checks only on the same reviewed commit without dropping coverage. Full certification and actual baseline ceremony remain separate authorized work; do not run another full suite for this plan.

## Plan review -- Codex (GPT-6), Reviewer -- 2026-11-02

**Obligation**: Internal  
**Verdict**: revise one blocking acceptance gap before implementation.

**Foundations.** (1) The plan should proceed: C1 preserves the accepted forward-only boundary, two independent reviews, exact-input checks and separate Maintainer approvals. Its disposable workflow and mutation checks exercise these promises. (2) The best alternative is to extend the existing transaction and apply/commit mechanisms behind one guided entry point, resuming after independent reviews as needed. This retains the required approvals without a parallel process; direct fixture edits would lose the scripted checks. (3) An end-to-end run that consults an old anchor, requires manual JSON or undocumented commands, accepts altered or unreviewed input, or cannot reach the existing baseline workflow would show the approach wrong. The verification section tests most of these, but does not require a user-facing guided flow through all steps.

**Blocking finding:** C1 says the script presents approval and separately confirms the commit, while the sequence only promises “maintained commands.” The accepted proposal requires a documented maintained script to guide the Maintainer's steps, and the requested outcome is a single user-friendly command. Multiple undocumented handoffs could satisfy the present wording while leaving the Maintainer to assemble the workflow. Close by requiring one documented, resumable guided entry point covering the correction approvals and directing the user to the existing final baseline approval/signing, with an end-to-end disposable test demonstrating the guidance. Keep review and signing boundaries intact; do not add a new ceremony.

**Coverage:** Read the plan and accepted proposal at `451281cc`, including the Decision and both proposal reviews. Did not execute tests, inspect every implementation consumer, or assess the full security threat model; the separate Security Review addresses that boundary. Elapsed: approximately 3 minutes. Tokens: unknown.

## Response to ordinary plan review -- Codex GPT-6.1 Sol -- 2026-11-02

Blocking finding accepted: C1 now requires one documented resumable entry point and its disposable end-to-end test, including the existing signing handoff. Independent review and Maintainer approvals remain unchanged; no new ceremony is added. Separate Security plan review remains outstanding. Elapsed: approximately 2 minutes; tokens: unknown.

## Plan review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: ffa0c2f966d88d75a20cde18315cf604907ca0ff  
Target: revised forward preparation, guided flow and approval boundaries  
Prior findings: ordinary guided-entry blocker read  
Assurance path: high-assurance

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none  
**Verdict**: ACCEPT  
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. C1 binds one committed candidate, interpreter, tools, fixtures, symbol deltas, transaction and both current-state reviews before Maintainer application. Preparation writes only external evidence, never installs or signs, and refuses missing/duplicate symbols or lockfile debt. Historical comparison is explicitly excluded rather than silently bypassed. -- Plan, C1, Scope and Verification; accepted proposal/Decision.
2. **Best alternative.** Reuse classification and exact-path transaction/apply/commit mechanisms behind the single resumable guide. This avoids manual JSON, a parallel trust store and historical reconstruction while preserving separate approval and commit confirmation. -- Plan, Reuse and revised C1; existing repin entry points; ordinary response.
3. **What would show it wrong?** A resumed flow accepting mutated or unreviewed inputs, preparation changing fixtures, or a guide requiring undocumented commands or old-anchor setup. The real-command matrix separately mutates candidate, transaction/packet, review binding and fixtures, and the disposable pause/resume workflow exercises the complete guide and signing handoff. -- Plan, Verification and C1; proposal S1–S4.

No blocking finding. The ordinary blocker is addressed by the documented resumable entry point and end-to-end acceptance check. Hashes are correctly limited to identity, not reviewer independence or safety. Current engine behavior and protection machinery remain review subjects; ordinary historical commands, actual Maintainer approvals and final baseline signing retain their own controls. No new authority system is needed.

Coverage: examined committed revised plan, accepted proposal/Decision, ordinary finding/response, current plan template and existing reuse entry points. Did not reproduce selector output, audit future implementation, run adversarial controls or execute suites. Final wide verification and the separate actual baseline ceremony remain owed; this review authorizes neither correction nor signing.

## Response to Security plan review -- Codex GPT-6.1 Sol -- 2026-11-02

The Security review accepted the revised plan without findings. Independent Security code review, disposable adversarial checks and wide final verification remain required; actual correction and signing require separate Maintainer approval. Elapsed: under one minute; tokens: unknown.

## Iteration evidence -- Codex GPT-6.1 Terra -- 2026-11-02

Implementation `4b066389` produced two failed forward checks. On a separate committed copy, I reproduced the duplicate-symbol acceptance (one failed, one passed) and stopped the altered-binding check after eight seconds when it reached a prompt. Correction `496a720d` refuses duplicate named definitions in forward mode and requires exact review-binding lines; the refusal test now has a bounded timeout.

On an isolated copy of `496a720d` under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13), the previously failing nodes passed all three cases in 3.58 seconds. `python -m pytest bootstrap/tests/test_repin.py -k forward -q` passed 10 tests, with 114 deselected, in 11.97 seconds. This selection exceeds the 10-second per-file diagnostic target; add the file to the consolidation list at the appropriate serialization point. The full mapped iteration selection and plan-specific security and workflow checks are not yet complete. Two real-tree AST gate failures were independently diagnosed at `f8379e9` before the stray prose edit; they are not attributed to that edit. No full suite, real baseline installation, signing or anchor move was run. Independent ordinary and Security code reviews and final wide Boundary B remain owed. Elapsed: approximately 8 minutes; tokens: unknown.

## Code review -- Codex (GPT-6), Reviewer -- 2026-11-02

**Reviewed**: implementation `4b066389`, correction `496a720d`, evidence `5d6ea8c7`.  
**Verdict**: revise; required implementation checks remain unmet.

**Foundations.** (1) The approach is appropriate: `forward_context` extracts one commit without reading an anchor; the guide rederives the transaction and packet, requires two reviews, and confirms fixture application and exact-path commit separately. It directs the Maintainer to the existing signing process without signing or installing a baseline. (2) The best alternative is continued reuse of `build_transaction` and existing exact-path safeguards, keeping the single guided entry point; a manual fixture edit would lose the reviewed-input checks. The new guide repeats some apply/commit logic: consider extracting shared mechanics only if it preserves all accepted outcomes and costs less than maintaining both paths. This is nonblocking advice. (3) A no-anchor guided run that fails, writes outside reviewed fixtures, or accepts mutated or unreviewed evidence would falsify the change. The focused tests exercise those cases; I ran the no-anchor guided test from an isolated copy of `496a720d` under Python 3.13.13: 1 passed in 3.21 seconds.

**Blocking finding:** The iteration record says the full mapped iteration selection and plan-specific security and workflow checks are not yet complete. C1 and Verification require those checks, including the named AST test and mutation controls. Complete the mapped checks on committed bytes and record commands, results and any non-pass dispositions before clearing implementation. This does not authorize a full suite.

**Coverage:** Read the implementation, its forward command dispatch, focused tests, runbook scope and iteration record. Did not run the mapped suite, verify every consumer, test interruption after fixture application, or audit the full hostile-input and signing boundary; separate Security Review and final wide Boundary B remain owed. Elapsed: approximately 6 minutes. Tokens: unknown.

## Iteration evidence -- Codex GPT-6.1 Terra -- 2026-11-02 (approval recheck)

An independent Security review identified that inputs could change during the apply confirmation. `72ccc6cd` rechecks HEAD, index, tracked worktree, review evidence and fixture bytes after approval and before any fixture replacement. In an isolated copy under Python 3.13.13, `test_forward_guide_refuses_changes_during_approval` passed all six prompt-time mutations in 14.75 seconds: HEAD, index, worktree, packet, review and fixture. No real baseline or ref was changed.

The mapped run on isolated `fdec837b` reproduced the two previously diagnosed AST baseline failures. An initial invocation was interrupted because its broad keyword filter excluded unrelated forward-named nodes. A corrected run excluded the two known failures and stopped at `test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports`: its clone had no `refs/cairn/gate-anchor`, and the test expected the historical bootstrap wording. That partial run had 236 passed, one failed and two deselected in 52.69 seconds. No old anchor was fetched or compared. The remaining mapped checks, targeted follow-up reviews and final wide Boundary B remain owed; no full suite ran. Elapsed: approximately 5 minutes; tokens: unknown.

## Mapped iteration -- Codex GPT-6.1 Terra -- 2026-11-02

On clean isolated commit `72ccc6cd7dc558586ebed13c2657017caf639514` under Python 3.13.13, the six approval-time mutation cases passed separately. The ten-file mapped selection excluded those six already-passed cases, the two known AST baseline-debt nodes and the missing-anchor live-repository check described above. An initial segment passed 32 nodes; its exact unrun tail was selected from collection. That tail stopped at `test_gate_preflight.py::TestAuthorizationPackage::test_the_executable_only_list_is_closed`: 318 passed and one failed in 420.82 seconds because this clone has no `refs/cairn/gate-anchor`. This is a distinct unfulfilled check, not a pass. Remaining nodes were not run. The selection exceeded the 30-second iteration diagnostic target; per-file timing was not measured. No old anchor was fetched or compared. The three excluded checks, this failure, remaining mapped checks and final wide Boundary B remain open; no full suite ran. Elapsed: approximately 8 minutes; tokens: unknown.

## Security code review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commits: 4b066389, 496a720d and 72ccc6cd  
Target: forward-only workflow; evidence `a699ba47`; ordinary review `fdec837b`  
Prior issue: stale candidate could write during Apply confirmation  
**Tier**: Security Review  
**Verdict**: REVISE for unmet required verification; no remaining code blocker found.  
**Elapsed**: approximately 15 minutes across inspection and targeted probes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The explicit forward path derives committed current-state transactions, binds distinct review records, limits fixture outputs and separates Apply/commit confirmations from later baseline signing. It neither reads an anchor nor grants historical certification. -- Forward context, packet, review and guide implementations; C1.
2. **Best alternative.** Keep the guided path and shared transaction machinery. Shared validation avoids extra machinery; manual JSON or historical reconstruction loses the accepted outcome. -- Plan Reuse; current correction and guide.
3. **What would show it wrong?** A changed candidate reaching fixture replacement. My scratch-only real-command/PTY probe reproduced that defect at `496a720d`; repeated under Python 3.13.13 at `72ccc6cd`, it refused before writing and left fixtures unchanged. It also rechecks index, worktree, evidence and targets. -- Targeted no-anchor probes; six author-recorded mutation passes.

**V1 — blocking verification gap, C2 unmet.** Evidence explicitly leaves two AST baseline-debt checks and the missing-anchor live-CLI check excluded, a distinct executable-list check failed, and the remaining mapped tail unrun. The partial 32-pass segment and 318-pass/one-failure tail under Python 3.13.13 do not complete the selection. Close with required mapped outcomes and named authorized dispositions for unresolved checks, then clean final wide Boundary B. No anchor comparison requested or check waived.

**Bounding**: WIDER RUN REQUIRED — mapped remainder and required-check dispositions remain open.

Coverage: examined committed code, tests, runbooks, prior findings and evidence; independently challenged prompt-time candidate mutation. No suite, signing, real refs, installation or anchor comparison. Did not audit all consumers or authenticate reviewer independence.

## Targeted code review -- Codex (GPT-6), Reviewer -- 2026-11-02

**Reviewed**: correction `72ccc6cd` and evidence `a699ba47`.  
**Verdict**: correction is proportionate; prior required-check blocker remains open.  
**Bounding**: WIDER RUN REQUIRED.

**Foundations.** (1) The correction rechecks the candidate, evidence and fixture bytes after the existing apply prompt, without adding a prompt, trust store or historical-anchor step. It addresses a change during approval while preserving the guided workflow. (2) The best alternative is to retain the existing revalidation and prompts rather than introduce a separate approval mechanism; omitting the recheck leaves changed inputs able to reach application. (3) Changed evidence reaching a write would show it wrong. On an isolated copy of `72ccc6cd` under Python 3.13.13, the public-command packet mutation at approval passed: 1 test in 4.36 seconds. The author reports six mutation cases passed.

The prior blocking finding is **not closed**: `a699ba47` records two excluded baseline-debt checks, an excluded missing-anchor check, another missing-anchor failure and an unrun tail. These are not passes; the required mapped checks and final wide Boundary B remain owed. No old anchor comparison is authorized or inferred from this review.

**Coverage:** Read the correction, its public-command tests and the updated evidence; independently ran the single packet mutation case. Did not run a suite, exercise every mutation, fetch or compare an anchor, or verify signing and host security. Separate Security Review covers that boundary. Elapsed: approximately 4 minutes. Tokens: unknown.

## Remaining mapped iteration -- Codex GPT-6.1 Terra -- 2026-11-02

On the same clean isolated `72ccc6cd7dc558586ebed13c2657017caf639514` under Python 3.13.13, the exact 1,145 nodes not yet executed after the prior interrupted selection ran once, without fail-fast: 1,144 passed and one failed in 1,575.38 seconds. `bootstrap/tests/test_repin_ceremony.py::test_inherited_child_marker_does_not_bypass_record_check_isolation` failed the `manifest_module is GM` module-identity assertion in the combined selection. A single-node rerun on the same candidate passed in 2.12 seconds, suggesting an order-dependent module-state interaction; the combined-selection failure remains open. Together with the earlier 32 and 318 passes and six targeted passes, these results do not clear the two baseline-debt or two historical-anchor-dependent checks previously recorded. No old anchor was fetched or compared. The selection exceeded the iteration timing target; per-file times were not measured. Independent review, non-pass disposition and final wide Boundary B remain owed. No full suite ran. Elapsed: approximately 27 minutes; tokens: unknown.

## Test isolation correction -- Codex GPT-6.1 Terra -- 2026-11-02

`dfe081d6` isolates the two existing in-process baseline-install race probes with `patch.dict(sys.modules)`, retaining their refusal and ref-state assertions; production code is unchanged. On an isolated committed copy under Python 3.13.13, a no-anchor control verified both test call sites use the isolation and exercised the real loader and its reverse cleanup. It confirmed original module identities and package attributes for the manifest and reanchor modules are restored and the original reanchor authority reader succeeds. The original combined selection was not rerun; the prior combined failure and four baseline/anchor-dependent checks remain recorded and require disposition. No old or synthetic anchor, baseline installation, signing or full suite was used. Elapsed: approximately 4 minutes; tokens: unknown.

## Ordered isolation check -- Codex GPT-6.1 Terra -- 2026-11-02

On isolated `dfe081d6` under Python 3.13.13, the ordered pair `test_repin.py::test_baseline_preparation_builds_exact_package_after_reader_binding` then `test_repin_ceremony.py::test_inherited_child_marker_does_not_bypass_record_check_isolation` passed: two tests in 49.43 seconds. Both used disposable scratch repositories and generated test keys; the ceremony fixture used a synthetic scratch anchor. No real historical anchor or keys were accessed. This targeted ordered check addresses the reproduced module-identity interaction; the complete mapped selection was not repeated, and the four baseline/anchor-dependent checks and final wide Boundary B remain open. The selection exceeded the 10-second per-file diagnostic target; individual file times were not measured. Elapsed: approximately 2 minutes; tokens: unknown.

## Targeted test review -- Codex (GPT-6), Reviewer -- 2026-11-02

**Reviewed**: test-only correction `dfe081d6` and evidence `c309a8ae`.  
**Verdict**: the reproduced order interaction is addressed; required verification remains open.  
**Bounding**: WIDER RUN REQUIRED.

**Foundations.** (1) Yes: the diff confines module-registry restoration to the two in-process race calls and leaves their refusal and ref-state assertions intact; production behavior is unchanged. (2) Restoring the registry around those calls is a small alternative to changing the production loader or adding persistent machinery. (3) The identity test failing after the race test would show the fix insufficient. The author reports the original ordered pair passed on `dfe081d6` under Python 3.13.13, two tests in 49.43 seconds, using disposable repositories and a synthetic scratch anchor. This addresses the observed interaction, not every possible test order.

The full mapped selection was not repeated. Four baseline/anchor-dependent exclusions remain unpassed and final wide Boundary B remains owed; no actual historical anchor comparison is implied or requested. The earlier verification blocker is not cleared.

**Coverage:** Read the correction, original test assertions and committed isolation evidence. Did not rerun tests, compare an old anchor, or assess all possible order interactions. Separate Security follow-up remains owed. Elapsed: approximately 2 minutes. Tokens: unknown.

## Targeted Security code review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: dfe081d64473a942b13eea276d61cb1db1603b24  
Target: test-only order correction; evidence `c309a8ae`, ordinary follow-up `91097a2b`  
Prior findings: V1 required verification gap; module-identity failure diagnosed afterward  
**Tier**: Security Review — second and final pass  
**Verdict**: order defect addressed; no new code blocker. V1 remains open.  
**Elapsed**: approximately 4 minutes, excluding prior diagnosis. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Only the two existing in-process baseline-install race calls gain module-registry restoration. Refusal, ref-state and identity assertions remain unchanged; production is untouched. This repairs test isolation within the accepted test scope. -- Exact `dfe081d6` diff; plan Scope.
2. **Best alternative.** Restore imports locally with the standard-library context manager. Moving probes into another process is more work; weakening identity assertions or changing production trust behavior would conceal the cause. -- Existing loader/cleanup and test call sites; correction diff.
3. **What would show it wrong?** Original module/package identities remaining replaced after the probes. My no-anchor committed-source control under Python 3.13.13 exercised the real loader and reverse cleanup inside the context; all prior identities and package attributes returned and the original authority reader succeeded. Both calls retain refusal contexts. -- Independent targeted control; author ordered-pair evidence.

**Bounding**: WIDER RUN REQUIRED. The author records two ordered tests passing under Python 3.13.13 in disposable repositories with generated keys and a synthetic anchor. That closes the reproduced functional interaction, not every order. Four baseline/anchor-dependent omissions remain unpassed, the full mapped selection was not repeated, and final clean canonical-Python wide Boundary B remains owed. V1 is not waived or cleared; unresolved required checks need named disposition under the existing cap rule, not another clearing review.

Coverage: inspected committed correction, unchanged assertions, evidence and ordinary follow-up; independently probed registry restoration. No suite, real historical-anchor comparison, signing or baseline operation. Did not assess every test order or independently repeat the ordered pair.

## Implementation verification -- Codex GPT-6.1 Terra -- 2026-11-02

**Boundary B mode**: wide — mapped security, command, ceremony, AST and shipped-rule families; forward preparation, review and guide public paths and both runbooks. The plan's ten mapped test files cover these consumers; the four named exclusions below leave coverage incomplete. A narrower bound cannot cover the trust ceremony.
**Tested commit**: `44ab91e3f1f3a5b436bf24bfcb06b2162ada977e`
**Reviewed range**: `5c49324b..44ab91e3`, forward-plan implementation paths; unrelated interleaved changes are not claimed.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13.
**Pre-run state**: clean isolated clone at tested HEAD. **Post-run state**: clean, same HEAD.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---|---|
| `python -m pytest bootstrap/tests/test_ast_attest.py bootstrap/tests/test_ceremony_review_report.py bootstrap/tests/test_gate_manifest.py bootstrap/tests/test_gate_preflight.py bootstrap/tests/test_reanchor.py bootstrap/tests/test_reanchor_driver_disclosures.py bootstrap/tests/test_repin.py bootstrap/tests/test_repin_ceremony.py bootstrap/tests/test_review_stance_in_shipped_files.py bootstrap/tests/test_security_marker.py` with the four `--deselect` nodes below, `--durations=0 -q` | 1 | 1,492 passed, 9 failed, 4 deselected | 2,075.20 s | unknown |
| `python scripts/claim_check.py` on each changed runbook; `python scripts/link_check.py` and `python scripts/sync_doc_snippets.py --check` on both | 0 | claim, link and snippet checks passed | unknown | unknown |
| `python scripts/check_cairn.py` | 0 | 187 Markdown files; 104 external links not probed | unknown | unknown |
| `python scripts/quality_gate.py --sub neutrality` | 0 | 0 failures, 43 informational | unknown | unknown |

**Non-pass disposition**: Nine `test_gate_preflight.py` failures are unresolved: `TestAnchorPosition::test_orphaned_anchor_refuses`, `TestSterileGitLauncher::test_a_reference_transaction_hook_cannot_move_a_third_ref`, `TestApplyTransaction::test_symbolic_gate_anchor_refuses`, both `TestCeremonyReflogs` tests and four `TestAtomicPublication` tests (`test_the_atomic_push_publishes_both_refs`, `test_without_atomic_the_split_state_is_real`, `test_a_clone_does_not_carry_the_anchor_without_an_explicit_refspec`, `test_the_authorization_ref_is_never_published`). Several traces show `refs/heads/master` missing; the Maintainer's agent inspected a failed scratch repo and found its HEAD on `main`. This suggests a default-branch mismatch, not a demonstrated production defect; all nine remain failures pending diagnosis. Pytest failed even though the logging pipeline returned zero. Full output: `/private/tmp/cairn-forward-finalb-44ab91e3.log`.

**Plan-specific acceptance commands**: The mapped run included the forward public-command and disposable workflow tests; the four exclusions below were not executed. No real historical anchor, baseline or signing key was used. **Known omissions**: `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`, `test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set`, `test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports`, and `test_gate_preflight.py::TestAuthorizationPackage::test_the_executable_only_list_is_closed` were deselected under the Maintainer's direction to separate new-baseline installation and avoid historical-anchor comparison. They are unpassed, not waived by this record. No full suite ran.

**Timing**: iteration and wide diagnostic targets were exceeded. Approximate cumulative pytest-reported per-file durations over 10 seconds, slowest first: `test_repin_ceremony.py` 1,145.08 s; `test_gate_preflight.py` 409.50 s; `test_repin.py` 292.81 s; `test_reanchor.py` 118.10 s; `test_ceremony_review_report.py` 53.62 s; `test_gate_manifest.py` 23.41 s; `test_security_marker.py` 13.38 s; `test_reanchor_driver_disclosures.py` 13.36 s. Add these to the consolidation list at its serialization point. This failed run does not clear final verification.

## Focused failure diagnosis -- Codex GPT-6.1 Terra -- 2026-11-02

On the same clean isolated `44ab91e3f1f3a5b436bf24bfcb06b2162ada977e` under Python 3.13.13, reran only the nine failed `test_gate_preflight.py` nodes listed above with process-only `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=init.defaultBranch` and `GIT_CONFIG_VALUE_0=master`: nine passed in 3.64 seconds. HEAD and clean state were unchanged; no user Git configuration changed. This supports the scratch default-branch mismatch diagnosis; it does not erase the original wide run's nine failures. The four baseline/real-anchor exclusions remain unpassed, and required verification and disposition remain open. No full suite or historical-anchor comparison ran. Elapsed: approximately 1 minute; tokens: unknown.

## Verification reconciliation -- Codex GPT-6 -- 2026-11-02

The Maintainer's quoted direction in Scope delta removes the four named baseline/real-anchor-dependent nodes from this plan's completion checks and places the baseline work on the existing v0.6 board. They remain unpassed; this record does not claim their results or historical certification. No old-anchor check or repeat suite was run for this reconciliation.

The wide run at `44ab91e3` was not green: 1,492 passed, nine failed and four were deselected. Its same-commit nine-node rerun passed under a process-only `master` default. The independently reviewed release-test correction `abea6d02` makes the disposable repository's branch explicit; its nine affected nodes passed under both `main` and `master` defaults, and removing the fix reproduced all nine failures under `main`. The later release-test wide selection at `68df1f21` recorded 801 passes, two socket-permission setup failures subsequently passed separately on the same commit, and two real-anchor omissions. See `dev/plans/2026-11-02-release-test-corrections.md` for its precise scope and results. These results resolve the observed branch-default failures; they do not turn the original run green or establish results for the four omitted nodes.

The ordinary and Security reviews found no remaining code blocker after targeted fixes. The latter was its second and final pass. With the Maintainer's explicit scope direction, the recorded wide selection, focused diagnosis, subsequent reviewed correction and applicable prose gates provide the plan's machinery verification; the four named omissions remain visible and outside this plan. No additional clearing review is required. Actual baseline approval, installation and signing remain separate Maintainer-controlled work. Elapsed: approximately 4 minutes; tokens: unknown.
