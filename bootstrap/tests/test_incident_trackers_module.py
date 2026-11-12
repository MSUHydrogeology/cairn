"""Tests for the `incident-trackers` default-on module
(Proposal C: fold-back-incident-trackers).

Promises:
- A default install with no modules key installs the incident-trackers
  doctrine, the tracker template and the archive marker under dev/modules/.
- A default install creates the dev/strategy folder and its archive folder.
- A profile whose modules list omits incident-trackers installs none of its
  files.
- A repeat install leaves the adopter's own archive note unchanged.
- An install refuses a linked archive parent and writes nothing through the
  link.
- An upgrade with --adopt-module incident-trackers delivers the archive home.
- A dry run names the module and writes no archive marker.
- The installed tracker template carries the canonical columns, the three
  Impact values and the three Resolved By forms.

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
ARCHIVE_MARKER_DST = "dev/measurement/archive/.gitkeep"

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


    def test_manifest_and_dry_run_include_archive_marker(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        from bootstrap.scaffold import install_manifest  # noqa: PLC0415

        manifest = install_manifest(modules=[MODULE])
        assert (
            "modules/default-on/measurement-archive/.gitkeep",
            ARCHIVE_MARKER_DST,
            True,
        ) in manifest

        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: IncidentTrackersTest\ntest_command: pytest\n"
            f"modules:\n  - {MODULE}\n",
            encoding="utf-8",
        )
        assert main([
            "--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--dry-run",
        ]) == 0
        assert "incident-trackers" in capsys.readouterr().out
        assert not (tmp_path / ARCHIVE_MARKER_DST).exists()


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
        assert (tmp_path / ARCHIVE_MARKER_DST).is_file()
        module_text = (tmp_path / MODULE_DOC_DST).read_text(encoding="utf-8")
        assert "Same-file sweeps require human confirmation" in module_text
        assert "reporting is complete" in module_text

    def test_default_install_scaffolds_strategy_dirs(
        self, tmp_path: Path,
    ) -> None:
        """Sharpened at commit 96b7fba: the
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
        assert not (tmp_path / ARCHIVE_MARKER_DST).exists()

    def test_repeat_install_preserves_adopter_archive_content(
        self, tmp_path: Path,
    ) -> None:
        assert _scaffold(tmp_path, [MODULE]) == 0
        marker = tmp_path / ARCHIVE_MARKER_DST
        marker.write_text("adopter archive note\n", encoding="utf-8")

        assert _scaffold(tmp_path, [MODULE]) == 0
        assert marker.read_text(encoding="utf-8") == "adopter archive note\n"

    def test_linked_archive_parent_refuses_without_escaping(
        self, tmp_path: Path,
    ) -> None:
        target = tmp_path / "target"
        measurement = target / "dev" / "measurement"
        measurement.mkdir(parents=True)
        outside = tmp_path / "outside"
        outside.mkdir()
        (measurement / "archive").symlink_to(outside, target_is_directory=True)

        from bootstrap._scaffold.security import (  # noqa: PLC0415
            ScaffoldSecurityError,
        )

        with pytest.raises(ScaffoldSecurityError, match="symlinked parent"):
            _scaffold(target, [MODULE])
        assert not (outside / ".gitkeep").exists()

    def test_explicit_adoption_delivers_archive_home(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, ["reflections"]) == 0
        marker = tmp_path / ARCHIVE_MARKER_DST
        assert not marker.exists()

        assert main([
            "upgrade", "--target", str(tmp_path), "--cairn-root",
            str(CAIRN_ROOT), "--adopt-module", MODULE,
        ]) == 0
        assert marker.is_file()


# ---------------------------------------------------------------------------
# Content fidelity: canonical schema + sweep evidence + Impact values
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
            "Commit",
            "Affected Paths",
            "Discovery Date",
            "Confirmation Reference",
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
