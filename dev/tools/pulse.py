#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Shared bounded pulse readers and reducers for Gauge, Audit and Meter."""

from __future__ import annotations

import argparse
import collections
import datetime as _dt
import datetime
from decimal import Decimal
from fractions import Fraction
import json
import math
import os
import re
import stat
import statistics
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_PULSE_MAX_REPORTS = 8
_PULSE_MAX_REPORT_BYTES = 8 * 1024 * 1024
_PULSE_MAX_TOTAL_BYTES = 64 * 1024 * 1024
_PULSE_MAX_INVENTORY_BYTES = 64 * 1024
_PULSE_MAX_METER_ROWS = 100_000
_PULSE_MAX_ARTIFACT_BYTES = 8 * 1024 * 1024
_PULSE_MAX_TIERS = 32
_PULSE_MAX_COUNT = (1 << 63) - 1
_INVENTORY_SCHEMA = "cairn-test-inventory/1"
_INVENTORY_COUNTING_METHOD = "recursive-test-files-utf8-replace-splitlines-v1"
_PULSE_OPEN_FLAGS = (os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                     | getattr(os, "O_NONBLOCK", 0)
                     | getattr(os, "O_BINARY", 0))
_PULSE_LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:+-]{0,127}\Z")
_PULSE_TIER_NAME = re.compile(r"[a-z][a-z0-9_-]{0,31}\Z")
# The form of a meter table's version label; the meter loads this module and shares it.
RATIO_VERSION_FORM = re.compile(r"cairn-api-token-index/[0-9]{4}-[0-9]{2}-[0-9]{2}")
_PULSE_BENIGN_REASONS = frozenset({
    "invalid_record", "unsupported_usage_contract", "unsupported_record",
    "unsupported_or_invalid_session_metadata", "conflicting_session_metadata",
    "conflicting_turn_context", "unsupported_fork_boundary", "snapshot_conflict",
    "legacy_checkpoint_unreconciled", "test_command_classification_unknown",
    "timing_identity_unknown", "project_remote_mismatch", "no_supported_usage",
    "fork_parent_unavailable", "capture_gap", "attribution_unavailable",
    "conflicting_binding", "global_completeness_unknown",
    "models_config_missing",
    "resume_failed_file_replaced", "resume_failed_cursor_past_end",
    "resume_failed_not_line_boundary", "resume_failed_digest_mismatch",
})


def _fraction_text(value):
    if value is None:
        return None
    decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return format(decimal, "f")


