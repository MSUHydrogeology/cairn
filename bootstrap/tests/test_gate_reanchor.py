#!/usr/bin/env python3
"""Phase 4 end-to-end tests — the single authoritative composing re-anchor gate.

The re-review's load-bearing demand (Finding 1): the ACTUAL re-anchor command —
not a unit-level library — must refuse unless activation acceptance, the oracle
over every required scenario, AND promotion validation all pass against one
immutable candidate SHA; and (Finding 3) it must claim a single-use nonce
atomically and re-anchor as one transaction, failing without consuming authority.

These drive ``run_reanchor_gate`` over a synthetic candidate repo with an injected
fake oracle (so the full install matrix is not re-run here — that is covered by
``test_oracle.py``), flipping ONE control at a time and asserting the transaction
properties: a refused control never burns the nonce and never writes; a passing
sweep claims the nonce once and writes once; replay (same ledger, concurrent
pre-claim) refuses; a write failure after the claim reports authority spent.
"""
from __future__ import annotations

import subprocess

import pytest

from bootstrap.tests import _gate_reanchor as R
from bootstrap.tests import _oracle_activation as A
from bootstrap.tests import _gate_transition as G

REQUIRED = ["solo-greenfield", "upgrade_apply"]
SENSITIVE_REL = "bootstrap/tests/_oracle.py"          # in the real sensitive roster


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=True)


def _activation_yaml(act: A.Activation) -> str:
    lines = [f"baseline_sha: {act.baseline_sha}", f"trusted_ref: {act.trusted_ref}",
             f"nonce: {act.nonce}", "scope:"]
    lines += [f"  - {s}" for s in act.scope]
    lines += ["required_scenarios:"] + [f"  - {s}" for s in act.required_scenarios]
    return "\n".join(lines) + "\n"


def _candidate_repo(tmp_path):
    """A repo with a prior commit and a candidate commit that changes one sensitive
    gate file and ships a matching activation artifact. Returns a bundle of
    everything ``run_reanchor_gate`` needs for a PASSING sweep."""
    repo = tmp_path / "target"
    (repo / "bootstrap" / "tests").mkdir(parents=True)
    (repo / "dev" / ".cairn").mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    checker = repo / "bootstrap" / "tests" / "_gate_transition.py"
    checker.write_text("# pinned checker bytes\n")
    sens = repo / SENSITIVE_REL
    sens.write_text("ENGINE = 0\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "prior")
    prior = _git(repo, "rev-parse", "HEAD").stdout.strip()

    # candidate: change the sensitive file + ship the activation artifact.
    sens.write_text("ENGINE = 1\n")
    trusted = A.Activation(baseline_sha=prior, trusted_ref="refs/heads/main",
                           nonce="activation-nonce", scope=["bootstrap/tests/"],
                           required_scenarios=list(REQUIRED))
    act_path = repo / "dev" / ".cairn" / "active-refactor.yml"
    act_path.write_text(_activation_yaml(trusted))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "candidate")
    candidate = _git(repo, "rev-parse", "HEAD").stdout.strip()

    manifest = G.PromotionManifest(
        nonce="promo-nonce-1", prior_anchor=prior, candidate_sha=candidate,
        checker_hash=G.sha256_file(checker),
        files={SENSITIVE_REL: G.sha256_git_object(repo, candidate, SENSITIVE_REL)})

    ledger = tmp_path / "ledger"            # the ONE externally-anchored ledger
    return dict(repo=repo, prior=prior, candidate=candidate, trusted=trusted,
                act_path=act_path, manifest=manifest, ledger=ledger)


def _fake_oracle(candidate_sha, *, ok=True, scenarios=REQUIRED):
    def _f(workdir, *, baseline_ref, trusted_ref, repo, target_root, gate):
        return {"status": "ran" if ok else "ran", "ok": ok,
                "candidate_sha": candidate_sha,
                "fixtures": [{"name": s, "status": "match"} for s in scenarios],
                "privileged": []}
    return _f


def _run(bundle, tmp_path, *, oracle=None, reanchor=None, manifest=None,
         trusted=None, ledger=None, postcondition=None):
    calls = []
    def _default_reanchor(sha):
        calls.append(sha)
    return R._run_reanchor_gate(
        trusted_repo=tmp_path / "trusted_checkout",      # distinct from target
        target_repo=bundle["repo"], candidate_ref="HEAD",
        prior_anchor=bundle["prior"],
        promotion_manifest=manifest or bundle["manifest"],
        trusted_expectation=trusted or bundle["trusted"],
        evaluated_activation_path=bundle["act_path"],
        nonce_ledger_dir=ledger or bundle["ledger"],
        oracle_workdir=tmp_path / "wd",
        reanchor_fn=reanchor or _default_reanchor,
        postcondition_fn=postcondition,
        baseline_ref=bundle["prior"], trusted_ref="refs/heads/main",
        run_oracle_fn=oracle or _fake_oracle(bundle["candidate"])), calls


