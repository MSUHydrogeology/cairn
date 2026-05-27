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
from typing import Any, NamedTuple

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

#: Matches the closing tag of a cairn block slot.
_SLOT_END_RE = re.compile(r"<!--\s*cairn:end\s+(\S+)\s*-->", re.IGNORECASE)

#: The inline tokens the core and module templates currently use.  The
#: scaffold only substitutes tokens present in this set; unknown keys
#: from the config are silently ignored so that future tokens do not
#: break old configs.  Documented in BOOTSTRAP.md Appendix A.
KNOWN_TOKENS: frozenset[str] = frozenset(
    {
        "project_name",
        "test_command",
        "claim_check_command",
        "metrics_command",
    }
)

#: Document-author placeholders -- written as ``{{...}}`` but
#: intentionally *kept unfilled* in installed templates, to be filled
#: at write-time by a document author (e.g., a reviewer writing a
#: Review section).  The scaffold does not substitute these and the
#: post-scaffold "unfilled token" report excludes them.  Documented in
#: BOOTSTRAP.md Appendix A and templates/README.md.
_DOC_AUTHOR_TOKENS: frozenset[str] = frozenset(
    {
        "Maintainer",
        "author",
        "reviewer",
        "assessor",
    }
)

#: Default-on modules installed when the profile YAML omits a
#: ``modules:`` key.  Matches the doctrine in BOOTSTRAP.md Act I-5
#: step 2 ("Default-on modules (installed *unless* a dimension removes
#: them)").
_DEFAULT_ON_MODULES: tuple[str, ...] = (
    "lifecycle-metrics",
    "reflections",
    "claim-check",
)


def substitute_tokens(text: str, tokens: dict[str, str]) -> str:
    """Replace ``{{key}}`` tokens found in *tokens*; leave others intact."""

    def _replace(m: re.Match[str]) -> str:
        return tokens.get(m.group(1), m.group(0))

    return _TOKEN_RE.sub(_replace, text)


def find_unfilled_tokens(text: str) -> list[str]:
    """Return token names that remain unfilled, excluding document-author
    placeholders that are intentionally kept unfilled at install time.
    """
    return [
        tok for tok in _TOKEN_RE.findall(text)
        if tok not in _DOC_AUTHOR_TOKENS
    ]


def find_block_slots(text: str) -> list[str]:
    """Return slot names found in *text* (open markers only)."""
    return _SLOT_RE.findall(text)


def find_unpaired_slots(text: str) -> list[str]:
    """Return slot names whose ``<!-- cairn:slot NAME -->`` opener has no
    matching ``<!-- cairn:end NAME -->`` closer, or vice versa.

    Useful for catching template-author errors at scaffold time rather
    than at customization time.
    """
    opens = _SLOT_RE.findall(text)
    closes = _SLOT_END_RE.findall(text)
    open_set = set(opens)
    close_set = set(closes)
    return sorted((open_set ^ close_set))


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

    def _list_item_text(stripped: str) -> str:
        """Strip leading ``- ``, an optional trailing ``# comment``, and
        surrounding quotes, returning the item value."""
        return stripped[2:].split("#")[0].strip().strip('"').strip("'")

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if line[:1] in (" ", "\t"):
            # Indented continuation -- list item under current_list_key.
            if current_list_key is not None and stripped.startswith("- "):
                item = _list_item_text(stripped)
                if item:
                    result.setdefault(current_list_key, []).append(item)
        elif stripped.startswith("- ") and current_list_key is not None:
            # Unindented list item under current_list_key.  PyYAML
            # accepts both ``key:\n  - a`` and ``key:\n- a`` shapes;
            # the minimal parser honors the second form too so a
            # PyYAML-free environment behaves the same way.
            item = _list_item_text(stripped)
            if item:
                result.setdefault(current_list_key, []).append(item)
        elif ":" in line:
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest and not rest.startswith("#"):
                # Recognize inline empty list/dict notations so e.g.
                # ``modules: []`` is honored as an explicit opt-out.
                if rest in ("[]", "{}"):
                    result[key] = []
                    current_list_key = None
                else:
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
    # Thin vendor wrapper (foldback #12): installed as VENDOR.md, a
    # vendor-neutral `@AGENTS.md` + harness-addendum template the
    # adopter renames to their tool's file (CLAUDE.md, etc.).  Core
    # ships no literal vendor name (R-G).
    ("core/VENDOR.md",                              "VENDOR.md"),
    # dev/ tree
    ("core/dev/README.md",                          "dev/README.md"),
    ("core/dev/PLANNING.md",                        "dev/PLANNING.md"),
    ("core/dev/NEXT_SESSION.md",                    "dev/NEXT_SESSION.md"),
    ("core/dev/collaboration_agreement.md",         "dev/collaboration_agreement.md"),
    ("core/dev/agent_collaboration.md",             "dev/agent_collaboration.md"),
    ("core/dev/proposals/_template.md",             "dev/proposals/_template.md"),
    ("core/dev/plans/_template.md",                 "dev/plans/_template.md"),
)

