# Plan: Clarify security triggers for guarded reuse

**Source proposal**: dev/proposals/archive/2026-11-01-codex-security-trigger-clarity.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Explain when reuse of a reviewed guard changes a security boundary and when it does not.

## Source proposal

The Maintainer accepted the heavy proposal as revised under Option 1: clarify guarded reuse without weakening named high-risk triggers, review authority or required verification.

## Scope

Update `dev/modules/security-review.md` and `templates/modules/team-gated/security-review.md`. Inspect `AGENTS.md`, its shipped copy and `docs/methodology/dual-review.md` and reconcile genuine conflicts without weakening their independent high-risk rule. Preserve periodic review, existing obligations and wide verification. Add no necessity field, automatic cancellation or reviewer authority to waive a required review.

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

The two security-review modules carry local security prescription; reconcile governing and descriptive guidance if it conflicts.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inspect triggers, installed consumers, direct readers and pins; align wording and exercise five cases and mutations. | Both required plan reviews and author response | Prose and scoped iteration evidence. |
| C2 | Independent code and Security Reviews, response and final integration. | C1 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** Both module copies explain that reuse or movement alone does not add or widen a boundary only when sources, accepted inputs, validation before every protected operation, operation authority and output recipients retain their reviewed limits. A new source, broader input, guard bypass, changed command construction or exposed output can trigger review through a familiar interface. Existing Foundations may challenge an unsupported declaration before Decision; changing an accepted obligation follows Maintainer authority and plan fences. Named high-risk triggers, periodic and required reviews and wide mapped verification remain; wide does not mean the full suite. Apply both copies to unchanged guarded reuse, same-format newly untrusted input, a move bypassing validation, a non-widening high-risk control edit, and confidential output sent to a newly public destination. Only the first lacks a trigger on those facts. An applicable rule check must fail when the unchanged-contract condition is removed or a bypass is exempted.

**C2.** Ordinary and separate Security Reviews assess committed implementation; all accepted criteria and required checks pass, including final wide Boundary B.

## Scope delta

**Scope delta**: preserved.

## Verification

Before editing, search readers and byte pins, identify installed consumers and map each changed path using `python tools/test_tiers.py for <paths>`. Open the assertions and selectors in `bootstrap/tests/test_review_and_verification_rules_ship.py` and `bootstrap/tests/test_review_stance_in_shipped_files.py`; name actual coverage and preserve movement and independent high-risk checks. Run mapped iteration tests and applicable claim, link, snippet and neutrality gates, plus `python scripts/check_cairn.py`. Check all five cases against both copies and record who applied them. For security preflight S2/S3, demonstrate the two specified mutations fail an applicable rule check; report the actual check and any gap rather than claiming prose proves runtime security.

Boundary C: independent reviewers read committed implementation and iteration evidence and run targeted falsification checks. After review and fixes, run wide Boundary B on a clean unchanged final commit under canonical Python 3.13, covering mapped iteration and integration/workflow tests, owning families, installed consumers and public paths, standing gates and case and mutation checks. When the other accepted v0.6 plans reach the same point, combine overlapping checks on one common reviewed final commit; retain every plan's required coverage and record its own evidence, range, SHA, interpreter, clean pre/post state, commands, counts, elapsed time, tokens, non-pass dispositions and omissions. Do not run the full certifying suite for this work.

## Ordinary plan review -- Codex GPT-6.1 Sol -- 2026-11-01

**Obligation:** Internal
**Verdict:** Revise before implementation; one blocking finding.

**Foundations**

- **Should it happen as framed?** Yes. C1 retains named high-risk triggers and authority, and exercises the five accepted cases and two mutations. Evidence: plan C1; accepted proposal Proposal and Tests required.
- **Best alternative:** Keep the existing trigger unchanged; this avoids editing but leaves guarded reuse unexplained. Conditional clarification in both copies preserves the accepted outcome without another field. Evidence: accepted proposal Alternatives and plan Scope.
- **What would show it wrong?** A familiar interface excusing a new source or bypass, or a required review being cancelled without authority, would defeat the clarification. Evidence: plan C1; accepted proposal Signals.

**Blocking finding:** The accepted proposal requires the plan to identify installed consumers and exact mapped checks, and open candidate triggers and name actual coverage. Verification instead postpones those steps until before editing. For example, `test_review_and_verification_rules_ship.py::test_security_module_movement_alone_does_not_trigger_review` asserts movement and added/widened wording, but its shown assertions do not establish either proposed mutation. Map consumers and checks in the operative plan and state actual coverage and gaps; retain the accepted mutation requirement without assuming these assertions prove it.

**Advice:** Coordinate overlapping final checks on the common reviewed commit as planned, retaining each plan's required coverage and record; avoid repeats without changed inputs or unresolved concerns.

**Coverage:** Read the plan at `f489be4a`, accepted proposal and Decision, plan template, and candidate test assertions. Did not trace all installed consumers, run mutations or inspect final wording; implementation and separate Security Review remain outstanding. No suite run. Elapsed: approximately 3 minutes; tokens: unknown.
