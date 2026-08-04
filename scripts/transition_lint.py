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

**Suppression is two layers, and the third pre-registered layer is
deliberately not shipped.**  The two that exist: the trigger-root
narrowing below, and the commit-SHA whitelist in
``transition_lint_whitelist.py``.  The one that does not: a *class-level
info downgrade*.  It was dropped on the argument that the measured
false-positive rate was 0 across the corpus the tool was pinned against,
so a class-level suppressor would be machinery for a failure that had
never occurred.  **That argument no longer holds, and this comment exists
so the unmet pre-registration cannot go quiet**: six distinct
false-positive shapes in shape (a), plus a seventh in shape (b), appeared
within twelve days of that measurement.  The layer is still not shipped,
because a class-level downgrade lets a bad shape be *absorbed* rather
than surfaced -- the wrong direction for a tool whose whole value is
honesty about the record.  The honest replacement is the one the accepted
proposal already named: a recurring false-positive shape is evidence the
heuristics are wrong, and should surface as a proposal.

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

import importlib.util as _importlib_util

_HERE = Path(__file__).resolve().parent
_CAIRN_ROOT = _HERE.parent

# Loaded by file path -- as ``scripts/quality_gate.py`` loads its own
# whitelist -- so the CLI works from any cwd without a package context.
_whitelist_spec = _importlib_util.spec_from_file_location(
    "_transition_lint_whitelist", _HERE / "transition_lint_whitelist.py",
)
assert _whitelist_spec is not None and _whitelist_spec.loader is not None
_whitelist_mod = _importlib_util.module_from_spec(_whitelist_spec)
_whitelist_spec.loader.exec_module(_whitelist_mod)

#: Full 40-character SHA -> mandatory non-empty rationale.
WHITELIST: dict[str, str] = _whitelist_mod.WHITELIST


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


@dataclass(frozen=True)
class Rules:
    """Which amendments to the originally-pinned heuristics are active.

    **Not a suppression surface and not reachable from the CLI.**  It
    exists so the corpus-regression tier can measure the *shipped* rule
    against the rule as the accepted proposal pinned it, over a real
    rev-range -- rather than over the fixtures the author built to
    demonstrate the amendments.  A property test whose domain is the
    author's own examples is a green light, not a pin.
    """

    #: Match h3 headings as well as h2, **additively** (an h3 never
    #: truncates the enclosing h2).
    h3_spans: bool = True
    #: Classify a heading by kind **exclusively** -- a heading starting
    #: ``Response`` / ``Revised proposal`` / ``Decision`` is that kind and
    #: is never review-kind evidence.
    exclusive_kind: bool = True
    #: Treat ``respond`` as a *response* token so "respond to ... review"
    #: stops reading as a review claim.
    respond_token: bool = True
    #: Require a review-kind section's own heading to carry an ISO
    #: date before its body can read as a *landed* review.
    dated_heading: bool = True


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

#: Unified-diff hunk header.
_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")

#: Claim tokens -> the transition each claims.  Matched
#: **case-insensitively** and the comment says why: ``f4a8308``'s subject
#: is "dev/proposals: add Gemini External **Review** for check_cairn
#: self-host-compat" -- capital R.  A case-sensitive build produces no
#: claim, no finding, and silently inverts the headline result.  Each
#: token is matched with an optional plural ``s`` and a non-word,
#: non-hyphen boundary on both sides, so a slug like
#: ``automated-review-committer`` never claims.  **Leftmost match wins**:
#: at most one claim per subject.
#:
#: ``reject`` and ``supersede`` are **dead tokens in v1** and are left
#: commented out rather than enabled: a reject/supersede Decision is a
#: rename-only commit, which never triggers, so an active token could
#: only add noise.
#:
#: ``opening`` is absent -- 0 occurrences across all 943 commit subjects
#: in history (re-measured 2026-08-04).  ``accept`` is retained pending
#: the Maintainer fence; measured over the same 943 subjects it is the
#: winning leftmost token on exactly 5, all 5 false positives, because
#: every genuine Decision subject also carries the word "Decision".
_CLAIM_TOKENS: tuple[tuple[str, str], ...] = (
    ("review", "review"),
    ("response", "response"),
    ("respond", "response"),
    ("decision", "decision"),
    ("accept", "decision"),
    # ("reject", "decision"),      # dead token in v1
    # ("supersede", "decision"),   # dead token in v1
)

