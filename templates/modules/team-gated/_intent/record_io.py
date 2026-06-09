#!/usr/bin/env python3
"""Work-intent engine — record-I/O subsystem (intent-split phase A2).

The claim-ledger record schema (claim/release dataclasses), the best-effort
atomic JSONL append, and the read-side helpers (active intents, conflict check,
log iteration). Depends only on the shared-core leaf.
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
