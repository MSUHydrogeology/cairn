# Plan: Supply practical scoped-certification defaults

**Source proposal**: dev/proposals/archive/2026-11-01-sol-project-certification.md
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Give agents practical testing defaults so they can certify affected behavior without scientists designing routine test selection.

## Source proposal

The Maintainer accepted the heavy proposal: Cairn supplies testing architecture and agents map affected behavior, while existing requirements and Cairn's own full-tree ceremonies remain owed.

## Scope

Align `AGENTS.md`, `templates/core/AGENTS.md`, self-hosted and shipped plan and proposal templates, `docs/methodology/plans.md`, `docs/methodology/dual-review.md`, lifecycle wording, and both testing-discipline module copies. Search their consumers and examples; refer to existing optional architecture-review guidance without changing its selection. Core must work without optional modules. Update affected rule tests to distinguish adopter defaults from Cairn's retained local certification contract. Preserve historical records, unrevised plans, engine, installer and ceremony commands; add no selector, manifest, service, ledger or mandatory architecture-review program.

**Reuse.** N/A: no new code infrastructure. Existing testing-discipline guidance covers tiers, contracts and simulation timescales; existing architecture-review is optional.

### Documentation / doctrine surface

Core and self-hosted governing files carry prescription; templates carry workflow, modules supply practical examples, and methodology describes the resulting rules.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Trace consumers, readers and pins; align core, methodology, templates, module examples and affected rule tests. Exercise installed examples and core-only use. | Both required plan reviews and author response | Guidance, focused rule checks and iteration evidence. |
| C2 | Align scoped claims and project operations; exercise installed cases. | Both required plan reviews and author response | Claims and operation guidance with examples. |
| C3 | Independent code and Security Reviews, response and final integration. | C1 and C2 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** Core supplies component ownership, unit, contract, integration and real-entry workflow checks, plus small-domain real equations and analytical or convergence benchmarks where relevant and work-specific long runs. Agents search effects, callers, imports, configuration/data readers and public paths, map existing checks and gates, and add tests for plausible gaps; independent review challenges coverage and trivial work retains author evidence. Local changes default to affected checks. Shared contracts, infrastructure, language seams, solver/physics or uncertain dependencies widen to owning families and relevant consumers; missing evidence keeps work open. Tangled dependencies prompt the smallest useful remedy, not automatic whole-suite or architecture review. 

**C2.** Scoped claims identify commit, components, checks, results and omissions, do not claim unrelated or untested combinations or all prior changes, and reopen when contradicted. Routine operations use affected checks; integration/release guidance recommends a representative cross-component workflow. Agents adapt to project requirements; Maintainers set high-level needs and material exceptions, not routine per-proposal coverage. Whole suites are optional unless required. Existing obligations cannot be silently removed or rescheduled; Cairn's full-tree pair and triggers remain.

**C3.** Ordinary and separate Security Reviews assess the committed implementation; all accepted criteria and checks pass, including wide Boundary B.

## Scope delta

**Scope delta**: preserved.

## Verification

The installer maps the shipped testing-discipline module to `dev/modules/testing-discipline.md` when selected (`bootstrap/_scaffold/config.py`); core-only installation must stand alone. Search direct readers, byte pins and examples before editing, with a known-positive control. `python tools/test_tiers.py for <paths>` maps final changes; pass the complete reviewed range for governing files. The current map for the named templates, methodology and module copies selects 23 test files, including `bootstrap/tests/test_certifying_run_rule.py`, `bootstrap/tests/test_verification_boundaries.py` and `bootstrap/tests/test_review_and_verification_rules_ship.py`. The first currently pins universal full-suite wording across both governing copies and methodology; the second pins both operational surfaces and the configured full suite; the third pins Boundary B and wide rules. Open assertions and selectors before changing them, preserve Cairn-specific ceremony protections, and remap any added paths. Run mapped iteration tests and applicable claim, link, snippet and neutrality gates and `python scripts/check_cairn.py`.

C2 applies installed guidance to a local reader, shared solver, uncertain cross-component dependency and existing mandatory release check, plus core without optional modules. A reviewer must find no scientist-designed routine policy, forced unrelated suite, accepted missing known consumer or waived requirement. Record who applied the examples and their outcomes; omission examples are the security preflight S2/S3 check, not an automatic coverage guarantee.

Boundary C: independent reviewers read committed implementation and iteration evidence and run targeted falsification checks. After review and fixes, run wide Boundary B on a clean unchanged final commit under canonical Python 3.13, covering mapped iteration and integration/workflow tests, owning families, known consumers and public paths, standing gates and examples. Record SHA/range, interpreter, clean pre/post state, commands, counts, elapsed time, tokens, non-pass dispositions and omissions. Do not run the full certifying suite for this work; Cairn's separate authorized ceremonies remain unchanged.

## Plan review -- Codex Sol (Reviewer) -- 2026-11-01

