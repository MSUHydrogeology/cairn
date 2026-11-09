# SPDX-License-Identifier: MIT
"""Synthetic-only contracts for tools/meter.py; no host-source access."""

import copy
import ctypes
import importlib.util
import json
import io
import os
import runpy
import stat
import struct
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[3]
METER = ROOT / "tools/meter.py"
spec = importlib.util.spec_from_file_location("meter_reader", METER)
meter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meter)
STAMP = "2026-11-05T12:00:00Z"
POSIX_ONLY = pytest.mark.skipif(os.name != "posix", reason="private-file checks require POSIX evidence")
EVENT_FIELDS = {"event_key", "source_aliases", "thread_key", "session_key", "turn_key",
                "session_digest", "root_turn_key", "observed_at", "time_coverage", "kinds",
                "cache_write_ttl", "project_alias", "project_association", "ownership",
                "model", "model_provenance", "effective_model", "account", "lineage_key",
                "reasons"}


def encoded(records):
    return [(json.dumps(record) + "\n").encode() for record in records]


def row(kind, payload):
    return {"type": kind, "timestamp": STAMP, "payload": payload}


def codex():
    owner = "019a0000-0000-7000-8000-000000000001"
    usage = {"input_tokens": 20, "cached_input_tokens": 8,
             "cache_write_input_tokens": 0, "output_tokens": 4,
             "reasoning_output_tokens": 2, "total_tokens": 24}
    return [
        row("session_meta", {"id": owner, "session_id": owner, "source": "cli",
                              "thread_source": "user", "history_mode": "legacy"}),
        row("turn_context", {"turn_id": "turn-a", "cwd": "/synthetic/repo-a"}),
        row("token_usage_record", {
            "thread_id": owner, "session_id": owner, "turn_id": "turn-a",
            "root_turn_id": "turn-a", "response_id": "response-a",
            "usage": copy.deepcopy(usage),
            "turn_token_usage": copy.deepcopy(usage),
            "thread_token_usage": copy.deepcopy(usage),
        }),
    ]


def codex_direct(thread, session, turn, root, response, input_count,
                 turn_count, thread_count, *, cache_read=0):
    usage = {"input_tokens": input_count + cache_read,
             "cached_input_tokens": cache_read,
             "output_tokens": 0, "reasoning_output_tokens": 0,
             "total_tokens": input_count + cache_read}
    turn_usage = dict(usage, input_tokens=turn_count,
                      total_tokens=turn_count)
    thread_usage = dict(usage, input_tokens=thread_count,
                        total_tokens=thread_count)
    return row("token_usage_record", {
        "thread_id": thread, "session_id": session, "turn_id": turn,
        "root_turn_id": root, "response_id": response,
        "usage": usage, "turn_token_usage": turn_usage,
        "thread_token_usage": thread_usage,
    })


def codex_fork_fixture(project, *, parent_input=100):
    parent = "019a0000-0000-7000-8000-000000000011"
    child = "019a0000-0000-7000-8000-000000000022"
    root_turn, child_turn = "turn-parent", "turn-child"
    parent_header = row("session_meta", {
        "id": parent, "session_id": parent, "source": "cli",
        "thread_source": "user", "history_mode": "legacy",
    })
    parent_context = row("turn_context", {
        "turn_id": root_turn, "root_turn_id": root_turn,
        "cwd": str(project), "model": "gpt-5.3-codex",
    })
    parent_usage = codex_direct(parent, parent, root_turn, root_turn,
                                "response-parent", parent_input,
                                parent_input, parent_input)
    child_header = row("session_meta", {
        "id": child, "session_id": parent, "source": {
            "subagent": {"thread_spawn": {
                "parent_thread_id": parent, "depth": 1}}},
        "thread_source": "subagent", "forked_from_id": parent,
        "parent_thread_id": parent, "history_mode": "legacy",
    })
    marker = row("event_msg", {"type": "task_started", "turn_id": child_turn})
    child_context = row("turn_context", {
        "turn_id": child_turn, "root_turn_id": root_turn,
        "cwd": str(project), "model": "gpt-5.3-codex",
    })
    child_usage = codex_direct(child, parent, child_turn, root_turn,
                               "response-child", 30, 30,
                               parent_input + 30)
    parent_rows = [parent_header, parent_context, parent_usage]
    child_rows = [child_header, parent_header, parent_context,
                  parent_usage, marker, child_context, child_usage]
    return parent_rows, child_rows, parent, child


def claude():
    return [{"type": "assistant", "timestamp": STAMP, "sessionId": "session-a",
             "requestId": "request-a", "cwd": "/synthetic/not-proof",
             "message": {"id": "message-a", "model": "synthetic-model",
                         "content": "SECRET-BODY", "usage": {
                             "input_tokens": 10, "output_tokens": 4,
                             "cache_creation_input_tokens": 2,
                             "cache_read_input_tokens": 8}}}]


def read(tool, records):
    return meter.read_records(tool, encoded(records))


def c2_home(tmp_path, *, enabled=True, records=None, claims=None):
    home = tmp_path / "account-home"
    home.mkdir()
    cairn = home / ".cairn"
    cairn.mkdir(mode=0o700)
    cairn.chmod(0o700)
    source_root = tmp_path / "approved-source"
    source_root.mkdir()
    project = tmp_path / "approved-project"
    project.mkdir()
    (project / ".git").mkdir()
    (project / ".git" / "config").write_text(
        '[remote "origin"]\n\turl = https://example.test/team/project.git\n',
        encoding="utf-8")
    (project / "dev").mkdir()
    (project / "dev" / "measurement").mkdir()
    (project / "dev" / "intents.jsonl").write_bytes(
        b"" if claims is None else b"".join(encoded(claims)))
    if records is not None:
        (source_root / "session.jsonl").write_bytes(b"".join(encoded(records)))
    config = {"version": 1, "enabled": enabled,
              "sources": [{"alias": "codex-source", "tool": "codex",
                           "root": str(source_root)}],
              "projects": [{"alias": "sample", "path": str(project),
                            "remote": "https://example.test/team/project.git"}]}
    config_path = cairn / "meter.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    config_path.chmod(0o600)
    return home, source_root, project, config_path


def windows_config_bytes(enabled=True):
    return json.dumps({
        "version": 1, "enabled": enabled,
        "sources": [{"alias": "source", "tool": "codex",
                     "root": str(Path("/synthetic/source").absolute())}],
        "projects": [{"alias": "project",
                      "path": str(Path("/synthetic/project").absolute()),
                      "remote": "https://example.test/team/project.git"}],
    }).encode()


class SyntheticWindowsConsent:
    def __init__(self, content):
        self.content = content
        self.calls = []

    def current_user_profile(self):
        self.calls.append("profile")
        return "C:\\synthetic\\profile", b"synthetic-user-sid"

    def read_config(self, profile, sid):
        self.calls.append(("config", profile, sid))
        if isinstance(self.content, Exception):
            raise self.content
        return self.content


class SyntheticWindowsStreamAPI:
    """Small native-call seam for the shared Windows line-stream checks."""

    def __init__(self, content):
        import ctypes

        self.C = ctypes
        self.W = SimpleNamespace(DWORD=ctypes.c_uint32)
        self.content = content
        self.entry_file_id = 4
        self.offsets = {}
        self.paths = {}
        self.next_handle = 1
        self.accessed = 21
        self.directory_written = 31
        self.closed = []
        self.kernel = SimpleNamespace(
            QueryDosDeviceW=self.query_dos_device,
            GetVolumeInformationByHandleW=self.volume_info,
            ReadFile=self.read_file,
        )

    def current_user_profile(self):
        return "C:\\unused-profile", b"synthetic-user-sid"

    def query_dos_device(self, drive, buffer, size):
        buffer.value = r"\Device\HarddiskVolume7"
        return 1

    def volume_info(self, handle, volume, volume_size, serial, maximum, flags,
                    fs_name, fs_name_size):
        fs_name.value = "NTFS"
        return 1

    def open(self, name, parent=None, *, directory=False, read_data=False):
        parent_path = self.paths.get(parent)
        if parent is None:
            path = "volume"
        elif parent_path == "volume" and name == "synthetic":
            path = "synthetic"
        elif parent_path == "synthetic" and name == "source":
            path = "source"
        elif parent_path == "source" and name == "session.jsonl":
            path = "file"
        else:
            raise meter.Unavailable("source_read_unavailable")
        handle = self.next_handle
        self.next_handle += 1
        self.paths[handle] = path
        self.offsets[handle] = 0
        return handle

    def enumerate(self, parent, remaining):
        assert remaining >= 1
        assert self.paths[parent] == "source"
        return [{"name": "session.jsonl", "file_id": self.entry_file_id,
                 "size": len(self.content), "directory": False,
                 "reparse": False, "device": False,
                 "offline": False, "recall": False}]

    def info(self, handle):
        path = self.paths[handle]
        is_file = path == "file"
        return {"identity": (7, {"volume": 1, "synthetic": 2,
                                  "source": 3, "file": 4}[path]),
                "size": len(self.content) if is_file else 0,
                "directory": not is_file, "links": 1,
                "created": 11, "accessed": self.accessed,
                "written": self.directory_written, "changed": 41,
                "mtime_ns": 3100, "ctime_ns": 4100}

    def check_acl(self, handle, user_sid, role):
        assert user_sid == b"synthetic-user-sid"

    def read_file(self, handle, buffer, size, received, overlapped):
        start = self.offsets[handle]
        count = min(size, len(self.content) - start)
        if count:
            self.C.memmove(buffer, self.content[start:start + count], count)
            self.offsets[handle] += count
            self.accessed += 1
        self.C.cast(received, self.C.POINTER(self.W.DWORD)).contents.value = count
        return 1

    def close(self, handle):
        self.closed.append(handle)


class SyntheticWindowsLedgerAPI:
    """Temporary-filesystem model for native transaction ordering and failures."""

    def __init__(self, fail_flush=None, *, post_rename_created=None,
                 post_rename_created_sequence=None, drift_candidate_created=False):
        self.handles = {}
        self.access = {}
        self.share = {}
        self.created = {}
        self.opens = []
        self.next_handle = 1
        self.fail_flush = fail_flush
        self.post_rename_created = post_rename_created
        self.post_rename_created_sequence = post_rename_created_sequence
        self.drift_candidate_created = drift_candidate_created
        self.published_candidate_identity = None
        self.published_candidate_created = None
        self.published_prior_created = None
        self.published_info_count = 0

    def handle(self, path, *, access=0, share=7):
        path = Path(path)
        identity = (path.stat().st_dev, path.stat().st_ino)
        self.created.setdefault(identity, 1000 + len(self.created))
        value = self.next_handle
        self.next_handle += 1
        self.handles[value] = path
        self.access[value] = access
        self.share[value] = share
        return value

    def _check_share(self, path, access, share):
        path = Path(path)
        identity = (path.stat().st_dev, path.stat().st_ino)
        for handle, opened in self.handles.items():
            if not opened.exists():
                continue
            opened_identity = (opened.stat().st_dev, opened.stat().st_ino)
            if identity != opened_identity:
                continue
            prior_access, prior_share = self.access[handle], self.share[handle]
            if ((access & ~prior_share) or (prior_access & ~share)):
                raise PermissionError("synthetic sharing violation")

    def open(self, name, parent, *, read_data=False, write_data=False, delete=False,
             share=1, **_kwargs):
        path = self.handles[parent] / name
        if not path.exists():
            raise meter._MissingConfig
        access = int(read_data) | (int(write_data) << 1) | (int(delete) << 2)
        self._check_share(path, access, share)
        self.opens.append((path.name, access, share))
        return self.handle(path, access=access, share=share)

    def create_private(self, name, parent, _sid, *, directory, delete=False,
                       candidate=False, transaction_parent=False):
        if (type(transaction_parent) is not bool
                or (transaction_parent and
                    (not directory or candidate or delete))
                or (candidate and directory)):
            raise meter.Unavailable("ledger_write_failed")
        path = self.handles[parent] / name
        if directory:
            path.mkdir(mode=0o700)
        else:
            path.touch(mode=0o600, exist_ok=False)
        access = int(directory or candidate) | 2 | (4 if delete or candidate else 0)
        share = (3 if transaction_parent else
                 1 if directory or candidate else 0)
        self.opens.append((path.name, access, share))
        return self.handle(path, access=access, share=share)

    def info(self, handle):
        info = self.handles[handle].stat()
        identity = (info.st_dev, info.st_ino)
        self.created.setdefault(identity, 1000 + len(self.created))
        created = self.created[identity]
        if identity == self.published_candidate_identity:
            if self.post_rename_created_sequence is not None:
                sequence = self.post_rename_created_sequence
                choice = sequence[min(self.published_info_count, len(sequence) - 1)]
                self.published_info_count += 1
                created = self._post_rename_created_value(choice)
            elif self.post_rename_created is not None:
                created = self._post_rename_created_value(self.post_rename_created)
        return {"identity": (1, info.st_ino), "size": info.st_size,
                "directory": self.handles[handle].is_dir(),
                "links": 1 if self.handles[handle].is_dir() else info.st_nlink,
                "created": created, "accessed": info.st_atime_ns,
                "written": info.st_mtime_ns, "changed": info.st_ctime_ns}

    def _post_rename_created_value(self, choice):
        if choice == "candidate":
            return self.published_candidate_created
        if choice == "prior":
            return self.published_prior_created
        return choice

    def check_acl(self, _handle, _sid, _role):
        return None

    def enumerate(self, parent, remaining):
        rows = []
        for path in self.handles[parent].iterdir():
            if len(rows) >= remaining:
                raise meter.Unavailable("source_budget_exceeded")
            info = path.stat()
            rows.append({"name": path.name, "file_id": info.st_ino,
                         "size": info.st_size, "directory": path.is_dir()})
        return sorted(rows, key=lambda row: row["name"])

    def read_bounded(self, handle, limit):
        before = self.info(handle)
        raw = self.handles[handle].read_bytes()
        if len(raw) > limit:
            raise meter.Unavailable("ledger_invalid")
        return raw, before

    def write_all(self, handle, data):
        self.handles[handle].write_bytes(data)
        if self.drift_candidate_created:
            stat = self.handles[handle].stat()
            self.created[(stat.st_dev, stat.st_ino)] = 900001

    def flush_full(self, handle):
        path = self.handles[handle]
        if (self.fail_flush == path.name
                or (self.fail_flush == "candidate"
                    and path.name.startswith((".ledger-", ".meter-")))):
            raise meter.Unavailable("ledger_write_failed")

    def seek_zero(self, _handle):
        return None

    def rename_replace(self, handle, directory, name):
        target = self.handles[directory] / name
        candidate_stat = self.handles[handle].stat()
        candidate_identity = (candidate_stat.st_dev, candidate_stat.st_ino)
        self.published_candidate_identity = candidate_identity
        self.published_candidate_created = self.created[candidate_identity]
        if target.exists():
            prior_stat = target.stat()
            prior_identity = (prior_stat.st_dev, prior_stat.st_ino)
            self.created.setdefault(prior_identity, 1000 + len(self.created))
            self.published_prior_created = self.created[prior_identity]
        self.published_info_count = 0
        self.handles[handle].replace(target)
        self.handles[handle] = target

    def delete_by_handle(self, handle):
        self.handles[handle].unlink()

    def close(self, _handle):
        self.handles.pop(_handle, None)
        self.access.pop(_handle, None)
        self.share.pop(_handle, None)


class SyntheticWindowsProjectAPI(SyntheticWindowsStreamAPI):
    def __init__(self, content, *, missing=False):
        super().__init__(content)
        self.missing = missing
        self.change_after_read = False

    def open(self, name, parent=None, *, directory=False, read_data=False, **_kwargs):
        parent_path = self.paths.get(parent)
        if parent is None:
            path = "volume"
        elif parent_path == "volume" and name == "synthetic":
            path = "synthetic"
        elif parent_path == "synthetic" and name == "project":
            path = "project"
        elif parent_path == "project" and name == "dev":
            path = "dev"
        elif parent_path == "dev" and name == "intents.jsonl" and not self.missing:
            path = "intents"
        else:
            raise meter._MissingConfig
        handle = self.next_handle
        self.next_handle += 1
        self.paths[handle] = path
        self.offsets[handle] = 0
        return handle

    def info(self, handle):
        path = self.paths[handle]
        index = {"volume": 1, "synthetic": 2, "project": 3, "dev": 4,
                 "intents": 5}[path]
        is_file = path == "intents"
        return {"identity": (7, index), "size": len(self.content) if is_file else 0,
                "directory": not is_file, "links": 1,
                "created": 11, "accessed": self.accessed,
                "written": self.directory_written, "changed": 41,
                "mtime_ns": 3100, "ctime_ns": 4100}

    def read_bounded(self, handle, limit):
        before = self.info(handle)
        if len(self.content) > limit:
            raise meter.Unavailable("source_budget_exceeded")
        if self.change_after_read:
            self.directory_written += 1
        return self.content, before


class SyntheticWindowsExportAPI(SyntheticWindowsLedgerAPI):
    def __init__(self, volume_root, fail_flush=None, fail_acl_call=None,
                 missing_at=None, disappear_after_publish=False,
                 missing_during_cleanup=False, post_rename_created=None,
                 post_rename_created_sequence=None, drift_candidate_created=False):
        import ctypes

        super().__init__(fail_flush=fail_flush,
                         post_rename_created=post_rename_created,
                         post_rename_created_sequence=post_rename_created_sequence,
                         drift_candidate_created=drift_candidate_created)
        self.volume_root = Path(volume_root)
        self.fail_acl_call = fail_acl_call
        self.missing_at = missing_at
        self.disappear_after_publish = disappear_after_publish
        self.missing_during_cleanup = missing_during_cleanup
        self.published = False
        self.acl_calls = 0
        self.C = ctypes
        self.W = SimpleNamespace(DWORD=ctypes.c_uint32)

        def query(_drive, buffer, _size):
            buffer.value = r"\Device\HarddiskVolume7"
            return 1

        def volume_info(_handle, _volume, _volume_size, _serial, _maximum,
                        _flags, fs_name, _fs_name_size):
            fs_name.value = "NTFS"
            return 1

        self.kernel = SimpleNamespace(QueryDosDeviceW=query,
                                      GetVolumeInformationByHandleW=volume_info)

    def check_acl(self, _handle, _sid, _role):
        self.acl_calls += 1
        if self.acl_calls == self.fail_acl_call:
            raise meter.Unavailable("source_changed")

    def open(self, name, parent=None, *, directory=False, read_data=False,
             write_data=False, delete=False, share=1, **_kwargs):
        if (name == self.missing_at
                or (self.disappear_after_publish and self.published
                    and name == "meter.json")):
            raise meter._MissingConfig
        path = self.volume_root if parent is None else self.handles[parent] / name
        if not path.exists():
            raise meter._MissingConfig
        if directory and not path.is_dir():
            raise meter.Unavailable("source_read_unavailable")
        access = int(read_data or directory) | (int(write_data) << 1) | (int(delete) << 2)
        self._check_share(path, access, share)
        self.opens.append((path.name, access, share))
        return self.handle(path, access=access, share=share)

    def rename_replace(self, handle, directory, name):
        super().rename_replace(handle, directory, name)
        self.published = True

    def delete_by_handle(self, handle):
        super().delete_by_handle(handle)
        if self.missing_during_cleanup:
            raise meter._MissingConfig


WINDOWS_ONLY = pytest.mark.skipif(os.name != "nt", reason="requires native Windows token, NTFS handles and ACLs")

NATIVE_CSC = Path(r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe")
NATIVE_GIT_FIXTURE = ROOT / "bootstrap" / "tests" / "fixtures" / "native_git_fixture.cs"
NATIVE_METER_ROOT_MARKERS = (
    "__candidate_name__", "__fault_marker__", "__meter_worker_child_pid__",
)


@pytest.fixture(scope="session")
def native_meter_git_exe(request):
    import shutil
    import tempfile

    if os.name != "nt":
        pytest.skip("native Windows Meter controls")
    assert NATIVE_CSC.is_file(), "the authorized Windows compiler is unavailable"
    compile_root = Path(tempfile.mkdtemp(prefix="cairn-meter-git-"))
    request.addfinalizer(lambda: shutil.rmtree(compile_root, ignore_errors=True))
    output = compile_root / "git.exe"
    compiled = __import__("subprocess").run(
        [str(NATIVE_CSC), "/nologo", "/out:" + str(output), str(NATIVE_GIT_FIXTURE)],
        stdin=__import__("subprocess").DEVNULL,
        stdout=__import__("subprocess").PIPE,
        stderr=__import__("subprocess").PIPE, timeout=30, check=False)
    assert compiled.returncode == 0, compiled.stderr.decode("utf-8", "replace")
    assert output.is_file()
    return output


def _native_meter_event():
    kernel = ctypes.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
    kernel.CreateEventW.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                                    ctypes.c_wchar_p]
    kernel.CreateEventW.restype = ctypes.c_void_p
    kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    kernel.WaitForSingleObject.restype = ctypes.c_uint32
    kernel.SetEvent.argtypes = [ctypes.c_void_p]
    kernel.SetEvent.restype = ctypes.c_int
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel.CloseHandle.restype = ctypes.c_int
    name = "CairnGit-" + uuid.uuid4().hex
    handle = kernel.CreateEventW(None, 1, 0, name)
    assert handle, "could not create owned Meter synchronization event"
    return kernel, handle, name


def _native_meter_process_handle(pid):
    from ctypes import wintypes as W
    kernel = ctypes.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
    kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, W.DWORD]
    kernel.WaitForSingleObject.restype = W.DWORD
    kernel.TerminateProcess.argtypes = [ctypes.c_void_p, W.UINT]
    kernel.TerminateProcess.restype = W.BOOL
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel.CloseHandle.restype = W.BOOL
    handle = kernel.OpenProcess(0x00100001, False, pid)
    assert handle, ctypes.get_last_error()
    return kernel, handle


def _native_meter_assignment_handle(pid):
    from ctypes import wintypes as W
    kernel = ctypes.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
    kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel.CloseHandle.restype = W.BOOL
    handle = kernel.OpenProcess(0x00100101, False, pid)
    assert handle, ctypes.get_last_error()
    return kernel, handle


def _native_meter_job():
    from ctypes import wintypes as W

    class Basic(ctypes.Structure):
        _fields_ = [("process_time", ctypes.c_int64), ("job_time", ctypes.c_int64),
                    ("flags", W.DWORD), ("minimum", ctypes.c_size_t),
                    ("maximum", ctypes.c_size_t), ("processes", W.DWORD),
                    ("affinity", ctypes.c_size_t), ("priority", W.DWORD),
                    ("scheduling", W.DWORD)]

    class Io(ctypes.Structure):
        _fields_ = [(name, ctypes.c_uint64) for name in
                    ("read_ops", "write_ops", "other_ops", "read_bytes",
                     "write_bytes", "other_bytes")]

    class Extended(ctypes.Structure):
        _fields_ = [("basic", Basic), ("io", Io),
                    ("process_memory", ctypes.c_size_t),
                    ("job_memory", ctypes.c_size_t),
                    ("peak_process_memory", ctypes.c_size_t),
                    ("peak_job_memory", ctypes.c_size_t)]

    assert ctypes.sizeof(Basic) == 64 and ctypes.sizeof(Extended) == 144
    kernel = ctypes.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
    kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, W.LPCWSTR]
    kernel.CreateJobObjectW.restype = ctypes.c_void_p
    kernel.SetInformationJobObject.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                                ctypes.c_void_p, W.DWORD]
    kernel.SetInformationJobObject.restype = W.BOOL
    kernel.AssignProcessToJobObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    kernel.AssignProcessToJobObject.restype = W.BOOL
    kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel.CloseHandle.restype = W.BOOL
    handle = kernel.CreateJobObjectW(None, None)
    assert handle, ctypes.get_last_error()
    limits = Extended()
    limits.basic.flags = 0x2000
    assert kernel.SetInformationJobObject(handle, 9, ctypes.byref(limits),
                                          ctypes.sizeof(limits)), ctypes.get_last_error()
    return kernel, handle


def _native_meter_setup(root, native_git_exe, *, git_mode="ordinary",
                        source_records=True, meter_overrides=None):
    import hashlib
    import shutil
    import json

    # These sibling entries precede the config reader's held ancestry snapshot;
    # the runner may overwrite them but must never add/remove directory entries.
    for name in NATIVE_METER_ROOT_MARKERS:
        (root / name).write_text("", encoding="ascii")
    source_root = root / "approved-source"
    project = root / "approved-project"
    source_root.mkdir()
    project.mkdir()
    remote = "https://example.invalid/repo.git"
    config = {
        "version": 1, "enabled": True,
        "sources": [{"alias": "source", "tool": "codex",
                     "root": str(source_root)}],
        "projects": [{"alias": "sample", "path": str(project),
                       "remote": remote}],
    }
    _api, _wrapped, profile = native_windows_status(
        root, json.dumps(config).encode("utf-8"))
    (project / ".git").mkdir()
    (project / ".git" / "config").write_text(
        f'[remote "origin"]\n\turl = {remote}\n', encoding="utf-8")
    (project / "dev").mkdir()
    (project / "dev" / "measurement").mkdir()
    owner = "019a0000-0000-7000-8000-000000000001"
    _claim_id, claims = c2_claim_records(owner)
    (project / "dev" / "intents.jsonl").write_bytes(b"".join(encoded(claims)))
    if source_records:
        (source_root / "session-alpha.jsonl").write_bytes(
            b"".join(encoded(c2_codex_records(project))))

    runtime_tools = root / "runtime" / "tools"
    runtime_tools.mkdir(parents=True)
    runtime_meter = runtime_tools / "meter.py"
    runtime_git = runtime_tools / "git_read.py"
    shutil.copyfile(METER, runtime_meter)
    shutil.copyfile(ROOT / "tools" / "git_read.py", runtime_git)
    for original, copied in ((METER, runtime_meter),
                             (ROOT / "tools" / "git_read.py", runtime_git)):
        assert hashlib.sha256(original.read_bytes()).digest() == hashlib.sha256(
            copied.read_bytes()).digest()
    if meter_overrides:
        source = runtime_meter.read_text(encoding="utf-8")
        for old, new in meter_overrides:
            assert source.count(old) == 1
            source = source.replace(old, new, 1)
        runtime_meter.write_text(source, encoding="utf-8")

    bin_dir = root / "git-bin"
    bin_dir.mkdir()
    shutil.copyfile(native_git_exe, bin_dir / "git.exe")
    return {"root": root, "api": _api, "profile": profile, "source": source_root,
            "project": project, "remote": remote, "meter": runtime_meter,
            "git": bin_dir / "git.exe", "bin": bin_dir}


