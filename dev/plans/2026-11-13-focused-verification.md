# Plan: Focus verification on delivered promises

**Source proposal**: dev/proposals/archive/2026-11-12-codex-focused-verification-cost.md
**Status**: revising-code
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-13
**In brief**: Check changed promises as plans finish and join related work at the end of the development arc.

## Build summary

Make the self-hosted, shipped and public guidance agree on focused checks and evidence reuse. Plans finish after their own required checks and reviews; the arc owner joins interactions later. Keep security, scientific and release obligations intact.

## Source proposal

The [accepted proposal](../proposals/archive/2026-11-12-codex-focused-verification-cost.md) places this consistency repair in v0.7 and defines the changed selection and integration rules. Its Decision authorizes this plan, not baseline application, signing, publication or another full suite.

## Scope

Doctrine and shipped guidance: `dev/agent_collaboration.md`, `templates/core/dev/agent_collaboration.md`; public explanations: `docs/methodology/plans.md`, `docs/methodology/dual-review.md`; authoring templates: `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`. `AGENTS.md` routing remains unchanged. No new forms, tools, checkers, roles, gates, coordination rewrite or permanent tests are in scope. Reuse: N/A, no code added.

## Sequence

Estimate 4.5–8 agent-hours and 2–5 elapsed hours including release packet refresh, with reviewer availability and affected reader bindings uncertain. Plan review precedes implementation. After approval C1 and C2 can run in parallel, each owning only its named files; the coordinator owns plan records, board, changelog, review disposition and closure. Each worker claims its exact paths and commits its own files. Required ordinary and Security code reviews follow the combined implementation; correct findings and run affected checks before archive.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Guidance and public explanations: the two collaboration files and two methodology files | Reviewed plan | Consistent operative and public rules |
| C2 | Both plan and both proposal templates | Reviewed plan | Matching authoring guidance and one short example |
| C3 | Coordinator joins evidence, reviews and corrections; records closure | C1 and C2 | Reviewed, verified plan ready to archive |

The existing item 12 release-closeout owner refreshes the AST packet's exact-candidate binding and affected reader bindings after the final committed guidance, reusing applicable AST body analysis. This is release work in `dev/PLANNING.md` item 12, not a plan completion or human baseline gate. The baseline remains unpassed until the named Maintainer operation supplies evidence. The known certification at `072d82d2` had 5,344 passed, 63 skipped and six failed in 49m06s; five corrected cases have 14 targeted passes. No full repeat is required for this documentation change.

## Acceptance criteria

**C1.** Name changed caller-visible promises, public entry points and outputs; select the smallest checks for plausible faults and reuse results only where bytes, platform, input and obligation still apply, citing source and limits. Review may use committed evidence or static calculation when adequate, with executable evidence for forward behavior. Remove blanket scratch attempts and per-member mutations; universal claims inventory their members and check applicable paths. Preserve scientific *touches* triggers and independent error and positive controls, required security checks and reviews, and S2's valid existing negative control; a new security check has a demonstrated failing case.

Plans complete required checks, reviews and dispositions before archive. One joined run follows connected plans, or occurs earlier at a named critical shared boundary. Before arc completion or release, the arc owner records final combined revision coverage, producers, consumers, results and omissions; applicable prior results cover unchanged behavior and inputs, and corrections rerun only affected interactions. The arc owner owns and records a post-archive defect's repair under existing rules without reopening the archived plan. Failed promises and required checks remain plan work before archive.

**C2.** Templates express the same rules and preserve scientific, security and release triggers. One short plan example names a changed output and its check, a reused control with its limit, and a later joined run. It does not require a mutant or scratch attempt for each claim. Shipped and self-hosted template pairs agree.

**C3.** Independent ordinary and Security reviews test the combined text against the accepted proposal and name gaps; findings and required checks are disposed before archive. The item 12 owner receives the candidate-refresh trigger and evidence location. No human baseline operation blocks this plan's closure.

## Scope delta

**Scope delta**: preserved.

## Verification

Check the eight files against the accepted proposal and existing obligations, including a known-positive search when searching for retired instructions. Compare each shipped pair with its self-hosted counterpart. Run claim, link, snippet and neutrality prose gates; inspect readers and byte pins before selecting affected tests. At minimum run `bootstrap/tests/contract/test_scientific_check_guidance_ships.py::test_the_check_guidance_reaches_every_copy_and_promise_site` for the installer acceptance slot and `bootstrap/tests/test_review_sweep_ships.py::test_every_install_carries_the_sweep_as_shipped` for installed review guidance if their actual paths exercise the edited text. Run `bootstrap/tests/contract/test_writing_rules_ship.py::test_installed_readable_prompt_and_contrary_mutation` with `-k "not strategy"` for the plan and proposal template installations; compare substantive duties statically because byte parity does not prove them. Select other real affected public/shipping nodes from their test bodies, not all 18 mapper owners; explain omissions and any applicable prior evidence. Do not add wording pins or permanent tests for this prose. A failed required check remains open; no full suite solely for this change. Record commands, results, limits, elapsed time and tokens in existing plan records.

