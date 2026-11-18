# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
"""Locate the Cairn repository for its tests."""
from pathlib import Path


def repository_root(start: Path) -> Path:
    """Find the nearest ancestor containing Cairn's repository marker."""
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".zenodo.json").is_file():
            return candidate
    raise FileNotFoundError(f"Cairn repository marker not found from {start}")
