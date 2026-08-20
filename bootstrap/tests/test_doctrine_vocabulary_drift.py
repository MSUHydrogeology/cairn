"""Doctrine must not teach a status vocabulary the tool refuses.

The lifecycle status vocabulary is owned by ``lifecycle_planner``. When a token
is retired there, every place that *teaches* the vocabulary has to follow, and
`doctrine/` is where a reader goes for the deeper why. Nothing detected the last
divergence: the retirement landed in the operational files, the templates, the
planner and the metrics extractors, and five doctrine files went on describing
the retired set for ten days while the tool refused it.

Prose has no type-checker, so this is the type-checker: the retired tokens are
read from the planner rather than hand-listed here, which means a *future*
retirement is covered the day it lands without anyone remembering to widen a
list.

Naming a retired token as history is legitimate and stays possible -- mark the
passage and say why.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
_PLANNER_PATH = (
    CAIRN_ROOT / "templates" / "skills" / "_lib" / "lifecycle_planner.py"
)

#: A passage may name the retired vocabulary if it says so. The marker exempts
#: from its own line until the next blank line -- a Markdown paragraph -- so an
#: exemption cannot silently widen to the rest of the file.
MARKER = "retired-vocabulary-ok:"


def _load_planner() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "cairn_planner_for_drift", _PLANNER_PATH
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["cairn_planner_for_drift"] = module
    spec.loader.exec_module(module)
    return module


def _retired_tokens() -> tuple[str, ...]:
    planner = _load_planner()
    return tuple(planner.HISTORICAL_PROPOSAL_STATES) + tuple(
        planner.HISTORICAL_PLAN_STATES
    )


def _exempt_lines(lines: list[str]) -> set[int]:
    """Line numbers (1-based) covered by a marker, to the next blank line."""
    exempt: set[int] = set()
    for i, line in enumerate(lines):
        if MARKER not in line:
            continue
        for j in range(i, len(lines)):
            if j > i and not lines[j].strip():
                break
            exempt.add(j + 1)
    return exempt


def _fenced_diagram_lines(lines: list[str]) -> set[int]:
    """Line numbers (1-based) inside a ```mermaid fence.

    A diagram states the vocabulary as loudly as prose does and is the surface
    that actually drifted, but its tokens are bare graph labels -- never
    backticked -- so the prose rule below cannot see them at all.
    """
    inside = False
    out: set[int] = set()
    for n, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if inside:
                inside = False
            elif stripped[3:].strip().lower() == "mermaid":
                inside = True
            continue
        if inside:
            out.add(n)
    return out


def _offenders(text: str, tokens: tuple[str, ...]) -> list[tuple[int, str]]:
    """Retired status tokens presented as current, as (line, token).

    Two surfaces, two rules, because the token looks different on each.
    """
    lines = text.splitlines()
    exempt = _exempt_lines(lines)
    diagram = _fenced_diagram_lines(lines)

    # Prose: backticked whole spans only. "open", "review" and "revised" are
    # ordinary English, so flagging bare prose would drown the signal; a token
    # presented as `code` is being presented as a status name. Whole-span only
    # because substring matching flags `Plan review` and `plan-review`, which are
    # section names -- and that is how a check earns the reputation that gets it
    # deleted. A span may hold a status *list* (`proposed / open / executing /
    # review`), so split on the list separators and require each part to match.
    span_re = re.compile(r"`([^`]+)`")

    # Diagrams: whole-word, since graph labels carry no backticks. The lookarounds
    # exclude word characters AND hyphens, so `review` does not match inside
    # `awaiting-code-review` -- without that, every live state ending in a retired
    # word would report as drift.
    word_res = {
        tok: re.compile(rf"(?<![\w-]){re.escape(tok)}(?![\w-])") for tok in tokens
    }

    found: list[tuple[int, str]] = []
    for n, line in enumerate(lines, start=1):
        if n in exempt:
            continue
        if n in diagram:
            for tok, rx in word_res.items():
                if rx.search(line):
                    found.append((n, tok))
            continue
        for span in span_re.findall(line):
            parts = [p.strip() for p in re.split(r"[/,]", span)]
            if not parts or not all(parts):
                continue
            for part in parts:
                if part in tokens:
                    found.append((n, part))
    return found


