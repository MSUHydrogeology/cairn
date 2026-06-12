#!/usr/bin/env python3
"""Work-intent engine — the private ``_intent`` package.

The work-intent tool (claim/release JSONL substrate, per-session identity, the
pre-commit conflict check, the CLI, and the git-hook installers) is loaded by the
thin launcher/facade ``intent.py`` under the canonical identity ``tools._intent``.
Adopters and the git hooks reach it only through ``intent.py``.

Topology (intent-split, 2026-06): the former single-file monolith is split into
five owned subsystems in an acyclic, downward dependency DAG:

* ``shared``    — repo-root anchor + cross-subsystem path helpers (the leaf).
* ``record_io`` — claim-ledger record schema + best-effort atomic JSONL append +
                  read-side helpers (active intents, conflict check, iteration).
* ``identity``  — per-session agent-identity / session-token resolution.
* ``conflict``  — claim-TTL / stale-claim policy + the staged-path-vs-other-claim
                  decision + incident recording + warn/confirm/block enforcement.
                  Also owns the pre-commit sentinels + git helpers, co-located at
                  their earliest consumer to keep the package acyclic.
* ``hooks``     — post-commit / pre-commit hook install (writes ``.git/hooks/``).
* ``cli``       — ``argparse`` + ``main`` (the top layer; imports downward).

This module is a **pure re-export facade**: it defines no functions or classes of
its own; it re-exports each subsystem's surface so ``from tools.intent import X``
and every historical internal reference resolve unchanged through the launcher.
"""
from __future__ import annotations

from .shared import (  # noqa: F401  (re-exported for the facade)
    INTENTS_LOG_PATH,
    _REPO_ROOT,
    _read_nul_delimited_paths,
    normalize_path,
)
from .record_io import (  # noqa: F401  (re-exported for the facade)
    ClaimRecord,
    RECORD_SIZE_CAP,
    ReleaseRecord,
    _record_bytes,
    active_intents,
    append_record,
    conflict_check,
    generate_id,
    iter_log,
    read_log,
    write_claim,
    write_release,
)
from .identity import (  # noqa: F401  (re-exported for the facade)
    AGENT_ENV_VAR,
    DEFAULT_CONFIG_PATH,
    HARNESS_SESSION_VARS,
    _load_config,
    _session_digest,
    _session_identity,
    effective_harness_vars,
    resolve_agent_identity,
    resolve_session_token,
)
from .conflict import (  # noqa: F401  (re-exported for the facade)
    ALLOW_UNCLAIMED_ENV_VAR,
    DEFAULT_CLAIM_TTL_HOURS,
    ENFORCE_MODES,
    INCIDENT_EVENT_CLASS_DEFAULT,
    INCIDENT_LOG_RELPATH_DEFAULT,
    INTENT_CONFIG_RELPATH,
    INTENT_CONFIG_RELPATH_CANONICAL,
    INVOKE_HINT,
    PRECOMMIT_SENTINEL_BEGIN,
    PRECOMMIT_SENTINEL_END,
    _claim_is_stale,
    _classify_existing_precommit,
    _compute_overlaps,
    _confirm_proceed,
    _confirm_tty,
    _describe_collision,
    _drop_stale_claims,
    _format_conflict_warning,
    _git_path,
    _git_toplevel,
    _incident_tracker_skeleton,
    _insert_incident_row,
    _other_session_warning,
    _precommit_check_impl,
    _precommit_hook_block,
    _precommit_shebang_is_shell,
    _read_claim_ttl_hours,
    _read_enforce_mode,
    _read_incident_config,
    _read_solo_mode,
    _record_incident,
    _rename_map_via_git,
    _staged_paths_via_git,
    _strip_precommit_block,
    _unclaimed_warning,
    _unknown_identity_warning,
    classify_precommit_warnings,
    other_session_overlaps,
    split_file_tokens,
)
from .hooks import (  # noqa: F401  (re-exported for the facade)
    PYTHON_ENV_VAR,
    SENTINEL_BEGIN,
    SENTINEL_END,
    _FRAMEWORK_MARKERS,
    _build_hook_block,
    _cmd_install_hook,
    _cmd_install_precommit,
    _detect_framework,
    _first_shebang_is_shell,
    _hook_installed,
    _intent_tool_path,
    _replace_block,
    _resolve_hook_interpreter,
    _resolve_hooks_dir,
    _uninstall_hook,
)
from .cli import (  # noqa: F401  (re-exported for the facade)
    _build_parser,
    _cmd_auto_release,
    _cmd_claim,
    _cmd_hooks_status,
    _cmd_list,
    _cmd_precommit_check,
    _cmd_release,
    _cmd_whoami,
    main,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
