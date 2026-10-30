# Plan: Deliver the outcome with less apparatus

**Source proposal**: dev/proposals/archive/2026-10-30-claude-cut-the-apparatus.md
**Status**: awaiting-plan-review
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

**C1.** One proposal review and response, one plan and code review, and at most two Security passes; only unresolved blockers or unmet criteria at the cap go to the Maintainer by name. Clean work advances without clearing review. Light is the proposal default, proposed higher tiers stand unless the Decision changes them; named high-risk surfaces and added or widened trust boundaries trigger heavy, and newly discovered boundaries stop work. Ordinary uncertainty takes the lighter lane with a reason. Blocking means hard-to-undo damage or unmet accepted criteria/checks; authors dispose of other advice. Proposal operative text revises in place, reviews remain intact, and responses list dispositions. Trivial work and the scope floor remain intact.

**C2.** `AGENTS.md` is at most 2,500 words, preserving operative rules and moving explanation to doctrine. Reviews are at most 300 words and append to the artifact; preserve verdict, findings and coverage gap. Mutation summaries name control, total, killed, each survivor and equivalent with reason. Commit bodies are at most 30 lines, excluding verbatim Decision quotations. The governing sentence cites rationale anchor 17; avoidable burden against a simpler adequate alternative is a finding, without per-addition accounting. Deferral records remaining effort and re-entry cost and carries the obligation forward. Existing step records capture elapsed time and reported or defensibly estimated tokens, or unknown, without a new tool or approval.

**C3.** Shipped copies and all affected readers agree with C1–C2; existing property tests are updated without discarding their protection. The one-month indicator is review commits per archived artifact against the proposal's stated 6.9 baseline, not proof of value. No independent scientific check was specified.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A and B use Python 3.13.x. This is a contract change: Boundary B is **wide**, on the final clean committed tree, with `Certified by: pending`; no full-suite run is implied. Search actual readers and pinned bytes before edits and include all affected owners and consumers, splitting guarded selections without overrides. The initial mapped families are `bootstrap/tests/test_review_and_verification_rules_ship.py`, `test_scope_reduction_trap.py`, `test_model_tier_rule_ships.py`, `test_writing_rules_ship.py`, `test_review_stance_in_shipped_files.py`, `test_review_sweep_ships.py`, `test_session_start_drain_rules.py`, `test_verification_boundaries.py`, and `test_scaffold.py`; add other owners discovered by the named searches. These check the rules, shipped text, lifecycle and adopter paths. Check the gate manifest before changing pinned files and follow its existing ceremony only if actually triggered; do not repin or re-anchor per plan.

Run `python scripts/claim_check.py` on changed documents, `python scripts/check_cairn.py` for internal links and claims, `python scripts/link_check.py` for cross references, and `python scripts/quality_gate.py --sub neutrality --sub redundancy` for prose gates. Run snippet sync if a synced source changes. Record exact commands, outcomes and non-passes, elapsed time, interpreter, pre/post state, reviewed range and omissions in the implementation verification record. Code review independently challenges the record and its bounds; no certifying full suite is required here.
