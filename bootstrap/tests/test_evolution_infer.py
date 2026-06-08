"""Tests for evolution_infer.py -- the deterministic rate-limit-gate /
fold-up-backlog decision-support tool (self-evolution-loop Part B).

Covers:

* registration: the tool installs verbatim under the ``incident-trackers``
  module to ``tools/evolution_infer.py``;
* gate eval: ``>=threshold`` ``occurred`` rows of one event-class within the
  rolling window -> a suggestion; ``prevented`` / out-of-window rows excluded;
* fail-closed: an Incidents table with no parseable rolling window -> the gate
  is NOT evaluated and the tool exits 3 (no silent default);
* backlog: ``>=`` the backlog threshold of open ``candidate`` rows -> an alarm;
* only-suggests: the tool mutates nothing.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_evolution_infer.py
"""
from __future__ import annotations

import datetime
import importlib.util
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
TOOL_SRC = TEMPLATES_ROOT / "modules" / "default-on" / "evolution_infer.py"

sys.path.insert(0, str(CAIRN_ROOT))
from bootstrap.scaffold import _MODULE_MAPPINGS, main as scaffold_main  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)

_TODAY = datetime.date(2026, 6, 8)


@pytest.fixture()
def ei() -> ModuleType:
    spec = importlib.util.spec_from_file_location("evolution_infer_uut", TOOL_SRC)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["evolution_infer_uut"] = mod
    spec.loader.exec_module(mod)
    return mod


def _tracker(window_line: str, rows: list[tuple[str, str, str]]) -> str:
    body = (
        "# T\n\n" + window_line + "\n\n## What counts\n\n* class\n\n"
        "## Incidents\n\n"
        "| Date | Event Class | Description | Recurrence-Window Match "
        "| Impact | Migrated From Reflection | Resolved By |\n"
        "|---|---|---|---|---|---|---|\n"
    )
    for d, ec, imp in rows:
        body += f"| {d} | {ec} | desc | auto | {imp} | direct | pending |\n"
    return body


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

class TestRegistration:
    def test_tool_registered(self) -> None:
        specs = _MODULE_MAPPINGS["incident-trackers"]
        dsts = {s.dst: s for s in specs}
        assert "tools/evolution_infer.py" in dsts
        assert dsts["tools/evolution_infer.py"].verbatim is True

    def test_tool_installed_verbatim(self, tmp_path: Path) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: EvoTest\ntest_command: pytest\nmodules:\n"
            "  - incident-trackers\n"
        )
        rc = scaffold_main(
            ["--config", str(cfg), "--target", str(tmp_path),
             "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
        )
        assert rc == 0
        installed = tmp_path / "tools" / "evolution_infer.py"
        assert installed.is_file()
        assert installed.read_bytes() == TOOL_SRC.read_bytes()


# ---------------------------------------------------------------------------
# Gate evaluation
# ---------------------------------------------------------------------------

class TestGateEval:
    def test_two_occurred_in_window_suggests(self, ei) -> None:
        text = _tracker("**Rolling window**: 14 days.", [
            ("2026-06-05", "staged-index", "occurred"),
            ("2026-06-01", "staged-index", "occurred"),
            ("2026-05-01", "staged-index", "occurred"),   # outside window
            ("2026-06-06", "staged-index", "prevented"),  # not occurred
        ])
        window, findings = ei.evaluate_tracker(text, today=_TODAY, threshold=2)
        assert window == 14
        assert len(findings) == 1
        assert findings[0]["event_class"] == "staged-index"
        assert findings[0]["count"] == 2

    def test_one_occurred_no_suggestion(self, ei) -> None:
        text = _tracker("**Rolling window**: 14 days.",
                        [("2026-06-05", "x", "occurred")])
        _w, findings = ei.evaluate_tracker(text, today=_TODAY, threshold=2)
        assert findings == []

    def test_weeks_unit_parsed(self, ei) -> None:
        assert ei.parse_rolling_window("**Rolling window**: 2 weeks.") == 14
        assert ei.parse_rolling_window("**Rolling window**: 7 days") == 7
        assert ei.parse_rolling_window("**Rolling window**: 21") == 21

    def test_unparseable_window_is_fail_closed(self, ei) -> None:
        assert ei.parse_rolling_window("no window here") is None
        text = _tracker("(no window line)",
                        [("2026-06-05", "z", "occurred"),
                         ("2026-06-06", "z", "occurred")])
        window, findings = ei.evaluate_tracker(text, today=_TODAY, threshold=2)
        assert window is None       # fail-closed signal
        assert findings == []

    def test_main_fail_closed_exits_3(self, ei, tmp_path) -> None:
        (tmp_path / "dev" / "measurement").mkdir(parents=True)
        (tmp_path / "dev" / "measurement" / "collision_log.md").write_text(
            _tracker("(no window line)",
                     [("2026-06-05", "z", "occurred"),
                      ("2026-06-06", "z", "occurred")])
        )
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path)])
        assert rc == 3                       # fail-closed exit
        assert "FAIL-CLOSED" in out.getvalue()
        assert "Rolling window" in out.getvalue()

    def test_main_suggests_and_json(self, ei, tmp_path) -> None:
        (tmp_path / "dev" / "measurement").mkdir(parents=True)
        (tmp_path / "dev" / "measurement" / "collision_log.md").write_text(
            _tracker("**Rolling window**: 14 days.", [
                ("2026-06-05", "staged-index", "occurred"),
                ("2026-06-01", "staged-index", "occurred"),
            ])
        )
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path), "--json"])
        assert rc == 0
        payload = json.loads(out.getvalue())
        assert len(payload["findings"]) == 1
        assert payload["findings"][0]["count"] == 2

    def test_file_without_incidents_table_skipped(self, ei, tmp_path) -> None:
        (tmp_path / "dev" / "measurement").mkdir(parents=True)
        # A doc with no '## Incidents' table is not an incident tracker.
        (tmp_path / "dev" / "measurement" / "notes.md").write_text(
            "# Notes\n\nNo incidents table here.\n"
        )
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path)])
        assert rc == 0          # not fail-closed -- simply skipped


