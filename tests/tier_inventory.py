#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
"""Assign every test file to exactly one tier, from a per-tier configuration.

The testing-discipline module asks that a test's tier come from where it
lives, never from a label someone remembers to apply. Cairn's ordinary tests
are grouped under ``unit/``, ``contract/``, ``integration/``, and ``security/``;
workflow tests and protected apparatus remain at their approved paths.
``tests/test_tiers.json`` maps file-name patterns to tiers, and discovery stays
recursive; the first tier whose pattern matches a file owns it. ``check`` fails
when a test file matches no tier or a pattern matches no file, so a new test is
placed automatically by its name or stopped until a pattern places it.

  python tests/tier_inventory.py check
  python tests/tier_inventory.py list [TIER]
  python tests/tier_inventory.py list --json
  python tests/tier_inventory.py files TIER    # paths for a scoped pytest run
  python tests/tier_inventory.py for [--range BASE..HEAD] [--include-release-only] PATH...
  python tests/tier_inventory.py cert-files [--host linux|windows] [--write PATH]
  python tests/tier_inventory.py release-only [--host mac|windows]

``files`` only prints paths. A tier larger than the broad-run guard allows
is still refused by that guard outside a certifying run; this tool does not
work around it.

``cert-files`` prints the test files Linux and Windows run at certification:
every test file except the Cairn-only ones in ``RELEASE_EXCLUDED_TESTS``
(``tests/security_manifest.py``, read as data and never imported), the
release-only files and the files the ``system_independent`` list in
``tests/test_tiers.json`` names. A file on none of these lists runs on every
host. A release-only file is one that exists only to protect Cairn's own
release cut; the ``hosts.release_only`` groups in ``tests/test_tiers.json``
name each one with the hosts that run it (the Mac, and for the strict
native-evidence check also Windows) and a reason. With no ``--host`` the output
is the selection Linux and Windows share (``--host linux`` says the same);
``--host windows`` adds back the release-only files listed for Windows.
``--write PATH`` also saves the lines to a new file at an absolute path, for
``python -m pytest @PATH``; it never replaces a file. ``check`` also refuses a
``system_independent`` pattern that places no file, matches a security-tier file
or matches an excluded file.

``release-only`` prints those files, one path per line, with the counts on
standard error; ``--host`` keeps the files that host runs. ``check`` refuses a
``release_only`` pattern that places no file, a file two groups both place, a
file that ``system_independent`` also lists, a malformed group, and any file of
``RELEASE_EXCLUDED_TESTS`` that no group places or that a group lists for
Windows, so the two lists cannot drift.

``for`` leaves a release-only test out of its answer unless a changed path is
release machinery (``hosts.release_paths``: ``release/``, the gate, oracle and
quality-gate tools, the release manifest and roster, the signers file) or is
that test file itself, so ordinary development never runs one by accident.
``--include-release-only`` keeps them, for the certification reuse judgment.

Standard library only; it reads files and writes nothing, except the one new
file ``cert-files --write`` is asked for.
"""
from __future__ import annotations

import argparse
import ast
import fnmatch
import hashlib
import json
import os
import re
import stat
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_REPO_ROOT = ROOT

# Living files change in nearly every commit. The tests that mention the board
# and changelog build their own throwaway copies. For other frequently edited
# files, retain the known tests that read the current file and skip references
# in tests that build their own copies.
_LIVING_FILES = frozenset({"dev/PLANNING.md", "CHANGELOG.md"})
_PATH_READERS = {
    "dev/.cairn/cairn-lock.yml": frozenset({
        "tests/test_portable_security_sweeps.py",
    }),
    "dev/agent_collaboration.md": frozenset({
        "tests/contract/test_writing_rules_ship.py",
        "tests/test_review_stance_in_shipped_files.py",
        "tests/test_review_sweep_ships.py",
    }),
    "templates/core/dev/agent_collaboration.md": frozenset({
        "tests/contract/test_writing_rules_ship.py",
        "tests/test_review_stance_in_shipped_files.py",
        "tests/test_review_sweep_ships.py",
    }),
}

