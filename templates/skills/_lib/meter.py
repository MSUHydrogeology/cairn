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
try:
    import pwd
except ImportError:  # vendor-ok: POSIX account lookup is deliberately unsupported elsewhere
    pwd = None
try:
    import fcntl
except ImportError:  # vendor-ok: private ledger locking is deliberately unsupported elsewhere
    fcntl = None
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
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
LEDGER_SCHEMA = "cairn-meter-ledger/1"
MAX_SOURCE_ROOT_DEPTH = 32
MAX_REFRESH_ENTRIES = 100_000
MAX_SOURCE_FILES = 10_000
MAX_TOTAL_SOURCE_BYTES = 256 * 1024 * 1024
MAX_RETAINED_EVENTS = 100_000
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

        if (C.sizeof(US), C.sizeof(OA), C.sizeof(IOS), C.sizeof(BHI)) != (16, 48, 16, 52):
            raise Unavailable
        self.US, self.OA, self.IOS, self.BHI = US, OA, IOS, BHI
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

    def _privileged_sid(self, sid_bytes):
        C = self.C
        for value in ("S-1-5-18", "S-1-5-32-544"):
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
        if attrs & (0x400 | 0x40):
            raise Unavailable
        stamp = lambda item: (int(item.dwHighDateTime) << 32) | int(item.dwLowDateTime)
        return {"identity": (int(value.volume), (int(value.id_high) << 32) | int(value.id_low)),
                "size": (int(value.size_high) << 32) | int(value.size_low),
                "directory": bool(attrs & 0x10), "links": int(value.links),
                "created": stamp(value.created), "accessed": stamp(value.accessed),
                "written": stamp(value.written)}

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
        options = 0x00200000 | 0x20 | (0x1 if directory else 0x40)
        status = self.nt.NtCreateFile(C.byref(out), access, C.byref(oa), C.byref(ios),
                                      None, 0, 1, 1, options, None, 0)
        code = status & 0xffffffff
        if status != 0:
            if code in (0xC0000034, 0xC000003A):
                raise _MissingConfig
            raise Unavailable
        return int(out.value)

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
            if role == "ancestor" and owner_bytes != user_sid and not self._privileged_sid(owner_bytes):
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
                    if ace_sid != user_sid and not self._privileged_sid(ace_sid):
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
            if before != after or total != before["size"]:
                raise Unavailable
            return b"".join(blocks)
        finally:
            for handle in reversed(held):
                self.close(handle)


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


def _iter_approved_lines(root, relative, budget=MAX_BATCH_BYTES):
    """Stream complete lines from one explicitly approved synthetic/source path."""
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
    "project_alias", "project_association", "ownership", "model", "account", "reasons",
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
_LEDGER_FIELDS = {
    "schema", "reader_version", "ratio_version", "events", "claims", "cursors",
    "mappings", "project_remotes", "aggregates", "coverage",
}


def _copy_event(event):
    return {name: (value.copy() if isinstance(value, (dict, list)) else value)
            for name, value in event.items()}


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
    if event["account"] is not None:
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


def _load_ledger(raw):
    if raw is None:
        return {
            "schema": LEDGER_SCHEMA, "reader_version": READER_VERSION,
            "ratio_version": "none", "events": [], "claims": [], "cursors": [],
            "mappings": [], "project_remotes": [], "aggregates": [],
            "coverage": {"global": "unknown", "reasons": []},
        }
    try:
        if not isinstance(raw, bytes) or len(raw) > MAX_LEDGER_BYTES:
            raise ValueError
        ledger = json.loads(raw.decode("utf-8"), object_pairs_hook=_object,
                            parse_constant=_constant)
        if not isinstance(ledger, dict) or set(ledger) != _LEDGER_FIELDS:
            raise ValueError
        if (ledger["schema"] != LEDGER_SCHEMA
                or ledger["reader_version"] != READER_VERSION
                or ledger["ratio_version"] != "none"):
            raise ValueError
        if any(not isinstance(ledger[key], list) for key in (
                "events", "claims", "cursors", "mappings", "project_remotes", "aggregates")):
            raise ValueError
        if len(ledger["events"]) > MAX_RETAINED_EVENTS:
            raise ValueError
        event_keys = set()
        for event in ledger["events"]:
            _validate_event(event)
            if event["event_key"] in event_keys:
                raise ValueError
            event_keys.add(event["event_key"])
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
            for field in ("dev", "ino", "generation", "offset", "line",
                          "size", "mtime_ns", "ctime_ns"):
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
        for aggregate in ledger["aggregates"]:
            if (not isinstance(aggregate, dict)
                    or set(aggregate) != {"project_alias", "day", "tool", "model",
                                          "events", "unknown_events", "kinds"}):
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
            or any(value is None for value in prior["kinds"].values())
            or any(value is None for value in incoming["kinds"].values())):
        prior["kinds"] = _unknown_kinds()
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
    if "conflicting_binding" in reasons or identity_conflict:
        for field in ("thread_key", "session_digest", "session_key", "turn_key", "root_turn_key"):
            prior[field] = None
        prior["project_alias"] = None
        prior["project_association"] = "unknown"
        prior["ownership"] = "unknown"
        prior["model"] = None
        reasons.add("conflicting_binding")
    else:
        if prior["ownership"] == "unknown" and incoming["ownership"] == "proven":
            prior["ownership"] = "proven"
        if prior["session_digest"] is None:
            prior["session_digest"] = incoming["session_digest"]
        if prior["thread_key"] is None:
            prior["thread_key"] = incoming["thread_key"]
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
                reasons.add("conflicting_binding")
        elif incoming["project_association"] == "current_local_verified":
            prior["project_alias"] = incoming["project_alias"]
            prior["project_association"] = "current_local_verified"
        if prior["model"] is None:
            prior["model"] = incoming["model"]
        elif incoming["model"] is not None and prior["model"] != incoming["model"]:
            prior["model"] = None
            reasons.add("conflicting_binding")
    if "conflicting_binding" in reasons:
        for field in ("thread_key", "session_digest", "session_key", "turn_key", "root_turn_key"):
            prior[field] = None
        prior["project_alias"] = None
        prior["project_association"] = "unknown"
        prior["ownership"] = "unknown"
        prior["model"] = None
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


