#!/usr/bin/env python3
"""Phase 4 — the single **authoritative** supervised re-anchor gate.

The code-review re-review (Codex, 2026-06-11) confirmed the three controls were
each correct in isolation but composed by nothing: activation acceptance, the
differential oracle, and promotion validation were callable libraries with test
callers only, so a supervised operator could re-anchor after running just the
gate-manifest producer. This module is the missing composition (re-review
Finding 1): **one trusted-checkout command that runs all three controls against
ONE immutable candidate SHA and refuses the re-anchor unless each passes**, then
— only on a clean sweep — **atomically claims the single-use nonce and performs
the re-anchor as one transaction**.

Authority discipline
--------------------
* **Fail without consuming authority.** A failure in *any* control returns before
  the nonce is claimed and before any write — a refused candidate never spends a
  nonce (re-review Finding 3).
* **One immutable candidate.** The candidate ref is resolved to a full SHA once;
  every control is bound to that SHA. The worktree must be clean *and* at that
  SHA, so what was validated (the immutable object) is exactly what the re-anchor
  writes (no dirty-worktree / TOCTOU gap).
* **The verifier never measures itself.** The oracle runs in gate mode
  (``target_root`` = the evaluated candidate, distinct from the trusted
  ``repo``); this module runs from the trusted checkout.
* **The re-anchor write is injected, never implicit.** ``reanchor_fn`` is a
  required argument: the supervised operator wires the real gate-manifest
  producer; the regressions wire a fake (and an injected-failure). There is no
  default that silently writes — *blessing* the gate stays a deliberate
  supervised act, separate from *building* this command.

Stdlib only. Run from the trusted ``master`` checkout, target the candidate tree.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:  # package import (pytest)
    from bootstrap.tests import _oracle as O
    from bootstrap.tests import _oracle_activation as A
    from bootstrap.tests import _gate_transition as G
except ImportError:  # script mode
    import _oracle as O
    import _oracle_activation as A
    import _gate_transition as G


@dataclass
class GateResult:
    ok: bool
    candidate_sha: str | None
    controls: dict[str, bool] = field(default_factory=dict)   # name -> passed
    refusals: list[str] = field(default_factory=list)
    nonce_claimed: bool = False
    reanchored: bool = False


def _resolve_sha(repo: Path, ref: str) -> str:
    p = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"],
        capture_output=True, text=True, check=False)
    sha = (p.stdout or "").strip()
    if p.returncode != 0 or len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
        raise ValueError(f"ref does not resolve to a commit: {ref!r} ({p.stderr.strip()})")
    return sha


def _worktree_clean_at(repo: Path, candidate_sha: str) -> list[str]:
    """Refusals if the worktree is not clean AND exactly at *candidate_sha* — so
    the bytes the re-anchor writes equal the immutable object the controls
    validated. Empty list = clean and aligned."""
    refusals: list[str] = []
    head = _resolve_sha(repo, "HEAD")
    if head != candidate_sha:
        refusals.append(f"worktree HEAD {head[:12]} != candidate {candidate_sha[:12]} "
                        f"(the re-anchor must write the validated candidate)")
    st = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"],
                        capture_output=True, text=True, check=False)
    if st.returncode != 0:
        refusals.append(f"git status failed in {repo}: {st.stderr.strip()}")
    elif st.stdout.strip():
        refusals.append("evaluated worktree is dirty — refusing (validated object would "
                        "not equal the re-anchored bytes)")
    return refusals


def _required_scenarios_covered(report: dict, required: list[str]) -> tuple[bool, list[str]]:
    """Every entry in the activation's ``required_scenarios`` must be present AND
    matched in the oracle report (fixture or privileged). A missing or non-matched
    required scenario is a refusal — the oracle cannot silently skip one."""
    if report.get("status") != "ran" or not report.get("ok"):
        return False, [f"oracle did not pass (status={report.get('status')}, ok={report.get('ok')})"]
    matched = {f["name"] for f in report.get("fixtures", []) if f.get("status") == "match"}
    matched |= {p["name"] for p in report.get("privileged", []) if p.get("status") == "match"}
    missing = [s for s in required if s not in matched]
    return (not missing), [f"required oracle scenario not matched: {s}" for s in missing]


def run_reanchor_gate(
    *,
    trusted_repo: Path,
    target_repo: Path,
    candidate_ref: str,
    prior_anchor: str,
    promotion_manifest: G.PromotionManifest,
    trusted_expectation: A.Activation,
    evaluated_activation_path: Path | str,
    nonce_ledger_dir: Path,
    oracle_workdir: Path,
    reanchor_fn,
    baseline_ref: str | None = None,
    trusted_ref: str | None = None,
    run_oracle_fn=None,
    is_sensitive=A.is_sensitive,
) -> GateResult:
    """Run the three controls bound to one immutable candidate SHA; on a clean
    sweep, atomically claim the nonce and perform the injected re-anchor as one
    transaction. *reanchor_fn* is ``callable(candidate_sha) -> None``; it is only
    invoked after every control passes and the nonce is freshly claimed.

    *baseline_ref* / *trusted_ref* configure the differential oracle (the
    refactor's pre-change baseline + its out-of-band trust root). *run_oracle_fn*
    overrides ``_oracle.run_oracle`` (the regressions inject a fake)."""
    run_oracle_fn = run_oracle_fn or O.run_oracle
    target_repo = Path(target_repo)
    refusals: list[str] = []
    controls: dict[str, bool] = {}

    # One immutable candidate; the worktree must be clean and at it.
    candidate_sha = _resolve_sha(target_repo, candidate_ref)
    wt = _worktree_clean_at(target_repo, candidate_sha)
    controls["clean_worktree"] = not wt
    refusals.extend(wt)

    # Control A — activation acceptance over the independently-derived candidate diff.
    ok_a, holds_a, _changed = A.run_acceptance(
        target_repo, prior_anchor, candidate_sha,
        trusted_expectation=trusted_expectation,
        evaluated_activation_path=evaluated_activation_path,
        is_sensitive_fn=is_sensitive)
    controls["activation"] = ok_a
    refusals.extend(f"activation: {h}" for h in holds_a)

    # Control B — the differential oracle over EVERY required scenario.
    report = run_oracle_fn(oracle_workdir, baseline_ref=baseline_ref,
                           trusted_ref=trusted_ref, repo=trusted_repo,
                           target_root=target_repo, gate=True)
    ok_b, holds_b = _required_scenarios_covered(report, trusted_expectation.required_scenarios)
    # The oracle must have measured THIS candidate, not some other tree.
    if report.get("candidate_sha") and report["candidate_sha"] != candidate_sha:
        ok_b = False
        holds_b = holds_b + [f"oracle measured {report['candidate_sha'][:12]} != candidate "
                             f"{candidate_sha[:12]}"]
    controls["oracle"] = ok_b
    refusals.extend(f"oracle: {h}" for h in holds_b)

    # Control C — data-only promotion validation, bound to the same candidate SHA.
    ok_c, holds_c = G.check_promotion(
        target_repo, promotion_manifest, prior_anchor_actual=prior_anchor,
        candidate=candidate_sha, is_sensitive=is_sensitive)
    controls["promotion"] = ok_c
    refusals.extend(f"promotion: {h}" for h in holds_c)

    if not (controls["clean_worktree"] and ok_a and ok_b and ok_c):
        # Fail WITHOUT consuming authority — no nonce claim, no write.
        return GateResult(ok=False, candidate_sha=candidate_sha, controls=controls,
                          refusals=refusals, nonce_claimed=False, reanchored=False)

    # Every control passed → atomically claim the single-use nonce. A lost claim is
    # a replay (a concurrent or prior promotion already used it).
    if not G.claim_nonce(nonce_ledger_dir, promotion_manifest.nonce):
        return GateResult(ok=False, candidate_sha=candidate_sha, controls=controls,
                          refusals=[f"nonce {promotion_manifest.nonce!r} already consumed "
                                    f"(replay refused)"], nonce_claimed=False, reanchored=False)

    # Authority claimed → perform the re-anchor write as the final transaction step.
    # If it fails, the authority is spent (safe direction: no replay with this
    # nonce; a fresh supervised manifest+nonce is required).
    try:
        reanchor_fn(candidate_sha)
    except Exception as e:  # noqa: BLE001 — surface any writer failure as a refusal
        return GateResult(ok=False, candidate_sha=candidate_sha, controls=controls,
                          refusals=[f"re-anchor write failed AFTER nonce consumed "
                                    f"(authority spent; mint a fresh manifest): {e}"],
                          nonce_claimed=True, reanchored=False)

    return GateResult(ok=True, candidate_sha=candidate_sha, controls=controls,
                      refusals=[], nonce_claimed=True, reanchored=True)


def _build_check_parser(sub):
    c = sub.add_parser("check", help="run all three controls (dry-run; no nonce claim, no write)")
    c.add_argument("--repo", required=True, help="the TRUSTED checkout (verifier authority)")
    c.add_argument("--target-root", required=True, help="the EVALUATED candidate tree (data)")
    c.add_argument("--candidate-ref", default="HEAD", help="candidate ref in the target (default HEAD)")
    c.add_argument("--prior-anchor", required=True, help="the trusted prior anchor SHA")
    c.add_argument("--baseline-ref", default=None, help="the oracle's pre-refactor baseline ref")
    c.add_argument("--trusted-ref", default=None, help="the oracle's out-of-band trusted ref")
    c.add_argument("--promotion-manifest", required=True, help="path to the promotion manifest")
    c.add_argument("--activation", required=True, help="path to the evaluated activation artifact")
    c.add_argument("--trusted-activation", required=True,
                   help="path to the externally-supplied trusted activation expectation")
    c.add_argument("--nonce-ledger", required=True, help="the single externally-anchored nonce ledger dir")
    return c


def _check_cmd(args) -> int:
    """The supervised pre-check: controls only. Never claims the nonce or writes —
    it passes a reanchor_fn that raises if (impossibly) reached, and a throwaway
    ledger so a real nonce is never consumed by a dry run."""
    import tempfile
    manifest = G.parse_promotion(Path(args.promotion_manifest).read_text(encoding="utf-8"))
    trusted = A.parse_activation(Path(args.trusted_activation).read_text(encoding="utf-8"))

    def _must_not_write(_sha):
        raise AssertionError("dry-run reanchor_fn reached — refusing to write")

    with tempfile.TemporaryDirectory(prefix="cairn-reanchor-check-") as td:
        # A dry run reports the control sweep. To guarantee no real nonce burn, it
        # runs against a THROWAWAY ledger; the authoritative claim happens only in
        # a real `promote`. We stop before the write by intercepting reanchor_fn.
        res = run_reanchor_gate(
            trusted_repo=Path(args.repo), target_repo=Path(args.target_root),
            candidate_ref=args.candidate_ref, prior_anchor=args.prior_anchor,
            promotion_manifest=manifest, trusted_expectation=trusted,
            evaluated_activation_path=args.activation,
            nonce_ledger_dir=Path(td) / "throwaway",
            oracle_workdir=Path(td) / "wd", reanchor_fn=_must_not_write,
            baseline_ref=args.baseline_ref, trusted_ref=args.trusted_ref)
    print(f"[reanchor-check] candidate {(res.candidate_sha or '?')[:12]}")
    for name, ok in res.controls.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if res.ok or all(res.controls.values()):
        print("[reanchor-check] all controls PASS — a supervised `promote` would proceed.")
        return 0
    print("[reanchor-check] HOLD — controls refuse:", file=sys.stderr)
    for r in res.refusals:
        print(f"  {r}", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="gate_reanchor", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    _build_check_parser(sub)
    args = ap.parse_args(argv)
    if args.cmd == "check":
        return _check_cmd(args)
    ap.error(f"unknown command {args.cmd!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
