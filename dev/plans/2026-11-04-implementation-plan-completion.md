# Plan: Complete implementation plans without human-run operations

**Source proposal**: `dev/proposals/archive/2026-11-03-codex-implementation-plan-completion.md`
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**In brief**: Let implementation plans finish after agent-owned work is complete while tracking human trust and release operations separately.

## Source proposal

The accepted heavy proposal assigns v0.7 delivery of the completion split to
self-hosted and shipped guidance, while preserving all checks, authority and
release safeguards. Its Decision and appended reviews remain in the archived
source; archiving implementation does not authorize activation or release.

## Scope

Update `AGENTS.md`, `templates/core/AGENTS.md`, `dev/plans/_template.md`,
`templates/core/dev/plans/_template.md`, `templates/core/dev/PLANNING.md`,
and `docs/methodology/plans.md` and `docs/methodology/lifecycle.md`. Adjust
`dev/proposals/_template.md` and `templates/core/dev/proposals/_template.md`
only where needed to prevent human operations being made implementation
acceptance criteria. Use existing standalone board rows for the actual human
operation and its evidence; do not create a release plan, tool or workflow.
No retrospective rewrite of archived work, release ceremony, pin, signing,
publication or push is included.

**Reuse.** No production code is added. Search of `bootstrap/tests` for
installed doctrine and scaffold found `test_review_sweep_ships.py`, whose
`installs` fixture runs `bootstrap/scaffold.py` for each profile and whose
installed and mutation tests provide a test-home pattern. The existing
`test_review_and_verification_rules_ship.py` covers both governing copies;
`test_verification_boundaries.py` guards verification and release separation.
`tools/board.py::_roadmap_waits` reads standalone waits, as established in the
source reviews. Do not duplicate that mechanism.

### Documentation / doctrine surface

Prescription belongs in both governing files and templates, with explanatory
methodology in the two named documents. Coordinate one writer for the shared
template window in batches 4-6 before implementation; this plan does not
claim or expand into the parent work on suite consolidation or onboarding.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align governing, template and methodology guidance; extend existing shipped-doctrine tests. | Both independent plan reviews, their disposition, and template-writer coordination. | The complete split and its installed-output and mutation checks. |
| C2 | Obtain independent ordinary and Security code reviews; address findings, then perform final wide Boundary B. | C1 and its iteration evidence. | Reviewed implementation and recorded final change verification. |

## Acceptance criteria

**C1.** Implementation plans finish only after agent-owned scope, reviews and
applicable checks are complete, with no human-run trust or release operation
as a completion prerequisite. Existing board rows independently name those
operations, owners, evidence and links to implementation; archive is not
permission to activate or release. Decision, scope and unexpected-boundary
stops remain. No agent failure, defect, missing scientific or functional
evidence, or required review is moved to a human row to close work. A reviewed
trust record awaiting a named human baseline operation remains unpassed and
distinct from an unexplained integrity failure, which remains implementation
work. Fixing an issue is not a release.

Fresh installation through `bootstrap/scaffold.py` exposes the required
guidance in each named installed doctrine, plan and roadmap surface. Extend an
existing shipped-doctrine test home: list each required source and installed
surface, then separately delete or insert contrary instruction for each in
isolated copies; each mutation must fail its relevant check against a passing
unmutated control. Keep scope-floor, verification-boundary and release-gate
controls passing. Preserve functional, scientific and security checks.

**C2.** Separate ordinary and Security code reviews by reviewers other than the
implementer assess committed work; required findings and checks are resolved.
Final wide Boundary B covers reviewed fixes on a clean final commit. No real
key, pin or release operation is exercised. Scientific check: N/A; the source
changes no scientific assumption or result.

## Scope delta

**Scope delta**: preserved. The accepted outcomes and human authority remain;
no operation or check is waived.

## Verification

Boundary A: before implementation use `tools/test_tiers.py for <changed
paths>` with the reviewed range for governing text; run its named iteration
tests and applicable claim, link, snippet, content and neutrality prose gates.
Map actual changed paths and readers, including proposal guidance if changed.
Use `bootstrap/tests/test_review_sweep_ships.py` as the existing real-install
and mutation pattern, and inspect its `installs`, installed-output and deletion
test nodes before extending it. `bootstrap/tests/test_verification_boundaries.py`
contains explicit wide-boundary and release-separation guards; retain their
passing controls and identify the actual scope-floor and release-gate nodes
by opening their triggers during implementation. Test negative searches
against a known-positive case. Record each surface and mutation outcome,
including any survivor or omission; text tests do not prove honest conduct.

