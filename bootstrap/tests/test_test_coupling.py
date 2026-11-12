"""Advisory test-coupling report: which tests reach project internals.

Promises:
- The coupling report lists each test file that reaches project-internal underscore names, with a count, and never runs project code.
- The report lists test files that carry no Promises block.
- Helper modules and conftest files are not reported as coupled tests.
- Test files that cannot be parsed, decoded, or resolved through an out-of-root link are reported as scan failures with escaped paths.
- Advisory mode exits 0; strict mode exits 1 when private reach, missing promise lists or scan failures are reported.
- A failure while scanning one file is reported as a scan failure, not a crash.
"""
from __future__ import annotations

import json
import os
import runpy
import subprocess
import sys
from pathlib import Path


TOOL = Path(__file__).resolve().parents[2] / "scripts" / "test_coupling.py"


def _project(tmp_path: Path, test_source: str = '"""Tests.\n\nPromises:\n- returns a value\n"""\n') -> Path:
    root = tmp_path / "project"
    (root / "tests").mkdir(parents=True)
    (root / "component.py").write_text(
        "from pathlib import Path\nPath('executed').write_text('yes')\n", encoding="utf-8")
    (root / "tests" / "test_unit.py").write_text(test_source, encoding="utf-8")
    return root


def _run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root), *args],
        text=True, capture_output=True, check=False,
    )


def _rows(result: subprocess.CompletedProcess[str]) -> list[dict[str, object]]:
    lines = result.stdout.splitlines()
    start = lines.index("Files, worst first:") + 1
    rows = []
    for line in lines[start:]:
        if line == "Scan failures:":
            break
        if line.startswith("{"):
            rows.append(json.loads(line))
    return rows


def test_resolves_project_aliases_and_private_imports_without_running_project(tmp_path: Path) -> None:
    source = '''"""Tests.\n\nPromises:\n- does work\n"""\nimport component as comp\nfrom component import _hidden as hidden\nfrom namespace_pkg import worker as worker\ncomp._secret()\ncomp.__dunder__()\nhidden()\nworker._secret()\n'''
    root = _project(tmp_path, source)
    namespace = root / "namespace_pkg"
    namespace.mkdir()
    (namespace / "worker.py").write_text(
        "from pathlib import Path\nPath('namespace-executed').write_text('yes')\n",
        encoding="utf-8",
    )
    local = root / "examples" / "minimal"
    local.mkdir(parents=True)
    (local / "water_budget.py").write_text(
        "from pathlib import Path\nPath('local-executed').write_text('yes')\n",
        encoding="utf-8",
    )
    (local / "test_local.py").write_text(
        'import water_budget as budget\n'
        'from water_budget import _hidden as hidden\n'
        'budget._secret()\nhidden()\n',
        encoding="utf-8",
    )
    result = _run(root)
    assert result.returncode == 0
    assert _rows(result) == [
        {"path": "tests/test_unit.py", "private_reach": 3,
         "missing_promises": False},
        {"path": "examples/minimal/test_local.py", "private_reach": 2,
         "missing_promises": True},
    ]
    assert not (root / "executed").exists()
    assert not (root / "namespace-executed").exists()
    assert not (root / "local-executed").exists()
    assert "Refusal tests and hostile-state tests using internal hooks stay" in result.stdout
    assert "Python only" in result.stdout

    cairn_root = TOOL.parent.parent
    sample = _run(cairn_root)
    assert sample.returncode == 0
    example = next(
        row for row in _rows(sample)
        if row["path"] == "examples/scientific-minimal/test_water_budget.py"
    )
    assert example == {
        "path": "examples/scientific-minimal/test_water_budget.py",
        "private_reach": 0,
        "missing_promises": False,
    }


def test_ignores_test_helpers_and_counts_missing_promise_lists(tmp_path: Path) -> None:
    root = _project(
        tmp_path,
        "import test_helper as helper\nimport conftest as fixtures\n"
        "helper._secret()\nfixtures._setup()\n",
    )
    (root / "tests" / "test_helper.py").write_text("def _secret(): pass\n", encoding="utf-8")
    (root / "tests" / "conftest.py").write_text("def _setup(): pass\n", encoding="utf-8")
    result = _run(root, "--strict")
    assert result.returncode == 1
    assert _rows(result)[0]["private_reach"] == 0
    assert _rows(result)[0]["missing_promises"] is True
    assert "tests/test_helper.py" in [row["path"] for row in _rows(result)]


def test_reports_parse_decode_and_out_of_root_link_failures_with_escaped_paths(tmp_path: Path) -> None:
    root = _project(tmp_path)
    weird_name = "test_line\u2028break.py" if os.name == "nt" else "test_line\nbreak.py"
    weird = root / "tests" / weird_name
    weird.write_text("def broken(:\n", encoding="utf-8")
    (root / "tests" / "test_bad_encoding.py").write_bytes(b"\xff")
    outside = tmp_path / "outside.py"
    outside.write_text("pass\n", encoding="utf-8")
    (root / "tests" / "test_escape.py").symlink_to(outside)
    result = _run(root)
    assert result.returncode == 0
    failures = result.stdout.split("Scan failures:\n", 1)[1]
    expected_failure = f"parse:tests/{weird_name}:SyntaxError"
    assert json.dumps(expected_failure, ensure_ascii=True) in failures
    assert '"decode:tests/test_bad_encoding.py:UnicodeDecodeError"' in failures
    assert '"link:tests/test_escape.py"' in failures
    assert outside.read_text(encoding="utf-8") == "pass\n"


def test_strict_mode_fails_for_private_reach_but_advisory_mode_stays_zero(tmp_path: Path) -> None:
    root = _project(tmp_path, '"""Tests.\n\nPromises:\n- promise\n"""\nimport component as c\nc._private()\n')
    assert _run(root).returncode == 0
    strict = _run(root, "--strict")
    assert strict.returncode == 1
    assert _rows(strict)[0]["private_reach"] == 1


# Declared exception (internal hook): injects RecursionError through internal hook _Reach.visit (monkeypatched on a runpy namespace) because no ordinary file overflows the walker; the trai.
def test_reports_recursion_failures_and_tool_has_no_import_execution_mechanism(
    tmp_path: Path, monkeypatch,
) -> None:
    root = _project(tmp_path)
    namespace = runpy.run_path(str(TOOL), run_name="test_coupling_probe")
    monkeypatch.setattr(namespace["_Reach"], "visit", lambda self, tree: (_ for _ in ()).throw(RecursionError()))
    rows, failures = namespace["scan"](root)
    assert rows == []
    assert failures == ["parse:tests/test_unit.py:RecursionError"]
    source = TOOL.read_text(encoding="utf-8")
    assert "importlib" not in source
    assert "find_spec" not in source
    assert "import_module" not in source
    assert "__import__" not in source
