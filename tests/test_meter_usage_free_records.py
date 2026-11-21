"""Usage-free Claude records are not 'unsupported'; usage-bearing ones still are.

Arc C3, issue #96. Every record here is written by hand from the shapes in
Detail D6. No assistant log is read. The reader is driven through
`meter.read_records`, the public entry point the criterion names.
"""

import importlib.util
import json
from pathlib import Path

import pytest

from tests._repo_root import repository_root

ROOT = repository_root(Path(__file__))
METER = ROOT / "dev/tools/meter.py"
spec = importlib.util.spec_from_file_location("meter_usage_free_reader", METER)
meter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meter)

STAMP = "2026-11-05T12:00:00Z"


def encoded(records):
    return [(json.dumps(record) + "\n").encode() for record in records]


def assistant_record():
    """Shaped like the `claude()` fixture in tests/integration/test_meter.py."""
    return {"type": "assistant", "timestamp": STAMP, "sessionId": "session-a",
            "requestId": "request-a", "cwd": "/synthetic/not-proof",
            "message": {"id": "message-a", "model": "synthetic-model",
                        "content": "SECRET-BODY", "usage": {
                            "input_tokens": 10, "output_tokens": 4,
                            "cache_creation_input_tokens": 2,
                            "cache_read_input_tokens": 8}}}


def read_claude(extra_record):
    return meter.read_records("claude", encoded([assistant_record(), extra_record]))


@pytest.mark.parametrize("record", [
    {"type": "queue-operation"},
    {"type": "attachment"},
    {"type": "api-request"},
    {"type": "last-prompt"},
    {"type": "future-record-type"},
    {"sessionId": "session-a"},
], ids=["queue-operation", "attachment", "api-request", "last-prompt",
        "future-record-type", "no-type-key"])
def test_usage_free_record_is_skipped_silently(record):
    result = read_claude(record)
    assert result["issues"] == []
    assert len(result["events"]) == 1


@pytest.mark.parametrize("record", [
    {"type": "future-record-type", "message": {"usage": {}}},
    {"type": "future-record-type", "usage": {}},
    {"type": "future-record-type", "data": {"message": {"message": {"usage": {}}}}},
], ids=["usage-under-message", "usage-at-top", "usage-nested-deep"])
def test_unknown_record_type_with_usage_is_unsupported(record):
    result = read_claude(record)
    assert "unsupported_record" in result["issues"]


def test_assistant_with_bad_usage_is_invalid_record():
    record = assistant_record()
    record["message"]["usage"]["output_tokens"] = -1
    result = meter.read_records("claude", encoded([record]))
    assert "invalid_record" in result["issues"]
    event, = result["events"]
    assert event["kinds"] == meter._unknown_kinds()


@pytest.mark.parametrize("name", ["user", "system", "progress", "file-history-snapshot"])
def test_existing_record_names_are_skipped(name):
    result = read_claude({"type": name})
    assert result["issues"] == []
    assert len(result["events"]) == 1
