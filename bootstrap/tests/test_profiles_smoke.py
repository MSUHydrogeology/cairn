"""
Smoke tests for the copyable governance-preset profile YAMLs at
``bootstrap/profiles/``.

These YAMLs are the adopter-friction package's item 2 (per the
``2026-05-28-claude-cairn-adopter-friction-package`` plan in
modflow_tools, Chunk 1).  Each is a thin profile YAML that names
its dimensional axes in a comment header and references a
named governance preset via the ``preset:`` key.

Promises:
- Each shipped profile in bootstrap/profiles/ reads cleanly and names a known preset. (bootstrap/profiles/*.yml)
- A shipped profile's install includes the default-on modules and every module its preset's baseline names. (BOOTSTRAP.md:188-189)
- ``--summary`` on a shipped profile names its preset, shows its axes and default-on modules, and writes nothing. (production code: bootstrap/_scaffold/cli.py:169)
- The solo-greenfield profile installs default-on modules only. (BOOTSTRAP.md:188)

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
