#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Fixed, contained operations for the installed count checker."""
from __future__ import annotations

import ast
import datetime
import json
import hashlib
import os
import re
import stat
import types
from dataclasses import dataclass
from pathlib import Path

#: The Cairn repo root (this file lives in ``<cairn>/scripts/``).
_CAIRN_ROOT = Path(__file__).resolve().parents[2]
_REPO_ROOT = _CAIRN_ROOT

_GIT_READ_SHA256 = "b67deb4e50eaee1e420d49af5ddac318aa110407bcd7c03d305091146cf15252"
_GIT_READ_MAX_BYTES = 256 * 1024


def _load_verified_git_read():
    """Execute only the fixed, caller-pinned helper buffer from this delivery."""
    path = os.path.abspath(os.path.join(_REPO_ROOT, "dev", "tools", "git_read.py"))
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


#: A rev-range accepted by :func:`git_commits_in_range`.  Deliberately
#: narrow -- ref characters plus the ``..`` / ``...`` range operators
#: only, so a range can never carry a shell metacharacter or a path
#: traversal.  (git itself is invoked ``shell=False`` regardless; this is
#: defence in depth.)
_REV_RANGE_RE = re.compile(r'^[0-9A-Za-z._/~^-]+\.\.\.?[0-9A-Za-z._/~^-]+$')


@dataclass(frozen=True)
class Invariant:
    """A live count re-measured *today* and compared to the annotated
    number; a mismatch is drift.

    ``fn`` is a key into :data:`MEASURE_FNS` (the closed allowlist);
    ``root`` is a code-given directory (a project root or a sibling
    checkout) and ``target`` a root-relative path (or, for
    ``git_commits_in_range``, a rev-range).
    """

    root: Path
    fn: str
    target: str


@dataclass(frozen=True)
class Snapshot:
    """A measurement frozen *at a moment*, recorded as evidence and
    **never re-measured**.  ``verify_counts`` confirms the annotated
    number equals :attr:`value` and that the verified line carries the
    ISO :attr:`as_of` date -- re-running would erase the evidence the
    snapshot is."""

    value: int
    as_of: str  # ISO YYYY-MM-DD


def _resolve_within(root: Path, target: str) -> Path:
    """Resolve ``root/target`` and refuse a result that escapes ``root``.

    Both sides are fully resolved (symlinks followed), so a symlink or a
    ``..`` segment inside *target* that would leave the tree is caught
    (containment).  *root* must exist (the caller -- ``verify_counts``
    -- gates an absent root into a visible skip before reaching here).
    """
    root_real = root.resolve(strict=True)
    candidate = (root / target).resolve()
    if not candidate.is_relative_to(root_real):
        raise ValueError(
            f'measurement target {target!r} resolves to {candidate}, which '
            f'escapes its root {root_real} -- refusing (containment, IR3)'
        )
    return candidate


def count_lines(root: Path, target: str) -> int:
    """Number of newline-terminated lines in the contained ``target`` file."""
    path = _resolve_within(root, target)
    if not path.is_file():
        raise FileNotFoundError(f'count_lines: not a file: {path}')
    with path.open(encoding='utf-8', errors='replace') as handle:
        return sum(1 for _ in handle)


def count_files(root: Path, target: str) -> int:
    """Number of files (not directories) under the contained ``target``
    directory, excluding dot-entries (``.git`` and friends).  Bounded by
    the target subtree -- a registered target is a small dir."""
    path = _resolve_within(root, target)
    if not path.is_dir():
        raise NotADirectoryError(f'count_files: not a directory: {path}')
    total = 0
    for item in path.rglob('*'):
        if any(part.startswith('.') for part in item.relative_to(path).parts):
            continue
        if not item.resolve().is_relative_to(root.resolve(strict=True)):
            raise ValueError("child escapes root")
        if item.is_file():
            total += 1
    return total


