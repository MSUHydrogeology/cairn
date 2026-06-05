#!/usr/bin/env python3
"""Differential-oracle harness — scaffold-split 0A.3 (P2#5 / P2#7 / RR4).

The scaffold-split refactor claims each extraction stage preserves *behavior*.
"Tests green" is not a sufficient security gate for a large code-motion refactor
(SR3): a semantic change can hide in thousands of moved lines while every unit
test still passes. This harness is the **behavioral** guard (the AST attestation
in ``_ast_attest.py`` is the *source-motion* guard; both are required).

What it does
------------
For each fixture in a **fixed, recorded matrix**, it:

1. runs a **frozen pre-split engine** (``fixtures/frozen_engine/scaffold_frozen.py``,
   a byte-copy of the pre-extraction monolith) and the **current** engine
   (``bootstrap/scaffold.py`` — the launcher+package once 0B lands), each as a
   subprocess installing into its own cloned adopter tree, with **identical
   templates** (same ``--cairn-root``) and the **same profile**;
2. **byte-compares** every installed file between the two trees;
3. **normalizes only the enumerated provenance fields** (``cairn_version`` /
   ``cairn_commit`` in the lockfile) so a commit/version advancing *between* the
   two runs cannot masquerade as a behavior diff. A broad normalization that
   could hide a content diff is rejected (P2#5) — in particular **per-file
   content hashes are NOT normalized**: they are the content guard;
4. enumerates the **location-dependent** untracked files (the interpreter
   binding embeds each tree's own absolute path, so it differs by construction)
   — presence parity is still asserted, but bytes are not compared;
5. emits a **machine-readable JSON report** so the per-stage gate is bounded and
   auditable rather than a hand-recorded "green" (P2#7).

At Stage 0A the current engine *is* the frozen engine, so the oracle is a
tautology that proves the harness itself is sound; its teeth bite at Stages 1–8.

Run::

    python bootstrap/tests/_oracle.py run --report /tmp/oracle.json
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_TESTS_DIR = Path(__file__).resolve().parent
CAIRN_ROOT = _TESTS_DIR.parent.parent
FROZEN_ENGINE = _TESTS_DIR / "fixtures" / "frozen_engine" / "scaffold_frozen.py"
CURRENT_ENGINE = CAIRN_ROOT / "bootstrap" / "scaffold.py"

REPORT_SCHEMA = "cairn.scaffold_split.oracle/v1"

# The fixed, recorded fixture matrix (P2#7: bounded + auditable). The three
# shipped presets span minimal -> rich module rosters, so the install path is
# exercised across core + skills + onboarding + the team-gated module set.
FIXTURES: tuple[dict[str, str], ...] = (
    {"name": "solo-greenfield", "preset": "solo-greenfield"},
    {"name": "collaborative-team", "preset": "collaborative-team"},
    {"name": "high-rigor-legacy", "preset": "high-rigor-legacy"},
)

# Enumerated provenance fields normalized in the lockfile before byte-compare
# (and NOTHING else). Per-file hashes are deliberately excluded from this set.
_PROVENANCE_KEYS: tuple[str, ...] = ("cairn_version", "cairn_commit")
_LOCKFILE_REL = "dev/.cairn/cairn-lock.yml"

# Enumerated location-dependent exclusions: untracked files that embed the
# adopter tree's own absolute path / interpreter binding, which differ by
# construction (the two runs install into different temp roots). Presence parity
# is asserted; bytes are not compared. Recorded so the surface is auditable.
_LOCATION_DEPENDENT: frozenset[str] = frozenset({"dev/.cairn/local-env.json"})


class OracleError(RuntimeError):
    """A fixture failed to install under one of the engines (a run error, not a diff)."""


def _profile_text(preset: str) -> str:
    return f'project_name: "OracleFixture"\ntest_command: "pytest"\npreset: {preset}\n'


def _run_engine(engine: Path, target: Path, preset: str) -> None:
    target.mkdir(parents=True, exist_ok=True)
    cfg = target / "profile.yml"
    cfg.write_text(_profile_text(preset), encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable, str(engine),
            "--config", str(cfg),
            "--target", str(target),
            "--cairn-root", str(CAIRN_ROOT),
            "--allow-dev", "--non-interactive",
        ],
        capture_output=True, text=True, cwd=str(CAIRN_ROOT), check=False,
    )
    if proc.returncode != 0:
        raise OracleError(
            f"engine {engine.name} failed on preset {preset!r} (rc={proc.returncode})\n"
            f"--- stderr ---\n{proc.stderr[-2000:]}\n--- stdout ---\n{proc.stdout[-1000:]}"
        )


def _snapshot(target: Path) -> dict[str, bytes]:
    """Map ``{relative_posix_path: bytes}`` for every file under ``target``,
    excluding the profile.yml we wrote in and any VCS dir."""
    out: dict[str, bytes] = {}
    for p in sorted(target.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(target).as_posix()
        if rel == "profile.yml" or rel.startswith(".git/"):
            continue
        out[rel] = p.read_bytes()
    return out


def _normalize(rel: str, data: bytes) -> bytes:
    """Normalize ONLY the enumerated provenance fields, ONLY in the lockfile."""
    if rel != _LOCKFILE_REL:
        return data
    text = data.decode("utf-8")
    for key in _PROVENANCE_KEYS:
        # Top-level YAML key only (column 0): per-file hash:/base_hash: are
        # indented under files: and are left untouched (they are the guard).
        text = re.sub(rf"(?m)^({re.escape(key)}:).*$", rf"\1 <pinned>", text)
    return text.encode("utf-8")


def _compare(frozen: dict[str, bytes], current: dict[str, bytes]) -> list[dict]:
    diffs: list[dict] = []
    for rel in sorted(set(frozen) - set(current)):
        diffs.append({"path": rel, "kind": "only_in_frozen"})
    for rel in sorted(set(current) - set(frozen)):
        diffs.append({"path": rel, "kind": "only_in_current"})
    for rel in sorted(set(frozen) & set(current)):
        if rel in _LOCATION_DEPENDENT:
            continue  # presence parity already proven above; bytes are location-bound
        if _normalize(rel, frozen[rel]) != _normalize(rel, current[rel]):
            diffs.append({
                "path": rel,
                "kind": "bytes_differ",
                "frozen_len": len(frozen[rel]),
                "current_len": len(current[rel]),
            })
    return diffs


def run_oracle(workdir: Path) -> dict:
    if not FROZEN_ENGINE.is_file():
        raise OracleError(f"frozen engine snapshot missing: {FROZEN_ENGINE}")
    fixtures_report: list[dict] = []
    for fx in FIXTURES:
        froot = workdir / fx["name"] / "frozen"
        croot = workdir / fx["name"] / "current"
        _run_engine(FROZEN_ENGINE, froot, fx["preset"])
        _run_engine(CURRENT_ENGINE, croot, fx["preset"])
        fsnap, csnap = _snapshot(froot), _snapshot(croot)
        diffs = _compare(fsnap, csnap)
        fixtures_report.append({
            "name": fx["name"],
            "preset": fx["preset"],
            "status": "match" if not diffs else "diff",
            "frozen_file_count": len(fsnap),
            "current_file_count": len(csnap),
            "diffs": diffs,
        })
    return {
        "schema": REPORT_SCHEMA,
        "frozen_engine": str(FROZEN_ENGINE.relative_to(CAIRN_ROOT)),
        "current_engine": str(CURRENT_ENGINE.relative_to(CAIRN_ROOT)),
        "normalized_provenance_fields": list(_PROVENANCE_KEYS),
        "location_dependent_excluded": sorted(_LOCATION_DEPENDENT),
        "fixtures": fixtures_report,
        "ok": all(f["status"] == "match" for f in fixtures_report),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="oracle", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run the differential oracle over the fixture matrix")
    r.add_argument("--report", default=None, help="write the machine-readable JSON report here")
    r.add_argument("--workdir", default=None, help="reuse a directory instead of a fresh tempdir")
    args = parser.parse_args(argv)

    if args.workdir:
        report = run_oracle(Path(args.workdir))
    else:
        with tempfile.TemporaryDirectory(prefix="cairn-oracle-") as td:
            report = run_oracle(Path(td))

    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for fx in report["fixtures"]:
        line = f"  {fx['status'].upper():5}  {fx['name']:20}  {fx['frozen_file_count']} file(s)"
        if fx["status"] != "match":
            line += f"  -- {len(fx['diffs'])} diff(s)"
        print(line)
    if report["ok"]:
        print(f"oracle: OK -- {len(report['fixtures'])} fixture(s), behavior preserved.")
        return 0
    print("oracle: FAILED -- behavioral divergence between frozen and current engine:", file=sys.stderr)
    for fx in report["fixtures"]:
        for d in fx["diffs"]:
            print(f"  [{fx['name']}] {d['kind']}: {d['path']}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
