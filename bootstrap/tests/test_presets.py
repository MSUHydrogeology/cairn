"""
Tests for the governance presets + the preset-merge engine.

Promises:
- A preset installs its full baseline roster, including every default-on module; ``modules:`` alone installs exactly its list. (BOOTSTRAP.md:188-189)
- ``modules_add`` installs a module the preset does not include; ``modules_remove`` drops one, and removal wins when both name it. (BOOTSTRAP.md:768)
- Removing a default-on module is allowed and is recorded in the profile summary. (production code: bootstrap/_scaffold/cli.py:366)
- An explicit add of a module the team cannot staff installs it with a staffability warning. (BOOTSTRAP.md:189)
- The team staffing choice decides whether coordination modules enter the baseline: a single-agent team gets none. (BOOTSTRAP.md:188-189)
- A profile with both ``preset:`` and ``modules:`` is refused with a clear error; the other refusals (unknown preset, module or axis value, a scalar where a list belongs) are tested in test_profile_grammar.py. (production code: bootstrap/_scaffold/config.py:1915)
- ``--summary`` shows the preset, axes, roster and overrides, and writes nothing to the project. (production code: bootstrap/_scaffold/cli.py:169, 208)
- The solo-legacy recipe in docs/solo-legacy-recipe.md installs and summarizes without PyYAML. (docs/solo-legacy-recipe.md)

Covers, per the executing plan (cairn-v0.2-p4-governance-presets):

* resolution (one test through ``--summary``): each shipped preset lists
  only shipped modules and keeps the default-on set; preset + modules_add /
  modules_remove both directions, **remove wins** on a same-module conflict;
  an explicit add of an unstaffable module installs with a warning; an
  adopter whose real agent-team can't staff the coordination modules gets
  none in the baseline (team profile wins); the overrides resolve the same
  with and without PyYAML.
* backward-compat: modules: alone = exact list; modules: [] = none;
  modules: + preset: = hard error; neither = default-on.
* profile summary: ``--summary`` shows preset + axes + roster + overrides +
  staffability warnings, and installs nothing.

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
    main,
)

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
_DEFAULT_ON = set(_DEFAULT_ON_MODULES)

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


# ---------------------------------------------------------------------------
# Preset resolution, read through the public `--summary` entry
# ---------------------------------------------------------------------------

_SHIPPED_PRESETS = sorted(
    p.stem for p in (CAIRN_ROOT / "bootstrap" / "profiles").glob("*.yml")
)

#: Modules only a preset's gate table can bring in (never default-on).
_GATED_MODULES = (
    "dual-review", "coordination-tiers", "model-selection",
    "testing-discipline", "doc-drift-prevention", "legacy-agent",
    "security-review", "dual-language-tests",
)

_NO_YAML_DRIVER = (
    "import sys\n"
    "sys.modules['yaml'] = None\n"
    "sys.path.insert(0, {root!r})\n"
    "from bootstrap.scaffold import main\n"
    "sys.exit(main(['--summary', '--config', {cfg!r}]))\n"
)


def _run_summary(tmp_path: Path, capsys, preset: str, extra: str = "",
                 *, no_yaml: bool = False):
    """Run ``scaffold.py --summary --config`` on a one-preset profile.

    Returns ``(exit status, roster ids, staffability warning lines, the
    summary lines outside the roster)``.  With ``no_yaml`` the run is a
    subprocess in which PyYAML cannot be imported."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    cfg = tmp_path / "profile.yml"
    cfg.write_text(
        f"project_name: T\npreset: {preset}\n{extra}", encoding="utf-8")
    if no_yaml:
        proc = subprocess.run(
            [sys.executable, "-c",
             _NO_YAML_DRIVER.format(root=str(CAIRN_ROOT), cfg=str(cfg))],
            capture_output=True, text=True, cwd=str(CAIRN_ROOT),
        )
        rc, out = proc.returncode, proc.stdout
    else:
        rc = main(["--summary", "--config", str(cfg)])
        out = capsys.readouterr().out
    roster: set[str] = set()
    other: list[str] = []
    in_roster = False
    for line in out.splitlines():
        if line == "Module roster (to install):":
            in_roster = True
        elif in_roster and line.startswith("  - "):
            roster.add(line[len("  - "):])
        else:
            in_roster = False
            other.append(line)
    warnings = [ln for ln in other if "[warn] staffability:" in ln]
    return rc, roster, warnings, other


_CASE_DEFAULTS = {
    "preset": "solo-greenfield", "extra": "",
    "add": (),      # modules the roster gains over the bare preset
    "drop": (),     # modules the roster loses against the bare preset
    "warned": (),   # modules named in a staffability warning
    "shown": (),    # names the summary must show outside the roster list
    "forbid": (),   # modules that must not be in the roster at all
    "no_yaml": False,
}

_OVERRIDES = (
    "agent_team: single\n"
    "modules_add:\n  - examples-gallery\n"
    "modules_remove:\n  - security-review\n"
)

