#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Advisory functional-prose comparison for two Git revisions (stdlib only)."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import stat
import sys
import time
import types
import difflib
import unicodedata
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
_SOURCE = (os.path.basename(_HERE) == "team-gated"
           and os.path.basename(os.path.dirname(_HERE)) == "modules")
_ROOT = os.path.abspath(os.path.join(_HERE, "../../..")) if _SOURCE else os.path.dirname(_HERE)
_GIT_REL = "templates/skills/_lib/git_read.py" if _SOURCE else "tools/git_read.py"
_GIT_SHA256 = "ec471c34c18ff4698ef6f2511d4e9e5d29b76190ec2a9a9f2e8524c5827db9c3"
_HELPER_CAP = 256 * 1024
_FILE_CAP = 8 * 1024 * 1024
_TOTAL_CAP = 128 * 1024 * 1024
_TREE_CAP = 64 * 1024 * 1024
_MANIFEST_CAP = 64 * 1024
_RUN_CAP = 120.0
_OUT_CAP = 8 * 1024 * 1024
_UNIT_CAP = 2048
_START = time.monotonic()


class Incomplete(Exception):
    pass


def _checked_file(path: str, limit: int) -> bytes:
    chain = []
    drive, tail = os.path.splitdrive(os.path.abspath(path))
    current = drive + os.sep
    for part in (p for p in tail.split(os.sep) if p):
        current = os.path.join(current, part)
        info = os.lstat(current)
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise Incomplete("linked helper path")
        if current != path and not stat.S_ISDIR(info.st_mode):
            raise Incomplete("non-directory helper parent")
        chain.append((current, info))
    before = chain[-1][1]
    if not stat.S_ISREG(before.st_mode) or before.st_size < 0 or before.st_size > limit:
        raise Incomplete("helper size or type refused")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0) |
                 getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    try:
        opened = os.fstat(fd)
        opened_key = list((opened.st_dev, opened.st_ino, opened.st_mode, opened.st_size,
                           opened.st_mtime_ns, opened.st_ctime_ns,
                           getattr(opened, "st_uid", 0), getattr(opened, "st_gid", 0),
                           getattr(opened, "st_file_attributes", 0), getattr(opened, "st_reparse_tag", 0)))
        path_key = list((before.st_dev, before.st_ino, before.st_mode, before.st_size,
                         before.st_mtime_ns, before.st_ctime_ns,
                         getattr(before, "st_uid", 0), getattr(before, "st_gid", 0),
                         getattr(before, "st_file_attributes", 0), getattr(before, "st_reparse_tag", 0)))
        if os.name == "nt":
            path_birth = getattr(before, "st_birthtime_ns", None)
            descriptor_birth = getattr(opened, "st_birthtime_ns", None)
            if (type(path_birth) is not int or type(descriptor_birth) is not int or
                    before.st_ctime_ns != path_birth or path_birth != descriptor_birth):
                raise Incomplete("helper creation-time mapping failed")
            opened_key[5] = descriptor_birth
        if tuple(opened_key) != tuple(path_key):
            raise Incomplete("helper changed while opening")
        data = bytearray()
        while len(data) <= limit:
            part = os.read(fd, min(65536, limit + 1 - len(data)))
            if not part:
                break
            data.extend(part)
        after = os.fstat(fd)
        if (len(data) != opened.st_size or len(data) > limit or
            (opened.st_dev, opened.st_ino, opened.st_mode, opened.st_size,
             opened.st_mtime_ns, opened.st_ctime_ns, getattr(opened, "st_uid", 0),
             getattr(opened, "st_gid", 0), getattr(opened, "st_file_attributes", 0),
             getattr(opened, "st_reparse_tag", 0)) !=
            (after.st_dev, after.st_ino, after.st_mode, after.st_size,
             after.st_mtime_ns, after.st_ctime_ns, getattr(after, "st_uid", 0),
             getattr(after, "st_gid", 0), getattr(after, "st_file_attributes", 0),
             getattr(after, "st_reparse_tag", 0))):
            raise Incomplete("helper changed while reading")
        for name, old in chain:
            now = os.lstat(name)
            if (now.st_dev, now.st_ino, now.st_mode, now.st_size,
                now.st_mtime_ns, now.st_ctime_ns) != (
                old.st_dev, old.st_ino, old.st_mode, old.st_size,
                old.st_mtime_ns, old.st_ctime_ns):
                raise Incomplete("helper path changed while reading")
        return bytes(data)
    finally:
        os.close(fd)


