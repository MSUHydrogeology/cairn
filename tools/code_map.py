#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Bounded, read-only filesystem map for the optional architecture module.

The collector never imports or executes inspected files. It only runs where
descriptor-relative no-follow traversal is available; other systems receive an
explicit incomplete result. Git revisions and HTML rendering are intentionally
outside this filesystem-only first stage.
"""
from __future__ import annotations

import sys

if not sys.flags.isolated:
    sys.stderr.write("code_map: run with the trusted Python runtime in -I mode\n")
    raise SystemExit(2)

import argparse
import ast
import collections
import io
import json
import os
import re
import signal
import stat
import subprocess
import time
import tokenize
from pathlib import PurePosixPath
from typing import Any


MAX_ENTRIES = 10_000
MAX_TOTAL_READ = 128 * 1024 * 1024
MAX_SOURCE = 1024 * 1024
MAX_AST_NODES = 2_000_000
MAX_SYMBOLS = 20_000
MAX_COMPARISONS = 1_000_000
PER_FILE_SECONDS = 5.0
PARSER_SECONDS = 30.0
COMMAND_SECONDS = 60.0
_WORKER_SCAN = "--_scan-worker"
_WORKER_PARSE = "--_parse-worker"


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def _write_result(result: dict[str, Any], exit_code: int = 0) -> int:
    sys.stdout.buffer.write(_json_bytes(result))
    sys.stdout.buffer.flush()
    return exit_code


def _diagnostic(code: str, path: str, message: str, remedy: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message, "remedy": remedy}


def _empty_result(root: str, mode: str) -> dict[str, Any]:
    return {
        "schema": "cairn-code-map-v1",
        "status": "incomplete",
        "mode": mode,
        "root": root,
        "revision": None,
        "revision_note": "not read: filesystem mode performs no Git inspection",
        "budgets": {
            "entries_limit": MAX_ENTRIES,
            "entries_seen": 0,
            "bytes_limit": MAX_TOTAL_READ,
            "bytes_read": 0,
            "source_limit": MAX_SOURCE,
            "ast_nodes_limit": MAX_AST_NODES,
            "ast_nodes": 0,
            "symbols_limit": MAX_SYMBOLS,
            "symbols": 0,
            "comparisons_limit": MAX_COMPARISONS,
            "comparisons": 0,
            "parser_seconds_limit": PARSER_SECONDS,
            "parser_seconds": 0.0,
            "command_seconds_limit": COMMAND_SECONDS,
            "command_seconds": 0.0,
        },
        "components": [],
        "files": [],
        "scope": {"excluded_directory_names": [".git", "__pycache__", ".pytest_cache"]},
        "omissions": [],
        "neighbors": [],
        "sampling": None,
        "diagnostics": [],
    }


def _secure_walk_available() -> bool:
    required = (os.open, os.stat)
    return (
        all(fn in os.supports_dir_fd for fn in required)
        and os.scandir in os.supports_fd
        and hasattr(os, "O_DIRECTORY")
        and hasattr(os, "O_NOFOLLOW")
    )


def _open_absolute_directory(path: str) -> int:
    """Open every root component by handle without following links."""
    absolute = os.path.abspath(path)
    drive, tail = os.path.splitdrive(absolute)
    if drive:
        raise OSError("only POSIX absolute roots are supported by this walker")
    fd = os.open(os.sep, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in (item for item in tail.split(os.sep) if item):
            next_fd = os.open(
                part,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=fd,
            )
            os.close(fd)
            fd = next_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


def _read_at(parent_fd: int, name: str, before: os.stat_result,
             allowance: int, read_count: list[int] | None = None) -> tuple[bytes, os.stat_result]:
    flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(name, flags, dir_fd=parent_fd)
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode):
            raise OSError("not a regular file")
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise OSError("file changed between inspection and open")
        if opened.st_size > MAX_SOURCE:
            raise OverflowError("source grew beyond the per-file limit")
        if opened.st_size > allowance:
            raise OverflowError("total read budget would be exceeded")
        chunks: list[bytes] = []
        remaining = min(allowance, MAX_SOURCE + 1)
        while remaining:
            chunk = os.read(fd, min(64 * 1024, remaining))
            if not chunk:
                break
            if read_count is not None:
                read_count[0] += len(chunk)
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        if len(data) > MAX_SOURCE:
            raise OverflowError("source grew beyond the per-file limit")
        if len(data) > allowance:
            raise OverflowError("file grew beyond the remaining read budget")
        after = os.fstat(fd)
        if ((after.st_dev, after.st_ino, after.st_size)
                != (opened.st_dev, opened.st_ino, opened.st_size)):
            raise OSError("file changed while it was read")
        return data, after
    finally:
        os.close(fd)


def _tokens(name: str) -> list[str]:
    parts = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name).split("_")
    return [piece.lower() for part in parts for piece in part.split()
            if piece and not piece.isdigit()]


def _summary(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.split())[:240]


def _parse_source_worker() -> int:
    request = json.loads(sys.argv[2])
    source = sys.stdin.buffer.read(MAX_SOURCE + 1)
    if len(source) > MAX_SOURCE:
        return _write_result({"ok": False, "error": "source-limit"}, 2)
    try:
        encoding, _ = tokenize.detect_encoding(io.BytesIO(source).readline)
        text = source.decode(encoding)
        tree = ast.parse(text)
    except (SyntaxError, UnicodeError, LookupError, RecursionError) as exc:
        return _write_result({"ok": False, "error": "parse-error",
                              "message": str(exc)[:500]}, 0)

    node_limit = int(request["node_limit"])
    stack = [tree]
    node_count = 0
    while stack:
        node = stack.pop()
        node_count += 1
        if node_count > node_limit:
            return _write_result({"ok": False, "error": "ast-node-limit",
                                  "nodes": node_count}, 0)
        stack.extend(ast.iter_child_nodes(node))

    definitions: list[tuple[ast.AST, str, bool]] = []
    pending = [(tree, "", True)]
    while pending:
        node, parent, visible = pending.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            qualified = f"{parent}.{node.name}" if parent else node.name
            public = visible and not node.name.startswith("_")
            definitions.append((node, qualified, public))
            if len(definitions) > int(request["symbol_limit"]):
                return _write_result({"ok": False, "error": "symbol-limit",
                                      "definitions": len(definitions), "nodes": node_count}, 0)
            parent = qualified
            if not isinstance(node, ast.ClassDef):
                parent += ".<locals>"
                public = False
            visible = public
        pending.extend((child, parent, visible)
                       for child in reversed(list(ast.iter_child_nodes(node))))
    symbols: list[dict[str, Any]] = []
    symbol_limit = int(request["symbol_limit"])
    for node, qualified, public in definitions:
        name = node.name
        stack2 = [node]
        shape: collections.Counter[str] = collections.Counter()
        identifiers: set[str] = set()
        while stack2:
            child = stack2.pop()
            shape[type(child).__name__] += 1
            if isinstance(child, ast.Name):
                identifiers.update(_tokens(child.id))
            elif isinstance(child, ast.arg):
                identifiers.update(_tokens(child.arg))
            elif isinstance(child, ast.Attribute):
                identifiers.update(_tokens(child.attr))
            stack2.extend(ast.iter_child_nodes(child))
        symbols.append({
            "name": name,
            "qualified_name": qualified,
            "kind": ("class" if isinstance(node, ast.ClassDef) else "function"),
            "public": public,
            "line": int(getattr(node, "lineno", 0)),
            "summary": _summary(ast.get_docstring(node, clean=False)),
            "shape": dict(shape),
            "names": sorted(identifiers | set(_tokens(name))),
        })
        if len(symbols) > symbol_limit:
            return _write_result({"ok": False, "error": "symbol-limit",
                                  "symbols": symbol_limit, "nodes": node_count}, 0)
    return _write_result({"ok": True, "nodes": node_count,
                          "definitions": len(definitions),
                          "symbols": symbols}, 0)


def _parse_file(data: bytes, node_limit: int, symbol_limit: int,
                timeout: float) -> tuple[dict[str, Any], float]:
    request = json.dumps({"node_limit": node_limit,
                          "symbol_limit": symbol_limit}, separators=(",", ":"))
    command = [sys.executable, "-I", os.path.abspath(__file__),
               _WORKER_PARSE, request]
    started = time.monotonic()
    completed = subprocess.run(
        command, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=timeout, check=False, env={
            "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",
        },
    )
    elapsed = time.monotonic() - started
    try:
        result = json.loads(completed.stdout.decode("ascii"))
    except (UnicodeError, json.JSONDecodeError):
        result = {"ok": False, "error": "parser-worker-failed",
                  "message": completed.stderr.decode("ascii", "backslashreplace")[:500]}
    return result, elapsed


def _file_record(relative: str, info: os.stat_result) -> dict[str, Any]:
    suffix = os.path.splitext(relative)[1].lower()
    language = "Python" if suffix == ".py" else (suffix[1:] or "unknown")
    return {
        "path": relative,
        "component": relative.split("/", 1)[0] if "/" in relative else ".",
        "language": language,
        "analysis": "pending" if language == "Python" else "unsupported",
        "bytes": info.st_size,
        "public": [],
    }


def _walk(root_fd: int, root_name: str, args: dict[str, Any]) -> dict[str, Any]:
    result = _empty_result(root_name, "release" if args["release"] else
                           "changed" if args["changed"] else "map")
    diagnostics = result["diagnostics"]
    records: list[dict[str, Any]] = []
    symbol_rows: list[dict[str, Any]] = []
    dirs_seen: set[str] = set()
    total_bytes = 0
    total_nodes = 0
    total_definitions = 0
    parser_time = 0.0
    entries = 0
    parsing_open = True
    deadline = time.monotonic() + PARSER_SECONDS
    wanted = set(args["changed"])
    found_wanted: set[str] = set()

    def visit(folder_fd: int, prefix: str) -> None:
        nonlocal entries, total_bytes, total_nodes, total_definitions
        nonlocal parser_time, parsing_open
        if entries >= MAX_ENTRIES:
            diagnostics.append(_diagnostic(
                "entry-limit", prefix, f"entry limit {MAX_ENTRIES} reached",
                "Narrow the filesystem root; the limit is fixed for this scan."))
            parsing_open = False
            return
        try:
            names = []
            scan = os.scandir(folder_fd)
            try:
                for item in scan:
                    names.append(item)
                    if len(names) > MAX_ENTRIES - entries:
                        break
            finally:
                scan.close()
            names.sort(key=lambda item: item.name)
        except OSError as exc:
            diagnostics.append(_diagnostic(
                "directory-read", prefix, str(exc),
                "Grant read access or scan a stable, readable directory."))
            return
        for item in names:
            if entries >= MAX_ENTRIES:
                diagnostics.append(_diagnostic(
                    "entry-limit", prefix, f"entry limit {MAX_ENTRIES} reached",
                    "Narrow the filesystem root; the limit is fixed for this scan."))
                parsing_open = False
                return
            relative = f"{prefix}/{item.name}" if prefix else item.name
            entries += 1
            try:
                before = os.stat(item.name, dir_fd=folder_fd,
                                 follow_symlinks=False)
            except OSError as exc:
                diagnostics.append(_diagnostic(
                    "entry-stat", relative, str(exc),
                    "Retry after the directory stops changing."))
                continue
            if stat.S_ISLNK(before.st_mode):
                diagnostics.append(_diagnostic(
                    "linked-entry", relative, "entry is a symbolic link",
                    "Replace links/reparse points with contained real files or directories."))
                continue
            if stat.S_ISDIR(before.st_mode):
                if item.name in result["scope"]["excluded_directory_names"]:
                    result["omissions"].append({
                        "path": relative,
                        "reason": "metadata directory excluded from default scope",
                    })
                    continue
                dirs_seen.add(relative.split("/", 1)[0])
                try:
                    child_fd = os.open(
                        item.name,
                        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                        dir_fd=folder_fd,
                    )
                except OSError as exc:
                    diagnostics.append(_diagnostic(
                        "directory-changed-or-linked", relative, str(exc),
                        "Replace links/reparse points with contained real directories."))
                    continue
                try:
                    opened = os.fstat(child_fd)
                    if ((opened.st_dev, opened.st_ino)
                            != (before.st_dev, before.st_ino)):
                        diagnostics.append(_diagnostic(
                            "directory-race", relative,
                            "directory changed between inspection and open",
                            "Retry against a stable tree."))
                        continue
                    visit(child_fd, relative)
                finally:
                    os.close(child_fd)
                continue
            if not stat.S_ISREG(before.st_mode):
                diagnostics.append(_diagnostic(
                    "special-file", relative, "entry is not a regular file or directory",
                    "Replace it with a regular file or remove it from the scan root."))
                continue
            record = _file_record(relative, before)
            records.append(record)
            if relative in wanted:
                found_wanted.add(relative)
            if record["language"] != "Python":
                continue
            if not parsing_open:
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    "analysis-stopped", relative,
                    "Python analysis stopped after an earlier limit",
                    "Narrow the scan and address the earlier diagnostic."))
                continue
            if before.st_size > MAX_SOURCE:
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    "source-limit", relative,
                    f"source is {before.st_size} bytes; limit is {MAX_SOURCE}",
                    "Split the source or inspect a narrower set of files."))
                continue
            if total_bytes + before.st_size > MAX_TOTAL_READ:
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    "total-read-limit", relative,
                    f"reading this file would exceed {MAX_TOTAL_READ} bytes",
                    "Narrow the filesystem root; the limit is fixed for this scan."))
                parsing_open = False
                continue
            remaining_time = deadline - time.monotonic()
            if remaining_time <= 0:
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    "parser-total-time-limit", relative,
                    f"parser time limit {PARSER_SECONDS:g} seconds reached",
                    "Narrow the filesystem root or reduce the Python source set."))
                parsing_open = False
                continue
            read_count = [0]
            try:
                data, _after = _read_at(
                    folder_fd, item.name, before, MAX_TOTAL_READ - total_bytes,
                    read_count)
            except OverflowError as exc:
                record["analysis"] = "incomplete"
                code = "source-limit" if "per-file" in str(exc) else "total-read-limit"
                diagnostics.append(_diagnostic(
                    code, relative, str(exc),
                    "Narrow the filesystem root; the limit is fixed for this scan."))
                parsing_open = False
                continue
            except OSError as exc:
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    "file-read-or-race", relative, str(exc),
                    "Retry against a stable tree containing only regular files."))
                continue
            finally:
                total_bytes += read_count[0]
            timeout = min(PER_FILE_SECONDS, remaining_time)
            try:
                parsed, elapsed = _parse_file(
                    data, MAX_AST_NODES - total_nodes,
                    MAX_SYMBOLS - total_definitions, timeout)
            except subprocess.TimeoutExpired:
                elapsed = timeout
                parsed = {"ok": False, "error": "parser-file-time-limit"}
            parser_time += elapsed
            result["budgets"]["parser_seconds"] = round(parser_time, 3)
            result["budgets"]["bytes_read"] = total_bytes
            if not parsed.get("ok"):
                code = parsed.get("error", "parser-worker-failed")
                if code == "ast-node-limit":
                    total_nodes += int(parsed.get("nodes", 0))
                if code == "symbol-limit":
                    total_definitions += int(parsed.get("definitions", 0))
                    total_nodes += int(parsed.get("nodes", 0))
                record["analysis"] = "incomplete"
                diagnostics.append(_diagnostic(
                    code, relative, parsed.get("message", code),
                    "Correct the source or narrow the scan; do not treat missing analysis as clean."))
                if code in ("parser-file-time-limit", "ast-node-limit",
                            "symbol-limit"):
                    parsing_open = code != "parser-file-time-limit"
                    if code in ("ast-node-limit", "symbol-limit"):
                        parsing_open = False
                continue
            nodes = int(parsed["nodes"])
            total_nodes += nodes
            total_definitions += int(parsed["definitions"])
            result["budgets"]["ast_nodes"] = total_nodes
            for symbol in parsed["symbols"]:
                symbol["path"] = relative
                if symbol["kind"] == "function":
                    symbol_rows.append(symbol)
            record["analysis"] = "parsed"
            record["public"] = [
                {key: symbol[key] for key in
                 ("name", "qualified_name", "kind", "line", "summary")}
                for symbol in parsed["symbols"]
                if symbol["public"]
            ]
    visit(root_fd, "")
    result["budgets"].update({
        "entries_seen": entries,
        "bytes_read": total_bytes,
        "ast_nodes": total_nodes,
        "symbols": total_definitions,
        "parser_seconds": round(parser_time, 3),
    })
    result["components"] = sorted(dirs_seen)
    result["files"] = records
    result["diagnostics"].extend(
        _diagnostic("changed-path-missing", path,
                    "requested changed path was not found as a contained regular file",
                    "Pass a root-relative regular file path present in the scanned tree.")
        for path in sorted(wanted - found_wanted)
    )
    if args["release"] or wanted:
        focal = [row for row in symbol_rows
                 if args["release"] or row["path"] in wanted]
        result["neighbors"], result["sampling"] = _neighbors(
            symbol_rows, focal, args["release"])
        result["budgets"]["comparisons"] = result["sampling"]["compared"]
    result["status"] = "incomplete" if result["diagnostics"] else "complete"
    return result


def _counter_similarity(left: dict[str, int], right: dict[str, int]) -> float:
    keys = left.keys() | right.keys()
    denom = sum(max(left.get(key, 0), right.get(key, 0)) for key in keys)
    if not denom:
        return 1.0
    return sum(min(left.get(key, 0), right.get(key, 0)) for key in keys) / denom


def _name_similarity(left: list[str], right: list[str]) -> float:
    a, b = set(left), set(right)
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def _similarity(left: dict[str, Any], right: dict[str, Any]) -> float:
    shape = _counter_similarity(left["shape"], right["shape"])
    names = _name_similarity(left["names"], right["names"])
    return 0.7 * shape + 0.3 * names


def _neighbors(all_symbols: list[dict[str, Any]], focal: list[dict[str, Any]],
               release: bool) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = sorted(all_symbols, key=lambda row: (row["path"], row["line"], row["name"]))
    positions = {id(row): index for index, row in enumerate(rows)}
    focal = sorted(focal, key=lambda row: (row["path"], row["line"], row["name"]))
    candidate_count = max(0, len(rows) - 1)
    total = (len(rows) * (len(rows) - 1) // 2 if release else
             len(focal) * candidate_count)
    budget = min(total, MAX_COMPARISONS)
    ranked: dict[int, list[tuple[float, dict[str, Any]]]] = collections.defaultdict(list)

    def keep(index: int, score: float, other: dict[str, Any]) -> None:
        choices = ranked[index]
        choices.append((score, other))
        choices.sort(key=lambda pair: (
            -pair[0], pair[1]["path"], pair[1]["line"], pair[1]["name"]))
        del choices[5:]

    comparisons = 0
    if release:
        # Evenly sample the lexicographically ordered unordered-pair population.
        total_pairs = total
        if budget:
            for sample in range(budget):
                pair_index = (sample * (total_pairs - 1) // (budget - 1)
                              if budget > 1 else 0)
                low, high = 0, len(rows) - 1
                while low < high:
                    mid = (low + high + 1) // 2
                    prefix = mid * (2 * len(rows) - mid - 1) // 2
                    if prefix <= pair_index:
                        low = mid
                    else:
                        high = mid - 1
                i = low
                prefix = i * (2 * len(rows) - i - 1) // 2
                j = i + 1 + (pair_index - prefix)
                score = _similarity(rows[i], rows[j])
                keep(i, score, rows[j])
                keep(j, score, rows[i])
                comparisons += 1
    elif focal:
        per_focus = budget // len(focal)
        extra = budget % len(focal)
        for focus_index, item in enumerate(focal):
            i = positions[id(item)]
            quota = min(candidate_count, per_focus + (focus_index < extra))
            if not quota:
                continue
            for sample in range(quota):
                candidate_index = (sample * (candidate_count - 1) // (quota - 1)
                                   if quota > 1 else 0)
                other_index = candidate_index if candidate_index < i else candidate_index + 1
                other = rows[other_index]
                score = _similarity(item, other)
                keep(i, score, other)
                comparisons += 1
    neighbor_rows: list[dict[str, Any]] = []
    focus_rows = rows if release else focal
    for item in focus_rows:
        index = positions[id(item)]
        ranked_items = sorted(
            ranked.get(index, []),
            key=lambda pair: (-pair[0], pair[1]["path"], pair[1]["line"], pair[1]["name"]),
        )[:5]
        neighbor_rows.append({
            "function": {key: item[key] for key in
                         ("path", "line", "qualified_name", "kind")},
            "neighbors": [
                {"score": round(score, 4), "path": other["path"],
                 "line": other["line"], "qualified_name": other["qualified_name"],
                 "kind": other["kind"]}
                for score, other in ranked_items
            ],
        })
    return neighbor_rows, {
        "algorithm": "evenly spaced deterministic sampling over sorted pair population; "
                     "score=0.7 multiset Jaccard of AST-node types + 0.3 Jaccard of lowercase "
                     "snake/camel identifier tokens",
        "population": total,
        "compared": comparisons,
        "unsampled": max(0, total - comparisons),
        "truncated": total > comparisons,
    }


def _scan_worker() -> int:
    args = json.loads(sys.argv[2])
    root_name = os.path.abspath(args["root"])
    result = _empty_result(root_name, "filesystem")
    if not _secure_walk_available():
        result["diagnostics"].append(_diagnostic(
            "secure-traversal-unavailable", root_name,
            "this platform lacks descriptor-relative no-follow directory traversal",
            "Run on a platform with openat-style O_NOFOLLOW traversal; no weaker fallback is used."))
        return _write_result(result, 1)
    try:
        root_fd = _open_absolute_directory(root_name)
    except OSError as exc:
        result["diagnostics"].append(_diagnostic(
            "root-open", root_name, str(exc),
            "Use an existing directory whose path contains no links or reparse points."))
        return _write_result(result, 2)
    try:
        result = _walk(root_fd, root_name, args)
    finally:
        os.close(root_fd)
    return _write_result(result, 1 if result["status"] == "incomplete" else 0)


def _supervise_scan(args: dict[str, Any]) -> int:
    command = [sys.executable, "-I", os.path.abspath(__file__),
               _WORKER_SCAN, json.dumps(args, ensure_ascii=True)]
    kwargs: dict[str, Any] = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "env": {"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
    }
    if os.name == "posix":
        kwargs["start_new_session"] = True
    started = time.monotonic()
    process = subprocess.Popen(command, **kwargs)
    try:
        stdout, stderr = process.communicate(timeout=COMMAND_SECONDS)
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        process.communicate()
        result = _empty_result(os.path.abspath(args["root"]), "filesystem")
        result["budgets"]["command_seconds"] = round(
            time.monotonic() - started, 3)
        result["diagnostics"].append(_diagnostic(
            "command-time-limit", result["root"],
            f"complete command exceeded {COMMAND_SECONDS:g} seconds",
            "Narrow the filesystem root; the limit is fixed for this scan."))
        return _write_result(result, 1)
    if stdout:
        elapsed = time.monotonic() - started
        try:
            result = json.loads(stdout.decode("ascii"))
        except (UnicodeError, json.JSONDecodeError):
            result = _empty_result(os.path.abspath(args["root"]), "filesystem")
            result["diagnostics"].append(_diagnostic(
                "collector-worker-failed", result["root"],
                "worker returned invalid JSON",
                "Retry with the canonical Python interpreter and a readable root."))
            return _write_result(result, 2)
        result["budgets"]["command_seconds"] = round(elapsed, 3)
        return _write_result(result, process.returncode or 0)
    result = _empty_result(os.path.abspath(args["root"]), "filesystem")
    result["diagnostics"].append(_diagnostic(
        "collector-worker-failed", result["root"],
        stderr.decode("ascii", "backslashreplace")[:500],
        "Retry with the canonical Python interpreter and a readable root."))
    return _write_result(result, 2)


def _changed_paths(paths: list[str]) -> tuple[list[str], list[str]]:
    accepted: list[str] = []
    rejected: list[str] = []
    for raw in paths:
        path = PurePosixPath(raw)
        if (path.is_absolute() or not path.parts
                or any(part in ("", ".", "..") for part in path.parts)
                or "\\" in raw):
            rejected.append(raw)
        else:
            accepted.append(path.as_posix())
    return accepted, rejected


def main(argv: list[str] | None = None) -> int:
    if len(sys.argv) > 1 and sys.argv[1] == _WORKER_PARSE:
        return _parse_source_worker()
    if len(sys.argv) > 1 and sys.argv[1] == _WORKER_SCAN:
        return _scan_worker()
    parser = argparse.ArgumentParser(
        prog="code_map", description="Bounded filesystem map and reuse leads.")
    parser.add_argument("--root", default=".", help="filesystem root to inspect")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--changed", action="append", default=[], metavar="PATH",
                      help="root-relative changed Python file; repeat as needed")
    mode.add_argument("--release", action="store_true",
                      help="compare the whole tree using the bounded pair sample")
    args = parser.parse_args(argv)
    changed, rejected = _changed_paths(args.changed)
    root = os.path.abspath(args.root)
    packed = {"root": root, "changed": changed, "release": bool(args.release)}
    if rejected:
        result = _empty_result(root, "changed")
        result["diagnostics"].extend(
            _diagnostic("invalid-changed-path", path,
                        "changed paths must be root-relative and contain no parent traversal",
                        "Pass a regular file path relative to --root.")
            for path in rejected
        )
        return _write_result(result, 2)
    return _supervise_scan(packed)


if __name__ == "__main__":
    raise SystemExit(main())
