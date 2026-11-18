"""Private revision evidence and durable publication for layout upgrades."""
from __future__ import annotations

import ast
import json
import os
import re
import secrets
import shutil
import stat
from pathlib import Path
from typing import NamedTuple

from .lockfile import _git_read_helper, _resolve_commit_oid, _sha256_hex
from .security import (
    ScaffoldSecurityError,
    _assert_safe_write,
    _read_regular_bytes,
    _remove_unchanged_file,
    _stage_exclusive,
)

JOURNAL = "dev/.cairn-upgrade/layout"
RECEIPT = f"{JOURNAL}/receipt.json"
_CONFIGS = ("install/_scaffold/config.py", "bootstrap/_scaffold/config.py")
_HEX = re.compile(r"[0-9a-f]{64}")
_OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")


def _git(root: Path, *args: str, limit: int = 8 * 1024 * 1024) -> bytes:
    try:
        result = _git_read_helper().run_git(str(root), args, timeout=30, output_limit=limit)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ScaffoldSecurityError("could not read the selected Cairn Git history") from exc
    if result.state != "completed" or result.returncode != 0:
        raise ScaffoldSecurityError("could not read the selected Cairn Git history")
    return result.stdout


def resolve_revision(root: Path, revision: str) -> str:
    oid = _resolve_commit_oid(root, revision)
    if oid is None:
        raise ScaffoldSecurityError("the selected Cairn revision is unavailable")
    return oid


class SourceBlob(NamedTuple):
    oid: str
    raw: bytes
    mode: int


class SourceRevision:
    """Read exact regular blobs and static installer rows, never import history."""

    def __init__(self, root: Path, oid: str):
        self.root = root
        self.oid = oid
        self._blobs: dict[str, SourceBlob | None] = {}
        tree = _git(root, "ls-tree", "-r", "-z", oid)
        self._tree = {}
        for entry in tree.split(b"\0"):
            if entry:
                header, path = entry.split(b"\t", 1)
                self._tree[path] = header.split(b" ")
        self.config = next((blob for path in _CONFIGS if (blob := self.blob(path))), None)
        self.rows = installer_rows(self.config.raw) if self.config else set()

    def blob(self, path: str) -> SourceBlob | None:
        if path in self._blobs:
            return self._blobs[path]
        metadata = self._tree.get(path.encode("utf-8"))
        if metadata is None:
            self._blobs[path] = None
            return None
        mode, kind, object_id = metadata
        oid = object_id.decode("ascii")
        if kind != b"blob" or mode not in (b"100644", b"100755") or not _OID.fullmatch(oid):
            raise ScaffoldSecurityError(f"Cairn source at {path} is not a regular blob")
        blob = SourceBlob(oid, _git(self.root, "cat-file", "blob", oid), int(mode, 8) & 0o777)
        self._blobs[path] = blob
        return blob

    def includes(self, other: str) -> bool:
        if self.oid == other:
            return True
        # A descendant in HEAD's ancestry proves reachability. Keep the read
        # bounded even when the two histories are far apart.
        return bool(_git(self.root, "rev-list", "--max-count=1", f"--ancestry-path={other}",
                         f"{other}..{self.oid}", limit=128).strip())


def installer_rows(raw: bytes) -> set[tuple[str, str, str, bool]]:
    """Recognize the literal mappings used by both installer layouts."""
    try:
        tree = ast.parse(raw)
        registry = {node.target.id: node.value for node in tree.body
                    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)}
        rows = set()
        for name, owner in (("_CORE_MAPPINGS", "core"), ("_SKILLS_MAPPINGS", "skills")):
            for row in ast.literal_eval(registry[name]):
                src, dst = row[:2]
                rows.add((owner, f"templates/{src}", dst, row[2] if len(row) == 3 else False))
        optional = registry.get("_OPTIONAL_TEMPLATES")
        if isinstance(optional, (ast.List, ast.Tuple)):
            for row in optional.elts:
                src, dst = [ast.literal_eval(item) for item in row.elts[:2]]
                rows.add(("optional:human_team", f"templates/{src}", dst, False))
        modules = registry["_MODULE_MAPPINGS"]
        if not isinstance(modules, ast.Dict):
            raise ValueError("module registry is not literal")
        for key, items in zip(modules.keys, modules.values):
            owner = f"module:{ast.literal_eval(key)}"
            for spec in items.elts:
                if (not isinstance(spec, ast.Call) or not isinstance(spec.func, ast.Name)
                        or spec.func.id != "InstallSpec"):
                    raise ValueError("unrecognized install row")
                values = [ast.literal_eval(arg) for arg in spec.args]
                src, dst = values[:2]
                verbatim = values[2] if len(values) == 3 else False
                for keyword in spec.keywords:
                    if keyword.arg == "verbatim":
                        verbatim = ast.literal_eval(keyword.value)
                rows.add((owner, f"templates/modules/{src}", dst, verbatim))
        return rows
    except (AttributeError, KeyError, IndexError, SyntaxError, TypeError, ValueError) as exc:
        raise ScaffoldSecurityError("the Cairn installer mapping is not a recognized static registry") from exc


