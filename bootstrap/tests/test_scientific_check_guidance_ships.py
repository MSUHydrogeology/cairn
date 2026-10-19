"""The independent-scientific-check guidance must reach an author word for word.

An author reads the check in the proposal template and in the plan template,
and an adopter receives both through the shipped copies under
``templates/core/``. Cairn keeps its own copy of each template too, so four
files carry the guidance. None of it sits in a slot, so nothing an adopter
writes can explain a difference between the copies.

This module holds the proposal block and the plan paragraph as whole texts and
compares every copy to them by equality, not by clause anchors. An anchor per
clause leaves the clauses that make the rule binding ("only if", "becomes",
"written down before the result is seen") free to be deleted from both copies
at once, with every anchor still found and the two copies still equal. Pinning
every word closes that, at a price: editing either text means editing this
test in the same commit.

It also pins the layout and the place. Collapsing whitespace is what lets a
sentence be re-wrapped, and it would also let a nested list flatten into one
list, or a paragraph fold into the bullet above it, with every word still
present. So the blank lines, the list items (with their indents and markers)
and the paragraph starts are compared as well, and line wrapping is the only
thing left free. The block must come after the security-preflight sub-block,
whose slice another test compares byte for byte between the two proposal
templates: a block placed inside that slice would be swallowed into it and no
test would go red, because both copies grow alike. It must be followed by the
Signals heading, and the plan paragraph must sit under Acceptance criteria
after the security-touching paragraph. Neither text may sit inside a slot,
because an adopter who fills the slot replaces everything in it.

Three further places tell a reader what the review practice does about
scientific results: the Complex position in ``dimensions/complexity.md``, the
Complexity row of ``dimensions/README.md``, and the profile-filling paragraph
of ``bootstrap/BOOTSTRAP.md``. Each must point at the check, not at a review
lens that no module installs, and this module requires each to name it. That
is presence only, never absence: a later change may reword those places, or
put a lens beside the check, without touching this module, provided the check
stays named.

Whitespace is collapsed before comparing, so the check is on words and not on
line width. A failure names the copy and the first sentence that differs.

**What it deliberately does not test.** It does not test that a proposal which
touches a scientific assumption carries a check, or that a check is
independent. Those are the reviewer's judgment, and a pattern for them would
only be a ritual.

Run from the Cairn repo root:
    python -m pytest bootstrap/tests/test_scientific_check_guidance_ships.py
"""
from __future__ import annotations

import re
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent

_PROPOSAL_TEMPLATES = (
    "dev/proposals/_template.md",
    "templates/core/dev/proposals/_template.md",
)
_PLAN_TEMPLATES = (
    "dev/plans/_template.md",
    "templates/core/dev/plans/_template.md",
)

_PROMISE_SITES = (
    "dimensions/complexity.md",
    "dimensions/README.md",
    "bootstrap/BOOTSTRAP.md",
)
_CHECK_NAME = "independent scientific check"
_COMPLEXITY_FINDING = (
    'an unexplained "N/A" on a change that touches a scientific assumption '
    "or a result the project publishes or acts on is a review finding"
)

_BLOCK_HEADING = "### Independent scientific check"
_PREFLIGHT_CLOSE = "**Prospective only.**"
_PROPOSAL_NEXT_HEADING = "## Signals the change is wrong"
_PLAN_LEAD = "**An independent scientific check is accepted scope.**"
_PLAN_PRECEDING = "A security-touching plan re-answers"
_PLAN_HOME_HEADING = "## Acceptance criteria"
_PLAN_SLOT = "acceptance-doc-tooling"