# Optional top-level templates, gated on a dimension axis.  Unlike
# modules (which land under ``dev/modules/``), these are project-root
# files an adopter's *human* contributors read.  Each entry is
# ``(src rel to templates/, dst rel to repo root, gate axis, selecting
# values)``: the template installs when the *resolved* profile value for
# that axis is in the selecting set.  An installed optional template is
# recorded under ``optional_templates:`` in the fidelity manifest so the
# gate is auditable (bootstrap/fidelity-check.md).
_OPTIONAL_TEMPLATES: tuple[tuple[str, str, str, frozenset[str]], ...] = (
    # CONTRIBUTING.md — the human-contributor entry (foldback #10),
    # installed when the repo expects human authors beyond a solo
    # maintainer: the human-team axis at small-multi or large-multi.
    (
        "optional/CONTRIBUTING.md",
        "CONTRIBUTING.md",
        "human_team",
        frozenset({"small-multi", "large-multi"}),
    ),
)


def select_optional_templates(axes: dict[str, object]) -> list[tuple[str, str]]:
    """Return ``(src, dst)`` for each optional template whose dimension
    gate the profile satisfies.

    *axes* is the **resolved** dimension profile — a preset's canonical
    point merged with the adopter's overrides (``resolve_axes``), or the
    raw profile when no ``preset:`` is used.  A profile that omits the
    gate axis, or sets it to a non-selecting value, gets no optional
    template — the conservative default.
    """
    selected: list[tuple[str, str]] = []
    for src, dst, axis, values in _OPTIONAL_TEMPLATES:
        if str(axes.get(axis, "")) in values:
            selected.append((src, dst))
    return selected


class InstallSpec(NamedTuple):
    """One file a module installs.

    ``src`` is relative to ``cairn/templates/modules/``; ``dst`` is
    relative to the target repo root.  ``verbatim`` marks an executable
    script (or any non-template asset) that is copied **byte-for-byte**:
    no ``{{token}}`` substitution runs over it, and it is not scanned for
    unfilled tokens / block slots (a code file's f-string braces or
    docstring would otherwise false-positive the post-scaffold report).
    """

    src: str
    dst: str
    verbatim: bool = False


# Module name → list of InstallSpec (1:many).  Most modules install a
# single substituted ``.md`` doctrine file; the two default-on
# discipline modules also install their reference *script* verbatim
# (Cairn v0.2 P1).  The script ``dst`` paths are the single source of
# truth for the command-token defaults below (see
# ``_REFERENCE_SCRIPT_TOKEN`` and ``reference_script_token_defaults``)
# so the doc's "run it via {{...}}" line and the install destination
# cannot desync.
_MODULE_MAPPINGS: dict[str, list[InstallSpec]] = {
    # default-on
    "lifecycle-metrics": [
        InstallSpec("default-on/lifecycle-metrics.md",
                    "dev/modules/lifecycle-metrics.md"),
        InstallSpec("default-on/lifecycle_metrics.py",
                    "tools/lifecycle_metrics.py", verbatim=True),
    ],
    "reflections": [
        InstallSpec("default-on/reflections.md", "dev/modules/reflections.md"),
    ],
    "claim-check": [
        InstallSpec("default-on/claim-check.md",
                    "dev/modules/claim-check.md"),
        InstallSpec("default-on/claim_check.py",
                    "scripts/claim_check.py", verbatim=True),
    ],
    # team-gated
    "dual-review": [
        InstallSpec("team-gated/dual-review.md", "dev/modules/dual-review.md"),
    ],
    "domain-agents": [
        InstallSpec("team-gated/domain-agents.md",
                    "dev/modules/domain-agents.md"),
    ],
    "legacy-agent": [
        InstallSpec("team-gated/legacy-agent.md",
                    "dev/modules/legacy-agent.md"),
    ],
    "dual-language-tests": [
        InstallSpec("team-gated/dual-language-tests.md",
                    "dev/modules/dual-language-tests.md"),
    ],
    "coordination-tiers": [
        InstallSpec("team-gated/coordination-tiers.md",
                    "dev/modules/coordination-tiers.md"),
        # Cairn v0.2 P5: the work-intent tool ships verbatim alongside the
        # doctrine (1:many, the P1 claim-check/lifecycle-metrics pattern).
        InstallSpec("team-gated/intent.py",
                    "tools/intent.py", verbatim=True),
    ],
    "security-review": [
        InstallSpec("team-gated/security-review.md",
                    "dev/modules/security-review.md"),
    ],
    "issue-capture": [
        InstallSpec("team-gated/issue-capture.md",
                    "dev/modules/issue-capture.md"),
    ],
    "model-selection": [
        InstallSpec("team-gated/model-selection.md",
                    "dev/modules/model-selection.md"),
    ],
    # Practice-discipline modules (Cairn v0.2 P3).  Team-gated -- a
    # governance preset (P4) turns them on per profile rather than
    # doubling the default-on auto-install set.  Doctrine-only (single
    # substituted .md each; no scripts).
    "testing-discipline": [
        InstallSpec("team-gated/testing-discipline.md",
                    "dev/modules/testing-discipline.md"),
    ],
    "doc-drift-prevention": [
        InstallSpec("team-gated/doc-drift-prevention.md",
                    "dev/modules/doc-drift-prevention.md"),
        # Cairn v0.2 foldback: the module flips from doctrine-only to
        # doctrine + stack-neutral runnable tooling (1:many, the P1
        # claim-check pattern).  Two verbatim stdlib-only scripts -- the
        # link half and the snippet-sync.  The claim half is NOT shipped
        # here: the default-on claim-check module already installs
        # scripts/claim_check.py, so the doc-drift gate composes with it
        # rather than duplicating a second checker.  The schema-doc
        # generator is deferred (an adopter slot/hook) -- it cannot ship
        # stack-neutrally.
        InstallSpec("team-gated/link_check.py",
                    "scripts/link_check.py", verbatim=True),
        InstallSpec("team-gated/sync_doc_snippets.py",
                    "scripts/sync_doc_snippets.py", verbatim=True),
    ],
    "examples-gallery": [
        InstallSpec("team-gated/examples-gallery.md",
                    "dev/modules/examples-gallery.md"),
    ],
}