Boundary C: independent ordinary and Security reviewers read the committed
implementation and iteration evidence and run tight falsification checks,
not a suite. Boundary B follows review and fixes, in `wide` mode, on a clean,
unchanged final commit using `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(3.13.13): the reviewed-range iteration list, mapped integration/workflow
tests, installed-output and mutation checks, and applicable standing gates.
Record SHA and range, clean pre/post state, commands, counts, elapsed time,
tokens or unknown, non-pass dispositions and omissions. A missing required
check keeps the work open. No full-tree certification is authorized here.

## Plan review -- Codex Terra (MEDIUM) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. C1 preserves agent-owned checks and the distinction between an unpassed baseline operation and an unexplained integrity failure; C2 requires separate reviews and final wide verification -- accepted proposal, Alternatives and Decision; plan, C1-C2.
2. **Best alternative.** Continue case-by-case amendments and existing board waits; it avoids doctrine edits but repeats human intervention and leaves adopters without the general rule -- accepted proposal, Alternatives; `tools/board.py::_roadmap_waits`.
3. **What would show it wrong?** A fresh install with contradictory completion guidance that survives a per-surface mutation, or a missing agent check treated as a human wait, would show failure -- plan, C1 and Verification; `bootstrap/tests/test_review_sweep_ships.py::installs`.

Reviewed commit: 26c1133c2a0fbca7836b317ac6e98868a5d8fc95

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: SHIP

The plan names both governing copies, live and shipped templates, the shipped board and methodology; it requires isolated mutations and passing controls, without adding machinery or a release plan. Existing verification-boundary tests include wide and release-separation guards. Scientific evidence required by other work remains required; this change makes no scientific claim.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Coverage**: Committed plan, accepted proposal and Decision, plan template, named methodology and board guidance, and cited test and board triggers. **Not covered**: implementation, actual mutations or test runs, Security Review, scientific runs, release operations and full suite.

## Plan review -- Codex Sol (HIGH) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. C1 retains failed agent-owned checks, missing scientific/functional evidence and reviews as implementation work; a named human baseline operation stays unpassed, and archive grants no activation authority -- plan, C1; accepted Decision `e2aae09f`; Terra classification `9b59ba4e` and author response.
2. **Best alternative.** Extend the existing install-test home and use existing board waits, as planned; a new operational register or release-plan lifecycle adds upkeep without strengthening authority -- plan, Scope and Verification; `bootstrap/tests/test_review_sweep_ships.py::installs`; `templates/core/dev/PLANNING.md`, Waiting on you.
3. **What would show it wrong?** Delete the split or insert human-only completion instructions separately on each listed source/installed surface: a surviving mutation, transferred functional failure or archive-as-release permission would falsify delivery -- plan, C1 and Verification; accepted proposal, S2-S4.

Reviewed commit: 26c1133c2a0fbca7836b317ac6e98868a5d8fc95
Ordinary review read: b0de365c.

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT -- plan only.

The scope names live and shipped governing text, plan templates, roadmap and
methodology, with proposal guidance adjusted where needed. C1 requires a
surface roster, isolated mutations and passing controls. The cited fixture
actually invokes the scaffold CLI and installed-output tests read its files;
this is a viable extension point, not evidence that future checks already pass.
C2 preserves separate ordinary/Security code reviews and final wide Boundary B.
Scope, Decision and unexpected-boundary stops remain; no key, pin, release
operation or added execution machinery is authorized.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed plan, accepted proposal/Decision/classification response,
ordinary review, governing rules, plan template, installed-test fixture and
mutation bodies, scope-floor and verification/release-separation guards.
**Not covered**: implementation, future per-surface mutation outcomes,
scientific execution, cryptographic authentication or ceremonies. No
implementation tests or full suite run; text checks cannot prove honest conduct.

## Response -- Codex LunaLOW -- 2026-11-04

Both required plan reviews are committed with matching Internal and Internal
Security Review obligations and no findings. No operative change is needed;
the accepted scope, evidence requirements and human-authority boundaries remain
as reviewed. The plan advances to `ready-to-implement`.

## Implementation verification -- Codex LunaLOW -- 2026-11-04

**Boundary A**: scoped iteration on the nine source paths in `5820b150`.
Seven source surfaces and all three installed surfaces across the three
shipped profiles were checked: 7 source and 9 installed-output deletion
mutations were caught against passing controls. The real-install criterion
passed for installed `AGENTS.md`, `dev/plans/_template.md` and `dev/PLANNING.md`.

**Tested commit**: `5820b15086056680ba5df024e0b037f68b749358`.
**Reviewed range**: `7f98d9411cc56452867b6d66b1f099fa5edba7cc..5820b15086056680ba5df024e0b037f68b749358`.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13.
**Pre-run state**: clean detached checkout. **Post-run state**: clean; `HEAD` remained the tested commit.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---:|
| `python tools/test_tiers.py for --range 5820b150^..5820b150` with the nine paths below | 0 | 36 files selected; 23 other AGENTS readers omitted by the configured passage guard | 1.1s | unknown |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q` with the 36 selected files below | 0 | 2,261 passed, 1 skipped | 2m21s | unknown |
| `python scripts/claim_check.py` on each changed Markdown file | 0 | All changed Markdown, including this plan and `CHANGELOG.md`, passed | under 1s per file | unknown |
| `git diff --check` | 0 | Clean | under 1s | unknown |
| `python scripts/check_cairn.py` on changed Markdown | 0 | 8 files clean; 3 external links not probed | 0.3s | unknown |
| `python scripts/link_check.py` on changed Markdown | 0 | 8 files clean; 3 external links not probed | 0.2s | unknown |
| `python scripts/sync_doc_snippets.py --check` on changed Markdown | 0 | 8 docs; no drift | 0.1s | unknown |
| `python scripts/quality_gate.py --sub neutrality` | 0 | 0 failures; 43 informational matches | 0.8s | unknown |