class _PulseInputError(ValueError):
    """A public report cannot safely contribute to a pulse."""

    def __init__(self, message="unreadable or invalid"):
        super().__init__(message)
        self.message = message


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
    if not stat.S_ISREG(leaf.st_mode) or leaf.st_nlink != 1:
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
        if (not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1
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
                               st.st_mtime_ns, st.st_nlink)
        if (identity(opened) != identity(after)
                or opened.st_ctime_ns != after.st_ctime_ns
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


def _parse_meter_aggregate(data: bytes) -> dict:
    """Validate one explicitly supplied, already-sanitized project aggregate."""
    if b"\0" in data:
        raise _PulseInputError
    try:
        value = json.loads(data.decode("utf-8-sig"),
                           object_pairs_hook=_unique_json_object,
                           parse_constant=_reject_json_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError,
            ValueError, TypeError) as exc:
        raise _PulseInputError from exc
    schema = value.get("schema") if type(value) is dict else None
    if schema not in {"cairn-meter-project/1", "cairn-meter-project/2", "cairn-meter-project/3"}:
        raise _PulseInputError
    required = {"schema", "project_alias", "ratio_version", "aggregates", "wait", "coverage"}
    if schema == "cairn-meter-project/3":
        required = required | {"by_tier"}
    if type(value) is not dict or set(value) != required:
        raise _PulseInputError
    ratio_version = value["ratio_version"]
    if ratio_version is None:
        if schema != "cairn-meter-project/3":
            raise _PulseInputError
    elif (not isinstance(ratio_version, str)
          or not RATIO_VERSION_FORM.fullmatch(ratio_version)):
        raise _PulseInputError
    if (not isinstance(value["project_alias"], str)
            or not _PULSE_LABEL.fullmatch(value["project_alias"])):
        raise _PulseInputError
    rows = value["aggregates"]
    row_fields = {"week", "day", "artifact", "tool", "model", "model_provenance",
                  "effective_model", "events", "unknown_events", "kinds",
                  "reference_tokens"}
    if schema == "cairn-meter-project/3":
        row_fields = row_fields | {"tier"}
    if type(rows) is not list or len(rows) > _PULSE_MAX_METER_ROWS:
        raise _PulseInputError
    normalized = []
    seen = set()
    kind_names = {"fresh_input", "cache_read", "cache_write", "output"}
    number_form = re.compile(r"(?:0|[1-9][0-9]*)(?:\.[0-9]+)?")
    model_tiers = {}
    for row in rows:
        if type(row) is not dict or set(row) != row_fields:
            raise _PulseInputError
        day, week, artifact = row["day"], row["week"], row["artifact"]
        if day is None:
            if week is not None:
                raise _PulseInputError
        else:
            if not isinstance(day, str):
                raise _PulseInputError
            try:
                parsed_day = _dt.date.fromisoformat(day)
            except ValueError as exc:
                raise _PulseInputError from exc
            if parsed_day.isoformat() != day or week != (
                    f"{parsed_day.isocalendar().year}-W{parsed_day.isocalendar().week:02d}"):
                raise _PulseInputError
        if artifact is not None:
            if (not isinstance(artifact, str) or not artifact or len(artifact) > 4096
                    or artifact.startswith("/") or "\\" in artifact
                    or any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in artifact)
                    or any(part in {"", ".", ".."} for part in artifact.split("/"))):
                raise _PulseInputError
        if row["tool"] not in {"codex", "claude", "antigravity", None}:
            raise _PulseInputError
        for model_field in ("model", "effective_model"):
            model = row[model_field]
            if model is not None and (not isinstance(model, str)
                                      or not _PULSE_LABEL.fullmatch(model)):
                raise _PulseInputError
        if row["model_provenance"] not in {
                "usage_record", "selected_context", "unknown"}:
            raise _PulseInputError
        if schema == "cairn-meter-project/3":
            row_tier = row["tier"]
            if (not isinstance(row_tier, str)
                    or not _PULSE_TIER_NAME.fullmatch(row_tier)
                    or row_tier == "unspecified"):
                raise _PulseInputError
            resolved_model = (row["effective_model"] if row["effective_model"] is not None
                              else (row["model"]
                                    if row["model_provenance"] == "selected_context"
                                    else None))
            if resolved_model is None:
                if row_tier != "unknown":
                    raise _PulseInputError
            else:
                expected_model_tier = model_tiers.setdefault(resolved_model, row_tier)
                if expected_model_tier != row_tier:
                    raise _PulseInputError
        events = _inventory_count(row["events"])
        unknown = _inventory_count(row["unknown_events"])
        if events < 1 or unknown > events:
            raise _PulseInputError
        kinds = row["kinds"]
        if type(kinds) is not dict or set(kinds) != kind_names:
            raise _PulseInputError
        parsed_kinds = {name: (None if kinds[name] is None
                               else _inventory_count(kinds[name]))
                        for name in kind_names}
        references = row["reference_tokens"]
        if type(references) is not dict or set(references) != {*kind_names, "total"}:
            raise _PulseInputError
        for amount in references.values():
            if amount is not None and (not isinstance(amount, str)
                    or not number_form.fullmatch(amount)):
                raise _PulseInputError
        identity = (week, day, artifact, row["tool"], row["model"],
                    row["model_provenance"], row["effective_model"])
        if identity in seen:
            raise _PulseInputError
        seen.add(identity)
        normalized.append({**row, "events": events, "unknown_events": unknown,
                           "kinds": parsed_kinds})
    if schema == "cairn-meter-project/3":
        by_tier = value["by_tier"]
        if type(by_tier) is not list or len(by_tier) > _PULSE_MAX_TIERS + 1:
            raise _PulseInputError
        tier_groups = {}
        for row in normalized:
            tier_groups.setdefault(row["tier"], []).append(row)
        seen_tiers = []
        seen_tier_set = set()
        tier_fields = {"tier", "events", "unknown_events", "kinds", "reference_tokens"}
        normalized_by_tier = []
        for entry in by_tier:
            if type(entry) is not dict or set(entry) != tier_fields:
                raise _PulseInputError
            tier = entry["tier"]
            if (not isinstance(tier, str)
                    or not _PULSE_TIER_NAME.fullmatch(tier)
                    or tier == "unspecified"
                    or tier in seen_tier_set):
                raise _PulseInputError
            seen_tiers.append(tier)
            seen_tier_set.add(tier)
            group = tier_groups.get(tier)
            if not group:
                raise _PulseInputError
            events = _inventory_count(entry["events"])
            unknown = _inventory_count(entry["unknown_events"])
            if (events < 1 or unknown > events
                    or events != sum(r["events"] for r in group)
                    or unknown != sum(r["unknown_events"] for r in group)):
                raise _PulseInputError
            ekinds = entry["kinds"]
            if type(ekinds) is not dict or set(ekinds) != kind_names:
                raise _PulseInputError
            parsed_ekinds = {name: (None if ekinds[name] is None
                                    else _inventory_count(ekinds[name]))
                             for name in kind_names}
            for name in kind_names:
                exp_kind = (None if any(r["kinds"][name] is None for r in group)
                            else sum(r["kinds"][name] for r in group))
                if parsed_ekinds[name] != exp_kind:
                    raise _PulseInputError
            erefs = entry["reference_tokens"]
            if type(erefs) is not dict or set(erefs) != {*kind_names, "total"}:
                raise _PulseInputError
            for name in (*kind_names, "total"):
                amount = erefs[name]
                if amount is not None and (not isinstance(amount, str)
                        or not number_form.fullmatch(amount)):
                    raise _PulseInputError
                vals = [r["reference_tokens"][name] for r in group]
                exp_ref = (None if any(v is None for v in vals)
                           else _fraction_text(sum(
                               (Fraction(Decimal(v)) for v in vals), Fraction(0))))
                if amount != exp_ref:
                    raise _PulseInputError
            normalized_by_tier.append({
                "tier": tier, "events": events, "unknown_events": unknown,
                "kinds": parsed_ekinds, "reference_tokens": erefs,
            })
        if "unknown" in seen_tier_set and seen_tiers[-1] != "unknown":
            raise _PulseInputError
        if seen_tier_set != set(tier_groups):
            raise _PulseInputError
        value = {**value, "by_tier": normalized_by_tier}
    wait = value["wait"]
    if value["schema"] == "cairn-meter-project/1":
        if (type(wait) is not dict or set(wait) != {"seconds", "coverage"}
                or wait["seconds"] is not None or wait["coverage"] != "unknown"):
            raise _PulseInputError
    else:
        if (type(wait) is not dict
                or set(wait) != {"coverage", "observed", "by_day", "by_artifact"}
                or wait["coverage"] != "unknown"
                or type(wait["by_day"]) is not list
                or type(wait["by_artifact"]) is not list):
            raise _PulseInputError

        def triple(item, fields):
            if type(item) is not dict or set(item) != fields:
                raise _PulseInputError
            executions = _inventory_count(item["executions"])
            execution_ms = _inventory_count(item["execution_ms"])
            wall_ms = _inventory_count(item["wall_wait_ms"])
            if execution_ms < wall_ms or (executions == 0 and execution_ms == 0):
                raise _PulseInputError
            return executions, execution_ms, wall_ms

        observed_fields = {"executions", "execution_ms", "wall_wait_ms"}
        observed = wait["observed"]
        if observed is not None:
            observed_values = triple(observed, observed_fields)
            if observed_values[0] == 0:
                raise _PulseInputError
        day_totals = {}
        day_seen = set()
        previous_day = None
        for item in wait["by_day"]:
            if type(item) is not dict or set(item) != {"day", *observed_fields}:
                raise _PulseInputError
            day = item["day"]
            if not isinstance(day, str):
                raise _PulseInputError
            try:
                parsed_day = _dt.date.fromisoformat(day)
            except ValueError as exc:
                raise _PulseInputError from exc
            if parsed_day.isoformat() != day or day in day_seen or (
                    previous_day is not None and day <= previous_day):
                raise _PulseInputError
            day_seen.add(day)
            previous_day = day
            values = triple({name: item[name] for name in observed_fields}, observed_fields)
            day_totals[day] = values
        artifact_seen = set()
        previous_artifact = None
        artifact_totals = {}
        for item in wait["by_artifact"]:
            if type(item) is not dict or set(item) != {"day", "artifact", *observed_fields}:
                raise _PulseInputError
            day, artifact = item["day"], item["artifact"]
            if day not in day_seen or not isinstance(artifact, str):
                raise _PulseInputError
            if (not artifact or len(artifact) > 4096 or artifact.startswith("/")
                    or "\\" in artifact
                    or any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in artifact)
                    or any(part in {"", ".", ".."} for part in artifact.split("/"))):
                raise _PulseInputError
            identity = (day, artifact)
            if identity in artifact_seen or (previous_artifact is not None
                    and identity <= previous_artifact):
                raise _PulseInputError
            artifact_seen.add(identity)
            previous_artifact = identity
            artifact_totals[identity] = triple(
                {name: item[name] for name in observed_fields}, observed_fields)
        if observed is None:
            if day_seen or artifact_seen:
                raise _PulseInputError
        else:
            summed = tuple(sum(values[index] for values in day_totals.values())
                           for index in range(3))
            if summed != observed_values:
                raise _PulseInputError
            for (day, _artifact), values in artifact_totals.items():
                if any(values[index] > day_totals[day][index] for index in range(3)):
                    raise _PulseInputError
    coverage = value["coverage"]
    if (type(coverage) is not dict or set(coverage) != {"global", "reasons"}
            or coverage["global"] != "unknown"
            or type(coverage["reasons"]) is not list
            or coverage["reasons"] != sorted(set(coverage["reasons"]))
            or any(not isinstance(item, str) or not _PULSE_LABEL.fullmatch(item)
                   for item in coverage["reasons"])):
        raise _PulseInputError
    reasons = value["coverage"]["reasons"]
    incomplete_reasons = sorted(reason for reason in reasons
                                if reason not in _PULSE_BENIGN_REASONS)
    return {**value, "aggregates": normalized,
            "incomplete_reasons": incomplete_reasons}


