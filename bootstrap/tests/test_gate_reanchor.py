#!/usr/bin/env python3
"""Phase 4 two-stage contract tests (round-4 contract + round-5 trust-root).

Stage A gathers **non-authoritative** evidence by materializing C in isolation;
Stage B is **data-only and authoritative**. Round 5 added the trust-root
authenticity: the authority anchor A must be a one-parent authorization commit on
P with a bounded diff, the executing verifier code is pinned against P's trusted
gate manifest, the designated gate ref is fixed (no override), and N is accepted
by the real gate verifier before reanchored=True.
"""
from __future__ import annotations

import hashlib
import inspect
import json
import subprocess
from pathlib import Path

import pytest

from bootstrap.tests import _gate_reanchor as R
from bootstrap.tests import _oracle_activation as A
from bootstrap.tests import _gate_transition as G
from bootstrap.tests import _gate_preflight as P

REQUIRED = ["solo-greenfield", "upgrade_apply"]
SENSITIVE_REL = "bootstrap/tests/_oracle.py"
REPO = Path(__file__).resolve().parents[2]
DESIGNATED = R._DESIGNATED_REF
AUTHZ_REF = R._AUTHORIZATION_REF


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
    tree = Path(tree)
    return {"schema": "cairn-gate-manifest/v1",
            "frozen_files": {
                rel: hashlib.sha256((tree / rel).read_bytes()).hexdigest()
                for rel in R.M._legacy_frozen_files(tree)
            }}


def _trusted_frozen_files() -> dict:
    """The trusted gate-manifest frozen_files that pin the EXECUTING authority code
    (so Stage B's authority-code pin passes for the real running modules)."""
    return {rel: hashlib.sha256(open(path, "rb").read()).hexdigest()
            for rel, path in R._authority_code_files()}


def _commit_all(repo, msg, *, allow_empty=False):
    _git(repo, "add", "-A")
    args = ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q"]
    if allow_empty:
        args.append("--allow-empty")
    _git(repo, *args, "-m", msg)
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _author_A(repo, parent, manifest, trusted_act, *, extra=None):
    """Author an authorization commit on *parent* holding the authz bundle (plus any
    *extra* files, for the bounded-diff negative test); return its SHA."""
    _git(repo, "checkout", "-q", parent)
    for rel, text in {R._AUTHZ_REL: _authz_yaml(manifest),
                      R._TRUSTED_ACT_REL: _activation_yaml(trusted_act)}.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    for rel, text in (extra or {}).items():
        (repo / rel).write_text(text)
    a = _commit_all(repo, "A authority bundle")
    _git(repo, "checkout", "-q", "main")
    return a


def _two_stage_repo(tmp_path):
    repo = tmp_path / "trusted"
    (repo / "bootstrap" / "tests" / "fixtures").mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / SENSITIVE_REL).write_text("ENGINE = 0\n")
    # P's gate manifest pins the executing authority code (the trust root).
    (repo / R._MANIFEST_REL).write_text(
        json.dumps({"frozen_files": _trusted_frozen_files()}, indent=2, sort_keys=True) + "\n")
    P = _commit_all(repo, "P prior gate state")
    _git(repo, "update-ref", DESIGNATED, P)

    trusted_act = A.Activation(baseline_sha=P, trusted_ref="refs/heads/main",
                               nonce="act-nonce", scope=["bootstrap/tests/"],
                               required_scenarios=list(REQUIRED))
    (repo / SENSITIVE_REL).write_text("ENGINE = 1\n")
    (repo / R._ACTIVATION_REL).parent.mkdir(parents=True, exist_ok=True)
    (repo / R._ACTIVATION_REL).write_text(_activation_yaml(trusted_act))
    C = _commit_all(repo, "C candidate")

    evidence = R.gather_evidence(
        trusted_repo=repo, candidate_ref=C, prior_anchor=P,
        workdir=tmp_path / "wd_A", required_scenarios=REQUIRED,
        run_oracle_fn=_fake_oracle(), produce_fn=_fake_produce, env_scrub=False)

    manifest = G.PromotionManifest(
        nonce="audit-1", prior_anchor=P, candidate_sha=C,
        checker_hash=G.sha256_file(R.G.__file__),          # the EXECUTING checker
        evidence_hash=evidence.digest(),
        prospective_manifest_hash=evidence.prospective_manifest_hash,
        files={SENSITIVE_REL: G.sha256_git_object(repo, C, SENSITIVE_REL)})
    Asha = _author_A(repo, P, manifest, trusted_act)
    _git(repo, "update-ref", AUTHZ_REF, Asha)
    return dict(repo=repo, P=P, C=C, A=Asha, evidence=evidence,
                manifest=manifest, trusted_act=trusted_act)


