"""
Tests for the Cairn v0.2 P4 governance presets + the preset-merge engine.

Covers, per the executing plan (cairn-v0.2-p4-governance-presets):

* expansion: each named preset expands to its expected baseline roster.
* composability (F2): preset + modules_add / modules_remove both
  directions; **remove wins** on a same-module conflict.
* staffability (I1/F3): an explicit add of an unstaffable module installs
  with a warning; an adopter whose real agent-team can't staff the
  coordination modules gets none in the baseline (team profile wins).
* backward-compat (F2): modules: alone = exact list; modules: [] = none;
  modules: + preset: = hard error; neither = default-on.
* PyYAML / stdlib parity (F4): the flat schema resolves identically via
  PyYAML and via _minimal_yaml_parse.
* profile summary (F5): format_profile_summary shows preset + axes +
  roster + overrides + staffability warnings.
* config type validation (P-5): scalar-where-list and unknown enum are
  friendly hard errors.
* unknown module / unknown preset -> error.
* roster integrity (I4): every module any preset names is real.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Allow tests to import scaffold without installing a package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    _DEFAULT_ON_MODULES,
    _MODULE_MAPPINGS,
    _PRESETS,
    _TEAM_STAFFING_GATED,
    PresetError,
    _minimal_yaml_parse,
    _yaml_load,
    expand_preset,
    format_profile_summary,
    main,
    resolve_axes,
)

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
_DEFAULT_ON = set(_DEFAULT_ON_MODULES)

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _roster(cfg: dict) -> set:
    modules, _summary = expand_preset(cfg)
    return set(modules)


# ---------------------------------------------------------------------------
# Expansion -- each preset -> expected baseline roster
# ---------------------------------------------------------------------------

class TestExpansion:
    def test_solo_greenfield_is_default_on_only(self) -> None:
        assert _roster({"preset": "solo-greenfield"}) == _DEFAULT_ON

    def test_collaborative_team_roster(self) -> None:
        roster = _roster({"preset": "collaborative-team"})
        # default-on + complexity/size-derived practice modules + the
        # team-staffing gate (agent_team=concurrent-multi-type).
        assert roster == _DEFAULT_ON | {
            "model-selection", "testing-discipline", "doc-drift-prevention",
            "dual-review", "coordination-tiers",
        }

    def test_high_rigor_legacy_roster(self) -> None:
        roster = _roster({"preset": "high-rigor-legacy"})
        assert roster == _DEFAULT_ON | {
            "legacy-agent", "security-review", "dual-language-tests",
            "model-selection", "testing-discipline", "doc-drift-prevention",
            "dual-review", "coordination-tiers",
        }

    def test_default_on_always_present(self) -> None:
        for name in _PRESETS:
            assert _DEFAULT_ON <= _roster({"preset": name}), name


# ---------------------------------------------------------------------------
# Composability (F2) -- add / remove, remove wins
# ---------------------------------------------------------------------------

class TestComposability:
    def test_modules_add_installs_off_baseline(self) -> None:
        roster = _roster({
            "preset": "solo-greenfield", "modules_add": ["security-review"],
        })
        assert "security-review" in roster

    def test_modules_remove_drops_from_baseline(self) -> None:
        base = _roster({"preset": "high-rigor-legacy"})
        assert "security-review" in base
        roster = _roster({
            "preset": "high-rigor-legacy",
            "modules_remove": ["security-review"],
        })
        assert "security-review" not in roster

    def test_remove_wins_on_conflict(self) -> None:
        roster = _roster({
            "preset": "solo-greenfield",
            "modules_add": ["security-review"],
            "modules_remove": ["security-review"],
        })
        assert "security-review" not in roster  # remove wins

    def test_remove_default_on_is_permitted_and_logged(self) -> None:
        modules, summary = expand_preset({
            "preset": "solo-greenfield", "modules_remove": ["reflections"],
        })
        assert "reflections" not in modules
        assert "reflections" in summary["removed_default_on"]


# ---------------------------------------------------------------------------
# Staffability (I1 / F3)
# ---------------------------------------------------------------------------

class TestStaffability:
    def test_explicit_add_of_unstaffable_installs_with_warning(self) -> None:
        modules, summary = expand_preset({
            "preset": "solo-greenfield",  # agent_team=single
            "modules_add": ["dual-review"],
        })
        assert "dual-review" in modules  # adopter intent wins (I1)
        assert any(
            "dual-review" in w for w in summary["staffability_warnings"]
        )

    def test_team_profile_wins_suppresses_coordination(self) -> None:
        # collaborative-team's canonical point staffs the coordination
        # modules; an adopter whose real agent-team is single must not get
        # them in the baseline (F3).
        roster = _roster({
            "preset": "collaborative-team", "agent_team": "single",
        })
        assert not (set(_TEAM_STAFFING_GATED) & roster)

    def test_axis_override_adds_coordination(self) -> None:
        # solo-greenfield's canonical agent_team is single; overriding to
        # concurrent-multi-type makes the gate add the coordination modules.
        roster = _roster({
            "preset": "solo-greenfield",
            "agent_team": "concurrent-multi-type",
        })
        assert set(_TEAM_STAFFING_GATED) <= roster


# ---------------------------------------------------------------------------
# Validation -- friendly hard errors
# ---------------------------------------------------------------------------

class TestValidation:
    def test_unknown_preset_errors(self) -> None:
        with pytest.raises(PresetError):
            expand_preset({"preset": "nonesuch"})

    def test_unknown_module_errors(self) -> None:
        with pytest.raises(PresetError):
            expand_preset({
                "preset": "solo-greenfield", "modules_add": ["no-such-mod"],
            })

    def test_unknown_axis_enum_errors(self) -> None:
        with pytest.raises(PresetError):
            resolve_axes("solo-greenfield", {"agent_team": "bogus"})

    def test_scalar_where_list_expected_errors(self) -> None:
        # A scalar string where modules_add expects a list (Codex P-5).
        with pytest.raises(PresetError):
            expand_preset({
                "preset": "solo-greenfield", "modules_add": "security-review",
            })

    def test_duplicate_add_remove_resolves_sanely(self) -> None:
        # Duplicates must not crash or double-apply; remove still wins.
        roster = _roster({
            "preset": "solo-greenfield",
            "modules_add": ["security-review", "security-review"],
            "modules_remove": ["security-review", "security-review"],
        })
        assert "security-review" not in roster


# ---------------------------------------------------------------------------
# Backward-compat + main()-level contract
# ---------------------------------------------------------------------------

class TestBackwardCompat:
    def _write(self, tmp_path: Path, text: str) -> Path:
        cfg = tmp_path / "profile.yml"
        cfg.write_text(text)
        return cfg

    def test_modules_alone_is_exact_list(self, tmp_path: Path) -> None:
        cfg = self._write(
            tmp_path,
            "project_name: T\nmodules:\n  - reflections\n  - dual-review\n",
        )
        rc = main([
            "--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
        ])
        assert rc == 0
        assert (tmp_path / "dev" / "modules" / "reflections.md").is_file()
        assert (tmp_path / "dev" / "modules" / "dual-review.md").is_file()
        # An exact list does not pull in the other default-on modules.
        assert not (
            tmp_path / "dev" / "modules" / "lifecycle-metrics.md"
        ).is_file()

    def test_modules_empty_installs_none(self, tmp_path: Path) -> None:
        cfg = self._write(tmp_path, "project_name: T\nmodules: []\n")
        rc = main([
            "--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
        ])
        assert rc == 0
        mdir = tmp_path / "dev" / "modules"
        assert not list(mdir.glob("*.md")) if mdir.exists() else True

    def test_modules_plus_preset_is_hard_error(self, tmp_path: Path) -> None:
        cfg = self._write(
            tmp_path,
            "project_name: T\npreset: solo-greenfield\nmodules:\n"
            "  - reflections\n",
        )
        rc = main([
            "--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
        ])
        assert rc == 1  # hard error

    def test_preset_install_writes_roster(self, tmp_path: Path) -> None:
        cfg = self._write(
            tmp_path, "project_name: T\npreset: collaborative-team\n",
        )
        rc = main([
            "--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
        ])
        assert rc == 0
        mdir = tmp_path / "dev" / "modules"
        for m in ("coordination-tiers", "dual-review", "testing-discipline"):
            assert (mdir / f"{m}.md").is_file(), m


# ---------------------------------------------------------------------------
# PyYAML / stdlib parity (F4)
# ---------------------------------------------------------------------------

class TestParserParity:
    _PROFILE = (
        "project_name: T\n"
        "preset: high-rigor-legacy\n"
        "agent_team: single\n"
        "modules_add:\n"
        "  - examples-gallery\n"
        "modules_remove:\n"
        "  - security-review\n"
    )

    def test_flat_schema_parses_identically(self) -> None:
        via_pyyaml = _yaml_load(self._PROFILE)
        via_minimal = _minimal_yaml_parse(self._PROFILE)
        # The flat schema is exactly what the minimal parser supports, so
        # both expansions must agree (no nested-mapping divergence).
        assert _roster(via_pyyaml) == _roster(via_minimal)

    def test_minimal_parser_handles_the_override_keys(self) -> None:
        parsed = _minimal_yaml_parse(self._PROFILE)
        assert parsed["preset"] == "high-rigor-legacy"
        assert parsed["agent_team"] == "single"
        assert parsed["modules_add"] == ["examples-gallery"]
        assert parsed["modules_remove"] == ["security-review"]


# ---------------------------------------------------------------------------
# Profile summary (F5)
# ---------------------------------------------------------------------------

class TestProfileSummary:
    def test_summary_shows_preset_axes_roster_overrides_warnings(self) -> None:
        text = format_profile_summary({
            "project_name": "Demo",
            "preset": "solo-greenfield",
            "modules_add": ["dual-review"],
        })
        assert "solo-greenfield" in text
        assert "agent_team" in text
        assert "dual-review" in text          # roster + explicit add
        assert "Explicit add" in text
        # Unstaffable add surfaced in the SAME format as the installer path
        # (`[warn] staffability: ...`) -- standardized per code-review P1.1.
        assert "[warn] staffability:" in text

    def test_summary_cli_exits_without_installing(self, tmp_path: Path) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text("project_name: T\npreset: collaborative-team\n")
        rc = main(["--summary", "--config", str(cfg)])
        assert rc == 0
        # --summary must not create the dev/ tree (no --target, no install).
        assert not (tmp_path / "dev").exists()


# ---------------------------------------------------------------------------
# Roster integrity (I4) -- every preset module is real
# ---------------------------------------------------------------------------

class TestRosterIntegrity:
    def test_every_preset_baseline_module_exists(self) -> None:
        known = set(_MODULE_MAPPINGS) | _DEFAULT_ON
        for name, spec in _PRESETS.items():
            for module in spec["baseline"]:
                assert module in known, (
                    f"preset {name!r} names unknown module {module!r}"
                )

    def test_team_staffing_modules_exist(self) -> None:
        for module in _TEAM_STAFFING_GATED:
            assert module in _MODULE_MAPPINGS, module

    def test_every_preset_expands_to_real_modules(self) -> None:
        known = set(_MODULE_MAPPINGS) | _DEFAULT_ON
        for name in _PRESETS:
            assert _roster({"preset": name}) <= known, name