def _unknown_artifact_metrics() -> dict:
    return {
        "source": "not_supplied", "window": None,
        "coverage": {"cohort_selection": "unknown", "completeness": "unknown"},
        "project_alias": None, "commit_label": None,
        "parents": None, "orphans": None, "orphan_labels": None,
        "summary": {name: None for name in (
            "artifact_count", "orphan_count", "median_combined_words",
            "max_combined_words", "median_review_passes", "max_review_passes")},
        "model_records": {"source": "declared_record_mix_not_metered_call_mix",
                          "by_tier": None},
        "always_loaded": None, "deliberation": None,
    }


def _parse_artifact_snapshot(data: bytes) -> tuple[dict, dict]:
    try:
        snapshot = _pulse_validate_bundle(data)
        metrics = _pulse_artifact_metrics(
            snapshot["files"], snapshot["always_loaded"], snapshot["deliberation"],
            snapshot["model_tiers"], project_alias=snapshot["project_alias"],
            week=snapshot["week"], commit_label=snapshot["commit_label"])
    except (KeyError, ValueError, TypeError, OverflowError, RecursionError) as exc:
        raise _PulseInputError from exc
    return snapshot, metrics


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


def _format_observed_time(seconds: float, known: int, unknown: int,
                         unit: str) -> str:
    if known == 0:
        value = "unknown"
    elif unknown:
        value = f"partial {seconds:.6f}"
    else:
        value = f"{seconds:.6f}"
    return f"{value} (known {unit}={known}, unknown={unknown})"


def register_arguments(parser: argparse.ArgumentParser, *, include_switch=False,
                       include_json=True):
    if include_switch:
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
    parser.add_argument("--meter-aggregate", metavar="PATH",
                        help="Read one explicit sanitized project meter aggregate JSON.")
    parser.add_argument("--artifact-input", metavar="PATH",
                        help="Read one explicit public artifact snapshot from audit_report.")
    if include_json:
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
    return parser


def read_pulse_report(path: Path, limit: int) -> bytes:
    return _read_pulse_report(path, limit)


def validate_artifact_bundle(data: bytes) -> dict:
    return _pulse_validate_bundle(data)


def artifact_metrics(files: List[dict], always_loaded: List[str],
                     deliberation: List[str], model_tiers: Dict[str, str],
                     *, project_alias: str, week: str,
                     commit_label: Optional[str]) -> dict:
    return _pulse_artifact_metrics(
        files, always_loaded, deliberation, model_tiers,
        project_alias=project_alias, week=week, commit_label=commit_label)


def _read_inputs_error(message):
    raise _PulseInputError(message) from None


