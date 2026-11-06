# Plan: Human-useful ceremony output and return on attention

**Source proposal**: dev/proposals/archive/2026-11-06-codex-human-useful-ceremony.md
**Author**: Codex GPT-6.1 Terra (Medium)
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Explain existing trust approvals where people make them and record whether each finished outcome repaid the effort it required.

## Source proposal

The Maintainer accepted both outcomes as heavy on 2026-11-06: explain the
existing approvals and complete attention accounting in existing records,
without adding a ceremony, ledger, confirmation or archive gate.

## Scope

Revise the maintained `scripts/repin.py` presentation and
`bootstrap/REANCHOR_RUNBOOK.md` for ordinary and transition ceremonies,
verifier HOLD dispositions, and forward and baseline approvals. At each real
approval explain the change, purpose, residual risk, evidence and exact action
authorized. Distinguish preparation, independent review, applying or
committing pins, signing or moving refs, and publication. A bounded proceed
disposition does not resolve a HOLD. Derive labels from checked state, never a
semantic safety verdict from a digest. Preserve exact bytes, fingerprints,
packet and reader binding, refusal, prompt order, authority, schemas and
required comparisons at their decision points.

Clarify existing Decision cost prose to name material human operations and
follow-up homes/counts, including zero when useful. Require one concise
closing sentence in existing verification or disposition records judging
benefit against observed effort and remaining burden, or saying unknown;
light work uses its proposal. Reconcile existing archive completeness judgment
without another gate, score, response or timesheet.

**Reuse.** Searches of `scripts/repin.py`, the runbook and ceremony tests found
existing prompt, evidence and refusal paths; extend those rather than create a
reporter. Existing AGENTS Decision guidance and proposal/plan templates provide
record homes. Coordinate shared plan-template edits with lifecycle
reconciliation if concurrent; neither plan depends on the other's completion.

### Documentation / doctrine surface

Presentation belongs in the driver and runbook; cross-cutting prescription
in local and shipped AGENTS and existing proposal/plan templates, with
rationale in lifecycle documentation. No new artifact or evidence schema.

## Sequence

The existing driver, evidence and record homes are available now. Estimate
2–4 workdays including reviews and verification; prompt-consumer mapping,
protected tests and security findings introduce uncertainty. Coordinate shared
files during concurrent work; no unfinished plan or human release operation is
a prerequisite.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Map all prompt consumers and protected test nodes, then clarify existing approvals and runbook | Usual and Security plan reviews | Evidence-qualified explanations at each existing entry point |
| C2 | Clarify Decision and closeout guidance in existing records | C1; serialize shared template edits | Human-operation costs and one evidence-qualified retrospective sentence |
| C3 | Review and verify the complete change | C1–C2; usual and Security code reviews | Wide Boundary B and concise dispositions |

## Acceptance criteria

**C1.** A fresh reader of saved synthetic transcripts and evidence can identify
each approval's action, evidence, risk and limits, including refusal and HOLD.
Required pasted digests and independently sourced fingerprints remain visible
at comparison; candidate claims are not authenticated evidence. Before/after
comparison shows no added manual operation, confirmation or comparison. Existing
exact-byte, binding, refusal and authorization checks continue to pass; tests
also detect misleading explanations and missing comparison values.

**C2.** Existing Decision guidance names material human operations and
follow-up homes/counts without exhaustive routine-agent inventory. Existing
closeout guidance calls for one benefit-versus-observed-effort sentence,
including unknown where unsupported, for plans and light proposals; it adds no
separate archive gate or Maintainer response.

**C3.** Both code reviews and mapped checks pass; the result makes no measured
usability or saved-time claim without evidence.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: inventory ordinary, transition, verifier, forward and baseline
prompt consumers and protected parameterized test nodes before edits. Run
`python tools/test_tiers.py for <changed paths>` and selected tests, preserving
comparison and authority assertions; extend existing synthetic ceremony,
forward and baseline tests for misleading text and omitted comparison values.
Account for protected-test review and baseline handling. Compare synthetic
transcripts and prescribed operations before/after and have a fresh reader
explain each action and HOLD. Run claim, link, snippet and neutrality gates.

