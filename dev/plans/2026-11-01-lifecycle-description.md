# Plan: Align lifecycle descriptions

**Source proposal**: dev/proposals/archive/2026-11-01-codex-lifecycle-description.md
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Correct four published descriptions so readers can see when a proposal needs a plan.

## Source proposal

The Maintainer accepted the heavy proposal at `2867a8e6`: describe the existing lifecycle consistently, without changing its rules or safeguards.

## Scope

Correct `README.md`, `docs/assets/three-lanes-of-change.svg`, `docs/release-process.md`, `docs/methodology/lifecycle.md`, the diagram alternative text in `docs/index.html`, and the two lifecycle references in `docs/quickstart.md`. The published method is a protected doctrine surface; the other three describe the workflow. The operative prescription in `AGENTS.md`, shipped templates, and enforcement stay unchanged. Coordinate the lifecycle method with its existing claim holder before editing.

**Reuse.** N/A: no code added. Reuse the existing diagram and lanes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align descriptions and accessible diagram text | Plan review, including Security Review | Six corrected existing surfaces |

## Acceptance criteria

C1: All six surfaces agree with `AGENTS.md` and the accepted cut-the-apparatus Decision: light is the default and has no plan, including wide or multi-area work; non-trivial standard and heavy work uses plan triage; named high-risk surfaces and added or widened trust boundaries trigger heavy. Preserve the outer lanes and all other review and check obligations. The diagram's visible labels, title, description and README alternative text agree. No new process, prescription or enforcement is introduced. Inspect the rendered diagram and accessibility text. A deliberate mutation asserting that light needs a plan must be detected by comparison with governing text; record the result.

## Scope delta

**Scope delta**: expanded. The Maintainer approved adding the website's image description and two quickstart passages to the accepted four surfaces. Asked: “The accepted lifecycle correction names four files. I found the same outdated wording in the website’s image description and two quickstart passages. May I include those small corrections in the same work so the published explanations agree?” Answer: “Yes, include both”. This adds no process or safeguards; the accepted scope remains intact.

## Verification

Boundary A: Run all files selected by `python tools/test_tiers.py for README.md docs/assets/three-lanes-of-change.svg docs/release-process.md docs/methodology/lifecycle.md` (32 at planning). The selector matches file names as well as paths, so many `README.md` hits are fixtures for other files, but the full selection remains required. Run claim and link checks on the changed Markdown, snippet sync in check mode, and the neutrality gate; these test paths, links, snippet drift and neutral language, not lifecycle meaning.

Direct readers: `test_review_and_verification_rules_ship.py::test_light_tier_can_ship_wide_work_without_a_plan` pins two lifecycle statements; `test_status_vocabulary_advisory.py::TestTheVocabularyMatchesTheDoctrineDiagrams::test_lifecycle_diagrams_draw_exactly_the_words_in_the_table` and `test_board_json_contract.py::TestGuideLookupMatchesLifecycle` check lifecycle status diagrams and their consumers. `test_stewardship_rules_ship.py::test_small_fix_rule_and_capture_pointer_reach_install`, `test_scope_reduction_trap.py::test_scope_reduction_obligation_present`, and `test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement` / `test_doctrine_omits_the_retired_privilege` pin other lifecycle obligations. `test_review_stance_in_shipped_files.py::test_readme_explains_the_review_contract` and `test_descriptive_page_omits_the_old_wording` read the root README. Run whole selected files, including their parameterized cases. Path citations in `test_loop_fidelity_gate.py`, `test_claim_check_module.py` and `test_session_start_drain_rules.py` are fixture text or references, not reads of the changed lifecycle. No selected direct reader tests the SVG or release-process semantics; compare them and README accessible text against the operative rules and perform the specified mutation and visual checks.

