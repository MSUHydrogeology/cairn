"""Real-entry checks for the bounded, filesystem-only architecture map.

Promises:
- The map lists files, symbols and unsupported languages under a root, and never executes the Python it inspects.
- Output escapes control characters in names and paths, and reports the sampling of changed and release neighbours.
- The command runs in isolated Python mode and ignores planted project and adjacent modules.
- The map refuses symbolic links, named pipes and a linked root.
- Malformed, deeply nested and oversized sources are reported as diagnostics, not as a crash.
- Fixed budgets for entries, bytes read, syntax nodes, definitions and neighbour comparisons are enforced and reported.
- Per-file, total and whole-command parser deadlines are enforced and mark the remaining files incomplete.
- The installed copy of the map is byte-identical to the shipped one and runs.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
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


def _collector_with_test_limits(
    directory: Path, *, parser_subprocess_delay: float = 0.0,
    **limits: float,
) -> Path:
    """Copy trusted collector bytes and scale only fixed budgets for CLI tests."""
    source = SCRIPT.read_text(encoding="utf-8")
    defaults = {
        "PER_FILE_SECONDS": "5.0",
        "PARSER_SECONDS": "30.0",
        "COMMAND_SECONDS": "60.0",
    }
    for name, value in limits.items():
        assert name in defaults
        old = f"{name} = {defaults[name]}"
        assert source.count(old) == 1
        source = source.replace(old, f"{name} = {value!r}")
    if parser_subprocess_delay:
        entrypoint = 'if __name__ == "__main__":'
        assert source.count(entrypoint) == 1
        delay_wrapper = (
            "_test_subprocess_run = subprocess.run\n"
            "def _subprocess_run_with_test_delay(*args, **kwargs):\n"
            "    result = _test_subprocess_run(*args, **kwargs)\n"
            f"    time.sleep({parser_subprocess_delay!r})\n"
            "    return result\n"
            "subprocess.run = _subprocess_run_with_test_delay\n\n"
        )
        source = source.replace(entrypoint, delay_wrapper + entrypoint)
    copied = directory / "code_map.py"
    copied.write_text(source, encoding="utf-8")
    return copied


def _internal(script: Path, body: str, *args: str,
              timeout: float = 65.0) -> subprocess.CompletedProcess[bytes]:
    runner = (
        "import importlib.util,sys\n"
        "spec=importlib.util.spec_from_file_location('code_map_test',sys.argv[1])\n"
        "ns=importlib.util.module_from_spec(spec)\n"
        "sys.modules[spec.name]=ns; spec.loader.exec_module(ns); ns=ns.__dict__\n"
        "def walk_root(root,args):\n"
        "    if ns['os'].name=='nt':\n"
        "        api=ns['_WindowsAPI'](); ns['_WINDOWS_WORKER_JOB']=api.install_worker_job()\n"
        "        handles,_fs=api.admit_root(root)\n"
        "        try: return ns['_walk'](handles[-1],root,args,ns['_WindowsFilesystem'](api))\n"
        "        finally:\n"
        "            for handle in reversed(handles): api.close(handle)\n"
        "    fd=ns['_open_absolute_directory'](root)\n"
        "    try: return ns['_walk'](fd,root,args)\n"
        "    finally: ns['os'].close(fd)\n"
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
    (tmp_path / "\x7fhostile.py").write_text(payload, encoding="utf-8")
    completed, result = _run(tmp_path)
    assert completed.returncode == 0
    assert not marker.exists()
    assert b"\x7f" not in completed.stdout
    assert "\\u007f" in completed.stdout.decode("ascii")
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


def test_real_cli_refuses_links(tmp_path: Path) -> None:
    (tmp_path / "real").mkdir()
    (tmp_path / "real" / "source.py").write_text("def kept(): pass\n")
    (tmp_path / "linked-dir").symlink_to(tmp_path / "real", target_is_directory=True)
    (tmp_path / "linked.py").symlink_to(tmp_path / "real" / "source.py")
    completed, result = _run(tmp_path)
    assert completed.returncode == 1
    assert result["status"] == "incomplete"
    codes = {item["code"] for item in result["diagnostics"]}
    assert "linked-entry" in codes
    assert "source.py" not in [row["path"] for row in result["files"]]


@pytest.mark.skipif(os.name != "posix", reason="POSIX FIFO")
def test_real_cli_refuses_fifo(tmp_path: Path) -> None:
    (tmp_path / "real").mkdir()
    (tmp_path / "real" / "source.py").write_text("def kept(): pass\n")
    assert hasattr(os, "mkfifo"), "the POSIX FIFO fixture requires os.mkfifo"
    os.mkfifo(tmp_path / "pipe.py")
    completed, result = _run(tmp_path)
    assert completed.returncode == 1
    assert result["status"] == "incomplete"
    codes = {item["code"] for item in result["diagnostics"]}
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
    frame = rubric.read_bytes()
    template_rubric = (
        ROOT / "templates" / "modules" / "team-gated"
        / "architecture_review_template.md"
    )
    assert frame == template_rubric.read_bytes()
    rubric_edit = frame + b"\nProject-specific normalization boundary.\n"
    rubric.write_bytes(rubric_edit)
    edited = installed.read_bytes() + b"\n# adopter edit\n"
    installed.write_bytes(edited)
    install_modules(ROOT / "templates", tmp_path, {}, ["architecture-review"])
    assert installed.read_bytes() == edited
    assert rubric.read_bytes() == rubric_edit
    target = tmp_path / "fixture"
    target.mkdir()
    (target / "api.py").write_text("def answer(): return 42\n")
    completed, result = _run(target, script=installed)
    assert completed.returncode == 0
    assert result["files"][0]["public"][0]["name"] == "answer"


# Declared exception (internal hook): Hook: child calls internal _read_at after the test swaps a file for a link; the race cannot be timed through the public CLI.
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


# Declared exception (internal hook): Hook: child patches os.read to interrupt reads through the _internal runner; interruption needs an internal hook.
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
result=walk_root(root,{'changed':[],'release':False})
print(json.dumps({'actual':actual,'result':result}))
"""
    completed = _internal(SCRIPT, body, str(tmp_path))
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout)
    assert observed["actual"] == 100
    assert observed["result"]["budgets"]["bytes_read"] == 100
    assert "total-read-limit" in {d["code"] for d in observed["result"]["diagnostics"]}


