#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Meter reader foundations; no source discovery, collection, or ledger is enabled.

Internal bounded readers accept only explicitly supplied paths and bytes, and
current tests use synthetic roots/files. The CLI resolves consent from the
fixed OS account home and stops before source, project, Git, or ledger access.
Normalized events remain unknown globally and are not project aggregates.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
import argparse
import uuid
import selectors
import signal
import subprocess
import time
try:
    import pwd
except ImportError:  # vendor-ok: POSIX account lookup is deliberately unsupported elsewhere
    pwd = None
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
MAX_BATCH_BYTES = 64 * 1024 * 1024
MAX_BATCH_LINES = 100_000
MAX_NORMALIZED_EVENTS = 100_000
MAX_GIT_BYTES = 64 * 1024 * 1024
MAX_GIT_CONFIG_BYTES = 256 * 1024
MAX_GIT_STDOUT = 16 * 1024
MAX_GIT_STDERR = 4 * 1024
GIT_TIMEOUT_SECONDS = 5
GIT_CLEANUP_SECONDS = 1
_PRIVATE_FS_SUPPORTED = os.name == "posix"


class Unavailable(Exception):
    """A closed, non-sensitive failure used at the CLI boundary."""


class _MissingConfig(Exception):
    """The opt-in file or its private directory has not been created."""


def _fixed_user_home():
    """Resolve consent only from the equal-UID POSIX account database."""
    try:
        uid = os.getuid()
        if uid != os.geteuid() or pwd is None:
            raise Unavailable
        home_text = pwd.getpwuid(uid).pw_dir
        home = Path(home_text)
        if not home.is_absolute() or any(part in {".", ".."} for part in home.parts):
            raise Unavailable
        _verify_private_home(home)
        return home
    except Unavailable:
        raise
    except (OSError, KeyError, TypeError, ValueError, AttributeError):
        raise Unavailable from None


def _verify_private_home(home):
    """Verify the account home and every ancestor without following links."""
    if (not _PRIVATE_FS_SUPPORTED or not hasattr(os, "O_DIRECTORY")
            or not hasattr(os, "O_NOFOLLOW")):
        raise Unavailable
    path = Path(os.path.abspath(home))
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = -1
    try:
        fd = os.open(path.anchor, flags)
        current = Path(path.anchor)
        for part in path.parts[1:]:
            next_fd = os.open(part, flags, dir_fd=fd)
            info = os.fstat(next_fd)
            current = current / part
            if not stat.S_ISDIR(info.st_mode):
                os.close(next_fd)
                raise Unavailable
            if info.st_uid not in {0, os.getuid()}:
                os.close(next_fd)
                raise Unavailable
            if (stat.S_IMODE(info.st_mode) & 0o022
                    and not (info.st_uid == 0 and info.st_mode & stat.S_ISVTX)):
                os.close(next_fd)
                raise Unavailable
            if current == path and info.st_uid != os.getuid():
                os.close(next_fd)
                raise Unavailable
            os.close(fd)
            fd = next_fd
    except (OSError, ValueError, TypeError):
        raise Unavailable from None
    finally:
        if fd >= 0:
            os.close(fd)


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
    """Legacy synthetic whole-file helper; source reading uses `_iter_approved_lines`."""
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


def _open_directory_chain(path):
    """Open an absolute directory path without following any component."""
    path = Path(os.path.abspath(path))
    if (not _PRIVATE_FS_SUPPORTED or not hasattr(os, "O_NOFOLLOW")
            or not hasattr(os, "O_DIRECTORY")):
        raise Unavailable
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open(path.anchor, flags)
    try:
        for part in path.parts[1:]:
            next_fd = os.open(part, flags, dir_fd=fd)
            info = os.fstat(next_fd)
            if not stat.S_ISDIR(info.st_mode):
                os.close(next_fd)
                raise Unavailable
            os.close(fd)
            fd = next_fd
        return fd
    except Exception:
        os.close(fd)
        raise


