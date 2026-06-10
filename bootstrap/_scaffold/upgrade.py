"""Scaffold engine -- upgrade subsystem (scaffold-split Stage 7).

The ``scaffold.py upgrade`` capability: plan, stage, and apply the token- + slot-
aware 3-way merge of a Cairn template change into an adopter's customized tree, the
lockfile subcommands (``--init-lock`` / ``--adopt-module`` / ``--finalize``), the
dirty-tree refusal, the staging area, the profile self-heal, and the ``cmd_upgrade``
dispatcher. Also owns the canonical Cairn-root resolver (``_cairn_root`` /
``_find_cairn_root``, 0B.2) -- shared with the cli, which sits above this module.

A layer-7 subsystem: it depends DOWNWARD on the leaves and the install subsystem
(config, security, merge, slotmerge, lockfile, install) and never upward on the
cli (``main`` / ``build_arg_parser``); ``main`` dispatches to ``cmd_upgrade`` and
reads ``_cairn_root`` from here.

Pure motion from the pre-split monolith (Stage 7): the symbols are unchanged; only
their home moved. Loaded via the engine's verifying finder, so this file's real
path is confirmed within the Cairn root before it executes.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, NamedTuple

from .config import (
    KNOWN_TOKENS,
    PresetError,
    _AXES,
    _CORE_MAPPINGS,
    _GITIGNORE_SEEDS,
    _KNOWN_VENDOR_WRAPPERS,
    _MODULE_MAPPINGS,
    _SKILLS_GITIGNORE,
    _SKILLS_MAPPINGS,
    load_config,
    missing_required_tokens,
    resolve_axes,
    strip_conditional_regions,
)
from .security import _assert_safe_write, ScaffoldSecurityError
from .merge import SlotError, merge_file
from .slotmerge import substitute_tokens
from .lockfile import (
    _BASE_CACHE_REL,
    _LIVING_STATE_DSTS,
    _LOCKFILE_REL,
    _LOCK_SCHEMA,
    _PROFILE_REL,
    _behind_by_n,
    _cairn_commit,
    _cairn_version,
    _emit_lock_yaml,
    _sha256_hex,
    classify_verbatim,
    read_lockfile,
)
from .install import (
    _lock_file_list,
    fan_out_skills,
    seed_gitignore,
)


def _cairn_root() -> Path:
    """The Cairn repo root, resolved ONCE from this engine module's stable
    on-disk location and **owned here** (scaffold-split 0B.2 / RR2).

    The engine lives at ``bootstrap/_scaffold/__init__.py`` → ``parents[2]`` is
    ``<cairn root>``. Subsystems must read the root from **this** owner — they
    must NOT re-derive it from their own ``__file__`` (a module extracted into
    ``bootstrap/_scaffold/<m>.py`` sits at the same depth as this ``__init__``,
    but a per-call-site ``Path(__file__).parent.parent`` would mis-anchor if the
    file's depth ever changed). Anchoring to one owner removes that footgun.
    """
    return Path(__file__).resolve().parents[2]


def _find_cairn_root(script_path: Path) -> Path:
    """Back-compat shim for callers that pass an explicit script path. The
    canonical resolver is :func:`_cairn_root` (0B.2). Resolves two directories
    above ``script_path`` (the historical ``bootstrap/scaffold.py`` layout)."""
    return script_path.resolve().parent.parent

#: Directories searched (in order) for an adopter's fidelity manifest when
#: recovering ``cairn_commit`` / checking the citation.  ``dev/.cairn/`` is the
#: canonical home (the adoption-state-home convention); ``dev/strategy/`` is the
#: legacy home, kept indefinitely for un-migrated adopters with a migration
#: advisory at the call site.
_MANIFEST_SEARCH_DIRS = ("dev/.cairn", "dev/strategy")


# ---------------------------------------------------------------------------
# The `upgrade` subcommand (Chunk 5/6): --plan / --stage / --apply / --init-lock
# ---------------------------------------------------------------------------

_STAGING_REL = "dev/.cairn-upgrade"          # ephemeral, gitignored (R3)
_STAGE_META = "stage-metadata.json"
_CONFLICT_MARKER = "<<<<<<< ours"


def _cairn_is_git(cairn_root: Path) -> bool:
    import subprocess
    try:
        r = subprocess.run(
            ["git", "-C", str(cairn_root), "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return r.returncode == 0 and r.stdout.strip() == "true"


def _theirs_text(
    cairn_root: Path, templates_root: Path, src_rel: str, to_ref: str | None,
) -> str | None:
    """The upstream template for *src_rel* at the target version: the
    currently-running tree (``to_ref is None``) or, **git-checkout-only**
    (P-4), ``git show <to_ref>:templates/<src_rel>``.  None if absent."""
    if to_ref is None:
        p = templates_root / src_rel
        return p.read_text(encoding="utf-8") if p.exists() else None
    import subprocess
    try:
        r = subprocess.run(
            ["git", "-C", str(cairn_root), "show",
             f"{to_ref}:templates/{src_rel}"],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None


def _theirs_bytes(
    cairn_root: Path, templates_root: Path, src_rel: str, to_ref: str | None,
) -> bytes | None:
    if to_ref is None:
        p = templates_root / src_rel
        return p.read_bytes() if p.exists() else None
    text = _theirs_text(cairn_root, templates_root, src_rel, to_ref)
    return text.encode("utf-8") if text is not None else None


#: Kinds that may be staged + applied (they advance the machine
#: authority).  Every other kind is report-only and is NEVER staged, so it
#: can never be applied: slot-removed, error,
#: review-only, needs-value, removed-upstream, verbatim-locally-modified,
#: verbatim-missing, verbatim-up-to-date, up-to-date.
#:
#: ``clean-locally-modified`` is the B-C-1 sub-classification of a clean
#: 3-way merge result: the adopter had customized the file locally
#: (``ours != base``) and the customization merged cleanly with the new
#: upstream.  Advances identically to ``clean``; reported separately so
#: the adopter sees their customizations were preserved across the merge
#: (vs. ``clean`` which means the file was untouched).
_ADVANCING_KINDS = frozenset(
    {"clean", "clean-locally-modified", "conflict", "verbatim-update",
     "new-core", "new-module"}
)

#: Display labels for the upgrade report.  Maps the internal kind to the
#: adopter-facing label; kinds not in this map render verbatim.
_KIND_DISPLAY_LABEL = {
    "clean": "clean (untouched)",
    "clean-locally-modified": "locally-modified (merged clean)",
    "new-core": "new core/skills (added)",
    "new-module": "new module file (added)",
    "new-module-blocked": "new module file (BLOCKED — adopt-as-fork or reconcile, then re-stage)",
    "new-module-lockconflict": "new module file (BLOCKED — destination owned by another source; resolve by hand)",
}


class FilePlan(NamedTuple):
    dst: str
    kind: str
    applied: str | None      # content written on --apply (advancing kinds); else None
    detail: str
    theirs_raw: str | None    # new upstream RAW template (mergeable) -> refreshed base cache
    base_cache: str | None    # lockfile base_cache rel path (mergeable) to refresh
    src: str | None = None    # new-core: source template rel-to-templates/ (to build the lockfile entry)
    verbatim: bool = False    # new-core: verbatim flag for the new lockfile entry


def _embedded_axes(profile: dict[str, Any] | None) -> dict[str, str]:
    """The six-axis strip key from a lockfile/profile block (string values)."""
    return {k: str(v) for k, v in ((profile or {}).get("axes") or {}).items()}


def _resolve_current_profile(
    target: Path, lock: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, str]]:
    """The adopter's CURRENT profile for upgrade-time materialization (S1).

    Returns ``(profile_block, axes)``.  Reads the committed
    ``dev/.cairn/profile.yml`` -- the adopter may have changed their profile
    since install (solo -> multi or back) -- and resolves it exactly as install
    / init-lock do.  **Falls back to the pre-upgrade lockfile's embedded
    profile** when ``profile.yml`` is absent, unparseable, or incomplete, so the
    overwhelmingly-common no-change case is byte-for-byte a same-profile upgrade
    (``theirs`` sized identically to ``base``).  A profile *change* makes
    ``theirs`` materialize under the new profile, so the 3-way merge sees a
    newly-selected section as a clean ADD and a newly-dropped one as a clean
    DELETE -- never a spurious conflict, and slot-transplant still preserves
    every filled adopter slot (F3)."""
    lock_profile = lock.get("profile") or {}
    lock_axes = _embedded_axes(lock_profile)
    profile_path = target / _PROFILE_REL
    if not profile_path.is_file():
        return lock_profile, lock_axes
    try:
        cfg = load_config(profile_path)
        block, _tokens, missing, invalid = _resolve_lock_profile_fields(cfg)
    except Exception:  # noqa: BLE001 -- a malformed profile.yml falls back
        return lock_profile, lock_axes
    axes = _embedded_axes(block)
    if missing or invalid or not axes:
        # An incomplete/invalid current profile is not a safe basis to re-strip
        # the upgrade ancestor: fall back to the lockfile profile (a no-op vs.
        # the install-time sizing) rather than risk dropping a section.
        return lock_profile, lock_axes
    return block, axes


def _assert_mapping_ownership(lock_modules: set[str]) -> None:
    """Global destination-ownership invariant (External Security review F4): a
    destination claimed by more than one selected InstallSpec -- across the core,
    skills, and adopted-module mapping sets -- is a mapping bug. Refuse it (never
    silently let one spec shadow another), independent of lock / source state, so
    a duplicate hidden by source-absence or processing order cannot slip through.
    Current Cairn mappings have none; this preserves that as an enforced invariant."""
    owners: dict[str, list[str]] = {}
    for src, dst in _CORE_MAPPINGS:
        owners.setdefault(dst, []).append(f"core:{src}")
    for src, dst, _verbatim in _SKILLS_MAPPINGS:
        owners.setdefault(dst, []).append(f"skills:{src}")
    for mod in sorted(lock_modules):
        for spec in _MODULE_MAPPINGS.get(mod, []):
            owners.setdefault(spec.dst, []).append(f"module[{mod}]:{spec.src}")
    dupes = {dst: who for dst, who in owners.items() if len(who) > 1}
    if dupes:
        detail = "; ".join(
            f"{dst} <- {', '.join(who)}" for dst, who in sorted(dupes.items()))
        raise ValueError(
            "mapping ownership conflict: destination(s) claimed by multiple "
            f"InstallSpecs: {detail}")


def _compute_upgrade(
    target: Path, cairn_root: Path, templates_root: Path,
    lock: dict[str, Any], to_ref: str | None,
) -> tuple[list[FilePlan], dict[str, Any]]:
    """Classify every lockfile-tracked file for upgrade + the structural
    drift.  Pure read-only -- no writes."""
    tokens = {str(k): str(v) for k, v in (lock.get("tokens") or {}).items()}
    # Profile-sized assembly (cairn-profile-sized-assembly P3 / S1): materialize
    # the merge ancestor `base` under the OLD embedded profile and `theirs` under
    # the adopter's CURRENT profile.  `ours` (on disk) is already old-profile-
    # sized and is left untouched.
    old_axes = _embedded_axes(lock.get("profile"))
    _new_profile, new_axes = _resolve_current_profile(target, lock)
    plans: list[FilePlan] = []
    for rec in lock.get("files", []):
        dst = rec["dst"]
        verbatim = bool(rec.get("verbatim"))
        src_rel = rec["src"]
        # Renamed vendor wrapper (#45): the lockfile records the thin
        # wrapper under its canonical dst ``VENDOR.md`` (``write_install_
        # lockfile`` does not resolve the rename), but an adopter renames it
        # to their tool's file (``CLAUDE.md`` etc.).  If ``VENDOR.md`` is
        # absent on disk but a known wrapper is present, classify THAT file
        # -- the base cache stays keyed on VENDOR.md (``rec["base_cache"]``),
        # so the 3-way merge still recovers the clean ancestor.  Without this,
        # a renamed-wrapper adopter sees a spurious ``review-only`` "file
        # missing on disk" for VENDOR.md on every upgrade.
        if src_rel == "core/VENDOR.md" and not (target / dst).exists():
            resolved = _resolve_vendor_wrapper(
                target, {r["dst"] for r in lock.get("files", [])},
            )
            if resolved is not None:
                dst = resolved
        dst_abs = target / dst
        ours_bytes = dst_abs.read_bytes() if dst_abs.exists() else None
        theirs_b = _theirs_bytes(cairn_root, templates_root, src_rel, to_ref)
        if theirs_b is None:
            plans.append(FilePlan(dst, "removed-upstream", None,
                                  "no longer in upstream templates", None, None))
            continue
        if verbatim:
            # Use the as-shipped baseline (``base_hash``) for fork detection,
            # not ``hash`` (which ``--finalize`` advances to the adopter's
            # committed on-disk content). Fall back to ``hash`` for lockfiles
            # written before verbatim records carried ``base_hash``.
            kind = classify_verbatim(
                ours_bytes, rec.get("base_hash") or rec.get("hash", ""), theirs_b)
            plans.append(FilePlan(
                dst, f"verbatim-{kind}",
                theirs_b.decode("utf-8", "replace") if kind == "update" else None,
                "", None, None))
            continue
        # Mergeable .md.
        if ours_bytes is None:
            # File missing on disk (e.g. a default-on module slot that never
            # installed).  Carry theirs_raw so --stage can write the upstream
            # version into the review-only surface (there is no .ours to pair
            # it with -- nothing is on disk).
            plans.append(FilePlan(dst, "review-only", None,
                                  "file missing on disk",
                                  theirs_b.decode("utf-8"), None))
            continue
        ours = ours_bytes.decode("utf-8")
        theirs_raw = theirs_b.decode("utf-8")
        cache_rel = rec.get("base_cache")
        base_path = (target / cache_rel) if cache_rel else None
        if base_path is None or not base_path.exists():
            # No recoverable base (e.g. a --init-lock migrated tree, I3) ->
            # review-only diff, never a pretended 3-way merge.  Carry
            # theirs_raw so --stage can write the upstream version alongside
            # the on-disk copy for a by-hand merge.
            plans.append(FilePlan(dst, "review-only", None,
                                  "no recoverable base (review-only diff)",
                                  theirs_raw, None))
            continue
        base_raw = base_path.read_text(encoding="utf-8")
        # Size the ancestor sides for the merge view only: base under the OLD
        # profile, theirs under the NEW profile.  The cached `base_raw` and the
        # FilePlan's `theirs_raw` (the next ancestor) stay FULL/unsized -- the
        # strip is a reconstruction-time view, never baked into the cache, so a
        # later profile change can still re-include a stripped section.  strip on
        # the raw template commutes with token substitution (a `cairn:if` marker
        # carries no token), so stripping here matches an install-time strip.
        base_sized = (strip_conditional_regions(base_raw, old_axes)
                      if old_axes else base_raw)
        theirs_sized = (strip_conditional_regions(theirs_raw, new_axes)
                        if new_axes else theirs_raw)
        try:
            res = merge_file(base_sized, theirs_sized, ours, tokens)
        except SlotError as exc:
            plans.append(FilePlan(dst, "error", None,
                                  f"malformed slots: {exc}", None, None))
            continue
        # B-C-1: split `clean` into `clean (untouched)` vs.
        # `locally-modified (merged clean)` so the adopter sees their
        # customizations were preserved across the merge.  When the
        # merge resolved cleanly AND the on-disk file differs from the
        # *token-substituted* base, the adopter had customized this
        # file beyond the install-time substitution, and those
        # customizations rode through the merge.  The substituted
        # comparison is critical -- a plain ``ours != base_raw`` check
        # would flag every normally-installed file (where ours has
        # ``Demo`` for ``{{project_name}}`` but base_raw still has the
        # token) as "locally modified," which is the wrong signal.
        kind = res.status
        if kind == "clean" and ours != substitute_tokens(base_sized, tokens):
            kind = "clean-locally-modified"
        advancing = kind in _ADVANCING_KINDS
        plans.append(FilePlan(
            dst, kind,
            res.merged if advancing else None, res.detail,
            theirs_raw if advancing else None,
            cache_rel if advancing else None))

    # New core-like files (#47): core + skills install unconditionally, so a
    # core/skills file present upstream but absent from the lockfile (an
    # adopter whose lockfile predates it -- e.g. the lifecycle skills, added
    # after a pre-skills install) is brought in, not silently omitted. Modules
    # stay opt-in (the new_modules flow below); only the unconditional tier
    # auto-adds. Restricting to the known core/skills mapping set keeps --apply
    # from ever writing a path outside it (plan-review safety note).
    # Key on the *source* template, not the dst: an adopter may have installed a
    # core file under a renamed dst (the vendor wrapper VENDOR.md -> CLAUDE.md,
    # #45), so a src already tracked under any dst is NOT new -- keying on dst
    # would spuriously re-add VENDOR.md alongside the renamed CLAUDE.md.
    lock_srcs = {rec.get("src") for rec in lock.get("files", [])}
    core_like = [(s, d, False) for s, d in _CORE_MAPPINGS] + list(_SKILLS_MAPPINGS)
    seen_new: set[str] = set()
    for src_rel, dst_rel, verbatim in core_like:
        if src_rel in lock_srcs or dst_rel in seen_new:
            continue
        theirs_b = _theirs_bytes(cairn_root, templates_root, src_rel, to_ref)
        if theirs_b is None:
            continue
        seen_new.add(dst_rel)
        if verbatim:
            plans.append(FilePlan(
                dst_rel, "new-core", theirs_b.decode("utf-8", "replace"),
                "new core-like file (added)", None, None,
                src=src_rel, verbatim=True))
        else:
            theirs_raw = theirs_b.decode("utf-8")
            # Profile-size a newly-added core-like file too (P3); base cache
            # (5th field) keeps the full/unsized raw template.
            applied = substitute_tokens(theirs_raw, tokens)
            if new_axes:
                applied = strip_conditional_regions(applied, new_axes)
            plans.append(FilePlan(
                dst_rel, "new-core", applied,
                "new core-like file (added)", theirs_raw,
                f"{_BASE_CACHE_REL}/{dst_rel}", src=src_rel, verbatim=False))

    # New module-internal files: a module the adopter has ALREADY adopted
    # (``M in lock["modules"]``) may have GAINED files upstream since install --
    # the facade+package split case (a single tracked tool file became a thin
    # facade beside a sibling engine package). Unlike a brand-new module (the
    # opt-in ``new_modules`` structural flow below), the adopter already chose
    # ``M``, so it is owed ``M``'s new files. The write-set stays bounded to
    # ``_MODULE_MAPPINGS[M]`` (a hard-coded mapping set) -- the same safety the
    # core/skills restriction guarantees, extended to already-adopted modules.
    lock_modules = set(lock.get("modules", []))
    # F4 (External Security review): a destination claimed by more than one of
    # the selected core / skills / adopted-module InstallSpecs is a mapping bug
    # -- refuse it globally, before any per-file detection, independent of
    # lock/source state (so a duplicate hidden by source-absence or processing
    # order cannot slip through).
    _assert_mapping_ownership(lock_modules)
    lock_dsts = {rec["dst"] for rec in lock.get("files", [])}
    for mod in sorted(lock_modules):
        for spec in _MODULE_MAPPINGS.get(mod, []):
            # Canonical lockfile source key (matches install's
            # ``f"modules/{spec.src}"`` -- the lockfile namespace, NOT the
            # module-relative ``InstallSpec.src``): used for BOTH the
            # new-upstream test and the recorded lockfile entry.
            canonical_src = f"modules/{spec.src}"
            if canonical_src in lock_srcs:
                continue  # already tracked -> not a new-upstream addition
            dst_rel = spec.dst
            theirs_b = _theirs_bytes(
                cairn_root, templates_root, canonical_src, to_ref)
            if theirs_b is None:
                continue
            seen_new.add(dst_rel)
            # F3 (External Security review): under an explicit ``--to <ref>``,
            # structural additions are enumerated from the *running* engine's
            # registry, which need not match ``to_ref``. A pending addition is a
            # HARD BLOCK, never a silent skip -- otherwise an explicit-ref upgrade
            # could advance an already-tracked facade while omitting the package
            # it imports (the exact broken state this change exists to close).
            # Run scaffold from the target tree (``to_ref is None``) to carry them.
            if to_ref is not None:
                plans.append(FilePlan(
                    dst_rel, "new-module-blocked", None,
                    f"module-internal addition for {mod!r} cannot be carried "
                    f"under --to {to_ref!r}; run scaffold from the target tree",
                    None, None))
                continue
            # Text-only contract: a non-UTF-8 module InstallSpec fails crisply
            # rather than being decoded with U+FFFD replacement characters
            # (binary module files are out of scope).
            try:
                theirs_text = theirs_b.decode("utf-8")
            except UnicodeDecodeError:
                plans.append(FilePlan(
                    dst_rel, "error", None,
                    "module-internal addition is not UTF-8 text "
                    "(binary module files are out of scope)", None, None))
                continue
            # F2 (External Security review): a genuinely-new spec whose
            # destination already exists OUTSIDE the lockfile is a HARD BLOCK in
            # its own kind that the generic ``--ack-review-only`` switch CANNOT
            # bypass. A plain review-only item would let apply advance the lock +
            # install the siblings while leaving this file importable but
            # unattested. Two distinct provenance states (R3/R5 -- not the same):
            # a destination already tracked under ANOTHER lockfile source is an
            # ownership conflict adoption never clears (its own kind); an
            # occupied-UNLOCKED regular file is an adoptable fork
            # (`upgrade --adopt-collisions`) -- it carries src+verbatim so the
            # adopt path can record it (and re-verifies regular+contained).
            dst_abs_collide = target / dst_rel
            if dst_rel in lock_dsts:
                plans.append(FilePlan(
                    dst_rel, "new-module-lockconflict", None,
                    "module-internal addition's destination is already tracked "
                    "under another lockfile source (provenance conflict); resolve "
                    "by hand", theirs_text, None))
                continue
            if dst_abs_collide.exists():
                adoptable = (dst_abs_collide.is_file()
                             and not dst_abs_collide.is_symlink())
                plans.append(FilePlan(
                    dst_rel, "new-module-blocked", None,
                    "module-internal addition collides with an existing unlocked "
                    "destination; keep it as a tracked fork "
                    "(`upgrade --adopt-collisions`) or reconcile by hand, then "
                    "re-stage", theirs_text, None,
                    src=(canonical_src if adoptable else None),
                    verbatim=spec.verbatim))
                continue
            # Absent destination -> a clean module-internal add. Verbatim vs
            # mergeable mirrors the new-core branch above.
            if spec.verbatim:
                plans.append(FilePlan(
                    dst_rel, "new-module", theirs_text,
                    "new module-internal file (added)", None, None,
                    src=canonical_src, verbatim=True))
            else:
                applied = substitute_tokens(theirs_text, tokens)
                if new_axes:
                    applied = strip_conditional_regions(applied, new_axes)
                plans.append(FilePlan(
                    dst_rel, "new-module", applied,
                    "new module-internal file (added)", theirs_text,
                    f"{_BASE_CACHE_REL}/{dst_rel}",
                    src=canonical_src, verbatim=False))

    # Structural reconciliation.
    current_modules = set(_MODULE_MAPPINGS)
    structural = {
        "new_modules": sorted(current_modules - lock_modules),
        "removed_modules": sorted(lock_modules - current_modules),
    }
    return plans, structural


def _citation_ok(target: Path, lock: dict[str, Any]) -> bool | None:
    """R10: if the target carries a fidelity manifest, does it cite the
    current lockfile version/commit?  None if no manifest to check.  Uses the
    shared `_find_manifest_path` (dev/.cairn/ first, legacy dev/strategy/
    fallback) and emits the same migration advisory `init-lock` does."""
    found = _find_manifest_path(target)
    if found is None:
        return None
    manifest, is_legacy = found
    if is_legacy:
        _warn_legacy_manifest_home(manifest)
    text = manifest.read_text(encoding="utf-8", errors="replace")
    commit = str(lock.get("cairn_commit", ""))
    version = str(lock.get("cairn_version", ""))
    return (commit and commit in text) or (version and version in text)


def _print_upgrade_report(
    plans: list[FilePlan], structural: dict[str, Any],
    citation: bool | None, *, mode: str, drift: str | None = None,
) -> None:
    import collections
    by_kind: dict[str, list[str]] = collections.defaultdict(list)
    for fp in plans:
        by_kind[fp.kind].append(fp.dst)
    print(f"\nCairn upgrade -- {mode}\n" + "=" * 40)
    if drift:
        print(f"  {drift}")
    order = ["clean", "clean-locally-modified", "new-core",
             "conflict", "slot-removed", "review-only",
             "verbatim-update", "verbatim-locally-modified",
             "verbatim-up-to-date", "verbatim-missing", "up-to-date",
             "removed-upstream", "error"]
    # Column width sized for the longest display label ("locally-modified
    # (merged clean)" = 31 chars) plus a 2-space pad.
    label_width = max(len(_KIND_DISPLAY_LABEL.get(k, k)) for k in order) + 2
    for kind in order + [k for k in by_kind if k not in order]:
        if kind in by_kind:
            label = _KIND_DISPLAY_LABEL.get(kind, kind)
            print(f"  {label:{label_width}s} {len(by_kind[kind])}: "
                  f"{', '.join(by_kind[kind][:6])}"
                  f"{'...' if len(by_kind[kind]) > 6 else ''}")
    if structural["new_modules"]:
        print(f"\n  new modules available (opt-in): "
              f"{', '.join(structural['new_modules'])}")
    if structural["removed_modules"]:
        print(f"  modules removed upstream (flagged): "
              f"{', '.join(structural['removed_modules'])}")
    if citation is False:
        print("\n  [warn] the fidelity manifest does NOT cite the current "
              "lockfile version/commit (R10) -- update its citation.")
    conflicts = [fp.dst for fp in plans if fp.kind == "conflict"]
    flags = [fp for fp in plans if fp.kind in
             ("slot-removed", "verbatim-locally-modified", "error")]
    if conflicts:
        print(f"\n  {len(conflicts)} file(s) need conflict resolution before "
              "--apply.")
    for fp in flags:
        print(f"  [flag] {fp.dst}: {fp.detail}")
    # Review-only files owe a by-hand merge: the upgrade is NOT complete until
    # each is reconciled against the new upstream.  Surface them per-file with
    # the reason (not just the summary count) + the concrete next step, so an
    # adopter cannot read "review-only: N" as "done".
    review_only = [fp for fp in plans if fp.kind == "review-only"]
    if review_only:
        print("\n  ⚠ manual merge owed -- the upgrade is NOT complete "
              "until these are reconciled against the new upstream:")
        for fp in review_only:
            print(f"      {fp.dst}: {fp.detail}")
        print(f"  next step: `upgrade --stage` writes each file's upstream "
              f"version (+ your current copy) under "
              f"{_STAGING_REL}/review-only/ for a by-hand merge; `--apply` "
              f"fail-closes until they are reconciled "
              f"(override: --ack-review-only).")


def _seed_staging_gitignore(target: Path) -> None:
    seed_gitignore(target, (_STAGING_REL + "/",))


def _write_stage(
    target: Path, plans: list[FilePlan], lock: dict[str, Any],
    to_ref: str | None, cairn_root: Path,
    new_profile: dict[str, Any] | None = None,
) -> Path:
    """Write the staged review surface into the ephemeral, gitignored
    staging dir; return its path.

    Stages **only advancing kinds** (clean / conflict / verbatim-update) --
    a flagged/non-advancing file is reported but never staged, so it can
    never be applied.  Also stages the **new
    base-template** for each advancing mergeable file (under ``new-base/``)
    + the new version/commit in metadata, so ``--apply`` can advance the
    lockfile + base cache without needing the Cairn source again."""
    import json
    import shutil
    stage = target / _STAGING_REL
    # F1 round 2 (External Security review): guard the STAGE ROOT itself BEFORE
    # the first rmtree / mkdir. If ``target/dev`` is a symlink to an external
    # directory, ``shutil.rmtree(stage)`` / ``stage.mkdir(...)`` would FOLLOW it
    # and delete/recreate that external dir -- a containment escape the per-plan
    # guard below catches only AFTER the damage. ``_assert_safe_write`` refuses a
    # symlinked parent (``target/dev``) here, before any mutation.
    _assert_safe_write(stage, target)
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)
    # F1 (External Security review): validate EVERY planned destination is a
    # contained relative path BEFORE any stage / new-base / review-only write.
    # The stage write paths derive from ``fp.dst``; a malformed (absolute or
    # ``..``-traversing) hard-coded InstallSpec.dst would otherwise escape the
    # staging tree AND the adopter root during --stage, before the apply-time
    # swap guard can help. ``_assert_safe_write`` refuses absolute paths,
    # traversal, and symlink-parent escapes (ScaffoldSecurityError, caught at the
    # CLI top level, exit 2).
    for fp in plans:
        _assert_safe_write(target / fp.dst, target)
    staged_files: list[str] = []
    ours_hashes: dict[str, str] = {}
    expected_absent: set[str] = set()
    kinds: dict[str, str] = {}
    # #47: per-file provenance for files NOT already in the lockfile (new-core),
    # so --apply can append correct lockfile records (refs only -- no file
    # bodies -- keeping stage-metadata.json lightweight, plan-review rec 4b).
    new_entries: dict[str, dict[str, Any]] = {}
    for fp in plans:
        if fp.kind not in _ADVANCING_KINDS or fp.applied is None:
            continue
        dst_abs = target / fp.dst
        # Skip a genuine no-op (the applied content already on disk).
        if dst_abs.exists() and \
                dst_abs.read_text(encoding="utf-8") == fp.applied:
            continue
        out = stage / "files" / fp.dst
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fp.applied, encoding="utf-8")
        staged_files.append(fp.dst)
        kinds[fp.dst] = fp.kind
        if fp.kind in ("new-core", "new-module"):
            new_entries[fp.dst] = {
                "src": fp.src, "verbatim": fp.verbatim,
                "base_cache": fp.base_cache,
            }
        # Snapshot the on-disk *ours* hash at stage time (R7a: detect an
        # adopter edit made between --stage and --apply).
        if dst_abs.exists():
            ours_hashes[fp.dst] = "sha256:" + _sha256_hex(dst_abs.read_bytes())
        else:
            # A new add (new-core / new-module): its destination was absent at
            # --stage, so it carries no ours_hashes snapshot. Record it so
            # --apply fails closed if the destination APPEARED since (the data-
            # loss guard, hardening the shared new-file path).
            expected_absent.add(fp.dst)
        # Stage the new base-template content (mergeable files only).
        if fp.theirs_raw is not None and fp.base_cache:
            nb = stage / "new-base" / fp.dst
            nb.parent.mkdir(parents=True, exist_ok=True)
            nb.write_text(fp.theirs_raw, encoding="utf-8")
    # Review-only files (no recoverable base / missing on disk) get a by-hand
    # review pair in a SIBLING ``review-only/`` dir -- deliberately NOT under
    # ``files/``, which ``--apply`` swaps onto disk + checks for exactness
    # (placing side-files there would trip that safety gate).  ``.theirs`` is
    # the new upstream; ``.ours`` is the current on-disk copy, omitted when
    # the file is missing on disk (nothing to pair).  ``--apply`` never
    # advances these; the whole stage (incl. ``review-only/``) is rmtree'd on
    # apply.
    review_only_dsts: list[str] = []
    for fp in plans:
        if fp.kind != "review-only":
            continue
        review_only_dsts.append(fp.dst)
        if fp.theirs_raw is not None:
            theirs_out = stage / "review-only" / (fp.dst + ".theirs")
            theirs_out.parent.mkdir(parents=True, exist_ok=True)
            theirs_out.write_text(fp.theirs_raw, encoding="utf-8")
        dst_abs = target / fp.dst
        if dst_abs.exists():
            ours_out = stage / "review-only" / (fp.dst + ".ours")
            ours_out.parent.mkdir(parents=True, exist_ok=True)
            ours_out.write_text(
                dst_abs.read_text(encoding="utf-8"), encoding="utf-8")
    # F2 / F3 (External Security review): new-module-blocked items -- an occupied
    # destination collision, or a structural addition pending under an explicit
    # ``--to`` -- are HARD blocks. They are recorded DISTINCTLY (not folded into
    # review_only) so --apply fails closed UNCONDITIONALLY: the generic
    # ``--ack-review-only`` override cannot bypass them. Stage the .theirs/.ours
    # pair (when content is available) so the adopter can reconcile by hand.
    module_blocked_dsts: list[str] = []
    collision_adopt: dict[str, dict[str, Any]] = {}
    for fp in plans:
        if fp.kind not in ("new-module-blocked", "new-module-lockconflict"):
            continue
        module_blocked_dsts.append(fp.dst)
        if fp.theirs_raw is not None:
            theirs_out = stage / "review-only" / (fp.dst + ".theirs")
            theirs_out.parent.mkdir(parents=True, exist_ok=True)
            theirs_out.write_text(fp.theirs_raw, encoding="utf-8")
        dst_abs = target / fp.dst
        if dst_abs.exists():
            ours_out = stage / "review-only" / (fp.dst + ".ours")
            ours_out.parent.mkdir(parents=True, exist_ok=True)
            ours_out.write_text(
                dst_abs.read_text(encoding="utf-8"), encoding="utf-8")
        # Adoptable-collision manifest (R2): bind a later `--adopt-collisions` to
        # exactly this dst + the bytes --stage observed. Only an occupied-UNLOCKED
        # `new-module-blocked` that carries a canonical src AND is a present
        # regular (non-symlink) file is adoptable; a lock-conflict never is.
        if (fp.kind == "new-module-blocked" and fp.src
                and dst_abs.is_file() and not dst_abs.is_symlink()):
            collision_adopt[fp.dst] = {
                "src": fp.src, "verbatim": bool(fp.verbatim),
                "observed_hash": "sha256:" + _sha256_hex(dst_abs.read_bytes()),
            }
    # #48: a verbatim file already byte-identical to the new upstream
    # (verbatim-up-to-date) but whose lockfile hash is stale -- the adopter
    # hand-synced it to a later Cairn before upgrading. Record it so --apply
    # heals the lock hash (no content swap; the file is already correct on
    # disk, so it never enters staged_files / the exactness gate).
    lock_by_dst = {r["dst"]: r for r in lock.get("files", [])}
    verbatim_rehash: list[str] = []
    for fp in plans:
        if fp.kind != "verbatim-up-to-date":
            continue
        rec = lock_by_dst.get(fp.dst)
        dst_abs = target / fp.dst
        if rec is None or not dst_abs.exists():
            continue
        if "sha256:" + _sha256_hex(dst_abs.read_bytes()) != rec.get("hash"):
            verbatim_rehash.append(fp.dst)
    meta = {
        "lock_commit": lock.get("cairn_commit"),
        "lock_version": lock.get("cairn_version"),
        "to_ref": to_ref,
        "tokens": lock.get("tokens"),
        "modules": lock.get("modules"),
        "new_version": _cairn_version(cairn_root),
        "new_commit": to_ref or _cairn_commit(cairn_root),
        "staged_files": sorted(staged_files),
        "kinds": kinds,
        "ours_hashes": ours_hashes,
        # New-add destinations that were ABSENT at --stage; --apply fails closed
        # if any reappeared since (data-loss guard for new-core / new-module).
        "expected_absent": sorted(expected_absent),
        # Outstanding by-hand merges: --apply fail-closes on a non-empty list
        # unless --ack-review-only is passed (#44 completion gate).
        "review_only": sorted(review_only_dsts),
        # F2/F3: occupied-collision / pending-under-`--to` module additions --
        # --apply fails closed UNCONDITIONALLY (no --ack-review-only bypass).
        "module_blocked": sorted(module_blocked_dsts),
        # Adoptable occupied-unlocked collisions -> {dst: {src, verbatim,
        # observed_hash}}, bound so `--adopt-collisions` records exactly the
        # reviewed set + bytes (R2). A lock-conflict block is NOT listed here.
        "collision_adopt": collision_adopt,
        # #47 new core-like files to record in the lockfile on apply (refs only).
        "new_entries": new_entries,
        # #48 verbatim files whose stale lock hash --apply should heal.
        "verbatim_rehash": sorted(verbatim_rehash),
        # S1: the adopter's CURRENT resolved profile, so --apply re-embeds it in
        # the advanced lockfile when the profile changed since install (keeps the
        # embedded profile consistent with the now-resized on-disk files).
        "new_profile": new_profile,
    }
    (stage / _STAGE_META).write_text(
        json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")
    _seed_staging_gitignore(target)
    return stage


def _resolve_vendor_wrapper(
    target: Path, mapped_dsts: set[str],
) -> str | None:
    """Resolve the adopter's renamed vendor wrapper (foldback #45).

    Cairn installs the thin wrapper as ``VENDOR.md`` and the adopter renames it
    to their tool's file (``CLAUDE.md`` etc.), so on a renamed tree the install
    dst ``VENDOR.md`` is missing and the wrapper would drop to untracked.  Two-
    tier resolution (plan-review S1), first hit wins:

    * **Tier 1 (name):** a repo-root file named in ``_KNOWN_VENDOR_WRAPPERS``
      that is not already a mapped core/module dst -> resolved, with **no
      content check** (a heavily customized wrapper may have dropped the
      ``@AGENTS.md`` import line, and the name alone is a strong signal).
    * **Tier 2 (content):** else a repo-root ``*.md`` (not already mapped)
      whose first few lines carry the ``@AGENTS.md`` import -> resolved (a
      custom-named wrapper).

    Returns the repo-root-relative dst, or ``None`` (the caller warns rather
    than silently skipping or recording a wrong file).  The not-already-mapped
    guard (both tiers) is the false-positive backstop."""
    # Tier 1: a known vendor filename at repo root.
    for name in _KNOWN_VENDOR_WRAPPERS:
        if name not in mapped_dsts and (target / name).is_file():
            return name
    # Tier 2: a custom-named root .md importing @AGENTS.md near the top.
    for md in sorted(target.glob("*.md")):
        if md.name in mapped_dsts or not md.is_file():
            continue
        head = md.read_text(encoding="utf-8", errors="replace").splitlines()[:5]
        if any("@AGENTS.md" in line for line in head):
            return md.name
    return None


def _find_manifest_path(target: Path) -> tuple[Path, bool] | None:
    """Locate the adopter's fidelity manifest, searching `dev/.cairn/` first
    (the canonical adoption-state home), then the legacy `dev/strategy/`. Returns
    ``(path, is_legacy)`` or ``None``. The single manifest-finder shared by the
    `cairn_commit` recovery (B1) and the R10 citation check, so the two cannot
    diverge on which file is the manifest."""
    for idx, rel in enumerate(_MANIFEST_SEARCH_DIRS):
        d = target / rel
        if not d.is_dir():
            continue
        cands = sorted(
            {c for c in list(d.glob("*fidelity*")) + list(d.glob("*manifest*"))
             if c.is_file()})
        if cands:
            return cands[0], idx > 0
    return None


def _warn_legacy_manifest_home(manifest: Path) -> None:
    """The shared migration advisory emitted whenever a manifest is found in the
    legacy `dev/strategy/` home (by either the citation check or `init-lock`)."""
    print(f"  [advisory] fidelity manifest found in the legacy `dev/strategy/` "
          f"home ({manifest.name}); move it to `dev/.cairn/` (the adoption-state "
          "home).", file=sys.stderr)


def _manifest_cairn_commit(target: Path) -> str:
    """Best-effort ``cairn_commit`` recovered from the fidelity manifest, or
    ``"unknown"`` (B1: `dev/.cairn/` first, legacy `dev/strategy/` fallback with
    a migration advisory)."""
    found = _find_manifest_path(target)
    if found is None:
        return "unknown"
    path, is_legacy = found
    if is_legacy:
        _warn_legacy_manifest_home(path)
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r'\s*cairn_commit\s*:\s*"?([0-9a-f]{7,40})"?', line)
        if m:
            return m.group(1)
    return "unknown"


def _infer_init_lock_axes(target: Path) -> dict[str, str]:
    """Structurally-inferable axis prefill for `init-lock` (R3 + S1): the axes a
    tree's installed modules / files determine. `size` / `complexity` are human
    judgments, left as placeholders."""
    def _mod(name: str) -> bool:
        return (target / "dev" / "modules" / f"{name}.md").is_file()
    axes: dict[str, str] = {}
    if _mod("dual-review"):
        axes["agent_team"] = "concurrent-multi-type"
    elif _mod("coordination-tiers"):
        axes["agent_team"] = "concurrent-single-type"
    else:
        axes["agent_team"] = "single"
    axes["human_team"] = (
        "small-multi" if (target / "CONTRIBUTING.md").is_file() else "solo")
    axes["language"] = "multi" if _mod("dual-language-tests") else "single"
    axes["age"] = "legacy" if _mod("legacy-agent") else "greenfield"
    return axes


#: Axes `init-lock` cannot structurally infer -- the operator fills these between
#: the two runs (R2). Each placeholder names its allowed values.
_AXIS_PLACEHOLDERS: dict[str, str] = {
    "size": "<small|medium|large>",
    "complexity": "<simple|moderate|complex>",
}
_INIT_LOCK_TOKEN_PLACEHOLDERS: dict[str, str] = {
    "project_name": "<your project name>",
    "test_command": "<your test command, e.g. pytest>",
}


def _resolve_lock_profile_fields(
    cfg: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, str], list[str], dict[str, str]]:
    """From a parsed profile config, build the lockfile ``profile`` block + token
    map, and report *missing* / *invalid* axes (validated against ``_AXES`` --
    S2). Mirrors the install path so a `init-lock`'d lockfile matches a
    `--config` one. Raises ``PresetError`` on an unknown preset."""
    tokens = {k: str(v) for k, v in cfg.items()
              if isinstance(k, str) and k in KNOWN_TOKENS and v}
    if cfg.get("preset"):
        resolved: dict[str, Any] = dict(resolve_axes(str(cfg["preset"]), cfg))
    else:
        resolved = {a: cfg.get(a) for a in _AXES if cfg.get(a) is not None}
    missing = [a for a in _AXES if not resolved.get(a)]
    invalid = {a: str(resolved[a]) for a in _AXES
               if resolved.get(a) is not None and str(resolved[a]) not in _AXES[a]}
    lock_profile: dict[str, Any] = {
        "preset": cfg.get("preset"),
        "axes": {a: resolved[a] for a in _AXES if resolved.get(a) is not None},
    }
    return lock_profile, tokens, missing, invalid


def _write_init_lock_profile_template(target: Path) -> int:
    """First `init-lock` run with no committed config: write a
    ``dev/.cairn/profile.yml`` prefilled with the structurally-inferable axes +
    placeholders for the rest, then **fail loud** (exit non-zero, no lockfile) so
    the operator completes it and re-runs (R2 step 1)."""
    profile_path = target / _PROFILE_REL
    inferred = _infer_init_lock_axes(target)
    modules = sorted(m for m in _MODULE_MAPPINGS
                     if (target / "dev" / "modules" / f"{m}.md").is_file())
    lines = [
        "# Cairn install-config (profile.yml).",
        "# Materialized by `upgrade --init-lock`: structurally-inferable axes are",
        "# prefilled; replace every <...> placeholder with a real value, then",
        "# re-run `upgrade --init-lock` to write the lockfile.",
        "",
        f'project_name: "{_INIT_LOCK_TOKEN_PLACEHOLDERS["project_name"]}"',
        f'test_command: "{_INIT_LOCK_TOKEN_PLACEHOLDERS["test_command"]}"',
        "",
        "# Six-axis dimension profile (all required):",
    ]
    for a in _AXES:
        if a in inferred:
            lines.append(f"{a}: {inferred[a]}")
        else:
            lines.append(f"{a}: {_AXIS_PLACEHOLDERS[a]}")
    lines += ["", "# Installed modules (inferred from dev/modules/):", "modules:"]
    lines += [f"  - {m}" for m in modules]
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    n_ph = len(_AXIS_PLACEHOLDERS) + len(_INIT_LOCK_TOKEN_PLACEHOLDERS)
    print(
        f"Wrote {_PROFILE_REL}: {len(inferred)} axis(es) inferred, {n_ph} "
        "placeholder(s) to fill (project_name, test_command, "
        f"{', '.join(_AXIS_PLACEHOLDERS)}).\n"
        "  Replace every <...> value, then re-run `upgrade --init-lock`. "
        "No lockfile was written (fail-with-template).",
        file=sys.stderr,
    )
    return 2


def _cmd_init_lock(
    target: Path, cairn_root: Path, templates_root: Path,
) -> int:
    """`upgrade --init-lock` (R6/I3): synthesize a lockfile for a
    pre-lockfile tree from on-disk content + the fidelity manifest.

    Token-substituted files have **no recoverable token values** (the
    manifest records names, not values, I3) -> classified
    *unrecoverable-base* and handled review-only on later upgrades, never a
    pretended 3-way merge.  Verbatim scripts record their on-disk hash."""
    if read_lockfile(target) is not None:
        print(f"  [info] {_LOCKFILE_REL} already exists; nothing to migrate.",
              file=sys.stderr)
        return 0
    # Arm A (init-lock-full-profile): resolve the full six-axis profile + tokens
    # so the synthesized lockfile is never a gating-only stub. With no committed
    # config, fail-with-template (R2); with one, validate it (S2) before use.
    profile_path = target / _PROFILE_REL
    if not profile_path.is_file():
        return _write_init_lock_profile_template(target)
    try:
        cfg = load_config(profile_path)
    except Exception as exc:  # noqa: BLE001 -- surface any YAML/read error
        print(f"error loading {_PROFILE_REL}: {exc}", file=sys.stderr)
        return 1
    try:
        lock_profile, tokens, missing, invalid = _resolve_lock_profile_fields(cfg)
    except PresetError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    placeholder_tokens = sorted(
        k for k, v in tokens.items()
        if v.strip().startswith("<") and v.strip().endswith(">"))
    if missing or invalid or placeholder_tokens:
        parts: list[str] = []
        if missing:
            parts.append(f"missing axis(es): {', '.join(missing)}")
        if invalid:
            parts.append("invalid axis value(s): " + ", ".join(
                f"{a}={v!r} (allowed: {'/'.join(_AXES[a])})"
                for a, v in invalid.items()))
        if placeholder_tokens:
            parts.append(
                f"unfilled placeholder(s): {', '.join(placeholder_tokens)}")
        print(f"error: {_PROFILE_REL} is incomplete -- " + "; ".join(parts) +
              ".\n  Fill every value (axes validated against their allowed "
              "values), then re-run `upgrade --init-lock`.", file=sys.stderr)
        return 1
    # cairn_commit recovery (B1: dev/.cairn/ first, legacy dev/strategy/ fallback).
    commit = _manifest_cairn_commit(target)
    records: list[dict[str, Any]] = []
    classification: dict[str, list[str]] = {"verbatim": [], "unrecoverable-base": []}
    entries = _lock_file_list(list(_MODULE_MAPPINGS), [])
    mapped_dsts = {dst for _src, dst, _vb in entries}
    for src_rel, dst_rel, verbatim in entries:
        dst_abs = target / dst_rel
        if not dst_abs.exists():
            # The vendor wrapper installs as VENDOR.md but the adopter renames
            # it to their tool's file (#45).  Follow the rename so it stays
            # tracked + 3-way merges later, instead of dropping it to untracked.
            if src_rel == "core/VENDOR.md":
                resolved = _resolve_vendor_wrapper(target, mapped_dsts)
                if resolved is None:
                    print(f"  [warn] vendor wrapper {dst_rel} installed but no "
                          "renamed wrapper found at repo root (a known vendor "
                          f"filename {', '.join(_KNOWN_VENDOR_WRAPPERS)}, or a "
                          "root *.md importing @AGENTS.md) -- it will be "
                          "untracked. Rename it to a known vendor filename or "
                          "re-install from an upgrade-capable Cairn.",
                          file=sys.stderr)
                    continue
                dst_rel = resolved
                dst_abs = target / dst_rel
            else:
                continue
        h = "sha256:" + _sha256_hex(dst_abs.read_bytes())
        rec: dict[str, Any] = {"src": src_rel, "dst": dst_rel,
                               "verbatim": verbatim, "hash": h}
        if verbatim:
            classification["verbatim"].append(dst_rel)
        else:
            # No token values -> base not reconstructable (I3); no base_cache.
            rec["unrecoverable_base"] = True
            classification["unrecoverable-base"].append(dst_rel)
        records.append(rec)
    lock = {
        "schema": _LOCK_SCHEMA, "migrated": True,
        "cairn_version": _cairn_version(cairn_root), "cairn_commit": commit,
        "profile": lock_profile, "modules": sorted(
            m for m in _MODULE_MAPPINGS
            if (target / "dev" / "modules" / f"{m}.md").exists()),
        "optional_templates": [], "tokens": dict(tokens), "files": records,
    }
    lock_path = target / _LOCKFILE_REL
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(_emit_lock_yaml(lock), encoding="utf-8")
    print(f"Wrote migrated {_LOCKFILE_REL} ({len(records)} files).")
    print(f"  verbatim scripts (hash-tracked): "
          f"{len(classification['verbatim'])}")
    print(f"  token-substituted files (no recoverable base -> review-only "
          f"on upgrade, per I3): {len(classification['unrecoverable-base'])}")
    print("  NOTE: a migrated lockfile cannot 3-way-merge token-substituted "
          "files (the install token values were never recorded); those "
          "upgrade as a review-only diff. Re-install from an "
          "upgrade-capable Cairn for clean merges.")
    return 0


def _record_fork_entry(
    target: Path, src_rel: str, dst_rel: str, verbatim: bool,
    upstream_bytes: bytes,
) -> tuple[dict[str, Any], tuple[Path, bytes] | None]:
    """Build a lockfile ``files`` record for an **on-disk** file tracked as an
    adopter fork, plus any base-cache write it needs (returned, NOT performed --
    the caller batches an all-or-nothing preflight + atomic commit).

    Records ``hash`` from the on-disk bytes (integrity) **and** ``base_hash``
    from the upstream-at-record bytes (fork detection) for BOTH verbatim and
    mergeable specs -- so ``classify_verbatim`` / the 3-way merge see the
    adopter's divergence as ``locally-modified``, never ``update``
    (safe-to-overwrite). This is the External Security review R1 fix:
    recording only the on-disk ``hash`` for a verbatim fork makes its own hash
    the comparison baseline, so a later upstream change classifies ``update``
    and the fork is silently overwritten. A mergeable spec also caches the raw
    upstream template at ``base_cache`` (the merge ancestor); a verbatim spec
    records ``base_hash`` only (the hash policy, no cached file -- parity with
    ``write_install_lockfile``). The destination must already exist on disk."""
    dst_abs = target / dst_rel
    rec: dict[str, Any] = {
        "src": src_rel, "dst": dst_rel, "verbatim": bool(verbatim),
        "hash": "sha256:" + _sha256_hex(dst_abs.read_bytes()),
        "base_hash": "sha256:" + _sha256_hex(upstream_bytes),
    }
    if verbatim:
        return rec, None
    base_rel = f"{_BASE_CACHE_REL}/{dst_rel}"
    rec["base_cache"] = base_rel
    return rec, (target / base_rel, upstream_bytes)


def _commit_lock_and_caches(
    target: Path, lock: dict[str, Any],
    cache_writes: list[tuple[Path, bytes]],
) -> None:
    """All-or-nothing commit of a set of base-cache writes + the lockfile
    authority (External Security review R4). **Preflight** containment of every
    write path (``_assert_safe_write`` -- including the lockfile itself, which
    ``_cmd_adopt_module`` previously wrote unguarded), then stage every write to
    a temp path, and only then **replace** the caches and -- LAST -- the
    lockfile via an atomic ``os.replace``. A failure during preflight or temp
    staging leaves the authoritative lockfile (and the prior caches) unchanged;
    the lockfile is the integrity authority and is swapped last."""
    import os
    lock_path = target / _LOCKFILE_REL
    # Preflight: containment of every destination BEFORE any write.
    for cache_path, _raw in cache_writes:
        _assert_safe_write(cache_path, target)
    _assert_safe_write(lock_path, target)
    # Stage every write to a temp sibling first -- no live file touched yet, so a
    # failure here leaves everything unchanged (nothing has been replaced).
    pending: list[tuple[Path, Path]] = []
    for cache_path, raw in cache_writes:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = cache_path.with_name(cache_path.name + ".tmp")
        _assert_safe_write(tmp, target)
        tmp.write_bytes(raw)
        pending.append((tmp, cache_path))
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_tmp = lock_path.with_name(lock_path.name + ".tmp")
    _assert_safe_write(lock_tmp, target)
    lock_tmp.write_text(_emit_lock_yaml(lock), encoding="utf-8")
    # Commit: replace the caches, then the lockfile LAST (each os.replace atomic).
    for tmp, final in pending:
        os.replace(tmp, final)
    os.replace(lock_tmp, lock_path)


def _cmd_adopt_module(
    target: Path, name: str, cairn_root: Path, templates_root: Path,
) -> int:
    """`upgrade --adopt-module <name>` (#49): record an already-on-disk opt-in
    module into the lockfile so it 3-way-merges on later upgrades.

    Explicit, never automatic (modules are a deliberate choice -- the opt-in
    contrast to #47's auto-add of the unconditional core/skills tier). For each
    of the module's ``InstallSpec``s it records a lockfile ``files`` entry
    exactly as ``init`` would (``src``/``dst``/``verbatim``, on-disk ``hash``;
    non-verbatim -> ``base_cache`` raw template + ``base_hash``), installing a
    spec's ``dst`` from the template first only if it is missing on disk. Adds
    the module to ``modules`` and seeds its ``.gitignore`` entries. Fail-closed
    on an unknown name; a no-op if the module is already locked."""
    lock = read_lockfile(target)
    if lock is None:
        print(f"error: no {_LOCKFILE_REL} in the target; run "
              "`upgrade --init-lock` (or a clean install) first.",
              file=sys.stderr)
        return 1
    if name not in _MODULE_MAPPINGS:
        print(f"error: unknown module {name!r}. Known modules: "
              f"{', '.join(sorted(_MODULE_MAPPINGS))}.", file=sys.stderr)
        return 1
    if name in lock.get("modules", []):
        print(f"  [info] module {name!r} is already recorded in "
              f"{_LOCKFILE_REL}; nothing to adopt.", file=sys.stderr)
        return 0

    tokens = {str(k): str(v) for k, v in (lock.get("tokens") or {}).items()}

    # Required-token preflight (security-apparatus-enrichment B0): adopting a
    # module whose required token is unfilled in the lockfile would install a
    # placeholder-bearing file and record it.  Fail closed BEFORE any write or
    # lockfile mutation.
    gaps = missing_required_tokens([name], tokens)
    if gaps:
        print(
            f"error: module {name!r} requires token(s) "
            f"{', '.join(sorted(t for _m, t in gaps))} but the lockfile has no "
            "filled value; refusing to adopt (no files written, lockfile "
            "unchanged). Fill the token (upgrade --init-lock) and retry.",
            file=sys.stderr,
        )
        return 2

    lock_dsts = {rec["dst"] for rec in lock.get("files", [])}
    new_files = [dict(rec) for rec in lock.get("files", [])]
    cache_writes: list[tuple[Path, bytes]] = []
    added: list[str] = []
    for spec in _MODULE_MAPPINGS[name]:
        src_rel = f"modules/{spec.src}"        # lockfile src convention
        dst_rel = spec.dst
        if dst_rel in lock_dsts:
            continue  # already tracked under another roster entry; skip the file
        theirs_b = _theirs_bytes(cairn_root, templates_root, src_rel, None)
        if theirs_b is None:
            print(f"error: upstream template {src_rel!r} for module {name!r} "
                  "not found.", file=sys.stderr)
            return 1
        dst_abs = target / dst_rel
        if not dst_abs.exists():
            # Adoption is for an already-present module; install a missing spec
            # dst from the template (substituted for mergeable, raw for verbatim)
            # exactly as `init` would, so a partially-placed module completes.
            _assert_safe_write(dst_abs, target)
            dst_abs.parent.mkdir(parents=True, exist_ok=True)
            content = (theirs_b.decode("utf-8", "replace") if spec.verbatim
                       else substitute_tokens(theirs_b.decode("utf-8"), tokens))
            dst_abs.write_text(content, encoding="utf-8")
        # Record via the shared fork primitive: base_hash = upstream for BOTH
        # verbatim and mergeable (R1 -- a verbatim adopt previously recorded no
        # base_hash, so a later upstream change classified `update` and
        # overwrote the adopter's file). The base-cache + lockfile writes are
        # committed once, atomically, after the loop (R4).
        rec, cache_write = _record_fork_entry(
            target, src_rel, dst_rel, bool(spec.verbatim), theirs_b)
        if cache_write is not None:
            cache_writes.append(cache_write)
        new_files.append(rec)
        added.append(dst_rel)

    lock["files"] = new_files
    lock["modules"] = sorted(set(lock.get("modules", [])) | {name})
    _commit_lock_and_caches(target, lock, cache_writes)
    seeded = seed_gitignore(target, _GITIGNORE_SEEDS.get(name, ()))
    note = f"; seeded .gitignore: {', '.join(seeded)}" if seeded else ""
    print(f"Adopted module {name!r}: recorded {len(added)} file(s) in "
          f"{_LOCKFILE_REL}{note}.")
    return 0


def _cmd_adopt_collisions(
    target: Path, cairn_root: Path, templates_root: Path, lock: dict[str, Any],
) -> int:
    """`upgrade --adopt-collisions`: record each occupied-destination collision
    a prior `--stage` surfaced as a tracked adopter **fork**, so the upgrade is
    no longer blocked on it and ``verify_integrity`` attests it. The adopter
    keeps their divergent file unchanged; the upstream template becomes its
    merge base (``base_hash``), so a later upgrade classifies it
    ``locally-modified`` -- surfaced, never silently overwritten.

    Bound to the staged set + bytes (R2): adoption requires a prior ``--stage``
    and refuses a collision that appeared or changed since. Eligibility (R3):
    canonical src absent from the lockfile, dst absent from lock records, a
    present regular contained on-disk file -- a lock-conflict block is never
    adoptable. All-or-nothing (R4): the FULL selected set is preflighted
    (containment, staged-hash, eligibility, upstream availability) before any
    mutation; then the base caches + lockfile are written guarded + atomic
    (lockfile last). It never writes the adopter's destination."""
    import json
    stage = target / _STAGING_REL
    meta_path = stage / _STAGE_META
    if not meta_path.exists():
        print("error: no staged upgrade found; run `upgrade --stage` first, "
              f"review the collisions under {_STAGING_REL}/review-only/, then "
              "`upgrade --adopt-collisions`.", file=sys.stderr)
        return 1
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    # Same staleness contract as --apply: the stage must reflect the current lock.
    if meta.get("lock_commit") != lock.get("cairn_commit") or \
            meta.get("tokens") != lock.get("tokens") or \
            meta.get("modules") != lock.get("modules"):
        print("error: staged upgrade is stale (lockfile/tokens/roster changed "
              "since --stage); re-run `upgrade --stage`.", file=sys.stderr)
        return 1
    collisions: dict[str, dict[str, Any]] = meta.get("collision_adopt", {})
    if not collisions:
        print("  [info] no adoptable collisions in the current stage; nothing "
              "to adopt.", file=sys.stderr)
        return 0
    lock_srcs = {rec.get("src") for rec in lock.get("files", [])}
    lock_dsts = {rec.get("dst") for rec in lock.get("files", [])}
    # --- Preflight the FULL selected set BEFORE any mutation (R4). ---
    planned: list[tuple[dict[str, Any], tuple[Path, bytes] | None]] = []
    for dst_rel in sorted(collisions):
        info = collisions[dst_rel]
        src_rel = info["src"]
        dst_abs = target / dst_rel
        # Eligibility (R3): src genuinely new, dst not already owned by another.
        if src_rel in lock_srcs:
            print(f"error: {dst_rel}: source {src_rel} is already tracked; "
                  "re-run `upgrade --stage`.", file=sys.stderr)
            return 1
        if dst_rel in lock_dsts:
            print(f"error: {dst_rel}: already tracked under another source "
                  "(provenance conflict); not adoptable.", file=sys.stderr)
            return 1
        # Present, regular, contained on-disk file (re-verified at adopt time).
        if not (dst_abs.is_file() and not dst_abs.is_symlink()):
            print(f"error: {dst_rel}: not a present regular file; refusing to "
                  "adopt (re-run `upgrade --stage`).", file=sys.stderr)
            return 1
        _assert_safe_write(dst_abs, target)   # containment of the dst path
        # Hash-bound (R2): bytes must be EXACTLY what --stage observed.
        observed = "sha256:" + _sha256_hex(dst_abs.read_bytes())
        if observed != info.get("observed_hash"):
            print(f"error: {dst_rel}: changed on disk since --stage; refusing "
                  "to adopt (re-run `upgrade --stage`).", file=sys.stderr)
            return 1
        # Re-fetch the upstream template (running-tree adoption -> to_ref=None).
        theirs_b = _theirs_bytes(cairn_root, templates_root, src_rel, None)
        if theirs_b is None:
            print(f"error: upstream template {src_rel!r} not found.",
                  file=sys.stderr)
            return 1
        rec, cache_write = _record_fork_entry(
            target, src_rel, dst_rel, bool(info.get("verbatim")), theirs_b)
        planned.append((rec, cache_write))
    # --- Commit: guarded, atomic, lockfile last (R4). ---
    new_files = [dict(rec) for rec in lock.get("files", [])]
    cache_writes: list[tuple[Path, bytes]] = []
    adopted: list[str] = []
    for rec, cache_write in planned:
        new_files.append(rec)
        if cache_write is not None:
            cache_writes.append(cache_write)
        adopted.append(rec["dst"])
    lock["files"] = new_files
    _commit_lock_and_caches(target, lock, cache_writes)
    print(f"Adopted {len(adopted)} collision(s) as tracked fork(s) in "
          f"{_LOCKFILE_REL}:\n  " + "\n  ".join(adopted) +
          "\n  These now classify as locally-modified forks (upstream recorded "
          "as the merge base). Re-run `upgrade --stage`, then `upgrade --apply`.")
    return 0


def _cmd_finalize_lockfile(target: Path, lock: dict[str, Any]) -> int:
    """`upgrade --finalize`: advance each record's ``hash`` to the adopter's
    *committed on-disk* content, so ``verify_integrity`` attests the customized
    tree the adopter actually ships -- filled slots, the ``VENDOR.md ->
    CLAUDE.md`` wrapper rename, project-owned forks -- rather than the pristine
    clean-install state no real adopter keeps.  This is the step that makes a
    *customized* install verifiable (R10): without it, every slot fill and
    wrapper rename reads as integrity tampering.

    The upgrade ancestor is left untouched: ``base_cache`` / ``base_hash`` (the
    clean-install baseline the 3-way merge + ``classify_verbatim`` fork
    detection use) are preserved.  For a verbatim record predating ``base_hash``,
    the current ``hash`` (the as-shipped baseline) is copied into ``base_hash``
    *before* ``hash`` is advanced, so fork detection survives.  A renamed vendor
    wrapper's record ``dst`` is resolved to the on-disk wrapper (#45) so
    integrity checks the real file, not the absent ``VENDOR.md``.  Idempotent.
    Fail-closed: a tracked file missing on disk aborts (never silently drop a
    file from the integrity set)."""
    files = lock.get("files") or []
    mapped = {r.get("dst") for r in files}
    changed = 0
    missing: list[str] = []
    for rec in files:
        dst_rel = rec.get("dst")
        if not isinstance(dst_rel, str) or not dst_rel:
            continue
        # Resolve a renamed vendor wrapper: the lockfile records VENDOR.md but
        # the adopter renamed it (CLAUDE.md, ...).
        if rec.get("src") == "core/VENDOR.md" and not (target / dst_rel).is_file():
            resolved = _resolve_vendor_wrapper(target, mapped)
            if resolved is not None:
                rec["dst"] = dst_rel = resolved
        dst_abs = target / dst_rel
        if not dst_abs.is_file():
            missing.append(dst_rel)
            continue
        if dst_rel in _LIVING_STATE_DSTS:
            # Adopter-authored project state: tracked for upgrade but excluded
            # from the verify_integrity tamper check. Stamp the flag (this
            # migrates pre-living_state lockfiles) and skip the hash advance --
            # the hash is unused for these records, so don't churn it.
            rec["living_state"] = True
            continue
        # Preserve the as-shipped baseline before advancing hash, for verbatim
        # records that predate base_hash.
        if rec.get("verbatim") and not rec.get("base_hash"):
            rec["base_hash"] = rec.get("hash", "")
        new_hash = "sha256:" + _sha256_hex(dst_abs.read_bytes())
        if new_hash != rec.get("hash"):
            changed += 1
        rec["hash"] = new_hash
    if missing:
        print(f"error: {len(missing)} tracked file(s) missing on disk -- cannot "
              f"finalize (fix or re-install first):\n  " + "\n  ".join(missing),
              file=sys.stderr)
        return 1
    (target / _LOCKFILE_REL).parent.mkdir(parents=True, exist_ok=True)
    (target / _LOCKFILE_REL).write_text(_emit_lock_yaml(lock), encoding="utf-8")
    print(f"Finalized {_LOCKFILE_REL}: advanced {changed} hash(es) to the "
          f"committed on-disk content. `verify_integrity` now attests this tree "
          f"(the base cache / upgrade ancestor is unchanged).")
    return 0


def _dirty_tracked_paths(target: Path) -> set[str] | None:
    """The set of **tracked, uncommitted** paths in ``target`` (repo-root
    relative), or ``None`` when ``target`` is not a git work tree / git is
    absent (fail-soft: no guard when the tree cannot be read).

    Untracked (``??``) and ignored (``!!``) entries are **excluded** -- the
    Layer-3 dirty-tree guard (#56) is keyed on the upgrade write-set, and a
    guard that tripped on scratch or gitignored files would false-positive
    (the proposal's "signals wrong"). Both sides of a rename
    (``R  old -> new``) are reported -- either colliding with the write-set
    is a real overwrite hazard.
    """
    import subprocess

    def _git(*args: str) -> subprocess.CompletedProcess[str] | None:
        try:
            return subprocess.run(
                ["git", "-C", str(target), *args],
                capture_output=True, text=True, timeout=10, check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return None

    inside = _git("rev-parse", "--is-inside-work-tree")
    if inside is None or inside.returncode != 0 \
            or inside.stdout.strip() != "true":
        return None  # not a checkout / git absent -- no guard
    status = _git("status", "--porcelain")
    if status is None or status.returncode != 0:
        return None

    def _unquote(p: str) -> str:
        return p[1:-1] if len(p) >= 2 and p[0] == '"' and p[-1] == '"' else p

    dirty: set[str] = set()
    for line in status.stdout.splitlines():
        if len(line) < 4:
            continue
        code = line[:2]
        if code in ("??", "!!"):
            continue  # untracked / ignored -- benign dirt
        path = line[3:]
        if " -> " in path:  # rename / copy: both sides count
            old, new = path.split(" -> ", 1)
            dirty.add(_unquote(old))
            dirty.add(_unquote(new))
        else:
            dirty.add(_unquote(path))
    return dirty


def _writeset_dirty_collisions(
    target: Path, staged_files: list[str],
) -> list[str]:
    """The sorted intersection of the upgrade write-set (``staged_files``) with
    the target's tracked-uncommitted paths. Empty when the tree is clean, the
    write-set is disjoint from the dirt, or the tree is unreadable
    (fail-soft)."""
    dirty = _dirty_tracked_paths(target)
    if not dirty:
        return []
    return sorted(set(staged_files) & dirty)


def _apply_upgrade(
    target: Path, lock: dict[str, Any], cairn_root: Path, templates_root: Path,
    *, ack_review_only: bool = False, force: bool = False,
) -> int:
    """`--apply` (R7): consume the staged result under the safety contract,
    swap the originals, **advance the lockfile + base cache** to the new
    version, and clean the stage.  Fail-closed at every gate.

    ``ack_review_only`` (the ``--ack-review-only`` flag) is the explicit
    override for the #44 completion gate: ``--apply`` refuses to advance the
    lockfile while files still owe a by-hand merge unless the adopter
    acknowledges them.

    ``force`` (the ``--force`` flag) overrides the Layer-3 dirty-tree guard
    (#56): ``--apply`` refuses when its write-set would overwrite a tracked
    file the adopter has uncommitted edits in (a concurrent session's
    in-flight work)."""
    import json
    import shutil
    stage = target / _STAGING_REL
    meta_path = stage / _STAGE_META
    if not meta_path.exists():
        print("error: no staged upgrade found; run `upgrade --stage` first.",
              file=sys.stderr)
        return 1
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    files_dir = stage / "files"
    staged_meta = sorted(meta.get("staged_files", []))

    # (a) the stage was produced from the current lockfile + tokens + roster.
    if meta.get("lock_commit") != lock.get("cairn_commit") or \
            meta.get("tokens") != lock.get("tokens") or \
            meta.get("modules") != lock.get("modules"):
        print("error: staged upgrade is stale (lockfile/tokens/roster changed "
              "since --stage); re-run `upgrade --stage`.", file=sys.stderr)
        return 1
    # (b) staged-manifest exactness: the files on disk under the
    #     stage must be EXACTLY the metadata's staged set -- no missing, no
    #     extra (a corrupted/hand-edited stage must not apply a subset).
    on_disk = sorted(
        str(f.relative_to(files_dir)) for f in files_dir.rglob("*")
        if f.is_file()
    ) if files_dir.exists() else []
    if on_disk != staged_meta:
        print("error: staged file set does not match the stage manifest "
              "(corrupted/edited stage); re-run `upgrade --stage`.\n"
              f"  manifest: {staged_meta}\n  on disk:  {on_disk}",
              file=sys.stderr)
        return 1
    # (c) every staged file is an advancing kind (defense-in-depth;
    #     non-advancing kinds were never staged).
    kinds = meta.get("kinds", {})
    non_adv = [d for d in staged_meta if kinds.get(d) not in _ADVANCING_KINDS]
    if non_adv:
        print(f"error: staged non-advancing file(s) {non_adv} cannot be "
              "applied; re-run `upgrade --stage`.", file=sys.stderr)
        return 1
    # (d) no residual conflict markers (P-5: only a resolved tree applies).
    for staged in staged_meta:
        if _CONFLICT_MARKER in (files_dir / staged).read_text(
                encoding="utf-8", errors="replace"):
            print(f"error: staged file {staged} still has conflict markers; "
                  "resolve them, then re-run --apply.", file=sys.stderr)
            return 1
    # (d2) #44 completion gate: outstanding review-only files owe a by-hand
    #      merge.  Fail-closed (mirrors the conflict-marker gate) unless the
    #      adopter explicitly acknowledges with --ack-review-only -- so a
    #      --stage -> --apply cannot advance the lockfile to the new version
    #      while customized doctrine silently never landed (the LHM failure).
    review_only = meta.get("review_only", [])
    if review_only and not ack_review_only:
        print("error: the upgrade is not complete -- "
              f"{len(review_only)} file(s) owe a by-hand merge and were not "
              "reconciled:\n  " + "\n  ".join(review_only) +
              f"\n  review the .theirs/.ours pair under {_STAGING_REL}/"
              "review-only/, merge by hand into the original, then re-run "
              "`--apply --ack-review-only` to acknowledge.", file=sys.stderr)
        return 1
    # (d3) Module-addition HARD block (External Security review F2/F3): an
    #      occupied-destination collision, or a structural addition pending under
    #      an explicit --to, fails closed UNCONDITIONALLY -- neither
    #      --ack-review-only NOR --force bypasses it. Without this, apply could
    #      advance the lock + install the package siblings while leaving the
    #      collided/omitted module file importable but absent from the lockfile's
    #      integrity record (the facade-plus-incomplete-package risk this change
    #      exists to close).
    module_blocked = meta.get("module_blocked", [])
    if module_blocked:
        print("error: the upgrade cannot complete -- "
              f"{len(module_blocked)} module-internal addition(s) are blocked "
              "(occupied destination, or pending under --to) and must be "
              "reconciled first:\n  " + "\n  ".join(module_blocked) +
              "\n  remove/merge the on-disk file (or re-run from the target tree "
              "without --to), then re-run `upgrade --stage`.", file=sys.stderr)
        return 1
    # (e) the on-disk originals are unchanged *since --stage* (R7a),
    #     compared to the stage-time snapshot (NOT the clean-install hash --
    #     a customized file differs from that by design).
    ours_hashes = meta.get("ours_hashes", {})
    for staged in staged_meta:
        dst_abs = target / staged
        snap = ours_hashes.get(staged)
        if snap is not None and dst_abs.exists():
            if "sha256:" + _sha256_hex(dst_abs.read_bytes()) != snap:
                print(f"error: {staged} changed on disk since --stage; "
                      "re-run `upgrade --stage`.", file=sys.stderr)
                return 1
    # (e2) Expected-absence guard (R2): a new add (new-core / new-module)
    #      carried no ours_hashes snapshot because its destination was absent at
    #      --stage. If it APPEARED since -- another process/agent created it, or
    #      it is now a symlink -- applying would silently overwrite that content.
    #      Fail closed. --force does NOT override this (it overrides only the
    #      dirty-tree guard on tracked files).
    for dst in meta.get("expected_absent", []):
        dst_abs = target / dst
        if dst_abs.is_symlink() or dst_abs.exists():
            print(f"error: {dst} was absent at --stage but exists now; refusing "
                  "--apply (it would overwrite content created since --stage). "
                  "Re-run `upgrade --stage`.", file=sys.stderr)
            return 1

    # (f) Layer-3 dirty-tree guard (#56): refuse to overwrite a tracked path
    #     the adopter has uncommitted edits in -- applying would clobber a
    #     concurrent session's in-flight work. Scoped to tracked paths (benign
    #     untracked / gitignored dirt does not trip it); --force overrides.
    if not force:
        collide = _writeset_dirty_collisions(target, staged_meta)
        if collide:
            print(
                f"error: refusing --apply: it would overwrite {len(collide)} "
                "tracked file(s) with uncommitted changes:\n  "
                + "\n  ".join(collide) +
                "\n  commit or stash them first, or re-run `--apply --force` "
                "to overwrite.", file=sys.stderr)
            return 1

    # Swap staged files into place.
    for staged in staged_meta:
        dst_abs = target / staged
        _assert_safe_write(dst_abs, target)
        dst_abs.parent.mkdir(parents=True, exist_ok=True)
        dst_abs.write_text(
            (files_dir / staged).read_text(encoding="utf-8"), encoding="utf-8")
    # Advance the base cache to the new upstream raw templates (the next
    # upgrade's ancestor).
    new_base = stage / "new-base"
    if new_base.exists():
        for nb in new_base.rglob("*"):
            if not nb.is_file():
                continue
            cache_abs = target / _BASE_CACHE_REL / nb.relative_to(new_base)
            _assert_safe_write(cache_abs, target)
            cache_abs.parent.mkdir(parents=True, exist_ok=True)
            cache_abs.write_text(nb.read_text(encoding="utf-8"), encoding="utf-8")

    # Advance the lockfile: bump version/commit;
    # recompute each applied file's hash from the NOW-on-disk content (so a
    # resolved conflict is recorded correctly) + refresh the base_hash from
    # the swapped-in base cache.  Non-applied records carry over unchanged.
    new_lock = dict(lock)
    new_lock["cairn_version"] = meta.get("new_version", lock.get("cairn_version"))
    new_lock["cairn_commit"] = meta.get("new_commit", lock.get("cairn_commit"))
    # S1: if the adopter's profile changed since install, re-embed the current
    # resolved profile so the advanced lockfile matches the now-resized on-disk
    # files (the staged content was already sized under this profile).
    new_profile = meta.get("new_profile")
    if new_profile:
        new_lock["profile"] = new_profile
    new_files: list[dict[str, Any]] = []
    staged_set = set(staged_meta)
    rehash_set = set(meta.get("verbatim_rehash", []))
    for rec in lock.get("files", []):
        rec = dict(rec)
        # Renamed vendor wrapper (#45): _compute_upgrade staged the *resolved*
        # wrapper (e.g. CLAUDE.md), but this record still names the canonical
        # VENDOR.md. Rewrite the dst to the on-disk wrapper so the advanced
        # lockfile points at the file that exists -- otherwise --apply leaves a
        # dangling VENDOR.md record and verify_integrity fails.
        if rec.get("src") == "core/VENDOR.md" and rec["dst"] not in staged_set \
                and not (target / rec["dst"]).is_file():
            resolved = _resolve_vendor_wrapper(
                target, {r["dst"] for r in lock.get("files", [])})
            if resolved is not None:
                rec["dst"] = resolved
        if rec["dst"] in staged_set:
            rec["hash"] = "sha256:" + _sha256_hex((target / rec["dst"]).read_bytes())
            if rec.get("base_cache"):
                cache_abs = target / rec["base_cache"]
                if cache_abs.exists():
                    rec["base_hash"] = \
                        "sha256:" + _sha256_hex(cache_abs.read_bytes())
        elif rec["dst"] in rehash_set and (target / rec["dst"]).exists():
            # #48: heal a stale verbatim hash whose on-disk content already
            # equals the new upstream (no content swap -- recompute on disk).
            rec["hash"] = "sha256:" + _sha256_hex((target / rec["dst"]).read_bytes())
        new_files.append(rec)
    # #47: append lockfile records for new core-like files added this upgrade
    # (auto-added; src/verbatim/base_cache carried through stage metadata).
    new_entries = meta.get("new_entries", {})
    added_dsts = [d for d in sorted(new_entries) if d in staged_set]
    for dst in added_dsts:
        info = new_entries[dst]
        rec = {"src": info["src"], "dst": dst,
               "verbatim": bool(info.get("verbatim")),
               "hash": "sha256:" + _sha256_hex((target / dst).read_bytes())}
        if info.get("base_cache"):
            rec["base_cache"] = info["base_cache"]
            cache_abs = target / info["base_cache"]
            if cache_abs.exists():
                rec["base_hash"] = "sha256:" + _sha256_hex(cache_abs.read_bytes())
        new_files.append(rec)
    new_lock["files"] = new_files
    (target / _LOCKFILE_REL).parent.mkdir(parents=True, exist_ok=True)
    (target / _LOCKFILE_REL).write_text(_emit_lock_yaml(new_lock), encoding="utf-8")

    # #47: a newly-added skill needs its vendor fan-out (e.g. .claude/skills ->
    # the canonical .agents/skills) + its machine-state .gitignore seeds, just
    # as a fresh install does. Fan-out is best-effort: a containment refusal
    # warns rather than aborting the already-applied upgrade.
    added_skills = [d for d in added_dsts if d.startswith(".agents/skills/")]
    if added_skills:
        try:
            fan_out_skills(templates_root, target)
        except Exception as exc:  # noqa: BLE001 -- containment/vendor edge
            print(f"  [warn] skills fan-out skipped: {exc}", file=sys.stderr)
        seeded = seed_gitignore(target, _SKILLS_GITIGNORE)
        if seeded:
            print(f"  Seeded .gitignore (skills): {', '.join(seeded)}")

    shutil.rmtree(stage)
    added_note = f" (+{len(added_dsts)} new core-like)" if added_dsts else ""
    print(f"Applied {len(staged_meta)} file(s){added_note}; advanced "
          f"{_LOCKFILE_REL} + the base cache to {new_lock['cairn_commit']}.")
    return 0


def _yaml_sq(v: str) -> str:
    """A YAML single-quoted scalar (doubling any embedded single quote) --
    always valid, and safe for values carrying double quotes / shell syntax
    (e.g. a `test_command`)."""
    return "'" + str(v).replace("'", "''") + "'"


def _self_heal_profile_config(target: Path, lock: dict[str, Any]) -> bool:
    """R1: if `dev/.cairn/profile.yml` is absent but the lockfile carries a
    non-empty profile, materialize the committed config from the lockfile --
    **merging the lockfile `tokens` (project_name, test_command, ...) with the
    `profile` axes/preset (B1)** so the written config is complete and
    re-loadable. Only-when-absent (never clobbers an existing config). Returns
    True iff it wrote one.

    Called on ``--apply`` only -- never ``--stage`` (a non-mutating preview).
    The materialized file is a single new path outside the upgrade's staged
    write-set, so the #56 dirty-tree guard never refuses it."""
    profile_path = target / _PROFILE_REL
    if profile_path.exists():
        return False
    profile = lock.get("profile") or {}
    axes = profile.get("axes") or {}
    if not axes:
        return False  # gating-only / empty lockfile profile -- nothing to heal
    tokens = lock.get("tokens") or {}
    lines = [
        "# Cairn install-config (profile.yml).",
        "# Self-healed by `upgrade` from the lockfile profile: this adopter was",
        "# init-lock'd before profile.yml was materialized. Edit THIS file to",
        "# change the profile, then regenerate the lockfile.",
        "",
    ]
    for key in ("project_name", "test_command", "claim_check_command",
                "metrics_command"):
        if tokens.get(key):
            lines.append(f"{key}: {_yaml_sq(tokens[key])}")
    lines.append("")
    if profile.get("preset"):
        lines.append(f"preset: {profile['preset']}")
    for a in _AXES:
        if axes.get(a):
            lines.append(f"{a}: {axes[a]}")
    modules = lock.get("modules") or []
    if modules:
        lines += ["", "modules:"] + [f"  - {m}" for m in modules]
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  [self-heal] materialized {_PROFILE_REL} from the lockfile profile "
          "(this adopter predates the committed config; edit it to change the "
          "profile, then regenerate the lockfile).", file=sys.stderr)
    return True


def cmd_upgrade(argv: list[str] | None = None) -> int:
    """`scaffold.py upgrade` -- the adopter upgrade path (Chunk 5/6)."""
    import argparse
    p = argparse.ArgumentParser(prog="scaffold.py upgrade")
    p.add_argument("--target", required=True)
    p.add_argument("--to", default=None,
                   help="Upgrade to this Cairn git ref (git-checkout source "
                        "only); default = the currently-running tree.")
    p.add_argument("--cairn-root", default=None)
    p.add_argument("--init-lock", action="store_true",
                   help="Synthesize a lockfile for a pre-lockfile tree (R6).")
    p.add_argument("--finalize", action="store_true",
                   help="Advance each record's hash to the committed on-disk "
                        "content so verify_integrity attests a *customized* "
                        "install (filled slots, wrapper rename, forks). The "
                        "base cache / upgrade ancestor is left unchanged.")
    p.add_argument("--plan", action="store_true",
                   help="Read-only: classify drift, write nothing (default).")
    p.add_argument("--stage", action="store_true",
                   help="Write the staged review surface (no swap).")
    p.add_argument("--apply", action="store_true",
                   help="Apply a previously-staged, resolved upgrade.")
    p.add_argument("--ack-review-only", action="store_true",
                   help="Acknowledge outstanding review-only files so --apply "
                        "proceeds (the #44 completion gate is fail-closed "
                        "without this).")
    p.add_argument("--force", action="store_true",
                   help="Override the Layer-3 dirty-tree guard (#56): apply "
                        "even when the write-set overlaps tracked files with "
                        "uncommitted changes (they will be overwritten).")
    p.add_argument("--adopt-module", default=None, metavar="NAME",
                   help="Record an already-on-disk opt-in module NAME into the "
                        "lockfile so it 3-way-merges on later upgrades (#49). "
                        "Explicit, never automatic -- a module is a deliberate "
                        "choice.")
    p.add_argument("--adopt-collisions", action="store_true",
                   help="Record occupied-destination collisions surfaced by a "
                        "prior --stage as tracked adopter forks (keep-mine), so "
                        "the upgrade is no longer blocked on them. Bound to the "
                        "staged set + bytes; explicit, never automatic.")
    args = p.parse_args(argv)

    # R5 (External Security review): the upgrade ACTIONS are mutually exclusive.
    # argparse parses them independently and the dispatch is first-match, so a
    # mixed invocation (e.g. `--adopt-collisions --apply`) would silently run
    # only one branch while reading as "adopt, then apply". Reject before any
    # work. (--to / --ack-review-only / --force / --cairn-root are modifiers,
    # not actions; --plan is the default action and composes with none of these.)
    actions = [name for name, on in (
        ("--init-lock", args.init_lock),
        ("--finalize", args.finalize),
        ("--stage", args.stage),
        ("--apply", args.apply),
        ("--adopt-collisions", args.adopt_collisions),
    ) if on]
    if args.adopt_module:
        actions.append("--adopt-module")
    if len(actions) > 1:
        print(f"error: {', '.join(sorted(actions))} are mutually exclusive; "
              "run one upgrade action at a time.", file=sys.stderr)
        return 2

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"error: target not found: {target}", file=sys.stderr)
        return 1
    cairn_root = (Path(args.cairn_root).resolve() if args.cairn_root
                  else _cairn_root())
    templates_root = cairn_root / "templates"

    if args.init_lock:
        return _cmd_init_lock(target, cairn_root, templates_root)

    if args.adopt_module:
        return _cmd_adopt_module(
            target, args.adopt_module, cairn_root, templates_root)

    lock = read_lockfile(target)
    if lock is None:
        print(f"error: no {_LOCKFILE_REL} in the target. Run "
              "`upgrade --init-lock --target <repo>` to migrate a "
              "pre-lockfile tree first.", file=sys.stderr)
        return 1

    if args.finalize:
        return _cmd_finalize_lockfile(target, lock)

    if args.adopt_collisions:
        if args.to is not None:
            print("error: --adopt-collisions runs against the running target "
                  "tree; --to is not supported (run scaffold from the target "
                  "tree).", file=sys.stderr)
            return 2
        try:
            return _cmd_adopt_collisions(target, cairn_root, templates_root, lock)
        except ScaffoldSecurityError as exc:
            print("error: upgrade --adopt-collisions refused (containment): "
                  f"{exc}", file=sys.stderr)
            return 2

    if args.to is not None and not _cairn_is_git(cairn_root):
        print("error: --to <ref> needs a git-checkout Cairn source; a "
              "packaged release can upgrade only to the currently-running "
              "tree (omit --to).", file=sys.stderr)
        return 1

    # Required-token preflight (security-apparatus-enrichment B0): the writing
    # upgrade paths (--stage materializes the review surface, --apply swaps the
    # tree) re-render token-substituted files from the lockfile's token map. If
    # an installed module's required token is unfilled in the lockfile, re-render
    # would propagate the placeholder. Fail closed BEFORE either write path. The
    # read-only --plan is left available so an adopter can diagnose the gap.
    if args.apply or args.stage:
        gaps = missing_required_tokens(
            list(lock.get("modules", [])),
            {str(k): str(v) for k, v in (lock.get("tokens") or {}).items()},
        )
        if gaps:
            by_module: dict[str, list[str]] = {}
            for module, token in gaps:
                by_module.setdefault(module, []).append(token)
            print(
                "error: installed module(s) have unfilled required token(s) in "
                f"{_LOCKFILE_REL}; refusing to upgrade (no files written):",
                file=sys.stderr,
            )
            for module in sorted(by_module):
                print(f"  - {module}: {', '.join(sorted(by_module[module]))}",
                      file=sys.stderr)
            print("Fill the token(s) (upgrade --init-lock) and retry.",
                  file=sys.stderr)
            return 2

    # R1 self-heal (--apply only -- NOT --stage, which is a non-mutating preview
    # that writes solely to the gitignored review surface; and never on the
    # read-only --plan): an already-init-lock'd adopter may carry a populated
    # lockfile profile but no committed dev/.cairn/profile.yml. Materialize it
    # from the lockfile so the config you edit exists. Only-when-absent;
    # composes with the #56 guard.
    if args.apply:
        _self_heal_profile_config(target, lock)

    if args.apply:
        try:
            return _apply_upgrade(target, lock, cairn_root, templates_root,
                                  ack_review_only=args.ack_review_only,
                                  force=args.force)
        except ScaffoldSecurityError as exc:
            print(f"error: upgrade --apply refused (containment): {exc}",
                  file=sys.stderr)
            return 2

    plans, structural = _compute_upgrade(
        target, cairn_root, templates_root, lock, args.to)
    citation = _citation_ok(target, lock)
    # #54 adoption->canonical drift surfacing (informational; never blocks).
    drift = _behind_by_n(
        cairn_root, lock.get("cairn_commit"),
        args.to or _cairn_commit(cairn_root))

    if args.stage:
        _new_profile, _new_axes = _resolve_current_profile(target, lock)
        try:
            stage = _write_stage(target, plans, lock, args.to, cairn_root,
                                 new_profile=_new_profile)
        except ScaffoldSecurityError as exc:
            print(f"error: upgrade --stage refused (containment): {exc}",
                  file=sys.stderr)
            return 2
        _print_upgrade_report(plans, structural, citation, mode="stage",
                              drift=drift)
        # (R1) --stage writes only the gitignored review surface, so it
        # *completes* even on a dirty tree -- but advise when the write-set
        # overlaps a tracked uncommitted path so the eventual --apply refusal
        # is no surprise.
        try:
            import json as _json
            _meta = _json.loads(
                (stage / _STAGE_META).read_text(encoding="utf-8"))
            _collide = _writeset_dirty_collisions(
                target, _meta.get("staged_files", []))
        except (OSError, ValueError):
            _collide = []
        if _collide:
            print(
                f"\n  [advisory] {len(_collide)} staged file(s) overlap "
                "tracked uncommitted changes; --apply will refuse until they "
                "are committed/stashed (or pass --force):\n    "
                + "\n    ".join(_collide), file=sys.stderr)
        print(f"\nStaged under {_STAGING_REL}/ . Resolve any conflicts, then "
              "`upgrade --apply --target <repo>`.")
        return 0

    # Default: --plan (strictly read-only).
    _print_upgrade_report(plans, structural, citation,
                          mode="plan (read-only)", drift=drift)
    return 0
