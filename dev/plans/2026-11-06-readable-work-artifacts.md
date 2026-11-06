# Plan: Readable work artifacts that finish well

**Source proposal**: dev/proposals/archive/2026-11-04-codex-readable-plans-and-finish-work.md
**Author**: Codex GPT-6.1 Terra (Medium)
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Make work summaries clear, plans executable and small follow-ups and completion records timely.

## Source proposal

The primary source is `dev/proposals/archive/2026-11-04-codex-readable-plans-and-finish-work.md`;
the second source is `dev/proposals/archive/2026-11-06-codex-concrete-delivery-summaries.md`.
Delegated Decisions `27300e1e` and `6801982a` accept all five readable-work
outcomes and three summary types. This plan delivers them together in local and
shipped guidance. Decision `1952b092` opens this one coordinated plan. The
supplemental disposition `34ed2712` allows the five-outcome bundle despite an
unmet doctrine-evolution evidence prerequisite; it does not call the gate passed
or classify an incident as high-risk. The summary request is design, not an
invented incident remedy.

## Scope

Change local/shipped `AGENTS.md`, `dev/agent_collaboration.md`, and proposal,
plan and strategy templates; reconcile relevant methodology and manual
session-end skill guidance. Preserve historical records. No runtime Meter,
session, helper or Safe-Git safety changes. Keep existing review caps, three
Foundations questions, model and authority floors, verification and word targets
and clarity exceptions. The summaries are reading aids, not a second authority.

**Reuse.** Existing templates already have word targets, board `In brief`,
proposal Decision summary, review Foundations and plan deferral homes. Searches
of those templates and `tools/test_tiers.py for` found existing writing,
review/verification, scope-reduction, scaffold and install test owners. Reuse
those, the actual scaffold entry point and current shared-file serialization;
no new runner, evidence ledger, scoring field or fourth formal review question.

### Documentation / doctrine surface

Put cross-cutting prescription in AGENTS and its shipped twin, review guidance
in collaboration twins, artifact-specific prompts in the six templates,
and software/methodology descriptions in their existing homes. Manual
session-end guidance checks omissions rather than reconstructing entries.

## Sequence

All existing templates and scaffold capabilities are available; no unfinished
plan or human release operation gates completion. Estimate 2–4 workdays for
implementation, independent examples, both code reviews and wide verification;
reader/pin mapping, installed mutations and shared-file coordination may extend
this. The doctrine exception below applies only to this accepted bundle.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Map current wording, twins, readers, byte pins and existing owners; implement the five specific writing/finish duties | Usual and Security plan reviews before Low execution | Consistent local/shipped instructions and executable plan/review guidance |
| C2 | Update the six summary templates and copy rules | C1; serialize shared templates | Proposal deliverables, plan Build summary and exploratory strategy Summary |
| C3 | Run fresh-install, reading and contrary-wording evidence; obtain both code reviews and run final wide Boundary B | C1–C2; review reads iteration evidence | Verified guidance, issue closure at fixing commit and completion records |

## Acceptance criteria

**C1.** At finishing commit or archive, applicable roadmap/changelog entries are
updated under existing shared-file ownership; session-end checks omissions.
Reviewers read proposal title, one-line and Decision summaries before body/code,
state a one- or two-sentence gist and report dependence on the body as a
finding; authors reread the top after every revision. When shortening, cut
repeatable detail before explanation and shorten the Decision summary last;
modest clarity-preserving overruns remain permitted. Within the existing three
review questions, plan review identifies missing design for each assigned-tier
chunk and returns it to its author, rather than assigning a stronger implementer.

Near chunks and code-review response, define cheap as a few person-steps, no
new Decision or public name beyond the plan, and a test in existing test files.
Review identifies cheap findings/advice; the response fixes each before archive
or uses an existing deferral reason with verbatim Maintainer authorization.
Cheapness grants no scope, boundary or check waiver; non-cheap advice retains
its existing disposition. Preserve the narrower defect-fix rule and bounded
retry/model floors. Required failed checks stay implementation work.

