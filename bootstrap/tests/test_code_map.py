"""Real-entry checks for the bounded, filesystem-only architecture map."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "code_map.py"
TEMPLATE_SCRIPT = ROOT / "templates" / "modules" / "team-gated" / "code_map.py"
sys.path.insert(0, str(ROOT))


def _run(root: Path, *args: str, script: Path = SCRIPT,
         timeout: float = 65.0) -> tuple[subprocess.CompletedProcess[bytes], dict]:
    completed = subprocess.run(
        [sys.executable, "-I", str(script), "--root", str(root), *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
        check=False,
    )
    return completed, json.loads(completed.stdout.decode("ascii"))


def _internal(script: Path, body: str, *args: str,
              timeout: float = 65.0) -> subprocess.CompletedProcess[bytes]:
    runner = (
        "import importlib.util,sys\n"
        "spec=importlib.util.spec_from_file_location('code_map_test',sys.argv[1])\n"
        "ns=importlib.util.module_from_spec(spec)\n"
        "sys.modules[spec.name]=ns; spec.loader.exec_module(ns); ns=ns.__dict__\n"
        + body
    )
    return subprocess.run(
        [sys.executable, "-I", "-c", runner, str(script), *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
        check=False,
    )


def test_real_cli_maps_files_symbols_and_unsupported_languages(tmp_path: Path) -> None:
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "main.py").write_text(
        '"""Module summary."""\n'
        'def public_call(value):\n    """Returns a value."""\n    return value\n'
        'class PublicType:\n    """A public type."""\n    def method(self):\n        return 1\n'
        'def _private():\n    return 0\n', encoding="utf-8")
    (tmp_path / "pkg" / "model.rs").write_text("fn main() {}\n", encoding="utf-8")
    completed, result = _run(tmp_path)
    assert completed.returncode == 0
    assert result["status"] == "complete"
    assert result["revision"] is None
    assert "no Git inspection" in result["revision_note"]
    assert "pkg" in result["components"]
    assert {row["path"]: row["analysis"] for row in result["files"]} == {
        "pkg/main.py": "parsed", "pkg/model.rs": "unsupported",
    }
    public = result["files"][0]["public"]
    assert [(row["qualified_name"], row["summary"]) for row in public] == [
        ("public_call", "Returns a value."),
        ("PublicType", "A public type."),
        ("PublicType.method", ""),
    ]
    assert "_private" not in json.dumps(result)


def test_real_cli_does_not_execute_inspected_python_and_escapes_controls(
    tmp_path: Path,
) -> None:
    marker = tmp_path / "executed"
    payload = f"import pathlib\npathlib.Path({str(marker)!r}).touch()\n"
    (tmp_path / "\x1b[31mhostile.py").write_text(payload, encoding="utf-8")
    completed, result = _run(tmp_path)
    assert completed.returncode == 0
    assert not marker.exists()
    assert b"\x1b" not in completed.stdout
    assert "\\u001b" in completed.stdout.decode("ascii")
    assert result["status"] == "complete"


def test_cli_requires_isolated_python_mode(tmp_path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    assert completed.returncode == 2
    assert b"run with the trusted Python runtime in -I mode" in completed.stderr


def test_isolated_cli_ignores_planted_project_and_adjacent_modules(
    tmp_path: Path,
) -> None:
    from bootstrap.scaffold import create_dev_tree, install_modules

    create_dev_tree(tmp_path)
    install_modules(ROOT / "templates", tmp_path, {}, ["architecture-review"])
    tools = tmp_path / "tools"
    tools.mkdir(exist_ok=True)
    sentinels = [tmp_path / f"{name}.sentinel" for name in
                 ("ast", "json", "sitecustomize", "adjacent_ast",
                  "adjacent_json", "adjacent_sitecustomize")]
    for name, sentinel in zip(
        ("ast", "json", "sitecustomize"), sentinels[:3], strict=True
    ):
        (tmp_path / f"{name}.py").write_text(
            f"import pathlib\npathlib.Path({str(sentinel)!r}).touch()\n")
    for name, sentinel in zip(
        ("ast", "json", "sitecustomize"), sentinels[3:], strict=True
    ):
        (tools / f"{name}.py").write_text(
            f"import pathlib\npathlib.Path({str(sentinel)!r}).touch()\n")
    (tmp_path / "api.py").write_text("def answer(): return 42\n")
    installed = tools / "code_map.py"
    completed, result = _run(tmp_path, script=installed)
    assert completed.returncode == 0
    assert result["status"] == "complete"
    assert not any(sentinel.exists() for sentinel in sentinels)


def test_real_cli_changed_and_release_neighbors_report_sampling(tmp_path: Path) -> None:
    (tmp_path / "changed.py").write_text(
        "def route_data(source):\n    return source.value\n", encoding="utf-8")
    (tmp_path / "old.py").write_text(
        "def route_value(source):\n    return source.value\n", encoding="utf-8")
    completed, changed = _run(tmp_path, "--changed", "changed.py")
    assert completed.returncode == 0
    assert changed["sampling"]["population"] == 1
    assert changed["sampling"]["compared"] == 1
    assert changed["budgets"]["comparisons"] == 1
    assert changed["neighbors"][0]["neighbors"][0]["path"] == "old.py"
    completed, release = _run(tmp_path, "--release")
    assert completed.returncode == 0
    assert release["sampling"]["population"] == 1
    assert release["sampling"]["unsampled"] == 0
    assert release["budgets"]["comparisons"] == release["sampling"]["compared"]


def test_real_cli_maps_nested_classes_and_compares_private_local_functions(
    tmp_path: Path,
) -> None:
    (tmp_path / "a.py").write_text(
        "class Outer:\n    class Inner:\n        def flow_rate(self): return 1\n"
        "def _private_flow():\n    def local_helper(): return 1\n    return local_helper()\n")
    (tmp_path / "b.py").write_text("def _private_pump(): return 1\n")
    completed, result = _run(tmp_path, "--changed", "a.py")
    assert completed.returncode == 0
    assert result["status"] == "complete"
    public = {s["qualified_name"] for s in result["files"][0]["public"]}
    assert public == {"Outer", "Outer.Inner", "Outer.Inner.flow_rate"}
    functions = {row["function"]["qualified_name"] for row in result["neighbors"]}
    assert {"Outer.Inner.flow_rate", "_private_flow",
            "_private_flow.<locals>.local_helper"} <= functions
    matches = {n["qualified_name"] for row in result["neighbors"]
               for n in row["neighbors"]}
    assert "_private_pump" in matches
    assert result["sampling"]["compared"] == result["budgets"]["comparisons"]


def test_real_cli_declares_metadata_omissions_and_allows_explicit_root(
    tmp_path: Path,
) -> None:
    for name in (".git", "__pycache__", ".pytest_cache", ".agents", ".claude", ".cairn", ".hidden"):
        directory = tmp_path / name
        directory.mkdir()
        (directory / "source.py").write_text("def visible(): pass\n")
    (tmp_path / ".hidden" / ".git").write_text("ordinary file\n")
    (tmp_path / ".hidden" / "__pycache__").mkdir()
    (tmp_path / ".hidden" / "__pycache__" / "cached.py").write_text("def ignored(): pass\n")
    completed, result = _run(tmp_path)
    assert completed.returncode == 0
    assert result["status"] == "complete"
    assert set(result["scope"]["excluded_directory_names"]) == {
        ".git", "__pycache__", ".pytest_cache"}
    assert {item["path"] for item in result["omissions"]} == {
        ".git", "__pycache__", ".pytest_cache", ".hidden/__pycache__"}
    assert all(item["reason"] for item in result["omissions"])
    assert {row["path"] for row in result["files"]} == {
        ".agents/source.py", ".claude/source.py", ".cairn/source.py", ".hidden/source.py",
        ".hidden/.git"}
    assert result["budgets"]["entries_seen"] == 13
    completed, explicit = _run(tmp_path / ".git")
    assert completed.returncode == 0
    assert [row["path"] for row in explicit["files"]] == ["source.py"]
    assert explicit["omissions"] == []


def test_real_cli_refuses_links_and_special_files(tmp_path: Path) -> None:
    (tmp_path / "real").mkdir()
    (tmp_path / "real" / "source.py").write_text("def kept(): pass\n")
    (tmp_path / "linked-dir").symlink_to(tmp_path / "real", target_is_directory=True)
    (tmp_path / "linked.py").symlink_to(tmp_path / "real" / "source.py")
    if hasattr(os, "mkfifo"):
        os.mkfifo(tmp_path / "pipe.py")
    completed, result = _run(tmp_path)
    assert completed.returncode == 1
    assert result["status"] == "incomplete"
    codes = {item["code"] for item in result["diagnostics"]}
    assert "linked-entry" in codes
    assert "special-file" in codes
    assert "source.py" not in [row["path"] for row in result["files"]]


@pytest.mark.skipif(os.name != "posix", reason="POSIX no-follow root walk")
def test_real_cli_refuses_a_linked_root(tmp_path: Path) -> None:
    root = tmp_path / "real"
    root.mkdir()
    linked = tmp_path / "linked-root"
    linked.symlink_to(root, target_is_directory=True)
    completed = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), "--root", str(linked)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    assert completed.returncode == 2
    assert json.loads(completed.stdout.decode("ascii"))["status"] == "incomplete"


def test_real_cli_reports_malformed_deep_and_oversized_sources(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text("def unfinished(:\n pass\n")
    (tmp_path / "deep.py").write_text("x = " + "(" * 2_000 + "1" + ")" * 2_000)
    (tmp_path / "large.py").write_bytes(b"#" + b"x" * 1_048_576)
    completed, result = _run(tmp_path)
    assert completed.returncode == 1
    assert result["status"] == "incomplete"
    assert {item["code"] for item in result["diagnostics"]} >= {
        "parse-error", "source-limit",
    }


def test_real_cli_enforces_fixed_entry_budget(tmp_path: Path) -> None:
    for index in range(10_001):
        (tmp_path / f"f{index:05}.txt").touch()
    completed, result = _run(tmp_path)
    assert completed.returncode == 1
    assert result["budgets"]["entries_limit"] == 10_000
    assert result["budgets"]["entries_seen"] == 10_000
    assert result["diagnostics"][0]["code"] == "entry-limit"


def test_real_cli_enforces_fixed_total_read_budget(tmp_path: Path) -> None:
    block = b"#" + b"x" * (1024 * 1024 - 1)
    for index in range(129):
        (tmp_path / f"f{index:03}.py").write_bytes(block)
    completed, result = _run(tmp_path, timeout=65)
    assert completed.returncode == 1
    assert result["budgets"]["bytes_limit"] == 128 * 1024 * 1024
    assert result["budgets"]["bytes_read"] == 128 * 1024 * 1024
    assert "total-read-limit" in {item["code"] for item in result["diagnostics"]}


def test_real_cli_enforces_fixed_ast_node_budget(tmp_path: Path) -> None:
    values = ",".join(["0"] * 450_000)
    source = f"x=({values})\n"
    for index in range(5):
        (tmp_path / f"f{index}.py").write_text(source)
    completed, result = _run(tmp_path, timeout=65)
    assert completed.returncode == 1
    assert result["budgets"]["ast_nodes_limit"] == 2_000_000
    assert result["budgets"]["ast_nodes"] > 2_000_000
    assert "ast-node-limit" in {item["code"] for item in result["diagnostics"]}


def test_real_cli_enforces_fixed_definition_budget(tmp_path: Path) -> None:
    source = "".join(f"def f{index}(): return {index}\n"
                     for index in range(20_001))
    (tmp_path / "functions.py").write_text(source)
    completed, result = _run(tmp_path)
    assert completed.returncode == 1
    assert result["budgets"]["symbols_limit"] == 20_000
    assert "symbol-limit" in {item["code"] for item in result["diagnostics"]}


def test_real_cli_enforces_fixed_neighbor_comparison_budget(tmp_path: Path) -> None:
    source = "".join(f"def f{index}(): return {index}\n"
                     for index in range(1_415))
    (tmp_path / "functions.py").write_text(source)
    completed, result = _run(tmp_path, "--release", timeout=65)
    assert completed.returncode == 0
    assert result["status"] == "complete"
    assert result["budgets"]["comparisons_limit"] == 1_000_000
    assert result["sampling"]["population"] == 1_000_405
    assert result["sampling"]["compared"] == 1_000_000
    assert result["sampling"]["unsampled"] == 405


def test_real_cli_rejects_changed_path_escape(tmp_path: Path) -> None:
    completed, result = _run(tmp_path, "--changed", "../outside.py")
    assert completed.returncode == 2
    assert result["status"] == "incomplete"
    assert result["diagnostics"][0]["code"] == "invalid-changed-path"


def test_installed_copy_is_identical_and_runs(tmp_path: Path) -> None:
    from bootstrap.scaffold import _MODULE_MAPPINGS, create_dev_tree, install_modules

    mapping = {spec.dst: spec for spec in _MODULE_MAPPINGS["architecture-review"]}
    assert mapping["tools/code_map.py"].src == "team-gated/code_map.py"
    assert mapping["tools/code_map.py"].verbatim is True
    create_dev_tree(tmp_path)
    install_modules(ROOT / "templates", tmp_path, {}, ["architecture-review"])
    installed = tmp_path / "tools" / "code_map.py"
    assert installed.read_bytes() == TEMPLATE_SCRIPT.read_bytes()
    rubric = tmp_path / "dev" / "architecture_review.md"
    frame = rubric.read_text(encoding="utf-8")
    assert sum(line.startswith("### ") for line in frame.splitlines()) == 5
    for contract in ("regular-file reading", "terminal", "Legacy:", "New:",
                     "Mixed:", "Adequate practice", "## Release assessment"):
        assert contract in frame
    rubric_edit = frame + "\nProject-specific normalization boundary.\n"
    rubric.write_text(rubric_edit, encoding="utf-8")
    edited = installed.read_bytes() + b"\n# adopter edit\n"
    installed.write_bytes(edited)
    install_modules(ROOT / "templates", tmp_path, {}, ["architecture-review"])
    assert installed.read_bytes() == edited
    assert rubric.read_text(encoding="utf-8") == rubric_edit
    target = tmp_path / "fixture"
    target.mkdir()
    (target / "api.py").write_text("def answer(): return 42\n")
    completed, result = _run(target, script=installed)
    assert completed.returncode == 0
    assert result["files"][0]["public"][0]["name"] == "answer"


@pytest.mark.skipif(os.name != "posix", reason="POSIX descriptor-relative walk")
def test_race_substituting_a_file_for_a_link_is_refused(tmp_path: Path) -> None:
    body = """
