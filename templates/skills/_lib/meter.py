#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Meter reader and ledger primitives; live source collection remains disabled.

Internal bounded readers accept only explicitly supplied paths and bytes, and
current refresh tests use synthetic roots/files and a synthetic account home.
The CLI resolves consent from the fixed OS account home and stops before source,
project, Git, or ledger access. Normalized events remain unknown globally and
live project reporting is not wired.
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
import secrets
import struct
from fractions import Fraction
from decimal import Decimal
try:
    import pwd
except ImportError:  # vendor-ok: POSIX account lookup is deliberately unsupported elsewhere
    pwd = None
try:
    import fcntl
except ImportError:  # vendor-ok: private ledger locking is deliberately unsupported elsewhere
    fcntl = None
from datetime import datetime, timezone, timedelta
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit, urlunsplit


READER_VERSION = "cairn-source-readers/4"
_LEGACY_READER_VERSION = "cairn-source-readers/3"
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
LEDGER_SCHEMA = "cairn-meter-ledger/4"
_LEGACY_LEDGER_SCHEMA = "cairn-meter-ledger/3"
RATIO_VERSION = "cairn-api-token-index/2026-11-06"
_RATIO_INDEX = {
    "version": RATIO_VERSION,
    "profile": "Hypothetical first-party Standard/global API text-token reference profile; excludes tools, taxes, discounts, and subscriptions.",
    "reference_model": "claude-haiku-4-5-20251001",
    "reference_kind": "fresh_input",
    "reference_rate": "1",
    "currency": "USD",
    "denominator_tokens": 1_000_000,
    "as_of": "2026-11-06",
    "sources": [
        "https://platform.claude.com/docs/en/models/haiku-4-5/overview",
        "https://platform.claude.com/docs/en/models/sonnet-4-6/overview",
        "https://platform.claude.com/docs/en/models/opus-5-5/overview",
        "https://developers.openai.com/api/docs/models/gpt-5.3-codex",
        "https://platform.claude.com/docs/en/build-with-claude/prompt-caching#1-hour-cache-duration",
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
    },
}
MAX_SOURCE_ROOT_DEPTH = 32
MAX_REFRESH_ENTRIES = 100_000
MAX_SOURCE_FILES = 10_000
MAX_TOTAL_SOURCE_BYTES = 256 * 1024 * 1024
MAX_RETAINED_EVENTS = 100_000
MAX_RETAINED_WAITS = 100_000
MAX_WAIT_OCCURRENCES = 100_000
MAX_WAIT_EXPORT_WORK = 100_000
MAX_CLAIM_BYTES = 8 * 1024 * 1024
MAX_CLAIM_LINE = 64 * 1024
MAX_LEDGER_BYTES = 64 * 1024 * 1024
LEDGER_NAME = "ledger.json"
LEDGER_LOCK_NAME = "ledger.lock"
_PRIVATE_FS_SUPPORTED = os.name == "posix"


class Unavailable(Exception):
    """A closed, non-sensitive failure used at the CLI boundary."""

    def __init__(self, reason="unavailable"):
        self.reason = reason if re.fullmatch(r"[a-z][a-z0-9_]*", reason or "") else "unavailable"
        super().__init__(self.reason)


class _MissingConfig(Exception):
    """The opt-in file or its private directory has not been created."""


def _windows_config_decision(config_bytes):
    """Return only disabled or unavailable; Windows collection is unsupported."""
    if config_bytes is None:
        return "disabled"
    try:
        config = validate_config_bytes(config_bytes)
    except Unavailable:
        return "unavailable"
    return "disabled" if not config["enabled"] else "unavailable"


