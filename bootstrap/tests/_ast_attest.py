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


# Mapping symbols whose digest the surgical ``update-symbol`` path may rewrite
# (Antigravity R1 / Codex S2). Restricted to the registry mapping symbols a
# package/skill/core-file install legitimately mutates — NOT functions, classes,
# or any other top-level symbol. Keyed by the bare name; the baseline key is
# ``Assign:<name>`` (both plain ``Assign`` and ``AnnAssign`` collapse to that
# key via ``_node_key``). Hard-coded, never derived from input.
_UPDATE_ALLOWLIST = frozenset({"_MODULE_MAPPINGS", "_SKILLS_MAPPINGS", "_CORE_MAPPINGS"})


def _classify(baseline: dict[str, dict], merged: dict[str, list[tuple[str, str]]]):
    """Compare a baseline against merged live digests.

    Returns ``(problems, changed, missing, duplicate, new)`` where ``problems``
    is the human-readable line list ``verify`` emits, ``changed`` maps
    ``key -> (baseline_digest, live_digest, file)``, ``missing``/``duplicate``
    are key lists, and ``new`` is the sorted set of live keys absent from the
    baseline. The skip rule (imports + module docstrings are per-module
    necessities, not single-source moved symbols) is applied here so ``verify``
    and ``update_symbol`` share one enforcement definition."""
    problems: list[str] = []
    changed: dict[str, tuple[str, str, str]] = {}
    missing: list[str] = []
    duplicate: list[str] = []
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
            missing.append(key)
            problems.append(f"MISSING   {key}  (baselined, absent from the current module set)")
        elif len(hits) > 1:
            files = ", ".join(f for _d, f in hits)
            duplicate.append(key)
            problems.append(f"DUPLICATE {key}  (defined in {len(hits)} files: {files} — single-source broken)")
        else:
            digest, where = hits[0]
            if digest != info["digest"]:
                changed[key] = (info["digest"], digest, where)
                problems.append(f"CHANGED   {key}  in {where}  (baseline {info['digest']} != {digest} — NOT pure motion)")
    new = sorted(set(merged) - set(baseline))
    return problems, changed, missing, duplicate, new


def verify(baseline_path: str | Path, module_paths: list[str | Path]) -> int:
    baseline: dict[str, dict] = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
    merged, _ = _merge_current(module_paths)
    problems, _changed, _missing, _duplicate, new = _classify(baseline, merged)

    # New top-level symbols are allowed (compat shims, __init__ facade re-exports),
    # but report them so a reviewer sees what an extraction commit introduced.
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