class FileState(NamedTuple):
    raw: bytes
    mode: int
    identity: tuple[int, int]

    def seal(self) -> list:
        return [_sha256_hex(self.raw), self.mode, list(self.identity)]


def _identity(info: os.stat_result) -> tuple[int, int]:
    return info.st_dev, info.st_ino


def read_state(target: Path, name: str, *, publisher: Path | None = None) -> FileState | None:
    path = target / name
    _assert_safe_write(path, target)
    try:
        before = path.lstat()
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(before.st_mode):
        raise ScaffoldSecurityError(f"{name} is not a regular file")
    # A process can stop between publishing a hard link and dropping its
    # journal name. This one matching second name can be resumed.
    linked = before.st_nlink != 1
    if linked:
        if publisher is None or before.st_nlink != 2:
            raise ScaffoldSecurityError(f"{name} has unexpected hard links")
        _assert_safe_write(publisher, target)
        try:
            published = publisher.lstat()
        except FileNotFoundError as exc:
            raise ScaffoldSecurityError(f"{name} has unexpected hard links") from exc
        if not stat.S_ISREG(published.st_mode) or _identity(published) != _identity(before):
            raise ScaffoldSecurityError(f"{name} has unexpected hard links")
    raw = _read_regular_bytes(path, single_link=not linked)
    try:
        after = path.lstat()
    except FileNotFoundError as exc:
        raise ScaffoldSecurityError(f"{name} changed during the layout check") from exc
    if raw is None or (after.st_mode, after.st_size, after.st_mtime_ns, after.st_ctime_ns,
                       _identity(after)) != (before.st_mode, before.st_size, before.st_mtime_ns,
                                             before.st_ctime_ns, _identity(before)):
        raise ScaffoldSecurityError(f"{name} changed during the layout check")
    return FileState(raw, stat.S_IMODE(after.st_mode), _identity(after))


def pending(target: Path) -> bool:
    return _read_private(target, RECEIPT) is not None


def _encode(value: dict) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def _sync_dir(folder: Path) -> None:
    # Python's ordinary directory descriptors are a POSIX interface.
    if os.name != "nt":
        fd = os.open(folder, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def _folders(target: Path, folder: Path) -> None:
    _assert_safe_write(folder, target)
    if folder == target or folder.is_dir():
        return
    _folders(target, folder.parent)
    folder.mkdir(exist_ok=True)
    _sync_dir(folder.parent)


def _flushed_temp(target: Path, path: Path, raw: bytes, mode: int) -> Path:
    _folders(target, path.parent)
    tmp = _stage_exclusive(path, raw, target)
    try:
        # Windows needs a writable handle to set file attributes and flush it.
        access = os.O_RDWR if os.name == "nt" else os.O_RDONLY
        flags = access | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0)
        fd = os.open(tmp, flags)
        try:
            if hasattr(os, "fchmod"):
                os.fchmod(fd, mode)
            else:
                os.chmod(tmp, mode)
            os.fsync(fd)
        finally:
            os.close(fd)
    except BaseException:
        tmp.unlink()
        raise
    return tmp


def _local_mode(mode: int) -> int:
    if os.name == "nt":
        return 0o666 if mode & stat.S_IWRITE else 0o444
    return mode


def _replace(target: Path, name: str, raw: bytes, mode: int, expected: FileState) -> None:
    path = target / name
    tmp = _flushed_temp(target, path, raw, mode)
    try:
        if read_state(target, name) != expected:
            raise ScaffoldSecurityError(f"{name} changed before layout publication")
        os.replace(tmp, path)
        _sync_dir(path.parent)
    finally:
        tmp.unlink(missing_ok=True)


def _private_ready(target: Path, name: str) -> Path:
    return target / JOURNAL / ("ready-" + _sha256_hex(name.encode("utf-8")))


def _read_private(target: Path, name: str) -> FileState | None:
    return read_state(target, name, publisher=_private_ready(target, name))