Boundary C: independent code review runs tight falsification checks; separate
Security Review is required. Boundary B: after review, run wide on a clean
final commit under canonical Python 3.13.x, including mapped iteration,
integration/workflow, trust-ceremony security and public-path checks and prose
gates. Record SHA/range, interpreter, clean pre/post state, commands, counts,
timing, non-pass dispositions and omissions. Required release ceremonies and
certification remain separate; this plan authorizes no signing or ref movement.

## Plan review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed commit**: `9b2f7a55937ed13b644e9720cd9bf0a1fc40e51d`
**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: PROCEED
**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes. C1 retains comparison values, authority and refusal while requiring evidence-qualified explanations; C2 places the retrospective in existing records, and C3 preserves both reviews and wide verification. The 2–4 day estimate is uncertain until protected consumers are mapped. -- Plan Scope, Sequence, Acceptance criteria and Verification; accepted proposal Decision.
2. **Best alternative.** Extending the current driver and record homes is the simplest identified route delivering both outcomes; a runbook-only explanation misses the approval entry point and a new ledger adds maintenance. -- `scripts/repin.py`, `bootstrap/REANCHOR_RUNBOOK.md`, `AGENTS.md` Decision guidance and `dev/plans/_template.md` Dispositions.
3. **What would show it wrong?** A synthetic transcript missing a required fingerprint or digest, misstating an action or a HOLD, changing refusal, adding a manual step, or a reader unable to explain an approval would falsify C1; an unsupported payoff claim would falsify C2. -- Plan C1–C2 and Boundary A; `bootstrap/tests/test_repin_ceremony.py` Summary 2 consumers and runbook HOLD contract.

**Coverage**: Read the committed plan and accepted proposal, template, review sweep, runbook HOLD and fingerprint requirements, prompt-test consumers and existing Decision and disposition homes. Did not exhaustively map consumers, execute synthetic transcripts, tests or ceremonies, or assess private host state; a separate Internal Security Review remains required.

## Plan review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Reviewed commit**: `bfdffc0212afe1e138ae04d368b3c7a6eb73b4d5`
**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: PROCEED
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes. C1 preserves exact-byte, fingerprint, packet/reader binding, comparison visibility, refusal, prompt order and authority while improving the explanation. Scope keeps a dispositioned HOLD unresolved and separates preparation, review, pin application/commit, signing/ref movement and publication. C2 confines the attention judgment to existing records without a new gate or response. -- Plan Scope and C1–C2; `scripts/repin.py:2343` and `bootstrap/REANCHOR_RUNBOOK.md:88`.
2. **Best alternative.** Extend the existing driver prompts and record guidance with concise, evidence-qualified prose, as planned. Runbook-only wording leaves the real approval point implicit; a new reporter or ledger adds another maintained channel. The existing Decision cost sentence and plan/proposal closeout homes already support both accepted outcomes. -- Accepted source Proposal and Alternatives; `AGENTS.md` choice/Decision guidance; `dev/plans/_template.md` Dispositions.
3. **What would show it wrong?** Saved synthetic transcripts must fail checks when a comparison digest or independent fingerprint disappears, a candidate claim becomes authenticated evidence, a HOLD becomes cleared, or an explanation grants the next action more authority. Compare before/after operations and prompt order; any added human step fails C1. A fresh reader must explain every named approval and its limits; unsupported payoff claims fail C2–C3. -- Plan Verification; `bootstrap/tests/test_repin_ceremony.py` Summary 2 disclosure and prompt-driving consumers; runbook verifier/forward/baseline boundaries.

**Coverage**: Examined committed scope and Decision, driver digest/package rechecks and Summary 2, runbook HOLD and approval limits, existing record homes and prompt-test consumers. The plan requires consumer/protected-node mapping before edits and wide final verification. Did not exhaustively map consumers, run transcripts, tests or ceremonies, measure usability, inspect private host state, sign, move refs or authorize baseline installation; implementation evidence remains due.

