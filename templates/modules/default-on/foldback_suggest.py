#!/usr/bin/env python3
"""Foldback-surfacing helper -- list open candidates ready to surface.

Stdlib-only.  Reads the deployment's fold-back ledger (a Markdown
file under ``dev/.cairn/<framework>_foldback.md``), parses the "Open
candidates" table, and emits a structured listing of the
``candidate``-status rows that are eligible for active surfacing.

**Grace period**: this helper enforces the standing **7-day capture
grace** the doctrine names (``cairn/doctrine/fold-back.md`` > "Active
surfacing" > "Trigger -- standing").  A row freshly captured within
the last 7 days is suppressed from surfacing; once the grace elapses
the row surfaces normally.  The ``--grace-days`` flag overrides the
default per deployment.

The grace period is computed from an optional **``captured:
<ISO-date>``** field (conventionally written in the row's Source
cell prose).  Two resolution strategies are tried in order:

1. **Explicit ``captured:`` field**: if the row text contains
   ``captured: YYYY-MM-DD`` or ``captured YYYY-MM-DD`` the date is
   parsed directly and the grace is applied.
2. **Legacy prose-date fallback**: if no explicit ``captured:`` is
   found, the helper scans the Source cell for the *first* ISO date
   (``YYYY-MM-DD``) anywhere in the prose.  If found, the same
   7-day grace is applied using it as a proxy for the capture date.
3. **No parseable date**: if neither strategy yields a date, the row
   is treated as surfaceable (conservative: never suppress a row we
   cannot prove is fresh).  This matches the pre-grace behavior and
   means legacy rows with no date in Source behave as before.

Malformed or absent date values never crash the helper.

A row is eligible when:

1. Its **Status** field is exactly ``candidate``.  Rows with newer
   states (``filed -> <#>`` / ``pr -> <#>`` / ``scoped -> ...`` /
   ``synced`` / ``dropped``) are pre-acceptance or post-acceptance and
   are NOT surfaced.  Rows with the older vocabulary (``queued``) are
   also skipped -- the surfacing protocol acts only on the bridge
   between capture and the first deliberate filing decision.  The
   migration rule (per ``cairn/doctrine/fold-back.md`` > "Status
   vocabulary" > "Migration rule") makes this graceful: existing
   ledgers with mixed old + new vocabulary work as-is; only
   ``candidate`` surfaces.
2. Its **deferred-until** value is absent OR has elapsed.  A row
   carrying a future-dated ``deferred-until`` (ISO 8601 ``YYYY-MM-DD``)
   is snoozed; the helper skips it until the deferral expires.  A
   row with a ``deferred-until`` condition string (non-date,
   free-form) is also skipped -- the maintainer evaluates the
   condition manually during the surfacing prompt; the helper does
   not try to parse it.

The active-surfacing protocol (see ``cairn/doctrine/fold-back.md`` >
"Active surfacing") uses this helper as the on-demand trigger: a
maintainer reviewing the funnel state runs::

    python scripts/foldback_suggest.py [--ledger <path>] [--all]

to see the surfaceable rows + their detail-entry pointers.  The
default ledger path is ``dev/.cairn/cairn_foldback.md`` (the
modflow_tools / reference-deployment convention); the
``--ledger <path>`` flag overrides for adopters whose ledger lives
elsewhere.  ``--all`` includes snoozed rows in the output (still
flagged as snoozed), useful for the maintainer reviewing the
funnel's full state.  ``--grace-days`` overrides the default 7-day
capture grace.

Usage::

    python scripts/foldback_suggest.py                # surfaceable rows
    python scripts/foldback_suggest.py --ledger <path>
    python scripts/foldback_suggest.py --all          # incl. snoozed
    python scripts/foldback_suggest.py --json         # machine-readable
    python scripts/foldback_suggest.py --grace-days 14  # custom grace

Exit codes: ``0`` always (this is a read-only listing helper; it
does not gate anything); ``2`` only on a usage error (ledger not
found).
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_LEDGER_PATH = Path("dev/.cairn/cairn_foldback.md")


# ---------------------------------------------------------------------------
# Row shape
# ---------------------------------------------------------------------------


@dataclass
class Candidate:
    """One ledger row eligible for surfacing classification."""

    candidate: str   # First column ("Candidate" -- the human-readable id).
    type_: str       # Second column ("Type").
    size: str        # Third column ("Size").
    status: str      # Fourth column ("Status").
    source: str      # Fifth column ("Source").
    deferred_until: str = ""   # Parsed from the candidate / source
                               # field if present (free-form
                               # ``deferred-until: <date|condition>``).
    captured: str = ""         # Parsed ``captured: <ISO-date>`` value
                               # (empty if absent).  Used to apply the
                               # standing 7-day capture grace.
    surfaceable: bool = False  # Computed by classify_rows().
    skip_reason: str = ""      # When NOT surfaceable, the human-
                               # readable reason.


# ---------------------------------------------------------------------------
# Markdown table parsing
# ---------------------------------------------------------------------------


_OPEN_CANDIDATES_HEADING_RE = re.compile(
    r"^##\s*Open candidates\s*$", re.MULTILINE,
)


def _find_open_candidates_section(text: str) -> str:
    """Extract the "Open candidates" section's body (until the next
    H2 / EOF).  Returns the empty string if the section is absent.
    """
    m = _OPEN_CANDIDATES_HEADING_RE.search(text)
    if m is None:
        return ""
    start = m.end()
    # Find the next H2 or EOF.
    rest = text[start:]
    next_h2 = re.search(r"^##\s", rest, re.MULTILINE)
    return rest if next_h2 is None else rest[: next_h2.start()]


_DEFERRED_UNTIL_RE = re.compile(
    r"\bdeferred-until\s*[:=]\s*([^,;\)\|\n]+?)(?=[,;\)\|]|$)",
    re.IGNORECASE,
)

#: Matches ``captured: YYYY-MM-DD`` or ``captured YYYY-MM-DD`` anywhere
#: in the row text.  Both ``captured:`` and ``captured `` syntaxes are
#: accepted (mirrors the ``deferred-until`` pattern).
_CAPTURED_RE = re.compile(
    r"\bcaptured\s*:?\s*(\d{4}-\d{2}-\d{2})\b",
    re.IGNORECASE,
)

#: Fallback: the first bare ISO date anywhere in a string.
_FIRST_ISO_DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")


def _parse_deferred_until(row_text: str) -> str:
    """Find a ``deferred-until <ISO-date | condition>`` substring in
    a row's content.  Returns the trimmed value, or "" if absent.
    Accepts both ``deferred-until: <value>`` and
    ``deferred-until <value>`` syntaxes.
    """
    m = _DEFERRED_UNTIL_RE.search(row_text)
    if m is None:
        return ""
    return m.group(1).strip()


def _parse_captured(row_text: str) -> str:
    """Find an explicit ``captured: YYYY-MM-DD`` substring in a row's
    content.  Returns the ISO date string, or "" if absent.  Never
    raises; returns "" on any parse failure.
    """
    m = _CAPTURED_RE.search(row_text)
    if m is None:
        return ""
    return m.group(1).strip()


def _first_iso_date_in(text: str) -> str:
    """Return the first ``YYYY-MM-DD`` ISO date found anywhere in
    *text*, or "" if none is present.  Used as the legacy fallback
    when no explicit ``captured:`` field is present.
    """
    m = _FIRST_ISO_DATE_RE.search(text)
    return m.group(1) if m else ""


def _is_table_row(line: str) -> bool:
    """A markdown table row line: starts with ``|`` and has at least
    one more ``|``.  Excludes the separator line (``|---|---|``).
    """
    if not line.startswith("|"):
        return False
    body = line.strip().strip("|").strip()
    return body.count("|") >= 1 and not all(c in "-: |" for c in body)


def _parse_row(line: str) -> list[str]:
    """Split a Markdown table row into its cell values (trimmed,
    pipe-unescaped)."""
    # Strip leading/trailing pipes + whitespace; split on remaining.
    inner = line.strip().strip("|")
    raw_cells = [c.strip() for c in inner.split("|")]
    return raw_cells


def parse_open_candidates(text: str) -> list[Candidate]:
    """Parse the "Open candidates" section's Markdown table.  Returns
    one :class:`Candidate` per data row.  Header row + separator are
    skipped; the helper is tolerant of blank lines / prose between
    section start and the table.
    """
    section = _find_open_candidates_section(text)
    if not section:
        return []
    candidates: list[Candidate] = []
    saw_header = False
    for line in section.split("\n"):
        if not line.strip().startswith("|"):
            # Skip prose lines, blank lines, notes.  Once the table
            # ends (we exit the row block) we still keep scanning for
            # a second table in the section -- the ledger sometimes
            # carries multiple sub-tables.
            continue
        if _is_table_row(line):
            cells = _parse_row(line)
            if len(cells) < 5:
                continue  # malformed row -- skip silently
            if not saw_header:
                # First row of a table is the header.  Recognize it
                # by the literal "Candidate" header cell.
                if cells[0].lower() == "candidate":
                    saw_header = True
                continue
            cand = Candidate(
                candidate=cells[0],
                type_=cells[1],
                size=cells[2],
                status=cells[3],
                source=cells[4],
            )
            # deferred-until can appear in any cell; scan the whole
            # row text for it.
            cand.deferred_until = _parse_deferred_until(line)
            # captured: can appear in any cell; scan the whole row.
            cand.captured = _parse_captured(line)
            candidates.append(cand)
        else:
            # Separator line (|---|---|...) -- not a header reset; the
            # next data row continues the same table.
            pass
    return candidates


# ---------------------------------------------------------------------------
# Surfacing classification
# ---------------------------------------------------------------------------


def _is_iso_date(s: str) -> bool:
    """True when *s* parses as an ISO-8601 ``YYYY-MM-DD`` date."""
    try:
        datetime.date.fromisoformat(s)
        return True
    except (ValueError, TypeError):
        return False


def classify_rows(
    candidates: list[Candidate], *,
    today: datetime.date | None = None,
    grace_days: int = 7,
) -> list[Candidate]:
    """Classify each row's surfaceability per the doctrine.

    A row is **surfaceable** when:
      * status == ``candidate`` (case-insensitive, exact match),
      * AND ``deferred-until`` is absent OR has elapsed (ISO date in
        the past or today; a non-date condition string is treated
        as "still snoozed" since the helper cannot evaluate it),
      * AND the capture grace has elapsed (default 7 days from the
        captured date; see module docstring for the two-strategy
        resolution and the legacy prose-date fallback).

    Args:
        candidates:  rows to classify.
        today:       override "today" for deterministic testing.
        grace_days:  the standing capture-grace window in days.
                     Default 7; adopters can tune per deployment.
    """
    today = today or datetime.date.today()
    classified: list[Candidate] = []
    for c in candidates:
        # Status check: only "candidate" surfaces.  Strip markdown
        # emphasis + whitespace.
        status_clean = c.status.strip().strip("*").strip().lower()
        if status_clean != "candidate":
            c.skip_reason = f"status={c.status!r} (not 'candidate')"
            classified.append(c)
            continue
        # Deferred-until check.
        if c.deferred_until:
            if _is_iso_date(c.deferred_until):
                defer_date = datetime.date.fromisoformat(c.deferred_until)
                if defer_date > today:
                    c.skip_reason = (
                        f"deferred-until {c.deferred_until} "
                        f"(snoozed until that date)"
                    )
                    classified.append(c)
                    continue
                # Elapsed -- surfaceable.
            else:
                # Non-date condition string: maintainer judges
                # manually.  Skip from automatic surfacing.
                c.skip_reason = (
                    f"deferred-until {c.deferred_until!r} "
                    f"(condition string; maintainer judges manually)"
                )
                classified.append(c)
                continue
        # Capture-grace check -- only applied to rows that have
        # passed the status + deferred-until filters above.
        #
        # Strategy 1: explicit ``captured: YYYY-MM-DD`` field.
        # Strategy 2 (legacy fallback): first ISO date in Source prose.
        # No parseable date -> surfaceable (conservative; matches
        # pre-grace behavior for rows with no date at all).
        captured_date: datetime.date | None = None
        try:
            if c.captured and _is_iso_date(c.captured):
                captured_date = datetime.date.fromisoformat(c.captured)
            else:
                # Legacy fallback: scan Source cell for the first ISO date.
                fallback = _first_iso_date_in(c.source)
                if fallback and _is_iso_date(fallback):
                    captured_date = datetime.date.fromisoformat(fallback)
                # No date found -> captured_date stays None -> surfaceable.
        except Exception:  # noqa: BLE001 -- defensive; never crash
            captured_date = None

        if captured_date is not None:
            age = (today - captured_date).days
            if age < grace_days:
                c.skip_reason = (
                    f"in {grace_days}-day capture grace "
                    f"(captured {captured_date.isoformat()})"
                )
                classified.append(c)
                continue
        c.surfaceable = True
        classified.append(c)
    return classified


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


def _format_human(rows: list[Candidate], show_all: bool) -> str:
    """Render *rows* as a human-readable listing."""
    surfaceable = [r for r in rows if r.surfaceable]
    skipped = [r for r in rows if not r.surfaceable]

    lines: list[str] = []
    lines.append(f"Surfaceable candidates: {len(surfaceable)}")
    if not surfaceable:
        lines.append("  (none)")
    for r in surfaceable:
        lines.append(f"  - {r.candidate}")
        lines.append(f"    type={r.type_} size={r.size}")
        if r.captured:
            lines.append(f"    captured={r.captured}")
        lines.append(f"    source={r.source[:120]}{'...' if len(r.source) > 120 else ''}")
    if show_all and skipped:
        lines.append(f"\nSkipped rows: {len(skipped)}")
        for r in skipped:
            lines.append(f"  - {r.candidate[:60]}{'...' if len(r.candidate) > 60 else ''}")
            lines.append(f"    skip: {r.skip_reason}")
    return "\n".join(lines)


def _format_json(rows: list[Candidate], show_all: bool) -> str:
    payload = []
    for r in rows:
        if not show_all and not r.surfaceable:
            continue
        payload.append({
            "candidate": r.candidate,
            "type": r.type_,
            "size": r.size,
            "status": r.status,
            "source": r.source,
            "deferred_until": r.deferred_until,
            "captured": r.captured,
            "surfaceable": r.surfaceable,
            "skip_reason": r.skip_reason,
        })
    return json.dumps(payload, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="foldback_suggest",
        description=(
            "List open `candidate`-status rows from the fold-back "
            "ledger that are eligible for the active-surfacing "
            "protocol (not snoozed via deferred-until)."
        ),
    )
    parser.add_argument(
        "--ledger", type=Path, default=DEFAULT_LEDGER_PATH,
        help=f"Ledger file (default: {DEFAULT_LEDGER_PATH}).",
    )
    parser.add_argument(
        "--all", action="store_true",
        help=(
            "Include snoozed / non-candidate rows in the output "
            "(still classified as not-surfaceable)."
        ),
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Emit machine-readable JSON instead of human-readable.",
    )
    parser.add_argument(
        "--grace-days", type=int, default=7,
        help=(
            "Standing capture-grace window in days.  A row captured "
            "within this many days of today is suppressed from "
            "surfacing.  Default: 7."
        ),
    )
    args = parser.parse_args(argv)

    if not args.ledger.is_file():
        print(
            f"foldback_suggest: ledger not found: {args.ledger}",
            file=sys.stderr,
        )
        return 2

    text = args.ledger.read_text(encoding="utf-8", errors="replace")
    candidates = parse_open_candidates(text)
    classified = classify_rows(candidates, grace_days=args.grace_days)

    out = (
        _format_json(classified, args.all)
        if args.json
        else _format_human(classified, args.all)
    )
    print(out)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
