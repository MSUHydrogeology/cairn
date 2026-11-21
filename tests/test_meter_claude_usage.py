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
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from tests._repo_root import repository_root

ROOT = repository_root(Path(__file__))
METER = ROOT / "dev/tools/meter.py"
spec = importlib.util.spec_from_file_location("meter_claude_usage_reader", METER)
meter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meter)
pulse_spec = importlib.util.spec_from_file_location("pulse_claude_usage", ROOT / "dev/tools/pulse.py")
pulse = importlib.util.module_from_spec(pulse_spec)
pulse_spec.loader.exec_module(pulse)

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


# Arc C3: the ledger remembers sub-agent runs across refreshes, and sets the reason.

NOW = datetime(2026, 11, 5, tzinfo=timezone.utc)
OTHER_SESSION_KEY = meter._digest("claude", "session-b")
SIBLING = meter._digest("agent-id", "b1b2c3d4e5f6g7h8j")
PAIR = (SESSION_KEY, DIGEST)
SIBLING_PAIR = (SESSION_KEY, SIBLING)
OTHER_PAIR = (OTHER_SESSION_KEY, DIGEST)


def runs(transcripts=(), summaries=(), unclassified=0):
    """The sets one refresh gathers from its batches (Detail D4)."""
    return {"transcripts": set(transcripts), "summaries": set(summaries),
            "unclassified": unclassified}


def new_ledger(prior, gathered, *, remotes=()):
    """One refresh's ledger from its sub-agent sets, with no events, claims or cursors."""
    return meter._new_ledger(prior, cfg(), [], [], [], [], list(remotes), [], set(),
                             [], [], now=NOW, agent_runs=gathered)


def reasons_of(ledger):
    return ledger["coverage"]["reasons"]


@pytest.fixture
def start_ledger():
    return meter._load_ledger(None)


def test_summary_then_its_transcript_clears_the_reason(start_ledger):
    first = new_ledger(start_ledger, runs(summaries=[PAIR]))
    assert "agent_runs_incomplete" in reasons_of(first)
    second = new_ledger(first, runs(transcripts=[PAIR]))
    assert "agent_runs_incomplete" not in reasons_of(second)
    assert second["agent_runs"]["summaries"] == []
    assert second["agent_runs"]["transcripts"] == [SUMMARY_ROW]


@pytest.mark.parametrize("gathered, incomplete", [
    (runs(summaries=[PAIR]), True),
    (runs(summaries=[PAIR], transcripts=[PAIR]), False),
    (runs(unclassified=1), True),
    (runs(summaries=[PAIR], transcripts=[SIBLING_PAIR]), True),
    (runs(summaries=[PAIR], transcripts=[OTHER_PAIR]), True),
], ids=["own-run-not-read", "own-run-read", "no-frame-or-two-ids",
        "sibling-read-but-own-run-not", "run-read-in-another-session"])
def test_summary_frames_decide_covered_or_incomplete(start_ledger, gathered, incomplete):
    ledger = new_ledger(start_ledger, gathered)
    assert ("agent_runs_incomplete" in reasons_of(ledger)) is incomplete


def test_a_run_summarised_twice_is_covered_by_its_one_transcript(start_ledger):
    first = new_ledger(start_ledger, runs(summaries=[PAIR]))
    second = new_ledger(first, runs(summaries=[PAIR]))
    third = new_ledger(second, runs(transcripts=[PAIR]))
    assert "agent_runs_incomplete" not in reasons_of(third)
    assert third["agent_runs"]["summaries"] == []


def test_an_unclassified_record_keeps_the_reason_until_the_ledger_is_replaced(start_ledger):
    first = new_ledger(start_ledger, runs(unclassified=1))
    second = new_ledger(first, runs())
    assert "agent_runs_incomplete" in reasons_of(second)
    assert second["agent_runs"]["unclassified"] == 1


def test_caps_cut_the_excess_and_count_it_without_failing(monkeypatch, start_ledger):
    monkeypatch.setattr(meter, "MAX_AGENT_SUMMARIES", 3)
    summaries = [(SESSION_KEY, meter._digest("agent-id", "run-%d" % index))
                 for index in range(4)]
    ledger = new_ledger(start_ledger, runs(summaries=summaries))
    assert len(ledger["agent_runs"]["summaries"]) == 3
    assert ledger["agent_runs"]["unclassified"] == 1
    assert "agent_runs_incomplete" in reasons_of(ledger)


def run_ledger():
    return new_ledger(meter._load_ledger(None), runs(
        transcripts=[PAIR, SIBLING_PAIR], summaries=[OTHER_PAIR], unclassified=2))


def ledger_bytes(ledger):
    return json.dumps(ledger, sort_keys=True).encode("utf-8")


def test_the_ledger_round_trips_its_run_record():
    ledger = run_ledger()
    assert meter._load_ledger(ledger_bytes(ledger), NOW) == ledger


EDITS = {
    "unsorted-rows": lambda record: record["transcripts"].reverse(),
    "duplicate-row": lambda record: record["transcripts"].__setitem__(
        1, dict(record["transcripts"][0])),
    "key-not-hex": lambda record: record["transcripts"][0].__setitem__(
        "session_key", "X" * 64),
    "missing-agent-key": lambda record: record["transcripts"][0].pop("agent_key"),
    "negative-count": lambda record: record.__setitem__("unclassified", -1),
    "extra-key": lambda record: record.__setitem__("extra", 1),
}


@pytest.mark.parametrize("name", sorted(EDITS))
def test_a_hand_edit_of_the_run_record_is_refused(name):
    raw = json.loads(ledger_bytes(run_ledger()))
    EDITS[name](raw["agent_runs"])
    with pytest.raises(meter.Unavailable) as refused:
        meter._load_ledger(json.dumps(raw).encode("utf-8"), NOW)
    assert refused.value.reason == "ledger_invalid"


def test_the_empty_ledger_starts_with_no_runs():
    assert meter._load_ledger(None)["agent_runs"] == meter._empty_agent_runs()


def test_the_export_reaches_the_pulse_as_an_incomplete_reason():
    ledger = new_ledger(meter._load_ledger(None), runs(summaries=[PAIR]),
                        remotes=[{"alias": "alpha", "remote": REMOTE}])
    data = meter._project_export_bytes(ledger, cfg(), "alpha")
    assert "agent_runs_incomplete" in pulse._parse_meter_aggregate(data)["incomplete_reasons"]