**Changed paths**: `AGENTS.md`, `templates/core/AGENTS.md`,
`dev/plans/_template.md`, `templates/core/dev/plans/_template.md`,
`templates/core/dev/PLANNING.md`, `docs/methodology/plans.md`,
`docs/methodology/lifecycle.md`, `bootstrap/tests/test_review_sweep_ships.py`,
`CHANGELOG.md`.

**Selected test files (36)**: `test_board_json_contract.py`,
`test_certifying_run_rule.py`, `test_claim_check_module.py`,
`test_core_dev_folders.py`, `test_documentation_plan_module.py`,
`test_finalize_retired_living_state.py`, `test_hardening.py`,
`test_install_report_slots.py`, `test_install_time_onboarding.py`,
`test_intents_tool.py`, `test_loop_fidelity_gate.py`,
`test_module_merge_lockfile.py`, `test_next_session_local_note.py`,
`test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`,
`test_quickstart_sequence.py`, `test_replacement_tools.py`,
`test_review_and_verification_rules_ship.py`,
`test_review_stance_in_shipped_files.py`, `test_review_sweep_ships.py`,
`test_scaffold.py`, `test_scientific_check_guidance_ships.py`,
`test_scope_reduction_trap.py`, `test_session_routines.py`,
`test_session_start_drain_rules.py`, `test_skills_onboarding.py`,
`test_status_vocabulary_advisory.py`, `test_stewardship_rules_ship.py`,
`test_upgrade.py`, `test_upgrade_edit_check_runs_no_project_programs.py`,
`test_upgrade_lockfile_path_containment.py`, `test_upgrade_module_additions.py`,
`test_verification_boundaries.py`, `test_verify_integrity.py`,
`test_verify_ref.py`, `test_verify_stems.py`.

