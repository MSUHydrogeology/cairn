#!/usr/bin/env python3
"""Phase 0.3/4.2 tests — the data-only gate-transition checker.

Promotion binds to **one immutable candidate SHA** and to the exact reviewed
candidate-object bytes, with the changed gate/sensitive set derived
**independently** from git : an altered
checker, a moving/wrong candidate ref, a wrong prior anchor, a reviewed-hash
mismatch in the candidate object, an omitted-but-changed file, and an
unmanifested gate file all REFUSE — without ever executing the candidate.
Validation is **pure** (no nonce side effect); the atomic single-use nonce claim
is exercised separately (``claim_nonce``).
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
    files. Returns (repo, prior_sha, candidate_sha, manifest)."""
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
    candidate = _git(repo, "rev-parse", "HEAD").stdout.strip()
    gate_paths = ["bootstrap/tests/_oracle.py", "bootstrap/tests/test_oracle.py"]
    manifest = G.PromotionManifest(
        nonce="n1", prior_anchor=prior, candidate_sha=candidate,
        checker_hash=G.sha256_file(G.__file__),        # the EXECUTING checker
        files={p: G.sha256_git_object(repo, candidate, p) for p in gate_paths},
    )
    return repo, prior, candidate, manifest


def _call(repo, prior, manifest, candidate="HEAD"):
    return G.check_promotion(
        repo, manifest, prior_anchor_actual=prior, candidate=candidate,
        is_sensitive=_is_sensitive)


def test_valid_promotion_ok_and_pure(tmp_path):
    repo, prior, candidate, m = _setup(tmp_path)
    ok, holds = _call(repo, prior, m)
    assert ok and holds == []


def test_candidate_sha_mismatch_refused(tmp_path):
    """The manifest is pinned to an immutable candidate SHA; a
    candidate ref that resolves to a different SHA refuses (moving-ref defense)."""
    repo, prior, candidate, m = _setup(tmp_path)
    m.candidate_sha = "0" * 40
    ok, holds = _call(repo, prior, m)
    assert not ok and "candidate SHA mismatch" in holds[0]


def test_decisive_regression_object_differs_from_review(tmp_path):
    """A manifest hash that does not match the bytes in the candidate object
    refuses (the reviewed bytes are pinned to the immutable commit)."""
    repo, prior, candidate, m = _setup(tmp_path)
    m.files["bootstrap/tests/_oracle.py"] = "sha256:" + "0" * 64
    ok, holds = _call(repo, prior, m)
    assert not ok and any("differs from its reviewed hash" in h for h in holds)


def test_dirty_worktree_does_not_alter_validation(tmp_path):
    """Hashing reads the IMMUTABLE candidate object, so dirtying the
    worktree after commit does not change what is validated (the composing command
    separately enforces worktree==candidate before the re-anchor write)."""
    repo, prior, candidate, m = _setup(tmp_path)
    (repo / "bootstrap" / "tests" / "_oracle.py").write_text("ENGINE = 999  # dirtied\n")
    ok, holds = _call(repo, prior, m)
    assert ok and holds == [], holds          # object bytes unchanged → still valid


def test_altered_checker_rejected(tmp_path):
    """The checker pin is on the EXECUTING module; an authorization
    whose checker_hash does not match the running checker code refuses."""
    repo, prior, candidate, m = _setup(tmp_path)
    m.checker_hash = "sha256:" + "0" * 64
    ok, holds = _call(repo, prior, m)
    assert not ok and "checker" in holds[0]


def test_prior_anchor_mismatch_rejected(tmp_path):
    repo, prior, candidate, m = _setup(tmp_path)
    ok, holds = G.check_promotion(
        repo, m, prior_anchor_actual="0" * 40, candidate="HEAD",
        is_sensitive=_is_sensitive)
    assert not ok and "replay refused" in holds[0]


def test_omitted_changed_file_holds(tmp_path):
    """A file that actually changed but is omitted from the manifest -> HOLD
    (the checker derives the changed set independently)."""
    repo, prior, candidate, m = _setup(tmp_path)
    del m.files["bootstrap/tests/test_oracle.py"]
    ok, holds = _call(repo, prior, m)
    assert not ok and any("NOT in the promotion manifest" in h for h in holds)


def test_unmanifested_extra_file_holds(tmp_path):
    repo, prior, candidate, m = _setup(tmp_path)
    m.files["bootstrap/tests/_oracle_trust.py"] = "sha256:dead"   # not actually changed
    ok, holds = _call(repo, prior, m)
    assert not ok and any("not an actual changed" in h for h in holds)


# --- atomic single-use nonce claim --------------------------------

def test_claim_nonce_atomic_single_use(tmp_path):
    ledger = tmp_path / "nonces"
    assert not G.nonce_used(ledger, "abc")
    assert G.claim_nonce(ledger, "abc") is True       # first claim wins
    assert G.nonce_used(ledger, "abc")
    assert G.claim_nonce(ledger, "abc") is False      # replay loses
    assert G.claim_nonce(ledger, "other") is True     # a distinct nonce is independent


def test_parse_promotion_roundtrip():
    text = (
        "nonce: nnn\n"
        "prior_anchor: " + "C" * 40 + "\n"
        "candidate_sha: " + "D" * 40 + "\n"
        "checker_hash: sha256:abc\n"
        "evidence_hash: sha256:ev\n"
        "prospective_manifest_hash: sha256:pm\n"
        "files:\n"
        "  bootstrap/tests/_oracle.py: sha256:111\n"
        "  bootstrap/tests/test_oracle.py: sha256:222\n"
    )
    m = G.parse_promotion(text)
    assert m.nonce == "nnn" and m.prior_anchor == "C" * 40
    assert m.candidate_sha == "D" * 40
    assert m.evidence_hash == "sha256:ev" and m.prospective_manifest_hash == "sha256:pm"
    assert m.files["bootstrap/tests/_oracle.py"] == "sha256:111"


def test_parse_promotion_missing_field():
    with pytest.raises(G.PromotionError):
        G.parse_promotion("nonce: x\n")               # no prior_anchor/candidate_sha/checker_hash
