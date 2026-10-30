# Plan: Deliver the outcome with less apparatus

**Source proposal**: dev/proposals/archive/2026-10-30-claude-cut-the-apparatus.md
**Status**: revising-code
**Plan review**: required(Internal)
**Opened**: 2026-10-30
**In brief**: Reduce recurring review and instruction overhead while preserving agreed outcomes and required assurance.

## Source proposal

The accepted proposal sets bounded review, proposal tiers, author closure of advice, shorter instructions and current proposal text, comparative complexity review, and accountable deferral. Its Decision addendum retains elapsed time and reported or defensibly estimated tokens in each existing step record, with unknown recorded as unknown.

## Scope

Update `AGENTS.md`, `dev/agent_collaboration.md`, proposal and plan templates, their shipped counterparts under `templates/core/`, `doctrine/lifecycle.md`, `doctrine/dual-review.md`, `doctrine/rationale.md`, `templates/modules/team-gated/dual-review.md` and `security-review.md`, and both session-start skill copies. Follow changed rules through affected guidance, executable templates, and tests; retain the accepted scope floor, trivial lane, and existing security obligations. Do not add a telemetry tool or approval. Existing records retain their history.

**Reuse.** Search `rg -n 'second round|Uncertainty resolves|complete current contract|Security Review' doctrine dev templates bootstrap/tests` and the corresponding surface-name search in `bootstrap/tests`; reuse the current templates, review records, and shipping-property tests instead of adding a parallel process. Resolve any additional actual readers found while implementing.

### Documentation / doctrine surface

Cross-cutting prescription stays in `AGENTS.md`, detailed rationale in doctrine, and authoring procedures in the deliberation templates; shipped guidance follows the same rules. Route any descriptive changes by `docs/DOCUMENTATION_PLAN.md`.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Reconcile lifecycle and risk rules | Plan review | Pass caps, tiers, advice closure, in-place proposal revision, and corresponding shipped rules. |
| C2 | Reduce load and account for burden | C1 | Compressed guidance, review and mutation summaries, complexity and deferral rules, timing/token observations. |
| C3 | Align consumers and verify | C1–C2 | Updated existing tests, shipped copies and scoped verification evidence. |

## Acceptance criteria

**C1.** One proposal review and response, one plan and code review, and at most two Security passes; only unresolved blockers or unmet criteria at the cap go to the Maintainer by name. Clean work advances without clearing review. Light is the proposal default (one short review, no plan); standard has one pass per stage, and heavy adds Security Review. Proposed higher tiers stand unless the Decision changes them; named high-risk surfaces and added or widened trust boundaries trigger heavy, and newly discovered boundaries stop work. Ordinary uncertainty takes the lighter lane with a reason. Blocking means hard-to-undo damage or unmet accepted criteria/checks; authors dispose of other advice. Proposal operative text revises in place, reviews remain intact, and responses list dispositions. Trivial work and the scope floor remain intact.

**C2.** `AGENTS.md` is at most 2,500 words, preserving operative rules and moving explanation to doctrine. Reviews are at most 300 words and append to the artifact; preserve verdict, findings and coverage gap. Mutation summaries name control, total, killed, each survivor and equivalent with reason. Commit bodies are at most 30 lines, excluding verbatim Decision quotations. The governing sentence cites rationale anchor 17; avoidable burden against a simpler adequate alternative is a finding, without per-addition accounting. Deferral records remaining effort and re-entry cost and carries the obligation forward. Existing step records capture elapsed time and reported or defensibly estimated tokens, or unknown, without a new tool or approval.

**C3.** Shipped copies and all affected readers agree with C1–C2; existing property tests are updated without discarding their protection. Within one month, review commits per archived artifact are at or below 3.5, counted by the proposal's Context method (subjects containing `review` or `respon` divided by Markdown files added under the plan and proposal archives), against its stated 6.9 baseline; this is an indicator, not proof of value. No independent scientific check was specified.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A and B use Python 3.13.x. This is a contract change: Boundary B is **wide**, on the final clean committed tree, with `Certified by: pending`; no full-suite run is implied. Search actual readers and pinned bytes before edits and include all affected owners and consumers, splitting guarded selections without overrides. The initial mapped families are `bootstrap/tests/test_review_and_verification_rules_ship.py`, `test_scope_reduction_trap.py`, `test_model_tier_rule_ships.py`, `test_writing_rules_ship.py`, `test_review_stance_in_shipped_files.py`, `test_review_sweep_ships.py`, `test_session_start_drain_rules.py`, `test_verification_boundaries.py`, `test_skills_install.py`, `test_skills_upgrade.py`, and `test_scaffold.py`; add other owners discovered by the named searches. These check the rules, shipped text, lifecycle, and adopter install and upgrade paths. If the security designation changes, also run `bootstrap/tests/test_security_verification.py`; the prose gates below apply to these surfaces. Check the gate manifest before changing pinned files and follow its existing ceremony only if actually triggered; do not repin or re-anchor per plan.

