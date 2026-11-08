# Plan: Adopter execution retries

**Source proposal**: [Bounded execution retries for adopters](../proposals/archive/2026-11-05-codex-adopter-execution-retries.md)
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Let adopters correct an ordinary execution mistake twice before escalating, while keeping capability floors and safeguards.

## Build summary

Align the installed governing rule and published roles guidance with the accepted bounded retry rule. Verify real installs with and without the optional model-selection module, and show that each accepted safeguard is detected when removed. Existing reviews, checks and authority boundaries remain in force.

## Source proposal

The heavy Decision at `f499cb12` accepts two feedback-driven same-tier retries after an initial correctable execution failure, with immediate escalation on demonstrated capability mismatch. The incident rate-limit is unmet; the delegated Sol disposition at `888a3f3f` grants one exception for this complete reversible bundle, not a gate pass or standing change. The independent stronger-check rule and review-failure escalation remain distinct.

## Scope

Revise `templates/core/AGENTS.md` and `docs/methodology/roles.md`, and their actual readers in `bootstrap/tests/contract/test_model_tier_rule_ships.py` and, only if stale, `bootstrap/tests/test_review_stance_in_shipped_files.py`. Inspect `dev/modules/model-selection.md` and `templates/modules/team-gated/model-selection.md`; both currently address failed review and the independent stronger check rather than ordinary execution correction, so retain them unless the specified wording creates a contradiction. If changed, update both in parity and test each. Do not edit Cairn's local `AGENTS.md`: its local retry rule already exists. Coordinate roadmap/changelog entries with their owner at the applicable serialization point. No runtime tool, ledger, new file protocol or release operation is added.

**Reuse.** `rg` for escalation and retry found the existing local rule, the two shipped owners, both module twins and the model-tier contract's real solo scaffold fixture. Extend that existing test home; N/A: no production code added. The archived readable-work plan at `5b2bc401` retains complete-plan and assigned-tier requirements; the wording below preserves them and does not reopen its Decision.

## Sequence

Both required fresh plan reviews and their response precede one Low execution chunk. The source owners and scaffold profiles exist; no unfinished plan is a prerequisite. Estimate one to two focused work windows plus reviews; installed-profile mutations and mapped test runtime are uncertain.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align rule and roles, extend existing installed-profile safeguards, run scoped checks and mutations | Both plan reviews and response | Consistent adopter guidance and evidence |

After C1, ordinary and separate Security code reviews, their responses and final wide Boundary B remain due. Human release operations are not a completion condition.

## Acceptance criteria

**C1 wording.** In `templates/core/AGENTS.md`, remove only “If lower-tier work fails its check, re-run once one tier up.” from the Model tier paragraph. Immediately after that paragraph insert:

> **Execution retries.** For a correctable execution error in work at or above its capability floor, allow up to two same-tier retries after the initial failed attempt. Each retry uses concrete failure feedback, retains earlier failure evidence and reruns only the affected check during the correction loop. After two failed retries, re-run once one tier up. Escalate immediately if the failure shows the task exceeds the assigned tier; work below its capability floor is not eligible. Retries never replace independent review or Security Review, waive an accepted criterion or required check, expand authority, cross a plan fence or data-governance boundary, or change capability floors. Before repeating a potentially destructive operation, establish the previous attempt's effects. The correction-loop limit does not remove final Boundary B or any other required check. A review finding is not an execution retry.

In `docs/methodology/roles.md`, retain the fan-out paragraph and stronger-check exclusion. Replace the existing **Escalation applies** paragraph with:

> **Escalation applies to every role, not only the fan-out.** Work written below its floor, or a review blocked on a defect that tier should have caught, is re-run once one tier up; do not retry it at the same tier. For a correctable execution error in work at or above its floor, allow up to two same-tier retries after the initial failed attempt. Each retry uses concrete failure feedback, retains earlier failure evidence and reruns only the affected check during the correction loop. After two failed retries, re-run once one tier up. Escalate immediately if the failure shows the task exceeds the assigned tier. Retries never replace independent review or Security Review, waive an accepted criterion or required check, expand authority, cross a plan fence or data-governance boundary, or change capability floors. Before repeating a potentially destructive operation, establish the previous attempt's effects. Final Boundary B and all other required checks remain due. A review finding is not an execution retry.

