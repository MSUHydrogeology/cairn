#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Bounded, offline reads through the operator's host Git executable.

This is a small private implementation helper. Callers supply fixed read forms
and interpret ``ReadResult`` using their own absence/failure policy. It does
not authenticate Git, freeze a repository, or provide a sandbox.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import selectors
import signal
import stat
import subprocess
import sys
import threading
import time
from typing import NamedTuple


HELPER_MAX_BYTES = 256 * 1024
EXECUTABLE_MAX_BYTES = 512 * 1024 * 1024
VERSION_MAX_BYTES = 256
CONFIG_MAX_BYTES = 256 * 1024
ROOTS_MAX_BYTES = 64 * 1024
OUTPUT_MAX_BYTES = 8 * 1024 * 1024
HISTORY_MAX_BYTES = 64 * 1024 * 1024
STDERR_MAX_BYTES = 64 * 1024
DEFAULT_TIMEOUT_SECONDS = 10.0
CLEANUP_SECONDS = 2.0
_MAX_ARG_BYTES = 1024 * 1024
_MAX_REQUEST_BYTES = 2 * 1024 * 1024
_MAX_ANCESTORS = 512
_READ_COMMANDS = frozenset({
    "config", "diff", "diff-index", "diff-tree", "for-each-ref",
    "ls-files", "ls-tree", "log", "rev-parse", "rev-list", "show",
    "status", "cat-file", "describe",
})
_OLD_GIT_COMMANDS = frozenset({"config", "for-each-ref", "ls-files", "rev-parse"})
_FORBIDDEN_ARGS = (
    "--exec-path", "--upload-pack", "--receive-pack", "--config-env",
    "--ext-diff", "--textconv", "--work-tree",
)
_VERSION_CACHE: dict[tuple[object, ...], tuple[tuple[int, int, int], bytes]] = {}
_VERSION_LOCK = threading.Lock()
_VERIFIED_SOURCE: bytes | None = None
_VERIFIED_SHA256: str | None = None
_WINDOWS_JOB_HANDLE = None


class GitReadError(RuntimeError):
    """Fixed local reason for an unavailable or incomplete read."""


class ReadResult(NamedTuple):
    state: str
    returncode: int | None
    stdout: bytes
    reason: str | None = None


class _Snapshot(NamedTuple):
    lexical: str
    resolved: str
    identity: tuple[int, int]
    size: int
    mtime_ns: int
    ctime_ns: int
    mode: int
    digest: str


def _stat_key(info: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (int(info.st_dev), int(info.st_ino), int(info.st_mode),
            int(info.st_size), int(info.st_mtime_ns), int(info.st_ctime_ns))


def _is_reparse(info: os.stat_result) -> bool:
    return bool(getattr(info, "st_file_attributes", 0) & 0x400)


def _absolute(path: str | os.PathLike[str]) -> str:
    value = os.fspath(path)
    if not isinstance(value, str) or not value or "\x00" in value:
        raise GitReadError("invalid-path")
    if not os.path.isabs(value):
        raise GitReadError("path-not-absolute")
    return os.path.normpath(value)


def _component_chain(path: str) -> list[str]:
    """Return an absolute path and its parents, without following links."""
    absolute = _absolute(path)
    drive, tail = os.path.splitdrive(absolute)
    if os.name == "nt":
        current = drive + os.sep
        parts = [part for part in tail.replace("/", "\\").split("\\") if part]
        result = [current]
        for part in parts:
            current = os.path.join(current, part)
            result.append(current)
    else:
        result = [os.sep]
        current = os.sep
        for part in tail.split(os.sep):
            if part:
                current = os.path.join(current, part)
                result.append(current)
    if len(result) > _MAX_ANCESTORS:
        raise GitReadError("path-depth-limit")
    return result


def _lstat_chain(path: str, *, leaf_regular: bool = False,
                 allow_leaf_link: bool = False,
                 allow_path_links: bool = False) -> list[os.stat_result]:
    names = _component_chain(path)
    rows: list[os.stat_result] = []
    for index, name in enumerate(names):
        try:
            info = os.lstat(name)
        except OSError:
            raise GitReadError("path-component-unavailable") from None
        linked = stat.S_ISLNK(info.st_mode) or _is_reparse(info)
        if (linked and not allow_path_links
                and not (allow_leaf_link and index == len(names) - 1)):
            raise GitReadError("linked-path-component")
        target_info = info
        if linked and allow_path_links:
            try:
                target_info = os.stat(name)
            except OSError:
                raise GitReadError("linked-path-unavailable") from None
        if index < len(names) - 1 and not stat.S_ISDIR(target_info.st_mode):
            raise GitReadError("nondirectory-path-parent")
        if (index == len(names) - 1 and leaf_regular
                and not stat.S_ISREG(target_info.st_mode)):
            raise GitReadError("not-regular-file")
        rows.append(info)
    return rows


def _checked_bytes(path: str, limit: int) -> tuple[bytes, tuple[int, int, int, int, int, int],
                                                    tuple[tuple[int, int, int, int, int, int], ...]]:
    before_chain = _lstat_chain(path, leaf_regular=True)
    before = before_chain[-1]
    if before.st_size < 0 or before.st_size > limit:
        raise GitReadError("file-size-limit")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        fd = os.open(path, flags)
    except OSError:
        raise GitReadError("file-open-failed") from None
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode) or _stat_key(opened) != _stat_key(before):
            raise GitReadError("file-identity-changed")
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining:
            part = os.read(fd, min(65536, remaining))
            if not part:
                break
            chunks.append(part)
            remaining -= len(part)
        data = b"".join(chunks)
        after = os.fstat(fd)
        after_chain = _lstat_chain(path, leaf_regular=True)
        if (_stat_key(after) != _stat_key(opened)
                or tuple(_stat_key(row) for row in after_chain)
                != tuple(_stat_key(row) for row in before_chain)):
            raise GitReadError("file-changed-during-read")
        if len(data) != opened.st_size or len(data) > limit:
            raise GitReadError("file-size-changed")
        return data, _stat_key(after), tuple(_stat_key(row) for row in after_chain)
    finally:
        os.close(fd)