class _WindowsConsentAPI:
    """Fixed-path local NTFS consent reader using parent-relative held handles."""

    def __init__(self):
        import ctypes as C
        from ctypes import wintypes as W

        if os.name != "nt" or C.sizeof(C.c_void_p) != 8:
            raise Unavailable
        try:
            self.C, self.W = C, W
            self.nt = C.WinDLL("ntdll.dll", winmode=0x800, use_last_error=True)
            self.kernel = C.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
            self.advapi = C.WinDLL("advapi32.dll", winmode=0x800, use_last_error=True)
            self.userenv = C.WinDLL("userenv.dll", winmode=0x800, use_last_error=True)
        except (AttributeError, OSError):
            raise Unavailable from None

        class US(C.Structure):
            _fields_ = [("Length", W.USHORT), ("MaximumLength", W.USHORT),
                        ("Buffer", C.c_void_p)]

        class OA(C.Structure):
            _fields_ = [("Length", W.ULONG), ("RootDirectory", C.c_void_p),
                        ("ObjectName", C.POINTER(US)), ("Attributes", W.ULONG),
                        ("SecurityDescriptor", C.c_void_p),
                        ("SecurityQualityOfService", C.c_void_p)]

        class IOS(C.Structure):
            class U(C.Union):
                _fields_ = [("Status", C.c_int32), ("Pointer", C.c_void_p)]
            _fields_ = [("u", U), ("Information", C.c_size_t)]

        class BHI(C.Structure):
            _fields_ = [("attributes", W.DWORD), ("created", W.FILETIME),
                        ("accessed", W.FILETIME), ("written", W.FILETIME),
                        ("volume", W.DWORD), ("size_high", W.DWORD),
                        ("size_low", W.DWORD), ("links", W.DWORD),
                        ("id_high", W.DWORD), ("id_low", W.DWORD)]

        class BASIC_INFO(C.Structure):
            _fields_ = [("created", C.c_int64), ("accessed", C.c_int64),
                        ("written", C.c_int64), ("changed", C.c_int64),
                        ("attributes", W.DWORD)]

        if (C.sizeof(US), C.sizeof(OA), C.sizeof(IOS), C.sizeof(BHI),
                C.sizeof(BASIC_INFO), struct.calcsize("<II6qIIIbx24s2xq")) != (
                    16, 48, 16, 52, 40, 104):
            raise Unavailable
        self.US, self.OA, self.IOS, self.BHI, self.BASIC_INFO = US, OA, IOS, BHI, BASIC_INFO
        H = C.c_void_p
        self.nt.NtCreateFile.argtypes = [C.POINTER(H), W.ULONG, C.POINTER(OA),
            C.POINTER(IOS), C.c_void_p, W.ULONG, W.ULONG, W.ULONG, W.ULONG,
            C.c_void_p, W.ULONG]
        self.nt.NtCreateFile.restype = C.c_int32
        self.kernel.GetCurrentThread.argtypes = []
        self.kernel.GetCurrentThread.restype = H
        self.kernel.GetCurrentProcess.argtypes = []
        self.kernel.GetCurrentProcess.restype = H
        self.kernel.CloseHandle.argtypes = [H]
        self.kernel.CloseHandle.restype = W.BOOL
        self.kernel.QueryDosDeviceW.argtypes = [W.LPCWSTR, W.LPWSTR, W.DWORD]
        self.kernel.QueryDosDeviceW.restype = W.DWORD
        self.kernel.GetFileType.argtypes = [H]
        self.kernel.GetFileType.restype = W.DWORD
        self.kernel.GetFileInformationByHandle.argtypes = [H, C.POINTER(BHI)]
        self.kernel.GetFileInformationByHandle.restype = W.BOOL
        self.kernel.GetFileInformationByHandleEx.argtypes = [H, C.c_int, C.c_void_p, W.DWORD]
        self.kernel.GetFileInformationByHandleEx.restype = W.BOOL
        self.kernel.ReadFile.argtypes = [H, C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.c_void_p]
        self.kernel.ReadFile.restype = W.BOOL
        self.kernel.GetVolumeInformationByHandleW.argtypes = [
            H, W.LPWSTR, W.DWORD, C.POINTER(W.DWORD), C.POINTER(W.DWORD),
            C.POINTER(W.DWORD), W.LPWSTR, W.DWORD]
        self.kernel.GetVolumeInformationByHandleW.restype = W.BOOL
        self.kernel.LocalFree.argtypes = [H]
        self.kernel.LocalFree.restype = H
        self.advapi.OpenThreadToken.argtypes = [H, W.DWORD, W.BOOL, C.POINTER(H)]
        self.advapi.OpenThreadToken.restype = W.BOOL
        self.advapi.OpenProcessToken.argtypes = [H, W.DWORD, C.POINTER(H)]
        self.advapi.OpenProcessToken.restype = W.BOOL
        self.advapi.GetTokenInformation.argtypes = [
            H, C.c_int, C.c_void_p, W.DWORD, C.POINTER(W.DWORD)]
        self.advapi.GetTokenInformation.restype = W.BOOL
        self.userenv.GetUserProfileDirectoryW.argtypes = [H, W.LPWSTR, C.POINTER(W.DWORD)]
        self.userenv.GetUserProfileDirectoryW.restype = W.BOOL
        self.advapi.GetSecurityInfo.argtypes = [
            H, C.c_int, W.DWORD, C.POINTER(C.c_void_p), C.POINTER(C.c_void_p),
            C.POINTER(C.c_void_p), C.POINTER(C.c_void_p), C.POINTER(C.c_void_p)]
        self.advapi.GetSecurityInfo.restype = W.DWORD
        self.advapi.IsValidSid.argtypes = [C.c_void_p]
        self.advapi.IsValidSid.restype = W.BOOL
        self.advapi.GetLengthSid.argtypes = [C.c_void_p]
        self.advapi.GetLengthSid.restype = W.DWORD
        self.advapi.ConvertStringSidToSidW.argtypes = [W.LPCWSTR, C.POINTER(C.c_void_p)]
        self.advapi.ConvertStringSidToSidW.restype = W.BOOL

    def close(self, handle):
        if handle:
            self.kernel.CloseHandle(self.C.c_void_p(handle))

    def _sid_bytes(self, sid):
        if not sid or not self.advapi.IsValidSid(sid):
            raise Unavailable
        size = int(self.advapi.GetLengthSid(sid))
        if not 8 <= size <= 68:
            raise Unavailable
        return self.C.string_at(sid, size)

    def current_user_profile(self):
        C, W = self.C, self.W
        thread, process = C.c_void_p(), C.c_void_p()
        try:
            if self.advapi.OpenThreadToken(self.kernel.GetCurrentThread(), 0x0008, True,
                                           C.byref(thread)):
                raise Unavailable  # Refuse impersonation.
            if C.get_last_error() != 1008:  # Only ERROR_NO_TOKEN means no impersonation.
                raise Unavailable
            if not self.advapi.OpenProcessToken(self.kernel.GetCurrentProcess(), 0x0008,
                                                C.byref(process)):
                raise Unavailable
            needed = W.DWORD()
            if self.advapi.GetTokenInformation(process, 1, None, 0, C.byref(needed)):
                raise Unavailable
            if C.get_last_error() != 122:  # ERROR_INSUFFICIENT_BUFFER is expected here.
                raise Unavailable
            if not 16 <= needed.value <= 4096:
                raise Unavailable
            token_user = C.create_string_buffer(needed.value)
            if not self.advapi.GetTokenInformation(process, 1, token_user,
                                                   needed.value, C.byref(needed)):
                raise Unavailable
            user_sid = self._sid_bytes(C.c_void_p.from_buffer(token_user).value)
            chars = W.DWORD()
            if self.userenv.GetUserProfileDirectoryW(process, None, C.byref(chars)):
                raise Unavailable
            if C.get_last_error() != 122:
                raise Unavailable
            if not 2 <= chars.value <= 32768:
                raise Unavailable
            path = C.create_unicode_buffer(chars.value)
            if not self.userenv.GetUserProfileDirectoryW(process, path, C.byref(chars)):
                raise Unavailable
            if (len(path.value) > 32760 or "\x00" in path.value
                    or chars.value != len(path.value) + 1):
                raise Unavailable
            return path.value, user_sid
        except (OSError, ValueError, TypeError, AttributeError):
            raise Unavailable from None
        finally:
            self.close(thread.value)
            self.close(process.value)

    def _privileged_sid(self, sid_bytes, *, ancestor=False):
        C = self.C
        values = ["S-1-5-18", "S-1-5-32-544"]
        if ancestor:
            values.append("S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464")
        for value in values:
            sid = C.c_void_p()
            if not self.advapi.ConvertStringSidToSidW(value, C.byref(sid)):
                raise Unavailable
            try:
                if self._sid_bytes(sid) == sid_bytes:
                    return True
            finally:
                self.kernel.LocalFree(sid)
        return False

    def info(self, handle):
        value = self.BHI()
        if (self.kernel.GetFileType(handle) != 1 or
                not self.kernel.GetFileInformationByHandle(handle, self.C.byref(value))):
            raise Unavailable
        attrs = int(value.attributes)
        if attrs & (0x400 | 0x40 | 0x1000 | 0x40000 | 0x400000):
            raise Unavailable
        stamp = lambda item: (int(item.dwHighDateTime) << 32) | int(item.dwLowDateTime)
        basic = self.BASIC_INFO()
        if not self.kernel.GetFileInformationByHandleEx(
                handle, 0, self.C.byref(basic), self.C.sizeof(basic)):
            raise Unavailable
        def unix_ns(filetime):
            result = (int(filetime) - 116444736000000000) * 100
            if not -(1 << 63) <= result <= (1 << 63) - 1:
                raise Unavailable
            return result
        volume, file_id = int(value.volume), (int(value.id_high) << 32) | int(value.id_low)
        if not 0 <= volume <= (1 << 64) - 1 or not 0 <= file_id <= (1 << 64) - 1:
            raise Unavailable
        return {"identity": (int(value.volume), (int(value.id_high) << 32) | int(value.id_low)),
                "size": (int(value.size_high) << 32) | int(value.size_low),
                "directory": bool(attrs & 0x10), "links": int(value.links),
                "created": stamp(value.created), "accessed": stamp(value.accessed),
                "written": unix_ns(basic.written), "changed": unix_ns(basic.changed),
                "mtime_ns": unix_ns(basic.written), "ctime_ns": unix_ns(basic.changed)}

    def open(self, name, parent=None, *, directory=False, read_data=False):
        C = self.C
        if parent is not None and (not name or name in {".", ".."} or
                any(ch in name for ch in "\\/:") or "\0" in name or
                len(name.encode("utf-16-le")) > 510):
            raise Unavailable
        text = C.create_unicode_buffer(name)
        length = len(name.encode("utf-16-le"))
        us = self.US(length, length + 2, C.cast(text, C.c_void_p))
        oa = self.OA(C.sizeof(self.OA), parent, C.pointer(us), 0, None, None)
        ios, out = self.IOS(), C.c_void_p()
        access = 0x80 | 0x20000 | 0x100000 | (0x1 if directory or read_data else 0)
        options = 0x00200000 | 0x00400000 | 0x20 | (0x1 if directory else 0x40)
        status = self.nt.NtCreateFile(C.byref(out), access, C.byref(oa), C.byref(ios),
                                      None, 0, 1, 1, options, None, 0)
        code = status & 0xffffffff
        if status != 0:
            if code in (0xC0000034, 0xC000003A):
                raise _MissingConfig
            raise Unavailable
        return int(out.value)

    def enumerate(self, parent, remaining):
        """List one held NTFS directory with checked FILE_ID_BOTH_DIR_INFO rows."""
        if type(remaining) is not int or remaining < 0:
            raise Unavailable("source_budget_exceeded")
        before = self.info(parent)
        if not before["directory"]:
            raise Unavailable("source_read_unavailable")
        C = self.C
        size = 64 * 1024
        buffer = (C.c_uint64 * (size // 8))()
        first, calls, seen, rows = True, 0, set(), []
        while True:
            calls += 1
            if calls > remaining + 2:
                raise Unavailable("source_budget_exceeded")
            C.memset(C.addressof(buffer), 0, size)
            if not self.kernel.GetFileInformationByHandleEx(
                    parent, 11 if first else 10, buffer, size):
                error = C.get_last_error()
                if error == 18:  # ERROR_NO_MORE_FILES
                    break
                raise Unavailable("source_read_unavailable")
            first = False
            for row in _decode_windows_directory_entries(C.string_at(buffer, size)):
                name = row["name"]
                if name in {".", ".."}:
                    continue
                if name in seen:
                    raise Unavailable("source_changed")
                seen.add(name)
                if row["reparse"] or row["device"] or row["offline"] or row["recall"]:
                    raise Unavailable("source_read_unavailable")
                rows.append(row)
                if len(rows) > remaining:
                    raise Unavailable("source_budget_exceeded")
        after = self.info(parent)
        if ({key: value for key, value in before.items() if key != "accessed"}
                != {key: value for key, value in after.items() if key != "accessed"}):
            raise Unavailable("source_changed")
        return sorted(rows, key=lambda item: item["name"])

    def check_acl(self, handle, user_sid, role):
        C = self.C
        owner, dacl, sd = C.c_void_p(), C.c_void_p(), C.c_void_p()
        status = self.advapi.GetSecurityInfo(handle, 1, 0x1 | 0x4, C.byref(owner),
            None, C.byref(dacl), None, C.byref(sd))
        try:
            if status or not owner.value or not dacl.value:
                raise Unavailable
            owner_bytes = self._sid_bytes(owner)
            if role in {"profile", "cairn", "config"} and owner_bytes != user_sid:
                raise Unavailable
            if role == "ancestor" and owner_bytes != user_sid and not self._privileged_sid(
                    owner_bytes, ancestor=True):
                raise Unavailable
            header = C.string_at(dacl, 8)
            revision, _sbz, acl_size, count = struct.unpack("<BBHH", header[:6])
            if revision not in (2, 4) or not 8 <= acl_size <= 65535 or count > 1024:
                raise Unavailable
            raw = C.string_at(dacl, acl_size)
            offset = 8
            ancestor_denied = 0x40 | 0x10000 | 0x40000 | 0x80000 | 0x10000000 | 0x40000000
            profile_denied = ancestor_denied | 0x2 | 0x4 | 0x10 | 0x100
            for _ in range(count):
                if offset + 8 > len(raw):
                    raise Unavailable
                kind, flags, size = struct.unpack_from("<BBH", raw, offset)
                if (kind != 0 or flags & ~0x1F or size < 16 or size % 4
                        or offset + size > len(raw)):
                    raise Unavailable
                mask = struct.unpack_from("<I", raw, offset + 4)[0]
                ace_sid = self._sid_bytes(C.c_void_p(dacl.value + offset + 8))
                if len(ace_sid) > size - 8:
                    raise Unavailable
                if not flags & 0x08:  # INHERIT_ONLY does not apply to this object.
                    if ace_sid != user_sid and not self._privileged_sid(
                            ace_sid, ancestor=(role == "ancestor")):
                        forbidden = (ancestor_denied if role == "ancestor" else
                                     profile_denied if role == "profile" else 0xffffffff)
                        if mask & forbidden:
                            raise Unavailable
                offset += size
            if offset > acl_size:
                raise Unavailable
        finally:
            if sd:
                self.kernel.LocalFree(sd)

    def read_config(self, profile, user_sid):
        import ntpath
        drive, tail = ntpath.splitdrive(profile)
        parts = tail[1:].split("\\") if tail.startswith("\\") else []
        if (not re.fullmatch(r"[A-Za-z]:", drive) or profile.startswith("\\\\")
                or not parts or any(not p or p in {".", ".."} for p in parts)):
            raise Unavailable
        targets = self.C.create_unicode_buffer(32768)
        if not self.kernel.QueryDosDeviceW(drive, targets, len(targets)):
            raise Unavailable
        device = targets.value
        if not re.fullmatch(r"\\Device\\HarddiskVolume[0-9]+", device):
            raise Unavailable
        held = []
        try:
            try:
                current = self.open(device + "\\", directory=True)
            except _MissingConfig:
                raise Unavailable from None
            held.append(current)
            if not self.info(current)["directory"]:
                raise Unavailable
            fs_name = self.C.create_unicode_buffer(64)
            serial, max_component, flags = self.W.DWORD(), self.W.DWORD(), self.W.DWORD()
            if not self.kernel.GetVolumeInformationByHandleW(
                    current, None, 0, self.C.byref(serial), self.C.byref(max_component),
                    self.C.byref(flags), fs_name, len(fs_name)) or fs_name.value != "NTFS":
                raise Unavailable
            self.check_acl(current, user_sid, "ancestor")
            for index, part in enumerate(parts):
                try:
                    child = self.open(part, current, directory=True)
                except _MissingConfig:
                    raise Unavailable from None
                held.append(child)
                current = child
                self.check_acl(child, user_sid, "profile" if index == len(parts) - 1 else "ancestor")
            try:
                cairn = self.open(".cairn", current, directory=True)
            except _MissingConfig:
                return None
            held.append(cairn)
            self.check_acl(cairn, user_sid, "cairn")
            try:
                config = self.open("meter.json", cairn, read_data=True)
            except _MissingConfig:
                return None
            held.append(config)
            before = self.info(config)
            if before["directory"] or before["links"] != 1 or before["size"] > MAX_CONFIG_BYTES:
                raise Unavailable
            self.check_acl(config, user_sid, "config")
            blocks, total = [], 0
            while True:
                buf = self.C.create_string_buffer(min(65536, MAX_CONFIG_BYTES + 1 - total))
                got = self.W.DWORD()
                if not self.kernel.ReadFile(config, buf, len(buf), self.C.byref(got), None):
                    raise Unavailable
                if not got.value:
                    break
                total += int(got.value)
                if total > MAX_CONFIG_BYTES:
                    raise Unavailable
                blocks.append(buf.raw[:got.value])
            after = self.info(config)
            self.check_acl(config, user_sid, "config")
            stable_before = {key: value for key, value in before.items()
                             if key != "accessed"}
            stable_after = {key: value for key, value in after.items()
                            if key != "accessed"}
            if stable_before != stable_after or total != before["size"]:
                raise Unavailable
            return b"".join(blocks)
        finally:
            for handle in reversed(held):
                self.close(handle)


def _decode_windows_directory_entries(raw):
    """Decode the bounded NTFS directory layout without trusting host paths."""
    header = struct.Struct("<II6qIIIbx24s2xq")
    if not isinstance(raw, bytes) or len(raw) != 64 * 1024:
        raise Unavailable("source_read_unavailable")
    rows, offset = [], 0
    while True:
        if len(raw) - offset < header.size:
            raise Unavailable("source_read_unavailable")
        row = header.unpack_from(raw, offset)
        step, name_bytes = row[0], row[9]
        end = offset + header.size + name_bytes
        if not name_bytes or name_bytes % 2 or name_bytes > 510 or end > len(raw) or row[6] < 0:
            raise Unavailable("source_read_unavailable")
        if step and (step % 8 or step < header.size + name_bytes
                     or offset + step >= len(raw)):
            raise Unavailable("source_read_unavailable")
        try:
            name = raw[offset + header.size:end].decode("utf-16-le", errors="strict")
        except UnicodeError:
            raise Unavailable("source_read_unavailable") from None
        if (not name or any(char in "\\/:\x00" or ord(char) < 32 or ord(char) == 127
                            for char in name)
                or (name not in {".", ".."} and name.endswith((".", " ")))
                or len(name.encode("utf-16-le")) > 510):
            raise Unavailable("source_read_unavailable")
        attrs = int(row[8])
        file_id = row[13] if row[13] >= 0 else row[13] + (1 << 64)
        rows.append({"name": name, "file_id": file_id, "size": row[6],
                     "directory": bool(attrs & 0x10), "attributes": attrs,
                     "reparse": bool(attrs & 0x400), "device": bool(attrs & 0x40),
                     "offline": bool(attrs & 0x1000),
                     "recall": bool(attrs & (0x40000 | 0x400000))})
        if not step:
            return rows
        offset += step


def _windows_config_status(api=None):
    """Resolve fixed OS consent only; collection remains unsupported on Windows."""
    try:
        api = _WindowsConsentAPI() if api is None else api
        profile, sid = api.current_user_profile()
        return _windows_config_decision(api.read_config(profile, sid))
    except (_MissingConfig, Unavailable, OSError, ValueError, TypeError, AttributeError):
        return "unavailable"


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
        self.bytes_read = 0
        self.complete_lines = 0
        self.open_identity = None
        self.final_identity = None

    def __iter__(self):
        if self._started:
            self.terminal_reason = "source_read_unavailable"
            return
        self._started = True
        directory_fd = file_fd = -1
        directory_fds = []
        parent_links = []
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
            root_info = os.fstat(directory_fd)
            root_identity = (root_info.st_dev, root_info.st_ino)
            directory_fds.append(directory_fd)
            for part in parts[:-1]:
                before_dir = os.stat(part, dir_fd=directory_fd, follow_symlinks=False)
                if not stat.S_ISDIR(before_dir.st_mode):
                    reason = "source_changed"
                    return
                next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                  dir_fd=directory_fd)
                opened_dir = os.fstat(next_fd)
                if ((opened_dir.st_dev, opened_dir.st_ino)
                        != (before_dir.st_dev, before_dir.st_ino)):
                    os.close(next_fd)
                    reason = "source_changed"
                    return
                parent_links.append((directory_fd, part,
                                     before_dir.st_dev, before_dir.st_ino))
                directory_fds.append(next_fd)
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
            self.open_identity = {
                "dev": opened.st_dev, "ino": opened.st_ino,
                "size": opened.st_size, "mtime_ns": opened.st_mtime_ns,
                "ctime_ns": opened.st_ctime_ns,
            }
            total = line_count = 0
            pending = b""
            while True:
                block = os.read(file_fd, min(64 * 1024, self.budget - total + 1))
                if not block:
                    break
                total += len(block)
                self.bytes_read = total
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
                    self.complete_lines = line_count
                    if line_count > MAX_BATCH_LINES:
                        reason = "source_budget_exceeded"
                        return
                    yield line
            after = os.fstat(file_fd)
            self.final_identity = {
                "dev": after.st_dev, "ino": after.st_ino,
                "size": after.st_size, "mtime_ns": after.st_mtime_ns,
                "ctime_ns": after.st_ctime_ns,
            }
            named_file = os.stat(leaf, dir_fd=directory_fd, follow_symlinks=False)
            if ((named_file.st_dev, named_file.st_ino)
                    != (opened.st_dev, opened.st_ino)):
                reason = "source_changed"
                return
            for parent_fd, name, device, inode in parent_links:
                current_dir = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
                if (current_dir.st_dev, current_dir.st_ino) != (device, inode):
                    reason = "source_changed"
                    return
            root_after_fd = _open_directory_chain(self.root)
            try:
                root_after = os.fstat(root_after_fd)
            finally:
                os.close(root_after_fd)
            if (root_after.st_dev, root_after.st_ino) != root_identity:
                reason = "source_changed"
                return
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
            for descriptor in reversed(directory_fds):
                os.close(descriptor)
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


def _windows_relative_parts(value):
    if not isinstance(value, str) or not value or "/" in value or value.startswith("\\"):
        raise Unavailable("source_read_unavailable")
    raw_parts = value.split("\\")
    if any(not part for part in raw_parts):
        raise Unavailable("source_read_unavailable")
    return [_windows_component(part) for part in raw_parts]


def _windows_stable_info(info):
    return {key: value for key, value in info.items() if key != "accessed"}


def _windows_open_root(api, root, user_sid):
    drive, parts = _windows_absolute_parts(root)
    if not parts:
        raise Unavailable("source_read_unavailable")
    targets = api.C.create_unicode_buffer(32768)
    if not api.kernel.QueryDosDeviceW(drive, targets, len(targets)):
        raise Unavailable("source_read_unavailable")
    device = targets.value
    if not re.fullmatch(r"\\Device\\HarddiskVolume[0-9]+", device):
        raise Unavailable("source_read_unavailable")
    handles, links = [], []
    try:
        current = api.open(device + "\\", directory=True)
        handles.append(current)
        root_info = api.info(current)
        if not root_info["directory"]:
            raise Unavailable("source_read_unavailable")
        fs_name = api.C.create_unicode_buffer(64)
        serial, maximum, flags = api.W.DWORD(), api.W.DWORD(), api.W.DWORD()
        if (not api.kernel.GetVolumeInformationByHandleW(
                current, None, 0, api.C.byref(serial), api.C.byref(maximum),
                api.C.byref(flags), fs_name, len(fs_name)) or fs_name.value != "NTFS"):
            raise Unavailable("source_read_unavailable")
        api.check_acl(current, user_sid, "ancestor")
        for part in parts:
            child = api.open(part, current, directory=True)
            handles.append(child)
            info = api.info(child)
            if not info["directory"] or info["identity"][0] != root_info["identity"][0]:
                raise Unavailable("source_changed")
            api.check_acl(child, user_sid, "ancestor")
            links.append((current, part, child, info))
            current = child
        return handles, links, root_info
    except BaseException:
        for handle in reversed(handles):
            api.close(handle)
        raise


class _WindowsApprovedLineStream(_ApprovedLineStream):
    """Native bounded stream over a configured root and relative JSONL path."""

    def __init__(self, root, relative, budget, api, user_sid):
        super().__init__(root, relative, budget)
        self.api, self.user_sid = api, user_sid

    def _open_root(self):
        handles, links, root_info = _windows_open_root(
            self.api, self.root, self.user_sid)
        return handles, links, root_info["identity"][0], root_info

    def __iter__(self):
        if self._started:
            self.terminal_reason = "source_read_unavailable"
            return
        self._started = True
        api, handles = self.api, []
        file_handle = -1
        reason = "source_read_unavailable"
        try:
            if (type(self.budget) is not int or not 0 <= self.budget <= MAX_BATCH_BYTES):
                reason = "source_budget_exceeded"
                return
            root_handles, root_links, volume, volume_info = self._open_root()
            handles.extend(root_handles)
            relative = _windows_relative_parts(self.relative)
            current = handles[-1]
            directory_links = []
            for part in relative[:-1]:
                child = api.open(part, current, directory=True)
                handles.append(child)
                info = api.info(child)
                if not info["directory"] or info["identity"][0] != volume:
                    reason = "source_changed"
                    return
                api.check_acl(child, self.user_sid, "ancestor")
                directory_links.append((current, part, child, info))
                current = child
            leaf = relative[-1]
            file_handle = api.open(leaf, current, read_data=True)
            before = api.info(file_handle)
            if (before["directory"] or before["links"] != 1
                    or before["identity"][0] != volume
                    or before["size"] > self.budget):
                reason = "source_budget_exceeded" if before["size"] > self.budget else "source_read_unavailable"
                return
            api.check_acl(file_handle, self.user_sid, "ancestor")
            self.open_identity = {
                "dev": before["identity"][0], "ino": before["identity"][1],
                "size": before["size"], "mtime_ns": before["mtime_ns"],
                "ctime_ns": before["ctime_ns"],
            }
            total = line_count = 0
            pending = b""
            while True:
                allowance = self.budget - total + 1
                block_size = min(64 * 1024, allowance)
                buffer = api.C.create_string_buffer(block_size)
                received = api.W.DWORD()
                if not api.kernel.ReadFile(file_handle, buffer, block_size,
                                           api.C.byref(received), None):
                    reason = "source_read_unavailable"
                    return
                count = int(received.value)
                if count > block_size:
                    reason = "source_read_unavailable"
                    return
                if count == 0:
                    break
                total += count
                self.bytes_read = total
                if total > self.budget:
                    reason = "source_budget_exceeded"
                    return
                pending += buffer.raw[:count]
                while True:
                    boundary = pending.find(b"\n")
                    if boundary < 0:
                        if len(pending) > MAX_LINE:
                            reason = "source_budget_exceeded"
                            return
                        break
                    line, pending = pending[:boundary + 1], pending[boundary + 1:]
                    if len(line) > MAX_LINE:
                        reason = "source_budget_exceeded"
                        return
                    line_count += 1
                    self.complete_lines = line_count
                    if line_count > MAX_BATCH_LINES:
                        reason = "source_budget_exceeded"
                        return
                    yield line
            after = api.info(file_handle)
            api.check_acl(file_handle, self.user_sid, "ancestor")
            self.final_identity = {
                "dev": after["identity"][0], "ino": after["identity"][1],
                "size": after["size"], "mtime_ns": after["mtime_ns"],
                "ctime_ns": after["ctime_ns"],
            }
            stable = _windows_stable_info(before) == _windows_stable_info(after)
            if (not stable or total != before["size"] or pending):
                reason = "partial_tail" if pending and stable and total == before["size"] else "source_changed"
                return
            current_volume = api.info(root_handles[0])
            api.check_acl(root_handles[0], self.user_sid, "ancestor")
            if _windows_stable_info(current_volume) != _windows_stable_info(volume_info):
                reason = "source_changed"
                return
            for parent, name, original, identity in root_links + directory_links:
                check = api.open(name, parent, directory=True)
                try:
                    reopened = api.info(check)
                    api.check_acl(check, self.user_sid, "ancestor")
                    if _windows_stable_info(reopened) != _windows_stable_info(identity):
                        reason = "source_changed"
                        return
                finally:
                    api.close(check)
                current_info = api.info(original)
                api.check_acl(original, self.user_sid, "ancestor")
                if _windows_stable_info(current_info) != _windows_stable_info(identity):
                    reason = "source_changed"
                    return
            named = api.open(leaf, current, read_data=True)
            try:
                named_info = api.info(named)
                api.check_acl(named, self.user_sid, "ancestor")
                if _windows_stable_info(named_info) != _windows_stable_info(before):
                    reason = "source_changed"
                    return
            finally:
                api.close(named)
            reason = None
        except Unavailable as exc:
            reason = exc.reason
        except (OSError, ValueError, TypeError, AttributeError, OverflowError):
            reason = "source_read_unavailable"
        finally:
            if file_handle >= 0:
                api.close(file_handle)
            for handle in reversed(handles):
                api.close(handle)
            self.terminal_reason = reason


def _iter_approved_lines(root, relative, budget=MAX_BATCH_BYTES, *,
                         windows_api=None, windows_user_sid=None):
    """Stream complete lines from one explicitly approved synthetic/source path."""
    if os.name == "nt" or windows_api is not None:
        api = _WindowsConsentAPI() if windows_api is None else windows_api
        if windows_user_sid is None:
            _profile, windows_user_sid = api.current_user_profile()
        return _WindowsApprovedLineStream(root, relative, budget, api, windows_user_sid)
    return _ApprovedLineStream(root, relative, budget)


def _valid_relative(value):
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    parts = PurePosixPath(value).parts
    if (not parts or value.startswith("/")
            or any(part in {"", ".", ".."} for part in parts)
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        return None
    return parts


def _enumerate_jsonl(root):
    """Enumerate only regular JSONL files below one configured root."""
    if not _PRIVATE_FS_SUPPORTED:
        raise Unavailable
    root_fd = _open_directory_chain(root)
    root_info = os.fstat(root_fd)
    root_identity = {"dev": root_info.st_dev, "ino": root_info.st_ino}
    open_dirs = [root_fd]
    stack = [(root_fd, "", 0)]
    entries = 0
    files = []
    try:
        while stack:
            directory_fd, prefix, depth = stack.pop()
            names = os.listdir(directory_fd)
            entries += len(names)
            if entries > MAX_REFRESH_ENTRIES:
                raise Unavailable("source_budget_exceeded")
            for name in names:
                if (not isinstance(name, str) or not name or name in {".", ".."}
                        or "/" in name or "\\" in name):
                    raise Unavailable
                info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                relative = f"{prefix}/{name}" if prefix else name
                if stat.S_ISDIR(info.st_mode):
                    if depth >= MAX_SOURCE_ROOT_DEPTH:
                        raise Unavailable("source_budget_exceeded")
                    child_fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                       dir_fd=directory_fd)
                    child_info = os.fstat(child_fd)
                    if ((child_info.st_dev, child_info.st_ino)
                            != (info.st_dev, info.st_ino)):
                        os.close(child_fd)
                        raise Unavailable
                    open_dirs.append(child_fd)
                    stack.append((child_fd, relative, depth + 1))
                elif stat.S_ISREG(info.st_mode):
                    if name.endswith(".jsonl"):
                        files.append((relative, {
                            "dev": info.st_dev, "ino": info.st_ino,
                            "size": info.st_size, "mtime_ns": info.st_mtime_ns,
                            "ctime_ns": info.st_ctime_ns,
                        }))
                        if len(files) > MAX_SOURCE_FILES:
                            raise Unavailable("source_budget_exceeded")
                else:
                    raise Unavailable
        files.sort(key=lambda item: item[0])
        return files, entries, root_identity
    except Unavailable:
        raise
    except (OSError, ValueError, TypeError):
        raise Unavailable from None
    finally:
        for descriptor in reversed(open_dirs):
            try:
                os.close(descriptor)
            except OSError:
                pass


class _WindowsDirectorySnapshot:
    """Held native directory tree whose metadata can gate later source acceptance."""

    def __init__(self, api, user_sid, handles, links, snapshots):
        self.api, self.user_sid = api, user_sid
        self.handles, self.links, self.snapshots = handles, links, snapshots

    def verify(self):
        for handle in self.handles:
            before = self.snapshots[handle]
            after = self.api.info(handle)
            self.api.check_acl(handle, self.user_sid, "ancestor")
            if _windows_stable_info(after) != _windows_stable_info(before):
                raise Unavailable("source_changed")
        for parent, name, handle, before in self.links:
            reopened = self.api.open(name, parent, directory=True)
            try:
                after = self.api.info(reopened)
                self.api.check_acl(reopened, self.user_sid, "ancestor")
            finally:
                self.api.close(reopened)
            if _windows_stable_info(after) != _windows_stable_info(before):
                raise Unavailable("source_changed")

    def close(self):
        handles, self.handles = self.handles, []
        for handle in reversed(handles):
            self.api.close(handle)


def _enumerate_windows_jsonl(root, api, user_sid, *, retain_snapshot=False):
    """Enumerate one explicit approved NTFS root through held handles."""
    handles, root_links, volume_info = _windows_open_root(api, root, user_sid)
    all_handles = list(handles)
    links = list(root_links)
    files, entries = [], 0
    root_handle = handles[-1]
    root_identity = api.info(root_handle)
    snapshots = {handle: api.info(handle) for handle in all_handles}
    retained = False
    stack = [(root_handle, "", 0)]
    try:
        while stack:
            parent, prefix, depth = stack.pop()
            remaining = MAX_REFRESH_ENTRIES - entries
            if remaining < 0:
                raise Unavailable("source_budget_exceeded")
            rows = api.enumerate(parent, remaining)
            entries += len(rows)
            if entries > MAX_REFRESH_ENTRIES:
                raise Unavailable("source_budget_exceeded")
            for row in rows:
                name = _windows_component(row["name"])
                relative = f"{prefix}\\{name}" if prefix else name
                directory = row["directory"]
                if directory and depth >= MAX_SOURCE_ROOT_DEPTH:
                    raise Unavailable("source_budget_exceeded")
                child = api.open(name, parent, directory=directory)
                try:
                    info = api.info(child)
                    if (info["identity"] != (volume_info["identity"][0], row["file_id"])
                            or info["directory"] != directory
                            or info["size"] != row["size"]):
                        raise Unavailable("source_changed")
                    api.check_acl(child, user_sid, "ancestor")
                    if directory:
                        all_handles.append(child)
                        links.append((parent, name, child, info))
                        stack.append((child, relative, depth + 1))
                        child = -1
                    else:
                        if info["links"] != 1:
                            raise Unavailable("source_read_unavailable")
                        if name.lower().endswith(".jsonl"):
                            files.append((relative, {
                                "dev": info["identity"][0], "ino": info["identity"][1],
                                "size": info["size"], "mtime_ns": info["mtime_ns"],
                                "ctime_ns": info["ctime_ns"],
                            }))
                            if len(files) > MAX_SOURCE_FILES:
                                raise Unavailable("source_budget_exceeded")
                finally:
                    if child >= 0:
                        api.close(child)
        snapshot = _WindowsDirectorySnapshot(api, user_sid, all_handles, links, snapshots)
        snapshot.verify()
        identity = {"dev": root_identity["identity"][0],
                    "ino": root_identity["identity"][1]}
        result = (sorted(files, key=lambda item: item[0]), entries, identity)
        if retain_snapshot:
            retained = True
            return (*result, snapshot)
        return result
    except Unavailable:
        raise
    except (OSError, ValueError, TypeError, AttributeError, OverflowError):
        raise Unavailable("source_read_unavailable") from None
    finally:
        if not retained:
            for handle in reversed(all_handles):
                api.close(handle)


def _read_relative_bytes(root_fd, relative, *, limit, line_limit=None, missing_ok=False):
    """Read one relative regular file with no-follow descriptor revalidation."""
    parts = _valid_relative(relative)
    if parts is None or type(limit) is not int or limit < 0:
        raise Unavailable
    directory_fd = os.dup(root_fd)
    file_fd = -1
    try:
        for part in parts[:-1]:
            before = os.stat(part, dir_fd=directory_fd, follow_symlinks=False)
            if not stat.S_ISDIR(before.st_mode):
                raise Unavailable
            next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                              dir_fd=directory_fd)
            opened = os.fstat(next_fd)
            if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                os.close(next_fd)
                raise Unavailable
            os.close(directory_fd)
            directory_fd = next_fd
        leaf = parts[-1]
        before = os.stat(leaf, dir_fd=directory_fd, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):
            raise Unavailable
        file_fd = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd)
        opened = os.fstat(file_fd)
        if (not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)
                or opened.st_size > limit):
            raise Unavailable
        chunks, total, pending = [], 0, b""
        while True:
            block = os.read(file_fd, min(64 * 1024, limit - total + 1))
            if not block:
                break
            total += len(block)
            if total > limit:
                raise Unavailable
            chunks.append(block)
            if line_limit is not None:
                pending += block
                while True:
                    index = pending.find(b"\n")
                    if index < 0:
                        if len(pending) > line_limit:
                            raise Unavailable
                        break
                    line, pending = pending[:index + 1], pending[index + 1:]
                    if len(line) > line_limit:
                        raise Unavailable
        if line_limit is not None and pending:
            raise Unavailable
        after = os.fstat(file_fd)
        named = os.stat(leaf, dir_fd=directory_fd, follow_symlinks=False)
        identity = (opened.st_dev, opened.st_ino, opened.st_size,
                    opened.st_mtime_ns, opened.st_ctime_ns)
        if ((after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
             after.st_ctime_ns) != identity
                or (named.st_dev, named.st_ino) != (opened.st_dev, opened.st_ino)
                or total != opened.st_size):
            raise Unavailable
        return b"".join(chunks), {
            "dev": opened.st_dev, "ino": opened.st_ino,
            "size": opened.st_size, "mtime_ns": opened.st_mtime_ns,
            "ctime_ns": opened.st_ctime_ns,
        }
    except FileNotFoundError:
        if missing_ok:
            return None
        raise Unavailable from None
    except Unavailable:
        raise
    except (OSError, ValueError, TypeError):
        raise Unavailable from None
    finally:
        if file_fd >= 0:
            os.close(file_fd)
        os.close(directory_fd)


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
                if match is None or not isinstance(record["files"], list):
                    raise ValueError
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