The complete reviewed plan and assigned task floor remain requirements; no retry grants a design decision or bypasses a fence. The optional module's failed-review and stronger-check clauses continue unchanged; a same-tier model cannot supply the independent stronger check. A contradictory installed instruction, third retry, below-floor retry or missing safeguard fails delivery.

**Install and mutations.** In `bootstrap/tests/contract/test_model_tier_rule_ships.py`, preserve checks for the common Model tier paragraph and local-only retry paragraph; update `test_the_rule_reads_the_same_in_both_copies` to compare common Model tier text directly after removing the shipped immediate-escalation sentence, and independently check the new shipped retry paragraph. Extend the existing solo fixture and add a fixture using `bootstrap/profiles/collaborative-team.yml`, each invoking the real `bootstrap/scaffold.py --config <profile> --target <empty target> --cairn-root <root> --allow-dev`. Assert the solo output lacks `dev/modules/model-selection.md`; assert the collaborative output contains it. In each installed `AGENTS.md`, isolate **Execution retries.** through the next paragraph and assert the exact sentences above after whitespace normalization. Assert the old immediate-escalation sentence is absent. Verify the collaborative module retains the failed-review escalation and same-tier stronger-check exclusion. Keep `test_review_stance_in_shipped_files.py` stronger-check assertions intact.

For source roles and each installed core output, use the existing contract test home to check the following distinct exact clauses: “up to two same-tier retries after the initial failed attempt”; “concrete failure feedback”; “retains earlier failure evidence”; “only the affected check during the correction loop”; “After two failed retries, re-run once one tier up”; “Escalate immediately if the failure shows the task exceeds the assigned tier”; below-floor exclusion (the source roles' first sentence and installed core's explicit ineligibility); independent review and Security Review; each accepted criterion and required check; authority; plan fence; data-governance boundary; capability floors; previous attempt's effects; final Boundary B and other required checks; and the distinction from review findings. Account for the two explicit wording variants above in the checks. Use one negative assertion per clause: from a fresh physical copy of the source or installed file, remove that exact clause once, assert the original anchor occurs once, and run the same file-reading assertion against it; it must fail while its untouched control passes. The test must read each named physical file, not substitute an in-memory string. For each profile also mutate the actual shipped core source in a separate clean copy by removing the retry-limit clause, run the real scaffold and require the installed-file assertion to fail; this proves the installation path reaches the guard. Record each mutation, actual failing assertion, controls and omissions. If either module twin changes, apply the same physical removal check to each changed module and the collaborative installed copy. These checks establish text delivery, not that agents classify errors honestly.

S1/S4/S5 remain as the proposal states: the worker supplies fallible evidence; an unclear failure does not authorize proceeding; prose cannot enforce honest classification. S2/S3 are exercised in C1 by the physical mutations and real installs, with each check's inputs traced and recorded.

## Scope delta

**Scope delta**: preserved.

## Verification

**Boundary A.** Before edits, map readers and byte pins using `rg` and `python tools/test_tiers.py for <changed paths>`; inspect each selected test's trigger and input, including both named test homes. Run the resulting scoped list and relevant claim, link, snippet and neutrality gates plus `python scripts/check_cairn.py`, using canonical Python 3.13.13 on separate committed copies with interpreter bindings. Test negative searches against a known positive. Record commands, source SHA, inputs, counts, timings, controls and omissions. Do not bypass integrity guards or run full-tree certification for ordinary implementation.

**Boundary C.** Fresh ordinary and separate Security code reviewers examine the committed result and implementation evidence, including physical mutations and both real profiles, and run tight targeted falsification. Address required failures and cheap advice; return a substantive fix to its reviewer for a targeted look.

**Boundary B.** After reviews and fixes, run wide verification on a clean unchanged final commit under canonical Python 3.13.x: mapped iteration checks for every changed file in the reviewed range, tier-map integration/workflow tests naming those files, and standing gates. Record range, clean pre/post state, interpreter, commands, counts, timings, touched surfaces, non-passes and omissions; record timing misses and place slow files on the existing consolidation list. Failed required checks remain implementation work. Certification and release remain separate.

## Plan review -- Codex Terra Medium -- 2026-11-06

