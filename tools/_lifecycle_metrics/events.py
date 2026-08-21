# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""The ``cairn-event-v1`` grammar: closed-schema HTML-comment blocks a
lifecycle-artifact edit appends alongside the act it records (a status
transition, a review pass, a Response), read back by the history-diff
algorithm this module also carries.

This module is the ``metrics-events-not-prose`` Part 3 replacement for
prose-parsing the retained event-shaped fields (``review_rounds``,
reviewer identity/tier, ``response_models``, the stage-timing columns):
instead of scraping section headings and regex-matched fields out of
file text, the same edit that performs a lifecycle act appends a small,
closed-vocabulary block declaring what it just did, and the extractor
reads those blocks back rather than re-deriving the act from prose.

Three block shapes, reproduced verbatim from the accepted proposal's
Round 7 §1 as the binding contract this module pins:

    <!-- cairn-event-v1
    kind: transition
    from_state: reviewed
    to_state: revised
    -->

    <!-- cairn-event-v1
    kind: review-pass
    tier: External
    reviewer: <reviewer name as written in the section heading>
    -->

    <!-- cairn-event-v1
    kind: response
    model: <model identity as written in the Response's **Model** field>
    -->

**No import of ``.extract``.**  ``extract.py`` imports THIS module for
reconciliation (wiring the retained fields to reconciled blocks); a
loader call the other direction would be circular.  Every function here
that needs the runtime status vocabulary (the ``from_state``/``to_state``
bound) takes it as an explicit ``valid_states`` parameter instead of
loading it itself -- the caller (``extract.py``, which already owns the
contained vocabulary loader) supplies it.
"""
from __future__ import annotations

import re
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

from .parse import _header_field, _CODE_REVIEW_HEADING_RE, _PLAN_REVIEW_HEADING_RE


# --------------------------------------------------------------- grammar


#: The literal version token, as it appears in the fence (``<!--
#: cairn-event-v1``).  Any other token after ``cairn-event-`` is a
#: recognized-but-unsupported fence and refuses (never silently ignored
#: -- an adopter who upgrades to a v2 grammar someday must not have
#: their v2 blocks silently vanish from a v1-only reader).
VERSION_TOKEN = "cairn-event-v1"

#: The suffix ``_FENCE_RE`` captures after the shared ``cairn-event-``
#: prefix -- compared against directly so the prefix is not double-
#: counted (``VERSION_TOKEN`` names the whole fence word for messages
#: and docs; this is the bare suffix the regex group actually yields).
_VERSION_SUFFIX = "v1"

#: The three event kinds the closed grammar admits.
KIND_TRANSITION = "transition"
KIND_REVIEW_PASS = "review-pass"
KIND_RESPONSE = "response"
VALID_KINDS: Tuple[str, ...] = (KIND_TRANSITION, KIND_REVIEW_PASS, KIND_RESPONSE)

#: Required keys per kind, beyond the universal ``kind`` itself.
_REQUIRED_KEYS: Dict[str, Tuple[str, ...]] = {
    KIND_TRANSITION: ("from_state", "to_state"),
    KIND_REVIEW_PASS: ("tier", "reviewer"),
    KIND_RESPONSE: ("model",),
}

#: Every key a given kind admits -- ``kind`` and the optional
#: ``recorded_by`` are legal on all three; anything else is scoped to
#: its own kind.  An unknown key refuses rather than being silently
#: dropped.
_ALLOWED_KEYS: Dict[str, frozenset] = {
    kind: frozenset({"kind", "recorded_by"}) | frozenset(_REQUIRED_KEYS[kind])
    for kind in VALID_KINDS
}

#: ``tier``'s closed bound (``review-pass`` only).
VALID_TIERS: Tuple[str, ...] = ("Internal", "External", "Security", "Code")

#: ``reviewer`` / ``model`` / ``recorded_by`` share one bound: at most
#: 120 characters, single line (already guaranteed by the line-based
#: parser below -- a value can never itself contain a newline).
_MAX_FIELD_LEN = 120

#: One ``key: value`` body line.  The key is a bare identifier; the value
#: is everything after the first ``:`` on the line, stripped.
_FIELD_LINE_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$')

#: The fence itself: an HTML comment opening with ``cairn-event-<token>``.
#: Captures the version token and the body between the opening line and
#: the closing ``-->``, across the whole document (``re.DOTALL``).
_FENCE_RE = re.compile(
    r'<!--\s*cairn-event-(?P<version>\S+)\s*\n(?P<body>.*?)-->',
    re.DOTALL,
)


class EventGrammarError(ValueError):
    """A ``cairn-event-*`` fence exists but fails to validate the closed
    grammar above.  Raised rather than returned so a caller cannot
    accidentally treat a partially-parsed, invalid block as clean data --
    refuses, never ignores, never defaults, per Round 7 §1's own text."""


