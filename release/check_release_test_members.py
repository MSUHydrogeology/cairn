#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compare a fresh pytest JUnit report with independently required test files.

This checks file presence and reported outcomes, not node completeness, command
provenance or semantic adequacy. It never runs tests or grants release authority.

In Cairn's own run (no ``--required-files``) one skip is allowed in a required
file: a genuine ``pytest.skip`` whose exact test the project manifest's
native-only list (``NATIVE_ONLY_NODE_IDS``, bound to ``NATIVE_ONLY_POLICY_ID``)
names for the other platform than the one that produced the report. The list is
read as literals, never imported, and every static binding of its two names
must be unique. A listed skip is never the passing case a required file needs.
Whether each platform-only test then ran and passed on its own host is proved
only by the separate native records that ``release/security_check.py`` joins.
An adopter-owned list stays strict and never reads the manifest.
"""
from __future__ import annotations

import argparse
import ast
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import time
from typing import NamedTuple
import xml.etree.ElementTree as ET

MAX_REPORT_BYTES = 32 * 1024 * 1024


class CheckError(Exception):
    """The report cannot establish the required file-level result.

    ``code`` is a stable identifier printed after the message; callers and tests
    tell refusals apart by it, never by wording.
    """

    def __init__(self, message: str, code: str = "refused") -> None:
        super().__init__(message)
        self.code = code


class NativeSkips(NamedTuple):
    """Native-only test IDs: those whose skip is expected on this host, and those
    that belong on this host and so must never skip here."""

    other_platform: frozenset[str]
    this_platform: frozenset[str]


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
        manifest = root / "tests/security_manifest.py"
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
        names = ["tests/" + name for name in family]
        names.append("tests/test_security_marker.py")
    resolved = [_file(root, name) for name in names]
    if len(set(resolved)) != len(resolved):
        raise CheckError("required-file configuration contains duplicate identities")
    return set(resolved)


def _host_tag() -> str:
    """The native-only list's tag for the host that produced the report."""
    return "nt" if os.name == "nt" else "posix"


def _binds(node: ast.AST, name: str) -> bool:
    """Whether *node* can bind *name* anywhere in the module (conservative)."""
    if isinstance(node, ast.Name):
        return node.id == name and isinstance(node.ctx, (ast.Store, ast.Del))
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                         ast.ExceptHandler, ast.MatchAs, ast.MatchStar)):
        return getattr(node, "name", None) == name
    if isinstance(node, ast.MatchMapping):
        return node.rest == name
    if isinstance(node, (ast.Global, ast.Nonlocal)):
        return name in node.names
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return any(alias.name == "*" or (alias.asname or alias.name.split(".")[0]) == name
                   for alias in node.names)
    return False


def _policy_literal(tree: ast.Module, name: str) -> object:
    statements = [node for node in tree.body
                  if (isinstance(node, ast.AnnAssign) and node.value is not None
                      and isinstance(node.target, ast.Name) and node.target.id == name)
                  or (isinstance(node, ast.Assign) and len(node.targets) == 1
                      and isinstance(node.targets[0], ast.Name) and node.targets[0].id == name)]
    if len(statements) != 1:
        raise CheckError("native-only policy is absent or not one plain module-level "
                         "assignment: " + name, "policy-malformed")
    try:
        return ast.literal_eval(statements[0].value)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError) as exc:
        raise CheckError("native-only policy is not a literal: " + name,
                         "policy-malformed") from exc


def other_platform_skips(root: Path, host: str) -> NativeSkips:
    """Read the project's native-only list as literals and return its test IDs.

    The manifest is parsed, never imported. The list must be bound exactly once,
    well formed, without duplicates, and match its recorded SHA-256 identity
    (computed as ``tests/security_manifest.py`` computes it).
    """
    names = ("NATIVE_ONLY_NODE_IDS", "NATIVE_ONLY_POLICY_ID")
    try:
        tree = ast.parse((root / "tests/security_manifest.py").read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError) as exc:
        raise CheckError("could not read the native-only policy", "policy-malformed") from exc
    for name in names:
        if sum(_binds(node, name) for node in ast.walk(tree)) > 1:
            raise CheckError("native-only policy is bound more than once: " + name,
                             "policy-bindings-competing")
    rows, declared = (_policy_literal(tree, name) for name in names)
    if type(rows) is not tuple or type(declared) is not str:
        raise CheckError("native-only policy has the wrong type", "policy-malformed")
    grouped: dict[str, set[str]] = {"nt": set(), "posix": set()}
    seen: set[str] = set()
    canonical: list[str] = []
    for entry in rows:
        if type(entry) is not tuple or len(entry) != 2:
            raise CheckError("malformed native-only policy entry", "policy-malformed")
        tag, nodeid = entry
        if type(tag) is not str or tag not in grouped:
            raise CheckError("unknown native-only host", "policy-malformed")
        if (type(nodeid) is not str or not nodeid or not nodeid.isascii()
                or "\n" in nodeid or "\r" in nodeid or nodeid in seen):
            raise CheckError("duplicate or malformed native-only node ID", "policy-malformed")
        path, _, case = nodeid.partition("::")
        if (not case or not path.endswith(".py") or "\\" in path
                or PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts
                or PurePosixPath(path).as_posix() != path):
            raise CheckError("native-only node ID has no canonical file and case",
                             "policy-malformed")
        seen.add(nodeid)
        grouped[tag].add(nodeid)
        canonical.append(f"{tag}\t{nodeid}\n")
    identity = "sha256:" + hashlib.sha256("".join(canonical).encode("ascii")).hexdigest()
    if identity != declared:
        raise CheckError("native-only policy identity mismatch", "policy-digest-mismatch")
    other = "posix" if host == "nt" else "nt"
    return NativeSkips(frozenset(grouped[other]), frozenset(grouped[host]))