Reviewed commit: 5e81a000ba671ffbb69cc8c4f5de844265dd8756

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 4 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: C1 specifies the accepted wording, preserved floors and fences, and both real install profiles sufficiently for Low execution; the incident gate remains unmet with a one-bundle exception, not a pass -- Acceptance criteria; source Decision and `888a3f3f`.
2. **Best alternative.** Keep immediate escalation: it avoids implementation and mutation work but retains the reported handoffs and does not deliver the accepted retry outcome; no simpler path shown preserves the required safeguards and install evidence -- source Alternatives and Evidence; C1 Install and mutations.
3. **What would show it wrong?** A missing safeguard passing its physical mutation, a profile lacking the expected rule or module state, or an installed instruction allowing below-floor retries would falsify delivery -- C1 Install and mutations.

The plan supplies exact text and mutation targets, retains the separate stronger-check and review rules, and directs tracing actual inputs. The source's doctrine rate-limit is identified as unmet and the exception is bounded to this bundle. Scoped `claim_check.py` on the committed plan passed in an archive copy.

**Coverage:** Read the committed plan, accepted source, plan template, relevant existing contract test and profile, and rate-limit rationale. Did not run implementation tests or mutations, assess the separate Security Review obligation, or independently verify the global prose gates; those remain due under their owners.

## Plan review -- Codex Sol High (Security Review) -- 2026-11-06

Reviewed commit: c8a9eec4

**Obligation**: Internal Security Review
**Tier**: Internal
**Model**: gpt-6.1-sol (High)
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 4 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: C1 gives Low execution exact governing and roles wording while preserving the accepted capability, authority and verification safeguards; the one-bundle exception leaves the incident prerequisite unmet -- Acceptance criteria; source Decision and Doctrine gate disposition at `888a3f3f`.
2. **Best alternative.** Reuse the existing file-reading contract and scaffold fixture, extending them for both module states, as planned: a source-only assertion would be smaller but lose the accepted evidence that adopters receive the safeguards -- Install and mutations; `bootstrap/tests/contract/test_model_tier_rule_ships.py`, `solo_install`.
3. **What would show it wrong?** Remove each specified safeguard from a physical source or installed copy and require the same assertion to fail beside a passing control; a surviving deletion or contradictory collaborative instruction would refute delivery -- Install and mutations; `bootstrap/profiles/collaborative-team.yml`.

The exact paragraphs exclude below-floor retries, require immediate capability escalation, retain failure evidence and prior-effect inspection, and preserve independent reviews, checks, authority, plan fences and data governance. The correction-loop restriction explicitly leaves final Boundary B due. The optional module's stronger-check rule remains distinct: its same-tier exclusion and failed-review escalation are preserved rather than reinterpreted as execution corrections -- C1 wording; `templates/modules/team-gated/model-selection.md`, stronger independent check.

The real entry-point installs and physical clause removals address source-to-adopter delivery without claiming honest failure classification. S1/S4/S5 retain that limitation. The source gate disposition authorizes one reversible bundle, adds no standing exception and grants no release or trust operation; the plan introduces no runtime tracker or new authority -- source Doctrine gate disposition; Scope.

**Coverage:** Read the committed plan and accepted source, current plan template, existing contract fixture and clause reader, collaborative profile, and module safeguards. Did not execute future implementation tests or mutations, verify global prose gates, measure retry behavior, or discharge either future code review.

## Plan review response -- gpt-6-luna -- 2026-11-06

The ordinary and Security plan reviews accept C1 without findings (`c8a9eec4`, `8e616a06`). No operative change or Decision is needed. The accepted gate disposition remains a one-bundle exception for reversible work, not a pass or a standing change.

**Elapsed**: unknown. **Tokens**: unknown.

## Implementation verification -- gpt-6-luna -- 2026-11-06

**Model**: gpt-6-luna (Low). **Tokens**: unknown. **Elapsed**: owner contract 3.07 s as reported by pytest; test-tier selection time not reported.

**Bytes and interpreter.** Checks used a separate clean clone of commit `131241249ae9391c76e711a6fea39045e51784a7` at `/private/tmp/cairn-adopter-retries-13124124`, with its local interpreter binding installed via `bootstrap._scaffold.install.write_local_env`. Canonical Python was 3.13.13. The clone was clean before and after the owner check.

