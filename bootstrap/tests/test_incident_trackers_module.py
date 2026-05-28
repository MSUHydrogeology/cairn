"""Tests for the `incident-trackers` default-on module
(Proposal C: fold-back-incident-trackers).

Covers:
* Registration: the module is in `_DEFAULT_ON_MODULES` and
  carries an `_MODULE_MAPPINGS` entry.
* Install path: a default scaffold installs both the module
  doctrine + the forkable tracker template at the canonical
  destinations under `dev/modules/`.
* Content fidelity: the forkable template carries the 7-column
  canonical schema header line + names the three `Impact` values
  (`occurred` / `prevented` / `non-conflict`).
* Cross-references: session-routines.md doctrine + rationale.md
  doctrine name the module's substrate role.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_incident_trackers_module.py
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

MODULE = "incident-trackers"
MODULE_DOC_DST = "dev/modules/incident-trackers.md"
TRACKER_TEMPLATE_DST = "dev/modules/incident_log_template.md"

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available",
)


def _scaffold(target: Path, modules: list[str] | None) -> int:
    cfg = target / "profile.yml"
    body = "project_name: IncidentTrackersTest\ntest_command: pytest\n"
    if modules is not None:
        body += "modules:\n" + "".join(f"  - {m}\n" for m in modules)
    cfg.write_text(body)
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT)]
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
        assert TRACKER_TEMPLATE_DST in dsts


# ---------------------------------------------------------------------------
# Install path
# ---------------------------------------------------------------------------


class TestInstallPath:
    def test_default_install_includes_module(self, tmp_path: Path) -> None:
        """A profile that omits `modules:` installs the default-on
        set, which now includes incident-trackers."""
        assert _scaffold(tmp_path, None) == 0
        assert (tmp_path / MODULE_DOC_DST).is_file()
        assert (tmp_path / TRACKER_TEMPLATE_DST).is_file()

    def test_default_install_scaffolds_strategy_dirs(
        self, tmp_path: Path,
    ) -> None:
        """Antigravity A-P3 (commit 96b7fba sharpening): the
        extended commit-permission exception covers
        `dev/strategy/`; the scaffold should create the directory
        by default so adopters who use the exception don't have
        to mkdir manually."""
        assert _scaffold(tmp_path, None) == 0
        assert (tmp_path / "dev" / "strategy").is_dir()
        assert (tmp_path / "dev" / "strategy" / "archive").is_dir()

    def test_omission_path(self, tmp_path: Path) -> None:
        """A pinned `modules:` list without incident-trackers leaves
        it uninstalled."""
        assert _scaffold(tmp_path, ["reflections"]) == 0
        assert not (tmp_path / MODULE_DOC_DST).exists()
        assert not (tmp_path / TRACKER_TEMPLATE_DST).exists()


# ---------------------------------------------------------------------------
# Content fidelity: canonical 7-column schema + 3 Impact values
# ---------------------------------------------------------------------------


class TestSchemaContract:
    def test_forkable_template_carries_canonical_schema(
        self, tmp_path: Path,
    ) -> None:
        assert _scaffold(tmp_path, [MODULE]) == 0
        text = (tmp_path / TRACKER_TEMPLATE_DST).read_text(
            encoding="utf-8",
        )
        # The canonical 7-column header.
        for column in (
            "Date",
            "Event Class",
            "Description",
            "Recurrence-Window Match",
            "Impact",
            "Migrated From Reflection",
            "Resolved By",
        ):
            assert column in text, (
                f"canonical column {column!r} missing from "
                f"forkable tracker template"
            )

    def test_template_names_three_impact_values(
        self, tmp_path: Path,
    ) -> None:
        assert _scaffold(tmp_path, [MODULE]) == 0
        text = (tmp_path / TRACKER_TEMPLATE_DST).read_text(
            encoding="utf-8",
        )
        for value in ("occurred", "prevented", "non-conflict"):
            assert value in text, (
                f"Impact value {value!r} missing from forkable "
                f"tracker template"
            )

    def test_template_names_resolved_by_three_forms(
        self, tmp_path: Path,
    ) -> None:
        """Resolved By accepts proposal-stem / commit-SHA / pending."""
        assert _scaffold(tmp_path, [MODULE]) == 0
        text = (tmp_path / TRACKER_TEMPLATE_DST).read_text(
            encoding="utf-8",
        )
        for form in ("Proposal stem", "Commit SHA", "pending"):
            assert form in text, (
                f"Resolved-By form {form!r} missing from forkable "
                f"tracker template"
            )


# ---------------------------------------------------------------------------
# Cross-references: doctrine surfaces name the module
# ---------------------------------------------------------------------------


class TestDoctrineCrossReferences:
    def test_rationale_md_names_trackers_module(self) -> None:
        rationale = (CAIRN_ROOT / "doctrine" / "rationale.md").read_text(
            encoding="utf-8",
        )
        assert "incident-trackers" in rationale, (
            "rationale.md rate-limit gate section should cross-reference "
            "the incident-trackers module (substrate)"
        )

    def test_session_routines_carries_migration_substep(self) -> None:
        sr = (CAIRN_ROOT / "doctrine" / "session-routines.md").read_text(
            encoding="utf-8",
        )
        assert "incident-trackers module is installed" in sr, (
            "session-routines.md should carry the goodnight migration "
            "sub-step for the incident-trackers module"
        )
