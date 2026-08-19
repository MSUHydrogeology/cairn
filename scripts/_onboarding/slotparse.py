#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""onboarding-activate engine -- slot + preset parsing.

The PLANNING.md ``onboarding-tasks`` slot grammar and the preset-source-file
parsers: the slot-name constant, the slot open/close + preset / deferred-task /
seed-task regexes, the valid-preset set, the ``DeferredTask`` record, and the
slot-body / preset-name / deferred-task / seed-task extractors. Depends only on
the containment leaf (``security``) for ``OnboardingSecurityError`` (raised by
``extract_preset_from_slot`` on a preset name outside the safe character set).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .security import OnboardingSecurityError


#: The slot name the helper reads + writes.
SLOT_NAME = "onboarding-tasks"


#: ``<!-- preset: <name> -->`` metadata comment inside the slot.
#: Security-hardening (
#: post-v0.2 follow-up plan): the capture group is restricted to
#: alphanumerics, hyphen, and underscore.  This blocks path-
#: traversal sequences (``../etc/passwd``) at the regex level
#: before the name is used in path concatenation.
_PRESET_META_RE = re.compile(r"<!--\s*preset:\s*([a-zA-Z0-9_-]+)\s*-->")


#: Strict-form validator for the ``--preset`` CLI flag.  Same
#: character set as ``_PRESET_META_RE``'s capture group; rejected
#: names raise ``OnboardingSecurityError``.
_PRESET_NAME_RE = re.compile(r"^[a-zA-Z0-9_-]+$")


#: ``* [trigger: <trigger-name>; id: <task-id>] ...`` deferred task
#: list-items.  The trigger + id capture groups are the parser's
#: primary keys.
_DEFERRED_TASK_RE = re.compile(
    r"^\*\s+\[trigger:\s*(?P<trigger>\S+);\s*id:\s*(?P<id>\S+)[^\]]*\]\s*$",
)


#: ``* [seed; id: <task-id>] ...`` seed list-items (for completeness;
#: derived-state helpers parse these too).
_SEED_TASK_RE = re.compile(
    r"^\*\s+\[seed;\s*id:\s*(?P<id>\S+)[^\]]*\]\s*$",
)


#: Slot opener / closer.
_SLOT_OPEN_RE = re.compile(r"<!--\s*cairn:slot\s+" + SLOT_NAME + r"\s*-->")


_SLOT_CLOSE_RE = re.compile(r"<!--\s*cairn:end\s+" + SLOT_NAME + r"\s*-->")


@dataclass(frozen=True)
class DeferredTask:
    """A ``[trigger: X; id: Y]`` list-item from a preset source file.

    ``body`` is the multi-line markdown block (header line +
    indented continuation lines) ready to inline into PLANNING.
    """

    trigger: str
    task_id: str
    body: str


def find_slot_body(planning_text: str) -> tuple[int, int, str] | None:
    """Return ``(body_start, body_end, body)`` for the slot, where
    *body* is the text **between** the cairn:slot / cairn:end markers
    (excluding the markers themselves) and *body_start* / *body_end*
    are absolute character offsets into *planning_text*.  Returns
    ``None`` if the slot is not found or unpaired.
    """
    m_open = _SLOT_OPEN_RE.search(planning_text)
    if m_open is None:
        return None
    body_start = m_open.end()
    m_close = _SLOT_CLOSE_RE.search(planning_text, body_start)
    if m_close is None:
        return None
    body_end = m_close.start()
    return body_start, body_end, planning_text[body_start:body_end]


def extract_preset_from_slot(planning_text: str) -> str | None:
    """Read the ``<!-- preset: <name> -->`` metadata comment from
    inside the ``onboarding-tasks`` slot body.  Returns the preset
    name, or ``None`` if no metadata is present.

    Defense-in-depth: although ``_PRESET_META_RE`` already restricts
    the capture group to ``[a-zA-Z0-9_-]+``, the extracted name is
    re-validated through ``_PRESET_NAME_RE`` before return.  Any
    mismatch raises ``OnboardingSecurityError`` so a future
    accidental loosening of the regex cannot silently propagate
    attacker-controlled path components into ``dev/modules/
    onboarding/<preset>.md``.
    """
    found = find_slot_body(planning_text)
    if found is None:
        return None
    _, _, body = found
    m = _PRESET_META_RE.search(body)
    if m is None:
        return None
    name = m.group(1)
    if not _PRESET_NAME_RE.match(name):
        raise OnboardingSecurityError(
            f"refusing to use preset name with disallowed characters: "
            f"{name!r} (must match {_PRESET_NAME_RE.pattern})"
        )
    return name


def parse_deferred_tasks(preset_text: str) -> list[DeferredTask]:
    """Extract ``[trigger: X; id: Y]`` list-items from a preset source
    file.  Each task is captured with its indented continuation
    body so the activation step can inline a complete markdown
    list-item into PLANNING.
    """
    out: list[DeferredTask] = []
    current_header: re.Match[str] | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_header, current_lines
        if current_header is not None:
            body = "\n".join(current_lines).rstrip()
            out.append(
                DeferredTask(
                    trigger=current_header.group("trigger"),
                    task_id=current_header.group("id"),
                    body=body,
                )
            )
        current_header = None
        current_lines = []

    for line in preset_text.splitlines():
        m = _DEFERRED_TASK_RE.match(line)
        if m is not None:
            flush()
            current_header = m
            current_lines = [line]
            continue
        if current_header is None:
            continue
        # Continuation if indented (>= 2 spaces) or empty; otherwise
        # the current task ends.
        if line.startswith("  ") or line.startswith("\t"):
            current_lines.append(line)
        elif line.strip() == "":
            current_lines.append(line)
        else:
            flush()
    flush()
    return out


def extract_seed_task_blocks(preset_text: str) -> list[str]:
    """Extract seed-task entries as multi-line markdown blocks.

    Parallel to ``bootstrap.scaffold._extract_seed_tasks`` (helper-
    side copy so --seed works without a Cairn checkout).  Each block
    preserves the `* [seed; id: ...]` header line + any indented
    continuation lines until the next top-level item or blank line.
    """
    blocks: list[str] = []
    current: list[str] = []
    in_seed = False
    for line in preset_text.splitlines():
        if _SEED_TASK_RE.match(line):
            if current:
                blocks.append("\n".join(current).rstrip())
                current = []
            current.append(line)
            in_seed = True
            continue
        if not in_seed:
            continue
        if line.startswith("  ") or line.startswith("\t"):
            current.append(line)
        elif line.strip() == "":
            current.append(line)
        else:
            blocks.append("\n".join(current).rstrip())
            current = []
            in_seed = False
    if current:
        blocks.append("\n".join(current).rstrip())
    return blocks


def parse_seed_task_ids(preset_text: str) -> list[str]:
    """Extract the task ids of `[seed; id: Y]` items.  Used by
    derived-state helpers to enumerate the full task set declared in
    a preset source file.
    """
    ids: list[str] = []
    for line in preset_text.splitlines():
        m = _SEED_TASK_RE.match(line)
        if m is not None:
            ids.append(m.group("id"))
    return ids


VALID_PRESETS = ("solo-greenfield", "collaborative-team", "high-rigor-legacy")
