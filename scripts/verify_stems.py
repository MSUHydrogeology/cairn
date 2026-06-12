#!/usr/bin/env python3
"""Verify proposal/plan filename stems cited in coordination files.

The Cairn ``AGENTS.md`` > "Shared communication files" convention requires
``PLANNING.md`` and ``NEXT_SESSION.md`` (and any adopter-added coordination
files) to refer to proposals and plans by **filename stem, in backticks**
(e.g. ``2026-05-15-author-slug``) rather than by relative-path link -- a
stem is invariant across the ``dev/proposals/`` -> ``dev/proposals/archive/``
move, so an archive move needs no edit to those two files.  The cost:
``link_check`` no longer covers those references, so a typo'd or stale stem
would go unnoticed.  This is the stem-resolution check that fills the gap.

Every backticked date-prefixed stem (``YYYY-MM-DD-<author>-<slug>``) in the
scanned files must resolve to one work item under ``dev/proposals/`` or
``dev/plans/`` -- searched recursively, so live and archived files both count.
Zero matches = a typo or a missing file.  A stem's proposal and its
implementing plan share the stem, so one proposal **plus** one plan is the
normal accepted-and-in-flight state and resolves cleanly; only more than one
*proposal* or more than one *plan* is a genuine ambiguity.

Commit hashes and issue ids do not carry the ``YYYY-MM-DD-`` date prefix, so
the grammar excludes them without a special case.

A backticked date-stem that is deliberately *not* an artifact of this repo --
e.g. an accepted proposal in a sibling repository -- is exempted by an
HTML-comment directive placed anywhere in the same file::

    <!-- verify-stems-ignore: <stem> -- <reason> -->

This is the "tokens explicitly marked non-artifact" exception.

Usage::

    python scripts/verify_stems.py            # exit 0 clean, 1 on issues
    python scripts/verify_stems.py --verbose  # also print each resolved stem
    python scripts/verify_stems.py --scan dev/PLANNING.md dev/MYFILE.md
    python scripts/verify_stems.py --root /path/to/repo

The scaffold installs this script as ``scripts/verify_stems.py`` when the
``claim-check`` module is selected (default-on).  It is the stem-resolution
complement to ``claim_check.py`` (repo-path/line-bounds) and ``link_check.py``
(markdown links): together they form a full lifecycle-hygiene gate.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# A backticked date-prefixed stem: `YYYY-MM-DD-<author>-<slug>`.  The
# closing backtick must follow the stem directly, so a backticked
# *path* (`dev/proposals/<stem>.md`) does not match -- those are
# link_check's job.
STEM_RE = re.compile(r"`(\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)+)`")

# An HTML-comment directive exempting a non-artifact stem; the first
# whitespace-delimited token after the colon is the exempted stem.
IGNORE_RE = re.compile(r"<!--\s*verify-stems-ignore:\s*(\S+)")

# Default files to scan when no --scan argument is provided.
# Adopters may override via --scan to add project-specific coordination files.
_DEFAULT_SCANNED: tuple[Path, ...] = (
    Path("dev") / "PLANNING.md",
    Path("dev") / "NEXT_SESSION.md",
)

# Roots a stem may resolve under (rglob covers the archive/ subdirs).
STEM_ROOTS: tuple[Path, ...] = (
    Path("dev") / "proposals",
    Path("dev") / "plans",
)


def extract_stems(text: str) -> set[str]:
    """All backticked date-prefixed stems appearing in *text*."""
    return set(STEM_RE.findall(text))


def ignored_stems(text: str) -> set[str]:
    """Stems exempted by a ``verify-stems-ignore`` directive in *text*."""
    return set(IGNORE_RE.findall(text))


def resolve_stem(stem: str, repo_root: Path) -> list[Path]:
    """Files under the proposal/plan trees whose name carries *stem*."""
    matches: list[Path] = []
    for root in STEM_ROOTS:
        base = repo_root / root
        if base.is_dir():
            matches.extend(sorted(base.rglob(f"*{stem}*")))
    return matches


def check_stems(
    repo_root: Path,
    *,
    scanned: tuple[Path, ...] | None = None,
    verbose: bool = False,
) -> list[str]:
    """Return a list of stem-resolution issues across the scanned files.

    *scanned* is the set of repo-relative paths to scan for date-stems.
    When ``None``, the default set (``PLANNING.md`` + ``NEXT_SESSION.md``)
    is used.  Adopters may supply additional coordination files here or via
    the ``--scan`` CLI option.
    """
    if scanned is None:
        scanned = _DEFAULT_SCANNED
    issues: list[str] = []
    for rel in scanned:
        src = repo_root / rel
        if not src.is_file():
            issues.append(f"{rel}: file not found")
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        exempt = ignored_stems(text)
        prop_root = repo_root / "dev" / "proposals"
        plan_root = repo_root / "dev" / "plans"
        for stem in sorted(extract_stems(text)):
            if stem in exempt:
                if verbose:
                    print(f"IGNORED  {rel}: `{stem}` (marked non-artifact)")
                continue
            matches = resolve_stem(stem, repo_root)
            props = [m for m in matches if prop_root in m.parents]
            plans = [m for m in matches if plan_root in m.parents]
            if not matches:
                issues.append(
                    f"{rel}: stem `{stem}` resolves to no file under "
                    "dev/proposals/ or dev/plans/"
                )
            elif len(props) <= 1 and len(plans) <= 1:
                # A stem names one work item: its proposal and/or its
                # implementing plan (each possibly live or archived).  One
                # proposal + one plan is the normal accepted-proposal-archived
                # + plan-in-flight state -- not an ambiguity (pair-tolerance fix).
                if verbose:
                    shown = ", ".join(
                        str(m.relative_to(repo_root)) for m in matches
                    )
                    print(f"OK  {rel}: `{stem}` -> {shown}")
            else:
                shown = ", ".join(
                    str(m.relative_to(repo_root)) for m in matches
                )
                issues.append(
                    f"{rel}: stem `{stem}` is ambiguous -- "
                    f"{len(props)} proposal(s) + {len(plans)} plan(s): {shown}"
                )
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify proposal/plan stems cited in coordination files resolve "
            "to exactly one work item.  A stem names one proposal (optionally "
            "plus its implementing plan) -- any other count is an error."
        )
    )
    parser.add_argument(
        "--verbose", action="store_true", help="print each resolved stem"
    )
    parser.add_argument(
        "--root", default=None,
        help="repo root (default: parent of scripts/ directory)",
    )
    parser.add_argument(
        "--scan", nargs="+", metavar="FILE",
        help=(
            "coordination files to scan for stems (repo-relative paths; "
            f"default: dev/PLANNING.md dev/NEXT_SESSION.md)"
        ),
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.root or Path(__file__).resolve().parent.parent)

    if args.scan:
        scanned: tuple[Path, ...] = tuple(Path(f) for f in args.scan)
    else:
        scanned = _DEFAULT_SCANNED

    issues = check_stems(repo_root, scanned=scanned, verbose=args.verbose)

    if issues:
        print("Stem-resolution issues:", file=sys.stderr)
        for issue in issues:
            print(f"  {issue}", file=sys.stderr)
        print(f"\n{len(issues)} issue(s) found.", file=sys.stderr)
        return 1

    scanned_names = ", ".join(str(f) for f in scanned)
    print(
        f"verify_stems: OK -- all stems in [{scanned_names}] resolve."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
