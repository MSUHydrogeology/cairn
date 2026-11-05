# Plan: Security Review pass limit

**Source proposal**: dev/proposals/archive/2026-11-02-codex-security-review-pass-limit.md
**Status**: revising-code
**Waiting on Maintainer**: C2 human trial or explicit deviation
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**Author**: CodexTerra (gpt-6.1-terra), ordinary plan author
**In brief**: Keep the normal Security Review limit while allowing a specifically authorized further pass.

## Source proposal

The accepted heavy proposal retains the normal two-pass limit and named
disposition at the cap, with a Maintainer-authorized exception for each
further scoped pass. Neither an exception nor an ordinary review clears a
Security obligation, finding, criterion or check.

## Scope

Align the cap in `AGENTS.md`, `templates/core/AGENTS.md`, both proposal
templates, `dev/modules/security-review.md`, its shipped counterpart, and
`docs/methodology/dual-review.md`; map other applicable readers and pins
before editing. Keep existing triggers and verification selections. Shared
core guidance for sequence items 4-6 has one writer, Herschel; coordinate a
combined editing and verification window without changing plan 4.

**Reuse**: N/A: no code added. The existing stage record carries the reason,
scope and authorization; no new form or authorization mechanism.

### Documentation / doctrine surface

Prescription belongs in governing and shipped instructions; the published
methodology explains the same contract. Existing tests guard shipped text.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Map cap statements, readers and pins; align guidance and focused guards. | Both independent plan reviews and their dispositions; coordinate shared writer. | Consistent instructions and affected tests. |
| C2 | Exercise worked cases and affected checks; obtain ordinary and Security code reviews, then wide Boundary B. | C1 | Recorded change evidence. |

## Acceptance criteria

**C1.** Two passes remain normal at each stage; unresolved blockers or unmet
criteria/checks receive named disposition at the cap. Each further pass needs
a specific unresolved security question or newly changed material, why prior
passes and evidence cannot resolve it, its expected value, and a Maintainer
authorization for the named artifact and scope. Each further pass needs its
own reason and authorization. Agents have no scheduling or clearance authority;
no routine Security necessity explanation is added. Triggers, usual review and
verification remain unchanged. Enumerate applicable statements and readers,
including positive search controls and byte pins; align them without weakening
existing obligations.

**C2.** Human-applied examples show a closed second pass advances and an
unresolved question gets a further scoped pass only after authorization.
Reject missing reason or authorization, reusable authorization, automatic
passes and treating a pass as clearance. The existing stage record and
Maintainer decision own this check; text tests cannot establish authorization
or sound judgment. Ordinary and Security code reviews are independent.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: map `python tools/test_tiers.py for <changed paths>`, readers and
pins, run the selected tests and standing claim, link, snippet, neutrality and
redundancy gates. Inspect actual test triggers; add focused coverage only for
an uncovered plausible fault. Search controls must find a known cap statement.
Boundary C: independent reviewers falsify the contract with targeted checks.
Boundary B: wide, after both code reviews, on a clean final commit under
canonical Python 3.13; include the reviewed-range iteration selection,
applicable integration/workflow consumers and standing gates. Record SHA,
range, interpreter, clean pre/post state, commands, counts, elapsed time,
non-passes and omissions. No full certification is implied.

## Plan review -- Codex Terra (MEDIUM) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. C1 keeps the normal cap and named disposition while requiring a specific reason and Maintainer authorization for each scoped exception -- accepted proposal, Proposal and Decision; plan, C1.
2. **Best alternative.** Reuse the existing stage record and human decision, as planned; a new authorization tool would add burden without establishing sound judgment -- accepted proposal, S1-S5; plan, Reuse and C2.
3. **What would show it wrong?** A worked case that permits a reusable authorization or treats an extra pass as clearance would falsify the change -- plan, C2; `docs/methodology/dual-review.md`, Caps and closure.

Reviewed commit: 7e439763b266170100cc7b63131f91e9f7c246e5

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: SHIP

The plan maps live and shipped cap statements, retains review triggers and checks, and requires independent code reviews followed by wide Boundary B. Its examples test human application, not the truth of authorization through text matching.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

**Coverage**: Committed plan, accepted proposal and Decision, plan template, governing and shipped cap statements, Security Review modules and methodology. **Not covered**: all readers and pins, future examples or implementation, Security Review, tests and full suite.

