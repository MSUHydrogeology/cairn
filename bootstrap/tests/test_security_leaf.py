"""Stage 1 — the extracted containment leaf (`bootstrap/_scaffold/security.py`).

Two contracts:

* **Guard-routing regression** — every guarded adopter-tree write function still routes its
  destination through a containment guard, so an extraction stage cannot silently
  drop a guard.  The pinned set is Class A of the engine's mutation
  inventory, `bootstrap/_scaffold/SECURITY_MUTATIONS.md`.
* **Single identity** — `ScaffoldSecurityError` is defined exactly once
  (in the leaf) and every consumer (engine, facade) resolves to that one class;
  the two guards likewise resolve to the leaf functions.

Stdlib only.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

_PKG = Path(__file__).resolve().parents[1] / "_scaffold"
_GUARD_CALLS = {"_assert_safe_write", "_assert_fanout_contained"}

#: Class A of `bootstrap/_scaffold/SECURITY_MUTATIONS.md`: functions that
#: perform GUARDED adopter-tree writes.
#: Each must call a containment guard on its destination. Pinned so a later
#: extraction that relocates one without its guard fails this test.
_GUARDED_WRITE_FUNCS = {
    "_install_one",
    "write_local_env",
    "install_onboarding",
    "write_install_lockfile",
    "_emit_skill_copy_fallback",
    "fan_out_skills",
    "_cmd_adopt_module",
    "_apply_upgrade",
    # Module-merge destinations are
    # module-template-controlled, so this write must be guarded too.
    "merge_module_into_slot",
    # Adopt-as-fork: the collision-adoption write
    # path + the shared guarded/atomic lock-and-cache committer.
    "_cmd_adopt_collisions",
    "_commit_lock_and_caches",
}


def _guard_calls_by_function() -> dict[str, set[str]]:
    """Map ``{function_name: {guard names it calls}}`` across the engine package."""
    out: dict[str, set[str]] = {}
    for py in sorted(_PKG.glob("*.py")):
        tree = ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                calls = {
                    n.func.id for n in ast.walk(node)
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                }
                out.setdefault(node.name, set()).update(calls & _GUARD_CALLS)
    return out


def test_guarded_write_functions_still_call_a_containment_guard():
    found = _guard_calls_by_function()
    for fn in sorted(_GUARDED_WRITE_FUNCS):
        assert fn in found, f"SR6: guarded-write function {fn!r} not found in the engine package"
        assert found[fn], (
            f"SR6 regression: {fn!r} no longer calls a containment guard "
            f"({sorted(_GUARD_CALLS)}) -- a guarded adopter-tree write lost its guard"
        )


def test_scaffold_security_error_defined_exactly_once_in_the_leaf():
    defs: list[str] = []
    for py in sorted(_PKG.glob("*.py")):
        for node in ast.walk(ast.parse(py.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ClassDef) and node.name == "ScaffoldSecurityError":
                defs.append(py.name)
    assert defs == ["security.py"], (
        f"ScaffoldSecurityError must be defined exactly once (security.py); found in {defs}"
    )


def test_single_scaffold_security_error_identity_across_consumers():
    from bootstrap._scaffold import security as S  # noqa: PLC0415
    import bootstrap._scaffold as engine  # noqa: PLC0415
    import bootstrap.scaffold  # the facade (== engine)  # noqa: PLC0415

    assert engine.ScaffoldSecurityError is S.ScaffoldSecurityError
    assert sys.modules["bootstrap.scaffold"].ScaffoldSecurityError is S.ScaffoldSecurityError
    # the guards resolve to the leaf functions too
    assert engine._assert_safe_write is S._assert_safe_write
    assert engine._assert_fanout_contained is S._assert_fanout_contained


def test_containment_guard_refuses_a_symlink_escape(tmp_path):
    """The leaf still enforces: a symlinked destination is refused with the one
    ScaffoldSecurityError class."""
    from bootstrap._scaffold import security as S  # noqa: PLC0415
    target = tmp_path / "tgt"
    target.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    trap = target / "AGENTS.md"
    trap.symlink_to(outside / "evil")
    with pytest.raises(S.ScaffoldSecurityError, match="symlinked destination"):
        S._assert_safe_write(trap, target)
    # a normal destination within target is allowed
    S._assert_safe_write(target / "ok.md", target)


def test_security_leaf_is_a_pure_stdlib_leaf():
    """The leaf imports only the stdlib -- it must not import back into the
    engine package (install/upgrade depend on it, never the reverse)."""
    from bootstrap._scaffold import security as S  # noqa: PLC0415
    tree = ast.parse(Path(S.__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            assert not mod.startswith("bootstrap"), f"leaf imports engine module {mod!r}"
            assert node.level == 0, "leaf must not use package-relative imports"
        if isinstance(node, ast.Import):
            for a in node.names:
                assert not a.name.startswith("bootstrap"), f"leaf imports {a.name!r}"
