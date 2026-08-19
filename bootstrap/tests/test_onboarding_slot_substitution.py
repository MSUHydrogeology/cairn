"""
Tests for the progressive-onboarding scaffold integration.

Plan: 2026-05-28-claude-cairn-progressive-onboarding.

Covers per the Codex External plan-review (P1-1 + P2-4):

* `_extract_seed_tasks` parses seed list-items from preset
  onboarding files while excluding `[trigger:` deferred tasks and
  non-task prose (P1-1).
* The scaffold inlines **only** seed tasks plus a
  `<!-- preset: <name> -->` metadata comment into PLANNING's
  `onboarding-tasks` slot (P1-1 + P2-4).
* The scaffold also copies the full source onboarding file
  byte-for-byte to `dev/modules/onboarding/<preset>.md` -- the
  authoritative reference for goodnight deferred-task discovery
  (P1-1).
* A profile without `preset:` (explicit-modules path) yields no
  onboarding install (the slot remains its empty placeholder).
* `--dry-run` reports the planned onboarding install without
  writing.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_onboarding_slot_substitution.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    _ONBOARDING_PRESETS,
    _extract_seed_tasks,
    _render_onboarding_slot,
    _substitute_slot,
    main,
)

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
ONBOARDING_TEMPLATES = TEMPLATES_ROOT / "onboarding"

# The three preset onboarding files the scaffold ships.  They start
# as placeholders and are filled with real content later.  Either way
# the seed/deferred distinction holds.
PRESETS = ("solo-greenfield", "collaborative-team", "high-rigor-legacy")


pytestmark = pytest.mark.skipif(
    not ONBOARDING_TEMPLATES.exists(),
    reason="Cairn onboarding templates not available",
)


def _scaffold(target: Path, preset: str | None) -> int:
    """Scaffold into *target* via the real CLI.

    *preset* None -> no `preset:` key (explicit-modules path);
    a string -> `preset: <name>`.
    """
    cfg = target / "profile.yml"
    body = "project_name: OnboardingTest\ntest_command: pytest\n"
    if preset is None:
        body += "modules:\n  - reflections\n"  # explicit-modules path
    else:
        body += f"preset: {preset}\n"
    cfg.write_text(body)
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT)]
    )


# ---------------------------------------------------------------------------
# Registration: the three named presets are first-class
# ---------------------------------------------------------------------------


class TestRegistration:
    def test_three_named_presets_registered(self) -> None:
        assert _ONBOARDING_PRESETS == set(PRESETS)

    @pytest.mark.parametrize("preset", PRESETS)
    def test_each_preset_source_file_exists(self, preset: str) -> None:
        src = ONBOARDING_TEMPLATES / f"{preset}.md"
        assert src.is_file(), (
            f"missing onboarding template: templates/onboarding/{preset}.md"
        )


# ---------------------------------------------------------------------------
# Seed-task extraction unit tests
# ---------------------------------------------------------------------------


class TestSeedExtraction:
    """`_extract_seed_tasks` parses `[seed; id: ...]` items + excludes
    `[trigger: ...]` deferred items + ignores non-task prose."""

    def test_extracts_seed_blocks_with_continuation_lines(self) -> None:
        text = (
            "Some preamble prose.\n"
            "\n"
            "## Tasks\n"
            "\n"
            "* [seed; id: alpha]\n"
            "  Continuation line for alpha.\n"
            "\n"
            "* [trigger: first-proposal-archived; id: beta]\n"
            "  This is a deferred task, should NOT be extracted.\n"
            "\n"
            "* [seed; id: gamma]\n"
            "  Continuation for gamma.\n"
        )
        blocks = _extract_seed_tasks(text)
        assert len(blocks) == 2
        assert "[seed; id: alpha]" in blocks[0]
        assert "Continuation line for alpha." in blocks[0]
        assert "[seed; id: gamma]" in blocks[1]

    def test_excludes_trigger_tasks(self) -> None:
        text = (
            "* [trigger: first-proposal-archived; id: deferred-only]\n"
            "  Body.\n"
        )
        blocks = _extract_seed_tasks(text)
        assert blocks == []

    def test_no_tasks_returns_empty(self) -> None:
        assert _extract_seed_tasks("# Just a heading\n\nProse only.\n") == []


# ---------------------------------------------------------------------------
# Slot-substitution unit tests
# ---------------------------------------------------------------------------


class TestSlotSubstitution:
    def test_substitute_finds_and_replaces_slot_body(self) -> None:
        original = (
            "Before slot.\n"
            "<!-- cairn:slot test-slot -->\n"
            "Original placeholder body.\n"
            "<!-- cairn:end test-slot -->\n"
            "After slot.\n"
        )
        new_body = "<!-- preset: solo-greenfield -->\n\n* [seed; id: x]"
        result, ok = _substitute_slot(original, "test-slot", new_body)
        assert ok is True
        assert "<!-- preset: solo-greenfield -->" in result
        assert "Original placeholder body" not in result
        assert "Before slot." in result
        assert "After slot." in result

    def test_substitute_missing_slot_returns_unchanged(self) -> None:
        original = "No slots here.\n"
        result, ok = _substitute_slot(original, "nonexistent", "body")
        assert ok is False
        assert result == original

    def test_render_emits_preset_metadata_first(self) -> None:
        rendered = _render_onboarding_slot(
            "collaborative-team", ["* [seed; id: x]\n  body"],
        )
        lines = rendered.strip("\n").splitlines()
        assert lines[0] == "<!-- preset: collaborative-team -->"


# ---------------------------------------------------------------------------
# Scaffold integration: each preset substitutes correctly
# ---------------------------------------------------------------------------


class TestInstallPath:
    @pytest.mark.parametrize("preset", PRESETS)
    def test_preset_install_inlines_seeds_only(
        self, tmp_path: Path, preset: str,
    ) -> None:
        """Scaffold with each preset yields a PLANNING slot containing
        ONLY seed-task lines + the preset metadata comment.  Deferred
        tasks (`[trigger:` lines) MUST NOT appear in PLANNING (per
        Codex P1-1)."""
        assert _scaffold(tmp_path, preset) == 0

        planning = (tmp_path / "dev" / "PLANNING.md").read_text(
            encoding="utf-8"
        )
        # The slot delimiters are present.
        assert "<!-- cairn:slot onboarding-tasks -->" in planning
        assert "<!-- cairn:end onboarding-tasks -->" in planning
        # The preset metadata comment is present.
        assert f"<!-- preset: {preset} -->" in planning
        # The slot body (between delimiters) contains zero `[trigger:`
        # lines.  Extract the body deterministically.
        a = planning.index("<!-- cairn:slot onboarding-tasks -->")
        b = planning.index("<!-- cairn:end onboarding-tasks -->", a)
        slot_body = planning[a:b]
        assert "[trigger:" not in slot_body, (
            f"deferred [trigger:] task leaked into PLANNING slot for "
            f"preset={preset}; slot body was:\n{slot_body}"
        )
        # At least one seed task IS in the slot body.
        assert "[seed;" in slot_body, (
            f"no [seed;] tasks rendered for preset={preset}"
        )

    @pytest.mark.parametrize("preset", PRESETS)
    def test_installed_source_file_matches_byte_for_byte(
        self, tmp_path: Path, preset: str,
    ) -> None:
        """`dev/modules/onboarding/<preset>.md` matches the Cairn-side
        `templates/onboarding/<preset>.md` byte-for-byte.  This is the
        authoritative reference the goodnight activation helper reads
        to discover deferred tasks (per Codex P1-1)."""
        assert _scaffold(tmp_path, preset) == 0

        installed = tmp_path / "dev" / "modules" / "onboarding" / f"{preset}.md"
        source = ONBOARDING_TEMPLATES / f"{preset}.md"
        assert installed.is_file()
        assert installed.read_bytes() == source.read_bytes(), (
            f"installed onboarding source mismatch for {preset}"
        )

    @pytest.mark.parametrize("preset", PRESETS)
    def test_slot_seed_count_matches_source(
        self, tmp_path: Path, preset: str,
    ) -> None:
        """The number of `* [seed;` task list-items in the PLANNING
        slot equals the number in the source file (sanity: no seeds
        dropped, no seeds duplicated).  Counts the LIST-ITEM form
        `* [seed;` only -- mentions of `[seed;` in source prose /
        documentation headers do not count.
        """
        assert _scaffold(tmp_path, preset) == 0

        planning = (tmp_path / "dev" / "PLANNING.md").read_text(
            encoding="utf-8"
        )
        source = (ONBOARDING_TEMPLATES / f"{preset}.md").read_text(
            encoding="utf-8"
        )

        slot_start = planning.index("<!-- cairn:slot onboarding-tasks -->")
        slot_end = planning.index(
            "<!-- cairn:end onboarding-tasks -->", slot_start,
        )
        slot_body = planning[slot_start:slot_end]

        slot_seeds = slot_body.count("* [seed;")
        src_seeds = source.count("* [seed;")
        assert slot_seeds == src_seeds > 0, (
            f"seed-count mismatch for {preset}: slot has {slot_seeds}, "
            f"source has {src_seeds}"
        )


class TestOnboardingDocDelivery:
    """Write E (fold-back onboarding-doc-delivery): a preset install
    ships the two shared reference docs from ``cairn/docs/`` into the
    adopter's ``dev/modules/onboarding/`` so the presets' "walk this
    doc" refs resolve on first run instead of pointing at never-shipped
    ``docs/`` paths."""

    DOC_NAMES = ("agent-team-onboarding.md", "dev-tour.md")

    @pytest.mark.parametrize("preset", PRESETS)
    def test_preset_install_ships_both_docs(
        self, tmp_path: Path, preset: str,
    ) -> None:
        assert _scaffold(tmp_path, preset) == 0
        onboarding = tmp_path / "dev" / "modules" / "onboarding"
        for name in self.DOC_NAMES:
            installed = onboarding / name
            source = CAIRN_ROOT / "docs" / name
            assert installed.is_file(), (
                f"onboarding doc {name} not shipped for preset={preset}"
            )
            assert (
                installed.read_text(encoding="utf-8")
                == source.read_text(encoding="utf-8")
            ), f"shipped {name} differs from cairn/docs source"

    @pytest.mark.parametrize("preset", PRESETS)
    def test_preset_walk_refs_resolve_post_ship(
        self, tmp_path: Path, preset: str,
    ) -> None:
        """Every ``dev/modules/onboarding/<doc>`` ref the installed
        preset source names points at a file that now exists -- the
        delivery's whole point (no dead "walk this doc" links)."""
        assert _scaffold(tmp_path, preset) == 0
        preset_src = (
            tmp_path / "dev" / "modules" / "onboarding" / f"{preset}.md"
        ).read_text(encoding="utf-8")
        for name in self.DOC_NAMES:
            ref = f"dev/modules/onboarding/{name}"
            if ref in preset_src:
                assert (tmp_path / ref).is_file(), (
                    f"preset {preset} references {ref} but it was not "
                    f"shipped"
                )

    def test_no_preset_ships_no_docs(self, tmp_path: Path) -> None:
        """Explicit-modules path (no preset) ships neither doc -- Write E
        is gated behind a named-preset selection."""
        assert _scaffold(tmp_path, None) == 0
        onboarding = tmp_path / "dev" / "modules" / "onboarding"
        for name in self.DOC_NAMES:
            assert not (onboarding / name).exists(), (
                f"onboarding doc {name} shipped under explicit-modules path"
            )