## Plan review response -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

Both Internal and Internal Security Reviews proceed with no findings. Consumer
and protected-node mapping, synthetic transcript and comparison evidence,
required code reviews and wide final verification remain implementation work.
No scope or operative plan change is needed.

**Elapsed**: approximately 1 minute. **Tokens**: unknown.

## Implementation verification -- Codex GPT-6 Luna (Low) -- 2026-11-06

**Record state**: interim implementation and iteration handoff. C1 remains
unresolved after the Low retry budget; code reviews and final Boundary B are
still due. Do not treat these iteration results as C1 completion.

**Boundary B mode**: wide, planned; not run. Trust-ceremony changes and
published/local template guidance are in scope. The final wide selection must
follow both code reviews and include the mapped consumers and standing gates.

**Tested commits**: C1 `0fc4326a9dff773429baff360267c5c41890cd15`; C2
`c769b585c53af5570daedd40e19b9075c6136e24`; restored-board node
`d143ddb336fe2a41230e2d8ce30ef0b9388c8484`. Each test run used a clean copy
of the cited commit. The C1 retry copy was
`/tmp/cairn-ceremony-test-0fc4326a`; the C2 correction copy was
`/tmp/cairn-ceremony-c2-fix-check`; the restored-board copy was
`/tmp/cairn-ceremony-c2-board-check`.

**Reviewed range**: not established; usual and Security code reviews remain
due. **Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
Python 3.13.13. **Pre-run and post-run state**: each cited check copy was clean
at its tested commit before and after the run. **Tokens**: unknown.

| Command / selection | Exit and outcomes | Elapsed |
|---|---|---:|
| `test_tiers.py for scripts/repin.py bootstrap/REANCHOR_RUNBOOK.md bootstrap/tests/test_repin.py bootstrap/tests/test_repin_ceremony.py` (7 files); full mapped selection on `9ea798c0` | 1,398 passed, 41 failed; missing anchor in 2 preflight nodes, incomplete isolated test environment, and one incorrect assertion | 1,354.3 s |
| Corrected rerun of 41 failed node IDs on the same mapped selection | 2 passed, 39 failed; anchor setup and assertion were corrected, but SSH-agent/passphrase harness failures remained | 339.97 s |
| Final Low retry: 39 previously failed nodes on `0fc4326a` | 2 passed, 37 failed: 2 scratch SSH-agent startup failures and 35 scratch signing-passphrase failures. Exact 37 node IDs and stderr were not retained; the executor must reconstruct affected cases from the selection/cache before a single higher-tier attempt. No more Low retries. | 298.3 s |
| C2 initial mapped selection on `831d0e3b` (20 files; 32 AGENTS readers omitted by the selector guard) | 1,425 passed, 8 failed: 7 proposal-template placeholder findings corrected in `c769b585`; one finished-plans node reflected the temporary reopened Suite state | 21.43 s |
| Corrected C2 mapped selection on `c769b585` (17 files) | 1,419 passed, 1 failed: the same temporary finished-plans metadata mismatch. All seven placeholder nodes passed. After Suite was restored, the single node passed on `d143ddb3`. | 22.64 s; 0.34 s |

**Non-pass disposition**: C1 remains open pending higher-tier diagnosis and
resolution of the 37 affected nodes. The SSH-agent failures reported inability
to start `/usr/bin/ssh-agent`; ceremony failures reported the scratch
`throwaway-passphrase-for-tests` as incorrect. The exact list and tracebacks
are unavailable in the retained output; only the failing count and categories
above are known. The temporary finished-plans failure passed after Suite was
restored; no source or helper change was made for it.

**Plan-specific acceptance commands**: `claim_check.py` passed on each changed
proposal, plan, AGENTS and lifecycle file. C2 mapped checks are passing after
the placeholder correction and restored-board node. C1 synthetic ceremony
checks remain unresolved. No signing, ref movement, baseline operation,
release, full suite, or certification was run.

