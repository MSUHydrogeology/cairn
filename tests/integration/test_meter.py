# SPDX-License-Identifier: MIT
"""Synthetic-only contracts for dev/tools/meter.py; no host-source access.

Promises:
- Default and disabled commands stay off and do not read configured sources or ledgers.
- Closed configuration, privacy, consent, and source refusals fail closed without exposing input.
- Usage, waits, unknowns, and project exports are normalized and sanitized; raw content and identifiers do not escape.
- Refresh and rebuild publish stable ledger and sanitized export state, preserving or reporting atomic failures.
"""

import copy
import importlib.util
import json
import io
import os
import runpy
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from tests._repo_root import repository_root

ROOT = repository_root(Path(__file__))
sys.path.insert(0, str(ROOT))
from install.scaffold import main as scaffold_main  # noqa: E402
METER = ROOT / "dev/tools/meter.py"
MODELS_CONFIG_SRC = ROOT / "dev/.cairn/meter-models.json"
spec = importlib.util.spec_from_file_location("meter_reader", METER)
meter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meter)


def reference_models():
    return meter.validate_models_config_bytes(MODELS_CONFIG_SRC.read_bytes())


def install_models_config(home, data=None, mode=0o600):
    cairn = home / ".cairn"
    cairn.mkdir(parents=True, exist_ok=True)
    path = cairn / "meter-models.json"
    raw = (MODELS_CONFIG_SRC.read_bytes() if data is None
           else (data if isinstance(data, bytes)
                 else json.dumps(data).encode("utf-8")))
    path.write_bytes(raw)
    os.chmod(path, mode)
    return path
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


def codex_host_cwd():
    """The synthetic Codex records, with a context cwd that is valid on this host."""
    records = codex()
    records[1]["payload"]["cwd"] = ("C:\\synthetic\\repo-a" if os.name == "nt"
                                    else "/synthetic/repo-a")
    return records


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


CLOCK = datetime(2026, 11, 5, 0, 0, tzinfo=timezone.utc)
CLOCK_STAMP = "2026-11-05T00:00:00Z"


@pytest.fixture(autouse=True)
def synthetic_clock(monkeypatch):
    """Every run reads one patched clock, dated before the fixtures' events."""
    monkeypatch.setattr(meter, "_now_utc", lambda: CLOCK, raising=False)


def start_counting(home, source, refresh=None):
    """Truncate every log in place and refresh: that refresh is the start.

    Every bookmark is then at byte 0. Returns a function that writes the saved
    bytes back into the same files (same inode), so the next refresh counts
    them as growth after the start.
    """
    refresh = meter._refresh_ledger if refresh is None else refresh
    saved = {path: path.read_bytes() for path in sorted(Path(source).rglob("*.jsonl"))}
    for path in saved:
        with open(path, "r+b") as handle:
            handle.truncate(0)
    started = refresh(home)
    assert started["status"] in {"written", "ok"}, started

    def restore():
        for path, data in saved.items():
            with open(path, "r+b") as handle:
                handle.write(data)
    return restore


def refresh_counted(home, source, refresh=None):
    """Start counting over empty logs, restore the bytes in place, refresh again.

    Returns the second result: the first refresh that counts the logs' lines.
    """
    start_counting(home, source, refresh)()
    return (meter._refresh_ledger if refresh is None else refresh)(home)


def scan_started(config, cursors=(), **kwargs):
    """The scan with one start row per alias dated the patched clock; six values."""
    starts = [{"source_alias": source["alias"], "started_at": CLOCK_STAMP}
              for source in sorted(config["sources"], key=lambda item: item["alias"])]
    return meter._scan_approved_sources(
        config, list(cursors), starts=starts, now=CLOCK, **kwargs)[:6]


def c2_home(tmp_path, *, enabled=True, records=None, claims=None, models_config=True):
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
    if models_config:
        install_models_config(home)
    return home, source_root, project, config_path


def host_absolute(path):
    """A synthetic absolute path: Windows needs a drive letter added to a POSIX spelling."""
    return str(Path(path).absolute())


def test_ledger_cursor_preserves_full_unsigned_windows_file_identity():
    config = meter.validate_config_bytes(json.dumps({
        "version": 1, "enabled": False,
        "sources": [{"alias": "source", "tool": "codex",
                     "root": host_absolute("/synthetic/source")}],
        "projects": [],
    }).encode())
    cursor = {"source_alias": "source", "file_key": "a" * 64,
              "dev": (1 << 32) - 1, "ino": (1 << 64) - 1,
              "generation": 1, "offset": 0, "line": 0,
              "size": 0, "mtime_ns": 0, "ctime_ns": 0,
              "digest": None, "owner_key": None}
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
    scan = scan_started(config)
    return home, config, scan


def run_main_with_synthetic_home(home, monkeypatch, capsys, *, fake_home=None,
                                 command=None, refresh_result=None,
                                 global_overrides=None, meter_path=METER,
                                 report=False, report_args=()):
    namespace = runpy.run_path(str(meter_path), run_name="meter_test")
    namespace["main"].__globals__["_fixed_user_home"] = lambda: Path(home)
    namespace["main"].__globals__["_now_utc"] = lambda: CLOCK
    if refresh_result is not None:
        def synthetic_refresh(received_home, **_kwargs):
            assert Path(received_home) == Path(home)
            return refresh_result
        namespace["main"].__globals__["_refresh_ledger"] = synthetic_refresh
    if global_overrides is not None:
        namespace["main"].__globals__.update(global_overrides)
    if fake_home is not None:
        monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.setattr(sys, "stdin", io.StringIO("SYNTHETIC-STDIN"))
    argv = [str(meter_path)]
    if command:
        argv.append(command)
        if report:
            argv.append("--report")
            argv.extend(report_args)
        argv.append("--json")
    else:
        argv.append("--json")
    monkeypatch.setattr(sys, "argv", argv)
    code = namespace["main"]()
    return code, capsys.readouterr()


def _run_synthetic_meter_command(home, monkeypatch, capsys, command):
    return run_main_with_synthetic_home(home, monkeypatch, capsys, command=command)


def _arm_after_ledger_commit(monkeypatch, arm):
    original = meter._atomic_replace_ledger

    def replace_then_arm(*args, **kwargs):
        result = original(*args, **kwargs)
        arm()
        return result

    monkeypatch.setattr(meter, "_atomic_replace_ledger", replace_then_arm)


def test_report_freshness_public(tmp_path, monkeypatch, capsys):
    home, _source, project, _config_path = c2_home(tmp_path)
    old_project = tmp_path / "unconfigured-project"
    (old_project / "dev" / "measurement").mkdir(parents=True)
    stale = {"schema": "cairn-meter-project/2", "project_alias": "old",
             "aggregates": [{"events": 999999, "kinds": {"fresh_input": 999999}}]}
    stale_path = old_project / "dev" / "measurement" / "meter.json"
    stale_path.write_text(json.dumps(stale), encoding="utf-8")

    monkeypatch.chdir(old_project)
    code, captured = run_main_with_synthetic_home(
        home, monkeypatch, capsys, command="refresh", report=True)
    pulse = json.loads(captured.out)
    assert code == 0 and pulse["schema"] == "cairn-pulse/1"
    assert pulse["project_usage"] is None
    assert "999999" not in captured.out

    current_export = project / "dev" / "measurement" / "meter.json"
    current_export.write_text(json.dumps(stale), encoding="utf-8")
    current_export.chmod(0o600)
    monkeypatch.chdir(project)
    code, captured = run_main_with_synthetic_home(
        home, monkeypatch, capsys, command="refresh", report=True)
    pulse = json.loads(captured.out)
    assert code == 0 and pulse["schema"] == "cairn-pulse/1"
    assert pulse["project_usage"]["project_alias"] == "sample"
    assert "999999" not in captured.out

    for status, reason in (("partial", "catching_up"),
                           ("unavailable", "source_budget_exceeded")):
        code, captured = run_main_with_synthetic_home(
            home, monkeypatch, capsys, command="refresh", report=True,
            refresh_result={"status": status, "reason": reason,
                            "current_project_aggregate": json.dumps(stale).encode()})
        receipt = json.loads(captured.out)
        assert code == 5 and receipt["schema"] == "cairn-meter-refresh/1"
        assert receipt["status"] == status and receipt["reason"] == reason
        assert "999999" not in captured.out

    # The pulse's report reader refuses a file whose handle and name report different
    # change times, which Windows does after a write (found in this plan's build; the
    # pulse is not changed here), so the explicit-report part runs where that holds.
    if os.name != "nt":
        junit = tmp_path / "public.xml"
        junit.write_text('<testsuite tests="1"><testcase name="public" /></testsuite>',
                         encoding="utf-8")
        disabled_root = tmp_path / "disabled"
        disabled_root.mkdir()
        disabled_home, *_ = c2_home(disabled_root, enabled=False)
        code, captured = run_main_with_synthetic_home(
            disabled_home, monkeypatch, capsys, command="refresh", report=True,
            report_args=("--junit-report", str(junit)),
            refresh_result={"status": "disabled", "reason": "disabled"})
        pulse = json.loads(captured.out)
        assert code == 0 and pulse["schema"] == "cairn-pulse/1"
        assert pulse["coverage"]["report_count"] == 1
        assert pulse["project_usage"] is None

    with pytest.raises(SystemExit) as refused:
        run_main_with_synthetic_home(
            home, monkeypatch, capsys, command="refresh", report=True,
            report_args=("--meter-aggregate", str(stale_path)),
            refresh_result={"status": "unavailable", "reason": "source_budget_exceeded"})
    assert refused.value.code == 2
    assert "--report does not accept --meter-aggregate" in capsys.readouterr().err


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

    unavailable_code, unavailable = run_main_with_synthetic_home(
        tmp_path, monkeypatch, capsys, command=command,
        refresh_result={"status": "unavailable", "reason": "SECRET-path"},
    )
    assert unavailable_code != 0
    assert json.loads(unavailable.out) == {
        "schema": "cairn-meter-refresh/1", "status": "unavailable",
        "reason": "unavailable", "coverage": "unknown",
    }
    assert "SECRET-path" not in unavailable.out + unavailable.err

    adopter = tmp_path / "installed-meter"
    adopter.mkdir()
    profile = adopter / "profile.yml"
    profile.write_text(
        "project_name: MeterTest\ntest_command: pytest\nmodules: []\n",
        encoding="utf-8",
    )
    assert scaffold_main(
        ["--config", str(profile), "--target", str(adopter),
         "--cairn-root", str(ROOT), "--allow-dev"]
    ) == 0
    capsys.readouterr()
    installed_meter = adopter / "dev" / "tools" / "meter.py"
    disabled_config = json.dumps(
        {"version": 1, "enabled": False, "sources": [], "projects": []}
    ).encode("utf-8")
    if command != "refresh":
        return
    home = tmp_path / "synthetic-home"
    home.mkdir(mode=0o700)
    os.chmod(home, 0o700)
    config_dir = home / ".cairn"
    config_dir.mkdir(mode=0o700)
    os.chmod(config_dir, 0o700)
    config_path = config_dir / "meter.json"
    config_path.write_bytes(disabled_config)
    os.chmod(config_path, 0o600)
    _code, public_output = run_main_with_synthetic_home(
        home, monkeypatch, capsys, meter_path=installed_meter,
        global_overrides={
            "_refresh_ledger": lambda _home: (_ for _ in ()).throw(
                AssertionError("installed default --json must not refresh")),
        },
    )
    assert json.loads(public_output.out) == {
        "schema": "cairn-meter-foundation/1", "collection": "disabled",
        "usage": {"codex": "unknown", "claude": "unknown",
                  "antigravity": "unknown"},
    }
    assert public_output.err == ""
    assert not (config_dir / "meter").exists()


@pytest.mark.parametrize("command", ["refresh", "rebuild"])
def test_explicit_refresh_partial_receipt_is_closed_and_nonzero(
        tmp_path, monkeypatch, capsys, command):
    code, captured = run_main_with_synthetic_home(
        tmp_path, monkeypatch, capsys, command=command,
        refresh_result={"status": "partial", "reason": "catching_up"})
    assert code == 5
    assert json.loads(captured.out) == {
        "schema": "cairn-meter-refresh/1", "status": "partial",
        "reason": "catching_up", "coverage": "unknown",
    }
    assert captured.err == ""

    bad_code, bad = run_main_with_synthetic_home(
        tmp_path, monkeypatch, capsys, command=command,
        refresh_result={"status": "partial", "reason": "future_reason"})
    assert bad_code == 5
    assert json.loads(bad.out)["status"] == "unavailable"

    wrong_code, wrong = run_main_with_synthetic_home(
        tmp_path, monkeypatch, capsys, command=command,
        refresh_result={"status": "ok", "reason": "catching_up"})
    assert wrong_code == 5
    assert json.loads(wrong.out)["status"] == "unavailable"


def test_oversized_codex_refresh_publishes_partial_export_and_receipt(
        tmp_path, monkeypatch, capsys):
    records = codex()
    home, source, _project, _config = c2_home(tmp_path, records=records)
    start_counting(home, source)()
    monkeypatch.setattr(meter, "MAX_REREAD_BYTES", 1)

    result = meter._refresh_ledger(home)

    assert (result["status"], result["reason"]) == ("partial", "source_too_large")
    ledger = ledger_of(home)
    assert {"source_too_large", "incomplete"} <= set(ledger["coverage"]["reasons"])
    export_path = _project / "dev" / "measurement" / "meter.json"
    exported = json.loads(export_path.read_bytes())
    assert {"source_too_large", "incomplete"} <= set(exported["coverage"]["reasons"])
    assert all(key not in json.dumps(exported) for key in
               ("cursor", "digest", "file_key", "owner_key"))
    code, receipt = run_main_with_synthetic_home(
        home, monkeypatch, capsys, command="refresh",
        global_overrides={"_refresh_ledger": lambda _home: result})
    assert code == 5
    assert json.loads(receipt.out)["status"] == "partial"


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
    ["pytest", "-q", "tests/test_example.py"],
    ["python3.13", "-m", "pytest"],
])
def test_direct_pytest_command_classification(command):
    assert meter.classify_pytest_command(command) == "pytest"


@pytest.mark.parametrize("command", [
    None, [], ["pytest", None], ["sh", "-c", "pytest"],
    ["python3.13", "-m", "unittest"], ["python2", "-m", "pytest"],
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
    events, cursors, reasons, forks, conflicts, waits = scan_started(config)
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
    records = codex_host_cwd()
    context = records.pop(1)
    records.append(context)
    event, = read("codex", records)["events"]
    assert event["ownership"] == "unknown"
    records = codex_host_cwd()
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


def test_first_publication_canonicalizes_conflicted_binding_and_repeats_stably(
        tmp_path, monkeypatch):
    records = c2_codex_records(tmp_path / "approved-project")
    home, _source, _project, config_path = c2_home(tmp_path, records=records)
    config = meter.validate_config_bytes(config_path.read_bytes())
    events, cursors, reasons, proofs, conflicts, waits = scan_started(config)
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
    doubled, single = read(tool, records + records), read(tool, records)
    for result in (doubled, single):
        del result["event_last_line"]       # where an event was last seen: a copy moves it
    assert doubled == single


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
                                 b' ' * (meter.MAX_LINE + 1) + b'\n'],
                         ids=["duplicate-key", "nan", "infinity",
                              "partial-no-newline", "invalid-utf8",
                              "non-object", "oversized-line"])
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


AG_CONVERSATION = "7a6b5c4d-3e2f-4a1b-8c9d-0e1f2a3b4c5d"
AG_UNNAMED = {AG_CONVERSATION: (None, "antigravity_project_not_named")}


def antigravity_reply(input_tokens=120, output_tokens=30, created_at=STAMP, **more):
    """One synthetic token record: counts and a time, plus a body that must not leave."""
    return {"created_at": created_at, "input_tokens": input_tokens,
            "output_tokens": output_tokens, "content": "SECRET-BODY", **more}


def read_antigravity(records, **keywords):
    keywords.setdefault("conversation", AG_CONVERSATION)
    keywords.setdefault("attribution", AG_UNNAMED)
    return meter.read_records("antigravity", encoded(records), **keywords)


def test_antigravity_token_records_become_events_with_unknown_cache_kinds(tmp_path):
    reply = antigravity_reply()
    # The tool writes a reply about four times; a fifth copy differs only in its body.
    result = read_antigravity([reply] * 4 + [antigravity_reply(content="another copy")])
    event, = result["events"]
    assert set(event) == EVENT_FIELDS
    assert event["kinds"] == {"fresh_input": 120, "cache_read": None,
                              "cache_write": None, "output": 30}
    assert event["observed_at"] == "2026-11-05T12:00:00+00:00"
    assert event["time_coverage"] == "known"
    assert event["session_key"] == event["thread_key"] == meter._digest(
        "antigravity", AG_CONVERSATION)
    assert event["session_digest"] == meter._short_session_digest(AG_CONVERSATION)
    assert (event["model"], event["model_provenance"], event["effective_model"]) == (
        None, "unknown", None)
    assert meter._weighted_reference_tokens(event)["total"] is None
    assert (event["project_alias"], event["ownership"]) == (None, "unknown")
    assert event["reasons"] == ["antigravity_project_not_named"]
    assert result["issues"] == []
    assert AG_CONVERSATION not in json.dumps(result) and "SECRET" not in json.dumps(result)
    # A different count or a different time is a different reply.
    other = read_antigravity([reply, antigravity_reply(output_tokens=31),
                              antigravity_reply(created_at="2026-11-05T12:00:01Z")])
    assert len(other["events"]) == 3
    # The same instant spelled with an offset is the same reply, not a second one.
    same_instant = read_antigravity(
        [reply, antigravity_reply(created_at="2026-11-05T07:00:00-05:00")])
    assert [item["event_key"] for item in same_instant["events"]] == [event["event_key"]]
    # A record that names its own conversation is an ordinary reply.
    own = read_antigravity([antigravity_reply(conversationId=AG_CONVERSATION,
                                              conversation_id=AG_CONVERSATION)])
    assert [item["event_key"] for item in own["events"]] == [event["event_key"]]
    assert own["issues"] == []

    root = Path(host_absolute(tmp_path / "ag-source"))
    config = {"version": 1, "enabled": True,
              "sources": [{"alias": "ag-source", "tool": "antigravity", "root": str(root)}],
              "projects": [{"alias": "sample", "path": host_absolute(tmp_path / "project"),
                            "remote": "https://example.test/team/project.git"}]}
    named = {AG_CONVERSATION: ("sample", None)}
    approved = dict(config=config, source_aliases=["ag-source"], source_root=str(root))
    event, = read_antigravity([reply], attribution=named, **approved)["events"]
    assert (event["project_alias"], event["project_association"], event["ownership"]) == (
        "sample", "current_local_verified", "proven")
    assert event["reasons"] == [] and event["source_aliases"] == ["ag-source"]
    elsewhere = dict(approved, source_root=host_absolute(tmp_path / "elsewhere"))
    event, = read_antigravity([reply], attribution=named, **elsewhere)["events"]
    assert event["project_alias"] is None and event["reasons"] == ["project_path_unapproved"]
    account = dict(config, requested_accounts={"ag-source": "someone"})
    event, = read_antigravity([reply], attribution=named,
                              **dict(approved, config=account))["events"]
    assert event["project_alias"] is None and event["reasons"] == ["account_filter_unproven"]
    assert set(event["kinds"].values()) == {None}

    # A stream's conversation is the second part of its path under the root.
    log = root / "brain" / AG_CONVERSATION / ".system_generated" / "logs" / "transcript.jsonl"
    log.parent.mkdir(parents=True)
    log.write_bytes(b"".join(encoded([reply, reply])))
    stream = meter._iter_approved_lines(
        str(root), f"brain/{AG_CONVERSATION}/.system_generated/logs/transcript.jsonl")
    event, = meter.read_records("antigravity", stream, attribution=AG_UNNAMED)["events"]
    assert event["session_key"] == meter._digest("antigravity", AG_CONVERSATION)


@pytest.mark.parametrize("record,keywords,issue", [
    ({"created_at": STAMP, "input_tokens": 5}, {}, "invalid_record"),
    ({"created_at": STAMP, "output_tokens": 5}, {}, "invalid_record"),
    (antigravity_reply(input_tokens=True), {}, "invalid_record"),
    (antigravity_reply(output_tokens=False), {}, "invalid_record"),
    (antigravity_reply(input_tokens=-1), {}, "invalid_record"),
    (antigravity_reply(output_tokens=1.5), {}, "invalid_record"),
    (antigravity_reply(input_tokens="12"), {}, "invalid_record"),
    (antigravity_reply(output_tokens=meter.MAX_COUNTER + 1), {}, "invalid_record"),
    (antigravity_reply(created_at="2026-11-05T12:00:00"), {}, "invalid_record"),
    (antigravity_reply(created_at="2026-11-05"), {}, "invalid_record"),
    (antigravity_reply(created_at="not-a-time"), {}, "invalid_record"),
    (antigravity_reply(created_at=1_700_000_000), {}, "invalid_record"),
    (antigravity_reply(created_at="9999-12-31T23:59:59-05:00"), {}, "invalid_record"),
    (antigravity_reply(created_at="0001-01-01T00:00:00+05:00"), {}, "invalid_record"),
    ({"input_tokens": 5, "output_tokens": 5}, {}, "invalid_record"),
    (antigravity_reply(conversationId="3f2e1d0c-9b8a-4c7d-8e6f-5a4b3c2d1e0f"), {},
     "conflicting_binding"),
    (antigravity_reply(conversation_id="3f2e1d0c-9b8a-4c7d-8e6f-5a4b3c2d1e0f"), {},
     "conflicting_binding"),
    (antigravity_reply(conversationId=12), {}, "conflicting_binding"),
    (antigravity_reply(), {"conversation": None}, "invalid_record"),
    (antigravity_reply(), {"conversation": AG_CONVERSATION.upper()}, "invalid_record"),
    (antigravity_reply(), {"conversation": "not-a-conversation"}, "invalid_record"),
    (antigravity_reply(), {"attribution": None}, "invalid_record"),
    (antigravity_reply(), {"attribution": {}}, "invalid_record"),
    (antigravity_reply(), {"attribution": {AG_CONVERSATION: (None, None)}}, "invalid_record"),
    ({"created_at": STAMP, "content": {"usage": {"anything": 1}}}, {},
     "unsupported_usage_contract"),
    ({"created_at": STAMP, "content": "text"}, {}, "no_supported_usage"),
])
def test_antigravity_lines_that_are_not_complete_token_records_make_no_event(
        record, keywords, issue):
    result = read_antigravity([record], **keywords)
    assert result["events"] == []
    assert result["issues"] == [issue]
    assert "SECRET" not in json.dumps(result)
    # Beside a complete reply the bad line is closed and the reply still counts once.
    mixed = read_antigravity([antigravity_reply(input_tokens=7), record], **keywords)
    if keywords:                    # the reply itself has no usable conversation
        assert mixed["events"] == []
    else:
        assert len(mixed["events"]) == 1
        assert (issue in mixed["issues"]) == (issue != "no_supported_usage")


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
             "sources": [{"alias": "codex-main", "tool": "codex",
                          "root": host_absolute("/synthetic/source")}],
             "projects": [{"alias": "cairn", "path": host_absolute("/synthetic/project"),
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
], ids=["duplicate-key", "nan", "infinity", "invalid-utf8", "oversized-config"])
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
    records_value = codex()
    records_value[1]["payload"]["cwd"] = str(project)
    file.write_bytes(b"".join(encoded(records_value))[:-1])
    result = meter.read_records("codex", meter._iter_approved_lines(root, "records.jsonl"),
                                config=config, source_aliases=("codex-main",))
    assert result["events"] == []
    assert calls == []


def _worktree_project(tmp_path, remote, extra_config=b""):
    """A synthetic project whose config turns on the worktree setting."""
    project_path = tmp_path / "synthetic-project"
    git_dir = project_path / ".git"
    git_dir.mkdir(parents=True, mode=0o700)
    (git_dir / "config").write_bytes(
        b"[extensions]\n\tworktreeConfig = true\n" + extra_config
        + b'[remote "origin"]\n\turl = ' + remote.encode() + b"\n")
    return {"alias": "repo", "path": str(project_path), "remote": remote}, git_dir


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


def test_session_digest_matches_existing_intent_identity_rule():
    import hashlib

    owner = "  synthetic-owner  "
    expected = hashlib.sha256(b"synthetic-owner").hexdigest()[:8]
    assert meter._short_session_digest(owner) == expected
    event, = read("codex", codex_host_cwd())["events"]
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


def test_claim_snapshot_skips_a_claim_whose_agent_is_not_a_session_tag():
    owner = "synthetic-owner"
    claim_id, rows = c2_claim_records(owner)
    named = [
        {"event": "claim", "id": "named-claim", "ts": "2026-11-05T10:00:00Z",
         "agent": "Codex named coordinator", "files": ["src/app.py"],
         "action": "x"},
        {"event": "release", "id": "named-claim", "ts": "2026-11-05T10:30:00Z"},
    ]
    claim, = meter._claim_snapshot("sample", encoded(named + rows))
    assert claim["tool"] == "codex"
    assert claim["session_digest"] == meter._short_session_digest(owner)
    with pytest.raises(meter.Unavailable):
        meter._claim_snapshot("sample", encoded([dict(named[0], files="not-a-list")]))


def test_refresh_persists_normalized_history_and_claims_without_raw_inputs(
        tmp_path, monkeypatch):
    owner = "019a0000-0000-7000-8000-000000000001"
    claim_id, claim_rows = c2_claim_records(owner)
    records = c2_codex_records(tmp_path / "approved-project")
    home, source, project, _config_path = c2_home(
        tmp_path, records=records, claims=claim_rows)

    result = refresh_counted(home, source)

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
    assert not (home / ".cairn" / "meter" / "ledger.lock").exists()
    if os.name == "posix":
        assert ledger_path.stat().st_mode & 0o777 == 0o600
    assert ledger_path.stat().st_nlink == 1


