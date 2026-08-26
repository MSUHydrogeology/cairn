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
import subprocess
import sys
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
    ("doctrine/",                         "product"),
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
    args = parser.parse_args(argv)
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