Indirect readers and pins: path and basename searches across scripts, tools, bootstrap and manifests found the direct readers above; `check_cairn.py`, `link_check.py` and `sync_doc_snippets.py` also discover tracked Markdown, while `quality_gate.py` walks docs for neutrality and `test_review_stance_in_shipped_files.py` scans live docs. Run `python scripts/check_cairn.py`, `python scripts/link_check.py README.md docs/release-process.md docs/methodology/lifecycle.md`, `python scripts/sync_doc_snippets.py --check README.md docs/release-process.md docs/methodology/lifecycle.md`, individual `python scripts/claim_check.py <file>` for those three, and `python scripts/quality_gate.py --sub neutrality`. The SVG and HTML image description are covered by render and accessible-text inspection, not Markdown gates. Include `docs/quickstart.md` in the Markdown gate commands. A repository search for the four current SHA-256 digests found no byte pin; the same search found the known digest of `bootstrap/tests/fixtures/skills/README.md` in `protected_test_roster.json` and `gate_manifest.json`. This does not rule out a differently expressed or stale pin.

For the added paths, `python tools/test_tiers.py for docs/index.html docs/quickstart.md` selects `test_quickstart_sequence.py` and `test_review_stance_in_shipped_files.py`, already in the 32-file selection. `TestLayerAStepsOneThroughThree::test_step3_install_writes_expected_kernel_and_modules` reads quickstart counts and install commands; `test_descriptive_page_omits_the_old_wording[docs-quickstart-md]` scans retired wording. Neither tests the two changed lifecycle passages or HTML alternative text; compare those directly with the operative rules. The Markdown corpus readers above include quickstart; inspect the HTML image description alongside the rendered SVG. Searches in scripts, tools, bootstrap and manifests found no direct HTML test or current SHA-256 pins for either added file; the same digest search found the known fixture hash in the protected roster and gate manifest. Stale or differently expressed pins remain possible.

Boundary C: ordinary code review and separate Security Review examine the committed implementation and iteration evidence, and run targeted falsification checks rather than a suite.

Boundary B: wide, because published methodology is a protected doctrine surface. After review, run once on a clean unchanged final commit under canonical Python 3.13.x: the iteration selection for the reviewed range, integration/workflow tests in the tier map naming those files, and the applicable prose and plan-specific checks. For the four paths, those integration/workflow tests are already in the 32-file selection: `test_check_cairn_content.py`, `test_claim_check_module.py`, `test_link_check_exclusions.py`, `test_module_roster.py`, `test_onboarding_seed_roster.py`, `test_prune_tools.py`, `test_session_start_drain_rules.py`, `test_finalize_retired_living_state.py`, `test_presets.py`, `test_quickstart_sequence.py`, `test_scaffold.py`, `test_upgrade.py`, `test_upgrade_added_slots.py`, and `test_upgrade_module_additions.py`. Cover affected consumers and public paths; record commands, counts, interpreter, SHA/range, clean pre/post state, elapsed time, non-passes and omissions. Coordinate this selection with other concurrent work on the common final commit. No full-tree certification is authorized by this plan.

## Ordinary plan review -- Codex GPT-6.1 Sol -- 2026-11-01

**Obligation:** Internal
**Verdict:** Revise before implementation; one blocking finding.

**Foundations**

- **Should it happen as framed?** Yes. C1 addresses all four accepted descriptions, including accessible diagram text, while preserving tier and security rules. Evidence: plan Scope and C1; accepted proposal Proposal.
- **Best alternative:** Correct only the README and diagram; that costs fewer edits but leaves the release process and published method contradictory. Evidence: accepted proposal Alternatives considered.
- **What would show it wrong?** A description requiring a light plan or weakening the heavy trigger would contradict the operative rules. Evidence: plan C1; accepted proposal Signals and `AGENTS.md` Review.

**Blocking finding:** The accepted proposal requires reader triggers, exact applicable nodes and the Boundary B selection to be mapped during planning. The plan lists 32 selected files and preliminary path matches, but postpones the full search and trigger inspection. A path match alone does not establish coverage: for example, `test_stewardship_rules_ship.py` reads lifecycle text for a Maintainer-decision assertion. Complete the mapping and record exact applicable nodes, triggers, consumers and any gaps in the operative plan before implementation; combine overlapping selections without dropping required coverage.

**Coverage:** Read the committed plan and accepted proposal at `b97a4788`, current plan template and an example reader trigger. Did not enumerate all readers, inspect final wording or render the diagram; those remain for planning and implementation. Separate Security Review remains outstanding. No suite run. Elapsed: approximately 3 minutes; tokens: unknown.

## Response -- Codex (GPT-6) -- 2026-11-01

