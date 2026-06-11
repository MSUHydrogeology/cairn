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


def check_promotion(
    repo: Path,
    manifest: PromotionManifest,
    *,
    gate_control_paths: list[str],
    prior_anchor_actual: str,
    checker_path: str = "bootstrap/tests/_gate_transition.py",
) -> tuple[bool, list[str]]:
    """**Data-only** validation that the candidate's gate-control bytes EXACTLY
    match the externally-authored *manifest*. The candidate is **never executed**.

    HOLDs on: a candidate that altered the transition checker; replay against a
    different prior anchor; a permitted-path file whose current bytes differ from
    its reviewed hash (the decisive regression — bytes changed after review); an
    omitted authorized file; an extra changed gate-control file not in the
    manifest.
    """
    repo = Path(repo)
    holds: list[str] = []

    # 1. The checker itself must be the pinned one (a candidate cannot alter it).
    actual_checker = sha256_file(repo / checker_path)
    if actual_checker != manifest.checker_hash:
        holds.append("transition checker has been altered (candidate may not modify the checker)")
        return False, holds                      # fail hard: the verifier is untrusted

    # 2. Replay / wrong-base: the promotion must build on the expected prior anchor.
    if manifest.prior_anchor != prior_anchor_actual:
        holds.append(f"prior-anchor mismatch (replay refused): manifest {manifest.prior_anchor[:12]} "
                     f"vs actual {prior_anchor_actual[:12]}")
        return False, holds

    # 3. Every authorized gate-control path must match its reviewed new hash exactly.
    for rel in gate_control_paths:
        expected = manifest.files.get(rel)
        if expected is None:
            holds.append(f"authorized gate file omitted from the promotion manifest: {rel}")
            continue
        p = repo / rel
        if not p.is_file():
            holds.append(f"authorized gate file missing on disk: {rel}")
            continue
        actual = sha256_file(p)
        if actual != expected:
            holds.append(f"gate file changed after its reviewed hash was recorded: {rel} "
                         f"(decisive: bytes != promotion manifest)")

    # 4. No EXTRA file in the manifest beyond the authorized gate-control set
    #    (the checker entry itself excepted — it is pinned via checker_hash).
    extra = set(manifest.files) - set(gate_control_paths)
    for rel in sorted(extra):
        holds.append(f"promotion manifest authorizes a file outside the gate-control set: {rel}")

    return (not holds), holds
