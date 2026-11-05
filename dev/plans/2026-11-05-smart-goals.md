# Plan: Achievable SMART goals

**Source proposal**: [Achievable plans that finish](../proposals/archive/2026-11-05-codex-atomic-implementation-plans.md)
**Status**: awaiting-code-review
**Plan review**: required(Internal)
**Opened**: 2026-11-05
**In brief**: Teach authors to set useful, independently finishable plan goals without losing accepted work.

## Source proposal

The [accepted proposal](../proposals/archive/2026-11-05-codex-atomic-implementation-plans.md) directs existing guidance to teach SMART goals and independent completion, preserving scope and checks without splitting work by default. The Decision at `1fe81f7a` authorizes ordinary plan and code reviews, not Security Review.

## Scope

Deliver one useful outcome: local and shipped authoring surfaces and existing guides consistently teach goal-first, independent completion, demonstrated in source and real installations. This helps authors choose achievable work while retaining the proposal's larger objective. Update `AGENTS.md` and `templates/core/AGENTS.md`; local and shipped `dev/proposals/_template.md` and `dev/plans/_template.md`; and `docs/methodology/proposals.md`, `docs/methodology/plans.md`, and `docs/methodology/lifecycle.md`. Extend the existing completion mapping and tests in `bootstrap/tests/test_review_sweep_ships.py`. Update `CHANGELOG.md` in the same or next implementation commit through parent serialization.

**Reuse.** The existing `_PLAN_COMPLETION_SURFACES` mapping and source/installed completion mutation tests in `bootstrap/tests/test_review_sweep_ships.py` already check this guidance and install profiles; extend them, not a new checker or test file. Search: `rg 'completion|surface_mutation|profiles' bootstrap/tests/test_review_sweep_ships.py` found those hooks. Doctrine belongs in governing and shipped authoring surfaces; explanatory guidance belongs in the existing methodology guides.

No runtime engine, parser, status, inventory or security-control change; no new form, tracker, enforcement apparatus, mass replanning or dropped outcome. Existing plans remain valid. A coherent helper and its consumers may share a plan; future goals remain proposal/board owned. An unavailable prerequisite keeps a goal queued, not open in an unfinishable plan. Preserve existing authority for deferrals, permissions and scope changes.

Also clarify the Cairn-only AST disposition in `AGENTS.md`, as the Maintainer
directed in chat on 2026-11-05: "Exactly, and that should be guidance going
forward in our project-specific rules" and "And the baseline happens at
release, and does not hold up plan closure". A verified expected mismatch
from reviewed engine changes stays unpassed until the separate release baseline
operation, but alone does not block archive. Unexpected drift, missing review
and other unmet implementation checks remain work. No baseline is changed here.

## Sequence

