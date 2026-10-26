<!-- ^ Illustrative path: this example narrates a hypothetical proposal in the example's own dev/ tree, not a claim about Cairn's tree. -->

# Scientific minimal example — Cairn on a tiny science workflow

The two [`case-studies/`](../../case-studies/) are the full-apparatus
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
[`../../on-ramp/README.md`](../../on-ramp/README.md)): a `dev/`
tree with the proposal lifecycle, run by hand.

## The change, traced through the lifecycle

Cairn first sorts a change into one of three lanes
([`../../doctrine/lifecycle.md`](../../doctrine/lifecycle.md)): a typo or
one-line fix is just a commit with its test and no code review; a change
with a settled shape gets a short note and a review; a new capability gets
the full path. The change here -- *add the mass-balance invariant test and
the residual writer to `water_budget.py`* -- adds a capability, so it took
the full path, shown in five steps:

1. **Propose.** A proposal is written and committed:
   [`dev/proposals/archive/0001-add-mass-balance-invariant-test.md`](dev/proposals/archive/0001-add-mass-balance-invariant-test.md).
   It states the context, the change, and that it is small enough that
   no separate plan was needed.
2. **Review.** A fresh reviewer who did not write the proposal appends
   a `## Review` section to the same file -- here, confirming
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

That is the entire loop on a scientific shape. On a real project the
proposal is larger (the tolerance comes from the data rather than a
constant, the dataset is real and may not close to within machine
epsilon, and the residual gets its own diagnostic plot) and a change
that is not this small opens a plan. Review is the same at every stage:
a fresh reviewer, plus a domain expert if you have one, who checks the
conservation-law step. The shape is identical.

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