**C2.** Proposal Decision summaries name material added, changed or removed
outputs with problem and costs; documentation-only work invents no tool. Plan
copy instructions include `## Build summary` after its header; it states the
accepted result and outputs without duplicating Scope. Strategy templates
suggest `## Summary` after the header, identifying question, recommendation and
possible outputs without portraying exploration as accepted. Preserve one-line
board fields, budgets, authority and prospective application; correct conflicts
with operative scope instead of creating a second contract.

**C3.** Fresh actual scaffold installation shows all required local/shipped
instructions without contrary wording. Separately remove or reverse each new
obligation in isolated copies and demonstrate the relevant behavior or existing
assertion fails; positive controls establish the check can detect each fault.
An independent reader states a cold top-first gist, checks top preservation
after revision, identifies material outputs in proposal, plan and strategy
examples, recognizes a documentation-only change and detects a strategy
recommendation falsely presented as accepted. Test an underspecified assigned-tier
chunk and cheap in-scope, out-of-scope and failed-check deferral cases. Close
issues #46–#50 at the fixing commit after their checks, not at release; record
closure evidence. Existing completion scope-floor, verification-boundary and
release-gate controls must still pass, even when the changed-file selector
does not choose them. Both code reviews and all mapped checks remain required.

## Scope delta

**Scope delta**: degraded assurance -- delegated Sol disposition `34ed2712`
quotes the Maintainer's temporary authority and allows this one bundle “despite
the unmet doctrine-rate-limit evidence prerequisite.” Recurrence in a pinned
tracker window or genuine routine-close synthesis is unestablished. #50 reports two plans; #47/#48 may be one
episode, #46 is one report and #49 has no occurrence count. Existing targets,
deferral and shared-record rules supply partial standing duties, not proof of
the missing gate. No outcome or technical check is removed; normal gate applies
to widened scope and later doctrine bundles. No high-risk incident bypass,
new tracker, special human trial or standing exception is claimed.

## Verification

Boundary A: map concrete changed instructions, local/shipped readers and byte
pins with `python tools/test_tiers.py for <paths>` (use `--range BASE..HEAD`
for AGENTS) and run selected tests plus claim, link, snippet and neutrality
gates. Existing candidate owners include writing and review/verification
contract tests, `test_scope_reduction_trap.py`, `test_review_stance_in_shipped_files.py`,
`test_scaffold.py` and install/upgrade tests; map final paths and add controls to
existing homes only for uncovered faults. Independently of selector output,
map and run the applicable existing completion scope-floor, verification-boundary
and release-gate controls. Current starting nodes are
`bootstrap/tests/test_scope_reduction_trap.py::test_scope_reduction_obligation_present`,
`bootstrap/tests/contract/test_verification_boundaries.py::test_change_verification_contract_reaches_every_surface`,
`bootstrap/tests/contract/test_verification_boundaries.py::test_plan_doctrine_binds_record_to_tested_range`,
and `bootstrap/tests/test_review_sweep_ships.py::test_source_plan_completion_rule_and_surface_mutation`
and `test_installed_plan_completion_and_surface_mutation`; map their applicable
parameter cases and other release-gate controls to final changes. Use a disposable fresh scaffold and
actual emitted instructions. In separate copies mutate each obligation and run
its real entry-point or behavioral control, including independent reading
examples; report omissions and uncertainty concisely without an evidence folder.

Boundary C is independent code falsification, with a separate Security Review;
review reads iteration evidence and fixes precede final integration. Boundary B
is wide on the clean final reviewed commit under canonical Python 3.13.x:
selected iteration and integration/workflow tests, the applicable preserved
completion and release-gate controls, installed output, accepted mutation/example
controls and standing gates. Record SHA/range, interpreter,
clean pre/post state, commands/counts, elapsed, non-pass dispositions,
omissions and one evidence-qualified benefit-versus-effort sentence. Tree
certification and human trust/release operations remain separate.

## Plan review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