# Module → the inline command-token whose value should default to the
# module's installed reference script.  The default value is derived
# from the verbatim spec's ``dst`` (below), so the token the module doc
# resolves (``{{claim_check_command}}`` etc.) and the path the scaffold
# installs to are one source of truth (I5).
_REFERENCE_SCRIPT_TOKEN: dict[str, str] = {
    "claim-check": "claim_check_command",
    "lifecycle-metrics": "metrics_command",
}

#: Module → ``.gitignore`` entries the scaffold seeds when the module is
#: selected.  Cairn v0.2 P5: the work-intent log is session-local
#: coordination state, never a tracked artifact, so selecting
#: ``coordination-tiers`` seeds the substrate path.  Seeding is
#: non-clobber + idempotent (see :func:`seed_gitignore`).
_GITIGNORE_SEEDS: dict[str, tuple[str, ...]] = {
    "coordination-tiers": ("dev/intents.jsonl",),
}


def seed_gitignore(
    target: Path,
    entries: tuple[str, ...] | list[str],
    *,
    dry_run: bool = False,
) -> list[str]:
    """Append *entries* to ``<target>/.gitignore`` if absent.

    Adopter-owned-file contract (Cairn v0.2 P5, C6): **non-clobber**
    (existing content preserved verbatim), **idempotent** (an entry
    already present -- exact-line match, ignoring surrounding
    whitespace -- is never re-added, so repeated scaffolds add no
    duplicate lines), and **``--dry-run`` aware** (returns what *would*
    be added without writing).  Returns the entries actually added (or
    that would be added under ``dry_run``); an empty list means the
    file already covered everything.
    """
    gitignore = target / ".gitignore"
    text = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    existing = {ln.strip() for ln in text.splitlines()}
    to_add = [e for e in entries if e not in existing]
    if not to_add or dry_run:
        return to_add
    prefix = text
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    block = "\n".join(to_add) + "\n"
    gitignore.write_text(prefix + block, encoding="utf-8")
    return to_add


def reference_script_token_defaults(module_names: list[str]) -> dict[str, str]:
    """Default command-token values for the selected reference-script
    modules.

    For each selected module that ships a verbatim reference script, map
    its command token (``claim_check_command`` / ``metrics_command``) to
    ``python <dst>`` where ``<dst>`` is the exact path the scaffold
    installs the script to.  The caller injects these into the token set
    *without* overriding a value the profile already supplied
    (``setdefault`` semantics), so an adopter can still point the token
    at a custom invocation.
    """
    defaults: dict[str, str] = {}
    for name in module_names:
        token = _REFERENCE_SCRIPT_TOKEN.get(name)
        if token is None:
            continue
        for spec in _MODULE_MAPPINGS.get(name, []):
            if spec.verbatim:
                defaults[token] = f"python {spec.dst}"
                break
    return defaults


