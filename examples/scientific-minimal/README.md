<!-- ^ Illustrative path: this example narrates a hypothetical proposal in the example's own dev/ tree, not a claim about Cairn's tree. -->

# Scientific minimal example — Cairn on a tiny science workflow

The two [`case-studies/`](../../case-studies/) are the full-apparatus
examples on real scientific projects. The
[`minimal/`](../minimal/README.md) example is a one-file `greet` CLI
showing the lifecycle at the smallest possible *generic* scale. This
example sits between them: a tiny **scientific** workflow (CSV in,
invariant tested, residual table out) so a scientist sees the
lifecycle on a shape they recognize rather than on a CLI toy.

The toy science: **monthly water-budget reconciliation.** Given a
CSV of monthly precipitation, evapotranspiration, runoff, recharge,
and observed storage change (all in mm/month for a catchment), the
workflow computes a residual and pins the **mass-balance invariant**
as a test:

> `precip - et - runoff - recharge = dS_storage`
>
> Equivalently, `residual = precip - et - runoff - recharge - dS_storage ≈ 0`.
>
> The test asserts `max(|residual|) < RESIDUAL_TOL_MM` across all
> rows.

This is the smallest shape that carries a *scientific contract*: a
named conservation law, a tolerance, and a synthetic-balanced input
the contract holds on. A real hydrologic dataset would have
process-rooted residuals (lateral subsurface flow, snow storage,
diversions) and a tolerance derived from the data, but the
lifecycle shape is identical.

This example, like [`minimal/`](../minimal/), has adopted Cairn at
**Level 1** (hand-copied kernel — see
[`../../on-ramp/README.md`](../../on-ramp/README.md)): a `dev/`
tree with the proposal lifecycle, run by hand.

## The change, traced through the lifecycle

One small change — *add the mass-balance invariant test and the
residual writer to `water_budget.py`* — moves through Cairn's five
steps ([`../../doctrine/lifecycle.md`](../../doctrine/lifecycle.md)):

1. **Propose.** A proposal is written and committed:
   [`dev/proposals/archive/0001-add-mass-balance-invariant-test.md`](dev/proposals/archive/0001-add-mass-balance-invariant-test.md).
   It states the context, the change, and that it's small enough to
   be a *trivial accept* (no separate plan).
2. **Review.** A reviewer (structurally independent of the author)
   appends a `## Review` section to the same file — here, confirming
   that the residual formula matches the canonical mass-balance and
   that the test pins both the closed-dataset case and unbalanced
   sentinels (so the invariant is not vacuous).
3. **Decide.** The Maintainer appends the `## Decision` section
   (accept), closing the deliberation. The proposal then moves to
   `dev/proposals/archive/`.
4. **Implement (absorbing tests + docs).** The code change lands
   with its test in the same step —
   [`water_budget.py`](water_budget.py) (the change) and
   [`test_water_budget.py`](test_water_budget.py) (the absorbed
   test). "A change absorbs its tests" is the discipline.
5. **Record.** The decision and rationale live in the archived
   proposal; a one-line CHANGELOG entry would record the invariant
   addition. The git history plus the archived proposal *are* the
   record.

That is the entire loop on a scientific shape. On a real project
the proposal is larger (the invariant has data-derived rather than
constant tolerance, the dataset is real and may not close to
within machine epsilon, and the residual gets its own diagnostic
plot), review is two-tier (Dual-Review with a domain reviewer for
the conservation-law step), and non-trivial changes open a plan —
but the shape is identical.

## Running the example

The workflow has **no third-party dependencies** (only `csv`,
`pathlib`, and `sys` from the standard library), so it runs anywhere
Python 3.11+ runs. Either form works -- pick whichever is more
convenient.

**From this example's directory** (`cairn/examples/scientific-minimal/`):

```bash
cd /path/to/cairn/examples/scientific-minimal

# Run the workflow (writes outputs/residuals.csv):
python water_budget.py

# Run the invariant test:
python -m pytest test_water_budget.py
```

**From the Cairn repo root** (the form Cairn's own pytest uses):

```bash
cd /path/to/cairn

# Run the workflow (writes outputs/residuals.csv beside the input):
python examples/scientific-minimal/water_budget.py

# Run the invariant test:
python -m pytest examples/scientific-minimal/test_water_budget.py
```

The CLI exits 0 when the mass-balance invariant holds; it exits 2
if the dataset's `max(|residual|)` exceeds tolerance. That second
exit code makes it easy to wire the workflow into a downstream
gate.

## What you will end up with

The workflow output (after a clean run):

* `outputs/residuals.csv` — the input rows with a `residual_mm`
  column appended; `< RESIDUAL_TOL_MM` everywhere on the shipped
  dataset.

The lifecycle record (already in this tree):

* `dev/proposals/archive/0001-add-mass-balance-invariant-test.md`
  — the trivial-accept proposal that introduced the invariant.

## Scientific assumptions made explicit

External-repo paths: `docs/assumptions.md`
The example's docs/assumptions.md analogue (the adopter's repo's
equivalent of that file) lives in the proposal's **Context**
section and the docstring of `compute_residual`. The load-bearing
ones:

* **Sign convention**: precipitation is a positive inflow;
  evapotranspiration, runoff, and recharge are positive outflows;
  `dS_storage` is the *observed* storage change (positive when
  storage grew).
* **Units**: all six budget columns are millimetres per month over
  the catchment area. The residual is in the same units.
* **Tolerance**: `RESIDUAL_TOL_MM = 0.5 mm/month`, tuned to the
  synthetic input's round-off. A real dataset would derive
  tolerance from measurement error and expected sub-monthly process
  residuals.

If a contributor changed a sign or a unit silently, the invariant
test would fail — that is what the discipline of pinning the
invariant earns.
