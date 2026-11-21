"""A usage record counts toward a project only by its own working folder.

Arc C1 of the Claude usage plan. Every record here is written by hand from the
shapes in Detail D1, D2 and D5. No assistant log is read. The reader is driven
through `meter.read_records`, the public entry point the criterion names, and
`meter._project_for_folder` and `meter._build_mappings` are called directly
where the plan names them.
"""

import importlib.util
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from tests._repo_root import repository_root

ROOT = repository_root(Path(__file__))
METER = ROOT / "dev/tools/meter.py"
spec = importlib.util.spec_from_file_location("meter_claude_usage_reader", METER)
meter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meter)

STAMP = "2026-11-05T12:00:00Z"
REMOTE = "https://example.test/team/project.git"
SEP = "\\" if os.name == "nt" else "/"
BASE = "C:\\synthetic" if os.name == "nt" else "/synthetic"
PROJECT = BASE + SEP + "project"
OTHER_PROJECT = BASE + SEP + "other-project"
SOURCE_ROOT = BASE + SEP + "source"
OTHER_ROOT = BASE + SEP + "source-two"
MISSING = object()


def encoded(records):
    return [(json.dumps(record) + "\n").encode() for record in records]


def rec(**changes):
    """An assistant record shaped like the `claude()` fixture in the integration tests."""
    record = {"type": "assistant", "timestamp": STAMP, "sessionId": "session-a",
              "requestId": "request-a", "cwd": PROJECT,
              "message": {"id": "message-a", "model": "synthetic-model",
                          "content": "SECRET-BODY", "usage": {
                              "input_tokens": 10, "output_tokens": 4,
                              "cache_creation_input_tokens": 2,
                              "cache_read_input_tokens": 8}}}
    record.update(changes)
    return record


def cfg(paths=(PROJECT,), roots=(SOURCE_ROOT,)):
    aliases = ["alpha", "beta", "gamma"]
    return {"version": 1, "enabled": True,
            "sources": [{"alias": "source-" + str(index), "tool": "claude", "root": root}
                        for index, root in enumerate(roots)],
            "projects": [{"alias": aliases[index], "path": path, "remote": REMOTE}
                         for index, path in enumerate(paths)]}


def read(records, *, config=None, root=SOURCE_ROOT):
    return meter.read_records("claude", encoded(records),
                              config=cfg() if config is None else config,
                              source_root=root)


@pytest.fixture(autouse=True)
def passing_remote(monkeypatch):
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda project, excluded_roots, **kwargs: (REMOTE, None))


def test_record_in_project_folder_counts_as_proven():
    event, = read([rec()])["events"]
    assert event["project_alias"] == "alpha"
    assert event["project_association"] == "current_local_verified"
    assert event["ownership"] == "proven"
    assert "project_path_unapproved" not in event["reasons"]
    assert event["kinds"]["fresh_input"] == 10


def test_record_in_sub_folder_counts_as_proven():
    event, = read([rec(cwd=PROJECT + SEP + "sub")])["events"]
    assert event["project_alias"] == "alpha"
    assert event["ownership"] == "proven"


@pytest.mark.parametrize("cwd", [
    BASE + SEP + "elsewhere",
    PROJECT + "-old",
    PROJECT + SEP,
    PROJECT.upper(),
    PROJECT + SEP + ".." + SEP + "x",
    "project" + SEP + "sub",
    PROJECT + SEP + "sub\x01",
    PROJECT + SEP + SEP + "sub",
    "",
    PROJECT + SEP + "a" * 4100,
    MISSING,
], ids=["outside", "sibling-name", "trailing-separator", "other-letter-case",
        "dot-dot-part", "relative", "control-character", "empty-part",
        "empty-cwd", "over-4096-characters", "missing-cwd"])
def test_folder_that_is_not_inside_the_project_stays_unknown(cwd):
    record = rec()
    if cwd is MISSING:
        del record["cwd"]
    else:
        record["cwd"] = cwd
    event, = read([record])["events"]
    assert event["project_alias"] is None
    assert event["ownership"] == "unknown"
    assert "project_path_unapproved" in event["reasons"]
    assert event["kinds"]["fresh_input"] == 10


@pytest.mark.parametrize("cwd", [
    "C:/synthetic/p",
    "\\\\host\\share\\p",
    "C:\\synthetic\\p\\",
], ids=["forward-slashes", "unc-share", "trailing-backslash"])
def test_windows_forms_that_are_not_proof(monkeypatch, cwd):
    monkeypatch.setattr(meter, "os", SimpleNamespace(name="nt"))
    projects = [{"alias": "alpha", "path": "C:\\synthetic\\p", "remote": REMOTE}]
    assert meter._project_for_folder(cwd, projects) is None


def test_windows_sub_folder_is_proof(monkeypatch):
    monkeypatch.setattr(meter, "os", SimpleNamespace(name="nt"))
    projects = [{"alias": "alpha", "path": "C:\\synthetic\\p", "remote": REMOTE}]
    assert meter._project_for_folder("C:\\synthetic\\p\\sub", projects) is projects[0]


