"""Scaffold engine -- configuration / tokens / profile resolution (scaffold-split Stage 4).

The static install schema and configuration-resolution surface: the YAML config
loader (with the no-PyYAML minimal fallback), the inline-token vocabulary, the
template/skills/module mapping registries (including the trust anchor
``_MODULE_MAPPINGS`` the release-security scanner reads), and the governance
preset / six-axis resolution that derives a module roster + profile summary.

A **pure stdlib leaf**: it imports only the standard library and holds no
adopter-tree writes (the dev-tree / gitignore / fan-out writers stay in the
engine; they consume this module's data). **This module** owns no file writes and
no CLI/upgrade execution; importing it defines names only (import-purity, SR2).
Note this is an *ownership* property, not a runtime-loading boundary: importing
``bootstrap._scaffold.config`` runs the eager package facade
(``bootstrap._scaffold.__init__``) first, which loads the whole engine
(install / upgrade / cli included) -- see the ``test_trust_anchor_imports_are_
owner_specific_not_runtime_isolated`` regression. install / upgrade depend on it,
never the reverse.

Pure motion from the pre-split monolith (Stage 4): the symbols are unchanged;
only their home moved. ``_MODULE_MAPPINGS`` migrates here as its owning module
(plan 0B.3); ``bootstrap/security_check.py`` imports the trust anchor from this
narrow owner. Loaded via the engine's verifying finder, so this file's real path
is confirmed within the Cairn root before it executes.
"""
from __future__ import annotations

import re
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
        # The repo-relative Python package a python-security adopter scans
        # (security-apparatus-enrichment Chunk B0 / C; RV2).  A *required*
        # token for that module -- see ``_MODULE_REQUIRED_TOKENS`` and the
        # selected-module required-token preflight that fails closed before
        # any write when a selected module's required token is unfilled.
        "python_package",
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
    "fold-back-ledger",
    "incident-trackers",
    "documentation-plan",
)


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
    # Self-instrumentation home (measurement-folder standard): a core dir
    # carried by its README, which states the membership rule.  Same shape as
    # proposals/ + plans/ (a core dir installed via its content file).
    ("core/dev/measurement/README.md",              "dev/measurement/README.md"),
    # External-dependency upstream channel (core-dev-folder-set proposal):
    # draft issue reports for external OSS deps, distinct from the
    # methodology fold-back ledger (dev/.cairn/cairn_foldback.md).
    # archive/.gitkeep is verbatim (an empty placeholder, not a template).
    ("core/dev/upstream/README.md",                 "dev/upstream/README.md"),
    ("core/dev/upstream/_template.md",              "dev/upstream/_template.md"),
    ("core/dev/upstream/archive/.gitkeep",          "dev/upstream/archive/.gitkeep"),
    # Project-owned agent-discipline detail folder: the folder + README
    # ship from Cairn; the rule files inside are entirely the adopter's own
    # (Cairn never templates them).  Empty at adoption by design.
    ("core/dev/rules/README.md",                    "dev/rules/README.md"),
    # Stage-0 strategy space: the README (lifecycle + status vocabulary)
    # and the note template.  Shipped default-on; the strategy/ dir and
    # archive/ placeholder are created by create_dev_tree (see install.py).
    ("core/dev/strategy/README.md",                 "dev/strategy/README.md"),
    ("core/dev/strategy/_template.md",              "dev/strategy/_template.md"),
)

#: Lifecycle-routine skills install **unconditionally, like core/** -- the
#: session routines are invariant kernel (every adoption runs them), so they
#: are not a conditional ``templates/modules/*`` module.  ``(src relative to
#: templates/, dst relative to the repo root, verbatim)``.  The CLI is a script
#: -> ``verbatim`` (byte-for-byte, hash-only upgrade policy); the ``SKILL.md``
#: sources are markdown -> substituted (so they get a base-template cache entry
#: and a token-/slot-aware 3-way merge on upgrade, exactly like ``core/`` docs).
_SKILLS_MAPPINGS: tuple[tuple[str, str, bool], ...] = (
    ("skills/_lib/lifecycle.py",         "tools/lifecycle.py",                       True),
    ("skills/_lib/lifecycle_planner.py", "tools/lifecycle_planner.py",               True),
    ("skills/_data/vendor_targets.yml",  ".agents/skills/_data/vendor_targets.yml",  True),
    ("skills/session-start/SKILL.md",   ".agents/skills/session-start/SKILL.md",    False),
    ("skills/session-end/SKILL.md",     ".agents/skills/session-end/SKILL.md",      False),
)