Available prerequisites are the current scaffold, existing completion tests and canonical Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`; no unfinished external plan or ceremony is needed. Estimate roughly one to two working days including review and checks, with uncertainty from coordination and test runtime. This is a planning window, not a deadline or waiver.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align guidance and extend existing tests | Plan review folded; coordinate shared files and changelog | Local, shipped and guide wording with source and installed controls |
| C2 | Exercise examples, review and close | C1 and ordinary code review; final wide Boundary B follows review | Recorded applications, passing evidence and archive-ready plan |

## Acceptance criteria

**C1.** Guidance places the specific useful result and relevance in Scope, observable completion in Acceptance criteria, and available capabilities plus a realistic uncertain work window in Sequence. A plan can implement, obtain required checks and reviews, and archive independently; internal chunks can depend on each other. A proposal may authorize several current or future plans: the first opening archives the proposal while queued siblings remain on the board linked to that immutable source; later unchanged authorized work needs no new Decision. No accepted outcome or safeguard is silently lost. Required failed functional, scientific or security checks remain implementation work; routine human operations have separately owned, evidenced board waits, and archive grants no release authority.

The proposal names each outcome, prerequisites and intended release or
capability; each queued board entry retains its source and revival condition.

Existing source checks cover all nine named guidance surfaces. In separate
copies of each actual surface, independently remove independent-completion
guidance and separately permit a human-only final task; each mutation must
fail through the owning test entry point, alongside passing controls. Real
scaffold installations across all shipped profiles retain and test the
shipped AGENTS, proposal and plan templates, including those mutation controls.
These checks detect specified wording changes; they do not enforce agent semantics.

**C2.** Record four agent applications, not a human trial: a coherent helper-plus-consumer goal, an unavailable helper, a later-release goal, and a missing-check/human-ceremony case. Each shows specificity, observable evidence, feasibility, relevance, estimated window and uncertainty, retained original scope, and whether archive is allowed. The cases distinguish an owned human operation from an unmet required check. Ordinary code review and all applicable checks pass before archive; no human-only final archive chore is introduced.

## Scope delta

Preserved. A proposed reduction or changed authority follows the existing Maintainer disposition; this plan does not concede accepted scope.

## Verification

Boundary A: before implementation use `python tools/test_tiers.py for <changed paths>` and, for governing text, its `--range BASE..HEAD` selection; run the returned affected tests and applicable claim, content/link, snippet and neutrality gates. Map changed surfaces to their readers and installed consumers, and record omissions and non-passes. Extend the named source and installed tests with separate per-surface mutations and passing controls; run the real profile installs. Record the four applications and their outcomes in the implementation record.

Boundary C: an independent ordinary code reviewer reads the committed implementation and iteration evidence, then runs only targeted falsification checks, not a suite. No Security pass is required by the Decision. Resolve findings under the existing review rules.

Boundary B: **wide**, because authoring guidance is a shared documentation contract. After code review, on a clean unchanged final commit under `/Users/kendal30/conda_envs/lhm/bin/python3.13` 3.13.13, run the exact mapped iteration list for the reviewed range, mapped integration/workflow tests, owning guidance and install consumers, and standing prose gates. Record the SHA and range, interpreter, clean pre/post state, commands, outcomes and counts, elapsed time, token use or unknown, non-pass dispositions, omissions and timing misses; list test files over ten seconds as required. No full-suite override or tree certification is authorized here. Missing evidence or a failed required check keeps implementation open.

## Plan review -- Codex gpt-6.1-terra -- 2026-11-05

Reviewed commit: 594cb47517a9858c1f88ac15b5291bc9b4ad7367

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, after the gaps below are folded: one coherent goal, nine named surfaces, four applications and wide verification deliver the Decision without arbitrary splitting -- Scope, Sequence, Acceptance criteria and Verification.
2. **Best alternative.** Retain the existing tests and authoring sections, extending their coverage rather than adding a checker; a narrower rollout would leave shipped guidance or accepted sequencing uncovered -- Scope and accepted proposal, Documentation / doctrine surface.
3. **What would show it wrong?** A separate surface mutation that survives its owning test, an installed profile missing guidance, or an example losing scope or treating an unmet check as complete would falsify delivery -- Acceptance criteria and `bootstrap/tests/test_review_sweep_ships.py`.

**F1 (blocking):** C1 preserves queued siblings and their source but omits the accepted proposal's requirement to name each outcome, prerequisites and intended release or capability in the Proposal section, and its board revival condition. Add these to the guidance outcome and observable criteria; otherwise later authorized work may remain visible without a usable trigger or sequence. Evidence: accepted proposal, Proposal 3 and 6; plan C1.

**F2 (blocking):** C1 requires each mutation to fail its owning check, but the existing tests call `_missing_completion` on altered strings rather than running the owning entry point against separately mutated files. Specify independent copies of each actual required surface, passing controls, and failure through the real owning test entry point; retain all-profile installed controls. This establishes the accepted per-surface evidence, not just matcher behavior. Evidence: `test_source_plan_completion_rule_and_surface_mutation` and `test_installed_plan_completion_and_surface_mutation`; `AGENTS.md`, Working tree and commits.

**Coverage:** Read committed plan, accepted proposal and Decision, plan template, and existing source/install test hooks; assessed scope, examples and verification by inspection. Did not run mutations or suites, inspect every consumer, assess implementation, or perform Security Review. The later relayed AST-baseline instruction was not part of the reviewed commit.

## Response -- Codex Terra -- 2026-11-05

**F1: accept.** C1 now names each queued outcome's prerequisites, intended
release or capability, source and revival condition.

**F2: accept.** C1 now requires separate real-surface mutations to fail at the
owning test entry point, with passing and installed-profile controls.

The Maintainer also explicitly directed the Cairn-only AST clarification in
Scope. It records expected mismatch as unpassed until release without making
that operation a plan-archive prerequisite; no trust record is changed.
**Elapsed**: unknown. **Tokens**: unknown.

## Implementation verification -- Codex gpt-6-luna (Low) -- 2026-11-05

**Source SHA**: `230e2425c9a3b6ff2e79aeae8d607605ee1e7536`
**Range**: `6e3f32e9..230e2425`
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` -- Python 3.13.13
**Tree**: clean before and after in a separate clone of the committed snapshot. The shared checkout was not used for tests.
**Tokens**: unknown.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---:|
| `python3.13 tools/test_tiers.py for <11 changed paths> --range 6e3f32e9..230e2425` | 0 | 23 test files selected; 30 broad AGENTS readers omitted by the guard | unknown | unknown |
| `python3.13 -m pytest <23 selected files>` at `0aca6581` | 1 | 1,640 collected; 1,633 passed; 7 failed in the changed review-sweep tests | 83.29 s | unknown |
| `python3.13 -m pytest bootstrap/tests/test_review_sweep_ships.py` at `230e2425` | 0 | 236 passed, including actual source and installed-copy mutations | 3.05 s | unknown |
| `python3.13 scripts/claim_check.py <each changed Markdown file>` | 0 | All ten Markdown paths clear; plan templates also rechecked before `230e2425` | unknown | unknown |
| `python3.13 scripts/link_check.py <ten Markdown paths>` | 0 | Ten files scanned; no issues; three external links not probed | 0.28 s | unknown |
| `python3.13 scripts/sync_doc_snippets.py --check <ten Markdown paths>` | 0 | Ten docs scanned; no drift | <0.01 s | unknown |
| `python3.13 scripts/content_scan.py <ten Markdown paths>` | 1 | Two pre-existing non-allowlisted GitHub URL flags in unchanged historical changelog entries; no new suppression added | 0.08 s | unknown |
| `python3.13 scripts/quality_gate.py --sub neutrality` | 0 | Zero failures; 43 informational notes | 1.08 s | unknown |
| `git diff --check` on committed source paths | 0 | Clean | unknown | unknown |

