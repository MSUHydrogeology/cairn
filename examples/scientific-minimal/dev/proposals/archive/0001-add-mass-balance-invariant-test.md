# Add the mass-balance invariant test to `water_budget`

**Author**: Maintainer
**Status**: accepted
**Review**: usual
**Plan review**: not required(one test module and a small dataset; implemented and archived in one commit)
**Opened**: 2026-05-28
**In brief**: Test that the water budget closes, so a sign, unit or column mistake can no longer ship silently.

> This is a deliberately tiny, illustrative proposal for the
> `examples/scientific-minimal/` walkthrough. It shows the *shape* of a
> Cairn record on a *scientific* workflow, at the smallest scale. See
> the example `README.md` for the narrated trace.

## Context

The toy `water_budget.py` reads a CSV of monthly precipitation,
evapotranspiration, runoff, recharge and observed storage change for a
catchment, all in millimetres per month, and writes a residual column.
Water in minus water out must equal the change in storage:

    precip - et - runoff - recharge = dS_storage

so the residual is

    residual = precip - et - runoff - recharge - dS_storage

On a closed synthetic budget the residual should be round-off only. The
script computes and writes it, but **nothing tests that the budget
closes**. A sign flip in the formula, a column rename in the loader, or a
silent scaling error in a future contribution would all ship without a
test catching them.

## Proposal

Add `test_water_budget.py`, pinning the mass-balance invariant:

1. The shipped dataset (`data/water_budget_2025.csv`) satisfies
   `max(|residual|) < RESIDUAL_TOL_MM` (0.5 mm/month).
2. The formula's signs are right, on rows whose answer is known by hand:
   an all-zero row gives 0; a precipitation-only row gives +precip; a row
   where evapotranspiration equals precipitation gives 0.
3. Reading the CSV and writing the residuals keeps every row and adds the
   `residual_mm` column.
4. The command-line entry point returns 0 on the balanced dataset.

Plus two deliberately unbalanced rows ("sentinels") that must exceed the
tolerance. They prove the test can fail: if the residual formula
collapsed to `return 0`, the sentinels would catch it.

## Alternatives considered

* **Do nothing.** The budget is checked by eye, when someone remembers.
* **Check the residual only on the shipped dataset.** A balanced dataset
  cannot tell a correct formula from one that always returns 0; the
  sentinels and the hand-computed rows close that gap.

## Evidence / verification plan

The test module above, run with `python -m pytest test_water_budget.py`.

### Independent scientific check

The expected values in item 2 come from hand arithmetic on rows with
known answers, not from the code. Flipping the sign of evapotranspiration
in the formula must make `test_residual_formula_signs_match_doctrine`
fail; that failing run is the evidence the check works.

## Signals the change is wrong

The shipped dataset fails the tolerance (the data, not the formula, is
unbalanced), or a sentinel row passes.

## Review -- Reviewer -- 2026-05-28

```
Reviewed commit: illustrative example; no real commit
Target: the whole proposal
Prior findings: none
Assurance path: standard
```

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes: it pins the conservation law the
   script already encodes, without changing the script's behaviour --
   `water_budget.py`.
2. **Best alternative.** Checking only the shipped dataset, which a
   formula returning 0 would also pass; the sentinels rule that out --
   `test_water_budget.py::test_unbalanced_rows_exceed_tolerance`.
3. **What would show it wrong.** Each mistake the author fears has a test
   that fails on it. A flipped sign fails
   `test_residual_formula_signs_match_doctrine` on the row where
   evapotranspiration equals precipitation. A relaxed tolerance lets the
   sentinels pass, which their test catches. A renamed column raises
   `KeyError` in `test_default_dataset_satisfies_invariant`.

No findings. A plan is not needed at this size.

## Decision -- Maintainer -- 2026-05-28

**ACCEPTED.** The Maintainer's authorization, quoted verbatim:

> "Accepted. Land the test with the dataset and archive this proposal in the same commit."

Implemented in the commit that archived this proposal, with the test and a
CHANGELOG line.
