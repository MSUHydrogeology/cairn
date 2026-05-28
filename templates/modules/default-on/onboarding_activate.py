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
#: dev/intents.jsonl.  The scaffold SEEDS the file empty at install
#: time (the canonical path); the helper also carries a lazy-mkdir
#: backstop on ``append_activation_log`` for callers that bypass the
#: scaffold (existing-adopter --seed paths run against a
#: scaffold-less tree, etc.).  Per Claude External code review P3-1:
#: scaffold-seeds is the primary contract; lazy-mkdir is the
#: backstop, not the primary mechanism.
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

    * ``level-0-to-1`` -- the adopter has shipped at least one
      proposal through archive (>= 1 file in ``dev/proposals/
      archive/``).  Per Claude External code review P2-3 +
      Antigravity confirmation: the earlier "_template.md present"
      check fired at install time for every adopter and carried no
      signal value; the real transition is "the adopter has begun
      using the lifecycle," for which the archived-proposal count
      is a stronger explicit-state signal.
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

    archived_proposals_pre = _count_archived_proposals(target)
    if archived_proposals_pre >= 1:
        out.add("level-0-to-1")

    level_1_to_2 = (target / "dev" / "cairn-lock.yml").is_file()
    if level_1_to_2:
        out.add("level-1-to-2")

    archived_proposals = archived_proposals_pre
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


# Known AI-agent vendor / model / tool substrings used by the
# cross-type-review detector + the second-agent-type roster scan.
# Conservative: the patterns are case-insensitive substring matches,
# common enough to detect real attributions while infrequent enough
# in plain prose to keep false-positives bounded.  Per Claude
# External-functioning code review P2 + Antigravity confirmation:
# the foldback active-surfacing proposal's I-8 disposition already
# converged on a broader enumeration; this list reflects that
# convergence + a documented update doctrine (the goodnight harvest
# checks for new vendor names entering the literature; adopters who
# encounter false-negatives can add patterns via a v1.x
# capability-pull-from-adopter follow-up).
_AGENT_VENDOR_PATTERNS: tuple[str, ...] = (
    # vendors / labs
    "claude", "anthropic",
    "codex", "gpt", "openai",
    "antigravity", "gemini", "google", "deepmind",
    "copilot", "microsoft",
    "mistral",
    "llama", "meta",
    "deepseek",
    # agent-tooling brands
    "cline", "aider", "continue", "devin",
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
    # Walk until the next `## ` heading (next release).  Per
    # Antigravity External code review P2: skip HTML comment lines
    # (`<!-- ... -->`) since template scaffolds often carry header
    # comments under `## Unreleased` that should NOT trigger.
    for line in lines[start_idx:]:
        if line.startswith("## "):
            break
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("<!--"):
            continue
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
    # Find each review-shape heading.  Per Antigravity External code
    # review P1-A: extend match from `## Review\b` (which missed
    # `## Plan review` and `## Code review` shapes) to also accept
    # `Plan ` / `Code ` qualifiers in the canonical convention.
    for i, line in enumerate(lines):
        m = re.match(
            r"^##\s+(?:Plan\s+|Code\s+)?Review\b", line, re.IGNORECASE,
        )
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
# Active-surfacing prompts (Chunks P1.10a mechanisms + P1.10b content)
# ---------------------------------------------------------------------------
#
# The four named active-surfacing rows, in priority order (the
# activation helper emits at most one per goodnight, picking the
# highest-priority unmuted row).

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
    """
    if not records:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
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
        planning_path.write_text(new_planning, encoding="utf-8")
        planning_updated = True
    append_activation_log(log_path, new_records)

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


VALID_PRESETS = ("solo-greenfield", "collaborative-team", "high-rigor-legacy")


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
        except OnboardingError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(summary)
        return 0

    try:
        outcome = activate(target, dry_run=args.dry_run)
    except OnboardingError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(_format_outcome_summary(outcome))
    return 0


if __name__ == "__main__":
    sys.exit(main())