def test_project_export_contains_only_sanitized_project_aggregates(
        tmp_path, monkeypatch):
    home, source, project, config_path = c2_home(tmp_path)
    owner = "019a0000-0000-7000-8000-000000000001"
    claim_id, claim_rows = c2_claim_records(owner)
    (project / "dev" / "intents.jsonl").write_bytes(b"".join(encoded(claim_rows)))
    records = c2_codex_records(project)
    (source / "session.jsonl").write_bytes(b"".join(encoded(records)))

    assert refresh_counted(home, source)["status"] == "written"
    ledger_path = home / ".cairn" / "meter" / "ledger.json"
    config_value = json.loads(config_path.read_text(encoding="utf-8"))
    config_value["projects"].append({
        "alias": "other", "path": host_absolute("/synthetic/other-project"),
        "remote": "https://example.test/team/other.git"})
    config = meter.validate_config_bytes(json.dumps(config_value).encode())
    ledger = meter._load_ledger(ledger_path.read_bytes())
    other = dict(ledger["events"][0])
    other["event_key"] = meter._digest("synthetic-other-project")
    other["project_alias"] = "other"
    ledger["events"].append(other)
    models_cfg = reference_models()
    ledger["aggregates"] = meter._recompute_aggregates(
        ledger["events"], config, models_cfg)
    export = meter._project_export(ledger, config, "sample", models_cfg)
    assert set(export) == {
        "schema", "project_alias", "ratio_version", "aggregates", "by_tier",
        "wait", "coverage"}
    row, = export["aggregates"]
    assert len(export["aggregates"]) == 1
    assert row["artifact"] == "src/app.py"
    assert row["tool"] == "codex"
    assert row["tier"] == "unknown"
    assert row["kinds"] == {
        "fresh_input": 12, "cache_read": 8, "cache_write": 0, "output": 4}
    assert export["ratio_version"] == models_cfg["ratio_version"]
    assert export["schema"] == "cairn-meter-project/3"
    assert [entry["tier"] for entry in export["by_tier"]] == ["unknown"]
    assert export["wait"] == {"coverage": "unknown", "observed": None,
                               "by_day": [], "by_artifact": []}
    serialized = json.dumps(export)
    for secret in (owner, claim_id, str(home), str(source), str(project),
                   "other-project", "session.jsonl", "session_digest",
                   "event_key", "cursor"):
        assert secret not in serialized


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

    exports = [alpha / "dev" / "measurement" / "meter.json",
               beta / "dev" / "measurement" / "meter.json"]
    receipt = {"schema": "cairn-meter-refresh/1", "status": "ok",
               "reason": "none", "coverage": "unknown"}

    def public_refresh(_home, command="refresh"):
        code, captured = _run_synthetic_meter_command(
            home, monkeypatch, capsys, command)
        assert code == 0
        assert json.loads(captured.out) == receipt
        assert captured.err == ""
        return json.loads(captured.out)

    assert refresh_counted(home, source, public_refresh) == receipt
    snapshots = tuple(path.read_bytes() for path in exports)
    for command in ("refresh", "rebuild"):
        public_refresh(home, command)
        assert tuple(path.read_bytes() for path in exports) == snapshots

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


def test_public_refresh_exports_many_closed_claims_without_pairwise_work(
        tmp_path, monkeypatch, capsys):
    home, source, project, _config_path = c2_home(tmp_path)
    owner = "019a0000-0000-7000-8000-000000000011"
    records = c2_bound_records(project, owner, "turn-sweep", 10,
                               [("wait-one", 1000), ("wait-two", 1000)])
    start = datetime(2026, 11, 5, 12, 0, tzinfo=timezone.utc)
    late_start = datetime(2026, 11, 5, 17, 30, tzinfo=timezone.utc)
    timing_rows = [item for item in records if item["type"] == "event_msg"
                   and item["payload"].get("type") == "item_completed"]
    assert len(timing_rows) == 2
    for item, when in zip(timing_rows, (start, late_start)):
        item["payload"]["started_at_ms"] = int(when.timestamp() * 1000)
        item["payload"]["completed_at_ms"] = int(
            (when + timedelta(seconds=1)).timestamp() * 1000)
        item["payload"]["item"]["cwd"] = str(project)
    (source / "session.jsonl").write_bytes(b"".join(encoded(records)))

    def stamp(hour, minute, second=0):
        return datetime(2026, 11, 5, hour, minute, second,
                        tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")

    claims = []
    for index in range(445):
        left = datetime(2026, 11, 5, 0, 0, tzinfo=timezone.utc) + timedelta(
            seconds=index * 2)
        right = left + timedelta(seconds=1)
        claim_id = f"closed-{index:03d}"
        claims.extend([
            {"event": "claim", "id": claim_id,
             "ts": left.isoformat().replace("+00:00", "Z"),
             "agent": "codex-" + meter._short_session_digest(owner),
             "files": [f"src/{index}.py"], "action": "Synthetic claim"},
            {"event": "release", "id": claim_id,
             "ts": right.isoformat().replace("+00:00", "Z"), "commit": "abc123"},
        ])
    for claim_id, left, right in (
            ("claim-a", stamp(11, 59), stamp(12, 0)),
            ("claim-b", stamp(12, 0), stamp(12, 1)),
            ("claim-c", stamp(14, 0), stamp(17, 0)),
            ("claim-d", stamp(15, 0), stamp(16, 0)),
            ("claim-e", stamp(16, 30), stamp(18, 0))):
        claims.extend([
            {"event": "claim", "id": claim_id, "ts": left,
             "agent": "codex-" + meter._short_session_digest(owner),
             "files": [f"src/{claim_id}.py"], "action": "Synthetic claim"},
            {"event": "release", "id": claim_id, "ts": right, "commit": "abc123"},
        ])
    (project / "dev" / "intents.jsonl").write_bytes(b"".join(encoded(claims)))

    start_counting(home, source)()
    final_clock = datetime(2026, 11, 6, 0, 0, tzinfo=timezone.utc)
    code, captured = run_main_with_synthetic_home(
        home, monkeypatch, capsys, command="refresh",
        global_overrides={"_now_utc": lambda: final_clock})
    assert code == 0
    assert json.loads(captured.out)["status"] == "ok"
    exported = json.loads((project / "dev" / "measurement" / "meter.json").read_text())
    assert exported["wait"]["observed"] == {
        "executions": 2, "execution_ms": 2000, "wall_wait_ms": 2000}, exported["wait"]
    assert exported["wait"]["by_artifact"] == [{
        "day": "2026-11-05", "artifact": "src/claim-b.py",
        "executions": 1, "execution_ms": 1000, "wall_wait_ms": 1000,
    }]
    serialized = json.dumps(exported, sort_keys=True)
    assert owner not in serialized and str(project) not in serialized

    prior = (project / "dev" / "measurement" / "meter.json").read_bytes()
    code, captured = run_main_with_synthetic_home(
        home, monkeypatch, capsys, command="refresh",
        global_overrides={"MAX_WAIT_EXPORT_WORK": 448})
    assert code != 0
    assert json.loads(captured.out)["reason"] == "source_budget_exceeded"
    assert (project / "dev" / "measurement" / "meter.json").read_bytes() == prior


@pytest.mark.parametrize("binding_change", ["unchanged", "changed"])
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

    def run(command):
        return _run_synthetic_meter_command(home, monkeypatch, capsys, command)

    def public_refresh(_home):
        code, captured = run("refresh")
        assert code == 0
        return json.loads(captured.out)

    assert refresh_counted(home, source, public_refresh)["status"] == "ok"
    ledger_path = home / ".cairn" / "meter" / "ledger.json"
    export_path = project / "dev" / "measurement" / "meter.json"
    initial = meter._load_ledger(ledger_path.read_bytes())
    old_wait, = initial["waits"]
    assert old_wait["project_alias"] == "sample"
    assert old_wait["project_association"] == "current_local_verified"

    session_path.unlink()
    if binding_change == "changed":
        config["projects"][0]["remote"] = changed_remote
        config_path.write_text(json.dumps(config), encoding="utf-8")
        config_path.chmod(0o600)

    code, captured = run("refresh")
    middle_receipt = json.loads(captured.out)
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


def _make_folder_link(link, target):
    """A folder link: a symbolic link, or on Windows a junction (it needs no privilege)."""
    if os.name == "nt":
        made = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                              capture_output=True, check=False)
        assert made.returncode == 0
    else:
        Path(link).symlink_to(target, target_is_directory=True)


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
        _make_folder_link(dev, outside_dev)
    else:
        measurement.rename(dev / "measurement-original")
        _make_folder_link(measurement, outside)

    monkeypatch.setattr(meter, "_capture_project_claims",
                        lambda _project: ([], "captured"))
    result = meter._refresh_ledger(home)

    assert result["status"] == "unavailable"
    assert result["reason"] == "project_export_unavailable"
    assert external_target.read_bytes() == b"outside export\n"
    if not meter._is_link(os.lstat(measurement)) if measurement.exists() else False:
        assert not list((dev / "measurement").glob(".meter-*.tmp"))


@pytest.mark.parametrize("fault", ["replace"])
def test_posix_project_export_write_failures_preserve_or_report_state(
        tmp_path, monkeypatch, fault):
    home, _source, project, _config_path = c2_home(tmp_path)
    target = project / "dev" / "measurement" / "meter.json"
    target.write_bytes(b"old export\n")
    original_replace = os.replace

    def arm():
        def injected_replace(source, destination, **kwargs):
            if Path(source).name.startswith(".meter-"):
                raise OSError("synthetic replace refusal")
            return original_replace(source, destination, **kwargs)
        monkeypatch.setattr(meter.os, "replace", injected_replace)

    _arm_after_ledger_commit(monkeypatch, arm)
    result = meter._refresh_ledger(home)

    assert result["status"] == "unavailable"
    assert result["reason"] == "project_export_unavailable"
    assert target.read_bytes() == b"old export\n"
    assert not list(target.parent.glob(".meter-*.tmp"))
    assert "SECRET" not in json.dumps(result)


def test_public_refresh_closes_failed_project_publication_receipt(
        tmp_path, monkeypatch, capsys):
    home, _source, project, _config_path = c2_home(tmp_path)
    (project / "dev" / "measurement").rmdir()

    code, captured = _run_synthetic_meter_command(home, monkeypatch, capsys, "refresh")

    assert code == 5
    assert json.loads(captured.out) == {
        "schema": "cairn-meter-refresh/1", "status": "unavailable",
        "reason": "project_export_unavailable", "coverage": "unknown"}
    assert captured.err == ""
    assert (home / ".cairn" / "meter" / "ledger.json").is_file()


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
    models_cfg = reference_models()
    prior = meter._load_ledger(None)
    ledger = meter._new_ledger(prior, config, events, _waits, cursors, [],
        [{"alias": "sample", "remote": "https://example.test/team/project.git"}],
        {"captured"}, reasons, proofs, conflicts, models_config=models_cfg)
    restored = meter._load_ledger(
        (json.dumps(ledger, sort_keys=True, separators=(",", ":")) + "\n").encode())
    assert restored["ratio_version"] == models_cfg["ratio_version"]
    assert restored["ratio_index"] == models_cfg
    lineage, = restored["lineages"]
    assert lineage["state"] == "verified"
    assert lineage["proofs"][0]["parent_terminal"]["thread_snapshot"]["fresh_input"] == 100
    assert lineage["proofs"][0]["child_sequence"][-1]["thread_snapshot"]["fresh_input"] == 130
    assert restored["aggregates"][0]["kinds"]["cache_write"] is None
    assert restored["coverage"]["global"] == "unknown"
    repeated = meter._new_ledger(restored, config, events, _waits, cursors, [],
        [{"alias": "sample", "remote": "https://example.test/team/project.git"}],
        {"captured"}, reasons, proofs, conflicts, models_config=models_cfg)
    repeated_bytes = json.dumps(repeated, sort_keys=True, separators=(",", ":")) + "\n"
    assert repeated_bytes == json.dumps(restored, sort_keys=True,
                                        separators=(",", ":")) + "\n"
    assert sum(event["kinds"]["fresh_input"] for event in repeated["events"]) == 130


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
    assert not hasattr(meter, "_RATIO_INDEX") and not hasattr(meter, "RATIO_VERSION")
    index = reference_models()
    assert index["schema"] == "cairn-meter-models/1"
    assert index["ratio_version"] == "cairn-api-token-index/2026-11-22"
    assert index["tiers"] == ["frontier", "high", "medium", "low"]
    assert index["models"]["claude-sonnet-4-6"] == {
        "fresh_input": [3, 1], "cache_read": [3, 10], "output": [15, 1],
        "cache_write_mode": "ttl_split",
        "cache_write_5m": [15, 4], "cache_write_1h": [6, 1],
        "tier": "medium", "prefixes": ["claude-sonnet-4-6-"],
    }
    assert index["models"]["claude-fable-5-2"]["tier"] == "frontier"
    assert index["models"]["claude-opus-5-5"]["cache_read"] == [1, 5]
    assert index["models"]["gpt-5.3-codex"]["cache_write_mode"] == "unbilled"
    assert index["models"]["gpt-5.3-codex"]["cache_write_5m"] is None
    assert index["models"]["claude-haiku-5-5"]["long_prompt"]["over_tokens"] == 100_000
    assert index["tools"]["antigravity"]["log_filename"] == "transcript.jsonl"


def test_reference_index_uses_source_reported_cache_ttl_and_keeps_unknown_partial():
    models_cfg = reference_models()
    records = claude()
    records[-1]["message"]["model"] = "claude-sonnet-4-6"
    records[-1]["message"]["usage"]["cache_creation"] = {
        "ephemeral_5m_input_tokens": 2, "ephemeral_1h_input_tokens": 0}
    event, = read("claude", records)["events"]
    assert event["model"] == event["effective_model"] == "claude-sonnet-4-6"
    assert event["model_provenance"] == "usage_record"
    assert event["cache_write_ttl"] == {"five_minute": 2, "one_hour": 0}
    assert meter._weighted_reference_tokens(event, models_cfg) == {
        "fresh_input": "30", "cache_read": "2.4", "cache_write": "7.5",
        "output": "60", "total": "99.9"}
    assert set(meter._weighted_reference_tokens(event, None).values()) == {None}

    del records[-1]["message"]["usage"]["cache_creation"]
    event, = read("claude", records)["events"]
    weighted = meter._weighted_reference_tokens(event, models_cfg)
    assert weighted == {
        "fresh_input": "30", "cache_read": "2.4", "cache_write": None,
        "output": "60", "total": None}

    def weighted_reply(model, fresh, cache_read, write, output, ttl):
        records = claude()
        usage = records[-1]["message"]["usage"]
        records[-1]["message"]["model"] = model
        usage.update(input_tokens=fresh, cache_read_input_tokens=cache_read,
                     cache_creation_input_tokens=write, output_tokens=output)
        usage["cache_creation"] = {"ephemeral_5m_input_tokens": ttl[0],
                                   "ephemeral_1h_input_tokens": ttl[1]}
        event, = read("claude", records)["events"]
        return meter._weighted_reference_tokens(event, models_cfg)

    assert weighted_reply("claude-fable-5-2", 10, 8, 2, 4, (0, 2)) == {
        "fresh_input": "80", "cache_read": "1.6", "cache_write": "32",
        "output": "160", "total": "273.6"}
    haiku = "claude-haiku-5-5"
    assert weighted_reply(haiku, 10, 8, 2, 4, (2, 0)) == {
        "fresh_input": "1", "cache_read": "0.08", "cache_write": "0.25",
        "output": "2", "total": "3.33"}
    assert weighted_reply(haiku, 99990, 8, 2, 4, (2, 0)) == {
        "fresh_input": "9999", "cache_read": "0.08", "cache_write": "0.25",
        "output": "2", "total": "10001.33"}
    assert weighted_reply(haiku, 100000, 8, 2, 4, (2, 0)) == {
        "fresh_input": "50000", "cache_read": "0.4", "cache_write": "1.25",
        "output": "10", "total": "50011.65"}


def test_selected_codex_model_is_weighted_and_a_missing_write_is_not():
    models_cfg = reference_models()
    records = codex_host_cwd()
    records[1]["payload"]["model"] = "gpt-6.2-sol"
    event, = read("codex", records)["events"]
    assert event["model_provenance"] == "selected_context"
    assert event["effective_model"] is None
    assert meter._weighted_reference_tokens(event, models_cfg) == {
        "fresh_input": "24", "cache_read": "0.8", "cache_write": "0",
        "output": "40", "total": "64.8"}

    # Under unbilled cache_write_mode, omitted cache_write still prices at 0 when the other
    # three kinds are known, while non-zero cache_write, missing cache_read, or _unknown_kinds fail closed.
    del records[-1]["payload"]["usage"]["cache_write_input_tokens"]
    event, = read("codex", records)["events"]
    assert event["kinds"]["cache_write"] is None
    assert meter._weighted_reference_tokens(event, models_cfg) == {
        "fresh_input": "24", "cache_read": "0.8", "cache_write": "0",
        "output": "40", "total": "64.8"}

    nonzero_write = {
        "effective_model": "gpt-5.3-codex",
        "kinds": {"fresh_input": 12, "cache_read": 8, "cache_write": 5, "output": 4},
        "cache_write_ttl": {"five_minute": None, "one_hour": None},
    }
    assert meter._weighted_reference_tokens(nonzero_write, models_cfg) == {
        "fresh_input": "21", "cache_read": "1.4", "cache_write": None,
        "output": "56", "total": None}

    missing_read = {
        "effective_model": "gpt-5.3-codex",
        "kinds": {"fresh_input": 12, "cache_read": None, "cache_write": None, "output": 4},
        "cache_write_ttl": {"five_minute": None, "one_hour": None},
    }
    assert meter._weighted_reference_tokens(missing_read, models_cfg) == {
        "fresh_input": "21", "cache_read": None, "cache_write": None,
        "output": "56", "total": None}

    unknown = {
        "effective_model": "gpt-5.3-codex",
        "kinds": meter._unknown_kinds(),
        "cache_write_ttl": {"five_minute": None, "one_hour": None},
    }
    assert set(meter._weighted_reference_tokens(unknown, models_cfg).values()) == {None}

    abstract = {
        "effective_model": "gpt-5.3-codex",
        "kinds": {"fresh_input": 12, "cache_read": 8, "cache_write": 0, "output": 4},
        "cache_write_ttl": {"five_minute": 0, "one_hour": 0},
    }
    assert meter._weighted_reference_tokens(abstract, models_cfg) == {
        "fresh_input": "21", "cache_read": "1.4", "cache_write": "0",
        "output": "56", "total": "78.4"}


def test_refresh_deduplicates_rotation_and_partial_tail_keeps_prior_state(
        tmp_path, monkeypatch):
    records = c2_codex_records(tmp_path / "approved-project")
    home, source, _project, _config_path = c2_home(tmp_path, records=records)
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
    assert "partial_tail" not in after_partial["coverage"]["reasons"]
    assert len(after_partial["events"]) == 1
    assert {name: prior_cursor[name] for name in ("offset", "digest", "generation")} == {
        name: first_cursor[name] for name in ("offset", "digest", "generation")}


def test_refresh_lock_busy_and_replace_failure_preserve_previous_ledger(
        tmp_path, monkeypatch):
    home, _source, project, _config_path = c2_home(
        tmp_path, records=c2_codex_records(tmp_path / "approved-project"))
    assert meter._refresh_ledger(home)["status"] == "written"
    area = home / ".cairn" / "meter"
    ledger = area / "ledger.json"
    before = ledger.read_bytes()
    lock = area / "ledger.lock"
    lock.write_bytes(b"0" * 32)
    busy = meter._refresh_ledger(home)
    assert busy["status"] == "unavailable" and busy["reason"] == "ledger_busy"
    assert ledger.read_bytes() == before
    assert lock.read_bytes() == b"0" * 32          # a run that did not make it leaves it
    stale = time.time() - 20 * 60
    os.utime(lock, (stale, stale))
    assert meter._refresh_ledger(home)["status"] == "written"
    assert not lock.exists()                       # taken over, then removed by its own run
    before = ledger.read_bytes()

    def fail_replace(*_args, **_kwargs):
        raise OSError("SECRET-REPLACE-FAILURE")

    monkeypatch.setattr(meter.os, "replace", fail_replace)
    failed = meter._refresh_ledger(home)
    assert failed["status"] == "unavailable"
    assert failed["reason"] == "ledger_write_failed"
    assert ledger.read_bytes() == before
    assert not list(area.glob(".ledger-*.tmp"))
    assert "SECRET" not in json.dumps(failed)


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


def test_disabled_refresh_does_not_create_ledger_directory_or_read_sources(tmp_path):
    home, _source, _project, _config_path = c2_home(tmp_path, enabled=False,
        records=c2_codex_records(tmp_path / "approved-project"))

    result = meter._refresh_ledger(home)

    assert result == {"status": "disabled", "reason": "disabled"}
    assert not (home / ".cairn" / "meter").exists()


@pytest.mark.parametrize("remote, expected", [
    ("git@host:team/project.git", "host:team/project.git"),
    ("git@GitHub.com:Org/Repo.git/", "github.com:Org/Repo.git"),
])
def test_documented_ssh_style_remote_is_accepted(tmp_path, remote, expected):
    """Promise: a project remote in the SSH form the measurement README shows
    (`git@host:team/project.git`) passes configuration validation. The user
    part is dropped and the host lowercased, as for URL remotes."""
    config = {"version": 1, "enabled": True,
              "sources": [{"alias": "codex-main", "tool": "codex",
                           "root": str(tmp_path / "provider-data")}],
              "projects": [{"alias": "cairn", "path": str(tmp_path / "project"),
                            "remote": remote}]}
    parsed = meter.validate_config_bytes(json.dumps(config).encode("utf-8"))
    assert parsed["projects"][0]["remote"] == expected
    # The meter validates its own normalized configuration again before it
    # reads sources, so the normalized form must validate to itself.
    again = meter.validate_config_bytes(json.dumps(parsed).encode("utf-8"))
    assert again["projects"][0]["remote"] == expected


@pytest.mark.parametrize("remote", ["git@host:", "git@:team/project.git",
                                    "git@host/x:team/project.git"])
def test_malformed_ssh_style_remote_is_refused(tmp_path, remote):
    """Promise: an SSH-form remote with no host or no path still fails closed."""
    config = {"version": 1, "enabled": True, "sources": [],
              "projects": [{"alias": "cairn", "path": str(tmp_path / "project"),
                            "remote": remote}]}
    with pytest.raises(meter.Unavailable):
        meter.validate_config_bytes(json.dumps(config).encode("utf-8"))


# ---- Counting forward: start point, bookmarks, ledger /5 (plan C1) ----------

import hashlib  # noqa: E402


def sha256_of(data):
    return hashlib.sha256(data).hexdigest()


def claude_record(message_id, timestamp=STAMP, session="session-a"):
    record = {"type": "assistant", "timestamp": timestamp, "sessionId": session,
              "requestId": "request-" + message_id, "cwd": "/synthetic/not-proof",
              "message": {"id": message_id, "model": "synthetic-model",
                          "content": "SECRET-BODY", "usage": {
                              "input_tokens": 10, "output_tokens": 4,
                              "cache_creation_input_tokens": 2,
                              "cache_read_input_tokens": 8}}}
    if timestamp is None:
        del record["timestamp"]
    return record


def user_record(text="SECRET-USER"):
    return {"type": "user", "timestamp": STAMP, "sessionId": "session-a",
            "message": {"content": text}}


def c1_home(tmp_path, monkeypatch, *, claude_logs=None, codex_logs=None):
    """A synthetic home with one Claude and one Codex source root."""
    home, codex_root, project, config_path = c2_home(tmp_path)
    claude_root = tmp_path / "approved-claude-source"
    claude_root.mkdir()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["sources"].append({"alias": "claude-source", "tool": "claude",
                              "root": str(claude_root)})
    config_path.write_text(json.dumps(config), encoding="utf-8")
    config_path.chmod(0o600)
    for name, data in (claude_logs or {}).items():
        (claude_root / name).write_bytes(data)
    for name, data in (codex_logs or {}).items():
        (codex_root / name).write_bytes(data)
    return home, claude_root, codex_root, project, config_path


def ledger_of(home):
    return meter._load_ledger((home / ".cairn" / "meter" / "ledger.json").read_bytes())


def cursor_for(ledger, alias):
    found = [item for item in ledger["cursors"] if item["source_alias"] == alias]
    assert len(found) == 1
    return found[0]


def test_first_refresh_records_where_each_log_ends_and_counts_nothing(tmp_path, monkeypatch):
    claude_lines = encoded([claude_record("message-a"), user_record()])
    codex_data_lines = encoded(c2_codex_records(tmp_path / "approved-project"))
    home, _claude_root, _codex_root, _project, _config = c1_home(
        tmp_path, monkeypatch, claude_logs={"session.jsonl": b"".join(claude_lines)},
        codex_logs={"session.jsonl": b"".join(codex_data_lines)})

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 0
    assert ledger["schema"] == "cairn-meter-ledger/7"
    assert ledger["reader_version"] == "cairn-source-readers/7"
    assert ledger["events"] == [] and ledger["waits"] == []
    assert ledger["fold_horizon"] == "2026-10-22" and ledger["daily"] == []
    assert ledger["starts"] == [
        {"source_alias": "claude-source", "started_at": CLOCK_STAMP},
        {"source_alias": "codex-source", "started_at": CLOCK_STAMP}]
    claude_cursor = cursor_for(ledger, "claude-source")
    codex_cursor = cursor_for(ledger, "codex-source")
    assert claude_cursor["offset"] == len(b"".join(claude_lines))
    assert claude_cursor["digest"] == sha256_of(claude_lines[-1])
    assert claude_cursor["line"] == 0 and claude_cursor["generation"] == 1
    assert claude_cursor["size"] == len(b"".join(claude_lines))
    assert claude_cursor["owner_key"] is None
    assert codex_cursor["offset"] == len(b"".join(codex_data_lines))
    assert codex_cursor["digest"] == sha256_of(codex_data_lines[-1])
    assert codex_cursor["owner_key"] == meter._digest(
        "codex", "019a0000-0000-7000-8000-000000000001")
    for cursor in (claude_cursor, codex_cursor):
        assert set(cursor) == meter._CURSOR_FIELDS

    again = meter._refresh_ledger(home)
    assert again["status"] == "written" and again["events"] == 0
    assert ledger_of(home)["cursors"] == ledger["cursors"]


@pytest.mark.parametrize("content, last_line", [
    (b'one\ntwo\n{"torn', b"two\n"),
    (b"", None),
    (b'{"no newline yet"', None),
    (b"x\r\ny\r\n", b"y\r\n"),
    (b"only\n", b"only\n"),
], ids=["torn-tail", "empty", "no-newline", "crlf-last-line", "single-line"])
def test_start_bookmark_stops_after_the_last_complete_line(tmp_path, monkeypatch, content, last_line):
    home, _claude_root, _codex_root, _project, _config = c1_home(
        tmp_path, monkeypatch, claude_logs={"session.jsonl": content})

    assert meter._refresh_ledger(home)["status"] == "written"

    cursor = cursor_for(ledger_of(home), "claude-source")
    expected_offset = content.rfind(b"\n") + 1
    assert cursor["offset"] == expected_offset
    assert cursor["digest"] == (None if last_line is None else sha256_of(last_line))
    assert cursor["line"] == 0
    assert cursor["size"] == len(content)


def test_log_created_after_the_start_counts_only_events_not_before_it(tmp_path, monkeypatch):
    home, claude_root, _codex_root, _project, _config = c1_home(tmp_path, monkeypatch)
    assert meter._refresh_ledger(home)["status"] == "written"
    ledger = ledger_of(home)
    assert len(ledger["starts"]) == 2 and ledger["cursors"] == []

    late = [claude_record("before-start", "2026-11-04T12:00:00Z"),
            claude_record("after-start", "2026-11-05T12:00:00Z"),
            claude_record("no-time", None)]
    older = [claude_record("old-log-event", "2026-11-05T12:00:00Z")]
    (claude_root / "late.jsonl").write_bytes(b"".join(encoded(late)))
    (claude_root / "older.jsonl").write_bytes(b"".join(encoded(older)))
    after = int(datetime(2026, 11, 6, tzinfo=timezone.utc).timestamp() * 1e9)
    before = int(datetime(2026, 11, 1, tzinfo=timezone.utc).timestamp() * 1e9)
    os.utime(claude_root / "late.jsonl", ns=(after, after))
    os.utime(claude_root / "older.jsonl", ns=(before, before))

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 2
    assert sorted(event["observed_at"] for event in ledger["events"]
                  if event["observed_at"] is not None) == ["2026-11-05T12:00:00+00:00"]
    assert sum(event["observed_at"] is None for event in ledger["events"]) == 1
    cursors = {item["file_key"]: item for item in ledger["cursors"]}
    older_key = meter._digest("cursor", "claude-source", "older.jsonl")
    late_key = meter._digest("cursor", "claude-source", "late.jsonl")
    assert cursors[older_key]["line"] == 0
    assert cursors[older_key]["offset"] == len(b"".join(encoded(older)))
    assert cursors[late_key]["line"] == 3
    assert cursors[late_key]["offset"] == len(b"".join(encoded(late)))
    assert cursors[late_key]["digest"] == sha256_of(encoded(late)[-1])
    assert ledger["starts"] == [
        {"source_alias": "claude-source", "started_at": CLOCK_STAMP},
        {"source_alias": "codex-source", "started_at": CLOCK_STAMP}]


