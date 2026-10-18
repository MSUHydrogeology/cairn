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
import sys
from pathlib import Path
from typing import Any

from .security import ScaffoldSecurityError
from .slotmerge import DuplicateSlotError
from .config import (
    KNOWN_TOKENS,
    PresetError,
    _AXES,
    _DEFAULT_ON_MODULES,
    _GITIGNORE_SEEDS,
    _SKILLS_GITIGNORE,
    _SKILLS_MAPPINGS,
    _as_str_list,
    expand_preset,
    format_profile_summary,
    load_config,
    missing_required_tokens,
    reference_script_token_defaults,
    select_optional_templates,
    token_gated_modules,
)
from .lockfile import _BASE_CACHE_REL, _LOCKFILE_REL
from .install import (
    InstallResult,
    _FORGE_REFERENCE_DIRS,
    _MODEL_SELECTION_MAPPING_REL,
    _ONBOARDING_PRESETS,
    capability_install_notice_lines,
    capture_model_selection_mapping,
    create_dev_tree,
    fan_out_skills,
    format_manifest,
    git_provenance_warning,
    install_core,
    install_issue_capture_reference,
    install_modules,
    install_onboarding,
    install_optional,
    install_skills,
    print_report,
    run_module_merge_pass,
    seed_gitignore,
    write_install_lockfile,
    write_local_env,
)
from .upgrade import _cairn_root, cmd_upgrade


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

    # --summary is the pre-install acceptance artifact: resolve the
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
                # Capability install notice (call site 1 of
                # 2): the capability install notice, on the pre-install
                # `--summary` acceptance artifact -- both capabilities are
                # explicit-selection only, so a Maintainer accepting a
                # `--summary` never otherwise sees that one was chosen.
                summary_modules, _summary_s = expand_preset(summary_cfg)
                notice = capability_install_notice_lines(summary_modules)
                if notice:
                    sys.stdout.write("\n".join(notice) + "\n")
            else:
                # No preset: the modules: list (or the default-on set) is the
                # literal install -- summarize it plainly.
                mods = (
                    _as_str_list(summary_cfg.get("modules"), "modules")
                    if "modules" in summary_cfg
                    else list(_DEFAULT_ON_MODULES)
                )
                token_selected = (
                    [] if "modules" in summary_cfg
                    else token_gated_modules(summary_cfg)
                )
                mods.extend(m for m in token_selected if m not in mods)
                project = str(summary_cfg.get("project_name") or "<project_name>")
                out = [f"## Dimension profile -- {project}", "",
                       "Preset: (none -- literal module list)", "",
                       "Module roster (to install):"]
                out.extend(f"  - {m}" for m in mods)
                if token_selected:
                    out.extend([
                        "",
                        "Token-gated (selected by a declared token): "
                        + ", ".join(token_selected),
                    ])
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
    # shapes, plus the preset fast path:
    #   * `preset:` -> expand to a roster via the pinned ordered merge
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
        token_selected = token_gated_modules(cfg)
        modules.extend(m for m in token_selected if m not in modules)
        resolved_axes = cfg
        print(
            "  [info] profile omits `modules:` and `preset:`; installing the "
            f"default-on set ({', '.join(_DEFAULT_ON_MODULES)}).  Set "
            "`modules: []` to opt out explicitly, pick a `preset:`, or list a "
            "specific selection.",
            file=sys.stderr,
        )
        if token_selected:
            print(
                "  [info] token-gated additions selected by declared tokens: "
                f"{', '.join(token_selected)}.",
                file=sys.stderr,
            )

    # Optional top-level templates (foldback #10): selected by the
    # dimension axes — e.g. the human-team axis selects CONTRIBUTING.md
    # at small-multi / large-multi.  Fed the RESOLVED axes (preset point +
    # overrides when a `preset:` is used, else the raw profile) per the
    # seam foldback #10 left for the preset path.
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
    # scaffold installs the scripts to, unless the profile already
    # supplied a value.  This makes the shipped scripts immediately
    # runnable via the documented {{claim_check_command}} /
    # {{metrics_command}} line, and keeps the doc's invocation and the
    # install destination from desyncing.
    for token, value in reference_script_token_defaults(modules).items():
        tokens.setdefault(token, value)

    # Selected-module required-token preflight (security-apparatus-enrichment
    # preflight).  A selected module may declare
    # inline tokens that have no safe default (e.g. python-security's
    # {{python_package}}); rendering its files with the token unfilled would
    # leave a partially-installed, lockfile-recorded security stack containing
    # the literal placeholder.  Resolve every required token for every selected
    # module BEFORE any target-tree or lockfile write, and FAIL CLOSED (no
    # files, no lockfile / module-state mutation) on the first unfilled one.
    # Runs ahead of the --dry-run report too, so a dry run surfaces the gap
    # rather than printing a falsely-clean plan.
    required_gaps = missing_required_tokens(modules, tokens)
    if required_gaps:
        by_module: dict[str, list[str]] = {}
        for module, token in required_gaps:
            by_module.setdefault(module, []).append(token)
        print(
            "error: required token(s) for selected module(s) are unfilled; "
            "refusing to install (no files written):",
            file=sys.stderr,
        )
        for module in sorted(by_module):
            print(
                f"  - {module}: {', '.join(sorted(by_module[module]))}",
                file=sys.stderr,
            )
        print(
            "Fill the token(s) in the profile (or deselect the module) and "
            "re-run.",
            file=sys.stderr,
        )
        return 2

    # A linked .gitignore is refused here, before the first write, so the
    # refusal never leaves a half-installed tree and a dry run predicts it.
    # seed_gitignore's own guard is what runs: with no entries it writes nothing.
    try:
        seed_gitignore(target, (), dry_run=True)
    except ScaffoldSecurityError as exc:
        print(f"error: .gitignore seed refused (containment): {exc}\n"
              "  replace the link with a regular file, then re-run.",
              file=sys.stderr)
        return 2

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
            "tools/session.py + .agents/skills/{session-start,session-end}/"
            "SKILL.md (+ untracked dev/.cairn/local-env.json)"
        )
        for mod in modules:
            for entry in _GITIGNORE_SEEDS.get(mod, ()):  # dry-run
                would = seed_gitignore(target, (entry,), dry_run=True)
                if would:
                    print(f"[dry-run] Would seed .gitignore: {entry}")
        return 0

    # Create directory tree
    print(f"\nScaffolding Cairn into: {target}")
    if args.force:
        print("  (--force: existing files will be overwritten)")
    dirs_created = create_dev_tree(target)

    # The embedded six-axis profile used to strip `cairn:if` regions from the
    # always-on surface (cairn-profile-sized-assembly).  Computed ONCE here so
    # the install, the lockfile's expected-clean-install `would`, verify, and the
    # 3-way merge all key off byte-identical axes -- the lockfile divergence
    # check (install == cached) demands the install-strip and the `would`-strip
    # see the same point.  This is exactly the axes block embedded in the
    # lockfile `profile` below.
    embedded_axes: dict[str, Any] = {
        axis: resolved_axes.get(axis)
        for axis in _AXES
        if isinstance(resolved_axes, dict) and resolved_axes.get(axis)
    }

    # Install core templates
    print("Installing core templates ...")
    core_results = install_core(
        templates_root, target, tokens, axes=embedded_axes, force=args.force
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
        f"(+ the tools/session.py CLI). Try "
        f"`python tools/session.py session-start`."
    )
    env_result = write_local_env(target, force=args.force)
    if env_result[3] == "installed":
        print(f"  Wrote interpreter binding: {env_result[0]} (untracked)")
    # Fan the canonical skills out to in-use vendor read-paths (symlink, or a
    # gitignored generated copy where symlinks are unavailable).  A containment
    # violation here is reported as a crisp non-zero exit, not a traceback
    # local-env.json is already gitignored by this point.
    try:
        fanout = fan_out_skills(templates_root, target, force=args.force)
    except ScaffoldSecurityError as exc:
        print(f"error: skills fan-out refused (containment): {exc}",
              file=sys.stderr)
        return 2
    for name, tier, status in fanout:
        if status == "skipped-vendor-absent":
            # The normal first-install state: the harness config
            # dir doesn't exist until the adopter's first launch, so this
            # is expected, not a fault -- a calm no-action line, never
            # "skipped"/"error" (session-start's self-heal fans out the
            # link automatically once the dir exists, lifecycle.py's
            # _heal_skills_fanout).
            print(
                f"  Skills fan-out [{tier}] {name}: link automatically the "
                f"first time you launch your harness -- no action needed."
            )
        elif status != "noop":
            print(f"  Skills fan-out [{tier}] {name}: {status}")

    # Install progressive-onboarding content.  Must run AFTER
    # install_core because it edits the just-installed
    # dev/PLANNING.md's `onboarding-tasks` slot.  Always installs the
    # helper script + seeds the activation log; only
    # populates the slot + copies the preset source file when a
    # `preset:` is selected.
    preset_name = str(cfg.get("preset") or "").strip() or None
    label = (
        f"progressive onboarding ({preset_name})"
        if preset_name
        else "progressive onboarding (helper + log only; no preset)"
    )
    print(f"Installing {label} ...")
    # install_onboarding fails closed (ScaffoldSecurityError) on an incomplete
    # always-on launcher+engine completeness group BEFORE any write. Convert that
    # to a crisp non-zero exit (no traceback), mirroring the skills-fanout guard.
    try:
        onboarding_results = install_onboarding(
            templates_root, target, preset_name,
            axes=embedded_axes, force=args.force,
        )
    except ScaffoldSecurityError as exc:
        print(f"error: onboarding install refused: {exc}", file=sys.stderr)
        return 2

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
    # forces it.
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

    # model-selection interactive capture (foldback #2): when the module is
    # selected and the install is interactive, capture the adopter's
    # tier -> model bindings now so the fidelity gate ships green; a
    # non-interactive / CI install keeps the FILL ME stub (the gate then flags
    # it until filled by hand). Runs before the lockfile write so the recorded
    # mapping is the filled one. Never blocks the install.
    if "model-selection" in modules:
        try:
            wrote = capture_model_selection_mapping(
                target, interactive=not non_interactive)
        except KeyboardInterrupt:
            wrote = False
            print("\n  model-selection: capture interrupted; FILL ME stub kept.",
                  file=sys.stderr)
        if not wrote and not non_interactive:
            print("  model-selection: kept the FILL ME stub -- fill "
                  f"{_MODEL_SELECTION_MAPPING_REL} and run "
                  "`python scripts/check_model_selection.py`.", file=sys.stderr)

    # Capability install notice (call site 2 of 2): the
    # capability install notice, printed post-install beside the
    # model-selection notice just above -- same "adoption must not be
    # silent" principle Chunk C established for security-verification.
    for line in capability_install_notice_lines(modules):
        print(line)

    # Seed the lifecycle skills' machine-state .gitignore entries
    # (unconditional -- the skills always install): the untracked interpreter
    # binding + the full-handoff lock.
    skills_ignored = seed_gitignore(target, _SKILLS_GITIGNORE)
    if skills_ignored:
        print(f"\nSeeded .gitignore (skills): {', '.join(skills_ignored)}")

    # Seed adopter-owned .gitignore for selected modules
    # (non-clobber + idempotent), and print the OPT-IN hook command --
    # the scaffold never mutates .git/hooks itself.
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

    # security-verification-activation Chunk C: the non-silent install.
    # Adoption must not be silent, and it must not overclaim -- the whole
    # point of the note is that installing a ROUTE is not gathering
    # evidence.  Runs no host tool, on the `coordination-tiers` precedent
    # just above: the scaffold prints a command for the adopter to run and
    # never runs it (mechanically -- every subprocess the
    # install makes must be `git`, and none may name the dispatcher).
    if "security-verification" in modules:
        print(
            "\nNOTE (security-verification) -- an evidence ROUTE was\n"
            "installed, and nothing was inspected. The scaffold ran no host\n"
            "tool and makes no claim about this repository. Run the\n"
            "dispatcher yourself to see what it reports:\n"
            "  python scripts/run_security_verification.py local\n"
            "Its registry admits a fixed, source-owned set of capabilities\n"
            "(api-web-security-modules Chunk G); a selected capability with\n"
            "no admitted registry entry reports INCOMPLETE."
        )

    # Write the install lockfile + base-template cache: the upgrade
    # ancestor anchor (dev/.cairn/cairn-lock.yml + dev/.cairn/base/).  Fail-closed
    # if the tree diverges from a clean install (P-1) -- then it points the
    # user at `upgrade --init-lock`, or at `upgrade --plan` when a readable
    # lockfile is already there, and the install still succeeds.
    lock_profile: dict[str, Any] = {"preset": cfg.get("preset")}
    lock_profile["axes"] = embedded_axes
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