@dataclass(frozen=True)
class EventBlock:
    """One validated ``cairn-event-v1`` block.

    ``fields`` carries every key present in the block (including
    ``kind`` itself and ``recorded_by`` when present), already bounds-
    checked.  ``raw`` is the exact verbatim text of the block, from the
    opening ``<!--`` through the closing ``-->`` -- used by the history
    reader (below / Chunk 5) for byte-exact mutation detection: a block
    edited in ANY way, including whitespace, no longer compares equal to
    its earlier self, which is the maximally sensitive reading of "an
    existing block was mutated" from Round 7 §2 step 2."""

    kind: str
    fields: Mapping[str, str] = field(default_factory=dict)
    raw: str = ""

    @property
    def from_state(self) -> str:
        return self.fields.get("from_state", "")

    @property
    def to_state(self) -> str:
        return self.fields.get("to_state", "")

    @property
    def tier(self) -> str:
        return self.fields.get("tier", "")

    @property
    def reviewer(self) -> str:
        return self.fields.get("reviewer", "")

    @property
    def model(self) -> str:
        return self.fields.get("model", "")

    @property
    def recorded_by(self) -> str:
        """Informational only -- explicitly barred from authority,
        identity, and idempotency (Round 7's closed key table)."""
        return self.fields.get("recorded_by", "")


def _line_of(text: str, offset: int) -> int:
    """1-indexed line number of ``offset`` within ``text`` -- for
    refusal messages a human can act on without re-deriving it."""
    return text.count("\n", 0, offset) + 1


_MARKDOWN_CODE_FENCE_RE = re.compile(r'^(`{3,}|~{3,})')


def _blank_fenced_code_blocks(text: str) -> str:
    """Blank the CONTENTS of every triple-backtick/tilde fenced markdown
    code block, preserving line count and every non-blanked line
    verbatim (so byte offsets within a KEPT line, and line numbers
    throughout, stay accurate against the original text).

    Doctrine and plan prose routinely reproduces the grammar's own
    worked examples verbatim inside a fenced code block -- this very
    plan's Chunk 4 does exactly that, quoting Round 7's three examples --
    and a raw-text scan cannot otherwise tell that apart from a real,
    committed event block.  Discovered empirically running the real
    extractor against this repository's own corpus during Chunk 6's
    implementation (`AGENTS.md` > "Verifying claims"): the plan's own
    illustrative examples crashed a real corpus walk with a spurious
    'reviewed' is not a declared lifecycle status refusal before this
    fix existed."""
    lines = text.split("\n")
    out: List[str] = []
    fence_marker: Optional[str] = None
    for line in lines:
        stripped = line.strip()
        if fence_marker is None:
            m = _MARKDOWN_CODE_FENCE_RE.match(stripped)
            if m:
                fence_marker = m.group(1)[0] * len(m.group(1))
                out.append(line)
                continue
            out.append(line)
        else:
            if stripped.startswith(fence_marker):
                fence_marker = None
                out.append(line)
            else:
                out.append("")
    return "\n".join(out)


def parse_event_blocks(
    text: str, *, valid_states: Sequence[str],
) -> List[EventBlock]:
    """Parse every ``cairn-event-*`` fence in ``text`` into validated
    :class:`EventBlock` objects, in document order.

    ``valid_states`` bounds ``from_state``/``to_state`` -- the caller
    (``extract.py``) supplies the real runtime vocabulary (current +
    historical, per artifact kind); this function performs no loading of
    its own.  Text carrying no fence at all returns an empty list
    (nothing is wrong with a document that has not yet recorded any
    events).  A fence that fails to validate -- unknown key, unknown
    kind, unknown version token, missing required key, or a value
    outside its bounds -- raises :class:`EventGrammarError` naming the
    line and the reason; the whole call refuses rather than silently
    skipping the one bad block and returning the rest.

    A fence found inside a triple-backtick/tilde MARKDOWN code block is
    never real -- see :func:`_blank_fenced_code_blocks` -- and is
    excluded from every check above, including the refusal checks: an
    illustrative example with a deliberately-wrong field is legitimate
    documentation, not a defect to refuse on."""
    scan_text = _blank_fenced_code_blocks(text)
    blocks: List[EventBlock] = []
    for m in _FENCE_RE.finditer(scan_text):
        line_no = _line_of(scan_text, m.start())
        version = m.group("version")
        if version != _VERSION_SUFFIX:
            raise EventGrammarError(
                f"line {line_no}: unknown event version token "
                f"'cairn-event-{version}' -- only '{VERSION_TOKEN}' is "
                f"recognized"
            )
        body = m.group("body")
        raw = m.group(0)

        parsed: Dict[str, str] = {}
        for body_line in body.splitlines():
            stripped = body_line.strip()
            if not stripped:
                continue
            fm = _FIELD_LINE_RE.match(stripped)
            if not fm:
                raise EventGrammarError(
                    f"line {line_no}: malformed event field line "
                    f"{stripped!r} -- expected 'key: value'"
                )
            key, value = fm.group(1), fm.group(2).strip()
            if key in parsed:
                raise EventGrammarError(
                    f"line {line_no}: duplicate event key '{key}'"
                )
            parsed[key] = value

        if "kind" not in parsed:
            raise EventGrammarError(
                f"line {line_no}: event block is missing the required "
                f"'kind' key"
            )
        kind = parsed["kind"]
        if kind not in VALID_KINDS:
            raise EventGrammarError(
                f"line {line_no}: unknown event kind '{kind}' -- expected "
                f"one of {', '.join(VALID_KINDS)}"
            )

        allowed = _ALLOWED_KEYS[kind]
        unknown = sorted(set(parsed) - allowed)
        if unknown:
            raise EventGrammarError(
                f"line {line_no}: unknown key(s) for kind '{kind}': "
                f"{', '.join(unknown)}"
            )
        missing = [k for k in _REQUIRED_KEYS[kind] if k not in parsed]
        if missing:
            raise EventGrammarError(
                f"line {line_no}: event kind '{kind}' is missing required "
                f"key(s): {', '.join(missing)}"
            )

        if kind == KIND_TRANSITION:
            for state_key in ("from_state", "to_state"):
                value = parsed[state_key]
                if value not in valid_states:
                    raise EventGrammarError(
                        f"line {line_no}: {state_key} {value!r} is not a "
                        f"declared lifecycle status for this artifact type"
                    )
        if kind == KIND_REVIEW_PASS and parsed["tier"] not in VALID_TIERS:
            raise EventGrammarError(
                f"line {line_no}: tier {parsed['tier']!r} is not one of "
                f"{', '.join(VALID_TIERS)}"
            )
        for len_bound_key in ("reviewer", "model", "recorded_by"):
            if len_bound_key in parsed and len(parsed[len_bound_key]) > _MAX_FIELD_LEN:
                raise EventGrammarError(
                    f"line {line_no}: {len_bound_key} exceeds "
                    f"{_MAX_FIELD_LEN} characters"
                )

        blocks.append(EventBlock(kind=kind, fields=dict(parsed), raw=raw))
    return blocks


