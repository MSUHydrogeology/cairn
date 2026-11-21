"""The Bandit pass reads an optional adopter-set threshold (arc C4, issue #101).

Permanent cases from Detail D7, driven through `run_bandit_pass`. Stubbed
cases replace `_run_tool` with hand-written JSON and record the argv. The
real-Bandit case runs only where Bandit is installed.
"""

import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path

import pytest

from tests._repo_root import repository_root

CAIRN_ROOT = repository_root(Path(__file__))
_ORCH_SRC = CAIRN_ROOT / "templates" / "modules" / "team-gated" / "run_security_audit.py"

_HAS_BANDIT = (shutil.which("bandit") is not None
               or importlib.util.find_spec("bandit") is not None)

SCHEMA = "cairn-python-security-policy/1"
POLICY_REL = Path("dev") / ".cairn" / "python-security.json"
PREFIX = ("the python-security policy file dev/.cairn/python-security.json "
          "cannot be used: ")
SUFFIX = " Fix the file, or delete it to restore the default (any finding fails). The audit will not pick a threshold for you."


@pytest.fixture(scope="module")
def orch():
    spec = importlib.util.spec_from_file_location("run_security_audit_threshold", _ORCH_SRC)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "python_package").mkdir()
    (tmp_path / "dev" / ".cairn").mkdir(parents=True)
    return tmp_path


@pytest.fixture
def bandit_present(orch, monkeypatch):
    monkeypatch.setattr(orch.shutil, "which", lambda _n: "/usr/bin/bandit")


def write_policy(repo, body):
    text = body if isinstance(body, str) else json.dumps(body)
    (repo / POLICY_REL).write_text(text, encoding="utf-8")


def policy(min_severity="low", min_confidence="low"):
    return {"schema": SCHEMA, "min_severity": min_severity,
            "min_confidence": min_confidence}


def bandit_json(*findings):
    return json.dumps({"results": [
        {"issue_severity": sev, "issue_confidence": conf, "test_id": "B101"}
        for sev, conf in findings]})


def stub_tool(monkeypatch, orch, code, stdout="", status="ran"):
    """Replace `_run_tool` with a fixed answer; return the list of argvs seen."""
    seen = []

    def fake(argv, **kwargs):
        seen.append(argv)
        return orch.ToolRun(code, status, stdout, "")
    monkeypatch.setattr(orch, "_run_tool", fake)
    return seen


def first_bandit_line(capsys):
    out = capsys.readouterr().out
    return next(line for line in out.splitlines() if line.startswith("[bandit]"))


# Declared exception (internal hook): Hook: _run_tool stub with hand-written JSON; the stub records argv. Bandit presence is faked through shutil.which.
def test_no_file_keeps_today_argv_and_verdict(orch, repo, bandit_present,
                                              monkeypatch, capsys):
    seen = stub_tool(monkeypatch, orch, 0)
    status, tier = orch.run_bandit_pass(repo / "python_package", repo)
    assert status == "bandit:clean" and tier == orch._AGG_CLEAN
    argv = seen[0]
    assert "-q" in argv and "json" not in argv
    assert first_bandit_line(capsys) == (
        "[bandit] threshold in force: any finding fails (default; no "
        "dev/.cairn/python-security.json).")


# Declared exception (internal hook): Hook: _run_tool stub with hand-written JSON; the stub records argv.
def test_no_file_one_low_finding_still_fails(orch, repo, bandit_present, monkeypatch):
    stub_tool(monkeypatch, orch, 1)
    status, tier = orch.run_bandit_pass(repo / "python_package", repo)
    assert status == "bandit:findings" and tier == orch._AGG_FINDINGS


# Declared exception (internal hook): Hook: _run_tool stub; a file that sets both minimums to low changes nothing.
def test_file_with_both_minimums_low_changes_nothing(orch, repo, bandit_present,
                                                     monkeypatch, capsys):
    write_policy(repo, policy("low", "low"))
    seen = stub_tool(monkeypatch, orch, 1, bandit_json(("LOW", "LOW")))
    status, tier = orch.run_bandit_pass(repo / "python_package", repo)
    assert status == "bandit:findings" and tier == orch._AGG_FINDINGS
    assert "json" not in seen[0]
    assert first_bandit_line(capsys) == (
        "[bandit] threshold in force: severity at least low and confidence "
        "at least low, set in dev/.cairn/python-security.json. A finding below "
        "it is printed but does not fail the audit.")


# Declared exception (internal hook): Hook: _run_tool stub with hand-written JSON; the stub records argv.
def test_medium_low_one_low_and_one_medium_fails_with_count_one(
        orch, repo, bandit_present, monkeypatch, capsys):
    write_policy(repo, policy("medium", "low"))
    seen = stub_tool(monkeypatch, orch, 1,
                     bandit_json(("LOW", "LOW"), ("MEDIUM", "LOW")))
    status, tier = orch.run_bandit_pass(repo / "python_package", repo)
    assert status == "bandit:findings [threshold: severity>=medium, confidence>=low]"
    assert tier == orch._AGG_FINDINGS
    assert "-f" in seen[0] and "json" in seen[0]
    out = capsys.readouterr().out
    assert ("[bandit] 1 finding(s) at or above the threshold (these fail the "
            "audit); 1 below it (printed above; they do not fail the audit).") in out


