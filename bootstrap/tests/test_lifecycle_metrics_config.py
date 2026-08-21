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

import pytest

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


#: The eight columns Part 1 of `metrics-events-not-prose` retires: a
#: `total_findings`/`findings_p*` bullet-count group and a
#: `review_yield_*` disposition-token group. Both were derived by
#: parsing review prose, which rewards writing more of it -- the
#: cheapest way to look thorough is to split one finding into three.
_RETIRED_PROPOSAL_COLUMNS = frozenset({
    "total_findings",
    "findings_p1",
    "findings_p2",
    "findings_p3",
    "review_yield_accept_count",
    "review_yield_accept_with_modification_count",
    "review_yield_reject_count",
    "review_yield_defer_count",
})

#: Every structural column Part 1 keeps, named explicitly so a future
#: accidental drop of a *kept* column fails loudly rather than only
#: showing up as a smaller-than-expected count.
_RETAINED_PROPOSAL_COLUMNS = (
    "stem",
    "author",
    "date_opened",
    "status",
    "decision_date",
    "days_to_decision",
    "review_rounds",
    "reviewer_agents",
    "cross_agent_type_review",
    "external_tier_review",
    "revised",
    "reviewed_date",
    "revised_date",
    "days_open_to_reviewed",
    "days_reviewed_to_revised",
    "days_revised_to_decision",
    "hours_open_to_reviewed",
    "hours_reviewed_to_revised",
    "hours_revised_to_decision",
    "stage_timestamp_reliability",
    "proposal_annotation_count",
    "response_models",
)


def test_proposal_columns_retires_exactly_the_eight_prose_scraped_names() -> None:
    """`PROPOSAL_COLUMNS` carries none of the eight retired columns and
    every retained structural column, by name -- not just a count."""
    columns = set(_lm.PROPOSAL_COLUMNS)
    present_retired = columns & _RETIRED_PROPOSAL_COLUMNS
    assert not present_retired, (
        f"retired columns still present in PROPOSAL_COLUMNS: {present_retired}"
    )
    missing_retained = set(_RETAINED_PROPOSAL_COLUMNS) - columns
    assert not missing_retained, (
        f"retained columns dropped from PROPOSAL_COLUMNS: {missing_retained}"
    )
    assert len(_lm.PROPOSAL_COLUMNS) == len(_RETAINED_PROPOSAL_COLUMNS) == 22


def test_backfill_from_is_not_a_recognized_argument() -> None:
    """`--backfill-from` and its `backfill` snapshot-event value are
    removed outright (the mode misattributed measurements to commits
    that did not produce them -- a defect independent of the v1->v2
    schema break, and removal is the only option that stops shipping
    it); `--help` no longer names either."""
    with pytest.raises(SystemExit) as exc:
        _lm.main(["--backfill-from", "2026-01-01"])
    assert exc.value.code != 0

    import io
    import contextlib

    buf = io.StringIO()
    with contextlib.suppress(SystemExit), contextlib.redirect_stdout(buf):
        _lm.main(["--help"])
    assert "--backfill-from" not in buf.getvalue()
    assert "backfill" not in buf.getvalue()


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


def test_v1_snapshot_bytes_survive_a_v2_run_and_the_two_are_distinguishable(
    tmp_path: Path,
) -> None:
    """Chunk 3's own acceptance property: a pre-existing (fixture-persisted)
    v1 snapshot's bytes are unchanged after a v2 code path runs; a freshly
    emitted snapshot carries the v2 identity; and a consumer reading the
    two files side by side can tell them apart from the schema_version
    field alone -- the v1 file carries no such column at all (its own
    absence IS the v1 marker; this tool never rewrites a persisted file
    to retroactively add one), the v2 file carries 'v2', and there is no
    third, ambiguous state."""
    root = tmp_path.resolve()
    (root / "dev" / "proposals").mkdir(parents=True)
    (root / "dev" / "proposals" / "2026-05-01-alice-thing.md").write_text(
        "# t\n\n**Author**: A (Strategy)\n"
        "**Date opened**: 2026-05-01\n**Status**: accepted\n",
        encoding="utf-8",
    )
    snapshots_dir = root / "dev" / "measurement" / "snapshots"
    snapshots_dir.mkdir(parents=True)
    v1_path = snapshots_dir / "2026-01-01-1.csv"
    v1_bytes = (
        b"kind,stem,author,date_opened,status,decision_date,"
        b"days_to_decision,review_rounds,corpus_commit,snapshot_event,"
        b"snapshot_timestamp_utc,corpus_collision_count_14d\r\n"
        b"proposal,2026-01-01-old-thing,Old,2026-01-01,accepted,,,,"
        b"abc1234,manual,2026-01-01T00:00:00Z,\r\n"
    )
    v1_path.write_bytes(v1_bytes)

    v2_path, _ = _lm.emit_snapshot(
        root=root, timestamp_utc=datetime.datetime(2026, 6, 1),
    )

    # The pre-existing v1 file is untouched -- byte-identical, not merely
    # equivalent.
    assert v1_path.read_bytes() == v1_bytes
    assert b"schema_version" not in v1_bytes

    v2_text = v2_path.read_text(encoding="utf-8")
    assert "schema_version" in v2_text.splitlines()[0]
    header = v2_text.splitlines()[0].split(",")
    data_row = v2_text.splitlines()[1].split(",")
    version_col = header.index("schema_version")
    assert data_row[version_col] == _lm.SNAPSHOT_SCHEMA_VERSION == "v2"

    # The manifest names the version identity too, so a reader need not
    # open either file to tell v1 apart from v2.
    manifest_md = _lm.format_manifest_md()
    assert "Schema version" in manifest_md
    assert "v2" in manifest_md
    snapshot_entry = next(
        e for e in _lm.output_manifest()
        if e["file"] == "dev/measurement/snapshots/<date>-N.csv"
    )
    assert snapshot_entry["schema_version"] == "v2"
