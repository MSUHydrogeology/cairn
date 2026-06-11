#!/usr/bin/env python3
"""Phase 4 — the single **authoritative** supervised re-anchor gate.

The code-review re-reviews (Codex, 2026-06-11) drove this from "three correct but
uncomposed controls" to one fail-closed transaction. Round 3 closed the remaining
**authority** boundary: the success path must not be dependency-injectable, the
candidate binding must be unconditional, the nonce ledger must be **owned** (not
caller-selectable), and the re-anchor write must be **atomic and verified**.

Two entry points
----------------
* :func:`promote` — the **production** command (and the ``promote`` CLI). Its path
  is **not** dependency-injectable: it owns the real differential oracle, derives
  the **one** nonce ledger from externally trusted state, runs a **real atomic
  gate-manifest writer**, and **verifies the resulting manifest** (the
  postcondition) before reporting success. A no-op or wrong writer cannot report
  success — the postcondition catches it. It refuses unless explicitly confirmed
  for a supervised re-anchor; *running* it against the real tree is the
  Maintainer's supervised act.
* :func:`_run_reanchor_gate` — the **internal** transaction engine with injectable
  seams (oracle / writer / postcondition). It is **test-only** — exercised by the
  regressions to drive each control and each failure mode. ``promote`` is the only
  non-test caller, and it injects the real implementations.

Authority discipline (unchanged, now enforced end to end)
---------------------------------------------------------
* **One immutable candidate.** Every control is bound to one resolved candidate
  SHA; the oracle report MUST carry that exact SHA (missing is a refusal). The
  worktree must be clean and at that SHA.
* **Fail without consuming authority.** Any control failure returns before the
  nonce claim and before any write.
* **Owned ledger.** ``promote`` derives the single ledger from the trusted repo +
  prior anchor; there is no public override (no alternate-ledger replay).
* **Atomic + verified write.** The real writer regenerates the manifest, writes it
  via temp-file + ``os.replace`` (atomic), then the postcondition re-derives and
  byte-compares — a write that did not faithfully land cannot be reported as a
  successful re-anchor.

Stdlib only. Run from the trusted ``master`` checkout, target the candidate tree.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

try:  # package import (pytest)
    from bootstrap.tests import _oracle as O
    from bootstrap.tests import _oracle_activation as A
    from bootstrap.tests import _gate_transition as G
    from bootstrap.tests import _gate_manifest as M
except ImportError:  # script mode
    import _oracle as O
    import _oracle_activation as A
    import _gate_transition as G
    import _gate_manifest as M

_MANIFEST_REL = "bootstrap/tests/fixtures/gate_manifest.json"
_ACTIVATION_REL = "dev/.cairn/active-refactor.yml"


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


def _derive_ledger(trusted_repo: Path, prior_anchor: str) -> Path:
    """The **one** nonce ledger, derived from externally trusted state (re-review
    round-3 Finding 3): a contained directory under the **trusted** repo, keyed by
    the prior anchor. It is a pure function of (trusted_repo, prior_anchor) — there
    is no caller override, so two promotions of one authority share one ledger and
    a second claim of a spent nonce refuses (no alternate-ledger replay)."""
    safe = "".join(c for c in prior_anchor if c in "0123456789abcdef")[:40] or "none"
    return Path(trusted_repo) / "bootstrap" / "tests" / "fixtures" / ".reanchor_nonce_ledger" / safe


def _atomic_write(dest: Path, data: bytes) -> None:
    """Atomic temp-write + ``os.replace`` (re-review round-3 Finding 4): the
    destination is never left partially written — a reader sees either the old file
    or the complete new one."""
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(dest.parent), prefix=".reanchor-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, dest)            # atomic on POSIX
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def _produce_manifest_text(target_repo: Path) -> str:
    """The canonical serialized gate manifest for *target_repo*'s current tree."""
    return json.dumps(M.produce(Path(target_repo)), indent=2, sort_keys=True) + "\n"


def _real_reanchor_writer(target_repo: Path, manifest_rel: str = _MANIFEST_REL) -> None:
    """The **real** re-anchor write (not injectable in ``promote``): regenerate the
    gate manifest from the promoted tree and write it atomically."""
    text = _produce_manifest_text(target_repo)
    _atomic_write(Path(target_repo) / manifest_rel, text.encode("utf-8"))


def _postcondition_manifest_written(target_repo: Path, manifest_rel: str = _MANIFEST_REL) -> bool:
    """Post-write verification (Finding 1 + 4): the on-disk manifest must byte-equal
    a freshly produced one. A no-op writer leaves the OLD manifest, which will not
    match the promoted tree's produce() — so success cannot be reported for a write
    that did not faithfully land."""
    dest = Path(target_repo) / manifest_rel
    if not dest.is_file():
        return False
    return dest.read_text(encoding="utf-8") == _produce_manifest_text(target_repo)