def count_defs(root: Path, target: str) -> int:
    """Number of ``def`` / ``async def`` / ``class`` statements in the
    contained ``target`` Python file (every level, via :mod:`ast`)."""
    path = _resolve_within(root, target)
    if not path.is_file():
        raise FileNotFoundError(f'count_defs: not a file: {path}')
    tree = ast.parse(path.read_text(encoding='utf-8', errors='replace'))
    return sum(
        1 for node in ast.walk(tree)
        if isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        )
    )


def git_commits_in_range(root: Path, target: str) -> int:
    """Number of commits in the rev-range ``target`` (e.g. ``A..B``) in
    the git repo at ``root``.  Runs ``git`` with a **fixed argument
    vector** (``shell=False``) and a validated range -- no shell, no
    document-supplied command."""
    if target.startswith("-") or not _REV_RANGE_RE.fullmatch(target):
        raise ValueError(
            f'git_commits_in_range: unsafe rev-range {target!r} -- expected '
            f'`<ref>..<ref>` / `<ref>...<ref>` ref characters only'
        )
    root_real = root.resolve(strict=True)
    version = _GIT_READ.read_version(str(root_real))
    match = re.match(rb"git version (\d+)\.(\d+)", version.stdout)
    if version.state != "completed" or version.returncode != 0 or not match or tuple(map(int, match.groups())) < (2, 45):
        raise RuntimeError("Git 2.45 or later required")
    top = _GIT_READ.run_git(str(root_real), ("rev-parse", "--show-toplevel"))
    if top.state != "completed" or top.returncode != 0 or Path(os.fsdecode(top.stdout.strip())).resolve() != root_real:
        raise RuntimeError("selected root is not Git worktree root")
    result = _GIT_READ.run_git(
        str(root_real), ("log", "--oneline", target, "--"))
    if result.state != "completed" or result.returncode != 0:
        raise RuntimeError("git_commits_in_range: Git history unavailable")
    return sum(1 for line in result.stdout.splitlines() if line.strip())


MEASURE_FNS = {
    "count_lines": count_lines,
    "count_files": count_files,
    "count_defs": count_defs,
    "git_commits_in_range": git_commits_in_range,
}


def measure(invariant: Invariant) -> int:
    return MEASURE_FNS[invariant.fn](invariant.root, invariant.target)


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate registry key")
        result[key] = value
    return result


def load_registry():
    project = _REPO_ROOT.resolve(strict=True)
    registry_path = (project / "dev/.cairn/measurements.json").resolve(strict=True)
    if not registry_path.is_relative_to(project):
        raise ValueError("registry escapes project")
    data = json.loads(registry_path.read_text(encoding="utf-8"), object_pairs_hook=_unique)
    if not isinstance(data, dict):
        raise ValueError("registry must be an object")
    registry = {}
    for key, entry in data.items():
        if not re.fullmatch(r"[\w-]+", key) or not isinstance(entry, dict):
            raise ValueError("invalid registry entry")
        kind = entry.get("kind")
        if kind == "snapshot" and set(entry) == {"kind", "value", "as_of"}:
            value, date = entry["value"], entry["as_of"]
            if type(value) is not int or value < 0 or not isinstance(date, str):
                raise ValueError("invalid snapshot")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                raise ValueError("invalid snapshot date")
            datetime.date.fromisoformat(date)
            registry[key] = Snapshot(value, date)
        elif kind == "invariant" and set(entry) in ({"kind", "fn", "target"}, {"kind", "fn", "target", "root"}):
            fn, target, root = entry["fn"], entry["target"], entry.get("root", ".")
            if not all(isinstance(x, str) for x in (fn, target, root)) or fn not in MEASURE_FNS:
                raise ValueError("invalid invariant")
            root_path = Path(root)
            if root_path.is_absolute():
                raise ValueError("root must be project-relative")
            resolved = (project / root_path).resolve()
            if not resolved.is_relative_to(project):
                raise ValueError("root escapes project")
            registry[key] = Invariant(resolved, fn, target)
        else:
            raise ValueError("invalid registry entry fields")
    return registry
