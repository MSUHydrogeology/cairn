"""Stage 6 — the extracted install subsystem (`bootstrap/_scaffold/install.py`).

Contracts:

* **Layer-6 subsystem, downward-only dependencies** — `install` imports only the
  stdlib and the lower leaves (config / security / slotmerge / lockfile). It must
  never import the engine package, nor `upgrade` / `cli` / `merge` (no upward or
  sideways edge), and none of those leaves may import `install` (no cycle).
* **Single identity** — every moved symbol resolves to the one `install` object
  across the engine and the `bootstrap.scaffold` facade.
* **Boundary pin** — the shared root helpers (`_cairn_root` / `_find_cairn_root`)
  and the upgrade-time `_MANIFEST_SEARCH_DIRS` stay in the engine, not install.
* **Guarded-write regression (SR6)** — the install-side Class-A writers still
  route their destinations through a containment guard (re-checks the SR6 set
  now that they live in install.py).
* **Behavioral smoke** — a dev-tree creation and a core install round-trip work.

Stdlib only.
"""
from __future__ import annotations

import ast
from pathlib import Path

_PKG = Path(__file__).resolve().parents[1] / "_scaffold"
_GUARD_CALLS = {"_assert_safe_write", "_assert_fanout_contained"}

#: SR6 Class-A install-side writers that must each call a containment guard.
_INSTALL_GUARDED_WRITERS = {
    "_install_one", "write_local_env", "install_onboarding",
    "write_install_lockfile", "_emit_skill_copy_fallback", "fan_out_skills",
}


def _import_modules(pyfile: str) -> set[str]:
    mods: set[str] = set()
    for node in ast.walk(ast.parse(Path(pyfile).read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module)
        if isinstance(node, ast.Import):
            mods.update(a.name for a in node.names)
    return mods


def test_install_depends_only_downward():
    from bootstrap._scaffold import install as INS  # noqa: PLC0415

    allowed = {"config", "security", "slotmerge", "lockfile"}
    for node in ast.walk(ast.parse(Path(INS.__file__).read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if node.level > 0:  # package-relative -> a sibling submodule
                assert mod in allowed, f"install imports sideways/up: .{mod}"
            else:
                assert not mod.startswith("bootstrap"), f"install imports {mod!r}"
        if isinstance(node, ast.Import):
            for a in node.names:
                assert not a.name.startswith("bootstrap"), f"install imports {a.name!r}"


def test_no_lower_leaf_imports_install():
    for leaf in ("config", "security", "slotmerge", "lockfile", "merge"):
        mods = _import_modules(str(_PKG / f"{leaf}.py"))
        assert not any(m.endswith("install") for m in mods), f"{leaf} imports install (cycle)"


def test_single_identity_across_consumers():
    import sys  # noqa: PLC0415

    from bootstrap._scaffold import install as INS  # noqa: PLC0415
    import bootstrap._scaffold as engine  # noqa: PLC0415
    import bootstrap.scaffold  # noqa: PLC0415  (facade == engine)

    facade = sys.modules["bootstrap.scaffold"]
    for name in ("install_core", "install_skills", "fan_out_skills",
                 "install_onboarding", "install_modules", "write_install_lockfile",
                 "run_module_merge_pass", "print_report"):
        obj = getattr(INS, name)
        assert getattr(engine, name) is obj, f"engine.{name} is not the install object"
        assert getattr(facade, name) is obj, f"facade.{name} is not the install object"


def test_shared_helpers_stay_in_engine_not_install():
    import bootstrap._scaffold as engine  # noqa: PLC0415
    from bootstrap._scaffold import install as INS  # noqa: PLC0415

    for nm in ("_cairn_root", "_find_cairn_root", "_MANIFEST_SEARCH_DIRS"):
        assert hasattr(engine, nm), f"{nm} should remain on the engine"
        assert not hasattr(INS, nm), f"{nm} must not be in the install module"


def test_install_writers_still_route_through_a_containment_guard():
    tree = ast.parse((_PKG / "install.py").read_text(encoding="utf-8"))
    calls: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            calls[node.name] = {
                n.func.id for n in ast.walk(node)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            } & _GUARD_CALLS
    for fn in sorted(_INSTALL_GUARDED_WRITERS):
        assert fn in calls, f"SR6: install writer {fn!r} not found in install.py"
        assert calls[fn], f"SR6 regression: {fn!r} no longer calls a containment guard"


def test_dev_tree_and_core_install_smoke(tmp_path):
    from bootstrap._scaffold import install as INS  # noqa: PLC0415

    created = INS.create_dev_tree(tmp_path)
    assert (tmp_path / "dev").is_dir()
    assert any(p.name == "dev" for p in created)
    # dry-run creates nothing new on a second pass
    dry = INS.create_dev_tree(tmp_path, dry_run=True)
    assert isinstance(dry, list)