class _ApprovedLineStream:
    """Single-file bounded reader; `terminal_reason` is final after exhaustion."""

    def __init__(self, root, relative, budget):
        self.root = root
        self.relative = relative
        self.budget = budget
        self.terminal_reason = "source_read_unavailable"
        self._started = False

    def __iter__(self):
        if self._started:
            self.terminal_reason = "source_read_unavailable"
            return
        self._started = True
        directory_fd = file_fd = -1
        reason = "source_read_unavailable"
        try:
            if (type(self.budget) is not int or not 0 <= self.budget <= MAX_BATCH_BYTES
                    or not isinstance(self.relative, str) or not self.relative
                    or Path(self.relative).is_absolute()
                    or any(part in {".", ".."} for part in Path(self.relative).parts)):
                reason = "source_budget_exceeded"
                return
            parts = Path(self.relative).parts
            directory_fd = _open_directory_chain(self.root)
            for part in parts[:-1]:
                next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                  dir_fd=directory_fd)
                os.close(directory_fd)
                directory_fd = next_fd
            leaf = parts[-1]
            before = os.stat(leaf, dir_fd=directory_fd, follow_symlinks=False)
            if not stat.S_ISREG(before.st_mode):
                return
            file_fd = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd)
            opened = os.fstat(file_fd)
            if (not stat.S_ISREG(opened.st_mode)
                    or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)):
                reason = "source_changed"
                return
            total = line_count = 0
            pending = b""
            while True:
                block = os.read(file_fd, min(64 * 1024, self.budget - total + 1))
                if not block:
                    break
                total += len(block)
                if total > self.budget:
                    reason = "source_budget_exceeded"
                    return
                pending += block
                while True:
                    index = pending.find(b"\n")
                    if index < 0:
                        if len(pending) > MAX_LINE:
                            reason = "source_budget_exceeded"
                            return
                        break
                    line, pending = pending[:index + 1], pending[index + 1:]
                    if len(line) > MAX_LINE:
                        reason = "source_budget_exceeded"
                        return
                    line_count += 1
                    if line_count > MAX_BATCH_LINES:
                        reason = "source_budget_exceeded"
                        return
                    yield line
            after = os.fstat(file_fd)
            if ((after.st_dev, after.st_ino) != (opened.st_dev, opened.st_ino)
                    or (after.st_size, after.st_mtime_ns, after.st_ctime_ns)
                    != (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns)
                    or total != opened.st_size):
                reason = "source_changed"
                return
            if pending:
                reason = "partial_tail"
                return
            reason = None
        except (OSError, ValueError, TypeError, Unavailable):
            reason = "source_read_unavailable"
        finally:
            if file_fd >= 0:
                os.close(file_fd)
            if directory_fd >= 0:
                os.close(directory_fd)
            self.terminal_reason = reason


def _iter_approved_lines(root, relative, budget=MAX_BATCH_BYTES):
    """Stream complete lines from one explicitly approved synthetic/source path."""
    return _ApprovedLineStream(root, relative, budget)


def _path_inside(path, root):
    return path == root or root in path.parents


def _collector_checkout():
    """Resolve only this module's two installed locations, or fail closed."""
    try:
        source = Path(__file__).resolve()
        if source.name != "meter.py":
            return None
        if source.parent.name == "tools":
            return source.parents[1]
        if source.parent.name == "_lib" and len(source.parents) > 3:
            return source.parents[3]
    except (OSError, RuntimeError, ValueError):
        return None
    return None


def _verified_roots(roots):
    checked = []
    try:
        for root in roots:
            path = Path(root)
            if (not path.is_absolute() or any(part in {".", ".."} for part in path.parts)):
                return None
            fd = _open_directory_chain(path)
            os.close(fd)
            resolved = path.resolve(strict=True)
            checked.extend((path, resolved))
    except (OSError, ValueError, TypeError, Unavailable):
        return None
    return checked


