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
from pathlib import Path
from typing import Any

try:
    import yaml as _yaml  # type: ignore[import]

    def _yaml_load(text: str) -> Any:
        return _yaml.safe_load(text)

except ImportError:  # pragma: no cover
    _yaml = None  # type: ignore[assignment]

    def _yaml_load(text: str) -> Any:
        return _minimal_yaml_parse(text)


# ---------------------------------------------------------------------------
# Token and slot patterns
# ---------------------------------------------------------------------------

#: Matches ``{{token_name}}`` tokens.
_TOKEN_RE = re.compile(r"\{\{(\w+)\}\}")

#: Matches the opening tag of a cairn block slot.
_SLOT_RE = re.compile(r"<!--\s*cairn:slot\s+(\S+)\s*-->", re.IGNORECASE)

#: The inline tokens the core templates currently use.  The scaffold
#: only substitutes tokens present in this set; unknown keys from the
#: config are silently ignored so that future tokens do not break old
#: configs.
KNOWN_TOKENS: frozenset[str] = frozenset(
    {
        "project_name",
        "test_command",
    }
)


def substitute_tokens(text: str, tokens: dict[str, str]) -> str:
    """Replace ``{{key}}`` tokens found in *tokens*; leave others intact."""

    def _replace(m: re.Match[str]) -> str:
        return tokens.get(m.group(1), m.group(0))

    return _TOKEN_RE.sub(_replace, text)


def find_unfilled_tokens(text: str) -> list[str]:
    """Return token names that remain unfilled (i.e. still ``{{...}}``)."""
    return _TOKEN_RE.findall(text)


def find_block_slots(text: str) -> list[str]:
    """Return slot names found in *text*."""
    return _SLOT_RE.findall(text)


# ---------------------------------------------------------------------------
# Minimal YAML fallback (no dependency on PyYAML)
# ---------------------------------------------------------------------------

def _minimal_yaml_parse(text: str) -> dict[str, Any]:
    """Very small YAML parser covering the subset scaffold.py needs.

    Handles::

        key: value
        key:
          - item

    Not a full YAML parser.  PyYAML is used when available.
    """
    result: dict[str, Any] = {}
    current_list_key: str | None = None

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if line[:1] in (" ", "\t"):
            # List item under current_list_key
            if current_list_key is not None and stripped.startswith("- "):
                item = stripped[2:].split("#")[0].strip().strip('"').strip("'")
                if item:
                    result.setdefault(current_list_key, []).append(item)
        elif ":" in line:
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest and not rest.startswith("#"):
                result[key] = rest.strip('"').strip("'")
                current_list_key = None
            else:
                current_list_key = key
                if key not in result:
                    result[key] = []

    return result


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_config(config_path: Path) -> dict[str, Any]:
    """Load a profile YAML config file."""
    text = config_path.read_text(encoding="utf-8")
    cfg = _yaml_load(text)
    if not isinstance(cfg, dict):
        raise ValueError(
            f"{config_path}: expected a YAML mapping at the top level, "
            f"got {type(cfg).__name__}"
        )
    return cfg


# ---------------------------------------------------------------------------
# dev/ directory tree
# ---------------------------------------------------------------------------

#: Relative paths (from repo root) that the scaffold always creates.
_DEV_DIRS: tuple[str, ...] = (
    "dev",
    "dev/proposals",
    "dev/proposals/archive",
    "dev/plans",
    "dev/plans/archive",
    "dev/modules",
)


def create_dev_tree(target: Path, *, dry_run: bool = False) -> list[Path]:
    """Create the ``dev/`` directory tree under *target*.

    Returns the list of directories that were (or would be) created.
    """
    created: list[Path] = []
    for rel in _DEV_DIRS:
        d = target / rel
        if not d.exists():
            if not dry_run:
                d.mkdir(parents=True, exist_ok=True)
            created.append(d)
    return created


# ---------------------------------------------------------------------------
# Template installation
# ---------------------------------------------------------------------------

