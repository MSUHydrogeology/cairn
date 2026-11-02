# Plan: Clarify security triggers for guarded reuse

**Source proposal**: dev/proposals/archive/2026-11-01-codex-security-trigger-clarity.md
**Status**: awaiting-code-review
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

The installer maps `templates/modules/team-gated/security-review.md` to the selected adopter module `dev/modules/security-review.md` (`bootstrap/_scaffold/config.py`); its onboarding prompt and `templates/onboarding/high-rigor-legacy.md` direct readers there. The profile templates and content-scan runner also point to the guidance. `python tools/test_tiers.py for dev/modules/security-review.md templates/modules/team-gated/security-review.md` selects `bootstrap/tests/test_review_and_verification_rules_ship.py`, `bootstrap/tests/test_review_stance_in_shipped_files.py`, `bootstrap/tests/test_scaffold.py` and `bootstrap/tests/test_security_stack.py`. The movement node checks added/widened wording and movement, the stance nodes check reviewer/author authority, scaffold checks registration and installation, and security-stack checks separate injection and self-audit guidance. None tests either new mutation. The movement wording search finds the two copies and its assertion; recheck readers and pins for any additionally changed paths. Preserve movement and independent high-risk checks. Add a repeatable applicable rule check for both copies that fails if the unchanged-contract condition is removed or a bypass is exempted; demonstrate each mutation in a separate copy and record its outcome. Do not claim that these prose checks prove runtime security. Run mapped iteration tests and applicable claim, link, snippet and neutrality gates, plus `python scripts/check_cairn.py`. Check all five cases against both copies and record who applied them. For security preflight S2/S3, demonstrate the two specified mutations fail an applicable rule check; report the actual check and any gap rather than claiming prose proves runtime security.

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

## Response to ordinary plan review -- Codex GPT-6.1 Sol -- 2026-11-01

Blocking finding accepted: Verification now identifies the installed destination, consumers, four mapped test files and their actual coverage, and the gap in both mutations. C1 retains both mutations; a repeatable check and separate-copy demonstrations are required before completion. Shared final verification remains conditional on common reviewed bytes and does not drop coverage. The separate Security plan review remains outstanding. Elapsed: approximately 5 minutes; tokens: unknown.

## Plan review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commit: cfb91c857c3a9d63a4172667194aabebe4ecbd5d  
Target: entire revised plan against accepted trigger and authority requirements  
Prior findings: none in this separate Security pass  
Assurance path: high-assurance, inherited from accepted proposal

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none  
**Verdict**: ACCEPT  
**Elapsed**: approximately 2 minutes  
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. C1 makes reuse conditional on unchanged source, input, validation, authority and recipient limits. It preserves independent high-risk triggers and accepted review authority, so a familiar API cannot excuse bypass or exposure. -- Plan, Scope and C1; accepted proposal, Proposal; module, Trusted-input vs user-controlled.
2. **Best alternative.** Extend an existing applicable rule check for the two prose copies and reuse existing evidence records. This satisfies the accepted mutations without a new review field or runtime mechanism; leaving the movement assertion alone misses both defects. -- Plan, Verification; `bootstrap/tests/test_review_and_verification_rules_ship.py`, test_security_module_movement_alone_does_not_trigger_review; accepted proposal, S2/S3.
3. **What would show it wrong?** Removing the unchanged-limits condition or exempting a bypass while checks still pass. The plan now requires repeatable rule checks and separate-copy mutation demonstrations, plus five cases covering new sources, bypass, independent high-risk edits and output exposure. -- Plan, C1 and Verification; accepted proposal, Tests required and S2.

No blocking security finding. The required check is a prose-rule safeguard, not proof that runtime guards execute. Wide final verification and separate Security code review remain; common final checks preserve each plan's coverage.

Coverage: examined the committed plan, accepted proposal, plan template, current module trigger and input-class distinction, movement-test assertions, installer mapping and onboarding reference. Did not run mutations or cases, inspect final rule-check design, audit runtime guards or enumerate every installed consumer. No suite run.

## Response to Security plan review -- Codex GPT-6.1 Sol -- 2026-11-01

The Security review found no blockers. Its suggested reuse of an applicable rule check fits the revised Verification; the two mutations, five cases, separate Security code review and wide final verification remain required. Elapsed: under one minute; tokens: unknown.

## Implementation verification -- Codex GPT-6.1 Luna -- 2026-11-01

Changed surfaces: `dev/modules/security-review.md`,
`templates/modules/team-gated/security-review.md`, and
`bootstrap/tests/test_review_and_verification_rules_ship.py`. Both module
copies now explain guarded reuse, the five widening cases, Foundations'
pre-Decision challenge, Maintainer authority after acceptance, and that wide
means mapped change verification rather than a whole-suite instruction.

The applicable test-tier mapping selected four files:
`test_review_and_verification_rules_ship.py`,
`test_review_stance_in_shipped_files.py`, `test_scaffold.py`, and
`test_security_stack.py`. After the guarded-reuse, authority and mutation
fixes, all four passed: 793 passed and one Bandit-dependent node skipped in
20.95 seconds under Python 3.12.9. The skipped node,
`test_security_stack.py::TestOrchestrator::test_subprocess_runs_isolated_not_repo_shadow`,
then passed alone under canonical Python 3.13.13 with Bandit available (1
passed in 0.38 seconds). The added wide-mode assertion passed for both copies
on `da48cfd9` (2 passed in 0.04 seconds under Python 3.12.9). The four-file
selection did not exceed the 30-second overall target; per-file durations were
not collected. The separate shared 18-file selection exceeded that target,
as recorded in the decision-options plan. No runtime security behavior is
claimed.

