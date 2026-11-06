"""File-level release evidence through real pytest XML and the public comparator.

Small isolated release-shaped fixtures do not run Cairn's certifying suite.
The independent manifest bytes and expected names come from the real tree.
"""
from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts/check_release_test_members.py"
DOC = ROOT / "docs/release-process.md"
MANIFEST = ROOT / "bootstrap/tests/security_manifest.py"
VICTIM = "bootstrap/tests/test_security_lint.py"


@pytest.fixture
def project(tmp_path: Path) -> Path:
    tests = tmp_path / "bootstrap/tests"
    tests.mkdir(parents=True)
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    shutil.copyfile(SCRIPT, scripts / SCRIPT.name)
    shutil.copyfile(MANIFEST, tests / MANIFEST.name)
    tree = ast.parse(MANIFEST.read_text(encoding="utf-8"))
    family = next(ast.literal_eval(node.value) for node in tree.body
                  if isinstance(node, ast.AnnAssign)
                  and isinstance(node.target, ast.Name)
                  and node.target.id == "SECURITY_FAMILY")
    for name in [*family, "test_security_marker.py"]:
        (tests / name).write_text("def test_pass():\n    assert True\n", encoding="utf-8")
    # The fixture preserves the release option, not the suite's shuffle engine.
    (tmp_path / "conftest.py").write_text(
        'def pytest_addoption(parser):\n'
        '    parser.addoption("--quality-gate-shuffle-seed")\n', encoding="utf-8")
    return tmp_path


def _env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("CAIRN_FULL_SUITE", None)
    env.pop("CAIRN_RELEASE_GATE_ACTIVE", None)
    env.pop("PYTEST_ADDOPTS", None)
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    return env


def _sequence(root: Path, *, omit: str | None = None, adopter: bool = False,
              family: str = "xunit2", preexisting: bool = False) -> subprocess.CompletedProcess:
    block = re.search(r"```bash\n(\(\n.*?\n\))\n```", DOC.read_text(), re.S)
    assert block is not None
    command = block.group(1)
    assert "CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0" in command
    # Only a tiny fixture is executed. Never set the certification override.
    command = command.replace("CAIRN_FULL_SUITE=1 ", "")
    option = f"--quality-gate-shuffle-seed=0 -o junit_family={family}"
    if omit:
        option += f" --ignore={omit}"
    command = command.replace("--quality-gate-shuffle-seed=0", option)
    if adopter:
        command = command.replace("python scripts/check_release_test_members.py",
                                  "python scripts/check_release_test_members.py --required-files required.json")
    if preexisting:
        command = command.replace('report="$report_dir/pytest.xml"',
                                  'report="$report_dir/pytest.xml"\ntouch "$report"')
    return subprocess.run(["bash", "-c", command], cwd=root, env=_env(),
                          capture_output=True, text=True, timeout=30)


@pytest.mark.parametrize("family", ["xunit1", "xunit2"])
def test_actual_pytest_identities_and_documented_sequence(project: Path, family: str):
    result = _sequence(project, family=family)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "release membership: PASS: 18 required files" in result.stdout


@pytest.mark.parametrize("omit", [VICTIM, "bootstrap/tests/test_security_marker.py"])
def test_actual_security_omission_fails_after_pytest_passes(project: Path, omit: str):
    result = _sequence(project, omit=omit)
    assert result.returncode != 0
    assert "17 passed" in result.stdout
    assert omit in result.stderr


@pytest.mark.parametrize("omit", [False, True])
def test_adopter_owned_slow_selection_is_independent(project: Path, omit: bool):
    slow = "bootstrap/tests/test_slow.py"
    (project / slow).write_text("def test_slow():\n    assert True\n")
    (project / "required.json").write_text(json.dumps([slow]))
    result = _sequence(project, adopter=True, omit=slow if omit else None)
    assert "passed" in result.stdout
    assert (result.returncode != 0) is omit, result.stdout + result.stderr
    if omit:
        assert slow in result.stderr


def test_pytest_failure_is_preserved_even_if_comparison_passes(project: Path):
    (project / "bootstrap/tests/test_optional.py").write_text(
        "def test_optional():\n    assert False\n")
    result = _sequence(project)
    assert result.returncode == 1
    assert "release membership: PASS" in result.stdout
    assert "1 failed" in result.stdout


def test_documented_sequence_refuses_existing_report_path(project: Path):
    result = _sequence(project, preexisting=True)
    assert result.returncode != 0
    assert "passed" not in result.stdout
    assert "release membership" not in result.stdout + result.stderr


