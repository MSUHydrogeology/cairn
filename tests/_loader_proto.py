#!/usr/bin/env python3
"""Fail-closed file-relative engine loader.

**Prototype, not yet wired as production** (it is wired into the launcher at
Stage 0B). It exists now so the *contract* — one canonical identity per file,
loaded file-relative and fail-closed against import hijack — is pinned and
tested on the substrate *before* any privileged code moves.

Why a bespoke loader at all
---------------------------
``bootstrap/`` is a **namespace package** (no ``__init__.py``), so an attacker
who lands a ``bootstrap/`` earlier on ``sys.path`` (a hostile ``PYTHONPATH``)
can shadow the engine. A plain ``import
bootstrap._scaffold`` trusts ``sys.path`` resolution; this loader does **not**.
It loads the engine package from a **verified absolute directory** computed
relative to the launcher's own ``__file__`` (the stable on-disk location), and
**fails closed** if any module it loads resolves to a path outside the Cairn
root (``ScaffoldLoaderError``). ``sys.path`` is never consulted for engine
resolution, so a decoy ``bootstrap/`` on the path cannot hijack it.

Canonical identity
------------------
The engine is registered under the single canonical name ``bootstrap._scaffold``
in ``sys.modules``; ``load_engine`` is **idempotent** — a second call returns the
same object. That guarantees **one ``sys.modules`` entry / one object identity
per implementation file** no matter how the engine is reached (abs-path launcher,
``from bootstrap.scaffold import X`` facade, ``import bootstrap._scaffold.<m>``),
so the engine's mutable singletons are never duplicated into divergent copies.

This module is stdlib-only and import-pure (defining it loads nothing, writes
nothing, consults no ``sys.path``).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


class ScaffoldLoaderError(RuntimeError):
    """Fail-closed loader rejection: the engine package is missing/malformed,
    or a module it loads resolves to a path outside the Cairn root (import hijack)."""


def _verify_within_root(path: Path, cairn_root: Path) -> Path:
    """Return ``path`` resolved, or raise if it escapes ``cairn_root``.

    The fail-closed core: a loaded engine module whose real on-disk path is
    not under the Cairn root is refused — that is precisely the import-hijack /
    symlink-escape signature."""
    resolved = path.resolve()
    root = cairn_root.resolve()
    if resolved != root and root not in resolved.parents:
        raise ScaffoldLoaderError(
            f"engine module {resolved} escapes the Cairn root {root} — "
            f"refusing to load (fail-closed, SR1)"
        )
    return resolved


def load_engine(
    package_dir: str | Path,
    cairn_root: str | Path,
    canonical_name: str = "bootstrap._scaffold",
) -> ModuleType:
    """Load the engine package at ``package_dir`` under ``canonical_name``.

    File-relative (``package_dir`` is an absolute directory, never resolved via
    ``sys.path``) and fail-closed (every loaded file is verified within
    ``cairn_root``). **Idempotent**: if ``canonical_name`` is already loaded, the
    existing object is returned — one identity per file."""
    package_dir = Path(package_dir)
    cairn_root = Path(cairn_root)

    cached = sys.modules.get(canonical_name)
    if cached is not None:
        return cached

    init = package_dir / "__init__.py"
    if not init.is_file():
        raise ScaffoldLoaderError(
            f"engine package has no __init__.py at {package_dir} — refusing to load"
        )
    verified_init = _verify_within_root(init, cairn_root)
    verified_dir = _verify_within_root(package_dir, cairn_root)

    spec = importlib.util.spec_from_file_location(
        canonical_name,
        verified_init,
        submodule_search_locations=[str(verified_dir)],
    )
    if spec is None or spec.loader is None:
        raise ScaffoldLoaderError(f"could not build an import spec for {verified_init}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[canonical_name] = module
    try:
        spec.loader.exec_module(module)
        # Post-exec: the package's own __file__ must still be within root.
        _verify_within_root(Path(module.__file__), cairn_root)
    except BaseException:
        # Never leave a half-initialized canonical entry behind.
        sys.modules.pop(canonical_name, None)
        raise
    return module


def load_submodule(
    submodule: str,
    package_dir: str | Path,
    cairn_root: str | Path,
    canonical_name: str = "bootstrap._scaffold",
) -> ModuleType:
    """Load ``<canonical_name>.<submodule>`` from ``<package_dir>/<submodule>.py``,
    file-relative and fail-closed, under the same canonical namespace. Idempotent."""
    full = f"{canonical_name}.{submodule}"
    cached = sys.modules.get(full)
    if cached is not None:
        return cached

    # Fail closed if the parent package is not yet initialized:
    # a submodule's package-relative imports (``from . import config``) resolve
    # against the registered parent in sys.modules, so exec'ing it first would
    # raise an opaque import-time error. Require load_engine() first.
    if canonical_name not in sys.modules:
        raise ScaffoldLoaderError(
            f"cannot load submodule {full!r}: parent package {canonical_name!r} "
            f"is not initialized -- call load_engine() first (a submodule's "
            f"package-relative imports resolve against the registered parent)"
        )

    path = _verify_within_root(Path(package_dir) / f"{submodule}.py", cairn_root)
    if not path.is_file():
        raise ScaffoldLoaderError(f"engine submodule not found: {path}")

    spec = importlib.util.spec_from_file_location(full, path)
    if spec is None or spec.loader is None:
        raise ScaffoldLoaderError(f"could not build an import spec for {path}")

    mod = importlib.util.module_from_spec(spec)
    sys.modules[full] = mod
    try:
        spec.loader.exec_module(mod)
        _verify_within_root(Path(mod.__file__), cairn_root)
    except BaseException:
        sys.modules.pop(full, None)
        raise
    return mod
