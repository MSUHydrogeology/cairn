"""Contract for the AST source-motion attestation tool (scaffold-split 0A.4 / SR3).

Pins: the digest is position/comment-insensitive but logic-sensitive; the
committed baseline matches the live `scaffold.py` (a staleness guard — if the
monolith changes before extraction, the baseline must be regenerated); and
`verify` catches CHANGED / MISSING / DUPLICATE symbols (a non-pure-motion edit
riding an extraction commit). Stdlib only.
"""
from __future__ import annotations

import json
from pathlib import Path

from bootstrap.tests import _ast_attest as A

# Post-0B the engine monolith lives in the private package's __init__; the
# attestation reference re-pins here (the launcher bootstrap/scaffold.py is not
# the engine). Stages 1-8 extract submodules from this file.
_REPO = Path(__file__).resolve().parents[2]
_SCAFFOLD = _REPO / "bootstrap" / "_scaffold" / "__init__.py"
_BASELINE = _REPO / "bootstrap" / "tests" / "fixtures" / "scaffold_ast_baseline.json"


def _write(tmp_path, name, body):
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p


def test_digest_is_position_and_comment_insensitive(tmp_path):
    a = _write(tmp_path, "a.py", "def f(x):\n    return x + 1\n")
    b = _write(tmp_path, "b.py", "# a comment\n\n\ndef f(x):\n    return x + 1  # trailing\n")
    assert A.digest_module(a)["FunctionDef:f"]["digest"] == \
        A.digest_module(b)["FunctionDef:f"]["digest"]


def test_digest_detects_a_logic_change(tmp_path):
    a = _write(tmp_path, "a.py", "def f(x):\n    return x + 1\n")
    b = _write(tmp_path, "b.py", "def f(x):\n    return x + 2\n")
    assert A.digest_module(a)["FunctionDef:f"]["digest"] != \
        A.digest_module(b)["FunctionDef:f"]["digest"]


def test_digest_detects_a_default_or_decorator_change(tmp_path):
    a = _write(tmp_path, "a.py", "def f(x, y=1):\n    return x\n")
    b = _write(tmp_path, "b.py", "def f(x, y=2):\n    return x\n")
    assert A.digest_module(a)["FunctionDef:f"]["digest"] != \
        A.digest_module(b)["FunctionDef:f"]["digest"]


def test_committed_baseline_matches_live_scaffold():
    # Staleness guard: the baseline must reflect the CURRENT scaffold.py. If this
    # fails, scaffold.py changed -- regenerate before extraction:
    #   python bootstrap/tests/_ast_attest.py baseline bootstrap/scaffold.py \
    #       > bootstrap/tests/fixtures/scaffold_ast_baseline.json
    assert _BASELINE.is_file(), "the pre-split AST baseline artifact is missing"
    baseline = json.loads(_BASELINE.read_text(encoding="utf-8"))
    live = A.digest_module(_SCAFFOLD)
    live_digests = {k: v["digest"] for k, v in live.items()}
    base_digests = {k: v["digest"] for k, v in baseline.items()}
    assert base_digests == live_digests, (
        "AST baseline is stale vs scaffold.py -- regenerate it before extraction "
        "UNDER THE CANONICAL INTERPRETER (lhm env, Python 3.13): ast.dump structure "
        "varies across Python minor versions, so a baseline pinned on one minor and "
        "verified on another mismatches spuriously (code review C2)."
    )


def test_ast_gate_passes_over_the_full_scaffold_module_set():
    """The EXACT command run between extraction stages: the baseline verified
    against the COMPLETE current ``_scaffold`` module set, not only ``__init__.py``
    (re-review-2 finding 3). Module docstrings recur across modules and must not
    trip single-source; this test fails if the real multi-module gate rots (e.g.
    a new module's docstring re-introducing a DUPLICATE)."""
    modules = sorted(_SCAFFOLD.parent.glob("*.py"))
    assert len(modules) >= 2, f"expected __init__.py + _guard.py at least, got {modules}"
    assert A.verify(_BASELINE, modules) == 0


def test_module_docstrings_do_not_trip_single_source(tmp_path):
    base = A.digest_module(_write(tmp_path, "mono.py", '"""mod."""\ndef f():\n    return 1\n'))
    (tmp_path / "base.json").write_text(json.dumps(base), encoding="utf-8")
    m1 = _write(tmp_path, "m1.py", '"""m1 doc."""\ndef f():\n    return 1\n')
    m2 = _write(tmp_path, "m2.py", '"""m2 doc -- different text."""\n')  # docstring only
    assert A.verify(tmp_path / "base.json", [m1, m2]) == 0


