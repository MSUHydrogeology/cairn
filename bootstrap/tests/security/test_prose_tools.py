"""CLI contracts for the prose report and exact replacer."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
TEMPLATE = ROOT / "templates" / "modules" / "team-gated"
GIT_HELPER = ROOT / "tools" / "git_read.py"
GIT_SHA = hashlib.sha256(GIT_HELPER.read_bytes()).hexdigest()


def _git(path: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=path, check=True,
                          stdout=subprocess.PIPE, text=True).stdout.strip()


def _repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "--initial-branch=main")
    _git(repo, "config", "user.email", "cairn-test@example.invalid")
    _git(repo, "config", "user.name", "Cairn test")
    scripts, tools = repo / "scripts", repo / "tools"
    scripts.mkdir(); tools.mkdir()
    for name in ("prose_diff.py", "exact_replace.py", "prose_roots.txt"):
        shutil.copyfile(TEMPLATE / name, scripts / name)
    source_tools = repo / "templates" / "modules" / "team-gated"
    source_tools.mkdir(parents=True)
    for name in ("prose_diff.py", "exact_replace.py", "prose_roots.txt"):
        shutil.copyfile(TEMPLATE / name, source_tools / name)
    source_helper = repo / "templates" / "skills" / "_lib"
    source_helper.mkdir(parents=True)
    shutil.copyfile(GIT_HELPER, source_helper / "git_read.py")
    shutil.copyfile(GIT_HELPER, tools / "git_read.py")
    (scripts / "content_scan_roots.txt").write_text(
        "# content-scan-roots v1\n!AGENTS.md\n", encoding="utf-8")
    (repo / "AGENTS.md").write_text(
        "Keep every tool output bounded. This protects the user.\n", encoding="utf-8")
    (repo / "dev" / ".cairn").mkdir(parents=True)
    (repo / "dev" / ".cairn" / "cairn-lock.yml").write_text(
        "# generated fixture\n" + json.dumps({"files": [
            {"dst": "tools/git_read.py", "verbatim": True, "hash": GIT_SHA},
            {"dst": "scripts/prose_diff.py", "verbatim": True,
             "hash": hashlib.sha256((scripts / "prose_diff.py").read_bytes()).hexdigest()},
        ]}), encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "fixture base")
    return repo, _git(repo, "rev-parse", "HEAD")


def _run(repo: Path, script: str, *args: str, timeout: float = 20) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(repo / "scripts" / script), *args],
                          cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, timeout=timeout)


def test_report_cli_uses_committed_base_roots_and_shows_rule_change(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    (repo / "AGENTS.md").write_text("Keep every tool output available.\n", encoding="utf-8")
    _git(repo, "add", "AGENTS.md"); _git(repo, "commit", "-m", "change rule")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 0, result.stderr
    assert "CHANGED AGENTS.md" in result.stdout
    assert "bounded" in result.stdout and "available" in result.stdout


def test_report_cli_refuses_a_substituted_git_helper(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    helper = repo / "tools" / "git_read.py"
    helper.write_text("raise RuntimeError('must not execute')\n", encoding="utf-8")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 2
    assert "INCOMPLETE" in result.stderr


def test_replacer_refuses_a_substituted_report_before_writing(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    before = target.read_bytes()
    marker = tmp_path / "executed"
    report = repo / "scripts" / "prose_diff.py"
    report.write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('executed')\n", encoding="utf-8")
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")
    result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old),
                  "--new-file", str(new))
    assert result.returncode == 2
    assert target.read_bytes() == before
    assert not marker.exists()


def test_replacer_refuses_an_oversized_report_binding_before_writing(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    before = target.read_bytes()
    report = repo / "scripts" / "prose_diff.py"
    report.write_bytes(b"#" + b"x" * (256 * 1024))
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")
    result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old),
                  "--new-file", str(new))
    assert result.returncode == 2
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


def test_template_source_cli_uses_its_fixed_helper_layout(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    (repo / "AGENTS.md").write_text("Keep all tool output bounded. This protects the user.\n", encoding="utf-8")
    _git(repo, "add", "AGENTS.md"); _git(repo, "commit", "-m", "change rule")
    script = repo / "templates" / "modules" / "team-gated" / "prose_diff.py"
    result = subprocess.run([sys.executable, str(script), base, "HEAD"], cwd=repo,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, timeout=20)
    assert result.returncode == 0, result.stderr
    assert "CHANGED AGENTS.md" in result.stdout


def test_exact_replacer_preserves_raw_crlf_and_reports_the_edit(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    old, new = tmp_path / "old.bin", tmp_path / "new.bin"
    old.write_bytes(b"bounded.\r\n")
    new.write_bytes(b"available.\r\n")
    (repo / "AGENTS.md").write_bytes(
        b"Keep every tool output bounded.\r\nThis protects the user.\r\n")
    result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old),
                  "--new-file", str(new))
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert (repo / "AGENTS.md").read_bytes() == b"Keep every tool output available.\r\nThis protects the user.\r\n"
    assert "CHANGED AGENTS.md" in result.stdout
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


def test_overlapping_match_failure_and_batch_failure_leave_target_unchanged(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    target.write_bytes(b"ababa\n")
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"aba"); new.write_bytes(b"x")
    before = target.read_bytes()
    result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old), "--new-file", str(new))
    assert result.returncode == 1 and "match count 2" in result.stdout
    assert target.read_bytes() == before
    target.write_bytes(b"ab\nother\n")
    before = target.read_bytes()
    batch = tmp_path / "batch.json"
    batch.write_text(json.dumps([{"old": "ab", "new": "xy"}, {"old": "missing", "new": "q"}]), encoding="utf-8")
    result = _run(repo, "exact_replace.py", "AGENTS.md", "--batch", str(batch))
    assert result.returncode == 1
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


def test_replacer_rejects_link_and_retained_open_stdin_times_out(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")
    link = repo / "linked.md"
    try:
        link.symlink_to(repo / "AGENTS.md")
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable")
    before = (repo / "AGENTS.md").read_bytes()
    linked = _run(repo, "exact_replace.py", "linked.md", "--old-file", str(old), "--new-file", str(new))
    assert linked.returncode == 2
    assert (repo / "AGENTS.md").read_bytes() == before

    # A separate copy shortens only the internal deadline so this real CLI
    # subprocess exercises an input pipe deliberately kept open by its parent.
    script = repo / "scripts" / "exact_replace.py"
    script.write_text(script.read_text(encoding="utf-8").replace(
        "_DEADLINE_SECONDS = 120.0", "_DEADLINE_SECONDS = 0.4"), encoding="utf-8")
    proc = subprocess.Popen([sys.executable, str(script), "AGENTS.md", "--old-file", "-",
                             "--new-file", str(new)], cwd=repo, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        proc.wait(timeout=4)
    except subprocess.TimeoutExpired:
        proc.kill(); proc.communicate(); pytest.fail("retained-open stdin blocked the CLI")
    out = proc.stdout.read(); err = proc.stderr.read()
    proc.stdin.close()
    assert proc.returncode == 2, (out, err)
    assert (repo / "AGENTS.md").read_bytes() == before

