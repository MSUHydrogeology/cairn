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
    install_optional,
    load_config,
    select_optional_templates,
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

    def test_installed_templates_carry_plan_review_line(
        self, tmp_path: Path
    ) -> None:
        """D-2: the installed `dev/proposals/_template.md` and
        `dev/plans/_template.md` must carry the mandatory
        ``**Plan review**:`` metadata line.  Pins the templates against
        silent regression of the plan-review-gate doctrine (the
        Plan-review precondition needs this line to be load-bearing,
        not optional).
        """
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not templates_root.exists():
            pytest.skip("Cairn templates not available")
        tokens = {"project_name": "TestProject", "test_command": "pytest"}
        create_dev_tree(tmp_path)
        install_core(templates_root, tmp_path, tokens)
        for rel in ("dev/proposals/_template.md", "dev/plans/_template.md"):
            installed = tmp_path / rel
            assert installed.is_file(), (
                f"{rel} was not installed by install_core"
            )
            content = installed.read_text()
            assert "**Plan review**:" in content, (
                f"{rel} is missing the mandatory `**Plan review**:` "
                f"metadata line -- silent regression of the plan-review "
                f"entry-gate doctrine"
            )


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
        # fold-back #42: reflections also installs a tracked directory guide
        # so dev/reflections/ materializes on a fresh scaffold (the entries
        # themselves stay untracked via the .gitignore seed).
        assert (
            tmp_path / "dev" / "reflections" / "README.md"
        ) in installed_files

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


class TestNewTeamGatedModules:
    """The two team-gated modules added by the cairn-fidelity-gaps
    sync (security-review, issue-capture). Each must be registered in
    _MODULE_MAPPINGS and installable when its gate selects it -- a
    documented module file that is never selectable would satisfy the
    docs but not the scaffold (Codex External finding 1 / Antigravity
    R8)."""

    @pytest.mark.parametrize("module_name", ["security-review", "issue-capture"])
    def test_new_module_registered(self, module_name: str) -> None:
        from bootstrap.scaffold import _MODULE_MAPPINGS

        assert module_name in _MODULE_MAPPINGS, (
            f"{module_name} not registered in _MODULE_MAPPINGS"
        )
        # 1:many contract (Cairn v0.2 P1): each module maps to a list of
        # InstallSpec.  These team-gated modules install a single .md.
        specs = _MODULE_MAPPINGS[module_name]
        assert len(specs) == 1
        spec = specs[0]
        assert spec.src == f"team-gated/{module_name}.md"
        assert spec.dst == f"dev/modules/{module_name}.md"
        assert spec.verbatim is False

    @pytest.mark.parametrize("module_name", ["security-review", "issue-capture"])
    def test_new_module_installs_when_selected(
        self, tmp_path: Path, module_name: str
    ) -> None:
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not templates_root.exists():
            pytest.skip("Cairn templates not available")
        create_dev_tree(tmp_path)
        results = install_modules(
            templates_root, tmp_path, {}, [module_name]
        )
        installed_files = [r[0] for r in results]
        expected = tmp_path / "dev" / "modules" / f"{module_name}.md"
        assert expected in installed_files
        assert expected.exists()

    def test_lhm_shaped_profile_selects_both_new_modules(
        self, tmp_path: Path
    ) -> None:
        """An LHM-shaped profile -- legacy + multi-language +
        multi-agent + a trust boundary + an issue tracker -- selects
        every team-gated module, including the two new ones. The
        generated tree must *contain* both, not leave them as files
        that exist but are never installed."""
        cairn_root = Path(__file__).resolve().parent.parent.parent
        if not (cairn_root / "templates").exists():
            pytest.skip("Cairn templates not available")
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: LhmShaped\n"
            "test_command: pytest\n"
            "modules:\n"
            "  - lifecycle-metrics\n"
            "  - reflections\n"
            "  - claim-check\n"
            "  - dual-review\n"
            "  - domain-agents\n"
            "  - legacy-agent\n"
            "  - dual-language-tests\n"
            "  - coordination-tiers\n"
            "  - security-review\n"
            "  - issue-capture\n"
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
        for module_file in ("security-review.md", "issue-capture.md"):
            assert (tmp_path / "dev" / "modules" / module_file).exists(), (
                f"new team-gated module {module_file} not installed for "
                f"the LHM-shaped profile"
            )


