# SPDX-License-Identifier: MIT
"""Synthetic-only contracts for tools/meter.py; no host-source access."""

import copy
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
METER = ROOT / "tools/meter.py"
spec = importlib.util.spec_from_file_location("meter_reader", METER)
meter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meter)
STAMP = "2026-11-05T12:00:00Z"
POSIX_ONLY = pytest.mark.skipif(os.name != "posix", reason="private-file checks require POSIX evidence")


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
    return row("event_msg", {"type": "item_completed", "started_at_ms": start,
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
    (-1, 3500), (3500, 1000), (1000, 2**63),
])
def test_timing_reader_invalid_endpoints_remain_unknown(start, end):
    result = read("codex", codex() + [timing_record(start=start, end=end)])
    assert result["timing_observations"] == []
    assert result["timing_coverage"] == "unknown"
    assert "invalid_record" in result["issues"]


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


def test_codex_direct_response_not_running_totals_or_checkpoints():
    records = codex()
    records.append(row("event_msg", {"type": "token_count", "info": {
        "total_token_usage": {"input_tokens": 900}}}))
    result = read("codex", records)
    event, = result["events"]
    assert event["kinds"] == {"fresh_input": 12, "cache_read": 8,
                              "cache_write": 0, "output": 4}
    assert set(event) == {"kinds"}
    assert result["coverage"] == "unknown"
    assert "legacy_checkpoint_unreconciled" in result["issues"]


def test_codex_per_turn_cwd_override_does_not_use_initial_or_latest_cwd():
    records = codex()
    second = copy.deepcopy(records[-1])
    second["payload"].update(turn_id="turn-b", root_turn_id="turn-b", response_id="response-b")
    records.extend([row("turn_context", {"turn_id": "turn-b", "cwd": "/synthetic/repo-b"}), second])
    events = read("codex", records)["events"]
    assert len(events) == 2
    assert all(set(event) == {"kinds"} for event in events)


@pytest.mark.parametrize("field,value", [("cached_input_tokens", 21),
                                        ("reasoning_output_tokens", 5),
                                        ("total_tokens", 99),
                                        ("cache_write_input_tokens", 2)])
def test_codex_inconsistent_or_unproven_cache_semantics_are_unknown(field, value):
    records = codex()
    records[-1]["payload"]["usage"][field] = value
    assert read("codex", records)["events"] == []


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
    assert result["events"] and set(result["events"][0]) == {"kinds"}
    assert "source_turn_binding_unproven" in result["issues"]
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
    assert "source_turn_binding_unproven" in read("codex", records)["issues"]


def test_codex_context_must_precede_response_and_duplicates_must_agree():
    records = codex()
    context = records.pop(1)
    records.append(context)
    assert "source_turn_binding_unproven" in read("codex", records)["issues"]
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
    duplicate["payload"]["turn_token_usage"]["input_tokens"] += 1
    duplicate["payload"]["turn_token_usage"]["total_tokens"] += 1
    result = read("codex", records + [duplicate])
    assert result["events"] == []
    assert "conflicting_usage" in result["issues"]


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
    assert result["events"] and "source_turn_binding_unproven" in result["issues"]


@pytest.mark.parametrize("field", ["turn_token_usage", "thread_token_usage"])
@pytest.mark.parametrize("bad", [True, "1", -1, 2**63, None])
def test_codex_snapshots_are_validated_but_never_counted(field, bad):
    records = codex()
    records[-1]["payload"][field]["input_tokens"] = bad
    assert read("codex", records)["events"] == []
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
    assert result["events"] == []
    assert "conflicting_usage" in result["issues"]


@pytest.mark.parametrize("field", ["forked_from_id", "parent_thread_id", "history_base",
                                  "forked_from_ordinal_exclusive", "subagent_history_start_ordinal"])
def test_inherited_codex_history_never_gets_a_directory_binding(field):
    records = codex()
    records[0]["payload"][field] = 1
    result = read("codex", records)
    assert set(result["events"][0]) == {"kinds"}
    assert "source_turn_binding_unproven" in result["issues"]


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
    assert set(read("codex", records)["events"][0]) == {"kinds"}


def test_claude_cache_kinds_and_ttl_are_disjoint_not_added_twice():
    records = claude()
    records[0]["message"]["usage"]["cache_creation"] = {
        "ephemeral_5m_input_tokens": 1, "ephemeral_1h_input_tokens": 1}
    event, = read("claude", records)["events"]
    assert event["kinds"] == {"fresh_input": 10, "output": 4, "cache_write": 2, "cache_read": 8}
    assert set(event) == {"kinds"}
    records[0]["message"]["usage"]["cache_creation"]["ephemeral_5m_input_tokens"] = 2
    assert not read("claude", records)["events"]


def test_requestless_claude_does_not_guess_lineage_from_directory():
    records = claude()
    del records[0]["requestId"]
    assert not read("claude", records)["events"]


@pytest.mark.parametrize("bad", [True, False, "1", 1.5, -1, 2**63, None])
@pytest.mark.parametrize("tool,fixture", [("codex", codex), ("claude", claude)])
def test_numeric_values_are_exact_bounded_integers(tool, fixture, bad):
    records = fixture()
    usage = records[-1]["payload"]["usage"] if tool == "codex" else records[-1]["message"]["usage"]
    usage["input_tokens"] = bad
    result = read(tool, records)
    assert not result["events"]
    assert "invalid_record" in result["issues"]


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
    assert not read("codex", records)["events"]


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


def test_default_cli_is_disabled_and_does_not_consume_stdin(tmp_path):
    result = subprocess.run([sys.executable, str(METER), "--json"], input="SECRET-BODY",
                            capture_output=True, text=True, cwd=tmp_path, check=False,
                            env={"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)})
    assert result.returncode == 0
    assert not result.stderr
    value = json.loads(result.stdout)
    assert value["collection"] == "disabled"
    assert value["usage"] == {tool: "unknown" for tool in meter.TOOLS}
    assert list(tmp_path.iterdir()) == []


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
def test_enabled_cli_stops_before_source_or_ledger_io(tmp_path):
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
    result = subprocess.run([sys.executable, str(METER), "--json"], cwd=tmp_path,
                            env={"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)}, capture_output=True,
                            text=True, timeout=5, check=False)
    assert result.returncode == 5
    assert json.loads(result.stdout)["collection"] == "unavailable"
    assert "PRIVATE-SENTINEL" not in result.stdout + result.stderr
    assert ledger.read_text(encoding="utf-8") == "PRIVATE-SENTINEL"


@POSIX_ONLY
def test_disabled_cli_does_not_open_configured_sources_or_ledger(tmp_path):
    cairn = tmp_path / ".cairn"
    cairn.mkdir(mode=0o700)
    os.chmod(cairn, 0o700)
    source = tmp_path / "synthetic-source"
    source.mkdir()
    os.mkfifo(source / "do-not-open")
    write_config(cairn / "meter.json", valid_config(enabled=False,
        sources=[{"alias": "codex-main", "tool": "codex", "root": str(source)}]))
    result = subprocess.run([sys.executable, str(METER), "--json"], cwd=tmp_path,
                            env={"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)}, capture_output=True,
                            text=True, timeout=5, check=False)
    assert result.returncode == 0
    assert json.loads(result.stdout)["collection"] == "disabled"


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
