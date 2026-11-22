#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Meter reader, ledger and explicit refresh/rebuild entry points.

Internal bounded readers accept only explicitly supplied paths and bytes, and
refresh tests use synthetic roots/files and a synthetic account home. The bare
CLI status remains config-only; explicit refresh/rebuild commands use fixed OS
consent and closed receipts. Normalized global coverage remains unknown.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import stat
import sys
import argparse
import uuid
import time
import secrets
from fractions import Fraction
from decimal import Decimal
try:
    import pwd
except ImportError:  # vendor-ok: there is no account database module on Windows
    pwd = None
from datetime import datetime, timezone, timedelta
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit, urlunsplit


READER_VERSION = "cairn-source-readers/6"
CODEX_CONTRACT = "49f0c6022596c361fe676a5c4738fb2be34e3a93"  # vendor-ok: pins reviewed input contract
MAX_COUNTER = 2**63 - 1
TOOLS = ("codex", "claude", "antigravity")  # vendor-ok: source adapters
CONFIG_VERSION = 1
MAX_CONFIG_BYTES = 256 * 1024
MAX_LINE = 8 * 1024 * 1024
MAX_BATCH_BYTES = 64 * 1024 * 1024
MAX_BATCH_LINES = 100_000
MAX_REREAD_BYTES = 512 * 1024 * 1024
MAX_REREAD_LINES = 1_000_000
MAX_NORMALIZED_EVENTS = 100_000


def _load_shared_pulse():
    """Load the shared pulse only from beside this resolved tool source."""
    path = Path(__file__).resolve().with_name("pulse.py")
    spec = importlib.util.spec_from_file_location("_cairn_shared_pulse", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("pulse-module-unavailable")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except (OSError, ImportError, ValueError, TypeError):
        raise RuntimeError("pulse-module-unavailable") from None
    return module


_PULSE = _load_shared_pulse()
LEDGER_SCHEMA = "cairn-meter-ledger/6"
_OLD_LEDGER_SCHEMAS = frozenset({"cairn-meter-ledger/3", "cairn-meter-ledger/4",
                                 "cairn-meter-ledger/5"})
RATIO_VERSION = "cairn-api-token-index/2026-11-22"
_RATIO_INDEX = {
    "version": RATIO_VERSION,
    "profile": "Hypothetical first-party Standard/global API text-token reference profile; excludes tools, taxes, discounts, and subscriptions.",
    "reference_model": "claude-haiku-4-5-20251001",
    "reference_kind": "fresh_input",
    "reference_rate": "1",
    "currency": "USD",
    "denominator_tokens": 1_000_000,
    "as_of": "2026-11-22",
    "sources": [
        "https://platform.claude.com/docs/en/about-claude/pricing",
        "https://developers.openai.com/api/docs/pricing",
        "https://aistudio.google.com/docs/pricing",
    ],
    "models": {
        "claude-haiku-4-5-20251001": {
            "fresh_input": [1, 1], "cache_read": [1, 10], "output": [5, 1],
            "cache_write_5m": [5, 4], "cache_write_1h": [2, 1],
        },
        "claude-sonnet-4-6": {
            "fresh_input": [3, 1], "cache_read": [3, 10], "output": [15, 1],
            "cache_write_5m": [15, 4], "cache_write_1h": [6, 1],
        },
        "claude-opus-5-5": {
            "fresh_input": [4, 1], "cache_read": [1, 5], "output": [20, 1],
            "cache_write_5m": [5, 1], "cache_write_1h": [8, 1],
        },
        "gpt-5.3-codex": {
            "fresh_input": [7, 4], "cache_read": [7, 40], "output": [14, 1],
            "cache_write_5m": None, "cache_write_1h": None,
        },
        "claude-fable-5-2": {
            "fresh_input": [8, 1], "cache_read": [1, 5], "output": [40, 1],
            "cache_write_5m": [10, 1], "cache_write_1h": [16, 1],
        },
        "claude-sonnet-5-5": {
            "fresh_input": [2, 1], "cache_read": [1, 10], "output": [10, 1],
            "cache_write_5m": [5, 2], "cache_write_1h": [4, 1],
        },
        "claude-haiku-5-5": {
            "fresh_input": [1, 10], "cache_read": [1, 100], "output": [1, 2],
            "cache_write_5m": [1, 8], "cache_write_1h": [1, 5],
            "long_prompt": {
                "over_tokens": 100_000,
                "fresh_input": [1, 2], "cache_read": [1, 20], "output": [5, 2],
                "cache_write_5m": [5, 8], "cache_write_1h": [1, 1],
            },
        },
        "gpt-6.2-sol": {
            "fresh_input": [2, 1], "cache_read": [1, 10], "output": [10, 1],
            "cache_write_5m": None, "cache_write_1h": None,
            "long_prompt": {
                "over_tokens": 272_000,
                "fresh_input": [4, 1], "cache_read": [1, 5], "output": [15, 1],
                "cache_write_5m": None, "cache_write_1h": None,
            },
        },
        "gpt-6.1-sol": {
            "fresh_input": [2, 1], "cache_read": [1, 10], "output": [10, 1],
            "cache_write_5m": None, "cache_write_1h": None,
            "long_prompt": {
                "over_tokens": 272_000,
                "fresh_input": [4, 1], "cache_read": [1, 5], "output": [15, 1],
                "cache_write_5m": None, "cache_write_1h": None,
            },
        },
        "gpt-6-sol": {
            "fresh_input": [2, 1], "cache_read": [1, 5], "output": [10, 1],
            "cache_write_5m": None, "cache_write_1h": None,
            "long_prompt": {
                "over_tokens": 272_000,
                "fresh_input": [4, 1], "cache_read": [2, 5], "output": [15, 1],
                "cache_write_5m": None, "cache_write_1h": None,
            },
        },
        "gpt-6.1-terra": {
            "fresh_input": [1, 1], "cache_read": [1, 20], "output": [5, 1],
            "cache_write_5m": None, "cache_write_1h": None,
            "long_prompt": {
                "over_tokens": 272_000,
                "fresh_input": [2, 1], "cache_read": [1, 10], "output": [15, 2],
                "cache_write_5m": None, "cache_write_1h": None,
            },
        },
        "gpt-6-luna": {
            "fresh_input": [1, 10], "cache_read": [1, 100], "output": [1, 2],
            "cache_write_5m": None, "cache_write_1h": None,
            "long_prompt": {
                "over_tokens": 272_000,
                "fresh_input": [1, 5], "cache_read": [1, 50], "output": [3, 4],
                "cache_write_5m": None, "cache_write_1h": None,
            },
        },
        "gemini-4-argon": {
            "fresh_input": [4, 1], "cache_read": [1, 5], "output": [20, 1],
            "cache_write_5m": None, "cache_write_1h": None,
        },
        "gemini-4-neon": {
            "fresh_input": [3, 1], "cache_read": [3, 20], "output": [15, 1],
            "cache_write_5m": None, "cache_write_1h": None,
        },
        "gemini-4-hydrogen": {
            "fresh_input": [3, 2], "cache_read": [3, 40], "output": [15, 2],
            "cache_write_5m": None, "cache_write_1h": None,
        },
    },
}
MAX_SOURCE_ROOT_DEPTH = 32
MAX_REFRESH_ENTRIES = 100_000
MAX_SOURCE_FILES = 10_000
# The antigravity attribution search (plan 2026-11-22-antigravity-reader, rule 5).
# Starting values, not measured: per conversation, then per refresh. A conversation
# over a cap is left unattributed, never guessed; one the refresh cannot pay for waits.
MAX_ATTRIBUTION_BYTES = 16 * 1024 * 1024
MAX_ATTRIBUTION_ENTRIES = 5_000
MAX_ATTRIBUTION_DEPTH = 8
MAX_ATTRIBUTION_RUN_BYTES = 256 * 1024 * 1024
MAX_ATTRIBUTION_RUN_ENTRIES = 50_000
MAX_ANTIGRAVITY_CONVERSATIONS = 2_000
# C7, synthetic-only on macOS from clean source commit 835dc50c, Python 3.13.13:
# The 16 x 64 MiB workload took a median 8.98 s (114.01 MiB/s). Rereading a
# 400 MiB structured log took 7.61 s with peak RSS 406 MiB. The 1 GiB cap meets
# the 512 MiB floor; peak RSS is below the 2 GiB threshold.
MAX_RUN_READ_BYTES = 1024 * 1024 * 1024
MAX_RUN_EVENTS = 200_000
FOLD_AFTER_DAYS = 14
RETAINED_EVENT_TARGET = 50_000
FOLD_FORCE_EVENTS = 80_000
MAX_RETAINED_EVENTS = 100_000
MAX_RETAINED_WAITS = 100_000
MAX_WAIT_OCCURRENCES = 100_000
MAX_WAIT_EXPORT_WORK = 100_000
MAX_CLAIM_BYTES = 8 * 1024 * 1024
MAX_CLAIM_LINE = 64 * 1024
MAX_LEDGER_BYTES = 64 * 1024 * 1024
MAX_AGENT_SUMMARIES = 1_000
MAX_AGENT_TRANSCRIPTS = 100_000
# The three counts a finished sub-agent's summary record holds (Detail D0, P1).
_SUMMARY_FIELDS = frozenset({"totalTokens", "toolUses", "durationMs"})
# The frame the tool writes around a run's id inside its summary (Detail D0, P4).
_SUMMARY_FRAME = re.compile(r"<task-id>([A-Za-z0-9]{8,64})</task-id>")
LEDGER_NAME = "ledger.json"
LEDGER_LOCK_NAME = "ledger.lock"


class Unavailable(Exception):
    """A closed, non-sensitive failure used at the CLI boundary."""

    def __init__(self, reason="unavailable"):
        self.reason = reason if re.fullmatch(r"[a-z][a-z0-9_]*", reason or "") else "unavailable"
        super().__init__(self.reason)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError
        result[key] = value
    return result


def _reject_constant(_value):
    raise ValueError


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
    if "://" not in value and ":" in value and "/" not in value.split(":", 1)[0]:
        # SSH form `[user@]host:path`: keep `host:path`. urlsplit would read
        # `host` as a URL scheme, so this form is normalized here instead,
        # and the normalized form normalizes to itself.
        host, _sep, path = value.partition(":")
        host = host.rsplit("@", 1)[-1]
        if not host or not path or any(ch in host for ch in "?#[]@"):
            raise ValueError
        value = f"{host.lower()}:{path.rstrip('/')}"
        if any(ch in value for ch in "\r\n\x00"):
            raise ValueError
        return value
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


_O_BINARY = getattr(os, "O_BINARY", 0)
_O_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
# Windows reparse tags that redirect a folder or file: a symbolic link, a mount point.
_REPARSE_REDIRECTS = frozenset({0xA000000C, 0xA0000003})
_REPARSE_ATTRIBUTE = 0x400
LOCK_TAKEOVER_SECONDS = 900


def _fixed_user_home():
    """The account's home: the account database on Mac and Linux, Python's own home on Windows."""
    try:
        if pwd is not None:
            uid = os.getuid()
            if uid != os.geteuid():
                raise Unavailable
            home = Path(pwd.getpwuid(uid).pw_dir)
        else:
            home = Path.home()
        if not home.is_absolute() or any(part in {".", ".."} for part in home.parts):
            raise Unavailable
        return home
    except Unavailable:
        raise
    except (OSError, KeyError, TypeError, ValueError, AttributeError, RuntimeError):
        raise Unavailable from None


def _is_link(info):
    """True for a link or, on Windows, an entry the system redirects (link or mount point)."""
    if stat.S_ISLNK(info.st_mode):
        return True
    attributes = getattr(info, "st_file_attributes", 0)
    return bool(attributes & _REPARSE_ATTRIBUTE
                and getattr(info, "st_reparse_tag", 0) in _REPARSE_REDIRECTS)


def _read_limited(path, limit, reason="unavailable", *, nofollow=False):
    """Read at most `limit` bytes from one open; a longer file is refused."""
    try:
        fd = os.open(path, os.O_RDONLY | _O_BINARY | (_O_NOFOLLOW if nofollow else 0))
        try:
            chunks, total = [], 0
            while True:
                block = os.read(fd, min(64 * 1024, limit + 1 - total))
                if not block:
                    break
                total += len(block)
                if total > limit:
                    raise Unavailable(reason)
                chunks.append(block)
        finally:
            os.close(fd)
        return b"".join(chunks)
    except Unavailable:
        raise
    except (OSError, ValueError):
        raise Unavailable(reason) from None


def load_config(config_path):
    """Read only ~/.cairn/meter.json; a missing file is None, anything else must validate."""
    path = Path(config_path)
    try:
        if not path.exists() and not path.is_symlink():
            return None
        if not path.is_file():
            raise Unavailable
    except OSError:
        raise Unavailable from None
    return validate_config_bytes(_read_limited(path, MAX_CONFIG_BYTES))


def _enumerate_jsonl(root):
    """Walk one configured root: regular `.jsonl` files, skipping links and redirected folders."""
    files, entries = [], 0
    stack = [(str(root), "", 0)]
    try:
        while stack:
            directory, prefix, depth = stack.pop()
            with os.scandir(directory) as scan:
                for entry in scan:
                    entries += 1
                    if entries > MAX_REFRESH_ENTRIES:
                        raise Unavailable("source_budget_exceeded")
                    name = entry.name
                    relative = f"{prefix}/{name}" if prefix else name
                    info = entry.stat(follow_symlinks=False)
                    if _is_link(info):
                        continue
                    if stat.S_ISDIR(info.st_mode):
                        if depth >= MAX_SOURCE_ROOT_DEPTH:
                            raise Unavailable("source_budget_exceeded")
                        stack.append((entry.path, relative, depth + 1))
                    elif stat.S_ISREG(info.st_mode) and name.endswith(".jsonl"):
                        info = os.lstat(entry.path)       # a directory entry has no file id on Windows
                        files.append((relative, {
                            "dev": info.st_dev, "ino": info.st_ino,
                            "size": info.st_size, "mtime_ns": info.st_mtime_ns,
                            "ctime_ns": info.st_ctime_ns,
                        }))
                        if len(files) > MAX_SOURCE_FILES:
                            raise Unavailable("source_budget_exceeded")
    except Unavailable:
        raise
    except (OSError, ValueError, TypeError):
        raise Unavailable from None
    files.sort(key=lambda item: item[0])
    return files, entries


def _enumerate_antigravity(root):  # vendor-ok: walk the one folder shape the tool writes
    """List one antigravity root's logs by fixed names: `brain/<uuid>/.system_generated/logs/*.jsonl`.

    Every path is built from those fixed names and listed entries, never from
    record text; links are skipped at every level and a linked root is refused.
    Returns `(files, entries, waiting)`: the files as `_enumerate_jsonl` lists
    them, the entries listed, and whether a cap or an error inside one
    conversation left something for the next refresh. A missing `brain/` or
    `logs/` gives no files. Only a missing or linked root raises Unavailable.
    """
    try:
        info = os.lstat(root)
    except (OSError, ValueError, TypeError):
        raise Unavailable from None
    if _is_link(info) or not stat.S_ISDIR(info.st_mode):
        raise Unavailable
    files, entries, waiting = [], 0, False
    brain = os.path.join(root, "brain")
    try:
        info = os.lstat(brain)
    except FileNotFoundError:
        return files, entries, False
    except (OSError, ValueError):
        return files, entries, True
    if _is_link(info) or not stat.S_ISDIR(info.st_mode):
        return files, entries, False
    conversations = []
    try:
        with os.scandir(brain) as scan:
            for entry in scan:
                entries += 1
                if entries > MAX_ATTRIBUTION_RUN_ENTRIES:
                    return files, entries, True
                try:
                    name = _codex_uuid(entry.name)
                except ValueError:
                    continue                  # not a conversation folder
                try:
                    info = entry.stat(follow_symlinks=False)
                except OSError:
                    waiting = True
                    continue
                if not _is_link(info) and stat.S_ISDIR(info.st_mode):
                    conversations.append(name)
    except (OSError, ValueError):
        return files, entries, True
    conversations.sort()
    if len(conversations) > MAX_ANTIGRAVITY_CONVERSATIONS:
        del conversations[MAX_ANTIGRAVITY_CONVERSATIONS:]
        waiting = True
    for conversation in conversations:
        system = os.path.join(brain, conversation, ".system_generated")
        logs = os.path.join(system, "logs")
        found = []
        try:
            if any(_is_link(info) or not stat.S_ISDIR(info.st_mode)
                   for info in (os.lstat(system), os.lstat(logs))):
                continue
            with os.scandir(logs) as scan:
                for entry in scan:
                    entries += 1
                    if entries > MAX_ATTRIBUTION_RUN_ENTRIES:
                        found = None          # this conversation, and the rest, wait
                        break
                    info = entry.stat(follow_symlinks=False)
                    if (_is_link(info) or not stat.S_ISREG(info.st_mode)
                            or not entry.name.endswith(".jsonl")):
                        continue
                    info = os.lstat(entry.path)   # a directory entry has no file id on Windows
                    found.append((f"brain/{conversation}/.system_generated/logs/{entry.name}", {
                        "dev": info.st_dev, "ino": info.st_ino,
                        "size": info.st_size, "mtime_ns": info.st_mtime_ns,
                        "ctime_ns": info.st_ctime_ns,
                    }))
        except FileNotFoundError:
            continue                          # no logs folder: nothing to read here
        except (OSError, ValueError):
            waiting = True                    # this conversation waits for the next refresh
            continue
        if found is None:
            waiting = True
            break
        files.extend(found)
    files.sort(key=lambda item: item[0])
    return files, entries, waiting


_ATTRIBUTION_SUFFIXES = (".txt", ".md", ".json", ".jsonl", ".log")
_NAME_ALNUM = frozenset(b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
_NAME_BEFORE_BLOCKED = _NAME_ALNUM | frozenset(b"._-~%/")
_NAME_AFTER_BLOCKED = _NAME_ALNUM | frozenset(b"_-")


def _attribution_spellings(path):
    """The byte spellings of a project path that a saved file may hold."""
    spellings = [path.encode("utf-8", "surrogatepass")]
    if os.name == "nt":                       # JSON text doubles each backslash
        doubled = path.replace("\\", "\\\\").encode("utf-8", "surrogatepass")
        if doubled != spellings[0]:
            spellings.append(doubled)
    return spellings


def _names_project(window, spelling, at_start, at_end):
    """Whether `spelling` occurs in `window` as a whole name (plan rule 5).

    The byte before is not a letter, digit, `.`, `_`, `-`, `~`, `%` or `/`, but
    the `/` of a literal `file://` is allowed. The byte after is not a letter,
    digit, `_`, `-` or a byte of 0x80 or above; a `.` after counts as an end
    when the byte after it is not a letter, digit, `_` or `-`. A match is judged
    only when the 7 bytes before it and the 2 after it are in the window, or the
    window starts or ends the file; the overlap between windows makes that so.
    """
    size, length = len(spelling), len(window)
    position = window.find(spelling)
    while position >= 0:
        end = position + size
        if (position >= 7 or at_start) and (end + 2 <= length or at_end):
            before = window[position - 1] if position > 0 else None
            after = window[end] if end < length else None
            before_ok = (before is None or before not in _NAME_BEFORE_BLOCKED
                         or (before == 0x2F and position >= 7
                             and window[position - 7:position] == b"file://"))
            if after is None:
                after_ok = True
            elif after >= 0x80 or after in _NAME_AFTER_BLOCKED:
                after_ok = False
            elif after == 0x2E:
                following = window[end + 1] if end + 1 < length else None
                after_ok = following is None or following not in _NAME_AFTER_BLOCKED
            else:
                after_ok = True
            if before_ok and after_ok:
                return True
        position = window.find(spelling, position + 1)
    return False


def _search_attribution_file(path, identity, allowance, names, overlap):
    """Search one file's text for project names, reading at most `allowance` bytes.

    Returns (aliases named, bytes read, complete). The file must open without
    following a link and be the file the walk saw (same device and inode); a file
    larger than the allowance is not opened for reading. Never raises on a read.
    """
    named, used = set(), 0
    try:
        fd = os.open(path, os.O_RDONLY | _O_BINARY | _O_NOFOLLOW)
    except (OSError, ValueError):
        return named, used, False
    try:
        opened = os.fstat(fd)
        if (not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino) != identity
                or opened.st_size > allowance):
            return named, used, False
        size, window, base = opened.st_size, b"", 0
        while used < size:
            block = os.read(fd, min(64 * 1024, size - used))
            if not block:
                break                         # the file shrank since it was opened
            used += len(block)
            window += block
            for alias, spellings in names.items():
                if alias not in named and any(
                        _names_project(window, spelling, base == 0, used >= size)
                        for spelling in spellings):
                    named.add(alias)
            keep = min(len(window), overlap)
            base += len(window) - keep
            window = window[len(window) - keep:]
        return named, used, True
    except (OSError, ValueError):
        return named, used, False
    finally:
        os.close(fd)


def _conversation_project(source_root, conversation, projects):  # vendor-ok: the saved files of one conversation
    """Which one listed project do a conversation's saved files name? (plan rule 5)

    Searches the regular files under `brain/<conversation>/` (links skipped, at most
    MAX_ATTRIBUTION_DEPTH levels down, MAX_ATTRIBUTION_ENTRIES entries and
    MAX_ATTRIBUTION_BYTES bytes) for each listed project's path text. Returns
    `(alias, None, bytes read, entries)` for exactly one project named, else
    `(None, reason, bytes read, entries)` with the reason `antigravity_projects_ambiguous`
    (two or more named, found first), `antigravity_search_incomplete` (a cap, an
    unreadable file or folder) or `antigravity_project_not_named`. Only which
    projects matched leaves the search.
    """
    names = {project["alias"]: _attribution_spellings(project["path"])
             for project in projects}
    if not names:
        return None, "antigravity_project_not_named", 0, 0
    overlap = max(len(spelling) for spellings in names.values()
                  for spelling in spellings) + 8
    named, incomplete, capped = set(), False, False
    used = entries = 0
    stack = [(os.path.join(source_root, "brain", conversation), 0)]
    while stack and len(named) < 2 and not capped:
        directory, depth = stack.pop()
        listing = []
        try:
            with os.scandir(directory) as scan:
                for entry in scan:
                    entries += 1
                    if entries > MAX_ATTRIBUTION_ENTRIES:
                        capped = True
                        break
                    info = entry.stat(follow_symlinks=False)
                    if not _is_link(info):
                        listing.append((entry.name, entry.path, info))
        except (OSError, ValueError):
            incomplete = True
        if capped:
            incomplete = True
            break
        folders = []
        for name, path, info in sorted(listing, key=lambda item: item[0]):
            if stat.S_ISDIR(info.st_mode):
                if depth >= MAX_ATTRIBUTION_DEPTH:
                    incomplete = True
                else:
                    folders.append((path, depth + 1))
            elif stat.S_ISREG(info.st_mode) and name.endswith(_ATTRIBUTION_SUFFIXES):
                try:
                    walked = os.lstat(path)
                except (OSError, ValueError):
                    incomplete = True
                    continue
                hit, read, complete = _search_attribution_file(
                    path, (walked.st_dev, walked.st_ino),
                    MAX_ATTRIBUTION_BYTES - used, names, overlap)
                used += read
                named |= hit
                incomplete = incomplete or not complete
                if len(named) >= 2:
                    break
        stack.extend(reversed(folders))
    if len(named) >= 2:
        return None, "antigravity_projects_ambiguous", used, entries
    if incomplete:
        return None, "antigravity_search_incomplete", used, entries
    if not named:
        return None, "antigravity_project_not_named", used, entries
    return next(iter(named)), None, used, entries


def _capture_project_claims(project):
    """Read the project's work claims (`dev/intents.jsonl`), never through a link."""
    dev = Path(project["path"]) / "dev"
    target = dev / "intents.jsonl"
    try:
        for item in (dev, target):
            try:
                info = os.lstat(item)
            except FileNotFoundError:
                return [], "attribution_unavailable"
            if _is_link(info):
                return [], "attribution_unavailable"
        if not stat.S_ISREG(info.st_mode):
            return [], "attribution_unavailable"
        raw = _read_limited(target, MAX_CLAIM_BYTES, "source_budget_exceeded", nofollow=True)
        lines = raw.splitlines(keepends=True)
        if any(len(line) > MAX_CLAIM_LINE for line in lines):
            raise Unavailable("source_budget_exceeded")
        claims = _claim_snapshot(project["alias"], lines)
        return claims, "capture_gap" if not claims else "captured"
    except Unavailable:
        raise
    except (OSError, KeyError, TypeError, ValueError):
        raise Unavailable("source_read_unavailable") from None


def _capture_all_claims(config):
    """The project remotes come from the consent file; the claims from each project."""
    claims, status, remotes = [], set(), []
    for project in sorted(config["projects"], key=lambda item: item["alias"]):
        remotes.append({"alias": project["alias"], "remote": project["remote"]})
        project_claims, claim_status = _capture_project_claims(project)
        claims.extend(project_claims)
        status.add(claim_status)
    if not status:
        status.add("attribution_unavailable")
    return claims, remotes, status


def _write_beside_and_rename(directory, name, data, reason, prefix):
    """Write `data` to a new file in `directory`, then rename it over `name`.

    The file is readable by the user alone where the system has file modes. A
    failure leaves the old file and no temporary file, and gives only `reason`.
    """
    directory = Path(directory)
    temporary = directory / (prefix + secrets.token_hex(16) + ".tmp")
    fd = -1
    renamed = False
    try:
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | _O_BINARY, 0o600)
        offset = 0
        while offset < len(data):
            written = os.write(fd, data[offset:offset + 64 * 1024])
            if written <= 0:
                raise OSError
            offset += written
        os.fsync(fd)
        os.close(fd)
        fd = -1
        os.replace(temporary, directory / name)
        renamed = True
    except (OSError, ValueError, TypeError):
        raise Unavailable(reason) from None
    finally:
        if fd >= 0:
            try:
                os.close(fd)
            except OSError:
                pass
        if not renamed:
            try:
                os.unlink(temporary)
            except OSError:
                pass


