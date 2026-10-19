#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""onboarding-activate engine -- active-surfacing prompt rendering.

The active-surfacing UX layer: the registry of surfacing rows,
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
    ("second-agent-type", "second-agent-type"),
)


#: UX caps per goodnight.  Per the plan: <=1 active prompt;
#: <=3 newly-inserted PLANNING tasks.
MAX_ACTIVE_PROMPTS_PER_GOODNIGHT = 1


MAX_NEW_TASKS_PER_GOODNIGHT = 3


#: Per-preset prompt-content section anchor.  The preset file's
#: active-surfacing prompt content lives under `### Row N -- <label>`
#: headings.  Matching is two-stage: this pattern enforces the
#: structural shape and captures the label, and the label is then
#: compared to the row name under `_fold_for_match` below.
#:
#: The `Row N -- ` prefix is load-bearing, not decoration: without it
#: `### Notes on second-agent-type` matches as readily as the
#: real prompt heading.  Keep the two-hyphen separator required.
_ROW_HEADING_RE = re.compile(
    r"\A###\s+Row\s+\d+\s+--\s+(?P<label>.*)\Z",
    re.IGNORECASE,
)

#: Arrow spellings a heading label may use for a transition.
_ARROW_FORMS = ("\u2192", "->")


def _fold_for_match(text: str) -> str:
    """Fold a row name or a heading label to one comparable shape.

    Row names are registry identifiers (`second-agent-type`); heading
    labels are prose written for a human to read
    (`second-agent-type spin-up prompt`, or a transition written with
    an arrow).  The two spell the same thing differently, so a literal
    substring test between them is false whenever a label uses an arrow
    or a space where the row name uses `-to-` or a hyphen.

    Folding both sides is what lets the identifier stay stable while
    the prose stays readable.  The row name is an idempotency key --
    `select_active_prompt_to_fire` derives the activation-log marker
    from it -- so renaming a row to match its heading would re-fire a
    one-shot prompt for everyone who had already dismissed it.
    """
    folded = text.lower()
    for arrow in _ARROW_FORMS:
        folded = folded.replace(arrow, "-to-")
    folded = re.sub(r"[\s_]+", "-", folded)
    return re.sub(r"-{2,}", "-", folded)


def _heading_matches(line: str, row_name: str) -> bool:
    """Is *line* the prompt heading introducing *row_name*?

    Structure is checked on the raw line so the `Row N -- ` shape
    still gates the match; only the captured label is folded.
    """
    found = _ROW_HEADING_RE.match(line)
    if found is None:
        return False
    label = _fold_for_match(found.group("label"))
    row = _fold_for_match(row_name)
    # Anchored at the front and at a token boundary, not bare containment:
    # a label may trail extra words ("... spin-up prompt"), but a row name
    # must not match because it happens to appear mid-label. Bare containment
    # let a heading mentioning another row's words capture that row's body.
    return label == row or label.startswith(row + "-")


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
    lines = preset_text.splitlines()
    body_start: int | None = None
    for i, line in enumerate(lines):
        if _heading_matches(line, row_name):
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
