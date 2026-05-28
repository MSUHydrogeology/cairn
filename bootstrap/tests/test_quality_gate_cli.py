"""CLI contract tests for ``scripts/quality_gate.py``.

Pins:

* ``--sub <name>`` runs a single sub-gate; default runs all.
* ``--report`` emits TAB-separated machine-readable output.
* ``--root`` overrides the repo root.
* Bad ``--root`` exits 2 (usage error).
* ``--seed-list a,b,c`` parses; ``--seed-count N`` produces ``[0..N-1]``;
  ``--seed N`` produces ``[N]``; absent flags produce ``[0]``.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
QG_SRC = CAIRN_ROOT / "scripts" / "quality_gate.py"

pytestmark = pytest.mark.skipif(
    not QG_SRC.exists(), reason="quality_gate.py not available",
)


def _load_qg(name: str = "_quality_gate_under_test") -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, QG_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def qg() -> ModuleType:
    return _load_qg()


class TestArgs:
    def test_default_seed_is_single_zero(self, qg):
        ns = qg._build_arg_parser().parse_args([])
        assert qg._resolve_seeds(ns) == [0]

    def test_seed_single(self, qg):
        ns = qg._build_arg_parser().parse_args(["--seed", "7"])
        assert qg._resolve_seeds(ns) == [7]

    def test_seed_count(self, qg):
        ns = qg._build_arg_parser().parse_args(["--seed-count", "3"])
        assert qg._resolve_seeds(ns) == [0, 1, 2]

    def test_seed_list(self, qg):
        ns = qg._build_arg_parser().parse_args(["--seed-list", "11,42,7"])
        assert qg._resolve_seeds(ns) == [11, 42, 7]

    def test_seed_list_precedence_over_count(self, qg):
        ns = qg._build_arg_parser().parse_args([
            "--seed-list", "5,6", "--seed-count", "3", "--seed", "99",
        ])
        assert qg._resolve_seeds(ns) == [5, 6]


class TestExitCodes:
    def test_bad_root_exits_2(self, qg, tmp_path, capsys):
        not_a_dir = tmp_path / "nope"
        rc = qg.main(["--root", str(not_a_dir), "--sub", "neutrality"])
        assert rc == 2

    def test_clean_neutrality_subset_exits_0(self, qg, tmp_path, capsys):
        # An empty repo under the seven scan roots: zero findings -> 0.
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "ok.md").write_text(
            "# Clean prose with no vendor or project tokens.\n"
        )
        rc = qg.main([
            "--root", str(tmp_path), "--sub", "neutrality",
        ])
        assert rc == 0

    def test_neutrality_failure_exits_1(self, qg, tmp_path, capsys):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "leak.md").write_text(
            "# Some text mentioning Claude without exemption.\n"
        )
        rc = qg.main([
            "--root", str(tmp_path), "--sub", "neutrality",
        ])
        assert rc == 1


class TestReport:
    def test_machine_report_is_tab_separated(self, qg, tmp_path, capsys):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "leak.md").write_text(
            "Mention of Claude here.\n"
        )
        qg.main([
            "--root", str(tmp_path), "--sub", "neutrality", "--report",
        ])
        out = capsys.readouterr().out
        # Find the fail line; verify it has 4 tabs (5 fields).
        for line in out.splitlines():
            if line.startswith("neutrality\t"):
                fields = line.split("\t")
                assert len(fields) == 5, fields
                assert fields[1] == "fail"
                return
        pytest.fail("no neutrality fail finding in --report output")

    def test_default_report_groups_by_subgate(self, qg, tmp_path, capsys):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "ok.md").write_text("clean prose\n")
        qg.main([
            "--root", str(tmp_path), "--sub", "neutrality",
        ])
        out = capsys.readouterr().out
        # Per-sub-gate header always prints for sub-gates that ran,
        # even when zero findings -- so the user sees the gate
        # confirmed its scan, not silently skipped.
        assert "[neutrality]" in out
        assert "fail=0" in out
        assert "(no findings)" in out


class TestSubSelection:
    def test_sub_neutrality_only_runs_neutrality(self, qg, tmp_path, capsys):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "ok.md").write_text("clean prose\n")
        qg.main([
            "--root", str(tmp_path), "--sub", "neutrality",
        ])
        out = capsys.readouterr().out
        assert "[neutrality]" in out
        assert "[redundancy]" not in out
        assert "[order-independence]" not in out

    def test_sub_repeatable(self, qg, tmp_path, capsys):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "ok.md").write_text("clean prose\n")
        qg.main([
            "--root", str(tmp_path),
            "--sub", "neutrality", "--sub", "redundancy",
        ])
        out = capsys.readouterr().out
        assert "[neutrality]" in out
        assert "[redundancy]" in out
        assert "[order-independence]" not in out
