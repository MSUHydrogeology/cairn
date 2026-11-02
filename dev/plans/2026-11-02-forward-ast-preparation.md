# Plan: Prepare a forward AST correction

**Source proposal**: dev/proposals/archive/2026-11-02-codex-forward-ast-preparation.md
**Status**: ready-to-implement
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

**C2.** Ordinary and separate Security Reviews assess the committed implementation; all required checks pass, including wide Boundary B. Hashes identify bytes, not reviewer independence or safety.

Actual correction approval, exact-path commit and later baseline approval/signing are Maintainer-only steps outside this implementation; they require their own concrete approvals and existing ceremony controls. This plan authorizes none of them.

## Scope delta

**Scope delta**: preserved.

## Verification

`python tools/test_tiers.py for scripts/repin.py bootstrap/tests/test_repin.py bootstrap/tests/test_repin_ceremony.py bootstrap/tests/test_ast_attest.py bootstrap/AST_BASELINE_RUNBOOK.md bootstrap/REANCHOR_RUNBOOK.md` selects ten files, including the three named command and AST tests, re-anchor, gate and review consumers. Remap all final paths, including any governing change with its reviewed range; inspect readers and byte pins. Run mapped iteration checks and applicable claim, link, snippet, neutrality and `python scripts/check_cairn.py` gates.

C1 exercises the documented guided entry point end to end in disposable repositories, including a pause and resume after independent reviews, correction approval, exact-path commit confirmation and handoff to the existing baseline approval/signing without signing or moving real refs. It also exercises real commands for: no prior anchor, unchanged ordinary refusal, missing/duplicate and lockfile-debt refusal, no preparation writes, unreviewed packet refusal, and reviewed-path-only apply/commit. Separately mutate candidate, transaction/packet, review binding and target fixture; each must refuse. `bootstrap/tests/test_ast_attest.py` checks unchanged membership and accounted-for digests. These tests are S2/S3; report outcomes and omissions concisely. No real refs move and no signing occurs in tests.

Boundary C is independent ordinary and Security code review, examining affected engine behavior and protection machinery as well as the packet. After fixes, wide Boundary B on a clean unchanged final commit under canonical Python 3.13 covers mapped iteration and integration/workflow tests, owning families, public command paths, standing gates and the disposable workflow. Record SHA/range, interpreter, pre/post state, commands, counts, timing, tokens, non-pass dispositions and omissions. Combine overlapping checks only on the same reviewed commit without dropping coverage. Full certification and actual baseline ceremony remain separate authorized work; do not run another full suite for this plan.

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
