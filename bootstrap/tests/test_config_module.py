"""Stage 4 — the extracted config / token / profile module (`_scaffold/config.py`).

Contracts:

* **Pure stdlib leaf** — `config` imports only the stdlib (yaml is an optional
  best-effort import inside a try/except); it holds the static install schema and
  resolution logic and must never import back into the engine package, nor hold
  adopter-tree writes (those stay in the engine and consume this data).
* **Trust-anchor narrow import** — the release-security scanner
  `bootstrap/security_check.py` imports the `_MODULE_MAPPINGS` trust anchor from
  its *narrowest owner* (`bootstrap._scaffold.config`), not the broad facade.
* **Single identity** — every moved symbol resolves to the one `config` object
  across the engine and the `bootstrap.scaffold` facade.
* **Boundary pin** — the dev-tree / gitignore / fan-out WRITE functions stay in
  the engine, not config (config is write-free).
* **Behavioral smoke** — the YAML fallback parser and preset resolution work
  standalone, so the import boundary didn't break the engine.

Stdlib only.
"""
from __future__ import annotations

import ast
from pathlib import Path

_PKG = Path(__file__).resolve().parents[1] / "_scaffold"
_SECURITY_CHECK = Path(__file__).resolve().parents[1] / "security_check.py"

_MOVED = (
    "_yaml_load", "_minimal_yaml_parse", "load_config", "KNOWN_TOKENS",
    "_DEFAULT_ON_MODULES", "_MODULE_MAPPINGS", "InstallSpec",
    "select_optional_templates", "reference_script_token_defaults",
    "resolve_axes", "expand_preset", "format_profile_summary", "PresetError",
    "_AXES", "_PRESETS", "_CORE_MAPPINGS", "_GITIGNORE_SEEDS",
    "_TOKEN_GATED_MODULES", "token_gated_modules",
)


def test_config_is_a_pure_stdlib_leaf():
    from bootstrap._scaffold import config as C  # noqa: PLC0415

    for node in ast.walk(ast.parse(Path(C.__file__).read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom):
            assert not (node.module or "").startswith("bootstrap"), node.module
            assert node.level == 0, "config leaf must not use package-relative imports"
        if isinstance(node, ast.Import):
            for a in node.names:
                assert a.name == "yaml" or not a.name.startswith("bootstrap"), a.name


def test_security_check_imports_trust_anchor_from_narrowest_owner():
    # plan 0B.3 / Stage 4: the release scanner reads _MODULE_MAPPINGS from the
    # module that OWNS it now (config), not the broad bootstrap.scaffold facade.
    tree = ast.parse(_SECURITY_CHECK.read_text(encoding="utf-8"))
    sources = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and any(a.name == "_MODULE_MAPPINGS" for a in node.names)
    }
    assert sources == {"bootstrap._scaffold.config"}, (
        f"security_check must import the trust anchor from its narrow owner; got {sources}"
    )


def test_single_identity_across_consumers():
    import sys  # noqa: PLC0415

    from bootstrap._scaffold import config as C  # noqa: PLC0415
    import bootstrap._scaffold as engine  # noqa: PLC0415
    import bootstrap.scaffold  # noqa: PLC0415  (facade == engine)

    facade = sys.modules["bootstrap.scaffold"]
    for name in _MOVED:
        obj = getattr(C, name)
        assert getattr(engine, name) is obj, f"engine.{name} is not the config object"
        assert getattr(facade, name) is obj, f"facade.{name} is not the config object"
    # the security_check trust anchor is the same object too
    import bootstrap.security_check as sc  # noqa: PLC0415
    assert sc._MODULE_MAPPINGS is C._MODULE_MAPPINGS


def test_write_functions_stay_in_the_engine_not_config():
    import bootstrap._scaffold as engine  # noqa: PLC0415
    from bootstrap._scaffold import config as C  # noqa: PLC0415

    for fn in ("create_dev_tree", "seed_gitignore"):
        assert hasattr(engine, fn), f"{fn} should remain on the engine"
        assert not hasattr(C, fn), f"{fn} (adopter-tree write) must not be in the config leaf"


def test_yaml_fallback_and_preset_resolution_smoke():
    from bootstrap._scaffold import config as C  # noqa: PLC0415

    parsed = C._minimal_yaml_parse("project_name: demo\nmodules:\n  - claim-check\n")
    assert parsed["project_name"] == "demo"
    assert parsed["modules"] == ["claim-check"]

    # default-on modules are always part of the resolved baseline roster
    modules, axes = C.expand_preset({"preset": "solo-greenfield"})
    assert isinstance(modules, list) and modules
    for default_on in C._DEFAULT_ON_MODULES:
        assert default_on in modules

    summary = C.format_profile_summary({"preset": "solo-greenfield"})
    assert "Does this profile look right" in summary


# ---------------------------------------------------------------------------
# strip_conditional_regions
# ---------------------------------------------------------------------------

