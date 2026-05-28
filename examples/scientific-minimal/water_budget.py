"""A throwaway monthly-water-budget reconciler -- the toy scientific
workflow this example adopts Cairn on.

This file is the *result* of the worked change traced in
``README.md`` (proposal 0001 added the mass-balance invariant test
and the residual-writer alongside it).  It exists only to make the
lifecycle trace concrete on a *scientifically* shaped workflow
(CSV in, invariant tested, residual table out) -- it is not part of
Cairn's apparatus.

Mass balance (column units are all mm/month over the catchment):

    precip - et - runoff - recharge = dS_storage

so the residual is::

    residual = precip - et - runoff - recharge - dS_storage

For a closed water budget on synthetic data the residual is small
(round-off only).  The invariant the test pins is
``max(|residual|) < TOL`` where ``TOL`` is set by the maintainer.

Usage::

    python water_budget.py [INPUT_CSV [OUTPUT_CSV]]

Defaults to ``data/water_budget_2025.csv`` -> ``outputs/residuals.csv``
relative to this file.  No third-party dependencies -- ``csv`` is
in the Python standard library, so the example runs anywhere Python
runs.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Iterable


# Tolerance the invariant test pins.  Tuned to the synthetic input;
# a real-world hydrologic dataset would have process-rooted budget
# residuals (lateral subsurface flow, snow storage, anthropogenic
# diversions) that warrant a tolerance derived from the data, not
# this constant.
RESIDUAL_TOL_MM = 0.5

# Component columns in the canonical mass-balance order.
_FLUX_COLUMNS = ("precip_mm", "et_mm", "runoff_mm", "recharge_mm")
_STORAGE_COLUMN = "dS_storage_mm"


def compute_residual(row: dict) -> float:
    """Return ``precip - et - runoff - recharge - dS_storage`` for a row.

    Negative residual means the components imply less storage than
    the row's reported ``dS_storage_mm``; positive means more.
    """
    fluxes = [float(row[col]) for col in _FLUX_COLUMNS]
    storage = float(row[_STORAGE_COLUMN])
    precip, et, runoff, recharge = fluxes
    return precip - et - runoff - recharge - storage


def compute_residuals(rows: Iterable[dict]) -> list[dict]:
    """Return the input rows with a ``residual_mm`` column appended."""
    out = []
    for row in rows:
        residual = compute_residual(row)
        new_row = {**row, "residual_mm": f"{residual:.6f}"}
        out.append(new_row)
    return out


def write_residuals_csv(rows: list[dict], destination: Path) -> None:
    """Write the residuals table to ``destination`` as CSV."""
    if not rows:
        raise ValueError("no rows to write")
    destination.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with destination.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    here = Path(__file__).resolve().parent
    input_path = Path(args[0]) if len(args) >= 1 else here / "data" / "water_budget_2025.csv"
    output_path = Path(args[1]) if len(args) >= 2 else here / "outputs" / "residuals.csv"

    with input_path.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        print(f"error: no rows in {input_path}", file=sys.stderr)
        return 1

    rows_out = compute_residuals(rows)
    write_residuals_csv(rows_out, output_path)

    max_abs = max(abs(float(r["residual_mm"])) for r in rows_out)
    print(f"wrote {len(rows_out)} residual rows to {output_path}")
    print(f"max(|residual|) = {max_abs:.6f} mm  (tolerance: {RESIDUAL_TOL_MM} mm)")
    return 0 if max_abs < RESIDUAL_TOL_MM else 2


if __name__ == "__main__":
    raise SystemExit(main())
