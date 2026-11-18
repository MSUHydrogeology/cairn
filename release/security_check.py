#!/usr/bin/env python3
"""Cairn release security check -- fail closed until native evidence joins.

The dev-time Bandit gate (``tests/test_security_lint.py``)
*skips* when Bandit is absent locally, so a contributor without dev-deps
is not blocked. That is the wrong posture for a **release**: "the security
gate may have skipped on the machine that cut the release" is not
acceptable evidence. This command is the release-facing counterpart -- it
**fails closed**. A missing Bandit, a scanner error, a requested file the
scanner could not open, or any unallowlisted MEDIUM+ finding is a non-zero
exit.

Run from the Cairn repo root on each native host and retain the local record:

    python release/security_check.py --record /absolute/path/mac.json

The Windows host uses the same command with a distinct external record path.
Each clean local run prints ``INCOMPLETE`` and exits 5. Only the explicit join
on the clean final candidate can print ``PASS``:

    python release/security_check.py --join /absolute/path/mac.json /absolute/path/windows.json

**A repository-state preflight runs first and stops the command on failure**:
the invocation must name the checkout root, the worktree must be clean of
tracked *and untracked* changes, and ``HEAD`` must resolve to a full commit id.
A release security run is evidence about a *commit*; over a dirty tree it is
evidence about bytes nobody can fetch. The same state is re-checked after the
phases, and the full ``HEAD`` is printed in the summary so release notes can
bind the run to the tagged commit.

The checking phases do not execute from that operator checkout. The parent
creates a detached temporary worktree at the preflight commit, verifies every
leaf against the commit's Git blob id (and rejects extra ignored leaves), then
executes the committed checker there. The bytes are verified again before the
temporary worktree is removed. Thus an ignored pytest plugin or bytecode file
cannot influence the verdict, and repository-local checkout filters are never
executed while constructing the evidence tree.

**Four phases**, and every phase after the preflight is *attempted* even once
an earlier one has failed, so one run yields a complete repair list:

1. the repository-state preflight above;
2. Bandit over the derived shipped surface, plus the Markdown self-check
   (``tests/check_cairn.py``);
3. the shipped-only engine selection (``tests``) in default order;
   only fixed, source-reviewed opposite-platform node IDs may have their
   expected setup skip recorded;
4. ``tests/quality_gate.py`` with its seed-0 shipped-only child, plus
   vendor-neutrality and redundancy.

Each suite order records the exact collected IDs and setup/call/teardown
outcomes. Any missing, duplicate or deselected ID, collection skip, unexpected
skip, xfail, xpass, failure, phase failure or changed candidate refuses.
Successful local execution emits a structured record but remains
``INCOMPLETE`` (exit 5). The same runner's explicit join accepts exactly one
Mac and one Windows record at the clean current ``HEAD``, with matching Python
3.13 evidence and roster identity, and requires every native ID to pass once
in both orders on its native host. Only that join may print release-security
``PASS``. The Maintainer runs it at the final release point and attaches both
local records and the joined output to the existing release notes. A local
child pytest exit 5 remains a failure (no tests collected).

The Bandit surface is the same **derived** one as the dev gate -- every
file the scaffold ships **byte-for-byte** as Python, derived from the
published install manifest (``install_manifest``, the same enumeration
behind ``scaffold.py --manifest``), plus Cairn's own dev scripts and the
scaffold engine. This module is the
single source of the scan-target set and the Bandit allowlist; the dev
gate imports them (no second drift-prone copy).

**What this command does not do**, stated rather than implied: the parent
process that establishes and launches the committed checkout is not
authenticated, and nothing cryptographically binds its output to a release
tag. Running it, reading it, and recording it in the release notes is the
Maintainer's act -- see ``SECURITY.md`` and ``install/PROVENANCE.md``.

Manifest derivation per the ``scan-coverage`` plan; four-phase
orchestration per the ``release-security-orchestration`` plan.
"""
from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import os
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
from contextlib import ExitStack, contextmanager
from collections.abc import Callable, Mapping
from collections.abc import Iterator
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from install._scaffold.config import (  # noqa: E402  (trust anchor: narrowest owner, plan 0B.3 / Stage 4)
    _MODULE_MAPPINGS,
)
from install._scaffold.install import install_manifest  # noqa: E402
from install._scaffold.layout_catalog import LAYOUT_INSTALLS  # noqa: E402
from tests.security_manifest import (  # noqa: E402
    NATIVE_ONLY_POLICY_ID,
    release_excluded_files,
    validated_native_only_nodes,
)

_RELEASE_EXCLUDED = release_excluded_files()

_BLOCKING_SEVERITIES = {"MEDIUM", "HIGH"}

#: The **closed** set of severities a Bandit report may carry. Read from the
#: scanner's own source -- ``bandit.core.constants.RANKING`` under Bandit 1.9.4
#: -- not guessed, and hard-coded rather than imported because this module must
#: load on a machine with no Bandit installed (that is the whole point of the
#: fail-closed absence branch below).
#:
#: A value outside this set is **unclassifiable evidence**, not a
#: low-severity finding. Both severity predicates in this repository treat an
#: unknown value as "below MEDIUM", so a renamed or added Bandit severity would
#: be neither blocking nor liveness-confirming -- silently. Rejecting the report
#: at validation is one rule instead of teaching every predicate a fallback.
_KNOWN_SEVERITIES = frozenset({"UNDEFINED", "LOW", "MEDIUM", "HIGH"})

#: Fields every finding must carry for the rules below to mean anything.
_REQUIRED_FINDING_FIELDS = ("filename", "test_id", "issue_severity",
                            "line_number", "issue_text")
_REQUIRED_ERROR_FIELDS = ("filename", "reason")

#: The release-mode token, and its **one** recognized value.
#: ``tests/conftest.py`` reads exactly this pair and
#: refuses skipped / xfailed / xpassed outcomes when it matches; any other
#: value -- including the variable being absent -- leaves ordinary contributor
#: behaviour untouched. The pair lives here because this command is the only
#: thing that sets it.
RELEASE_GATE_ENV = "CAIRN_RELEASE_GATE_ACTIVE"
RELEASE_GATE_VALUE = "1"

NATIVE_RUN_NONCE_ENV = "CAIRN_NATIVE_RUN_NONCE"
NATIVE_RUN_HEAD_ENV = "CAIRN_NATIVE_RUN_HEAD"
NATIVE_RUN_POLICY_ENV = "CAIRN_NATIVE_RUN_POLICY_ID"
NATIVE_RUN_DEFAULT_REPORT_ENV = "CAIRN_NATIVE_RUN_DEFAULT_REPORT"
NATIVE_RUN_SEED0_REPORT_ENV = "CAIRN_NATIVE_RUN_SEED0_REPORT"
_NATIVE_RUN_SUMMARY_ENV = "CAIRN_NATIVE_RUN_SUMMARY"
_NATIVE_CONTEXT_ENV_NAMES = (
    NATIVE_RUN_NONCE_ENV, NATIVE_RUN_HEAD_ENV, NATIVE_RUN_POLICY_ENV,
    NATIVE_RUN_DEFAULT_REPORT_ENV, NATIVE_RUN_SEED0_REPORT_ENV,
)
_NATIVE_POLICY = validated_native_only_nodes()
_NATIVE_RUN_EVIDENCE: dict[str, dict] = {}
_PHASE_RESULTS: dict[str, str] = {}

#: Triaged-acceptable Bandit findings, keyed by (repo-relative file,
#: test_id), each with a mandatory rationale. The single source of truth
#: for both this release command and the dev gate.
#:
#: **Self-retiring.** ``run_bandit`` fails closed on any key here that the
#: scan does not actually report at blocking severity. A suppression that no
#: longer suppresses anything is not harmless: it is a standing permission for
#: a *future* finding at that (file, test_id), granted by a rationale written
#: about code that has since changed, and nothing would say so. Rationale
#: stays mandatory; liveness is an **additional** condition, not a substitute.
#:
#: On 2026-08-05 the sole entry
#: (``templates/modules/team-gated/link_check.py``, ``B310``) was measured
#: absent from the report -- Bandit 1.9.4 under Python 3.13.13 reports only
#: LOW findings there -- and was deleted rather than left as a latch. Its
#: rationale (the opt-in, SSRF-guarded external-link probe) is preserved in
#: that module and in ``SECURITY.md``'s documented residual risks. The current
#: entries below classify guarded Pulse XML parsing and fixed-pin,
#: verified-buffer helper loading; they remain subject to the same
#: report-liveness check.
ALLOWLIST: dict[tuple[str, str], str] = {
    ("install/_scaffold/lockfile.py", "B102"):
        "`_git_read_helper` executes only the bounded single-descriptor bytes "
        "from the fixed source-layout helper after literal `_GIT_READ_SHA256` "
        "comparison and descriptor/component rechecks; no target-supplied "
        "Python is executed.",
    ("dev/tools/content_scan_runner.py", "B102"):
        "`_load_verified_git_read` executes only the bounded, revalidated "
        "helper bytes from its fixed delivery root after the literal "
        "`_GIT_READ_SHA256` pin matches; target and CWD data do not select code.",
    ("dev/tools/prose_diff.py", "B102"):
        "`_load_git` executes only bounded, revalidated bytes from the fixed "
        "Git-helper destination after literal digest and applicable installed-lock "
        "checks; no target-supplied Python is executed.",
    ("dev/tools/exact_replace.py", "B102"):
        "`_load_module` executes only bounded, revalidated captured bytes for the "
        "fixed Git-helper or sibling-report destination after its caller-literal "
        "digest and applicable installed-lock checks; no target-supplied Python "
        "is executed.",
    ("templates/modules/team-gated/content_scan_runner.py", "B102"):
        "`_load_verified_git_read` executes only the bounded, revalidated "
        "helper bytes from the trusted packaged delivery root after the literal "
        "`_GIT_READ_SHA256` pin matches; inspected target and CWD data do not "
        "select code.",
    ("templates/modules/team-gated/prose_diff.py", "B102"):
        "`_load_git` executes only bounded, revalidated bytes from the fixed "
        "Git-helper destination after literal digest and applicable installed-lock "
        "checks; no target-supplied Python is executed.",
    ("templates/modules/team-gated/exact_replace.py", "B102"):
        "`_load_module` executes only bounded, revalidated captured bytes for the "
        "fixed Git-helper or sibling-report destination after its caller-literal "
        "digest and applicable installed-lock checks; no target-supplied Python "
        "is executed.",
    ("templates/skills/_lib/git_read.py", "B102"):
        "`load_verified_module` executes only the bounded bytes whose digest "
        "matches its explicit caller pin, without reopening, linked-path "
        "components, bytecode or module-cache reuse; this helper API does not "
        "authenticate the caller-supplied pin.",
    ("templates/skills/_lib/meter.py", "B102"):
        "`_verified_git_helper` executes only raw helper bytes from the fixed "
        "source/tools layout after the literal `SAFE_GIT_SOURCE_SHA256` pin "
        "matches; descriptor-relative or verified NTFS reading precedes "
        "execution, never target code.",
    ("templates/skills/_lib/pulse.py", "B314"):
        "`_parse_pulse_report` parses only bounded UTF-8 text after rejecting "
        "NUL, non-UTF-8 declarations, DOCTYPE and ENTITY; the input checks "
        "precede its sole ElementTree call. Reassess this path/rule allowance "
        "if that changes.",
    ("templates/skills/_lib/session.py", "B102"):
        "`_load_git_read_helper` executes only its bounded, revalidated "
        "sibling helper bytes after the literal `_GIT_READ_SHA256` pin "
        "matches; no target-selected source or unverified cached module is "
        "executed.",
    ("templates/modules/team-gated/_intent/conflict.py", "B102"):
        "`_git_read` resolves only its fixed packaged source/tools layout and "
        "literal `_GIT_READ_SHA256`, performs a bounded single-descriptor "
        "no-follow read with component and identity rechecks, then executes "
        "only that verified buffer with `dont_inherit=True`; target/CWD data "
        "select neither helper bytes nor expected pin.",
    ("tests/gen_legacy_code_review_passes.py", "B102"):
        "`_load_verified_git_read` executes only the bounded, revalidated "
        "helper bytes from the fixed source/tools layout after the literal "
        "`_GIT_READ_SHA256` pin matches; baseline and target data do not select code.",
    ("dev/tools/link_check.py", "B102"):
        "`_load_verified_git_read` executes only the bounded, revalidated "
        "helper bytes from the fixed source/tools layout after the literal "
        "`_GIT_READ_SHA256` pin matches; target and CWD data do not select code.",
    ("tests/tier_inventory.py", "B102"):
        "`_load_verified_git_read` executes only bounded, revalidated helper "
        "bytes from the fixed repository tool directory after the literal "
        "`_GIT_READ_SHA256` pin matches; selected paths cannot supply code.",
    ("tests/gauge.py", "B102"):
        "`_load_verified_git_read` executes only the bounded buffer read from "
        "the fixed repository helper path after descriptor and path-component "
        "rechecks and a match to the literal `_GIT_READ_SHA256` pin.",
    ("templates/modules/default-on/measurements.py", "B102"):
        "`_load_verified_git_read` executes only the bounded, revalidated "
        "helper bytes from the fixed installed path after the literal "
        "`_GIT_READ_SHA256` pin matches; registry data do not select code.",
    ("tests/measurements.py", "B102"):
        "`_load_verified_git_read` executes only the bounded, revalidated "
        "helper bytes from the fixed source/tools layout after the literal "
        "`_GIT_READ_SHA256` pin matches; registered measurements do not select code.",
    ("dev/tools/run_portable_security_sweeps.py", "B102"):
        "`_load_verified_git_read` executes only the bounded single-descriptor "
        "helper buffer from its fixed packaged source/tools root after literal "
        "`_GIT_READ_SHA256` comparison and component/identity rechecks; "
        "`dont_inherit=True` and source binding precede Git use, and target/CWD "
        "data selects neither code nor expected pin.",
    ("dev/tools/sync_doc_snippets.py", "B102"):
        "`_load_verified_git_read` executes only the bounded, revalidated "
        "helper bytes from the fixed source/tools layout after the literal "
        "`_GIT_READ_SHA256` pin matches; snippet inputs do not select code.",
    ("templates/modules/team-gated/link_check.py", "B102"):
        "`_load_verified_git_read` executes only the bounded, revalidated "
        "helper bytes from the trusted packaged source/tools layout after the "
        "literal `_GIT_READ_SHA256` pin matches; target data does not select code.",
    ("templates/modules/team-gated/run_portable_security_sweeps.py", "B102"):
        "`_load_verified_git_read` executes only the bounded single-descriptor "
        "helper buffer from its fixed packaged source/tools root after literal "
        "`_GIT_READ_SHA256` comparison and component/identity rechecks; "
        "`dont_inherit=True` and source binding precede Git use, and target/CWD "
        "data selects neither code nor expected pin.",
    ("templates/modules/team-gated/sync_doc_snippets.py", "B102"):
        "`_load_verified_git_read` executes only the bounded, revalidated "
        "helper bytes from the trusted packaged source/tools layout after the "
        "literal `_GIT_READ_SHA256` pin matches; snippet inputs do not select code.",
}


