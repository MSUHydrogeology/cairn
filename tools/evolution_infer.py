#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Deterministic decision-support for the self-evolution loop.

Reads the **incident trackers** and machine-evaluates the
**adaptive-doctrine rate-limit gate**
(``doctrine/rationale.md`` > "Adaptive-doctrine rate-limit gate"), emitting
text decision-support:

* **rate-limit suggestions** -- when an incident event-class accumulates
  ``>=`` the threshold (default 2) ``Impact = occurred`` rows within the
  tracker's rolling window, the gate's recurrence trigger is met and a
  doctrine proposal *may* be justified;

It is **deterministic, rule-based, and zero-token** (no model calls): the
recurrence count is *computed*, not eyeballed. It **only suggests** -- it
emits text and **never mutates** the trackers, doctrine, or
anything else (it opens no proposal and files no issue). Any richer
LLM-driven clustering is a separate, on-demand command, deliberately *out*
of this deterministic pipeline.

**Fail-closed (the gate is adopter-pinned).** The doctrine pins the rolling
window in each tracker's prose (the ``**Rolling window**:`` line; the
``## What counts`` sub-section defines the event classes), and the gate reads
the ``Date``, ``Event Class`` and ``Impact`` columns by header name. If a
tracker carries an ``## Incidents`` table but **no parseable rolling window**,
or its table lacks one of those columns, the gate for that tracker **cannot
be evaluated** -- this tool says why and exits non-zero (3) rather than
counting zero, which would read exactly like a tracker with nothing to report.
A tracker named with ``--trackers`` that has no ``## Incidents`` table fails
closed the same way; during discovery, such a file is not an incident tracker
and is skipped, but it is named as skipped. Every evaluated tracker is listed
with what was read from it, and a run that read no tracker says so instead of
printing a bare "none", so an empty result can be told apart from an unread
one.

Usage::

    python tools/evolution_infer.py
    python tools/evolution_infer.py --root /path/to/repo
    python tools/evolution_infer.py --trackers dev/measurement/collision_log.md
    python tools/evolution_infer.py --threshold 2
    python tools/evolution_infer.py --json

Exit codes::

    0  -- evaluated cleanly (with or without findings)
    2  -- usage error (a named tracker path does not exist)
    3  -- fail-closed: a tracker the gate could not evaluate (no parseable
          rolling window, a missing Date / Event Class / Impact column, or a
          named tracker with no Incidents table)
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path


DEFAULT_TRACKER_DIR = "dev/measurement"
DEFAULT_THRESHOLD = 2

_INCIDENTS_HEADING = "## Incidents"

#: ``**Rolling window**: <value>`` -- the adopter-pinned window line.
_ROLLING_WINDOW_RE = re.compile(r"\*\*Rolling window\*\*\s*:\s*(.+)", re.IGNORECASE)
#: A leading ``<int> [day|week]`` inside the window value ("14 days", "2 weeks",
#: "21 days.", a bare "14").
_DURATION_RE = re.compile(r"(\d+)\s*(days?|weeks?)?", re.IGNORECASE)
#: The Incidents-table columns the gate reads, matched by header name
#: (case- and whitespace-insensitive), so reordered columns still read and a
#: missing one is refused rather than counted as zero.
_REQUIRED_COLUMNS = ("date", "event class", "impact")


# ---------------------------------------------------------------------------
# Markdown parsing (shared, stdlib-only)
# ---------------------------------------------------------------------------


def _section_body(text: str, heading: str) -> str:
    """The body of the H2 section whose heading equals *heading*
    (case-insensitive), until the next ``## `` heading or EOF. ``""`` if
    the section is absent."""
    out: list[str] = []
    in_section = False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("## "):
            if in_section:
                break
            in_section = stripped.lower() == heading.lower()
            continue
        if in_section:
            out.append(line)
    return "".join(out)


def _header_cells(section: str) -> list[str] | None:
    """The normalised header row of the first markdown table in *section*,
    or ``None`` when the section holds no table."""
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            return [" ".join(c.lower().split())
                    for c in stripped.strip("|").split("|")]
    return None


def _data_rows(section: str):
    """Yield the cell-lists of each *data* row of the first markdown table in
    *section* (the header row and the ``|---|`` separator are skipped)."""
    seen_header = False
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        # Separator row: every non-empty cell is only dashes / colons / spaces.
        if all(set(c) <= set("-: ") for c in cells if c):
            continue
        if not seen_header:
            seen_header = True
            continue
        yield cells


# ---------------------------------------------------------------------------
# Rolling-window parse (fail-closed signal is ``None``)
# ---------------------------------------------------------------------------