The 23 selected files were `bootstrap/tests/test_board_json_contract.py`,
`test_certifying_run_rule.py`, `test_claim_check_module.py`,
`test_core_dev_folders.py`, `test_documentation_plan_module.py`,
`test_install_report_slots.py`, `test_loop_fidelity_gate.py`,
`test_quickstart_sequence.py`, `test_replacement_tools.py`,
`test_review_and_verification_rules_ship.py`,
`test_review_stance_in_shipped_files.py`, `test_review_sweep_ships.py`,
`test_scaffold.py`, `test_scientific_check_guidance_ships.py`,
`test_scope_reduction_trap.py`, `test_session_routines.py`,
`test_session_start_drain_rules.py`, `test_status_vocabulary_advisory.py`,
`test_stewardship_rules_ship.py`, `test_upgrade.py`,
`test_upgrade_module_additions.py`, `test_verification_boundaries.py`, and
`test_verify_ref.py` (all under `bootstrap/tests/`).

The selector omitted these 30 broad `AGENTS.md` readers: `test_agreement_retired.py`,
`test_check_cairn_content.py`, `test_comprehension_floor.py`,
`test_doc_drift_tools.py`, `test_fork_advisory.py`, `test_gate_manifest.py`,
`test_gate_preflight.py`, `test_generated_output_scan.py`, `test_hardening.py`,
`test_install_time_onboarding.py`, `test_link_check_exclusions.py`,
`test_lockfile_module.py`, `test_model_tier_rule_ships.py`,
`test_module_merge.py`, `test_module_merge_lockfile.py`,
`test_next_session_local_note.py`, `test_notice_install.py`, `test_oracle.py`,
`test_quality_gate_neutrality.py`, `test_scaffold_substrate.py`,
`test_security_leaf.py`, `test_security_stack.py`,
`test_security_verification.py`, `test_slotmerge_leaf.py`,
`test_test_tiers.py`, `test_upgrade_edit_check_runs_no_project_programs.py`,
`test_upgrade_lockfile_path_containment.py`,
`test_upgrade_refuses_hostile_project_data.py`, `test_verify_integrity.py`,
and `test_writing_rules_ship.py` (all under `bootstrap/tests/`).