**Non-pass disposition**: the one skip was
`test_intents_tool.py::test_windows_drive_case_normalization_for_pointer_chain`,
marked Windows-only and inapplicable on this host. Scope-floor,
change-verification and release-separation controls passed: scope floor in
`test_review_and_verification_rules_ship.py::test_light_tier_can_ship_wide_work_without_a_plan`;
release separation in
`test_verification_boundaries.py::test_both_operational_surfaces_separate_change_checks_from_tree_certification`
and `test_installed_operational_rule_is_project_general`; public-path coverage
in `test_verification_boundaries.py::test_change_verification_contract_reaches_every_surface`.
**Known omissions**: ordinary and Security code reviews, final wide Boundary B,
full-tree certification, real trust/release operations and scientific execution
remain outstanding or N/A as scoped. No release permission is inferred.

## Code review -- Codex Terra (MEDIUM) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. The governing, plan and board text keeps agent-owned failures and scientific evidence in implementation while separating human operations and release authority -- `AGENTS.md`; `templates/core/dev/plans/_template.md`; accepted Decision.
2. **Best alternative.** Reuse the existing installation fixture and surface checks, as implemented; a new checker would add machinery without proving human conduct -- `bootstrap/tests/test_review_sweep_ships.py::installs` and `test_installed_plan_completion_and_surface_mutation`.
3. **What would show it wrong?** An installed surface missing the split, a deletion mutant surviving its relevant check, or a failed functional check treated as a human operation would falsify delivery -- C1; `_PLAN_COMPLETION_SURFACES` and the source and installed mutation tests.

Reviewed commit: 5820b15086056680ba5df024e0b037f68b749358
Reviewed range: 7f98d9411cc56452867b6d66b1f099fa5edba7cc..5820b15086056680ba5df024e0b037f68b749358
Iteration record: 8089b1c8; status: 721d67b4.

**Tier**: Internal
**Bounding**: ACCEPTED
**Findings**: one non-blocking evidence correction
**Verdict**: ACCEPT

The iteration record calls `test_light_tier_can_ship_wide_work_without_a_plan` a scope-floor control, but it checks light-tier plan triage. The recorded run also includes `test_scope_reduction_trap.py`, whose governing and plan-template guards check the accepted-scope floor. Correct the attribution in a later evidence record; for release-gate separation, also cite `test_verification_boundaries.py::test_plan_doctrine_binds_record_to_tested_range`, which checks that change verification cannot shorten a release gate.

The tests read real source and installed text and delete a sentence per listed surface against passing controls; their phrase checks cannot prove semantic compliance or honest conduct. Final wide Boundary B and separate Security code review remain owed.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Coverage**: Committed nine-path source diff, accepted proposal, iteration record, mutation and control bodies, scope-floor and release-separation triggers. **Not covered**: independent mutation execution, implementation test reruns, full suite, Security Review, scientific runs or actual release operations.

## Code review -- Codex Sol (HIGH) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. The nine-path diff retains implementation failures and required reviews/checks, keeps reviewed pending baselines unpassed, and denies archive any activation authority -- `AGENTS.md`, Lifecycle; both plan templates, Sequence; accepted Decision/C1-C2.
2. **Best alternative.** Reuse the existing install fixture and scoped guards, as implemented; another operational tool adds burden without authenticating conduct -- `bootstrap/tests/test_review_sweep_ships.py::installs`; source diff, no production-code changes.
3. **What would show it wrong?** Mark a pending human baseline passed in each actual input file: every corresponding check must reject it beside passing controls. All seven source and nine installed-file faults were caught -- `/private/tmp/cairn-sol-completion-code.T5zf9K/probe.py` and `report.json`.

Reviewed commit: 5820b15086056680ba5df024e0b037f68b749358
Reviewed range: 7f98d9411cc56452867b6d66b1f099fa5edba7cc..5820b15086056680ba5df024e0b037f68b749358
Iteration evidence: 8089b1c8; status: 721d67b4; ordinary review: 83ae9556.

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Bounding**: ACCEPTED
**Findings**: none
**Verdict**: SHIP -- reviewed source; final wide Boundary B remains owed.

I derived seven doctrine surfaces from the committed diff and three installed
destinations from the core install registry, then matched the test rosters.
Under Python 3.13.13, 16 control nodes passed. Separate source copies and
fresh scaffold outputs for all three profiles received the contrary
`unpassed`-to-`passed` mutation; all 16 were rejected by the relevant pytest
entry, not merely a helper invocation. No survivor or unmeasured member remains
for this fault.

