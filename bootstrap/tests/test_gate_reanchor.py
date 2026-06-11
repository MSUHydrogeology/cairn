#!/usr/bin/env python3
"""Phase 4 two-stage contract tests (round-4 final contract).

Stage A gathers **non-authoritative** evidence by materializing C in isolation;
Stage B is **data-only and authoritative**: it resolves the authorization from the
git object at the authority anchor, binds C + the evidence + the prospective
manifest exactly, executes NO candidate code, constructs N = C + the manifest
commit, and advances the one designated trusted ref P -> N via expected-old CAS.

Acceptance regressions (Codex round-4): candidate mutation during Stage A cannot
affect Stage B; arbitrary/absent authorization refuses; a second promotion cannot
replay the same advance; a stale prior refuses; candidate execution is impossible
in Stage B; and success returns an immutable N carrying exactly the reviewed
manifest.
"""
from __future__ import annotations

import inspect
import json
import subprocess

import pytest

from bootstrap.tests import _gate_reanchor as R
from bootstrap.tests import _oracle_activation as A
from bootstrap.tests import _gate_transition as G

REQUIRED = ["solo-greenfield", "upgrade_apply"]
SENSITIVE_REL = "bootstrap/tests/_oracle.py"
CHECKER_REL = "bootstrap/tests/_gate_transition.py"
DESIGNATED = "refs/cairn/gate-anchor"


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=True)


def _activation_yaml(act: A.Activation) -> str:
    lines = [f"baseline_sha: {act.baseline_sha}", f"trusted_ref: {act.trusted_ref}",
             f"nonce: {act.nonce}", "scope:"]
    lines += [f"  - {s}" for s in act.scope]
    lines += ["required_scenarios:"] + [f"  - {s}" for s in act.required_scenarios]
    return "\n".join(lines) + "\n"


def _authz_yaml(m: G.PromotionManifest) -> str:
    lines = [f"nonce: {m.nonce}", f"prior_anchor: {m.prior_anchor}",
             f"candidate_sha: {m.candidate_sha}", f"checker_hash: {m.checker_hash}",
             f"evidence_hash: {m.evidence_hash}",
             f"prospective_manifest_hash: {m.prospective_manifest_hash}", "files:"]
    lines += [f"  {k}: {v}" for k, v in m.files.items()]
    return "\n".join(lines) + "\n"


def _fake_oracle(scenarios=REQUIRED, ok=True):
    def _f(workdir, *, baseline_ref, trusted_ref, repo, target_root, gate=False):
        return {"status": "ran", "ok": ok,
                "fixtures": [{"name": s, "status": "match"} for s in scenarios],
                "privileged": []}
    return _f


def _fake_produce(tree):
    return {"schema": "cairn-gate-manifest/v1", "frozen_files": {"x": "sha256:0"}}


def _two_stage_repo(tmp_path):
    """A trusted repo with prior gate state P, candidate C, and an authority anchor
    A holding the authorization bundle. Returns a bundle of everything Stage B
    needs, plus the already-gathered evidence."""
    repo = tmp_path / "trusted"
    (repo / "bootstrap" / "tests" / "fixtures").mkdir(parents=True)
    (repo / "dev" / ".cairn").mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / CHECKER_REL).write_text("# pinned checker bytes\n")
    (repo / SENSITIVE_REL).write_text("ENGINE = 0\n")
    (repo / "bootstrap" / "tests" / "fixtures" / "gate_manifest.json").write_text("{}\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "P prior gate state")
    P = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "update-ref", DESIGNATED, P)                  # the designated gate ref starts at P

    # Candidate C: change the sensitive file + ship the evaluated activation.
    trusted_act = A.Activation(baseline_sha=P, trusted_ref="refs/heads/main",
                               nonce="act-nonce", scope=["bootstrap/tests/"],
                               required_scenarios=list(REQUIRED))
    (repo / SENSITIVE_REL).write_text("ENGINE = 1\n")
    (repo / R._ACTIVATION_REL).write_text(_activation_yaml(trusted_act))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "C candidate")
    C = _git(repo, "rev-parse", "HEAD").stdout.strip()

    # Stage A — gather evidence (non-authoritative; fakes for oracle/produce).
    evidence = R.gather_evidence(
        trusted_repo=repo, candidate_ref=C, prior_anchor=P,
        workdir=tmp_path / "wd_A", required_scenarios=REQUIRED,
        run_oracle_fn=_fake_oracle(), produce_fn=_fake_produce, env_scrub=False)

    # The supervised reviewer authors the authorization binding P, C, the evidence,
    # and the prospective manifest, then commits it at the authority anchor A.
    manifest = G.PromotionManifest(
        nonce="audit-1", prior_anchor=P, candidate_sha=C,
        checker_hash=G.sha256_file(repo / CHECKER_REL),
        evidence_hash=evidence.digest(),
        prospective_manifest_hash=evidence.prospective_manifest_hash,
        files={SENSITIVE_REL: G.sha256_git_object(repo, C, SENSITIVE_REL)})
    (repo / R._AUTHZ_REL).write_text(_authz_yaml(manifest))
    (repo / R._TRUSTED_ACT_REL).write_text(_activation_yaml(trusted_act))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "A authority bundle")
    Asha = _git(repo, "rev-parse", "HEAD").stdout.strip()
    # restore the worktree's checker/sensitive to P-pinned bytes is unnecessary:
    # check_promotion reads the checker worktree (unchanged across P/C/A).
    return dict(repo=repo, P=P, C=C, A=Asha, evidence=evidence,
                manifest=manifest, trusted_act=trusted_act)


