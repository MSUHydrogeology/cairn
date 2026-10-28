# Plan: Verify changes at their scope

**Source proposal**: dev/proposals/archive/2026-10-28-codex-scoped-change-verification.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Verify each change against its affected behavior and reserve whole-tree certification for authorized integration points.

## Source proposal

The accepted Current contract and Decision in the source supersede its opening where they differ. Planned changes need complete evidence on the final commit; trivial changes record checks of candidate bytes in their commit body. Tree certification is distinct and does not replace missing change checks.

## Scope

Reconcile `AGENTS.md`, `templates/core/AGENTS.md`, both plan and proposal templates, `doctrine/plans.md`, `doctrine/dual-review.md`, `doctrine/lifecycle.md`, `doctrine/proposals.md`, and `docs/glossary.md`. Search readers and public paths again before editing; include any affected live governing consumer. Preserve installed wording's project-general form and neutrality. Do not retrofit archives. Existing accepted plans retain their written contract unless revised through their lifecycle; a plan requiring certification stays open until an authorized run or revision.

**Reuse.** Extend the existing verification-boundary, certification, shipped-rule and broad-run guard tests; no parser, selector or new approval stage. Search: `rg -n 'Boundary B|certifying run|FULL RUN REQUIRED|full [|] bounded|full suite'` across live doctrine, templates and tests found those consumers and `bootstrap/tests/conftest.py`. Search touched paths for additional readers and test owners during implementation.

### Documentation / doctrine surface

Prescriptions belong in governing and published doctrine, per `docs/DOCUMENTATION_PLAN.md`; glossary describes the resulting terms. Proposal and plan are deliberation.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Map consumers and reconcile rules | Model-floor alignment implementation and code review complete before shared files are edited | Governing, doctrine, templates and glossary |
| C2 | Guard obligations and exercise the record | C1 | Tests, split collection evidence and illustrative reviewer verdicts |

## Acceptance criteria

**C1.** Planned Boundary B records clean final SHA, range, interpreter, commands, outcomes, counts, omissions and criteria; `bounded` covers affected behavior and consumers, `wide` whole owning families, known cross-family paths and gates. Search readers, imports, callers and public paths when uncertain. Known missing checks or unmet criteria keep work open; all required checks and criteria passing permits `Implementation verified at <SHA>`. Trivial work searches owners, tests exact candidate bytes before commit and records evidence in its commit body; its author owns it without Boundary C. Boundary C names missing checks in `WIDER RUN REQUIRED`; new final-commit evidence follows changes to implementation, tests, executable templates or fixtures. Certification is separately recorded by SHA, with release, re-anchor and security ceremonies intact; push certification is conditional on Maintainer instruction at `787c558e`. No guard override. Old accepted plans and archives retain their contracts.

**C2.** Rule tests detect removed obligations and include meaningful positive and negative controls; they do not claim to parse records. A named independent reviewer, agent or human, evaluates a complete illustrative record (SHA, clean state, interpreter, producer and consumer, mandatory security check, commands, counts, outcomes, criteria and omissions) and two variants omitting respectively a known consumer and a mandatory security check: record verdicts and missing checks, accept the complete example only when its checks pass, reject both omissions and leave their claims open. Split a selection exceeding 40 test files at the guard limit; compare collected union to the original selection and record cross-family checks, without override. If required coverage cannot be established, keep work open. S2: C2 runs these omission and guard exercises. S3: mapped pytest and named gates below fire the rule checks; the existing reviewer role adjudicates examples.

## Scope delta

**Scope delta**: preserved.

## Verification

Use `/Users/kendal30/conda_envs/lhm/bin/python3.13`. Boundary A and final-commit Boundary B run the affected test families and gates below; expand the mapping for newly discovered consumers. The current template's full-default wording conflicts with the accepted Current contract: this plan executes that contract and does not itself authorize a whole-suite run. Record tested SHA and range, clean pre/post state, interpreter, commands, counts, timing, non-pass dispositions, criteria and omissions; certify separately at an authorized integration point. Boundary C challenges this mapping and performs independent targeted falsification.

- Operational and shipped obligations: `bootstrap/tests/test_verification_boundaries.py`, especially `test_bounded_boundary_b_contract_reaches_every_surface`, `test_bounded_guard_detects_a_removed_fence`, `test_already_open_plans_keep_their_written_contract`, `test_boundary_c_adjudicates_a_bounded_record`, `test_both_plan_templates_carry_record_and_review_contract`, and `test_both_proposal_templates_reject_speed_as_coverage`; update names and controls to the new contract.
- Certification and trigger preservation: `bootstrap/tests/test_certifying_run_rule.py`, including `test_the_governing_rule_names_its_integration_points_and_its_failure_path` and `test_reviewers_are_told_never_to_run_the_full_suite`; inspect actual release, re-anchor and security triggers.
- Both operational copies and trivial lane: `bootstrap/tests/test_review_and_verification_rules_ship.py::test_agents_md_carries_the_obligation`, `::test_agents_md_omits_the_forbidden_phrasing`, and `::test_an_empty_file_carries_no_obligation`.
- Guard and split: `bootstrap/tests/test_broad_run_guard.py::test_a_run_over_the_file_threshold_is_refused_regardless_of_selector`, `::test_the_file_threshold_boundary_is_exact`, `::test_collect_only_is_exempt_from_the_guard`, plus the C2 union exercise. Open `bootstrap/tests/conftest.py` to verify the collection and execution triggers.
- Run `scripts/claim_check.py` for each authored document, `scripts/check_cairn.py`, `scripts/link_check.py`, and `scripts/quality_gate.py --sub neutrality --sub redundancy`; inspect each trigger and selection. Check snippet synchronization if a synced block changes. Search tests and manifests reading every touched surface; run their owners and any applicable frozen-file ceremony. Record any uncovered surface and keep required coverage open.
