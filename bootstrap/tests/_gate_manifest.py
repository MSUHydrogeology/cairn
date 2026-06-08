#!/usr/bin/env python3
"""Gate-integrity manifest — six-proposal superplan pre-run gate-control prerequisite.

"Tests green" is not an independent gate when the same unattended actor that the
gate governs may weaken, delete, skip, xfail, re-baseline, or allow-list the very
test that failed (Codex S2 / R2-2). This tool freezes a **pre-run manifest** of
what the gate surface *is*, so any later tampering is mechanically detectable.

Two file classes
----------------

* **Frozen set** — every pre-existing test, harness, scanner, and fixture whose
  content defines a gate's pass/fail semantics. Discovered by glob
  (``bootstrap/tests/**/*.py`` + ``bootstrap/tests/fixtures/**`` + ``scripts/*.py``)
  and byte-hashed. During the batch, **modifying or deleting a frozen file HOLDs
  by default**; *adding* a new test file is allowed and recorded. The unattended
  run must NOT decide that an edit to an existing gate is merely "strengthening."

* **Cascade-mutable set** — ``config.py``, ``scaffold_ast_baseline.json``, and the
  frozen-engine ``scaffold_frozen.py`` legitimately change as A/B/C/E add an
  ``InstallSpec`` to a registry mapping symbol. These are **excluded from frozen
  hashing**; their integrity is governed by the AST source-motion attest (one
  symbol delta), the hardened ``_ast_attest.py update-symbol`` (one allowlisted
  baseline key, ``--expect-old`` guarded), and the differential oracle (frozen
  engine lockstep). The manifest records their pre-run hashes + the three pinned
  mapping-symbol digests so the end reviewer sees the before-state and the
  per-phase deltas — but the verifier does not HOLD on their change.

Collection identity
-------------------

The manifest pins the **set of pytest node-IDs** plus the **identities of any
skip/xfail-marked nodes** (not merely counts — Codex R2-2). A dropped node
(reduced collection) or a node that *gains* a skip/xfail marker HOLDs; added
nodes are allowed and recorded.

External anchor
---------------

The manifest lives at ``bootstrap/tests/fixtures/gate_manifest.json``, committed
in the supervised pre-run prerequisite commit. ``verify --anchor-ref <SHA>``
reads the expected manifest from that **immutable git object**
(``git show <SHA>:<manifest>``) and HOLDs if the working-tree manifest differs —
so the unattended actor cannot change both the artifact and its anchor. Run the
verifier from a trusted checkout (the main ``master`` clone, not the batch
worktree) so a tampered worktree copy of *this tool* cannot whitewash itself.

Usage
-----

    python bootstrap/tests/_gate_manifest.py produce > bootstrap/tests/fixtures/gate_manifest.json
    python bootstrap/tests/_gate_manifest.py verify --anchor-ref <PREREQ_SHA>

All gate work runs under the canonical interpreter (lhm / Python 3.13); the
verifier HOLDs if the running interpreter's *minor* differs from the pinned one
(``ast.dump`` / oracle digests are interpreter-minor sensitive). Stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = "cairn-gate-manifest/v1"
_REPO = Path(__file__).resolve().parents[2]
_MANIFEST_REL = "bootstrap/tests/fixtures/gate_manifest.json"
_TESTDIR_REL = "bootstrap/tests"

# Legitimately mutated by the cascade — EXCLUDED from frozen hashing; integrity
# governed by the named mechanism, not a byte hash.
CASCADE_MUTABLE: dict[str, str] = {
    "bootstrap/_scaffold/config.py":
        "AST source-motion attest — one predeclared mapping-symbol delta only (A/B/C/E)",
    "bootstrap/tests/fixtures/scaffold_ast_baseline.json":
        "_ast_attest.py update-symbol — one allowlisted baseline key, --expect-old guarded",
    "bootstrap/tests/fixtures/frozen_engine/scaffold_frozen.py":
        "differential oracle — frozen-engine _MODULE_MAPPINGS lockstep",
}

# Which phases may legitimately change each registry mapping symbol's digest.
MAPPING_SYMBOLS_PHASES: dict[str, list[str]] = {
    "_MODULE_MAPPINGS": ["A intent-split", "B onboarding-split", "C metrics fold-up"],
    "_SKILLS_MAPPINGS": ["E mechanization skill register"],
    "_CORE_MAPPINGS": ["E (heavier R6 pytest-wrapper option only)"],
}

# Canonical gate commands, recorded as data (run under `python` == lhm/3.13).
GATE_COMMANDS: list[dict] = [
    {"id": "bootstrap-suite",
     "cmd": ["python", "-m", "pytest", "bootstrap/tests/", "-q"],
     "expect": "all green; 0 skipped / 0 xfailed (the dev Bandit gate, AST attest, "
               "differential oracle, and loader-identity tests all run inside this suite)"},
    {"id": "ast-attest-verify",
     "cmd": ["python", "bootstrap/tests/_ast_attest.py", "verify",
             "bootstrap/tests/fixtures/scaffold_ast_baseline.json",
             "bootstrap/_scaffold/*.py"],
     "expect": "exit 0 — every baselined symbol accounted for unchanged; the ONLY "
               "permitted CHANGED is the predeclared one-symbol mapping delta"},
    {"id": "check-cairn",
     "cmd": ["python", "scripts/check_cairn.py"],
     "expect": "green"},
    {"id": "quality-gate-neutrality",
     "cmd": ["python", "scripts/quality_gate.py", "--sub", "neutrality"],
     "expect": "green"},
]

_INTERPRETER_NOTE = ("ast.dump / differential-oracle digests are interpreter-minor "
                     "sensitive; every gate runs under the canonical lhm/3.13 interpreter")


def _sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _frozen_files(repo: Path = _REPO) -> list[str]:
    """Discover the frozen gate surface by glob, minus cascade-mutable files and
    the manifest artifact itself."""
    exclude = set(CASCADE_MUTABLE) | {_MANIFEST_REL}
    found: set[str] = set()
    # ``bootstrap/*.py`` (top-level, NON-recursive) freezes the gate-defining engine
    # modules — security_check.py (the single source of the Bandit ALLOWLIST +
    # scan_targets), verify_integrity.py, check_module_body_coverage.py, and the
    # scaffold.py launcher — which the in-suite security/integrity gates import. The
    # cascade edits ``bootstrap/_scaffold/config.py`` (a subdir, not matched here),
    # so these stay frozen; a launcher change during the batch is a deliberate HOLD.
    for pattern in ("bootstrap/*.py", "bootstrap/tests/**/*.py",
                    "bootstrap/tests/fixtures/**/*", "scripts/*.py"):
        for p in repo.glob(pattern):
            if not p.is_file() or "__pycache__" in p.parts:
                continue
            rel = p.relative_to(repo).as_posix()
            if rel in exclude:
                continue
            found.add(rel)
    return sorted(found)


# --- pytest plugin hook: active ONLY when CAIRN_GATE_COLLECT_OUT is set ----------
# Loaded via `-p bootstrap.tests._gate_manifest` from the _collect subprocess; a
# no-op for any normal pytest run (the module is never auto-registered as a plugin).
def pytest_collection_modifyitems(items):  # noqa: D401 (pytest hook)
    dest = os.environ.get("CAIRN_GATE_COLLECT_OUT")
    if not dest:
        return
    collected: list[str] = []
    marked: list[str] = []
    for it in items:
        collected.append(it.nodeid)
        if (it.get_closest_marker("skip") or it.get_closest_marker("skipif")
                or it.get_closest_marker("xfail")):
            marked.append(it.nodeid)
    Path(dest).write_text(json.dumps({"collected": collected, "marked": marked}),
                          encoding="utf-8")


def _collect(repo: Path = _REPO) -> tuple[list[str], list[str], int]:
    """Collect node-IDs + skip/xfail-marked identities via a clean subprocess."""
    fd, out_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        env = dict(os.environ, CAIRN_GATE_COLLECT_OUT=out_path)
        r = subprocess.run(
            [sys.executable, "-m", "pytest", _TESTDIR_REL, "--collect-only", "-q",
             "-p", "bootstrap.tests._gate_manifest", "-p", "no:cacheprovider"],
            cwd=str(repo), env=env, capture_output=True, text=True,
        )
        try:
            data = json.loads(Path(out_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return [], [], (r.returncode or 1)
        return sorted(data.get("collected", [])), sorted(data.get("marked", [])), r.returncode
    finally:
        Path(out_path).unlink(missing_ok=True)


def produce(repo: Path = _REPO) -> dict:
    """Build the gate-integrity manifest dict from the current tree."""
    collected, marked, rc = _collect(repo)
    if rc != 0:
        raise RuntimeError(
            f"pytest collection failed (rc={rc}); refusing to produce a manifest over "
            f"a non-collecting suite")
    if not collected:
        # Defence-in-depth: a real suite has hundreds of nodes. An empty set means
        # the collection plugin hook did not run (env stripped / plugin shadowed)
        # even though pytest exited 0 — refuse rather than pin a vacuous manifest.
        raise RuntimeError(
            "pytest collected zero nodes; refusing to pin a vacuous collection manifest")
    frozen = {rel: _sha256(repo / rel) for rel in _frozen_files(repo)}
    cascade = {
        rel: {"pre_run_sha256": _sha256(repo / rel), "governed_by": why}
        for rel, why in sorted(CASCADE_MUTABLE.items())
        if (repo / rel).is_file()
    }
    baseline = json.loads((repo / "bootstrap/tests/fixtures/scaffold_ast_baseline.json")
                          .read_text(encoding="utf-8"))
    mappings = {}
    for sym, phases in MAPPING_SYMBOLS_PHASES.items():
        entry = baseline.get(f"Assign:{sym}")
        if entry is None:
            raise RuntimeError(f"mapping symbol Assign:{sym} not present in the AST baseline")
        mappings[sym] = {"baseline_digest": entry["digest"], "may_change_in_phases": phases}
    return {
        "schema": SCHEMA,
        "interpreter": {
            "version": ".".join(map(str, sys.version_info[:3])),
            "version_info": list(sys.version_info[:3]),
            "note": _INTERPRETER_NOTE,
        },
        "gate_commands": GATE_COMMANDS,
        "collection": {
            "node_count": len(collected),
            "node_ids": collected,
            "skip_xfail_marked": marked,
        },
        "frozen_files": frozen,
        "cascade_mutable": cascade,
        "mapping_symbols": mappings,
    }


def verify(manifest_path: str | Path, *, anchor_ref: str | None = None,
           repo: Path = _REPO, out=None) -> int:
    """Verify gate integrity against a manifest. 0 = intact (additions allowed),
    1 = HOLD (a gate-integrity violation)."""
    if out is None:
        out = sys.stderr
    manifest_path = Path(manifest_path)
    live_text = manifest_path.read_text(encoding="utf-8")
    manifest = json.loads(live_text)
    holds: list[str] = []
    notes: list[str] = []

    # 1) External git anchor — the working-tree manifest must equal the immutable object.
    if anchor_ref:
        r = subprocess.run(["git", "show", f"{anchor_ref}:{_MANIFEST_REL}"],
                           cwd=str(repo), capture_output=True, text=True)
        if r.returncode != 0:
            holds.append(f"ANCHOR: cannot read the manifest from {anchor_ref}: "
                         f"{r.stderr.strip() or 'git show failed'}")
        elif r.stdout != live_text:
            holds.append(f"ANCHOR: working-tree manifest differs from the immutable "
                         f"{anchor_ref} object — the manifest itself was altered")
    else:
        notes.append("ANCHOR: skipped (no --anchor-ref; REQUIRED for the unattended batch)")

    # 2) Interpreter minor must match (patch may differ).
    pin = manifest["interpreter"]["version_info"]
    if list(sys.version_info[:2]) != list(pin[:2]):
        holds.append(f"INTERPRETER: running {tuple(sys.version_info[:2])} != pinned "
                     f"{tuple(pin[:2])} — ast.dump/oracle digests are minor-sensitive")
    elif list(sys.version_info[:3]) != list(pin[:3]):
        notes.append(f"INTERPRETER: patch differs (running "
                     f"{'.'.join(map(str, sys.version_info[:3]))} vs pinned "
                     f"{'.'.join(map(str, pin[:3]))}); minor matches — ok")

    # 3) Frozen files — modification / removal HOLDs; new files are recorded.
    pinned_frozen = manifest["frozen_files"]
    current_frozen = {rel: _sha256(repo / rel) for rel in _frozen_files(repo)}
    for rel, h in pinned_frozen.items():
        if rel not in current_frozen:
            holds.append(f"FROZEN-MISSING: {rel} (a pinned gate file was removed)")
        elif current_frozen[rel] != h:
            holds.append(f"FROZEN-MODIFIED: {rel} (gate file edited — sha differs)")
    for rel in sorted(set(current_frozen) - set(pinned_frozen)):
        notes.append(f"FROZEN-NEW: {rel} (new gate/test file — allowed, recorded)")

    # 4) Collection identity — dropped node or new skip/xfail HOLDs; added recorded.
    collected, marked, rc = _collect(repo)
    if rc != 0:
        holds.append(f"COLLECTION: pytest collection failed (rc={rc})")
    pinned_ids = set(manifest["collection"]["node_ids"])
    cur_ids = set(collected)
    for nid in sorted(pinned_ids - cur_ids):
        holds.append(f"COLLECTION-DROPPED: {nid} (reduced test collection)")
    pinned_marked = set(manifest["collection"]["skip_xfail_marked"])
    for nid in sorted(set(marked) - pinned_marked):
        holds.append(f"SKIP-XFAIL-NEW: {nid} (a test gained a skip/xfail marker)")
    for nid in sorted(cur_ids - pinned_ids):
        notes.append(f"COLLECTION-ADDED: {nid} (new test — allowed, recorded)")

    # 5) Cascade-mutable + mapping digests — report deltas, never HOLD.
    for rel, info in manifest["cascade_mutable"].items():
        cur = _sha256(repo / rel) if (repo / rel).is_file() else "<absent>"
        if cur != info["pre_run_sha256"]:
            notes.append(f"CASCADE-CHANGED: {rel} (governed by: {info['governed_by']})")
    baseline_p = repo / "bootstrap/tests/fixtures/scaffold_ast_baseline.json"
    if baseline_p.is_file():
        baseline = json.loads(baseline_p.read_text(encoding="utf-8"))
        for sym, info in manifest["mapping_symbols"].items():
            cur = baseline.get(f"Assign:{sym}", {}).get("digest")
            if cur != info["baseline_digest"]:
                notes.append(f"MAPPING-DIGEST-CHANGED: {sym} {info['baseline_digest']} -> "
                             f"{cur} (allowed phases: {', '.join(info['may_change_in_phases'])})")

    for n in notes:
        print(f"[gate-manifest] note: {n}", file=out)
    if holds:
        print(f"[gate-manifest] HOLD — {len(holds)} gate-integrity violation(s):", file=out)
        for h in holds:
            print(f"  {h}", file=out)
        return 1
    print(f"[gate-manifest] OK — gate integrity intact "
          f"({len(pinned_frozen)} frozen files, {len(pinned_ids)} pinned nodes, "
          f"{len(notes)} note(s))", file=out)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="gate_manifest", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("produce", help="emit the gate-integrity manifest JSON to stdout")
    v = sub.add_parser("verify", help="verify gate integrity against a manifest")
    v.add_argument("--manifest", default=str(_REPO / _MANIFEST_REL))
    v.add_argument("--anchor-ref", default=None,
                   help="git ref/sha holding the immutable manifest (the prerequisite commit)")
    args = ap.parse_args(argv)
    if args.cmd == "produce":
        json.dump(produce(), sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    return verify(args.manifest, anchor_ref=args.anchor_ref)


if __name__ == "__main__":
    raise SystemExit(main())