def test_a_source_added_later_gets_its_own_start_point(tmp_path, monkeypatch):
    home, _claude_root, codex_root, project, config_path = c1_home(tmp_path, monkeypatch)
    assert meter._refresh_ledger(home)["status"] == "written"
    later = datetime(2026, 11, 9, 8, 30, 15, 987654, tzinfo=timezone.utc)
    extra_root = tmp_path / "approved-extra-source"
    extra_root.mkdir()
    (extra_root / "session.jsonl").write_bytes(b"".join(encoded([claude_record("extra")])))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["sources"].append({"alias": "extra-source", "tool": "claude",
                              "root": str(extra_root)})
    config_path.write_text(json.dumps(config), encoding="utf-8")
    config_path.chmod(0o600)
    monkeypatch.setattr(meter, "_now_utc", lambda: later)

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 0
    assert ledger["starts"] == [
        {"source_alias": "claude-source", "started_at": CLOCK_STAMP},
        {"source_alias": "codex-source", "started_at": CLOCK_STAMP},
        {"source_alias": "extra-source", "started_at": "2026-11-09T08:30:15Z"}]
    assert cursor_for(ledger, "extra-source")["line"] == 0


@pytest.mark.parametrize("schema, reader", [
    ("cairn-meter-ledger/3", "cairn-source-readers/3"),
    ("cairn-meter-ledger/4", "cairn-source-readers/4"),
    ("cairn-meter-ledger/5", "cairn-source-readers/5"),
])
def test_an_old_ledger_is_refused_and_never_overwritten(tmp_path, monkeypatch, schema, reader):
    home, _claude_root, _codex_root, _project, _config = c1_home(
        tmp_path, monkeypatch, claude_logs={"session.jsonl": b"".join(encoded([claude_record("m")]))})
    assert meter._refresh_ledger(home)["status"] == "written"
    path = home / ".cairn" / "meter" / "ledger.json"
    old = json.loads(path.read_bytes())
    old.update(schema=schema, reader_version=reader)
    del old["agent_runs"]
    if not schema.endswith("/5"):
        for field in ("starts", "fold_horizon", "daily"):
            del old[field]
        for cursor in old["cursors"]:
            del cursor["digest"], cursor["owner_key"]
    if schema.endswith("/3"):
        del old["waits"]
    path.write_bytes((json.dumps(old, sort_keys=True, separators=(",", ":")) + "\n").encode())
    before = path.read_bytes()

    result = meter._refresh_ledger(home)

    assert result == {"status": "unavailable", "reason": "ledger_old_schema",
                      "coverage": "unknown"}
    assert path.read_bytes() == before
    assert meter._closed_refresh_receipt(result)["reason"] == "ledger_old_schema"
    with pytest.raises(meter.Unavailable) as refused:
        meter._load_ledger(before)
    assert refused.value.reason == "ledger_old_schema"


SUB_RUN = "a1b2c3d4e5f6g7h8i"


def record_in_project(project, message_id, **changes):
    """A Claude record whose own working folder is the approved project."""
    record = claude_record(message_id)
    record["cwd"] = str(project)
    record.update(changes)
    return record


def sub_agent_summary(run=SUB_RUN):
    return {"type": "attachment", "timestamp": STAMP, "sessionId": "session-a",
            "text": "done <task-id>" + run + "</task-id>",
            "usage": {"totalTokens": 9, "toolUses": 2, "durationMs": 500}}


def fresh_totals(ledger, alias):
    rows = [row for row in ledger["aggregates"]
            if row["tool"] == "claude" and row["project_alias"] == alias]
    return {name: sum(row["kinds"][name] or 0 for row in rows)
            for name in ("fresh_input", "cache_write", "cache_read", "output")}


def test_sub_agent_usage_counts_with_its_transcript_and_summary(tmp_path, monkeypatch):
    home, claude_root, _codex_root, project, _config = c1_home(tmp_path, monkeypatch)
    assert meter._refresh_ledger(home)["status"] == "written"
    (claude_root / "session.jsonl").write_bytes(b"".join(encoded(
        [record_in_project(project, "message-main"), sub_agent_summary()])))
    (claude_root / "agent.jsonl").write_bytes(b"".join(encoded(
        [record_in_project(project, "message-sub", isSidechain=True, agentId=SUB_RUN)])))

    assert meter._refresh_ledger(home)["status"] == "written"

    ledger = ledger_of(home)
    assert "agent_runs_incomplete" not in ledger["coverage"]["reasons"]
    assert fresh_totals(ledger, "sample") == {
        "fresh_input": 20, "cache_write": 4, "cache_read": 16, "output": 8}


def test_summary_without_its_transcript_is_incomplete_until_it_is_read(tmp_path, monkeypatch):
    home, claude_root, _codex_root, project, config_path = c1_home(tmp_path, monkeypatch)
    assert meter._refresh_ledger(home)["status"] == "written"
    (claude_root / "session.jsonl").write_bytes(b"".join(encoded(
        [record_in_project(project, "message-main"), sub_agent_summary()])))
    assert meter._refresh_ledger(home)["status"] == "written"
    config = meter.validate_config_bytes(config_path.read_bytes())
    first = ledger_of(home)
    assert "agent_runs_incomplete" in first["coverage"]["reasons"]
    assert b"agent_runs_incomplete" in meter._project_export_bytes(first, config, "sample")

    (claude_root / "agent.jsonl").write_bytes(b"".join(encoded(
        [record_in_project(project, "message-sub", isSidechain=True, agentId=SUB_RUN)])))
    assert meter._refresh_ledger(home)["status"] == "written"
    second = ledger_of(home)
    assert "agent_runs_incomplete" not in second["coverage"]["reasons"]
    assert b"agent_runs_incomplete" not in meter._project_export_bytes(second, config, "sample")


def daily_row(day="2026-11-01", **changes):
    row = {"project_alias": None, "day": day, "tool": "claude",
           "model": "synthetic-model", "model_provenance": "usage_record",
           "effective_model": "synthetic-model", "events": 3, "unknown_events": 0,
           "kinds": {"fresh_input": 30, "cache_read": 24, "cache_write": 6, "output": 12},
           "reference_index": reference_models()["ratio_version"],
           "reference_tokens": {name: None for name in (*meter._EVENT_KIND_NAMES, "total")}}
    row.update(changes)
    return row


def ledger_with_cursors(tmp_path, monkeypatch):
    claude_lines = b"".join(encoded([claude_record("message-a"), user_record()]))
    codex_lines = b"".join(encoded(c2_codex_records(tmp_path / "approved-project")))
    home, _claude_root, _codex_root, _project, _config = c1_home(
        tmp_path, monkeypatch, claude_logs={"session.jsonl": claude_lines},
        codex_logs={"session.jsonl": codex_lines})
    assert meter._refresh_ledger(home)["status"] == "written"
    return json.loads((home / ".cairn" / "meter" / "ledger.json").read_bytes())


def as_bytes(ledger):
    return (json.dumps(ledger, sort_keys=True, separators=(",", ":")) + "\n").encode()


def edit_cursor(**changes):
    def apply(ledger):
        ledger["cursors"][0].update(changes)
    return apply


def edit_start(**changes):
    def apply(ledger):
        ledger["starts"][0].update(changes)
    return apply


def edit_daily(rows, horizon="2026-11-05"):
    def apply(ledger):
        ledger["daily"] = rows
        ledger["fold_horizon"] = horizon
    return apply


def repeat_start(ledger):
    ledger["starts"].append(dict(ledger["starts"][0]))


INVALID_LEDGER_EDITS = {
    "digest-null-past-offset-zero": edit_cursor(digest=None),
    "digest-set-at-offset-zero": edit_cursor(offset=0),
    "digest-not-hex": edit_cursor(digest="z" * 64),
    "digest-too-short": edit_cursor(digest="ab"),
    "digest-upper-case": edit_cursor(digest="A" * 64),
    "digest-not-text": edit_cursor(digest=5),
    "owner-key-not-hex": edit_cursor(owner_key="xyz"),
    "owner-key-not-text": edit_cursor(owner_key=7),
    "start-unsafe-alias": edit_start(source_alias="../escape"),
    "start-empty-alias": edit_start(source_alias=""),
    "start-bad-time": edit_start(started_at="2026-11-05 00:00:00"),
    "start-time-zone-spelling": edit_start(started_at="2026-11-05T00:00:00+00:00"),
    "start-impossible-date": edit_start(started_at="2026-13-05T00:00:00Z"),
    "start-not-text": edit_start(started_at=5),
    "start-repeated-alias": repeat_start,
    "start-after-the-clock": edit_start(started_at="2026-11-05T00:00:01Z"),
    "fold-horizon-not-a-date": lambda ledger: ledger.update(fold_horizon="2026-13-45"),
    "fold-horizon-words": lambda ledger: ledger.update(fold_horizon="yesterday"),
    "fold-horizon-number": lambda ledger: ledger.update(fold_horizon=20261105),
    "fold-horizon-short-spelling": lambda ledger: ledger.update(fold_horizon="2026-11-5"),
    "fold-horizon-after-today": lambda ledger: ledger.update(fold_horizon="2026-11-06"),
    "ratio-version-not-a-label": lambda ledger: ledger.update(ratio_version="today"),
    "daily-reference-index-not-a-label": edit_daily([daily_row(reference_index="today")]),
    "daily-repeated-key": edit_daily([daily_row(), daily_row(events=9)]),
    "daily-without-a-day": edit_daily([daily_row(day=None)]),
    "daily-day-on-the-horizon": edit_daily([daily_row("2026-11-03")], "2026-11-03"),
    "daily-day-after-the-horizon": edit_daily([daily_row("2026-11-04")], "2026-11-03"),
    "daily-while-horizon-is-null": edit_daily([daily_row()], None),
    "daily-row-shape": edit_daily([daily_row(unknown_events=99)]),
}


@pytest.mark.parametrize("name", sorted(INVALID_LEDGER_EDITS))
def test_hand_edited_ledger_is_refused_as_invalid(tmp_path, monkeypatch, name):
    ledger = ledger_with_cursors(tmp_path, monkeypatch)
    assert meter._load_ledger(as_bytes(ledger), CLOCK)["schema"].endswith("/7")
    INVALID_LEDGER_EDITS[name](ledger)
    with pytest.raises(meter.Unavailable) as refused:
        meter._load_ledger(as_bytes(ledger))
    assert refused.value.reason == "ledger_invalid"
    with pytest.raises(meter.Unavailable) as explicit:
        meter._load_ledger(as_bytes(ledger), CLOCK)
    assert explicit.value.reason == "ledger_invalid"


def test_well_formed_daily_rows_and_horizon_load(tmp_path, monkeypatch):
    ledger = ledger_with_cursors(tmp_path, monkeypatch)
    ledger["fold_horizon"] = "2026-11-05"
    ledger["daily"] = [daily_row("2026-11-01"), daily_row("2026-11-02", model="other-model",
                                                          effective_model="other-model")]
    loaded = meter._load_ledger(as_bytes(ledger), CLOCK)
    assert loaded["fold_horizon"] == "2026-11-05" and len(loaded["daily"]) == 2


def test_a_retained_event_before_the_horizon_is_refused(tmp_path, monkeypatch):
    home, _claude_root, codex_root, _project, _config = c1_home(
        tmp_path, monkeypatch, codex_logs={"session.jsonl": b"".join(encoded(
            c2_codex_records(tmp_path / "approved-project")))})
    assert refresh_counted(home, codex_root)["status"] == "written"
    ledger = json.loads((home / ".cairn" / "meter" / "ledger.json").read_bytes())
    assert ledger["events"] and ledger["events"][0]["observed_at"].startswith("2026-11-05")
    later = datetime(2026, 11, 20, tzinfo=timezone.utc)
    ledger["fold_horizon"] = "2026-11-05"
    assert meter._load_ledger(as_bytes(ledger), later)["fold_horizon"] == "2026-11-05"
    ledger["fold_horizon"] = "2026-11-06"
    with pytest.raises(meter.Unavailable) as refused:
        meter._load_ledger(as_bytes(ledger), later)
    assert refused.value.reason == "ledger_invalid"


def test_the_empty_ledger_has_the_new_fields():
    empty = meter._load_ledger(None)
    assert empty["starts"] == [] and empty["fold_horizon"] is None and empty["daily"] == []
    assert empty["schema"] == "cairn-meter-ledger/7"
    assert meter._load_ledger(as_bytes(empty), CLOCK) == empty


# ---- The stream's piece, max_lines and tail keywords (plan C1, D12) ---------

def stream_over(tmp_path, content, **options):
    root = tmp_path / "synthetic-source"
    root.mkdir(exist_ok=True, mode=0o700)
    (root / "records.jsonl").write_bytes(content)
    budget = options.pop("budget", meter.MAX_BATCH_BYTES)
    return meter._iter_approved_lines(root, "records.jsonl", budget, **options)


TAIL_BUDGET = 2 * meter.MAX_LINE + 2


@pytest.mark.parametrize("content, offset, line", [
    (b"one\ntwo\ntor", 8, b"two\n"),
    (b"abc", 0, None),
    (b"", 0, None),
    (b"a\r\nb\r\n", 6, b"b\r\n"),
    (b"\n", 1, b"\n"),
    (b"first\n", 6, b"first\n"),
    (b"first\nsecond\n\n", 14, b"\n"),
], ids=["torn-tail", "no-newline", "empty", "crlf-last-line", "blank-line", "one-line",
        "blank-last-line"])
def test_tail_stream_finds_the_last_complete_line(tmp_path, content, offset, line):
    stream = stream_over(tmp_path, content, budget=TAIL_BUDGET, piece=True, tail=True)
    assert list(stream) == []
    assert stream.terminal_reason is None
    assert stream.tail_offset == offset
    assert stream.tail_digest == (None if line is None else sha256_of(line))
    assert stream.open_identity["size"] == len(content)
    assert stream.bytes_read <= TAIL_BUDGET


def test_tail_stream_crosses_read_blocks(tmp_path):
    long_line = b"x" * (70 * 1024) + b"\n"
    content = b"head\n" + long_line + b"y" * 100_000
    content = content[:len(b"head\n") + len(long_line)] + b"z" * 90_000
    stream = stream_over(tmp_path, content, budget=TAIL_BUDGET, piece=True, tail=True)
    assert list(stream) == [] and stream.terminal_reason is None
    assert stream.tail_offset == len(b"head\n") + len(long_line)
    assert stream.tail_digest == sha256_of(long_line)
    assert stream.bytes_read <= TAIL_BUDGET


def test_tail_stream_refuses_a_line_or_torn_tail_over_the_line_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(meter, "MAX_LINE", 5)
    budget = 2 * 5 + 2
    for content in (b"123456\n", b"ab\n1234567", b"x" * 6, b"ab\n123456\n"):
        stream = stream_over(tmp_path, content, budget=budget, piece=True, tail=True)
        assert list(stream) == []
        assert stream.terminal_reason == "source_budget_exceeded", content
    for content, line in ((b"1234\n", b"1234\n"), (b"ab\n12345", b"ab\n"),
                          (b"12345", None), (b"x\n12345\n", None)):
        stream = stream_over(tmp_path, content, budget=budget, piece=True, tail=True)
        assert list(stream) == []
        if line is None and content.endswith(b"\n"):
            assert stream.terminal_reason == "source_budget_exceeded"
        else:
            assert stream.terminal_reason is None, content
            assert stream.tail_digest == (None if line is None else sha256_of(line))


def test_piece_stream_ignores_a_torn_tail_and_stops_at_the_line_limit(tmp_path):
    torn = stream_over(tmp_path, b"one\ntwo\nthr", piece=True)
    assert list(torn) == [b"one\n", b"two\n"]
    assert torn.terminal_reason is None
    assert torn.end_offset == 8 and torn.complete_lines == 2
    assert torn.tail_digest == sha256_of(b"two\n") and torn.limit_stop is False
    assert torn.bytes_read == 11

    first = stream_over(tmp_path, b"one\ntwo\nthree\n", piece=True, max_lines=1,
                        budget=meter.MAX_LINE + 1)
    assert list(first) == [b"one\n"]
    assert first.terminal_reason is None and first.limit_stop is True
    assert first.end_offset == 4

    whole = stream_over(tmp_path, b"only\n", piece=True, max_lines=1,
                        budget=meter.MAX_LINE + 1)
    assert list(whole) == [b"only\n"]
    assert whole.terminal_reason is None and whole.limit_stop is False


def test_piece_stream_ends_at_the_last_whole_line_when_the_byte_budget_runs_out(tmp_path):
    stream = stream_over(tmp_path, b"aaaa\nbbbb\ncccc\n", piece=True, budget=7)
    assert list(stream) == [b"aaaa\n"]
    assert stream.terminal_reason is None and stream.limit_stop is True
    assert stream.end_offset == 5 and stream.bytes_read == 7


def test_piece_stream_ceilings_follow_the_reread_limits_not_the_batch_limits(
        tmp_path, monkeypatch):
    monkeypatch.setattr(meter, "MAX_BATCH_BYTES", 8)
    monkeypatch.setattr(meter, "MAX_BATCH_LINES", 1)
    plain = stream_over(tmp_path, b"one\ntwo\n", budget=9)
    assert list(plain) == [] and plain.terminal_reason == "source_budget_exceeded"
    piece = stream_over(tmp_path, b"one\ntwo\n", piece=True, budget=9, max_lines=2)
    assert list(piece) == [b"one\n", b"two\n"] and piece.terminal_reason is None
    limited = stream_over(tmp_path, b"one\ntwo\n", piece=True, budget=9)
    assert list(limited) == [b"one\n"] and limited.limit_stop is True
    for options in ({"budget": meter.MAX_REREAD_BYTES + 1},
                    {"budget": 9, "max_lines": meter.MAX_REREAD_LINES + 1},
                    {"budget": 9, "max_lines": 0}):
        refused = stream_over(tmp_path, b"one\n", piece=True, **options)
        assert list(refused) == [] and refused.terminal_reason == "source_budget_exceeded"


@pytest.mark.parametrize("options", [
    {"tail": True}, {"max_lines": 1}, {"piece": "yes"},
    {"piece": True, "tail": "yes"}])
def test_stream_refuses_inconsistent_keywords(tmp_path, options):
    stream = stream_over(tmp_path, b"one\n", **options)
    assert list(stream) == [] and stream.terminal_reason is not None


def test_a_fresh_read_drops_waits_that_began_before_the_start(tmp_path, monkeypatch):
    home, source, project, config_path = c2_home(tmp_path)
    owner = "019a0000-0000-7000-8000-000000000001"
    clock_ms = int(CLOCK.timestamp() * 1000)
    records = c2_bound_records(project, owner, "turn-a", 10, [])
    for item_id, start in (("before-start", clock_ms - 5000), ("after-start", clock_ms + 5000)):
        timing = timing_record(item_id=item_id, start=start, end=start + 1000)
        timing["payload"]["thread_id"] = owner
        timing["payload"]["turn_id"] = "turn-a"
        records.append(timing)
    (source / "session.jsonl").write_bytes(b"".join(encoded(records)))
    config = meter.validate_config_bytes(config_path.read_bytes())

    _events, _cursors, _reasons, _forks, _conflicts, waits = scan_started(config)

    assert [wait["started_at_ms"] for wait in waits] == [clock_ms + 5000]


# ---- Resume, pieces and the run limit (plan C2) ------------------------------

def resume_request(tmp_path, offset, line=None, **changes):
    """A resume dict for records.jsonl as stream_over wrote it."""
    info = os.stat(tmp_path / "synthetic-source" / "records.jsonl")
    request = {"dev": info.st_dev, "ino": info.st_ino, "offset": offset,
               "digest": None if line is None else sha256_of(line)}
    request.update(changes)
    return request


@pytest.mark.parametrize("window, offset, digest, expected", [
    (b"one\ntwo\n", 8, sha256_of(b"two\n"), None),
    (b"abc\n", 4, sha256_of(b"abc\n"), None),
    (b"x\r\nabc\r\n", 8, sha256_of(b"abc\r\n"), None),
    (b"", 0, None, None),
    (b"one\ntwo", 7, sha256_of(b"two"), "not_line_boundary"),
    (b"one\ntwo\n", 8, sha256_of(b"one\n"), "digest_mismatch"),
    (b"one\ntwo\n", 8, "0" * 64, "digest_mismatch"),
    (b"two\n", 100, sha256_of(b"two\n"), "digest_mismatch"),
], ids=["two-lines", "whole-file-is-the-line", "crlf", "offset-zero",
        "not-a-boundary", "wrong-line", "wrong-digest", "line-longer-than-the-window"])
def test_resume_window_verdict_is_a_pure_check(window, offset, digest, expected):
    assert meter._resume_window_verdict(window, offset, digest) == expected


def test_resume_stream_seeks_to_the_bookmark_after_checking_the_line_before_it(tmp_path):
    content = b"one\ntwo\nthree\nfour\n"
    stream = stream_over(tmp_path, content, piece=True,
                         resume=None)
    assert list(stream) == [b"one\n", b"two\n", b"three\n", b"four\n"]
    resumed = meter._iter_approved_lines(
        tmp_path / "synthetic-source", "records.jsonl", meter.MAX_BATCH_BYTES, piece=True,
        resume=resume_request(tmp_path, 8, b"two\n"))
    assert list(resumed) == [b"three\n", b"four\n"]
    assert resumed.terminal_reason is None and resumed.resume_failure is None
    assert resumed.end_offset == len(content) and resumed.complete_lines == 2
    assert resumed.tail_digest == sha256_of(b"four\n")
    assert resumed.bytes_read == 8 + len(b"three\nfour\n")
    assert resumed.open_identity["size"] == len(content)
    start = meter._iter_approved_lines(
        tmp_path / "synthetic-source", "records.jsonl", meter.MAX_BATCH_BYTES, piece=True,
        resume=resume_request(tmp_path, 0))
    assert len(list(start)) == 4 and start.resume_failure is None


@pytest.mark.parametrize("name, changes, offset, line", [
    ("file_replaced", {"ino": 1}, 8, b"two\n"),
    ("file_replaced", {"dev": 1}, 8, b"two\n"),
    ("cursor_past_end", {}, 1000, b"two\n"),
    ("not_line_boundary", {}, 6, b"two\n"),
    ("digest_mismatch", {}, 8, b"one\n"),
    ("digest_mismatch", {"digest": "f" * 64}, 8, b"two\n"),
], ids=["wrong-inode", "wrong-device", "past-the-end", "inside-a-line",
        "wrong-line", "wrong-digest"])
def test_resume_stream_failures_yield_no_line_and_name_the_check(
        tmp_path, name, changes, offset, line):
    stream_over(tmp_path, b"one\ntwo\nthree\nfour\n")
    failed = meter._iter_approved_lines(
        tmp_path / "synthetic-source", "records.jsonl", meter.MAX_BATCH_BYTES, piece=True,
        resume=resume_request(tmp_path, offset, line, **changes))
    assert list(failed) == []
    assert failed.terminal_reason is None
    assert failed.resume_failure == name
    assert failed.complete_lines == 0


def test_resume_stream_reports_a_closed_checks_order(tmp_path):
    stream_over(tmp_path, b"one\ntwo\n")
    both = meter._iter_approved_lines(
        tmp_path / "synthetic-source", "records.jsonl", meter.MAX_BATCH_BYTES, piece=True,
        resume=resume_request(tmp_path, 1000, b"two\n", ino=1))
    assert list(both) == [] and both.resume_failure == "file_replaced"


def test_reread_stream_reads_from_zero_and_checks_the_line_at_the_bookmark(tmp_path):
    content = b"one\ntwo\nthree\n"

    def reread(offset, line=None, **changes):
        stream_over(tmp_path, content)
        return meter._iter_approved_lines(
            tmp_path / "synthetic-source", "records.jsonl", meter.MAX_REREAD_BYTES,
            piece=True, reread=True,
            resume=resume_request(tmp_path, offset, line, **changes))

    good = reread(8, b"two\n")
    assert list(good) == [b"one\n", b"two\n", b"three\n"]
    assert good.resume_failure is None and good.checkpoint_line == 2
    assert good.end_offset == len(content) and good.complete_lines == 3
    assert good.terminal_reason is None
    start = reread(0)
    assert len(list(start)) == 3 and start.checkpoint_line == 0
    assert start.resume_failure is None
    mismatch = reread(8, b"one\n")
    assert len(list(mismatch)) == 3 and mismatch.resume_failure == "digest_mismatch"
    inside = reread(6, b"two\n")
    assert len(list(inside)) == 3 and inside.resume_failure == "not_line_boundary"
    assert inside.checkpoint_line is None
    replaced = reread(8, b"two\n", ino=1)
    assert list(replaced) == [] and replaced.resume_failure == "file_replaced"
    past = reread(500, b"two\n")
    assert list(past) == [] and past.resume_failure == "cursor_past_end"


@pytest.mark.parametrize("options", [
    {"resume": {"dev": 1, "ino": 1, "offset": 4, "digest": None}},
    {"piece": True, "resume": {"dev": 1, "ino": 1, "offset": 0, "digest": "ab"}},
    {"piece": True, "resume": {"dev": 1, "ino": 1, "offset": -1, "digest": None}},
    {"piece": True, "resume": {"dev": 1, "ino": 1, "offset": 4}},
    {"piece": True, "resume": [1, 2]},
    {"piece": True, "resume": {"dev": 1, "ino": 1, "offset": 0, "digest": None},
     "tail": True},
    {"piece": True, "reread": True},
    {"piece": True, "reread": "yes",
     "resume": {"dev": 1, "ino": 1, "offset": 0, "digest": None}},
], ids=["resume-without-piece", "digest-too-short", "negative-offset", "missing-field",
        "not-a-mapping", "resume-with-tail", "reread-without-resume", "reread-not-bool"])
def test_stream_refuses_inconsistent_resume_keywords(tmp_path, options):
    stream = stream_over(tmp_path, b"one\n", **options)
    assert list(stream) == [] and stream.terminal_reason is not None


def test_resume_stream_fails_closed_when_it_cannot_seek(tmp_path, monkeypatch):
    stream_over(tmp_path, b"one\ntwo\nthree\n")
    request = resume_request(tmp_path, 8, b"two\n")

    def refuse(*_args, **_kwargs):
        raise OSError("SECRET-SEEK")

    monkeypatch.setattr(meter.os, "lseek", refuse)
    failed = meter._iter_approved_lines(
        tmp_path / "synthetic-source", "records.jsonl", meter.MAX_BATCH_BYTES,
        piece=True, resume=request)
    assert list(failed) == []
    assert failed.terminal_reason == "source_read_unavailable"
    assert failed.resume_failure is None