_NATIVE_METER_MAIN_WRAPPER = r'''import ctypes, json, os, runpy, subprocess, sys
meter_path, profile, source_root, git_exe, command, hook, fault, start_ready, start_release, ready, release, done, done_release = sys.argv[1:]
k = ctypes.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
k.OpenEventW.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_wchar_p]
k.OpenEventW.restype = ctypes.c_void_p
k.SetEvent.argtypes = [ctypes.c_void_p]
k.SetEvent.restype = ctypes.c_int
k.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
k.WaitForSingleObject.restype = ctypes.c_uint32
k.CloseHandle.argtypes = [ctypes.c_void_p]
k.CloseHandle.restype = ctypes.c_int
def event(name, wait=False):
    if not name: return
    handle = k.OpenEventW(0x00100002, False, name)
    if not handle: raise OSError(ctypes.get_last_error(), "OpenEventW")
    try:
        if wait:
            if k.WaitForSingleObject(handle, 30000) != 0: raise TimeoutError("event wait")
        elif not k.SetEvent(handle): raise OSError(ctypes.get_last_error(), "SetEvent")
    finally: k.CloseHandle(handle)
def gate():
    event(ready)
    event(release, wait=True)
ns = runpy.run_path(meter_path, run_name="meter_native_control")
globals_ = ns["main"].__globals__
real_api = globals_["_WindowsConsentAPI"]
class SyntheticProfileAPI:
    def __init__(self):
        self.api = real_api()
        _actual_profile, self.sid = self.api.current_user_profile()
        self.state = {"candidate": None, "candidate_parent": None,
                      "candidate_name": None,
                      "candidate_kind": None, "published": False,
                      "candidate_published": False,
                      "source_handle": None, "ready_once": False,
                      "fault_once": False}
        if done:
            original_install = self.api.install_worker_job
            def install_worker_job():
                job = original_install()
                child = subprocess.Popen(
                    [git_exe, "--fixture-child", ready],
                    cwd=os.path.dirname(git_exe), stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    close_fds=True)
                with open(r"__meter_worker_child_pid__", "w", encoding="ascii") as marker:
                    marker.write(str(child.pid))
                return job
            self.api.install_worker_job = install_worker_job
        self._instrument()
    def _instrument(self):
        api, state = self.api, self.state
        if hook == "origin-config-query-failed":
            original_verified_helper = globals_["_verified_git_helper"]
            def verified_helper_with_capture_marker():
                helper = original_verified_helper()
                if helper is None:
                    return None
                class CapturedHelper:
                    def read_origin_from_config(self, *args, **kwargs):
                        result = helper.read_origin_from_config(*args, **kwargs)
                        if (getattr(result, "state", None) == "failed"
                                and getattr(result, "reason", None) ==
                                "origin-config-query-failed"):
                            with open(r"__fault_marker__", "w", encoding="ascii") as marker:
                                marker.write("origin-config-query-failed")
                        return result
                return CapturedHelper()
            globals_["_verified_git_helper"] = verified_helper_with_capture_marker
        original_create = api.create_private
        def create_private(name, parent, sid, **kwargs):
            handle = original_create(name, parent, sid, **kwargs)
            if kwargs.get("candidate"):
                state["candidate"] = handle
                state["candidate_parent"] = parent
                state["candidate_kind"] = "ledger" if name.startswith(".ledger-") else "export"
                state["candidate_name"] = name
                state["candidate_published"] = False
                with open(r"__candidate_name__", "w", encoding="ascii") as marker:
                    marker.write(name)
            return handle
        api.create_private = create_private
        original_open = api.open
        def open_file(name, parent=None, **kwargs):
            wanted_kind = "ledger" if fault.startswith("ledger-") else "export"
            wanted_target = "ledger.json" if wanted_kind == "ledger" else "meter.json"
            if (fault.endswith("-old-reopen") and state["candidate"] is not None
                    and state["candidate_kind"] == wanted_kind
                    and parent == state["candidate_parent"]
                    and name == wanted_target and not state["candidate_published"]
                    and not state["fault_once"]):
                state["fault_once"] = True
                with open(r"__fault_marker__", "w", encoding="ascii") as marker: marker.write("old-reopen")
                return original_open(name, 0x7ffffffe, **kwargs)
            if (state["candidate_published"] and state["candidate_kind"] == wanted_kind
                    and parent == state["candidate_parent"]
                    and fault.endswith("-target-reopen") and name == wanted_target
                    and not state["fault_once"]):
                state["fault_once"] = True
                with open(r"__fault_marker__", "w", encoding="ascii") as marker: marker.write("target-reopen")
                return original_open(name, 0x7ffffffe, **kwargs)
            is_source_root = (hook == "source-root-reparse"
                              and name == os.path.basename(source_root))
            if is_source_root:
                state["opening_source_root"] = True
            try:
                handle = original_open(name, parent, **kwargs)
            finally:
                if is_source_root:
                    state["opening_source_root"] = False
            if (hook in {"source-open-held", "source-info-held"}
                    and name == "session-alpha.jsonl"
                    and kwargs.get("read_data") is True):
                state["source_handle"] = handle
            if is_source_root:
                state["source_root_handle"] = handle
            if (hook == "source-open-held" and name == "session-alpha.jsonl"
                    and kwargs.get("read_data") is True and not state["ready_once"]):
                state["ready_once"] = True
                gate()
            return handle
        api.open = open_file
        original_info = api.info
        def info(handle):
            if (hook == "source-root-reparse" and state.get("opening_source_root")):
                with open(r"__fault_marker__", "a", encoding="ascii") as marker:
                    marker.write("source-root-info-attempted\n")
            try:
                result = original_info(handle)
            except BaseException:
                if (hook == "source-root-reparse" and state.get("opening_source_root")):
                    with open(r"__fault_marker__", "a", encoding="ascii") as marker:
                        marker.write("source-root-info-refused\n")
                raise
            if hook == "source-info-held" and handle == state["source_handle"] and not state["ready_once"]:
                state["ready_once"] = True
                gate()
            return result
        api.info = info
        original_check_acl = api.check_acl
        def check_acl(handle, user_sid, role):
            try:
                return original_check_acl(handle, user_sid, role)
            except BaseException as exc:
                if (getattr(exc, "reason", None) == "unavailable"
                        and hook == "source-info-held" and handle == state.get("source_handle")
                        and state["ready_once"]):
                    with open(r"__fault_marker__", "w", encoding="ascii") as marker:
                        marker.write("bad-acl-recheck")
                raise
        api.check_acl = check_acl
        original_enumerate = api.enumerate
        def enumerate_directory(parent, remaining):
            rows = original_enumerate(parent, remaining)
            if (hook in {"source-enumerated", "source-enumerated-leaf"}
                    and not state["ready_once"]
                    and any(row.get("name") == "session-alpha.jsonl" for row in rows)):
                if hook == "source-enumerated-leaf":
                    row = next(row for row in rows
                               if row.get("name") == "session-alpha.jsonl")
                    assert row.get("directory") is False
                    state["saved_enum_row_file"] = True
                    with open(r"__fault_marker__", "w", encoding="ascii") as marker:
                        marker.write("saved-enum-row-file:directory=false\n")
                state["ready_once"] = True
                gate()
            if hook == "source-enumerated-leaf":
                original_open = api.open
                def open_leaf_after_directory(name, parent=None, **kwargs):
                    try:
                        return original_open(name, parent, **kwargs)
                    except globals_["Unavailable"]:
                        if (state.get("saved_enum_row_file") is True
                                and name == "session-alpha.jsonl"
                                and kwargs.get("directory") is False
                                and "read_data" not in kwargs):
                            with open(r"__fault_marker__", "a", encoding="ascii") as marker:
                                marker.write("replacement-real-leaf-open-failed\n")
                        raise
                api.open = open_leaf_after_directory
            return rows
        api.enumerate = enumerate_directory
        original_rename = api.rename_replace
        def rename_replace(handle, directory, name):
            result = original_rename(handle, directory, name)
            state["published"] = True
            if handle == state["candidate"]:
                state["candidate_published"] = True
            return result
        api.rename_replace = rename_replace
        wanted_kind = "ledger" if fault.startswith("ledger-") else "export"
        if fault.endswith("-candidate-write"):
            original_write = api.kernel.WriteFile
            def write_file(handle, buffer, size, received, overlapped):
                if (state["candidate"] is not None
                        and state["candidate_kind"] == wanted_kind
                        and not state["fault_once"]):
                    state["fault_once"] = True
                    partial = max(1, int(size) // 2)
                    if not original_write(handle, buffer, partial, received, overlapped):
                        return False
                    with open(r"__fault_marker__", "w", encoding="ascii") as marker: marker.write("partial-write")
                    return original_write(ctypes.c_void_p(-1), buffer, size, received, overlapped)
                return original_write(handle, buffer, size, received, overlapped)
            api.kernel.WriteFile = write_file
        elif fault.endswith("-candidate-flush") or fault.endswith("-directory-flush"):
            original_flush = api.nt.NtFlushBuffersFileEx
            def flush_file(handle, flags, buffer, length, io_status):
                candidate_flush = state["candidate"] == handle
                directory_fault = (state["candidate_published"] and state["candidate_kind"] == wanted_kind
                                   and state["candidate_parent"] == handle
                                   and fault.endswith("-directory-flush"))
                candidate_fault = (candidate_flush and state["candidate_kind"] == wanted_kind
                                   and fault.endswith("-candidate-flush"))
                if (candidate_fault or directory_fault) and not state["fault_once"]:
                    state["fault_once"] = True
                    with open(r"__fault_marker__", "w", encoding="ascii") as marker:
                        marker.write("candidate-flush" if candidate_fault else "directory-flush")
                    return original_flush(ctypes.c_void_p(-1), flags, buffer, length, io_status)
                return original_flush(handle, flags, buffer, length, io_status)
            api.nt.NtFlushBuffersFileEx = flush_file
        elif fault.endswith("-rename"):
            original_rename_native = api.nt.NtSetInformationFile
            def set_information(handle, io_status, buffer, length, info_class):
                if (state["candidate"] == handle and state["candidate_kind"] == wanted_kind
                        and int(info_class) == 65 and not state["fault_once"]):
                    state["fault_once"] = True
                    with open(r"__fault_marker__", "w", encoding="ascii") as marker: marker.write("rename")
                    return original_rename_native(ctypes.c_void_p(-1), io_status,
                                                  buffer, length, info_class)
                return original_rename_native(handle, io_status, buffer, length, info_class)
            api.nt.NtSetInformationFile = set_information
        if hook == "candidate-held":
            original_flush_full = api.flush_full
            def flush_full(handle):
                result = original_flush_full(handle)
                if state["candidate"] == handle and not state["ready_once"]:
                    state["ready_once"] = True
                    gate()
                return result
            api.flush_full = flush_full
        if hook == "lock-held":
            def open_with_lock_gate(name, parent=None, **kwargs):
                handle = original_open(name, parent, **kwargs)
                if name == "ledger.lock" and not state["ready_once"]:
                    state["ready_once"] = True
                    gate()
                return handle
            api.open = open_with_lock_gate
        if hook == "volume-reply":
            real_volume = api.kernel.GetVolumeInformationByHandleW
            def unsupported_reply(*args):
                ok = real_volume(*args)
                if ok and state.get("source_volume_query"):
                    args[6].value = "FAT32"
                    with open(r"__fault_marker__", "w", encoding="ascii") as marker: marker.write("real-volume-query-injected-name")
                return ok
            api.kernel.GetVolumeInformationByHandleW = unsupported_reply
            original_open_root = globals_["_windows_open_root"]
            def open_source_root(api_instance, root, user_sid):
                if os.path.normcase(os.path.abspath(str(root))) != os.path.normcase(os.path.abspath(source_root)):
                    return original_open_root(api_instance, root, user_sid)
                state["source_volume_query"] = True
                try:
                    return original_open_root(api_instance, root, user_sid)
                finally:
                    state["source_volume_query"] = False
            globals_["_windows_open_root"] = open_source_root
    def current_user_profile(self): return profile, self.sid
    def read_config(self, received_profile, sid, **kwargs):
        assert received_profile == profile and sid == self.sid
        if (hook == "writable-consent-held" and kwargs.get("writable_cairn") is True
                and not self.state["ready_once"]):
            self.state["ready_once"] = True
            gate()
        return self.api.read_config(received_profile, sid, **kwargs)
    def __getattr__(self, name): return getattr(self.api, name)
globals_["_WindowsConsentAPI"] = SyntheticProfileAPI
if start_ready:
    event(start_ready)
    event(start_release, wait=True)
sys.argv = [meter_path, command, "--json"]
try:
    status = ns["main"]()
except SystemExit as exc:
    status = exc.code if type(exc.code) is int else 1
if done:
    event(done)
    event(done_release, wait=True)
raise SystemExit(status if type(status) is int else 0)
'''


def _native_meter_write_control(setup, mode, ready_name="", release_name=""):
    (setup["git"].parent / "control.txt").write_text(
        f"{mode}\nready={ready_name}\nrelease={release_name}\n",
        encoding="ascii")


def _native_meter_start(setup, command="refresh", *, hook="", fault="",
                        start_ready="", start_release="", ready="",
                        release="", done="", done_release=""):
    import subprocess

    marker = setup["root"] / "__fault_marker__"
    assert all((setup["root"] / name).is_file()
               for name in NATIVE_METER_ROOT_MARKERS)
    if fault or hook == "volume-reply":
        assert marker.is_file(), "native control marker must be precreated before config capture"
        marker.write_text("", encoding="ascii")
    code = _NATIVE_METER_MAIN_WRAPPER.replace("__fault_marker__", str(marker))
    env = os.environ.copy()
    env["PATH"] = str(setup["bin"])
    args = [sys.executable, "-c", code, str(setup["meter"]), str(setup["profile"]),
            str(setup["source"]), str(setup["git"]), command, hook, fault,
            start_ready, start_release, ready, release,
            done, done_release]
    return subprocess.Popen(args, cwd=setup["root"], env=env,
                            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)


def _native_meter_wait(kernel, handle, timeout_ms=30000):
    result = kernel.WaitForSingleObject(handle, timeout_ms)
    assert result == 0, f"owned synchronization event wait returned {result}"


def _native_meter_finish(process, *, timeout=60):
    output, error = process.communicate(timeout=timeout)
    assert process.returncode in (0, 1, 5), error
    rows = [line for line in output.splitlines() if line.strip()]
    assert rows, error
    return json.loads(rows[-1]), output, error


def _native_meter_set(kernel, handle):
    assert kernel.SetEvent(handle), ctypes.get_last_error()


def _native_meter_receipt(receipt, status, reason):
    assert receipt["schema"] == "cairn-meter-refresh/1"
    assert receipt["status"] == status
    assert receipt["reason"] == reason


@WINDOWS_ONLY
@pytest.mark.parametrize("case", ["normal-exit", "nested-job", "forced-timeout"])
def test_windows_native_worker_process_cleanup_contract(
        native_windows_root, native_meter_git_exe, case):
    import time

    mode = "config-hang" if case == "forced-timeout" else "ordinary"
    setup = _native_meter_setup(native_windows_root, native_meter_git_exe,
                                git_mode=mode)
    child_ready = done_pair = done_release_pair = start_pair = start_release_pair = None
    child_pair = assignment_pair = outer_job = None
    process = None
    try:
        child_ready = _native_meter_event()
        done_pair = _native_meter_event()
        done_release_pair = _native_meter_event()
        ck, ch, child_ready_name = child_ready
        dk, dh, done_name = done_pair
        drk, drh, done_release_name = done_release_pair
        _native_meter_write_control(setup, mode, child_ready_name)
        if case == "nested-job":
            start_pair, start_release_pair = _native_meter_event(), _native_meter_event()
            sk, sh, start_name = start_pair
            srk, srh, start_release_name = start_release_pair
            process = _native_meter_start(setup, ready=child_ready_name,
                                          start_ready=start_name,
                                          start_release=start_release_name,
                                          done=done_name,
                                          done_release=done_release_name)
            _native_meter_wait(sk, sh)
            outer_job = _native_meter_job()
            outer_kernel, outer_handle = outer_job
            assignment_pair = _native_meter_assignment_handle(process.pid)
            assignment_kernel, assignment_handle = assignment_pair
            assert outer_kernel.AssignProcessToJobObject(outer_handle, assignment_handle), ctypes.get_last_error()
            assert assignment_kernel.CloseHandle(assignment_handle)
            assignment_pair = None
            _native_meter_set(srk, srh)
        else:
            process = _native_meter_start(setup, ready=child_ready_name,
                                          hook=("origin-config-query-failed"
                                                if case == "forced-timeout" else ""),
                                          done=done_name,
                                          done_release=done_release_name)

        _native_meter_wait(ck, ch)
        child_pid_path = setup["root"] / "__meter_worker_child_pid__"
        deadline = time.monotonic() + 5
        while not child_pid_path.is_file() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert child_pid_path.is_file(), "Meter did not record its direct child handle target"
        child_pair = _native_meter_process_handle(int(child_pid_path.read_text("ascii")))
        child_kernel, child_handle = child_pair
        assert child_kernel.WaitForSingleObject(child_handle, 0) == 0x102

        if case == "forced-timeout":
            deadline = time.monotonic() + 15
            while not (setup["bin"] / "ready.txt").exists() and time.monotonic() < deadline:
                time.sleep(0.05)
            assert (setup["bin"] / "ready.txt").read_text() == "config"
        _native_meter_wait(dk, dh, 30000)
        assert process.poll() is None
        assert child_kernel.WaitForSingleObject(child_handle, 0) == 0x102
        _native_meter_set(drk, drh)
        receipt, _out, _err = _native_meter_finish(process, timeout=30)
        if case == "forced-timeout":
            assert (setup["bin"] / "ready.txt").read_text() == "config"
            assert (setup["root"] / "__fault_marker__").read_text("ascii") == \
                "origin-config-query-failed"
            _native_meter_receipt(receipt, "unavailable", "git_parser_failed")
        else:
            _native_meter_receipt(receipt, "ok", "none")
        assert child_kernel.WaitForSingleObject(child_handle, 30000) == 0
    finally:
        if assignment_pair:
            assignment_pair[0].CloseHandle(assignment_pair[1])
        if process is not None and process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        if child_pair:
            child_kernel, child_handle = child_pair
            if child_kernel.WaitForSingleObject(child_handle, 0) == 0x102:
                child_kernel.TerminateProcess(child_handle, 91)
                child_kernel.WaitForSingleObject(child_handle, 5000)
            child_kernel.CloseHandle(child_handle)
        if outer_job:
            outer_job[0].CloseHandle(outer_job[1])
        for pair in (child_ready, done_pair, done_release_pair, start_pair,
                     start_release_pair):
            if pair:
                pair[0].CloseHandle(pair[1])


@WINDOWS_ONLY
def test_windows_native_meter_lock_lifetime(native_windows_root, native_meter_git_exe):
    setup = _native_meter_setup(native_windows_root, native_meter_git_exe)
    lock_path = setup["profile"] / ".cairn" / "meter" / "ledger.lock"
    _native_meter_successful_refresh(setup)
    for terminate_first in (False, True):
        ready_pair, release_pair = _native_meter_event(), _native_meter_event()
        rk, rh, rn = ready_pair
        lk, lh, ln = release_pair
        process = None
        contender = None
        extra_event_pairs = []
        try:
            lock_before = lock_path.read_bytes()
            if not terminate_first:
                contender_ready, contender_release = _native_meter_event(), _native_meter_event()
                extra_event_pairs.extend((contender_ready, contender_release))
                crk, crh, crn = contender_ready
                clk, clh, cln = contender_release
                holder_ready, holder_release = _native_meter_event(), _native_meter_event()
                extra_event_pairs.extend((holder_ready, holder_release))
                hrk, hrh, hrn = holder_ready
                hlk, hlh, hln = holder_release
                _native_meter_write_control(setup, "ordinary")
                contender = _native_meter_start(
                    setup, hook="writable-consent-held", ready=crn, release=cln)
                _native_meter_wait(crk, crh)
                process = _native_meter_start(
                    setup, hook="lock-held", ready=hrn, release=hln)
                _native_meter_wait(hrk, hrh)
                _native_meter_set(clk, clh)
                receipt, _out, _err = _native_meter_finish(contender)
                _native_meter_receipt(receipt, "unavailable", "ledger_busy")
                _native_meter_set(hlk, hlh)
                receipt, _out, _err = _native_meter_finish(process)
                _native_meter_receipt(receipt, "ok", "none")
                assert lock_path.read_bytes() == lock_before
            else:
                _native_meter_write_control(setup, "ordinary", rn, ln)
                process = _native_meter_start(setup, hook="lock-held", ready=rn, release=ln)
                _native_meter_wait(rk, rh)
                owned_kernel, owned_handle = _native_meter_process_handle(process.pid)
                assert owned_kernel.TerminateProcess(owned_handle, 92), ctypes.get_last_error()
                assert owned_kernel.WaitForSingleObject(owned_handle, 5000) == 0
                owned_kernel.CloseHandle(owned_handle)
                process.wait(timeout=5)
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()
                assert lock_path.read_bytes() == lock_before
                receipt, _out, _err = _native_meter_finish(_native_meter_start(setup))
                _native_meter_receipt(receipt, "ok", "none")
        finally:
            if process is not None and process.poll() is None:
                process.kill()
                process.wait(timeout=5)
            if contender is not None and contender.poll() is None:
                contender.kill()
                contender.wait(timeout=5)
            rk.CloseHandle(rh)
            lk.CloseHandle(lh)
            for pair in extra_event_pairs:
                pair[0].CloseHandle(pair[1])


def _native_meter_successful_refresh(setup):
    _native_meter_write_control(setup, "ordinary")
    receipt, _out, _err = _native_meter_finish(_native_meter_start(setup))
    _native_meter_receipt(receipt, "ok", "none")


def _native_meter_append_valid_update(setup):
    owner = "019a0000-0000-7000-8000-000000000001"
    rows = [row("turn_context", {"turn_id": "turn-b", "root_turn_id": "turn-b",
                                  "cwd": str(setup["project"]),
                                  "model": "gpt-5.3-codex"}),
            codex_direct(owner, owner, "turn-b", "turn-b", "response-b",
                         10, 10, 30)]
    path = setup["source"] / "session-alpha.jsonl"
    with path.open("ab") as stream:
        stream.write(b"".join(encoded(rows)))
    return path, path.read_bytes()


def _native_meter_assert_update(ledger_bytes, source_size, old_event_keys):
    ledger = json.loads(ledger_bytes)
    event_keys = {event["event_key"] for event in ledger["events"]}
    assert old_event_keys <= event_keys
    assert len(event_keys) == len(old_event_keys) + 1
    cursors = [cursor for cursor in ledger["cursors"]
               if cursor["source_alias"] == "source"]
    assert len(cursors) == 1
    assert cursors[0]["offset"] == source_size
    return ledger


def _native_meter_export_event_count(raw):
    export = json.loads(raw)
    return sum(row["events"] for row in export["aggregates"])


def _native_meter_basic_times(path, values=None):
    from ctypes import wintypes as W

    class BASIC_INFO(ctypes.Structure):
        _fields_ = [("creation", ctypes.c_int64), ("access", ctypes.c_int64),
                    ("write", ctypes.c_int64), ("change", ctypes.c_int64),
                    ("attributes", W.DWORD)]

    class IO_STATUS(ctypes.Structure):
        _fields_ = [("status", ctypes.c_void_p), ("information", ctypes.c_size_t)]

    kernel = ctypes.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
    kernel.CreateFileW.argtypes = [W.LPCWSTR, W.DWORD, W.DWORD, ctypes.c_void_p,
                                   W.DWORD, W.DWORD, ctypes.c_void_p]
    kernel.CreateFileW.restype = ctypes.c_void_p
    kernel.GetFileInformationByHandleEx.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                                    ctypes.c_void_p, W.DWORD]
    kernel.GetFileInformationByHandleEx.restype = W.BOOL
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel.CloseHandle.restype = W.BOOL
    ntdll = ctypes.WinDLL("ntdll.dll", winmode=0x800, use_last_error=True)
    ntdll.NtSetInformationFile.argtypes = [ctypes.c_void_p, ctypes.POINTER(IO_STATUS),
                                          ctypes.c_void_p, W.ULONG, ctypes.c_int]
    ntdll.NtSetInformationFile.restype = ctypes.c_long
    handle = kernel.CreateFileW(str(path), 0x100, 1, None, 3, 0x80, None)
    assert handle not in (None, ctypes.c_void_p(-1).value), ctypes.get_last_error()
    try:
        before = BASIC_INFO()
        assert kernel.GetFileInformationByHandleEx(handle, 0, ctypes.byref(before),
                                                    ctypes.sizeof(before)), ctypes.get_last_error()
        old = (before.creation, before.access, before.write, before.change,
               before.attributes)
        desired = old if values is None else tuple(values)
        if values is not None:
            updated = BASIC_INFO(*desired)
            ios = IO_STATUS()
            status = ntdll.NtSetInformationFile(handle, ctypes.byref(ios),
                                                ctypes.byref(updated),
                                                ctypes.sizeof(updated), 4)
            assert status >= 0, f"NtSetInformationFile(FileBasicInformation)={status:#x}"
            observed = BASIC_INFO()
            assert kernel.GetFileInformationByHandleEx(handle, 0, ctypes.byref(observed),
                                                        ctypes.sizeof(observed)), ctypes.get_last_error()
            actual = (observed.creation, observed.access, observed.write,
                      observed.change, observed.attributes)
            assert actual == desired, (actual, desired)
            return actual
        return old
    finally:
        kernel.CloseHandle(handle)


def _native_meter_dacl(path, replacement=None):
    from ctypes import wintypes as W

    advapi = ctypes.WinDLL("advapi32.dll", winmode=0x800, use_last_error=True)
    kernel = ctypes.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
    advapi.GetFileSecurityW.argtypes = [W.LPCWSTR, W.DWORD, ctypes.c_void_p,
                                       W.DWORD, ctypes.POINTER(W.DWORD)]
    advapi.GetFileSecurityW.restype = W.BOOL
    advapi.SetFileSecurityW.argtypes = [W.LPCWSTR, W.DWORD, ctypes.c_void_p]
    advapi.SetFileSecurityW.restype = W.BOOL
    needed = W.DWORD()
    advapi.GetFileSecurityW(str(path), 4, None, 0, ctypes.byref(needed))
    assert ctypes.get_last_error() == 122 and 20 <= needed.value <= 65536
    descriptor = ctypes.create_string_buffer(needed.value)
    assert advapi.GetFileSecurityW(str(path), 4, descriptor, needed.value,
                                   ctypes.byref(needed)), ctypes.get_last_error()
    original = descriptor.raw[:needed.value]
    advapi.GetSecurityDescriptorControl.argtypes = [ctypes.c_void_p,
                                                   ctypes.POINTER(W.WORD),
                                                   ctypes.POINTER(W.DWORD)]
    advapi.GetSecurityDescriptorControl.restype = W.BOOL
    advapi.GetSecurityDescriptorDacl.argtypes = [ctypes.c_void_p,
                                                 ctypes.POINTER(W.BOOL),
                                                 ctypes.POINTER(ctypes.c_void_p),
                                                 ctypes.POINTER(W.BOOL)]
    advapi.GetSecurityDescriptorDacl.restype = W.BOOL
    control, revision = W.WORD(), W.DWORD()
    assert advapi.GetSecurityDescriptorControl(descriptor, ctypes.byref(control),
                                               ctypes.byref(revision)), ctypes.get_last_error()
    present, defaulted, acl = W.BOOL(), W.BOOL(), ctypes.c_void_p()
    assert advapi.GetSecurityDescriptorDacl(descriptor, ctypes.byref(present),
                                            ctypes.byref(acl), ctypes.byref(defaulted)), ctypes.get_last_error()
    acl_bytes = None
    if present.value and acl.value:
        acl_size = ctypes.cast(acl, ctypes.POINTER(W.WORD))[1]
        acl_bytes = ctypes.string_at(acl, acl_size)
    original_state = (int(control.value), bool(present.value), bool(defaulted.value), acl_bytes)
    if replacement is not None:
        # A protected Everyone full-control ACE is a real ACL drift which the
        # source reader must refuse. The saved DACL is restored by the caller.
        empty = ctypes.c_void_p()
        size = W.DWORD()
        advapi.ConvertStringSecurityDescriptorToSecurityDescriptorW.argtypes = [
            W.LPCWSTR, W.DWORD, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(W.DWORD)]
        advapi.ConvertStringSecurityDescriptorToSecurityDescriptorW.restype = W.BOOL
        if not advapi.ConvertStringSecurityDescriptorToSecurityDescriptorW(
                "D:P(A;;FA;;;WD)", 1, ctypes.byref(empty), ctypes.byref(size)):
            raise AssertionError(ctypes.get_last_error())
        try:
            if not advapi.SetFileSecurityW(str(path), 4, empty):
                raise AssertionError(ctypes.get_last_error())
        finally:
            kernel.LocalFree(empty)
    return original, original_state


def _native_meter_restore_dacl(path, saved):
    from ctypes import wintypes as W
    import ctypes

    descriptor, state = saved
    control = state[0]
    protected = bool(control & 0x1000)  # SE_DACL_PROTECTED
    security_information = 4 | (0x80000000 if protected else 0x20000000)
    raw = ctypes.create_string_buffer(descriptor, len(descriptor))
    advapi = ctypes.WinDLL("advapi32.dll", winmode=0x800, use_last_error=True)
    advapi.SetFileSecurityW.argtypes = [W.LPCWSTR, W.DWORD, ctypes.c_void_p]
    advapi.SetFileSecurityW.restype = W.BOOL
    if not advapi.SetFileSecurityW(str(path), security_information, raw):
        raise OSError(ctypes.get_last_error(), "restore saved DACL security information")
    observed = _native_meter_dacl(path)
    assert observed[1][1:] == state[1:], "restored DACL entries or inheritance semantics differ"
    assert (observed[1][0] & 0x1000) == (control & 0x1000), \
        "restored DACL protection semantics differ"