**Owner control and mutations.** `python3.13 -m pytest bootstrap/tests/contract/test_model_tier_rule_ships.py -q` passed: 64 passed in 3.07 s. It exercises real solo and collaborative scaffold installs, verifies optional-module presence/absence, the exact installed retry paragraph, and the module's same-tier stronger-check exclusion and failed-review escalation. Its physical-file control/mutation check covers every accepted clause on source roles and both installed core outputs: all 51 isolated deletions failed the same file-reading assertion with the corresponding missing-clause label. Two further separate clean Cairn clones each removed the retry-limit clause only from `templates/core/AGENTS.md`, ran the real scaffold with the solo and collaborative profiles, and failed the installed-file assertion as expected. Controls passed; no mutation was unresolved. These checks establish delivery of wording, not honest failure classification.

**Mapped selection.** On the clean clone, `python3.13 tools/test_tiers.py for --range 2b0556e4..131241249ae9391c76e711a6fea39045e51784a7 templates/core/AGENTS.md docs/methodology/roles.md bootstrap/tests/contract/test_model_tier_rule_ships.py` selected six test files: `bootstrap/tests/contract/test_model_tier_rule_ships.py`, `bootstrap/tests/contract/test_writing_rules_ship.py`, `bootstrap/tests/integration/test_link_check_exclusions.py`, `bootstrap/tests/test_check_cairn_content.py`, `bootstrap/tests/test_loop_fidelity_gate.py`, and `bootstrap/tests/test_review_stance_in_shipped_files.py`. The AGENTS guard omitted 42 readers: `bootstrap/tests/contract/test_certifying_run_rule.py`, `bootstrap/tests/contract/test_comprehension_floor.py`, `bootstrap/tests/contract/test_review_and_verification_rules_ship.py`, `bootstrap/tests/contract/test_stewardship_rules_ship.py`, `bootstrap/tests/contract/test_test_tiers.py`, `bootstrap/tests/contract/test_verification_boundaries.py`, `bootstrap/tests/integration/test_gauge.py`, `bootstrap/tests/test_agreement_retired.py`, `bootstrap/tests/test_board_json_contract.py`, `bootstrap/tests/test_claim_check_module.py`, `bootstrap/tests/test_core_dev_folders.py`, `bootstrap/tests/test_doc_drift_tools.py`, `bootstrap/tests/test_documentation_plan_module.py`, `bootstrap/tests/test_fork_advisory.py`, `bootstrap/tests/test_gate_manifest.py`, `bootstrap/tests/test_gate_preflight.py`, `bootstrap/tests/test_hardening.py`, `bootstrap/tests/test_install_report_slots.py`, `bootstrap/tests/test_install_time_onboarding.py`, `bootstrap/tests/test_lockfile_module.py`, `bootstrap/tests/test_module_merge.py`, `bootstrap/tests/test_module_merge_lockfile.py`, `bootstrap/tests/test_next_session_local_note.py`, `bootstrap/tests/test_notice_install.py`, `bootstrap/tests/test_oracle.py`, `bootstrap/tests/test_quality_gate_neutrality.py`, `bootstrap/tests/test_quickstart_sequence.py`, `bootstrap/tests/test_review_sweep_ships.py`, `bootstrap/tests/test_scaffold.py`, `bootstrap/tests/test_scaffold_substrate.py`, `bootstrap/tests/test_scope_reduction_trap.py`, `bootstrap/tests/test_security_leaf.py`, `bootstrap/tests/test_security_stack.py`, `bootstrap/tests/test_security_verification.py`, `bootstrap/tests/test_slotmerge_leaf.py`, `bootstrap/tests/test_upgrade.py`, `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py`, `bootstrap/tests/test_upgrade_lockfile_path_containment.py`, `bootstrap/tests/test_upgrade_module_additions.py`, `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`, and `bootstrap/tests/test_verify_integrity.py`. Root owns the joined mapped run; only the contract file was run by this author.

**Other checks and limits.** `python scripts/claim_check.py docs/methodology/roles.md` passed before commit, and the assigned-path diff check passed. Root owns the scoped committed-copy prose gates and the joined mapped run. Did not run the other five selected test files or full-tree certification; ordinary and Security code reviews and final wide Boundary B remain due. No module twin or `bootstrap/tests/test_review_stance_in_shipped_files.py` was changed; the latter remains in the mapped selection.