_CLAIM_RES: tuple[tuple[re.Pattern[str], str], ...] = tuple(
    (re.compile(rf"(?<![-\w]){tok}s?(?![-\w])", re.IGNORECASE), kind)
    for tok, kind in _CLAIM_TOKENS
)

#: ``open`` counts only as the first word after an optional ``<tree>: ``
#: subject prefix.  "Open questions" is live Cairn vocabulary
#: (``templates/core/dev/strategy/_template.md``), so an unanchored match
#: would demand an added file from every commit that mentions one.
_OPEN_ANCHOR_RE = re.compile(r"^(?:[\w./ -]+:\s*)?(open)(?![-\w])", re.IGNORECASE)

#: A heading whose title *starts with* one of these words **is** that
#: kind, and is therefore never review-kind evidence.  Without the
#: exclusion, ``## Response -- <author> (to External Security Review)``
#: counts as evidence for a *review* claim -- a false negative bought,
#: not a false positive fixed.  Measured 2026-08-04: 78 h2 headings under
#: the two trigger roots contain "review" without matching the three
#: originally-pinned prefixes, and 52 of the 78 are exactly this shape.
_EXCLUSIVE_PREFIXES: tuple[tuple[str, str], ...] = (
    ("response", "response"),
    ("revised proposal", "revised"),
    ("decision", "decision"),
)

#: The three review-section prefixes the accepted proposal pinned.  Kept
#: because the corpus tier measures the shipped rule against them.
_PINNED_REVIEW_PREFIXES = ("review", "plan review", "code review")

#: Evidence threshold.  Heading-presence is worthless and this was
#: measured: a plan-open seeds a *titled* review section, so the genuine
#: review-append adds zero ``+## Review`` lines
#: (``git show --format= --unified=0 e31625c | grep -c '^+## Review'``
#: -> 0, its single hunk being ``@@ -251,6 +251,166 @@``).  A
#: heading-presence rule flags the honest commit and misses the
#: dishonest one.  Count *body* lines instead.
_MIN_EVIDENCE_LINES = 3

#: A lifecycle file is a shape-(b) candidate only while it is still
#: pre-review.  ``proposed`` alone was the original rule; no plan ever
#: carries it, which made the exact analogue of the 17b7e5c incident
#: undetectable on plans.
_OPEN_STATUSES = ("proposed", "open", "awaiting-plan-review")

#: How far into an added blob ``**Status**:`` is looked for.  Measured
#: 2026-08-04 across every file under both trigger roots including
#: archives: the deepest ``**Status**:`` in a non-template file is line
#: **31**; the two ``_template.md`` files sit at 77 and 123 and are
#: excluded by basename anyway.  60 leaves ~29 lines of headroom, and
#: the bound is stated here rather than inferred.
_HEADER_BOUND = 60

_STATUS_RE = re.compile(r"^\*\*Status\*\*:\s*([A-Za-z][A-Za-z-]*)")

#: Review-grammar markers: what a *landed* review's body contains.
_REVIEW_MARKER_RE = re.compile(r"\[R\d+\]|\[E\d+\]|\*\*Steelman|\*\*Covered\*\*")