def _recompute_aggregates(events, config):
    tool_by_alias = {source["alias"]: source["tool"] for source in config["sources"]}
    groups = {}
    for event in events:
        aliases = event["source_aliases"]
        tools = {tool_by_alias[alias] for alias in aliases if alias in tool_by_alias}
        tool = next(iter(tools)) if len(tools) == 1 else None
        project = (event["project_alias"]
                   if event["project_association"] == "current_local_verified" else None)
        day = None
        if event["time_coverage"] == "known" and event["observed_at"] is not None:
            day = datetime.fromisoformat(
                event["observed_at"].replace("Z", "+00:00")).astimezone(timezone.utc).date().isoformat()
        key = (project, day, tool, event["model"])
        group = groups.setdefault(key, {"events": [], "unknown": 0})
        group["events"].append(event)
        if any(value is None for value in event["kinds"].values()):
            group["unknown"] += 1
    result = []
    for (project, day, tool, model), group in sorted(
            groups.items(), key=lambda item: tuple("" if v is None else str(v)
                                                   for v in item[0])):
        kinds = {}
        for name in _EVENT_KIND_NAMES:
            values = [event["kinds"][name] for event in group["events"]]
            kinds[name] = None if any(value is None for value in values) else sum(values)
        result.append({"project_alias": project, "day": day, "tool": tool,
                       "model": model, "events": len(group["events"]),
                       "unknown_events": group["unknown"], "kinds": kinds})
    return result


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
    incoming = _merge_event_batches(batches)
    if len(incoming) > MAX_RETAINED_EVENTS:
        raise Unavailable
    return incoming, sorted(cursors.values(), key=lambda item: item["file_key"]), reasons


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


def _new_ledger(prior, config, incoming_events, cursors, incoming_claims,
                project_remotes, capture_status, scan_reasons):
    events = _merge_events(prior["events"], incoming_events)
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
    mappings = _build_mappings(events, claims, config)
    reasons = set(scan_reasons)
    reasons.update(status for status in capture_status if status != "captured")
    return {
        "schema": LEDGER_SCHEMA, "reader_version": READER_VERSION,
        "ratio_version": "none", "events": events, "claims": claims,
        "cursors": cursors, "mappings": mappings,
        "project_remotes": sorted(project_remotes, key=lambda item: item["alias"]),
        "aggregates": _recompute_aggregates(events, config),
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
        incoming_events, cursors, scan_reasons = _scan_approved_sources(
            config, prior["cursors"])
        incoming_claims, project_remotes, capture_status = _capture_all_claims(config)
        candidate = _new_ledger(prior, config, incoming_events, cursors,
                                incoming_claims, project_remotes,
                                capture_status, scan_reasons)
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


def _short_session_digest(raw_id):
    """Match the existing intent session digest without importing its writer."""
    if not isinstance(raw_id, str) or not raw_id.strip():
        return None
    return hashlib.sha256(raw_id.strip().encode("utf-8")).hexdigest()[:8]


def _event_record(*, tool, event_key, aliases, thread, session=None, turn=None,
                  root=None, timestamp=None, time_known=False, kinds=None,
                  project_alias=None, project_state="unknown", ownership="unknown",
                  model=None, session_digest=None, reasons=()):
    return {
        "event_key": event_key,
        "source_aliases": sorted(set(aliases)),
        "thread_key": _digest(tool, thread) if thread else None,
        "session_digest": session_digest,
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
    binding_fields = ("thread_key", "session_digest", "session_key", "turn_key", "root_turn_key",
                      "project_alias", "project_association", "ownership", "model")
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
                    session=session, session_digest=_short_session_digest(session),
                    timestamp=timestamp, time_known=time_known,
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
                    ownership=ownership, model=model,
                    session_digest=(_short_session_digest(thread) if binding_proven else None),
                    reasons=reasons)
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
                event["session_digest"] = None
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
                                 event["session_digest"],
                                 event["turn_key"], event["root_turn_key"],
                                 event["project_alias"], event["project_association"],
                                 event["ownership"], event["model"])
        else:
            usage_signature = tuple(event["kinds"].items())
            binding_signature = (event["thread_key"], event["session_key"],
                                 event["session_digest"],
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
            merged[key]["session_digest"] = None
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