## Plan review -- Codex Sol (HIGH) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. C1 retains the normal two-pass cap, named disposition and separate checks while requiring a reason, expected value and named Maintainer authorization for every further scoped pass -- accepted proposal, Proposal/Decision; plan, C1-C2.
2. **Best alternative.** Keep reasons and authorization in existing stage records, as planned. An absolute cap is cheaper but loses the accepted targeted exception; a new register or parser adds upkeep without proving authorization -- accepted proposal, Alternatives/S1-S5; plan, Reuse.
3. **What would show it wrong?** Human-applied examples must reject an unapproved or reusable exception and any claimed clearance, while closed second-pass work advances without another read -- plan, C2; `docs/methodology/dual-review.md`, Caps and closure.

Reviewed commit: 7e439763b266170100cc7b63131f91e9f7c246e5
Ordinary review read: 3781123b.

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT -- plan only.

An exception commissions one read; it grants no scope concession, waived check
or automatic closure. Each later pass needs fresh authorization for its own
artifact/scope. Ordinary review and Security triggers remain independent;
routine invocation acquires no new permission or necessity-explanation ritual.

The existing `test_review_stance_in_shipped_files.py` obligation checks protect
separate usual/Security passes and matching plan obligations; they do not
establish the truth or merit of an exception. C1's cap-reader/pin inventory and
C2's human-applied negative examples therefore remain necessary implementation
evidence. The shipped module already states the cap while the self-hosted copy
lacks that paragraph; the named alignment scope can resolve this drift.

Shared-writer coordination changes editing ownership, not review independence.
Wide Boundary B follows both code reviews; no release/security ceremony is
shortened or authorized by this pass.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed plan, ordinary review, accepted source/reviews/response/
Decision, current review template, governing/module cap statements and actual
text-guard bodies. **Not covered**: exhaustive reader/pin mapping, future worked
cases, implementation or authorization authenticity. No implementation tests,
suite or ceremony run; misleading reasons and mistaken human judgment remain possible.

## Author response -- Codex LunaLOW -- 2026-11-04

No findings. Both required plan-review obligations match and accept the plan.
The nonblocking human-application cases remain in C2: a closed second pass
advances, while each further scoped pass needs its own reason and Maintainer
authorization; missing or reusable authorization and automatic clearance do
not qualify. No operative change is needed.

**Status**: ready-to-implement. Implementation follows after this transition.


## Implementation log -- Codex (High) -- 2026-11-05

Source: `b30adff0`; current guidance at `7d675b81`. Herschel's Low attempt
and Sagan's Medium retry handed execution to the parent High implementation
agent after failed checks; no reviewer authored the repair.

The current-rule search used `two.pass|two .*pass|at most two|Security
Review.*passes|further pass` across governing, shipped, module and methodology
prose. Known-positive AGENTS and Security-module statements matched. The eight
operative carriers are the two AGENTS files, two proposal templates, two
Security modules, `docs/methodology/dual-review.md` and
`docs/methodology/plans.md`; `_SECURITY_CAP_FILES` enumerates the same set.
Historical records and ordinary-plus-Security obligations are not new cap
statements. The owning guard checks intact text and an expected-value deletion
in each carrier; this checks delivery, not authority or judgment.

C2 manual rule application by Codex High, using hypothetical human record
review, not fabricated authorizations or actual extra passes:

- A closed second pass with no unmet check advances without a clearing read.
- A named new security question, explanation of inadequate prior evidence,
  expected value, artifact and scope still cannot commission a pass without
  the Maintainer's authorization. Adding an explicit authorization for that
  one hypothetical pass permits only that read.
- Removing the reason or authorization rejects the extra pass; the normal cap
  and named disposition remain.
- Reusing that authorization for a later pass, an automatic third pass, or
  calling the read itself clearance is rejected. Unmet checks remain unmet.

These cases simulate the decision rule; they do not test an actual person's
judgment or establish the truth of a future authorization. The ordinary and
Security code reviewers must challenge this evidence. Final Boundary A and
both code passes remain owed; no green union or Boundary B is claimed here.

**Elapsed**: approximately 5 minutes including inventory/application.
**Tokens**: unknown.

## Implementation verification -- Codex Luna (Implementation verification executor, LOW) -- 2026-11-05

**Boundary A**: passed on the final implementation commit in a clean, Git-backed clone. This is scoped change evidence, not a whole-tree certification. The C2 worked cases above are hypothetical human-rule applications, not actual authorizations, extra reviews, or proof of human judgment. The ordinary and Security code reviews remain owed.

