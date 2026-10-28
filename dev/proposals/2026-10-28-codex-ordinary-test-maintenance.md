# Make one ordinary test family easier to maintain

**Author**: Codex (Sol), Proposal author
**Status**: awaiting-review
**Review**: usual
**Plan review**: required(Internal)
**Opened**: 2026-10-28
**In brief**: Consolidate one board test family while preserving what it detects, then measure whether maintenance and test time improve.

## Context

Cairn's certifying suite took 24 minutes 55 seconds for 5,479 passing tests
at `7c910851` (`dev/PLANNING.md:123`). That is a whole-suite cost, **not**
evidence that board tests are slow. The 2,293-line
`bootstrap/tests/test_board_json_contract.py` repeatedly builds scratch
trees: `_build_golden_main_tree` supports terminal and JSON checks; other
tests construct trees separately for record fields, waits, guide examples,
and templates (for example lines 292–328, 764–834, 892–1008,
1088–1135, and 1554–1700). Those cases test different behavior; repeated
setup alone does not prove any assertion is redundant. The v0.6 roadmap
already calls for test-suite maintenance after narrowing the test freeze
(`dev/PLANNING.md:63`).

## Proposal

Pilot a bounded cleanup in `bootstrap/tests/test_board_json_contract.py`.
The plan inventories the file's test nodes, scratch-tree builders, repeated
case construction, public board behaviors, and plausible faults each case
catches. Select one coherent cluster of ordinary board cases with repeated
setup. Share only immutable input descriptions or fresh per-test builders;
never share a mutable repository, output capture, or temporary path between
tests. Merge equivalent cases only where the ledger maps every removed case
to a retained assertion against the same observable behavior and plausible
fault. Keep representative real `tools/board.py` CLI/subprocess checks,
including failure and exit behavior. A less repetitive test is useful even
if no case can safely be removed.

The pilot changes test organization, not `tools/board.py`, board JSON schema,
golden fixture, governing rules, or security/trust tests. It adds no testing
policy, new dependency, or lifecycle gate. Do not edit the currently frozen
test file until `dev/proposals/2026-10-28-codex-test-trust-boundary.md` is
accepted **and implemented** so ordinary test maintenance uses its reviewed
lane. The gate and any ceremony still in force at implementation remain
binding. This pilot does not discharge the roadmap's wider suite-maintenance
row; remaining families stay queued for later evidence and decisions.

## Rationale

A small family provides a checkable inventory and a meaningful before/after
comparison. It addresses the setup and review burden without treating test
lines or node counts as a deletion target. Keeping public-path and fault
coverage makes a shorter file useful only if it remains trustworthy.

## Alternatives considered

Do nothing: avoids churn, but repeated setup and long cases remain costly to
read and revise. Rewrite the whole suite or impose a line-ratio quota: neither
is justified by this family's evidence, and both make coverage loss hard to
audit. Parallel pytest or a new dependency may reduce elapsed time, but does
not simplify this family's maintenance and belongs to the separate runtime
row (`dev/PLANNING.md:123`).

## Documentation / doctrine surface

This deliberation lives in `dev/`. No governing or adopter-facing text
changes. The separate governing-text proposal owns semantic prose-test
changes; this pilot does not replace them (`dev/proposals/2026-10-28-codex-governing-text-single-source.md`).

## Evidence / verification plan

### Tests required

The plan identifies exact nodes in `test_board_json_contract.py` after its
inventory. Preserve the terminal golden-output, JSON baseline and record
shape, symlink/failure, wait, guide-example, and template-read behaviors that
the selected cluster covers. Run the affected nodes and the owning board
family through `tools/board.py`'s real `main` and retained CLI/subprocess
paths under the canonical Python 3.13 interpreter. Record a before-deletion
ledger: each removed node or case, its distinct property and plausible fault,
the retained node, and a probe that would expose an accidental loss. If a
case has no convincing replacement, keep it. The plan maps other files that
read the touched tests or builders, and applies Boundary A/B and existing
gate rules; an unbounded effect falls to full mode at the next authorized
certifying run.

### Examples / smoke checks

Run `scripts/claim_check.py`, `scripts/link_check.py`, and applicable
`scripts/quality_gate.py` subsets on changed prose. Compare the same scoped
board-family command on the committed control and final test bytes, using
the same interpreter, environment, and `pytest --durations` settings; report
elapsed time, slow nodes, setup duplication removed, reviewable line/case
changes, and unresolved costs. Time this during required scoped verification,
not with an extra full-suite run. Only the next authorized certifying run may
support a claim about whole-suite time. No timing gain is assumed.

#### Security preflight

N/A: no trust boundary added, moved, or widened; the pilot changes only
ordinary board tests and retains their subprocess checks.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A removed case has no retained property or fault probe; shared setup lets
tests influence each other; a real CLI failure or exit behavior disappears;
or measured maintenance and scoped runtime evidence shows no useful benefit
against the review and ceremony cost. In that case, keep or restore the case
and reconsider the pilot before broader consolidation.

## Scope delta

**Scope delta**: preserved. This opening pilot promises one bounded family
and keeps the roadmap's larger maintenance work visible.

## Assurance path

**Assurance path**: standard. Only ordinary test organization is proposed;
the separate test-trust-boundary work governs when those tests become editable.
