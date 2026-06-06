"""Scaffold engine -- lockfile data / read / emit / classify core (scaffold-split Stage 5).

The install lockfile is the second trust anchor: ``bootstrap/verify_integrity.py``
attests the shipped Cairn apparatus against the recorded hashes. This module owns
that surface -- the lockfile path/cache/profile constants, the living-state
exclusion set, the secret-token guard, the deterministic JSON-as-YAML emit, the
stdlib-only ``read_lockfile`` parse, the Cairn version/commit/behind-by provenance
helpers, and the verbatim-script hash policy (``classify_verbatim``, deferred from
Stage 3 because it couples to ``_sha256_hex`` here).

A near-leaf: it imports only the stdlib plus the ``config`` leaf (for
``PresetError``, raised by the secret-token guard) -- a downward dependency, no
cycle. It reads/serializes lockfile data and computes hashes but performs no
adopter-tree writes (the install-time WRITER ``write_install_lockfile`` stays in
the engine -- it couples to onboarding/install symbols -- and joins install.py at
Stage 6; ``_lock_file_list`` likewise couples to the manifest). **This module**
owns no writes and no CLI/upgrade execution; importing it defines names only
(import-purity, SR2). That is an *ownership* property, not a runtime-loading
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
from typing import Any

from .config import PresetError  # the secret-token guard raises this (downward dep)


_LOCKFILE_REL = "dev/.cairn/cairn-lock.yml"        # tracked machinery (in .cairn/ with its kin)
_BASE_CACHE_REL = "dev/.cairn/base"         # tracked raw-template cache (R1/I4)
_PROFILE_REL = "dev/.cairn/profile.yml"     # canonical committed install-config (BOOTSTRAP.md)
_LOCK_SCHEMA = 1


#: Lockfile records for these dsts carry ``living_state: true`` and are
#: **tracked for upgrade but excluded from the ``verify_integrity`` hash
#: check**.  Rationale: ``verify_integrity`` exists so a cold adopter can
#: attest the *shipped Cairn apparatus* (scripts, module/core doctrine,
#: templates) was not swapped -- a supply-chain check.  These four files are
#: not apparatus: their content is **adopter-authored project state** (a living
#: roadmap, the per-goodnight handoff, the fold-back ledger, the signed
#: collaboration agreement) that merely starts from a thin Cairn template.
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
})


#: Token names that must never be recorded in the lockfile (R9): a
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


def _behind_by_n(cairn_root: Path, lock_commit: str | None,
                 new_commit: str | None) -> str:
    """#54 adoption->canonical drift surfacing: a one-line message for how far
    the adopter's installed Cairn ref (*lock_commit*) is behind canonical
    (*new_commit*).

    **Degrades gracefully (R1).** If either ref is missing or the ``unknown``
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
    """Raise PresetError if any token name looks secret-bearing (R9)."""
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