_GIT_READ_SHA256 = "e29f38935490c2619130bdf79fc072088618221bb0d2e64ff404c61aff3d5a7a"
_GIT_READ_MAX_BYTES = 256 * 1024


def _load_verified_git_read():
    """Execute only the fixed, caller-pinned helper buffer from this delivery."""
    path = os.path.abspath(os.path.join(_REPO_ROOT, "dev", "tools", "git_read.py"))
    if not os.path.exists(path):  # Before Cairn self-upgrades its installed copy.
        path = os.path.abspath(os.path.join(_REPO_ROOT, "tools", "git_read.py"))
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
        if not stat.S_ISREG(before.st_mode) or before.st_size < 0 \
                or before.st_size > _GIT_READ_MAX_BYTES:
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
            current_chain = []
            for name, _old in chain:
                row = os.lstat(name)
                current_chain.append((name, row))
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

CONFIG = ROOT / "tests" / "test_tiers.json"
TEST_DIR = ROOT / "tests"
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


def load_hosts(config: Path = CONFIG) -> list[str]:
    """Return the ``system_independent`` patterns; none when "hosts" is absent.

    A file that matches one of them is run on the Mac only at certification.
    Unlisted means system-dependent, so a new test file runs on every host."""
    hosts = json.loads(config.read_text(encoding="utf-8")).get("hosts")
    if hosts is None:
        return []
    patterns = hosts.get("system_independent") if isinstance(hosts, dict) else None
    if not isinstance(patterns, list) \
            or not all(isinstance(p, str) and p for p in patterns):
        raise ValueError(f"{config.name}: 'hosts' needs a 'system_independent' "
                         "list of patterns")
    return patterns


def load_release_excluded(test_dir: Path = TEST_DIR) -> frozenset[str]:
    """Return the test paths in ``RELEASE_EXCLUDED_TESTS``, read as data.

    The list lives in ``security_manifest.py`` beside the tests. It is parsed
    and its literal read, never imported, so reading it runs no code. Each row
    is (test path, subjects, reason); the test path is the first item."""
    manifest = test_dir / "security_manifest.py"
    try:
        tree = ast.parse(manifest.read_text(encoding="utf-8"), filename=manifest.name)
    except (OSError, SyntaxError, ValueError) as exc:
        raise ValueError(f"cannot read RELEASE_EXCLUDED_TESTS from {manifest.name}: "
                         f"{exc}") from None
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name, value = node.target.id, node.value
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            name, value = node.targets[0].id, node.value
        else:
            continue
        if name != "RELEASE_EXCLUDED_TESTS" or value is None:
            continue
        try:
            rows = ast.literal_eval(value)
        except (ValueError, TypeError, SyntaxError):
            rows = None
        if not isinstance(rows, tuple) or not all(
                isinstance(row, tuple) and len(row) == 3 and isinstance(row[0], str)
                for row in rows):
            raise ValueError(f"RELEASE_EXCLUDED_TESTS in {manifest.name} is not a "
                             "tuple of (test path, subjects, reason) rows")
        return frozenset(row[0] for row in rows)
    raise ValueError(f"no RELEASE_EXCLUDED_TESTS found in {manifest.name}")


def _repo_path(path: Path, test_dir: Path) -> str:
    """The repository-relative name the release manifest uses for a test file."""
    return "tests/" + path.relative_to(test_dir).as_posix()


def _files_matching(pattern: str, files: list[Path]) -> list[Path]:
    """The test files one pattern matches, by the matcher the tiers use."""
    owner, _unplaced, _unused = classify(files, [{"name": "hosts",
                                                  "patterns": [pattern]}])
    return [p for p in files if p.stem in owner]


