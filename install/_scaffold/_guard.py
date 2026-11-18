"""Engine import-boundary guard.

The launcher (`bootstrap/scaffold.py`) defends the *launcher* load path. But the
accepted architecture also imports engine submodules **directly**
(`import bootstrap._scaffold.config` at Stages 4/5; the canonical-identity
contract names `import bootstrap._scaffold.<m>` as a supported route; the
circular-import gate imports each module clean). A finder installed only by the
launcher does not mediate those — Python's default `PathFinder` would resolve and
execute the child, following a submodule symlink outside the Cairn root.

This module moves the boundary to a place that **necessarily runs before every
engine child import**: the engine package's own `__init__` installs it as its
first action. Because Python imports a package before any of its submodules, the
guard is in place before any `bootstrap._scaffold.<child>` resolves — whether the
engine was loaded by the launcher or imported directly.

It does two things (`install`):

1. **Rejects an already-cached polluted child.** Any `bootstrap._scaffold.*`
   module already in `sys.modules` whose real source is outside the engine
   directory is refused — a preloaded child must not be trusted as the engine
   (the cached-child route the re-review flagged).
2. **Installs a verifying finder** ahead of `PathFinder` that resolves every
   future `bootstrap._scaffold.*` source and verifies its **real** path is within
   the Cairn root **before** the import machinery executes it.

Threat-model note (per the re-review): a hostile `sitecustomize` / `PYTHONPATH`
that shadows the engine *parent* already has arbitrary execution — the loader
cannot undo that. What it can and does guarantee is that the engine the rest of
Cairn uses, and every child it imports, is the verified one under the Cairn root.

Stdlib only; import-pure (defining it installs nothing — `install()` is explicit).
"""
from __future__ import annotations

import importlib.abc
import importlib.util
import sys
from pathlib import Path

_CANONICAL = "bootstrap._scaffold"


class ScaffoldLoaderError(RuntimeError):
    """Fail-closed engine-import rejection: a `bootstrap._scaffold.*` module
    resolves to a path outside the Cairn root (import hijack / symlink escape)."""


def verify_within_root(path: Path, cairn_root: Path) -> Path:
    resolved = Path(path).resolve()
    root = Path(cairn_root).resolve()
    if resolved != root and root not in resolved.parents:
        raise ScaffoldLoaderError(
            f"engine path {resolved} escapes the Cairn root {root} — refusing "
            f"to load (fail-closed, SR1)"
        )
    return resolved


class EngineFinder(importlib.abc.MetaPathFinder):
    """Mediates every ``bootstrap._scaffold.<sub>`` import: maps the dotted name to
    a source under the engine directory, verifies the **real** source is within
    the Cairn root before building the spec, and refuses an escape."""

    def __init__(self, engine_dir: Path, cairn_root: Path) -> None:
        self._prefix = _CANONICAL + "."
        self._engine_dir = Path(engine_dir).resolve()
        self._cairn_root = Path(cairn_root).resolve()

    def find_spec(self, fullname, path=None, target=None):  # noqa: ARG002
        if not fullname.startswith(self._prefix):
            return None
        suffix = fullname[len(self._prefix):]
        base = self._engine_dir.joinpath(*suffix.split("."))
        for src, is_pkg in ((base / "__init__.py", True), (base.with_suffix(".py"), False)):
            if not src.exists():
                continue
            verify_within_root(src, self._cairn_root)  # before the loader execs it
            return importlib.util.spec_from_file_location(
                fullname, str(src),
                submodule_search_locations=[str(src.parent)] if is_pkg else None,
            )
        return None


def _reject_polluted_children(engine_dir: Path) -> None:
    engine_dir = engine_dir.resolve()
    for name, mod in list(sys.modules.items()):
        if not name.startswith(_CANONICAL + "."):
            continue
        f = getattr(mod, "__file__", None)
        if f is None:
            # Absence of a source path cannot satisfy source verification
            # (re-review-2 finding 2): a synthetic types.ModuleType injected
            # under the canonical name has no __file__ and must NOT be trusted.
            raise ScaffoldLoaderError(
                f"cached engine child {name!r} has no source path — cannot verify; "
                f"refusing (synthetic/polluted module, SR1)"
            )
        real = Path(f).resolve()
        if real != engine_dir and engine_dir not in real.parents:
            raise ScaffoldLoaderError(
                f"cached engine child {name!r} is loaded from {real}, outside the "
                f"engine directory {engine_dir} — refusing (polluted namespace, SR1)"
            )


def install(engine_dir: Path, cairn_root: Path) -> None:
    """Install the engine import boundary. Idempotent. Raises if a polluted child
    is already cached."""
    engine_dir = Path(engine_dir)
    cairn_root = Path(cairn_root)
    _reject_polluted_children(engine_dir)
    for f in sys.meta_path:
        if isinstance(f, EngineFinder):
            return
    sys.meta_path.insert(0, EngineFinder(engine_dir, cairn_root))