def _checked_digest(path: str, limit: int) -> tuple[tuple[int, int, int, int, int, int], str]:
    """Hash a bounded executable without retaining hundreds of MiB in memory."""
    before_chain = _lstat_chain(path, leaf_regular=True)
    before = before_chain[-1]
    if before.st_size < 0 or before.st_size > limit:
        raise GitReadError("executable-size-limit")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        fd = os.open(path, flags)
    except OSError:
        raise GitReadError("executable-open-failed") from None
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode) or _stat_key(opened) != _stat_key(before):
            raise GitReadError("executable-identity-changed")
        digest = hashlib.sha256()
        total = 0
        while True:
            part = os.read(fd, 65536)
            if not part:
                break
            total += len(part)
            if total > limit:
                raise GitReadError("executable-size-limit")
            digest.update(part)
        after = os.fstat(fd)
        after_chain = _lstat_chain(path, leaf_regular=True)
        if (_stat_key(after) != _stat_key(opened)
                or tuple(_stat_key(row) for row in after_chain)
                != tuple(_stat_key(row) for row in before_chain)
                or total != after.st_size):
            raise GitReadError("executable-changed-during-read")
        return _stat_key(after), digest.hexdigest()
    finally:
        os.close(fd)


def load_verified_module(path: str | os.PathLike[str], expected_sha256: str,
                         module_name: str):
    """Execute only the single-read buffer that matches a caller-owned pin.

    Trusted first importers must provide the literal pin from their reviewed
    bytes. This routine never inserts or reuses a ``sys.modules`` entry.
    """
    if (not isinstance(expected_sha256, str) or len(expected_sha256) != 64
            or any(char not in "0123456789abcdef" for char in expected_sha256)):
        raise GitReadError("invalid-helper-pin")
    source_path = _absolute(path)
    data, _identity, _chain = _checked_bytes(source_path, HELPER_MAX_BYTES)
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected_sha256:
        raise GitReadError("helper-pin-mismatch")
    import types
    module = types.ModuleType(module_name)
    module.__file__ = source_path
    module.__package__ = ""
    module.__verified_source__ = data
    module.__verified_sha256__ = expected_sha256
    try:
        code = compile(data, source_path, "exec", dont_inherit=True)
        exec(code, module.__dict__)
    except BaseException:
        raise GitReadError("helper-execution-failed") from None
    module._VERIFIED_SOURCE = data
    module._VERIFIED_SHA256 = expected_sha256
    return module


def _path_identity(path: str) -> tuple[str, str]:
    lexical = _absolute(path)
    try:
        resolved = os.path.realpath(lexical, strict=True)
        info = os.stat(resolved, follow_symlinks=False)
    except (OSError, TypeError):
        raise GitReadError("executable-unavailable") from None
    if not stat.S_ISREG(info.st_mode) or _is_reparse(info):
        raise GitReadError("executable-not-regular")
    if os.name != "nt" and not (info.st_mode & 0o111):
        raise GitReadError("executable-not-executable")
    return lexical, os.path.normpath(resolved)


def _under(path: str, root: str) -> bool:
    path = os.path.normcase(os.path.normpath(path))
    root = os.path.normcase(os.path.normpath(root))
    try:
        return os.path.commonpath((path, root)) == root
    except ValueError:
        return False


def worktree_exclusions(target: str | os.PathLike[str]) -> tuple[str, ...]:
    """Discover enclosing worktree/bare-repository roots before Git executes."""
    lexical_target = _absolute(target)
    try:
        resolved_target = os.path.realpath(lexical_target, strict=True)
        os.stat(resolved_target)
    except OSError:
        raise GitReadError("target-path-unavailable") from None
    roots: set[str] = set()
    paths = tuple(dict.fromkeys((lexical_target, resolved_target)))
    for value in paths:
        try:
            info = os.stat(value)
            start = value if stat.S_ISDIR(info.st_mode) else os.path.dirname(value)
        except OSError:
            raise GitReadError("target-path-unavailable") from None
        chain = _component_chain(start)
        for directory in reversed(chain):
            try:
                marker = os.path.join(directory, ".git")
                try:
                    os.lstat(marker)
                    roots.add(os.path.normcase(os.path.abspath(directory)))
                    roots.add(os.path.normcase(os.path.realpath(directory)))
                except FileNotFoundError:
                    pass
                except OSError:
                    raise GitReadError("repository-marker-unreadable") from None
                present = []
                for name in ("HEAD", "config", "objects", "refs"):
                    try:
                        os.lstat(os.path.join(directory, name))
                        present.append(name)
                    except FileNotFoundError:
                        pass
                    except OSError:
                        raise GitReadError("repository-marker-unreadable") from None
                if len(present) == 4:
                    roots.add(os.path.normcase(os.path.abspath(directory)))
                    roots.add(os.path.normcase(os.path.realpath(directory)))
            except GitReadError:
                raise
    return tuple(sorted(roots))