Reviewed commit: 4595db7e

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** The plan covers the five duties and three summary types while retaining both reviews and authority, but omits an explicit accepted check (finding below) -- C1–C3; source proposals' Evidence / verification plans.
2. **Best alternative.** Keep the combined chunks and add the existing completion controls to verification; splitting the work repeats template coordination without removing the shared verification dependency -- Sequence; readable-plans Evidence / verification plan; completion proposal Evidence / verification plan.
3. **What would show it wrong?** An installed contrary instruction, a mutation that survives, a reader missing the examples' meaning, or a failed completion safeguard would falsify delivery; run C3 and the completion controls on the final change -- C3 and Verification; completion proposal Evidence / verification plan.

**Verdict**: REVISE before implementation.

**Finding -- accepted completion controls.** The readable-plans proposal expressly requires preserving the completion proposal's controls. That proposal names existing scope-floor, verification-boundary and release-gate controls that must still pass. The plan requires mapped checks and new-obligation mutations, but does not identify these preserved controls; selection by changed-file names alone does not establish they all run. Name and require the applicable existing controls in verification, with their concrete nodes identified during mapping. This closes an accepted required-check omission, not a change to the Decision.

**Finding -- board source join.** The header joins two source paths with a semicolon, but `tools/board.py` treats the entire field as one path and requires an exact source match. The plan therefore cannot resolve its source for the board next-step calculation. Use one actual primary path in the header and retain both sources in the Source proposal section; confirm the existing board join recognizes it without changing the parser.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Read the committed plan, both accepted source proposals and the completion proposal's evidence requirements. Assessed chunk duties, assigned-tier specificity, independent completion, evidence, authority and budgets. Did not run checks or examine installed output, individual test nodes, implementation, Security Review or release operations.


## Plan review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

Reviewed commit: 5365d97e3f0cdce6261a5a6721b6dc1fd5eb6857

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** The plan delivers all five accepted duties and three summary types, but must explicitly retain the completion safeguards below -- C1–C3; Decisions `27300e1e`, `6801982a`; readable-plans Evidence / verification plan.
2. **Best alternative.** Keep the combined template window and existing controls; a new runner adds upkeep without establishing comprehension or authority -- Scope / Reuse; Sequence; completion proposal Evidence / verification plan.
3. **What would show it wrong?** Test installed contrary wording, an out-of-scope cheap suggestion, a failed check transferred to a wait, and strategy exploration presented as approval; any surviving bypass falsifies delivery -- C3; both source proposals' Security preflights S2–S4.

**Verdict**: REVISE before implementation.

**Finding -- completion safeguards (blocking; same omission as ordinary review).** The readable-plans proposal preserves the completion proposal's required scope-floor, verification-boundary and release-gate controls. Verification lists candidate owners but does not require that preserved set. Require those controls explicitly and resolve their current nodes during mapping. Existing triggers include `bootstrap/tests/test_scope_reduction_trap.py::test_scope_reduction_obligation_present` and `bootstrap/tests/contract/test_verification_boundaries.py::test_change_verification_contract_reaches_every_surface` / `test_plan_doctrine_binds_record_to_tested_range`; their bodies enforce scope authority, coverage and release separation. Selection by filenames alone is insufficient.

C1 preserves the narrower defect-fix exception, bounded retries, model floors and failed-check ownership. Scope treats summaries as reading aids. The one-bundle exception remains an unmet prerequisite disposition, with no high-risk classification, publication authority or technical-check waiver; widened scope revives the normal gate. Installed and independent-reader evidence remains owed, not measured.

**Elapsed**: approximately 8 minutes. **Tokens**: unknown.

**Coverage**: Read committed plan/template, review stance, accepted sources/Decisions, supplemental and scheduling dispositions, completion record, and cited control bodies. Not covered: implementation, actual installed output, reader/mutation execution, private inputs, trust/release operations or suites. No checks were replayed.

## Plan review response -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

- **Completion safeguards (both reviews):** C3 and Verification now require
  applicable scope-floor, verification-boundary and release-gate controls even
  outside the selector, with current starting nodes and final mapping.
- **Board source join:** The header now names one real primary source; Source
  proposal names both accepted inputs and retains both scopes.

No criterion or check is waived; the degraded-assurance disposition and both
review records remain intact. **Elapsed**: approximately 3 minutes. **Tokens**:
unknown.