def test_the_run_limit_is_never_below_the_reread_limit():
    assert meter.MAX_RUN_READ_BYTES >= meter.MAX_REREAD_BYTES
    assert meter.MAX_RUN_READ_BYTES == 1024 * 1024 * 1024
    assert meter.MAX_RUN_EVENTS == 200_000
    assert not hasattr(meter, "MAX_TOTAL_SOURCE_BYTES")


def claude_lines(*message_ids, timestamp=STAMP, newline=b"\n", session="session-a"):
    return b"".join(json.dumps(claude_record(item, timestamp, session)).encode() + newline
                    for item in message_ids)


OLD = "2026-11-04T12:00:00Z"   # before the patched start
NEW = "2026-11-05T12:00:00Z"   # after it


def keys_of(ledger):
    return sorted(event["event_key"] for event in ledger["events"])


def event_key_for(message_id, session="session-a"):
    return meter._digest("claude", "request-" + message_id, message_id)


def grow(path, data):
    with open(path, "ab") as handle:
        handle.write(data)


def run_until_caught_up(home, limit=40):
    results = []
    for _ in range(limit):
        result = meter._refresh_ledger(home)
        results.append(result)
        reasons = set(ledger_of(home)["coverage"]["reasons"])
        partial = bool(reasons & {"catching_up", "source_too_large"})
        assert result["status"] == ("partial" if partial else "written"), result
        if not partial:
            return results
    raise AssertionError("still catching up")


def test_a_grown_claude_log_counts_only_the_appended_lines(tmp_path, monkeypatch):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    log.write_bytes(claude_lines("old-1", "old-2", timestamp=OLD))
    assert meter._refresh_ledger(home)["events"] == 0
    bookmark = cursor_for(ledger_of(home), "claude-source")

    grow(log, claude_lines("new-1", "new-2", timestamp=NEW))
    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 2
    assert keys_of(ledger) == sorted([event_key_for("new-1"), event_key_for("new-2")])
    cursor = cursor_for(ledger, "claude-source")
    assert cursor["offset"] == log.stat().st_size == cursor["size"]
    assert cursor["line"] == 2 and cursor["generation"] == 1
    assert cursor["digest"] == sha256_of(claude_lines("new-2", timestamp=NEW))
    assert cursor["dev"] == bookmark["dev"] and cursor["ino"] == bookmark["ino"]
    assert not {"resume_failed_file_replaced", "resume_failed_digest_mismatch",
                "catching_up", "partial_tail"} & set(ledger["coverage"]["reasons"])
    assert meter._refresh_ledger(home)["events"] == 2


def test_resumed_lines_equal_the_same_lines_read_as_a_new_log(tmp_path, monkeypatch):
    for name in ("grown", "fresh"):
        (tmp_path / name).mkdir()
    grown_home, grown_root, *_ = c1_home(tmp_path / "grown", monkeypatch)
    fresh_home, fresh_root, *_ = c1_home(tmp_path / "fresh", monkeypatch)
    log = grown_root / "session.jsonl"
    log.write_bytes(claude_lines("old-1", timestamp=OLD))
    meter._refresh_ledger(grown_home)
    meter._refresh_ledger(fresh_home)
    new_lines = claude_lines("new-1", "new-2", timestamp=NEW)
    grow(log, new_lines)
    (fresh_root / "session.jsonl").write_bytes(new_lines)
    meter._refresh_ledger(grown_home)
    meter._refresh_ledger(fresh_home)
    grown, fresh = ledger_of(grown_home), ledger_of(fresh_home)
    assert grown["events"] == fresh["events"] and len(grown["events"]) == 2
    assert grown["aggregates"] == fresh["aggregates"]


def test_an_unchanged_log_is_not_opened(tmp_path, monkeypatch):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    log.write_bytes(claude_lines("old-1", timestamp=OLD))
    opened = []
    real_open = os.open

    def counting_open(target, *args, **kwargs):
        if str(target).endswith("session.jsonl"):
            opened.append(target)
        return real_open(target, *args, **kwargs)

    monkeypatch.setattr(meter.os, "open", counting_open)
    meter._refresh_ledger(home)
    assert len(opened) == 1                 # the start's tail read
    meter._refresh_ledger(home)
    assert len(opened) == 1                 # unchanged: not opened again
    grow(log, claude_lines("new-1", timestamp=NEW))
    assert meter._refresh_ledger(home)["events"] == 1
    assert len(opened) == 2


@pytest.mark.parametrize("name", [
    "file_replaced", "cursor_past_end", "not_line_boundary", "digest_mismatch"])
def test_a_failed_resume_check_restarts_and_records_why(tmp_path, monkeypatch, name):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    old = claude_lines("old-1", "old-2", timestamp=OLD)
    new = claude_lines("new-1", "new-2", timestamp=NEW)
    log.write_bytes(old)
    assert meter._refresh_ledger(home)["events"] == 0
    expected = ["new-1", "new-2"]
    if name == "file_replaced":
        successor = claude_root / "successor.tmp"    # made while the old file still exists,
        successor.write_bytes(old + new)             # so it cannot get the old inode number
        os.replace(successor, log)                   # (ext4 hands a freed number straight back)
    elif name == "cursor_past_end":
        with open(log, "r+b") as handle:             # same file, now shorter
            handle.truncate(0)
            handle.write(claude_lines("new-1", timestamp=NEW))
        expected = ["new-1"]
        assert log.stat().st_size < len(old)
    elif name == "not_line_boundary":
        ledger_path = home / ".cairn" / "meter" / "ledger.json"
        ledger = json.loads(ledger_path.read_bytes())
        ledger["cursors"][0]["offset"] -= 3          # a saved offset inside a line
        ledger_path.write_bytes(as_bytes(ledger))
        grow(log, new)
    else:
        last = claude_lines("old-2", timestamp=OLD)
        assert b"SECRET-BODY" in last and old.endswith(last)
        edit_at = len(old) - len(last) + last.index(b"SECRET-BODY")
        with open(log, "r+b") as handle:             # same length, same file
            handle.seek(edit_at)
            handle.write(b"SECRET-B0DY")
        assert log.stat().st_size == len(old)
        grow(log, new)

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written", result
    assert keys_of(ledger) == sorted(event_key_for(item) for item in expected)
    assert "resume_failed_" + name in ledger["coverage"]["reasons"]
    cursor = cursor_for(ledger, "claude-source")
    assert cursor["generation"] == 2 and cursor["offset"] == log.stat().st_size
    assert cursor["line"] == len(expected) + (2 if name != "cursor_past_end" else 0)


def test_a_torn_tail_is_left_for_the_next_run_and_counts_once(tmp_path, monkeypatch):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    old = claude_lines("old-1", timestamp=OLD)
    log.write_bytes(old)
    meter._refresh_ledger(home)
    whole = claude_lines("new-0", timestamp=NEW)
    torn = claude_lines("new-1", timestamp=NEW)
    half = len(torn) // 2
    grow(log, whole + torn[:half])

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 1
    cursor = cursor_for(ledger, "claude-source")
    assert cursor["offset"] == len(old) + len(whole)
    assert cursor["size"] == log.stat().st_size
    assert "partial_tail" not in ledger["coverage"]["reasons"]
    grow(log, torn[half:])
    assert meter._refresh_ledger(home)["events"] == 2
    assert meter._refresh_ledger(home)["events"] == 2
    assert keys_of(ledger_of(home)) == sorted([event_key_for("new-0"), event_key_for("new-1")])


def test_an_append_during_a_read_is_left_for_the_next_run(tmp_path, monkeypatch):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    log.write_bytes(claude_lines("old-1", timestamp=OLD))
    meter._refresh_ledger(home)
    grow(log, claude_lines("new-1", timestamp=NEW))
    real_read = os.read
    state = {"appended": False}

    def read_then_append(descriptor, size):
        data = real_read(descriptor, size)
        if not state["appended"] and b'"sessionId"' in data:
            state["appended"] = True
            grow(log, claude_lines("late-1", timestamp=NEW))
        return data

    monkeypatch.setattr(meter.os, "read", read_then_append)

    result = meter._refresh_ledger(home)

    assert state["appended"]
    assert result["status"] == "written" and result["events"] == 1
    assert keys_of(ledger_of(home)) == [event_key_for("new-1")]
    assert meter._refresh_ledger(home)["events"] == 2
    assert keys_of(ledger_of(home)) == sorted([event_key_for("new-1"), event_key_for("late-1")])


def test_a_crlf_log_resumes_after_its_last_line(tmp_path, monkeypatch):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    old = claude_lines("old-1", "old-2", timestamp=OLD, newline=b"\r\n")
    log.write_bytes(old)
    meter._refresh_ledger(home)
    bookmark = cursor_for(ledger_of(home), "claude-source")
    assert bookmark["offset"] == len(old)
    assert bookmark["digest"] == sha256_of(claude_lines("old-2", timestamp=OLD, newline=b"\r\n"))
    new = claude_lines("new-1", timestamp=NEW, newline=b"\r\n")
    grow(log, new)

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["events"] == 1 and keys_of(ledger) == [event_key_for("new-1")]
    assert cursor_for(ledger, "claude-source")["generation"] == 1
    assert cursor_for(ledger, "claude-source")["digest"] == sha256_of(new)
    assert not [reason for reason in ledger["coverage"]["reasons"]
                if reason.startswith("resume_failed")]


def usage_record(message_id, input_tokens, timestamp=NEW):
    record = claude_record(message_id, timestamp)
    record["message"]["usage"]["input_tokens"] = input_tokens
    return json.dumps(record).encode() + b"\n"


def test_a_replys_repeated_usage_lines_count_once_across_runs(tmp_path, monkeypatch):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    log.write_bytes(claude_lines("old-1", timestamp=OLD))
    meter._refresh_ledger(home)
    grow(log, usage_record("reply-1", 10))
    meter._refresh_ledger(home)
    grow(log, usage_record("reply-1", 10))
    meter._refresh_ledger(home)

    ledger = ledger_of(home)
    event, = ledger["events"]
    assert event["event_key"] == event_key_for("reply-1")
    assert event["kinds"]["fresh_input"] == 10 and "conflicting_usage" not in event["reasons"]
    assert ledger["aggregates"][0]["events"] == 1


def test_differing_usage_for_one_reply_is_a_conflict_as_in_a_full_read(tmp_path, monkeypatch):
    for name in ("split", "whole"):
        (tmp_path / name).mkdir()
    split_home, split_root, *_ = c1_home(tmp_path / "split", monkeypatch)
    whole_home, whole_root, *_ = c1_home(tmp_path / "whole", monkeypatch)
    log = split_root / "session.jsonl"
    log.write_bytes(claude_lines("old-1", timestamp=OLD))
    meter._refresh_ledger(split_home)
    meter._refresh_ledger(whole_home)
    grow(log, usage_record("reply-1", 10))
    meter._refresh_ledger(split_home)
    grow(log, usage_record("reply-1", 99))
    meter._refresh_ledger(split_home)
    (whole_root / "session.jsonl").write_bytes(usage_record("reply-1", 10) + usage_record("reply-1", 99))
    meter._refresh_ledger(whole_home)

    split_event, = ledger_of(split_home)["events"]
    whole_event, = ledger_of(whole_home)["events"]
    assert "conflicting_usage" in split_event["reasons"]
    assert split_event["kinds"] == whole_event["kinds"] == {
        "fresh_input": None, "cache_read": None, "cache_write": None, "output": None}
    assert split_event == whole_event


@pytest.mark.parametrize("limit", ["lines", "bytes"])
def test_a_small_batch_limit_ends_a_piece_on_a_line_boundary_and_later_runs_finish(
        tmp_path, monkeypatch, limit):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    old = claude_lines("old-1", timestamp=OLD)
    log.write_bytes(old)
    meter._refresh_ledger(home)
    names = [f"new-{index}" for index in range(1, 7)]
    one_line = len(claude_lines("new-1", timestamp=NEW))
    grow(log, claude_lines(*names, timestamp=NEW))
    if limit == "lines":
        monkeypatch.setattr(meter, "MAX_BATCH_LINES", 2)
    else:
        # the window before the bookmark also counts, so keep it to a line or so
        monkeypatch.setattr(meter, "MAX_LINE", one_line + 10)
        monkeypatch.setattr(meter, "MAX_BATCH_BYTES", (one_line + 11) + 2 * one_line + 10)

    first = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert first["status"] == "partial" and first["events"] == 2
    assert "catching_up" in ledger["coverage"]["reasons"]
    cursor = cursor_for(ledger, "claude-source")
    assert cursor["offset"] == len(old) + 2 * one_line and cursor["line"] == 2
    assert cursor["size"] == cursor["offset"] < log.stat().st_size
    run_until_caught_up(home)
    final = ledger_of(home)
    assert keys_of(final) == sorted(event_key_for(item) for item in names)
    assert cursor_for(final, "claude-source")["offset"] == log.stat().st_size


def test_a_small_event_limit_leaves_later_logs_for_later_runs(tmp_path, monkeypatch):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    for name in ("a.jsonl", "b.jsonl", "c.jsonl"):
        (claude_root / name).write_bytes(claude_lines("old-" + name, timestamp=OLD))
    meter._refresh_ledger(home)
    for name in ("a.jsonl", "b.jsonl", "c.jsonl"):
        grow(claude_root / name, claude_lines(name + "-1", name + "-2", timestamp=NEW,
                                              session=name))
    monkeypatch.setattr(meter, "MAX_RUN_EVENTS", 2)

    first = meter._refresh_ledger(home)

    assert first["status"] == "partial" and first["events"] == 2
    assert "catching_up" in ledger_of(home)["coverage"]["reasons"]
    run_until_caught_up(home)
    assert len(ledger_of(home)["events"]) == 6


@pytest.mark.parametrize("failing", ["seek", "open"])
def test_a_failing_seek_or_identity_read_is_unavailable_and_leaves_the_ledger(
        tmp_path, monkeypatch, failing):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    log.write_bytes(claude_lines("old-1", timestamp=OLD))
    meter._refresh_ledger(home)
    cursors = ledger_of(home)["cursors"]
    grow(log, claude_lines("new-1", timestamp=NEW))

    def refuse(*_args, **_kwargs):
        raise OSError("SECRET-SYSCALL")

    if failing == "seek":
        monkeypatch.setattr(meter.os, "lseek", refuse)
    else:
        real_open = os.open

        def open_then_fail(target, *args, **kwargs):
            if str(target).endswith("session.jsonl"):
                refuse()
            return real_open(target, *args, **kwargs)

        monkeypatch.setattr(meter.os, "open", open_then_fail)

    result = meter._refresh_ledger(home)

    assert result["status"] == "partial" and result["reason"] == "catching_up"
    assert ledger_of(home)["cursors"] == cursors      # the log waits for the next run
    assert "SECRET" not in json.dumps(result)


def test_public_refresh_accepts_an_exact_8_mib_line_without_leaking_or_recounting(
        tmp_path, monkeypatch):
    limit = 8 * 1024 * 1024
    home, source, project, _config_path = c2_home(tmp_path, records=codex())
    log = source / "session.jsonl"

    started = meter._refresh_ledger(home)
    assert started["status"] == "written" and started["events"] == 0, started
    context = row("turn_context", {
        "turn_id": "turn-large", "cwd": str(project),
        "synthetic_padding": "C10_SYNTHETIC_PADDING_MUST_NOT_ESCAPE_"})
    context["payload"]["synthetic_padding"] += "x" * (
        limit - len(encoded([context])[0]))
    context_line = encoded([context])[0]
    assert len(context_line) == limit
    owner = "019a0000-0000-7000-8000-000000000001"
    usage_line = encoded([codex_direct(
        owner, owner, "turn-large", "turn-large", "response-large", 31, 31, 31)])[0]
    log.write_bytes(log.read_bytes() + context_line + usage_line)

    result = meter._refresh_ledger(home)

    ledger_path = home / ".cairn" / "meter" / "ledger.json"
    export_path = project / "dev" / "measurement" / "meter.json"
    ledger_bytes = ledger_path.read_bytes()
    export_bytes = export_path.read_bytes()
    ledger = meter._load_ledger(ledger_bytes)
    export = json.loads(export_bytes)
    assert result["status"] == "written" and result["events"] == 1, result
    assert len(ledger["events"]) == 1
    assert ledger["events"][0]["project_alias"] == "sample"
    assert cursor_for(ledger, "codex-source")["offset"] == log.stat().st_size
    assert sum(item["events"] for item in export["aggregates"]) == 1
    assert b"C10_SYNTHETIC_PADDING_MUST_NOT_ESCAPE_" not in ledger_bytes
    assert b"C10_SYNTHETIC_PADDING_MUST_NOT_ESCAPE_" not in export_bytes
    assert b"synthetic_padding" not in export_bytes

    repeated = meter._refresh_ledger(home)
    assert repeated["status"] == "written" and repeated["events"] == 1, repeated
    assert len(ledger_of(home)["events"]) == 1


def test_public_refresh_refuses_one_byte_over_8_mib_without_publication_changes(
        tmp_path, monkeypatch):
    limit = 8 * 1024 * 1024
    home, source, project, _config_path = c2_home(tmp_path, records=codex())
    log = source / "session.jsonl"
    started = meter._refresh_ledger(home)
    assert started["status"] == "written" and started["events"] == 0, started

    context = row("turn_context", {
        "turn_id": "turn-over-limit", "cwd": str(project),
        "synthetic_padding": "C10_SYNTHETIC_PADDING_MUST_NOT_ESCAPE_"})
    context["payload"]["synthetic_padding"] += "x" * (
        limit + 1 - len(encoded([context])[0]))
    context_line = encoded([context])[0]
    assert len(context_line) == limit + 1
    owner = "019a0000-0000-7000-8000-000000000001"
    usage_line = encoded([codex_direct(
        owner, owner, "turn-over-limit", "turn-over-limit", "response-over-limit",
        31, 31, 31)])[0]
    log.write_bytes(log.read_bytes() + context_line + usage_line)
    ledger_path = home / ".cairn" / "meter" / "ledger.json"
    export_path = project / "dev" / "measurement" / "meter.json"
    previous_ledger = ledger_path.read_bytes()
    previous_export = export_path.read_bytes()

    result = meter._refresh_ledger(home)

    assert result["status"] == "unavailable"
    assert result["reason"] == "source_budget_exceeded"
    assert ledger_path.read_bytes() == previous_ledger
    assert export_path.read_bytes() == previous_export


def test_a_line_over_the_line_limit_is_still_source_budget_exceeded(tmp_path, monkeypatch):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    log.write_bytes(claude_lines("old-1", timestamp=OLD))
    meter._refresh_ledger(home)
    monkeypatch.setattr(meter, "MAX_LINE", 100)
    grow(log, b"x" * 101 + b"\n")
    assert meter._refresh_ledger(home)["reason"] == "source_budget_exceeded"


@pytest.mark.parametrize("over_by", [0, 1], ids=["exact-bytes", "one-byte-under"])
def test_refresh_total_source_budget_is_all_or_unavailable(tmp_path, monkeypatch, over_by):
    """The run limit counts bytes read, window included; over it the rest is deferred.

    The bytes a resume needs are the window before the bookmark (the whole old
    part here) plus the appended line. One byte under: the line is not whole, the
    cursor stays, the run says catching_up and does not fail.
    """
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    old = claude_lines("old-1", "old-2", timestamp=OLD)
    log.write_bytes(old)
    meter._refresh_ledger(home)
    bookmark = cursor_for(ledger_of(home), "claude-source")
    new = claude_lines("new-1", timestamp=NEW)
    grow(log, new)
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", len(old) + len(new) - over_by)

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == ("partial" if over_by else "written")
    reasons = ledger["coverage"]["reasons"]
    if over_by:
        assert result["events"] == 0 and "catching_up" in reasons
        cursor = cursor_for(ledger, "claude-source")
        assert (cursor["offset"], cursor["digest"], cursor["line"]) == (
            bookmark["offset"], bookmark["digest"], 0)
        assert cursor["size"] == bookmark["offset"] < log.stat().st_size
        monkeypatch.undo()
        monkeypatch.setattr(meter, "_now_utc", lambda: CLOCK)
        assert meter._refresh_ledger(home)["events"] == 1
    else:
        assert result["events"] == 1 and "catching_up" not in reasons


def test_the_start_run_counts_tail_and_first_line_bytes_and_defers_the_rest(
        tmp_path, monkeypatch):
    home, claude_root, codex_root, *_ = c1_home(tmp_path, monkeypatch)
    old = claude_lines("old-1", "old-2", timestamp=OLD)
    for name in ("a.jsonl", "b.jsonl"):
        (claude_root / name).write_bytes(old)
        before = int(datetime(2026, 11, 1, tzinfo=timezone.utc).timestamp() * 1e9)
        os.utime(claude_root / name, ns=(before, before))
    tail_reservation = 2 * meter.MAX_LINE + 2
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", tail_reservation + len(old) - 1)

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "partial" and result["reason"] == "catching_up"
    assert [item["file_key"] for item in ledger["cursors"]] == [
        meter._digest("cursor", "claude-source", "a.jsonl")]
    assert "catching_up" in ledger["coverage"]["reasons"]
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", 1024 ** 3)
    assert meter._refresh_ledger(home)["events"] == 0
    assert len(ledger_of(home)["cursors"]) == 2


@pytest.mark.parametrize("tool", ["claude", "codex"])
def test_a_start_bookmark_waits_for_its_full_read_reservation(
        tmp_path, monkeypatch, tool):
    records = {"claude_logs": {}, "codex_logs": {}}
    if tool == "claude":
        data = claude_lines("old-1", timestamp=OLD)
    else:
        codex_records = codex_host_cwd()
        for record in codex_records:
            record["timestamp"] = OLD
        data = b"".join(encoded(codex_records))
    records[f"{tool}_logs"] = {"session.jsonl": data}
    home, claude_root, codex_root, _project, _config = c1_home(
        tmp_path, monkeypatch, **records)
    source_fd_set = set()
    source_reads = []
    real_open, real_read, real_close = os.open, os.read, os.close

    def tracking_open(path, *args, **kwargs):
        fd = real_open(path, *args, **kwargs)
        if isinstance(path, str) and Path(path).name == "session.jsonl":
            source_fd_set.add(fd)
        return fd

    def tracking_read(fd, size):
        block = real_read(fd, size)
        if fd in source_fd_set:
            source_reads.append(len(block))
        return block

    def tracking_close(fd):
        source_fd_set.discard(fd)
        return real_close(fd)

    monkeypatch.setattr(meter.os, "open", tracking_open)
    monkeypatch.setattr(meter.os, "read", tracking_read)
    monkeypatch.setattr(meter.os, "close", tracking_close)
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", 1)

    first = meter._refresh_ledger(home)

    assert (first["status"], first["reason"]) == ("partial", "catching_up")
    assert source_reads == []
    assert ledger_of(home)["cursors"] == []

    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", 1024 ** 3)
    second = meter._refresh_ledger(home)
    assert second["status"] == "written" and second["events"] == 0
    assert source_reads and len(ledger_of(home)["cursors"]) == 1


def test_a_run_with_no_budget_opens_no_log_and_keeps_its_cursors(tmp_path, monkeypatch):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    log.write_bytes(claude_lines("old-1", timestamp=OLD))
    meter._refresh_ledger(home)
    kept = ledger_of(home)["cursors"]
    grow(log, claude_lines("new-1", timestamp=NEW))
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", 0)
    result = meter._refresh_ledger(home)
    assert result["status"] == "partial" and result["events"] == 0
    ledger = ledger_of(home)
    assert ledger["cursors"] == kept and "catching_up" in ledger["coverage"]["reasons"]


def test_a_resume_window_that_does_not_fit_the_piece_defers_the_log(tmp_path, monkeypatch):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    old = claude_lines("old-1", "old-2", timestamp=OLD)
    log.write_bytes(old)
    meter._refresh_ledger(home)
    bookmark = cursor_for(ledger_of(home), "claude-source")
    grow(log, claude_lines("new-1", timestamp=NEW))
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", len(old) - 1)

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    cursor = cursor_for(ledger, "claude-source")
    assert result["status"] == "partial" and result["events"] == 0
    assert "catching_up" in ledger["coverage"]["reasons"]
    assert (cursor["offset"], cursor["digest"], cursor["line"], cursor["generation"]) == (
        bookmark["offset"], bookmark["digest"], 0, 1)
    assert cursor["size"] == bookmark["offset"]


def test_a_fresh_read_drops_events_older_than_the_fold_window(tmp_path, monkeypatch):
    home, claude_root, _codex_root, _project, config_path = c1_home(tmp_path, monkeypatch)
    (claude_root / "session.jsonl").write_bytes(
        claude_lines("too-old", timestamp="2026-10-21T23:59:59Z")
        + claude_lines("edge", timestamp="2026-10-22T00:00:00Z"))
    config = meter.validate_config_bytes(config_path.read_bytes())
    starts = [{"source_alias": alias, "started_at": "2026-09-01T00:00:00Z"}
              for alias in ("claude-source", "codex-source")]

    events, *_rest = meter._scan_approved_sources(config, [], starts=starts, now=CLOCK)

    assert [event["event_key"] for event in events] == [event_key_for("edge")]


# ---- Codex re-read, parent context and grown fork children (plan C3) ---------

CODEX_OWNER = "019a0000-0000-7000-8000-000000000001"


def codex_log_header(owner=CODEX_OWNER):
    return row("session_meta", {"id": owner, "session_id": owner, "source": "cli",
                                "thread_source": "user", "history_mode": "legacy"})


def codex_turn(project, owner, turn, input_count, thread_count, *, timestamp=NEW, waits=()):
    """One whole Codex turn: its context, one usage line, then one wait per item."""
    records = [
        row("turn_context", {"turn_id": turn, "root_turn_id": turn,
                             "cwd": str(project), "model": "gpt-5.3-codex"}),
        codex_direct(owner, owner, turn, turn, "response-" + turn,
                     input_count, input_count, thread_count),
    ]
    for record in records:
        record["timestamp"] = timestamp
    for item_id, start in waits:
        wait = timing_record(item_id=item_id, start=start, end=start + 1000)
        wait["payload"]["thread_id"] = owner
        wait["payload"]["turn_id"] = turn
        records.append(wait)
    return records


def codex_event_key(owner, turn):
    return meter._digest("codex", owner, "response-" + turn)


def codex_wait_key(owner, turn, item_id):
    return meter._digest("codex-wait", "codex", owner, turn, item_id)


def codex_home(tmp_path, monkeypatch):
    return c2_home(tmp_path)


def write_codex(path, records):
    path.write_bytes(b"".join(encoded(records)))


def cursor_key(name, alias="codex-source"):
    return meter._digest("cursor", alias, name)


def cursors_of(ledger):
    return {item["file_key"]: item for item in ledger["cursors"]}


