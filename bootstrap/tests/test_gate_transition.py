#!/usr/bin/env python3
"""Phase 0.3/4.2 tests — the data-only gate-transition checker.

Promotion binds to the exact reviewed candidate bytes AND to single-use nonce
state, with the changed gate/sensitive set derived **independently** from git
(code-review P1.3): an altered checker, a replayed nonce, a permitted-path file
changed after its reviewed hash, an omitted-but-changed file, and an
unmanifested gate file all REFUSE — without ever executing the candidate.
"""
from __future__ import annotations

import subprocess

import pytest

from bootstrap.tests import _gate_transition as G


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=True)


def _is_sensitive(f: str) -> bool:
    return f.startswith("bootstrap/tests/") and not f.endswith("_gate_transition.py")


def _setup(tmp_path):
    """A git repo: a prior commit, then a candidate commit changing two gate
    files. Returns (repo, prior_sha, manifest, ledger)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "bootstrap" / "tests").mkdir(parents=True)
    checker = repo / "bootstrap" / "tests" / "_gate_transition.py"
    checker.write_text("# pinned checker bytes\n")
    g1 = repo / "bootstrap" / "tests" / "_oracle.py"
    g2 = repo / "bootstrap" / "tests" / "test_oracle.py"
    g1.write_text("ENGINE = 0\n")
    g2.write_text("TEST = 0\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "prior")
    prior = _git(repo, "rev-parse", "HEAD").stdout.strip()
    # candidate: change the two gate files
    g1.write_text("ENGINE = 1\n")
    g2.write_text("TEST = 1\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "candidate")
    gate_paths = ["bootstrap/tests/_oracle.py", "bootstrap/tests/test_oracle.py"]
    manifest = G.PromotionManifest(
        nonce="n1", prior_anchor=prior, checker_hash=G.sha256_file(checker),
        files={p: G.sha256_file(repo / p) for p in gate_paths},
    )
    ledger = tmp_path / "nonces.txt"
    return repo, prior, manifest, ledger


def _call(repo, prior, manifest, ledger):
    return G.check_promotion(
        repo, manifest, prior_anchor_actual=prior, candidate="HEAD",
        is_sensitive=_is_sensitive, nonce_ledger=ledger)


def test_valid_promotion_ok_and_consumes_nonce(tmp_path):
    repo, prior, m, ledger = _setup(tmp_path)
    ok, holds = _call(repo, prior, m, ledger)
    assert ok and holds == []
    assert G.nonce_used(ledger, "n1")              # consumed


def test_replayed_nonce_refused(tmp_path):
    repo, prior, m, ledger = _setup(tmp_path)
    ok1, _ = _call(repo, prior, m, ledger)
    assert ok1
    ok2, holds = _call(repo, prior, m, ledger)     # same nonce again
    assert not ok2 and "already consumed" in holds[0]


def test_decisive_regression_file_changed_after_review(tmp_path):
    repo, prior, m, ledger = _setup(tmp_path)
    (repo / "bootstrap" / "tests" / "_oracle.py").write_text("ENGINE = 999  # tampered\n")
    ok, holds = _call(repo, prior, m, ledger)
    assert not ok and any("after its reviewed hash" in h for h in holds)


def test_altered_checker_rejected(tmp_path):
    repo, prior, m, ledger = _setup(tmp_path)
    (repo / "bootstrap" / "tests" / "_gate_transition.py").write_text("# candidate altered me\n")
    ok, holds = _call(repo, prior, m, ledger)
    assert not ok and "altered" in holds[0]


def test_prior_anchor_mismatch_rejected(tmp_path):
    repo, prior, m, ledger = _setup(tmp_path)
    ok, holds = G.check_promotion(
        repo, m, prior_anchor_actual="0" * 40, candidate="HEAD",
        is_sensitive=_is_sensitive, nonce_ledger=ledger)
    assert not ok and "replay refused" in holds[0]


def test_omitted_changed_file_holds(tmp_path):
    """A file that actually changed but is omitted from the manifest -> HOLD
    (the checker derives the changed set independently, P1.3)."""
    repo, prior, m, ledger = _setup(tmp_path)
    del m.files["bootstrap/tests/test_oracle.py"]
    ok, holds = _call(repo, prior, m, ledger)
    assert not ok and any("NOT in the promotion manifest" in h for h in holds)


def test_unmanifested_extra_file_holds(tmp_path):
    repo, prior, m, ledger = _setup(tmp_path)
    m.files["bootstrap/tests/_oracle_trust.py"] = "sha256:dead"   # not actually changed
    ok, holds = _call(repo, prior, m, ledger)
    assert not ok and any("not an actual changed" in h for h in holds)


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
