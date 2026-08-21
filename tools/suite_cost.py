#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""suite_cost.py -- render the recorded cost of past test sessions.

Reads the JSONL ledger the test suite's own collector appends to (one row per
top-level pytest session) and renders it for a person.  **It runs nothing.**
That is the entire point: the suite's cost had been re-measured by hand
repeatedly and lost every time, because what survived was the number rather
than the place to look it up.

Stdlib only, and Cairn's own tooling rather than anything an adopter installs.

Usage::

    python tools/suite_cost.py                       # the default ledger
    python tools/suite_cost.py --ledger <path>       # another one
    python tools/suite_cost.py --top 15              # more files in the
                                                     # concentration table
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = REPO_ROOT / "dev" / "measurement" / "suite-runs.jsonl"

#: The suite root, relative to the repository root, as the collector defines it
#: (the directory containing the collector itself).  Carried as a constant
#: because the row schema records resolved targets but not the root they were
#: compared against; a ledger produced by a tree that homes its suite elsewhere
#: would be re-derived against the wrong root, and every row would read as a
#: disagreement.  That is a stated limit, not a silent one.
SUITE_ROOT_REL = "bootstrap/tests"

#: The closed option family a ``full`` session may carry -- the same closed set
#: the collector applies.  **Deliberately re-implemented rather than imported.**
#: A re-derivation that called the collector's own classifier could never
#: disagree with it, and reporting a disagreement is the only audit this record
#: has: it is what catches a row written by an older or patched collector.
FAMILY_FLAGS = ("-q", "--no-header", "--no-summary")
SHUFFLE_FLAG = "--quality-gate-shuffle-seed"

OUTCOMES = ("passed", "failed", "errors", "skipped", "xfailed", "xpassed",
            "aborted")


# --- Reading ------------------------------------------------------------------


def read_ledger(path: Path) -> tuple[list[dict], list[tuple[int, str, str]]]:
    """Return ``(rows, malformed)``.

    ``malformed`` carries ``(line_number, reason, excerpt)`` for every line that
    did not decode into a JSON object.  Malformed lines are **reported, never
    skipped**: a line that cannot be parsed is usually a session that was killed
    mid-write, and quietly dropping it turns a visible durability problem into
    an invisible under-count.

    The ledger is gitignored and unsigned -- any local process can write a line
    here, not only the collector -- so a line is untrusted input, not merely a
    possibly-truncated one.  ``json.loads`` raises ``RecursionError`` (a
    ``RuntimeError``, not a ``ValueError``) on a deeply nested array or object,
    which a bare ``except ValueError`` does not catch: one adversarial line
    would otherwise crash this whole tool with an uncaught traceback instead of
    being reported alongside every other malformed line, defeating the
    report-never-skip contract this docstring states for every *other* shape of
    bad input.
    """
    rows: list[dict] = []
    malformed: list[tuple[int, str, str]] = []
    if not path.is_file():
        return rows, malformed
    with path.open(encoding="utf-8", errors="replace") as handle:
        for number, raw in enumerate(handle, start=1):
            text = raw.strip()
            if not text:
                continue
            try:
                value = json.loads(text)
            except ValueError as exc:
                malformed.append((number, f"not valid JSON ({exc})", text[:120]))
                continue
            except RecursionError:
                malformed.append(
                    (number, "not valid JSON (nested too deeply to parse)",
                     text[:120]))
                continue
            if not isinstance(value, dict):
                malformed.append(
                    (number, f"decoded to {type(value).__name__}, not an object",
                     text[:120]))
                continue
            rows.append(value)
    return rows, malformed


# --- Re-derivation ------------------------------------------------------------