def opened_names(monkeypatch):
    """Patch os.open and return the list of log names opened from now on."""
    names, real_open = [], os.open

    def recording_open(target, *args, **kwargs):
        if isinstance(target, (str, Path)) and str(target).endswith(".jsonl"):
            names.append(Path(target).name)
        return real_open(target, *args, **kwargs)

    monkeypatch.setattr(meter.os, "open", recording_open)
    return names


def edit_ledger(home, change):
    path = home / ".cairn" / "meter" / "ledger.json"
    ledger = json.loads(path.read_bytes())
    change(ledger)
    path.write_bytes(as_bytes(ledger))


def test_a_grown_codex_log_counts_only_the_new_turn_and_equals_a_fresh_read(
        tmp_path, monkeypatch):
    clock_ms = int(CLOCK.timestamp() * 1000)
    old_wait, new_wait = ("old-wait", clock_ms + 60_000), ("new-wait", clock_ms + 120_000)
    homes = {}
    for name in ("grown", "fresh"):
        (tmp_path / name).mkdir()
        homes[name] = codex_home(tmp_path / name, monkeypatch)

    def records(project, *, new):
        rows = [codex_log_header()] + codex_turn(
            project, CODEX_OWNER, "turn-old", 10, 10, timestamp=OLD, waits=[old_wait])
        if new:
            rows += codex_turn(project, CODEX_OWNER, "turn-new", 20, 30, waits=[new_wait])
        return rows

    home, source, project, _config = homes["grown"]
    write_codex(source / "session.jsonl", records(project, new=False))
    assert meter._refresh_ledger(home)["events"] == 0
    grow(source / "session.jsonl", b"".join(encoded(records(project, new=True)[
        len(records(project, new=False)):])))
    result = meter._refresh_ledger(home)
    grown = ledger_of(home)

    fresh_home, fresh_source, fresh_project, _config = homes["fresh"]
    assert meter._refresh_ledger(fresh_home)["events"] == 0
    write_codex(fresh_source / "session.jsonl", records(fresh_project, new=True))
    meter._refresh_ledger(fresh_home)
    fresh = ledger_of(fresh_home)

    new_key = codex_event_key(CODEX_OWNER, "turn-new")
    assert result["status"] == "written" and result["events"] == 1
    assert keys_of(grown) == [new_key]            # the old turn adds no event key at all
    event, = grown["events"]
    assert event["project_alias"] == "sample" and event["ownership"] == "proven"
    assert event["thread_key"] == meter._digest("codex", CODEX_OWNER)
    assert [wait["wait_key"] for wait in grown["waits"]] == [
        codex_wait_key(CODEX_OWNER, "turn-new", "new-wait")]
    fresh_event = next(item for item in fresh["events"] if item["event_key"] == new_key)
    assert event == fresh_event
    fresh_wait = next(item for item in fresh["waits"]
                      if item["wait_key"] == codex_wait_key(CODEX_OWNER, "turn-new", "new-wait"))
    assert grown["waits"] == [fresh_wait]
    cursor = cursor_for(grown, "codex-source")
    assert cursor["generation"] == 1 and cursor["offset"] == cursor["size"]
    assert cursor["line"] == len(records(project, new=True))


def fork_start(tmp_path, monkeypatch):
    """A Codex home whose parent log is bookmarked by the start run."""
    home, source, project, _config = codex_home(tmp_path, monkeypatch)
    parent_rows, child_rows, parent, child = codex_fork_fixture(project)
    write_codex(source / "parent.jsonl", parent_rows)
    assert meter._refresh_ledger(home)["events"] == 0
    return home, source, project, parent_rows, child_rows, parent, child


CHILD_EVENT = "response-child"


def test_a_child_is_verified_against_a_parent_that_grew_since_the_start(tmp_path, monkeypatch):
    home, source, project, _parent_rows, child_rows, parent, child = fork_start(
        tmp_path, monkeypatch)
    write_codex(source / "child.jsonl", child_rows)
    grow(source / "parent.jsonl", b"".join(encoded(
        codex_turn(project, parent, "turn-parent-2", 20, 120))))

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 2
    assert keys_of(ledger) == sorted([meter._digest("codex", child, CHILD_EVENT),
                                      codex_event_key(parent, "turn-parent-2")])
    assert meter._digest("codex", parent, "response-parent") not in keys_of(ledger)
    lineage, = ledger["lineages"]
    assert lineage["state"] == "verified" and len(lineage["proofs"]) == 1
    child_event = next(item for item in ledger["events"]
                       if item["event_key"] == meter._digest("codex", child, CHILD_EVENT))
    assert child_event["lineage_key"] == lineage["lineage_key"]
    assert child_event["ownership"] == "proven" and child_event["project_alias"] == "sample"
    assert "fork_parent_unavailable" not in ledger["coverage"]["reasons"]


def test_a_parent_that_was_not_read_is_read_as_context_and_never_changed(tmp_path, monkeypatch):
    home, source, _project, parent_rows, child_rows, _parent, child = fork_start(
        tmp_path, monkeypatch)
    parent_size = len(b"".join(encoded(parent_rows)))
    child_size = len(b"".join(encoded(child_rows)))
    parent_cursor = cursors_of(ledger_of(home))[cursor_key("parent.jsonl")]
    write_codex(source / "child.jsonl", child_rows)
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", child_size + parent_size)

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 1
    lineage, = ledger["lineages"]
    assert lineage["state"] == "verified"
    event, = ledger["events"]
    assert event["event_key"] == meter._digest("codex", child, CHILD_EVENT)
    assert event["project_alias"] == "sample" and event["ownership"] == "proven"
    assert cursors_of(ledger)[cursor_key("parent.jsonl")] == parent_cursor
    assert "catching_up" not in ledger["coverage"]["reasons"]
    assert "fork_parent_unavailable" not in ledger["coverage"]["reasons"]


def test_a_child_is_dropped_when_the_run_cannot_pay_for_its_parent(tmp_path, monkeypatch):
    home, source, _project, parent_rows, child_rows, _parent, child = fork_start(
        tmp_path, monkeypatch)
    parent_size = len(b"".join(encoded(parent_rows)))
    child_size = len(b"".join(encoded(child_rows)))
    parent_cursor = cursors_of(ledger_of(home))[cursor_key("parent.jsonl")]
    write_codex(source / "child.jsonl", child_rows)
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", child_size + parent_size - 1)
    opened = opened_names(monkeypatch)

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "partial" and result["events"] == 0
    assert "parent.jsonl" not in opened and "child.jsonl" in opened
    assert "catching_up" in ledger["coverage"]["reasons"]
    assert ledger["events"] == [] and ledger["lineages"] == []
    assert cursors_of(ledger) == {cursor_key("parent.jsonl"): parent_cursor}
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", 1024 ** 3)
    assert meter._refresh_ledger(home)["events"] == 1
    again = ledger_of(home)
    assert again["lineages"][0]["state"] == "verified"
    assert "catching_up" not in again["coverage"]["reasons"]
    assert cursor_key("child.jsonl") in cursors_of(again)


def test_a_parent_the_run_already_read_is_not_read_again_as_context(tmp_path, monkeypatch):
    home, source, project, parent_rows, child_rows, parent, _child = fork_start(
        tmp_path, monkeypatch)
    write_codex(source / "copy.jsonl", parent_rows)       # a second log of the same parent
    os.utime(source / "copy.jsonl", ns=(1, 1))             # older than the start: bookmarked
    assert meter._refresh_ledger(home)["events"] == 0
    assert cursors_of(ledger_of(home))[cursor_key("copy.jsonl")]["owner_key"] is not None
    write_codex(source / "child.jsonl", child_rows)
    grow(source / "parent.jsonl", b"".join(encoded(
        codex_turn(project, parent, "turn-parent-2", 20, 120))))
    needed = sum((source / name).stat().st_size for name in ("child.jsonl", "parent.jsonl"))
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", needed)   # no room for copy.jsonl

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 2
    assert ledger["lineages"][0]["state"] == "verified"
    assert "catching_up" not in ledger["coverage"]["reasons"]


def test_a_parent_cursor_without_an_owner_leaves_the_child_unverified(tmp_path, monkeypatch):
    home, source, _project, _parent_rows, child_rows, parent, child = fork_start(
        tmp_path, monkeypatch)
    edit_ledger(home, lambda ledger: ledger["cursors"][0].update(owner_key=None))
    write_codex(source / "child.jsonl", child_rows)

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 1
    event, = ledger["events"]
    assert event["event_key"] == meter._digest("codex", child, CHILD_EVENT)
    assert event["project_alias"] is None and event["ownership"] == "unknown"
    assert ledger["lineages"] == []
    assert "fork_parent_unavailable" in ledger["coverage"]["reasons"]


def test_a_verified_child_that_gains_a_turn_stays_verified_with_one_proof(
        tmp_path, monkeypatch):
    home, source, _project, _parent_rows, child_rows, parent, child = fork_start(
        tmp_path, monkeypatch)
    write_codex(source / "child.jsonl", child_rows)
    assert meter._refresh_ledger(home)["events"] == 1
    first_proof = ledger_of(home)["lineages"][0]["proofs"][0]
    more = codex_direct(child, parent, "turn-child", "turn-parent", "response-child-2",
                        20, 50, 150)
    grow(source / "child.jsonl", b"".join(encoded([more])))

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 2
    lineage, = ledger["lineages"]
    assert lineage["state"] == "verified" and lineage["reasons"] == []
    proof, = lineage["proofs"]
    assert len(first_proof["child_sequence"]) == 1 and len(proof["child_sequence"]) == 2
    assert proof["child_sequence"][:1] == first_proof["child_sequence"]
    assert proof["child_event_keys"] == sorted(
        meter._digest("codex", child, name) for name in (CHILD_EVENT, "response-child-2"))
    assert all(item["ownership"] == "proven" and item["project_alias"] == "sample"
               and item["lineage_key"] == lineage["lineage_key"]
               for item in ledger["events"])
    cursor = cursors_of(ledger)[cursor_key("child.jsonl")]
    assert cursor["generation"] == 1 and cursor["offset"] == cursor["size"]


def test_a_child_whose_earlier_sequence_is_edited_becomes_conflicting(tmp_path, monkeypatch):
    home, source, _project, _parent_rows, child_rows, parent, child = fork_start(
        tmp_path, monkeypatch)
    write_codex(source / "child.jsonl", child_rows)
    assert meter._refresh_ledger(home)["events"] == 1
    edited = codex_direct(child, parent, "turn-child", "turn-parent", CHILD_EVENT,
                          31, 31, 131)                    # same length, other usage
    original = encoded([child_rows[-1]])[0]
    replacement = encoded([edited])[0]
    assert len(original) == len(replacement) and original != replacement
    with open(source / "child.jsonl", "r+b") as handle:
        handle.seek(source.joinpath("child.jsonl").stat().st_size - len(original))
        handle.write(replacement)

    meter._refresh_ledger(home)

    ledger = ledger_of(home)
    lineage, = ledger["lineages"]
    assert lineage["state"] == "conflicting" and len(lineage["proofs"]) == 2
    assert "resume_failed_digest_mismatch" in ledger["coverage"]["reasons"]
    assert all(item["ownership"] == "unknown" and item["project_alias"] is None
               for item in ledger["events"])


@pytest.mark.parametrize("name", [
    "file_replaced", "cursor_past_end", "not_line_boundary", "digest_mismatch"])
def test_a_failed_codex_check_restarts_and_counts_only_events_not_before_the_start(
        tmp_path, monkeypatch, name):
    home, source, project, _config = codex_home(tmp_path, monkeypatch)
    log = source / "session.jsonl"
    padding = row("response_item", {"text": "x" * 400})
    old = [codex_log_header(), padding] + codex_turn(
        project, CODEX_OWNER, "turn-old", 10, 10, timestamp=OLD)
    new = codex_turn(project, CODEX_OWNER, "turn-new", 20, 30)
    write_codex(log, old)
    assert meter._refresh_ledger(home)["events"] == 0
    old_bytes = b"".join(encoded(old))
    if name == "file_replaced":
        replacement = source / "replacement"
        replacement.write_bytes(old_bytes + b"".join(encoded(new)))
        os.replace(replacement, log)                 # a different file, so a new inode
    elif name == "cursor_past_end":
        with open(log, "r+b") as handle:             # the same file, now shorter
            handle.truncate(0)
            handle.write(b"".join(encoded([codex_log_header()] + new)))
        assert log.stat().st_size < len(old_bytes)
    elif name == "not_line_boundary":
        edit_ledger(home, lambda ledger: ledger["cursors"][0].update(
            offset=ledger["cursors"][0]["offset"] - 3))
        grow(log, b"".join(encoded(new)))
    else:
        last = encoded(old)[-1]
        assert b"response-turn-old" in last
        with open(log, "r+b") as handle:             # same length, same file
            handle.seek(len(old_bytes) - len(last) + last.index(b"response-turn-old"))
            handle.write(b"response-turn-olx")
        assert log.stat().st_size == len(old_bytes)
        grow(log, b"".join(encoded(new)))

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written", result
    assert keys_of(ledger) == [codex_event_key(CODEX_OWNER, "turn-new")]
    assert "resume_failed_" + name in ledger["coverage"]["reasons"]
    cursor = cursor_for(ledger, "codex-source")
    assert cursor["generation"] == 2 and cursor["offset"] == log.stat().st_size
    assert cursor["line"] == log.read_bytes().count(b"\n")


def test_codex_logs_over_a_read_limit_are_skipped_and_the_others_count(tmp_path, monkeypatch):
    home, source, project, _config = codex_home(tmp_path, monkeypatch)
    owners = {name: f"019a0000-0000-7000-8000-0000000000a{index}"
              for index, name in enumerate(("big", "many", "noisy", "fine"), start=1)}
    for name, owner in owners.items():
        write_codex(source / f"{name}.jsonl", [codex_log_header(owner)] + codex_turn(
            project, owner, "turn-old", 10, 10, timestamp=OLD))
    assert meter._refresh_ledger(home)["events"] == 0
    bookmarks = cursors_of(ledger_of(home))
    extra = {
        "big": [row("response_item", {"text": "x" * 20_000})],
        "many": [row("response_item", {"n": item}) for item in range(10)],
        "noisy": codex_turn(project, owners["noisy"], "turn-b", 5, 15),
        "fine": [],
    }
    for name, owner in owners.items():
        grow(source / f"{name}.jsonl", b"".join(encoded(
            extra[name] + codex_turn(project, owner, "turn-new", 20, 30 + len(extra[name])))))
    monkeypatch.setattr(meter, "MAX_REREAD_BYTES", 10_000)
    monkeypatch.setattr(meter, "MAX_REREAD_LINES", 8)
    monkeypatch.setattr(meter, "MAX_NORMALIZED_EVENTS", 2)
    opened = opened_names(monkeypatch)

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "partial" and result["events"] == 1
    assert keys_of(ledger) == [codex_event_key(owners["fine"], "turn-new")]
    reasons = ledger["coverage"]["reasons"]
    assert "source_too_large" in reasons and "source_budget_exceeded" not in reasons
    after = cursors_of(ledger)
    for name in ("big", "many", "noisy"):
        assert after[cursor_key(f"{name}.jsonl")] == bookmarks[cursor_key(f"{name}.jsonl")]
    assert after[cursor_key("fine.jsonl")]["offset"] == (source / "fine.jsonl").stat().st_size
    assert "big.jsonl" not in opened             # over the byte limit: never opened
    assert meter._refresh_ledger(home)["events"] == 1      # skipped again, still counted once
    assert "source_too_large" in ledger_of(home)["coverage"]["reasons"]


def test_a_codex_log_that_fits_the_limits_but_not_the_rest_of_the_run_is_deferred(
        tmp_path, monkeypatch):
    home, source, project, _config = codex_home(tmp_path, monkeypatch)
    owners = {"a": "019a0000-0000-7000-8000-0000000000b1",
              "b": "019a0000-0000-7000-8000-0000000000b2"}
    for name, owner in owners.items():
        write_codex(source / f"{name}.jsonl", [codex_log_header(owner)] + codex_turn(
            project, owner, "turn-old", 10, 10, timestamp=OLD))
    meter._refresh_ledger(home)
    for name, owner in owners.items():
        grow(source / f"{name}.jsonl", b"".join(encoded(
            codex_turn(project, owner, "turn-new", 20, 30))))
    sizes = [(source / f"{name}.jsonl").stat().st_size for name in owners]
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", sum(sizes) - 1)

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "partial" and result["events"] == 1
    reasons = ledger["coverage"]["reasons"]
    assert "catching_up" in reasons and "source_too_large" not in reasons
    monkeypatch.setattr(meter, "MAX_RUN_READ_BYTES", 1024 ** 3)
    assert meter._refresh_ledger(home)["events"] == 2


def test_a_codex_reread_ignores_the_claude_piece_limits(tmp_path, monkeypatch):
    home, source, project, _config = codex_home(tmp_path, monkeypatch)
    log = source / "session.jsonl"
    write_codex(log, [codex_log_header()] + codex_turn(
        project, CODEX_OWNER, "turn-old", 10, 10, timestamp=OLD))
    meter._refresh_ledger(home)
    grow(log, b"".join(encoded(codex_turn(project, CODEX_OWNER, "turn-new", 20, 30))))
    monkeypatch.setattr(meter, "MAX_BATCH_BYTES", 64)
    monkeypatch.setattr(meter, "MAX_BATCH_LINES", 1)
    assert log.stat().st_size > 64

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 1
    assert keys_of(ledger) == [codex_event_key(CODEX_OWNER, "turn-new")]
    assert "catching_up" not in ledger["coverage"]["reasons"]


def test_a_fresh_codex_file_drops_events_before_the_start(tmp_path, monkeypatch):
    home, source, project, _config = codex_home(tmp_path, monkeypatch)
    assert meter._refresh_ledger(home)["events"] == 0
    write_codex(source / "late.jsonl", [codex_log_header()]
                + codex_turn(project, CODEX_OWNER, "turn-before", 10, 10, timestamp=OLD)
                + codex_turn(project, CODEX_OWNER, "turn-after", 20, 30))

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 1
    assert keys_of(ledger) == [codex_event_key(CODEX_OWNER, "turn-after")]
    assert cursor_for(ledger, "codex-source")["line"] == 5


def test_a_codex_torn_tail_is_left_for_the_next_run_and_counts_once(tmp_path, monkeypatch):
    home, source, project, _config = codex_home(tmp_path, monkeypatch)
    log = source / "session.jsonl"
    write_codex(log, [codex_log_header()] + codex_turn(
        project, CODEX_OWNER, "turn-old", 10, 10, timestamp=OLD))
    meter._refresh_ledger(home)
    bookmark = cursor_for(ledger_of(home), "codex-source")
    new = b"".join(encoded(codex_turn(project, CODEX_OWNER, "turn-new", 20, 30)))
    half = len(new) - 20
    grow(log, new[:half])

    result = meter._refresh_ledger(home)

    ledger = ledger_of(home)
    assert result["status"] == "written" and result["events"] == 0   # usage line is torn
    assert "partial_tail" not in ledger["coverage"]["reasons"]
    cursor = cursor_for(ledger, "codex-source")
    assert cursor["offset"] < bookmark["offset"] + len(new[:half])
    grow(log, new[half:])
    assert meter._refresh_ledger(home)["events"] == 1
    assert meter._refresh_ledger(home)["events"] == 1
    assert keys_of(ledger_of(home)) == [codex_event_key(CODEX_OWNER, "turn-new")]
    final = cursor_for(ledger_of(home), "codex-source")
    assert final["line"] == log.read_bytes().count(b"\n") == 5
    assert final["offset"] == final["size"] == log.stat().st_size


def verified_fork_ledger(tmp_path, monkeypatch):
    """A ledger holding one verified fork lineage; parent and child are read together."""
    home, source, project, _config = codex_home(tmp_path, monkeypatch)
    parent_rows, child_rows, _parent, child = codex_fork_fixture(project)
    write_codex(source / "parent.jsonl", parent_rows)
    write_codex(source / "child.jsonl", child_rows)
    assert refresh_counted(home, source)["events"] == 2
    ledger = json.loads((home / ".cairn" / "meter" / "ledger.json").read_bytes())
    assert ledger["lineages"][0]["state"] == "verified"
    return ledger, child


def test_a_proof_may_name_an_event_the_ledger_does_not_hold(tmp_path, monkeypatch):
    ledger, child = verified_fork_ledger(tmp_path, monkeypatch)
    assert ledger["lineages"][0]["proofs"][0]["child_event_keys"] == [
        meter._digest("codex", child, CHILD_EVENT)]
    ledger["events"] = []
    ledger["mappings"] = []
    loaded = meter._load_ledger(as_bytes(ledger), CLOCK)
    assert loaded["events"] == [] and len(loaded["lineages"]) == 1


def test_a_proof_naming_an_event_of_another_lineage_is_refused(tmp_path, monkeypatch):
    ledger, _child = verified_fork_ledger(tmp_path, monkeypatch)
    assert meter._load_ledger(as_bytes(ledger), CLOCK)["lineages"]
    child_event, = [item for item in ledger["events"] if item["lineage_key"] is not None]
    child_event["lineage_key"] = None
    with pytest.raises(meter.Unavailable) as refused:
        meter._load_ledger(as_bytes(ledger), CLOCK)
    assert refused.value.reason == "ledger_invalid"


# ---- Fold: daily rows, the horizon, the export and lineages (plan C4) ---------

LATER = datetime(2026, 11, 30, tzinfo=timezone.utc)      # its horizon is 2026-11-16
OTHER_OWNER = "019a0000-0000-7000-8000-000000000042"


def at_clock(monkeypatch, moment):
    monkeypatch.setattr(meter, "_now_utc", lambda: moment)


def day_stamp(day, hour=10, month=11):
    return f"2026-{month:02d}-{day:02d}T{hour:02d}:00:00Z"


def priced_lines(message_id, timestamp, *, fresh=10, output=4, cache_read=8,
                 model="claude-sonnet-4-6", cwd=None):
    """One reply by a model with a reference rate, so its reference tokens are numbers."""
    record = claude_record(message_id, timestamp)
    record["message"]["model"] = model
    if cwd is not None:
        record["cwd"] = cwd
    record["message"]["usage"] = {"input_tokens": fresh, "output_tokens": output,
                                  "cache_creation_input_tokens": 0,
                                  "cache_read_input_tokens": cache_read}
    return json.dumps(record).encode() + b"\n"


def claude_home_started(tmp_path, monkeypatch):
    """A Claude home whose start run bookmarked one old line: home, log, config path."""
    home, claude_root, _codex_root, _project, config_path = c1_home(tmp_path, monkeypatch)
    log = claude_root / "session.jsonl"
    log.write_bytes(claude_lines("old-1", timestamp=OLD))
    assert meter._refresh_ledger(home)["events"] == 0
    return home, log, config_path


def fold_history():
    """Replies on 2026-11-05 to 11-12, one reply whose usage lines disagree, one with no time."""
    lines = b""
    for day in range(5, 13):
        lines += priced_lines(f"day-{day}-a", day_stamp(day), fresh=10 + day)
        lines += priced_lines(f"day-{day}-b", day_stamp(day, 15), output=day)
    lines += priced_lines("clash", day_stamp(8), fresh=1) + priced_lines("clash", day_stamp(8), fresh=2)
    return lines + claude_lines("no-time", timestamp=None)


def daily_events(ledger):
    return sum(item["events"] for item in ledger["daily"])


def test_folding_changes_no_aggregate_sum(tmp_path, monkeypatch):
    ledgers = {}
    for name, fold_days in (("folded", 14), ("never", 10_000)):
        (tmp_path / name).mkdir()
        at_clock(monkeypatch, CLOCK)
        home, log, config_path = claude_home_started(tmp_path / name, monkeypatch)
        grow(log, fold_history())
        at_clock(monkeypatch, LATER)
        monkeypatch.setattr(meter, "FOLD_AFTER_DAYS", fold_days)
        assert meter._refresh_ledger(home)["status"] == "written"
        # late lines for days already folded: their rows add to the saved ones
        grow(log, priced_lines("late-7", day_stamp(7, 20)) + priced_lines("late-8", day_stamp(8, 20))
             + priced_lines("late-clash", day_stamp(8, 21), fresh=1)
             + priced_lines("late-clash", day_stamp(8, 21), fresh=2))
        assert meter._refresh_ledger(home)["status"] == "written"
        ledgers[name] = ledger_of(home)
    folded, never = ledgers["folded"], ledgers["never"]

    assert folded["aggregates"] == never["aggregates"]
    assert any(item["unknown_events"] for item in folded["aggregates"])
    assert any(item["reference_tokens"]["total"] is not None for item in folded["aggregates"])
    assert sum(item["events"] for item in never["aggregates"]) == 21
    assert never["daily"] == []
    models_cfg = reference_models()
    config = meter.validate_config_bytes(config_path.read_bytes())
    assert never["aggregates"] == meter._recompute_aggregates(
        never["events"], config, models_cfg)
    assert folded["fold_horizon"] == "2026-11-16" and daily_events(folded) == 20
    assert [event["observed_at"] for event in folded["events"]] == [None]   # no time: never folded
    assert folded["mappings"] == []
    assert meter._load_ledger(as_bytes(folded), LATER)["daily"] == folded["daily"]


def test_a_ledger_written_under_an_older_table_loads_and_is_weighted_by_the_current_one(
        tmp_path, monkeypatch):
    at_clock(monkeypatch, CLOCK)
    home, log, config_path = claude_home_started(tmp_path, monkeypatch)
    project = json.loads(config_path.read_text(encoding="utf-8"))["projects"][0]["path"]
    grow(log, priced_lines("old-day", day_stamp(5), cwd=project)
         + priced_lines("recent", day_stamp(29), model="claude-sonnet-5-5", cwd=project))
    at_clock(monkeypatch, LATER)
    assert meter._refresh_ledger(home)["status"] == "written"
    ledger_path = home / ".cairn" / "meter" / "ledger.json"
    ledger = json.loads(ledger_path.read_bytes())
    folded, = ledger["daily"]
    assert folded["reference_tokens"]["total"] == "92.4"

    previous = "cairn-api-token-index/2026-11-06"
    ledger["ratio_version"] = previous
    ledger["ratio_index"] = {"version": previous, "models": {}}
    for row in (*ledger["daily"], *ledger["aggregates"]):
        row["reference_index"] = previous
        if row["model"] == "claude-sonnet-5-5":
            row["reference_tokens"] = {name: None for name in row["reference_tokens"]}
    ledger_path.write_bytes(as_bytes(ledger))

    models_cfg = reference_models()
    assert meter._refresh_ledger(home)["status"] == "written"
    after = ledger_of(home)
    assert after["ratio_version"] == models_cfg["ratio_version"]
    assert after["ratio_index"] == models_cfg
    assert after["daily"] == [{**folded, "reference_index": previous}]
    held, = [row for row in after["aggregates"] if row["model"] == "claude-sonnet-5-5"]
    assert held["reference_tokens"]["total"] == "60.8"
    assert held["reference_index"] == models_cfg["ratio_version"]
    summary = json.loads((Path(project) / "dev" / "measurement" / "meter.json").read_bytes())
    totals = {row["model"]: row["reference_tokens"]["total"] for row in summary["aggregates"]}
    assert totals == {"claude-sonnet-4-6": "92.4", "claude-sonnet-5-5": "60.8"}