**Tested commit**: `7d675b815954ec2fe2c6e88184e51321d4da53d6`.
**Reviewed source pairs**: `b30adff030d24101c703fed0f35f059de21a29fb^..b30adff030d24101c703fed0f35f059de21a29fb`; `bef11a3fe4f0da7145fbb910b68e2dc5d13730b0^..bef11a3fe4f0da7145fbb910b68e2dc5d13730b0`; `6b1785d34086abfbab21005b4589a977f660d367^..6b1785d34086abfbab21005b4589a977f660d367`; `05f4659f49fcf777aae2f4426b4e5e96c9e36bc1^..05f4659f49fcf777aae2f4426b4e5e96c9e36bc1`; `7d675b815954ec2fe2c6e88184e51321d4da53d6^..7d675b815954ec2fe2c6e88184e51321d4da53d6`; and `212be448c34c2ae9e0b36f879d644de40a8d23ef^..212be448c34c2ae9e0b36f879d644de40a8d23ef`. Each selector input was the complete changed-path list for that pair, including `CHANGELOG.md`; no changed path was excluded.

Pair path inventory, in the same order:

- `b30adff0`: `AGENTS.md`; `CHANGELOG.md`; `bootstrap/tests/test_practice_modules.py`; `bootstrap/tests/test_review_stance_in_shipped_files.py`; `bootstrap/tests/test_scaffold.py`; `bootstrap/tests/test_verification_boundaries.py`; `dev/modules/security-review.md`; `dev/modules/testing-discipline.md`; `dev/plans/_template.md`; `dev/proposals/_template.md`; `docs/methodology/dual-review.md`; `docs/methodology/plans.md`; `templates/core/AGENTS.md`; `templates/core/dev/plans/_template.md`; `templates/core/dev/proposals/_template.md`; `templates/modules/team-gated/security-review.md`; `templates/modules/team-gated/testing-discipline.md`.
- `bef11a3f`: `CHANGELOG.md`; `bootstrap/tests/test_practice_modules.py`; `bootstrap/tests/test_review_stance_in_shipped_files.py`; `bootstrap/tests/test_scaffold.py`; `bootstrap/tests/test_verification_boundaries.py`; `dev/modules/testing-discipline.md`; `dev/plans/_template.md`; `templates/core/dev/plans/_template.md`; `templates/modules/team-gated/testing-discipline.md`.
- `6b1785d3`: `CHANGELOG.md`; `bootstrap/tests/test_practice_modules.py`.
- `05f4659f`: `CHANGELOG.md`; `dev/modules/testing-discipline.md`.
- `7d675b81`: `CHANGELOG.md`; `dev/modules/testing-discipline.md`; `templates/modules/team-gated/testing-discipline.md`.
- `212be448`: `CHANGELOG.md`; `examples/scientific-minimal/test_water_budget.py`.

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13, pytest 9.0.3. **Pre-run state** and **Post-run state**: clean detached clone at the tested SHA; no tracked or untracked working-tree changes. Reports are outside the clone.

The selector used `tools.test_tiers.tests_for_paths` separately for each source pair, with that pair's complete paths and `reviewed_range=BASE..HEAD`. Results were 27, 22, 7, 8, 8 and 6 selected bootstrap test files respectively; the union is 27 files. The b30adff0 AGENTS guard omitted 28 readers; every other pair omitted none. The final selected union was `bootstrap/tests/test_board_json_contract.py`, `test_certifying_run_rule.py`, `test_claim_check_module.py`, `test_core_dev_folders.py`, `test_documentation_plan_module.py`, `test_install_report_slots.py`, `test_loop_fidelity_gate.py`, `test_model_tier_rule_ships.py`, `test_onboarding_seed_roster.py`, `test_practice_modules.py`, `test_presets.py`, `test_quickstart_sequence.py`, `test_replacement_tools.py`, `test_review_and_verification_rules_ship.py`, `test_review_stance_in_shipped_files.py`, `test_review_sweep_ships.py`, `test_scaffold.py`, `test_scientific_check_guidance_ships.py`, `test_scope_reduction_trap.py`, `test_security_stack.py`, `test_session_routines.py`, `test_status_vocabulary_advisory.py`, `test_stewardship_rules_ship.py`, `test_upgrade.py`, `test_upgrade_module_additions.py`, `test_verification_boundaries.py`, and `test_verify_ref.py` (all under `bootstrap/tests/`). The initial run also explicitly included `examples/scientific-minimal/test_water_budget.py` and `examples/minimal/test_greet.py`.