# Declared exception (internal hook): Hook: _run_tool stub with hand-written JSON.
def test_high_low_passes_below_threshold_and_carries_suffix(
        orch, repo, bandit_present, monkeypatch, capsys):
    write_policy(repo, policy("high", "low"))
    stub_tool(monkeypatch, orch, 1, bandit_json(("LOW", "LOW"), ("MEDIUM", "LOW")))
    status, tier = orch.run_bandit_pass(repo / "python_package", repo)
    assert status == ("bandit:clean-below-threshold "
                      "[threshold: severity>=high, confidence>=low]")
    assert tier == orch._AGG_CLEAN
    assert first_bandit_line(capsys) == (
        "[bandit] threshold in force: severity at least high and confidence "
        "at least low, set in dev/.cairn/python-security.json. A finding below "
        "it is printed but does not fail the audit.")


# Declared exception (internal hook): Hook: _run_tool stub with hand-written JSON.
def test_medium_high_needs_both_levels(orch, repo, bandit_present, monkeypatch):
    write_policy(repo, policy("medium", "high"))
    stub_tool(monkeypatch, orch, 1, bandit_json(("MEDIUM", "LOW")))
    status, tier = orch.run_bandit_pass(repo / "python_package", repo)
    assert status == ("bandit:clean-below-threshold "
                      "[threshold: severity>=medium, confidence>=high]")
    assert tier == orch._AGG_CLEAN
    stub_tool(monkeypatch, orch, 1, bandit_json(("MEDIUM", "HIGH")))
    status, tier = orch.run_bandit_pass(repo / "python_package", repo)
    assert status == "bandit:findings [threshold: severity>=medium, confidence>=high]"
    assert tier == orch._AGG_FINDINGS


# Declared exception (internal hook): Hook: _run_tool stub with hand-written JSON.
def test_undefined_severity_fails(orch, repo, bandit_present, monkeypatch):
    write_policy(repo, policy("medium", "low"))
    stub_tool(monkeypatch, orch, 1, bandit_json(("UNDEFINED", "LOW")))
    status, tier = orch.run_bandit_pass(repo / "python_package", repo)
    assert status.startswith("bandit:findings") and tier == orch._AGG_FINDINGS


@pytest.mark.parametrize("body", [
    {"schema": "other/1"},
    {"min_severity": "high"},
    {"schema": SCHEMA, "min_colour": "low"},
    {"schema": SCHEMA, "min_severity": "HIGH"},
    {"schema": SCHEMA, "min_severity": ["high"]},
    '{"schema": "%s", "min_severity": "high", "min_severity": "low"}' % SCHEMA,
    '["not", "an", "object"]',
    '{',
    '{"schema": "%s", "pad": "%s"}' % (SCHEMA, "x" * 4100),
], ids=["wrong-schema", "no-schema", "unknown-key", "uppercase-level",
        "list-level", "repeated-key", "not-object", "not-json", "too-large"])
def test_bad_policy_file_degrades(orch, repo, bandit_present, body):
    write_policy(repo, body)
    with pytest.raises(orch.AuditDegraded) as info:
        orch.run_bandit_pass(repo / "python_package", repo)
    assert str(info.value).startswith(PREFIX)
    assert str(info.value).endswith(SUFFIX)


def test_policy_that_is_a_folder_degrades(orch, repo, bandit_present):
    (repo / POLICY_REL).mkdir()
    with pytest.raises(orch.AuditDegraded, match="it is not a regular file"):
        orch.run_bandit_pass(repo / "python_package", repo)


def test_policy_that_is_a_link_degrades(orch, repo, bandit_present):
    target = repo / "elsewhere.json"
    write_policy(repo, policy())
    target.write_text(json.dumps(policy()), encoding="utf-8")
    (repo / POLICY_REL).unlink()
    try:
        os.symlink(target, repo / POLICY_REL)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"cannot create a symbolic link here: {exc}")
    with pytest.raises(orch.AuditDegraded, match="it is not a regular file"):
        orch.run_bandit_pass(repo / "python_package", repo)


# Declared exception (internal hook): Hook: _run_tool stub with hand-written output.
@pytest.mark.parametrize("code, stdout, status, expected", [
    (1, "[" * 4000, "ran", "bandit:unparseable"),
    (1, "[]", "ran", "bandit:unparseable"),
    (0, bandit_json(("LOW", "LOW")), "ran", "bandit:inconsistent"),
    (1, json.dumps({"results": []}), "ran", "bandit:inconsistent"),
    (2, "", "ran", "bandit:error"),
    (0, "", "timeout", "bandit:timeout"),
], ids=["deep-output", "not-object", "code0-with-finding",
        "code1-without-finding", "code2", "timeout"])
def test_unusable_output_is_degraded_without_suffix(
        orch, repo, bandit_present, monkeypatch, code, stdout, status, expected):
    write_policy(repo, policy("medium", "low"))
    stub_tool(monkeypatch, orch, code, stdout, status)
    got, tier = orch.run_bandit_pass(repo / "python_package", repo)
    assert got == expected
    assert tier == orch._AGG_DEGRADED


@pytest.mark.skipif(not _HAS_BANDIT, reason="Bandit is not installed here")
def test_real_bandit_passes_under_high_and_fails_by_default(orch, tmp_path):
    package = tmp_path / "python_package"
    package.mkdir()
    (package / "check.py").write_text("assert 1 == 1\n", encoding="utf-8")
    (tmp_path / "dev" / ".cairn").mkdir(parents=True)
    status, tier = orch.run_bandit_pass(package, tmp_path)
    assert tier == orch._AGG_FINDINGS
    write_policy(tmp_path, policy("high", "low"))
    status, tier = orch.run_bandit_pass(package, tmp_path)
    assert tier == orch._AGG_CLEAN