def _meter_area(home):
    """`~/.cairn/meter`, made if it is missing."""
    area = Path(home) / ".cairn" / "meter"
    try:
        os.makedirs(area, mode=0o700, exist_ok=True)
        if not area.is_dir():
            raise Unavailable("ledger_unavailable")
    except OSError:
        raise Unavailable("ledger_unavailable") from None
    return area


def _take_lock(area):
    """A plain lock file holding this run's token; a dead run's lock is taken over after 15 minutes."""
    path = Path(area) / LEDGER_LOCK_NAME
    token = secrets.token_hex(16).encode("ascii")

    def make():
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | _O_BINARY, 0o600)
        try:
            if os.write(fd, token) != len(token):
                raise OSError
        except OSError:
            os.close(fd)
            fd = -1
            os.unlink(path)               # no empty lock is left behind
            raise
        finally:
            if fd >= 0:
                os.close(fd)

    try:
        try:
            make()
            return token
        except FileExistsError:
            pass
        info = os.lstat(path)
        if time.time() - info.st_mtime < LOCK_TAKEOVER_SECONDS:
            raise Unavailable("ledger_busy")
        first = _read_limited(path, 256, "ledger_busy")
        if _read_limited(path, 256, "ledger_busy") != first:
            raise Unavailable("ledger_busy")
        os.unlink(path)
        try:
            make()
        except FileExistsError:
            raise Unavailable("ledger_busy") from None
        return token
    except Unavailable:
        raise
    except OSError:
        raise Unavailable("ledger_unavailable") from None


def _release_lock(area, token):
    """Remove the lock only if this run made it and it still holds this run's token."""
    path = Path(area) / LEDGER_LOCK_NAME
    try:
        if _read_limited(path, 256) == token:
            os.unlink(path)
    except (OSError, Unavailable):
        pass