def read_inputs(options, meter_aggregate_bytes=None):
    """Read and validate only explicit, bounded public inputs."""
    if options.meter_aggregate is not None and meter_aggregate_bytes is not None:
        _read_inputs_error("meter aggregate path and bytes cannot both be used")
    if meter_aggregate_bytes is not None and not isinstance(meter_aggregate_bytes, bytes):
        _read_inputs_error("meter aggregate is unreadable or invalid")
    all_report_paths = options.junit_report + options.before_junit_report
    if len(all_report_paths) > _PULSE_MAX_REPORTS:
        _read_inputs_error("at most 8 reports are accepted")

    total_bytes = 0
    parsed, before_parsed = [], []
    for paths, destination, prefix in (
            (options.junit_report, parsed, "report"),
            (options.before_junit_report, before_parsed, "before-report")):
        for index, raw_path in enumerate(paths, 1):
            alias = f"{prefix}-{index}"
            try:
                remaining = _PULSE_MAX_TOTAL_BYTES - total_bytes
                if remaining <= 0:
                    raise _PulseInputError
                data = _read_pulse_report(
                    Path(raw_path), min(_PULSE_MAX_REPORT_BYTES, remaining))
                total_bytes += len(data)
                destination.append(_parse_pulse_report(data))
            except (OSError, _PulseInputError, OverflowError, ValueError):
                _read_inputs_error(f"{alias} is unreadable or invalid")

    inventories = []
    for raw_path, alias in (
            (options.tier_inventory, "tier-inventory"),
            (options.before_tier_inventory, "before-tier-inventory")):
        inventory = None
        if raw_path is not None:
            try:
                remaining = _PULSE_MAX_TOTAL_BYTES - total_bytes
                if remaining <= 0:
                    raise _PulseInputError
                data = _read_pulse_report(
                    Path(raw_path), min(_PULSE_MAX_INVENTORY_BYTES, remaining))
                total_bytes += len(data)
                inventory = _parse_tier_inventory(data)
            except (OSError, _PulseInputError, OverflowError, ValueError):
                _read_inputs_error(f"{alias} is unreadable or invalid")
        inventories.append(inventory)
    after_inventory, before_inventory = inventories

    meter_usage = None
    if meter_aggregate_bytes is not None:
        remaining = _PULSE_MAX_TOTAL_BYTES - total_bytes
        if len(meter_aggregate_bytes) > remaining:
            _read_inputs_error("meter aggregate is unreadable or invalid")
        try:
            meter_usage = _parse_meter_aggregate(meter_aggregate_bytes)
        except (OverflowError, ValueError, TypeError):
            _read_inputs_error("meter aggregate is unreadable or invalid")
        total_bytes += len(meter_aggregate_bytes)
    elif options.meter_aggregate is not None:
        try:
            remaining = _PULSE_MAX_TOTAL_BYTES - total_bytes
            if remaining <= 0:
                raise _PulseInputError
            data = _read_pulse_report(
                Path(options.meter_aggregate), min(_PULSE_MAX_TOTAL_BYTES, remaining))
            total_bytes += len(data)
            meter_usage = _parse_meter_aggregate(data)
        except (OSError, _PulseInputError, OverflowError, ValueError):
            _read_inputs_error("meter aggregate is unreadable or invalid")

    artifact_metrics = _unknown_artifact_metrics()
    if options.artifact_input is not None:
        try:
            remaining = _PULSE_MAX_TOTAL_BYTES - total_bytes
            if remaining <= 0:
                raise _PulseInputError
            data = _read_pulse_report(
                Path(options.artifact_input), min(_PULSE_MAX_ARTIFACT_BYTES, remaining))
            total_bytes += len(data)
            snapshot = _pulse_validate_bundle(data)
            artifact_metrics = _pulse_artifact_metrics(
                snapshot["files"], snapshot["always_loaded"], snapshot["deliberation"],
                snapshot["model_tiers"], project_alias=snapshot["project_alias"],
                week=snapshot["week"], commit_label=snapshot["commit_label"])
            if (meter_usage is not None
                    and artifact_metrics["project_alias"] != meter_usage["project_alias"]):
                raise _PulseInputError
        except (OSError, _PulseInputError, OverflowError, ValueError):
            _read_inputs_error(
                "artifact input is unreadable, invalid, or mismatched")

    return {"reports": parsed, "before_reports": before_parsed,
            "tier_inventory": after_inventory,
            "before_tier_inventory": before_inventory,
            "project_usage": meter_usage, "artifacts": artifact_metrics}


def build_pulse(options, inputs):
    """Build the public cairn-pulse/1 record from validated inputs."""
    parsed = inputs["reports"]
    before_parsed = inputs["before_reports"]
    after_inventory = inputs["tier_inventory"]
    before_inventory = inputs["before_tier_inventory"]
    meter_usage = inputs["project_usage"]
    artifact_metrics = inputs["artifacts"]
    outcomes = collections.Counter()
    for report in parsed:
        outcomes.update(report["outcomes"])
    try:
        phase_total = math.fsum(report["phase_seconds"] for report in parsed)
        session_total = math.fsum(report["session_seconds"] for report in parsed)
    except OverflowError:
        _read_inputs_error("numeric summary is out of range")
    if not math.isfinite(phase_total) or not math.isfinite(session_total):
        _read_inputs_error("numeric summary is out of range")

    labels = {"commit": options.commit_label, "python": options.python_label,
              "selection": options.selection_label, "seed": options.seed_label}
    before_labels = {
        "commit": options.before_commit_label,
        "python": options.before_python_label,
        "selection": options.before_selection_label,
        "seed": options.before_seed_label,
    }
    if any(value is not None and not _PULSE_LABEL.fullmatch(value)
           for value in (*labels.values(), *before_labels.values())):
        _read_inputs_error("report labels must be short safe identifiers")
    report_summaries = [
        {"alias": f"report-{index}", "case_records": report["cases"],
         "outcomes": {name: report["outcomes"][name]
                      for name in ("passed", "failures", "errors", "skipped")},
         "testcase_phase_seconds": report["phase_seconds"],
         "testsuite_session_seconds": report["session_seconds"]}
        for index, report in enumerate(parsed, 1)]
    usage = {name: "UNKNOWN" for name in ("claude", "codex", "antigravity")}
    if meter_usage is not None:
        for name in usage:
            if any(row["tool"] == name for row in meter_usage["aggregates"]):
                usage[name] = "PARTIAL"
    pulse = {
        "schema": "cairn-pulse/1", "reports": report_summaries,
        "case_records": sum(report["cases"] for report in parsed),
        "outcomes": {name: outcomes[name]
                     for name in ("passed", "failures", "errors", "skipped")},
        "testcase_phase_seconds": phase_total,
        "testsuite_session_seconds": session_total,
        "tier_inventory": after_inventory, "project_usage": meter_usage,
        "artifacts": artifact_metrics,
        "coverage": {
            "complete": bool(parsed), "report_count": len(parsed),
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
            "private_collection_join": (
                "explicit_project_aggregate" if meter_usage is not None
                else "not_performed"),
        },
    }
    try:
        pulse.update(_comparison_observations(
            before_parsed, parsed, before_inventory, after_inventory,
            before_labels, labels))
    except OverflowError:
        _read_inputs_error("baseline numeric summary is out of range")
    return pulse


