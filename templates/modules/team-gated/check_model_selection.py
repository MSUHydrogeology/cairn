#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Fidelity check for the Cairn model-selection module mapping.

Fails non-zero (exit code 1) if the adopter-local tier-to-model mapping
file (``dev/.cairn/model-selection-mapping.yml``) still contains the
unfilled ``FILL ME`` sentinel from the scaffold-seeded stub.

This is the machine gate for the model-selection module's R1 requirement:
the mapping MUST be filled before the capability-floor question is
considered addressed.

Usage::

    python scripts/check_model_selection.py
    python scripts/check_model_selection.py --mapping dev/.cairn/my-mapping.yml
    python scripts/check_model_selection.py --quiet  # silent on success

Exit codes::

    0  -- mapping file exists, contains no ``FILL ME`` sentinel, and (when
          PyYAML is available) parses as a non-empty YAML mapping
    1  -- mapping file exists but still contains ``FILL ME`` (needs filling)
    2  -- mapping file is missing (not yet seeded; scaffold may not have run)
    3  -- mapping is filled but is **not structurally valid YAML** (PyYAML
          present): the pass-the-gate-then-crash-the-loader gap.  When PyYAML
          is **not** installed, structural validation is skipped (graceful
          degradation) and this code is never returned.

Source
------

Installed by the Cairn ``model-selection`` module (Fold 5 of the
``foldback-drain-tooling`` proposal).  Seed-vs-gate sequencing: the
scaffold seeds ``dev/.cairn/model-selection-mapping.yml`` at install
time **carrying a ``FILL ME`` placeholder**, so this gate **fails
(non-zero) on a fresh, unfilled mapping** — forcing a fresh adopter to
record their real tier-to-model assignments (forced, not silent: the
silent-empty install is exactly the failure this module prevents, R1).
The scaffold install itself succeeds (the tree is not blocked); this is
a *standalone* adopter fidelity check (run it directly or wire it into
CI), so "not instantly red" means the install is not blocked — the gate
stays red until the placeholder is replaced.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

#: The sentinel string the scaffold stub contains.  The check is a
#: whole-file scan (case-sensitive, as a literal phrase), not just a
#: YAML-key check -- a partially-filled mapping that still carries one
#: ``FILL ME`` placeholder fails just as cleanly as a fully unfilled one.
_FILL_ME_RE = re.compile(r"\bFILL ME\b")

_DEFAULT_MAPPING_REL = "dev/.cairn/model-selection-mapping.yml"


def _structural_validate(
    text: str, mapping_path: Path, *, quiet: bool = False
) -> int:
    """Structurally validate the (already ``FILL ME``-free) mapping as YAML.

    Returns 0 when the mapping parses as a **non-empty YAML mapping**, OR when
    PyYAML is not installed -- structural validation is a *bonus*, not a hard
    dependency, so a dependency-bare adopter / CI degrades to the sentinel-only
    check rather than crashing with a raw ``ModuleNotFoundError`` (rollup #3b /
    External R2).  Returns 3 when PyYAML is present and the file is not valid
    YAML, or does not parse as a non-empty top-level mapping -- the
    pass-the-gate-then-crash-the-loader gap the sentinel scan alone misses.
    """
    try:
        import yaml  # optional: a bonus structural check, never a hard dep
    except ImportError:
        if not quiet:
            print(
                "check_model_selection: note -- structural validation skipped: "
                "PyYAML not installed (the FILL ME sentinel check still ran).",
                file=sys.stderr,
            )
        return 0
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        if not quiet:
            print(
                f"check_model_selection: FAIL -- {mapping_path} is filled but "
                f"is not valid YAML: {exc}",
                file=sys.stderr,
            )
        return 3
    if not isinstance(data, dict) or not data:
        if not quiet:
            print(
                f"check_model_selection: FAIL -- {mapping_path} is filled but "
                "did not parse as a non-empty YAML mapping (expected a "
                "top-level mapping).",
                file=sys.stderr,
            )
        return 3
    return 0


def check_mapping(mapping_path: Path, *, quiet: bool = False) -> int:
    """Check *mapping_path* for the ``FILL ME`` sentinel, then (when PyYAML is
    available) for structural YAML validity.

    Returns the exit code (0 = pass, 1 = needs filling, 2 = missing,
    3 = filled-but-malformed-YAML).  Prints a diagnostic unless *quiet* is True.
    """
    if not mapping_path.exists():
        if not quiet:
            print(
                f"check_model_selection: mapping file not found: {mapping_path}\n"
                "  Run `python bootstrap/scaffold.py install` (or "
                "`scaffold.py upgrade`) to seed it.",
                file=sys.stderr,
            )
        return 2

    text = mapping_path.read_text(encoding="utf-8", errors="replace")
    if _FILL_ME_RE.search(text):
        if not quiet:
            print(
                f"check_model_selection: FAIL -- {mapping_path} still contains "
                "\"FILL ME\" placeholder(s).\n"
                "  Fill the tier-to-model mapping before relying on the "
                "model-selection module.  See `dev/modules/model-selection.md` "
                "for the record schema.",
                file=sys.stderr,
            )
        return 1

    structural_rc = _structural_validate(text, mapping_path, quiet=quiet)
    if structural_rc != 0:
        return structural_rc

    if not quiet:
        print(f"check_model_selection: OK -- {mapping_path} is filled.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_model_selection",
        description=(
            "Fidelity check: fail non-zero if the model-selection mapping "
            "still contains 'FILL ME' placeholder(s)."
        ),
    )
    parser.add_argument(
        "--mapping", type=Path, default=None,
        help=(
            f"Path to the mapping file "
            f"(default: <repo-root>/{_DEFAULT_MAPPING_REL})."
        ),
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress output on success; only print on failure.",
    )
    args = parser.parse_args(argv)

    if args.mapping is not None:
        mapping_path = args.mapping
    else:
        # Resolve relative to the caller's cwd (typical adopter invocation).
        mapping_path = Path.cwd() / _DEFAULT_MAPPING_REL

    return check_mapping(mapping_path, quiet=args.quiet)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