import os,sys
from pathlib import Path
root=Path(sys.argv[2]); (root/'source.py').write_text('def safe(): pass\\n')
fd=ns['_open_absolute_directory'](str(root))
before=os.stat('source.py',dir_fd=fd,follow_symlinks=False)
(root/'source.py').unlink(); (root/'source.py').symlink_to(root/'elsewhere.py')
try:
    ns['_read_at'](fd,'source.py',before,4096)
except OSError:
    print('refused')
else:
    print('followed')
finally:
    os.close(fd)
"""
    completed = _internal(SCRIPT, body, str(tmp_path))
    assert completed.returncode == 0
    assert completed.stdout.strip() == b"refused"


@pytest.mark.skipif(os.name != "posix", reason="POSIX descriptor-relative walk")
def test_interrupted_reads_count_against_total_budget(tmp_path: Path) -> None:
    for name in ("a.py", "b.py", "c.py"):
        (tmp_path / name).write_bytes(b"x" * 100)
    body = """
import json,os,sys
root=sys.argv[2]; original=os.read; calls=0; actual=0
def interrupted(fd, size):
    global calls, actual
    calls+=1
    if calls % 2 == 0: raise OSError('interrupted read')
    chunk=original(fd,size); actual+=len(chunk); return chunk
os.read=interrupted; ns['MAX_TOTAL_READ']=150
fd=ns['_open_absolute_directory'](root)
try: result=ns['_walk'](fd,root,{'changed':[],'release':False})
finally: os.close(fd)
print(json.dumps({'actual':actual,'result':result}))
"""
    completed = _internal(SCRIPT, body, str(tmp_path))
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout)
    assert observed["actual"] == 100
    assert observed["result"]["budgets"]["bytes_read"] == 100
    assert "total-read-limit" in {d["code"] for d in observed["result"]["diagnostics"]}


def test_symbol_limit_reports_already_counted_ast_nodes(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("def first(): pass\ndef second(): pass\n")
    body = """