_PRESET_CASES = [
    pytest.param({**_CASE_DEFAULTS, "preset": name,
                  "forbid": _GATED_MODULES if name == "solo-greenfield" else ()},
                 id=f"{name}-alone")
    for name in _SHIPPED_PRESETS
] + [
    pytest.param({**_CASE_DEFAULTS,
                  "extra": "agent_team: concurrent-multi-type\n",
                  "add": ("dual-review", "coordination-tiers")},
                 id="team-axis-override-adds-coordination"),
    pytest.param({**_CASE_DEFAULTS,
                  "extra": "agent_team: concurrent-single-type\n",
                  "add": ("coordination-tiers",)},
                 id="same-type-team-adds-only-coordination-tiers"),
    pytest.param({**_CASE_DEFAULTS, "preset": "collaborative-team",
                  "extra": "agent_team: single\n",
                  "drop": ("dual-review", "coordination-tiers")},
                 id="single-agent-team-wins-over-the-preset"),
    pytest.param({**_CASE_DEFAULTS, "preset": "high-rigor-legacy",
                  "extra": "modules_remove:\n  - security-review\n",
                  "drop": ("security-review",), "shown": ("security-review",)},
                 id="remove-drops-a-baseline-module"),
    pytest.param({**_CASE_DEFAULTS,
                  "extra": ("modules_add:\n  - security-review\n"
                            "modules_remove:\n  - security-review\n"),
                  "shown": ("security-review",)},
                 id="remove-wins-over-add"),
    pytest.param({**_CASE_DEFAULTS,
                  "extra": "modules_remove:\n  - reflections\n",
                  "drop": ("reflections",), "shown": ("reflections",)},
                 id="default-on-removal-is-allowed-and-shown"),
    pytest.param({**_CASE_DEFAULTS,
                  "extra": "modules_add:\n  - dual-review\n",
                  "add": ("dual-review",), "warned": ("dual-review",)},
                 id="unstaffable-add-installs-with-a-warning"),
    pytest.param({**_CASE_DEFAULTS, "preset": "high-rigor-legacy",
                  "extra": _OVERRIDES, "add": ("examples-gallery",),
                  "drop": ("security-review", "dual-review",
                           "coordination-tiers"),
                  "shown": ("security-review",)},
                 id="overrides-together"),
    pytest.param({**_CASE_DEFAULTS, "preset": "high-rigor-legacy",
                  "extra": _OVERRIDES, "add": ("examples-gallery",),
                  "drop": ("security-review", "dual-review",
                           "coordination-tiers"),
                  "shown": ("security-review",), "no_yaml": True},
                 id="overrides-together-without-pyyaml"),
]


@pytest.mark.parametrize("case", _PRESET_CASES)
def test_a_preset_with_overrides_resolves_the_module_set(
    tmp_path: Path, capsys, case: dict,
) -> None:
    """A preset, its team axis and its add/remove lists resolve to one module
    set; default-on modules are always in it; every module it names ships."""
    assert main(["--manifest"]) == 0
    shipped = {
        dest[len("dev/modules/"):-len(".md")]
        for dest in (ln.split("\t", 1)[0]
                     for ln in capsys.readouterr().out.splitlines())
        if dest.startswith("dev/modules/") and dest.endswith(".md")
    }
    _rc, base, _w, _o = _run_summary(tmp_path / "base", capsys, "solo-greenfield")
    _rc, bare, _w, _o = _run_summary(tmp_path / "bare", capsys, case["preset"])
    add, drop = set(case["add"]), set(case["drop"])
    # Preconditions on the case itself: default-on is in every preset, and
    # the override really changes something.
    assert "reflections" in base and base <= bare
    assert drop <= bare and not add & bare

    rc, roster, warnings, other = _run_summary(
        tmp_path / "got", capsys, case["preset"], case["extra"],
        no_yaml=case["no_yaml"])
    outside = "\n".join(other)

    assert {
        "rc": rc,
        "roster": roster,
        "unshipped": roster - shipped,
        "forbidden": roster & set(case["forbid"]),
        "warned": {m for m in shipped if any(m in w for w in warnings)},
        "warning lines": len(warnings),
        "shown": {m for m in case["shown"] if m in outside},
    } == {
        "rc": 0,
        "roster": (bare | add) - drop,
        "unshipped": set(),
        "forbidden": set(),
        "warned": set(case["warned"]),
        "warning lines": len(case["warned"]),
        "shown": set(case["shown"]),
    }


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
        assert [p.name for p in mdir.glob("*.md")] == ["README.md"]
        assert "<!-- cairn:module id=" not in (mdir / "README.md").read_text()

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
# Profile summary
# ---------------------------------------------------------------------------

class TestProfileSummary:


    def test_summary_cli_exits_without_installing(self, tmp_path: Path) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text("project_name: T\npreset: collaborative-team\n")
        rc = main(["--summary", "--config", str(cfg)])
        assert rc == 0
        # --summary must not create the dev/ tree (no --target, no install).
        assert not (tmp_path / "dev").exists()


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


    def test_summary_cli_under_a_genuinely_forced_no_pyyaml_path(
        self, tmp_path: Path,
    ) -> None:
        # Exercises the real CLI / stderr `--summary` path
        # (format_profile_summary), not just _minimal_yaml_parse called
        # directly -- the direct call cannot catch a break in the CLI's own
        # formatting. Runs in a SUBPROCESS under sys.executable (the
        # same interpreter running this test suite, so this is portable --
        # no hardcoded /usr/bin/python3 path) with `sys.modules["yaml"] =
        # None` set before bootstrap.scaffold is ever imported, which
        # makes any attempted runtime PyYAML import fail. The CLI must still
        # parse the profile and format the summary using the stdlib parser.
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
