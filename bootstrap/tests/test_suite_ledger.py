# SPDX-License-Identifier: MIT
"""The suite-cost ledger: what the collector records, and what it must never do.

**Why almost everything here spawns a real pytest.** The collector is a set of
pytest hooks, and its behaviour is a property of a *session* -- which hooks fire,
in what order, with what reports, and what the process's environment looked like
when it started. Calling a hook function directly exercises none of that. Each
test that needs a written row builds a throwaway tree carrying a copy of the real
collector and runs pytest inside it, so what is measured is the shipped
mechanism.

**Why the throwaway tree, and not this repository's own.** The ledger path is
derived from the collector's own file location, so a copy of the collector
resolves its ledger inside the copy's tree. That is what makes these tests
possible *and* what keeps them out of the live ledger the reader renders: a test
that pointed at the real tree would write test rows into the record the whole
mechanism exists to produce.

**Why the child environment is scrubbed rather than inherited.** These tests very
often run inside a session that has already claimed the collector's ownership
marker. A child that simply inherited it would take the "I am a nested session"
path and record nothing, and every assertion about a written row would pass
without testing anything. That failure is silent, which is what makes it worth a
paragraph.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]
CONFTEST = CAIRN_ROOT / "bootstrap" / "tests" / "conftest.py"
READER_SRC = CAIRN_ROOT / "tools" / "suite_cost.py"

#: Environment names that would otherwise decide a child's behaviour by
#: accident. Every child starts from a known state and opts back in explicitly.
_SCRUBBED = (
    "PYTEST_ADDOPTS", "PYTEST_PLUGINS", "CAIRN_RELEASE_GATE_ACTIVE",
    "CAIRN_SUITE_LEDGER", "CAIRN_SUITE_LEDGER_LABEL", "CAIRN_SUITE_LEDGER_SESSION",
    "CAIRN_FULL_SUITE",
)

_TWO_PASSING = "def test_one():\n    assert True\n\n\ndef test_two():\n    assert True\n"
_ONE_PASSING = "def test_three():\n    assert True\n"
_ONE_SKIPPED = (
    "import pytest\n\n\n"
    "@pytest.mark.skip(reason='dev dependency absent')\n"
    "def test_skipped():\n    pass\n"
)

#: A second plugin, in its own module, that dumps pytest's own record of every
#: runtest report. Its own module rather than an append to the collector: the
#: point is to read a source the collector does not control.
_STATS_PROBE = '''\
import json
import os


def pytest_sessionfinish(session, exitstatus):
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    entries = []
    if reporter is not None:
        for _bucket, reports in reporter.stats.items():
            for report in reports:
                when = getattr(report, "when", None)
                # Runtest phases only. A CollectReport also carries a `when`
                # ("collect"), and counting it would make a module that skipped
                # itself before collection look like a node that executed.
                if when not in ("setup", "call", "teardown"):
                    continue
                entries.append({
                    "nodeid": getattr(report, "nodeid", ""),
                    "when": when,
                    "outcome": getattr(report, "outcome", ""),
                    "wasxfail": hasattr(report, "wasxfail"),
                })
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stats.json")
    with open(target, "w", encoding="utf-8") as handle:
        json.dump(entries, handle)
'''


# --- Loading the units under test ---------------------------------------------


def _load(name: str, path: Path):
    """Load a module from a path as a *fresh* object.

    Fresh matters twice over: pytest registers plugins by identity, so this does
    not double-register the collector's hooks, and a test that mutates the
    module's accumulation state cannot leak that state into the next test.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def collector():
    return _load("_cairn_ledger_probe", CONFTEST)


def reader():
    return _load("_cairn_suite_cost_probe", READER_SRC)


# --- Building and running a throwaway tree ------------------------------------


def _tree(tmp_path: Path, files=None, *, extra_conftest: str = "",
          ini: str | None = None, probe: bool = False,
          measurement: bool = True) -> Path:
    tests = tmp_path / "bootstrap" / "tests"
    tests.mkdir(parents=True)
    if measurement:
        (tmp_path / "dev" / "measurement").mkdir(parents=True)
    shutil.copy(CONFTEST, tests / "conftest.py")
    if extra_conftest:
        # Appended to the SAME module, so a name defined here REPLACES the
        # collector's -- which is exactly what the fault-injection tests want.
        # Every injection below replaces an internal helper and never a pytest
        # hook: rebinding a hook name deletes the hook, and the deletion is
        # silent, because a function of the right name is still present and
        # still does something reasonable.
        with (tests / "conftest.py").open("a", encoding="utf-8") as handle:
            handle.write("\n\n" + extra_conftest + "\n")
    for name, body in (files or {"test_a.py": _TWO_PASSING,
                                 "test_b.py": _ONE_PASSING}).items():
        (tests / name).write_text(body, encoding="utf-8")
    if ini is not None:
        (tmp_path / "pytest.ini").write_text(ini, encoding="utf-8")
    if probe:
        (tmp_path / "_ledger_stats_probe.py").write_text(
            _STATS_PROBE, encoding="utf-8")
    return tmp_path


def _child_env(overrides=None, keep_marker=None) -> dict:
    env = dict(os.environ)
    for name in _SCRUBBED:
        env.pop(name, None)
    if keep_marker is not None:
        env["CAIRN_SUITE_LEDGER_SESSION"] = keep_marker
    env.update(overrides or {})
    return env


def _run(root: Path, args=("bootstrap/tests",), *, env=None, keep_marker=None):
    return subprocess.run(
        [sys.executable, "-m", "pytest", *args], cwd=str(root),
        env=_child_env(env, keep_marker), capture_output=True, text=True,
        check=False,
    )


def _ledger_file(root: Path) -> Path:
    return root / "dev" / "measurement" / "suite-runs.jsonl"


