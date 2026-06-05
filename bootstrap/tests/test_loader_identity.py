"""Contract for the fail-closed file-relative engine loader (scaffold-split 0A.2).

Pins SR1 (fail-closed against import hijack / path escape) and P1#3 (one
canonical ``sys.modules`` identity per implementation file). The loader is a
**prototype** at 0A; these contracts are re-run on the *landed* substrate at
0B.4 (the real launcher + ``_scaffold/`` package). Exercising them now against a
synthetic engine tree proves the design before any privileged code moves.

Stdlib only.
"""
from __future__ import annotations

import sys
import textwrap

import pytest

from bootstrap.tests import _loader_proto as L


@pytest.fixture()
def clean_modules():
    """Snapshot sys.modules and restore it, so a test-loaded engine never leaks
    into the real import system (these names shadow a future bootstrap._scaffold)."""
    before = set(sys.modules)
    try:
        yield
    finally:
        for name in set(sys.modules) - before:
            sys.modules.pop(name, None)


def _write(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(body), encoding="utf-8")
    return path


def _make_engine(root, *, marker="real", state_init="{}"):
    """A throwaway Cairn-root tree: <root>/bootstrap/_scaffold/{__init__,config}.py."""
    pkg = root / "bootstrap" / "_scaffold"
    _write(pkg / "__init__.py", f"""
        MARKER = {marker!r}
        STATE = {state_init}        # a mutable singleton — identity matters
    """)
    _write(pkg / "config.py", """
        VALUE = 42
    """)
    return pkg


def test_loads_under_single_canonical_identity(tmp_path, clean_modules):
    pkg = _make_engine(tmp_path)
    name = "bootstrap._scaffold_t_single"
    mod = L.load_engine(pkg, tmp_path, canonical_name=name)
    assert mod.MARKER == "real"
    assert sys.modules[name] is mod  # exactly one entry, and it IS the returned object


def test_load_engine_is_idempotent_one_object_per_file(tmp_path, clean_modules):
    """P1#3: a second load returns the SAME object — the engine's mutable
    singletons are never duplicated into divergent copies."""
    pkg = _make_engine(tmp_path)
    name = "bootstrap._scaffold_t_idem"
    a = L.load_engine(pkg, tmp_path, canonical_name=name)
    a.STATE["k"] = "v"               # mutate the singleton through handle A
    b = L.load_engine(pkg, tmp_path, canonical_name=name)
    assert a is b
    assert b.STATE.get("k") == "v"   # same object — mutation is visible


def test_file_relative_ignores_a_hostile_path_decoy(tmp_path, monkeypatch, clean_modules):
    """SR1 / the reproduced S1 attack: a decoy ``bootstrap/`` injected on
    ``sys.path`` (hostile PYTHONPATH) must NOT hijack the engine — the loader
    resolves the package from the verified absolute dir, never via sys.path."""
    real = _make_engine(tmp_path / "real", marker="real")
    # A booby-trapped decoy that, if ever import-resolved, would mark itself.
    decoy_root = tmp_path / "attacker"
    _write(decoy_root / "bootstrap" / "_scaffold" / "__init__.py", """
        MARKER = 'HIJACKED'
    """)
    monkeypatch.syspath_prepend(str(decoy_root))  # attacker earlier on sys.path

    mod = L.load_engine(real, tmp_path / "real", canonical_name="bootstrap._scaffold_t_hostile")
    assert mod.MARKER == "real", "loader must load the verified dir, not the sys.path decoy"


def test_fails_closed_when_package_dir_escapes_root(tmp_path, clean_modules):
    """SR1: a package dir outside the declared Cairn root is refused (fail-closed),
    not loaded — the symlink/escape signature."""
    pkg = _make_engine(tmp_path / "elsewhere")
    bogus_root = tmp_path / "cairn_root"   # the engine is NOT under here
    bogus_root.mkdir()
    with pytest.raises(L.ScaffoldLoaderError, match="escapes the Cairn root"):
        L.load_engine(pkg, bogus_root, canonical_name="bootstrap._scaffold_t_escape")


def test_fails_closed_on_missing_package(tmp_path, clean_modules):
    empty = tmp_path / "bootstrap" / "_scaffold"
    empty.mkdir(parents=True)            # no __init__.py
    with pytest.raises(L.ScaffoldLoaderError, match="no __init__.py"):
        L.load_engine(empty, tmp_path, canonical_name="bootstrap._scaffold_t_missing")


def test_failed_load_leaves_no_half_initialized_entry(tmp_path, clean_modules):
    """A module that raises during exec must not leave a poisoned canonical entry."""
    pkg = tmp_path / "bootstrap" / "_scaffold"
    _write(pkg / "__init__.py", "raise RuntimeError('boom during import')\n")
    name = "bootstrap._scaffold_t_boom"
    with pytest.raises(RuntimeError, match="boom"):
        L.load_engine(pkg, tmp_path, canonical_name=name)
    assert name not in sys.modules


def test_submodule_without_parent_fails_closed(tmp_path, clean_modules):
    """Code review C1: loading a submodule before its parent package is
    initialized must fail closed with a clear error, not exec a module whose
    package-relative imports would raise an opaque parent-module error."""
    pkg = _make_engine(tmp_path)
    base = "bootstrap._scaffold_t_noparent"
    assert base not in sys.modules
    with pytest.raises(L.ScaffoldLoaderError, match="not initialized"):
        L.load_submodule("config", pkg, tmp_path, canonical_name=base)


def test_submodule_shares_canonical_namespace(tmp_path, clean_modules):
    pkg = _make_engine(tmp_path)
    base = "bootstrap._scaffold_t_sub"
    L.load_engine(pkg, tmp_path, canonical_name=base)
    cfg = L.load_submodule("config", pkg, tmp_path, canonical_name=base)
    assert cfg.VALUE == 42
    assert sys.modules[f"{base}.config"] is cfg
    # idempotent at the submodule level too
    assert L.load_submodule("config", pkg, tmp_path, canonical_name=base) is cfg