def _reject_duplicate_json_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_json_constant(token: str):
    raise ValueError(f"non-finite JSON number is forbidden: {token}")


def _load_strict_json(path: Path) -> object:
    """Read one regular JSON file, rejecting duplicate keys and NaN values."""
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"evidence path is not a regular file: {path}")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(fd, "rb") as stream:
        raw = stream.read()
    return json.loads(raw.decode("utf-8"),
                      object_pairs_hook=_reject_duplicate_json_keys,
                      parse_constant=_reject_json_constant)


def _exact_keys(value: object, keys: set[str], where: str) -> dict:
    if type(value) is not dict or set(value) != keys:
        raise ValueError(f"{where} has an unexpected shape")
    return value


def _is_full_sha(value: object) -> bool:
    """Accept only complete SHA-1 or SHA-256 Git object IDs."""
    return (type(value) is str and len(value) in {40, 64}
            and all(c in "0123456789abcdef" for c in value))


def _supported_native_host(platform_name: object, os_name: object) -> str:
    if platform_name == "darwin" and os_name == "posix":
        return "posix"
    if platform_name == "win32" and os_name == "nt":
        return "nt"
    raise ValueError("native evidence platform is unsupported or inconsistent")


def _validate_outcome_rows(collection_ids: list[str], rows: object,
                           host_tag: str, where: str) -> dict[str, dict]:
    if type(rows) is not list:
        raise ValueError(f"{where} outcomes are not a list")
    by_id: dict[str, dict] = {}
    for index, raw in enumerate(rows):
        row = _exact_keys(raw, {"nodeid", "status", "phases"},
                          f"{where} outcome {index}")
        nodeid = row["nodeid"]
        if type(nodeid) is not str or nodeid in by_id:
            raise ValueError(f"{where} has a duplicate or malformed outcome ID")
        if type(row["status"]) is not str:
            raise ValueError(f"{where} outcome status is malformed")
        phases = row["phases"]
        if type(phases) is not dict:
            raise ValueError(f"{where} outcome phases are malformed")
        for phase_name, phase_value in phases.items():
            if phase_name not in {"setup", "call", "teardown"}:
                raise ValueError(f"{where} has an unknown test phase")
            phase = _exact_keys(phase_value, {"outcome", "wasxfail"},
                                f"{where} {phase_name}")
            if (type(phase["outcome"]) is not str
                    or phase["outcome"] not in {"passed", "skipped", "failed"}
                    or type(phase["wasxfail"]) is not bool):
                raise ValueError(f"{where} has a malformed raw phase fact")
        expected_native = NATIVE_POLICY_BY_ID.get(nodeid, (None, None))[0]
        eligible_skip = expected_native is not None and expected_native != host_tag
        if (set(phases) == {"setup", "call", "teardown"}
                and all(phases[name] == {"outcome": "passed", "wasxfail": False}
                        for name in ("setup", "call", "teardown"))):
            status = "PASS"
        elif (eligible_skip and set(phases) == {"setup", "teardown"}
              and phases["setup"] == {"outcome": "skipped", "wasxfail": False}
              and phases["teardown"] == {"outcome": "passed", "wasxfail": False}):
            status = "SKIP"
        else:
            raise ValueError(f"{where} has an ineligible or incomplete outcome: {nodeid}")
        if row["status"] != status:
            raise ValueError(f"{where} status disagrees with raw phase facts")
        by_id[nodeid] = {"nodeid": nodeid, "status": status, "phases": phases}
    if set(by_id) != set(collection_ids):
        raise ValueError(f"{where} outcome coverage differs from collection")
    required = set().union(*_NATIVE_POLICY.values())
    if not required <= set(by_id):
        raise ValueError(f"{where} is missing fixed native IDs")
    for nodeid, (tag, _) in NATIVE_POLICY_BY_ID.items():
        status = by_id[nodeid]["status"]
        if tag == host_tag and status != "PASS":
            raise ValueError(f"native node did not pass on its host: {nodeid}")
        if tag != host_tag and status not in {"PASS", "SKIP"}:
            raise ValueError(f"opposite-platform node has invalid outcome: {nodeid}")
    return by_id


NATIVE_POLICY_ROWS = tuple(
    (host, nodeid)
    for host in ("nt", "posix")
    for nodeid in sorted(_NATIVE_POLICY[host])
)
NATIVE_POLICY_BY_ID = {nodeid: (host, nodeid)
                       for host, nodeid in NATIVE_POLICY_ROWS}


def _validate_raw_suite_report(raw: object, *, nonce: str, head: str,
                               order: str, platform_name: str,
                               os_name: str) -> dict:
    report = _exact_keys(raw, {
        "schema", "nonce", "head", "policy_id", "platform", "os_name",
        "python", "order", "seed", "collection_input_ids", "collected_ids",
        "collection_reports", "runtime_reports", "pytest_exit",
    }, "suite report")
    seed = None if order == "default" else 0
    seed_matches = (report["seed"] is None if order == "default" else
                    type(report["seed"]) is int and report["seed"] == 0)
    if (type(report["schema"]) is not int or report["schema"] != 1
            or report["nonce"] != nonce or report["head"] != head
            or report["policy_id"] != NATIVE_ONLY_POLICY_ID
            or report["platform"] != platform_name or report["os_name"] != os_name
            or report["order"] != order or not seed_matches
            or type(report["pytest_exit"]) is not int
            or report["pytest_exit"] != 0):
        raise ValueError("suite report identity, order or phase result mismatches")
    version = report["python"]
    if (type(version) is not list or len(version) != 3
            or any(type(part) is not int for part in version)
            or version[:2] != [3, 13]):
        raise ValueError("suite report is not from Python 3.13")
    input_ids = report["collection_input_ids"]
    collected_ids = report["collected_ids"]
    for label, ids in (("pre-modifier", input_ids), ("final", collected_ids)):
        if (type(ids) is not list or any(type(node) is not str or not node for node in ids)
                or len(set(ids)) != len(ids)):
            raise ValueError(f"suite {label} collection IDs are malformed or repeated")
    if set(input_ids) != set(collected_ids) or len(input_ids) != len(collected_ids):
        raise ValueError("suite collection was deselected or changed")
    if type(report["collection_reports"]) is not list:
        raise ValueError("suite collection reports are malformed")
    collected_report_ids = set()
    for raw_collect in report["collection_reports"]:
        collect = _exact_keys(raw_collect, {"nodeid", "outcome", "wasxfail"},
                              "collection report")
        if (type(collect["nodeid"]) is not str
                or collect["nodeid"] in collected_report_ids
                or collect["outcome"] != "passed"
                or type(collect["wasxfail"]) is not bool
                or collect["wasxfail"]):
            raise ValueError("collection skip or failure is incomplete evidence")
        collected_report_ids.add(collect["nodeid"])
    outcomes: dict[str, dict[str, dict]] = {}
    if type(report["runtime_reports"]) is not list:
        raise ValueError("suite runtime reports are malformed")
    for index, raw_phase in enumerate(report["runtime_reports"]):
        phase = _exact_keys(raw_phase, {"nodeid", "when", "outcome", "wasxfail"},
                            f"runtime report {index}")
        nodeid = phase["nodeid"]
        when = phase["when"]
        if (type(nodeid) is not str or type(when) is not str
                or when not in {"setup", "call", "teardown"}
                or type(phase["outcome"]) is not str
                or phase["outcome"] not in {"passed", "skipped", "failed"}
                or type(phase["wasxfail"]) is not bool
                or nodeid not in collected_ids):
            raise ValueError("malformed, unknown or uncollected runtime report")
        phases = outcomes.setdefault(nodeid, {})
        if when in phases:
            raise ValueError(f"duplicate runtime phase for node: {nodeid} {when}")
        phases[when] = {"outcome": phase["outcome"],
                        "wasxfail": phase["wasxfail"]}
    rows = []
    host_tag = _supported_native_host(platform_name, os_name)
    for nodeid in sorted(collected_ids):
        phases = outcomes.get(nodeid, {})
        if (set(phases) == {"setup", "call", "teardown"}
                and all(phases[name] == {"outcome": "passed", "wasxfail": False}
                        for name in ("setup", "call", "teardown"))):
            status = "PASS"
        elif (NATIVE_POLICY_BY_ID.get(nodeid, (None, None))[0] != host_tag
              and set(phases) == {"setup", "teardown"}
              and phases.get("setup") == {"outcome": "skipped", "wasxfail": False}
              and phases.get("teardown") == {"outcome": "passed", "wasxfail": False}):
            status = "SKIP"
        else:
            raise ValueError(f"suite node has incomplete or refused outcome: {nodeid}")
        rows.append({"nodeid": nodeid, "status": status, "phases": phases})
    normalized = _validate_outcome_rows(collected_ids, rows, host_tag, order)
    return {"label": order, "seed": seed,
            "collection_ids": sorted(collected_ids),
            "outcomes": [normalized[node] for node in sorted(normalized)]}


def _is_sha256(value: object) -> bool:
    return (type(value) is str and len(value) == 64
            and all(c in "0123456789abcdef" for c in value))


def _validate_history_sweep_record(raw: object, expected_head: str) -> dict:
    sweep = _exact_keys(raw, {
        "manifest_sha256", "pack_sha256", "candidate",
        "projection_before", "projection_after", "sweep",
    }, "history sweep record")
    for key in ("manifest_sha256", "pack_sha256"):
        if not _is_sha256(sweep[key]):
            raise ValueError(f"history sweep {key} is malformed")
    if not _is_full_sha(sweep["candidate"]) or sweep["candidate"] != expected_head:
        raise ValueError("history sweep candidate SHA mismatch")
    for label in ("projection_before", "projection_after"):
        proj = _exact_keys(sweep[label], {
            "head", "projected_count", "projected_sha256",
            "object_count", "objects_sha256",
        }, f"history sweep {label}")
        if not _is_full_sha(proj["head"]) or proj["head"] != expected_head:
            raise ValueError(f"{label} head mismatch")
        if type(proj["projected_count"]) is not int or proj["projected_count"] < 0:
            raise ValueError(f"{label} projected_count is malformed")
        if type(proj["object_count"]) is not int or proj["object_count"] <= 0:
            raise ValueError(f"{label} object_count is malformed")
        if not _is_sha256(proj["projected_sha256"]):
            raise ValueError(f"{label} projected_sha256 is malformed")
        if not _is_sha256(proj["objects_sha256"]):
            raise ValueError(f"{label} objects_sha256 is malformed")
    if sweep["projection_before"] != sweep["projection_after"]:
        raise ValueError("frozen history projection drifted during scan")
    sw = _exact_keys(sweep["sweep"], {
        "result", "mode", "legs", "adapter_version", "adapter_digest",
        "policy_sha256", "runner_sha256",
    }, "history sweep summary")
    if type(sw["result"]) is not int or sw["result"] != 0 or sw["mode"] != "full":
        raise ValueError("history sweep did not pass in full mode")
    if not _is_sha256(sw["adapter_digest"]):
        raise ValueError("history sweep adapter_digest is malformed")
    if not _is_sha256(sw["policy_sha256"]):
        raise ValueError("history sweep policy_sha256 is malformed")
    if not _is_sha256(sw["runner_sha256"]):
        raise ValueError("history sweep runner_sha256 is malformed")
    if type(sw["adapter_version"]) is not str or not sw["adapter_version"]:
        raise ValueError("history sweep adapter_version is malformed")
    legs = sw["legs"]
    if type(legs) is not dict or set(legs) != {"current-tree", "history"}:
        raise ValueError("history sweep must report both current-tree and history legs")
    for leg_name, leg_row in legs.items():
        row = _exact_keys(leg_row, {"status", "result", "finding_count"}, f"{leg_name} leg")
        if row["status"] != "CLEAN" or type(row["result"]) is not int or row["result"] != 0:
            raise ValueError(f"history sweep {leg_name} leg is not CLEAN")
        if type(row["finding_count"]) is not int or row["finding_count"] != 0:
            raise ValueError(f"history sweep {leg_name} leg reported findings")
    return sweep


def _validate_local_record(raw: object, expected_head: str) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("local record must be a JSON object")
    allowed = {
        "schema", "kind", "head", "platform", "os_name", "python",
        "policy_id", "nonce", "phases", "orders", "excluded",
    }
    if "history_sweep" in raw:
        allowed.add("history_sweep")
    record = _exact_keys(raw, allowed, "local record")
    if (type(record["schema"]) is not int or record["schema"] != 1
            or record["kind"] != "cairn-native-local-v1"
            or not _is_full_sha(record["head"]) or record["head"] != expected_head
            or record["policy_id"] != NATIVE_ONLY_POLICY_ID):
        raise ValueError("local record SHA, schema or roster identity mismatch")
    nonce = record["nonce"]
    if (type(nonce) is not str or len(nonce) != 64
            or any(c not in "0123456789abcdef" for c in nonce)):
        raise ValueError("local record nonce is malformed")
    host_tag = _supported_native_host(record["platform"], record["os_name"])
    version = record["python"]
    if (type(version) is not list or len(version) != 3
            or any(type(part) is not int for part in version)
            or version[:2] != [3, 13]):
        raise ValueError("local record is not from Python 3.13")
    phases = _exact_keys(record["phases"], {
        "bandit", "check_cairn", "release-mode suite", "quality_gate",
    }, "local phase results")
    if any(type(value) is not str or value != "PASS" for value in phases.values()):
        raise ValueError("local record contains a failed phase")
    orders = _exact_keys(record["orders"], {"default", "seed-0"}, "local orders")
    order_ids = {}
    for label, expected_seed in (("default", None), ("seed-0", 0)):
        order = _exact_keys(orders[label], {
            "label", "seed", "collection_ids", "outcomes",
        }, f"{label} order")
        seed_matches = (order["seed"] is None if expected_seed is None else
                        type(order["seed"]) is int and order["seed"] == 0)
        if order["label"] != label or not seed_matches:
            raise ValueError("suite order label or seed was substituted")
        ids = order["collection_ids"]
        if (type(ids) is not list or any(type(node) is not str or not node for node in ids)
                or len(ids) != len(set(ids))):
            raise ValueError("local collection IDs are malformed or repeated")
        required = set().union(*_NATIVE_POLICY.values())
        if not required <= set(ids):
            raise ValueError("local record omits fixed native IDs")
        _validate_outcome_rows(ids, order["outcomes"], host_tag, label)
        order_ids[label] = set(ids)
    if order_ids["default"] != order_ids["seed-0"]:
        raise ValueError("default and seed-0 collection sets differ")
    excluded = _exact_keys(record["excluded"], {"files", "count"},
                           "local excluded-test summary")
    excluded_files = excluded["files"]
    excluded_count = excluded["count"]
    expected_excluded = sorted(_RELEASE_EXCLUDED)
    if (type(excluded_files) is not list
            or any(type(path) is not str or not path for path in excluded_files)
            or excluded_files != expected_excluded):
        raise ValueError("local excluded-test file list differs from the manifest")
    if (type(excluded_count) is not int
            or excluded_count < len(excluded_files)
            or (not excluded_files and excluded_count != 0)
            or (excluded_files and excluded_count == 0)):
        raise ValueError("local excluded-test count is malformed")
    for label, ids in order_ids.items():
        if any(node.split("::", 1)[0] in _RELEASE_EXCLUDED for node in ids):
            raise ValueError(f"{label} order collected an excluded test file")
    if "history_sweep" in record:
        _validate_history_sweep_record(record["history_sweep"], expected_head)
    return record