# Declared exception (internal hook): Hook: child process calls internal walk and read helpers (_walk, _read_at, _parse_file or similar) via the _internal runner; no public route to this s.
def test_symbol_limit_reports_already_counted_ast_nodes(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("def first(): pass\ndef second(): pass\n")
    body = """
import json,os,sys
root=sys.argv[2]; ns['MAX_SYMBOLS']=1
result=walk_root(root,{'changed':[],'release':False})
print(json.dumps(result))
"""
    completed = _internal(SCRIPT, body, str(tmp_path))
    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout)
    assert "symbol-limit" in {d["code"] for d in result["diagnostics"]}
    assert result["budgets"]["ast_nodes"] > 0


# Declared exception (internal hook): Hook: child process calls internal walk and read helpers (_walk, _read_at, _parse_file or similar) via the _internal runner; no public route to this s.
def test_unsupported_platform_branch_is_explicit_not_a_fallback(
    tmp_path: Path,
) -> None:
    body = """
import json,sys
ns['_secure_walk_available']=lambda:False
ns['os'].name='posix'
sys.argv=['code_map','--_scan-worker',json.dumps({'root':sys.argv[2],'changed':[],'release':False})]
raise SystemExit(ns['_scan_worker']())
"""
    completed = _internal(SCRIPT, body, str(tmp_path))
    assert completed.returncode == 1
    result = json.loads(completed.stdout.decode("ascii"))
    assert result["status"] == "incomplete"
    assert result["diagnostics"][0]["code"] == "secure-traversal-unavailable"
    assert "no weaker fallback" in result["diagnostics"][0]["remedy"]


