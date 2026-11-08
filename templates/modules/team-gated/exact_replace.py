#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Bounded exact text replacement for repository files (stdlib only)."""
from __future__ import annotations

import argparse
from array import array
import hashlib
import json
import os
import queue
import re
import stat
import sys
import threading
import time
import types

_HERE = os.path.dirname(os.path.abspath(__file__))
_SOURCE = (os.path.basename(_HERE) == "team-gated"
           and os.path.basename(os.path.dirname(_HERE)) == "modules")
_ROOT = os.path.abspath(os.path.join(_HERE, "../../..")) if _SOURCE else os.path.dirname(_HERE)
_GIT_REL = "templates/skills/_lib/git_read.py" if _SOURCE else "tools/git_read.py"
_GIT_SHA256 = "ec471c34c18ff4698ef6f2511d4e9e5d29b76190ec2a9a9f2e8524c5827db9c3"
_REPORT_REL = "templates/modules/team-gated/prose_diff.py" if _SOURCE else "scripts/prose_diff.py"
_REPORT_SHA256 = "180db64cf8bbfd9af9a70b9bda1267b06a655edd31b3715ebdbacdd8dbcbc414"
_HELPER_CAP = 256 * 1024
_FILE_CAP = 8 * 1024 * 1024
_JSON_CAP = 16 * 1024 * 1024
_AGG_CAP = 64 * 1024 * 1024
_PAIR_CAP = 256
_WORK_CAP = 128 * 1024 * 1024
_DEADLINE_SECONDS = 120.0
_START = time.monotonic()


class Refused(Exception):
    pass


def _deadline():
    if time.monotonic() - _START > _DEADLINE_SECONDS:
        raise Refused("invocation deadline exceeded")


def _identity(info):
    return (int(info.st_dev), int(info.st_ino), int(info.st_mode),
            int(info.st_size), int(info.st_mtime_ns), int(info.st_ctime_ns),
            int(getattr(info, "st_uid", 0) or 0), int(getattr(info, "st_gid", 0) or 0),
            int(getattr(info, "st_file_attributes", 0) or 0), int(getattr(info, "st_reparse_tag", 0) or 0))


def _chain(path):
    path = os.path.abspath(path)
    drive, tail = os.path.splitdrive(path)
    current = drive + os.sep
    rows = []
    for part in (p for p in tail.split(os.sep) if p):
        current = os.path.join(current, part)
        info = os.lstat(current)
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise Refused("linked or reparse path component")
        if current != path and not stat.S_ISDIR(info.st_mode):
            raise Refused("non-directory path parent")
        rows.append((current, info))
    return rows


def _open_checked(path, cap):
    rows = _chain(path)
    before = rows[-1][1]
    if not stat.S_ISREG(before.st_mode) or before.st_size < 0 or before.st_size > cap:
        raise Refused("input is not a bounded regular file")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(path, flags)
    try:
        opened = os.fstat(fd)
        opened_key = list(_identity(opened)); path_key = list(_identity(before))
        if os.name == "nt":
            path_birth = getattr(before, "st_birthtime_ns", None)
            descriptor_birth = getattr(opened, "st_birthtime_ns", None)
            if (type(path_birth) is not int or type(descriptor_birth) is not int or
                    before.st_ctime_ns != path_birth or path_birth != descriptor_birth):
                raise Refused("input creation-time mapping failed")
            opened_key[5] = descriptor_birth
        if tuple(opened_key) != tuple(path_key):
            raise Refused("input changed while opening")
        chunks, size = [], 0
        while size <= cap:
            _deadline()
            part = os.read(fd, min(65536, cap + 1 - size))
            if not part: break
            chunks.append(part); size += len(part)
        after = os.fstat(fd)
        if size > cap or size != opened.st_size or _identity(opened) != _identity(after):
            raise Refused("input changed or exceeded its byte limit")
        for name, expected in rows:
            if _identity(os.lstat(name)) != _identity(expected):
                raise Refused("input path changed while reading")
        return b"".join(chunks), rows
    finally:
        os.close(fd)


