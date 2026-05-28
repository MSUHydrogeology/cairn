# Add the mass-balance invariant test to `water_budget`

**Author**: Maintainer
**Date opened**: 2026-05-28
**Status**: accepted
**Touches**: `water_budget.py`, `test_water_budget.py`,
`data/water_budget_2025.csv`

> This is a deliberately tiny, illustrative proposal for the
> `examples/scientific-minimal/` walkthrough. It shows the *shape*
> of a Cairn lifecycle record at the smallest possible scale on a
> *scientific* workflow — a trivial-accept change on a throwaway
> water-budget reconciler. See the example `README.md` for the
> narrated trace.

## Context

The toy `water_budget.py` reads a CSV of monthly precipitation,
evapotranspiration, runoff, recharge, and observed storage change
for a catchment, and writes a residual column. The residual
formula encodes the conservation law

    precip - et - runoff - recharge = dS_storage

so the residual is

    residual = precip - et - runoff - recharge - dS_storage

For a closed water budget on synthetic data, the residual should be
small (round-off only). The script today computes and writes the
residual, but **does not test that the invariant actually holds** —
a sign flip in the formula, a column rename in the loader, or a
silent scaling error in a future contribution would all ship
without the test catching them.

This is the single most differentiated thing Cairn asks of a
scientific codebase (see `../../../docs/workflow-role.md` and the
codebase-readiness-report template section 11): the scientific
assumptions should be made *explicit* and *testable* rather than
left implicit in the code. The mass-balance invariant is exactly
that kind of assumption.

This is a one-function change plus one test plus two synthetic
edge cases — small enough to be a **trivial accept** (no separate
plan).

## Proposal

Add a test module `test_water_budget.py` that pins the
mass-balance invariant as four pytest cases:

1. The default dataset (`data/water_budget_2025.csv`) satisfies
   `max(|residual|) < RESIDUAL_TOL_MM`.
2. The residual formula's sign convention is correct (zero-row →
   residual 0; precip-only row → residual = +precip; closed
   precip=et row → residual 0).
3. The round-trip from CSV input through `compute_residuals` and
   `write_residuals_csv` produces a destination CSV with the
   `residual_mm` column and the same row count as the input.
4. The CLI `main()` returns exit code 0 on the balanced dataset
   (and would return 2 on an unbalanced one).

Plus two parametrized **sentinels** in `test_unbalanced_rows_exceed_tolerance`
covering deliberately-unbalanced rows: a precip-only row and a
precip-with-too-small-storage-change row, both well above
tolerance. The sentinels prove the invariant is not vacuous — if
the residual formula collapsed to "return 0", the sentinels would
catch it.

Absorb the test alongside the code (`a change absorbs its tests`)
in a single implementing-and-archiving commit.

## Review -- Reviewer (Internal) -- 2026-05-28

Verified the change is the test module plus two sentinel rows
plus the input dataset, with no edit to the existing `water_budget.py`
module beyond exporting the constants the test imports.
Backward-compatible (the script's external behaviour is unchanged;
the test exercises the existing public functions).

The four invariant cases plus the two parametrized sentinels give
a real falsification footprint:

* If the residual formula's sign flips, the
  `test_residual_formula_signs_match_doctrine` case fails on the
  closed-precip-et row.
* If the tolerance is silently relaxed, the
  `test_unbalanced_rows_exceed_tolerance` parametrized cases either
  start passing the unbalanced rows (which is the bug) or the
  tolerance constant is moved out of reach of the assertions
  (which is visible in the diff).
* If a column is renamed in the loader without updating the
  computation, `compute_residual` raises `KeyError` and the
  `test_default_dataset_satisfies_invariant` case red-flags it.

Recommend **accept** as a trivial change. The discipline of pinning
the conservation law as a test is exactly what the
codebase-readiness-report template's section 11 asks for; this
example will be the first place a reader sees that discipline in
action.

## Decision -- Maintainer -- 2026-05-28

**Accepted** as a trivial change. Implemented in the same commit
that archived this proposal; the test landed with it, and the
CHANGELOG line recorded it. This is the whole loop at minimum
scale on a scientifically-shaped workflow:
propose → review → decide → implement (with the test) → record.