def _assert_off_target(lexical: str, resolved: str, exclusions: tuple[str, ...]) -> None:
    for candidate in (lexical, resolved):
        for root in exclusions:
            if _under(candidate, root):
                raise GitReadError("git-inside-inspected-repository")


def _snapshot_executable(path: str) -> _Snapshot:
    lexical, resolved = _path_identity(path)
    before_chain = _lstat_chain(lexical, leaf_regular=True, allow_path_links=True)
    # The resolved target is opened directly: symlinked PATH entries are
    # allowed only when both spellings remain stable and outside the target.
    identity_key, digest = _checked_digest(resolved, EXECUTABLE_MAX_BYTES)
    current_resolved = os.path.realpath(lexical, strict=True)
    current_chain = _lstat_chain(lexical, leaf_regular=True, allow_path_links=True)
    if (os.path.normcase(current_resolved) != os.path.normcase(resolved)
            or tuple(_stat_key(row) for row in current_chain)
            != tuple(_stat_key(row) for row in before_chain)):
        raise GitReadError("executable-path-changed")
    info = os.stat(resolved, follow_symlinks=False)
    if (int(info.st_dev), int(info.st_ino)) != (identity_key[0], identity_key[1]):
        raise GitReadError("executable-identity-changed")
    return _Snapshot(lexical, resolved, (identity_key[0], identity_key[1]),
                     identity_key[3], identity_key[4], identity_key[5], identity_key[2],
                     digest)


def select_git(target: str | os.PathLike[str], path_value: str | None = None) -> _Snapshot | None:
    """Select the first absolute PATH Git executable, after exclusion discovery."""
    exclusions = worktree_exclusions(target)
    if path_value is None:
        path_value = os.environ.get("PATH", "")
    if not isinstance(path_value, str) or "\x00" in path_value:
        raise GitReadError("invalid-path-environment")
    leaf = "git.exe" if os.name == "nt" else "git"
    for entry in path_value.split(os.pathsep):
        if not entry or not os.path.isabs(entry):
            continue
        candidate = os.path.join(entry, leaf)
        if not os.path.lexists(candidate):
            continue
        lexical, resolved = _path_identity(candidate)
        _assert_off_target(lexical, resolved, exclusions)
        return _snapshot_executable(lexical)
    return None


def _snapshot_still_matches(snapshot: _Snapshot) -> bool:
    current = _snapshot_executable(snapshot.lexical)
    return current == snapshot


def _base_environment() -> dict[str, str]:
    env = {
        "PATH": "",
        "LC_ALL": "C",
        "LANG": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_PROTOCOL_FROM_USER": "0",
        "GIT_ALLOW_PROTOCOL": "",
        "GIT_PAGER": "",
        "GIT_CONFIG_COUNT": "15",
        "GIT_CONFIG_KEY_0": "protocol.allow",
        "GIT_CONFIG_VALUE_0": "never",
        "GIT_CONFIG_KEY_1": "core.hooksPath",
        "GIT_CONFIG_VALUE_1": os.devnull,
        "GIT_CONFIG_KEY_2": "core.fsmonitor",
        "GIT_CONFIG_VALUE_2": "false",
        "GIT_CONFIG_KEY_3": "core.pager",
        "GIT_CONFIG_VALUE_3": "",
        "GIT_CONFIG_KEY_4": "color.ui",
        "GIT_CONFIG_VALUE_4": "false",
        "GIT_CONFIG_KEY_5": "log.showSignature",
        "GIT_CONFIG_VALUE_5": "false",
        "GIT_CONFIG_KEY_6": "diff.external",
        "GIT_CONFIG_VALUE_6": "",
        "GIT_CONFIG_KEY_7": "diff.textconv",
        "GIT_CONFIG_VALUE_7": "false",
        "GIT_CONFIG_KEY_8": "protocol.file.allow",
        "GIT_CONFIG_VALUE_8": "never",
        "GIT_CONFIG_KEY_9": "protocol.git.allow",
        "GIT_CONFIG_VALUE_9": "never",
        "GIT_CONFIG_KEY_10": "protocol.ssh.allow",
        "GIT_CONFIG_VALUE_10": "never",
        "GIT_CONFIG_KEY_11": "protocol.http.allow",
        "GIT_CONFIG_VALUE_11": "never",
        "GIT_CONFIG_KEY_12": "protocol.https.allow",
        "GIT_CONFIG_VALUE_12": "never",
        "GIT_CONFIG_KEY_13": "protocol.ftp.allow",
        "GIT_CONFIG_VALUE_13": "never",
        "GIT_CONFIG_KEY_14": "protocol.ext.allow",
        "GIT_CONFIG_VALUE_14": "never",
    }
    if os.name == "nt":
        root = os.environ.get("SystemRoot") or os.environ.get("WINDIR")
        if root and os.path.isabs(root):
            env["SystemRoot"] = root
            env["WINDIR"] = root
    return env