## Implementation verification -- Codex GPT-6 Luna (Low) -- 2026-11-06

**Source:** `290bd5d49f89ffb55b330e033232455b22046b71` (implementation
snapshot; changes since `69869b8c` are the 17 instruction/test paths listed in
the committed source diff, plus this record). Python: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13).

**Boundary A mapping:** `python tools/test_tiers.py for --range
69869b8c..290bd5d4` over the 17 changed instruction/test paths selected 36
files: `bootstrap/tests/contract/{test_certifying_run_rule.py,
test_review_and_verification_rules_ship.py,
test_scientific_check_guidance_ships.py,test_stewardship_rules_ship.py,
test_verification_boundaries.py,test_writing_rules_ship.py}` and
`bootstrap/tests/{test_agreement_retired.py,test_board_json_contract.py,
test_claim_check_module.py,test_core_dev_folders.py,
test_documentation_plan_module.py,test_engine_copy_fallback_contained.py,
test_incident_trackers_module.py,test_install_report_slots.py,
test_install_time_onboarding.py,test_next_session_local_note.py,
test_quickstart_sequence.py,test_replacement_tools.py,
test_review_stance_in_shipped_files.py,test_review_sweep_ships.py,
test_scaffold.py,test_scope_reduction_trap.py,test_security_stack.py,
test_session_routines.py,test_session_start_drain_rules.py,
test_session_writes_contained.py,test_skill_contract.py,test_skills_fanout.py,
test_skills_install.py,test_skills_matrix.py,test_skills_security.py,
test_skills_self_heal.py,test_skills_upgrade.py,
test_status_vocabulary_advisory.py,test_upgrade.py,
test_upgrade_lockfile_path_containment.py}`. The selector omitted 26 other
AGENTS readers above its guard: `test_comprehension_floor.py`,
`test_model_tier_rule_ships.py`, `test_test_tiers.py`,
`test_link_check_exclusions.py`, `test_check_cairn_content.py`,
`test_doc_drift_tools.py`, `test_fork_advisory.py`, `test_gate_manifest.py`,
`test_gate_preflight.py`, `test_generated_output_scan.py`,
`test_hardening.py`, `test_lockfile_module.py`, `test_loop_fidelity_gate.py`,
`test_module_merge.py`, `test_module_merge_lockfile.py`,
`test_notice_install.py`, `test_oracle.py`,
`test_quality_gate_neutrality.py`, `test_scaffold_substrate.py`,
`test_security_leaf.py`, `test_security_verification.py`,
`test_slotmerge_leaf.py`,
`test_upgrade_edit_check_runs_no_project_programs.py`,
`test_upgrade_module_additions.py`,
`test_upgrade_refuses_hostile_project_data.py`, and `test_verify_integrity.py`.
These are the 26 additional AGENTS.md readers omitted by the selector guard,
not a claim that all other ordinary tests are omitted; only independently
selected SG-map members join final-source A, while other coverage remains due
at its existing release trigger. A machine-readable frozen map is at
`/private/tmp/cairn-readable-final-map.json`.

**Focused evidence:** On a disposable clone at this SHA, the two mapped
writing/review files ran 396 cases, all passed (4.61s), including per-clause
mutations and installed-copy checks. The separately selected completion
controls ran 120 cases, all passed (0.89s):
`test_scope_reduction_trap.py::test_scope_reduction_obligation_present`,
`test_verification_boundaries.py::{test_change_verification_contract_reaches_every_surface,test_plan_doctrine_binds_record_to_tested_range}`,
and `test_review_sweep_ships.py::{test_source_plan_completion_rule_and_surface_mutation,test_installed_plan_completion_and_surface_mutation}`.
The clone's Git binding was verified as the canonical interpreter and its
tracked tree was clean before and after these runs. A separate empty adopter
repo received a fresh 49-file Solo Greenfield scaffold from this commit;
installed AGENTS, collaboration, proposal/plan/strategy templates and session
skill contained the updated rules and summaries, while the local two-retry
budget remained absent. Its installed Git binding named the canonical Python.