## Plan review -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-13

Reviewed commit: 55cf427c7a23d1e53e95d6e13eedbb1056ff0770

**Obligation**: Internal
**Tier**: Internal
**Verdict**: REVISE
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** Yes, once installed template verification is specified: the two independent chunks carry the accepted eight-file consistency repair and preserve required controls. -- Plan Scope, Sequence and C1–C3; accepted proposal > Proposal.
2. **Best alternative.** Reuse the existing installer parity check and static semantic comparison; no new wording tests or wider owner replay are needed. -- `bootstrap/tests/contract/test_writing_rules_ship.py::test_installed_readable_prompt_and_contrary_mutation`.
3. **What would show it wrong?** A real installation differing from either shipped template, or a preserved duty missing from an operative copy, would falsify completion. -- Same installer node; plan C2 and Verification.

**Blocking — installed template path.** C2 promises shipped template parity, but Verification names a slot parser and a review-sweep installer check; neither establishes installation of the edited proposal and plan templates. The instruction to select other nodes leaves the executable path unspecified for the low-tier worker. Name the existing `bootstrap/tests/contract/test_writing_rules_ship.py::test_installed_readable_prompt_and_contrary_mutation` node for both template parameters; compare substantive duties statically rather than claiming that byte parity proves them.

**Rules and audience:** The proposed changes deliberately replace per-plan integration and blanket mutation, while retaining scientific, security and release duties in installed instructions and public explanations; their actual preservation needs the implementation comparison. **Covered:** committed plan, accepted proposal, named test bodies and template review rules. **Not covered:** implementation, test execution, full downstream reader inventory or measured savings. **Elapsed:** approximately four minutes. **Tokens:** unknown.

## Plan review -- GPT-6 Sol (Security Review, High) -- 2026-11-13

Reviewed commit: 55cf427c7a23d1e53e95d6e13eedbb1056ff0770

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Verdict**: ACCEPT
**Findings**: none

The plan checks each changed public promise and joins related work at arc end, while preserving required security and scientific controls.

**Foundations**

1. **Should this happen as framed?** Yes. C1 assigns the public-output evidence, required security checks and reviews, scientific error and positive controls, final combined coverage, and late-defect owner; C2 reaches installed templates. -- `dev/plans/2026-11-13-focused-verification.md` > Acceptance criteria.
2. **Best alternative.** Use the existing eight homes and their current review and verification records, as planned; adding a new gate or per-plan integration would add burden without an accepted outcome. -- accepted proposal > Proposal and Documentation / doctrine surface; plan > Scope.
3. **What would show it wrong?** In the final eight-file comparison, a security check with no demonstrated failing case, a touched scientific result with no independent error and positive controls, or an arc closed without applicable final-revision integration evidence would falsify delivery. -- plan > Acceptance criteria and Verification; `dev/proposals/_template.md` > Security preflight and Independent scientific check.

**Rules and trust boundary:** The current S2 wording requires a fresh mutation for each check; the accepted change permits an applicable existing negative control and still requires a demonstrated failing case for a new security check. C1 states that distinction. Missing or failed required checks stay open, and the Maintainer's release operations remain separate. The Internal review's installed-template test finding still needs author disposition; this pass does not clear that obligation.

**Covered:** The frozen plan, accepted proposal and current security, scientific, review and archive triggers; static comparison only. **Not covered:** Edited guidance, test bodies or execution, future integration evidence, packet refresh or release. No tests ran. **Elapsed:** approximately eight minutes. **Tokens:** unknown.

## Response -- GPT-6.1 Terra (Implementation) -- 2026-11-13

The ordinary review finding is closed in Verification: the existing real-install byte-parity node is named for both edited template parameters, with static comparison retained for substantive duties. The Security Review accepted without another finding. **Disposition**: ready-to-implement. **Elapsed**: approximately one minute. **Tokens**: unknown.


## Implementation -- GPT-6.1 Terra (coordinator) -- 2026-11-13

C1 is `19ffac65`, corrected at `8643bb14` to remove the remaining fresh-probe-only wording and retain temporary-development-test cleanup. C2 is `12ba3fab`, with the example corrected to the supported upgrade-plan command at `85afa73d`. The supported scoped finalizer renewed only the three changed self-install guidance records; no ancestor cache, engine, schema or ref changed. Workers ran claim checks and no tests. One C2 pre-edit claim was missed; the four-file commit had no overlap, and its correction was claimed.

Independent ordinary and Security reviews now read the joined committed eight-file change. The coordinator runs the named installed-copy and slot checks once, plus prose gates, rather than replaying the 18-owner mapper list. Other live-session changes to the board, changelog and archived records remain outside this work's commits. **Elapsed:** aggregate worker time unknown; **Tokens:** unknown.

## Code review -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-13

**Reviewed:** `bbbf426f`; **Obligation:** Internal; **Verdict:** REVISE.

**Foundations**

