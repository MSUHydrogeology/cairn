"""Tests for per-preset active-surfacing prompt content rendering.

Plan: 2026-05-28-claude-cairn-progressive-onboarding.

Validates the 9 fixture combinations (3 active-surfacing rows ×
3 presets).  For each combination:

* The prompt content extracted from the preset source file is
  non-empty.
* The content includes the per-preset distinguishing language
  named in the plan + the doctrine (the maintainer-judgment
  content review surface).

Per Codex External Review P3-9: the Level-1->2 prompts MUST be
drafted concretely (not hand-wavy); each preset's variant is
asserted to include preset-specific guidance.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_active_surfacing_render.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
HELPER_SRC = (
    CAIRN_ROOT
    / "templates"
    / "modules"
    / "default-on"
    / "onboarding_activate.py"
)
ONBOARDING_DIR = CAIRN_ROOT / "templates" / "onboarding"

pytestmark = pytest.mark.skipif(
    not HELPER_SRC.exists() or not ONBOARDING_DIR.exists(),
    reason="onboarding source files not available",
)


def _load_helper() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "_onboarding_activate_under_test_surfacing_content", HELPER_SRC,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["_onboarding_activate_under_test_surfacing_content"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def helper() -> ModuleType:
    return _load_helper()


PRESETS = ("solo-greenfield", "collaborative-team", "high-rigor-legacy")
ROWS = (
    "collab-agreement-signing",
    "Level-1-to-2-graduation",
    "second-agent-type",
)


def _preset_text(preset: str) -> str:
    return (ONBOARDING_DIR / f"{preset}.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# The 12 fixture combinations: each renders a non-empty body
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("preset", PRESETS)
@pytest.mark.parametrize("row", ROWS)
class TestTwelveCombinations:
    def test_renders_non_empty_body(
        self, helper: ModuleType, preset: str, row: str,
    ) -> None:
        # Match the heading slug used in the preset files:
        # "collab-agreement-signing", "Level 1->2 graduation",
        # "second-agent-type spin-up".
        # The render helper matches case-insensitive substring, so
        # passing the row name above works against the actual heading
        # text in each preset file IF the heading mentions the
        # relevant keyword.  Below we pass a normalized row keyword.
        keyword_for_row = {
            "collab-agreement-signing": "collab-agreement-signing",
            "Level-1-to-2-graduation": "Level 1",
            "second-agent-type": "second-agent",
        }[row]
        body = helper.render_active_surfacing_prompt(
            _preset_text(preset), keyword_for_row,
        )
        assert body is not None, (
            f"prompt content missing for preset={preset} row={row}"
        )
        assert len(body) > 20, (
            f"prompt content too short for preset={preset} row={row}: "
            f"{body!r}"
        )


# ---------------------------------------------------------------------------
# Per-preset distinguishing language (Codex P3-9: Level-1->2
# variants must be concretely drafted, not hand-wavy)
# ---------------------------------------------------------------------------


class TestPerPresetDistinguishingLanguage:
    """Each preset's prompt content includes the
    preset-distinguishing language named in the plan + doctrine.
    Surfaces drift between preset content + the spec."""

    def test_solo_greenfield_collab_agreement_says_you_are_team(
        self, helper: ModuleType,
    ) -> None:
        body = helper.render_active_surfacing_prompt(
            _preset_text("solo-greenfield"), "collab-agreement-signing",
        )
        assert body is not None
        # The solo-greenfield variant frames the team-roster fill as
        # "no multi-party negotiation -- you're the team."
        lowered = body.lower()
        assert "you're the team" in lowered or "your own name" in lowered

    def test_collaborative_team_collab_agreement_invokes_negotiation(
        self, helper: ModuleType,
    ) -> None:
        body = helper.render_active_surfacing_prompt(
            _preset_text("collaborative-team"), "collab-agreement-signing",
        )
        assert body is not None
        lowered = body.lower()
        # Multi-party negotiation language is the collaborative-team
        # marker.
        assert "negotiate" in lowered

    def test_high_rigor_legacy_collab_agreement_confirms_existing_maintainer(
        self, helper: ModuleType,
    ) -> None:
        body = helper.render_active_surfacing_prompt(
            _preset_text("high-rigor-legacy"), "collab-agreement-signing",
        )
        assert body is not None
        lowered = body.lower()
        # Existing-maintainer authority confirmation is the
        # high-rigor-legacy marker.
        assert "existing maintainer" in lowered or "pre-existing" in lowered

    def test_level_graduation_drafts_concrete_per_preset_p3_9(
        self, helper: ModuleType,
    ) -> None:
        """Codex P3-9 disposition: each preset's Level-1->2 prompt is
        a concrete paragraph, NOT hand-wavy.  Assert each variant
        names a concrete action (walk a specific doc, coordinate
        with maintainer, etc.)."""
        for preset in PRESETS:
            body = helper.render_active_surfacing_prompt(
                _preset_text(preset), "Level 1",
            )
            assert body is not None, (
                f"Level 1->2 prompt missing for preset={preset}"
            )
            lowered = body.lower()
            # Every variant references BOOTSTRAP.md (the concrete
            # action surface for the Level-2 graduation).
            assert "bootstrap.md" in lowered, (
                f"Level 1->2 prompt for {preset} lacks concrete "
                f"action reference to BOOTSTRAP.md (Codex P3-9): "
                f"{body!r}"
            )