## Implementation verification addendum -- gpt-6-luna -- 2026-11-08

**Model**: gpt-6-luna (Low). **Tokens**: unknown. **Elapsed**: targeted repair check 0.32 s as reported by pytest; remaining orchestration time unknown.

**Joined Boundary A and qualification.** On clean committed range `2b0556e4..c997107f`, canonical Python 3.13.13 ran the 12-file mapped selection in 219.207 s: 1,256 passed, 1 failed, 0 skipped; all seven scoped prose gates passed and the copy was clean before and after (`/private/tmp/cairn-retry-iteration-k2dum1g8/result.json`). The sole failure was `bootstrap/tests/contract/test_writing_rules_ship.py::test_cairn_only_retry_budget_does_not_enter_adopter_guidance`: its old assertion prohibited the accepted generic adopter retry budget. At `18f4fbee`, the guard was replaced to prohibit Cairn-specific local retry label/override markers while positively checking generic retry guidance. The replacement node `test_cairn_local_retry_markers_do_not_enter_adopter_guidance` passed 1 test in 0.32 s with four physical-copy controls/mutations (shipped and installed controls pass; label and override marker mutants fail their corresponding assertions). No original suite result is relabeled as a 1,257-pass run.

**Post-fix readiness.** Root rechecked clean commit `18f4fbee2d26d0389d01ae72c5948e5c9127b101` in a separate copy. The mapped selection remained the same 12 files; the `AGENTS.md` guard reported 37 omitted readers, listed in `/private/tmp/cairn-retry-ready-xtl1bdg9/ready.json`; all seven scoped prose gates passed, with clean pre/post state. This was a readiness/map and prose-gate check, not a rerun of the 12-file suite. The original 64-test owner contract and 51 source/installed safeguard deletions plus two real-scaffold source mutations remain as recorded above. Source wording and implementation evidence are unchanged by `18f4fbee`.

**Disposition and remaining work.** The obsolete assertion is corrected and the mapped result is ready for independent review. Ordinary and Security code reviews and final wide Boundary B remain due; this plan remains open until those required reviews and checks pass. No full-tree certification was run.

## Code review -- Codex Terra Medium -- 2026-11-08

Reviewed commit: 176d2caf93ef196e488fd014af1fff1c1c5b4ff2
Reviewed range: 2b0556e4..176d2caf93ef196e488fd014af1fff1c1c5b4ff2

**Model**: gpt-6.1-terra (Medium). **Verdict**: ACCEPT. **Findings**: none.
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the installed rule and roles text preserve the accepted two-retry ceiling, immediate capability escalation, review distinction and authority safeguards; the owner exercised both real install profiles and physical clause removals -- C1 wording and implementation verification; `templates/core/AGENTS.md`; `docs/methodology/roles.md`.
2. **Best alternative.** Source-only assertions would be smaller but would not show the safeguards reach both adopter profiles; the existing scaffold fixture and physical-file checks provide that evidence without a new mechanism -- `test_model_tier_rule_ships.py` and C1 Install and mutations.
3. **What would show it wrong?** A physical removal of a safeguard that the file reader accepts, an installed profile missing the rule, or a same-tier stronger check accepted by the module would falsify delivery; repeat those mutations and installs if their paths change -- owner verification and `test_model_tier_rule_ships.py`.

**Bounding**: ACCEPTED. Challenged the stale writing-rule assertion and the 37 omitted AGENTS readers: the former now tests local-only markers alongside generic guidance, while the mapped selection and omissions are recorded for final wide Boundary B. The 12-file run's one failure was repaired and only its replacement node rerun; it is not claimed as a full passing run.

On a separate committed copy with canonical Python 3.13.13, `test_the_rule_reads_the_same_in_both_copies` and `test_cairn_local_retry_markers_do_not_enter_adopter_guidance` passed (2 tests, 0.35 s). The latter includes four physical control/mutation cases. The module retains failed-review escalation and the same-tier stronger-check exclusion. The one-bundle gate exception is not a gate pass. No cheap findings or advice identified.

**Coverage:** Read the committed plan, accepted proposal and Decision, implementation and verification records, changed rule and test surfaces, and module safeguards. Did not rerun the owner mutation set or mapped suite, assess honest classification of failures, or perform the separate Security Review or final Boundary B.