# Declared exception (internal hook): Hook: internal Windows directory decoder called with malformed buffers through the _internal runner; no public route.
def test_windows_directory_decoder_rejects_malformed_buffers_portably(
    tmp_path: Path,
) -> None:
    body = r"""
import json,struct,sys
def row(name, *, next_offset=0, length=None, attributes=0):
    encoded=name.encode('utf-16-le')
    header=struct.pack('<II6qIIIbx24s2xq', next_offset,0,0,0,0,0,0,0,
                       attributes,len(encoded) if length is None else length,
                       0,0,b'\0'*24,7)
    return header+encoded
decode=ns['_decode_windows_entries']
valid=row('part.py')
assert decode(valid)[0]['name']=='part.py'
bad=[b'',valid[:100],row('part.py',length=3),row('part.py',length=512),
     row('part.py',next_offset=8),row('part.py',next_offset=113),
     row('part.py',next_offset=65536),row('..\\escape'),row('x:stream'),
     row('x\0y'),row('')]
refused=0
for raw in bad:
    try: decode(raw)
    except ns['_WindowsUnavailable']: refused+=1
    else: raise AssertionError('malformed-buffer-accepted')
print(json.dumps({'valid':'part.py','malformed_refused':refused}))
"""
    completed = _internal(SCRIPT, body, str(tmp_path))
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout) == {
        "valid": "part.py", "malformed_refused": 11,
    }


@pytest.mark.skipif(os.name != "nt", reason="native Windows NTFS traversal")
def test_windows_native_cli_modes_succeed_with_job_and_do_not_execute_targets(
    tmp_path: Path,
) -> None:
    marker = tmp_path / "target-executed"
    (tmp_path / "changed.py").write_text(
        f"import pathlib\npathlib.Path({str(marker)!r}).touch()\n"
        "def route_data(source):\n    return source.value\n", encoding="utf-8")
    (tmp_path / "neighbor.py").write_text(
        "def route_value(source):\n    return source.value\n", encoding="utf-8")
    (tmp_path / "readme.md").write_text("Synthetic fixture only.\n", encoding="utf-8")
    completed, mapped = _run(tmp_path)
    assert completed.returncode == 0, completed.stderr
    assert mapped["status"] == "complete"
    assert mapped["budgets"]["entries_seen"] == 3
    assert {row["analysis"] for row in mapped["files"]} == {"parsed", "unsupported"}
    completed, changed = _run(tmp_path, "--changed", "changed.py")
    assert completed.returncode == 0, completed.stderr
    assert changed["status"] == "complete"
    assert changed["sampling"]["population"] == 1
    assert changed["neighbors"][0]["neighbors"][0]["path"] == "neighbor.py"
    assert not marker.exists()


@pytest.mark.skipif(os.name != "nt", reason="native Windows NTFS source budget")
def test_windows_native_cli_enforces_per_source_budget(tmp_path: Path) -> None:
    (tmp_path / "large.py").write_bytes(b"#" + b"x" * (1024 * 1024))
    completed, result = _run(tmp_path)
    assert completed.returncode == 1
    assert result["status"] == "incomplete"
    assert result["budgets"]["source_limit"] == 1024 * 1024
    assert result["budgets"]["bytes_read"] == 0
    assert "source-limit" in {item["code"] for item in result["diagnostics"]}