def rederive_scope(row: dict) -> str:
    """Re-derive ``scope`` from ``invocation``, ``scope_basis`` and the runtime
    fields, without consulting the stored ``scope``.

    The one step this cannot repeat is path *resolution*: the collector resolved
    the invocation's positionals against the working directory of a session that
    is over.  It is taken on trust that ``scope_basis.targets`` is that resolved
    form, which is why a disagreement here means "these fields no longer support
    that claim", not "the collector lied".
    """
    if row.get("truncated"):
        return "unknown"
    basis = row.get("scope_basis")
    invocation = row.get("invocation")
    if not isinstance(basis, dict) or not isinstance(invocation, list):
        return "unknown"
    targets = basis.get("targets")
    if not isinstance(targets, list):
        return "unknown"

    positionals: list[str] = []
    index = 0
    while index < len(invocation):
        token = str(invocation[index])
        if token.startswith("-"):
            if token in FAMILY_FLAGS:
                index += 1
                continue
            if token.startswith(SHUFFLE_FLAG + "=") and _is_int(
                    token.split("=", 1)[1]):
                index += 1
                continue
            if token == SHUFFLE_FLAG and index + 1 < len(invocation) \
                    and _is_int(invocation[index + 1]):
                index += 2
                continue
            return "unknown"
        positionals.append(token)
        index += 1
    if not positionals:
        return "unknown"

    if len(positionals) == 1 and targets == [SUITE_ROOT_REL]:
        if (not basis.get("inipath") and not basis.get("addopts_set")
                and not basis.get("plugins_set")
                and _int(row, "collected") > 0 and _int(row, "executed") > 0
                and _int(row, "not_run") == 0 and _int(row, "deselected") == 0
                and _int(row, "collection_errors") == 0
                and not row.get("interrupted")):
            return "full"
        return "unknown"
    if targets and all(
            value == SUITE_ROOT_REL or str(value).startswith(SUITE_ROOT_REL + "/")
            for value in targets):
        return "targeted"
    return "unknown"


def _is_int(text) -> bool:
    try:
        int(str(text))
    except (TypeError, ValueError):
        return False
    return True


def _int(row: dict, key: str) -> int:
    value = row.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) else -1


# --- Intervals and overlap ----------------------------------------------------


def _moment(row: dict, key: str):
    value = row.get(key)
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def overlapping_rows(rows: list[dict]) -> set[int]:
    """Indices of rows whose recorded interval intersects another row's.

    Computed from the recorded intervals and nothing else, which is exactly why
    the rendered phrase is "overlapped another **recorded** top-level session":
    release, nested, opted-out, crashed and uninstrumented sessions leave no
    row, so this can never support the stronger claim that no other suite was
    running.
    """
    spans = []
    for index, row in enumerate(rows):
        start, end = _moment(row, "ts_start"), _moment(row, "ts_end")
        if start is not None and end is not None and end >= start:
            spans.append((index, start, end))
    hits: set[int] = set()
    for position, (index_a, start_a, end_a) in enumerate(spans):
        for index_b, start_b, end_b in spans[position + 1:]:
            if start_a <= end_b and start_b <= end_a:
                hits.add(index_a)
                hits.add(index_b)
    return hits


def _day(row: dict) -> str:
    start = _moment(row, "ts_start")
    return start.date().isoformat() if start is not None else "unknown-date"


def _commit(row: dict) -> str:
    head = row.get("head")
    if isinstance(head, str) and len(head) >= 7:
        return head[:12]
    return "commit unrecorded"


def _wall(row: dict):
    value = row.get("wall_s")
    return value if isinstance(value, (int, float)) \
        and not isinstance(value, bool) else None


# --- Rendering ----------------------------------------------------------------


def render(rows: list[dict], malformed: list[tuple[int, str, str]],
           ledger_path: Path, top: int = 10) -> str:
    lines: list[str] = []
    add = lines.append

    add("# Suite cost -- already measured. Do not re-run the suite.")
    add("")
    add("Every figure below comes from a test session that has already run and "
        "was recorded at the time. Running the suite again to answer a question "
        "this page answers is the exact cost this record exists to avoid: it is "
        "the most expensive command in the repository, and the answer does not "
        "improve for being re-measured.")
    add("")
    add(f"Ledger file: `{ledger_path}`")
    add(f"Rows read: {len(rows)}. Unreadable lines: {len(malformed)}.")
    add("")

    _render_limits(add)
    _render_sessions(add, rows)
    _render_refusals(add, rows)
    _render_full_runs_per_day(add, rows)
    _render_session_table(add, rows)
    _render_concentration(add, rows, top)
    _render_trend(add, rows)
    _render_disagreements(add, rows)
    _render_malformed(add, malformed)
    return "\n".join(lines) + "\n"


