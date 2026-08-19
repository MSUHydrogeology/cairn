"""Tests for the `documentation-plan` default-on module
(Proposal D: fold-back-documentation-plan).

Covers:
* Registration: the module is in `_DEFAULT_ON_MODULES` and
  carries an `_MODULE_MAPPINGS` entry.
* Install path: a default scaffold installs both the module
  doctrine + the forkable at the canonical destinations
  (`dev/modules/documentation-plan.md` +
  `docs/DOCUMENTATION_PLAN.md`).
* Content fidelity: the forkable carries the four-layer vision
  (entry / governing / deliberation / descriptive), the decision
  procedure, voice rules, and uses adopter-relative paths only
  (no `cairn/` prefix in worked examples).
* Slot anchors: the three core templates carry the expected slot
  anchor names (`documentation-discipline` in core AGENTS.md,
  `documentation-tier-home` in proposals + plans templates).
* Merged-into blocks: the module file ships three named blocks
  (Block 1 / 2 / 3) carrying the slot-fill content for adopters
  (or agents) to paste. Mechanical merge via Proposal B's
  `cairn:merge-target` directives is **deferred** pending
  resolution of the lockfile-divergence interaction (a separate
  Cairn follow-up).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_documentation_plan_module.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    _DEFAULT_ON_MODULES,
    _MODULE_MAPPINGS,
    main,
)

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"

MODULE = "documentation-plan"
MODULE_DOC_DST = "dev/modules/documentation-plan.md"
FORKABLE_DST = "docs/DOCUMENTATION_PLAN.md"

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available",
)


def _scaffold(target: Path, modules: list[str] | None) -> int:
    cfg = target / "profile.yml"
    body = "project_name: DocumentationPlanTest\ntest_command: pytest\n"
    if modules is not None:
        body += "modules:\n" + "".join(f"  - {m}\n" for m in modules)
    cfg.write_text(body)
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT),
         "--non-interactive"]
    )


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


class TestRegistration:
    def test_module_is_default_on(self) -> None:
        assert MODULE in _DEFAULT_ON_MODULES

    def test_module_mapping_targets(self) -> None:
        specs = _MODULE_MAPPINGS[MODULE]
        dsts = {s.dst for s in specs}
        assert MODULE_DOC_DST in dsts
        assert FORKABLE_DST in dsts

    def test_forkable_installs_to_docs_root(self) -> None:
        """Forkable installs directly at adopter docs/, not into
        dev/modules/ (where the module doctrine lands)."""
        specs = _MODULE_MAPPINGS[MODULE]
        forkable = next(
            (s for s in specs if s.dst == FORKABLE_DST), None,
        )
        assert forkable is not None, (
            f"Forkable spec installing to {FORKABLE_DST!r} not found"
        )
        # The forkable is NOT installed into dev/modules/ -- it lands
        # directly at the adopter's docs/ root.
        assert not forkable.dst.startswith("dev/modules/")


# ---------------------------------------------------------------------------
# Install path
# ---------------------------------------------------------------------------


class TestInstallPath:
    def test_default_install_includes_module(self, tmp_path: Path) -> None:
        """A profile that omits `modules:` installs the default-on
        set, which now includes documentation-plan."""
        assert _scaffold(tmp_path, None) == 0
        assert (tmp_path / MODULE_DOC_DST).is_file()
        assert (tmp_path / FORKABLE_DST).is_file()

    def test_omission_path(self, tmp_path: Path) -> None:
        """A pinned `modules:` list without documentation-plan leaves
        both artifacts uninstalled."""
        assert _scaffold(tmp_path, ["reflections"]) == 0
        assert not (tmp_path / MODULE_DOC_DST).exists()
        assert not (tmp_path / FORKABLE_DST).exists()


# ---------------------------------------------------------------------------
# Content fidelity: four-layer vision + adopter-relative paths
# ---------------------------------------------------------------------------


class TestForkableContent:
    def test_forkable_carries_four_layer_vision(
        self, tmp_path: Path,
    ) -> None:
        assert _scaffold(tmp_path, [MODULE]) == 0
        text = (tmp_path / FORKABLE_DST).read_text(encoding="utf-8")
        # The four layers must be named, by canonical name.
        for layer in (
            "Entry layer",
            "Governing layer",
            "Deliberation layer",
            "Descriptive layer",
        ):
            assert layer in text, (
                f"forkable docs/DOCUMENTATION_PLAN.md missing "
                f"canonical layer name {layer!r}"
            )

    def test_forkable_carries_decision_procedure(
        self, tmp_path: Path,
    ) -> None:
        assert _scaffold(tmp_path, [MODULE]) == 0
        text = (tmp_path / FORKABLE_DST).read_text(encoding="utf-8")
        # The decision procedure section is the load-bearing core.
        assert "## The decision procedure" in text
        # The procedure's three substantive routing rules.
        assert "Cross-cutting prescription" in text
        assert "Deliberating what to build" in text
        assert "Describing the software as it exists today" in text

    def test_forkable_uses_adopter_relative_paths(
        self, tmp_path: Path,
    ) -> None:
        """The forkable ships to adopters -- every path in its
        worked examples must be adopter-relative (no `cairn/`
        prefix).  This is the check's primary
        guarantee."""
        assert _scaffold(tmp_path, [MODULE]) == 0
        text = (tmp_path / FORKABLE_DST).read_text(encoding="utf-8")
        # No `cairn/` prefix anywhere in the forkable's content.
        # (The string `cairn` may appear in "Cairn module" prose;
        # the specific failure mode is path-prefix leakage like
        # `cairn/doctrine/`, `cairn/templates/`, `cairn/docs/`.)
        for leaked in (
            "cairn/doctrine/",
            "cairn/templates/",
            "cairn/docs/",
            "cairn/dev/",
            "cairn/bootstrap/",
            "cairn/scripts/",
        ):
            assert leaked not in text, (
                f"forkable docs/DOCUMENTATION_PLAN.md leaks "
                f"cairn-framework-internal path prefix {leaked!r} -- "
                f"adopters do not have a `cairn/` directory at their "
                f"tree root (Antigravity P1)"
            )

    def test_forkable_carries_agents_boundary_doctrine(
        self, tmp_path: Path,
    ) -> None:
        """The forkable carries the `AGENTS.md` ↔
        `agent_collaboration.md` boundary doctrine -- one of the
        load-bearing routing rules the procedure ships."""
        assert _scaffold(tmp_path, [MODULE]) == 0
        text = (tmp_path / FORKABLE_DST).read_text(encoding="utf-8")
        assert "AGENTS.md" in text
        assert "agent_collaboration.md" in text
        # The boundary section's canonical heading.
        assert "boundary" in text.lower()


# ---------------------------------------------------------------------------
# Cairn-self-hosted instance: dogfood
# ---------------------------------------------------------------------------


class TestCairnSelfHosted:
    def test_cairn_dogfoods_the_module(self) -> None:
        """Cairn IS its own first adopter -- the self-hosted
        instance lives at `cairn/docs/DOCUMENTATION_PLAN.md` and
        discusses Cairn's actual file inventory (cairn-prefixed
        paths)."""
        self_hosted = CAIRN_ROOT / "docs" / "DOCUMENTATION_PLAN.md"
        assert self_hosted.is_file(), (
            "Cairn self-hosted DOCUMENTATION_PLAN.md is missing -- "
            "the dogfood instance is part of the module's "
            "two-artifact contract"
        )
        text = self_hosted.read_text(encoding="utf-8")
        # The self-hosted instance uses cairn-prefixed paths in its
        # worked examples (the inverse of the forkable's check).
        assert "cairn/doctrine/" in text, (
            "Cairn self-hosted instance should discuss "
            "cairn/doctrine/ in worked examples"
        )
        assert "cairn/templates/core/" in text, (
            "Cairn self-hosted instance should discuss "
            "cairn/templates/core/ in worked examples"
        )


# ---------------------------------------------------------------------------
# Slot anchors: the three core templates carry the expected slots
# ---------------------------------------------------------------------------


class TestSlotAnchors:
    def test_core_agents_has_documentation_discipline_slot(
        self,
    ) -> None:
        text = (TEMPLATES_ROOT / "core" / "AGENTS.md").read_text(
            encoding="utf-8",
        )
        assert "<!-- cairn:slot documentation-discipline -->" in text
        assert "<!-- cairn:end documentation-discipline -->" in text

    def test_proposals_template_has_tier_home_slot(self) -> None:
        text = (
            TEMPLATES_ROOT / "core" / "dev" / "proposals" / "_template.md"
        ).read_text(encoding="utf-8")
        assert "<!-- cairn:slot documentation-tier-home -->" in text
        assert "<!-- cairn:end documentation-tier-home -->" in text

    def test_plans_template_has_tier_home_slot(self) -> None:
        text = (
            TEMPLATES_ROOT / "core" / "dev" / "plans" / "_template.md"
        ).read_text(encoding="utf-8")
        assert "<!-- cairn:slot documentation-tier-home -->" in text
        assert "<!-- cairn:end documentation-tier-home -->" in text


# ---------------------------------------------------------------------------
# Merged-into blocks: paste-into-slot content for the three slots
# ---------------------------------------------------------------------------


class TestMergedIntoBlocks:
    """The module ships three `Merged into:` blocks (one per slot)
    that adopters paste into the named target file.  Mechanical
    merge via Proposal B's `cairn:merge-target` machinery is
    deferred pending resolution of the helper's interaction with
    the install-lockfile divergence check (a separate Cairn
    follow-up tracked alongside this plan)."""

    def _module_text(self) -> str:
        return (
            TEMPLATES_ROOT / "modules" / "default-on"
            / "documentation-plan.md"
        ).read_text(encoding="utf-8")

    def test_module_names_three_blocks_by_target_and_slot(self) -> None:
        text = self._module_text()
        # Each block's heading names its (target, slot) tuple.
        assert "Block 1: `AGENTS.md` -- slot `documentation-discipline`" in text
        assert (
            "Block 2: `dev/proposals/_template.md` -- slot "
            "`documentation-tier-home`"
        ) in text
        assert (
            "Block 3: `dev/plans/_template.md` -- slot "
            "`documentation-tier-home`"
        ) in text

    def test_each_block_references_documentation_plan(self) -> None:
        """Each `Merged into:` block carries a cross-reference to
        `docs/DOCUMENTATION_PLAN.md` (the forkable install path)."""
        text = self._module_text()
        # `docs/DOCUMENTATION_PLAN.md` appears in all three blocks.
        # Count >= 3 since each block references it at least once.
        assert text.count("docs/DOCUMENTATION_PLAN.md") >= 3
