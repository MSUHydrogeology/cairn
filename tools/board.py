#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""The board: one row per active proposal and plan, plus a JSON data form.

It reads the header block (`**Field**: value` lines above the first `##`
heading) and the title line (`# ` above the first `##` heading) of each
proposal and plan, the rows of `dev/PLANNING.md` that carry one fixed wait
marker, and, under `--maintainer`, the active plan bodies for two fixed fence
words. `--json` prints what authors wrote in those header lines, the title
line and the marked roadmap rows (`schema` `"cairn-board/1"`), and derives no
value. It makes no judgment about whether a review cleared or what should
happen next -- those are questions for a reader holding the artifact, and a
tool that answered them would be asserting a conclusion it cannot support. The
one lookup it does make is whether an active artifact's status opens with a
word from the published vocabulary (held in `tools/session.py`, so there is one
list); if not, one advisory line names it as retired or unknown. That line only
warns: every artifact is still listed, archived records are never flagged, and
`--json` is unchanged. `--maintainer` lists what authors *declared* as
waiting on the Maintainer, and names the plans that mention a fence but
declare nothing; it never decides whether a wait is over.

The artifact is authoritative; this view is derived and says so. It is
read-only and mutates nothing. A symbolic link is never read and is named in
the output.

Usage:

    python tools/board.py               # active proposals and plans
    python tools/board.py --archive     # include the archives
    python tools/board.py --maintainer  # what waits on the Maintainer
    python tools/board.py --json        # data output (schema cairn-board/1)
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import stat
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

#: Header fields worth a column in the terminal table, in print order. Anything
#: else an author writes in the header block is still theirs to write -- it
#: simply has no column in the plain terminal table.
_FIELDS: Tuple[str, ...] = (
    "Status",
    "Review",
    "Plan review",
    "Opened",
    "Source proposal",
    "Waiting on Maintainer",
)

_HEADER_FIELD_RE = re.compile(r"^\*\*(?P<name>[A-Za-z][A-Za-z /-]*)\*\*:\s*(?P<value>.*)$")

#: What counts as a declared wait under `--maintainer`.
_WAIT = "Waiting on Maintainer"
_FENCE_WORDS: Tuple[str, ...] = ("MAINTAINER-GATED", "MAINTAINER-ONLY")
#: `awaiting-decision`, with an optional note after the word (` -- ...`, ` (...)`).
_AWAITING_DECISION_RE = re.compile(r"^awaiting-decision(?![A-Za-z0-9_])")
#: In `dev/PLANNING.md`, the marker counts only when the line starts with it
#: (after indentation and one optional list bullet), never inside prose or
#: backticks.
_ROW_BULLET_RE = re.compile(r"^ *(?:[*-] )?")


