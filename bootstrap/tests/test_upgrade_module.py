"""Stage 7 — the extracted upgrade subsystem (`bootstrap/_scaffold/upgrade.py`).

Contracts:

* **Layer-7 subsystem, downward-only dependencies** — `upgrade` imports only the
  stdlib and the lower modules (config / security / merge / slotmerge / lockfile /
  install). It must never import the engine package nor `cli`, and none of those
  lower modules may import `upgrade` (no cycle).
* **Single identity** — every moved symbol resolves to the one `upgrade` object
  across the engine and the `bootstrap.scaffold` facade.
* **Boundary pin** — the cli entry points (`main` / `build_arg_parser`) stay in the
  engine, not upgrade.
* **Root resolver still correct** — `_cairn_root()` (moved here) resolves the same
  Cairn root via depth, regardless of which `_scaffold/*.py` owns it.
* **Cross-module patch semantics** — `_cairn_is_git` is owned here; patching it at
  this module reaches `cmd_upgrade`'s internal call (the facade re-export does not).

Stdlib only.
"""
from __future__ import annotations

import ast
from pathlib import Path

_PKG = Path(__file__).resolve().parents[1] / "_scaffold"
_CAIRN_ROOT = Path(__file__).resolve().parents[2]


def _import_modules(pyfile: str) -> set[str]:
    mods: set[str] = set()
    for node in ast.walk(ast.parse(Path(pyfile).read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module)
        if isinstance(node, ast.Import):
            mods.update(a.name for a in node.names)
    return mods


def test_upgrade_depends_only_downward():
    from bootstrap._scaffold import upgrade as UP  # noqa: PLC0415

    allowed = {"config", "security", "merge", "slotmerge", "lockfile", "install"}
    for node in ast.walk(ast.parse(Path(UP.__file__).read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if node.level > 0:
                assert mod in allowed, f"upgrade imports sideways/up: .{mod}"
            else:
                assert not mod.startswith("bootstrap"), f"upgrade imports {mod!r}"
        if isinstance(node, ast.Import):
            for a in node.names:
                assert not a.name.startswith("bootstrap"), f"upgrade imports {a.name!r}"


def test_no_lower_module_imports_upgrade():
    for low in ("config", "security", "merge", "slotmerge", "lockfile", "install"):
        mods = _import_modules(str(_PKG / f"{low}.py"))
        assert not any(m.endswith("upgrade") for m in mods), f"{low} imports upgrade (cycle)"


def test_single_identity_across_consumers():
    import sys  # noqa: PLC0415

    from bootstrap._scaffold import upgrade as UP  # noqa: PLC0415
    import bootstrap._scaffold as engine  # noqa: PLC0415
    import bootstrap.scaffold  # noqa: PLC0415  (facade == engine)

    facade = sys.modules["bootstrap.scaffold"]
    for name in ("cmd_upgrade", "_compute_upgrade", "_write_stage", "_apply_upgrade",
                 "_cmd_init_lock", "_cmd_adopt_module", "_cairn_root", "_cairn_is_git"):
        obj = getattr(UP, name)
        assert getattr(engine, name) is obj, f"engine.{name} is not the upgrade object"
        assert getattr(facade, name) is obj, f"facade.{name} is not the upgrade object"


def test_cli_entrypoints_stay_in_engine_not_upgrade():
    import bootstrap._scaffold as engine  # noqa: PLC0415
    from bootstrap._scaffold import upgrade as UP  # noqa: PLC0415

    for nm in ("main", "build_arg_parser"):
        assert hasattr(engine, nm), f"{nm} should remain on the engine (cli, Stage 8)"
        assert not hasattr(UP, nm), f"{nm} must not be in the upgrade module"


def test_cairn_root_resolves_from_upgrade_module():
    from bootstrap._scaffold import upgrade as UP  # noqa: PLC0415

    assert UP._cairn_root() == _CAIRN_ROOT


def test_cross_module_patch_reaches_cmd_upgrade(monkeypatch):
    # Patching the OWNING module reaches cmd_upgrade's internal call; this pins the
    # post-split monkeypatch contract (the facade re-export is a separate binding).
    from bootstrap._scaffold import upgrade as UP  # noqa: PLC0415

    assert UP.cmd_upgrade.__globals__["_cairn_is_git"] is UP._cairn_is_git
    sentinel = object()
    monkeypatch.setattr(UP, "_cairn_is_git", lambda root: sentinel)
    assert UP.cmd_upgrade.__globals__["_cairn_is_git"](_CAIRN_ROOT) is sentinel


# ---------------------------------------------------------------------------
# Superseded-surface advisory flag (foldback rollup #1)
# ---------------------------------------------------------------------------

def test_superseded_local_surfaces_lists_present(tmp_path):
    from bootstrap._scaffold import config as CFG  # noqa: PLC0415

    (tmp_path / "dev").mkdir()
    (tmp_path / "dev" / "model_tier_mapping.md").write_text("x", encoding="utf-8")
    assert CFG.superseded_local_surfaces("model-selection", tmp_path) == [
        "dev/model_tier_mapping.md"
    ]


def test_superseded_local_surfaces_empty_when_absent_or_unknown(tmp_path):
    from bootstrap._scaffold import config as CFG  # noqa: PLC0415

    # Declared surface, but not present on disk -> no false flag.
    assert CFG.superseded_local_surfaces("model-selection", tmp_path) == []
    # A module with no declared supersession -> empty.
    assert CFG.superseded_local_surfaces("coordination-tiers", tmp_path) == []
    # Unknown module name -> empty (never raises).
    assert CFG.superseded_local_surfaces("no-such-module", tmp_path) == []


def test_superseded_surface_note_present_is_advisory(tmp_path):
    from bootstrap._scaffold import upgrade as UP  # noqa: PLC0415

    (tmp_path / "dev").mkdir()
    (tmp_path / "dev" / "security_review_protocols.md").write_text(
        "x", encoding="utf-8"
    )
    note = UP._superseded_surface_note(tmp_path, "security-review")
    assert note is not None
    assert "dev/security_review_protocols.md" in note
    assert "reconcile or retire" in note
    assert "advisory" in note  # never deletes/blocks


def test_superseded_surface_note_none_when_nothing_present(tmp_path):
    from bootstrap._scaffold import upgrade as UP  # noqa: PLC0415

    assert UP._superseded_surface_note(tmp_path, "security-review") is None
    assert UP._superseded_surface_note(tmp_path, "model-selection") is None