class TestDoctrineTeachesTheLiveVocabulary:
    def test_the_retired_set_is_read_from_the_tool_not_hardcoded(self) -> None:
        """A hand-listed denylist goes stale exactly when it matters -- at the
        next retirement. Read it from the vocabulary owner instead."""
        tokens = _retired_tokens()
        assert tokens, "the planner exposes no historical vocabulary to check against"
        planner = _load_planner()
        live = set(planner.PROPOSAL_STATES) | set(planner.PLAN_STATES)
        assert not (set(tokens) & live), (
            "a token is both live and historical; the two groups must stay disjoint "
            "or this check cannot tell drift from current usage"
        )

    @pytest.mark.parametrize(
        "path",
        sorted((CAIRN_ROOT / "doctrine").glob("*.md")) + [CAIRN_ROOT / "README.md"],
        ids=lambda p: p.name,
    )
    def test_no_doctrine_file_presents_a_retired_status_as_current(
        self, path: Path
    ) -> None:
        """README.md is checked alongside doctrine because it carries a
        *simplification* of the lifecycle diagram, and a simplification is a
        second drawing rather than a second view of one source. It may leave
        states out; it may never name one that no longer exists. That is exactly
        how it failed before -- the front page kept the retired tokens after the
        vocabulary moved, under a caption asserting fidelity to doctrine.

        This binds the state *names* only. A simplification could still invent a
        transition doctrine does not have, and nothing here would notice; that
        needs a reader, and the caption is where the claim is made.
        """
        offenders = _offenders(path.read_text(encoding="utf-8"), _retired_tokens())
        assert not offenders, (
            f"{path.relative_to(CAIRN_ROOT)} presents retired status token(s) as "
            f"current: {offenders}. Either update the passage to the live "
            f"vocabulary, or -- if it names the retired set deliberately as "
            f"history -- mark the paragraph with an HTML comment carrying "
            f"'{MARKER} <reason>'."
        )

    def test_the_check_can_actually_fail(self) -> None:
        """Confirm the instrument before trusting its silence: a synthetic
        passage carrying a retired token must be caught, and the same passage
        under a marker must not be."""
        tokens = _retired_tokens()
        bare = "The plan moves to `executing` once work starts.\n"
        assert _offenders(bare, tokens), "the detector missed a retired token"

        marked = (
            f"<!-- {MARKER} naming the retired set as history -->\n"
            "The plan moves to `executing` once work starts.\n"
            "\n"
            "The plan moves to `executing` once work starts.\n"
        )
        found = _offenders(marked, tokens)
        assert [n for n, _ in found] == [4], (
            "the marker must exempt its own paragraph and nothing beyond the "
            f"next blank line; got {found}"
        )

    def test_the_check_sees_inside_a_diagram(self) -> None:
        """The prose rule is blind to diagrams, which is the surface that
        actually drifted: the README's Mermaid nodes carried the retired tokens
        for ten days and no backtick appears anywhere in a Mermaid block. A
        README-scoped check that only read prose would have passed the exact
        failure it was added for -- green, and blind."""
        tokens = _retired_tokens()
        drifted = "```mermaid\nflowchart LR\n    P[proposed] --> R[reviewed]\n```\n"
        assert _offenders(drifted, tokens), "the detector cannot see into a diagram"

        live = (
            "```mermaid\nflowchart LR\n"
            "    A[awaiting-review] --> B[awaiting-code-review]\n```\n"
        )
        assert not _offenders(live, tokens), (
            "a live state ending in a retired word (awaiting-code-review) must "
            "not report as drift"
        )
