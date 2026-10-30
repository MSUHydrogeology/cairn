# Plan: Deliver the outcome with less apparatus

**Source proposal**: dev/proposals/archive/2026-10-30-claude-cut-the-apparatus.md
**Status**: ready-to-implement
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