#: The proposal template's block, word for word. Whitespace is collapsed when
#: it is compared, so line wrapping is free and the words are not.
_PROPOSAL_BLOCK = """\
### Independent scientific check

*Gated to a change that touches a scientific assumption, or a result the
project publishes or acts on: a governing equation, a unit or sign convention,
a boundary condition, a parameter default, a calibration setup, or a coupling
between models. For every other change, one line — "N/A: no scientific
assumption or result touched" — is the correct entry.*

Name **one** check that could show the change is wrong about the world, not
only about itself:

* **What it compares.** The quantity, the expected value, and the tolerance
  with its source. Say whether the data behind the expected value is in hand
  and has been checked. If the check depends on data that does not exist yet,
  say so.
* **Why the expectation is independent.** Neither the proposed code nor a test
  written from the same understanding computes it. Its basis is one of these:
  * an analytical or manufactured solution;
  * a conservation law chosen against the error this change risks (a closed
    budget does not catch a wrong input);
  * a trusted observation or benchmark;
  * an independent implementation, or the saved output of the model the code
    reads (independent of the port, not of the model's physics);
  * a domain expert's expectation, written down before the result is seen.
* **The error it would catch.** The plausible mistake under which the check
  fails (a reversed sign, a unit slip, a misplaced boundary, a missed
  warm-up). This is security preflight S2's "Can it fail?", asked of a
  scientific check. At implementation, the implementer makes that mistake on
  purpose and records the check's failing output.
* **When the check passes by finding nothing.** A check that passes on "no
  change", "no difference" or "no effect" is evidence only if it could have
  found a change. Show the same analysis detecting a known effect of the size
  that matters (a positive control), or say plainly that it cannot. The failing
  run above serves as the control when the mistake it makes produces an effect
  of that size. At implementation, the implementer records the control with the
  failing run. For example, an analysis that reports no streamflow depletion
  from a pumping well first recovers the depletion of a synthetic well of
  comparable rate.

**Reviewers.** The proposal reviewer challenges whether the basis is really
independent of the code under review. The code reviewer verifies the recorded
failing run and, where one is owed, the positive control, and re-runs them when
that is cheap. The Maintainer judges at the Decision whether this is the right
check and the expected value is right. If no independent basis exists, say so;
the Maintainer weighs that, and it is not a reason to invent one.
"""

#: The plan template's paragraph, word for word.
_PLAN_PARAGRAPH = """\
**An independent scientific check is accepted scope.** If the proposal names
one, it becomes an acceptance criterion. A replacement qualifies only if it
fails under the error the original names. If nothing qualifies, dropping the
check is a scope reduction under *Scope delta* and needs the Maintainer's
quoted allowance. Saying that the result now rests on the implementation does
not settle it. When the check fails for real during implementation, one line
records whether anything else would have shown the error.
"""


def _collapse(text: str) -> str:
    """Collapse runs of space, tab and line breaks to one space.

    Only ASCII whitespace: a non-breaking space is a different character and
    renders differently, so it counts as a difference.
    """
    return re.sub(r"[ \t\r\n]+", " ", text).strip()


def _first_difference(want: str, got: str) -> str:
    """Name the first sentence where two whitespace-collapsed texts differ."""
    split = lambda t: re.split(r"(?<=[.!?])\s+", _collapse(t))  # noqa: E731
    want_s, got_s = split(want), split(got)
    for i in range(max(len(want_s), len(got_s))):
        w = want_s[i] if i < len(want_s) else "<nothing>"
        g = got_s[i] if i < len(got_s) else "<nothing>"
        if w != g:
            return f"expected {w!r}, found {g!r}"
    return "the texts differ only in spacing"


_LIST_ITEM = re.compile(r"^(\s*)([*+-]|\d+[.)])\s+\S")


def _shape(lines: list[str]) -> list[tuple]:
    """The layout of a region, with line wrapping left free.

    One entry per blank line, per heading, per list item (with its indent and
    its marker) and per paragraph start. A line that only continues the line
    above adds nothing, so re-wrapping a sentence changes no entry, while
    flattening a nested list, dropping a blank line or turning a paragraph
    into part of a bullet does.
    """
    shape: list[tuple] = []
    for line in lines:
        item = _LIST_ITEM.match(line)
        if not line.strip():
            shape.append(("blank",))
        elif line.startswith("#"):
            shape.append(("heading", len(line) - len(line.lstrip("#"))))
        elif item:
            shape.append(("item", len(item.group(1)), item.group(2)))
        elif not shape or shape[-1] == ("blank",):
            shape.append(("paragraph",))
    return shape


def _first_shape_difference(want: list[tuple], got: list[tuple]) -> str:
    for i in range(max(len(want), len(got))):
        w = want[i] if i < len(want) else "<nothing>"
        g = got[i] if i < len(got) else "<nothing>"
        if w != g:
            return f"at layout element {i + 1}: expected {w}, found {g}"
    return "the layouts are equal"