def _run_reanchor_gate(
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
    postcondition_fn=None,
    is_sensitive=A.is_sensitive,
) -> GateResult:
    """**Internal, test-only** transaction engine with injectable seams. Runs the
    three controls bound to one immutable candidate SHA; on a clean sweep,
    atomically claims the nonce and performs *reanchor_fn*, then requires
    *postcondition_fn* (if given) to confirm the write landed. ``promote`` is the
    only non-test caller and injects the **real** oracle / writer / postcondition.

    Seam params (*reanchor_fn*, *run_oracle_fn*, *postcondition_fn*,
    *nonce_ledger_dir*) exist for the regressions; production code must use
    :func:`promote`, whose path is not dependency-injectable."""
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

    # Control B — the differential oracle over EVERY required scenario, bound to the
    # candidate SHA. The report MUST carry that exact SHA — a missing/omitted
    # candidate identity is a refusal (round-3 Finding 2: no conditional skip).
    report = run_oracle_fn(oracle_workdir, baseline_ref=baseline_ref,
                           trusted_ref=trusted_ref, repo=trusted_repo,
                           target_root=target_repo, gate=True)
    ok_b, holds_b = _required_scenarios_covered(report, trusted_expectation.required_scenarios)
    if report.get("candidate_sha") != candidate_sha:
        ok_b = False
        holds_b = holds_b + [f"oracle report candidate {report.get('candidate_sha')!r} != "
                             f"{candidate_sha[:12]} (missing/mismatch refused)"]
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

    # Authority claimed → perform the re-anchor write. If it fails, authority is
    # spent (safe: no replay with this nonce; a fresh manifest+nonce is required).
    try:
        reanchor_fn(candidate_sha)
    except Exception as e:  # noqa: BLE001
        return GateResult(ok=False, candidate_sha=candidate_sha, controls=controls,
                          refusals=[f"re-anchor write failed AFTER nonce consumed "
                                    f"(authority spent; mint a fresh manifest): {e}"],
                          nonce_claimed=True, reanchored=False)

    # Post-write verification — the write must have faithfully landed. A no-op or
    # wrong writer fails here and CANNOT be reported as a successful re-anchor.
    if postcondition_fn is not None:
        try:
            verified = bool(postcondition_fn(candidate_sha))
        except Exception as e:  # noqa: BLE001
            verified = False
            controls["postcondition_error"] = False
            return GateResult(ok=False, candidate_sha=candidate_sha, controls=controls,
                              refusals=[f"post-write verification raised AFTER nonce consumed "
                                        f"(authority spent): {e}"],
                              nonce_claimed=True, reanchored=False)
        controls["postcondition"] = verified
        if not verified:
            return GateResult(ok=False, candidate_sha=candidate_sha, controls=controls,
                              refusals=["post-write verification failed AFTER nonce consumed: the "
                                        "manifest on disk does not match the promoted tree "
                                        "(no-op/incorrect writer; authority spent)"],
                              nonce_claimed=True, reanchored=False)

    return GateResult(ok=True, candidate_sha=candidate_sha, controls=controls,
                      refusals=[], nonce_claimed=True, reanchored=True)


def promote(
    *,
    trusted_repo: Path,
    target_repo: Path,
    prior_anchor: str,
    promotion_manifest_path: Path | str,
    trusted_activation_path: Path | str,
    candidate_ref: str = "HEAD",
    baseline_ref: str | None = None,
    trusted_ref: str | None = None,
    confirm: bool = False,
    oracle_workdir: Path | None = None,
) -> GateResult:
    """The **production** re-anchor command. Its path is NOT dependency-injectable:
    it owns the real differential oracle (:func:`_oracle.run_oracle`), derives the
    **one** nonce ledger from trusted state, runs the **real atomic** gate-manifest
    writer, and verifies the resulting manifest (postcondition) before success.

    *confirm* must be ``True`` — *running* this against the real tree is the
    Maintainer's supervised act; the gate refuses without explicit confirmation."""
    if not confirm:
        return GateResult(ok=False, candidate_sha=None,
                          refusals=["promote requires explicit supervised confirmation "
                                    "(confirm=True / --confirm-supervised-reanchor)"])
    manifest = G.parse_promotion(Path(promotion_manifest_path).read_text(encoding="utf-8"))
    trusted = A.parse_activation(Path(trusted_activation_path).read_text(encoding="utf-8"))
    ledger = _derive_ledger(trusted_repo, prior_anchor)             # OWNED, no override
    evaluated_activation = Path(target_repo) / _ACTIVATION_REL

    def _writer(_sha):
        _real_reanchor_writer(target_repo)

    def _postcond(_sha):
        return _postcondition_manifest_written(target_repo)

    workdir = Path(oracle_workdir) if oracle_workdir else None
    if workdir is None:
        td = tempfile.mkdtemp(prefix="cairn-promote-")
        workdir = Path(td)
    return _run_reanchor_gate(
        trusted_repo=Path(trusted_repo), target_repo=Path(target_repo),
        candidate_ref=candidate_ref, prior_anchor=prior_anchor,
        promotion_manifest=manifest, trusted_expectation=trusted,
        evaluated_activation_path=evaluated_activation,
        nonce_ledger_dir=ledger, oracle_workdir=workdir,
        reanchor_fn=_writer, postcondition_fn=_postcond,
        baseline_ref=baseline_ref, trusted_ref=trusted_ref,
        run_oracle_fn=O.run_oracle)                                  # REAL oracle, not injectable