def _git_snapshot(lexical, excluded_roots):
    """Hash one trusted executable and capture all identity metadata."""
    try:
        lexical_path = Path(lexical)
        if not lexical_path.is_absolute():
            return None
        resolved = lexical_path.resolve(strict=True)
        if not resolved.is_absolute():
            return None
        roots = _verified_roots(excluded_roots)
        if roots is None:
            return None
        collector = _collector_checkout()
        if collector is None:
            return None
        if (_path_inside(resolved, collector) or _path_inside(lexical_path, collector) or any(
                _path_inside(resolved, root) or _path_inside(lexical_path, root)
                for root in roots)):
            return None
        for ancestor in (resolved, *resolved.parents):
            info = ancestor.stat(follow_symlinks=False)
            if ancestor == resolved:
                if (not stat.S_ISREG(info.st_mode) or info.st_uid != 0
                        or stat.S_IMODE(info.st_mode) & 0o022
                        or not info.st_mode & 0o111):
                    return None
            elif (not stat.S_ISDIR(info.st_mode) or info.st_uid != 0
                    or stat.S_IMODE(info.st_mode) & 0o022):
                return None
        before = resolved.stat(follow_symlinks=False)
        if before.st_size > MAX_GIT_BYTES:
            return None
        fd = os.open(resolved, os.O_RDONLY | os.O_NOFOLLOW)
        try:
            opened = os.fstat(fd)
            if (not stat.S_ISREG(opened.st_mode) or opened.st_uid != 0
                    or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)
                    or opened.st_size > MAX_GIT_BYTES):
                return None
            digest = hashlib.sha256()
            total = 0
            while True:
                block = os.read(fd, min(64 * 1024, MAX_GIT_BYTES + 1 - total))
                if not block:
                    break
                total += len(block)
                if total > MAX_GIT_BYTES:
                    return None
                digest.update(block)
            after = os.fstat(fd)
            if ((after.st_dev, after.st_ino) != (opened.st_dev, opened.st_ino)
                    or (after.st_size, after.st_mtime_ns, after.st_ctime_ns)
                    != (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns)
                    or total != opened.st_size):
                return None
            return {
                "lexical": str(lexical_path), "resolved": str(resolved),
                "dev": opened.st_dev, "ino": opened.st_ino,
                "uid": opened.st_uid, "mode": stat.S_IMODE(opened.st_mode),
                "size": opened.st_size, "mtime_ns": opened.st_mtime_ns,
                "ctime_ns": opened.st_ctime_ns, "sha256": digest.hexdigest(),
            }
        finally:
            os.close(fd)
    except (OSError, ValueError, TypeError, RuntimeError):
        return None


def _trusted_git(excluded_roots):
    """Select Git only from the fixed system path and return its hash record."""
    if not _PRIVATE_FS_SUPPORTED:
        return None, "git_untrusted"
    roots = tuple(excluded_roots) if isinstance(excluded_roots, (list, tuple)) else None
    if roots is None or _verified_roots(roots) is None:
        return None, "git_untrusted"
    found = False
    for directory in os.defpath.split(os.pathsep):
        if not directory or not os.path.isabs(directory):
            continue
        candidate = Path(directory) / "git"
        if not candidate.exists() and not candidate.is_symlink():
            continue
        found = True
        record = _git_snapshot(candidate, roots)
        if record is None:
            return None, "git_untrusted"
        return record, None
    return None, "git_untrusted" if found else "git_unavailable"


def _revalidate_git(record, excluded_roots):
    """Re-resolve, re-stat and re-hash a selected Git executable before launch."""
    if not isinstance(record, dict) or set(record) != {
            "lexical", "resolved", "dev", "ino", "uid", "mode", "size",
            "mtime_ns", "ctime_ns", "sha256"}:
        return False
    current = _git_snapshot(record["lexical"], excluded_roots)
    return current == record