def _build_local_record(head: str, nonce: str, platform_name: str,
                        os_name: str, version: list[int], phases: dict[str, str],
                        orders: dict[str, dict], excluded: dict) -> dict:
    return {
        "schema": 1,
        "kind": "cairn-native-local-v1",
        "head": head,
        "platform": platform_name,
        "os_name": os_name,
        "python": version,
        "policy_id": NATIVE_ONLY_POLICY_ID,
        "nonce": nonce,
        "phases": phases,
        "orders": orders,
        "excluded": excluded,
    }


def _measure_excluded_tests(root: Path) -> dict[str, object]:
    """Collect only listed files to record the exact unrun test count."""
    paths = sorted(_RELEASE_EXCLUDED)
    if not paths:
        return {"files": [], "count": 0}
    for rel in paths:
        path = root / rel
        if not path.is_file():
            raise ValueError(f"excluded test path is not a file: {rel}")
    env = _release_child_env()
    env.pop(RELEASE_GATE_ENV, None)
    for name in _NATIVE_CONTEXT_ENV_NAMES:
        env.pop(name, None)
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", *paths, "--collect-only", "-q",
             "-p", "no:cacheprovider"],
            cwd=str(root), env=env, capture_output=True, text=True, check=False,
        )
    except OSError as exc:
        raise ValueError(f"cannot collect excluded test files: {exc}") from exc
    if proc.returncode != 0:
        raise ValueError("excluded-test collection failed")
    counts = {
        rel: sum(line.startswith(rel + "::") for line in proc.stdout.splitlines())
        for rel in paths
    }
    if any(count == 0 for count in counts.values()):
        raise ValueError("an excluded test file collected no test IDs")
    return {"files": paths, "count": sum(counts.values())}


def _write_exclusive_json(path: Path, value: object, root: Path) -> None:
    resolved = path.resolve()
    if (not path.is_absolute() or resolved.is_relative_to(root.resolve())
            or path.exists() or path.is_symlink() or not path.parent.is_dir()):
        raise ValueError("evidence output must be a new external absolute path")
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                allow_nan=False).encode("ascii"))
        stream.flush()
        os.fsync(stream.fileno())


def _native_context_from_environment() -> dict[str, str] | None:
    values = [os.environ.get(name) for name in _NATIVE_CONTEXT_ENV_NAMES]
    if not any(value is not None for value in values):
        return None
    if any(not value for value in values):
        raise ValueError("incomplete strict native evidence context")
    nonce, head, policy_id, default_report, seed0_report = values
    if (len(nonce) != 64 or any(c not in "0123456789abcdef" for c in nonce)
            or not _is_full_sha(head) or policy_id != NATIVE_ONLY_POLICY_ID):
        raise ValueError("malformed strict native evidence identity")
    if _supported_native_host(sys.platform, os.name) not in {"nt", "posix"}:
        raise ValueError("unsupported native evidence host")
    paths = [Path(default_report), Path(seed0_report)]
    resolved = [path.resolve() for path in paths]
    root = CAIRN_ROOT.resolve()
    if (any(not path.is_absolute() for path in paths)
            or any(path.is_relative_to(root) for path in resolved)
            or resolved[0] == resolved[1]):
        raise ValueError("native suite reports must be distinct external paths")
    return {
        "nonce": nonce,
        "head": head,
        "policy_id": policy_id,
        "default_report": str(paths[0]),
        "seed0_report": str(paths[1]),
    }


def _consume_suite_report(order: str) -> dict:
    context = _native_context_from_environment()
    if context is None:
        raise ValueError("strict native evidence context is absent")
    key = "default_report" if order == "default" else "seed0_report"
    path = Path(context[key])
    raw = _load_strict_json(path)
    normalized = _validate_raw_suite_report(
        raw, nonce=context["nonce"], head=context["head"], order=order,
        platform_name=sys.platform, os_name=os.name)
    path.unlink()
    if path.exists() or path.is_symlink():
        raise ValueError("strict suite report could not be consumed")
    return normalized


def _tracked_test_files(head: str) -> set[str]:
    """Return committed pytest files under tests at *head*."""
    blobs = _committed_blobs(CAIRN_ROOT, head)
    return {
        rel for rel in blobs
        if rel.startswith("tests/")
        and rel.endswith(".py")
        and (Path(rel).name.startswith("test_")
             or Path(rel).name.endswith("_test.py"))
    }


def _join_local_records(record_paths: list[Path], head: str) -> dict[str, object]:
    if len(record_paths) != 2 or len({path.resolve() for path in record_paths}) != 2:
        raise ValueError("join requires two distinct local record files")
    records = [_validate_local_record(_load_strict_json(path), head)
               for path in record_paths]
    by_platform = {record["platform"]: record for record in records}
    if set(by_platform) != {"darwin", "win32"}:
        raise ValueError("join requires exactly one Mac and one Windows record")
    mac, windows = by_platform["darwin"], by_platform["win32"]
    if (mac["head"] != windows["head"]
            or mac["policy_id"] != windows["policy_id"]):
        raise ValueError("native records do not name the same commit and roster")
    mac_excluded = mac["excluded"]
    windows_excluded = windows["excluded"]
    if mac_excluded != windows_excluded:
        raise ValueError("native records disagree on excluded tests")
    tracked = _tracked_test_files(head)
    if not _RELEASE_EXCLUDED <= tracked:
        raise ValueError("release exclusion list contains an untracked test file")
    expected_files = tracked - _RELEASE_EXCLUDED
    for label in ("default", "seed-0"):
        for record in (mac, windows):
            collected_files = {
                node.split("::", 1)[0]
                for node in record["orders"][label]["collection_ids"]
            }
            if collected_files != expected_files:
                raise ValueError(
                    f"{record['platform']} {label} collected files differ "
                    "from tracked release selection")
        mac_outcomes = {row["nodeid"]: row for row in mac["orders"][label]["outcomes"]}
        win_outcomes = {row["nodeid"]: row for row in windows["orders"][label]["outcomes"]}
        common = set(mac_outcomes) & set(win_outcomes)
        if not set().union(*_NATIVE_POLICY.values()) <= common:
            raise ValueError("native counterpart outcomes are incomplete")
        for host_tag, platform, outcomes in (("posix", "darwin", mac_outcomes),
                                             ("nt", "win32", win_outcomes)):
            for nodeid in _NATIVE_POLICY[host_tag]:
                if outcomes[nodeid]["status"] != "PASS":
                    raise ValueError(
                        f"native counterpart did not pass {label}: {nodeid}")
    return mac_excluded


# ===========================================================================
# Phase 1 -- repository-state preflight / postflight
# ===========================================================================
#
# A release security run is evidence ABOUT A COMMIT. Run over a dirty tree it
# is evidence about nothing citable: the bytes that were scanned are not the
# bytes anyone can fetch. So the command establishes three facts before any
# scanner runs -- this invocation names the checkout root, the worktree is
# clean of tracked AND untracked changes, and HEAD resolves to a full commit
# id -- and re-establishes the first two afterwards, so a candidate that
# changed mid-run cannot be reported as clean.
#
# Untracked files are refused, not tolerated. Cairn's own tree reproduced the
# fail-open on 2026-08-05: an untracked `.py` under a scanned root is a file
# the release scan may open and no adopter can fetch.


class _RepoStateError(RuntimeError):
    """A repository fact the command could not establish.

    Never converted into "the fact does not hold" -- an unestablishable state
    is a fail-closed condition of its own, which is why every raiser reports
    the git stderr rather than returning a bare False.
    """


#: Git config forced onto every invocation below. Same posture -- and the
#: same reasons, each verified against a real attack in that module's review
#: rounds -- as ``tests/_gate_preflight._STERILE_CONFIG``: an
#: in-repo ``.git/config`` key must not be able to steer, or execute during,
#: the state check that decides whether a release may be cut. Command-line
#: ``-c`` outranks system, global, repository and worktree config.
#:
#: Deliberately a NARROW SECOND INSTANCE rather than an import. The trust-root
#: pattern lives in ``tests/`` and pulls in ``_gate_manifest`` and
#: ``_gate_reanchor``; importing the test package into the release command
#: would make Cairn's release gate depend on its own gate-ceremony tooling and
#: invert the dependency direction. What is reused is the pattern, named here
#: so the two can be compared by a reader.
_STERILE_GIT_CONFIG: dict[str, str] = {
    "core.useReplaceRefs": "false",   # refs/replace/<sha> forges `show` output
    "core.hooksPath": os.devnull,     # a hook is candidate-supplied execution
    "core.fsmonitor": "false",        # a monitor program runs during `status`
    "core.quotePath": "false",        # non-ASCII paths must read back raw
    "diff.external": "",
    "core.pager": "cat",
}


def _sterile_git_env() -> dict[str, str]:
    """The child environment for the state-check git calls.

    Every ``GIT_*`` variable is **dropped** rather than denylisted by name.
    The steering set is large (``GIT_DIR``, ``GIT_WORK_TREE``,
    ``GIT_INDEX_FILE``, ``GIT_CONFIG_*``, ``GIT_EXTERNAL_DIFF``,
    ``GIT_OBJECT_DIRECTORY``, the pathspec flags) and grows between releases,
    so dropping the prefix and putting back what is needed fails safe where an
    enumerated denylist does not. The rest of the environment is the
    operator's and is left alone -- a scope statement, not a trust claim.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _git_at(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    """Run one text-producing Git command against *repo_root*, sterilised."""
    git = shutil.which("git")
    if git is None:
        raise _RepoStateError("git was not found on PATH")
    overrides: list[str] = []
    for key, value in _STERILE_GIT_CONFIG.items():
        overrides += ["-c", f"{key}={value}"]
    try:
        return subprocess.run(
            [git, "-C", str(repo_root), *overrides, *args],
            capture_output=True, text=True, check=False,
            env=_sterile_git_env(),
        )
    except OSError as exc:
        raise _RepoStateError(f"could not run git ({exc})") from None


def _git(*args: str) -> subprocess.CompletedProcess:
    """Run one Git command against ``CAIRN_ROOT``."""
    return _git_at(CAIRN_ROOT, *args)


def _git_bytes_at(repo_root: Path, *args: str,
                  input_bytes: bytes | None = None) -> subprocess.CompletedProcess:
    """Binary-output counterpart used for NUL-delimited tree records."""
    git = shutil.which("git")
    if git is None:
        raise _RepoStateError("git was not found on PATH")
    overrides: list[str] = []
    for key, value in _STERILE_GIT_CONFIG.items():
        overrides += ["-c", f"{key}={value}"]
    try:
        return subprocess.run(
            [git, "-C", str(repo_root), *overrides, *args],
            capture_output=True, text=False, check=False,
            env=_sterile_git_env(), input=input_bytes,
        )
    except OSError as exc:
        raise _RepoStateError(f"could not run git ({exc})") from None


def _require_checkout_root() -> None:
    """Refuse unless ``CAIRN_ROOT`` is the top level of the worktree.

    ``git -C <path>`` **discovers upward**, so "a repository answered" is not
    "the repository this command names answered": run from a copy of the tree
    nested under some other checkout, every state check below would report on
    that outer repository and the run would pass against a commit the operator
    never named.
    """
    p = _git("rev-parse", "--show-toplevel")
    top = (p.stdout or "").strip()
    if p.returncode != 0 or not top:
        raise _RepoStateError(
            f"{CAIRN_ROOT} is not inside a git repository "
            f"({(p.stderr or '').strip() or 'git rev-parse failed'})")
    if Path(top).resolve() != CAIRN_ROOT.resolve():
        raise _RepoStateError(
            f"{CAIRN_ROOT} is not the top level of a git worktree -- git "
            f"discovered {Path(top).resolve()} by walking upward")


def _head_commit() -> str:
    """The full object id of ``HEAD`` at this repository's format, or raise."""
    p = _git("rev-parse", "--verify", "--end-of-options", "HEAD^{commit}")
    sha = (p.stdout or "").strip()
    # Width comes from the repository's object format, never a literal 40: a
    # SHA-256 repository returns a valid 64-hex HEAD, and a fixed-width check
    # rejects it before any helper is reached.
    width = _OBJECT_FORMAT_WIDTH[_repository_object_format(CAIRN_ROOT)]
    if p.returncode != 0 or len(sha) != width or any(
            c not in "0123456789abcdef" for c in sha):
        raise _RepoStateError(
            f"HEAD does not resolve to a full commit id "
            f"({(p.stderr or '').strip() or sha!r})")
    return sha


def _dirty_entries() -> list[str]:
    """Porcelain status lines for tracked **and untracked** changes."""
    p = _git("status", "--porcelain", "--untracked-files=all")
    if p.returncode != 0:
        raise _RepoStateError(
            f"could not read the worktree status "
            f"({(p.stderr or '').strip() or 'git status failed'})")
    return [ln for ln in (p.stdout or "").splitlines() if ln.strip()]


def _format_dirty(entries: list[str]) -> str:
    shown = ", ".join(ln[3:] for ln in entries[:5])
    more = f" (+{len(entries) - 5} more)" if len(entries) > 5 else ""
    return shown + more