def _native_node(filename: str, classname: str, name: str) -> str:
    """The pytest node ID for a report identity: file, any classes, then the case
    name with its parameter label kept as pytest wrote it."""
    module = ".".join(PurePosixPath(filename).with_suffix("").parts)
    classes = classname[len(module):].split(".")[1:]
    return "::".join([filename, *classes, name])


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


def compare(root: Path, report: Path, started_ns: int, required: set[str],
            native: NativeSkips | None = None) -> tuple[int, int]:
    """Return (reported cases, listed other-platform skips accepted).

    ``native`` is given only for Cairn's own run; without it any skipped or failed
    case in a required file is refused.
    """
    suite = _report(report, started_ns)
    modules: dict[str, set[str]] = defaultdict(set)
    for path in root.rglob("*.py"):
        relative = path.relative_to(root)
        modules[".".join(relative.with_suffix("").parts)].add(relative.as_posix())
    counts = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    seen: set[tuple[str, str]] = set()
    successes: set[str] = set()
    nodes: set[str] = set()
    listed = 0
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
        node = _native_node(filename, classname, name) if native is not None else ""
        if native is not None:
            if node in nodes:
                raise CheckError("two report cases translate to one native test: " + node,
                                 "identity-ambiguous")
            nodes.add(node)
        counts["tests"] += 1
        if outcomes:
            counts[{"failure": "failures", "error": "errors", "skipped": "skipped"}[outcomes[0]]] += 1
            if filename in required:
                listed += _refuse_unless_listed(outcomes[0], case, filename, native, node)
        else:
            successes.add(filename)
    for key, actual in counts.items():
        declared = suite.get(key, "")
        if not re.fullmatch(r"[0-9]+", declared) or int(declared) != actual:
            raise CheckError("suite counts are absent or disagree with reported cases")
    missing = required - successes
    if missing:
        raise CheckError("required files without successful executed cases: "
                         + ", ".join(sorted(missing)), "required-file-no-pass")
    return counts["tests"], listed


def _refuse_unless_listed(outcome: str, case: ET.Element, filename: str,
                          native: NativeSkips | None, node: str) -> int:
    """Refuse a non-passing case in a required file, except a listed skip (returns 1)."""
    if outcome != "skipped":
        raise CheckError("a required file has a failed case: " + filename, "required-case-failed")
    if native is None:
        raise CheckError("a required file has a skipped case: " + filename, "required-case-skipped")
    if node in native.this_platform:
        raise CheckError("a test that belongs on this platform was skipped: " + node,
                         "skip-same-platform")
    if node not in native.other_platform:
        raise CheckError("a required file has a skip the native list does not name: " + node,
                         "skip-unlisted")
    skipped = case.find("skipped")
    if skipped is None or skipped.get("type") != "pytest.skip":
        raise CheckError("a listed test was not skipped by pytest.skip: " + node,
                         "skip-not-genuine")
    return 1


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
        native = (other_platform_skips(root, _host_tag())
                  if args.required_files is None else None)
        count, listed = compare(root, args.report, args.started_ns, required, native)
    except (CheckError, OSError, RuntimeError) as exc:
        print(f"release membership: FAIL: {exc} [{getattr(exc, 'code', 'refused')}]",
              file=sys.stderr)
        return 1
    extra = f" (listed other-platform skips accepted: {listed})" if listed else ""
    print(f"release membership: PASS: {len(required)} required files; {count} reported cases{extra}. "
          "File-level outcomes only; no node, provenance or adequacy proof.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