def _neutral_cwd(target: str) -> str:
    if os.name == "nt":
        root = os.environ.get("SystemRoot") or os.environ.get("WINDIR")
        if not root or not os.path.isabs(root):
            raise GitReadError("neutral-working-directory-unavailable")
        cwd = os.path.join(root, "System32")
    else:
        cwd = os.sep
    try:
        info = os.stat(cwd)
    except OSError:
        raise GitReadError("neutral-working-directory-unavailable") from None
    if not stat.S_ISDIR(info.st_mode):
        raise GitReadError("neutral-working-directory-unavailable")
    _lstat_chain(cwd)
    resolved = os.path.realpath(cwd)
    _assert_off_target(cwd, resolved, worktree_exclusions(target))
    return cwd


def _argv(snapshot: _Snapshot, target: str, args: tuple[str, ...],
          config_overrides: tuple[tuple[str, str], ...] = ()) -> list[str]:
    if not args or args[0] not in _READ_COMMANDS:
        raise GitReadError("unsupported-read-form")
    if any(not isinstance(item, str) or "\x00" in item for item in args):
        raise GitReadError("invalid-read-argument")
    if sum(len(item.encode("utf-8", "surrogatepass")) + 1 for item in args) > _MAX_ARG_BYTES:
        raise GitReadError("argument-size-limit")
    for item in args:
        if any(item == option or item.startswith(option + "=") for option in _FORBIDDEN_ARGS):
            raise GitReadError("forbidden-read-option")
    version = _git_version(snapshot, target)
    if version is None:
        raise GitReadError("git-version-unavailable")
    if version < (2, 45, 0) and args[0] not in _OLD_GIT_COMMANDS:
        raise GitReadError("git-version-below-read-floor")
    overrides = [
        "--no-optional-locks", "-c", "protocol.allow=never",
        "-c", "protocol.file.allow=never", "-c", "core.hooksPath=" + os.devnull,
        "-c", "core.fsmonitor=false", "-c", "core.pager=", "-c", "color.ui=false",
        "-c", "log.showSignature=false", "-c", "diff.external=",
        "-c", "diff.textconv=false", "--no-replace-objects",
    ]
    for key, value in config_overrides:
        overrides.extend(("-c", key + "=" + value))
    result = [snapshot.resolved, "--no-pager", "-C", target, *overrides]
    result.append(args[0])
    if args[0] in {"diff", "diff-index", "diff-tree", "show"}:
        result.extend(("--no-ext-diff", "--no-textconv"))
    result.extend(args[1:])
    return result


def _filter_config_overrides(output: bytes) -> tuple[tuple[str, str], ...]:
    """Turn expanded filter-driver config names into command-precedence disables."""
    drivers: set[str] = set()
    for record in output.split(b"\x00"):
        if not record:
            continue
        if b"\n" not in record:
            raise GitReadError("filter-config-unparseable")
        raw_key, _raw_value = record.split(b"\n", 1)
        try:
            key = raw_key.decode("ascii").lower()
        except UnicodeError:
            raise GitReadError("filter-config-unparseable") from None
        if not key.startswith("filter."):
            continue
        for suffix in (".clean", ".smudge", ".process", ".required"):
            if key.endswith(suffix):
                name = key[len("filter."):-len(suffix)]
                if not name or not re.fullmatch(r"[a-z0-9._-]+", name):
                    raise GitReadError("filter-name-unrepresentable")
                drivers.add(name)
                break
    rows: list[tuple[str, str]] = []
    for driver in sorted(drivers):
        rows.extend((f"filter.{driver}.clean", ""),
                    (f"filter.{driver}.smudge", ""),
                    (f"filter.{driver}.process", ""),
                    (f"filter.{driver}.required", "false"))
    return tuple(rows)


def _parse_version(output: bytes) -> tuple[int, int, int] | None:
    try:
        text = output.decode("ascii").strip()
    except UnicodeError:
        return None
    prefix = "git version "
    if not text.startswith(prefix):
        return None
    raw = text[len(prefix):].split(".")
    if len(raw) < 3:
        return None
    values = []
    for part in raw[:3]:
        digits = ""
        for char in part:
            if not char.isdigit():
                break
            digits += char
        if not digits:
            return None
        values.append(int(digits))
    return tuple(values)  # type: ignore[return-value]


