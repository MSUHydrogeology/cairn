"""The full suite runs only as a certifying run, and the guard stops offering it.

A full run is evidence about a tree, not about one change, so the governing
text in every surface that defines verification says it is paid for once per
integration point (before a push, a gate-re-pinning ceremony, a release cut, or
when the Maintainer asks), and that a record cites it as ``Certified by``.
These tests keep that rule present in each surface, and keep the broad-run
guard's refusal from handing out the full-suite override as the remedy -- the
offer that turned an override into a habit.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

SURFACES = (
    ROOT / "AGENTS.md",
    ROOT / "templates" / "core" / "AGENTS.md",
    ROOT / "doctrine" / "plans.md",
    ROOT / "doctrine" / "dual-review.md",
    ROOT / "dev" / "plans" / "_template.md",
    ROOT / "templates" / "core" / "dev" / "plans" / "_template.md",
)

#: Surfaces that state the whole rule, not just point at it.
GOVERNING = SURFACES[:3]


def _flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


@pytest.mark.parametrize("path", SURFACES, ids=lambda p: str(p.relative_to(ROOT)))
def test_every_verification_surface_says_the_full_suite_is_a_certifying_run(path):
    text = _flat(path)
    assert ("runs only as a certifying run" in text
            or "never runs the full suite" in text), path
    assert "Certified by" in text, path


@pytest.mark.parametrize("path", GOVERNING, ids=lambda p: str(p.relative_to(ROOT)))
def test_the_governing_rule_names_its_integration_points_and_its_failure_path(path):
    text = _flat(path)
    for phrase in ("before a push", "before a release cut",
                   "when the Maintainer asks", "certifies every change at or before",
                   "bisect"):
        assert phrase in text, (path, phrase)


@pytest.mark.parametrize("path", SURFACES[:2], ids=lambda p: str(p.relative_to(ROOT)))
def test_reviewers_are_told_never_to_run_the_full_suite(path):
    assert "The reviewer never runs the full suite." in _flat(path), path


def test_the_shipped_rule_names_no_cairn_only_command():
    text = _flat(ROOT / "templates" / "core" / "AGENTS.md")
    start = text.index("The full suite runs only as a certifying run.")
    rule = text[start:start + 1600]
    for token in ("CAIRN_FULL_SUITE", "bootstrap/tests", "Python 3.13"):
        assert token not in rule, token


def test_the_broad_run_refusal_no_longer_offers_the_override():
    source = (ROOT / "bootstrap" / "tests" / "conftest.py").read_text(encoding="utf-8")
    body = source[source.index("def _refuse_broad_run_if_warranted"):]
    message = body[body.index("raise pytest.UsageError("):body.index("\n\n\n")]
    assert "certifying run" in message
    assert not re.search(r"set\s*\"?\s*f?\"?\{FULL_SUITE_ENV\}", message), (
        "the refusal must not tell the reader to set the override")
