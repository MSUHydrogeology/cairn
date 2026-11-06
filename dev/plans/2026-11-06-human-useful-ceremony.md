# Plan: Human-useful ceremony output and return on attention

**Source proposal**: dev/proposals/archive/2026-11-06-codex-human-useful-ceremony.md
**Author**: Codex GPT-6.1 Terra (Medium)
**Status**: implementing
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
