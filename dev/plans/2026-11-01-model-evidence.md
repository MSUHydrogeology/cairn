# Plan: Locate scientific model evidence

**Source proposal**: dev/proposals/archive/2026-11-01-codex-model-evidence.md
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Clarify where scientific model evidence is required without changing the configured certification suite.

## Source proposal

The Maintainer accepted the heavy proposal as revised under Option 1: associate scientific evidence with the work or release requiring it while retaining every configured suite member and other required check.

## Scope

Clarify `AGENTS.md` and `templates/core/AGENTS.md`; align `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, and `docs/methodology/plans.md` where needed. Inspect proposal templates for conflicts and reconcile any found. Preserve certification commands and triggers, independent scientific checks and their required controls, and all accepted, safety, security and release requirements. Add no form, gate, label or review round.

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

Cross-cutting prescription belongs in both governing files; plan templates carry the operative workflow and methodology describes it.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inspect guidance, readers and pins; align wording and exercise both examples. | Both required plan reviews and author response | Prose and scoped iteration evidence. |
| C2 | Independent code and Security Reviews, response and final integration. | C1 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** Scientific evidence is specified and recorded with the work or release requiring it; it does not enter routine certification merely because it is scientific. A configured suite member remains required at every required point, as do other applicable criteria, safety, security and release checks; subject and duration waive nothing. Removing or rescheduling a requirement requires separate authority. Independent scientific checks and their failing and required positive controls remain. Certification definition, commands and triggers remain intact. Compare installed and self-hosted wording using (1) a model run outside the configured suite and all other requirements, and (2) a configured suite member also serving a safety or work-specific requirement. Record the person and outcomes; a waiver must fail the second example.

**C2.** Ordinary and separate Security Reviews assess the committed implementation; all accepted criteria and required checks pass, including final wide Boundary B.

## Scope delta

**Scope delta**: preserved.

## Verification

Before edits, search direct readers and byte pins, inspect their assertions and map changed paths using `python tools/test_tiers.py for <paths>`; use the complete reviewed range for governing text. Run mapped iteration checks, applicable claim, link, snippet and neutrality gates, and `python scripts/check_cairn.py`. Compare installed and self-hosted guidance with the two examples and record the person and outcomes. Security preflight S2/S3 uses the required-run human example; no automated proof is claimed.

Boundary C: independent reviewers read the committed implementation and iteration evidence and run targeted falsification checks. After review and fixes, run wide Boundary B on a clean unchanged final commit under canonical Python 3.13, covering mapped iteration and integration/workflow tests, owning families, known consumers and public paths, prose gates and both examples. When the other accepted v0.6 plans reach the same point, combine overlapping checks on one common reviewed final commit; retain every plan's required coverage and record its own evidence, range, SHA, interpreter, clean pre/post state, commands, counts, elapsed time, tokens, non-pass dispositions and omissions. Do not run the full certifying suite for this work.

## Ordinary plan review -- Codex GPT-6.1 Sol -- 2026-11-01

**Obligation:** Internal
**Verdict:** Support; no blocking findings.

**Foundations**

- **Should it happen as framed?** Yes. The plan assigns evidence to its requiring work while preserving configured suite members, other requirements and scientific controls. Evidence: plan C1 and Scope; accepted proposal Proposal and Decision.
- **Best alternative:** Retain existing guidance; it avoids edits but leaves the reported ambiguity about model evidence unresolved. Conditional alignment of existing guidance achieves the accepted clarification without new machinery. Evidence: accepted proposal Alternatives and plan Scope.
- **What would show it wrong?** Either example failing, especially a required suite member being waived for being scientific or slow, would falsify the clarification. Evidence: plan C1 and accepted proposal Evidence / verification plan.

**Advice:** The plan already combines overlapping final checks on a common reviewed commit while retaining each plan's coverage and evidence. Coordinate that run with the other plans and avoid repeats unless changed inputs, failed checks or unresolved concerns require them.

**Coverage:** Read the committed plan at `d44605ff`, accepted proposal and Decision, and current plan template. Did not inspect every reader or final wording, run the examples, or assess the separate Security Review; implementation and Security Review remain outstanding. No suite run. Elapsed: approximately 2 minutes; tokens: unknown.

## Plan review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commit: 18787e52bbbbeda67ec129380072a04605b9f6be  
Target: entire plan against accepted proposal and scientific-check obligations  
Prior findings: none  
Assurance path: high-assurance, inherited from accepted proposal

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none  
**Verdict**: ACCEPT  
**Elapsed**: approximately 2 minutes  
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. C1 preserves every configured suite member at every required point, other applicable checks, independent scientific checks and their failing and required positive controls. Scope preserves certification commands and triggers. Evidence ownership therefore grants no waiver. -- Plan, Scope and C1; accepted proposal, Proposal; proposal template, Independent scientific check.
2. **Best alternative.** Align only conflicting existing guidance and reuse its evidence records; no new classification mechanism is needed. The common final reviewed commit can share overlapping checks while retaining each plan's required coverage and recorded range. -- Plan, Scope and Verification; accepted proposal, no-new-form constraint.
3. **What would show it wrong?** A scientific suite member disappearing at certification, or a safety/work-specific run being rescheduled merely because its evidence has another home. C1 requires a configured-suite example overlapping another obligation and rejects a waiver; the optional example excludes both suite membership and other requirements. -- Plan, C1; accepted proposal, Evidence / verification plan and S2/S3.

No blocking security finding. Shared verification is conditional on the plans reaching the same reviewed final commit; it does not replace plan-specific examples, required checks or omission records. Full-tree certification remains a separate ceremony.

Coverage: examined the committed plan, accepted proposal, governing verification contract, current plan template and scientific-check/control requirements in the proposal template. Did not run examples, discover final readers, inspect implementation wording or execute tests. No suite run; implementation and separate Security code review remain owed.

## Response to plan reviews -- Codex GPT-6.1 Sol -- 2026-11-01

Both reviews found no blockers. Accepted the ordinary advice: coordinate overlapping final checks on the common reviewed commit when feasible while retaining each plan’s coverage and evidence. The separate Security code review and plan-specific examples remain required. Elapsed: under one minute; tokens: unknown.

## Implementation verification -- Codex GPT-6.1 Luna -- 2026-11-01

Changed surfaces: `AGENTS.md`, `templates/core/AGENTS.md`,
`dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, and
`docs/methodology/plans.md`. Proposal-template inspection found no conflicting
scientific-check rule. The self-hosted and adopter-facing guidance leave the
configured suite, commands and triggers unchanged.

