"""Cross-facade loader poison-cleanup regressions (Codex cross-phase finding #4).

Each thin launcher facade (`intent.py`, `lifecycle_metrics.py`) registers its
canonical package in `sys.modules` *before* `exec_module()` (a package `__init__` may import its own submodules by
canonical name). A mid-exec failure must therefore remove the parent **and**
every canonical child it registered, so a later retry rebuilds a clean module
graph instead of reusing a stale submodule. And a fully-loaded canonical package
must be reused idempotently (one object), not re-executed.

These exercise the real facade (loaded from its template location); it loads
unconditionally (the facade is an always-present source artifact).
"""
from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent

FACADES = [
    ("templates/modules/team-gated/intent.py", "tools._intent"),
]


def _load_facade(rel: str):
    path = CAIRN_ROOT / rel
    spec = importlib.util.spec_from_file_location(
        "cairn_facadeprobe_" + Path(rel).stem, path
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)  # runs `_engine = _load_engine()` at module top
    return mod


def _drop_canonical(canonical: str) -> None:
    for n in [n for n in sys.modules
              if n == canonical or n.startswith(canonical + ".")]:
        sys.modules.pop(n, None)


@pytest.mark.parametrize("rel,canonical", FACADES)
def test_facade_load_is_idempotent_one_object(rel, canonical):
    """A fully-loaded canonical package is reused (one object), not re-executed."""
    f = _load_facade(rel)
    a = f._load_engine()
    b = f._load_engine()
    assert a is b is sys.modules[canonical]


@pytest.mark.parametrize("rel,canonical", FACADES)
def test_facade_cleans_poison_on_failed_exec_then_retries_clean(rel, canonical):
    """A mid-exec failure leaves NO canonical parent or child in sys.modules, so a
    retry cannot construct a mixed module graph from a stale submodule."""
    f = _load_facade(rel)
    _drop_canonical(canonical)  # force a real re-exec (not the cached short-circuit)

    real_spec_from = importlib.util.spec_from_file_location

    def boom_spec(name, location, **kw):
        spec = real_spec_from(name, location, **kw)

        def boom(module):
            # Simulate a child registered mid-__init__, then a failure.
            child = canonical + ".shared"
            sys.modules[child] = types.ModuleType(child)
            raise RuntimeError("boom-mid-exec")

        spec.loader.exec_module = boom  # type: ignore[method-assign]
        return spec

    # Patch only for the single _load_engine() call, then restore immediately.
    f.importlib.util.spec_from_file_location = boom_spec
    try:
        with pytest.raises(RuntimeError):
            f._load_engine()
        assert canonical not in sys.modules, "failed load left the parent poisoned"
        assert not any(n.startswith(canonical + ".") for n in sys.modules), \
            "failed load left a canonical child poisoned (mixed-graph risk)"
    finally:
        f.importlib.util.spec_from_file_location = real_spec_from
        # Restore the real, fully-loaded engine for any downstream consumer.
        f._load_engine()
    # Retry from clean: a fresh full load, the real engine, no stale child.
    assert canonical in sys.modules
    assert getattr(sys.modules[canonical], "__cairn_loaded__", False) is True
