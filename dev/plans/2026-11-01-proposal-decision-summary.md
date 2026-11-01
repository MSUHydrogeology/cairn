# Plan: Make proposals easier to decide

**Source proposal**: dev/proposals/archive/2026-11-01-codex-proposal-decision-summary.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Bring the problem, change and tradeoffs together at the start of proposals so the Maintainer can understand the choice.

## Source proposal

The Maintainer accepted a short decision summary after the board's one-line
`In brief` field, with supporting detail below and existing safeguards retained.
The existing proposal review considers whether the Maintainer can explain the
choice; this adds no review stage or score.

## Scope

Revise the common opening and review guidance in `dev/proposals/_template.md`
and `templates/core/dev/proposals/_template.md`. Preserve their intentional
slot differences. Update `doctrine/proposals.md` only if needed to describe the
revised shape. Reuse Cairn Plain Language instead of adding a general rule.

**Reuse**: N/A: no code added.

### Documentation / doctrine surface

The templates are deliberation guidance; `doctrine/proposals.md` is published
methodology. No governing instruction or software description is planned.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Revise both templates and, if needed, proposal doctrine; verify and record iteration evidence. | Plan review and Security Review resolved. | Opening prompts and existing review guidance. |

## Acceptance criteria

C1: Both templates ask for the observed problem, proposed change and meaningful
costs together before supporting detail, in ordinary language; define terms when
needed, use concrete examples to clarify abstractions, and avoid repetition.
The existing review considers whether the Maintainer can explain the choice.
The one-line board field, required evidence, lifecycle records, slot behavior,
security and scientific preflights remain intact. Common text agrees across the
shipped and self-hosted templates. No new review stage, score or general rule is
added. Inspect the guidance against a short and a technically involved existing
proposal; record what the examples show and do not claim a reader was tested.

S2–S3: C1 identifies readers and byte pins, runs the scoped checks and traces
any changed machine check from trigger to runner; demonstrate a failing case
for each changed check. No machine-check change is proposed. The other security
preflight answers remain as accepted. Independent scientific check: N/A; no
scientific assumption or result touched.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: Before implementation search for readers and byte pins, including
known-positive controls for negative searches. Run `python tools/test_tiers.py
for <changed paths>` and its selected tests, plus applicable claim, link,
snippet and neutrality gates. Follow the high-risk surface checks; trace each
named check to its trigger and runner. Record commands, outcomes and omissions.

Boundary C: An independent code reviewer reads committed changes and iteration
evidence and runs the tightest targeted falsification checks, without a suite.
The separate Security Review remains required.

Boundary B: After review, run the wide integration selection on the clean,
unchanged final commit under canonical Python 3.13.x. Include the iteration
list for the reviewed range, mapped integration/workflow tests, owning families,
known public paths, applicable prose and high-risk checks, and the qualitative
examples. Record the tested SHA and range, interpreter, clean pre/post state,
commands, counts, elapsed time, tokens or unknown, non-pass dispositions,
acceptance checks and omissions. A known unmet check keeps work open. Full-tree
certification and any re-anchor remain separate authorized ceremonies.

## Plan review -- Codex GPT-6 (ordinary reviewer) -- 2026-11-01

**Tier**: Internal
**Reviewed**: `62e668da`
**Elapsed**: unknown; **Tokens**: unknown

**Foundations**

- **Should it happen as framed?** Yes. C1 puts the problem, change and costs together and retains the board field and preflights, matching the accepted proposal's Proposal and Decision.
- **Best alternative:** Apply the existing Plain Language rules without changing the templates. That avoids template work, but leaves the choice spread across their Context, Proposal and Rationale prompts (`dev/proposals/_template.md`; `dev/agent_collaboration.md`, rules 2–3, 5–6 and 9).
- **What would show it wrong?** A revised template that hides material costs, repeats the proposal or loses required evidence would fail its purpose; C1 calls for examples and preservation checks (accepted proposal, Signals the change is wrong; plan, Acceptance criteria).

**Verdict:** Proceed with non-blocking improvements.

**Findings:** The accepted proposal explicitly allows short proposals to do most of their work in the summary and rationale and forbids a mandatory checklist. C1 says to avoid repetition and adds no stage, score or general rule, but does not state those two points. Name both in C1 so the implementation does not inadvertently require filler or a checklist. For the Maintainer, explain “S2–S3” and “Boundary A/B/C” where they matter or point to their definitions; the plan otherwise asks its reader to decode its verification terms (Plain Language rule 5: “Define a specialist term where it first matters”).

**Coverage:** Compared the committed plan with the accepted proposal, both template openings, plan review guidance and Plain Language rules. Did not inspect every reader or byte pin, test implementation, or perform the separate Security Review.

## Plan review -- Codex gpt-6.1-sol (Security Review) -- 2026-11-01

```
Reviewed commit: 62e668da
Target: accepted scope, safeguards and verification
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 5 minutes; **Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. C1 retains required evidence,
   lifecycle records, security and scientific preflights while improving the
   opening; it implements the accepted Proposal without granting authors
   Decision authority -- source proposal, Proposal, S1 and Decision; plan, C1.
2. **Best alternative.** Change only the common opening and review prompts,
   using existing Plain Language guidance. The plan already takes that path,
   making doctrine edits conditional and adding no general rule -- plan, Scope;
   source proposal, Rationale.
3. **What would show it wrong?** A summary that hides costs or replaces evidence,
   or guidance that weakens a preflight, would violate C1. Compare both revised
   templates and the two qualitative examples with the preserved sections --
   plan, Acceptance criteria and Verification; source proposal, S5.

The author-controlled summary cannot establish its own truth. The accepted
S1, S4 and S5 answers retain the Maintainer's authority, the pause for unclear
information and the risk of misleading authors. The plan preserves those
answers, separately requires Security Review, and retains high-risk surface
checks and wide final verification. Scientific N/A matches the unchanged
scope. The planned reading judgment adds no authorization mechanism or stage.

**Covered**: committed plan against accepted safeguards, current template
preflight and Decision sections, and `AGENTS.md` role boundaries.
**Not covered / low confidence**: implementation bytes, scanner outcomes,
reader comprehension and every downstream reader; no tests or suite run.