@WINDOWS_ONLY
@pytest.mark.parametrize("case", [
    "append-and-replace-held", "replace-after-enumeration", "creation-time-drift",
    "hardlink", "file-to-directory", "entry-and-parent-reparse",
    "rejected-attribute", "dacl-drift-restored-times", "enumeration-bound",
    "read-bound", "unsupported-filesystem-response",
])
def test_windows_native_meter_source_metadata_mutations(
        native_windows_root, native_meter_git_exe, case):
    import subprocess

    setup = _native_meter_setup(native_windows_root, native_meter_git_exe)
    source = setup["source"] / "session-alpha.jsonl"
    original = source.read_bytes()
    _native_meter_successful_refresh(setup)
    if case == "hardlink":
        os.link(source, setup["source"] / "linked.jsonl")
        receipt, _out, _err = _native_meter_finish(_native_meter_start(setup))
        _native_meter_receipt(receipt, "unavailable", "source_read_unavailable")
        return
    if case == "entry-and-parent-reparse":
        target_dir = native_windows_root / "outside-entry"
        target_dir.mkdir()
        (target_dir / source.name).write_bytes(original)
        junction_entry = setup["source"] / "nested"
        subprocess.run(["cmd", "/c", "mklink", "/J", str(junction_entry), str(target_dir)],
                       capture_output=True, check=True)
        assert os.stat(junction_entry, follow_symlinks=False).st_file_attributes & 0x400
        receipt, _out, _err = _native_meter_finish(_native_meter_start(setup))
        _native_meter_receipt(receipt, "unavailable", "source_read_unavailable")
        junction_entry.rmdir()
        original_root = setup["source"]
        moved = native_windows_root / "approved-source-real"
        original_root.rename(moved)
        target_dir = native_windows_root / "outside-source"
        target_dir.mkdir()
        (target_dir / source.name).write_bytes(original)
        junction = native_windows_root / "approved-source"
        subprocess.run(["cmd", "/c", "mklink", "/J", str(junction), str(target_dir)],
                       capture_output=True, check=True)
        assert os.stat(junction, follow_symlinks=False).st_file_attributes & 0x400
        receipt, _out, _err = _native_meter_finish(
            _native_meter_start(setup, hook="source-root-reparse"))
        _native_meter_receipt(receipt, "unavailable", "unavailable")
        marker = (setup["root"] / "__fault_marker__").read_text("ascii")
        assert "source-root-info-attempted" in marker
        assert "source-root-info-refused" in marker
        junction.rmdir()
        return
    if case == "rejected-attribute":
        api = setup["api"]
        api.kernel.GetFileAttributesW.argtypes = [ctypes.c_wchar_p]
        api.kernel.GetFileAttributesW.restype = ctypes.c_uint32
        api.kernel.SetFileAttributesW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32]
        api.kernel.SetFileAttributesW.restype = ctypes.c_int
        before = api.kernel.GetFileAttributesW(str(source))
        assert before != 0xFFFFFFFF
        changed = before | 0x1000  # FILE_ATTRIBUTE_OFFLINE
        assert api.kernel.SetFileAttributesW(str(source), changed), ctypes.get_last_error()
        assert api.kernel.GetFileAttributesW(str(source)) & 0x1000
        try:
            receipt, _out, _err = _native_meter_finish(_native_meter_start(setup))
            _native_meter_receipt(receipt, "unavailable", "source_read_unavailable")
        finally:
            assert api.kernel.SetFileAttributesW(str(source), before), ctypes.get_last_error()
            assert api.kernel.GetFileAttributesW(str(source)) == before
        return
    if case in {"enumeration-bound", "read-bound"}:
        _native_meter_successful_refresh(setup)
        bound = "MAX_SOURCE_FILES" if case == "enumeration-bound" else "MAX_BATCH_BYTES"
        bounded_root = native_windows_root / ("bounded-enumeration" if
                                               case == "enumeration-bound" else "bounded-read")
        bounded_root.mkdir()
        setup = _native_meter_setup(
            bounded_root, native_meter_git_exe,
            meter_overrides=[(f"{bound} = " + ("10_000" if bound == "MAX_SOURCE_FILES" else "64 * 1024 * 1024"),
                             f"{bound} = 0" if bound == "MAX_SOURCE_FILES" else f"{bound} = 1")])
        receipt, _out, _err = _native_meter_finish(_native_meter_start(setup))
        _native_meter_receipt(receipt, "unavailable", "source_budget_exceeded")
        return

    if case == "unsupported-filesystem-response":
        _native_meter_write_control(setup, "ordinary")
        receipt, _out, _err = _native_meter_finish(
            _native_meter_start(setup, hook="volume-reply"))
        assert (setup["root"] / "__fault_marker__").read_text("ascii") == \
            "real-volume-query-injected-name"
        _native_meter_receipt(receipt, "unavailable", "source_read_unavailable")
        return

    hook = ("source-open-held" if case == "append-and-replace-held" else
            "source-enumerated-leaf" if case == "file-to-directory" else
            "source-enumerated" if case == "replace-after-enumeration" else
            "source-info-held")
    ready_pair, release_pair = _native_meter_event(), _native_meter_event()
    rk, rh, rn = ready_pair
    lk, lh, ln = release_pair
    process = None
    saved_dacl = None
    old_times = None
    dacl_times = None
    replacement = None
    try:
        if case in {"append-and-replace-held", "replace-after-enumeration"}:
            replacement = native_windows_root / "replacement.jsonl"
            replacement.write_bytes(original + b"{}\n")
        _native_meter_write_control(setup, "ordinary", rn, ln)
        process = _native_meter_start(setup, hook=hook, ready=rn, release=ln)
        _native_meter_wait(rk, rh)
        if case == "append-and-replace-held":
            with pytest.raises(OSError):
                with source.open("ab") as stream:
                    stream.write(b"{}\n")
            replacement = native_windows_root / "replacement.jsonl"
            replacement.write_bytes(original + b"{}\n")
            with pytest.raises(OSError):
                os.replace(replacement, source)
            assert source.read_bytes() == original
            _native_meter_set(lk, lh)
            receipt, _out, _err = _native_meter_finish(process)
            _native_meter_receipt(receipt, "ok", "none")
            return
        if case == "replace-after-enumeration":
            with pytest.raises(OSError) as denied:
                os.replace(replacement, source)
            assert denied.value.winerror == 32, denied.value.winerror
            assert source.read_bytes() == original
            assert replacement.read_bytes() == original + b"{}\n"
            _native_meter_set(lk, lh)
            receipt, _out, _err = _native_meter_finish(process)
            _native_meter_receipt(receipt, "ok", "none")
            return
        elif case == "file-to-directory":
            source.unlink()
            source.mkdir()
            reason = "unavailable"
        elif case == "creation-time-drift":
            old_times = _native_meter_basic_times(source)
            changed = list(old_times)
            changed[0] += 10_000_000
            _native_meter_basic_times(source, changed)
            reason = "source_changed"
        elif case == "dacl-drift-restored-times":
            dacl_times = old_times = _native_meter_basic_times(source)
            saved_dacl = _native_meter_dacl(source, replacement=True)
            assert _native_meter_dacl(source)[1][1:] != saved_dacl[1][1:]
            reason = "unavailable"
        _native_meter_set(lk, lh)
        receipt, _out, _err = _native_meter_finish(process)
        _native_meter_receipt(receipt, "unavailable", reason)
        if case == "file-to-directory":
            marker = (setup["root"] / "__fault_marker__").read_text("ascii")
            assert "saved-enum-row-file" in marker
            assert "replacement-real-leaf-open-failed" in marker
            assert source.is_dir()
        if case == "dacl-drift-restored-times":
            marker = (setup["root"] / "__fault_marker__").read_text("ascii")
            assert marker == "bad-acl-recheck"
    finally:
        primary_error = sys.exc_info()[1]
        cleanup_errors = []
        if process is not None and process.poll() is None:
            try:
                process.kill()
                process.wait(timeout=5)
            except BaseException as exc:
                cleanup_errors.append(exc)
        process_stopped = process is None or process.poll() is not None
        if saved_dacl is not None and process_stopped:
            try:
                _native_meter_restore_dacl(source, saved_dacl)
            except BaseException as exc:
                cleanup_errors.append(exc)
            try:
                assert _native_meter_basic_times(source, dacl_times) == dacl_times
            except BaseException as exc:
                cleanup_errors.append(exc)
        if old_times is not None and process_stopped:
            try:
                assert _native_meter_basic_times(source, old_times) == old_times
            except BaseException as exc:
                cleanup_errors.append(exc)
        rk.CloseHandle(rh)
        lk.CloseHandle(lh)
        if cleanup_errors:
            if primary_error is not None:
                for error in cleanup_errors:
                    primary_error.add_note(f"cleanup failure: {error!r}")
            else:
                raise cleanup_errors[0]


@WINDOWS_ONLY
def test_windows_native_meter_candidate_sharing_contract(
        native_windows_root, native_meter_git_exe):
    from ctypes import wintypes as W

    setup = _native_meter_setup(native_windows_root, native_meter_git_exe)
    _native_meter_successful_refresh(setup)
    ready_pair, release_pair = _native_meter_event(), _native_meter_event()
    rk, rh, rn = ready_pair
    lk, lh, ln = release_pair
    kernel = ctypes.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
    kernel.CreateFileW.argtypes = [W.LPCWSTR, W.DWORD, W.DWORD, ctypes.c_void_p,
                                   W.DWORD, W.DWORD, ctypes.c_void_p]
    kernel.CreateFileW.restype = ctypes.c_void_p
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel.CloseHandle.restype = W.BOOL
    kernel.ReadFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p, W.DWORD,
                                ctypes.POINTER(W.DWORD), ctypes.c_void_p]
    kernel.ReadFile.restype = W.BOOL
    kernel.SetFilePointerEx.argtypes = [ctypes.c_void_p, ctypes.c_longlong,
                                       ctypes.c_void_p, W.DWORD]
    kernel.SetFilePointerEx.restype = W.BOOL

    def read_reader():
        chunks = []
        while True:
            buffer = ctypes.create_string_buffer(65536)
            received = W.DWORD()
            assert kernel.ReadFile(reader, buffer, len(buffer), ctypes.byref(received), None), ctypes.get_last_error()
            if not received.value:
                break
            chunks.append(buffer.raw[:received.value])
            assert sum(map(len, chunks)) <= 8 * 1024 * 1024
        data = b"".join(chunks)
        assert json.loads(data)
        return data

    process = None
    reader = None
    try:
        _native_meter_write_control(setup, "ordinary", rn, ln)
        process = _native_meter_start(setup, hook="candidate-held", ready=rn,
                                      release=ln)
        _native_meter_wait(rk, rh)
        candidate_name = (setup["root"] / "__candidate_name__").read_text("ascii")
        candidate = setup["profile"] / ".cairn" / "meter" / candidate_name
        assert candidate.is_file()
        reader = kernel.CreateFileW(str(candidate), 0x80000000, 7, None, 3, 0x80, None)
        assert reader not in (None, ctypes.c_void_p(-1).value), ctypes.get_last_error()
        before = read_reader()
        for access in (0x40000000, 0x00010000):
            ctypes.set_last_error(0)
            denied = kernel.CreateFileW(str(candidate), access, 7, None, 3, 0x80, None)
            assert denied in (None, ctypes.c_void_p(-1).value)
            assert ctypes.get_last_error() == 32, ctypes.get_last_error()
        _native_meter_set(lk, lh)
        receipt, _out, _err = _native_meter_finish(process)
        _native_meter_receipt(receipt, "ok", "none")
        published = setup["profile"] / ".cairn" / "meter" / "ledger.json"
        assert published.is_file()
        position = ctypes.c_longlong()
        assert kernel.SetFilePointerEx(reader, 0, ctypes.byref(position), 0), ctypes.get_last_error()
        assert read_reader() == before
        assert kernel.CloseHandle(reader)
        reader = None
    finally:
        if reader not in (None, ctypes.c_void_p(-1).value):
            kernel.CloseHandle(reader)
        if process is not None and process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        rk.CloseHandle(rh)
        lk.CloseHandle(lh)


@WINDOWS_ONLY
@pytest.mark.parametrize("fault", [
    "ledger-candidate-write", "ledger-candidate-flush", "ledger-rename",
    "ledger-old-reopen", "ledger-directory-flush", "ledger-target-reopen",
    "export-candidate-write", "export-candidate-flush", "export-rename",
    "export-old-reopen", "export-directory-flush", "export-target-reopen",
])
def test_windows_native_meter_publication_fault_boundaries(
        native_windows_root, native_meter_git_exe, fault):
    setup = _native_meter_setup(native_windows_root, native_meter_git_exe)
    _native_meter_write_control(setup, "ordinary")
    baseline, _out, _err = _native_meter_finish(_native_meter_start(setup))
    _native_meter_receipt(baseline, "ok", "none")
    ledger_path = setup["profile"] / ".cairn" / "meter" / "ledger.json"
    export_path = setup["project"] / "dev" / "measurement" / "meter.json"
    target = ledger_path if fault.startswith("ledger-") else export_path
    old_ledger_bytes = ledger_path.read_bytes()
    old_export_bytes = export_path.read_bytes()
    old_ledger = json.loads(old_ledger_bytes)
    old_event_keys = {event["event_key"] for event in old_ledger["events"]}
    old_source_offset = next(cursor["offset"] for cursor in old_ledger["cursors"]
                             if cursor["source_alias"] == "source")
    old_export_count = _native_meter_export_event_count(old_export_bytes)
    source_path, updated_source = _native_meter_append_valid_update(setup)
    assert len(updated_source) > old_source_offset
    (setup["root"] / "__fault_marker__").write_text("", encoding="ascii")
    _native_meter_write_control(setup, "ordinary")
    receipt, _out, _err = _native_meter_finish(_native_meter_start(setup, fault=fault))
    marker = setup["root"] / "__fault_marker__"
    expected_marker = {"candidate-write": "partial-write",
                       "candidate-flush": "candidate-flush",
                       "rename": "rename", "old-reopen": "old-reopen",
                       "directory-flush": "directory-flush",
                       "target-reopen": "target-reopen"}[fault.split("-", 1)[1]]
    assert marker.read_text("ascii") == expected_marker, fault
    if fault.endswith(("directory-flush", "target-reopen")):
        reason = ("ledger_durability_uncertain" if fault.startswith("ledger-")
                  else "project_export_uncertain")
        _native_meter_receipt(receipt, "unavailable", reason)
        assert target.is_file() and target.read_bytes() != (
            old_ledger_bytes if target == ledger_path else old_export_bytes)
    else:
        expected = ("unavailable" if fault.endswith("-old-reopen") else
                    "ledger_write_failed")
        _native_meter_receipt(receipt, "unavailable", expected)
    assert source_path.read_bytes() == updated_source
    if fault.startswith("ledger-") and not fault.endswith(("directory-flush", "target-reopen")):
        assert ledger_path.read_bytes() == old_ledger_bytes
        assert export_path.read_bytes() == old_export_bytes
    else:
        new_ledger = _native_meter_assert_update(
            ledger_path.read_bytes(), len(updated_source), old_event_keys)
        assert len(new_ledger["events"]) == len(old_event_keys) + 1
        if fault.startswith("ledger-"):
            assert export_path.read_bytes() == old_export_bytes
        elif fault.endswith(("directory-flush", "target-reopen")):
            assert _native_meter_export_event_count(export_path.read_bytes()) == old_export_count + 1
        else:
            assert export_path.read_bytes() == old_export_bytes
    assert not list((setup["profile"] / ".cairn" / "meter").glob(".ledger-*.tmp"))
    assert not list((setup["project"] / "dev" / "measurement").glob(".meter-*.tmp"))


@pytest.fixture
def native_windows_root():
    import tempfile

    # The shared pytest-of-* parent is outside this fixture's authority.
    # Keep the native private-profile control under a root this test owns.
    with tempfile.TemporaryDirectory(prefix="cairn-meter-native-") as root:
        yield Path(root)


class SyntheticProfileWindowsConsent:
    """Use real Windows APIs, but direct the config read into a disposable profile."""

    def __init__(self, api, profile, sid):
        self.api, self.profile, self.sid = api, str(profile), sid

    def current_user_profile(self):
        return self.profile, self.sid

    def read_config(self, profile, sid):
        assert profile == self.profile and sid == self.sid
        return self.api.read_config(profile, sid)


def native_windows_status(synthetic_root, content=None):
    import subprocess

    api = meter._WindowsConsentAPI()
    # Resolve the actual token profile only for account metadata. Never ask the
    # reader to inspect that profile; all filesystem reads use this temp tree.
    _actual_profile, sid = api.current_user_profile()
    sid_buffer = api.C.create_string_buffer(sid)
    sid_text_ptr = api.W.LPWSTR()
    if not api.advapi.ConvertSidToStringSidW(api.C.cast(sid_buffer, api.C.c_void_p),
                                             api.C.byref(sid_text_ptr)):
        raise AssertionError("could not prepare the disposable Windows ACL fixture")
    try:
        sid_text = api.C.wstring_at(sid_text_ptr)
    finally:
        api.kernel.LocalFree(api.C.cast(sid_text_ptr, api.C.c_void_p))
    # Give only this separately allocated disposable root a private ACL so the
    # reader can distinguish the synthetic profile from inherited host ACLs.
    acl = subprocess.run([
        "icacls", str(synthetic_root), "/inheritance:r", "/grant:r",
        f"*{sid_text}:(OI)(CI)F", "*S-1-5-18:(OI)(CI)F",
        "*S-1-5-32-544:(OI)(CI)F",
    ], capture_output=True, check=False)
    assert acl.returncode == 0, "could not prepare the disposable Windows ACL fixture"

    def set_synthetic_owner(path):
        owner = subprocess.run(["icacls", str(path), "/setowner", f"*{sid_text}"],
                               capture_output=True, check=False)
        assert owner.returncode == 0, "could not set the disposable Windows fixture owner"
        owner_rights = subprocess.run(["icacls", str(path), "/remove", "*S-1-3-4"],
                                      capture_output=True, check=False)
        assert owner_rights.returncode == 0, "could not prepare the disposable Windows ACL fixture"

    set_synthetic_owner(synthetic_root)
    profile = synthetic_root / "synthetic-profile"
    profile.mkdir()
    set_synthetic_owner(profile)
    if content is not None:
        cairn = profile / ".cairn"
        cairn.mkdir()
        set_synthetic_owner(cairn)
        config = cairn / "meter.json"
        config.write_bytes(content)
        set_synthetic_owner(config)
    wrapped = SyntheticProfileWindowsConsent(api, profile, sid)
    return api, wrapped, profile


def synthetic_read_config_api(content, *, changed_field=None, short_read=False):
    """Exercise the production read_config method with synthetic API calls."""
    import ctypes
    word = ctypes.c_uint32

    class Kernel:
        def __init__(self):
            self.offset = 0

        def QueryDosDeviceW(self, drive, buffer, size):
            buffer.value = r"\Device\HarddiskVolume7"
            return 1

        def GetVolumeInformationByHandleW(self, handle, volume, volume_size,
                                          serial, max_component, flags, fs_name,
                                          fs_name_size):
            fs_name.value = "NTFS"
            return 1

        def ReadFile(self, handle, buffer, size, received, overlapped):
            count = max(0, len(content) - self.offset)
            if short_read:
                count = min(count, max(0, len(content) - 1 - self.offset))
            count = min(count, size)
            if count:
                ctypes.memmove(buffer, content[self.offset:self.offset + count], count)
                self.offset += count
            ctypes.cast(received, ctypes.POINTER(word)).contents.value = count
            return 1

    api = object.__new__(meter._WindowsConsentAPI)
    api.C, api.W, api.kernel = ctypes, SimpleNamespace(DWORD=word), Kernel()
    api.handles_closed = []
    api.open_calls = []
    open_calls = 0

    def open_handle(name, parent=None, **kwargs):
        nonlocal open_calls
        api.open_calls.append((name, parent, dict(kwargs)))
        if parent is None:
            return 1
        if name == "profile":
            return 2 if open_calls == 0 else 5
        if name == ".cairn":
            return 3 if open_calls == 0 else 6
        if name == "meter.json":
            open_calls += 1
            if open_calls == 1:
                return 4
            api.kernel.offset = 0
            return 7
        raise AssertionError("unexpected synthetic path")

    api.open = open_handle
    api.close = lambda handle: api.handles_closed.append(handle)
    api.check_acl = lambda handle, sid, role: None
    seen_config = 0
    info_values = {
        "identity": (7, 42), "size": len(content), "directory": False,
        "links": 1, "created": 11, "accessed": 21, "written": 31, "changed": 41,
    }

    def info(handle):
        nonlocal seen_config
        if handle == 1:
            return {"directory": True}
        seen_config += 1
        value = dict(info_values)
        if seen_config > 1:
            value["accessed"] += 1
            if changed_field is not None:
                if changed_field == "directory":
                    value[changed_field] = True
                elif changed_field == "identity":
                    value[changed_field] = (7, 43)
                else:
                    value[changed_field] += 1
        return value

    api.info = info
    return api