def _stream_source(path, cap):
    """Read a possibly blocking source on an abandonable bounded daemon."""
    channel = queue.Queue(maxsize=2)
    stop = threading.Event()
    def send(item):
        while not stop.is_set():
            try: channel.put(item, timeout=max(0.001, min(0.1, _DEADLINE_SECONDS - (time.monotonic() - _START))))
            except queue.Full: continue
            return
    def worker():
        fd = None
        try:
            if path == "-":
                fd = os.dup(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.setmode(fd, os.O_BINARY)
            else:
                rows = _chain(path)
                before = rows[-1][1]
                if not stat.S_ISREG(before.st_mode) or before.st_size > cap:
                    raise Refused("source is not a bounded regular file")
                fd = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
                opened = os.fstat(fd)
                opened_key = list(_identity(opened)); before_key = list(_identity(before))
                if os.name == "nt":
                    path_birth = getattr(before, "st_birthtime_ns", None)
                    descriptor_birth = getattr(opened, "st_birthtime_ns", None)
                    if (type(path_birth) is not int or type(descriptor_birth) is not int or
                            before.st_ctime_ns != path_birth or path_birth != descriptor_birth):
                        raise Refused("source creation-time mapping failed")
                    opened_key[5] = descriptor_birth
                if tuple(opened_key) != tuple(before_key): raise Refused("source changed while opening")
                send(("meta", rows, _identity(opened)))
            total = 0
            while total <= cap and not stop.is_set():
                part = os.read(fd, min(65536, cap + 1 - total))
                if not part: break
                total += len(part); send(("data", part))
            if path != "-" and _identity(os.fstat(fd)) != _identity(opened):
                raise Refused("source changed while reading")
            send(("end", total))
        except BaseException as exc:
            send(("error", exc if isinstance(exc, Refused) else Refused("source read failed")))
        finally:
            if fd is not None:
                try: os.close(fd)
                except OSError: pass
    threading.Thread(target=worker, daemon=True, name="cairn-bounded-input").start()
    chunks, size, metadata = [], 0, None
    try:
        while True:
            _deadline()
            try: item = channel.get(timeout=max(0.001, min(0.1, _DEADLINE_SECONDS - (time.monotonic() - _START))))
            except queue.Empty: continue
            if item[0] == "meta": metadata = item[1:]
            elif item[0] == "data":
                size += len(item[1])
                if size > cap: raise Refused("source byte limit exceeded")
                chunks.append(item[1])
            elif item[0] == "error": raise item[1]
            else:
                if item[1] != size: raise Refused("source read count changed")
                if path != "-":
                    rows, expected = metadata
                    if expected != _identity(os.stat(path, follow_symlinks=False)):
                        raise Refused("source changed while reading")
                    for name, old in rows:
                        if _identity(os.lstat(name)) != _identity(old): raise Refused("source path changed while reading")
                return b"".join(chunks)
    except BaseException:
        stop.set()
        raise


def _read_source(path, cap):
    return _stream_source(path, cap)


def _load_module(path, digest, name):
    data, _ = _open_checked(path, _HELPER_CAP)
    if hashlib.sha256(data).hexdigest() != digest:
        raise Refused("trusted module hash mismatch")
    module = types.ModuleType(name)
    module.__file__ = "<verified source buffer>"
    module.__verified_source__ = data
    module.__verified_sha256__ = digest
    exec(compile(data, module.__file__, "exec", dont_inherit=True), module.__dict__)
    if name.endswith("git"):
        module.bind_verified_source(data, digest)
    return module


def _require_lock_hash(destination, digest):
    path = os.path.join(_ROOT, "dev", ".cairn", "cairn-lock.yml")
    raw, _ = _open_checked(path, 2 * 1024 * 1024)
    try:
        body = "\n".join(line for line in raw.decode("utf-8", "strict").splitlines()
                           if not line.lstrip().startswith("#"))
        lock = json.loads(body)
    except (UnicodeError, ValueError, RecursionError, MemoryError):
        raise Refused("install lock is invalid") from None
    files = lock.get("files") if isinstance(lock, dict) else None
    if not isinstance(files, list): raise Refused("install lock has no file records")
    matches = [row for row in files if isinstance(row, dict) and row.get("dst") == destination]
    if len(matches) != 1 or matches[0].get("verbatim") is not True or matches[0].get("hash") != digest:
        raise Refused("install lock does not uniquely pin the trusted binding")


def _git_binding():
    if not _SOURCE: _require_lock_hash("tools/git_read.py", _GIT_SHA256)
    path = os.path.join(_ROOT, _GIT_REL)
    return _load_module(path, _GIT_SHA256, "_cairn_verified_git_read")


def _report_binding():
    if not _SOURCE: _require_lock_hash("scripts/prose_diff.py", _REPORT_SHA256)
    path = os.path.join(_ROOT, _REPORT_REL)
    return _load_module(path, _REPORT_SHA256, "_cairn_verified_prose_diff")


def _parse_batch(raw):
    if len(raw) > _JSON_CAP: raise Refused("JSON batch exceeds 16 MiB")
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result: raise Refused("duplicate JSON object key")
            result[key] = value
        return result
    try: pairs = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=unique_object)
    except (UnicodeError, ValueError, RecursionError, MemoryError): raise Refused("invalid JSON batch") from None
    if not isinstance(pairs, list) or not pairs or len(pairs) > _PAIR_CAP:
        raise Refused("batch must contain 1 to 256 pairs")
    result = []
    for item in pairs:
        if not isinstance(item, dict) or set(item) != {"old", "new"} or type(item["old"]) is not str or type(item["new"]) is not str or not item["old"]:
            raise Refused("each batch item needs exactly nonempty old and string new")
        old = item["old"].encode("utf-8", "strict")
        new = item["new"].encode("utf-8", "strict")
        if len(old) > _FILE_CAP or len(new) > _FILE_CAP: raise Refused("decoded pair exceeds 8 MiB")
        result.append((old, new))
    return result


