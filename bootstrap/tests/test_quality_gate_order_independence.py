"""Order-independence sub-gate -- seed contract + pytest wrapper.

Promises:
- The same seed always produces the same test collection order.
- Without the shuffle flag, pytest runs tests in their default collection order.
- The sub-gate runs the suite once per configured seed and reports each seed's pass or fail.
- A failure under any seed is reported as a failure that names that seed.
- Seeds come from --seed, --seed-count or --seed-list; with no option the run uses seed 0 alone.
- An explicit seed list takes precedence over a seed count.
- In a native release run, only the seed-0 child receives the release context; any other seed is refused.

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

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
QG_SRC = CAIRN_ROOT / "scripts" / "quality_gate.py"

pytestmark = pytest.mark.skipif(
    not QG_SRC.exists(), reason="quality_gate.py not available",
)


@pytest.mark.parametrize("context", ["plain", "release"])
def test_each_seed_runs_a_failing_seed_is_named_and_release_context_reaches_only_seed_zero(
    tmp_path: Path, context: str,
) -> None:
    """Promise: the sub-gate runs the suite once per listed seed (the list
    wins over ``--seed-count``) and reports one finding per seed, naming a
    failing seed.  Each child gets a copy of the parent environment plus the
    gate's own override, and in a release run only the seed-0 child receives
    the release context; any other seed is refused.  The fixture suite's own
    assertions make a child fail when the environment is not as promised."""
    suite = tmp_path / "_fixture_tests"
    suite.mkdir()
    (suite / "conftest.py").write_text(
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
    (suite / "test_env.py").write_text(
        "import os\n"
        "def test_the_gate_override_reached_the_child():\n"
        "    assert os.environ.get('CAIRN_FULL_SUITE') == '1'\n"
        "def test_the_parent_environment_survived():\n"
        "    assert os.environ.get('CAIRN_PROBE_PARENT') == 'kept'\n"
        "def test_the_release_context_arrived_when_one_was_set():\n"
        "    if os.environ.get('CAIRN_PROBE_EXPECT_RELEASE') != '1':\n"
        "        return\n"
        "    assert os.environ.get('CAIRN_NATIVE_RUN_NONCE') == 'a' * 64\n"
        "    assert os.environ.get('CAIRN_NATIVE_RUN_HEAD') == 'b' * 40\n"
        "    assert os.environ.get('CAIRN_NATIVE_RUN_POLICY_ID') == 'policy'\n"
        "    assert os.environ.get('CAIRN_NATIVE_RUN_SEED0_REPORT') == 'seed0.json'\n"
        "    assert os.environ.get('CAIRN_RELEASE_GATE_ACTIVE') == '1'\n"
        "def test_seven_is_the_one_failing_seed(request):\n"
        "    assert request.config.getoption('--quality-gate-shuffle-seed') != 7\n"
    )
    env = {
        name: value for name, value in os.environ.items()
        if not name.startswith("CAIRN_NATIVE_RUN_")
        and name not in ("CAIRN_FULL_SUITE", "CAIRN_RELEASE_GATE_ACTIVE")
    }
    env["CAIRN_PROBE_PARENT"] = "kept"
    if context == "release":
        env.update({
            "CAIRN_PROBE_EXPECT_RELEASE": "1",
            "CAIRN_NATIVE_RUN_NONCE": "a" * 64,
            "CAIRN_NATIVE_RUN_HEAD": "b" * 40,
            "CAIRN_NATIVE_RUN_POLICY_ID": "policy",
            "CAIRN_NATIVE_RUN_DEFAULT_REPORT": "default.json",
            "CAIRN_NATIVE_RUN_SEED0_REPORT": "seed0.json",
            "CAIRN_RELEASE_GATE_ACTIVE": "1",
        })
        seeds = "0,1"
    else:
        seeds = "0,1,7"
    result = subprocess.run(
        [sys.executable, str(QG_SRC), "--root", str(tmp_path),
         "--sub", "order-independence", "--test-dir", "_fixture_tests",
         "--seed-list", seeds, "--seed-count", "1", "--report"],
        cwd=tmp_path, env=env, capture_output=True, text=True,
    )
    reported: list[tuple[int, str]] = []
    for line in result.stdout.splitlines():
        if not line.startswith("order-independence\t"):
            continue
        fields = line.split("\t")
        reported.append((int(re.search(r"seed=(\d+)", fields[4]).group(1)), fields[1]))
    expected = ([(0, "info"), (1, "fail")] if context == "release"
                else [(0, "info"), (1, "info"), (7, "fail")])
    assert reported == expected, result.stdout
    assert result.returncode == 1
