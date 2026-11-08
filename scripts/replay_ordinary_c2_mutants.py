#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Replay sealed ordinary C2 probes in clean, disposable committed checkouts.

Git cleanliness cannot prove a checkout is disposable. The utility refuses
its own repository root, overlapping checkouts and output inside either tree.
A hard kill may interrupt restoration; dispose both supplied checkouts after
any interrupted or failed replay.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "bootstrap/tests/fixtures/ordinary_c2_promise_mutants.json"
FIXTURE_SHA256 = "d69e0361b2b83ec366fe56b472ab0625cdd53641308cf25660642aaa4234dac2"
DESCRIPTION_SHA256 = "62c27fc36c04165b983fba99fc6f3f24a069ac082f0d8ca188269f8983af6879"
FAMILIES = {
    "redundancy": ("scripts/quality_gate.py", "scripts/quality_gate.py",
                   "bootstrap/tests/integration/test_quality_gate_redundancy.py"),
    "evolution": ("tools/evolution_infer.py",
                  "templates/modules/default-on/evolution_infer.py",
                  "bootstrap/tests/integration/test_evolution_infer.py"),
}
TOP_KEYS = {"description_sha256", "list_sha256", "mutants", "candidate_only_probe"}
MUTANT_KEYS = {"id", "family", "source", "target", "old", "new", "tuple_sha256"}
EXTRA_KEYS = {"id", "family", "target", "old", "new"}
_ID = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
HAS_SAFE_OPEN = (
    os.name == "posix" and bool(_NOFOLLOW) and hasattr(os, "O_DIRECTORY")
    and os.open in os.supports_dir_fd and os.stat in os.supports_dir_fd
)


class ReplayError(RuntimeError):
    pass


