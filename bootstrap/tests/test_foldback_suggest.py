"""Tests for the foldback_suggest helper.

Pins the four ``deferred-until`` cases the plan-review N3 disposition
called for (future-date / past-date / empty / condition-string), plus
ledger-shape smoke tests (empty ledger; ledger with no `candidate`
rows; ledger with mixed old- + new-vocab rows).

The helper itself is read-only; these tests treat it as a pure
classifier over a fixture ledger.
"""
from __future__ import annotations

import datetime
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
HELPER_SRC = (
    CAIRN_ROOT / "templates" / "modules" / "default-on" / "foldback_suggest.py"
)

pytestmark = pytest.mark.skipif(
    not HELPER_SRC.exists(),
    reason="foldback_suggest.py not available",
)


def _load_helper(name: str = "_foldback_suggest_under_test") -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, HELPER_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def fs() -> ModuleType:
    return _load_helper()


def _ledger_with_table(rows: str) -> str:
    """Build a fixture ledger string with the given table rows
    embedded between the "Open candidates" heading + the standard
    table header.
    """
    return (
        "# Fixture ledger\n\n"
        "## Open candidates\n\n"
        "| Candidate | Type | Size | Status | Source |\n"
        "|---|---|---|---|---|\n"
        f"{rows}"
        "\n## Already synced\n\n"
        "(empty)\n"
    )


# ---------------------------------------------------------------------------
# Four deferred-until cases (per plan-review N3 + N4 acceptance)
# ---------------------------------------------------------------------------


class TestDeferredUntilCases:
    """The four shapes the surfacing protocol must handle."""

    def test_future_iso_date_is_NOT_surfaced(self, fs):
        # Row with deferred-until in the future -- snoozed.
        future = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
        rows = (
            f"| **Cand A** | tooling | small | candidate | "
            f"some source; deferred-until: {future} |\n"
        )
        candidates = fs.parse_open_candidates(_ledger_with_table(rows))
        classified = fs.classify_rows(candidates)
        assert len(classified) == 1
        assert classified[0].surfaceable is False
        assert "snoozed" in classified[0].skip_reason

    def test_past_iso_date_IS_surfaced(self, fs):
        # Row with deferred-until in the past -- snooze expired.
        past = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
        rows = (
            f"| **Cand B** | doctrine | medium | candidate | "
            f"some source; deferred-until: {past} |\n"
        )
        candidates = fs.parse_open_candidates(_ledger_with_table(rows))
        classified = fs.classify_rows(candidates)
        assert len(classified) == 1
        assert classified[0].surfaceable is True, classified[0].skip_reason

    def test_empty_deferred_until_IS_surfaced(self, fs):
        # Row with no deferred-until field -- surfaceable by default.
        rows = (
            "| **Cand C** | tooling | small | candidate | "
            "some source (no defer) |\n"
        )
        candidates = fs.parse_open_candidates(_ledger_with_table(rows))
        classified = fs.classify_rows(candidates)
        assert len(classified) == 1
        assert classified[0].surfaceable is True

    def test_condition_string_is_NOT_surfaced(self, fs):
        # Row with a free-form condition string -- maintainer judges
        # manually; the helper does not surface automatically.
        rows = (
            "| **Cand D** | doctrine | medium | candidate | "
            "some source; deferred-until: after Cairn 0.3 self-host |\n"
        )
        candidates = fs.parse_open_candidates(_ledger_with_table(rows))
        classified = fs.classify_rows(candidates)
        assert len(classified) == 1
        assert classified[0].surfaceable is False
        assert "condition string" in classified[0].skip_reason


# ---------------------------------------------------------------------------
# Ledger-shape smoke tests
# ---------------------------------------------------------------------------