# --------------------------------------------------------------------------- CLI

def _build_parsers(sub):
    for name, helptext in (("check", "run all three controls (dry-run; no nonce claim, no write)"),
                           ("promote", "SUPERVISED re-anchor: all controls + atomic verified write")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("--repo", required=True, help="the TRUSTED checkout (verifier authority)")
        p.add_argument("--target-root", required=True, help="the EVALUATED candidate tree (data)")
        p.add_argument("--candidate-ref", default="HEAD", help="candidate ref in the target (default HEAD)")
        p.add_argument("--prior-anchor", required=True, help="the trusted prior anchor SHA")
        p.add_argument("--baseline-ref", default=None, help="the oracle's pre-refactor baseline ref")
        p.add_argument("--trusted-ref", default=None, help="the oracle's out-of-band trusted ref")
        p.add_argument("--promotion-manifest", required=True, help="path to the promotion manifest")
        p.add_argument("--trusted-activation", required=True,
                       help="path to the externally-supplied trusted activation expectation")
        if name == "promote":
            p.add_argument("--confirm-supervised-reanchor", action="store_true",
                           help="REQUIRED: confirm this is the Maintainer's supervised re-anchor")


def _check_cmd(args) -> int:
    """Supervised dry-run: controls only. Never claims a real nonce or writes — it
    uses a throwaway ledger and a reanchor_fn that raises if (impossibly) reached."""
    manifest = G.parse_promotion(Path(args.promotion_manifest).read_text(encoding="utf-8"))
    trusted = A.parse_activation(Path(args.trusted_activation).read_text(encoding="utf-8"))

    def _must_not_write(_sha):
        raise AssertionError("dry-run reanchor_fn reached — refusing to write")

    with tempfile.TemporaryDirectory(prefix="cairn-reanchor-check-") as td:
        res = _run_reanchor_gate(
            trusted_repo=Path(args.repo), target_repo=Path(args.target_root),
            candidate_ref=args.candidate_ref, prior_anchor=args.prior_anchor,
            promotion_manifest=manifest, trusted_expectation=trusted,
            evaluated_activation_path=Path(args.target_root) / _ACTIVATION_REL,
            nonce_ledger_dir=Path(td) / "throwaway",
            oracle_workdir=Path(td) / "wd", reanchor_fn=_must_not_write,
            baseline_ref=args.baseline_ref, trusted_ref=args.trusted_ref)
    print(f"[reanchor-check] candidate {(res.candidate_sha or '?')[:12]}")
    for name, ok in res.controls.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if all(res.controls.get(k) for k in ("clean_worktree", "activation", "oracle", "promotion")):
        print("[reanchor-check] all controls PASS — a supervised `promote` would proceed.")
        return 0
    print("[reanchor-check] HOLD — controls refuse:", file=sys.stderr)
    for r in res.refusals:
        print(f"  {r}", file=sys.stderr)
    return 1


def _promote_cmd(args) -> int:
    res = promote(
        trusted_repo=Path(args.repo), target_repo=Path(args.target_root),
        candidate_ref=args.candidate_ref, prior_anchor=args.prior_anchor,
        promotion_manifest_path=args.promotion_manifest,
        trusted_activation_path=args.trusted_activation,
        baseline_ref=args.baseline_ref, trusted_ref=args.trusted_ref,
        confirm=bool(args.confirm_supervised_reanchor))
    print(f"[reanchor-promote] candidate {(res.candidate_sha or '?')[:12]}  "
          f"reanchored={res.reanchored}  nonce_claimed={res.nonce_claimed}")
    if res.ok:
        print("[reanchor-promote] OK — controls passed, nonce claimed, manifest re-anchored "
              "and verified.")
        return 0
    print("[reanchor-promote] HOLD — refused:", file=sys.stderr)
    for r in res.refusals:
        print(f"  {r}", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="gate_reanchor", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    _build_parsers(sub)
    args = ap.parse_args(argv)
    if args.cmd == "check":
        return _check_cmd(args)
    if args.cmd == "promote":
        return _promote_cmd(args)
    ap.error(f"unknown command {args.cmd!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
