#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
"""Assign every test file to exactly one tier, from a per-tier configuration.

The testing-discipline module asks that a test's tier come from where it
lives, never from a label someone remembers to apply. Cairn's tests share one
folder, so ``tools/test_tiers.json`` maps file-name patterns to tiers; the
first tier whose pattern matches a file owns it. ``check`` fails when a test
file matches no tier or a pattern matches no file, so a new test is placed
automatically by its name or stopped until a pattern places it.

  python tools/test_tiers.py check
  python tools/test_tiers.py list [TIER]
  python tools/test_tiers.py files TIER    # paths for a scoped pytest run

``files`` only prints paths. A tier larger than the broad-run guard allows
is still refused by that guard outside a certifying run; this tool does not
work around it. Standard library only; it reads files and writes nothing.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "tools" / "test_tiers.json"
TEST_DIR = ROOT / "bootstrap" / "tests"


def load_tiers(config: Path = CONFIG) -> list[dict]:
    """Return the tiers in priority order, each with name, about and patterns."""
    data = json.loads(config.read_text(encoding="utf-8"))
    tiers = data["tiers"]
    names = [t["name"] for t in tiers]
    if len(set(names)) != len(names):
        raise ValueError(f"duplicate tier name in {config}")
    return tiers


def find_test_files(test_dir: Path = TEST_DIR) -> list[Path]:
    """Every top-level ``test_*.py`` file, sorted."""
    return sorted(test_dir.glob("test_*.py"))


def classify(files: list[Path], tiers: list[dict]):
    """Return (tier of each file stem, unplaced stems, (tier, pattern) pairs
    that place no file). The first tier with a matching pattern wins.

    A pattern places no file when it matches nothing, or when every file it
    matches is already owned by an earlier tier; either way the configuration
    claims a placement that never happens, so it is reported."""
    owner: dict[str, str] = {}
    placing: set[tuple[str, str]] = set()
    for path in files:
        stem = path.stem
        for tier in tiers:
            hits = [p for p in tier["patterns"] if fnmatch.fnmatchcase(stem, p)]
            if hits:
                owner[stem] = tier["name"]
                placing.update((tier["name"], p) for p in hits)
                break
    unplaced = sorted(p.stem for p in files if p.stem not in owner)
    unused = [(t["name"], p) for t in tiers for p in t["patterns"]
              if (t["name"], p) not in placing]
    return owner, unplaced, unused


def main(argv: list[str] | None = None, *, config: Path = CONFIG,
         test_dir: Path = TEST_DIR, out=sys.stdout, err=sys.stderr) -> int:
    ap = argparse.ArgumentParser(prog="test_tiers", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="verb", required=True)
    sub.add_parser("check", help="fail on an unplaced file or an unused pattern")
    ls = sub.add_parser("list", help="files and lines per tier")
    ls.add_argument("tier", nargs="?")
    fs = sub.add_parser("files", help="print the paths in one tier")
    fs.add_argument("tier")
    args = ap.parse_args(argv)

    tiers = load_tiers(config)
    files = find_test_files(test_dir)
    owner, unplaced, unused = classify(files, tiers)
    known = [t["name"] for t in tiers]
    if getattr(args, "tier", None) and args.tier not in known:
        print(f"unknown tier {args.tier!r}; tiers are {', '.join(known)}", file=err)
        return 2

    if args.verb == "check":
        for stem in unplaced:
            print(f"UNPLACED {stem}.py: add a pattern for it to {config.name}", file=err)
        for name, pattern in unused:
            print(f"UNUSED   {name}: pattern {pattern!r} places no test file (matches none, or an earlier tier owns them)", file=err)
        if unplaced or unused:
            return 1
        print(f"ok: {len(files)} test files, each in exactly one of {len(tiers)} tiers", file=out)
        return 0

    by_tier = {name: [p for p in files if owner.get(p.stem) == name] for name in known}
    if args.verb == "files":
        chosen = by_tier[args.tier]
        for p in chosen:
            print(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p, file=out)
        print(f"{len(chosen)} files in tier {args.tier}; a run over many files is "
              "still subject to the broad-run guard", file=err)
        return 0

    for name in ([args.tier] if args.tier else known):
        paths = by_tier[name]
        lines = sum(len(p.read_text(encoding="utf-8", errors="replace").splitlines())
                    for p in paths)
        print(f"{name:12} {len(paths):4d} files {lines:8,d} lines", file=out)
    if unplaced:
        print(f"{'unplaced':12} {len(unplaced):4d} files", file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