def render_text(pulse):
    """Render the existing human-readable pulse from a validated record."""
    lines = ["gauge: public JUnit pulse (cairn-pulse/1)"]
    lines.append(f"gauge: reports={pulse['coverage']['report_count']} "
                 f"case-records={pulse['case_records']} "
                 f"possible-duplicates={str(pulse['coverage']['possible_duplicate_case_records']).lower()}")
    lines.append("gauge: outcomes " + " | ".join(
        f"{name}={pulse['outcomes'][name]}" for name in pulse["outcomes"]))
    lines.append(f"gauge: testcase phase seconds={pulse['testcase_phase_seconds']:.6f} "
                 f"(known cases={pulse['coverage']['phase_time_known_cases']}, "
                 f"unknown={pulse['coverage']['phase_time_unknown_cases']})")
    lines.append(f"gauge: testsuite session seconds={pulse['testsuite_session_seconds']:.6f} "
                 f"(known reports={pulse['coverage']['session_time_known_reports']}, "
                 f"unknown={pulse['coverage']['session_time_unknown_reports']})")
    for report in pulse["reports"]:
        lines.append(f"gauge: {report['alias']} case-records={report['case_records']} "
                     + " ".join(f"{name}={report['outcomes'][name]}"
                                for name in report["outcomes"]))
    meter_usage = pulse["project_usage"]
    if meter_usage is not None:
        if meter_usage["incomplete_reasons"]:
            labels = ", ".join(meter_usage["incomplete_reasons"])
            lines.append("gauge: supplied project usage alias="
                         + meter_usage["project_alias"]
                         + f" aggregates={len(meter_usage['aggregates'])}; "
                         + f"INCOMPLETE ({labels}); coverage=unknown")
        else:
            lines.append("gauge: supplied project usage alias="
                         + meter_usage["project_alias"]
                         + f" aggregates={len(meter_usage['aggregates'])}; coverage=unknown")
        for row in meter_usage["aggregates"]:
            kind_values = " ".join(
                f"{name}={row['kinds'][name] if row['kinds'][name] is not None else 'unknown'}"
                for name in ("fresh_input", "cache_read", "cache_write", "output"))
            model_part = f"model={row['model'] or 'unknown'} "
            if "tier" in row:
                model_part += f"tier={row['tier']} "
            lines.append("gauge: usage "
                         + f"week={row['week'] or 'unknown'} "
                         + f"day={row['day'] or 'unknown'} "
                         + f"artifact={row['artifact'] or 'project'} "
                         + f"tool={row['tool'] or 'unknown'} "
                         + model_part
                         + f"events={row['events']} unknown-events={row['unknown_events']} "
                         + kind_values
                         + " weighted="
                         + (str(row['reference_tokens']['total'])
                            if row['reference_tokens']['total'] is not None
                            else 'unknown'))
        for entry in meter_usage.get("by_tier", ()):
            kind_values = " ".join(
                f"{name}={entry['kinds'][name] if entry['kinds'][name] is not None else 'unknown'}"
                for name in ("fresh_input", "cache_read", "cache_write", "output"))
            lines.append("gauge: usage by tier "
                         + f"tier={entry['tier']} "
                         + f"events={entry['events']} unknown-events={entry['unknown_events']} "
                         + kind_values
                         + " weighted="
                         + (str(entry['reference_tokens']['total'])
                            if entry['reference_tokens']['total'] is not None
                            else 'unknown'))
        wait = meter_usage["wait"]
        if "observed" not in wait or wait["observed"] is None:
            lines.append("gauge: test waits observed=unknown; coverage=unknown")
        else:
            observed = wait["observed"]
            lines.append("gauge: test waits "
                         + f"executions={observed['executions']} "
                         + f"execution-ms={observed['execution_ms']} "
                         + f"wall-wait-ms={observed['wall_wait_ms']}; coverage=unknown")
            for row in wait["by_day"]:
                lines.append("gauge: test waits by day "
                             + f"day={row['day']} executions={row['executions']} "
                             + f"execution-ms={row['execution_ms']} "
                             + f"wall-wait-ms={row['wall_wait_ms']}; coverage=unknown")
            for row in wait["by_artifact"]:
                lines.append("gauge: test waits by artifact "
                             + f"day={row['day']} artifact={row['artifact']} "
                             + f"executions={row['executions']} "
                             + f"execution-ms={row['execution_ms']} "
                             + f"wall-wait-ms={row['wall_wait_ms']}; coverage=unknown")
    artifact_metrics = pulse["artifacts"]
    if artifact_metrics["source"] == "explicit_public_snapshot":
        summary = artifact_metrics["summary"]
        tiers = artifact_metrics["model_records"]["by_tier"]
        lines.append(f"gauge: artifact snapshot source=explicit_public_snapshot "
                     f"week={artifact_metrics['window']['week']} "
                     f"project={artifact_metrics['project_alias']} "
                     f"cohort-selection=unverified coverage=unknown")
        lines.append(f"gauge: artifacts={summary['artifact_count']} "
                     f"orphans={summary['orphan_count']} "
                     f"combined-words median={summary['median_combined_words']} "
                     f"max={summary['max_combined_words']} review-passes "
                     f"median={summary['median_review_passes']} "
                     f"max={summary['max_review_passes']}")
        lines.append("gauge: declared model records " + " ".join(
            f"{tier}={tiers[tier]}" for tier in ("high", "medium", "low", "unspecified"))
            + "; not metered call mix")
        for name in ("always_loaded", "deliberation"):
            row = artifact_metrics[name]
            lines.append(f"gauge: {name} explicit files={row['files']} "
                         f"chars={row['chars']} estimated-tokens={row['estimated_tokens']} "
                         f"({row['estimator']}); completeness=unknown")
        if artifact_metrics["orphan_labels"]:
            lines.append("gauge: orphan review labels: "
                         + ", ".join(artifact_metrics["orphan_labels"]))
    else:
        lines.append("gauge: artifact metrics unknown: no explicit public snapshot supplied")
    lines.append("gauge: comparability=" + pulse["coverage"]["comparability"]
                 + "; run equivalence not assessed")
    baseline = pulse["baseline"]
    if baseline["observations"] is None:
        lines.append("gauge: baseline reports=unknown")
    else:
        observed = baseline["observations"]
        lines.append(f"gauge: baseline reports={observed['report_count']} "
                     f"case-records={observed['case_records']} "
                     "testcase-phase-seconds="
                     + _format_observed_time(
                         observed["testcase_phase_seconds"],
                         observed["phase_time_known_cases"],
                         observed["phase_time_unknown_cases"], "cases")
                     + "; testsuite-session-seconds="
                     + _format_observed_time(
                         observed["testsuite_session_seconds"],
                         observed["session_time_known_reports"],
                         observed["session_time_unknown_reports"], "reports"))
    if baseline["tier_inventory"] is None:
        lines.append("gauge: baseline tier inventory=unknown")
    else:
        before_total = baseline["tier_inventory"]["total"]
        lines.append(f"gauge: baseline tier inventory files={before_total['files']} "
                     f"lines={before_total['lines']}")
    comparison = pulse["comparison"]
    lines.append("gauge: suite growth files="
                 + (str(comparison["tier_inventory"]["files_delta"])
                    if comparison["tier_inventory"]["files_delta"] is not None else "unknown")
                 + " lines="
                 + (str(comparison["tier_inventory"]["lines_delta"])
                    if comparison["tier_inventory"]["lines_delta"] is not None else "unknown"))
    lines.append("gauge: case-record delta="
                 + (str(comparison["case_record_delta"])
                    if comparison["case_record_delta"] is not None else "unknown")
                 + " (not unique tests or collected nodes)")
    lines.append("gauge: testcase phase delta="
                 + (f"{comparison['testcase_phase_seconds_delta']:.6f}"
                    if comparison["testcase_phase_seconds_delta"] is not None else "unknown")
                 + "; testsuite session delta="
                 + (f"{comparison['testsuite_session_seconds_delta']:.6f}"
                    if comparison['testsuite_session_seconds_delta'] is not None else "unknown"))
    for tier in comparison["tier_inventory"]["shared_tiers"]:
        lines.append(f"gauge: tier {tier['name']} files delta={tier['files_delta']} "
                     f"lines delta={tier['lines_delta']}")
    unequal = comparison["tier_inventory"]["unequal_tiers"]
    if unequal is not None and (unequal["before_only"] or unequal["after_only"]):
        lines.append("gauge: unequal tiers before-only="
                     + ",".join(unequal["before_only"])
                     + " after-only=" + ",".join(unequal["after_only"]))
    lines.append("gauge: usage " + ", ".join(
        f"{name.title()}={pulse['coverage']['usage'][name].lower()}"
        for name in ("claude", "codex", "antigravity"))
        + "; private collection join="
        + ("explicit project aggregate" if meter_usage is not None
           else "not performed"))
    return "\n".join(lines) + "\n"