def _kmp_positions(haystack, needle):
    prefix = array("I", [0]) * len(needle)
    q = 0
    steps = 0
    for i in range(1, len(needle)):
        while q and needle[q] != needle[i]:
            q = prefix[q - 1]; steps += 1
            if steps % 65536 == 0: _deadline()
        steps += 1
        if steps % 65536 == 0: _deadline()
        if needle[q] == needle[i]: q += 1
        prefix[i] = q
    found, count, q = [], 0, 0
    for i, byte in enumerate(haystack):
        while q and needle[q] != byte:
            q = prefix[q - 1]; steps += 1
            if steps % 65536 == 0: _deadline()
        steps += 1
        if steps % 65536 == 0: _deadline()
        if needle[q] == byte: q += 1
        if q == len(needle):
            count += 1
            if len(found) < 2048: found.append(i - len(needle) + 1)
            q = prefix[q - 1]
    return count, found


def _line_numbers(raw, positions):
    kept = positions[:2048]
    result = []
    start = 0
    newlines = []
    for pos, byte in enumerate(raw):
        if byte == 10: newlines.append(pos)
        if pos % 65536 == 0: _deadline()
    import bisect
    for p in kept: result.append(bisect.bisect_left(newlines, p) + 1)
    return result


def _target_path(raw):
    try: target = raw.decode("utf-8", "strict")
    except UnicodeError: raise Refused("target path is not UTF-8") from None
    if not target or target.startswith(("/", "\\")) or ":" in target or "\\" in target or "\x00" in target:
        raise Refused("target must be repository-root-relative")
    parts = target.split("/")
    if any(p in {"", ".", ".."} or p.casefold() == ".git" or re.fullmatch(r"(?i)GIT~[0-9]+", p) for p in parts):
        raise Refused("target path contains a refused component")
    return target


def _target_read(path):
    root_real = os.path.realpath(_ROOT)
    target_real = os.path.realpath(path)
    try:
        if os.path.commonpath((os.path.normcase(root_real), os.path.normcase(target_real))) != os.path.normcase(root_real):
            raise Refused("target resolves outside the repository root")
    except ValueError:
        raise Refused("target resolves outside the repository root") from None
    rows = _chain(path)
    info = rows[-1][1]
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > _FILE_CAP:
        raise Refused("target is not a bounded single-link regular file")
    data, _rows = _open_checked(path, _FILE_CAP)
    try: data.decode("utf-8", "strict")
    except UnicodeError: raise Refused("target is not valid UTF-8") from None
    return data, rows, info.st_mode


def _same_target(path, rows, mode, digest):
    try:
        now = _chain(path)
        if len(now) != len(rows): return False
        for index, ((n, a), (o, b)) in enumerate(zip(now, rows)):
            if n != o: return False
            if index < len(now) - 1:
                if (a.st_dev, a.st_ino, a.st_mode) != (b.st_dev, b.st_ino, b.st_mode): return False
            elif _identity(a) != _identity(b): return False
        info = now[-1][1]
        data, _ = _open_checked(path, _FILE_CAP)
        return info.st_nlink == 1 and info.st_mode == mode and hashlib.sha256(data).hexdigest() == digest
    except (OSError, Refused): return False


def _atomic_replace(path, old, new, rows, mode):
    """Stage and replace a sibling file; a swap after the final check is residual.

    The accepted race after that check and through an already-open target handle
    remains. On Windows, an open/read-only replacement failure is a refusal.
    """
    import tempfile
    parent = os.path.dirname(path)
    fd = None; temp = None
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        for _ in range(20):
            _deadline()
            temp = os.path.join(parent, ".cairn-replace-" + os.urandom(12).hex() + ".tmp")
            try: fd = os.open(temp, flags, stat.S_IMODE(mode)); break
            except FileExistsError: continue
        if fd is None: raise Refused("could not reserve a temporary sibling")
        if hasattr(os, "fchmod"):
            os.fchmod(fd, stat.S_IMODE(mode))
        else:
            os.chmod(temp, stat.S_IMODE(mode))
        view = memoryview(new)
        while view:
            _deadline()
            count = os.write(fd, view[:65536])
            if count <= 0: raise Refused("temporary write failed")
            view = view[count:]
        os.fsync(fd); os.close(fd); fd = None
        _deadline()
        if not _same_target(path, rows, mode, hashlib.sha256(old).hexdigest()):
            raise Refused("target changed before replacement")
        _deadline()
        os.replace(temp, path); temp = None
        try:
            dfd = os.open(parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)); os.fsync(dfd); os.close(dfd)
        except OSError: pass
    finally:
        if fd is not None: os.close(fd)
        if temp is not None:
            try: os.unlink(temp)
            except OSError: pass