def synthetic_native_open_api(*, directory_result=True):
    import ctypes

    class US(ctypes.Structure):
        _fields_ = [("Length", ctypes.c_ushort), ("MaximumLength", ctypes.c_ushort),
                    ("Buffer", ctypes.c_void_p)]

    class OA(ctypes.Structure):
        _fields_ = [("Length", ctypes.c_uint32), ("RootDirectory", ctypes.c_void_p),
                    ("ObjectName", ctypes.POINTER(US)), ("Attributes", ctypes.c_uint32),
                    ("SecurityDescriptor", ctypes.c_void_p),
                    ("SecurityQualityOfService", ctypes.c_void_p)]

    class IOS(ctypes.Structure):
        class U(ctypes.Union):
            _fields_ = [("Status", ctypes.c_int32), ("Pointer", ctypes.c_void_p)]
        _fields_ = [("u", U), ("Information", ctypes.c_size_t)]

    api = object.__new__(meter._WindowsConsentAPI)
    api.C, api.W = ctypes, SimpleNamespace(USHORT=ctypes.c_ushort,
                                            ULONG=ctypes.c_uint32)
    api.US, api.OA, api.IOS = US, OA, IOS
    calls = []

    class Nt:
        def NtCreateFile(self, out_ptr, access, oa_ptr, ios_ptr, _allocation,
                         _attributes, share, disposition, options, _ea, _ea_size):
            oa = ctypes.cast(oa_ptr, ctypes.POINTER(OA)).contents
            us = oa.ObjectName.contents
            calls.append({
                "operation": "open", "access": int(access), "share": int(share),
                "disposition": int(disposition), "options": int(options),
                "name": ctypes.wstring_at(us.Buffer, us.Length // 2),
                "parent_is_null": oa.RootDirectory is None,
            })
            ctypes.cast(out_ptr, ctypes.POINTER(ctypes.c_void_p)).contents.value = 73
            return 0

    api.nt = Nt()

    def info(handle):
        calls.append({"operation": "info", "handle": handle})
        return {"directory": directory_result}

    api.info = info
    api.close = lambda handle: calls.append({"operation": "close", "handle": handle})
    return api, calls


def test_windows_existing_directory_open_omits_directory_flag_and_validates_immediately():
    api, calls = synthetic_native_open_api()
    root_name = "\\Device\\HarddiskVolume7\\"
    handle = api.open(root_name, directory=True)
    assert handle == 73
    assert calls == [
        {"operation": "open", "access": 0x00120081, "share": 1,
         "disposition": 1, "options": 0x00600020,
         "name": root_name, "parent_is_null": True},
        {"operation": "info", "handle": 73},
    ]


@pytest.mark.parametrize("directory_result", [False, "info-error"],
                         ids=["wrong-type", "info-failure"])
def test_windows_existing_directory_open_closes_unvalidated_handle(directory_result):
    api, calls = synthetic_native_open_api(directory_result=directory_result)
    if directory_result == "info-error":
        def failed_info(handle):
            calls.append({"operation": "info", "handle": handle})
            raise OSError("synthetic info failure")
        api.info = failed_info
    with pytest.raises(meter.Unavailable):
        api.open("synthetic-root", directory=True)
    assert [call["operation"] for call in calls] == ["open", "info", "close"]
    assert calls[-1] == {"operation": "close", "handle": 73}


def test_windows_directory_creation_and_file_open_masks_are_scoped():
    api, calls = synthetic_native_open_api()
    api.open("created-dir", directory=True, read_data=True, write_data=True,
             disposition=2, write_through=True)
    api.open("existing-file", read_data=True)
    assert [(call["access"], call["options"]) for call in calls] == [
        (0x00120083, 0x00200023),
        (0x00120081, 0x00600060),
    ]
    assert all(call["operation"] == "open" for call in calls)


def native_windows_directory_open_controls(api, profile, sid):
    import re

    drive, parts = meter._windows_absolute_parts(str(profile))
    targets = api.C.create_unicode_buffer(32768)
    assert api.kernel.QueryDosDeviceW(drive, targets, len(targets))
    device = targets.value
    assert re.fullmatch(r"\\Device\\HarddiskVolume[0-9]+", device)
    parent_handles = []
    owned_handles = {}
    try:
        current = api.open(device + "\\", directory=True)
        parent_handles.append(current)
        api.check_acl(current, sid, "ancestor")
        for index, part in enumerate(parts):
            current = api.open(part, current, directory=True)
            parent_handles.append(current)
            role = "profile" if index == len(parts) - 1 else "ancestor"
            api.check_acl(current, sid, role)
        parent = current

        def create(name, *, directory):
            descriptor = api._private_security_descriptor(sid, directory=directory)
            try:
                return api.open(name, parent, directory=directory,
                                read_data=True, write_data=True, delete=True,
                                share=1, disposition=2, write_through=True,
                                security_descriptor=descriptor)
            finally:
                api.kernel.LocalFree(descriptor)

        directory_name = ".meter-native-directory-probe"
        directory_handle = create(directory_name, directory=True)
        owned_handles[directory_name] = directory_handle
        created = api.info(directory_handle)
        api.check_acl(directory_handle, sid, "meter")
        assert created["directory"] and created["links"] == 1
        api.close(directory_handle)
        del owned_handles[directory_name]

        existing = api.open(directory_name, parent, directory=True, delete=True)
        try:
            existing_info = api.info(existing)
            api.check_acl(existing, sid, "meter")
            assert meter._windows_stable_info(existing_info) == meter._windows_stable_info(created)
        finally:
            api.close(existing)

        with pytest.raises(meter.Unavailable):
            create(directory_name, directory=True)

        cleanup_directory = api.open(directory_name, parent, directory=True, delete=True)
        try:
            after_collision = api.info(cleanup_directory)
            api.check_acl(cleanup_directory, sid, "meter")
            assert meter._windows_stable_info(after_collision) == meter._windows_stable_info(created)
            api.delete_by_handle(cleanup_directory)
        finally:
            api.close(cleanup_directory)

        file_name = ".meter-native-file-probe"
        file_handle = create(file_name, directory=False)
        owned_handles[file_name] = file_handle
        file_info = api.info(file_handle)
        api.check_acl(file_handle, sid, "ledger")
        assert not file_info["directory"] and file_info["links"] == 1
        api.close(file_handle)
        del owned_handles[file_name]

        with pytest.raises(meter.Unavailable):
            api.open(file_name, parent, directory=True)

        cleanup_file = api.open(file_name, parent, read_data=True, delete=True)
        try:
            after_refusal = api.info(cleanup_file)
            api.check_acl(cleanup_file, sid, "ledger")
            assert meter._windows_stable_info(after_refusal) == meter._windows_stable_info(file_info)
            api.delete_by_handle(cleanup_file)
        finally:
            api.close(cleanup_file)
    finally:
        for handle in reversed(tuple(owned_handles.values())):
            try:
                api.delete_by_handle(handle)
            except BaseException:
                pass
            api.close(handle)
        for handle in reversed(parent_handles):
            api.close(handle)


def test_windows_read_config_tolerates_accessed_only_drift():
    content = b'{"version":1,"enabled":false}'
    api = synthetic_read_config_api(content)
    assert api.read_config("C:\\profile", b"synthetic-sid") == content
    assert api.handles_closed == [4, 3, 2, 1]


def test_verified_git_helper_compiles_admitted_bytes_without_inherited_flags(monkeypatch):
    import builtins
    import hashlib

    raw = b"def bind_verified_source(raw, digest):\n    pass\n"
    calls = []
    monkeypatch.setattr(meter, "_VERIFIED_GIT_HELPER", None)
    monkeypatch.setattr(meter, "_git_helper_source", lambda: raw)
    monkeypatch.setattr(meter, "SAFE_GIT_SOURCE_SHA256", hashlib.sha256(raw).hexdigest())

    def record_compile(source, *args, **kwargs):
        calls.append((source, kwargs))
        return builtins.compile(source, *args, **kwargs)

    monkeypatch.setattr(meter, "compile", record_compile, raising=False)
    helper = meter._verified_git_helper()
    assert helper is not None
    assert calls == [(raw, {"dont_inherit": True})]
    monkeypatch.setattr(meter, "_git_helper_source", lambda: b"substituted")
    assert meter._verified_git_helper() is helper
    monkeypatch.setattr(meter, "_VERIFIED_GIT_HELPER", None)
    assert meter._verified_git_helper() is None
    assert len(calls) == 1


def test_windows_read_config_can_retain_and_revalidate_consent_handles():
    content = b'{"version":1,"enabled":false}'
    api = synthetic_read_config_api(content)
    raw, held = api.read_config("C:\\profile", b"synthetic-sid", retain_handles=True)
    assert raw == content
    held.revalidate()
    held.close()
    assert set(api.handles_closed) == {1, 2, 3, 4, 5, 6, 7}


def test_windows_writable_consent_reopen_changes_only_cairn_access():
    content = b'{"version":1,"enabled":false}'
    api = synthetic_read_config_api(content)
    raw, held = api.read_config("C:\\profile", b"synthetic-sid",
                                retain_handles=True, writable_cairn=True)
    assert raw == content
    initial = api.open_calls[:4]
    cairn_call = next(call for call in initial if call[0] == ".cairn")
    assert cairn_call[2] == {
        "directory": True, "write_data": True, "write_through": True, "share": 3}
    assert next(call for call in initial if call[0] == "profile")[2] == {
        "directory": True}
    assert next(call for call in initial if call[0] == "meter.json")[2] == {
        "read_data": True}
    held.revalidate()
    named_cairn = [call for call in api.open_calls[4:] if call[0] == ".cairn"]
    assert len(named_cairn) == 1
    assert named_cairn[0][2] == {"directory": True, "read_data": False, "share": 3}
    named_profile = [call for call in api.open_calls[4:] if call[0] == "profile"]
    assert named_profile[0][2] == {"directory": True, "read_data": False}
    held.close()


@pytest.mark.parametrize("field", ["size", "written", "changed", "mtime_ns", "ctime_ns"])
def test_windows_owned_cairn_creation_allows_only_namespace_metadata(field):
    content = b'{"version":1,"enabled":false}'
    api = synthetic_read_config_api(content)
    raw, held = api.read_config("C:\\profile", b"synthetic-sid",
                                retain_handles=True, writable_cairn=True)
    assert raw == content
    cairn = next(link[2] for link in held.links if link[3] == "cairn")
    original_info = api.info
    original_acl = api.check_acl
    checked_roles = []

    def record_acl(handle, sid, role):
        checked_roles.append(role)
        original_acl(handle, sid, role)

    api.check_acl = record_acl

    def changed_info(handle):
        info = original_info(handle)
        if handle == cairn:
            info[field] = info.get(field, 0) + 1
        return info

    api.info = changed_info
    with pytest.raises(meter.Unavailable, match="source_changed"):
        held.revalidate()
    held.revalidate(allow_owned_cairn_metadata=True)
    assert checked_roles.count("cairn") >= 3
    assert checked_roles.count("config") >= 2
    held.close()


@pytest.mark.parametrize("field", ["written", "changed", "mtime_ns", "ctime_ns"])
def test_windows_owned_cairn_metadata_exception_keeps_other_roles_strict(field):
    content = b'{"version":1,"enabled":false}'
    api = synthetic_read_config_api(content)
    _raw, held = api.read_config("C:\\profile", b"synthetic-sid",
                                 retain_handles=True, writable_cairn=True)
    profile = next(link[2] for link in held.links if link[3] == "profile")
    original_info = api.info

    def changed_info(handle):
        info = original_info(handle)
        if handle == profile:
            info[field] = info.get(field, 0) + 1
        return info

    api.info = changed_info
    with pytest.raises(meter.Unavailable, match="source_changed"):
        held.revalidate(allow_owned_cairn_metadata=True)
    held.close()


@pytest.mark.parametrize("field", ["identity", "directory", "links", "created"])
def test_windows_owned_cairn_metadata_exception_keeps_identity_proofs(field):
    content = b'{"version":1,"enabled":false}'
    api = synthetic_read_config_api(content)
    _raw, held = api.read_config("C:\\profile", b"synthetic-sid",
                                 retain_handles=True, writable_cairn=True)
    cairn = next(link[2] for link in held.links if link[3] == "cairn")
    original_info = api.info

    def changed_info(handle):
        info = original_info(handle)
        if handle == cairn:
            if field == "identity":
                info[field] = (7, 99)
            elif field == "directory":
                info[field] = not info[field]
            elif field == "links":
                info[field] = 2
            else:
                info[field] += 1
        return info

    api.info = changed_info
    with pytest.raises(meter.Unavailable, match="source_changed"):
        held.revalidate(allow_owned_cairn_metadata=True)
    held.close()


def test_windows_owned_cairn_metadata_exception_keeps_acl_checks():
    content = b'{"version":1,"enabled":false}'
    api = synthetic_read_config_api(content)
    _raw, held = api.read_config("C:\\profile", b"synthetic-sid",
                                 retain_handles=True, writable_cairn=True)
    original_acl = api.check_acl
    calls = []

    def changed_acl(handle, sid, role):
        calls.append(role)
        if role == "cairn":
            raise meter.Unavailable("source_changed")
        return original_acl(handle, sid, role)

    api.check_acl = changed_acl
    with pytest.raises(meter.Unavailable, match="source_changed"):
        held.revalidate(allow_owned_cairn_metadata=True)
    assert calls[-1] == "cairn"
    held.close()


def test_windows_owned_cairn_metadata_exception_keeps_exact_consent_bytes():
    content = b'{"version":1,"enabled":false}'
    api = synthetic_read_config_api(content)
    _raw, held = api.read_config("C:\\profile", b"synthetic-sid",
                                 retain_handles=True, writable_cairn=True)
    original_read = api.read_bounded

    def changed_config(handle, limit):
        if handle == 7:
            return content + b" ", api.info(handle)
        return original_read(handle, limit)

    api.read_bounded = changed_config
    with pytest.raises(meter.Unavailable, match="source_changed"):
        held.revalidate(allow_owned_cairn_metadata=True)
    held.close()


def test_windows_refresh_reopens_enabled_consent_before_private_io(monkeypatch):
    initial_raw = b'{"version":1,"enabled":true,"sources":[],"projects":[]}'

    class Held:
        def __init__(self, tag):
            self.raw = initial_raw
            self.links = [(None, ".cairn", tag, "cairn", True)]
            self.closed = False

        def close(self):
            self.closed = True

    class Api:
        def __init__(self, second):
            self.first = Held("first-cairn")
            self.second = Held("second-cairn")
            self.second_result = second
            self.calls = []

        def read_config(self, _profile, _sid, *, retain_handles, writable_cairn=False):
            self.calls.append((retain_handles, writable_cairn,
                               self.first.closed, self.second.closed))
            assert retain_handles
            if not writable_cairn:
                return initial_raw, self.first
            if self.second_result == "missing":
                return None
            if self.second_result == "disabled":
                return b'{"version":1,"enabled":false,"sources":[],"projects":[]}', self.second
            if self.second_result == "changed":
                return initial_raw + b" ", self.second
            return initial_raw, self.second

    for outcome in ("missing", "disabled", "changed"):
        api = Api(outcome)
        monkeypatch.setattr(meter, "_scan_approved_sources",
                            lambda *_args, **_kwargs: pytest.fail("source scan preceded consent re-read"))
        monkeypatch.setattr(meter, "_windows_atomic_replace",
                            lambda *_args, **_kwargs: pytest.fail("ledger write preceded consent re-read"))
        result = meter._refresh_ledger_windows("C:\\synthetic\\profile", api, b"sid",
                                               opened=(initial_raw, api.first))
        assert result == {"status": "unavailable", "reason": "source_changed",
                          "coverage": "unknown"}
        assert api.calls == [(True, True, True, False)]
        assert api.first.closed
        if outcome != "missing":
            assert api.second.closed


def test_windows_refresh_flush_failure_closes_both_consent_chains(monkeypatch):
    raw = b'{"version":1,"enabled":true,"sources":[],"projects":[]}'

    class Held:
        def __init__(self, tag):
            self.raw = raw
            self.links = [(None, ".cairn", tag, "cairn", True)]
            self.closed = False

        def close(self):
            self.closed = True

    class Api:
        def __init__(self):
            self.first, self.second = Held("initial"), Held("writable")
            self.calls = []

        def read_config(self, _profile, _sid, *, retain_handles, writable_cairn=False):
            self.calls.append((writable_cairn, self.first.closed))
            return (raw, self.second) if writable_cairn else (raw, self.first)

    api = Api()

    def fail_flush(_api, held, _cairn, config_raw, _sid, _candidate):
        assert held is api.second and config_raw == raw
        raise meter.Unavailable("ledger_write_failed")

    monkeypatch.setattr(meter, "_windows_atomic_replace", fail_flush)
    result = meter._refresh_ledger_windows("C:\\synthetic\\profile", api, b"sid",
                                           opened=(raw, api.first))
    assert result == {"status": "unavailable", "reason": "ledger_write_failed",
                      "coverage": "unknown"}
    assert api.calls == [(True, True)]
    assert api.first.closed and api.second.closed


@pytest.mark.parametrize("field", [
    "identity", "size", "directory", "links", "created", "written", "changed",
])
def test_windows_read_config_refuses_stable_metadata_changes(field):
    api = synthetic_read_config_api(
        b'{"version":1,"enabled":false}', changed_field=field)
    with pytest.raises(meter.Unavailable):
        api.read_config("C:\\profile", b"synthetic-sid")


def test_windows_read_config_refuses_short_file_read():
    content = b'{"version":1,"enabled":false}'
    api = synthetic_read_config_api(content, short_read=True)
    with pytest.raises(meter.Unavailable):
        api.read_config("C:\\profile", b"synthetic-sid")


def _windows_directory_record(name, *, file_id=1, attrs=0x80, next_offset=0):
    header = struct.Struct("<II6qIIIbx24s2xq")
    encoded_name = name.encode("utf-16-le")
    raw = bytearray(64 * 1024)
    header.pack_into(raw, 0, next_offset, 0, 0, 0, 0, 0, 12, 16, attrs,
                     len(encoded_name), 0, 0, b"\0" * 24, file_id)
    raw[header.size:header.size + len(encoded_name)] = encoded_name
    return raw


def test_windows_directory_decoder_accepts_unsigned_file_ids_and_dot_entries():
    first = _windows_directory_record(".", next_offset=120)
    second = _windows_directory_record("session.jsonl", file_id=-1)
    first[120:] = second[:len(first) - 120]
    rows = meter._decode_windows_directory_entries(bytes(first))
    assert rows[0]["name"] == "."
    assert rows[1]["file_id"] == (1 << 64) - 1
    assert rows[1]["size"] == 12


def test_ledger_cursor_preserves_full_unsigned_windows_file_identity():
    config = meter.validate_config_bytes(json.dumps({
        "version": 1, "enabled": False,
        "sources": [{"alias": "source", "tool": "codex", "root": "/synthetic/source"}],
        "projects": [],
    }).encode())
    cursor = {"source_alias": "source", "file_key": "a" * 64,
              "dev": (1 << 32) - 1, "ino": (1 << 64) - 1,
              "generation": 1, "offset": 0, "line": 0,
              "size": 0, "mtime_ns": 0, "ctime_ns": 0}
    ledger = meter._new_ledger(meter._load_ledger(None), config, [], [], [cursor],
                               [], [], {"captured"}, set(), [], set())
    encoded_ledger = (json.dumps(ledger, sort_keys=True, separators=(",", ":")) + "\n").encode()
    assert meter._load_ledger(encoded_ledger)["cursors"] == [cursor]


@pytest.mark.parametrize(("path", "expected"), [
    (r"C:\synthetic\source", ("C:", ["synthetic", "source"])),
    (r"C:\synthetic\CON.txt", None),
    (r"C:\synthetic\dir.", None),
    (r"C:\synthetic\a:stream", None),
    (r"C:\synthetic\..\outside", None),
    (r"\\server\share\logs", None),
    (r"C:relative\logs", None),
])
def test_windows_absolute_source_path_is_closed(path, expected):
    if expected is None:
        with pytest.raises(meter.Unavailable):
            meter._windows_absolute_parts(path)
    else:
        assert meter._windows_absolute_parts(path) == expected


def test_windows_replace_payload_uses_fixed_relative_atomic_rename_shape():
    parent = (1 << 63) + 11
    payload = meter._windows_rename_payload(parent, "ledger.json")
    flags, root, length = struct.unpack_from("<I4xQI", payload)
    assert flags == 3
    assert root == parent
    assert length == len("ledger.json".encode("utf-16-le"))
    assert payload[20:] == "ledger.json".encode("utf-16-le")
    for name in ("..", "../outside", "bad:name"):
        with pytest.raises(meter.Unavailable):
            meter._windows_rename_payload(parent, name)


def _synthetic_windows_transaction(tmp_path, *, fail_flush=None, old_target=False,
                                   api_options=None):
    cairn = tmp_path / ".cairn"
    cairn.mkdir(mode=0o700, exist_ok=True)
    (cairn / "meter.json").write_bytes(b"synthetic validated config")
    if old_target:
        meter_dir = cairn / "meter"
        meter_dir.mkdir()
        old = meter._load_ledger(None)
        old_raw = (json.dumps(old, sort_keys=True, separators=(",", ":"))
                   + "\n").encode("ascii")
        (meter_dir / meter.LEDGER_NAME).write_bytes(old_raw)
    api = SyntheticWindowsLedgerAPI(fail_flush=fail_flush, **(api_options or {}))
    cairn_handle = api.handle(cairn)
    held = SimpleNamespace(raw=b"synthetic validated config",
                           user_sid=b"synthetic-user-sid",
                           revalidate=lambda **_options: None)
    return api, held, cairn_handle


def test_windows_synthetic_sharing_is_symmetric_and_candidate_scoped(tmp_path):
    api = SyntheticWindowsLedgerAPI()
    parent = api.handle(tmp_path)
    candidate = api.create_private(".candidate.tmp", parent, b"sid",
                                   directory=False, delete=True, candidate=True)
    reopened = api.open(".candidate.tmp", parent, read_data=True, share=7)
    api.close(reopened)
    with pytest.raises(PermissionError):
        api.open(".candidate.tmp", parent, write_data=True, share=7)
    with pytest.raises(PermissionError):
        api.open(".candidate.tmp", parent, delete=True, share=7)
    api.close(candidate)
    assert (".candidate.tmp", 7, 1) in api.opens

    lock_path = tmp_path / meter.LEDGER_LOCK_NAME
    lock_path.write_bytes(b"")
    native_open = api.open
    def native_sharing_result(name, parent, *, read_data=False, write_data=False,
                              delete=False, share=1, **kwargs):
        try:
            return native_open(name, parent, read_data=read_data,
                               write_data=write_data, delete=delete,
                               share=share, **kwargs)
        except PermissionError:
            if (name == meter.LEDGER_LOCK_NAME and read_data is True
                    and share == 0):
                raise meter.Unavailable("native_lock_open_refused") from None
            raise
    api.open = native_sharing_result
    first_lock, first_info = meter._windows_lock(api, parent, b"sid")
    assert first_info["size"] == 0
    assert (meter.LEDGER_LOCK_NAME, 1, 0) in api.opens
    with pytest.raises(meter.Unavailable) as refused:
        meter._windows_lock(api, parent, b"sid")
    assert refused.value.reason == "ledger_busy"
    api.close(first_lock)


@pytest.mark.parametrize("existing", [False, True])
def test_windows_meter_transaction_parent_shares_read_write_without_delete(
        tmp_path, existing):
    cairn = tmp_path / ".cairn"
    cairn.mkdir()
    if existing:
        (cairn / "meter").mkdir()
    api = SyntheticWindowsLedgerAPI()
    cairn_handle = api.handle(cairn)
    meter_handle, created = meter._windows_open_meter_area(api, cairn_handle, b"sid")
    assert created is not existing
    assert any(name == "meter" and access == 3 and share == 3
               for name, access, share in api.opens)
    competing_writer = api.open("meter", cairn_handle, directory=True,
                                read_data=True, write_data=True, share=3)
    with pytest.raises(PermissionError):
        api.open("meter", cairn_handle, directory=True, read_data=True,
                 delete=True, share=7)
    api.close(competing_writer)
    api.close(meter_handle)


@pytest.mark.parametrize(("directory", "delete", "candidate", "transaction_parent",
                          "expected_access", "expected_share", "expected_role"), [
    (False, False, False, False, 2, 0, "ledger"),
    (True, False, False, False, 3, 1, "meter"),
    (False, True, True, False, 7, 1, "ledger"),
    (True, False, False, True, 3, 3, "meter"),
])
def test_windows_native_create_private_share_modes(directory, delete, candidate,
                                                    transaction_parent,
                                                    expected_access, expected_share,
                                                    expected_role):
    api = object.__new__(meter._WindowsConsentAPI)
    opens, roles, freed = [], [], []
    api.kernel = SimpleNamespace(LocalFree=lambda descriptor: freed.append(descriptor))
    api._private_security_descriptor = lambda _sid, *, directory: "private-descriptor"

    def open_private(name, parent, **options):
        opens.append((name, parent, options))
        return len(opens)

    api.open = open_private
    api.info = lambda _handle: {"directory": directory, "links": 1}
    api.check_acl = lambda _handle, _sid, role: roles.append(role)
    api.close = lambda _handle: None
    handle = api.create_private(
        "owned", 10, b"sid", directory=directory, delete=delete,
        candidate=candidate, transaction_parent=transaction_parent)
    assert handle == 1
    name, parent, options = opens[0]
    assert (name, parent) == ("owned", 10)
    assert options == {
        "directory": directory,
        "read_data": directory or candidate,
        "write_data": True,
        "delete": delete or candidate,
        "share": expected_share,
        "disposition": 2,
        "write_through": True,
        "security_descriptor": "private-descriptor",
    }
    actual_access = (int(options["read_data"]) | (int(options["write_data"]) << 1)
                     | (int(options["delete"]) << 2))
    assert actual_access == expected_access
    assert roles == [expected_role]
    assert freed == ["private-descriptor"]


@pytest.mark.parametrize(("directory", "delete", "candidate", "transaction_parent"), [
    (False, False, False, True),
    (False, True, True, True),
    (True, False, True, True),
    (True, True, False, True),
    (True, False, False, 1),
])
def test_windows_native_create_private_rejects_invalid_transaction_parent_modes(
        directory, delete, candidate, transaction_parent):
    api = object.__new__(meter._WindowsConsentAPI)
    api._private_security_descriptor = lambda *_args, **_kwargs: pytest.fail(
        "invalid transaction-parent mode reached descriptor creation")
    with pytest.raises(meter.Unavailable, match="ledger_write_failed"):
        api.create_private("owned", 10, b"sid", directory=directory,
                           delete=delete, candidate=candidate,
                           transaction_parent=transaction_parent)


@pytest.mark.parametrize("missing", [False, True])
def test_windows_meter_parent_open_or_create_selects_transaction_mode(missing):
    calls = []

    class Api:
        def open(self, name, parent, *, directory=False, read_data=False,
                 write_data=False, share=1):
            calls.append(("open", name, parent, directory, read_data, write_data, share))
            if missing:
                raise meter._MissingConfig
            return 17

        def create_private(self, name, parent, sid, **options):
            calls.append(("create", name, parent, sid, options))
            return 18

        def info(self, _handle):
            return {"directory": True}

        def check_acl(self, handle, sid, role):
            calls.append(("acl", handle, sid, role))

        def flush_full(self, handle):
            calls.append(("flush", handle))

        def close(self, _handle):
            calls.append(("close", _handle))

    api = Api()
    handle, created = meter._windows_open_meter_area(api, 11, b"sid")
    assert created is missing
    assert handle == (18 if missing else 17)
    assert calls[0] == ("open", "meter", 11, True, True, True, 3)
    if missing:
        assert calls[1] == ("create", "meter", 11, b"sid", {
            "directory": True, "transaction_parent": True})
        assert calls[2] == ("flush", 11)
        assert calls[3] == ("acl", 18, b"sid", "meter")
    else:
        assert calls[1] == ("acl", 17, b"sid", "meter")


def test_windows_atomic_replace_publishes_complete_validated_candidate(tmp_path):
    api, held, cairn = _synthetic_windows_transaction(tmp_path)
    def build(prior):
        assert (tmp_path / ".cairn" / "meter" / meter.LEDGER_LOCK_NAME).is_file()
        return prior
    assert meter._windows_atomic_replace(
        api, held, cairn, held.raw, held.user_sid, build) == "written"
    candidate = meter._load_ledger(None)
    stored = (tmp_path / ".cairn" / "meter" / meter.LEDGER_NAME).read_bytes()
    assert stored == (json.dumps(candidate, sort_keys=True, separators=(",", ":"))
                      + "\n").encode("ascii")
    lock = tmp_path / ".cairn" / "meter" / meter.LEDGER_LOCK_NAME
    assert lock.is_file() and lock.stat().st_size == 0
    assert not list((tmp_path / ".cairn" / "meter").glob(".ledger-*.tmp"))
    assert any(name.startswith(".ledger-") and access == 7 and share == 1
               for name, access, share in api.opens)
    assert (meter.LEDGER_NAME, 1, 7) in api.opens


def test_windows_atomic_replace_failure_preserves_old_bytes_and_cleans_candidate(tmp_path):
    meter_dir = tmp_path / ".cairn" / "meter"
    meter_dir.mkdir(parents=True, mode=0o700)
    old = meter._load_ledger(None)
    old_bytes = (json.dumps(old, sort_keys=True, separators=(",", ":"))
                 + "\n").encode("ascii")
    (meter_dir / meter.LEDGER_NAME).write_bytes(old_bytes)
    api, held, cairn = _synthetic_windows_transaction(tmp_path, fail_flush="candidate")
    candidate = meter._load_ledger(None)
    with pytest.raises(meter.Unavailable):
        meter._windows_atomic_replace(api, held, cairn, held.raw, held.user_sid, candidate)
    assert (meter_dir / meter.LEDGER_NAME).read_bytes() == old_bytes
    assert not list(meter_dir.glob(".ledger-*.tmp"))


def test_windows_atomic_replace_postpublication_flush_failure_is_uncertain(tmp_path):
    api, held, cairn = _synthetic_windows_transaction(tmp_path, fail_flush="meter")
    candidate = meter._load_ledger(None)
    assert meter._windows_atomic_replace(
        api, held, cairn, held.raw, held.user_sid, candidate) == "committed_uncertain"
    assert (tmp_path / ".cairn" / "meter" / meter.LEDGER_NAME).is_file()


def test_windows_refresh_disabled_paths_stop_before_source_or_ledger_access():
    class Api:
        def __init__(self, opened):
            self.opened = opened
            self.calls = 0

        def read_config(self, _profile, _sid, *, retain_handles, writable_cairn=False):
            assert retain_handles
            assert not writable_cairn
            self.calls += 1
            return self.opened

    missing = Api(None)
    assert meter._refresh_ledger_windows("C:\\synthetic\\profile", missing, b"sid") == {
        "status": "disabled", "reason": "config_missing", "coverage": "unknown"}
    assert missing.calls == 1
    held = SimpleNamespace(links=[], raw=b'{"version":1,"enabled":false,"sources":[],"projects":[]}',
                           closed=False)
    held.close = lambda: setattr(held, "closed", True)
    disabled = Api((held.raw, held))
    assert meter._refresh_ledger_windows("C:\\synthetic\\profile", disabled, b"sid") == {
        "status": "disabled", "reason": "disabled", "coverage": "unknown"}
    assert disabled.calls == 1 and held.closed


def _synthetic_windows_export_context(tmp_path, monkeypatch, *, old_target=True,
                                      api_options=None):
    project_path = tmp_path / "synthetic" / "project"
    measurement = project_path / "dev" / "measurement"
    measurement.mkdir(parents=True)
    old = b"old sanitized export\n"
    if old_target:
        (measurement / "meter.json").write_bytes(old)
    project = {"alias": "sample", "path": r"C:\synthetic\project",
               "remote": "https://example.test/team/project.git"}
    config = meter.validate_config_bytes(json.dumps({
        "version": 1, "enabled": True, "sources": [],
        "projects": [dict(project, path="/synthetic/project")],
    }).encode())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda _project, _roots, **_kwargs:
                        (project["remote"], None))
    api = SyntheticWindowsExportAPI(tmp_path, **(api_options or {}))
    return project, config, api, measurement, old


def test_windows_project_export_replaces_only_the_sanitized_ignored_file(
        tmp_path, monkeypatch):
    project_path = tmp_path / "synthetic" / "project"
    measurement = project_path / "dev" / "measurement"
    measurement.mkdir(parents=True)
    (measurement / "meter.json").write_bytes(b"old sanitized export\n")
    project = {"alias": "sample", "path": r"C:\synthetic\project",
               "remote": "https://example.test/team/project.git"}
    excluded = [r"C:\synthetic\source", project["path"]]
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda _project, _roots, **_kwargs:
                        (project["remote"], None))
    api = SyntheticWindowsExportAPI(tmp_path)
    config_project = dict(project, path="/synthetic/project")
    config = meter.validate_config_bytes(json.dumps({
        "version": 1, "enabled": True, "sources": [],
        "projects": [config_project],
    }).encode())
    ledger = meter._load_ledger(None)
    assert meter._windows_atomic_write_project_export(
        project, ledger, config, excluded, api, b"synthetic-user-sid") == "written"
    stored = json.loads((measurement / "meter.json").read_bytes())
    assert stored["schema"] == "cairn-meter-project/2"
    assert stored["coverage"]["global"] == "unknown"
    assert not list(measurement.glob(".meter-*.tmp"))
    assert any(name.startswith(".meter-") and access == 7 and share == 1
               for name, access, share in api.opens)
    assert ("meter.json", 1, 7) in api.opens
    assert ("measurement", 3, 3) in api.opens
    assert ("measurement", 1, 3) in api.opens


@pytest.mark.parametrize("transaction", ["ledger", "export"])
@pytest.mark.parametrize(("case", "old_target", "post_created", "sequence", "expected"), [
    ("candidate-created", True, "candidate", None, "written"),
    ("prior-target-created", True, "prior", None, "written"),
    ("absent-target-third", False, 900002, None, "committed_uncertain"),
    ("third-created", True, 900002, None, "committed_uncertain"),
    ("later-switch", True, None, ("prior", "candidate"), "committed_uncertain"),
])
def test_windows_rename_creation_time_admission(
        tmp_path, monkeypatch, transaction, case, old_target,
        post_created, sequence, expected):
    options = {"post_rename_created": post_created,
               "post_rename_created_sequence": sequence}
    if transaction == "ledger":
        api, held, cairn = _synthetic_windows_transaction(
            tmp_path, old_target=old_target, api_options=options)
        target = tmp_path / ".cairn" / "meter" / meter.LEDGER_NAME
        temporary = tmp_path / ".cairn" / "meter"
        result = meter._windows_atomic_replace(
            api, held, cairn, held.raw, held.user_sid, meter._load_ledger(None))
        api.close(cairn)
    else:
        project, config, api, temporary, old = _synthetic_windows_export_context(
            tmp_path, monkeypatch, old_target=old_target, api_options=options)
        target = temporary / "meter.json"
        result = meter._windows_atomic_write_project_export(
            project, meter._load_ledger(None), config, [project["path"]],
            api, b"synthetic-user-sid")
    assert result == expected, case
    assert target.is_file()
    assert not list(temporary.glob(".ledger-*.tmp" if transaction == "ledger"
                                   else ".meter-*.tmp"))
    assert not api.handles
    if expected == "committed_uncertain":
        published = api.published_candidate_identity
        assert published is not None
        stat = target.stat()
        assert (stat.st_dev, stat.st_ino) == published


@pytest.mark.parametrize("transaction", ["ledger", "export"])
def test_windows_rename_prepublication_creation_time_drift_still_refuses(
        tmp_path, monkeypatch, transaction):
    options = {"drift_candidate_created": True}
    if transaction == "ledger":
        api, held, cairn = _synthetic_windows_transaction(
            tmp_path, old_target=True, api_options=options)
        target = tmp_path / ".cairn" / "meter" / meter.LEDGER_NAME
        old = target.read_bytes()
        temporary = tmp_path / ".cairn" / "meter"
        write = lambda: meter._windows_atomic_replace(
            api, held, cairn, held.raw, held.user_sid, meter._load_ledger(None))
    else:
        project, config, api, temporary, _old = _synthetic_windows_export_context(
            tmp_path, monkeypatch, old_target=True, api_options=options)
        target = temporary / "meter.json"
        old = target.read_bytes()
        write = lambda: meter._windows_atomic_write_project_export(
            project, meter._load_ledger(None), config, [project["path"]],
            api, b"synthetic-user-sid")
    with pytest.raises(meter.Unavailable) as caught:
        write()
    if transaction == "ledger":
        api.close(cairn)
    assert caught.value.reason == "source_changed"
    assert target.read_bytes() == old
    assert not list(temporary.glob(".ledger-*.tmp" if transaction == "ledger"
                                   else ".meter-*.tmp"))
    assert api.published_candidate_identity is None
    assert not api.handles


def test_windows_project_export_rechecks_directory_acl_before_replace(
        tmp_path, monkeypatch):
    project_path = tmp_path / "synthetic" / "project"
    measurement = project_path / "dev" / "measurement"
    measurement.mkdir(parents=True)
    old = b"old sanitized export\n"
    (measurement / "meter.json").write_bytes(old)
    project = {"alias": "sample", "path": r"C:\synthetic\project",
               "remote": "https://example.test/team/project.git"}
    config = meter.validate_config_bytes(json.dumps({
        "version": 1, "enabled": True, "sources": [],
        "projects": [dict(project, path="/synthetic/project")],
    }).encode())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda _project, _roots, **_kwargs:
                        (project["remote"], None))
    api = SyntheticWindowsExportAPI(tmp_path, fail_acl_call=7)
    before = api.volume_root.stat().st_ctime_ns
    with pytest.raises(meter.Unavailable):
        meter._windows_atomic_write_project_export(
            project, meter._load_ledger(None), config, [project["path"]],
            api, b"synthetic-user-sid")
    assert (measurement / "meter.json").read_bytes() == old
    assert not list(measurement.glob(".meter-*.tmp"))
    assert api.volume_root.stat().st_ctime_ns == before


@pytest.mark.parametrize("failure", ["candidate", "measurement"])
def test_windows_project_export_preserves_or_reports_uncertainty(
        tmp_path, monkeypatch, failure):
    project_path = tmp_path / "synthetic" / "project"
    measurement = project_path / "dev" / "measurement"
    measurement.mkdir(parents=True)
    old = b"old sanitized export\n"
    (measurement / "meter.json").write_bytes(old)
    project = {"alias": "sample", "path": r"C:\synthetic\project",
               "remote": "https://example.test/team/project.git"}
    config = meter.validate_config_bytes(json.dumps({
        "version": 1, "enabled": True, "sources": [],
        "projects": [dict(project, path="/synthetic/project")],
    }).encode())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda _project, _roots, **_kwargs:
                        (project["remote"], None))
    api = SyntheticWindowsExportAPI(tmp_path, fail_flush=failure)
    call = lambda: meter._windows_atomic_write_project_export(
        project, meter._load_ledger(None), config,
        [project["path"]], api, b"synthetic-user-sid")
    if failure == "candidate":
        with pytest.raises(meter.Unavailable):
            call()
        assert (measurement / "meter.json").read_bytes() == old
        assert not list(measurement.glob(".meter-*.tmp"))
    else:
        assert call() == "committed_uncertain"
        assert (measurement / "meter.json").read_bytes() != old


@pytest.mark.parametrize("missing_at", ["project", "dev", "measurement"])
def test_windows_project_export_missing_directory_returns_fixed_unavailability(
        tmp_path, monkeypatch, missing_at):
    project_path = tmp_path / "synthetic" / "project"
    measurement = project_path / "dev" / "measurement"
    measurement.mkdir(parents=True)
    old = b"old sanitized export\n"
    (measurement / "meter.json").write_bytes(old)
    project = {"alias": "sample", "path": r"C:\synthetic\project",
               "remote": "https://example.test/team/project.git"}
    config = meter.validate_config_bytes(json.dumps({
        "version": 1, "enabled": True, "sources": [],
        "projects": [dict(project, path="/synthetic/project")],
    }).encode())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda _project, _roots, **_kwargs:
                        (project["remote"], None))
    api = SyntheticWindowsExportAPI(tmp_path, missing_at=missing_at)
    with pytest.raises(meter.Unavailable) as caught:
        meter._windows_atomic_write_project_export(
            project, meter._load_ledger(None), config, [project["path"]],
            api, b"synthetic-user-sid")
    assert caught.value.reason == "project_export_unavailable"
    assert str(tmp_path) not in str(caught.value)
    assert (measurement / "meter.json").read_bytes() == old
    assert not list(measurement.glob(".meter-*.tmp"))
    assert not api.handles


def test_windows_project_export_missing_during_cleanup_returns_fixed_unavailability(
        tmp_path, monkeypatch):
    project_path = tmp_path / "synthetic" / "project"
    measurement = project_path / "dev" / "measurement"
    measurement.mkdir(parents=True)
    old = b"old sanitized export\n"
    (measurement / "meter.json").write_bytes(old)
    project = {"alias": "sample", "path": r"C:\synthetic\project",
               "remote": "https://example.test/team/project.git"}
    config = meter.validate_config_bytes(json.dumps({
        "version": 1, "enabled": True, "sources": [],
        "projects": [dict(project, path="/synthetic/project")],
    }).encode())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda _project, _roots, **_kwargs:
                        (project["remote"], None))
    api = SyntheticWindowsExportAPI(
        tmp_path, fail_flush="candidate", missing_during_cleanup=True)
    with pytest.raises(meter.Unavailable) as caught:
        meter._windows_atomic_write_project_export(
            project, meter._load_ledger(None), config, [project["path"]],
            api, b"synthetic-user-sid")
    assert caught.value.reason == "project_export_unavailable"
    assert str(tmp_path) not in str(caught.value)
    assert (measurement / "meter.json").read_bytes() == old
    assert not list(measurement.glob(".meter-*.tmp"))
    assert not api.handles


def test_windows_project_export_disappearance_after_publish_is_uncertain(
        tmp_path, monkeypatch):
    project_path = tmp_path / "synthetic" / "project"
    measurement = project_path / "dev" / "measurement"
    measurement.mkdir(parents=True)
    old = b"old sanitized export\n"
    (measurement / "meter.json").write_bytes(old)
    project = {"alias": "sample", "path": r"C:\synthetic\project",
               "remote": "https://example.test/team/project.git"}
    config = meter.validate_config_bytes(json.dumps({
        "version": 1, "enabled": True, "sources": [],
        "projects": [dict(project, path="/synthetic/project")],
    }).encode())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda _project, _roots, **_kwargs:
                        (project["remote"], None))
    api = SyntheticWindowsExportAPI(tmp_path, disappear_after_publish=True)
    assert meter._windows_atomic_write_project_export(
        project, meter._load_ledger(None), config, [project["path"]],
        api, b"synthetic-user-sid") == "committed_uncertain"
    assert api.published
    assert (measurement / "meter.json").read_bytes() != old
    assert not list(measurement.glob(".meter-*.tmp"))
    assert not api.handles