class TestNoPresetPath:
    def test_explicit_modules_install_leaves_slot_empty(
        self, tmp_path: Path,
    ) -> None:
        """A profile that uses `modules:` without `preset:` is the
        explicit-modules path.  No onboarding install fires; the slot
        body keeps its empty placeholder + the `dev/modules/onboarding/`
        directory exists (from `_DEV_DIRS`) but holds no preset file."""
        assert _scaffold(tmp_path, None) == 0

        planning = (tmp_path / "dev" / "PLANNING.md").read_text(
            encoding="utf-8"
        )
        # Slot still present (the template ships with it).
        assert "<!-- cairn:slot onboarding-tasks -->" in planning
        # No preset metadata comment was written INTO THE SLOT BODY.
        # (The template's intro prose mentions the `<!-- preset: -->`
        # syntax as documentation; the assertion narrows to the slot
        # body between the cairn:slot / cairn:end markers.)
        slot_start = planning.index("<!-- cairn:slot onboarding-tasks -->")
        slot_end = planning.index(
            "<!-- cairn:end onboarding-tasks -->", slot_start,
        )
        slot_body = planning[
            slot_start + len("<!-- cairn:slot onboarding-tasks -->")
            : slot_end
        ]
        assert "<!-- preset:" not in slot_body, (
            f"preset metadata leaked into slot under explicit-modules "
            f"path; slot body:\n{slot_body}"
        )
        # No preset source file installed.
        onboarding_dir = tmp_path / "dev" / "modules" / "onboarding"
        assert onboarding_dir.is_dir()
        installed = list(onboarding_dir.glob("*.md"))
        assert installed == [], (
            f"unexpected onboarding files installed: {installed}"
        )


# ---------------------------------------------------------------------------
# Dry-run mode: shows the plan, writes nothing
# ---------------------------------------------------------------------------


class TestDryRun:
    def test_dry_run_does_not_write_planning(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        """`--dry-run` with a preset prints the planned onboarding
        install line without creating any files in the target."""
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: DryRunTest\n"
            "test_command: pytest\n"
            "preset: solo-greenfield\n",
            encoding="utf-8",
        )
        # Scaffold requires the target dir to exist; create it but
        # confirm no scaffold-side files land inside.
        target = tmp_path / "would-install-here"
        target.mkdir()
        rc = main([
            "--config", str(cfg), "--target", str(target),
            "--cairn-root", str(CAIRN_ROOT),
            "--dry-run",
        ])
        assert rc == 0
        # Target untouched by the scaffold (no dev/ etc.).
        assert not (target / "dev").exists()
        # The onboarding-plan line was printed.
        out = capsys.readouterr().out
        assert "Onboarding:" in out
        assert "templates/onboarding/solo-greenfield.md" in out