Run `python scripts/claim_check.py` on changed documents, `python scripts/check_cairn.py` for internal links and claims, `python scripts/link_check.py` for cross references, and `python scripts/quality_gate.py --sub neutrality --sub redundancy` for prose gates. Run snippet sync if a synced source changes. Record exact commands, outcomes and non-passes, elapsed time, interpreter, pre/post state, reviewed range and omissions in the implementation verification record. Code review independently challenges the record and its bounds; no certifying full suite is required here.

## Plan review -- Codex (GPT-6) -- 2026-10-30

```
Reviewed commit: e72e0e9d5d3bb18aff041664ebba366e133fcc4d
Target: operative plan against accepted proposal and Q1 addendum
Prior findings: none
Assurance path: high-assurance -- governing doctrine
```

**Obligation**: Internal plan review
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes, with two contract and verification gaps closed: the chunks cover the six cuts and Q1, but C3 weakens an accepted outcome and the test map omits known consumers. -- proposal cuts 1–6, Q1 addendum, and plan C1–C3.
2. **Best alternative.** Keep the three chunks and current files; add the missing target and affected readers to their existing cells, then use the plan's wide Boundary B. No new framework or routine full-suite run is needed. -- plan Sequence and Verification; `AGENTS.md` > Verification boundaries.
3. **What would show it wrong.** A month with more than 3.5 review commits per archived artifact despite a claim of success, or an installed session skill retaining the old escalation rule, would falsify delivery. -- proposal Evidence / verification plan; `bootstrap/tests/test_skills_install.py:42`, `test_skills_upgrade.py:35`.

### Findings

1. **P1 -- Blocking: restore the accepted one-month target.** C3 names the 6.9 baseline but drops the accepted `at or below 3.5` target. The baseline alone permits a result such as 6.8 to be called progress, while the proposal's criterion fails. Put the target and its counting method in C3; keep the warning that the ratio is an indicator, not proof of value. Satisfier: C3 criterion. -- proposal Evidence / verification plan:122–123; plan C3.

2. **P2 -- Blocking: map the known installed-skill consumers.** The plan changes both session-start skill copies, but its initial mapping omits `bootstrap/tests/test_skills_install.py` and `test_skills_upgrade.py`. Search may discover them later, but the pre-implementation map must make these known public paths reviewable now. Name the relevant install and upgrade nodes or families and their standing gates; retain discovery for further readers. The security-designation property in `test_security_verification.py` is relevant only if that designation changes. Satisfier: Verification cell. -- plan Scope and Verification; `test_skills_install.py:42,136–150`; `test_skills_upgrade.py:35,58–73`; `test_security_verification.py:1506–1551`; plan template Verification.

3. **P3 -- Non-blocking: spell out the three tier outcomes.** C1 protects the light default and heavy triggers but does not state that light has one short review and no plan, standard one pass per stage, and heavy adds Security Review. This is the central ceremony change and merits a falsifiable C1 criterion. Satisfier: C1 criterion. -- proposal cut 2; plan C1.

**Coverage.** Compared accepted scope, Q1, sequence, criteria, alternative, burden, placement, shipped paths, and named test readers (review sweep lenses 1, 2, 5, 7–9; cited above). Did not run implementation, tests, scaffold, month-long measurement, or Security Review. Existing Security Review obligations remain separate.

## Response to plan review -- Codex (GPT-6) -- 2026-10-30

- **P1, accept:** C3 restores the one-month threshold and the proposal's counting method, with its indicator limitation.
- **P2, accept:** Verification maps the installed-skill install and upgrade families and conditionally the security-designation owner, alongside standing prose gates and reader discovery.
- **P3, accept:** C1 states each tier's review and plan outcome.

The operative cells carry the corrections; the Internal plan review is complete.

## Implementation verification -- Codex (GPT-6.1 SOL) -- 2026-10-30

**Boundary B mode**: wide. This changes governing contracts and shipped
instructions. The mapping covers review, scope, model-tier, writing, session,
verification, installer, upgrade, scaffold, certifying-run, comprehension,
stewardship, note, slot, documentation and integrity readers. Narrower bounds
could miss a shipped reader or a removed module slot.

