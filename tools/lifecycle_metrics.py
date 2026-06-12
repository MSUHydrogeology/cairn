#!/usr/bin/env python3
"""Thin launcher over the `_lifecycle_metrics` engine package."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_CANONICAL = "tools._lifecycle_metrics"
_TOOL_PATH = Path(__file__).resolve()


def _load_engine():
    tool_dir = _TOOL_PATH.parent
    engine_dir = tool_dir / "_lifecycle_metrics"
    engine_init = engine_dir / "__init__.py"
    if not engine_init.is_file():
        raise RuntimeError(
            f"lifecycle_metrics engine package not found at {engine_dir} — refusing to run "
            f"(the _lifecycle_metrics/ package must be installed beside lifecycle_metrics.py)"
        )
    # Fail-closed containment (parity with bootstrap/scaffold.py's launcher): the
    # engine must be a REAL directory inside this file's own directory — refuse a
    # symlinked or out-of-tree _lifecycle_metrics/, and never trust sys.path.
    if (engine_dir.is_symlink() or engine_init.is_symlink()
            or engine_dir.resolve().parent != tool_dir.resolve()):
        raise RuntimeError(
            f"lifecycle_metrics engine package at {engine_dir} is a symlink or resolves "
            f"outside {tool_dir} — refusing to load (fail-closed)"
        )
    # Idempotent + poison-free (Codex cross-phase F#4): reuse a FULLY-LOADED
    # cached canonical package, and on ANY exec failure remove the parent + every
    # canonical child this load registered, so a later retry rebuilds a clean
    # module graph instead of reusing a stale submodule (the mixed-graph the
    # repository's loader prototype already forecloses).
    cached = sys.modules.get(_CANONICAL)
    if cached is not None and getattr(cached, "__cairn_loaded__", False):
        return cached
    spec = importlib.util.spec_from_file_location(
        _CANONICAL, engine_init, submodule_search_locations=[str(engine_dir)],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not build an import spec for {engine_init}")
    engine = importlib.util.module_from_spec(spec)
    sys.modules[_CANONICAL] = engine
    try:
        spec.loader.exec_module(engine)
    except BaseException:
        for _name in [n for n in sys.modules
                      if n == _CANONICAL or n.startswith(_CANONICAL + ".")]:
            sys.modules.pop(_name, None)
        raise
    engine.__cairn_loaded__ = True
    return engine


_engine = _load_engine()

# Full-namespace re-export: every public AND test-accessed private engine symbol
# becomes an attribute of THIS module, so `import`, `helper.X`, `vars(mod)`, and
# `dir(mod)` resolve unchanged through the launcher.
globals().update({k: v for k, v in vars(_engine).items() if not k.startswith("__")})


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())  # noqa: F821  (main re-exported from the engine above)
