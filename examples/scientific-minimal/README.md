<!-- ^ Illustrative path: this example narrates a hypothetical proposal in the example's own dev/ tree, not a claim about Cairn's tree. -->

# Scientific minimal example — Cairn on a tiny science workflow

The two [`case-studies/`](../../docs/case-studies/) are the full-apparatus
examples on real scientific projects. The
[`minimal/`](../minimal/README.md) example is a one-file `greet` CLI
showing the lifecycle at the smallest possible *generic* scale. This
example sits between them: a tiny **scientific** workflow (CSV in,
invariant tested, residual table out) so a scientist sees the
lifecycle on a shape they recognize rather than on a CLI toy.

The toy science: **monthly water-budget reconciliation.** Water that
enters a catchment must leave it or stay in it. The input is a CSV with one
row per month: precipitation, evapotranspiration, runoff, recharge, and the
observed change in stored water, all in millimetres per month. The workflow
checks that the rows add up, and a test pins that check:

> `precip - et - runoff - recharge = dS_storage`
>
> In other words, `residual = precip - et - runoff - recharge - dS_storage`
> should be close to zero.
>
> The test asserts `max(|residual|) < RESIDUAL_TOL_MM` across all rows.

This is the smallest shape that carries a *scientific contract*: a named
conservation law, a tolerance, and a made-up input that balances by
construction. A real dataset has residuals with physical causes (lateral
subsurface flow, snow storage, diversions) and a tolerance taken from the
data, but the lifecycle shape is identical.

This example, like [`minimal/`](../minimal/), carries a Cairn kernel
copied in by hand, with no lockfile (see
[`../../install/on-ramp/README.md`](../../install/on-ramp/README.md)): a `dev/`
tree with the proposal lifecycle, run by hand.

## The change, traced through the lifecycle

This example narrates a **planned** standard change. Its records are
illustrative: they do not claim an actual independent review, Decision or
research result.

1. The [proposal](dev/proposals/archive/0001-add-mass-balance-invariant-test.md)
   describes the invariant and an illustrative review and Decision.
2. The [plan](dev/plans/archive/0001-mass-balance.md) sets a result and checks;
   its example review, code review and archive show how work can continue.
3. The shipped program and tests are the implemented result. Run the commands
   below, then try the deliberately unbalanced input. A zero exit means the
   synthetic rows close; exit 2 means a row exceeds the tolerance.
4. Try [installation and upgrade](upgrade.md), then read the [handoff](handoff.md).

The hand-calculated row P=100, ET=30, runoff=20, recharge=40 and storage
change=10 gives `100 - 30 - 20 - 40 - 10 = 0 mm/month` independently of the
program. Closure alone does not validate a scientific model.

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

# Deliberately unbalanced: writes a residual and exits 2.
python examples/scientific-minimal/water_budget.py examples/scientific-minimal/data/unbalanced.csv /tmp/cairn-unbalanced.csv
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
  — the illustrative accepted proposal that introduced the invariant.

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
* **Units**: the five budget columns (`precip_mm`, `et_mm`,
  `runoff_mm`, `recharge_mm`, `dS_storage_mm`) are millimetres per
  month over the catchment area; `month` is a date. The residual is
  in millimetres too.
* **Tolerance**: `RESIDUAL_TOL_MM = 0.5 mm/month`, tuned to the
  synthetic input's round-off. A real dataset would derive
  tolerance from measurement error and expected sub-monthly process
  residuals.

If a contributor changed a sign or a unit silently, the invariant
test would fail — that is what the discipline of pinning the
invariant earns.