**Known omissions**: exact C1 failed node IDs/stderr, protected synthetic
transcript walkthrough, ordinary and Security code reviews, final wide Boundary
B, and its mapped integration/security/prose gates. Review remains fresh;
iteration testing is not code review.

Observed C2 checks support the record and template changes, but C1's remaining
assurance and burden are unknown until its mapped failures and required reviews
are resolved.

### Corrected C1 validation and review handoff -- 2026-11-06

**Final source commit**: `c172c6710ccb80ca1008d474decec0d1239ca6af`.
**Source SHA-256**: `scripts/repin.py`
`8e3ed54060cdfb2b78da52f7f2cfd363e62cd0166fa4a129acc885cbb85a620e`;
`bootstrap/tests/test_repin_ceremony.py`
`1fd5f17dce368ba493f76f99f87781bb8a4f45c58796b0b3a7b7702a2d61c81f`.
These are the only source changes after the earlier interim record. The driver
now prints purpose/next action/publication on one line and the claims/safety
limitation separately. Its Summary 2 test requires one exact standalone scan
digest line and removes that line in the existing missing-disclosure mutation.
The independent prior-scanner/report disagreement guard is unchanged.

**C1 targeted validation**: Medium ran on a clean copy of the final source
commit under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13),
with scratch HOME, valid Darwin
`TMPDIR`, inherited signing credentials unset, and local scratch signing
permission. Both logs show no failures, errors or skips.

| Command / selection | Exit and outcomes | Elapsed | Tokens |
|---|---|---:|---|
| `bootstrap/tests/test_repin_ceremony.py::test_summary_two_shows_each_disclosure` | 1 passed; 0 failed, 0 skipped | 10.45 s | unknown |
| The 38 IDs in `/private/tmp/cairn-terra-signing.3fdu5A/unexecuted.txt` (SHA-256 `5ec301a0b4ea83ca73f2d84f6d5e45bc2f343632761e4ff4d607bff1d9c182a4`) | 38 passed; 0 failed, 0 skipped | 239.30 s (240.66 s wall) | unknown |

Logs: `/private/tmp/cairn-ceremony-c172.I88NcE/disclosure.log`,
`disclosure.xml`, `remaining.log`, and `remaining.xml`. The earlier history
remains as recorded above: initial full mapped run at `9ea798c0` was 1,398
passed/41 failed; retries on earlier commits ended at 37 failures. The original
37 failed node IDs remain unknown. Forty earlier passing nodes and two
representative reruns were on `0fc4326a`, not this final source commit. The
new 39 targeted passes do not establish a fresh pass of all 1,439 original
mapped items at `c172c671`.

**C2 final disposition**: source commits are `831d0e3b` and
`c769b585`. On the corrected 17-file mapping, 1,419 of 1,420 nodes passed and
the single finished-plans node failed while Suite was temporarily reopened;
that node passed after restoration at `d143ddb3`. Thus all 1,420 distinct
mapped nodes passed across those runs, with zero skips. The initial 20-file
run had 1,425 passes and eight failures: seven were the proposal-template
placeholder correction and one was the temporary Suite state. All seven
corrected placeholder nodes passed on `c769b585`. The initial selector
omitted 32 AGENTS readers; the current combined map below reports 31 omitted
readers under its guard.

**Final implementation path map**:
`scripts/repin.py`, `bootstrap/REANCHOR_RUNBOOK.md`,
`bootstrap/tests/test_repin.py`, `bootstrap/tests/test_repin_ceremony.py`,
`AGENTS.md`, `templates/core/AGENTS.md`, `dev/plans/_template.md`,
`templates/core/dev/plans/_template.md`, `dev/proposals/_template.md`,
`templates/core/dev/proposals/_template.md`, and
`docs/methodology/lifecycle.md`.

The combined mapping command was:

