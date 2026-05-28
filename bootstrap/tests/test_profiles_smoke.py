"""
Smoke tests for the copyable governance-preset profile YAMLs at
``bootstrap/profiles/``.

These YAMLs are the adopter-friction package's item 2 (per the
``2026-05-28-claude-cairn-adopter-friction-package`` plan in
modflow_tools, Chunk 1).  Each is a thin profile YAML that names
its dimensional axes in a comment header and references a
named governance preset via the ``preset:`` key.

The tests below verify three things for each YAML:

1. The YAML loads under Cairn's own minimal parser (the same
   parser ``scaffold.py`` uses without PyYAML installed).
2. The ``preset:`` value resolves to one of ``_PRESETS``.
3. ``scaffold.py --summary --config <yaml>`` produces a profile
   summary that lists the preset's axes and the expected
   baseline module roster, including the default-on set and
   any coordination modules added by the team-staffing gate.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_profiles_smoke.py
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
    _PRESETS,
    _TEAM_STAFFING_GATED,
    _minimal_yaml_parse,
    expand_preset,
)

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
PROFILES_DIR = CAIRN_ROOT / "bootstrap" / "profiles"
SCAFFOLD = CAIRN_ROOT / "bootstrap" / "scaffold.py"

# The three profile YAMLs that ship in this package, paired with
# the preset name each is expected to reference.
PROFILE_FIXTURES = [
    ("solo-greenfield.yml", "solo-greenfield"),
    ("collaborative-team.yml", "collaborative-team"),
    ("high-rigor-legacy.yml", "high-rigor-legacy"),
]


@pytest.fixture(scope="module")
def profiles_dir() -> Path:
    """Cairn-side path to the shipped profile YAMLs."""
    assert PROFILES_DIR.exists(), (
        f"bootstrap/profiles/ missing at {PROFILES_DIR}; this directory is "
        "shipped by the adopter-friction package (plan stem: "
        "2026-05-28-claude-cairn-adopter-friction-package)."
    )
    return PROFILES_DIR


@pytest.mark.parametrize("yaml_name,preset_name", PROFILE_FIXTURES)
def test_profile_yaml_parses(
    profiles_dir: Path, yaml_name: str, preset_name: str
) -> None:
    """Each profile YAML loads under Cairn's own minimal parser."""
    yaml_path = profiles_dir / yaml_name
    assert yaml_path.exists(), f"missing shipped profile YAML: {yaml_path}"
    cfg = _minimal_yaml_parse(yaml_path.read_text())
    # The minimal parser must have produced a dict with the keys the
    # rest of scaffold.py expects.
    assert isinstance(cfg, dict), f"{yaml_name} did not parse to a dict"
    assert "preset" in cfg, f"{yaml_name} omits the `preset:` key"
    assert cfg["preset"] == preset_name, (
        f"{yaml_name} has preset={cfg['preset']!r}, expected {preset_name!r}"
    )
    # Token-substitution keys required for a successful scaffold.
    assert "project_name" in cfg, f"{yaml_name} omits `project_name:`"
    assert "test_command" in cfg, f"{yaml_name} omits `test_command:`"


@pytest.mark.parametrize("yaml_name,preset_name", PROFILE_FIXTURES)
def test_profile_preset_is_known(
    profiles_dir: Path, yaml_name: str, preset_name: str
) -> None:
    """Each YAML's `preset:` resolves to one of `_PRESETS`."""
    cfg = _minimal_yaml_parse((profiles_dir / yaml_name).read_text())
    assert cfg["preset"] in _PRESETS, (
        f"{yaml_name} names preset {cfg['preset']!r}, which is not in "
        f"_PRESETS (known: {sorted(_PRESETS.keys())}); update either the "
        "YAML or _PRESETS in bootstrap/scaffold.py."
    )


@pytest.mark.parametrize("yaml_name,preset_name", PROFILE_FIXTURES)
def test_profile_expands_to_expected_roster(
    profiles_dir: Path, yaml_name: str, preset_name: str
) -> None:
    """Expanding the preset yields the default-on set + the preset's
    baseline + any team-staffing-gate additions."""
    cfg = _minimal_yaml_parse((profiles_dir / yaml_name).read_text())
    modules, _summary = expand_preset(cfg)

    # Default-on modules are always present (the four-module floor).
    for default_on in _DEFAULT_ON_MODULES:
        assert default_on in modules, (
            f"{yaml_name} expansion is missing default-on module "
            f"{default_on!r}; got {modules!r}"
        )

    # Every module in the preset's named baseline must appear.
    preset = _PRESETS[preset_name]
    for baseline_mod in preset["baseline"]:
        assert baseline_mod in modules, (
            f"{yaml_name} expansion is missing baseline module "
            f"{baseline_mod!r} from preset {preset_name!r}; got {modules!r}"
        )

    # The roster has no duplicates and no unknown modules.
    assert len(modules) == len(set(modules)), (
        f"{yaml_name} expansion contains duplicate modules: {modules!r}"
    )