def test_the_export_shows_folded_days_without_an_artifact_and_waits_are_unchanged(
        tmp_path, monkeypatch):
    owner = "019a0000-0000-7000-8000-000000000033"
    records = c2_bound_records(tmp_path / "approved-project", owner, "turn-fold", 12,
                               [("old-item", 2500)])
    _claim_id, claims = c2_claim_records(owner)
    home, source, project, _config = c2_home(tmp_path, claims=claims)
    (source / "session.jsonl").write_bytes(b"".join(encoded(records)))
    assert refresh_counted(home, source)["status"] == "written"
    export_path = project / "dev" / "measurement" / "meter.json"
    before = json.loads(export_path.read_bytes())
    row_before, = before["aggregates"]
    assert row_before["artifact"] == "src/app.py" and before["wait"]["by_artifact"]

    at_clock(monkeypatch, LATER)
    assert meter._refresh_ledger(home)["status"] == "written"

    ledger = ledger_of(home)
    assert ledger["events"] == [] and ledger["mappings"] == [] and daily_events(ledger) == 1
    after = json.loads(export_path.read_bytes())
    row_after, = after["aggregates"]
    assert row_after["artifact"] is None
    assert ({key: value for key, value in row_after.items() if key != "artifact"}
            == {key: value for key, value in row_before.items() if key != "artifact"})
    assert row_after["week"] == row_before["week"] and row_after["day"] == "2026-11-05"
    assert after["wait"] == before["wait"]


def test_a_rotated_copy_of_a_log_whose_days_were_folded_adds_nothing(tmp_path, monkeypatch):
    home, log, _config = claude_home_started(tmp_path, monkeypatch)
    at_clock(monkeypatch, datetime(2026, 11, 10, tzinfo=timezone.utc))
    monkeypatch.setattr(meter, "RETAINED_EVENT_TARGET", 2)
    lines = (priced_lines("a-1", day_stamp(5)) + priced_lines("a-2", day_stamp(5, 11))
             + priced_lines("a-3", day_stamp(5, 12)) + priced_lines("b-1", day_stamp(9))
             + priced_lines("b-2", day_stamp(9, 11)))
    grow(log, lines)
    assert meter._refresh_ledger(home)["status"] == "written"
    first = ledger_of(home)
    assert first["fold_horizon"] == "2026-11-06" and len(first["events"]) == 2
    assert [item["events"] for item in first["daily"]] == [3]

    rotated = log.with_name("rotated.jsonl")
    rotated.write_bytes(claude_lines("old-1", timestamp=OLD) + lines)
    stamp = int(datetime(2026, 11, 10, tzinfo=timezone.utc).timestamp() * 1e9)
    os.utime(rotated, ns=(stamp, stamp))
    assert meter._refresh_ledger(home)["status"] == "written"

    second = ledger_of(home)
    assert second["daily"] == first["daily"] and second["aggregates"] == first["aggregates"]
    assert keys_of(second) == keys_of(first)
    assert cursor_key("rotated.jsonl", "claude-source") in cursors_of(second)


def test_a_fork_child_read_again_after_its_events_folded_adds_nothing_twice(
        tmp_path, monkeypatch):
    home, source, project, _config = codex_home(tmp_path, monkeypatch)
    parent_rows, child_rows, _parent, _child = codex_fork_fixture(project)
    write_codex(source / "parent.jsonl", parent_rows)
    write_codex(source / "child.jsonl", child_rows)
    assert refresh_counted(home, source)["events"] == 2
    at_clock(monkeypatch, LATER)
    assert meter._refresh_ledger(home)["events"] == 0
    folded = ledger_of(home)
    assert daily_events(folded) == 2 and folded["lineages"] == []

    copy_path = source / "child-copy.jsonl"
    write_codex(copy_path, child_rows)
    stamp = int(LATER.timestamp() * 1e9)
    os.utime(copy_path, ns=(stamp, stamp))
    assert meter._refresh_ledger(home)["status"] == "written"

    again = ledger_of(home)
    assert again["daily"] == folded["daily"] and again["events"] == []
    assert again["aggregates"] == folded["aggregates"]
    assert cursor_key("child-copy.jsonl") in cursors_of(again)


def test_sixty_thousand_events_over_twenty_days_leave_at_most_the_target(tmp_path, monkeypatch):
    home, log, _config = claude_home_started(tmp_path, monkeypatch)
    at_clock(monkeypatch, datetime(2026, 11, 25, tzinfo=timezone.utc))
    lines, number = [], 0
    for day in range(6, 26):                  # 20 days; the last 14 hold 54,000 replies
        count = 1000 if day < 12 else 54_000 // 14
        for _ in range(count):
            number += 1
            lines.append(priced_lines(f"m{number}", day_stamp(day)))
    while number < 60_000:                    # the division above leaves a few over
        number += 1
        lines.append(priced_lines(f"m{number}", day_stamp(25)))
    lines.extend(claude_lines(f"no-time-{index}", timestamp=None) for index in range(5))
    grow(log, b"".join(lines))

    assert meter._refresh_ledger(home)["status"] == "written"

    ledger = ledger_of(home)
    assert len(ledger["events"]) <= meter.RETAINED_EVENT_TARGET
    assert sum(event["observed_at"] is None for event in ledger["events"]) == 5
    horizon = ledger["fold_horizon"]
    assert "2026-11-11" < horizon <= "2026-11-25"
    assert all(event["observed_at"] is None or event["observed_at"][:10] >= horizon
               for event in ledger["events"])
    assert sum(item["events"] for item in ledger["aggregates"]) == 60_005
    assert all(item["day"] < horizon for item in ledger["daily"])

    at_clock(monkeypatch, datetime(2026, 11, 20, tzinfo=timezone.utc))
    assert meter._refresh_ledger(home)["status"] == "written"
    assert ledger_of(home)["fold_horizon"] == horizon          # an earlier clock never lowers it


def test_a_partly_folded_lineage_stays_and_loads(tmp_path, monkeypatch):
    home, source, project, _parent_rows, child_rows, parent, child = fork_start(
        tmp_path, monkeypatch)
    write_codex(source / "child.jsonl", child_rows)
    assert meter._refresh_ledger(home)["events"] == 1
    later_turn = codex_direct(child, parent, "turn-child", "turn-parent", "response-child-2",
                              20, 50, 150)
    later_turn["timestamp"] = day_stamp(25)
    grow(source / "child.jsonl", b"".join(encoded([later_turn])))
    at_clock(monkeypatch, LATER)

    assert meter._refresh_ledger(home)["status"] == "written"

    ledger = ledger_of(home)
    assert keys_of(ledger) == [meter._digest("codex", child, "response-child-2")]
    assert daily_events(ledger) == 1
    lineage, = ledger["lineages"]
    assert lineage["state"] == "verified"
    assert len(lineage["proofs"][0]["child_event_keys"]) == 2      # one of them is folded
    assert ledger["events"][0]["lineage_key"] == lineage["lineage_key"]


def test_a_verified_lineage_whose_child_events_are_all_folded_is_dropped(tmp_path, monkeypatch):
    home, source, _project, _parent_rows, child_rows, _parent, _child = fork_start(
        tmp_path, monkeypatch)
    write_codex(source / "child.jsonl", child_rows)
    assert meter._refresh_ledger(home)["events"] == 1
    assert len(ledger_of(home)["lineages"]) == 1
    at_clock(monkeypatch, LATER)

    assert meter._refresh_ledger(home)["status"] == "written"

    ledger = ledger_of(home)
    assert ledger["lineages"] == [] and ledger["events"] == [] and daily_events(ledger) == 1


def test_a_wait_that_cites_a_lineage_keeps_it_when_the_events_fold(tmp_path, monkeypatch):
    home, source, _project, _parent_rows, child_rows, parent, child = fork_start(
        tmp_path, monkeypatch)
    start_ms = int(CLOCK.timestamp() * 1000)
    wait = timing_record(item_id="child-wait", start=start_ms + 60_000, end=start_ms + 61_000)
    wait["payload"]["thread_id"], wait["payload"]["turn_id"] = child, "turn-child"
    write_codex(source / "child.jsonl", child_rows + [wait])
    assert meter._refresh_ledger(home)["events"] == 1
    first = ledger_of(home)
    lineage_key = first["lineages"][0]["lineage_key"]
    wait_row, = first["waits"]
    assert wait_row["lineage_key"] == lineage_key
    assert wait_row["ownership"] == "proven"
    assert wait_row["thread_key"] == meter._digest("codex", child)
    assert wait_row["session_key"] == meter._digest("codex", parent)
    assert wait_row["turn_key"] == meter._digest("codex", child, "turn-child")
    assert wait_row["root_turn_key"] == meter._digest("codex", parent, "turn-parent")
    assert wait_row["project_alias"] == "sample"
    assert wait_row["project_association"] == "current_local_verified"
    at_clock(monkeypatch, LATER)

    assert meter._refresh_ledger(home)["status"] == "written"

    ledger = ledger_of(home)
    assert ledger["events"] == [] and daily_events(ledger) == 1
    assert [item["lineage_key"] for item in ledger["lineages"]] == [lineage_key]


def test_a_fork_wait_without_its_parent_proof_stays_unknown(tmp_path, monkeypatch):
    home, source, _project, _parent_rows, child_rows, _parent, child = fork_start(
        tmp_path, monkeypatch)
    start_ms = int(CLOCK.timestamp() * 1000)
    wait = timing_record(item_id="child-wait", start=start_ms + 60_000, end=start_ms + 61_000)
    wait["payload"]["thread_id"], wait["payload"]["turn_id"] = child, "turn-child"
    write_codex(source / "child.jsonl", child_rows + [wait])
    (source / "parent.jsonl").unlink()

    meter._refresh_ledger(home)

    ledger = ledger_of(home)
    wait_row, = ledger["waits"]
    assert wait_row["ownership"] == "unknown"
    assert wait_row["lineage_key"] is None
    assert wait_row["thread_key"] is None and wait_row["session_key"] is None
    assert wait_row["turn_key"] is None and wait_row["root_turn_key"] is None
    assert wait_row["project_alias"] is None


def test_a_conflicting_lineage_is_kept_when_its_events_fold(tmp_path, monkeypatch):
    home, source, _project, _parent_rows, child_rows, parent, child = fork_start(
        tmp_path, monkeypatch)
    write_codex(source / "child.jsonl", child_rows)
    assert meter._refresh_ledger(home)["events"] == 1
    edited = codex_direct(child, parent, "turn-child", "turn-parent", CHILD_EVENT,
                          31, 31, 131)
    original, replacement = encoded([child_rows[-1]])[0], encoded([edited])[0]
    with open(source / "child.jsonl", "r+b") as handle:
        handle.seek(source.joinpath("child.jsonl").stat().st_size - len(original))
        handle.write(replacement)
    meter._refresh_ledger(home)
    assert ledger_of(home)["lineages"][0]["state"] == "conflicting"
    at_clock(monkeypatch, LATER)

    assert meter._refresh_ledger(home)["status"] == "written"

    ledger = ledger_of(home)
    lineage, = ledger["lineages"]
    assert lineage["state"] == "conflicting" and ledger["events"] == []
    assert daily_events(ledger) == 1


@pytest.mark.parametrize("change", ["remote-changed", "project-removed"])
def test_a_project_change_merges_folded_rows_into_the_unattributed_row(
        tmp_path, monkeypatch, change):
    home, source, project, config_path = codex_home(tmp_path, monkeypatch)
    write_codex(source / "attributed.jsonl", [codex_log_header(CODEX_OWNER)] + codex_turn(
        project, CODEX_OWNER, "turn-a", 10, 10, timestamp=STAMP))
    write_codex(source / "elsewhere.jsonl", [codex_log_header(OTHER_OWNER)] + codex_turn(
        host_absolute("/synthetic/elsewhere"), OTHER_OWNER, "turn-b", 20, 20, timestamp=STAMP))
    assert refresh_counted(home, source)["events"] == 2
    at_clock(monkeypatch, LATER)
    assert meter._refresh_ledger(home)["status"] == "written"
    first = ledger_of(home)
    assert sorted(item["project_alias"] or "" for item in first["daily"]) == ["", "sample"]
    assert first["events"] == []

    config = json.loads(config_path.read_text(encoding="utf-8"))
    if change == "remote-changed":
        config["projects"][0]["remote"] = "https://example.test/team/renamed.git"
    else:
        config["projects"] = []
    config_path.write_text(json.dumps(config), encoding="utf-8")
    config_path.chmod(0o600)
    assert meter._refresh_ledger(home)["status"] == "written"

    second = ledger_of(home)
    row, = second["daily"]
    assert row["project_alias"] is None and row["events"] == 2
    for name in meter._EVENT_KIND_NAMES:
        parts = [item["kinds"][name] for item in first["daily"]]
        assert row["kinds"][name] == (None if None in parts else sum(parts))
    assert second["aggregates"] == second["daily"]


@pytest.mark.parametrize("force", [None, 1], ids=["default", "force-fold"])
def test_a_run_that_is_catching_up_raises_no_horizon_unless_the_ledger_is_very_large(
        tmp_path, monkeypatch, force):
    home, log, _config = claude_home_started(tmp_path, monkeypatch)
    at_clock(monkeypatch, LATER)
    grow(log, b"".join(priced_lines(name, day_stamp(2)) for name in "abcd"))
    monkeypatch.setattr(meter, "MAX_BATCH_LINES", 2)
    if force is not None:
        monkeypatch.setattr(meter, "FOLD_FORCE_EVENTS", force)

    assert meter._refresh_ledger(home)["status"] == "partial"

    ledger = ledger_of(home)
    assert "catching_up" in ledger["coverage"]["reasons"]
    assert ledger["fold_horizon"] == ("2026-10-22" if force is None else "2026-11-16")
    assert (len(ledger["events"]), daily_events(ledger)) == (
        (2, 0) if force is None else (0, 2))


def test_a_reply_split_across_a_piece_boundary_counts_once_in_the_daily_rows(
        tmp_path, monkeypatch):
    home, log, _config = claude_home_started(tmp_path, monkeypatch)
    at_clock(monkeypatch, LATER)
    grow(log, usage_record("split-1", 10, day_stamp(2)) + usage_record("split-1", 10, day_stamp(2)))
    monkeypatch.setattr(meter, "MAX_BATCH_LINES", 1)

    assert meter._refresh_ledger(home)["status"] == "partial"
    first = ledger_of(home)
    assert "catching_up" in first["coverage"]["reasons"]
    assert len(first["events"]) == 1 and first["daily"] == []

    monkeypatch.setattr(meter, "MAX_BATCH_LINES", 100_000)
    assert meter._refresh_ledger(home)["status"] == "written"

    second = ledger_of(home)
    assert second["events"] == [] and daily_events(second) == 1
    assert second["aggregates"] == second["daily"]


@pytest.mark.parametrize("catching_up", [False, True])
def test_a_late_line_older_than_the_saved_horizon_still_counts_and_folds_the_same_run(
        tmp_path, monkeypatch, catching_up):
    home, log, _config = claude_home_started(tmp_path, monkeypatch)
    at_clock(monkeypatch, LATER)
    assert meter._refresh_ledger(home)["status"] == "written"
    assert ledger_of(home)["fold_horizon"] == "2026-11-16"
    grow(log, priced_lines("late", day_stamp(3)))
    if catching_up:
        grow(log, priced_lines("recent", day_stamp(28)))
        monkeypatch.setattr(meter, "MAX_BATCH_LINES", 1)

    assert meter._refresh_ledger(home)["status"] == ("partial" if catching_up else "written")

    ledger = ledger_of(home)
    assert ("catching_up" in ledger["coverage"]["reasons"]) is catching_up
    assert ledger["fold_horizon"] == "2026-11-16"
    assert [item["day"] for item in ledger["daily"]] == ["2026-11-03"]
    assert daily_events(ledger) == 1 and ledger["events"] == []


def test_the_event_cap_applies_after_folding_and_unknown_time_events_still_hit_it(
        tmp_path, monkeypatch):
    home, log, _config = claude_home_started(tmp_path, monkeypatch)
    at_clock(monkeypatch, LATER)
    monkeypatch.setattr(meter, "MAX_RETAINED_EVENTS", 5)
    grow(log, b"".join(priced_lines(f"old-day-{day}", day_stamp(day)) for day in range(3, 11))
         + priced_lines("recent", day_stamp(28)))

    assert meter._refresh_ledger(home)["status"] == "written"       # 9 events, 1 kept
    ledger = ledger_of(home)
    assert len(ledger["events"]) == 1 and daily_events(ledger) == 8

    path = home / ".cairn" / "meter" / "ledger.json"
    before = path.read_bytes()
    grow(log, b"".join(claude_lines(f"no-time-{index}", timestamp=None) for index in range(5)))

    result = meter._refresh_ledger(home)

    assert result["status"] == "unavailable" and result["reason"] == "source_budget_exceeded"
    assert path.read_bytes() == before


def test_events_of_unknown_time_count_toward_the_target_and_never_fold(tmp_path, monkeypatch):
    home, log, _config = claude_home_started(tmp_path, monkeypatch)
    at_clock(monkeypatch, datetime(2026, 11, 10, tzinfo=timezone.utc))
    monkeypatch.setattr(meter, "RETAINED_EVENT_TARGET", 3)
    grow(log, priced_lines("d5", day_stamp(5)) + priced_lines("d6", day_stamp(6))
         + priced_lines("d9", day_stamp(9)) + claude_lines("none-1", "none-2", timestamp=None))

    assert meter._refresh_ledger(home)["status"] == "written"

    ledger = ledger_of(home)
    assert ledger["fold_horizon"] == "2026-11-07"       # 5 would stay at 10-27; 3 stay at 11-07
    assert sorted(event["observed_at"] or "" for event in ledger["events"]) == [
        "", "", "2026-11-09T10:00:00+00:00"]
    assert daily_events(ledger) == 2


def test_events_of_the_clock_day_are_never_folded_even_above_the_target(tmp_path, monkeypatch):
    home, log, _config = claude_home_started(tmp_path, monkeypatch)
    at_clock(monkeypatch, datetime(2026, 11, 10, 18, tzinfo=timezone.utc))
    monkeypatch.setattr(meter, "RETAINED_EVENT_TARGET", 2)
    grow(log, b"".join(priced_lines(f"today-{index}", day_stamp(10, 8 + index))
                       for index in range(4)))

    assert meter._refresh_ledger(home)["status"] == "written"

    ledger = ledger_of(home)
    assert ledger["fold_horizon"] == "2026-11-10"
    assert len(ledger["events"]) == 4 and ledger["daily"] == []



def test_a_run_over_a_log_folder_with_a_sub_folder_counts_its_logs(tmp_path, monkeypatch):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    nested = claude_root / "project-a" / "nested"
    nested.mkdir(parents=True)
    log = nested / "session.jsonl"
    log.write_bytes(claude_lines("old-1", timestamp=OLD))
    assert meter._refresh_ledger(home)["events"] == 0

    grow(log, claude_lines("new-1", "new-2", timestamp=NEW))
    result = meter._refresh_ledger(home)

    assert result["status"] == "written" and result["events"] == 2
    assert keys_of(ledger_of(home)) == sorted([event_key_for("new-1"), event_key_for("new-2")])


def _can_make_file_link():
    with tempfile.TemporaryDirectory() as folder:
        try:
            os.symlink(Path(folder) / "target", Path(folder) / "link")
        except (OSError, NotImplementedError):
            return False
    return True


@pytest.mark.parametrize("case", ["folder-link"] + (["file-link"] if _can_make_file_link() else []))
def test_a_link_out_of_a_log_folder_is_not_followed(tmp_path, monkeypatch, case):
    home, claude_root, *_ = c1_home(tmp_path, monkeypatch)
    outside = tmp_path / "outside-logs"
    outside.mkdir()
    outside_log = outside / "outside.jsonl"
    outside_log.write_bytes(claude_lines("old-9", timestamp=OLD))
    inside = claude_root / "session.jsonl"
    inside.write_bytes(claude_lines("old-1", timestamp=OLD))
    if case == "folder-link":
        _make_folder_link(claude_root / "linked-folder", outside)
    else:
        (claude_root / "linked.jsonl").symlink_to(outside_log)
    assert meter._refresh_ledger(home)["events"] == 0

    grow(inside, claude_lines("new-1", timestamp=NEW))
    grow(outside_log, claude_lines("new-9", timestamp=NEW))
    result = meter._refresh_ledger(home)

    assert result["status"] == "written" and result["events"] == 1
    assert keys_of(ledger_of(home)) == [event_key_for("new-1")]


@pytest.mark.parametrize("case", ["dev-link"] + (["file-link"] if _can_make_file_link() else []))
def test_the_work_claims_are_not_read_through_a_link(tmp_path, case):
    _home, _source, project, _config_path = c2_home(tmp_path)
    _claim_id, rows = c2_claim_records("019a0000-0000-7000-8000-000000000001")
    outside = tmp_path / "outside-dev"
    outside.mkdir()
    (outside / "intents.jsonl").write_bytes(b"".join(encoded(rows)))
    if case == "dev-link":
        (project / "dev").rename(project / "dev-original")
        _make_folder_link(project / "dev", outside)
    else:
        (project / "dev" / "intents.jsonl").unlink()
        (project / "dev" / "intents.jsonl").symlink_to(outside / "intents.jsonl")
    approved = {"alias": "sample", "path": str(project),
                "remote": "https://example.test/team/project.git"}

    assert meter._capture_project_claims(approved) == ([], "attribution_unavailable")


# ---- Antigravity: attribution to a project and the log reads (plan antigravity-reader, C2) ----

AG_OTHER = "9b8a7c6d-5e4f-4a3b-9c2d-1e0f9a8b7c6d"      # sorts after AG_CONVERSATION


def antigravity_home(tmp_path, *, claude=False, extra_projects=()):
    """A synthetic home with an antigravity source, a Codex one and optionally a Claude one.

    `extra_projects` are paths listed beside the first project (each is made a
    project folder). Returns home, antigravity root, Claude root, project, config path.
    """
    home, _codex_root, project, config_path = c2_home(tmp_path)
    root = tmp_path / "approved-antigravity-source"
    root.mkdir()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["sources"].append({"alias": "ag-source", "tool": "antigravity", "root": str(root)})
    claude_root = None
    if claude:
        claude_root = tmp_path / "approved-claude-source"
        claude_root.mkdir()
        config["sources"].append({"alias": "claude-source", "tool": "claude",
                                  "root": str(claude_root)})
    for number, path in enumerate(extra_projects):
        (Path(path) / "dev" / "measurement").mkdir(parents=True)
        config["projects"].append({"alias": f"extra-{number}", "path": str(path),
                                   "remote": "https://example.test/team/project.git"})
    config_path.write_text(json.dumps(config), encoding="utf-8")
    config_path.chmod(0o600)
    return home, root, claude_root, project, config_path


def antigravity_logs(root, conversation):
    folder = Path(root) / "brain" / conversation / ".system_generated" / "logs"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def reply_lines(*replies):
    return b"".join(json.dumps(reply).encode() + b"\n" for reply in replies)


def antigravity_key(created_at, input_tokens, output_tokens, conversation=AG_CONVERSATION):
    return meter._digest("antigravity", conversation, meter._timestamp(created_at),
                         input_tokens, output_tokens)


def across_a_block_edge(root, before="", beyond=None):
    """Text that puts `before` and the root across the first 64 KiB block edge.

    `beyond` is how many bytes of the root lie past the edge (half of it by default).
    """
    beyond = len(root) // 2 if beyond is None else beyond
    return " " * (64 * 1024 - len(before) - (len(root) - beyond)) + before + root + " end\n"


ATTRIBUTION_CASES = [
    pytest.param({"notes.md": lambda r: f"worked in {r} today\n"}, {}, None, "sample",
                 id="one-name"),
    pytest.param({"a/b/c/notes.txt": lambda r: f"worked in {r}\n"}, {}, None, "sample",
                 id="a-name-in-nested-folders"),
    pytest.param({"notes.md": lambda r: f"file://{r}/plan.md\n"}, {}, None, "sample",
                 id="after-a-file-scheme"),
    pytest.param({"notes.md": across_a_block_edge}, {}, None, "sample",
                 id="the-root-across-a-block-edge"),
    pytest.param({"notes.md": lambda r: across_a_block_edge(r, "file://")}, {}, None, "sample",
                 id="a-file-scheme-across-a-block-edge"),
    pytest.param({"notes.md": lambda r: across_a_block_edge(r, beyond=3)}, {}, None, "sample",
                 id="the-root-ends-just-past-a-block-edge"),
    pytest.param({"notes.md": lambda r: across_a_block_edge(r, beyond=0)}, {}, None, "sample",
                 id="the-root-ends-at-a-block-edge"),
    pytest.param({"notes.md": lambda r: across_a_block_edge(r, beyond=-1)}, {}, None, "sample",
                 id="the-root-ends-one-byte-before-a-block-edge"),
    pytest.param({"notes.md": lambda r: f"in {r}. More\n"}, {}, None, "sample",
                 id="a-period-ends-a-name"),
    pytest.param({"notes.md": lambda r: f"in {r} and {r}3\n"}, {}, None, "sample",
                 id="an-unlisted-folder-is-ignored"),
    pytest.param({"notes.md": lambda r: f"in {r} and {r}2.\n"}, {}, None,
                 "antigravity_projects_ambiguous", id="two-named-the-second-before-a-period"),
    pytest.param({"notes.md": lambda r: f"in {r}/sub/x\n"}, {}, None,
                 "antigravity_projects_ambiguous", id="a-nested-project-names-both"),
    pytest.param({"notes.md": lambda r: "nothing here\n"}, {}, None,
                 "antigravity_project_not_named", id="none-named"),
    pytest.param({"notes.md": lambda r: f"{r}-old\n"}, {}, None,
                 "antigravity_project_not_named", id="a-longer-name-only"),
    pytest.param({"notes.md": lambda r: f"a{r}\n"}, {}, None,
                 "antigravity_project_not_named", id="a-letter-before-the-root"),
    pytest.param({"notes.md": lambda r: f"{r}\u00e9\n"}, {}, None,
                 "antigravity_project_not_named", id="a-non-ascii-byte-after-the-root"),
    pytest.param({"notes.md": lambda r: f"{r}.txt\n"}, {}, None,
                 "antigravity_project_not_named", id="a-period-then-a-letter"),
    pytest.param({"notes.dat": lambda r: f"{r}\n"}, {}, None,
                 "antigravity_project_not_named", id="a-file-that-is-not-a-text-kind"),
    # The first file is read in full (the temp path alone is longer than a small fixed
    # limit, so the limit follows the root); the second is 60 bytes against 59 left.
    pytest.param({"a.md": lambda r: f"{r}\n", "b.md": lambda r: "." * 60},
                 {"MAX_ATTRIBUTION_BYTES": lambda r: len(r) + 60}, None,
                 "antigravity_search_incomplete", id="a-byte-cap-passed-across-files"),
    pytest.param({f"n{number}.md": (lambda r: f"{r}\n") for number in range(5)},
                 {"MAX_ATTRIBUTION_ENTRIES": 3}, None,
                 "antigravity_search_incomplete", id="an-entry-cap-passed"),
    pytest.param({"a/b/notes.md": lambda r: f"{r}\n"}, {"MAX_ATTRIBUTION_DEPTH": 1}, None,
                 "antigravity_search_incomplete", id="a-depth-cap-passed"),
    # The project named by the most files wins at ten to one. "other.md" names the second
    # listed project, whose path is the first one's with a "2" added.
    pytest.param({**{f"n{number}.md": (lambda r: f"{r}\n") for number in range(10)},
                  "other.md": lambda r: f"{r}2\n"}, {}, None, "sample",
                 id="ten-files-to-one-leads-enough"),
    pytest.param({**{f"n{number}.md": (lambda r: f"{r}\n") for number in range(9)},
                  "other.md": lambda r: f"{r}2\n"}, {}, None,
                 "antigravity_projects_ambiguous", id="nine-files-to-one-does-not"),
    pytest.param({f"n{number}.md": (lambda r: f"{r}\n") for number in range(3)}, {}, None,
                 "sample", id="three-files-to-none-leads-enough"),
    pytest.param({"n0.md": lambda r: f"{r}\n", "n1.md": lambda r: f"{r}2\n"}, {}, None,
                 "antigravity_projects_ambiguous", id="one-file-each-does-not-lead"),
    # A folder named `chunks` holds copies: not counted, at any level.
    pytest.param({"notes.md": lambda r: f"{r}\n", "chunks/a.md": lambda r: f"{r}2\n",
                  "chunks/b.md": lambda r: f"{r}2\n"}, {}, None, "sample",
                 id="a-chunks-folder-is-not-counted"),
    pytest.param({"notes.md": lambda r: f"{r}\n", "a/b/chunks/c.md": lambda r: f"{r}2\n"},
                 {}, None, "sample", id="a-nested-chunks-folder-is-not-counted"),
    pytest.param({"chunks/a.md": lambda r: f"{r}\n"}, {}, None,
                 "antigravity_project_not_named", id="a-chunks-folder-alone-names-none"),
    pytest.param({"notes.md": lambda r: f"{r}\n", "chunks-old/a.md": lambda r: f"{r}2\n"},
                 {}, None, "antigravity_projects_ambiguous",
                 id="a-folder-that-only-starts-with-chunks-is-counted"),
    pytest.param({}, {}, "folder", "antigravity_project_not_named",
                 id="a-link-to-an-outside-folder-that-names-the-project"),
] + ([pytest.param({}, {}, "file", "antigravity_project_not_named",
                   id="a-link-to-an-outside-file-that-names-the-project")]
     if _can_make_file_link() else [])


