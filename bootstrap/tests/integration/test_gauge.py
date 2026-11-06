# SPDX-License-Identifier: MIT
"""Public JUnit pulse behavior through the gauge command line."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
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


def _inventory(path: Path, tiers: list[dict], total: dict | None = None) -> Path:
    value = {
        "schema": "cairn-test-inventory/1",
        "counting_method": "recursive-test-files-utf8-replace-splitlines-v1",
        "tiers": tiers,
        "total": total or {
            "files": sum(tier["files"] for tier in tiers),
            "lines": sum(tier["lines"] for tier in tiers),
        },
    }
    path.write_text(json.dumps(value), encoding="utf-8")
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


def test_before_after_pulse_reports_aggregate_growth_and_runtime_deltas(tmp_path):
    before_report = _junit(tmp_path / "before.xml")
    after_report = tmp_path / "after.xml"
    after_report.write_text(
        '<testsuite tests="2" time="4">'
        '<testcase classname="pkg.a" name="pass" time="1" />'
        '<testcase classname="pkg.a" name="second" time="2" />'
        '</testsuite>',
        encoding="utf-8",
    )
    before_inventory = _inventory(tmp_path / "before-inventory.json", [
        {"name": "unit", "files": 2, "lines": 10},
        {"name": "contract", "files": 1, "lines": 5},
    ])
    after_inventory = _inventory(tmp_path / "after-inventory.json", [
        {"name": "unit", "files": 3, "lines": 14},
        {"name": "integration", "files": 1, "lines": 8},
    ])
    record = _record(_run(
        "--json", "--before-junit-report", str(before_report),
        "--junit-report", str(after_report),
        "--before-tier-inventory", str(before_inventory),
        "--tier-inventory", str(after_inventory),
        "--before-commit-label", "baseline-a", "--commit-label", "candidate-b",
        "--before-python-label", "3.13.13", "--python-label", "3.13.13",
        "--before-selection-label", "bounded", "--selection-label", "bounded",
        "--before-seed-label", "0", "--seed-label", "0",
    ))

    assert record["case_records"] == 2
    assert record["comparison"]["snapshot_commits_distinct"] is True
    assert record["comparison"]["labels"]["python_selection_seed"] == "not_assessed"
    assert record["comparison"]["case_record_delta"] == -2
    assert record["comparison"]["case_records_are_unique_tests"] is False
    assert record["comparison"]["testcase_phase_seconds_delta"] == -3.0
    assert record["comparison"]["testsuite_session_seconds_delta"] == -6.0
    growth = record["comparison"]["tier_inventory"]
    assert growth["status"] == "known"
    assert growth["files_delta"] == 1
    assert growth["lines_delta"] == 7
    assert growth["shared_tiers"] == [{
        "name": "unit", "before_files": 2, "after_files": 3,
        "files_delta": 1, "before_lines": 10, "after_lines": 14,
        "lines_delta": 4,
    }]
    assert growth["unequal_tiers"] == {
        "before_only": ["contract"], "after_only": ["integration"],
    }


def test_growth_does_not_fill_missing_tiers_or_imply_test_equivalence(tmp_path):
    report_before = _junit(tmp_path / "before.xml")
    report_after = tmp_path / "after.xml"
    report_after.write_text(
        '<testsuite tests="4" failures="0" time="10">'
        '<testcase classname="different" name="a" time="1" />'
        '<testcase classname="different" name="b" time="2" />'
        '<testcase classname="different" name="c" time="3" />'
        '<testcase classname="different" name="d" time="0" />'
        '</testsuite>', encoding="utf-8")
    inv_before = _inventory(tmp_path / "before-inventory.json", [
        {"name": "unit", "files": 1, "lines": 3},
    ])
    inv_after = _inventory(tmp_path / "after-inventory.json", [
        {"name": "contract", "files": 1, "lines": 3},
    ])
    record = _record(_run(
        "--json", "--before-junit-report", str(report_before),
        "--junit-report", str(report_after),
        "--before-tier-inventory", str(inv_before),
        "--tier-inventory", str(inv_after),
        "--before-python-label", "3.13.13", "--python-label", "3.13.13",
        "--before-selection-label", "same", "--selection-label", "same",
        "--before-seed-label", "1", "--seed-label", "1",
    ))
    comparison = record["comparison"]
    assert comparison["case_record_delta"] == 0
    assert comparison["labels"]["python_selection_seed"] == "not_assessed"
    assert comparison["tier_inventory"]["shared_tiers"] == []
    assert comparison["tier_inventory"]["unequal_tiers"] == {
        "before_only": ["unit"], "after_only": ["contract"],
    }
    assert record["outcomes"] != record["baseline"]["observations"]["outcomes"]


def test_missing_baseline_or_timing_stays_unknown(tmp_path):
    report = tmp_path / "untimed.xml"
    report.write_text('<testsuite tests="1"><testcase name="missing" /></testsuite>',
                      encoding="utf-8")
    record = _record(_run("--json", "--junit-report", str(report)))
    comparison = record["comparison"]
    assert comparison["case_record_delta"] is None
    assert comparison["testcase_phase_seconds_delta"] is None
    assert comparison["testsuite_session_seconds_delta"] is None
    assert comparison["labels"]["python_selection_seed"] == "unknown"
    assert comparison["tier_inventory"]["status"] == "unknown"
    assert comparison["tier_inventory"]["files_delta"] is None
    assert comparison["baseline"]["observations"] is None


@pytest.mark.parametrize("inventory", [
    '{"schema":"cairn-test-inventory/1","schema":"cairn-test-inventory/1",'
    '"counting_method":"recursive-test-files-utf8-replace-splitlines-v1",'
    '"tiers":[],"total":{"files":0,"lines":0}}',
    '{"schema":"wrong","counting_method":"recursive-test-files-utf8-replace-splitlines-v1",'
    '"tiers":[],"total":{"files":0,"lines":0}}',
    '{"schema":"cairn-test-inventory/1","counting_method":"wrong",'
    '"tiers":[],"total":{"files":0,"lines":0}}',
])
def test_inventory_duplicate_keys_and_wrong_schema_are_rejected(tmp_path, inventory):
    path = tmp_path / "inventory.json"
    path.write_text(inventory, encoding="utf-8")
    result = _run("--tier-inventory", str(path))
    assert result.returncode != 0
    assert "tier-inventory" in result.stderr
    assert str(tmp_path) not in result.stderr


@pytest.mark.parametrize("files,lines,total_files,total_lines", [
    (True, 0, 1, 0),
    (-1, 0, -1, 0),
    (1, 0, 0, 0),
    (1 << 63, 0, 1 << 63, 0),
])
def test_inventory_rejects_bool_negative_overflow_and_unreconciled_totals(
        tmp_path, files, lines, total_files, total_lines):
    value = {
        "schema": "cairn-test-inventory/1",
        "counting_method": "recursive-test-files-utf8-replace-splitlines-v1",
        "tiers": [{"name": "unit", "files": files, "lines": lines}],
        "total": {"files": total_files, "lines": total_lines},
    }
    path = tmp_path / "inventory.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    result = _run("--tier-inventory", str(path))
    assert result.returncode != 0
    assert "tier-inventory" in result.stderr
    assert str(tmp_path) not in result.stderr


@pytest.mark.parametrize("tiers", [
    [{"name": "unit", "files": 1, "lines": 0},
     {"name": "unit", "files": 1, "lines": 0}],
    [{"name": "../unit", "files": 0, "lines": 0}],
    [{"name": f"tier-{index}", "files": 0, "lines": 0}
     for index in range(33)],
])
def test_inventory_rejects_duplicate_unsafe_and_excess_tiers(tmp_path, tiers):
    path = _inventory(tmp_path / "inventory.json", tiers)
    result = _run("--tier-inventory", str(path))
    assert result.returncode != 0
    assert "tier-inventory" in result.stderr
    assert str(tmp_path) not in result.stderr


def test_inventory_is_bounded_to_64_kibibytes_and_link_safe(tmp_path):
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * (64 * 1024 + 1))
    result = _run("--tier-inventory", str(oversized))
    assert result.returncode != 0
    assert "tier-inventory" in result.stderr
    assert str(tmp_path) not in result.stderr

    target = _inventory(tmp_path / "target.json", [
        {"name": "unit", "files": 0, "lines": 0},
    ])
    link = tmp_path / "linked.json"
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable")
    result = _run("--tier-inventory", str(link))
    assert result.returncode != 0
    assert str(tmp_path) not in result.stderr

    real_dir = tmp_path / "real"
    real_dir.mkdir()
    _inventory(real_dir / "nested.json", [])
    parent_link = tmp_path / "linked-dir"
    parent_link.symlink_to(real_dir, target_is_directory=True)
    result = _run("--tier-inventory", str(parent_link / "nested.json"))
    assert result.returncode != 0
    assert str(tmp_path) not in result.stderr

    if hasattr(os, "mkfifo"):
        fifo = tmp_path / "inventory.fifo"
        os.mkfifo(fifo)
        result = _run("--tier-inventory", str(fifo))
        assert result.returncode != 0
        assert str(tmp_path) not in result.stderr


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


def test_before_and_after_reports_share_the_eight_report_limit(tmp_path):
    paths = [str(_junit(tmp_path / f"report-{index}.xml")) for index in range(9)]
    result = _run(*sum(([
        ("--before-junit-report" if index < 5 else "--junit-report"), path,
    ] for index, path in enumerate(paths)), []))
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
    inventory = _inventory(tmp_path / "inventory.json", [
        {"name": "unit", "files": 1, "lines": 2},
    ])
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
    result = _run("--json", "--junit-report", str(report),
                  "--tier-inventory", str(inventory), env=env)
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


def test_mismatched_before_labels_are_reported_without_equivalence_claim(tmp_path):
    before = _junit(tmp_path / "before.xml")
    after = _junit(tmp_path / "after.xml")
    record = _record(_run(
        "--json", "--before-junit-report", str(before),
        "--junit-report", str(after),
        "--before-commit-label", "commit-a", "--commit-label", "commit-b",
        "--before-python-label", "3.13.12", "--python-label", "3.13.13",
        "--before-selection-label", "bounded", "--selection-label", "wide",
        "--before-seed-label", "0", "--seed-label", "1",
    ))
    assert record["comparison"]["snapshot_commits_distinct"] is True
    assert record["comparison"]["labels"]["python_selection_seed"] == "labels_differ"
    assert record["comparison"]["case_record_delta"] == 0
    assert record["comparison"]["testcase_phase_seconds_delta"] == 0
    assert record["comparison"]["testsuite_session_seconds_delta"] == 0


def test_non_pulse_mode_rejects_before_and_inventory_inputs(tmp_path):
    inventory = _inventory(tmp_path / "inventory.json", [])
    result = subprocess.run(
        [sys.executable, str(GAUGE), "--tier-inventory", str(inventory)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert result.returncode != 0
    assert "require --pulse" in result.stderr