def _stage_private(target: Path, name: str, raw: bytes, mode: int) -> None:
    """Publish a journal file exclusively; a crash may leave its known alias."""
    path = target / name
    ready = _private_ready(target, name)
    ready_name = ready.relative_to(target).as_posix()
    current = _read_private(target, name)
    if current is None:
        prepared = read_state(target, ready_name)
        if prepared is None:
            tmp = _flushed_temp(target, ready, raw, mode)
            try:
                if read_state(target, ready_name) is None:
                    os.replace(tmp, ready)
                    _sync_dir(ready.parent)
            finally:
                tmp.unlink(missing_ok=True)
            prepared = read_state(target, ready_name)
        if prepared is None or (prepared.raw, prepared.mode) != (raw, mode):
            raise ScaffoldSecurityError(f"layout preparation for {name} changed")
        _assert_safe_write(path, target)
        os.link(ready, path)
    elif (current.raw, current.mode) != (raw, mode):
        raise ScaffoldSecurityError(f"layout stage file {name} changed")
    _sync_dir(path.parent)
    _drop_publisher(target, ready, path)


def _drop_publisher(target: Path, publisher: Path, path: Path) -> None:
    _assert_safe_write(publisher, target)
    try:
        identity = _identity(publisher.lstat())
    except FileNotFoundError:
        return
    _assert_safe_write(path, target)
    if identity != _identity(path.lstat()):
        raise ScaffoldSecurityError(f"layout publication file for {path.name} changed")
    publisher.unlink()
    _sync_dir(publisher.parent)


def _payload_name(digest: str) -> str:
    if not isinstance(digest, str) or not _HEX.fullmatch(digest):
        raise ScaffoldSecurityError("invalid layout payload digest")
    return f"{JOURNAL}/payload-{digest}"


def _payload(target: Path, digest: str) -> bytes:
    name = _payload_name(digest)
    payload = _read_private(target, name)
    if payload is None or _sha256_hex(payload.raw) != digest:
        raise ScaffoldSecurityError(f"the staged layout payload {name} changed")
    return payload.raw


