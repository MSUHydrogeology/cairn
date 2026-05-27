"""Tests for the fail-closed release security check (security-hardening Chunk 7).

``bootstrap/security_check.py`` is the release-facing counterpart to the dev
Bandit gate: where the gate *skips* when Bandit is absent locally, the
release check **fails closed** -- release evidence must be unskippable (R1).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import security_check  # noqa: E402


def _bandit_available() -> bool:
    try:
        import bandit  # noqa: F401
    except ImportError:
        return False
    return True


def test_scan_targets_are_explicit_files_covering_shipped_surface() -> None:
    targets = set(security_check.scan_targets())
    assert "bootstrap/scaffold.py" in targets
    assert "templates/modules/team-gated/link_check.py" in targets
    # content_scan is single-sourced as the content-security module script.
    assert "templates/modules/team-gated/content_scan.py" in targets
    # Explicit files only -- no bare directory (the no-`-r` footgun).
    assert all(t.endswith(".py") for t in targets), targets


def test_fail_closed_when_bandit_absent(monkeypatch) -> None:
    """A missing Bandit FAILS (nonzero), unlike the dev gate's local skip --
    release evidence is unskippable (R1)."""
    class _Proc:
        returncode = 127
        stdout = ""
        stderr = "No module named bandit"

    monkeypatch.setattr(security_check.subprocess, "run",
                        lambda *a, **k: _Proc())
    assert security_check.run_bandit() == 1


def test_fail_closed_on_scanner_error(monkeypatch) -> None:
    class _Proc:
        returncode = 2
        stdout = ""
        stderr = "bandit: config error"

    monkeypatch.setattr(security_check.subprocess, "run",
                        lambda *a, **k: _Proc())
    assert security_check.run_bandit() == 1


@pytest.mark.skipif(not _bandit_available(), reason="bandit not installed")
def test_run_bandit_clean_with_bandit_present() -> None:
    # The shipped surface is clean of unallowlisted MEDIUM+ after Chunks 1-3.
    assert security_check.run_bandit() == 0