`sync_doc_snippets.py --check` over the 15 changed documentation files passed.
`quality_gate.py --sub neutrality --sub redundancy` passed (zero failures).
`check_cairn.py --no-content-scan` found two unresolved test-file references
in unchanged documents (the code-map test and test-tier test) and unused
allowlist entries; this gate therefore remains a recorded non-pass, not a
waiver. The claim checker passed for the changed documents before
implementation commits.

**Earlier broad attempt and disposition:** At `9178bf57`, a clean-copy mapped
run reported 2,153 passed, 3 failed and 46 setup errors (126.46s). The three
failures were `test_session_writes_contained.py::test_a_cloned_vendor_table_cannot_replace_the_users_virtual_environment`,
`test_skills_security.py::test_git_stream_normalizes_crlf_pairs_but_escapes_lone_cr`,
and `test_skills_security.py::test_failed_git_call_reports_plain_text`; the 46
errors came from the template runner resolving its source helper under the
wrong directory. The setup issue was fixed at `5b4516ef`; SG reports the three
nodes passed there and 142 passed / 1 failed in the related selected run, whose
only failure was an obsolete helper-substitution assertion. Its replacement
control passed 1/1 at `40a868ee`. These are SG-owned runtime/test changes, not
claimed as this source's broad pass. The 26 omitted readers and joined final
source still require the planned selection.

**Still open:** final joined-source Boundary A, cold-reader C3 on the neutral
examples, ordinary code review, separate Security Review, and post-review
wide Boundary B. The neutral input packet and separate expected-classification
key are at `/private/tmp/cairn-readable-reader-packet.md` and
`/private/tmp/cairn-readable-reader-key.md`; only the packet is for the reader.
No review clearance, release operation, certification or plan completion is
claimed. Measured benefit: the fresh install and 396 focused cases show the
local and shipped instructions agree on the checked paths; the omitted readers,
open reviews and final integration remain continuing assurance work. Elapsed
time and token use: unknown.

**Scoped prose and reader follow-up (2026-11-06):** On clean committed copy
`30ba3e86dd45e834fbafb2df20516d148d7dae66`, content-enabled
`check_cairn.py` passed all 16 Markdown files (the 15 changed documents and
this plan); snippet sync passed all 16; plan `claim_check` passed; neutrality
and redundancy passed with zero failures. This is the required scoped prose
gate result. A separate global no-content scan had reported four unused
allowlist entries and two stale test paths in unchanged files; those remain an
outside-scope global non-pass, and no exemptions or historical-record edits
were made.

Cold reader record `7630ec0a` reports all ten neutral examples matched the
separate expected classifications, with no concrete correction. This is
independent agent evidence only, not a human usability trial. The 26 selector
omissions above are specifically AGENTS.md readers omitted by the selector's
guard, not a claim that every other ordinary test is omitted. Only members
independently selected by the joined SG map join final-source A; other checks
remain due at their existing release trigger. The machine-readable frozen map
at `/private/tmp/cairn-readable-final-map.json` records source/tree and changed
file hashes, selected files, those 26 reader omissions, the five completion
nodes (120 cases), and scoped prose-gate source/results. Joined final-source A,
code review, Security Review and final wide Boundary B remain open; plan status
stays `implementing`.

## Independent reading record -- gpt-6.1-terra -- 2026-11-06

**Scope and source:** C3 cold reading of the ten neutral cases in
`/private/tmp/cairn-readable-reader-packet.md`, before consulting its separate
expected-reading key. Original answers were saved unchanged at
`/private/tmp/cairn-readable-cold-terra-20261106.txt`. This is agent reading
evidence, not a lifecycle review or evidence of human usability.

**Outcome:** All ten answers matched the key's intended classifications:
manual command versus guide-only outputs, removal after revision, plan summary,
missing Low-tier design, exploratory versus unsupported approval, in-scope
cheap follow-up versus new scope, and a failed required check. In case 4 I
noted that the excerpt does not specify the command name, format, response
categories or detailed tests; that observation does not establish that design
is missing elsewhere. No material misunderstanding or correction emerged from
the comparison. This packet is synthetic and does not establish how readers
understand the actual changed artifacts. Elapsed time and token use: unknown.