# ------------------------------------------------------- the history-diff reader
#
# The algorithm, reproduced from Round 7 §2-§4 as the binding contract this
# section pins:
#
#   1. Walk the artifact's rename-aware history, oldest first.
#   2. At each commit, parse the block sequence at that commit and at its
#      parent; the parent sequence must be an exact prefix of the child's --
#      any reordering, edit, or deletion of an existing block is a mutation
#      and refuses.
#   3. Attribute only the added suffix to that commit.
#   4. Require the matching lifecycle act in the same diff (a `transition`
#      block needs the `**Status**` change; a `review-pass` block needs the
#      added review section; a `response` block needs the added Response
#      section).
#   5. Refuse on ambiguous multi-parent attribution -- a merge commit is
#      never an introducing commit.
#
# Identity is `(introducing full commit SHA, added-block index)`, both
# derived here and never stored.
#
# **The act list is read from the same committed history the block list is
# read from, not from the live working-copy file.**  This reader never calls
# `Path.read_text()` on the artifact -- every content read is `git show
# <sha>:<path>` -- so an uncommitted working-copy edit is structurally
# invisible to it, symmetrically on both the block side and the act side
# (EPR-15's resolution).


class ReconciliationError(ValueError):
    """History cannot be reconciled at all: a mutated existing block, a
    merge commit introducing a block, an event block with no matching
    lifecycle act in its own introducing commit, or an unresolvable
    grammar violation.  Fail-closed -- a defensible series is not produced
    when one cannot be computed."""


class GitUnavailable(RuntimeError):
    """Git itself could not be consulted (no ``git`` on PATH, not a git
    checkout, or the command otherwise failed) -- distinct from
    :class:`ReconciliationError`, which means git IS available but the
    history it reports cannot be reconciled.  The caller (Chunk 6's
    wiring in ``extract.py``) is the one that knows whether this
    matters: unavailable git forecloses proving an artifact is past its
    activation cutoff, so it is treated as pre-cutoff rather than
    refused (Chunk 5's Activation section)."""


#: Section-kind tags for a `review-pass` act/event -- which heading
#: pattern matched, retained alongside the reconciled record (rather than
#: the block's own self-reported `tier` field) so `extract_plan_row` can
#: classify `plan_review_rounds` vs. `code_review_rounds` by the same
#: `_CODE_REVIEW_HEADING_RE`/`_PLAN_REVIEW_HEADING_RE` patterns it already
#: imports -- the reconciler already inspected the matched heading line to
#: confirm the act exists at all, so this repurposes that inspection
#: rather than depending on a block author correctly setting `tier: Code`.
SECTION_KIND_REVIEW = "review"
SECTION_KIND_PLAN_REVIEW = "plan-review"
SECTION_KIND_CODE_REVIEW = "code-review"

_RESPONSE_HEADING_RE = re.compile(r'^## Response\b')
_REVIEW_HEADING_RE = re.compile(r'^## Review\b')


def _section_kind_of(line: str) -> Optional[str]:
    """Which review-pass section-kind a heading LINE matches, or ``None``.
    Checked in a fixed order so a heading that happens to match more than
    one pattern (should not occur given the patterns' own anchors, but
    checked defensively) resolves deterministically."""
    if _PLAN_REVIEW_HEADING_RE.match(line):
        return SECTION_KIND_PLAN_REVIEW
    if _CODE_REVIEW_HEADING_RE.match(line):
        return SECTION_KIND_CODE_REVIEW
    if _REVIEW_HEADING_RE.match(line):
        return SECTION_KIND_REVIEW
    return None


