# SPDX-License-Identifier: MIT
"""Public JUnit pulse behavior through the gauge command line."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
GAUGE = ROOT / "tools" / "gauge.py"


def _run(*args: str, env=None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GAUGE), "--pulse", *args],
        cwd=ROOT, env=env, capture_output=True, text=True, check=False,
    )


def _junit(path: Path) -> Path:
    path.write_text(
        """<?xml version="1.0"?>
<testsuites tests="4" failures="1" errors="1" skipped="1" time="10">
  <testsuite tests="4" failures="1" errors="1" skipped="1" time="9">
    <testcase classname="pkg.a" name="pass" time="1" />
    <testcase classname="pkg.a" name="failure" time="2"><failure>private body</failure></testcase>
    <testcase classname="pkg.b" name="error" time="3"><error>private body</error></testcase>
    <testcase classname="pkg.b" name="skip" time="0"><skipped /></testcase>
  </testsuite>
</testsuites>
""",
        encoding="utf-8",
    )
    return path


def _record(result: subprocess.CompletedProcess) -> dict:
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_testsuites_and_testsuite_counts_keep_phase_and_session_time_distinct(tmp_path):
    suite = _junit(tmp_path / "suite.xml")
    single = tmp_path / "single.xml"
    single.write_text(
        '<testsuite tests="1" time="2"><testcase name="one" time="0.5" /></testsuite>',
        encoding="utf-8",
    )
    record = _record(_run("--json", "--junit-report", str(suite),
                          "--junit-report", str(single)))

    assert record["schema"] == "cairn-pulse/1"
    assert record["reports"][0]["case_records"] == 4
    assert record["reports"][0]["outcomes"]["failures"] == 1
    assert record["reports"][1]["case_records"] == 1
    assert record["reports"][1]["outcomes"]["passed"] == 1
    assert record["case_records"] == 5
    assert record["outcomes"] == {
        "passed": 2, "failures": 1, "errors": 1, "skipped": 1,
    }
    assert record["testcase_phase_seconds"] == 6.5
    assert record["testsuite_session_seconds"] == 12.0
    assert record["coverage"]["report_count"] == 2
    assert record["coverage"]["possible_duplicate_case_records"] is True
    assert record["coverage"]["case_records_are_unique_tests"] is False
    assert record["coverage"]["comparability"] == "unknown"
    assert set(record["coverage"]["usage"].values()) == {"UNKNOWN"}
    assert "private body" not in result_text(record)


def result_text(record: dict) -> str:
    return json.dumps(record)


def test_repeated_execution_is_counted_again_and_missing_values_stay_unknown(tmp_path):
    report = _junit(tmp_path / "same.xml")
    record = _record(_run("--json", "--junit-report", str(report),
                          "--junit-report", str(report),
                          "--commit-label", "abc", "--python-label", "3.13.13",
                          "--selection-label", "bounded", "--seed-label", "0"))
    assert record["case_records"] == 8
    assert record["testcase_phase_seconds"] == 12.0
    assert record["testsuite_session_seconds"] == 20.0
    assert record["coverage"]["comparability"] == "not_assessed"
    assert all(record["coverage"]["labels_present"].values())
    assert record["coverage"]["labels_present"]["python"] == "3.13.13"


def test_no_report_is_honestly_unknown_and_does_not_call_usage_zero():
    record = _record(_run("--json"))
    assert record["case_records"] == 0
    assert record["coverage"]["complete"] is False
    assert record["coverage"]["report_count"] == 0
    assert record["coverage"]["comparability"] == "unknown"
    assert set(record["coverage"]["usage"].values()) == {"UNKNOWN"}
    assert record["coverage"]["private_collection_join"] == "not_performed"


def test_missing_case_and_session_times_remain_separately_unknown(tmp_path):
    report = tmp_path / "untimed.xml"
    report.write_text('<testsuite tests="1"><testcase name="untimed" /></testsuite>',
                      encoding="utf-8")
    record = _record(_run("--json", "--junit-report", str(report)))
    assert record["testcase_phase_seconds"] == 0
    assert record["testsuite_session_seconds"] == 0
    assert record["coverage"]["phase_time_unknown_cases"] == 1
    assert record["coverage"]["session_time_unknown_reports"] == 1


def test_more_than_eight_reports_is_rejected(tmp_path):
    paths = []
    for index in range(9):
        paths.append(str(_junit(tmp_path / f"report-{index}.xml")))
    result = _run(*sum((["--junit-report", path] for path in paths), []))
    assert result.returncode != 0
    assert "at most 8" in result.stderr
    assert str(tmp_path) not in result.stderr


@pytest.mark.parametrize("xml", [
    "<testsuite>",
    '<!DOCTYPE testsuite [<!ENTITY x "bad">]><testsuite>&x;</testsuite>',
    '<testsuite><testcase time="NaN" /></testsuite>',
    '<testsuite><testcase time="-0.1" /></testsuite>',
    '<testsuites time="1"><testsuite time="Infinity" /></testsuites>',
    '<?xml version="1.0" encoding="UTF-16"?><testsuite/>',
    '<testsuite tests="2"><testcase /></testsuite>',
    '<testsuite failures="1"><testcase><error /></testcase></testsuite>',
    '<testsuite><testcase><failure /><skipped /></testcase></testsuite>',
])
def test_invalid_xml_and_impossible_counts_fail_without_echoing_input(tmp_path, xml):
    report = tmp_path / "bad.xml"
    report.write_text(xml, encoding="utf-8")
    result = _run("--json", "--junit-report", str(report))
    assert result.returncode != 0
    assert "pulse incomplete" in result.stderr
    assert str(report) not in result.stderr
    assert xml not in result.stderr


def test_utf16_and_nul_are_rejected_before_xml_parsing(tmp_path):
    utf16 = tmp_path / "utf16.xml"
    utf16.write_bytes('<testsuite/>'.encode("utf-16"))
    nul = tmp_path / "nul.xml"
    nul.write_bytes(b"<testsuite>\0</testsuite>")
    for report in (utf16, nul):
        result = _run("--junit-report", str(report))
        assert result.returncode != 0
        assert str(report) not in result.stderr


def test_missing_and_oversized_reports_fail_with_only_alias_diagnostics(tmp_path):
    missing = tmp_path / "missing.xml"
    result = _run("--junit-report", str(missing))
    assert result.returncode != 0
    assert "report-1" in result.stderr
    assert str(tmp_path) not in result.stderr

    oversized = tmp_path / "large.xml"
    oversized.write_bytes(b" " * (8 * 1024 * 1024 + 1))
    result = _run("--junit-report", str(oversized))
    assert result.returncode != 0
    assert "report-1" in result.stderr
    assert str(tmp_path) not in result.stderr


def test_linked_report_and_fifo_are_refused(tmp_path):
    target = _junit(tmp_path / "target.xml")
    link = tmp_path / "linked.xml"
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable")
    result = _run("--junit-report", str(link))
    assert result.returncode != 0
    assert str(tmp_path) not in result.stderr

    real_dir = tmp_path / "real"
    real_dir.mkdir()
    _junit(real_dir / "nested.xml")
    parent_link = tmp_path / "linked-dir"
    parent_link.symlink_to(real_dir, target_is_directory=True)
    result = _run("--junit-report", str(parent_link / "nested.xml"))
    assert result.returncode != 0
    assert str(tmp_path) not in result.stderr

    if hasattr(os, "mkfifo"):
        fifo = tmp_path / "report.fifo"
        os.mkfifo(fifo)
        result = _run("--junit-report", str(fifo))
        assert result.returncode != 0
        assert str(tmp_path) not in result.stderr


def test_pulse_never_executes_git_or_target_python(tmp_path):
    report = _junit(tmp_path / "public.xml")
    marker = tmp_path / "executed"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("git", "python", "python3"):
        command = bin_dir / name
        command.write_text(f"#!/bin/sh\nprintf x >> '{marker}'\n", encoding="utf-8")
        command.chmod(0o755)
    env = os.environ.copy()
    env["PATH"] = str(bin_dir)
    env.pop("GIT_CONFIG_GLOBAL", None)
    result = _run("--json", "--junit-report", str(report), env=env)
    assert result.returncode == 0, result.stderr
    assert not marker.exists()


def test_pulse_rejects_snapshot_and_target_root():
    assert _run("--snapshot").returncode != 0
    result = subprocess.run(
        [sys.executable, str(GAUGE), "--pulse", "--root", str(ROOT)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert result.returncode != 0


def test_json_without_pulse_refuses_before_git(monkeypatch):
    import importlib.util

    spec = importlib.util.spec_from_file_location("gauge_cli", GAUGE)
    gauge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gauge)

    def unexpected_git(*args, **kwargs):
        pytest.fail("--json without --pulse must not invoke Git")

    monkeypatch.setattr(gauge.subprocess, "run", unexpected_git)
    with pytest.raises(SystemExit) as stopped:
        gauge.main(["--json"])
    assert stopped.value.code == 2


def test_unsafe_label_is_not_echoed(tmp_path):
    report = _junit(tmp_path / "report.xml")
    result = _run("--junit-report", str(report), "--commit-label", str(tmp_path))
    assert result.returncode != 0
    assert "report labels" in result.stderr
    assert str(tmp_path) not in result.stderr
