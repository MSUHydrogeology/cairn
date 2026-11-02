# Plan: Supply practical scoped-certification defaults

**Source proposal**: dev/proposals/archive/2026-11-01-sol-project-certification.md
**Status**: archived
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

## Code review -- Codex Sol (Reviewer) -- 2026-11-02

Reviewed commit: 9c110c14
Target: 6b8e8924..9c110c14 and iteration evidence at d0e537c4
Prior findings: none
**Verdict**: REVISE. **Bounding**: WIDER RUN REQUIRED after fixes.
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Not yet: new affected-check guidance is useful, but installed core still mandates full-suite release certification and its claim covers all ancestors. -- `templates/core/AGENTS.md`, Verification; plan C2.
2. **Best alternative.** Revise the existing certification paragraphs and their existing tests to distinguish adopter scoped claims from Cairn's retained local ceremony, rather than add another mechanism. -- Plan Scope and C2; `bootstrap/tests/test_certifying_run_rule.py`.
3. **What would show it wrong?** An installed core-only project can certify a local change without unrelated suites, while its claim names tested scope and omissions and an existing mandatory release check remains owed. -- Plan C2 and Verification.

**B1 — blocking, accepted C2 unmet.** `templates/core/AGENTS.md` still directs the configured full suite before a release cut and says it certifies every preceding change; `docs/methodology/plans.md` repeats both. The new optional-whole-suite paragraph contradicts those rules. No scoped-certification claim rule was found in core, methodology plans or shipped plan/proposal templates (`git grep` for scoped certification and claim omissions at 9c110c14); thus C2's commit, scope, results, omissions and reopening semantics are not delivered. Existing `test_certifying_run_rule.py::test_the_governing_rule_names_its_integration_points_and_its_failure_path` still requires the universal ancestor claim on adopter core and methodology. Close by delivering C2 in shipped guidance, preserving Cairn's local full-tree requirements and existing obligations, and updating existing assertions to distinguish them. Exercise the accepted installed examples against the corrected bytes.

Coverage: compared committed core, methodology, module, changed tests and iteration record to C1/C2. Read-only targeted searches only; no suite, mutation, installed example or Security Review. Iteration union predates final bytes; final wide Boundary B remains owed.

## Security code review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: 9c110c14  
Target: `6b8e8924..9c110c14`; iteration `d0e537c4`, ordinary review `33ae2695`  
Prior findings: none in this Security code pass  
**Tier**: Security Review  
**Verdict**: REVISE; one blocking finding.  
**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** The architecture guidance fits the accepted intent: agents map effects without routine scientist approval. Delivery is incomplete because the old certification contract still governs adopters. -- Core diff; plan C1/C2; accepted proposal.
2. **Best alternative.** Replace contradictory certification paragraphs and revise existing assertions, preserving Cairn's local ceremony. No additional policy form, selector or review process is necessary. -- Plan Scope; existing certifying-rule tests and governing verification sections.
3. **What would show it wrong?** Installed core forcing a full suite solely to certify a local component, or scoped evidence claiming unrelated ancestors. Both outcomes remain prescribed by the current core paragraph despite the new optional-suite guidance. -- Committed `templates/core/AGENTS.md`, Verification; `docs/methodology/plans.md`, Tree certification.

**S1 — blocking, accepted C2 unmet.** Independently confirm ordinary B1: shipped core still requires the configured full suite before release and says it certifies every earlier change; methodology repeats that universal rule. Scope-limited certification and reopening contradicted claims are absent. The existing `test_certifying_run_rule.py::test_the_governing_rule_names_its_integration_points_and_its_failure_path` still requires the ancestor claim on adopter guidance. Close by delivering C2's scoped claim and reopening semantics, qualifying universal wording while retaining Cairn-specific requirements and existing project obligations, and correcting those assertions. Apply installed examples to corrected bytes; preserve required release/security checks.

**Bounding**: WIDER RUN REQUIRED — corrected scoped/mandatory installed cases and final mapped verification remain required.

Coverage: inspected committed guidance/tests, accepted scope, iteration and ordinary review; used targeted source searches. No suite or mutation run. Did not audit adopter dependencies or repeat installation. The iteration union predates final corrections; clean canonical-Python wide Boundary B remains owed after review fixes.

## Response to code reviews -- Codex GPT-6.1 Terra -- 2026-11-02

B1 and S1 accepted: `3d168701` replaces the adopter-wide release-suite and ancestor claims with scoped evidence and reopening, retains required checks and Cairn's local full-tree policy, and aligns methodology and shipped templates. `4358247d` corrects a stale proposal-template assertion found by iteration. No new mechanism was added.

