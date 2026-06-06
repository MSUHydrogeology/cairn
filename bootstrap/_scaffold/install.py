"""Scaffold engine -- fresh-install subsystem (scaffold-split Stage 6).

The install path: the dev/ tree creation, the core/skills/optional template
installs with token substitution + slot fan-out, the skills symlink/copy fan-out,
the onboarding seeding, the module installs + issue-capture reference, the install
report, the fidelity manifest, and the install-time lockfile writer. This is one
module (no sub-split, per plan).

A layer-6 subsystem: it depends downward on the leaves -- config (mapping
registries), security (the containment guards), slotmerge (token/slot helpers),
and lockfile (constants, emit, hashing, secret-token guard) -- and never upward on
upgrade / cli. The shared root helpers (``_cairn_root`` / ``_find_cairn_root``) and
the upgrade-time ``_MANIFEST_SEARCH_DIRS`` stay in the engine.

Pure motion from the pre-split monolith (Stage 6): the symbols are unchanged; only
their home moved (``run_module_merge_pass`` / ``write_install_lockfile`` /
``_lock_file_list`` / ``create_dev_tree`` / ``seed_gitignore`` land here as
foretold by Stages 2/4/5). Loaded via the engine's verifying finder, so this
file's real path is confirmed within the Cairn root before it executes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from .config import (
    _CORE_MAPPINGS,
    _MODULE_MAPPINGS,
    _SKILLS_GITIGNORE,
    _SKILLS_MAPPINGS,
    strip_conditional_regions,
)
from .security import (
    ScaffoldSecurityError,
    _assert_fanout_contained,
    _assert_safe_write,
)
from .slotmerge import (
    ModuleMergeResult,
    check_slot_fidelity,
    find_block_slots,
    find_unfilled_tokens,
    find_unpaired_slots,
    merge_module_into_slot,
    parse_module_merge_directives,
    substitute_tokens,
)
from .lockfile import (
    _BASE_CACHE_REL,
    _LIVING_STATE_DSTS,
    _LOCKFILE_REL,
    _LOCK_SCHEMA,
    _cairn_commit,
    _cairn_version,
    _emit_lock_yaml,
    _refuse_secret_tokens,
    _sha256_hex,
)


def run_module_merge_pass(
    templates_root: Path,
    target_root: Path,
    installed_modules: list[str],
    *,
    non_interactive: bool,
    dry_run: bool = False,
) -> tuple[list[ModuleMergeResult], list[tuple[str, str, str]]]:
    """Walk all installed modules + perform the merge pass + the
    fidelity check.

    Returns ``(merge_results, fidelity_warnings)``.  Modules without
    structured merge directives are silently skipped (transitional
    period; not every module ships directives yet).
    """
    results: list[ModuleMergeResult] = []
    expected: list[tuple[str, str, str]] = []
    for name in installed_modules:
        specs = _MODULE_MAPPINGS.get(name, [])
        for spec in specs:
            if spec.verbatim:
                continue
            module_src = templates_root / "modules" / spec.src
            if not module_src.is_file():
                continue
            module_text = module_src.read_text(encoding="utf-8")
            for target_rel, slot_name, content in (
                parse_module_merge_directives(module_text)
            ):
                expected.append((target_rel, slot_name, content))
                results.append(
                    merge_module_into_slot(
                        target_root, target_rel, slot_name, content,
                        non_interactive=non_interactive,
                        dry_run=dry_run,
                    )
                )
    warnings = check_slot_fidelity(target_root, expected)
    return results, warnings


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
    # The strategy-doc lifecycle directory (Antigravity External
    # code review A-P3 on commit 96b7fba): scaffolded by default so
    # adopters who use the commit-permission exception extension's
    # `dev/strategy/` coverage don't have to `mkdir` manually.
    "dev/strategy",
    "dev/strategy/archive",
    # External-dependency upstream issue drafts (core-dev-folder-set).
    # archive/ is tracked via the .gitkeep installed by _CORE_MAPPINGS;
    # the dir itself must exist before the installer writes it.
    "dev/upstream",
    "dev/upstream/archive",
    # Project-owned agent-discipline detail (core-dev-folder-set).
    # Ships empty at adoption; the README is installed by _CORE_MAPPINGS.
    "dev/rules",
    "dev/modules",
    # Progressive-onboarding module's installed-source-file home.
    # Per plan 2026-05-28-claude-cairn-progressive-onboarding (Chunk
    # P1.1, Codex P1-1 disposition): scaffold inlines a preset's seed
    # tasks into `dev/PLANNING.md` and ALSO copies the full source
    # file here so the activation helper can discover deferred tasks
    # at goodnight.  The directory exists from install time onward.
    "dev/modules/onboarding",
    # Progressive-onboarding state-file directory (Chunk P1.2 per
    # Codex P2-5 disposition: tracked, parallel to dev/intents.jsonl).
    # The scaffold creates this dir + writes an empty activation log
    # (`onboarding-activated.jsonl`) at install time so the helper
    # never has to mkdir; the tracked state means multi-team profiles
    # share activation history through git.
    "dev/.cairn",
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


#: Result record for one installed file.
#: ``status`` is ``"installed"`` (file written), ``"skipped-exists"``
#: (skipped because the file already existed and ``force`` was not
#: set), or ``"dry-run"`` (would have been written under
#: ``--dry-run``).
InstallResult = tuple[Path, list[str], list[str], str]
# (target_path, unfilled_token_names, block_slot_names, status)


def _install_one(
    src: Path,
    dst: Path,
    tokens: dict[str, str],
    target: Path,
    *,
    dry_run: bool,
    force: bool = False,
    verbatim: bool = False,
    axes: dict[str, object] | None = None,
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
        if axes is not None:
            text = strip_conditional_regions(text, axes)
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
    axes: dict[str, object] | None = None,
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
            _install_one(
                src, dst, tokens, target,
                dry_run=dry_run, force=force, axes=axes,
            )
        )
    return results


def install_skills(
    templates_root: Path,
    target: Path,
    tokens: dict[str, str],
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[InstallResult]:
    """Install the lifecycle-routine skills **unconditionally** (like core).

    A sibling to :func:`install_core` (kept separate rather than folded into
    it): the skills install to distinct destinations (``.agents/skills/`` +
    ``tools/lifecycle.py``) and carry per-file verbatim/substituted rules that
    differ from core docs, so a dedicated installer keeps each surface's rules
    legible.  Because the routines are invariant kernel they are not a
    conditional module.  ``verbatim`` is read per spec from
    :data:`_SKILLS_MAPPINGS` (the CLI script is byte-for-byte; the SKILL.md
    sources are substituted so they ride the base-cache + 3-way-merge path).
    """
    results: list[InstallResult] = []
    for src_rel, dst_rel, verbatim in _SKILLS_MAPPINGS:
        src = templates_root / src_rel
        if not src.exists():
            print(f"  [warn] skill template missing: {src_rel}", file=sys.stderr)
            continue
        dst = target / dst_rel
        results.append(
            _install_one(
                src, dst, tokens, target,
                dry_run=dry_run, force=force, verbatim=verbatim,
            )
        )
    return results


def write_local_env(
    target: Path, *, dry_run: bool = False, force: bool = False,
) -> InstallResult:
    """Write the untracked ``dev/.cairn/local-env.json`` interpreter binding.

    Resolve-don't-bake (Decision 6 / R3): record the bootstrap interpreter's
    **fully-resolved** absolute path (``Path.resolve()`` dereferences every
    symlink component, so the strict tamper-aware schema the lifecycle CLI
    enforces is satisfied) so the wrapper invokes it directly instead of relying
    on shell-level conda activation.  The file is **gitignored**, so an absolute
    path here never enters a commit -- it is forbidden only in tracked
    artifacts.  Non-clobber: an existing adopter binding is preserved unless
    ``force``.
    """
    import json

    dst = target / "dev" / ".cairn" / "local-env.json"
    if dst.exists() and not force:
        return (dst, [], [], "skipped-exists")
    if dry_run:
        return (dst, [], [], "dry-run")
    # Seed the ignore entries FIRST (Codex P1#2): otherwise a failure between
    # this write and the later unconditional gitignore seed would leave an
    # unignored local-env.json carrying a local absolute path, exposed to a
    # broad `git add`. Seeding first makes it ignored the instant it exists.
    seed_gitignore(target, _SKILLS_GITIGNORE)
    interpreter = str(Path(sys.executable).resolve())
    _assert_safe_write(dst, target)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(
        json.dumps({"interpreter": interpreter}) + "\n", encoding="utf-8"
    )
    return (dst, [], [], "installed")


def load_vendor_targets(templates_root: Path) -> list[dict[str, Any]]:
    """Load the data-driven vendor fan-out table (``skills/_data/
    vendor_targets.yml``).  JSON-encoded (valid YAML 1.2) so it parses
    stdlib-only, like the lockfile.  A vendor refresh is a row edit here."""
    import json

    path = templates_root / "skills" / "_data" / "vendor_targets.yml"
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data.get("targets", []))


def render_compatibility_matrix(templates_root: Path) -> str:
    """Render the skills compatibility matrix from the vendor-targets table.

    Generated, never hand-authored (II3 / Decision 8): the published level for
    each target is the table's, and the table's levels are claimed-pending-
    fixture until Chunk 7's harness proves a target into ``native-tested``.  The
    ``auto_suppress`` column makes the R4 gap visible per target rather than
    buried in prose.  Deterministic (sorted by target) so the drift gate is
    stable."""
    rows = sorted(load_vendor_targets(templates_root), key=lambda r: r["target"])
    out = [
        "# Skills compatibility matrix",
        "",
        "<!-- GENERATED from templates/skills/_data/vendor_targets.yml by",
        "     bootstrap.scaffold.render_compatibility_matrix; hand edits are",
        "     replaced on the next render.  Levels are CLAIMED-pending-fixture",
        "     (II3): a target is `native-tested` only once a fixture proves",
        "     install + invoke on it. -->",
        "",
        "| Target | Tier | Format | Install/invoke level | Auto-suppress |",
        "|--------|------|--------|----------------------|---------------|",
    ]
    for r in rows:
        out.append(
            f"| {r['target']} | {r['tier']} | {r.get('format', '-')} "
            f"| {r.get('level', '-')} | {r.get('auto_suppress', '-')} |"
        )
    out += [
        "",
        "## Runtime self-heal",
        "",
        "A **symlink**-tier target's read-path is fanned out from the canonical",
        "`.agents/skills/` source at install time. It is *also* re-ensured at",
        "**session-start** by the lifecycle backend (`tools/lifecycle.py",
        "session-start`), so an adopter established by lockfile-copy -- or whose",
        "symlink-tier harness was not present at install -- self-heals on first",
        "run instead of silently having no skills in that harness. The self-heal",
        "is idempotent and carries the installer's writer-safety contract:",
        "path-containment, a copy fallback where symlinks are unavailable (with a",
        "`.gitignore` seed), and a refuse-or-quarantine guard that never clobbers",
        "a divergent existing target. **alias**-tier targets read `.agents/skills/`",
        "directly and need no fan-out (nothing is emitted for them).",
    ]
    return "\n".join(out) + "\n"


def _symlinks_available(target: Path) -> bool:
    """Probe whether ``os.symlink`` works in *target* (False on Windows without
    Developer Mode / Administrator -- the copy-fallback trigger, R2)."""
    import os

    probe = target / ".cairn-symlink-probe"
    try:
        if probe.is_symlink() or probe.exists():
            probe.unlink()
        os.symlink(".", probe)
        ok = probe.is_symlink()
        probe.unlink()
        return ok
    except (OSError, NotImplementedError):
        return False


def _emit_skill_symlink(dst: Path, canonical: Path) -> str:
    """Create / verify a relative symlink ``dst`` -> the canonical skills dir."""
    import os

    rel = os.path.relpath(canonical, dst.parent)
    if dst.is_symlink():
        if os.readlink(dst) == rel:
            return "linked"  # idempotent
        dst.unlink()
    elif dst.exists():
        print(
            f"  [warn] {dst} exists as a non-symlink; leaving it untouched "
            "(remove it to enable the skills symlink).",
            file=sys.stderr,
        )
        return "exists-nonsymlink"
    dst.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(rel, dst, target_is_directory=True)
    return "linked"


def _emit_skill_copy_fallback(
    dst: Path, canonical: Path, target: Path,
) -> str:
    """Regenerate gitignored copies of the canonical skills under *dst*.

    The generated copy is a **vendor-read supply-chain artifact**, not an
    author-owned file (the canonical ``.agents/skills/`` source is the single
    editable copy).  So a diverged copy must NOT stay the active read-path
    (Codex code review P1#1, refining EP3's "never clobber", which applied to
    author-owned files, not this generated tier): the vendor harness would
    otherwise ingest stale / locally-edited / tampered instructions while the
    install reports success and the lockfile/security tests describe only the
    canonical bytes.

    Fail-safe-for-the-supply-chain: a diverged copy is **quarantined** (moved
    aside to ``<file>.diverged.bak`` -- the stray bytes are preserved for
    recovery, never silently destroyed) and then **regenerated from canonical**,
    so the active vendor-read path always carries the safe, already-scanned
    canonical bytes.  The divergence is still surfaced loudly."""
    import shutil

    quarantined: list[str] = []
    for src_file in sorted(canonical.rglob("*")):
        if not src_file.is_file():
            continue
        rel = src_file.relative_to(canonical)
        out = dst / rel
        _assert_fanout_contained(out, target)
        if out.is_file() and out.read_bytes() != src_file.read_bytes():
            # Quarantine the stray bytes (preserve, don't destroy), then
            # regenerate the canonical bytes as the active read-path.
            bak = out.with_name(out.name + ".diverged.bak")
            _assert_fanout_contained(bak, target)
            shutil.move(str(out), str(bak))
            quarantined.append(str(rel))
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_file, out)
    if quarantined:
        print(
            f"  [warn] copy-fallback divergence under {dst}: "
            f"{', '.join(quarantined)} differed from the canonical "
            ".agents/skills/ source. Each was quarantined to "
            "*.diverged.bak and the canonical bytes regenerated as the active "
            "vendor-read path -- edit the canonical source, not the generated "
            "copy. Recover any intended change from the .bak.",
            file=sys.stderr,
        )
        return "diverged-quarantined"
    return "copied"


def fan_out_skills(
    templates_root: Path,
    target: Path,
    *,
    dry_run: bool = False,
    force: bool = False,
    targets: list[dict[str, Any]] | None = None,
    allow_symlinks: bool | None = None,
) -> list[tuple[str, str, str]]:
    """Fan the canonical ``.agents/skills/`` source out to each vendor target by
    tier (Decision 4, revised).  Returns ``(target, tier_used, status)`` rows.

    * **alias** -- the harness reads ``.agents/skills/`` directly; nothing emitted.
    * **symlink** -- same SKILL.md format at a different path: a *verified*
      relative symlink to the canonical dir, emitted only when the vendor's
      parent dir already exists (a light "is this harness in use?" detection, so
      a fresh repo is not littered with empty vendor dirs).  Where symlinks are
      unavailable (Windows without Developer Mode) it degrades to the
      **gitignored generated copy** + divergence guard.
    * **manual** -- a different-format target (compiled artifact / documented
      manual fallback); never a symlink to incompatible files.

    Every destination is containment-checked **before** any write (S3); the
    divergence guard runs only after containment validates the target.
    """
    canonical = target / ".agents" / "skills"
    rows = targets if targets is not None else load_vendor_targets(templates_root)
    can_symlink = (
        _symlinks_available(target) if allow_symlinks is None else allow_symlinks
    )
    results: list[tuple[str, str, str]] = []
    advisory = False
    for row in rows:
        name = str(row.get("target", "?"))
        tier = row.get("tier")
        if tier == "alias":
            results.append((name, "alias", "noop"))
            continue
        if tier == "manual":
            results.append((name, "manual", "manual-fallback"))
            continue
        if tier != "symlink":
            results.append((name, str(tier), "unknown-tier"))
            continue
        path = str(row.get("path", ""))
        if not path or path.startswith("/") or ".." in Path(path).parts:
            raise ScaffoldSecurityError(
                f"vendor target {name!r}: unsafe fan-out path {path!r}"
            )
        dst = target / path
        if not dst.parent.exists():
            results.append((name, "symlink", "skipped-vendor-absent"))
            continue
        _assert_fanout_contained(dst, target)
        if dry_run:
            results.append((name, "symlink" if can_symlink else "copy", "dry-run"))
            continue
        if can_symlink:
            results.append((name, "symlink", _emit_skill_symlink(dst, canonical)))
        else:
            advisory = True
            status = _emit_skill_copy_fallback(dst, canonical, target)
            seed_gitignore(target, (path.rstrip("/") + "/",))
            results.append((name, "copy", status))
    if advisory:
        print(
            "  [advisory] symlinks unavailable (Windows without Developer "
            "Mode?) -- skills fanned out as gitignored generated copies. "
            "Enable Developer Mode for symlinked vendor targets.",
            file=sys.stderr,
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


# ---------------------------------------------------------------------------
# Progressive onboarding -- preset-keyed slot substitution
# ---------------------------------------------------------------------------

#: Three named preset onboarding files (under
#: ``templates/onboarding/<name>.md``).  An adopter's chosen preset
#: maps 1:1 to one of these files; the scaffold inlines the file's
#: seed tasks into ``dev/PLANNING.md``'s ``onboarding-tasks`` slot and
#: copies the full source file to ``dev/modules/onboarding/<name>.md``
#: as the authoritative reference for deferred-task discovery at
#: goodnight (Codex P1-1 / P2-4 disposition: seed-only PLANNING render
#: + tracked installed source).
_ONBOARDING_PRESETS: frozenset[str] = frozenset(
    {"solo-greenfield", "collaborative-team", "high-rigor-legacy"}
)

#: Matches ``* [seed; id: <name>]`` task lines in a preset onboarding
#: file.  The bracket payload syntax also accepts other ``key: value``
#: pairs (extension point); the parser keeps the whole bracketed
#: payload + task body together when rendering into the slot.
_ONBOARDING_SEED_RE = re.compile(
    r"^\*\s+\[seed;\s*id:\s*\S+[^\]]*\]\s*$",
)


def _extract_seed_tasks(preset_text: str) -> list[str]:
    """Extract seed-task entries from a preset onboarding file.

    Each seed task is a multi-line markdown list item:

        * [seed; id: read-lifecycle-doctrine]
          Read `doctrine/lifecycle.md` ...

    Returns the rendered list-item blocks (each block preserving the
    `[seed; ...]` header line + any indented continuation lines until
    the next top-level item or non-indented blank line).  Deferred
    tasks (``[trigger: ...]``) and non-task content (prose, doctrine
    headers, metadata blocks) are excluded by construction.
    """
    blocks: list[str] = []
    current: list[str] = []
    in_seed = False
    for line in preset_text.splitlines():
        if _ONBOARDING_SEED_RE.match(line):
            if current:
                blocks.append("\n".join(current).rstrip())
                current = []
            current.append(line)
            in_seed = True
            continue
        if not in_seed:
            continue
        # Continuation if indented (>= 2 spaces); otherwise close the
        # current seed block on first non-indented non-empty line.
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


def _render_onboarding_slot(preset_name: str, seed_blocks: list[str]) -> str:
    """Build the slot content for ``dev/PLANNING.md``'s
    ``onboarding-tasks`` slot from the preset name + extracted seeds.

    The first line is the ``<!-- preset: <name> -->`` metadata
    comment the goodnight activation helper reads to resolve which
    installed source file
    (``<target>/dev/modules/onboarding/<name>.md``) carries the
    deferred tasks (Codex P2-4 disposition: the metadata-comment
    contract is established here at scaffold time so the helper's
    contract is uniform).
    """
    parts = [f"<!-- preset: {preset_name} -->", ""]
    parts.extend(seed_blocks)
    return "\n".join(parts).rstrip() + "\n"


def _substitute_slot(
    text: str, slot_name: str, replacement: str,
) -> tuple[str, bool]:
    """Replace the body BETWEEN ``<!-- cairn:slot NAME -->`` and
    ``<!-- cairn:end NAME -->`` markers with *replacement*.

    Returns ``(new_text, did_substitute)``.  If the slot is not
    found, returns ``(text, False)`` so the caller can warn.
    """
    open_marker = f"<!-- cairn:slot {slot_name} -->"
    close_marker = f"<!-- cairn:end {slot_name} -->"
    o = text.find(open_marker)
    if o < 0:
        return text, False
    c = text.find(close_marker, o + len(open_marker))
    if c < 0:
        return text, False
    body_start = o + len(open_marker)
    new_body = "\n" + replacement.strip("\n") + "\n"
    return text[:body_start] + new_body + text[c:], True


#: The activation helper script Cairn ships to every adopter (Chunk
#: P1.2 -- ALWAYS installed alongside any progressive-onboarding
#: deployment).  The source lives under templates/modules/default-on/
#: parallel to the foldback_suggest.py + claim_check.py precedent;
#: the destination is the adopter's scripts/ tree, invoked at
#: goodnight per doctrine/onboarding.md.
_ONBOARDING_HELPER_SRC_REL = "modules/default-on/onboarding_activate.py"
_ONBOARDING_HELPER_DST_REL = "scripts/onboarding_activate.py"

#: The activation log path the helper appends to (Chunk P1.2 per
#: Codex P2-5: tracked, parallel to dev/intents.jsonl).
_ONBOARDING_LOG_REL = "dev/.cairn/onboarding-activated.jsonl"

#: The header comment the scaffold writes into a freshly-seeded
#: activation log so a cold reader knows what it is + the schema.
_ONBOARDING_LOG_HEADER = (
    "# dev/.cairn/onboarding-activated.jsonl -- progressive-onboarding\n"
    "# activation log; one JSONL line per activation; append-only.\n"
    "# Schema: {task-id, activated-at, by-agent, source-preset, trigger}.\n"
    "# Managed by scripts/onboarding_activate.py at goodnight;\n"
    "# see doctrine/onboarding.md for the mechanism.\n"
)

#: The shared onboarding reference docs Cairn ships into an adopter when
#: a preset is selected (fold-back: onboarding-doc-delivery).  Sourced
#: from ``cairn/docs/`` (``templates_root.parent / "docs"``) and installed
#: under ``dev/modules/onboarding/``.  The presets' "walk this doc" task
#: refs point at the *installed* copies; without this write those refs
#: were dead links on first run (the bug this delivery fixes).
_ONBOARDING_DOC_NAMES = ("agent-team-onboarding.md", "dev-tour.md")
_ONBOARDING_DOC_DST_DIR_REL = "dev/modules/onboarding"


def install_onboarding(
    templates_root: Path,
    target: Path,
    preset_name: str | None,
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[InstallResult]:
    """Install the progressive-onboarding artifacts (Chunk P1.1 +
    P1.2).

    Three categories of writes:

    **Always (regardless of preset selection)** -- per Chunk P1.2:

    A. Install the activation helper script to
       ``<target>/scripts/onboarding_activate.py`` (verbatim copy).
    B. Seed an empty activation log at
       ``<target>/dev/.cairn/onboarding-activated.jsonl`` (header-
       comment-only; the helper appends to it at goodnight).

    **Only when a named preset is selected** -- per Chunk P1.1:

    C. Inline seed tasks + the ``<!-- preset: <name> -->`` metadata
       comment into ``dev/PLANNING.md``'s ``onboarding-tasks`` slot.
       ONLY ``[seed; id: ...]`` items render into the slot; deferred
       tasks (``[trigger: X; id: ...]``) stay in the installed source
       file (write D).
    D. Copy the full preset source file
       ``templates/onboarding/<name>.md`` to
       ``<target>/dev/modules/onboarding/<name>.md`` byte-for-byte.
       This is the authoritative reference the goodnight activation
       helper reads to discover deferred tasks (Codex External
       Review P1-1).
    E. Copy the shared onboarding reference docs
       (``docs/agent-team-onboarding.md`` + ``docs/dev-tour.md``) to
       ``<target>/dev/modules/onboarding/`` so the presets' "walk this
       doc" task refs resolve in the adopter (fold-back:
       onboarding-doc-delivery; without this they were dead links on
       first run).  Shared across presets -- shipped on any preset
       selection.

    Returns the list of InstallResults for each write (the
    always-writes always present; the preset-conditional writes only
    when ``preset_name`` is one of the three named presets).

    Per plan 2026-05-28-claude-cairn-progressive-onboarding Chunks
    P1.1 (slot subst + preset source copy) + P1.2 (helper script
    install + activation log seed) + Codex External Review P1-1 /
    P2-4 / P2-5 dispositions.
    """
    results: list[InstallResult] = []

    # ----- Always: install the activation helper script (A) -------------
    helper_src = templates_root / _ONBOARDING_HELPER_SRC_REL
    helper_dst = target / _ONBOARDING_HELPER_DST_REL
    if helper_src.exists():
        if dry_run:
            results.append((helper_dst, [], [], "dry-run"))
        elif helper_dst.exists() and not force:
            print(
                f"  [skip] {helper_dst}: already exists -- pass --force "
                f"to overwrite",
                file=sys.stderr,
            )
            results.append((helper_dst, [], [], "skipped-exists"))
        else:
            _assert_safe_write(helper_dst, target)
            helper_dst.parent.mkdir(parents=True, exist_ok=True)
            helper_dst.write_bytes(helper_src.read_bytes())
            results.append((helper_dst, [], [], "installed"))
    else:
        print(
            f"  [warn] onboarding helper source missing: "
            f"templates/{_ONBOARDING_HELPER_SRC_REL}",
            file=sys.stderr,
        )

    # ----- Always: seed an empty activation log (B) ---------------------
    log_dst = target / _ONBOARDING_LOG_REL
    if dry_run:
        results.append((log_dst, [], [], "dry-run"))
    elif log_dst.exists() and not force:
        print(
            f"  [skip] {log_dst}: already exists -- pass --force to "
            f"overwrite",
            file=sys.stderr,
        )
        results.append((log_dst, [], [], "skipped-exists"))
    else:
        _assert_safe_write(log_dst, target)
        log_dst.parent.mkdir(parents=True, exist_ok=True)
        log_dst.write_text(_ONBOARDING_LOG_HEADER, encoding="utf-8")
        results.append((log_dst, [], [], "installed"))

    # ----- Preset-conditional: slot subst + source copy (C + D) ---------
    if not preset_name or preset_name not in _ONBOARDING_PRESETS:
        return results

    src = templates_root / "onboarding" / f"{preset_name}.md"
    if not src.exists():
        print(
            f"  [warn] onboarding preset source missing: "
            f"templates/onboarding/{preset_name}.md",
            file=sys.stderr,
        )
        return results

    preset_text = src.read_text(encoding="utf-8")
    seed_blocks = _extract_seed_tasks(preset_text)
    rendered = _render_onboarding_slot(preset_name, seed_blocks)

    # Write C: substitute into installed PLANNING.md's slot.
    planning_dst = target / "dev" / "PLANNING.md"
    if not planning_dst.exists():
        print(
            f"  [warn] onboarding: dev/PLANNING.md not yet installed -- "
            f"slot substitution skipped (run after install_core)",
            file=sys.stderr,
        )
    else:
        planning_text = planning_dst.read_text(encoding="utf-8")
        new_text, ok = _substitute_slot(
            planning_text, "onboarding-tasks", rendered,
        )
        if not ok:
            print(
                f"  [warn] onboarding: `onboarding-tasks` slot not found "
                f"in dev/PLANNING.md -- preset content not injected",
                file=sys.stderr,
            )
        elif new_text != planning_text:
            if dry_run:
                results.append((planning_dst, [], [], "dry-run"))
            else:
                _assert_safe_write(planning_dst, target)
                planning_dst.write_text(new_text, encoding="utf-8")
                results.append((planning_dst, [], [], "installed"))

    # Write D: copy source file verbatim to installed-source path.
    source_dst = target / "dev" / "modules" / "onboarding" / f"{preset_name}.md"
    if dry_run:
        results.append((source_dst, [], [], "dry-run"))
    else:
        if source_dst.exists() and not force:
            print(
                f"  [skip] {source_dst}: already exists -- pass --force to "
                f"overwrite",
                file=sys.stderr,
            )
            results.append((source_dst, [], [], "skipped-exists"))
        else:
            _assert_safe_write(source_dst, target)
            source_dst.parent.mkdir(parents=True, exist_ok=True)
            source_dst.write_text(preset_text, encoding="utf-8")
            results.append((source_dst, [], [], "installed"))

    # Write E: ship the shared onboarding reference docs into the
    # installed-source dir so the presets' "walk this doc" refs resolve
    # in the adopter (fold-back: onboarding-doc-delivery).  Sourced from
    # cairn/docs/; same skip-unless-force guard as Write D.  Shared across
    # presets, so a preset selection ships both regardless of which one.
    docs_root = templates_root.parent / "docs"
    for doc_name in _ONBOARDING_DOC_NAMES:
        doc_src = docs_root / doc_name
        doc_dst = target / _ONBOARDING_DOC_DST_DIR_REL / doc_name
        if not doc_src.exists():
            print(
                f"  [warn] onboarding doc source missing: docs/{doc_name}",
                file=sys.stderr,
            )
            continue
        if dry_run:
            results.append((doc_dst, [], [], "dry-run"))
            continue
        if doc_dst.exists() and not force:
            print(
                f"  [skip] {doc_dst}: already exists -- pass --force to "
                f"overwrite",
                file=sys.stderr,
            )
            results.append((doc_dst, [], [], "skipped-exists"))
            continue
        _assert_safe_write(doc_dst, target)
        doc_dst.parent.mkdir(parents=True, exist_ok=True)
        doc_dst.write_text(
            doc_src.read_text(encoding="utf-8"), encoding="utf-8"
        )
        results.append((doc_dst, [], [], "installed"))

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


#: Forge name -> adopter-root reference directory (fold-back #38).  The
#: issue-capture module ships starter issue templates + a labels.yml per
#: forge under reference/<dir>/; when a forge is named in the profile and
#: issue-capture installs, that dir is copied into the adopter root.
_FORGE_REFERENCE_DIRS: dict[str, str] = {"gitlab": ".gitlab", "github": ".github"}


def install_issue_capture_reference(
    templates_root: Path,
    target: Path,
    forge: str,
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[InstallResult]:
    """Copy the issue-capture forge reference starter into *target*.

    For ``forge`` in ``_FORGE_REFERENCE_DIRS`` (gitlab/github), copies every
    file under ``templates/modules/team-gated/issue-capture/reference/<dir>/``
    to the matching adopter-root path (``.gitlab/...`` / ``.github/...``),
    verbatim (starter content; no token substitution).  Non-clobber:
    ``_install_one`` skips an existing file unless ``force`` -- so a
    Maintainer's customized templates survive a re-scaffold.  Fold-back #38.
    """
    forge_dir = _FORGE_REFERENCE_DIRS[forge]
    ref_root = (
        templates_root / "modules" / "team-gated"
        / "issue-capture" / "reference" / forge_dir
    )
    results: list[InstallResult] = []
    if not ref_root.is_dir():
        print(
            f"  [warn] issue-capture reference missing: {ref_root}",
            file=sys.stderr,
        )
        return results
    for src in sorted(p for p in ref_root.rglob("*") if p.is_file()):
        rel = src.relative_to(ref_root)
        dst = target / forge_dir / rel
        results.append(
            _install_one(
                src, dst, {}, target,
                dry_run=dry_run, force=force, verbatim=True,
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
    # Skills install unconditionally (like core); always in the manifest.
    entries.extend(_SKILLS_MAPPINGS)
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


def _lock_file_list(
    modules: list[str], optional: list[tuple[str, str]],
) -> list[tuple[str, str, bool]]:
    """The ``(src-rel-to-templates/, dst, verbatim)`` set a lockfile tracks:
    core + selected modules (via :func:`install_manifest`) + optional
    templates.  De-duplicated by destination, stable order."""
    entries = list(install_manifest(modules))
    for src_rel, dst_rel in optional:
        entries.append((src_rel, dst_rel, False))
    seen: set[str] = set()
    out: list[tuple[str, str, bool]] = []
    for src, dst, verbatim in entries:
        if dst in seen:
            continue
        seen.add(dst)
        out.append((src, dst, verbatim))
    return out


def write_install_lockfile(
    target: Path,
    cairn_root: Path,
    templates_root: Path,
    *,
    tokens: dict[str, str],
    modules: list[str],
    optional: list[tuple[str, str]],
    profile: dict[str, Any],
    allow_secret_tokens: tuple[str, ...] = (),
    onboarding_preset: str | None = None,
) -> dict[str, Any] | None:
    """Write ``dev/.cairn/cairn-lock.yml`` + the scoped base-template cache.

    **Fail-closed (P-1)**: a lockfile must record a *clean* ancestor, so
    this refuses (returns ``None``, prints guidance) if any tracked file on
    disk differs from a clean install -- e.g. a ``skipped-exists`` file the
    adopter customized.  On a fresh install every file matches, so the
    lockfile + cache are written.  Token-secret guard runs first (R9).

    The base cache stores the **raw** (pre-substitution) template for each
    **non-verbatim** install only (I4: verbatim scripts use the hash policy,
    not a cached base).

    ``onboarding_preset`` (per plan 2026-05-28-claude-cairn-progressive-
    onboarding Chunk P1.1): when set, the lockfile's "clean install"
    computation for ``dev/PLANNING.md`` includes the post-install
    onboarding-slot substitution + preset metadata write, so the file's
    on-disk content matches the expected ``would`` despite
    ``install_onboarding`` having modified it after ``install_core``.
    """
    _refuse_secret_tokens(tokens, allow_secret_tokens)

    file_records: list[dict[str, Any]] = []
    cache_writes: list[tuple[Path, str]] = []
    diverged: list[str] = []

    # Pre-compute the onboarding overlay for PLANNING.md so the
    # `would` calculation in the loop below can apply the same slot
    # substitution `install_onboarding` did at install time.  If no
    # preset is selected, the overlay is empty and PLANNING.md is
    # checked against the token-substituted raw template (the
    # baseline behavior).
    onboarding_overlay: str | None = None
    if (
        onboarding_preset
        and onboarding_preset in _ONBOARDING_PRESETS
    ):
        preset_src = (
            templates_root / "onboarding" / f"{onboarding_preset}.md"
        )
        if preset_src.exists():
            seed_blocks = _extract_seed_tasks(
                preset_src.read_text(encoding="utf-8")
            )
            onboarding_overlay = _render_onboarding_slot(
                onboarding_preset, seed_blocks,
            )

    for src_rel, dst_rel, verbatim in _lock_file_list(modules, optional):
        src = templates_root / src_rel
        if not src.exists():
            continue
        raw = src.read_text(encoding="utf-8")
        if verbatim:
            would = src.read_bytes()
        else:
            substituted = substitute_tokens(raw, tokens)
            # Profile-size the always-on surface (cairn-profile-sized-assembly
            # P2): strip `cairn:if` regions the embedded profile does not select,
            # keyed off the SAME `profile["axes"]` `install_core` stripped the
            # on-disk file with -- so this expected-clean-install `would` matches
            # the stripped install and the divergence check below stays clean for
            # every profile.  No-op on a template carrying no directive (the
            # common case) and on an empty axes map (keep-on-missing-axis).
            substituted = strip_conditional_regions(
                substituted, profile.get("axes") or {}
            )
            if (
                dst_rel == "dev/PLANNING.md"
                and onboarding_overlay is not None
            ):
                # Apply the same slot substitution `install_onboarding`
                # did so the lockfile sees a clean install.
                with_overlay, ok = _substitute_slot(
                    substituted, "onboarding-tasks", onboarding_overlay,
                )
                substituted = with_overlay if ok else substituted
            would = substituted.encode("utf-8")
        dst_abs = target / dst_rel
        on_disk = dst_abs.read_bytes() if dst_abs.exists() else None
        if on_disk is None or on_disk != would:
            diverged.append(dst_rel)
            continue
        rec: dict[str, Any] = {
            "src": src_rel, "dst": dst_rel, "verbatim": verbatim,
            "hash": "sha256:" + _sha256_hex(would),
        }
        if dst_rel in _LIVING_STATE_DSTS:
            # Adopter-authored project state: tracked for upgrade, excluded
            # from the verify_integrity tamper check (see _LIVING_STATE_DSTS).
            rec["living_state"] = True
        if not verbatim:
            cache_rel = f"{_BASE_CACHE_REL}/{dst_rel}"
            rec["base_cache"] = cache_rel
            rec["base_hash"] = "sha256:" + _sha256_hex(raw.encode("utf-8"))
            cache_writes.append((target / cache_rel, raw))
        else:
            # The as-shipped baseline for a verbatim file, kept distinct from
            # ``hash`` so ``hash`` can be advanced to the adopter's committed
            # on-disk content (``upgrade --finalize``) for integrity while
            # ``classify_verbatim`` still detects an adopter fork against the
            # upstream baseline.  At fresh install ``hash == base_hash``.
            rec["base_hash"] = "sha256:" + _sha256_hex(would)
        file_records.append(rec)

    if diverged:
        shown = ", ".join(diverged[:5]) + ("..." if len(diverged) > 5 else "")
        print(
            f"  [warn] {_LOCKFILE_REL} NOT written: {len(diverged)} installed "
            f"file(s) differ from a clean install ({shown}). A lockfile must "
            "record a clean ancestor; run `python bootstrap/scaffold.py "
            "upgrade --init-lock --target <repo>` to synthesize one from the "
            "current tree instead.",
            file=sys.stderr,
        )
        return None

    lock: dict[str, Any] = {
        "schema": _LOCK_SCHEMA,
        "cairn_version": _cairn_version(cairn_root),
        "cairn_commit": _cairn_commit(cairn_root),
        "profile": profile,
        "modules": sorted(modules),
        "optional_templates": sorted(dst for _, dst in optional),
        "tokens": dict(tokens),
        "files": file_records,
    }
    for cache_path, raw in cache_writes:
        _assert_safe_write(cache_path, target)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(raw, encoding="utf-8")
    lock_path = target / _LOCKFILE_REL
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    _assert_safe_write(lock_path, target)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(_emit_lock_yaml(lock), encoding="utf-8")
    return lock