def _load_git():
    if not _SOURCE:
        _require_lock_hash("tools/git_read.py", _GIT_SHA256)
    data = _checked_file(os.path.join(_ROOT, _GIT_REL), _HELPER_CAP)
    digest = hashlib.sha256(data).hexdigest()
    if digest != _GIT_SHA256:
        raise Incomplete("trusted Git helper hash mismatch")
    mod = types.ModuleType("_cairn_verified_prose_git_read")
    mod.__file__ = "<verified git_read.py buffer>"
    mod.__verified_source__ = data
    mod.__verified_sha256__ = digest
    exec(compile(data, mod.__file__, "exec", dont_inherit=True), mod.__dict__)
    mod.bind_verified_source(data, digest)
    return mod


def _require_lock_hash(destination: str, digest: str) -> None:
    lock_path = os.path.join(_ROOT, "dev", ".cairn", "cairn-lock.yml")
    raw = _checked_file(lock_path, 2 * 1024 * 1024)
    try:
        body = "\n".join(line for line in raw.decode("utf-8", "strict").splitlines()
                           if not line.lstrip().startswith("#"))
        lock = json.loads(body)
    except (UnicodeError, ValueError, RecursionError, MemoryError):
        raise Incomplete("install lock is invalid") from None
    files = lock.get("files") if isinstance(lock, dict) else None
    if not isinstance(files, list): raise Incomplete("install lock has no file records")
    matches = [row for row in files if isinstance(row, dict) and row.get("dst") == destination]
    if (len(matches) != 1 or matches[0].get("verbatim") is not True or
            matches[0].get("hash") != digest):
        raise Incomplete("install lock does not uniquely pin the trusted binding")


def _git(helper, root: str, args: tuple[str, ...], cap: int = _TOTAL_CAP) -> bytes:
    if time.monotonic() - _START > _RUN_CAP:
        raise Incomplete("120-second report deadline exceeded")
    result = helper.run_git(root, args, timeout=10, output_limit=cap)
    if result.state != "completed" or result.returncode != 0:
        raise Incomplete("Git read failed or exceeded its bound: " + str(result.reason or result.state))
    if time.monotonic() - _START > _RUN_CAP:
        raise Incomplete("120-second report deadline exceeded")
    return result.stdout


def _oid(helper, root: str, rev: str) -> str:
    if not rev or rev.startswith("-") or "\x00" in rev:
        raise Incomplete("invalid revision argument")
    out = _git(helper, root, ("rev-parse", "--verify", "--end-of-options", rev + "^{commit}"), 4096)
    value = out.decode("ascii", "strict").strip()
    if not re.fullmatch(r"[0-9a-fA-F]{40,64}", value):
        raise Incomplete("revision did not resolve to one commit")
    return value


def _merge_base(helper, root: str, a: str, b: str) -> str:
    out = _git(helper, root, ("rev-parse", "--revs-only", "--end-of-options", a + "..." + b), 4096)
    values = out.decode("ascii", "strict").splitlines()
    excluded = {x[1:] for x in values if x.startswith("^")}
    bases = [x for x in values if not x.startswith("^") and x not in excluded]
    if len(bases) != 1 or not re.fullmatch(r"[0-9a-fA-F]{40,64}", bases[0]):
        raise Incomplete("merge base is unavailable or ambiguous")
    return bases[0]


def _blob(helper, root: str, oid: str, cap: int) -> bytes:
    if not re.fullmatch(r"[0-9a-fA-F]{40,64}", oid):
        raise Incomplete("invalid tree object id")
    return _git(helper, root, ("cat-file", "blob", oid), cap)


def _tree(helper, root: str, oid: str):
    raw = _git(helper, root, ("ls-tree", "-r", "-z", oid), _TREE_CAP)
    rows = {}
    for rec in raw.split(b"\0"):
        if not rec:
            continue
        try:
            meta, name = rec.split(b"\t", 1)
            mode, kind, blob = meta.decode("ascii").split(" ")
            path = name.decode("utf-8", "strict")
        except (ValueError, UnicodeError):
            raise Incomplete("tree enumeration was malformed") from None
        rows[path] = (mode, kind, blob)
    return rows


