#!/usr/bin/env python3
"""Data-only gate-transition checker (plan Phase 0.3 / 4.2).

The bootstrap reality the External-Security review closed (confirming-2 Finding
1): implementing the new verifier in the evaluated target does NOT make its SHA
trusted. So a candidate's gate-control bytes are promoted only when they
**exactly match an externally-authored promotion manifest** — checked here
**without executing the candidate** (hashes + paths + nonce only).

This checker is itself trusted: it is **pinned in the trusted checkout before any
target edit** (supervised Phase 0). A candidate that alters the checker is
rejected because the promotion manifest pins the checker's own expected hash.
The *pinning, manifest authoring, and the actual promotion / re-anchor* are the
supervised Phase 0/4 steps — this module is only the verification logic they run.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


class PromotionError(ValueError):
    """The promotion manifest is malformed."""


@dataclass
class PromotionManifest:
    nonce: str                                   # audit id (the trusted-ref CAS is the replay guard)
    prior_anchor: str                            # the trusted prior SHA this builds on (A)
    candidate_sha: str                           # the IMMUTABLE candidate commit promoted (C)
    checker_hash: str                            # expected sha256 of THIS checker file
    # The two-stage contract (re-review round 4): the reviewed authorization also
    # binds the Stage-A evidence bundle and the prospective manifest bytes, so the
    # data-only Stage B promotes EXACTLY the reviewed evidence — never a substitute.
    evidence_hash: str = ""                      # expected sha256 of the Stage-A evidence bundle
    prospective_manifest_hash: str = ""          # expected sha256 of the prospective gate manifest
    files: dict[str, str] = field(default_factory=dict)   # path -> expected new sha256


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _resolve_sha(repo: Path, ref: str) -> str:
    """Resolve *ref* to a full 40-hex commit SHA in *repo*; raise on failure."""
    p = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"],
        capture_output=True, text=True, check=False)
    sha = (p.stdout or "").strip()
    if p.returncode != 0 or len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
        raise PromotionError(f"ref does not resolve to a commit: {ref!r} ({p.stderr.strip()})")
    return sha


def sha256_git_object(repo: Path, sha: str, rel: str) -> str | None:
    """The sha256 of *rel* as it exists in the **immutable git object** at *sha*
    (``git show <sha>:<rel>``), NOT the mutable worktree (re-review Finding 3 —
    a dirty/raced worktree cannot alter what is validated). ``None`` if absent."""
    p = subprocess.run(
        ["git", "-C", str(repo), "show", f"{sha}:{rel}"],
        capture_output=True, check=False)
    if p.returncode != 0:
        return None
    return "sha256:" + hashlib.sha256(p.stdout).hexdigest()


def parse_promotion(text: str) -> PromotionManifest:
    """Parse the promotion manifest (stdlib subset: ``key: value`` scalars and a
    ``files:`` block of ``  path: sha256:...`` lines)."""
    scalars: dict[str, str] = {}
    files: dict[str, str] = {}
    in_files = False
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw[:1].isspace()
        line = raw.strip()
        if line == "files:":
            in_files = True
            continue
        if ":" not in line:
            raise PromotionError(f"unparseable line: {line!r}")
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if in_files and indented:
            files[key] = val
        else:
            in_files = False
            scalars[key] = val
    try:
        return PromotionManifest(
            nonce=scalars["nonce"], prior_anchor=scalars["prior_anchor"],
            candidate_sha=scalars["candidate_sha"],
            checker_hash=scalars["checker_hash"],
            evidence_hash=scalars["evidence_hash"],
            prospective_manifest_hash=scalars["prospective_manifest_hash"],
            files=files,
        )
    except KeyError as e:
        raise PromotionError(f"promotion manifest missing field: {e}") from e


def derive_changed_gate_files(repo: Path, prior_anchor: str, candidate: str, is_sensitive) -> list[str]:
    """**Independently** derive the changed gate/sensitive file set via
    ``git diff --name-only prior_anchor..candidate``, filtered by *is_sensitive* —
    so a permissive caller cannot omit an actually-changed sensitive file."""
    out = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-only", f"{prior_anchor}..{candidate}"],
        capture_output=True, text=True, check=False)
    if out.returncode != 0:
        raise PromotionError(f"git diff {prior_anchor[:12]}..{candidate} failed: {out.stderr.strip()}")
    return sorted(f for f in out.stdout.splitlines() if f.strip() and is_sensitive(f.strip()))


def _nonce_slot(nonce_ledger_dir: Path, nonce: str) -> Path:
    """The one-file-per-nonce slot in the ledger DIRECTORY (the name is the nonce's
    digest so an arbitrary nonce string is a safe filename)."""
    digest = hashlib.sha256(nonce.encode("utf-8")).hexdigest()
    return Path(nonce_ledger_dir) / f"{digest}.used"


def nonce_used(nonce_ledger_dir: Path, nonce: str) -> bool:
    """Read-only: has *nonce* already been claimed in this ledger directory?"""
    return _nonce_slot(nonce_ledger_dir, nonce).exists()


def claim_nonce(nonce_ledger_dir: Path, nonce: str) -> bool:
    """**Atomically** claim *nonce* (re-review Finding 3). Returns ``True`` if this
    call won the claim, ``False`` if it was already used — the win is decided by an
    ``O_CREAT | O_EXCL`` create, which is atomic on POSIX, so two concurrent
    claimants cannot both succeed. The authoritative single-use enforcement; the
    ledger directory is owned by the supervised composing command, never a
    caller-arbitrary path per validation call."""
    slot = _nonce_slot(nonce_ledger_dir, nonce)
    slot.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(slot), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(nonce + "\n")
    return True


def check_promotion(
    repo: Path,
    manifest: PromotionManifest,
    *,
    prior_anchor_actual: str,
    candidate: str,
    is_sensitive,
    checker_path: str = "bootstrap/tests/_gate_transition.py",
) -> tuple[bool, list[str]]:
    """**Data-only, pure** validation that the candidate's gate-control bytes
    EXACTLY match the externally-authored *manifest*, **bound to one immutable
    candidate SHA**. The candidate is **never executed**, and this function is
    **side-effect free** — it does NOT claim the nonce (the supervised composing
    command claims it atomically *after* validation, so a failed validation never
    consumes authority; re-review Finding 3).

    HOLDs on: a candidate that altered the transition checker; a *candidate* ref
    whose resolved SHA differs from the manifest's pinned ``candidate_sha`` (a
    moving ref / wrong candidate); replay against a different prior anchor; an
    **independently-derived** changed gate/sensitive file omitted from (or a file
    in the manifest not actually changed); a permitted-path file whose bytes **in
    the immutable candidate object** differ from its reviewed hash."""
    repo = Path(repo)
    holds: list[str] = []

    # 1. The checker itself must be the pinned one — hashed from the EXECUTING module
    #    file (re-review round-5 F1b), not the mutable target worktree, so the running
    #    verifier code is what is pinned (a candidate cannot alter the deciding code).
    if sha256_file(Path(__file__)) != manifest.checker_hash:
        return False, ["transition checker (executing code) does not match the pinned checker hash"]

    # 2. The candidate ref must resolve to the manifest's PINNED immutable SHA
    #    (a moving ref, or a manifest aimed at a different candidate, refuses).
    candidate_sha = _resolve_sha(repo, candidate)
    if candidate_sha != manifest.candidate_sha:
        return False, [f"candidate SHA mismatch (moving-ref/wrong-candidate refused): "
                       f"manifest {manifest.candidate_sha[:12]} vs resolved {candidate_sha[:12]}"]

    # 3. Replay / wrong-base: the promotion must build on the expected prior anchor.
    if manifest.prior_anchor != prior_anchor_actual:
        return False, [f"prior-anchor mismatch (replay refused): manifest "
                       f"{manifest.prior_anchor[:12]} vs actual {prior_anchor_actual[:12]}"]

    # 4. INDEPENDENT changed-file derivation against the IMMUTABLE candidate SHA —
    #    exact equality with the manifest set (omitted changed file OR unmanifested
    #    gate file both refuse).
    changed = set(derive_changed_gate_files(repo, prior_anchor_actual, candidate_sha, is_sensitive))
    declared = set(manifest.files)
    for rel in sorted(changed - declared):
        holds.append(f"changed gate/sensitive file is NOT in the promotion manifest: {rel}")
    for rel in sorted(declared - changed):
        holds.append(f"manifest authorizes a file that is not an actual changed gate/sensitive file: {rel}")

    # 5. Each manifest file's bytes IN THE CANDIDATE OBJECT must match its reviewed
    #    new hash exactly (read from the git object, not the mutable worktree).
    for rel, expected in manifest.files.items():
        actual = sha256_git_object(repo, candidate_sha, rel)
        if actual is None:
            holds.append(f"authorized gate file absent in candidate object: {rel}")
        elif actual != expected:
            holds.append(f"gate file in candidate differs from its reviewed hash: {rel} "
                         f"(decisive: object bytes != promotion manifest)")

    return (not holds), holds