def _kill_git_group(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except (OSError, ProcessLookupError):
        pass
    try:
        process.wait(timeout=GIT_CLEANUP_SECONDS)
    except (OSError, subprocess.TimeoutExpired):
        pass
    for pipe in (process.stdin, process.stdout, process.stderr):
        try:
            if pipe is not None:
                pipe.close()
        except OSError:
            pass


def _fixed_git_tmpdir():
    """Return the verified Darwin system temp path; never consult environment."""
    if sys.platform != "darwin":
        return None
    if not _PRIVATE_FS_SUPPORTED or not hasattr(os, "O_NOFOLLOW"):
        return False
    fd = -1
    try:
        fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        for part in ("private", "tmp"):
            next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                              dir_fd=fd)
            info = os.fstat(next_fd)
            os.close(fd)
            fd = next_fd
            if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0:
                return False
            mode = stat.S_IMODE(info.st_mode)
            if part == "private":
                if mode & 0o022:
                    return False
            elif mode != 0o1777 or not info.st_mode & stat.S_ISVTX:
                return False
        return "/private/tmp"
    except (OSError, ValueError, TypeError):
        return False
    finally:
        if fd >= 0:
            os.close(fd)


def _git_origin_from_config(record, config_bytes, excluded_roots):
    """Run only the fixed Git config query against bounded supplied bytes."""
    if not isinstance(config_bytes, bytes) or len(config_bytes) > MAX_GIT_CONFIG_BYTES:
        return None, "source_budget_exceeded"
    if not _revalidate_git(record, excluded_roots):
        return None, "git_changed"
    argv = [record["resolved"], "config", "--file", "-", "--no-includes",
            "--null", "--get-all", "remote.origin.url"]
    environment = {
        "PATH": os.defpath, "HOME": "/", "LC_ALL": "C", "TZ": "UTC",
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_SYSTEM": "/dev/null",
        "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0", "GIT_NO_LAZY_FETCH": "1", "GIT_PAGER": "",
    }
    fixed_tmpdir = _fixed_git_tmpdir()
    if fixed_tmpdir is False:
        return None, "git_untrusted"
    if fixed_tmpdir is not None:
        environment["TMPDIR"] = fixed_tmpdir
    process = None
    selector = selectors.DefaultSelector()
    output = {"stdout": bytearray(), "stderr": bytearray()}
    limits = {"stdout": MAX_GIT_STDOUT, "stderr": MAX_GIT_STDERR}
    try:
        process = subprocess.Popen(
            argv, cwd="/", env=environment, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
            close_fds=True, start_new_session=True,
        )
        for pipe, name in ((process.stdout, "stdout"), (process.stderr, "stderr")):
            os.set_blocking(pipe.fileno(), False)
            selector.register(pipe, selectors.EVENT_READ, name)
        os.set_blocking(process.stdin.fileno(), False)
        selector.register(process.stdin, selectors.EVENT_WRITE, "stdin")
        sent = 0
        deadline = time.monotonic() + GIT_TIMEOUT_SECONDS
        while selector.get_map() or process.poll() is None:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                _kill_git_group(process)
                return None, "git_timeout"
            for key, _mask in selector.select(min(remaining, 0.1)):
                pipe, name = key.fileobj, key.data
                if name == "stdin":
                    if sent >= len(config_bytes):
                        selector.unregister(pipe)
                        pipe.close()
                        continue
                    try:
                        sent += os.write(pipe.fileno(), config_bytes[sent:sent + 64 * 1024])
                    except (BrokenPipeError, OSError):
                        selector.unregister(pipe)
                        pipe.close()
                    continue
                current = output[name]
                remaining_limit = limits[name] - len(current)
                block = os.read(pipe.fileno(), min(64 * 1024, remaining_limit + 1))
                if not block:
                    selector.unregister(pipe)
                    pipe.close()
                    continue
                if len(block) > remaining_limit:
                    _kill_git_group(process)
                    return None, "git_output_limit"
                current.extend(block)
            if process.poll() is not None:
                stdin_key = next((key for key in selector.get_map().values()
                                  if key.data == "stdin"), None)
                if stdin_key is not None:
                    selector.unregister(stdin_key.fileobj)
                    stdin_key.fileobj.close()
        returncode = process.wait(timeout=1)
        if returncode != 0 or output["stderr"]:
            return None, "git_parser_failed"
        raw = bytes(output["stdout"])
        if not raw.endswith(b"\0") or raw.count(b"\0") != 1 or len(raw) <= 1:
            return None, "project_remote_ambiguous"
        try:
            remote = raw[:-1].decode("utf-8", errors="strict")
            remote = _strip_remote(remote)
        except (UnicodeError, ValueError, TypeError):
            return None, "project_remote_unavailable"
        if len(remote) > 2048:
            return None, "project_remote_unavailable"
        return remote, None
    except (OSError, ValueError, TypeError, subprocess.SubprocessError):
        if process is not None:
            _kill_git_group(process)
        return None, "git_parser_failed"
    finally:
        selector.close()


