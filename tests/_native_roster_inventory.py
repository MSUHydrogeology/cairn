# SPDX-License-Identifier: MIT
"""Bounded source reconciliation for a proposed native-node roster.

This reads Python syntax and an existing protected node list. It never imports
test source, collects tests, observes host skips, or decides skip eligibility.
Dynamic parameters and parameterized fixtures remain explicit review items.
"""
from __future__ import annotations

import ast
from itertools import product
from pathlib import Path


def _definitions(body: list[ast.stmt], prefix: str = ""):
    for node in body:
        if isinstance(node, ast.ClassDef):
            yield from _definitions(node.body, prefix + node.name + "::")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield prefix + node.name, node


def _literal_ids(call: ast.Call) -> list[str]:
    explicit = next((item.value for item in call.keywords if item.arg == "ids"), None)
    if explicit is not None:
        ids = ast.literal_eval(explicit)
        if not isinstance(ids, (list, tuple)) or not all(isinstance(x, str) for x in ids):
            raise ValueError("nonliteral explicit IDs")
        if len(ids) != len(set(ids)) or (isinstance(call.args[1], (ast.List, ast.Tuple))
                                       and len(ids) != len(call.args[1].elts)):
            raise ValueError("explicit IDs need disambiguation or arity review")
        return list(ids)
    names = ast.literal_eval(call.args[0])
    if isinstance(names, str):
        names = [name.strip() for name in names.split(",")]
    values = ast.literal_eval(call.args[1])
    if not isinstance(names, (list, tuple)) or not isinstance(values, (list, tuple)):
        raise ValueError("nonliteral parameter sequence")
    ids = []
    for index, value in enumerate(values):
        row = [value] if len(names) == 1 else value
        if not isinstance(row, (list, tuple)) or len(row) != len(names):
            raise ValueError("parameter arity mismatch")
        parts = []
        for name, item in zip(names, row):
            if isinstance(item, str):
                parts.append(item.encode("unicode_escape").decode("ascii"))
            elif item is None or isinstance(item, (bool, int, float)):
                parts.append(str(item))
            else:
                parts.append(f"{name}{index}")
        ids.append("-".join(parts))
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate IDs need pytest disambiguation review")
    return ids


def reconcile(root: Path, proposed: list[str], protected: list[str]) -> dict:
    """Check named source identities; leave unsupported forms unresolved.

    A clean result is source reconciliation only, never roster completeness or
    permission to skip. Missing protected entries remain visible, even for a
    source identity that is fully understood.
    """
    result = {key: [] for key in (
        "missing_source", "literal_id_mismatch", "unresolved", "absent_from_record")}
    cache = {}
    protected_set = set(protected)
    for identity in proposed:
        if identity not in protected_set:
            result["absent_from_record"].append(identity)
        filename, separator, tail = identity.partition("::")
        if not separator or not filename.startswith("bootstrap/tests/") or ".." in Path(filename).parts:
            result["missing_source"].append(identity)
            continue
        if filename not in cache:
            path = root / filename
            if not path.is_file():
                cache[filename] = ({}, set())
            else:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=filename)
                definitions = dict(_definitions(tree.body))
                fixtures = {name for name, node in definitions.items()
                            if any(isinstance(d, ast.Call) and ast.unparse(d.func).endswith("fixture")
                                   and any(k.arg == "params" for k in d.keywords)
                                   for d in node.decorator_list)}
                cache[filename] = definitions, fixtures
        definitions, fixtures = cache[filename]
        name = tail.partition("[")[0]
        node = definitions.get(name)
        if node is None:
            result["missing_source"].append(identity)
            continue
        parameters = [d for d in reversed(node.decorator_list)
                      if isinstance(d, ast.Call) and ast.unparse(d.func).endswith("parametrize")]
        try:
            if {arg.arg for arg in node.args.args} & fixtures:
                raise ValueError("parameterized fixture requires source review")
            dimensions = [_literal_ids(d) for d in parameters]
            expected = {name + "[" + "-".join(parts) + "]" for parts in product(*dimensions)} if dimensions else {name}
            if tail not in expected:
                result["literal_id_mismatch"].append(identity)
        except (ValueError, TypeError, SyntaxError, IndexError):
            result["unresolved"].append({"node": identity, "line": node.lineno,
                                         "parameters": [ast.unparse(d) for d in parameters]})
    return result