def _object_no_duplicates(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ReplayError(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def _validate_manifest(data):
    if type(data) is not dict or set(data) != TOP_KEYS:
        raise ReplayError("unexpected fixture fields")
    for key in ("description_sha256", "list_sha256"):
        if type(data[key]) is not str or not re.fullmatch(r"[0-9a-f]{64}", data[key]):
            raise ReplayError(f"invalid fixture digest: {key}")
    if data["description_sha256"] != DESCRIPTION_SHA256:
        raise ReplayError("sealed description digest does not match")
    items = data["mutants"]
    if type(items) is not list or len(items) != 15:
        raise ReplayError("fixture must contain exactly fifteen sealed mutations")
    seen = set()
    for item in items:
        if type(item) is not dict or set(item) != MUTANT_KEYS:
            raise ReplayError("unexpected mutation fields")
        mid = item["id"]
        if type(mid) is not str or not _ID.fullmatch(mid) or mid in seen:
            raise ReplayError("unsafe or duplicate mutation ID")
        seen.add(mid)
        family = item["family"]
        if type(family) is not str or family not in FAMILIES:
            raise ReplayError(f"unsupported mutation family: {family!r}")
        source, target, _test = FAMILIES[family]
        if item["source"] != source or item["target"] != target:
            raise ReplayError(f"mutation path does not match fixed family: {mid}")
        if any(type(item[k]) is not str or not item[k] for k in ("old", "new")):
            raise ReplayError(f"invalid mutation text: {mid}")
        digest = hashlib.sha256(json.dumps(
            (mid, source, item["old"], item["new"]), ensure_ascii=True,
        ).encode("utf-8")).hexdigest()
        if type(item["tuple_sha256"]) is not str or digest != item["tuple_sha256"]:
            raise ReplayError(f"sealed mutation changed: {mid}")
    listing = "".join(f"{x['id']} {x['tuple_sha256']}\n" for x in items).encode()
    if hashlib.sha256(listing).hexdigest() != data["list_sha256"]:
        raise ReplayError("sealed list digest does not match")
    extra = data["candidate_only_probe"]
    if type(extra) is not dict or set(extra) != EXTRA_KEYS:
        raise ReplayError("unexpected candidate probe fields")
    if (extra["id"] != "r1_public_omit" or extra["id"] in seen
            or extra["family"] != "redundancy"
            or extra["target"] != FAMILIES["redundancy"][1]
            or any(type(extra[k]) is not str or not extra[k] for k in ("old", "new"))):
        raise ReplayError("invalid candidate-only probe")
    return items, extra


def _load_manifest():
    raw = DATA.read_bytes()
    if hashlib.sha256(raw).hexdigest() != FIXTURE_SHA256:
        raise ReplayError("canonical fixture bytes changed")
    try:
        parsed = json.loads(raw.decode("utf-8"), object_pairs_hook=_object_no_duplicates)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ReplayError("fixture is not UTF-8 JSON") from exc
    return _validate_manifest(parsed)


def _reparse(info) -> bool:
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return stat.S_ISLNK(info.st_mode) or bool(flag and getattr(info, "st_file_attributes", 0) & flag)


def _id(info):
    return info.st_dev, info.st_ino, stat.S_IFMT(info.st_mode)


def _chain(path: Path, final_dir: bool) -> tuple[Path, list[tuple[Path, tuple]]]:
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    rows = []
    parts = absolute.parts[1:]
    for index, part in enumerate(parts):
        current /= part
        try:
            info = os.lstat(current)
        except OSError as exc:
            raise ReplayError(f"path component unavailable: {current}: {exc}") from exc
        last = index == len(parts) - 1
        if _reparse(info) or (not last and not stat.S_ISDIR(info.st_mode)):
            raise ReplayError(f"path contains a link or non-directory parent: {current}")
        if last and final_dir and not stat.S_ISDIR(info.st_mode):
            raise ReplayError(f"expected directory: {current}")
        rows.append((current, _id(info)))
    if absolute.resolve(strict=True) != absolute:
        raise ReplayError(f"path is not canonical: {absolute}")
    return absolute, rows


def _check_chain(rows):
    for path, expected in rows:
        info = os.lstat(path)
        if _reparse(info) or _id(info) != expected:
            raise ReplayError(f"path component changed: {path}")


def _overlap(a: Path, b: Path) -> bool:
    return a == b or a in b.parents or b in a.parents


def _within(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _safe_open_available() -> bool:
    return HAS_SAFE_OPEN


def _root_handle(path: Path, rows) -> int:
    if not _safe_open_available():
        raise ReplayError("platform lacks no-follow directory-descriptor support")
    fd = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY | _NOFOLLOW)
    expected = dict(rows)
    current = Path(path.anchor)
    try:
        for part in path.parts[1:]:
            current /= part
            info = os.stat(part, dir_fd=fd, follow_symlinks=False)
            if _reparse(info) or not stat.S_ISDIR(info.st_mode) or _id(info) != expected[current]:
                raise ReplayError(f"unsafe checkout component: {current}")
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | _NOFOLLOW, dir_fd=fd)
            if _id(os.fstat(child)) != _id(info):
                os.close(child)
                raise ReplayError(f"checkout component changed: {current}")
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


class Checkout:
    def __init__(self, path: Path, rows):
        self.path, self.rows = path, rows
        self.fd = _root_handle(path, rows)

    def verify(self):
        _check_chain(self.rows)
        if _id(os.fstat(self.fd)) != self.rows[-1][1]:
            raise ReplayError(f"checkout root changed: {self.path}")

    def close(self):
        os.close(self.fd)


def _target_state(root: Checkout, relative: str):
    root.verify()
    parts = relative.split("/")
    if any(x in ("", ".", "..") for x in parts):
        raise ReplayError("unsafe fixed target")
    path = root.path
    rows = list(root.rows)
    for index, part in enumerate(parts):
        path /= part
        info = os.lstat(path)
        last = index == len(parts) - 1
        if (_reparse(info) or (last and (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1))
                or (not last and not stat.S_ISDIR(info.st_mode))):
            raise ReplayError(f"unsafe replay target component: {path}")
        rows.append((path, _id(info)))
    if not _within(path, root.path) or path.resolve(strict=True) != path:
        raise ReplayError(f"target escapes canonical checkout: {relative}")
    return path, rows, info


def _verify_target(root: Checkout, relative: str, rows, expected_id):
    _check_chain(root.rows)
    path, current, info = _target_state(root, relative)
    if current != rows or _id(info) != expected_id:
        raise ReplayError(f"target was replaced: {relative}")
    return path


def _read_target(root: Checkout, relative: str):
    path, rows, before = _target_state(root, relative)
    fd = os.open(path, os.O_RDONLY | _NOFOLLOW)
    try:
        opened = os.fstat(fd)
        if (_id(opened) != _id(before) or opened.st_nlink != 1
                or not stat.S_ISREG(opened.st_mode)
                or stat.S_IMODE(opened.st_mode) != stat.S_IMODE(before.st_mode)):
            raise ReplayError(f"target changed while opening: {relative}")
        chunks = []
        while True:
            part = os.read(fd, 65536)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        _verify_target(root, relative, rows, _id(opened))
        if ((after.st_size, after.st_mtime_ns, after.st_ctime_ns,
             stat.S_IMODE(after.st_mode)) !=
            (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns,
             stat.S_IMODE(opened.st_mode))):
            raise ReplayError(f"target changed while reading: {relative}")
        return b"".join(chunks), stat.S_IMODE(after.st_mode), _id(after), rows
    finally:
        os.close(fd)


def _mutant_bytes(original: bytes, old: str, new: str, mid: str):
    old_bytes, new_bytes = old.encode("utf-8"), new.encode("utf-8")
    if original.count(old_bytes) != 1:
        raise ReplayError(f"sealed byte preimage not unique or line endings differ: {mid}")
    line = original[:original.index(old_bytes)].count(b"\n") + 1
    return original.replace(old_bytes, new_bytes, 1), set(range(line, line + new_bytes.count(b"\n") + 1))


def _write_target(root: Checkout, relative: str, content: bytes, mode: int,
                  expected_id, expected_chain, expected_bytes: bytes | None,
                  on_write=None):
    path = _verify_target(root, relative, expected_chain, expected_id)
    fd = os.open(path, os.O_RDWR | _NOFOLLOW)
    try:
        opened = os.fstat(fd)
        if (_id(opened) != expected_id or opened.st_nlink != 1
                or not stat.S_ISREG(opened.st_mode) or stat.S_IMODE(opened.st_mode) != mode):
            raise ReplayError(f"target changed before writing: {relative}")
        if expected_bytes is not None:
            os.lseek(fd, 0, os.SEEK_SET)
            chunks = []
            while True:
                part = os.read(fd, 65536)
                if not part:
                    break
                chunks.append(part)
            if b"".join(chunks) != expected_bytes:
                raise ReplayError(f"target content changed before writing: {relative}")
        _verify_target(root, relative, expected_chain, expected_id)
        if on_write is not None:
            on_write()
        os.ftruncate(fd, 0)
        os.lseek(fd, 0, os.SEEK_SET)
        view = memoryview(content)
        while view:
            count = os.write(fd, view)
            if count <= 0:
                raise ReplayError(f"short write: {relative}")
            view = view[count:]
        os.fchmod(fd, mode)
        os.fsync(fd)
        after = os.fstat(fd)
        if _id(after) != expected_id or stat.S_IMODE(after.st_mode) != mode:
            raise ReplayError(f"target identity or mode changed after writing: {relative}")
        _verify_target(root, relative, expected_chain, expected_id)
    finally:
        os.close(fd)
    _verify_target(root, relative, expected_chain, expected_id)


def _clean(root: Checkout) -> bool:
    root.verify()
    result = subprocess.run(["git", "-C", str(root.path), "status", "--porcelain"],
                            capture_output=True, text=True, check=False)
    root.verify()
    return result.returncode == 0 and not result.stdout.strip()


def _write_output(output_fd: int, name: str, data: bytes):
    if Path(name).name != name or name in ("", ".", ".."):
        raise ReplayError("unsafe output name")
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | _NOFOLLOW, 0o600,
                 dir_fd=output_fd)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ReplayError(f"unsafe output file: {name}")
        view = memoryview(data)
        while view:
            count = os.write(fd, view)
            if count <= 0:
                raise ReplayError(f"short output write: {name}")
            view = view[count:]
    finally:
        os.close(fd)


