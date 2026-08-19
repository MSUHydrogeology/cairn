#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Work-intent engine — shared-core leaf.

Repo-root anchoring plus the path helpers used across the record-I/O,
identity, conflict-check, CLI, and git-hook-install subsystems. This is the
leaf of the ``_intent/`` dependency DAG: stdlib-only, no intra-package imports.
"""
from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import List, Optional

#: Repo root: the launcher/facade installs to ``<repo>/tools/intent.py`` and this
#: engine package sits at ``<repo>/tools/_intent/``, so the repo root is **two**
#: directories above this file. (The pre-split single file lived one level
#: shallower at ``tools/intent.py`` and used ``parents[1]``; moving the body into
#: the ``_intent/`` package shifts the anchor to ``parents[2]`` so the value is
#: computed correctly at the leaf rather than patched in by the facade.)
_REPO_ROOT = Path(__file__).resolve().parents[2]

#: Default location of the active intent log (gitignored).
INTENTS_LOG_PATH = _REPO_ROOT / "dev" / "intents.jsonl"


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