def _verified_project_remote(project, excluded_roots):
    """Verify only an approved project's direct `.git/config` remote."""
    try:
        if not isinstance(project, dict) or not {"path", "remote"} <= set(project):
            return None, "project_path_unapproved"
        root = Path(project["path"])
        if (not root.is_absolute() or any(part in {".", ".."} for part in root.parts)):
            return None, "project_path_unapproved"
        all_excluded = tuple(excluded_roots) + (str(root),)
        if _verified_roots(all_excluded) is None:
            return None, "git_untrusted"
        project_fd = _open_directory_chain(root)
        project_identity = os.fstat(project_fd)
        git_dir_fd = -1
        config_fd = -1
        try:
            try:
                before_git = os.stat(".git", dir_fd=project_fd, follow_symlinks=False)
            except OSError:
                return None, "project_layout_unsupported"
            if not stat.S_ISDIR(before_git.st_mode):
                return None, "project_layout_unsupported"
            git_dir_fd = os.open(".git", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                 dir_fd=project_fd)
            opened_git = os.fstat(git_dir_fd)
            if (opened_git.st_dev, opened_git.st_ino) != (before_git.st_dev, before_git.st_ino):
                return None, "source_changed"
            try:
                before = os.stat("config", dir_fd=git_dir_fd, follow_symlinks=False)
            except OSError:
                return None, "project_remote_unavailable"
            if not stat.S_ISREG(before.st_mode):
                return None, "project_remote_unavailable"
            config_fd = os.open("config", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=git_dir_fd)
            opened = os.fstat(config_fd)
            if (not stat.S_ISREG(opened.st_mode)
                    or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)):
                return None, "source_changed"
            if opened.st_size > MAX_GIT_CONFIG_BYTES:
                return None, "source_budget_exceeded"
            chunks, size = [], 0
            while True:
                block = os.read(config_fd, min(64 * 1024, MAX_GIT_CONFIG_BYTES + 1 - size))
                if not block:
                    break
                size += len(block)
                if size > MAX_GIT_CONFIG_BYTES:
                    return None, "source_budget_exceeded"
                chunks.append(block)
            after = os.fstat(config_fd)
            named_git = os.stat(".git", dir_fd=project_fd, follow_symlinks=False)
            current_project_fd = _open_directory_chain(root)
            try:
                current_project = os.fstat(current_project_fd)
            finally:
                os.close(current_project_fd)
            if ((after.st_dev, after.st_ino) != (opened.st_dev, opened.st_ino)
                    or (after.st_size, after.st_mtime_ns, after.st_ctime_ns)
                    != (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns)
                    or size != opened.st_size
                    or (named_git.st_dev, named_git.st_ino) != (opened_git.st_dev, opened_git.st_ino)
                    or (current_project.st_dev, current_project.st_ino)
                    != (project_identity.st_dev, project_identity.st_ino)):
                return None, "source_changed"
            config_bytes = b"".join(chunks)
        finally:
            if config_fd >= 0:
                os.close(config_fd)
            if git_dir_fd >= 0:
                os.close(git_dir_fd)
            os.close(project_fd)
        git, reason = _trusted_git(all_excluded)
        if reason:
            return None, reason
        remote, reason = _git_origin_from_config(git, config_bytes, all_excluded)
        if reason:
            return None, reason
        configured = _strip_remote(project["remote"])
        if remote != configured:
            return None, "project_remote_mismatch"
        return remote, None
    except (OSError, ValueError, TypeError, KeyError, Unavailable):
        return None, "project_remote_unavailable"


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
    if payload["source"] not in {"cli", "vscode", "exec", "mcp"}:
        raise ValueError
    if payload.get("thread_source") not in {None, "user"}:
        raise ValueError
    if payload.get("history_mode") not in {"legacy", "paginated"}:
        raise ValueError
    attached = payload.get("attached_thread", False)
    if type(attached) is not bool or attached:
        raise ValueError
    if any(payload.get(field) is not None for field in (
            "forked_from_id", "parent_thread_id", "forked_from_ordinal_exclusive",
            "history_base", "subagent_history_start_ordinal")):
        raise ValueError
    return thread, session