def test_full_pass_claims_nonce_and_reanchors_once(tmp_path):
    b = _candidate_repo(tmp_path)
    res, calls = _run(b, tmp_path)
    assert res.ok and res.reanchored and res.nonce_claimed
    assert res.candidate_sha == b["candidate"]
    assert all(res.controls.values()), res.controls
    assert calls == [b["candidate"]]                 # wrote exactly once, the candidate
    assert G.nonce_used(b["ledger"], "promo-nonce-1")


def test_activation_failure_refuses_without_burning_nonce(tmp_path):
    b = _candidate_repo(tmp_path)
    bad_trusted = A.Activation(**{**b["trusted"].__dict__, "nonce": "DIFFERENT"})
    res, calls = _run(b, tmp_path, trusted=bad_trusted)
    assert not res.ok and not res.reanchored and not res.nonce_claimed
    assert not res.controls["activation"]
    assert calls == [] and not G.nonce_used(b["ledger"], "promo-nonce-1")


def test_missing_required_oracle_scenario_refuses(tmp_path):
    b = _candidate_repo(tmp_path)
    short = _fake_oracle(b["candidate"], scenarios=["solo-greenfield"])  # drops upgrade_apply
    res, calls = _run(b, tmp_path, oracle=short)
    assert not res.ok and not res.controls["oracle"]
    assert any("upgrade_apply" in r for r in res.refusals)
    assert calls == [] and not G.nonce_used(b["ledger"], "promo-nonce-1")


def test_failing_oracle_refuses(tmp_path):
    b = _candidate_repo(tmp_path)
    res, calls = _run(b, tmp_path, oracle=_fake_oracle(b["candidate"], ok=False))
    assert not res.ok and not res.controls["oracle"] and calls == []


def test_oracle_measured_other_candidate_refuses(tmp_path):
    """The oracle must have measured THIS candidate SHA, not some other tree."""
    b = _candidate_repo(tmp_path)
    res, calls = _run(b, tmp_path, oracle=_fake_oracle("0" * 40))
    assert not res.ok and not res.controls["oracle"]
    assert any("missing/mismatch refused" in r for r in res.refusals) and calls == []


def test_promotion_failure_refuses_without_burning_nonce(tmp_path):
    b = _candidate_repo(tmp_path)
    b["manifest"].files[SENSITIVE_REL] = "sha256:" + "0" * 64     # wrong reviewed hash
    res, calls = _run(b, tmp_path)
    assert not res.ok and not res.controls["promotion"]
    assert calls == [] and not G.nonce_used(b["ledger"], "promo-nonce-1")


def test_wrong_candidate_sha_in_manifest_refuses(tmp_path):
    b = _candidate_repo(tmp_path)
    b["manifest"].candidate_sha = "0" * 40
    res, calls = _run(b, tmp_path)
    assert not res.ok and not res.controls["promotion"] and calls == []


def test_dirty_worktree_refuses(tmp_path):
    b = _candidate_repo(tmp_path)
    (b["repo"] / SENSITIVE_REL).write_text("ENGINE = 999  # dirtied after commit\n")
    res, calls = _run(b, tmp_path)
    assert not res.ok and not res.controls["clean_worktree"]
    assert any("dirty" in r for r in res.refusals)
    assert calls == [] and not G.nonce_used(b["ledger"], "promo-nonce-1")


def test_injected_reanchor_failure_reports_authority_spent(tmp_path):
    b = _candidate_repo(tmp_path)
    def _boom(_sha):
        raise RuntimeError("disk full")
    res, calls = _run(b, tmp_path, reanchor=_boom)
    assert not res.ok and not res.reanchored
    assert res.nonce_claimed                          # authority WAS spent (safe direction)
    assert any("authority spent" in r for r in res.refusals)
    assert G.nonce_used(b["ledger"], "promo-nonce-1")  # cannot be replayed with this nonce


def test_same_ledger_replay_refused(tmp_path):
    """Codex's alternate-ledger probe, closed: the command owns ONE ledger, so a
    second promotion of the same nonce against it refuses (no fresh-path bypass)."""
    b = _candidate_repo(tmp_path)
    res1, calls1 = _run(b, tmp_path)
    assert res1.ok and calls1 == [b["candidate"]]
    res2, calls2 = _run(b, tmp_path)                  # same nonce, same ledger
    assert not res2.ok and not res2.reanchored
    assert any("replay refused" in r for r in res2.refusals) and calls2 == []


def test_concurrent_preclaim_refuses(tmp_path):
    """A concurrent claimant that wins the atomic claim first makes this run lose
    it — modeled by pre-claiming the nonce. The gate refuses and does not write."""
    b = _candidate_repo(tmp_path)
    assert G.claim_nonce(b["ledger"], "promo-nonce-1") is True   # the 'other' run wins
    res, calls = _run(b, tmp_path)
    assert not res.ok and not res.reanchored and not res.nonce_claimed
    assert any("replay refused" in r for r in res.refusals) and calls == []