```text
/Users/kendal30/conda_envs/lhm/bin/python3.13 tools/test_tiers.py for --range 831d0e3b..c172c671 scripts/repin.py bootstrap/REANCHOR_RUNBOOK.md bootstrap/tests/test_repin.py bootstrap/tests/test_repin_ceremony.py AGENTS.md templates/core/AGENTS.md dev/plans/_template.md templates/core/dev/plans/_template.md dev/proposals/_template.md templates/core/dev/proposals/_template.md docs/methodology/lifecycle.md
```

It selects 26 test files and reports 31 AGENTS readers omitted by the guard.
The selection is a map, not a new run. It names `test_certifying_run_rule`,
`test_review_and_verification_rules_ship`,
`test_scientific_check_guidance_ships`, `test_stewardship_rules_ship`,
`test_verification_boundaries`, `test_board_json_contract`,
`test_ceremony_review_report`, `test_claim_check_module`,
`test_core_dev_folders`, `test_documentation_plan_module`,
`test_gate_preflight`, `test_install_report_slots`, `test_loop_fidelity_gate`,
`test_quickstart_sequence`, `test_reanchor`,
`test_reanchor_driver_disclosures`, `test_repin`, `test_repin_ceremony`,
`test_replacement_tools`, `test_review_stance_in_shipped_files`,
`test_review_sweep_ships`, `test_scaffold`, `test_scope_reduction_trap`,
`test_session_routines`, `test_session_start_drain_rules`, and
`test_status_vocabulary_advisory`.

**Review handoff**: implementation source is complete. Fresh usual and first
Security code reviews remain due; wide Boundary B must follow both reviews and
cover the combined map, integration/workflow paths and applicable security
and prose gates. Boundary B is not run. No signing, anchor movement, baseline
operation, release, full suite or certification was run.

Whether the accepted benefit justifies total effort and the remaining review
burden is unknown until the required reviews and wide verification finish.

## Code review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed commit**: `2f41b499864900d0e9b26ee6de853fc496bf8ae5` (source through `c172c671`).

**Foundations**:

1. **Should this happen as framed?** The source adds explanations at existing actions and leaves prompt and signing control flow intact; the accepted comprehension evidence is still missing (finding below). The verifier retains unresolved HOLD and Summary 2 retains the independent scan comparison and package recheck. -- `scripts/repin.py`, `_verifier_run` and `run_ceremony`; commits `dac1c301`, `c172c671`.
2. **Best alternative.** Extend the existing driver and record homes as implemented; a runbook alone misses the approval point, while a separate ledger adds burden without delivering more of the accepted outcome. -- `bootstrap/REANCHOR_RUNBOOK.md`, `dev/plans/_template.md` and `dev/proposals/_template.md`.
3. **What would show it wrong?** A synthetic transcript that hides a required comparison, grants extra authority or clears a HOLD, or an added human step, would falsify C1. The disclosure test removes each disclosure independently and requires one 64-hex scan line; the existing scanner-disagreement test refuses before signing. A fresh-reader walkthrough and operation comparison remain unmeasured. -- `bootstrap/tests/test_repin_ceremony.py::test_summary_two_shows_each_disclosure` and `::test_prior_scanner_disagreement_stops_before_signing`; corrected handoff above.

**Finding (blocking; accepted check unmet).** C1 and Boundary A require a fresh reader to explain each approval from saved synthetic transcripts and evidence, including refusal/HOLD, and a before/after comparison of manual prompts and prescribed operations. The interim record lists the transcript walkthrough as omitted; the corrected handoff records targeted tests but neither result. Close by recording the fresh reader's evidence and explanations for ordinary, transition, verifier/HOLD, forward and baseline paths, and the before/after operation comparison; address any discrepancy found. Do not infer this evidence from substring assertions or source inspection.

**Bounding**: ACCEPTED for the named mapped selection, subject to the missing plan-specific checks and final wide Boundary B. The 31 AGENTS readers omitted by the selector guard are disclosed; wide verification remains due.

**Verdict**: REVISE. **Elapsed**: approximately 8 minutes. **Tokens**: unknown.