class Transaction:
    """Snapshot reader and write set. The planner supplies every path it uses."""

    def __init__(self, target: Path, source: dict, saved: dict | None = None):
        self.target = target
        self.source = source
        self.saved = saved
        self.inputs: dict[str, FileState | None] = {}
        self.outputs: dict[str, tuple[bytes, int]] = {}
        self.actions: list[tuple[str, str, str]] = []
        self.retire: dict[str, str] = {}

    def read(self, name: str) -> FileState | None:
        if name not in self.inputs:
            if self.saved is None:
                state = read_state(self.target, name)
            else:
                try:
                    entry = self.saved["inputs"][name]
                    state = None if entry is None else FileState(
                        _payload(self.target, entry[0]), entry[1], tuple(entry[2]))
                except (KeyError, IndexError, TypeError) as exc:
                    raise ScaffoldSecurityError(f"missing layout receipt input for {name}") from exc
            self.inputs[name] = state
        return self.inputs[name]

    def write(self, name: str, raw: bytes, mode: int, *, absent: bool = False) -> None:
        prior = self.read(name)
        if absent and prior is not None:
            raise ScaffoldSecurityError(f"{name} is occupied; preserve it and resolve the layout collision")
        self.outputs[name] = raw, _local_mode(mode)

    def receipt(self) -> bytes:
        return _encode({
            "schema": 1, "target": str(self.target),
            "identity": _identity(self.target.lstat()), "source": self.source,
            "inputs": {name: state.seal() if state else None for name, state in self.inputs.items()},
            "outputs": {name: [_sha256_hex(raw), mode] for name, (raw, mode) in self.outputs.items()},
            "actions": self.actions,
        })

    def stage(self) -> str:
        payloads = [state.raw for state in self.inputs.values() if state is not None]
        payloads.extend(raw for raw, _ in self.outputs.values())
        for raw in set(payloads):
            digest = _sha256_hex(raw)
            name = _payload_name(digest)
            _stage_private(self.target, name, raw, _local_mode(0o600))
        receipt = self.receipt()
        _stage_private(self.target, RECEIPT, receipt, _local_mode(0o600))
        return _sha256_hex(receipt)

    def _publisher(self, name: str) -> Path:
        return self.target / JOURNAL / ("publish-" + _sha256_hex(name.encode("utf-8")))

    def _check(self, lock_name: str) -> bool:
        live = read_state(self.target, lock_name)
        before = self.inputs[lock_name]
        lock_output = self.outputs[lock_name]
        after = live is not None and (live.raw, live.mode) == lock_output
        if live != before and not after:
            raise ScaffoldSecurityError(f"{lock_name} differs from both layout lock states")
        for name, expected in self.inputs.items():
            if name == lock_name:
                continue
            publisher = self._publisher(name) if name in self.outputs and expected is None else None
            state = read_state(self.target, name, publisher=publisher)
            same_input = state == expected
            is_output = (name in self.outputs and state is not None
                         and (state.raw, state.mode) == self.outputs[name])
            if name in self.outputs:
                valid = is_output or (not after and same_input)
            else:
                valid = same_input or (after and name in self.retire and state is None)
            if not valid:
                raise ScaffoldSecurityError(f"{name} changed during the layout transaction")
        return after

    def _publish(self, name: str, raw: bytes, mode: int) -> None:
        target = self.target
        path = target / name
        publisher = self._publisher(name)
        present = read_state(target, name, publisher=publisher)
        publish_name = publisher.relative_to(target).as_posix()
        _assert_safe_write(publisher, target)
        if present is None:
            _stage_private(target, publish_name, raw, mode)
            _folders(target, path.parent)
            _assert_safe_write(path, target)
            os.link(publisher, path)
        elif (present.raw, present.mode) != (raw, mode):
            raise ScaffoldSecurityError(f"{name} changed before layout publication")
        _sync_dir(path.parent)
        _drop_publisher(target, publisher, path)

    def apply(self, raw_receipt: bytes, lock_name: str, profile_name: str, guard) -> None:
        if self.receipt() != raw_receipt:
            raise ScaffoldSecurityError("the layout receipt no longer matches the verified plan")
        for raw, _ in self.outputs.values():
            _payload(self.target, _sha256_hex(raw))
        after = self._check(lock_name)
        guard(after, self)
        if not after:
            for name, (raw, mode) in self.outputs.items():
                if name not in (lock_name, profile_name):
                    self._publish(name, raw, mode)
            if profile_name in self.outputs:
                raw, mode = self.outputs[profile_name]
                before = self.inputs[profile_name]
                current = read_state(self.target, profile_name, publisher=self._publisher(profile_name))
                if current == before:
                    if before is None:
                        self._publish(profile_name, raw, mode)
                    else:
                        _replace(self.target, profile_name, raw, mode, before)
                elif current is None or (current.raw, current.mode) != (raw, mode):
                    raise ScaffoldSecurityError(f"{profile_name} changed before layout publication")
            self._check(lock_name)
            lock_before = self.inputs[lock_name]
            if lock_before is None:
                raise ScaffoldSecurityError(f"{lock_name} has no original layout state")
            _replace(self.target, lock_name, *self.outputs[lock_name], lock_before)
        if not self._check(lock_name):
            raise ScaffoldSecurityError(f"{lock_name} was not published")
        for name, destination in self.retire.items():
            raw, mode = self.outputs[destination]
            output = read_state(self.target, destination, publisher=self._publisher(destination))
            if output is None or (output.raw, output.mode) != (raw, mode):
                raise ScaffoldSecurityError(f"{destination} changed before retirement")
            state = self.inputs[name]
            if state is None or not _remove_unchanged_file(
                    self.target / name, self.target, state.raw,
                    expected_identity=(*state.identity, state.mode), durable=True):
                raise ScaffoldSecurityError(f"{name} changed before retirement")
        self._check(lock_name)
        receipt = _read_private(self.target, RECEIPT)
        if receipt is None or receipt.raw != raw_receipt:
            raise ScaffoldSecurityError("the layout receipt changed before completion")
        journal = self.target / JOURNAL
        complete = journal.with_name(f"layout-complete-{secrets.token_hex(8)}")
        _assert_safe_write(journal, self.target)
        _assert_safe_write(complete, self.target)
        os.rename(journal, complete)
        _sync_dir(journal.parent)
        # The fixed journal name is now free for a new stage. If the process
        # stops during cleanup, ordinary restaging removes the retired copy.
        shutil.rmtree(complete, ignore_errors=True)


def load_receipt(target: Path, digest: str) -> tuple[bytes, dict]:
    live = _read_private(target, RECEIPT)
    if (not _HEX.fullmatch(digest) or live is None
            or _sha256_hex(live.raw) != digest):
        raise ScaffoldSecurityError("the staged layout receipt does not match --migration-receipt")
    try:
        value = json.loads(live.raw)
        if not isinstance(value, dict) or value["schema"] != 1 or not isinstance(value["source"], dict):
            raise ValueError("wrong receipt schema")
        return live.raw, value
    except (KeyError, ValueError) as exc:
        raise ScaffoldSecurityError("the staged layout receipt is malformed") from exc