On a separate copy of `4358247d`, canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) ran `test_certifying_run_rule.py` and `test_verification_boundaries.py`: 62 passed in 0.15 seconds. The earlier run on `3d168701` had 61 passed and one failed stale assertion; the latter commit fixes it. Link and snippet checks passed for five documents, neutrality reported zero failures (43 informational), and `check_cairn.py` passed on 185 files after initializing Git in the copy (94 external links not probed). Claim checks and diff checks passed on the changed documents before commit. No full suite ran.

The corrected `solo-greenfield` and `collaborative-team` installs succeeded. Core works without testing-discipline; the team module matches its source. Applying installed guidance, a local reader maps its own tests and entry workflow without an unrelated suite; a shared solver widens to benchmarks and consumers; an uncertain dependency leaves known missing evidence open; and a mandatory release check remains required. These are guidance exercises, not executions of adopter software. The new claim names commit, components, checks, results and omissions and reopens upon contradictory failure. Targeted review by the same ordinary and Security reviewers and final wide Boundary B remain owed. Elapsed: approximately 9 minutes; tokens: unknown.

## Targeted code review -- Codex Sol (Reviewer) -- 2026-11-02

Reviewed commit: 4358247d5e52e1639a4a7b28e63f9618120bf22b
Target: B1 correction `3d168701..4358247d` and response `5e21d5e7`
Prior findings: B1
**Verdict**: B1 closed; final wide Boundary B remains owed.
**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Shipped core now names the tested commit, scope, results and omissions, excludes unrelated and earlier work, reopens contradicted claims and preserves required checks. -- `templates/core/AGENTS.md`, Verification.
2. **Best alternative.** The correction revises existing guidance and assertions, without a new decision or mechanism; retaining the prior universal rule would leave C2 unmet. -- `docs/methodology/plans.md`; `bootstrap/tests/test_certifying_run_rule.py`.
3. **What would show it wrong?** A corrected core-only example forcing an unrelated suite or waiving a required release check would contradict the correction. The implementation response records both examples applied to corrected installs. -- Response to code reviews at `5e21d5e7`.

Cairn's own full-tree pair and triggers remain in root `AGENTS.md`; the revised test distinguishes that local contract from adopter scope. Agents still select routine coverage without per-change Maintainer approval. -- Root and shipped Verification; changed certifying-rule test.

Coverage: read committed correction, affected assertions and implementation response. No suite, mutation or independent installation run; the author reports 62 targeted passes and installed guidance exercises. Final wide Boundary B and separate Security review remain owed.

## Targeted Security code review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: 4358247d5e52e1639a4a7b28e63f9618120bf22b  
Target: S1 correction `3d168701` and `4358247d`; evidence `5e21d5e7`, ordinary follow-up `61563ff4`  
Prior findings: S1  
**Tier**: Security Review — second and final pass  
**Verdict**: S1 closed; no new finding.  
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Shipped core now names commit, components, checks, results and omissions, excludes unrelated/untested/earlier behavior and reopens contradicted claims. It requires project checks and ceremonies without imposing an unrelated whole suite. -- Corrected `templates/core/AGENTS.md`, Verification.
2. **Best alternative.** The correction replaces existing contradictory paragraphs and splits existing assertions between adopter scope and Cairn's local contract. This supplies C2 without a form, selector or routine Maintainer approval. -- Corrected methodology, shipped templates and certifying-rule tests.
3. **What would show it wrong?** A scoped claim waiving a mandatory security/release check or still certifying unrelated ancestors. The core clause and corrected shipped plan template explicitly prevent both; methodology separately preserves Cairn's green whole-tree claim. The author records corrected installed local/shared/uncertain/mandatory examples. -- Correction diffs; response at `5e21d5e7`.

**Bounding**: ACCEPTED — challenged the original universal-rule conflict and local/required-check distinction. Root `AGENTS.md` and executable ceremony commands are unchanged by these corrections. Revised tests check scope/reopening and retain Cairn's pair/triggers. Author evidence reports 62 targeted passes under Python 3.13.13, corrected installs and prose gates; no implementation checks rerun here.

Coverage: read committed corrections, changed assertions, implementation response and ordinary follow-up. Did not independently install, audit adopter dependencies, run mutation or suite, or certify the tree. This clears the Security Review obligation, not final integration: wide Boundary B remains owed on clean unchanged canonical-Python bytes.

## Response to targeted reviews -- Codex GPT-6.1 Terra -- 2026-11-02

B1 and S1 are closed with no new findings; the Security reviewer accepted the bounds. Final wide Boundary B and issue #33 closure remain owed before archive. Elapsed: under one minute; tokens: unknown.

## Implementation verification -- Codex GPT-6 -- 2026-11-02

