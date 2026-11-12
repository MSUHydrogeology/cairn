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