def _worker_job() -> None:
    """Install the existing kill-on-close Windows Job pattern in this worker."""
    global _WINDOWS_JOB_HANDLE
    if os.name != "nt":
        return
    import ctypes as C
    from ctypes import wintypes as W
    if C.sizeof(C.c_void_p) != 8:
        raise GitReadError("windows-worker-abi-unavailable")

    class BASIC(C.Structure):
        _fields_ = [("process_time", C.c_int64), ("job_time", C.c_int64),
                    ("flags", W.DWORD), ("minimum", C.c_size_t),
                    ("maximum", C.c_size_t), ("processes", W.DWORD),
                    ("affinity", C.c_size_t), ("priority", W.DWORD),
                    ("scheduling", W.DWORD)]

    class IO(C.Structure):
        _fields_ = [(name, C.c_uint64) for name in
                    ("read_ops", "write_ops", "other_ops", "read_bytes",
                     "write_bytes", "other_bytes")]

    class EXTENDED(C.Structure):
        _fields_ = [("basic", BASIC), ("io", IO), ("process_memory", C.c_size_t),
                    ("job_memory", C.c_size_t), ("peak_process_memory", C.c_size_t),
                    ("peak_job_memory", C.c_size_t)]

    if C.sizeof(BASIC) != 64 or C.sizeof(EXTENDED) != 144:
        raise GitReadError("windows-worker-abi-unavailable")
    try:
        kernel = C.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
        kernel.CreateJobObjectW.argtypes = [C.c_void_p, W.LPCWSTR]
        kernel.CreateJobObjectW.restype = C.c_void_p
        kernel.SetInformationJobObject.argtypes = [C.c_void_p, C.c_int, C.c_void_p, W.DWORD]
        kernel.SetInformationJobObject.restype = W.BOOL
        kernel.AssignProcessToJobObject.argtypes = [C.c_void_p, C.c_void_p]
        kernel.AssignProcessToJobObject.restype = W.BOOL
        kernel.GetCurrentProcess.argtypes = []
        kernel.GetCurrentProcess.restype = C.c_void_p
        kernel.CloseHandle.argtypes = [C.c_void_p]
        kernel.CloseHandle.restype = W.BOOL
    except (AttributeError, OSError):
        raise GitReadError("windows-job-api-unavailable") from None
    handle = kernel.CreateJobObjectW(None, None)
    if not handle:
        raise GitReadError("windows-job-create-failed")
    limits = EXTENDED()
    limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    if (not kernel.SetInformationJobObject(handle, 9, C.byref(limits), C.sizeof(limits))
            or not kernel.AssignProcessToJobObject(handle, kernel.GetCurrentProcess())):
        kernel.CloseHandle(handle)
        raise GitReadError("windows-job-install-failed")
    _WINDOWS_JOB_HANDLE = (kernel, handle)


def _capture_process(argv: list[str], env: dict[str, str], cwd: str,
                     timeout: float, stdout_limit: int, stderr_limit: int,
                     snapshot: _Snapshot, target: str) -> ReadResult:
    if os.name == "nt":
        return _capture_windows_git(argv, env, cwd, timeout, stdout_limit, stderr_limit,
                                    snapshot, target)
    if (os.name != "posix" or not hasattr(os, "waitid")
            or not all(hasattr(os, name) for name in ("P_PID", "WEXITED", "WNOHANG", "WNOWAIT"))):
        raise GitReadError("safe-process-supervision-unavailable")
    return _capture_posix_git(argv, env, cwd, timeout, stdout_limit, stderr_limit)


