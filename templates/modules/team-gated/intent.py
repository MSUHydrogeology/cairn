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

Root resolution (bound contract 3): ``_REPO_ROOT`` / ``INTENTS_LOG_PATH`` and the
launcher path the git hooks must invoke are re-derived from *this* file's install
location (``<repo>/tools/intent.py``) — identical to the pre-split single-file
tool, since the facade sits where the monolith used to — and threaded into the
engine, whose own ``__file__`` is one directory deeper.
"""
from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

_CANONICAL = "tools._intent"
_TOOL_PATH = Path(__file__).resolve()
#: Repo root: this facade installs to ``<repo>/tools/intent.py``, so the repo root
#: is one directory above ``tools/`` — identical to the pre-split single-file tool.
_REPO_ROOT = _TOOL_PATH.parents[1]


def _load_engine():
    engine_dir = _TOOL_PATH.parent / "_intent"
    engine_init = engine_dir / "__init__.py"
    if not engine_init.is_file():
        raise RuntimeError(
            f"intent engine package not found at {engine_dir} — refusing to run "
            f"(the _intent/ package must be installed beside intent.py)"
        )
    spec = importlib.util.spec_from_file_location(
        _CANONICAL, engine_init, submodule_search_locations=[str(engine_dir)],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not build an import spec for {engine_init}")
    engine = importlib.util.module_from_spec(spec)
    # Thread the facade's identity BEFORE exec so the engine resolves the launcher
    # path the git hooks must invoke (read as _FACADE_FILE; see _intent_tool_path).
    engine.__dict__["_FACADE_FILE"] = str(_TOOL_PATH)
    sys.modules[_CANONICAL] = engine
    spec.loader.exec_module(engine)
    # Re-anchor the repo-root-derived constants to THIS install path (the engine
    # computed them from _intent/__init__.py, one directory too deep). Identical
    # values to the pre-split tool, since the facade sits where the monolith was.
    engine._REPO_ROOT = _REPO_ROOT
    engine.INTENTS_LOG_PATH = _REPO_ROOT / "dev" / "intents.jsonl"
    return engine


_engine = _load_engine()

# Full-namespace re-export (bound contract 1): make every public AND test-accessed
# private engine symbol an attribute of THIS module, so `from tools.intent import X`,
# `mod.X`, `vars(mod)`, and `dir(mod)` resolve unchanged.
globals().update({k: v for k, v in vars(_engine).items() if not k.startswith("__")})


class _IntentFacade(types.ModuleType):
    """Facade module type that **forwards attribute writes/deletes to the engine**.

    The pre-split tool was a single module, so the adopter suite monkeypatches a
    private at the module it loads (``monkeypatch.setattr(mod, "_confirm_proceed",
    ...)``) and relies on an *engine-internal* caller (``_precommit_check_impl``)
    seeing it. Post-split, those callers resolve names in the engine module's
    namespace, so a copy-on-the-facade alone would not reach them. Forwarding the
    write to ``_engine`` restores that single-module monkeypatch contract while the
    engine keeps its own canonical identity (``tools._intent``, bound contract 2).
    """

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if not name.startswith("__"):
            setattr(_engine, name, value)

    def __delattr__(self, name):
        super().__delattr__(name)
        if not name.startswith("__") and hasattr(_engine, name):
            delattr(_engine, name)


sys.modules[__name__].__class__ = _IntentFacade


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_engine.main())