@pytest.mark.skipif(os.name != "nt", reason="native Windows Job object")
def test_windows_native_worker_job_kills_child_on_forced_timeout(
    tmp_path: Path,
) -> None:
    import ctypes as C
    from ctypes import wintypes as W

    handshake = tmp_path / "child-pid"
    runner = (
        "import importlib.util,subprocess,sys,time\n"
        "from pathlib import Path\n"
        "spec=importlib.util.spec_from_file_location('code_map_job_test',sys.argv[1])\n"
        "ns=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ns;spec.loader.exec_module(ns);ns=ns.__dict__\n"
        "api=ns['_WindowsAPI']();ns['_WINDOWS_WORKER_JOB']=api.install_worker_job()\n"
        "child=subprocess.Popen([sys.executable,'-I','-c','import time;time.sleep(60)'],"
        "stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\n"
        "Path(sys.argv[2]).write_text(str(child.pid),encoding='ascii');time.sleep(60)\n"
    )
    worker = subprocess.Popen(
        [sys.executable, "-I", "-c", runner, str(SCRIPT), str(handshake)],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    kernel = C.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
    kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
    kernel.OpenProcess.restype = C.c_void_p
    kernel.WaitForSingleObject.argtypes = [C.c_void_p, W.DWORD]
    kernel.WaitForSingleObject.restype = W.DWORD
    kernel.TerminateProcess.argtypes = [C.c_void_p, W.UINT]
    kernel.TerminateProcess.restype = W.BOOL
    kernel.CloseHandle.argtypes = [C.c_void_p]
    kernel.CloseHandle.restype = W.BOOL
    child_handle = None
    try:
        import time
        deadline = time.monotonic() + 5
        while not handshake.exists():
            if worker.poll() is not None or time.monotonic() >= deadline:
                raise AssertionError("job worker did not publish child PID")
            time.sleep(0.01)
        child_pid = int(handshake.read_text(encoding="ascii"))
        child_handle = kernel.OpenProcess(0x00100000, False, child_pid)
        assert child_handle
        assert kernel.WaitForSingleObject(child_handle, 0) == 258
        worker.kill()  # Same direct worker termination used at the outer timeout.
        worker.communicate(timeout=5)
        assert kernel.WaitForSingleObject(child_handle, 5000) == 0
    finally:
        if worker.poll() is None:
            worker.kill()
            worker.communicate(timeout=5)
        if child_handle:
            if kernel.WaitForSingleObject(child_handle, 0) == 258:
                kernel.TerminateProcess(child_handle, 1)
                kernel.WaitForSingleObject(child_handle, 5000)
            kernel.CloseHandle(child_handle)


# Declared exception (internal hook): Hook: child calls internal _WindowsAPI and _walk to hold a reparse parent; reparse points cannot be created portably.
@pytest.mark.skipif(os.name != "nt", reason="native Windows NTFS reparse controls")
def test_windows_native_cli_refuses_reparse_entries_and_held_reparse_parent(
    tmp_path: Path,
) -> None:
    import ctypes as C
    from ctypes import wintypes as W
    import struct

    kernel = C.WinDLL("kernel32.dll", winmode=0x800, use_last_error=True)
    kernel.CreateFileW.argtypes = [W.LPCWSTR, W.DWORD, W.DWORD, C.c_void_p,
                                  W.DWORD, W.DWORD, C.c_void_p]
    kernel.CreateFileW.restype = C.c_void_p
    kernel.DeviceIoControl.argtypes = [C.c_void_p, W.DWORD, C.c_void_p, W.DWORD,
                                       C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.c_void_p]
    kernel.DeviceIoControl.restype = W.BOOL
    kernel.CloseHandle.argtypes = [C.c_void_p]
    kernel.CloseHandle.restype = W.BOOL
    invalid = C.c_void_p(-1).value

    completed, unsupported = _run(Path("\\\\?\\C:\\"))
    assert completed.returncode == 2
    assert unsupported["status"] == "incomplete"
    assert unsupported["diagnostics"][0]["message"] == "unsupported-root-form"

    def reparse_control(path: Path, target: Path | None) -> None:
        handle = kernel.CreateFileW(
            str(path), 0x100, 7, None, 3, 0x02000000 | 0x00200000, None)
        assert handle and handle != invalid, C.get_last_error()
        try:
            tag = 0xA0000003
            if target is None:
                data = struct.pack("<IHH", tag, 0, 0)
                control = 0x900AC
            else:
                substitute = ("\\??\\" + str(target)).encode("utf-16-le")
                printable = str(target).encode("utf-16-le")
                names = substitute + b"\0\0" + printable + b"\0\0"
                body = struct.pack("<HHHH", 0, len(substitute),
                                   len(substitute) + 2, len(printable)) + names
                data = struct.pack("<IHH", tag, len(body), 0) + body
                control = 0x900A4
            buffer = C.create_string_buffer(data)
            returned = W.DWORD()
            assert kernel.DeviceIoControl(handle, control, buffer, len(data),
                                          None, 0, C.byref(returned), None), C.get_last_error()
        finally:
            kernel.CloseHandle(handle)

    root = tmp_path / "scan"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (root / "inside.py").write_text("def inside(): return 1\n", encoding="utf-8")
    (outside / "outside.py").write_text("def outside(): return 2\n", encoding="utf-8")
    junction = root / "jump"
    junction.mkdir()
    reparse_control(junction, outside)
    try:
        completed, root_result = _run(junction)
        assert completed.returncode == 2
        assert root_result["status"] == "incomplete"
        assert root_result["diagnostics"][0]["code"] == "root-open"
        completed, result = _run(root)
        assert completed.returncode == 1
        assert result["status"] == "incomplete"
        assert "linked-entry" in {item["code"] for item in result["diagnostics"]}
        assert "outside.py" not in {item["path"] for item in result["files"]}
    finally:
        reparse_control(junction, None)
        junction.rmdir()

    held = tmp_path / "held-parent"
    held.mkdir()
    (held / "identity.py").write_text("def present(): return 1\n", encoding="utf-8")
    body = r"""
import ctypes as C,json,os,sys,struct
from ctypes import wintypes as W
kernel=C.WinDLL('kernel32.dll',winmode=0x800,use_last_error=True)
kernel.CreateFileW.argtypes=[W.LPCWSTR,W.DWORD,W.DWORD,C.c_void_p,W.DWORD,W.DWORD,C.c_void_p]
kernel.CreateFileW.restype=C.c_void_p
kernel.DeviceIoControl.argtypes=[C.c_void_p,W.DWORD,C.c_void_p,W.DWORD,C.c_void_p,W.DWORD,C.POINTER(W.DWORD),C.c_void_p]
kernel.DeviceIoControl.restype=W.BOOL
kernel.CloseHandle.argtypes=[C.c_void_p]
def set_link(path,target):
    h=kernel.CreateFileW(path,0x100,7,None,3,0x02000000|0x00200000,None)
    assert h and h!=C.c_void_p(-1).value,C.get_last_error()
    try:
        tag=0xA0000003
        if target is None: raw=struct.pack('<IHH',tag,0,0); code=0x900AC
        else:
            sub=('\\??\\'+target).encode('utf-16-le'); printable=target.encode('utf-16-le')
            names=sub+b'\0\0'+printable+b'\0\0'
            body=struct.pack('<HHHH',0,len(sub),len(sub)+2,len(printable))+names
            raw=struct.pack('<IHH',tag,len(body),0)+body; code=0x900A4
        buf=C.create_string_buffer(raw); out=W.DWORD()
        assert kernel.DeviceIoControl(h,code,buf,len(raw),None,0,C.byref(out),None),C.get_last_error()
    finally: kernel.CloseHandle(h)
api=ns['_WindowsAPI'](); handles,_=api.admit_root(sys.argv[2])
rows=api.enumerate(handles[-1],10)
entry=next(row for row in rows if row['name']=='identity.py')
wrong=dict(entry,file_id=entry['file_id']^1)
try: api.open_child(handles[-1],wrong)
except ns['_WindowsUnavailable'] as exc:
    assert 'enumerated-identity-or-type-changed' in str(exc)
else: raise AssertionError('enumerated-identity-mismatch-accepted')
for handle in reversed(handles): api.close(handle)
handles=[]
os.unlink(os.path.join(sys.argv[2],'identity.py'))
handles,_=api.admit_root(sys.argv[2])
set_link(sys.argv[2],sys.argv[3])
try:
    try: api.enumerate(handles[-1],10)
    except ns['_WindowsUnavailable'] as exc:
        assert 'reparse-or-device' in str(exc)
        print(json.dumps({'identity_mismatch_refused':True,'held_parent_refused':True}))
    else: raise AssertionError('converted-parent-followed')
finally:
    try: set_link(sys.argv[2],None)
    finally:
        for handle in reversed(handles): api.close(handle)
"""
    completed = _internal(SCRIPT, body, str(held), str(outside))
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout) == {
        "identity_mismatch_refused": True, "held_parent_refused": True,
    }