def _capture_posix_git(argv: list[str], env: dict[str, str], cwd: str,
                       timeout: float, stdout_limit: int, stderr_limit: int) -> ReadResult:
    try:
        process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=False, start_new_session=True, close_fds=True)
    except OSError:
        raise GitReadError("git-start-failed") from None
    assert process.stdout is not None and process.stderr is not None
    selector = selectors.DefaultSelector()
    streams = {process.stdout: bytearray(), process.stderr: bytearray()}
    limits = {process.stdout: stdout_limit, process.stderr: stderr_limit}
    for stream in streams:
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ)
    deadline = time.monotonic() + timeout
    cleanup_deadline: float | None = None
    leader_seen = False
    failed = False
    code: int | None = None
    group_id = process.pid
    try:
        while selector.get_map() or not leader_seen:
            now = time.monotonic()
            if not leader_seen:
                try:
                    observed = os.waitid(os.P_PID, process.pid,
                                         os.WEXITED | os.WNOHANG | os.WNOWAIT)
                except (ChildProcessError, OSError):
                    failed = True
                    observed = None
                if observed is not None and observed.si_pid:
                    leader_seen = True
                    try:
                        os.killpg(group_id, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    except OSError:
                        failed = True
                    cleanup_deadline = now + CLEANUP_SECONDS
            if not leader_seen and now >= deadline:
                failed = True
                try:
                    os.killpg(group_id, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                except OSError:
                    failed = True
                cleanup_deadline = now + CLEANUP_SECONDS
                # Do not continue waiting for a normal leader exit.
                deadline = float("inf")
            if cleanup_deadline is not None and now >= cleanup_deadline:
                failed = True
                break
            events = selector.select(0.05)
            for key, _mask in events:
                stream = key.fileobj
                try:
                    chunk = os.read(stream.fileno(), 65536)
                except BlockingIOError:
                    continue
                except OSError:
                    failed = True
                    selector.unregister(stream)
                    continue
                if not chunk:
                    selector.unregister(stream)
                    continue
                buffer = streams[stream]
                limit = limits[stream]
                if len(buffer) + len(chunk) > limit:
                    failed = True
                    try:
                        os.killpg(group_id, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    except OSError:
                        failed = True
                    cleanup_deadline = time.monotonic() + CLEANUP_SECONDS
                    # Keep no over-limit bytes.
                    continue
                buffer.extend(chunk)
        if not leader_seen:
            try:
                os.killpg(group_id, signal.SIGKILL)
            except OSError:
                pass
        remaining_cleanup = (CLEANUP_SECONDS if cleanup_deadline is None else
                             max(0.0, cleanup_deadline - time.monotonic()))
        try:
            code = process.wait(timeout=remaining_cleanup)
        except subprocess.TimeoutExpired:
            failed = True
            try:
                os.killpg(group_id, signal.SIGKILL)
            except OSError:
                pass
            code = None
    finally:
        selector.close()
        process.stdout.close()
        process.stderr.close()
    if failed or code is None:
        return ReadResult("failed", code, b"", "process-or-cleanup-incomplete")
    return ReadResult("completed", code, bytes(streams[process.stdout]))


_WINDOWS_BOOTSTRAP = r'''
import base64, hashlib, json, sys, types
raw = sys.stdin.buffer.read(2097153)
if len(raw) > 2097152:
    sys.stdout.buffer.write(b"{\"state\":\"failed\",\"returncode\":null,\"stdout\":\"\"}")
    raise SystemExit(2)
try:
    request = json.loads(raw.decode("ascii"))
    source = base64.b64decode(request["source"], validate=True)
    expected = request["pin"]
    if hashlib.sha256(source).hexdigest() != expected:
        raise ValueError
    module = types.ModuleType("_cairn_verified_git_read_worker")
    module.__file__ = "<verified git_read buffer>"
    module.__verified_source__ = source
    module.__verified_sha256__ = expected
    exec(compile(source, module.__file__, "exec", dont_inherit=True), module.__dict__)
    result = module._windows_worker_run(request)
    message = {"state": result.state, "returncode": result.returncode,
               "stdout": base64.b64encode(result.stdout).decode("ascii")}
    sys.stdout.buffer.write(json.dumps(message, separators=(",", ":")).encode("ascii"))
    sys.stdout.buffer.flush()
except BaseException:
    sys.stdout.buffer.write(b"{\"state\":\"failed\",\"returncode\":null,\"stdout\":\"\"}")
    sys.stdout.buffer.flush()
    raise SystemExit(2)
'''


class _Collector:
    def __init__(self, stream, cap: int):
        self.stream = stream
        self.cap = cap
        self.data = bytearray()
        self.overflow = threading.Event()
        self.done = threading.Event()
        self.error = threading.Event()

    def drain(self) -> None:
        try:
            while True:
                try:
                    part = self.stream.read(65536)
                except OSError:
                    self.error.set()
                    return
                if not part:
                    return
                if len(self.data) + len(part) > self.cap:
                    self.overflow.set()
                    return
                self.data.extend(part)
        finally:
            self.done.set()


def _join_until(threads: tuple[threading.Thread, ...], deadline: float) -> bool:
    for thread in threads:
        thread.join(max(0.0, deadline - time.monotonic()))
    return all(not thread.is_alive() for thread in threads)


def _capture_windows_git(argv: list[str], env: dict[str, str], cwd: str,
                         timeout: float, stdout_limit: int, stderr_limit: int,
                         snapshot: _Snapshot, target: str) -> ReadResult:
    source = _VERIFIED_SOURCE
    pin = _VERIFIED_SHA256
    if source is None or pin is None or hashlib.sha256(source).hexdigest() != pin:
        raise GitReadError("verified-helper-buffer-unavailable")
    request = {
        "source": base64.b64encode(source).decode("ascii"), "pin": pin,
        "argv": argv, "env": env, "cwd": cwd, "timeout": timeout,
        "stdout_limit": stdout_limit, "stderr_limit": stderr_limit,
        "target": target,
        "snapshot": [snapshot.lexical, snapshot.resolved, list(snapshot.identity),
                     snapshot.size, snapshot.mtime_ns, snapshot.ctime_ns,
                     snapshot.mode, snapshot.digest],
    }
    payload = json.dumps(request, ensure_ascii=True, separators=(",", ":")).encode("ascii")
    if len(payload) > _MAX_REQUEST_BYTES:
        raise GitReadError("worker-request-size-limit")
    interpreter = os.path.realpath(sys.executable, strict=True)
    snapshot = _snapshot_executable(interpreter)
    _assert_off_target(snapshot.lexical, snapshot.resolved,
                       worktree_exclusions(target))
    if not _snapshot_still_matches(snapshot):
        raise GitReadError("worker-interpreter-changed")
    worker_env = {"PATH": "", "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    system_root = env.get("SystemRoot")
    if system_root:
        worker_env["SystemRoot"] = system_root
        worker_env["WINDIR"] = system_root
    try:
        worker = subprocess.Popen(
            [snapshot.resolved, "-I", "-S", "-B", "-c", _WINDOWS_BOOTSTRAP],
            cwd=cwd, env=worker_env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=False, close_fds=True)
    except OSError:
        raise GitReadError("worker-start-failed") from None
    assert worker.stdin is not None and worker.stdout is not None and worker.stderr is not None
    reply_limit = ((stdout_limit + 2) // 3) * 4 + 4096
    out_collector = _Collector(worker.stdout, reply_limit)
    err_collector = _Collector(worker.stderr, STDERR_MAX_BYTES)
    out_thread = threading.Thread(target=out_collector.drain, daemon=True)
    err_thread = threading.Thread(target=err_collector.drain, daemon=True)
    out_thread.start()
    err_thread.start()
    failed = False
    try:
        worker.stdin.write(payload)
        worker.stdin.flush()
    except OSError:
        failed = True
    finally:
        worker.stdin.close()
    deadline = time.monotonic() + timeout + CLEANUP_SECONDS
    while worker.poll() is None:
        if time.monotonic() >= deadline or out_collector.overflow.is_set() \
                or err_collector.overflow.is_set():
            failed = True
            worker.kill()
            break
        time.sleep(0.02)
    try:
        worker.wait(timeout=CLEANUP_SECONDS)
    except subprocess.TimeoutExpired:
        failed = True
        worker.kill()
        try:
            worker.wait(timeout=CLEANUP_SECONDS)
        except subprocess.TimeoutExpired:
            pass
    reader_deadline = time.monotonic() + CLEANUP_SECONDS
    readers = (out_thread, err_thread)
    if not _join_until(readers, reader_deadline):
        failed = True
    if (out_thread.is_alive() or err_thread.is_alive()
            or not out_collector.done.is_set() or not err_collector.done.is_set()):
        failed = True
    if out_collector.error.is_set() or err_collector.error.is_set():
        failed = True
    worker.stdout.close()
    worker.stderr.close()
    if not _join_until(readers, reader_deadline):
        failed = True
    if failed or out_collector.overflow.is_set() or err_collector.overflow.is_set():
        return ReadResult("failed", worker.returncode, b"", "worker-incomplete")
    try:
        reply = json.loads(bytes(out_collector.data).decode("ascii"))
        data = base64.b64decode(reply["stdout"], validate=True)
        if len(data) > stdout_limit:
            raise ValueError
        if reply["state"] != "completed":
            return ReadResult("failed", reply.get("returncode"), b"", "worker-incomplete")
        return ReadResult("completed", reply.get("returncode"), data)
    except (ValueError, UnicodeError, KeyError, json.JSONDecodeError):
        return ReadResult("failed", worker.returncode, b"", "worker-incomplete")


def _windows_worker_run(request: dict[str, object]) -> ReadResult:
    try:
        _worker_job()
        argv = request["argv"]
        env = request["env"]
        cwd = request["cwd"]
        timeout = request["timeout"]
        stdout_limit = request["stdout_limit"]
        stderr_limit = request["stderr_limit"]
        target = request["target"]
        raw_snapshot = request["snapshot"]
        if (not isinstance(argv, list) or any(not isinstance(item, str) for item in argv)
                or not isinstance(env, dict) or any(not isinstance(k, str) or not isinstance(v, str)
                                                      for k, v in env.items())
                or not isinstance(cwd, str) or not isinstance(timeout, (int, float))
                or not isinstance(stdout_limit, int) or not isinstance(stderr_limit, int)
                or not isinstance(target, str) or not isinstance(raw_snapshot, list)
                or len(raw_snapshot) != 8):
            raise GitReadError("worker-request-invalid")
        snapshot = _Snapshot(raw_snapshot[0], raw_snapshot[1], tuple(raw_snapshot[2]),
                             raw_snapshot[3], raw_snapshot[4], raw_snapshot[5],
                             raw_snapshot[6], raw_snapshot[7])
        _assert_off_target(snapshot.lexical, snapshot.resolved,
                           worktree_exclusions(target))
        if not _snapshot_still_matches(snapshot):
            raise GitReadError("executable-changed-before-launch")
        if _neutral_cwd(target) != cwd:
            raise GitReadError("neutral-working-directory-changed")
        return _capture_windows_child(argv, env, cwd, float(timeout), stdout_limit, stderr_limit)
    except BaseException:
        return ReadResult("failed", None, b"")


def _capture_windows_child(argv: list[str], env: dict[str, str], cwd: str,
                           timeout: float, stdout_limit: int, stderr_limit: int) -> ReadResult:
    try:
        child = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 shell=False, close_fds=True,
                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except OSError:
        return ReadResult("failed", None, b"")
    assert child.stdout is not None and child.stderr is not None
    out_collector = _Collector(child.stdout, stdout_limit)
    err_collector = _Collector(child.stderr, stderr_limit)
    out_thread = threading.Thread(target=out_collector.drain, daemon=True)
    err_thread = threading.Thread(target=err_collector.drain, daemon=True)
    out_thread.start()
    err_thread.start()
    deadline = time.monotonic() + timeout
    failed = False
    while child.poll() is None:
        if (time.monotonic() >= deadline or out_collector.overflow.is_set()
                or err_collector.overflow.is_set()):
            failed = True
            child.kill()
            break
        time.sleep(0.02)
    try:
        child.wait(timeout=CLEANUP_SECONDS)
    except subprocess.TimeoutExpired:
        failed = True
        child.kill()
        try:
            child.wait(timeout=CLEANUP_SECONDS)
        except subprocess.TimeoutExpired:
            pass
    reader_deadline = time.monotonic() + CLEANUP_SECONDS
    readers = (out_thread, err_thread)
    if not _join_until(readers, reader_deadline):
        failed = True
    child.stdout.close()
    child.stderr.close()
    if not _join_until(readers, reader_deadline):
        failed = True
    if (out_thread.is_alive() or err_thread.is_alive()
            or not out_collector.done.is_set() or not err_collector.done.is_set()):
        failed = True
    if out_collector.error.is_set() or err_collector.error.is_set():
        failed = True
    if failed or out_collector.overflow.is_set() or err_collector.overflow.is_set():
        return ReadResult("failed", child.returncode, b"", "process-or-cleanup-incomplete")
    return ReadResult("completed", child.returncode, bytes(out_collector.data))


def _version_key(snapshot: _Snapshot) -> tuple[object, ...]:
    return (snapshot.lexical, snapshot.resolved, snapshot.identity, snapshot.size,
            snapshot.mtime_ns, snapshot.ctime_ns, snapshot.mode, snapshot.digest)


def _version_probe(snapshot: _Snapshot, target: str) -> ReadResult:
    exclusions = worktree_exclusions(target)
    _assert_off_target(snapshot.lexical, snapshot.resolved, exclusions)
    if not _snapshot_still_matches(snapshot):
        raise GitReadError("executable-changed-before-launch")
    key = _version_key(snapshot)
    with _VERSION_LOCK:
        cached = _VERSION_CACHE.get(key)
    if cached:
        if not _snapshot_still_matches(snapshot):
            raise GitReadError("executable-changed-before-launch")
        return ReadResult("completed", 0, cached[1])
    env = _base_environment()
    cwd = _neutral_cwd(target)
    result = _capture_process([snapshot.resolved, "--version"],
                              env, cwd, DEFAULT_TIMEOUT_SECONDS, VERSION_MAX_BYTES,
                              STDERR_MAX_BYTES, snapshot, _absolute(target))
    if result.state != "completed" or result.returncode != 0:
        return ReadResult("failed", result.returncode, b"", "git-version-unavailable")
    version = _parse_version(result.stdout)
    if version is None:
        return ReadResult("failed", result.returncode, b"", "git-version-unparseable")
    with _VERSION_LOCK:
        if len(_VERSION_CACHE) >= 32:
            _VERSION_CACHE.pop(next(iter(_VERSION_CACHE)))
        _VERSION_CACHE[key] = (version, result.stdout)
    return result


def _git_version(snapshot: _Snapshot, target: str) -> tuple[int, int, int] | None:
    result = _version_probe(snapshot, target)
    if result.state != "completed" or result.returncode != 0:
        return None
    return _parse_version(result.stdout)


def _run_once(snapshot: _Snapshot, target: str, args: tuple[str, ...], *,
              timeout: float, output_limit: int,
              config_overrides: tuple[tuple[str, str], ...] = ()) -> ReadResult:
    exclusions = worktree_exclusions(target)
    _assert_off_target(snapshot.lexical, snapshot.resolved, exclusions)
    if not _snapshot_still_matches(snapshot):
        raise GitReadError("executable-changed-before-launch")
    argv = _argv(snapshot, target, args, config_overrides)
    if not _snapshot_still_matches(snapshot):
        raise GitReadError("executable-changed-before-launch")
    result = _capture_process(argv, _base_environment(), _neutral_cwd(target), timeout,
                              output_limit, STDERR_MAX_BYTES, snapshot, target)
    if args[0] == "config" and len(result.stdout) > CONFIG_MAX_BYTES:
        return ReadResult("failed", result.returncode, b"")
    return result


def _run_git(target: str | os.PathLike[str], args: tuple[str, ...], *,
             executable: _Snapshot | None,
             path_value: str | None,
             timeout: float,
             output_limit: int) -> ReadResult:
    target_path = _absolute(target)
    if timeout <= 0 or timeout > 60 or output_limit < 0 or output_limit > HISTORY_MAX_BYTES:
        raise GitReadError("invalid-read-budget")
    if not args or args[0] not in _READ_COMMANDS:
        raise GitReadError("unsupported-read-form")
    snapshot = executable if executable is not None else select_git(target_path, path_value)
    if snapshot is None:
        return ReadResult("absent", None, b"", "git-not-found")
    if args[0] == "status":
        config = _run_once(snapshot, target_path,
                           ("config", "--includes", "--null", "--list"),
                           timeout=timeout, output_limit=CONFIG_MAX_BYTES)
        if config.state != "completed" or config.returncode != 0:
            return ReadResult("failed", config.returncode, b"", "status-filter-config-failed")
        filters = _filter_config_overrides(config.stdout)
        return _run_once(snapshot, target_path, args, timeout=timeout,
                         output_limit=output_limit, config_overrides=filters)
    if args[0] == "config":
        output_limit = min(output_limit, CONFIG_MAX_BYTES)
    return _run_once(snapshot, target_path, args, timeout=timeout,
                     output_limit=output_limit)


def read_version(target: str | os.PathLike[str], *,
                 path_value: str | None = None) -> ReadResult:
    """Read the validated Git version, preserving absence/failure separately."""
    try:
        target_path = _absolute(target)
        snapshot = select_git(target_path, path_value)
        if snapshot is None:
            return ReadResult("absent", None, b"", "git-not-found")
        return _version_probe(snapshot, target_path)
    except GitReadError as exc:
        return ReadResult("failed", None, b"", str(exc))


def run_git(target: str | os.PathLike[str], args: tuple[str, ...], *,
            executable: _Snapshot | None = None,
            path_value: str | None = None,
            timeout: float = DEFAULT_TIMEOUT_SECONDS,
            output_limit: int = OUTPUT_MAX_BYTES) -> ReadResult:
    """Run one source-owned Git read form with fixed offline host settings."""
    try:
        return _run_git(target, args, executable=executable, path_value=path_value,
                        timeout=timeout, output_limit=output_limit)
    except GitReadError as exc:
        # The reason is an implementation-owned code, never Git stderr or
        # repository text. Callers decide how a failed read affects policy.
        return ReadResult("failed", None, b"", str(exc))


def bind_verified_source(data: bytes, expected_sha256: str) -> None:
    """Bind the source bytes and caller pin for the Windows worker boundary."""
    if not isinstance(data, bytes) or hashlib.sha256(data).hexdigest() != expected_sha256:
        raise GitReadError("helper-pin-mismatch")
    global _VERIFIED_SOURCE, _VERIFIED_SHA256
    _VERIFIED_SOURCE = data
    _VERIFIED_SHA256 = expected_sha256