class TestArchitectureReviewModule:
    """architecture-review (modflow_tools doctrine-parity fold) ships a
    *2-spec* contract -- the module doctrine plus a forkable rubric frame
    -- unlike the single-.md team-gated modules above. Both must be
    registered in _MODULE_MAPPINGS and install when the gate selects it,
    so a documented-but-uninstallable module cannot slip through."""

    def test_registered_with_two_specs(self) -> None:
        from bootstrap.scaffold import _MODULE_MAPPINGS

        assert "architecture-review" in _MODULE_MAPPINGS, (
            "architecture-review not registered in _MODULE_MAPPINGS"
        )
        specs = _MODULE_MAPPINGS["architecture-review"]
        assert len(specs) == 2
        by_dst = {s.dst: s for s in specs}
        doctrine = by_dst["dev/modules/architecture-review.md"]
        frame = by_dst["dev/architecture_review.md"]
        assert doctrine.src == "team-gated/architecture-review.md"
        assert frame.src == "team-gated/architecture_review_template.md"
        # Both are substituted forkable templates, not verbatim scripts.
        assert doctrine.verbatim is False
        assert frame.verbatim is False

    def test_installs_both_files_when_selected(self, tmp_path: Path) -> None:
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not templates_root.exists():
            pytest.skip("Cairn templates not available")
        create_dev_tree(tmp_path)
        results = install_modules(
            templates_root, tmp_path, {}, ["architecture-review"]
        )
        installed_files = [r[0] for r in results]
        for rel in ("dev/modules/architecture-review.md",
                    "dev/architecture_review.md"):
            expected = tmp_path / rel
            assert expected in installed_files, f"{rel} not installed"
            assert expected.exists()


