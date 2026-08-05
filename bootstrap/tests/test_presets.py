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

import subprocess
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
        """Pins expansion consumption, not membership of the table itself.

        Literal membership is owned by test_default_security_stance.py.
        """
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

    def test_concurrent_single_type_splits_the_gate(self) -> None:
        # fold-back #40: a concurrent-single-type team staffs
        # coordination-tiers (same-type agents still collide on shared
        # files, and work-intent is the mechanism) but NOT dual-review
        # (no second agent type to fill its External tier).
        roster = _roster({
            "preset": "solo-greenfield",
            "agent_team": "concurrent-single-type",
        })
        assert "coordination-tiers" in roster
        assert "dual-review" not in roster


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


# ---------------------------------------------------------------------------
# The solo-legacy adopter recipe (docs/solo-legacy-recipe.md) -- pins the
# recipe's central claim (copy-pasteability, not just resolver math) and
# documents the finding-2 behavior it routes around, per the
# solo-legacy-adopter-path plan's Chunk B.
# ---------------------------------------------------------------------------

_SOLO_LEGACY_RECIPE = (
    CAIRN_ROOT / "docs" / "solo-legacy-recipe.md"
)
_SOLO_LEGACY_MARKER = "<!-- solo-legacy-recipe: canonical-profile -->"


def _extract_marked_yaml(text: str, marker: str) -> str:
    """Locate `marker`, then the single fenced ```yaml block immediately
    following it. Fails loudly (not a silent first/last-fence pick) if the
    marker or the fence is missing or duplicated -- a doc that ends up with
    a second, contrasting YAML example (e.g. for a "why not the naive
    override" callout) must not be picked up by accident."""
    assert text.count(marker) == 1, (
        f"expected exactly one {marker!r} in the recipe, found "
        f"{text.count(marker)}"
    )
    rest = text[text.index(marker) + len(marker):]
    fence_start = rest.index("```yaml") + len("```yaml")
    fence_end = rest.index("```", fence_start)
    return rest[fence_start:fence_end].lstrip("\n")


class TestSoloLegacyRecipe:
    def test_recipe_file_exists(self) -> None:
        assert _SOLO_LEGACY_RECIPE.is_file(), _SOLO_LEGACY_RECIPE

    def test_marked_yaml_extraction_is_unambiguous(self) -> None:
        text = _SOLO_LEGACY_RECIPE.read_text(encoding="utf-8")
        # Fails loudly if a second marker or fence is ever added without
        # updating this extraction -- the whole point of anchoring on the
        # marker rather than "the first ```yaml block in the file."
        assert text.count(_SOLO_LEGACY_MARKER) == 1

    def test_literal_recipe_yaml_round_trips_under_the_stdlib_parser(self) -> None:
        # This is the recipe's actual headline claim: a zero-dependency
        # adopter, with no PyYAML, copy-pastes this block and it works.
        # Calling _minimal_yaml_parse directly (not _yaml_load, which
        # prefers PyYAML when present) genuinely exercises the stdlib-only
        # path regardless of what's installed in this environment -- the
        # exact gap the original "verified via expand_preset on a
        # hand-built dict" claim had (it never touched either YAML parser).
        text = _SOLO_LEGACY_RECIPE.read_text(encoding="utf-8")
        yaml_text = _extract_marked_yaml(text, _SOLO_LEGACY_MARKER)
        parsed = _minimal_yaml_parse(yaml_text)
        assert parsed["preset"] == "solo-greenfield"
        assert parsed["age"] == "legacy"
        assert parsed["modules_add"] == ["legacy-agent", "testing-discipline"]

        modules, summary = expand_preset(parsed)
        assert set(modules) == _DEFAULT_ON | {"legacy-agent", "testing-discipline"}
        assert len(modules) == 9
        assert summary["staffability_warnings"] == []

    def test_literal_recipe_yaml_also_parses_via_pyyaml(self) -> None:
        # Parity check (F4's existing convention): both parsers must agree
        # on the recipe's flat schema, so neither path is silently wrong.
        text = _SOLO_LEGACY_RECIPE.read_text(encoding="utf-8")
        yaml_text = _extract_marked_yaml(text, _SOLO_LEGACY_MARKER)
        assert _roster(_yaml_load(yaml_text)) == _roster(_minimal_yaml_parse(yaml_text))

    def test_summary_cli_under_a_genuinely_forced_no_pyyaml_path(
        self, tmp_path: Path,
    ) -> None:
        # Closes the residual verification item both proposal-stage reviews
        # flagged as unexercised: the real CLI / stderr `--summary` path
        # (format_profile_summary, mirroring test_summary_cli_exits_
        # without_installing's F5 pattern), not just _minimal_yaml_parse
        # called directly. Runs in a SUBPROCESS under sys.executable (the
        # same interpreter running this test suite, so this is portable --
        # no hardcoded /usr/bin/python3 path) with `sys.modules["yaml"] =
        # None` set before bootstrap.scaffold is ever imported, which
        # forces config.py's `try: import yaml` to raise ImportError and
        # bind _yaml_load to the _minimal_yaml_parse fallback for real --
        # not a simulation, the actual branch a zero-dependency adopter's
        # interpreter takes.
        text = _SOLO_LEGACY_RECIPE.read_text(encoding="utf-8")
        yaml_text = _extract_marked_yaml(text, _SOLO_LEGACY_MARKER)
        cfg = tmp_path / "profile.yml"
        cfg.write_text(yaml_text, encoding="utf-8")

        driver = (
            "import sys\n"
            "sys.modules['yaml'] = None\n"
            f"sys.path.insert(0, {str(CAIRN_ROOT)!r})\n"
            "from bootstrap.scaffold import main\n"
            f"sys.exit(main(['--summary', '--config', {str(cfg)!r}]))\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", driver],
            capture_output=True, text=True, cwd=str(CAIRN_ROOT),
        )
        assert result.returncode == 0, result.stderr
        for module in _DEFAULT_ON | {"legacy-agent", "testing-discipline"}:
            assert module in result.stdout, (
                f"{module!r} missing from --summary output:\n{result.stdout}"
            )
        assert "[warn] staffability:" not in result.stdout, result.stdout

    def test_naive_age_override_alone_does_not_add_legacy_agent(self) -> None:
        # Pins the finding-2 behavior the recipe's "why these lines are
        # load-bearing" section routes around: overriding `age` alone does
        # NOT re-derive age-gated baseline rows (the static-preset-baseline
        # mechanism in expand_preset only re-derives the team-staffing-gated
        # rows). This is CURRENT behavior, not a desired invariant -- it is
        # pinned here so a future engine fix (the solo-legacy-adopter-path
        # proposal's deferred Alternative 4) turning this red is expected
        # and should be treated as "update this test," not "regression."
        roster = _roster({"preset": "solo-greenfield", "age": "legacy"})
        assert roster == _DEFAULT_ON
        assert "legacy-agent" not in roster
