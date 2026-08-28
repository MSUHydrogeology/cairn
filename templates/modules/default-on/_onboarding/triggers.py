#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""onboarding-activate engine -- trigger evaluation.

The maturity- and action-trigger evaluation engine: the deepen
thresholds, the agent-vendor / human-maintainer authorship patterns, the
proposal/plan counters + listers, the team-roster / cross-type-review / foldback
probes, and the top-level ``evaluate_maturity_triggers`` /
``evaluate_action_triggers`` / ``evaluate_triggers``. Depends on the containment
leaf (``security``) for the read + glob guards used when scanning the adopter's
deliberation tree.
"""
from __future__ import annotations

import re

from .security import _assert_safe_dir_for_glob, _assert_safe_read


# Per plan 2026-05-28-claude-cairn-progressive-onboarding (Codex
# External Review P2-3): triggers evaluate against EXPLICIT
# deployment state (filesystem + roster + ledger) wherever possible,
# NOT git archaeology.  The collab-agreement-signing trigger evaluator
# uses a "first-proposal-archived has fired" precondition recorded in
# the activation log -- the log IS the explicit state for prior
# trigger fires.
#
# The trigger matrix lives in two families:
# * Maturity-ladder triggers (this section): level-0-to-1,
#   level-1-to-2, level-1-deepen, level-2-deepen.
# * Action triggers (next section): first-proposal-opened,
#   first-proposal-archived, first-plan-opened, first-plan-archived,
#   first-changelog-entry, second-agent-type, first-cross-type-review,
#   collab-agreement-signing.


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
    _assert_safe_dir_for_glob(archive, target)
    return sum(
        1 for p in archive.glob("*.md")
        if p.is_file() and not p.is_symlink() and p.name != "_template.md"
    )


def _count_archived_plans(target: Path) -> int:
    archive = target / "dev" / "plans" / "archive"
    if not archive.is_dir():
        return 0
    _assert_safe_dir_for_glob(archive, target)
    return sum(
        1 for p in archive.glob("*.md")
        if p.is_file() and not p.is_symlink() and p.name != "_template.md"
    )


def evaluate_maturity_triggers(target: Path) -> set[str]:
    """Maturity-ladder trigger evaluators.

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
    * ``level-1-to-2`` -- ``dev/.cairn/cairn-lock.yml`` present (canonical
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

    level_1_to_2 = (target / "dev" / ".cairn" / "cairn-lock.yml").is_file()
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
# Confirmed against a real deployment:
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
    # Parent-once containment validation (Antigravity plan-review
    # P2-2): one full three-check on the glob parent; per-leaf
    # ``is_symlink()`` filters out symlinked leaves cheaply.  Equivalent
    # to per-leaf ``_assert_safe_read`` at lower cost.
    _assert_safe_dir_for_glob(root, target)
    return [
        p for p in root.glob("*.md")
        if p.is_file() and not p.is_symlink() and p.name != "_template.md"
    ]


def _list_plan_files(target: Path, *, archived: bool) -> list[Path]:
    sub = "archive" if archived else ""
    root = target / "dev" / "plans" / sub if sub else target / "dev" / "plans"
    if not root.is_dir():
        return []
    _assert_safe_dir_for_glob(root, target)
    return [
        p for p in root.glob("*.md")
        if p.is_file() and not p.is_symlink() and p.name != "_template.md"
    ]


def _unreleased_changelog_has_content(target: Path) -> bool:
    """``CHANGELOG.md > Unreleased`` non-empty == any non-blank line
    between the Unreleased heading and the next release heading.
    """
    changelog = target / "CHANGELOG.md"
    if not changelog.is_file():
        return False
    _assert_safe_read(changelog, target)
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
    # Skip HTML comment lines
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
    _assert_safe_read(coll, target)
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

    Per Antigravity plan-review P2-2 disposition: the glob roots are
    already containment-validated inside ``_list_proposal_files`` +
    ``_list_plan_files`` (one-shot ``_assert_safe_dir_for_glob`` per
    root), and the lister filters symlinked leaves with
    ``not p.is_symlink()``.  The combination is security-equivalent
    to per-leaf ``_assert_safe_read`` at much lower cost on large
    archives.
    """
    files = (
        _list_proposal_files(target, archived=False)
        + _list_proposal_files(target, archived=True)
        + _list_plan_files(target, archived=False)
        + _list_plan_files(target, archived=True)
    )
    for f in files:
        # Defense in depth: even though the lister already filters
        # symlinked leaves, a TOCTOU race could swap a regular file
        # for a symlink between glob and read.  Re-check at the
        # read site for fail-closed semantics.
        if f.is_symlink():
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        if _has_cross_type_review_in_file(text):
            return True
    return False


def evaluate_action_triggers(
    target: Path,
    log_records: list["ActivationRecord"] | None = None,
) -> set[str]:
    """Action-trigger evaluators.

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
    and keeps the maturity / action split visible at the
    code surface.  ``log_records`` is forwarded to the action-trigger
    family for the ``collab-agreement-signing`` precondition check.
    """
    return (
        evaluate_maturity_triggers(target)
        | evaluate_action_triggers(target, log_records=log_records)
    )