#: An attributed, landed review heading carries the date it landed.  This
#: conjunct is what separates a landed review from a *brief* that merely
#: quotes finding-id grammar while telling a future reviewer what to do,
#: and it amends a discriminator the accepted scope reproduces -- so it
#: is fenced to the Maintainer and strikeable in one line.  Measured over
#: 0f1fc68..da2d00e: marker-only gives 3 shape-(b) findings, one of them
#: false (000e480, on a reviewer brief); marker + dated heading gives 2,
#: both the true 17b7e5c pair.  Priced rather than asserted free: of 161
#: pinned-prefix review h2 headings in the tree (2026-08-04), 103 carry a
#: date and 58 do not, and the undated ones are briefs, placeholders and
#: template headings.  The false-negative cost is real -- a baked-in
#: review whose heading omits a date goes unseen.
_ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


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


def _blob_lines(root: Path, sha: str, path: str) -> list[str]:
    """The post-image of *path* at *sha*, as lines.  Empty on any error."""
    rc, out = _git(root, "show", f"{sha}:{path}")
    if rc != 0:
        return []
    return out.decode("utf-8", errors="replace").splitlines()


def _heading_kind(title: str, rules: Rules) -> str | None:
    """The lifecycle kind a heading *is*, or ``None``."""
    low = title.strip().lower()
    if rules.exclusive_kind:
        for prefix, kind in _EXCLUSIVE_PREFIXES:
            if low.startswith(prefix):
                return kind
        return "review" if "review" in low else None
    # The rule as originally pinned: three literal prefixes, nothing else.
    for prefix in _PINNED_REVIEW_PREFIXES:
        if low.startswith(prefix):
            return "review"
    for prefix, kind in _EXCLUSIVE_PREFIXES:
        if low.startswith(prefix):
            return kind
    return None


def _section_spans(
    lines: list[str], kind: str, rules: Rules,
) -> list[tuple[int, int, str]]:
    """``(start_line, end_line, heading)`` for every section of *kind*.

    h2 and h3 headings are matched **additively**: an h2 span still runs
    to the next h2, and an h3 additionally opens its own span running to
    the next h2-or-h3.  An h3 must never *truncate* the enclosing h2 --
    a truncating implementation was measured and it creates 16 new
    shape-(a) findings over one corpus window by pushing evidence out of
    the h2 span it used to sit in.
    """
    heads: list[tuple[int, int, str]] = []  # (level, line_no, title)
    for idx, line in enumerate(lines, start=1):
        if line.startswith("### "):
            if rules.h3_spans:
                heads.append((3, idx, line[4:]))
        elif line.startswith("## "):
            heads.append((2, idx, line[3:]))
    spans: list[tuple[int, int, str]] = []
    total = len(lines)
    for pos, (level, line_no, title) in enumerate(heads):
        if _heading_kind(title, rules) != kind:
            continue
        end = total
        for later_level, later_line, _ in heads[pos + 1:]:
            if level == 2 and later_level != 2:
                continue
            end = later_line - 1
            break
        spans.append((line_no, end, title.strip()))
    return spans


def _added_nonblank_lines(root: Path, sha: str, path: str) -> list[int]:
    """Post-image line numbers of the non-blank lines *added* to *path*.

    Hunk grammar, pinned explicitly: ``@@ -a[,b] +c[,d] @@``.  A missing
    ``,d`` means a count of 1; ``+c,0`` is a pure deletion and
    contributes nothing.  The rename flag matches ``_entries``' -- if the
    two disagree, the evidence and the trigger disagree about what the
    file is.
    """
    rc, out = _git(
        root, "show", "--find-renames=100%", "--format=", "--unified=0",
        sha, "--", path,
    )
    if rc != 0 or not out:
        return []
    added: list[int] = []
    cursor = 0
    for line in out.decode("utf-8", errors="replace").splitlines():
        m = _HUNK_RE.match(line)
        if m:
            cursor = int(m.group(1))
            continue
        if line.startswith("+++"):
            continue
        if line.startswith("+"):
            if line[1:].strip():
                added.append(cursor)
            cursor += 1
    return added