import json,os,sys
root=sys.argv[2]; ns['MAX_SYMBOLS']=1
fd=ns['_open_absolute_directory'](root)
try: result=ns['_walk'](fd,root,{'changed':[],'release':False})
finally: os.close(fd)
print(json.dumps(result))
"""
    completed = _internal(SCRIPT, body, str(tmp_path))
    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout)
    assert "symbol-limit" in {d["code"] for d in result["diagnostics"]}
    assert result["budgets"]["ast_nodes"] > 0


def test_unsupported_platform_branch_is_explicit_not_a_fallback(
    tmp_path: Path,
) -> None:
    body = """
import json,sys
ns['_secure_walk_available']=lambda:False
sys.argv=['code_map','--_scan-worker',json.dumps({'root':sys.argv[2],'changed':[],'release':False})]
raise SystemExit(ns['_scan_worker']())
"""
    completed = _internal(SCRIPT, body, str(tmp_path))
    assert completed.returncode == 1
    result = json.loads(completed.stdout.decode("ascii"))
    assert result["status"] == "incomplete"
    assert result["diagnostics"][0]["code"] == "secure-traversal-unavailable"
    assert "no weaker fallback" in result["diagnostics"][0]["remedy"]


@pytest.mark.parametrize("limit_name,fixture_kind,expected", [
    ("MAX_ENTRIES", "entries", "entry-limit"),
    ("MAX_TOTAL_READ", "total-read", "total-read-limit"),
    ("MAX_AST_NODES", "ast-nodes", "ast-node-limit"),
    ("MAX_SYMBOLS", "symbols", "symbol-limit"),
    ("MAX_COMPARISONS", "comparisons", "truncated"),
])
def test_fixed_budget_paths_with_small_test_controls(
    tmp_path: Path,
    limit_name: str, fixture_kind: str, expected: str,
) -> None:
    """Exercise each budget's real scan/compare logic with reduced test limits."""
    limits = {"MAX_ENTRIES": 100, "MAX_TOTAL_READ": 4096,
              "MAX_SOURCE": 4096, "MAX_AST_NODES": 1000,
              "MAX_SYMBOLS": 100, "MAX_COMPARISONS": 100,
              "PARSER_SECONDS": 2.0}
    if fixture_kind == "entries":
        limits["MAX_ENTRIES"] = 3
    elif fixture_kind == "total-read":
        limits["MAX_TOTAL_READ"] = 16
    elif fixture_kind == "ast-nodes":
        limits["MAX_AST_NODES"] = 8
    elif fixture_kind == "symbols":
        limits["MAX_SYMBOLS"] = 1
    elif fixture_kind == "comparisons":
        limits["MAX_COMPARISONS"] = 1
    if fixture_kind == "entries":
        for name in ("a", "b", "c", "d"):
            (tmp_path / name).write_text("")
    elif fixture_kind == "total-read":
        (tmp_path / "a.py").write_text("#123456789\n")
        (tmp_path / "b.py").write_text("#123456789\n")
    elif fixture_kind == "ast-nodes":
        (tmp_path / "a.py").write_text("x = 1 + 2 + 3 + 4\n")
    elif fixture_kind == "symbols":
        (tmp_path / "a.py").write_text("def first(): pass\ndef second(): pass\n")
    else:
        (tmp_path / "a.py").write_text(
            "".join(f"def f{i}(): return {i}\n" for i in range(4)))
    body = """
import json,os,sys
cfg=json.loads(sys.argv[3])
for name,value in cfg['limits'].items(): ns[name]=value
root=sys.argv[2]; fd=ns['_open_absolute_directory'](root)
try: result=ns['_walk'](fd,root,cfg['args'])
finally: os.close(fd)
print(json.dumps(result))
"""
    config = {"limits": limits, "args": {
        "root": str(tmp_path), "changed": [],
        "release": fixture_kind == "comparisons",
    }}
    completed = _internal(SCRIPT, body, str(tmp_path),
                          json.dumps(config))
    assert completed.returncode == 0, completed.stderr.decode("ascii", "replace")
    result = json.loads(completed.stdout.decode("ascii"))
    if fixture_kind == "comparisons":
        assert result["sampling"]["truncated"] is True
        assert result["sampling"]["unsampled"] > 0
    else:
        assert expected in {item["code"] for item in result["diagnostics"]}