def _xml(*, classname: str = "bootstrap.tests.test_security_lint",
         name: str = "test_ok", outcome: str | None = None) -> ET.Element:
    suite = ET.Element("testsuite", tests="1", failures="0", errors="0", skipped="0")
    case = ET.SubElement(suite, "testcase", classname=classname, name=name)
    if outcome:
        ET.SubElement(case, outcome)
        suite.set({"failure": "failures", "error": "errors", "skipped": "skipped"}[outcome], "1")
    return suite


def _check(root: Path, report: Path, start: int, *, configured: bool = True):
    args = [sys.executable, str(root / "scripts" / SCRIPT.name), str(report),
            "--started-ns", str(start)]
    if configured:
        args += ["--required-files", str(root / "required.json")]
    return subprocess.run(args, cwd=root, env=_env(), capture_output=True,
                          text=True, timeout=10)


@pytest.fixture
def evidence(project: Path):
    report = project / "report.xml"
    (project / "required.json").write_text(json.dumps([VICTIM]))
    start = time.time_ns()
    ET.ElementTree(_xml()).write(report, encoding="utf-8")
    return project, report, start


def test_minimal_report_passes(evidence):
    root, report, start = evidence
    assert _check(root, report, start).returncode == 0


@pytest.mark.parametrize("fault", [
    "absent", "stale", "future", "malformed", "dtd", "utf16", "symlink", "oversized",
    "empty", "counts", "duplicate", "two-suites", "unknown-class", "ambiguous-class",
    "file-disagrees", "missing-name", "nested-case", "two-outcomes", "no-success",
    "skipped", "failure", "error", "missing-source",
])
def test_report_refusals(evidence, fault: str):
    root, report, start = evidence
    suite = _xml()
    case = suite.find("testcase")
    assert case is not None
    if fault == "absent":
        report.unlink()
    elif fault in {"stale", "future"}:
        stamp = start - 1 if fault == "stale" else time.time_ns() + 10**12
        os.utime(report, ns=(stamp, stamp))
    elif fault == "malformed":
        report.write_text("<broken")
    elif fault == "dtd":
        report.write_text('<!DOCTYPE x [<!ENTITY x "boom">]><testsuite/>')
    elif fault == "utf16":
        report.write_bytes(ET.tostring(suite, encoding="utf-16"))
    elif fault == "symlink":
        target = report.with_name("target.xml")
        report.rename(target)
        report.symlink_to(target)
    elif fault == "oversized":
        with report.open("wb") as handle:
            handle.truncate(32 * 1024 * 1024 + 1)
    elif fault == "missing-source":
        (root / VICTIM).unlink()
    else:
        if fault == "empty":
            suite.remove(case)
            suite.set("tests", "0")
        elif fault == "counts":
            suite.set("tests", "9")
        elif fault == "duplicate":
            suite.append(ET.fromstring(ET.tostring(case)))
            suite.set("tests", "2")
        elif fault == "two-suites":
            container = ET.Element("testsuites")
            container.extend([suite, ET.fromstring(ET.tostring(suite))])
            suite = container
        elif fault == "unknown-class":
            case.set("classname", "not.a.source.file")
        elif fault == "ambiguous-class":
            (root / "bootstrap.tests.test_security_lint.py").write_text("")
        elif fault == "file-disagrees":
            case.set("file", "bootstrap/tests/test_security_marker.py")
        elif fault == "missing-name":
            case.attrib.pop("name")
        elif fault == "nested-case":
            ET.SubElement(case, "testcase")
        elif fault == "two-outcomes":
            ET.SubElement(case, "skipped")
            ET.SubElement(case, "failure")
        elif fault == "no-success":
            case.set("classname", "bootstrap.tests.test_security_marker")
        else:
            suite = _xml(outcome=fault)
        ET.ElementTree(suite).write(report, encoding="utf-8")
    result = _check(root, report, start)
    assert result.returncode != 0, fault
    assert "FAIL" in result.stderr


@pytest.mark.parametrize("value", [None, [], {}, [VICTIM, VICTIM], ["../outside.py"],
                                       ["missing.py"], [123], "wrong-type"])
def test_invalid_required_configuration_fails(evidence, value):
    root, report, start = evidence
    config = root / "required.json"
    if value is None:
        config.unlink()
    else:
        config.write_text(json.dumps(value))
    assert _check(root, report, start).returncode != 0


def test_malformed_required_configuration_fails(evidence):
    root, report, start = evidence
    (root / "required.json").write_text("[")
    assert _check(root, report, start).returncode != 0


def test_invalid_start_time_fails(evidence):
    root, report, _start = evidence
    for start in [0, -1, time.time_ns() + 10**12]:
        assert _check(root, report, start).returncode != 0


def test_empty_security_manifest_is_not_a_pass(evidence):
    root, report, start = evidence
    (root / "bootstrap/tests/security_manifest.py").write_text("SECURITY_FAMILY: dict = {}")
    assert _check(root, report, start, configured=False).returncode != 0