def _promote(b, *, confirm=False, anchor_ref=None, evidence=None, verify=True):
    return R.promote_data_only(
        trusted_repo=b["repo"], anchor_ref=anchor_ref or b["A"],
        evidence=evidence or b["evidence"], designated_ref=DESIGNATED, confirm=confirm,
        verify_anchor_fn=(lambda *a: True) if verify else (lambda *a: False))


# --- happy path -----------------------------------------------------------------

def test_prepare_then_supervised_promote(tmp_path):
    b = _two_stage_repo(tmp_path)
    prep = _promote(b, confirm=False)
    assert prep.ok and not prep.reanchored and not prep.ref_advanced
    assert prep.checks["authority_anchor_parent"] and prep.checks["authority_bounded_diff"]
    assert prep.checks["authority_code_pinned"] and prep.checks["anchor_static_verified"]
    assert _git(b["repo"], "rev-parse", DESIGNATED).stdout.strip() == b["P"]

    res = _promote(b, confirm=True)
    assert res.ok and res.reanchored and res.ref_advanced
    assert _git(b["repo"], "rev-parse", DESIGNATED).stdout.strip() == res.new_anchor
    diff = _git(b["repo"], "diff", "--name-only", f"{b['C']}..{res.new_anchor}").stdout.split()
    assert diff == [R._MANIFEST_REL]


# --- round-4 regressions (still hold) -------------------------------------------

def test_candidate_mutation_during_stage_a_cannot_affect_stage_b(tmp_path):
    b = _two_stage_repo(tmp_path)
    (b["repo"] / SENSITIVE_REL).write_text("ENGINE = 999\n")
    res = _promote(b, confirm=True)
    assert res.ok and res.reanchored, res.refusals
    assert _git(b["repo"], "show", f"{res.new_anchor}:{SENSITIVE_REL}").stdout == "ENGINE = 1\n"


def test_second_promotion_cannot_replay_the_advance(tmp_path):
    b = _two_stage_repo(tmp_path)
    assert _promote(b, confirm=True).reanchored
    second = _promote(b, confirm=True)
    assert not second.ok and not second.reanchored and not second.checks["gate_ref_at_prior"]


def test_wrong_evidence_hash_refuses(tmp_path):
    b = _two_stage_repo(tmp_path)
    tampered = R.EvidenceBundle(**{**b["evidence"].__dict__,
                                   "scenario_results": {"solo-greenfield": "match"}})
    res = _promote(b, confirm=True, evidence=tampered)
    assert not res.ok and any("evidence_hash" in r for r in res.refusals)


# --- authority-anchor authenticity ---------------------------------

def test_authority_anchor_must_be_one_parent_on_P(tmp_path):
    b = _two_stage_repo(tmp_path)
    a_on_c = _author_A(b["repo"], b["C"], b["manifest"], b["trusted_act"])   # parent = C, not P
    res = _promote(b, confirm=True, anchor_ref=a_on_c)
    assert not res.ok and not res.checks["authority_anchor_parent"]


def test_authority_anchor_bounded_diff(tmp_path):
    b = _two_stage_repo(tmp_path)
    a_fat = _author_A(b["repo"], b["P"], b["manifest"], b["trusted_act"],
                      extra={SENSITIVE_REL: "SMUGGLED\n"})       # changes more than authz
    res = _promote(b, confirm=True, anchor_ref=a_fat)
    assert not res.ok and not res.checks["authority_bounded_diff"]


# --- executing authority-code pin ----------------------------------

def test_untrusted_authority_code_refuses(tmp_path):
    """If P's trusted manifest pins a different hash for a verifier module than the
    executing code, Stage B refuses (the running verifier is not trusted)."""
    repo = tmp_path / "repo"
    (repo / "bootstrap" / "tests" / "fixtures").mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    frozen = _trusted_frozen_files()
    frozen["bootstrap/tests/_gate_transition.py"] = "0" * 64        # wrong pin
    (repo / R._MANIFEST_REL).write_text(json.dumps({"frozen_files": frozen}) + "\n")
    P = _commit_all(repo, "P")
    ok, holds = R._verify_executing_authority_code(repo, P)
    assert not ok and any("_gate_transition.py" in h for h in holds)


def test_executing_authority_code_pin_passes_for_real_modules(tmp_path):
    repo = tmp_path / "repo2"
    (repo / "bootstrap" / "tests" / "fixtures").mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / R._MANIFEST_REL).write_text(json.dumps({"frozen_files": _trusted_frozen_files()}) + "\n")
    P = _commit_all(repo, "P")
    ok, holds = R._verify_executing_authority_code(repo, P)
    assert ok and holds == []