def _new_matching_lines(
    parent_text: str, child_text: str, predicate,
) -> List[str]:
    """Lines in ``child_text`` matching ``predicate`` that were NOT already
    present (by exact string, multiset-counted) in ``parent_text`` --
    the added suffix's structural evidence, in order of appearance.
    Multiset (not set) so a second occurrence of an already-present exact
    line still counts as new; two commits can each add a heading whose
    text happens to collide only in a synthetic fixture, and the count
    must not silently drop the second one."""
    parent_counts: Counter = Counter(
        line for line in parent_text.splitlines() if predicate(line))
    seen: Counter = Counter()
    new_lines: List[str] = []
    for line in child_text.splitlines():
        if not predicate(line):
            continue
        seen[line] += 1
        if seen[line] > parent_counts.get(line, 0):
            new_lines.append(line)
    return new_lines


def _status_of(text: str) -> str:
    """The raw ``**Status**:`` header field value, or ``''`` when absent
    (including when ``text`` is the empty string standing in for "the
    file did not exist yet")."""
    return _header_field(text, "Status") if text else ""


# --------------------------------------------------------------- git plumbing


def _run_git(repo_root: Path, args: Sequence[str], *, timeout: int = 30):
    try:
        return subprocess.run(
            ["git", *args], cwd=str(repo_root), capture_output=True,
            timeout=timeout, check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        raise GitUnavailable(f"git could not be run: {exc}") from None


def _git_available(repo_root: Path) -> bool:
    """Whether ``repo_root`` is a usable git checkout at all -- checked
    once, cheaply, rather than inferring "unavailable" from every
    downstream call returning empty (which would be indistinguishable
    from "genuinely no history")."""
    try:
        result = _run_git(repo_root, ["rev-parse", "--git-dir"], timeout=10)
    except GitUnavailable:
        return False
    return result.returncode == 0


def _show(repo_root: Path, commit: str, relpath: str) -> Optional[str]:
    """``git show <commit>:<relpath>``, or ``None`` when the path did not
    exist at that commit (never raises for that ordinary case)."""
    result = _run_git(repo_root, ["show", f"{commit}:{relpath}"])
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8", errors="replace")


@dataclass(frozen=True)
class _FollowedCommit:
    sha: str          # full commit SHA
    parents: Tuple[str, ...]
    path: str         # the artifact's path AS IT APPEARED at this commit


def _followed_history(repo_root: Path, relpath: str) -> List[_FollowedCommit]:
    """The artifact's rename-aware history, OLDEST FIRST: one
    :class:`_FollowedCommit` per commit that touched ``relpath`` (or an
    earlier name it was renamed from), each carrying the full parent SHA
    list (so a merge commit's multi-parent shape is visible) and the
    path the artifact held AT that commit (so content reads survive a
    rename without a second, hand-rolled rename detector).

    **A known limitation of ``--follow``, discovered building this
    reader's own test fixtures (row 7-1/7-2): its rename detection is
    CONTENT-SIMILARITY-based, not identity-based.** Two unrelated
    proposals whose bodies happen to be near-identical -- a hand-built
    test fixture using boilerplate text for both, most concretely -- can
    make git attribute a brand-new file's CREATION commit as a "rename"
    from an entirely different, pre-existing file, pulling that other
    file's own commit into this one's history. For a real lifecycle
    corpus this is very unlikely (each proposal/plan carries a distinct
    title, author, date, and substantive prose), but it is a real
    property of this function, not a hypothetical one -- named here
    rather than only worked around in the fixtures that hit it."""
    parents_out = _run_git(
        repo_root,
        ["log", "--follow", "--format=%H%x00%P", "--", relpath],
    )
    if parents_out.returncode != 0:
        return []
    parents_by_sha: Dict[str, Tuple[str, ...]] = {}
    order: List[str] = []
    for line in parents_out.stdout.decode("utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        parts = line.split("\x00")
        sha = parts[0]
        parent_field = parts[1] if len(parts) > 1 else ""
        parents_by_sha[sha] = tuple(parent_field.split()) if parent_field else ()
        order.append(sha)

    paths_out = _run_git(
        repo_root,
        ["log", "--follow", "--format=%x01%H", "--name-only", "--", relpath],
    )
    path_by_sha: Dict[str, str] = {}
    if paths_out.returncode == 0:
        current_sha: Optional[str] = None
        for line in paths_out.stdout.decode("utf-8", errors="replace").splitlines():
            if line.startswith("\x01"):
                current_sha = line[1:]
            elif line.strip() and current_sha is not None and current_sha not in path_by_sha:
                path_by_sha[current_sha] = line

    commits = [
        _FollowedCommit(
            sha=sha, parents=parents_by_sha[sha],
            path=path_by_sha.get(sha, relpath),
        )
        for sha in order
    ]
    commits.reverse()  # `git log` is newest-first; the algorithm walks oldest-first.
    return commits


def _check_no_merge_smuggled_a_block(
    repo_root: Path, relpath: str, *, valid_states: Sequence[str],
) -> None:
    """Step 5's own safety net, run separately from the main walk.

    ``git log --follow`` -- the main walk's own history source -- never
    surfaces a merge commit touching a path at all (git's default history
    simplification hides it, and this holds even with ``--full-history``
    added: the two do not compose the way their names suggest, verified
    empirically while building this reader). So the main walk can never
    observe a merge commit on its own, and the "ambiguous multi-parent
    attribution" refusal needs its own pass: ``--full-history`` alone
    (no ``--follow``) over the artifact's CURRENT path finds every real
    merge commit, and for each one, a merge whose own block count
    exceeds every parent's own block count at the same path has blocks
    neither parent accounts for -- necessarily introduced by the merge
    resolution itself. Rename-unaware by construction (a merge commit
    that predates an archive rename is out of this check's reach); named
    here rather than silently assumed complete."""
    result = _run_git(
        repo_root,
        ["log", "--full-history", "--min-parents=2",
         "--format=%H%x00%P", "--", relpath],
    )
    if result.returncode != 0:
        return
    for line in result.stdout.decode("utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        parts = line.split("\x00")
        sha = parts[0]
        parent_shas = parts[1].split() if len(parts) > 1 and parts[1] else []
        merge_content = _show(repo_root, sha, relpath)
        if merge_content is None:
            continue
        merge_block_count = len(
            parse_event_blocks(merge_content, valid_states=valid_states))
        if merge_block_count == 0:
            continue
        parent_max = 0
        for parent_sha in parent_shas:
            parent_content = _show(repo_root, parent_sha, relpath)
            if parent_content is None:
                continue
            parent_max = max(
                parent_max,
                len(parse_event_blocks(parent_content, valid_states=valid_states)),
            )
        if merge_block_count > parent_max:
            raise ReconciliationError(
                f"{sha}: a merge commit cannot introduce a new event "
                f"block -- ambiguous multi-parent attribution"
            )


# ------------------------------------------------------------- reconciled data


@dataclass(frozen=True)
class ReconciledEvent:
    """One event, attributed to its introducing commit -- identity is the
    ``(commit, index)`` pair, both fields here."""

    kind: str
    commit: str
    index: int
    section_kind: Optional[str]
    block: EventBlock


@dataclass(frozen=True)
class UnmatchedAct:
    """A structural act with no corresponding event block, at a given
    commit -- what Chunk 6's post-cutoff reconciliation turns into
    `INCOMPLETE`, and what a pre-cutoff act simply is (no block expected
    yet)."""

    kind: str
    commit: str
    section_kind: Optional[str]
    detail: str


@dataclass(frozen=True)
class HistoryWalkResult:
    events: List[ReconciledEvent] = field(default_factory=list)
    unmatched_acts: List[UnmatchedAct] = field(default_factory=list)


def walk_history(
    repo_root: Path, relpath: str, *, valid_states: Sequence[str],
) -> HistoryWalkResult:
    """Walk ``relpath``'s rename-aware history oldest-first, attributing
    every event block to its introducing commit and reporting every
    structural act with no matching block (as :class:`UnmatchedAct`,
    for the caller to judge against the activation cutoff).

    Raises :class:`GitUnavailable` when git itself cannot be consulted,
    and :class:`ReconciliationError` (or :class:`EventGrammarError`) on
    any of: a mutated existing block, a merge commit introducing a
    block, or an event block with no matching act in its own
    introducing commit."""
    if not _git_available(repo_root):
        raise GitUnavailable(f"{repo_root} is not a usable git checkout")

    _check_no_merge_smuggled_a_block(repo_root, relpath, valid_states=valid_states)

    commits = _followed_history(repo_root, relpath)
    events: List[ReconciledEvent] = []
    unmatched: List[UnmatchedAct] = []

    prev_content: Optional[str] = None
    prev_blocks: List[EventBlock] = []

    for commit in commits:
        child_content = _show(repo_root, commit.sha, commit.path)
        if child_content is None:
            # The path this commit is indexed under does not resolve at
            # this commit -- can happen at the tail of a --follow chain
            # when rename detection's own path attribution is imprecise.
            # Skip rather than fail closed on a plumbing artifact; the
            # block-sequence invariant is unaffected either way, since
            # nothing is attributed here.
            continue
        child_blocks = parse_event_blocks(child_content, valid_states=valid_states)

        if child_blocks[:len(prev_blocks)] != prev_blocks:
            raise ReconciliationError(
                f"{commit.sha}: an existing event block was mutated "
                f"(edited, reordered, or deleted) -- the prior block "
                f"sequence is no longer an exact prefix of this commit's"
            )
        added = child_blocks[len(prev_blocks):]
        is_merge = len(commit.parents) > 1

        # File CREATION (no prior committed content at all) is treated
        # specially below: an artifact declaring its first-ever status is
        # not a transition act requiring a block -- the grammar's own
        # from_state bound requires "a declared lifecycle status", and
        # there is no prior state to declare a transition FROM.  A
        # creation commit MAY still carry a transition block (some
        # authors document the opening state explicitly); it is simply
        # never REQUIRED to, in either direction.
        is_creation = prev_content is None
        parent_text = prev_content or ""
        status_changed = (
            _status_of(child_content) != ""
            and _status_of(child_content) != _status_of(parent_text)
        )
        new_review_lines = _new_matching_lines(
            parent_text, child_content, lambda l: _section_kind_of(l) is not None)
        new_response_lines = _new_matching_lines(
            parent_text, child_content, lambda l: bool(_RESPONSE_HEADING_RE.match(l)))

        added_transition = [b for b in added if b.kind == KIND_TRANSITION]
        added_review = [b for b in added if b.kind == KIND_REVIEW_PASS]
        added_response = [b for b in added if b.kind == KIND_RESPONSE]

        if len(added_transition) > 1:
            raise ReconciliationError(
                f"{commit.sha}: more than one transition block added in "
                f"one commit -- a single diff carries at most one "
                f"**Status** change"
            )
        if added_transition and not (status_changed or is_creation):
            raise ReconciliationError(
                f"{commit.sha}: a transition block was added with no "
                f"matching **Status** change in this diff"
            )
        if len(added_review) > len(new_review_lines):
            raise ReconciliationError(
                f"{commit.sha}: {len(added_review)} review-pass block(s) "
                f"added but only {len(new_review_lines)} new review-type "
                f"section(s) found in this diff"
            )
        if len(added_response) > len(new_response_lines):
            raise ReconciliationError(
                f"{commit.sha}: {len(added_response)} response block(s) "
                f"added but only {len(new_response_lines)} new Response "
                f"section(s) found in this diff"
            )
        if added and is_merge:
            raise ReconciliationError(
                f"{commit.sha}: a merge commit cannot introduce a new "
                f"event block -- ambiguous multi-parent attribution"
            )

        for i, block in enumerate(added):
            section_kind = None
            if block.kind == KIND_REVIEW_PASS:
                paired_idx = added_review.index(block)
                if paired_idx < len(new_review_lines):
                    section_kind = _section_kind_of(new_review_lines[paired_idx])
            events.append(ReconciledEvent(
                kind=block.kind, commit=commit.sha, index=i,
                section_kind=section_kind, block=block,
            ))

        if status_changed and not added_transition and not is_creation:
            unmatched.append(UnmatchedAct(
                kind=KIND_TRANSITION, commit=commit.sha, section_kind=None,
                detail="a **Status** change has no matching transition block",
            ))
        for extra_line in new_review_lines[len(added_review):]:
            unmatched.append(UnmatchedAct(
                kind=KIND_REVIEW_PASS, commit=commit.sha,
                section_kind=_section_kind_of(extra_line),
                detail=f"section {extra_line!r} has no matching review-pass block",
            ))
        for extra_line in new_response_lines[len(added_response):]:
            unmatched.append(UnmatchedAct(
                kind=KIND_RESPONSE, commit=commit.sha, section_kind=None,
                detail=f"section {extra_line!r} has no matching response block",
            ))

        prev_content = child_content
        prev_blocks = child_blocks

    return HistoryWalkResult(events=events, unmatched_acts=unmatched)


# ------------------------------------------------------------- activation


def _marker_status_by_commit(
    repo_root: Path, relpath: str, marker: str = VERSION_TOKEN,
) -> List[Tuple[str, bool]]:
    """``[(sha, marker_present), ...]`` oldest-first for every commit
    touching ``relpath`` -- the raw signal both the introducing-commit
    derivation and the multiply-introduced check are built from."""
    commits = _followed_history(repo_root, relpath)
    out: List[Tuple[str, bool]] = []
    for commit in commits:
        content = _show(repo_root, commit.sha, commit.path)
        out.append((commit.sha, content is not None and marker in content))
    return out


#: Memoized per ``(repo_root, template_relpath, companion_relpath)`` --
#: a corpus walk calls this once per ARTIFACT, but the answer depends
#: only on the TEMPLATE's own history, which is identical for every
#: artifact of one kind (every proposal shares one
#: ``dev/proposals/_template.md`` cutoff).  Recomputing it per file
#: turned a real corpus walk from a handful of git invocations into one
#: per artifact -- measured empirically running the real extractor
#: against this repository's own corpus during Chunk 6's implementation.
#: A refusal (:class:`ReconciliationError`) is NOT cached: a transient
#: refusal should be re-derived, not remembered as permanent.
_activation_cache: Dict[Tuple[str, str, Optional[str]], Optional[str]] = {}


def activation_commit(
    repo_root: Path, template_relpath: str,
    *, companion_relpath: Optional[str] = None,
) -> Optional[str]:
    """The full SHA of the commit that FIRST adds the literal
    ``cairn-event-v1`` marker to ``template_relpath``'s history, or
    ``None`` when the marker has never been introduced -- **not** a
    refusal (Chunk 5's Activation section, disposition (c), authorized
    by the Maintainer: "I think (c) is right"): a tree with no marker at
    all is simply not yet activated, every act on it pre-cutoff.

    Refuses (:class:`ReconciliationError`) on:

    * **multiply-introduced** -- the marker's presence toggles
      absent -> present more than once across the commit sequence
      (added, removed, re-added);
    * **divergent** -- when ``companion_relpath`` is given and exists in
      this tree, and its own marker-introduction state (present vs.
      absent, as of HEAD) disagrees with ``template_relpath``'s.  This is
      the mechanism for Cairn's own self-hosted case, where
      ``templates/core/...`` mirrors the installed template; an ordinary
      adopter tree carries no such companion at all, so the check is
      vacuously skipped when ``companion_relpath`` does not resolve --
      this is this module's own design choice for a mechanism Round 7's
      text names but does not specify (recorded in the implementing
      commit body, per this task's instrument-confirmation rule)."""
    cache_key = (str(repo_root), template_relpath, companion_relpath)
    if cache_key in _activation_cache:
        return _activation_cache[cache_key]

    history = _marker_status_by_commit(repo_root, template_relpath, VERSION_TOKEN)

    # Count absent->present edges across the oldest-first sequence (the
    # "removed and re-added" signal), capturing the FIRST such edge's
    # commit as the candidate introducing commit.
    edges = 0
    first_present_sha: Optional[str] = None
    was_present = False
    for sha, present in history:
        if present and not was_present:
            edges += 1
            if first_present_sha is None:
                first_present_sha = sha
        was_present = present

    if edges == 0:
        result: Optional[str] = None
    elif edges == 1:
        result = first_present_sha
    else:
        raise ReconciliationError(
            f"{template_relpath}: the '{VERSION_TOKEN}' marker was "
            f"removed and re-added ({edges} introductions) -- "
            f"multiply-introduced markers refuse rather than guessing "
            f"which period they cover"
        )

    if companion_relpath is not None:
        companion_path = repo_root / companion_relpath
        if companion_path.is_file():
            companion_present_at_head = VERSION_TOKEN in companion_path.read_text(
                encoding="utf-8", errors="replace")
            primary_present_at_head = result is not None
            if companion_present_at_head != primary_present_at_head:
                raise ReconciliationError(
                    f"{template_relpath}: divergent activation marker -- "
                    f"{template_relpath} and {companion_relpath} disagree "
                    f"on whether the '{VERSION_TOKEN}' marker is present"
                )

    _activation_cache[cache_key] = result
    return result


# --------------------------------------------------------- fail-closed reconciliation
#
# Chunk 6: ties `activation_commit()` and `walk_history()` together into the
# cutoff-aware disposition `extract.py` wires into the retained-field
# columns.  "Empty" for a pre-cutoff or unprovable-cutoff review-pass/
# response field is the literal string `''`, never `0`/`False`/any other
# falsy stand-in that could be mistaken for a computed value -- named here
# because the caller (`extract.py`) is where that representation is chosen,
# but the boundary this module returns (which events are POST-cutoff) is
# what makes that choice possible in the first place.


def _is_strictly_after(repo_root: Path, cutoff_sha: str, candidate_sha: str) -> bool:
    """Whether ``candidate_sha`` is strictly after ``cutoff_sha`` in
    history -- true ancestry, EXCLUSIVE of equality: the marker's own
    introducing commit is itself pre-cutoff (Chunk 5's Activation
    section, "the marker's own introducing commit is pre-cutoff, not
    post-cutoff"), not the boundary at which post-cutoff behavior
    starts."""
    if candidate_sha == cutoff_sha:
        return False
    result = _run_git(
        repo_root, ["merge-base", "--is-ancestor", cutoff_sha, candidate_sha])
    return result.returncode == 0


@dataclass(frozen=True)
class Reconciliation:
    """The final, cutoff-aware disposition for one artifact's events --
    what `extract.py` reads to source the retained event-derived fields."""

    activation: Optional[str]              # the cutoff commit, or None (never activated)
    events: List[ReconciledEvent] = field(default_factory=list)
    post_cutoff_events: List[ReconciledEvent] = field(default_factory=list)
    #: Acts (of any kind) that are NOT provably post-cutoff -- either a
    #: real pre-cutoff act (before the marker's own introduction), or the
    #: marker's own introducing commit itself (exclusive reading), or
    #: every act at all when the tree was never activated.  `extract.py`
    #: reads this to decide the "empty, not a silently-partial count"
    #: disposition per retained field: an artifact carrying BOTH a
    #: pre-cutoff and a post-cutoff act of the same kind reports that
    #: field empty rather than a count that omits the pre-cutoff one --
    #: this module's own resolution of a genuine ambiguity in the
    #: accepted text for the mixed-history case (recorded in the
    #: implementing commit body).
    pre_cutoff_acts: List[UnmatchedAct] = field(default_factory=list)
    incomplete_reasons: List[str] = field(default_factory=list)

    @property
    def incomplete(self) -> bool:
        return bool(self.incomplete_reasons)


def reconcile(
    repo_root: Path, relpath: str, *, valid_states: Sequence[str],
    template_relpath: str, companion_relpath: Optional[str] = None,
) -> Reconciliation:
    """The fail-closed, cutoff-aware reconciliation entry point.

    Combines :func:`activation_commit` (read from ``template_relpath``'s
    own history -- the artifact-KIND-wide cutoff) with :func:`walk_history`
    (this SPECIFIC artifact's own event blocks), classifying every event
    and every unmatched act as pre- or post-cutoff.  A post-cutoff
    unmatched act is what makes ``.incomplete`` true; a pre-cutoff one is
    not an error at all -- it is simply what "before its cutoff, an empty
    series is correct" (Round 7 SS4) looks like.

    Raises :class:`GitUnavailable` when there is no git checkout at all
    (the caller -- ``extract.py`` -- is the one that knows this means
    "cannot prove past cutoff, fall back to pre-cutoff behavior", not
    "refuse"; that disposition lives there, not here, because it differs
    by field kind).  Raises :class:`ReconciliationError` (or
    :class:`EventGrammarError`) on any structural defect a mutated block,
    an orphaned block, a merge-smuggled block, or a malformed grammar --
    all unconditional, independent of the activation cutoff.

    **Never activated is a fast path, not merely a special case.** When
    ``activation_commit`` returns ``None``, every act on this artifact is
    pre-cutoff by definition (disposition (c)) regardless of what a full
    history walk would show, so this returns immediately WITHOUT calling
    :func:`walk_history` at all -- skipping a `git log`/`git show` walk
    (and the separate merge-commit scan) per artifact that a corpus-wide
    call would otherwise pay for every single file, for a result the
    cutoff alone already determines.  Measured empirically: running the
    real extractor against this repository's own corpus, before this
    fast path existed, did not complete inside a 120-second budget.

    **An artifact untouched since the cutoff is a second fast path, for
    the same reason.** Once activation is real (a marker IS committed),
    the corpus-wide cost moves from "one activation check" to "one full
    history walk per artifact" -- measured empirically, over Cairn's own
    corpus, as the difference between an 8-second run and one that did
    not finish in two minutes. If ``relpath``'s own most recent commit is
    not strictly after ``cutoff``, NOTHING in its history can be
    post-cutoff either, so the full walk (and its merge-commit scan) is
    skipped; only ``HEAD``'s own current content is read once, to tell a
    genuinely event-free artifact (0) apart from one whose acts are all
    pre-cutoff (empty) -- the same distinction Chunk 6's `_reconciled_kind`
    otherwise draws from a full walk's `pre_cutoff_acts`, cheapened here to
    "does the CURRENT text carry a review/response heading at all",
    trading detail (which specific commit, which specific act) for a
    single `git show` instead of a walk -- correct because a per-kind
    breakdown is never needed when EVERY act is already known to be
    pre-cutoff."""
    cutoff = activation_commit(
        repo_root, template_relpath, companion_relpath=companion_relpath)
    if cutoff is None:
        return Reconciliation(activation=None)

    latest = _run_git(
        repo_root, ["log", "-1", "--format=%H", "--", relpath])
    latest_sha = (
        latest.stdout.decode("utf-8", errors="replace").strip()
        if latest.returncode == 0 else ""
    )
    if not latest_sha or not _is_strictly_after(repo_root, cutoff, latest_sha):
        head_text = _show(repo_root, "HEAD", relpath) or ""
        pre_cutoff_acts: List[UnmatchedAct] = []
        if any(_section_kind_of(l) is not None for l in head_text.splitlines()):
            pre_cutoff_acts.append(UnmatchedAct(
                kind=KIND_REVIEW_PASS, commit=latest_sha or "(untracked)",
                section_kind=None,
                detail="fast path: artifact untouched since cutoff, "
                       "current text carries a review-type heading",
            ))
        if any(_RESPONSE_HEADING_RE.match(l) for l in head_text.splitlines()):
            pre_cutoff_acts.append(UnmatchedAct(
                kind=KIND_RESPONSE, commit=latest_sha or "(untracked)",
                section_kind=None,
                detail="fast path: artifact untouched since cutoff, "
                       "current text carries a Response heading",
            ))
        return Reconciliation(activation=cutoff, pre_cutoff_acts=pre_cutoff_acts)

    walked = walk_history(repo_root, relpath, valid_states=valid_states)

    post_cutoff_events = [
        ev for ev in walked.events
        if cutoff is not None and _is_strictly_after(repo_root, cutoff, ev.commit)
    ]
    incomplete_reasons = [
        f"{relpath} @ {act.commit}: {act.kind} act has no matching event "
        f"block -- {act.detail}"
        for act in walked.unmatched_acts
        if cutoff is not None and _is_strictly_after(repo_root, cutoff, act.commit)
    ]
    pre_cutoff_acts = [
        act for act in walked.unmatched_acts
        if not (cutoff is not None and _is_strictly_after(repo_root, cutoff, act.commit))
    ]

    return Reconciliation(
        activation=cutoff, events=walked.events,
        post_cutoff_events=post_cutoff_events,
        pre_cutoff_acts=pre_cutoff_acts,
        incomplete_reasons=incomplete_reasons,
    )