The review correctly identifies a mapping gap. The Verification cell now identifies direct readers and their triggers, the selected integration/workflow files and semantic coverage gaps. The indirect-reader and byte-pin search remains incomplete; this finding is not yet closed. Elapsed: approximately 4 minutes; tokens: unknown.

## Mapping follow-up -- Codex (GPT-6) -- 2026-11-01

The Verification cell now identifies corpus readers, commands, digest search and its positive control. The mapping finding is addressed; separate Security plan review remains. Elapsed: approximately 3 minutes; tokens: unknown.

## Scope expansion -- Codex (GPT-6) -- 2026-11-01

The Maintainer allowed the two additional files as quoted in Scope delta. The operative cells and mapped checks now include them. Review the widened scope before implementation; Security plan review remains owed. Coordinate the final selection with concurrent work. Elapsed: approximately 3 minutes; tokens: unknown.

## Plan review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commit: 84a81f8779a6daf45f830d37f91eea7550b2e076  
Target: revised plan, including approved HTML and quickstart additions  
Prior findings: ordinary mapping blocker read  
Assurance path: high-assurance

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none  
**Verdict**: ACCEPT  
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. C1 preserves named high-risk and added/widened-boundary triggers, outer lanes and required reviews/checks. Scope leaves governing instructions, shipped templates and enforcement unchanged. The two additional surfaces have the Maintainer's explicit allowance quoted in Scope delta, and retain the accepted descriptive outcome. -- Plan, Scope, C1 and Scope delta; accepted proposal, Proposal and Decision.
2. **Best alternative.** Correct the existing descriptions and reuse their mapped checks plus direct comparison/rendering. A new semantic checker or classification form adds maintenance without being necessary for the accepted human comparison. -- Plan, Verification and C1; accepted proposal, no-new-process constraint.
3. **What would show it wrong?** Light work still acquiring a plan, deliberate work being equated with heavy, or a high-risk trigger disappearing. C1 compares all six surfaces with the governing rules, includes accessible text and requires a deliberately wrong light-plan example to be detected. -- Plan, C1 and Verification; accepted cut-the-apparatus, cut 2.

The original mapping blocker is addressed: Verification now identifies direct reader nodes, corpus runners, integration/workflow selection, positive-control pin search and explicit semantic gaps. The added paths are mapped too. The inspected light-tier, lifecycle-vocabulary and README reader assertions support those coverage distinctions. No new security apparatus is needed.

Coverage: examined committed revised plan, accepted proposal/Decision, current plan template, ordinary finding and responses, and representative reader assertions. Did not exhaustively reproduce discovery, inspect final wording, render output or run the mutation/tests. Common final verification remains post-review on clean canonical-Python bytes, with plan-specific checks retained. No suite run.

## Plan review response -- Codex (GPT-6) -- 2026-11-01

The ordinary mapping finding was addressed in the Verification cell and mapping follow-up. Security plan review found no additional findings and reviewed the approved expansion. Both required plan obligations are complete; C1 may begin. Elapsed: approximately 1 minute; tokens: unknown.

## Implementation verification -- Codex (GPT-6) -- 2026-11-01

Changed surfaces: `README.md`, `docs/assets/three-lanes-of-change.svg`, `docs/release-process.md`, `docs/methodology/lifecycle.md`, `docs/index.html`, and `docs/quickstart.md`. Compared the descriptions with the operative lifecycle rules and accepted Decision: light is the default with no plan; non-trivial standard/heavy accepted proposals use plan triage; named high-risk surfaces and added or widened trust boundaries trigger heavy. The SVG metadata, accessible description, visible labels and rendered footer were inspected. This is a manual semantic comparison; the required deliberate light-needs-a-plan mutation is not yet run.

Checks performed under Python 3.12.9: `claim_check.py` passed for each of the four changed Markdown files; `git diff --check` passed for all six paths. `python tools/test_tiers.py for README.md docs/assets/three-lanes-of-change.svg docs/release-process.md docs/methodology/lifecycle.md` selected 32 files. This command selected tests; it did not run them. `rsvg-convert` rendered the SVG and its visible content was inspected. Elapsed: approximately 4 minutes. Tokens: unknown.