# Each entry is (source path relative to cairn/templates/, target path
# relative to repo root).
_CORE_MAPPINGS: tuple[tuple[str, str], ...] = (
    # repo root
    ("core/AGENTS.md",                              "AGENTS.md"),
    # dev/ tree
    ("core/dev/README.md",                          "dev/README.md"),
    ("core/dev/PLANNING.md",                        "dev/PLANNING.md"),
    ("core/dev/NEXT_SESSION.md",                    "dev/NEXT_SESSION.md"),
    ("core/dev/collaboration_agreement.md",         "dev/collaboration_agreement.md"),
    ("core/dev/agent_collaboration.md",             "dev/agent_collaboration.md"),
    ("core/dev/proposals/_template.md",             "dev/proposals/_template.md"),
    ("core/dev/plans/_template.md",                 "dev/plans/_template.md"),
)

# Module name → (source relative to cairn/templates/modules/,
#               target relative to repo root)
_MODULE_MAPPINGS: dict[str, tuple[str, str]] = {
    # default-on
    "lifecycle-metrics":   (
        "default-on/lifecycle-metrics.md",
        "dev/modules/lifecycle-metrics.md",
    ),
    "reflections":         (
        "default-on/reflections.md",
        "dev/modules/reflections.md",
    ),
    "claim-check":         (
        "default-on/claim-check.md",
        "dev/modules/claim-check.md",
    ),
    # team-gated
    "dual-review":         (
        "team-gated/dual-review.md",
        "dev/modules/dual-review.md",
    ),
    "domain-agents":       (
        "team-gated/domain-agents.md",
        "dev/modules/domain-agents.md",
    ),
    "legacy-agent":        (
        "team-gated/legacy-agent.md",
        "dev/modules/legacy-agent.md",
    ),
    "dual-language-tests": (
        "team-gated/dual-language-tests.md",
        "dev/modules/dual-language-tests.md",
    ),
    "coordination-tiers":  (
        "team-gated/coordination-tiers.md",
        "dev/modules/coordination-tiers.md",
    ),
}

#: Result record for one installed file.
InstallResult = tuple[Path, list[str], list[str]]
# (target_path, unfilled_token_names, block_slot_names)


def _install_one(
    src: Path,
    dst: Path,
    tokens: dict[str, str],
    *,
    dry_run: bool,
) -> InstallResult:
    """Copy *src* to *dst*, substituting tokens.  Returns an InstallResult."""
    text = src.read_text(encoding="utf-8")
    text = substitute_tokens(text, tokens)
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
    return dst, find_unfilled_tokens(text), find_block_slots(text)


def install_core(
    templates_root: Path,
    target: Path,
    tokens: dict[str, str],
    *,
    dry_run: bool = False,
) -> list[InstallResult]:
    """Copy core templates into *target*, substituting tokens."""
    results: list[InstallResult] = []
    for src_rel, dst_rel in _CORE_MAPPINGS:
        src = templates_root / src_rel
        if not src.exists():
            print(f"  [warn] core template missing: {src_rel}", file=sys.stderr)
            continue
        dst = target / dst_rel
        results.append(_install_one(src, dst, tokens, dry_run=dry_run))
    return results


def install_modules(
    templates_root: Path,
    target: Path,
    tokens: dict[str, str],
    module_names: list[str],
    *,
    dry_run: bool = False,
) -> list[InstallResult]:
    """Copy selected module templates into *target*.

    Module source paths in ``_MODULE_MAPPINGS`` are relative to
    ``templates_root / "modules"`` (i.e. ``cairn/templates/modules/``).
    """
    modules_root = templates_root / "modules"
    results: list[InstallResult] = []
    known = set(_MODULE_MAPPINGS)
    for name in module_names:
        if name not in known:
            print(
                f"  [warn] unknown module '{name}' — skipped. "
                f"Known modules: {', '.join(sorted(known))}",
                file=sys.stderr,
            )
            continue
        src_rel, dst_rel = _MODULE_MAPPINGS[name]
        src = modules_root / src_rel
        if not src.exists():
            print(f"  [warn] module template missing: {src_rel}", file=sys.stderr)
            continue
        dst = target / dst_rel
        results.append(_install_one(src, dst, tokens, dry_run=dry_run))
    return results


