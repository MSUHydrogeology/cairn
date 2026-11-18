#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Fidelity check for the Cairn model-selection module mapping.

Fails non-zero (exit code 1) if the adopter-local tier-to-model mapping
file (``dev/.cairn/model-selection-mapping.yml``) still contains the
unfilled ``FILL ME`` sentinel on a non-comment line or in a parsed YAML
value, or if it has no mapping rows.

Full-line comments (lines whose first non-space character is ``#``, after
splitting on YAML 1.1 line breaks) are skipped so explanatory header and
example comments in the seeded stub do not cause a filled mapping to fail.
Trailing comments on value lines are still scanned.

When PyYAML is available, the parsed document is also walked once per
object (strings, dictionary keys, set members, and bytes decoded as text)
for ``FILL ME``, YAML merge keys (``<<``) are refused, and ``mapping``
must be a non-empty list.  When PyYAML is not installed, structural
validation is skipped and the bare line scan requires at least one
non-comment row line.  On that bare path, a value whose ``FILL ME`` is
not spelled out on one non-comment line (such as a block scalar, a value
folded over lines, a line continuation, an escape, or a tag) reads as
filled, and so does a row-shaped line that is not an item of ``mapping``.

This is the machine gate for the model-selection module's core requirement:
the mapping MUST be filled before the capability-floor question is
considered addressed.

Usage::

    python scripts/check_model_selection.py
    python scripts/check_model_selection.py --mapping dev/.cairn/my-mapping.yml
    python scripts/check_model_selection.py --quiet  # silent on success

Exit codes::

    0  -- mapping file exists, contains no ``FILL ME`` sentinel outside
          full-line comments, has at least one row, and (when PyYAML is
          available) parses as a valid YAML mapping with a non-empty
          ``mapping`` list
    1  -- mapping file exists but still contains ``FILL ME`` or has no rows
          (needs filling)
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
silent-empty install is exactly the failure this module prevents).
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

#: The sentinel string the scaffold stub contains.  The line scan skips
#: full-line comments (leading spaces then ``#``) and checks every other
#: line for this case-sensitive phrase, so a partially-filled mapping or a
#: trailing comment carrying ``FILL ME`` still fails cleanly.
_FILL_ME_RE = re.compile(r"\bFILL ME\b")

#: YAML 1.1 line breaks: CRLF, LF, CR, NEL (U+0085), LS (U+2028), PS (U+2029).
#: Form feed and vertical tab are not YAML line breaks.
_LINE_SPLIT_RE = re.compile(r"\r\n|[\n\r\x85\u2028\u2029]")

#: Bare-path row pattern: anchored at line start (after spaces), matching a
#: block row, a flow item, a single- or double-quoted ``tier`` key, or a
#: one-line ``mapping: [{tier: ...}]`` list whose first key is ``tier``.
_ROW_LINE_RE = re.compile(
    r'^ *(?:mapping *: *\[ *|- +)?(?:\{ *)?(?:"tier"|\'tier\'|tier) *:'
)

_DEFAULT_MAPPING_REL = "dev/.cairn/model-selection-mapping.yml"


def _non_comment_lines(text: str) -> list[str]:
    """Split *text* on YAML 1.1 line breaks and drop full-line comments
    (only ASCII space before ``#`` makes a comment)."""
    return [
        line
        for line in _LINE_SPLIT_RE.split(text)
        if not line.lstrip(" ").startswith("#")
    ]


def _value_contains_fill_me(root: object) -> bool:
    """Walk *root* with an explicit stack, visiting each object at most once
    by identity.  Scans strings, dictionary keys and values, list/tuple/set
    members, and bytes decoded as UTF-8 text."""
    stack: list[object] = [root]
    visited: set[int] = set()
    while stack:
        node = stack.pop()
        obj_id = id(node)
        if obj_id in visited:
            continue
        visited.add(obj_id)
        if isinstance(node, str):
            if _FILL_ME_RE.search(node):
                return True
        elif isinstance(node, (bytes, bytearray)):
            if _FILL_ME_RE.search(node.decode("utf-8", errors="replace")):
                return True
        elif isinstance(node, dict):
            for k, v in node.items():
                stack.append(v)
                stack.append(k)
        elif isinstance(node, (list, tuple, set, frozenset)):
            stack.extend(node)
    return False


def _print_fill_me_failure(mapping_path: Path, *, quiet: bool) -> None:
    if not quiet:
        print(
            f"check_model_selection: FAIL -- {mapping_path} still contains "
            "\"FILL ME\" placeholder(s).\n"
            "  Fill the tier-to-model mapping before relying on the "
            "model-selection module.  See `dev/modules/model-selection.md` "
            "for the record schema.",
            file=sys.stderr,
        )


def _print_no_rows_failure(mapping_path: Path, *, quiet: bool) -> None:
    if not quiet:
        print(
            f"check_model_selection: FAIL -- {mapping_path} has no rows "
            "under `mapping`.\n"
            "  Record at least one tier-to-model row before relying on the "
            "model-selection module.  See `dev/modules/model-selection.md` "
            "for the record schema.",
            file=sys.stderr,
        )


def _structural_validate(
    text: str,
    non_comment: list[str],
    mapping_path: Path,
    *,
    quiet: bool = False,
) -> int:
    """Structurally validate the mapping as YAML when PyYAML is available,
    scanning every parsed value for ``FILL ME`` and checking that ``mapping``
    is a non-empty list.

    When PyYAML is not installed, structural validation is skipped with a note
    and the bare row-line check decides whether at least one row is present.
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
        if not any(_ROW_LINE_RE.search(line) for line in non_comment):
            _print_no_rows_failure(mapping_path, quiet=quiet)
            return 1
        return 0

    class _NoMergeSafeLoader(yaml.SafeLoader):
        def flatten_mapping(self, node: object) -> None:
            for key_node, _ in getattr(node, "value", ()):
                if getattr(key_node, "tag", None) == "tag:yaml.org,2002:merge":
                    raise yaml.constructor.ConstructorError(
                        None,
                        None,
                        "YAML merge keys ('<<') are not permitted in a "
                        "model-selection mapping",
                        None,
                    )
            super().flatten_mapping(node)

    try:
        loader = _NoMergeSafeLoader(text)
        try:
            data = loader.get_single_data()
        finally:
            loader.dispose()
    except RecursionError:
        if not quiet:
            print(
                f"check_model_selection: FAIL -- {mapping_path} is filled but "
                "is not valid YAML: maximum nesting depth exceeded.",
                file=sys.stderr,
            )
        return 3
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
    if _value_contains_fill_me(data):
        _print_fill_me_failure(mapping_path, quiet=quiet)
        return 1
    rows = data.get("mapping")
    if not isinstance(rows, list) or not rows:
        _print_no_rows_failure(mapping_path, quiet=quiet)
        return 1
    return 0


def check_mapping(mapping_path: Path, *, quiet: bool = False) -> int:
    """Check *mapping_path* for the ``FILL ME`` sentinel on non-comment lines,
    then (when PyYAML is available) for structural YAML validity, parsed-value
    ``FILL ME`` placeholders, and at least one row under ``mapping``.

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
    non_comment = _non_comment_lines(text)
    if any(_FILL_ME_RE.search(line) for line in non_comment):
        _print_fill_me_failure(mapping_path, quiet=quiet)
        return 1

    structural_rc = _structural_validate(
        text, non_comment, mapping_path, quiet=quiet
    )
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
            "still contains 'FILL ME' placeholder(s) or has no rows."
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