def _claim(subject: str, rules: Rules) -> str | None:
    """The transition *subject* claims, leftmost-wins, or ``None``."""
    best: tuple[int, str] | None = None
    anchor = _OPEN_ANCHOR_RE.match(subject)
    if anchor:
        best = (anchor.start(1), "open")
    for token, (pattern, kind) in zip(
        (t for t, _ in _CLAIM_TOKENS), _CLAIM_RES, strict=True,
    ):
        if token == "respond" and not rules.respond_token:
            continue
        m = pattern.search(subject)
        if m is None:
            continue
        if best is None or m.start() < best[0]:
            best = (m.start(), kind)
    return None if best is None else best[1]


def _shape_a(
    root: Path, sha: str, subject: str, triggers: list[tuple[str, str]],
    rules: Rules,
) -> list[Finding]:
    """The subject claims a transition the diff does not contain."""
    kind = _claim(subject, rules)
    if kind is None:
        return []
    if kind == "open":
        # The one claim whose evidence is structural rather than
        # sectional: an ``A`` entry under a trigger root.
        if any(status == "A" for status, _ in triggers):
            return []
        return [Finding(
            sha, "a", sorted(p for _, p in triggers)[0],
            "subject claims 'open' but the diff adds no lifecycle file",
        )]
    for _, path in triggers:
        lines = _blob_lines(root, sha, path)
        if not lines:
            continue
        spans = _section_spans(lines, kind, rules)
        if not spans:
            continue
        added = _added_nonblank_lines(root, sha, path)
        inside = sum(
            1 for n in added if any(start <= n <= end for start, end, _ in spans)
        )
        if inside >= _MIN_EVIDENCE_LINES:
            return []
    return [Finding(
        sha, "a", sorted(p for _, p in triggers)[0],
        f"subject claims '{kind}' but the diff adds no {kind} section body",
    )]


def _shape_b(
    root: Path, sha: str, triggers: list[tuple[str, str]], rules: Rules,
) -> list[Finding]:
    """An open commit whose added file already carries a real review.

    One ``Finding`` **per baked-in section**, not per commit: the
    incident commit carries two review sections and must produce two.
    """
    findings: list[Finding] = []
    for status, path in triggers:
        if status != "A":
            continue
        lines = _blob_lines(root, sha, path)
        if not lines:
            continue
        declared = None
        for line in lines[:_HEADER_BOUND]:
            m = _STATUS_RE.match(line)
            if m:
                declared = m.group(1).lower()
                break
        if declared not in _OPEN_STATUSES:
            continue
        for start, end, heading in _section_spans(lines, "review", rules):
            if rules.dated_heading and not _ISO_DATE_RE.search(heading):
                continue
            if _REVIEW_MARKER_RE.search("\n".join(lines[start:end])):
                findings.append(Finding(sha, "b", path, heading))
    return findings


# ---------------------------------------------------------------------------
# Scan + CLI
# ---------------------------------------------------------------------------


def scan(
    rev_range: str,
    root: Path,
    whitelist: dict[str, str] | None = None,
    rules: Rules | None = None,
) -> tuple[int, int, list[Finding]]:
    """``(scanned, triggered, findings)`` over *rev_range*."""
    # ``None`` loads the shipped whitelist; an explicit ``{}`` **bypasses**
    # it.  The bypass is what lets the corpus tier assert the incident
    # findings while human-facing runs stay quiet.
    suppressed: dict[str, str] = WHITELIST if whitelist is None else whitelist
    active = rules or Rules()
    scanned = 0
    triggered = 0
    findings: list[Finding] = []
    for sha, subject in _commits(root, rev_range):
        scanned += 1
        trigs = _triggers(_entries(root, sha))
        if not trigs:
            continue
        triggered += 1
        if sha in suppressed:
            continue
        findings.extend(_shape_a(root, sha, subject, trigs, active))
        findings.extend(_shape_b(root, sha, trigs, active))
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