**Coverage**: Read the committed source and test diffs, accepted scope, handoff and existing refusal, digest and signing paths. Inspected the line-removal and scanner-disagreement tests; did not execute them, inspect saved transcripts, independently mutate cases, access keys or perform a ceremony. Security Review and wide Boundary B remain separate and outstanding.

## Code review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Reviewed commit**: `305ffd53374734cd013ae8893d7d4ff2bea165a3` (ceremony source through `c172c671`; C2 through `c769b585`).
**Obligation**: Internal Security Review
**Tier**: Internal Security Review

**Foundations**:

1. **Should this happen as framed?** The existing approval and record homes deliver the accepted design, but one new promise misstates the commit's signing effect (finding below). Digest/report agreement, reader binding, package recheck and transition fingerprint refusal remain unchanged. -- `scripts/repin.py`, `run_ceremony` and `commit_reviewed_pin`; source diffs `dac1c301` and `c172c671`.
2. **Best alternative.** Keep the presentation changes and existing commit policy; distinguish ordinary Git signing/hooks from trust-anchor signing. Disabling signing would change behavior unnecessarily. Existing Decision and verification records already deliver C2 without another ledger or approval. -- `commit_reviewed_pin`; `831d0e3b` template and AGENTS changes.
3. **What would show it wrong?** A configured signer invoked after a no-sign promise falsifies C1; the isolated real-entry-point probe reproduced this. After correction, a signer-spy regression must detect inaccurate explanations while retaining normal commit policy. Fresh-reader comprehension and before/after operations remain unmeasured. -- scratch probe below; ordinary review `305ffd53`.

**Finding (blocking; C1).** `commit_reviewed_pin` newly says “This does not sign,” and the runbook's reviewed-pin row says neither approval signs. The subprocess deliberately restores normal Git configuration/hooks and does not disable `commit.gpgsign`. With that setting enabled, the probe observed the promise followed by invocation of a fake configured signer. Correct both explanations to distinguish normal Git commit policy from the later trust-anchor signing operation; preserve prompts and control flow, and add a targeted regression.

**Falsification evidence**: Python 3.13.13; clean clone of the reviewed commit before scratch-only test extension. The existing transition/AST-pin workflow, extended with a no-key signer spy, passed once in 29.24 s (30.02 s wall), confirming invocation and subsequent normal workflow completion. Repeatable probe: `/private/tmp/cairn-ceremony-signing-probe.py`; log: `/private/tmp/cairn-security-ceremony-s4wj579q/probe.log`.

**Retained blocker**: the ordinary review's saved-transcript fresh-reader walkthrough and manual-operation comparison remain owed. Final wide Boundary B remains due; separate release-baseline operations remain unpassed.

**Bounding**: WIDER RUN REQUIRED for normal Git signing policy at the exact-path commit; extend its existing mapped ceremony test before final integration.
**Verdict**: REVISE. **Elapsed**: approximately 10 minutes. **Tokens**: unknown.

**Coverage**: Examined committed source/test and C2 diffs, trust boundaries, HOLD limits and staged validation; independently falsified the signing disclosure. Did not replay author checks, read saved transcripts, run a suite, access real keys, sign a real trust artifact or move real refs. Exceeds 300 words to preserve the new finding's probe evidence and existing acceptance blocker.

## Delegated verification-schedule Decision -- gpt-6.1-sol (High) -- 2026-11-06

**Decision-maker**: gpt-6.1-sol (High), under temporary Maintainer delegation. This is Sol's own reversible local scheduling choice, not a claim that the Maintainer personally selected it. **Elapsed**: unknown. **Tokens**: unknown.

**Authority**: Maintainer -- chat, 2026-11-06, relayed by the coordinating agent:

> "I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome."