def _render_limits(add) -> None:
    add("## What this record cannot see")
    add("")
    add("Stated first, because every number further down is bounded by it:")
    add("")
    add("* **Release-mode sessions are not recorded.** A run made under the "
        "release gate writes no row, by design -- the release ceremony's "
        "evidence must not share a mechanism with a diagnostics side-channel.")
    add("* **Nested sessions are not recorded.** A pytest session started "
        "inside another one is treated as a child of the session already "
        "recording, and writes nothing. Suite-spawned children and in-process "
        "`pytest.main()` calls are both in this class.")
    add("* **Opted-out sessions are not recorded.** An operator can switch the "
        "collector off for a run, and a run made in a tree with no measurement "
        "directory records nothing.")
    add("* **Crashed sessions may not be recorded.** A row is written at the "
        "very end of a session; a run killed before that point, or one that "
        "could not take the ledger's write lock in time, leaves no trace.")
    add("* **Uninstrumented sessions are not recorded.** Any run made before "
        "the collector existed, or from a tree that does not carry it, is "
        "invisible here.")
    add("* **Working-tree cleanliness is `unknown`, not clean.** The collector "
        "records the commit a session ran at but does **not** record whether "
        "the working tree was modified at the time, so a figure attributed to "
        "a commit may have been produced by code that never was that commit. "
        "Treat every commit below as `unknown`-dirty.")
    add("")


def _render_sessions(add, rows: list[dict]) -> None:
    add("## How many sessions this covers")
    add("")
    add(f"Recorded top-level sessions: **{len(rows)}** -- and that is a "
        "**lower bound**, never a count. Each exclusion in the list above "
        "removes sessions silently, so the real number of times this suite ran "
        "is at least this and may be considerably more.")
    add("")


def _is_refused(row: dict) -> bool:
    """A session the broad-run guard refused before any test ran.

    Keyed on ``exitstatus == 4`` -- pytest's own exit code for a ``UsageError``,
    which is what the guard raises -- and not on ``scope == "unknown"``, which
    cannot tell a refusal apart from any other non-full run such as a ``-k``
    selection.  Both fields are already pinned, so this adds no schema term.

    The ``isinstance`` test is load-bearing and not defensive habit: JSON has one
    number type, so a corrupted or hand-written ``4.0`` parses to a float, and
    ``4.0 == 4`` is true. A bare equality check would count it. ``bool`` needs no
    separate exclusion -- ``True`` is ``1``, which is not ``4``.
    """
    status = row.get("exitstatus")
    return isinstance(status, int) and status == 4


def _render_refusals(add, rows: list[dict]) -> None:
    add("## Sessions the broad-run guard refused")
    add("")
    add("A refused session ran no tests but still contributes real wall-clock "
        "and an empty ``by_file``, so it is named here rather than left to be "
        "inferred from a zero row further down.")
    add("")
    add("Keyed on ``exitstatus == 4``, the exit code the guard's own "
        "``UsageError`` sets. A ``scope`` of ``unknown`` alone cannot tell a "
        "refusal apart from any other non-full run, such as a ``-k`` selection.")
    add("")
    refused = [row for row in rows if _is_refused(row)]
    add("**" + str(len(refused)) + "** of " + str(len(rows))
        + " recorded session(s).")
    add("")
    if not refused:
        return
    per_day: dict[str, int] = {}
    for row in refused:
        per_day[_day(row)] = per_day.get(_day(row), 0) + 1
    for day in sorted(per_day):
        add("* **" + day + "** -- " + str(per_day[day]) + " refusal(s).")
    add("")


def _render_full_runs_per_day(add, rows: list[dict]) -> None:
    add("## Complete runs, per calendar day")
    add("")
    add("Counted **per day, never per plan.** No field in a row binds a session "
        "to a piece of work, so any per-plan attribution would be invented. The "
        "only attribution that exists is the optional operator-supplied label "
        "shown in the session table; a run made without one is not attributable "
        "at all.")
    add("")
    per_day: dict[str, int] = {}
    for row in rows:
        if row.get("scope") == "full":
            per_day[_day(row)] = per_day.get(_day(row), 0) + 1
    if not per_day:
        add("No session in this ledger covered the whole suite, so there is "
            "nothing to count here yet.")
        add("")
        return
    for day in sorted(per_day):
        add(f"* **{day}** -- {per_day[day]} complete run(s) of the whole suite.")
    add("")


