# Plan: Align model floors with the team roster

**Source proposal**: dev/proposals/archive/2026-10-28-codex-model-floor-alignment.md
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Align the task-based capability floors and Cairn's local model assignments while keeping review and authority safeguards.

## Source proposal

The Maintainer accepted revised proposal 3 and added the Antigravity families in
Decision `63e315fa`. Its task-based floors and safeguards govern this plan;
model-family assignments apply only to Cairn.

## Scope

Align `doctrine/roles.md`, `AGENTS.md`, `templates/core/AGENTS.md`,
`dev/modules/model-selection.md`, `templates/modules/team-gated/model-selection.md`,
`bootstrap/BOOTSTRAP.md`, and `templates/onboarding/collaborative-team.md` and
`templates/onboarding/high-rigor-legacy.md`. Update Cairn's local
`dev/.cairn/model-selection-mapping.yml` and affected tests. Search lifecycle
prose for conflicting floor or scribing guidance; resolve every conflict within
the accepted rule. No installer, checker or schema change is authorized.

**Reuse.** N/A: no code added. Searches for model-selection and tier references
in `bootstrap/tests`, and floor and scribing references in the named sources,
found existing copy, installation, mapping and wording checks to update or run.

### Documentation / doctrine surface

Cross-cutting prescription belongs in `doctrine/roles.md` and the governing
`AGENTS.md` copies; module, bootstrap and onboarding copies deliver it to
adopters. Vendor names belong only in Cairn's local mapping and deliberation.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align floor, fan-out, mapping and install guidance together | Both plan reviews and author response | Source copies, local mapping and owning tests |
| C2 | Record scoped integration evidence and hand off for code review | C1 committed | Verification record; certification pending |

## Acceptance criteria

**C1.** High covers strategy, premise, novel design and security or trust-boundary
judgment and Security Review; medium covers proposal authoring and ordinary
proposal, plan and code reviews; low covers execution of accepted reviewed plans,
including high-risk and non-trivial chunks, trivial work and authorized Decision scribing. Lane governs process; task governs floor. Both
module copies align fan-out, bright-line and below-floor rules and retain all
review, governance, escalation and scribing safeguards.

Cairn's mapping has dated Maintainer-assigned high/medium/low rows for
Opus/Sonnet/Haiku, Sol/Terra/Luna and Argon/Pro/Flash, with no Astra or Fable
defaults and no benchmark claim. Shipped text stays vendor-neutral. Installation
seeds one family per tier; module, bootstrap and both onboarding copies explain
manual additional family rows using the existing schema. Tests exercise rule, copies, installation and multiple rows. Inspect the first
dated low-tier implementation and review for missed criteria or floor-related
defects; record the result when available.

**C2.** Record the tested commit, reviewed range, canonical interpreter,
pre/post clean state, commands, counts, elapsed times, non-pass dispositions and
omissions. The record states full mode and certification pending; independent
code review follows. No full suite is run for this plan alone.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: update and run `python -m pytest bootstrap/tests/test_model_tier_rule_ships.py`
(including its lane, proposal, fan-out, copy and solo-install checks),
`python -m pytest bootstrap/tests/test_review_stance_in_shipped_files.py` (module floor and
cost-rule obligations), `python -m pytest bootstrap/tests/test_onboarding_seed_roster.py`, and
`python -m pytest bootstrap/tests/test_model_selection_stub.py` (local mapping, copy, interactive
capture, bootstrap and onboarding paths). Add a multiple-family mapping check
and a real installed guidance check in the owning test files. Re-search test
readers of every touched surface before implementing; run any additional owners
found. Check the search against the known `test_model_tier_rule_ships.py` reader.
Run `python scripts/check_model_selection.py`, `python scripts/check_cairn.py`,
`python scripts/link_check.py`, `python scripts/quality_gate.py --sub neutrality
--sub redundancy`, and `python scripts/claim_check.py <file>` for each changed
Markdown file. Open the named triggers and report what they actually check.

Boundary B: this changes governing and shipped high-risk doctrine, so full mode
is mandatory. After the final implementation commit run the scoped mapping and
gates above on a clean unchanged commit under
`/Users/kendal30/conda_envs/lhm/bin/python3.13`; record **Certified by**: pending
until the next certifying run covers it. The certifying run, not this plan's
implementation or review, owns the full suite. Boundary C is independent targeted
falsification by the code reviewer. No new security check or trigger is added;
the proposal's S1–S5 and existing human checks remain unchanged.

## Plan review -- Codex gpt-6.1-terra (Internal reviewer) -- 2026-10-28

Reviewed commit: 07a08d19e706411f1ce876f65207c8dea1aff0ac
Target: Source proposal, Scope, Sequence, Acceptance criteria, Scope delta, Verification
Prior findings: none
Assurance path: required(Internal + Internal Security Review)

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The named sources and pending certification can deliver the Decision, but the mapped checks need explicit properties for the new distinctions -- `dev/plans/model-floor-alignment.md`, C1 and Verification.
2. **Best alternative.** Extend the existing owning checks and real-install checks rather than add a new gate; retain the source and installed copies -- `bootstrap/tests/test_model_tier_rule_ships.py`; `bootstrap/tests/test_onboarding_seed_roster.py`.
3. **What would show it wrong.** A changed floor or installed instruction that contradicts the accepted rule while the mapped checks pass would show the evidence cannot establish delivery -- `dev/proposals/archive/2026-10-28-codex-model-floor-alignment.md`, “Rule and boundary”; `bootstrap/tests/test_review_stance_in_shipped_files.py`, `_MODEL_OBLIGATIONS`.

**F1 (blocking): Map the semantic properties to their checks.** C1 asks that tests exercise the rule and fan-out, but the verification mapping names files and broad areas, not the new properties each must catch. The existing fan-out check in `bootstrap/tests/test_model_tier_rule_ships.py` checks the stronger-check clauses, while `bootstrap/tests/test_review_stance_in_shipped_files.py` currently pins the old proposal-review and bright-line wording. Merely updating those old assertions can leave a low floor for ordinary unreviewed non-trivial writing, a high floor for settled high-risk plan execution, or an unchanged standard-lane floor undetected. The existing mapping checker validates shape, not the assigned families. **Satisfier:** map the owning tests or nodes to the task-versus-lane distinction, all three fan-out categories, the high-judgment/low-execution boundary, the below-floor-only check, and each assigned local family/tier; require checks on relevant source and installed guidance, including both onboarding paths. Make each check fail for the wrong property rather than just finding a general tier word.

**Covered:** claims and scope (accepted “Delivery and evidence” and plan C1); public installation and cross-document drift (`bootstrap/tests/test_model_tier_rule_ships.py::test_a_profile_with_no_module_still_installs_the_rule`, `bootstrap/tests/test_onboarding_seed_roster.py`); design, silent failure and satisfier (F1); lifecycle and verification placement (plan Sequence and Verification; `dev/plans/_template.md`, Verification); reuse search (`rg -n -i 'tier|floor|fan.out|scrib|model.selection'` over named sources and owning tests, with the known test reader as positive control); domain limits (accepted “Signals and scope”).
**Not covered / low confidence:** No implementation exists to exercise, and no tests or capability benchmarks were run. I did not independently verify the security-preflight threat analysis.