def test_strip_conditional_keep_on_match():
    """Semantic 1: value in set → keep body, strip both marker lines."""
    from bootstrap._scaffold.config import strip_conditional_regions  # noqa: PLC0415

    text = (
        "preamble\n"
        "<!-- cairn:if agent_team in concurrent-multi-type,single -->\n"
        "kept body\n"
        "<!-- cairn:endif -->\n"
        "postamble\n"
    )
    result = strip_conditional_regions(text, {"agent_team": "single"})
    assert result == "preamble\nkept body\npostamble\n"


def test_strip_conditional_remove_otherwise():
    """Semantic 2: axis present, value NOT in set → remove markers + body."""
    from bootstrap._scaffold.config import strip_conditional_regions  # noqa: PLC0415

    text = (
        "before\n"
        "<!-- cairn:if agent_team in concurrent-multi-type -->\n"
        "removed body\n"
        "<!-- cairn:endif -->\n"
        "after\n"
    )
    result = strip_conditional_regions(text, {"agent_team": "single"})
    assert result == "before\nafter\n"


def test_strip_conditional_keep_on_missing_axis():
    """Semantic 3: axis absent from axes dict → keep body (safe default)."""
    from bootstrap._scaffold.config import strip_conditional_regions  # noqa: PLC0415

    text = (
        "<!-- cairn:if size in large -->\n"
        "large-only content\n"
        "<!-- cairn:endif -->\n"
    )
    # axis 'size' is missing entirely → keep
    result = strip_conditional_regions(text, {})
    assert result == "large-only content\n"


def test_strip_conditional_raise_on_unclosed():
    """Semantic 4a: open cairn:if with no cairn:endif → ValueError."""
    from bootstrap._scaffold.config import strip_conditional_regions  # noqa: PLC0415
    import pytest  # noqa: PLC0415

    text = (
        "<!-- cairn:if agent_team in single -->\n"
        "content with no close\n"
    )
    with pytest.raises(ValueError, match="Unclosed cairn:if"):
        strip_conditional_regions(text, {"agent_team": "single"})


def test_strip_conditional_raise_on_stray_endif():
    """Semantic 4b: stray cairn:endif with no open → ValueError."""
    from bootstrap._scaffold.config import strip_conditional_regions  # noqa: PLC0415
    import pytest  # noqa: PLC0415

    text = "<!-- cairn:endif -->\n"
    with pytest.raises(ValueError, match="Stray cairn:endif"):
        strip_conditional_regions(text, {})


def test_strip_conditional_raise_on_nesting():
    """Semantic 4c: a second cairn:if before the first closes → ValueError."""
    from bootstrap._scaffold.config import strip_conditional_regions  # noqa: PLC0415
    import pytest  # noqa: PLC0415

    text = (
        "<!-- cairn:if agent_team in single -->\n"
        "<!-- cairn:if size in small -->\n"
        "nested body\n"
        "<!-- cairn:endif -->\n"
        "<!-- cairn:endif -->\n"
    )
    with pytest.raises(ValueError, match="nested"):
        strip_conditional_regions(text, {"agent_team": "single", "size": "small"})


def test_strip_conditional_identity_no_directives():
    """Semantic 5: text with no cairn:if returns byte-identical."""
    from bootstrap._scaffold.config import strip_conditional_regions  # noqa: PLC0415

    text = "# Just a normal doc\n\nNo directives here.\n"
    result = strip_conditional_regions(text, {"agent_team": "single"})
    assert result is not text or result == text  # identity by value
    assert result == text


def test_strip_conditional_determinism():
    """Semantic: same (text, axes) → byte-identical output every call."""
    from bootstrap._scaffold.config import strip_conditional_regions  # noqa: PLC0415

    text = (
        "header\n"
        "<!-- cairn:if human_team in small-multi,large-multi -->\n"
        "team content\n"
        "<!-- cairn:endif -->\n"
        "footer\n"
    )
    axes = {"human_team": "small-multi"}
    r1 = strip_conditional_regions(text, axes)
    r2 = strip_conditional_regions(text, axes)
    assert r1 == r2


def test_strip_conditional_multiple_regions():
    """Multiple non-nested regions in one text are processed independently."""
    from bootstrap._scaffold.config import strip_conditional_regions  # noqa: PLC0415

    text = (
        "intro\n"
        "<!-- cairn:if agent_team in single -->\n"
        "keep-single\n"
        "<!-- cairn:endif -->\n"
        "middle\n"
        "<!-- cairn:if size in large -->\n"
        "remove-large\n"
        "<!-- cairn:endif -->\n"
        "end\n"
    )
    result = strip_conditional_regions(text, {"agent_team": "single", "size": "small"})
    assert result == "intro\nkeep-single\nmiddle\nend\n"


def test_strip_conditional_no_spurious_blank_lines():
    """Removing a region must not leave a residue blank line."""
    from bootstrap._scaffold.config import strip_conditional_regions  # noqa: PLC0415

    text = (
        "line-before\n"
        "<!-- cairn:if size in large -->\n"
        "dropped\n"
        "<!-- cairn:endif -->\n"
        "line-after\n"
    )
    result = strip_conditional_regions(text, {"size": "small"})
    assert result == "line-before\nline-after\n"
    assert "\n\n" not in result