def _render_session_table(add, rows: list[dict]) -> None:
    add("## Every recorded session, with the conditions it ran under")
    add("")
    add("A duration with no conditions attached is the thing this record exists "
        "to replace, so each row carries the date it ran, the commit it ran at, "
        "the interpreter that ran it, what the session covered, and whether "
        "another recorded session was running at the same time.")
    add("")
    if not rows:
        add("The ledger has no readable rows yet.")
        add("")
        return
    overlaps = overlapping_rows(rows)
    add("| date | commit | interpreter | covered | wall clock | tests run | "
        "concurrent | label |")
    add("|---|---|---|---|---|---|---|---|")
    for index, row in enumerate(rows):
        wall = _wall(row)
        wall_text = f"{wall:.1f}s" if wall is not None else "unrecorded"
        label = row.get("label")
        label_text = f"`{label}`" if isinstance(label, str) and label \
            else "no label given"
        concurrent = ("overlapped another recorded top-level session"
                      if index in overlaps
                      else "no overlap with another recorded session")
        executed = row.get("executed")
        collected = row.get("collected")
        add(f"| {_day(row)} | {_commit(row)} | "
            f"{row.get('interpreter') or 'unrecorded'} | "
            f"{_covered(row)} | {wall_text} | {executed} of {collected} "
            f"collected | {concurrent} | {label_text} |")
    add("")


def _covered(row: dict) -> str:
    scope = row.get("scope")
    if scope == "full":
        return "the whole suite"
    if scope == "targeted":
        return "part of the suite"
    return "cannot be determined from the row"


def _render_concentration(add, rows: list[dict], top: int) -> None:
    add("## Where the cost is concentrated")
    add("")
    full_rows = [row for row in rows if row.get("scope") == "full"]
    source = full_rows or rows
    if full_rows:
        add(f"Summed across the {len(full_rows)} session(s) that covered the "
            "whole suite, so the files compare against each other on equal "
            "terms.")
    elif rows:
        add(f"No session covered the whole suite, so this sums all "
            f"{len(rows)} recorded session(s) instead. Files touched by fewer "
            "sessions will look cheaper than they are -- this table ranks what "
            "was *measured*, not what a complete run would cost.")
    else:
        add("The ledger has no readable rows yet.")
        add("")
        return

    totals: dict[str, int] = {}
    pruned = []
    for row in source:
        by_file = row.get("by_file")
        if isinstance(by_file, dict):
            for path, millis in by_file.items():
                if isinstance(millis, int) and not isinstance(millis, bool):
                    totals[str(path)] = totals.get(str(path), 0) + millis
        kept, total = row.get("by_file_kept"), row.get("by_file_total")
        if isinstance(kept, int) and isinstance(total, int) and kept < total:
            pruned.append((_day(row), kept, total))
    add("")
    if pruned:
        add("**Incomplete breakdowns.** These sessions' per-file detail did not "
            "fit the ledger's line budget, so the cheapest files were dropped "
            "before the row was written. The table below therefore *understates* "
            "the number of files and the total, and the files it lost are the "
            "cheap ones:")
        add("")
        for day, kept, total in pruned:
            add(f"* {day}: kept {kept} of {total} files measured.")
        add("")
    if not totals:
        add("No session recorded a per-file breakdown.")
        add("")
        return
    grand = sum(totals.values()) or 1
    ranked = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
    add(f"Measured test time across those sessions: "
        f"{grand / 1000.0:.1f}s over {len(totals)} file(s).")
    add("")
    add("| test file | measured time | share of measured time |")
    add("|---|---|---|")
    for path, millis in ranked[:top]:
        add(f"| `{path}` | {millis / 1000.0:.1f}s | "
            f"{100.0 * millis / grand:.1f}% |")
    add("")
    head = sum(millis for _p, millis in ranked[:top])
    add(f"Those {min(top, len(ranked))} file(s) account for "
        f"{100.0 * head / grand:.1f}% of the measured time. Note this is "
        "*measured test time*, which is smaller than the wall clock above: "
        "collection, fixtures and interpreter startup are not attributed to any "
        "file.")
    add("")


