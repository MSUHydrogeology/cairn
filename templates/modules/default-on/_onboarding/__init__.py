#!/usr/bin/env python3
"""onboarding_activate.py -- progressive-onboarding activation engine package.

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

Package layout (onboarding-split phase B2): this engine was a single file
(``scripts/onboarding_activate.py``); it is now a private ``_onboarding/``
package loaded by the thin launcher/facade ``onboarding_activate.py``. The
subsystems form an acyclic, leaf-first DAG:

* ``security``   -- containment guards + the ``OnboardingError`` taxonomy (leaf).
* ``shared``     -- default paths + identity / timestamp helpers (leaf).
* ``prompts``    -- active-surfacing rendering + UX caps (leaf).
* ``slotparse``  -- slot + preset parsing (depends on ``security``).
* ``triggers``   -- maturity / action trigger evaluation (depends on ``security``).
* ``activation`` -- records, log I/O + computation (depends on ``security`` + ``slotparse``).
* ``cli``        -- activate / seed / ``main`` (the top layer; imports downward).

This module is a **pure re-export facade**: it defines no functions or classes
of its own; it re-exports each subsystem's public AND test-accessed symbols so
``from scripts.onboarding_activate import X``, ``helper.X`` attribute access in
the test-suite, and every historical internal reference resolve unchanged
through the launcher.
"""
from __future__ import annotations

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
from .activation import (  # noqa: F401  (re-exported for the facade)
    ActivationOutcome,
    ActivationRecord,
    PendingActivation,
    activated_task_ids,
    append_activation_log,
    compute_activations,
    read_activation_log,
    render_appended_slot_body,
    update_planning_slot,
)
from .cli import (  # noqa: F401  (re-exported for the facade)
    _format_outcome_summary,
    _interactive_preset_prompt,
    _render_onboarding_slot_seed,
    _substitute_slot_body,
    activate,
    derive_completed_task_ids,
    derive_held_task_ids,
    main,
    seed_existing_adopter,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
