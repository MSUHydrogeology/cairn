#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""The code-side measurement registry for ``verify_counts.py``.

The **live-invariant** leg of the three-kind numeric-claim discipline
(`claim-check` module doctrine): a count cited in a doc as present fact,
prone to drift, is *registered here* and *re-measured* by
``verify_counts.py`` rather than trusted from memory.  The other two
kinds need no code -- a decision-irrelevant count is approximated, a
dated snapshot is recorded once and never re-measured.

**Cairn-maintainer-only.**  This registry and ``verify_counts.py`` are a
dogfood tool: they are **not** installed into adopter trees (not in
``_CORE_MAPPINGS``) and add nothing to an adopter's operational kernel.
They run on Cairn's own docs.

Security by construction
------------------------
A document annotation (``<!-- verify: <key> -->``) carries **only a
registry key** -- never a path, never a command.  The key maps here to a
code-controlled measurement whose ``root`` and ``fn`` are fixed in this
file and reviewed once.  ``fn`` is one of a **closed allowlist**.  Every
path measurement is **contained**: the resolved target (symlinks
followed) must stay within the resolved ``root`` -- a symlink or glob
that escapes the root is refused.  ``git_commits_in_range`` runs git with
a **fixed argument vector** (``shell=False``) and a validated rev-range,
never a shell string.  There is therefore no document-supplied path, no
Markdown execution, and no shell-injection surface.

Scope bound: no cache, no incremental layer.  Each
measurement is a cheap, bounded stdlib scan or a bounded ``git log``
range, and the registry stays small (soft cap ~10 keys).  If it ever
wants a cache to stay fast, that is the curation-tax kill-signal -- shrink
or freeze the registry, do not accelerate it.
"""
from __future__ import annotations

import ast
import hashlib
import os
import re
import stat
import types
from dataclasses import dataclass
from pathlib import Path

#: The Cairn repo root (this file lives in ``<cairn>/scripts/``).
_CAIRN_ROOT = Path(__file__).resolve().parents[1]
_REPO_ROOT = _CAIRN_ROOT

_GIT_READ_SHA256 = "a1c54924ef70e15d583ed265aba1fbaa3195554f7e29e36fdd726cb7cc322cec"
_GIT_READ_MAX_BYTES = 256 * 1024


def _load_verified_git_read():
    """Execute only the fixed, caller-pinned helper buffer from this delivery."""
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
    return sum(
        1 for item in path.rglob('*')
        if item.is_file() and not any(
            part.startswith('.') for part in item.relative_to(path).parts
        )
    )


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
    if not _REV_RANGE_RE.match(target):
        raise ValueError(
            f'git_commits_in_range: unsafe rev-range {target!r} -- expected '
            f'`<ref>..<ref>` / `<ref>...<ref>` ref characters only'
        )
    root_real = root.resolve(strict=True)
    result = _GIT_READ.run_git(
        str(root_real), ("log", "--oneline", target))
    if result.state != "completed" or result.returncode != 0:
        raise RuntimeError("git_commits_in_range: Git history unavailable")
    return sum(1 for line in result.stdout.splitlines() if line.strip())


def count_preset_modules(root: Path, target: str) -> int:
    """Number of modules the scaffold resolves for the governance preset
    ``target`` (e.g. ``solo-greenfield``).

    Unlike the path-scan fns above, this **imports Cairn's own preset
    resolver** (``_scaffold.expand_preset``) and calls it in-process.  It is
    *resolve-only* -- ``expand_preset`` reads a profile dict and returns a
    module roster; it writes nothing and installs nothing.  The preset name
    ``target`` is **code-fixed in the REGISTRY**, never document-supplied (a
    doc annotation carries only the registry key), so this fn -- like the
    rest of the allowlist -- has no document-supplied path or command.  The
    only widening over the file-scan fns is that it imports Cairn's trusted
    engine; that is a Maintainer-accepted trade for guarding a count the
    quickstart mirrors but that no bounded file scan can derive."""
    import sys
    bootstrap = (root / 'bootstrap').resolve()
    if str(bootstrap) not in sys.path:
        sys.path.insert(0, str(bootstrap))
    from _scaffold import expand_preset  # Cairn's own engine; resolve-only
    modules, _summary = expand_preset({'preset': target})
    return len(modules)


#: The closed allowlist of measurement functions.  An ``Invariant.fn`` is
#: resolved here; a key absent from this map is refused by :func:`measure`.
MEASURE_FNS = {
    'count_lines': count_lines,
    'count_files': count_files,
    'count_defs': count_defs,
    'git_commits_in_range': git_commits_in_range,
    'count_preset_modules': count_preset_modules,
}


def measure(invariant: Invariant) -> int:
    """Re-measure an :class:`Invariant` via its allowlisted ``fn``.

    Raises ``KeyError`` if ``fn`` is not in :data:`MEASURE_FNS` (a
    registry-author mistake; never reachable from a document), and
    propagates the measurement function's own errors (containment
    refusal, missing target)."""
    try:
        fn = MEASURE_FNS[invariant.fn]
    except KeyError:
        raise KeyError(
            f'measurement fn {invariant.fn!r} is not in the allowlist '
            f'{sorted(MEASURE_FNS)} -- registry error'
        ) from None
    return fn(invariant.root, invariant.target)


#: The seed registry -- only the headline sizes that already drift across
#: Cairn's docs (soft cap ~10 keys).  Keyed by a short, stable name a
#: doc annotates with ``<!-- verify: <key> -->``.
#:
#: ``claim_check_watch_file_lines`` is the canonical drift case: the
#: complexity-debt audit tracks ``claim_check.py`` as a watch file and its
#: size is re-quoted across docs as it changes (the count-soft-flag
#: retirement just shrank it ~876 -> ~786).
REGISTRY: dict[str, Invariant | Snapshot] = {
    'claim_check_watch_file_lines': Invariant(
        root=_CAIRN_ROOT,
        fn='count_lines',
        target='templates/modules/default-on/claim_check.py',
    ),
    # The `solo-greenfield` module count the quickstart states. Guards the
    # adopter-entry drift the 2026-06-12 audit found (its module half) under
    # the check_cairn docs lens, complementing the install-path pytest gate in
    # test_quickstart_sequence.py (which also guards the slot count).
    'solo_greenfield_module_count': Invariant(
        root=_CAIRN_ROOT,
        fn='count_preset_modules',
        target='solo-greenfield',
    ),
}
