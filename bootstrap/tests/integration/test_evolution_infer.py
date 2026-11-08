"""Tests for evolution_infer.py -- the deterministic rate-limit-gate /
decision-support tool (self-evolution-loop Part B).

Promises:

- Public JSON suggestions count only occurred events inside the rolling
  window and at or above the class threshold.
- Missing or invalid windows fail closed, and the tool only suggests without
  mutating tracker files.

Covers:

* registration: the tool installs verbatim under the ``incident-trackers``
  module to ``tools/evolution_infer.py``;
* gate eval: ``>=threshold`` ``occurred`` rows of one event-class within the
  rolling window -> a suggestion; ``prevented`` / out-of-window rows excluded;
* fail-closed: an Incidents table with no parseable rolling window -> the gate
  is NOT evaluated and the tool exits 3 (no silent default);
* only-suggests: the tool mutates nothing.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/integration/test_evolution_infer.py
"""
from __future__ import annotations

import datetime
import importlib.util
import io
import json
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
TOOL_SRC = TEMPLATES_ROOT / "modules" / "default-on" / "evolution_infer.py"

sys.path.insert(0, str(CAIRN_ROOT))
from bootstrap.scaffold import _MODULE_MAPPINGS, main as scaffold_main  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)

_TODAY = datetime.date(2026, 6, 8)


def _recent(days_ago: int) -> str:
    """An incident date anchored to the *real* clock, for the ``main()`` path.

    ``evaluate_tracker`` takes an injectable ``today=``, so tests that call it
    pin ``_TODAY`` and stay hermetic.  ``main()`` resolves its own ``today``
    from ``datetime.date.today()`` and exposes no injection point, so any test
    exercising it must anchor its rows to the real clock -- a fixed date here
    silently ages out of the rolling window and the test starts failing purely
    because time passed (it did: 2026-06-05/-06-01 rows against a 14-day
    window).  Keep ``days_ago`` well inside the narrowest window under test.
    """
    return (datetime.date.today() - datetime.timedelta(days=days_ago)).isoformat()


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


