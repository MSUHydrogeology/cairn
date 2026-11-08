"""CLI contracts for the prose report and exact replacer."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
import types
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


def _entrypoint(repo: Path, script: str, layout: str) -> Path:
    if layout == "source":
        return repo / "templates" / "modules" / "team-gated" / script
    return repo / "scripts" / script


def _run_layout(repo: Path, script: str, layout: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(_entrypoint(repo, script, layout)), *args],
                          cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, timeout=20)


def _load_entrypoint(path: Path) -> types.ModuleType:
    name = "_cairn_prose_binding_test_" + str(abs(hash(path)))
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _replace_report_lock_hash(repo: Path, digest: str) -> None:
    lock_path = repo / "dev" / ".cairn" / "cairn-lock.yml"
    lock = json.loads(lock_path.read_text(encoding="utf-8").split("\n", 1)[1])
    matches = [row for row in lock["files"] if row.get("dst") == "scripts/prose_diff.py"]
    assert len(matches) == 1
    matches[0]["hash"] = digest
    lock_path.write_text("# fixture\n" + json.dumps(lock), encoding="utf-8")


def test_report_cli_uses_committed_base_roots_and_shows_rule_change(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    (repo / "AGENTS.md").write_text("Keep every tool output available.\n", encoding="utf-8")
    _git(repo, "add", "AGENTS.md"); _git(repo, "commit", "-m", "change rule")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 0, result.stderr
    assert "CHANGED AGENTS.md" in result.stdout
    assert "bounded" in result.stdout and "available" in result.stdout


def test_report_uses_base_roots_and_places_list_notice_first(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    manifest = repo / "scripts" / "prose_roots.txt"
    manifest.write_text("# prose-roots v1\nnew.md\n", encoding="utf-8")
    (repo / "new.md").write_text("Newly listed prose must not enter this base report.\n", encoding="utf-8")
    (repo / "AGENTS.md").write_text("Keep every tool output available.\n", encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt", "new.md", "AGENTS.md")
    _git(repo, "commit", "-m", "change roots and rule")

    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[0].startswith("NOTICE first: scripts/prose_roots.txt")
    assert "CHANGED AGENTS.md" in result.stdout
    assert "new.md" not in result.stdout


def test_report_refuses_a_negated_prose_root_in_base_manifest(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    manifest = repo / "scripts" / "prose_roots.txt"
    manifest.write_text("# prose-roots v1\n!AGENTS.md\n", encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt"); _git(repo, "commit", "-m", "invalid prose roots")
    result = _run(repo, "prose_diff.py", "HEAD", "HEAD")
    assert result.returncode == 2
    assert "negated prose root is invalid" in result.stderr


def test_report_shows_bounded_raw_evidence_for_yaml_svg_and_python_gaps(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    roots = repo / "scripts" / "prose_roots.txt"
    roots.write_text("# prose-roots v1\nrules.yml\nasset.svg\nchecks.py\n", encoding="utf-8")
    (repo / "rules.yml").write_text("checks:\n  allowed: true\n", encoding="utf-8")
    (repo / "asset.svg").write_text("<svg><title>Old rule</title></svg>\n", encoding="utf-8")
    (repo / "checks.py").write_text(
        '# Never remove this guard.\nSHORT = "Never push."\n', encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt", "rules.yml", "asset.svg", "checks.py")
    _git(repo, "commit", "-m", "add raw evidence fixtures")
    base = _git(repo, "rev-parse", "HEAD")
    (repo / "rules.yml").write_text(
        "checks:\n  allowed: true\n  forbidden: true" + chr(0x202E) + "\n", encoding="utf-8")
    (repo / "asset.svg").write_text("<svg><title></title></svg>\n", encoding="utf-8")
    (repo / "checks.py").write_text(
        '# Guard is removed.\nSHORT = "Always push."\n', encoding="utf-8")
    _git(repo, "add", "rules.yml", "asset.svg", "checks.py")
    _git(repo, "commit", "-m", "change raw evidence fixtures")

    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 0, result.stderr
    assert "NOT COMPARED rules.yml: unsupported suffix '.yml'; structured prose extraction unavailable" in result.stdout
    assert 'RAW ADDED rules.yml [before lines 3, after lines 3]' in result.stdout
    assert 'after="  forbidden: true\\u202e\\n"' in result.stdout
    assert "NOT COMPARED asset.svg: unsupported suffix '.svg'; structured prose extraction unavailable" in result.stdout
    assert 'RAW REMOVED asset.svg [before lines 1, after lines 1]' in result.stdout
    assert 'before="Old rule" ; after=""' in result.stdout
    assert 'RAW CHANGED checks.py [before lines 1-2, after lines 1-2]' in result.stdout
    assert "Guard is removed." in result.stdout
    assert "GAPS checks.py: 2 short Python string constants skipped" in result.stdout


def test_report_marks_raw_span_cap_and_invalid_utf8_incomplete(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    roots = repo / "scripts" / "prose_roots.txt"
    roots.write_text("# prose-roots v1\nlarge.yml\ninvalid.svg\n", encoding="utf-8")
    (repo / "large.yml").write_text("x" * 65537, encoding="utf-8")
    (repo / "invalid.svg").write_bytes(b"<svg>valid</svg>\n")
    _git(repo, "add", "scripts/prose_roots.txt", "large.yml", "invalid.svg")
    _git(repo, "commit", "-m", "add incomplete raw fixtures")
    base = _git(repo, "rev-parse", "HEAD")
    (repo / "large.yml").write_text("y" * 65537, encoding="utf-8")
    (repo / "invalid.svg").write_bytes(b"<svg>\xff</svg>\n")
    _git(repo, "add", "large.yml", "invalid.svg"); _git(repo, "commit", "-m", "break raw evidence")

    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 2, result.stderr
    assert "RAW EVIDENCE INCOMPLETE large.yml: differing span exceeds 64 KiB per side" in result.stdout
    assert "RAW EVIDENCE INCOMPLETE invalid.svg: blob is not valid UTF-8" in result.stdout


def test_exact_replacer_uses_raw_report_for_unsupported_target(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    roots = repo / "scripts" / "prose_roots.txt"
    roots.write_text("# prose-roots v1\nrules.yml\n", encoding="utf-8")
    target = repo / "rules.yml"
    target.write_text("guard: forbidden\n", encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt", "rules.yml")
    _git(repo, "commit", "-m", "install unsupported target fixture")
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_text("forbidden", encoding="utf-8"); new.write_text("allowed", encoding="utf-8")
    result = _run(repo, "exact_replace.py", "rules.yml", "--old-file", str(old), "--new-file", str(new))
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert target.read_text(encoding="utf-8") == "guard: allowed\n"
    assert "NOT COMPARED rules.yml: unsupported suffix '.yml'; structured prose extraction unavailable" in result.stdout
    assert 'RAW CHANGED rules.yml' in result.stdout and 'before="forbidden" ; after="allowed"' in result.stdout


def test_report_counts_short_python_strings_and_compares_long_constants_once(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    roots = repo / "scripts" / "prose_roots.txt"
    roots.write_text("# prose-roots v1\nrules.py\n", encoding="utf-8")
    source = repo / "rules.py"
    source.write_text(
        '"""This docstring has six words at least."""\n'
        'SHORT = "Never push."\n'
        'JOINED = ("This constant has six words "\n'
        '          "when the literals join.")\n'
        'FSTRING = f"Never push now {value}"\n', encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt", "rules.py")
    _git(repo, "commit", "-m", "add Python prose fixture")
    old = _git(repo, "rev-parse", "HEAD")
    source.write_text(
        '"""This docstring now has six words at least."""\n'
        'SHORT = "Always push."\n'
        'JOINED = ("This constant now has six words "\n'
        '          "when the literals join.")\n'
        'FSTRING = f"Always push now {value}"\n', encoding="utf-8")
    _git(repo, "add", "rules.py"); _git(repo, "commit", "-m", "change Python prose")
    result = _run(repo, "prose_diff.py", old, "HEAD")
    assert result.returncode == 0, result.stderr
    assert "CHANGED rules.py" in result.stdout
    assert "docstring now" in result.stdout
    assert "constant now" in result.stdout
    assert "GAPS rules.py: 4 short Python string constants skipped" in result.stdout


def test_cairn_roots_cover_template_directory_and_direct_python_files(tmp_path: Path) -> None:
    expected = {
        "templates", "dimensions", "bootstrap", "README.md", "on-ramp",
        "scripts/reanchor_ceremony.py", "scripts/repin.py",
        "bootstrap/tests/_gate_preflight.py", "bootstrap/tests/conftest.py",
    }
    cairn_roots = ROOT / "scripts" / "prose_roots.txt"
    shipped_roots = TEMPLATE / "prose_roots.txt"
    lines = [line for line in cairn_roots.read_text(encoding="utf-8").splitlines()
             if line and not line.startswith("#")]
    assert expected <= set(lines)
    assert shipped_roots.read_text(encoding="utf-8") == "# prose-roots v1\n"

    repo, _base = _repo(tmp_path)
    scripts_roots = repo / "scripts" / "prose_roots.txt"
    scripts_roots.write_bytes(cairn_roots.read_bytes())
    template_rule = repo / "templates" / "core" / "AGENTS.md"
    direct_python = repo / "bootstrap" / "tests" / "conftest.py"
    template_rule.parent.mkdir(parents=True)
    direct_python.parent.mkdir(parents=True)
    template_rule.write_text("Require the exact rule before review.\n", encoding="utf-8")
    direct_python.write_text('"""This fixture contains six useful words."""\n', encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt", "templates/core/AGENTS.md",
         "bootstrap/tests/conftest.py")
    _git(repo, "commit", "-m", "add covered roots")
    old = _git(repo, "rev-parse", "HEAD")
    template_rule.write_text("Require the exact rule in review.\n", encoding="utf-8")
    direct_python.write_text('"""This fixture now contains six useful words."""\n', encoding="utf-8")
    _git(repo, "add", "templates/core/AGENTS.md", "bootstrap/tests/conftest.py")
    _git(repo, "commit", "-m", "change covered roots")
    result = _run(repo, "prose_diff.py", old, "HEAD")
    assert result.returncode == 0, result.stderr
    assert "CHANGED templates/core/AGENTS.md" in result.stdout
    assert "CHANGED bootstrap/tests/conftest.py" in result.stdout


def test_report_cli_refuses_a_substituted_git_helper(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    helper = repo / "tools" / "git_read.py"
    helper.write_text("raise RuntimeError('must not execute')\n", encoding="utf-8")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 2
    assert "INCOMPLETE" in result.stderr


@pytest.mark.parametrize("layout", ["installed", "source"])
def test_replacer_refuses_a_substituted_report_before_writing(tmp_path: Path, layout: str) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    before = target.read_bytes()
    marker = tmp_path / "executed"
    report = _entrypoint(repo, "prose_diff.py", layout)
    report.write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('executed')\n", encoding="utf-8")
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")
    result = _run_layout(repo, "exact_replace.py", layout, "AGENTS.md", "--old-file", str(old),
                         "--new-file", str(new))
    assert result.returncode == 2
    assert target.read_bytes() == before
    assert not marker.exists()


@pytest.mark.parametrize("layout", ["installed", "source"])
def test_replacer_refuses_an_oversized_report_binding_before_writing(tmp_path: Path, layout: str) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    before = target.read_bytes()
    report = _entrypoint(repo, "prose_diff.py", layout)
    report.write_bytes(b"#" + b"x" * (256 * 1024))
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")
    result = _run_layout(repo, "exact_replace.py", layout, "AGENTS.md", "--old-file", str(old),
                         "--new-file", str(new))
    assert result.returncode == 2
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


@pytest.mark.parametrize("layout", ["installed", "source"])
def test_replacer_refuses_a_wrong_report_pin_before_writing(tmp_path: Path, layout: str) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    before = target.read_bytes()
    caller = _entrypoint(repo, "exact_replace.py", layout)
    caller.write_text(caller.read_text(encoding="utf-8").replace(
        f'_REPORT_SHA256 = "{hashlib.sha256(_entrypoint(repo, "prose_diff.py", layout).read_bytes()).hexdigest()}"',
        f'_REPORT_SHA256 = "{"0" * 64}"'), encoding="utf-8")
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")

    result = _run_layout(repo, "exact_replace.py", layout, "AGENTS.md", "--old-file", str(old),
                         "--new-file", str(new))
    assert result.returncode == 2
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


@pytest.mark.parametrize("lock_state", ["missing", "duplicate", "invalid"])
def test_installed_replacer_refuses_bad_report_lock_record(tmp_path: Path, lock_state: str) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    before = target.read_bytes()
    lock_path = repo / "dev" / ".cairn" / "cairn-lock.yml"
    lock = json.loads(lock_path.read_text(encoding="utf-8").split("\n", 1)[1])
    reports = [row for row in lock["files"] if row.get("dst") == "scripts/prose_diff.py"]
    assert len(reports) == 1
    if lock_state == "missing":
        lock["files"].remove(reports[0])
    elif lock_state == "duplicate":
        lock["files"].append(dict(reports[0]))
    else:
        reports[0]["verbatim"] = False
    lock_path.write_text("# fixture\n" + json.dumps(lock), encoding="utf-8")
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")

    result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old),
                  "--new-file", str(new))
    assert result.returncode == 2
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


@pytest.mark.parametrize("layout", ["installed", "source"])
def test_report_binding_ignores_poisoned_module_cache(tmp_path: Path, layout: str,
                                                      monkeypatch: pytest.MonkeyPatch) -> None:
    repo, _base = _repo(tmp_path)
    caller = _load_entrypoint(_entrypoint(repo, "exact_replace.py", layout))
    name = "_cairn_verified_prose_diff"
    poisoned = types.ModuleType(name)
    poisoned.POISONED = True
    monkeypatch.setitem(sys.modules, name, poisoned)

    bound = caller._report_binding()
    report_bytes = _entrypoint(repo, "prose_diff.py", layout).read_bytes()
    assert bound is not poisoned
    assert not hasattr(bound, "POISONED")
    assert bound.__verified_source__ == report_bytes
    assert bound.__verified_sha256__ == hashlib.sha256(report_bytes).hexdigest()


@pytest.mark.parametrize("layout", ["installed", "source"])
def test_report_binding_refuses_descriptor_change_during_read(tmp_path: Path, layout: str,
                                                               monkeypatch: pytest.MonkeyPatch) -> None:
    repo, _base = _repo(tmp_path)
    report = _entrypoint(repo, "prose_diff.py", layout)
    original = report.read_bytes()
    report_info = os.stat(report)
    caller = _load_entrypoint(_entrypoint(repo, "exact_replace.py", layout))
    real_read = os.read
    evidence = {"triggered": False}

    def mutate_report_descriptor(fd: int, size: int) -> bytes:
        result = real_read(fd, size)
        info = os.fstat(fd)
        if not evidence["triggered"] and (info.st_dev, info.st_ino) == (report_info.st_dev, report_info.st_ino):
            before = os.stat(report)
            report.write_bytes(original)
            os.utime(report, ns=(before.st_atime_ns, before.st_mtime_ns))
            time.sleep(0.02)
            evidence["triggered"] = True
        return result

    monkeypatch.setattr(os, "read", mutate_report_descriptor)
    with pytest.raises(Exception, match="(?i)changed|modified"):
        caller._report_binding()
    assert evidence["triggered"]


@pytest.mark.parametrize("layout", ["installed", "source"])
def test_report_binding_executes_captured_buffer_after_path_swap(tmp_path: Path, layout: str,
                                                                  monkeypatch: pytest.MonkeyPatch) -> None:
    repo, _base = _repo(tmp_path)
    report = _entrypoint(repo, "prose_diff.py", layout)
    trusted = report.read_bytes() + b"\nCAPTURED_REPORT_TEST_MARKER = 'captured-buffer'\n"
    digest = hashlib.sha256(trusted).hexdigest()
    report.write_bytes(trusted)
    caller_path = _entrypoint(repo, "exact_replace.py", layout)
    caller_source = caller_path.read_text(encoding="utf-8")
    import re
    caller_source, count = re.subn(r'(?m)^_REPORT_SHA256 = "[0-9a-f]{64}"$',
                                   f'_REPORT_SHA256 = "{digest}"', caller_source, count=1)
    assert count == 1
    caller_path.write_text(caller_source, encoding="utf-8")
    if layout == "installed":
        _replace_report_lock_hash(repo, digest)
    caller = _load_entrypoint(caller_path)
    real_exec = exec

    def swap_then_exec(code, namespace):
        report.write_text("raise RuntimeError('path replacement was executed')\n", encoding="utf-8")
        return real_exec(code, namespace)

    caller.exec = swap_then_exec
    bound = caller._report_binding()
    assert report.read_text(encoding="utf-8").startswith("raise RuntimeError")
    assert bound.CAPTURED_REPORT_TEST_MARKER == "captured-buffer"
    assert bound.__verified_source__ == trusted


@pytest.mark.parametrize("layout", ["installed", "source"])
def test_report_binding_uses_fixed_destination_not_lock_src_or_cwd(tmp_path: Path, layout: str,
                                                                   monkeypatch: pytest.MonkeyPatch) -> None:
    repo, _base = _repo(tmp_path)
    fixed_report = _entrypoint(repo, "prose_diff.py", layout)
    fixed_bytes = fixed_report.read_bytes()
    decoy = repo / "decoy" / "prose_diff.py"
    decoy.parent.mkdir()
    marker = tmp_path / "decoy-executed"
    decoy.write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('bad')\n", encoding="utf-8")
    if layout == "installed":
        lock_path = repo / "dev" / ".cairn" / "cairn-lock.yml"
        lock = json.loads(lock_path.read_text(encoding="utf-8").split("\n", 1)[1])
        for row in lock["files"]:
            if row.get("dst") == "scripts/prose_diff.py":
                row["src"] = "decoy/prose_diff.py"
        lock_path.write_text("# fixture\n" + json.dumps(lock), encoding="utf-8")
    caller = _load_entrypoint(_entrypoint(repo, "exact_replace.py", layout))
    monkeypatch.chdir(decoy.parent)

    bound = caller._report_binding()
    assert bound.__verified_source__ == fixed_bytes
    assert not marker.exists()


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


@pytest.mark.parametrize("layout", ["installed", "source"])
def test_exact_replacer_preserves_raw_crlf_and_reports_the_edit(tmp_path: Path, layout: str) -> None:
    repo, _base = _repo(tmp_path)
    old, new = tmp_path / "old.bin", tmp_path / "new.bin"
    old.write_bytes(b"bounded.\r\n")
    new.write_bytes(b"available.\r\n")
    (repo / "AGENTS.md").write_bytes(
        b"Keep every tool output bounded.\r\nThis protects the user.\r\n")
    result = _run_layout(repo, "exact_replace.py", layout, "AGENTS.md", "--old-file", str(old),
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