def _promote(b, *, confirm=False, anchor_ref=None, evidence=None):
    return R.promote_data_only(
        trusted_repo=b["repo"], anchor_ref=anchor_ref or b["A"],
        evidence=evidence or b["evidence"], designated_ref=DESIGNATED, confirm=confirm)


# --- evidence (Stage A) ----------------------------------------------------------

def test_stage_a_evidence_is_deterministic_and_isolated(tmp_path):
    b = _two_stage_repo(tmp_path)
    ev = b["evidence"]
    assert ev.candidate_sha == b["C"] and ev.prior_anchor == b["P"]
    assert ev.scenario_results == {s: "match" for s in REQUIRED}
    assert ev.oracle_ok and ev.prospective_manifest_hash.startswith("sha256:")
    # a second gather over the same C reproduces the same bundle digest
    ev2 = R.gather_evidence(
        trusted_repo=b["repo"], candidate_ref=b["C"], prior_anchor=b["P"],
        workdir=tmp_path / "wd_A2", required_scenarios=REQUIRED,
        run_oracle_fn=_fake_oracle(), produce_fn=_fake_produce, env_scrub=False)
    assert ev2.digest() == ev.digest()


# --- the happy path: prepare (data-only) then supervised promote -----------------

def test_prepare_then_supervised_promote(tmp_path):
    b = _two_stage_repo(tmp_path)
    prep = _promote(b, confirm=False)
    assert prep.ok and not prep.reanchored and not prep.ref_advanced
    assert prep.new_anchor and prep.checks["anchor_minimal"]
    # ref still at P (no advance during prepare)
    assert _git(b["repo"], "rev-parse", DESIGNATED).stdout.strip() == b["P"]

    res = _promote(b, confirm=True)
    assert res.ok and res.reanchored and res.ref_advanced
    N = res.new_anchor
    assert _git(b["repo"], "rev-parse", DESIGNATED).stdout.strip() == N
    # N = C + the manifest only
    diff = _git(b["repo"], "diff", "--name-only", f"{b['C']}..{N}").stdout.split()
    assert diff == [R._MANIFEST_REL]
    # N carries exactly the reviewed prospective manifest bytes
    shown = _git(b["repo"], "show", f"{N}:{R._MANIFEST_REL}").stdout
    assert shown == b["evidence"].prospective_manifest_bytes


# --- Codex round-4 acceptance regressions ----------------------------------------

def test_candidate_mutation_during_stage_a_cannot_affect_stage_b(tmp_path):
    """Stage B reads git objects at C, so mutating the live worktree after Stage A
    does not change what is validated or promoted."""
    b = _two_stage_repo(tmp_path)
    (b["repo"] / SENSITIVE_REL).write_text("ENGINE = 999  # mutated after evidence\n")
    res = _promote(b, confirm=True)
    assert res.ok and res.reanchored, res.refusals
    shown = _git(b["repo"], "show", f"{res.new_anchor}:{SENSITIVE_REL}").stdout
    assert shown == "ENGINE = 1\n"                 # promoted the OBJECT bytes, not the worktree


def test_absent_authorization_refuses(tmp_path):
    """Authorization is resolved only from the git object at the authority anchor —
    an anchor without the bundle refuses (no arbitrary-path authority)."""
    b = _two_stage_repo(tmp_path)
    res = _promote(b, confirm=True, anchor_ref=b["C"])    # C has no authz bundle
    assert not res.ok and any("authority bundle absent" in r for r in res.refusals)


def test_second_promotion_cannot_replay_the_advance(tmp_path):
    b = _two_stage_repo(tmp_path)
    first = _promote(b, confirm=True)
    assert first.ok and first.reanchored
    second = _promote(b, confirm=True)               # gate ref now at N, not P
    assert not second.ok and not second.reanchored
    assert not second.checks["gate_ref_at_prior"]