def test_folder_inside_two_projects_is_not_proof():
    config = cfg([PROJECT, PROJECT + SEP + "inner"])
    event, = read([rec(cwd=PROJECT + SEP + "inner" + SEP + "x")], config=config)["events"]
    assert event["project_alias"] is None
    assert event["ownership"] == "unknown"
    assert "project_path_unapproved" in event["reasons"]


def test_failed_remote_check_gives_its_reason(monkeypatch):
    monkeypatch.setattr(meter, "_verified_project_remote",
                        lambda project, excluded_roots, **kwargs: (None, "project_remote_mismatch"))
    event, = read([rec()])["events"]
    assert event["project_alias"] is None
    assert event["ownership"] == "unknown"
    assert "project_remote_mismatch" in event["reasons"]
    assert "project_path_unapproved" not in event["reasons"]


def test_unapproved_source_root_is_not_proof():
    event, = read([rec()], root=OTHER_ROOT)["events"]
    assert event["project_alias"] is None
    assert event["ownership"] == "unknown"
    assert "project_path_unapproved" in event["reasons"]


def test_record_without_request_id_is_not_proven():
    record = rec()
    del record["requestId"]
    event, = read([record])["events"]
    assert event["project_alias"] is None
    assert event["ownership"] == "unknown"
    assert "conflicting_binding" in event["reasons"]


def test_one_message_under_two_sessions_is_one_unknown_event():
    first = rec(sessionId="session-a")
    second = rec(sessionId="session-b")
    event, = read([first, second])["events"]
    assert event["ownership"] == "unknown"
    assert event["project_alias"] is None
    assert "conflicting_binding" in event["reasons"]


def test_same_message_twice_in_one_session_is_one_proven_event():
    event, = read([rec(), rec()])["events"]
    assert event["ownership"] == "proven"
    assert event["project_alias"] == "alpha"
    assert "conflicting_binding" not in event["reasons"]


@pytest.mark.parametrize("second_cwd", [OTHER_PROJECT, BASE + SEP + "elsewhere"],
                         ids=["other-project", "outside"])
def test_one_message_under_two_folders_is_one_unknown_event(second_cwd):
    config = cfg([PROJECT, OTHER_PROJECT])
    for records in ([rec(), rec(cwd=second_cwd)], [rec(cwd=second_cwd), rec()]):
        event, = read(records, config=config)["events"]
        assert event["ownership"] == "unknown"
        assert event["project_alias"] is None
        assert "conflicting_binding" in event["reasons"]


def test_repeats_with_differing_usage_are_conflicting_usage():
    changed = rec()
    changed["message"]["usage"]["output_tokens"] = 5
    event, = read([rec(), changed])["events"]
    assert event["kinds"] == meter._unknown_kinds()
    assert "conflicting_usage" in event["reasons"]


def test_repeats_with_equal_usage_merge_without_conflict():
    event, = read([rec(), rec()])["events"]
    assert event["kinds"]["output"] == 4
    assert "conflicting_usage" not in event["reasons"]


def test_same_records_read_under_two_roots_are_one_event():
    config = cfg(roots=(SOURCE_ROOT, OTHER_ROOT))
    first = read([rec()], config=config, root=SOURCE_ROOT)
    second = read([rec()], config=config, root=OTHER_ROOT)
    merged = meter._merge_event_batches([first, second])
    assert len(merged) == 1


def _claim(session_digest, *, released_at="2026-11-05T13:00:00Z"):
    return {"claim_key": "a" * 64, "project_alias": "alpha", "tool": "claude",
            "session_digest": session_digest, "claimed_at": "2026-11-05T11:00:00Z",
            "released_at": released_at, "confidence": "reliable",
            "targets": ["artifact-a"]}


def test_proven_event_joins_the_one_claim_that_covers_it():
    config = cfg()
    event, = read([rec()], config=config)["events"]
    mappings = meter._build_mappings([event], [_claim(event["session_digest"])], config)
    assert mappings == [{"event_key": event["event_key"], "claim_key": "a" * 64,
                         "artifact": "artifact-a", "confidence": "reliable"}]


def test_proven_event_without_a_covering_claim_stays_unmapped():
    config = cfg()
    event, = read([rec()], config=config)["events"]
    assert meter._build_mappings([event], [], config) == []
    open_claim = _claim(event["session_digest"], released_at=None)
    assert meter._build_mappings([event], [open_claim], config) == []


# Arc C2: summaries of finished sub-agents and transcripts, read at read time.

RUN = "a1b2c3d4e5f6g7h8i"
DIGEST = meter._digest("agent-id", RUN)
SESSION_KEY = meter._digest("claude", "session-a")
SUMMARY_ROW = {"session_key": SESSION_KEY, "agent_key": DIGEST}
VALID = {"totalTokens": 9, "toolUses": 2, "durationMs": 500}