The 28 AGENTS readers omitted by the selector guard were `bootstrap/tests/test_agreement_retired.py`, `test_check_cairn_content.py`, `test_comprehension_floor.py`, `test_doc_drift_tools.py`, `test_fork_advisory.py`, `test_gate_manifest.py`, `test_gate_preflight.py`, `test_generated_output_scan.py`, `test_hardening.py`, `test_install_time_onboarding.py`, `test_link_check_exclusions.py`, `test_lockfile_module.py`, `test_module_merge.py`, `test_module_merge_lockfile.py`, `test_next_session_local_note.py`, `test_notice_install.py`, `test_oracle.py`, `test_quality_gate_neutrality.py`, `test_scaffold_substrate.py`, `test_security_leaf.py`, `test_security_verification.py`, `test_slotmerge_leaf.py`, `test_test_tiers.py`, `test_upgrade_edit_check_runs_no_project_programs.py`, `test_upgrade_lockfile_path_containment.py`, `test_upgrade_refuses_hostile_project_data.py`, `test_verify_integrity.py`, and `test_writing_rules_ship.py`. The guard was preserved; these readers were not run. This is 28, not 29.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest --junitxml=/private/tmp/cairn-final-a-7d675b81.xml` with the 25 initially selected bootstrap files and both explicit example files | 0 | 1,662 passed; 0 failed, errors or skips | 67.97 s | unknown |
| `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest --junitxml=/private/tmp/cairn-final-a-7d675b81-supplement.xml bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_verify_ref.py` | 0 | 131 passed; 0 failed, errors or skips | 28.93 s | unknown |
| JUnit ID comparison for the two reports | 0 | 1,662 + 131 distinct IDs; overlap 0; unique union 1,793 | <1 s | unknown |

The first run's 25-file bootstrap selection was the corrected union minus `test_upgrade_module_additions.py` and `test_verify_ref.py`; it was not rerun. The supplemental run was disjoint by exact JUnit `classname::name` IDs. Reports: `/private/tmp/cairn-final-a-7d675b81.xml` and `/private/tmp/cairn-final-a-7d675b81-supplement.xml`.

Standing prose checks ran before pytest on all 13 changed Markdown files, including `CHANGELOG.md`: `AGENTS.md`, `CHANGELOG.md`, `dev/modules/security-review.md`, `dev/modules/testing-discipline.md`, `dev/plans/_template.md`, `dev/proposals/_template.md`, `docs/methodology/dual-review.md`, `docs/methodology/plans.md`, `templates/core/AGENTS.md`, `templates/core/dev/plans/_template.md`, `templates/core/dev/proposals/_template.md`, `templates/modules/team-gated/security-review.md`, and `templates/modules/team-gated/testing-discipline.md`. Commands were canonical Python 3.13.13 `scripts/claim_check.py <file>` once per file; `scripts/link_check.py <13 files>`; `scripts/check_cairn.py <13 files>`; `scripts/sync_doc_snippets.py <13 files>`; `scripts/quality_gate.py --sub neutrality`; `scripts/quality_gate.py --sub redundancy`; and `git diff --check BASE^..COMMIT` separately for all six source pairs. All exited 0. Link and content checks scanned 13 files; snippets had no drift. Neutrality had 0 failures and 43 informational notices; redundancy had 0 failures and 1 informational notice. Three external links were not probed. No full suite, certification, or Boundary B ran.

**Non-pass disposition**: no non-passes in these two final pytest segments or prose gates. Earlier failed attempts remain historical and are excluded from these counts and from the 1,793-node unique union; no partial green totals were combined. **Plan-specific acceptance commands**: C2 remains a human-judgment obligation; these automated checks do not establish authorization authenticity or complete the ordinary/Security code reviews. **Known omissions**: 28 guarded AGENTS readers above; external-link probes; Boundary B and code reviews remain outstanding.

**Boundary B mode**: not run; it follows the required code reviews and parent authorization. This record closes only Boundary A.

## Code review -- Codex Terra (MEDIUM) -- 2026-11-05

**Foundations**

1. **Should this happen as framed?** The guidance retains the normal cap, scoped per-pass authorization and no automatic clearance, but C2's human-applied evidence is still missing -- `AGENTS.md`; `docs/methodology/dual-review.md`, Caps and closure; implementation log.
2. **Best alternative.** Keep the existing stage record and human decision instead of an authorization checker; phrase guards cannot establish that an authorization is genuine -- accepted proposal, S1-S5; `test_review_stance_in_shipped_files.py::_security_cap_violations`.
3. **What would show it wrong?** An unapproved third pass, reusable authorization or automatic clearance accepted as valid would defeat the rule -- plan, C2; implementation log's hypothetical cases.

Reviewed source: `b30adff0` and final combined source `7d675b815954ec2fe2c6e88184e51321d4da53d6`; source pairs and iteration selection recorded at `c06d69ca`. Status: `5cb529c4a`.

**Tier**: Internal
**Bounding**: ACCEPTED
**Findings**: one blocking unmet criterion
**Verdict**: REVISE

**C2 human application remains unshown.** C2 requires human-applied examples. The implementation log honestly identifies its applications as agent simulations, not actual human judgment. My own application agrees that closed work advances, missing or reused authorization rejects a further pass, and a pass does not itself clear a finding; it is also an agent application and cannot satisfy the human criterion. Close with a human applying and recording the hypothetical cases, including the authorized scoped case and the negative cases, or obtain the Maintainer's explicit allowance for a plan deviation. No real additional pass or authorization need be fabricated.

Boundary A reports 1,793 distinct passes on the clean final source; no test rerun here. Final wide Boundary B and separate Security code review remain owed.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed source, accepted proposal, plan and reviews, exception-guard bodies, worked-case record and final iteration evidence. **Not covered**: actual human judgment, authorization authenticity, suite reruns, Security Review or Boundary B.

## Code review -- Codex Sol (HIGH) -- 2026-11-05

**Foundations**

1. **Should this happen as framed?** The guidance preserves the normal cap, fresh per-pass authority and no automatic clearance, but accepted C2 remains unmet -- eight cap carriers; plan, C2; implementation log at `8731e741`.
2. **Best alternative.** Keep existing stage records and worked cases, not an authorization parser or more automated runs; neither can substitute for the required human application -- accepted proposal, S1-S5; plan, C2.
3. **What would show it wrong?** Removing expected value from any actual carrier must fail its owning entry point. Eight controls passed and all eight carrier-file faults were caught -- `/private/tmp/cairn-sol-code56.nbJqIF/cap-probe.py` and `cap-report.json`.

Reviewed commit: 7d675b815954ec2fe2c6e88184e51321d4da53d6
Owned source pairs: b30adff0^..b30adff0; bef11a3f^..bef11a3f; final pair inventory/evidence: c06d69ca.
Worked cases: 8731e741; ordinary review: f8a9542e; submitted status: cb529c4a.

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Bounding**: ACCEPTED -- mapped carrier coverage is adequate; more tests cannot supply human application.
**Findings**: one blocking unmet criterion, F5-1
**Verdict**: REVISE

**F5-1 -- Human application remains missing.** C2 explicitly requires
human-applied examples. The implementation honestly records agent simulations;
Bohr's and my applications are also agent work. Close through the Maintainer
applying and recording the listed hypothetical positive/negative cases in the
existing record, or an explicit Maintainer allowance amending that criterion
and naming the lost human-interpretation evidence. No real extra pass or
authorization need be fabricated. An unanswered request supplies no allowance.

Python 3.13.13 probes changed each actual input file separately, not merely a
helper. Those eight carriers and their guard are byte-identical between the
probed `bef11a3f` and final source. No tested mutation survived. The final A
record reports 1,793 distinct passes, including the disjoint changelog-reader
supplement; that establishes neither authorization authenticity nor C2.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed carrier/guard changes, accepted source/plan, ordinary
review, worked cases, final A and actual-file probes. **Not covered**: actual
human application, authenticity, dishonest records or final wide Boundary B.
No mapped-suite replay or full suite; no source change or new review stage.

## Author response -- Codex Luna (Implementation, LOW) -- 2026-11-05

**F5-1 accepted.** The recorded cases are agent simulations, not the required
actual human application. The request for that application or an explicit
Maintainer deviation remains pending; it is not granted or inferred from the
unanswered request. Source `7d675b81` and the 1,793-node Boundary A evidence
remain unchanged. Boundary B may verify the reviewed code but cannot satisfy
C2 or clear F5-1. No additional Security Review pass is requested or ordered.

## Boundary B pointer -- Codex Luna (Implementation, LOW) -- 2026-11-05

The [shared wide verification](archive/2026-11-04-implementation-plan-completion.md#implementation-verification----codex-high----2026-11-05) on `573da3f4` passed 2,471 tests with one Windows-only skip
across 2,472 distinct nodes. F5-1 remains unmet; the Maintainer wait and
`revising-code` status stand. B does not establish actual human application,
and no A totals were added. Elapsed is in the shared record; tokens unknown.