Reviewed commit: 41944b42
Target: scope, sequence, criteria and verification
Prior findings: none
Assurance path: high-assurance

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. C1 and C2 carry the accepted agent-led local and widened defaults, core-only usability and preserved obligations into criteria and installed examples. -- Plan Acceptance criteria and Verification; accepted proposal Proposal and Examples.
2. **Best alternative.** Amend core guidance alone, but that would leave templates, methodology and the existing optional module inconsistent. The plan reuses those surfaces and adds no selector or mandatory review program. -- Plan Scope and Reuse; `bootstrap/_scaffold/config.py` testing-discipline install mapping.
3. **What would show it wrong?** An installed core-only example needing scientist-designed coverage, an omitted known consumer, or a required release check waived would fail the planned examples and accepted criteria. -- Plan Verification and C1–C2.

The three named existing tests check certification wording, verification boundaries and shipped wide-mode rules; the plan directs the implementer to inspect their assertions, preserve Cairn-specific protections and remap changed paths rather than add duplicate tests by default. -- `bootstrap/tests/test_certifying_run_rule.py`, `test_verification_boundaries.py`, `test_review_and_verification_rules_ship.py`; Plan Verification.

Coverage: read committed plan, accepted proposal, plan review template, install mapping and named test assertions. Did not run the selector or tests, exercise installed cases, or perform Security Review.

## Plan review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commit: a666b9f049c61801e66d91c46393d7eb6a8f251b  
Target: complete plan against accepted supplied-default architecture  
Prior findings: none  
Assurance path: high-assurance

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none  
**Verdict**: ACCEPT  
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. C1 supplies practical component/contract/integration/workflow defaults, agent-owned effect mapping and relevant widening. C2 reserves high-level needs and material exceptions for Maintainers, preserves existing obligations and limits claims to tested scope. Core-only use prevents optional modules becoming hidden prerequisites. -- Plan, C1/C2, Scope and installed examples; accepted proposal, Proposal.
2. **Best alternative.** Change only core guidance. That is fewer edits but leaves templates and methodology's whole-ancestor claims contradictory; aligning existing homes and reusing tests avoids a selector, manifest or extra review program. -- Plan, Scope and Reuse; certifying-rule test surfaces and governing failure-path assertions.
3. **What would show it wrong?** A core-only reader needing scientist-designed coverage, a shared solver missing a known consumer, or an existing security/release requirement being waived under a renamed scoped suite. The installed local/shared/uncertain/mandatory cases and omission checks address those failures; final wide verification follows independent reviews. -- Plan, C2 and Verification; accepted requirement-preservation paragraph.

No blocking security finding. The named rule tests genuinely read governing/template/method surfaces and currently pin the universal contract; their changes must distinguish adopter defaults from Cairn's retained local protections. Verification assigns final-path mapping, reader/pin discovery and remapping before edits, with known-positive control and explicit coverage limits. The installer mapping confirms testing-discipline is optional.

Coverage: examined committed plan, ordinary review, accepted proposal/Decision, current plan template, installer mapping and representative certifying/boundary assertions. Did not reproduce the 23-file selection, inspect final test edits, exercise installed cases or run suites. Actual mapping, requirement-preservation evidence and clean canonical-Python wide Boundary B remain implementation obligations.

## Response to plan reviews -- Codex GPT-6.1 Sol -- 2026-11-01

Both reviews accepted the plan without findings. Final-path mapping, installed examples, preservation of existing requirements, separate Security code review and wide final verification remain implementation obligations. Elapsed: under one minute; tokens: unknown.

## Iteration evidence -- Codex GPT-6 -- 2026-11-02

Committed implementation: `1bac4fb1` through `9c110c14`; reviewed range begins at `6b8e8924`. The non-AGENTS changed-surface map selected 23 test files. The first union run on `1bac4fb1`, Python 3.13.13, collected 1,322 tests: 1,321 passed and one new wording guard failed because root AGENTS differed from the shipped copy. Commits `510b8531` and `9c110c14` aligned both copies. The affected node `test_verification_boundaries.py::test_scoped_defaults_reach_core_templates_and_optional_module` then passed on `9c110c14` (1 passed, 0.04 s). The union was not rerun; its prior passing results do not certify the corrected final bytes. The `AGENTS.md` selector for the reviewed range selects that same test file and omits 46 other readers under its >40 passage-pin rule. Wide Boundary B after code review must run the deduplicated mapped iteration plus integration/workflow selection.

Installed examples: the `solo-greenfield` scaffold installed core AGENTS and plan/proposal templates without `testing-discipline`; the `collaborative-team` scaffold installed the optional module, byte-identical to `dev/modules/testing-discipline.md`. Applying the installed guidance: a local reader maps to its unit/contract checks and a real entry path; a shared solver widens to its owner family, numerical benchmark and consumers; uncertainty is recorded and keeps known missing evidence open; an existing release check remains required. These are guidance exercises, not runs against an adopter's code or scientific model.

Checks: claim_check passed on all 12 changed documents; link_check passed on 11, excluding the self-hosted module whose existing optional sibling link does not resolve in Cairn's source home; snippets passed on 12; neutrality passed (0 failures, 43 informational findings); `check_cairn.py` passed (185 Markdown files, no issues, 93 external links not probed); `git diff --check` passed. No full-tree certification ran. Elapsed: approximately 20 minutes; tokens: unknown.