# ---------------------------------------------------------------------------
# Governance presets (Cairn v0.2 P4)
# ---------------------------------------------------------------------------
#
# Presets are *named points in the six-axis dimension model*, not a parallel
# config system.  An adopter picks a preset (the fast path) instead of
# hand-deriving the module roster; the six-axis scoring + the BOOTSTRAP.md
# I-5 gate table remain the principled backing (the gate table is the
# canonical per-module rationale).  See BOOTSTRAP.md Act I and the
# modflow_tools-hosted ``cairn-v0.2-p4-governance-presets`` plan.

#: The six dimension axes -> allowed enum values (the BOOTSTRAP.md I-4 table).
#: An adopter overrides a preset's canonical axis by setting a flat top-level
#: key in the profile YAML; an unknown enum value is a hard error.
_AXES: dict[str, tuple[str, ...]] = {
    "age": ("greenfield", "legacy"),
    "size": ("small", "medium", "large"),
    "complexity": ("simple", "moderate", "complex"),
    "language": ("single", "multi"),
    "human_team": ("solo", "small-multi", "large-multi"),
    "agent_team": (
        "single", "concurrent-single-type", "concurrent-multi-type",
    ),
}

#: Modules whose staffability is a pure function of the team axes.  These are
#: the ONLY part of the I-5 gate evaluated as runtime code; the non-axis gate
#: conditions (trust boundary, issue tracker, domain partitioning, legacy
#: readiness) are baked into each preset's authored baseline below (the
#: "gate-table encoding" split from the P4 plan).  Both gate on
#: ``agent_team == concurrent-multi-type`` per the I-5 table.
_TEAM_STAFFING_GATED: tuple[str, ...] = ("dual-review", "coordination-tiers")


def _can_staff_team_modules(axes: dict[str, str]) -> bool:
    """True when the resolved agent-team axis can staff the team-staffing
    modules (concurrent-multi-type)."""
    return axes.get("agent_team") == "concurrent-multi-type"


#: Named governance presets.  Each carries a **canonical six-axis point** and
#: a **baseline roster** of the *non-team-staffing* modules the I-5 gate table
#: yields at that point (axis-derivable rows resolved at the canonical scores,
#: plus the non-axis rows the preset's profile assumes).  The team-staffing
#: modules (``dual-review`` / ``coordination-tiers``) are NOT listed here --
#: they are added at expand time iff the *resolved* agent-team axis staffs
#: them, so an adopter's real team is ground truth (F3).  ``_DEFAULT_ON_MODULES``
#: is always the floor.  Derivation is documented row-by-row in BOOTSTRAP.md.
_PRESETS: dict[str, dict[str, object]] = {
    "solo-greenfield": {
        "axes": {
            "age": "greenfield", "size": "small", "complexity": "simple",
            "language": "single", "human_team": "solo",
            "agent_team": "single",
        },
        # Minimal: default-on only; no axis fires a team-gated module.
        "baseline": (),
    },
    "collaborative-team": {
        "axes": {
            "age": "greenfield", "size": "medium", "complexity": "moderate",
            "language": "single", "human_team": "small-multi",
            "agent_team": "concurrent-multi-type",
        },
        # complexity=moderate -> model-selection + testing-discipline;
        # size=medium -> doc-drift-prevention.  Coordination modules come
        # from the team-staffing gate (agent_team=concurrent-multi-type).
        "baseline": (
            "model-selection", "testing-discipline", "doc-drift-prevention",
        ),
    },
    "high-rigor-legacy": {
        "axes": {
            "age": "legacy", "size": "large", "complexity": "complex",
            "language": "multi", "human_team": "large-multi",
            "agent_team": "concurrent-multi-type",
        },
        # age=legacy -> legacy-agent; complexity=complex -> model-selection
        # + testing-discipline; size=large/language=multi ->
        # doc-drift-prevention; language=multi -> dual-language-tests;
        # trust-boundary (non-axis, assumed for legacy/large) ->
        # security-review.  Coordination modules from the team-staffing gate.
        "baseline": (
            "legacy-agent", "security-review", "dual-language-tests",
            "model-selection", "testing-discipline", "doc-drift-prevention",
        ),
    },
}


class PresetError(ValueError):
    """Raised on an invalid preset / override config (unknown preset, unknown
    module, unknown axis enum, wrong-type value, or the ``modules:`` +
    ``preset:`` conflict).  A friendly hard error, surfaced by ``main()``."""


def _as_str_list(value: object, key: str) -> list[str]:
    """Coerce a YAML value for a list-typed key to ``list[str]``; a scalar
    where a list is expected is a friendly hard error (Codex P-5)."""
    if value is None:
        return []
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise PresetError(
            f"`{key}` must be a YAML list (e.g. `{key}:` with `- module` "
            f"lines), not a {type(value).__name__} ({value!r})."
        )
    return [str(v) for v in value]