@pytest.mark.parametrize("files,patches,link,expected", ATTRIBUTION_CASES)
def test_an_antigravity_conversation_is_attributed_only_to_the_one_listed_project_its_files_name(
        tmp_path, monkeypatch, files, patches, link, expected):
    project = tmp_path / "approved-project"
    home, ag_root, _claude, _project, _config_path = antigravity_home(
        tmp_path, extra_projects=[tmp_path / "approved-project2", project / "sub"])
    root = str(project)
    folder = ag_root / "brain" / AG_CONVERSATION
    logs = antigravity_logs(ag_root, AG_CONVERSATION)
    log = logs / "transcript.jsonl"
    log.write_bytes(reply_lines(antigravity_reply(created_at=OLD)))
    for name, make in files.items():
        (folder / name).parent.mkdir(parents=True, exist_ok=True)
        (folder / name).write_bytes(make(root).encode("utf-8"))
    if link is not None:
        outside = tmp_path / "outside-saved-files"
        outside.mkdir()
        (outside / "notes.md").write_text(f"in {root}\n", encoding="utf-8")
        if link == "folder":
            _make_folder_link(folder / "linked-folder", outside)
        else:
            (folder / "linked.md").symlink_to(outside / "notes.md")
    for name, value in patches.items():
        monkeypatch.setattr(meter, name, value(root) if callable(value) else value)
    if set(patches) & {"MAX_ATTRIBUTION_BYTES", "MAX_ATTRIBUTION_ENTRIES"}:
        # Remove explicit adapter overrides so monkeypatched global caps govern the run.
        models_file = home / ".cairn" / "meter-models.json"
        models_data = json.loads(models_file.read_text(encoding="utf-8"))
        for key in ("MAX_ATTRIBUTION_BYTES", "MAX_ATTRIBUTION_ENTRIES"):
            if key in patches:
                models_data["tools"]["antigravity"].pop(
                    "max_bytes" if key == "MAX_ATTRIBUTION_BYTES" else "max_entries", None)
        models_file.write_text(json.dumps(models_data), encoding="utf-8")
    assert meter._refresh_ledger(home)["events"] == 0             # the start

    grow(log, reply_lines(antigravity_reply(created_at=NEW)))
    assert meter._refresh_ledger(home)["status"] == "written"

    event, = ledger_of(home)["events"]
    assert event["event_key"] == antigravity_key(NEW, 120, 30)
    if expected == "sample":
        assert (event["project_alias"], event["project_association"], event["ownership"],
                event["reasons"]) == ("sample", "current_local_verified", "proven", [])
        want = ("sample", None)
    else:
        assert (event["project_alias"], event["ownership"], event["reasons"]) == (
            None, "unknown", [expected])
        want = (None, expected)
    # The search itself, called alone: the same answer, and no cap is read past.
    config = json.loads((home / ".cairn" / "meter.json").read_text(encoding="utf-8"))
    alias, reason, used, listed = meter._conversation_project(
        str(ag_root), AG_CONVERSATION, config["projects"])
    assert (alias, reason) == want
    assert used <= meter.MAX_ATTRIBUTION_BYTES and listed <= meter.MAX_ATTRIBUTION_ENTRIES + 1


def test_an_antigravity_refresh_reads_only_conversation_logs_and_counts_each_reply_once(
        tmp_path, monkeypatch):
    home, ag_root, claude_root, project, _config_path = antigravity_home(tmp_path, claude=True)
    root = str(project)
    logs = antigravity_logs(ag_root, AG_CONVERSATION)
    real = logs / "transcript.jsonl"
    real.write_bytes(reply_lines(antigravity_reply(created_at=OLD)))
    (logs.parent.parent / "notes.md").write_text(f"saved in {root}\n", encoding="utf-8")
    # Decoys, each holding counts that differ from the real logs: a read would show.
    decoy = reply_lines(antigravity_reply(9990, 9991, NEW))
    (logs / "chunks").mkdir()
    (logs / "chunks" / "copy.jsonl").write_bytes(decoy)
    outside = tmp_path / "outside-logs"
    outside.mkdir()
    (outside / "outside.jsonl").write_bytes(decoy)
    if _can_make_file_link():
        (logs / "linked.jsonl").symlink_to(outside / "outside.jsonl")
    stranger = ag_root / "brain" / "not-a-uuid" / ".system_generated" / "logs"
    stranger.mkdir(parents=True)
    (stranger / "transcript.jsonl").write_bytes(decoy)
    (ag_root / "brain" / "stray.jsonl").write_bytes(decoy)        # a file, not a folder
    (ag_root / "stray.jsonl").write_bytes(decoy)                  # a file in the root
    beside = tmp_path / "approved-antigravity-source.jsonl"       # a file beside the root
    beside.write_bytes(decoy)
    claude_log = claude_root / "session.jsonl"
    claude_log.write_bytes(claude_lines("old-1", timestamp=OLD))
    # The folder lists more entries than this shared cap: charged to it, the refresh would fail.
    monkeypatch.setattr(meter, "MAX_REFRESH_ENTRIES", 4)
    assert meter._refresh_ledger(home)["events"] == 0             # the start

    reply_a = antigravity_reply(120, 30, NEW)
    reply_b = antigravity_reply(7, 3, "2026-11-05T12:00:01Z")
    old_copy = antigravity_reply(created_at=OLD)
    grow(real, reply_lines(old_copy, reply_a))                    # a copy before the start, a reply
    (logs / "transcript_full.jsonl").write_bytes(reply_lines(old_copy, reply_a, reply_a, reply_b))
    grow(claude_log, claude_lines("new-1", timestamp=NEW))
    opened, real_open, named_by = [], os.open, {}

    def spy(path, flags=0, *args, dir_fd=None, **kwargs):
        # A name opened inside an open folder is recorded by its whole path.
        full = os.fsdecode(path)
        if dir_fd is None:
            handle = real_open(path, flags, *args, **kwargs)
        else:
            full = os.path.join(named_by.get(dir_fd, "?"), full)
            handle = real_open(path, flags, *args, dir_fd=dir_fd, **kwargs)
        named_by[handle] = full
        opened.append((full, flags))
        return handle

    with monkeypatch.context() as patched:
        patched.setattr(os, "open", spy)
        result = meter._refresh_ledger(home)

    assert result["status"] == "written", result
    ledger = ledger_of(home)
    assert keys_of(ledger) == sorted([event_key_for("new-1"), antigravity_key(NEW, 120, 30)])
    key = antigravity_key(NEW, 120, 30)
    by_key = {event["event_key"]: event for event in ledger["events"]}
    assert by_key[key]["project_alias"] == "sample" and by_key[key]["reasons"] == []
    # The search reads the conversation's saved text and the log reader reads only
    # `transcript.jsonl`; `transcript_full.jsonl` is never counted as a log (`chunks/` never opened).
    assert [rel for rel, _ in meter._enumerate_antigravity(str(ag_root))[0]] == [
        f"brain/{AG_CONVERSATION}/.system_generated/logs/transcript.jsonl"]
    paths = [path for path, _flags in opened]
    inside = {path for path, flags in opened
              if path.startswith(str(ag_root)) and not flags & meter._O_DIRECTORY}
    base = ag_root / "brain" / AG_CONVERSATION
    assert inside == {str(base / "notes.md"), str(real), str(logs / "transcript_full.jsonl")}
    assert not any("chunks" in Path(path).parts for path in paths)
    assert not any(path.startswith((str(outside), str(beside))) for path in paths)
    # The search opens each saved file, and on Mac and Linux each folder too, without
    # following a link or waiting on a pipe (where the platform has those flags).
    for path, flags in opened:
        if path.startswith(str(ag_root)) and path != str(real):
            assert flags & meter._O_NOFOLLOW == meter._O_NOFOLLOW, path
            assert flags & meter._O_NONBLOCK == meter._O_NONBLOCK, path
    if meter._DIR_FD_WALK:
        folders = {path for path, flags in opened if flags & meter._O_DIRECTORY}
        assert str(base) in folders and str(base / ".system_generated" / "logs") in folders
        assert all(path.startswith(str(ag_root)) for path in folders)

    # A folder with more conversations than its cap waits, and the other sources still count.
    other = antigravity_logs(ag_root, AG_OTHER)
    (other / "transcript.jsonl").write_bytes(reply_lines(antigravity_reply(created_at=NEW)))
    monkeypatch.setattr(meter, "MAX_ANTIGRAVITY_CONVERSATIONS", 1)
    third = meter._refresh_ledger(home)
    assert (third["status"], third["reason"]) == ("partial", "catching_up")
    after = ledger_of(home)
    assert keys_of(after) == keys_of(ledger)
    assert "source_budget_exceeded" not in after["coverage"]["reasons"]


def test_the_windows_spelling_of_a_project_path_counts_doubled(monkeypatch):
    monkeypatch.setattr(os, "name", "nt")
    assert meter._attribution_spellings("C:\\work\\project") == [
        b"C:\\work\\project", b"C:\\\\work\\\\project"]
    monkeypatch.setattr(os, "name", "posix")
    assert meter._attribution_spellings("/work/project") == [b"/work/project"]


@pytest.mark.parametrize("before", ["", "file://"])
def test_an_antigravity_name_is_found_wherever_a_block_edge_falls(tmp_path, before):
    root = str(tmp_path / "the-one-listed-project")           # the only, so the longest, path
    folder = tmp_path / "brain" / AG_CONVERSATION
    folder.mkdir(parents=True)
    projects = [{"alias": "only", "path": root, "remote": "https://example.test/team/p.git"}]
    span = len(before) + len(root)
    for shift in sorted({0, 1, 2, 3, 5, 7, 8, 9, 10, span // 2, span - 3, span - 2, span - 1,
                         span, span + 1, span + 2, span + 3}):
        # The text (`before` and the root) starts `shift` bytes before the first block edge.
        text = " " * (64 * 1024 - shift) + before + root + " end\n"
        (folder / "notes.md").write_bytes(text.encode("utf-8"))
        found = meter._conversation_project(str(tmp_path), AG_CONVERSATION, projects)
        assert found[:2] == ("only", None), shift


def test_an_antigravity_search_cap_is_128_mib_a_conversation_over_it_is_not_guessed(tmp_path,
                                                                                    monkeypatch):
    # A file of 20 MiB (a sparse file of zeros) is past the old 16 MiB cap, within the new one.
    folder = tmp_path / "brain" / AG_CONVERSATION
    folder.mkdir(parents=True)
    (folder / "notes.md").write_text("/synthetic/project\n", encoding="utf-8")
    with open(folder / "big.md", "wb") as handle:
        handle.truncate(20 * 1024 * 1024)
    projects = [{"alias": "only", "path": "/synthetic/project",
                 "remote": "https://example.test/team/p.git"}]
    assert meter.MAX_ATTRIBUTION_BYTES == 128 * 1024 * 1024
    assert meter.MAX_ATTRIBUTION_RUN_BYTES == 256 * 1024 * 1024
    found = meter._conversation_project(str(tmp_path), AG_CONVERSATION, projects)
    assert found[:2] == ("only", None)
    assert found[2] == 20 * 1024 * 1024 + len("/synthetic/project\n")
    # Over the cap the search ends incomplete, never with a guess.
    monkeypatch.setattr(meter, "MAX_ATTRIBUTION_BYTES", 20 * 1024 * 1024)
    found = meter._conversation_project(str(tmp_path), AG_CONVERSATION, projects)
    assert found[:2] == (None, "antigravity_search_incomplete")


def test_an_antigravity_search_entry_cap_is_20000_so_a_conversation_of_5200_files_is_searched(
        tmp_path):
    assert meter.MAX_ATTRIBUTION_ENTRIES == 20_000
    assert meter.MAX_ATTRIBUTION_RUN_ENTRIES == 50_000
    folder = tmp_path / "brain" / AG_CONVERSATION / "steps"
    folder.mkdir(parents=True)
    (folder / "notes.md").write_text("/synthetic/project\n", encoding="utf-8")
    for number in range(5_200):                       # past the old 5,000, within the new cap
        (folder / f"step{number}.log").write_text("nothing\n", encoding="utf-8")
    projects = [{"alias": "only", "path": "/synthetic/project",
                 "remote": "https://example.test/team/p.git"}]
    alias, reason, _used, listed = meter._conversation_project(
        str(tmp_path), AG_CONVERSATION, projects)
    assert (alias, reason) == ("only", None)
    assert 5_200 < listed <= meter.MAX_ATTRIBUTION_ENTRIES


def test_an_antigravity_search_refuses_a_file_that_is_not_the_one_the_walk_saw(tmp_path):
    note = tmp_path / "notes.md"
    note.write_text("/synthetic/project\n", encoding="utf-8")
    seen = os.lstat(note)
    names = {"only": [b"/synthetic/project"]}
    same = meter._search_attribution_file(
        str(note), (seen.st_dev, seen.st_ino), 1000, names, 40)
    other = meter._search_attribution_file(
        str(note), (seen.st_dev, seen.st_ino + 1), 1000, names, 40)
    over = meter._search_attribution_file(
        str(note), (seen.st_dev, seen.st_ino), 5, names, 40)
    assert same == ({"only"}, 19, True)
    assert other == (set(), 0, False)             # not the file the walk saw: not read
    assert over == (set(), 0, False)              # larger than the allowance: not read


@pytest.mark.skipif(os.name != "posix" or (hasattr(os, "geteuid") and os.geteuid() == 0),
                    reason="needs a file this account cannot read")
def test_an_antigravity_conversation_with_an_unreadable_file_is_left_unattributed(tmp_path):
    folder = tmp_path / "brain" / AG_CONVERSATION
    folder.mkdir(parents=True)
    (folder / "notes.md").write_text("/synthetic/project\n", encoding="utf-8")
    (folder / "secret.md").write_text("nothing\n", encoding="utf-8")
    (folder / "secret.md").chmod(0)
    projects = [{"alias": "only", "path": "/synthetic/project",
                 "remote": "https://example.test/team/p.git"}]
    try:
        found = meter._conversation_project(str(tmp_path), AG_CONVERSATION, projects)
    finally:
        (folder / "secret.md").chmod(0o600)
    assert found[:2] == (None, "antigravity_search_incomplete")


def test_an_antigravity_walk_lists_only_logs_and_refuses_a_missing_or_linked_root(tmp_path):
    root = tmp_path / "walk-root"
    root.mkdir()
    assert meter._enumerate_antigravity(str(root)) == ([], 0, False)      # no brain folder
    logs = antigravity_logs(root, AG_CONVERSATION)
    (logs / "transcript.jsonl").write_bytes(reply_lines(antigravity_reply()))
    (logs / "transcript_full.jsonl").write_bytes(reply_lines(antigravity_reply(999, 999)))
    (logs / "not-a-log.txt").write_bytes(b"x")
    (logs / "chunks").mkdir()
    (logs / "chunks" / "b.jsonl").write_bytes(reply_lines(antigravity_reply()))
    (root / "brain" / AG_OTHER / ".system_generated").mkdir(parents=True)  # no logs folder
    files, entries, waiting = meter._enumerate_antigravity(str(root))
    assert [name for name, _info in files] == [
        f"brain/{AG_CONVERSATION}/.system_generated/logs/transcript.jsonl"]
    assert (entries, waiting) == (2 + 1, False)
    with pytest.raises(meter.Unavailable):
        meter._enumerate_antigravity(str(tmp_path / "missing-root"))
    link = tmp_path / "linked-root"
    _make_folder_link(link, root)
    with pytest.raises(meter.Unavailable):
        meter._enumerate_antigravity(str(link))
    moved = tmp_path / "walk-root-two"
    moved.mkdir()
    _make_folder_link(moved / "brain", root / "brain")                     # a linked brain folder
    assert meter._enumerate_antigravity(str(moved)) == ([], 0, False)