def test_codex_context_accepts_exact_native_windows_cwd_spelling(monkeypatch):
    monkeypatch.setattr(meter, "os", SimpleNamespace(name="nt"))
    owner = ("thread-id", "session-id")
    context = meter._codex_context({"turn_id": "turn-a",
                                    "cwd": r"C:\Work\repo"}, owner)
    assert context["cwd"] == r"C:\Work\repo"
    for cwd in (r"c:/Work/repo", r"C:\Work\..\repo",
                r"\\server\share\repo", r"C:relative\repo"):
        with pytest.raises(ValueError):
            meter._codex_context({"turn_id": "turn-a", "cwd": cwd}, owner)


def test_codex_context_accepts_exact_native_windows_cwd_spelling(monkeypatch):
    monkeypatch.setattr(meter, "os", SimpleNamespace(name="nt"))
    owner = ("thread-id", "session-id")
    context = meter._codex_context({"turn_id": "turn-a",
                                    "cwd": r"C:\Work\repo"}, owner)
    assert context["cwd"] == r"C:\Work\repo"
    for cwd in (r"c:/Work/repo", r"C:\Work\..\repo",
                r"\\server\share\repo", r"C:relative\repo"):
        with pytest.raises(ValueError):
            meter._codex_context({"turn_id": "turn-a", "cwd": cwd}, owner)


def test_windows_approved_stream_revalidates_and_excludes_access_time():
    api = SyntheticWindowsStreamAPI(b'{"record":1}\n')
    stream = meter._iter_approved_lines(
        r"C:\synthetic\source", "session.jsonl", windows_api=api,
        windows_user_sid=b"synthetic-user-sid")
    assert list(stream) == [b'{"record":1}\n']
    assert stream.terminal_reason is None
    assert stream.bytes_read == len(b'{"record":1}\n')
    assert stream.complete_lines == 1
    assert stream.open_identity == stream.final_identity


def test_windows_approved_stream_marks_a_partial_tail_unknown():
    api = SyntheticWindowsStreamAPI(b'{"partial":1}')
    stream = meter._iter_approved_lines(
        r"C:\synthetic\source", "session.jsonl", windows_api=api,
        windows_user_sid=b"synthetic-user-sid")
    assert list(stream) == []
    assert stream.terminal_reason == "partial_tail"


def test_windows_source_enumeration_reopens_and_matches_entry_identity():
    api = SyntheticWindowsStreamAPI(b'{"record":1}\n')
    files, entries, identity = meter._enumerate_windows_jsonl(
        r"C:\synthetic\source", api, b"synthetic-user-sid")
    assert entries == 1
    assert files == [("session.jsonl", {
        "dev": 7, "ino": 4, "size": len(b'{"record":1}\n'),
        "mtime_ns": 3100, "ctime_ns": 4100,
    })]
    assert identity == {"dev": 7, "ino": 3}


def test_windows_source_enumeration_refuses_replaced_file_identity():
    api = SyntheticWindowsStreamAPI(b'{"record":1}\n')
    api.entry_file_id += 1
    with pytest.raises(meter.Unavailable):
        meter._enumerate_windows_jsonl(
            r"C:\synthetic\source", api, b"synthetic-user-sid")


def test_windows_source_snapshot_detects_directory_changes_until_closed():
    api = SyntheticWindowsStreamAPI(b'{"record":1}\n')
    _files, _entries, _identity, snapshot = meter._enumerate_windows_jsonl(
        r"C:\synthetic\source", api, b"synthetic-user-sid",
        retain_snapshot=True)
    try:
        snapshot.verify()
        api.directory_written += 1
        with pytest.raises(meter.Unavailable):
            snapshot.verify()
    finally:
        snapshot.close()


def test_windows_claim_capture_hashes_only_bounded_project_intents():
    claim_id, rows = c2_claim_records("synthetic-claim-owner")
    raw = b"".join(encoded(rows))
    api = SyntheticWindowsProjectAPI(raw)
    project = {"alias": "sample", "path": r"C:\synthetic\project"}
    claims, status = meter._capture_project_claims(
        project, windows_api=api, windows_user_sid=b"synthetic-user-sid")
    claim, = claims
    assert status == "captured"
    assert claim["session_digest"] == meter._short_session_digest("synthetic-claim-owner")
    assert claim_id not in json.dumps(claim)
    assert "synthetic-claim-owner" not in json.dumps(claim)


def test_windows_claim_capture_treats_missing_or_changed_file_as_unavailable():
    project = {"alias": "sample", "path": r"C:\synthetic\project"}
    missing = SyntheticWindowsProjectAPI(b"", missing=True)
    assert meter._capture_project_claims(
        project, windows_api=missing, windows_user_sid=b"synthetic-user-sid") == (
            [], "attribution_unavailable")
    changed = SyntheticWindowsProjectAPI(b"{}\n")
    changed.change_after_read = True
    with pytest.raises(meter.Unavailable, match="source_changed"):
        meter._capture_project_claims(
            project, windows_api=changed, windows_user_sid=b"synthetic-user-sid")


def test_windows_claim_capture_enforces_complete_line_cap():
    project = {"alias": "sample", "path": r"C:\synthetic\project"}
    _claim_id, rows = c2_claim_records("synthetic-claim-owner")
    valid = encoded(rows)[0][:-1]
    exact = valid + b" " * (meter.MAX_CLAIM_LINE - len(valid) - 1) + b"\n"
    claims, status = meter._capture_project_claims(
        project, windows_api=SyntheticWindowsProjectAPI(exact),
        windows_user_sid=b"synthetic-user-sid")
    assert len(claims) == 1 and status == "captured"
    oversized = SyntheticWindowsProjectAPI(
        valid + b" " * (meter.MAX_CLAIM_LINE - len(valid)) + b"\n")
    with pytest.raises(meter.Unavailable, match="source_budget_exceeded"):
        meter._capture_project_claims(
            project, windows_api=oversized,
            windows_user_sid=b"synthetic-user-sid")


def test_windows_scan_normalizes_synthetic_source_without_project_proof(monkeypatch):
    from pathlib import PureWindowsPath

    monkeypatch.setattr(meter, "Path", PureWindowsPath)
    monkeypatch.setattr(meter, "os", SimpleNamespace(
        name="nt", path=SimpleNamespace(abspath=lambda value: value)))
    config = {
        "version": 1, "enabled": True,
        "sources": [{"alias": "source", "tool": "codex",
                     "root": r"C:\synthetic\source"}],
        "projects": [{"alias": "project", "path": r"C:\synthetic\project",
                      "remote": "https://example.test/team/project.git"}],
        "requested_accounts": {},
    }
    records = codex()
    records[1]["payload"]["cwd"] = r"C:\synthetic\project"
    api = SyntheticWindowsStreamAPI(b"".join(encoded(records)))
    events, cursors, reasons, forks, conflicts, waits = meter._scan_approved_sources(
        config, [], windows_api=api, windows_user_sid=b"synthetic-user-sid")
    event, = events
    assert event["ownership"] == "proven"
    assert event["project_association"] == "unknown"
    assert "project_remote_unavailable" in event["reasons"]
    assert cursors[0]["dev"] == 7 and cursors[0]["ino"] == 4
    assert not forks and not conflicts and not waits


@pytest.mark.parametrize("name", ["../escape", "bad:name", "trailing.", "name "])
def test_windows_directory_decoder_rejects_unsafe_component_names(name):
    with pytest.raises(meter.Unavailable):
        meter._decode_windows_directory_entries(bytes(_windows_directory_record(name)))


@pytest.mark.parametrize(("content", "expected"), [
    (None, "disabled"),
    (windows_config_bytes(False), "disabled"),
    (windows_config_bytes(True), "unavailable"),
    (b'{"version":1,"enabled":NaN}', "unavailable"),
    (OSError("SECRET-PATH"), "unavailable"),
])
def test_windows_consent_status_is_closed_and_uses_only_fixed_profile(content, expected):
    api = SyntheticWindowsConsent(content)
    assert meter._windows_config_status(api) == expected
    assert api.calls == [
        "profile", ("config", "C:\\synthetic\\profile", b"synthetic-user-sid")]


@WINDOWS_ONLY
@pytest.mark.parametrize(("content", "expected"), [
    (None, "disabled"),
    (windows_config_bytes(False), "disabled"),
    (windows_config_bytes(True), "unavailable"),
    (b'{"version":1,"enabled":NaN}', "unavailable"),
], ids=["missing", "disabled", "enabled", "invalid-json"])
def test_windows_native_status_reads_only_synthetic_profile(native_windows_root, monkeypatch, content, expected):
    def forbidden(*_args, **_kwargs):
        raise AssertionError("status check crossed into collection")

    for name in ("_scan_approved_sources", "_verified_project_remote", "_refresh_ledger"):
        monkeypatch.setattr(meter, name, forbidden)
    api, wrapped, profile = native_windows_status(native_windows_root, content)
    assert api.read_config(str(profile), wrapped.sid) == content
    assert meter._windows_config_status(wrapped) == expected


@WINDOWS_ONLY
def test_windows_native_status_refuses_config_hardlink(native_windows_root, monkeypatch):
    content = windows_config_bytes(False)
    api, wrapped, profile = native_windows_status(native_windows_root, content)
    assert meter._windows_config_status(wrapped) == "disabled"
    config = profile / ".cairn" / "meter.json"
    os.link(config, config.with_name("linked-copy.json"))
    observed = []
    original_info = api.info

    def record_link_count(handle):
        info = original_info(handle)
        if not info["directory"]:
            observed.append(info["links"])
        return info

    monkeypatch.setattr(api, "info", record_link_count)
    assert meter._windows_config_status(wrapped) == "unavailable"
    assert observed == [2], "the refusal must reach the linked config"


@WINDOWS_ONLY
def test_windows_native_status_refuses_permissive_config_dacl(native_windows_root, monkeypatch):
    import subprocess

    api, wrapped, profile = native_windows_status(native_windows_root, windows_config_bytes(False))
    assert meter._windows_config_status(wrapped) == "disabled"
    config_raw, held = api.read_config(str(profile), wrapped.sid,
                                       retain_handles=True, writable_cairn=True)
    assert config_raw == windows_config_bytes(False)
    cairn = profile / ".cairn"
    result = subprocess.run(["icacls", str(cairn), "/grant", "*S-1-1-0:F"],
                            capture_output=True, check=False)
    assert result.returncode == 0, "could not prepare the disposable permissive ACL fixture"
    original_cairn_acl = api.check_acl
    refused_roles = []

    def record_cairn_acl_refusal(handle, sid, role):
        try:
            return original_cairn_acl(handle, sid, role)
        except meter.Unavailable:
            refused_roles.append(role)
            raise

    api.check_acl = record_cairn_acl_refusal
    try:
        with pytest.raises(meter.Unavailable) as refused:
            held.revalidate(allow_owned_cairn_metadata=True)
        assert refused.value.reason == "unavailable"
        assert refused_roles == ["cairn"]
    finally:
        try:
            result = subprocess.run(["icacls", str(cairn), "/remove", "*S-1-1-0"],
                                    capture_output=True, check=False)
        finally:
            api.check_acl = original_cairn_acl
            held.close()
        assert result.returncode == 0, "could not restore the disposable ACL fixture"

    config = profile / ".cairn" / "meter.json"
    result = subprocess.run(["icacls", str(config), "/grant", "*S-1-1-0:F"],
                            capture_output=True, check=False)
    assert result.returncode == 0, "could not prepare the disposable permissive ACL fixture"
    refused_roles = []
    original_check_acl = api.check_acl

    def record_acl_refusal(handle, sid, role):
        try:
            return original_check_acl(handle, sid, role)
        except meter.Unavailable:
            refused_roles.append(role)
            raise

    monkeypatch.setattr(api, "check_acl", record_acl_refusal)
    assert meter._windows_config_status(wrapped) == "unavailable"
    assert refused_roles == ["config"], "the refusal must reach the config ACL"


def c2_codex_records(project):
    records = codex()
    records[1]["payload"]["cwd"] = str(project)
    return records


def c2_bound_records(project, owner, turn, input_count, waits):
    records = [
        row("session_meta", {"id": owner, "session_id": owner, "source": "cli",
                             "thread_source": "user", "history_mode": "legacy"}),
        row("turn_context", {"turn_id": turn, "root_turn_id": turn,
                              "cwd": str(project), "model": "gpt-5.3-codex"}),
        codex_direct(owner, owner, turn, turn, "response-" + turn,
                     input_count, input_count, input_count),
    ]
    start = int(datetime(2026, 11, 5, 12, 0, tzinfo=timezone.utc).timestamp() * 1000)
    for item_id, duration in waits:
        timing = timing_record(item_id=item_id, start=start, end=start + duration)
        timing["payload"]["thread_id"] = owner
        timing["payload"]["turn_id"] = turn
        records.append(timing)
    return records


def c2_claim_records(owner):
    claim_id = "synthetic-claim-identifier"
    agent = "codex-" + meter._short_session_digest(owner)
    return claim_id, [
        {"event": "claim", "id": claim_id, "ts": "2026-11-05T11:00:00Z",
         "agent": agent, "files": ["src/app.py"], "action": "SECRET-ACTION",
         "stem": "SECRET-STEM"},
        {"event": "release", "id": claim_id, "ts": "2026-11-05T13:00:00Z",
         "commit": "SECRET-COMMIT"},
    ]


def scan_fork_files(tmp_path, monkeypatch, *, parent_input=100,
                    child_mutation=None):
    home, source, project, config_path = c2_home(tmp_path)
    parent_rows, child_rows, _parent, _child = codex_fork_fixture(
        project, parent_input=parent_input)
    if child_mutation is not None:
        child_mutation(child_rows)
    (source / "parent.jsonl").write_bytes(b"".join(encoded(parent_rows)))
    (source / "child.jsonl").write_bytes(b"".join(encoded(child_rows)))
    config = meter.validate_config_bytes(config_path.read_bytes())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))
    scan = meter._scan_approved_sources(config, [])
    return home, config, scan


def run_main_with_synthetic_home(home, monkeypatch, capsys, *, fake_home=None,
                                 command=None, refresh_result=None,
                                 global_overrides=None):
    namespace = runpy.run_path(str(METER), run_name="meter_test")
    namespace["main"].__globals__["_fixed_user_home"] = lambda: Path(home)
    def synthetic_windows_status():
        config = Path(home) / ".cairn" / "meter.json"
        try:
            content = config.read_bytes()
        except FileNotFoundError:
            content = None
        return meter._windows_config_decision(content)
    namespace["main"].__globals__["_windows_config_status"] = synthetic_windows_status
    if refresh_result is not None:
        def synthetic_refresh(received_home):
            assert Path(received_home) == Path(home)
            return refresh_result
        namespace["main"].__globals__["_refresh_ledger"] = synthetic_refresh
    if global_overrides is not None:
        namespace["main"].__globals__.update(global_overrides)
    if fake_home is not None:
        monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.setattr(sys, "stdin", io.StringIO("SYNTHETIC-STDIN"))
    argv = [str(METER)]
    argv.extend([command, "--json"] if command else ["--json"])
    monkeypatch.setattr(sys, "argv", argv)
    code = namespace["main"]()
    return code, capsys.readouterr()


def _run_synthetic_meter_command(home, monkeypatch, capsys, command, verified_remote):
    return run_main_with_synthetic_home(
        home, monkeypatch, capsys, command=command,
        global_overrides={"_verified_project_remote": verified_remote})


def _arm_after_ledger_commit(monkeypatch, arm):
    original = meter._atomic_replace_ledger

    def replace_then_arm(*args, **kwargs):
        result = original(*args, **kwargs)
        arm()
        return result

    monkeypatch.setattr(meter, "_atomic_replace_ledger", replace_then_arm)


@pytest.mark.parametrize("command", ["refresh", "rebuild"])
def test_explicit_refresh_commands_emit_closed_receipt_from_synthetic_home(
        tmp_path, monkeypatch, capsys, command):
    result = {"status": "written", "reason": "none", "events": 123,
              "claims": 456, "coverage": "complete"}
    code, captured = run_main_with_synthetic_home(
        tmp_path, monkeypatch, capsys, command=command, refresh_result=result)
    receipt = json.loads(captured.out)
    assert code == 0
    assert receipt == {"schema": "cairn-meter-refresh/1", "status": "ok",
                       "reason": "none", "coverage": "unknown"}
    assert set(receipt) == {"schema", "status", "reason", "coverage"}
    assert captured.err == ""


def test_refresh_receipt_rejects_unlisted_reasons_and_unknown_status():
    assert meter._closed_refresh_receipt({"status": "unavailable",
                                          "reason": "SECRET-path"}) == {
        "schema": "cairn-meter-refresh/1", "status": "unavailable",
        "reason": "unavailable", "coverage": "unknown"}
    assert meter._closed_refresh_receipt({"status": "written", "events": 8}) == {
        "schema": "cairn-meter-refresh/1", "status": "ok",
        "reason": "none", "coverage": "unknown"}


def test_windows_refresh_installs_job_only_after_enabled_config_and_retains_it(monkeypatch):
    class Held:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    class Api:
        def __init__(self, enabled):
            self.enabled = enabled
            self.calls = []
            self.held = Held()

        def current_user_profile(self):
            self.calls.append("profile")
            return r"C:\synthetic\profile", b"synthetic-sid"

        def read_config(self, profile, sid, *, retain_handles):
            self.calls.append(("config", profile, sid, retain_handles))
            raw = json.dumps({"version": 1, "enabled": self.enabled,
                              "sources": [], "projects": []}).encode()
            return raw, self.held

        def install_worker_job(self):
            self.calls.append("job")
            return 77

        def close(self, handle):
            self.calls.append(("close", handle))

    api = Api(enabled=True)
    monkeypatch.setattr(meter, "_WindowsConsentAPI", lambda: api)
    monkeypatch.setattr(meter, "_WINDOWS_WORKER_JOBS", [])

    def refresh(profile, received_api, sid, *, opened):
        assert profile == r"C:\synthetic\profile"
        assert received_api is api and sid == b"synthetic-sid"
        assert opened[1] is api.held
        assert api.calls[-1] == "job"
        try:
            return {"status": "ok", "reason": "none", "events": 5}
        finally:
            opened[1].close()

    monkeypatch.setattr(meter, "_refresh_ledger_windows", refresh)
    assert meter._run_windows_refresh() == {"status": "ok", "reason": "none",
                                            "events": 5}
    assert api.calls == ["profile", ("config", r"C:\synthetic\profile",
                                      b"synthetic-sid", True), "job"]
    assert api.held.closed
    assert meter._WINDOWS_WORKER_JOBS == [(api, 77)]


def test_windows_disabled_refresh_never_installs_job_or_enters_collector(monkeypatch):
    class Held:
        closed = False

        def close(self):
            self.closed = True

    class Api:
        def __init__(self):
            self.held = Held()
            self.calls = []

        def current_user_profile(self):
            return r"C:\synthetic\profile", b"synthetic-sid"

        def read_config(self, _profile, _sid, *, retain_handles):
            assert retain_handles
            raw = b'{"version":1,"enabled":false,"sources":[],"projects":[]}'
            return raw, self.held

        def install_worker_job(self):
            self.calls.append("job")
            raise AssertionError("disabled refresh must not create a Job")

        def close(self, handle):
            self.calls.append(handle)

    api = Api()
    monkeypatch.setattr(meter, "_WindowsConsentAPI", lambda: api)
    monkeypatch.setattr(meter, "_refresh_ledger_windows",
                        lambda *_args, **_kwargs: pytest.fail("collector was entered"))
    assert meter._run_windows_refresh() == {"status": "disabled",
                                            "reason": "disabled"}
    assert api.held.closed
    assert api.calls == []


def test_windows_job_failure_closes_config_and_stops_before_collector(monkeypatch):
    class Held:
        closed = False

        def close(self):
            self.closed = True

    class Api:
        def __init__(self):
            self.held = Held()

        def current_user_profile(self):
            return r"C:\synthetic\profile", b"synthetic-sid"

        def read_config(self, _profile, _sid, *, retain_handles):
            assert retain_handles
            raw = b'{"version":1,"enabled":true,"sources":[],"projects":[]}'
            return raw, self.held

        def install_worker_job(self):
            raise meter.Unavailable("job_unavailable")

    api = Api()
    monkeypatch.setattr(meter, "_WindowsConsentAPI", lambda: api)
    monkeypatch.setattr(meter, "_refresh_ledger_windows",
                        lambda *_args, **_kwargs: pytest.fail("collector was entered"))
    assert meter._run_windows_refresh() == {"status": "unavailable",
                                            "reason": "job_unavailable"}
    assert api.held.closed


def test_windows_main_refresh_uses_only_injected_profile_and_closed_receipt(
        monkeypatch, capsys):
    class Held:
        def close(self):
            self.closed = True

        closed = False

    class Api:
        held = Held()

        def current_user_profile(self):
            return r"C:\synthetic\profile", b"synthetic-sid"

        def read_config(self, _profile, _sid, *, retain_handles):
            assert retain_handles
            raw = b'{"version":1,"enabled":true,"sources":[],"projects":[]}'
            return raw, self.held

        def install_worker_job(self):
            return 99

    api = Api()
    namespace = runpy.run_path(str(METER), run_name="meter_test")
    globals_ = namespace["main"].__globals__
    globals_["os"] = SimpleNamespace(name="nt")
    globals_["_WindowsConsentAPI"] = lambda: api
    globals_["_WINDOWS_WORKER_JOBS"] = []

    def collect(profile, received_api, sid, *, opened):
        assert profile == r"C:\synthetic\profile"
        assert received_api is api and sid == b"synthetic-sid"
        assert opened[1] is api.held
        assert globals_["_WINDOWS_WORKER_JOBS"] == [(api, 99)]
        opened[1].close()
        return {"status": "ok", "reason": "none", "events": 7}

    globals_["_refresh_ledger_windows"] = collect
    monkeypatch.setattr(sys, "argv", [str(METER), "refresh", "--json"])
    assert namespace["main"]() == 0
    assert capsys.readouterr().out == (
        '{"coverage":"unknown","reason":"none",'
        '"schema":"cairn-meter-refresh/1","status":"ok"}\n')
    assert api.held.closed


@WINDOWS_ONLY
def test_windows_native_refresh_rebuild_and_exports_use_only_synthetic_profile(
        native_windows_root):
    import hashlib
    import shutil
    import subprocess

    source_root = native_windows_root / "approved-source"
    projects = [native_windows_root / "project-alpha",
                native_windows_root / "project-beta"]
    aliases = ("alpha", "beta")
    remotes = ("https://example.test/team/alpha.git",
               "https://example.test/team/beta.git")
    config = {
        "version": 1, "enabled": True,
        "sources": [{"alias": "codex-source", "tool": "codex",
                     "root": str(source_root)}],
        "projects": [{"alias": alias, "path": str(project), "remote": remote}
                     for alias, project, remote in zip(aliases, projects, remotes)],
    }
    _api, _wrapped, profile = native_windows_status(
        native_windows_root, json.dumps(config).encode("utf-8"))
    native_windows_directory_open_controls(_api, profile, _wrapped.sid)

    # Run the real entry point from an owned runtime tree under the same fresh
    # synthetic root. This keeps helper admission within the fixture's private
    # inherited DACL instead of traversing the checkout's ancestor ACLs.
    runtime_tools = native_windows_root / "runtime" / "tools"
    runtime_tools.mkdir(parents=True)
    runtime_meter = runtime_tools / "meter.py"
    runtime_git_helper = runtime_tools / "git_read.py"
    shutil.copyfile(METER, runtime_meter)
    shutil.copyfile(ROOT / "tools" / "git_read.py", runtime_git_helper)
    for original, copied in ((METER, runtime_meter),
                             (ROOT / "tools" / "git_read.py", runtime_git_helper)):
        assert hashlib.sha256(original.read_bytes()).digest() == hashlib.sha256(
            copied.read_bytes()).digest()
    assert native_windows_root in runtime_tools.parents
    assert runtime_tools != source_root and source_root not in runtime_tools.parents
    assert all(runtime_tools != project and project not in runtime_tools.parents
               for project in projects)

    source_root.mkdir()
    for index, (alias, project, remote) in enumerate(zip(aliases, projects, remotes), 1):
        (project / ".git").mkdir(parents=True)
        (project / ".git" / "config").write_text(
            f'[remote "origin"]\n\turl = {remote}\n', encoding="utf-8")
        (project / "dev").mkdir()
        (project / "dev" / "measurement").mkdir()
        owner = f"019a0000-0000-7000-8000-00000000000{index}"
        turn = f"turn-{alias}"
        owner_rows = [
            row("session_meta", {"id": owner, "session_id": owner,
                                 "source": "cli", "thread_source": "user",
                                 "history_mode": "legacy"}),
            row("turn_context", {"turn_id": turn, "cwd": str(project),
                                 "model": "gpt-5.3-codex"}),
            codex_direct(owner, owner, turn, turn, f"response-{alias}", 20, 20, 20),
        ]
        (source_root / f"session-{alias}.jsonl").write_bytes(
            b"".join(encoded(owner_rows)))
        _claim_id, project_claims = c2_claim_records(owner)
        (project / "dev" / "intents.jsonl").write_bytes(b"".join(encoded(project_claims)))

    wrapper = r'''import runpy, sys
meter_path, synthetic_profile, command = sys.argv[1:]
namespace = runpy.run_path(meter_path, run_name="meter_native_synthetic")
globals_ = namespace["main"].__globals__
real_api = globals_["_WindowsConsentAPI"]
class SyntheticProfileAPI:
    def __init__(self):
        self.api = real_api()
        _actual_profile, self.sid = self.api.current_user_profile()
    def current_user_profile(self):
        return synthetic_profile, self.sid
    def __getattr__(self, name):
        return getattr(self.api, name)
globals_["_WindowsConsentAPI"] = SyntheticProfileAPI
sys.argv = [meter_path, command, "--json"]
raise SystemExit(namespace["main"]())
'''

    def run(command):
        result = subprocess.run(
            [sys.executable, "-c", wrapper, str(runtime_meter), str(profile), command],
            capture_output=True, text=True, check=False, timeout=90)
        assert result.returncode == 0, result.stderr
        assert str(native_windows_root) not in result.stdout + result.stderr
        receipt = json.loads(result.stdout)
        assert receipt == {"schema": "cairn-meter-refresh/1", "status": "ok",
                           "reason": "none", "coverage": "unknown"}

    ledger_path = profile / ".cairn" / "meter" / "ledger.json"
    export_paths = [project / "dev" / "measurement" / "meter.json"
                    for project in projects]
    snapshots = None
    for command in ("refresh", "refresh", "rebuild"):
        run(command)
        ledger_bytes = ledger_path.read_bytes()
        export_bytes = [path.read_bytes() for path in export_paths]
        current = (ledger_bytes, export_bytes)
        if snapshots is None:
            snapshots = current
        else:
            assert current == snapshots

    ledger = json.loads(snapshots[0])
    assert len(ledger["events"]) == 2
    assert {event["project_alias"] for event in ledger["events"]} == set(aliases)
    assert all(event["ownership"] == "proven" for event in ledger["events"])
    assert {mapping["artifact"] for mapping in ledger["mappings"]} == {
        "src/app.py"}
    for alias, path, other_alias in zip(aliases, export_paths, reversed(aliases)):
        exported = json.loads(path.read_bytes())
        assert exported["project_alias"] == alias
        assert {row["events"] for row in exported["aggregates"]} == {1}
        assert all(row["kinds"]["cache_write"] is None
                   for row in exported["aggregates"])
        assert other_alias not in path.read_text(encoding="utf-8")
        assert str(native_windows_root) not in path.read_text(encoding="utf-8")

    # Reopen only the synthetic profile and confirm the durable ledger retained
    # its private native ACL after actual refresh/rebuild publication.
    _profile_path, user_sid = _api.current_user_profile()
    config_bytes, held = _api.read_config(str(profile), user_sid, retain_handles=True)
    assert meter.validate_config_bytes(config_bytes)["enabled"] is True
    try:
        cairn_handle = next(link[2] for link in held.links if link[3] == "cairn")
        meter_handle = _api.open("meter", cairn_handle, directory=True)
        try:
            _api.check_acl(meter_handle, user_sid, "meter")
            ledger_handle = _api.open("ledger.json", meter_handle,
                                      read_data=True, share=7)
            try:
                _api.check_acl(ledger_handle, user_sid, "ledger")
            finally:
                _api.close(ledger_handle)
        finally:
            _api.close(meter_handle)
    finally:
        held.close()


def test_repeated_cumulative_checkpoints_are_not_summed():
    result = meter.reconcile_checkpoints([20, 20, 35], baseline=0)
    assert result == {"deltas": [20, 0, 15], "total": 35, "last_checkpoint": 35}


def test_known_inherited_baseline_is_subtracted_once():
    result = meter.reconcile_checkpoints([100, 130], baseline=100)
    assert result == {"deltas": [0, 30], "total": 30, "last_checkpoint": 130}


def test_checkpoint_partitions_match_full_arithmetic_when_baseline_is_retained():
    whole = meter.reconcile_checkpoints([20, 20, 35], baseline=0)
    first = meter.reconcile_checkpoints([20, 20], baseline=0)
    second = meter.reconcile_checkpoints([35], baseline=first["last_checkpoint"])
    assert first["deltas"] + second["deltas"] == whole["deltas"]
    assert first["total"] + second["total"] == whole["total"]


@pytest.mark.parametrize("checkpoints,baseline", [
    ([100, 130], None), ([20, 19], 0), ([19], 20), ([], 0),
    ([20, None, 35], 0), ([20, True], 0), ([20, "35"], 0),
    ([20, -1], 0), ([20, 2**63], 0), ([20], False), ([20], -1),
    ([20], 2**63), (None, 0),
])
def test_unavailable_invalid_or_decreasing_checkpoint_sequence_is_unknown(checkpoints, baseline):
    assert meter.reconcile_checkpoints(checkpoints, baseline=baseline) is None