def _capture_project_claims(project):
    """Capture only the approved project's bounded existing intent JSONL."""
    try:
        root_fd = _open_directory_chain(project["path"])
        try:
            root_identity = os.fstat(root_fd)
            raw, _identity = _read_relative_bytes(
                root_fd, "dev/intents.jsonl", limit=MAX_CLAIM_BYTES,
                line_limit=MAX_CLAIM_LINE, missing_ok=True)
            if raw is None:
                return [], "attribution_unavailable"
            current_fd = _open_directory_chain(project["path"])
            try:
                current = os.fstat(current_fd)
            finally:
                os.close(current_fd)
            if (current.st_dev, current.st_ino) != (
                    root_identity.st_dev, root_identity.st_ino):
                raise Unavailable("source_changed")
        finally:
            os.close(root_fd)
        lines = raw.splitlines(keepends=True)
        claims = _claim_snapshot(project["alias"], lines)
        return claims, "capture_gap" if not claims else "captured"
    except Unavailable:
        raise
    except (OSError, KeyError, TypeError, ValueError):
        raise Unavailable from None


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
    "size", "mtime_ns", "ctime_ns",
}
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
}
_LEGACY_LEDGER_FIELDS = _LEDGER_FIELDS - {"waits"}


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


def _load_ledger(raw):
    if raw is None:
        return {
            "schema": LEDGER_SCHEMA, "reader_version": READER_VERSION,
            "ratio_version": RATIO_VERSION, "ratio_index": _ratio_index_copy(),
            "events": [], "claims": [], "cursors": [],
            "mappings": [], "project_remotes": [], "aggregates": [], "lineages": [],
            "waits": [],
            "coverage": {"global": "unknown", "reasons": []},
        }
    try:
        if not isinstance(raw, bytes) or len(raw) > MAX_LEDGER_BYTES:
            raise ValueError
        ledger = json.loads(raw.decode("utf-8"), object_pairs_hook=_object,
                            parse_constant=_constant)
        if (isinstance(ledger, dict)
                and set(ledger) == _LEGACY_LEDGER_FIELDS
                and ledger.get("schema") == _LEGACY_LEDGER_SCHEMA):
            if (ledger.get("reader_version") != _LEGACY_READER_VERSION
                    or ledger.get("ratio_version") != RATIO_VERSION
                    or ledger.get("ratio_index") != _RATIO_INDEX
                    or not isinstance(ledger.get("coverage"), dict)
                    or set(ledger["coverage"]) != {"global", "reasons"}
                    or ledger["coverage"].get("global") != "unknown"
                    or not isinstance(ledger["coverage"].get("reasons"), list)
                    or ledger["coverage"]["reasons"] != sorted(set(
                        ledger["coverage"]["reasons"]))
                    or any(not isinstance(reason, str) or not re.fullmatch(
                        r"[a-z][a-z0-9_]*", reason)
                           for reason in ledger["coverage"]["reasons"])):
                raise ValueError
            ledger["schema"] = LEDGER_SCHEMA
            ledger["reader_version"] = READER_VERSION
            ledger["waits"] = []
            ledger["coverage"]["reasons"] = sorted(set(
                ledger["coverage"]["reasons"] + ["pre_v4_timing_history"]))
        if not isinstance(ledger, dict) or set(ledger) != _LEDGER_FIELDS:
            raise ValueError
        if (ledger["schema"] != LEDGER_SCHEMA
                or ledger["reader_version"] != READER_VERSION
                or ledger["ratio_version"] != RATIO_VERSION
                or ledger["ratio_index"] != _RATIO_INDEX):
            raise ValueError
        if any(not isinstance(ledger[key], list) for key in (
                "events", "claims", "cursors", "mappings", "project_remotes",
                "aggregates", "lineages", "waits")):
            raise ValueError
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
                    event = events_by_key.get(event_key)
                    if event is None or event["lineage_key"] != lineage["lineage_key"]:
                        raise ValueError
        for wait in ledger["waits"]:
            if wait["lineage_key"] is not None:
                lineage = lineage_by_key.get(wait["lineage_key"])
                if lineage is None or (lineage["state"] != "verified"
                                       and wait["ownership"] == "proven"):
                    raise ValueError
        for aggregate in ledger["aggregates"]:
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
            if (aggregate["reference_index"] != RATIO_VERSION
                    or not isinstance(aggregate["reference_tokens"], dict)
                    or set(aggregate["reference_tokens"])
                    != {*_EVENT_KIND_NAMES, "total"}):
                raise ValueError
            for value in aggregate["reference_tokens"].values():
                if value is not None and (not isinstance(value, str)
                        or not re.fullmatch(r"(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", value)):
                    raise ValueError
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
    if ("conflicting_usage" in reasons or prior["kinds"] != incoming["kinds"]
            or prior["cache_write_ttl"] != incoming["cache_write_ttl"]
            or any(value is None for value in prior["kinds"].values())
            or any(value is None for value in incoming["kinds"].values())):
        prior["kinds"] = _unknown_kinds()
        prior["cache_write_ttl"] = {"five_minute": None, "one_hour": None}
        if prior["kinds"] != incoming["kinds"]:
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
    if len(by_key) > MAX_RETAINED_EVENTS:
        raise Unavailable
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
        for index, left in enumerate(closed):
            left_start = datetime.fromisoformat(left["claimed_at"].replace("Z", "+00:00"))
            left_end = datetime.fromisoformat(left["released_at"].replace("Z", "+00:00"))
            for right in closed[index + 1:]:
                comparisons += 1
                if comparisons > MAX_WAIT_EXPORT_WORK:
                    raise Unavailable("source_budget_exceeded")
                right_start = datetime.fromisoformat(right["claimed_at"].replace("Z", "+00:00"))
                right_end = datetime.fromisoformat(right["released_at"].replace("Z", "+00:00"))
                if max(left_start, right_start) < min(left_end, right_end):
                    overlaps.update((left["claim_key"], right["claim_key"]))
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