**ACCEPTED -- this fix only.** For the correction of `commit-reviewed-pin`'s inaccurate no-sign explanation and matching runbook wording, Boundary A may use the tight real-entry-point fake-signer regression, directly affected disclosure/authority controls and affected prose gates instead of replaying the complete mapped seven-file C1 selection before review. Retain normal configured Git signing/hooks and all actual behavior. The targeted controls must run on the corrected committed source, detect the old false no-sign promise while a configured no-key signer is invoked, and verify the corrected disclosure. Record exact nodes, commit, results and omissions. Earlier failures and source-specific evidence remain intact; this does not establish a current complete mapped pass.

The complete C1 mapping, full C2 consumers and applicable integration/workflow/security/prose selections remain required in final **wide Boundary B**, on a clean unchanged final commit under canonical Python 3.13.x, after the ordinary targeted return and second Security pass. Derive the union from every implementation path in the whole reviewed range. Combining archive/lifecycle verification is permitted only at the same final commit/interpreter/environment, naming each plan's full selection and outcomes. Shared nodes may run once for unchanged covered inputs; required nodes and reported omissions cannot disappear through deduplication. A failure or later source change still requires its affected reruns: this is no run-count cap. No full-tree certification or `CAIRN_FULL_SUITE=1` is authorized.

Saved-transcript fresh-reader evidence for ordinary, transition, verifier/HOLD, forward and baseline paths, and the before/after manual-operation comparison, remain mandatory. Neither tests nor this schedule replace them. Both review findings remain open until their named closure evidence exists. Preserve the same-reviewer targeted return and second Security pass within the existing cap; no third or clearing pass is authorized. Broad Boundary B stays explicitly pending during review; no completion/archive before it passes. If correction changes signing/hook behavior, trust/binding/schema logic, substantive scope or another affected test family, this exception ends for that new material; remap under existing rules or obtain a specific disposition.

**Options, cost and reason.** Literal A now plus B after review retains immediate broad replay but repeats unchanged ceremony families. The initial 1,354.3-second run is historical and harness-affected, not a forecast or promised saving. Postponing the defect leaves C1 unmet and cannot complete the work. Tight A plus complete B keeps immediate causal falsification and independent review, placing the broad run on the final source where it remains required. It can expose an unrelated regression later; keeping work open through B bounds that risk. No check or outcome is removed. This adds zero human ceremonies, recurring processes or ledgers, changes no model floor and claims no measured time saving. It is a one-fix local schedule exception, not a permanent rule change, Security clearance or release authorization.

**Evidence read**: source at `452aa3cd`, this plan's C1–C3/Verification and corrected `c172c671` evidence, ordinary review `305ffd53`, Security Review `88a6373a`, and governing iteration/final-verification rules. No tests or edits were performed by the decision-maker.

## Implementation evidence update -- Codex GPT-6 Luna (Low) -- 2026-11-06

**Source**: correction at `a96dc6eb8e1340308df46e7598ed019dabd22ecc`; no
source changes followed it. The ordinary Git commit explanation now preserves
configured hooks and commit-signing policy while distinguishing the separate
trusted-anchor operation. `test_a_transition_packet_drives_both_stages_against_a_disposable_signed_anchor`
uses a scratch no-key signer spy: it confirms the configured signer is invoked,
the output discloses normal Git policy, failure leaves `HEAD` unchanged, and
the existing no-sign fixture path completes. This is ordinary history commit
behavior; no real key, host profile, trust reference or anchor was used.

**Targeted iteration**: on a clean copy of `a96dc6eb`, canonical Python
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13), the six-case
signer/disclosure selection passed 6/6 with zero skips in 100.39 seconds; the
separate `test_summary_two_shows_each_disclosure` passed 1/1 with zero skips
in 9.10 seconds. The seven-case scrubbed transcript capture passed 7/7 in
101.87 seconds. These are targeted checks only, not a fresh pass of the earlier
full mapping. Existing earlier failures and unknown original 37 IDs above
remain part of the record.

