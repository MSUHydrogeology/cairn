#!/usr/bin/env python3
"""onboarding-activate engine -- active-surfacing prompt rendering (B2).

The active-surfacing UX layer (plan P1.10a/b): the registry of surfacing rows,
the per-goodnight UX caps, the cached heading-matcher, and the prompt renderers
/ selector. A leaf of the ``_onboarding/`` dependency DAG: stdlib-only (``re``),
no intra-package imports.
"""
from __future__ import annotations

import re


#: Priority-ordered list of active-surfacing row names.  Index 0 is
#: highest priority; ties are broken by list order.  The mapping
#: between rows and their firing triggers is also encoded here so the
#: helper can resolve "which row goes with which fired trigger" in
#: one place.
_ACTIVE_SURFACING_ROWS: tuple[tuple[str, str], ...] = (
    # (row-name, firing-trigger)
    ("collab-agreement-signing", "collab-agreement-signing"),
    ("Level-1-to-2-graduation", "level-1-to-2"),
    ("second-agent-type", "second-agent-type"),
    ("upstream-PR-issue-walkthrough", "first-foldback-candidate"),
)


#: UX caps per goodnight.  Per the plan: <=1 active prompt;
#: <=3 newly-inserted PLANNING tasks.
MAX_ACTIVE_PROMPTS_PER_GOODNIGHT = 1


MAX_NEW_TASKS_PER_GOODNIGHT = 3


#: Per-preset prompt-content section anchor.  The preset file's
#: active-surfacing prompt content lives under markdown headings
#: matching this pattern, with the row-name embedded.  Tolerant to
#: small wording variations between presets (the regex captures the
#: row keyword, not the exact heading text).
_PROMPT_HEADING_RE_CACHE: dict[str, re.Pattern[str]] = {}


def _prompt_heading_re(row_name: str) -> re.Pattern[str]:
    """Build (cached) a regex that matches the markdown heading
    introducing the prompt content for *row_name* in a preset file.

    Per Claude External code review P3-3: tightened from the
    earlier overly-permissive ``^###\\s+.*<row>.*$`` (which would
    match `### Notes on collab-agreement-signing` as well as the
    real prompt heading).  The convention the three preset files
    use is `### Row N -- <row-keyword> ...`; the regex requires the
    row keyword to follow a `Row N -- ` shape so off-pattern
    headings don't false-match.
    """
    if row_name not in _PROMPT_HEADING_RE_CACHE:
        slug = row_name.lower()
        _PROMPT_HEADING_RE_CACHE[row_name] = re.compile(
            r"^###\s+Row\s+\d+\s+--\s+.*" + re.escape(slug) + r".*$",
            re.IGNORECASE,
        )
    return _PROMPT_HEADING_RE_CACHE[row_name]


def render_active_surfacing_prompt(
    preset_text: str, row_name: str,
) -> str | None:
    """Extract the prompt content for *row_name* from a preset
    source file.

    Looks for the markdown heading whose name contains *row_name*
    (case-insensitive) inside the "Active-surfacing prompt content"
    section, and returns the body until the next heading at the same
    level (`###`) or end of file.

    Returns the body text, or ``None`` if the row's heading is not
    found.
    """
    heading_re = _prompt_heading_re(row_name)
    lines = preset_text.splitlines()
    body_start: int | None = None
    for i, line in enumerate(lines):
        if heading_re.match(line):
            body_start = i + 1
            break
    if body_start is None:
        return None
    body_end = len(lines)
    for j in range(body_start, len(lines)):
        if lines[j].startswith("### ") or lines[j].startswith("## "):
            body_end = j
            break
    return "\n".join(lines[body_start:body_end]).strip("\n").strip() or None


def select_active_prompt_to_fire(
    fired_triggers: set[str], log_records: list[ActivationRecord],
) -> str | None:
    """Pick the highest-priority unmuted active-surfacing row whose
    firing trigger is in *fired_triggers* AND whose row-name does
    not appear in the log (idempotency -- once an active prompt has
    been emitted, it does not re-fire on subsequent goodnights).

    Returns the row-name (an `_ACTIVE_SURFACING_ROWS` first-column
    string) or ``None`` if no row qualifies.
    """
    already_emitted = {
        rec.task_id for rec in log_records
        if rec.task_id.startswith("active-surface:")
    }
    for row_name, trigger in _ACTIVE_SURFACING_ROWS:
        if trigger not in fired_triggers:
            continue
        marker_id = f"active-surface:{row_name}"
        if marker_id in already_emitted:
            continue
        return row_name
    return None


def render_outcome_with_active_prompt(
    preset_text: str, row_name: str,
) -> tuple[str, str]:
    """Return ``(heading, body)`` for the active-surfacing prompt
    terminal output.  *heading* is the short row label; *body* is the
    per-preset prompt content extracted from the preset file."""
    body = render_active_surfacing_prompt(preset_text, row_name) or (
        f"(prompt content for {row_name!r} not found in preset; "
        "see doctrine/onboarding.md.)"
    )
    return row_name, body