def repo_state_preflight() -> tuple[int, str | None]:
    """Phase 1. Returns ``(rc, head)``; ``head`` is None on any refusal."""
    try:
        _require_checkout_root()
        head = _head_commit()
        dirty = _dirty_entries()
    except _RepoStateError as exc:
        print(f"security_check: repository state could not be established "
              f"({exc}) -- FAIL CLOSED. A release security run must name the "
              f"commit it is evidence about.", file=sys.stderr)
        return 1, None
    if dirty:
        print(f"security_check: worktree is not clean ({len(dirty)} tracked or "
              f"untracked change(s)) -- FAIL CLOSED. The bytes scanned must be "
              f"the bytes the tagged commit carries: "
              f"{_format_dirty(dirty)}", file=sys.stderr)
        return 1, None
    print(f"security_check: preflight OK -- clean worktree at {head}.")
    return 0, head


def repo_state_postflight(head: str) -> int:
    """Phase 1, second half: the candidate must not have moved mid-run."""
    try:
        now = _head_commit()
        dirty = _dirty_entries()
    except _RepoStateError as exc:
        print(f"security_check: repository state could not be re-established "
              f"after the phases ({exc}) -- FAIL CLOSED.", file=sys.stderr)
        return 1
    if now != head:
        print(f"security_check: HEAD moved during the run ({head} -> {now}) "
              f"-- FAIL CLOSED. The phases above measured a candidate that is "
              f"no longer checked out.", file=sys.stderr)
        return 1
    if dirty:
        print(f"security_check: the worktree was modified during the run "
              f"({len(dirty)} change(s)) -- FAIL CLOSED. "
              f"{_format_dirty(dirty)}", file=sys.stderr)
        return 1
    return 0


#: Object format -> full object-id width. The single place a width is named.
_OBJECT_FORMAT_WIDTH = {"sha1": 40, "sha256": 64}


def _repository_object_format(repo_root: Path) -> str:
    """The repository's own object format, or a refusal.

    **There is no default.** A missing, unreadable or non-repository root
    refuses rather than falling back to Git's process default of SHA-1 --
    that fallback is precisely the failure this function exists to remove.
    """
    proc = _git_at(repo_root, "rev-parse", "--show-object-format")
    fmt = (proc.stdout or "").strip()
    if proc.returncode != 0 or fmt not in _OBJECT_FORMAT_WIDTH:
        raise _RepoStateError(
            f"could not establish the object format of {str(repo_root)!r} "
            f"({(proc.stderr or '').strip() or fmt!r}); refusing rather than "
            f"assuming SHA-1")
    return fmt


def _blob_oid_at(repo_root: Path, data: bytes) -> str:
    """Ask **Git** for the blob id of *data*, under *repo_root*'s format.

    Replaces a Python reimplementation of Git's blob framing
    (``b"blob " + len + NUL + data`` hashed with sha1/sha256). Cairn does not
    reimplement a Git object algorithm when the native plumbing produces the
    same fact.

    The call is sterile and read-only by construction: **no ``-w``** (nothing
    is written to the object database), **no path argument and no ``--path``**
    (so no `.gitattributes` filter or eol conversion participates), and the
    repository is **explicit** -- there is no default root.
    """
    fmt = _repository_object_format(repo_root)
    width = _OBJECT_FORMAT_WIDTH[fmt]
    proc = _git_bytes_at(repo_root, "hash-object", "-t", "blob", "--stdin",
                         input_bytes=data)
    oid = os.fsdecode(proc.stdout or b"").strip()
    if proc.returncode != 0 or len(oid) != width or any(
            c not in "0123456789abcdef" for c in oid):
        detail = os.fsdecode(proc.stderr or b"").strip()
        raise _RepoStateError(
            f"git hash-object did not return a {width}-hex {fmt} id "
            f"({detail or oid!r})")
    return oid


def _committed_blobs(repo_root: Path, head: str) -> dict[str, tuple[str, str]]:
    """Return ``path -> (mode, oid)`` for every committed blob at *head*."""
    proc = _git_bytes_at(repo_root, "ls-tree", "-r", "-z", "--full-tree", head)
    if proc.returncode != 0:
        detail = os.fsdecode(proc.stderr or b"").strip()
        raise _RepoStateError(
            f"could not enumerate committed tree {head} "
            f"({detail or 'git ls-tree failed'})")
    entries: dict[str, tuple[str, str]] = {}
    for record in (proc.stdout or b"").split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            raw_mode, raw_kind, raw_oid = metadata.split(b" ", 2)
        except ValueError as exc:
            raise _RepoStateError(
                "git ls-tree returned a malformed NUL-delimited record") from exc
        rel = os.fsdecode(raw_path)
        path = Path(rel)
        if path.is_absolute() or not path.parts or ".." in path.parts:
            raise _RepoStateError(
                f"committed tree contains unsafe path {rel!r}")
        if raw_kind != b"blob":
            raise _RepoStateError(
                f"committed path {rel!r} is {os.fsdecode(raw_kind)!r}, not a "
                "self-contained blob (submodules are not release evidence)")
        if rel in entries:
            raise _RepoStateError(f"committed tree repeats path {rel!r}")
        entries[rel] = (raw_mode.decode("ascii"), raw_oid.decode("ascii"))
    if not entries:
        raise _RepoStateError("committed tree contains no blobs")
    return entries


def _checkout_leaf_paths(repo_root: Path) -> set[str]:
    """Enumerate every non-directory worktree object except Git metadata."""
    leaves: set[str] = set()
    try:
        for base, dirs, files in os.walk(repo_root, followlinks=False):
            base_path = Path(base)
            if base_path == repo_root:
                dirs[:] = [name for name in dirs if name != ".git"]
                files = [name for name in files if name != ".git"]
            for name in list(dirs):
                candidate = base_path / name
                if candidate.is_symlink():
                    leaves.add(candidate.relative_to(repo_root).as_posix())
                    dirs.remove(name)
            for name in files:
                leaves.add((base_path / name).relative_to(repo_root).as_posix())
    except OSError as exc:
        raise _RepoStateError(
            f"could not enumerate detached checkout bytes ({exc})") from None
    return leaves


def _read_committed_payloads(
        repo_root: Path,
        entries: Mapping[str, tuple[str, str]]) -> dict[str, bytes]:
    """Read every requested blob in one ``git cat-file --batch`` exchange."""
    ordered = list(entries.items())
    request = b"".join(oid.encode("ascii") + b"\n"
                       for _rel, (_mode, oid) in ordered)
    proc = _git_bytes_at(
        repo_root, "cat-file", "--batch", input_bytes=request)
    if proc.returncode != 0:
        detail = os.fsdecode(proc.stderr or b"").strip()
        raise _RepoStateError(
            f"could not read committed blobs ({detail or 'git cat-file failed'})")
    output = proc.stdout or b""
    cursor = 0
    payloads: dict[str, bytes] = {}
    for rel, (_mode, expected_oid) in ordered:
        line_end = output.find(b"\n", cursor)
        if line_end < 0:
            raise _RepoStateError("git cat-file returned a truncated header")
        header = output[cursor:line_end].split(b" ")
        if len(header) != 3:
            raise _RepoStateError(
                f"git cat-file returned a malformed header for {rel!r}")
        raw_oid, raw_kind, raw_size = header
        try:
            size = int(raw_size)
        except ValueError as exc:
            raise _RepoStateError(
                f"git cat-file returned a malformed size for {rel!r}") from exc
        cursor = line_end + 1
        end = cursor + size
        if end >= len(output) or output[end:end + 1] != b"\n":
            raise _RepoStateError(
                f"git cat-file returned a truncated payload for {rel!r}")
        if raw_oid.decode("ascii") != expected_oid or raw_kind != b"blob":
            raise _RepoStateError(
                f"git cat-file returned the wrong object for {rel!r}")
        payloads[rel] = output[cursor:end]
        cursor = end + 1
    if cursor != len(output):
        raise _RepoStateError("git cat-file returned unexpected trailing bytes")
    return payloads


def _materialize_committed_checkout(repo_root: Path, head: str) -> None:
    """Populate a ``--no-checkout`` worktree directly from committed blobs.

    Normal checkout invokes configured smudge filters before any verifier can
    inspect their result. Reading objects with ``cat-file`` avoids executing
    those repository-local programs at all.
    """
    entries = _committed_blobs(repo_root, head)
    payloads = _read_committed_payloads(repo_root, entries)
    root = repo_root.resolve(strict=True)
    for rel, (mode, _oid) in entries.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        data = payloads[rel]
        if mode == "120000":
            target = Path(os.fsdecode(data))
            if target.is_absolute():
                raise _RepoStateError(
                    f"committed symlink {rel!r} has an absolute target")
            resolved = (path.parent / target).resolve(strict=False)
            if resolved != root and root not in resolved.parents:
                raise _RepoStateError(
                    f"committed symlink {rel!r} resolves outside the detached "
                    "checkout")
            os.symlink(os.fsdecode(data), path)
        elif mode in {"100644", "100755"}:
            path.write_bytes(data)
            path.chmod(0o755 if mode == "100755" else 0o644)
        else:
            raise _RepoStateError(
                f"committed path {rel!r} has unsupported mode {mode!r}")


def _populate_committed_index(repo_root: Path, head: str) -> None:
    """Make Git's status baseline describe *head* without checking files out.

    ``worktree add --no-checkout`` creates an empty per-worktree index. The
    exact-byte materializer writes the committed files itself, so leaving that
    index empty makes the child preflight report every path as deleted. A plain
    ``read-tree`` updates only the index; it does not run checkout filters or
    replace the blob materialization and verification below.
    """
    proc = _git_at(repo_root, "read-tree", "--reset", head)
    if proc.returncode != 0:
        raise _RepoStateError(
            "could not populate detached checkout index "
            f"({(proc.stderr or '').strip() or 'git read-tree failed'})")


def _verify_committed_index(
        repo_root: Path,
        expected: Mapping[str, tuple[str, str]]) -> None:
    """Require every stage-0 index entry to match the committed tree.

    Windows does not expose Git's executable flag through ``stat``. The index
    remains a useful mode source there, provided its complete path/mode/object
    set is compared and any unmerged or ambiguous entry refuses.
    """
    proc = _git_bytes_at(repo_root, "ls-files", "--stage", "-z")
    if proc.returncode != 0:
        detail = os.fsdecode(proc.stderr or b"").strip()
        raise _RepoStateError(
            "could not enumerate detached checkout index "
            f"({detail or 'git ls-files failed'})")
    entries: dict[str, tuple[str, str]] = {}
    for record in (proc.stdout or b"").split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            raw_mode, raw_oid, raw_stage = metadata.split(b" ", 2)
            mode = raw_mode.decode("ascii")
            oid = raw_oid.decode("ascii")
            stage = raw_stage.decode("ascii")
        except (ValueError, UnicodeDecodeError) as exc:
            raise _RepoStateError(
                "git ls-files returned a malformed stage entry") from exc
        rel = os.fsdecode(raw_path)
        if not rel or stage != "0":
            raise _RepoStateError(
                f"detached checkout index has a non-stage-0 entry for {rel!r}")
        if rel in entries:
            raise _RepoStateError(
                f"detached checkout index repeats path {rel!r}")
        entries[rel] = (mode, oid)
    if entries != dict(expected):
        missing = sorted(set(expected) - set(entries))[:5]
        extra = sorted(set(entries) - set(expected))[:5]
        changed = sorted(path for path in set(entries) & set(expected)
                         if entries[path] != expected[path])[:5]
        raise _RepoStateError(
            "detached checkout index does not match the committed tree "
            f"(missing={missing}, extra={extra}, changed={changed})")


def _verify_committed_checkout(repo_root: Path, head: str) -> None:
    """Require the checkout to contain exactly *head*'s blob bytes.

    ``git worktree add`` can apply configured checkout filters, and ordinary
    status honors ignore rules. Neither is an exact-byte oracle. This verifier
    compares every leaf to the object id in ``ls-tree`` using Git's blob hash,
    rejects extra ignored leaves, and refuses symlinks that resolve outside the
    detached tree.
    """
    try:
        root = repo_root.resolve(strict=True)
    except OSError as exc:
        raise _RepoStateError(
            f"detached checkout root cannot be resolved ({exc})") from None
    expected = _committed_blobs(root, head)
    if os.name == "nt":
        _verify_committed_index(root, expected)
    actual = _checkout_leaf_paths(root)
    expected_paths = set(expected)
    if actual != expected_paths:
        missing = sorted(expected_paths - actual)[:5]
        extra = sorted(actual - expected_paths)[:5]
        raise _RepoStateError(
            "detached checkout does not contain exactly the committed paths "
            f"(missing={missing}, extra={extra})")

    for rel, (mode, oid) in expected.items():
        path = root / rel
        try:
            metadata = path.lstat()
            if mode == "120000":
                if not stat.S_ISLNK(metadata.st_mode):
                    raise _RepoStateError(
                        f"committed symlink {rel!r} is not a symlink on disk")
                data = os.fsencode(os.readlink(path))
                resolved = path.resolve(strict=True)
                if resolved != root and root not in resolved.parents:
                    raise _RepoStateError(
                        f"committed symlink {rel!r} resolves outside the "
                        "detached checkout")
            elif mode in {"100644", "100755"}:
                if not stat.S_ISREG(metadata.st_mode):
                    raise _RepoStateError(
                        f"committed file {rel!r} is not a regular file on disk")
                if os.name != "nt":
                    is_executable = bool(metadata.st_mode & stat.S_IXUSR)
                    if is_executable != (mode == "100755"):
                        raise _RepoStateError(
                            f"committed file {rel!r} has the wrong executable mode")
                data = path.read_bytes()
            else:
                raise _RepoStateError(
                    f"committed path {rel!r} has unsupported mode {mode!r}")
        except _RepoStateError:
            raise
        except (OSError, RuntimeError) as exc:
            raise _RepoStateError(
                f"could not read detached checkout path {rel!r} ({exc})") from None
        if _blob_oid_at(repo_root, data) != oid:
            raise _RepoStateError(
                f"detached checkout path {rel!r} does not match commit {head}")


class _ObjectIntegrityError(_RepoStateError):
    """Structural object corruption. Distinct from a scanner finding.

    `fsck` proves structural object integrity -- **not** authorization, not
    safety, not signature validity. The type keeps those claims apart in the
    result labels.
    """