# ---------------------------------------------------------------------------
# Post-scaffold report
# ---------------------------------------------------------------------------

def print_report(
    target: Path,
    dirs_created: list[Path],
    installed: list[InstallResult],
) -> None:
    """Print a human-readable post-scaffold report to stdout."""
    print()
    print("=" * 68)
    print("  Cairn scaffold complete")
    print("=" * 68)
    print(f"\nTarget repository : {target}")
    print(f"Directories created ({len(dirs_created)}):")
    for d in dirs_created:
        print(f"  {d.relative_to(target)}/")

    print(f"\nFiles installed ({len(installed)}):")
    for dst, _unfilled, _slots in installed:
        print(f"  {dst.relative_to(target)}")

    # Unfilled inline tokens
    all_unfilled = sorted(
        {tok for _, unfilled, _ in installed for tok in unfilled}
    )
    if all_unfilled:
        print(f"\n[WARN] {len(all_unfilled)} unfilled token(s) remain:")
        for tok in all_unfilled:
            print(f"  {{{{ {tok} }}}}")
        print("  -> Add these to the profile config and re-run, or fill manually.")
    else:
        print("\n[OK] All inline tokens substituted.")

    # Block slots needing agent attention
    all_slots = [
        (dst.relative_to(target), slot)
        for dst, _, slots in installed
        for slot in slots
    ]
    if all_slots:
        print(f"\nBlock slots requiring agent attention ({len(all_slots)}):")
        for path, slot in all_slots:
            print(f"  {path}  [cairn:slot {slot}]")
        print("  -> See BOOTSTRAP.md Act II-4 for guidance.")
    else:
        print("\n[OK] No block slots detected.")

    print()
    print("Next steps (BOOTSTRAP.md Act II):")
    print("  3. Confirm the installed files match the accepted profile (II-3).")
    print("  4. Fill all block slots (II-4).")
    print("  5. Run the R-F acceptance gate (II-5).")
    print("  6. Dogfood one change through the lifecycle (II-6).")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _find_cairn_root(script_path: Path) -> Path:
    """Locate the Cairn repo root as two directories above this script.

    ``bootstrap/scaffold.py`` → ``bootstrap/`` → ``<cairn root>``.
    """
    return script_path.resolve().parent.parent


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="scaffold.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--config",
        required=True,
        metavar="PROFILE_YAML",
        help="Path to the profile YAML config (see Appendix B in BOOTSTRAP.md).",
    )
    p.add_argument(
        "--target",
        required=True,
        metavar="REPO_ROOT",
        help="Path to the target repository root.",
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
    return p


def main(argv: list[str] | None = None) -> int:
    """Entry point.  Returns an exit code (0 = success, 1 = error)."""
    parser = build_arg_parser()
    args = parser.parse_args(argv)

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
        else _find_cairn_root(Path(__file__))
    )
    templates_root = cairn_root / "templates"
    if not templates_root.exists():
        print(
            f"error: templates/ not found under Cairn root: {cairn_root}",
            file=sys.stderr,
        )
        return 1

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
    modules: list[str] = [str(m) for m in cfg.get("modules", [])]

    if args.dry_run:
        print("[dry-run] Would install to:", target)
        print("[dry-run] Tokens:          ", tokens)
        print("[dry-run] Modules:         ", modules)
        return 0

    # Create directory tree
    print(f"\nScaffolding Cairn into: {target}")
    dirs_created = create_dev_tree(target)

    # Install core templates
    print("Installing core templates ...")
    core_results = install_core(templates_root, target, tokens)

    # Install module templates
    print(f"Installing modules: {', '.join(modules) or '(none)'} ...")
    module_results = install_modules(templates_root, target, tokens, modules)

    print_report(target, dirs_created, core_results + module_results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