1. **Should this happen as framed?** Yes: the installed collaboration and template rules select changed public outputs, retain security and scientific controls, and join connected work later; the public explanation must agree. -- plan C1–C2; collaboration > Verification; plan template > Verification.
2. **Best alternative:** Correct the existing public passages in place; a new gate or wording test is unnecessary. -- accepted proposal > Proposal; `docs/methodology/plans.md` > Plan triage rule and Boundary C.
3. **What would show it wrong?** A reader following the public explanation still performs per-plan integration, or repeats evidence solely for a later unrelated commit. -- accepted proposal > Integration point.

**Blocking — conflicting public instructions.** `docs/methodology/plans.md` > Plan triage rule still says light work records Boundary B after its implementation and uses per-plan bounded/wide B to choose a plan; the latter also conflicts with the current light/standard/heavy plan rule. Its later Boundary C replacement trigger requires a new B record for *any* later change, including an unrelated commit, despite the adjacent reuse rule. Align these passages with the operative lifecycle and joined-evidence rules, retaining required checks and affected-interaction corrections.

**Audience and changed rules:** The installed files are operative; the two methodology files explain them publicly. The change deliberately replaces per-plan integration and blanket scratch/per-member mutations, not security, scientific or release obligations. **Covered:** static comparison of all eight committed files, accepted proposal and plan, including later repeated sections; finalizer changes three lock rows. **Not covered:** execution, installation, hash correctness, measured savings or future arc evidence; coordinator owns selected checks. **Elapsed:** approximately six minutes. **Tokens:** unknown.

## Code review -- GPT-6 Sol (Security Review, High) -- 2026-11-13

**Reviewed:** `efb03f5a..bbbf426f`; **Obligation:** Internal Security Review; **Verdict:** REVISE.

The change reuses applicable negative controls while retaining required checks, reviews, scientific controls and trust ceremonies. The joined-run rule gives the arc owner the final combined revision.

**Foundations**

1. **Should this happen as framed?** Yes, after the public record example and replacement rule agree with the accepted joined-run timing. -- accepted proposal > Integration point; `dev/plans/_template.md` > Verification; `docs/methodology/plans.md` > Boundary B.
2. **Best alternative.** Repair the existing public passages in place and retain ceremony-specific full runs; no new check or form is needed. -- `docs/methodology/plans.md` > Boundary B and Boundary C.
3. **What would show it wrong?** A future plan archiving only after a per-plan B record, or an arc owner replaying unchanged checks for an unrelated commit, would contradict the accepted rule. -- `docs/methodology/plans.md` > implementation-verification example and replacement trigger 4.

**Blocking — stale public record contract.** The `docs/methodology/plans.md` implementation-verification example still labels a plan-local record `Boundary B mode`, requires clean pre/post state at one tested commit, and describes a later plan-only commit. Replacement trigger 4 fires for *any* later change. This tells security-sensitive plan authors to produce per-plan joined evidence or replay it for an unrelated commit, despite nearby final-arc and reuse rules. Separate the plan-local record from the arc owner's joined record; limit replacement to affected behavior while retaining prescribed trust-ceremony runs. The ordinary review identifies stale triage text.

**Rules and audience:** Installed S2 accepts an applicable existing negative control and requires a failing case for a new security check; scientific *touches*, independent error and positive controls, security reviews, final-arc coverage and release duties remain stated. **Covered:** frozen eight-file text, repeated sections, three lock-row changes and accepted proposal; static comparison. **Not covered:** tests, installation, hash validation, future arc evidence or release. **Elapsed:** approximately 12 minutes. **Tokens:** unknown.

## Code review, second pass -- GPT-6 Sol (Security Review, High) -- 2026-11-13

**Reviewed:** `172e0010..bf1d7bff`; **Obligation:** Internal Security Review; **Verdict:** REVISE. This pass addresses a new repair defect.

The repair correctly separates plan-local checks from joined integration evidence. Its plan-triage edit also removes a required route to code review.

**Foundations**

1. **Should this happen as framed?** The record repair should remain, but the triage change cannot remove review for a one-file contract or trust-ceremony change. -- `docs/methodology/plans.md` > Plan triage rule, before and after `bf1d7bff`.
2. **Best alternative.** Keep the original fifth trigger's underlying risk categories independently of Boundary B mode, with the existing cheap-defect exception. -- same triage rule at `efb03f5a`; accepted proposal > Integration point.
3. **What would show it wrong?** Apply the revised skip rule to a one-commit, one-file trust-ceremony change: it skips the plan and therefore code review. -- `docs/methodology/plans.md` > “For standard/heavy, skip the plan when.”

**Blocking — review trigger lost.** `bf1d7bff` replaces the fifth open-plan trigger with a duplicate of the first four and removes the skip condition for contract, trust-ceremony and unbounded-effect changes. A single-file change on those surfaces can now skip both plan and code review. Restore those risk categories as the independent fifth trigger, exclude them from plan skipping, and update the fast-multi-stage explanation while retaining the three-condition cheap-defect exception. Do not reinstate per-plan Boundary B execution.

**Covered:** only this new triage defect against the prior public rule and accepted scope; static counterexample. **Not covered:** other repair passages, tests, installation or ceremony execution. **Elapsed:** approximately five minutes. **Tokens:** unknown.
