#!/usr/bin/env python3
"""AST source-motion attestation — scaffold-split plan, Stage 0A.4 (SR3 / P2#4).

The scaffold-split refactor claims each extraction stage is **pure motion**:
a function/class/constant moves from ``bootstrap/scaffold.py`` into an owning
``bootstrap/_scaffold/<module>.py`` with its source unchanged. "Tests green"
is not a sufficient security gate for a large code-motion refactor — a semantic
change can hide in thousands of moved lines while preserving tests and Bandit
cleanliness. This tool makes motion **mechanically attestable**.

It digests **every top-level AST node** of a module — functions, classes,
module-level assignments / regexes / mappings / frozensets / constants /
named-tuples, and imports — by their **structural AST** (``ast.dump`` with
``include_attributes=False``, so the digest is insensitive to line numbers,
comments, and formatting, but sensitive to any change in defaults, decorators,
class bodies, global bindings, or logic). It is **motion evidence, not a proof
of behavioral equivalence** — identical AST under a different import graph can
still change behavior, which is why the differential oracle harness and the
identity tests are the behavioral guards (plan Verification).

Workflow
--------

**Interpreter pinning (code review C2).** ``ast.dump`` output and the AST node
structure vary across Python *minor* versions (e.g. 3.12 vs 3.13). The baseline
artifact and every ``verify`` run **must** use the project's canonical
interpreter (the ``lhm`` env, Python 3.13) — generating the baseline on one
minor and verifying on another causes spurious digest mismatches that look like
a logic change. ``test_committed_baseline_matches_live_scaffold`` says so in its
failure message.

1. **Baseline** (Stage 0A, re-pinned at 0B just before extraction; run under the
   canonical interpreter — see "Interpreter pinning" above)::

       python bootstrap/tests/_ast_attest.py baseline bootstrap/scaffold.py \
           > bootstrap/tests/fixtures/scaffold_ast_baseline.json

2. **Verify a stage** — prove every symbol the commit claims to have moved is
   present, exactly once, with an unchanged digest, across the new module set::

       python bootstrap/tests/_ast_attest.py verify \
           bootstrap/tests/fixtures/scaffold_ast_baseline.json \
           bootstrap/scaffold.py bootstrap/_scaffold/security.py ...

   Exit 0 = every baselined symbol is accounted for unchanged (and nothing
   changed identity); non-zero = a CHANGED / MISSING / DUPLICATE symbol — i.e.
   a non-pure-motion edit rode an extraction commit.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path

# Top-level node types whose *identity* is named (so a move is trackable by
# name across modules). Everything else is keyed structurally.
_NAMED = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def _targets(node: ast.AST) -> list[str]:
    out: list[str] = []
    for t in getattr(node, "targets", []) or ([node.target] if getattr(node, "target", None) else []):
        if isinstance(t, ast.Name):
            out.append(t.id)
        elif isinstance(t, (ast.Tuple, ast.List)):
            out.extend(e.id for e in t.elts if isinstance(e, ast.Name))
    return out


def _node_key(node: ast.AST) -> str:
    """A stable identifier for a top-level node, used to track it across a move."""
    if isinstance(node, _NAMED):
        return f"{type(node).__name__}:{node.name}"
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        names = _targets(node)
        return f"Assign:{','.join(names)}" if names else f"AssignExpr:{type(node).__name__}"
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        # imports are keyed by their full structural content (no name to track)
        return "Import:" + hashlib.sha256(
            ast.dump(node, include_attributes=False).encode()).hexdigest()[:12]
    if (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)):
        # A bare string expression -- a module docstring. Every split module has
        # one, so it must NOT be single-sourced (re-review-2 finding 3). Keyed
        # distinctly from executable top-level expressions, which stay enforced.
        return "Docstring"
    return f"{type(node).__name__}"


def digest_module(path: str | Path) -> dict[str, dict]:
    """Map ``{node_key: {digest, span, type}}`` for every top-level node.

    ``digest`` is the sha256 (first 16 hex) of the node's structural AST,
    position-stripped. Duplicate keys (e.g. two re-assignments to one name) get
    a ``#<n>`` suffix so each occurrence is tracked distinctly (a multiset)."""
    src = Path(path).read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(path))
    out: dict[str, dict] = {}
    seen: dict[str, int] = {}
    for node in tree.body:
        base = _node_key(node)
        seen[base] = seen.get(base, 0) + 1
        key = base if seen[base] == 1 else f"{base}#{seen[base]}"
        structural = ast.dump(node, include_attributes=False)
        out[key] = {
            "digest": hashlib.sha256(structural.encode("utf-8")).hexdigest()[:16],
            "span": [node.lineno, getattr(node, "end_lineno", node.lineno)],
            "type": type(node).__name__,
        }
    return out


def _merge_current(paths: list[str | Path]) -> tuple[dict[str, list[tuple[str, str]]], list[str]]:
    """Merge the digests of several modules. Returns ``({key: [(digest, file)...]}, errors)``.
    A key appearing in >1 file (a duplicate definition) is an error (S5 single-source)."""
    merged: dict[str, list[tuple[str, str]]] = {}
    for p in paths:
        rel = str(p)
        for key, info in digest_module(p).items():
            merged.setdefault(key, []).append((info["digest"], rel))
    return merged, []


def verify(baseline_path: str | Path, module_paths: list[str | Path]) -> int:
    baseline: dict[str, dict] = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
    merged, _ = _merge_current(module_paths)
    problems: list[str] = []

    for key, info in baseline.items():
        if info.get("type") in ("Import", "ImportFrom") or key.split("#", 1)[0] == "Docstring":
            # Per-module necessities, not single-source "moved symbols":
            # - imports (code review C3): the same ``import sys`` recurs across
            #   split modules (false-DUPLICATE); a relocated import is not lost.
            # - module docstrings (re-review-2 finding 3): every split module
            #   carries one. Executable top-level expressions stay enforced.
            # functions/classes/constants remain strictly single-sourced.
            continue
        hits = merged.get(key, [])
        if not hits:
            problems.append(f"MISSING   {key}  (baselined, absent from the current module set)")
        elif len(hits) > 1:
            files = ", ".join(f for _d, f in hits)
            problems.append(f"DUPLICATE {key}  (defined in {len(hits)} files: {files} — single-source broken)")
        else:
            digest, where = hits[0]
            if digest != info["digest"]:
                problems.append(f"CHANGED   {key}  in {where}  (baseline {info['digest']} != {digest} — NOT pure motion)")

    # New top-level symbols are allowed (compat shims, __init__ facade re-exports),
    # but report them so a reviewer sees what an extraction commit introduced.
    new = sorted(set(merged) - set(baseline))
    for key in new:
        where = ", ".join(f for _d, f in merged[key])
        print(f"note: NEW {key}  ({where})", file=sys.stderr)

    if problems:
        print(f"AST attestation FAILED — {len(problems)} non-pure-motion symbol(s):", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1
    print(f"AST attestation OK — {len(baseline)} baselined symbol(s) accounted for, unchanged.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ast_attest", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("baseline", help="emit the per-symbol digest of a module as JSON")
    b.add_argument("module")
    v = sub.add_parser("verify", help="verify a stage's module set against a baseline")
    v.add_argument("baseline")
    v.add_argument("modules", nargs="+")
    args = parser.parse_args(argv)
    if args.cmd == "baseline":
        json.dump(digest_module(args.module), sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    return verify(args.baseline, args.modules)


if __name__ == "__main__":
    raise SystemExit(main())