def _codex_context(payload, owner):  # vendor-ok: validate the supported input protocol
    turn = _text(payload["turn_id"])
    root_value = payload.get("root_turn_id")
    root = turn if root_value is None else _text(root_value)
    cwd = payload.get("cwd")
    if cwd is not None:
        cwd = _text(cwd)
        if not cwd.startswith("/") or any(part in {".", ".."} for part in cwd.split("/")):
            raise ValueError
    model = payload.get("model")
    if model is not None:
        model = _safe_alias(model)
    return {"turn": turn, "root": root, "cwd": cwd, "model": model,
            "owner": owner}


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
    if "cache_creation" in data:
        ttl = data["cache_creation"]
        if set(ttl) != {"ephemeral_5m_input_tokens", "ephemeral_1h_input_tokens"}:
            raise ValueError
        if sum(_counter(value) for value in ttl.values()) != kinds["cache_write"]:
            raise ValueError
    return kinds


_EVENT_KIND_NAMES = ("fresh_input", "cache_read", "cache_write", "output")


def _unknown_kinds():
    return {name: None for name in _EVENT_KIND_NAMES}


def _event_record(*, tool, event_key, aliases, thread, session=None, turn=None,
                  root=None, timestamp=None, time_known=False, kinds=None,
                  project_alias=None, project_state="unknown", ownership="unknown",
                  model=None, reasons=()):
    return {
        "event_key": event_key,
        "source_aliases": sorted(set(aliases)),
        "thread_key": _digest(tool, thread) if thread else None,
        "session_key": _digest(tool, session) if session else None,
        "turn_key": _digest(tool, thread, turn) if thread and turn else None,
        "root_turn_key": _digest(tool, thread, root) if thread and root else None,
        "observed_at": timestamp,
        "time_coverage": "known" if time_known else "unknown",
        "kinds": dict(kinds) if kinds is not None else _unknown_kinds(),
        "project_alias": project_alias,
        "project_association": project_state,
        "ownership": ownership,
        "model": model,
        "account": None,
        "reasons": sorted(set(reasons)),
    }