**Non-pass disposition.** The first mapped run exposed the missing explicit
human-final-task prohibition in both plan templates and stale mutation anchors;
the two template sentences were added at `230e2425`, then the owning file passed
all 236 cases. The two content-scan flags are unchanged historical links, not
introduced by this range. No files were individually timed during the mapped
run; the 83.29-second iteration exceeded the 30-second diagnostic target, and
per-file 10-second misses remain unmeasured. No full suite or certification
override ran. The one missed ordering check was the plan's `claim_check` before
the status-transition commit: it passed after `6e3f32e9`; the oversight was
reported, and all changed source Markdown was checked before its commit.

**Coverage map.** The 23-file selection includes source/install profile
consumers, the documentation and slot installers, verification/lifecycle
readers, and the owning review-sweep mutations. The focused rerun covers the
new actual-copy controls after the template fix. No shipped engine or runtime
path changed. **Review-ready after this record**: ordinary code review remains
owed; the four C2 applied examples and final wide Boundary B remain open and
must follow that review. Do not archive this plan.

## C2 applied examples -- Codex gpt-6-luna (Low) -- 2026-11-05

These four agent-applied examples demonstrate the accepted guidance; they are
not a human trial or evidence of human outcomes.

1. **Coherent helper plus consumers.** Scope: deliver one shared CLI argument
   helper and both command consumers. Observable result: both commands accept
   the same validated options and pass contract/workflow tests. All code is
   locally available; consistent CLI behavior is relevant to the accepted
   objective. Estimate: 1-2 working days, uncertainty about one day. Preserve
   all three outcomes and checks; archive only after delivery, reviews, checks
   and Boundary B pass. No child plan is needed.
2. **Unavailable helper.** Scope: deliver the accepted report-export consumer
   and validate its output against a named schema with a real workflow test.
   This serves the accepted export capability, but its validator is not shipped,
   so it is not achievable now. Keep the full consumer/check scope queued with
   its proposal source and validator-shipped revival condition. Afterward,
   estimate 1-2 working days, uncertainty about one day. No plan opens or
   archives yet.
3. **Later release.** Scope: retain the accepted offline-export outcome for a
   later release, with a deterministic archive and round-trip check as
   observable evidence.
   It is relevant to the proposal's offline capability and achievable after
   release 1 ships the format; estimate 2-3 working days afterward, uncertainty
   about one day. Preserve its full scope, source and release-capability revival
   condition on the board. The current plan may archive after its own criteria,
   reviews, checks and Boundary B; the later outcome stays queued.