@pytest.mark.parametrize("command", [
    ["pytest"], ["pytest", "-q", "tests/test_example.py"],
    ["python", "-m", "pytest"], ["python3", "-m", "pytest", "-q"],
    ["python3.13", "-m", "pytest"],
])
def test_direct_pytest_command_classification(command):
    assert meter.classify_pytest_command(command) == "pytest"


@pytest.mark.parametrize("command", [
    None, [], "pytest", ["sh", "-c", "pytest"], ["python", "script.py"],
    ["python3.13", "-m", "unittest"], ["python2", "-m", "pytest"],
    ["python3.13.1", "-m", "pytest"], ["/usr/bin/pytest"],
    ["pytest", "bad\nsecret"], ["pytest", None], ["pytest", ""],
])
def test_unsupported_pytest_command_classification_is_unknown(command):
    assert meter.classify_pytest_command(command) is None


def test_pytest_classification_returns_no_command_arguments():
    command = ["pytest", "SECRET_BODY"]
    assert "SECRET_BODY" not in json.dumps(meter.classify_pytest_command(command))


def test_test_intervals_use_milliseconds_and_union_overlaps():
    assert meter.union_test_intervals([(1000, 3500)]) == {
        "executions": 1, "execution_ms": 2500, "wall_wait_ms": 2500,
    }
    result = meter.union_test_intervals([(1000, 3500), (3000, 4000), (5000, 6000)])
    assert result == {"executions": 3, "execution_ms": 4500, "wall_wait_ms": 4000}


def test_test_intervals_count_distinct_repeats_and_unordered_nested_intervals():
    result = meter.union_test_intervals([(2000, 3000), (1000, 4000), (2000, 3000)])
    assert result == {"executions": 3, "execution_ms": 5000, "wall_wait_ms": 3000}


def test_test_intervals_touching_and_zero_duration():
    result = meter.union_test_intervals([(0, 0), (0, 1000), (1000, 2000)])
    assert result == {"executions": 3, "execution_ms": 2000, "wall_wait_ms": 2000}


@pytest.mark.parametrize("intervals", [
    None, [], [(1000, None)], [(True, 1000)], [(1000, False)],
    [(1000, "3500")], [(1000, 2.5)], [(-1, 5)], [(5, 4)],
    [(0, 2**63)], [(0, 1), (0, None)], [(1,)], ["bad"],
    [(0, 2**63 - 1), (0, 2**63 - 1)],
])
def test_invalid_test_intervals_are_unknown_without_partial_totals(intervals):
    assert meter.union_test_intervals(intervals) is None


def timing_record(command=None, item_id="item-a", start=1000, end=3500):
    return row("event_msg", {"type": "item_completed",
               "thread_id": "019a0000-0000-7000-8000-000000000001",
               "turn_id": "turn-a", "started_at_ms": start,
               "completed_at_ms": end, "item": {
                   "type": "CommandExecution", "id": item_id,
                   "command": ["pytest", "SECRET-ARG"] if command is None else command,
                   "cwd": "/synthetic/SECRET-PATH", "exit_code": 0,
                   "output": "SECRET-OUTPUT"}})


def test_timing_reader_extracts_only_transient_classification_and_times():
    result = read("codex", codex() + [timing_record()])
    observation, = result["timing_observations"]
    assert observation["classification"] == "pytest"
    assert observation["started_at_ms"] == 1000
    assert observation["completed_at_ms"] == 3500
    assert set(observation) == {"classification", "started_at_ms", "completed_at_ms"}
    assert result["timing_coverage"] == "unknown"
    assert "SECRET" not in json.dumps(result)
    assert "item-a" not in json.dumps(result)


def test_timing_reader_copied_items_remain_observations_not_execution_totals():
    item = timing_record()
    result = read("codex", codex() + [item, copy.deepcopy(item)])
    assert len(result["timing_observations"]) == 2
    assert result["timing_observations"][0] == result["timing_observations"][1]
    assert result["timing_coverage"] == "unknown"
    assert "wall_wait_ms" not in result


def test_timing_reader_shell_wrapper_is_unknown_without_command_retention():
    result = read("codex", codex() + [timing_record(["sh", "-c", "SECRET-COMMAND"])])
    assert result["timing_observations"] == []
    assert "test_command_classification_unknown" in result["issues"]
    assert "SECRET" not in json.dumps(result)


@pytest.mark.parametrize("start,end", [
    (None, 3500), (1000, None), (True, 3500), (1000, "3500"),
    (-1, 3500), (3500, 1000), (1000, 2**63), (2**63 - 2, 2**63 - 1),
])
def test_timing_reader_invalid_endpoints_remain_unknown(start, end):
    result = read("codex", codex() + [timing_record(start=start, end=end)])
    assert result["timing_observations"] == []
    assert result["timing_coverage"] == "unknown"
    assert "invalid_record" in result["issues"]


def test_wait_timing_requires_the_supported_root_context_binding():
    records = codex() + [timing_record()]
    records[1]["payload"]["root_turn_id"] = "foreign-root"
    result = read("codex", records)
    candidate, = result["wait_candidates"]
    assert candidate["ownership"] == "unknown"
    assert candidate["project_association"] == "unknown"
    assert candidate["started_at_ms"] == 1000
    assert "conflicting_binding" in candidate["reasons"]


def test_timing_reader_missing_fields_and_noncommand_items():
    missing = timing_record()
    del missing["payload"]["started_at_ms"]
    result = read("codex", codex() + [missing])
    assert result["timing_observations"] == []
    assert "invalid_record" in result["issues"]
    noncommand = timing_record()
    noncommand["payload"]["item"]["type"] = "Other"
    result = read("codex", codex() + [noncommand])
    assert result["timing_observations"] == []
    assert result["timing_coverage"] == "unknown"


@POSIX_ONLY
def test_wait_rows_bind_dedupe_retain_and_export_sanitized_utc_totals(
        tmp_path, monkeypatch):
    home, source, project, config_path = c2_home(tmp_path)
    owner = "019a0000-0000-7000-8000-000000000001"
    start = int(datetime(2026, 11, 5, 23, 59, 59, tzinfo=timezone.utc).timestamp() * 1000)
    end = start + 2500
    records = [
        row("session_meta", {"id": owner, "session_id": owner, "source": "cli",
                             "thread_source": "user", "history_mode": "legacy"}),
        row("turn_context", {"turn_id": "turn-a", "root_turn_id": "turn-a",
                              "cwd": str(project), "model": "gpt-5.3-codex"}),
        timing_record(item_id="item-a", start=start, end=end),
    ]
    timing = records[-1]["payload"]
    timing["thread_id"] = owner
    timing["turn_id"] = "turn-a"
    for name in ("one.jsonl", "copy.jsonl"):
        (source / name).write_bytes(b"".join(encoded(records)))
    config = meter.validate_config_bytes(config_path.read_bytes())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))
    events, cursors, reasons, forks, conflicts, waits = meter._scan_approved_sources(config, [])
    assert events == [] and not forks and not conflicts
    wait, = waits
    assert wait["classification"] == "pytest"
    assert wait["ownership"] == "proven"
    assert wait["project_alias"] == "sample"
    assert wait["started_at_ms"] == start and wait["completed_at_ms"] == end
    assert len(wait["occurrences"]) == 2
    assert wait["wait_key"] == meter._digest("codex-wait", "codex", owner,
                                              "turn-a", "item-a")
    assert owner not in json.dumps(wait)
    claim = {"claim_key": meter._digest("synthetic-wait-claim"),
             "project_alias": "sample", "tool": "codex",
             "session_digest": meter._short_session_digest(owner),
             "claimed_at": "2026-11-05T23:00:00+00:00",
             "released_at": "2026-11-06T01:00:00+00:00",
             "targets": ["src/app.py"], "confidence": "reliable"}
    prior = meter._load_ledger(None)
    ledger = meter._new_ledger(
        prior, config, events, waits, cursors, [claim],
        [{"alias": "sample", "remote": "https://example.test/team/project.git"}],
        {"captured"}, reasons, forks, conflicts)
    assert meter._load_ledger((json.dumps(ledger) + "\n").encode())["waits"] == waits
    exported = meter._project_export(ledger, config, "sample")
    assert exported["wait"] == {
        "coverage": "unknown",
        "observed": {"executions": 1, "execution_ms": 2500, "wall_wait_ms": 2500},
        "by_day": [
            {"day": "2026-11-05", "executions": 0,
             "execution_ms": 1000, "wall_wait_ms": 1000},
            {"day": "2026-11-06", "executions": 1,
             "execution_ms": 1500, "wall_wait_ms": 1500},
        ],
        "by_artifact": [
            {"day": "2026-11-05", "artifact": "src/app.py", "executions": 0,
             "execution_ms": 1000, "wall_wait_ms": 1000},
            {"day": "2026-11-06", "artifact": "src/app.py", "executions": 1,
             "execution_ms": 1500, "wall_wait_ms": 1500},
        ],
    }
    serialized = json.dumps(exported)
    for secret in (owner, str(home), str(source), str(project), "one.jsonl", "item-a"):
        assert secret not in serialized


def test_v3_ledger_migrates_in_memory_with_persistent_timing_gap():
    current = meter._load_ledger(None)
    legacy = copy.deepcopy(current)
    legacy.pop("waits")
    legacy["schema"] = "cairn-meter-ledger/3"
    legacy["reader_version"] = "cairn-source-readers/3"
    legacy["coverage"]["reasons"] = []
    restored = meter._load_ledger((json.dumps(legacy) + "\n").encode())
    assert restored["schema"] == "cairn-meter-ledger/4"
    assert restored["reader_version"] == "cairn-source-readers/4"
    assert restored["waits"] == []
    assert restored["coverage"]["reasons"] == ["pre_v4_timing_history"]
    invalid = dict(legacy, schema="cairn-meter-ledger/2")
    with pytest.raises(meter.Unavailable):
        meter._load_ledger((json.dumps(invalid) + "\n").encode())


def test_codex_direct_response_not_running_totals_or_checkpoints():
    records = codex()
    records.append(row("event_msg", {"type": "token_count", "info": {
        "total_token_usage": {"input_tokens": 900}}}))
    result = read("codex", records)
    event, = result["events"]
    assert event["kinds"] == {"fresh_input": 12, "cache_read": 8,
                              "cache_write": 0, "output": 4}
    assert set(event) == EVENT_FIELDS
    assert result["coverage"] == "unknown"
    assert "legacy_checkpoint_unreconciled" in result["issues"]


def test_codex_per_turn_cwd_override_does_not_use_initial_or_latest_cwd():
    records = codex()
    second = copy.deepcopy(records[-1])
    second["payload"].update(turn_id="turn-b", root_turn_id="turn-b", response_id="response-b")
    records.extend([row("turn_context", {"turn_id": "turn-b", "cwd": "/synthetic/repo-b"}), second])
    events = read("codex", records)["events"]
    assert len(events) == 2
    assert all(set(event) == EVENT_FIELDS for event in events)


@pytest.mark.parametrize("field,value", [("cached_input_tokens", 21),
                                        ("reasoning_output_tokens", 5),
                                        ("total_tokens", 99),
                                        ("cache_write_input_tokens", 2),
                                        ("cache_write_input_tokens", None)])
def test_codex_inconsistent_or_unproven_cache_semantics_are_unknown(field, value):
    records = codex()
    records[-1]["payload"]["usage"][field] = value
    event, = read("codex", records)["events"]
    assert event["kinds"] == meter._unknown_kinds()
    assert "invalid_record" in event["reasons"]


def test_codex_explicit_zero_cache_write_is_distinct_from_absence():
    records = codex()
    records[-1]["payload"]["usage"]["cache_write_input_tokens"] = 0
    assert read("codex", records)["events"][0]["kinds"]["cache_write"] == 0


def test_codex_canonical_direct_record_and_id_fallback_are_synthetic_only():
    records = codex()
    del records[0]["payload"]["session_id"]
    result = read("codex", records)
    assert result["events"][0]["kinds"] == {
        "fresh_input": 12, "cache_read": 8, "cache_write": 0, "output": 4}
    assert result["identity_coverage"] == result["ownership_coverage"] == "unknown"
    assert result["coverage"] == "unknown"


@pytest.mark.parametrize("change", [
    lambda header: header.update(session_id=None),
    lambda header: header.pop("source"),
    lambda header: header.update(source="recovery"),
    lambda header: header.update(thread_source="subagent"),
    lambda header: header.update(attached_thread=None),
    lambda header: header.update(attached_thread=True),
    lambda header: header.update(history_mode="unknown"),
    lambda header: header.update(history_base=1),
    lambda header: header.update(id="not-a-canonical-uuid"),
])
def test_codex_unproven_header_stays_unattributed(change):
    records = codex()
    change(records[0]["payload"])
    result = read("codex", records)
    assert result["events"] and set(result["events"][0]) == EVENT_FIELDS
    assert result["events"][0]["ownership"] == "unknown"
    assert "conflicting_binding" in result["events"][0]["reasons"]
    assert result["identity_coverage"] == result["ownership_coverage"] == "unknown"


def test_codex_context_root_fallback_and_explicit_root():
    for root in (None, "turn-a"):
        records = codex()
        if root is None:
            records[1]["payload"].pop("root_turn_id", None)
        else:
            records[1]["payload"]["root_turn_id"] = root
        assert read("codex", records)["events"]
    records = codex()
    records[1]["payload"]["root_turn_id"] = "foreign-root"
    event, = read("codex", records)["events"]
    assert event["ownership"] == "unknown"


def test_codex_context_must_precede_response_and_duplicates_must_agree():
    records = codex()
    context = records.pop(1)
    records.append(context)
    event, = read("codex", records)["events"]
    assert event["ownership"] == "unknown"
    records = codex()
    records.append(copy.deepcopy(records[1]))
    assert read("codex", records)["events"]
    records[-1]["payload"]["model"] = "other-model"
    assert "conflicting_turn_context" in read("codex", records)["issues"]


def test_codex_response_dedup_ignores_envelope_timestamp_but_conflicts_on_payload():
    records = codex()
    duplicate = copy.deepcopy(records[-1])
    duplicate["timestamp"] = "2026-11-06T12:00:03Z"
    result = read("codex", records + [duplicate])
    assert len(result["events"]) == 1
    duplicate["payload"]["usage"]["output_tokens"] += 1
    duplicate["payload"]["usage"]["total_tokens"] += 1
    result = read("codex", records + [duplicate])
    event, = result["events"]
    assert event["kinds"] == meter._unknown_kinds()
    assert "conflicting_usage" in event["reasons"]


def test_codex_compaction_markers_are_not_extra_usage_records():
    records = codex()
    marker = row("compacted", {"compaction_response_id": "response-a",
                               "latest_token_usage_record": records[-1]["payload"]})
    result = read("codex", records + [marker])
    assert len(result["events"]) == 1
    assert result["coverage"] == "unknown"
    unmatched = row("compacted", {"compaction_response_id": "background-response"})
    assert read("codex", records + [unmatched])["coverage"] == "unknown"


def test_codex_identical_header_repeats_are_harmless_but_owner_change_is_not():
    records = codex()
    result = read("codex", records[:1] + [copy.deepcopy(records[0])] + records[1:])
    assert result["events"]
    records.insert(1, row("session_meta", {
        "id": "019a0000-0000-7000-8000-000000000002",
        "session_id": "019a0000-0000-7000-8000-000000000002",
        "source": "cli", "history_mode": "legacy"}))
    result = read("codex", records)
    assert result["events"] and result["events"][0]["ownership"] == "unknown"


def test_codex_normalized_events_bind_only_exact_approved_local_projects(monkeypatch, tmp_path):
    source_root = tmp_path / "source"
    project_path = tmp_path / "project"
    source_root.mkdir()
    project_path.mkdir()
    config_value = valid_config(
        sources=[{"alias": "codex-main", "tool": "codex", "root": str(source_root)}],
        projects=[{"alias": "cairn", "path": str(project_path),
                   "remote": "https://user:secret@example.test/org/repo.git?token=x#frag"}],
    )
    del config_value["requested_accounts"]
    config = meter.validate_config_bytes(json.dumps(config_value).encode())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda project, roots: (project["remote"], None))
    records = codex()
    records[1]["payload"].update(cwd=str(project_path), model="synthetic-model")
    event, = meter.read_records("codex", encoded(records), config=config,
                                source_aliases=("codex-main",),
                                source_root=source_root)["events"]
    assert set(event) == EVENT_FIELDS
    assert event["source_aliases"] == ["codex-main"]
    assert event["project_alias"] == "cairn"
    assert event["project_association"] == "current_local_verified"
    assert event["ownership"] == "proven"
    assert event["model"] == "synthetic-model"
    assert event["account"] is None
    assert all(value not in json.dumps(event) for value in (
        str(project_path), "019a0000-0000-7000-8000-000000000001", "turn-a", "response-a"))
    records[0]["payload"]["git"] = {
        "repository_url": "https://example.test/other/repo.git"}
    event, = meter.read_records("codex", encoded(records), config=config,
                                source_aliases=("codex-main",),
                                source_root=source_root)["events"]
    assert event["project_alias"] is None
    assert event["project_association"] == "unknown"
    assert "project_remote_mismatch" in event["reasons"]


def test_requested_account_filter_is_unknown_without_source_account_evidence(monkeypatch, tmp_path):
    source_root, project_path = tmp_path / "source", tmp_path / "project"
    source_root.mkdir()
    project_path.mkdir()
    config = meter.validate_config_bytes(json.dumps(valid_config(
        sources=[{"alias": "codex-main", "tool": "codex", "root": str(source_root)}],
        projects=[{"alias": "cairn", "path": str(project_path),
                   "remote": "https://example.test/org/repo.git"}],
    )).encode())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda project, roots: (project["remote"], None))
    records = codex()
    records[1]["payload"]["cwd"] = str(project_path)
    event, = meter.read_records("codex", encoded(records), config=config,
                                source_aliases=("codex-main",),
                                source_root=source_root)["events"]
    assert event["kinds"] == meter._unknown_kinds()
    assert "account_filter_unproven" in event["reasons"]


def test_event_batches_deduplicate_and_drop_conflicting_time_or_usage():
    first = codex()
    second = copy.deepcopy(first)
    second[-1]["timestamp"] = "2026-11-06T12:00:03Z"
    merged, = meter._merge_event_batches([
        read("codex", first), read("codex", second)])
    assert merged["kinds"]["fresh_input"] == 12
    assert merged["observed_at"] is None
    assert merged["time_coverage"] == "unknown"
    assert "ambiguous_time" in merged["reasons"]
    second[-1]["payload"]["usage"]["output_tokens"] += 1
    second[-1]["payload"]["usage"]["total_tokens"] += 1
    merged, = meter._merge_event_batches([read("codex", first), read("codex", second)])
    assert merged["kinds"] == meter._unknown_kinds()
    assert "conflicting_usage" in merged["reasons"]


def test_retained_partial_usage_survives_identical_rescan_and_json_roundtrip():
    event, = read("codex", codex())["events"]
    event["kinds"]["cache_write"] = None
    event["cache_write_ttl"] = {"five_minute": None, "one_hour": None}
    expected = copy.deepcopy(event["kinds"])

    merged = copy.deepcopy(event)
    meter._merge_retained_event(merged, copy.deepcopy(event))
    assert merged["kinds"] == expected
    assert "conflicting_usage" not in merged["reasons"]

    restored = json.loads(json.dumps(merged))
    meter._merge_retained_event(restored, copy.deepcopy(restored))
    assert restored["kinds"] == expected
    assert "conflicting_usage" not in restored["reasons"]


@pytest.mark.parametrize("difference", ["counter", "ttl"])
def test_retained_usage_conflict_is_sticky_unknown(difference):
    tool, records = (("codex", codex()) if difference == "counter"
                     else ("claude", claude()))
    event, = read(tool, records)["events"]
    prior = copy.deepcopy(event)
    incoming = copy.deepcopy(event)
    if difference == "counter":
        incoming["kinds"]["output"] += 1
    else:
        prior["cache_write_ttl"] = {"five_minute": 1, "one_hour": 1}

    meter._merge_retained_event(prior, incoming)
    assert prior["kinds"] == meter._unknown_kinds()
    assert prior["cache_write_ttl"] == {"five_minute": None, "one_hour": None}
    assert "conflicting_usage" in prior["reasons"]

    meter._merge_retained_event(prior, copy.deepcopy(event))
    assert prior["kinds"] == meter._unknown_kinds()
    assert prior["cache_write_ttl"] == {"five_minute": None, "one_hour": None}
    assert "conflicting_usage" in prior["reasons"]


@POSIX_ONLY
def test_first_publication_canonicalizes_conflicted_binding_and_repeats_stably(
        tmp_path, monkeypatch):
    records = c2_codex_records(tmp_path / "approved-project")
    home, _source, _project, config_path = c2_home(tmp_path, records=records)
    config = meter.validate_config_bytes(config_path.read_bytes())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))
    events, cursors, reasons, proofs, conflicts, waits = meter._scan_approved_sources(
        config, [])
    event, = events
    event["reasons"] = sorted(set(event["reasons"]) | {"conflicting_binding"})
    prior = meter._load_ledger(None)
    _claim_id, claim_rows = c2_claim_records(
        "019a0000-0000-7000-8000-000000000001")
    claims = meter._claim_snapshot("sample", encoded(claim_rows))
    remotes = [{"alias": "sample",
                "remote": "https://example.test/team/project.git"}]

    ledger = meter._new_ledger(prior, config, events, waits, cursors, claims,
        remotes, {"captured"}, reasons, proofs, conflicts)
    published, = ledger["events"]
    assert published["ownership"] == "unknown"
    assert published["project_alias"] is None
    assert published["project_association"] == "unknown"
    assert published["thread_key"] is None
    assert published["session_digest"] is None
    assert published["session_key"] is None
    assert published["turn_key"] is None
    assert published["root_turn_key"] is None
    assert published["model"] is None
    assert "conflicting_binding" in published["reasons"]
    assert ledger["mappings"] == []

    first_bytes = json.dumps(ledger, sort_keys=True, separators=(",", ":")) + "\n"
    restored = meter._load_ledger(first_bytes.encode())
    repeated = meter._new_ledger(restored, config, events, waits, cursors, claims,
        remotes, {"captured"}, reasons, proofs, conflicts)
    repeated_bytes = json.dumps(repeated, sort_keys=True,
                                separators=(",", ":")) + "\n"
    assert repeated_bytes == first_bytes


def test_combined_owner_headers_stay_unassociated_after_ledger_roundtrip(
        tmp_path, monkeypatch):
    source_root = tmp_path / "source"
    source_root.mkdir()
    projects = [tmp_path / "project-a", tmp_path / "project-b"]
    for project in projects:
        project.mkdir()
    config_value = valid_config(
        sources=[{"alias": "codex-main", "tool": "codex",
                  "root": str(source_root)}],
        projects=[{"alias": alias, "path": str(project),
                   "remote": f"https://example.test/team/{alias}.git"}
                  for alias, project in zip(("a", "b"), projects)])
    config = meter.validate_config_bytes(json.dumps(config_value).encode())
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))
    first, second = codex(), codex()
    owner = "019a0000-0000-7000-8000-000000000002"
    second[0]["payload"].update(id=owner, session_id=owner)
    second[1]["payload"].update(turn_id="turn-b", cwd=str(projects[1]))
    second[2]["payload"].update(
        thread_id=owner, session_id=owner, turn_id="turn-b",
        root_turn_id="turn-b", response_id="response-b")
    first[1]["payload"]["cwd"] = str(projects[0])
    scanned = meter.read_records(
        "codex", encoded(first + second), config=config,
        source_aliases=("codex-main",), source_root=source_root)
    assert len(scanned["events"]) == 2
    assert all(event["ownership"] == "unknown"
               and event["project_association"] == "unknown"
               for event in scanned["events"])

    remotes = [{"alias": alias,
                "remote": f"https://example.test/team/{alias}.git"}
               for alias in ("a", "b")]
    ledger = meter._new_ledger(meter._load_ledger(None), config,
        scanned["events"], [], [], [], remotes, {"captured"},
        scanned["issues"], [], [])
    assert ledger["mappings"] == []
    assert all(event["ownership"] == "unknown"
               and event["project_association"] == "unknown"
               and event["project_alias"] is None
               and event["session_digest"] is None
               and event["thread_key"] is None
               for event in ledger["events"])

    first_bytes = json.dumps(ledger, sort_keys=True, separators=(",", ":")) + "\n"
    restored = meter._load_ledger(first_bytes.encode())
    repeated = meter._new_ledger(restored, config, scanned["events"], [], [], [],
        remotes, {"captured"}, scanned["issues"], [], [])
    assert json.dumps(repeated, sort_keys=True, separators=(",", ":")) + "\n" == first_bytes


def test_event_batches_drop_conflicting_project_binding(monkeypatch, tmp_path):
    source_root = tmp_path / "source"
    project_a, project_b = tmp_path / "project-a", tmp_path / "project-b"
    for path in (source_root, project_a, project_b):
        path.mkdir()
    config = meter.validate_config_bytes(json.dumps(valid_config(
        sources=[{"alias": "codex-main", "tool": "codex", "root": str(source_root)}],
        projects=[{"alias": "a", "path": str(project_a), "remote": "https://example.test/a"},
                  {"alias": "b", "path": str(project_b), "remote": "https://example.test/b"}],
    )).encode())
    config["requested_accounts"] = {}
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda project, roots: (project["remote"], None))
    left, right = codex(), codex()
    left[1]["payload"]["cwd"] = str(project_a)
    right[1]["payload"]["cwd"] = str(project_b)
    batches = [meter.read_records("codex", encoded(records), config=config,
                                  source_aliases=("codex-main",), source_root=source_root)
               for records in (left, right)]
    merged, = meter._merge_event_batches(batches)
    assert merged["kinds"]["fresh_input"] == 12
    assert merged["project_alias"] is None
    assert merged["project_association"] == "unknown"
    assert merged["ownership"] == "unknown"
    assert "conflicting_binding" in merged["reasons"]


def test_normalized_event_count_limit_is_fail_closed(monkeypatch):
    records = codex()
    second = copy.deepcopy(records[-1])
    second["payload"].update(turn_id="turn-b", root_turn_id="turn-b",
                             response_id="response-b")
    records.extend([row("turn_context", {"turn_id": "turn-b", "cwd": "/synthetic/repo-b"}),
                    second])
    monkeypatch.setattr(meter, "MAX_NORMALIZED_EVENTS", 1)
    result = read("codex", records)
    assert result["events"] == []
    assert "source_budget_exceeded" in result["issues"]


def test_disabled_or_invalid_config_does_not_iterate_a_source():
    class RefuseIteration:
        def __iter__(self):
            raise AssertionError("source must remain unopened")

    disabled = meter.validate_config_bytes(json.dumps(valid_config(enabled=False)).encode())
    result = meter.read_records("codex", RefuseIteration(), config=disabled)
    assert result["events"] == []
    assert result["issues"] == ["disabled"]
    result = meter.read_records("codex", RefuseIteration(), config={"enabled": True})
    assert result["events"] == []
    assert result["issues"] == ["invalid_record"]


@pytest.mark.parametrize("field", ["turn_token_usage", "thread_token_usage"])
@pytest.mark.parametrize("bad", [True, "1", -1, 2**63, None])
def test_codex_snapshots_are_validated_but_never_counted(field, bad):
    records = codex()
    records[-1]["payload"][field]["input_tokens"] = bad
    event, = read("codex", records)["events"]
    assert event["kinds"] == {"fresh_input": 12, "cache_read": 8,
                              "cache_write": 0, "output": 4}
    assert "snapshot_conflict" in event["reasons"]
    records = codex()
    records[-1]["payload"][field].update(input_tokens=2000, total_tokens=2004)
    assert read("codex", records)["events"][0]["kinds"]["fresh_input"] == 12


@pytest.mark.parametrize("tool,fixture", [("codex", codex), ("claude", claude)])
def test_copied_usage_is_counted_once(tool, fixture):
    records = fixture()
    assert read(tool, records + records) == read(tool, records)


@pytest.mark.parametrize("tool,fixture", [("codex", codex), ("claude", claude)])
def test_conflicting_copies_are_unknown_not_maximized(tool, fixture):
    records = fixture()
    other = copy.deepcopy(records[-1])
    usage = other["payload"]["usage"] if tool == "codex" else other["message"]["usage"]
    usage["output_tokens"] += 1
    if tool == "codex":
        usage["total_tokens"] += 1
    result = read(tool, records + [other, records[-1]])
    event, = result["events"]
    assert event["kinds"] == meter._unknown_kinds()
    assert "conflicting_usage" in event["reasons"]


@pytest.mark.parametrize("field", ["forked_from_id", "parent_thread_id", "history_base",
                                  "forked_from_ordinal_exclusive", "subagent_history_start_ordinal"])
def test_inherited_codex_history_never_gets_a_directory_binding(field):
    records = codex()
    records[0]["payload"][field] = 1
    result = read("codex", records)
    assert set(result["events"][0]) == EVENT_FIELDS
    assert result["events"][0]["ownership"] == "unknown"


@pytest.mark.parametrize("mutation", ["missing_context", "foreign_header", "wrong_thread",
                                     "wrong_session", "wrong_root", "conflicting_context"])
def test_codex_unproven_source_binding(mutation):
    records = codex()
    if mutation == "missing_context":
        del records[1]
    elif mutation == "foreign_header":
        records.append(row("session_meta", {"id": "019a0000-0000-7000-8000-000000000002",
                                             "session_id": "019a0000-0000-7000-8000-000000000002",
                                             "source": "cli", "history_mode": "legacy"}))
    elif mutation == "conflicting_context":
        records.append(row("turn_context", {"turn_id": "turn-a", "cwd": "/synthetic/other"}))
    else:
        field = {"wrong_thread": "thread_id", "wrong_session": "session_id", "wrong_root": "root_turn_id"}[mutation]
        records[-1]["payload"][field] = ("019a0000-0000-7000-8000-000000000002"
                                         if field != "root_turn_id" else "foreign")
    event, = read("codex", records)["events"]
    assert set(event) == EVENT_FIELDS
    assert event["ownership"] == "unknown"