def test_antigravity_attribution_shows_in_the_export_reasons(tmp_path):
    # Only attributed: the figure is marked inferred, and nothing is called unattributed.
    (tmp_path / "attributed-only").mkdir()
    only_home, only_root, _claude, only_project, _config = antigravity_home(
        tmp_path / "attributed-only")
    only_logs = antigravity_logs(only_root, AG_CONVERSATION)
    (only_logs.parent.parent / "notes.md").write_text(
        f"saved in {only_project}\n", encoding="utf-8")
    only_log = only_logs / "transcript.jsonl"
    only_log.write_bytes(reply_lines(antigravity_reply(created_at=OLD)))
    assert meter._refresh_ledger(only_home)["events"] == 0
    grow(only_log, reply_lines(antigravity_reply(120, 30, NEW)))
    assert meter._refresh_ledger(only_home)["status"] == "written"
    assert "antigravity_unattributed" not in ledger_of(only_home)["coverage"]["reasons"]
    only_export = json.loads((only_project / "dev" / "measurement" / "meter.json").read_text(
        encoding="utf-8"))
    assert "antigravity_project_inferred" in only_export["coverage"]["reasons"]
    assert "antigravity_unattributed" not in only_export["coverage"]["reasons"]

    second = tmp_path / "approved-project2"
    home, ag_root, _claude, project, _config_path = antigravity_home(
        tmp_path, extra_projects=[second])
    named = antigravity_logs(ag_root, AG_CONVERSATION)
    (named.parent.parent / "notes.md").write_text(f"saved in {project}\n", encoding="utf-8")
    unnamed = antigravity_logs(ag_root, AG_OTHER)               # its files name no project
    logs = [named / "transcript.jsonl", unnamed / "transcript.jsonl"]
    for log in logs:
        log.write_bytes(reply_lines(antigravity_reply(created_at=OLD)))
    assert meter._refresh_ledger(home)["events"] == 0           # the start

    grow(logs[0], reply_lines(antigravity_reply(120, 30, NEW)))
    grow(logs[1], reply_lines(antigravity_reply(7, 3, NEW)))
    assert meter._refresh_ledger(home)["status"] == "written"

    assert "antigravity_unattributed" in ledger_of(home)["coverage"]["reasons"]
    exports = {}
    for name, folder in (("sample", project), ("extra-0", second)):
        path = folder / "dev" / "measurement" / "meter.json"
        exports[name] = (path, json.loads(path.read_text(encoding="utf-8")))
    sample, other = exports["sample"][1], exports["extra-0"][1]
    # The matched project says its figure is inferred; every project says some Antigravity
    # conversation is unattributed, and only the matched one holds any Antigravity row.
    assert {"antigravity_project_inferred", "antigravity_unattributed"} <= set(
        sample["coverage"]["reasons"])
    assert "antigravity_unattributed" in other["coverage"]["reasons"]
    assert "antigravity_project_inferred" not in other["coverage"]["reasons"]
    row, = [item for item in sample["aggregates"] if item["tool"] == "antigravity"]
    assert row["events"] == 1 and row["model"] is None
    assert row["kinds"] == {"fresh_input": 120, "cache_read": None,
                            "cache_write": None, "output": 30}
    assert row["reference_tokens"]["total"] is None
    assert other["aggregates"] == []                             # the unattributed 7 and 3 stay private
    assert "SECRET" not in json.dumps([sample, other])

    # The pulse prints INCOMPLETE once, on the report's header line; the Antigravity row
    # says how many tokens, not what they cost.
    junit = tmp_path / "report.xml"
    junit.write_text('<testsuite tests="1" time="2"><testcase name="one" time="0.5" />'
                     "</testsuite>", encoding="utf-8")
    printed = {}
    for name, (path, _export) in exports.items():
        result = subprocess.run(
            [sys.executable, str(ROOT / "tests" / "gauge.py"), "--pulse",
             "--junit-report", str(junit), "--meter-aggregate", str(path)],
            cwd=ROOT, capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stderr
        printed[name] = result.stdout.splitlines()
        marked = [line for line in printed[name] if "INCOMPLETE" in line]
        assert len(marked) == 1
        assert marked[0].startswith(f"gauge: supplied project usage alias={name} ")
        assert "antigravity_unattributed" in marked[0]
        assert ("antigravity_project_inferred" in marked[0]) == (name == "sample")
    usage_line, = [line for line in printed["sample"] if "tool=antigravity" in line]
    assert "weighted=unknown" in usage_line


# ---- Antigravity: the code review's fixes (plan antigravity-reader, code response) ----

AG_THIRD = "5c4d3e2f-1a0b-4c9d-8e7f-6a5b4c3d2e1f"
AG_FOURTH = "2f1e0d9c-8b7a-4695-a483-72615a4b3c2d"


def ledger_cursor(home, alias, relative):
    key = meter._digest("cursor", alias, relative)
    return next((item for item in ledger_of(home)["cursors"] if item["file_key"] == key), None)


@pytest.mark.parametrize("when", ["after-the-start", "at-the-start"])
def test_one_over_long_antigravity_line_skips_that_log_and_never_stops_another_tool(
        tmp_path, monkeypatch, when):
    home, ag_root, claude_root, _project, _config_path = antigravity_home(tmp_path, claude=True)
    logs = antigravity_logs(ag_root, AG_CONVERSATION)
    log = logs / "transcript.jsonl"
    relative = f"brain/{AG_CONVERSATION}/.system_generated/logs/transcript.jsonl"
    long_reply = reply_lines(antigravity_reply(created_at=NEW, content="x" * 1000))
    log.write_bytes(reply_lines(antigravity_reply(created_at=OLD))
                    + (long_reply if when == "at-the-start" else b""))
    claude_log = claude_root / "session.jsonl"
    claude_log.write_bytes(claude_lines("old-1", timestamp=OLD))
    monkeypatch.setattr(meter, "MAX_LINE", 500)           # the Claude lines stay under it

    first = meter._refresh_ledger(home)                    # the start
    assert first["events"] == 0
    if when == "after-the-start":
        assert first["status"] == "written"
        before = ledger_cursor(home, "ag-source", relative)
        assert before is not None
        grow(log, long_reply)
    else:
        assert (first["status"], first["reason"]) == ("partial", "source_too_large")
        assert ledger_cursor(home, "ag-source", relative) is None      # nothing to keep yet
    grow(claude_log, claude_lines("new-1", timestamp=NEW))

    second = meter._refresh_ledger(home)

    # The log with the long line is skipped and named; the Claude reply still counts.
    assert (second["status"], second["reason"]) == ("partial", "source_too_large"), second
    ledger = ledger_of(home)
    assert keys_of(ledger) == [event_key_for("new-1")]
    assert "source_too_large" in ledger["coverage"]["reasons"]
    assert "source_budget_exceeded" not in ledger["coverage"]["reasons"]
    if when == "after-the-start":
        assert ledger_cursor(home, "ag-source", relative) == before       # its old position
    assert "SECRET" not in json.dumps(ledger)


@pytest.mark.skipif(os.name != "posix", reason="Windows walks by path (plan rule 7)")
def test_a_folder_swapped_for_a_link_during_the_antigravity_search_is_not_followed(
        tmp_path, monkeypatch):
    home, ag_root, _claude, project, _config_path = antigravity_home(tmp_path)
    folder = ag_root / "brain" / AG_CONVERSATION
    log = antigravity_logs(ag_root, AG_CONVERSATION) / "transcript.jsonl"
    log.write_bytes(reply_lines(antigravity_reply(created_at=OLD)))
    (folder / "a-notes.md").write_text("nothing named here\n", encoding="utf-8")
    (folder / "zz").mkdir()
    (folder / "zz" / "inner.md").write_text("nothing named here either\n", encoding="utf-8")
    outside = tmp_path / "outside-saved-files"
    outside.mkdir()
    (outside / "inner.md").write_text(f"saved in {project}\n", encoding="utf-8")
    assert meter._refresh_ledger(home)["events"] == 0                  # the start
    grow(log, reply_lines(antigravity_reply(created_at=NEW)))
    real_open, swapped = os.open, []

    def swap(path, *args, **kwargs):
        # The folder `zz` was listed as a real folder; now it becomes a link out of the root.
        if os.fsdecode(path).endswith("a-notes.md") and not swapped:
            (folder / "zz" / "inner.md").unlink()
            (folder / "zz").rmdir()
            _make_folder_link(folder / "zz", outside)
            swapped.append(True)
        return real_open(path, *args, **kwargs)

    with monkeypatch.context() as patched:
        patched.setattr(os, "open", swap)
        result = meter._refresh_ledger(home)

    assert swapped and result["status"] == "written", result
    event, = ledger_of(home)["events"]
    assert (event["project_alias"], event["ownership"], event["reasons"]) == (
        None, "unknown", ["antigravity_search_incomplete"])


def test_an_inferred_figure_keeps_its_label_after_the_antigravity_source_is_removed(tmp_path):
    home, ag_root, _claude, project, config_path = antigravity_home(tmp_path)
    logs = antigravity_logs(ag_root, AG_CONVERSATION)
    (logs.parent.parent / "notes.md").write_text(f"saved in {project}\n", encoding="utf-8")
    log = logs / "transcript.jsonl"
    log.write_bytes(reply_lines(antigravity_reply(created_at=OLD)))
    assert meter._refresh_ledger(home)["events"] == 0
    grow(log, reply_lines(antigravity_reply(120, 30, NEW)))
    assert meter._refresh_ledger(home)["status"] == "written"
    export_path = project / "dev" / "measurement" / "meter.json"

    def exported():
        return json.loads(export_path.read_text(encoding="utf-8"))

    assert "antigravity_project_inferred" in exported()["coverage"]["reasons"]

    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["sources"] = [item for item in config["sources"] if item["tool"] != "antigravity"]
    config_path.write_text(json.dumps(config), encoding="utf-8")
    config_path.chmod(0o600)
    assert meter._refresh_ledger(home)["status"] == "written"

    # The figure is still in the project's export, its tool no longer named, and still marked.
    after = exported()
    row, = [item for item in after["aggregates"] if item["kinds"]["fresh_input"] == 120]
    assert row["tool"] is None and row["kinds"]["output"] == 30
    assert "antigravity_project_inferred" in after["coverage"]["reasons"]


def test_an_antigravity_walk_never_follows_a_link_at_any_level_and_stops_at_its_entry_caps(
        tmp_path, monkeypatch):
    root = tmp_path / "walk-root"
    real_logs = antigravity_logs(root, AG_CONVERSATION)
    (real_logs / "transcript.jsonl").write_bytes(reply_lines(antigravity_reply()))
    tree = tmp_path / "outside-conversation"           # a whole conversation, outside the root
    (tree / ".system_generated" / "logs").mkdir(parents=True)
    decoy = reply_lines(antigravity_reply(9990, 9991, NEW))
    (tree / ".system_generated" / "logs" / "transcript.jsonl").write_bytes(decoy)
    _make_folder_link(root / "brain" / AG_OTHER, tree)                         # the conversation
    (root / "brain" / AG_THIRD).mkdir()
    _make_folder_link(root / "brain" / AG_THIRD / ".system_generated",
                      tree / ".system_generated")                              # its middle folder
    (root / "brain" / AG_FOURTH / ".system_generated").mkdir(parents=True)
    _make_folder_link(root / "brain" / AG_FOURTH / ".system_generated" / "logs",
                      tree / ".system_generated" / "logs")                     # its logs folder

    files, entries, waiting = meter._enumerate_antigravity(str(root))

    assert [name for name, _info in files] == [
        f"brain/{AG_CONVERSATION}/.system_generated/logs/transcript.jsonl"]
    assert not waiting
    # The entry caps: the listing of `brain/` (4 folders), then of a conversation's logs.
    monkeypatch.setattr(meter, "MAX_ATTRIBUTION_RUN_ENTRIES", 1)
    assert meter._enumerate_antigravity(str(root)) == ([], 2, True)    # stops in `brain/`
    monkeypatch.setattr(meter, "MAX_ATTRIBUTION_RUN_ENTRIES", 4)       # `brain/` fits, its logs do not
    assert meter._enumerate_antigravity(str(root)) == ([], 5, True)


def make_two_attributed_conversations(tmp_path):
    """Two conversations that both name the project, each with one old reply (the start)."""
    home, ag_root, _claude, project, _config_path = antigravity_home(tmp_path)
    logs = {}
    for conversation in (AG_CONVERSATION, AG_OTHER):
        folder = antigravity_logs(ag_root, conversation)
        (folder.parent.parent / "notes.md").write_text(f"saved in {project}\n", encoding="utf-8")
        logs[conversation] = folder / "transcript.jsonl"
        logs[conversation].write_bytes(reply_lines(antigravity_reply(created_at=OLD)))
    assert meter._refresh_ledger(home)["events"] == 0                  # the start
    grow(logs[AG_CONVERSATION], reply_lines(antigravity_reply(120, 30, NEW)))
    grow(logs[AG_OTHER], reply_lines(antigravity_reply(7, 3, NEW)))
    return home, ag_root


@pytest.mark.parametrize("limit", ["search-bytes", "search-entries", "read-bytes"])
def test_an_antigravity_conversation_the_refresh_cannot_pay_for_waits_for_the_next_refresh(
        tmp_path, monkeypatch, limit):
    home, ag_root = make_two_attributed_conversations(tmp_path)
    patched = {
        "search-bytes": ("MAX_ATTRIBUTION_RUN_BYTES", meter.MAX_ATTRIBUTION_BYTES),
        "search-entries": ("MAX_ATTRIBUTION_RUN_ENTRIES", meter._enumerate_antigravity(
            str(ag_root))[1] + meter.MAX_ATTRIBUTION_ENTRIES),
        "read-bytes": ("MAX_RUN_READ_BYTES", meter.MAX_ATTRIBUTION_BYTES + 10),
    }[limit]
    real_value = getattr(meter, patched[0])
    monkeypatch.setattr(meter, *patched)

    second = meter._refresh_ledger(home)

    # The first conversation (by name) is searched and counted; the second waits, labelled.
    assert (second["status"], second["reason"]) == ("partial", "catching_up"), second
    assert keys_of(ledger_of(home)) == [antigravity_key(NEW, 120, 30)]

    monkeypatch.setattr(meter, patched[0], real_value)                 # not monkeypatch.undo()
    third = meter._refresh_ledger(home)
    assert third["status"] == "written", third
    assert keys_of(ledger_of(home)) == sorted([antigravity_key(NEW, 120, 30),
                                               antigravity_key(NEW, 7, 3, AG_OTHER)])


def test_a_claude_time_beyond_the_year_9999_limit_is_an_unknown_time_not_a_stopped_refresh(
        tmp_path):
    home, _ag_root, claude_root, _project, _config_path = antigravity_home(tmp_path, claude=True)
    claude_log = claude_root / "session.jsonl"
    claude_log.write_bytes(claude_lines("old-1", timestamp=OLD))
    assert meter._refresh_ledger(home)["events"] == 0                  # the start
    grow(claude_log, claude_lines("far-1", timestamp="9999-12-31T23:59:59-05:00")
         + claude_lines("new-1", timestamp=NEW))

    result = meter._refresh_ledger(home)

    # The reply with that time counts with its time unknown, as any unreadable time does.
    assert result["status"] == "written", result
    ledger = ledger_of(home)
    assert keys_of(ledger) == sorted([event_key_for("far-1"), event_key_for("new-1")])
    by_key = {event["event_key"]: event for event in ledger["events"]}
    assert by_key[event_key_for("far-1")]["time_coverage"] == "unknown"
    assert by_key[event_key_for("new-1")]["time_coverage"] == "known"


@pytest.mark.skipif(os.name != "posix" or (hasattr(os, "geteuid") and os.geteuid() == 0),
                    reason="needs a folder this account cannot read")
def test_an_antigravity_conversation_with_an_unreadable_folder_is_left_unattributed(tmp_path):
    folder = tmp_path / "brain" / AG_CONVERSATION
    (folder / "sub").mkdir(parents=True)
    (folder / "notes.md").write_text("/synthetic/project\n", encoding="utf-8")
    (folder / "sub" / "inner.md").write_text("nothing\n", encoding="utf-8")
    (folder / "sub").chmod(0)
    projects = [{"alias": "only", "path": "/synthetic/project",
                 "remote": "https://example.test/team/p.git"}]
    try:
        found = meter._conversation_project(str(tmp_path), AG_CONVERSATION, projects)
    finally:
        (folder / "sub").chmod(0o700)
    assert found[:2] == (None, "antigravity_search_incomplete")


# ---- Config-driven model weights, configurable tiers, v6->v7, Antigravity fixes ----


def test_models_config_absence_degrades_gracefully_and_bare_status_skips_opening(
        tmp_path, monkeypatch):
    home, claude_root, _codex_root, project, config_path = c1_home(tmp_path, monkeypatch)
    models_path = home / ".cairn" / "meter-models.json"
    models_path.unlink()
    log = claude_root / "session.jsonl"
    log.write_bytes(claude_lines("old-1", timestamp=OLD))
    assert meter._refresh_ledger(home)["events"] == 0
    grow(log, priced_lines("new-1", NEW, model="claude-fable-5-2", cwd=str(project)))

    # Bare status validates meter.json without opening an explicit models_config file.
    bad_models = home / ".cairn" / "broken-models.json"
    bad_models.write_text("{not-json", encoding="utf-8")
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    config_path.write_text(json.dumps({**cfg, "models_config": str(bad_models)}),
                           encoding="utf-8")
    opened_models = []
    real_load_models = meter.load_models_config
    with monkeypatch.context() as patched:
        patched.setattr(meter, "_fixed_user_home", lambda: home)
        patched.setattr(meter, "load_models_config",
                        lambda *a, **kw: opened_models.append(True))
        patched.setattr(sys, "argv", ["meter.py", "--json"])
        rc = meter._main()
    assert rc == 5 and opened_models == []
    assert real_load_models
    config_path.write_text(json.dumps(cfg), encoding="utf-8")

    # Without ~/.cairn/meter-models.json, raw counts persist while tier & weighted stay unknown.
    res = meter._refresh_ledger(home)
    assert res["status"] == "written"
    ledger = ledger_of(home)
    assert ledger["ratio_version"] is None and ledger["ratio_index"] is None
    assert "models_config_missing" in ledger["coverage"]["reasons"]
    row, = ledger["aggregates"]
    assert row["reference_index"] is None
    assert set(row["reference_tokens"].values()) == {None}
    export = json.loads((project / "dev" / "measurement" / "meter.json").read_text(
        encoding="utf-8"))
    assert export["schema"] == "cairn-meter-project/3"
    assert export["ratio_version"] is None
    assert export["aggregates"][0]["tier"] == "unknown"
    assert len(export["by_tier"]) == 1
    assert export["by_tier"][0]["tier"] == "unknown"
    assert export["by_tier"][0]["events"] == 1
    assert "models_config_missing" in export["coverage"]["reasons"]


def test_models_config_path_containment_unc_link_hardlink_and_schema_rejections(tmp_path):
    base = reference_models()
    home, _codex_root, project, config_path = c2_home(tmp_path, models_config=False)
    config_data = json.loads(config_path.read_text(encoding="utf-8"))

    # Missing explicit models_config fails closed with config_invalid.
    missing_path = tmp_path / "missing-models.json"
    config_path.write_text(json.dumps({**config_data, "models_config": str(missing_path)}),
                           encoding="utf-8")
    assert meter._refresh_ledger(home) == {
        "status": "unavailable", "reason": "config_invalid", "coverage": "unknown"}

    # Windows UNC / mixed-slash / device prefixes and containment inside project/source fail closed.
    for bad_path in (
        "\\\\server\\share\\models.json",
        "//server/share/models.json",
        "\\/server/share/models.json",
        "/\\server/share/models.json",
        str(project / "models.json"),
        str(project),
        str(tmp_path / "approved-source" / "models.json"),
    ):
        with pytest.raises(meter.Unavailable) as exc:
            meter.validate_config_bytes(
                json.dumps({**config_data, "models_config": bad_path}).encode("utf-8"))
        assert exc.value.reason == "config_invalid"

    # Symlinked ancestor directory redirecting explicit models_config into project fails closed.
    if _can_make_file_link():
        inside = project / "nested.json"
        inside.write_bytes(MODELS_CONFIG_SRC.read_bytes())
        ancestor_link = tmp_path / "sneaky-dir-link"
        _make_folder_link(ancestor_link, project)
        cfg_sym_ancestor = meter.validate_config_bytes(
            json.dumps({**config_data, "models_config": str(ancestor_link / "nested.json")}
                       ).encode("utf-8"))
        with pytest.raises(meter.Unavailable) as exc:
            meter.load_models_config(home, cfg_sym_ancestor)
        assert exc.value.reason == "config_invalid"

        # Symlinked default meter-models.json fails closed even when unconfigured explicit.
        default_models = home / ".cairn" / "meter-models.json"
        outside = tmp_path / "outside-models.json"
        outside.write_bytes(MODELS_CONFIG_SRC.read_bytes())
        default_models.symlink_to(outside)
        with pytest.raises(meter.Unavailable) as exc:
            meter.load_models_config(home, meter.validate_config_bytes(
                json.dumps(config_data).encode("utf-8")))
        assert exc.value.reason == "config_invalid"
        default_models.unlink()

        # Hardlinked meter-models.json (st_nlink == 2) fails closed.
        os.link(outside, default_models)
        try:
            with pytest.raises(meter.Unavailable) as exc:
                meter.load_models_config(home, meter.validate_config_bytes(
                    json.dumps(config_data).encode("utf-8")))
            assert exc.value.reason == "config_invalid"
        finally:
            default_models.unlink()

    # Schema / weights / prefix / tier_rules / adapter rejections.
    def reject_raw(raw_bytes):
        with pytest.raises(meter.Unavailable) as exc:
            meter.validate_models_config_bytes(raw_bytes)
        assert exc.value.reason == "config_invalid"

    def reject_mut(mutator):
        cand = copy.deepcopy(base)
        mutator(cand)
        reject_raw(json.dumps(cand).encode("utf-8"))

    reject_raw(b'{"schema":"cairn-meter-models/1","schema":"cairn-meter-models/1"}')
    reject_raw(b'{"schema":NaN}')
    reject_raw(b" " * (meter.MAX_CONFIG_BYTES + 1))
    reject_mut(lambda d: d.update(schema="cairn-meter-models/99"))
    reject_mut(lambda d: d.update(extra=1))
    reject_mut(lambda d: d.update(ratio_version="cairn-api-token-index/bad"))
    reject_mut(lambda d: d.update(tiers=[]))
    reject_mut(lambda d: d.update(tiers=["t" + str(i) for i in range(33)]))
    reject_mut(lambda d: d.update(tiers=["high", "unknown"]))
    reject_mut(lambda d: d.update(tiers=["high", "unspecified"]))
    reject_mut(lambda d: d.update(tiers=["high", "high"]))
    reject_mut(lambda d: d.update(tiers=["High"]))
    reject_mut(lambda d: d["models"]["claude-opus-5-5"].update(tier="nonexistent"))
    reject_mut(lambda d: d["models"]["claude-opus-5-5"].update(fresh_input=[True, 1]))
    reject_mut(lambda d: d["models"]["claude-opus-5-5"].update(fresh_input=[1, 0]))
    reject_mut(lambda d: d["models"]["claude-opus-5-5"].update(fresh_input=[-1, 1]))
    reject_mut(lambda d: d["models"]["claude-opus-5-5"].pop("cache_write_5m"))
    reject_mut(lambda d: d["models"]["gpt-5.3-codex"].update(cache_write_5m=[1, 1]))
    reject_mut(lambda d: d["models"]["gpt-5.3-codex"].update(long_prompt=None))
    reject_mut(lambda d: d["models"]["claude-haiku-5-5"]["long_prompt"].update(over_tokens=0))
    reject_mut(lambda d: d["models"]["gemini-4-argon"].update(
        prefixes=["gemini-4-neon-"]))                                  # overlaps sibling model
    reject_mut(lambda d: d["models"]["claude-opus-5-5"].update(
        prefixes=["claude-sonnet-4-6-x"]))                             # overlaps prefix on other model
    reject_mut(lambda d: d["models"]["claude-opus-5-5"].update(
        prefixes=["gpt-5.3-codex"]))                                   # prefix equals exact model key
    reject_mut(lambda d: d["tier_rules"].append({"prefix": "claude-op", "tier": "high"}))
    reject_mut(lambda d: d["tier_rules"].append({"segment": "high", "tier": "high"}))
    reject_mut(lambda d: d["tier_rules"].append({"segment": "frontier", "tier": "frontier"}))
    reject_mut(lambda d: d["tier_rules"].append({"segment": "unknown", "tier": "high"}))
    reject_mut(lambda d: d["tier_rules"].append({"segment": "neon", "tier": "high"}))
    reject_mut(lambda d: d["tier_rules"].append({"prefix": "x", "segment": "x", "tier": "high"}))
    reject_mut(lambda d: d["tools"]["antigravity"].update(lead_factor=1))
    reject_mut(lambda d: d["tools"]["antigravity"].update(lead_factor=1001))
    reject_mut(lambda d: d["tools"]["antigravity"].update(lead_factor=True))
    reject_mut(lambda d: d["tools"]["antigravity"].update(max_bytes=0))
    reject_mut(lambda d: d["tools"]["antigravity"].update(max_entries=0))
    reject_mut(lambda d: d["tools"]["antigravity"].update(log_filename="CON.jsonl"))
    reject_mut(lambda d: d["tools"]["antigravity"].update(log_filename="../evil.jsonl"))
    reject_mut(lambda d: d["tools"]["antigravity"].update(log_filename="bad.txt"))
    reject_mut(lambda d: d["tools"]["antigravity"].update(cache_read_field="input_tokens"))
    reject_mut(lambda d: d["tools"]["antigravity"].update(cache_read_field="usage"))


def test_ledger_v6_migrates_to_v7_in_place_and_rejects_mismatched_pairs(
        tmp_path, monkeypatch):
    at_clock(monkeypatch, CLOCK)
    home, log, config_path = claude_home_started(tmp_path, monkeypatch)
    project = json.loads(config_path.read_text(encoding="utf-8"))["projects"][0]["path"]
    grow(log, priced_lines("old-1", day_stamp(5), cwd=project))
    at_clock(monkeypatch, LATER)
    assert meter._refresh_ledger(home)["status"] == "written"

    ledger_path = home / ".cairn" / "meter" / "ledger.json"
    v6 = json.loads(ledger_path.read_bytes())
    v6["schema"] = "cairn-meter-ledger/6"
    v6["reader_version"] = "cairn-source-readers/6"
    saved_daily = copy.deepcopy(v6["daily"])
    assert saved_daily and saved_daily[0]["reference_tokens"]["total"] == "92.4"
    ledger_path.write_bytes(as_bytes(v6))

    migrated_direct = meter._load_ledger(as_bytes(v6), LATER)
    assert migrated_direct["schema"] == "cairn-meter-ledger/7"
    assert migrated_direct["reader_version"] == "cairn-source-readers/7"
    assert migrated_direct["daily"] == saved_daily

    # Incremental refresh migrates v6->v7 in place while preserving daily sums & counting forward.
    grow(log, priced_lines("new-2", day_stamp(29), model="claude-fable-5-2", cwd=project))
    assert meter._refresh_ledger(home)["status"] == "written"
    after = ledger_of(home)
    assert after["schema"] == "cairn-meter-ledger/7"
    assert after["reader_version"] == "cairn-source-readers/7"
    assert after["daily"] == saved_daily

    # Mismatched (schema, reader_version) or asymmetric null ratio fields fail closed.
    for schema, reader in (
        ("cairn-meter-ledger/6", "cairn-source-readers/7"),
        ("cairn-meter-ledger/7", "cairn-source-readers/6"),
    ):
        bad = {**after, "schema": schema, "reader_version": reader}
        with pytest.raises(meter.Unavailable) as exc:
            meter._load_ledger(as_bytes(bad), LATER)
        assert exc.value.reason == "ledger_invalid"

    for mut in (
        {"ratio_version": None},
        {"ratio_index": None},
    ):
        bad = {**after, **mut}
        with pytest.raises(meter.Unavailable) as exc:
            meter._load_ledger(as_bytes(bad), LATER)
        assert exc.value.reason == "ledger_invalid"

    # reference_index: None rejects any non-None reference_tokens entry.
    bad_row = daily_row("2026-11-01", reference_index=None)
    bad_row["reference_tokens"]["total"] = "1.0"
    with pytest.raises(ValueError):
        meter._validate_aggregate_row(bad_row)

    # _add_rows with differing reference_index and current_ratio_version=None zeros reference_tokens.
    left = daily_row("2026-11-01", reference_index="cairn-api-token-index/2026-11-06")
    left["reference_tokens"] = {k: "1" for k in left["reference_tokens"]}
    right = daily_row("2026-11-01", reference_index=None)
    merged = meter._add_rows(left, right, current_ratio_version=None)
    assert merged["reference_index"] is None
    assert set(merged["reference_tokens"].values()) == {None}
    meter._validate_aggregate_row(merged)


def test_tier_resolution_prefix_segment_weights_and_by_tier_export(tmp_path, monkeypatch):
    cfg = reference_models()
    # Exact, prefix, segment without effort collision (-high != high), and ties.
    assert meter._resolve_model_tier("claude-fable-5-2", cfg) == "frontier"
    assert meter._resolve_model_tier("claude-fable-5-2-20261201", cfg) == "frontier"
    assert meter._resolve_model_tier("gemini-4-neon-high", cfg) == "medium"
    assert meter._resolve_model_tier("gemini-4-astra-high", cfg) == "frontier"
    assert meter._resolve_model_tier("gemini-4-carbon-xhigh", cfg) == "frontier"
    assert meter._resolve_model_tier("my-opus-sonnet-clash", cfg) == "unknown"
    assert meter._resolve_model_tier("completely-unknown", cfg) == "unknown"
    assert meter._resolve_model_tier("claude-fable-5-2", None) == "unknown"

    # Custom configured tiers drive by_tier ordering & exclude empty tiers.
    custom = meter.validate_models_config_bytes(json.dumps({
        "schema": "cairn-meter-models/1",
        "ratio_version": "cairn-api-token-index/2026-11-22",
        "tiers": ["top", "base"],
        "models": {
            "alpha-1": {
                "tier": "top",
                "prefixes": ["alpha-1-"],
                "fresh_input": [1, 3], "cache_read": [0, 1], "output": [1, 1],
                "cache_write_mode": "unbilled",
            },
        },
        "tier_rules": [{"segment": "beta", "tier": "base"}],
    }).encode("utf-8"))
    assert meter._resolve_model_tier("alpha-1-fast", custom) == "top"
    assert meter._resolve_model_tier("gamma-beta-x", custom) == "base"

    home, claude_root, _codex_root, project, _cfg_path = c1_home(tmp_path, monkeypatch)
    install_models_config(home, custom)
    config = meter.validate_config_bytes((home / ".cairn" / "meter.json").read_bytes())
    log = claude_root / "session.jsonl"
    e1 = meter._event_record(
        tool="claude", event_key=meter._digest("e1"), aliases=["claude-source"],
        thread="t1", timestamp=NEW, time_known=True,
        kinds={"fresh_input": 1, "cache_read": 0, "cache_write": 0, "output": 0},
        model="alpha-1-fast", model_provenance="usage_record",
        effective_model="alpha-1-fast",
        project_alias="sample", project_state="current_local_verified", ownership="proven")
    e2 = meter._event_record(
        tool="claude", event_key=meter._digest("e2"), aliases=["claude-source"],
        thread="t2", timestamp="2026-11-06T12:00:00Z", time_known=True,
        kinds={"fresh_input": 1, "cache_read": 0, "cache_write": 0, "output": 0},
        model="alpha-1-fast", model_provenance="usage_record",
        effective_model="alpha-1-fast",
        project_alias="sample", project_state="current_local_verified", ownership="proven")
    e3 = meter._event_record(
        tool="claude", event_key=meter._digest("e3"), aliases=["claude-source"],
        thread="t3", timestamp=NEW, time_known=True,
        kinds={"fresh_input": 5, "cache_read": None, "cache_write": None, "output": 1},
        model=None, model_provenance="unknown", effective_model=None,
        project_alias="sample", project_state="current_local_verified", ownership="proven")
    ledger = meter._new_ledger(
        meter._load_ledger(None), config, [e1, e2, e3], [], [], [],
        [{"alias": "sample", "remote": "https://example.test/team/project.git"}],
        {"captured"}, set(), [], set(), models_config=custom)
    export_bytes = meter._project_export_bytes(ledger, config, "sample", custom)
    export = json.loads(export_bytes)
    # "base" has 0 events so only "top" and "unknown" appear, in order.
    assert [row["tier"] for row in export["by_tier"]] == ["top", "unknown"]
    assert export["by_tier"][1]["reference_tokens"]["total"] is None
    # Parity check with pulse._parse_meter_aggregate on [1, 3] rounding.
    pulse_mod_spec = importlib.util.spec_from_file_location(
        "pulse_check", ROOT / "dev" / "tools" / "pulse.py")
    pulse_mod = importlib.util.module_from_spec(pulse_mod_spec)
    pulse_mod_spec.loader.exec_module(pulse_mod)
    parsed = pulse_mod._parse_meter_aggregate(export_bytes)
    assert len(parsed["by_tier"]) == 2


def test_antigravity_model_cache_read_tokens_and_adapter_bounds(tmp_path):
    cfg = reference_models()
    home, ag_root, _claude, project, _cfg_path = antigravity_home(tmp_path)
    install_models_config(home, cfg)
    logs = antigravity_logs(ag_root, AG_CONVERSATION)
    (logs.parent.parent / "notes.md").write_text(f"saved in {project}\n", encoding="utf-8")
    log = logs / "transcript.jsonl"
    log.write_bytes(reply_lines(antigravity_reply(created_at=OLD)))
    assert meter._refresh_ledger(home)["events"] == 0

    good = antigravity_reply(120, 30, NEW, model="gemini-4-neon-xhigh", cache_read_tokens=200)
    null_model = antigravity_reply(10, 10, "2026-11-05T12:00:01Z", model=None)
    null_cache = antigravity_reply(10, 10, "2026-11-05T12:00:02Z", cache_read_tokens=None)
    bool_cache = antigravity_reply(10, 10, "2026-11-05T12:00:03Z", cache_read_tokens=True)
    grow(log, reply_lines(good, null_model, null_cache, bool_cache))

    res = meter._refresh_ledger(home)
    assert res["status"] == "written"
    ledger = ledger_of(home)
    assert "invalid_record" in ledger["coverage"]["reasons"]
    event, = ledger["events"]
    assert event["model"] == event["effective_model"] == "gemini-4-neon-xhigh"
    assert event["model_provenance"] == "usage_record"
    assert event["kinds"] == {
        "fresh_input": 120, "cache_read": 200, "cache_write": None, "output": 30}
    export = json.loads((project / "dev" / "measurement" / "meter.json").read_text(
        encoding="utf-8"))
    row, = export["aggregates"]
    assert row["tier"] == "medium"
    # 120*3 + 200*(3/20) + 0 + 30*15 = 360 + 30 + 450 = 840
    assert row["reference_tokens"] == {
        "fresh_input": "360", "cache_read": "30", "cache_write": "0",
        "output": "450", "total": "840"}
    assert [b["tier"] for b in export["by_tier"]] == ["medium"]

    # Configured adapter log_filename, max_entries, and lead_factor take effect via _refresh_ledger.
    custom = copy.deepcopy(cfg)
    custom["tools"]["antigravity"]["log_filename"] = "custom.jsonl"
    custom["tools"]["antigravity"]["max_entries"] = 1
    custom["tools"]["antigravity"]["lead_factor"] = 20
    install_models_config(home, custom)
    custom_log = logs / "custom.jsonl"
    custom_log.write_bytes(reply_lines(antigravity_reply(created_at=OLD)))
    os.utime(custom_log, ns=(1, 1))
    (logs.parent.parent / "other.md").write_text("empty\n", encoding="utf-8")
    assert meter._refresh_ledger(home)["events"] == 1
    grow(custom_log, reply_lines(antigravity_reply(11, 13, "2026-11-05T12:05:00Z")))
    assert meter._refresh_ledger(home)["events"] == 2
    custom_event = max(ledger_of(home)["events"], key=lambda e: e["observed_at"])
    # max_entries=1 caps the 2-entry conversation directory as search incomplete.
    assert custom_event["reasons"] == ["antigravity_search_incomplete"]