def _scan_approved_sources(config, prior_cursors):
    previous = {cursor["file_key"]: cursor for cursor in prior_cursors}
    batches, cursors, reasons = [], {}, set()
    total_entries = total_files = total_bytes = 0
    aliases_seen = set()
    excluded = [source["root"] for source in config["sources"]]
    excluded.extend(project["path"] for project in config["projects"])
    for source in sorted(config["sources"], key=lambda item: item["alias"]):
        if source["alias"] in aliases_seen:
            raise Unavailable
        aliases_seen.add(source["alias"])
        files, entries, root_identity = _enumerate_jsonl(source["root"])
        total_entries += entries
        total_files += len(files)
        if total_entries > MAX_REFRESH_ENTRIES or total_files > MAX_SOURCE_FILES:
            raise Unavailable("source_budget_exceeded")
        root_fd = _open_directory_chain(source["root"])
        root_opened = os.fstat(root_fd)
        if (root_opened.st_dev, root_opened.st_ino) != (
                root_identity["dev"], root_identity["ino"]):
            os.close(root_fd)
            raise Unavailable
        try:
            for relative, enumerated in files:
                if enumerated["size"] < 0:
                    raise Unavailable
                total_bytes += enumerated["size"]
                if total_bytes > MAX_TOTAL_SOURCE_BYTES:
                    raise Unavailable("source_budget_exceeded")
                file_key = _digest("cursor", source["alias"], relative)
                stream = _iter_approved_lines(source["root"], relative)
                batch = read_records(source["tool"], stream, config=config,
                                     source_aliases=[source["alias"]],
                                     source_root=source["root"])
                if stream.terminal_reason == "partial_tail":
                    reasons.add("partial_tail")
                    old = previous.get(file_key)
                    if old is not None:
                        cursors[file_key] = dict(old)
                    continue
                if stream.terminal_reason is not None:
                    raise Unavailable(stream.terminal_reason)
                if stream.open_identity is None or stream.final_identity is None:
                    raise Unavailable
                if any(stream.open_identity[name] != enumerated[name]
                       for name in ("dev", "ino")):
                    raise Unavailable
                if ((stream.final_identity["dev"], stream.final_identity["ino"])
                        != (stream.open_identity["dev"], stream.open_identity["ino"])):
                    raise Unavailable
                total_bytes += max(0, stream.bytes_read - enumerated["size"])
                if total_bytes > MAX_TOTAL_SOURCE_BYTES:
                    raise Unavailable("source_budget_exceeded")
                old = previous.get(file_key)
                changed = bool(old is not None and (
                    old["dev"] != stream.final_identity["dev"]
                    or old["ino"] != stream.final_identity["ino"]
                    or stream.final_identity["size"] < old["offset"]
                    or old["size"] != stream.final_identity["size"]
                    or old["mtime_ns"] != stream.final_identity["mtime_ns"]
                    or old["ctime_ns"] != stream.final_identity["ctime_ns"]))
                generation = (1 if old is None else
                              old["generation"] + (1 if changed else 0))
                cursors[file_key] = {
                    "source_alias": source["alias"], "file_key": file_key,
                    "dev": stream.final_identity["dev"],
                    "ino": stream.final_identity["ino"],
                    "generation": generation, "offset": stream.bytes_read,
                    "line": stream.complete_lines,
                    "size": stream.final_identity["size"],
                    "mtime_ns": stream.final_identity["mtime_ns"],
                    "ctime_ns": stream.final_identity["ctime_ns"],
                }
                batch["source_alias"] = source["alias"]
                batch["file_key"] = file_key
                batch["cursor"] = dict(cursors[file_key])
                batches.append(batch)
                reasons.update(batch["issues"])
        finally:
            os.close(root_fd)
        root_after = _open_directory_chain(source["root"])
        try:
            after = os.fstat(root_after)
            if (after.st_dev, after.st_ino) != (
                    root_identity["dev"], root_identity["ino"]):
                raise Unavailable
        finally:
            os.close(root_after)
    verified_forks, fork_conflicts = _verify_copied_forks(batches)
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
    wait_rows = []
    independently_owned_waits = {
        candidate["wait_key"]
        for batch in batches for candidate in batch.get("wait_candidates", ())
        if not candidate.get("_fork_parent_copy") and candidate["ownership"] == "proven"
    }
    for batch in batches:
        cursor = batch["cursor"]
        for candidate in batch.get("wait_candidates", ()):
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
                if lineage_key in verified_lineages:
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
    if len(incoming) > MAX_RETAINED_EVENTS:
        raise Unavailable
    return (incoming, sorted(cursors.values(), key=lambda item: item["file_key"]),
            reasons, verified_forks, fork_conflicts, wait_rows)


