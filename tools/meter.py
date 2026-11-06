#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Pure usage readers. No private-source access or collection is implemented.

Inputs are caller-supplied JSONL bytes, currently exercised only synthetically.
Directory digests are source evidence, NOT verified project identities. No
reader result is a project aggregate. The future consent/file-safety layer and
allowlisted local Git verification must precede any private use or export.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
import argparse
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


READER_VERSION = "cairn-source-readers/1"
CODEX_CONTRACT = "49f0c6022596c361fe676a5c4738fb2be34e3a93"  # vendor-ok: pins reviewed input contract
MAX_COUNTER = 2**63 - 1
TOOLS = ("codex", "claude", "antigravity")  # vendor-ok: source adapters
CONFIG_VERSION = 1
MAX_CONFIG_BYTES = 256 * 1024
MAX_LINE = 1024 * 1024
_PRIVATE_FS_SUPPORTED = os.name == "posix"


class Unavailable(Exception):
    """A closed, non-sensitive failure used at the CLI boundary."""


class _MissingConfig(Exception):
    """The opt-in file or its private directory has not been created."""


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError
        result[key] = value
    return result


def _reject_constant(_value):
    raise ValueError


def _private_regular_file(path, *, limit):
    """Read a private regular file with no-follow and opened-identity checks."""
    path = Path(path)
    if (not _PRIVATE_FS_SUPPORTED or not hasattr(os, "O_DIRECTORY")
            or not hasattr(os, "O_NOFOLLOW")):
        raise Unavailable
    path = Path(os.path.abspath(path))
    home = path.parent.parent
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    directory_fd = -1
    try:
        directory_fd = os.open(path.anchor, directory_flags)
        current = Path(path.anchor)
        for part in path.parent.parts[1:]:
            try:
                next_fd = os.open(part, directory_flags, dir_fd=directory_fd)
            except FileNotFoundError:
                raise _MissingConfig from None
            opened_dir = os.fstat(next_fd)
            current = current / part
            if not stat.S_ISDIR(opened_dir.st_mode):
                os.close(next_fd)
                raise Unavailable
            if opened_dir.st_uid not in {0, os.getuid()}:
                os.close(next_fd)
                raise Unavailable
            if (stat.S_IMODE(opened_dir.st_mode) & 0o022
                    and not (opened_dir.st_uid == 0 and opened_dir.st_mode & stat.S_ISVTX)):
                os.close(next_fd)
                raise Unavailable
            if current == home and opened_dir.st_uid != os.getuid():
                os.close(next_fd)
                raise Unavailable
            if current.name == ".cairn" and (
                opened_dir.st_uid != os.getuid()
                or stat.S_IMODE(opened_dir.st_mode) & 0o077
            ):
                os.close(next_fd)
                raise Unavailable
            os.close(directory_fd)
            directory_fd = next_fd
        try:
            before = os.stat(path.name, dir_fd=directory_fd, follow_symlinks=False)
        except FileNotFoundError:
            raise _MissingConfig from None
        if not stat.S_ISREG(before.st_mode) or before.st_uid != os.getuid():
            raise Unavailable
        if stat.S_IMODE(before.st_mode) & 0o077:
            raise Unavailable
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd)
        try:
            opened = os.fstat(fd)
            if (not stat.S_ISREG(opened.st_mode) or opened.st_uid != os.getuid()
                    or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)
                    or stat.S_IMODE(opened.st_mode) & 0o077):
                raise Unavailable
            chunks = []
            size = 0
            while True:
                block = os.read(fd, min(65536, limit + 1 - size))
                if not block:
                    break
                size += len(block)
                if size > limit:
                    raise Unavailable
                chunks.append(block)
            after = os.fstat(fd)
            if (after.st_dev, after.st_ino) != (opened.st_dev, opened.st_ino):
                raise Unavailable
            return b"".join(chunks)
        finally:
            os.close(fd)
    except (_MissingConfig, Unavailable):
        raise
    except (OSError, ValueError, TypeError):
        raise Unavailable from None
    finally:
        if directory_fd >= 0:
            os.close(directory_fd)


