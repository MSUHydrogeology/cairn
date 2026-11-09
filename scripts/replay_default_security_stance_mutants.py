#!/usr/bin/env python3
"""Replay the four sealed default-security witness mutants on a private copy."""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "bootstrap/tests/fixtures/default_security_stance_promise_mutants.json"
DATA_SHA256 = "380d2e78e177736f9430793647332fe7e78db9c48b5345132800a72f7b7ec4b4"
TEST = "bootstrap/tests/test_default_security_stance.py"
OLD_NODE = "test_an_unfilled_python_package_token_does_not_select"
NODES = {
    "S1-exact-summary-default": "test_the_profile_summary_names_the_token_gated_addition",
    "S2-exact-summary-token": "test_the_profile_summary_names_the_token_gated_addition",
    "U1-new-core-conscripts-module": "test_a_new_default_on_module_stays_opt_in_for_an_existing_adopter",
    "U2-adoption-conscripts-module": "test_a_new_default_on_module_stays_opt_in_for_an_existing_adopter",
}
TARGETS = {
    "bootstrap/_scaffold/cli.py",
    "bootstrap/_scaffold/upgrade.py",
}
CHILD = r'''
import json, sys, pytest
from pathlib import Path
source = str(Path(sys.argv[1]).resolve())
lines, reports = set(), []
def trace(frame, event, arg):
    if frame.f_code.co_filename == source:
        if event == "line": lines.add(frame.f_lineno)
        return trace
    return None
class Reports:
    def pytest_runtest_logreport(self, report):
        reports.append([report.when, report.outcome])
sys.settrace(trace)
code = pytest.main([sys.argv[2], "-q", "--tb=short", "-p", "no:cacheprovider"], plugins=[Reports()])
sys.settrace(None)
Path(sys.argv[3]).write_text(json.dumps({"code": int(code), "lines": sorted(lines), "reports": reports}))
raise SystemExit(int(code))
'''


def _run(root: Path, target: str, node: str) -> dict:
    report = root / "probe-report.json"
    result = subprocess.run(
        [sys.executable, "-c", CHILD, str(root / target), f"{TEST}::{node}", str(report)],
        cwd=root, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90,
    )
    if not report.is_file():
        raise RuntimeError(f"pytest produced no report: {result.stdout[-1200:]}")
    data = json.loads(report.read_text(encoding="utf-8"))
    data["output"] = result.stdout[-1200:]
    return data


def _exclude_old_cases(root: Path) -> None:
    path = root / TEST
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    node = next(
        item for item in tree.body
        if isinstance(item, ast.FunctionDef) and item.name == OLD_NODE
    )
    start = min([node.lineno, *(decorator.lineno for decorator in node.decorator_list)])
    lines = source.splitlines(keepends=True)
    del lines[start - 1:node.end_lineno]
    source = "".join(lines)
    import_line = "from bootstrap._scaffold.config import token_gated_modules  # noqa: E402\n"
    assert source.count(import_line) == 1
    path.write_text(source.replace(import_line, ""), encoding="utf-8")


def _commit_copy(root: Path) -> None:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run([
        "git", "-c", "user.name=Promise probe", "-c",
        "user.email=promise-probe@localhost", "commit", "-qm", "Disposable candidate",
    ], cwd=root, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", choices=tuple(NODES))
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 13):
        parser.error("use canonical Python 3.13")
    data_bytes = DATA.read_bytes()
    if hashlib.sha256(data_bytes).hexdigest() != DATA_SHA256:
        parser.error("sealed default-security fixture digest changed")
    rows = json.loads(data_bytes)
    if len(rows) != 14 or any(type(row) is not list or len(row) != 4 for row in rows):
        parser.error("sealed fixture must contain the original 14 four-field patches")
    selected = args.only or list(NODES)
    by_id = {row[0]: row for row in rows}
    if len(by_id) != 14 or not set(NODES).issubset(by_id):
        parser.error("sealed fixture IDs changed")
    root_repo = Path(__file__).resolve().parents[1]
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root_repo, text=True).strip()
    archive = subprocess.run(["git", "archive", revision], cwd=root_repo, check=True, stdout=subprocess.PIPE).stdout

    for mutant_id in selected:
        _, target, old, new = by_id[mutant_id]
        if target not in TARGETS or len(old.splitlines()) > 2 or len(new.splitlines()) > 3:
            parser.error(f"unsupported fixed target or patch shape: {mutant_id}")
        with tempfile.TemporaryDirectory(prefix="default-security-probe-") as temporary:
            root = Path(temporary)
            with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
                bundle.extractall(root, filter="data")
            _exclude_old_cases(root)
            _commit_copy(root)
            healthy = _run(root, target, NODES[mutant_id])
            healthy_phases = [["setup", "passed"], ["call", "passed"], ["teardown", "passed"]]
            if healthy["code"] != 0 or healthy["reports"] != healthy_phases:
                raise RuntimeError(f"{mutant_id}: unhealthy baseline {healthy}")

            path = root / target
            original = path.read_bytes()
            source = original.decode("utf-8")
            if source.count(old) != 1:
                raise RuntimeError(f"{mutant_id}: sealed source text does not match exactly once")
            changed_line = source[:source.index(old)].count("\n") + 1
            path.write_text(source.replace(old, new, 1), encoding="utf-8")
            try:
                mutated = _run(root, target, NODES[mutant_id])
            finally:
                path.write_bytes(original)
            changed_lines = set(range(changed_line, changed_line + len(new.splitlines())))
            reached = sorted(changed_lines.intersection(mutated["lines"]))
            caught = (
                mutated["code"] == 1
                and mutated["reports"] == [["setup", "passed"], ["call", "failed"], ["teardown", "passed"]]
                and bool(reached)
            )
            clean = subprocess.run(["git", "diff", "--quiet", "HEAD"], cwd=root).returncode == 0
            if not clean or not caught:
                raise RuntimeError(f"{mutant_id}: inconclusive or survived; reached={reached}; report={mutated}")
            print(f"{mutant_id}: healthy call passed; mutated call assertion failed; changed lines reached {reached}; copy restored")
    print(f"candidate={revision}; probes={len(selected)}; old private pair excluded from disposable copies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