def _capture_all_claims(config):
    claims, status, remotes = [], set(), []
    excluded = [source["root"] for source in config["sources"]]
    excluded.extend(project["path"] for project in config["projects"])
    for project in sorted(config["projects"], key=lambda item: item["alias"]):
        remote, reason = _verified_project_remote(project, excluded)
        if reason is not None or remote != project["remote"]:
            status.add("attribution_unavailable")
            continue
        remotes.append({"alias": project["alias"], "remote": remote})
        project_claims, claim_status = _capture_project_claims(project)
        after_remote, after_reason = _verified_project_remote(project, excluded)
        if after_reason is not None or after_remote != remote:
            raise Unavailable("source_changed")
        claims.extend(project_claims)
        status.add(claim_status)
    if not status:
        status.add("attribution_unavailable")
    return claims, remotes, status


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
                fork_conflicts):
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
    mappings = _build_mappings(events, claims, config)
    reasons = set(scan_reasons)
    if "pre_v4_timing_history" in prior["coverage"]["reasons"]:
        reasons.add("pre_v4_timing_history")
    reasons.update(status for status in capture_status if status != "captured")
    if fork_conflicts or any(item["state"] == "conflicting" for item in lineages):
        reasons.add("conflicting_binding")
    return {
        "schema": LEDGER_SCHEMA, "reader_version": READER_VERSION,
        "ratio_version": RATIO_VERSION, "ratio_index": _ratio_index_copy(),
        "events": events, "waits": waits, "claims": claims,
        "cursors": cursors, "mappings": mappings,
        "project_remotes": sorted(project_remotes, key=lambda item: item["alias"]),
        "aggregates": _recompute_aggregates(events, config),
        "lineages": lineages,
        "coverage": {"global": "unknown", "reasons": sorted(reasons)},
    }