4. **Missing check and human ceremony.** Scope: deliver the accepted checksum
   command; an independently specified functional test makes output observable.
   It is locally feasible and relevant; estimate 1 working day, uncertainty up
   to one day for the fixture. If that required test is missing or fails,
   implementation continues and archive is barred. Preserve the checksum
   outcome and the test obligation. A routine Maintainer-run
   release baseline instead stays in a separately owned, evidenced board wait;
   alone it does not bar archive once agent criteria, reviews and checks pass.
   A verified expected AST mismatch remains unpassed until release but alone
   does not block archive under the Cairn-local rule.

**Elapsed**: unknown. **Tokens**: unknown.

### 230e2425 template-fix verification

`230e2425` changed only `dev/plans/_template.md` and
`templates/core/dev/plans/_template.md`. Under the clean committed snapshot,
the canonical Python 3.13.13 `test_tiers.py for` selection for
`230e2425^..230e2425` selected 17 test files with no omissions. The owning
`test_review_sweep_ships.py` had already passed all 236 tests at this exact
commit, including source and installed-copy controls. To cover the remaining
selection without repeating that unchanged run, the other 16 selected files
were run and passed: 1,108 passed in 15.58 seconds, zero skipped or non-pass.
Together the full path-specific selection has 1,344 passing tests.

The six files from the earlier 23-file full-range selection that the 230e
path-specific map did not select were `bootstrap/tests/test_loop_fidelity_gate.py`,
`test_session_start_drain_rules.py`, `test_stewardship_rules_ship.py`,
`test_upgrade.py`, `test_upgrade_module_additions.py`, and
`test_verify_ref.py`. They passed in the earlier mapped run at `0aca6581` and
do not name either template changed by `230e2425`; their test/source inputs are
unchanged, so those results are reused rather than rerun.

The full 17-file selection was: `bootstrap/tests/test_board_json_contract.py`,
`test_certifying_run_rule.py`, `test_claim_check_module.py`,
`test_core_dev_folders.py`, `test_documentation_plan_module.py`,
`test_install_report_slots.py`, `test_quickstart_sequence.py`,
`test_replacement_tools.py`, `test_review_and_verification_rules_ship.py`,
`test_review_stance_in_shipped_files.py`, `test_review_sweep_ships.py`,
`test_scaffold.py`, `test_scientific_check_guidance_ships.py`,
`test_scope_reduction_trap.py`, `test_session_routines.py`,
`test_status_vocabulary_advisory.py`, and
`test_verification_boundaries.py` (all under `bootstrap/tests/`).

Standing prose evidence on the same committed snapshot is reused from the
prior record: claim checks passed on the changed plan templates and all ten
changed Markdown files; link check passed on ten docs with three external
links unprobed; snippet check passed on ten docs; neutrality had zero failures
and 43 informational notes. Content scan retained only the same two flags on
unchanged historical GitHub links in `CHANGELOG.md`. These gates' inputs were
unchanged by `230e2425` except for the two plan-template sentences already
checked; no new path, link, snippet or neutrality trigger was introduced.

**Remaining evidence.** Ordinary code review is still owed. After review, run
the plan's final wide Boundary B on the reviewed range, including the exact
mapped iteration list and integration/workflow tests, record per-file timing
misses, and close any review findings. No full suite or certification run is
authorized.

**Coordination note.** The November 1 intent claims from `codex-ce051c38` on
`docs/methodology/proposals.md` and `docs/methodology/plans.md` remained active
during implementation. The assignment identified them as apparently stale,
but their owner status was not confirmed; do not treat them as released. The
overlap was reported before editing, and no further edits to either guide are
in progress. **Elapsed**: unknown. **Tokens**: unknown.

**C2 plan-record checks.** `claim_check`, `link_check`, snippet check and
`content_scan` all passed on this plan after the examples were finalized;
neutrality had zero failures and 43 informational notes (0.92 s). No runtime
or behavioral test applies to this prose-only plan-log addition. **Tokens**:
unknown.
