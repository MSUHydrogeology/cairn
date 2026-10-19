"""Scaffold engine — containment leaf.

The Layer-4 executable hardening for adopter-tree writes: the single
``ScaffoldSecurityError`` identity and the two containment guards
(``_assert_safe_write`` for ordinary writes, ``_assert_fanout_contained`` for the
skills fan-out). This is a **leaf** — it imports only the stdlib; install /
upgrade / fan-out depend on it, never the reverse. Every adopter-tree write in
the engine routes its destination through one of these guards before touching
disk (see the SR6 mutation inventory, ``SECURITY_MUTATIONS.md``).

Pure motion from the pre-split monolith (Stage 1): the symbols are unchanged;
only their home moved. Loaded via the engine's verifying finder, so this file's
real path is confirmed within the Cairn root before it executes.
"""
from __future__ import annotations

import os
import secrets
import stat
from pathlib import Path


class ScaffoldSecurityError(Exception):
    """Raised when an install would write through a symlink or escape the
    target directory (Layer-4 executable hardening).  Fail-closed: the
    scaffold refuses the write rather than following the redirect."""


def _read_regular_bytes(path: Path, *, single_link: bool = False) -> bytes | None:
    """Read one regular-file descriptor, never a link or blocking special file."""
    if path.is_symlink():
        raise ScaffoldSecurityError("refusing to read a non-regular file")
    flags = os.O_RDONLY
    for name in ("O_NOFOLLOW", "O_NONBLOCK", "O_NOCTTY", "O_BINARY"):
        flags |= getattr(os, name, 0)
    try:
        fd = os.open(path, flags)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise ScaffoldSecurityError("refusing to read a non-regular file") from exc
    try:
        mode = os.fstat(fd)
        if not stat.S_ISREG(mode.st_mode) or (single_link and mode.st_nlink != 1):
            raise ScaffoldSecurityError("refusing to read a non-regular file")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            return stream.read()
    except OSError as exc:
        raise ScaffoldSecurityError("refusing to read a non-regular file") from exc
    finally:
        os.close(fd)


def _stage_exclusive(path: Path, data: bytes, target: Path) -> Path:
    """Stage bytes beside a guarded destination without opening an existing name."""
    _assert_safe_write(path, target)
    tmp = path.with_name(path.name + "." + secrets.token_hex(8) + ".tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    for name in ("O_NOFOLLOW", "O_BINARY"):
        flags |= getattr(os, name, 0)
    fd = os.open(tmp, flags, 0o666)
    created = os.fstat(fd)
    try:
        with os.fdopen(fd, "wb", closefd=False) as stream:
            stream.write(data)
            stream.flush()
        try:
            old = path.stat(follow_symlinks=False)
        except FileNotFoundError:
            old = None
        if old is not None and stat.S_ISREG(old.st_mode) and hasattr(os, "fchmod"):
            os.fchmod(fd, stat.S_IMODE(old.st_mode) & 0o666)
        _assert_safe_write(tmp, target)
        current = tmp.stat(follow_symlinks=False)
        if (current.st_dev, current.st_ino) != (created.st_dev, created.st_ino):
            raise ScaffoldSecurityError("staged file changed during write")
        return tmp
    except BaseException:
        try:
            current = tmp.stat(follow_symlinks=False)
            if (current.st_dev, current.st_ino) == (created.st_dev, created.st_ino):
                tmp.unlink()
        except FileNotFoundError:
            pass
        raise
    finally:
        os.close(fd)


def _write_by_replacing(path: Path, data: bytes, target: Path) -> None:
    """Atomically replace a guarded destination with exclusive staged bytes."""
    tmp = _stage_exclusive(path, data, target)
    staged = tmp.stat(follow_symlinks=False)
    try:
        _assert_safe_write(path, target)
        current = tmp.stat(follow_symlinks=False)
        if (current.st_dev, current.st_ino) != (staged.st_dev, staged.st_ino):
            raise ScaffoldSecurityError("staged file changed before replacement")
        os.replace(tmp, path)
    except BaseException:
        try:
            current = tmp.stat(follow_symlinks=False)
            if (current.st_dev, current.st_ino) == (staged.st_dev, staged.st_ino):
                tmp.unlink()
        except FileNotFoundError:
            pass
        raise


def _assert_safe_write(dst: Path, target: Path) -> None:
    """Refuse to write through a symlink or outside *target* (Layer 4).

    Runs before **every** write (fresh or ``--force``), not only
    overwrites: ``Path.exists()`` follows symlinks and returns ``False``
    for a *dangling* symlink, so a guard scoped to the ``--force`` path
    would let a fresh install write through a planted symlink at ``dst``
    -- or through a **symlinked parent directory** -- and escape
    ``target``.  Three fail-closed checks:

    1. ``dst`` itself must not be a symlink.
    2. No existing directory **between** ``target`` and ``dst`` may be a
       symlink (a symlinked parent redirects the write even when ``dst``
       is a normal name).
    3. The resolved final write path must stay within ``target`` (defense
       in depth against an ``..`` / absolute ``dst``).

    ``target`` is already ``resolve()``-d by the caller.  The containment
    check is 3.8-safe (``try: relative_to; except ValueError``) -- it does
    **not** use ``Path.is_relative_to`` (3.9+).
    """
    target_resolved = target.resolve()

    # (1) dst must not itself be a symlink.
    if dst.is_symlink():
        raise ScaffoldSecurityError(
            f"refusing to write through a symlinked destination: {dst}"
        )

    # (2) no existing ancestor strictly inside target may be a symlink.
    for ancestor in dst.parents:
        if ancestor == target_resolved:
            break  # reached target itself; don't police above it
        try:
            ancestor.relative_to(target_resolved)
        except ValueError:
            break  # ancestor is at/above target -- stop walking
        if ancestor.is_symlink():
            raise ScaffoldSecurityError(
                f"refusing to write through a symlinked parent: {ancestor}"
            )

    # (3) the resolved final path must stay within target.
    final = dst.parent.resolve() / dst.name
    try:
        final.relative_to(target_resolved)
    except ValueError:
        raise ScaffoldSecurityError(
            f"refusing to write outside the target directory: {final} "
            f"is not under {target_resolved}"
        )


def _assert_fanout_contained(dst: Path, target: Path) -> None:
    """Containment for a fan-out destination.

    Like :func:`_assert_safe_write` but permits ``dst`` *itself* to be a symlink
    (the symlink we are about to (re)create): it still refuses a **symlinked
    parent** and any path resolving **outside** *target*."""
    tr = target.resolve()
    for ancestor in dst.parents:
        if ancestor == tr:
            break
        try:
            ancestor.relative_to(tr)
        except ValueError:
            break
        if ancestor.is_symlink():
            raise ScaffoldSecurityError(
                f"refusing fan-out through a symlinked parent: {ancestor}"
            )
    final = dst.parent.resolve() / dst.name
    try:
        final.relative_to(tr)
    except ValueError:
        raise ScaffoldSecurityError(
            f"refusing fan-out outside the target directory: {final}"
        )
