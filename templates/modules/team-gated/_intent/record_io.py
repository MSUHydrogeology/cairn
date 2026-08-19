#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Work-intent engine — record-I/O subsystem .

The claim-ledger record schema (claim/release dataclasses), the best-effort
atomic JSONL append, and the read-side helpers (active intents, conflict check,
log iteration). Depends only on the shared-core leaf.

## Substrate

The active intent log is a single JSON-lines file at ``dev/intents.jsonl``
(gitignored; the scaffold seeds the entry). Each line is one record; two event
types: ``claim`` (``event``, ``id``, ``ts``, ``agent``, ``files``, ``action``,
optional ``stem``) and ``release`` (``event``, ``id``, ``ts``, optional
``commit``). Active intents = claims without a matching release event (matched by
shared ``id``).

## Atomicity -- best-effort, filesystem-dependent

Concurrent appenders rely on the **implementation shape**, NOT on a POSIX
guarantee:

* ``os.open(path, O_WRONLY | O_APPEND | O_CREAT)`` -- the kernel positions every
  write at current EOF.
* A single ``os.write(fd, bytes)`` call per record, payload < 512 bytes (a
  conservative small-write floor).
* No buffered-writer layer (text-mode ``open(..., 'a')`` would emit multiple
  ``write(2)`` calls and break the atomicity).

