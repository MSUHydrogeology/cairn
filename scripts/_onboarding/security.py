#!/usr/bin/env python3
"""onboarding-activate engine -- containment / security leaf (onboarding-split B2).

The error taxonomy (``OnboardingError`` / ``OnboardingSecurityError``) plus the
three write / read / glob containment guards. This is the leaf of the
``_onboarding/`` dependency DAG: stdlib-only, no intra-package imports.

Every writer, reader, and globber in the engine routes through one of these
guards, so isolating them here keeps the **single ``OnboardingSecurityError``
identity** (every ``raise`` and ``except`` across the package resolves to one
class) and gives the split a clear, auditable containment surface. The guard
bodies are preserved verbatim from the pre-split single-file helper
(onboarding-split bound contract: containment preserved byte-for-byte and
unweakened; proven by the negative-path tests).
"""
from __future__ import annotations

from pathlib import Path


class OnboardingError(Exception):
    """Raised on a recoverable error the maintainer should fix
    (missing slot, missing metadata, missing source file, etc.).
    The CLI catches + prints a friendly message + exits non-zero."""


class OnboardingSecurityError(OnboardingError):
    """Containment-guard refusal: path escapes the target, passes
    through a symlink, or violates the preset-name character set.

    Inherits ``OnboardingError`` so the CLI's existing catch-all
    surfaces it as a clean user-facing error rather than a raw
    traceback (Antigravity proposal-review P2-2 disposition).  The
    CLI's ``main()`` handler distinguishes this class from generic
    ``OnboardingError`` by returning exit code **2** instead of 1
    (Antigravity plan-review P3-1 disposition), so automation
    wrappers + diagnostics can tell containment failures apart
    from operational ones.
    """


# ---------------------------------------------------------------------------
# Containment guards (Antigravity proposal-review I-3 + P1; plan
# Chunk P1.1).  Ported from ``bootstrap/scaffold.py:_assert_safe_write``
# (the established Cairn pattern).  Three call-shapes:
#
# * ``_assert_safe_write(dst, target)`` -- write-path guard, run
#   immediately before every ``write_text`` / ``os.open`` against
#   a target-derived path.
# * ``_assert_safe_read(src, target)`` -- read-path guard, run
#   immediately before every ``read_text`` / ``read_bytes`` against
#   a target-derived path.
# * ``_assert_safe_dir_for_glob(d, target)`` -- parent-once
#   optimization for glob loops (Antigravity plan-review P2-2):
#   one full three-check on the parent directory + a cheap
#   ``is_symlink()`` per leaf, avoiding per-leaf ``resolve()``
#   overhead on large archives.
#
# All three raise ``OnboardingSecurityError`` (a subclass of
# ``OnboardingError``) so the CLI's existing catch surfaces them
# cleanly.  All are 3.8-safe (``try: relative_to / except
# ValueError`` rather than 3.9+ ``is_relative_to``).
# ---------------------------------------------------------------------------


def _assert_safe_write(dst: Path, target: Path) -> None:
    """Refuse to write through a symlink or outside *target*.

    Three fail-closed checks (mirror ``scaffold.py``'s pattern):

    1. ``dst`` itself must not be a symlink.
    2. No existing directory between ``target`` and ``dst`` may be
       a symlink (a symlinked parent redirects the write even when
       ``dst`` is a normal name).
    3. The resolved final write path must stay within ``target``
       (defense in depth against ``..`` / absolute ``dst``).

    The caller is responsible for ensuring ``dst.parent`` exists
    BEFORE calling (Antigravity plan-review P2-1 disposition:
    ``mkdir → assert`` so ``resolve()`` operates on an existing
    parent rather than a non-existent path).
    """
    target_resolved = target.resolve()

    # (1) dst must not itself be a symlink.
    if dst.is_symlink():
        raise OnboardingSecurityError(
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
            raise OnboardingSecurityError(
                f"refusing to write through a symlinked parent: "
                f"{ancestor}"
            )

    # (3) the resolved final path must stay within target.
    final = dst.parent.resolve() / dst.name
    try:
        final.relative_to(target_resolved)
    except ValueError:
        raise OnboardingSecurityError(
            f"refusing to write outside the target directory: "
            f"{final} is not under {target_resolved}"
        )


def _assert_safe_read(src: Path, target: Path) -> None:
    """Refuse to read through a symlink or outside *target*.

    Read-only variant of ``_assert_safe_write``.  Same three
    checks; raises ``OnboardingSecurityError`` on any violation.
    Called immediately before ``src.read_text`` / ``src.read_bytes``
    against a target-derived path.
    """
    target_resolved = target.resolve()

    # (1) src must not itself be a symlink.
    if src.is_symlink():
        raise OnboardingSecurityError(
            f"refusing to read through a symlinked source: {src}"
        )

    # (2) no existing ancestor strictly inside target may be a symlink.
    for ancestor in src.parents:
        if ancestor == target_resolved:
            break
        try:
            ancestor.relative_to(target_resolved)
        except ValueError:
            break
        if ancestor.is_symlink():
            raise OnboardingSecurityError(
                f"refusing to read through a symlinked parent: "
                f"{ancestor}"
            )

    # (3) the resolved final read path must stay within target.
    final = src.parent.resolve() / src.name
    try:
        final.relative_to(target_resolved)
    except ValueError:
        raise OnboardingSecurityError(
            f"refusing to read outside the target directory: "
            f"{final} is not under {target_resolved}"
        )


def _assert_safe_dir_for_glob(d: Path, target: Path) -> None:
    """Parent-once optimization for glob loops (Antigravity
    plan-review P2-2): validate the glob's parent directory in one
    pass, so the loop body can do only ``f.is_symlink()`` per leaf
    (O(1), no ``resolve()``) and still catch every escape vector
    per-leaf ``_assert_safe_read`` would catch.

    Same three checks as ``_assert_safe_read`` applied to the
    parent directory itself.  The combination
    (parent validated + leaf ``is_symlink()`` check) is
    security-equivalent to per-leaf ``_assert_safe_read`` at much
    lower cost on large archives.
    """
    target_resolved = target.resolve()

    # (1) d must not itself be a symlink.
    if d.is_symlink():
        raise OnboardingSecurityError(
            f"refusing to enter a symlinked glob parent: {d}"
        )

    # (2) no existing ancestor strictly inside target may be a symlink.
    for ancestor in d.parents:
        if ancestor == target_resolved:
            break
        try:
            ancestor.relative_to(target_resolved)
        except ValueError:
            break
        if ancestor.is_symlink():
            raise OnboardingSecurityError(
                f"refusing to enter glob through a symlinked parent: "
                f"{ancestor}"
            )

    # (3) the resolved directory must stay within target.
    final = d.resolve()
    try:
        final.relative_to(target_resolved)
    except ValueError:
        raise OnboardingSecurityError(
            f"refusing glob outside the target directory: "
            f"{final} is not under {target_resolved}"
        )
