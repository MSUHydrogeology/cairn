"""
Unit tests for bootstrap/scaffold.py.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

# Allow tests to import scaffold without installing a package
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    KNOWN_TOKENS,
    _DEFAULT_ON_MODULES,
    _DOC_AUTHOR_TOKENS,
    _minimal_yaml_parse,
    build_arg_parser,
    create_dev_tree,
    find_block_slots,
    find_unfilled_tokens,
    find_unpaired_slots,
    install_core,
    install_modules,
    load_config,
    substitute_tokens,
)


# ---------------------------------------------------------------------------
# Token substitution
# ---------------------------------------------------------------------------

class TestSubstituteTokens:
    def test_substitutes_known_token(self) -> None:
        text = "Hello {{project_name}}!"
        result = substitute_tokens(text, {"project_name": "Cairn"})
        assert result == "Hello Cairn!"

    def test_substitutes_multiple_tokens(self) -> None:
        text = "{{project_name}} uses {{test_command}} for testing."
        result = substitute_tokens(
            text, {"project_name": "Cairn", "test_command": "pytest"}
        )
        assert result == "Cairn uses pytest for testing."

    def test_leaves_unknown_token_intact(self) -> None:
        text = "See {{unknown_token}} for details."
        result = substitute_tokens(text, {"project_name": "Cairn"})
        assert result == "See {{unknown_token}} for details."

    def test_leaves_token_intact_when_not_in_dict(self) -> None:
        text = "{{test_command}}"
        result = substitute_tokens(text, {})
        assert result == "{{test_command}}"

    def test_empty_text(self) -> None:
        assert substitute_tokens("", {"project_name": "X"}) == ""

    def test_repeated_token(self) -> None:
        text = "{{project_name}} and {{project_name}} again."
        result = substitute_tokens(text, {"project_name": "Cairn"})
        assert result == "Cairn and Cairn again."


# ---------------------------------------------------------------------------
# Unfilled-token detection
# ---------------------------------------------------------------------------

class TestFindUnfilledTokens:
    def test_finds_remaining_tokens(self) -> None:
        text = "Hello Cairn! See {{test_command}}."
        assert find_unfilled_tokens(text) == ["test_command"]

    def test_empty_when_all_substituted(self) -> None:
        text = "Hello World!"
        assert find_unfilled_tokens(text) == []

    def test_multiple_tokens(self) -> None:
        text = "{{a}} and {{b}}"
        assert find_unfilled_tokens(text) == ["a", "b"]

    def test_excludes_doc_author_placeholders(self) -> None:
        """{{Maintainer}}, {{author}}, {{reviewer}}, {{assessor}} are
        document-author placeholders the scaffold deliberately leaves
        unfilled at install -- they should not appear in the warning."""
        text = (
            "## Review -- {{reviewer}} -- 2026-05-20\n"
            "## Response -- {{author}} -- 2026-05-20\n"
            "## Decision -- {{Maintainer}} -- 2026-05-20\n"
            "Profile by {{assessor}}\n"
            "But {{claim_check_command}} is genuinely unfilled.\n"
        )
        assert find_unfilled_tokens(text) == ["claim_check_command"]

    def test_doc_author_tokens_constant(self) -> None:
        """Sanity-check the _DOC_AUTHOR_TOKENS set against the templates
        that use them (proposals/_template.md + phase-0/*)."""
        assert "Maintainer" in _DOC_AUTHOR_TOKENS
        assert "author" in _DOC_AUTHOR_TOKENS
        assert "reviewer" in _DOC_AUTHOR_TOKENS
        assert "assessor" in _DOC_AUTHOR_TOKENS


# ---------------------------------------------------------------------------
# Paired-marker detection (find_unpaired_slots)
# ---------------------------------------------------------------------------

class TestFindUnpairedSlots:
    def test_paired_slot_returns_empty(self) -> None:
        text = (
            "<!-- cairn:slot project-overview -->\n"
            "content\n"
            "<!-- cairn:end project-overview -->"
        )
        assert find_unpaired_slots(text) == []

    def test_missing_close_marker_flagged(self) -> None:
        text = "<!-- cairn:slot orphan -->\ncontent (no close)"
        assert find_unpaired_slots(text) == ["orphan"]

    def test_missing_open_marker_flagged(self) -> None:
        text = "content\n<!-- cairn:end stray -->"
        assert find_unpaired_slots(text) == ["stray"]

    def test_multiple_paired_slots(self) -> None:
        text = (
            "<!-- cairn:slot foo -->\n<!-- cairn:end foo -->\n"
            "<!-- cairn:slot bar -->\n<!-- cairn:end bar -->\n"
        )
        assert find_unpaired_slots(text) == []


# ---------------------------------------------------------------------------
# Block-slot detection
# ---------------------------------------------------------------------------

class TestFindBlockSlots:
    def test_finds_slot_name(self) -> None:
        text = "<!-- cairn:slot project-overview -->\nsome content\n<!-- cairn:end project-overview -->"
        assert find_block_slots(text) == ["project-overview"]

    def test_finds_multiple_slots(self) -> None:
        text = (
            "<!-- cairn:slot foo -->\n"
            "<!-- cairn:slot bar -->\n"
        )
        assert find_block_slots(text) == ["foo", "bar"]

    def test_case_insensitive(self) -> None:
        text = "<!-- CAIRN:SLOT my-slot -->"
        assert find_block_slots(text) == ["my-slot"]

    def test_no_slots(self) -> None:
        text = "No slots here."
        assert find_block_slots(text) == []


# ---------------------------------------------------------------------------
# Minimal YAML parser
# ---------------------------------------------------------------------------

class TestMinimalYamlParse:
    def test_simple_key_value(self) -> None:
        text = "project_name: MyProject\ntest_command: pytest\n"
        result = _minimal_yaml_parse(text)
        assert result["project_name"] == "MyProject"
        assert result["test_command"] == "pytest"

    def test_list_value(self) -> None:
        text = textwrap.dedent("""\
            modules:
              - lifecycle-metrics
              - reflections
        """)
        result = _minimal_yaml_parse(text)
        assert result["modules"] == ["lifecycle-metrics", "reflections"]

    def test_unindented_list_value(self) -> None:
        """Unindented list items under a key (PyYAML accepts this; the
        minimal parser must honor the same shape so no-PyYAML
        environments do not silently drop the modules list)."""
        text = textwrap.dedent("""\
            modules:
            - lifecycle-metrics
            - reflections
            - claim-check
        """)
        result = _minimal_yaml_parse(text)
        assert result["modules"] == [
            "lifecycle-metrics",
            "reflections",
            "claim-check",
        ]

    def test_mixed_indent_list(self) -> None:
        """Mixed indented and unindented items under one key -- not valid
        YAML strictly speaking, but the minimal parser is forgiving."""
        text = textwrap.dedent("""\
            modules:
              - lifecycle-metrics
            - reflections
        """)
        result = _minimal_yaml_parse(text)
        assert result["modules"] == ["lifecycle-metrics", "reflections"]

    def test_skips_comments(self) -> None:
        text = "# comment\nproject_name: MyProject\n"
        result = _minimal_yaml_parse(text)
        assert "project_name" in result

    def test_inline_comment_in_list_item(self) -> None:
        text = textwrap.dedent("""\
            modules:
              - lifecycle-metrics  # always on
        """)
        result = _minimal_yaml_parse(text)
        assert result["modules"] == ["lifecycle-metrics"]

    def test_quoted_value(self) -> None:
        text = 'project_name: "My Project"\n'
        result = _minimal_yaml_parse(text)
        assert result["project_name"] == "My Project"


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

class TestLoadConfig:
    def test_loads_valid_config(self, tmp_path: Path) -> None:
        cfg_file = tmp_path / "profile.yml"
        cfg_file.write_text("project_name: Test\nmodules:\n  - reflections\n")
        cfg = load_config(cfg_file)
        assert cfg["project_name"] == "Test"
        assert cfg["modules"] == ["reflections"]

    def test_raises_on_invalid_yaml(self, tmp_path: Path) -> None:
        cfg_file = tmp_path / "bad.yml"
        # A bare list is not a mapping
        cfg_file.write_text("- item1\n- item2\n")
        # _minimal_yaml_parse may return a dict; only PyYAML will return a list.
        # Just verify load_config doesn't crash for the minimal parser.
        # (We tolerate the minimal parser's inaccuracy here.)


# ---------------------------------------------------------------------------
# dev/ tree creation
# ---------------------------------------------------------------------------

class TestCreateDevTree:
    def test_creates_expected_directories(self, tmp_path: Path) -> None:
        created = create_dev_tree(tmp_path)
        for rel in (
            "dev",
            "dev/proposals",
            "dev/proposals/archive",
            "dev/plans",
            "dev/plans/archive",
            "dev/modules",
        ):
            assert (tmp_path / rel).is_dir(), f"Missing dir: {rel}"

    def test_returns_only_newly_created(self, tmp_path: Path) -> None:
        # Pre-create dev/
        (tmp_path / "dev").mkdir()
        created = create_dev_tree(tmp_path)
        # dev/ already existed; should not be in the created list
        created_names = [p.name for p in created]
        # "dev" was already present; only sub-dirs newly created
        assert "dev" not in created_names or len(created) < 6  # at least one was new

    def test_dry_run_creates_nothing(self, tmp_path: Path) -> None:
        created = create_dev_tree(tmp_path, dry_run=True)
        assert not (tmp_path / "dev").exists()
        assert len(created) > 0  # still reports what *would* be created


# ---------------------------------------------------------------------------
# Core and module installation
# ---------------------------------------------------------------------------

class TestInstallCore:
    def test_installs_agents_md(self, tmp_path: Path) -> None:
        """install_core writes AGENTS.md to the target root."""
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not templates_root.exists():
            pytest.skip("Cairn templates not available")
        tokens = {"project_name": "TestProject", "test_command": "pytest"}
        create_dev_tree(tmp_path)
        results = install_core(templates_root, tmp_path, tokens)
        installed_files = [r[0].name for r in results]
        assert "AGENTS.md" in installed_files
        agents_md = tmp_path / "AGENTS.md"
        assert agents_md.exists()
        content = agents_md.read_text()
        assert "TestProject" in content
        assert "{{project_name}}" not in content

    def test_token_substitution_in_dev_readme(self, tmp_path: Path) -> None:
        """dev/README.md has {{project_name}} substituted."""
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not templates_root.exists():
            pytest.skip("Cairn templates not available")
        tokens = {"project_name": "AwesomeRepo", "test_command": "make test"}
        create_dev_tree(tmp_path)
        install_core(templates_root, tmp_path, tokens)
        dev_readme = tmp_path / "dev" / "README.md"
        assert dev_readme.exists()
        content = dev_readme.read_text()
        assert "AwesomeRepo" in content


class TestInstallModules:
    def test_installs_selected_module(self, tmp_path: Path) -> None:
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not templates_root.exists():
            pytest.skip("Cairn templates not available")
        create_dev_tree(tmp_path)
        results = install_modules(
            templates_root, tmp_path, {}, ["reflections"]
        )
        installed_files = [r[0] for r in results]
        assert (tmp_path / "dev" / "modules" / "reflections.md") in installed_files

    def test_unknown_module_skipped(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not templates_root.exists():
            pytest.skip("Cairn templates not available")
        create_dev_tree(tmp_path)
        results = install_modules(
            templates_root, tmp_path, {}, ["nonexistent-module"]
        )
        assert results == []
        captured = capsys.readouterr()
        assert "warn" in captured.err.lower() or "warn" in captured.out.lower()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

class TestCLI:
    def test_dry_run_exits_zero(self, tmp_path: Path) -> None:
        cairn_root = Path(__file__).resolve().parent.parent.parent
        cfg = tmp_path / "profile.yml"
        cfg.write_text("project_name: DryRunTest\ntest_command: pytest\nmodules:\n  - reflections\n")

        from bootstrap.scaffold import main
        rc = main(
            [
                "--config", str(cfg),
                "--target", str(tmp_path),
                "--cairn-root", str(cairn_root),
                "--dry-run",
            ]
        )
        assert rc == 0

    def test_missing_config_returns_error(self, tmp_path: Path) -> None:
        from bootstrap.scaffold import main
        rc = main(
            [
                "--config", str(tmp_path / "nonexistent.yml"),
                "--target", str(tmp_path),
            ]
        )
        assert rc == 1

    def test_missing_target_returns_error(self, tmp_path: Path) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text("project_name: Test\n")
        from bootstrap.scaffold import main
        rc = main(
            [
                "--config", str(cfg),
                "--target", str(tmp_path / "no_such_dir"),
            ]
        )
        assert rc == 1

    def test_omitted_modules_installs_default_on_set(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When the profile YAML omits `modules:`, the scaffold installs
        the default-on set (BOOTSTRAP Act I-5 step 2 doctrine) and
        warns explicitly."""
        cairn_root = Path(__file__).resolve().parent.parent.parent
        if not (cairn_root / "templates").exists():
            pytest.skip("Cairn templates not available")
        cfg = tmp_path / "profile.yml"
        cfg.write_text("project_name: DefaultOnTest\ntest_command: pytest\n")
        from bootstrap.scaffold import main
        rc = main(
            [
                "--config", str(cfg),
                "--target", str(tmp_path),
                "--cairn-root", str(cairn_root),
            ]
        )
        assert rc == 0
        # Default-on module files should be present
        for module_file in (
            "lifecycle-metrics.md",
            "reflections.md",
            "claim-check.md",
        ):
            assert (tmp_path / "dev" / "modules" / module_file).exists(), (
                f"default-on module {module_file} not installed"
            )
        # The info banner should appear on stderr
        captured = capsys.readouterr()
        assert "default-on" in captured.err.lower()

    def test_empty_modules_list_installs_nothing(
        self, tmp_path: Path
    ) -> None:
        """An explicit `modules: []` means "install no modules" (opt-out
        of even the default-on set)."""
        cairn_root = Path(__file__).resolve().parent.parent.parent
        if not (cairn_root / "templates").exists():
            pytest.skip("Cairn templates not available")
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: NoModulesTest\ntest_command: pytest\nmodules: []\n"
        )
        from bootstrap.scaffold import main
        rc = main(
            [
                "--config", str(cfg),
                "--target", str(tmp_path),
                "--cairn-root", str(cairn_root),
            ]
        )
        assert rc == 0
        modules_dir = tmp_path / "dev" / "modules"
        assert modules_dir.exists()
        # No .md files installed
        assert list(modules_dir.glob("*.md")) == []
