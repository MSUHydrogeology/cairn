#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""onboarding-activate engine -- activation records, log I/O + computation.

The activation state model and the activate() machinery's data layer: the
``ActivationRecord`` schema + JSONL activation-log read/write
(``append_activation_log`` / ``read_activation_log`` / ``activated_task_ids``),
the ``PendingActivation`` / ``ActivationOutcome`` results, and
``compute_activations`` / ``render_appended_slot_body`` / ``update_planning_slot``.
Depends on the containment leaf (``security``) for the read + write guards and on
the slot-parse leaf (``slotparse``) for ``DeferredTask`` + ``find_slot_body``.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass

from .security import _assert_safe_read, _assert_safe_write
from .slotparse import DeferredTask, find_slot_body


@dataclass(frozen=True)
class ActivationRecord:
    """One line in ``onboarding-activated.jsonl``.

    Schema (the log is the only durable state; the plan's state-file
    design):

    * ``task-id``: stable id from the source file's
      ``[trigger: X; id: Y]`` header.
    * ``activated-at``: ISO-8601 UTC timestamp.
    * ``by-agent``: identifier of the agent / runner that performed
      the activation.
    * ``source-preset``: the preset name (resolved from PLANNING's
      ``<!-- preset: <name> -->`` metadata).
    * ``trigger``: the trigger that caused the activation.
    """

    task_id: str
    activated_at: str
    by_agent: str
    source_preset: str
    trigger: str

    def to_jsonl(self) -> str:
        return json.dumps(
            {
                "task-id": self.task_id,
                "activated-at": self.activated_at,
                "by-agent": self.by_agent,
                "source-preset": self.source_preset,
                "trigger": self.trigger,
            },
            sort_keys=True,
        )

    @classmethod
    def from_jsonl_line(cls, line: str) -> "ActivationRecord | None":
        line = line.strip()
        if not line or line.startswith("#"):
            return None
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            return None
        try:
            return cls(
                task_id=str(obj["task-id"]),
                activated_at=str(obj["activated-at"]),
                by_agent=str(obj["by-agent"]),
                source_preset=str(obj["source-preset"]),
                trigger=str(obj["trigger"]),
            )
        except KeyError:
            return None


def read_activation_log(
    log_path: Path, target: Path | None = None,
) -> list[ActivationRecord]:
    """Read all records from the JSONL log.  A missing file is
    treated as an empty log (the scaffold creates an empty file at
    install time, so missing-file means an adopter who never ran the
    scaffold against this tree).

    Optional ``target`` enables the containment guard: when supplied,
    ``_assert_safe_read(log_path, target)`` runs before the read so a
    symlinked log path is refused.  Production call sites in
    ``activate()`` always pass ``target``; test fixtures may omit it
    when exercising controlled paths.
    """
    if not log_path.is_file():
        return []
    if target is not None:
        _assert_safe_read(log_path, target)
    out: list[ActivationRecord] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        rec = ActivationRecord.from_jsonl_line(line)
        if rec is not None:
            out.append(rec)
    return out


def activated_task_ids(records: Iterable[ActivationRecord]) -> set[str]:
    """The set of task ids that have been activated at some point.
    Used for idempotency: an id in this set never re-activates."""
    return {r.task_id for r in records}


@dataclass(frozen=True)
class PendingActivation:
    """A task ready to activate: source-file deferred task + the
    trigger that newly fired (one of the task's allowable triggers).
    """

    task: DeferredTask
    trigger: str


def compute_activations(
    deferred: list[DeferredTask],
    fired_triggers: set[str],
    already_activated_ids: set[str],
) -> list[PendingActivation]:
    """Return the diff: deferred tasks whose trigger has fired AND
    whose id is not yet in the activation log.

    Order matches the deferred-tasks list (which preserves source
    file ordering) -- predictable for testing + reproducible output.
    """
    out: list[PendingActivation] = []
    for task in deferred:
        if task.task_id in already_activated_ids:
            continue
        if task.trigger not in fired_triggers:
            continue
        out.append(PendingActivation(task=task, trigger=task.trigger))
    return out


def render_appended_slot_body(
    current_body: str,
    pending: list[PendingActivation],
) -> str:
    """Render the new slot body: keep the existing body content +
    append the newly-activated tasks (each as its full
    multi-line markdown list-item)."""
    parts = [current_body.rstrip("\n")]
    for p in pending:
        parts.extend(["", p.task.body.rstrip("\n")])
    return "\n".join(parts).rstrip() + "\n"


def update_planning_slot(planning_text: str, new_body: str) -> str | None:
    """Substitute the slot body in *planning_text* with *new_body*.
    Returns the new text, or ``None`` if the slot is not found."""
    found = find_slot_body(planning_text)
    if found is None:
        return None
    body_start, body_end, _ = found
    return (
        planning_text[:body_start]
        + "\n"
        + new_body.strip("\n")
        + "\n"
        + planning_text[body_end:]
    )


def append_activation_log(
    log_path: Path,
    records: list[ActivationRecord],
    target: Path | None = None,
) -> None:
    """Atomic-append each record's JSONL line to the log.

    Matches the intent log's precedent for true POSIX-atomic append:
    ``os.open`` with ``O_WRONLY|O_APPEND|O_CREAT`` + a single
    ``os.write(fd, bytes)`` per record.  This guarantees the kernel performs the seek-to-end
    + write atomically (single line is shorter than ``PIPE_BUF``);
    Python-level line-buffered ``open(... 'a', buffering=1)`` does
    NOT make this contract.  Partial-write detection raises so a
    silent truncation surfaces loudly.

    Optional ``target`` enables the containment guard.  When supplied
    the ordering is ``mkdir → assert``: the parent directory is
    created first, then ``_assert_safe_write(log_path, target)``
    runs so ``resolve()`` operates on an existing parent.  Production
    call sites in
    ``activate()`` always pass ``target``; test fixtures may omit it
    when exercising controlled paths.
    """
    if not records:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if target is not None:
        # mkdir → assert ordering: parent now exists, so resolve() in
        # the guard operates on a real directory rather than a
        # non-existent path.
        _assert_safe_write(log_path, target)
    fd = os.open(
        str(log_path),
        os.O_WRONLY | os.O_APPEND | os.O_CREAT,
        0o644,
    )
    try:
        for rec in records:
            payload = (rec.to_jsonl() + "\n").encode("utf-8")
            written = os.write(fd, payload)
            if written != len(payload):
                raise IOError(
                    f"partial write to {log_path}: wrote {written} "
                    f"of {len(payload)} bytes (load-bearing atomicity "
                    f"contract broken; investigate filesystem / "
                    f"platform interaction)"
                )
    finally:
        os.close(fd)


@dataclass(frozen=True)
class ActivationOutcome:
    """Result of one ``activate(...)`` run.

    Extended with active-surfacing prompt outputs:

    * ``active_prompt_row`` -- the active-surfacing row name that
      fired this goodnight (or ``None`` if no row qualifies under
      UX caps + priority).
    * ``active_prompt_body`` -- the prompt content the helper
      would emit to the terminal (the per-preset content extracted
      from the installed source file).
    * ``deferred_over_cap`` -- pending activations beyond the
      ``MAX_NEW_TASKS_PER_GOODNIGHT`` UX cap; they re-emerge at
      the next goodnight.
    """

    preset: str | None
    pending: list[PendingActivation]
    planning_updated: bool
    log_records: list[ActivationRecord]
    active_prompt_row: str | None = None
    active_prompt_body: str | None = None
    deferred_over_cap: tuple[PendingActivation, ...] = ()