def _sweep_tracker(rows: list[tuple[str, str, str, str]]) -> str:
    """Build a tracker with occurrence date, commit grouping and confirmation."""
    body = (
        "# Collision log\n\n**Rolling window**: 14 days.\n\n"
        "## What counts\n\n* `same-file-sweep`\n\n"
        "## Unconfirmed reports\n\n"
        "| Date | Event Class | Claim | Impact |\n|---|---|---|---|\n"
        f"| {_recent(0)} | same-file-sweep | claim only | occurred |\n\n"
        "## Incidents\n\n"
        "| Date | Event Class | Description | Recurrence-Window Match "
        "| Impact | Migrated From Reflection | Resolved By | Commit | "
        "Affected Paths | Discovery Date | Confirmation Reference |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
    )
    for occurrence, commit, paths, impact in rows:
        body += (
            f"| {occurrence} | same-file-sweep | confirmed sweep | auto | "
            f"{impact} | direct | pending | {commit} | {paths} | "
            f"{_recent(0)} | local author confirmation |\n"
        )
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

    def test_installed_tool_discloses_reporting_limit(
            self, tmp_path: Path) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: EvoTest\ntest_command: pytest\nmodules:\n"
            "  - incident-trackers\n"
        )
        assert scaffold_main(
            ["--config", str(cfg), "--target", str(tmp_path),
             "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
        ) == 0
        tracker = tmp_path / "dev" / "measurement" / "collision_log.md"
        tracker.parent.mkdir(parents=True, exist_ok=True)
        tracker.write_text(_sweep_tracker([]))
        installed = tmp_path / "tools" / "evolution_infer.py"
        result = subprocess.run(
            [sys.executable, str(installed), "--root", str(tmp_path)],
            check=False, capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "REPORTING LIMIT" in result.stdout
        assert "cannot detect unreported incidents" in result.stdout


# ---------------------------------------------------------------------------
# Gate evaluation
# ---------------------------------------------------------------------------

class TestGateEval:
    def test_two_occurred_in_window_suggests(self, ei, tmp_path) -> None:
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

        (tmp_path / "dev" / "measurement").mkdir(parents=True)
        tracker = tmp_path / "dev" / "measurement" / "collision_log.md"
        tracker.write_text(_tracker("**Rolling window**: 14 days.", [
            (_recent(1), "staged-index", "occurred"),
            (_recent(3), "staged-index", "occurred"),
            (_recent(40), "staged-index", "occurred"),
            (_recent(2), "staged-index", "prevented"),
        ]))
        before = tracker.read_bytes()
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path), "--json"])
        assert rc == 0
        payload = json.loads(out.getvalue())
        assert payload["trackers_read"][0]["occurred_in_window"] == 2
        assert len(payload["findings"]) == 1
        assert payload["findings"][0]["event_class"] == "staged-index"
        assert payload["findings"][0]["count"] == 2
        assert tracker.read_bytes() == before

    def test_one_occurred_no_suggestion(self, ei) -> None:
        text = _tracker("**Rolling window**: 14 days.",
                        [("2026-06-05", "x", "occurred")])
        _w, findings = ei.evaluate_tracker(text, today=_TODAY, threshold=2)
        assert findings == []

    def test_weeks_unit_parsed(self, ei) -> None:
        assert ei.parse_rolling_window("**Rolling window**: 2 weeks.") == 14
        assert ei.parse_rolling_window("**Rolling window**: 7 days") == 7
        assert ei.parse_rolling_window("**Rolling window**: 21") == 21

    def test_nonpositive_window_is_fail_closed(self, ei) -> None:
        # Zero and negative windows fail closed (no silent positive coercion).
        assert ei.parse_rolling_window("**Rolling window**: 0 days") is None
        assert ei.parse_rolling_window("**Rolling window**: -3 days") is None

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
                (_recent(1), "staged-index", "occurred"),
                (_recent(3), "staged-index", "occurred"),
                (_recent(40), "staged-index", "occurred"),
                (_recent(2), "staged-index", "prevented"),
            ])
        )
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path), "--json"])
        assert rc == 0
        payload = json.loads(out.getvalue())
        assert len(payload["findings"]) == 1
        assert payload["findings"][0]["count"] == 2

    def test_real_main_counts_confirmed_commits_not_paths(self, ei, tmp_path) -> None:
        tracker = tmp_path / "dev" / "measurement" / "collision_log.md"
        tracker.parent.mkdir(parents=True)
        tracker.write_text(_sweep_tracker([
            (_recent(1), "commit-a", "plan.md, proposal.md", "occurred"),
        ]))
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path), "--json"])
        payload = json.loads(out.getvalue())
        assert rc == 0
        assert payload["findings"] == []

        tracker.write_text(_sweep_tracker([
            (_recent(1), "commit-a", "plan.md, proposal.md", "occurred"),
            (_recent(2), "commit-b", "coordination.md", "occurred"),
        ]))
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path), "--json"])
        payload = json.loads(out.getvalue())
        assert rc == 0
        assert [(f["event_class"], f["count"])
                for f in payload["findings"]] == [("same-file-sweep", 2)]
        assert payload["reporting"]["complete"] is False
        assert payload["reporting"]["basis"] == "reported tracker rows only"

    def test_prevented_uncertain_and_late_discovery_do_not_inflate_count(
            self, ei, tmp_path) -> None:
        tracker = tmp_path / "dev" / "measurement" / "collision_log.md"
        tracker.parent.mkdir(parents=True)
        tracker.write_text(_sweep_tracker([
            (_recent(1), "commit-a", "plan.md, proposal.md", "occurred"),
            (_recent(2), "commit-b", "coordination.md", "prevented"),
            (_recent(20), "commit-c", "old.md", "occurred"),
        ]))
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path), "--json"])
        payload = json.loads(out.getvalue())
        assert rc == 0
        assert payload["findings"] == []
        assert payload["trackers_read"][0]["occurred_in_window"] == 1

    def test_s2_prevented_mutation_removes_threshold_finding(
            self, ei, tmp_path) -> None:
        tracker = tmp_path / "dev" / "measurement" / "collision_log.md"
        tracker.parent.mkdir(parents=True)
        rows = [
            (_recent(1), "commit-a", "plan.md, proposal.md", "occurred"),
            (_recent(2), "commit-b", "coordination.md", "occurred"),
        ]
        tracker.write_text(_sweep_tracker(rows))
        control = io.StringIO()
        with redirect_stdout(control):
            assert ei.main(["--root", str(tmp_path), "--json"]) == 0
        assert len(json.loads(control.getvalue())["findings"]) == 1

        rows[1] = (*rows[1][:3], "prevented")
        tracker.write_text(_sweep_tracker(rows))
        mutated = io.StringIO()
        with redirect_stdout(mutated):
            assert ei.main(["--root", str(tmp_path), "--json"]) == 0
        assert json.loads(mutated.getvalue())["findings"] == []

    def test_human_output_discloses_incomplete_reporting(self, ei, tmp_path) -> None:
        tracker = tmp_path / "dev" / "measurement" / "collision_log.md"
        tracker.parent.mkdir(parents=True)
        tracker.write_text(_sweep_tracker([]))
        out = io.StringIO()
        with redirect_stdout(out):
            assert ei.main(["--root", str(tmp_path)]) == 0
        assert "REPORTING LIMIT" in out.getvalue()
        assert "cannot detect unreported incidents" in out.getvalue()

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