def _atomic_replace_ledger(area, candidate):
    data = (json.dumps(candidate, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")
    if len(data) > MAX_LEDGER_BYTES:
        raise Unavailable("source_budget_exceeded")
    if _load_ledger(data) != candidate:
        raise Unavailable("ledger_invalid")
    _write_beside_and_rename(area, LEDGER_NAME, data, "ledger_write_failed", ".ledger-")
    return "written"


def _write_summary(project, ledger, config):
    """Write one project's summary into its existing `dev/measurement`, never through a link."""
    candidate_remote = {item["alias"]: item["remote"]
                        for item in ledger["project_remotes"]}.get(project["alias"])
    if candidate_remote is None:
        raise Unavailable("project_remote_unavailable")
    if candidate_remote != project["remote"]:
        raise Unavailable("project_remote_mismatch")
    payload = _project_export_bytes(ledger, config, project["alias"])
    dev = Path(project["path"]) / "dev"
    measurement = dev / "measurement"
    for folder in (dev, measurement):
        try:
            info = os.lstat(folder)
        except OSError:
            raise Unavailable("project_export_unavailable") from None
        if _is_link(info) or not stat.S_ISDIR(info.st_mode):
            raise Unavailable("project_export_unavailable")
    try:
        for entry in os.listdir(measurement):
            if entry.startswith(".meter-") and entry.endswith(".tmp"):
                try:
                    os.unlink(measurement / entry)
                except OSError:
                    pass
    except OSError:
        raise Unavailable("project_export_unavailable") from None
    _write_beside_and_rename(measurement, "meter.json", payload,
                             "project_export_unavailable", ".meter-")
    return "written"


class _LineCutter:
    """Cut byte blocks into complete lines; no line or pending tail passes MAX_LINE."""

    def __init__(self):
        self.pending = b""

    def feed(self, block):
        """Return the complete lines in `block` and a refusal reason or None."""
        data = self.pending + block
        lines, start, reason = [], 0, None
        while True:
            index = data.find(b"\n", start)
            if index < 0:
                break
            if index + 1 - start > MAX_LINE:
                reason = "source_budget_exceeded"
                break
            lines.append(data[start:index + 1])
            start = index + 1
        self.pending = data[start:]
        if reason is None and len(self.pending) > MAX_LINE:
            reason = "source_budget_exceeded"
        return lines, reason


def _resume_window_verdict(window, offset, digest):
    """Check the bytes before a saved offset: None when they match, else the reason.

    `window` is the (at most MAX_LINE + 1) bytes that end at `offset`. It must
    end in a newline, and the line it ends must hash to `digest`.
    """
    if offset == 0:
        return None
    if not window.endswith(b"\n"):
        return "not_line_boundary"
    earlier = window.rfind(b"\n", 0, len(window) - 1)
    if earlier >= 0:
        line = window[earlier + 1:]
    elif offset > len(window):
        return "digest_mismatch"
    else:
        line = window
    if hashlib.sha256(line).hexdigest() != digest:
        return "digest_mismatch"
    return None


class _ApprovedLineStream:
    """Single-file bounded reader; `terminal_reason` is final after exhaustion.

    With the defaults the stream reads a whole file and ends at once on a torn
    tail. `piece=True` reads at most the size seen at open, stops at `budget`
    bytes or `max_lines` lines on a whole line (`limit_stop`), and ignores a torn
    tail. `tail=True` (with `piece`) yields no line: it finds the last complete
    line (`tail_offset`, `tail_digest`) reading back from the size at open.
    `resume` (a dict of dev, ino, offset and digest, with `piece`) first checks
    the file and the line before `offset`, then reads on from `offset`; a failed
    check ends the stream with `resume_failure` set and no line. With `reread`
    too every line is yielded from byte 0 and the check is made on
    the way through: `checkpoint_line` is the number of lines through `offset`.
    """

    def __init__(self, root, relative, budget, *, piece=False, max_lines=None,
                 tail=False, resume=None, reread=False):
        self.root = root
        self.relative = relative
        self.budget = budget
        self.piece = piece
        self.max_lines = max_lines
        self.tail = tail
        self.resume = resume
        self.reread = reread
        self.resume_failure = None
        self.checkpoint_line = None
        self.terminal_reason = "source_read_unavailable"
        self._started = False
        self.bytes_read = 0
        self.complete_lines = 0
        self.end_offset = 0
        self.limit_stop = False
        self.tail_offset = None
        self.tail_digest = None
        self.open_identity = None

    def _request_error(self):
        """Return the refusal reason for an out-of-range request, else None."""
        if type(self.piece) is not bool or type(self.tail) is not bool:
            return "source_read_unavailable"
        if type(self.budget) is not int or self.budget < 0:
            return "source_budget_exceeded"
        if not self.piece:
            if (self.tail or self.max_lines is not None or self.resume is not None
                    or self.reread):
                return "source_read_unavailable"
            return "source_budget_exceeded" if self.budget > MAX_BATCH_BYTES else None
        if self.tail and self.budget > 2 * MAX_LINE + 2:
            return "source_budget_exceeded"
        if self.budget > MAX_REREAD_BYTES:
            return "source_budget_exceeded"
        if self.max_lines is not None and (
                type(self.max_lines) is not int
                or not 0 < self.max_lines <= MAX_REREAD_LINES):
            return "source_budget_exceeded"
        if type(self.reread) is not bool or (self.reread and self.resume is None):
            return "source_read_unavailable"
        if self.resume is not None:
            resume = self.resume
            if (self.tail or not isinstance(resume, dict)
                    or set(resume) != {"dev", "ino", "offset", "digest"}
                    or any(type(resume[name]) is not int or resume[name] < 0
                           for name in ("dev", "ino", "offset"))
                    or (resume["digest"] is None) != (resume["offset"] == 0)
                    or (resume["digest"] is not None and (
                        not isinstance(resume["digest"], str)
                        or not re.fullmatch(r"[0-9a-f]{64}", resume["digest"])))):
                return "source_read_unavailable"
        return None

    def _scan_tail(self, file_fd, size):
        """Read back from `size` to the last newline and hash the line ending there.

        Returns (offset after that newline, SHA-256 of the line, refusal reason).
        No newline gives offset 0 and no digest. A torn tail or a line over
        MAX_LINE is refused, and so is a read that would pass the budget.
        """
        total = 0
        position = size
        scanned = 0
        newline = -1
        block = b""
        base = size
        while position > 0 and scanned < MAX_LINE + 1:
            want = min(64 * 1024, position, MAX_LINE + 1 - scanned)
            position -= want
            os.lseek(file_fd, position, os.SEEK_SET)
            block = os.read(file_fd, want)
            if len(block) != want:
                raise OSError("short read")
            total += want
            scanned += want
            found = block.rfind(b"\n")
            if found >= 0:
                newline = position + found
                base = position
                block = block[:found + 1]
                break
        self.bytes_read = total
        if newline < 0:
            if scanned > MAX_LINE:
                return None, None, "source_budget_exceeded"
            return 0, None, None
        line = block
        while True:
            earlier = line.rfind(b"\n", 0, len(line) - 1)
            if earlier >= 0:
                line = line[earlier + 1:]
                break
            if base == 0:
                break
            want = min(64 * 1024, base, MAX_LINE + 1 - len(line))
            if want <= 0:
                return None, None, "source_budget_exceeded"
            base -= want
            os.lseek(file_fd, base, os.SEEK_SET)
            more = os.read(file_fd, want)
            if len(more) != want:
                raise OSError("short read")
            total += want
            self.bytes_read = total
            if total > self.budget:
                return None, None, "source_budget_exceeded"
            earlier = more.rfind(b"\n")
            if earlier >= 0:
                line = more[earlier + 1:] + line
                break
            line = more + line
        if len(line) > MAX_LINE:
            return None, None, "source_budget_exceeded"
        return newline + 1, hashlib.sha256(line).hexdigest(), None

    def __iter__(self):
        if self._started:
            self.terminal_reason = "source_read_unavailable"
            return
        self._started = True
        file_fd = -1
        reason = "source_read_unavailable"
        try:
            request_error = self._request_error()
            if request_error is None and (
                    not isinstance(self.relative, str) or not self.relative
                    or Path(self.relative).is_absolute()
                    or any(part in {".", ".."} for part in Path(self.relative).parts)):
                request_error = "source_budget_exceeded"
            if request_error is not None:
                reason = request_error
                return
            full = os.path.join(self.root, *Path(self.relative).parts)
            file_fd = os.open(full, os.O_RDONLY | _O_BINARY | _O_NOFOLLOW)
            opened = os.fstat(file_fd)
            if not stat.S_ISREG(opened.st_mode):
                return
            # The identity is read by name, as the folder walk reads it: on Windows a
            # handle and a name can report different change times for one file.
            named = os.lstat(full)
            self.open_identity = {
                "dev": named.st_dev, "ino": named.st_ino,
                "size": opened.st_size, "mtime_ns": named.st_mtime_ns,
                "ctime_ns": named.st_ctime_ns,
            }
            cutter = _LineCutter()
            last_line = None
            if self.tail:
                offset, digest, failure = self._scan_tail(file_fd, opened.st_size)
                if failure is not None:
                    reason = failure
                    return
                self.end_offset = self.tail_offset = offset
                self.tail_digest = digest
            else:
                total = line_count = position = 0
                limit_lines = (MAX_BATCH_LINES if self.max_lines is None
                               else self.max_lines)
                stopped = False
                resume = self.resume
                if resume is not None:
                    if not self.reread:
                        self.end_offset = resume["offset"]
                    if (opened.st_dev, opened.st_ino) != (resume["dev"], resume["ino"]):
                        self.resume_failure = "file_replaced"
                    elif opened.st_size < resume["offset"]:
                        self.resume_failure = "cursor_past_end"
                    elif self.reread:
                        if resume["offset"] == 0:
                            self.checkpoint_line = 0
                    elif resume["offset"] > 0:
                        window_size = min(MAX_LINE + 1, resume["offset"])
                        if window_size > self.budget:
                            self.limit_stop = True
                            stopped = True
                        else:
                            os.lseek(file_fd, resume["offset"] - window_size,
                                     os.SEEK_SET)
                            window = os.read(file_fd, window_size)
                            if len(window) != window_size:
                                raise OSError("short read")
                            total = window_size
                            self.bytes_read = total
                            self.resume_failure = _resume_window_verdict(
                                window, resume["offset"], resume["digest"])
                    if (self.resume_failure is None and not stopped
                            and not self.reread):
                        os.lseek(file_fd, resume["offset"], os.SEEK_SET)
                        position = resume["offset"]
                    if self.resume_failure is not None:
                        stopped = True
                while not stopped:
                    if self.piece:
                        room = min(64 * 1024, opened.st_size - position,
                                   self.budget - total)
                        if room <= 0:
                            self.limit_stop = position < opened.st_size
                            break
                    else:
                        room = min(64 * 1024, self.budget - total + 1)
                    block = os.read(file_fd, room)
                    if not block:
                        break
                    total += len(block)
                    position += len(block)
                    self.bytes_read = total
                    if not self.piece and total > self.budget:
                        reason = "source_budget_exceeded"
                        return
                    lines, failure = cutter.feed(block)
                    for line in lines:
                        line_count += 1
                        self.complete_lines = line_count
                        if not self.piece and line_count > MAX_BATCH_LINES:
                            reason = "source_budget_exceeded"
                            return
                        self.end_offset += len(line)
                        last_line = line
                        if (self.reread and self.checkpoint_line is None
                                and self.end_offset == resume["offset"]):
                            self.checkpoint_line = line_count
                            if hashlib.sha256(line).hexdigest() != resume["digest"]:
                                self.resume_failure = "digest_mismatch"
                        yield line
                        if self.piece and line_count >= limit_lines:
                            self.limit_stop = self.end_offset < opened.st_size
                            stopped = True
                            break
                    if not stopped and failure is not None:
                        reason = failure
                        return
                if (self.reread and self.resume_failure is None
                        and self.checkpoint_line is None and not self.limit_stop):
                    self.resume_failure = "not_line_boundary"
                self.tail_offset = self.end_offset
                if last_line is not None:
                    self.tail_digest = hashlib.sha256(last_line).hexdigest()
            if self.piece:
                reason = None
                return
            if cutter.pending:
                reason = "partial_tail"
                return
            reason = None
        except (OSError, ValueError, TypeError, Unavailable):
            reason = "source_read_unavailable"
        finally:
            if file_fd >= 0:
                os.close(file_fd)
            self.terminal_reason = reason


def _windows_component(value):
    if (not isinstance(value, str) or not value or value in {".", ".."}
            or any(char in value for char in "\\/:*?\"<>|\x00")
            or value.endswith((".", " "))
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise Unavailable("source_read_unavailable")
    stem = value.split(".", 1)[0].upper()
    if (stem in {"CON", "PRN", "AUX", "NUL"}
            or re.fullmatch(r"(?:COM|LPT)[1-9]", stem)):
        raise Unavailable("source_read_unavailable")
    try:
        if len(value.encode("utf-16-le")) > 510:
            raise Unavailable("source_read_unavailable")
    except UnicodeError:
        raise Unavailable("source_read_unavailable") from None
    return value


def _windows_absolute_parts(value):
    import ntpath
    if (not isinstance(value, str) or value.startswith("\\\\") or "/" in value
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise Unavailable("source_read_unavailable")
    drive, tail = ntpath.splitdrive(value)
    if not re.fullmatch(r"[A-Za-z]:", drive) or not tail.startswith("\\"):
        raise Unavailable("source_read_unavailable")
    raw_parts = tail[1:].split("\\")
    if not raw_parts or any(not part for part in raw_parts):
        raise Unavailable("source_read_unavailable")
    return drive, [_windows_component(part) for part in raw_parts]


def _iter_approved_lines(root, relative, budget=MAX_BATCH_BYTES, *,
                         piece=False, max_lines=None, tail=False, resume=None,
                         reread=False):
    """Stream complete lines from one explicitly approved synthetic/source path."""
    return _ApprovedLineStream(root, relative, budget, piece=piece,
                               max_lines=max_lines, tail=tail, resume=resume,
                               reread=reread)


def _valid_relative(value):
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    parts = PurePosixPath(value).parts
    if (not parts or value.startswith("/")
            or any(part in {"", ".", ".."} for part in parts)
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        return None
    return parts


def _utc_stamp(value):
    parsed = datetime.fromisoformat(_timestamp(value).replace("Z", "+00:00"))
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


_CLAIM_AGENT = re.compile(  # vendor-ok: matches existing source-session intent tags
    r"^(codex|claude|antigravity)-([0-9a-f]{8})$")


def _safe_claim_target(value):
    if not isinstance(value, str) or len(value) > 2048 or not value:
        return None
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        return None
    parts = _valid_relative(value)
    if parts is None or ":" in value:
        return None
    normalized = "/".join(parts)
    return normalized if normalized == value else None


def _claim_snapshot(project_alias, records):
    """Reduce a validated intent log to claim keys, intervals and safe targets."""
    claims = {}
    releases = {}
    for line in records:
        if len(line) > MAX_CLAIM_LINE or not line.endswith(b"\n"):
            raise Unavailable
        try:
            record = json.loads(line.decode("utf-8"), object_pairs_hook=_object,
                                parse_constant=_constant)
            if not isinstance(record, dict):
                raise ValueError
            event = record.get("event")
            if event == "claim":
                required = {"event", "id", "ts", "agent", "files", "action"}
                if not required <= set(record) or set(record) - required - {"stem"}:
                    raise ValueError
                raw_id = _text(record["id"])
                stamp = _utc_stamp(record["ts"])
                match = _CLAIM_AGENT.fullmatch(_text(record["agent"]))
                if not isinstance(record["files"], list):
                    raise ValueError
                if match is None:
                    # A named agent, not a session tag: it cannot be tied to a
                    # source, so skip it instead of refusing the whole project.
                    continue
                if not isinstance(record["action"], str):
                    raise ValueError
                if "stem" in record and record["stem"] is not None and not isinstance(record["stem"], str):
                    raise ValueError
                safe_targets = [_safe_claim_target(item) for item in record["files"]]
                targets = sorted({target for target in safe_targets if target is not None})
                invalid_target = any(target is None for target in safe_targets)
                confidence = ("reliable" if len(targets) == 1 and not invalid_target
                              else "ambiguous")
                key = _digest("claim", project_alias, raw_id)
                candidate = {
                    "claim_key": key, "project_alias": project_alias,
                    "tool": match.group(1), "session_digest": match.group(2),
                    "claimed_at": stamp, "released_at": None,
                    "targets": targets, "confidence": confidence,
                }
                previous = claims.get(key)
                if previous is None:
                    claims[key] = candidate
                elif {k: v for k, v in previous.items() if k != "released_at"} != {
                        k: v for k, v in candidate.items() if k != "released_at"}:
                    previous["confidence"] = "ambiguous"
                    previous["targets"] = []
                    previous["released_at"] = None
            elif event == "release":
                required = {"event", "id", "ts"}
                if not required <= set(record) or set(record) - required - {"commit"}:
                    raise ValueError
                if "commit" in record and record["commit"] is not None and not isinstance(record["commit"], str):
                    raise ValueError
                raw_id = _text(record["id"])
                stamp = _utc_stamp(record["ts"])
                key = _digest("claim", project_alias, raw_id)
                prior = releases.get(key)
                releases[key] = stamp if prior is None or prior == stamp else False
            else:
                raise ValueError
        except (ValueError, TypeError, KeyError, UnicodeError, RecursionError,
                OverflowError):
            raise Unavailable from None
    for key, claim in claims.items():
        released = releases.get(key)
        if released is False:
            claim["confidence"] = "ambiguous"
            claim["targets"] = []
        elif released is not None:
            if datetime.fromisoformat(released.replace("Z", "+00:00")) <= datetime.fromisoformat(
                    claim["claimed_at"].replace("Z", "+00:00")):
                claim["confidence"] = "ambiguous"
                claim["targets"] = []
            else:
                claim["released_at"] = released
        if claim["released_at"] is None and claim["confidence"] == "reliable":
            claim["confidence"] = "unattributed"
    return sorted(claims.values(), key=lambda item: item["claim_key"])


def _merge_claim_history(retained, incoming):
    merged = {claim["claim_key"]: dict(claim) for claim in retained}
    for claim in incoming:
        key = claim["claim_key"]
        prior = merged.get(key)
        if prior is None:
            merged[key] = dict(claim)
            continue
        stable_fields = ("project_alias", "tool", "session_digest", "claimed_at", "targets")
        if any(prior[field] != claim[field] for field in stable_fields):
            prior["confidence"] = "ambiguous"
            prior["targets"] = []
            prior["released_at"] = None
            continue
        if prior["confidence"] == "ambiguous" or claim["confidence"] == "ambiguous":
            prior["confidence"] = "ambiguous"
            prior["targets"] = []
            prior["released_at"] = None
        elif prior["released_at"] is None and claim["released_at"] is not None:
            prior["released_at"] = claim["released_at"]
            prior["confidence"] = claim["confidence"]
        elif (prior["released_at"] is not None and claim["released_at"] is not None
              and prior["released_at"] != claim["released_at"]):
            prior["confidence"] = "ambiguous"
            prior["targets"] = []
            prior["released_at"] = None
    return sorted(merged.values(), key=lambda item: item["claim_key"])


_LEDGER_EVENT_FIELDS = {
    "event_key", "source_aliases", "thread_key", "session_digest", "session_key",
    "turn_key", "root_turn_key", "observed_at", "time_coverage", "kinds",
    "cache_write_ttl", "project_alias", "project_association", "ownership",
    "model", "model_provenance", "effective_model", "account", "lineage_key",
    "reasons",
}
_CLAIM_FIELDS = {
    "claim_key", "project_alias", "tool", "session_digest", "claimed_at",
    "released_at", "targets", "confidence",
}
_CURSOR_FIELDS = {
    "source_alias", "file_key", "dev", "ino", "generation", "offset", "line",
    "size", "mtime_ns", "ctime_ns", "digest", "owner_key",
}
_START_FIELDS = {"source_alias", "started_at"}
_START_STAMP = "%Y-%m-%dT%H:%M:%SZ"
_MAPPING_FIELDS = {"event_key", "claim_key", "artifact", "confidence"}
_LINEAGE_SEQUENCE_FIELDS = {
    "event_key", "owner_key", "session_key", "turn_key", "root_key",
    "counter_family_key", "ordinal", "parent_ordinal", "kinds",
    "turn_snapshot", "thread_snapshot", "context_key",
}
_LINEAGE_PROOF_FIELDS = {
    "contract", "source_alias", "child_file_key", "child_generation",
    "child_dev", "child_ino", "child_offset", "child_line", "parent_cursors",
    "parent_key", "child_key", "session_key", "root_key", "boundary_turn_key",
    "parent_header_key", "counter_family_key", "boundary_line",
    "direct_record_count", "parent_prefix", "parent_terminal",
    "child_sequence",
    "child_event_keys",
}
_LINEAGE_FIELDS = {"lineage_key", "state", "proofs", "reasons"}
_WAIT_FIELDS = {
    "wait_key", "source_aliases", "occurrences", "thread_key", "session_key",
    "session_digest", "turn_key", "root_turn_key", "lineage_key", "project_alias",
    "project_association", "ownership", "classification", "started_at_ms",
    "completed_at_ms", "model", "model_provenance", "reasons",
}
_WAIT_REASONS = {
    "ambiguous_time", "conflicting_binding", "conflicting_timing",
    "test_command_classification_unknown", "project_path_unapproved",
    "project_remote_mismatch", "project_remote_unavailable",
    "project_layout_unsupported", "source_changed", "git_unavailable",
    "git_untrusted", "git_changed", "git_timeout", "git_output_limit",
    "git_parser_failed", "account_filter_unproven",
}
_LEDGER_FIELDS = {
    "schema", "reader_version", "ratio_version", "ratio_index", "events", "claims", "cursors",
    "mappings", "project_remotes", "aggregates", "lineages", "waits", "coverage",
    "starts", "fold_horizon", "daily", "agent_runs",
}


def _now_utc():
    """The run's one clock reading, an aware UTC time; tests patch it."""
    return datetime.now(timezone.utc)


def _start_stamp(moment):
    """A start time as the ledger spells it: UTC, whole seconds."""
    return moment.astimezone(timezone.utc).strftime(_START_STAMP)


def _parse_start(value):
    """Parse a saved start time; only the exact ledger spelling is accepted."""
    parsed = datetime.strptime(value, _START_STAMP).replace(tzinfo=timezone.utc)
    if parsed.strftime(_START_STAMP) != value:
        raise ValueError
    return parsed


def _parse_fold_day(value):
    """Parse a saved fold horizon, `YYYY-MM-DD` and nothing else."""
    parsed = datetime.strptime(value, "%Y-%m-%d").date()
    if parsed.isoformat() != value:
        raise ValueError
    return parsed


def _copy_event(event):
    return {name: (value.copy() if isinstance(value, (dict, list)) else value)
            for name, value in event.items()}


def _ratio_index_copy():
    return json.loads(json.dumps(_RATIO_INDEX, sort_keys=True))


def _validate_event(event):
    if not isinstance(event, dict) or set(event) != _LEDGER_EVENT_FIELDS:
        raise ValueError
    if (not isinstance(event["event_key"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", event["event_key"])):
        raise ValueError
    if (not isinstance(event["source_aliases"], list)
            or event["source_aliases"] != sorted(set(event["source_aliases"]))):
        raise ValueError
    for alias in event["source_aliases"]:
        _safe_alias(alias)
    for key in ("thread_key", "session_key", "turn_key", "root_turn_key"):
        if event[key] is not None and (not isinstance(event[key], str)
                                       or not re.fullmatch(r"[0-9a-f]{64}", event[key])):
            raise ValueError
    if event["session_digest"] is not None and (
            not isinstance(event["session_digest"], str)
            or not re.fullmatch(r"[0-9a-f]{8}", event["session_digest"])):
        raise ValueError
    if event["observed_at"] is not None:
        _utc_stamp(event["observed_at"])
    if event["time_coverage"] not in {"known", "unknown"}:
        raise ValueError
    if (event["time_coverage"] == "known") != (event["observed_at"] is not None):
        raise ValueError
    if not isinstance(event["kinds"], dict) or set(event["kinds"]) != set(_EVENT_KIND_NAMES):
        raise ValueError
    for value in event["kinds"].values():
        if value is not None:
            _counter(value)
    ttl = event["cache_write_ttl"]
    if (not isinstance(ttl, dict) or set(ttl) != {"five_minute", "one_hour"}
            or any(value is not None and (type(value) is not int
                                          or value < 0 or value > MAX_COUNTER)
                   for value in ttl.values())):
        raise ValueError
    if (ttl["five_minute"] is None) != (ttl["one_hour"] is None):
        raise ValueError
    if (ttl["five_minute"] is not None
            and (event["kinds"]["cache_write"] is None
                 or ttl["five_minute"] + ttl["one_hour"]
                 != event["kinds"]["cache_write"])):
        raise ValueError
    if event["project_alias"] is not None:
        _safe_alias(event["project_alias"])
    if event["project_association"] not in {"current_local_verified", "unknown"}:
        raise ValueError
    if (event["project_association"] == "current_local_verified") != (
            event["project_alias"] is not None):
        raise ValueError
    if event["ownership"] not in {"proven", "unknown"}:
        raise ValueError
    if event["model"] is not None:
        _safe_alias(event["model"])
    if event["model_provenance"] not in {"usage_record", "selected_context", "unknown"}:
        raise ValueError
    if event["effective_model"] is not None:
        _safe_alias(event["effective_model"])
        if (event["model_provenance"] != "usage_record"
                or event["effective_model"] != event["model"]):
            raise ValueError
    if (event["model_provenance"] == "selected_context"
            and event["effective_model"] is not None):
        raise ValueError
    if event["account"] is not None:
        raise ValueError
    if event["lineage_key"] is not None and (
            not isinstance(event["lineage_key"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", event["lineage_key"])):
        raise ValueError
    if (not isinstance(event["reasons"], list)
            or event["reasons"] != sorted(set(event["reasons"]))
            or any(not isinstance(reason, str)
                   or not re.fullmatch(r"[a-z][a-z0-9_]*", reason)
                   for reason in event["reasons"])):
        raise ValueError


def _validate_claim(claim):
    if not isinstance(claim, dict) or set(claim) != _CLAIM_FIELDS:
        raise ValueError
    if (not isinstance(claim["claim_key"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", claim["claim_key"])):
        raise ValueError
    _safe_alias(claim["project_alias"])
    if (claim["tool"] not in TOOLS or not isinstance(claim["session_digest"], str)
            or not re.fullmatch(r"[0-9a-f]{8}", claim["session_digest"])):
        raise ValueError
    _utc_stamp(claim["claimed_at"])
    if claim["released_at"] is not None:
        _utc_stamp(claim["released_at"])
    if not isinstance(claim["targets"], list):
        raise ValueError
    if any(_safe_claim_target(target) != target for target in claim["targets"]):
        raise ValueError
    if claim["confidence"] not in {"reliable", "ambiguous", "unattributed"}:
        raise ValueError


def _validate_lineage_sequence(sequence):
    if not isinstance(sequence, list) or not sequence or len(sequence) > MAX_RETAINED_EVENTS:
        raise ValueError
    for item in sequence:
        if not isinstance(item, dict) or set(item) != _LINEAGE_SEQUENCE_FIELDS:
            raise ValueError
        for key in ("event_key", "owner_key", "session_key", "turn_key",
                    "root_key", "counter_family_key", "context_key"):
            if not isinstance(item[key], str) or not re.fullmatch(r"[0-9a-f]{64}", item[key]):
                raise ValueError
        _counter(item["ordinal"])
        if item["parent_ordinal"] is not None:
            _counter(item["parent_ordinal"])
        for vector_name in ("kinds", "turn_snapshot", "thread_snapshot"):
            vector = item[vector_name]
            if not _complete_vector(vector):
                raise ValueError
    event_keys = [item["event_key"] for item in sequence]
    if len(event_keys) != len(set(event_keys)):
        raise ValueError


def _validate_lineage_proof(proof):
    if not isinstance(proof, dict) or set(proof) != _LINEAGE_PROOF_FIELDS:
        raise ValueError
    if proof["contract"] != "codex-copied-legacy/1":
        raise ValueError
    _safe_alias(proof["source_alias"])
    for name in ("child_file_key", "parent_key", "child_key", "session_key",
                 "root_key", "parent_header_key", "counter_family_key",
                 "boundary_turn_key"):
        if not isinstance(proof[name], str) or not re.fullmatch(r"[0-9a-f]{64}", proof[name]):
            raise ValueError
    for name in ("child_dev", "child_ino", "child_generation",
                 "child_offset", "child_line", "boundary_line",
                 "direct_record_count"):
        (_unsigned64 if name in {"child_dev", "child_ino"} else _counter)(proof[name])
    parents = proof["parent_cursors"]
    if (not isinstance(parents, list) or not parents
            or parents != sorted(parents, key=lambda item: item.get("file_key", ""))):
        raise ValueError
    for parent in parents:
        if not isinstance(parent, dict) or set(parent) != {
                "file_key", "dev", "ino", "generation", "offset", "line"}:
            raise ValueError
        if not isinstance(parent["file_key"], str) or not re.fullmatch(
                r"[0-9a-f]{64}", parent["file_key"]):
            raise ValueError
        for name in ("dev", "ino"):
            _unsigned64(parent[name])
        for name in ("generation", "offset", "line"):
            _counter(parent[name])
    _validate_lineage_sequence(proof["parent_prefix"])
    _validate_lineage_sequence(proof["child_sequence"])
    if len(proof["parent_prefix"]) + len(proof["child_sequence"]) > MAX_RETAINED_EVENTS:
        raise ValueError
    if proof["parent_terminal"] != proof["parent_prefix"][-1]:
        raise ValueError
    if any(parent["file_key"] == proof["child_file_key"] for parent in parents):
        raise ValueError
    child_keys = sorted(item["event_key"] for item in proof["child_sequence"])
    if proof["child_event_keys"] != sorted(set(proof["child_event_keys"])) \
            or proof["child_event_keys"] != child_keys:
        raise ValueError
    if any(item["owner_key"] != proof["parent_key"]
           or item["session_key"] != proof["session_key"]
           for item in proof["parent_prefix"]):
        raise ValueError
    if any(item["parent_ordinal"] is None for item in proof["parent_prefix"]):
        raise ValueError
    if any(item["parent_ordinal"] is not None for item in proof["child_sequence"]):
        raise ValueError
    if any(item["owner_key"] != proof["child_key"]
           or item["session_key"] != proof["session_key"]
           or item["root_key"] != proof["root_key"]
           or item["turn_key"] != proof["boundary_turn_key"]
           for item in proof["child_sequence"]):
        raise ValueError
    if proof["counter_family_key"] != _digest(
            "codex-counter-family", proof["session_key"], proof["root_key"]):
        raise ValueError
    if proof["parent_terminal"]["counter_family_key"] != proof["counter_family_key"]:
        raise ValueError
    if any(item["counter_family_key"] != _digest(
            "codex-counter-family", item["session_key"], item["root_key"])
           for item in proof["parent_prefix"] + proof["child_sequence"]):
        raise ValueError
    baseline = proof["parent_terminal"]["thread_snapshot"]
    running = {name: 0 for name in _EVENT_KIND_NAMES}
    for item in proof["child_sequence"]:
        running = _add_vectors(running, item["kinds"])
        if item["turn_snapshot"] != running:
            raise ValueError
        if item["thread_snapshot"] != _add_vectors(baseline, running):
            raise ValueError


def _lineage_semantics(proof):
    return {key: proof[key] for key in (
        "contract", "parent_key", "child_key", "session_key", "root_key",
        "parent_header_key", "counter_family_key", "boundary_turn_key",
        "parent_prefix", "parent_terminal",
        "child_sequence", "child_event_keys")}


def _proof_only_gained_turns(old, new):
    """True when `new` is `old` plus later child turns and nothing else changed."""
    before, after = old["child_sequence"], new["child_sequence"]
    rest = {key for key in _lineage_semantics(old)
            if key not in {"child_sequence", "child_event_keys"}}
    return (len(after) > len(before) and after[:len(before)] == before
            and all(old[key] == new[key] for key in rest))


def _merge_lineage_history(retained, incoming, conflicts=()):
    history = {item["lineage_key"]: {
        "lineage_key": item["lineage_key"], "state": item["state"],
        "proofs": [dict(proof) for proof in item["proofs"]],
        "reasons": list(item["reasons"]),
    } for item in retained}
    for proof in incoming:
        _validate_lineage_proof(proof)
        key = _digest("codex-lineage", proof["child_key"])
        prior = history.get(key)
        if prior is None:
            history[key] = {"lineage_key": key, "state": "verified",
                            "proofs": [proof], "reasons": []}
            continue
        if any(_lineage_semantics(old) == _lineage_semantics(proof)
               for old in prior["proofs"]):
            continue
        if (prior["state"] == "verified" and len(prior["proofs"]) == 1
                and _proof_only_gained_turns(prior["proofs"][0], proof)):
            prior["proofs"] = [proof]
            continue
        if not any(old == proof for old in prior["proofs"]):
            prior["proofs"].append(proof)
        prior["proofs"].sort(key=lambda item: _digest(json.dumps(
            item, sort_keys=True, separators=(",", ":"))))
        prior["state"] = "conflicting"
        prior["reasons"] = ["conflicting_binding"]
    for key in conflicts:
        prior = history.get(key)
        if prior is not None:
            prior["state"] = "conflicting"
            prior["reasons"] = ["conflicting_binding"]
    return [history[key] for key in sorted(history)]


def _validate_lineage(lineage):
    if not isinstance(lineage, dict) or set(lineage) != _LINEAGE_FIELDS:
        raise ValueError
    if (not isinstance(lineage["lineage_key"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", lineage["lineage_key"])
            or not isinstance(lineage["proofs"], list) or not lineage["proofs"]
            or not isinstance(lineage["reasons"], list)
            or lineage["reasons"] != sorted(set(lineage["reasons"]))
            or any(reason not in {"conflicting_binding"} for reason in lineage["reasons"])):
        raise ValueError
    for proof in lineage["proofs"]:
        _validate_lineage_proof(proof)
        if lineage["lineage_key"] != _digest("codex-lineage", proof["child_key"]):
            raise ValueError
    expected = ("verified" if len(lineage["proofs"]) == 1 and not lineage["reasons"]
                else "conflicting")
    if lineage["state"] != expected:
        raise ValueError


def _validate_wait(wait):
    if not isinstance(wait, dict) or set(wait) != _WAIT_FIELDS:
        raise ValueError
    if (not isinstance(wait["wait_key"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", wait["wait_key"])):
        raise ValueError
    aliases = wait["source_aliases"]
    if not isinstance(aliases, list) or not aliases or aliases != sorted(set(aliases)):
        raise ValueError
    for alias in aliases:
        _safe_alias(alias)
    occurrences = wait["occurrences"]
    if (not isinstance(occurrences, list) or not occurrences
            or len(occurrences) > MAX_WAIT_OCCURRENCES):
        raise ValueError
    occurrence_keys = []
    for occurrence in occurrences:
        if not isinstance(occurrence, dict) or set(occurrence) != {
                "file_key", "generation", "line"}:
            raise ValueError
        if (not isinstance(occurrence["file_key"], str)
                or not re.fullmatch(r"[0-9a-f]{64}", occurrence["file_key"])):
            raise ValueError
        if _counter(occurrence["generation"]) < 1 or _counter(occurrence["line"]) < 1:
            raise ValueError
        occurrence_keys.append((occurrence["file_key"], occurrence["generation"],
                                occurrence["line"]))
    if occurrence_keys != sorted(set(occurrence_keys)):
        raise ValueError
    for key in ("thread_key", "session_key", "turn_key", "root_turn_key", "lineage_key"):
        if wait[key] is not None and (not isinstance(wait[key], str)
                                      or not re.fullmatch(r"[0-9a-f]{64}", wait[key])):
            raise ValueError
    if wait["session_digest"] is not None and (
            not isinstance(wait["session_digest"], str)
            or not re.fullmatch(r"[0-9a-f]{8}", wait["session_digest"])):
        raise ValueError
    if wait["project_alias"] is not None:
        _safe_alias(wait["project_alias"])
    if wait["project_association"] not in {"current_local_verified", "unknown"}:
        raise ValueError
    if (wait["project_association"] == "current_local_verified") != (
            wait["project_alias"] is not None):
        raise ValueError
    if wait["ownership"] not in {"proven", "unknown"}:
        raise ValueError
    if wait["classification"] not in {"pytest", "unknown"}:
        raise ValueError
    for name in ("started_at_ms", "completed_at_ms"):
        if wait[name] is not None:
            _counter(wait[name])
    if ((wait["started_at_ms"] is None) != (wait["completed_at_ms"] is None)
            or (wait["started_at_ms"] is not None
                and not 0 < wait["started_at_ms"] < wait["completed_at_ms"])):
        raise ValueError
    if wait["started_at_ms"] is not None:
        try:
            _wait_datetime(wait["started_at_ms"])
            _wait_datetime(wait["completed_at_ms"])
        except (OverflowError, ValueError):
            raise ValueError
    if wait["model"] is not None:
        _safe_alias(wait["model"])
    if wait["model_provenance"] not in {"selected_context", "unknown"}:
        raise ValueError
    if (not isinstance(wait["reasons"], list)
            or wait["reasons"] != sorted(set(wait["reasons"]))
            or any(reason not in _WAIT_REASONS for reason in wait["reasons"])):
        raise ValueError
    if wait["ownership"] == "proven" and any(wait[key] is None for key in (
            "thread_key", "session_key", "session_digest", "turn_key", "root_turn_key")):
        raise ValueError
    if ("conflicting_binding" in wait["reasons"]
            and (wait["ownership"] != "unknown"
                 or wait["project_association"] != "unknown")):
        raise ValueError


def _validate_aggregate_row(aggregate):
    if (not isinstance(aggregate, dict)
            or set(aggregate) != {
                "project_alias", "day", "tool", "model", "model_provenance",
                "effective_model", "events", "unknown_events", "kinds",
                "reference_index", "reference_tokens"}):
        raise ValueError
    if aggregate["project_alias"] is not None:
        _safe_alias(aggregate["project_alias"])
    if aggregate["day"] is not None:
        parsed_day = datetime.fromisoformat(aggregate["day"])
        if parsed_day.date().isoformat() != aggregate["day"]:
            raise ValueError
    if aggregate["tool"] is not None and aggregate["tool"] not in TOOLS:
        raise ValueError
    if aggregate["model"] is not None:
        _safe_alias(aggregate["model"])
    if aggregate["effective_model"] is not None:
        _safe_alias(aggregate["effective_model"])
    if aggregate["model_provenance"] not in {
            "usage_record", "selected_context", "unknown"}:
        raise ValueError
    event_count = _counter(aggregate["events"])
    unknown_count = _counter(aggregate["unknown_events"])
    if unknown_count > event_count:
        raise ValueError
    kinds = aggregate["kinds"]
    if not isinstance(kinds, dict) or set(kinds) != set(_EVENT_KIND_NAMES):
        raise ValueError
    for value in kinds.values():
        if value is not None:
            _counter(value)
    if (not isinstance(aggregate["reference_index"], str)
            or not _PULSE.RATIO_VERSION_FORM.fullmatch(aggregate["reference_index"])
            or not isinstance(aggregate["reference_tokens"], dict)
            or set(aggregate["reference_tokens"])
            != {*_EVENT_KIND_NAMES, "total"}):
        raise ValueError
    for value in aggregate["reference_tokens"].values():
        if value is not None and (not isinstance(value, str)
                or not re.fullmatch(r"(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", value)):
            raise ValueError


def _validate_agent_runs(value):
    if not isinstance(value, dict) or set(value) != {"transcripts", "summaries", "unclassified"}:
        raise ValueError
    _counter(value["unclassified"])
    for name, cap in (("transcripts", MAX_AGENT_TRANSCRIPTS),
                      ("summaries", MAX_AGENT_SUMMARIES)):
        rows = value[name]
        if not isinstance(rows, list) or len(rows) > cap:
            raise ValueError
        keys = []
        for row in rows:
            if not isinstance(row, dict) or set(row) != {"session_key", "agent_key"}:
                raise ValueError
            for field in ("session_key", "agent_key"):
                if (not isinstance(row[field], str)
                        or not re.fullmatch(r"[0-9a-f]{64}", row[field])):
                    raise ValueError
            keys.append((row["session_key"], row["agent_key"]))
        if keys != sorted(keys) or len(set(keys)) != len(keys):
            raise ValueError


def _load_ledger(raw, now=None):
    if raw is None:
        return {
            "schema": LEDGER_SCHEMA, "reader_version": READER_VERSION,
            "ratio_version": RATIO_VERSION, "ratio_index": _ratio_index_copy(),
            "events": [], "claims": [], "cursors": [],
            "mappings": [], "project_remotes": [], "aggregates": [], "lineages": [],
            "waits": [], "starts": [], "fold_horizon": None, "daily": [],
            "agent_runs": _empty_agent_runs(),
            "coverage": {"global": "unknown", "reasons": []},
        }
    try:
        if not isinstance(raw, bytes) or len(raw) > MAX_LEDGER_BYTES:
            raise ValueError
        ledger = json.loads(raw.decode("utf-8"), object_pairs_hook=_object,
                            parse_constant=_constant)
        if isinstance(ledger, dict) and ledger.get("schema") in _OLD_LEDGER_SCHEMAS:
            raise Unavailable("ledger_old_schema")
        if not isinstance(ledger, dict) or set(ledger) != _LEDGER_FIELDS:
            raise ValueError
        if (ledger["schema"] != LEDGER_SCHEMA
                or ledger["reader_version"] != READER_VERSION
                or not isinstance(ledger["ratio_version"], str)
                or not _PULSE.RATIO_VERSION_FORM.fullmatch(ledger["ratio_version"])
                or not isinstance(ledger["ratio_index"], dict)):
            raise ValueError
        # A ledger outlives a table change: nothing reads the stored table or label.
        ledger["ratio_version"] = RATIO_VERSION
        ledger["ratio_index"] = _ratio_index_copy()
        if any(not isinstance(ledger[key], list) for key in (
                "events", "claims", "cursors", "mappings", "project_remotes",
                "aggregates", "lineages", "waits", "starts", "daily")):
            raise ValueError
        _validate_agent_runs(ledger["agent_runs"])
        now = _now_utc() if now is None else now
        if ledger["fold_horizon"] is not None and (
                not isinstance(ledger["fold_horizon"], str)
                or _parse_fold_day(ledger["fold_horizon"])
                > now.astimezone(timezone.utc).date()):
            raise ValueError
        start_aliases = set()
        for start in ledger["starts"]:
            if not isinstance(start, dict) or set(start) != _START_FIELDS:
                raise ValueError
            _safe_alias(start["source_alias"])
            if (not isinstance(start["started_at"], str)
                    or _parse_start(start["started_at"]) > now
                    or start["source_alias"] in start_aliases):
                raise ValueError
            start_aliases.add(start["source_alias"])
        if (len(ledger["events"]) > MAX_RETAINED_EVENTS
                or len(ledger["lineages"]) > MAX_RETAINED_EVENTS
                or len(ledger["waits"]) > MAX_RETAINED_WAITS):
            raise ValueError
        wait_keys = set()
        occurrence_count = 0
        for wait in ledger["waits"]:
            _validate_wait(wait)
            occurrence_count += len(wait["occurrences"])
            if wait["wait_key"] in wait_keys:
                raise ValueError
            wait_keys.add(wait["wait_key"])
        if occurrence_count > MAX_WAIT_OCCURRENCES:
            raise ValueError
        event_keys = set()
        events_by_key = {}
        for event in ledger["events"]:
            _validate_event(event)
            if event["event_key"] in event_keys:
                raise ValueError
            event_keys.add(event["event_key"])
            events_by_key[event["event_key"]] = event
            if (ledger["fold_horizon"] is not None
                    and event["time_coverage"] == "known"
                    and event["observed_at"] is not None
                    and datetime.fromisoformat(event["observed_at"].replace("Z", "+00:00"))
                    .astimezone(timezone.utc).date().isoformat()
                    < ledger["fold_horizon"]):
                raise ValueError
        claim_keys = set()
        for claim in ledger["claims"]:
            _validate_claim(claim)
            if claim["claim_key"] in claim_keys:
                raise ValueError
            claim_keys.add(claim["claim_key"])
        for cursor in ledger["cursors"]:
            if not isinstance(cursor, dict) or set(cursor) != _CURSOR_FIELDS:
                raise ValueError
            _safe_alias(cursor["source_alias"])
            if (not isinstance(cursor["file_key"], str)
                    or not re.fullmatch(r"[0-9a-f]{64}", cursor["file_key"])):
                raise ValueError
            for field in ("dev", "ino"):
                _unsigned64(cursor[field])
            for field in ("generation", "offset", "line", "size", "mtime_ns", "ctime_ns"):
                _counter(cursor[field])
            for field in ("digest", "owner_key"):
                if cursor[field] is not None and (
                        not isinstance(cursor[field], str)
                        or not re.fullmatch(r"[0-9a-f]{64}", cursor[field])):
                    raise ValueError
            if (cursor["digest"] is None) != (cursor["offset"] == 0):
                raise ValueError
        cursor_keys = [cursor["file_key"] for cursor in ledger["cursors"]]
        if len(cursor_keys) != len(set(cursor_keys)):
            raise ValueError
        for mapping in ledger["mappings"]:
            if not isinstance(mapping, dict) or set(mapping) != _MAPPING_FIELDS:
                raise ValueError
            if (not isinstance(mapping["event_key"], str)
                    or not isinstance(mapping["claim_key"], str)
                    or not re.fullmatch(r"[0-9a-f]{64}", mapping["event_key"])
                    or not re.fullmatch(r"[0-9a-f]{64}", mapping["claim_key"])
                    or _safe_claim_target(mapping["artifact"]) != mapping["artifact"]
                    or mapping["confidence"] != "reliable"):
                raise ValueError
            if mapping["event_key"] not in event_keys or mapping["claim_key"] not in claim_keys:
                raise ValueError
        mapping_events = [mapping["event_key"] for mapping in ledger["mappings"]]
        if len(mapping_events) != len(set(mapping_events)):
            raise ValueError
        for remote in ledger["project_remotes"]:
            if (not isinstance(remote, dict) or set(remote) != {"alias", "remote"}
                    or _strip_remote(remote["remote"]) != remote["remote"]):
                raise ValueError
            _safe_alias(remote["alias"])
        remote_aliases = [remote["alias"] for remote in ledger["project_remotes"]]
        if len(remote_aliases) != len(set(remote_aliases)):
            raise ValueError
        lineage_keys = []
        lineage_by_key = {}
        for lineage in ledger["lineages"]:
            _validate_lineage(lineage)
            lineage_keys.append(lineage["lineage_key"])
            lineage_by_key[lineage["lineage_key"]] = lineage
        if len(lineage_keys) != len(set(lineage_keys)):
            raise ValueError
        for event in ledger["events"]:
            if event["lineage_key"] is not None:
                lineage = lineage_by_key.get(event["lineage_key"])
                if lineage is None or (
                        lineage["state"] != "verified" and event["ownership"] == "proven"):
                    raise ValueError
        for lineage in ledger["lineages"]:
            for proof in lineage["proofs"]:
                for event_key in proof["child_event_keys"]:
                    # An event before a bookmark, or a folded one, is not held.
                    event = events_by_key.get(event_key)
                    if event is not None and event["lineage_key"] != lineage["lineage_key"]:
                        raise ValueError
        for wait in ledger["waits"]:
            if wait["lineage_key"] is not None:
                lineage = lineage_by_key.get(wait["lineage_key"])
                if lineage is None or (lineage["state"] != "verified"
                                       and wait["ownership"] == "proven"):
                    raise ValueError
        for aggregate in ledger["aggregates"]:
            _validate_aggregate_row(aggregate)
        daily_keys = set()
        for aggregate in ledger["daily"]:
            _validate_aggregate_row(aggregate)
            key = _aggregate_key(aggregate)
            if (aggregate["day"] is None or key in daily_keys
                    or ledger["fold_horizon"] is None
                    or aggregate["day"] >= ledger["fold_horizon"]):
                raise ValueError
            daily_keys.add(key)
        coverage = ledger["coverage"]
        if (not isinstance(coverage, dict) or set(coverage) != {"global", "reasons"}
                or coverage["global"] != "unknown"
                or not isinstance(coverage["reasons"], list)
                or coverage["reasons"] != sorted(set(coverage["reasons"]))
                or any(not isinstance(reason, str)
                       or not re.fullmatch(r"[a-z][a-z0-9_]*", reason)
                       for reason in coverage["reasons"])):
            raise ValueError
        return ledger
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError,
            OverflowError, AttributeError):
        raise Unavailable("ledger_invalid") from None


def _merge_retained_event(prior, incoming):
    """Merge full rescans; conflict evidence is sticky and never selects a winner."""
    prior["source_aliases"] = sorted(set(prior["source_aliases"])
                                     | set(incoming["source_aliases"]))
    reasons = set(prior["reasons"]) | set(incoming["reasons"])
    usage_difference = (prior["kinds"] != incoming["kinds"]
                        or prior["cache_write_ttl"] != incoming["cache_write_ttl"])
    if "conflicting_usage" in reasons or usage_difference:
        prior["kinds"] = _unknown_kinds()
        prior["cache_write_ttl"] = {"five_minute": None, "one_hour": None}
        if usage_difference:
            reasons.add("conflicting_usage")

    if prior["observed_at"] is None or incoming["observed_at"] is None:
        if prior["observed_at"] != incoming["observed_at"]:
            reasons.add("ambiguous_time")
        prior["observed_at"] = None
        prior["time_coverage"] = "unknown"
    elif prior["observed_at"] != incoming["observed_at"]:
        prior["observed_at"] = None
        prior["time_coverage"] = "unknown"
        reasons.add("ambiguous_time")

    fields = ("thread_key", "session_digest", "session_key", "turn_key", "root_turn_key")
    identity_conflict = any(prior[field] is not None and incoming[field] is not None
                            and prior[field] != incoming[field] for field in fields)
    lineage_conflict = (prior["lineage_key"] is not None
                        and incoming["lineage_key"] is not None
                        and prior["lineage_key"] != incoming["lineage_key"])
    if lineage_conflict:
        reasons.add("conflicting_binding")
    model_conflict = (prior["model"] != incoming["model"]
                      or prior["effective_model"] != incoming["effective_model"]
                      or prior["model_provenance"] != incoming["model_provenance"])
    if model_conflict:
        reasons.add("conflicting_binding")
    if "conflicting_binding" in reasons or identity_conflict:
        for field in ("thread_key", "session_digest", "session_key", "turn_key",
                      "root_turn_key"):
            prior[field] = None
        prior["project_alias"] = None
        prior["project_association"] = "unknown"
        prior["ownership"] = "unknown"
        prior["model"] = None
        prior["model_provenance"] = "unknown"
        prior["effective_model"] = None
        reasons.add("conflicting_binding")
    else:
        if prior["ownership"] == "unknown" and incoming["ownership"] == "proven":
            prior["ownership"] = "proven"
        if prior["session_digest"] is None:
            prior["session_digest"] = incoming["session_digest"]
        if prior["thread_key"] is None:
            prior["thread_key"] = incoming["thread_key"]
        if prior["lineage_key"] is None:
            prior["lineage_key"] = incoming["lineage_key"]
        for field in ("session_key", "turn_key", "root_turn_key"):
            if prior[field] is None:
                prior[field] = incoming[field]
        if prior["project_association"] == "current_local_verified":
            if (incoming["project_association"] == "current_local_verified"
                    and prior["project_alias"] != incoming["project_alias"]):
                prior["project_alias"] = None
                prior["project_association"] = "unknown"
                prior["ownership"] = "unknown"
                prior["model"] = None
                prior["model_provenance"] = "unknown"
                prior["effective_model"] = None
                reasons.add("conflicting_binding")
        elif incoming["project_association"] == "current_local_verified":
            prior["project_alias"] = incoming["project_alias"]
            prior["project_association"] = "current_local_verified"
    if "conflicting_binding" in reasons:
        for field in ("thread_key", "session_digest", "session_key", "turn_key", "root_turn_key"):
            prior[field] = None
        prior["project_alias"] = None
        prior["project_association"] = "unknown"
        prior["ownership"] = "unknown"
        prior["model"] = None
        prior["model_provenance"] = "unknown"
        prior["effective_model"] = None
    if "project_remote_mismatch" in reasons:
        prior["project_alias"] = None
        prior["project_association"] = "unknown"
    prior["reasons"] = sorted(reasons)


def _merge_events(retained, incoming):
    by_key = {event["event_key"]: _copy_event(event) for event in retained}
    for event in incoming:
        _validate_event(event)
        prior = by_key.get(event["event_key"])
        if prior is None:
            by_key[event["event_key"]] = _copy_event(event)
        else:
            _merge_retained_event(prior, event)
    return [by_key[key] for key in sorted(by_key)]


def _merge_wait_rows(retained, incoming):
    """Deduplicate retained timing evidence and make conflicts sticky."""
    by_key = {row["wait_key"]: {
        name: (value.copy() if isinstance(value, (dict, list)) else value)
        for name, value in row.items()} for row in retained}
    for incoming_row in incoming:
        _validate_wait(incoming_row)
        key = incoming_row["wait_key"]
        prior = by_key.get(key)
        if prior is None:
            by_key[key] = {
                name: (value.copy() if isinstance(value, (dict, list)) else value)
                for name, value in incoming_row.items()}
            continue
        prior["source_aliases"] = sorted(set(prior["source_aliases"])
                                         | set(incoming_row["source_aliases"]))
        occurrence_map = {
            (item["file_key"], item["generation"], item["line"]): item
            for item in prior["occurrences"]
        }
        occurrence_map.update({
            (item["file_key"], item["generation"], item["line"]): item
            for item in incoming_row["occurrences"]
        })
        prior["occurrences"] = [occurrence_map[key] for key in sorted(occurrence_map)]
        reasons = set(prior["reasons"]) | set(incoming_row["reasons"])
        binding = ("thread_key", "session_key", "session_digest", "turn_key",
                   "root_turn_key", "lineage_key", "project_alias",
                   "project_association", "ownership", "model", "model_provenance")
        binding_conflict = any(prior[field] != incoming_row[field] for field in binding)
        if binding_conflict or "conflicting_binding" in reasons:
            for field in ("thread_key", "session_key", "session_digest", "turn_key",
                          "root_turn_key", "lineage_key", "project_alias", "model"):
                prior[field] = None
            prior["project_association"] = "unknown"
            prior["ownership"] = "unknown"
            prior["model_provenance"] = "unknown"
            reasons.add("conflicting_binding")
        if (prior["classification"] != incoming_row["classification"]
                or "conflicting_timing" in reasons):
            prior["classification"] = "unknown"
            reasons.add("conflicting_timing")
        if ((prior["started_at_ms"], prior["completed_at_ms"])
                != (incoming_row["started_at_ms"], incoming_row["completed_at_ms"])
                or "ambiguous_time" in reasons):
            prior["started_at_ms"] = prior["completed_at_ms"] = None
            reasons.add("ambiguous_time")
        prior["reasons"] = sorted(reasons)
    if len(by_key) > MAX_RETAINED_WAITS or sum(
            len(row["occurrences"]) for row in by_key.values()) > MAX_WAIT_OCCURRENCES:
        raise Unavailable("source_budget_exceeded")
    result = [by_key[key] for key in sorted(by_key)]
    for row in result:
        _validate_wait(row)
    return result


def _recompute_aggregates(events, config):
    tool_by_alias = {source["alias"]: source["tool"] for source in config["sources"]}
    groups = {}
    for event in events:
        aliases = event["source_aliases"]
        tools = {tool_by_alias[alias] for alias in aliases if alias in tool_by_alias}
        tool = next(iter(tools)) if len(tools) == 1 else None
        project = (event["project_alias"]
                   if event["project_association"] == "current_local_verified"
                   and event["ownership"] == "proven" else None)
        day = None
        if event["time_coverage"] == "known" and event["observed_at"] is not None:
            day = datetime.fromisoformat(
                event["observed_at"].replace("Z", "+00:00")).astimezone(timezone.utc).date().isoformat()
        key = (project, day, tool, event["model"],
               event["model_provenance"], event["effective_model"])
        group = groups.setdefault(key, {"events": [], "unknown": 0})
        group["events"].append(event)
        if any(value is None for value in event["kinds"].values()):
            group["unknown"] += 1
    result = []
    for (project, day, tool, model, model_provenance, effective_model), group in sorted(
            groups.items(), key=lambda item: tuple("" if v is None else str(v)
                                                   for v in item[0])):
        kinds = {}
        for name in _EVENT_KIND_NAMES:
            values = [event["kinds"][name] for event in group["events"]]
            kinds[name] = None if any(value is None for value in values) else sum(values)
        weighted = [_weighted_reference_tokens(event) for event in group["events"]]
        reference = {}
        for name in (*_EVENT_KIND_NAMES, "total"):
            values = [row[name] for row in weighted]
            reference[name] = (None if any(value is None for value in values)
                               else _fraction_text(sum(
                                   (Fraction(Decimal(value)) for value in values),
                                   Fraction(0))))
        result.append({"project_alias": project, "day": day, "tool": tool,
                       "model": model, "model_provenance": model_provenance,
                       "effective_model": effective_model, "events": len(group["events"]),
                       "unknown_events": group["unknown"], "kinds": kinds,
                       "reference_index": RATIO_VERSION,
                       "reference_tokens": reference})
    return result


def _aggregate_key(item):
    return (item["project_alias"], item["day"], item["tool"], item["model"],
            item["model_provenance"], item["effective_model"])


def _aggregate_sort_key(item):
    return tuple("" if value is None else str(value) for value in _aggregate_key(item))


def _add_rows(left, right):
    """Add two aggregate rows of equal key, as one pass over all their events would."""
    kinds = {}
    for name in _EVENT_KIND_NAMES:
        pair = (left["kinds"][name], right["kinds"][name])
        kinds[name] = None if None in pair else pair[0] + pair[1]
    reference = {}
    for name in (*_EVENT_KIND_NAMES, "total"):
        pair = (left["reference_tokens"][name], right["reference_tokens"][name])
        reference[name] = None if None in pair else _fraction_text(
            Fraction(Decimal(pair[0])) + Fraction(Decimal(pair[1])))
    return {
        "project_alias": left["project_alias"], "day": left["day"],
        "tool": left["tool"], "model": left["model"],
        "model_provenance": left["model_provenance"],
        "effective_model": left["effective_model"],
        "events": left["events"] + right["events"],
        "unknown_events": left["unknown_events"] + right["unknown_events"],
        "kinds": kinds,
        "reference_index": (left["reference_index"]
                            if left["reference_index"] == right["reference_index"]
                            else RATIO_VERSION),
        "reference_tokens": reference,
    }


def _merge_rows(rows):
    """Rows of equal key added into one; sorted like `aggregates`."""
    by_key = {}
    for item in rows:
        key = _aggregate_key(item)
        by_key[key] = _add_rows(by_key[key], item) if key in by_key else item
    return sorted(by_key.values(), key=_aggregate_sort_key)


def _event_day(event):
    """The UTC day of an event with a known time, else None."""
    if event["time_coverage"] != "known" or event["observed_at"] is None:
        return None
    return datetime.fromisoformat(event["observed_at"].replace("Z", "+00:00")
                                  ).astimezone(timezone.utc).date()


def _fold_horizon_day(events, saved, now, catching_up):
    """The first UTC day whose events stay as individual events (plan D9).

    It is the earliest day from `today - FOLD_AFTER_DAYS` (never before the saved
    horizon) at which no more than RETAINED_EVENT_TARGET events would stay, counting
    every event of unknown time. A run that is catching up raises nothing, unless the
    ledger holds more than FOLD_FORCE_EVENTS: a reply whose usage lines straddle a
    piece boundary must still meet its first half in the retained events.
    """
    saved_day = None if saved is None else _parse_fold_day(saved)
    if catching_up and len(events) <= FOLD_FORCE_EVENTS:
        return saved_day
    today = now.astimezone(timezone.utc).date()
    horizon = today - timedelta(days=FOLD_AFTER_DAYS)
    if saved_day is not None and saved_day > horizon:
        horizon = saved_day
    per_day, kept = {}, 0
    for event in events:
        day = _event_day(event)
        if day is None or day >= horizon:
            kept += 1
            if day is not None:
                per_day[day] = per_day.get(day, 0) + 1
    while kept > RETAINED_EVENT_TARGET and horizon < today:
        kept -= per_day.get(horizon, 0)
        horizon += timedelta(days=1)
    return horizon


def _fold_events(events, daily, config, saved, now, catching_up):
    """Fold events of a known day before the horizon into the daily rows.

    Returns the events that stay, the daily rows and the saved horizon text. An event
    of unknown time never folds.
    """
    horizon = _fold_horizon_day(events, saved, now, catching_up)
    if horizon is None:
        return events, daily, None
    old = [event for event in events
           if (day := _event_day(event)) is not None and day < horizon]
    if old:
        gone = {event["event_key"] for event in old}
        events = [event for event in events if event["event_key"] not in gone]
        daily = _merge_rows([*daily, *_recompute_aggregates(old, config)])
    return events, daily, horizon.isoformat()


def _drop_folded_lineages(lineages, events, waits):
    """Drop a verified lineage whose child events are all folded or absent and which
    no retained event or wait cites; a conflicting one is kept (plan D9)."""
    held = {event["event_key"] for event in events}
    cited = {event["lineage_key"] for event in events}
    cited.update(wait["lineage_key"] for wait in waits)
    return [lineage for lineage in lineages
            if lineage["state"] != "verified" or lineage["lineage_key"] in cited
            or any(key in held for proof in lineage["proofs"]
                   for key in proof["child_event_keys"])]


def _wait_datetime(value):
    return datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(milliseconds=value)


def _split_wait_days(start_ms, end_ms):
    start = _wait_datetime(start_ms)
    end = _wait_datetime(end_ms)
    pieces = []
    cursor = start
    while cursor < end:
        next_day = datetime.combine(cursor.date() + timedelta(days=1),
                                    datetime.min.time(), tzinfo=timezone.utc)
        stop = min(end, next_day)
        left = int((cursor - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() * 1000)
        right = int((stop - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() * 1000)
        pieces.append((cursor.date().isoformat(), left, right))
        if len(pieces) > MAX_WAIT_EXPORT_WORK:
            raise Unavailable("source_budget_exceeded")
        cursor = stop
    return pieces


def _wait_artifact_map(waits, events, claims, config, project_alias):
    tool_by_alias = {source["alias"]: source["tool"] for source in config["sources"]}
    owners = {}
    for row in [*events, *waits]:
        aliases = row["source_aliases"]
        tools = {tool_by_alias[alias] for alias in aliases if alias in tool_by_alias}
        if len(tools) == 1 and row.get("session_digest") is not None:
            owners.setdefault((next(iter(tools)), row["session_digest"]), set()).add(
                row.get("thread_key"))
    collisions = {identity for identity, threads in owners.items()
                  if None in threads or len(threads) != 1}
    grouped = {}
    for claim in claims:
        grouped.setdefault((claim["project_alias"], claim["tool"],
                            claim["session_digest"]), []).append(claim)
    overlaps = set()
    comparisons = 0
    for key, records in grouped.items():
        closed = [item for item in records if item["released_at"] is not None]
        comparisons += max(0, len(closed) - 1)
        if comparisons > MAX_WAIT_EXPORT_WORK:
            raise Unavailable("source_budget_exceeded")
        intervals = []
        for item in closed:
            start = datetime.fromisoformat(item["claimed_at"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(item["released_at"].replace("Z", "+00:00"))
            if start < end:
                intervals.append((start, end, item["claim_key"]))
        intervals.sort(key=lambda interval: (interval[0], interval[1], interval[2]))
        prior_max_end = None
        prior_max_key = None
        for start, end, claim_key in intervals:
            if prior_max_end is not None and start < prior_max_end:
                overlaps.update((prior_max_key, claim_key))
            if prior_max_end is None or end > prior_max_end:
                prior_max_end, prior_max_key = end, claim_key
    result = {}
    for wait in waits:
        if (wait["project_alias"] != project_alias
                or wait["project_association"] != "current_local_verified"
                or wait["ownership"] != "proven"
                or wait["classification"] != "pytest"
                or wait["started_at_ms"] is None):
            continue
        aliases = wait["source_aliases"]
        tools = {tool_by_alias[alias] for alias in aliases if alias in tool_by_alias}
        if len(tools) != 1:
            continue
        tool = next(iter(tools))
        if (tool, wait["session_digest"]) in collisions:
            continue
        start, end = _wait_datetime(wait["started_at_ms"]), _wait_datetime(
            wait["completed_at_ms"])
        eligible = []
        records = grouped.get((project_alias, tool, wait["session_digest"]), [])
        if any(item["released_at"] is None
               and datetime.fromisoformat(item["claimed_at"].replace("Z", "+00:00")) <= end
               for item in records):
            continue
        for claim in records:
            comparisons += 1
            if comparisons > MAX_WAIT_EXPORT_WORK:
                raise Unavailable("source_budget_exceeded")
            if (claim["claim_key"] in overlaps or claim["confidence"] != "reliable"
                    or claim["released_at"] is None or len(claim["targets"]) != 1):
                continue
            claim_start = datetime.fromisoformat(claim["claimed_at"].replace("Z", "+00:00"))
            claim_end = datetime.fromisoformat(claim["released_at"].replace("Z", "+00:00"))
            if claim_start <= start and end <= claim_end:
                eligible.append(claim)
        if len(eligible) == 1:
            result[wait["wait_key"]] = eligible[0]["targets"][0]
    return result


def _wait_export(waits, events, claims, config, project_alias):
    selected = [row for row in waits if (
        row["project_alias"] == project_alias
        and row["project_association"] == "current_local_verified"
        and row["ownership"] == "proven" and row["classification"] == "pytest"
        and row["started_at_ms"] is not None)]
    artifact_map = _wait_artifact_map(waits, events, claims, config, project_alias)
    by_day = {}
    by_artifact = {}
    full_intervals = []
    total_execution = 0
    work = 0
    for wait in selected:
        start, end = wait["started_at_ms"], wait["completed_at_ms"]
        pieces = _split_wait_days(start, end)
        work += len(pieces)
        if work > MAX_WAIT_EXPORT_WORK:
            raise Unavailable("source_budget_exceeded")
        full_intervals.append((start, end))
        total_execution += end - start
        completion_day = _wait_datetime(end).date().isoformat()
        artifact = artifact_map.get(wait["wait_key"])
        by_day.setdefault(completion_day, {"intervals": [], "executions": 0,
                                           "execution_ms": 0})["executions"] += 1
        if artifact is not None:
            by_artifact.setdefault((completion_day, artifact), {
                "intervals": [], "executions": 0, "execution_ms": 0})["executions"] += 1
        for day, left, right in pieces:
            group = by_day.setdefault(day, {"intervals": [], "executions": 0,
                                            "execution_ms": 0})
            group["intervals"].append((left, right))
            group["execution_ms"] += right - left
            if artifact is not None:
                item = by_artifact.setdefault((day, artifact), {
                    "intervals": [], "executions": 0, "execution_ms": 0})
                item["intervals"].append((left, right))
                item["execution_ms"] += right - left
        if sum(len(group["intervals"]) for group in by_day.values()) > MAX_WAIT_OCCURRENCES:
            raise Unavailable("source_budget_exceeded")
    if selected:
        overall_union = union_test_intervals(full_intervals)
        if overall_union is None:
            raise Unavailable("source_budget_exceeded")
        try:
            total_execution = _counter(total_execution)
        except ValueError:
            raise Unavailable("source_budget_exceeded") from None
        observed = {"executions": len(selected), "execution_ms": total_execution,
                    "wall_wait_ms": overall_union["wall_wait_ms"]}
    else:
        observed = None
    day_rows = []
    for day in sorted(by_day):
        group = by_day[day]
        wall = union_test_intervals(group["intervals"]) if group["intervals"] else {
            "wall_wait_ms": 0}
        if wall is None:
            raise Unavailable("source_budget_exceeded")
        day_rows.append({"day": day, "executions": group["executions"],
                         "execution_ms": group["execution_ms"],
                         "wall_wait_ms": wall["wall_wait_ms"]})
    artifact_rows = []
    for (day, artifact), group in sorted(by_artifact.items()):
        wall = union_test_intervals(group["intervals"]) if group["intervals"] else {
            "wall_wait_ms": 0}
        if wall is None:
            raise Unavailable("source_budget_exceeded")
        artifact_rows.append({"day": day, "artifact": artifact,
                              "executions": group["executions"],
                              "execution_ms": group["execution_ms"],
                              "wall_wait_ms": wall["wall_wait_ms"]})
    if len(day_rows) + len(artifact_rows) > MAX_WAIT_OCCURRENCES:
        raise Unavailable("source_budget_exceeded")
    return {"coverage": "unknown", "observed": observed,
            "by_day": day_rows, "by_artifact": artifact_rows}


def _project_export(ledger, config, project_alias):
    """Build one sanitized project-only aggregate without filesystem access."""
    if isinstance(config, bytes):
        config = validate_config_bytes(config)
    elif isinstance(config, dict):
        try:
            config = validate_config_bytes(json.dumps(
                config, allow_nan=False).encode("utf-8"))
        except (TypeError, ValueError, UnicodeError, RecursionError,
                OverflowError):
            raise Unavailable("config_invalid") from None
    else:
        raise Unavailable("config_invalid")
    if not config["enabled"]:
        raise Unavailable("disabled")
    projects = [item for item in config["projects"] if item["alias"] == project_alias]
    if len(projects) != 1:
        raise Unavailable("project_path_unapproved")
    if isinstance(ledger, dict):
        try:
            encoded = (json.dumps(ledger, sort_keys=True, separators=(",", ":"),
                                  allow_nan=False) + "\n").encode("ascii")
        except (TypeError, ValueError, UnicodeError, OverflowError):
            raise Unavailable("ledger_invalid") from None
    elif isinstance(ledger, bytes):
        encoded = ledger
    else:
        raise Unavailable("ledger_invalid")
    verified_ledger = _load_ledger(encoded)
    if len(verified_ledger["events"]) > MAX_RETAINED_EVENTS:
        raise Unavailable("source_budget_exceeded")
    tool_by_alias = {source["alias"]: source["tool"] for source in config["sources"]}
    artifacts = {item["event_key"]: item["artifact"]
                 for item in verified_ledger["mappings"]}
    groups = {}
    for event in verified_ledger["events"]:
        if (event["project_alias"] != project_alias
                or event["project_association"] != "current_local_verified"
                or event["ownership"] != "proven"):
            continue
        tools = {tool_by_alias[alias] for alias in event["source_aliases"]
                 if alias in tool_by_alias}
        tool = next(iter(tools)) if len(tools) == 1 else None
        day = None
        week = None
        if event["time_coverage"] == "known" and event["observed_at"] is not None:
            observed = datetime.fromisoformat(
                event["observed_at"].replace("Z", "+00:00")).astimezone(timezone.utc).date()
            day = observed.isoformat()
            iso = observed.isocalendar()
            week = f"{iso.year}-W{iso.week:02d}"
        key = (week, day, artifacts.get(event["event_key"]), tool, event["model"],
               event["model_provenance"], event["effective_model"])
        group = groups.setdefault(key, {"events": [], "unknown": 0})
        group["events"].append(event)
        if any(value is None for value in event["kinds"].values()):
            group["unknown"] += 1
    aggregates = []
    for key, group in sorted(groups.items(), key=lambda item: tuple(
            "" if value is None else str(value) for value in item[0])):
        week, day, artifact, tool, model, provenance, effective = key
        kinds, reference = {}, {}
        for name in _EVENT_KIND_NAMES:
            values = [event["kinds"][name] for event in group["events"]]
            kinds[name] = None if any(value is None for value in values) else sum(values)
        weighted = [_weighted_reference_tokens(event) for event in group["events"]]
        for name in (*_EVENT_KIND_NAMES, "total"):
            values = [row[name] for row in weighted]
            reference[name] = (None if any(value is None for value in values)
                               else _fraction_text(sum(
                                   (Fraction(Decimal(value)) for value in values),
                                   Fraction(0))))
        aggregates.append({
            "week": week, "day": day, "artifact": artifact, "tool": tool,
            "model": model, "model_provenance": provenance,
            "effective_model": effective, "events": len(group["events"]),
            "unknown_events": group["unknown"], "kinds": kinds,
            "reference_tokens": reference,
        })
    for item in verified_ledger["daily"]:
        if item["project_alias"] != project_alias:
            continue
        iso = datetime.fromisoformat(item["day"]).date().isocalendar()
        aggregates.append({
            "week": f"{iso.year}-W{iso.week:02d}", "day": item["day"], "artifact": None,
            "tool": item["tool"], "model": item["model"],
            "model_provenance": item["model_provenance"],
            "effective_model": item["effective_model"], "events": item["events"],
            "unknown_events": item["unknown_events"], "kinds": dict(item["kinds"]),
            "reference_tokens": dict(item["reference_tokens"]),
        })
    aggregates.sort(key=lambda item: tuple("" if value is None else str(value) for value in (
        item["week"], item["day"], item["artifact"], item["tool"], item["model"],
        item["model_provenance"], item["effective_model"])))
    reasons = set(verified_ledger["coverage"]["reasons"])
    reasons.add("global_completeness_unknown")
    result = {
        "schema": "cairn-meter-project/2",
        "project_alias": project_alias,
        "ratio_version": RATIO_VERSION,
        "aggregates": aggregates,
        "wait": _wait_export(verified_ledger["waits"], verified_ledger["events"],
                             verified_ledger["claims"], config, project_alias),
        "coverage": {"global": "unknown", "reasons": sorted(reasons)},
    }
    if len(json.dumps(result, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")) > MAX_LEDGER_BYTES:
        raise Unavailable("source_budget_exceeded")
    return result


def _project_export_bytes(ledger, config, project_alias):
    output = _project_export(ledger, config, project_alias)
    payload = (json.dumps(output, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")
    if len(payload) > MAX_LEDGER_BYTES:
        raise Unavailable("source_budget_exceeded")
    return payload


def _current_report_project(config, current_directory):
    try:
        current = os.path.normcase(os.path.abspath(os.fspath(current_directory)))
    except (OSError, TypeError, ValueError):
        return None
    matches = [project for project in config["projects"]
               if os.path.normcase(os.path.abspath(project["path"])) == current]
    return matches[0] if len(matches) == 1 else None


def _fork_sequence_identity(item):
    """Fields that must be identical when copied history is independently retained."""
    return {key: item[key] for key in (
        "event_key", "owner_key", "session_key", "turn_key", "root_key",
        "counter_family_key", "ordinal", "parent_ordinal",
        "kinds", "turn_snapshot", "thread_snapshot", "context_key")}


def _fork_sequence_compare(item):
    identity = _fork_sequence_identity(item)
    identity.pop("ordinal")
    identity.pop("parent_ordinal")
    return identity


def _complete_vector(value):
    return (isinstance(value, dict) and set(value) == set(_EVENT_KIND_NAMES)
            and any(value[name] is not None for name in _EVENT_KIND_NAMES)
            and all(item is None or (type(item) is int and 0 <= item <= MAX_COUNTER)
                    for item in value.values()))


def _add_vectors(left, right):
    result = {name: (None if left[name] is None or right[name] is None
                     else left[name] + right[name]) for name in _EVENT_KIND_NAMES}
    if any(value is not None and value > MAX_COUNTER for value in result.values()):
        raise ValueError
    return result


def _dedupe_checkpoint_sequence(sequence):
    unique, seen = [], {}
    for item in sequence:
        prior = seen.get(item["event_key"])
        if prior is None:
            seen[item["event_key"]] = item
            unique.append(item)
        elif _fork_sequence_compare(prior) != _fork_sequence_compare(item):
            return None
    return unique


def _checkpoint_sequence_matches_direct(sequence):
    thread_total = {name: 0 for name in _EVENT_KIND_NAMES}
    turn_totals = {}
    try:
        for item in sequence:
            thread_total = _add_vectors(thread_total, item["kinds"])
            turn_total = turn_totals.setdefault(
                item["turn_key"], {name: 0 for name in _EVENT_KIND_NAMES})
            turn_total = _add_vectors(turn_total, item["kinds"])
            turn_totals[item["turn_key"]] = turn_total
            if item["thread_snapshot"] != thread_total or item["turn_snapshot"] != turn_total:
                return False
    except (KeyError, TypeError, ValueError):
        return False
    return bool(sequence)


def _verify_copied_forks(batches):
    """Verify only the pinned fully copied legacy subagent prefix contract."""
    verified, conflicts = [], set()
    for child_batch in batches:
        fork = child_batch.get("fork_evidence")
        if fork is None:
            continue
        lineage_key = _digest("codex-lineage", fork["child_key"])
        parent_batches = [
            batch for batch in batches
            if batch is not child_batch
            and batch.get("source_alias") in fork["source_aliases"]
            and batch.get("fork_evidence") is None
            and batch.get("source_header_valid")
            and batch.get("source_owner_key") == fork["parent_key"]
            and batch.get("source_session_key") == fork["session_key"]
            and batch.get("source_header_key") == fork["parent_header_key"]
        ]
        prefix_raw = fork["parent_prefix"]
        prefix = _dedupe_checkpoint_sequence(prefix_raw)
        child_raw = fork["child_sequence"]
        child = _dedupe_checkpoint_sequence(child_raw)
        if (fork["invalid"] or not fork["parent_header"] or not prefix or not child
                or fork["direct_record_count"] != len(prefix_raw) + len(child_raw)
                or fork["boundary_turn_key"] is None
                or any(item["ordinal"] >= fork["boundary_line"] for item in prefix)
                or any(item["ordinal"] <= fork["boundary_line"] for item in child)
                or any(not _complete_vector(item["kinds"])
                       or not _complete_vector(item["turn_snapshot"])
                       or not _complete_vector(item["thread_snapshot"])
                       for item in prefix + child)):
            if parent_batches:
                conflicts.add(lineage_key)
            continue
        candidates = []
        for parent_batch in parent_batches:
            if set(parent_batch.get("issues", ())) & {
                    "invalid_record", "snapshot_conflict", "legacy_checkpoint_unreconciled",
                    "unsupported_record", "unsupported_or_invalid_session_metadata",
                    "conflicting_session_metadata", "conflicting_turn_context"}:
                continue
            raw_sequence = [item for item in parent_batch.get("checkpoint_sequence", [])
                        if item["owner_key"] == fork["parent_key"]
                        and item["session_key"] == fork["session_key"]
                        and item["role"] == "direct"]
            sequence = _dedupe_checkpoint_sequence(raw_sequence)
            if (sequence is None
                    or parent_batch.get("direct_record_count") != len(raw_sequence)
                    or not _checkpoint_sequence_matches_direct(sequence)
                    or len(sequence) < len(prefix)):
                continue
            if ([_fork_sequence_compare(item) for item in sequence[:len(prefix)]]
                    != [_fork_sequence_compare(item) for item in prefix]):
                continue
            proven_events = {event["event_key"] for event in parent_batch.get("events", [])
                             if event["ownership"] == "proven"}
            if not all(item["event_key"] in proven_events for item in prefix):
                continue
            candidates.append((parent_batch, sequence))
        if not candidates:
            if parent_batches:
                conflicts.add(lineage_key)
            continue
        baseline = prefix[-1]["thread_snapshot"]
        parent_root = prefix[-1]["root_key"]
        running = {name: 0 for name in _EVENT_KIND_NAMES}
        valid = all(item["root_key"] == parent_root for item in child)
        try:
            for item in child:
                if item["turn_key"] != fork["boundary_turn_key"] \
                        or item["root_key"] != parent_root:
                    valid = False
                running = _add_vectors(running, item["kinds"])
                if item["turn_snapshot"] != running:
                    valid = False
                expected_thread = _add_vectors(baseline, running)
                if item["thread_snapshot"] != expected_thread:
                    valid = False
        except (KeyError, TypeError, ValueError):
            valid = False
        if not valid:
            conflicts.add(lineage_key)
            continue
        parent_batch, parent_sequence = candidates[0]
        child_keys = {item["event_key"] for item in child}
        for event in child_batch.get("events", []):
            if event["event_key"] in child_keys:
                event["ownership"] = "proven"
                event["lineage_key"] = lineage_key
                event["reasons"] = sorted(set(event["reasons"]) - {"conflicting_binding"})
        verified.append({
            "contract": fork["contract"],
            "source_alias": child_batch["source_alias"],
            "child_file_key": child_batch["file_key"],
            "child_dev": child_batch["cursor"]["dev"],
            "child_ino": child_batch["cursor"]["ino"],
            "child_generation": child_batch["cursor"]["generation"],
            "child_offset": child_batch["cursor"]["offset"],
            "child_line": child_batch["cursor"]["line"],
            "parent_cursors": sorted(({
                "file_key": batch["file_key"],
                "dev": batch["cursor"]["dev"],
                "ino": batch["cursor"]["ino"],
                "generation": batch["cursor"]["generation"],
                "offset": batch["cursor"]["offset"],
                "line": batch["cursor"]["line"],
            } for batch, _sequence in candidates), key=lambda item: item["file_key"]),
            "parent_key": fork["parent_key"], "child_key": fork["child_key"],
            "session_key": fork["session_key"], "root_key": parent_root,
            "parent_header_key": fork["parent_header_key"],
            "counter_family_key": _digest(
                "codex-counter-family", fork["session_key"], parent_root),
            "boundary_turn_key": fork["boundary_turn_key"],
            "boundary_line": fork["boundary_line"],
            "direct_record_count": len(prefix) + len(child),
            "parent_prefix": [
                {**_fork_sequence_identity(item),
                 "parent_ordinal": parent_item["ordinal"]}
                for item, parent_item in zip(prefix, parent_sequence[:len(prefix)])
            ],
            "parent_terminal": {
                **_fork_sequence_identity(prefix[-1]),
                "parent_ordinal": parent_sequence[len(prefix) - 1]["ordinal"],
            },
            "child_sequence": [_fork_sequence_identity(item) for item in child],
            "child_event_keys": sorted(child_keys),
        })
    return verified, conflicts


def _start_bookmark(source, relative, enumerated, file_key):
    """Where a log ends now: its last complete line, and the source owner.

    Nothing before the returned offset is ever counted. Returns the cursor and
    the bytes read.
    """
    tail = _iter_approved_lines(
        source["root"], relative, 2 * MAX_LINE + 2, piece=True, tail=True)
    for _unused in tail:
        pass
    if tail.terminal_reason is not None:
        raise Unavailable(tail.terminal_reason)
    owner_key = None
    used = tail.bytes_read
    if source["tool"] == "codex":
        first = _iter_approved_lines(
            source["root"], relative, MAX_LINE + 1, piece=True, max_lines=1)
        owner_key = read_records("codex", first)["source_owner_key"]
        if first.terminal_reason is not None:
            raise Unavailable(first.terminal_reason)
        used += first.bytes_read
    return {
        "source_alias": source["alias"], "file_key": file_key,
        "dev": tail.open_identity["dev"], "ino": tail.open_identity["ino"],
        "generation": 1, "offset": tail.tail_offset, "line": 0,
        "size": tail.open_identity["size"],
        "mtime_ns": tail.open_identity["mtime_ns"],
        "ctime_ns": tail.open_identity["ctime_ns"],
        "digest": tail.tail_digest, "owner_key": owner_key,
    }, used


def _counts_after_start(event, started_at, horizon_day):
    """A fresh read counts an event of unknown time, or one that is not before the
    start and whose UTC day is not before `horizon_day`."""
    if event["time_coverage"] != "known" or event["observed_at"] is None:
        return True
    observed = datetime.fromisoformat(event["observed_at"].replace("Z", "+00:00"))
    return (observed >= started_at
            and observed.astimezone(timezone.utc).date() >= horizon_day)


def _piece_cursor(source, file_key, stream, old, resumed, *, whole_log=False,
                  owner_key=None):
    """The cursor a piece read leaves behind (plan D5).

    A whole-log re-read starts at byte 0, so its `line` is the lines consumed.
    """
    consumed = stream.complete_lines
    if consumed > 0:
        offset, digest = stream.end_offset, stream.tail_digest
        line = (old["line"] if resumed and not whole_log else 0) + consumed
    elif resumed:
        offset, digest, line = old["offset"], old["digest"], old["line"]
    else:
        offset, digest, line = 0, None, 0
    if resumed:
        generation = old["generation"]
    else:
        generation = 1 if old is None else old["generation"] + 1
    identity = stream.open_identity
    return {
        "source_alias": source["alias"], "file_key": file_key,
        "dev": identity["dev"], "ino": identity["ino"],
        "generation": generation, "offset": offset, "line": line,
        "size": stream.end_offset if stream.limit_stop else identity["size"],
        "mtime_ns": identity["mtime_ns"], "ctime_ns": identity["ctime_ns"],
        "digest": digest, "owner_key": owner_key,
    }


def _read_codex_log(source, relative, config, budget, *, resume=None):
    """Read one whole-log source from byte 0, or do not count it (plan D6, D12).

    With `resume` the stream checks the saved bookmark on the way through.
    Returns the stream and the batch.
    """
    stream = _iter_approved_lines(
        source["root"], relative, budget, piece=True, max_lines=MAX_REREAD_LINES,
        resume=resume, reread=resume is not None)
    batch = read_records("codex", stream, config=config,
                         source_aliases=[source["alias"]], source_root=source["root"])
    return stream, batch


def _codex_limit_reason(stream, budget):
    """Why a whole-log read stopped: permanently too large or temporarily over budget."""
    if budget >= MAX_REREAD_BYTES or stream.complete_lines >= MAX_REREAD_LINES:
        return "source_too_large"
    return "catching_up"


def _kept_events(batch):
    """The events of a batch that may count: all, or those a re-read made after
    its bookmark (the batch holds every event of the log, plan D8)."""
    first = batch.get("first_counted", 1)
    if first <= 1:
        return list(batch["events"])
    last_line = batch["event_last_line"]
    return [event for event in batch["events"]
            if last_line[event["event_key"]] >= first]


def _is_fork_parent(batch, fork):
    """The parent test of `_verify_copied_forks`, for one batch and one child."""
    return (batch.get("source_alias") in fork["source_aliases"]
            and batch.get("fork_evidence") is None
            and bool(batch.get("source_header_valid"))
            and batch.get("source_owner_key") == fork["parent_key"]
            and batch.get("source_session_key") == fork["session_key"]
            and batch.get("source_header_key") == fork["parent_header_key"])


def _read_fork_parents(source, config, files, previous, source_batches, spent):
    """Read, as context only, the parents of this source's fork children when no
    log of the run supplies them (plan D8).

    A parent is a prior cursor of the same alias whose owner is the child's
    parent, whose log is in this run's enumeration and was not read this run; at
    most 4 per child. Returns the context batches, the file keys of children to
    drop (a parent the run cannot pay for), and the bytes read.
    """
    located = {_digest("cursor", source["alias"], relative): (relative, enumerated)
               for relative, enumerated in files}
    read_keys = {batch["file_key"] for batch in source_batches}
    contexts, dropped, used = [], set(), 0
    for child in sorted((batch for batch in source_batches
                         if batch.get("fork_evidence") is not None),
                        key=lambda batch: batch["file_key"]):
        fork = child["fork_evidence"]
        if any(_is_fork_parent(batch, fork) for batch in source_batches + contexts):
            continue
        wanted = sorted((cursor for cursor in previous.values()
                         if cursor["source_alias"] == source["alias"]
                         and cursor["owner_key"] == fork["parent_key"]
                         and cursor["file_key"] in located
                         and cursor["file_key"] not in read_keys),
                        key=lambda cursor: cursor["file_key"])[:4]
        short = False
        for cursor in wanted:
            relative, enumerated = located[cursor["file_key"]]
            left = MAX_RUN_READ_BYTES - spent - used
            if enumerated["size"] > min(MAX_REREAD_BYTES, MAX_RUN_READ_BYTES):
                continue                      # too large: the child stays unverified
            if enumerated["size"] > left:
                short = True
                continue
            budget = min(MAX_REREAD_BYTES, left)
            stream, parent = _read_codex_log(source, relative, config, budget)
            used += stream.bytes_read
            if stream.terminal_reason == "source_read_unavailable":
                short = True          # a parent that cannot be read leaves the child for later
                continue
            if stream.terminal_reason is not None:
                raise Unavailable(stream.terminal_reason)
            read_keys.add(cursor["file_key"])
            if stream.limit_stop:
                short = short or _codex_limit_reason(stream, budget) == "catching_up"
                continue
            if ("source_budget_exceeded" in parent["issues"]
                    or parent.get("fork_evidence") is not None):
                continue
            parent["source_alias"] = source["alias"]
            parent["file_key"] = cursor["file_key"]
            parent["cursor"] = dict(cursor)
            parent["context_only"] = True
            contexts.append(parent)
        if short:
            dropped.add(child["file_key"])
    return contexts, dropped, used


def _scan_approved_sources(config, prior_cursors, *, starts, now, fold_horizon=None,
                           agent_runs=None):
    previous = {cursor["file_key"]: cursor for cursor in prior_cursors}
    start_rows = {row["source_alias"]: row["started_at"] for row in starts}
    had_start = set(start_rows)
    now_stamp = _start_stamp(now)
    batches, cursors, reasons = [], {}, set()
    context_batches = []          # parents read only to verify a fork; never counted
    total_entries = total_files = total_bytes = run_events = 0
    attribution_bytes = attribution_entries = 0
    horizon_day = now.astimezone(timezone.utc).date() - timedelta(days=FOLD_AFTER_DAYS)
    if fold_horizon is not None:
        horizon_day = max(horizon_day, _parse_fold_day(fold_horizon))
    aliases_seen = set()
    excluded = [source["root"] for source in config["sources"]]
    excluded.extend(project["path"] for project in config["projects"])
    for source in sorted(config["sources"], key=lambda item: item["alias"]):
        if source["alias"] in aliases_seen:
            raise Unavailable
        aliases_seen.add(source["alias"])
        start_rows.setdefault(source["alias"], now_stamp)
        started_at = _parse_start(start_rows[source["alias"]])
        started_ns = int(started_at.timestamp()) * 1_000_000_000
        conversations = {}        # each conversation's attribution, once per refresh
        if source["tool"] == "antigravity":  # vendor-ok: its own bounded walker
            # Its entries and files charge only the attribution caps, so a large
            # folder here can never fail the refresh for another source.
            files, entries, waiting = _enumerate_antigravity(source["root"])
            attribution_entries += entries
            if waiting:
                reasons.add("catching_up")
        else:
            files, entries = _enumerate_jsonl(source["root"])
            total_entries += entries
            total_files += len(files)
            if total_entries > MAX_REFRESH_ENTRIES or total_files > MAX_SOURCE_FILES:
                raise Unavailable("source_budget_exceeded")
        first_batch = len(batches)
        for relative, enumerated in files:
            if enumerated["size"] < 0:
                raise Unavailable
            file_key = _digest("cursor", source["alias"], relative)
            old = previous.get(file_key)
            if old is not None and all(
                    old[name] == enumerated[name]
                    for name in ("dev", "ino", "size", "mtime_ns", "ctime_ns")):
                cursors[file_key] = dict(old)
                continue
            remaining = MAX_RUN_READ_BYTES - total_bytes
            if remaining <= 0 or run_events >= MAX_RUN_EVENTS:
                reasons.add("catching_up")
                if old is not None:
                    cursors[file_key] = dict(old)
                continue
            if (old is None
                    and (source["alias"] not in had_start
                         or enumerated["mtime_ns"] < started_ns)):
                bookmark_reservation = (2 * MAX_LINE + 2
                                        + (MAX_LINE + 1 if source["tool"] == "codex"
                                           else 0))
                if remaining < bookmark_reservation:
                    reasons.add("catching_up")
                    continue
                try:
                    cursors[file_key], used = _start_bookmark(
                        source, relative, enumerated, file_key)
                except Unavailable as exc:
                    if exc.reason != "source_read_unavailable":
                        raise
                    reasons.add("catching_up")       # left for the next run
                    continue
                total_bytes += used
                continue
            if source["tool"] == "codex":
                # Whole or not at all: a log over a limit is skipped for good
                # (source_too_large); one the rest of the run cannot pay for waits.
                if enumerated["size"] > min(MAX_REREAD_BYTES, MAX_RUN_READ_BYTES):
                    reasons.add("source_too_large")
                    if old is not None:
                        cursors[file_key] = dict(old)
                    continue
                if enumerated["size"] > remaining:
                    reasons.add("catching_up")
                    if old is not None:
                        cursors[file_key] = dict(old)
                    continue
                resumed = old is not None
                resume = None if old is None else {
                    "dev": old["dev"], "ino": old["ino"],
                    "offset": old["offset"], "digest": old["digest"]}
                while True:
                    budget = min(MAX_REREAD_BYTES, MAX_RUN_READ_BYTES - total_bytes)
                    stream, batch = _read_codex_log(
                        source, relative, config, budget, resume=resume)
                    total_bytes += stream.bytes_read
                    if stream.terminal_reason == "source_read_unavailable":
                        break
                    if stream.terminal_reason is not None:
                        raise Unavailable(stream.terminal_reason)
                    if stream.resume_failure in {"file_replaced", "cursor_past_end"}:
                        # Decided before any line was read: read the log afresh.
                        reasons.add("resume_failed_" + stream.resume_failure)
                        resumed, resume = False, None
                        continue
                    break
                if stream.terminal_reason is not None:
                    reasons.add("catching_up")       # unreadable: left for the next run
                    if old is not None:
                        cursors[file_key] = dict(old)
                    continue
                skipped = None
                if stream.limit_stop:
                    skipped = _codex_limit_reason(stream, budget)
                elif "source_budget_exceeded" in batch["issues"]:
                    skipped = "source_too_large"
                if skipped is not None:
                    reasons.add(skipped)
                    if old is not None:
                        cursors[file_key] = dict(old)
                    continue
                if stream.resume_failure is not None:
                    # The batch just read is a fresh read of the whole log.
                    reasons.add("resume_failed_" + stream.resume_failure)
                    resumed = False
                if resumed:
                    batch["first_counted"] = stream.checkpoint_line + 1
                cursors[file_key] = _piece_cursor(
                    source, file_key, stream, old, resumed, whole_log=True,
                    owner_key=batch["source_owner_key"])
            else:
                attribution = None
                if source["tool"] == "antigravity":  # vendor-ok: one search per conversation
                    conversation = relative.split("/")[1]
                    decided = conversations.get(conversation)
                    if decided is None:
                        if (attribution_bytes + MAX_ATTRIBUTION_BYTES > MAX_ATTRIBUTION_RUN_BYTES
                                or total_bytes + MAX_ATTRIBUTION_BYTES > MAX_RUN_READ_BYTES
                                or attribution_entries + MAX_ATTRIBUTION_ENTRIES
                                > MAX_ATTRIBUTION_RUN_ENTRIES):
                            decided = "wait"
                        else:
                            named, unnamed, searched, listed = _conversation_project(
                                source["root"], conversation, config["projects"])
                            attribution_bytes += searched
                            total_bytes += searched
                            attribution_entries += listed
                            decided = (named, unnamed)
                        conversations[conversation] = decided
                    if decided == "wait":
                        reasons.add("catching_up")       # left for the next run
                        if old is not None:
                            cursors[file_key] = dict(old)
                        continue
                    attribution = {conversation: decided}
                resumed = old is not None
                resume = None if old is None else {
                    "dev": old["dev"], "ino": old["ino"],
                    "offset": old["offset"], "digest": old["digest"]}
                while True:
                    stream = _iter_approved_lines(
                        source["root"], relative,
                        min(MAX_BATCH_BYTES, MAX_RUN_READ_BYTES - total_bytes),
                        piece=True, resume=resume)
                    batch = read_records(source["tool"], stream, config=config,
                                         source_aliases=[source["alias"]],
                                         source_root=source["root"],
                                         attribution=attribution)
                    total_bytes += stream.bytes_read
                    if stream.terminal_reason == "source_read_unavailable":
                        break
                    if stream.terminal_reason is not None:
                        raise Unavailable(stream.terminal_reason)
                    if stream.resume_failure is None:
                        break
                    reasons.add("resume_failed_" + stream.resume_failure)
                    resumed, resume = False, None
                    if total_bytes >= MAX_RUN_READ_BYTES:
                        break
                if stream.terminal_reason is not None:
                    reasons.add("catching_up")       # unreadable: left for the next run
                    if old is not None:
                        cursors[file_key] = dict(old)
                    continue
                if stream.resume_failure is not None:
                    reasons.add("catching_up")
                    cursors[file_key] = dict(old)
                    continue
                cursors[file_key] = _piece_cursor(
                    source, file_key, stream, old, resumed)
                if stream.limit_stop:
                    reasons.add("catching_up")
            run_events += len(_kept_events(batch))
            batch["source_alias"] = source["alias"]
            batch["file_key"] = file_key
            batch["cursor"] = dict(cursors[file_key])
            if not resumed or source["tool"] == "antigravity":  # vendor-ok: copies keep their original time
                batch["started_at"] = started_at
            batches.append(batch)
            if agent_runs is not None:
                _gather_agent_runs(agent_runs, batch)
        if source["tool"] == "codex":
            parents, dropped, used = _read_fork_parents(
                source, config, files, previous, batches[first_batch:],
                total_bytes)
            total_bytes += used
            context_batches.extend(parents)
            if dropped:
                # A child is never counted unverified for lack of budget.
                reasons.add("catching_up")
                batches[first_batch:] = [
                    batch for batch in batches[first_batch:]
                    if batch["file_key"] not in dropped]
                for file_key in dropped:
                    if file_key in previous:
                        cursors[file_key] = dict(previous[file_key])
                    else:
                        del cursors[file_key]
    for batch in batches:
        reasons.update(batch["issues"])
    verified_forks, fork_conflicts = _verify_copied_forks(batches + context_batches)
    verified_lineages = {
        _digest("codex-lineage", proof["child_key"])
        for proof in verified_forks
    }
    if any(
        batch.get("fork_evidence") is not None
        and _digest("codex-lineage", batch["fork_evidence"]["child_key"])
        not in verified_lineages | fork_conflicts
        for batch in batches
    ):
        reasons.add("fork_parent_unavailable")
    for batch in batches:
        fork = batch.get("fork_evidence")
        if fork is None:
            continue
        lineage_key = _digest("codex-lineage", fork["child_key"])
        if lineage_key in verified_lineages:
            continue
        child_event_keys = {item["event_key"] for item in fork["child_sequence"]}
        for event in batch.get("events", []):
            if event["event_key"] in child_event_keys:
                event["ownership"] = "unknown"
                event["session_digest"] = None
                event["project_alias"] = None
                event["project_association"] = "unknown"
                event["lineage_key"] = None
                event["reasons"] = sorted(set(event["reasons"])
                                          | {"conflicting_binding"})
    for batch in batches:
        # Counting is decided only now, after every fork was verified on whole batches.
        kept = _kept_events(batch)
        if "started_at" in batch:
            kept = [event for event in kept
                    if _counts_after_start(event, batch["started_at"], horizon_day)]
        batch["events"] = kept
    wait_rows = []
    independently_owned_waits = {
        candidate["wait_key"]
        for batch in batches + context_batches
        for candidate in batch.get("wait_candidates", ())
        if not candidate.get("_fork_parent_copy") and candidate["ownership"] == "proven"
    }
    for batch in batches:
        cursor = batch["cursor"]
        first_counted = batch.get("first_counted", 1)
        started_ms = (int(batch["started_at"].timestamp() * 1000)
                      if "started_at" in batch else None)
        for candidate in batch.get("wait_candidates", ()):
            if candidate["_line_ordinal"] < first_counted:
                continue
            if (started_ms is not None and candidate["started_at_ms"] is not None
                    and candidate["started_at_ms"] < started_ms):
                continue
            row = {key: value for key, value in candidate.items()
                   if not key.startswith("_")}
            line = candidate.get("_line_ordinal")
            row["occurrences"] = [{
                "file_key": batch["file_key"],
                "generation": cursor["generation"],
                "line": line,
            }]
            lineage_key = row["lineage_key"]
            if candidate.get("_fork_parent_copy"):
                if row["wait_key"] in independently_owned_waits:
                    continue
                for field in ("thread_key", "session_key", "session_digest", "turn_key",
                              "root_turn_key", "project_alias", "model"):
                    row[field] = None
                row["project_association"] = "unknown"
                row["ownership"] = "unknown"
                row["model_provenance"] = "unknown"
                row["reasons"] = sorted(set(row["reasons"])
                                         | {"conflicting_binding"})
            if lineage_key is not None:
                matching_proof = next((proof for proof in verified_forks
                                       if proof["source_alias"] == batch["source_alias"]
                                       and proof["child_file_key"] == batch["file_key"]
                                       and any(item["owner_key"] == candidate["thread_key"]
                                               and item["session_key"] == candidate["session_key"]
                                               and item["turn_key"] == candidate["turn_key"]
                                               and item["root_key"] == candidate["root_turn_key"]
                                               for item in proof["child_sequence"])), None)
                if matching_proof is not None:
                    row["ownership"] = "proven"
                    candidate_project = candidate.get("_candidate_project_alias")
                    if candidate_project is not None:
                        row["project_alias"] = candidate_project
                        row["project_association"] = "current_local_verified"
                    row["reasons"] = sorted(set(row["reasons"])
                                             - {"conflicting_binding"})
                else:
                    for field in ("thread_key", "session_key", "session_digest",
                                  "turn_key", "root_turn_key", "lineage_key",
                                  "project_alias", "model"):
                        row[field] = None
                    row["project_association"] = "unknown"
                    row["ownership"] = "unknown"
                    row["model_provenance"] = "unknown"
                    row["reasons"] = sorted(set(row["reasons"])
                                             | {"conflicting_binding"})
            wait_rows.append(row)
    if len(wait_rows) > MAX_NORMALIZED_EVENTS:
        raise Unavailable("source_budget_exceeded")
    wait_rows = _merge_wait_rows([], wait_rows)
    incoming = _merge_event_batches(batches)
    if len(incoming) > MAX_RUN_EVENTS + MAX_NORMALIZED_EVENTS:
        raise Unavailable
    return (incoming, sorted(cursors.values(), key=lambda item: item["file_key"]),
            reasons, verified_forks, fork_conflicts, wait_rows,
            [{"source_alias": alias, "started_at": start_rows[alias]}
             for alias in sorted(start_rows)])


def _build_mappings(events, claims, config):
    tool_by_alias = {source["alias"]: source["tool"] for source in config["sources"]}
    owners = {}
    for event in events:
        tools = {tool_by_alias[alias] for alias in event["source_aliases"]
                 if alias in tool_by_alias}
        if len(tools) != 1 or event["session_digest"] is None:
            continue
        tool = next(iter(tools))
        owners.setdefault((tool, event["session_digest"]), set()).add(event["thread_key"])
    collisions = {key for key, threads in owners.items() if len(threads) != 1}
    grouped = {}
    for claim in claims:
        key = (claim["project_alias"], claim["tool"], claim["session_digest"])
        grouped.setdefault(key, []).append(claim)
    overlap = set()
    for key, records in grouped.items():
        intervals = [record for record in records if record["released_at"] is not None]
        for index, left in enumerate(intervals):
            left_start = datetime.fromisoformat(left["claimed_at"].replace("Z", "+00:00"))
            left_end = datetime.fromisoformat(left["released_at"].replace("Z", "+00:00"))
            for right in intervals[index + 1:]:
                right_start = datetime.fromisoformat(right["claimed_at"].replace("Z", "+00:00"))
                right_end = datetime.fromisoformat(right["released_at"].replace("Z", "+00:00"))
                if max(left_start, right_start) < min(left_end, right_end):
                    overlap.add(left["claim_key"])
                    overlap.add(right["claim_key"])
    mappings = []
    for event in events:
        if (event["project_association"] != "current_local_verified"
                or event["ownership"] != "proven" or event["time_coverage"] != "known"
                or event["session_digest"] is None or event["thread_key"] is None):
            continue
        tools = {tool_by_alias[alias] for alias in event["source_aliases"]
                 if alias in tool_by_alias}
        if len(tools) != 1:
            continue
        tool = next(iter(tools))
        identity = (tool, event["session_digest"])
        if identity in collisions:
            continue
        instant = datetime.fromisoformat(event["observed_at"].replace("Z", "+00:00"))
        candidates = []
        same_identity = grouped.get((event["project_alias"], tool,
                                     event["session_digest"]), [])
        open_claim = any(
            claim["released_at"] is None
            and datetime.fromisoformat(claim["claimed_at"].replace("Z", "+00:00")) <= instant
            for claim in same_identity)
        if open_claim:
            continue
        for claim in same_identity:
            if (claim["claim_key"] in overlap or claim["confidence"] != "reliable"
                    or claim["released_at"] is None or len(claim["targets"]) != 1):
                continue
            start = datetime.fromisoformat(claim["claimed_at"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(claim["released_at"].replace("Z", "+00:00"))
            if start <= instant < end:
                candidates.append(claim)
        if len(candidates) == 1:
            claim = candidates[0]
            mappings.append({"event_key": event["event_key"],
                             "claim_key": claim["claim_key"],
                             "artifact": claim["targets"][0],
                             "confidence": "reliable"})
    return sorted(mappings, key=lambda item: item["event_key"])


def _new_ledger(prior, config, incoming_events, incoming_waits, cursors, incoming_claims,
                project_remotes, capture_status, scan_reasons, verified_forks,
                fork_conflicts, starts=None, now=None, agent_runs=None):
    starts = prior["starts"] if starts is None else starts
    now = _now_utc() if now is None else now
    if agent_runs is None:
        incoming_runs = _empty_agent_runs()
    else:
        incoming_runs = {
            "transcripts": [{"session_key": session_key, "agent_key": agent_key}
                            for session_key, agent_key in sorted(agent_runs["transcripts"])],
            "summaries": [{"session_key": session_key, "agent_key": agent_key}
                          for session_key, agent_key in sorted(agent_runs["summaries"])],
            "unclassified": agent_runs["unclassified"]}
    runs = _merge_agent_runs(prior["agent_runs"], incoming_runs)
    events = _merge_events(prior["events"], incoming_events)
    waits = _merge_wait_rows(prior["waits"], incoming_waits)
    old_remotes = {item["alias"]: item["remote"] for item in prior["project_remotes"]}
    current_remotes = {item["alias"]: item["remote"] for item in project_remotes}
    for event in events:
        alias = event["project_alias"]
        if alias is None or event["project_association"] != "current_local_verified":
            continue
        if alias not in current_remotes:
            event["project_alias"] = None
            event["project_association"] = "unknown"
            event["reasons"] = sorted(set(event["reasons"])
                                      | {"project_path_unapproved"})
        elif alias in old_remotes and old_remotes[alias] != current_remotes[alias]:
            event["project_alias"] = None
            event["project_association"] = "unknown"
            event["reasons"] = sorted(set(event["reasons"])
                                      | {"project_remote_mismatch"})
    for wait in waits:
        alias = wait["project_alias"]
        if alias is None or wait["project_association"] != "current_local_verified":
            continue
        if alias not in current_remotes:
            wait["project_alias"] = None
            wait["project_association"] = "unknown"
            wait["reasons"] = sorted(set(wait["reasons"])
                                     | {"project_path_unapproved"})
        elif alias in old_remotes and old_remotes[alias] != current_remotes[alias]:
            wait["project_alias"] = None
            wait["project_association"] = "unknown"
            wait["reasons"] = sorted(set(wait["reasons"])
                                     | {"project_remote_mismatch"})
    daily = []
    for item in prior["daily"]:
        alias = item["project_alias"]
        if alias is not None and (alias not in current_remotes or (
                alias in old_remotes and old_remotes[alias] != current_remotes[alias])):
            item = {**item, "project_alias": None}
        daily.append(item)
    daily = _merge_rows(daily)
    claims = _merge_claim_history(prior["claims"], incoming_claims)
    lineages = _merge_lineage_history(prior["lineages"], verified_forks, fork_conflicts)
    conflicting_children = {
        proof["child_key"]
        for lineage in lineages if lineage["state"] == "conflicting"
        for proof in lineage["proofs"]
    }
    for event in events:
        if event["thread_key"] in conflicting_children:
            event["ownership"] = "unknown"
            event["project_alias"] = None
            event["project_association"] = "unknown"
            event["session_digest"] = None
            event["reasons"] = sorted(set(event["reasons"]) | {"conflicting_binding"})
    for event in events:
        _merge_retained_event(event, _copy_event(event))
    conflicting_lineage_keys = {item["lineage_key"] for item in lineages
                                if item["state"] == "conflicting"}
    for wait in waits:
        if wait["lineage_key"] in conflicting_lineage_keys or (
                wait["thread_key"] in conflicting_children):
            for field in ("thread_key", "session_key", "session_digest", "turn_key",
                          "root_turn_key", "project_alias", "model"):
                wait[field] = None
            wait["project_association"] = "unknown"
            wait["ownership"] = "unknown"
            wait["model_provenance"] = "unknown"
            wait["reasons"] = sorted(set(wait["reasons"]) | {"conflicting_binding"})
    events, daily, fold_horizon = _fold_events(
        events, daily, config, prior["fold_horizon"], now, "catching_up" in scan_reasons)
    if len(events) > MAX_RETAINED_EVENTS:
        raise Unavailable("source_budget_exceeded")
    lineages = _drop_folded_lineages(lineages, events, waits)
    mappings = _build_mappings(events, claims, config)
    reasons = set(scan_reasons)
    if runs["summaries"] or runs["unclassified"] > 0:
        reasons.add("agent_runs_incomplete")
    if reasons & {"catching_up", "source_too_large"}:
        reasons.add("incomplete")
    reasons.update(status for status in capture_status if status != "captured")
    if fork_conflicts or any(item["state"] == "conflicting" for item in lineages):
        reasons.add("conflicting_binding")
    return {
        "schema": LEDGER_SCHEMA, "reader_version": READER_VERSION,
        "ratio_version": RATIO_VERSION, "ratio_index": _ratio_index_copy(),
        "events": events, "waits": waits, "claims": claims,
        "cursors": cursors, "mappings": mappings,
        "project_remotes": sorted(project_remotes, key=lambda item: item["alias"]),
        "aggregates": sorted([*_recompute_aggregates(events, config), *daily],
                             key=_aggregate_sort_key),
        "lineages": lineages,
        "starts": sorted(starts, key=lambda item: item["source_alias"]),
        "fold_horizon": fold_horizon, "daily": daily, "agent_runs": runs,
        "coverage": {"global": "unknown", "reasons": sorted(reasons)},
    }


def _refresh_ledger(home, *, report_current_directory=None):
    """Run one explicit refresh, optionally returning fresh usage bytes in memory."""
    area = token = None
    try:
        config = load_config(Path(home) / ".cairn" / "meter.json")
        if config is None:
            return {"status": "disabled", "reason": "config_missing"}
        if not config["enabled"]:
            return {"status": "disabled", "reason": "disabled"}
        report_project = (_current_report_project(config, report_current_directory)
                          if report_current_directory is not None else None)
        area = _meter_area(home)
        token = _take_lock(area)
        ledger_path = area / LEDGER_NAME
        old_raw = (_read_limited(ledger_path, MAX_LEDGER_BYTES, "ledger_invalid")
                   if ledger_path.exists() else None)
        now = _now_utc()
        prior = _load_ledger(old_raw, now)
        runs = {"transcripts": set(), "summaries": set(), "unclassified": 0}
        (incoming_events, cursors, scan_reasons, verified_forks, fork_conflicts,
         incoming_waits, starts) = _scan_approved_sources(
            config, prior["cursors"], starts=prior["starts"], now=now,
            fold_horizon=prior["fold_horizon"], agent_runs=runs)
        incoming_claims, project_remotes, capture_status = _capture_all_claims(config)
        candidate = _new_ledger(prior, config, incoming_events, incoming_waits, cursors,
                                incoming_claims, project_remotes,
                                capture_status, scan_reasons, verified_forks,
                                fork_conflicts, starts=starts, now=now, agent_runs=runs)
        result = _atomic_replace_ledger(area, candidate)
        current_aggregate = None
        for project in sorted(config["projects"], key=lambda item: item["alias"]):
            try:
                state = _write_summary(project, candidate, config)
            except Unavailable as exc:
                return {"status": "unavailable", "reason": exc.reason,
                        "coverage": "unknown"}
            if state != "written":
                return {"status": "unavailable", "reason": "project_export_unavailable",
                        "coverage": "unknown"}
            if report_project is not None and project["alias"] == report_project["alias"]:
                current_aggregate = _project_export_bytes(candidate, config,
                                                          project["alias"])
        partial_reason = ("catching_up" if "catching_up" in candidate["coverage"]["reasons"]
                          else "source_too_large" if "source_too_large" in
                          candidate["coverage"]["reasons"] else None)
        output = {"status": "partial" if partial_reason else result,
                  "reason": partial_reason or "none", "events": len(candidate["events"]),
                  "claims": len(candidate["claims"]), "coverage": "unknown"}
        if report_current_directory is not None:
            output["current_project_aggregate"] = current_aggregate
        return output
    except Unavailable as exc:
        return {"status": "unavailable", "reason": exc.reason,
                "coverage": "unknown"}
    except (OSError, ValueError, TypeError, OverflowError, KeyError):
        return {"status": "unavailable", "reason": "ledger_unavailable",
                "coverage": "unknown"}
    finally:
        if token is not None:
            _release_lock(area, token)


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


def _unsigned64(value):
    if type(value) is not int or not 0 <= value <= (1 << 64) - 1:
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
    if "cache_write_input_tokens" in data:
        write = _counter(data["cache_write_input_tokens"])
        if write != 0:
            # Its inclusion in input is not established by the pinned type alone.
            raise ValueError
    else:
        write = None
    return {
        "fresh_input": raw["input_tokens"] - raw["cached_input_tokens"],
        "cache_read": raw["cached_input_tokens"],
        "cache_write": None if write is None else 0,
        "output": raw["output_tokens"],
    }


def _codex_uuid(value):
    """Require the producer's canonical UUID spelling for ownership IDs."""
    value = _text(value)
    if str(uuid.UUID(value)) != value:
        raise ValueError
    return value


def _codex_header(payload):  # vendor-ok: validate the supported input protocol
    thread = _codex_uuid(payload["id"])
    session_value = payload["session_id"] if "session_id" in payload else thread
    session = _codex_uuid(session_value)
    attached = payload.get("attached_thread", False)
    if type(attached) is not bool or attached:
        raise ValueError
    fork_fields = ("forked_from_id", "parent_thread_id")
    forked = any(payload.get(field) is not None for field in fork_fields)
    if any(payload.get(field) is not None for field in (
            "forked_from_ordinal_exclusive", "history_base",
            "subagent_history_start_ordinal")):
        raise ValueError
    if forked:
        parent = _codex_uuid(payload["forked_from_id"])
        if (parent != _codex_uuid(payload["parent_thread_id"])
                or session != parent or thread == parent
                or payload.get("thread_source") != "subagent"
                or payload.get("history_mode") != "legacy"):
            raise ValueError
        source = payload.get("source")
        if source != {"subagent": {"thread_spawn": {
                "parent_thread_id": parent, "depth": 1}}}:
            raise ValueError
        return (thread, session), {
            "kind": "copied_legacy_subagent", "child": thread, "parent": parent,
            "session": session,
        }
    if (payload["source"] not in {"cli", "vscode", "exec", "mcp"}
            or payload.get("thread_source") not in {None, "user"}
            or payload.get("history_mode") not in {"legacy", "paginated"}):
        raise ValueError
    return (thread, session), None


def _codex_header_key(owner, payload):
    """Hash only the stable validated owner-protocol fields for copied-header comparison."""
    return _digest("codex-header", owner[0], owner[1], payload["source"],
                   payload.get("thread_source"),
                   payload.get("history_mode"),
                   payload.get("attached_thread", False),
                   payload.get("forked_from_id"),
                   payload.get("parent_thread_id"))


def _codex_context(payload, owner):  # vendor-ok: validate the supported input protocol
    turn = _text(payload["turn_id"])
    root_value = payload.get("root_turn_id")
    root = turn if root_value is None else _text(root_value)
    cwd = payload.get("cwd")
    if cwd is not None:
        cwd = _text(cwd)
        if os.name == "nt":
            try:
                _windows_absolute_parts(cwd)
            except Unavailable:
                raise ValueError from None
        elif (not cwd.startswith("/")
              or any(part in {".", ".."} for part in cwd.split("/"))):
            raise ValueError
    model = payload.get("model")
    if model is not None:
        model = _safe_alias(model)
    return {"turn": turn, "root": root, "cwd": cwd, "model": model,
            "owner": owner}


def _project_for_folder(cwd, projects):
    """Return the one configured project whose path holds `cwd` as text, or None.

    The folder is never opened, linked or resolved; it is compared as text.
    """
    if not isinstance(cwd, str):
        return None
    try:
        cwd = _text(cwd)
    except ValueError:
        return None
    if os.name == "nt":
        try:
            _windows_absolute_parts(cwd)
        except Unavailable:
            return None
        sep = "\\"
    else:
        if not cwd.startswith("/") or any(part in {".", ".."} for part in cwd.split("/")):
            return None
        sep = "/"
    containing = []
    for project in projects:
        path = project.get("path")
        if not isinstance(path, str):
            continue
        if cwd == path:
            containing.append(project)
            continue
        prefix = path if path.endswith(sep) else path + sep
        if cwd.startswith(prefix):
            rest = cwd[len(prefix):]
            if rest and all(rest.split(sep)):
                containing.append(project)
    return containing[0] if len(containing) == 1 else None


def _codex_identity(payload):  # vendor-ok: extract the supported input protocol
    thread = _codex_uuid(payload["thread_id"])
    session = _codex_uuid(payload["session_id"])
    turn = _text(payload["turn_id"])
    root = _text(payload["root_turn_id"])
    response = _text(payload["response_id"])
    return thread, session, turn, root, response


def _codex_direct(payload):  # vendor-ok: extract the supported input protocol
    thread, session, turn, root, response = _codex_identity(payload)
    kinds = _codex_usage(payload["usage"])
    return thread, session, turn, root, response, kinds


def _claude_usage(data):  # vendor-ok: normalize the supported input protocol
    kinds = {out: _counter(data[key]) for out, key in (
        ("fresh_input", "input_tokens"), ("output", "output_tokens"),
        ("cache_write", "cache_creation_input_tokens"),
        ("cache_read", "cache_read_input_tokens"),
    )}
    _claude_cache_ttl(data, kinds["cache_write"])
    return kinds


def _antigravity_usage(record):  # vendor-ok: normalize the supported input protocol
    """The kinds of one antigravity token record, or None when it holds neither token field.

    One field, or a number that is not a non-negative whole number (a boolean
    included), raises ValueError. Only input and output are stated: both cache
    kinds stay unknown (None, never 0).
    """
    names = ("input_tokens", "output_tokens")
    present = [name in record for name in names]
    if not any(present):
        return None
    if not all(present):
        raise ValueError
    kinds = _unknown_kinds()
    kinds["fresh_input"] = _counter(record["input_tokens"])
    kinds["output"] = _counter(record["output_tokens"])
    return kinds


def _antigravity_conversation_id(conversation, lines):  # vendor-ok: the conversation a log belongs to
    """The canonical conversation id of a batch, or None when there is no usable one.

    The `conversation` keyword (synthetic lines) wins; otherwise the id is the
    second part of the stream's relative path (`brain/<id>/...`).
    """
    value = conversation
    if value is None:
        relative = getattr(lines, "relative", None)
        if isinstance(relative, str):
            parts = PurePosixPath(relative).parts
            value = parts[1] if len(parts) >= 2 else None
    try:
        return _codex_uuid(value)
    except (ValueError, TypeError):
        return None


def _antigravity_attribution(entry):  # vendor-ok: one conversation's attribution
    """A conversation's attribution, `(project alias, None)` or `(None, reason)`; else ValueError."""
    if not isinstance(entry, tuple) or len(entry) != 2:
        raise ValueError
    alias, reason = entry
    if (alias is None) == (reason is None):
        raise ValueError
    if alias is not None:
        _safe_alias(alias)
    elif not isinstance(reason, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", reason):
        raise ValueError
    return alias, reason


def _claude_cache_ttl(data, cache_write=None):  # vendor-ok: retain supported input protocol detail
    if "cache_creation" not in data:
        return {"five_minute": None, "one_hour": None}
    ttl = data["cache_creation"]
    if (not isinstance(ttl, dict)
            or set(ttl) != {"ephemeral_5m_input_tokens", "ephemeral_1h_input_tokens"}):
        raise ValueError
    five = _counter(ttl["ephemeral_5m_input_tokens"])
    hour = _counter(ttl["ephemeral_1h_input_tokens"])
    if cache_write is not None and five + hour != cache_write:
        raise ValueError
    return {"five_minute": five, "one_hour": hour}


_EVENT_KIND_NAMES = ("fresh_input", "cache_read", "cache_write", "output")


def _unknown_kinds():
    return {name: None for name in _EVENT_KIND_NAMES}


def _fraction_text(value):
    if value is None:
        return None
    decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return format(decimal, "f")


def _weighted_reference_tokens(event):
    """Return hypothetical reference-token equivalents; never actual spend."""
    model = event["effective_model"]
    if model is None and event["model_provenance"] == "selected_context":
        model = event["model"]
    weights = _RATIO_INDEX["models"].get(model)
    if weights is None:
        return {name: None for name in (*_EVENT_KIND_NAMES, "total")}
    kinds = event["kinds"]
    level = weights
    long_level = weights.get("long_prompt")
    if long_level is not None:
        counts = [kinds["fresh_input"], kinds["cache_read"]]
        if long_level["cache_write_5m"] is not None:
            counts.append(kinds["cache_write"])
        if None in counts:
            return {name: None for name in (*_EVENT_KIND_NAMES, "total")}
        if sum(counts) > long_level["over_tokens"]:
            level = long_level
    components = {}
    for name in ("fresh_input", "cache_read", "output"):
        weight = level[name]
        count = kinds[name]
        components[name] = None if weight is None or count is None else (
            Fraction(*weight) * count)
    writes = kinds["cache_write"]
    if writes is None:
        components["cache_write"] = None
    elif writes == 0:
        components["cache_write"] = Fraction(0)
    else:
        ttl = event["cache_write_ttl"]
        if ttl["five_minute"] is None:
            components["cache_write"] = None
        else:
            short, long = level["cache_write_5m"], level["cache_write_1h"]
            if short is None or long is None:
                components["cache_write"] = None
            else:
                components["cache_write"] = (
                    Fraction(*short) * ttl["five_minute"]
                    + Fraction(*long) * ttl["one_hour"])
    total = (None if any(value is None for value in components.values())
             else sum(components.values(), Fraction(0)))
    return {name: _fraction_text(value) for name, value in
            {**components, "total": total}.items()}


def _short_session_digest(raw_id):
    """Match the existing intent session digest without importing its writer."""
    if not isinstance(raw_id, str) or not raw_id.strip():
        return None
    return hashlib.sha256(raw_id.strip().encode("utf-8")).hexdigest()[:8]


def _event_record(*, tool, event_key, aliases, thread, session=None, turn=None,
                  root=None, timestamp=None, time_known=False, kinds=None,
                  project_alias=None, project_state="unknown", ownership="unknown",
                  model=None, model_provenance="unknown", effective_model=None,
                  cache_write_ttl=None, session_digest=None, reasons=()):
    return {
        "event_key": event_key,
        "source_aliases": sorted(set(aliases)),
        "thread_key": _digest(tool, thread) if thread else None,
        "session_digest": session_digest,
        "session_key": _digest(tool, session) if session else None,
        "turn_key": _digest(tool, thread, turn) if thread and turn else None,
        "root_turn_key": _digest(tool, session, root) if session and root else None,
        "observed_at": timestamp,
        "time_coverage": "known" if time_known else "unknown",
        "kinds": dict(kinds) if kinds is not None else _unknown_kinds(),
        "cache_write_ttl": (dict(cache_write_ttl) if cache_write_ttl is not None
                            else {"five_minute": None, "one_hour": None}),
        "project_alias": project_alias,
        "project_association": project_state,
        "ownership": ownership,
        "model": model,
        "model_provenance": model_provenance,
        "effective_model": effective_model,
        "account": None,
        "lineage_key": None,
        "reasons": sorted(set(reasons)),
    }


def _merge_normalized_event(existing, incoming):
    """Merge copied responses without choosing between conflicts."""
    existing["source_aliases"] = sorted(set(existing["source_aliases"])
                                        | set(incoming["source_aliases"]))
    existing["reasons"] = sorted(set(existing["reasons"]) | set(incoming["reasons"]))
    if (existing["kinds"] != incoming["kinds"]
            or existing["cache_write_ttl"] != incoming["cache_write_ttl"]):
        existing["kinds"] = _unknown_kinds()
        existing["cache_write_ttl"] = {"five_minute": None, "one_hour": None}
        existing["reasons"] = sorted(set(existing["reasons"]) | {"conflicting_usage"})
    binding_fields = ("thread_key", "session_digest", "session_key", "turn_key", "root_turn_key",
                      "project_alias", "project_association", "ownership", "model",
                      "model_provenance", "effective_model")
    if any(existing[field] != incoming[field] for field in binding_fields):
        existing["thread_key"] = None
        existing["session_key"] = None
        existing["session_digest"] = None
        existing["turn_key"] = None
        existing["root_turn_key"] = None
        existing["project_alias"] = None
        existing["project_association"] = "unknown"
        existing["ownership"] = "unknown"
        existing["model"] = None
        existing["model_provenance"] = "unknown"
        existing["effective_model"] = None
        existing["reasons"] = sorted(set(existing["reasons"]) | {"conflicting_binding"})
    elif existing["lineage_key"] is None:
        existing["lineage_key"] = incoming["lineage_key"]
    elif (incoming["lineage_key"] is not None
          and existing["lineage_key"] != incoming["lineage_key"]):
        existing["reasons"] = sorted(set(existing["reasons"]) | {"conflicting_binding"})
    if existing["observed_at"] != incoming["observed_at"]:
        existing["observed_at"] = None
        existing["time_coverage"] = "unknown"
        existing["reasons"] = sorted(set(existing["reasons"]) | {"ambiguous_time"})


def _merge_event_batches(batches):
    """Deduplicate normalized events across files; never reconcile private history."""
    merged = {}
    for batch in batches:
        for event in batch.get("events", ()):
            if not isinstance(event, dict) or set(event) != {
                    "event_key", "source_aliases", "thread_key", "session_digest", "session_key", "turn_key",
                    "root_turn_key", "observed_at", "time_coverage", "kinds", "project_alias",
                    "cache_write_ttl", "project_association", "ownership", "model",
                    "model_provenance", "effective_model", "account",
                    "lineage_key", "reasons"}:
                raise ValueError("unsupported normalized event")
            key = event["event_key"]
            if key not in merged:
                merged[key] = {name: (value.copy() if isinstance(value, (dict, list)) else value)
                               for name, value in event.items()}
            else:
                _merge_normalized_event(merged[key], event)
    return list(merged.values())


def _usage_values(record):
    """Return every value stored under a `usage` key inside the record.

    Walks without recursion: a list is used as a stack over dict values and
    list items, so a deeply nested record cannot exhaust the call stack.
    """
    found = []
    pending = [record]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            if "usage" in item:
                found.append(item["usage"])
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
    return found


def _empty_agent_runs():
    return {"transcripts": [], "summaries": [], "unclassified": 0}


def _gather_agent_runs(gathered, batch):
    """Add one batch's sub-agent rows to a refresh's sets; nothing is covered here."""
    runs = batch["agent_runs"]
    gathered["transcripts"].update(
        (row["session_key"], row["agent_key"]) for row in runs["transcripts"])
    gathered["summaries"].update(
        (row["session_key"], row["agent_key"]) for row in runs["summaries"])
    gathered["unclassified"] = min(MAX_COUNTER,
                                   gathered["unclassified"] + runs["unclassified"])


def _merge_agent_runs(first, second):
    """Union two sub-agent records, drop covered summaries, then apply the caps."""
    transcripts = {(row["session_key"], row["agent_key"])
                   for row in [*first["transcripts"], *second["transcripts"]]}
    summaries = {(row["session_key"], row["agent_key"])
                 for row in [*first["summaries"], *second["summaries"]]}
    unclassified = min(MAX_COUNTER, first["unclassified"] + second["unclassified"])
    summaries -= transcripts
    kept_transcripts = sorted(transcripts)
    kept_summaries = sorted(summaries)
    cut = max(0, len(kept_transcripts) - MAX_AGENT_TRANSCRIPTS)
    cut += max(0, len(kept_summaries) - MAX_AGENT_SUMMARIES)
    kept_transcripts = kept_transcripts[:MAX_AGENT_TRANSCRIPTS]
    kept_summaries = kept_summaries[:MAX_AGENT_SUMMARIES]
    return {
        "transcripts": [{"session_key": session_key, "agent_key": agent_key}
                        for session_key, agent_key in kept_transcripts],
        "summaries": [{"session_key": session_key, "agent_key": agent_key}
                      for session_key, agent_key in kept_summaries],
        "unclassified": min(MAX_COUNTER, unclassified + cut)}


def _summary_shape(value):
    if not isinstance(value, dict) or set(value) != _SUMMARY_FIELDS:
        return False
    try:
        for name in _SUMMARY_FIELDS:
            _counter(value[name])
    except ValueError:
        return False
    return True


def _summary_run(record):
    """Return the digest of the run a finished sub-agent's summary names.

    None when the record's usage values are not the summary shape. "" when the
    frame names no run, or more than one. The id is read only inside the frame.
    """
    values = _usage_values(record)
    if not values or not all(_summary_shape(value) for value in values):
        return None
    found = set()
    pending = [record]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
        elif isinstance(item, str):
            for match in _SUMMARY_FRAME.finditer(item):
                found.add(match.group(1))
                if len(found) > 1:
                    return ""
    if len(found) != 1:
        return ""
    return _digest("agent-id", next(iter(found)))


def read_records(tool, lines, *, config=None, source_aliases=(), source_root=None,
                 conversation=None, attribution=None):
    """Normalize a bounded source batch without exposing raw IDs or paths.

    `lines` may be synthetic bytes or an exhausted `_ApprovedLineStream`. Any
    terminal reader failure invalidates the entire batch. This normalizer is not
    a collector or a ledger input while global coverage remains unknown.

    The last two keywords serve the antigravity reader only. `conversation` is
    the id of the conversation synthetic lines belong to (a stream's id is the
    second part of its relative path). `attribution` maps a conversation id to
    a pair, the project alias its saved files name (or None) and the reason it
    names none; without it, or without the conversation in it, no reply is read.
    """
    if tool not in TOOLS:
        raise ValueError("unsupported source")
    issues, contexts, candidates = set(), {}, []
    timing_observations = []
    timing_candidates = []
    agent_transcripts, agent_summaries, agent_unclassified = set(), set(), 0
    config_supplied = config is not None

    def verify_project(project, excluded_roots):
        # The project's remote is the one the user wrote in the consent file.
        return project["remote"], None
    owner = None
    active_owner = None
    source_header_key = None
    parent_header_key = None
    fork_metadata = None
    fork_marker = None
    fork_parent_header = False
    fork_invalid = False
    line_ordinal = 0
    checkpoint_sequence = []
    direct_record_count = 0
    owner_conflict = False
    header_eligible = True
    creation_remote = None
    creation_remote_conflict = False
    aliases = []
    account_filter_requested = False
    source_root_approved = False
    projects = []
    verified_projects = {}
    excluded_roots = []
    requested_accounts = {}
    if config is not None:
        try:
            config = validate_config_bytes(json.dumps(config, allow_nan=False).encode("utf-8"))
        except (TypeError, ValueError, UnicodeError, Unavailable, RecursionError,
                OverflowError):
            config = None
            issues.add("invalid_record")
    if config_supplied and config is None:
        return {"schema": READER_VERSION, "tool": tool, "events": [],
                "timing_observations": [], "timing_coverage": "unknown",
                "coverage": "unknown", "identity_coverage": "unknown",
                "ownership_coverage": "unknown", "issues": ["invalid_record"],
                "agent_runs": _empty_agent_runs()}
    if isinstance(config, dict) and not config["enabled"]:
        return {"schema": READER_VERSION, "tool": tool, "events": [],
                "timing_observations": [], "timing_coverage": "unknown",
                "coverage": "unknown", "identity_coverage": "unknown",
                "ownership_coverage": "unknown", "issues": ["disabled"],
                "agent_runs": _empty_agent_runs()}
    if isinstance(config, dict) and isinstance(source_aliases, (list, tuple, set)):
        if any(not isinstance(alias, str) for alias in source_aliases):
            source_aliases = ()
            issues.add("invalid_record")
        sources = [source for source in config.get("sources", [])
                   if isinstance(source, dict) and source.get("tool") == tool]
        available_aliases = {source.get("alias") for source in sources}
        input_root = source_root
        if input_root is None and isinstance(lines, _ApprovedLineStream):
            input_root = lines.root
        try:
            input_root = str(Path(os.path.abspath(input_root))) if input_root is not None else None
        except (TypeError, ValueError, OSError):
            input_root = None
        root_aliases = {source.get("alias") for source in sources
                        if input_root is not None and source.get("root") == input_root}
        source_root_approved = bool(root_aliases)
        aliases = sorted((set(source_aliases) & root_aliases) if source_aliases
                         else root_aliases)
        projects = [project for project in config.get("projects", [])
                    if isinstance(project, dict)]
        excluded_roots = [source.get("root") for source in config.get("sources", [])
                          if isinstance(source, dict)]
        excluded_roots.extend(project.get("path") for project in projects)
        requested_accounts = config.get("requested_accounts", {})
        account_filter_requested = bool(set(requested_accounts) &
                                        (set(aliases) if aliases else available_aliases))
    elif config is not None:
        issues.add("invalid_record")

    antigravity_id = (_antigravity_conversation_id(conversation, lines)
                      if tool == "antigravity" else None)  # vendor-ok: one id per log
    kind = None
    for line in lines:
        kind = None
        line_ordinal += 1
        try:
            if not isinstance(line, bytes) or len(line) > MAX_LINE or not line.endswith(b"\n"):
                raise ValueError
            record = json.loads(line.decode("utf-8"), object_pairs_hook=_object,
                                parse_constant=_constant)
            if not isinstance(record, dict):
                raise ValueError
            kind = record.get("type")
            if tool == "antigravity":  # vendor-ok: producer token-record shape
                # A reply is a complete token record with a zone-aware time; a
                # line with neither token field is skipped (a `usage` key shows
                # a changed format); anything half-formed is closed and uncounted.
                try:
                    kinds = _antigravity_usage(record)
                    if kinds is not None:
                        timestamp = _timestamp(record.get("created_at"))
                except (ValueError, TypeError, OverflowError):
                    issues.add("invalid_record")
                    continue
                if kinds is None:
                    if _usage_values(record):
                        issues.add("unsupported_usage_contract")
                    continue
                if antigravity_id is None:
                    issues.add("invalid_record")
                    continue
                if any(name in record and record[name] != antigravity_id
                       for name in ("conversationId", "conversation_id")):
                    issues.add("conflicting_binding")
                    continue
                try:
                    folder_alias, folder_reason = _antigravity_attribution(
                        attribution.get(antigravity_id)
                        if isinstance(attribution, dict) else None)
                except ValueError:
                    issues.add("invalid_record")
                    continue
                reasons = set()
                bound = None
                event_key = _digest(tool, antigravity_id, timestamp,
                                    kinds["fresh_input"], kinds["output"])
                if account_filter_requested:
                    kinds = _unknown_kinds()
                    reasons.add("account_filter_unproven")
                elif folder_alias is None:
                    reasons.add(folder_reason)
                else:
                    folder_project = next(
                        (item for item in projects if item.get("alias") == folder_alias),
                        None) if source_root_approved else None
                    if folder_project is None:
                        reasons.add("project_path_unapproved")
                    else:
                        cache_key = (folder_project.get("alias"), folder_project.get("path"))
                        if cache_key not in verified_projects:
                            verified_projects[cache_key] = verify_project(folder_project,
                                                                          excluded_roots)
                        current_remote, remote_reason = verified_projects[cache_key]
                        if remote_reason is None:
                            bound = folder_project
                        else:
                            reasons.add(remote_reason)
                candidate = _event_record(
                    tool=tool, event_key=event_key, aliases=aliases,
                    thread=antigravity_id, session=antigravity_id,
                    session_digest=_short_session_digest(antigravity_id),
                    timestamp=timestamp, time_known=True, kinds=kinds,
                    reasons=reasons,
                    project_alias=bound["alias"] if bound else None,
                    project_state="current_local_verified" if bound else "unknown",
                    ownership="proven" if bound else "unknown")
                candidates.append((candidate, tuple(candidate["kinds"].items()),
                                   (antigravity_id, None, None, None), None, line_ordinal))
                continue
            if tool == "claude":  # vendor-ok: producer assistant usage shape
                if kind != "assistant":
                    if kind in {"user", "system", "progress", "file-history-snapshot"}:
                        continue
                    if not _usage_values(record):
                        continue
                    run = _summary_run(record)
                    try:
                        session_key = _digest(tool, _text(record["sessionId"]))
                    except (KeyError, ValueError):
                        session_key = None
                    if not run or session_key is None:
                        issues.add("agent_runs_incomplete")
                        agent_unclassified += 1
                        continue
                    agent_summaries.add((session_key, run))
                    continue
                message = record["message"]
                session = _text(record["sessionId"])
                if record.get("isSidechain") is True:
                    try:
                        agent_key = _digest("agent-id", _text(record["agentId"]))
                    except (KeyError, ValueError):
                        pass
                    else:
                        agent_transcripts.add((_digest(tool, session), agent_key))
                message_id = _text(message["id"])
                request = record.get("requestId")
                response = _text(request) if request is not None else message_id
                event_key = _digest(tool, response, message_id)
                try:
                    kinds = _claude_usage(message["usage"])
                    cache_write_ttl = _claude_cache_ttl(
                        message["usage"], kinds["cache_write"])
                    usage_invalid = False
                except (ValueError, TypeError, KeyError):
                    kinds = _unknown_kinds()
                    cache_write_ttl = {"five_minute": None, "one_hour": None}
                    issues.add("invalid_record")
                    usage_invalid = True
                try:
                    timestamp = _timestamp(record.get("timestamp"))
                    time_known = True
                except (ValueError, TypeError, KeyError, OverflowError):
                    timestamp, time_known = None, False
                model = message.get("model")
                model_invalid = False
                if model is not None:
                    try:
                        model = _safe_alias(model)
                    except (ValueError, TypeError):
                        model = None
                        issues.add("invalid_record")
                        model_invalid = True
                reasons = set()
                bound = None
                folder_project = (_project_for_folder(record.get("cwd"), projects)
                                  if source_root_approved else None)
                if request is None:
                    reasons.add("conflicting_binding")
                elif account_filter_requested:
                    pass
                elif folder_project is None:
                    reasons.add("project_path_unapproved")
                else:
                    cache_key = (folder_project.get("alias"), folder_project.get("path"))
                    if cache_key not in verified_projects:
                        verified_projects[cache_key] = verify_project(folder_project,
                                                                      excluded_roots)
                    current_remote, remote_reason = verified_projects[cache_key]
                    if remote_reason is None:
                        bound = folder_project
                    else:
                        reasons.add(remote_reason)
                if usage_invalid or model_invalid:
                    reasons.add("invalid_record")
                if account_filter_requested:
                    kinds = _unknown_kinds()
                    cache_write_ttl = {"five_minute": None, "one_hour": None}
                    reasons.add("account_filter_unproven")
                candidate = _event_record(
                    tool=tool, event_key=event_key, aliases=aliases, thread=session,
                    session=session, session_digest=_short_session_digest(session),
                    timestamp=timestamp, time_known=time_known,
                    kinds=kinds, model=model,
                    model_provenance=("usage_record" if model is not None else "unknown"),
                    effective_model=model,
                    cache_write_ttl=cache_write_ttl, reasons=reasons,
                    project_alias=bound["alias"] if bound else None,
                    project_state="current_local_verified" if bound else "unknown",
                    ownership="proven" if bound else "unknown")
                candidates.append((candidate, tuple(candidate["kinds"].items()),
                                   (session, None, None, None), None, line_ordinal))
                continue

            payload = record.get("payload")
            if kind == "session_meta":
                try:
                    candidate_owner, candidate_fork = _codex_header(payload)
                except (ValueError, TypeError, KeyError, AttributeError):
                    header_eligible = False
                    fork_invalid = fork_invalid or fork_metadata is not None
                    issues.add("unsupported_or_invalid_session_metadata")
                    continue
                candidate_header_key = _codex_header_key(candidate_owner, payload)
                if owner is None:
                    owner = candidate_owner
                    active_owner = owner
                    fork_metadata = candidate_fork
                    source_header_key = candidate_header_key
                elif candidate_owner == owner:
                    if (candidate_fork != fork_metadata
                            or candidate_header_key != source_header_key):
                        owner_conflict = True
                        fork_invalid = fork_invalid or fork_metadata is not None
                        issues.add("conflicting_session_metadata")
                    active_owner = owner
                elif (fork_metadata is not None and fork_marker is None
                      and candidate_owner == (fork_metadata["parent"], fork_metadata["parent"])
                      and candidate_fork is None):
                    if parent_header_key is not None and parent_header_key != candidate_header_key:
                        fork_invalid = True
                        issues.add("conflicting_session_metadata")
                        continue
                    active_owner = candidate_owner
                    parent_header_key = candidate_header_key
                    fork_parent_header = True
                else:
                    owner_conflict = True
                    fork_invalid = fork_invalid or fork_metadata is not None
                    issues.add("conflicting_session_metadata")
                git_info = payload.get("git")
                source_remote = None
                if git_info is not None:
                    try:
                        if not isinstance(git_info, dict):
                            raise ValueError
                        raw_remote = git_info.get("repository_url")
                        if raw_remote is not None:
                            source_remote = _strip_remote(raw_remote)
                    except (ValueError, TypeError):
                        creation_remote_conflict = True
                        issues.add("project_remote_mismatch")
                if source_remote is not None:
                    if creation_remote is None:
                        creation_remote = source_remote
                    elif creation_remote != source_remote:
                        creation_remote_conflict = True
                        issues.add("project_remote_mismatch")
            elif kind == "turn_context":
                context = _codex_context(payload, active_owner if header_eligible else None)
                turn = context["turn"]
                normalized = (context["root"], context["cwd"], context["model"], context["owner"])
                context_key = (context["owner"], turn)
                previous = contexts.get(context_key)
                if previous is not None and previous[0] != normalized:
                    contexts[context_key] = None
                    issues.add("conflicting_turn_context")
                elif context_key not in contexts:
                    contexts[context_key] = (normalized, context)
            elif (kind == "event_msg" and isinstance(payload, dict)
                  and payload.get("type") in {"task_started", "turn_started"}):
                if fork_metadata is not None:
                    try:
                        marker_turn = _text(payload["turn_id"])
                        parent_pair = (fork_metadata["parent"], fork_metadata["parent"])
                        if (owner != (fork_metadata["child"], fork_metadata["session"])
                                or active_owner not in {owner, parent_pair}
                                or owner_conflict or not header_eligible
                                or fork_marker is not None
                                or not fork_parent_header
                                or not any(item["role"] == "parent_prefix"
                                           for item in checkpoint_sequence)
                                or payload.get("trigger_turn") is False
                                or (parent_pair, marker_turn) in contexts):
                            raise ValueError
                        fork_marker = {"turn": marker_turn, "line": line_ordinal}
                        active_owner = owner
                    except (ValueError, TypeError, KeyError):
                        fork_invalid = True
                        issues.add("unsupported_fork_boundary")
            elif kind == "token_usage_record":
                direct_record_count += 1
                thread, session, turn, root, response = _codex_identity(payload)
                event_key = _digest(tool, thread, response)
                reasons = set()
                try:
                    timestamp = _timestamp(record.get("timestamp"))
                    time_known = True
                except (ValueError, TypeError, KeyError, OverflowError):
                    timestamp, time_known = None, False
                try:
                    direct = _codex_direct(payload)
                    kinds = direct[-1]
                except (ValueError, TypeError, KeyError):
                    kinds = _unknown_kinds()
                    reasons.add("invalid_record")
                cache_write_ttl = (
                    {"five_minute": 0, "one_hour": 0}
                    if kinds["cache_write"] == 0
                    else {"five_minute": None, "one_hour": None})
                try:
                    # Cumulative snapshots are validated but never charge inputs.
                    turn_snapshot = _codex_usage(payload["turn_token_usage"])
                    thread_snapshot = _codex_usage(payload["thread_token_usage"])
                    snapshots_valid = True
                except (ValueError, TypeError, KeyError):
                    reasons.add("snapshot_conflict")
                    issues.add("snapshot_conflict")
                    turn_snapshot = thread_snapshot = None
                    snapshots_valid = False
                context_entry = contexts.get(((thread, session), turn))
                context = None if context_entry is None else context_entry[1]
                valid_normal = bool(
                    fork_metadata is None and not owner_conflict and header_eligible
                    and owner == (thread, session) and context is not None
                    and context.get("owner") == (thread, session)
                    and context.get("turn") == turn and context.get("root") == turn
                    and root == turn)
                parent_pair = (fork_metadata["parent"], fork_metadata["parent"]) \
                    if fork_metadata is not None else None
                child_pair = (fork_metadata["child"], fork_metadata["session"]) \
                    if fork_metadata is not None else None
                copied_parent = bool(fork_metadata is not None and not fork_invalid
                    and fork_parent_header and fork_marker is None
                    and (thread, session) == parent_pair and context is not None
                    and context.get("owner") == parent_pair and root == turn
                    and context.get("root") == turn)
                fork_child = bool(fork_metadata is not None and not fork_invalid
                    and fork_marker is not None and active_owner == owner == child_pair
                    and (thread, session) == child_pair and turn == fork_marker["turn"]
                    and context is not None and context.get("owner") == child_pair
                    and context.get("turn") == turn and context.get("root") == root)
                if fork_metadata is not None and not (copied_parent or fork_child):
                    fork_invalid = True
                    issues.add("unsupported_fork_boundary")
                if fork_metadata is not None and (not snapshots_valid
                                                  or kinds == _unknown_kinds()):
                    fork_invalid = True
                    issues.add("snapshot_conflict" if not snapshots_valid
                               else "invalid_record")
                binding_proven = valid_normal or copied_parent or fork_child
                project = None
                model = context.get("model") if context is not None else None
                if (binding_proven and source_root_approved
                        and context.get("cwd") is not None):
                    matches = [project for project in projects
                               if project.get("path") == context["cwd"]]
                    if len(matches) == 1:
                        project = matches[0]
                    else:
                        reasons.add("project_path_unapproved")
                else:
                    reasons.add("project_path_unapproved")
                if account_filter_requested:
                    kinds = _unknown_kinds()
                    cache_write_ttl = {"five_minute": None, "one_hour": None}
                    reasons.add("account_filter_unproven")
                ownership = "proven" if binding_proven else "unknown"
                if not binding_proven:
                    reasons.add("conflicting_binding")
                candidate = _event_record(
                    tool=tool, event_key=event_key, aliases=aliases, thread=thread,
                    session=session, turn=turn, root=root,
                    timestamp=timestamp, time_known=time_known, kinds=kinds,
                    ownership=ownership, model=model,
                    model_provenance=("selected_context" if model is not None else "unknown"),
                    effective_model=None, cache_write_ttl=cache_write_ttl,
                    session_digest=(_short_session_digest(thread) if binding_proven else None),
                    reasons=reasons)
                candidates.append((candidate, None, None,
                                   (turn, context, project, binding_proven, fork_child,
                                    copied_parent), line_ordinal))
                if kinds != _unknown_kinds() and snapshots_valid and context is not None:
                    checkpoint_sequence.append({
                        "event_key": event_key,
                        "owner_key": _digest(tool, thread),
                        "session_key": _digest(tool, session),
                        "turn_key": _digest(tool, thread, turn),
                        "root_key": _digest(tool, session, root),
                        "counter_family_key": _digest(
                            "codex-counter-family", _digest(tool, session),
                            _digest(tool, session, root)),
                        "ordinal": line_ordinal,
                        "parent_ordinal": None,
                        "kinds": dict(kinds),
                        "turn_snapshot": turn_snapshot,
                        "thread_snapshot": thread_snapshot,
                        "context_key": _digest(context.get("root"), context.get("cwd"),
                                               context.get("model")),
                        "role": ("parent_prefix" if copied_parent else
                                 "child" if fork_child else "direct"),
                    })
            elif kind == "event_msg" and payload.get("type") == "token_count":
                issues.add("legacy_checkpoint_unreconciled")
            elif kind == "event_msg" and payload.get("type") == "item_completed":
                item = payload.get("item")
                if not isinstance(item, dict):
                    raise ValueError
                if item.get("type") != "CommandExecution":
                    continue
                classification = classify_pytest_command(item.get("command"))
                reasons = set()
                if classification is None:
                    issues.add("test_command_classification_unknown")
                    reasons.add("test_command_classification_unknown")
                try:
                    thread = _codex_uuid(payload["thread_id"])
                    turn = _text(payload["turn_id"])
                    item_id = _text(item["id"])
                except (ValueError, TypeError, KeyError):
                    issues.add("timing_identity_unknown")
                    continue
                try:
                    start = _counter(payload["started_at_ms"])
                    end = _counter(payload["completed_at_ms"])
                    if not 0 < start < end:
                        raise ValueError
                    _wait_datetime(start)
                    _wait_datetime(end)
                except (ValueError, TypeError, KeyError, OverflowError):
                    start = end = None
                    reasons.add("ambiguous_time")
                    issues.add("invalid_record")
                if classification is not None and start is not None:
                    timing_observations.append({
                        "classification": classification,
                        "started_at_ms": start,
                        "completed_at_ms": end,
                    })
                active_pair = active_owner
                context_entry = contexts.get((active_pair, turn))
                context = None if context_entry is None else context_entry[1]
                wait = {
                    "wait_key": _digest("codex-wait", tool, thread, turn, item_id),
                    "source_aliases": list(aliases), "occurrences": [],
                    "thread_key": _digest(tool, thread),
                    "session_key": _digest(tool, active_pair[1]) if active_pair else None,
                    "session_digest": _short_session_digest(thread),
                    "turn_key": _digest(tool, thread, turn),
                    "root_turn_key": (_digest(tool, active_pair[1], context["root"])
                                       if context is not None else None),
                    "lineage_key": (_digest("codex-lineage",
                                             _digest(tool, fork_metadata["child"]))
                                    if fork_metadata is not None and fork_marker is not None
                                    and thread == fork_metadata["child"]
                                    and turn == fork_marker["turn"] else None),
                    "project_alias": None, "project_association": "unknown",
                    "ownership": "unknown", "classification": classification or "unknown",
                    "started_at_ms": start, "completed_at_ms": end,
                    "model": context.get("model") if context is not None else None,
                    "model_provenance": ("selected_context" if context is not None
                                         and context.get("model") is not None else "unknown"),
                    "reasons": sorted(reasons), "_line_ordinal": line_ordinal,
                    "_thread": thread, "_session": active_pair[1] if active_pair else None,
                    "_turn": turn, "_fork_child": bool(fork_metadata is not None
                        and fork_marker is not None and thread == fork_metadata["child"]
                        and turn == fork_marker["turn"]),
                    "_fork_parent_copy": bool(fork_metadata is not None
                        and fork_marker is None and thread == fork_metadata["parent"]),
                }
                timing_candidates.append(wait)
            elif kind not in {"response_item", "event_msg", "compacted", "world_state"}:
                issues.add("unsupported_record")
        except (ValueError, TypeError, KeyError, AttributeError, UnicodeError,
                OverflowError, RecursionError):
            issues.add("invalid_record")
            if kind == "token_usage_record" and fork_metadata is not None:
                fork_invalid = True
                issues.add("unsupported_fork_boundary")

    if isinstance(lines, _ApprovedLineStream) and lines.terminal_reason is not None:
        candidates.clear()
        timing_observations.clear()
        timing_candidates.clear()
        agent_transcripts.clear()
        agent_summaries.clear()
        agent_unclassified = 0
        issues.add(lines.terminal_reason)
    if len(candidates) > MAX_NORMALIZED_EVENTS:
        candidates.clear()
        timing_candidates.clear()
        agent_transcripts.clear()
        agent_summaries.clear()
        agent_unclassified = 0
        issues.add("source_budget_exceeded")

    normalized_waits = []
    for wait in timing_candidates:
        thread, session, turn = wait["_thread"], wait["_session"], wait["_turn"]
        context_entry = contexts.get(((thread, session), turn)) if session is not None else None
        context = None if context_entry is None else context_entry[1]
        reasons = set(wait["reasons"])
        binding_proven = bool(
            context is not None and context.get("owner") == (thread, session)
            and context.get("turn") == turn
            and (context.get("root") == turn or wait["_fork_child"])
            and not owner_conflict and header_eligible
            and ((fork_metadata is None and owner == (thread, session))
                 or wait["_fork_child"])
            and not wait["_fork_parent_copy"])
        if not binding_proven:
            reasons.add("conflicting_binding")
            wait["session_key"] = None
            wait["session_digest"] = None
            wait["turn_key"] = None
            wait["root_turn_key"] = None
            wait["model"] = None
            wait["model_provenance"] = "unknown"
        else:
            wait["root_turn_key"] = _digest(tool, session, context["root"])
            if wait["_fork_child"]:
                reasons.add("conflicting_binding")  # scanner clears only after verified lineage
            if source_root_approved and context.get("cwd") is not None:
                matching = [project for project in projects
                            if project.get("path") == context["cwd"]]
                if len(matching) == 1 and not account_filter_requested:
                    project = matching[0]
                    cache_key = (project.get("alias"), project.get("path"))
                    if cache_key not in verified_projects:
                        verified_projects[cache_key] = verify_project(project, excluded_roots)
                    current_remote, remote_reason = verified_projects[cache_key]
                    if remote_reason is None and not creation_remote_conflict and (
                            creation_remote is None or creation_remote == current_remote):
                        if wait["_fork_child"]:
                            wait["_candidate_project_alias"] = project.get("alias")
                            wait["project_alias"] = None
                            wait["project_association"] = "unknown"
                        else:
                            wait["project_alias"] = project.get("alias")
                            wait["project_association"] = "current_local_verified"
                    else:
                        reasons.add(remote_reason or "project_remote_mismatch")
                elif account_filter_requested:
                    reasons.add("account_filter_unproven")
                else:
                    reasons.add("project_path_unapproved")
            else:
                reasons.add("project_path_unapproved")
        wait["ownership"] = "proven" if binding_proven and not wait["_fork_child"] else "unknown"
        wait["reasons"] = sorted(reasons)
        for private_field in ("_thread", "_session", "_turn"):
            wait.pop(private_field, None)
        normalized_waits.append(wait)

    merged = {}
    merge_signatures = {}
    event_last_line = {}
    for event, usage_signature, binding_signature, details, ordinal in candidates:
        if details is not None:
            turn, context, project, binding_proven, fork_child, copied_parent = details
            current = contexts.get((context.get("owner"), turn)) if context is not None else None
            if copied_parent:
                continue
            if (owner_conflict or not header_eligible or context is None or current is None
                    or current[1] != context):
                event["session_key"] = None
                event["session_digest"] = None
                event["turn_key"] = None
                event["root_turn_key"] = None
                event["project_alias"] = None
                event["project_association"] = "unknown"
                event["ownership"] = "unknown"
                event["model"] = None
                event["model_provenance"] = "unknown"
                event["effective_model"] = None
                event["reasons"] = sorted(set(event["reasons"]) | {"conflicting_binding"})
            elif binding_proven and project is not None:
                if account_filter_requested:
                    event["reasons"] = sorted(set(event["reasons"]) | {"account_filter_unproven"})
                else:
                    project_cache_key = (project.get("alias"), project.get("path"))
                    if project_cache_key not in verified_projects:
                        verified_projects[project_cache_key] = verify_project(
                            project, excluded_roots)
                    current_remote, remote_reason = verified_projects[project_cache_key]
                    if remote_reason is not None:
                        event["reasons"] = sorted(set(event["reasons"]) | {remote_reason})
                    elif creation_remote_conflict or (creation_remote is not None
                                                      and creation_remote != current_remote):
                        event["reasons"] = sorted(set(event["reasons"]) | {"project_remote_mismatch"})
                    else:
                        event["project_alias"] = project.get("alias")
                        event["project_association"] = "current_local_verified"
            if fork_child:
                event["ownership"] = "unknown"
                event["reasons"] = sorted(set(event["reasons"])
                                          | {"conflicting_binding"})
            if creation_remote_conflict and project is not None:
                event["project_alias"] = None
                event["project_association"] = "unknown"
                event["reasons"] = sorted(set(event["reasons"]) | {"project_remote_mismatch"})
            usage_signature = (tuple(event["kinds"].items()),
                               tuple(event["cache_write_ttl"].items()))
            binding_signature = (event["thread_key"], event["session_key"],
                                 event["session_digest"],
                                 event["turn_key"], event["root_turn_key"],
                                 event["project_alias"], event["project_association"],
                                 event["ownership"], event["model"],
                                 event["model_provenance"], event["effective_model"])
        else:
            usage_signature = (tuple(event["kinds"].items()),
                               tuple(event["cache_write_ttl"].items()))
            binding_signature = (event["thread_key"], event["session_key"],
                                 event["session_digest"],
                                 event["turn_key"], event["root_turn_key"],
                                 event["project_alias"], event["project_association"],
                                 event["ownership"], event["model"],
                                 event["model_provenance"], event["effective_model"])
        key = event["event_key"]
        event_last_line[key] = max(event_last_line.get(key, 0), ordinal)
        if key not in merged:
            merged[key] = event
            merge_signatures[key] = (usage_signature, binding_signature)
            continue
        prior_usage, prior_binding = merge_signatures[key]
        earlier = None
        if tool == "claude":
            first, second = merged[key]["observed_at"], event["observed_at"]
            if first is not None and second is not None and first != second:
                earlier = min(first, second, key=lambda text: datetime.fromisoformat(
                    text.replace("Z", "+00:00")))
        _merge_normalized_event(merged[key], event)
        if earlier is not None:
            merged[key]["observed_at"] = earlier
            merged[key]["time_coverage"] = "known"
            merged[key]["reasons"] = sorted(set(merged[key]["reasons"]) - {"ambiguous_time"})
        if prior_usage != usage_signature:
            merged[key]["kinds"] = _unknown_kinds()
            merged[key]["cache_write_ttl"] = {
                "five_minute": None, "one_hour": None}
            merged[key]["reasons"] = sorted(set(merged[key]["reasons"]) | {"conflicting_usage"})
        if prior_binding != binding_signature:
            merged[key]["session_key"] = None
            merged[key]["session_digest"] = None
            merged[key]["turn_key"] = None
            merged[key]["root_turn_key"] = None
            merged[key]["project_alias"] = None
            merged[key]["project_association"] = "unknown"
            merged[key]["ownership"] = "unknown"
            merged[key]["model"] = None
            merged[key]["model_provenance"] = "unknown"
            merged[key]["effective_model"] = None
            merged[key]["reasons"] = sorted(set(merged[key]["reasons"]) | {"conflicting_binding"})
        merge_signatures[key] = (prior_usage, prior_binding)

    normalized = list(merged.values())
    if not normalized and not issues:
        issues.add("no_supported_usage")
    checkpoint_sequence = _dedupe_checkpoint_sequence(checkpoint_sequence) or checkpoint_sequence
    direct_record_count = len(checkpoint_sequence)
    fork_evidence = None
    if fork_metadata is not None:
        parent_prefix = [item for item in checkpoint_sequence
                         if item["role"] == "parent_prefix"]
        child_sequence = [item for item in checkpoint_sequence
                          if item["role"] == "child"]
        fork_evidence = {
            "contract": "codex-copied-legacy/1",
            "source_aliases": aliases,
            "child_key": _digest(tool, fork_metadata["child"]),
            "parent_key": _digest(tool, fork_metadata["parent"]),
            "session_key": _digest(tool, fork_metadata["session"]),
            "parent_header": fork_parent_header,
            "parent_header_key": parent_header_key,
            "invalid": fork_invalid or owner_conflict or not header_eligible,
            "boundary_turn_key": (_digest(tool, fork_metadata["child"],
                                          fork_marker["turn"]) if fork_marker else None),
            "boundary_line": (fork_marker["line"] if fork_marker else None),
            "direct_record_count": direct_record_count,
            "parent_prefix": parent_prefix,
            "child_sequence": child_sequence,
        }
    return {"schema": READER_VERSION, "tool": tool,
            "events": normalized, "event_last_line": event_last_line,
            "checkpoint_sequence": checkpoint_sequence,
            "fork_evidence": fork_evidence,
            "direct_record_count": direct_record_count,
            "source_owner_key": (_digest(tool, owner[0]) if owner else None),
            "source_session_key": (_digest(tool, owner[1]) if owner else None),
            "source_header_key": source_header_key,
            "source_header_valid": bool(owner is not None and header_eligible
                                        and not owner_conflict),
            "timing_observations": timing_observations,
            "wait_candidates": normalized_waits, "timing_coverage": "unknown",
            "coverage": "unknown", "identity_coverage": "unknown",
            "ownership_coverage": "unknown", "issues": sorted(issues),
            "agent_runs": {
                "transcripts": [{"session_key": session_key, "agent_key": agent_key}
                                for session_key, agent_key in sorted(agent_transcripts)],
                "summaries": [{"session_key": session_key, "agent_key": agent_key}
                              for session_key, agent_key in sorted(agent_summaries)],
                "unclassified": agent_unclassified}}


_REFRESH_REASONS = frozenset({
    "none", "disabled", "config_missing", "config_home_unavailable",
    "config_invalid", "git_changed", "git_output_limit", "git_parser_failed",
    "git_timeout", "git_unavailable", "git_untrusted", "ledger_busy",
    "ledger_durability_uncertain", "ledger_invalid", "ledger_old_schema",
    "ledger_unavailable", "ledger_write_failed", "project_export_uncertain", "project_layout_unsupported",
    "project_path_unapproved", "project_remote_ambiguous", "project_remote_mismatch",
    "project_remote_unavailable", "project_export_unavailable",
    "job_unavailable",
    "source_budget_exceeded", "source_changed", "source_read_unavailable",
    "catching_up", "source_too_large",
    "account_filter_unproven", "partial_tail", "conflicting_usage",
    "conflicting_binding", "snapshot_conflict", "unavailable",
})


def _closed_refresh_receipt(result):
    """Return the exact public receipt shape, discarding private counters."""
    if not isinstance(result, dict):
        result = {}
    status = result.get("status")
    reason = result.get("reason")
    if status in {"written", "ok"}:
        if reason is not None and reason != "none":
            status, reason = "unavailable", "unavailable"
        else:
            status, reason = "ok", "none"
    elif status == "partial":
        if reason not in {"catching_up", "source_too_large"}:
            status, reason = "unavailable", "unavailable"
    elif status == "disabled":
        if reason not in {"config_missing", "disabled"}:
            reason = "disabled"
    elif status == "unavailable":
        if reason not in _REFRESH_REASONS or reason in {"none", "disabled", "config_missing"}:
            reason = "unavailable"
    else:
        status, reason = "unavailable", "unavailable"
    return {"schema": "cairn-meter-refresh/1", "status": status,
            "reason": reason, "coverage": "unknown"}


def _run_explicit_refresh(*, report=False):
    try:
        home = _fixed_user_home()
        if report:
            return _refresh_ledger(home, report_current_directory=os.getcwd())
        result = _refresh_ledger(home)
    except Unavailable:
        result = {"status": "unavailable", "reason": "config_home_unavailable"}
    return result if report else _closed_refresh_receipt(result)


def _pulse_has_explicit_inputs(args):
    return any((args.junit_report, args.before_junit_report,
                args.tier_inventory, args.before_tier_inventory,
                args.artifact_input, args.commit_label, args.python_label,
                args.selection_label, args.seed_label, args.before_commit_label,
                args.before_python_label, args.before_selection_label,
                args.before_seed_label))


def main():
    """Run one command; any failure prints only a closed answer, never a traceback or path."""
    try:
        return _main()
    except Exception:
        as_json = "--json" in sys.argv[1:]
        if any(argument in {"refresh", "rebuild"} for argument in sys.argv[1:]):
            receipt = _closed_refresh_receipt({"status": "unavailable", "reason": "unavailable"})
            if as_json:
                print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
            else:
                print(f"meter {receipt['status']}: {receipt['reason']}")
        elif as_json:
            print(json.dumps({"schema": "cairn-meter-foundation/1", "collection": "unavailable",
                              "usage": {tool: "unknown" for tool in TOOLS}}, sort_keys=True))
        else:
            print("meter: unavailable; usage remains unknown for all supported tools")
        return 5


def _main():
    """Config-only status by default; collection requires explicit refresh/rebuild."""
    parser = argparse.ArgumentParser(description="Cairn usage meter")
    parser.add_argument("--json", action="store_true", help="emit the status as JSON")
    commands = parser.add_subparsers(dest="command")
    for command in ("refresh", "rebuild"):
        child = commands.add_parser(command)
        child.add_argument("--json", action="store_true", dest="command_json",
                           help="emit the closed refresh receipt as JSON")
        if command == "refresh":
            child.add_argument("--report", action="store_true",
                               help="refresh and print the complete public pulse")
            _PULSE.register_arguments(child, include_json=False)
    args = parser.parse_args()
    if args.command is not None:
        emit_json = args.json or getattr(args, "command_json", False)
        if args.command == "refresh":
            pulse_inputs = _pulse_has_explicit_inputs(args)
            if args.report and args.meter_aggregate is not None:
                parser.error("--report does not accept --meter-aggregate")
            if not args.report and pulse_inputs:
                parser.error("pulse inputs require --report")
            if args.report:
                args.json = emit_json
                result = _run_explicit_refresh(report=True)
                receipt = _closed_refresh_receipt(result)
                should_render = (receipt["status"] == "ok"
                                 or (receipt["status"] == "disabled" and pulse_inputs))
                if should_render:
                    aggregate = result.get("current_project_aggregate")
                    return _PULSE.run_pulse(
                        args, parser, meter_aggregate_bytes=aggregate)
                code = 0 if receipt["status"] == "disabled" else 5
                if emit_json:
                    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
                else:
                    print(f"meter {receipt['status']}: {receipt['reason']}")
                return code
        receipt = _run_explicit_refresh()
        code = 0 if receipt["status"] in {"ok", "disabled"} else 5
        if emit_json:
            print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
        else:
            print(f"meter {receipt['status']}: {receipt['reason']}")
        return code

    try:
        home = _fixed_user_home()
        config = load_config(home / ".cairn" / "meter.json")
    except Unavailable:
        status, code = "unavailable", 5
    else:
        status = "disabled" if config is None or not config["enabled"] else "unavailable"
        code = 0 if status == "disabled" else 5
    result = {"schema": "cairn-meter-foundation/1", "collection": status,
              "usage": {tool: "unknown" for tool in TOOLS}}
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(f"meter: {status}; usage remains unknown for all supported tools")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