def host_problems(patterns: list[str], files: list[Path], owner: dict[str, str],
                  excluded: frozenset[str], test_dir: Path) -> list[str]:
    """Plain messages for each ``system_independent`` pattern that cannot stand."""
    problems = []
    for pattern in patterns:
        hits = _files_matching(pattern, files)
        if not hits:
            problems.append(f"system_independent pattern {pattern!r} places no "
                            "test file")
            continue
        secure = [p.name for p in hits if owner.get(p.stem) == "security"]
        if secure:
            problems.append(
                f"system_independent pattern {pattern!r} matches "
                f"{', '.join(secure)} in the security tier; hostile-input and "
                "trust tests depend on the system, so remove the pattern")
        listed = [p.name for p in hits if _repo_path(p, test_dir) in excluded]
        if listed:
            problems.append(
                f"system_independent pattern {pattern!r} matches "
                f"{', '.join(listed)}, which RELEASE_EXCLUDED_TESTS already "
                "lists; keep the two lists apart")
    return problems


RELEASE_HOSTS = ("mac", "windows")


def load_release_only(config: Path = CONFIG) -> tuple[list[dict], list[str]] | None:
    """Return the ``release_only`` groups and the ``release_paths`` patterns.

    Returns None when the configuration has no ``release_only`` key, so a
    configuration written before the list existed keeps working. Each group
    names the hosts that run its files at certification (the Mac always, and
    Windows where Windows records a half of its own), a one-line reason and
    file-stem patterns. A malformed group is refused rather than skipped, so a
    typo cannot quietly put a release-only file back on Linux."""
    hosts = json.loads(config.read_text(encoding="utf-8")).get("hosts")
    if not isinstance(hosts, dict) or "release_only" not in hosts:
        return None
    raw = hosts["release_only"]
    if not isinstance(raw, list):
        raise ValueError(f"{config.name}: 'release_only' must be a list of groups")
    groups = []
    for i, group in enumerate(raw, 1):
        where = f"{config.name}: release_only group {i}"
        if not isinstance(group, dict):
            raise ValueError(f"{where} must be an object")
        names = group.get("hosts")
        if (not isinstance(names, list) or not names
                or not all(isinstance(n, str) for n in names)
                or len(set(names)) != len(names)
                or any(n not in RELEASE_HOSTS for n in names)
                or "mac" not in names):
            raise ValueError(f"{where} needs a 'hosts' list drawn from "
                             f"{', '.join(RELEASE_HOSTS)} that includes 'mac' "
                             "(the Mac runs the whole suite)")
        reason = group.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"{where} needs a 'reason' in plain words")
        patterns = group.get("patterns")
        if (not isinstance(patterns, list) or not patterns
                or not all(isinstance(p, str) and p for p in patterns)):
            raise ValueError(f"{where} needs a non-empty list of 'patterns'")
        groups.append({"hosts": tuple(names), "reason": reason,
                       "patterns": patterns})
    paths = hosts.get("release_paths", [])
    if not isinstance(paths, list) \
            or not all(isinstance(p, str) and p for p in paths):
        raise ValueError(f"{config.name}: 'release_paths' must be a list of "
                         "repository path patterns")
    return groups, paths


def release_only_files(groups: list[dict], files: list[Path]
                       ) -> tuple[dict[Path, tuple[str, ...]], list[str]]:
    """Map each release-only test file to the hosts that run it.

    The second item names every file that two groups both place: its hosts
    would be ambiguous, so ``check`` refuses it. The first group to place a
    file keeps it."""
    placed: dict[Path, tuple[str, ...]] = {}
    doubled: list[str] = []
    for group in groups:
        mine: set[Path] = set()
        for pattern in group["patterns"]:
            mine.update(_files_matching(pattern, files))
        for path in sorted(mine):
            if path in placed:
                if path.name not in doubled:
                    doubled.append(path.name)
            else:
                placed[path] = group["hosts"]
    return placed, doubled