class TestUnreadableTrackersFailClosed:
    """A tracker the gate cannot read must never look like a tracker with
    nothing to report: both used to print 'none' and exit 0."""

    @staticmethod
    def _write(tmp_path: Path, name: str, text: str) -> None:
        d = tmp_path / "dev" / "measurement"
        d.mkdir(parents=True, exist_ok=True)
        (d / name).write_text(text)

    def test_incidents_table_without_an_impact_column(self, ei, tmp_path) -> None:
        self._write(tmp_path, "hazard_log.md",
                    "# H\n\n**Rolling window**: 14 days.\n\n## Incidents\n\n"
                    "| Date | Event Class | Brief | Recovery |\n|---|---|---|---|\n"
                    f"| {_recent(1)} | x (occurred) | a | b |\n")
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path), "--json"])
        assert rc == 3
        payload = json.loads(out.getvalue())
        assert payload["fail_closed_trackers"] == ["dev/measurement/hazard_log.md"]
        assert "Impact" in payload["fail_closed_reasons"][
            "dev/measurement/hazard_log.md"]

    def test_a_named_tracker_with_no_incidents_table(self, ei, tmp_path) -> None:
        self._write(tmp_path, "hazard_log.md",
                    "# H\n\n| Date | Event class | Brief |\n|---|---|---|\n")
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path),
                          "--trackers", "dev/measurement/hazard_log.md"])
        assert rc == 3
        assert "no '## Incidents' table" in out.getvalue()

    def test_columns_are_read_by_name_not_position(self, ei, tmp_path) -> None:
        self._write(tmp_path, "collision_log.md",
                    "# C\n\n**Rolling window**: 14 days.\n\n## Incidents\n\n"
                    "| Impact | Event Class | Date |\n|---|---|---|\n"
                    f"| occurred | staged-index | {_recent(1)} |\n"
                    f"| occurred | staged-index | {_recent(2)} |\n"
                    f"| occurred | staged-index | {_recent(40)} |\n")
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path), "--json"])
        assert rc == 0
        payload = json.loads(out.getvalue())
        assert [f["count"] for f in payload["findings"]] == [2]
        # The 40-day-old row is a row, but not one inside the window.
        assert payload["trackers_read"] == [{
            "tracker": "dev/measurement/collision_log.md", "rows": 3,
            "occurred_in_window": 2, "window_days": 14}]


class TestDiscoveryNamesWhatItSkipped:
    """In discovery -- the mode session-start runs -- a file with no
    '## Incidents' table is not a tracker and does not fail closed. But a
    skipped file must be named, and a run that read nothing must not print a
    bare 'none': an adopter whose tracker lacks the heading would otherwise
    read an unevaluated gate as a clean one."""

    @staticmethod
    def _issue_shaped(tmp_path: Path) -> None:
        d = tmp_path / "dev" / "measurement"
        d.mkdir(parents=True, exist_ok=True)
        (d / "hazard_log.md").write_text(
            "# Hazards\n\n| Date | Event class | Brief | Recovery / outcome |\n"
            f"|---|---|---|---|\n| {_recent(1)} | x | a | b |\n")

    def test_a_skipped_file_is_named(self, ei, tmp_path) -> None:
        self._issue_shaped(tmp_path)
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path), "--json"])
        assert rc == 0
        payload = json.loads(out.getvalue())
        assert payload["trackers_skipped"] == ["dev/measurement/hazard_log.md"]
        assert payload["trackers_read"] == []

    def test_reading_nothing_is_not_reported_as_a_clean_none(
            self, ei, tmp_path) -> None:
        self._issue_shaped(tmp_path)
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path)])
        text = out.getvalue()
        assert rc == 0
        assert "SKIPPED (1)" in text
        assert "dev/measurement/hazard_log.md" in text
        assert "RATE-LIMIT SUGGESTIONS: none.\n" not in text
        assert "no incident tracker was read" in text

    def test_a_read_tracker_still_prints_a_plain_none(
            self, ei, tmp_path) -> None:
        d = tmp_path / "dev" / "measurement"
        d.mkdir(parents=True)
        (d / "collision_log.md").write_text(
            _tracker("**Rolling window**: 14 days.",
                     [(_recent(1), "x", "occurred")]))
        out = io.StringIO()
        with redirect_stdout(out):
            rc = ei.main(["--root", str(tmp_path)])
        assert rc == 0
        assert "RATE-LIMIT SUGGESTIONS: none.\n" in out.getvalue()
        assert "SKIPPED" not in out.getvalue()


# ---------------------------------------------------------------------------
# Only-suggests invariant
# ---------------------------------------------------------------------------

class TestOnlySuggests:
    def test_no_file_mutation(self, ei, tmp_path) -> None:
        (tmp_path / "dev" / "measurement").mkdir(parents=True)
        tracker = tmp_path / "dev" / "measurement" / "collision_log.md"
        tracker.write_text(_tracker("**Rolling window**: 14 days.", [
            (_recent(1), "x", "occurred"),
            (_recent(3), "x", "occurred"),
        ]))
        before = tracker.read_bytes()
        out = io.StringIO()
        with redirect_stdout(out):
            ei.main(["--root", str(tmp_path)])
        assert tracker.read_bytes() == before  # unchanged: emits text only