# Declared exception (internal hook): Hook: child process calls internal walk and read helpers (_walk, _read_at, _parse_file or similar) via the _internal runner; no public route to this s.
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
root=sys.argv[2]; result=walk_root(root,cfg['args'])
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


# Declared exception (internal hook): Hook: child replaces internal _parse_file and time.monotonic to expire the parser deadline; not reachable in test time publicly.
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
result=walk_root(root,{'changed':[],'release':False})
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


# Declared exception (internal hook): Hook: child process calls internal walk and read helpers (_walk, _read_at, _parse_file or similar) via the _internal runner; no public route to this s.
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


# Declared exception (internal hook): Hook: _collector_with_test_limits copies the trusted script with scaled budget constants; production budgets cannot be reached in test time.
def test_public_cli_enforces_per_file_parser_deadline(tmp_path: Path) -> None:
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    marker = fixture / "executed"
    body = (f"import pathlib\npathlib.Path({str(marker)!r}).touch()\n"
            + "".join(f"value_{index} = {index}\n" for index in range(30_000)))
    (fixture / "large.py").write_text(body, encoding="utf-8")
    collector_dir = tmp_path / "collector"
    collector_dir.mkdir()
    fast_timeout = _collector_with_test_limits(
        collector_dir, PER_FILE_SECONDS=0.001, COMMAND_SECONDS=10.0)
    completed, result = _run(fixture, script=fast_timeout, timeout=15)
    assert completed.returncode == 1
    assert result["status"] == "incomplete"
    assert result["files"][0]["analysis"] == "incomplete"
    assert "parser-file-time-limit" in {
        item["code"] for item in result["diagnostics"]}
    assert not marker.exists()

    positive = _collector_with_test_limits(
        collector_dir, PER_FILE_SECONDS=10.0, COMMAND_SECONDS=30.0)
    completed, result = _run(fixture, script=positive, timeout=35)
    assert completed.returncode == 0
    assert result["status"] == "complete"
    assert result["files"][0]["analysis"] == "parsed"
    assert not marker.exists()