def release_only_problems(groups: list[dict], files: list[Path],
                          independent: list[str], excluded: frozenset[str],
                          test_dir: Path) -> list[str]:
    """Plain messages for each ``release_only`` fault ``check`` refuses.

    Whether a file really is release machinery is a judgment this cannot make;
    it keeps the lists consistent: every pattern places a file, no file has two
    owners or sits on ``system_independent`` too, and every file of
    ``RELEASE_EXCLUDED_TESTS`` is placed, on the Mac only."""
    problems = []
    for group in groups:
        for pattern in group["patterns"]:
            if not _files_matching(pattern, files):
                problems.append(f"release_only pattern {pattern!r} places no "
                                "test file")
    placed, doubled = release_only_files(groups, files)
    for name in doubled:
        problems.append(f"release_only groups both place {name}; list a file "
                        "in one group only")
    if independent:
        owner, _unplaced, _unused = classify(
            files, [{"name": "system_independent", "patterns": independent}])
        for path in sorted(placed):
            if path.stem in owner:
                problems.append(f"{path.name} is on both release_only and "
                                "system_independent; keep the two lists apart")
    by_path = {_repo_path(p, test_dir): p for p in files}
    for repo_path in sorted(excluded):
        found = by_path.get(repo_path)
        if found is None:
            continue
        if found not in placed:
            problems.append(f"RELEASE_EXCLUDED_TESTS lists {repo_path}, but no "
                            "release_only pattern places it; add it, for the "
                            "Mac only, so the two lists agree")
        elif "windows" in placed[found]:
            problems.append(f"RELEASE_EXCLUDED_TESTS keeps {repo_path} to the "
                            "Mac, but release_only lists it for windows")
    return problems


def _requested_paths(paths: list[str], root: Path) -> list[str]:
    """The repository-relative names of paths ``tests_for_paths`` accepted."""
    project_root = root.resolve()
    names = []
    for value in paths:
        path = Path(value)
        candidate = path.resolve() if path.is_absolute() else (project_root / path).resolve()
        names.append(candidate.relative_to(project_root).as_posix())
    return names


def drop_unrelated_release_only(chosen: list[Path], requested: list[str],
                                groups: list[dict], machinery: list[str],
                                files: list[Path], root: Path
                                ) -> tuple[list[Path], list[Path]]:
    """Split ``for``'s answer into the tests to run and release-only tests held back.

    A release-only test stays when some requested path is release machinery
    (matches a ``release_paths`` pattern) or is that test file itself; with no
    such path every release-only test is held back, so an ordinary change never
    runs one."""
    release_files = set(release_only_files(groups, files)[0])
    if any(fnmatch.fnmatchcase(path, pattern)
           for path in requested for pattern in machinery):
        return chosen, []
    named = {(root.resolve() / path).resolve() for path in requested}
    kept = [p for p in chosen
            if p not in release_files or p.resolve() in named]
    return kept, [p for p in chosen if p not in kept]


