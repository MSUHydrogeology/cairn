#!/usr/bin/env python3
"""
scaffold.py — Cairn bootstrap mechanical scaffold.

Creates the ``dev/`` directory tree in a target repository, copies
the core Cairn templates and the selected module files, and
substitutes inline ``{{placeholder}}`` tokens.  Block slots
(``<!-- cairn:slot ... -->`` regions) are left in place for a
reasoning agent and the Maintainer to fill.

Usage
-----
::

    python bootstrap/scaffold.py --config profile.yml --target /path/to/repo

Config YAML format
------------------
::

    # Inline token values (mechanical substitution)
    project_name: "MyProject"
    test_command: "pytest"

    # Issue forge (optional). When set and the issue-capture module is
    # installed, the scaffold copies that forge's issue-template +
    # labels.yml starter into the adopter root (non-clobber). Omit, or
    # use an unknown value, to keep the reference a manual-copy starter.
    forge: gitlab        # gitlab | github

    # Module selection
    modules:
      # Default-on (remove only with a documented reason):
      - lifecycle-metrics
      - reflections
      - claim-check
      # Team-gated (add as the dimensional profile warrants):
      # - dual-review
      # - domain-agents
      # - legacy-agent
      # - dual-language-tests
      # - coordination-tiers

The ``--cairn-root`` flag overrides the auto-detected Cairn repo
root (defaults to the directory two levels above this script's
location: ``bootstrap/scaffold.py`` → ``bootstrap/`` → ``cairn/``).

The ``--dry-run`` flag prints the plan without writing any files.
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


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="scaffold.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--config",
        required=False,
        metavar="PROFILE_YAML",
        help="Path to the profile YAML config (see Appendix B in BOOTSTRAP.md). "
             "Required for an install; not needed with --manifest.",
    )
    p.add_argument(
        "--target",
        required=False,
        metavar="REPO_ROOT",
        help="Path to the target repository root. Required for an install; "
             "not needed with --manifest.",
    )
    p.add_argument(
        "--cairn-root",
        default=None,
        metavar="CAIRN_ROOT",
        help=(
            "Path to the Cairn repo root.  Auto-detected from this script's "
            "location if omitted."
        ),
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without writing any files.",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help=(
            "Overwrite existing files in the target.  Default (no --force) "
            "skips files that already exist and prints a skip warning, so "
            "re-running the scaffold preserves any filled block slots and "
            "other customizations the existing files carry."
        ),
    )
    p.add_argument(
        "--non-interactive",
        action="store_true",
        help=(
            "Force the module-merge pass into non-interactive mode "
            "(any merge conflict defers to a `<target>.cairn-merge-pending` "
            "side-file).  Auto-detected from `sys.stdin.isatty()` when not "
            "explicitly set."
        ),
    )
    p.add_argument(
        "--manifest",
        action="store_true",
        help=(
            "Emit the install manifest (the destination<TAB>source<TAB>kind "
            "set the scaffold would install, all modules) and exit.  The "
            "Layer-1 published manifest; needs no --config / --target."
        ),
    )
    p.add_argument(
        "--summary",
        action="store_true",
        help=(
            "Print the resolved Act I-6 dimension profile (preset + resolved "
            "six-axis point + module roster + add/remove overrides + "
            "staffability warnings) and exit WITHOUT installing.  The "
            "pre-install acceptance artifact (P4); needs --config, not "
            "--target."
        ),
    )
    p.add_argument(
        "--allow-dev",
        action="store_true",
        help=(
            "Silence the Layer-1 provenance warning when scaffolding from a "
            "non-tagged / dirty Cairn source (i.e. when developing Cairn "
            "itself)."
        ),
    )
    return p


def main(argv: list[str] | None = None) -> int:
    """Entry point.  Returns an exit code (0 = success, 1 = error)."""
    raw = sys.argv[1:] if argv is None else argv
    # `scaffold.py upgrade ...` routes to the adopter upgrade path, which has
    # its own argument parser (isolated from the install CLI).
    if raw and raw[0] == "upgrade":
        return cmd_upgrade(raw[1:])

    parser = build_arg_parser()
    args = parser.parse_args(argv)

    # --manifest is a read-only emit; it needs neither --config nor
    # --target (it is the published catalog of all installable files).
    if args.manifest:
        sys.stdout.write(format_manifest())
        return 0

    # --summary is the pre-install acceptance artifact (P4): resolve the
    # profile and print it WITHOUT installing.  Needs --config, not --target.
    if args.summary:
        if not args.config:
            print("error: --summary requires --config.", file=sys.stderr)
            return 1
        summary_config_path = Path(args.config).resolve()
        if not summary_config_path.exists():
            print(
                f"error: config not found: {summary_config_path}",
                file=sys.stderr,
            )
            return 1
        try:
            summary_cfg = load_config(summary_config_path)
        except Exception as exc:
            print(f"error loading config: {exc}", file=sys.stderr)
            return 1
        if "preset" in summary_cfg and "modules" in summary_cfg:
            print(
                "error: a profile may not set both `preset:` and `modules:` "
                "-- use `preset:` with `modules_add:` / `modules_remove:`, or "
                "`modules:` alone.",
                file=sys.stderr,
            )
            return 1
        try:
            if summary_cfg.get("preset"):
                sys.stdout.write(format_profile_summary(summary_cfg))
            else:
                # No preset: the modules: list (or the default-on set) is the
                # literal install -- summarize it plainly.
                mods = (
                    _as_str_list(summary_cfg.get("modules"), "modules")
                    if "modules" in summary_cfg
                    else list(_DEFAULT_ON_MODULES)
                )
                project = str(summary_cfg.get("project_name") or "<project_name>")
                out = [f"## Dimension profile -- {project}", "",
                       "Preset: (none -- literal module list)", "",
                       "Module roster (to install):"]
                out.extend(f"  - {m}" for m in mods)
                out.append("")
                out.append(
                    "Does this profile look right before I install anything?"
                )
                sys.stdout.write("\n".join(out) + "\n")
        except PresetError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        return 0

    if not args.config or not args.target:
        print(
            "error: --config and --target are required for an install "
            "(omit them only with --manifest).",
            file=sys.stderr,
        )
        return 1

    config_path = Path(args.config).resolve()
    target = Path(args.target).resolve()

    if not config_path.exists():
        print(f"error: config not found: {config_path}", file=sys.stderr)
        return 1
    if not target.exists():
        print(f"error: target directory not found: {target}", file=sys.stderr)
        return 1

    cairn_root = (
        Path(args.cairn_root).resolve()
        if args.cairn_root
        else _cairn_root()
    )
    templates_root = cairn_root / "templates"
    if not templates_root.exists():
        print(
            f"error: templates/ not found under Cairn root: {cairn_root}",
            file=sys.stderr,
        )
        return 1

    # Layer-1 provenance nudge: warn (never block) when scaffolding from a
    # non-tagged / dirty Cairn source, unless --allow-dev.
    if not args.allow_dev:
        warning = git_provenance_warning(cairn_root)
        if warning:
            print(f"  [warn] {warning}", file=sys.stderr)

    # Load config
    try:
        cfg = load_config(config_path)
    except Exception as exc:
        print(f"error loading config: {exc}", file=sys.stderr)
        return 1

    tokens: dict[str, str] = {
        k: str(v)
        for k, v in cfg.items()
        if isinstance(k, str) and k in KNOWN_TOKENS and v
    }
    # Module selection (BOOTSTRAP.md Act I-5).  Three mutually-exclusive
    # shapes, plus the P4 preset fast path:
    #   * `preset:` (P4) -> expand to a roster via the pinned ordered merge
    #     (resolve axes -> gate-derived baseline -> add/remove); `resolved_axes`
    #     is the preset point + adopter overrides.
    #   * `modules:` alone -> today's exact-list semantics (`modules: []` opts
    #     out of all non-core modules).
    #   * `modules:` + `preset:` together -> a hard error (no replace-vs-merge
    #     guessing).
    #   * neither -> the default-on set, with an opt-out hint.
    # `resolved_axes` is the feed for axis-driven selection below (optional
    # templates): the preset-resolved point when a preset is used, else the
    # raw profile.
    resolved_axes: dict[str, object]
    if "preset" in cfg and "modules" in cfg:
        print(
            "error: a profile may not set both `preset:` and `modules:` -- "
            "use `preset:` with `modules_add:` / `modules_remove:` to "
            "compose, or `modules:` alone for an exact list.",
            file=sys.stderr,
        )
        return 1
    if cfg.get("preset"):
        try:
            modules, _preset_summary = expand_preset(cfg)
        except PresetError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        resolved_axes = dict(_preset_summary["axes"])  # type: ignore[arg-type]
        print(
            f"  [info] preset `{_preset_summary['preset']}` -> modules: "
            f"{', '.join(modules) or '(none)'}.",
            file=sys.stderr,
        )
        for warn in _preset_summary["staffability_warnings"]:  # type: ignore[union-attr]
            print(f"  [warn] staffability: {warn}", file=sys.stderr)
        if _preset_summary["removed_default_on"]:  # type: ignore[index]
            print(
                "  [info] default-on opted out via modules_remove: "
                f"{', '.join(_preset_summary['removed_default_on'])}.",  # type: ignore[arg-type]
                file=sys.stderr,
            )
    elif "modules" in cfg:
        try:
            modules: list[str] = _as_str_list(cfg.get("modules"), "modules")
        except PresetError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        resolved_axes = cfg
    else:
        modules = list(_DEFAULT_ON_MODULES)
        resolved_axes = cfg
        print(
            "  [info] profile omits `modules:` and `preset:`; installing the "
            f"default-on set ({', '.join(_DEFAULT_ON_MODULES)}).  Set "
            "`modules: []` to opt out explicitly, pick a `preset:`, or list a "
            "specific selection.",
            file=sys.stderr,
        )

    # Optional top-level templates (foldback #10): selected by the
    # dimension axes — e.g. the human-team axis selects CONTRIBUTING.md
    # at small-multi / large-multi.  Fed the RESOLVED axes (preset point +
    # overrides when a `preset:` is used, else the raw profile) per the
    # seam foldback #10 left for P4.
    optional = select_optional_templates(resolved_axes)
    if optional:
        names = ", ".join(dst for _, dst in optional)
        print(
            f"  [info] dimension profile selects optional template(s): "
            f"{names}.  Record each under `optional_templates:` in the "
            "fidelity manifest (bootstrap/fidelity-check.md) so the gate "
            "is auditable.",
            file=sys.stderr,
        )

    # Default the reference-script command tokens to the exact paths the
    # scaffold installs the scripts to (I5), unless the profile already
    # supplied a value.  This makes the shipped scripts immediately
    # runnable via the documented {{claim_check_command}} /
    # {{metrics_command}} line, and keeps the doc's invocation and the
    # install destination from desyncing.
    for token, value in reference_script_token_defaults(modules).items():
        tokens.setdefault(token, value)

    if args.dry_run:
        print("[dry-run] Would install to:", target)
        print("[dry-run] Tokens:          ", tokens)
        print("[dry-run] Modules:         ", modules)
        print(
            "[dry-run] Optional:        ",
            ", ".join(dst for _, dst in optional) or "(none)",
        )
        dry_preset = str(cfg.get("preset") or "").strip()
        if dry_preset and dry_preset in _ONBOARDING_PRESETS:
            print(
                f"[dry-run] Onboarding:      "
                f"templates/onboarding/{dry_preset}.md (seeds -> "
                f"dev/PLANNING.md slot; full source -> "
                f"dev/modules/onboarding/{dry_preset}.md)"
            )
        print(
            "[dry-run] Skills:          "
            "tools/lifecycle.py + .agents/skills/{session-start,session-end}/"
            "SKILL.md (+ untracked dev/.cairn/local-env.json)"
        )
        for mod in modules:
            for entry in _GITIGNORE_SEEDS.get(mod, ()):  # C6 dry-run
                would = seed_gitignore(target, (entry,), dry_run=True)
                if would:
                    print(f"[dry-run] Would seed .gitignore: {entry}")
        return 0

    # Create directory tree
    print(f"\nScaffolding Cairn into: {target}")
    if args.force:
        print("  (--force: existing files will be overwritten)")
    dirs_created = create_dev_tree(target)

    # Install core templates
    print("Installing core templates ...")
    core_results = install_core(
        templates_root, target, tokens, force=args.force
    )

    # Install lifecycle-routine skills (unconditional, like core) + write the
    # untracked interpreter binding (resolve-don't-bake).
    print("Installing lifecycle skills ...")
    skills_results = install_skills(
        templates_root, target, tokens, force=args.force
    )
    _n_skills = sum(
        1 for _s, d, _v in _SKILLS_MAPPINGS if d.endswith("/SKILL.md")
    )
    print(
        f"  Installed {_n_skills} lifecycle skill(s) -> .agents/skills/ "
        f"(+ the tools/lifecycle.py CLI). Try `session-start` (/good-morning)."
    )
    env_result = write_local_env(target, force=args.force)
    if env_result[3] == "installed":
        print(f"  Wrote interpreter binding: {env_result[0]} (untracked)")
    # Fan the canonical skills out to in-use vendor read-paths (symlink, or a
    # gitignored generated copy where symlinks are unavailable).  A containment
    # violation here is reported as a crisp non-zero exit, not a traceback
    # (Codex P1#2); local-env.json is already gitignored by this point.
    try:
        fanout = fan_out_skills(templates_root, target, force=args.force)
    except ScaffoldSecurityError as exc:
        print(f"error: skills fan-out refused (containment): {exc}",
              file=sys.stderr)
        return 2
    for name, tier, status in fanout:
        if status not in ("noop", "skipped-vendor-absent"):
            print(f"  Skills fan-out [{tier}] {name}: {status}")

    # Install progressive-onboarding content.  Must run AFTER
    # install_core because it edits the just-installed
    # dev/PLANNING.md's `onboarding-tasks` slot.  Always installs the
    # helper script + seeds the activation log (Chunk P1.2); only
    # populates the slot + copies the preset source file when a
    # `preset:` is selected (Chunk P1.1).
    preset_name = str(cfg.get("preset") or "").strip() or None
    label = (
        f"progressive onboarding ({preset_name})"
        if preset_name
        else "progressive onboarding (helper + log only; no preset)"
    )
    print(f"Installing {label} ...")
    onboarding_results = install_onboarding(
        templates_root, target, preset_name, force=args.force
    )

    # Install module templates
    print(f"Installing modules: {', '.join(modules) or '(none)'} ...")
    module_results = install_modules(
        templates_root, target, tokens, modules, force=args.force
    )

    # Issue-capture forge reference (fold-back #38): when issue-capture
    # installs and the profile names a forge, copy that forge's reference
    # starter (.gitlab/ or .github/) into the adopter root.  Non-clobber
    # (skip-unless --force).  Absent/unknown forge -> skipped; the
    # reference then stays a manual-copy starter under the module.
    reference_results: list[InstallResult] = []
    forge = str(cfg.get("forge") or "").strip().lower() or None
    if forge and forge not in _FORGE_REFERENCE_DIRS:
        print(
            f"  [warn] unknown forge '{forge}' (known: "
            f"{', '.join(sorted(_FORGE_REFERENCE_DIRS))}); issue-capture "
            f"reference not auto-copied.",
            file=sys.stderr,
        )
        forge = None
    if forge and "issue-capture" in modules:
        print(f"Installing issue-capture {forge} reference ...")
        reference_results = install_issue_capture_reference(
            templates_root, target, forge, force=args.force
        )

    # Install dimension-selected optional templates (foldback #10).
    optional_results: list[InstallResult] = []
    if optional:
        print(
            f"Installing optional templates: "
            f"{', '.join(dst for _, dst in optional)} ..."
        )
        optional_results = install_optional(
            templates_root, target, tokens, optional, force=args.force
        )

    print_report(
        target, dirs_created,
        core_results + skills_results + onboarding_results + module_results
        + reference_results + optional_results,
    )

    # Module-merge pass (Proposal B / audit gap #3).  Each installed
    # module's `cairn:merge-target` / `cairn:merge-content-*`
    # directives drive a mechanical merge into the named target
    # template's `cairn:slot` anchor.  Modules without structured
    # directives are silently skipped (transitional; not every
    # module ships directives yet).  Non-interactive defer is the
    # safe default; explicit --non-interactive or non-TTY stdin
    # forces it (Antigravity P1 disposition).
    non_interactive = args.non_interactive or not sys.stdin.isatty()
    try:
        merge_results, fidelity_warnings = run_module_merge_pass(
            templates_root, target, modules,
            non_interactive=non_interactive,
        )
    except DuplicateSlotError as exc:
        print(f"error: module-merge parse phase: {exc}", file=sys.stderr)
        return 2
    if merge_results or fidelity_warnings:
        print("\nModule-merge pass:")
        for r in merge_results:
            tag = f"  [{r.status}]"
            extra = (
                f" -> {r.side_file}" if r.side_file else ""
            )
            print(f"{tag} {r.target_path} > {r.slot_name}{extra}")
        for target_rel, slot_name, reason in fidelity_warnings:
            print(
                f"  [slot-content-{reason}] {target_rel} > {slot_name} "
                f"(fidelity check)"
            )

    # Seed the lifecycle skills' machine-state .gitignore entries
    # (unconditional -- the skills always install): the untracked interpreter
    # binding + the full-handoff lock.
    skills_ignored = seed_gitignore(target, _SKILLS_GITIGNORE)
    if skills_ignored:
        print(f"\nSeeded .gitignore (skills): {', '.join(skills_ignored)}")

    # Seed adopter-owned .gitignore for selected modules (Cairn v0.2 P5,
    # C6: non-clobber + idempotent), and print the OPT-IN hook command --
    # the scaffold never mutates .git/hooks itself (C2).
    for mod in modules:
        entries = _GITIGNORE_SEEDS.get(mod, ())
        if not entries:
            continue
        added = seed_gitignore(target, entries)
        if added:
            print(f"\nSeeded .gitignore ({mod}): {', '.join(added)}")
        else:
            print(
                f"\n.gitignore already covers the {mod} entr"
                f"{'y' if len(entries) == 1 else 'ies'}: "
                f"{', '.join(entries)}"
            )
    if "coordination-tiers" in modules:
        print(
            "\nRECOMMENDED (concurrent team) -- enable the work-intent git\n"
            "hooks. They are opt-in: the scaffold never mutates .git/hooks,\n"
            "so this is a one-time Day-1 step you run. Without them,\n"
            "dev/intents.jsonl stays empty even on a concurrent team -- the\n"
            "coordination signal this module exists for. Run:\n"
            "  python tools/intent.py install-hook        "
            "# post-commit auto-release\n"
            "  python tools/intent.py install-precommit   "
            "# pre-commit work-intent check (warn-only)\n"
            "  python tools/intent.py hooks-status        "
            "# confirm both are installed\n"
            "Opt out (now or later): re-run either install command with\n"
            "--uninstall. Your onboarding tasks include this step."
        )

    # Write the install lockfile + base-template cache: the upgrade
    # ancestor anchor (dev/.cairn/cairn-lock.yml + dev/.cairn/base/).  Fail-closed
    # if the tree diverges from a clean install (P-1) -- then it points the
    # user at `upgrade --init-lock` and the install still succeeds.
    lock_profile: dict[str, Any] = {"preset": cfg.get("preset")}
    lock_profile["axes"] = {
        axis: resolved_axes.get(axis)
        for axis in _AXES
        if isinstance(resolved_axes, dict) and resolved_axes.get(axis)
    }
    try:
        lock = write_install_lockfile(
            target, cairn_root, templates_root,
            tokens=tokens, modules=modules, optional=optional,
            profile=lock_profile,
            onboarding_preset=preset_name,
        )
    except PresetError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if lock is not None:
        print(
            f"\nWrote {_LOCKFILE_REL} (upgrade ancestor) + the base-template "
            f"cache under {_BASE_CACHE_REL}/."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
