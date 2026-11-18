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
import hashlib
import importlib.util
import json
import locale
import math
import os
import re
import stat
import subprocess
import sys
import types
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple


_TOOL_DIR = Path(__file__).resolve().parent
ROOT = _TOOL_DIR.parent.parent if _TOOL_DIR.name == "tools" and _TOOL_DIR.parent.name == "dev" else _TOOL_DIR.parent
_GIT_READ_SHA256 = "b67deb4e50eaee1e420d49af5ddac318aa110407bcd7c03d305091146cf15252"
_GIT_READ_MAX_BYTES = 256 * 1024


def _load_verified_git_read():
    """Execute only the bounded, pinned helper buffer from the fixed tools root."""
    path = os.path.abspath(os.path.join(ROOT, "dev", "tools", "git_read.py"))
    if not os.path.exists(path):
        path = os.path.abspath(os.path.join(ROOT, "tools", "git_read.py"))
    chain = []
    current = os.path.splitdrive(path)[0] + os.sep
    for part in path[len(current):].split(os.sep):
        if not part:
            continue
        current = os.path.join(current, part)
        try:
            info = os.lstat(current)
        except OSError:
            raise RuntimeError("git-read-binding-failed") from None
        attrs = getattr(info, "st_file_attributes", 0)
        reparse = bool(attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))
        if stat.S_ISLNK(info.st_mode) or reparse:
            raise RuntimeError("git-read-binding-failed")
        if current != path and not stat.S_ISDIR(info.st_mode):
            raise RuntimeError("git-read-binding-failed")
        chain.append((current, info))
    try:
        before = chain[-1][1]
        if (not stat.S_ISREG(before.st_mode) or before.st_size < 0
                or before.st_size > _GIT_READ_MAX_BYTES):
            raise RuntimeError("git-read-binding-failed")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        fd = os.open(path, flags)
        try:
            opened = os.fstat(fd)

            def key(row):
                return (
                    int(row.st_dev), int(row.st_ino), int(row.st_mode),
                    int(row.st_size), int(row.st_mtime_ns), int(row.st_ctime_ns),
                    int(getattr(row, "st_uid", 0) or 0),
                    int(getattr(row, "st_gid", 0) or 0),
                    int(getattr(row, "st_file_attributes", 0) or 0),
                    int(getattr(row, "st_reparse_tag", 0) or 0),
                )

            def opened_matches(path_info, descriptor_info):
                if (not stat.S_ISREG(path_info.st_mode)
                        or not stat.S_ISREG(descriptor_info.st_mode)):
                    return False
                opened_compare_key = list(key(descriptor_info))
                if os.name == "nt":
                    path_birth = getattr(path_info, "st_birthtime_ns", None)
                    descriptor_birth = getattr(
                        descriptor_info, "st_birthtime_ns", None)
                    if (type(path_birth) is not int
                            or type(descriptor_birth) is not int
                            or path_info.st_ctime_ns != path_birth
                            or path_birth != descriptor_birth):
                        return False
                    opened_compare_key[5] = descriptor_birth
                return tuple(opened_compare_key) == key(path_info)

            if not opened_matches(before, opened):
                raise RuntimeError("git-read-binding-failed")
            chunks = []
            remaining = _GIT_READ_MAX_BYTES + 1
            while remaining:
                part = os.read(fd, min(65536, remaining))
                if not part:
                    break
                chunks.append(part)
                remaining -= len(part)
            source = b"".join(chunks)
            after = os.fstat(fd)
            current_chain = [(name, os.lstat(name)) for name, _old in chain]
            if (key(after) != key(opened)
                    or tuple((name, key(row)) for name, row in current_chain)
                    != tuple((name, key(row)) for name, row in chain)
                    or len(source) != opened.st_size
                    or len(source) > _GIT_READ_MAX_BYTES):
                raise RuntimeError("git-read-binding-failed")
        finally:
            os.close(fd)
    except (OSError, IndexError):
        raise RuntimeError("git-read-binding-failed") from None
    if hashlib.sha256(source).hexdigest() != _GIT_READ_SHA256:
        raise RuntimeError("git-read-binding-failed")
    module = types.ModuleType("_cairn_verified_git_read")
    module.__file__ = "<verified tools/git_read.py buffer>"
    module.__verified_source__ = source
    module.__verified_sha256__ = _GIT_READ_SHA256
    try:
        exec(compile(source, module.__file__, "exec", dont_inherit=True), module.__dict__)
        module.bind_verified_source(source, _GIT_READ_SHA256)
    except Exception:
        raise RuntimeError("git-read-binding-failed") from None
    return module


_GIT_READ = _load_verified_git_read()
_GIT_HISTORY_MAX_BYTES = _GIT_READ.HISTORY_MAX_BYTES


class _GitHistoryUnavailable(RuntimeError):
    """A repository-history read failed or returned unusable data."""