def run_pulse(args: argparse.Namespace, parser: argparse.ArgumentParser,
             meter_aggregate_bytes=None) -> int:
    if getattr(args, "snapshot", False):
        parser.error("--pulse cannot be combined with --snapshot")
    if getattr(args, "root", None) is not None:
        parser.error("--root is not available with --pulse")
    try:
        inputs = read_inputs(args, meter_aggregate_bytes=meter_aggregate_bytes)
        pulse = build_pulse(args, inputs)
    except _PulseInputError as exc:
        print(f"gauge: pulse incomplete: {exc.message}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(pulse, sort_keys=True, allow_nan=False))
    else:
        sys.stdout.write(render_text(pulse))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pulse", description="Build a bounded public Cairn pulse.")
    register_arguments(parser)
    args = parser.parse_args(argv)
    return run_pulse(args, parser)


_PULSE_SCHEMA = "cairn-pulse-artifacts/1"
_PULSE_MAX_BYTES = 8 * 1024 * 1024
_PULSE_MAX_FILE_BYTES = 1024 * 1024
_PULSE_MAX_FILES = 512
_PULSE_MAX_MODELS = 128
_PULSE_LABEL_RE = _PULSE_LABEL
_REVIEW_SUFFIXES = (".code-review.md", ".security-review.md",
                    ".plan-review.md", ".review.md", ".second-look.md")
_PARENT_RE = re.compile(
    r"^\*\*(?:Parent plan|Parent proposal|Parent artifact|Reviewed artifact)\*\*\s*:\s*(?P<v>.+)$",
    re.M | re.I,
)
_PULSE_REVIEW_TYPES = (
    "security code review", "targeted code review return", "security review",
    "plan review", "code review", "review",
)
_PULSE_OTHER_TYPES = ("response", "decision", "implementation", "strategy")
_PULSE_REVIEW_FILE = re.compile(r"^\d{4}-\d{2}-\d{2}-code-review-", re.I)
_PULSE_MODEL_FIELD_RE = re.compile(r"^\*\*Model\*\*\s*:\s*(.*?)\s*$", re.I | re.M)
_PULSE_AUTHOR_FIELD_RE = re.compile(r"^\*\*Author\*\*\s*:\s*(.*?)\s*$", re.I | re.M)


def _pulse_safe_label(value: object) -> bool:
    if (not isinstance(value, str) or not value or len(value) > 2048
            or value.startswith("/") or "\\" in value or ":" in value
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        return False
    return all(part not in {"", ".", ".."} for part in value.split("/"))


def _pulse_sidefile(label: str) -> bool:
    name = label.rsplit("/", 1)[-1].lower()
    return (name.endswith(_REVIEW_SUFFIXES)
            or bool(_PULSE_REVIEW_FILE.match(name)))


def _pulse_sidefile_parent(label: str, text: str, labels: List[str]) -> Optional[str]:
    """Resolve only supplied labels; Markdown links are never opened or followed."""
    if not _pulse_sidefile(label):
        return None
    explicit = _PARENT_RE.findall(text)
    if explicit:
        raw_values = {value.strip().strip("`<>") for value in explicit}
        if len(raw_values) != 1:
            return None
        raw = raw_values.pop()
        if not _pulse_safe_label(raw):
            return None
        candidates = {raw}
        if not raw.endswith(".md"):
            candidates.add(raw + ".md")
        parent_dir = label.rsplit("/", 1)[0] if "/" in label else ""
        candidates.update(
            f"{parent_dir}/{item}" if parent_dir else item
            for item in tuple(candidates))
        matches = [item for item in labels if item in candidates]
        if len(matches) == 1:
            return matches[0]
        if "/" not in raw:
            basename = raw if raw.endswith(".md") else raw + ".md"
            matches = [item for item in labels if item.rsplit("/", 1)[-1] == basename]
            return matches[0] if len(matches) == 1 else None
        return None
    name = label.rsplit("/", 1)[-1]
    if _PULSE_REVIEW_FILE.match(name):
        return None
    suffix = next((item for item in _REVIEW_SUFFIXES
                   if name.lower().endswith(item)), None)
    if suffix is None:
        return None
    expected = name[:-len(suffix)] + ".md"
    matches = [item for item in labels if item.rsplit("/", 1)[-1] == expected]
    return matches[0] if len(matches) == 1 else None


def _pulse_heading(title: str):
    lowered = title.strip().casefold()
    for kind in _PULSE_REVIEW_TYPES:
        if (lowered == kind or lowered.startswith(kind + " --")
                or lowered.startswith(kind + " —") or lowered.startswith(kind + " –")):
            return "review"
    for kind in _PULSE_OTHER_TYPES:
        if (lowered == kind or lowered.startswith(kind + " ")
                or lowered.startswith(kind + " --")
                or lowered.startswith(kind + " —") or lowered.startswith(kind + " –")):
            return "other"
    return None


def _pulse_sections(text: str):
    headings = list(re.finditer(r"(?m)^##[ \t]+([^\r\n]+)\s*$", text))
    candidates = []
    for index, match in enumerate(headings):
        kind = _pulse_heading(match.group(1))
        if kind is None:
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        segment = text[match.start():end]
        authored = ("--" in match.group(1) or "—" in match.group(1)
                    or "–" in match.group(1)
                    or bool(_PULSE_MODEL_FIELD_RE.search(segment))
                    or bool(_PULSE_AUTHOR_FIELD_RE.search(segment)))
        if authored:
            candidates.append({"start": match.start(), "end": end,
                               "kind": kind, "text": segment,
                               "heading": match.group(1)})
    first = candidates[0]["start"] if candidates else len(text)
    opening = text[:first]
    review_text = []
    appendix_text = []
    if candidates:
        by_start = {item["start"]: item for item in candidates}
        later_headings = [item for item in headings if item.start() >= first]
        for index, heading in enumerate(later_headings):
            end = (later_headings[index + 1].start()
                   if index + 1 < len(later_headings) else len(text))
            segment = text[heading.start():end]
            record = by_start.get(heading.start())
            if record is not None and record["kind"] == "review":
                review_text.append(segment)
            else:
                appendix_text.append(segment)
    review_passes = sum(item["kind"] == "review" for item in candidates)
    return opening, "".join(review_text), "".join(appendix_text), candidates, review_passes


def _pulse_counts(text: str) -> dict:
    return {"words": len(text.split()), "bytes": len(text.encode("utf-8"))}


def _pulse_tier(candidate: str, model_tiers: Dict[str, str]) -> str:
    matched = set()
    boundary = r"(?<![A-Za-z0-9_.+-])"
    end = r"(?![A-Za-z0-9_.+-])"
    version = r"(?:\s+v?\d+(?:[._-]\d+)*)?"
    for family, tier in model_tiers.items():
        pattern = re.compile(boundary + re.escape(family) + version + end, re.I)
        if pattern.search(candidate):
            matched.add(family.casefold())
    if len(matched) != 1:
        return "unspecified"
    family = next(iter(matched))
    return next(tier for name, tier in model_tiers.items()
                if name.casefold() == family)


def _pulse_model_observation(text: str, heading: Optional[str], model_tiers: Dict[str, str]) -> str:
    models = _PULSE_MODEL_FIELD_RE.findall(text)
    authors = _PULSE_AUTHOR_FIELD_RE.findall(text)
    if models:
        chosen = models if len({value.casefold() for value in models}) == 1 else []
    elif authors:
        chosen = authors if len({value.casefold() for value in authors}) == 1 else []
    else:
        chosen = [heading] if heading else []
    return _pulse_tier(chosen[0], model_tiers) if len(chosen) == 1 else "unspecified"


def _pulse_artifact_metrics(files: List[dict], always_loaded: List[str],
                            deliberation: List[str], model_tiers: Dict[str, str],
                            *, project_alias: str, week: str,
                            commit_label: Optional[str]) -> dict:
    """Reduce an explicit public Markdown snapshot without filesystem access."""
    by_label = {item["artifact"]: item["text"] for item in files}
    labels = list(by_label)
    cohort = [label for label in labels
              if label not in set(always_loaded) and label not in set(deliberation)]
    sidefiles = [label for label in cohort if _pulse_sidefile(label)]
    parents = [label for label in cohort if label not in sidefiles]
    attached = {label: [] for label in parents}
    orphans = []
    parent_of = {}
    for label in sidefiles:
        parent = _pulse_sidefile_parent(label, by_label[label], labels)
        if parent in attached:
            attached[parent].append(label)
            parent_of[label] = parent
        else:
            orphans.append(label)

    model_counts = {tier: 0 for tier in ("high", "medium", "low", "unspecified")}
    parent_rows = []
    combined_words = []
    combined_passes = []
    for label in sorted(parents):
        text = by_label[label]
        opening, review_text, appendix_text, records, review_passes = _pulse_sections(text)
        opening_counts = _pulse_counts(opening)
        review_counts = _pulse_counts(review_text)
        appendix_counts = _pulse_counts(appendix_text)
        model_counts[_pulse_model_observation(opening, None, model_tiers)] += 1
        for record in records:
            model_counts[_pulse_model_observation(record["text"], record["heading"],
                                                  model_tiers)] += 1
        sidefile_words = sidefile_bytes = sidefile_passes = 0
        for sidefile in sorted(attached[label]):
            side_text = by_label[sidefile]
            sidefile_words += len(side_text.split())
            sidefile_bytes += len(side_text.encode("utf-8"))
            _so, _sr, _sa, side_records, side_passes = _pulse_sections(side_text)
            sidefile_passes += side_passes or 1
            if side_records:
                for record in side_records:
                    model_counts[_pulse_model_observation(
                        record["text"], record["heading"], model_tiers)] += 1
            else:
                model_counts[_pulse_model_observation(side_text, None, model_tiers)] += 1
        total_words = (opening_counts["words"] + review_counts["words"]
                       + appendix_counts["words"] + sidefile_words)
        total_bytes = (opening_counts["bytes"] + review_counts["bytes"]
                       + appendix_counts["bytes"] + sidefile_bytes)
        total_passes = review_passes + sidefile_passes
        combined_words.append(total_words)
        combined_passes.append(total_passes)
        parent_rows.append({
            "artifact": label,
            "opening": opening_counts,
            "reviews": {"words": review_counts["words"] + sidefile_words,
                        "bytes": review_counts["bytes"] + sidefile_bytes},
            "other_appendices": appendix_counts,
            "sidefiles": sorted(attached[label]),
            "combined": {"words": total_words, "bytes": total_bytes},
            "review_passes": total_passes,
            "flags": {
                "over_4000_words": total_words > 4000,
                "over_25_kib": total_bytes > 25 * 1024,
                "over_three_review_passes": total_passes > 3,
            },
        })
    orphan_rows = []
    for label in sorted(orphans):
        text = by_label[label]
        _opening, _review, _appendix, records, passes = _pulse_sections(text)
        passes = passes or 1
        for record in records:
            model_counts[_pulse_model_observation(record["text"], record["heading"],
                                                  model_tiers)] += 1
        if not records:
            model_counts[_pulse_model_observation(text, None, model_tiers)] += 1
        counts = _pulse_counts(text)
        orphan_rows.append({"artifact": label, **counts, "review_passes": passes})

    def manifest(rows):
        chars = sum(len(by_label[label]) for label in rows)
        return {"files": len(rows), "chars": chars,
                "estimated_tokens": round(chars / 4),
                "estimator": "chars/4 proxy (estimate)",
                "completeness": "unknown"}

    median_words = statistics.median(combined_words) if combined_words else None
    median_passes = statistics.median(combined_passes) if combined_passes else None
    return {
        "source": "explicit_public_snapshot",
        "window": {"week": week, "meaning": "caller_declared_cohort_not_verified_history"},
        "coverage": {"cohort_selection": "unverified", "completeness": "unknown"},
        "project_alias": project_alias,
        "commit_label": commit_label,
        "parents": parent_rows,
        "orphans": orphan_rows,
        "orphan_labels": sorted(orphans),
        "summary": {"artifact_count": len(parent_rows),
                    "orphan_count": len(orphan_rows),
                    "median_combined_words": median_words,
                    "max_combined_words": max(combined_words) if combined_words else None,
                    "median_review_passes": median_passes,
                    "max_review_passes": max(combined_passes) if combined_passes else None},
        "model_records": {"source": "declared_record_mix_not_metered_call_mix",
                          "by_tier": model_counts},
        "always_loaded": manifest(always_loaded),
        "deliberation": {**manifest(deliberation),
                         "always_loaded": False},
    }


def _pulse_week(value: object) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-W\d{2}", value):
        return False
    try:
        year, week = int(value[:4]), int(value[-2:])
        return datetime.date.fromisocalendar(year, week, 1).strftime("%G-W%V") == value
    except (ValueError, OverflowError):
        return False


def _pulse_text_is_safe(text: str) -> bool:
    return not any((ord(char) < 32 and char not in "\t\r\n")
                   or 0x7f <= ord(char) <= 0x9f for char in text)


def _pulse_validate_bundle(data: bytes) -> dict:
    if not isinstance(data, bytes) or len(data) > _PULSE_MAX_BYTES or b"\0" in data:
        raise ValueError("bundle")

    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate")
            result[key] = value
        return result

    def reject_constant(_value):
        raise ValueError("constant")

    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=unique_pairs,
                           parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError,
            TypeError, ValueError):
        raise ValueError("bundle") from None
    expected = {"schema", "project_alias", "week", "commit_label", "files",
                "always_loaded", "deliberation", "model_tiers"}
    if (type(value) is not dict or set(value) != expected
            or value["schema"] != _PULSE_SCHEMA
            or not isinstance(value["project_alias"], str)
            or not _PULSE_LABEL_RE.fullmatch(value["project_alias"])
            or not _pulse_week(value["week"])
            or (value["commit_label"] is not None and
                (not isinstance(value["commit_label"], str)
                 or not _PULSE_LABEL_RE.fullmatch(value["commit_label"])) )):
        raise ValueError("bundle")
    files = value["files"]
    if type(files) is not list or not 1 <= len(files) <= _PULSE_MAX_FILES:
        raise ValueError("bundle")
    labels = set()
    total_bytes = 0
    normalized_files = []
    for item in files:
        if type(item) is not dict or set(item) != {"artifact", "text"}:
            raise ValueError("bundle")
        label, text = item["artifact"], item["text"]
        if (not _pulse_safe_label(label) or not label.endswith(".md")
                or type(text) is not str or not _pulse_text_is_safe(text)):
            raise ValueError("bundle")
        raw = text.encode("utf-8")
        if len(raw) > _PULSE_MAX_FILE_BYTES:
            raise ValueError("bundle")
        total_bytes += len(raw)
        if total_bytes > _PULSE_MAX_BYTES or label in labels:
            raise ValueError("bundle")
        labels.add(label)
        normalized_files.append({"artifact": label, "text": text})
    categories = []
    for name in ("always_loaded", "deliberation"):
        rows = value[name]
        if type(rows) is not list or any(not _pulse_safe_label(item) for item in rows):
            raise ValueError("bundle")
        if len(rows) != len(set(rows)) or any(item not in labels for item in rows):
            raise ValueError("bundle")
        categories.append(set(rows))
    if categories[0] & categories[1] or not labels - categories[0] - categories[1]:
        raise ValueError("bundle")
    tiers = value["model_tiers"]
    if type(tiers) is not dict or len(tiers) > _PULSE_MAX_MODELS:
        raise ValueError("bundle")
    seen_families = set()
    for family, tier in tiers.items():
        if (not isinstance(family, str) or not family.strip() or len(family) > 128
                or any(ord(char) < 32 or 0x7f <= ord(char) <= 0x9f for char in family)
                or family.casefold() in seen_families
                or tier not in {"high", "medium", "low"}):
            raise ValueError("bundle")
        seen_families.add(family.casefold())
    return {**value, "files": normalized_files}


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

