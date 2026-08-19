"""Scaffold engine -- lockfile data / read / emit / classify core (scaffold-split Stage 5).

The install lockfile is the second trust anchor: ``bootstrap/verify_integrity.py``
attests the shipped Cairn apparatus against the recorded hashes. This module owns
that surface -- the lockfile path/cache/profile constants, the living-state
exclusion set, the secret-token guard, the deterministic JSON-as-YAML emit, the
stdlib-only ``read_lockfile`` parse, the Cairn version/commit/behind-by provenance
helpers, and the verbatim-script hash policy (``classify_verbatim``, deferred from
Stage 3 because it couples to ``_sha256_hex`` here).

A near-leaf: it imports only the stdlib plus the ``config`` leaf (for
``PresetError``, raised by the secret-token guard) and the ``security`` leaf
(for the one containment primitive the fork advisory's two disk reads route
through) -- downward dependencies, no cycle. It reads/serializes lockfile data
and computes hashes but performs no
adopter-tree writes (the install-time WRITER ``write_install_lockfile`` stays in
the engine -- it couples to onboarding/install symbols -- and joins install.py at
Stage 6; ``_lock_file_list`` likewise couples to the manifest). **This module**
owns no writes and no CLI/upgrade execution; importing it defines names only
(import-purity). That is an *ownership* property, not a runtime-loading
boundary: importing ``bootstrap._scaffold.lockfile`` runs the eager package facade
first, which loads the whole engine (see the
``test_trust_anchor_imports_are_owner_specific_not_runtime_isolated`` regression).
install / upgrade / verify_integrity depend on it, never the reverse.

Pure motion from the pre-split monolith (Stage 5): the symbols are unchanged; only
their home moved. ``read_lockfile`` + the lock constants migrate here as their
owning module (plan 0B.3); ``verify_integrity`` imports them from this narrow
owner. Loaded via the engine's verifying finder, so this file's real path is
confirmed within the Cairn root before it executes.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, NamedTuple

from .config import PresetError  # the secret-token guard raises this (downward dep)
# The fork advisory reads two files off disk and must not be talked out of
# either root.  It reuses the engine's ONE containment primitive rather than
# growing a second, unreviewed copy inside this near-leaf; the
# layering assertion in bootstrap/tests/test_lockfile_module.py admits exactly
# {config, security} because of this line.
from .security import ScaffoldSecurityError, _assert_safe_write


_LOCKFILE_REL = "dev/.cairn/cairn-lock.yml"        # tracked machinery (in .cairn/ with its kin)
_BASE_CACHE_REL = "dev/.cairn/base"         # tracked raw-template cache
_PROFILE_REL = "dev/.cairn/profile.yml"     # canonical committed install-config (BOOTSTRAP.md)
_LOCK_SCHEMA = 1
#: An additive optional top-level lockfile field does NOT bump this --
#: see "Adding a lockfile field without bumping the schema" in
#: bootstrap/UPGRADE.md for the full rule and the reader-tolerance it relies on.


#: Lockfile records for these dsts carry ``living_state: true`` and are
#: **tracked for upgrade but excluded from the ``verify_integrity`` hash
#: check**.  Rationale: ``verify_integrity`` exists so a cold adopter can
#: attest the *shipped Cairn apparatus* (scripts, module/core doctrine,
#: templates) was not swapped -- a supply-chain check.  These files are not
#: apparatus, in two classes.  Four are **adopter-authored project state** (a
#: living roadmap, the per-goodnight handoff, the fold-back ledger, the signed
#: collaboration agreement) that merely starts from a thin Cairn template.  The
#: rest are **adopter-filled configuration** -- installed as an unconfigured
#: stub and then filled in place (the model-selection mapping, and the two
#: network-security capability policies).
#: They are the highest-churn files in a mature adopter, so including them in
#: the strict integrity set means every routine edit reds the verifier until a
#: re-finalize -- friction that says nothing about whether the *scripts* are
#: trustworthy.  They keep ``base_cache`` / ``base_hash`` so ``upgrade`` still
#: 3-way-merges a Cairn template change into the adopter's customization; only
#: the tamper check skips them.  (Note this is deliberately NOT paired with a
#: goodnight auto-``--finalize``: blessing whatever is on disk on a schedule
#: would *launder* a real apparatus swap -- the very thing the check defends --
#: so ``--finalize`` stays an explicit, deliberate re-attestation.)
#:
#: **Conscious tradeoff (governance prose).**  ``dev/collaboration_agreement.md``
#: is the most delicate member: a signed agreement can govern review rights,
#: commit permissions, and trust boundaries, so excluding it from tamper
#: attestation is a real (accepted) tradeoff -- tampering with governance *prose*
#: is **outside ``verify_integrity``'s threat model** (which covers a swapped
#: *executable*) and is caught by git review + history, not by the
#: apparatus-integrity gate.  **This boundary is enforced by the verifier**, not
#: trusted from the lockfile: ``verify_integrity`` honors ``living_state`` only
#: for a ``dst`` in this set, and fails closed on any other record that asserts
#: it (so a modified script cannot hide by flipping the flag).
_LIVING_STATE_DSTS: frozenset[str] = frozenset({
    "dev/PLANNING.md",
    "dev/NEXT_SESSION.md",
    "dev/.cairn/cairn_foldback.md",
    "dev/collaboration_agreement.md",
    # Fold 5 (foldback-drain-tooling): the model-selection mapping is
    # adopter-local configuration that the adopter fills and re-fills as
    # their model lineup evolves.  Marking it living-state means
    # verify_integrity never flags an adopter edit as tampering, and the
    # lockfile divergence check does not prevent writing on first-fill.
    "dev/.cairn/model-selection-mapping.yml",
    # The two network-security capability
    # policies are adopter-filled configuration.  Each installs as an
    # unconfigured ``configured: false`` stub and is then filled in place with
    # local principals and operations, so hash-pinning it would report ordinary
    # configuration as tampering.  They stay tracked for upgrade -- substituted
    # installs, so they keep ``base_cache`` / ``base_hash`` and ``upgrade``
    # still 3-way-merges a Cairn stub change into the adopter's fill -- and are
    # excluded from the tamper check only.  They are explicitly **not** the
    # integrity anchor for the deployed leg: the capability facade and its four
    # engine members are verbatim, stay in the strict set, and are what the
    # dispatcher binds by digest.  The policy's own bytes are reviewed through
    # git, which the module doctrine records as a named residual.
    "dev/.cairn/api-access-policy.json",
    "dev/.cairn/web-hosting-policy.json",
})


#: Token names that must never be recorded in the lockfile: a
#: substitution token bearing a secret would leak it into a tracked file.
#: Matched as a **substring anywhere** in the token name (case-insensitive)
#: so camelCase / flatcase keys are caught too -- `apiKey`, `secretToken`,
#: `dbPassword`, `mysecret`, `passwdstr` all match, not only snake_case.
#: The allow-list makes false positives cheap; a silent secret leak is not.
_SECRET_TOKEN_RE = re.compile(
    r"password|passwd|secret|credential|token|key", re.IGNORECASE,
)


def _sha256_hex(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def _cairn_version(cairn_root: Path) -> str:
    """Read the Cairn version from ``CITATION.cff`` (``unknown`` if absent)."""
    cff = cairn_root / "CITATION.cff"
    if cff.exists():
        for line in cff.read_text(encoding="utf-8").splitlines():
            m = re.match(r'\s*version\s*:\s*"?([^"\s]+)"?\s*$', line)
            if m:
                return m.group(1)
    return "unknown"


def _cairn_commit(cairn_root: Path) -> str:
    """Short HEAD commit of the Cairn source, or ``unknown`` (no git)."""
    import subprocess
    try:
        r = subprocess.run(
            ["git", "-C", str(cairn_root), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return r.stdout.strip() if r.returncode == 0 else "unknown"


def _cairn_provenance(cairn_root: Path) -> tuple[str, list[str]]:
    """Read the declared source repository and licenses from ``CITATION.cff``
    (``("unknown", [])`` if absent, unreadable, or keyless).

    ``source_repository`` is a single-line match on ``repository-code:``,
    mirroring :func:`_cairn_version`'s pattern. ``source_licenses`` consumes
    the indented ``- `` items immediately following a bare ``license:`` line,
    stopping at the first line that is not such an item -- CITATION.cff's own
    ``license:`` block is immediately followed by a ``keywords:`` block with
    its own ``- `` items, and a scanner that kept consuming would silently
    record keywords as licenses. A scalar ``license: MIT`` form is accepted
    as a one-element list. A consumed value containing whitespace (not a bare
    SPDX-shaped token) is dropped.

    Both values are **declarations** derived from the source tree at
    install/upgrade time, not attestations of checkout origin or
    installed-file licensing -- see ``bootstrap/UPGRADE.md``.
    """
    cff = cairn_root / "CITATION.cff"
    if not cff.exists():
        return "unknown", []
    try:
        lines = cff.read_text(encoding="utf-8").splitlines()
    except OSError:
        return "unknown", []

    repository = "unknown"
    for line in lines:
        m = re.match(r'\s*repository-code\s*:\s*"?([^"\s]+)"?\s*$', line)
        if m:
            repository = m.group(1)
            break

    licenses: list[str] = []
    for i, line in enumerate(lines):
        m = re.match(r'\s*license\s*:\s*(.*)$', line)
        if not m:
            continue
        rest = m.group(1).strip()
        if rest:
            if " " not in rest:
                licenses.append(rest)
        else:
            for nxt in lines[i + 1:]:
                item = re.match(r'\s*-\s*(.+?)\s*$', nxt)
                if not item:
                    break
                value = item.group(1).strip()
                if value and " " not in value:
                    licenses.append(value)
        break

    return repository, licenses


def _behind_by_n(cairn_root: Path, lock_commit: str | None,
                 new_commit: str | None) -> str:
    """#54 adoption->canonical drift surfacing: a one-line message for how far
    the adopter's installed Cairn ref (*lock_commit*) is behind canonical
    (*new_commit*).

    **Degrades gracefully.** If either ref is missing or the ``unknown``
    sentinel (a non-git / packaged-release source, per ``_cairn_commit``), or
    git is unavailable, it returns an explicit *unavailable* message rather
    than running a git compare on a bad ref. Informational only -- the caller
    surfaces it; it never blocks."""
    import subprocess
    if (not lock_commit or not new_commit
            or "unknown" in (lock_commit, new_commit)):
        return ("adoption drift: behind-by-N check unavailable "
                "(git metadata missing)")
    if lock_commit == new_commit:
        return "adoption drift: installed tree is current with canonical"
    try:
        r = subprocess.run(
            ["git", "-C", str(cairn_root), "rev-list", "--count",
             f"{lock_commit}..{new_commit}"],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "adoption drift: behind-by-N check unavailable (git error)"
    if r.returncode != 0:
        return ("adoption drift: behind-by-N check unavailable "
                "(refs not comparable)")
    return ("adoption drift: installed tree is behind canonical by "
            f"{r.stdout.strip()} commit(s)")


def _refuse_secret_tokens(
    tokens: dict[str, str], allow: tuple[str, ...] = (),
) -> None:
    """Raise PresetError if any token name looks secret-bearing."""
    allowed = {a.lower() for a in allow}
    offending = sorted(
        name for name in tokens
        if _SECRET_TOKEN_RE.search(name) and name.lower() not in allowed
    )
    if offending:
        raise PresetError(
            "refusing to record secret-like token name(s) in the lockfile: "
            + ", ".join(offending)
            + " -- Cairn templates must not introduce secret-bearing "
            "substitution tokens (bootstrap/SAFETY.md). If a token is "
            "genuinely public, add it to the writer's allow-list."
        )


def _emit_lock_yaml(data: dict[str, Any]) -> str:
    """Serialize the lockfile as deterministic JSON (valid YAML 1.2) so it
    round-trips **stdlib-only** (no PyYAML dependency) while staying a
    parseable ``.yml``.  Tool-owned: regenerate-only, do not hand-edit."""
    import json
    header = (
        "# cairn-lock.yml -- machine-generated install lockfile "
        "(tool-owned; regenerate-only; do not hand-edit).\n"
        "# JSON-encoded (valid YAML 1.2) so it round-trips without a YAML "
        "dependency.\n"
        "# source_repository/source_licenses are declared, not attested -- "
        "see \"Adding a lockfile field without bumping the schema\" in "
        "bootstrap/UPGRADE.md (a reference in the Cairn source repository, "
        "not a file installed into this tree).\n"
    )
    return header + json.dumps(data, indent=2, sort_keys=True) + "\n"


def read_lockfile(target: Path) -> dict[str, Any] | None:
    """Read ``<target>/dev/.cairn/cairn-lock.yml`` (or None if absent/unparseable).

    Strips ``#`` comment lines, then parses the JSON body (the format
    :func:`_emit_lock_yaml` writes)."""
    import json
    p = target / _LOCKFILE_REL
    if not p.exists():
        return None
    body = "\n".join(
        ln for ln in p.read_text(encoding="utf-8").splitlines()
        if not ln.lstrip().startswith("#")
    )
    try:
        data = json.loads(body)
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


# ---------------------------------------------------------------------------
# Verbatim-script hash policy (Part 4) -- hash check, never a text merge
# ---------------------------------------------------------------------------

def classify_verbatim(
    ours_bytes: bytes | None, lock_hash: str, theirs_bytes: bytes,
) -> str:
    """Classify a verbatim script for upgrade (no text merge, hash only).

    Returns: ``"missing"`` (not on disk); ``"locally-modified"`` (on-disk
    hash != the lockfile's recorded base hash -> flag, never clobber);
    ``"up-to-date"`` (already equals the new upstream); or ``"update"``
    (unmodified vs base and differs from upstream -> safe to update).

    The ``ours == theirs`` check runs **first** (fold-back #48): a file an
    adopter hand-synced to *exactly* the new upstream before upgrading is
    ``up-to-date``, not a fork -- even when the lockfile hash is stale (it was
    recorded against an older Cairn). Were the stale-hash check first, such a
    file would be flagged a fork on every future upgrade. ``--apply`` heals the
    stale lock hash (see ``_write_stage``/``_apply_upgrade``: ``verbatim_rehash``).
    """
    if ours_bytes is None:
        return "missing"
    if ours_bytes == theirs_bytes:
        return "up-to-date"
    ours_h = "sha256:" + _sha256_hex(ours_bytes)
    if ours_h != lock_hash:
        return "locally-modified"
    return "update"


# ---------------------------------------------------------------------------
# Forked-facade / dormant-engine detector (foldback rollup #4)
# ---------------------------------------------------------------------------

def _facade_engine_dir(dst_rel: str) -> str | None:
    """The engine-package dir a facade ``<dir>/<name>.py`` launches:
    ``<dir>/_<name>`` -- the documented facade↔engine convention (e.g.
    ``tools/intent.py`` -> ``tools/_intent``).  ``None`` for a non-``.py`` dst."""
    p = Path(dst_rel)
    if p.suffix != ".py":
        return None
    return p.with_name("_" + p.stem).as_posix()


class UpstreamSource(NamedTuple):
    """The **caller-supplied** comparison source for the fork advisory.

    The defect class this type exists to close is one sentence: *the artifact
    under verification must not supply the material used to verify it.* Every
    field here is resolved by the caller from the caller's **own** on-disk
    location -- never from the target tree, never from the target's lockfile:

    * ``templates_root`` -- the root of the trusted template checkout whose
      bytes decide the verdict.
    * ``src_for_dst`` -- the destination -> source map, built from the engine's
      own in-memory install registries (``install_manifest``), **never** from a
      lockfile record's ``src``.
    * ``ref`` -- a human-readable identifier for that checkout (its Cairn
      version), printed in the note so an operator can see whose bytes decided
      it (a residual gap).

    **Not established by this type**: containment is a *path* property. A
    tampered file **inside** ``templates_root``, or a symlinked
    ``templates_root`` itself, passes every check below by construction.
    Authenticating the checkout that supplies the comparison bytes is residual
    That is `release-authenticity`'s job, not this module's.
    """

    templates_root: Path
    src_for_dst: dict[str, str]
    ref: str | None


def forked_facade_findings(
    target: Path, lock: dict[str, Any], *,
    upstream: UpstreamSource | None,
) -> list[dict[str, Any]]:
    """Find ``verbatim`` facades whose **on-disk bytes** differ from the
    caller's trusted upstream template while their engine package ``_<name>/``
    sits **installed** under *target* -- a live-but-stale launcher running an
    un-maintained fork while the maintained engine is dormant (rollup #4).

    ``verify_integrity`` reports such a tree OK (on-disk == the finalized
    ``hash``), so the divergence is invisible without this correlation.

    *upstream* is **keyword-only and has no default**: omitting it is a
    ``TypeError``, because a caller that cannot say where its comparison bytes
    come from must not get a silent answer. Passing ``None`` is the legal,
    explicit "I have no trusted upstream" -- every finding then degrades to
    ``unconfirmed`` and is **retained**.

    Each finding is ``{"dst", "engine", "acknowledged", "kind", "reason",
    "upstream", "src_relabelled", "skew"}``:

    * ``kind`` is ``"differs-from-upstream"`` (two validated reads disagreed)
      or ``"unconfirmed"`` (no comparison was possible; the difference is from
      the *install-time baseline* recorded in the lockfile, which ``--finalize``
      ratchets, so it is not evidence of an upstream fork).
    * ``reason`` says why an ``unconfirmed`` finding could not be confirmed.
    * ``upstream`` names the root and ref that decided (or would have decided).
    * ``src_relabelled`` / ``skew`` are **annotations on a finding that already
      exists** -- never a note of their own, so the finding set cannot grow.

    **The only suppression path** is byte-equality between two validated reads
    (``disk_bytes == upstream_bytes``). ``rec["hash"]``, ``rec["base_hash"]``,
    ``rec["src"]`` and every other lockfile field are forbidden as the
    target-side operand, and a caller may not pass precomputed hashes in to
    avoid the read. Every degradation path -- no trusted upstream, no map row,
    a missing or unreadable file on either side, a containment refusal on
    either side -- **retains** the finding as ``unconfirmed``.

    **Detection only** -- it reads, never mutates, never deletes.
    """
    # Resolve *target* ONCE, here, and use the resolved root for the
    # containment check, the destination join AND the engine-directory probe --
    # so containment can never depend on the caller's resolution ordering.
    unresolvable_target = False
    try:
        target_root = Path(target).resolve()
    except OSError:
        target_root, unresolvable_target = Path(target), True

    def _guarded_read(root: Path, rel: str, what: str) -> tuple[
            bytes | None, str | None]:
        """``(bytes, None)`` for a validated read of ``<root>/<rel>``, else
        ``(None, reason)``. Three fail-closed checks, in order:

        1. *shape* -- ``rel`` must be a non-empty, repo-relative POSIX path
           with no ``..`` component;
        2. *containment* -- ``_assert_safe_write(candidate, root)``: no
           symlinked destination, no symlinked parent, no escape from ``root``;
        3. *kind* -- the result must be an existing **regular, non-symlink**
           file.

        A refusal never suppresses: the caller turns ``reason`` into an
        ``unconfirmed`` finding that is still reported.
        """
        if not isinstance(rel, str) or not rel:
            return None, f"{what} path is missing from the record"
        head = rel.split("/", 1)[0]
        if "\\" in rel or ":" in head:
            return None, (f"{what} path is not a repo-relative POSIX path: "
                          f"{rel}")
        p = Path(rel)
        if p.is_absolute() or ".." in p.parts:
            return None, (f"{what} path is not a repo-relative POSIX path: "
                          f"{rel}")
        candidate = root / p
        # This is a WRITE-flavoured guard used on a READ path. The three
        # checks it performs (symlinked destination, symlinked parent, escape
        # from root) are exactly the ones a read needs, and growing the
        # security leaf with a read-flavoured sibling for one caller was
        # deferred by the proposal. Trigger to revisit: a second read-side
        # caller, or any divergence between what a read and a write must refuse.
        try:
            _assert_safe_write(candidate, root)
        except ScaffoldSecurityError as exc:
            # Caught HERE, inside this module, on purpose: a malformed trusted
            # templates tree must degrade the advisory, not abort the verifier
            # that hosts it. This is the one deliberately-open edge, and it is
            # on an advisory-only surface.
            return None, f"{what} failed the containment check ({exc})"
        if candidate.is_symlink() or not candidate.is_file():
            return None, f"{what} is not an existing regular file: {rel}"
        try:
            return candidate.read_bytes(), None
        except OSError as exc:
            return None, f"{what} could not be read ({exc})"

    templates_root: Path | None = None
    if upstream is not None:
        try:
            templates_root = Path(upstream.templates_root).resolve()
        except OSError:
            templates_root = None

    # Source-version skew: an annotation, computed once, attached to
    # findings that already exist. It never creates one.
    skew: str | None = None
    if upstream is not None:
        lock_ref = lock.get("cairn_version")
        up_ref = upstream.ref
        if (isinstance(lock_ref, str) and isinstance(up_ref, str)
                and lock_ref and up_ref and lock_ref != up_ref
                and "unknown" not in (lock_ref, up_ref)):
            skew = ("source-version skew: the comparison used Cairn "
                    f"{up_ref}, while this tree records its install from "
                    f"Cairn {lock_ref}")

    findings: list[dict[str, Any]] = []
    for rec in lock.get("files") or []:
        if not rec.get("verbatim"):
            continue
        h = rec.get("hash")
        base = rec.get("base_hash")
        # R10 -- CANDIDATE SELECTION IS STILL LOCK-DERIVED, and deliberately so
        # within this scope: `hash`, `base_hash`, `dst` and the engine-directory
        # probe decide *which* records are examined. A lockfile asserting
        # `hash == base_hash` evades the advisory entirely. What this change
        # fixes is the *verdict* (below), which is now decided by two reads off
        # disk. Selection stays unfixable while `base_hash` is a lockfile field
        # revisit the two together.
        if not (isinstance(h, str) and isinstance(base, str) and h != base):
            continue
        dst_rel = rec.get("dst")
        if not isinstance(dst_rel, str) or not dst_rel:
            continue
        engine_rel = _facade_engine_dir(dst_rel)
        if engine_rel is None:
            continue
        engine_dir = target_root / engine_rel
        # An installed engine = a present package dir carrying ≥1 .py module.
        if not engine_dir.is_dir() or not any(engine_dir.glob("*.py")):
            continue

        kind = "unconfirmed"
        reason: str | None = None
        compared: str | None = None
        relabelled = False

        if upstream is None:
            reason = "the caller supplied no trusted upstream"
        elif templates_root is None:
            reason = "the trusted templates root could not be resolved"
        elif unresolvable_target:
            reason = "the target root could not be resolved"
        else:
            compared = (f"{templates_root} (Cairn "
                        f"{upstream.ref or 'unknown'})")
            # The destination -> source map is the CALLER's. The lockfile's own
            # `src` is read for one purpose only: to say, as an annotation,
            # that it disagrees. It never selects the bytes.
            src_rel = upstream.src_for_dst.get(dst_rel)
            recorded_src = rec.get("src")
            if (isinstance(recorded_src, str) and isinstance(src_rel, str)
                    and recorded_src != src_rel):
                relabelled = True
            if not isinstance(src_rel, str):
                reason = ("this destination is absent from the trusted install "
                          "manifest, so no upstream template names it")
            else:
                up_bytes, why = _guarded_read(
                    templates_root, src_rel, "the upstream template")
                if up_bytes is None:
                    reason = why
                else:
                    disk_bytes, why = _guarded_read(
                        target_root, dst_rel, "the installed file")
                    if disk_bytes is None:
                        reason = why
                    elif disk_bytes == up_bytes:
                        # THE ONLY SUPPRESSION PATH: byte-equality between
                        # two validated reads. Nothing the lockfile asserts can
                        # reach this branch.
                        continue
                    else:
                        kind = "differs-from-upstream"

        findings.append({
            "dst": dst_rel,
            "engine": engine_rel,
            "acknowledged": rec.get("fork_acknowledged") is True,
            "kind": kind,
            "reason": reason,
            "upstream": compared,
            "src_relabelled": relabelled,
            "skew": skew,
        })
    return findings


def format_forked_facade_warning(
    finding: dict[str, Any], *, at_upgrade: bool,
) -> str:
    """One advisory block for a forked-facade finding.  **Advisory only** -- it
    never blocks or mutates; the adopter restores the facade from its upstream
    template to bring it back in sync with the maintained engine, or sets
    ``fork_acknowledged`` to silence it at ``verify`` time (``upgrade`` always
    re-surfaces it).

    Renders the finding's ``kind`` as a stated fact rather than leaving a reader
    to guess which comparison produced it, plus the two annotations (source-
    version skew, relabelled ``src``) when they are present. Reads every field
    with ``.get`` so a caller holding a bare ``{"dst", "engine",
    "acknowledged"}`` finding still renders (as ``unconfirmed``)."""
    where = "upgrade" if at_upgrade else "verify_integrity"
    dst = finding.get("dst")
    engine = finding.get("engine")
    compared = finding.get("upstream")

    if finding.get("kind") == "differs-from-upstream":
        head = (
            f"{where}: NOTE -- facade {dst!r} is forked from upstream (its "
            f"on-disk bytes differ from the upstream template) but its engine "
            f"package {engine!r} is installed.\n"
        )
        detail = f"  Compared against {compared}.\n" if compared else ""
    else:
        head = (
            f"{where}: NOTE -- facade {dst!r} differs from its install-time "
            f"baseline (hash != base_hash) but its engine package {engine!r} "
            "is installed.\n"
        )
        detail = (
            "  UNCONFIRMED -- this difference is measured against the "
            "install-time baseline in the lockfile, not against upstream: "
            f"{finding.get('reason') or 'no comparison was possible'}.\n"
        )
        if compared:
            detail += f"  The upstream that would have decided it: {compared}.\n"

    if finding.get("skew"):
        detail += f"  {finding['skew']}.\n"
    if finding.get("src_relabelled"):
        detail += (
            "  This record's own \"src\" does not name the upstream template "
            "the trusted install manifest names; the recorded \"src\" was "
            "ignored.\n"
        )

    ack_hint = (
        "" if at_upgrade else
        '  Set "fork_acknowledged": true on its lockfile record to silence '
        "this at verify time (upgrade still re-surfaces it).\n"
    )
    return (
        head + detail
        + "  You are running an un-maintained fork of the launcher while the "
        "maintained engine sits dormant; upstream engine fixes will not take "
        "effect.\n"
        "  Restore the facade from its upstream template to bring it back "
        f"in sync with the maintained engine.\n{ack_hint}"
    )