**Boundary B mode**: wide. The change revises a cross-cutting certification contract, shipped core and team module, templates and published method; the selection includes owning contract families, install workflows, and public paths.

- **Tested commit**: `dd24ce0acc544c613c8d463153d8cd6d52390f2d`
- **Reviewed range**: `6b8e89242d54f6ecae78b5f0f86a68777e0b7d29..dd24ce0acc544c613c8d463153d8cd6d52390f2d`
- **Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13
- **Pre-run / post-run**: detached isolated clone was clean at the tested SHA before and after; generated JUnit reports were removed. `HEAD` remained the tested SHA.

The original non-AGENTS selector from the plan's iteration record yielded 23 files. The final reviewed-range selector yielded 11 files and reported 44 unpinned AGENTS readers omitted by its passage-pin guard. The deduplicated union ran each of those 23 original files plus final-selector-only `test_upgrade.py`; it also included relevant install workflow `test_install_time_onboarding.py`. No test file was repeated. The union was run as two non-overlapping commands because the original 23-file list was recovered after the initial batch.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python3.13 -m pytest -q --durations=10` on 14 unique files (final selector plus named/install checks) | 0 | 600 passed; no failures or skips | 61.17 s real (59.97 s pytest) | unknown |
| Same pytest command on the 11 original-selector files not in the first batch | 0 | 924 passed; no failures or skips | 10.44 s real (9.72 s pytest) | unknown |
| Combined unique selection | 0 | 1,524 passed across 25 files; no failures or skips | 71.61 s real total | unknown |
| Claim, link, snippet, neutrality and content gates | 0 | 13 claim-checked Markdown files OK; 11 link-checked files no issues; 515 docs no snippet drift; neutrality 0 failures/43 informational; 185 Markdown files no content issues | 5.1 s combined | unknown |

The final selector's other mapped files were `test_certifying_run_rule.py`, `test_onboarding_seed_roster.py`, `test_practice_modules.py`, `test_presets.py`, `test_replacement_tools.py`, `test_scientific_check_guidance_ships.py`, `test_session_routines.py`, `test_session_start_drain_rules.py`, `test_status_vocabulary_advisory.py`, and `test_verification_boundaries.py`; the plan's explicit `test_review_and_verification_rules_ship.py` and workflow `test_scaffold.py` were also included in the 23-file selection. Fresh `solo-greenfield` installation contained core AGENTS and plan/proposal templates without `testing-discipline`; fresh `collaborative-team` installation included it. Source, shipped and installed module bytes were identical. Applied the installed guidance examples: local reader -> affected checks and real entry workflow; shared solver -> owner family, numerical benchmark and consumers; uncertain dependency -> state uncertainty and keep known missing evidence open; mandatory release check -> retain the requirement. All four outcomes matched C1/C2. These were guidance exercises, not runs against an adopter's software or scientific model.

**Non-pass disposition**: tests had no failures or skips. Initial scaffold attempts refused because temporary target directories did not exist; after creating them, both fresh installs succeeded. `git diff --check` flagged Markdown hard-break trailing spaces in the plan's appended review records only (lines 129–133 and 176–180); these append-only review records were left intact. Link check left 1 external link and `check_cairn.py` left 94 external links unprobed.

**Known omissions**: per-file durations were not captured; no individual test file can be named for the 10-second consolidation list. The 44 unpinned AGENTS readers remain selector omissions. Full-tree certification was not run; this plan explicitly keeps Cairn's separate authorized ceremony unchanged. **Elapsed**: test commands 71.61 seconds real; prose gates 5.1 seconds; install/example inspections unmeasured. **Tokens**: unknown.


## Dispositions -- archive preparation -- 2026-11-02

**Dispositions**: none. Issue #33 is closed after the accepted testing architecture, installed examples and final wide Boundary B were completed. No deferred follow-up remains in this plan. Cairn's full-tree certification remains a separate authorized ceremony.

## Lasting-truth migration -- 2026-11-02

**Evidence shipped**: implementation and correction commits `1bac4fb1` through `dd24ce0a` update governing guidance, methodology, templates, module examples and existing assertions. The clean canonical-Python Boundary B record above covers the unique mapped union, standing gates, core-only and team installs, and accepted examples. **Evidence deferred**: none. **Deferred evidence home**: N/A. The separate full-tree ceremony remains governed by existing requirements.

**Fidelity sign-off**: implementation commits `1bac4fb1` through `dd24ce0a` match the accepted `## Proposal` in `dev/proposals/archive/2026-11-01-sol-project-certification.md`, accepted at its `## Decision`: agents map affected behavior and widen for shared boundaries, while preserving required checks and Cairn's local full-tree ceremony. Issue #33 is closed; the plan adds no new policy mechanism or outstanding follow-up.
