# Plan: Check a synthetic water budget

**Source proposal**: ../../proposals/archive/0001-add-mass-balance-invariant-test.md
**Status**: archived
**Plan review**: required(Internal)
**Opened**: 2026-05-28
**Rules that apply**: bright lines only
**In brief**: Check that a synthetic monthly water budget closes and report its residual.

This entire record is illustrative, including reviews and archive; it is not
proof that these events occurred or that a scientific model is valid.

## Build summary

Write residuals and check closure, with an independently calculated example.

## Source proposal

The illustrative Decision accepts the mass-balance invariant.

## Scope

Use the existing synthetic inputs and equation; add no physical assumptions.

**Reuse.** N/A: example code is already present.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Calculate and test residuals | Accepted proposal | Program, input and tests |

## Acceptance criteria

**C1.** A balanced input passes; an unbalanced input exits 2. A hand-calculated
row checks signs independently, with units and tolerance explained.

## Scope delta

**Scope delta**: preserved

## Verification

Run the program and its tests, compare the hand calculation and try an
unbalanced row; closure is not model validation.

## Plan review -- illustrative reviewer -- 2026-05-28

**Obligation**: Internal
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**
1. The plan checks the accepted equation. -- Acceptance criteria
2. Existing inputs are simpler than another model. -- Scope
3. A wrong sign that passes the hand calculation would falsify it. -- Verification

Coverage: example plan only; no actual independent review occurred.

## Code review -- illustrative reviewer -- 2026-05-29

**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**
1. The example reports the residual. -- water_budget.py
2. The existing small workflow is sufficient. -- Scope
3. An inverted flux sign should fail the hand-calculated check. -- Verification

Coverage: example record only; no actual independent review occurred.

## Archive -- illustrative author -- 2026-05-29

The example depicts completed implementation, verification and review. The
commands in the walkthrough can be run now; this record is not their evidence.
