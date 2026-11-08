#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Replay the sealed ordinary C2 redundancy and evolution probes.

Use separate, clean committed old/new checkouts:
  python scripts/replay_ordinary_c2_mutants.py --old /tmp/old --new /tmp/new \
    --output /tmp/c2-mutant-results

The sealed fifteen patches and the later R1 public-aggregation probe live in
bootstrap/tests/fixtures/ordinary_c2_promise_mutants.json. Each run tests its
owning integration file. Engine bytes are restored after every mutation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "bootstrap" / "tests" / "fixtures" / "ordinary_c2_promise_mutants.json"
PYTHON = sys.executable
TESTS = {
    "redundancy": "bootstrap/tests/integration/test_quality_gate_redundancy.py",
    "evolution": "bootstrap/tests/integration/test_evolution_infer.py",
}


def _load_mutants() -> tuple[list[dict], dict]:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    mutants = data["mutants"]
    if len(mutants) != 15:
        raise ValueError("the sealed C2 set must contain exactly 15 mutants")
    seal = "".join(
        f"{item['id']} {item['tuple_sha256']}\n" for item in mutants
    ).encode("utf-8")
    if hashlib.sha256(seal).hexdigest() != data["list_sha256"]:
        raise ValueError("the sealed C2 list digest does not match")
    for item in mutants:
        original = (item["id"], item["source"], item["old"], item["new"])
        digest = hashlib.sha256(
            json.dumps(original, ensure_ascii=True).encode("utf-8")
        ).hexdigest()
        if digest != item["tuple_sha256"]:
            raise ValueError(f"sealed mutation changed: {item['id']}")
    return mutants, data["candidate_only_probe"]


def _clean_checkout(path: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(path), "status", "--porcelain"],
        capture_output=True, text=True, check=False,
    )
    return result.returncode == 0 and not result.stdout.strip()


def _run_test(root: Path, test_path: str, log: Path) -> tuple[int, float]:
    started = time.monotonic()
    result = subprocess.run(
        [PYTHON, "-m", "pytest", test_path, "-q", "--tb=short",
         "-p", "no:cacheprovider"],
        cwd=root, capture_output=True, text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        timeout=180,
    )
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    return result.returncode, round(time.monotonic() - started, 3)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old", type=Path, required=True)
    parser.add_argument("--new", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--only", help="run one sealed mutation ID")
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 13):
        parser.error("use canonical Python 3.13")
    old, new = args.old.resolve(), args.new.resolve()
    if old == new:
        parser.error("old and new must be separate checkouts")
    mutants, extra = _load_mutants()
    choices = {item["id"] for item in mutants} | {extra["id"]}
    if args.only and args.only not in choices:
        parser.error(f"--only must be one of: {', '.join(sorted(choices))}")
    selected = [item for item in mutants if not args.only or item["id"] == args.only]
    if not args.only or args.only == extra["id"]:
        selected.append(extra)
    args.output.mkdir(parents=True, exist_ok=True)
    for checkout in (old, new):
        if not _clean_checkout(checkout):
            parser.error(f"checkout must be clean: {checkout}")
    target_paths = {item["target"] for item in selected}
    for path in target_paths:
        if (old / path).read_bytes() != (new / path).read_bytes():
            parser.error(f"old/new implementation source differs: {path}")

    results = []
    for label, checkout in (("old", old), ("new", new)):
        for item in selected:
            target = checkout / item["target"]
            original = target.read_text(encoding="utf-8")
            if original.count(item["old"]) != 1:
                parser.error(f"mutation target is not unique: {item['id']}")
            test_path = TESTS[item["family"]]
            prefix = f"{label}-{item['id']}"
            baseline_code, baseline_seconds = _run_test(
                checkout, test_path, args.output / f"{prefix}-baseline.log",
            )
            if baseline_code:
                parser.error(f"healthy test family failed: {prefix}")
            try:
                target.write_text(
                    original.replace(item["old"], item["new"], 1),
                    encoding="utf-8",
                )
                mutant_code, mutant_seconds = _run_test(
                    checkout, test_path, args.output / f"{prefix}-mutant.log",
                )
            finally:
                target.write_text(original, encoding="utf-8")
            if not _clean_checkout(checkout):
                raise RuntimeError(f"mutation did not restore clean bytes: {prefix}")
            caught = mutant_code != 0
            results.append({
                "id": item["id"], "version": label, "family": item["family"],
                "test": test_path, "baseline_seconds": baseline_seconds,
                "mutant_seconds": mutant_seconds, "caught": caught,
                "mutant_exit": mutant_code,
            })
            print(label, item["id"], "caught" if caught else "SURVIVED", flush=True)
    (args.output / "results.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8",
    )
    return int(any(not row["caught"] for row in results if row["version"] == "new"))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