def _emit(payload):
    data = payload.encode("utf-8", "backslashreplace")[:_FILE_CAP]
    def writer():
        try:
            fd = 1
            view = memoryview(data)
            while view:
                n = os.write(fd, view[:65536])
                if n <= 0: return
                view = view[n:]
        except OSError: return
    thread = threading.Thread(target=writer, daemon=True, name="cairn-bounded-output")
    thread.start()
    thread.join(timeout=0.2)


def _apply(args):
    _deadline()
    # Bind both trusted entry points before reading any user-supplied source.
    git_helper = _git_binding()
    report = _report_binding()
    target = _target_path(os.fsencode(args.target))
    full = os.path.join(_ROOT, *target.split("/"))
    old_target, target_rows, mode = _target_read(full)
    if args.batch:
        if args.old_file is not None or args.new_file is not None: raise Refused("choose --batch or old/new sources")
        raw = _read_source(args.batch, _JSON_CAP)
        pairs = _parse_batch(raw)
        raw_total = len(old_target) + len(raw)
    else:
        if args.old_file is None or args.new_file is None: raise Refused("both --old-file and --new-file are required")
        if args.old_file == "-" and args.new_file == "-": raise Refused("stdin may supply only one source")
        old_raw = _read_source(args.old_file, _FILE_CAP); new_raw = _read_source(args.new_file, _FILE_CAP)
        try: old_raw.decode("utf-8", "strict"); new_raw.decode("utf-8", "strict")
        except UnicodeError: raise Refused("replacement sources must be valid UTF-8") from None
        if not old_raw: raise Refused("old text must not be empty")
        pairs = [(old_raw, new_raw)]
        raw_total = len(old_target) + len(old_raw) + len(new_raw)
    decoded_total = (sum(len(a) + len(b) for a, b in pairs) if args.batch else 0)
    if raw_total + decoded_total > _AGG_CAP: raise Refused("aggregate input limit exceeded")
    result = old_target
    work_total = 0
    for old, new in pairs:
        if not old: raise Refused("old text must not be empty")
        work = 2 * (len(old) + len(result))
        work_total += work
        if work_total > _WORK_CAP: raise Refused("matching work limit exceeded")
        count, positions = _kmp_positions(result, old)
        if count != 1:
            lines = _line_numbers(result, positions)
            raise LookupError(f"match count {count}; lines {lines}; omitted {max(0, count-len(lines))}")
        position = positions[0]
        result_size = len(result) - len(old) + len(new)
        if result_size > _FILE_CAP: raise Refused("replacement result exceeds 8 MiB")
        result = result[:position] + new + result[position + len(old):]
    _deadline()
    _atomic_replace(full, old_target, result, target_rows, mode)
    # Call only code from the verified report buffer; a post-write report
    # failure is distinct because the target has already been updated.
    if time.monotonic() - _START > _DEADLINE_SECONDS:
        _emit("Applied, but reporting exceeded the invocation deadline.\n")
        return 3
    try:
        report_text = report.report_text_change(
            git_helper, _ROOT, target, old_target.decode("utf-8"), result.decode("utf-8"))
        if time.monotonic() - _START > _DEADLINE_SECONDS:
            raise Refused("reporting exceeded the invocation deadline")
    except BaseException as exc:
        _emit("Applied, but the change report failed: " + str(exc) + "\n")
        return 3
    _emit("Applied exactly one replacement sequence.\n" + report_text + "\n")
    return 0


def main(argv=None):
    global _START
    _START = time.monotonic()
    parser = argparse.ArgumentParser(prog="exact_replace.py")
    parser.add_argument("target")
    parser.add_argument("--old-file")
    parser.add_argument("--new-file")
    parser.add_argument("--batch")
    args = parser.parse_args(argv)
    try: return _apply(args)
    except LookupError as exc:
        _emit("No write: " + str(exc) + "\n"); return 1
    except (Refused, OSError, ValueError, UnicodeError, MemoryError, RecursionError) as exc:
        _emit("Refused without write: " + str(exc) + "\n"); return 2
    except BaseException:
        _emit("Applied or report state uncertain; inspect target before retrying.\n"); return 3


if __name__ == "__main__":
    raise SystemExit(main())