# ---------------------------------------------------------------------------
# Fold-up backlog
# ---------------------------------------------------------------------------

class TestBacklog:
    def _ledger(self, n_candidates: int) -> str:
        body = (
            "## Open candidates\n\n"
            "| Candidate | Type | Size | Status | Source |\n"
            "|---|---|---|---|---|\n"
        )
        for i in range(n_candidates):
            body += f"| c{i} | tooling | small | candidate | src |\n"
        body += "| done | tooling | small | filed -> #1 | src |\n"  # not counted
        return body

    def test_count_open_candidates(self, ei) -> None:
        assert ei.count_open_candidates(self._ledger(3)) == 3

    def test_backlog_alarm_fires(self, ei, tmp_path) -> None:
        (tmp_path / "dev" / ".cairn").mkdir(parents=True)
        (tmp_path / "dev" / ".cairn" / "cairn_foldback.md").write_text(
            self._ledger(5)
        )
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path), "--backlog-threshold", "5"])
        assert rc == 0
        assert "FOLD-UP BACKLOG ALARM" in out.getvalue()

    def test_backlog_under_threshold_no_alarm(self, ei, tmp_path) -> None:
        (tmp_path / "dev" / ".cairn").mkdir(parents=True)
        (tmp_path / "dev" / ".cairn" / "cairn_foldback.md").write_text(
            self._ledger(2)
        )
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path), "--backlog-threshold", "10"])
        assert rc == 0
        assert "FOLD-UP BACKLOG ALARM" not in out.getvalue()


# ---------------------------------------------------------------------------
# Only-suggests invariant
# ---------------------------------------------------------------------------

class TestOnlySuggests:
    def test_no_file_mutation(self, ei, tmp_path) -> None:
        (tmp_path / "dev" / "measurement").mkdir(parents=True)
        tracker = tmp_path / "dev" / "measurement" / "collision_log.md"
        tracker.write_text(_tracker("**Rolling window**: 14 days.", [
            ("2026-06-05", "x", "occurred"),
            ("2026-06-01", "x", "occurred"),
        ]))
        before = tracker.read_bytes()
        out = io.StringIO()
        with redirect_stdout(out):
            ei.main(["--root", str(tmp_path)])
        assert tracker.read_bytes() == before  # unchanged: emits text only