class TestLedgerShapes:
    def test_empty_ledger_is_no_op(self, fs):
        # Ledger with no Open candidates section -- empty result.
        text = "# Empty\n\nNo Open candidates section here.\n"
        candidates = fs.parse_open_candidates(text)
        assert candidates == []
        classified = fs.classify_rows(candidates)
        assert classified == []

    def test_ledger_with_no_candidate_rows_is_empty(self, fs):
        # Section exists, table exists, but every row's status is
        # not "candidate" (e.g. all filed / scoped already).
        rows = (
            "| **X** | tooling | small | filed -> #42 | s1 |\n"
            "| **Y** | doctrine | medium | scoped -> v0.3 | s2 |\n"
            "| **Z** | tooling | small | dropped | s3 |\n"
        )
        candidates = fs.parse_open_candidates(_ledger_with_table(rows))
        assert len(candidates) == 3
        classified = fs.classify_rows(candidates)
        assert all(not c.surfaceable for c in classified), (
            "non-candidate rows should not surface"
        )

    def test_mixed_old_and_new_vocab_handled(self, fs):
        # Per the doctrine's migration rule: existing ledgers with
        # old vocab (queued / scoped / synced / dropped) work as-is;
        # only `candidate` surfaces, regardless of what other rows
        # carry.
        rows = (
            "| **A** | doctrine | small | candidate | new |\n"
            "| **B** | doctrine | medium | queued | old-vocab |\n"
            "| **C** | doctrine | small | filed -> #1 | new-vocab |\n"
            "| **D** | doctrine | small | candidate | new |\n"
        )
        candidates = fs.parse_open_candidates(_ledger_with_table(rows))
        classified = fs.classify_rows(candidates)
        surfaceable = [c for c in classified if c.surfaceable]
        assert len(surfaceable) == 2, (
            f"expected exactly the 2 `candidate` rows; got: "
            f"{[(c.candidate, c.surfaceable) for c in classified]}"
        )

    def test_no_open_candidates_section(self, fs):
        # No section heading at all.
        text = "# Just some prose\n\nNothing else here.\n"
        candidates = fs.parse_open_candidates(text)
        assert candidates == []


# ---------------------------------------------------------------------------
# Live-ledger smoke test (dogfood against modflow_tools' actual ledger)
# ---------------------------------------------------------------------------


class TestLiveLedgerSmoke:
    """A weak smoke test against the actual modflow_tools ledger.
    Skipped if the file is not present (e.g., the test runs in a
    fresh-checkout context that doesn't include modflow_tools).
    """

    @pytest.fixture
    def live_ledger(self):
        # Look one level up from Cairn checkout, in case modflow_tools
        # sits as a sibling.  Fall back to the modflow_tools-deployed
        # ledger if findable.
        candidates = [
            CAIRN_ROOT.parent / "modflow_tools"
            / "dev" / "upstream" / "cairn_ledger.md",
        ]
        for p in candidates:
            if p.is_file():
                return p
        pytest.skip("live ledger not available in this checkout")

    def test_live_ledger_parses_without_error(self, fs, live_ledger):
        text = live_ledger.read_text(encoding="utf-8")
        candidates = fs.parse_open_candidates(text)
        # Smoke: parsed at least one row (the ledger is documented
        # to have at least one open candidate at most times).
        # Tolerate zero rows -- the ledger could be empty between
        # captures.
        classified = fs.classify_rows(candidates)
        # The classifier must not raise on real-world data; the
        # presence of any row doesn't matter for this smoke.
        assert isinstance(classified, list)


# ---------------------------------------------------------------------------
# CLI smoke
# ---------------------------------------------------------------------------


class TestCLI:
    def test_missing_ledger_returns_2(self, fs, tmp_path):
        rc = fs.main(["--ledger", str(tmp_path / "does-not-exist.md")])
        assert rc == 2

    def test_clean_ledger_returns_0(self, fs, tmp_path, capsys):
        ledger = tmp_path / "ledger.md"
        ledger.write_text(_ledger_with_table(""))
        rc = fs.main(["--ledger", str(ledger)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "Surfaceable candidates: 0" in out

    def test_json_output_is_parseable(self, fs, tmp_path, capsys):
        import json
        ledger = tmp_path / "ledger.md"
        ledger.write_text(_ledger_with_table(
            "| **X** | tooling | small | candidate | source |\n"
        ))
        rc = fs.main(["--ledger", str(ledger), "--json"])
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out)
        assert isinstance(payload, list)
        assert len(payload) == 1
        assert payload[0]["surfaceable"] is True

    def test_all_flag_includes_snoozed(self, fs, tmp_path, capsys):
        future = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
        ledger = tmp_path / "ledger.md"
        ledger.write_text(_ledger_with_table(
            f"| **Snoozed** | tooling | small | candidate | s; deferred-until: {future} |\n"
            "| **Ready** | doctrine | medium | candidate | s2 |\n"
        ))
        # Default (without --all): only Ready surfaces.
        rc = fs.main(["--ledger", str(ledger)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "Surfaceable candidates: 1" in out
        # With --all: shows both, classifying the snoozed one as not-
        # surfaceable.
        rc2 = fs.main(["--ledger", str(ledger), "--all"])
        assert rc2 == 0
        out2 = capsys.readouterr().out
        assert "Skipped rows" in out2
