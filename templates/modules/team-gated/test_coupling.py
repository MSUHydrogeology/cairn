#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Advisory report of Python tests coupled to project internals.

The report is a prompt for promise-shaped tests, not a deletion list. Refusal
tests and hostile-state tests that inject state through an internal hook stay.
Only path-resolved project modules are inspected; this tool never imports code.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import sys
from pathlib import Path


def _default_root() -> Path:
    here = Path(__file__).absolute().parent
    if (here.name == "team-gated" and here.parent.name == "modules"
            and here.parent.parent.name == "templates"):
        return here.parents[2]
    return here.parent


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _safe_file(path: Path, root: Path) -> bool:
    """Check lexical containment and every component without following links."""
    if not _inside(path, root):
        return False
    current = root
    for part in path.relative_to(root).parts:
        current = current / part
        try:
            if current.is_symlink():
                return False
        except OSError:
            return False
    return path.is_file()


def _is_test_path(path: Path, root: Path) -> bool:
    return any(part in {"tests", "test"} for part in path.relative_to(root).parts[:-1])


def _module_file(
    name: str, root: Path, test_file: Path | None = None,
    failures: list[str] | None = None,
) -> Path | None:
    if not name or any(not part.isidentifier() for part in name.split(".")):
        return None
    search_roots = [root]
    if test_file is not None:
        search_roots = []
        current = test_file.parent
        while _inside(current, root):
            search_roots.append(current)
            if current == root:
                break
            current = current.parent
    for search_root in search_roots:
        base = search_root.joinpath(*name.split("."))
        for candidate in (base.with_suffix(".py"), base / "__init__.py"):
            if not _inside(candidate, root):
                continue
            current = root
            for part in candidate.relative_to(root).parts:
                current = current / part
                if current.is_symlink():
                    if failures is not None:
                        failures.append(f"link:{current.relative_to(root).as_posix()}")
                    return None
            if candidate.is_file():
                # A local test module or fixture shadows the project import but
                # is not itself a project module. Do not fall through to a
                # same-named module elsewhere in the tree.
                if _is_test_path(candidate, root):
                    return None
                return candidate
    return None


def _test_files(root: Path) -> tuple[list[Path], list[str]]:
    found: list[Path] = []
    failures: list[str] = []
    skip = {".git", ".hg", ".svn", "__pycache__", ".venv", "venv", "site-packages"}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        here = Path(current)
        kept = []
        for name in sorted(dirs):
            path = here / name
            if name in skip:
                continue
            if path.is_symlink():
                failures.append(f"link:{path.relative_to(root).as_posix()}")
                continue
            kept.append(name)
        dirs[:] = kept
        for name in sorted(files):
            if not (name.startswith("test_") or name.endswith("_test.py")):
                continue
            path = here / name
            if path.is_symlink():
                failures.append(f"link:{path.relative_to(root).as_posix()}")
            elif name.endswith(".py"):
                found.append(path)
    return found, failures


def _relative_module(test_file: Path, root: Path, level: int, module: str | None) -> str | None:
    if level == 0:
        return module
    rel = test_file.relative_to(root)
    package = list(rel.parent.parts)
    # Relative imports are meaningful only in package directories.
    while package and not _safe_file(root.joinpath(*package, "__init__.py"), root):
        package.pop()
    if level > len(package):
        return None
    prefix = package[:len(package) - level + 1]
    if module:
        prefix.extend(module.split("."))
    return ".".join(prefix) or None


def _private(name: str) -> bool:
    return name.startswith("_") and not (name.startswith("__") and name.endswith("__"))


class _Reach(ast.NodeVisitor):
    def __init__(self, test_file: Path, root: Path, failures: list[str]):
        self.test_file = test_file
        self.root = root
        self.failures = failures
        self.aliases: dict[str, Path] = {}
        self.count = 0

    def visit_Import(self, node: ast.Import) -> None:
        for item in node.names:
            module_path = _module_file(
                item.name, self.root, self.test_file, self.failures)
            if module_path is not None:
                bound = item.asname or item.name.split(".")[0]
                if item.asname:
                    self.aliases[bound] = module_path
                else:
                    root_name = item.name.split(".")[0]
                    root_path = _module_file(
                        root_name, self.root, self.test_file, self.failures)
                    if root_path is not None:
                        self.aliases[bound] = root_path

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        name = _relative_module(self.test_file, self.root, node.level, node.module)
        if not name or _module_file(
                name, self.root, self.test_file, self.failures) is None:
            return
        for item in node.names:
            if item.name == "*":
                continue
            if _private(item.name):
                self.count += 1
            submodule = f"{name}.{item.name}"
            submodule_path = _module_file(
                submodule, self.root, self.test_file, self.failures)
            if submodule_path is not None:
                self.aliases[item.asname or item.name] = submodule_path

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if _private(node.attr) and isinstance(node.value, ast.Name):
            module = self.aliases.get(node.value.id)
            if module and _safe_file(module, self.root):
                self.count += 1
        self.generic_visit(node)


def scan(root: Path) -> tuple[list[dict[str, object]], list[str]]:
    root = root.absolute()
    rows: list[dict[str, object]] = []
    test_files, failures = _test_files(root)
    for path in test_files:
        relative = path.relative_to(root).as_posix()
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            failures.append(f"decode:{relative}:{type(exc).__name__}")
            continue
        try:
            tree = ast.parse(source, filename=relative)
        except (SyntaxError, ValueError, RecursionError, MemoryError) as exc:
            failures.append(f"parse:{relative}:{type(exc).__name__}")
            continue
        doc = ast.get_docstring(tree) or ""
        lines = doc.splitlines()
        has_promises = any(
            lines[index].strip() == "Promises:"
            and any(line.strip().startswith("- ") for line in lines[index + 1:])
            for index in range(len(lines))
        )
        reach = _Reach(path, root, failures)
        try:
            reach.visit(tree)
        except (RecursionError, MemoryError) as exc:
            failures.append(f"parse:{relative}:{type(exc).__name__}")
            continue
        rows.append({"path": relative, "private_reach": reach.count,
                     "missing_promises": not has_promises})
    rows.sort(key=lambda row: (-int(row["private_reach"]), not bool(row["missing_promises"]), str(row["path"])))
    failures.sort()
    return rows, failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=_default_root(),
                        help="project root (defaults to the installed project)")
    parser.add_argument("--strict", action="store_true",
                        help="exit nonzero when private reach, missing promises, or scan failures are reported")
    args = parser.parse_args(argv)
    root = args.root.absolute()
    if not root.is_dir():
        parser.error("--root must name a directory")
    rows, failures = scan(root)
    print("Python only: tests in other languages are outside this report.")
    print("Refusal tests and hostile-state tests using internal hooks stay; private reach is not a deletion list.")
    print("Files, worst first:")
    for row in rows:
        print(json.dumps(row, ensure_ascii=True, sort_keys=True))
    if failures:
        print("Scan failures:")
        for failure in failures:
            print(json.dumps(failure, ensure_ascii=True))
    if args.strict and (failures or any(row["private_reach"] or row["missing_promises"] for row in rows)):
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