def test_claude_cache_kinds_and_ttl_are_disjoint_not_added_twice():
    records = claude()
    records[0]["message"]["usage"]["cache_creation"] = {
        "ephemeral_5m_input_tokens": 1, "ephemeral_1h_input_tokens": 1}
    event, = read("claude", records)["events"]
    assert event["kinds"] == {"fresh_input": 10, "output": 4, "cache_write": 2, "cache_read": 8}
    assert set(event) == EVENT_FIELDS
    records[0]["message"]["usage"]["cache_creation"]["ephemeral_5m_input_tokens"] = 2
    event, = read("claude", records)["events"]
    assert event["kinds"] == meter._unknown_kinds()


def test_requestless_claude_does_not_guess_lineage_from_directory():
    records = claude()
    del records[0]["requestId"]
    event, = read("claude", records)["events"]
    assert event["ownership"] == "unknown"
    assert event["kinds"]["fresh_input"] == 10


@pytest.mark.parametrize("bad", [True, False, "1", 1.5, -1, 2**63, None])
@pytest.mark.parametrize("tool,fixture", [("codex", codex), ("claude", claude)])
def test_numeric_values_are_exact_bounded_integers(tool, fixture, bad):
    records = fixture()
    usage = records[-1]["payload"]["usage"] if tool == "codex" else records[-1]["message"]["usage"]
    usage["input_tokens"] = bad
    result = read(tool, records)
    event, = result["events"]
    assert event["kinds"] == meter._unknown_kinds()
    assert "invalid_record" in event["reasons"]


@pytest.mark.parametrize("bad", [b'{"type":"assistant","type":"user"}\n',
                                 b'{"x":NaN}\n', b'{"x":Infinity}\n',
                                 b'{}', b'\xff\n', b'[]\n',
                                 b' ' * (meter.MAX_LINE + 1) + b'\n'])
def test_invalid_json_and_partial_or_oversized_lines_are_unknown(bad):
    result = meter.read_records("codex", [bad])
    assert not result["events"]
    assert "invalid_record" in result["issues"]


@pytest.mark.parametrize("timestamp", [STAMP[:-1], "not-time", "2026-11-05", 123, True])
def test_no_invented_observation_time(timestamp):
    records = codex()
    records[-1]["timestamp"] = timestamp
    event, = read("codex", records)["events"]
    assert event["observed_at"] is None
    assert event["time_coverage"] == "unknown"


def test_antigravity_transcript_and_live_payload_do_not_become_billed_usage():
    records = [{"step_index": 1, "source": "agent", "type": "step", "status": "done",
                "created_at": STAMP, "content": {"usage": "SECRET-BODY"}},
               {"conversation_id": "id", "cwd": "/synthetic/repo", "context_window": {
                   "total_input_tokens": 100, "total_output_tokens": 20}}]
    result = read("antigravity", records)
    assert result["events"] == []
    assert "unsupported_usage_contract" in result["issues"]
    assert "SECRET" not in json.dumps(result)


@pytest.mark.parametrize("tool,fixture", [("codex", codex), ("claude", claude)])
def test_outputs_do_not_retain_ids_paths_body_remote_or_configuration(tool, fixture):
    records = fixture()
    records[0]["body"] = "SECRET-BODY"
    records[0]["remote"] = "https://SECRET-CREDENTIAL@example.test/repo"
    records[0]["enabled"] = True
    records[0]["account"] = "SECRET-ACCOUNT"
    text = json.dumps(read(tool, records))
    assert all(secret not in text for secret in (
        "SECRET", "/synthetic", "thread-a", "turn-a", "session-a", "request-a", "message-a"))


def test_empty_batch_keeps_all_sources_unknown():
    for tool in meter.TOOLS:
        result = meter.read_records(tool, [])
        assert result["coverage"] == "unknown"
        assert result["events"] == []


def test_default_cli_is_disabled_and_ignores_home_environment(tmp_path, monkeypatch, capsys):
    account_home = tmp_path / "synthetic-os-home"
    account_home.mkdir(mode=0o700)
    fake_home = tmp_path / "synthetic-home-variable"
    fake_home.mkdir(mode=0o700)
    path = private_home(fake_home)
    write_config(path, valid_config(enabled=True))
    result, captured = run_main_with_synthetic_home(account_home, monkeypatch, capsys,
                                                    fake_home=fake_home)
    assert result == 0
    assert not captured.err
    value = json.loads(captured.out)
    assert value["collection"] == "disabled"
    assert value["usage"] == {tool: "unknown" for tool in meter.TOOLS}
    assert list(account_home.iterdir()) == []


def valid_config(**changes):
    value = {"version": 1, "enabled": True,
             "sources": [{"alias": "codex-main", "tool": "codex", "root": "/synthetic/source"}],
             "projects": [{"alias": "cairn", "path": "/synthetic/project",
                           "remote": "https://user:secret@example.test/org/cairn?token=x#frag"}],
             "requested_accounts": {"codex-main": "acct-test"}}
    value.update(changes)
    return value


def private_home(tmp_path):
    (tmp_path / ".cairn").mkdir(mode=0o700)
    os.chmod(tmp_path / ".cairn", 0o700)
    return tmp_path / ".cairn" / "meter.json"


def write_config(path, value, mode=0o600):
    path.write_text(json.dumps(value), encoding="utf-8")
    os.chmod(path, mode)


def test_closed_config_validates_aliases_paths_and_stripped_remote(tmp_path):
    path = private_home(tmp_path)
    write_config(path, valid_config())
    result = meter.validate_config_bytes(path.read_bytes())
    assert result["enabled"] is True
    assert result["projects"][0]["remote"] == "https://example.test/org/cairn"
    assert result["requested_accounts"] == {"codex-main": "acct-test"}


def test_requested_accounts_filter_is_optional():
    config = valid_config()
    del config["requested_accounts"]
    assert meter.validate_config_bytes(json.dumps(config).encode())["requested_accounts"] == {}


@pytest.mark.parametrize("mutate", [
    lambda c: c.update(spending_policy={"limit": 80}),
    lambda c: c.update(enabled=1),
    lambda c: c.update(version=True),
    lambda c: c.update(sources=[{"alias": "x", "tool": "unknown", "root": "/x"}]),
    lambda c: c.update(sources=[{"alias": "x", "tool": "codex", "root": "../x"}]),
    lambda c: c.update(projects=[{"alias": "x", "path": "/x/../y", "remote": "https://h/x"}]),
    lambda c: c.update(requested_accounts={"unknown": "acct"}),
])
def test_config_rejects_unknown_policy_wrong_types_and_bad_bindings(mutate):
    value = valid_config()
    mutate(value)
    with pytest.raises(meter.Unavailable):
        meter.validate_config_bytes(json.dumps(value).encode())


@pytest.mark.parametrize("raw", [
    b'{"version":1,"version":1}', b'{"version":NaN}', b'{"version":Infinity}',
    b"\xff", b" " * (meter.MAX_CONFIG_BYTES + 1),
])
def test_config_rejects_duplicate_keys_nonfinite_invalid_utf8_and_oversize(raw):
    with pytest.raises(meter.Unavailable):
        meter.validate_config_bytes(raw)


def test_config_accepts_exact_byte_cap_and_rejects_one_byte_over():
    compact = json.dumps(valid_config(), separators=(",", ":")).encode()
    exact = compact + b" " * (meter.MAX_CONFIG_BYTES - len(compact))
    assert len(exact) == meter.MAX_CONFIG_BYTES
    assert meter.validate_config_bytes(exact)["enabled"] is True
    with pytest.raises(meter.Unavailable):
        meter.validate_config_bytes(exact + b" ")


def test_config_rejects_duplicate_aliases(tmp_path):
    path = private_home(tmp_path)
    config = valid_config(sources=[
        {"alias": "same", "tool": "codex", "root": "/one"},
        {"alias": "same", "tool": "claude", "root": "/two"},
    ])
    write_config(path, config)
    with pytest.raises(meter.Unavailable):
        meter.validate_config_bytes(path.read_bytes())


@pytest.mark.parametrize("mode", [0o644, 0o640])
@POSIX_ONLY
def test_config_file_must_be_private(tmp_path, mode):
    path = private_home(tmp_path)
    write_config(path, valid_config(), mode=mode)
    with pytest.raises(meter.Unavailable):
        meter.load_config(path)


@POSIX_ONLY
def test_config_directory_must_be_private_and_link_free(tmp_path):
    path = private_home(tmp_path)
    write_config(path, valid_config())
    os.chmod(path.parent, 0o755)
    with pytest.raises(meter.Unavailable):
        meter.load_config(path)
    path.parent.chmod(0o700)
    path.parent.rename(tmp_path / "real-cairn")
    path.parent.symlink_to(tmp_path / "real-cairn", target_is_directory=True)
    with pytest.raises(meter.Unavailable):
        meter.load_config(path)


@POSIX_ONLY
def test_config_rejects_directory_and_fifo_leaves(tmp_path):
    path = private_home(tmp_path)
    path.mkdir()
    with pytest.raises(meter.Unavailable):
        meter.load_config(path)
    path.rmdir()
    os.mkfifo(path)
    with pytest.raises(meter.Unavailable):
        meter.load_config(path)


@POSIX_ONLY
def test_config_refuses_linked_leaf_and_unverifiable_owner(tmp_path, monkeypatch):
    path = private_home(tmp_path)
    other = tmp_path / "other.json"
    write_config(other, valid_config())
    path.symlink_to(other)
    with pytest.raises(meter.Unavailable):
        meter.load_config(path)
    path.unlink()
    write_config(path, valid_config())
    monkeypatch.setattr(meter.os, "getuid", lambda: -1)
    with pytest.raises(meter.Unavailable):
        meter.load_config(path)


@POSIX_ONLY
def test_private_config_open_revalidates_descriptor_identity(tmp_path, monkeypatch):
    path = private_home(tmp_path)
    write_config(path, valid_config())
    replacement = tmp_path / "replacement.json"
    write_config(replacement, valid_config(enabled=False))
    original_open = meter.os.open
    swapped = False

    def swap_then_open(target, flags, *args, **kwargs):
        nonlocal swapped
        if Path(target).name == path.name and kwargs.get("dir_fd") is not None and not swapped:
            swapped = True
            path.unlink()
            replacement.rename(path)
        return original_open(target, flags, *args, **kwargs)

    monkeypatch.setattr(meter.os, "open", swap_then_open)
    with pytest.raises(meter.Unavailable):
        meter.load_config(path)


@POSIX_ONLY
def test_safe_reader_rejects_escape_links_nonregular_and_partial_lines(tmp_path):
    root = tmp_path / "source"
    root.mkdir()
    (root / "good.jsonl").write_bytes(b'{"synthetic":true}\n')
    assert meter._contained_file(root, "good.jsonl") == b'{"synthetic":true}\n'
    outside = tmp_path / "outside.jsonl"
    outside.write_bytes(b"outside\n")
    (root / "linked.jsonl").symlink_to(outside)
    (root / "linked-dir").symlink_to(tmp_path, target_is_directory=True)
    (root / "partial.jsonl").write_bytes(b"partial")
    (root / "directory").mkdir()
    os.mkfifo(root / "fifo")
    for relative in ("../outside.jsonl", str(outside), "linked.jsonl",
                     "linked-dir/outside.jsonl", "partial.jsonl", "directory", "fifo"):
        with pytest.raises(meter.Unavailable):
            meter._contained_file(root, relative)


@POSIX_ONLY
def test_safe_reader_rejects_oversized_line(tmp_path):
    root = tmp_path / "source"
    root.mkdir()
    (root / "wide.jsonl").write_bytes(b"x" * (meter.MAX_LINE + 1) + b"\n")
    with pytest.raises(meter.Unavailable):
        meter._contained_file(root, "wide.jsonl")


@POSIX_ONLY
def test_safe_reader_open_revalidates_descriptor_identity(tmp_path, monkeypatch):
    root = tmp_path / "source"
    root.mkdir()
    path = root / "sample.jsonl"
    path.write_bytes(b"before\n")
    replacement = root / "replacement.jsonl"
    replacement.write_bytes(b"after\n")
    original_open = meter.os.open
    swapped = False

    def swap_then_open(target, flags, *args, **kwargs):
        nonlocal swapped
        if Path(target).name == path.name and kwargs.get("dir_fd") is not None and not swapped:
            swapped = True
            path.unlink()
            replacement.rename(path)
        return original_open(target, flags, *args, **kwargs)

    monkeypatch.setattr(meter.os, "open", swap_then_open)
    with pytest.raises(meter.Unavailable):
        meter._contained_file(root, "sample.jsonl")


@POSIX_ONLY
def test_fixed_user_home_uses_posix_account_and_equal_uids(tmp_path, monkeypatch):
    account_home = tmp_path / "synthetic-account-home"
    account_home.mkdir(mode=0o700)
    uid = os.getuid()
    monkeypatch.setattr(meter.os, "getuid", lambda: uid)
    monkeypatch.setattr(meter.os, "geteuid", lambda: uid)
    monkeypatch.setattr(meter.pwd, "getpwuid", lambda _uid: SimpleNamespace(
        pw_dir=str(account_home)))
    assert meter._fixed_user_home() == account_home
    monkeypatch.setattr(meter.os, "geteuid", lambda: uid + 1)
    with pytest.raises(meter.Unavailable):
        meter._fixed_user_home()


@POSIX_ONLY
def test_stream_reader_caps_and_partial_tail_invalidate_batch(tmp_path, monkeypatch):
    root = tmp_path / "synthetic-source"
    root.mkdir(mode=0o700)
    file = root / "records.jsonl"
    file.write_bytes(b"one\ntwo\n")
    exact = meter._iter_approved_lines(root, "records.jsonl", budget=8)
    assert list(exact) == [b"one\n", b"two\n"]
    assert exact.terminal_reason is None
    over = meter._iter_approved_lines(root, "records.jsonl", budget=7)
    assert list(over) == []
    assert over.terminal_reason == "source_budget_exceeded"
    monkeypatch.setattr(meter, "MAX_LINE", 5)
    file.write_bytes(b"123456\n")
    oversized = meter._iter_approved_lines(root, "records.jsonl")
    assert list(oversized) == []
    assert oversized.terminal_reason == "source_budget_exceeded"
    monkeypatch.setattr(meter, "MAX_LINE", 1024 * 1024)
    monkeypatch.setattr(meter, "MAX_BATCH_LINES", 1)
    file.write_bytes(b"one\ntwo\n")
    too_many = meter._iter_approved_lines(root, "records.jsonl")
    assert list(too_many) == [b"one\n"]
    assert too_many.terminal_reason == "source_budget_exceeded"
    monkeypatch.setattr(meter, "MAX_BATCH_LINES", 100_000)
    monkeypatch.setattr(meter, "MAX_LINE", 5)
    file.write_bytes(b"1234\n")
    exact_line = meter._iter_approved_lines(root, "records.jsonl")
    assert list(exact_line) == [b"1234\n"]
    assert exact_line.terminal_reason is None
    file.write_bytes(b"12345\n")
    over_line = meter._iter_approved_lines(root, "records.jsonl")
    assert list(over_line) == []
    assert over_line.terminal_reason == "source_budget_exceeded"
    monkeypatch.setattr(meter, "MAX_LINE", 1024 * 1024)
    records = encoded(codex())
    file.write_bytes(b"".join(records)[:-1])
    result = meter.read_records("codex", meter._iter_approved_lines(root, "records.jsonl"))
    assert result["events"] == []
    assert "partial_tail" in result["issues"]
    project = tmp_path / "synthetic-project"
    config = meter.validate_config_bytes(json.dumps(valid_config(
        sources=[{"alias": "codex-main", "tool": "codex", "root": str(root)}],
        projects=[{"alias": "project", "path": str(project),
                   "remote": "https://example.test/org/repo"}],
    )).encode())
    config["requested_accounts"] = {}
    calls = []
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda *_args: calls.append(True) or (None, "project_remote_unavailable"))
    records_value = codex()
    records_value[1]["payload"]["cwd"] = str(project)
    file.write_bytes(b"".join(encoded(records_value))[:-1])
    result = meter.read_records("codex", meter._iter_approved_lines(root, "records.jsonl"),
                                config=config, source_aliases=("codex-main",))
    assert result["events"] == []
    assert calls == []


@POSIX_ONLY
def test_stream_reader_revalidates_open_identity(tmp_path, monkeypatch):
    root = tmp_path / "synthetic-source"
    root.mkdir(mode=0o700)
    path = root / "records.jsonl"
    path.write_bytes(b"before\n")
    replacement = root / "replacement.jsonl"
    replacement.write_bytes(b"after!\n")
    original_open = meter.os.open
    swapped = False

    def swap_then_open(target, flags, *args, **kwargs):
        nonlocal swapped
        if target == "records.jsonl" and kwargs.get("dir_fd") is not None and not swapped:
            swapped = True
            path.unlink()
            replacement.rename(path)
        return original_open(target, flags, *args, **kwargs)

    monkeypatch.setattr(meter.os, "open", swap_then_open)
    stream = meter._iter_approved_lines(root, "records.jsonl")
    assert list(stream) == []
    assert stream.terminal_reason == "source_changed"


@POSIX_ONLY
def test_project_remote_reader_requires_direct_private_layout(tmp_path, monkeypatch):
    project_path = tmp_path / "synthetic-project"
    source_root = tmp_path / "source"
    source_root.mkdir(mode=0o700)
    git_dir = project_path / ".git"
    git_dir.mkdir(parents=True, mode=0o700)
    config = b'[remote "origin"]\nurl = https://example.test/org/repo.git\n'
    (git_dir / "config").write_bytes(config)
    project = {"alias": "repo", "path": str(project_path),
               "remote": "https://user:secret@example.test/org/repo.git?token=x#frag"}
    seen = {}

    def read_config(config_bytes, target, excluded_roots):
        seen["bytes"] = config_bytes
        assert target == str(project_path)
        assert str(project_path) in excluded_roots
        return "https://example.test/org/repo.git", None

    monkeypatch.setattr(meter, "_safe_git_origin", read_config)
    remote, reason = meter._verified_project_remote(project, [str(source_root)])
    assert remote == "https://example.test/org/repo.git"
    assert reason is None
    assert seen["bytes"] == config
    (git_dir / "config").unlink()
    (git_dir / "config").symlink_to(tmp_path / "secret-config")
    (tmp_path / "secret-config").write_bytes(b"secret")
    remote, reason = meter._verified_project_remote(project, [])
    assert remote is None and reason == "project_remote_unavailable"
    (git_dir / "config").unlink()
    (project_path / ".git").rmdir()
    (project_path / ".git").write_text("gitdir: /synthetic/worktree", encoding="utf-8")
    remote, reason = meter._verified_project_remote(project, [])
    assert remote is None and reason == "project_layout_unsupported"


@pytest.mark.parametrize("stdout,reason", [
    (b"https://example.test/org/repo.git\0", None),
    (b"https://example.test/a.git\0https://example.test/b.git\0",
     "project_remote_ambiguous"),
    (b"https://example.test/repo.git", "project_remote_ambiguous"),
    (b"\xff\0", "project_remote_unavailable"),
])
def test_meter_safe_git_adapter_accepts_only_one_bounded_origin(monkeypatch, stdout, reason):
    result = SimpleNamespace(state="completed", returncode=0, stdout=stdout, reason=None)

    class Helper:
        def read_origin_from_config(self, config_bytes, **kwargs):
            assert config_bytes == b"synthetic config"
            assert kwargs["target"] == "/synthetic/project"
            assert kwargs["excluded_roots"] == ("/synthetic/source", "/synthetic/project")
            assert kwargs["timeout"] <= 5.0
            return result

    monkeypatch.setattr(meter, "_verified_git_helper", lambda: Helper())
    remote, actual_reason = meter._safe_git_origin(
        b"synthetic config", "/synthetic/project",
        ("/synthetic/source", "/synthetic/project"))
    assert actual_reason == reason
    if reason is None:
        assert remote == "https://example.test/org/repo.git"
    else:
        assert remote is None


def test_meter_safe_git_adapter_closes_helper_failures(monkeypatch):
    result = SimpleNamespace(state="unavailable", returncode=None, stdout=b"",
                             reason="executable-untrusted")

    class Helper:
        def read_origin_from_config(self, *_args, **_kwargs):
            return result

    monkeypatch.setattr(meter, "_verified_git_helper", lambda: Helper())
    assert meter._safe_git_origin(b"config", "/synthetic/project", [])[1] == "git_untrusted"
    monkeypatch.setattr(meter, "_verified_git_helper", lambda: None)
    assert meter._safe_git_origin(b"config", "/synthetic/project", [])[1] == "git_untrusted"


@POSIX_ONLY
def test_enabled_cli_stops_before_source_or_ledger_io(tmp_path, monkeypatch, capsys):
    cairn = tmp_path / ".cairn"
    cairn.mkdir(mode=0o700)
    os.chmod(cairn, 0o700)
    source = tmp_path / "synthetic-source"
    source.mkdir()
    os.mkfifo(source / "do-not-open")
    ledger_dir = cairn / "meter"
    ledger_dir.mkdir()
    ledger = ledger_dir / "ledger.json"
    ledger.write_text("PRIVATE-SENTINEL", encoding="utf-8")
    write_config(cairn / "meter.json", valid_config(
        sources=[{"alias": "codex-main", "tool": "codex", "root": str(source)}]))
    result, captured = run_main_with_synthetic_home(tmp_path, monkeypatch, capsys)
    assert result == 5
    assert json.loads(captured.out)["collection"] == "unavailable"
    assert "PRIVATE-SENTINEL" not in captured.out + captured.err
    assert ledger.read_text(encoding="utf-8") == "PRIVATE-SENTINEL"


@POSIX_ONLY
def test_disabled_cli_does_not_open_configured_sources_or_ledger(tmp_path, monkeypatch, capsys):
    cairn = tmp_path / ".cairn"
    cairn.mkdir(mode=0o700)
    os.chmod(cairn, 0o700)
    source = tmp_path / "synthetic-source"
    source.mkdir()
    os.mkfifo(source / "do-not-open")
    write_config(cairn / "meter.json", valid_config(enabled=False,
        sources=[{"alias": "codex-main", "tool": "codex", "root": str(source)}]))
    result, captured = run_main_with_synthetic_home(tmp_path, monkeypatch, capsys)
    assert result == 0
    assert json.loads(captured.out)["collection"] == "disabled"


def test_unsupported_privacy_platform_fails_closed_but_missing_config_is_disabled(tmp_path, monkeypatch):
    path = tmp_path / ".cairn" / "meter.json"
    monkeypatch.setattr(meter, "_PRIVATE_FS_SUPPORTED", False)
    assert meter.load_config(path) is None
    path.parent.mkdir()
    path.write_text(json.dumps(valid_config()), encoding="utf-8")
    with pytest.raises(meter.Unavailable):
        meter.load_config(path)
    root = tmp_path / "source"
    root.mkdir()
    (root / "record.jsonl").write_bytes(b"synthetic\n")
    with pytest.raises(meter.Unavailable):
        meter._contained_file(root, "record.jsonl")


def test_session_digest_matches_existing_intent_identity_rule():
    import hashlib

    owner = "  synthetic-owner  "
    expected = hashlib.sha256(b"synthetic-owner").hexdigest()[:8]
    assert meter._short_session_digest(owner) == expected
    event, = read("codex", codex())["events"]
    assert event["session_digest"] == meter._short_session_digest(
        "019a0000-0000-7000-8000-000000000001")
    assert "019a0000-0000-7000-8000-000000000001" not in json.dumps(event)
    assert meter._short_session_digest("  ") is None


def test_claim_snapshot_retains_only_hashed_claim_and_safe_targets():
    owner = "synthetic-owner"
    claim_id, rows = c2_claim_records(owner)
    rows[0]["files"] = ["src/app.py", "/outside/SECRET", "../escape", "safe\nsecret"]
    claims = meter._claim_snapshot("sample", encoded(rows))
    claim, = claims
    assert claim["tool"] == "codex"
    assert claim["session_digest"] == meter._short_session_digest(owner)
    assert claim["targets"] == ["src/app.py"]
    assert claim["confidence"] == "ambiguous"
    assert claim["released_at"] == "2026-11-05T13:00:00Z"
    assert claim_id not in json.dumps(claim)
    assert "SECRET" not in json.dumps(claim)


@POSIX_ONLY
def test_refresh_persists_normalized_history_and_claims_without_raw_inputs(
        tmp_path, monkeypatch):
    owner = "019a0000-0000-7000-8000-000000000001"
    claim_id, claim_rows = c2_claim_records(owner)
    records = c2_codex_records(tmp_path / "approved-project")
    home, source, project, _config_path = c2_home(
        tmp_path, records=records, claims=claim_rows)
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))

    result = meter._refresh_ledger(home)

    ledger_path = home / ".cairn" / "meter" / "ledger.json"
    raw = ledger_path.read_bytes()
    ledger = meter._load_ledger(raw)
    event, = ledger["events"]
    claim, = ledger["claims"]
    mapping, = ledger["mappings"]
    assert result == {"status": "written", "reason": "none", "events": 1,
                      "claims": 1, "coverage": "unknown"}
    assert event["session_digest"] == meter._short_session_digest(owner)
    assert event["project_alias"] == "sample"
    assert event["kinds"] == {"fresh_input": 12, "cache_read": 8,
                              "cache_write": 0, "output": 4}
    assert claim["claim_key"] != claim_id
    assert claim["targets"] == ["src/app.py"]
    assert mapping == {"event_key": event["event_key"],
                       "claim_key": claim["claim_key"],
                       "artifact": "src/app.py", "confidence": "reliable"}
    assert ledger["aggregates"][0]["kinds"] == event["kinds"]
    for secret in (owner, claim_id, "SECRET-ACTION", "SECRET-STEM", "SECRET-COMMIT",
                   str(home), str(source), str(project), "session.jsonl"):
        assert secret.encode() not in raw
    assert (home / ".cairn" / "meter" / "ledger.lock").stat().st_size == 0
    assert (home / ".cairn" / "meter" / "ledger.lock").stat().st_mode & 0o777 == 0o600
    assert ledger_path.stat().st_mode & 0o777 == 0o600
    assert ledger_path.stat().st_nlink == 1


@POSIX_ONLY
def test_project_export_contains_only_sanitized_project_aggregates(
        tmp_path, monkeypatch):
    home, source, project, config_path = c2_home(tmp_path)
    owner = "019a0000-0000-7000-8000-000000000001"
    claim_id, claim_rows = c2_claim_records(owner)
    (project / "dev" / "intents.jsonl").write_bytes(b"".join(encoded(claim_rows)))
    records = c2_codex_records(project)
    (source / "session.jsonl").write_bytes(b"".join(encoded(records)))
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))

    assert meter._refresh_ledger(home)["status"] == "written"
    ledger_path = home / ".cairn" / "meter" / "ledger.json"
    config_value = json.loads(config_path.read_text(encoding="utf-8"))
    config_value["projects"].append({
        "alias": "other", "path": "/synthetic/other-project",
        "remote": "https://example.test/team/other.git"})
    config = meter.validate_config_bytes(json.dumps(config_value).encode())
    ledger = meter._load_ledger(ledger_path.read_bytes())
    other = dict(ledger["events"][0])
    other["event_key"] = meter._digest("synthetic-other-project")
    other["project_alias"] = "other"
    ledger["events"].append(other)
    ledger["aggregates"] = meter._recompute_aggregates(ledger["events"], config)
    export = meter._project_export(ledger, config, "sample")
    assert set(export) == {
        "schema", "project_alias", "ratio_version", "aggregates", "wait", "coverage"}
    row, = export["aggregates"]
    assert len(export["aggregates"]) == 1
    assert row["artifact"] == "src/app.py"
    assert row["tool"] == "codex"
    assert row["kinds"] == {
        "fresh_input": 12, "cache_read": 8, "cache_write": 0, "output": 4}
    assert export["ratio_version"] == "cairn-api-token-index/2026-11-06"
    assert export["schema"] == "cairn-meter-project/2"
    assert export["wait"] == {"coverage": "unknown", "observed": None,
                               "by_day": [], "by_artifact": []}
    serialized = json.dumps(export)
    for secret in (owner, claim_id, str(home), str(source), str(project),
                   "other-project", "session.jsonl", "session_digest",
                   "event_key", "cursor"):
        assert secret not in serialized


@POSIX_ONLY
def test_public_refresh_repeat_and_rebuild_publish_distinct_project_exports(
        tmp_path, monkeypatch, capsys):
    home, source, alpha, config_path = c2_home(tmp_path)
    beta = tmp_path / "approved-project-beta"
    beta.mkdir()
    (beta / ".git").mkdir()
    (beta / ".git" / "config").write_text(
        '[remote "origin"]\n\turl = https://example.test/team/beta.git\n',
        encoding="utf-8")
    (beta / "dev").mkdir()
    (beta / "dev" / "measurement").mkdir()
    beta_alias = "beta"
    alpha_owner = "019a0000-0000-7000-8000-000000000011"
    beta_owner = "019a0000-0000-7000-8000-000000000022"
    _alpha_claim_id, alpha_claims = c2_claim_records(alpha_owner)
    _beta_claim_id, beta_claims = c2_claim_records(beta_owner)
    (alpha / "dev" / "intents.jsonl").write_bytes(b"".join(encoded(alpha_claims)))
    (beta / "dev" / "intents.jsonl").write_bytes(b"".join(encoded(beta_claims)))
    alpha_records = c2_bound_records(alpha, alpha_owner, "turn-alpha", 10,
                                     [("alpha-test", 1000)])
    beta_records = c2_bound_records(beta, beta_owner, "turn-beta", 30,
                                    [("beta-test", 3000)])
    (source / "alpha.jsonl").write_bytes(b"".join(encoded(alpha_records)))
    (source / "beta.jsonl").write_bytes(b"".join(encoded(beta_records)))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["projects"] = [
        {"alias": "sample", "path": str(alpha),
         "remote": "https://example.test/team/project.git"},
        {"alias": beta_alias, "path": str(beta),
         "remote": "https://example.test/team/beta.git"},
    ]
    config_path.write_text(json.dumps(config), encoding="utf-8")
    config_path.chmod(0o600)

    def verified_remote(project, _roots, **_kwargs):
        return project["remote"], None

    exports = [alpha / "dev" / "measurement" / "meter.json",
               beta / "dev" / "measurement" / "meter.json"]
    snapshots = None
    for command in ("refresh", "refresh", "rebuild"):
        code, captured = _run_synthetic_meter_command(
            home, monkeypatch, capsys, command, verified_remote)
        assert code == 0
        assert json.loads(captured.out) == {
            "schema": "cairn-meter-refresh/1", "status": "ok",
            "reason": "none", "coverage": "unknown"}
        assert captured.err == ""
        current = tuple(path.read_bytes() for path in exports)
        if snapshots is None:
            snapshots = current
        else:
            assert current == snapshots

    ledger_path = home / ".cairn" / "meter" / "ledger.json"
    ledger_raw = ledger_path.read_bytes()
    ledger = meter._load_ledger(ledger_raw)
    assert len(ledger["events"]) == 2
    exported_alpha, exported_beta = (json.loads(raw) for raw in snapshots)
    assert exported_alpha["project_alias"] == "sample"
    assert exported_beta["project_alias"] == beta_alias
    alpha_aggregate, = exported_alpha["aggregates"]
    beta_aggregate, = exported_beta["aggregates"]
    assert alpha_aggregate["kinds"]["fresh_input"] == 10
    assert beta_aggregate["kinds"]["fresh_input"] == 30
    assert exported_alpha["wait"]["observed"] == {
        "executions": 1, "execution_ms": 1000, "wall_wait_ms": 1000}
    assert exported_beta["wait"]["observed"] == {
        "executions": 1, "execution_ms": 3000, "wall_wait_ms": 3000}
    assert {row["artifact"] for row in exported_alpha["wait"]["by_artifact"]} == {
        "src/app.py"}
    assert {row["artifact"] for row in exported_beta["wait"]["by_artifact"]} == {
        "src/app.py"}
    for raw in snapshots:
        text = raw.decode("ascii")
        for secret in (str(home), str(source), str(alpha), str(beta),
                       alpha_owner, beta_owner, "response-turn-alpha",
                       "response-turn-beta", "SECRET"):
            assert secret not in text
    assert str(beta) not in snapshots[0].decode("ascii")
    assert str(alpha) not in snapshots[1].decode("ascii")
    assert str(home).encode() not in ledger_raw


