"""Contract for the gate-integrity manifest tool (six-proposal superplan pre-run
gate-control prerequisite; Codex S2 / R2-2).

Pins: produce() captures the frozen gate surface + cascade-mutable set + the
collection identity; the frozen set excludes cascade-mutable files and the
manifest artifact itself; and verify() HOLDs on every tampering class
(frozen-file edit, dropped node, new skip/xfail marker, interpreter-minor
mismatch, broken external anchor) while allowing additions. Stdlib only.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

from bootstrap.tests import _gate_manifest as G

_REPO = Path(__file__).resolve().parents[2]


def _write_manifest(tmp_path, manifest: dict) -> Path:
    p = tmp_path / "gate_manifest.json"
    p.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return p


@pytest.fixture(scope="module")
def produced() -> dict:
    """Produce once (a full collection subprocess) and share across tests."""
    return G.produce(_REPO)


def test_produce_has_the_expected_shape(produced):
    assert produced["schema"] == G.SCHEMA
    for key in ("interpreter", "gate_commands", "collection", "frozen_files",
                "cascade_mutable", "mapping_symbols"):
        assert key in produced
    assert produced["collection"]["node_count"] == len(produced["collection"]["node_ids"])
    assert produced["collection"]["node_count"] > 100  # the real suite is large
    for sym in ("_MODULE_MAPPINGS", "_SKILLS_MAPPINGS", "_CORE_MAPPINGS"):
        assert produced["mapping_symbols"][sym]["baseline_digest"]


def test_frozen_set_boundary(produced):
    frozen = produced["frozen_files"]
    # known gate files are pinned
    assert "bootstrap/tests/test_ast_attest.py" in frozen
    assert "scripts/check_cairn.py" in frozen
    assert "bootstrap/tests/_ast_attest.py" in frozen
    assert "bootstrap/tests/_gate_manifest.py" in frozen  # self-pinned
    # top-level gate-defining engine modules MUST be frozen (Security review BLOCKER):
    # security_check.py is the single source of the Bandit allowlist + scan targets.
    assert "bootstrap/security_check.py" in frozen
    assert "bootstrap/verify_integrity.py" in frozen
    assert "bootstrap/check_module_body_coverage.py" in frozen
    # cascade-mutable files + the manifest artifact are NOT frozen-hashed
    assert "bootstrap/tests/fixtures/scaffold_ast_baseline.json" not in frozen
    assert "bootstrap/tests/fixtures/frozen_engine/scaffold_frozen.py" not in frozen
    assert "bootstrap/_scaffold/config.py" not in frozen
    assert G._MANIFEST_REL not in frozen


def test_verify_clean_tree_is_ok(produced, tmp_path, capsys):
    mp = _write_manifest(tmp_path, produced)
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 0
    assert "OK — gate integrity intact" in capsys.readouterr().err


def test_verify_holds_on_frozen_file_modification(produced, tmp_path, capsys):
    tampered = copy.deepcopy(produced)
    # pretend a pinned gate file was edited (wrong sha)
    tampered["frozen_files"]["bootstrap/tests/test_ast_attest.py"] = "0" * 64
    mp = _write_manifest(tmp_path, tampered)
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 1
    assert "FROZEN-MODIFIED" in capsys.readouterr().err


def test_verify_holds_on_dropped_node(produced, tmp_path, capsys):
    tampered = copy.deepcopy(produced)
    # pin a node-ID that collection will NOT produce -> reduced collection
    tampered["collection"]["node_ids"].append(
        "bootstrap/tests/test_does_not_exist.py::test_phantom")
    mp = _write_manifest(tmp_path, tampered)
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 1
    assert "COLLECTION-DROPPED" in capsys.readouterr().err


def test_verify_holds_on_interpreter_minor_mismatch(produced, tmp_path, capsys):
    tampered = copy.deepcopy(produced)
    tampered["interpreter"]["version_info"] = [3, 11, 0]
    mp = _write_manifest(tmp_path, tampered)
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 1
    assert "INTERPRETER" in capsys.readouterr().err


def test_verify_holds_on_new_skip_marker(produced, tmp_path, capsys, monkeypatch):
    mp = _write_manifest(tmp_path, produced)
    ids = produced["collection"]["node_ids"]
    pinned_marked = set(produced["collection"]["skip_xfail_marked"])
    # simulate the run adding a skip/xfail marker to a currently-UNMARKED test
    fresh = next(i for i in ids if i not in pinned_marked)
    monkeypatch.setattr(G, "_collect", lambda repo=_REPO: (sorted(ids), [fresh], 0))
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 1
    assert "SKIP-XFAIL-NEW" in capsys.readouterr().err


def test_verify_allows_added_test(produced, tmp_path, capsys, monkeypatch):
    mp = _write_manifest(tmp_path, produced)
    ids = produced["collection"]["node_ids"]
    extra = "bootstrap/tests/test_newly_added.py::test_extra"
    # a superset of pinned (nothing dropped) + one new node, no new markers
    monkeypatch.setattr(G, "_collect", lambda repo=_REPO: (sorted(ids + [extra]), [], 0))
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 0
    assert "COLLECTION-ADDED" in capsys.readouterr().err


def test_verify_holds_when_anchor_object_absent(produced, tmp_path, capsys):
    # HEAD does not (yet) carry the manifest at the fixtures path -> git show fails -> HOLD.
    mp = _write_manifest(tmp_path, produced)
    assert G.verify(mp, anchor_ref="HEAD", repo=_REPO) == 1
    assert "ANCHOR" in capsys.readouterr().err


def test_anchor_skipped_note_when_no_ref(produced, tmp_path, capsys):
    mp = _write_manifest(tmp_path, produced)
    G.verify(mp, anchor_ref=None, repo=_REPO)
    assert "ANCHOR: skipped" in capsys.readouterr().err