def _merge_normalized_event(existing, incoming):
    """Merge copied responses without choosing between conflicts."""
    existing["source_aliases"] = sorted(set(existing["source_aliases"])
                                        | set(incoming["source_aliases"]))
    existing["reasons"] = sorted(set(existing["reasons"]) | set(incoming["reasons"]))
    if existing["kinds"] != incoming["kinds"]:
        existing["kinds"] = _unknown_kinds()
        existing["reasons"] = sorted(set(existing["reasons"]) | {"conflicting_usage"})
    binding_fields = ("thread_key", "session_key", "turn_key", "root_turn_key",
                      "project_alias", "project_association", "ownership", "model")
    if any(existing[field] != incoming[field] for field in binding_fields):
        existing["session_key"] = None
        existing["turn_key"] = None
        existing["root_turn_key"] = None
        existing["project_alias"] = None
        existing["project_association"] = "unknown"
        existing["ownership"] = "unknown"
        existing["model"] = None
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
                    "event_key", "source_aliases", "thread_key", "session_key", "turn_key",
                    "root_turn_key", "observed_at", "time_coverage", "kinds", "project_alias",
                    "project_association", "ownership", "model", "account", "reasons"}:
                raise ValueError("unsupported normalized event")
            key = event["event_key"]
            if key not in merged:
                merged[key] = {name: (value.copy() if isinstance(value, (dict, list)) else value)
                               for name, value in event.items()}
            else:
                _merge_normalized_event(merged[key], event)
    return list(merged.values())