def _safe_text(value, *, limit=4096):
    if not isinstance(value, str) or not value or len(value) > limit:
        raise ValueError
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError
    return value


def _safe_alias(value):
    value = _safe_text(value, limit=80)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value):
        raise ValueError
    return value


def _strip_remote(value):
    value = _safe_text(value, limit=2048)
    if "@" in value and ":" in value and "://" not in value:
        value = value.rsplit("@", 1)[1]
    parsed = urlsplit(value)
    if parsed.scheme:
        if not parsed.hostname:
            raise ValueError
        value = urlunsplit((parsed.scheme.lower(), parsed.hostname.lower() +
                            (f":{parsed.port}" if parsed.port else ""),
                            parsed.path.rstrip("/"), "", ""))
    elif "@" in value or "?" in value or "#" in value:
        raise ValueError
    if not value or any(ch in value for ch in "\r\n\x00"):
        raise ValueError
    return value


def _safe_config_path(value):
    value = _safe_text(value)
    candidate = Path(value)
    if not candidate.is_absolute() or any(part in {".", ".."} for part in candidate.parts):
        raise ValueError
    return str(candidate)


def validate_config_bytes(raw):
    """Validate only the closed local opt-in schema; never imply collection."""
    try:
        if not isinstance(raw, bytes) or len(raw) > MAX_CONFIG_BYTES:
            raise ValueError
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                           parse_constant=_reject_constant)
        required = {"version", "enabled", "sources", "projects"}
        if (not isinstance(value, dict) or not required <= set(value)
                or set(value) - required - {"requested_accounts"}):
            raise ValueError
        if type(value["version"]) is not int or value["version"] != CONFIG_VERSION:
            raise ValueError
        if type(value["enabled"]) is not bool:
            raise ValueError
        if not isinstance(value["sources"], list) or not isinstance(value["projects"], list):
            raise ValueError
        source_aliases, source_roots, project_aliases, project_paths = set(), set(), set(), set()
        sources = []
        for source in value["sources"]:
            if not isinstance(source, dict) or set(source) != {"alias", "tool", "root"}:
                raise ValueError
            alias, tool = _safe_alias(source["alias"]), source["tool"]
            root = _safe_config_path(source["root"])
            identity = (tool, root)
            if tool not in TOOLS or alias in source_aliases or identity in source_roots:
                raise ValueError
            source_aliases.add(alias)
            source_roots.add(identity)
            sources.append({"alias": alias, "tool": tool, "root": root})
        projects = []
        for project in value["projects"]:
            if not isinstance(project, dict) or set(project) != {"alias", "path", "remote"}:
                raise ValueError
            alias = _safe_alias(project["alias"])
            project_path = _safe_config_path(project["path"])
            if alias in project_aliases or project_path in project_paths:
                raise ValueError
            project_aliases.add(alias)
            project_paths.add(project_path)
            projects.append({"alias": alias, "path": project_path,
                             "remote": _strip_remote(project["remote"])})
        requested = value.get("requested_accounts", {})
        if not isinstance(requested, dict):
            raise ValueError
        if set(requested) - source_aliases:
            raise ValueError
        accounts = {}
        for alias, account in requested.items():
            accounts[_safe_alias(alias)] = _safe_text(account, limit=256)
        return {"version": CONFIG_VERSION, "enabled": value["enabled"],
                "sources": sources, "projects": projects,
                "requested_accounts": accounts}
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError,
            OverflowError, AttributeError):
        raise Unavailable from None


def load_config(config_path):
    """Read only ~/.cairn/meter.json after private ancestry checks."""
    path = Path(config_path).absolute()
    if not _PRIVATE_FS_SUPPORTED:
        if not path.exists() and not path.is_symlink():
            return None
        raise Unavailable
    try:
        raw = _private_regular_file(path, limit=MAX_CONFIG_BYTES)
    except _MissingConfig:
        return None
    except Unavailable:
        raise
    return validate_config_bytes(raw)


