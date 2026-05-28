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


# ---------------------------------------------------------------------------
# Defaults + regex patterns
# ---------------------------------------------------------------------------

#: Default location of the tracked activation log inside the adopter's
#: deliberation tree.  Per Codex P2-5: tracked, parallel to
#: dev/intents.jsonl; the scaffold seeds it as empty at install time
#: so adopters never see lazy-mkdir behavior.
DEFAULT_LOG_REL = "dev/.cairn/onboarding-activated.jsonl"

#: Default location of PLANNING.md.
DEFAULT_PLANNING_REL = "dev/PLANNING.md"

#: Directory under the adopter tree where preset source files install.
DEFAULT_MODULES_ONBOARDING_REL = "dev/modules/onboarding"

#: The slot name the helper reads + writes.
SLOT_NAME = "onboarding-tasks"

#: ``<!-- preset: <name> -->`` metadata comment inside the slot.
_PRESET_META_RE = re.compile(r"<!--\s*preset:\s*(\S+)\s*-->")

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


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DeferredTask:
    """A ``[trigger: X; id: Y]`` list-item from a preset source file.

    ``body`` is the multi-line markdown block (header line +
    indented continuation lines) ready to inline into PLANNING.
    """

    trigger: str
    task_id: str
    body: str


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
    """
    found = find_slot_body(planning_text)
    if found is None:
        return None
    _, _, body = found
    m = _PRESET_META_RE.search(body)
    return m.group(1) if m else None


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


def read_activation_log(log_path: Path) -> list[ActivationRecord]:
    """Read all records from the JSONL log.  A missing file is
    treated as an empty log (the scaffold creates an empty file at
    install time, so missing-file means an adopter who never ran the
    scaffold against this tree)."""
    if not log_path.is_file():
        return []
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
# Trigger evaluation
# ---------------------------------------------------------------------------
#
# Per plan 2026-05-28-claude-cairn-progressive-onboarding (Codex
# External Review P2-3): triggers evaluate against EXPLICIT
# deployment state (filesystem + roster + ledger) wherever possible,
# NOT git archaeology.  The collab-agreement-signing trigger evaluator
# uses a "first-proposal-archived has fired" precondition recorded in
# the activation log -- the log IS the explicit state for prior
# trigger fires.
#
# The trigger matrix lives in two families:
# * Maturity-ladder triggers (P1.9a, this section): level-0-to-1,
#   level-1-to-2, level-1-deepen, level-2-deepen.
# * Action triggers (P1.9b, next section): first-proposal-opened,
#   first-proposal-archived, first-plan-opened, first-plan-archived,
#   first-changelog-entry, second-agent-type, first-cross-type-review,
#   first-foldback-candidate, collab-agreement-signing.


# Deepen-within-level thresholds (named here so doctrine + tests
# share the same constants).
LEVEL_1_DEEPEN_PROPOSALS_THRESHOLD = 5
LEVEL_1_DEEPEN_PLANS_THRESHOLD = 3
LEVEL_2_DEEPEN_PROPOSALS_THRESHOLD = 15
LEVEL_2_DEEPEN_PLANS_THRESHOLD = 10


def _count_archived_proposals(target: Path) -> int:
    archive = target / "dev" / "proposals" / "archive"
    if not archive.is_dir():
        return 0
    return sum(
        1 for p in archive.glob("*.md")
        if p.is_file() and p.name != "_template.md"
    )


def _count_archived_plans(target: Path) -> int:
    archive = target / "dev" / "plans" / "archive"
    if not archive.is_dir():
        return 0
    return sum(
        1 for p in archive.glob("*.md")
        if p.is_file() and p.name != "_template.md"
    )


def evaluate_maturity_triggers(target: Path) -> set[str]:
    """Maturity-ladder trigger evaluators (Chunk P1.9a).

    Each trigger observes filesystem state (Codex P2-3 explicit-state
    contract):

    * ``level-0-to-1`` -- ``dev/proposals/_template.md`` present
      (canonical Level 1 signal: adopter graduated from "read the
      doctrine" to "hand-copy the kernel").
    * ``level-1-to-2`` -- ``dev/cairn-lock.yml`` present (canonical
      Level 2 signal per ``bootstrap/UPGRADE.md`` doctrine).
    * ``level-1-deepen`` -- ``level-1-to-2`` NOT fired AND archived
      proposals >= LEVEL_1_DEEPEN_PROPOSALS_THRESHOLD AND archived
      plans >= LEVEL_1_DEEPEN_PLANS_THRESHOLD.
    * ``level-2-deepen`` -- ``level-1-to-2`` IS fired AND archived
      proposals >= LEVEL_2_DEEPEN_PROPOSALS_THRESHOLD AND archived
      plans >= LEVEL_2_DEEPEN_PLANS_THRESHOLD.
    """
    out: set[str] = set()

    level_0_to_1 = (target / "dev" / "proposals" / "_template.md").is_file()
    if level_0_to_1:
        out.add("level-0-to-1")

    level_1_to_2 = (target / "dev" / "cairn-lock.yml").is_file()
    if level_1_to_2:
        out.add("level-1-to-2")

    archived_proposals = _count_archived_proposals(target)
    archived_plans = _count_archived_plans(target)
    if (
        not level_1_to_2
        and archived_proposals >= LEVEL_1_DEEPEN_PROPOSALS_THRESHOLD
        and archived_plans >= LEVEL_1_DEEPEN_PLANS_THRESHOLD
    ):
        out.add("level-1-deepen")
    if (
        level_1_to_2
        and archived_proposals >= LEVEL_2_DEEPEN_PROPOSALS_THRESHOLD
        and archived_plans >= LEVEL_2_DEEPEN_PLANS_THRESHOLD
    ):
        out.add("level-2-deepen")

    return out


# Known AI-agent vendor / model substrings used by the cross-type-
# review detector + the second-agent-type roster scan.  Conservative:
# the patterns are case-insensitive substring matches, common enough
# to detect real attributions while infrequent enough in plain prose
# to keep false-positives bounded.
_AGENT_VENDOR_PATTERNS: tuple[str, ...] = (
    "claude", "codex", "gpt", "antigravity", "gemini", "copilot",
)

# Patterns that explicitly mark a roster line as the human Maintainer
# (so the line is not counted as an agent for second-agent-type).
_HUMAN_MAINTAINER_PATTERNS: tuple[str, ...] = (
    "(maintainer)", "(human contributor)", "(human reviewer)",
)


def _list_proposal_files(target: Path, *, archived: bool) -> list[Path]:
    sub = "archive" if archived else ""
    root = target / "dev" / "proposals" / sub if sub else target / "dev" / "proposals"
    if not root.is_dir():
        return []
    return [
        p for p in root.glob("*.md")
        if p.is_file() and p.name != "_template.md"
    ]


def _list_plan_files(target: Path, *, archived: bool) -> list[Path]:
    sub = "archive" if archived else ""
    root = target / "dev" / "plans" / sub if sub else target / "dev" / "plans"
    if not root.is_dir():
        return []
    return [
        p for p in root.glob("*.md")
        if p.is_file() and p.name != "_template.md"
    ]


def _unreleased_changelog_has_content(target: Path) -> bool:
    """``CHANGELOG.md > Unreleased`` non-empty == any non-blank line
    between the Unreleased heading and the next release heading.
    """
    changelog = target / "CHANGELOG.md"
    if not changelog.is_file():
        return False
    text = changelog.read_text(encoding="utf-8")
    lines = text.splitlines()
    # Find the Unreleased heading line.
    start_idx: int | None = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+\[?unreleased\]?", line, re.IGNORECASE):
            start_idx = i + 1
            break
    if start_idx is None:
        return False
    # Walk until the next `## ` heading (next release).
    for line in lines[start_idx:]:
        if line.startswith("## "):
            break
        if line.strip() and not line.strip().startswith("#"):
            return True
    return False


def _read_team_roster_body(target: Path) -> str | None:
    """Return the text BETWEEN ``<!-- cairn:slot team-roster -->`` +
    ``<!-- cairn:end team-roster -->`` in
    ``dev/collaboration_agreement.md``.  None if the file or slot is
    missing.
    """
    coll = target / "dev" / "collaboration_agreement.md"
    if not coll.is_file():
        return None
    text = coll.read_text(encoding="utf-8")
    open_marker = "<!-- cairn:slot team-roster -->"
    close_marker = "<!-- cairn:end team-roster -->"
    o = text.find(open_marker)
    if o < 0:
        return None
    c = text.find(close_marker, o + len(open_marker))
    if c < 0:
        return None
    return text[o + len(open_marker):c]


def _team_roster_is_unfilled(roster_body: str) -> bool:
    """The roster slot is "unfilled" when its body contains the
    template placeholder (``"the bootstrap records"`` substring) OR
    is otherwise blank.  Once the maintainer fills it, those markers
    are gone.
    """
    body = roster_body.strip()
    if not body:
        return True
    return "the bootstrap records" in body.lower()


def _count_distinct_agents_in_roster(roster_body: str) -> int:
    """Count distinct agent identifiers in the team-roster body.

    Heuristic: every Markdown list-item line ("* " or "- " start) is
    a roster entry; entries containing any
    ``_HUMAN_MAINTAINER_PATTERNS`` substring are human; entries that
    contain any ``_AGENT_VENDOR_PATTERNS`` substring are an agent.
    The count is the number of agent entries; the vendor-name acts as
    the deduplication key so the same agent listed twice doesn't
    double-count.
    """
    seen_vendors: set[str] = set()
    for line in roster_body.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("* ") or stripped.startswith("- ")):
            continue
        low = stripped.lower()
        if any(p in low for p in _HUMAN_MAINTAINER_PATTERNS):
            continue
        for pat in _AGENT_VENDOR_PATTERNS:
            if pat in low:
                seen_vendors.add(pat)
                break
    return len(seen_vendors)


def _author_vendor_in_file(text: str) -> str | None:
    """Find the file's author-vendor by scanning the header for a
    ``**Author**:`` (or ``Author:``) line + matching against the
    known vendor patterns.  Returns the matched pattern, or None if
    no author or vendor signal is found.
    """
    for line in text.splitlines()[:30]:
        if "author" not in line.lower():
            continue
        low = line.lower()
        for pat in _AGENT_VENDOR_PATTERNS:
            if pat in low:
                return pat
    return None


def _has_cross_type_review_in_file(text: str) -> bool:
    """Scan a proposal/plan file's ``## Review`` sections for an
    attribution naming a vendor different from the file's author
    vendor.  Returns True if at least one cross-type review is found.
    """
    author = _author_vendor_in_file(text)
    if author is None:
        return False
    lines = text.splitlines()
    # Find each "## Review" heading.
    for i, line in enumerate(lines):
        m = re.match(r"^##\s+Review\b", line, re.IGNORECASE)
        if m is None:
            continue
        # Scan the heading line itself (which often carries the
        # reviewer attribution like "## Review -- Codex (External)")
        # PLUS up to 10 lines into the body for a vendor pattern
        # different from `author`.
        for body_line in lines[i:i + 11]:
            low = body_line.lower()
            for pat in _AGENT_VENDOR_PATTERNS:
                if pat in low and pat != author:
                    return True
    return False


def _has_cross_type_review_anywhere(target: Path) -> bool:
    """File-content scan: any proposal or plan with a cross-type
    Review section fires the trigger.
    """
    files = (
        _list_proposal_files(target, archived=False)
        + _list_proposal_files(target, archived=True)
        + _list_plan_files(target, archived=False)
        + _list_plan_files(target, archived=True)
    )
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        if _has_cross_type_review_in_file(text):
            return True
    return False


def _foldback_has_open_candidate(target: Path) -> bool:
    """The fold-back ledger has at least one row whose status is
    ``candidate``.  Returns True if the canonical ledger
    (``dev/upstream/fold-back-ledger.md``) carries one.
    """
    ledger = target / "dev" / "upstream" / "fold-back-ledger.md"
    if not ledger.is_file():
        return False
    text = ledger.read_text(encoding="utf-8")
    # Match a markdown table row whose status column is `candidate`
    # (the ledger doctrine fixes the column names; the canonical
    # status set is `candidate` / `queued` / `filed` / `pr` / `scoped`
    # / `synced` / `dropped`).
    return bool(re.search(r"\|\s*candidate\s*\|", text, re.IGNORECASE))


def evaluate_action_triggers(
    target: Path,
    log_records: list["ActivationRecord"] | None = None,
) -> set[str]:
    """Action-trigger evaluators (Chunk P1.9b).

    Per Codex External Review P2-3 disposition: triggers observe
    explicit state (filesystem + roster + ledger + file content
    parsing); the ``collab-agreement-signing`` trigger consults the
    activation log to confirm the ``first-proposal-archived``
    precondition has fired.

    Triggers fired:

    * ``first-proposal-opened`` -- any non-template .md in
      ``dev/proposals/``.
    * ``first-proposal-archived`` -- any .md in
      ``dev/proposals/archive/``.
    * ``first-plan-opened`` / ``first-plan-archived`` -- parallel
      for plans.
    * ``first-changelog-entry`` -- ``CHANGELOG.md > Unreleased`` has
      content.
    * ``second-agent-type`` -- team-roster slot lists 2+ distinct
      agent identifiers.
    * ``first-cross-type-review`` -- file-content scan finds a
      proposal/plan with a Review section attributed to a vendor
      different from the file's author.
    * ``first-foldback-candidate`` -- fold-back ledger has a
      ``candidate``-status row.
    * ``collab-agreement-signing`` -- roster slot is unfilled AND
      ``first-proposal-archived`` has fired (recorded in the
      activation log).
    """
    out: set[str] = set()

    if _list_proposal_files(target, archived=False):
        out.add("first-proposal-opened")
    if _list_proposal_files(target, archived=True):
        out.add("first-proposal-archived")
    if _list_plan_files(target, archived=False):
        out.add("first-plan-opened")
    if _list_plan_files(target, archived=True):
        out.add("first-plan-archived")

    if _unreleased_changelog_has_content(target):
        out.add("first-changelog-entry")

    roster_body = _read_team_roster_body(target)
    roster_unfilled = roster_body is None or _team_roster_is_unfilled(
        roster_body
    )
    if roster_body and not roster_unfilled:
        if _count_distinct_agents_in_roster(roster_body) >= 2:
            out.add("second-agent-type")

    if _has_cross_type_review_anywhere(target):
        out.add("first-cross-type-review")
    if _foldback_has_open_candidate(target):
        out.add("first-foldback-candidate")

    # collab-agreement-signing: roster unfilled AND
    # first-proposal-archived has previously fired (in the log).
    if log_records is not None and roster_unfilled:
        prior_fired_triggers = {r.trigger for r in log_records}
        # The trigger ALSO requires first-proposal-archived to have
        # fired CURRENTLY (covering the case where the log doesn't
        # yet have it but the state does).
        first_archived_now = "first-proposal-archived" in out
        if "first-proposal-archived" in prior_fired_triggers or first_archived_now:
            out.add("collab-agreement-signing")

    return out


def evaluate_triggers(
    target: Path,
    log_records: list["ActivationRecord"] | None = None,
) -> set[str]:
    """Union of maturity-ladder + action trigger evaluators.

    The two-family split lets tests fixture each family independently
    and keeps the plan's P1.9a / P1.9b sub-chunking visible at the
    code surface.  ``log_records`` is forwarded to the action-trigger
    family for the ``collab-agreement-signing`` precondition check.
    """
    return (
        evaluate_maturity_triggers(target)
        | evaluate_action_triggers(target, log_records=log_records)
    )


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
    log_path: Path, records: list[ActivationRecord],
) -> None:
    """Atomic-append each record's JSONL line to the log.  Matches
    the ``dev/intents.jsonl`` precedent: open the file in append
    mode with line-buffering so concurrent appends don't collide.
    """
    if not records:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8", buffering=1) as fh:
        for rec in records:
            fh.write(rec.to_jsonl() + "\n")


# ---------------------------------------------------------------------------
# Top-level activate() flow
# ---------------------------------------------------------------------------


def default_agent_identity() -> str:
    """Best-effort identifier for the agent / runner appending the
    activation log line.  Reads ``CAIRN_AGENT_ID`` env var when set;
    otherwise returns ``unknown-agent``.
    """
    return os.environ.get("CAIRN_AGENT_ID", "unknown-agent")


def utc_now_iso() -> str:
    """ISO-8601 UTC timestamp with second precision.  Matches the
    `activated-at` schema field."""
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True)
class ActivationOutcome:
    """Result of one ``activate(...)`` run."""

    preset: str | None
    pending: list[PendingActivation]
    planning_updated: bool
    log_records: list[ActivationRecord]


class OnboardingError(Exception):
    """Raised on a recoverable error the maintainer should fix
    (missing slot, missing metadata, missing source file, etc.).
    The CLI catches + prints a friendly message + exits non-zero."""


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
    planning_text = planning_path.read_text(encoding="utf-8")

    found = find_slot_body(planning_text)
    if found is None:
        raise OnboardingError(
            f"`cairn:slot {SLOT_NAME}` not found in {planning_path}; "
            f"is your PLANNING.md from a Cairn scaffold of >= the "
            f"plan-2026-05-28 progressive-onboarding update?"
        )

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
    source_text = source_path.read_text(encoding="utf-8")

    deferred = parse_deferred_tasks(source_text)
    log_path = target / DEFAULT_LOG_REL
    existing_records = read_activation_log(log_path)
    already = activated_task_ids(existing_records)

    if fired_triggers_override is None:
        fired = evaluate_triggers(target, log_records=existing_records)
    else:
        fired = fired_triggers_override

    pending = compute_activations(deferred, fired, already)
    if not pending:
        return ActivationOutcome(
            preset=preset,
            pending=[],
            planning_updated=False,
            log_records=[],
        )

    agent_id = by_agent or default_agent_identity()
    ts = utc_now_iso()
    new_records = [
        ActivationRecord(
            task_id=p.task.task_id,
            activated_at=ts,
            by_agent=agent_id,
            source_preset=preset,
            trigger=p.trigger,
        )
        for p in pending
    ]

    if dry_run:
        return ActivationOutcome(
            preset=preset,
            pending=pending,
            planning_updated=False,
            log_records=new_records,
        )

    # Persist: PLANNING slot first, then append log.  Slot update is
    # idempotent under re-read (the log is the dedup key on the next
    # run); log-only ordering would risk re-activating on PLANNING
    # write failure, but a log entry without a PLANNING entry is
    # recoverable (operator re-runs activate; pending is empty
    # because the log already records the id).
    _, _, current_body = found
    new_body = render_appended_slot_body(current_body, pending)
    new_planning = update_planning_slot(planning_text, new_body)
    if new_planning is None:
        raise OnboardingError(
            f"PLANNING.md slot disappeared between read + write -- "
            f"concurrent edit?  Re-run after coordinating."
        )
    planning_path.write_text(new_planning, encoding="utf-8")
    append_activation_log(log_path, new_records)

    return ActivationOutcome(
        preset=preset,
        pending=pending,
        planning_updated=True,
        log_records=new_records,
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
# CLI
# ---------------------------------------------------------------------------


def _format_outcome_summary(outcome: ActivationOutcome) -> str:
    if not outcome.pending:
        return (
            f"onboarding_activate: no eligible activations (preset="
            f"{outcome.preset!r}; trigger evaluation P1.9 not yet "
            f"shipped, so the stub returns no fired triggers)."
        )
    lines = [
        f"onboarding_activate: {len(outcome.pending)} activation(s) "
        f"(preset={outcome.preset!r}):"
    ]
    for p in outcome.pending:
        lines.append(
            f"  * id={p.task.task_id}  trigger={p.trigger}"
        )
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

    if args.seed:
        print(
            "error: --seed mode lands in plan Chunk P1.11; in P1.2 "
            "only default mode + --dry-run are implemented.",
            file=sys.stderr,
        )
        return 2

    target = Path(args.target).resolve()
    try:
        outcome = activate(target, dry_run=args.dry_run)
    except OnboardingError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(_format_outcome_summary(outcome))
    return 0


if __name__ == "__main__":
    sys.exit(main())