The shared mapped selection recorded in the decision-options plan selected 18
files; it included `test_scientific_check_guidance_ships.py`,
`test_review_and_verification_rules_ship.py`, and the other shared readers.
All 18 passed on committed `d7434ba6`: 667 passed in 61.04 seconds under
Python 3.12.9. The selector also reported 46 unpinned `AGENTS.md` readers
omitted by its passage-pin guard. The run exceeded the 30-second iteration
target; per-file durations were not collected. The lifecycle plan's remaining
mapped tests and their outcomes are recorded there.

`python scripts/check_cairn.py` passed (189 Markdown files; 95 external links
not probed). `python scripts/link_check.py` passed (189 files; 96 external
links not probed). `python scripts/quality_gate.py --sub neutrality` reported
zero failures and 43 informational findings. Snippet sync was not applicable:
no synced snippet changed.

**Maintainer authorization** (chat, 2026-11-01): "Yes, use agent reviews" to
substitute independent agent reviewers for the two plan examples that called
for a person to compare them by hand. No automated or security check was
waived. Independent reviewer Codex GPT-6.1 applied the prepared examples at
`d7434ba6`: a model run that was neither a suite member nor otherwise required
was not added to routine certification; a configured, safety-required model
run remained required at every required point. This checks the distinction in
the examples, not whether future authors will find every applicable
requirement. Elapsed: approximately 32 minutes; tokens: unknown.

## Completion follow-ups

**Issue #33 remains open.** The accepted proposal deliberately did not adopt
the issue's alternative definition that would make certification scoped-only
and move the full suite to a separate ordinary check. After code review and
final wide Boundary B, retain the issue for a separate Maintainer decision;
do not close it as completed by this narrower clarification.
