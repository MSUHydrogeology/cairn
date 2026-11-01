# Plan: Make proposals easier to decide

**Source proposal**: dev/proposals/archive/2026-11-01-codex-proposal-decision-summary.md
**Status**: ready-to-archive
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
A short proposal may do most of its work in the summary and rationale.
The existing review considers whether the Maintainer can explain the choice;
this is a reading judgment, not a mandatory checklist.
The one-line board field, required evidence, lifecycle records, slot behavior,
security and scientific preflights remain intact. Common text agrees across the
shipped and self-hosted templates. No new review stage, score or general rule is
added. Inspect the guidance against a short and a technically involved existing
proposal; record what the examples show and do not claim a reader was tested.

Security preflight S2 asks whether a check can fail; S3 asks what runs it
and over which inputs. C1 identifies readers and byte pins, runs the scoped
checks and traces
any changed machine check from trigger to runner; demonstrate a failing case
for each changed check. No machine-check change is proposed. The other security
preflight answers remain as accepted. Independent scientific check: N/A; no
scientific assumption or result touched.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A (scoped checks during implementation): Before implementation search
for readers and byte pins, including
known-positive controls for negative searches. Run `python tools/test_tiers.py
for <changed paths>` and its selected tests, plus applicable claim, link,
snippet and neutrality gates. Follow the high-risk surface checks; trace each
named check to its trigger and runner. Record commands, outcomes and omissions.

Boundary C (independent falsification): An independent code reviewer reads
committed changes and iteration
evidence and runs the tightest targeted falsification checks, without a suite.
The separate Security Review remains required.

Boundary B (final integration checks): After review, run the wide integration
selection on the clean,
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

## Plan review response -- Codex GPT-6 -- 2026-11-01

**Elapsed**: unknown; **Tokens**: unknown

- Ordinary review: Accepted both recommendations; C1 preserves short-proposal
  flexibility and excludes a mandatory checklist, and Verification defines its
  terms in place.
- Security Review: No findings.

## Implementation verification -- Codex GPT-6 -- 2026-11-01

**Elapsed**: approximately 15 minutes; **Tokens**: unknown

Boundary A covered the two proposal templates at commit `dc83fbc55ee3be850274fb8a50911ef620d67dbd`. The working copy was clean before and after testing in a detached clone. Python was 3.12.9; Python 3.13 was unavailable, so this is iteration evidence only. `python tools/test_tiers.py for dev/proposals/_template.md templates/core/dev/proposals/_template.md` selected 16 files. The exact list ran with `python -m pytest` and passed: 1,018 tests in 11.92 seconds. No per-file duration report was collected.

Prose gates on both changed paths passed: `python scripts/check_cairn.py` (claims and links, 2 files), `python scripts/link_check.py` (2 files), and `python scripts/sync_doc_snippets.py --check` (2 files, no drift). `python scripts/quality_gate.py --sub neutrality` reported 0 failures and 43 informational exceptions. No machine check changed; no check-trigger mutation was applicable. Reader search found the existing install and template coverage in the selected test set; no exact-byte pin or proposal-summary parser was found.

Qualitative comparison: the short archived template-burden proposal is already concise enough to use a summary and rationale without filler. The technical metered-cost proposal's opening lets the new summary name the noticed problem, proposed meter/report/limit change, and privacy/authoring costs, while detailed token-counting, boundaries, and evidence remain below. These examples show the prompt fits both forms; they do not measure reader comprehension. Board field, lifecycle records, security preflight, and scientific preflight remain in place.

Boundary B remains required after independent review: wide integration selection on the clean, unchanged final commit under Python 3.13.x, including the mapped iteration and integration/workflow tests. No full-tree certification or re-anchor was run.

## Code review -- Codex GPT-6 (ordinary reviewer) -- 2026-11-01

**Tier**: Internal
**Reviewed**: `dc83fbc5`; iteration record at `9a445185`
**Elapsed**: approximately 3 minutes; **Tokens**: unknown

**Foundations**

- **Should it happen as framed?** Yes. Both openings ask for the noticed problem, change and meaningful tradeoff together, and retain evidence below; the implementation matches C1 without a new review stage.
- **Best alternative:** Rely on the existing Plain Language guidance alone. That avoids template changes but leaves the decision spread across separate sections, as the plan review observed.
- **What would show it wrong?** Lost preflights or board fields, divergent common prompts, or required filler would defeat C1. The committed diff preserves the fields and preflights, adds matching prompts and expressly permits short proposals.