def _only_line(lines: list[str], matches, what: str) -> int:
    """Index of the one line that ``matches``; an AssertionError otherwise.

    Raising, and never returning an empty region, matters: two missing
    regions would compare equal and the test would pass on nothing.
    """
    hits = [i for i, line in enumerate(lines) if matches(line)]
    if not hits:
        raise AssertionError(f"missing marker: no line {what}")
    if len(hits) > 1:
        raise AssertionError(f"marker repeated: {len(hits)} lines {what}")
    return hits[0]


def _is_slot_open(line: str) -> bool:
    return line.lstrip().startswith("<!-- cairn:slot")


def _is_slot_end(line: str) -> bool:
    return line.lstrip().startswith("<!-- cairn:end")


def _inside_a_slot(lines: list[str], index: int) -> bool:
    before = lines[:index]
    return sum(map(_is_slot_open, before)) != sum(map(_is_slot_end, before))


def _read(rel: str) -> list[str]:
    return (CAIRN_ROOT / rel).read_text(encoding="utf-8").splitlines()


def _without_trailing_blanks(lines: list[str]) -> list[str]:
    kept = list(lines)
    while kept and not kept[-1].strip():
        kept.pop()
    return kept


def test_the_check_guidance_reaches_every_copy_and_promise_site() -> None:
    """Both proposal copies hold the block, both plan copies hold the paragraph,
    each word for word, in the same layout, in the same place and outside every
    slot, and the three places that describe the review practice name the check.

    The groups accumulate into one ``failures`` list rather than stopping at
    the first, so every group runs every time and a failure shows all of what
    is wrong at once.

    (a) the block, in each proposal copy, equals the reviewed text in its words
        and in its layout (blank lines, list items with their indents and
        markers; line wrapping is free);
    (b) the paragraph, in each plan copy, equals the reviewed text the same way;
    (c) place: the block follows the security-preflight sub-block with no
        heading between and is followed directly by ``## Signals the change is
        wrong``; the paragraph sits under ``## Acceptance criteria``, after the
        security-touching paragraph and before the doc-tooling slot; neither
        holds a slot marker or sits inside a slot;
    (d) the three promise sites each name the check, and the Complex position
        says an unexplained "N/A" on a change that touches a scientific
        assumption or a result the project publishes or acts on is a review
        finding, which is the block's own gate. Presence only, and letter case
        is ignored.

    Not pinned, on purpose: text added as its own paragraph beside the pinned
    ones (the pinned text is closed, its neighbourhood is not), and where the
    text sits among the lines of a section the headings do not bound.
    """
    failures: list[str] = []

    for rel in _PROPOSAL_TEMPLATES:
        lines = _read(rel)
        try:
            start = _only_line(
                lines, lambda l: l == _BLOCK_HEADING, f"equal to {_BLOCK_HEADING!r}"
            )
            end = next(
                (j for j in range(start + 1, len(lines)) if lines[j].startswith("## ")),
                None,
            )
            if end is None:
                raise AssertionError("the block has no closing '## ' line after it")
        except AssertionError as exc:
            failures.append(f"(a) {rel}: {exc}")
            continue
        region = lines[start:end]
        if _collapse("\n".join(region)) != _collapse(_PROPOSAL_BLOCK):
            failures.append(
                f"(a) {rel}: the block differs from the reviewed text; "
                + _first_difference(_PROPOSAL_BLOCK, "\n".join(region))
            )
        got_shape = _shape(_without_trailing_blanks(region))
        want_shape = _shape(_PROPOSAL_BLOCK.splitlines())
        if got_shape != want_shape:
            failures.append(
                f"(a) {rel}: the block's layout differs from the reviewed text, "
                + _first_shape_difference(want_shape, got_shape)
            )
        if len(region) - len(_without_trailing_blanks(region)) != 1:
            failures.append(
                f"(a) {rel}: exactly one blank line must close the block, before "
                f"the next '## ' line"
            )
        if start == 0 or lines[start - 1].strip():
            failures.append(f"(a) {rel}: the block heading must follow a blank line")
        try:
            close = _only_line(
                lines,
                lambda l: l.startswith(_PREFLIGHT_CLOSE),
                f"starting {_PREFLIGHT_CLOSE!r}",
            )
            if start < close:
                failures.append(
                    f"(c) {rel}: the block sits above the line starting "
                    f"{_PREFLIGHT_CLOSE!r}, inside the security-preflight slice"
                )
            elif any(l.startswith("## ") for l in lines[close + 1:start]):
                failures.append(
                    f"(c) {rel}: a '## ' heading sits between the line starting "
                    f"{_PREFLIGHT_CLOSE!r} and the block"
                )
        except AssertionError as exc:
            failures.append(f"(c) {rel}: {exc}")
        if lines[end] != _PROPOSAL_NEXT_HEADING:
            failures.append(
                f"(c) {rel}: the block is followed by {lines[end]!r}, "
                f"not {_PROPOSAL_NEXT_HEADING!r}"
            )
        if any(_is_slot_open(l) or _is_slot_end(l) for l in region):
            failures.append(f"(c) {rel}: the block holds a slot marker")
        if _inside_a_slot(lines, start):
            failures.append(f"(c) {rel}: the block sits inside a slot")

    for rel in _PLAN_TEMPLATES:
        lines = _read(rel)
        try:
            start = _only_line(
                lines, lambda l: l.startswith(_PLAN_LEAD), f"starting {_PLAN_LEAD!r}"
            )
        except AssertionError as exc:
            failures.append(f"(b) {rel}: {exc}")
            continue
        end = next(
            (j for j in range(start + 1, len(lines)) if not lines[j].strip()),
            len(lines),
        )
        region = lines[start:end]
        if _collapse("\n".join(region)) != _collapse(_PLAN_PARAGRAPH):
            failures.append(
                f"(b) {rel}: the paragraph differs from the reviewed text; "
                + _first_difference(_PLAN_PARAGRAPH, "\n".join(region))
            )
        got_shape = _shape(region)
        want_shape = _shape(_PLAN_PARAGRAPH.splitlines())
        if got_shape != want_shape:
            failures.append(
                f"(b) {rel}: the paragraph's layout differs from the reviewed "
                "text, " + _first_shape_difference(want_shape, got_shape)
            )
        if start == 0 or lines[start - 1].strip():
            failures.append(f"(b) {rel}: the paragraph must follow a blank line")
        heading_above = next(
            (l for l in reversed(lines[:start]) if l.startswith("## ")), None
        )
        if heading_above != _PLAN_HOME_HEADING:
            failures.append(
                f"(c) {rel}: the paragraph sits under {heading_above!r}, "
                f"not {_PLAN_HOME_HEADING!r}"
            )
        try:
            before = _only_line(
                lines,
                lambda l: l.startswith(_PLAN_PRECEDING),
                f"starting {_PLAN_PRECEDING!r}",
            )
            if before > start:
                failures.append(
                    f"(c) {rel}: the paragraph sits above the paragraph starting "
                    f"{_PLAN_PRECEDING!r}"
                )
        except AssertionError as exc:
            failures.append(f"(c) {rel}: {exc}")
        try:
            slot = _only_line(
                lines,
                lambda l: _PLAN_SLOT in l and _is_slot_open(l),
                f"opening the {_PLAN_SLOT!r} slot",
            )
            if slot < start:
                failures.append(
                    f"(c) {rel}: the paragraph sits below the opening of the "
                    f"{_PLAN_SLOT!r} slot"
                )
        except AssertionError as exc:
            failures.append(f"(c) {rel}: {exc}")
        if any(_is_slot_open(l) or _is_slot_end(l) for l in region):
            failures.append(f"(c) {rel}: the paragraph holds a slot marker")
        if _inside_a_slot(lines, start):
            failures.append(f"(c) {rel}: the paragraph sits inside a slot")

    for rel in _PROMISE_SITES:
        try:
            text = _collapse("\n".join(_read(rel))).lower()
        except OSError as exc:
            failures.append(f"(d) {rel}: cannot be read: {exc}")
            continue
        if _CHECK_NAME.lower() not in text:
            failures.append(f"(d) {rel}: does not name the {_CHECK_NAME!r}")
        if rel == _PROMISE_SITES[0] and _COMPLEXITY_FINDING.lower() not in text:
            failures.append(
                f"(d) {rel}: does not say that {_COMPLEXITY_FINDING!r}"
            )

    assert not failures, "\n".join(failures)