def _contained_file(root, relative):
    """Return bytes from one synthetic-approved-root relative file safely."""
    if not _PRIVATE_FS_SUPPORTED or not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise Unavailable
    parts = Path(relative).parts
    if any(part in {".", ".."} for part in parts):
        raise Unavailable
    base = Path(root).absolute()
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    directory_fd = -1
    try:
        directory_fd = os.open(base.anchor, flags)
        for part in base.parts[1:]:
            next_fd = os.open(part, flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd
        for part in parts[:-1]:
            next_fd = os.open(part, flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd
        leaf = parts[-1]
        before = os.stat(leaf, dir_fd=directory_fd, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):
            raise Unavailable
        fd = os.open(leaf, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd)
        try:
            opened = os.fstat(fd)
            if (not stat.S_ISREG(opened.st_mode)
                    or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)):
                raise Unavailable
            chunks, pending = [], b""
            while True:
                block = os.read(fd, 65536)
                if not block:
                    break
                chunks.append(block)
                pending += block
                while True:
                    index = pending.find(b"\n")
                    if index < 0:
                        if len(pending) > MAX_LINE:
                            raise Unavailable
                        break
                    line, pending = pending[:index + 1], pending[index + 1:]
                    if len(line) > MAX_LINE:
                        raise Unavailable
            after = os.fstat(fd)
            if (after.st_dev, after.st_ino) != (opened.st_dev, opened.st_ino):
                raise Unavailable
            data = b"".join(chunks)
            if pending:
                raise Unavailable
            return data
        finally:
            os.close(fd)
    except Unavailable:
        raise
    except (OSError, ValueError, TypeError):
        raise Unavailable from None
    finally:
        if directory_fd >= 0:
            os.close(directory_fd)


def _digest(*values):
    return hashlib.sha256(json.dumps(values, ensure_ascii=True).encode()).hexdigest()


def _text(value):
    if not isinstance(value, str) or not value or len(value) > 4096:
        raise ValueError
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError
    return value


def _counter(value):
    if type(value) is not int or not 0 <= value <= MAX_COUNTER:
        raise ValueError
    return value


def _timestamp(value):
    value = _text(value)
    if "T" not in value:
        raise ValueError
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError
    return parsed.isoformat()


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError
        result[key] = value
    return result


def _constant(_value):
    raise ValueError


def reconcile_checkpoints(checkpoints, *, baseline):
    """Calculate one counter's deltas after a separately established baseline.

    The caller must establish source identity, ordering, lineage and completeness;
    this arithmetic alone proves none of them. Unknown or invalid inputs cannot
    produce a partial total. This function does not read or persist any data.
    """
    if not isinstance(checkpoints, (list, tuple)) or not checkpoints:
        return None
    try:
        previous = _counter(baseline)
        deltas = []
        for checkpoint in checkpoints:
            current = _counter(checkpoint)
            if current < previous:
                return None
            deltas.append(current - previous)
            previous = current
    except ValueError:
        return None
    return {"deltas": deltas, "total": sum(deltas), "last_checkpoint": previous}


def classify_pytest_command(command):
    """Recognize a direct pytest invocation without retaining its arguments."""
    if not isinstance(command, list) or not command:
        return None
    try:
        for part in command:
            _text(part)
    except ValueError:
        return None
    if command[0] == "pytest":
        return "pytest"
    if (len(command) >= 3 and re.fullmatch(r"python(?:3(?:\.[0-9]+)?)?", command[0])
            and command[1:3] == ["-m", "pytest"]):
        return "pytest"
    return None


def union_test_intervals(intervals):
    """Sum execution and union wall time for independently identified repeats.

    Values are milliseconds. The caller must establish identity, completeness
    and classification; unknown inputs return no partial total.
    """
    if not isinstance(intervals, (list, tuple)) or not intervals:
        return None
    checked = []
    try:
        for interval in intervals:
            if not isinstance(interval, (list, tuple)) or len(interval) != 2:
                return None
            start, end = (_counter(value) for value in interval)
            if end < start:
                return None
            checked.append((start, end))
        total = _counter(sum(end - start for start, end in checked))
    except ValueError:
        return None
    checked.sort()
    start, end = checked[0]
    wall = 0
    for next_start, next_end in checked[1:]:
        if next_start > end:
            wall += end - start
            start, end = next_start, next_end
        else:
            end = max(end, next_end)
    wall += end - start
    return {"executions": len(checked), "execution_ms": total, "wall_wait_ms": wall}


def _codex_usage(data):  # vendor-ok: normalize the supported input protocol
    raw = {key: _counter(data[key]) for key in (
        "input_tokens", "cached_input_tokens", "output_tokens",
        "reasoning_output_tokens", "total_tokens",
    )}
    if (raw["cached_input_tokens"] > raw["input_tokens"]
            or raw["reasoning_output_tokens"] > raw["output_tokens"]
            or raw["total_tokens"] != raw["input_tokens"] + raw["output_tokens"]):
        raise ValueError
    # Absence is not a measured zero, even though the producer defaults it.
    write = data.get("cache_write_input_tokens")
    if write is not None and _counter(write) != 0:
        # Its inclusion in input is not established by the pinned type alone.
        raise ValueError
    return {
        "fresh_input": raw["input_tokens"] - raw["cached_input_tokens"],
        "cache_read": raw["cached_input_tokens"],
        "cache_write": None if write is None else 0,
        "output": raw["output_tokens"],
    }


def _claude_usage(data):  # vendor-ok: normalize the supported input protocol
    kinds = {out: _counter(data[key]) for out, key in (
        ("fresh_input", "input_tokens"), ("output", "output_tokens"),
        ("cache_write", "cache_creation_input_tokens"),
        ("cache_read", "cache_read_input_tokens"),
    )}
    if "cache_creation" in data:
        ttl = data["cache_creation"]
        if set(ttl) != {"ephemeral_5m_input_tokens", "ephemeral_1h_input_tokens"}:
            raise ValueError
        if sum(_counter(value) for value in ttl.values()) != kinds["cache_write"]:
            raise ValueError
    return kinds


def read_records(tool, lines):
    """Normalize a finite evidence batch, never infer a project or account.

    The supported direct response contract only is accepted. Legacy checkpoints
    are flagged, never added to response counts. Fork/child histories are
    deliberately not bound until lineage reconciliation is implemented.
    Requestless messages are not deduplicated by guessed session identity.
    Transcript content and live status payloads are not usage contracts here.
    """
    if tool not in TOOLS:
        raise ValueError("unsupported source")
    events, contexts, issues = {}, {}, set()
    timing_observations = []
    owner = None
    unsafe_owner = False

    def keep(key, event):
        if key in events and events[key] != event:
            events[key] = None
            issues.add("conflicting_usage")
        elif key not in events:
            events[key] = event

    for line in lines:
        try:
            if not isinstance(line, bytes) or len(line) > MAX_LINE or not line.endswith(b"\n"):
                raise ValueError
            record = json.loads(line.decode("utf-8"), object_pairs_hook=_object,
                                parse_constant=_constant)
            if not isinstance(record, dict):
                raise ValueError
            kind = record.get("type")
            if tool == "antigravity":  # vendor-ok: metadata-only unsupported adapter
                issues.add("unsupported_usage_contract")
                continue
            if tool == "claude":  # vendor-ok: producer assistant usage shape
                if kind != "assistant":
                    if kind not in {"user", "system", "progress", "file-history-snapshot"}:
                        issues.add("unsupported_record")
                    continue
                message = record["message"]
                request = _text(record["requestId"])
                key = _digest(tool, request, _text(message["id"]))
                keep(key, {"key": key, "timestamp": _timestamp(record["timestamp"]),
                           "kinds": _claude_usage(message["usage"]),  # vendor-ok: protocol extraction
                           "turn_key": None, "cwd_key": None,
                           "project": None, "account": None})
                issues.add("project_turn_binding_unproven")
                continue
            payload = record.get("payload")
            if kind == "session_meta":
                candidate = (_text(payload["id"]), _text(payload["session_id"]))
                if owner is None:
                    owner = candidate
                elif owner != candidate:
                    unsafe_owner = True
                if any(payload.get(field) is not None for field in (
                    "forked_from_id", "parent_thread_id", "history_base",
                    "forked_from_ordinal_exclusive", "subagent_history_start_ordinal",
                )):
                    unsafe_owner = True
            elif kind == "turn_context":
                turn = _text(payload["turn_id"])
                cwd = _text(payload["cwd"])
                if not cwd.startswith("/") or any(part in {".", ".."} for part in cwd.split("/")):
                    raise ValueError
                value = (_digest("cwd", cwd), owner)
                if turn in contexts and contexts[turn] != value:
                    contexts[turn] = None
                    issues.add("conflicting_turn_context")
                elif turn not in contexts:
                    contexts[turn] = value
            elif kind == "token_usage_record":
                thread, session, turn, root, response = (
                    _text(payload[field]) for field in (
                        "thread_id", "session_id", "turn_id", "root_turn_id", "response_id",
                    )
                )
                key = _digest(tool, session, response)
                keep(key, {"key": key, "timestamp": _timestamp(record["timestamp"]),
                           "kinds": _codex_usage(payload["usage"]),  # vendor-ok: protocol extraction
                           "turn_key": _digest(tool, thread, turn),
                           "cwd_key": None, "project": None, "account": None,
                           "_binding": (thread, session, turn, root)})
            elif kind == "event_msg" and payload.get("type") == "token_count":
                issues.add("legacy_checkpoint_unreconciled")
            elif kind == "event_msg" and payload.get("type") == "item_completed":
                item = payload["item"]
                if item.get("type") != "CommandExecution":
                    continue
                classification = classify_pytest_command(item.get("command"))
                if classification is None:
                    issues.add("test_command_classification_unknown")
                    continue
                start = _counter(payload["started_at_ms"])
                end = _counter(payload["completed_at_ms"])
                if end < start:
                    raise ValueError
                timing_observations.append({
                    "classification": classification,
                    "started_at_ms": start,
                    "completed_at_ms": end,
                })
            elif kind not in {"response_item", "event_msg", "compacted", "world_state"}:
                issues.add("unsupported_record")
        except (ValueError, TypeError, KeyError, AttributeError, UnicodeError,
                OverflowError, RecursionError):
            # Do not retain raw exception text, filenames, source bodies or IDs.
            issues.add("invalid_record")
            if tool == "codex":  # vendor-ok: malformed ownership cannot be trusted
                unsafe_owner = True

    normalized = []
    for event in events.values():
        if event is None:
            continue
        binding = event.pop("_binding", None)
        if binding is not None:
            thread, session, turn, root = binding
            context = contexts.get(turn)
            if (not unsafe_owner and owner == (thread, session) and context is not None
                    and context[1] == owner and root == turn):
                event["cwd_key"] = context[0]
            else:
                issues.add("source_turn_binding_unproven")
        normalized.append({"kinds": event["kinds"]})
    issues.add("project_remote_verification_pending")
    if not normalized:
        issues.add("no_supported_usage")
    return {"schema": READER_VERSION, "tool": tool,
            "events": normalized,
            "timing_observations": timing_observations, "timing_coverage": "unknown",
            "coverage": "unknown", "identity_coverage": "unknown",
            "ownership_coverage": "unknown", "issues": sorted(issues)}


def main():
    """C1 checkpoint CLI: config-only, never enumerates a private source."""
    parser = argparse.ArgumentParser(description="Cairn usage meter (foundation checkpoint)")
    parser.add_argument("--json", action="store_true", help="emit the status as JSON")
    args = parser.parse_args()
    try:
        config = load_config(Path.home() / ".cairn" / "meter.json")
    except Unavailable:
        status, code = "unavailable", 5
    else:
        if config is None or not config["enabled"]:
            status, code = "disabled", 0
        else:
            # Source discovery, project binding, accounting, and ledger handling
            # are intentionally outside this foundation checkpoint.
            status, code = "unavailable", 5
    result = {"schema": "cairn-meter-foundation/1", "collection": status,
              "usage": {tool: "unknown" for tool in TOOLS}}
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(f"meter: {status}; usage remains unknown for all supported tools")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