**Verdict:** Accept; no findings. The prompts request definitions and examples where useful, and the existing review's reading judgment is expressly not a checklist or score. The author's qualitative comparisons support fit for short and technical proposals, but do not establish reader comprehension.

**Bounding:** Sufficient for independent review; wide Boundary B remains required. `git diff dc83fbc5^ dc83fbc5 --check` passed; searches of both committed templates located the board field, summary, preflights and lifecycle records. Read the committed diff and iteration evidence; did not rerun its test selection, test reader comprehension, inspect every downstream reader, or perform the separate Security Review.


## Code review -- Codex gpt-6.1-sol (Security Review) -- 2026-11-01

**Foundations**

1. **Should this happen as framed?** Yes. The summary asks for the noticed
   problem, proposed change and meaningful cost, while retaining supporting
   evidence below -- committed diff `dc83fbc5`, both proposal templates.
2. **Best alternative.** Apply existing Plain Language guidance alone; that
   avoids a prompt but leaves the choice distributed. The implemented common
   opening adds no authority or review stage -- accepted proposal, Rationale;
   template Lifecycle and Decision summary.
3. **What would show it wrong?** A weakened preflight or transferred Decision
   authority would break C1. Direct comparisons of both templates at `dc83fbc5`
   against its parent found Security preflight, Independent scientific check
   and Decision sections byte-identical -- Git-object section comparison.

**Reviewed**: `dc83fbc55ee3be850274fb8a50911ef620d67dbd` against its parent;
iteration evidence at `9a445185`.
**Obligation**: Internal Security Review (code)
**Tier**: Internal Security Review
**Verdict**: ACCEPT; **Findings**: none
**Bounding**: ACCEPTED for this security read; final wide Boundary B remains owed.
**Elapsed**: approximately 4 minutes; **Tokens**: unknown

The summary remains author-controlled evidence, with the Maintainer retaining
Decision authority. Both new common passages match across the shipped and
self-hosted templates. The diff preserves slot blocks, assurance declarations,
review obligations and required evidence. It changes no machine check, parser,
trust boundary or scientific claim, so changed-check mutation is inapplicable.
The reading judgment explicitly excludes a checklist or score.

**Coverage**: committed template diff, accepted safeguards, unchanged preflight
and Decision sections, and recorded iteration evidence. Did not rerun the
implementation checks, test reader comprehension, perform installation, or
complete Python 3.13 final integration; no full suite or mutation run.

## Boundary B verification -- Codex GPT-6 -- 2026-11-01

**Elapsed**: approximately 3 minutes; **Tokens**: unknown

**Mode**: wide. Tested clean commit `970b82bd33fd3d682b3ecf38c65ace08e23bcb08`; reviewed implementation range `dc83fbc55ee3be850274fb8a50911ef620d67dbd..970b82bd33fd3d682b3ecf38c65ace08e23bcb08`. Detached clone was clean before and after. Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python` 3.13.13.

The iteration selection and its mapped workflow/integration consumers were run with `python -m pytest` on all 16 selected files; the consumer overlap is `test_documentation_plan_module.py`, `test_install_report_slots.py`, `test_quickstart_sequence.py`, `test_replacement_tools.py`, `test_scaffold.py`, and `test_session_routines.py`. Result: 1,018 passed in 11.13 seconds. Per-file timing reruns also passed; slowest was `test_session_routines.py` at 2.71 seconds, and zero files exceeded the 10-second diagnostic target.

Applicable prose gates passed on both templates: `scripts/check_cairn.py` and `scripts/link_check.py` found no issues; `scripts/sync_doc_snippets.py --check` found no drift; `scripts/quality_gate.py --sub neutrality --report` returned 0 failures and 43 informational exceptions. No changed machine check or trigger required a mutation; no additional high-risk engine check applied. Qualitative examples were checked at Boundary A and remain applicable: a short proposal can stay short, and the technical proposal leaves detail below the summary. This does not establish reader comprehension. No check was omitted from the mapped scope. Full-tree certification and re-anchor were not run.
