#!/usr/bin/env python3
"""onboarding_activate.py -- progressive-onboarding activation helper.

The goodnight full-handoff owner runs this helper at the standing
goodnight foldback-capture step (per `doctrine/session-routines.md`
extension landed in Chunk P1.3): it scans the deployment for fired
triggers and activates the corresponding deferred onboarding tasks
into `dev/PLANNING.md`'s `onboarding-tasks` slot, recording each
activation as one line in `dev/.cairn/onboarding-activated.jsonl`.

Plan: ``2026-05-28-claude-cairn-progressive-onboarding`` (Chunk
P1.2 ships the core helper + state-file schema; P1.9a/b ship the
trigger-evaluation engine; P1.10a/b ship active-surfacing emission +
UX caps; P1.11 ships ``--seed`` for existing-adopter opt-in).

Reads:
* ``dev/PLANNING.md``'s ``<!-- cairn:slot onboarding-tasks -->`` block
  for the ``<!-- preset: <name> -->`` metadata comment (Codex P2-4
  contract: scaffold + ``--seed`` both write this comment so the
  helper resolves the installed source file uniformly across install
  paths).
* ``dev/.cairn/onboarding-activated.jsonl`` -- the **tracked**
  append-only activation log (Codex P2-5 decision: tracked, parallel
  to ``dev/intents.jsonl`` precedent; edits land at the goodnight
  serialization point only).
* ``dev/modules/onboarding/<preset>.md`` -- the installed source file
  carrying ``[trigger: X; id: Y]`` deferred-task list-items and (in
  later chunks) active-surfacing prompt-content metadata blocks.

Writes:
* Updates ``dev/PLANNING.md``'s slot body with newly-activated tasks.
* Appends one line per activation to
  ``dev/.cairn/onboarding-activated.jsonl``.

CLI::

    python scripts/onboarding_activate.py            # default: scan + activate
    python scripts/onboarding_activate.py --dry-run  # show plan, no writes
    python scripts/onboarding_activate.py --seed     # P1.11 (errors in P1.2)

Idempotency: re-running on unchanged deployment state is a no-op.
The activation log is the authoritative record of "already
activated"; tasks whose id appears in the log do not re-fire.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .security import (  # noqa: F401  (re-exported for the facade)
    OnboardingError,
    OnboardingSecurityError,
    _assert_safe_dir_for_glob,
    _assert_safe_read,
    _assert_safe_write,
)
from .shared import (  # noqa: F401  (re-exported for the facade)
    DEFAULT_LOG_REL,
    DEFAULT_MODULES_ONBOARDING_REL,
    DEFAULT_PLANNING_REL,
    default_agent_identity,
    utc_now_iso,
)
from .prompts import (  # noqa: F401  (re-exported for the facade)
    MAX_ACTIVE_PROMPTS_PER_GOODNIGHT,
    MAX_NEW_TASKS_PER_GOODNIGHT,
    _ACTIVE_SURFACING_ROWS,
    _PROMPT_HEADING_RE_CACHE,
    _prompt_heading_re,
    render_active_surfacing_prompt,
    render_outcome_with_active_prompt,
    select_active_prompt_to_fire,
)
from .slotparse import (  # noqa: F401  (re-exported for the facade)
    DeferredTask,
    SLOT_NAME,
    VALID_PRESETS,
    _DEFERRED_TASK_RE,
    _PRESET_META_RE,
    _PRESET_NAME_RE,
    _SEED_TASK_RE,
    _SLOT_CLOSE_RE,
    _SLOT_OPEN_RE,
    extract_preset_from_slot,
    extract_seed_task_blocks,
    find_slot_body,
    parse_deferred_tasks,
    parse_seed_task_ids,
)
from .triggers import (  # noqa: F401  (re-exported for the facade)
    LEVEL_1_DEEPEN_PLANS_THRESHOLD,
    LEVEL_1_DEEPEN_PROPOSALS_THRESHOLD,
    LEVEL_2_DEEPEN_PLANS_THRESHOLD,
    LEVEL_2_DEEPEN_PROPOSALS_THRESHOLD,
    _AGENT_VENDOR_PATTERNS,
    _HUMAN_MAINTAINER_PATTERNS,
    _author_vendor_in_file,
    _count_archived_plans,
    _count_archived_proposals,
    _count_distinct_agents_in_roster,
    _foldback_has_open_candidate,
    _has_cross_type_review_anywhere,
    _has_cross_type_review_in_file,
    _list_plan_files,
    _list_proposal_files,
    _read_team_roster_body,
    _team_roster_is_unfilled,
    _unreleased_changelog_has_content,
    evaluate_action_triggers,
    evaluate_maturity_triggers,
    evaluate_triggers,
)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ActivationRecord:
    """One line in ``onboarding-activated.jsonl``.

    Schema (Codex P2-5 + the plan's state-file design):

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


# ---------------------------------------------------------------------------
# Reading + parsing
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Activation computation + writing
# ---------------------------------------------------------------------------


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

    Matches the ``modflow_tools/tools/intent.py`` precedent for true
    POSIX-atomic append per Claude External code review P2-1 +
    Antigravity confirmation: ``os.open`` with
    ``O_WRONLY|O_APPEND|O_CREAT`` + a single ``os.write(fd, bytes)``
    per record.  This guarantees the kernel performs the seek-to-end
    + write atomically (single line is shorter than ``PIPE_BUF``);
    Python-level line-buffered ``open(... 'a', buffering=1)`` does
    NOT make this contract.  Partial-write detection raises so a
    silent truncation surfaces loudly.

    Optional ``target`` enables the containment guard.  When supplied
    the ordering is ``mkdir → assert``: the parent directory is
    created first, then ``_assert_safe_write(log_path, target)``
    runs so ``resolve()`` operates on an existing parent (Antigravity
    plan-review P2-1 disposition).  Production call sites in
    ``activate()`` always pass ``target``; test fixtures may omit it
    when exercising controlled paths.
    """
    if not records:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if target is not None:
        # mkdir → assert ordering: parent now exists, so resolve() in
        # the guard operates on a real directory rather than a
        # non-existent path (Antigravity plan-review P2-1).
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


# ---------------------------------------------------------------------------
# Top-level activate() flow
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ActivationOutcome:
    """Result of one ``activate(...)`` run.

    Extended in P1.10a with active-surfacing prompt outputs:

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


def activate(
    target: Path,
    *,
    by_agent: str | None = None,
    dry_run: bool = False,
    fired_triggers_override: set[str] | None = None,
) -> ActivationOutcome:
    """Top-level activation flow.

    1. Read PLANNING.md.
    2. Resolve preset from the slot's `<!-- preset: <name> -->`
       metadata comment (raises if missing -- the recoverable error
       message points the maintainer at the `--seed` path).
    3. Read the installed source file at
       ``dev/modules/onboarding/<preset>.md``.
    4. Parse its deferred tasks.
    5. Read the activation log; collect already-activated ids.
    6. Evaluate triggers (P1.2 stub; P1.9 replaces).
    7. Compute the activation diff.
    8. If not dry-run: write the updated PLANNING + append log lines.

    Returns the ``ActivationOutcome``.  Idempotent: a run with no
    eligible tasks returns an outcome with empty ``pending``,
    ``planning_updated=False``, and empty ``log_records``.
    """
    planning_path = target / DEFAULT_PLANNING_REL
    if not planning_path.is_file():
        raise OnboardingError(
            f"PLANNING.md not found at {planning_path}; this command "
            f"expects an adopter tree scaffolded by Cairn's bootstrap."
        )
    _assert_safe_read(planning_path, target)
    planning_text = planning_path.read_text(encoding="utf-8")

    found = find_slot_body(planning_text)
    if found is None:
        raise OnboardingError(
            f"`cairn:slot {SLOT_NAME}` not found in {planning_path}; "
            f"is your PLANNING.md from a Cairn scaffold of >= the "
            f"plan-2026-05-28 progressive-onboarding update?"
        )

    # ``extract_preset_from_slot`` validates the captured name
    # through ``_PRESET_NAME_RE`` and raises ``OnboardingSecurityError``
    # if it fails — defense-in-depth against any future regex
    # loosening that would otherwise pass attacker-controlled
    # characters into the ``{preset}.md`` path concatenation below.
    preset = extract_preset_from_slot(planning_text)
    if preset is None:
        raise OnboardingError(
            f"PLANNING.md's `{SLOT_NAME}` slot has no "
            f"`<!-- preset: <name> -->` metadata; bootstrap a preset "
            f"via `python scripts/onboarding_activate.py --seed "
            f"[--preset <name>]` (P1.11; coming in a later chunk)."
        )

    source_path = (
        target / DEFAULT_MODULES_ONBOARDING_REL / f"{preset}.md"
    )
    if not source_path.is_file():
        raise OnboardingError(
            f"installed onboarding source file not found at "
            f"{source_path}; was the scaffold run with `preset: "
            f"{preset}`?"
        )
    _assert_safe_read(source_path, target)
    source_text = source_path.read_text(encoding="utf-8")

    deferred = parse_deferred_tasks(source_text)
    log_path = target / DEFAULT_LOG_REL
    existing_records = read_activation_log(log_path, target=target)
    already = activated_task_ids(existing_records)

    if fired_triggers_override is None:
        fired = evaluate_triggers(target, log_records=existing_records)
    else:
        fired = fired_triggers_override

    pending_all = compute_activations(deferred, fired, already)

    # UX cap: at most MAX_NEW_TASKS_PER_GOODNIGHT new tasks per
    # goodnight; overflow defers to the next goodnight (the
    # held-tasks derived state re-surfaces them).
    pending = pending_all[:MAX_NEW_TASKS_PER_GOODNIGHT]
    deferred_over_cap = tuple(pending_all[MAX_NEW_TASKS_PER_GOODNIGHT:])

    # Select at most MAX_ACTIVE_PROMPTS_PER_GOODNIGHT active-surfacing
    # row (the cap is 1; the select function returns the highest-
    # priority unmuted row).
    active_row = select_active_prompt_to_fire(fired, existing_records)
    active_body: str | None = None
    if active_row is not None:
        active_body = render_active_surfacing_prompt(source_text, active_row)

    if not pending and active_row is None:
        return ActivationOutcome(
            preset=preset,
            pending=[],
            planning_updated=False,
            log_records=[],
            deferred_over_cap=deferred_over_cap,
        )

    agent_id = by_agent or default_agent_identity()
    ts = utc_now_iso()
    new_records: list[ActivationRecord] = [
        ActivationRecord(
            task_id=p.task.task_id,
            activated_at=ts,
            by_agent=agent_id,
            source_preset=preset,
            trigger=p.trigger,
        )
        for p in pending
    ]
    if active_row is not None:
        # Record the active-surfacing emission with a marker prefix
        # so idempotency (don't re-fire the prompt) carries forward.
        new_records.append(
            ActivationRecord(
                task_id=f"active-surface:{active_row}",
                activated_at=ts,
                by_agent=agent_id,
                source_preset=preset,
                trigger=f"active-surface:{active_row}",
            )
        )

    if dry_run:
        return ActivationOutcome(
            preset=preset,
            pending=pending,
            planning_updated=False,
            log_records=new_records,
            active_prompt_row=active_row,
            active_prompt_body=active_body,
            deferred_over_cap=deferred_over_cap,
        )

    # Persist: PLANNING slot first (if there are pending tasks), then
    # append log.  Active-surfacing prompts are emitted via the
    # outcome (no PLANNING write -- the prompt is terminal output).
    planning_updated = False
    if pending:
        _, _, current_body = found
        new_body = render_appended_slot_body(current_body, pending)
        new_planning = update_planning_slot(planning_text, new_body)
        if new_planning is None:
            raise OnboardingError(
                f"PLANNING.md slot disappeared between read + write -- "
                f"concurrent edit?  Re-run after coordinating."
            )
        # planning_path.parent is the adopter's ``dev/`` directory and
        # is guaranteed to exist (we already read PLANNING.md from it
        # above), so no mkdir is required here.
        _assert_safe_write(planning_path, target)
        planning_path.write_text(new_planning, encoding="utf-8")
        planning_updated = True
    append_activation_log(log_path, new_records, target=target)

    return ActivationOutcome(
        preset=preset,
        pending=pending,
        planning_updated=planning_updated,
        log_records=new_records,
        active_prompt_row=active_row,
        active_prompt_body=active_body,
        deferred_over_cap=deferred_over_cap,
    )


# ---------------------------------------------------------------------------
# Derived state (held / completed)
# ---------------------------------------------------------------------------


def derive_held_task_ids(
    source_text: str, log_records: list[ActivationRecord],
) -> list[str]:
    """Held tasks = source-file deferred task ids - log-recorded
    activations.  These are the tasks awaiting their trigger.

    Derived (not persisted) per Codex P2-5: the log is the only
    durable state; held / completed are computed each goodnight from
    source + log + PLANNING.
    """
    activated = activated_task_ids(log_records)
    return [
        t.task_id for t in parse_deferred_tasks(source_text)
        if t.task_id not in activated
    ]


def derive_completed_task_ids(
    log_records: list[ActivationRecord], current_planning_slot_body: str,
) -> list[str]:
    """Completed tasks = log-recorded activations whose id no longer
    appears in PLANNING's slot body.  The PLANNING-removal pattern
    (item is removed when done; the standard `doctrine/lifecycle.md`
    rule) thus surfaces completion without an explicit "completed"
    flag.
    """
    completed: list[str] = []
    for rec in log_records:
        if f"id: {rec.task_id}" not in current_planning_slot_body:
            completed.append(rec.task_id)
    return completed


# ---------------------------------------------------------------------------
# --seed mode (existing-adopter opt-in; Chunk P1.11)
# ---------------------------------------------------------------------------


def seed_existing_adopter(
    target: Path,
    *,
    preset_name: str | None,
    interactive: bool = True,
    dry_run: bool = False,
) -> str:
    """Existing-adopter opt-in path (Chunk P1.11).

    Performs the `--seed` flow:

    1. Resolve preset: from *preset_name* if provided; else
       interactive prompt (when *interactive* is True); else error.
    2. Read the preset source file -- the adopter MUST have
       installed it at ``<target>/dev/modules/onboarding/<preset>.md``
       before invoking --seed (per the manual recipe in
       ``doctrine/onboarding.md``).  Recoverable error if absent.
    3. Locate the ``cairn:slot onboarding-tasks`` block in
       PLANNING.md.  Recoverable error if not present (the adopter
       needs to paste the slot block first).
    4. Render the slot body (``<!-- preset: <name> -->`` metadata
       comment + seed tasks extracted from the source file).
    5. Write the new PLANNING.md.

    Idempotent: re-running --seed against a slot that already
    carries the preset metadata is a no-op (returns "already
    seeded" + makes no changes).

    Returns a one-line summary string for the CLI to print.
    """
    if preset_name is None:
        if not interactive:
            raise OnboardingError(
                "--seed requires --preset <name> when run non-"
                "interactively.  Valid presets: "
                + ", ".join(VALID_PRESETS)
            )
        preset_name = _interactive_preset_prompt()
    # Format validation FIRST (before the allowlist) so an attacker-
    # supplied ``--preset ../etc/passwd`` raises a clear security
    # error rather than an "unknown preset" message.  The allowlist
    # also catches it, but the security error code (exit 2) is more
    # diagnostic for automation wrappers.
    if not _PRESET_NAME_RE.match(preset_name):
        raise OnboardingSecurityError(
            f"refusing preset name with disallowed characters: "
            f"{preset_name!r} (must match {_PRESET_NAME_RE.pattern})"
        )
    if preset_name not in VALID_PRESETS:
        raise OnboardingError(
            f"unknown preset {preset_name!r}; valid: "
            + ", ".join(VALID_PRESETS)
        )

    # Step 2: read PLANNING + locate slot (do this BEFORE checking
    # the source file so the idempotency no-op fires even if the
    # source file isn't present yet).
    planning_path = target / DEFAULT_PLANNING_REL
    if not planning_path.is_file():
        raise OnboardingError(
            f"PLANNING.md not found at {planning_path}; this command "
            f"expects an adopter tree with a `dev/PLANNING.md`."
        )
    _assert_safe_read(planning_path, target)
    planning_text = planning_path.read_text(encoding="utf-8")
    found = find_slot_body(planning_text)
    if found is None:
        raise OnboardingError(
            f"`cairn:slot {SLOT_NAME}` not found in {planning_path}.  "
            f"Paste the slot block into your PLANNING.md first (per "
            f"doctrine/onboarding.md > Existing-adopter manual opt-in "
            f"path, Step 1)."
        )

    # Idempotency: if slot already has preset metadata, no-op.
    existing_preset = extract_preset_from_slot(planning_text)
    if existing_preset is not None:
        return (
            f"--seed: slot already carries preset metadata "
            f"({existing_preset!r}); no-op."
        )

    # Step 3: read preset source from the adopter's installed copy.
    source_path = (
        target / DEFAULT_MODULES_ONBOARDING_REL / f"{preset_name}.md"
    )
    if not source_path.is_file():
        raise OnboardingError(
            f"installed preset source not found at {source_path}.  "
            f"Copy `cairn/templates/onboarding/{preset_name}.md` to "
            f"that path first (per doctrine/onboarding.md > "
            f"Existing-adopter manual opt-in path)."
        )
    _assert_safe_read(source_path, target)
    source_text = source_path.read_text(encoding="utf-8")

    # Step 4: render the new slot body.
    seed_blocks = extract_seed_task_blocks(source_text)
    new_body = _render_onboarding_slot_seed(preset_name, seed_blocks)

    # Step 5: write the new PLANNING.
    new_text = _substitute_slot_body(planning_text, found, new_body)
    if dry_run:
        return (
            f"--seed [dry-run]: would write preset={preset_name!r} "
            f"metadata + {len(seed_blocks)} seed task(s) into "
            f"{planning_path}."
        )
    # ``planning_path.parent`` is the adopter's ``dev/`` directory and
    # was confirmed present by the ``is_file()`` check above.  No mkdir
    # required; guard runs immediately before the write.
    _assert_safe_write(planning_path, target)
    planning_path.write_text(new_text, encoding="utf-8")
    return (
        f"--seed: wrote preset={preset_name!r} metadata + "
        f"{len(seed_blocks)} seed task(s) into {planning_path}."
    )


def _interactive_preset_prompt() -> str:
    """Prompt the user to pick a preset (TTY input).  Returns the
    chosen preset name (one of VALID_PRESETS)."""
    print("Choose a preset:")
    for i, p in enumerate(VALID_PRESETS, 1):
        print(f"  {i}. {p}")
    raw = input("Enter 1-3 or preset name: ").strip()
    if raw in VALID_PRESETS:
        return raw
    if raw.isdigit() and 1 <= int(raw) <= len(VALID_PRESETS):
        return VALID_PRESETS[int(raw) - 1]
    raise OnboardingError(f"invalid preset selection: {raw!r}")


def _render_onboarding_slot_seed(
    preset_name: str, seed_blocks: list[str],
) -> str:
    """Render the slot body for --seed: identical shape to the
    scaffold-path render (`<!-- preset: <name> -->` + seed blocks),
    preserving the uniformity contract per Codex P2-4."""
    parts = [f"<!-- preset: {preset_name} -->", ""]
    parts.extend(seed_blocks)
    return "\n".join(parts).rstrip() + "\n"


def _substitute_slot_body(
    planning_text: str, found: tuple[int, int, str], new_body: str,
) -> str:
    """Replace the slot body with *new_body*."""
    body_start, body_end, _ = found
    return (
        planning_text[:body_start]
        + "\n"
        + new_body.strip("\n")
        + "\n"
        + planning_text[body_end:]
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _format_outcome_summary(outcome: ActivationOutcome) -> str:
    if not outcome.pending and outcome.active_prompt_row is None:
        return (
            f"onboarding_activate: no eligible activations or "
            f"prompts (preset={outcome.preset!r})."
        )
    lines: list[str] = []
    if outcome.pending:
        lines.append(
            f"onboarding_activate: {len(outcome.pending)} task "
            f"activation(s) (preset={outcome.preset!r}):"
        )
        for p in outcome.pending:
            lines.append(
                f"  * id={p.task.task_id}  trigger={p.trigger}"
            )
    if outcome.deferred_over_cap:
        lines.append(
            f"  ({len(outcome.deferred_over_cap)} additional "
            f"activation(s) deferred to the next goodnight per UX cap "
            f"of {MAX_NEW_TASKS_PER_GOODNIGHT}/goodnight)."
        )
    if outcome.active_prompt_row is not None:
        lines.append("")
        lines.append(
            f"--- Active-surfacing prompt: {outcome.active_prompt_row} ---"
        )
        body = outcome.active_prompt_body or "(no content)"
        lines.append(body)
        lines.append("--- end prompt ---")
    lines.append(
        f"PLANNING updated: {outcome.planning_updated}; log appended: "
        f"{len(outcome.log_records)} line(s)."
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="onboarding_activate.py",
        description=(
            "Progressive-onboarding activation helper (run at "
            "goodnight; per doctrine/onboarding.md)."
        ),
    )
    parser.add_argument(
        "--target",
        default=".",
        help="Adopter-tree root (default: cwd).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the activation plan without writing.",
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help=(
            "Existing-adopter opt-in seed mode (Chunk P1.11; the "
            "implementation lands in a later chunk)."
        ),
    )
    parser.add_argument(
        "--preset",
        default=None,
        help=(
            "Used with --seed to declare the preset; ignored in "
            "default mode (preset is read from PLANNING slot metadata)."
        ),
    )
    args = parser.parse_args(argv)

    target = Path(args.target).resolve()
    if args.seed:
        try:
            summary = seed_existing_adopter(
                target,
                preset_name=args.preset,
                interactive=sys.stdin.isatty(),
                dry_run=args.dry_run,
            )
        except OnboardingSecurityError as exc:
            # Containment refusal: distinct exit code 2 so automation
            # can tell security failures apart from operational ones
            # (Antigravity plan-review P3-1 disposition).
            print(f"security error: {exc}", file=sys.stderr)
            return 2
        except OnboardingError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(summary)
        return 0

    try:
        outcome = activate(target, dry_run=args.dry_run)
    except OnboardingSecurityError as exc:
        # Per Antigravity plan-review P3-1: distinct exit code for
        # containment failures.
        print(f"security error: {exc}", file=sys.stderr)
        return 2
    except OnboardingError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(_format_outcome_summary(outcome))
    return 0


if __name__ == "__main__":
    sys.exit(main())
