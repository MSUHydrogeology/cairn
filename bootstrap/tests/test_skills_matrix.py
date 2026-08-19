"""Compatibility-matrix drift gate + auto-suppress / anti-semantic lint
(Chunk 7 of the executing plan `2026-06-01-claude-cairn-vendor-neutral-skills`).

* the committed ``docs/skills-compatibility.md`` matches the generator (it is
  generated, never hand-edited);
* every target row carries the ``auto_suppress`` dimension;
* the anti-semantic-description lint: targets that rely on a dry description to
  suppress auto-trigger (``mitigated`` / ``cli-backstop-only``) are backed by a
  SKILL.md whose description is genuinely anti-semantic;
* the matrix doc leaks no local path / token.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_skills_matrix.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import (  # noqa: E402
    load_vendor_targets,
    render_compatibility_matrix,
)

TEMPLATES_ROOT = CAIRN_ROOT / "templates"
MATRIX_DOC = CAIRN_ROOT / "docs" / "skills-compatibility.md"

pytestmark = pytest.mark.skipif(
    not (TEMPLATES_ROOT / "skills").exists(),
    reason="templates/skills not available",
)

_VALID_LEVELS = {
    "native-tested", "native-claimed-unverified", "manual-fallback", "unsupported",
}
_VALID_SUPPRESS = {
    "native-tested", "declared-flag", "mitigated", "cli-backstop-only",
}


def test_committed_matrix_matches_generator():
    expected = render_compatibility_matrix(TEMPLATES_ROOT)
    assert MATRIX_DOC.read_text(encoding="utf-8") == expected, (
        "docs/skills-compatibility.md is stale -- regenerate it with "
        "render_compatibility_matrix (it is generated, not hand-edited)."
    )


def test_every_row_has_valid_level_and_auto_suppress():
    for row in load_vendor_targets(TEMPLATES_ROOT):
        assert row.get("level") in _VALID_LEVELS, row
        assert row.get("auto_suppress") in _VALID_SUPPRESS, row


def test_anti_semantic_description_backs_non_native_suppression():
    # A target whose auto-trigger is only "mitigated" (or cli-backstop)
    # relies on a dry, anti-semantic description so chatter/vector search does
    # not fire the lifecycle.  Every skill description must satisfy that.
    relies_on_description = any(
        r.get("auto_suppress") in {"mitigated", "cli-backstop-only"}
        for r in load_vendor_targets(TEMPLATES_ROOT)
    )
    assert relies_on_description, "expected at least one mitigated target"
    for skill in sorted((TEMPLATES_ROOT / "skills").glob("*/SKILL.md")):
        head = skill.read_text(encoding="utf-8")
        desc_line = next(
            (ln for ln in head.splitlines() if ln.startswith("description:")), ""
        ).lower()
        assert "manual" in desc_line
        assert "not a conversational helper" in desc_line


def test_matrix_doc_has_no_local_path_leak():
    text = MATRIX_DOC.read_text(encoding="utf-8")
    assert "/Users/" not in text and "/home/" not in text
    assert not re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