def _canonical_order(modules: set[str]) -> list[str]:
    """Order a module set deterministically: default-on first (in
    ``_DEFAULT_ON_MODULES`` order), then the rest in ``_MODULE_MAPPINGS``
    order.  Stable, diffable output for the summary + tests."""
    ordered: list[str] = [m for m in _DEFAULT_ON_MODULES if m in modules]
    for name in _MODULE_MAPPINGS:
        if name in modules and name not in ordered:
            ordered.append(name)
    # Any module not in the known maps (shouldn't happen post-validation)
    # trails, sorted, so nothing is silently dropped.
    ordered.extend(sorted(modules - set(ordered)))
    return ordered


def resolve_axes(preset_name: str, cfg: dict[str, object]) -> dict[str, str]:
    """Resolve the six-axis point: the preset's canonical point overridden by
    any flat axis key the adopter supplied.  An unknown enum value is a hard
    error; an absent axis key falls back to the preset's value (F3 / P-2)."""
    canonical = dict(_PRESETS[preset_name]["axes"])  # type: ignore[arg-type]
    resolved = dict(canonical)
    for axis, allowed in _AXES.items():
        if axis in cfg and cfg[axis] is not None:
            value = str(cfg[axis])
            if value not in allowed:
                raise PresetError(
                    f"axis `{axis}` value {value!r} is not one of "
                    f"{', '.join(allowed)}."
                )
            resolved[axis] = value
    return resolved


def expand_preset(cfg: dict[str, object]) -> tuple[list[str], dict[str, object]]:
    """Expand a ``preset:``-bearing profile into a module roster + a summary.

    The pinned ordered merge (P4 Decision):

    1. Resolve axes = preset canonical point overridden by adopter axis keys.
    2. Baseline = ``_DEFAULT_ON_MODULES`` (always) + the preset's authored
       non-team-staffing roster + the team-staffing modules iff the resolved
       agent-team axis staffs them.
    3. Apply ``modules_add`` then ``modules_remove`` -- **remove wins** on a
       same-module conflict; an explicit add of an unstaffable module installs
       it with a loud staffability warning.
    4. (Backward-compat for the no-preset cases is handled in ``main()``.)

    Returns ``(ordered_modules, summary)`` where ``summary`` carries the
    preset, resolved axes, roster, overrides, and any warnings (for the
    ``--summary`` acceptance artifact).
    """
    preset_name = str(cfg.get("preset") or "").strip()
    if preset_name not in _PRESETS:
        raise PresetError(
            f"unknown preset {preset_name!r}; choose one of "
            f"{', '.join(sorted(_PRESETS))}."
        )

    resolved_axes = resolve_axes(preset_name, cfg)

    # Step 2: baseline.
    baseline: set[str] = set(_DEFAULT_ON_MODULES)
    baseline |= set(_PRESETS[preset_name]["baseline"])  # type: ignore[arg-type]
    staffable = _can_staff_team_modules(resolved_axes)
    if staffable:
        baseline |= set(_TEAM_STAFFING_GATED)

    # Step 3: explicit overrides (validate names first).
    adds = _as_str_list(cfg.get("modules_add"), "modules_add")
    removes = _as_str_list(cfg.get("modules_remove"), "modules_remove")
    known = set(_MODULE_MAPPINGS) | set(_DEFAULT_ON_MODULES)
    for name in adds + removes:
        if name not in known:
            raise PresetError(
                f"unknown module {name!r} in modules_add/modules_remove; "
                f"known modules: {', '.join(sorted(known))}."
            )

    warnings: list[str] = []
    # Adds first.  An add of a team-staffing module the resolved team can't
    # staff installs anyway (adopter intent wins) with a loud warning (I1).
    for name in adds:
        if name in _TEAM_STAFFING_GATED and not staffable:
            warnings.append(
                f"`{name}` was explicitly added but the resolved agent-team "
                f"axis ({resolved_axes.get('agent_team')}) cannot staff it; "
                f"installing per your explicit request -- confirm the team "
                f"configuration can staff the module's coordination "
                f"requirements before relying on it."
            )
    roster = set(baseline) | set(adds)
    # Removes win on conflict.
    removed_default_on: list[str] = []
    for name in removes:
        roster.discard(name)
        if name in _DEFAULT_ON_MODULES:
            removed_default_on.append(name)

    ordered = _canonical_order(roster)
    summary: dict[str, object] = {
        "preset": preset_name,
        "axes": resolved_axes,
        "modules": ordered,
        "modules_add": adds,
        "modules_remove": removes,
        "removed_default_on": removed_default_on,
        "staffability_warnings": warnings,
    }
    return ordered, summary


