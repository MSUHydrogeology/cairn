# Plan: Verify changes at their scope

**Source proposal**: dev/proposals/archive/2026-10-28-codex-scoped-change-verification.md
**Status**: revising-code
**Waiting on Maintainer**: Required frozen-file ceremony
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Verify each change against its affected behavior and reserve whole-tree certification for authorized integration points.

## Source proposal

The accepted Current contract and Decision in the source supersede its opening where they differ. Planned changes need complete evidence on the final commit; trivial changes record checks of candidate bytes in their commit body. Tree certification is distinct and does not replace missing change checks.

## Scope

Reconcile `AGENTS.md`, `templates/core/AGENTS.md`, both plan and proposal templates, `doctrine/plans.md`, `doctrine/dual-review.md`, `doctrine/lifecycle.md`, `doctrine/proposals.md`, and `docs/glossary.md`; align the refusal message in `bootstrap/tests/conftest.py` with conditional push certification without changing guard behavior. Search readers and public paths again before editing; include any affected live governing consumer. Preserve installed wording's project-general form and neutrality. Do not retrofit archives. Existing accepted plans retain their written contract unless revised through their lifecycle; a plan requiring certification stays open until an authorized run or revision.

**User-authorized scope addition (2026-10-28; authorization in chat, not a Decision):**

> Your plan docs aren't following the right naming convention. See the archive. Can you check if the template specifies this? If not, please modify it and the other templates (And shipped copies) to specify the date as part of the naming.

Use `<YYYY-MM-DD>-<slug>.md` for plans and `<YYYY-MM-DD>-<author>-<slug>.md` for proposals and strategies. Keep the opening date when archiving; a plan's document-owned evidence folder uses the same stem and archives with it. Shared tests, scripts and assets stay in their canonical homes. Do not rename archived files.

Evidence artifacts (materialized at the declared paths after the final implementation SHA):
- `dev/plans/2026-10-28-scoped-change-verification/c2-record-adjudication.md` -- complete example and consumer/security omission variants; independent verdict pending.
- `dev/plans/2026-10-28-scoped-change-verification/c2-split-execution.md` -- commands, counts, outcomes and executed-node union.

**Reuse.** Extend the existing verification-boundary, certification, shipped-rule and broad-run guard tests; no parser, selector or new approval stage. Search: `rg -n 'Boundary B|certifying run|FULL RUN REQUIRED|full [|] bounded|full suite'` across live doctrine, templates and tests found those consumers and `bootstrap/tests/conftest.py`. Search touched paths for additional readers and test owners during implementation.

### Documentation / doctrine surface

Prescriptions belong in governing and published doctrine, per `docs/DOCUMENTATION_PLAN.md`; glossary describes the resulting terms. Proposal and plan are deliberation.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Map consumers and reconcile rules | Model-floor alignment implementation and code review complete before shared files are edited | Governing, doctrine, templates and glossary |
| C2 | Guard obligations and exercise the record | C1 | Tests, split collection evidence and illustrative reviewer verdicts |

## Acceptance criteria

**C1.** Planned Boundary B records the clean final commit/range, interpreter, commands, outcomes/counts, criteria and omissions. `bounded` covers affected behavior and consumers; `wide` covers owning families, known integration/public paths and gates. Search readers, imports, callers and public paths when uncertain. Missing checks/criteria keep work open; passing permits `Implementation verified at <SHA>`. Trivial work searches owners and runs checks on candidate bytes before commit, in a clean tree or separate copy; its commit body records search, commands, counts, interpreter, outcomes and omissions, and its SHA identifies those bytes. The author owns the trivial record; no Boundary C. Boundary C names gaps; implementation, test, executable-template or fixture changes require new final-commit evidence. Append certification by SHA without rewriting records or archives. Preserve accepted plans, ceremonies and conditional push certification; no override. Local and installed templates state dated plan/proposal/strategy names and same-stem plan evidence folders that archive with plans; archives keep their names.

