# Plan: Human-useful ceremony output and return on attention

**Source proposal**: dev/proposals/archive/2026-11-06-codex-human-useful-ceremony.md
**Author**: Codex GPT-6.1 Terra (Medium)
**Status**: ready-to-implement
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