def tests_for_paths(paths: list[str], files: list[Path], root: Path = ROOT, *,
                    reviewed_range: str | None = None,
                    broad_limit: int = 40,
                    omitted: list[Path] | None = None) -> list[Path]:
    """Select test files that name a changed file by path or file name.

    Folder sweeps do not name their discovered members and are intentionally
    absent; release verification covers those wider effects. The living files
    ``dev/PLANNING.md`` and ``CHANGELOG.md`` select nothing, for the same
    reason. AGENTS.md needs
    an explicit reviewed commit range so later commits cannot erase its diff.
    Its readers narrow to changed passages only when their broad list exceeds
    the runner limit; excluded readers are returned through ``omitted``.
    """
    needles: set[str] = set()
    python_stems: set[str] = set()
    governing_passages: list[str] = []
    governing_path_requested = False
    changed_test_files: set[Path] = set()
    resolved_range: str | None = None
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
        if path.as_posix() in _LIVING_FILES:
            continue
        if candidate in files:
            changed_test_files.add(candidate)
        if path.name == "AGENTS.md":
            governing_path_requested = True
            if not reviewed_range:
                raise ValueError("AGENTS.md selection requires --range BASE..HEAD")
            if resolved_range is None:
                resolved_range = _resolve_reviewed_range(root, reviewed_range)
            changed = _GIT_READ.run_git(
                str(root), ("diff", "--unified=0", resolved_range, "--",
                            path.as_posix()))
            if changed.state != "completed" or changed.returncode != 0:
                raise ValueError(
                    f"invalid reviewed range {reviewed_range!r}: Git diff unavailable")
            changed_text = changed.stdout.decode("utf-8", errors="replace")
            governing_passages.extend(
                " ".join(re.findall(r"[a-z0-9_]+", line.lower()))
                for line in changed_text.splitlines()
                if line.startswith(("+", "-"))
                and not line.startswith(("+++", "---"))
                and len(re.findall(r"[a-z0-9_]+", line.lower())) >= 5)
        elif path.as_posix() in _PATH_READERS:
            directly_selected_tests.update(
                project_root / reader for reader in _PATH_READERS[path.as_posix()]
                if project_root / reader in files
            )
            continue
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
        if (test in changed_test_files or test in directly_selected_tests
                or pins_changed_passage or names_requested_files
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


def _resolve_reviewed_range(root: Path, value: str) -> str:
    """Resolve a bounded two-ended review range to immutable commit IDs."""
    if (len(value) > 1024 or any(ord(char) < 32 or 0x7f <= ord(char) <= 0x9f
                                 for char in value)):
        raise ValueError("invalid reviewed range")
    match = re.fullmatch(r"(.+?)(\.\.\.?)(.+)", value)
    if match is None:
        raise ValueError("invalid reviewed range")
    left, separator, right = match.groups()
    if (not left or not right or left.startswith("-") or right.startswith("-")
            or left.endswith(".") or right.startswith(".")):
        raise ValueError("invalid reviewed range")
    if re.search(r"\.{2,3}", left) or re.search(r"\.{2,3}", right):
        raise ValueError("invalid reviewed range")

    endpoints = []
    for endpoint in (left, right):
        result = _GIT_READ.run_git(
            str(root), ("rev-parse", "--verify", "--end-of-options",
                        endpoint + "^{commit}"), output_limit=128)
        if result.state != "completed" or result.returncode != 0:
            raise ValueError(f"invalid reviewed range {value!r}: Git resolution unavailable")
        output = result.stdout
        if output.endswith(b"\n"):
            output = output[:-1]
        if (b"\n" in output or len(output) not in (40, 64)
                or re.fullmatch(rb"[0-9A-Fa-f]+", output) is None):
            raise ValueError(f"invalid reviewed range {value!r}: Git resolution unavailable")
        endpoints.append(output.decode("ascii"))
    return endpoints[0] + separator + endpoints[1]


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
    scoped.add_argument("--include-release-only", action="store_true",
                        help="keep release-only tests the changed paths do not "
                        "touch (for the certification reuse judgment)")
    scoped.add_argument("paths", nargs="+")
    cert = sub.add_parser("cert-files", help="print the test files Linux and "
                          "Windows run at certification")
    cert.add_argument("--host", choices=("linux", "windows"),
                      help="windows adds back the release-only files listed "
                      "for Windows; linux (the default) is the selection "
                      "Linux and Windows share")
    cert.add_argument("--write", metavar="PATH",
                      help="also save the lines to a new file at this absolute path")
    rel = sub.add_parser("release-only", help="print the test files that exist "
                         "only to protect Cairn's own release cut")
    rel.add_argument("--host", choices=RELEASE_HOSTS,
                     help="keep only the files this host runs at certification")
    args = ap.parse_args(argv)

    try:
        tiers = load_tiers(config)
        hosts = load_hosts(config) if args.verb in ("check", "cert-files") else []
        release = (load_release_only(config)
                   if args.verb in ("check", "cert-files", "release-only", "for")
                   else None)
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
        held: list[Path] = []
        if release is not None and not args.include_release_only:
            chosen, held = drop_unrelated_release_only(
                chosen, _requested_paths(args.paths, root), release[0],
                release[1], files, root)
        for path in chosen:
            print(path.relative_to(root) if path.is_relative_to(root) else path,
                  file=out)
        print(f"{len(chosen)} test files selected for the requested paths", file=err)
        if held:
            print(f"{len(held)} release-only test files held back, since no "
                  "changed path is release machinery (--include-release-only "
                  "keeps them): "
                  + ", ".join(p.relative_to(root).as_posix() if p.is_relative_to(root)
                              else str(p) for p in held), file=err)
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

    if args.verb == "cert-files":
        try:
            excluded = load_release_excluded(test_dir)
        except ValueError as exc:
            print(str(exc), file=err)
            return 2
        independent, _unplaced, _unused = classify(
            files, [{"name": "system_independent", "patterns": hosts}])
        release_hosts = (release_only_files(release[0], files)[0]
                         if release is not None else {})
        windows = args.host == "windows"

        def runs_on_this_host(path: Path) -> bool:
            if _repo_path(path, test_dir) in excluded or path.stem in independent:
                return False
            listed = release_hosts.get(path)
            return listed is None or (windows and "windows" in listed)

        lines = sorted(_repo_path(p, test_dir) for p in files
                       if runs_on_this_host(p))
        text = "".join(f"{line}\n" for line in lines)
        if args.write:
            target = Path(args.write)
            if not target.is_absolute():
                print(f"--write needs an absolute path: {args.write}", file=err)
                return 2
            try:
                with open(target, "x", encoding="utf-8", newline="\n") as handle:
                    handle.write(text)
            except FileExistsError:
                print(f"{target} already exists; choose a new path", file=err)
                return 2
            except OSError as exc:
                print(f"cannot write {target}: {exc}", file=err)
                return 2
        out.write(text)
        kept_release = sum(1 for p in files
                           if windows and "windows" in release_hosts.get(p, ()))
        print(f"cert-files: {len(lines)} of {len(files)} test files run on "
              f"{'Windows' if windows else 'Linux and Windows'} "
              f"({len(files) - len(lines)} left to the Mac: Cairn-only, "
              "release-only or system-independent)"
              + (f"; release-only files listed for Windows and kept: "
                 f"{kept_release}" if kept_release else ""), file=err)
        return 0

    if args.verb == "release-only":
        placed = release_only_files(release[0], files)[0] if release else {}
        chosen = sorted(
            _repo_path(p, test_dir) for p, listed in placed.items()
            if args.host is None or args.host in listed)
        for line in chosen:
            print(line, file=out)
        windows_too = sum(1 for listed in placed.values() if "windows" in listed)
        print(f"release-only: {len(chosen)} of {len(files)} test files"
              + (f" run on {args.host}" if args.host else
                 f" ({len(placed)} run on the Mac, {windows_too} of them also "
                 "on Windows)"), file=err)
        return 0

    if args.verb == "check":
        for stem in unplaced:
            print(f"UNPLACED {stem}.py: add a pattern for it to {config.name}", file=err)
        for name, pattern in unused:
            print(f"UNUSED   {name}: pattern {pattern!r} places no test file (matches none, or an earlier tier owns them)", file=err)
        problems = []
        if hosts or release is not None:
            try:
                excluded = load_release_excluded(test_dir)
            except ValueError as exc:
                print(str(exc), file=err)
                return 2
            if hosts:
                problems = host_problems(hosts, files, owner, excluded, test_dir)
            if release is not None:
                problems += release_only_problems(
                    release[0], files, hosts, excluded, test_dir)
        for problem in problems:
            print(f"HOSTS    {problem}", file=err)
        if unplaced or unused or problems:
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