def _manifest(helper, root: str, tree, path: str, sentinel: str, bang: bool):
    row = tree.get(path)
    if not row or row[1] != "blob" or row[0] == "120000":
        raise Incomplete("missing or linked base manifest: " + path)
    data = _blob(helper, root, row[2], _MANIFEST_CAP)
    text = data.decode("utf-8", "strict")
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    if not lines or lines[0] != sentinel:
        raise Incomplete("invalid base manifest: " + path)
    roots = []
    for line in text.splitlines():
        value = line.split("#", 1)[0].strip()
        if not value:
            continue
        required = value.startswith("!")
        if required and not bang:
            raise Incomplete("negated prose root is invalid")
        if required:
            value = value[1:].strip()
        lexical = Path(value)
        if not value or lexical.is_absolute() or ".." in lexical.parts or value.startswith("-"):
            raise Incomplete("invalid repository-relative root")
        roots.append((lexical.as_posix().rstrip("/"), required))
    return roots


def _covered(path: str, roots) -> bool:
    return any(path == root or path.startswith(root + "/") for root, _required in roots)


def _norm(text: str) -> str:
    return " ".join(text.split())


def _markdown_units(text: str):
    units = []
    fence = False
    para = []
    def flush():
        if para:
            joined = " ".join(para)
            for item in re.split(r"(?<=[.!?])\s+", joined):
                if item.strip():
                    units.append(("sentence", _norm(item)))
            para.clear()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush(); units.append(("fence", _norm(stripped))); fence = not fence
        elif fence:
            flush(); units.append(("fence", _norm(line)))
        elif not stripped:
            flush()
        elif stripped.startswith("#"):
            flush(); units.append(("heading", _norm(stripped)))
        elif stripped.startswith("|"):
            flush(); units.append(("table", _norm(stripped)))
        elif re.match(r"^(?:[-*+]\s|\d+[.)]\s)", stripped):
            flush(); units.append(("list", _norm(stripped)))
        else:
            para.append(stripped)
    flush()
    return units