This is **best-effort and filesystem-dependent**. POSIX specifies atomic appends
for pipes/FIFOs under ``PIPE_BUF``, *not* for regular files; the small
single-``write`` shape is non-interleaving on the **local** filesystems this
tooling is exercised on (APFS, ext4, xfs, btrfs). It is **not** guaranteed on
**networked or overlay** filesystems -- NFS, SMB/CIFS, Windows network shares,
and container overlay FS can interleave or reorder appends. A team running the
intent log on such a filesystem, or at very high concurrency, should treat the
append as advisory and prefer a local checkout for the ``dev/`` tree.
"""
from __future__ import annotations

import dataclasses
import datetime
import json
import os
import sys
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Sequence

from .shared import INTENTS_LOG_PATH, normalize_path


#: Conservative per-record size cap.  Records at or below this size stay
#: inside the small-write window local filesystems respect for
#: non-interleaved concurrent appends; larger records are rejected with
#: a precise diagnostic.
RECORD_SIZE_CAP = 512


@dataclasses.dataclass(frozen=True)
class ClaimRecord:
    """A ``claim`` event in the intent log."""

    id: str
    ts: str
    agent: str
    files: List[str]
    action: str
    stem: Optional[str] = None
    event: str = "claim"

    def to_dict(self) -> Dict[str, object]:
        d: Dict[str, object] = {
            "event": self.event,
            "id": self.id,
            "ts": self.ts,
            "agent": self.agent,
            "files": list(self.files),
            "action": self.action,
        }
        if self.stem is not None:
            d["stem"] = self.stem
        return d


@dataclasses.dataclass(frozen=True)
class ReleaseRecord:
    """A ``release`` event in the intent log."""

    id: str
    ts: str
    commit: Optional[str] = None
    event: str = "release"

    def to_dict(self) -> Dict[str, object]:
        d: Dict[str, object] = {
            "event": self.event,
            "id": self.id,
            "ts": self.ts,
        }
        if self.commit is not None:
            d["commit"] = self.commit
        return d


def _record_bytes(record_dict: Dict[str, object]) -> bytes:
    """Serialize a record dict to a single JSON line + ``\\n``, UTF-8.

    Raises ``ValueError`` when the encoded record meets or exceeds
    :data:`RECORD_SIZE_CAP`, with a diagnostic naming the cap, the
    actual size, and a remediation.
    """
    line = json.dumps(record_dict, separators=(",", ":"), ensure_ascii=False)
    payload = (line + "\n").encode("utf-8")
    if len(payload) >= RECORD_SIZE_CAP:
        files = record_dict.get("files") or []
        files_bytes = len(json.dumps(files).encode("utf-8"))
        action = record_dict.get("action") or ""
        action_bytes = len(json.dumps(action).encode("utf-8"))
        dominant = "paths" if files_bytes >= action_bytes else "action"
        raise ValueError(
            f"intent record is {len(payload)} bytes; cap is "
            f"{RECORD_SIZE_CAP} bytes. Dominant contributor: "
            f"{dominant} ({files_bytes} bytes paths / "
            f"{action_bytes} bytes action). Consider a shorter --action "
            f"and/or passing --stem <topic> to substitute a short topic "
            f"key for verbose action text."
        )
    return payload


def append_record(
    record_dict: Dict[str, object],
    *,
    log_path: Optional[Path] = None,
) -> None:
    """Append one record to the active intent log (best-effort atomic).

    Uses ``os.open(O_WRONLY | O_APPEND | O_CREAT)`` + a single
    ``os.write`` of a < cap payload, no buffered-writer layer.  Raises
    ``ValueError`` for over-cap records; raises ``IOError`` on the
    should-never-happen partial-write case so the failure surfaces
    loudly.
    """
    target = log_path if log_path is not None else INTENTS_LOG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = _record_bytes(record_dict)
    fd = os.open(str(target), os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        written = os.write(fd, payload)
        if written != len(payload):
            raise IOError(
                f"partial write to {target}: wrote {written} of "
                f"{len(payload)} bytes (atomicity contract broken; "
                f"investigate filesystem / platform interaction)"
            )
    finally:
        os.close(fd)


def generate_id(agent: str, ts: datetime.datetime) -> str:
    """Build a claim id: ``<agent>-<YYYYMMDD>T<HHMMSS>-<microsecond>``.

    The microsecond suffix guarantees per-call uniqueness within one
    agent's same-second issuances.
    """
    safe_agent = agent.replace("/", "-").replace(" ", "-").lower()
    return (
        f"{safe_agent}-{ts.strftime('%Y%m%dT%H%M%S')}-"
        f"{ts.microsecond:06d}"
    )


def write_claim(
    *,
    agent: str,
    files: Sequence[str],
    action: str,
    stem: Optional[str] = None,
    ts: Optional[datetime.datetime] = None,
    log_path: Optional[Path] = None,
    repo_root: Optional[Path] = None,
) -> ClaimRecord:
    """Append a claim record; return the :class:`ClaimRecord`."""
    if ts is None:
        ts = datetime.datetime.now().astimezone()
    normalized_files = [normalize_path(p, repo_root=repo_root) for p in files]
    claim_id = generate_id(agent, ts)
    record = ClaimRecord(
        id=claim_id,
        ts=ts.isoformat(),
        agent=agent,
        files=normalized_files,
        action=action,
        stem=stem,
    )
    append_record(record.to_dict(), log_path=log_path)
    return record


def write_release(
    *,
    claim_id: str,
    ts: Optional[datetime.datetime] = None,
    commit: Optional[str] = None,
    log_path: Optional[Path] = None,
) -> ReleaseRecord:
    """Append a release record; return the :class:`ReleaseRecord`."""
    if ts is None:
        ts = datetime.datetime.now().astimezone()
    record = ReleaseRecord(id=claim_id, ts=ts.isoformat(), commit=commit)
    append_record(record.to_dict(), log_path=log_path)
    return record


def read_log(log_path: Optional[Path] = None) -> List[Dict[str, object]]:
    """Read every record; skip malformed lines with a stderr warning."""
    target = log_path if log_path is not None else INTENTS_LOG_PATH
    if not target.exists():
        return []
    records: List[Dict[str, object]] = []
    with target.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                sys.stderr.write(
                    f"intent: skipping malformed line {line_no} in "
                    f"{target}: {exc}\n"
                )
                continue
    return records


def active_intents(log_path: Optional[Path] = None) -> List[Dict[str, object]]:
    """Return the claim records that lack a matching release (by id)."""
    records = read_log(log_path=log_path)
    released_ids = set()
    claims_by_id: Dict[str, Dict[str, object]] = {}
    for record in records:
        event = record.get("event")
        rid = record.get("id")
        if not isinstance(rid, str):
            continue
        if event == "release":
            released_ids.add(rid)
        elif event == "claim":
            claims_by_id[rid] = record
    return [
        claim for cid, claim in claims_by_id.items()
        if cid not in released_ids
    ]


#: Default age, in days, past which a RELEASED claim/release pair is garbage on
#: the coordination surface.  Sited to mirror ``lifecycle``'s
#: ``_REFLECTION_GRACE_DAYS``; the two windows are independent on purpose (a
#: reflection is a document, a claim is a lock).
DEFAULT_PRUNE_GRACE_DAYS = 30

#: How recent an *unreleased* claim must be to count as a **live session** and
#: refuse a prune.  Mirrors ``conflict.DEFAULT_CLAIM_TTL_HOURS`` -- the value
#: that module already uses to decide a claim is fresh enough to block a commit.
#: Duplicated as a literal rather than imported because ``conflict`` imports
#: *this* module; the layering runs one way.
#:
#: **Why this is not "any unreleased claim".**  A never-released claim IS active
#: by :func:`active_intents`, so refusing on any active claim would make
#: :func:`prune_released_pairs` refuse forever in exactly the repositories that
#: need it -- and would make its ``stale_unreleased`` report unreachable.  The
#: distinction that matters is *live appender* (refuse; a rewrite could lose its
#: claim) versus *dead lock* (report it, keep it, prune around it).
LIVE_CLAIM_HOURS = 4.0


def prune_released_pairs(
    *,
    older_than_days: int = DEFAULT_PRUNE_GRACE_DAYS,
    log_path: Optional[Path] = None,
    now: Optional[datetime.datetime] = None,
    dry_run: bool = False,
    live_within_hours: float = LIVE_CLAIM_HOURS,
) -> Dict[str, object]:
    """Drop ``claim``+``release`` **pairs** whose release is older than N days.

    The intent log is a *coordination surface*, not an archive: it is gitignored,
    local to one checkout, and exists to answer "who holds which paths right
    now".  A released pair from a month ago answers nothing, and
    :func:`active_intents` replays the whole file on the pre-commit path, so
    growth is a cost on the most frequent operation in the project.

    **Three invariants, each load-bearing and each tested:**

    1. **Pairwise, never a lone release.**  :func:`active_intents` derives the
       active set as *claims minus released ids*.  Removing a release while its
       claim survives would **resurrect that claim as active** and block its
       paths forever, with no release left to match it.  A pair is therefore
       eligible only when **both** records are present, and both leave together.
       The observable consequence: this function can never *increase* the active
       set, and can never change it at all.
    2. **An unreleased claim is never deleted.**  A month-old claim with no
       release means a session died holding a lock.  That is a bug signal and it
       is what blocks other agents; deleting it would make the surface tidier and
       the coordination worse.  Such claims are **reported** in
       ``stale_unreleased`` for the caller to surface, and left in place.
    3. **A line that cannot be parsed is never dropped.**  :func:`read_log`
       skips malformed lines with a warning; rebuilding the file from its output
       would silently delete them.  This function walks **raw lines** and
       preserves anything it cannot parse, byte for byte.

    **The concurrency residual, stated accurately.**  Rewriting is in tension
    with this module's lock-free append path (see the Atomicity note above).  A
    record appended between the snapshot and the replace does not survive it.
    Three things narrow that, and none of them closes it:

    * the caller is the **full handoff**, which by operating rule is the
      session-day's **last** act, run after other sessions have ended -- so the
      window is *quiet*, not merely narrow.  That rule is a precondition of this
      function, stated where the handoff owner reads it (``session-end``'s
      ``SKILL.md``, step 1);
    * a claim held within *live_within_hours* refuses the prune outright;
    * the ledger's size is re-checked immediately before the replace, so a
      detected concurrent append **skips** the prune rather than dropping it.

    What a missed window costs is **one advisory record**, degrading a collision
    *warning*.  This file is not a mutual-exclusion lock and never was -- the
    Atomicity note above says appends are best-effort and advisory.  An earlier
    draft of this docstring called a lost claim "a lost lock"; that overstated
    it, and the overstatement is what made a scratch-file cleanup look like a
    concurrency-critical change.

    **The consequence is bounded, and the bound is structural.**  A claim past
    ``conflict.DEFAULT_CLAIM_TTL_HOURS`` is *stale*: it still warns but never
    **blocks** a commit, so an abandoned session cannot wedge anyone.  This
    function refuses on any unreleased claim *newer* than that same horizon.
    The two numbers are deliberately equal, so a release lost to the window can
    only belong to a claim already past the blocking horizon.  The worst case is
    therefore a warning row that does not clear -- not a blocked commit -- on a
    gitignored, single-checkout file with no provenance role, correctable by
    appending one release line.  What is at risk is *wasted effort*, which is
    also the entire hazard this surface exists to reduce.

    Note the refusal is scoped to a **recent** unreleased claim, not to any
    active one: every unreleased claim is active by :func:`active_intents`, so
    refusing on all of them would refuse forever.

    Returns a report dict; writes nothing when *dry_run*.
    """
    target = log_path if log_path is not None else INTENTS_LOG_PATH
    report: Dict[str, object] = {
        "path": str(target), "pruned_pairs": 0, "pruned_lines": 0,
        "kept_lines": 0, "unparseable_kept": 0, "stale_unreleased": [],
        "refused": None, "dry_run": bool(dry_run),
    }
    if not target.exists():
        return report

    raw_lines = target.read_text(encoding="utf-8").splitlines(keepends=True)

    # Parse what we can; remember which raw index each parsed record came from.
    parsed: List[tuple] = []          # (index, record dict)
    unparseable: set = set()
    for idx, line in enumerate(raw_lines):
        if not line.strip():
            continue
        try:
            parsed.append((idx, json.loads(line.strip())))
        except json.JSONDecodeError:
            unparseable.add(idx)

    releases: Dict[str, str] = {}     # id -> release ts
    claims: Dict[str, Dict[str, object]] = {}
    for _idx, rec in parsed:
        rid = rec.get("id")
        if not isinstance(rid, str):
            continue
        if rec.get("event") == "release":
            ts = rec.get("ts")
            releases[rid] = ts if isinstance(ts, str) else ""
        elif rec.get("event") == "claim":
            claims[rid] = rec

    reference = now if now is not None else datetime.datetime.now(
        datetime.timezone.utc)
    cutoff = reference - datetime.timedelta(days=older_than_days)
    live_edge = reference - datetime.timedelta(hours=live_within_hours)

    def _parse_ts(ts_text: object) -> Optional[datetime.datetime]:
        if not isinstance(ts_text, str) or not ts_text:
            return None
        try:
            when = datetime.datetime.fromisoformat(ts_text)
        except (ValueError, TypeError):
            return None
        return when.replace(tzinfo=datetime.timezone.utc) if when.tzinfo is None \
            else when

    # Refuse only for a claim recent enough to be a LIVE session,
    # because a rewrite can lose a record such a session is appending.  An old
    # unreleased claim is a dead lock, not an appender -- it is reported below.
    live_ids = []
    for rid, claim in claims.items():
        if rid in releases:
            continue
        when = _parse_ts(claim.get("ts"))
        if when is None or when >= live_edge:
            live_ids.append(rid)      # unparseable ts counts as live: fail-safe
    if live_ids:
        report["refused"] = (
            f"{len(live_ids)} claim(s) held within the last "
            f"{live_within_hours}h -- a live session may be appending; run this "
            f"only at a quiet serialization point"
        )
        report["kept_lines"] = len(raw_lines)
        return report

    def _older(ts_text: object) -> bool:
        """True when *ts_text* parses and predates the cutoff.  An unparseable
        or absent timestamp is treated as NOT old -- fail-safe, since the cost
        of keeping a record is bytes and the cost of dropping one is a lock."""
        when = _parse_ts(ts_text)
        return when is not None and when < cutoff

    prunable = {rid for rid, ts in releases.items()
                if rid in claims and _older(ts)}

    # Invariant 2: report, never delete.
    for rid, claim in claims.items():
        if rid in releases:
            continue
        if _older(claim.get("ts")):
            report["stale_unreleased"].append({
                "id": rid, "agent": claim.get("agent"),
                "ts": claim.get("ts"), "files": claim.get("files"),
            })

    drop_indices = {idx for idx, rec in parsed
                    if isinstance(rec.get("id"), str)
                    and rec["id"] in prunable
                    and rec.get("event") in ("claim", "release")}
    # Invariant 3: never drop what we could not parse.
    drop_indices -= unparseable

    report["pruned_pairs"] = len(prunable)
    report["pruned_lines"] = len(drop_indices)
    report["kept_lines"] = len(raw_lines) - len(drop_indices)
    report["unparseable_kept"] = len(unparseable)

    if dry_run or not drop_indices:
        return report

    kept = [ln for idx, ln in enumerate(raw_lines) if idx not in drop_indices]
    payload = "".join(kept).encode("utf-8")

    # Exclusive, symlink-proof temp creation.  The previous fixed
    # ``.prune-tmp`` name written via ``Path.write_text`` FOLLOWED a
    # pre-existing symlink: a hostile or stale link at that path was truncated
    # to zero bytes and ``os.replace`` then made the ledger itself the symlink.
    # ``O_EXCL`` refuses an existing path and ``O_NOFOLLOW`` refuses a link, so
    # neither is reachable now.
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    tmp = target.with_name(f"{target.name}.prune-{os.getpid()}.tmp")
    try:
        fd = os.open(str(tmp), flags, 0o644)
    except FileExistsError:
        report["refused"] = f"temporary path {tmp.name} already exists"
        report["pruned_pairs"] = 0
        report["pruned_lines"] = 0
        report["kept_lines"] = len(raw_lines)
        return report
    try:
        os.write(fd, payload)
    finally:
        os.close(fd)

    # Concurrency residual, narrowed rather than solved.  Ordinary
    # claim/release appends are lock-free by design -- see this module's
    # Atomicity note -- so a record appended between the snapshot above and the
    # replace below would not survive it.  Re-checking the size immediately
    # before the replace turns "silently dropped" into "prune skipped, try
    # again next handoff", which is the right trade for an **advisory**
    # coordination hint in a gitignored file.  It does not eliminate the window,
    # and this comment does not pretend it does: a write landing between this
    # check and ``os.replace`` is still lost.  What is lost is one advisory
    # record, degrading a collision *warning* -- not a mutual-exclusion lock,
    # which this file has never been.
    try:
        if target.stat().st_size != sum(len(ln.encode("utf-8"))
                                        for ln in raw_lines):
            tmp.unlink(missing_ok=True)
            report["refused"] = (
                "the ledger changed while pruning -- skipped, so no concurrent "
                "append is dropped; it will be retried next time"
            )
            report["pruned_pairs"] = 0
            report["pruned_lines"] = 0
            report["kept_lines"] = len(raw_lines)
            return report
        os.replace(str(tmp), str(target))
    except OSError:
        tmp.unlink(missing_ok=True)
        raise
    return report


def conflict_check(
    files: Sequence[str],
    *,
    log_path: Optional[Path] = None,
    repo_root: Optional[Path] = None,
) -> List[Dict[str, object]]:
    """Return active intents whose file set intersects ``files``."""
    query = {normalize_path(p, repo_root=repo_root) for p in files}
    if not query:
        return []
    hits: List[Dict[str, object]] = []
    for claim in active_intents(log_path=log_path):
        claim_files = claim.get("files") or []
        if not isinstance(claim_files, list):
            continue
        claim_set = {
            normalize_path(str(f), repo_root=repo_root) for f in claim_files
        }
        if claim_set & query:
            hits.append(claim)
    return hits


def iter_log(log_path: Optional[Path] = None) -> Iterator[Dict[str, object]]:
    """Yield records one at a time; same forgiveness as :func:`read_log`."""
    target = log_path if log_path is not None else INTENTS_LOG_PATH
    if not target.exists():
        return
    with target.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                yield json.loads(stripped)
            except json.JSONDecodeError as exc:
                sys.stderr.write(
                    f"intent: skipping malformed line {line_no} in "
                    f"{target}: {exc}\n"
                )
                continue
