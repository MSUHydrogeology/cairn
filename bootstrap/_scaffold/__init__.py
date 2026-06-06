#!/usr/bin/env python3
"""Cairn bootstrap scaffold engine — the private ``bootstrap/_scaffold`` package.

This is the install/upgrade engine that ``bootstrap/scaffold.py`` (the thin,
fail-closed launcher + facade) loads under the single canonical identity
``bootstrap._scaffold``. It is **not** a public import surface: adopters and
tooling reach it only through ``bootstrap/scaffold.py`` (``python
bootstrap/scaffold.py --help`` for the CLI; that command's help text is the
docstring of the ``cli`` submodule, which owns ``main`` / ``build_arg_parser``).

Topology (scaffold-split, 2026-06): the former single-file monolith is split into
eight owned modules in an acyclic, downward dependency DAG, plus the verifying
loader:

* ``_guard``      — the engine import boundary (``EngineFinder`` + path checks),
                    installed by this ``__init__`` as its first action so every
                    ``bootstrap._scaffold.*`` import is mediated and fail-closed.
* ``security``    — the containment leaf (``ScaffoldSecurityError`` +
                    ``_assert_safe_write`` / ``_assert_fanout_contained``).
* ``slotmerge``   — token / slot / module-merge templating helpers.
* ``merge``       — the token- + slot-aware 3-way text merge.
* ``config``      — config / token / profile resolution; owns the
                    ``_MODULE_MAPPINGS`` trust anchor (read by ``security_check``).
* ``lockfile``    — lockfile data / read / emit / classify; owns ``read_lockfile``
                    + the lock constants (read by ``verify_integrity``).
* ``install``     — the fresh-install subsystem (templates, skills/onboarding
                    fan-out, manifest, install-time lockfile writer).
* ``upgrade``     — plan / stage / apply + lock subcommands; owns ``_cairn_root``.
* ``cli``         — ``argparse`` + ``main`` (the top layer).

This module is a thin prologue + verifying loader + **pure re-export facade**: it
defines no functions or classes of its own; it installs ``_guard`` and re-exports
each submodule's public surface so ``from bootstrap.scaffold import X`` and every
historical internal reference are unchanged.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NamedTuple

# Engine import boundary (substrate Security re-review R1): install BEFORE any
# `from . import <child>` below (Stages 1-8) and before any direct
# `import bootstrap._scaffold.<m>` can resolve a child -- the engine __init__ is
# the one place that necessarily runs first for every engine submodule import,
# whether the launcher loaded us or a caller imported a child directly. It
# rejects a preloaded polluted child and installs a finder that verifies every
# future child's real source is within the Cairn root before execution.
_ENGINE_DIR = Path(__file__).resolve().parent        # <cairn>/bootstrap/_scaffold
_CAIRN_ROOT = Path(__file__).resolve().parents[2]     # <cairn>

# `_guard` is itself the one engine child resolved BEFORE the finder exists, so
# it must be verified inline first (re-review-2 finding 1): a symlinked /
# out-of-tree _guard.py would otherwise execute unverified on both the launcher
# and direct-import paths. Refuse any symlink, non-file, or escape.
_GUARD_PATH = _ENGINE_DIR / "_guard.py"
if (_GUARD_PATH.is_symlink() or not _GUARD_PATH.is_file()
        or _CAIRN_ROOT not in _GUARD_PATH.resolve().parents):
    raise RuntimeError(
        f"scaffold engine guard {_GUARD_PATH} failed path verification "
        f"(symlinked, missing, or outside the Cairn root) -- refusing (SR1)"
    )

from ._guard import install as _install_engine_guard

_install_engine_guard(_ENGINE_DIR, _CAIRN_ROOT)

# Containment leaf (Stage 1, SR5): the single ScaffoldSecurityError identity and
# the two adopter-write guards live in `security.py`. Imported here through the
# verifying finder (installed just above), so every raise/except site in this
# module and every `_assert_safe_write` / `_assert_fanout_contained` call site
# resolves to that one class / those leaf functions (single-identity, SR5).
from .security import (  # noqa: E402
    ScaffoldSecurityError,
    _assert_safe_write,
    _assert_fanout_contained,
)

# -----------------------------------------------------------------------
# Configuration / tokens / profile resolution -> _scaffold/config.py
# -----------------------------------------------------------------------
# Extracted to the config leaf (scaffold-split Stage 4); pure stdlib. Re-exported
# here so the engine's internal references and the ``bootstrap.scaffold`` facade
# are unchanged. The trust anchor ``_MODULE_MAPPINGS`` is owned here now (plan
# 0B.3); security_check.py imports it from this narrow owner. The dev-tree /
# gitignore / fan-out WRITE functions stay in the engine (they consume this data).
from .config import (  # noqa: F401  (re-exported for the facade)
    InstallSpec,
    KNOWN_TOKENS,
    PresetError,
    _AXES,
    _CORE_MAPPINGS,
    _DEFAULT_ON_MODULES,
    _GITIGNORE_SEEDS,
    _KNOWN_VENDOR_WRAPPERS,
    _MODULE_MAPPINGS,
    _OPTIONAL_TEMPLATES,
    _PRESETS,
    _REFERENCE_SCRIPT_TOKEN,
    _SKILLS_GITIGNORE,
    _SKILLS_MAPPINGS,
    _TEAM_STAFFING_GATED,
    _TEAM_STAFFING_GATES,
    _as_str_list,
    _can_staff_module,
    _canonical_order,
    _minimal_yaml_parse,
    _yaml,
    _yaml_load,
    expand_preset,
    format_profile_summary,
    load_config,
    reference_script_token_defaults,
    resolve_axes,
    select_optional_templates,
)


# ---------------------------------------------------------------------------
# Token / slot / module-merge templating helpers -> _scaffold/slotmerge.py
# ---------------------------------------------------------------------------
# Extracted to the slotmerge leaf (scaffold-split Stage 2). Re-exported here so
# the engine's internal references and the ``bootstrap.scaffold`` facade are
# unchanged. ``run_module_merge_pass`` stays in the engine below (install-time
# orchestrator coupling to ``_MODULE_MAPPINGS`` / ``InstallSpec``; it joins
# install.py at Stage 6).
from .slotmerge import (  # noqa: F401  (re-exported for the facade)
    _CUSTOMIZED_MARKER_RE,
    _DOC_AUTHOR_TOKENS,
    _MERGE_CONTENT_END_RE,
    _MERGE_CONTENT_START_RE,
    _MERGE_TARGET_RE,
    _SLOT_END_RE,
    _SLOT_RE,
    _TOKEN_RE,
    DuplicateSlotError,
    ModuleMergeError,
    ModuleMergeResult,
    _normalize_for_compare,
    _slot_body_in_text,
    _slot_is_customized,
    _slot_is_empty,
    _write_slot_body,
    check_slot_fidelity,
    find_block_slots,
    find_unfilled_tokens,
    find_unpaired_slots,
    merge_module_into_slot,
    parse_module_merge_directives,
    substitute_tokens,
    validate_unique_slot_names,
)
# -----------------------------------------------------------------------
# Fresh-install subsystem -> _scaffold/install.py
# -----------------------------------------------------------------------
# Extracted to the install module (scaffold-split Stage 6); layer-6 subsystem
# depending downward on config/security/slotmerge/lockfile. Re-exported here so
# the engine's internal references (upgrade/cli call sites) and the
# ``bootstrap.scaffold`` facade are unchanged. The shared _cairn_root/
# _find_cairn_root helpers and the upgrade-time _MANIFEST_SEARCH_DIRS stay below.
from .install import (  # noqa: F401  (re-exported for the facade)
    InstallResult,
    _DEV_DIRS,
    _FORGE_REFERENCE_DIRS,
    _ONBOARDING_DOC_DST_DIR_REL,
    _ONBOARDING_DOC_NAMES,
    _ONBOARDING_HELPER_DST_REL,
    _ONBOARDING_HELPER_SRC_REL,
    _ONBOARDING_LOG_HEADER,
    _ONBOARDING_LOG_REL,
    _ONBOARDING_PRESETS,
    _ONBOARDING_SEED_RE,
    _emit_skill_copy_fallback,
    _emit_skill_symlink,
    _extract_seed_tasks,
    _install_one,
    _lock_file_list,
    _render_onboarding_slot,
    _substitute_slot,
    _symlinks_available,
    create_dev_tree,
    fan_out_skills,
    format_manifest,
    git_provenance_warning,
    install_core,
    install_issue_capture_reference,
    install_manifest,
    install_modules,
    install_onboarding,
    install_optional,
    install_skills,
    load_vendor_targets,
    print_report,
    render_compatibility_matrix,
    run_module_merge_pass,
    seed_gitignore,
    write_install_lockfile,
    write_local_env,
)
# -----------------------------------------------------------------------
# Upgrade subsystem -> _scaffold/upgrade.py
# -----------------------------------------------------------------------
# Extracted to the upgrade module (scaffold-split Stage 7); layer-7, depends
# downward on config/security/merge/slotmerge/lockfile/install. Re-exported here
# so the engine's internal references (the cli's main/dispatch) and the
# ``bootstrap.scaffold`` facade are unchanged. The canonical root resolver
# _cairn_root / _find_cairn_root is owned here now (cli reads it from upgrade).
from .upgrade import (  # noqa: F401  (re-exported for the facade)
    FilePlan,
    _ADVANCING_KINDS,
    _AXIS_PLACEHOLDERS,
    _CONFLICT_MARKER,
    _INIT_LOCK_TOKEN_PLACEHOLDERS,
    _KIND_DISPLAY_LABEL,
    _MANIFEST_SEARCH_DIRS,
    _STAGE_META,
    _STAGING_REL,
    _apply_upgrade,
    _cairn_is_git,
    _cairn_root,
    _citation_ok,
    _cmd_adopt_module,
    _cmd_finalize_lockfile,
    _cmd_init_lock,
    _compute_upgrade,
    _dirty_tracked_paths,
    _find_cairn_root,
    _find_manifest_path,
    _infer_init_lock_axes,
    _manifest_cairn_commit,
    _print_upgrade_report,
    _resolve_lock_profile_fields,
    _resolve_vendor_wrapper,
    _seed_staging_gitignore,
    _self_heal_profile_config,
    _theirs_bytes,
    _theirs_text,
    _warn_legacy_manifest_home,
    _write_init_lock_profile_template,
    _write_stage,
    _writeset_dirty_collisions,
    _yaml_sq,
    cmd_upgrade,
)


# ---------------------------------------------------------------------------
# Upgrade capability -- install lockfile + scoped base-template cache
# ---------------------------------------------------------------------------
#
# The install-side ancestor anchor for ``scaffold.py upgrade`` (the
# token- + slot-aware 3-way merge).  See ``bootstrap/UPGRADE.md`` and the
# the source ``cairn-module-upgrade-3way-merge`` plan.
#
#   * ``dev/.cairn/cairn-lock.yml`` -- a *tracked* machine lockfile: the upgrade
#     ancestor + the install-side provenance record.  Tool-owned (only
#     ``scaffold.py`` reads/writes it), not a human-readable document, so it
#     lives with the other Cairn machinery under ``dev/.cairn/`` rather than at
#     the ``dev/`` root.  (Reverses the original R2 "visible at dev/ root"
#     placement: a ``.cairn/`` dotfolder does not hide the file from agents, and
#     keeping it out of the ``dev/`` listing leaves that listing human-meaningful.)
#   * ``dev/.cairn/base/`` -- a *tracked* cache of the **raw** upstream
#     templates for the mergeable ``.md`` installs (R1/I4): so the merge's
#     ``base`` is on disk under any distribution mode (no Cairn git history
#     needed) and only the mergeable set is shadow-copied.

# -----------------------------------------------------------------------
# Lockfile data / read / emit / classify core -> _scaffold/lockfile.py
# -----------------------------------------------------------------------
# Extracted to the lockfile leaf (scaffold-split Stage 5); pure stdlib. Re-exported
# here so the engine's internal references and the ``bootstrap.scaffold`` facade
# are unchanged. The trust anchor (read_lockfile + lock constants + _LIVING_STATE_DSTS)
# is owned here now (plan 0B.3); verify_integrity.py imports it from this narrow
# owner. The install-time WRITER write_install_lockfile + _lock_file_list stay in
# the engine below (onboarding/manifest coupling; they join install.py at Stage 6).
from .lockfile import (  # noqa: F401  (re-exported for the facade)
    _BASE_CACHE_REL,
    _LIVING_STATE_DSTS,
    _LOCKFILE_REL,
    _LOCK_SCHEMA,
    _PROFILE_REL,
    _SECRET_TOKEN_RE,
    _behind_by_n,
    _cairn_commit,
    _cairn_version,
    _emit_lock_yaml,
    _refuse_secret_tokens,
    _sha256_hex,
    classify_verbatim,
    read_lockfile,
)


# ---------------------------------------------------------------------------
# Token- + slot-aware 3-way merge engine -> _scaffold/merge.py
# ---------------------------------------------------------------------------
# Extracted to the merge module (scaffold-split Stage 3); depends on the
# slotmerge leaf. Re-exported here so the engine's internal references (the
# upgrade machinery's merge_file / SlotError call sites) and the
# ``bootstrap.scaffold`` facade are unchanged. classify_verbatim (the verbatim
# hash policy) stays below -- it is never a text merge and couples to
# _sha256_hex (the lockfile cluster migrating at Stage 5).
from .merge import (  # noqa: F401  (re-exported for the facade)
    MergeResult,
    Slot,
    SlotError,
    _three_way_merge,
    _transplant_slots,
    merge_file,
    parse_slots,
)


# -----------------------------------------------------------------------
# CLI entry points -> _scaffold/cli.py
# -----------------------------------------------------------------------
# Extracted to the cli module (scaffold-split Stage 8); the top layer -- imports
# downward from every subsystem. Re-exported here so the launcher
# (bootstrap/scaffold.py -> _engine.main()) and the bootstrap.scaffold facade are
# unchanged. cli.py carries a copy of this module docstring so build_arg_parser's
# ``description=__doc__`` --help text is byte-preserved.
from .cli import build_arg_parser, main  # noqa: F401  (re-exported for the facade + launcher)


if __name__ == "__main__":
    sys.exit(main())