# --- round-3 Finding 2: candidate binding is unconditional -----------------------

def _oracle_no_candidate(scenarios=REQUIRED):
    def _f(workdir, *, baseline_ref, trusted_ref, repo, target_root, gate):
        return {"status": "ran", "ok": True,           # NOTE: no candidate_sha key
                "fixtures": [{"name": s, "status": "match"} for s in scenarios],
                "privileged": []}
    return _f


def test_oracle_report_missing_candidate_sha_refuses(tmp_path):
    """Round-3 F2: a report that OMITS candidate_sha must refuse — the prior
    `and report.get(...)` made the binding conditional, so a candidate-less report
    passed. It must not."""
    b = _candidate_repo(tmp_path)
    res, calls = _run(b, tmp_path, oracle=_oracle_no_candidate())
    assert not res.ok and not res.controls["oracle"]
    assert any("missing/mismatch refused" in r for r in res.refusals)
    assert calls == [] and not G.nonce_used(b["ledger"], "promo-nonce-1")


# --- round-3 Finding 1/4: the post-write postcondition gates success -------------

def test_noop_writer_fails_postcondition(tmp_path):
    """A writer that returns normally but did NOT land the manifest cannot be
    reported as a successful re-anchor — the postcondition catches it."""
    b = _candidate_repo(tmp_path)
    res, calls = _run(b, tmp_path,
                      reanchor=lambda _sha: None,        # no-op writer
                      postcondition=lambda _sha: False)  # verification fails
    assert not res.ok and not res.reanchored
    assert res.nonce_claimed and res.controls.get("postcondition") is False
    assert any("post-write verification failed" in r for r in res.refusals)


def test_postcondition_pass_reanchors(tmp_path):
    b = _candidate_repo(tmp_path)
    res, calls = _run(b, tmp_path, postcondition=lambda _sha: True)
    assert res.ok and res.reanchored and res.controls.get("postcondition") is True


def test_postcondition_raising_spends_authority_safely(tmp_path):
    b = _candidate_repo(tmp_path)
    def _boom(_sha):
        raise RuntimeError("verify crashed")
    res, calls = _run(b, tmp_path, postcondition=_boom)
    assert not res.ok and not res.reanchored and res.nonce_claimed
    assert any("post-write verification raised" in r for r in res.refusals)


# --- round-3 Finding 3: the production command OWNS exactly one ledger ------------

def test_derive_ledger_is_pure_and_contained(tmp_path):
    """The ledger is a pure function of (trusted_repo, prior_anchor) and lives
    UNDER the trusted repo — so an authority has exactly one ledger (no
    alternate-ledger replay), and it cannot be redirected by a caller."""
    trusted = tmp_path / "trusted"
    l1 = R._derive_ledger(trusted, "a" * 40)
    l2 = R._derive_ledger(trusted, "a" * 40)
    l3 = R._derive_ledger(trusted, "b" * 40)
    assert l1 == l2 and l1 != l3                       # deterministic; keyed by anchor
    assert str(l1).startswith(str(trusted))            # contained under the trusted repo


def test_promote_is_not_dependency_injectable():
    """Round-3 F1/F3: the production command exposes no oracle / writer / ledger
    seam — its path cannot be substituted with a permissive oracle or no-op
    writer, and the ledger is derived, not passed."""
    import inspect
    params = set(inspect.signature(R.promote).parameters)
    for forbidden in ("run_oracle_fn", "reanchor_fn", "postcondition_fn", "nonce_ledger_dir"):
        assert forbidden not in params, forbidden


def test_promote_refuses_without_confirmation(tmp_path):
    b = _candidate_repo(tmp_path)
    # write minimal manifest/activation files to parse
    mpath = tmp_path / "promo.yml"
    mpath.write_text("nonce: x\nprior_anchor: " + "a" * 40 + "\ncandidate_sha: " + "b" * 40 +
                     "\nchecker_hash: sha256:x\nfiles:\n  bootstrap/tests/_oracle.py: sha256:y\n")
    apath = tmp_path / "trusted_act.yml"
    apath.write_text(_activation_yaml(b["trusted"]))
    res = R.promote(trusted_repo=tmp_path / "trusted", target_repo=b["repo"],
                    prior_anchor=b["prior"], promotion_manifest_path=mpath,
                    trusted_activation_path=apath, confirm=False)
    assert not res.ok and any("supervised confirmation" in r for r in res.refusals)


# --- round-3 Finding 4: the real writer is atomic -------------------------------

def test_atomic_write_replaces_whole_file(tmp_path):
    dest = tmp_path / "sub" / "f.json"
    R._atomic_write(dest, b"first\n")
    assert dest.read_bytes() == b"first\n"
    R._atomic_write(dest, b"second\n")                 # replace
    assert dest.read_bytes() == b"second\n"
    # no leftover temp files in the dir
    assert [p.name for p in dest.parent.iterdir()] == ["f.json"]
