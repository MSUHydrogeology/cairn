# SPDX-License-Identifier: MIT
"""Synthetic-only contracts for tools/meter.py; no host-source access."""

import copy
import importlib.util
import json
import io
import os
import runpy
import struct
import sys
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
        self.offsets = {}
        self.paths = {}
        self.next_handle = 1
        self.accessed = 21
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
        return [{"name": "session.jsonl", "file_id": 4,
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
                "written": 31, "changed": 41,
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


WINDOWS_ONLY = pytest.mark.skipif(os.name != "nt", reason="requires native Windows token, NTFS handles and ACLs")


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
    sid_text_ptr = api.C.c_void_p()
    if not api.advapi.ConvertSidToStringSidW(api.C.cast(sid_buffer, api.C.c_void_p),
                                             api.C.byref(sid_text_ptr)):
        raise AssertionError("could not prepare the disposable Windows ACL fixture")
    try:
        sid_text = api.C.wstring_at(sid_text_ptr)
    finally:
        api.kernel.LocalFree(sid_text_ptr)
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
    api.open = lambda name, parent=None, **kwargs: (
        1 if parent is None else 2 if name == "profile" else
        3 if name == ".cairn" else 4)
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


def test_windows_read_config_tolerates_accessed_only_drift():
    content = b'{"version":1,"enabled":false}'
    api = synthetic_read_config_api(content)
    assert api.read_config("C:\\profile", b"synthetic-sid") == content
    assert api.handles_closed == [4, 3, 2, 1]


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
])
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


