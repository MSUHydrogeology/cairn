# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Prune the ``dev/reflections/`` session-reflection scratch directory.

Keeps the reflection files whose date falls in the most-recent ``KEEP``
distinct reflection dates and deletes the older ones.

``dev/reflections/`` holds per-agent, untracked, ephemeral session
reflections (see ``dev/reflections/README.md``).  By the time a reflection
date ages out of the window it has been read, dispositioned, and migrated on
its own day's goodnight, so the prune destroys nothing irreplaceable -- but
it IS the repo's one routine *file-deleting* operation (the files are
gitignored, not recoverable from git), so it is a single tested helper with
a strict delete-filter rather than a retyped shell one-liner:

* it deletes **only** files whose name matches the pinned reflection filename
  grammar (``<date>-<HHMMSS>-<agent>-<role>.md``);
* it never touches ``README.md``, directories, symlinks, or any non-matching
  file.

Note: the ``tools/lifecycle.py`` session-end full-handoff path runs its own
simpler date-cutoff reflection prune.  This standalone script is the
*explicit* tool the ``reflections`` module doctrine prescribes -- it gives
a finer keep-by-distinct-date window and can be invoked independently.

Installed at ``tools/prune_reflections.py`` with the ``reflections`` module.
Stdlib-only; no project-specific imports.

Invoked from the goodnight routine or directly::

    python tools/prune_reflections.py             # prune to the window
    python tools/prune_reflections.py --dry-run   # list, delete nothing
    python tools/prune_reflections.py --keep 60   # a wider window
    python tools/prune_reflections.py --dir dev/reflections
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REFLECTIONS_DIR = _REPO_ROOT / 'dev' / 'reflections'
DEFAULT_KEEP = 30

# The pinned reflection filename grammar:
# ``<date>-<HHMMSS>-<agent>-<role>.md``.  Group 1 is the date.  The
# trailing ``[a-z0-9]+(?:-[a-z0-9]+)+`` requires *both* an agent and a role
# field -- two or more hyphen-separated slug segments after the timestamp.
# The filter matches ONLY this grammar -- never README.md, a directory, a
# symlink, or any other file.
_REFLECTION_RE = re.compile(
    r'^(\d{4}-\d{2}-\d{2})-\d{6}-[a-z0-9]+(?:-[a-z0-9]+)+\.md$'
)


def reflection_dates(directory: Path) -> dict[str, list[Path]]:
    """Map each reflection ``<date>`` to its reflection files.

    Only regular files (not symlinks, not directories) whose name matches the
    pinned grammar *and* carries a real calendar date are included --
    ``README.md`` and any other file are skipped, so they can never be
    selected for deletion.
    """
    by_date: dict[str, list[Path]] = {}
    if not directory.is_dir():
        return by_date
    for item in sorted(directory.iterdir()):
        if item.is_symlink() or not item.is_file():
            continue
        match = _REFLECTION_RE.match(item.name)
        if match is None:
            continue
        try:
            datetime.datetime.strptime(match.group(1), '%Y-%m-%d')
        except ValueError:
            continue  # regex-shaped but not a real calendar date
        by_date.setdefault(match.group(1), []).append(item)
    return by_date


def prune_reflections(
    directory: Path,
    *,
    keep: int = DEFAULT_KEEP,
    dry_run: bool = False,
) -> list[Path]:
    """Delete reflection files outside the most-recent *keep* dates.

    A reflection file is removed only when its ``<date>`` is not among the
    *keep* most-recent distinct reflection dates.  Returns the sorted list of
    files actually deleted -- or, with ``dry_run``, the files that *would* be
    deleted.  A doomed file that cannot be unlinked is skipped with a stderr
    note and left out of the returned list, rather than aborting the prune
    mid-loop.

    Raises ``ValueError`` when *keep* is not positive: a non-positive window
    keeps zero dates and would prune *every* reflection, so the helper fails
    closed before any deletion.
    """
    if keep < 1:
        raise ValueError(
            f'keep must be >= 1 (got {keep}); a non-positive window '
            f'would prune every reflection'
        )
    by_date = reflection_dates(directory)
    kept_dates = set(sorted(by_date, reverse=True)[:keep])
    doomed = sorted(
        path
        for date, paths in by_date.items()
        if date not in kept_dates
        for path in paths
    )
    if dry_run:
        return doomed
    deleted: list[Path] = []
    for path in doomed:
        try:
            path.unlink(missing_ok=True)
        except OSError as exc:
            print(
                f'prune_reflections: could not delete {path.name}: {exc}',
                file=sys.stderr,
            )
            continue
        deleted.append(path)
    return deleted


def _positive_int(value: str) -> int:
    """An argparse type accepting only integers >= 1."""
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError(f'must be >= 1 (got {parsed})')
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='prune_reflections',
        description=(
            'Prune dev/reflections/ to the most-recent reflection '
            'dates.  Deletes only files matching the pinned '
            'reflection filename grammar; never README.md.'
        ),
    )
    parser.add_argument(
        '--dir', type=Path, default=DEFAULT_REFLECTIONS_DIR,
        help=f'Reflections directory. Default: {DEFAULT_REFLECTIONS_DIR}.',
    )
    parser.add_argument(
        '--keep', type=_positive_int, default=DEFAULT_KEEP,
        help=f'How many recent reflection dates to keep (>= 1). '
             f'Default: {DEFAULT_KEEP}.',
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='List what would be deleted; delete nothing.',
    )
    args = parser.parse_args(argv)

    deleted = prune_reflections(args.dir, keep=args.keep, dry_run=args.dry_run)
    verb = 'would prune' if args.dry_run else 'pruned'
    print(
        f'prune_reflections: {verb} {len(deleted)} reflection '
        f'file(s) outside the most-recent {args.keep} dates.'
    )
    for path in deleted:
        print(f'  {path.name}')
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
