"""Tests for honest fan-out
report + real invitation).

* The install closing line names no command that is not installable (no
  phantom `/good-morning`) and names the real, always-works invocation.
* The `skipped-vendor-absent` fan-out status -- the *normal* first-install
  state (the harness's config dir doesn't exist until the adopter's first
  launch) -- is a calm, no-action advisory line, never silently dropped and
  never phrased as a fault ("skipped"/"error").

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_first_session_report.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import main  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent


def _scaffold(target: Path, extra_yaml: str = "") -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: FirstSessionTest\ntest_command: pytest\n"
        "modules: []\n" + extra_yaml,
        encoding="utf-8",
    )
    return main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])


def test_no_phantom_good_morning_and_names_the_real_invocation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    rc = _scaffold(tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "/good-morning" not in out
    assert "python tools/session.py session-start" in out


def test_skipped_vendor_absent_is_a_calm_no_action_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    """A fresh scaffold target has no `.claude/` directory yet, so the
    claude-code symlink-tier row hits skipped-vendor-absent -- the
    NORMAL first-install state, not a fault."""
    rc = _scaffold(tmp_path)
    assert rc == 0
    assert not (tmp_path / ".claude").exists()
    out = capsys.readouterr().out
    fanout_lines = [ln for ln in out.splitlines() if "Skills fan-out" in ln]
    assert fanout_lines, "expected at least one Skills fan-out line in the report"
    claude_lines = [ln for ln in fanout_lines if "claude-code" in ln]
    assert claude_lines, "expected a claude-code fan-out row to be printed, not dropped"
    for line in claude_lines:
        assert "skipped" not in line.lower()
        assert "error" not in line.lower()
        assert "no action needed" in line.lower()


def test_calm_advisory_is_idempotent_across_a_force_rerun(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    """A re-run (still no `.claude/`) keeps printing the same calm,
    no-action line -- not a first-run-only message, and never escalates
    to "skipped"/"error" phrasing on a repeat."""
    rc1 = _scaffold(tmp_path)
    assert rc1 == 0
    capsys.readouterr()  # discard first-run output
    rc2 = _scaffold(tmp_path, extra_yaml="")
    assert rc2 == 0
    out = capsys.readouterr().out
    claude_lines = [
        ln for ln in out.splitlines()
        if "Skills fan-out" in ln and "claude-code" in ln
    ]
    assert claude_lines, "expected the claude-code row on the re-run too"
    for line in claude_lines:
        assert "skipped" not in line.lower()
        assert "error" not in line.lower()