def test_executable_top_level_expression_is_still_single_sourced(tmp_path):
    # The carve-out is docstring-only: a real top-level call duplicated across
    # modules still fails (executable logic, not a docstring).
    base = A.digest_module(_write(tmp_path, "mono.py", "import os\nos.getcwd()\n"))
    (tmp_path / "base.json").write_text(json.dumps(base), encoding="utf-8")
    m1 = _write(tmp_path, "m1.py", "import os\nos.getcwd()\n")
    m2 = _write(tmp_path, "m2.py", "import os\nos.getcwd()\n")  # same exec expr, two files
    assert A.verify(tmp_path / "base.json", [m1, m2]) == 1


def test_pure_motion_across_modules_verifies(tmp_path):
    src = "A = 1\n\ndef f(x):\n    return x\n\nclass C:\n    pass\n"
    base = A.digest_module(_write(tmp_path, "mono.py", src))
    (tmp_path / "base.json").write_text(json.dumps(base), encoding="utf-8")
    # split mono into two modules, bodies unchanged
    m1 = _write(tmp_path, "m1.py", "A = 1\n\ndef f(x):\n    return x\n")
    m2 = _write(tmp_path, "m2.py", "class C:\n    pass\n")
    assert A.verify(tmp_path / "base.json", [m1, m2]) == 0


def test_changed_symbol_fails(tmp_path):
    base = A.digest_module(_write(tmp_path, "mono.py", "def f(x):\n    return x\n"))
    (tmp_path / "base.json").write_text(json.dumps(base), encoding="utf-8")
    moved = _write(tmp_path, "m1.py", "def f(x):\n    return x + 99\n")  # altered
    assert A.verify(tmp_path / "base.json", [moved]) == 1


def test_duplicate_symbol_fails(tmp_path):
    base = A.digest_module(_write(tmp_path, "mono.py", "def f(x):\n    return x\n"))
    (tmp_path / "base.json").write_text(json.dumps(base), encoding="utf-8")
    m1 = _write(tmp_path, "m1.py", "def f(x):\n    return x\n")
    m2 = _write(tmp_path, "m2.py", "def f(x):\n    return x\n")  # same symbol in two files
    assert A.verify(tmp_path / "base.json", [m1, m2]) == 1


def test_shared_imports_across_modules_do_not_fail(tmp_path):
    # Code review C3: the same import recurring across split modules is a
    # per-module necessity, NOT a single-source violation -- it must not
    # DUPLICATE-fail the pure-motion gate. Functions still must move exactly once.
    src = "import sys\nimport os\n\ndef f(x):\n    return x\n"
    base = A.digest_module(_write(tmp_path, "mono.py", src))
    (tmp_path / "base.json").write_text(json.dumps(base), encoding="utf-8")
    m1 = _write(tmp_path, "m1.py", "import sys\nimport os\n\ndef f(x):\n    return x\n")
    m2 = _write(tmp_path, "m2.py", "import sys\nimport os\n")  # imports recur; no symbol
    assert A.verify(tmp_path / "base.json", [m1, m2]) == 0


def test_function_still_duplicate_fails_even_with_shared_imports(tmp_path):
    # The C3 carve-out is imports-only: a real symbol duplicated still fails.
    base = A.digest_module(_write(tmp_path, "mono.py", "import sys\n\ndef f(x):\n    return x\n"))
    (tmp_path / "base.json").write_text(json.dumps(base), encoding="utf-8")
    m1 = _write(tmp_path, "m1.py", "import sys\n\ndef f(x):\n    return x\n")
    m2 = _write(tmp_path, "m2.py", "import sys\n\ndef f(x):\n    return x\n")  # f in two files
    assert A.verify(tmp_path / "base.json", [m1, m2]) == 1


def test_missing_symbol_fails(tmp_path):
    base = A.digest_module(_write(tmp_path, "mono.py", "def f(x):\n    return x\n\ndef g():\n    return 0\n"))
    (tmp_path / "base.json").write_text(json.dumps(base), encoding="utf-8")
    partial = _write(tmp_path, "m1.py", "def f(x):\n    return x\n")  # g dropped
    assert A.verify(tmp_path / "base.json", [partial]) == 1
