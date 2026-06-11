#!/usr/bin/env python3
"""Trusted baseline materialization for the differential oracle.

Plan ``2026-06-10-claude-cairn-differential-oracle-gitref-baseline`` Phase 1 (the
*secure* half of the git-ref baseline). Given a baseline ref and an **out-of-band
trusted ref** (supplied by the caller, never read from the evaluated tree), it:

1. resolves the baseline to a full SHA and **proves it is reachable from the
   trusted ref** before any extraction or execution — refusing otherwise (a
   mutable ref name or an evaluated-tree config is insufficient; the trusted ref
   is the authority and is passed in out of band);
2. materializes that ref's tree by **two-pass bounded extraction** of
   ``git archive --format=tar`` — validate the *complete* member table, then
   extract — so the destination stays **empty on any refusal** (never a partial
   write), with fixed v1 resource budgets and no shell pipeline;
3. runs a minimal **pre-flight** so a baseline that cannot run under the current
   template / interpreter / dependency contract is reported as *"baseline not
   runnable here"*, not surfaced as a behavior diff.

Trust architecture (plan Phase 1.1): the *authoritative* verifier runs from a
separate trusted checkout with the evaluated tree as **data**; this module is
that verifier's materialization logic and **never executes target code to decide
trust**. Execute-after-proof holds in every mode: no extraction or run happens
before ``verify_baseline_trust`` succeeds.
"""
from __future__ import annotations

import io
import os
import subprocess
import sys
import tarfile
from pathlib import Path

# --- Fixed v1 extraction limits (plan Phase 1.2; confirming-2 Finding 4) --------
# The single executable posture — the runtime-derived alternative was removed at
# plan-review. A later *reviewed* change may introduce a bounded derivation.
RAW_ARCHIVE_MAX = 64 * 1024 * 1024        # 64 MB — raw tar stream cap (before parse)
MEMBER_MAX = 5_000                         # member count
PER_FILE_MAX = 8 * 1024 * 1024             # 8 MB — per expanded file
TOTAL_EXPANDED_MAX = 128 * 1024 * 1024     # 128 MB — total expanded


class TrustError(RuntimeError):
    """The baseline ref could not be proven trusted — refuse before execution."""


class ExtractionError(RuntimeError):
    """An archive member or resource bound failed — destination left untouched."""


def _git(repo: Path, *args: str, want_bytes: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=not want_bytes, check=False,
    )


def resolve_full_sha(ref: str, repo: Path) -> str:
    """Resolve *ref* to a full 40-hex commit SHA; raise ``TrustError`` if it does
    not resolve to exactly one commit object."""
    p = _git(repo, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}")
    sha = (p.stdout or "").strip()
    if p.returncode != 0 or len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
        raise TrustError(f"ref does not resolve to a commit: {ref!r} ({p.stderr.strip()})")
    return sha


def object_present(sha: str, repo: Path) -> bool:
    """True iff the commit object is present locally (no network)."""
    return _git(repo, "cat-file", "-e", f"{sha}^{{commit}}").returncode == 0


def verify_baseline_trust(
    baseline_ref: str,
    trusted_ref: str,
    repo: Path,
    *,
    allow_fetch: bool = False,
    trusted_remote: str | None = None,
) -> str:
    """Resolve the baseline and **prove it is reachable from the out-of-band
    trusted ref** before any extraction or execution. Returns the baseline's full
    SHA on success; raises ``TrustError`` otherwise.

    * *trusted_ref* is the authority and is supplied out of band by the caller
      (CI / maintainer) — it is never derived from the branch under evaluation.
    * Ancestry, not name: the baseline SHA must be an ancestor of *trusted_ref*
      (so a malicious commit reachable only from the evaluated branch — e.g. the
      two-commit-ancestor attack — is refused).
    * Object presence is required; a missing baseline is a **fail-closed,
      actionable error** unless ``allow_fetch`` is explicitly enabled, in which
      case a targeted fetch is attempted from the **configured trusted remote**
      (never an arbitrary remote), and enough history to prove ancestry must be
      present afterwards.
    """
    repo = Path(repo)
    # The trusted ref is the authority; it must itself resolve in this (trusted) repo.
    trusted_sha = resolve_full_sha(trusted_ref, repo)
    baseline_sha = resolve_full_sha(baseline_ref, repo)

    if not object_present(baseline_sha, repo):
        if not allow_fetch:
            raise TrustError(
                f"baseline object {baseline_sha[:12]} absent (shallow clone?). "
                f"Deepen the clone or fetch it from the trusted source, then retry "
                f"— fetch is fail-closed by default."
            )
        if not trusted_remote:
            raise TrustError("allow_fetch set but no trusted_remote configured — refusing")
        # Targeted fetch of the exact object from the configured trusted remote only,
        # with enough history for the ancestry proof. Network use is explicit + visible.
        f = _git(repo, "fetch", "--no-tags", trusted_remote, baseline_sha)
        if f.returncode != 0 or not object_present(baseline_sha, repo):
            raise TrustError(
                f"targeted fetch of {baseline_sha[:12]} from {trusted_remote!r} failed: "
                f"{f.stderr.strip()}"
            )

    # Reachability: baseline must be an ancestor of the trusted ref.
    anc = _git(repo, "merge-base", "--is-ancestor", baseline_sha, trusted_sha)
    if anc.returncode == 1:
        raise TrustError(
            f"baseline {baseline_sha[:12]} is NOT reachable from the trusted ref "
            f"{trusted_ref!r} ({trusted_sha[:12]}) — refusing to execute unvetted code "
            f"(ancestry-to-HEAD is not trust; the trusted ref is the authority)."
        )
    if anc.returncode != 0:  # e.g. object-unprovable (history too shallow) — distinct from "not ancestor"
        raise TrustError(
            f"ancestry of {baseline_sha[:12]} against {trusted_ref!r} is unprovable "
            f"(insufficient history): {anc.stderr.strip()}"
        )
    return baseline_sha


