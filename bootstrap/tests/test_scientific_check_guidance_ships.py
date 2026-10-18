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

It also pins where the text sits. The block must come after the
security-preflight sub-block, whose slice another test compares byte for byte
between the two proposal templates: a block placed inside that slice would be
swallowed into it and no test would go red, because both copies grow alike.
Neither text may sit inside a slot, because an adopter who fills the slot
replaces everything in it.

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

_BLOCK_HEADING = "### Independent scientific check"
_PREFLIGHT_CLOSE = "**Prospective only.**"
_PLAN_LEAD = "**An independent scientific check is accepted scope.**"

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
    return " ".join(text.split())


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


def test_the_check_guidance_reaches_every_copy_and_promise_site() -> None:
    """Both proposal copies hold the block, both plan copies hold the paragraph,
    each word for word and outside every slot.

    The groups accumulate into one ``failures`` list rather than stopping at
    the first, so every group runs every time and a failure shows all of what
    is wrong at once.

    (a) the block, in each proposal copy, equals the reviewed text;
    (b) the paragraph, in each plan copy, equals the reviewed text;
    (c) placement: the block sits after the security-preflight sub-block, and
        neither text holds a slot marker or sits inside a slot.
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
        except AssertionError as exc:
            failures.append(f"(c) {rel}: {exc}")
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
        if any(_is_slot_open(l) or _is_slot_end(l) for l in region):
            failures.append(f"(c) {rel}: the paragraph holds a slot marker")
        if _inside_a_slot(lines, start):
            failures.append(f"(c) {rel}: the paragraph sits inside a slot")

    assert not failures, "\n".join(failures)