**C2.** Rule tests detect removed obligations with positive and negative controls, without parsing records. A named independent reviewer, agent or human, evaluates a complete illustrative record (SHA, clean state, interpreter, producer, consumer, mandatory security check, commands, counts, outcomes, criteria and omissions) and variants separately omitting the consumer and security check. Record verdicts and missing checks; accept only passing complete evidence, reject omissions and keep claims open. For a selection exceeding 40 files, execute every split within the limit, record arguments, results and executed-node union, reconcile it with the original collected selection and exercise known cross-family and public paths. Preserve markers and shuffle seed; no override. Incomplete coverage keeps work open. S2: C2 runs omission and guard exercises. S3: mapped pytest and gates fire rule checks; the existing reviewer adjudicates examples.

The C2 example verdicts will be recorded in `dev/plans/2026-10-28-scoped-change-verification/c2-record-adjudication.md`; the executed split and reconciliation will be recorded in `dev/plans/2026-10-28-scoped-change-verification/c2-split-execution.md`.

## Scope delta

**Scope delta**: preserved.

## Verification

Use `/Users/kendal30/conda_envs/lhm/bin/python3.13`. Boundary A and final-commit Boundary B run the affected test families and gates below; expand the mapping for newly discovered consumers. The opening template's full-default wording conflicted with the accepted Current contract; both plan templates now express the scoped record and separate certification. This plan executes the accepted contract and does not itself authorize a whole-suite run. Record tested SHA and range, clean pre/post state, interpreter, commands, counts, timing, non-pass dispositions, criteria and omissions; certify separately at an authorized integration point. Boundary C challenges this mapping and performs independent targeted falsification.

- Operational and shipped obligations: `bootstrap/tests/test_verification_boundaries.py`, especially `test_change_verification_contract_reaches_every_surface`, `test_change_verification_guard_detects_removed_wide_fence`, `test_already_open_plans_keep_their_written_contract`, `test_boundary_c_adjudicates_a_scoped_record`, `test_both_plan_templates_carry_record_and_review_contract`, and `test_both_proposal_templates_reject_speed_as_coverage`.
- Certification and trigger preservation: `bootstrap/tests/test_certifying_run_rule.py`, including `test_the_governing_rule_names_its_integration_points_and_its_failure_path`, `test_reviewers_are_told_never_to_run_the_full_suite`, and `test_the_broad_run_refusal_no_longer_offers_the_override`. Extend the latter to distinguish conditional push certification from unconditional guidance, with a negative control; inspect actual release, re-anchor and security triggers.
- Both operational copies and trivial lane: `bootstrap/tests/test_review_and_verification_rules_ship.py::test_agents_md_carries_the_obligation`, `::test_agents_md_omits_the_forbidden_phrasing`, and `::test_an_empty_file_carries_no_obligation`.
- Guard and split: `bootstrap/tests/test_broad_run_guard.py::test_a_run_over_the_file_threshold_is_refused_regardless_of_selector`, `::test_the_file_threshold_boundary_is_exact`, `::test_collect_only_is_exempt_from_the_guard`, `::test_the_guard_refusal_follows_a_late_deselection`, and `::test_a_run_at_or_under_the_file_threshold_is_never_refused`, plus the C2 execution and union exercise. Open `bootstrap/tests/conftest.py` to verify the collection and execution triggers.
- Run `scripts/claim_check.py` for each authored document, `scripts/check_cairn.py`, `scripts/link_check.py`, and `scripts/quality_gate.py --sub neutrality --sub redundancy`; inspect each trigger and selection. Check snippet synchronization if a synced block changes. Search tests and manifests reading every touched surface; run their owners and any applicable frozen-file ceremony. Record any uncovered surface and keep required coverage open.


## Plan review -- Codex gpt-6.1-terra medium -- 2026-10-28

**Reviewed commit**: 865175bc
**Tier**: Internal
**Obligation**: Internal
**Verdict**: REVISE

**Foundations**

1. **Does it deliver the Decision?** The two lanes and reviewer exercise are mapped, but the execution union, trivial evidence, and certification migration need explicit criteria. -- plan `## Acceptance criteria`; source proposal `## Current contract`.
2. **Best alternative.** Keep the two chunks and existing tests; spell out these criteria and extend the existing guard-message test rather than create a new selector or stage. -- `bootstrap/tests/test_certifying_run_rule.py:67`; `bootstrap/tests/conftest.py:398`.
3. **What would show it wrong?** An example whose collected union matches while one required chunk never runs, or a changed record rewritten to claim certification, would meet the present wording without delivering the contract. -- plan `## Acceptance criteria`; source proposal `## Current contract`.

