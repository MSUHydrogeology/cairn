#!/usr/bin/env python3
"""Scaffold launcher + facade — scaffold-split 0B (RR1 / SR1 / P1#3).

The scaffold *engine* (install / upgrade / 3-way merge / lockfile / containment)
lives in the private package ``bootstrap/_scaffold/``. This module is the **thin
launcher and public facade**: every existing entry point — ``from
bootstrap.scaffold import main`` / ``read_lockfile`` / ``_MODULE_MAPPINGS`` / …,
``from bootstrap import scaffold as s; s.X``, and ``python bootstrap/scaffold.py
…`` — keeps working unchanged.

Security boundary (SR1) — three defenses, all *before* untrusted code runs
-------------------------------------------------------------------------
``bootstrap/`` is a **namespace package** (no ``__init__.py``), so plain
``import bootstrap._scaffold`` would trust ``sys.path`` — a hostile
``PYTHONPATH`` could shadow the engine (the S1 import-hijack). The launcher:

1. **Loads the engine file-relative and fail-closed.** The engine package is
   loaded from a directory computed next to *this* file, never via ``sys.path``,
   and refused if it resolves outside the Cairn root.
2. **Verifies any pre-existing canonical cache entry just as strictly.** Python
   imports ``sitecustomize`` before the launcher runs, so a hostile path could
   *preload* ``sys.modules["bootstrap._scaffold"]`` with a decoy. Returning the
   cache blindly would call the attacker's ``main()``; instead the cached
   module's ``__file__`` / ``__path__`` must match the expected engine, or it is
   refused (substrate Security Review F1).
3. **Mediates every engine submodule import through a verifying finder.** A
   ``from . import security`` would otherwise be resolved by the default path
   machinery, which *follows a submodule symlink and executes the outside
   target* before any check. ``_EngineFinder`` resolves each
   ``bootstrap._scaffold.*`` source, verifies its real path is under the Cairn
   root **before execution**, and fails closed on escape (F2).

If initialization fails, **every** newly-added ``bootstrap._scaffold`` /
``bootstrap._scaffold.*`` entry is removed, so a retry starts from a clean
namespace (F4) — no half-initialized child residue.

Identity + patch-through (P1#3 / RR5/R6)
----------------------------------------
The launcher then makes ``bootstrap.scaffold`` **the same object** as
``bootstrap._scaffold`` (``sys.modules[__name__] = engine``): one ``sys.modules``
entry / one object identity per file, the full public surface present by
construction (no inventory to drift), and patch-through for free — a test that
does ``monkeypatch.setattr(bootstrap.scaffold, "_cairn_is_git", …)`` mutates the
engine's own namespace, so the engine's internal calls see it.

This module is import-pure apart from loading the engine (itself import-pure).
"""
from __future__ import annotations

import importlib.abc
import importlib.util
import sys
from pathlib import Path

_CANONICAL = "bootstrap._scaffold"


class ScaffoldLoaderError(RuntimeError):
    """Fail-closed loader rejection (SR1): the engine package is missing, a
    pre-existing canonical cache entry does not match the expected engine, or a
    module resolves to a path outside the Cairn root (import hijack / symlink
    escape)."""


def _verify_within_root(path: Path, cairn_root: Path) -> Path:
    """Return ``path`` *resolved* (symlinks followed), or raise if its real
    location escapes ``cairn_root``. Resolving first is the point: a symlink
    whose target is outside the root is refused (the escape signature)."""
    resolved = path.resolve()
    root = cairn_root.resolve()
    if resolved != root and root not in resolved.parents:
        raise ScaffoldLoaderError(
            f"engine path {resolved} escapes the Cairn root {root} — refusing "
            f"to load (fail-closed, SR1)"
        )
    return resolved