def update_symbol(
    baseline_path: str | Path,
    symbol: str,
    expect_old: str,
    module_paths: list[str | Path],
    *,
    known_new: set[str] | None = None,
    dry_run: bool = False,
    out=None,
) -> int:
    """Surgically rewrite ONE allowlisted mapping symbol's digest in the baseline.

    The single legitimate baseline mutation during the six-proposal cascade: a
    package/skill/core install adds an ``InstallSpec`` to ``_MODULE_MAPPINGS`` /
    ``_SKILLS_MAPPINGS`` / ``_CORE_MAPPINGS``, changing exactly that symbol's
    structural digest. Hardened so a one-key rewrite cannot bless an unintended
    mutation (Codex S2):

    * the symbol must be in :data:`_UPDATE_ALLOWLIST` (registry mappings only);
    * ``--expect-old`` must equal the symbol's current baseline digest;
    * the live module set must show the target as the **only** CHANGED symbol,
      with **no** MISSING / DUPLICATE drift — any unrelated discrepancy refuses;
    * **no NEW top-level symbol may appear beyond the pinned ``known_new`` set**
      (Codex confirmation R2-2 Finding 1): the legitimate cascade adds an
      ``InstallSpec`` to an existing mapping and introduces NO new top-level
      node, so a mapping update carrying a brand-new function/class/assignment
      (e.g. an injected gate-bypass) is refused. ``known_new`` is the committed
      base NEW set (the original split's facade re-exports — see
      ``fixtures/scaffold_ast_known_new.json``); omitted ``known_new`` means
      **strict**: any new symbol refuses;
    * a before/after attestation is emitted for the audit trail; and
    * only that one key's ``digest`` field is rewritten — every other baselined
      symbol is left byte-for-byte (the file stays canonical JSON).

    Exit codes: 0 written/dry-run-ok; 2 usage/allowlist/absent-key; 3
    expect-old mismatch; 4 no-change or unrelated drift (refused, no write)."""
    # Resolve the stream at call time (a ``sys.stderr`` default would bind the
    # pre-capture stream at import, breaking capsys-style redirection).
    if out is None:
        out = sys.stderr
    norm = symbol[len("Assign:"):] if symbol.startswith("Assign:") else symbol
    full = f"Assign:{norm}"
    if norm not in _UPDATE_ALLOWLIST:
        print(f"[update-symbol] REFUSED — '{symbol}' is not an allowlisted mapping "
              f"symbol ({', '.join(sorted(_UPDATE_ALLOWLIST))})", file=out)
        return 2

    baseline_path = Path(baseline_path)
    baseline: dict[str, dict] = json.loads(baseline_path.read_text(encoding="utf-8"))
    if full not in baseline:
        print(f"[update-symbol] REFUSED — '{full}' is not present in the baseline", file=out)
        return 2

    baseline_old = baseline[full]["digest"]
    if baseline_old != expect_old:
        print(f"[update-symbol] REFUSED — expect-old mismatch for {full}: baseline carries "
              f"{baseline_old!r}, --expect-old said {expect_old!r}. No write.", file=out)
        return 3

    merged, _ = _merge_current(module_paths)
    problems, changed, _missing, _duplicate, new = _classify(baseline, merged)

    if full not in changed:
        print(f"[update-symbol] REFUSED — {full} is NOT changed vs the baseline in the given "
              f"module set; there is nothing to update (live digest already matches). No write.",
              file=out)
        return 4

    unexpected = [p for p in problems if not p.startswith(f"CHANGED   {full}  ")]
    if unexpected:
        print(f"[update-symbol] REFUSED — unrelated drift present; will not rewrite {full} while "
              f"other baselined symbols differ (one-symbol delta violated):", file=out)
        for p in unexpected:
            print(f"  {p}", file=out)
        return 4

    # No NEW top-level symbol may ride in on the surgical mapping update beyond the
    # pinned base set (Codex confirmation R2-2 Finding 1). The cascade only mutates an
    # existing mapping's value; a new function/class/assignment alongside it (an injected
    # gate-bypass) is a HOLD. ``known_new`` omitted ⇒ strict (any new refuses).
    allowed_new = known_new if known_new is not None else set()
    unexpected_new = [k for k in new if k not in allowed_new]
    if unexpected_new:
        print(f"[update-symbol] REFUSED — {len(unexpected_new)} new top-level symbol(s) appeared "
              f"alongside the mapping change, not in the pinned known-new set; a surgical "
              f"re-baseline must NOT bless injected top-level logic. HOLD (review + regenerate "
              f"via a reviewed path):", file=out)
        for k in unexpected_new:
            print(f"  NEW {k}", file=out)
        return 4

    old_d, new_d, where = changed[full]
    n_other = sum(
        1 for k, i in baseline.items()
        if i.get("type") not in ("Import", "ImportFrom")
        and k.split("#", 1)[0] != "Docstring" and k != full
    )
    print("[update-symbol] AST baseline single-symbol update", file=out)
    print(f"  baseline file : {baseline_path}", file=out)
    print(f"  symbol        : {full}  (allowlisted)", file=out)
    print(f"  expect-old    : {expect_old}", file=out)
    print(f"  baseline-old  : {old_d}  [MATCH]", file=out)
    print(f"  live-new      : {new_d}  in {where}", file=out)
    print(f"  unrelated     : none — 0 CHANGED / 0 MISSING / 0 DUPLICATE across "
          f"{n_other} other enforced symbols", file=out)
    print(f"  new top-level : {', '.join(new) if new else 'none'}", file=out)

    if dry_run:
        print("  action        : DRY-RUN — no write", file=out)
        return 0

    baseline[full]["digest"] = new_d
    text = json.dumps(baseline, indent=2, sort_keys=True) + "\n"
    tmp = baseline_path.with_name(baseline_path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(baseline_path)
    print(f"  action        : WROTE {baseline_path}", file=out)
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
    u = sub.add_parser(
        "update-symbol",
        help="surgically rewrite ONE allowlisted mapping symbol's digest in the baseline",
    )
    u.add_argument("symbol", help="mapping symbol name (_MODULE_MAPPINGS / _SKILLS_MAPPINGS / _CORE_MAPPINGS)")
    u.add_argument("--baseline", required=True, help="path to the baseline JSON to rewrite")
    u.add_argument("--expect-old", required=True, dest="expect_old",
                   help="the symbol's current baseline digest (refuses on mismatch)")
    u.add_argument("--known-new", default=None, dest="known_new",
                   help="path to a JSON list of allowed pre-existing NEW keys (the base "
                        "facade re-exports); omit for strict (any new symbol refuses)")
    u.add_argument("--dry-run", action="store_true", help="attest the change but write nothing")
    u.add_argument("modules", nargs="+", help="the live module set (same set 'verify' uses)")
    args = parser.parse_args(argv)
    if args.cmd == "baseline":
        json.dump(digest_module(args.module), sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    if args.cmd == "update-symbol":
        known_new = None
        if args.known_new:
            known_new = set(json.loads(Path(args.known_new).read_text(encoding="utf-8")))
        return update_symbol(
            args.baseline, args.symbol, args.expect_old, args.modules,
            known_new=known_new, dry_run=args.dry_run, out=sys.stderr,
        )
    return verify(args.baseline, args.modules)


if __name__ == "__main__":
    raise SystemExit(main())
