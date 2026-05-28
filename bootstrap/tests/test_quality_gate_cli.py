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


class TestReportFlattenNewlines:
    """P2 code-review regression: machine-mode `--report` promises
    one-finding-per-line TAB-separated output, but a multi-line finding
    message (e.g. order-independence echoes pytest stderr) used to
    break that contract by emitting raw newlines.  Now newlines are
    `\\n`-escaped in machine mode; the regression test drives a
    failing order-independence fixture through `main(... --report)`
    and asserts every output line begins with a sub-gate token.
    """

    def _write_failing_fixture_suite(self, target: Path) -> None:
        (target / "_fixture_tests").mkdir()
        (target / "_fixture_tests" / "conftest.py").write_text(
            "def pytest_addoption(parser):\n"
            "    parser.addoption('--quality-gate-shuffle-seed',\n"
            "                     action='store', default=None, type=int)\n"
            "\n"
            "def pytest_collection_modifyitems(config, items):\n"
            "    import random\n"
            "    seed = config.getoption('--quality-gate-shuffle-seed')\n"
            "    if seed is None: return\n"
            "    random.Random(seed).shuffle(items)\n"
        )
        (target / "_fixture_tests" / "test_fail.py").write_text(
            "def test_a(): assert False, 'multi\\nline\\nfailure'\n"
        )

    def test_report_flattens_multiline_failure_message(
        self, qg, tmp_path, capsys,
    ):
        self._write_failing_fixture_suite(tmp_path)
        rc = qg.main([
            "--root", str(tmp_path), "--sub", "order-independence",
            "--seed", "0", "--test-dir", "_fixture_tests", "--report",
        ])
        assert rc == 1  # failure propagates
        out = capsys.readouterr().out
        sub_gate_tokens = {"order-independence", "neutrality", "redundancy"}
        # Every emitted line must begin with a sub-gate token; no
        # mid-message newlines may leak through to break parsing.
        for line in out.strip().split("\n"):
            assert line == "" or line.split("\t", 1)[0] in sub_gate_tokens, (
                f"machine-mode --report emitted a non-finding line "
                f"(likely a leaked newline in a message): {line!r}"
            )


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