def _median(values: list[float]) -> float:
    """The true median: the mean of the two middle values on an even count.

    ``sorted(values)[len(values) // 2]`` -- the pattern this replaces --
    returns the upper of the two middle values on an even count, which is
    not the median; it silently passed here because no two-run day was ever
    exercised. Odd counts are unaffected.
    """
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def _render_trend(add, rows: list[dict]) -> None:
    add("## Whether it is getting slower")
    add("")
    per_day: dict[str, list[float]] = {}
    for row in rows:
        if row.get("scope") != "full":
            continue
        wall = _wall(row)
        if wall is not None:
            per_day.setdefault(_day(row), []).append(float(wall))
    if len(per_day) < 2:
        add("A trend needs complete runs on at least two different days; this "
            "ledger has "
            f"{len(per_day)}. Until then the figures above are single "
            "observations, not a direction.")
        add("")
        return
    add("Each day's median wall clock, over sessions that covered the whole "
        "suite. Interpreter and commit change between days, so a change here is "
        "a prompt to look, not a measurement of any one cause.")
    add("")
    days = sorted(per_day)
    for day in days:
        values = per_day[day]
        median = _median(values)
        add(f"* **{day}** -- median {median:.1f}s over {len(values)} run(s).")
    first = _median(per_day[days[0]])
    last = _median(per_day[days[-1]])
    add("")
    if last > first:
        add(f"From {days[0]} to {days[-1]} the median complete run got "
            f"slower: {first:.1f}s to {last:.1f}s.")
    elif last < first:
        add(f"From {days[0]} to {days[-1]} the median complete run got "
            f"faster: {first:.1f}s to {last:.1f}s.")
    else:
        add(f"From {days[0]} to {days[-1]} the median complete run did not "
            f"move: {first:.1f}s on both days.")
    add("")


def _render_disagreements(add, rows: list[dict]) -> None:
    add("## Rows whose recorded coverage no longer follows from their evidence")
    add("")
    add("Each row's coverage claim is re-derived here from its invocation, its "
        "recorded basis and its own counts, and compared with what the row "
        "says. A mismatch does not mean the number beside it is wrong; it means "
        "the row no longer carries the evidence for its own claim, so treat "
        "that claim as unproven.")
    add("")
    found = False
    for index, row in enumerate(rows):
        stored = row.get("scope")
        derived = rederive_scope(row)
        if stored != derived:
            found = True
            add(f"* Row {index + 1} ({_day(row)}, {_commit(row)}): recorded as "
                f"`{stored}`, but its own fields support `{derived}`.")
    if not found:
        add("None. Every row's recorded coverage follows from its own fields.")
    add("")


def _render_malformed(add, malformed: list[tuple[int, str, str]]) -> None:
    add("## Unreadable lines")
    add("")
    if not malformed:
        add("None. Every line in the ledger decoded.")
        add("")
        return
    add("Reported rather than skipped -- an unreadable line is usually a "
        "session that was killed while writing, which is information about the "
        "ledger's own reliability and about the sessions it is missing:")
    add("")
    for number, reason, excerpt in malformed:
        add(f"* Line {number}: {reason} -- `{excerpt}`")
    add("")


# --- Entry point --------------------------------------------------------------


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Render the recorded cost of past test sessions. "
                    "Runs nothing.")
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER),
                        help="path to the JSONL ledger to render")
    parser.add_argument("--top", type=int, default=10,
                        help="how many files to list in the concentration table")
    args = parser.parse_args(argv)
    path = Path(args.ledger)
    rows, malformed = read_ledger(path)
    sys.stdout.write(render(rows, malformed, path, top=max(1, args.top)))
    return 0


if __name__ == "__main__":                      # pragma: no cover
    raise SystemExit(main())
