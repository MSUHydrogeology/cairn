#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Bounded, read-only filesystem map for the optional architecture module.

The collector never imports or executes inspected files. It uses descriptor-
relative no-follow traversal on POSIX and a handle-relative backend for local
NTFS roots on 64-bit Windows; unsupported systems receive an explicit
incomplete result. Git revisions and HTML rendering are intentionally outside
this filesystem-only first stage.
"""
from __future__ import annotations

import sys

if not sys.flags.isolated:
    sys.stderr.write("code_map: run with the trusted Python runtime in -I mode\n")
    raise SystemExit(2)

import argparse
import ast
import collections
import io
import json
import os
import re
import signal
import stat
import struct
import subprocess
import time
import tokenize
from pathlib import PurePosixPath
from typing import Any


MAX_ENTRIES = 10_000
MAX_TOTAL_READ = 128 * 1024 * 1024
MAX_SOURCE = 1024 * 1024
MAX_AST_NODES = 2_000_000
MAX_SYMBOLS = 20_000
MAX_COMPARISONS = 1_000_000
PER_FILE_SECONDS = 5.0
PARSER_SECONDS = 30.0
COMMAND_SECONDS = 60.0
_WORKER_SCAN = "--_scan-worker"
_WORKER_PARSE = "--_parse-worker"


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def _write_result(result: dict[str, Any], exit_code: int = 0) -> int:
    sys.stdout.buffer.write(_json_bytes(result))
    sys.stdout.buffer.flush()
    return exit_code


def _diagnostic(code: str, path: str, message: str, remedy: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message, "remedy": remedy}


def _empty_result(root: str, mode: str) -> dict[str, Any]:
    return {
        "schema": "cairn-code-map-v1",
        "status": "incomplete",
        "mode": mode,
        "root": root,
        "revision": None,
        "revision_note": "not read: filesystem mode performs no Git inspection",
        "budgets": {
            "entries_limit": MAX_ENTRIES,
            "entries_seen": 0,
            "bytes_limit": MAX_TOTAL_READ,
            "bytes_read": 0,
            "source_limit": MAX_SOURCE,
            "ast_nodes_limit": MAX_AST_NODES,
            "ast_nodes": 0,
            "symbols_limit": MAX_SYMBOLS,
            "symbols": 0,
            "comparisons_limit": MAX_COMPARISONS,
            "comparisons": 0,
            "parser_seconds_limit": PARSER_SECONDS,
            "parser_seconds": 0.0,
            "command_seconds_limit": COMMAND_SECONDS,
            "command_seconds": 0.0,
        },
        "components": [],
        "files": [],
        "scope": {"excluded_directory_names": [".git", "__pycache__", ".pytest_cache"]},
        "omissions": [],
        "neighbors": [],
        "sampling": None,
        "diagnostics": [],
    }


def _secure_walk_available() -> bool:
    required = (os.open, os.stat)
    return (
        all(fn in os.supports_dir_fd for fn in required)
        and os.scandir in os.supports_fd
        and hasattr(os, "O_DIRECTORY")
        and hasattr(os, "O_NOFOLLOW")
    )


def _open_absolute_directory(path: str) -> int:
    """Open every root component by handle without following links."""
    absolute = os.path.abspath(path)
    drive, tail = os.path.splitdrive(absolute)
    if drive:
        raise OSError("only POSIX absolute roots are supported by this walker")
    fd = os.open(os.sep, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in (item for item in tail.split(os.sep) if item):
            next_fd = os.open(
                part,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=fd,
            )
            os.close(fd)
            fd = next_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


def _read_at(parent_fd: int, name: str, before: os.stat_result,
             allowance: int, read_count: list[int] | None = None) -> tuple[bytes, os.stat_result]:
    flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(name, flags, dir_fd=parent_fd)
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode):
            raise OSError("not a regular file")
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise OSError("file changed between inspection and open")
        if opened.st_size > MAX_SOURCE:
            raise OverflowError("source grew beyond the per-file limit")
        if opened.st_size > allowance:
            raise OverflowError("total read budget would be exceeded")
        chunks: list[bytes] = []
        remaining = min(allowance, MAX_SOURCE + 1)
        while remaining:
            chunk = os.read(fd, min(64 * 1024, remaining))
            if not chunk:
                break
            if read_count is not None:
                read_count[0] += len(chunk)
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        if len(data) > MAX_SOURCE:
            raise OverflowError("source grew beyond the per-file limit")
        if len(data) > allowance:
            raise OverflowError("file grew beyond the remaining read budget")
        after = os.fstat(fd)
        if ((after.st_dev, after.st_ino, after.st_size)
                != (opened.st_dev, opened.st_ino, opened.st_size)):
            raise OSError("file changed while it was read")
        return data, after
    finally:
        os.close(fd)


class _WindowsUnavailable(Exception):
    pass


class _WindowsLimit(Exception):
    pass


class _WindowsAPI:
    """Lazily bind the small, fixed set of Windows system APIs we need."""

    def __init__(self) -> None:
        import ctypes as C
        from ctypes import wintypes as W

        if C.sizeof(C.c_void_p) != 8:
            raise _WindowsUnavailable("unsupported-pointer-layout")
        try:
            nt = C.WinDLL("ntdll.dll", winmode=0x800, use_last_error=True)
            kernel = C.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
        except (AttributeError, OSError):
            raise _WindowsUnavailable("system-api-unavailable") from None

        HANDLE = C.c_void_p
        ULONG_PTR = C.c_size_t
        NTSTATUS = C.c_int32

        class UNICODE_STRING(C.Structure):
            _fields_ = [("Length", W.USHORT), ("MaximumLength", W.USHORT),
                        ("Buffer", C.c_void_p)]

        class OBJECT_ATTRIBUTES(C.Structure):
            _fields_ = [("Length", W.ULONG), ("RootDirectory", HANDLE),
                        ("ObjectName", C.POINTER(UNICODE_STRING)),
                        ("Attributes", W.ULONG), ("SecurityDescriptor", C.c_void_p),
                        ("SecurityQualityOfService", C.c_void_p)]

        class IO_STATUS_UNION(C.Union):
            _fields_ = [("Status", NTSTATUS), ("Pointer", C.c_void_p)]

        class IO_STATUS_BLOCK(C.Structure):
            _fields_ = [("u", IO_STATUS_UNION), ("Information", ULONG_PTR)]

        class BY_HANDLE_INFO(C.Structure):
            _fields_ = [("attributes", W.DWORD), ("created", W.FILETIME),
                        ("accessed", W.FILETIME), ("written", W.FILETIME),
                        ("volume", W.DWORD), ("size_high", W.DWORD),
                        ("size_low", W.DWORD), ("links", W.DWORD),
                        ("id_high", W.DWORD), ("id_low", W.DWORD)]

        class BASIC_LIMIT(C.Structure):
            _fields_ = [("process_time", C.c_int64), ("job_time", C.c_int64),
                        ("flags", W.DWORD), ("minimum", C.c_size_t),
                        ("maximum", C.c_size_t), ("processes", W.DWORD),
                        ("affinity", C.c_size_t), ("priority", W.DWORD),
                        ("scheduling", W.DWORD)]

        class IO_COUNTERS(C.Structure):
            _fields_ = [(name, C.c_uint64) for name in
                        ("read_ops", "write_ops", "other_ops", "read_bytes",
                         "write_bytes", "other_bytes")]

        class EXTENDED_LIMIT(C.Structure):
            _fields_ = [("basic", BASIC_LIMIT), ("io", IO_COUNTERS),
                        ("process_memory", C.c_size_t), ("job_memory", C.c_size_t),
                        ("peak_process_memory", C.c_size_t),
                        ("peak_job_memory", C.c_size_t)]

        sizes = (C.sizeof(UNICODE_STRING), C.sizeof(OBJECT_ATTRIBUTES),
                 C.sizeof(IO_STATUS_BLOCK), C.sizeof(BY_HANDLE_INFO),
                 struct.calcsize("<II6qIIIbx24s2xq"), C.sizeof(BASIC_LIMIT),
                 C.sizeof(EXTENDED_LIMIT))
        if sizes != (16, 48, 16, 52, 104, 64, 144):
            raise _WindowsUnavailable("unsupported-windows-abi-layout")

        try:
            nt.NtCreateFile.argtypes = [C.POINTER(HANDLE), W.ULONG,
                C.POINTER(OBJECT_ATTRIBUTES), C.POINTER(IO_STATUS_BLOCK), C.c_void_p,
                W.ULONG, W.ULONG, W.ULONG, W.ULONG, C.c_void_p, W.ULONG]
            nt.NtCreateFile.restype = NTSTATUS
            kernel.QueryDosDeviceW.argtypes = [W.LPCWSTR, W.LPWSTR, W.DWORD]
            kernel.QueryDosDeviceW.restype = W.DWORD
            kernel.GetFileType.argtypes = [HANDLE]
            kernel.GetFileType.restype = W.DWORD
            kernel.GetFileInformationByHandle.argtypes = [HANDLE, C.POINTER(BY_HANDLE_INFO)]
            kernel.GetFileInformationByHandle.restype = W.BOOL
            kernel.GetFileInformationByHandleEx.argtypes = [HANDLE, C.c_int, C.c_void_p, W.DWORD]
            kernel.GetFileInformationByHandleEx.restype = W.BOOL
            kernel.GetVolumeInformationByHandleW.argtypes = [HANDLE, W.LPWSTR, W.DWORD,
                C.POINTER(W.DWORD), C.POINTER(W.DWORD), C.POINTER(W.DWORD), W.LPWSTR, W.DWORD]
            kernel.GetVolumeInformationByHandleW.restype = W.BOOL
            kernel.ReadFile.argtypes = [HANDLE, C.c_void_p, W.DWORD,
                C.POINTER(W.DWORD), C.c_void_p]
            kernel.ReadFile.restype = W.BOOL
            kernel.CloseHandle.argtypes = [HANDLE]
            kernel.CloseHandle.restype = W.BOOL
            kernel.CreateJobObjectW.argtypes = [C.c_void_p, W.LPCWSTR]
            kernel.CreateJobObjectW.restype = HANDLE
            kernel.SetInformationJobObject.argtypes = [HANDLE, C.c_int, C.c_void_p, W.DWORD]
            kernel.SetInformationJobObject.restype = W.BOOL
            kernel.GetCurrentProcess.argtypes = []
            kernel.GetCurrentProcess.restype = HANDLE
            kernel.AssignProcessToJobObject.argtypes = [HANDLE, HANDLE]
            kernel.AssignProcessToJobObject.restype = W.BOOL
        except (AttributeError, OSError):
            raise _WindowsUnavailable("system-api-unavailable") from None

        self.C = C
        self.W = W
        self.nt = nt
        self.kernel = kernel
        self.HANDLE = HANDLE
        self.UNICODE_STRING = UNICODE_STRING
        self.OBJECT_ATTRIBUTES = OBJECT_ATTRIBUTES
        self.IO_STATUS_BLOCK = IO_STATUS_BLOCK
        self.BY_HANDLE_INFO = BY_HANDLE_INFO
        self.EXTENDED_LIMIT = EXTENDED_LIMIT

    def close(self, handle: int | None) -> None:
        if handle:
            self.kernel.CloseHandle(self.HANDLE(handle))

    def open(self, name: str, parent: int | None = None, *, file_read: bool = False) -> int:
        C, W = self.C, self.W
        if parent is not None and (not name or name in {".", ".."}
                                   or any(char in name for char in "\\/:\x00")
                                   or len(name.encode("utf-16-le")) > 510):
            raise _WindowsUnavailable("not-one-component")
        text = C.create_unicode_buffer(name)
        byte_length = len(name.encode("utf-16-le"))
        unicode_name = self.UNICODE_STRING(byte_length, byte_length + 2,
                                            C.cast(text, C.c_void_p))
        attributes = self.OBJECT_ATTRIBUTES(
            C.sizeof(self.OBJECT_ATTRIBUTES), parent, C.pointer(unicode_name), 0, None, None)
        io_status = self.IO_STATUS_BLOCK()
        handle = self.HANDLE()
        status = self.nt.NtCreateFile(
            C.byref(handle), 1 | 0x80 | 0x100000, C.byref(attributes),
            C.byref(io_status), None, 0, 1 if file_read else 3, 1,
            0x00200000 | 0x20, None, 0)
        if status != 0:
            self.close(handle.value)
            raise _WindowsUnavailable(f"open-status-0x{status & 0xffffffff:08X}")
        return int(handle.value)

    def info(self, handle: int) -> dict[str, Any]:
        C, W = self.C, self.W
        value = self.BY_HANDLE_INFO()
        if (self.kernel.GetFileType(handle) != 1
                or not self.kernel.GetFileInformationByHandle(handle, C.byref(value))):
            raise _WindowsUnavailable("not-verifiable-disk-object")
        attributes = int(value.attributes)
        if attributes & (0x400 | 0x40):
            raise _WindowsUnavailable("reparse-or-device")
        return {
            "identity": (int(value.volume), (int(value.id_high) << 32) | int(value.id_low)),
            "size": (int(value.size_high) << 32) | int(value.size_low),
            "directory": bool(attributes & 0x10),
            "written": (int(value.written.dwHighDateTime) << 32)
                       | int(value.written.dwLowDateTime),
        }

    def admit_root(self, path: str) -> tuple[list[int], str]:
        import ntpath
        import re

        if not isinstance(path, str) or path.startswith("\\\\"):
            raise _WindowsUnavailable("unsupported-root-form")
        drive, tail = ntpath.splitdrive(path)
        if not re.fullmatch(r"[A-Za-z]:", drive) or not tail.startswith("\\"):
            raise _WindowsUnavailable("unsupported-root-form")
        parts = tail[1:].split("\\")
        if parts == [""]:
            parts = []
        for part in parts:
            if (not part or part in {".", ".."} or any(c in part for c in "/:\x00")
                    or len(part.encode("utf-16-le")) > 510):
                raise _WindowsUnavailable("unsupported-root-component")
        targets = self.C.create_unicode_buffer(32768)
        if not self.kernel.QueryDosDeviceW(drive, targets, len(targets)):
            raise _WindowsUnavailable("drive-map-unavailable")
        target = targets.value
        if not re.fullmatch(r"\\Device\\HarddiskVolume[0-9]+", target):
            raise _WindowsUnavailable("unsupported-drive-alias")
        handles: list[int] = []
        try:
            volume = self.open(target + "\\")
            handles.append(volume)
            if not self.info(volume)["directory"]:
                raise _WindowsUnavailable("volume-not-directory")
            fs_name = self.C.create_unicode_buffer(64)
            serial, name_limit, flags = self.W.DWORD(), self.W.DWORD(), self.W.DWORD()
            if not self.kernel.GetVolumeInformationByHandleW(
                    volume, None, 0, self.C.byref(serial), self.C.byref(name_limit),
                    self.C.byref(flags), fs_name, len(fs_name)):
                raise _WindowsUnavailable("volume-info-unavailable")
            if fs_name.value != "NTFS":
                raise _WindowsUnavailable("unsupported-volume")
            for part in parts:
                child = self.open_child(handles[-1], part)
                handles.append(child)
                if not self.info(child)["directory"]:
                    raise _WindowsUnavailable("root-component-not-directory")
            return handles, fs_name.value
        except BaseException:
            for handle in reversed(handles):
                self.close(handle)
            raise

    def open_child(self, parent: int, entry: dict[str, Any] | str,
                   *, file_read: bool = False) -> int:
        name = entry if isinstance(entry, str) else entry["name"]
        before = self.info(parent)
        if not before["directory"]:
            raise _WindowsUnavailable("parent-not-directory")
        handle = self.open(name, parent, file_read=file_read)
        try:
            child = self.info(handle)
            after = self.info(parent)
            if after["identity"] != before["identity"]:
                raise _WindowsUnavailable("parent-changed")
            if child["identity"][0] != before["identity"][0]:
                raise _WindowsUnavailable("volume-changed")
            if isinstance(entry, dict) and (
                    child["identity"][1] != entry["file_id"]
                    or child["directory"] != entry["directory"]
                    or child["size"] != entry["size"]):
                raise _WindowsUnavailable("enumerated-identity-or-type-changed")
            return handle
        except BaseException:
            self.close(handle)
            raise

    def enumerate(self, parent: int, remaining: int) -> list[dict[str, Any]]:
        if not self.info(parent)["directory"]:
            raise _WindowsUnavailable("not-directory")
        C = self.C
        buffer_size = 64 * 1024
        buffer = (C.c_uint64 * (buffer_size // 8))()
        first = True
        calls = 0
        seen: set[str] = set()
        rows: list[dict[str, Any]] = []
        while True:
            calls += 1
            if calls > remaining + 2:
                raise _WindowsLimit("enumeration-call-limit")
            C.memset(C.addressof(buffer), 0, buffer_size)
            ok = self.kernel.GetFileInformationByHandleEx(
                parent, 11 if first else 10, buffer, buffer_size)
            first = False
            if not ok:
                error = C.get_last_error()
                if error == 18:
                    break
                raise _WindowsUnavailable(f"enumeration-error-{error}")
            batch = _decode_windows_entries(C.string_at(buffer, buffer_size))
            for row in batch:
                if row["name"] in {".", ".."}:
                    continue
                if row["name"] in seen:
                    raise _WindowsUnavailable("duplicate-live-enumeration-name")
                seen.add(row["name"])
                rows.append(row)
                if len(rows) > remaining:
                    return sorted(rows, key=lambda item: item["name"])
        self.info(parent)
        return sorted(rows, key=lambda row: row["name"])

    def read(self, handle: int, allowance: int, counted: list[int]) -> bytes:
        before = self.info(handle)
        if before["directory"]:
            raise _WindowsUnavailable("source-not-file")
        if before["size"] > MAX_SOURCE:
            raise _WindowsLimit("per-file source limit")
        if before["size"] > allowance:
            raise _WindowsLimit("total read budget would be exceeded")
        chunks: list[bytes] = []
        remaining = min(MAX_SOURCE + 1, allowance)
        while remaining:
            buffer = self.C.create_string_buffer(min(65536, remaining))
            count = self.W.DWORD()
            ok = self.kernel.ReadFile(handle, buffer, len(buffer), self.C.byref(count), None)
            counted[0] += int(count.value)
            if not ok:
                raise _WindowsUnavailable("read-failed")
            if count.value > len(buffer):
                raise _WindowsUnavailable("invalid-read-count")
            if not count.value:
                break
            chunks.append(buffer.raw[:count.value])
            remaining -= count.value
        after = self.info(handle)
        if after != before:
            raise _WindowsUnavailable("source-changed")
        data = b"".join(chunks)
        if len(data) != before["size"]:
            raise _WindowsUnavailable("source-size-changed")
        if len(data) > MAX_SOURCE:
            raise _WindowsLimit("per-file source limit")
        if len(data) > allowance:
            raise _WindowsLimit("total read budget would be exceeded")
        return data

    def install_worker_job(self) -> int:
        job = self.kernel.CreateJobObjectW(None, None)
        if not job:
            raise _WindowsUnavailable("job-create")
        limits = self.EXTENDED_LIMIT()
        limits.basic.flags = 0x2000
        if (not self.kernel.SetInformationJobObject(
                job, 9, self.C.byref(limits), self.C.sizeof(limits))
                or not self.kernel.AssignProcessToJobObject(
                    job, self.kernel.GetCurrentProcess())):
            self.close(job)
            raise _WindowsUnavailable("job-install")
        return int(job)


def _decode_windows_entries(raw: bytes) -> list[dict[str, Any]]:
    """Decode bounded FILE_ID_BOTH_DIR_INFO bytes using the fixed NTFS layout."""
    header = struct.Struct("<II6qIIIbx24s2xq")
    rows: list[dict[str, Any]] = []
    offset = 0
    while True:
        if len(raw) - offset < header.size:
            raise _WindowsUnavailable("truncated-directory-header")
        row = header.unpack_from(raw, offset)
        name_bytes = row[9]
        end = offset + header.size + name_bytes
        if not name_bytes or name_bytes % 2 or name_bytes > 510 or end > len(raw):
            raise _WindowsUnavailable("invalid-directory-name-length")
        try:
            name = raw[offset + header.size:end].decode("utf-16-le")
        except UnicodeError:
            raise _WindowsUnavailable("invalid-directory-name") from None
        if name not in {".", ".."}:
            if (not name or any(c in name for c in "\\/:\x00")
                    or len(name.encode("utf-16-le")) > 510):
                raise _WindowsUnavailable("not-one-component")
            if row[6] < 0:
                raise _WindowsUnavailable("negative-directory-size")
            rows.append({"name": name, "file_id": row[13] & ((1 << 64) - 1),
                         "size": row[6], "directory": bool(row[8] & 0x10),
                         "reparse": bool(row[8] & 0x400),
                         "device": bool(row[8] & 0x40)})
        step = row[0]
        if step == 0:
            return rows
        if step % 8 or step < header.size + name_bytes or offset + step >= len(raw):
            raise _WindowsUnavailable("invalid-directory-next-offset")
        offset += step


class _PosixFilesystem:
    """Descriptor-relative adapter used by the shared collector algorithm."""

    def enumerate(self, folder_fd: int, remaining: int) -> list[str]:
        names: list[str] = []
        scan = os.scandir(folder_fd)
        try:
            for item in scan:
                names.append(item.name)
                if len(names) > remaining:
                    break
        finally:
            scan.close()
        return sorted(names)

    def describe(self, folder_fd: int, name: str) -> dict[str, Any]:
        before = os.stat(name, dir_fd=folder_fd, follow_symlinks=False)
        return {"name": name, "stat": before,
                "reparse": stat.S_ISLNK(before.st_mode),
                "directory": stat.S_ISDIR(before.st_mode),
                "regular": stat.S_ISREG(before.st_mode),
                "size": before.st_size}

    def open_directory(self, folder_fd: int, entry: dict[str, Any]) -> int:
        return os.open(entry["name"], os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                       dir_fd=folder_fd)

    def verify_directory(self, before: dict[str, Any], opened: int) -> bool:
        after = os.fstat(opened)
        original = before["stat"]
        return (after.st_dev, after.st_ino) == (original.st_dev, original.st_ino)

    def read_file(self, folder_fd: int, entry: dict[str, Any], allowance: int,
                  counted: list[int]) -> bytes:
        data, _after = _read_at(folder_fd, entry["name"], entry["stat"], allowance, counted)
        return data

    @staticmethod
    def close(handle: int) -> None:
        os.close(handle)


class _WindowsFilesystem:
    def __init__(self, api: _WindowsAPI) -> None:
        self.api = api

    def enumerate(self, folder: int, remaining: int) -> list[dict[str, Any]]:
        return self.api.enumerate(folder, remaining)

    @staticmethod
    def describe(_folder: int, entry: dict[str, Any]) -> dict[str, Any]:
        return entry

    def open_directory(self, folder: int, entry: dict[str, Any]) -> int:
        return self.api.open_child(folder, entry)

    def verify_directory(self, _before: dict[str, Any], _opened: int) -> bool:
        return True

    def read_file(self, folder: int, entry: dict[str, Any], allowance: int,
                  counted: list[int]) -> bytes:
        handle = self.api.open_child(folder, entry, file_read=True)
        try:
            return self.api.read(handle, allowance, counted)
        finally:
            self.api.close(handle)

    def close(self, handle: int) -> None:
        self.api.close(handle)


_WINDOWS_WORKER_JOB: int | None = None


def _tokens(name: str) -> list[str]:
    parts = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name).split("_")
    return [piece.lower() for part in parts for piece in part.split()
            if piece and not piece.isdigit()]


def _summary(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.split())[:240]


def _parse_source_worker() -> int:
    request = json.loads(sys.argv[2])
    source = sys.stdin.buffer.read(MAX_SOURCE + 1)
    if len(source) > MAX_SOURCE:
        return _write_result({"ok": False, "error": "source-limit"}, 2)
    try:
        encoding, _ = tokenize.detect_encoding(io.BytesIO(source).readline)
        text = source.decode(encoding)
        tree = ast.parse(text)
    except (SyntaxError, UnicodeError, LookupError, RecursionError) as exc:
        return _write_result({"ok": False, "error": "parse-error",
                              "message": str(exc)[:500]}, 0)

    node_limit = int(request["node_limit"])
    stack = [tree]
    node_count = 0
    while stack:
        node = stack.pop()
        node_count += 1
        if node_count > node_limit:
            return _write_result({"ok": False, "error": "ast-node-limit",
                                  "nodes": node_count}, 0)
        stack.extend(ast.iter_child_nodes(node))

    definitions: list[tuple[ast.AST, str, bool]] = []
    pending = [(tree, "", True)]
    while pending:
        node, parent, visible = pending.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            qualified = f"{parent}.{node.name}" if parent else node.name
            public = visible and not node.name.startswith("_")
            definitions.append((node, qualified, public))
            if len(definitions) > int(request["symbol_limit"]):
                return _write_result({"ok": False, "error": "symbol-limit",
                                      "definitions": len(definitions), "nodes": node_count}, 0)
            parent = qualified
            if not isinstance(node, ast.ClassDef):
                parent += ".<locals>"
                public = False
            visible = public
        pending.extend((child, parent, visible)
                       for child in reversed(list(ast.iter_child_nodes(node))))
    symbols: list[dict[str, Any]] = []
    symbol_limit = int(request["symbol_limit"])
    for node, qualified, public in definitions:
        name = node.name
        stack2 = [node]
        shape: collections.Counter[str] = collections.Counter()
        identifiers: set[str] = set()
        while stack2:
            child = stack2.pop()
            shape[type(child).__name__] += 1
            if isinstance(child, ast.Name):
                identifiers.update(_tokens(child.id))
            elif isinstance(child, ast.arg):
                identifiers.update(_tokens(child.arg))
            elif isinstance(child, ast.Attribute):
                identifiers.update(_tokens(child.attr))
            stack2.extend(ast.iter_child_nodes(child))
        symbols.append({
            "name": name,
            "qualified_name": qualified,
            "kind": ("class" if isinstance(node, ast.ClassDef) else "function"),
            "public": public,
            "line": int(getattr(node, "lineno", 0)),
            "summary": _summary(ast.get_docstring(node, clean=False)),
            "shape": dict(shape),
            "names": sorted(identifiers | set(_tokens(name))),
        })
        if len(symbols) > symbol_limit:
            return _write_result({"ok": False, "error": "symbol-limit",
                                  "symbols": symbol_limit, "nodes": node_count}, 0)
    return _write_result({"ok": True, "nodes": node_count,
                          "definitions": len(definitions),
                          "symbols": symbols}, 0)


def _parse_file(data: bytes, node_limit: int, symbol_limit: int,
                timeout: float) -> tuple[dict[str, Any], float]:
    request = json.dumps({"node_limit": node_limit,
                          "symbol_limit": symbol_limit}, separators=(",", ":"))
    command = [sys.executable, "-I", os.path.abspath(__file__),
               _WORKER_PARSE, request]
    started = time.monotonic()
    completed = subprocess.run(
        command, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=timeout, check=False, env={
            "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",
        },
    )
    elapsed = time.monotonic() - started
    try:
        result = json.loads(completed.stdout.decode("ascii"))
    except (UnicodeError, json.JSONDecodeError):
        result = {"ok": False, "error": "parser-worker-failed",
                  "message": completed.stderr.decode("ascii", "backslashreplace")[:500]}
    return result, elapsed


def _file_record(relative: str, info: os.stat_result | int) -> dict[str, Any]:
    size = info.st_size if isinstance(info, os.stat_result) else info
    suffix = os.path.splitext(relative)[1].lower()
    language = "Python" if suffix == ".py" else (suffix[1:] or "unknown")
    return {
        "path": relative,
        "component": relative.split("/", 1)[0] if "/" in relative else ".",
        "language": language,
        "analysis": "pending" if language == "Python" else "unsupported",
        "bytes": size,
        "public": [],
    }


def _walk(root_fd: int, root_name: str, args: dict[str, Any],
          filesystem: _PosixFilesystem | _WindowsFilesystem | None = None
          ) -> dict[str, Any]:
    filesystem = filesystem or _PosixFilesystem()
    result = _empty_result(root_name, "release" if args["release"] else
                           "changed" if args["changed"] else "map")
    diagnostics = result["diagnostics"]
    records: list[dict[str, Any]] = []
    symbol_rows: list[dict[str, Any]] = []
    dirs_seen: set[str] = set()
    total_bytes = 0
    total_nodes = 0
    total_definitions = 0
    parser_time = 0.0
    entries = 0
    parsing_open = True
    deadline = time.monotonic() + PARSER_SECONDS
    wanted = set(args["changed"])
    found_wanted: set[str] = set()

    def visit(folder_fd: int, prefix: str) -> None:
        nonlocal entries, total_bytes, total_nodes, total_definitions
        nonlocal parser_time, parsing_open
        if entries >= MAX_ENTRIES:
            diagnostics.append(_diagnostic(
                "entry-limit", prefix, f"entry limit {MAX_ENTRIES} reached",
                "Narrow the filesystem root; the limit is fixed for this scan."))
            parsing_open = False
            return
        try:
            names = filesystem.enumerate(folder_fd, MAX_ENTRIES - entries)
        except _WindowsLimit as exc:
            diagnostics.append(_diagnostic(
                "entry-limit", prefix, str(exc),
                "Narrow the filesystem root; the limit is fixed for this scan."))
            parsing_open = False
            return
        except _WindowsUnavailable as exc:
            diagnostics.append(_diagnostic(
                "directory-read", prefix, str(exc),
                "Retry after the directory stops changing or use a supported NTFS volume."))
            return
        except OSError as exc:
            diagnostics.append(_diagnostic(
                "directory-read", prefix, str(exc),
                "Grant read access or scan a stable, readable directory."))
            return
        for name in names:
            if entries >= MAX_ENTRIES:
                diagnostics.append(_diagnostic(
                    "entry-limit", prefix, f"entry limit {MAX_ENTRIES} reached",
                    "Narrow the filesystem root; the limit is fixed for this scan."))
                parsing_open = False
                return
            relative = f"{prefix}/{name}" if prefix else name
            entries += 1
            try:
                before = filesystem.describe(folder_fd, name)
            except _WindowsUnavailable as exc:
                diagnostics.append(_diagnostic(
                    "entry-stat", relative, str(exc),
                    "Retry after the directory stops changing."))
                continue
            except OSError as exc:
                diagnostics.append(_diagnostic(
                    "entry-stat", relative, str(exc),
                    "Retry after the directory stops changing."))
                continue
            if before["reparse"]:
                diagnostics.append(_diagnostic(
                    "linked-entry", relative, "entry is a symbolic link or reparse point",
                    "Replace links/reparse points with contained real files or directories."))
                continue
            if before.get("device", False) or not before.get("directory", False) and not before.get("regular", True):
                diagnostics.append(_diagnostic(
                    "special-file", relative, "entry is not a regular file or directory",
                    "Replace it with a regular file or remove it from the scan root."))
                continue
            if before["directory"]:
                if name in result["scope"]["excluded_directory_names"]:
                    result["omissions"].append({
                        "path": relative,
                        "reason": "metadata directory excluded from default scope",
                    })
                    continue
                dirs_seen.add(relative.split("/", 1)[0])
                try:
                    child_fd = filesystem.open_directory(folder_fd, before)
                except _WindowsUnavailable as exc:
                    diagnostics.append(_diagnostic(
                        "directory-changed-or-linked", relative, str(exc),
                        "Replace links/reparse points with contained real directories."))
                    continue
                except OSError as exc:
                    diagnostics.append(_diagnostic(
                        "directory-changed-or-linked", relative, str(exc),
                        "Replace links/reparse points with contained real directories."))
                    continue
                try:
                    if not filesystem.verify_directory(before, child_fd):
                        diagnostics.append(_diagnostic(
                            "directory-race", relative,
                            "directory changed between inspection and open",
                            "Retry against a stable tree."))
                        continue
                    visit(child_fd, relative)
                finally:
                    filesystem.close(child_fd)
                continue
            if not before.get("regular", True):
                diagnostics.append(_diagnostic(
                    "special-file", relative, "entry is not a regular file or directory",
                    "Replace it with a regular file or remove it from the scan root."))
                continue
            record = _file_record(relative, before["size"])
            records.append(record)
            if relative in wanted:
                found_wanted.add(relative)
            if record["language"] != "Python":
                continue
            if not parsing_open:
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    "analysis-stopped", relative,
                    "Python analysis stopped after an earlier limit",
                    "Narrow the scan and address the earlier diagnostic."))
                continue
            if before["size"] > MAX_SOURCE:
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    "source-limit", relative,
                    f"source is {before['size']} bytes; limit is {MAX_SOURCE}",
                    "Split the source or inspect a narrower set of files."))
                continue
            if total_bytes + before["size"] > MAX_TOTAL_READ:
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    "total-read-limit", relative,
                    f"reading this file would exceed {MAX_TOTAL_READ} bytes",
                    "Narrow the filesystem root; the limit is fixed for this scan."))
                parsing_open = False
                continue
            remaining_time = deadline - time.monotonic()
            if remaining_time <= 0:
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    "parser-total-time-limit", relative,
                    f"parser time limit {PARSER_SECONDS:g} seconds reached",
                    "Narrow the filesystem root or reduce the Python source set."))
                parsing_open = False
                continue
            read_count = [0]
            try:
                data = filesystem.read_file(
                    folder_fd, before, MAX_TOTAL_READ - total_bytes, read_count)
            except (OverflowError, _WindowsLimit) as exc:
                record["analysis"] = "incomplete"
                code = "source-limit" if "per-file" in str(exc) else "total-read-limit"
                diagnostics.append(_diagnostic(
                    code, relative, str(exc),
                    "Narrow the filesystem root; the limit is fixed for this scan."))
                parsing_open = False
                continue
            except (OSError, _WindowsUnavailable) as exc:
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    "file-read-or-race", relative, str(exc),
                    "Retry against a stable tree containing only regular files."))
                continue
            finally:
                total_bytes += read_count[0]
            timeout = min(PER_FILE_SECONDS, remaining_time)
            try:
                parsed, elapsed = _parse_file(
                    data, MAX_AST_NODES - total_nodes,
                    MAX_SYMBOLS - total_definitions, timeout)
            except subprocess.TimeoutExpired:
                elapsed = timeout
                parsed = {"ok": False, "error": "parser-file-time-limit"}
            parser_time += elapsed
            result["budgets"]["parser_seconds"] = round(parser_time, 3)
            result["budgets"]["bytes_read"] = total_bytes
            if not parsed.get("ok"):
                code = parsed.get("error", "parser-worker-failed")
                if code == "ast-node-limit":
                    total_nodes += int(parsed.get("nodes", 0))
                if code == "symbol-limit":
                    total_definitions += int(parsed.get("definitions", 0))
                    total_nodes += int(parsed.get("nodes", 0))
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    code, relative, parsed.get("message", code),
                    "Correct the source or narrow the scan; do not treat missing analysis as clean."))
                if code in ("parser-file-time-limit", "ast-node-limit",
                            "symbol-limit"):
                    parsing_open = code != "parser-file-time-limit"
                    if code in ("ast-node-limit", "symbol-limit"):
                        parsing_open = False
                continue
            nodes = int(parsed["nodes"])
            total_nodes += nodes
            total_definitions += int(parsed["definitions"])
            result["budgets"]["ast_nodes"] = total_nodes
            for symbol in parsed["symbols"]:
                symbol["path"] = relative
                if symbol["kind"] == "function":
                    symbol_rows.append(symbol)
            record["analysis"] = "parsed"
            record["public"] = [
                {key: symbol[key] for key in
                 ("name", "qualified_name", "kind", "line", "summary")}
                for symbol in parsed["symbols"]
                if symbol["public"]
            ]
    visit(root_fd, "")
    result["budgets"].update({
        "entries_seen": entries,
        "bytes_read": total_bytes,
        "ast_nodes": total_nodes,
        "symbols": total_definitions,
        "parser_seconds": round(parser_time, 3),
    })
    result["components"] = sorted(dirs_seen)
    result["files"] = records
    result["diagnostics"].extend(
        _diagnostic("changed-path-missing", path,
                    "requested changed path was not found as a contained regular file",
                    "Pass a root-relative regular file path present in the scanned tree.")
        for path in sorted(wanted - found_wanted)
    )
    if args["release"] or wanted:
        focal = [row for row in symbol_rows
                 if args["release"] or row["path"] in wanted]
        result["neighbors"], result["sampling"] = _neighbors(
            symbol_rows, focal, args["release"])
        result["budgets"]["comparisons"] = result["sampling"]["compared"]
    result["status"] = "incomplete" if result["diagnostics"] else "complete"
    return result


def _counter_similarity(left: dict[str, int], right: dict[str, int]) -> float:
    keys = left.keys() | right.keys()
    denom = sum(max(left.get(key, 0), right.get(key, 0)) for key in keys)
    if not denom:
        return 1.0
    return sum(min(left.get(key, 0), right.get(key, 0)) for key in keys) / denom


def _name_similarity(left: list[str], right: list[str]) -> float:
    a, b = set(left), set(right)
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def _similarity(left: dict[str, Any], right: dict[str, Any]) -> float:
    shape = _counter_similarity(left["shape"], right["shape"])
    names = _name_similarity(left["names"], right["names"])
    return 0.7 * shape + 0.3 * names


def _neighbors(all_symbols: list[dict[str, Any]], focal: list[dict[str, Any]],
               release: bool) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = sorted(all_symbols, key=lambda row: (row["path"], row["line"], row["name"]))
    positions = {id(row): index for index, row in enumerate(rows)}
    focal = sorted(focal, key=lambda row: (row["path"], row["line"], row["name"]))
    candidate_count = max(0, len(rows) - 1)
    total = (len(rows) * (len(rows) - 1) // 2 if release else
             len(focal) * candidate_count)
    budget = min(total, MAX_COMPARISONS)
    ranked: dict[int, list[tuple[float, dict[str, Any]]]] = collections.defaultdict(list)

    def keep(index: int, score: float, other: dict[str, Any]) -> None:
        choices = ranked[index]
        choices.append((score, other))
        choices.sort(key=lambda pair: (
            -pair[0], pair[1]["path"], pair[1]["line"], pair[1]["name"]))
        del choices[5:]

    comparisons = 0
    if release:
        # Evenly sample the lexicographically ordered unordered-pair population.
        total_pairs = total
        if budget:
            for sample in range(budget):
                pair_index = (sample * (total_pairs - 1) // (budget - 1)
                              if budget > 1 else 0)
                low, high = 0, len(rows) - 1
                while low < high:
                    mid = (low + high + 1) // 2
                    prefix = mid * (2 * len(rows) - mid - 1) // 2
                    if prefix <= pair_index:
                        low = mid
                    else:
                        high = mid - 1
                i = low
                prefix = i * (2 * len(rows) - i - 1) // 2
                j = i + 1 + (pair_index - prefix)
                score = _similarity(rows[i], rows[j])
                keep(i, score, rows[j])
                keep(j, score, rows[i])
                comparisons += 1
    elif focal:
        per_focus = budget // len(focal)
        extra = budget % len(focal)
        for focus_index, item in enumerate(focal):
            i = positions[id(item)]
            quota = min(candidate_count, per_focus + (focus_index < extra))
            if not quota:
                continue
            for sample in range(quota):
                candidate_index = (sample * (candidate_count - 1) // (quota - 1)
                                   if quota > 1 else 0)
                other_index = candidate_index if candidate_index < i else candidate_index + 1
                other = rows[other_index]
                score = _similarity(item, other)
                keep(i, score, other)
                comparisons += 1
    neighbor_rows: list[dict[str, Any]] = []
    focus_rows = rows if release else focal
    for item in focus_rows:
        index = positions[id(item)]
        ranked_items = sorted(
            ranked.get(index, []),
            key=lambda pair: (-pair[0], pair[1]["path"], pair[1]["line"], pair[1]["name"]),
        )[:5]
        neighbor_rows.append({
            "function": {key: item[key] for key in
                         ("path", "line", "qualified_name", "kind")},
            "neighbors": [
                {"score": round(score, 4), "path": other["path"],
                 "line": other["line"], "qualified_name": other["qualified_name"],
                 "kind": other["kind"]}
                for score, other in ranked_items
            ],
        })
    return neighbor_rows, {
        "algorithm": "evenly spaced deterministic sampling over sorted pair population; "
                     "score=0.7 multiset Jaccard of AST-node types + 0.3 Jaccard of lowercase "
                     "snake/camel identifier tokens",
        "population": total,
        "compared": comparisons,
        "unsampled": max(0, total - comparisons),
        "truncated": total > comparisons,
    }


def _scan_worker() -> int:
    args = json.loads(sys.argv[2])
    root_name = os.path.abspath(args["root"])
    result = _empty_result(root_name, "filesystem")
    if os.name == "nt":
        global _WINDOWS_WORKER_JOB
        try:
            api = _WindowsAPI()
            _WINDOWS_WORKER_JOB = api.install_worker_job()
        except _WindowsUnavailable as exc:
            result["diagnostics"].append(_diagnostic(
                "secure-traversal-unavailable", root_name, str(exc),
                "Use 64-bit Python on a local NTFS volume with the required system APIs."))
            return _write_result(result, 1)
        try:
            root_handles, _filesystem = api.admit_root(root_name)
        except _WindowsUnavailable as exc:
            result["diagnostics"].append(_diagnostic(
                "root-open", root_name, str(exc),
                "Use an existing local NTFS directory reached through a plain drive path."))
            return _write_result(result, 2)
        try:
            result = _walk(root_handles[-1], root_name, args,
                           _WindowsFilesystem(api))
        finally:
            for handle in reversed(root_handles):
                api.close(handle)
        return _write_result(result, 1 if result["status"] == "incomplete" else 0)
    if not _secure_walk_available():
        result["diagnostics"].append(_diagnostic(
            "secure-traversal-unavailable", root_name,
            "this platform lacks descriptor-relative no-follow directory traversal",
            "Run on a platform with openat-style O_NOFOLLOW traversal; no weaker fallback is used."))
        return _write_result(result, 1)
    try:
        root_fd = _open_absolute_directory(root_name)
    except OSError as exc:
        result["diagnostics"].append(_diagnostic(
            "root-open", root_name, str(exc),
            "Use an existing directory whose path contains no links or reparse points."))
        return _write_result(result, 2)
    try:
        result = _walk(root_fd, root_name, args)
    finally:
        os.close(root_fd)
    return _write_result(result, 1 if result["status"] == "incomplete" else 0)


def _supervise_scan(args: dict[str, Any]) -> int:
    command = [sys.executable, "-I", os.path.abspath(__file__),
               _WORKER_SCAN, json.dumps(args, ensure_ascii=True)]
    kwargs: dict[str, Any] = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "env": {"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
    }
    if os.name == "posix":
        kwargs["start_new_session"] = True
    started = time.monotonic()
    process = subprocess.Popen(command, **kwargs)
    try:
        stdout, stderr = process.communicate(timeout=COMMAND_SECONDS)
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        process.communicate()
        result = _empty_result(os.path.abspath(args["root"]), "filesystem")
        result["budgets"]["command_seconds"] = round(
            time.monotonic() - started, 3)
        result["diagnostics"].append(_diagnostic(
            "command-time-limit", result["root"],
            f"complete command exceeded {COMMAND_SECONDS:g} seconds",
            "Narrow the filesystem root; the limit is fixed for this scan."))
        return _write_result(result, 1)
    if stdout:
        elapsed = time.monotonic() - started
        try:
            result = json.loads(stdout.decode("ascii"))
        except (UnicodeError, json.JSONDecodeError):
            result = _empty_result(os.path.abspath(args["root"]), "filesystem")
            result["diagnostics"].append(_diagnostic(
                "collector-worker-failed", result["root"],
                "worker returned invalid JSON",
                "Retry with the canonical Python interpreter and a readable root."))
            return _write_result(result, 2)
        result["budgets"]["command_seconds"] = round(elapsed, 3)
        return _write_result(result, process.returncode or 0)
    result = _empty_result(os.path.abspath(args["root"]), "filesystem")
    result["diagnostics"].append(_diagnostic(
        "collector-worker-failed", result["root"],
        stderr.decode("ascii", "backslashreplace")[:500],
        "Retry with the canonical Python interpreter and a readable root."))
    return _write_result(result, 2)


def _changed_paths(paths: list[str]) -> tuple[list[str], list[str]]:
    accepted: list[str] = []
    rejected: list[str] = []
    for raw in paths:
        path = PurePosixPath(raw)
        if (path.is_absolute() or not path.parts
                or any(part in ("", ".", "..") for part in path.parts)
                or "\\" in raw):
            rejected.append(raw)
        else:
            accepted.append(path.as_posix())
    return accepted, rejected


def main(argv: list[str] | None = None) -> int:
    if len(sys.argv) > 1 and sys.argv[1] == _WORKER_PARSE:
        return _parse_source_worker()
    if len(sys.argv) > 1 and sys.argv[1] == _WORKER_SCAN:
        return _scan_worker()
    parser = argparse.ArgumentParser(
        prog="code_map", description="Bounded filesystem map and reuse leads.")
    parser.add_argument("--root", default=".", help="filesystem root to inspect")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--changed", action="append", default=[], metavar="PATH",
                      help="root-relative changed Python file; repeat as needed")
    mode.add_argument("--release", action="store_true",
                      help="compare the whole tree using the bounded pair sample")
    args = parser.parse_args(argv)
    changed, rejected = _changed_paths(args.changed)
    root = os.path.abspath(args.root)
    packed = {"root": root, "changed": changed, "release": bool(args.release)}
    if rejected:
        result = _empty_result(root, "changed")
        result["diagnostics"].extend(
            _diagnostic("invalid-changed-path", path,
                        "changed paths must be root-relative and contain no parent traversal",
                        "Pass a regular file path relative to --root.")
            for path in rejected
        )
        return _write_result(result, 2)
    return _supervise_scan(packed)


if __name__ == "__main__":
    raise SystemExit(main())
