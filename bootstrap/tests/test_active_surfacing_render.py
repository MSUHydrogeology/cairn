"""Tests for per-preset active-surfacing prompt content rendering.

Plan: 2026-05-28-claude-cairn-progressive-onboarding.

Validates every combination of active-surfacing row and preset.  For
each combination:

* The prompt content extracted from the preset source file is
  non-empty.
* The content includes the per-preset distinguishing language
  named in the plan + the doctrine (the maintainer-judgment
  content review surface).

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
    """The surviving row and a prefix-named stand-in render differently.

    The matcher accepts a label that begins with the row name, so a row
    whose name is a prefix of another row's label would capture that
    row's body and still look healthy to a non-empty check.
    """
    source = _preset_text(preset)
    real_heading = "### Row 1 -- second-agent-type spin-up prompt"
    standin_heading = "### Row 0 -- second-agent prompt"
    assert real_heading in source
    trial = source.replace(
        real_heading,
        f"{standin_heading}\n\nStand-in body for a prefix row.\n\n{real_heading}",
        1,
    )
    rows = (*ROWS, "second-agent")
    bodies = [helper.render_active_surfacing_prompt(trial, row) for row in rows]
    assert all(body is not None for body in bodies)
    assert len(set(bodies)) == len(bodies), f"two rows share a body in {preset}"
    # This changed heading makes both rows select the stand-in. The distinct
    # body assertion above must be capable of turning red on a bad fixture.
    broken = trial.replace(standin_heading, real_heading, 1)
    broken_bodies = [
        helper.render_active_surfacing_prompt(broken, row) for row in rows
    ]
    assert len(set(broken_bodies)) < len(broken_bodies)

# ---------------------------------------------------------------------------
# Every row x preset combination renders a non-empty body
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("preset", PRESETS)
@pytest.mark.parametrize("row", ROWS)
class TestEveryRowRendersForEveryPreset:
    def test_renders_non_empty_body(
        self, helper: ModuleType, preset: str, row: str,
    ) -> None:
        # The row name is passed exactly as the registry holds it --
        # the same value production passes.  An earlier version
        # substituted a hand-picked keyword for the row name, which made
        # this test green while the real row name matched no heading in
        # any preset.
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
# Per-preset distinguishing language
# ---------------------------------------------------------------------------


class TestPerPresetDistinguishingLanguage:
    """Each preset's prompt content includes the
    preset-distinguishing language named in the plan + doctrine.
    Surfaces drift between preset content + the spec."""

    def test_solo_greenfield_prompt_names_solo_deployment(
        self, helper: ModuleType,
    ) -> None:
        body = helper.render_active_surfacing_prompt(
            _preset_text("solo-greenfield"), "second-agent-type",
        )
        assert body is not None
        lowered = body.lower()
        assert "your solo deployment" in lowered

    def test_collaborative_team_prompt_names_expected_multi_agent_shape(
        self, helper: ModuleType,
    ) -> None:
        body = helper.render_active_surfacing_prompt(
            _preset_text("collaborative-team"), "second-agent-type",
        )
        assert body is not None
        lowered = body.lower()
        assert "collaborative-team profile expects multi-agent" in lowered

    def test_high_rigor_legacy_prompt_names_security_staffing(
        self, helper: ModuleType,
    ) -> None:
        body = helper.render_active_surfacing_prompt(
            _preset_text("high-rigor-legacy"), "second-agent-type",
        )
        assert body is not None
        lowered = body.lower()
        assert "security-review module's bar" in lowered