def _require_private_fd(fd, *, directory, mode=None, private_only=False):
    info = os.fstat(fd)
    expected = stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)
    mode_ok = (stat.S_IMODE(info.st_mode) == mode if mode is not None
               else not (stat.S_IMODE(info.st_mode) & 0o077))
    if (not expected or info.st_uid != os.getuid() or not mode_ok
            or (not directory and info.st_nlink != 1)):
        raise Unavailable("ledger_unavailable")
    return info


def _open_consent_area(home):
    if not _PRIVATE_FS_SUPPORTED or fcntl is None:
        raise Unavailable("config_home_unavailable")
    _verify_private_home(Path(home))
    home_fd = _open_directory_chain(home)
    cairn_fd = config_fd = -1
    try:
        try:
            before_cairn = os.stat(".cairn", dir_fd=home_fd, follow_symlinks=False)
            if not stat.S_ISDIR(before_cairn.st_mode):
                raise Unavailable("config_home_unavailable")
            cairn_fd = os.open(".cairn", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                               dir_fd=home_fd)
        except FileNotFoundError:
            return home_fd, None, None, None, None
        cairn_info = _require_private_fd(cairn_fd, directory=True, mode=0o700)
        if (cairn_info.st_dev, cairn_info.st_ino) != (before_cairn.st_dev, before_cairn.st_ino):
            raise Unavailable("source_changed")
        config_fd, config_raw, config_identity = _open_private_leaf(
            cairn_fd, "meter.json", limit=MAX_CONFIG_BYTES, allow_missing=True,
            mode=None, private_only=True)
        if config_fd is None:
            return home_fd, cairn_fd, None, None, None
        config = validate_config_bytes(config_raw)
        return home_fd, cairn_fd, config_fd, config_identity, (config, config_raw)
    except Exception:
        for descriptor in (config_fd, cairn_fd, home_fd):
            if descriptor >= 0:
                os.close(descriptor)
        raise