class _BoardSourceError(Exception):
    """Raised when a board source cannot be read as a regular file or folder."""

    def __init__(self, rel: str, reason: str) -> None:
        super().__init__(f"{rel}: {reason}")
        self.rel = rel
        self.reason = reason


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _session_kernel():
    """The session kernel, which owns the terminal encoder and the status
    vocabulary, loaded from `tools/session.py`."""
    path = _repo_root() / "tools" / "session.py"
    spec = importlib.util.spec_from_file_location("_cairn_session_encoder", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _encode(limit: int = 48, module=None):
    """The one terminal encoder, loaded from the session kernel.

    Values here come out of files any contributor can edit, so they are
    untrusted for display purposes. There is deliberately no local escape table
    to fall back on: a second, weaker path engages exactly when something is
    already wrong.
    """
    module = module or _session_kernel()

    def cell(value: str) -> str:
        text = module.encode_display(str(value))
        # Elision is layered outside the encoder, and the cut is taken from
        # encoded output so it cannot split a source character into a
        # half-escape that reads as something else.
        return text if len(text) <= limit else text[:limit - 1] + "\u2026"

    return cell


def _check_source(root: Path, rel: str, expect: str,
                  skipped: List[str]) -> Optional[Path]:
    """Examine each component of `rel` below `root` before following any link.

    Gives one of three answers: a symbolic link (recorded once in `skipped` by
    its highest linked component, returns `None`), a regular file or real
    folder (returns its `Path`), or anything else (raises `_BoardSourceError`,
    except for `dev/PLANNING.md` where a non-regular entry returns `None`).
    """
    parts = Path(rel).parts
    for idx in range(len(parts)):
        sub_rel = "/".join(parts[:idx + 1])
        cur = root.joinpath(*parts[:idx + 1])
        if cur.is_symlink():
            if sub_rel not in skipped:
                skipped.append(sub_rel)
            return None
        try:
            mode = cur.lstat().st_mode
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise _BoardSourceError(sub_rel, "cannot stat") from exc
        if idx < len(parts) - 1:
            if not stat.S_ISDIR(mode):
                raise _BoardSourceError(sub_rel, "not a directory")
        elif expect == "dir":
            if not stat.S_ISDIR(mode):
                raise _BoardSourceError(sub_rel, "not a directory")
        elif expect == "planning":
            if not stat.S_ISREG(mode):
                return None
        else:
            if not stat.S_ISREG(mode):
                raise _BoardSourceError(sub_rel, "not a regular file")
    return root.joinpath(*parts)


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


def _title(text: str) -> Optional[str]:
    """The first `# ` line above the first `##` heading, or `None`."""
    for line in text.splitlines():
        if line.startswith("## "):
            break
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _artifacts(root: Path, include_archive: bool,
               skipped: Optional[List[str]] = None):
    """`(kind, path, text)` for each proposal and plan, in print order."""
    seen_skipped = skipped if skipped is not None else []
    for kind, rel in (("proposal", "dev/proposals"), ("plan", "dev/plans")):
        base = _check_source(root, rel, "dir", seen_skipped)
        if base is None:
            continue
        folders = [(rel, base)]
        if include_archive:
            arch_rel = f"{rel}/archive"
            arch = _check_source(root, arch_rel, "dir", seen_skipped)
            if arch is not None:
                folders.append((arch_rel, arch))
        for folder_rel, folder in folders:
            try:
                names = sorted(
                    entry.name for entry in folder.iterdir()
                    if entry.name.endswith(".md") and not entry.name.startswith("_")
                )
            except OSError as exc:
                raise _BoardSourceError(folder_rel, "cannot list directory") from exc
            for name in names:
                leaf_rel = f"{folder_rel}/{name}"
                path = _check_source(root, leaf_rel, "file", seen_skipped)
                if path is None:
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except (OSError, UnicodeError) as exc:
                    raise _BoardSourceError(leaf_rel, "cannot read UTF-8 text") from exc
                yield kind, path, text


def _rows(root: Path, include_archive: bool,
          skipped: Optional[List[str]] = None) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for kind, path, text in _artifacts(root, include_archive, skipped):
        fields = _header_fields(text)
        if not fields:
            continue
        row = {"kind": kind, "artifact": path.stem,
               "archived": "yes" if path.parent.name == "archive" else ""}
        row.update({f: fields.get(f, "") for f in _FIELDS})
        rows.append(row)
    return rows


def _roadmap_waits(root: Path,
                   skipped: List[str]) -> Tuple[List[Dict[str, object]], bool]:
    """Marked wait rows in `dev/PLANNING.md` and whether the file was read."""
    planning = _check_source(root, "dev/PLANNING.md", "planning", skipped)
    if planning is None:
        return [], False
    try:
        lines = planning.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise _BoardSourceError("dev/PLANNING.md", "cannot read UTF-8 text") from exc
    waits: List[Dict[str, object]] = []
    for number, line in enumerate(lines, 1):
        m = _HEADER_FIELD_RE.match(_ROW_BULLET_RE.sub("", line, count=1).strip())
        if m and m.group("name").strip() == _WAIT:
            waits.append({"line": number, "text": m.group("value").strip()})
    return waits, True


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
    skipped: List[str] = []
    for kind, path, text in _artifacts(root, include_archive=False, skipped=skipped):
        fields = _header_fields(text)
        declared = _WAIT in fields
        decision = bool(_AWAITING_DECISION_RE.match(fields.get("Status", "")))
        if decision or declared:
            entries.append({"kind": kind, "artifact": path.stem,
                            "reason": "awaiting-decision" if decision else "declared",
                            "text": fields.get(_WAIT, "")})
        if kind == "plan" and not declared and any(w in text for w in _FENCE_WORDS):
            fence_only.append(path.stem)
    roadmap_rows, has_planning = _roadmap_waits(root, skipped)
    planning_skipped = "dev" in skipped or "dev/PLANNING.md" in skipped
    for row in roadmap_rows:
        entries.append({"kind": "roadmap",
                        "artifact": f"dev/PLANNING.md:{row['line']}",
                        "reason": "declared",
                        "text": str(row["text"])})
    return {"entries": entries, "fence_only": fence_only,
            "has_planning": has_planning, "planning_skipped": planning_skipped,
            "skipped": skipped}


def _json_document(root: Path, include_archive: bool) -> Dict[str, object]:
    """The `cairn-board/1` JSON data document."""
    skipped: List[str] = []
    artifacts: List[Dict[str, object]] = []
    for kind, path, text in _artifacts(root, include_archive, skipped):
        fields = _header_fields(text)
        artifacts.append({
            "kind": kind,
            "id": path.stem,
            "path": path.relative_to(root).as_posix(),
            "archived": path.parent.name == "archive",
            "title": _title(text),
            "in_brief": fields.get("In brief"),
            "status": fields.get("Status"),
            "review": fields.get("Review"),
            "plan_review": fields.get("Plan review"),
            "opened": fields.get("Opened"),
            "source_proposal": fields.get("Source proposal"),
            "waiting_on_maintainer": fields.get(_WAIT),
        })
    artifacts.sort(key=lambda r: str(r["path"]))
    roadmap_waits, roadmap_read = _roadmap_waits(root, skipped)
    return {
        "schema": "cairn-board/1",
        "includes_archive": bool(include_archive),
        "artifacts": artifacts,
        "roadmap_waits": roadmap_waits,
        "roadmap_read": roadmap_read,
        "skipped_symlinks": sorted(skipped),
    }


def _render(rows: List[Dict[str, str]], encode,
            skipped: Optional[List[str]] = None, advisory: str = "") -> str:
    cols = ["kind", "artifact"] + [f for f in _FIELDS
                                   if any(r.get(f) for r in rows)] + ["archived"]
    if not any(r.get("archived") for r in rows):
        cols.remove("archived")
    lines = ["board: " + " | ".join(cols)]
    for r in rows:
        lines.append("board: " + " | ".join(encode(r.get(c, "")) for c in cols))
    lines.append(f"board: {len(rows)} row(s). Derived from header blocks; the "
                 f"artifact is authoritative.")
    if advisory:
        lines.append(f"board: {advisory}")
    for rel in skipped or ():
        lines.append(f"board: skipped (symbolic link, not read): {encode(rel)}")
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
    if not found["has_planning"] and not found.get("planning_skipped"):
        lines.append("board: dev/PLANNING.md is missing -- no board rows were read.")
    for rel in found.get("skipped", ()):
        lines.append(f"board: skipped (symbolic link, not read): {encode(rel)}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="board",
        description="Proposals, plans and declared roadmap waits from Cairn's "
                    "dev/ tree. Read-only.",
        epilog=(
            "JSON form: --json prints the board as data (schema cairn-board/1).\n"
            "Field reference and worked example: Cairn's own cairn/docs/build-a-board-view.md\n"
            "(in the repository you adopted from, not in this tree)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--archive", action="store_true",
                        help="Include archived artifacts in the plain board "
                             "and --json. Has no effect on --maintainer.")
    parser.add_argument("--maintainer", action="store_true",
                        help="List what waits on the Maintainer instead: "
                             "proposals awaiting a decision, plans and "
                             "dev/PLANNING.md rows that declare a wait. Also "
                             "names plans that mention a fence but declare "
                             "none. Reads active artifacts only; cannot be "
                             "combined with --json.")
    parser.add_argument("--json", action="store_true",
                        help="Print the board as JSON data (schema "
                             "cairn-board/1): header fields, title and "
                             "location of every proposal and plan, declared "
                             "roadmap waits, and skipped symbolic links. "
                             "Derives no value; cannot be combined with "
                             "--maintainer.")
    parser.add_argument("--root", default=None, help="Repository root.")
    args = parser.parse_args(argv)
    if args.json and args.maintainer:
        parser.error("--json cannot be combined with --maintainer")
    root = Path(args.root).resolve() if args.root else _repo_root()
    if args.json:
        try:
            doc = _json_document(root, args.archive)
        except _BoardSourceError as exc:
            # ascii() is used instead of the terminal encoder so that --json loads no other file.
            print(f"board: error: cannot read {ascii(exc.rel)} ({exc.reason})",
                  file=sys.stderr)
            return 1
        print(json.dumps(doc, ensure_ascii=True, indent=2, sort_keys=True))
        return 0
    kernel = _session_kernel()
    encode = _encode(module=kernel)
    try:
        if args.maintainer:
            print(_render_waiting(_waiting(root), encode))
            return 0
        skipped: List[str] = []
        rows = _rows(root, args.archive, skipped)
        advisory = kernel._status_advisory(
            [(r["artifact"], r["kind"], r["Status"])
             for r in rows if not r["archived"]],
            _encode(limit=200, module=kernel))
        print(_render(rows, encode, skipped, advisory))
        return 0
    except _BoardSourceError as exc:
        print(f"board: error: cannot read {encode(exc.rel)} ({exc.reason})",
              file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
