"""The test absorbed by proposal 0001 -- 'a change absorbs its tests.'

The invariant the test pins is the mass-balance closure: every row's
residual must satisfy ``|residual| < RESIDUAL_TOL_MM``.  This is the
scientific contract; the synthetic input is constructed to satisfy it.

Run with: ``python -m pytest test_water_budget.py``.  Cairn does not
run this; your test framework does -- see ``../../docs/workflow-role.md``.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from water_budget import (  # noqa: E402
    RESIDUAL_TOL_MM,
    compute_residual,
    compute_residuals,
    main,
    write_residuals_csv,
)

DEFAULT_INPUT = HERE / "data" / "water_budget_2025.csv"


def _load_rows(csv_path: Path) -> list[dict]:
    with csv_path.open(newline="") as fh:
        return list(csv.DictReader(fh))


class TestMassBalanceInvariant:
    """The scientific contract: each row's residual is below tolerance."""

    def test_default_dataset_satisfies_invariant(self) -> None:
        rows = _load_rows(DEFAULT_INPUT)
        assert rows, "default dataset is empty"
        residuals = [compute_residual(r) for r in rows]
        max_abs = max(abs(r) for r in residuals)
        assert max_abs < RESIDUAL_TOL_MM, (
            f"mass-balance closure violated: max(|residual|) = {max_abs:.6f} mm "
            f">= {RESIDUAL_TOL_MM} mm.  Either the input dataset is unbalanced "
            "or the residual formula drifted from the documented mass-balance."
        )

    def test_residual_formula_signs_match_doctrine(self) -> None:
        """Pin the residual formula's sign convention.

        precip is a positive inflow; et, runoff, recharge are
        positive outflows; dS_storage is the observed storage change.
        Pumping the inputs through known cases catches sign-flip bugs.
        """
        # All zero -> residual 0.
        zero_row = {
            "month": "2099-00",
            "precip_mm": 0,
            "et_mm": 0,
            "runoff_mm": 0,
            "recharge_mm": 0,
            "dS_storage_mm": 0,
        }
        assert compute_residual(zero_row) == 0.0

        # precip alone, no losses, no storage change -> residual = +precip.
        precip_only = {**zero_row, "precip_mm": 50.0}
        assert compute_residual(precip_only) == 50.0

        # precip = et alone (closed) -> residual = 0.
        closed = {**zero_row, "precip_mm": 30.0, "et_mm": 30.0}
        assert compute_residual(closed) == 0.0


class TestResidualWriter:
    """Round-trip the residual writer through tmp_path."""

    def test_compute_then_write_round_trip(self, tmp_path: Path) -> None:
        rows = _load_rows(DEFAULT_INPUT)
        rows_with_residuals = compute_residuals(rows)
        dest = tmp_path / "outputs" / "residuals.csv"
        write_residuals_csv(rows_with_residuals, dest)
        # File exists, has the right header, and has the same row count.
        round_trip = _load_rows(dest)
        assert len(round_trip) == len(rows)
        assert "residual_mm" in round_trip[0]

    def test_cli_main_returns_zero_for_balanced_input(
        self, tmp_path: Path
    ) -> None:
        """The CLI's exit code is 0 when the mass-balance invariant holds."""
        output_csv = tmp_path / "residuals.csv"
        result = main([str(DEFAULT_INPUT), str(output_csv)])
        assert result == 0, (
            f"CLI returned {result} on balanced input; expected 0 "
            f"(should only return 2 when max|residual| >= {RESIDUAL_TOL_MM} mm)"
        )
        assert output_csv.exists()


@pytest.mark.parametrize(
    "broken_row",
    [
        # Precip too high -> positive residual.
        {"precip_mm": 200, "et_mm": 0, "runoff_mm": 0, "recharge_mm": 0, "dS_storage_mm": 0},
        # Storage change too small for inflow -> positive residual.
        {"precip_mm": 100, "et_mm": 0, "runoff_mm": 0, "recharge_mm": 0, "dS_storage_mm": 50},
    ],
)
def test_unbalanced_rows_exceed_tolerance(broken_row: dict) -> None:
    """A row that genuinely fails mass balance produces a residual
    above tolerance -- the invariant is not vacuous."""
    broken_row.setdefault("month", "2099-00")
    residual = compute_residual(broken_row)
    assert abs(residual) >= RESIDUAL_TOL_MM, (
        f"unbalanced row {broken_row} returned residual {residual}, "
        "which is below tolerance -- the invariant test would not catch this."
    )
