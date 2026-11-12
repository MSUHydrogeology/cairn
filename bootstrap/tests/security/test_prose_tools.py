"""CLI contracts for the prose report and exact replacer.

Promises:
- The prose report compares the committed base's roots and marks changed or moved prose by unit position.
- The prose report refuses a base whose root manifest is missing, malformed, negated or oversized, or whose merge base is ambiguous.
- The prose report bounds what it reads and prints, escapes hidden characters in paths, and marks skipped or capped content as a gap.
- The exact replacer edits one target only when the old text matches exactly once, and leaves the target unchanged on refusal.
- The exact replacer refuses link and hard-link targets, oversized or malformed inputs, and keeps the target's file mode.
- The exact replacer refuses to write when its report step is substituted, mis-pinned, bare-digested or oversized, and exits 3 if the report fails after a write.
- Installed prose tools refuse a substituted git helper or a bad lock record, including one that points elsewhere; a fresh install runs both CLIs.
- Piped new text is accepted from one stdin source only, and a held-open stdin cannot hang the replacer.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
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
            {"dst": "tools/git_read.py", "verbatim": True, "hash": "sha256:" + GIT_SHA},
            {"dst": "scripts/prose_diff.py", "verbatim": True,
             "hash": "sha256:" + hashlib.sha256((scripts / "prose_diff.py").read_bytes()).hexdigest()},
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


def _run_stdin(repo: Path, *args: str, input_text: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(repo / "scripts" / "exact_replace.py"), *args],
                          cwd=repo, input=input_text, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, timeout=20)


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
    matches[0]["hash"] = "sha256:" + digest.removeprefix("sha256:")
    lock_path.write_text("# fixture\n" + json.dumps(lock), encoding="utf-8")


def test_report_cli_uses_committed_base_roots_and_shows_rule_change(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    (repo / "AGENTS.md").write_text("Keep every tool output available.\n", encoding="utf-8")
    _git(repo, "add", "AGENTS.md"); _git(repo, "commit", "-m", "change rule")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 0, result.stderr
    assert "CHANGED AGENTS.md" in result.stdout
    assert "bounded" in result.stdout and "available" in result.stdout


@pytest.mark.parametrize("layout", ["installed", "source"])
def test_report_cli_marks_a_heading_move_by_unit_position(
        tmp_path: Path, layout: str) -> None:
    repo, _initial = _repo(tmp_path)
    target = repo / "AGENTS.md"
    before = "## Anchor\n## Moving heading\n## Middle\n## End\n"
    after = "## Anchor\n## Middle\n## End\n## Moving heading\n"
    target.write_text(before, encoding="utf-8")
    _git(repo, "add", "AGENTS.md"); _git(repo, "commit", "-m", "heading move base")
    base = _git(repo, "rev-parse", "HEAD")
    target.write_text(after, encoding="utf-8")
    _git(repo, "add", "AGENTS.md"); _git(repo, "commit", "-m", "move heading")

    result = _run_layout(repo, "prose_diff.py", layout, base, "HEAD")
    assert result.returncode == 0, result.stderr
    assert "INCOMPLETE" not in result.stdout
    removed = re.search(
        r"REMOVED AGENTS\.md \[heading\] \[before unit (\d+)\]: (.+)",
        result.stdout,
    )
    added = re.search(
        r"ADDED AGENTS\.md \[heading\] \[after unit (\d+)\]: (.+)",
        result.stdout,
    )
    assert removed and added, result.stdout
    assert removed.group(2) == added.group(2) == "## Moving heading"
    assert removed.group(1) != added.group(1)


@pytest.mark.parametrize("layout", ["installed", "source"])
def test_replacer_report_marks_a_list_item_swap_by_unit_position(
        tmp_path: Path, layout: str) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    before = (
        "## Anchor\n- alpha requirement kept\n- beta requirement checked\n"
        "## End\n"
    )
    after = (
        "## Anchor\n- beta requirement checked\n- alpha requirement kept\n"
        "## End\n"
    )
    target.write_text(before, encoding="utf-8")
    old, new = tmp_path / "old.txt", tmp_path / "new.txt"
    old.write_text("- alpha requirement kept\n- beta requirement checked\n",
                   encoding="utf-8")
    new.write_text("- beta requirement checked\n- alpha requirement kept\n",
                   encoding="utf-8")

    result = _run_layout(
        repo, "exact_replace.py", layout, "AGENTS.md", "--old-file", str(old),
        "--new-file", str(new),
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert "Applied exactly one replacement sequence." in result.stdout
    assert "INCOMPLETE" not in result.stdout
    assert target.read_text(encoding="utf-8") == after
    removed = re.search(
        r"REMOVED AGENTS\.md \[list\] \[before unit (\d+)\]: (.+)",
        result.stdout,
    )
    added = re.search(
        r"ADDED AGENTS\.md \[list\] \[after unit (\d+)\]: (.+)",
        result.stdout,
    )
    assert removed and added, result.stdout
    assert removed.group(2) == added.group(2) == "- beta requirement checked"
    assert removed.group(1) != added.group(1)


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


def test_report_places_tool_policy_notice_first(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    tool = repo / "scripts" / "prose_diff.py"
    tool.write_text(tool.read_text(encoding="utf-8") + "\n# harmless tool policy change\n", encoding="utf-8")
    _git(repo, "add", "scripts/prose_diff.py"); _git(repo, "commit", "-m", "change report tool")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[0].startswith("NOTICE first: scripts/prose_diff.py")


def test_report_refuses_a_negated_prose_root_in_base_manifest(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    manifest = repo / "scripts" / "prose_roots.txt"
    manifest.write_text("# prose-roots v1\n!AGENTS.md\n", encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt"); _git(repo, "commit", "-m", "invalid prose roots")
    result = _run(repo, "prose_diff.py", "HEAD", "HEAD")
    assert result.returncode == 2
    assert "negated prose root is invalid" in result.stderr


@pytest.mark.parametrize("manifest", [
    "", "# wrong sentinel\n", "../outside\n", "/absolute\n", "-option\n",
])
def test_report_refuses_malformed_prose_root_manifests(tmp_path: Path, manifest: str) -> None:
    repo, _base = _repo(tmp_path)
    path = repo / "scripts" / "prose_roots.txt"
    path.write_text(manifest, encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt"); _git(repo, "commit", "-m", "malformed roots")
    result = _run(repo, "prose_diff.py", "HEAD", "HEAD")
    assert result.returncode == 2
    assert "INCOMPLETE" in result.stderr


def test_report_refuses_a_missing_base_prose_roots_list(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    (repo / "scripts" / "prose_roots.txt").unlink()
    _git(repo, "add", "-u", "scripts/prose_roots.txt"); _git(repo, "commit", "-m", "remove roots list")
    result = _run(repo, "prose_diff.py", "HEAD", "HEAD")
    assert result.returncode == 2
    assert "missing or linked base manifest: scripts/prose_roots.txt" in result.stderr


def test_report_uses_explicit_default_branch_and_refuses_missing_metadata(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    _git(repo, "branch", "stable-base", base)
    (repo / "AGENTS.md").write_text("Keep all tool output bounded. This protects the user.\n", encoding="utf-8")
    _git(repo, "add", "AGENTS.md"); _git(repo, "commit", "-m", "change from default branch")
    explicit = _run(repo, "prose_diff.py", "--default-branch", "stable-base")
    assert explicit.returncode == 0, explicit.stderr
    assert "CHANGED AGENTS.md" in explicit.stdout

    missing = _run(repo, "prose_diff.py")
    assert missing.returncode == 2
    assert "default branch metadata unavailable" in missing.stderr


def test_report_refuses_an_ambiguous_merge_base(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    _git(repo, "checkout", "-b", "left")
    (repo / "AGENTS.md").write_text("Keep all output bounded. This protects the user.\n", encoding="utf-8")
    _git(repo, "add", "AGENTS.md"); _git(repo, "commit", "-m", "left change")
    left_commit = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "-b", "right", base)
    (repo / "rule.txt").write_text("Another branch adds a separate prose file.\n", encoding="utf-8")
    _git(repo, "add", "rule.txt"); _git(repo, "commit", "-m", "right change")
    right_commit = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "-b", "left-merge", left_commit)
    _git(repo, "merge", "--no-ff", "right", "-m", "left merges right")
    _git(repo, "checkout", "-b", "right-merge", right_commit)
    _git(repo, "merge", "--no-ff", left_commit, "-m", "right merges left")

    # Independent merge commits from the original tips have two best common ancestors.
    _git(repo, "checkout", "left-merge")
    result = _run(repo, "prose_diff.py", "--default-branch", "right-merge")
    assert result.returncode == 2
    assert "merge base is unavailable or ambiguous" in result.stderr


def test_report_escapes_hidden_characters_in_repository_paths(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    roots = repo / "scripts" / "prose_roots.txt"
    roots.write_text("# prose-roots v1\nrules\n", encoding="utf-8")
    rules = repo / "rules"
    rules.mkdir()
    path = rules / f"rule{chr(0x202E)}.md"
    path.write_text("Keep the original wording.\n", encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt", "rules"); _git(repo, "commit", "-m", "add hidden-name prose")
    base = _git(repo, "rev-parse", "HEAD")
    path.write_text("Keep the changed wording.\n", encoding="utf-8")
    _git(repo, "add", "rules"); _git(repo, "commit", "-m", "change hidden-name prose")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 0, result.stderr
    assert "rule\\u202e.md" in result.stdout
    assert chr(0x202E) not in result.stdout


def test_report_refuses_an_oversized_base_manifest(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    manifest = repo / "scripts" / "prose_roots.txt"
    manifest.write_text("# prose-roots v1\n" + "x" * (64 * 1024), encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt"); _git(repo, "commit", "-m", "oversized roots")
    result = _run(repo, "prose_diff.py", "HEAD", "HEAD")
    assert result.returncode == 2
    assert "INCOMPLETE" in result.stderr


def test_report_refuses_an_oversized_changed_file(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    roots = repo / "scripts" / "prose_roots.txt"
    roots.write_text("# prose-roots v1\nrules/large.md\n", encoding="utf-8")
    target = repo / "rules" / "large.md"
    target.parent.mkdir()
    target.write_text("small\n", encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt", "rules"); _git(repo, "commit", "-m", "small tracked file")
    base = _git(repo, "rev-parse", "HEAD")
    target.write_text("x" * (8 * 1024 * 1024 + 1), encoding="utf-8")
    _git(repo, "add", "rules/large.md"); _git(repo, "commit", "-m", "oversized prose")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 2
    assert "INCOMPLETE" in (result.stdout + result.stderr)


def test_report_enforces_aggregate_read_cap(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    roots = repo / "scripts" / "prose_roots.txt"
    roots.write_text("# prose-roots v1\nrules\n", encoding="utf-8")
    rules = repo / "rules"
    rules.mkdir()
    (rules / "a.md").write_text("old rule a\n", encoding="utf-8")
    (rules / "b.md").write_text("old rule b\n", encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt", "rules"); _git(repo, "commit", "-m", "aggregate fixtures")
    base = _git(repo, "rev-parse", "HEAD")
    (rules / "a.md").write_text("new rule a\n", encoding="utf-8")
    (rules / "b.md").write_text("new rule b\n", encoding="utf-8")
    _git(repo, "add", "rules"); _git(repo, "commit", "-m", "change aggregate fixtures")
    script = repo / "scripts" / "prose_diff.py"
    source = script.read_text(encoding="utf-8")
    assert source.count("_TOTAL_CAP = 128 * 1024 * 1024") == 1
    script.write_text(source.replace("_TOTAL_CAP = 128 * 1024 * 1024", "_TOTAL_CAP = 24"), encoding="utf-8")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 2
    assert "aggregate blob cap exceeded" in result.stderr


def test_report_marks_raw_evidence_missing_when_output_cap_is_reached(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    roots = repo / "scripts" / "prose_roots.txt"
    roots.write_text("# prose-roots v1\nrules.yml\n", encoding="utf-8")
    target = repo / "rules.yml"
    target.write_text("x" * 4000, encoding="utf-8")
    _git(repo, "add", "scripts/prose_roots.txt", "rules.yml"); _git(repo, "commit", "-m", "raw output fixture")
    base = _git(repo, "rev-parse", "HEAD")
    target.write_text("y" * 4000, encoding="utf-8")
    script = repo / "scripts" / "prose_diff.py"
    source = script.read_text(encoding="utf-8")
    assert source.count("_OUT_CAP = 8 * 1024 * 1024") == 1
    script.write_text(source.replace("_OUT_CAP = 8 * 1024 * 1024", "_OUT_CAP = 1024"), encoding="utf-8")
    _git(repo, "add", "rules.yml", "scripts/prose_diff.py"); _git(repo, "commit", "-m", "exceed rendered cap")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 2
    assert "RAW EVIDENCE INCOMPLETE" in result.stdout


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
    old.write_text("forbidden", encoding="utf-8")
    new.write_text("allowed", encoding="utf-8")
    result = _run(repo, "exact_replace.py", "rules.yml", "--old-file", str(old), "--new-file", str(new))
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert target.read_text(encoding="utf-8") == "guard: allowed\n"
    assert "NOT COMPARED rules.yml: unsupported suffix '.yml'; structured prose extraction unavailable" in result.stdout
    assert 'RAW CHANGED rules.yml' in result.stdout
    assert 'before="forbidden" ; after="allowed"' in result.stdout


def test_exact_replacer_binds_git_reader_to_the_verified_buffer(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    caller = _load_entrypoint(repo / "scripts" / "exact_replace.py")
    helper = caller._git_binding()
    assert helper._VERIFIED_SOURCE == helper.__verified_source__
    assert helper._VERIFIED_SHA256 == helper.__verified_sha256__
    assert hashlib.sha256(helper._VERIFIED_SOURCE).hexdigest() == helper._VERIFIED_SHA256


def test_replacer_reads_rewritten_windows_fragment_after_creation(tmp_path: Path) -> None:
    if os.name != "nt":
        pytest.skip("Windows creation and change times are required for this control")
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    target.write_bytes(b"bounded")
    old, new = tmp_path / "old.txt", tmp_path / "new.txt"
    old.write_bytes(b"bounded")
    new.write_bytes(b"available")
    created_path = new.stat()
    with new.open("rb") as stream:
        created_descriptor = os.fstat(stream.fileno())
    birth = getattr(created_path, "st_birthtime_ns", None)
    assert type(birth) is int
    time.sleep(0.02)
    with new.open("r+b") as stream:
        stream.seek(0)
        stream.write(b"available")
        stream.flush()
        os.fsync(stream.fileno())
        descriptor_change = os.fstat(stream.fileno())
    rewritten_path = new.stat()
    assert created_path.st_dev == rewritten_path.st_dev
    assert created_path.st_ino == rewritten_path.st_ino
    assert created_path.st_size == rewritten_path.st_size
    assert rewritten_path.st_ctime_ns == birth
    assert rewritten_path.st_birthtime_ns == birth
    assert descriptor_change.st_birthtime_ns == birth
    assert descriptor_change.st_ctime_ns != created_descriptor.st_ctime_ns
    assert descriptor_change.st_ctime_ns != birth, (
        "descriptor ctime must expose the rewritten file change time")
    assert new.read_bytes() == b"available"

    result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old),
                  "--new-file", str(new))
    assert result.returncode == 0, result.stdout + result.stderr
    assert target.read_bytes() == b"available"


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


def test_report_cli_refuses_a_substituted_git_helper(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    helper = repo / "tools" / "git_read.py"
    helper.write_text("raise RuntimeError('must not execute')\n", encoding="utf-8")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 2
    assert "INCOMPLETE" in result.stderr


def test_report_cli_refuses_a_bare_digest_in_an_installed_lock(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    lock_path = repo / "dev" / ".cairn" / "cairn-lock.yml"
    lock = json.loads(lock_path.read_text(encoding="utf-8").split("\n", 1)[1])
    record = next(row for row in lock["files"] if row["dst"] == "tools/git_read.py")
    record["hash"] = record["hash"].removeprefix("sha256:")
    lock_path.write_text("# fixture\n" + json.dumps(lock), encoding="utf-8")
    result = _run(repo, "prose_diff.py", base, "HEAD")
    assert result.returncode == 2
    assert "install lock does not uniquely pin the trusted binding" in result.stderr


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


@pytest.mark.parametrize("lock_state", ["missing", "duplicate", "invalid", "bare_digest"])
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
    elif lock_state == "bare_digest":
        reports[0]["hash"] = reports[0]["hash"].removeprefix("sha256:")
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


def test_fresh_scaffold_install_runs_both_public_prose_clis_with_real_lock(
        tmp_path: Path) -> None:
    repo = tmp_path / "adopter"
    repo.mkdir()
    _git(repo, "init", "--initial-branch=main")
    _git(repo, "config", "user.email", "cairn-test@example.invalid")
    _git(repo, "config", "user.name", "Cairn test")
    _git(repo, "commit", "--allow-empty", "-m", "adopter base")
    profile = tmp_path / "profile.yml"
    profile.write_text(
        "project_name: Prose CLI test\n"
        "test_command: pytest\n"
        "modules:\n  - content-security\n",
        encoding="utf-8",
    )
    installed = subprocess.run(
        [sys.executable, str(ROOT / "bootstrap" / "scaffold.py"),
         "--config", str(profile), "--target", str(repo),
         "--cairn-root", str(ROOT), "--allow-dev"],
        cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, timeout=30,
    )
    assert installed.returncode == 0, installed.stdout + installed.stderr
    lock_text = (repo / "dev" / ".cairn" / "cairn-lock.yml").read_text(encoding="utf-8")
    lock = json.loads("\n".join(line for line in lock_text.splitlines()
                               if not line.lstrip().startswith("#")))
    records = {row["dst"]: row for row in lock["files"]}
    for destination in ("tools/git_read.py", "scripts/prose_diff.py"):
        data = (repo / destination).read_bytes()
        assert records[destination]["verbatim"] is True
        assert records[destination]["hash"] == "sha256:" + hashlib.sha256(data).hexdigest()
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "fresh Cairn install")
    installed_revision = _git(repo, "rev-parse", "HEAD")

    rule = repo / "AGENTS.md"
    old_line, *remaining_lines = rule.read_bytes().splitlines(keepends=True)
    if old_line.endswith(b"\r\n"):
        terminator = b"\r\n"
    elif old_line.endswith((b"\n", b"\r")):
        terminator = old_line[-1:]
    else:
        terminator = b""
    content = old_line[:-len(terminator)] if terminator else old_line
    new_line = content + b" (CLI fixture)" + terminator
    old, new = tmp_path / "old.txt", tmp_path / "new.txt"
    old.write_bytes(old_line)
    new.write_bytes(new_line)
    replaced = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old),
                    "--new-file", str(new))
    assert replaced.returncode == 0, replaced.stdout + replaced.stderr
    assert "CHANGED AGENTS.md" in replaced.stdout
    assert rule.read_bytes() == new_line + b"".join(remaining_lines)
    _git(repo, "add", "AGENTS.md")
    _git(repo, "commit", "-m", "edit through installed replacer")

    report = _run(repo, "prose_diff.py", installed_revision, "HEAD")
    assert report.returncode == 0, report.stderr
    assert "CHANGED AGENTS.md" in report.stdout
    assert "CLI fixture" in report.stdout


# Declared exception (internal hook): Hook: monkeypatch.setitem(sys.modules) plants a poisoned module under the report import name; test calls private _report_binding. A public CLI cannot .
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


# Declared exception (internal hook): Hook: monkeypatch of os.read rewrites the report file between read and fstat; test calls private _report_binding. A public CLI cannot pause a read to .
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


# Declared exception (internal hook): Hook: replaces the module's exec attribute to swap the report path after capture; test calls private _report_binding. A public CLI cannot pause betwee.
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


@pytest.mark.parametrize("target_name", [
    "../AGENTS.md", "/AGENTS.md", "C:/AGENTS.md", "a\\b", ".git/config",
    "GIT~1/AGENTS.md", "folder//AGENTS.md", "./AGENTS.md",
])
def test_replacer_refuses_unsafe_target_components(tmp_path: Path, target_name: str) -> None:
    repo, _base = _repo(tmp_path)
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")
    target = repo / "AGENTS.md"
    before = target.read_bytes()
    result = _run(repo, "exact_replace.py", target_name, "--old-file", str(old), "--new-file", str(new))
    assert result.returncode == 2
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


def test_replacer_refuses_hard_link_targets(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    peer = repo / "peer.md"
    try:
        os.link(target, peer)
    except (OSError, NotImplementedError):
        pytest.skip("hard links unavailable")
    before = target.read_bytes()
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")
    result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old), "--new-file", str(new))
    assert result.returncode == 2
    assert target.read_bytes() == before and peer.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


def test_replacer_preserves_target_mode(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    target.chmod(0o640)
    expected_mode = target.stat().st_mode & 0o777
    if os.name == "posix":
        assert expected_mode == 0o640
    before = target.read_bytes()
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")
    result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old), "--new-file", str(new))
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert target.read_bytes() == before.replace(b"bounded", b"available")
    assert target.stat().st_mode & 0o777 == expected_mode


@pytest.mark.parametrize("oversized", ["target", "old", "new", "stdin"])
def test_replacer_refuses_each_oversized_single_file_input(tmp_path: Path, oversized: str) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    if oversized == "target":
        target.write_bytes(b"x" * (8 * 1024 * 1024 + 1))
    before = target.read_bytes()
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded" if oversized != "old" else b"x" * (8 * 1024 * 1024 + 1))
    new.write_bytes(b"available" if oversized != "new" else b"y" * (8 * 1024 * 1024 + 1))
    if oversized == "stdin":
        result = _run_stdin(repo, "AGENTS.md", "--old-file", "-", "--new-file", str(new),
                            input_text="x" * (8 * 1024 * 1024 + 1))
    else:
        result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old), "--new-file", str(new))
    assert result.returncode == 2
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


def test_replacer_refuses_oversized_json_batch_and_decoded_pair(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    before = target.read_bytes()
    batch = tmp_path / "batch.json"
    batch.write_bytes(b" " * (16 * 1024 * 1024 + 1))
    result = _run(repo, "exact_replace.py", "AGENTS.md", "--batch", str(batch))
    assert result.returncode == 2 and target.read_bytes() == before

    batch.write_text(json.dumps([{"old": "bounded", "new": "x" * (8 * 1024 * 1024 + 1)}]),
                     encoding="utf-8")
    result = _run(repo, "exact_replace.py", "AGENTS.md", "--batch", str(batch))
    assert result.returncode == 2
    assert "decoded pair exceeds 8 MiB" in result.stdout
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


def test_replacer_refuses_more_than_256_batch_pairs(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    before = target.read_bytes()
    batch = tmp_path / "batch.json"
    batch.write_text(json.dumps([{"old": "x", "new": "y"} for _ in range(257)]), encoding="utf-8")
    result = _run(repo, "exact_replace.py", "AGENTS.md", "--batch", str(batch))
    assert result.returncode == 2
    assert "batch must contain 1 to 256 pairs" in result.stdout
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


@pytest.mark.parametrize("bad_input", ["empty-old", "invalid-utf8", "duplicate-json-key", "extra-json-key"])
def test_replacer_refuses_empty_or_malformed_sources(tmp_path: Path, bad_input: str) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    before = target.read_bytes()
    if bad_input == "empty-old":
        old, new = tmp_path / "old", tmp_path / "new"
        old.write_bytes(b""); new.write_bytes(b"replacement")
        result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old), "--new-file", str(new))
    elif bad_input == "invalid-utf8":
        old, new = tmp_path / "old", tmp_path / "new"
        old.write_bytes(b"\xff"); new.write_bytes(b"replacement")
        result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old), "--new-file", str(new))
    else:
        batch = tmp_path / "batch.json"
        raw = '[{"old":"bounded","old":"bounded","new":"changed"}]'
        if bad_input == "extra-json-key":
            raw = '[{"old":"bounded","new":"changed","extra":true}]'
        batch.write_text(raw, encoding="utf-8")
        result = _run(repo, "exact_replace.py", "AGENTS.md", "--batch", str(batch))
    assert result.returncode == 2
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


def test_replacer_accepts_new_text_from_stdin_and_refuses_two_stdin_sources(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    old = tmp_path / "old"
    old.write_bytes(b"bounded")
    success = _run_stdin(repo, "AGENTS.md", "--old-file", str(old), "--new-file", "-",
                         input_text="available")
    assert success.returncode == 0, (success.stdout, success.stderr)
    assert (repo / "AGENTS.md").read_text(encoding="utf-8").startswith("Keep every tool output available.")

    before = (repo / "AGENTS.md").read_bytes()
    both = _run_stdin(repo, "AGENTS.md", "--old-file", "-", "--new-file", "-", input_text="ignored")
    assert both.returncode == 2
    assert (repo / "AGENTS.md").read_bytes() == before


def test_replacer_refuses_oversized_result_before_write(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    target.write_bytes(b"Xzz")
    before = target.read_bytes()
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"zz"); new.write_bytes(b"x" * (8 * 1024 * 1024))
    result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old), "--new-file", str(new))
    assert result.returncode == 2
    assert "replacement result exceeds 8 MiB" in result.stdout
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


def test_replacer_enforces_cumulative_matching_work_limit(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    pairs = [{"old": f"marker-{index:02d}", "new": f"review-{index:02d}"}
             for index in range(9)]
    markers = "".join(item["old"] for item in pairs).encode("ascii")
    target.write_bytes(b"x" * (8 * 1024 * 1024 - len(markers)) + markers)
    before = target.read_bytes()
    batch = tmp_path / "batch.json"
    batch.write_text(json.dumps(pairs), encoding="utf-8")

    result = _run(repo, "exact_replace.py", "AGENTS.md", "--batch", str(batch))
    assert result.returncode == 2
    assert "matching work limit exceeded" in result.stdout
    assert target.read_bytes() == before
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


def test_replacer_refuses_a_target_changed_before_atomic_replace(tmp_path: Path) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    script = repo / "scripts" / "exact_replace.py"
    source = script.read_text(encoding="utf-8")
    call = "    _atomic_replace(full, old_target, result, target_rows, mode)"
    mutation = (
        "    with open(full, 'wb') as external_change:\n"
        "        external_change.write(b'external concurrent content\\n')\n" + call
    )
    assert source.count(call) == 1
    script.write_text(source.replace(call, mutation), encoding="utf-8")
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")

    result = _run(repo, "exact_replace.py", "AGENTS.md", "--old-file", str(old), "--new-file", str(new))
    assert result.returncode == 2
    assert target.read_bytes() == b"external concurrent content\n"
    assert list(repo.glob(".cairn-replace-*.tmp")) == []


@pytest.mark.parametrize("layout", ["installed", "source"])
def test_replacer_returns_three_after_a_postwrite_report_failure(tmp_path: Path, layout: str) -> None:
    repo, _base = _repo(tmp_path)
    target = repo / "AGENTS.md"
    report = _entrypoint(repo, "prose_diff.py", layout)
    failed_report = b"def report_text_change(*args):\n    raise RuntimeError('report failed after write')\n"
    report.write_bytes(failed_report)
    digest = hashlib.sha256(failed_report).hexdigest()
    caller_path = _entrypoint(repo, "exact_replace.py", layout)
    caller = caller_path.read_text(encoding="utf-8")
    import re
    caller, count = re.subn(r'(?m)^_REPORT_SHA256 = "[0-9a-f]{64}"$',
                            f'_REPORT_SHA256 = "{digest}"', caller, count=1)
    assert count == 1
    caller_path.write_text(caller, encoding="utf-8")
    if layout == "installed":
        _replace_report_lock_hash(repo, digest)
    old, new = tmp_path / "old", tmp_path / "new"
    old.write_bytes(b"bounded"); new.write_bytes(b"available")

    result = _run_layout(repo, "exact_replace.py", layout, "AGENTS.md", "--old-file", str(old),
                         "--new-file", str(new))
    assert result.returncode == 3
    assert target.read_bytes() == b"Keep every tool output available. This protects the user.\n"
    assert "Applied, but the change report failed" in result.stdout
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