def run_main_with_synthetic_home(home, monkeypatch, capsys, *, fake_home=None):
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
    if fake_home is not None:
        monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.setattr(sys, "stdin", io.StringIO("SYNTHETIC-STDIN"))
    monkeypatch.setattr(sys, "argv", [str(METER), "--json"])
    code = namespace["main"]()
    return code, capsys.readouterr()


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
    ledger = meter._new_ledger(prior, config, events, waits, cursors, [claim], [],
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
    config = b'[include]\npath = /synthetic/secret-include\n[remote "origin"]\nurl = https://example.test/org/repo.git\n'
    (git_dir / "config").write_bytes(config)
    project = {"alias": "repo", "path": str(project_path),
               "remote": "https://user:secret@example.test/org/repo.git?token=x#frag"}
    seen = {}

    def trust(excluded_roots):
        assert str(project_path) in excluded_roots
        return {"resolved": "/synthetic/trusted-git"}, None

    def read_config(record, config_bytes, excluded_roots):
        seen["bytes"] = config_bytes
        assert record["resolved"] == "/synthetic/trusted-git"
        return "https://example.test/org/repo.git", None

    monkeypatch.setattr(meter, "_trusted_git", trust)
    monkeypatch.setattr(meter, "_git_origin_from_config", read_config)
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


def _write_fake_git(tmp_path, body):
    executable = tmp_path / "synthetic-git"
    executable.write_text("#!/bin/sh\n" + body, encoding="utf-8")
    executable.chmod(0o700)
    return {"lexical": str(executable), "resolved": str(executable)}


@POSIX_ONLY
def test_git_config_runner_uses_sterile_bounded_pipeline(tmp_path, monkeypatch):
    tmpdir_check = ('[ "$TMPDIR" = /private/tmp ] || exit 9' if sys.platform == "darwin"
                    else '[ -z "${TMPDIR+x}" ] || exit 10')
    record = _write_fake_git(tmp_path, f"""printf 'https://user:secret@example.test/org/repo.git?token=x#frag\\000'
cat >/dev/null
test -z \"${{METER_HOST_CANARY+x}}\" || exit 7
[ \"$1/$2/$3/$4/$5/$6/$7\" = \"config/--file/-/--no-includes/--null/--get-all/remote.origin.url\" ] || exit 8
{tmpdir_check}
""")
    monkeypatch.setattr(meter, "_revalidate_git", lambda _record, _roots: True)
    monkeypatch.setenv("METER_HOST_CANARY", "SYNTHETIC-SECRET")
    remote, reason = meter._git_origin_from_config(record, b"x" * meter.MAX_GIT_CONFIG_BYTES, [])
    assert remote == "https://example.test/org/repo.git"
    assert reason is None
    remote, reason = meter._git_origin_from_config(
        record, b"x" * (meter.MAX_GIT_CONFIG_BYTES + 1), [])
    assert remote is None and reason == "source_budget_exceeded"


@POSIX_ONLY
def test_synthetic_git_config_query_uses_trusted_host_git(tmp_path):
    source_root, project_root = tmp_path / "source", tmp_path / "project"
    source_root.mkdir()
    project_root.mkdir()
    record, reason = meter._trusted_git((str(source_root), str(project_root)))
    assert reason is None and record is not None
    config = (b'[remote "origin"]\n'
              b'url = https://user:secret@example.test/org/repo.git?token=x#frag\n')
    remote, reason = meter._git_origin_from_config(
        record, config, (str(source_root), str(project_root)))
    assert reason is None
    assert remote == "https://example.test/org/repo.git"


@pytest.mark.parametrize("stream,size,expected", [
    ("stdout", meter.MAX_GIT_STDOUT, "project_remote_ambiguous"),
    ("stdout", meter.MAX_GIT_STDOUT + 1, "git_output_limit"),
    ("stderr", meter.MAX_GIT_STDERR, "git_parser_failed"),
    ("stderr", meter.MAX_GIT_STDERR + 1, "git_output_limit"),
])
@POSIX_ONLY
def test_git_config_runner_enforces_output_caps(tmp_path, monkeypatch, stream, size, expected):
    redirect = "1>&2 2>/dev/null" if stream == "stderr" else "2>/dev/null"
    record = _write_fake_git(tmp_path, f"cat >/dev/null\ndd if=/dev/zero bs={size} count=1 {redirect}\n")
    monkeypatch.setattr(meter, "_revalidate_git", lambda _record, _roots: True)
    remote, reason = meter._git_origin_from_config(record, b"synthetic config\n", [])
    assert remote is None and reason == expected


@POSIX_ONLY
def test_git_config_runner_kills_timed_out_process_group(tmp_path, monkeypatch):
    record = _write_fake_git(tmp_path, "sleep 30 &\nwait\n")
    monkeypatch.setattr(meter, "_revalidate_git", lambda _record, _roots: True)
    monkeypatch.setattr(meter, "GIT_TIMEOUT_SECONDS", 0.05)
    remote, reason = meter._git_origin_from_config(record, b"synthetic\n", [])
    assert remote is None and reason == "git_timeout"


def test_git_executable_revalidation_rejects_path_and_hash_swaps(monkeypatch):
    record = {"lexical": "/synthetic/git", "resolved": "/system/git",
              "dev": 1, "ino": 2, "uid": 0, "mode": 0o755, "size": 10,
              "mtime_ns": 3, "ctime_ns": 4, "sha256": "a" * 64}
    for field, replacement in (("resolved", "/synthetic/replacement"),
                               ("sha256", "b" * 64)):
        changed = dict(record, **{field: replacement})
        monkeypatch.setattr(meter, "_git_snapshot", lambda _path, _roots, value=changed: value)
        assert not meter._revalidate_git(record, [])


def test_git_lookup_is_unavailable_without_fixed_path_candidates(monkeypatch):
    monkeypatch.setattr(meter.os, "defpath", "")
    record, reason = meter._trusted_git([])
    assert record is None and reason == "git_unavailable"


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

    home, _source, _project, _config_path = c2_home(
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
def test_refresh_directory_sync_failure_reports_committed_uncertain(
        tmp_path, monkeypatch):
    home, _source, _project, _config_path = c2_home(
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
    assert result["status"] == "committed_uncertain"
    assert path.exists()
    assert meter._load_ledger(path.read_bytes())["events"]
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