def format_profile_summary(cfg: dict[str, object]) -> str:
    """Render the Maintainer-facing Act I-6 profile summary for a
    ``preset:``-bearing profile (the ``--summary`` acceptance artifact, P-4).

    Shows the chosen preset, the resolved six-axis point, the expanded module
    roster, the explicit add/remove overrides, any default-on opt-outs, and
    any staffability warnings -- so the Maintainer sees *why* the roster came
    out this way before anything is installed."""
    _modules, s = expand_preset(cfg)
    lines: list[str] = []
    project = str(cfg.get("project_name") or "<project_name>")
    lines.append(f"## Dimension profile -- {project}")
    lines.append("")
    lines.append(f"Preset: {s['preset']}")
    lines.append("")
    lines.append("Six-axis point (resolved):")
    for axis in _AXES:
        lines.append(f"  {axis:12s} {s['axes'][axis]}")  # type: ignore[index]
    lines.append("")
    lines.append("Module roster (to install):")
    for m in s["modules"]:  # type: ignore[union-attr]
        lines.append(f"  - {m}")
    if s["modules_add"]:
        lines.append(f"\nExplicit add:    {', '.join(s['modules_add'])}")  # type: ignore[arg-type]
    if s["modules_remove"]:
        lines.append(f"Explicit remove: {', '.join(s['modules_remove'])}")  # type: ignore[arg-type]
    if s["removed_default_on"]:
        lines.append(
            f"Default-on opted out: {', '.join(s['removed_default_on'])}"  # type: ignore[arg-type]
        )
    if s["staffability_warnings"]:
        lines.append("")
        # Same per-warning line format as the installer path in main()
        # (`[warn] staffability: ...`), so programmatic detection and the
        # user-facing presentation are consistent across both surfaces.
        for w in s["staffability_warnings"]:  # type: ignore[union-attr]
            lines.append(f"  [warn] staffability: {w}")
    lines.append("")
    lines.append("Does this profile look right before I install anything?")
    return "\n".join(lines) + "\n"


#: Result record for one installed file.
#: ``status`` is ``"installed"`` (file written), ``"skipped-exists"``
#: (skipped because the file already existed and ``force`` was not
#: set), or ``"dry-run"`` (would have been written under
#: ``--dry-run``).
InstallResult = tuple[Path, list[str], list[str], str]
# (target_path, unfilled_token_names, block_slot_names, status)


class ScaffoldSecurityError(Exception):
    """Raised when an install would write through a symlink or escape the
    target directory (Layer-4 executable hardening).  Fail-closed: the
    scaffold refuses the write rather than following the redirect."""


def _assert_safe_write(dst: Path, target: Path) -> None:
    """Refuse to write through a symlink or outside *target* (Layer 4).

    Runs before **every** write (fresh or ``--force``), not only
    overwrites: ``Path.exists()`` follows symlinks and returns ``False``
    for a *dangling* symlink, so a guard scoped to the ``--force`` path
    would let a fresh install write through a planted symlink at ``dst``
    -- or through a **symlinked parent directory** -- and escape
    ``target``.  Three fail-closed checks:

    1. ``dst`` itself must not be a symlink.
    2. No existing directory **between** ``target`` and ``dst`` may be a
       symlink (a symlinked parent redirects the write even when ``dst``
       is a normal name).
    3. The resolved final write path must stay within ``target`` (defense
       in depth against an ``..`` / absolute ``dst``).

    ``target`` is already ``resolve()``-d by the caller.  The containment
    check is 3.8-safe (``try: relative_to; except ValueError``) -- it does
    **not** use ``Path.is_relative_to`` (3.9+).
    """
    target_resolved = target.resolve()

    # (1) dst must not itself be a symlink.
    if dst.is_symlink():
        raise ScaffoldSecurityError(
            f"refusing to write through a symlinked destination: {dst}"
        )

    # (2) no existing ancestor strictly inside target may be a symlink.
    for ancestor in dst.parents:
        if ancestor == target_resolved:
            break  # reached target itself; don't police above it
        try:
            ancestor.relative_to(target_resolved)
        except ValueError:
            break  # ancestor is at/above target -- stop walking
        if ancestor.is_symlink():
            raise ScaffoldSecurityError(
                f"refusing to write through a symlinked parent: {ancestor}"
            )

    # (3) the resolved final path must stay within target.
    final = dst.parent.resolve() / dst.name
    try:
        final.relative_to(target_resolved)
    except ValueError:
        raise ScaffoldSecurityError(
            f"refusing to write outside the target directory: {final} "
            f"is not under {target_resolved}"
        )