def test_legacy_data_only_promotion_never_executes_unpinned_preflight(tmp_path, monkeypatch):
    """Roster-less P cannot authorize importing the newer preflight helper."""
    b = _two_stage_repo(tmp_path)
    monkeypatch.setattr(R, "_load_pinned_preflight",
                        lambda *a, **k: pytest.fail("legacy Stage B executed unpinned preflight"))
    result = _promote(b, confirm=False)
    assert result.ok
    assert result.checks["authority_code_pinned"]
    assert result.checks["trusted_manifest_derivation"]


def test_authority_pin_reads_v2_frozen_entry_digest(tmp_path):
    repo = tmp_path / "v2-pin"
    (repo / "bootstrap/tests/fixtures").mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    frozen = {
        rel: {"sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
              "mode": "100644", "oid": "0" * 40}
        for rel, path in R._authority_code_files()
    }
    preflight_source = Path(R.__file__).with_name("_gate_preflight.py").read_bytes()
    frozen["bootstrap/tests/_gate_preflight.py"] = {
        "sha256": hashlib.sha256(preflight_source).hexdigest(),
        "mode": "100644", "oid": "0" * 40}
    (repo / "bootstrap/tests/_gate_preflight.py").write_bytes(preflight_source)
    (repo / R._MANIFEST_REL).write_text(json.dumps({"schema": "cairn-gate-manifest/v2",
                                                      "frozen_files": frozen}) + "\n")
    P = _commit_all(repo, "P v2 manifest")
    ok, holds = R._verify_executing_authority_code(repo, P, include_preflight=True)
    assert ok and holds == []
    with R._load_pinned_preflight(repo, P) as trusted:
        assert callable(trusted.rederive_static_manifest)

    # A candidate working copy with different source cannot influence the
    # loader; the loader reads P's object and refuses a bad P manifest pin.
    frozen["bootstrap/tests/_gate_preflight.py"]["sha256"] = "0" * 64
    (repo / R._MANIFEST_REL).write_text(json.dumps({"frozen_files": frozen}) + "\n")
    bad_pin = _commit_all(repo, "P with a wrong preflight pin")
    with pytest.raises(RuntimeError, match="does not authenticate preflight"):
        with R._load_pinned_preflight(repo, bad_pin):
            pass