def parse_rolling_window(text: str) -> int | None:
    """Days from the ``**Rolling window**: <N days | N weeks | N>`` line.

    Returns the window length in **days**, or ``None`` when the line is absent
    or carries no parseable duration -- the **fail-closed** signal (the caller
    must NOT default; an unparseable window means the gate cannot be evaluated)."""
    m = _ROLLING_WINDOW_RE.search(text)
    if m is None:
        return None
    value = m.group(1).strip()
    dm = _DURATION_RE.search(value)
    if dm is None:
        return None
    # Fail-closed on a negative window (a leading '-' the digit-only capture
    # would otherwise drop, e.g. "-3 days" -> 3).
    if dm.start() > 0 and value[dm.start() - 1] == "-":
        return None
    try:
        n = int(dm.group(1))
    except (TypeError, ValueError):
        return None
    if n <= 0:
        return None
    unit = (dm.group(2) or "day").lower()
    return n * 7 if unit.startswith("week") else n


# ---------------------------------------------------------------------------
# Incident-table parse + gate evaluation
# ---------------------------------------------------------------------------


def parse_incidents(text: str) -> list[dict]:
    """``[{date, event_class, impact}]`` from the ``## Incidents`` table,
    reading each column by its header name.

    Rows whose date cell is not a real ISO date (the template's
    ``<YYYY-MM-DD>`` placeholder, or any malformed row) are skipped
    (fail-safe -- a bad row never crashes the evaluation); a row too short to
    reach the Impact cell counts as no impact.  A table missing a required
    column yields no rows -- :func:`tracker_problem` is what reports it."""
    body = _section_body(text, _INCIDENTS_HEADING)
    header = _header_cells(body) or []
    if any(col not in header for col in _REQUIRED_COLUMNS):
        return []
    i_date, i_class, i_impact = (header.index(c) for c in _REQUIRED_COLUMNS)
    out: list[dict] = []
    for cells in _data_rows(body):
        if len(cells) <= max(i_date, i_class):
            continue
        try:
            day = datetime.date.fromisoformat(cells[i_date].strip())
        except (TypeError, ValueError):
            continue
        out.append({
            "date": day,
            "event_class": cells[i_class].strip(),
            "impact": (cells[i_impact].strip().lower()
                       if len(cells) > i_impact else ""),
        })
    return out


def tracker_problem(text: str) -> str | None:
    """Why the gate cannot evaluate this tracker, or ``None`` when it can.

    Every reason is fail-closed: a tracker the gate cannot read must never be
    reported as a tracker with nothing to report."""
    if _INCIDENTS_HEADING not in text:
        return "no '## Incidents' table"
    reasons: list[str] = []
    header = _header_cells(_section_body(text, _INCIDENTS_HEADING))
    if header is None:
        reasons.append("an '## Incidents' section with no table")
    else:
        missing = [c for c in _REQUIRED_COLUMNS if c not in header]
        if missing:
            names = ", ".join(f"'{c.title()}'" for c in missing)
            reasons.append(f"no {names} column in the Incidents table")
    if parse_rolling_window(text) is None:
        reasons.append("no parseable '**Rolling window**:' line")
    return "; ".join(reasons) or None


def evaluate_tracker(
    text: str, *, today: datetime.date, threshold: int,
) -> tuple[int | None, list[dict]]:
    """``(window_days, findings)``. ``window_days is None`` is the fail-closed
    signal (an Incidents table with no parseable rolling window).

    A *finding* is an event-class with ``>= threshold`` ``occurred`` rows
    dated within the rolling window: ``{event_class, count, window_days}``."""
    window = parse_rolling_window(text)
    if window is None:
        return None, []
    cutoff = today - datetime.timedelta(days=window)
    counts: dict[str, int] = {}
    for inc in parse_incidents(text):
        if inc["impact"] == "occurred" and inc["date"] >= cutoff:
            counts[inc["event_class"]] = counts.get(inc["event_class"], 0) + 1
    findings = [
        {"event_class": ec, "count": n, "window_days": window}
        for ec, n in sorted(counts.items()) if n >= threshold
    ]
    return window, findings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _resolve_trackers(root: Path, named: list[str] | None) -> list[Path]:
    if named:
        return [root / n for n in named]
    tracker_dir = root / DEFAULT_TRACKER_DIR
    if not tracker_dir.is_dir():
        return []
    return sorted(tracker_dir.glob("*.md"))