#: Machine-local lifecycle state the skills write into ``dev/.cairn/`` -- the
#: untracked interpreter binding (resolve-don't-bake, Decision 6) and the
#: full-handoff lock.  Seeded into ``.gitignore`` unconditionally (the skills
#: always install).  ``dev/.cairn/base/`` itself stays tracked (the lockfile
#: base cache); only these machine-state members are ignored.
_SKILLS_GITIGNORE: tuple[str, ...] = (
    "dev/.cairn/local-env.json",
    "dev/.cairn/handoff.lock",
)

#: Common filenames an adopter renames the thin vendor wrapper
#: (``core/VENDOR.md``) to -- their AI tool's instruction file.  Used by
#: ``--init-lock`` to follow that rename so the wrapper stays tracked + 3-way
#: merges on later upgrades (foldback #45).  Distinctly vendor-specific names
#: only (``AGENTS.md`` is the shared file, deliberately excluded).
_KNOWN_VENDOR_WRAPPERS: tuple[str, ...] = (
    "CLAUDE.md", "GEMINI.md", "CODEX.md", "CURSOR.md", "COPILOT.md", "QWEN.md",
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


#: Always-on **executable** helper deliveries -- the progressive-onboarding
#: launcher + its private ``_onboarding/`` engine package.  Historically
#: ``install_onboarding`` fanned these out UNCONDITIONALLY but OUTSIDE the
#: manifest / lockfile (a side door): ``write_install_lockfile`` never recorded
#: them, so ``upgrade`` could not enumerate / refresh / attest them, and
#: ``security_check.scan_targets()`` (which derives shipped-code coverage from
#: ``_MODULE_MAPPINGS`` only) never release-scanned them.  Promoted here as
#: first-class always-on ``InstallSpec``s so the **same** declaration is consumed
#: by all three authorities: ``install_onboarding`` (delivery),
#: ``install_manifest`` / ``write_install_lockfile`` (tracking + attestation),
#: and ``scan_targets()`` (release Bandit).  ``src`` is relative to
#: ``templates/modules/`` (the ``_MODULE_MAPPINGS`` convention), so every consumer
#: reuses the same ``modules/{src}`` join.  ``verbatim=True`` -- byte-for-byte
#: executables on the hash-only upgrade policy.
#:
#: The launcher + the eight engine members are a **required completeness group**
#: (``install.assert_always_on_complete`` / the new-core advancement guard): a
#: partial group -- a present launcher with a missing/absent engine member --
#: fails closed BEFORE any facade/engine write or lock advancement, never
#: advancing a facade over an absent engine.  These are **always-on** structural
#: helpers (onboarding installs unconditionally); this is NOT an opt-in
#: ``_MODULE_MAPPINGS`` module, and the opt-in boundary is untouched.
_ALWAYS_ON_MAPPINGS: tuple[InstallSpec, ...] = (
    InstallSpec("default-on/onboarding_activate.py",
                "scripts/onboarding_activate.py", True),
    InstallSpec("default-on/_onboarding/__init__.py",
                "scripts/_onboarding/__init__.py", True),
    InstallSpec("default-on/_onboarding/activation.py",
                "scripts/_onboarding/activation.py", True),
    InstallSpec("default-on/_onboarding/cli.py",
                "scripts/_onboarding/cli.py", True),
    InstallSpec("default-on/_onboarding/prompts.py",
                "scripts/_onboarding/prompts.py", True),
    InstallSpec("default-on/_onboarding/security.py",
                "scripts/_onboarding/security.py", True),
    InstallSpec("default-on/_onboarding/shared.py",
                "scripts/_onboarding/shared.py", True),
    InstallSpec("default-on/_onboarding/slotparse.py",
                "scripts/_onboarding/slotparse.py", True),
    InstallSpec("default-on/_onboarding/triggers.py",
                "scripts/_onboarding/triggers.py", True),
)


def duplicate_destinations(
    entries: list[tuple[str, str]],
) -> dict[str, list[str]]:
    """Map each destination claimed by **more than one** owner to its owner
    labels; empty dict means every destination is uniquely owned.

    The shared destination-ownership preflight (External-Security review P1#2): a
    duplicate destination means one ``InstallSpec`` silently shadows another on a
    ``--force`` install, or the published manifest emits two rows for one path.
    Each entry is ``(owner_label, dst)``.  Pure leaf logic; the callers choose the
    failure (``install_onboarding`` / ``assert_always_on_complete`` and the
    upgrade planner fail closed before any write; ``install_manifest`` refuses)."""
    owners: dict[str, list[str]] = {}
    for label, dst in entries:
        owners.setdefault(dst, []).append(label)
    return {dst: who for dst, who in owners.items() if len(who) > 1}


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
        # lifecycle-metrics fold-up (phase C, 2026-06): lifecycle_metrics.py is
        # now a thin launcher/facade over an owned `_lifecycle_metrics/` engine
        # package; the nine package files install verbatim beside the facade so
        # `python tools/lifecycle_metrics.py` resolves its sibling engine at
        # runtime (parity with the _intent/ + _onboarding/ splits).  Byte-for-byte code.
        InstallSpec("default-on/_lifecycle_metrics/__init__.py",
                    "tools/_lifecycle_metrics/__init__.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/config.py",
                    "tools/_lifecycle_metrics/config.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/parse.py",
                    "tools/_lifecycle_metrics/parse.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/gitmeta.py",
                    "tools/_lifecycle_metrics/gitmeta.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/report.py",
                    "tools/_lifecycle_metrics/report.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/subsystems.py",
                    "tools/_lifecycle_metrics/subsystems.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/extract.py",
                    "tools/_lifecycle_metrics/extract.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/snapshot.py",
                    "tools/_lifecycle_metrics/snapshot.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/cli.py",
                    "tools/_lifecycle_metrics/cli.py", verbatim=True),
    ],
    "reflections": [
        InstallSpec("default-on/reflections.md", "dev/modules/reflections.md"),
        # A tracked directory guide so dev/reflections/ materializes on a
        # fresh scaffold (the reflection entries themselves stay untracked
        # via the .gitignore seed below) -- fold-back #42.
        InstallSpec("default-on/reflections-README.md",
                    "dev/reflections/README.md", verbatim=True),
        # Fold 2 (foldback-drain-tooling): explicit prune tool the reflections
        # module doctrine prescribes.  Complements the simpler date-cutoff prune
        # inside tools/lifecycle.py session-end (which runs at full-handoff);
        # this standalone script allows independent invocation and offers a
        # keep-by-distinct-date window rather than a wall-clock cutoff.
        InstallSpec("default-on/prune_reflections.py",
                    "tools/prune_reflections.py", verbatim=True),
    ],
    "claim-check": [
        InstallSpec("default-on/claim-check.md",
                    "dev/modules/claim-check.md"),
        InstallSpec("default-on/claim_check.py",
                    "scripts/claim_check.py", verbatim=True),
        # Fold 1 (foldback-drain-tooling): stem-resolution checker.
        # Complements claim_check.py (repo-path/line-bounds) and link_check.py
        # (markdown links) -- verifies that every backticked date-prefixed stem
        # in PLANNING.md / NEXT_SESSION.md resolves to one proposal or plan.
        # Default-on with the claim-check module family because both are
        # lifecycle-hygiene checkers.
        InstallSpec("default-on/verify_stems.py",
                    "scripts/verify_stems.py", verbatim=True),
    ],
    # The deployment-side measurement substrate the adaptive-doctrine
    # rate-limit gate (doctrine/rationale.md) evaluates against.
    # Ships the module doctrine + a forkable tracker template; adopters
    # fork the template to one or many live trackers (e.g.,
    # dev/incident_log.md or class-specific files), then the goodnight
    # migration sub-step feeds incident entries from reflections into
    # the trackers.  The canonical 7-column semantic-field schema is
    # the contract the eventual Goal 7 cross-adopter harvest reads.
    "incident-trackers": [
        InstallSpec("default-on/incident-trackers.md",
                    "dev/modules/incident-trackers.md"),
        InstallSpec("default-on/incident_log_template.md",
                    "dev/modules/incident_log_template.md"),
        # The deterministic, zero-token rate-limit-gate evaluator +
        # fold-up-backlog checker (self-evolution-loop Part B). Reads the
        # trackers + the fold-back ledger and emits suggestions only.
        InstallSpec("default-on/evolution_infer.py",
                    "tools/evolution_infer.py", verbatim=True),
    ],
    # The placement-decision procedure for documentation and doctrine.
    # Default-on: every adopter benefits from a four-layer routing
    # discipline (entry / governing / deliberation / descriptive).
    # Ships the module doctrine + a forkable DOCUMENTATION_PLAN.md the
    # adopter customizes for their own file inventory + tier vocabulary.
    # Three slot anchors land via the core templates --
    # `documentation-discipline` in AGENTS.md plus
    # `documentation-tier-home` in proposals + plans `_template.md` --
    # and are filled by **manual paste** from the module's
    # `Merged into:` Blocks 1/2/3 (the adopter copies the block matching
    # each target slot at install time, parallel to the existing
    # claim-check / lifecycle-metrics / reflections module pattern).
    # Mechanical merge via Proposal B's `cairn:merge-target` directives
    # is *deferred* pending the merge-pass / install-lockfile interaction
    # fix (the merge pass mutates files post-install, which the
    # lockfile's clean-install divergence guard rejects); see
    # `dev/PLANNING.md` (modflow_tools-side) > "Cairn-side merge-helper
    # / install-lockfile interaction fix".  The forkable's worked
    # examples are adopter-relative; Cairn's own self-hosted instance at
    # cairn/docs/DOCUMENTATION_PLAN.md uses cairn-prefixed paths and is
    # the methodology source-of-truth.
    "documentation-plan": [
        InstallSpec("default-on/documentation-plan.md",
                    "dev/modules/documentation-plan.md"),
        InstallSpec("default-on/documentation_plan_template.md",
                    "docs/DOCUMENTATION_PLAN.md"),
    ],
    # The deployment-side fold-back channel (doctrine: doctrine/fold-back.md).
    # Default-on but omittable: ships the module doctrine + the forkable
    # ledger artifact into dev/.cairn/, the active-surfacing prompt asset
    # into dev/modules/, the export-scrub scanner doc into dev/modules/, and
    # the scanner itself verbatim into scripts/.  The ledger is a cross-repo
    # export surface, so its template carries a [SECURITY WARNING] header;
    # the scanner is the machine half of the active-surfacing protocol's
    # two-gate export boundary (the manual half is the maintainer-signed
    # affirmation field in the Cairn issue / PR template).
    "fold-back-ledger": [
        InstallSpec("default-on/fold-back-ledger.md",
                    "dev/modules/fold-back-ledger.md"),
        InstallSpec("default-on/fold-back-ledger-template.md",
                    "dev/.cairn/cairn_foldback.md"),
        # Active-surfacing additions (Chunks 4-6 of
        # 2026-05-28-claude-cairn-foldback-active-surfacing).
        InstallSpec("default-on/foldback_export_scan.md",
                    "dev/modules/foldback_export_scan.md"),
        InstallSpec("default-on/foldback_export_scan.py",
                    "scripts/foldback_export_scan.py", verbatim=True),
        InstallSpec("default-on/fold-back-active-prompt.md",
                    "dev/modules/fold-back-active-prompt.md"),
        # Optional helper (Chunk 8): lists open `candidate`-status
        # rows from the ledger eligible for active surfacing.  Ships
        # verbatim into adopter scripts/; invocation in the agent
        # prompt is `python scripts/foldback_suggest.py [--ledger
        # <path>] [--all]`.
        InstallSpec("default-on/foldback_suggest.py",
                    "scripts/foldback_suggest.py", verbatim=True),
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
        # intent-split (phase A, 2026-06): intent.py is now a thin launcher/facade
        # over an owned `_intent/` engine package; the seven package files install
        # verbatim beside the facade so `python tools/intent.py` (the CLI + the git
        # hooks) resolves its sibling engine at runtime.  Each is byte-for-byte code.
        InstallSpec("team-gated/_intent/__init__.py",
                    "tools/_intent/__init__.py", verbatim=True),
        InstallSpec("team-gated/_intent/shared.py",
                    "tools/_intent/shared.py", verbatim=True),
        InstallSpec("team-gated/_intent/record_io.py",
                    "tools/_intent/record_io.py", verbatim=True),
        InstallSpec("team-gated/_intent/identity.py",
                    "tools/_intent/identity.py", verbatim=True),
        InstallSpec("team-gated/_intent/conflict.py",
                    "tools/_intent/conflict.py", verbatim=True),
        InstallSpec("team-gated/_intent/hooks.py",
                    "tools/_intent/hooks.py", verbatim=True),
        InstallSpec("team-gated/_intent/cli.py",
                    "tools/_intent/cli.py", verbatim=True),
        # Fold 2 (foldback-drain-tooling): the prune-intents goodnight compaction
        # tool.  Ships with coordination-tiers because the goodnight intent-hygiene
        # extension (coordination-tiers module doc) prescribes the prune-intents step.
        # Self-contained (no import from tools.intent); reads dev/intents.jsonl directly.
        InstallSpec("team-gated/prune_intents.py",
                    "tools/prune_intents.py", verbatim=True),
    ],
    "security-review": [
        InstallSpec("team-gated/security-review.md",
                    "dev/modules/security-review.md"),
    ],
    "issue-capture": [
        InstallSpec("team-gated/issue-capture.md",
                    "dev/modules/issue-capture.md"),
        # Fold 3 (foldback-drain-tooling): label-bootstrap helpers, one per
        # forge (GitLab + GitHub).  Generalise the per-adopter scripts into a
        # single Cairn-generic tool shipped with the module that prescribes
        # label-axis doctrine.  The additive-only flag absorbs the LHM
        # divergence (legacy-label note); no project-specific references.
        # Auth R2: both scripts emit a clear "set GITLAB_PRIVATE_TOKEN /
        # GITHUB_TOKEN" error when no credential is found.
        InstallSpec(
            "team-gated/issue-capture/bootstrap_gitlab_labels.py",
            "scripts/bootstrap_gitlab_labels.py",
            verbatim=True,
        ),
        InstallSpec(
            "team-gated/issue-capture/bootstrap_github_labels.py",
            "scripts/bootstrap_github_labels.py",
            verbatim=True,
        ),
    ],
    "model-selection": [
        InstallSpec("team-gated/model-selection.md",
                    "dev/modules/model-selection.md"),
        # Fold 5 (foldback-drain-tooling): stub mapping file + fidelity checker.
        # The stub is seeded carrying a "FILL ME" placeholder, so the gate is
        # **red on a fresh, unfilled mapping** -- forcing the adopter to record
        # their real tier->model assignments (the silent-empty install is the
        # failure this module prevents; the install itself is never blocked).
        # An *interactive* install captures the bindings up front so the gate
        # ships green (foldback #2: capture_model_selection_mapping); a
        # non-interactive / CI install leaves the FILL ME stub as the fallback.
        # The checker is installed verbatim so adopters can invoke it directly
        # (`python scripts/check_model_selection.py`) or wire it into their CI.
        InstallSpec(
            "team-gated/model_selection_mapping_stub.yml",
            "dev/.cairn/model-selection-mapping.yml",
        ),
        InstallSpec(
            "team-gated/check_model_selection.py",
            "scripts/check_model_selection.py",
            verbatim=True,
        ),
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
    # Cairn v0.2 security-hardening (R9): the content-integrity scanner,
    # shipped to adopters so their agents can scan working-tree files /
    # incoming PRs for prompt-injection patterns before ingesting them. The
    # verbatim script is single-sourced here (Cairn's own check_cairn composes
    # the same file), the 1:many claim-check pattern.
    "content-security": [
        InstallSpec("team-gated/content-security.md",
                    "dev/modules/content-security.md"),
        InstallSpec("team-gated/content_scan.py",
                    "scripts/content_scan.py", verbatim=True),
        # Security-apparatus-enrichment Chunk B: the decomposed stdlib-only
        # advisory runner + its policy inputs (audited-roots manifest,
        # reviewed-residual baseline, URL allowlist).  All verbatim -- code +
        # policy data, not token-substituted templates.  The runner resolves
        # its policy siblings from its own scripts/ directory.
        InstallSpec("team-gated/content_scan_runner.py",
                    "scripts/content_scan_runner.py", verbatim=True),
        InstallSpec("team-gated/content_scan_roots.txt",
                    "scripts/content_scan_roots.txt", verbatim=True),
        InstallSpec("team-gated/content_scan_residuals.txt",
                    "scripts/content_scan_residuals.txt", verbatim=True),
        InstallSpec("team-gated/content_scan_allowlist.txt",
                    "scripts/content_scan_allowlist.txt", verbatim=True),
    ],
    # The Python security gate stack (security-apparatus-enrichment, RV1
    # surface 3).  Team-gated + opt-in -- never default-on, and never
    # installed for a non-Python adopter.  v1 self-audit scope only (a
    # drift / content-injection tripwire on the adopter's *own trusted
    # tree*), explicitly NOT a reviewer for untrusted PRs that can modify
    # the apparatus itself.  Chunk B0 lands the module doctrine stub + its
    # required-token registration (``python_package``, below); Chunk C adds
    # the orchestrator (``run_security_audit.py``), the templated bandit
    # gate, and the adopted-executable source gate.  ``python_package`` has
    # no safe default, so it is a required token (the selected-module
    # required-token preflight refuses a fresh install / adopt / upgrade
    # that selects this module without a filled value -- fail closed before
    # any write).
    "python-security": [
        InstallSpec("team-gated/python-security.md",
                    "dev/modules/python-security.md"),
        # The standalone orchestrator (Chunk C): SR-1 integrity preflight +
        # content-scan (when content-security installed) + bandit over
        # {{python_package}} + the adopted-executable source gate + pip-audit
        # (egress opt-in).  Verbatim -- code, no token substitution; it reads
        # python_package + the installed roster from the lockfile at runtime.
        InstallSpec("team-gated/run_security_audit.py",
                    "scripts/run_security_audit.py", verbatim=True),
    ],
    # Architecture-review (modflow_tools doctrine-parity fold, 2026-06-01):
    # a triggered remediation / on-ramp module for an adopter whose
    # architecture accreted rather than was deliberately designed.  Ships
    # the module doctrine + a forkable rubric frame the adopter fills
    # (the incident-trackers / documentation-plan 2-spec pattern, both
    # substituted not verbatim).  Team-gated, opt-in -- not in any
    # default-on set or governance preset.
    "architecture-review": [
        InstallSpec("team-gated/architecture-review.md",
                    "dev/modules/architecture-review.md"),
        InstallSpec("team-gated/architecture_review_template.md",
                    "dev/architecture_review.md"),
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
    # Foldback active-surfacing (2026-05-28 arc): the protocol's Scrub
    # step writes the drafted issue / PR body to a gitignored temp
    # file pattern under `dev/.cairn/` before invoking the scanner.
    # The draft file is intentionally never committed -- the durable
    # record is the filed Cairn issue / PR + the ledger row's
    # status transition.  Seeded by default so an adopter does not
    # have to remember the pattern themselves.
    "fold-back-ledger": ("dev/.cairn/.foldback-draft-*.md",),
    # Reflections are per-agent + ephemeral (gitignored); only the tracked
    # README.md guide survives, so the dir materializes on a fresh scaffold
    # without committing reflection content (fold-back #42).  Order matters:
    # ignore-all then un-ignore the README.
    "reflections": ("dev/reflections/*", "!dev/reflections/README.md"),
}


#: Module → repo-relative **pre-module local surfaces** the module supersedes.
#: When an adopter adopts a module that now owns a concern, an older local doc /
#: config the adopter wrote *before* the module existed is left in place by the
#: install (the install writes only the module's own files).  The adopter is
#: then left with two canonical-looking sources per concern and must notice +
#: reconcile by hand -- the silent post-sync drift this flag turns into an
#: advisory (foldback rollup #1).  Listed names are Cairn's own pre-module
#: conventions (the most likely predecessor forms); the flag is **advisory** --
#: it never deletes or edits the local form, the adopter reconciles or retires.
_MODULE_SUPERSEDES: dict[str, tuple[str, ...]] = {
    "security-review": ("dev/security_review_protocols.md",),
    "model-selection": ("dev/model_tier_mapping.md",),
    "architecture-review": ("dev/architecture_review.md",),
}


def superseded_local_surfaces(module_name: str, target_root: Path) -> list[str]:
    """Repo-relative pre-module local surfaces *module_name* supersedes that
    actually exist under *target_root* -- the set worth flagging for the adopter
    to reconcile or retire.  Empty when the module declares no supersession or
    none of the declared surfaces are present (no false note)."""
    return [
        rel
        for rel in _MODULE_SUPERSEDES.get(module_name, ())
        if (target_root / rel).exists()
    ]


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
# Selected-module required-token preflight (security-apparatus-enrichment B0)
# ---------------------------------------------------------------------------
#
# A few modules carry inline tokens that have **no safe default** -- the
# scaffold cannot render the module's files without a real adopter-supplied
# value.  ``python-security`` is the first: its gate scans the adopter's own
# ``{{python_package}}`` directory, so an unfilled token would install a
# partially-rendered, lockfile-recorded security stack still containing the
# literal ``{{python_package}}`` (Codex External plan review, P1 #1).
#
# Adding such a token to ``KNOWN_TOKENS`` is **not** enough: the scaffold
# installs rendered files first and only *warns* about leftover inline tokens
# afterward.  So selecting a module whose required token is unfilled must
# **fail closed before any target-tree or lockfile write**.  The map below
# declares, per module, the tokens that must resolve to a real value; the
# install / adopt-module / upgrade paths run :func:`missing_required_tokens`
# as a pre-write gate (see ``cli.main`` and ``upgrade``).  This is generic --
# any future module declares its required tokens here and inherits the gate.
_MODULE_REQUIRED_TOKENS: dict[str, tuple[str, ...]] = {
    # python-security's bandit/source gate scans {{python_package}} (RV2);
    # there is no safe default for an adopter's own package directory.
    "python-security": ("python_package",),
}

#: An inline token whose *value* is still an unfilled ``{{placeholder}}`` --
#: a token resolved to another token is as unfilled as an absent one.
_UNFILLED_TOKEN_VALUE = re.compile(r"\{\{\s*[\w.-]+\s*\}\}")


def missing_required_tokens(
    modules: list[str], tokens: dict[str, str],
) -> list[tuple[str, str]]:
    """Return ``(module, token)`` pairs for every required token of every
    *selected* module that is **not** filled with a real value.

    A required token counts as unfilled when it is absent from *tokens*, is
    empty / whitespace-only, or still carries a ``{{placeholder}}`` value.
    The caller turns a non-empty result into a fail-closed refusal **before
    any write** (no target-tree files, no lockfile / module-state mutation).
    This function is pure: it reads no filesystem and mutates nothing, so it
    is safe to call from every install path's pre-write gate.

    The check is deliberately generic -- token *presence + fill*, not
    module-specific *value validity* (e.g. python-security's containment +
    is-a-directory checks on ``python_package`` live in that module's own
    gate, Chunk C).  B0 only guarantees a required token reaches the renderer
    with a real value; the module validates what that value means.
    """
    missing: list[tuple[str, str]] = []
    for module in modules:
        for token in _MODULE_REQUIRED_TOKENS.get(module, ()):
            value = tokens.get(token)
            if (
                value is None
                or not str(value).strip()
                or _UNFILLED_TOKEN_VALUE.fullmatch(str(value).strip())
            ):
                missing.append((module, token))
    return missing


# ---------------------------------------------------------------------------
# Governance presets (Cairn v0.2 P4)
# ---------------------------------------------------------------------------
#
# Presets are *named points in the six-axis dimension model*, not a parallel
# config system.  An adopter picks a preset (the fast path) instead of
# hand-deriving the module roster; the six-axis scoring + the BOOTSTRAP.md
# I-5 gate table remain the principled backing (the gate table is the
# canonical per-module rationale).  See BOOTSTRAP.md Act I and the
# the source ``cairn-v0.2-p4-governance-presets`` plan.

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

#: Per-module team-staffing gate: the ``agent_team`` axis values that staff
#: each module.  These are the ONLY part of the I-5 gate evaluated as runtime
#: code; the non-axis gate conditions (trust boundary, issue tracker, domain
#: partitioning, legacy readiness) are baked into each preset's authored
#: baseline below (the "gate-table encoding" split from the P4 plan).
#:
#: The two modules gate **differently** (fold-back #40): ``coordination-tiers``
#: serves any *concurrent* team -- multiple same-type agents collide on shared
#: files exactly as a multi-type team does, and the work-intent mechanism is
#: what prevents it -- so it staffs both ``concurrent-multi-type`` and
#: ``concurrent-single-type``.  ``dual-review`` needs a second agent *type* to
#: fill its External tier with structural independence, which a same-type team
#: lacks, so it stays ``concurrent-multi-type`` only.
_TEAM_STAFFING_GATES: dict[str, frozenset[str]] = {
    "dual-review": frozenset({"concurrent-multi-type"}),
    "coordination-tiers": frozenset(
        {"concurrent-multi-type", "concurrent-single-type"}
    ),
}

#: All team-staffing-gated module names (membership tests; staffability is
#: per-module via :func:`_can_staff_module`).
_TEAM_STAFFING_GATED: tuple[str, ...] = tuple(_TEAM_STAFFING_GATES)


def _can_staff_module(name: str, axes: dict[str, str]) -> bool:
    """True when the resolved agent-team axis staffs the given team-staffing
    module, per the per-module gate (fold-back #40)."""
    return axes.get("agent_team", "") in _TEAM_STAFFING_GATES.get(
        name, frozenset()
    )


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
    where a list is expected is a friendly hard error."""
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


#: Matches a ``cairn:if`` open-marker or a ``cairn:endif`` close-marker.
#: Group 1 = AXIS, Group 2 = comma-separated value list (open-marker only).
_IF_RE = re.compile(
    r"^[ \t]*<!--\s+cairn:(?:"
    r"if\s+(\w+)\s+in\s+([^\-].*?)(?:\s*-->)"
    r"|"
    r"endif"
    r"\s*-->"
    r")\s*$",
    re.MULTILINE,
)


def strip_conditional_regions(text: str, axes: dict[str, object]) -> str:
    """Remove or keep ``<!-- cairn:if AXIS in val1,val2 --> ... <!-- cairn:endif -->``
    regions according to the resolved dimension profile.

    **Five load-bearing semantics** (implement exactly):

    1. **keep-on-match** — if ``str(axes.get(AXIS, ""))`` is in the
       directive's value set, remove only the two marker comment lines
       (and each marker's own trailing newline), leaving the inner content
       in place with no blank-line artifact.

    2. **remove-otherwise** — if AXIS is present in *axes* but its value is
       NOT in the directive's value set, remove the entire region (both
       markers AND the content between them, including the trailing newline
       of the closing marker), leaving no blank-line residue.

    3. **keep-on-missing-axis** — if AXIS is **absent** from *axes*,
       keep the inner content (conservative safety default: never silently
       drop a section because the profile was incomplete).  This is the
       OPPOSITE of ``select_optional_templates``, which omits on missing;
       stripping from an always-on file must default to keep.

    4. **raise-on-unbalanced** — an open ``cairn:if`` with no matching
       ``cairn:endif``, a stray ``cairn:endif``, or a nested ``cairn:if``
       (a second open before the first closes) → ``ValueError`` with a
       clear message.

    5. **identity** — text with no ``cairn:if`` directive is returned
       byte-identical (the common case; no global state, no side-effects).

    Pure function; deterministic: same ``(text, axes)`` → byte-identical
    output every call.
    """
    # Fast path: nothing to process (checks both markers so a stray
    # cairn:endif with no cairn:if still goes through the validator).
    if "cairn:if" not in text and "cairn:endif" not in text:
        return text

    # Walk lines, collecting regions using a simple state machine.
    # We re-scan with splitlines(keepends=True) so we can reconstruct
    # the output exactly.
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    # State: None = top-level, or dict with region info once inside a block.
    region: dict[str, object] | None = None

    for lineno, line in enumerate(lines, start=1):
        # Try to match either an open or close marker on this line.
        # The marker must occupy the whole line (anchored by MULTILINE ^ $).
        m = _IF_RE.match(line.rstrip("\n"))
        if m is None:
            if region is None:
                out.append(line)
            else:
                # Accumulate content inside an open region.
                region["body_lines"].append(line)  # type: ignore[union-attr]
            continue

        axis_grp = m.group(1)   # None for endif
        vals_grp = m.group(2)   # None for endif

        if axis_grp is not None:
            # Open marker.
            if region is not None:
                raise ValueError(
                    f"cairn:if directive at line {lineno} is nested inside "
                    f"another open cairn:if (axis={region['axis']!r}); "
                    "nesting is not supported."
                )
            values = frozenset(v.strip() for v in vals_grp.split(","))
            region = {
                "axis": axis_grp,
                "values": values,
                "open_lineno": lineno,
                "body_lines": [],
            }
        else:
            # Close marker (endif).
            if region is None:
                raise ValueError(
                    f"Stray cairn:endif at line {lineno} with no matching "
                    "cairn:if open."
                )
            axis = region["axis"]
            values = region["values"]  # type: ignore[assignment]
            body: list[str] = region["body_lines"]  # type: ignore[assignment]

            if axis not in axes:
                # Semantic 3: missing axis → keep content.
                out.extend(body)
            else:
                current_value = str(axes[axis])
                if current_value in values:
                    # Semantic 1: keep-on-match → keep body, strip both markers.
                    out.extend(body)
                else:
                    # Semantic 2: remove-otherwise → discard markers + body.
                    pass  # nothing appended; blank-line residue is avoided
                    # because we also don't append the close marker below.

            region = None  # region closed

    if region is not None:
        raise ValueError(
            f"Unclosed cairn:if at line {region['open_lineno']} "
            f"(axis={region['axis']!r}): no matching cairn:endif found."
        )

    return "".join(out)


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
    for mod in _TEAM_STAFFING_GATED:
        if _can_staff_module(mod, resolved_axes):
            baseline.add(mod)

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
        if name in _TEAM_STAFFING_GATED and not _can_staff_module(
            name, resolved_axes
        ):
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