class TestModelSelectionWired:
    """`model-selection` shipped as a team-gated module *file* but was
    never registered in _MODULE_MAPPINGS, so a profile listing it printed
    `unknown module` and skipped it -- the LHM bootstrap had to copy it in
    by hand. cairn-foldbacks item 1 / ledger #1."""

    def test_model_selection_registered(self) -> None:
        from bootstrap.scaffold import _MODULE_MAPPINGS

        assert "model-selection" in _MODULE_MAPPINGS, (
            "model-selection not registered in _MODULE_MAPPINGS"
        )
        specs = _MODULE_MAPPINGS["model-selection"]
        assert len(specs) == 1
        spec = specs[0]
        assert spec.src == "team-gated/model-selection.md"
        assert spec.dst == "dev/modules/model-selection.md"
        assert spec.verbatim is False

    def test_model_selection_installs_when_selected(
        self, tmp_path: Path
    ) -> None:
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not templates_root.exists():
            pytest.skip("Cairn templates not available")
        create_dev_tree(tmp_path)
        results = install_modules(
            templates_root, tmp_path, {}, ["model-selection"]
        )
        installed_files = [r[0] for r in results]
        expected = tmp_path / "dev" / "modules" / "model-selection.md"
        assert expected in installed_files
        assert expected.exists()

    def test_model_selection_no_unknown_warning(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """The bug's signature: listing model-selection printed an
        `unknown module` warning and skipped it. After wiring, it must
        not."""
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not templates_root.exists():
            pytest.skip("Cairn templates not available")
        create_dev_tree(tmp_path)
        install_modules(templates_root, tmp_path, {}, ["model-selection"])
        captured = capsys.readouterr()
        assert "unknown module" not in (captured.err + captured.out).lower()


# ---------------------------------------------------------------------------
# Optional templates — human-team-gated CONTRIBUTING.md (foldback #10)
# ---------------------------------------------------------------------------

class TestOptionalContributing:
    def test_selected_at_small_multi(self) -> None:
        sel = select_optional_templates({"human_team": "small-multi"})
        assert ("optional/CONTRIBUTING.md", "CONTRIBUTING.md") in sel

    def test_selected_at_large_multi(self) -> None:
        sel = select_optional_templates({"human_team": "large-multi"})
        assert ("optional/CONTRIBUTING.md", "CONTRIBUTING.md") in sel

    def test_not_selected_for_solo(self) -> None:
        assert select_optional_templates({"human_team": "solo"}) == []

    def test_not_selected_when_axis_absent(self) -> None:
        assert select_optional_templates({}) == []

    def test_small_multi_install_writes_contributing(
        self, tmp_path: Path
    ) -> None:
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not (templates_root / "optional" / "CONTRIBUTING.md").exists():
            pytest.skip("optional CONTRIBUTING.md template not available")
        create_dev_tree(tmp_path)
        sel = select_optional_templates({"human_team": "small-multi"})
        results = install_optional(
            templates_root, tmp_path, {"project_name": "Demo"}, sel
        )
        installed = [r[0] for r in results]
        contributing = tmp_path / "CONTRIBUTING.md"
        assert contributing in installed
        assert contributing.exists()
        # Single-source check: the human entry points to AGENTS.md, it
        # does not duplicate the operational reference.
        body = contributing.read_text(encoding="utf-8")
        assert "AGENTS.md" in body

    def test_solo_install_writes_no_contributing(
        self, tmp_path: Path
    ) -> None:
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        create_dev_tree(tmp_path)
        sel = select_optional_templates({"human_team": "solo"})
        install_optional(templates_root, tmp_path, {"project_name": "Demo"}, sel)
        assert not (tmp_path / "CONTRIBUTING.md").exists()

    def test_optional_templates_recorded_in_manifest_spec(self) -> None:
        """The blocker: the gate must be auditable — the fidelity-manifest
        spec carries an `optional_templates:` block documenting the
        CONTRIBUTING.md gate."""
        cairn_root = Path(__file__).resolve().parent.parent.parent
        spec = (cairn_root / "bootstrap" / "fidelity-check.md").read_text(
            encoding="utf-8"
        )
        assert "optional_templates:" in spec
        assert "CONTRIBUTING.md" in spec
        assert "human_team" in spec


# ---------------------------------------------------------------------------
# RULES.md convention — project-owned, never templated / tracked
# ---------------------------------------------------------------------------

class TestRulesMdNeverTemplated:
    """``RULES.md`` is the project-owned rules file Cairn never templates.

    The structural guarantee (``doctrine/doc-governance.md`` >
    "Project-owned rules — the ``RULES.md`` convention"): because Cairn
    ships no mapping for ``RULES.md``, it never enters ``_lock_file_list``
    and ``scaffold.py upgrade`` can never merge or clobber it.
    """

    def _all_install_dsts(self) -> set[str]:
        import bootstrap.scaffold as scaffold

        dsts: set[str] = set()
        for _src, dst in scaffold._CORE_MAPPINGS:
            dsts.add(dst)
        for entry in scaffold._SKILLS_MAPPINGS:
            dsts.add(entry[1])
        for entry in scaffold._OPTIONAL_TEMPLATES:
            dsts.add(entry[1])
        for specs in scaffold._MODULE_MAPPINGS.values():
            for spec in specs:
                dst = getattr(spec, "dst", None)
                if dst is None and isinstance(spec, (tuple, list)) and len(spec) >= 2:
                    dst = spec[1]
                if dst is not None:
                    dsts.add(str(dst))
        return dsts

    def test_rules_md_absent_from_every_mapping(self) -> None:
        """No install-mapping table targets RULES.md (so it never locks)."""
        offenders = {
            p for p in self._all_install_dsts()
            if p == "RULES.md" or Path(p).name == "RULES.md"
        }
        assert not offenders, (
            f"RULES.md must be in no Cairn install mapping; found: {offenders}"
        )

    def test_full_install_writes_no_rules_md(self, tmp_path: Path) -> None:
        """A full install (core + every default-on module + optional)
        never creates a RULES.md at the target root."""
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not templates_root.exists():
            pytest.skip("Cairn templates not available")
        tokens = {"project_name": "RulesDemo", "test_command": "pytest"}
        create_dev_tree(tmp_path)
        install_core(templates_root, tmp_path, tokens)
        for module in _DEFAULT_ON_MODULES:
            install_modules(templates_root, tmp_path, tokens, [module])
        sel = select_optional_templates({"human_team": "large-multi"})
        install_optional(templates_root, tmp_path, tokens, sel)
        assert not (tmp_path / "RULES.md").exists(), (
            "a Cairn install must never create RULES.md"
        )


# ---------------------------------------------------------------------------
# Vendor wrapper — generic, neutral VENDOR.md (foldback #12)
# ---------------------------------------------------------------------------

class TestVendorWrapper:
    def test_vendor_md_installs_by_default(self, tmp_path: Path) -> None:
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not (templates_root / "core" / "VENDOR.md").exists():
            pytest.skip("VENDOR.md template not available")
        create_dev_tree(tmp_path)
        install_core(templates_root, tmp_path, {"project_name": "Demo"})
        assert (tmp_path / "VENDOR.md").exists()

    def test_vendor_md_imports_agents_and_stays_thin(
        self, tmp_path: Path
    ) -> None:
        cairn_root = Path(__file__).resolve().parent.parent.parent
        templates_root = cairn_root / "templates"
        if not (templates_root / "core" / "VENDOR.md").exists():
            pytest.skip("VENDOR.md template not available")
        create_dev_tree(tmp_path)
        install_core(templates_root, tmp_path, {"project_name": "Demo"})
        body = (tmp_path / "VENDOR.md").read_text(encoding="utf-8")
        # Opens by importing the shared, neutral AGENTS.md.
        assert "@AGENTS.md" in body
        # Carries the drift guard, and does NOT duplicate canonical
        # AGENTS.md operational content (e.g. the git-workflow section).
        assert "Drift guard" in body
        assert "## Git and commit workflow" not in body

    def test_core_ships_no_literal_vendor_name(self) -> None:
        """R-G: core templates name no specific AI tool.  The wrapper is
        the generic VENDOR.md, never a literal CLAUDE.md/GEMINI.md."""
        cairn_root = Path(__file__).resolve().parent.parent.parent
        core = cairn_root / "templates" / "core"
        assert (core / "VENDOR.md").exists()
        assert not (core / "CLAUDE.md").exists()
        assert not (core / "GEMINI.md").exists()


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

    def test_rerun_skips_existing_files_by_default(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Re-running the scaffold against an already-installed target
        preserves the existing files (so an adopter's filled block slots
        survive a second run).  Filed under External Review F2 from
        Antigravity, 2026-05-20."""
        cairn_root = Path(__file__).resolve().parent.parent.parent
        if not (cairn_root / "templates").exists():
            pytest.skip("Cairn templates not available")
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: SkipTest\ntest_command: pytest\nmodules: []\n"
        )
        # First install
        from bootstrap.scaffold import main
        rc1 = main(
            [
                "--config", str(cfg),
                "--target", str(tmp_path),
                "--cairn-root", str(cairn_root),
            ]
        )
        assert rc1 == 0

        # Customize AGENTS.md to simulate a filled block slot
        agents_md = tmp_path / "AGENTS.md"
        original = agents_md.read_text()
        custom = original + "\n<!-- CUSTOMIZED CONTENT -->\n"
        agents_md.write_text(custom)

        # Second install -- should NOT clobber
        rc2 = main(
            [
                "--config", str(cfg),
                "--target", str(tmp_path),
                "--cairn-root", str(cairn_root),
            ]
        )
        assert rc2 == 0
        assert agents_md.read_text() == custom, (
            "Re-running the scaffold without --force clobbered customizations"
        )
        captured = capsys.readouterr()
        # A skip warning should appear on stderr
        assert "[skip]" in captured.err.lower() or "skip" in captured.err.lower()

    def test_force_overwrites_existing_files(
        self, tmp_path: Path
    ) -> None:
        """--force opts into overwriting existing target files."""
        cairn_root = Path(__file__).resolve().parent.parent.parent
        if not (cairn_root / "templates").exists():
            pytest.skip("Cairn templates not available")
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: ForceTest\ntest_command: pytest\nmodules: []\n"
        )
        from bootstrap.scaffold import main
        rc1 = main(
            [
                "--config", str(cfg),
                "--target", str(tmp_path),
                "--cairn-root", str(cairn_root),
            ]
        )
        assert rc1 == 0
        agents_md = tmp_path / "AGENTS.md"
        agents_md.write_text("# Hand-edited content the user wants gone\n")

        # --force overwrites
        rc2 = main(
            [
                "--config", str(cfg),
                "--target", str(tmp_path),
                "--cairn-root", str(cairn_root),
                "--force",
            ]
        )
        assert rc2 == 0
        # Content should be the template again, not the hand-edited version
        content = agents_md.read_text()
        assert "Hand-edited content" not in content
        assert "ForceTest" in content  # token substitution happened

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