**Certified by**: pending
**Tested commit**: `3cceb2c06f9d894adb1ec2dcb2d3ce72f999ff07`
**Reviewed range**: `2e8cb0fea7158d83645b1ad473c34dba322da957..3cceb2c06f9d894adb1ec2dcb2d3ce72f999ff07`
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13)
**Pre-run state**: fresh detached worktree at `/tmp/cairn-boundary-b-k7Z7nH`; `git status --porcelain` empty; HEAD tested commit.
**Post-run state**: `git status --porcelain` empty; HEAD unchanged.
**Elapsed**: about 16 seconds of wall time for the parallel check groups and final claim/gate pass.
**Tokens**: unknown.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| Python 3.13.13 `-m pytest -q --tb=no` on group A below | 0 | 1,252 passed; 0 failed/skipped/xfail/xpass | 13.81 s | unknown |
| Python 3.13.13 `-m pytest -q --tb=no` on group B below | 0 | 256 passed; 0 failed/skipped/xfail/xpass | 7.79 s | unknown |
| `python3.13 scripts/check_cairn.py` | 0 | 199 Markdown files; 0 issues | within 1.60 s combined | unknown |
| `python3.13 scripts/link_check.py` | 0 | 199 Markdown files; 0 issues | within 1.60 s combined | unknown |
| `python3.13 scripts/sync_doc_snippets.py` | 0 | 468 documents; 0 drift | within 1.60 s combined | unknown |
| `python3.13 scripts/claim_check.py` on every changed Markdown file | 0 | 31 files; 0 flags | 1.07 s | unknown |
| `python3.13 scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | 0 failures; informational notes only | 1.12 s | unknown |

Every `python3.13` above means the absolute interpreter in the field above.
For pytest groups, prepend `bootstrap/tests/` to each listed basename. The
claim-check selection was the Markdown paths in `git diff HEAD^ HEAD --name-only`.

Group A (exact pytest selection): `test_review_and_verification_rules_ship.py`,
`test_scope_reduction_trap.py`, `test_model_tier_rule_ships.py`,
`test_writing_rules_ship.py`, `test_review_stance_in_shipped_files.py`,
`test_review_sweep_ships.py`, `test_session_start_drain_rules.py`,
`test_verification_boundaries.py`, `test_skills_install.py`,
`test_skills_upgrade.py`, `test_scaffold.py`, `test_certifying_run_rule.py`,
`test_comprehension_floor.py`, `test_stewardship_rules_ship.py`,
`test_next_session_local_note.py`, `test_quickstart_sequence.py`,
`test_install_report_slots.py`, `test_documentation_plan_module.py`,
`test_verify_integrity.py` (all under `bootstrap/tests/`).

Group B (exact pytest selection): `test_agreement_retired.py`,
`test_check_cairn_content.py`, `test_doc_drift_tools.py`,
`test_fork_advisory.py`, `test_generated_output_scan.py`,
`test_install_time_onboarding.py`, `test_link_check_exclusions.py`,
`test_loop_fidelity_gate.py`, `test_notice_install.py`,
`test_quality_gate_neutrality.py`, `test_replacement_tools.py`
(all under `bootstrap/tests/`).

**Non-pass disposition**: none. The prose gates reported informational
exemptions and one existing redundancy note, not failures. Whole-tree link
checks initially found an archived-proposal link in `dev/PLANNING.md:53`; its
target was repaired before this commit and both gates then passed.

**Plan-specific acceptance commands**: mapped and discovered readers above;
word counts were 2,455 for root `AGENTS.md` and 2,378 for the shipped copy;
session-start copies matched byte-for-byte. The four shipped module slots
remain installed and their supplier tests passed. No security designation
changed, so the conditional security-verification family was not triggered.

**Known omissions**: the one-month review-commit ratio in C3 is a future
indicator and cannot yet be measured; it remains open. No independent
scientific check was specified. External URLs (98 in `check_cairn`, 99 in
`link_check`) were not probed by these offline gates. The full-tree certifying
suite was not run, as this plan does not authorize it.

## Code review -- Codex (GPT-6.1 SOL) -- 2026-10-30

```
Reviewed commit: 3cceb2c06f9d894adb1ec2dcb2d3ce72f999ff07
Target: 2e8cb0fea7158d83645b1ad473c34dba322da957..3cceb2c06f9d894adb1ec2dcb2d3ce72f999ff07; Boundary B record at 4bfba7dd
Prior findings: none
```

**Verdict**: REVISE. **Bounding**: ACCEPTED. **Elapsed**: about 4 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes, but two shipped rules disagree with the accepted cuts. -- `AGENTS.md:83`, `doctrine/lifecycle.md:213`, `templates/modules/team-gated/security-review.md:53`.
2. **Best alternative.** Reconcile plan triage with the light tier and remove the extra boundary trigger in its existing carrier. -- `doctrine/proposals.md:180`, accepted proposal cuts 2 and 4.
3. **What would show it wrong?** A light proposal touching two areas must both skip and open a plan; the committed text produces that case. -- `AGENTS.md:16,83`; `doctrine/lifecycle.md:205-213`.

### Findings

1. **P1 -- Blocking: light-tier plan rule conflicts with mandatory triage.** Root and shipped `AGENTS.md` say light means no plan, while the same root file says every non-trivial accepted proposal gets a plan; `doctrine/lifecycle.md:205-213` requires one for multi-area or wide work. A light, multi-area proposal has no valid route. C1/C3 require coherent shipped rules. Align both carriers, doctrine, templates, and tests while delivering the accepted no-plan outcome.
2. **P2 -- Blocking: moved boundaries still trigger Security Review.** Accepted cut 2 expressly deletes “moves” as a trigger, retaining added/widened boundaries. `templates/modules/team-gated/security-review.md:53` and both proposal templates' security preflight still trigger on movement, while `AGENTS.md:86-87` does not. Reconcile the shipped rule and templates to the accepted trigger, preserving added/widened protection.

**Falsification ledger.** Isolated `git archive 3cceb2c0` control: 699 mapped property tests passed (Python 3.13.13); the light/multi-area conflict survives. Inspected root/shipped rules, triage, templates, and session skill; copies and word limits match Boundary B. No mutation or full suite. **Coverage:** lenses 1, 3, 5-9: cited paths and control; did not run adopter installation, external links, Security Review, or the one-month measure.

## Response to code review -- Codex (GPT-6.1 SOL) -- 2026-10-30

- **P1, accept:** `3c9892a6` makes light's no-plan route unconditional on the old standard/heavy plan triage, including multi-area and wide work. It records light Boundary B evidence in the accepted proposal. Root/shipped rules, doctrine, templates, readers, and a nine-carrier property test now agree.
- **P2, accept:** Both security modules and proposal preflight templates trigger for added or widened boundaries; movement alone does not trigger. Existing high-risk triggers remain. Scaffold and module property tests cover the shipped and self-hosted copies.

The focused follow-up should falsify these two corrections against the clean-commit record below. The plan remains `revising-code` until that follow-up confirms the findings are closed.

## Implementation verification -- Codex (GPT-6.1 SOL) -- 2026-10-30

This record covers the code-review correction at `3c9892a6`. **Boundary B mode**: wide. The correction changes governing lifecycle, review, security-trigger, template, and shipped-reader contracts. The mapping covers owning property families, scaffold/install/upgrade and documentation consumers, and the standing prose gates; narrower bounds would miss a public reader.

**Certified by**: pending
**Tested commit**: `3c9892a655b9bdc4ccae2722498ecc74d3794ccf`
**Reviewed range**: `88d6ff31b0d1b93adca1329088803ab9d86dbe20..3c9892a655b9bdc4ccae2722498ecc74d3794ccf`
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13)
**Pre-run state**: fresh detached worktree `/tmp/cairn-apparatus-b-3c9892a6`, clean `git status --porcelain`, HEAD at tested commit.
**Post-run state**: clean `git status --porcelain`, identical HEAD.
**Elapsed**: about 17 seconds for concurrent groups and gates. **Tokens**: unknown.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| Python 3.13.13 `-m pytest -q --tb=no` on Group A in the preceding record | 0 | 1,263 passed; 0 failed/skipped/xfail/xpass | 16.07 s | unknown |
| Python 3.13.13 `-m pytest -q --tb=no` on Group B in the preceding record | 0 | 256 passed; 0 failed/skipped/xfail/xpass | 8.03 s | unknown |
| Python 3.13.13 `scripts/check_cairn.py` | 0 | 199 Markdown files; 0 issues | 1.26 s | unknown |
| Python 3.13.13 `scripts/link_check.py` | 0 | 199 Markdown files; 0 issues | 0.11 s | unknown |
| Python 3.13.13 `scripts/sync_doc_snippets.py` | 0 | 468 documents; 0 drift | 0.04 s | unknown |
| Python 3.13.13 `scripts/claim_check.py` separately on every Markdown path in `git diff HEAD^ HEAD --name-only -- '*.md'` | 0 | 21 files; 0 flags | 0.72 s | unknown |
| Python 3.13.13 `scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | 0 failures; informational notes only | 1.11 s | unknown |

Every Python command used the absolute interpreter above; Group A and B expand to the exact `bootstrap/tests/` selections in the preceding record. **Non-pass disposition**: none. **Plan-specific acceptance commands**: all mapped/discovered readers and standing gates above passed; root/shipped AGENTS word counts were 2,487/2,410. Security designation did not change, so the conditional security-verification family was not triggered. **Known omissions**: the C3 one-month ratio remains open; external URLs were not probed; no independent scientific check was specified; the certifying full suite was not run under this plan.
