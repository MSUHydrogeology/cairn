# Plan: Align lifecycle descriptions

**Source proposal**: dev/proposals/archive/2026-11-01-codex-lifecycle-description.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Correct four published descriptions so readers can see when a proposal needs a plan.

## Source proposal

The Maintainer accepted the heavy proposal at `2867a8e6`: describe the existing lifecycle consistently, without changing its rules or safeguards.

## Scope

Correct `README.md`, `docs/assets/three-lanes-of-change.svg`, `docs/release-process.md`, and `docs/methodology/lifecycle.md`. The published method is a protected doctrine surface; the other three describe the workflow. The operative prescription in `AGENTS.md`, shipped templates, and enforcement stay unchanged. Coordinate the lifecycle method with its existing claim holder before editing.

**Reuse.** N/A: no code added. Reuse the existing diagram and lanes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align four descriptions and accessible diagram text | Plan review, including Security Review | Four corrected existing surfaces |

## Acceptance criteria

C1: All four surfaces agree with `AGENTS.md` and the accepted cut-the-apparatus Decision: light is the default and has no plan, including wide or multi-area work; non-trivial standard and heavy work uses plan triage; named high-risk surfaces and added or widened trust boundaries trigger heavy. Preserve the outer lanes and all other review and check obligations. The diagram's visible labels, title, description and README alternative text agree. No new process, prescription or enforcement is introduced. Inspect the rendered diagram and accessibility text. A deliberate mutation asserting that light needs a plan must be detected by comparison with governing text; record the result.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: `python tools/test_tiers.py for README.md docs/assets/three-lanes-of-change.svg docs/release-process.md docs/methodology/lifecycle.md` selected 32 test files. Run its complete selection, plus claim, link, snippet and neutrality gates. Search readers and byte pins for all four paths, testing negative searches against known positives; inspect actual triggers and record findings. The preliminary path search found lifecycle readers in `test_stewardship_rules_ship.py`, `test_status_vocabulary_advisory.py`, `test_review_and_verification_rules_ship.py`, `test_scope_reduction_trap.py`, and `test_board_json_contract.py`; path matches include references and fixtures, so examine the triggers before drawing conclusions. Search the full tree, including manifests and indirect readers, before implementation; do not assume a negative from this preliminary search.

Boundary C: ordinary code review and separate Security Review examine the committed implementation and iteration evidence, and run targeted falsification checks rather than a suite.

Boundary B: wide, because published methodology is a protected doctrine surface. After review, run once on a clean unchanged final commit under canonical Python 3.13.x: the iteration selection for the reviewed range, integration/workflow tests in the tier map naming those files, and the applicable prose and plan-specific checks. Cover affected consumers and public paths; record commands, counts, interpreter, SHA/range, clean pre/post state, elapsed time, non-passes and omissions. Coordinate this selection with other concurrent work on the common final commit. No full-tree certification is authorized by this plan.