def _open_meter_area(cairn_fd):
    if cairn_fd < 0:
        raise Unavailable("ledger_unavailable")
    meter_fd = -1
    try:
        try:
            before_meter = os.stat("meter", dir_fd=cairn_fd, follow_symlinks=False)
        except FileNotFoundError:
            os.mkdir("meter", mode=0o700, dir_fd=cairn_fd)
            os.fsync(cairn_fd)
            before_meter = os.stat("meter", dir_fd=cairn_fd, follow_symlinks=False)
        if not stat.S_ISDIR(before_meter.st_mode):
            raise Unavailable("ledger_unavailable")
        meter_fd = os.open("meter", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                           dir_fd=cairn_fd)
        meter_info = _require_private_fd(meter_fd, directory=True, mode=0o700)
        if (meter_info.st_dev, meter_info.st_ino) != (before_meter.st_dev, before_meter.st_ino):
            raise Unavailable("source_changed")
        return meter_fd
    except Exception:
        if meter_fd >= 0:
            os.close(meter_fd)
        raise


def _open_private_leaf(directory_fd, name, *, limit, allow_missing=False,
                       mode=0o600, private_only=False):
    try:
        before = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        if allow_missing:
            return None, None, None
        raise Unavailable("ledger_unavailable") from None
    if not stat.S_ISREG(before.st_mode):
        raise Unavailable("ledger_unavailable")
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd)
    try:
        opened = _require_private_fd(fd, directory=False, mode=mode,
                                     private_only=private_only)
        if ((opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)
                or opened.st_size > limit):
            raise Unavailable("ledger_invalid")
        pieces, total = [], 0
        while True:
            block = os.read(fd, min(64 * 1024, limit - total + 1))
            if not block:
                break
            total += len(block)
            if total > limit:
                raise Unavailable("ledger_invalid")
            pieces.append(block)
        after = os.fstat(fd)
        named = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        identity = (opened.st_dev, opened.st_ino, opened.st_size,
                    opened.st_mtime_ns, opened.st_ctime_ns)
        if ((after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
             after.st_ctime_ns) != identity
                or (named.st_dev, named.st_ino) != (opened.st_dev, opened.st_ino)
                or total != opened.st_size):
            raise Unavailable("source_changed")
        return fd, b"".join(pieces), identity
    except Exception:
        os.close(fd)
        raise


def _open_lock(meter_fd):
    try:
        try:
            fd = os.open(LEDGER_LOCK_NAME,
                         os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                         0o600, dir_fd=meter_fd)
        except FileExistsError:
            fd = os.open(LEDGER_LOCK_NAME, os.O_RDWR | os.O_NOFOLLOW, dir_fd=meter_fd)
        _require_private_fd(fd, directory=False, mode=0o600)
        info = os.fstat(fd)
        if info.st_size != 0:
            raise Unavailable("ledger_unavailable")
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (BlockingIOError, OSError):
            raise Unavailable("ledger_busy") from None
        current = os.stat(LEDGER_LOCK_NAME, dir_fd=meter_fd, follow_symlinks=False)
        locked = os.fstat(fd)
        if ((current.st_dev, current.st_ino) != (locked.st_dev, locked.st_ino)
                or locked.st_size != 0):
            raise Unavailable("source_changed")
        return fd, (locked.st_dev, locked.st_ino, locked.st_mode, locked.st_nlink)
    except Exception:
        if "fd" in locals():
            os.close(fd)
        raise


def _read_optional_ledger(meter_fd):
    fd, raw, identity = _open_private_leaf(
        meter_fd, LEDGER_NAME, limit=MAX_LEDGER_BYTES, allow_missing=True)
    return fd, raw, identity


def _read_ledger_fd_again(fd, limit):
    os.lseek(fd, 0, os.SEEK_SET)
    chunks, total = [], 0
    while True:
        block = os.read(fd, min(64 * 1024, limit - total + 1))
        if not block:
            break
        total += len(block)
        if total > limit:
            raise Unavailable("ledger_invalid")
        chunks.append(block)
    return b"".join(chunks)


