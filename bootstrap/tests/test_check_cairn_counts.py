"""check_cairn runs the verify_counts live-invariant lens (follow-up to
the numeric-claim Arm-3 fold-up).

Pins the wiring: a doc annotated ``<count> <!-- verify: <key> -->`` is
re-measured on every Cairn self-check -- a drifted number or an
unregistered key becomes a check_cairn flag, while a current number and
an un-annotated file pass clean.  The "current" value is computed from
the live registry (not hard-coded) so the test does not drift when
``claim_check.py`` legitimately changes size.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_check_cairn_counts.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT / "scripts"))

import check_cairn  # noqa: E402

_SEED_KEY = "claim_check_watch_file_lines"


def _count_flags(result) -> list:
    return [f for f in result.flags if f.kind.startswith("count-")]


@pytest.fixture(scope="module")
def measured() -> int:
    """The live measurement of the seed invariant (computed, not hard-coded)."""
    entry = check_cairn.measurements.REGISTRY[_SEED_KEY]
    return check_cairn.measurements.measure(entry)


class TestCheckCairnCountLens:
    def test_current_annotation_passes(self, tmp_path, measured):
        md = tmp_path / "docs" / "x.md"
        md.parent.mkdir(parents=True)
        md.write_text(f"the watch file is {measured} `<!-- verify: {_SEED_KEY} -->`")
        result = check_cairn.check_tree(tmp_path, [md])
        assert _count_flags(result) == []

    def test_drifted_annotation_flags(self, tmp_path, measured):
        md = tmp_path / "docs" / "x.md"
        md.parent.mkdir(parents=True)
        md.write_text(
            f"the watch file is {measured + 1} `<!-- verify: {_SEED_KEY} -->`"
        )
        result = check_cairn.check_tree(tmp_path, [md])
        flags = _count_flags(result)
        assert len(flags) == 1
        assert flags[0].kind == "count-drift"

    def test_unregistered_key_is_refused(self, tmp_path):
        md = tmp_path / "docs" / "x.md"
        md.parent.mkdir(parents=True)
        md.write_text("5 `<!-- verify: not_a_real_key -->`")
        result = check_cairn.check_tree(tmp_path, [md])
        flags = _count_flags(result)
        assert len(flags) == 1
        assert flags[0].kind == "count-refused"

    def test_unannotated_file_is_a_noop(self, tmp_path):
        md = tmp_path / "docs" / "x.md"
        md.parent.mkdir(parents=True)
        md.write_text("plain prose with a number 42 and no annotation.\n")
        result = check_cairn.check_tree(tmp_path, [md])
        assert _count_flags(result) == []
