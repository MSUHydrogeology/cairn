"""Order-independence sub-gate -- seed contract + pytest wrapper.

Pins (per plan-review finding #2):

* The conftest shuffle hook is deterministic: same seed -> same
  collection order.
* The hook is a strict no-op when ``--quality-gate-shuffle-seed`` is
  absent.
* The sub-gate runs once per seed; every run echoes the seed in its
  report.
* A failure under one seed surfaces with the seed visible.
"""
from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
QG_SRC = CAIRN_ROOT / "scripts" / "quality_gate.py"

pytestmark = pytest.mark.skipif(
    not QG_SRC.exists(), reason="quality_gate.py not available",
)


def _load_qg(name: str = "_quality_gate_order_under_test") -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, QG_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def qg() -> ModuleType:
    return _load_qg()


class TestShuffleHookContract:
    """Verifies the documented seed contract directly -- we
    re-implement the small ``random.Random(seed).shuffle`` step the
    conftest does, and check the contract properties (determinism,
    seed sensitivity).  This is faster than spawning pytest twice."""

    def test_same_seed_produces_same_order(self):
        items_a = ["a", "b", "c", "d", "e", "f", "g"]
        items_b = list(items_a)
        random.Random(0).shuffle(items_a)
        random.Random(0).shuffle(items_b)
        assert items_a == items_b

    def test_different_seeds_produce_different_orders(self):
        items_a = ["a", "b", "c", "d", "e", "f", "g"]
        items_b = list(items_a)
        random.Random(0).shuffle(items_a)
        random.Random(1).shuffle(items_b)
        assert items_a != items_b


class TestSeedResolution:
    """The CLI seed-resolution surface -- a wrapper around
    ``_resolve_seeds`` exercising every input form."""

    def test_default_is_single_zero(self, qg):
        ns = qg._build_arg_parser().parse_args([])
        assert qg._resolve_seeds(ns) == [0]

    def test_seed_overrides_default(self, qg):
        ns = qg._build_arg_parser().parse_args(["--seed", "42"])
        assert qg._resolve_seeds(ns) == [42]

    def test_seed_count_produces_consecutive_seeds(self, qg):
        ns = qg._build_arg_parser().parse_args(["--seed-count", "5"])
        assert qg._resolve_seeds(ns) == [0, 1, 2, 3, 4]

    def test_seed_list_overrides_count(self, qg):
        ns = qg._build_arg_parser().parse_args([
            "--seed-list", "11,42,7", "--seed-count", "2",
        ])
        assert qg._resolve_seeds(ns) == [11, 42, 7]


class TestSubGateRunWrapper:
    """End-to-end test of ``_run_order_independence`` via a
    constructed fixture tree.  We don't actually shell out to pytest
    against the real Cairn suite (the parent invocation itself is
    pytest; nested invocation is fragile in CI).  Instead we
    construct a trivial fixture tree with one passing test and one
    deliberately-failing test, and assert the gate's per-seed
    findings reflect each path.
    """

    def _write_passing_suite(self, target: Path) -> None:
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
        (target / "_fixture_tests" / "test_pass.py").write_text(
            "def test_one(): assert True\n"
            "def test_two(): assert True\n"
        )

    def _write_failing_suite(self, target: Path) -> None:
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
            "def test_fails(): assert False, 'deliberately failing'\n"
        )

    def test_clean_seed_reports_pass(self, qg, tmp_path):
        self._write_passing_suite(tmp_path)
        findings = qg._run_order_independence(
            seeds=[0], repo_root=tmp_path, test_dir="_fixture_tests",
        )
        assert len(findings) == 1
        assert findings[0].severity == "info"
        assert "seed=0: PASS" in findings[0].message

    def test_failing_seed_reports_fail_with_seed(self, qg, tmp_path):
        self._write_failing_suite(tmp_path)
        findings = qg._run_order_independence(
            seeds=[7], repo_root=tmp_path, test_dir="_fixture_tests",
        )
        assert len(findings) == 1
        assert findings[0].severity == "fail"
        assert "seed=7" in findings[0].message

    def test_multi_seed_runs_each(self, qg, tmp_path):
        self._write_passing_suite(tmp_path)
        findings = qg._run_order_independence(
            seeds=[0, 1, 2],
            repo_root=tmp_path, test_dir="_fixture_tests",
        )
        assert len(findings) == 3
        seeds_in_messages = sorted(
            int(f.message.split("seed=")[1].split(":")[0])
            for f in findings
        )
        assert seeds_in_messages == [0, 1, 2]

    def test_the_child_env_is_an_additive_copy_not_a_fresh_mapping(
            self, qg, tmp_path, monkeypatch):
        """The order-independence spawn is a full-suite run by construction, so
        it carries the broad-run override. It must build that environment as a
        **copy** of its own.

        A fresh mapping naming only the override would satisfy any check that
        merely looks for the override -- and would silently drop
        ``CAIRN_RELEASE_GATE_ACTIVE``, which ``bootstrap/security_check.py``
        passes into this process explicitly. A release run would then stop
        refusing a skip as evidence while every test still passed, which is a
        failure nothing else in the suite would catch.

        Directional: the child asserts on both variables, so an implementation
        that carries the override but not the parent fails on the second.
        """
        self._write_passing_suite(tmp_path)
        (tmp_path / "_fixture_tests" / "test_pass.py").write_text(
            "import os\n"
            "def test_the_override_reached_the_child():\n"
            "    assert os.environ.get('CAIRN_FULL_SUITE') == '1'\n"
            "def test_the_parent_environment_survived():\n"
            "    assert os.environ.get('CAIRN_PROBE_PARENT') == 'kept'\n"
        )
        monkeypatch.setenv("CAIRN_PROBE_PARENT", "kept")
        monkeypatch.delenv("CAIRN_FULL_SUITE", raising=False)
        findings = qg._run_order_independence(
            seeds=[0], repo_root=tmp_path, test_dir="_fixture_tests",
        )
        assert len(findings) == 1
        assert findings[0].severity == "info", findings[0].message