#: (prefix, class). First match wins, so order is the rule. `product` is never
#: a default -- an unmatched path is reported as unclassified.
_RULES: Tuple[Tuple[str, str], ...] = (
    ("dev/",                              "dev"),
    ("tests/test_security",               "security-machinery"),
    ("tests/test_gate",                   "security-machinery"),
    ("tests/test_reanchor",               "security-machinery"),
    ("tests/test_ast_attest",             "security-machinery"),
    ("install/security_check.py",         "security-machinery"),
    ("install/SAFETY.md",                 "security-machinery"),
    ("tests/quality_gate.py",             "security-machinery"),
    ("install/_scaffold/",               "product"),
    ("install/scaffold.py",              "product"),
    ("install/dimensions/",              "product"),
    ("install/on-ramp/",                 "product"),
    ("install/",                         "other-machinery"),
    ("tests/",                           "other-machinery"),
    ("release/",                         "other-machinery"),
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
    ("bootstrap/_scaffold/",            "product"),
    ("bootstrap/scaffold.py",           "product"),
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
    (".zenodo.json",                      "product"),
    ("CLAUDE.md",                         "product"),
    ("VENDOR.md",                         "product"),
    (".agents/",                          "other-machinery"),
    (".github/",                          "other-machinery"),
    (".gitignore",                        "other-machinery"),
)

_CLASSES = ("dev", "security-machinery", "other-machinery", "product")
def _load_shared_pulse():
    """Load the shared pulse only from the sibling tool directory."""
    path = Path(__file__).resolve().with_name("pulse.py")
    spec = importlib.util.spec_from_file_location("_cairn_shared_pulse", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("pulse-module-unavailable")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except (OSError, ImportError, ValueError, TypeError):
        raise RuntimeError("pulse-module-unavailable") from None
    return module


_PULSE = _load_shared_pulse()


def _pulse(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    return _PULSE.run_pulse(args, parser)


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
    result = _GIT_READ.run_git(
        str(root), ("log", f"--since={since}", "--numstat", "--date=short",
                    "--pretty=format:C%cd", "--no-merges"),
        output_limit=_GIT_HISTORY_MAX_BYTES)
    if result.state != "completed" or result.returncode != 0:
        raise _GitHistoryUnavailable from None
    try:
        out = result.stdout.decode(locale.getpreferredencoding(False), "strict")
    except (LookupError, UnicodeError):
        raise _GitHistoryUnavailable from None
    rows: List[Tuple[str, str, int]] = []
    week = ""
    for line in out.splitlines():
        if line.startswith("C"):
            try:
                week = _week_of(line[1:].strip())
            except ValueError:
                raise _GitHistoryUnavailable from None
            continue
        parts = line.split("\t")
        if len(parts) == 3 and parts[0].isdigit() and week:
            rows.append((week, parts[2], int(parts[0])))
    return rows


def _snapshot_date(root: Path) -> str:
    result = _GIT_READ.run_git(
        str(root), ("log", "-1", "--date=short", "--pretty=format:%cd"),
        output_limit=1024)
    if result.state != "completed" or result.returncode != 0:
        raise _GitHistoryUnavailable from None
    try:
        stamp = result.stdout.decode("ascii", "strict").strip()
        if not stamp:
            raise _GitHistoryUnavailable
        _dt.date.fromisoformat(stamp)
        return stamp
    except (UnicodeError, ValueError):
        raise _GitHistoryUnavailable from None


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gauge", description="Weekly lines added by class; product share.")
    parser.add_argument("--since", default="2026-04-27")
    parser.add_argument("--snapshot", action="store_true",
                        help="Write a dated path-to-class snapshot.")
    parser.add_argument("--root", default=None)
    _PULSE.register_arguments(parser, include_switch=True)
    args = parser.parse_args(argv)
    if args.pulse:
        return _pulse(args, parser)
    if args.json:
        parser.error("--json requires --pulse")
    if (args.junit_report or args.before_junit_report or args.tier_inventory
            or args.before_tier_inventory
            or args.meter_aggregate
            or args.artifact_input
            or any((args.commit_label, args.python_label,
                    args.selection_label, args.seed_label,
                    args.before_commit_label, args.before_python_label,
                    args.before_selection_label, args.before_seed_label))):
        parser.error("JUnit reports and pulse labels require --pulse")
    root = Path(args.root).resolve() if args.root else ROOT

    try:
        history_rows = _numstat(root, args.since)
        stamp = _snapshot_date(root) if args.snapshot else None
    except _GitHistoryUnavailable:
        print("gauge: Git history is unavailable; no measurement was produced.",
              file=sys.stderr)
        return 2

    by_week: Dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    unclassified: collections.Counter = collections.Counter()
    for week, path, added in history_rows:
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
        assert stamp is not None
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