**Saved transcript and operation comparison**: paired before/after synthetic
outputs are in `/private/tmp/cairn-ceremony-reader-view/01-before.txt` through
`05-before.txt` and matching `01-after.txt` through `05-after.txt`. They cite
baseline source `09b3eb1af0665044589e352762d60bb817da2e35` and corrected source
`a96dc6eb8e1340308df46e7598ed019dabd22ecc`. The paired ordinary path has four
prompt interactions on success and three before refusal; transition has four;
verifier/HOLD has one key-away confirmation (the proceeding fixture's
disposition remains file input and the HOLD stays unresolved); forward commit
has two confirmations on success and none when required evidence is absent;
baseline installation has no interactive prompt and still requires the
separate authorization plus explicit digest/fingerprint inputs. Counts and
order match before and after: zero new human prompts or operations. No saved
time or usability benefit is claimed. A fresh reader completed the transcript
read before opening source and reported correct distinctions for all five
flows; the reader's own interpretation belongs in its separate review record.

**Advice disposition**: the forward-commit output could additionally mention
configured signing/hooks. It makes no affirmative unsigned promise; I accept
this as nonblocking wording advice and do not widen the correction. The
explicit false promise at `commit-reviewed-pin` and runbook is corrected.

**Remaining work**: required ordinary targeted return, second Security Review,
and the combined 89-file wide Boundary B remain due. Boundary B must include
the full C1/C2 mapping and applicable integration, workflow, security and prose
checks on one clean final source; no accepted criteria, earlier failure, or
known omission is waived. No real ceremony, signing, anchor movement, baseline
operation, release or full suite was run. **Elapsed**: unknown. **Tokens**:
unknown.

## Targeted code-review return -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed**: source correction `a96dc6eb8e1340308df46e7598ed019dabd22ecc` and author evidence `4f4c43f25f10452459e381d8838c9c914fa37d04`. This is the original reviewer's targeted return, not a new clearing pass.

**Fresh-reader understanding**: I read the saved synthetic final transcripts at `/private/tmp/cairn-ceremony-public-traces/captures/` before opening the correction or expected answers. My interpretation follows; the outputs are synthetic evidence, not a human usability measurement.

- **Ordinary / transition**: matching the launcher digest continues checks; Summary 2 approval permits rechecks and signing/anchor movement, not publication. Refusal stops further action. Transition also compares the prior signer with the independent fingerprint and uses the candidate roster for the new signer. Review the evidence and stop if it does not match; publication is separate.
- **Reviewed pin**: approval writes the displayed bytes, then a separate approval makes an ordinary branch commit subject to configured hooks and signing; neither operation moves the trusted anchor. Refusal makes no commit; a configured-signer failure requires inspecting the repository before retrying. A completed commit needs fresh ceremony evidence.
- **Verifier / HOLD**: key-away YES permits candidate execution and collection, not containment or signing. Even matching proceed dispositions leave the HOLD unresolved. Review the bound HOLDs and do not infer authority to continue.
- **Forward correction**: separate approvals write and commit reviewed fixture paths; neither certifies historical AST review nor installs the baseline. Missing review evidence refuses. Obtain fresh baseline reader evidence and a separate Decision next.
- **Baseline**: reader inputs are an unreviewed draft and preparation changes no authority. An authorized installation signs a manifest-only commit and advances branch and anchor atomically, without publication or historical certification; missing reader input refuses. Independently review inputs and obtain the named Decision before installation.

**Disposition**: The comprehension part of my finding is satisfied by this read. The author's `4f4c43f2` comparison records matching prompt counts and order and zero added human operations across the named flows, closing the recorded evidence gap. The corrected pin disclosure distinguishes ordinary configured Git signing from trust-anchor signing; the scratch signer-spy result is reported in that evidence. Forward commit text does not disclose hooks or configured signing, but makes no contrary unsigned promise; matching the detail is optional advice, accepted by the author. I found no new defect in `a96dc6eb`.

**Coverage**: Read synthetic success and refusal cases for the five flows, the correction diff and author evidence. I did not replay tests, operate real keys or refs, or establish human usability. Separate targeted Security Review and full wide Boundary B remain due. **Elapsed**: approximately 10 minutes, including waiting for serialized evidence. **Tokens**: unknown.
