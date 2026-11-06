#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""The staff gauge: how much of what we write is the thing, and how much is
the apparatus around it.

Weekly lines added, split four ways. **Recovery is the product column climbing
back past 50%.**

**Why this exists as a script rather than a table someone maintains.** An
External review re-derived the repository totals to the exact line but could
not reproduce the security / machinery / product split, because the split lived
in one reader's head. A committed classifier and a dated snapshot make the
gauge repeatable month to month by someone who was not there.

**Its epistemic limit, stated rather than implied.** Commit share measures
process *cost*. Caught defects are survivorship evidence of benefit with no
counterfactual, so this gauge can tell you the apparatus is expensive and can
never tell you it was not worth it.

Unclassified paths are **printed, not silently bucketed** -- a path nobody has
classified is the one most likely to be misfiled.

**Two limits it does not paper over.** It walks one repository, so it measures
this repo's share and not the cross-repo totals a hand count covered; and it
does not resolve git's rename notation, so a renamed path reports unclassified
with its (zero) added lines rather than being attributed to a guess.

Usage:

    python tools/gauge.py --since 2026-04-27
    python tools/gauge.py --since 2026-08-01 --snapshot
"""

from __future__ import annotations

import argparse
import collections
import datetime as _dt
import json
import math
import os
import re
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple

#: (prefix, class). First match wins, so order is the rule. `product` is never
#: a default -- an unmatched path is reported as unclassified.
_RULES: Tuple[Tuple[str, str], ...] = (
    ("dev/",                              "dev"),
    ("bootstrap/tests/test_security",     "security-machinery"),
    ("bootstrap/tests/test_gate",         "security-machinery"),
    ("bootstrap/tests/test_reanchor",     "security-machinery"),
    ("bootstrap/tests/test_ast_attest",   "security-machinery"),
    ("bootstrap/security_check.py",       "security-machinery"),
    ("bootstrap/SAFETY.md",               "security-machinery"),
    ("SECURITY.md",                       "security-machinery"),
    ("scripts/quality_gate.py",           "security-machinery"),
    ("scripts/content_scan.py",           "security-machinery"),
    ("scripts/run_portable_security",     "security-machinery"),
    ("templates/modules/team-gated/run_portable_security", "security-machinery"),
    ("bootstrap/",                        "other-machinery"),
    ("tools/",                            "other-machinery"),
    ("scripts/",                          "other-machinery"),
    ("templates/skills/_lib/",            "other-machinery"),
    ("templates/modules/",                "other-machinery"),
    ("docs/methodology/",               "product"),
    ("docs/",                             "product"),
    ("templates/",                        "product"),
    ("on-ramp/",                          "product"),
    ("examples/",                         "product"),
    ("README.md",                         "product"),
    ("AGENTS.md",                         "product"),
    ("CHANGELOG.md",                      "product"),
    ("dimensions/",                       "product"),
    ("case-studies/",                     "product"),
    ("LICENSE",                           "product"),
    ("NOTICE.md",                         "product"),
    ("CITATION.cff",                      "product"),
    ("CLAUDE.md",                         "product"),
    ("VENDOR.md",                         "product"),
    (".agents/",                          "other-machinery"),
    (".github/",                          "other-machinery"),
    (".gitignore",                        "other-machinery"),
)

_CLASSES = ("dev", "security-machinery", "other-machinery", "product")
_PULSE_MAX_REPORTS = 8
_PULSE_MAX_REPORT_BYTES = 8 * 1024 * 1024
_PULSE_MAX_TOTAL_BYTES = 64 * 1024 * 1024
_PULSE_MAX_INVENTORY_BYTES = 64 * 1024
_PULSE_MAX_TIERS = 32
_PULSE_MAX_COUNT = (1 << 63) - 1
_INVENTORY_SCHEMA = "cairn-test-inventory/1"
_INVENTORY_COUNTING_METHOD = "recursive-test-files-utf8-replace-splitlines-v1"
_PULSE_OPEN_FLAGS = (os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                     | getattr(os, "O_NONBLOCK", 0)
                     | getattr(os, "O_BINARY", 0))
_PULSE_LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:+-]{0,127}\Z")


class _PulseInputError(ValueError):
    """A public report cannot safely contribute to a pulse."""


def _is_reparse(st: os.stat_result) -> bool:
    attrs = getattr(st, "st_file_attributes", 0)
    return bool(attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _check_report_path(path: Path) -> os.stat_result:
    """Refuse links/reparse points in every named component and special files."""
    absolute = Path(os.path.abspath(os.fspath(path)))
    parts = list(reversed((absolute, *absolute.parents)))
    for part in parts:
        try:
            mode = os.lstat(part)
        except OSError as exc:
            raise _PulseInputError from exc
        if stat.S_ISLNK(mode.st_mode) or _is_reparse(mode):
            raise _PulseInputError
    leaf = os.lstat(absolute)
    if not stat.S_ISREG(leaf.st_mode):
        raise _PulseInputError
    return leaf


def _read_pulse_report(path: Path, limit: int) -> bytes:
    before = _check_report_path(path)
    try:
        fd = os.open(path, _PULSE_OPEN_FLAGS)
    except OSError as exc:
        raise _PulseInputError from exc
    with os.fdopen(fd, "rb") as handle:
        opened = os.fstat(handle.fileno())
        if (not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)):
            raise _PulseInputError
        chunks = []
        remaining = limit + 1
        while remaining:
            chunk = handle.read(min(1024 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        after = os.fstat(handle.fileno())
        name_after = _check_report_path(path)
        identity = lambda st: (st.st_dev, st.st_ino, st.st_size,
                               st.st_mtime_ns, st.st_ctime_ns)
        if (identity(opened) != identity(after)
                or identity(after) != identity(name_after)):
            raise _PulseInputError
    data = b"".join(chunks)
    if len(data) > limit:
        raise _PulseInputError
    return data


def _xml_count(element: ET.Element, name: str) -> Optional[int]:
    raw = element.attrib.get(name)
    if raw is None:
        return None
    if not re.fullmatch(r"[0-9]+", raw):
        raise _PulseInputError
    return int(raw)


def _seconds(raw: Optional[str]) -> Optional[float]:
    if raw is None:
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError, OverflowError) as exc:
        raise _PulseInputError from exc
    if not math.isfinite(value) or value < 0:
        raise _PulseInputError
    return value


def _case_outcome(case: ET.Element) -> str:
    markers = {child.tag for child in case
               if child.tag in {"failure", "error", "skipped"}}
    if len(markers) > 1:
        raise _PulseInputError
    if "error" in markers:
        return "errors"
    if "failure" in markers:
        return "failures"
    if "skipped" in markers:
        return "skipped"
    return "passed"


def _parse_pulse_report(data: bytes) -> dict:
    if b"\0" in data:
        raise _PulseInputError
    try:
        source = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise _PulseInputError from exc
    declaration = re.match(
        r"\s*<\?xml\b[^?]*\bencoding\s*=\s*(['\"])([^'\"]+)\1",
        source, flags=re.IGNORECASE,
    )
    if declaration and declaration.group(2).lower().replace("_", "-") not in {
            "utf-8", "utf8"}:
        raise _PulseInputError
    upper = source.upper()
    if "<!DOCTYPE" in upper or "<!ENTITY" in upper:
        raise _PulseInputError
    try:
        root = ET.fromstring(source)
    except (ET.ParseError, ValueError) as exc:
        raise _PulseInputError from exc
    if root.tag not in {"testsuite", "testsuites"}:
        raise _PulseInputError

    cases = list(root.iter("testcase"))
    outcomes = collections.Counter(_case_outcome(case) for case in cases)
    phase_times = [_seconds(case.attrib.get("time")) for case in cases]
    phase_known = [value for value in phase_times if value is not None]

    for suite in (node for node in root.iter()
                  if node.tag in {"testsuite", "testsuites"}):
        _seconds(suite.attrib.get("time"))
        contained = list(suite.iter("testcase"))
        counts = collections.Counter(_case_outcome(case) for case in contained)
        actual = {
            "tests": len(contained),
            "failures": counts["failures"],
            "errors": counts["errors"],
            "skipped": counts["skipped"],
        }
        for name, value in actual.items():
            declared = _xml_count(suite, name)
            if declared is not None and declared != value:
                raise _PulseInputError

    if root.tag == "testsuite":
        session_raw = root.attrib.get("time")
        session_times = [] if session_raw is None else [_seconds(session_raw)]
        session_unknown = session_raw is None
    elif root.attrib.get("time") is not None:
        session_times = [_seconds(root.attrib["time"])]
        session_unknown = False
    else:
        top_suites = [child for child in root if child.tag == "testsuite"]
        session_times = [_seconds(suite.attrib.get("time")) for suite in top_suites]
        session_unknown = (not session_times
                           or any(value is None for value in session_times))
    known_sessions = [value for value in session_times if value is not None]
    return {
        "cases": len(cases),
        "outcomes": outcomes,
        "phase_seconds": math.fsum(phase_known),
        "phase_known": len(phase_known),
        "phase_unknown": len(phase_times) - len(phase_known),
        "session_seconds": math.fsum(known_sessions),
        "session_known": int(bool(session_times) and not session_unknown),
        "session_unknown": int(session_unknown),
    }


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise _PulseInputError
        result[key] = value
    return result


def _reject_json_constant(_value: str):
    raise _PulseInputError


def _inventory_count(value: object) -> int:
    if type(value) is not int or value < 0 or value > _PULSE_MAX_COUNT:
        raise _PulseInputError
    return value


def _parse_tier_inventory(data: bytes) -> dict:
    if b"\0" in data:
        raise _PulseInputError
    try:
        source = data.decode("utf-8-sig")
        inventory = json.loads(
            source, object_pairs_hook=_unique_json_object,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError,
            ValueError, TypeError) as exc:
        raise _PulseInputError from exc
    if (type(inventory) is not dict
            or set(inventory) != {"schema", "counting_method", "tiers", "total"}
            or inventory["schema"] != _INVENTORY_SCHEMA
            or inventory["counting_method"] != _INVENTORY_COUNTING_METHOD):
        raise _PulseInputError
    tiers = inventory["tiers"]
    total = inventory["total"]
    if type(tiers) is not list or len(tiers) > _PULSE_MAX_TIERS:
        raise _PulseInputError
    if type(total) is not dict or set(total) != {"files", "lines"}:
        raise _PulseInputError
    parsed_tiers = []
    names = set()
    for tier in tiers:
        if type(tier) is not dict or set(tier) != {"name", "files", "lines"}:
            raise _PulseInputError
        name = tier["name"]
        if (not isinstance(name, str) or not _PULSE_LABEL.fullmatch(name)
                or name in names):
            raise _PulseInputError
        names.add(name)
        parsed_tiers.append({
            "name": name,
            "files": _inventory_count(tier["files"]),
            "lines": _inventory_count(tier["lines"]),
        })
    files = _inventory_count(total["files"])
    lines = _inventory_count(total["lines"])
    if (files != sum(tier["files"] for tier in parsed_tiers)
            or lines != sum(tier["lines"] for tier in parsed_tiers)):
        raise _PulseInputError
    return {
        "schema": _INVENTORY_SCHEMA,
        "counting_method": _INVENTORY_COUNTING_METHOD,
        "tiers": parsed_tiers,
        "total": {"files": files, "lines": lines},
    }


def _inventory_comparison(before: Optional[dict], after: Optional[dict]) -> dict:
    if before is None or after is None:
        return {
            "status": "unknown",
            "files_delta": None,
            "lines_delta": None,
            "shared_tiers": [],
            "unequal_tiers": None,
        }
    before_by_name = {tier["name"]: tier for tier in before["tiers"]}
    after_by_name = {tier["name"]: tier for tier in after["tiers"]}
    shared_names = [tier["name"] for tier in after["tiers"]
                    if tier["name"] in before_by_name]
    before_only = [tier["name"] for tier in before["tiers"]
                   if tier["name"] not in after_by_name]
    after_only = [tier["name"] for tier in after["tiers"]
                  if tier["name"] not in before_by_name]
    shared = []
    for name in shared_names:
        old = before_by_name[name]
        new = after_by_name[name]
        shared.append({
            "name": name,
            "before_files": old["files"],
            "after_files": new["files"],
            "files_delta": new["files"] - old["files"],
            "before_lines": old["lines"],
            "after_lines": new["lines"],
            "lines_delta": new["lines"] - old["lines"],
        })
    return {
        "status": "known",
        "before_files": before["total"]["files"],
        "after_files": after["total"]["files"],
        "files_delta": after["total"]["files"] - before["total"]["files"],
        "before_lines": before["total"]["lines"],
        "after_lines": after["total"]["lines"],
        "lines_delta": after["total"]["lines"] - before["total"]["lines"],
        "shared_tiers": shared,
        "unequal_tiers": {"before_only": before_only, "after_only": after_only},
    }


def _label_comparability(before: dict, after: dict) -> str:
    names = ("python", "selection", "seed")
    old = [before.get(name) for name in names]
    new = [after.get(name) for name in names]
    if any(value is None for value in (*old, *new)):
        return "unknown"
    return "not_assessed" if old == new else "labels_differ"


def _comparison_observations(before_reports: list[dict], after_reports: list[dict],
                             before_inventory: Optional[dict],
                             after_inventory: Optional[dict],
                             before_labels: dict, after_labels: dict) -> dict:
    def summarize(reports: list[dict]) -> Optional[dict]:
        if not reports:
            return None
        outcomes = collections.Counter()
        for report in reports:
            outcomes.update(report["outcomes"])
        return {
            "report_count": len(reports),
            "case_records": sum(report["cases"] for report in reports),
            "outcomes": {name: outcomes[name]
                         for name in ("passed", "failures", "errors", "skipped")},
            "testcase_phase_seconds": math.fsum(
                report["phase_seconds"] for report in reports),
            "phase_time_known_cases": sum(report["phase_known"] for report in reports),
            "phase_time_unknown_cases": sum(report["phase_unknown"] for report in reports),
            "testsuite_session_seconds": math.fsum(
                report["session_seconds"] for report in reports),
            "session_time_known_reports": sum(report["session_known"] for report in reports),
            "session_time_unknown_reports": sum(report["session_unknown"] for report in reports),
        }

    before = summarize(before_reports)
    after = summarize(after_reports)
    has_both_runs = before is not None and after is not None
    phase_known = (has_both_runs
                   and before["phase_time_unknown_cases"] == 0
                   and after["phase_time_unknown_cases"] == 0
                   and before["phase_time_known_cases"] > 0
                   and after["phase_time_known_cases"] > 0)
    session_known = (has_both_runs
                     and before["session_time_unknown_reports"] == 0
                     and after["session_time_unknown_reports"] == 0
                     and before["session_time_known_reports"] == len(before_reports)
                     and after["session_time_known_reports"] == len(after_reports))
    before_commit = before_labels.get("commit")
    after_commit = after_labels.get("commit")
    distinct_commits = (None if before_commit is None or after_commit is None
                        else before_commit != after_commit)
    return {
        "baseline": {
            "labels": before_labels,
            "observations": before,
            "tier_inventory": before_inventory,
        },
        "comparison": {
            "labels": {"python_selection_seed": _label_comparability(
                before_labels, after_labels)},
            "snapshot_commits_distinct": distinct_commits,
            "case_record_delta": (
                after["case_records"] - before["case_records"]
                if has_both_runs else None
            ),
            "case_records_are_unique_tests": False,
            "testcase_phase_seconds_delta": (
                after["testcase_phase_seconds"] - before["testcase_phase_seconds"]
                if phase_known else None
            ),
            "testsuite_session_seconds_delta": (
                after["testsuite_session_seconds"] - before["testsuite_session_seconds"]
                if session_known else None
            ),
            "tier_inventory": _inventory_comparison(
                before_inventory, after_inventory),
        },
    }


def _pulse(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    if args.snapshot:
        parser.error("--pulse cannot be combined with --snapshot")
    if args.root is not None:
        parser.error("--root is not available with --pulse")
    all_report_paths = args.junit_report + args.before_junit_report
    if len(all_report_paths) > _PULSE_MAX_REPORTS:
        print("gauge: pulse incomplete: at most 8 reports are accepted", file=sys.stderr)
        return 2

    total_bytes = 0
    parsed = []
    before_parsed = []
    for paths, destination, prefix in (
            (args.junit_report, parsed, "report"),
            (args.before_junit_report, before_parsed, "before-report")):
        for index, raw_path in enumerate(paths, 1):
            alias = f"{prefix}-{index}"
            try:
                path = Path(raw_path)
                remaining = _PULSE_MAX_TOTAL_BYTES - total_bytes
                if remaining <= 0:
                    raise _PulseInputError
                data = _read_pulse_report(
                    path, min(_PULSE_MAX_REPORT_BYTES, remaining))
                total_bytes += len(data)
                destination.append(_parse_pulse_report(data))
            except (OSError, _PulseInputError, OverflowError, ValueError):
                print(f"gauge: pulse incomplete: {alias} is unreadable or invalid",
                      file=sys.stderr)
                return 2

    inventories = []
    for raw_path, alias in (
            (args.tier_inventory, "tier-inventory"),
            (args.before_tier_inventory, "before-tier-inventory")):
        inventory = None
        if raw_path is not None:
            try:
                path = Path(raw_path)
                remaining = _PULSE_MAX_TOTAL_BYTES - total_bytes
                if remaining <= 0:
                    raise _PulseInputError
                data = _read_pulse_report(
                    path, min(_PULSE_MAX_INVENTORY_BYTES, remaining))
                total_bytes += len(data)
                inventory = _parse_tier_inventory(data)
            except (OSError, _PulseInputError, OverflowError, ValueError):
                print(f"gauge: pulse incomplete: {alias} is unreadable or invalid",
                      file=sys.stderr)
                return 2
        inventories.append(inventory)
    after_inventory, before_inventory = inventories

    outcomes = collections.Counter()
    for report in parsed:
        outcomes.update(report["outcomes"])
    try:
        phase_total = math.fsum(report["phase_seconds"] for report in parsed)
        session_total = math.fsum(report["session_seconds"] for report in parsed)
    except OverflowError:
        print("gauge: pulse incomplete: numeric summary is out of range", file=sys.stderr)
        return 2
    if not math.isfinite(phase_total) or not math.isfinite(session_total):
        print("gauge: pulse incomplete: numeric summary is out of range", file=sys.stderr)
        return 2

    labels = {
        "commit": args.commit_label,
        "python": args.python_label,
        "selection": args.selection_label,
        "seed": args.seed_label,
    }
    before_labels = {
        "commit": args.before_commit_label,
        "python": args.before_python_label,
        "selection": args.before_selection_label,
        "seed": args.before_seed_label,
    }
    if any(value is not None and not _PULSE_LABEL.fullmatch(value)
           for value in (*labels.values(), *before_labels.values())):
        print("gauge: pulse incomplete: report labels must be short safe identifiers",
              file=sys.stderr)
        return 2
    report_summaries = [
        {
            "alias": f"report-{index}",
            "case_records": report["cases"],
            "outcomes": {name: report["outcomes"][name]
                         for name in ("passed", "failures", "errors", "skipped")},
            "testcase_phase_seconds": report["phase_seconds"],
            "testsuite_session_seconds": report["session_seconds"],
        }
        for index, report in enumerate(parsed, 1)
    ]
    usage = {name: "UNKNOWN" for name in ("claude", "codex", "antigravity")}
    pulse = {
        "schema": "cairn-pulse/1",
        "reports": report_summaries,
        "case_records": sum(report["cases"] for report in parsed),
        "outcomes": {name: outcomes[name]
                     for name in ("passed", "failures", "errors", "skipped")},
        "testcase_phase_seconds": phase_total,
        "testsuite_session_seconds": session_total,
        "tier_inventory": after_inventory,
        "coverage": {
            "complete": bool(parsed),
            "report_count": len(parsed),
            "report_aliases": [f"report-{index}" for index in range(1, len(parsed) + 1)],
            "case_records_are_unique_tests": False,
            "possible_duplicate_case_records": len(parsed) > 1,
            "phase_time_known_cases": sum(report["phase_known"] for report in parsed),
            "phase_time_unknown_cases": sum(report["phase_unknown"] for report in parsed),
            "session_time_known_reports": sum(report["session_known"] for report in parsed),
            "session_time_unknown_reports": sum(report["session_unknown"] for report in parsed),
            "labels_present": labels,
            "comparability": ("unknown" if not parsed or not all(labels.values())
                              else "not_assessed"),
            "usage": usage,
            "private_collection_join": "not_performed",
        },
    }
    try:
        pulse.update(_comparison_observations(
            before_parsed, parsed, before_inventory, after_inventory,
            before_labels, labels,
        ))
    except OverflowError:
        print("gauge: pulse incomplete: baseline numeric summary is out of range",
              file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(pulse, sort_keys=True, allow_nan=False))
    else:
        print("gauge: public JUnit pulse (cairn-pulse/1)")
        print(f"gauge: reports={pulse['coverage']['report_count']} "
              f"case-records={pulse['case_records']} "
              f"possible-duplicates={str(pulse['coverage']['possible_duplicate_case_records']).lower()}")
        print("gauge: outcomes " + " | ".join(
            f"{name}={pulse['outcomes'][name]}" for name in pulse["outcomes"]))
        print(f"gauge: testcase phase seconds={phase_total:.6f} "
              f"(known cases={pulse['coverage']['phase_time_known_cases']}, "
              f"unknown={pulse['coverage']['phase_time_unknown_cases']})")
        print(f"gauge: testsuite session seconds={session_total:.6f} "
              f"(known reports={pulse['coverage']['session_time_known_reports']}, "
              f"unknown={pulse['coverage']['session_time_unknown_reports']})")
        for report in report_summaries:
            print(f"gauge: {report['alias']} case-records={report['case_records']} "
                  + " ".join(f"{name}={report['outcomes'][name]}"
                             for name in report["outcomes"]))
        print("gauge: comparability=" + pulse["coverage"]["comparability"]
              + "; run equivalence not assessed")
        baseline = pulse["baseline"]
        if baseline["observations"] is None:
            print("gauge: baseline reports=unknown")
        else:
            observed = baseline["observations"]
            print(f"gauge: baseline reports={observed['report_count']} "
                  f"case-records={observed['case_records']} "
                  f"testcase-phase-seconds={observed['testcase_phase_seconds']:.6f} "
                  f"testsuite-session-seconds={observed['testsuite_session_seconds']:.6f}")
        if baseline["tier_inventory"] is None:
            print("gauge: baseline tier inventory=unknown")
        else:
            before_total = baseline["tier_inventory"]["total"]
            print(f"gauge: baseline tier inventory files={before_total['files']} "
                  f"lines={before_total['lines']}")
        comparison = pulse["comparison"]
        print("gauge: suite growth files="
              + (str(comparison["tier_inventory"]["files_delta"])
                 if comparison["tier_inventory"]["files_delta"] is not None
                 else "unknown")
              + " lines="
              + (str(comparison["tier_inventory"]["lines_delta"])
                 if comparison["tier_inventory"]["lines_delta"] is not None
                 else "unknown"))
        print("gauge: case-record delta="
              + (str(comparison["case_record_delta"])
                 if comparison["case_record_delta"] is not None else "unknown")
              + " (not unique tests or collected nodes)")
        print("gauge: testcase phase delta="
              + (f"{comparison['testcase_phase_seconds_delta']:.6f}"
                 if comparison["testcase_phase_seconds_delta"] is not None
                 else "unknown")
              + "; testsuite session delta="
              + (f"{comparison['testsuite_session_seconds_delta']:.6f}"
                 if comparison["testsuite_session_seconds_delta"] is not None
                 else "unknown"))
        for tier in comparison["tier_inventory"]["shared_tiers"]:
            print(f"gauge: tier {tier['name']} files delta={tier['files_delta']} "
                  f"lines delta={tier['lines_delta']}")
        unequal = comparison["tier_inventory"]["unequal_tiers"]
        if unequal is not None and (unequal["before_only"] or unequal["after_only"]):
            print("gauge: unequal tiers before-only="
                  + ",".join(unequal["before_only"])
                  + " after-only=" + ",".join(unequal["after_only"]))
        print("gauge: usage unknown: Claude, Codex, Antigravity; private collection join not performed")
    return 0


def classify(path: str) -> Optional[str]:
    """The class of *path*, or None when no rule claims it."""
    for prefix, cls in _RULES:
        if path.startswith(prefix):
            return cls
    return None


def _week_of(iso_date: str) -> str:
    d = _dt.date.fromisoformat(iso_date)
    return (d - _dt.timedelta(days=d.weekday())).isoformat()


def _numstat(root: Path, since: str) -> List[Tuple[str, str, int]]:
    """(week, path, lines_added) for every file touched since *since*."""
    out = subprocess.run(
        ["git", "log", f"--since={since}", "--numstat", "--date=short",
         "--pretty=format:C%cd", "--no-merges"],
        cwd=str(root), capture_output=True, text=True, check=False).stdout
    rows: List[Tuple[str, str, int]] = []
    week = ""
    for line in out.splitlines():
        if line.startswith("C"):
            week = _week_of(line[1:].strip())
            continue
        parts = line.split("\t")
        if len(parts) == 3 and parts[0].isdigit() and week:
            rows.append((week, parts[2], int(parts[0])))
    return rows


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gauge", description="Weekly lines added by class; product share.")
    parser.add_argument("--since", default="2026-04-27")
    parser.add_argument("--snapshot", action="store_true",
                        help="Write a dated path-to-class snapshot.")
    parser.add_argument("--root", default=None)
    parser.add_argument("--pulse", action="store_true",
                        help="Report public JUnit observations without Git.")
    parser.add_argument("--junit-report", action="append", default=[], metavar="PATH",
                        help="Add one public JUnit XML report (repeatable).")
    parser.add_argument("--before-junit-report", action="append", default=[], metavar="PATH",
                        help="Add one baseline public JUnit XML report (repeatable).")
    parser.add_argument("--tier-inventory", metavar="PATH",
                        help="Read the after-snapshot aggregate tier inventory JSON.")
    parser.add_argument("--before-tier-inventory", metavar="PATH",
                        help="Read the baseline aggregate tier inventory JSON.")
    parser.add_argument("--json", action="store_true",
                        help="Print the cairn-pulse/1 record.")
    parser.add_argument("--commit-label")
    parser.add_argument("--python-label")
    parser.add_argument("--selection-label")
    parser.add_argument("--seed-label")
    parser.add_argument("--before-commit-label")
    parser.add_argument("--before-python-label")
    parser.add_argument("--before-selection-label")
    parser.add_argument("--before-seed-label")
    args = parser.parse_args(argv)
    if args.pulse:
        return _pulse(args, parser)
    if args.json:
        parser.error("--json requires --pulse")
    if (args.junit_report or args.before_junit_report or args.tier_inventory
            or args.before_tier_inventory
            or any((args.commit_label, args.python_label,
                    args.selection_label, args.seed_label,
                    args.before_commit_label, args.before_python_label,
                    args.before_selection_label, args.before_seed_label))):
        parser.error("JUnit reports and pulse labels require --pulse")
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent

    by_week: Dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    unclassified: collections.Counter = collections.Counter()
    for week, path, added in _numstat(root, args.since):
        cls = classify(path)
        if cls is None:
            unclassified[path.split("/")[0]] += added
            continue
        by_week[week][cls] += added

    print("gauge: week | " + " | ".join(_CLASSES) + " | product share")
    for week in sorted(by_week):
        c = by_week[week]
        total = sum(c[k] for k in _CLASSES)
        share = f"{100 * c['product'] // total}%" if total else "-"
        print(f"gauge: {week} | " + " | ".join(str(c[k]) for k in _CLASSES)
              + f" | {share}")

    if unclassified:
        print("gauge: UNCLASSIFIED (reported, never bucketed):")
        for top, n in unclassified.most_common(10):
            print(f"gauge:   {top}/ -- {n} line(s)")
    else:
        print("gauge: every touched path is classified.")

    if args.snapshot:
        stamp = subprocess.run(["git", "log", "-1", "--date=short",
                                "--pretty=format:%cd"], cwd=str(root),
                               capture_output=True, text=True).stdout.strip()
        dest = root / "dev" / "measurement" / f"gauge-{stamp}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        lines = [f"# Gauge snapshot -- {stamp}", "",
                 "Path-to-class rules in force, first match wins:", ""]
        lines += [f"* `{p}` -> {c}" for p, c in _RULES]
        dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"gauge: wrote {dest.relative_to(root)}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