def test_rostered_stage_b_executes_only_preflight_bytes_pinned_by_p(tmp_path):
    """Real Stage B narrows from signed P and statically verifies N."""
    repo = tmp_path / "rostered-stage-b"
    subprocess.run(["git", "clone", "--shared", "--no-checkout", "-q",
                    str(REPO), str(repo)], capture_output=True, check=True)
    _git(repo, "checkout", "--detach", "HEAD")
    _git(repo, "checkout", "-b", "main")
    roster = R.M._roster_from_bytes(
        (repo / R.M._PROTECTED_ROSTER_REL).read_bytes(), require_initial_approval=True)
    base_manifest = R.M.produce(repo, roster)
    (repo / R._MANIFEST_REL).write_text(
        json.dumps(base_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    P_sha = _commit_all(repo, "P with signed roster policy", allow_empty=True)
    _git(repo, "update-ref", DESIGNATED, P_sha)

    act = A.Activation(baseline_sha=P_sha, trusted_ref="refs/heads/main",
                       nonce="rostered-stage-b", scope=["bootstrap/tests/"],
                       required_scenarios=list(REQUIRED))
    (repo / R._ACTIVATION_REL).parent.mkdir(parents=True, exist_ok=True)
    (repo / R._ACTIVATION_REL).write_text(_activation_yaml(act), encoding="utf-8")
    oracle_path = repo / SENSITIVE_REL
    oracle_path.write_text(oracle_path.read_text(encoding="utf-8")
                           + "\n# reviewed candidate change\n", encoding="utf-8")
    marker = tmp_path / "candidate-preflight-executed"
    preflight_path = repo / "bootstrap/tests/_gate_preflight.py"
    C = _commit_all(repo, "C changes a protected oracle")
    prospective = R.M.produce(repo, roster)
    prospective.pop("object_format")
    prospective["frozen_files"] = {
        rel: R.M._entry_sha256(entry)
        for rel, entry in prospective["frozen_files"].items()}
    for field in ("cascade_mutable", "phase_mutable"):
        for entry in prospective[field].values():
            entry.pop("mode", None)
            entry.pop("oid", None)
    prospective_bytes = (json.dumps(prospective, indent=2, sort_keys=True).encode()
                         + b"\n")
    evidence = R.EvidenceBundle(
        candidate_sha=C, prior_anchor=P_sha, required_scenarios=list(REQUIRED),
        scenario_results={name: "match" for name in REQUIRED},
        prospective_manifest_bytes=prospective_bytes.decode(),
        prospective_manifest_hash=R._sha256_bytes(prospective_bytes),
        checker_hash=G.sha256_file(Path(R.G.__file__)), oracle_ok=True)
    auth = G.PromotionManifest(
        nonce="stage-b-authz", prior_anchor=P_sha, candidate_sha=C,
        checker_hash=evidence.checker_hash, evidence_hash=evidence.digest(),
        prospective_manifest_hash=evidence.prospective_manifest_hash,
        files={SENSITIVE_REL: G.sha256_git_object(repo, C, SENSITIVE_REL)})
    A_sha = _author_A(repo, P_sha, auth, act)
    _git(repo, "update-ref", AUTHZ_REF, A_sha)

    # Dirty only the invoking checkout after C is fixed. Stage B must execute
    # P's authenticated source blob, never this checkout's gated marker.
    preflight_path.write_text(
        preflight_path.read_text(encoding="utf-8")
        + "\nif __import__('os').environ.get('CAIRN_STAGE_B_MARKER'):\n"
        + f"    Path({str(marker)!r}).write_text('executed')\n",
        encoding="utf-8")
    import os
    os.environ["CAIRN_STAGE_B_MARKER"] = "1"
    try:
        result = R.promote_data_only(trusted_repo=repo, anchor_ref=A_sha,
                                     evidence=evidence, confirm=False)
    finally:
        os.environ.pop("CAIRN_STAGE_B_MARKER", None)
    assert result.ok, result.refusals
    assert result.checks["authority_code_pinned"]
    assert result.checks["trusted_manifest_derivation"]
    assert result.checks["anchor_static_verified"]
    assert not result.ref_advanced
    assert not marker.exists(), "Stage B executed the candidate's preflight module"

    # A committed protected-byte replacement is different: without that exact
    # path in A's authorized files, Stage B refuses before constructing N.
    C_bad = _commit_all(repo, "C substitutes protected preflight bytes")
    prospective_bad = R.M.produce(repo, roster)
    prospective_bad.pop("object_format")
    prospective_bad["frozen_files"] = {
        rel: R.M._entry_sha256(entry)
        for rel, entry in prospective_bad["frozen_files"].items()}
    for field in ("cascade_mutable", "phase_mutable"):
        for entry in prospective_bad[field].values():
            entry.pop("mode", None)
            entry.pop("oid", None)
    bad_bytes = (json.dumps(prospective_bad, indent=2, sort_keys=True).encode()
                 + b"\n")
    bad_evidence = R.EvidenceBundle(
        candidate_sha=C_bad, prior_anchor=P_sha, required_scenarios=list(REQUIRED),
        scenario_results={name: "match" for name in REQUIRED},
        prospective_manifest_bytes=bad_bytes.decode(),
        prospective_manifest_hash=R._sha256_bytes(bad_bytes),
        checker_hash=G.sha256_file(Path(R.G.__file__)), oracle_ok=True)
    bad_auth = G.PromotionManifest(
        nonce="stage-b-bad-authz", prior_anchor=P_sha, candidate_sha=C_bad,
        checker_hash=bad_evidence.checker_hash, evidence_hash=bad_evidence.digest(),
        prospective_manifest_hash=bad_evidence.prospective_manifest_hash,
        files={SENSITIVE_REL: G.sha256_git_object(repo, C_bad, SENSITIVE_REL)})
    bad_A = _author_A(repo, P_sha, bad_auth, act)
    _git(repo, "update-ref", AUTHZ_REF, bad_A)
    os.environ["CAIRN_STAGE_B_MARKER"] = "1"
    try:
        refused = R.promote_data_only(trusted_repo=repo, anchor_ref=bad_A,
                                      evidence=bad_evidence, confirm=False)
    finally:
        os.environ.pop("CAIRN_STAGE_B_MARKER", None)
    assert not refused.ok
    assert not refused.checks["data_only_files"]
    assert refused.new_anchor is None
    assert not marker.exists(), "Stage B executed the candidate's preflight module"


def test_pretransition_manifest_refuses_until_supervised_bootstrap(tmp_path):
    """Production-shaped: the REAL pre-transition manifest shape does
    NOT pin the Stage-B authority modules (they read FROZEN-NEW). Against such a P
    the authority-code pin refuses — so the production command cannot pass until the
    supervised Phase-0 bootstrap (gate-manifest pre-pin) establishes the trust root.
    After the pre-pin (manifest regenerated to include the modules) it passes."""
    repo = tmp_path / "pretrans"
    (repo / "bootstrap" / "tests" / "fixtures").mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    # pre-transition shape: pins some unrelated test file, NOT the Stage-B modules.
    pre = {"frozen_files": {"bootstrap/tests/test_upgrade.py": "0" * 64}}
    (repo / R._MANIFEST_REL).write_text(json.dumps(pre) + "\n")
    P_old = _commit_all(repo, "P (pre-transition; Stage-B modules unpinned)")
    ok, holds = R._verify_executing_authority_code(repo, P_old)
    assert not ok
    assert any("_gate_reanchor.py" in h and "not pinned" in h for h in holds)

    # supervised pre-pin: the new manifest pins the executing Stage-B modules.
    (repo / R._MANIFEST_REL).write_text(
        json.dumps({"frozen_files": _trusted_frozen_files()}) + "\n")
    P_new = _commit_all(repo, "P (post-bootstrap; Stage-B modules pinned)")
    ok2, holds2 = R._verify_executing_authority_code(repo, P_new)
    assert ok2 and holds2 == []


# --- singular gate ref (fixed; no override) --------------------------

def test_promote_orchestrator_not_injectable_and_no_ref_overrides():
    params = set(inspect.signature(R.promote).parameters)
    for forbidden in ("run_oracle_fn", "produce_fn", "reanchor_fn", "evidence",
                      "nonce_ledger_dir", "anchor_ref", "designated_ref", "verify_anchor_fn"):
        assert forbidden not in params, forbidden


def test_cli_rejects_authority_ref_overrides(tmp_path):
    with pytest.raises(SystemExit):
        R.main(["promote", "--repo", str(tmp_path), "--anchor-ref", "x",
                "--confirm-supervised-reanchor"])
    with pytest.raises(SystemExit):
        R.main(["prepare", "--repo", str(tmp_path), "--designated-ref", "refs/x"])


# --- real gate verifier accepts N before reanchored ------------------

def test_static_verify_failure_refuses_before_cas(tmp_path):
    b = _two_stage_repo(tmp_path)
    res = _promote(b, confirm=True, verify=False)               # static verify returns False
    assert not res.ok and not res.ref_advanced
    assert not res.checks["anchor_static_verified"]
    assert _git(b["repo"], "rev-parse", DESIGNATED).stdout.strip() == b["P"]   # authority untouched


def test_static_verify_runs_against_materialized_N_not_checkout(tmp_path, monkeypatch):
    """The production path wires the REAL _gate_manifest.verify against
    N AS THE IMMUTABLE ANCHOR, checking frozen-file state from a MATERIALIZED N tree
    (repo=<N>), not the invoking checkout — even when the trusted worktree differs."""
    b = _two_stage_repo(tmp_path)
    # make the trusted working-tree manifest DIFFER from N, to prove we follow N.
    (b["repo"] / R._MANIFEST_REL).write_text("{}  # divergent worktree\n")
    seen = {}

    def _fake_verify(manifest_path, *, anchor_ref=None, repo=None, require_anchor=False,
                     do_collect=True, out=None, trusted_repo=None, trusted_ref="HEAD"):
        seen["anchor_ref"] = anchor_ref
        seen["do_collect"] = do_collect
        seen["repo"] = Path(repo)
        seen["manifest_in_repo"] = (Path(repo) / R._MANIFEST_REL).read_text(encoding="utf-8")
        return 0
    monkeypatch.setattr(R.M, "verify", _fake_verify)
    res = R.promote_data_only(trusted_repo=b["repo"], anchor_ref=b["A"],
                              evidence=b["evidence"], designated_ref=DESIGNATED, confirm=True)
    assert res.reanchored and seen["anchor_ref"] == res.new_anchor and seen["do_collect"] is False
    # verifier ran against the materialized N tree, NOT the (divergent) trusted checkout
    assert seen["repo"] != b["repo"]
    assert seen["manifest_in_repo"] == b["evidence"].prospective_manifest_bytes


def test_construct_anchor_commit_is_deterministic(tmp_path):
    b = _two_stage_repo(tmp_path)
    n1 = R._construct_anchor_commit(b["repo"], b["C"], R._MANIFEST_REL, b"manifest-bytes\n")
    n2 = R._construct_anchor_commit(b["repo"], b["C"], R._MANIFEST_REL, b"manifest-bytes\n")
    assert n1 == n2 and len(n1) == 40