_CHILD = r'''
import json, os, sys, traceback
from pathlib import Path
import pytest
source, test_path = str(Path(sys.argv[1]).resolve()), sys.argv[2]
lines = set()
class Observer:
    def __init__(self):
        self.nodes, self.phases, self.collection_errors, self.internal_errors = [], {}, [], []
        self.active_node, self.node_lines = None, {}
    def pytest_collection_finish(self, session):
        self.nodes = [item.nodeid for item in session.items]
    def pytest_collectreport(self, report):
        if report.failed:
            self.collection_errors.append({"nodeid": report.nodeid, "longrepr": str(report.longrepr)})
    def pytest_internalerror(self, excrepr, excinfo):
        self.internal_errors.append(str(excrepr))
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_call(self, item):
        self.active_node = item.nodeid
        try:
            yield
        finally:
            self.active_node = None
    def pytest_runtest_logreport(self, report):
        row = {"outcome": report.outcome, "wasxfail": getattr(report, "wasxfail", None),
               "assertion_failure": False}
        if report.when == "call" and report.failed:
            crash = getattr(report.longrepr, "reprcrash", None)
            message = getattr(crash, "message", "")
            row["assertion_failure"] = isinstance(message, str) and (
                message.startswith("assert ") or message.startswith("AssertionError"))
        self.phases.setdefault(report.nodeid, {})[report.when] = row
def trace(frame, event, arg):
    if os.path.realpath(frame.f_code.co_filename) != source:
        return None
    if event == "line":
        lines.add(frame.f_lineno)
        if observer.active_node is not None:
            observer.node_lines.setdefault(observer.active_node, set()).add(frame.f_lineno)
    return trace
observer = Observer()
sys.settrace(trace)
try:
    code = int(pytest.main([test_path, "-q", "--tb=short", "-p", "no:cacheprovider"],
                           plugins=[observer]))
    data = {"exit": code, "nodes": observer.nodes, "phases": observer.phases,
            "collection_errors": observer.collection_errors,
            "internal_errors": observer.internal_errors, "changed_lines": sorted(lines),
            "changed_lines_by_node": {k: sorted(v) for k, v in observer.node_lines.items()}}
except BaseException:
    data = {"exit": -1, "nodes": observer.nodes, "phases": observer.phases,
            "collection_errors": observer.collection_errors,
            "internal_errors": observer.internal_errors, "changed_lines": sorted(lines),
            "changed_lines_by_node": {k: sorted(v) for k, v in observer.node_lines.items()},
            "infrastructure_error": traceback.format_exc()}
finally:
    sys.settrace(None)
print("__C2_RESULT__" + json.dumps(data))
raise SystemExit(data["exit"] if data["exit"] >= 0 else 2)
'''


