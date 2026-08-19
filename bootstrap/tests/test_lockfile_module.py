"""Stage 5 — the extracted lockfile module (`bootstrap/_scaffold/lockfile.py`).

Contracts:

* **Near-leaf, correct dependency direction** — `lockfile` imports only the stdlib
  and the `config` leaf (for `PresetError`); it must never import the engine
  package or any higher module (install / upgrade / cli), and there must be no
  cycle (config must not import lockfile).
* **Trust-anchor narrow import** — `bootstrap/verify_integrity.py`
  imports `read_lockfile` / `_LOCKFILE_REL` / `_LIVING_STATE_DSTS` from the
  *narrowest owner* (`bootstrap._scaffold.lockfile`), not the broad facade.
* **Single identity** — every moved symbol resolves to the one `lockfile` object
  across the engine and the `bootstrap.scaffold` facade.
* **Boundary pin** — the install-time WRITER (`write_install_lockfile`) and the
  manifest-coupled `_lock_file_list` stay in the engine, not the lockfile module.
* **Behavioral smoke** — emit/read round-trip, the secret-token guard (the path
  that surfaced the `PresetError` dependency), and the verbatim hash classifier.

Stdlib only.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

_PKG = Path(__file__).resolve().parents[1] / "_scaffold"
_VERIFY_INTEGRITY = Path(__file__).resolve().parents[1] / "verify_integrity.py"

_MOVED = (
    "_LOCKFILE_REL", "_BASE_CACHE_REL", "_PROFILE_REL", "_LOCK_SCHEMA",
    "_LIVING_STATE_DSTS", "_SECRET_TOKEN_RE", "_sha256_hex", "_cairn_version",
    "_cairn_commit", "_behind_by_n", "_refuse_secret_tokens", "_emit_lock_yaml",
    "read_lockfile", "classify_verbatim",
)


def _import_modules(pyfile: str) -> set[str]:
    mods: set[str] = set()
    for node in ast.walk(ast.parse(Path(pyfile).read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module)
        if isinstance(node, ast.Import):
            mods.update(a.name for a in node.names)
    return mods


def test_lockfile_depends_only_on_stdlib_and_the_config_leaf():
    from bootstrap._scaffold import lockfile as LK  # noqa: PLC0415

    for node in ast.walk(ast.parse(Path(LK.__file__).read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod.startswith("bootstrap") or node.level > 0:
                assert mod.rsplit(".", 1)[-1] in {"config", "security"}, f"lockfile imports {mod!r} (level={node.level})"
        if isinstance(node, ast.Import):
            for a in node.names:
                assert not a.name.startswith("bootstrap"), f"lockfile imports {a.name!r}"


def test_no_cycle_config_does_not_import_lockfile():
    from bootstrap._scaffold import config as C  # noqa: PLC0415

    assert not any(m.endswith("lockfile") for m in _import_modules(C.__file__)), (
        "config must not import lockfile (cycle)"
    )


def test_verify_integrity_imports_from_narrowest_owner():
    tree = ast.parse(_VERIFY_INTEGRITY.read_text(encoding="utf-8"))
    sources = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and any(a.name == "read_lockfile" for a in node.names)
    }
    assert sources == {"bootstrap._scaffold.lockfile"}, (
        f"verify_integrity must import the lockfile trust anchor from its narrow owner; got {sources}"
    )


def test_single_identity_across_consumers():
    import sys  # noqa: PLC0415

    from bootstrap._scaffold import lockfile as LK  # noqa: PLC0415
    import bootstrap._scaffold as engine  # noqa: PLC0415
    import bootstrap.scaffold  # noqa: PLC0415  (facade == engine)

    facade = sys.modules["bootstrap.scaffold"]
    for name in _MOVED:
        obj = getattr(LK, name)
        assert getattr(engine, name) is obj, f"engine.{name} is not the lockfile object"
        assert getattr(facade, name) is obj, f"facade.{name} is not the lockfile object"
    import bootstrap.verify_integrity as vi  # noqa: PLC0415
    assert vi.read_lockfile is LK.read_lockfile


def test_writer_and_lock_file_list_stay_in_the_engine():
    import bootstrap._scaffold as engine  # noqa: PLC0415
    from bootstrap._scaffold import lockfile as LK  # noqa: PLC0415

    for fn in ("write_install_lockfile", "_lock_file_list"):
        assert hasattr(engine, fn), f"{fn} should remain on the engine"
        assert not hasattr(LK, fn), f"{fn} must not be in the lockfile leaf (Stage-6 install coupling)"


def test_emit_read_roundtrip_and_classifier_smoke(tmp_path):
    from bootstrap._scaffold import lockfile as LK  # noqa: PLC0415

    data = {"schema": LK._LOCK_SCHEMA, "files": [{"dst": "AGENTS.md", "hash": "sha256:deadbeef"}]}
    (tmp_path / "dev" / ".cairn").mkdir(parents=True)
    (tmp_path / LK._LOCKFILE_REL).write_text(LK._emit_lock_yaml(data), encoding="utf-8")
    assert LK.read_lockfile(tmp_path) == data
    assert LK.read_lockfile(tmp_path / "nope") is None

    # verbatim classifier
    raw = b"#!/usr/bin/env python\nprint('hi')\n"
    assert LK.classify_verbatim(None, "sha256:x", raw) == "missing"
    assert LK.classify_verbatim(raw, "sha256:x", raw) == "up-to-date"
    assert LK.classify_verbatim(b"local-edit", "sha256:stale", raw) == "locally-modified"


def test_secret_token_guard_raises_preseterror():
    # The path that surfaced lockfile's dependency on config.PresetError.
    from bootstrap._scaffold import lockfile as LK  # noqa: PLC0415
    from bootstrap._scaffold.config import PresetError  # noqa: PLC0415

    LK._refuse_secret_tokens({"project_name": "demo"})  # clean: no raise
    with pytest.raises(PresetError, match="secret-like token"):
        LK._refuse_secret_tokens({"api_token": "x"})
    # allow-list lets a vetted public token through
    LK._refuse_secret_tokens({"api_token": "x"}, allow=("api_token",))
