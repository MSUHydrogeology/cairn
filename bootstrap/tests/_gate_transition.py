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
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


class PromotionError(ValueError):
    """The promotion manifest is malformed."""


@dataclass
class PromotionManifest:
    nonce: str                                   # single-use; replay is refused
    prior_anchor: str                            # the trusted prior SHA this builds on
    checker_hash: str                            # expected sha256 of THIS checker file
    files: dict[str, str] = field(default_factory=dict)   # path -> expected new sha256


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


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
            checker_hash=scalars["checker_hash"], files=files,
        )
    except KeyError as e:
        raise PromotionError(f"promotion manifest missing field: {e}") from e


def derive_changed_gate_files(repo: Path, prior_anchor: str, candidate: str, is_sensitive) -> list[str]:
    """**Independently** derive the changed gate/sensitive file set (P1.3) via
    ``git diff --name-only prior_anchor..candidate``, filtered by *is_sensitive* —
    so a permissive caller cannot omit an actually-changed sensitive file."""
    out = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-only", f"{prior_anchor}..{candidate}"],
        capture_output=True, text=True, check=False)
    if out.returncode != 0:
        raise PromotionError(f"git diff {prior_anchor[:12]}..{candidate} failed: {out.stderr.strip()}")
    return sorted(f for f in out.stdout.splitlines() if f.strip() and is_sensitive(f.strip()))


def nonce_used(nonce_ledger: Path, nonce: str) -> bool:
    p = Path(nonce_ledger)
    return p.is_file() and nonce in p.read_text(encoding="utf-8").split()


def _consume_nonce(nonce_ledger: Path, nonce: str) -> None:
    p = Path(nonce_ledger)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:         # append-only single-use ledger
        f.write(nonce + "\n")


def check_promotion(
    repo: Path,
    manifest: PromotionManifest,
    *,
    prior_anchor_actual: str,
    candidate: str,
    is_sensitive,
    nonce_ledger: Path,
    checker_path: str = "bootstrap/tests/_gate_transition.py",
) -> tuple[bool, list[str]]:
    """**Data-only** validation that the candidate's gate-control bytes EXACTLY
    match the externally-authored *manifest*. The candidate is **never executed**.

    HOLDs on: a candidate that altered the transition checker; replay against a
    different prior anchor **or a consumed nonce**; an **independently-derived**
    changed gate/sensitive file omitted from (or a file in the manifest not
    actually changed); a permitted-path file whose current bytes differ from its
    reviewed hash (the decisive regression). On a clean pass the nonce is
    **consumed** (single-use)."""
    repo = Path(repo)
    holds: list[str] = []

    # 1. The checker itself must be the pinned one (a candidate cannot alter it).
    if sha256_file(repo / checker_path) != manifest.checker_hash:
        return False, ["transition checker has been altered (candidate may not modify the checker)"]

    # 2. Replay / wrong-base: the promotion must build on the expected prior anchor.
    if manifest.prior_anchor != prior_anchor_actual:
        return False, [f"prior-anchor mismatch (replay refused): manifest "
                       f"{manifest.prior_anchor[:12]} vs actual {prior_anchor_actual[:12]}"]

    # 3. Single-use nonce: a consumed nonce is a replay.
    if nonce_used(nonce_ledger, manifest.nonce):
        return False, [f"nonce {manifest.nonce!r} already consumed (replay refused)"]

    # 4. INDEPENDENT changed-file derivation — exact equality with the manifest set
    #    (an omitted changed file OR an unmanifested gate file both refuse).
    changed = set(derive_changed_gate_files(repo, prior_anchor_actual, candidate, is_sensitive))
    declared = set(manifest.files)
    for rel in sorted(changed - declared):
        holds.append(f"changed gate/sensitive file is NOT in the promotion manifest: {rel}")
    for rel in sorted(declared - changed):
        holds.append(f"manifest authorizes a file that is not an actual changed gate/sensitive file: {rel}")

    # 5. Each manifest file's current bytes must match its reviewed new hash exactly.
    for rel, expected in manifest.files.items():
        p = repo / rel
        if not p.is_file():
            holds.append(f"authorized gate file missing on disk: {rel}")
            continue
        if sha256_file(p) != expected:
            holds.append(f"gate file changed after its reviewed hash was recorded: {rel} "
                         f"(decisive: bytes != promotion manifest)")

    ok = not holds
    if ok:
        _consume_nonce(nonce_ledger, manifest.nonce)     # atomically consume on success
    return ok, holds
