#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Work-intent engine — shared-core leaf.

Repo-root anchoring plus the path helpers used across the record-I/O,
identity, conflict-check, CLI, and git-hook-install subsystems. This is the
leaf of the ``_intent/`` dependency DAG: stdlib-only, no intra-package imports.
"""
from __future__ import annotations

import os
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import List, Optional

#: Repo root: the launcher/facade installs to ``<repo>/tools/intent.py`` and this
#: engine package sits at ``<repo>/tools/_intent/``, so the repo root is **two**
#: directories above this file. (The pre-split single file lived one level
#: shallower at ``tools/intent.py`` and used ``parents[1]``; moving the body into
#: the ``_intent/`` package shifts the anchor to ``parents[2]`` so the value is
#: computed correctly at the leaf rather than patched in by the facade.)
_REPO_ROOT = Path(__file__).absolute().parents[2]


def _has_link_or_reparse(path: Path) -> bool:
    """Check every existing component without following it first."""
    # absolute() retains both links and '..' for the component walk.
    path = path.absolute()
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        try:
            info = os.lstat(current)
        except OSError:
            return True
        if stat.S_ISLNK(info.st_mode):
            return True
        attrs = getattr(info, "st_file_attributes", 0)
        if attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
            return True
    return False


def _absolute_pointer(value: str, base: Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = base / path
    return path


def _path_key(path: Path) -> str:
    return os.path.normcase(os.path.normpath(str(Path(os.path.abspath(path)))))


def _shared_intents_path() -> tuple[Path, Optional[str]]:
    """Use the main checkout log only for a fully cross-checked worktree."""
    root = _REPO_ROOT
    local = root / "dev" / "intents.jsonl"
    dotgit = root / ".git"
    try:
        if (_has_link_or_reparse(root) or dotgit.is_symlink()
                or (dotgit.exists() and _has_link_or_reparse(dotgit))):
            return local, "checkout or .git path contains a link or reparse point"
        mode = os.lstat(dotgit).st_mode
        if stat.S_ISDIR(mode):
            return local, None
        if not stat.S_ISREG(mode):
            return local, ".git is not a directory or regular pointer file"
        lines = dotgit.read_text(encoding="utf-8").splitlines()
        if len(lines) != 1 or not lines[0].startswith("gitdir: "):
            return local, ".git pointer is malformed"
        admin = _absolute_pointer(lines[0][len("gitdir: "):], root)
        if _has_link_or_reparse(admin) or not admin.is_dir():
            return local, "worktree administration path is missing or linked"
        admin = Path(os.path.abspath(admin))
        commondir_file = admin / "commondir"
        if _has_link_or_reparse(commondir_file) or not commondir_file.is_file():
            return local, "worktree commondir is missing or linked"
        common_text = commondir_file.read_text(encoding="utf-8").strip()
        common = _absolute_pointer(common_text, admin)
        if _has_link_or_reparse(common) or not common.is_dir():
            return local, "common Git directory is missing or linked"
        common = Path(os.path.abspath(common))
        expected_parent = common / "worktrees"
        if _path_key(admin.parent) != _path_key(expected_parent) or not admin.name:
            return local, "administration path is not <common>/worktrees/<name>"
        backpointer = admin / "gitdir"
        if _has_link_or_reparse(backpointer) or not backpointer.is_file():
            return local, "worktree back-pointer is missing or linked"
        back = _absolute_pointer(backpointer.read_text(encoding="utf-8").strip(), admin)
        if _has_link_or_reparse(back):
            return local, "worktree back-pointer target is missing or linked"
        if _path_key(back) != _path_key(dotgit):
            return local, "worktree back-pointer does not name this .git file"
        main = common.parent
        if common.name != ".git" or _path_key(main / ".git") != _path_key(common):
            return local, "common directory is not the main checkout's .git"
        dev = main / "dev"
        if _has_link_or_reparse(main) or _has_link_or_reparse(dev) or not dev.is_dir():
            return local, "main checkout is missing or its dev directory is absent/linked"
        return main / "dev" / "intents.jsonl", None
    except (OSError, UnicodeError, ValueError):
        return local, "Git pointer chain could not be verified"

#: Default location of the active intent log (gitignored).
INTENTS_LOG_PATH, _INTENTS_LOG_FALLBACK = _shared_intents_path()
_SHARED_INTENTS_LOG_PATH = (
    INTENTS_LOG_PATH
    if INTENTS_LOG_PATH != _REPO_ROOT / "dev" / "intents.jsonl" else None
)
if _INTENTS_LOG_FALLBACK:
    sys.stderr.write(f"intent: using checkout-local claims log: {_INTENTS_LOG_FALLBACK}\n")


def normalize_path(path: str, *, repo_root: Optional[Path] = None) -> str:
    """Normalize ``path`` to repo-root-relative, forward-slash, no
    leading ``./`` or trailing slashes.

    Absolute paths inside the repo are rewritten repo-root-relative;
    paths outside are preserved as absolute (POSIX-style).  Forward
    slashes on every platform; leading ``./`` and trailing ``/``
    stripped; backslashes converted.
    """
    if not path:
        return ""
    root = repo_root if repo_root is not None else _REPO_ROOT
    cleaned = path.replace("\\", "/").strip()
    while cleaned.startswith("./"):
        cleaned = cleaned[2:]
    cleaned = cleaned.rstrip("/")
    if not cleaned:
        return ""
    abs_candidate = Path(cleaned)
    if abs_candidate.is_absolute():
        try:
            rel = abs_candidate.resolve().relative_to(root.resolve())
        except ValueError:
            return PurePosixPath(abs_candidate).as_posix()
        return PurePosixPath(rel).as_posix()
    return PurePosixPath(cleaned).as_posix()


def _read_nul_delimited_paths(path: str) -> List[str]:
    """Read a NUL-delimited path file (``git diff-tree ... -z`` output)."""
    p = Path(path)
    if not p.exists():
        return []
    raw = p.read_bytes()
    if not raw:
        return []
    parts = raw.split(b"\x00")
    if parts and parts[-1] == b"":
        parts = parts[:-1]
    return [b.decode("utf-8", errors="replace") for b in parts]