def _normalize_member_path(name: str) -> str:
    """Return a safe POSIX-relative path for a tar member, or raise
    ``ExtractionError`` on anything that escapes the destination."""
    if name in ("", "."):
        raise ExtractionError(f"empty member name: {name!r}")
    if name.startswith("/") or (len(name) > 1 and name[1] == ":"):
        raise ExtractionError(f"absolute member path refused: {name!r}")
    parts = []
    for part in name.replace("\\", "/").split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            raise ExtractionError(f"path traversal refused: {name!r}")
        parts.append(part)
    if not parts:
        raise ExtractionError(f"member normalizes to nothing: {name!r}")
    return "/".join(parts)


def extract_ref_tree(ref: str, dest: Path, repo: Path) -> Path:
    """**Two-pass, bounded, shell-free** materialization of *ref*'s tree into
    *dest*. ``git archive --format=tar`` (no shell pipeline) is read in-process;
    the **complete member table is validated first**, and extraction happens
    **only if every member passes** — so *dest* stays empty on any refusal.

    Refuses absolute / traversal paths, symlinks, hard links, devices / special
    files, duplicate normalized paths, and file↔directory collisions; enforces the
    fixed v1 budgets (raw archive / member count / per-file / total expanded).
    """
    proc = subprocess.run(
        ["git", "-C", str(repo), "archive", "--format=tar", ref],
        capture_output=True, check=False,
    )
    if proc.returncode != 0:
        raise ExtractionError(f"git archive failed for {ref!r}: {proc.stderr.decode('utf-8', 'replace')[:400]}")
    return _validate_and_extract(proc.stdout, Path(dest))


def _validate_and_extract(raw: bytes, dest: Path) -> Path:
    """The two-pass validator/extractor over raw tar bytes (split out so the
    containment logic is testable with adversarial archives ``git archive`` would
    never itself emit)."""
    dest = Path(dest)
    if len(raw) > RAW_ARCHIVE_MAX:                                   # cap the raw stream BEFORE parsing
        raise ExtractionError(f"raw archive {len(raw)} bytes exceeds cap {RAW_ARCHIVE_MAX}")

    # --- Pass 1: validate the COMPLETE member table; write nothing -------------
    plan: list[tuple[str, bool, tarfile.TarInfo]] = []   # (relpath, is_dir, member)
    files: set[str] = set()
    dirs: set[str] = set()                               # explicit + implied (file parents)
    total = 0
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as tar:
        members = tar.getmembers()
        if len(members) > MEMBER_MAX:
            raise ExtractionError(f"member count {len(members)} exceeds cap {MEMBER_MAX}")
        for m in members:
            if m.issym() or m.islnk():
                raise ExtractionError(f"link member refused: {m.name!r}")
            if m.ischr() or m.isblk() or m.isfifo() or m.isdev():
                raise ExtractionError(f"special/device member refused: {m.name!r}")
            if not (m.isfile() or m.isdir()):
                raise ExtractionError(f"non-regular member refused: {m.name!r} (type {m.type!r})")
            rel = _normalize_member_path(m.name)
            is_dir = m.isdir()
            if is_dir:
                dirs.add(rel)
            else:
                if rel in files:
                    raise ExtractionError(f"duplicate normalized member: {rel!r}")
                if m.size > PER_FILE_MAX:
                    raise ExtractionError(f"member {rel!r} {m.size} bytes exceeds per-file cap {PER_FILE_MAX}")
                total += m.size
                if total > TOTAL_EXPANDED_MAX:
                    raise ExtractionError(f"total expanded {total} bytes exceeds cap {TOTAL_EXPANDED_MAX}")
                files.add(rel)
                parent = rel.rsplit("/", 1)[0] if "/" in rel else ""
                while parent:                            # every parent prefix is an implied dir
                    dirs.add(parent)
                    parent = parent.rsplit("/", 1)[0] if "/" in parent else ""
            plan.append((rel, is_dir, m))
        clash = files & dirs                             # a path used as BOTH file and directory
        if clash:
            raise ExtractionError(f"file/directory collision: {sorted(clash)[:3]}")

        # --- Pass 2: every member validated — extract regular files + dirs ----
        dest.mkdir(parents=True, exist_ok=True)
        for rel, is_dir, m in plan:
            target = dest / rel
            if is_dir:
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            src = tar.extractfile(m)
            data = src.read() if src is not None else b""
            if len(data) > PER_FILE_MAX:                            # defensive: actual bytes, not just header
                raise ExtractionError(f"member {rel!r} expanded beyond per-file cap")
            target.write_bytes(data)
            target.chmod(0o755 if (m.mode & 0o100) else 0o644)
    return dest


def preflight(engine: Path, repo: Path) -> bool:
    """A minimal baseline-executability check (plan Phase 1.3 / Antigravity S4):
    can the extracted baseline engine run *at all* under the current interpreter
    / environment? Returns ``False`` so the caller can report *"baseline not
    runnable here"* instead of surfacing an environment incompatibility as a
    behavior diff."""
    try:
        p = subprocess.run(
            [sys.executable, str(engine), "--help"],
            capture_output=True, text=True, cwd=str(repo), check=False, timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return p.returncode == 0


if __name__ == "__main__":  # pragma: no cover - manual smoke
    raise SystemExit("module: import-only (use the oracle harness)")
