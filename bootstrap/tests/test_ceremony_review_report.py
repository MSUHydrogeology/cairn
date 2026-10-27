"""Tests for what the re-anchor ceremony shows its reader and what it scans.

The reader of a ceremony (a fresh agent, then the Maintainer) trusts the report
the checker prints and the scanners that run over the closure. These nodes pin
the scan coverage and the report's contents against planted lines and against
mutations of the real code, never against a restatement of its own logic.
"""
from __future__ import annotations

import sys
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import security_check  # noqa: E402
from bootstrap.tests import _gate_preflight as P  # noqa: E402


# ---------------------------------------------------------------------------
# scan coverage
# ---------------------------------------------------------------------------

def test_release_scan_covers_every_python_member_of_the_authority_closure() -> None:
    """The closure decides what a ceremony blesses and runs, yet lives under
    ``bootstrap/tests/``, which the scan globs skip on purpose. So the release
    scan names its Python members itself, and this node compares that list with
    the checker's own declared closure: a member added there and not scanned
    fails here. Two spellings on purpose -- the scan module cannot import test
    code, so only a test can hold them equal."""
    closure_py = {p for p in P.declared_authority_closure() if p.endswith(".py")}
    assert len(closure_py) == 7, closure_py
    scanned = set(security_check.scan_targets())
    missing = sorted(closure_py - scanned)
    assert not missing, f"closure members the release scan skips: {missing}"
    # and nothing else under bootstrap/tests/ rides along (attack fixtures)
    extra = sorted(t for t in scanned
                   if t.startswith("bootstrap/tests/") and t not in closure_py)
    assert not extra, extra