**F1 -- Blocking: require execution of the split union.** C2 compares collection for a selection over 40 files and records cross-family checks, but does not say to run every resulting chunk or record the executed union. Collection is explicitly exempt from the guard; matching collected IDs alone is not execution evidence. Require every split invocation to run within the limit, record its results and union, and show the required cross-family paths are exercised. Keep the collection comparison and no override. -- `bootstrap/tests/conftest.py:398-416`; plan C2.

**F2 -- Blocking: make both record migrations explicit.** C1 says the trivial author records “evidence” but does not require an otherwise clean tree or separate copy, the search, commands, counts, interpreter, outcomes and omissions in the commit body. Its certification-by-SHA wording also does not require an append-only entry, leaving historical records open to rewriting. Add those fields and clean-candidate condition; require a later append-only certification entry keyed by the certifying SHA. Preserve old plans until their authorized certification or lifecycle revision. -- source proposal `## Current contract`; plan C1 and Scope.

**F3 -- Blocking: reconcile the guard's live push guidance.** The guard's refusal says certification occurs “before a push” without the accepted conditional; the mapped test only checks for “certifying run” and absence of an override. C1 scopes other *governing* consumers, and C2 does not require this executable message or its test to change. Add the message to the migration and extend its existing test to distinguish a required push certification from an unconditional one, with a negative control. -- `bootstrap/tests/conftest.py:410-416`; `bootstrap/tests/test_certifying_run_rule.py:67-73`; `AGENTS.md:305`.