def _fsck_from_sterile_context(repo_root: Path) -> None:
    """Validate the object graph from a context the candidate cannot configure.

    **Why not just run `fsck --strict` in the candidate repository.** Measured
    on git 2.53.0 against a reachable commit written with
    `hash-object -t commit -w --stdin --literally` and no `author` line:

      * default `--strict` refuses it (exit 1) -- correct;
      * repo-local `fsck.missingAuthor=ignore` makes it pass (exit 0);
      * repo-local `fsck.skipList=<file naming the oid>` also makes it pass.

    A command-line pin defeats the first and **not the second**: `fsck.skipList`
    is multi-valued, so `-c fsck.skipList=/dev/null` *accumulates* with the
    candidate's entry rather than replacing it. No enumeration of `fsck.*`
    closes this -- the family grows, and one member is immune to the technique.

    So the graph is checked from a **sterile bare clone**, which inherits the
    objects and none of the candidate's `.git/config`. Measured: the same
    malformed object refuses there with `missingAuthor`, exit 1. The clone is
    `--local`, so objects are hardlinked rather than copied.
    """
    with tempfile.TemporaryDirectory(prefix="cairn-fsck-") as parent:
        sterile = Path(parent) / "sterile.git"
        clone = _git_at(repo_root, "clone", "--bare", "--local", "--quiet",
                        str(repo_root), str(sterile))
        if clone.returncode != 0:
            raise _ObjectIntegrityError(
                f"could not build a sterile context for object validation "
                f"({(clone.stderr or '').strip()})")
        proc = _git_at(sterile, "fsck", "--strict", "--no-dangling")
        if proc.returncode != 0:
            raise _ObjectIntegrityError(
                "git fsck --strict reported object corruption in the "
                "repository being released -- FAIL CLOSED. This is a "
                "structural object-integrity failure, not a scanner finding "
                "and not a signature verdict.\n"
                f"{(proc.stdout or '').strip()}\n{(proc.stderr or '').strip()}")


@contextmanager
def _detached_checkout(head: str, *, parent_repo: Path | None = None) -> Iterator[Path]:
    """Yield an exact-byte detached worktree from the selected repository."""
    if parent_repo is None:
        parent_repo = CAIRN_ROOT
    # Before materialising anything executable from this repository, prove its
    # object graph is structurally sound -- from a context the candidate cannot
    # configure away. Fails closed.
    _fsck_from_sterile_context(parent_repo)
    with tempfile.TemporaryDirectory(prefix="cairn-release-") as parent:
        checkout = Path(parent) / "checkout"
        added = False
        try:
            proc = _git_at(parent_repo, "worktree", "add", "--detach", "--no-checkout",
                           str(checkout), head)
            if proc.returncode != 0:
                raise _RepoStateError(
                    "could not create detached release checkout "
                    f"({(proc.stderr or '').strip() or 'git worktree add failed'})")
            added = True
            _populate_committed_index(checkout, head)
            _materialize_committed_checkout(checkout, head)
            _verify_committed_checkout(checkout, head)
            yield checkout
            _verify_committed_checkout(checkout, head)
        finally:
            if added:
                proc = _git_at(parent_repo, "worktree", "remove", "--force", str(checkout))
                if proc.returncode != 0:
                    raise _RepoStateError(
                        "could not remove detached release checkout "
                        f"({(proc.stderr or '').strip() or 'git worktree remove failed'})")


# The Python members of the ceremony's authority closure
# (``_gate_preflight.declared_authority_closure()``), repo-relative. Spelled out
# here because this module cannot import test-tree code; kept honest by a test.
_CEREMONY_CLOSURE_PY: tuple[str, ...] = (
    "tests/_gate_preflight.py",
    "tests/_gate_manifest.py",
    "tests/_gate_reanchor.py",
    "tests/_gate_transition.py",
    "tests/_oracle_activation.py",
    "tests/_oracle.py",
    "tests/_oracle_trust.py",
)


def scan_targets() -> list[str]:
    """The executable surface to scan, derived from Cairn's source of truth:
    every **verbatim** (byte-for-byte, un-substituted) ``.py`` in the
    published install manifest -- the artifacts an adopter runs as code --
    plus Cairn's own development and release executables and the whole
    scaffold engine package, as explicit files. A newly shipped script is
    covered automatically through the install manifest.

    The registry loop below (``_MODULE_MAPPINGS``) is strictly redundant once
    the manifest union lands -- every verbatim ``.py`` it names is also a
    verbatim ``.py`` in the published manifest, and that subset relation, not
    any count, is what is durable -- and is **retained on purpose**: it is a
    ``set.add`` call into the same accumulator, so "this change cannot shrink
    the scanned surface" is true by inspection rather than by measurement. It
    is defence in depth, not a second guard: what actually catches a shipped
    ``.py`` falling out of this set is the on-disk oracle in
    ``tests/test_security_lint.py``, whose input this function never
    reads."""
    targets: set[str] = set()
    for specs in _MODULE_MAPPINGS.values():
        for spec in specs:
            if spec.verbatim and spec.src.endswith(".py"):
                targets.add(f"templates/modules/{spec.src}")
    # Cairn's executable sources and the installed copies that used to live
    # under scripts/. Include the latter at either known path during migration.
    for sub in ("install", "release"):
        targets.update(
            str(p.relative_to(CAIRN_ROOT))
            for p in (CAIRN_ROOT / sub).glob("*.py")
        )
    targets.update(str(p.relative_to(CAIRN_ROOT)) for p in (CAIRN_ROOT / "tests").glob("*.py")
                   if not p.name.startswith(("test_", "_", "conftest")))
    for _, _, old_dst, _, _, new_dst in LAYOUT_INSTALLS:
        if old_dst.startswith("scripts/") and old_dst.count("/") == 1 and old_dst.endswith(".py"):
            targets.update(path for path in (old_dst, new_dst) if (CAIRN_ROOT / path).is_file())
    # The scaffold engine package (post-split): RECURSE it -- every module
    # under install/_scaffold/ is
    # privileged implementation, equal in authority to the old monolith, so the
    # non-recursive install/*.py glob above would leave the engine's guts
    # unscanned after the split. tests/ (intentional attack fixtures)
    # stays excluded. A no-op until the package exists (Stage 0B), so the Bandit
    # surface is unchanged today.
    engine_pkg = CAIRN_ROOT / "install" / "_scaffold"
    if engine_pkg.is_dir():
        targets.update(
            str(p.relative_to(CAIRN_ROOT))
            for p in engine_pkg.rglob("*.py")
        )
    # The Python files that decide what a re-anchor ceremony blesses and runs.
    # They live under tests/, which the globs above leave out on
    # purpose (attack fixtures), so they are named one by one; a test compares
    # this tuple with the checker's own declared closure so a new member
    # cannot go unscanned.
    targets.update(_CEREMONY_CLOSURE_PY)
    # Every verbatim .py the scaffold ACTUALLY installs, from the published
    # install manifest -- the same enumeration adopters depend on through
    # `scaffold.py --manifest`. Two facts here are load-bearing:
    #   * `modules=None` means the FULL published catalog. A module subset
    #     would silently shrink the scanned surface, and nothing downstream
    #     would say so.
    #   * This is a UNION WITH the registry loop above, never a
    #     replacement for them. That framing is what makes "coverage cannot
    #     shrink" checkable by inspection instead of by measurement.
    # It closes a real, 63-day-old miss: `_SKILLS_MAPPINGS` ships the two
    # session-lifecycle tools unconditionally to every adoption and no loop
    # above reaches them (scan-coverage plan, Chunk B / proposal items 1-2).
    for src, _dst, verbatim in install_manifest(modules=None):
        if verbatim and src.endswith(".py"):
            targets.add(f"templates/{src}")
    return sorted(targets)


def _rel(filename: str) -> str:
    try:
        return Path(filename).resolve().relative_to(CAIRN_ROOT).as_posix()
    except ValueError:
        return filename


def is_blocking(finding: Mapping[str, object]) -> bool:
    """**The** blocking predicate over one Bandit finding.

    Exported and called by every consumer -- the release command's suppression
    filter and its allowlist-liveness set here, and (intended) the dev gate in
    ``tests/test_security_lint.py``, which today re-spells severity
    through its own ``_SEVERITY_RANK`` table. The single-sourcing comment on
    that import has always been true of the *data* (``ALLOWLIST``,
    ``scan_targets``) and silent about the *predicate*: two spellings of "is
    this finding blocking" that agree only by having been copied.
    """
    return finding.get("issue_severity") in _BLOCKING_SEVERITIES


def finding_key(finding: Mapping[str, object]) -> tuple[str, str]:
    """The allowlist key of one finding -- the other half of the rule that was
    spelled twice. Normalization lives here, once."""
    return (_rel(str(finding["filename"])), str(finding["test_id"]))


def validate_report(report: object, returncode: int) -> str | None:
    """Semantic validation of a Bandit report. ``None`` means usable.

    "Successfully parsed" must mean a *validated* report, not merely valid
    JSON. Measured against this module's own bytes at ``745c927``, five
    malformations all produced release evidence: ``{}`` with rc 0,
    ``{"errors": [], "results": []}`` with **rc 1**, and
    ``{"errors": [], "results": {}}`` with rc 0 each printed
    ``Bandit clean over 78 shipped file(s)`` and returned 0; ``[]`` and
    ``null`` raised ``AttributeError`` -- non-zero, but a traceback rather than
    a security message. A scanner failure or an incompatible Bandit could
    therefore become release ``PASS``.

    This is semantic checking of a shape the scanner already produces, not a
    schema dependency: nothing is imported to do it.
    """
    if not isinstance(report, dict):
        return (f"top-level JSON is {type(report).__name__}, not an object")
    for field in ("errors", "results"):
        if field not in report:
            return f"required key {field!r} is absent"
        if not isinstance(report[field], list):
            return (f"{field!r} is {type(report[field]).__name__}, not a list "
                    f"-- a mapping-valued {field!r} reads as 'nothing found'")
    for i, error in enumerate(report["errors"]):
        if not isinstance(error, dict):
            return f"errors[{i}] is {type(error).__name__}, not an object"
        missing = [k for k in _REQUIRED_ERROR_FIELDS if k not in error]
        if missing:
            return f"errors[{i}] is missing required field(s) {missing}"
        for field in _REQUIRED_ERROR_FIELDS:
            if not isinstance(error[field], str):
                return f"errors[{i}].{field} is not a string"
    for i, finding in enumerate(report["results"]):
        if not isinstance(finding, dict):
            return f"results[{i}] is {type(finding).__name__}, not an object"
        missing = [k for k in _REQUIRED_FINDING_FIELDS if k not in finding]
        if missing:
            return f"results[{i}] is missing required field(s) {missing}"
        for field in ("filename", "test_id", "issue_severity", "issue_text"):
            if not isinstance(finding[field], str):
                return f"results[{i}].{field} is not a string"
        if (not isinstance(finding["line_number"], int)
                or isinstance(finding["line_number"], bool)):
            return f"results[{i}].line_number is not an integer"
        severity = finding["issue_severity"]
        if severity not in _KNOWN_SEVERITIES:
            return (f"results[{i}] has issue_severity {severity!r}, outside "
                    f"the known set {sorted(_KNOWN_SEVERITIES)} -- "
                    f"unclassifiable evidence, not a low-severity finding")
    # An exit code that contradicts its own report. Bandit exits 1 when it has
    # findings to report, so 1 with nothing in `results` AND nothing in
    # `errors` means the exit code and the body disagree, and one of them is
    # wrong. Only this direction is refused: the converse (rc 0 with findings
    # present) is legitimate under Bandit's severity-threshold flags, and
    # refusing it would be a false refusal rather than a closed hole.
    if returncode == 1 and not report["results"] and not report["errors"]:
        return ("bandit exited 1 -- which it does when it has findings to "
                "report -- with zero results and zero errors; the exit code "
                "and the report contradict each other")
    return None


def run_bandit() -> int:
    """Run Bandit over the derived surface; fail closed on absence/error."""
    # `install_manifest` REFUSES a malformed mapping (duplicate destinations)
    # by raising ValueError. This wrapper is legibility, not new safety:
    # main() wraps run_bandit() in no handler, so an uncaught ValueError
    # already exits non-zero -- it buys a security message instead of a
    # traceback (scan-coverage plan, Chunk B / proposal item 2).
    try:
        scanned = scan_targets()
    except ValueError as exc:
        print("security_check: cannot enumerate the shipped surface "
              f"({exc}) -- FAIL CLOSED.", file=sys.stderr)
        return 1
    targets = [str(CAIRN_ROOT / t) for t in scanned]
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "bandit", "-q", "-f", "json", *targets],
            capture_output=True, text=True, check=False, cwd=str(CAIRN_ROOT),
        )
    except OSError as exc:
        print(f"security_check: cannot run bandit ({exc}) -- FAIL CLOSED.",
              file=sys.stderr)
        return 1
    if (proc.returncode == 127
            or "No module named bandit" in proc.stderr
            or "No module named 'bandit'" in proc.stderr):
        print("security_check: bandit is NOT installed -- FAIL CLOSED. A "
              "release security gate must not be skippable; install bandit "
              "(pip install bandit) and re-run.", file=sys.stderr)
        return 1
    if proc.returncode not in (0, 1):
        print(f"security_check: bandit error (rc={proc.returncode}) -- fail "
              f"closed.\n{proc.stderr[:800]}", file=sys.stderr)
        return 1
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print("security_check: bandit output was not JSON -- fail closed.",
              file=sys.stderr)
        return 1
    # Validation comes BEFORE the errors check, liveness, and suppression --
    # every rule below reads fields this establishes are present and
    # classifiable. A report the command cannot validate is not a report that
    # came back clean.
    problem = validate_report(report, proc.returncode)
    if problem is not None:
        print(f"security_check: bandit output is not a usable report "
              f"({problem}) -- FAIL CLOSED. A report the command cannot "
              f"validate is not a report that came back clean.",
              file=sys.stderr)
        return 1
    # A file Bandit could not READ is not a file Bandit found clean. Bandit
    # records such a failure (missing file, unparseable source) in the JSON
    # `errors` array, scans the rest, and exits 0 -- so the rc branch above
    # never fires and the run reports clean over a file it never opened.
    # Fail closed here, BEFORE allowlist filtering, matching the scanner-error
    # posture above.
    errors = report.get("errors") or []
    if errors:
        detail = "\n".join(
            f"  {_rel(str(e.get('filename', '?')))}: {e.get('reason', '?')}"
            for e in errors
        )
        print("security_check: bandit could not scan "
              f"{len(errors)} requested file(s) -- fail closed. A file the "
              "scanner never opened is not a file it found clean.\n" + detail,
              file=sys.stderr)
        return 1
    # `results` is a list of field-complete findings with classifiable
    # severities: validate_report() established that above, so `.get(... ) or
    # []` defaulting -- which is what let a mapping-valued `results` read as
    # "nothing found" -- is gone.
    results = report["results"]
    blocking = [
        f"  [{f['test_id']} {f['issue_severity']}] {_rel(f['filename'])}:"
        f"{f['line_number']}  {f['issue_text']}"
        for f in results
        if is_blocking(f) and finding_key(f) not in ALLOWLIST
    ]
    # Allowlist liveness. Derived from the **successfully parsed** report only
    # -- every earlier fail-closed branch has already returned, so a partial or
    # unreadable scan can never retire an entry by making its finding "absent".
    #
    # The predicate and the key rule are the SAME functions suppression uses one
    # line above, not a second spelling of them: a liveness set that could
    # disagree with the filter it is meant to describe is how an entry gets
    # called live while suppressing nothing. Blocking severity only, because
    # that is the sole thing the allowlist filters.
    observed = {finding_key(f) for f in results if is_blocking(f)}
    stale = sorted(key for key in ALLOWLIST if key not in observed)
    rc = 0
    if blocking:
        print("security_check: unallowlisted MEDIUM+ Bandit finding(s):\n"
              + "\n".join(blocking), file=sys.stderr)
        rc = 1
    if stale:
        print("security_check: ALLOWLIST entr(ies) the scan does not report at "
              "MEDIUM+ -- fail closed. A suppression that suppresses nothing is "
              "a standing permission for a future finding, granted by a "
              "rationale written about code that has since changed. Delete "
              "it:\n"
              + "\n".join(f"  {path}  {test_id}" for path, test_id in stale),
              file=sys.stderr)
        rc = 1
    if rc:
        return rc
    print(f"security_check: Bandit clean over {len(targets)} shipped file(s) "
          f"({len(ALLOWLIST)} live allowlist entr(ies)).")
    return 0