# Declared exception (internal hook): Hook: _collector_with_test_limits copies the trusted script with scaled budget constants; production budgets cannot be reached in test time.
def test_public_cli_enforces_total_parser_deadline(tmp_path: Path) -> None:
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    for index in range(2):
        (fixture / f"{index:02}.py").write_text(
            "def sample():\n    return 1\n", encoding="utf-8")
    collector_dir = tmp_path / "collector"
    collector_dir.mkdir()
    bounded = _collector_with_test_limits(
        collector_dir, PER_FILE_SECONDS=5.0, PARSER_SECONDS=0.5,
        COMMAND_SECONDS=10.0, parser_subprocess_delay=0.75)
    completed, result = _run(fixture, script=bounded, timeout=15)
    assert completed.returncode == 1
    assert result["status"] == "incomplete"
    assert any(row["analysis"] == "parsed" for row in result["files"])
    assert "parser-total-time-limit" in {
        item["code"] for item in result["diagnostics"]}
    assert "parser-file-time-limit" not in {
        item["code"] for item in result["diagnostics"]}

    positive = _collector_with_test_limits(
        collector_dir, PER_FILE_SECONDS=5.0, PARSER_SECONDS=5.0,
        COMMAND_SECONDS=30.0)
    completed, result = _run(fixture, script=positive, timeout=35)
    assert completed.returncode == 0
    assert result["status"] == "complete"
    assert all(row["analysis"] == "parsed" for row in result["files"])


# Declared exception (internal hook): Hook: _collector_with_test_limits copies the trusted script with scaled budget constants; production budgets cannot be reached in test time.
def test_public_cli_enforces_whole_command_deadline(tmp_path: Path) -> None:
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    marker = fixture / "executed"
    body = (f"import pathlib\npathlib.Path({str(marker)!r}).touch()\n"
            + "value = 1\n" * 80_000)
    (fixture / "large.py").write_text(body, encoding="utf-8")
    collector_dir = tmp_path / "collector"
    collector_dir.mkdir()
    bounded = _collector_with_test_limits(
        collector_dir, PER_FILE_SECONDS=10.0, PARSER_SECONDS=20.0,
        COMMAND_SECONDS=0.2)
    completed, result = _run(fixture, script=bounded, timeout=10)
    assert completed.returncode == 1
    assert result["status"] == "incomplete"
    assert "command-time-limit" in {
        item["code"] for item in result["diagnostics"]}
    assert result["files"] == []
    assert not marker.exists()

    positive = _collector_with_test_limits(
        collector_dir, PER_FILE_SECONDS=10.0, PARSER_SECONDS=20.0,
        COMMAND_SECONDS=30.0)
    completed, result = _run(fixture, script=positive, timeout=35)
    assert completed.returncode == 0
    assert result["status"] == "complete"
    assert result["files"][0]["analysis"] == "parsed"
    assert not marker.exists()
