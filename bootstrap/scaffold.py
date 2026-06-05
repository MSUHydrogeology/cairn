#!/usr/bin/env python3
"""Scaffold launcher + facade — scaffold-split 0B (RR1 / SR1 / P1#3).

The scaffold *engine* (install / upgrade / 3-way merge / lockfile / containment)
lives in the private package ``bootstrap/_scaffold/``. This module is the **thin
launcher and public facade**: every existing entry point — ``from
bootstrap.scaffold import main`` / ``read_lockfile`` / ``_MODULE_MAPPINGS`` / …,
``from bootstrap import scaffold as s; s.X``, and ``python bootstrap/scaffold.py
…`` — keeps working unchanged.

How it stays safe (SR1) and consistent (P1#3)
---------------------------------------------
``bootstrap/`` is a **namespace package** (no ``__init__.py``), so a plain
``import bootstrap._scaffold`` would trust ``sys.path`` resolution — a hostile
``PYTHONPATH`` could shadow the engine (the S1 import-hijack). Instead this
launcher loads the engine **file-relative**: from a directory computed next to
*this* file, never via ``sys.path``, and **fails closed** if the engine resolves
outside the Cairn root. The package is registered under the single canonical
name ``bootstrap._scaffold``; loading its ``__init__`` with ``__path__`` set to
the verified engine directory means the engine's own package-relative submodule
imports (added as the split proceeds) are equally file-anchored, not
``sys.path``-resolved.

The launcher then makes ``bootstrap.scaffold`` **the same object** as
``bootstrap._scaffold`` (``sys.modules[__name__] = engine``). That is the
strongest form of the facade: one ``sys.modules`` entry / one object identity
per implementation file (P1#3), the full public surface present by construction
(no inventory to drift), and **patch-through for free** — a test that does
``monkeypatch.setattr(bootstrap.scaffold, "_cairn_is_git", …)`` mutates the
engine's own namespace, so the engine's internal calls see it (RR5/R6).

This module is import-pure apart from loading the engine (which is itself
import-pure: it only defines names).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


class ScaffoldLoaderError(RuntimeError):
    """Fail-closed loader rejection (SR1): the engine package is missing, or a
    module it loads resolves to a path outside the Cairn root (import hijack /
    symlink escape)."""


def _verify_within_root(path: Path, cairn_root: Path) -> Path:
    resolved = path.resolve()
    root = cairn_root.resolve()
    if resolved != root and root not in resolved.parents:
        raise ScaffoldLoaderError(
            f"engine path {resolved} escapes the Cairn root {root} — refusing "
            f"to load (fail-closed, SR1)"
        )
    return resolved


def _load_engine():
    """Load ``bootstrap/_scaffold`` file-relative + fail-closed, register it
    under the canonical name ``bootstrap._scaffold``, and return it. Idempotent."""
    canonical = "bootstrap._scaffold"
    cached = sys.modules.get(canonical)
    if cached is not None:
        return cached

    launcher_dir = Path(__file__).resolve().parent           # <cairn>/bootstrap
    cairn_root = launcher_dir.parent                         # <cairn>
    engine_dir = launcher_dir / "_scaffold"
    engine_init = engine_dir / "__init__.py"
    if not engine_init.is_file():
        raise ScaffoldLoaderError(
            f"scaffold engine package not found at {engine_dir} — refusing to load"
        )
    _verify_within_root(engine_dir, cairn_root)
    _verify_within_root(engine_init, cairn_root)

    spec = importlib.util.spec_from_file_location(
        canonical, engine_init, submodule_search_locations=[str(engine_dir)],
    )
    if spec is None or spec.loader is None:
        raise ScaffoldLoaderError(f"could not build an import spec for {engine_init}")
    engine = importlib.util.module_from_spec(spec)
    sys.modules[canonical] = engine
    try:
        spec.loader.exec_module(engine)
        _verify_within_root(Path(engine.__file__), cairn_root)
    except BaseException:
        sys.modules.pop(canonical, None)
        raise
    return engine


_engine = _load_engine()

if __name__ == "__main__":
    sys.exit(_engine.main())
else:
    # Facade: bootstrap.scaffold IS the engine object (single identity +
    # patch-through). Must be the last statement — nothing after it runs in the
    # launcher namespace once the alias is installed.
    sys.modules[__name__] = _engine