The additions preserve Decision/scope/boundary stops and scientific, functional
and release obligations; no runtime ceremony or authority changes. Proposal
templates need no operation-related correction in this range. Bohr's
non-blocking evidence-attribution correction remains for author disposition.
No Maintainer fence was reached in the reviewed source range.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Frozen nine-path diff, accepted source/plan, iteration record,
ordinary review, actual-source/emitted-file probes and existing guard bodies.
**Not covered**: arbitrary semantic contradictions, dishonest records,
cryptographic authentication, scientific/native-platform execution or ceremonies.
The 36-file iteration selection and full suite were not replayed; final
integration remains required, including disposition of mapped omissions.


## Implementation verification -- Codex High -- 2026-11-05

**Boundary B**: wide. Luna executed; the parent joined the evidence and
independently checked both JUnit reports. Tested clean Git-backed commit
`573da3f439c133deb55c17da0fd3f7bd519c517a`, Python 3.13.13 / pytest 9.0.3;
pre/post state and HEAD unchanged. Source/test/tier-map bytes equal `7d675b81`.

Selection is the six source-pair union in plan 5's Boundary A packet, plus
`5820b150^..5820b150`, including every changed path and changelog. The current
selector gave 40 bootstrap files, including 17 integration/workflow consumers,
plus the two examples. No parallel 2a/8a source range was added. The 13 additions
to A's 27 bootstrap files are finalize-retired-living-state, hardening,
install-time-onboarding, intents-tool, module-merge-lockfile, next-session-local-note,
onboarding-slot-substitution, session-start-drain-rules, skills-onboarding,
upgrade-edit-check-runs-no-project-programs, upgrade-lockfile-path-containment,
verify-integrity and verify-stems (their existing `test_*.py` files).

| Command / Scope | Outcome | Session Time |
|---|---|---:|
| Canonical Python `-m pytest --junitxml=/private/tmp/cairn-wide-b-final-573da3f4-bootstrap.xml`, the 40-file union above | 2,462 passed, 1 Windows-only skip; no failures/errors | 154.592 s |
| Same command with `--junitxml=/private/tmp/cairn-wide-b-final-573da3f4-examples.xml`, both `examples/*/test_*.py` files named in A | 9 passed | 0.028 s |
| Claim/link/content/snippet checks over the 15 changed Markdown files plus F5-1 response; neutrality, redundancy and seven source-pair diff checks | Passed; 3 external URLs unprobed | 2.24 s summed |

JUnit identities are disjoint: **2,471 passed, 1 skipped, 2,472 unique**.
The skip is `test_intents_tool::test_windows_drive_case_normalization_for_pointer_chain`.
It was one of 13 native Windows cases passing at `64aac860`; the archived
shared-claims plan records that run. The covered test/helper definitions and
loaded shared-module bytes are unchanged. This reuses that limited evidence,
not a fresh Windows run or an added B count.

Twenty-one guarded readers remain outside the union: agreement-retired,
check-cairn-content, comprehension-floor, doc-drift-tools, fork-advisory,
gate-manifest, gate-preflight, generated-output-scan, link-check-exclusions,
lockfile-module, module-merge, notice-install, oracle, quality-gate-neutrality,
scaffold-substrate, security-leaf, security-verification, slotmerge-leaf,
test-tiers, upgrade-refuses-hostile-project-data and writing-rules-ship
(existing underscored test filenames). No full-tree certification ran.

Citation correction: scope-floor evidence is
`test_scope_reduction_trap.py::test_scope_reduction_obligation_present`;
the light-tier node is triage only. Release preservation is
`test_verification_boundaries.py::test_plan_doctrine_binds_record_to_tested_range`.
Five families remain over 10 s, already on 2a's ranking: upgrade 29.08,
upgrade-edit-check 25.68, security-stack 24.63, upgrade-module-additions 23.50,
intents-tool 11.05 s. No timing target waived a check.

Plans 4 and 6 have both code passes accepted and no remaining implementation
criterion. Plan 5's two reviews retain F5-1; this run cannot clear it.
**Elapsed**: session/gate times above; end-to-end wall time unknown.
**Tokens**: unknown. Omissions: guarded readers, external probes, current
native Windows execution, full certification and human trust/release operations.