Mapped iteration files not yet run (32): `test_board_json_contract.py`, `test_ceremony_review_report.py`, `test_check_cairn_content.py`, `test_check_release_publication.py`, `test_claim_check_module.py`, `test_core_dev_folders.py`, `test_default_security_stance.py`, `test_doc_governance.py`, `test_finalize_retired_living_state.py`, `test_hardening.py`, `test_link_check_exclusions.py`, `test_loop_fidelity_gate.py`, `test_module_roster.py`, `test_next_session_local_note.py`, `test_onboarding_seed_roster.py`, `test_oracle_activation.py`, `test_portable_security_sweeps.py`, `test_presets.py`, `test_prune_tools.py`, `test_quickstart_sequence.py`, `test_review_and_verification_rules_ship.py`, `test_review_stance_in_shipped_files.py`, `test_scaffold.py`, `test_scientific_check_guidance_ships.py`, `test_scope_reduction_trap.py`, `test_session_start_drain_rules.py`, `test_status_vocabulary_advisory.py`, `test_stewardship_rules_ship.py`, `test_upgrade.py`, `test_upgrade_added_slots.py`, `test_upgrade_lockfile_path_containment.py`, and `test_upgrade_module_additions.py`.

Also pending: the deliberate mutation, `check_cairn.py`, link checks, snippet sync, neutrality gate, and common Boundary B run on a clean final commit under canonical Python 3.13.x. No suite result is asserted here. Status remains `implementing` until the mapped checks and required review sequence permit transition. Elapsed: approximately 4 minutes; tokens: unknown.

## Implementation verification -- Codex (GPT-6) -- 2026-11-01 (completion update)

Changed surfaces remain the six named in the prior record. The completed edits include the light bypass route, the plan-review-when-required label and accessibility text, and the Quickstart correction. No operative rule or review obligation changed.

Boundary A is `wide` because the published lifecycle method is a protected doctrine surface. The prior record names the plan's 32-file mapped selection. `implement_shared` confirmed that all 32 filenames were covered by its 18-file common selection plus the 16-file lifecycle-only remainder, with none omitted. The common selection command was `python tools/test_tiers.py for --range b210f9b4d2e938e33905e8c99faabd7ab7e91148..d7434ba616289d8f1c1927d23784ab1a6b33b876`; it selected 18 files and passed 667 tests in 61.04 seconds under Python 3.12.9 on `d7434ba6`. The selector reported 46 unpinned `AGENTS.md` readers omitted. The 16-file lifecycle-only mapped remainder passed 942 tests in 72.16 seconds under Python 3.12.9 on `a6927476`; the exact test-run shell command was not retained. An earlier attempt at that remainder was interrupted after 669 passes in 9.35 seconds and is not counted as a completed run. No non-pass was reported for the completed runs. The companion decision-options plan records the common selection's filenames; the prior record here retains the 32-file plan selection.

After the conditional SVG-route edit, five corpus-search nodes in `test_review_stance_in_shipped_files.py` passed in 0.44 seconds under Python 3.12.9 on `212cba7a`: `test_every_file_with_a_phrasing_hit_is_exempt_for_a_reason`, `test_no_exemption_is_stale`, `test_removing_an_exemption_is_reported`, `test_a_phrase_inserted_into_a_scanned_copy_is_reported`, and `test_the_walk_reaches_the_roots_it_claims`. These nodes check corpus exemptions and scanning; the diagram itself was checked by render and accessible-text inspection. The SVG comment-only correction (`7f03a402`) and final Quickstart wording correction (`69e0bb5a`) postdate that run and are not claimed as covered by those nodes.

The prose gates passed on the shared corpus: `check_cairn.py` checked 189 Markdown files (95 external links not probed); `link_check.py` checked 189 files (96 external links not probed); neutrality reported zero failures and 43 informational findings. No synced snippet changed, so snippet sync was not applicable. Current `claim_check.py` checks passed for `README.md`, `docs/release-process.md`, `docs/methodology/lifecycle.md`, and `docs/quickstart.md` under Python 3.12.9; `docs/index.html` also passed. `git diff --check` passed for the committed fixes. The SVG was rendered with `rsvg-convert` and visually inspected after its route and conditional-review changes.

