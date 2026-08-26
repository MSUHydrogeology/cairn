#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""The board: one row per active proposal and plan.

**It parses header blocks and nothing else.** Every field it prints is a line
an author wrote above the first `##` heading. It makes no judgment about
whether a status is legal, whether a review cleared, or what should happen
next -- those are questions for a reader holding the artifact, and a tool that
answered them would be asserting a conclusion it cannot support.

The artifact is authoritative; this view is derived and says so. It is
read-only and mutates nothing.

Usage:

    python tools/board.py            # active proposals and plans
    python tools/board.py --archive  # include the archives
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

#: Header fields worth a column, in print order. Anything else an author writes
#: in the header block is still theirs to write -- it simply has no column.
_FIELDS = ("Status", "Review", "Plan review", "Opened", "Source proposal")

_HEADER_FIELD_RE = re.compile(r"^\*\*(?P<name>[A-Za-z][A-Za-z /-]*)\*\*\s*:\s*(?P<value>.*)$")


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _encode(limit: int = 48):
    """The one terminal encoder, loaded from the session kernel.

    Values here come out of files any contributor can edit, so they are
    untrusted for display purposes. There is deliberately no local escape table
    to fall back on: a second, weaker path engages exactly when something is
    already wrong.
    """
    path = _repo_root() / "tools" / "session.py"
    spec = importlib.util.spec_from_file_location("_cairn_session_encoder", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def cell(value: str) -> str:
        text = module.encode_display(str(value))
        # Elision is layered outside the encoder, and the cut is taken from
        # encoded output so it cannot split a source character into a
        # half-escape that reads as something else.
        return text if len(text) <= limit else text[:limit - 1] + "\u2026"

    return cell


def _header_fields(text: str) -> Dict[str, str]:
    """The `**Field**: value` lines above the first `##` heading."""
    out: Dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        m = _HEADER_FIELD_RE.match(line.strip())
        if m:
            out[m.group("name").strip()] = m.group("value").strip()
    return out


def _rows(root: Path, include_archive: bool) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for kind, rel in (("proposal", "dev/proposals"), ("plan", "dev/plans")):
        base = root / rel
        if not base.is_dir():
            continue
        globs = [base.glob("*.md")]
        if include_archive and (base / "archive").is_dir():
            globs.append((base / "archive").glob("*.md"))
        for group in globs:
            for path in sorted(group):
                if path.name.startswith("_"):
                    continue
                fields = _header_fields(path.read_text(encoding="utf-8"))
                if not fields:
                    continue
                row = {"kind": kind, "artifact": path.stem,
                       "archived": "yes" if path.parent.name == "archive" else ""}
                row.update({f: fields.get(f, "") for f in _FIELDS})
                rows.append(row)
    return rows


def _render(rows: List[Dict[str, str]], encode) -> str:
    cols = ["kind", "artifact"] + [f for f in _FIELDS
                                   if any(r.get(f) for r in rows)] + ["archived"]
    if not any(r.get("archived") for r in rows):
        cols.remove("archived")
    lines = ["board: " + " | ".join(cols)]
    for r in rows:
        lines.append("board: " + " | ".join(encode(r.get(c, "")) for c in cols))
    lines.append(f"board: {len(rows)} row(s). Derived from header blocks; the "
                 f"artifact is authoritative.")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="board", description="One row per proposal and plan, from header "
                                  "blocks only. Read-only.")
    parser.add_argument("--archive", action="store_true",
                        help="Include archived artifacts.")
    parser.add_argument("--root", default=None, help="Repository root.")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.root else _repo_root()
    rows = _rows(root, args.archive)
    print(_render(rows, _encode()))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