def _rows(root: Path) -> list[dict]:
    path = _ledger_file(root)
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def _one_row(root: Path, proc=None) -> dict:
    rows = _rows(root)
    assert len(rows) == 1, (
        f"expected exactly one recorded session, got {len(rows)}"
        + (f"\n{proc.stdout}\n{proc.stderr}" if proc else ""))
    return rows[0]


def _row_template(module, **overrides) -> dict:
    """A schema-shaped row, for the encoder and budget tests that have no
    session to produce one."""
    row = {
        "ts_start": "2026-08-21T00:00:00+00:00",
        "ts_end": "2026-08-21T00:02:00+00:00",
        "wall_s": 120.0, "collector_ms": 0.4, "head": "0" * 40,
        "interpreter": "cpython 3.13.13", "invocation": ["bootstrap/tests"],
        "scope": "full",
        "scope_basis": {"targets": ["bootstrap/tests"], "inipath": False,
                        "addopts_set": False, "plugins_set": False},
        "label": None, "collected": 1, "executed": 1, "not_run": 0,
        "deselected": 0, "collection_errors": 0, "exitstatus": 0,
        "interrupted": False, "truncated": False, "by_file": {},
        "by_file_total": 0, "by_file_kept": 0,
    }
    row.update({name: 0 for name in module.LEDGER_OUTCOMES})
    row.update(overrides)
    return row


# --- A session is recorded, and only the right ones ---------------------------