@pytest.mark.parametrize("file_count", [1, 3])
def test_parser_deadline_marks_only_remaining_files_incomplete(
    tmp_path: Path, file_count: int,
) -> None:
    for index in range(file_count):
        (tmp_path / f"{index}.py").write_text("def example(): pass\n")
    body = """
import json,os,sys
root=sys.argv[2]; parse=ns['_parse_file']; clock=ns['time'].monotonic
def expire_after_parse(*args):
    result=parse(*args)
    ns['time'].monotonic=lambda: clock()+100
    return result
ns['_parse_file']=expire_after_parse
fd=ns['_open_absolute_directory'](root)
try: result=ns['_walk'](fd,root,{'changed':[],'release':False})
finally: os.close(fd)
print(json.dumps(result))
"""
    completed = _internal(SCRIPT, body, str(tmp_path))
    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout)
    assert result["files"][0]["analysis"] == "parsed"
    if file_count == 1:
        assert result["status"] == "complete"
        assert result["diagnostics"] == []
    else:
        assert result["status"] == "incomplete"
        assert [row["analysis"] for row in result["files"]] == [
            "parsed", "incomplete", "incomplete"]
        assert {item["path"] for item in result["diagnostics"]} == {"1.py", "2.py"}
        assert result["diagnostics"][0]["code"] == "parser-total-time-limit"


def test_parser_and_command_deadlines_are_interruptible(
    tmp_path: Path,
) -> None:
    body = """
import json,subprocess,sys
ns['COMMAND_SECONDS']=0.001
data=b'x = '+b'('*20000+b'1'+b')'*20000
try: ns['_parse_file'](data,2000000,20000,0.001)
except subprocess.TimeoutExpired: print('parser-terminated')
sys.stdout.flush()
ns['_supervise_scan']({'root':sys.argv[2],'changed':[],'release':False})
"""
    completed = _internal(SCRIPT, body, str(tmp_path), timeout=10)
    assert completed.returncode == 0
    output = completed.stdout.decode("ascii").splitlines()
    assert output[0] == "parser-terminated"
    result = json.loads(output[-1])
    assert result["diagnostics"][0]["code"] == "command-time-limit"