@POSIX_ONLY
@pytest.mark.parametrize("binding_change", ["unchanged", "changed", "missing"])
def test_retained_wait_binding_is_sticky_across_refresh_and_rebuild(
        tmp_path, monkeypatch, capsys, binding_change):
    owner = "019a0000-0000-7000-8000-000000000033"
    records = c2_bound_records(tmp_path / "approved-project", owner, "turn-retained",
                               12, [("old-item", 2500)])
    _claim_id, claims = c2_claim_records(owner)
    home, source, project, config_path = c2_home(tmp_path, claims=claims)
    session_path = source / "session.jsonl"
    session_path.write_bytes(b"".join(encoded(records)))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    original_remote = config["projects"][0]["remote"]
    changed_remote = "https://example.test/team/renamed.git"
    remote_state = {"available": True}

    def verified_remote(item, _roots, **_kwargs):
        if not remote_state["available"]:
            return None, "project_remote_unavailable"
        return item["remote"], None

    def run(command):
        return _run_synthetic_meter_command(
            home, monkeypatch, capsys, command, verified_remote)

    code, captured = run("refresh")
    assert code == 0 and json.loads(captured.out)["status"] == "ok"
    ledger_path = home / ".cairn" / "meter" / "ledger.json"
    export_path = project / "dev" / "measurement" / "meter.json"
    old_export = export_path.read_bytes()
    initial = meter._load_ledger(ledger_path.read_bytes())
    old_wait, = initial["waits"]
    assert old_wait["project_alias"] == "sample"
    assert old_wait["project_association"] == "current_local_verified"

    session_path.unlink()
    if binding_change == "changed":
        config["projects"][0]["remote"] = changed_remote
        config_path.write_text(json.dumps(config), encoding="utf-8")
        config_path.chmod(0o600)
    elif binding_change == "missing":
        remote_state["available"] = False

    code, captured = run("refresh")
    middle_receipt = json.loads(captured.out)
    if binding_change == "missing":
        assert code == 5
        assert middle_receipt == {
            "schema": "cairn-meter-refresh/1", "status": "unavailable",
            "reason": "project_remote_unavailable", "coverage": "unknown"}
        assert export_path.read_bytes() == old_export
        invalidated = meter._load_ledger(ledger_path.read_bytes())["waits"]
        wait = next(item for item in invalidated if item["wait_key"] == old_wait["wait_key"])
        assert wait["project_alias"] is None
        assert wait["project_association"] == "unknown"
        assert "project_path_unapproved" in wait["reasons"]
    else:
        assert code == 0
        assert middle_receipt == {
            "schema": "cairn-meter-refresh/1", "status": "ok",
            "reason": "none", "coverage": "unknown"}
        retained = meter._load_ledger(ledger_path.read_bytes())["waits"]
        wait = next(item for item in retained if item["wait_key"] == old_wait["wait_key"])
        if binding_change == "unchanged":
            assert wait["project_alias"] == "sample"
            assert wait["project_association"] == "current_local_verified"
        else:
            assert wait["project_alias"] is None
            assert wait["project_association"] == "unknown"
            assert "project_remote_mismatch" in wait["reasons"]

    if binding_change == "changed":
        config["projects"][0]["remote"] = original_remote
        config_path.write_text(json.dumps(config), encoding="utf-8")
        config_path.chmod(0o600)
    remote_state["available"] = True
    code, captured = run("refresh")
    assert code == 0
    assert json.loads(captured.out) == {
        "schema": "cairn-meter-refresh/1", "status": "ok",
        "reason": "none", "coverage": "unknown"}
    replay = c2_bound_records(project, owner, "turn-retained", 12,
                              [("old-item", 2500), ("new-item", 4000)])
    session_path.write_bytes(b"".join(encoded(replay)))
    code, captured = run("rebuild")
    assert code == 0
    assert json.loads(captured.out) == {
        "schema": "cairn-meter-refresh/1", "status": "ok",
        "reason": "none", "coverage": "unknown"}

    raw = ledger_path.read_bytes()
    ledger = meter._load_ledger(raw)
    assert meter._load_ledger(raw)["waits"] == ledger["waits"]
    waits_by_key = {item["wait_key"]: item for item in ledger["waits"]}
    old_key = meter._digest("codex-wait", "codex", owner,
                            "turn-retained", "old-item")
    new_key = meter._digest("codex-wait", "codex", owner,
                            "turn-retained", "new-item")
    old_final, new_final = waits_by_key[old_key], waits_by_key[new_key]
    if binding_change == "unchanged":
        assert old_final["project_alias"] == "sample"
        assert old_final["project_association"] == "current_local_verified"
    else:
        assert old_final["project_alias"] is None
        assert old_final["project_association"] == "unknown"
        assert "conflicting_binding" in old_final["reasons"]
    assert new_final["project_alias"] == "sample"
    assert new_final["project_association"] == "current_local_verified"
    assert new_final["ownership"] == "proven"
    exported = json.loads(export_path.read_bytes())
    assert exported["wait"]["observed"] == {
        "executions": 2 if binding_change == "unchanged" else 1,
        "execution_ms": 6500 if binding_change == "unchanged" else 4000,
        "wall_wait_ms": 4000,
    }
    artifact_rows = exported["wait"]["by_artifact"]
    assert sum(item["executions"] for item in artifact_rows) == (
        2 if binding_change == "unchanged" else 1)


@POSIX_ONLY
@pytest.mark.parametrize("layout", ["missing", "dev-link", "measurement-link"])
def test_posix_project_export_refuses_missing_or_linked_parents(
        tmp_path, monkeypatch, layout):
    home, _source, project, _config_path = c2_home(tmp_path)
    dev = project / "dev"
    measurement = dev / "measurement"
    outside = tmp_path / "outside-project-output"
    outside.mkdir()
    outside_export = outside / "meter.json"
    outside_export.write_bytes(b"outside export\n")
    external_target = outside_export
    if layout == "missing":
        measurement.rmdir()
    elif layout == "dev-link":
        moved = project / "dev-original"
        dev.rename(moved)
        outside_dev = outside / "dev"
        outside_dev.mkdir()
        (outside_dev / "measurement").mkdir()
        external_target = outside_dev / "measurement" / "meter.json"
        external_target.write_bytes(outside_export.read_bytes())
        dev.symlink_to(outside_dev, target_is_directory=True)
    else:
        measurement.rename(dev / "measurement-original")
        measurement.symlink_to(outside, target_is_directory=True)

    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))
    monkeypatch.setattr(meter, "_capture_project_claims",
                        lambda _project: ([], "captured"))
    result = meter._refresh_ledger(home)

    assert result["status"] == "unavailable"
    assert result["reason"] == "project_export_unavailable"
    assert external_target.read_bytes() == b"outside export\n"
    if not measurement.is_symlink():
        assert not list((dev / "measurement").glob(".meter-*.tmp"))


@POSIX_ONLY
@pytest.mark.parametrize("leaf", ["symlink", "hardlink", "permissive"])
def test_posix_project_export_refuses_unsafe_existing_export(
        tmp_path, monkeypatch, leaf):
    home, _source, project, _config_path = c2_home(tmp_path)
    target = project / "dev" / "measurement" / "meter.json"
    outside = tmp_path / "outside-meter.json"
    outside.write_bytes(b"outside export\n")
    outside.chmod(0o600)
    if leaf == "symlink":
        target.symlink_to(outside)
    elif leaf == "hardlink":
        os.link(outside, target)
    else:
        target.write_bytes(b"permissive old export\n")
        target.chmod(0o644)
    original = outside.read_bytes() if leaf in {"symlink", "hardlink"} else target.read_bytes()
    original_mode = target.lstat().st_mode

    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))
    result = meter._refresh_ledger(home)

    assert result["status"] == "unavailable"
    assert result["reason"] == "project_export_unavailable"
    if leaf in {"symlink", "hardlink"}:
        assert outside.read_bytes() == original
        if leaf == "symlink":
            assert target.is_symlink() and target.resolve() == outside
        else:
            assert target.stat().st_ino == outside.stat().st_ino
    else:
        assert target.read_bytes() == original
        assert target.stat().st_mode == original_mode
    assert not list(target.parent.glob(".meter-*.tmp"))


@POSIX_ONLY
@pytest.mark.parametrize("substitution", [
    "dev-parent", "measurement-parent", "old-leaf", "candidate",
    "config", "remote",
])
def test_posix_project_export_detects_substitution_before_publication(
        tmp_path, monkeypatch, substitution):
    home, _source, project, config_path = c2_home(tmp_path)
    measurement = project / "dev" / "measurement"
    old_export = measurement / "meter.json"
    old_export.write_bytes(b"old export\n")
    old_export.chmod(0o600)
    replacement_bytes = b"unowned replacement\n"
    call = {"count": 0}

    def verified_remote(item, _roots):
        call["count"] += 1
        if call["count"] == 4:
            if substitution == "dev-parent":
                moved = project / "dev-original"
                (project / "dev").rename(moved)
                external_dev = tmp_path / "external-dev"
                external_dev.mkdir()
                (external_dev / "measurement").mkdir()
                (external_dev / "measurement" / "meter.json").write_bytes(
                    b"external sentinel\n")
                (project / "dev").symlink_to(external_dev, target_is_directory=True)
            elif substitution == "measurement-parent":
                moved = project / "dev" / "measurement-original"
                measurement.rename(moved)
                external_measurement = tmp_path / "external-measurement"
                external_measurement.mkdir()
                (external_measurement / "meter.json").write_bytes(
                    b"external sentinel\n")
                measurement.symlink_to(external_measurement, target_is_directory=True)
            elif substitution == "old-leaf":
                old_export.unlink()
                old_export.write_bytes(replacement_bytes)
                old_export.chmod(0o600)
            elif substitution == "candidate":
                candidate = next(measurement.glob(".meter-*.tmp"))
                candidate.unlink()
                candidate.write_bytes(replacement_bytes)
                candidate.chmod(0o600)
            elif substitution == "config":
                config_path.write_bytes(b"changed config sentinel\n")
            elif substitution == "remote":
                return "https://example.test/team/substituted.git", None
        return item["remote"], None

    monkeypatch.setattr(meter, "_verified_project_remote", verified_remote)
    result = meter._refresh_ledger(home)

    assert call["count"] == 4
    assert result["status"] == "unavailable"
    assert result["reason"] in {
        "source_changed", "project_remote_mismatch", "project_export_unavailable"}
    if substitution == "old-leaf":
        assert old_export.read_bytes() == replacement_bytes
    elif substitution == "candidate":
        candidates = list(measurement.glob(".meter-*.tmp"))
        assert len(candidates) == 1
        assert candidates[0].read_bytes() == replacement_bytes
        assert old_export.read_bytes() == b"old export\n"
    elif substitution == "config":
        assert config_path.read_bytes() == b"changed config sentinel\n"
        assert old_export.read_bytes() == b"old export\n"
    elif substitution == "remote":
        assert result["reason"] == "project_remote_mismatch"
        assert old_export.read_bytes() == b"old export\n"
    elif substitution == "dev-parent":
        assert (tmp_path / "external-dev" / "measurement" / "meter.json").read_bytes() == (
            b"external sentinel\n")
        assert (project / "dev-original" / "measurement" / "meter.json").read_bytes() == (
            b"old export\n")
    else:
        assert (tmp_path / "external-measurement" / "meter.json").read_bytes() == (
            b"external sentinel\n")
        assert (project / "dev" / "measurement-original" / "meter.json").read_bytes() == (
            b"old export\n")


@POSIX_ONLY
@pytest.mark.parametrize("fault", [
    "short-write", "zero-write", "replace", "cleanup", "post-flush",
])
def test_posix_project_export_write_failures_preserve_or_report_state(
        tmp_path, monkeypatch, fault):
    home, _source, project, _config_path = c2_home(tmp_path)
    target = project / "dev" / "measurement" / "meter.json"
    target.write_bytes(b"old export\n")
    target.chmod(0o600)
    original_write = os.write
    original_replace = os.replace
    original_unlink = os.unlink
    original_fsync = os.fsync

    def arm():
        if fault in {"short-write", "zero-write", "cleanup"}:
            def injected_write(fd, data):
                if fault == "short-write":
                    return original_write(fd, data[:7])
                return 0
            monkeypatch.setattr(meter.os, "write", injected_write)
        if fault == "replace":
            def injected_replace(source, destination, **kwargs):
                if str(source).startswith(".meter-"):
                    raise OSError("synthetic replace refusal")
                return original_replace(source, destination, **kwargs)
            monkeypatch.setattr(meter.os, "replace", injected_replace)
        if fault == "cleanup":
            def injected_unlink(path, *args, **kwargs):
                if str(path).startswith(".meter-"):
                    raise OSError("synthetic cleanup refusal")
                return original_unlink(path, *args, **kwargs)
            monkeypatch.setattr(meter.os, "unlink", injected_unlink)
        if fault == "post-flush":
            def injected_fsync(fd):
                if stat.S_ISDIR(os.fstat(fd).st_mode):
                    raise OSError("synthetic post-publication directory flush refusal")
                return original_fsync(fd)
            monkeypatch.setattr(meter.os, "fsync", injected_fsync)

    _arm_after_ledger_commit(monkeypatch, arm)
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))
    result = meter._refresh_ledger(home)

    if fault == "short-write":
        assert result["status"] == "written"
        exported = json.loads(target.read_bytes())
        assert exported["schema"] == "cairn-meter-project/2"
        assert not list(target.parent.glob(".meter-*.tmp"))
    elif fault == "post-flush":
        assert result["status"] == "unavailable"
        assert result["reason"] == "project_export_uncertain"
        assert json.loads(target.read_bytes())["schema"] == "cairn-meter-project/2"
        assert not list(target.parent.glob(".meter-*.tmp"))
    else:
        assert result["status"] == "unavailable"
        assert result["reason"] == "project_export_unavailable"
        assert target.read_bytes() == b"old export\n"
        if fault == "cleanup":
            candidates = list(target.parent.glob(".meter-*.tmp"))
            assert len(candidates) == 1 and candidates[0].stat().st_size == 0
        else:
            assert not list(target.parent.glob(".meter-*.tmp"))


@POSIX_ONLY
def test_posix_project_export_postrename_recheck_failure_is_uncertain(
        tmp_path, monkeypatch):
    home, _source, project, _config_path = c2_home(tmp_path)
    target = project / "dev" / "measurement" / "meter.json"
    target.write_bytes(b"old export\n")
    target.chmod(0o600)
    calls = {"count": 0}

    def verified_remote(item, _roots):
        calls["count"] += 1
        if calls["count"] == 5:
            return "https://example.test/team/substituted.git", None
        return item["remote"], None

    monkeypatch.setattr(meter, "_verified_project_remote", verified_remote)
    result = meter._refresh_ledger(home)

    assert calls["count"] == 5
    assert result == {"status": "unavailable", "reason": "project_export_uncertain",
                      "coverage": "unknown"}
    assert json.loads(target.read_bytes())["schema"] == "cairn-meter-project/2"
    assert not list(target.parent.glob(".meter-*.tmp"))


@POSIX_ONLY
def test_public_refresh_closes_failed_project_publication_receipt(
        tmp_path, monkeypatch, capsys):
    home, _source, project, _config_path = c2_home(tmp_path)
    (project / "dev" / "measurement").rmdir()
    verified_remote = lambda item, _roots, **_kwargs: (item["remote"], None)

    code, captured = _run_synthetic_meter_command(
        home, monkeypatch, capsys, "refresh", verified_remote)

    assert code == 5
    assert json.loads(captured.out) == {
        "schema": "cairn-meter-refresh/1", "status": "unavailable",
        "reason": "project_export_unavailable", "coverage": "unknown"}
    assert captured.err == ""
    assert (home / ".cairn" / "meter" / "ledger.json").is_file()


@POSIX_ONLY
def test_copied_legacy_fork_reconciles_direct_usage_and_retains_lineage_proof(
        tmp_path, monkeypatch):
    _home, config, scan = scan_fork_files(tmp_path, monkeypatch)
    events, cursors, reasons, proofs, conflicts, _waits = scan
    assert len(events) == 2
    assert len(proofs) == 1 and not conflicts
    parent_key = meter._digest("codex", "019a0000-0000-7000-8000-000000000011")
    parent = next(event for event in events if event["thread_key"] == parent_key)
    child = next(event for event in events if event["thread_key"] != parent_key)
    assert parent["ownership"] == child["ownership"] == "proven"
    assert child["lineage_key"] is not None
    assert parent["lineage_key"] is None
    assert child["kinds"] == {
        "fresh_input": 30, "cache_read": 0, "cache_write": None, "output": 0}
    assert parent["kinds"] == {
        "fresh_input": 100, "cache_read": 0, "cache_write": None, "output": 0}
    assert parent["kinds"]["fresh_input"] + child["kinds"]["fresh_input"] == 130
    prior = meter._load_ledger(None)
    ledger = meter._new_ledger(prior, config, events, _waits, cursors, [],
        [{"alias": "sample", "remote": "https://example.test/team/project.git"}],
        {"captured"}, reasons, proofs, conflicts)
    restored = meter._load_ledger(
        (json.dumps(ledger, sort_keys=True, separators=(",", ":")) + "\n").encode())
    assert restored["ratio_version"] == "cairn-api-token-index/2026-11-06"
    assert restored["ratio_index"] == meter._RATIO_INDEX
    lineage, = restored["lineages"]
    assert lineage["state"] == "verified"
    assert lineage["proofs"][0]["parent_terminal"]["thread_snapshot"]["fresh_input"] == 100
    assert lineage["proofs"][0]["child_sequence"][-1]["thread_snapshot"]["fresh_input"] == 130
    assert restored["aggregates"][0]["kinds"]["cache_write"] is None
    assert restored["coverage"]["global"] == "unknown"
    repeated = meter._new_ledger(restored, config, events, _waits, cursors, [],
        [{"alias": "sample", "remote": "https://example.test/team/project.git"}],
        {"captured"}, reasons, proofs, conflicts)
    repeated_bytes = json.dumps(repeated, sort_keys=True, separators=(",", ":")) + "\n"
    assert repeated_bytes == json.dumps(restored, sort_keys=True,
                                        separators=(",", ":")) + "\n"
    assert sum(event["kinds"]["fresh_input"] for event in repeated["events"]) == 130


@POSIX_ONLY
@pytest.mark.parametrize("mutation", [
    "changed_copied_usage", "missing_marker", "changed_child_snapshot", "changed_child_root",
])
def test_unproven_copied_fork_keeps_child_usage_unattributed(
        tmp_path, monkeypatch, mutation):
    def mutate(rows):
        if mutation == "changed_copied_usage":
            rows[3]["payload"]["usage"]["input_tokens"] = 101
            rows[3]["payload"]["usage"]["total_tokens"] = 101
        elif mutation == "missing_marker":
            del rows[4]
        elif mutation == "changed_child_snapshot":
            rows[-1]["payload"]["thread_token_usage"]["input_tokens"] = 131
            rows[-1]["payload"]["thread_token_usage"]["total_tokens"] = 131
        elif mutation == "changed_child_root":
            rows[-2]["payload"]["root_turn_id"] = "foreign-root"
            rows[-1]["payload"]["root_turn_id"] = "foreign-root"

    _home, _config, scan = scan_fork_files(tmp_path, monkeypatch, child_mutation=mutate)
    events, _cursors, _reasons, proofs, conflicts, _waits = scan
    child = next(event for event in events if event["thread_key"] !=
                 meter._digest("codex", "019a0000-0000-7000-8000-000000000011"))
    assert child["ownership"] == "unknown"
    assert child["project_association"] == "unknown"
    assert child["lineage_key"] is None
    assert not proofs
    assert conflicts


def test_dated_reference_index_is_exact_and_not_actual_spend():
    index = meter._RATIO_INDEX
    assert index["version"] == "cairn-api-token-index/2026-11-06"
    assert index["reference_model"] == "claude-haiku-4-5-20251001"
    assert index["currency"] == "USD"
    assert index["denominator_tokens"] == 1_000_000
    assert index["models"]["claude-sonnet-4-6"] == {
        "fresh_input": [3, 1], "cache_read": [3, 10], "output": [15, 1],
        "cache_write_5m": [15, 4], "cache_write_1h": [6, 1],
    }
    assert index["models"]["claude-opus-5-5"]["cache_read"] == [1, 5]
    assert index["models"]["gpt-5.3-codex"]["cache_write_5m"] is None
    assert len(index["sources"]) == 5


def test_reference_index_uses_source_reported_cache_ttl_and_keeps_unknown_partial():
    records = claude()
    records[-1]["message"]["model"] = "claude-sonnet-4-6"
    records[-1]["message"]["usage"]["cache_creation"] = {
        "ephemeral_5m_input_tokens": 2, "ephemeral_1h_input_tokens": 0}
    event, = read("claude", records)["events"]
    assert event["model"] == event["effective_model"] == "claude-sonnet-4-6"
    assert event["model_provenance"] == "usage_record"
    assert event["cache_write_ttl"] == {"five_minute": 2, "one_hour": 0}
    assert meter._weighted_reference_tokens(event) == {
        "fresh_input": "30", "cache_read": "2.4", "cache_write": "7.5",
        "output": "60", "total": "99.9"}

    del records[-1]["message"]["usage"]["cache_creation"]
    event, = read("claude", records)["events"]
    weighted = meter._weighted_reference_tokens(event)
    assert weighted == {
        "fresh_input": "30", "cache_read": "2.4", "cache_write": None,
        "output": "60", "total": None}


def test_selected_codex_context_and_missing_write_do_not_make_a_weighted_total():
    records = codex()
    records[1]["payload"]["model"] = "gpt-5.3-codex"
    del records[-1]["payload"]["usage"]["cache_write_input_tokens"]
    event, = read("codex", records)["events"]
    assert event["model_provenance"] == "selected_context"
    assert event["effective_model"] is None
    assert event["kinds"]["cache_write"] is None
    assert meter._weighted_reference_tokens(event) == {
        "fresh_input": None, "cache_read": None, "cache_write": None,
        "output": None, "total": None}

    abstract = {
        "effective_model": "gpt-5.3-codex",
        "kinds": {"fresh_input": 12, "cache_read": 8, "cache_write": 0, "output": 4},
        "cache_write_ttl": {"five_minute": 0, "one_hour": 0},
    }
    assert meter._weighted_reference_tokens(abstract) == {
        "fresh_input": "21", "cache_read": "1.4", "cache_write": "0",
        "output": "56", "total": "78.4"}


@POSIX_ONLY
def test_refresh_deduplicates_rotation_and_partial_tail_keeps_prior_state(
        tmp_path, monkeypatch):
    records = c2_codex_records(tmp_path / "approved-project")
    home, source, _project, _config_path = c2_home(tmp_path, records=records)
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))
    first = meter._refresh_ledger(home)
    ledger_path = home / ".cairn" / "meter" / "ledger.json"
    before = meter._load_ledger(ledger_path.read_bytes())
    first_cursor = before["cursors"][0]

    (source / "rotated.jsonl").write_bytes(b"".join(encoded(records)))
    duplicate = meter._refresh_ledger(home)
    after_rotation = meter._load_ledger(ledger_path.read_bytes())
    assert first["status"] == duplicate["status"] == "written"
    assert len(after_rotation["events"]) == 1
    assert len(after_rotation["cursors"]) == 2

    with (source / "session.jsonl").open("ab") as handle:
        handle.write(b'{"type":"token_usage_record"')
    partial = meter._refresh_ledger(home)
    after_partial = meter._load_ledger(ledger_path.read_bytes())
    prior_cursor = next(cursor for cursor in after_partial["cursors"]
                        if cursor["file_key"] == first_cursor["file_key"])
    assert partial["status"] == "written"
    assert "partial_tail" in after_partial["coverage"]["reasons"]
    assert len(after_partial["events"]) == 1
    assert prior_cursor == first_cursor


@POSIX_ONLY
def test_refresh_lock_busy_and_replace_failure_preserve_previous_ledger(
        tmp_path, monkeypatch):
    import fcntl as host_fcntl

    home, _source, project, _config_path = c2_home(
        tmp_path, records=c2_codex_records(tmp_path / "approved-project"))
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))
    assert meter._refresh_ledger(home)["status"] == "written"
    area = home / ".cairn" / "meter"
    ledger = area / "ledger.json"
    before = ledger.read_bytes()
    lock_fd = os.open(area / "ledger.lock", os.O_RDWR)
    try:
        host_fcntl.flock(lock_fd, host_fcntl.LOCK_EX | host_fcntl.LOCK_NB)
        busy = meter._refresh_ledger(home)
        assert busy["status"] == "unavailable" and busy["reason"] == "ledger_busy"
        assert ledger.read_bytes() == before
    finally:
        os.close(lock_fd)

    def fail_replace(*_args, **_kwargs):
        raise OSError("SECRET-REPLACE-FAILURE")

    monkeypatch.setattr(meter.os, "replace", fail_replace)
    failed = meter._refresh_ledger(home)
    assert failed["status"] == "unavailable"
    assert failed["reason"] == "ledger_write_failed"
    assert ledger.read_bytes() == before
    assert not list(area.glob(".ledger-*.tmp"))
    assert "SECRET" not in json.dumps(failed)


@POSIX_ONLY
def test_refresh_rejects_duplicate_old_ledger_and_preserves_its_bytes(tmp_path):
    home, _source, _project, _config_path = c2_home(
        tmp_path, records=c2_codex_records(tmp_path / "approved-project"))
    area = home / ".cairn" / "meter"
    area.mkdir(mode=0o700)
    area.chmod(0o700)
    path = area / "ledger.json"
    original = b'{"schema":"bad","schema":"duplicate"}\n'
    path.write_bytes(original)
    path.chmod(0o600)

    result = meter._refresh_ledger(home)

    assert result["status"] == "unavailable"
    assert result["reason"] == "ledger_invalid"
    assert path.read_bytes() == original


@POSIX_ONLY
def test_refresh_directory_sync_failure_refuses_project_publication(
        tmp_path, monkeypatch):
    home, _source, project, _config_path = c2_home(
        tmp_path, records=c2_codex_records(tmp_path / "approved-project"))
    area = home / ".cairn" / "meter"
    area.mkdir(mode=0o700)
    area.chmod(0o700)
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))
    real_fsync = os.fsync

    def fail_directory_sync(fd):
        if stat.S_ISDIR(os.fstat(fd).st_mode):
            raise OSError("SECRET-DIRECTORY-SYNC")
        return real_fsync(fd)

    import stat
    monkeypatch.setattr(meter.os, "fsync", fail_directory_sync)
    result = meter._refresh_ledger(home)
    path = home / ".cairn" / "meter" / "ledger.json"
    assert result == {"status": "unavailable", "reason": "ledger_durability_uncertain",
                      "coverage": "unknown"}
    assert path.exists()
    assert meter._load_ledger(path.read_bytes())["events"]
    assert not (project / "dev" / "measurement" / "meter.json").exists()
    assert "SECRET" not in json.dumps(result)


@POSIX_ONLY
@pytest.mark.parametrize("over_by", [0, 1], ids=["exact-cap", "cap-plus-one"])
def test_refresh_total_source_budget_is_all_or_unavailable(tmp_path, monkeypatch, over_by):
    records = c2_codex_records(tmp_path / "approved-project")
    home, source, _project, _config_path = c2_home(tmp_path, records=records)
    source_size = (source / "session.jsonl").stat().st_size
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda item, _roots: (item["remote"], None))
    monkeypatch.setattr(meter, "MAX_TOTAL_SOURCE_BYTES", source_size - over_by)
    result = meter._refresh_ledger(home)
    if over_by:
        assert result["status"] == "unavailable"
        assert result["reason"] == "source_budget_exceeded"
        assert not (home / ".cairn" / "meter" / "ledger.json").exists()
    else:
        assert result["status"] == "written"


@POSIX_ONLY
def test_disabled_refresh_does_not_create_ledger_directory_or_read_sources(tmp_path):
    home, _source, _project, _config_path = c2_home(tmp_path, enabled=False,
        records=c2_codex_records(tmp_path / "approved-project"))

    result = meter._refresh_ledger(home)

    assert result == {"status": "disabled", "reason": "disabled"}
    assert not (home / ".cairn" / "meter").exists()
