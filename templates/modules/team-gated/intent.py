#!/usr/bin/env python3
"""Work-intent helper — thin launcher/facade over the owned ``_intent/`` package.

The work-intent *engine* (record I/O, identity/session, conflict-check, CLI, and
git-hook install) lives in the private sibling package ``_intent/``. This file is
the **thin launcher and full-namespace facade**: every existing entry point keeps
working unchanged — ``python tools/intent.py …`` (the git hooks + the CLI),
``from tools.intent import …``, and the adopter test-suite's
``_load_tool(intent.py)`` attribute + monkeypatch access to public *and*
test-accessed private symbols.

Launcher (intent-split bound contract 2): the engine is loaded with
``importlib.util`` from a directory computed next to *this* file (never via
``sys.path``) and registered under the single canonical name ``tools._intent``.
The facade then re-exports the engine's complete namespace into its own module
dict via ``globals().update`` — *not* a ``sys.modules[__name__] = engine`` swap,
because the harness's ``_load_tool`` returns the original (pre-swap) module
object, which a swap would leave empty. No ``import _intent`` statement appears
here, so the stdlib-only AST gate sees only stdlib imports.

Root resolution (bound contract 3): the engine's ``shared`` leaf computes
``_REPO_ROOT`` / ``INTENTS_LOG_PATH`` from its own location (``parents[2]`` of
``_intent/shared.py`` resolves to the repo root, identical to the pre-split
single-file tool's ``parents[1]`` from ``tools/intent.py``); the launcher path
the git hooks must invoke is computed file-relative by the engine
(``_intent/hooks.py`` ``_intent_tool_path``). The engine package is loaded
**fail-closed**: it must be a real directory inside this file's own directory,
never a symlink or out-of-tree path (parity with ``bootstrap/scaffold.py``'s
launcher; the loader never trusts ``sys.path``).
"""
from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

_CANONICAL = "tools._intent"
_TOOL_PATH = Path(__file__).resolve()


def _load_engine():
    tool_dir = _TOOL_PATH.parent
    engine_dir = tool_dir / "_intent"
    engine_init = engine_dir / "__init__.py"
    if not engine_init.is_file():
        raise RuntimeError(
            f"intent engine package not found at {engine_dir} — refusing to run "
            f"(the _intent/ package must be installed beside intent.py)"
        )
    # Fail-closed containment (parity with bootstrap/scaffold.py's launcher): the
    # engine must be a REAL directory inside this file's own directory — refuse a
    # symlinked or out-of-tree _intent/, so the loader never executes code from
    # outside the installed tool dir and never trusts sys.path.
    if (engine_dir.is_symlink() or engine_init.is_symlink()
            or engine_dir.resolve().parent != tool_dir.resolve()):
        raise RuntimeError(
            f"intent engine package at {engine_dir} is a symlink or resolves "
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

# Full-namespace re-export (bound contract 1): make every public AND test-accessed
# private engine symbol an attribute of THIS module, so `from tools.intent import X`,
# `mod.X`, `vars(mod)`, and `dir(mod)` resolve unchanged.
globals().update({k: v for k, v in vars(_engine).items() if not k.startswith("__")})


def _engine_modules():
    """The engine package + every loaded ``tools._intent.<sub>`` submodule."""
    prefix = _CANONICAL + "."
    return [m for name, m in list(sys.modules.items())
            if m is not None and (name == _CANONICAL or name.startswith(prefix))]


class _IntentFacade(types.ModuleType):
    """Facade module type that **forwards attribute writes/deletes to the engine**.

    The pre-split tool was a single module, so the adopter suite monkeypatches a
    private at the module it loads (``monkeypatch.setattr(mod, "_confirm_proceed",
    ...)``) and relies on an *engine-internal* caller (``_precommit_check_impl``)
    seeing it. Post-split those callers resolve names in their **own** engine
    submodule's namespace, so a copy on the facade alone would not reach them.
    Forwarding each write to every engine submodule that already binds the name
    restores the single-module monkeypatch contract while each submodule keeps its
    own canonical identity (``tools._intent[.<sub>]``, bound contract 2).
    """

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name.startswith("__"):
            return
        for mod in _engine_modules():
            if hasattr(mod, name):
                setattr(mod, name, value)

    def __delattr__(self, name):
        super().__delattr__(name)
        if name.startswith("__"):
            return
        for mod in _engine_modules():
            if hasattr(mod, name):
                delattr(mod, name)


sys.modules[__name__].__class__ = _IntentFacade


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_engine.main())