def _install_one(
    src: Path,
    dst: Path,
    tokens: dict[str, str],
    target: Path,
    *,
    dry_run: bool,
    force: bool = False,
    verbatim: bool = False,
) -> InstallResult:
    """Copy *src* to *dst*.  Returns an InstallResult.

    Token-substituted by default.  When ``verbatim`` is True the file is
    copied **byte-for-byte** -- no ``{{token}}`` substitution, no
    unpaired-slot warning, and the result's unfilled-token / block-slot
    lists are **empty** (a script's f-string braces or docstring must
    not be scanned as template tokens / slots, else the post-scaffold
    report false-positives on code).  This is the I4 contract for the
    1:many script-install path.

    Default-safe: if *dst* already exists and *force* is False, the
    file is **not** overwritten and the result's status is
    ``"skipped-exists"``.  Re-running the scaffold against an
    already-installed repo therefore preserves filled block slots and
    other customizations; pass ``--force`` to opt into overwriting.
    """
    text = src.read_text(encoding="utf-8")

    if verbatim:
        # No substitution, no slot/token scan -- code is not a template.
        unfilled: list[str] = []
        slots: list[str] = []
    else:
        # Pre-substitution: warn about template-author errors (unpaired
        # cairn:slot markers) before the file ships.  These would
        # manifest as a malformed installed file otherwise; cheaper to
        # catch here.
        unpaired = find_unpaired_slots(text)
        if unpaired:
            print(
                f"  [warn] {src.name}: unpaired slot marker(s): "
                f"{', '.join(unpaired)} (each open `cairn:slot NAME` needs "
                f"a matching `cairn:end NAME`)",
                file=sys.stderr,
            )
        text = substitute_tokens(text, tokens)
        unfilled = find_unfilled_tokens(text)
        slots = find_block_slots(text)

    if dry_run:
        return dst, unfilled, slots, "dry-run"

    if dst.exists() and not force:
        print(
            f"  [skip] {dst}: already exists -- pass --force to overwrite "
            f"(re-running the scaffold without --force preserves any "
            f"customizations the file already carries)",
            file=sys.stderr,
        )
        return (dst, unfilled, slots, "skipped-exists")

    # Layer-4 hardening: refuse to write through a symlink or outside
    # target -- on every write, fresh or --force (fail-closed).
    _assert_safe_write(dst, target)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    return dst, unfilled, slots, "installed"