def run_check_cairn() -> int:
    """Run the Markdown self-check (link / claim / content integrity)."""
    script = CAIRN_ROOT / "tests" / "check_cairn.py"
    if not script.is_file():
        print(f"security_check: {script} missing -- fail closed.",
              file=sys.stderr)
        return 1
    try:
        return subprocess.run([sys.executable, str(script)],
                              cwd=str(CAIRN_ROOT), check=False).returncode
    except OSError as exc:
        print(f"security_check: cannot run check_cairn ({exc}) -- fail "
              "closed.", file=sys.stderr)
        return 1


def _release_child_env() -> dict[str, str]:
    """The child environment for phases 3 and 4.

    Built from a **copy** of ``os.environ`` and passed **explicitly** to both
    subprocesses. Three properties, each load-bearing:

    * a *copy*, so setting the token cannot leak into this process or into a
      sibling phase that must not see it;
    * *explicit*, so the token's arrival does not depend on inheritance being
      left undisturbed by a future edit;
    * a *superset* of the operator's environment, because the quality gate's
      order-independence sub-gate launches pytest as a **grandchild** with no
      ``env=`` of its own (``tests/quality_gate.py``, argv bound at the
      ``cmd`` assignment, ``subprocess.run`` immediately below). It reaches
      that grandchild by inheritance alone -- which is why the decisive
      regression in ``tests/test_security_check.py`` drives the real
      child path rather than reading this dict back.
    """
    env = dict(os.environ)
    env[RELEASE_GATE_ENV] = RELEASE_GATE_VALUE
    # The detached checkout is exact before phases and must stay exact between
    # them. Pytest's cache provider and Python bytecode are execution byproducts,
    # not release inputs; suppress them instead of teaching the verifier to
    # tolerate uncommitted files.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTEST_ADDOPTS"] = "-p no:cacheprovider"
    # The summary belongs to the committed runner, not its pytest children.
    # The five report-context values remain so the quality-gate grandchild can
    # write its independently named seed-0 report.
    env.pop(_NATIVE_RUN_SUMMARY_ENV, None)
    return env


def run_suite() -> int:
    """Phase 3: the shipped-only engine selection, in release mode.

    Output is not captured: the operator records this run in the release
    notes, so the evidence has to be visible while it happens.
    """
    tests = CAIRN_ROOT / "tests"
    if not tests.is_dir():
        print(f"security_check: {tests} is missing -- fail closed. A release "
              f"cannot be cut on a suite that is not there.", file=sys.stderr)
        return 1
    print(f"security_check: running the shipped-only selection in release mode "
          f"({RELEASE_GATE_ENV}={RELEASE_GATE_VALUE}) -- only fixed opposite-"
          "platform setup skips are eligible; all other incomplete outcomes refuse.")
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "tests", "-q"],
            cwd=str(CAIRN_ROOT), env=_release_child_env(), check=False,
        )
    except OSError as exc:
        print(f"security_check: cannot run the suite ({exc}) -- fail closed.",
              file=sys.stderr)
        return 1
    # Every non-zero pytest exit is a refusal, including the ones that are not
    # test failures: 4 (usage error) and 5 (no tests collected) are absent
    # evidence, and absent evidence must not read as a clean gate.
    if proc.returncode != 0:
        print(f"security_check: the release-mode suite exited "
              f"{proc.returncode} -- fail closed.", file=sys.stderr)
        return 1
    try:
        if _native_context_from_environment() is not None:
            _NATIVE_RUN_EVIDENCE["default"] = _consume_suite_report("default")
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        print(f"security_check: default-order evidence refused ({exc}) -- "
              "fail closed.", file=sys.stderr)
        return 1
    return 0


def run_quality_gate() -> int:
    """Phase 4: ``tests/quality_gate.py`` -- in no release checklist before
    this plan, though it owns the vendor-neutrality gate that protects every
    adopter-facing template."""
    script = CAIRN_ROOT / "tests" / "quality_gate.py"
    if not script.is_file():
        print(f"security_check: {script} missing -- fail closed.",
              file=sys.stderr)
        return 1
    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(CAIRN_ROOT), env=_release_child_env(), check=False,
        )
    except OSError as exc:
        print(f"security_check: cannot run the quality gate ({exc}) -- fail "
              f"closed.", file=sys.stderr)
        return 1
    if proc.returncode != 0:
        print(f"security_check: quality_gate exited {proc.returncode} -- fail "
              f"closed.", file=sys.stderr)
        return 1
    try:
        if _native_context_from_environment() is not None:
            _NATIVE_RUN_EVIDENCE["seed-0"] = _consume_suite_report("seed-0")
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        print(f"security_check: seed-0 evidence refused ({exc}) -- "
              "fail closed.", file=sys.stderr)
        return 1
    return 0


def _phases() -> tuple[tuple[str, Callable[[], int]], ...]:
    """The phases attempted after the preflight passes, in order. Every one is
    attempted even after an earlier failure, so a single run yields a complete
    repair list rather than the first thing that broke.

    A **function**, not a module constant, on purpose: a module-level tuple
    binds each runner *by value at import*, so repointing
    ``security_check.run_suite`` -- the ordinary way to isolate one phase --
    would be a silent no-op. That exact trap is documented against
    ``_SKILLS_MAPPINGS`` in ``tests/test_security_lint.py``; the
    globals are resolved here at call time instead.
    """
    return (
        ("bandit", run_bandit),
        ("check_cairn", run_check_cairn),
        ("release-mode suite", run_suite),
        ("quality_gate", run_quality_gate),
    )


def _run_bound_phases(head: str) -> int:
    """Run every checking phase and the checkout postflight.

    Ordinary phase exceptions become labelled failures so later phases still
    produce a repair list. ``KeyboardInterrupt`` and ``SystemExit`` are not
    ``Exception`` subclasses and retain their control-flow semantics.
    """
    global _PHASE_RESULTS
    _PHASE_RESULTS = {}
    rc = 0
    for label, phase in _phases():
        try:
            phase_rc = phase()
        except Exception as exc:  # noqa: BLE001 -- phase failure is evidence
            print(f"security_check: phase {label} raised "
                  f"{type(exc).__name__}: {exc} -- FAIL CLOSED; continuing "
                  "the remaining phases.", file=sys.stderr)
            rc = 1
            _PHASE_RESULTS[label] = "FAIL"
            continue
        if phase_rc != 0:
            print(f"security_check: phase {label} did not pass.",
                  file=sys.stderr)
            rc = 1
            _PHASE_RESULTS[label] = "FAIL"
        else:
            _PHASE_RESULTS[label] = "PASS"
    postflight_rc = repo_state_postflight(head)
    if postflight_rc != 0:
        rc = 1
    context = _native_context_from_environment()
    if rc == 0 and context is not None:
        try:
            if set(_NATIVE_RUN_EVIDENCE) != {"default", "seed-0"}:
                raise ValueError("both suite-order reports are required")
            default = _NATIVE_RUN_EVIDENCE["default"]
            seeded = _NATIVE_RUN_EVIDENCE["seed-0"]
            if set(default["collection_ids"]) != set(seeded["collection_ids"]):
                raise ValueError("default and seed-0 collections differ")
            excluded = _measure_excluded_tests(CAIRN_ROOT)
            local = _build_local_record(
                head, context["nonce"], sys.platform, os.name,
                list(sys.version_info[:3]), dict(_PHASE_RESULTS),
                {"default": default, "seed-0": seeded},
                excluded,
            )
            _validate_local_record(local, head)
            summary_path = os.environ.get(_NATIVE_RUN_SUMMARY_ENV)
            if not summary_path:
                raise ValueError("strict local summary path is absent")
            _write_exclusive_json(Path(summary_path), local, CAIRN_ROOT)
        except (OSError, UnicodeError, ValueError, TypeError) as exc:
            print(f"security_check: local evidence record refused ({exc}) -- "
                  "fail closed.", file=sys.stderr)
            rc = 1
    return rc


_BOUND_HEAD_ARG = "--_cairn-bound-head"
_BOUND_SUMMARY_ARG = "--_cairn-native-summary"


def _bound_main(expected_head: str, summary_path: str) -> int:
    """Internal child entry: run phases only in the detached checkout."""
    rc, head = repo_state_preflight()
    if rc or head is None:
        print("security_check: detached checkout preflight failed -- FAIL "
              "CLOSED.", file=sys.stderr)
        return 1
    if head != expected_head:
        print(f"security_check: detached checkout resolved {head}, expected "
              f"{expected_head} -- FAIL CLOSED.", file=sys.stderr)
        return 1
    try:
        context = _native_context_from_environment()
        summary = Path(summary_path)
        if context is None or context["head"] != head:
            raise ValueError("internal native evidence context is missing or stale")
        if os.environ.get(_NATIVE_RUN_SUMMARY_ENV) != str(summary):
            raise ValueError("internal native summary path was substituted")
        if (not summary.is_absolute()
                or summary.resolve().is_relative_to(CAIRN_ROOT.resolve())
                or summary.exists() or summary.is_symlink()
                or not summary.parent.is_dir()):
            raise ValueError("internal native summary must be external")
        if sys.version_info[:2] != (3, 13):
            raise ValueError("strict native run requires Python 3.13")
    except (OSError, ValueError, TypeError) as exc:
        print(f"security_check: internal native evidence refused ({exc}).",
              file=sys.stderr)
        return 1
    _NATIVE_RUN_EVIDENCE.clear()
    rc = _run_bound_phases(head)
    if rc == 0:
        print(f"security_check: committed-checkout phases clean at {head}.")
    return rc


def _load_portable_sweeps_runner(root: Path = CAIRN_ROOT):
    import sys as _sys
    runner_path = root / "dev" / "tools" / "run_portable_security_sweeps.py"
    if not runner_path.is_file():
        runner_path = Path(__file__).resolve().parent.parent / "dev" / "tools" / "run_portable_security_sweeps.py"
    spec = importlib.util.spec_from_file_location("_cairn_portable_sweeps", runner_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load portable sweeps runner at {runner_path}")
    module = importlib.util.module_from_spec(spec)
    _sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _derive_pack_path(manifest_path: Path) -> Path:
    if manifest_path.suffix != ".json":
        raise ValueError("frozen history manifest path must end with .json")
    return manifest_path.with_suffix(".pack")


def _write_exclusive_bytes(path: Path, data: bytes, root: Path) -> None:
    resolved = path.resolve()
    if (not path.is_absolute() or resolved.is_relative_to(root.resolve())
            or path.exists() or path.is_symlink() or not path.parent.is_dir()):
        raise ValueError("output path must be a new external absolute path")
    flags = (os.O_CREAT | os.O_EXCL | os.O_WRONLY
             | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0))
    fd = os.open(path, flags, 0o600)
    try:
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            if written <= 0:
                raise OSError("incomplete write")
            view = view[written:]
    finally:
        os.close(fd)


def _resolve_release_git(runner, target: Path, git_override: object = None):
    if git_override is not None:
        return git_override
    git_path = shutil.which("git")
    if not git_path:
        raise ValueError("git executable is absent")
    return runner.resolve_executable("git", target, os.path.dirname(git_path))


