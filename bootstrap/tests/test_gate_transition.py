#!/usr/bin/env python3
"""Phase 0.3/4.2 tests — the data-only gate-transition checker.

Promotion binds to the exact reviewed candidate bytes (confirming-2 Finding 1):
a checker that was altered, a replayed prior anchor, a permitted-path file
changed after its reviewed hash, an omitted authorized file, and an extra
authorized file all REFUSE — without ever executing the candidate.
"""
from __future__ import annotations

import pytest

from bootstrap.tests import _gate_transition as G


def _setup(tmp_path):
    """A fake repo with a pinned checker + two gate-control files, and a matching
    promotion manifest."""
    repo = tmp_path
    (repo / "bootstrap" / "tests").mkdir(parents=True)
    checker = repo / "bootstrap" / "tests" / "_gate_transition.py"
    checker.write_text("# pinned checker bytes\n")
    g1 = repo / "bootstrap" / "tests" / "_oracle.py"
    g1.write_text("ENGINE = 1\n")
    g2 = repo / "bootstrap" / "tests" / "test_oracle.py"
    g2.write_text("TEST = 1\n")
    gate_paths = ["bootstrap/tests/_oracle.py", "bootstrap/tests/test_oracle.py"]
    manifest = G.PromotionManifest(
        nonce="n1", prior_anchor="A" * 40,
        checker_hash=G.sha256_file(checker),
        files={p: G.sha256_file(repo / p) for p in gate_paths},
    )
    return repo, gate_paths, manifest


def test_valid_promotion_ok(tmp_path):
    repo, paths, m = _setup(tmp_path)
    ok, holds = G.check_promotion(repo, m, gate_control_paths=paths, prior_anchor_actual="A" * 40)
    assert ok and holds == []


def test_decisive_regression_file_changed_after_review(tmp_path):
    """A permitted-path file edited AFTER its reviewed hash was recorded → HOLD."""
    repo, paths, m = _setup(tmp_path)
    (repo / "bootstrap" / "tests" / "_oracle.py").write_text("ENGINE = 999  # tampered\n")
    ok, holds = G.check_promotion(repo, m, gate_control_paths=paths, prior_anchor_actual="A" * 40)
    assert not ok and any("after its reviewed hash" in h for h in holds)


def test_altered_checker_rejected(tmp_path):
    repo, paths, m = _setup(tmp_path)
    (repo / "bootstrap" / "tests" / "_gate_transition.py").write_text("# candidate altered me\n")
    ok, holds = G.check_promotion(repo, m, gate_control_paths=paths, prior_anchor_actual="A" * 40)
    assert not ok and "altered" in holds[0]


def test_replay_prior_anchor_mismatch_rejected(tmp_path):
    repo, paths, m = _setup(tmp_path)
    ok, holds = G.check_promotion(repo, m, gate_control_paths=paths, prior_anchor_actual="B" * 40)
    assert not ok and "replay" in holds[0]


def test_omitted_authorized_file_holds(tmp_path):
    repo, paths, m = _setup(tmp_path)
    del m.files["bootstrap/tests/test_oracle.py"]          # manifest omits an authorized file
    ok, holds = G.check_promotion(repo, m, gate_control_paths=paths, prior_anchor_actual="A" * 40)
    assert not ok and any("omitted" in h for h in holds)


def test_extra_manifest_file_holds(tmp_path):
    repo, paths, m = _setup(tmp_path)
    m.files["bootstrap/_scaffold/upgrade.py"] = "sha256:dead"   # outside the gate-control set
    ok, holds = G.check_promotion(repo, m, gate_control_paths=paths, prior_anchor_actual="A" * 40)
    assert not ok and any("outside the gate-control set" in h for h in holds)


def test_parse_promotion_roundtrip():
    text = (
        "nonce: nnn\n"
        "prior_anchor: " + "C" * 40 + "\n"
        "checker_hash: sha256:abc\n"
        "files:\n"
        "  bootstrap/tests/_oracle.py: sha256:111\n"
        "  bootstrap/tests/test_oracle.py: sha256:222\n"
    )
    m = G.parse_promotion(text)
    assert m.nonce == "nnn" and m.prior_anchor == "C" * 40
    assert m.files["bootstrap/tests/_oracle.py"] == "sha256:111"


def test_parse_promotion_missing_field():
    with pytest.raises(G.PromotionError):
        G.parse_promotion("nonce: x\n")
