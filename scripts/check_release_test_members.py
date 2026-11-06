#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compare a fresh pytest JUnit report with independently required test files.

This checks file presence and reported outcomes, not node completeness, command
provenance or semantic adequacy. It never runs tests or grants release authority.
"""
from __future__ import annotations

import argparse
import ast
from collections import defaultdict
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import time
import xml.etree.ElementTree as ET

MAX_REPORT_BYTES = 32 * 1024 * 1024


class CheckError(Exception):
    """The report cannot establish the required file-level result."""


def _file(root: Path, raw: str) -> str:
    if (not isinstance(raw, str) or not raw or "\\" in raw
            or any(ord(char) < 32 for char in raw)):
        raise CheckError("invalid test-file identity")
    path = Path(raw)
    if not path.is_absolute():
        parts = PurePosixPath(raw).parts
        if ".." in parts or PurePosixPath(raw).as_posix() != raw:
            raise CheckError("test-file identity is not a canonical relative path")
        path = root / path
    try:
        resolved = path.resolve(strict=True)
        relative = resolved.relative_to(root).as_posix()
    except (OSError, ValueError, RuntimeError) as exc:
        raise CheckError("test file is missing or outside the project") from exc
    if not resolved.is_file() or resolved.suffix != ".py":
        raise CheckError("test identity does not name a Python file")
    return relative


def required_files(root: Path, configured: Path | None) -> set[str]:
    if configured is not None:
        try:
            names = json.loads(configured.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise CheckError("required-file configuration is absent or malformed") from exc
        if not isinstance(names, list) or not names:
            raise CheckError("required-file configuration must be a nonempty JSON list")
    else:
        manifest = root / "bootstrap/tests/security_manifest.py"
        try:
            tree = ast.parse(manifest.read_text(encoding="utf-8"))
            definitions = [node.value for node in tree.body
                           if isinstance(node, ast.AnnAssign)
                           and isinstance(node.target, ast.Name)
                           and node.target.id == "SECURITY_FAMILY"]
            if len(definitions) != 1:
                raise ValueError("ambiguous security family")
            family = ast.literal_eval(definitions[0])
        except (OSError, SyntaxError, ValueError, TypeError) as exc:
            raise CheckError("could not read the independent security family") from exc
        if not isinstance(family, dict) or not family:
            raise CheckError("security family must be nonempty")
        if any(not isinstance(name, str) or Path(name).name != name
               or not name.startswith("test_") or not name.endswith(".py")
               for name in family):
            raise CheckError("invalid security family member")
        names = ["bootstrap/tests/" + name for name in family]
        names.append("bootstrap/tests/test_security_marker.py")
    resolved = [_file(root, name) for name in names]
    if len(set(resolved)) != len(resolved):
        raise CheckError("required-file configuration contains duplicate identities")
    return set(resolved)


def _report(path: Path, started_ns: int) -> ET.Element:
    now = time.time_ns()
    if started_ns <= 0 or started_ns > now:
        raise CheckError("invalid run start time")
    try:
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode):
            raise CheckError("report must be a regular, non-symlink file")
        if before.st_mtime_ns < started_ns or before.st_mtime_ns > now:
            raise CheckError("report is stale or has a future modification time")
        if before.st_size > MAX_REPORT_BYTES:
            raise CheckError("report exceeds the size limit")
        with path.open("rb") as handle:
            data = handle.read(MAX_REPORT_BYTES + 1)
        after = path.lstat()
        identity = lambda value: (value.st_dev, value.st_ino, value.st_size,
                                  value.st_mtime_ns, value.st_ctime_ns)
        if identity(before) != identity(after) or len(data) > MAX_REPORT_BYTES:
            raise CheckError("report changed during comparison")
        source = data.decode("utf-8-sig")
        if "\x00" in source or "<!DOCTYPE" in source.upper() or "<!ENTITY" in source.upper():
            raise CheckError("report contains unsupported XML declarations")
        document = ET.fromstring(source)  # nosec B314: bounded UTF-8, no DTD/entities
    except (OSError, UnicodeError, ET.ParseError, ValueError) as exc:
        raise CheckError("report is absent or malformed") from exc
    if document.tag == "testsuites":
        suites = list(document)
        if len(suites) != 1 or suites[0].tag != "testsuite":
            raise CheckError("report must describe exactly one pytest suite")
        document = suites[0]
    if document.tag != "testsuite":
        raise CheckError("report is not a pytest test suite")
    return document


def compare(root: Path, report: Path, started_ns: int, required: set[str]) -> int:
    suite = _report(report, started_ns)
    modules: dict[str, set[str]] = defaultdict(set)
    for path in root.rglob("*.py"):
        relative = path.relative_to(root)
        modules[".".join(relative.with_suffix("").parts)].add(relative.as_posix())
    counts = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    seen: set[tuple[str, str]] = set()
    successes: set[str] = set()
    for case in suite:
        if case.tag in {"properties", "system-out", "system-err"}:
            continue
        if case.tag != "testcase":
            raise CheckError("report contains an unsupported suite member")
        classname, name = case.get("classname", ""), case.get("name", "")
        if not classname or not name or (classname, name) in seen:
            raise CheckError("report contains an ambiguous or duplicate test identity")
        seen.add((classname, name))
        candidates = set().union(*(paths for module, paths in modules.items()
                                   if classname == module or classname.startswith(module + ".")))
        if len(candidates) != 1:
            raise CheckError("test classname does not resolve to exactly one source file")
        filename = _file(root, candidates.pop())
        if "file" in case.attrib and _file(root, case.attrib["file"]) != filename:
            raise CheckError("test file and classname identities disagree")
        outcomes = [child.tag for child in case
                    if child.tag in {"failure", "error", "skipped"}]
        if len(outcomes) > 1 or any(child.tag not in {
                "failure", "error", "skipped", "properties", "system-out", "system-err"
        } for child in case):
            raise CheckError("test case has ambiguous outcomes")
        counts["tests"] += 1
        if outcomes:
            counts[{"failure": "failures", "error": "errors", "skipped": "skipped"}[outcomes[0]]] += 1
            if filename in required:
                raise CheckError("a required file has a skipped or failed case: " + filename)
        else:
            successes.add(filename)
    for key, actual in counts.items():
        declared = suite.get(key, "")
        if not re.fullmatch(r"[0-9]+", declared) or int(declared) != actual:
            raise CheckError("suite counts are absent or disagree with reported cases")
    missing = required - successes
    if missing:
        raise CheckError("required files without successful executed cases: " + ", ".join(sorted(missing)))
    return counts["tests"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--started-ns", type=int, required=True,
                        help="time.time_ns() recorded before the pytest run")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--required-files", type=Path,
                        help="adopter-owned JSON list instead of Cairn's security family")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve(strict=True)
        required = required_files(root, args.required_files)
        count = compare(root, args.report, args.started_ns, required)
    except (CheckError, OSError, RuntimeError) as exc:
        print("release membership: FAIL: " + str(exc), file=sys.stderr)
        return 1
    print(f"release membership: PASS: {len(required)} required files; {count} reported cases. "
          "File-level outcomes only; no node, provenance or adequacy proof.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