def _pin_source_paths(repo_root: Path) -> dict[str, str]:
    if "GIT_ALTERNATE_OBJECT_DIRECTORIES" in os.environ:
        raise ValueError("GIT_ALTERNATE_OBJECT_DIRECTORIES is forbidden")
    top = _git_at(repo_root, "rev-parse", "--path-format=absolute", "--show-toplevel")
    gdir = _git_at(repo_root, "rev-parse", "--path-format=absolute", "--git-dir")
    cdir = _git_at(repo_root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    shallow = _git_at(repo_root, "rev-parse", "--is-shallow-repository")
    if any(p.returncode != 0 for p in (top, gdir, cdir, shallow)):
        raise ValueError("could not resolve pinned repository paths")
    if shallow.stdout.strip() != "false":
        raise ValueError("shallow repository is refused")
    common_dir = Path(cdir.stdout.strip())
    if ((common_dir / "shallow").exists()
            or (common_dir / "info" / "grafts").exists()
            or (common_dir / "objects" / "info" / "alternates").exists()):
        raise ValueError("shallow, grafted, or alternate object storage is refused")
    return {
        "top_level": top.stdout.strip(),
        "git_dir": gdir.stdout.strip(),
        "common_dir": str(common_dir),
    }


def _parse_worktree_porcelain_z(raw: bytes, common_dir: Path) -> list[dict[str, str]]:
    if not raw:
        raise ValueError("empty worktree inventory")
    stanzas = raw.split(b"\0\0")
    entries: list[dict[str, str]] = []
    seen_main = False
    for stanza in stanzas:
        if not stanza:
            continue
        fields = stanza.split(b"\0")
        wt_path = None
        wt_head = None
        is_bare = False
        for field in fields:
            if not field:
                continue
            if field.startswith(b"worktree "):
                wt_path = field[len(b"worktree "):].decode("utf-8", "strict")
            elif field.startswith(b"HEAD "):
                wt_head = field[len(b"HEAD "):].decode("ascii", "strict")
            elif field == b"bare":
                is_bare = True
            elif field == b"prunable" or field.startswith(b"prunable "):
                raise ValueError("prunable worktree is refused")
        if not wt_path or is_bare or not wt_head or not _is_full_sha(wt_head):
            raise ValueError("malformed or bare worktree entry in source inventory")
        wt_dir = Path(wt_path)
        if not wt_dir.is_dir():
            raise ValueError(f"inaccessible worktree directory: {wt_path}")
        gdir_proc = _git_at(wt_dir, "rev-parse", "--path-format=absolute", "--git-dir")
        cdir_proc = _git_at(wt_dir, "rev-parse", "--path-format=absolute", "--git-common-dir")
        if gdir_proc.returncode != 0 or cdir_proc.returncode != 0:
            raise ValueError(f"worktree git metadata check failed: {wt_path}")
        wt_cdir = Path(cdir_proc.stdout.strip())
        if wt_cdir.resolve() != common_dir.resolve():
            raise ValueError(f"worktree common directory mismatch: {wt_path}")
        wt_gdir = Path(gdir_proc.stdout.strip())
        if wt_gdir.resolve() == common_dir.resolve():
            if seen_main:
                raise ValueError("duplicate main worktree in inventory")
            seen_main = True
            scope = "main"
        else:
            worktrees_parent = (common_dir / "worktrees").resolve()
            if wt_gdir.resolve().parent != worktrees_parent:
                raise ValueError(f"unexpected linked worktree admin dir: {wt_gdir}")
            scope = f"worktrees/{wt_gdir.name}"
        entries.append({"scope": scope, "path": wt_path, "head": wt_head})
    if not seen_main:
        raise ValueError("main worktree missing from inventory")
    return sorted(entries, key=lambda item: item["scope"])


def _parse_for_each_ref_z(raw: bytes, scope: str) -> list[dict[str, str]]:
    if not raw:
        return []
    rows: list[dict[str, str]] = []
    for raw_entry in raw.split(b"\0"):
        entry = raw_entry.removeprefix(b"\n")
        if not entry:
            continue
        first_sp = entry.find(b" ")
        second_sp = entry.find(b" ", first_sp + 1) if first_sp > 0 else -1
        if first_sp <= 0 or second_sp <= first_sp + 1:
            raise ValueError("malformed for-each-ref entry")
        oid = entry[:first_sp].decode("ascii", "strict")
        objtype = entry[first_sp + 1:second_sp].decode("ascii", "strict")
        ref_bytes = entry[second_sp + 1:]
        if not _is_full_sha(oid) or objtype not in {"commit", "tag", "tree", "blob"}:
            raise ValueError("invalid object id or type in ref inventory")
        rows.append({
            "scope": scope,
            "ref_b64": base64.b64encode(ref_bytes).decode("ascii"),
            "oid": oid,
            "object_type": objtype,
        })
    return rows


def _collect_source_inventory(runner, session, repo_root: Path, head: str) -> dict:
    pinned = _pin_source_paths(repo_root)
    common_dir = Path(pinned["common_dir"])
    wt_res = runner._release_history_git(session, "WORKTREES")
    worktrees = _parse_worktree_porcelain_z(wt_res.stdout, common_dir)
    shared_res = runner._release_history_git(session, "FOR_EACH_REF_SHARED")
    refs = _parse_for_each_ref_z(shared_res.stdout, "shared")
    heads: list[dict] = []
    for wt in worktrees:
        wt_path = Path(wt["path"])
        priv_res = runner._release_history_git(
            session, "FOR_EACH_REF_PRIVATE", repo_path=wt_path,
        )
        refs.extend(_parse_for_each_ref_z(priv_res.stdout, wt["scope"]))
        sym_res = runner._release_history_git(
            session, "HEAD_SYMBOLIC", repo_path=wt_path,
        )
        if sym_res.returncode == 0:
            symbolic = sym_res.stdout.decode("utf-8", "strict").rstrip("\r\n")
            peel = _git_at(wt_path, "rev-parse", "--verify", "--quiet", "HEAD^{commit}")
            unborn = peel.returncode != 0
            resolved_oid = None if unborn else peel.stdout.strip()
            if not unborn and resolved_oid != wt["head"]:
                raise ValueError(f"HEAD mismatch in {wt['scope']}")
            heads.append({
                "scope": wt["scope"],
                "symbolic": symbolic,
                "oid": resolved_oid,
                "unborn": unborn,
            })
        else:
            peel = _git_at(wt_path, "rev-parse", "--verify", "--quiet", "HEAD^{commit}")
            if peel.returncode != 0 or peel.stdout.strip() != wt["head"]:
                raise ValueError(f"detached HEAD verification failed in {wt['scope']}")
            heads.append({
                "scope": wt["scope"],
                "symbolic": None,
                "oid": wt["head"],
                "unborn": False,
            })
    refs_sorted = sorted(refs, key=lambda r: (r["scope"], r["ref_b64"], r["oid"]))
    heads_sorted = sorted(heads, key=lambda h: h["scope"])
    raw_roots = sorted(
        {head}
        | {row["oid"] for row in refs_sorted}
        | {row["oid"] for row in heads_sorted if row["oid"] is not None}
    )
    peeled_roots: set[str] = set()
    for oid in raw_roots:
        peel = _git_at(repo_root, "rev-parse", "--verify", "--quiet", f"{oid}^{{commit}}")
        if peel.returncode != 0 or not _is_full_sha(peel.stdout.strip()):
            raise ValueError(f"root {oid} cannot peel to a commit")
        peeled_roots.add(peel.stdout.strip())
    return {
        "candidate": head,
        "object_format": _repository_object_format(repo_root),
        "source": pinned,
        "refs": refs_sorted,
        "heads": heads_sorted,
        "roots": sorted(peeled_roots),
    }


def _freeze_history(manifest_path: Path) -> int:
    if sys.version_info[:2] != (3, 13):
        print("security_check: --freeze-history requires Python 3.13.", file=sys.stderr)
        return 1
    try:
        if not manifest_path.is_absolute():
            raise ValueError("manifest path must be absolute")
        if manifest_path.resolve().is_relative_to(CAIRN_ROOT.resolve()):
            raise ValueError("manifest must be outside the checkout")
        pack_path = _derive_pack_path(manifest_path)
        for p in (manifest_path, pack_path):
            if p.exists() or p.is_symlink():
                raise ValueError(f"output path already exists: {p}")
            if not p.parent.is_dir():
                raise ValueError(f"output parent directory is absent: {p.parent}")
    except (OSError, ValueError, TypeError) as exc:
        print(f"security_check: --freeze-history refused ({exc}).", file=sys.stderr)
        return 1
    rc, head = repo_state_preflight()
    if rc or head is None:
        return rc or 1
    try:
        runner = _load_portable_sweeps_runner(CAIRN_ROOT)
        git = _resolve_release_git(runner, CAIRN_ROOT)
        ws_cm = runner._private_sweep_workspace(CAIRN_ROOT) if os.name == "nt" else tempfile.TemporaryDirectory(prefix="cairn-freeze-")
        with ws_cm as ws_dir:
            private = (runner._WindowsInvocation(CAIRN_ROOT, Path(ws_dir))
                       if os.name == "nt" else None)
            session = runner.ReleaseHistorySession(
                git=git, target=CAIRN_ROOT, source_repo=CAIRN_ROOT, private=private,
            )
            inv_before = _collect_source_inventory(runner, session, CAIRN_ROOT, head)
            rev_proc = _git_at(
                CAIRN_ROOT, "rev-list", "--objects", "--no-object-names",
                "--missing=print", *inv_before["roots"], "--",
            )
            if rev_proc.returncode != 0:
                raise ValueError("rev-list object enumeration failed")
            obj_lines = [line.strip() for line in rev_proc.stdout.splitlines() if line.strip()]
            if not obj_lines or any(line.startswith("?") or not _is_full_sha(line) for line in obj_lines):
                raise ValueError("missing or malformed object during rev-list")
            sorted_objs = sorted(set(obj_lines))
            objects_sha256 = hashlib.sha256("\n".join(sorted_objs).encode("ascii")).hexdigest()
            pack_res = runner._release_history_git(
                session, "PACK", stdin_data=("\n".join(sorted_objs) + "\n").encode("ascii"),
            )
            pack_bytes = pack_res.stdout
            pack_sha256 = hashlib.sha256(pack_bytes).hexdigest()
            inv_after = _collect_source_inventory(runner, session, CAIRN_ROOT, head)
            if inv_before != inv_after:
                raise ValueError("source repository inventory drifted during freeze")
        _write_exclusive_bytes(pack_path, pack_bytes, CAIRN_ROOT)
        manifest = {
            "schema": 1,
            "kind": "cairn-frozen-history-v1",
            "candidate": head,
            "object_format": inv_before["object_format"],
            "source": inv_before["source"],
            "pack": {"size": len(pack_bytes), "sha256": pack_sha256},
            "objects": {"count": len(sorted_objs), "objects_sha256": objects_sha256},
            "refs": inv_before["refs"],
            "heads": inv_before["heads"],
            "roots": inv_before["roots"],
        }
        _write_exclusive_json(manifest_path, manifest, CAIRN_ROOT)
    except (OSError, UnicodeError, ValueError, TypeError, Exception) as exc:
        print(f"security_check: --freeze-history failed ({exc}) -- FAIL CLOSED.", file=sys.stderr)
        return 1
    if repo_state_postflight(head) != 0:
        return 1
    print(f"security_check: frozen history written to {manifest_path} and {pack_path} at {head}.")
    return 0


def _validate_frozen_manifest(manifest_path: Path, expected_head: str) -> tuple[dict, bytes, str]:
    if not manifest_path.is_absolute() or manifest_path.resolve().is_relative_to(CAIRN_ROOT.resolve()):
        raise ValueError("manifest path must be an absolute path outside the checkout")
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise ValueError("frozen history manifest is missing or a symlink")
    pack_path = _derive_pack_path(manifest_path)
    if not pack_path.is_file() or pack_path.is_symlink():
        raise ValueError("frozen history sibling pack is missing or a symlink")
    raw_manifest = manifest_path.read_bytes()
    manifest_sha256 = hashlib.sha256(raw_manifest).hexdigest()
    doc = _load_strict_json(manifest_path)
    manifest = _exact_keys(doc, {
        "schema", "kind", "candidate", "object_format", "source",
        "pack", "objects", "refs", "heads", "roots",
    }, "frozen history manifest")
    if (type(manifest["schema"]) is not int or manifest["schema"] != 1
            or manifest["kind"] != "cairn-frozen-history-v1"
            or manifest["candidate"] != expected_head
            or manifest["object_format"] not in {"sha1", "sha256"}):
        raise ValueError("frozen history manifest header mismatch")
    pack_meta = _exact_keys(manifest["pack"], {"size", "sha256"}, "manifest pack")
    pack_bytes = pack_path.read_bytes()
    if (type(pack_meta["size"]) is not int or len(pack_bytes) != pack_meta["size"]
            or not _is_sha256(pack_meta["sha256"])
            or hashlib.sha256(pack_bytes).hexdigest() != pack_meta["sha256"]):
        raise ValueError("frozen history pack size or SHA-256 mismatch")
    obj_meta = _exact_keys(manifest["objects"], {"count", "objects_sha256"}, "manifest objects")
    if type(obj_meta["count"]) is not int or obj_meta["count"] <= 0 or not _is_sha256(obj_meta["objects_sha256"]):
        raise ValueError("frozen history object summary is malformed")
    if type(manifest["roots"]) is not list or not manifest["roots"] or any(not _is_full_sha(r) for r in manifest["roots"]):
        raise ValueError("frozen history roots are malformed")
    return manifest, pack_bytes, manifest_sha256


def _measure_store_projection(runner, session, store_repo: Path, expected_head: str) -> dict:
    ref_res = runner._release_history_git(session, "FOR_EACH_REF_SHARED", repo_path=store_repo)
    rows = _parse_for_each_ref_z(ref_res.stdout, "store")
    for row in rows:
        ref_name = base64.b64decode(row["ref_b64"]).decode("ascii", "strict")
        if not ref_name.startswith("refs/cairn-frozen/"):
            raise ValueError(f"unexpected ref in sterile store: {ref_name}")
    head_proc = _git_at(store_repo, "rev-parse", "--verify", "HEAD")
    if head_proc.returncode != 0 or head_proc.stdout.strip() != expected_head:
        raise ValueError("sterile store HEAD mismatch")
    rev_proc = _git_at(
        store_repo, "rev-list", "--objects", "--no-object-names",
        "--missing=print", "--all", "HEAD", "--",
    )
    if rev_proc.returncode != 0:
        raise ValueError("sterile store object closure check failed")
    objs = sorted({line.strip() for line in rev_proc.stdout.splitlines() if line.strip()})
    if not objs or any(line.startswith("?") or not _is_full_sha(line) for line in objs):
        raise ValueError("sterile store has missing objects")
    proj_lines = "\n".join(f"{row['oid']}:{row['ref_b64']}" for row in sorted(rows, key=lambda r: r["ref_b64"]))
    return {
        "head": expected_head,
        "projected_count": len(rows),
        "projected_sha256": hashlib.sha256(proj_lines.encode("ascii")).hexdigest(),
        "object_count": len(objs),
        "objects_sha256": hashlib.sha256("\n".join(objs).encode("ascii")).hexdigest(),
    }


def _check_store_registrations(runner, session, store_repo: Path, *, expected_checkout: Path | None) -> None:
    wt_res = runner._release_history_git(session, "WORKTREES", repo_path=store_repo)
    stanzas = [s for s in wt_res.stdout.split(b"\0\0") if s]
    expected_count = 1 if expected_checkout is None else 2
    if len(stanzas) != expected_count:
        raise ValueError(f"unexpected mirror worktree count: {len(stanzas)} != {expected_count}")
    if expected_checkout is not None:
        paths = []
        for stanza in stanzas:
            for field in stanza.split(b"\0"):
                if field.startswith(b"worktree "):
                    paths.append(Path(field[len(b"worktree "):].decode("utf-8", "strict")).resolve())
        if expected_checkout.resolve() not in paths:
            raise ValueError("detached checkout registration missing from sterile store")


def _run_in_detached_checkout(head: str, context: dict[str, str],
                              summary_path: Path) -> int:
    """Execute this checker from an exact-byte detached checkout of *head*."""
    rc, _ = _run_in_detached_frozen_checkout(head, context, summary_path)
    return rc


def _run_in_detached_frozen_checkout(
    head: str, context: dict[str, str], summary_path: Path, *,
    parent_repo: Path | None = None,
    history_sweep_cb: Callable[[Path], dict] | None = None,
) -> tuple[int, dict | None]:
    """Execute this checker from an exact-byte detached checkout of *head*."""
    history_sweep: dict | None = None
    try:
        with _detached_checkout(head, parent_repo=parent_repo) as checkout:
            checker = checkout / "release" / "security_check.py"
            env = dict(os.environ)
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            env[NATIVE_RUN_NONCE_ENV] = context["nonce"]
            env[NATIVE_RUN_HEAD_ENV] = context["head"]
            env[NATIVE_RUN_POLICY_ENV] = context["policy_id"]
            env[NATIVE_RUN_DEFAULT_REPORT_ENV] = context["default_report"]
            env[NATIVE_RUN_SEED0_REPORT_ENV] = context["seed0_report"]
            env[_NATIVE_RUN_SUMMARY_ENV] = str(summary_path)
            try:
                proc = subprocess.run(
                    [sys.executable, str(checker), _BOUND_HEAD_ARG, head,
                     _BOUND_SUMMARY_ARG, str(summary_path)],
                    cwd=str(checkout), env=env, check=False,
                )
            except OSError as exc:
                print("security_check: cannot launch the detached committed "
                      f"checker ({exc}) -- FAIL CLOSED.", file=sys.stderr)
                return 1, None
            if proc.returncode != 0:
                print("security_check: detached committed-checkout phases did "
                      f"not pass (rc={proc.returncode}).", file=sys.stderr)
                return 1, None
            if history_sweep_cb is not None:
                history_sweep = history_sweep_cb(checkout)
    except (_RepoStateError, ValueError, Exception) as exc:
        print("security_check: detached committed checkout could not be "
              f"established or preserved ({exc}) -- FAIL CLOSED.",
              file=sys.stderr)
        return 1, None
    return 0, history_sweep


def _parse_cli_flags(args: list[str]) -> tuple[str, list[Path], Path | None]:
    if not args:
        return "usage", [], None
    if len(args) == 4 and args[0] == _BOUND_HEAD_ARG and args[2] == _BOUND_SUMMARY_ARG:
        return "bound", [Path(args[1]), Path(args[3])], None
    if len(args) == 2 and args[0] == "--freeze-history":
        return "freeze", [Path(args[1])], None
    history_roots: Path | None = None
    filtered: list[str] = []
    idx = 0
    while idx < len(args):
        if args[idx] == "--history-roots":
            if idx + 1 >= len(args):
                return "usage", [], None
            history_roots = Path(args[idx + 1])
            idx += 2
        else:
            filtered.append(args[idx])
            idx += 1
    if len(filtered) == 2 and filtered[0] == "--record":
        return "record", [Path(filtered[1])], history_roots
    if len(filtered) == 3 and filtered[0] == "--join":
        return "join", [Path(filtered[1]), Path(filtered[2])], history_roots
    return "usage", [], None


def main(argv: list[str] | None = None) -> int:
    args = [] if argv is None else list(argv)
    mode, paths, history_roots = _parse_cli_flags(args)
    if mode == "bound":
        return _bound_main(str(paths[0]), str(paths[1]))
    if mode == "freeze":
        return _freeze_history(paths[0])
    if mode == "record":
        return _run_local_record(paths[0], history_roots=history_roots)
    if mode == "join":
        return _run_join(paths, history_roots=history_roots)
    print("Usage: security_check.py --freeze-history <manifest.json> | "
          "--record <external-path> [--history-roots <manifest.json>] | "
          "--join <mac-record> <windows-record> [--history-roots <manifest.json>]",
          file=sys.stderr)
    return 2


def _run_local_record(record_path: Path, *, history_roots: Path | None = None) -> int:
    if sys.version_info[:2] != (3, 13):
        print("security_check: local records require Python 3.13.",
              file=sys.stderr)
        return 1
    try:
        if not record_path.is_absolute():
            raise ValueError("local record path must be absolute")
        resolved = record_path.resolve()
        if resolved.is_relative_to(CAIRN_ROOT.resolve()):
            raise ValueError("local record must be outside the operator checkout")
        if record_path.exists() or record_path.is_symlink():
            raise ValueError("local record path already exists")
        if not record_path.parent.is_dir():
            raise ValueError("local record parent directory is absent")
        if _supported_native_host(sys.platform, os.name) not in {"nt", "posix"}:
            raise ValueError("unsupported strict native host")
    except (OSError, ValueError, TypeError) as exc:
        print(f"security_check: local record path refused ({exc}).",
              file=sys.stderr)
        return 1
    rc, head = repo_state_preflight()
    if rc or head is None:
        print("security_check: FAIL -- resolve the above before release.",
              file=sys.stderr)
        return rc or 1
    scratch = Path(tempfile.mkdtemp(prefix="cairn-native-evidence-"))
    if os.name != "nt":
        scratch.chmod(0o700)
    if scratch.resolve().is_relative_to(CAIRN_ROOT.resolve()):
        shutil.rmtree(scratch, ignore_errors=True)
        print("security_check: temporary evidence directory is inside the "
              "operator checkout -- FAIL CLOSED.", file=sys.stderr)
        return 1
    nonce = secrets.token_hex(32)
    context = {
        "nonce": nonce,
        "head": head,
        "policy_id": NATIVE_ONLY_POLICY_ID,
        "default_report": str(scratch / "default.json"),
        "seed0_report": str(scratch / "seed-0.json"),
    }
    summary = scratch / "local-summary.json"
    try:
        with ExitStack() as stack:
            parent_repo: Path | None = None
            history_sweep_cb: Callable[[Path], dict] | None = None
            if history_roots is not None:
                manifest, pack_bytes, manifest_sha256 = _validate_frozen_manifest(history_roots, head)
                runner = _load_portable_sweeps_runner(CAIRN_ROOT)
                git = _resolve_release_git(runner, CAIRN_ROOT)
                if os.name == "nt":
                    priv_root = Path(stack.enter_context(runner._private_sweep_workspace(CAIRN_ROOT)))
                    private = runner._WindowsInvocation(CAIRN_ROOT, priv_root)
                    store_root = priv_root / "frozen-store"
                else:
                    private = None
                    store_root = scratch / "frozen-store"
                src_session = runner.ReleaseHistorySession(
                    git=git, target=CAIRN_ROOT, source_repo=CAIRN_ROOT, private=private,
                )
                live = _collect_source_inventory(runner, src_session, CAIRN_ROOT, head)
                if (live["refs"] != manifest["refs"]
                        or live["heads"] != manifest["heads"]
                        or live["roots"] != manifest["roots"]):
                    raise ValueError("live source repository inventory differs from frozen manifest")
                store_repo = store_root / "mirror.git"
                if os.name == "nt":
                    with runner._win_private_create(store_root, target=CAIRN_ROOT, directory=True):
                        pass
                    with runner._win_private_create(store_repo, target=CAIRN_ROOT, directory=True):
                        pass
                else:
                    store_root.mkdir(mode=0o700)
                    store_repo.mkdir(mode=0o700)
                store_session = runner.ReleaseHistorySession(
                    git=git, target=CAIRN_ROOT, source_repo=CAIRN_ROOT,
                    store_repo=store_repo, store_root=store_root, private=private,
                )
                runner._release_history_git(store_session, "INIT")
                runner._release_history_git(store_session, "INDEX", stdin_data=pack_bytes)
                proj_chunks = []
                for idx, ref_row in enumerate(manifest["refs"]):
                    proj_chunks.append(f"update refs/cairn-frozen/{idx:06d}\0{ref_row['oid']}\0".encode("ascii"))
                if proj_chunks:
                    runner._release_history_git(store_session, "PROJECT", stdin_data=b"".join(proj_chunks))
                runner._release_history_git(store_session, "HEAD", expected_head=head)
                _check_store_registrations(runner, store_session, store_repo, expected_checkout=None)
                proj_before = _measure_store_projection(runner, store_session, store_repo, head)
                parent_repo = store_repo

                def _run_sweep_in_checkout(checkout: Path) -> dict:
                    _check_store_registrations(runner, store_session, store_repo, expected_checkout=checkout)
                    c_runner = _load_portable_sweeps_runner(checkout)
                    policy_path = checkout / "dev" / "tools" / "portable_security_policy.json"
                    runner_file = checkout / "dev" / "tools" / "run_portable_security_sweeps.py"
                    sweep_args = c_runner.build_parser().parse_args([
                        "--target", str(checkout),
                        "--policy", str(policy_path),
                        "--json",
                    ])
                    frozen_ctx = c_runner._WindowsFrozenHistory(
                        store_repo, store_root, CAIRN_ROOT, tuple(manifest["roots"]),
                    )
                    sweep_rc, sweep_summary = c_runner.run_sweep(sweep_args, frozen_history=frozen_ctx)
                    if sweep_rc != 0 or sweep_summary.get("mode") != "full":
                        raise ValueError(
                            f"portable security sweep did not pass CLEAN in full mode "
                            f"(rc={sweep_rc}, mode={sweep_summary.get('mode')})"
                        )
                    proj_after = _measure_store_projection(runner, store_session, store_repo, head)
                    if proj_before != proj_after:
                        raise ValueError("frozen history projection drifted during sweep")
                    legs_map = {
                        item["leg"]: {
                            "status": item["status"],
                            "result": item["result"],
                            "finding_count": item["finding_count"],
                        }
                        for item in sweep_summary["legs"]
                    }
                    facts = sweep_summary.get("adapter_facts", {})
                    return {
                        "manifest_sha256": manifest_sha256,
                        "pack_sha256": manifest["pack"]["sha256"],
                        "candidate": head,
                        "projection_before": proj_before,
                        "projection_after": proj_after,
                        "sweep": {
                            "result": sweep_summary["result"],
                            "mode": sweep_summary["mode"],
                            "legs": legs_map,
                            "adapter_version": str(facts.get("adapter_version_output", "")),
                            "adapter_digest": str(facts.get("adapter_sha256", "")),
                            "policy_sha256": hashlib.sha256(policy_path.read_bytes()).hexdigest(),
                            "runner_sha256": hashlib.sha256(runner_file.read_bytes()).hexdigest(),
                        },
                    }

                history_sweep_cb = _run_sweep_in_checkout

            if history_roots is None:
                rc_detached = _run_in_detached_checkout(head, context, summary)
                history_sweep = None
            else:
                rc_detached, history_sweep = _run_in_detached_frozen_checkout(
                    head, context, summary, parent_repo=parent_repo,
                    history_sweep_cb=history_sweep_cb,
                )
            if rc_detached != 0:
                return 1
            if repo_state_postflight(head) != 0:
                print("security_check: operator checkout changed during the local "
                      "run -- FAIL CLOSED.", file=sys.stderr)
                return 1
            raw_record = _load_strict_json(summary)
            if history_sweep is not None and isinstance(raw_record, dict):
                raw_record["history_sweep"] = history_sweep
            record = _validate_local_record(raw_record, head)
            if (record["platform"] != sys.platform or record["os_name"] != os.name
                    or record["python"] != list(sys.version_info[:3])):
                raise ValueError("local summary does not match this host and interpreter")
            _write_exclusive_json(record_path, record, CAIRN_ROOT)
    except (OSError, UnicodeError, ValueError, TypeError, Exception) as exc:
        print(f"security_check: local record was not created ({exc}) -- "
              "FAIL CLOSED.", file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    print(f"security_check: INCOMPLETE -- local evidence at {record_path}; "
          f"commit {head}. A Mac/Windows join is still required.")
    return 5


def _run_join(record_paths: list[Path], *, history_roots: Path | None = None) -> int:
    if sys.version_info[:2] != (3, 13):
        print("security_check: join requires Python 3.13.", file=sys.stderr)
        return 1
    try:
        _supported_native_host(sys.platform, os.name)
    except ValueError as exc:
        print(f"security_check: join refuses this platform ({exc}).",
              file=sys.stderr)
        return 1
    rc, head = repo_state_preflight()
    if rc or head is None:
        print("security_check: join preflight failed -- FAIL CLOSED.",
              file=sys.stderr)
        return rc or 1
    try:
        for path in record_paths:
            if not path.is_absolute() or path.resolve().is_relative_to(CAIRN_ROOT.resolve()):
                raise ValueError("join records must be absolute paths outside the checkout")
        excluded = _join_local_records(record_paths, head)
        manifest_sha256: str | None = None
        if history_roots is not None:
            manifest, _pack_bytes, manifest_sha256 = _validate_frozen_manifest(history_roots, head)
            runner = _load_portable_sweeps_runner(CAIRN_ROOT)
            git = _resolve_release_git(runner, CAIRN_ROOT)
            ws_cm = runner._private_sweep_workspace(CAIRN_ROOT) if os.name == "nt" else tempfile.TemporaryDirectory(prefix="cairn-join-")
            with ws_cm as ws_dir:
                private = (runner._WindowsInvocation(CAIRN_ROOT, Path(ws_dir))
                           if os.name == "nt" else None)
                src_session = runner.ReleaseHistorySession(
                    git=git, target=CAIRN_ROOT, source_repo=CAIRN_ROOT, private=private,
                )
                live = _collect_source_inventory(runner, src_session, CAIRN_ROOT, head)
            if (live["refs"] != manifest["refs"]
                    or live["heads"] != manifest["heads"]
                    or live["roots"] != manifest["roots"]):
                raise ValueError("live source repository inventory differs from frozen manifest")
            loaded = [_validate_local_record(_load_strict_json(p), head) for p in record_paths]
            for rec in loaded:
                if "history_sweep" not in rec:
                    raise ValueError(f"{rec['platform']} record omits frozen history_sweep evidence")
                hs = rec["history_sweep"]
                if (hs["manifest_sha256"] != manifest_sha256
                        or hs["pack_sha256"] != manifest["pack"]["sha256"]
                        or hs["candidate"] != head):
                    raise ValueError(f"{rec['platform']} history_sweep does not match frozen manifest")
            if (loaded[0]["history_sweep"]["sweep"]["policy_sha256"]
                    != loaded[1]["history_sweep"]["sweep"]["policy_sha256"]
                    or loaded[0]["history_sweep"]["sweep"]["runner_sha256"]
                    != loaded[1]["history_sweep"]["sweep"]["runner_sha256"]):
                raise ValueError("native records disagree on policy or runner identity")
    except (_RepoStateError, OSError, UnicodeError, ValueError, TypeError, Exception) as exc:
        print(f"security_check: join refused ({exc}) -- FAIL CLOSED.",
              file=sys.stderr)
        return 1
    if repo_state_postflight(head) != 0:
        return 1
    files = excluded["files"]
    if files:
        print(f"security_check: PASS (shipped-only) -- Mac and Windows evidence joined at {head}.")
        if history_roots is not None and manifest_sha256 is not None:
            print(f"  frozen-history manifest_sha256={manifest_sha256}")
        print("NOT CERTIFIED (shipped-only release selection): "
              f"{excluded['count']} tests in {len(files)} files were not run. "
              "They run when their own files change.")
        for path in files:
            print(f"  {path}")
    else:
        print(f"security_check: PASS -- Mac and Windows evidence joined at {head}.")
        if history_roots is not None and manifest_sha256 is not None:
            print(f"  frozen-history manifest_sha256={manifest_sha256}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
