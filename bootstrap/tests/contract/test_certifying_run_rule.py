"""Tree certification stays separate, and the guard preserves conditional push wording.

A full run is evidence about a tree, not about one change, so the governing
text in every surface that defines verification preserves its triggers
(before a push when required, a gate-re-pinning ceremony, a release cut, or
when the Maintainer asks), without requiring a marker in each change record.
These tests keep that rule present in each surface, and keep
the broad-run guard from making a conditional push certification sound
automatic or handing out the full-suite override as a remedy.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]

SURFACES = (
    ROOT / "AGENTS.md",
    ROOT / "templates" / "core" / "AGENTS.md",
    ROOT / "docs" / "methodology" / "plans.md",
    ROOT / "docs" / "methodology" / "dual-review.md",
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
    assert "tree certification" in text or "certifying run" in text, path
    assert "Certified by: pending" not in text, path


def test_cairn_governing_rule_names_integration_points_and_ancestor_claim():
    text = _flat(SURFACES[0])
    for phrase in ("before a push", "before a release cut",
                   "when the Maintainer asks", "certifies every change at or before",
                   "bisect"):
        assert phrase in text, phrase


@pytest.mark.parametrize("path", SURFACES[1:3], ids=lambda p: str(p.relative_to(ROOT)))
def test_adopter_certification_limits_claim_and_reopens_contradictions(path):
    text = _flat(path)
    for phrase in ("tested commit", "components", "checks", "results", "omissions",
                   "unrelated", "untested combined", "earlier changes",
                   "later failure contradicts"):
        assert phrase in text, (path, phrase)
    assert "before a release cut" not in text
    assert "Required project checks and ceremonies remain owed" in text


@pytest.mark.parametrize("path", SURFACES[:2], ids=lambda p: str(p.relative_to(ROOT)))
def test_reviewers_are_told_never_to_run_the_full_suite(path):
    assert "The reviewer never runs the full suite." in _flat(path), path


def test_the_shipped_rule_names_no_cairn_only_command():
    text = _flat(ROOT / "templates" / "core" / "AGENTS.md")
    start = text.index("Change verification and tree certification are separate.")
    rule = text[start:start + 1600]
    for token in ("CAIRN_FULL_SUITE", "bootstrap/tests", "Python 3.13"):
        assert token not in rule, token


def test_the_broad_run_refusal_no_longer_offers_the_override():
    source = (ROOT / "bootstrap" / "tests" / "conftest.py").read_text(encoding="utf-8")
    body = source[source.index("def _refuse_broad_run_if_warranted"):]
    message = body[body.index("raise pytest.UsageError("):body.index("\n\n\n")]
    flattened = " ".join(message.lower().split())
    assert _push_certification_is_conditional(flattened)
    assert not re.search(r"set\s*\"?\s*f?\"?\{FULL_SUITE_ENV\}", message), (
        "the refusal must not tell the reader to set the override")

    unconditional = flattened.replace(
        "before a push, when required",
        "before a push",
    )
    assert not _push_certification_is_conditional(unconditional)
    assert "Record each actual run" in message


def test_cairn_keeps_its_own_certification_pair_and_triggers():
    text = _flat(ROOT / "AGENTS.md")
    assert "CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests" in text
    assert "python scripts/quality_gate.py --sub neutrality --sub redundancy" in text
    for trigger in ("before a push when required", "before re-anchor",
                    "before a release cut", "when the Maintainer asks"):
        assert trigger in text, trigger


def _push_certification_is_conditional(message: str) -> bool:
    return ("before a push, when required" in message
            and "pushing may require certification; ask the maintainer" in message)