def test_a_top_level_session_records_one_row_naming_its_own_coverage(tmp_path):
    """The base case everything else varies from: an ordinary run of the suite
    root writes exactly one row and says it covered that root completely.
    Without a working positive case the classifier is pinned only against
    over-claiming, and an implementation that answered `unknown` to everything
    would satisfy every negative case in this file."""
    root = _tree(tmp_path)
    proc = _run(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    row = _one_row(root, proc)
    assert row["scope"] == "full"
    assert row["scope_basis"]["targets"] == ["bootstrap/tests"]
    assert row["collected"] == 3 and row["executed"] == 3
    assert row["passed"] == 3 and row["not_run"] == 0
    assert row["truncated"] is False


def test_the_order_independence_spelling_of_the_same_run_reads_the_same():
    """The two invocations that legitimately cover the whole suite spell their
    positional differently -- one relative, one absolute and resolved -- so a
    classifier comparing argv strings would recognize at most one of them.

    Built under a short base directory rather than ``tmp_path`` on purpose: an
    argv token is capped at 128 bytes, and the temporary paths this suite is
    handed are longer than that on their own. That cap is the accepted contract
    and it is not what this test is about, so the token length is asserted
    explicitly -- if the environment ever makes it too long, this fails loudly
    instead of quietly measuring the cap instead of the classifier."""
    base = tempfile.mkdtemp(prefix="cled", dir=_short_base())
    try:
        root = _tree(Path(base))
        target = str((root / "bootstrap" / "tests").resolve())
        assert len(target.encode("ascii")) <= 128, target
        proc = _run(root, (target, "--quality-gate-shuffle-seed=7", "-q",
                           "--no-header", "--no-summary"))
        assert proc.returncode == 0, proc.stdout + proc.stderr
        row = _one_row(root, proc)
        assert row["truncated"] is False, row
        assert row["scope"] == "full", row
    finally:
        shutil.rmtree(base, ignore_errors=True)


def _short_base() -> str:
    """The shortest writable temporary base available.

    The mechanism is POSIX-only by contract, and `/tmp` is the short spelling
    every POSIX host has; the platform default is the fallback rather than the
    first choice because on macOS it is roughly fifty bytes deep before anything
    of the caller's is added.
    """
    for candidate in ("/tmp", tempfile.gettempdir()):
        if os.path.isdir(candidate) and os.access(candidate, os.W_OK):
            return candidate
    return tempfile.gettempdir()


def test_a_session_started_inside_another_one_records_nothing(tmp_path):
    """A suite-spawned child inherits the environment as a superset, marker
    included. Recording it would double-count every session that spawns one, and
    attribute the parent's cost to the child."""
    root = _tree(tmp_path)
    proc = _run(root, keep_marker="1")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _rows(root) == []


def test_consecutive_top_level_sessions_are_each_recorded(tmp_path):
    """The ownership marker is released when the session that claimed it ends.
    Without that release the second session in a process would see a marker,
    call itself a child, and every run after the first would vanish -- and a
    fresh subprocess per session would hide the bug completely."""
    root = _tree(tmp_path)
    (root / "driver.py").write_text(
        "import pytest\n"
        "pytest.main(['bootstrap/tests', '-q'])\n"
        "pytest.main(['bootstrap/tests', '-q'])\n", encoding="utf-8")
    proc = subprocess.run([sys.executable, "driver.py"], cwd=str(root),
                          env=_child_env(), capture_output=True, text=True,
                          check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert len(_rows(root)) == 2, proc.stdout + proc.stderr


def test_a_marker_this_session_did_not_claim_survives_untouched(tmp_path):
    """A pre-existing marker in the *same process* is the precondition the
    ownership rule exists to detect. The nested session must record nothing and
    must leave the marker exactly as it found it: releasing a marker it does not
    own would let the owner's next child start recording."""
    root = _tree(tmp_path)
    (root / "driver.py").write_text(
        "import os\n"
        "import pytest\n"
        "os.environ['CAIRN_SUITE_LEDGER_SESSION'] = 'an-outer-owner'\n"
        "pytest.main(['bootstrap/tests', '-q'])\n"
        "print('MARKER:' + repr(os.environ.get('CAIRN_SUITE_LEDGER_SESSION')))\n",
        encoding="utf-8")
    proc = subprocess.run([sys.executable, "driver.py"], cwd=str(root),
                          env=_child_env(), capture_output=True, text=True,
                          check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "MARKER:'an-outer-owner'" in proc.stdout, proc.stdout + proc.stderr
    assert _rows(root) == []


def test_a_release_session_is_not_recorded(tmp_path):
    """Release evidence must not share a mechanism with a diagnostics
    side-channel: a release run that took a write lock, or wrote a row nobody
    reviewed, would be a new thing for the ceremony to account for."""
    root = _tree(tmp_path)
    proc = _run(root, env={"CAIRN_RELEASE_GATE_ACTIVE": "1"})
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _rows(root) == []


def test_the_operator_opt_out_is_honoured(tmp_path):
    """An operator who switches the collector off gets a run that records
    nothing at all -- not a run that records that it was switched off."""
    root = _tree(tmp_path)
    proc = _run(root, env={"CAIRN_SUITE_LEDGER": "0"})
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _rows(root) == []


def test_a_tree_with_no_measurement_directory_is_not_given_one(tmp_path):
    """The collector never creates the directory it writes into. A tree that
    does not keep measurements is a tree that opted out by construction, and a
    diagnostics mechanism that materializes directories in someone else's
    checkout is a surprise, not a service."""
    root = _tree(tmp_path, measurement=False)
    proc = _run(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert not (root / "dev" / "measurement").exists()


# --- The session's outcome is never the collector's to change -----------------


_FAULTED_HOOKS = (
    "_ledger_begin_session", "_ledger_accumulate_report",
    "_ledger_accumulate_collect", "_ledger_accumulate_deselected",
    "_ledger_finish_session",
)


def _fault(name: str) -> str:
    return (f"def {name}(*args, **kwargs):\n"
            f"    raise RuntimeError('injected fault in {name}')\n")


@pytest.mark.parametrize("hook", _FAULTED_HOOKS)
def test_a_fault_in_any_one_hook_leaves_the_session_outcome_untouched(
        tmp_path, hook):
    """A diagnostics hook that can fail a suite teaches an operator to switch
    diagnostics off, and then there is no measurement and no trust. The
    expectation comes from a control run with the collector disabled, not from
    the collector's own output."""
    files = {"test_a.py": _TWO_PASSING, "test_mixed.py": _ONE_SKIPPED}
    control_root = _tree(tmp_path / "control", files, probe=True)
    faulted_root = _tree(tmp_path / "faulted", files, probe=True,
                         extra_conftest=_fault(hook))
    args = ("bootstrap/tests", "-p", "_ledger_stats_probe",
            "--deselect", "bootstrap/tests/test_a.py::test_two")
    control = _run(control_root, args, env={"CAIRN_SUITE_LEDGER": "0"})
    faulted = _run(faulted_root, args)
    assert faulted.returncode == control.returncode, (
        faulted.stdout + faulted.stderr)
    assert _stats(faulted_root) == _stats(control_root)


def _stats(root: Path):
    entries = json.loads((root / "stats.json").read_text(encoding="utf-8"))
    return sorted((e["nodeid"], e["when"], e["outcome"], e["wasxfail"])
                  for e in entries)


_REMOVE_THE_GUARD = "def _ledger_step(fn, *args):\n    fn(*args)\n"
_RAISE_IN_ACCUMULATOR = (
    "def _ledger_accumulate_report(report):\n"
    "    raise RuntimeError('injected')\n")
_RAISE_IN_SESSIONFINISH = (
    "def _ledger_finish_session(session, exitstatus):\n"
    "    raise KeyboardInterrupt('injected')\n")


def test_release_evidence_survives_a_diagnostics_fault(tmp_path):
    """The release rule decides whether a build may ship. A fault in a
    measurement side-channel must not take that decision away from it, in either
    direction: the report must print, with the nodeids an operator needs to
    repair the run, and the exit code must stay the release rule's own."""
    root = _tree(tmp_path, {"test_a.py": _TWO_PASSING,
                            "test_mixed.py": _ONE_SKIPPED},
                 extra_conftest=_RAISE_IN_ACCUMULATOR + "\n\n"
                 + _RAISE_IN_SESSIONFINISH)
    proc = _run(root, env={"CAIRN_RELEASE_GATE_ACTIVE": "1"})
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "RELEASE MODE" in proc.stderr
    assert "test_mixed.py::test_skipped" in proc.stderr


@pytest.mark.parametrize("case,injection,expected,report_survives", [
    ("accumulator", _RAISE_IN_ACCUMULATOR, 3, False),
    ("sessionfinish", _RAISE_IN_SESSIONFINISH, -2, True),
])
def test_the_guard_is_what_keeps_a_diagnostics_fault_off_the_exit_code(
        tmp_path, case, injection, expected, report_survives):
    """The companion the test above needs, and the reason to trust it. Remove
    the guard and the identical fault takes the release rule's exit 1 away:
    ``3`` (pytest's internal error) from the report hook, and death by SIGINT
    from the session-finish block -- the exact "exit 1 with a report becomes an
    interrupt with none" the guard exists to prevent.

    Ordering is only defence in depth, and this measures how far it reaches: the
    release report survives the session-finish fault, because the release rule
    ran first in that same hook, and does **not** survive the report-hook fault,
    because the session aborted before the skip it would have reported ever
    happened. Recorded as it behaves, not as it would be tidier."""
    root = _tree(tmp_path, {"test_a.py": _TWO_PASSING,
                            "test_mixed.py": _ONE_SKIPPED},
                 extra_conftest=_REMOVE_THE_GUARD + "\n\n" + injection)
    proc = _run(root, env={"CAIRN_RELEASE_GATE_ACTIVE": "1"})
    assert proc.returncode == expected, (
        f"{case}: {proc.returncode}\n{proc.stdout}\n{proc.stderr}")
    assert proc.returncode != 1
    assert ("RELEASE MODE" in proc.stderr) is report_survives, proc.stderr


# --- Node accounting ----------------------------------------------------------


_ABORT_SHAPES = {
    "stop-on-first-failure": (
        {"test_a.py": "def test_bad():\n    assert False\n\n\n"
                      "def test_never():\n    assert True\n",
         "test_b.py": _ONE_PASSING},
        ("-x",),
    ),
    "maxfail-two": (
        {"test_a.py": "def test_bad():\n    assert False\n\n\n"
                      "def test_worse():\n    assert False\n\n\n"
                      "def test_never():\n    assert True\n"},
        ("--maxfail=2",),
    ),
    "explicit-exit": (
        {"test_a.py": "import pytest\n\n\n"
                      "def test_stop():\n    pytest.exit('stopping')\n\n\n"
                      "def test_never():\n    assert True\n"},
        (),
    ),
    "keyboard-interrupt": (
        {"test_a.py": "def test_interrupt():\n    raise KeyboardInterrupt\n\n\n"
                      "def test_never():\n    assert True\n"},
        (),
    ),
    "setup-error": (
        {"test_a.py": "import pytest\n\n\n"
                      "@pytest.fixture\ndef broken():\n    raise RuntimeError('setup')\n\n\n"
                      "def test_uses(broken):\n    assert True\n"},
        (),
    ),
    "teardown-error": (
        {"test_a.py": "import pytest\n\n\n"
                      "@pytest.fixture\ndef leaky():\n    yield\n    raise RuntimeError('teardown')\n\n\n"
                      "def test_uses(leaky):\n    assert True\n"},
        (),
    ),
    "module-level-skip": (
        {"test_a.py": _TWO_PASSING,
         "test_skipmod.py": "import pytest\n"
                            "pytest.skip('absent', allow_module_level=True)\n\n\n"
                            "def test_never():\n    assert True\n"},
        (),
    ),
}


def _resolve_outcome(node) -> dict:
    if node["errors"]:
        return "errors"
    if node["failed"]:
        return "failed"
    if node["xpassed"]:
        return "xpassed"
    if node["xfailed"]:
        return "xfailed"
    if node["skipped"]:
        return "skipped"
    if node["setup_passed"] and "call" not in node["phases"]:
        return "aborted"
    return "passed"


def _expected_accounting(root: Path, outcomes) -> tuple[int, dict]:
    """Re-derive node accounting from pytest's own record of the session.

    Derived from ``terminalreporter.stats`` -- a record the collector neither
    writes nor reads -- so a dropped report, a double count, or a phase filed
    under the wrong node shows up as a disagreement. What it cannot catch is a
    shared misreading of the precedence rule itself, which is why the precedence
    is also stated in prose beside the collector's own copy.
    """
    entries = json.loads((root / "stats.json").read_text(encoding="utf-8"))
    nodes: dict = {}
    for entry in entries:
        node = nodes.setdefault(entry["nodeid"], {
            "phases": set(), "errors": False, "failed": False, "xpassed": False,
            "xfailed": False, "skipped": False, "setup_passed": False})
        node["phases"].add(entry["when"])
        if entry["outcome"] == "failed":
            if entry["when"] in ("setup", "teardown"):
                node["errors"] = True
            elif entry["when"] == "call":
                node["failed"] = True
        if entry["wasxfail"]:
            if entry["outcome"] == "passed":
                node["xpassed"] = True
            else:
                node["xfailed"] = True
        if entry["outcome"] == "skipped":
            node["skipped"] = True
        if entry["when"] == "setup" and entry["outcome"] == "passed":
            node["setup_passed"] = True
    counts = {name: 0 for name in outcomes}
    for node in nodes.values():
        counts[_resolve_outcome(node)] += 1
    return len(nodes), counts


@pytest.mark.parametrize("shape", sorted(_ABORT_SHAPES))
def test_node_accounting_agrees_with_pytests_own_record_of_the_session(
        tmp_path, shape):
    """A session that stops early is the case where a count is easiest to get
    wrong and hardest to notice: the bare inequality `executed <= collected` is
    satisfied by a session that ran nothing at all, so it is not the criterion.
    The criterion is that every count reconciles, node for node, against
    pytest's own record."""
    files, extra = _ABORT_SHAPES[shape]
    root = _tree(tmp_path, files, probe=True)
    proc = _run(root, ("bootstrap/tests", "-p", "_ledger_stats_probe", *extra))
    row = _one_row(root, proc)
    outcomes = collector().LEDGER_OUTCOMES
    expected_executed, expected_counts = _expected_accounting(root, outcomes)
    assert 0 <= row["executed"] <= row["collected"], row
    assert row["executed"] == expected_executed, (row, expected_counts)
    for name in outcomes:
        assert row[name] == expected_counts[name], (name, row, expected_counts)
    assert sum(row[name] for name in outcomes) == row["executed"]


# --- Scope classification -----------------------------------------------------


def test_a_narrowed_run_never_claims_it_covered_everything(tmp_path):
    """Deselection removes tests from a run without touching argv, so a
    classifier reading only the command line would call this complete."""
    root = _tree(tmp_path)
    proc = _run(root, ("bootstrap/tests", "--deselect",
                       "bootstrap/tests/test_a.py::test_two"))
    row = _one_row(root, proc)
    assert row["deselected"] == 1
    assert row["scope"] != "full"


_UNKNOWN_CASES = {
    "ignore": (("bootstrap/tests", "--ignore=bootstrap/tests/test_b.py"), {}, None, None),
    "ignore-glob": (("bootstrap/tests", "--ignore-glob=*test_b*"), {}, None, None),
    "addopts-env": (("bootstrap/tests",), {"PYTEST_ADDOPTS": "-q"}, None, None),
    "ini-addopts": (("bootstrap/tests",), {}, "[pytest]\naddopts = -q\n", None),
    "no-python-plugin": (("bootstrap/tests", "-p", "no:python"), {}, None, None),
    "zero-positionals": ((), {}, None, None),
    "module-level-skip": (("bootstrap/tests",), {}, None, {
        "test_a.py": _TWO_PASSING,
        "test_skipmod.py": "import pytest\n"
                           "pytest.skip('absent', allow_module_level=True)\n"}),
    "importorskip": (("bootstrap/tests",), {}, None, {
        "test_a.py": _TWO_PASSING,
        "test_skipmod.py": "import pytest\n"
                           "pytest.importorskip('cairn_absent_module_probe')\n"}),
}


@pytest.mark.parametrize("case", sorted(_UNKNOWN_CASES))
def test_a_run_that_might_have_been_narrowed_refuses_to_claim_coverage(
        tmp_path, case):
    """Each of these narrows a run, or could, by a route the resolved counts
    alone cannot detect -- an ignored path, an environment variable, an ini
    file, a disabled plugin, a file that skipped itself before it was collected.
    Under-claiming costs one data point; over-claiming corrupts every figure
    derived from the row."""
    args, env, ini, files = _UNKNOWN_CASES[case]
    root = _tree(tmp_path, files, ini=ini)
    proc = _run(root, args, env=env)
    row = _one_row(root, proc)
    assert row["scope"] == "unknown", (case, row)


def test_a_basis_too_long_to_record_refuses_to_claim_coverage(tmp_path):
    """A classification a reader cannot re-derive must not be asserted. When the
    evidence is capped away, `unknown` is the only honest answer -- the row still
    carries a timing, which is what it was written for."""
    deep = "d" * 200
    root = _tree(tmp_path, {"test_a.py": _TWO_PASSING})
    nested = root / "bootstrap" / "tests" / deep
    nested.mkdir()
    (nested / "test_deep.py").write_text(_ONE_PASSING, encoding="utf-8")
    proc = _run(root, (f"bootstrap/tests/{deep}",))
    row = _one_row(root, proc)
    assert row["truncated"] is True, row
    assert row["scope"] == "unknown", row


def test_the_same_command_under_a_different_environment_records_a_different_basis(
        tmp_path):
    """The basis exists so a coverage claim can be audited later. Two runs whose
    argv is identical but whose *effective* configuration differs must not
    produce indistinguishable rows, or the audit has nothing to work with."""
    plain_root = _tree(tmp_path / "plain")
    addopts_root = _tree(tmp_path / "addopts")
    plain = _one_row(plain_root, _run(plain_root))
    seeded = _one_row(addopts_root, _run(addopts_root,
                                         env={"PYTEST_ADDOPTS": "-q"}))
    assert plain["invocation"] == seeded["invocation"]
    assert plain["scope_basis"] != seeded["scope_basis"]
    assert plain["scope_basis"]["addopts_set"] is False
    assert seeded["scope_basis"]["addopts_set"] is True
    # The variable's *value* is never copied into the row: whether it was set is
    # the whole of what the classification depends on, and its content is not
    # the project's to publish.
    assert "-q" not in json.dumps(seeded["scope_basis"])
    rederive = reader().rederive_scope
    assert rederive(plain) == plain["scope"]
    assert rederive(seeded) == seeded["scope"]


def test_a_claim_the_rows_own_fields_contradict_is_reported(tmp_path):
    """The reader re-derives every coverage claim instead of trusting it, so a
    row written by an older or patched collector is visible rather than
    authoritative. A reader that echoed the stored value would report a wrong
    claim as confidently as a right one."""
    root = _tree(tmp_path)
    row = _one_row(root, _run(root))
    assert row["scope"] == "full"
    tampered = dict(row, deselected=3)
    ledger = tmp_path / "tampered.jsonl"
    ledger.write_text(json.dumps(tampered) + "\n", encoding="utf-8")
    module = reader()
    assert module.rederive_scope(tampered) == "unknown"
    rows, malformed = module.read_ledger(ledger)
    report = module.render(rows, malformed, ledger)
    assert "recorded as `full`" in report
    assert "support `unknown`" in report


# --- Sanitizing, capping, encoding, the budget --------------------------------


@pytest.mark.parametrize("raw,expected", [
    ("ok", "ok"),
    ("café", "caf\\xe9"),
    ("\U0001f600", "\\U0001f600"),
    ("\ud800", "\\ud800"),
    ("a café \U0001f600 \ud800 z", "a caf\\xe9 \\U0001f600 \\ud800 z"),
])
def test_every_string_survives_as_ascii_with_its_content_intact(raw, expected):
    """Totality alone is not the property: a sanitizer returning the empty
    string for everything non-ASCII is total and sets its flag correctly on
    every case here. What must hold is that the content *survives* in a form a
    reader can still recognize."""
    value, capped = collector()._ledger_cap(raw, 128)
    assert value == expected
    assert capped is False
    assert value.encode("ascii")


def test_a_string_past_its_cap_keeps_its_beginning_and_says_it_was_cut():
    module = collector()
    value, capped = module._ledger_cap("z" * 500, 128)
    assert capped is True
    assert value == "z" * 128


def test_the_encoder_call_site_is_the_pinned_one():
    """Every byte budget in this mechanism is stated against one exact encoding.
    A call site that quietly dropped `sort_keys` or `ensure_ascii` would keep
    passing every size assertion here while making the budget mean something
    else."""
    import inspect
    source = inspect.getsource(collector()._ledger_encode)
    for fragment in ("json.dumps(row", "ensure_ascii=True",
                     'separators=(",", ":")', "allow_nan=False",
                     "sort_keys=True"):
        assert fragment in source, fragment


def test_a_row_that_fits_carries_its_real_content(tmp_path):
    """The half of the budget contract that can actually fail. Every totality
    clause below is satisfied by an encoder that emits the skeleton row
    unconditionally -- one line, under budget, parses, flag set. This is what
    says the row carried the measurement."""
    root = _tree(tmp_path)
    proc = _run(root, env={"CAIRN_SUITE_LEDGER_LABEL": "chunk-c"})
    row = _one_row(root, proc)
    assert row["truncated"] is False
    assert row["label"] == "chunk-c"
    assert row["invocation"] == ["bootstrap/tests"]
    assert row["scope_basis"]["targets"] == ["bootstrap/tests"]
    assert set(row["by_file"]) == {"bootstrap/tests/test_a.py",
                                   "bootstrap/tests/test_b.py"}
    assert row["by_file_kept"] == row["by_file_total"] == 2


@pytest.mark.parametrize("case", ["oversized-label", "token-flood",
                                  "control-characters"])
def test_a_hostile_field_still_yields_exactly_one_parseable_line(tmp_path, case):
    """A row is a record of a session that happened. Whatever a field's content,
    exactly one line must be appended and it must parse -- a half-written or
    unparseable line loses the session it describes *and* corrupts the next
    append after it."""
    root = _tree(tmp_path)
    if case == "oversized-label":
        proc = _run(root, env={"CAIRN_SUITE_LEDGER_LABEL": "L" * 5000})
    elif case == "control-characters":
        proc = _run(root, env={"CAIRN_SUITE_LEDGER_LABEL": "a\x01b\x1fc\x7fd"})
    else:
        proc = _run(root, ("bootstrap/tests", *["-q"] * 70))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    raw = _ledger_file(root).read_bytes()
    assert raw.count(b"\n") == 1
    assert len(raw.rstrip(b"\n")) <= 4096
    row = json.loads(raw)
    if case == "oversized-label":
        assert len(row["label"].encode("ascii")) == 128
        assert row["truncated"] is True
    elif case == "control-characters":
        assert row["label"] == "a\x01b\x1fc\x7fd"
    else:
        assert row["truncated"] is True
        assert len(row["invocation"]) <= 64


def test_every_real_test_file_in_this_suite_fits_the_budget():
    """Enumerated at run time rather than pinned to a count: this file's own
    arrival changes the number, so a hardcoded figure would be stale before it
    was first run."""
    module = collector()
    paths = sorted(
        path.relative_to(CAIRN_ROOT).as_posix()
        for path in (CAIRN_ROOT / "bootstrap" / "tests").rglob("test_*.py"))
    assert len(paths) > 50, "the enumeration found almost nothing -- check it"
    row = _row_template(module, by_file={path: 1234 for path in paths},
                        by_file_total=len(paths), by_file_kept=len(paths))
    line, skeletonized = module._ledger_fit(row)
    assert "\n" not in line
    assert len(line.encode("ascii")) <= module.LEDGER_ROW_BUDGET
    decoded = json.loads(line)
    assert decoded["truncated"] is True
    if not skeletonized:
        assert decoded["by_file_kept"] < decoded["by_file_total"]


def test_eviction_keeps_the_expensive_files_and_drops_the_cheap_ones():
    """A pruned breakdown exists to answer "where does the time go", so what it
    keeps must be the expensive end. Dropping by insertion order, or by name,
    would leave a table that ranks nothing."""
    module = collector()
    by_file = {f"bootstrap/tests/test_cheap_{i:03d}.py": 1 for i in range(400)}
    by_file["bootstrap/tests/test_one_slow_file.py"] = 900_000
    row = _row_template(module, by_file=dict(by_file),
                        by_file_total=len(by_file), by_file_kept=len(by_file))
    line, skeletonized = module._ledger_fit(row)
    assert not skeletonized
    decoded = json.loads(line)
    assert len(line.encode("ascii")) <= module.LEDGER_ROW_BUDGET
    assert decoded["truncated"] is True
    assert decoded["by_file_kept"] < decoded["by_file_total"]
    assert "bootstrap/tests/test_one_slow_file.py" in decoded["by_file"]
    assert decoded["by_file"]["bootstrap/tests/test_one_slow_file.py"] == 900_000


def test_nothing_is_evicted_from_a_breakdown_that_already_fits():
    """The companion the eviction test needs. "Eviction preserves cost" is
    satisfied by an implementation that evicts everything down to the single
    most expensive file, on every row, forever."""
    module = collector()
    by_file = {"bootstrap/tests/test_a.py": 12345,
               "bootstrap/tests/test_b.py": 1,
               "bootstrap/tests/test_c.py": 0}
    row = _row_template(module, by_file=dict(by_file), by_file_total=3,
                        by_file_kept=3)
    line, skeletonized = module._ledger_fit(row)
    assert not skeletonized
    decoded = json.loads(line)
    assert decoded["truncated"] is False
    assert decoded["by_file"] == by_file
    assert decoded["by_file_kept"] == decoded["by_file_total"] == 3


def test_sub_millisecond_phases_are_not_each_rounded_to_nothing():
    """A file of two thousand fast tests costs real time. Converting each report
    to milliseconds as it arrives rounds every one of them to zero and reports
    that file as free -- which is exactly the file a cost reader would then stop
    looking at."""
    module = collector()
    module._LEDGER["enabled"] = True

    class _Report:
        nodeid = "bootstrap/tests/test_fast.py::test_x"
        when = "call"
        failed = False
        passed = True
        skipped = False
        duration = 0.0004

    for _ in range(2000):
        module._ledger_accumulate_report(_Report())
    total_seconds = module._LEDGER["by_file"]["bootstrap/tests/test_fast.py"]
    assert int(round(total_seconds * 1000)) == 800
    assert 2000 * int(round(0.0004 * 1000)) == 0, (
        "the wrong implementation would report this file as free")


def test_a_row_with_an_impossible_timing_still_produces_a_row():
    """Silence is the worse failure: a missing row is indistinguishable from a
    session that never ran, so an unencodable row degrades to a skeleton that
    still says a session happened."""
    module = collector()
    row = _row_template(module, wall_s=float("nan"),
                        collector_ms=float("inf"))
    line, skeletonized = module._ledger_fit(row)
    assert skeletonized
    decoded = json.loads(line)
    assert decoded["wall_s"] is None
    assert decoded["collector_ms"] is None
    assert decoded["truncated"] is True
    assert decoded["scope"] == "unknown"
    assert decoded["ts_start"] == row["ts_start"]


# --- head resolution ----------------------------------------------------------


def _git(cwd: Path, *args):
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                          text=True, check=True)


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-b", "main")
    _git(root, "config", "user.email", "probe@example.invalid")
    _git(root, "config", "user.name", "Probe")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(root, "add", "seed.txt")
    _git(root, "commit", "-m", "seed")
    return root


def test_head_resolves_in_a_plain_checkout(tmp_path):
    root = _repo(tmp_path)
    expected = _git(root, "rev-parse", "HEAD").stdout.strip()
    assert collector()._ledger_head(root) == expected


def test_head_resolves_when_the_ref_lives_only_in_packed_refs(tmp_path):
    """After `git pack-refs` the loose ref file is gone. A resolver that only
    reads loose refs reports no commit for every repository that has been packed
    -- which is every repository that has been cloned."""
    root = _repo(tmp_path)
    expected = _git(root, "rev-parse", "HEAD").stdout.strip()
    _git(root, "pack-refs", "--all")
    assert not (root / ".git" / "refs" / "heads" / "main").exists()
    assert collector()._ledger_head(root) == expected


def test_head_resolves_in_a_linked_worktree_on_a_branch(tmp_path):
    """A linked worktree keeps HEAD in its own git directory and its branch ref
    in the shared one, so resolving it means following `commondir`. Agents work
    in worktrees, and a row from one that reported no commit would be
    unattributable."""
    root = _repo(tmp_path)
    linked = tmp_path / "linked"
    _git(root, "worktree", "add", "-b", "side", str(linked))
    expected = _git(linked, "rev-parse", "HEAD").stdout.strip()
    assert (linked / ".git").is_file()
    assert collector()._ledger_head(linked) == expected


def test_an_unreadable_git_directory_costs_the_commit_but_not_the_row(tmp_path):
    """A row without a commit still carries a timing, which is what it was
    written for. Dropping it would under-count sessions silently -- the one
    direction this record must not fail in."""
    root = _tree(tmp_path)
    (root / ".git").write_text("not a gitdir pointer at all\n", encoding="utf-8")
    proc = _run(root)
    row = _one_row(root, proc)
    assert row["head"] is None
    assert collector()._ledger_head(root) is None


# --- Durability ---------------------------------------------------------------


class _HeldLock:
    """Hold an exclusive flock on a path for a fixed time, from another thread."""

    def __init__(self, path: Path, seconds: float):
        self.path, self.seconds = path, seconds
        self.acquired = threading.Event()
        self._thread = threading.Thread(target=self._hold, daemon=True)

    def _hold(self):
        import fcntl
        handle = os.open(str(self.path), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
        try:
            fcntl.flock(handle, fcntl.LOCK_EX)
            self.acquired.set()
            time.sleep(self.seconds)
            fcntl.flock(handle, fcntl.LOCK_UN)
        finally:
            os.close(handle)

    def __enter__(self):
        self._thread.start()
        assert self.acquired.wait(5), "could not take the probe lock"
        return self

    def __exit__(self, *exc):
        self._thread.join(timeout=10)
        return False


def test_a_lock_held_past_the_deadline_costs_the_row_not_the_session(tmp_path):
    """The ceiling. A collector that waited indefinitely for a lock would hang
    the session it was measuring, which is the one cost a measurement may never
    impose."""
    module = collector()
    path = tmp_path / "held.jsonl"
    control_start = time.monotonic()
    assert module._ledger_append(path, '{"control":1}')
    control_elapsed = time.monotonic() - control_start
    with _HeldLock(path, 2.0):
        start = time.monotonic()
        wrote = module._ledger_append(path, '{"blocked":1}')
        elapsed = time.monotonic() - start
    assert wrote is False
    assert elapsed < control_elapsed + 1.0, elapsed
    assert path.read_text(encoding="utf-8").count("blocked") == 0


def test_a_lock_released_within_the_deadline_is_waited_for(tmp_path):
    """The floor, and the half that exercises the retry loop at all. An
    implementation with no retry gives up instantly, writes nothing, and passes
    the ceiling test above on its own."""
    module = collector()
    path = tmp_path / "brief.jsonl"
    with _HeldLock(path, 0.08):
        assert module._ledger_append(path, '{"waited":1}') is True
    assert "waited" in path.read_text(encoding="utf-8")
    # The same call with no deadline gives up, which is what makes the assertion
    # above evidence rather than a coincidence of timing.
    other = tmp_path / "nodeadline.jsonl"
    with _HeldLock(other, 0.08):
        assert module._ledger_append(other, '{"gave-up":1}', deadline_s=0.0) is False


def test_a_partial_tail_is_repaired_and_both_lines_survive(tmp_path):
    """A session killed mid-write leaves a fragment. Appending straight after it
    would splice the fragment onto the next row and lose two sessions instead of
    one -- and the fragment itself must stay visible, because it is evidence
    about the ledger's own reliability."""
    module = collector()
    path = tmp_path / "torn.jsonl"
    path.write_text('{"ts_start":"2026-08-21T00:00:00+00:00","wall',
                    encoding="utf-8")
    assert module._ledger_append(path, json.dumps(_row_template(module))) is True
    rows, malformed = reader().read_ledger(path)
    assert len(malformed) == 1
    assert len(rows) == 1
    assert rows[0]["scope"] == "full"


# --- The collector's own cost -------------------------------------------------


def test_the_collector_records_its_own_cost_and_the_cost_is_small(tmp_path):
    """A ledger whose headline figure is the suite's wall clock must be able to
    say how much of that figure is itself, or the number is unattributable.
    Five runs each way, back to back, same interpreter."""
    enabled_root = _tree(tmp_path / "enabled")
    disabled_root = _tree(tmp_path / "disabled")
    enabled_wall, disabled_wall = [], []
    for _ in range(5):
        start = time.monotonic()
        _run(enabled_root)
        enabled_wall.append(time.monotonic() - start)
        start = time.monotonic()
        _run(disabled_root, env={"CAIRN_SUITE_LEDGER": "0"})
        disabled_wall.append(time.monotonic() - start)
    rows = _rows(enabled_root)
    assert len(rows) == 5
    reported = sorted(row["collector_ms"] for row in rows)
    assert all(isinstance(value, float) and value > 0 for value in reported), rows
    median_reported = reported[len(reported) // 2]
    enabled_median = sorted(enabled_wall)[2]
    disabled_median = sorted(disabled_wall)[2]
    delta_ms = (enabled_median - disabled_median) * 1000
    # An absolute ceiling rather than a ratio against `delta_ms`: subprocess
    # start-up noise is tens of milliseconds and the collector is a fraction of
    # one, so a ratio would be a coin toss. The ceiling is what actually matters
    # -- the collector must not be a measurable share of the figure it reports.
    assert median_reported < 50.0, (median_reported, delta_ms)
    assert delta_ms < 100.0, (median_reported, delta_ms, enabled_wall, disabled_wall)


# --- What the reader tells a person -------------------------------------------


def _rendered(tmp_path: Path, rows, extra_lines=()) -> str:
    module = reader()
    path = tmp_path / "rendered.jsonl"
    lines = [json.dumps(row) for row in rows] + list(extra_lines)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    parsed, malformed = module.read_ledger(path)
    return module.render(parsed, malformed, path)


def _reader_row(module, day, start, end, **overrides):
    row = _row_template(module,
                        ts_start=f"2026-08-{day}T{start}+00:00",
                        ts_end=f"2026-08-{day}T{end}+00:00")
    row.update(overrides)
    return row


def test_the_report_opens_by_telling_the_reader_not_to_re_run_the_suite(tmp_path):
    """The action this record exists to prevent. If the opening does not say so,
    a reader who is already half-decided to re-run will re-run."""
    text = _rendered(tmp_path, [_reader_row(collector(), "19", "10:00:00",
                                            "10:02:00")])
    opening = text.split("##")[0]
    assert "Do not re-run the suite" in opening
    assert "already" in opening


def test_the_report_counts_complete_runs_per_day_and_never_per_plan(tmp_path):
    """No field binds a session to a piece of work, so a per-plan figure would
    be invented. Saying so is part of the figure."""
    module = collector()
    text = _rendered(tmp_path, [
        _reader_row(module, "19", "10:00:00", "10:02:00"),
        _reader_row(module, "20", "10:00:00", "10:02:00"),
    ])
    assert "per day, never per plan" in text
    assert "2026-08-19** -- 1 complete run" in text
    assert "2026-08-20** -- 1 complete run" in text


def test_the_report_claims_only_that_another_recorded_session_overlapped(
        tmp_path):
    """Release, nested, opted-out and crashed sessions leave no row, so "nothing
    else was running" is a claim this record can never support. The weaker
    phrasing is the true one."""
    module = collector()
    text = _rendered(tmp_path, [
        _reader_row(module, "19", "10:00:00", "10:02:00"),
        _reader_row(module, "19", "10:01:00", "10:03:00"),
    ])
    assert "overlapped another recorded top-level session" in text
    assert "another suite was running" not in text


def test_the_report_states_the_session_count_as_a_lower_bound(tmp_path):
    """Every exclusion removes sessions silently, so the count is a floor. A
    reader who took it as a total would mis-read every per-session average built
    on it."""
    text = _rendered(tmp_path, [_reader_row(collector(), "19", "10:00:00",
                                            "10:02:00")])
    assert "lower bound" in text


def test_the_report_names_working_tree_state_as_unknown(tmp_path):
    """The collector does not record whether the tree was dirty, so the reader
    must not imply it observed a condition nobody collected. Reporting it as
    clean would attribute a measurement to a commit that never produced it."""
    text = _rendered(tmp_path, [_reader_row(collector(), "19", "10:00:00",
                                            "10:02:00")])
    assert "`unknown`, not clean" in text


def test_the_report_surfaces_an_unreadable_line_rather_than_dropping_it(tmp_path):
    """An unreadable line is usually a session killed mid-write. Skipping it
    silently turns a visible durability problem into an invisible under-count."""
    text = _rendered(tmp_path, [_reader_row(collector(), "19", "10:00:00",
                                            "10:02:00")],
                     extra_lines=["{this is not json}"])
    assert "Unreadable lines" in text
    assert "{this is not json}" in text
    assert "Line 2" in text


def test_the_report_says_when_a_breakdown_was_pruned(tmp_path):
    """A concentration table built from pruned rows understates both the file
    count and the total. Presenting it without that caveat invites a reader to
    conclude the cheap files are free."""
    module = collector()
    text = _rendered(tmp_path, [
        _reader_row(module, "19", "10:00:00", "10:02:00",
                    by_file={"bootstrap/tests/test_a.py": 90000},
                    by_file_total=40, by_file_kept=1),
    ])
    assert "kept 1 of 40 files measured" in text
    assert "understates" in text


def test_the_report_names_every_condition_a_figure_depends_on(tmp_path):
    """A duration with no conditions attached is the thing this record replaces.
    Date, commit, interpreter and overlap travel with every row."""
    module = collector()
    text = _rendered(tmp_path, [
        _reader_row(module, "19", "10:00:00", "10:02:00", head="b" * 40,
                    interpreter="cpython 3.13.13"),
    ])
    assert "2026-08-19" in text
    assert "bbbbbbbbbbbb" in text
    assert "cpython 3.13.13" in text
    assert "no overlap with another recorded session" in text
