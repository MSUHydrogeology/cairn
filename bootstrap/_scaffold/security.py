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


def _remove_unchanged_file(
    path: Path, target: Path, expected: bytes | None, *, _after_walk=None,
) -> bool:
    """Remove *path* only if it is a regular file holding exactly *expected*.

    Returns ``True`` when nothing is left at the name (removed, or already gone),
    ``False`` when the file was kept: its bytes are not *expected*, or it was
    replaced between the read and the removal, or the removal did not happen.
    Raises :class:`ScaffoldSecurityError` for a link at the name or above it, a
    name outside *target*, or anything at the name that is not a regular file.
    The caller clears its record of the file only on ``True``.  With *expected*
    ``None`` nothing is removed: the call only confirms, through the same folder
    handles, that nothing is at the name (``True``) or that something is
    (``False``).

    Where ``os.unlink`` takes ``dir_fd`` (every of ``os.open``, ``os.unlink``,
    ``os.rmdir`` and ``os.stat`` is in ``os.supports_dir_fd``, and the platform
    has ``O_DIRECTORY`` and ``O_NOFOLLOW``), the project folder and each folder
    down to the file are opened one level at a time without following links, and
    the file is read, checked and unlinked *by name through the last folder
    handle*.  A folder swapped for a link after the walk then changes nothing: the
    handles still point at the original folders.  Where those are missing
    (Windows), the same steps run by path, and a folder swapped for a link in that
    window can redirect the removal; ``bootstrap/SAFETY.md`` names that residual.

    After the file goes, its own folder is removed if it is now empty -- that one
    folder, never one above it and never *target* -- through the same handles.
    ``_after_walk`` is called once, after the last handle is open and before the
    file is read; it exists so a test can change the tree at that instant.
    """
    _assert_safe_write(path, target)
    try:
        parts = path.relative_to(target).parts
    except ValueError:
        raise ScaffoldSecurityError(
            "refusing to remove a path outside the target directory") from None
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise ScaffoldSecurityError("refusing to remove a path that is not a plain name")
    not_regular = "refusing to remove a non-regular file"

    read_flags = os.O_RDONLY
    for name in ("O_NOFOLLOW", "O_NONBLOCK", "O_NOCTTY", "O_BINARY", "O_CLOEXEC"):
        read_flags |= getattr(os, name, 0)

    def read_open_file(fd: int) -> tuple[bytes, os.stat_result]:
        try:
            opened = os.fstat(fd)
            if not stat.S_ISREG(opened.st_mode):
                raise ScaffoldSecurityError(not_regular)
            with os.fdopen(fd, "rb", closefd=False) as stream:
                return stream.read(), opened
        except OSError as exc:
            raise ScaffoldSecurityError(not_regular) from exc
        finally:
            os.close(fd)

    can_walk = (
        all(fn in os.supports_dir_fd for fn in (os.open, os.unlink, os.rmdir, os.stat))
        and hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")
    )
    if not can_walk:
        if expected is None:
            return not os.path.lexists(path)
        try:
            fd = os.open(path, read_flags)
        except FileNotFoundError:
            return True
        except OSError as exc:
            raise ScaffoldSecurityError(not_regular) from exc
        data, opened = read_open_file(fd)
        if data != expected:
            return False
        try:
            now = os.lstat(path)
        except FileNotFoundError:
            return True
        if (now.st_dev, now.st_ino) != (opened.st_dev, opened.st_ino):
            return False
        try:
            os.unlink(path)
        except OSError:
            pass
        if os.path.lexists(path):
            return False
        if len(parts) > 1:
            try:
                os.rmdir(path.parent)
            except OSError:
                pass
        return True

    folder_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    handles: list[int] = []
    try:
        try:
            handles.append(os.open(target, folder_flags))
        except OSError as exc:
            raise ScaffoldSecurityError("refusing to open the target directory") from exc
        for folder in parts[:-1]:
            try:
                handles.append(os.open(folder, folder_flags, dir_fd=handles[-1]))
            except FileNotFoundError:
                return True
            except OSError as exc:
                raise ScaffoldSecurityError(
                    "refusing to remove through a link or a file standing as a folder"
                ) from exc
        if _after_walk is not None:
            _after_walk()
        name, folder = parts[-1], handles[-1]
        if expected is None:
            try:
                os.stat(name, dir_fd=folder, follow_symlinks=False)
            except FileNotFoundError:
                return True
            except OSError:
                return False
            return False
        try:
            fd = os.open(name, read_flags, dir_fd=folder)
        except FileNotFoundError:
            return True
        except OSError as exc:
            raise ScaffoldSecurityError(not_regular) from exc
        data, opened = read_open_file(fd)
        if data != expected:
            return False
        try:
            now = os.stat(name, dir_fd=folder, follow_symlinks=False)
        except FileNotFoundError:
            return True
        if (now.st_dev, now.st_ino) != (opened.st_dev, opened.st_ino):
            return False
        try:
            os.unlink(name, dir_fd=folder)
        except OSError:
            pass
        try:
            os.stat(name, dir_fd=folder, follow_symlinks=False)
        except FileNotFoundError:
            pass
        except OSError:
            return False
        else:
            return False
        if len(handles) > 1:
            try:
                os.rmdir(parts[-2], dir_fd=handles[-2])
            except OSError:
                pass
        return True
    finally:
        for handle in handles:
            os.close(handle)
