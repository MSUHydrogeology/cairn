"""Advisory check: does a commit's message match its lifecycle diff?

Flags two shapes over a bounded rev-range: **(a)** a commit subject
claiming a review / response / decision transition whose diff adds no
such section, and **(b)** a proposal- or plan-*open* commit whose added
file already carries a real review.  It enforces an existing rule
(``doctrine/lifecycle.md`` > one commit per lifecycle transition) rather
than creating one.

**Advisory forever.**  :func:`main` returns ``0`` on any completed scan --
with findings or without.  ``2`` is reserved for a *usage* error (a
missing, malformed, or unresolvable rev-range).  It never returns ``1``,
and nothing here may be wired to a gate.  A finding is a printed line a
human reads, not a build failure.

**Not installed into adopter trees.**  ``scripts/`` as a *directory* is a
shipped destination namespace -- ``python bootstrap/scaffold.py
--manifest`` carries 24 ``scripts/``-destination rows (measured
2026-08-04), including three of the reference checkers Cairn ships
adopters (``claim_check.py``, ``link_check.py``, ``content_scan.py``).
*This file* is repo-local for a checkable reason: it has **no row in the
install manifest** (0 rows match ``transition_lint``).  The heuristics
below are pinned against Cairn's own commit-subject conventions and would
not generalise unchanged to another tree.

**Two postures toward git errors, deliberately different.**

* *Fail-fast on inputs.*  A rev-range that does not parse, or that parses
  but does not resolve, exits ``2`` with a message on stderr.  A range
  that scans nothing and reports "clean" is worse than no tool.
* *Degrade-quiet on per-commit enumeration.*  If ``git diff-tree`` errors
  on one commit, that commit yields an empty entry list and the commit is
  passed over -- one unreadable commit must not abort a 900-commit scan.

**Exemption model.**  There is none in this tool, by construction.  No
exception keyword, no in-message opt-out directive, no new obligation on
a contributor.  The only thing that keeps the legitimate no-approval
commit shapes quiet is the *narrowing*: a commit is examined only when it
adds or modifies a file under ``dev/proposals/`` or ``dev/plans/``.  The
source of truth for which lifecycle commits legitimately bundle other
files is ``doctrine/proposals.md`` > "File moves"; this tool restates it
and adds nothing to it.

Stdlib only.  Two public entry points: :func:`main` and :func:`scan`.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_CAIRN_ROOT = _HERE.parent


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Finding:
    """One advisory finding.

    Four fields and **no severity field**.  Contrast
    ``scripts/quality_gate.py``'s ``Finding`` (which carries one), its
    ``failed`` property, and its ``return 1 if report.failed else 0``.
    The absent field is *not* the pin -- a later edit could add one.  The
    pin is the test that :func:`main` returns 0 on a repo *with*
    findings.
    """

    sha: str
    shape: str
    file: str
    message: str


#: The narrowing.  A commit is examined only if it adds or modifies a
#: file under one of these roots.  This -- not a keyword -- is what keeps
#: the ``dev/strategy/`` and goodnight-handoff carve-in shapes quiet.
_TRIGGER_ROOTS = ("dev/proposals/", "dev/plans/")

#: Archive destinations are excluded.  ``doctrine/proposals.md`` >
#: "File moves" blesses the plan-open archive bundle and the
#: reject/supersede archive bundle; a file arriving under ``archive/`` is
#: a move, never an authored transition.
_EXCLUDE_SUBSTRING = "/archive/"

#: Lifecycle templates carry every heading as placeholder text.
_EXCLUDE_BASENAME = "_template.md"

#: Deliberately narrow -- ref characters plus the ``..`` / ``...`` range
#: operators only, so a range can never carry a shell metacharacter or a
#: path traversal.  git itself runs ``shell=False`` regardless; this is
#: defence in depth.  Re-implemented from ``scripts/measurements.py``.
_REV_RANGE_RE = re.compile(r"^[0-9A-Za-z._/~^-]+\.\.\.?[0-9A-Za-z._/~^-]+$")


# ---------------------------------------------------------------------------
# git plumbing
# ---------------------------------------------------------------------------


def _git(root: Path, *args: str) -> tuple[int, bytes]:
    """Run git with a fixed argument vector, ``shell=False``."""
    try:
        out = subprocess.run(
            ["git", *args], cwd=str(root), capture_output=True, check=False,
        )
    except OSError:
        return 1, b""
    return out.returncode, out.stdout


def _validate_range(rev_range: str, root: Path) -> str | None:
    """``None`` if *rev_range* parses **and** both endpoints resolve.

    The second half is the point: a range that parses but names a commit
    that is not in this repository must not exit 0 with no output.
    """
    if not _REV_RANGE_RE.match(rev_range):
        return f"transition_lint: not a rev-range: {rev_range!r}"
    body = rev_range.replace("...", "..", 1) if "..." in rev_range else rev_range
    left, _, right = body.partition("..")
    for endpoint in (left, right):
        if not endpoint:
            return f"transition_lint: empty rev-range endpoint in {rev_range!r}"
        rc, _ = _git(
            root, "rev-parse", "--verify", "--quiet", endpoint + "^{commit}",
        )
        if rc != 0:
            return f"transition_lint: rev-range endpoint does not resolve: {endpoint}"
    return None


def _commits(root: Path, rev_range: str) -> list[tuple[str, str]]:
    """``(sha, subject)`` newest-first over *rev_range*.

    Only the subject is read.  Commit bodies and ``git notes`` are out of
    scope, so there is nowhere to write an in-message opt-out.
    """
    rc, out = _git(root, "log", "--format=%H%x1f%s", rev_range)
    if rc != 0 or not out:
        return []
    rows: list[tuple[str, str]] = []
    for line in out.decode("utf-8", errors="replace").splitlines():
        sha, sep, subject = line.partition("\x1f")
        if sep:
            rows.append((sha, subject))
    return rows


def _entries(root: Path, sha: str) -> list[tuple[str, str]]:
    """``(status, path)`` for one commit, rename-aware.

    Degrade-quiet: any git error yields ``[]`` and the commit is passed
    over.  The ``-z`` token walk is **copied and re-implemented** from
    the intent-module conflict helper rather than imported -- that
    function runs a staged-index diff, takes no rev-range, and discards
    every non-``R`` entry, so it cannot enumerate an A/M set, and
    importing it would couple a repo-local script to a byte-frozen
    shipped file.

    ``--find-renames=100%`` rather than ``-M``: a bare ``-M`` can absorb
    a genuine ``A`` under a trigger root into a rename pair and silently
    un-trigger the commit.  Measured across 898 commits of history the
    two flags produce identical trigger sets, so this is a prophylactic
    with no observed benefit on this corpus -- kept because the hazard is
    real in principle and the stricter flag costs nothing.
    """
    rc, out = _git(
        root, "diff-tree", "--no-commit-id", "--name-status",
        "--find-renames=100%", "-r", "-z", sha,
    )
    if rc != 0 or not out:
        return []
    tokens = out.split(b"\x00")
    if tokens and tokens[-1] == b"":
        tokens = tokens[:-1]
    entries: list[tuple[str, str]] = []
    i = 0
    while i < len(tokens):
        status = tokens[i].decode("utf-8", errors="replace")
        if status[:1] == "R":
            # name-status -z renames: ``R<score>\0<source>\0<dest>``.
            if i + 2 < len(tokens):
                entries.append(
                    (status, tokens[i + 2].decode("utf-8", errors="replace"))
                )
            i += 3
        else:
            # ``<status>\0<path>`` for A / M / D / T.
            if i + 1 < len(tokens):
                entries.append(
                    (status, tokens[i + 1].decode("utf-8", errors="replace"))
                )
            i += 2
    return entries


def _in_scope(path: str) -> bool:
    if not path.startswith(_TRIGGER_ROOTS):
        return False
    if _EXCLUDE_SUBSTRING in path:
        return False
    return not path.endswith("/" + _EXCLUDE_BASENAME)


def _triggers(entries: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """The in-scope ``A``/``M`` entries.  A rename is never a trigger."""
    return [
        (status, path) for status, path in entries
        if status in ("A", "M") and _in_scope(path)
    ]


# ---------------------------------------------------------------------------
# Scan + CLI
# ---------------------------------------------------------------------------


def scan(
    rev_range: str,
    root: Path,
    whitelist: dict[str, str] | None = None,
) -> tuple[int, int, list[Finding]]:
    """``(scanned, triggered, findings)`` over *rev_range*."""
    suppressed: dict[str, str] = {} if whitelist is None else whitelist
    scanned = 0
    triggered = 0
    findings: list[Finding] = []
    for sha, _subject in _commits(root, rev_range):
        scanned += 1
        trigs = _triggers(_entries(root, sha))
        if not trigs:
            continue
        triggered += 1
        if sha in suppressed:
            continue
    return scanned, triggered, findings


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="transition_lint",
        description="Advisory: does a commit's message match its lifecycle diff?",
    )
    parser.add_argument(
        "rev_range",
        help="required, e.g. d6646a3..57d1daf -- there is no default, because "
             "a HEAD-relative default is a window that moves under the reader",
    )
    parser.add_argument("--root", type=Path, default=_CAIRN_ROOT)
    parser.add_argument(
        "--report", action="store_true",
        help="machine mode: TAB-separated sha/shape/file/message",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    root: Path = args.root
    if not (root / ".git").exists():
        print(
            f"transition_lint: --root is not a git work tree: {root}",
            file=sys.stderr,
        )
        return 2
    problem = _validate_range(args.rev_range, root)
    if problem is not None:
        print(problem, file=sys.stderr)
        return 2
    scanned, triggered, findings = scan(args.rev_range, root)
    if args.report:
        for f in findings:
            print(f"{f.sha}\t{f.shape}\t{f.file}\t{f.message}")
    # The census prints on every run, including a clean one: a
    # zero-finding run must be positive evidence, not silence.
    print(
        f"scanned {scanned} commits, {triggered} triggered, "
        f"{len(findings)} findings"
    )
    if not args.report:
        for f in findings:
            print(f"  {f.sha[:7]}  shape ({f.shape})  {f.file}: {f.message}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