class _EngineFinder(importlib.abc.MetaPathFinder):
    """A meta-path finder that mediates **every** ``bootstrap._scaffold.<sub>``
    import (F2). It maps the dotted name to a source file under the verified
    engine directory, **resolves and verifies that the real source is within the
    Cairn root before any code runs**, and builds the spec from the verified
    path. A submodule symlinked outside the root is refused (the default path
    machinery would have followed it and executed the target). Installed ahead
    of the default ``PathFinder`` so it wins for the engine namespace."""

    def __init__(self, engine_dir: Path, cairn_root: Path) -> None:
        self._prefix = _CANONICAL + "."
        self._engine_dir = engine_dir.resolve()
        self._cairn_root = cairn_root.resolve()

    def find_spec(self, fullname, path=None, target=None):  # noqa: ARG002
        if not fullname.startswith(self._prefix):
            return None
        suffix = fullname[len(self._prefix):]
        base = self._engine_dir.joinpath(*suffix.split("."))
        # Prefer a package (dir/__init__.py); else a module (<base>.py).
        candidates = [(base / "__init__.py", True), (base.with_suffix(".py"), False)]
        for src, is_pkg in candidates:
            if not src.exists():
                continue
            # Verify the REAL target is within the Cairn root BEFORE execution.
            _verify_within_root(src, self._cairn_root)
            return importlib.util.spec_from_file_location(
                fullname, str(src),
                submodule_search_locations=[str(src.parent)] if is_pkg else None,
            )
        return None  # not an engine module we own; let import fail normally


def _install_engine_finder(engine_dir: Path, cairn_root: Path) -> None:
    """Idempotently install the verifying finder at the front of sys.meta_path."""
    for f in sys.meta_path:
        if isinstance(f, _EngineFinder):
            return
    sys.meta_path.insert(0, _EngineFinder(engine_dir, cairn_root))


def _verify_cached_engine(cached, engine_init: Path, engine_dir: Path) -> None:
    """F1: a pre-existing ``bootstrap._scaffold`` must match the expected engine
    exactly (``__file__`` and package search locations), or be refused — a
    hostile ``sitecustomize`` preload must not satisfy the canonical name."""
    cached_file = getattr(cached, "__file__", None)
    if cached_file is None or Path(cached_file).resolve() != engine_init.resolve():
        raise ScaffoldLoaderError(
            f"a module named {_CANONICAL!r} is already loaded from "
            f"{cached_file!r}, not the expected engine {engine_init} — refusing "
            f"(possible canonical-name preload hijack, SR1/F1)"
        )
    search = [Path(p).resolve() for p in getattr(cached, "__path__", []) or []]
    if search != [engine_dir.resolve()]:
        raise ScaffoldLoaderError(
            f"the loaded {_CANONICAL!r} has unexpected search locations {search} "
            f"(expected [{engine_dir.resolve()}]) — refusing (SR1/F1)"
        )


def _load_engine():
    """Load ``bootstrap/_scaffold`` file-relative + fail-closed, register it
    under the canonical name, install the verifying submodule finder, and return
    it. Idempotent (a verified cache hit is returned)."""
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
        _verify_cached_engine(cached, engine_init, engine_dir)  # raises on mismatch
        _install_engine_finder(engine_dir, cairn_root)
        return cached

    # Mediate submodule imports before the engine init can trigger any.
    _install_engine_finder(engine_dir, cairn_root)

    spec = importlib.util.spec_from_file_location(
        _CANONICAL, engine_init, submodule_search_locations=[str(engine_dir)],
    )
    if spec is None or spec.loader is None:
        raise ScaffoldLoaderError(f"could not build an import spec for {engine_init}")
    engine = importlib.util.module_from_spec(spec)

    # F4: snapshot the canonical namespace so a failed init leaves no residue —
    # neither the parent nor any child module imported before the failure.
    before = {k for k in sys.modules if k == _CANONICAL or k.startswith(_CANONICAL + ".")}
    sys.modules[_CANONICAL] = engine
    try:
        spec.loader.exec_module(engine)
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
    # patch-through). Must be the last statement — nothing after it runs in the
    # launcher namespace once the alias is installed.
    sys.modules[__name__] = _engine
