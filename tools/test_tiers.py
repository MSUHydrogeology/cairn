#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
"""Assign every test file to exactly one tier, from a per-tier configuration.

The testing-discipline module asks that a test's tier come from where it
lives, never from a label someone remembers to apply. Cairn's ordinary tests
are grouped under ``unit/``, ``contract/``, ``integration/``, and ``security/``;
workflow tests and protected apparatus remain at their approved paths.
``tools/test_tiers.json`` maps file-name patterns to tiers, and discovery stays
recursive; the first tier whose pattern matches a file owns it. ``check`` fails
when a test file matches no tier or a pattern matches no file, so a new test is
placed automatically by its name or stopped until a pattern places it.

  python tools/test_tiers.py check
  python tools/test_tiers.py list [TIER]
  python tools/test_tiers.py list --json
  python tools/test_tiers.py files TIER    # paths for a scoped pytest run
  python tools/test_tiers.py for [--range BASE..HEAD] PATH...

``files`` only prints paths. A tier larger than the broad-run guard allows
is still refused by that guard outside a certifying run; this tool does not
work around it. Standard library only; it reads files and writes nothing.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "tools" / "test_tiers.json"
TEST_DIR = ROOT / "bootstrap" / "tests"
_INVENTORY_SCHEMA = "cairn-test-inventory/1"
_INVENTORY_COUNTING_METHOD = "recursive-test-files-utf8-replace-splitlines-v1"


def load_tiers(config: Path = CONFIG) -> list[dict]:
    """Return the tiers in priority order, each with name, about and patterns."""
    data = json.loads(config.read_text(encoding="utf-8"))
    tiers = data.get("tiers")
    if not isinstance(tiers, list) or not tiers:
        raise ValueError(f"{config.name}: 'tiers' must be a non-empty list")
    for i, tier in enumerate(tiers):
        patterns = tier.get("patterns") if isinstance(tier, dict) else None
        if not isinstance(tier, dict) or not isinstance(tier.get("name"), str) \
                or not isinstance(patterns, list) or not patterns \
                or not all(isinstance(p, str) and p for p in patterns):
            raise ValueError(f"{config.name}: tier {i + 1} needs a name and a "
                             "non-empty list of patterns")
    names = [t["name"] for t in tiers]
    if len(set(names)) != len(names):
        raise ValueError(f"{config.name}: duplicate tier name")
    return tiers


def find_test_files(test_dir: Path = TEST_DIR) -> list[Path]:
    """Every file pytest would collect as a test module, at any depth, sorted.

    pytest collects ``test_*.py`` and ``*_test.py`` in subfolders too, so a
    file the check skipped would be a test with no tier. A ``*_test.py`` name
    matches no ``test_*`` pattern, so the check stops it until one is added."""
    found = set(test_dir.rglob("test_*.py")) | set(test_dir.rglob("*_test.py"))
    return sorted(p for p in found if "__pycache__" not in p.parts)


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


def tests_for_paths(paths: list[str], files: list[Path], root: Path = ROOT, *,
                    reviewed_range: str | None = None,
                    broad_limit: int = 40,
                    omitted: list[Path] | None = None) -> list[Path]:
    """Select test files that name a changed file by path or file name.

    Folder sweeps do not name their discovered members and are intentionally
    absent; release verification covers those wider effects. AGENTS.md needs
    an explicit reviewed commit range so later commits cannot erase its diff.
    Its readers narrow to changed passages only when their broad list exceeds
    the runner limit; excluded readers are returned through ``omitted``.
    """
    needles: set[str] = set()
    python_stems: set[str] = set()
    governing_passages: list[str] = []
    governing_path_requested = False
    changed_test_files: set[Path] = set()
    directly_selected_tests: set[Path] = set()
    project_root = root.resolve()
    for value in paths:
        path = Path(value)
        candidate = path.resolve() if path.is_absolute() else (project_root / path).resolve()
        try:
            path = candidate.relative_to(project_root)
        except ValueError as exc:
            raise ValueError(f"path is outside project root: {value}") from exc
        if not path.name or not candidate.is_file():
            raise ValueError(f"expected a file path: {value}")
        if candidate in files:
            changed_test_files.add(candidate)
        if path.name == "AGENTS.md":
            governing_path_requested = True
            if not reviewed_range:
                raise ValueError("AGENTS.md selection requires --range BASE..HEAD")
            changed = subprocess.run(
                ["git", "-C", str(root), "diff", "--unified=0", reviewed_range, "--",
                 path.as_posix()], text=True, capture_output=True, check=False)
            if changed.returncode:
                raise ValueError(f"invalid reviewed range {reviewed_range!r}: "
                                 f"{changed.stderr.strip()}")
            governing_passages.extend(
                " ".join(re.findall(r"[a-z0-9_]+", line.lower()))
                for line in changed.stdout.splitlines()
                if line.startswith(("+", "-"))
                and not line.startswith(("+++", "---"))
                and len(re.findall(r"[a-z0-9_]+", line.lower())) >= 5)
        else:
            needles.add(path.as_posix())
            needles.add(path.name)
            if path.suffix == ".py":
                python_stems.add(path.stem)
                needles.add(path.with_suffix("").as_posix().replace("/", "."))
    candidates = []
    governing_readers = []
    for test in files:
        source = test.read_text(encoding="utf-8", errors="replace")
        normalized = " ".join(re.findall(r"[a-z0-9_]+", source.lower()))
        pins_changed_passage = False
        for passage in governing_passages:
            words = passage.split()
            if any(" ".join(words[i:i + 5]) in normalized
                   for i in range(max(0, len(words) - 4))):
                pins_changed_passage = True
                break
        names_requested_files = any(
            re.search(rf"(?<![\w-]){re.escape(needle)}(?![\w-])", source,
                      flags=re.IGNORECASE)
            for needle in needles)
        # A bare stem can be prose. Keep it when it is used as an import,
        # called symbol, exact CLI argument, or quoted helper name.
        names_requested_python_module = any(
            re.search(
                rf"(?:\bimport\s+(?:[\w.]+\.)?{re.escape(stem)}\b"
                rf"|\bfrom\s+{re.escape(stem)}\s+import\b"
                rf"|\bfrom\s+[\w.]+\s+import\s+(?:"
                rf"\([^)]*\b{re.escape(stem)}\b[^)]*\)"
                rf"|[^\n#]*\b{re.escape(stem)}\b)"
                rf"|(?<![\w-]){re.escape(stem)}\s*\("
                rf"|['\"]{re.escape(stem)}['\"]"
                rf"|['\"][\w]*_{re.escape(stem)}['\"]"
                rf"|\bscaffold\.py\s+{re.escape(stem)}\b"
                rf"|(?<![\w-])(?:scaffold\.py\s+)?{re.escape(stem)}"
                rf"\s+(?:--(?:plan|stage|apply)|stage|apply)\b)",
                source, flags=re.IGNORECASE)
            for stem in python_stems)
        if (test in changed_test_files or pins_changed_passage or names_requested_files
                or names_requested_python_module
                or (governing_path_requested and "AGENTS.md" in source)):
            candidates.append(test)
        if (test in changed_test_files or names_requested_files
                or names_requested_python_module):
            directly_selected_tests.add(test)
        if governing_path_requested and "AGENTS.md" in source:
            governing_readers.append(test)
    selected = candidates
    if governing_path_requested and len(governing_readers) > broad_limit:
        def pins_changed_passage(test: Path) -> bool:
            normalized = " ".join(re.findall(
                r"[a-z0-9_]+", test.read_text(
                    encoding="utf-8", errors="replace").lower()))
            return any(
                any(" ".join(words[i:i + 5]) in normalized
                    for i in range(max(0, len(words) - 4)))
                for words in (passage.split() for passage in governing_passages))

        selected = [test for test in candidates
                    if test not in governing_readers or test in changed_test_files
                    or test in directly_selected_tests or pins_changed_passage(test)]
        excluded = [test for test in governing_readers if test not in selected]
        if omitted is not None:
            omitted.extend(excluded)
    return selected


def main(argv: list[str] | None = None, *, config: Path = CONFIG,
         test_dir: Path = TEST_DIR, root: Path = ROOT,
         out=sys.stdout, err=sys.stderr) -> int:
    ap = argparse.ArgumentParser(prog="test_tiers", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="verb", required=True)
    sub.add_parser("check", help="fail on an unplaced file or an unused pattern")
    ls = sub.add_parser("list", help="files and lines per tier")
    ls.add_argument("tier", nargs="?")
    ls.add_argument("--json", action="store_true",
                    help="emit the complete aggregate tier inventory")
    fs = sub.add_parser("files", help="print the paths in one tier")
    fs.add_argument("tier")
    scoped = sub.add_parser("for", help="tests that name changed file paths")
    scoped.add_argument("--range", dest="reviewed_range",
                        help="commit range covered by this review (required for AGENTS.md)")
    scoped.add_argument("paths", nargs="+")
    args = ap.parse_args(argv)

    try:
        tiers = load_tiers(config)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"invalid tier configuration: {exc}", file=err)
        return 2
    files = find_test_files(test_dir)
    if args.verb == "for":
        try:
            omitted: list[Path] = []
            chosen = tests_for_paths(args.paths, files, root,
                                     reviewed_range=args.reviewed_range,
                                     omitted=omitted)
        except ValueError as exc:
            print(str(exc), file=err)
            return 2
        for path in chosen:
            print(path.relative_to(root) if path.is_relative_to(root) else path,
                  file=out)
        print(f"{len(chosen)} test files selected for the requested paths", file=err)
        if omitted:
            print(f"{len(omitted)} AGENTS.md readers omitted above the guard: "
                  + ", ".join(str(p.relative_to(root)) for p in omitted), file=err)
        return 0
    owner, unplaced, unused = classify(files, tiers)
    known = [t["name"] for t in tiers]
    if args.verb == "list" and args.json:
        if args.tier:
            print("JSON inventory requires the complete tier list", file=err)
            return 2
        if unplaced or unused:
            print("JSON inventory unavailable: tier placement is invalid", file=err)
            return 2
        by_tier = {name: [p for p in files if owner.get(p.stem) == name]
                   for name in known}
        rows = []
        for tier in tiers:
            name = tier["name"]
            paths = by_tier[name]
            rows.append({
                "name": name,
                "files": len(paths),
                "lines": sum(
                    len(path.read_text(encoding="utf-8", errors="replace").splitlines())
                    for path in paths
                ),
            })
        inventory = {
            "schema": _INVENTORY_SCHEMA,
            "counting_method": _INVENTORY_COUNTING_METHOD,
            "tiers": rows,
            "total": {
                "files": sum(row["files"] for row in rows),
                "lines": sum(row["lines"] for row in rows),
            },
        }
        print(json.dumps(inventory, sort_keys=True), file=out)
        return 0
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