def summary_record(**changes):
    """A summary-shaped record: the tool's frame around the run's id, and usage of the three counts."""
    record = {"type": "attachment", "timestamp": STAMP, "sessionId": "session-a",
              "text": "done <task-id>" + RUN + "</task-id>", "usage": dict(VALID)}
    record.update(changes)
    return record


def test_summary_is_not_usage_and_leaves_one_row():
    result = read([rec(), summary_record()])
    assert len(result["events"]) == 1
    assert "unsupported_record" not in result["issues"]
    assert "agent_runs_incomplete" not in result["issues"]
    assert result["agent_runs"]["summaries"] == [SUMMARY_ROW]


def test_user_record_with_summary_shape_is_skipped():
    result = read([rec(), summary_record(type="user")])
    assert result["issues"] == []
    assert result["agent_runs"] == meter._empty_agent_runs()


BAD_SHAPES = {
    "wrong-field-name": {"totalTokens": 9, "toolUses": 2, "duration": 500},
    "extra-field": dict(VALID, extra=1),
    "missing-field": {"totalTokens": 9, "toolUses": 2},
    "negative": dict(VALID, toolUses=-1),
    "boolean": dict(VALID, totalTokens=True),
    "fraction": dict(VALID, durationMs=1.5),
    "string-number": dict(VALID, totalTokens="3"),
    "usage-in-usage": {"usage": dict(VALID)},
    "usage-list": [dict(VALID)],
    "empty-usage": {},
}


@pytest.mark.parametrize("name", sorted(BAD_SHAPES))
def test_summary_shape_failure_is_incomplete_not_unsupported(name):
    result = read([summary_record(usage=BAD_SHAPES[name])])
    assert "agent_runs_incomplete" in result["issues"]
    assert "unsupported_record" not in result["issues"]
    assert result["agent_runs"]["unclassified"] == 1
    assert result["agent_runs"]["summaries"] == []


def test_one_good_and_one_bad_usage_in_one_record_is_incomplete():
    record = summary_record(other={"usage": dict(VALID, toolUses=-1)})
    result = read([record])
    assert "agent_runs_incomplete" in result["issues"]
    assert result["agent_runs"]["summaries"] == []


@pytest.mark.parametrize("name", ["user", "system", "progress", "file-history-snapshot"])
def test_skipped_types_stay_skipped_whatever_they_hold(name):
    result = read([rec(), {"type": name, "usage": dict(VALID)},
                   {"type": name, "usage": {"bad": 1}}])
    assert result["issues"] == []
    assert result["agent_runs"] == meter._empty_agent_runs()


def test_summary_without_session_is_incomplete():
    record = summary_record()
    del record["sessionId"]
    result = read([record])
    assert "agent_runs_incomplete" in result["issues"]
    assert result["agent_runs"]["unclassified"] == 1


@pytest.mark.parametrize("extra, expected", [
    ({"text": "<task-id>" + RUN + "</task-id>"}, DIGEST),
    ({"text": "done"}, ""),
    ({"text": "<task-id>" + RUN + "</task-id> then <task-id>" + RUN + "</task-id>"}, DIGEST),
    ({"text": "<task-id>" + RUN + "</task-id> <task-id>b1b2c3d4e5f6g7h8j</task-id>"}, ""),
    ({"text": "stray1234567890ab <task-id>" + RUN + "</task-id>"}, DIGEST),
    ({"text": "<task-id>" + "a" * 65 + "</task-id>"}, ""),
    ({"<task-id>" + RUN + "</task-id>": "x"}, ""),
    ({"a": "<task-id>" + RUN, "b": "</task-id>"}, ""),
    ({"text": "<TASK-ID>" + RUN + "</TASK-ID>"}, ""),
    ({"text": "<task-id>a1b2c3d</task-id>"}, ""),
], ids=["one-frame", "no-frame", "same-frame-twice", "two-ids",
        "stray-word-beside-frame", "frame-with-65-characters", "frame-only-in-key",
        "frame-split-across-strings", "upper-case-tag", "seven-characters"])
def test_summary_run_reads_only_the_frame(extra, expected):
    record = {"type": "attachment", "usage": dict(VALID), **extra}
    assert meter._summary_run(record) == expected


def test_transcript_record_registers_one_pair():
    result = read([rec(isSidechain=True, agentId=RUN)])
    assert result["agent_runs"]["transcripts"] == [SUMMARY_ROW]
    assert len(result["events"]) == 1


def test_transcript_mark_needs_true_and_a_text_agent_id():
    no_mark = read([rec(agentId=RUN)])
    assert no_mark["agent_runs"]["transcripts"] == []
    bad_id = read([rec(isSidechain=True, agentId=5)])
    assert bad_id["agent_runs"]["transcripts"] == []
    assert len(bad_id["events"]) == 1