def install_core(
    templates_root: Path,
    target: Path,
    tokens: dict[str, str],
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[InstallResult]:
    """Copy core templates into *target*, substituting tokens."""
    results: list[InstallResult] = []
    for src_rel, dst_rel in _CORE_MAPPINGS:
        src = templates_root / src_rel
        if not src.exists():
            print(f"  [warn] core template missing: {src_rel}", file=sys.stderr)
            continue
        dst = target / dst_rel
        results.append(
            _install_one(src, dst, tokens, target, dry_run=dry_run, force=force)
        )
    return results


def install_optional(
    templates_root: Path,
    target: Path,
    tokens: dict[str, str],
    optional: list[tuple[str, str]],
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[InstallResult]:
    """Copy the dimension-selected optional templates into *target*.

    *optional* is the ``(src, dst)`` list from
    ``select_optional_templates``; source paths are relative to
    ``cairn/templates/`` (like ``_CORE_MAPPINGS``).
    """
    results: list[InstallResult] = []
    for src_rel, dst_rel in optional:
        src = templates_root / src_rel
        if not src.exists():
            print(
                f"  [warn] optional template missing: {src_rel}",
                file=sys.stderr,
            )
            continue
        dst = target / dst_rel
        results.append(
            _install_one(src, dst, tokens, target, dry_run=dry_run, force=force)
        )
    return results


def install_modules(
    templates_root: Path,
    target: Path,
    tokens: dict[str, str],
    module_names: list[str],
    *,
    dry_run: bool = False,
    force: bool = False,
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
        # 1:many -- a module installs its doctrine .md and (for the two
        # default-on discipline modules) its reference script verbatim.
        for spec in _MODULE_MAPPINGS[name]:
            src = modules_root / spec.src
            if not src.exists():
                print(
                    f"  [warn] module template missing: {spec.src}",
                    file=sys.stderr,
                )
                continue
            dst = target / spec.dst
            results.append(
                _install_one(
                    src, dst, tokens, target,
                    dry_run=dry_run, force=force, verbatim=spec.verbatim,
                )
            )
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

    written = [r for r in installed if r[3] == "installed"]
    skipped = [r for r in installed if r[3] == "skipped-exists"]
    dry = [r for r in installed if r[3] == "dry-run"]

    if dry:
        print(f"\n[dry-run] Files that would be installed ({len(dry)}):")
        for dst, _u, _s, _st in dry:
            print(f"  {dst.relative_to(target)}")
    else:
        print(f"\nFiles installed ({len(written)}):")
        for dst, _u, _s, _st in written:
            print(f"  {dst.relative_to(target)}")
        if skipped:
            print(
                f"\nFiles skipped -- already exist, --force not set "
                f"({len(skipped)}):"
            )
            for dst, _u, _s, _st in skipped:
                print(f"  {dst.relative_to(target)}")
            print(
                "  -> These files already exist in the target.  The scaffold "
                "preserved their contents by default to protect filled\n"
                "     block slots and other customizations.  Pass --force to "
                "overwrite (back up first if you have customizations\n"
                "     you want to keep)."
            )

    # Unfilled inline tokens (only count files we actually wrote or
    # would write; skipped files keep their on-disk content untouched)
    accounted = written or dry
    all_unfilled = sorted(
        {tok for _d, unfilled, _s, _st in accounted for tok in unfilled}
    )
    if all_unfilled:
        print(f"\n[WARN] {len(all_unfilled)} unfilled token(s) remain:")
        for tok in all_unfilled:
            print(f"  {{{{ {tok} }}}}")
        print("  -> Add these to the profile config and re-run, or fill manually.")
    elif accounted:
        print("\n[OK] All inline tokens substituted.")

    # Block slots needing agent attention (only for written/dry files)
    all_slots = [
        (dst.relative_to(target), slot)
        for dst, _u, slots, _st in accounted
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

def install_manifest(
    modules: list[str] | None = None,
) -> list[tuple[str, str, bool]]:
    """The ``(source, destination, verbatim)`` set the scaffold installs.

    Core templates always; modules per *modules* (or **all** known
    modules when ``None`` -- the published catalog).  ``source`` is
    relative to ``templates/``; ``destination`` is relative to the
    target repo root.  Derived from ``_CORE_MAPPINGS`` +
    ``_MODULE_MAPPINGS`` so the published manifest (Layer 1) cannot
    drift from what the scaffold actually writes.  Sorted by
    destination for a stable, diffable emission.
    """
    entries: list[tuple[str, str, bool]] = [
        (src_rel, dst_rel, False) for src_rel, dst_rel in _CORE_MAPPINGS
    ]
    names = sorted(_MODULE_MAPPINGS) if modules is None else modules
    for name in names:
        for spec in _MODULE_MAPPINGS.get(name, []):
            entries.append((f"modules/{spec.src}", spec.dst, spec.verbatim))
    entries.sort(key=lambda e: (e[1], e[0]))
    return entries


def format_manifest(modules: list[str] | None = None) -> str:
    """Render the install manifest as a stable, machine-readable table:
    one ``destination<TAB>source<TAB>{verbatim|substituted}`` line per
    file (Layer 1; ``scaffold.py --manifest``)."""
    lines = [
        "# Cairn install manifest "
        "(destination<TAB>source<TAB>verbatim|substituted)",
    ]
    for src, dst, verbatim in install_manifest(modules):
        kind = "verbatim" if verbatim else "substituted"
        lines.append(f"{dst}\t{src}\t{kind}")
    return "\n".join(lines) + "\n"


def git_provenance_warning(cairn_root: Path) -> str | None:
    """Layer-1 provenance nudge: return a warning when *cairn_root* is a
    git checkout whose ``HEAD`` is **not a tagged release commit** or has
    **uncommitted changes**; return ``None`` when it is a clean tagged
    release, or when git is unavailable / the path is not a checkout
    (degrade silently -- the warning never blocks an install).

    Read-only, fixed-argument ``git`` via ``subprocess`` (no shell, no
    input interpolation).  ``git`` is local VCS, not a network call, so
    SAFETY Rule 5 (the bootstrap does not read from the internet) is
    untouched.
    """
    import subprocess

    def _git(*args: str) -> subprocess.CompletedProcess[str] | None:
        try:
            return subprocess.run(
                ["git", "-C", str(cairn_root), *args],
                capture_output=True, text=True, timeout=10, check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return None

    inside = _git("rev-parse", "--is-inside-work-tree")
    if inside is None or inside.returncode != 0 \
            or inside.stdout.strip() != "true":
        return None  # not a checkout / git absent -- silent

    issues: list[str] = []
    tagged = _git("describe", "--exact-match", "--tags", "HEAD")
    if tagged is None or tagged.returncode != 0:
        issues.append("its HEAD is not a tagged release commit")
    dirty = _git("status", "--porcelain")
    if dirty is not None and dirty.stdout.strip():
        issues.append("its source tree has uncommitted changes")
    if not issues:
        return None
    return (
        f"provenance: scaffolding from a Cairn source where "
        f"{' and '.join(issues)} ({cairn_root}). Prefer a tagged release "
        f"(see bootstrap/PROVENANCE.md); pass --allow-dev to silence."
    )


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
        else _find_cairn_root(Path(__file__))
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

    # Install module templates
    print(f"Installing modules: {', '.join(modules) or '(none)'} ...")
    module_results = install_modules(
        templates_root, target, tokens, modules, force=args.force
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
        core_results + module_results + optional_results,
    )

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
            "\nTo enable post-commit auto-release of work intents (opt-in;\n"
            "the scaffold does NOT install git hooks for you), run:\n"
            "  python tools/intent.py install-hook"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