**Covered**: claims and execution path (#1-2: F1 and F3); completeness and refusal (#3-4: F1-F3); consistency and drift (#5-6: plan Scope and mapped test files); lifecycle and scope (#7-8: F2 and source Current contract); satisfiers (#9: each finding).
**Not covered / low confidence**: no implementation, example verdict, tests, security ceremony or full suite was run; this pass does not discharge the separate Internal Security Review.


## Plan review -- Codex gpt-6.1-sol high (Security Reviewer) -- 2026-10-28

```
Reviewed commit: 865175bc62bd74cbbd87ea84076f22d42f0dc7e7
Target: operative plan; accepted source Current contract and Decision at f110d263
Prior findings: none (ordinary pass at b0fbb948 read for coordination)
Assurance path: required(Internal + Internal Security Review)
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Does it deliver the Decision?** Mostly: C1 preserves required checks,
   separate certification and older-plan contracts; C2 retains independent
   judgment without a parser. Its execution and record-preservation criteria
   need the corrections below. -- plan C1-C2; source `## Current contract`.
2. **Best alternative.** Keep the two chunks, existing reviewer role and
   existing guard tests; make execution and immutable evidence explicit rather
   than adding a selector or approval stage. --
   `bootstrap/tests/test_broad_run_guard.py::_run`;
   `bootstrap/tests/test_verification_boundaries.py`.
3. **What would show it wrong.** A collected-but-unexecuted required selection,
   accepted missing security check, or rewritten historical verification record
   would defeat the promised safeguard. -- plan C2; source `## Current contract`.

**SR1 -- Blocking: collection does not prove the split checks ran.** C2 requires
matching collected unions but does not explicitly require executing every split
invocation. The guard exempts collection, and its file span is computed after
selection; the existing late-deselection test demonstrates why file counts alone
cannot prove coverage. This independently supports ordinary F1. **Satisfier:**
require all split invocations to execute within the limit, preserve their
selection arguments, results and executed-test union, and reconcile that union
with the original collected selection. Identify the checks exercising known
cross-family paths; a matching collection alone cannot close acceptance.
Keep the no-override and incomplete-coverage refusal. --
`bootstrap/tests/conftest.py::_refuse_broad_run_if_warranted`;
`bootstrap/tests/test_broad_run_guard.py::test_the_guard_refusal_follows_a_late_deselection`.

**SR2 -- Blocking: require preservation of the evidence being trusted.** C1's
trivial-lane “evidence” omits the clean-candidate condition and required commit
fields; separate certification “by SHA” does not require appending rather than
rewriting. These are ordinary F2's security consequences. **Satisfier:** name
otherwise-clean candidate bytes or a separate copy; search, commands, counts,
interpreter, outcomes and omissions in the trivial commit body; and a later
append-only certification entry keyed by SHA. Distinguish implementation
verification from pending tree certification while preserving accepted plans'
written obligations and archives. -- source `## Current contract`; plan C1.

The omission exercise correctly accepts only passing complete evidence and
rejects missing consumers/security checks through the existing reviewer role.
Ceremony preservation is implementable: the release command reaches detached
committed phases, including Bandit, release-mode pytest and quality gates;
re-anchor retains its launcher and Maintainer signing steps. C1 must preserve
those paths, alongside conditional push certification (ordinary F3). --
`bootstrap/security_check.py::main`, `::_phases`;
`bootstrap/REANCHOR_RUNBOOK.md`; plan Verification.

**Covered**: claims/execution/completeness/refusal (#1-4: SR1-SR2 and C2);
consistency/drift (#5-6: source contract, mapped rule tests and ordinary F3);
lifecycle/scope/satisfiers (#7-9: existing reviewer, ceremony entry points and
SR1-SR2). **Not covered / low confidence**: no implementation, illustrative
verdicts, tests or ceremonies executed; no full suite. Coverage truth remains a
reviewer judgment, and undiscovered dependencies remain possible.


## Response to plan review -- Codex gpt-6.1-terra medium -- 2026-10-28

| Finding | Disposition | Operative cell |
|---|---|---|
| F1, SR1 | Accepted | C2 and Verification: execute and reconcile split selections. |
| F2, SR2 | Accepted | C1 and Scope: candidate evidence and append-only certification. |
| F3 | Accepted | Scope and Verification: align guard message and its test. |


## Filename maintenance -- Codex (Coordination) -- 2026-10-28

Maintainer naming instruction, verbatim:

> "Your plan docs aren't following the right naming convention. See the archive. Can you check if the template specifies this? If not, please modify it and the other templates (And shipped copies) to specify the date as part of the naming."

The filename now uses its original Opened date. Its document-owned evidence
folder, where present, uses the same dated stem and archives with the plan.
This is a path migration, not a scope or lifecycle change. Historical review
and evidence citations retain the paths valid at their named commits; current
link destinations and operative targets use the dated paths.

## Implementation verification -- Codex gpt-6.1-luna low -- 2026-10-28

**Boundary B mode**: wide
**Tested SHA**: `69b8bc7e4f86fd6c669fd765a1ffe7951e9e10d9`
**Range**: `2ed8ddabc80c985ebc93171c7e628a7ec070459f..69b8bc7e4f86fd6c669fd765a1ffe7951e9e10d9`
**Certified by**: pending
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — Python 3.13.13
**Pre/post state**: detached worktree `/private/tmp/cairn-scope-worktree-69b8bc7e`; clean before and after; HEAD unchanged at tested SHA. `refs/cairn/gate-anchor` present at `443de20f81169fabe36c4ca3cc620206f7850254`.

**Selection and reconciliation**: Reader search selected 48 pytest modules. The five mapped guard nodes in `bootstrap/tests/test_broad_run_guard.py` ran separately; the other 47 modules were collected and executed in two invocations because the guard refuses selections above 40 files. Collection reported 2,700 node IDs. The sorted executed-node union contains 2,700 unique IDs, with zero missing and zero extra against the collected set; both lists have SHA-256 `56be3c2e7c2507e68c3faac1f93dd28f6f65946f1cb11cd291a6cb7f28ca3052`. All commands retained `--quality-gate-shuffle-seed=0`; no marker selector was used and `CAIRN_FULL_SUITE=1` was not set.

**Commands and outcomes**:

- Collection over the 47 explicit files listed in [`c2-split-execution.md`](2026-10-28-scoped-change-verification/c2-split-execution.md) with `python3.13 -m pytest -q --collect-only ... --quality-gate-shuffle-seed=0` — 2,700 collected; 1.33s.
- The first 40 sorted files listed in [`c2-split-execution.md`](2026-10-28-scoped-change-verification/c2-split-execution.md), run with `python3.13 -m pytest -vv ... --quality-gate-shuffle-seed=0` — 2,129 passed, 3 failed; 234.85s. The three failures were sandbox restrictions on disposable `ssh-agent` socket creation and loopback binding, not assertion failures in the changed contract.
- The remaining 7 sorted files listed in [`c2-split-execution.md`](2026-10-28-scoped-change-verification/c2-split-execution.md), run with `python3.13 -m pytest -vv ... --quality-gate-shuffle-seed=0` — 568 passed; 71.31s.
- The five exact broad-run guard node commands are listed in [`c2-split-execution.md`](2026-10-28-scoped-change-verification/c2-split-execution.md); all 5 passed in 3.44s. The refusal remains unchanged and applies regardless of selector.
- Elevated local rerun of the three affected mapped security nodes — 3 passed; 0.61s. Nodes: `test_gate_preflight.py::TestCandidateCodeCannotSignFromStageOne::test_the_candidate_position_cannot_sign_through_a_live_agent`, `...::test_the_same_key_signs_when_the_socket_is_present`, and `test_security_verification.py::TestNoCapabilityContract::test_a_socket_opening_child_is_excluded_by_admission_not_blocked_at_runtime`.
- `python3.13 -m pytest -q bootstrap/tests/test_verification_boundaries.py bootstrap/tests/test_certifying_run_rule.py bootstrap/tests/test_review_and_verification_rules_ship.py` — 129 passed; 0.17s.
- `python3.13 -m pytest -q bootstrap/tests/test_review_stance_in_shipped_files.py` — 480 passed; 1.16s. This owner module was rerun after its pinned wording exposed a missing accepted statement; the statement was restored in `doctrine/dual-review.md` before this final-SHA evidence.
- `python3.13 scripts/check_cairn.py` — 184 Markdown files, no issues. `python3.13 scripts/link_check.py` — 184 Markdown files, no issues. `python3.13 scripts/quality_gate.py --sub neutrality --sub redundancy` — zero failures. `python3.13 scripts/claim_check.py` on the authored governing and plan documents — 13 checks passed.

**Surface and omission disposition**: Covered operational and installed guidance, governing templates/doctrine, refusal text, the 47-file cross-family selection, all five guard nodes, and the three mapped security nodes. There is no known missing consumer or mandatory security check in this mapping. This scoped evidence does not certify the tree. Frozen-file gate-manifest/re-anchor ceremony remains pending; this record does not claim that ceremony passed. Independent C2 adjudication of the illustrative records and code review remain pending. No full suite was run.


## Code review -- Codex gpt-6.1-terra medium -- 2026-10-28

**Reviewed commit**: `26c8a055` (record and adjudication); implementation `69b8bc7e4f86fd6c669fd765a1ffe7951e9e10d9`
**Target**: scoped verification implementation commits `89e44c78`, `0566202e`, `69b8bc7e`, and final evidence `e052da5c`.
**Prior findings**: none

**Foundations**

1. **Does it do what it claims?** The six governed surfaces carry the wide-mode fence and the mapped guard detects its removal, but the plan's required ceremony remains uncompleted. -- falsification ledger; plan Verification and Implementation verification.
2. **Best alternative.** Retain the scoped mapping and separate certification; complete the prescribed ceremony at its authorized point or revise the plan through its lifecycle before claiming completion. -- plan Verification; `AGENTS.md` Verification boundaries.
3. **What would show it wrong?** A changed surface that loses the wide fence without its mapped test failing, or an unperformed required check treated as complete. -- falsification ledger below.

**Bounding**: WIDER RUN REQUIRED -- the plan requires any applicable frozen-file ceremony and its evidence records that ceremony pending. Complete and record the applicable ceremony before acceptance, or revise the plan's contract through its lifecycle; a scoped test run cannot replace it.

**F1 -- Blocking: required ceremony remains pending.** Verification requires the applicable frozen-file ceremony and the final record expressly leaves the gate-manifest/re-anchor ceremony pending. The plan's known required check therefore is not met; do not mark the plan ready to archive on the scoped evidence alone. This finding does not authorize changes to manifests or trust roots. -- plan Verification and Implementation verification; `AGENTS.md` Verification boundaries.

**Falsification ledger** (Python 3.13.13, detached local clones of `69b8bc7e`):

- Control: `python3.13 -m pytest -q bootstrap/tests/test_verification_boundaries.py::test_change_verification_contract_reaches_every_surface` -- 24 passed.
- In separate fresh clones, replace the wide fence with bounded in each tree-enumerated member: `AGENTS.md`, `templates/core/AGENTS.md`, `doctrine/plans.md`, `doctrine/dual-review.md`, `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`. Each mutation matched once and was killed by that targeted test (1 failed, 23 passed each).
- Examined the final verification record and independent C2 verdict against the plan's required checks; the ceremony remains explicitly pending (F1). The initial literal mutation pattern matched no surface because lines wrap; it was discarded and the whitespace-aware control above measured each actual member.

**Covered**: claims and execution (#1-2: control and mutations); completeness and refusal (#3-4: F1); consistency and drift (#5-6: six surface mutations); lifecycle, scope and satisfier (#7-9: plan Verification and F1). **Not covered / low confidence**: did not reproduce the 2,700-node selection or raw logs, execute the frozen-file ceremony, inspect every naming consumer, or certify the tree. Security Review is separate.

## Code review -- Codex gpt-6.1-sol high (Security Reviewer) -- 2026-10-28

**Reviewed commit**: `69b8bc7e4f86fd6c669fd765a1ffe7951e9e10d9`
**Target**: implementation `89e44c78`, `0566202e`, `69b8bc7e`; evidence `e052da5c`; independent C2 adjudication `26c8a055`.
**Prior findings**: ordinary code F1 read at `f19f4f53`.
**Tier**: Security Review
**Obligation**: Security Review of governing/vendor-neutrality verification rules and preservation of required security and trust ceremonies.
**Verdict**: REVISE -- obligation remains open for the prescribed frozen-file ceremony (ordinary F1); no additional security defect found.

**Foundations**

1. **Does it do what it claims?** The scoped evidence preserves required checks and separate certification, but cannot establish completion while its prescribed ceremony is pending. -- plan Verification and Implementation verification; `doctrine/plans.md`, verification boundaries.
2. **Best alternative.** Keep the existing guard and reviewer judgment; complete the Maintainer ceremony or obtain a lifecycle revision of that contract rather than treating scoped evidence as authority to waive it. -- ordinary F1; `bootstrap/REANCHOR_RUNBOOK.md` prerequisites and stages.
3. **What would show it wrong?** A guard bypass, acceptance of missing security evidence, or a scoped record replacing a ceremony would defeat this boundary. -- falsification ledger below.

**Bounding**: WIDER RUN REQUIRED -- ordinary F1 names the outstanding frozen-file gate-manifest/re-anchor ceremony. This review authorizes neither execution nor waiver of that Maintainer gate.

**Falsification ledger** (Python 3.13.13; fresh detached worktree at the reviewed implementation):

- Compared the AST of `_refuse_broad_run_if_warranted` with its pre-C2 version: statements before the final refusal are identical. Executed the reviewed function with controlled sessions: 40 files allowed; 41 refused; 41 with collection-only allowed; 41 with an existing stop preserved that stop. The refusal retained conditional push certification and exposed no full-suite override. These four boundary probes passed without running pytest selections or the full suite.
- Opened `bootstrap/security_check.py::main`, `::_phases`, release-suite and quality-gate runners: release preflight leads to detached committed phases, including Bandit, release-mode suite and quality gates. Compared that file, `bootstrap/REANCHOR_RUNBOOK.md`, and `bootstrap/reanchor-launcher.template.sh` with pre-C1 bytes: unchanged. The runbook still reserves comparison, signing and pushing to the Maintainer.
- Challenged missing-check acceptance against the committed C2 examples and independent verdicts: B remains open for the shipped consumer, C for the three security nodes; A accepts only its reported mapped checks and expressly leaves the ceremony open. The recorded same-SHA elevated rerun disposes of the three initial environment denials; it does not dispose of F1.
- Opened `scripts/quality_gate.py` dispatch and neutrality file selection: doctrine Markdown and shipped template types remain selected. Implementation evidence reports zero neutrality failures; no model names were introduced into governing shipped prose. No machine record parser or automatic coverage guarantee is claimed.

**Covered**: claims/execution/refusal (#1-4: guard probes and release dispatch); consistency/drift (#5-6: unchanged ceremony bytes and C2 verdicts); lifecycle/scope/satisfier (#7-9: ordinary F1, preserved conditional certification and ceremony authority). **Not covered / low confidence**: did not reproduce the 2,700-node logs, run the ceremony, certify the tree, or authenticate author-reported results. Mapping completeness remains reviewer judgment. No full suite or mutation sweep was run.

## Response to code review -- Codex gpt-6.1-luna low -- 2026-10-28

| Finding | Disposition | Current state |
|---|---|---|
| Ordinary code F1, `f19f4f53` | Accepted | The frozen-file gate-manifest ceremony remains required. Keep this implementation and plan open; the scoped record does not satisfy or replace it. |
| Security Review F1, `9d813013` | Accepted | The Security Review obligation remains open until the Maintainer completes and records that same ceremony. No waiver or scope reduction is granted here. |
| C2 example adjudication | Complete | Independent Terra adjudication is appended at `26c8a055`: A accepted for its reported checks, B and C rejected with their missing consumer/security checks named. |

**Status remains**: revising-code. The original implementation is at `69b8bc7e`; its evidence record is at `e052da5c`. A later documentation-only correction of live dated-name examples is at `5c525367` and has its own bounded evidence below; it does not resolve F1. Both reviews found no implementation defect. The outstanding action is the existing Maintainer-only frozen-file ceremony on the final reviewed tree: run `python bootstrap/tests/_gate_manifest.py verify` as part of the supervised procedure in `bootstrap/REANCHOR_RUNBOOK.md`, resolve and record any reported frozen-file or dropped-node discrepancy under that procedure, then return to the Maintainer for disposition. This response does not authorize editing the manifest, changing a trust root, signing, pushing, or treating any outstanding check as complete.

## Follow-up verification -- Codex gpt-6.1-luna low -- 2026-10-28

**Reviewed content commit**: `5c525367` (`doctrine/plans.md`, `doctrine/proposals.md`)
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — Python 3.13.13
**Change type**: prose-only correction of live filename examples; the historical archive text was not changed. The documents are not entries in `bootstrap/tests/fixtures/gate_manifest.json`'s `frozen_files` map.

**Reader search and owner tests**: `rg -l -F 'doctrine/plans.md' bootstrap/tests -g '*.py'` and the corresponding search for `doctrine/proposals.md` found the relevant readers. The resulting owner set was `test_certifying_run_rule.py`, `test_verification_boundaries.py`, `test_scope_reduction_trap.py`, `test_review_stance_in_shipped_files.py`, `test_stewardship_rules_ship.py`, and `test_status_vocabulary_advisory.py`. `python3.13 -m pytest -q` on those six files with `--quality-gate-shuffle-seed=0` passed 656 tests in 2.49s.

**Prose gates**: `python3.13 scripts/check_cairn.py` and `python3.13 scripts/link_check.py` each passed over 186 Markdown files. `python3.13 scripts/quality_gate.py --sub neutrality --sub redundancy` reported zero failures. `python3.13 scripts/claim_check.py doctrine/plans.md` and the corresponding command for `doctrine/proposals.md` both passed. A positive control matched seven obsolete forms in the pre-edit blobs at `918638f5`; the same obsolete-form search returned no matches in the current documents, while the explicit dated forms remain present.

This follow-up does not run or discharge the Maintainer-only frozen-file ceremony. No whole suite, manifest verification, trust-root operation, or push was performed.

## Scope amendment -- Codex (GPT-6.1 Sol) -- 2026-10-29

The Maintainer directs the plans to finish before the v0.6 baseline. The
following supersedes the frozen-file historical-anchor ceremony as an archive
prerequisite and the conflicting response above; earlier records remain intact.

> “They can each build the machinery, the new baseline does not need to be part of their plans. It can be a work board item for v0.6.”
>
> “If you want, build an anchor now to test that their machinery works properly. I'm okay either way. Remember: correctness of function is what matters, not of the trust root itself.”
>
> “Remove those requirements from the plans”

**Scope delta**: degraded. **Disposition**: defer to the v0.6 board item:
the actual frozen-file re-anchor and historical-anchor comparison or
reconciliation. The loss is that ceremony evidence within this plan; cutting it
follows the Maintainer's sequencing rather than specifying it here. Functional
verification and independent reviews remain required. This amendment itself
does not declare review findings resolved, change the trust root, or authorize
signing or pushing. Respond to the existing review findings under the revised
scope before moving the plan forward.