def read_records(tool, lines, *, config=None, source_aliases=(), source_root=None):
    """Normalize a bounded source batch without exposing raw IDs or paths.

    `lines` may be synthetic bytes or an exhausted `_ApprovedLineStream`. Any
    terminal reader failure invalidates the entire batch. This normalizer is not
    a collector or a ledger input while global coverage remains unknown.
    """
    if tool not in TOOLS:
        raise ValueError("unsupported source")
    issues, contexts, candidates = set(), {}, []
    timing_observations = []
    config_supplied = config is not None
    owner = None
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
                "ownership_coverage": "unknown", "issues": ["invalid_record"]}
    if isinstance(config, dict) and not config["enabled"]:
        return {"schema": READER_VERSION, "tool": tool, "events": [],
                "timing_observations": [], "timing_coverage": "unknown",
                "coverage": "unknown", "identity_coverage": "unknown",
                "ownership_coverage": "unknown", "issues": ["disabled"]}
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
                session = _text(record["sessionId"])
                message_id = _text(message["id"])
                request = record.get("requestId")
                response = _text(request) if request is not None else message_id
                event_key = _digest(tool, session, response, message_id)
                try:
                    kinds = _claude_usage(message["usage"])
                    usage_invalid = False
                except (ValueError, TypeError, KeyError):
                    kinds = _unknown_kinds()
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
                reasons = {"project_path_unapproved"}
                if usage_invalid or model_invalid:
                    reasons.add("invalid_record")
                if account_filter_requested:
                    kinds = _unknown_kinds()
                    reasons.add("account_filter_unproven")
                candidate = _event_record(
                    tool=tool, event_key=event_key, aliases=aliases, thread=session,
                    session=session, timestamp=timestamp, time_known=time_known,
                    kinds=kinds, model=model, reasons=reasons)
                candidates.append((candidate, tuple(candidate["kinds"].items()),
                                   (session, None, None, None), None))
                continue

            payload = record.get("payload")
            if kind == "session_meta":
                try:
                    candidate_owner = _codex_header(payload)
                except (ValueError, TypeError, KeyError, AttributeError):
                    header_eligible = False
                    issues.add("unsupported_or_invalid_session_metadata")
                    continue
                if owner is None:
                    owner = candidate_owner
                elif owner != candidate_owner:
                    owner_conflict = True
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
                context = _codex_context(payload, owner if header_eligible else None)
                turn = context["turn"]
                normalized = (context["root"], context["cwd"], context["model"], context["owner"])
                previous = contexts.get(turn)
                if previous is not None and previous[0] != normalized:
                    contexts[turn] = None
                    issues.add("conflicting_turn_context")
                elif turn not in contexts:
                    contexts[turn] = (normalized, context)
            elif kind == "token_usage_record":
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
                try:
                    # Cumulative snapshots are validated but never charge inputs.
                    _codex_usage(payload["turn_token_usage"])
                    _codex_usage(payload["thread_token_usage"])
                except (ValueError, TypeError, KeyError):
                    reasons.add("snapshot_conflict")
                    issues.add("snapshot_conflict")
                context_entry = contexts.get(turn)
                context = None if context_entry is None else context_entry[1]
                binding_proven = bool(
                    not owner_conflict and header_eligible and owner == (thread, session)
                    and context is not None and context.get("owner") == owner
                    and context.get("turn") == turn and context.get("root") == turn
                    and root == turn)
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
                    reasons.add("account_filter_unproven")
                ownership = "proven" if binding_proven else "unknown"
                if not binding_proven:
                    reasons.add("conflicting_binding")
                candidate = _event_record(
                    tool=tool, event_key=event_key, aliases=aliases, thread=thread,
                    session=session, turn=turn, root=root,
                    timestamp=timestamp, time_known=time_known, kinds=kinds,
                    ownership=ownership, model=model, reasons=reasons)
                candidates.append((candidate, None, None,
                                   (turn, context, project, binding_proven)))
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
            issues.add("invalid_record")

    if isinstance(lines, _ApprovedLineStream) and lines.terminal_reason is not None:
        candidates.clear()
        timing_observations.clear()
        issues.add(lines.terminal_reason)
    if len(candidates) > MAX_NORMALIZED_EVENTS:
        candidates.clear()
        issues.add("source_budget_exceeded")

    merged = {}
    merge_signatures = {}
    for event, usage_signature, binding_signature, details in candidates:
        if details is not None:
            turn, context, project, binding_proven = details
            current = contexts.get(turn)
            if (owner_conflict or not header_eligible or context is None or current is None
                    or current[1] != context):
                event["session_key"] = None
                event["turn_key"] = None
                event["root_turn_key"] = None
                event["project_alias"] = None
                event["project_association"] = "unknown"
                event["ownership"] = "unknown"
                event["model"] = None
                event["reasons"] = sorted(set(event["reasons"]) | {"conflicting_binding"})
            elif binding_proven and project is not None:
                if account_filter_requested:
                    event["reasons"] = sorted(set(event["reasons"]) | {"account_filter_unproven"})
                else:
                    project_cache_key = (project.get("alias"), project.get("path"))
                    if project_cache_key not in verified_projects:
                        verified_projects[project_cache_key] = _verified_project_remote(
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
            if creation_remote_conflict and project is not None:
                event["project_alias"] = None
                event["project_association"] = "unknown"
                event["reasons"] = sorted(set(event["reasons"]) | {"project_remote_mismatch"})
            usage_signature = tuple(event["kinds"].items())
            binding_signature = (event["thread_key"], event["session_key"],
                                 event["turn_key"], event["root_turn_key"],
                                 event["project_alias"], event["project_association"],
                                 event["ownership"], event["model"])
        else:
            usage_signature = tuple(event["kinds"].items())
            binding_signature = (event["thread_key"], event["session_key"],
                                 event["turn_key"], event["root_turn_key"],
                                 event["project_alias"], event["project_association"],
                                 event["ownership"], event["model"])
        key = event["event_key"]
        if key not in merged:
            merged[key] = event
            merge_signatures[key] = (usage_signature, binding_signature)
            continue
        prior_usage, prior_binding = merge_signatures[key]
        _merge_normalized_event(merged[key], event)
        if prior_usage != usage_signature:
            merged[key]["kinds"] = _unknown_kinds()
            merged[key]["reasons"] = sorted(set(merged[key]["reasons"]) | {"conflicting_usage"})
        if prior_binding != binding_signature:
            merged[key]["session_key"] = None
            merged[key]["turn_key"] = None
            merged[key]["root_turn_key"] = None
            merged[key]["project_alias"] = None
            merged[key]["project_association"] = "unknown"
            merged[key]["ownership"] = "unknown"
            merged[key]["model"] = None
            merged[key]["reasons"] = sorted(set(merged[key]["reasons"]) | {"conflicting_binding"})
        merge_signatures[key] = (prior_usage, prior_binding)

    normalized = list(merged.values())
    if not normalized and not issues:
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
        home = _fixed_user_home()
        config = load_config(home / ".cairn" / "meter.json")
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
