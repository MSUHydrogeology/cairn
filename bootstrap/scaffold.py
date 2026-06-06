#!/usr/bin/env python3
"""Scaffold launcher + facade — scaffold-split 0B (RR1 / SR1 / P1#3).

The scaffold *engine* (install / upgrade / 3-way merge / lockfile / containment)
lives in the private package ``bootstrap/_scaffold/``. This module is the **thin
launcher and public facade**: every existing entry point — ``from
bootstrap.scaffold import main`` / ``read_lockfile`` / ``_MODULE_MAPPINGS`` / …,
``from bootstrap import scaffold as s; s.X``, and ``python bootstrap/scaffold.py
…`` — keeps working unchanged.

Security boundary (SR1)
-----------------------
``bootstrap/`` is a **namespace package** (no ``__init__.py``), so plain
``import bootstrap._scaffold`` would trust ``sys.path``. The launcher defends the
launcher load path:

1. **File-relative, fail-closed parent load.** The engine package is loaded from
   a directory computed next to *this* file, never via ``sys.path``, and refused
   if it resolves outside the Cairn root.
2. **Verified canonical cache.** A pre-existing ``sys.modules["bootstrap._scaffold"]``
   is accepted only if its ``__file__`` / ``__path__`` match the expected engine
   (a hostile ``sitecustomize`` preload is refused), and its cached child
   namespace is re-validated through the engine guard.
3. **Clean failure.** If init fails, every newly-added ``bootstrap._scaffold`` /
   ``bootstrap._scaffold.*`` entry is removed so a retry starts clean.

The **engine submodule** boundary — every ``bootstrap._scaffold.<child>`` import,
including the **direct** imports Stages 4/5 and the canonical-identity contract
use — is owned by ``bootstrap/_scaffold/_guard.py``, which the engine ``__init__``
installs as its first action (it necessarily runs before any child resolves,
launcher path or direct). See that module.

Identity + patch-through (P1#3 / RR5/R6): the launcher makes ``bootstrap.scaffold``
**the same object** as ``bootstrap._scaffold`` (``sys.modules[__name__] = engine``)
— one identity per file, the full public surface present by construction, and
patch-through for free.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_CANONICAL = "bootstrap._scaffold"


class ScaffoldLoaderError(RuntimeError):
    """Fail-closed launcher rejection (SR1): the engine package is missing, a
    pre-existing canonical cache entry does not match the expected engine, or a
    path escapes the Cairn root."""


def _verify_within_root(path: Path, cairn_root: Path) -> Path:
    resolved = path.resolve()
    root = cairn_root.resolve()
    if resolved != root and root not in resolved.parents:
        raise ScaffoldLoaderError(
            f"engine path {resolved} escapes the Cairn root {root} — refusing "
            f"to load (fail-closed, SR1)"
        )
    return resolved


def _verify_cached_engine(cached, engine_init: Path, engine_dir: Path) -> None:
    """A pre-existing ``bootstrap._scaffold`` must match the expected engine
    (``__file__`` and search locations) — a hostile preload must not satisfy the
    canonical name (F1)."""
    cached_file = getattr(cached, "__file__", None)
    if cached_file is None or Path(cached_file).resolve() != engine_init.resolve():
        raise ScaffoldLoaderError(
            f"a module named {_CANONICAL!r} is already loaded from {cached_file!r}, "
            f"not the expected engine {engine_init} — refusing (preload hijack, SR1/F1)"
        )
    search = [Path(p).resolve() for p in getattr(cached, "__path__", []) or []]
    if search != [engine_dir.resolve()]:
        raise ScaffoldLoaderError(
            f"the loaded {_CANONICAL!r} has unexpected search locations {search} "
            f"(expected [{engine_dir.resolve()}]) — refusing (SR1/F1)"
        )


def _revalidate_cached_namespace(cached, engine_dir: Path, cairn_root: Path) -> None:
    """Re-run the engine guard over a cached engine so a child preloaded *after*
    the parent (the polluted-cached-child route, re-review R1) is refused and the
    finder is present."""
    guard = getattr(cached, "_install_engine_guard", None)
    if guard is None:
        raise ScaffoldLoaderError(
            f"cached {_CANONICAL!r} has no import guard — refusing (SR1/R1)"
        )
    guard(engine_dir, cairn_root)


def _load_engine():
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

    cached = sys.modules.get(_CANONICAL)
    if cached is not None:
        _verify_cached_engine(cached, engine_init, engine_dir)
        _revalidate_cached_namespace(cached, engine_dir, cairn_root)
        return cached

    spec = importlib.util.spec_from_file_location(
        _CANONICAL, engine_init, submodule_search_locations=[str(engine_dir)],
    )
    if spec is None or spec.loader is None:
        raise ScaffoldLoaderError(f"could not build an import spec for {engine_init}")
    engine = importlib.util.module_from_spec(spec)

    # F4: snapshot the canonical namespace so a failed init leaves no residue --
    # neither the parent nor any child imported before the failure.
    before = {k for k in sys.modules if k == _CANONICAL or k.startswith(_CANONICAL + ".")}
    sys.modules[_CANONICAL] = engine
    try:
        spec.loader.exec_module(engine)   # the engine __init__ installs the guard
        _verify_within_root(Path(engine.__file__), cairn_root)
    except BaseException:
        for key in [
            k for k in list(sys.modules)
            if (k == _CANONICAL or k.startswith(_CANONICAL + ".")) and k not in before
        ]:
            sys.modules.pop(key, None)
        raise
    return engine


_engine = _load_engine()

if __name__ == "__main__":
    sys.exit(_engine.main())
else:
    # Facade: bootstrap.scaffold IS the engine object (single identity +
    # patch-through). Must be the last statement.
    sys.modules[__name__] = _engine
