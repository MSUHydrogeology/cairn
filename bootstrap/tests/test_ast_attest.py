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


def test_committed_baseline_accounted_for_across_the_engine_package():
    # The pre-split baseline is the FIXED reference for the whole split: every
    # baselined symbol must remain present, exactly once, with an unchanged
    # digest, across the engine module set as extraction proceeds (symbols leave
    # __init__ and land in security.py / etc. -- pure motion). Before any
    # extraction this is just __init__.py; mid-extraction it is the union. Do NOT
    # re-pin the baseline during extraction -- that would erase the motion
    # reference. Re-pin only deliberately at Stage 0B (already done).
    #
    # If this fails with CHANGED, a symbol's logic changed (regenerate only if
    # intentional, under the canonical interpreter -- lhm / Python 3.13 -- since
    # ast.dump structure varies across minors, C2). MISSING/DUPLICATE => a symbol
    # was dropped or single-source was broken by an extraction.
    assert _BASELINE.is_file(), "the pre-split AST baseline artifact is missing"
    modules = sorted(_SCAFFOLD.parent.glob("*.py"))
    assert A.verify(_BASELINE, modules) == 0, (
        "AST baseline not accounted for across the engine package -- a "
        "non-pure-motion change (CHANGED/MISSING/DUPLICATE) rode an extraction, "
        "or the baseline drifted (regenerate only intentionally, under the "
        "canonical interpreter: lhm env, Python 3.13)."
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


# --- update-symbol: the hardened single-symbol cascade baseline rewrite ----------
# (scaffold six-proposal superplan, pre-run gate-control prerequisite; Antigravity
# R1 + Codex S2). The ONLY legitimate baseline mutation during the cascade is a
# registry mapping symbol gaining an InstallSpec, changing exactly that symbol's
# digest. These pin: rewrites exactly one allowlisted key (others byte-for-byte),
# and every refusal path (non-allowlist, expect-old mismatch, unrelated drift,
# no-change, dry-run) writes nothing.

_MM = "Assign:_MODULE_MAPPINGS"
_SRC_V1 = (
    "_MODULE_MAPPINGS = {'a': 1}\n"
    "_SKILLS_MAPPINGS = (('x', 'y', True),)\n"
    "def helper():\n    return 1\n"
)
_SRC_V2 = (  # only _MODULE_MAPPINGS changed (an InstallSpec added) — the legit cascade delta
    "_MODULE_MAPPINGS = {'a': 1, 'b': 2}\n"
    "_SKILLS_MAPPINGS = (('x', 'y', True),)\n"
    "def helper():\n    return 1\n"
)
_SRC_V3 = (  # _MODULE_MAPPINGS AND helper changed — unrelated drift, must refuse
    "_MODULE_MAPPINGS = {'a': 1, 'b': 2}\n"
    "_SKILLS_MAPPINGS = (('x', 'y', True),)\n"
    "def helper():\n    return 999\n"
)


def _canon_baseline(tmp_path, src, fname="mono.py", bname="base.json"):
    """Write a baseline in the SAME canonical form the committed baseline uses
    (indent=2, sort_keys, trailing newline) so byte-for-byte assertions are real."""
    base = A.digest_module(_write(tmp_path, fname, src))
    bp = tmp_path / bname
    bp.write_text(json.dumps(base, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return bp, base


def test_update_symbol_rewrites_exactly_one_key(tmp_path, capsys):
    bp, base = _canon_baseline(tmp_path, _SRC_V1)
    live = _write(tmp_path, "live.py", _SRC_V2)
    old = base[_MM]["digest"]
    new_expected = A.digest_module(live)[_MM]["digest"]
    assert new_expected != old
    before = json.loads(bp.read_text(encoding="utf-8"))

    assert A.update_symbol(bp, "_MODULE_MAPPINGS", old, [live]) == 0

    after = json.loads(bp.read_text(encoding="utf-8"))
    assert set(before) == set(after), "no key added or dropped"
    for k in before:
        if k == _MM:
            assert after[k]["digest"] == new_expected
            assert after[k]["digest"] != before[k]["digest"]
        else:
            assert after[k] == before[k], f"unrelated key {k} must be untouched"
    # the file stays canonical — only the one digest moved
    assert bp.read_text(encoding="utf-8") == json.dumps(after, indent=2, sort_keys=True) + "\n"
    err = capsys.readouterr().err
    assert "single-symbol update" in err and "WROTE" in err


def test_update_symbol_refuses_non_allowlisted_key(tmp_path):
    bp, base = _canon_baseline(tmp_path, _SRC_V1)
    live = _write(tmp_path, "live.py", _SRC_V3)
    before = bp.read_text(encoding="utf-8")
    assert A.update_symbol(bp, "helper", "whatever", [live]) == 2
    assert bp.read_text(encoding="utf-8") == before  # no write


def test_update_symbol_refuses_on_expect_old_mismatch(tmp_path):
    bp, base = _canon_baseline(tmp_path, _SRC_V1)
    live = _write(tmp_path, "live.py", _SRC_V2)
    before = bp.read_text(encoding="utf-8")
    assert A.update_symbol(bp, "_MODULE_MAPPINGS", "deadbeefdeadbeef", [live]) == 3
    assert bp.read_text(encoding="utf-8") == before  # no write


def test_update_symbol_refuses_on_unrelated_drift(tmp_path):
    bp, base = _canon_baseline(tmp_path, _SRC_V1)
    live = _write(tmp_path, "live.py", _SRC_V3)  # mapping + helper both changed
    old = base[_MM]["digest"]
    before = bp.read_text(encoding="utf-8")
    assert A.update_symbol(bp, "_MODULE_MAPPINGS", old, [live]) == 4
    assert bp.read_text(encoding="utf-8") == before  # no write


def test_update_symbol_refuses_when_unchanged(tmp_path):
    bp, base = _canon_baseline(tmp_path, _SRC_V1)
    live = _write(tmp_path, "live.py", _SRC_V1)  # identical — nothing to update
    old = base[_MM]["digest"]
    before = bp.read_text(encoding="utf-8")
    assert A.update_symbol(bp, "_MODULE_MAPPINGS", old, [live]) == 4
    assert bp.read_text(encoding="utf-8") == before  # no write


def test_update_symbol_dry_run_writes_nothing(tmp_path, capsys):
    bp, base = _canon_baseline(tmp_path, _SRC_V1)
    live = _write(tmp_path, "live.py", _SRC_V2)
    old = base[_MM]["digest"]
    before = bp.read_text(encoding="utf-8")
    assert A.update_symbol(bp, "_MODULE_MAPPINGS", old, [live], dry_run=True) == 0
    assert bp.read_text(encoding="utf-8") == before  # no write
    assert "DRY-RUN" in capsys.readouterr().err


def test_update_symbol_cli_path(tmp_path):
    bp, base = _canon_baseline(tmp_path, _SRC_V1)
    live = _write(tmp_path, "live.py", _SRC_V2)
    old = base[_MM]["digest"]
    rc = A.main(["update-symbol", "_MODULE_MAPPINGS", "--baseline", str(bp),
                 "--expect-old", old, str(live)])
    assert rc == 0
    after = json.loads(bp.read_text(encoding="utf-8"))
    assert after[_MM]["digest"] == A.digest_module(live)[_MM]["digest"]


# Codex confirmation R2-2 Finding 1: a mapping update must NOT bless a brand-new
# top-level symbol (an injected gate-bypass) riding alongside the legit mapping change.
_SRC_INJECT = (  # _MODULE_MAPPINGS changed PLUS a new top-level function
    "_MODULE_MAPPINGS = {'a': 1, 'b': 2}\n"
    "_SKILLS_MAPPINGS = (('x', 'y', True),)\n"
    "def helper():\n    return 1\n"
    "def injected_gate_bypass():\n    return True\n"
)


def test_update_symbol_refuses_injected_new_symbol_strict(tmp_path, capsys):
    bp, base = _canon_baseline(tmp_path, _SRC_V1)
    live = _write(tmp_path, "live.py", _SRC_INJECT)
    old = base[_MM]["digest"]
    before = bp.read_text(encoding="utf-8")
    # strict (no known_new): the injected function refuses, no write
    assert A.update_symbol(bp, "_MODULE_MAPPINGS", old, [live]) == 4
    assert bp.read_text(encoding="utf-8") == before
    assert "new top-level symbol" in capsys.readouterr().err


def test_update_symbol_allows_only_pinned_known_new(tmp_path):
    # The real cascade carries pre-existing facade re-exports; a known-new allowlist
    # that contains exactly those lets the one-mapping update proceed, while an
    # UNPINNED new symbol still refuses.
    bp, base = _canon_baseline(tmp_path, _SRC_V1)
    old = base[_MM]["digest"]
    # (a) the injected symbol IS in known_new -> allowed, writes
    live_a = _write(tmp_path, "a.py", _SRC_INJECT)
    assert A.update_symbol(bp, "_MODULE_MAPPINGS", old, [live_a],
                           known_new={"FunctionDef:injected_gate_bypass"}) == 0
    assert json.loads(bp.read_text())[_MM]["digest"] == A.digest_module(live_a)[_MM]["digest"]
    # (b) a DIFFERENT new symbol, not in known_new -> refuses, no write
    bp2, base2 = _canon_baseline(tmp_path, _SRC_V1, bname="base2.json")
    live_b = _write(tmp_path, "b.py", _SRC_INJECT)
    before2 = bp2.read_text(encoding="utf-8")
    assert A.update_symbol(bp2, "_MODULE_MAPPINGS", base2[_MM]["digest"], [live_b],
                           known_new={"FunctionDef:some_other_reexport"}) == 4
    assert bp2.read_text(encoding="utf-8") == before2