def _revalidate_transaction(home_path, home_fd, cairn_fd, meter_fd, lock_fd, lock_identity,
                            old_fd, old_raw, old_identity, config_fd,
                            config_raw, config_identity):
    held_home = os.fstat(home_fd)
    _verify_private_home(Path(home_path))
    current_home_fd = _open_directory_chain(home_path)
    try:
        current_home = os.fstat(current_home_fd)
    finally:
        os.close(current_home_fd)
    if (current_home.st_dev, current_home.st_ino) != (held_home.st_dev, held_home.st_ino):
        raise Unavailable("source_changed")
    if held_home.st_uid != os.getuid() or not stat.S_ISDIR(held_home.st_mode):
        raise Unavailable("ledger_unavailable")
    cairn = os.stat(".cairn", dir_fd=home_fd, follow_symlinks=False)
    opened_cairn = os.fstat(cairn_fd)
    meter = os.stat("meter", dir_fd=cairn_fd, follow_symlinks=False)
    opened_meter = os.fstat(meter_fd)
    if ((cairn.st_dev, cairn.st_ino) != (opened_cairn.st_dev, opened_cairn.st_ino)
            or (meter.st_dev, meter.st_ino) != (opened_meter.st_dev, opened_meter.st_ino)):
        raise Unavailable("source_changed")
    _require_private_fd(cairn_fd, directory=True, mode=0o700)
    _require_private_fd(meter_fd, directory=True, mode=0o700)
    _require_private_fd(lock_fd, directory=False, mode=0o600)
    lock = os.stat(LEDGER_LOCK_NAME, dir_fd=meter_fd, follow_symlinks=False)
    locked = os.fstat(lock_fd)
    if ((lock.st_dev, lock.st_ino, locked.st_mode, locked.st_nlink) != lock_identity
            or locked.st_size != 0):
        raise Unavailable("source_changed")
    if old_fd is None:
        try:
            os.stat(LEDGER_NAME, dir_fd=meter_fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Unavailable("source_changed")
    else:
        _require_private_fd(old_fd, directory=False, mode=0o600)
        old = os.fstat(old_fd)
        named = os.stat(LEDGER_NAME, dir_fd=meter_fd, follow_symlinks=False)
        if ((named.st_dev, named.st_ino) != (old.st_dev, old.st_ino)
                or (old.st_dev, old.st_ino, old.st_size, old.st_mtime_ns,
                    old.st_ctime_ns) != old_identity
                or _read_ledger_fd_again(old_fd, MAX_LEDGER_BYTES) != old_raw):
            raise Unavailable("source_changed")
    _require_private_fd(config_fd, directory=False, mode=None, private_only=True)
    config = os.fstat(config_fd)
    named_config = os.stat("meter.json", dir_fd=cairn_fd, follow_symlinks=False)
    if ((config.st_dev, config.st_ino, config.st_size, config.st_mtime_ns,
         config.st_ctime_ns) != config_identity
            or (named_config.st_dev, named_config.st_ino) != (config.st_dev, config.st_ino)
            or _read_ledger_fd_again(config_fd, MAX_CONFIG_BYTES) != config_raw):
        raise Unavailable("source_changed")


def _atomic_replace_ledger(home_path, home_fd, cairn_fd, meter_fd, lock_fd, lock_identity,
                           old_fd, old_raw, old_identity, config_fd,
                           config_raw, config_identity, candidate):
    data = (json.dumps(candidate, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")
    if len(data) > MAX_LEDGER_BYTES:
        raise Unavailable("source_budget_exceeded")
    temporary = ".ledger-" + secrets.token_hex(16) + ".tmp"
    temp_fd = -1
    temp_identity = None
    committed = False
    try:
        temp_fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                          0o600, dir_fd=meter_fd)
        temp_info = _require_private_fd(temp_fd, directory=False, mode=0o600)
        temp_identity = (temp_info.st_dev, temp_info.st_ino)
        offset = 0
        while offset < len(data):
            written = os.write(temp_fd, data[offset:offset + 64 * 1024])
            if written <= 0:
                raise Unavailable("ledger_write_failed")
            offset += written
        os.fsync(temp_fd)
        final_info = os.fstat(temp_fd)
        if (final_info.st_size != len(data)
                or (final_info.st_dev, final_info.st_ino) != temp_identity):
            raise Unavailable("ledger_write_failed")
        _revalidate_transaction(home_path, home_fd, cairn_fd, meter_fd, lock_fd, lock_identity,
                                old_fd, old_raw, old_identity, config_fd,
                                config_raw, config_identity)
        named_temp = os.stat(temporary, dir_fd=meter_fd, follow_symlinks=False)
        if ((named_temp.st_dev, named_temp.st_ino) != temp_identity
                or not stat.S_ISREG(named_temp.st_mode)
                or named_temp.st_nlink != 1
                or stat.S_IMODE(named_temp.st_mode) != 0o600):
            raise Unavailable("source_changed")
        os.replace(temporary, LEDGER_NAME,
                   src_dir_fd=meter_fd, dst_dir_fd=meter_fd)
        committed = True
        try:
            os.fsync(meter_fd)
        except OSError:
            return "committed_uncertain"
        return "written"
    except Unavailable:
        raise
    except (OSError, ValueError, TypeError, OverflowError):
        raise Unavailable("ledger_write_failed") from None
    finally:
        if temp_fd >= 0:
            os.close(temp_fd)
        if not committed:
            try:
                named = os.stat(temporary, dir_fd=meter_fd, follow_symlinks=False)
                if temp_identity == (named.st_dev, named.st_ino):
                    os.unlink(temporary, dir_fd=meter_fd)
            except OSError:
                pass


def _refresh_ledger(home):
    """Run one explicit internal refresh; the live CLI does not call this yet."""
    home_fd = cairn_fd = config_fd = meter_fd = lock_fd = old_fd = -1
    try:
        home_fd, cairn_fd, config_fd, config_identity, config_pair = _open_consent_area(home)
        if config_pair is None:
            return {"status": "disabled", "reason": "config_missing"}
        config, config_raw = config_pair
        if not config["enabled"]:
            return {"status": "disabled", "reason": "disabled"}
        if cairn_fd is None:
            raise Unavailable("config_home_unavailable")
        meter_fd = _open_meter_area(cairn_fd)
        lock_fd, lock_identity = _open_lock(meter_fd)
        old_fd, old_raw, old_identity = _read_optional_ledger(meter_fd)
        prior = _load_ledger(old_raw)
        incoming_events, cursors, scan_reasons, verified_forks, fork_conflicts, incoming_waits = _scan_approved_sources(
            config, prior["cursors"])
        incoming_claims, project_remotes, capture_status = _capture_all_claims(config)
        candidate = _new_ledger(prior, config, incoming_events, incoming_waits, cursors,
                                incoming_claims, project_remotes,
                                capture_status, scan_reasons, verified_forks,
                                fork_conflicts)
        result = _atomic_replace_ledger(
            home, home_fd, cairn_fd, meter_fd, lock_fd, lock_identity,
            old_fd if isinstance(old_fd, int) and old_fd >= 0 else None,
            old_raw, old_identity,
            config_fd, config_raw, config_identity, candidate)
        return {"status": result, "reason": "none" if result == "written"
                else "ledger_durability_uncertain", "events": len(candidate["events"]),
                "claims": len(candidate["claims"]), "coverage": "unknown"}
    except Unavailable as exc:
        return {"status": "unavailable", "reason": exc.reason,
                "coverage": "unknown"}
    except (OSError, ValueError, TypeError, OverflowError, KeyError):
        return {"status": "unavailable", "reason": "ledger_unavailable",
                "coverage": "unknown"}
    finally:
        for descriptor in (old_fd, lock_fd, meter_fd, config_fd, cairn_fd, home_fd):
            if isinstance(descriptor, int) and descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass


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
    weights = _RATIO_INDEX["models"].get(model)
    if weights is None:
        return {name: None for name in (*_EVENT_KIND_NAMES, "total")}
    kinds = event["kinds"]
    components = {}
    for name in ("fresh_input", "cache_read", "output"):
        weight = weights[name]
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
            short, long = weights["cache_write_5m"], weights["cache_write_1h"]
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
    timing_candidates = []
    config_supplied = config is not None
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
                reasons = {"project_path_unapproved"}
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
                    cache_write_ttl=cache_write_ttl, reasons=reasons)
                candidates.append((candidate, tuple(candidate["kinds"].items()),
                                   (session, None, None, None), None))
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
                                    copied_parent)))
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
                    "lineage_key": (_digest("codex-lineage", fork_metadata["child"])
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
        issues.add(lines.terminal_reason)
    if len(candidates) > MAX_NORMALIZED_EVENTS:
        candidates.clear()
        timing_candidates.clear()
        issues.add("source_budget_exceeded")

    normalized_waits = []
    for wait in timing_candidates:
        thread, session, turn = wait["_thread"], wait["_session"], wait["_turn"]
        context_entry = contexts.get(((thread, session), turn)) if session is not None else None
        context = None if context_entry is None else context_entry[1]
        reasons = set(wait["reasons"])
        binding_proven = bool(
            context is not None and context.get("owner") == (thread, session)
            and context.get("turn") == turn and context.get("root") == turn
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
                        verified_projects[cache_key] = _verified_project_remote(
                            project, excluded_roots)
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
    for event, usage_signature, binding_signature, details in candidates:
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
        if key not in merged:
            merged[key] = event
            merge_signatures[key] = (usage_signature, binding_signature)
            continue
        prior_usage, prior_binding = merge_signatures[key]
        _merge_normalized_event(merged[key], event)
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
            "events": normalized,
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
            "ownership_coverage": "unknown", "issues": sorted(issues)}


def main():
    """C1 checkpoint CLI: config-only, never enumerates a private source."""
    parser = argparse.ArgumentParser(description="Cairn usage meter (foundation checkpoint)")
    parser.add_argument("--json", action="store_true", help="emit the status as JSON")
    args = parser.parse_args()
    if os.name == "nt":
        status = _windows_config_status()
        code = 0 if status == "disabled" else 5
        result = {"schema": "cairn-meter-foundation/1", "collection": status,
                  "usage": {tool: "unknown" for tool in TOOLS}}
        if args.json:
            print(json.dumps(result, sort_keys=True))
        else:
            print(f"meter: {status}; usage remains unknown for all supported tools")
        return code
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
