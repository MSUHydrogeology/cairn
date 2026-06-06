"""Stage 8 — the extracted cli module (`bootstrap/_scaffold/cli.py`).

Contracts:

* **Top layer, downward-only dependencies** — `cli` imports only the stdlib and the
  subsystems below it; nothing in the package imports `cli` except the engine
  __init__'s re-export, and no submodule imports it (no cycle).
* **Single identity** — `main` / `build_arg_parser` resolve to the one `cli` object
  across the engine and the `bootstrap.scaffold` facade, and the launcher path
  (`_engine.main()`) reaches it.
* **`--help` text preserved** — `build_arg_parser`'s ``description=__doc__`` uses
  cli's module docstring, which carries the original scaffold help text, so the CLI
  help description is unchanged by the split. (The engine __init__ docstring was
  retitled to an engine-package description at Stage 9, so the two are now
  intentionally distinct.)
* **Engine is a pure facade** — after Stage 8 the engine __init__ defines no
  functions/classes of its own; it is a prologue + re-export surface.

Stdlib only.
"""
from __future__ import annotations

import ast
from pathlib import Path

_PKG = Path(__file__).resolve().parents[1] / "_scaffold"


def _import_modules(pyfile: str) -> set[str]:
    mods: set[str] = set()
    for node in ast.walk(ast.parse(Path(pyfile).read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module)
        if isinstance(node, ast.Import):
            mods.update(a.name for a in node.names)
    return mods


def test_cli_depends_only_downward():
    from bootstrap._scaffold import cli as CLI  # noqa: PLC0415

    allowed = {"config", "security", "merge", "slotmerge", "lockfile", "install", "upgrade"}
    for node in ast.walk(ast.parse(Path(CLI.__file__).read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if node.level > 0:
                assert mod in allowed, f"cli imports sideways/up: .{mod}"
            else:
                assert not mod.startswith("bootstrap"), f"cli imports {mod!r}"


def test_no_submodule_imports_cli():
    for low in ("config", "security", "merge", "slotmerge", "lockfile", "install", "upgrade"):
        mods = _import_modules(str(_PKG / f"{low}.py"))
        assert not any(m.endswith("cli") for m in mods), f"{low} imports cli (cycle)"


def test_single_identity_and_launcher_reach():
    import sys  # noqa: PLC0415

    from bootstrap._scaffold import cli as CLI  # noqa: PLC0415
    import bootstrap._scaffold as engine  # noqa: PLC0415
    import bootstrap.scaffold  # noqa: PLC0415  (facade == engine)

    facade = sys.modules["bootstrap.scaffold"]
    for name in ("main", "build_arg_parser"):
        obj = getattr(CLI, name)
        assert getattr(engine, name) is obj, f"engine.{name} is not the cli object"
        assert getattr(facade, name) is obj, f"facade.{name} is not the cli object"
    # the launcher entry point reaches main
    assert callable(engine.main)


def test_help_description_is_preserved():
    from bootstrap._scaffold import cli as CLI  # noqa: PLC0415
    import bootstrap._scaffold as engine  # noqa: PLC0415

    # The parser description is cli's own module docstring (description=__doc__) ...
    parser = CLI.build_arg_parser()
    assert parser.description == CLI.__doc__, "--help description drifted from cli.__doc__"
    # ... and that docstring carries the original scaffold help text (unchanged by
    # the split), not the engine-package description the facade now exposes.
    assert "Cairn bootstrap mechanical scaffold" in CLI.__doc__
    assert "Config YAML format" in CLI.__doc__
    assert CLI.__doc__ != engine.__doc__, (
        "cli help text and the engine-package docstring are intentionally distinct "
        "after the Stage-9 retitle"
    )


def test_engine_init_is_a_pure_facade():
    # No business logic left in the engine __init__: it is a prologue + re-exports.
    tree = ast.parse((_PKG / "__init__.py").read_text(encoding="utf-8"))
    fns = [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    classes = [n.name for n in tree.body if isinstance(n, ast.ClassDef)]
    assert fns == [], f"engine __init__ still defines functions: {fns}"
    assert classes == [], f"engine __init__ still defines classes: {classes}"
