#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""The board: one row per active proposal and plan.

**It parses header blocks and nothing else, bar two reads under
`--maintainer`:** the rows of `dev/PLANNING.md` that carry one fixed marker, and
the active plan bodies, for two fixed words. Every field it prints is a line an
author wrote: above the first `##` heading, or, under `--maintainer`, in a
marked board row. It makes no judgment about whether a status is legal, whether
a review cleared, or what should happen next -- those are questions for a reader
holding the artifact, and a tool that answered them would be asserting a
conclusion it cannot support. `--maintainer` lists what authors *declared* as
waiting on the Maintainer, and names the plans that mention a fence but declare
nothing; it never decides whether a wait is over.

The artifact is authoritative; this view is derived and says so. It is
read-only and mutates nothing.

Usage:

    python tools/board.py               # active proposals and plans
    python tools/board.py --archive     # include the archives
    python tools/board.py --maintainer  # what waits on the Maintainer
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
_FIELDS = ("Status", "Review", "Plan review", "Opened", "Source proposal",
           "Waiting on Maintainer")

_HEADER_FIELD_RE = re.compile(r"^\*\*(?P<name>[A-Za-z][A-Za-z /-]*)\*\*\s*:\s*(?P<value>.*)$")

#: The one line an author writes to say an item waits on the Maintainer: a
#: header field in a plan or change note, a marked row in `dev/PLANNING.md`.
_WAIT = "Waiting on Maintainer"

#: Words that mark a chunk only the Maintainer can release. A plan that says one
#: but declares no wait is named on the advisory line, never listed as waiting.
_FENCE_WORDS = ("MAINTAINER-GATED", "MAINTAINER-ONLY")

#: A status that hands the item to the Maintainer. Matched on its leading word,
#: so a note after it (`awaiting-decision -- note`) still lists: a silent drop
#: is the failure the list exists to remove.
_AWAITING_DECISION_RE = re.compile(r"^awaiting-decision(?![A-Za-z0-9_])")

#: Leading spaces and at most one list bullet, ahead of a board row's marker.
_ROW_BULLET_RE = re.compile(r"^ *(?:[*-] )?")


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


def _artifacts(root: Path, include_archive: bool):
    """`(kind, path, text)` for each proposal and plan, in print order."""
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
                yield kind, path, path.read_text(encoding="utf-8")


def _rows(root: Path, include_archive: bool) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for kind, path, text in _artifacts(root, include_archive):
        fields = _header_fields(text)
        if not fields:
            continue
        row = {"kind": kind, "artifact": path.stem,
               "archived": "yes" if path.parent.name == "archive" else ""}
        row.update({f: fields.get(f, "") for f in _FIELDS})
        rows.append(row)
    return rows


def _waiting(root: Path) -> Dict[str, object]:
    """What authors declared as waiting on the Maintainer.

    Active artifacts only: an archived file is a record, so the archives never
    count. An artifact is listed once however many ways it qualifies, and a
    Waiting line with no text still counts as declared, so a blanked line stays
    visible. A board row qualifies only in the row form -- after leading spaces
    and one optional bullet, `**Waiting on Maintainer**: <what>` -- read by the
    same rule as a header field, so a mention in a sentence or in backticks is
    not a marker.
    """
    entries: List[Dict[str, str]] = []
    fence_only: List[str] = []
    for kind, path, text in _artifacts(root, include_archive=False):
        fields = _header_fields(text)
        declared = _WAIT in fields
        decision = bool(_AWAITING_DECISION_RE.match(fields.get("Status", "")))
        if decision or declared:
            entries.append({"kind": kind, "artifact": path.stem,
                            "reason": "awaiting-decision" if decision else "declared",
                            "text": fields.get(_WAIT, "")})
        if kind == "plan" and not declared and any(w in text for w in _FENCE_WORDS):
            fence_only.append(path.stem)
    planning = root / "dev" / "PLANNING.md"
    has_planning = planning.is_file()
    if has_planning:
        lines = planning.read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(lines, 1):
            m = _HEADER_FIELD_RE.match(_ROW_BULLET_RE.sub("", line, count=1).strip())
            if m and m.group("name").strip() == _WAIT:
                entries.append({"kind": "roadmap",
                                "artifact": f"dev/PLANNING.md:{number}",
                                "reason": "declared",
                                "text": m.group("value").strip()})
    return {"entries": entries, "fence_only": fence_only,
            "has_planning": has_planning}


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


def _render_waiting(found: Dict[str, object], encode) -> str:
    cols = ["kind", "artifact", "reason", "text"]
    entries = found["entries"]
    lines = ["board: " + " | ".join(cols)]
    for e in entries:
        lines.append("board: " + " | ".join(encode(e[c]) for c in cols))
    lines.append(f"board: {len(entries)} waiting on the Maintainer, as authors "
                 f"declared. The artifact or row is authoritative.")
    names = ", ".join(encode(n) for n in found["fence_only"]) or "none"
    lines.append("board: advisory -- plans that mention a fence but declare no "
                 f"wait (open each): {names}")
    lines.append("board: not listed -- pushes (git status shows them) and "
                 "anything no artifact or row declares.")
    if not found["has_planning"]:
        lines.append("board: dev/PLANNING.md is missing -- no board rows were read.")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="board", description="One row per proposal and plan, read from "
                                  "their header blocks. Read-only.")
    parser.add_argument("--archive", action="store_true",
                        help="Include archived artifacts. Has no effect on "
                             "--maintainer.")
    parser.add_argument("--maintainer", action="store_true",
                        help="List what waits on the Maintainer instead: "
                             "proposals awaiting a decision, plans and "
                             "dev/PLANNING.md rows that declare a wait. Also "
                             "names plans that mention a fence but declare "
                             "none. Reads active artifacts only.")
    parser.add_argument("--root", default=None, help="Repository root.")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.root else _repo_root()
    if args.maintainer:
        print(_render_waiting(_waiting(root), _encode()))
        return 0
    rows = _rows(root, args.archive)
    print(_render(rows, _encode()))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