The prose gates passed: `check_cairn.py` (189 Markdown files; 95 external
links not probed), `link_check.py` (189 files; 96 external links not probed),
and neutrality (zero failures, 43 informational findings). The rule test
mutates each module copy separately: removing the reviewed-limits condition
and appending an explicit bypass exemption both fail the predicate. No
snippet-synced block changed. Elapsed: approximately 32 minutes; tokens:
unknown.

Codex GPT-6.1 Luna applied the five accepted cases to both module copies:
(1) unchanged guarded reuse has no boundary-change trigger; (2) same-format
input from a new untrusted source triggers review; (3) moving code to bypass
validation triggers review; (4) a non-widening edit to a named high-risk
control still triggers under the independent high-risk rule; (5) sending
confidential output to a newly public destination changes recipients and
triggers review. The prose checks do not prove runtime guard behavior.

## Completion follow-ups

**Issue #37 remains open.** The accepted proposal does not add the requested
necessity line and author-strike mechanism for proposal and plan review, does
not allow bounded verification for non-widening edits to named high-risk
surfaces, and retains the `adds or widens` trigger. After code review and final
wide Boundary B, keep these three residual requests visible for separate
Maintainer disposition; do not close the issue as fully delivered.

## Code review -- Codex GPT-6.1 Sol -- 2026-11-01

**Verdict**: Accept; no findings remain. Reviewed `d7434ba6`, corrections through `da48cfd9`, and iteration evidence at `e8c11a43`.

**Foundations**: Should this happen as framed? Yes: both module copies condition reuse on unchanged sources, inputs, validation, authority and recipients, and preserve independent high-risk triggers and Maintainer authority. Best alternative: retain the former movement rule; it avoids edits but leaves guarded reuse ambiguous (proposal Context and Alternatives). What would show it wrong? A familiar interface excusing a new source or bypass, or an accepted review being waived without authority, would violate C1. The recorded five cases and two prose mutations address those examples, without establishing runtime security.

**Evidence**: Compared the copies, accepted proposal and C1. My earlier finding that the modules omitted the required wide-mode explanation is closed by `da48cfd9`, which states it in both copies and adds a focused assertion. The implementation record reports the mapped four-file checks, the separately resolved Bandit skip, both mutations and five cases.

**Coverage**: Read committed implementation and corrections, proposal, plan, test assertions and iteration evidence; independently compared the five cases against the text. Did not rerun tests, inspect installed output, audit runtime guards or perform separate Security Review. Final wide verification remains outstanding. No suite run. Elapsed: approximately 6 minutes; tokens: unknown.

## Security code review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commits: d7434ba6, 8a7bdebf and da48cfd9  
Target: security-trigger module/test changes; evidence `e8c11a43`, ordinary review `fb5e37ed`  
Prior findings: omitted Foundations/authority clarification; bypass-exemption mutation gap  
**Tier**: Security Review  
**Verdict**: ACCEPT; prior findings closed, no new findings.  
**Elapsed**: approximately 8 minutes across preparation and correction review. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Both copies retain added/widened triggers and condition reuse on unchanged sources, inputs, validation, authority and recipients. Corrections restore Foundations' pre-Decision challenge, Maintainer authority after acceptance and mapped-wide meaning without a reviewer waiver. -- Module diffs; C1; accepted proposal.
2. **Best alternative.** Extend the existing prose check and use the five accepted cases. New runtime or classification apparatus would exceed this wording clarification; relying only on unchanged trigger phrases missed an explicit exemption. -- Test diff and preliminary adversarial probe; accepted S2/S3.
3. **What would show it wrong?** An exemption for bypassed validation passing the rule check. Initially my appended exemption survived both copies. At `8a7bdebf`, targeted source-only execution rejected that original mutant, a guard-bypass variant and condition removal; genuine text and a safeguard control passed. The predicate is unchanged by the subsequent wide-mode assertion. -- Recorded targeted probe and correction diffs.

**Bounding**: ACCEPTED — meaningful targeted mutants now fail, without claiming general prose or runtime validation. Author evidence records 793 passed/one Bandit skip under Python 3.12.9, the skipped node passing under Python 3.13.13, two later wide assertions passing, both required mutations and five cases. No mapped list was rerun.

Coverage: read accepted scope, committed modules/tests, corrections, iteration evidence and ordinary review; probed the named adversarial exemption. Did not inspect installed output or audit runtime guards. No suite run. No reached fence/deviation in this implementation range; final canonical-Python wide verification and recorded issue residuals remain owed.

## Response to code reviews -- Codex GPT-6.1 Luna -- 2026-11-01

Both the ordinary and Security code reviews accept the implementation with no
findings. No code revision is needed. Preserve the three open issue #37
requests in Completion follow-ups for separate Maintainer disposition. Final
wide Boundary B remains required before archival. Elapsed: under one minute;
tokens: unknown.