def _relpath(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="evolution_infer",
        description=(
            "Deterministic, zero-token decision-support: machine-evaluate the "
            "adaptive-doctrine rate-limit gate over the incident trackers. "
            "Emits suggestions only -- never mutates."
        ),
    )
    parser.add_argument(
        "--root", type=Path, default=Path("."),
        help="Repo root. Default: the current directory.",
    )
    parser.add_argument(
        "--trackers", nargs="*", default=None,
        help=(
            "Tracker file(s) to evaluate (relative to --root). Default: every "
            f"*.md under {DEFAULT_TRACKER_DIR}/ that carries an Incidents table."
        ),
    )
    parser.add_argument(
        "--threshold", type=int, default=DEFAULT_THRESHOLD,
        help=(
            "Recurrence trigger: an event-class with this many 'occurred' rows "
            f"in the window is suggested. Default: {DEFAULT_THRESHOLD} (the "
            "doctrine's '>=2 same-shape' rule)."
        ),
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Emit machine-readable JSON instead of human-readable text.",
    )
    args = parser.parse_args(argv)

    root = args.root
    today = datetime.date.today()

    tracker_paths = _resolve_trackers(root, args.trackers)
    if args.trackers:
        for tp in tracker_paths:
            if not tp.is_file():
                print(
                    f"evolution_infer: tracker not found: {tp}", file=sys.stderr,
                )
                return 2

    findings: list[dict] = []
    failclosed: list[str] = []
    reasons: dict[str, str] = {}
    read: list[dict] = []
    skipped: list[str] = []
    for tp in tracker_paths:
        if not tp.is_file():
            continue
        text = tp.read_text(encoding="utf-8", errors="replace")
        rel = _relpath(tp, root)
        if _INCIDENTS_HEADING not in text and not args.trackers:
            skipped.append(rel)  # discovered, and not an incident tracker
            continue
        problem = tracker_problem(text)
        if problem is not None:
            failclosed.append(rel)
            reasons[rel] = problem
            continue
        window, tracker_findings = evaluate_tracker(
            text, today=today, threshold=args.threshold,
        )
        cutoff = today - datetime.timedelta(days=window)
        incidents = parse_incidents(text)
        read.append({
            "tracker": rel,
            "rows": len(incidents),
            "occurred_in_window": sum(
                1 for inc in incidents
                if inc["impact"] == "occurred" and inc["date"] >= cutoff),
            "window_days": window,
        })
        for f in tracker_findings:
            f["tracker"] = rel
            findings.append(f)

    if args.json:
        print(json.dumps({
            "findings": findings,
            "fail_closed_trackers": failclosed,
            "fail_closed_reasons": reasons,
            "trackers_read": read,
            "trackers_skipped": skipped,
            "threshold": args.threshold,
        }, indent=2))
    else:
        _print_human(findings, failclosed, reasons, read, skipped, args)

    # Fail-closed is the only non-zero exit (besides usage): an unparseable
    # window must not pass silently.
    return 3 if failclosed else 0


def _print_human(findings, failclosed, reasons, read, skipped, args) -> None:
    print("evolution_infer: rate-limit gate (advisory only)")
    if read:
        print(f"\nREAD ({len(read)}):")
        for r in read:
            print(
                f"  - tracker {r['tracker']}: {r['rows']} incident row(s), "
                f"{r['occurred_in_window']} 'occurred' in the "
                f"{r['window_days']}-day window"
            )
    if skipped:
        print(f"\nSKIPPED ({len(skipped)}) -- no '{_INCIDENTS_HEADING}' "
              "table, so not read as a tracker:")
        for rel in skipped:
            print(f"  - {rel}")
    if findings:
        print(f"\nRATE-LIMIT SUGGESTIONS ({len(findings)}):")
        for f in findings:
            print(
                f"  - event-class '{f['event_class']}' has {f['count']} "
                f"'occurred' incident(s) in the {f['window_days']}-day window "
                f"(tracker {f['tracker']}) -- the recurrence trigger "
                f"(>={args.threshold}) is met; a doctrine proposal may be "
                f"justified. (Suggestion only -- the decision stays human.)"
            )
    elif read:
        print("\nRATE-LIMIT SUGGESTIONS: none.")
    else:
        # Nothing evaluated is not the same as nothing recurring.
        print(
            "\nRATE-LIMIT SUGGESTIONS: none -- but no incident tracker was "
            "read, so the gate evaluated nothing."
        )
    if failclosed:
        print(f"\nFAIL-CLOSED ({len(failclosed)}):")
        for rel in failclosed:
            print(
                f"  - tracker {rel}: {reasons[rel]} -- the rate-limit gate "
                "cannot be evaluated until that is fixed (no silent default)."
            )


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