def test_stale_prior_refuses(tmp_path):
    """If the designated ref is not at the manifest's prior gate state, refuse."""
    b = _two_stage_repo(tmp_path)
    _git(b["repo"], "update-ref", DESIGNATED, b["C"])    # move the gate ref off P
    res = _promote(b, confirm=True)
    assert not res.ok and not res.checks["gate_ref_at_prior"]


def test_stage_b_executes_no_candidate_code(tmp_path):
    """A candidate carrying a conftest tripwire that raises on import is still
    promoted — Stage B never imports/collects/executes candidate code."""
    b = _two_stage_repo(tmp_path)
    # add a tripwire conftest to a NEW candidate commit, re-author the bundle.
    repo = b["repo"]
    _git(repo, "checkout", "-q", b["C"])
    (repo / "bootstrap" / "tests" / "conftest_tripwire.py").write_text(
        "raise SystemExit('candidate code executed during Stage B!')\n")
    _git(repo, "add", "-A")
    _git(repo, "-c", "user.email=t@t", "-c", "user.name=t",
         "commit", "-q", "-m", "C2 candidate with tripwire")
    C2 = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "checkout", "-q", "main")
    ev = R.gather_evidence(trusted_repo=repo, candidate_ref=C2, prior_anchor=b["P"],
                           workdir=tmp_path / "wd_trip", required_scenarios=REQUIRED,
                           run_oracle_fn=_fake_oracle(), produce_fn=_fake_produce, env_scrub=False)
    manifest = G.PromotionManifest(
        nonce="audit-2", prior_anchor=b["P"], candidate_sha=C2,
        checker_hash=G.sha256_file(repo / CHECKER_REL),
        evidence_hash=ev.digest(), prospective_manifest_hash=ev.prospective_manifest_hash,
        files={SENSITIVE_REL: G.sha256_git_object(repo, C2, SENSITIVE_REL)})
    # the tripwire conftest is a NON-sensitive file present in C2's tree; it is
    # never in the manifest and never imported — its presence proves Stage B does
    # not collect/execute candidate code.
    (repo / R._AUTHZ_REL).write_text(_authz_yaml(manifest))
    (repo / R._TRUSTED_ACT_REL).write_text(_activation_yaml(b["trusted_act"]))
    _git(repo, "add", "-A")
    _git(repo, "-c", "user.email=t@t", "-c", "user.name=t",
         "commit", "-q", "-m", "A2 authority bundle")
    A2 = _git(repo, "rev-parse", "HEAD").stdout.strip()
    res = R.promote_data_only(trusted_repo=repo, anchor_ref=A2, evidence=ev,
                              designated_ref=DESIGNATED, confirm=True)
    assert res.ok and res.reanchored, res.refusals   # tripwire never ran


def test_success_returns_immutable_anchor(tmp_path):
    b = _two_stage_repo(tmp_path)
    res = _promote(b, confirm=True)
    N = res.new_anchor
    # N is a real, immutable commit object whose manifest equals the reviewed bytes
    assert subprocess.run(["git", "-C", str(b["repo"]), "cat-file", "-e", N],
                          capture_output=True).returncode == 0
    assert res.checks["anchor_verified"] and res.checks["anchor_minimal"]


# --- evidence binding must be exact ----------------------------------------------

def test_wrong_evidence_hash_refuses(tmp_path):
    b = _two_stage_repo(tmp_path)
    tampered = R.EvidenceBundle(**{**b["evidence"].__dict__,
                                   "scenario_results": {"solo-greenfield": "match"}})
    res = _promote(b, confirm=True, evidence=tampered)
    assert not res.ok and any("evidence_hash" in r for r in res.refusals)


def test_prospective_manifest_mismatch_refuses(tmp_path):
    b = _two_stage_repo(tmp_path)
    tampered = R.EvidenceBundle(**{**b["evidence"].__dict__,
                                   "prospective_manifest_bytes": "DIFFERENT\n",
                                   "prospective_manifest_hash": R._sha256_bytes(b"DIFFERENT\n")})
    res = _promote(b, confirm=True, evidence=tampered)
    assert not res.ok and any("prospective_manifest" in r for r in res.refusals)


# --- the production orchestrator is not authority-injectable ----------------------

def test_promote_orchestrator_not_injectable():
    params = set(inspect.signature(R.promote).parameters)
    for forbidden in ("run_oracle_fn", "produce_fn", "reanchor_fn", "evidence", "nonce_ledger_dir"):
        assert forbidden not in params, forbidden


def test_construct_anchor_commit_is_deterministic(tmp_path):
    b = _two_stage_repo(tmp_path)
    n1 = R._construct_anchor_commit(b["repo"], b["C"], R._MANIFEST_REL, b"manifest-bytes\n")
    n2 = R._construct_anchor_commit(b["repo"], b["C"], R._MANIFEST_REL, b"manifest-bytes\n")
    assert n1 == n2 and len(n1) == 40            # fixed identity+dates -> reproducible N