The required wrong-plan mutation was performed in a separate archive copy of committed `fb5e37ed`, not in the worktree. I changed the copied README image description to assert “Light is the default and needs a plan.” Comparison detected the contradiction with `AGENTS.md` (“light has no plan even for multi-area or wide implementation”) and the accepted Decision (“light” is the default, one short review, no plan). Result: **DETECTED CONTRADICTION**.

The shared run records describe committed inputs, but do not preserve pre/post `git status` evidence; clean state is therefore not asserted here. The combined mapped iteration results complete the plan's Boundary A selection as confirmed by `implement_shared`; the interrupted attempt is recorded above and not counted. Boundary B remains `wide` and is still owed after code review on a clean final commit under canonical Python 3.13.x. The full-tree certification is also pending its authorized release trigger. Elapsed: approximately 8 minutes; tokens: unknown.

## Code review -- Codex GPT-6.1 Sol -- 2026-11-01

**Verdict**: Accept; no findings remain. Reviewed `55d0034b`, corrections through `69e0bb5a`, and iteration evidence at `364c26c2`.

**Foundations**: Should this happen as framed? Yes: the six descriptions now distinguish the outer lanes from proposal tiers, preserve light's no-plan rule and the heavy triggers, and retain existing obligations. Best alternative: correct only the README and diagram; that leaves release guidance and the published method inconsistent (proposal Alternatives). What would show it wrong? A light proposal routed through a plan, an unconditional plan review, or a weakened heavy trigger would contradict C1 and the operative rules.

**Evidence**: Compared the changes, diagram paths and accessible descriptions with the accepted proposal and plan. My findings on the SVG's unconditional plan and plan review are closed by `a6927476` and `212cba7a`; `7f03a402` aligns the source comment and `69e0bb5a` corrects Quickstart's review condition. The implementation record reports the mapped selection, prose gates, rendered inspection and a detected false-light-plan mutation. It discloses unrecorded clean-state evidence and final edits after the mapped runs; those remain limits for final verification.

**Coverage**: Read the committed six-surface changes, proposal, plan and iteration evidence. Inspected the SVG paths and accessibility text, relying on the author's rendered inspection. Did not rerun tests or the mutation, inspect installed output, or perform the separate Security Review. Wide final verification remains outstanding. No suite run. Elapsed: approximately 7 minutes; tokens: unknown.

## Security code review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commits: 55d0034b, a6927476, 212cba7a, 7f03a402 and 69e0bb5a  
Target: six descriptive surfaces; evidence `364c26c2`, ordinary review `214b49a7`  
Prior finding: Quickstart's unconditional reviewed-plan wording  
**Tier**: Security Review  
**Verdict**: ACCEPT; prior finding closed, no new findings.  
**Elapsed**: approximately 7 minutes across preparation and final review. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The descriptions retain light's no-plan rule, separate outer lanes from proposal tiers and preserve named high-risk and added/widened-boundary heavy triggers. The approved HTML/Quickstart additions remain descriptive. No governing instructions or enforcement changed. -- Six-surface diff, accepted scope and C1.
2. **Best alternative.** Keep the existing diagram with a conditional route and short explanation, as implemented. Removing it loses useful process guidance; adding another classification mechanism is unnecessary. -- SVG paths and labels; accepted proposal, Alternatives.
3. **What would show it wrong?** The diagram sending light through a plan, or Quickstart requiring every plan review. My render of committed `7f03a402` shows the light bypass and conditional review label; metadata and both alternatives agree. `69e0bb5a` closes the Quickstart finding. The author separately records detection of the deliberately false light-needs-plan example. -- Rendered committed SVG, correction diff and completion evidence.

**Bounding**: ACCEPTED — challenged visual routing and conditional-review semantics. Evidence reports the shared 667 and remainder 942 passes under Python 3.12.9 and targeted later checks. Missing pre/post clean-state records, an unretained remainder command and later edits limit that evidence; this review does not certify it as final clean-tree verification.

Coverage: examined accepted scope, committed changes, rendered branch, accessible text, implementation evidence and ordinary review. Did not rerun suites or mutation, test browser themes or certify the tree. The scope allowance is recorded; no further reached fence/deviation appears. Final wide Boundary B on clean canonical-Python bytes remains owed.
