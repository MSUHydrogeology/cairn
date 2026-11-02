# Plan: Locate scientific model evidence

**Source proposal**: dev/proposals/archive/2026-11-01-codex-model-evidence.md
**Status**: ready-to-archive
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

## Code review -- Codex GPT-6.1 Sol -- 2026-11-01

**Verdict**: Accept; no findings. Reviewed `d7434ba6` and implementation evidence at `e8c11a43`.

**Foundations**: Should this happen as framed? Yes: the governing copies place scientific evidence with its requiring work while retaining configured suite members and other required checks. Best alternative: keep prior guidance; it avoids an edit but leaves the reported evidence-ownership ambiguity (proposal Context and Alternatives). What would show it wrong? Adding a non-required model run solely because it is scientific, or waiving a configured safety-related run because of its subject or duration, would violate C1; the recorded examples distinguish those cases.

**Evidence**: Compared both governing copies and plan guidance with the accepted proposal and C1. The iteration record reports 667 mapped tests passing, prose gates and independent comparisons; it identifies 46 omitted unpinned governing-file readers. Certification commands and triggers are unchanged in the diff.

**Coverage**: Read the committed change, proposal, plan and iteration evidence. Did not rerun tests, inspect installed output, independently audit all scientific controls, or perform the separate Security Review. Final wide verification remains outstanding. No suite run. Elapsed: approximately 5 minutes; tokens: unknown.

## Security code review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commit: d7434ba616289d8f1c1927d23784ab1a6b33b876  
Target: model-evidence changes in `d7434ba6^..d7434ba6`; evidence `e8c11a43`, ordinary review `ed934a93`  
Prior findings: none  
**Tier**: Security Review  
**Verdict**: ACCEPT; no findings.  
**Elapsed**: approximately 4 minutes across preparation and final review. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Both governing copies and plan guidance retain configured suite membership and other applicable obligations at every required point. Scientific subject or duration grants neither waiver nor rescheduling authority; certification commands and triggers are unchanged. -- Implementation diff; accepted proposal and C1.
2. **Best alternative.** Keep the short ownership clarification in existing evidence records. A new classification system adds burden; removing configured runs would violate the accepted scope. -- Proposal, Proposal and Alternatives; changed plan guidance.
3. **What would show it wrong?** Treating a long scientific safety test as optional after assigning its evidence to a plan. The retained every-required-point clause defeats that inference, and the authorized independent example preserves the configured safety-required run while excluding a genuinely unrequired run. -- Governing paragraphs; iteration evidence, examples.

**Bounding**: ACCEPTED — challenged the overlapping suite/safety case and retention of scientific controls. Targeted source assertions confirmed counterpart agreement, the required-suite clause, and failing/positive-control text in both unchanged proposal templates. The shared record reports 667 mapped passes under Python 3.12.9, prose gates and 46 selector omissions; no implementation test was rerun.

Coverage: read accepted scope, committed governing/template/method changes, scientific-control guidance, iteration evidence and ordinary review. Did not audit every work/release requirement, inspect installed output or certify the tree. No suite or mutation run. No reached fence or deviation request in this range; final canonical-Python wide Boundary B remains owed. Issue #33's broader terminology request remains open as recorded.

## Response to code reviews -- Codex GPT-6.1 Luna -- 2026-11-01

Both the ordinary and Security code reviews accept the implementation with no
findings. No code revision is needed. Preserve the open issue #33 disposition:
the accepted scope did not adopt scoped-only certification or a separate
ordinary full-suite check. Final wide Boundary B remains required before
archival. Elapsed: under one minute; tokens: unknown.

## Implementation verification -- Codex GPT-6 -- 2026-11-01

- **Boundary B mode**: wide, including governing and shipped counterparts,
  plan templates, scientific-check readers and installed public paths.
- **Tested commit**: `bfdaacd833685caf599d7c959e759fbda78c0510`
- **Reviewed range**: `b210f9b4d2e938e33905e8c99faabd7ab7e91148..bfdaacd833685caf599d7c959e759fbda78c0510` (shared v0.6 selection)
- **Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13; Bandit on `PATH`
- **Pre-run state**: clean isolated clone at tested SHA. **Post-run state**: clean, same `HEAD`.

The shared 36-file test union, gates, counts and local-socket disposition are
recorded in `dev/plans/2026-11-01-decision-options.md`; the scientific-check
guidance test and all mapped lifecycle/integration families are included.
Compared self-hosted and fresh-installed cases: (1) a model run outside the
configured suite and all other requirements belongs with the work/release that
needs it and is not added to routine certification; (2) a configured suite
member also serving a safety or work-specific need remains required at every
required point. Subject and duration waive neither requirement. The relevant
final guidance is unchanged since the authorized examples at `d7434ba6`.

**Plan-specific acceptance commands**: human comparison of both installed and
self-hosted cases above; both outcomes match C1.

**Non-pass disposition**: see the common run record; the 14 local-socket nodes
passed on the targeted rerun.

**Known omissions**: 46 unpinned governing-file readers were omitted by the
selector guard; external links were not probed; per-file durations were not
collected. No full-tree certification was run. **Elapsed**: shared automated
checks 190.28 seconds; plan-specific comparison included in session; tokens:
unknown. Issue #33 remains open as already recorded.