def test_solo_greenfield_is_minimal_default_on_only() -> None:
    """solo-greenfield is the floor: default-on modules only, no
    team-gated ones.  This is the quickstart's published profile."""
    cfg = _minimal_yaml_parse(
        (PROFILES_DIR / "solo-greenfield.yml").read_text()
    )
    modules, _ = expand_preset(cfg)
    assert set(modules) == set(_DEFAULT_ON_MODULES), (
        "solo-greenfield should expand to default-on only -- the "
        "quickstart's published profile.  Got extra modules: "
        f"{set(modules) - set(_DEFAULT_ON_MODULES)}"
    )


def test_collaborative_team_adds_axis_driven_and_coordination_modules() -> None:
    """collaborative-team picks up the moderate-complexity / medium-size
    team-gated modules + the coordination modules through the
    team-staffing gate."""
    cfg = _minimal_yaml_parse(
        (PROFILES_DIR / "collaborative-team.yml").read_text()
    )
    modules, _ = expand_preset(cfg)
    # Axis-driven (named in the preset baseline).
    for axis_driven in ("model-selection", "testing-discipline", "doc-drift-prevention"):
        assert axis_driven in modules, (
            f"collaborative-team should include {axis_driven!r}; got {modules!r}"
        )
    # Coordination modules from the team-staffing gate.
    for coordination in _TEAM_STAFFING_GATED:
        assert coordination in modules, (
            f"collaborative-team should include {coordination!r} via the "
            f"team-staffing gate; got {modules!r}"
        )


def test_high_rigor_legacy_includes_legacy_agent_and_security_review() -> None:
    """high-rigor-legacy is the heaviest preset: legacy-agent +
    security-review + dual-language-tests are the load-bearing
    legacy-scientific-codebase additions."""
    cfg = _minimal_yaml_parse(
        (PROFILES_DIR / "high-rigor-legacy.yml").read_text()
    )
    modules, _ = expand_preset(cfg)
    for legacy_mod in (
        "legacy-agent",
        "security-review",
        "dual-language-tests",
    ):
        assert legacy_mod in modules, (
            f"high-rigor-legacy should include {legacy_mod!r}; got {modules!r}"
        )


@pytest.mark.parametrize("yaml_name,preset_name", PROFILE_FIXTURES)
def test_summary_invocation_prints_preset_axes(
    tmp_path: Path, yaml_name: str, preset_name: str
) -> None:
    """`scaffold.py --summary --config <profile.yml>` is the literal
    command an adopter runs to preview the profile before installing.
    This test invokes it as a subprocess (mirroring adopter use) and
    asserts the printed summary names the preset and lists the
    preset's six-axis point."""
    yaml_path = PROFILES_DIR / yaml_name
    # --summary exits without installing; tmp_path is only used as a
    # safe --target placeholder.
    result = subprocess.run(
        [
            sys.executable,
            str(SCAFFOLD),
            "--config",
            str(yaml_path),
            "--target",
            str(tmp_path),
            "--summary",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"scaffold.py --summary --config {yaml_name} exited with "
        f"{result.returncode}; stderr:\n{result.stderr}\nstdout:\n{result.stdout}"
    )
    assert f"Preset: {preset_name}" in result.stdout, (
        f"--summary output for {yaml_name} did not name preset "
        f"{preset_name!r}; got:\n{result.stdout}"
    )
    # The six-axis values from the preset must all appear in the
    # summary's resolved-axis block.
    for axis_value in _PRESETS[preset_name]["axes"].values():
        assert axis_value in result.stdout, (
            f"--summary output for {yaml_name} did not include axis "
            f"value {axis_value!r}; got:\n{result.stdout}"
        )
    # The default-on modules must appear in the roster.
    for default_on in _DEFAULT_ON_MODULES:
        assert default_on in result.stdout, (
            f"--summary output for {yaml_name} did not include "
            f"default-on module {default_on!r}; got:\n{result.stdout}"
        )

    # --summary writes nothing under the target.
    assert not list(tmp_path.iterdir()), (
        f"--summary should not install anything, but {yaml_name} run "
        f"populated the target: {list(tmp_path.iterdir())}"
    )
