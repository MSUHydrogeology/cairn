#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Progressive-onboarding activation helper — thin launcher/facade over the owned
``_onboarding/`` package.

The onboarding engine (slot/preset parse, trigger evaluation,
active-surfacing prompt rendering, the activation core, and the write-containment
guards ``_assert_safe_write`` / ``_assert_safe_read`` / ``_assert_safe_dir_for_glob``)
lives in the private sibling package ``_onboarding/``. This file is the thin
launcher + full-namespace facade: every existing entry point keeps working —
``python scripts/onboarding_activate.py`` (the goodnight CLI), ``import``, and the
adopter test-suite's in-process ``_load_helper`` attribute access to public and
test-accessed private symbols.

Launcher: ``importlib.util`` dynamic spec-loader; the engine is registered under
the canonical name ``scripts._onboarding`` and its complete namespace is
re-exported via ``globals().update``. Loaded **fail-closed**: the engine must be a
real directory inside this file's own directory, never a symlink or out-of-tree
path (parity with ``bootstrap/scaffold.py``'s launcher; never trusts ``sys.path``).
No ``__setattr__`` forwarder is installed — unlike the intent tool, the onboarding
test-suite does not monkeypatch engine internals, so a plain namespace copy suffices.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_CANONICAL = "scripts._onboarding"
_TOOL_PATH = Path(__file__).resolve()


def _load_engine():
    tool_dir = _TOOL_PATH.parent
    engine_dir = tool_dir / "_onboarding"
    engine_init = engine_dir / "__init__.py"
    if not engine_init.is_file():
        raise RuntimeError(
            f"onboarding engine package not found at {engine_dir} — refusing to run "
            f"(the _onboarding/ package must be installed beside onboarding_activate.py)"
        )
    # Fail-closed containment (parity with bootstrap/scaffold.py's launcher): the
    # engine must be a REAL directory inside this file's own directory — refuse a
    # symlinked or out-of-tree _onboarding/, and never trust sys.path.
    if (engine_dir.is_symlink() or engine_init.is_symlink()
            or engine_dir.resolve().parent != tool_dir.resolve()):
        raise RuntimeError(
            f"onboarding engine package at {engine_dir} is a symlink or resolves "
            f"outside {tool_dir} — refusing to load (fail-closed)"
        )
    # Idempotent + poison-free: reuse a FULLY-LOADED
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
