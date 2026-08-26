# SPDX-License-Identifier: MIT
"""The three small tools that replace what the sweep removes.

Each carries one property the thing it replaces had, and these tests pin that
property rather than the output format. They import unconditionally: a tool
that has gone missing should error here, not skip.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]


def _load(name: str):
    path = CAIRN_ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_cairn_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


board = _load("board")
gauge = _load("gauge")
audit = _load("audit_report")


class TestTheBoardReadsHeadersAndJudgesNothing:
    """The board it replaces derived status, obligations and blockers. This one
    reports header fields, because a derived judgment printed beside a fact
    reads as a fact."""

    def test_it_lists_the_active_artifacts(self) -> None:
        rows = board._rows(CAIRN_ROOT, include_archive=False)
        assert rows, "no active artifacts found"
        assert {r["kind"] for r in rows} <= {"proposal", "plan"}

    def test_it_reports_only_fields_the_author_wrote(self, tmp_path) -> None:
        """A field the artifact does not carry must come back empty, not
        inferred. The failure this guards is a column that looks authored."""
        d = tmp_path / "dev" / "plans"
        d.mkdir(parents=True)
        (d / "example.md").write_text(
            "# Plan: example\n\n**Status**: implementing\n\n## Scope\n"
            "**Opened**: 2026-01-01\n", encoding="utf-8")
        rows = board._rows(tmp_path, include_archive=False)
        assert len(rows) == 1
        assert rows[0]["Status"] == "implementing"
        # Below the first heading, so not a header field.
        assert rows[0]["Opened"] == ""

    def test_long_values_are_encoded_and_elided(self) -> None:
        cell = board._encode(limit=20)
        assert len(cell("A" * 500)) == 20
        assert "͏" not in cell("͏")


class TestTheGaugeNeverBucketsWhatItCannotClassify:
    """The hand-built table could not be reproduced by an independent reader,
    which is the whole reason a classifier is committed. A rule that silently
    absorbed unknown paths would reintroduce exactly that opacity."""

    def test_an_unknown_path_is_unclassified_not_product(self) -> None:
        assert gauge.classify("some/path/nobody/ruled/on.txt") is None

    @pytest.mark.parametrize("path,expected", [
        ("dev/plans/x.md", "dev"),
        ("bootstrap/security_check.py", "security-machinery"),
        ("bootstrap/_scaffold/install.py", "other-machinery"),
        ("doctrine/rationale.md", "product"),
    ])
    def test_representative_paths_land_in_their_class(self, path, expected) -> None:
        assert gauge.classify(path) == expected

    def test_security_rules_win_over_the_broader_machinery_prefix(self) -> None:
        """`bootstrap/` would claim these too. First match wins, so rule order
        is the rule -- and a reordering that quietly reclassified the security
        column would move the number the gauge exists to report."""
        assert gauge.classify("bootstrap/tests/test_security_lint.py") == "security-machinery"
        assert gauge.classify("bootstrap/tests/test_upgrade.py") == "other-machinery"


class TestTheAuditSampleCannotBeChosenByItsSubject:
    """Whoever assembles an audit packet has every incentive to pick the
    tidiest artifacts. The sample is a hash of committed identity so it is
    reproducible by anyone and unchoosable by the party being audited."""

    def test_the_same_salt_draws_the_same_sample(self) -> None:
        stems = [f"artifact-{i}" for i in range(40)]
        assert audit._sample(stems, 5, "s") == audit._sample(stems, 5, "s")

    def test_a_different_salt_draws_a_different_sample(self) -> None:
        stems = [f"artifact-{i}" for i in range(40)]
        assert audit._sample(stems, 5, "s") != audit._sample(stems, 5, "t")

    def test_input_order_does_not_move_the_sample(self) -> None:
        """Otherwise the preparer chooses by choosing how to list."""
        stems = [f"artifact-{i}" for i in range(40)]
        assert audit._sample(stems, 5, "s") == audit._sample(list(reversed(stems)), 5, "s")


class TestTheAuditReporterDetectsAbsenceForRealReasons:
    """A checker that flags everything is as uninformative as one that flags
    nothing. These pin both directions."""

    def test_a_complete_change_raises_no_warning(self, tmp_path) -> None:
        p = tmp_path / "complete.md"
        p.write_text(
            "**Status**: archived\n**Risk**: low\n\n"
            "## Plan review -- someone -- 2026-01-01\n\n"
            "## Implementation verification -- someone -- 2026-01-02\n"
            "4596 passed, 3 failed\n", encoding="utf-8")
        assert audit._warnings(audit._facts(p)) == []

    def test_a_ledger_naming_no_numbers_is_flagged(self, tmp_path) -> None:
        """"Ran the suite" is a claim; a count is a record."""
        p = tmp_path / "vague.md"
        p.write_text(
            "**Status**: archived\n**Risk**: low\n\n"
            "## Plan review -- someone -- 2026-01-01\n\n"
            "## Implementation verification -- someone -- 2026-01-02\n"
            "Ran the full suite and it was fine.\n", encoding="utf-8")
        warns = audit._warnings(audit._facts(p))
        assert any("falsification output" in w for w in warns)

    def test_pending_is_an_accepted_outcome(self, tmp_path) -> None:
        """Whether a scientific change worked is usually not knowable at
        archive time. Without `pending` that answer is forced to be either
        falsely confident or silently absent."""
        p = tmp_path / "pending.md"
        p.write_text(
            "**Status**: pending -- revisit after the next field season\n"
            "**Risk**: low\n\n## Plan review -- someone -- 2026-01-01\n\n"
            "## Implementation verification -- someone -- 2026-01-02\n"
            "12 passed\n", encoding="utf-8")
        assert audit._warnings(audit._facts(p)) == []
