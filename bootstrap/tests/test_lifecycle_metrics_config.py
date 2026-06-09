"""Containment + fail-safe tests for the lifecycle-metrics config loader.

Guards the Phase-C external-review findings:

* config-supplied paths that would escape the repo root (absolute or
  ``..``-traversing) fall back to the built-in repo-relative default, so the
  tool's only write surface (the snapshots dir) stays under
  ``dev/measurement/`` even under a hostile / careless ``metrics-config.json``;
* wrong-typed scalar config values fall back to their defaults rather than
  raising (the load path is forgiving by contract).

These exercise ``load_config`` / ``emit_snapshot`` through the installed
launcher facade — the same surface an adopter imports. This is a NEW test
file (recorded as FROZEN-NEW by the gate manifest; its node-IDs as
COLLECTION-ADDED), so it adds coverage without a gate re-anchor.
"""
from __future__ import annotations

import datetime
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
_LM_PATH = CAIRN_ROOT / "templates" / "modules" / "default-on" / "lifecycle_metrics.py"


def _load_lm() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cairn_lm_config", _LM_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["cairn_lm_config"] = module
    spec.loader.exec_module(module)
    return module


# The lifecycle-metrics template is a required, always-present source artifact
# in this repo, so it is loaded unconditionally (no skip guard) — its absence is
# a real failure to surface, not a skip. Leaving these tests UNMARKED keeps them
# COLLECTION-ADDED-only for the gate manifest (no skip/xfail re-anchor).
_lm = _load_lm()


def _write_config(root: Path, cfg: object) -> None:
    d = root / "dev" / ".cairn"
    d.mkdir(parents=True, exist_ok=True)
    (d / "metrics-config.json").write_text(
        cfg if isinstance(cfg, str) else json.dumps(cfg), encoding="utf-8"
    )


def test_default_config_paths_are_repo_relative(tmp_path: Path) -> None:
    """No config file -> built-in defaults, byte-identical to pre-fix behavior."""
    root = tmp_path.resolve()
    cfg = _lm.load_config(root)
    assert cfg.snapshots_dir == root / "dev" / "measurement" / "snapshots"
    assert cfg.annotations_dir == root / "dev" / "metrics_annotations"
    assert cfg.collision_window_days == 14
    assert cfg.backfill_max_days == 14


def test_traversal_snapshots_dir_falls_back_to_default(tmp_path: Path) -> None:
    """A ``..``-traversing snapshots_dir is rejected -> contained default."""
    root = (tmp_path / "repo").resolve()
    root.mkdir()
    _write_config(root, {"snapshots_dir": "../../../../escape"})
    cfg = _lm.load_config(root)
    assert cfg.snapshots_dir == root / "dev" / "measurement" / "snapshots"
    # Positive containment property: resolves under the repo root.
    resolved = cfg.snapshots_dir.resolve()
    assert resolved == root.resolve() or root.resolve() in resolved.parents


def test_absolute_snapshots_dir_falls_back_to_default(tmp_path: Path) -> None:
    """An absolute snapshots_dir (outside the repo) is rejected -> default."""
    root = (tmp_path / "repo").resolve()
    root.mkdir()
    outside = (tmp_path / "outside").resolve()
    _write_config(root, {"snapshots_dir": str(outside)})
    cfg = _lm.load_config(root)
    assert cfg.snapshots_dir == root / "dev" / "measurement" / "snapshots"


def test_inbounds_config_path_is_honored(tmp_path: Path) -> None:
    """An in-bounds override is honored unchanged (containment is not a clamp
    onto the default for legitimate relocations)."""
    root = tmp_path.resolve()
    _write_config(root, {"snapshots_dir": "dev/measurement/snaps2"})
    cfg = _lm.load_config(root)
    assert cfg.snapshots_dir == root / "dev" / "measurement" / "snaps2"


def test_wrong_typed_scalar_falls_back_without_raising(tmp_path: Path) -> None:
    """A non-numeric tunable falls back to the default rather than raising."""
    root = tmp_path.resolve()
    _write_config(root, {"collision_window_days": "not-an-int"})
    cfg = _lm.load_config(root)  # must not raise
    assert cfg.collision_window_days == 14


def test_malformed_json_uses_all_defaults(tmp_path: Path) -> None:
    """Malformed JSON falls back to the full default set (no raise)."""
    root = tmp_path.resolve()
    _write_config(root, "{ this is not valid json ")
    cfg = _lm.load_config(root)  # must not raise
    assert cfg.snapshots_dir == root / "dev" / "measurement" / "snapshots"
    assert cfg.collision_window_days == 14


def test_emit_snapshot_stays_contained_under_hostile_config(tmp_path: Path) -> None:
    """The integration guard: even with an escaping snapshots_dir, the
    snapshot write lands inside the repo, never at the escaping path."""
    root = (tmp_path / "repo").resolve()
    (root / "dev" / "proposals").mkdir(parents=True)
    (root / "dev" / "proposals" / "2026-05-01-alice-thing.md").write_text(
        "# t\n\n**Author**: A (Strategy)\n"
        "**Date opened**: 2026-05-01\n**Status**: accepted\n",
        encoding="utf-8",
    )
    _write_config(root, {"snapshots_dir": "../../../../escape-out"})
    path, _ = _lm.emit_snapshot(root=root, timestamp_utc=datetime.datetime(2026, 6, 1))
    assert path == root / "dev" / "measurement" / "snapshots" / "2026-06-01-1.csv"
    assert path.exists()
    # The write is contained: it resolves under the repo root.
    assert root.resolve() in path.resolve().parents
