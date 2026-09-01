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
def _registry_rows() -> tuple[str, ...]:
    """Row names exactly as the shipped registry declares them.

    Derived, never transcribed: a hand-copied list drifts from the
    registry silently, and every combination below would keep passing
    against names production no longer uses.
    """
    if not HELPER_SRC.exists():
        return ()
    try:
        return tuple(
            row for row, _trigger in _load_helper()._ACTIVE_SURFACING_ROWS
        )
    except Exception:
        # An engine that fails to import must not abort collection for the
        # entire suite; the non-vacuity test below reports it readably.
        return ()


ROWS = _registry_rows()


def _preset_text(preset: str) -> str:
    return (ONBOARDING_DIR / f"{preset}.md").read_text(encoding="utf-8")


def test_the_row_registry_is_not_empty(helper: ModuleType) -> None:
    """Refuse to pass vacuously.

    Every combination test below is parametrized over ROWS.  If the
    registry could not be read, ROWS is empty, pytest generates no
    cases, and the whole file reports green having checked nothing.
    """
    registry = tuple(row for row, _trigger in helper._ACTIVE_SURFACING_ROWS)
    assert registry, "the shipped registry declares no active-surfacing rows"
    assert ROWS == registry, (
        f"ROWS drifted from the registry: {ROWS!r} != {registry!r}"
    )


@pytest.mark.parametrize("preset", PRESETS)
def test_each_row_renders_a_distinct_body(
    helper: ModuleType, preset: str,
) -> None:
    """Two rows must never resolve to the same heading.

    The matcher accepts a label that begins with the row name, so a row
    whose name is a prefix of another row's label would capture that
    row's body and still look healthy to a non-empty check.
    """
    bodies = {
        row: helper.render_active_surfacing_prompt(_preset_text(preset), row)
        for row in ROWS
    }
    rendered = [b for b in bodies.values() if b is not None]
    assert len(set(rendered)) == len(rendered), (
        f"two rows share a body in preset={preset}: "
        f"{ {r: (b or '')[:40] for r, b in bodies.items()} }"
    )

# ---------------------------------------------------------------------------
# The 12 fixture combinations: each renders a non-empty body
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("preset", PRESETS)
@pytest.mark.parametrize("row", ROWS)
class TestTwelveCombinations:
    def test_renders_non_empty_body(
        self, helper: ModuleType, preset: str, row: str,
    ) -> None:
        # The row name is passed exactly as the registry holds it --
        # the same value production passes.  An earlier version
        # substituted a hand-picked keyword here ("Level 1" for
        # "Level-1-to-2-graduation"), which made this test green while
        # the real row name matched no heading in any preset.
        body = helper.render_active_surfacing_prompt(
            _preset_text(preset), row,
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
            graduation_row = next(
                row for row, trigger in helper._ACTIVE_SURFACING_ROWS
                if trigger == "level-1-to-2"
            )
            body = helper.render_active_surfacing_prompt(
                _preset_text(preset), graduation_row,
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