def _py_units(text: str):
    tree = ast.parse(text)
    units, short = [], 0
    seen = set()
    fstring_literals = {id(part) for joined in ast.walk(tree)
                         if isinstance(joined, ast.JoinedStr)
                         for part in joined.values
                         if isinstance(part, ast.Constant) and isinstance(part.value, str)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if id(node) in fstring_literals:
                continue
            # An implicit-join group is one Constant. Skip docstring duplication
            # because its Constant is already visited by the tree walk.
            value = node.value
            words = re.findall(r"\b\w+\b", value)
            if len(words) < 6:
                short += 1
            else:
                units.append(("python-string", _norm(value)))
        elif isinstance(node, ast.JoinedStr) and id(node) not in seen:
            seen.add(id(node))
            bits = []
            for part in node.values:
                bits.append(part.value if isinstance(part, ast.Constant) and isinstance(part.value, str) else "{}")
            value = "".join(bits)
            words = re.findall(r"\b\w+\b", value)
            if len(words) < 6:
                short += 1
            else:
                units.append(("python-string", _norm(value)))
    return units, short


def _escape(value: str) -> str:
    out = []
    for ch in value:
        n = ord(ch)
        if unicodedata.category(ch) in {"Cc", "Cf"}:
            out.append(f"\\u{n:04x}")
        else:
            out.append(ch)
    return "".join(out)


def _bounded_lines(lines):
    bounded, rendered = [], 0
    for line in lines:
        size = len(line.encode("utf-8")) + 1
        if size > _OUT_CAP or rendered + size > _OUT_CAP:
            bounded.append("INCOMPLETE: rendered output exceeded 8 MiB; later findings omitted")
            break
        bounded.append(line); rendered += size
    return bounded


def _compare(helper, root: str, base: str, head: str) -> str:
    btree, htree = _tree(helper, root, base), _tree(helper, root, head)
    roots = _manifest(helper, root, btree, "scripts/content_scan_roots.txt", "# content-scan-roots v1", True)
    roots += _manifest(helper, root, btree, "scripts/prose_roots.txt", "# prose-roots v1", False)
    for path, required in roots:
        if required:
            candidates = [name for name in btree if (name == path or name.startswith(path + "/"))
                          and os.path.splitext(name)[1].lower() in {".md", ".txt"}]
            if not candidates:
                raise Incomplete("required base root is absent or contributes no tracked prose: " + _escape(path))
    first = []
    for path in ("scripts/content_scan_roots.txt", "scripts/prose_roots.txt", "scripts/prose_diff.py"):
        if btree.get(path) != htree.get(path):
            first.append(f"NOTICE first: {path} changed; base roots/tool policy govern this report")
    total = 0
    output = []
    rendered = sum(len(x.encode("utf-8")) + 1 for x in first)
    for path in sorted(set(btree) | set(htree)):
        if time.monotonic() - _START > _RUN_CAP:
            output.append("INCOMPLETE: 120-second deadline exceeded; later files omitted")
            break
        if not _covered(path, roots):
            continue
        suffix = os.path.splitext(path)[1].lower()
        before, after = btree.get(path), htree.get(path)
        if before == after:
            continue
        output_start = len(output)
        if suffix not in {".md", ".txt", ".py"}:
            output.append(f"NOT COMPARED { _escape(path) }: unsupported suffix {suffix!r}"); continue
        if any(row and (row[1] != "blob" or row[0] == "120000") for row in (before, after)):
            output.append(f"NOT COMPARED {_escape(path)}: link or gitlink"); continue
        try:
            old = _blob(helper, root, before[2], _FILE_CAP).decode("utf-8", "strict") if before else ""
            new = _blob(helper, root, after[2], _FILE_CAP).decode("utf-8", "strict") if after else ""
            total += len(old.encode()) + len(new.encode())
            if total > _TOTAL_CAP:
                raise Incomplete("aggregate blob cap exceeded")
            if suffix == ".py":
                old_units, old_short = _py_units(old)
                new_units, new_short = _py_units(new)
                short = old_short + new_short
            else:
                old_units, new_units = _markdown_units(old), _markdown_units(new)
                short = 0
            if len(old_units) > _UNIT_CAP or len(new_units) > _UNIT_CAP:
                output.append(f"INCOMPLETE {_escape(path)}: unit cap exceeded; this file was omitted"); continue
            matcher = difflib.SequenceMatcher(a=old_units, b=new_units, autojunk=False)
            changed = False
            for tag, i, j, k, l in matcher.get_opcodes():
                if tag == "equal": continue
                changed = True
                if tag == "replace":
                    output.append(f"CHANGED {_escape(path)}: before {_escape(' | '.join(v for _t, v in old_units[i:j]))} ; after {_escape(' | '.join(v for _t, v in new_units[k:l]))}")
                else:
                    if tag == "delete":
                        for typ, val in old_units[i:j]: output.append(f"REMOVED {_escape(path)} [{typ}]: {_escape(val)}")
                    if tag == "insert":
                        for typ, val in new_units[k:l]: output.append(f"ADDED {_escape(path)} [{typ}]: {_escape(val)}")
            if not changed and old != new:
                output.append(f"REFLOW ONLY {_escape(path)}")
            if suffix == ".py":
                output.append(f"GAPS {_escape(path)}: {short} short Python string constants skipped; runtime and '+' construction not compared")
        except Incomplete:
            raise
        except (UnicodeError, SyntaxError, RecursionError, MemoryError, ValueError) as exc:
            output.append(f"NOT COMPARED {_escape(path)}: {_escape(str(exc))}")
        rendered += sum(len(x.encode("utf-8")) + 1 for x in output[output_start:])
        if rendered > _OUT_CAP:
            output = output[:max(1, len(output) // 2)] + ["INCOMPLETE: rendered output exceeded 8 MiB; later findings omitted"]
            break
    lines = [*first, *output]
    lines = _bounded_lines(lines)
    return "\n".join(lines) if lines else "No functional prose changes found in the base-root union."


def report_text_change(helper, root: str, target: str, old: str, new: str) -> str:
    """Report one already validated in-memory edit using roots in committed HEAD."""
    version = helper.read_version(root)
    if version.state != "completed":
        raise Incomplete("Git version could not be established")
    match = re.search(rb"version\s+(\d+)\.(\d+)", version.stdout)
    if not match or tuple(map(int, match.groups())) < (2, 45):
        raise Incomplete("Git 2.45 or later is required")
    head = _oid(helper, root, "HEAD")
    tree = _tree(helper, root, head)
    roots = _manifest(helper, root, tree, "scripts/content_scan_roots.txt", "# content-scan-roots v1", True)
    roots += _manifest(helper, root, tree, "scripts/prose_roots.txt", "# prose-roots v1", False)
    if target in {"scripts/content_scan_roots.txt", "scripts/prose_roots.txt", "scripts/prose_diff.py"}:
        return f"NOTICE first: {target} is a roots/report-tool edit; committed HEAD roots govern this report."
    if not _covered(target, roots):
        return f"NOT COMPARED { _escape(target) }: outside committed functional-prose roots"
    suffix = os.path.splitext(target)[1].lower()
    if suffix not in {".md", ".txt", ".py"}:
        return f"NOT COMPARED {_escape(target)}: unsupported suffix {suffix!r}"
    try:
        left, right = old.encode("utf-8", "strict"), new.encode("utf-8", "strict")
        if max(len(left), len(right)) > _FILE_CAP or len(left) + len(right) > _TOTAL_CAP:
            return f"NOT COMPARED {_escape(target)}: in-memory input cap exceeded"
        if suffix == ".py":
            a, short_a = _py_units(old); b, short_b = _py_units(new)
            short = short_a + short_b
        else:
            a, b, short = _markdown_units(old), _markdown_units(new), 0
        if len(a) > _UNIT_CAP or len(b) > _UNIT_CAP:
            raise Incomplete("in-memory report exceeded 2,048 units")
        matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        lines = []
        for tag, i, j, k, l in matcher.get_opcodes():
            if tag == "equal": continue
            if tag == "replace":
                lines.append(f"CHANGED {_escape(target)}: before {_escape(' | '.join(v for _t, v in a[i:j]))} ; after {_escape(' | '.join(v for _t, v in b[k:l]))}")
            elif tag == "delete":
                lines.extend(f"REMOVED {_escape(target)} [{t}]: {_escape(v)}" for t, v in a[i:j])
            else:
                lines.extend(f"ADDED {_escape(target)} [{t}]: {_escape(v)}" for t, v in b[k:l])
        if not lines and old != new: lines.append(f"REFLOW ONLY {_escape(target)}")
        if suffix == ".py": lines.append(f"GAPS: {short} short Python string constants skipped; runtime and '+' construction not compared")
        if any(line.startswith("INCOMPLETE") for line in lines):
            raise Incomplete("in-memory report exceeded the rendered output cap")
        lines = _bounded_lines(lines)
        if any(line.startswith("INCOMPLETE") for line in lines):
            raise Incomplete("in-memory report exceeded the rendered output cap")
        return "\n".join(lines) if lines else "No functional prose unit changed."
    except (UnicodeError, SyntaxError, RecursionError, MemoryError) as exc:
        return f"NOT COMPARED {_escape(target)}: {_escape(str(exc))}"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="prose_diff.py")
    parser.add_argument("base", nargs="?")
    parser.add_argument("head", nargs="?", default="HEAD")
    parser.add_argument("--default-branch", dest="default_branch")
    args = parser.parse_args(argv)
    try:
        if time.monotonic() - _START > _RUN_CAP: raise Incomplete("time limit exceeded")
        helper = _load_git()
        root_raw = _git(helper, _ROOT, ("rev-parse", "--show-toplevel"), 4096)
        root = root_raw.decode("utf-8", "strict").strip()
        version = helper.read_version(root)
        version_match = re.search(rb"version\s+(\d+)\.(\d+)", version.stdout) if version.state == "completed" else None
        if not version_match or tuple(map(int, version_match.groups())) < (2, 45):
            raise Incomplete("Git 2.45 or later is required")
        head = _oid(helper, root, args.head)
        if args.base:
            base = _oid(helper, root, args.base)
        else:
            ref = args.default_branch
            if ref is None:
                try:
                    ref = _git(helper, root, ("rev-parse", "--symbolic-full-name", "--verify", "--end-of-options", "refs/remotes/origin/HEAD"), 4096).decode("utf-8", "strict").strip()
                except Exception:
                    raise Incomplete("default branch metadata unavailable; use --default-branch REF") from None
            if not ref or ref.startswith("-"):
                raise Incomplete("invalid default branch ref")
            branch = _oid(helper, root, ref)
            base = _merge_base(helper, root, head, branch)
        if time.monotonic() - _START > _RUN_CAP: raise Incomplete("time limit exceeded")
        report = _compare(helper, root, base, head)
        if time.monotonic() - _START > _RUN_CAP: raise Incomplete("120-second report deadline exceeded")
        print(report)
        return 2 if "INCOMPLETE" in report else 0
    except (Incomplete, OSError, ValueError, UnicodeError, RecursionError, MemoryError) as exc:
        print("INCOMPLETE: " + _escape(str(exc)), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