def _run_test(root: Checkout, test: str, target: str, output_fd: int,
              logname: str, timeout: int) -> dict:
    path, rows, _info = _target_state(root, target)
    started = time.monotonic()
    try:
        result = subprocess.run(
            [sys.executable, "-c", _CHILD, str(path), test], cwd=root.path,
            capture_output=True, text=True, timeout=timeout,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except subprocess.TimeoutExpired as exc:
        chunks = [x.decode("utf-8", "replace") if isinstance(x, bytes) else x
                  for x in (exc.stdout, exc.stderr) if x]
        _write_output(output_fd, logname, "".join(chunks).encode("utf-8"))
        return {"timeout": True, "seconds": round(time.monotonic() - started, 3),
                "infrastructure_error": "test process timed out"}
    except OSError as exc:
        _write_output(output_fd, logname, str(exc).encode("utf-8", "replace"))
        return {"seconds": round(time.monotonic() - started, 3),
                "infrastructure_error": f"test process could not start: {exc}"}
    _verify_target(root, target, rows, _id(_info))
    marker = "__C2_RESULT__"
    line = next((x for x in reversed(result.stdout.splitlines()) if x.startswith(marker)), None)
    data = {"infrastructure_error": "child did not return a result record"}
    log = result.stdout
    if line:
        try:
            data = json.loads(line[len(marker):])
        except json.JSONDecodeError:
            data = {"infrastructure_error": "child result record was invalid JSON"}
        log = result.stdout.rsplit(line, 1)[0]
    _write_output(output_fd, logname, (log + result.stderr).encode("utf-8", "replace"))
    data["process_exit"] = result.returncode
    data["seconds"] = round(time.monotonic() - started, 3)
    return data


def _ordinary_baseline(data):
    if data.get("exit") != 0 or data.get("process_exit") != 0 or not data.get("nodes"):
        return False, "baseline must collect nodes and exit zero"
    if data.get("collection_errors") or data.get("internal_errors"):
        return False, "baseline collection/internal error"
    phases = data.get("phases", {})
    if set(phases) != set(data["nodes"]):
        return False, "baseline node reports do not match collection"
    for node in data["nodes"]:
        rows = phases[node]
        if set(rows) != {"setup", "call", "teardown"}:
            return False, f"baseline phase missing: {node}"
        if any(x.get("outcome") != "passed" or x.get("wasxfail") for x in rows.values()):
            return False, f"baseline has a non-pass or xfail: {node}"
    return True, "ordinary all-pass baseline"


def _classify(data, nodeids, changed_lines):
    if data.get("timeout") or data.get("infrastructure_error"):
        return "inconclusive", "timeout or infrastructure error"
    if data.get("collection_errors") or data.get("internal_errors"):
        return "inconclusive", "collection or internal error"
    if data.get("exit") != data.get("process_exit"):
        return "inconclusive", "child and process exit reports differ"
    if data.get("nodes") != nodeids:
        return "inconclusive", "collected node IDs changed"
    phases = data.get("phases", {})
    if set(phases) != set(nodeids):
        return "inconclusive", "test reports missing or extra"
    assertion_failed = False
    reached_assertion = False
    for node in nodeids:
        rows = phases[node]
        if set(rows) != {"setup", "call", "teardown"}:
            return "inconclusive", f"phase report missing: {node}"
        for phase, row in rows.items():
            if row.get("wasxfail") or row.get("outcome") in {"skipped", "xfailed", "xpassed"}:
                return "inconclusive", f"skip/xfail: {node}:{phase}"
            if phase != "call" and row.get("outcome") != "passed":
                return "inconclusive", f"non-pass {phase}: {node}"
            if phase == "call" and row.get("outcome") == "failed":
                if not row.get("assertion_failure"):
                    return "inconclusive", f"non-assertion call failure: {node}"
                assertion_failed = True
                if changed_lines.intersection(data.get("changed_lines_by_node", {}).get(node, [])):
                    reached_assertion = True
            elif phase == "call" and row.get("outcome") != "passed":
                return "inconclusive", f"non-pass call: {node}"
    if data.get("process_exit") == 0:
        return ("inconclusive", "zero exit conflicts with failed reports") if assertion_failed else (
            "survived", "mutant exited zero")
    if (data.get("process_exit") == 1 and assertion_failed
            and reached_assertion):
        return "caught", "call assertion failed after changed line ran"
    return "inconclusive", "failure did not meet caught criteria"


def _paths(old_arg: Path, new_arg: Path, out_arg: Path):
    if not _safe_open_available():
        raise ReplayError("platform lacks required no-follow descriptor support")
    old, old_rows = _chain(old_arg, True)
    new, new_rows = _chain(new_arg, True)
    if _overlap(old, new):
        raise ReplayError("old and new checkout roots overlap")
    if _overlap(old, ROOT) or _overlap(new, ROOT):
        raise ReplayError("refusing the utility's own repository root or an overlapping root")
    out = Path(os.path.abspath(out_arg))
    if _within(out, old) or _within(out, new) or _within(out, ROOT):
        raise ReplayError("output must be outside both checkouts and the utility repository")
    _chain(out.parent, True)
    if os.path.lexists(out):
        raise ReplayError("output directory must be new")
    old_checkout = Checkout(old, old_rows)
    try:
        new_checkout = Checkout(new, new_rows)
    except BaseException:
        old_checkout.close()
        raise
    return old_checkout, new_checkout, out


def _output_dir(path: Path):
    parent, rows = _chain(path.parent, True)
    parent_fd = _root_handle(parent, rows)
    try:
        name = path.name
        if not name or name in (".", ".."):
            raise ReplayError("invalid output directory")
        _check_chain(rows)
        os.mkdir(name, 0o700, dir_fd=parent_fd)
        info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        if _reparse(info) or not stat.S_ISDIR(info.st_mode):
            raise ReplayError("output is not a plain directory")
        fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | _NOFOLLOW, dir_fd=parent_fd)
        if _id(os.fstat(fd)) != _id(info):
            os.close(fd)
            raise ReplayError("output directory changed while opening")
        _check_chain(rows)
        return fd
    finally:
        os.close(parent_fd)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old", type=Path, required=True, help="clean disposable old checkout")
    parser.add_argument("--new", type=Path, required=True, help="clean disposable new checkout")
    parser.add_argument("--output", type=Path, required=True, help="new directory outside both checkouts")
    parser.add_argument("--only", help="one fixed mutation ID")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args(argv)
    if sys.version_info[:2] != (3, 13):
        parser.error("use canonical Python 3.13")
    if not 1 <= args.timeout <= 1800:
        parser.error("timeout must be 1..1800 seconds")
    try:
        mutants, extra = _load_manifest()
        known = {x["id"] for x in mutants} | {extra["id"]}
        if args.only and args.only not in known:
            parser.error("unknown fixed mutation ID")
        selected = [x for x in mutants if not args.only or x["id"] == args.only]
        if not args.only or args.only == extra["id"]:
            selected.append(extra)
        old, new, out = _paths(args.old, args.new, args.output)
    except ReplayError as exc:
        parser.error(str(exc))
    outfd = -1
    try:
        outfd = _output_dir(out)
        for root in (old, new):
            if not _clean(root):
                raise ReplayError(f"checkout is not clean: {root.path}")
        for family in {x["family"] for x in selected}:
            _source, target, _test = FAMILIES[family]
            a = _read_target(old, target)[0]
            b = _read_target(new, target)[0]
            if a != b:
                raise ReplayError(f"old/new implementation source differs: {target}")
            source, _target, _test = FAMILIES[family]
            if source != target:
                for root in (old, new):
                    if _read_target(root, source)[0] != _read_target(root, target)[0]:
                        raise ReplayError(f"installed/template sources differ: {root.path}")

        results = []
        for label, root in (("old", old), ("new", new)):
            families = sorted({x["family"] for x in selected})
            baselines = {}
            for family in families:
                _source, target, test = FAMILIES[family]
                baseline = _run_test(root, test, target, outfd,
                                     f"{label}-{family}-baseline.log", args.timeout)
                ok, why = _ordinary_baseline(baseline)
                if not ok:
                    raise ReplayError(f"unhealthy baseline {label}-{family}: {why}")
                baselines[family] = baseline
            for item in selected:
                _source, target, test = FAMILIES[item["family"]]
                original, mode, identity, chain = _read_target(root, target)
                mutant, changed = _mutant_bytes(original, item["old"], item["new"], item["id"])
                prefix = f"{label}-{item['id']}"
                mutation_started = False
                write_complete = False
                run = None
                restore_error = None
                try:
                    def mark_write_started():
                        nonlocal mutation_started
                        mutation_started = True
                    _write_target(root, target, mutant, mode, identity, chain, original,
                                  on_write=mark_write_started)
                    write_complete = True
                    run = _run_test(root, test, target, outfd, prefix + "-mutant.log", args.timeout)
                finally:
                    if mutation_started:
                        try:
                            _write_target(root, target, original, mode, identity, chain,
                                          mutant if write_complete else None)
                            restored = _read_target(root, target)
                            if restored[:3] != (original, mode, identity) or not _clean(root):
                                raise ReplayError(f"restore verification failed: {prefix}")
                        except BaseException as exc:
                            restore_error = exc
                if restore_error:
                    raise ReplayError(f"RESTORATION FAILURE for {prefix}; dispose checkout: {restore_error}")
                if run is None:
                    raise ReplayError(f"test produced no result: {prefix}")
                outcome, detail = _classify(run, baselines[item["family"]]["nodes"], changed)
                results.append({
                    "id": item["id"], "version": label, "family": item["family"],
                    "test": test, "node_ids": run.get("nodes", []),
                    "baseline_node_ids": baselines[item["family"]]["nodes"],
                    "baseline_phases": baselines[item["family"]]["phases"],
                    "phases": run.get("phases", {}),
                    "collection_errors": run.get("collection_errors", []),
                    "internal_errors": run.get("internal_errors", []),
                    "process_exit": run.get("process_exit"),
                    "baseline_seconds": baselines[item["family"]].get("seconds"),
                    "mutant_seconds": run.get("seconds"),
                    "wasxfail": [node for node, rows in run.get("phases", {}).items()
                                 if any(row.get("wasxfail") for row in rows.values())],
                    "changed_lines": sorted(changed),
                    "reached_changed_lines": sorted(changed.intersection(run.get("changed_lines", []))),
                    "outcome": outcome, "detail": detail,
                })
                print(label, item["id"], outcome, detail, flush=True)
        _write_output(outfd, "results.json", (json.dumps(results, indent=2) + "\n").encode())
        return int(any(x["outcome"] != "caught" for x in results if x["version"] == "new"))
    except ReplayError as exc:
        print(f"replay stopped: {exc}", file=sys.stderr)
        return 2
    finally:
        if outfd >= 0:
            os.close(outfd)
        new.close()
        old.close()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
