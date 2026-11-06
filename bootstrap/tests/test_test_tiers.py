# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
"""Every test file belongs to exactly one tier.

The shipped testing-discipline module tells adopters that a test's tier comes
from where it lives, and says Cairn's own suite is tiered. Cairn's tests share
one folder, so ``tools/test_tiers.json`` places each file by name pattern. If
a new test file matched no tier, or a pattern placed nothing, the claim would
quietly stop being true; these tests keep it true.
"""
from __future__ import annotations

import importlib.util
import io
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("_test_tiers_tool", ROOT / "tools" / "test_tiers.py")
tiers_tool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tiers_tool)


def _config(tmp_path: Path, tiers: list[dict]) -> Path:
    path = tmp_path / "tiers.json"
    path.write_text(json.dumps({"tiers": tiers}), encoding="utf-8")
    return path


def _tests(tmp_path: Path, *stems: str) -> Path:
    folder = tmp_path / "tests"
    folder.mkdir()
    for stem in stems:
        (folder / f"{stem}.py").write_text("", encoding="utf-8")
    return folder


def _check(config: Path, folder: Path) -> tuple[int, str]:
    err = io.StringIO()
    code = tiers_tool.main(["check"], config=config, test_dir=folder,
                           out=io.StringIO(), err=err)
    return code, err.getvalue()


def test_every_cairn_test_file_is_in_exactly_one_tier():
    tiers = tiers_tool.load_tiers()
    owner, unplaced, unused = tiers_tool.classify(tiers_tool.find_test_files(), tiers)
    assert unplaced == [], f"test files with no tier: {unplaced}"
    assert unused == [], f"patterns that place no file: {unused}"
    assert len(owner) == len(tiers_tool.find_test_files())


def test_a_new_test_file_no_pattern_places_fails_the_check(tmp_path):
    config = _config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_known"]}])
    code, err = _check(config, _tests(tmp_path, "test_known", "test_brand_new"))
    assert code == 1
    assert "UNPLACED test_brand_new.py" in err


def test_a_pattern_an_earlier_tier_shadows_fails_the_check(tmp_path):
    config = _config(tmp_path, [
        {"name": "security", "about": "", "patterns": ["test_security_*"]},
        {"name": "unit", "about": "", "patterns": ["test_security_marker"]},
    ])
    code, err = _check(config, _tests(tmp_path, "test_security_marker"))
    assert code == 1
    assert "UNUSED   unit: pattern 'test_security_marker'" in err


def test_list_json_exports_reconciled_aggregate_inventory_with_empty_tiers(tmp_path):
    config = _config(tmp_path, [
        {"name": "unit", "about": "", "patterns": ["test_*"]},
        {"name": "contract", "about": "", "patterns": ["contract_*"]},
    ])
    folder = _tests(tmp_path, "test_first", "contract_second")
    (folder / "test_first.py").write_text("one\ntwo\n", encoding="utf-8")
    (folder / "contract_second.py").write_text("three\n", encoding="utf-8")
    out, err = io.StringIO(), io.StringIO()

    code = tiers_tool.main(["list", "--json"], config=config, test_dir=folder,
                           out=out, err=err)

    assert code == 0
    assert err.getvalue() == ""
    assert json.loads(out.getvalue()) == {
        "schema": "cairn-test-inventory/1",
        "counting_method": "recursive-test-files-utf8-replace-splitlines-v1",
        "tiers": [
            {"name": "unit", "files": 1, "lines": 2},
            {"name": "contract", "files": 1, "lines": 1},
        ],
        "total": {"files": 2, "lines": 3},
    }


def test_list_json_requires_complete_valid_tier_placement(tmp_path):
    config = _config(tmp_path, [
        {"name": "unit", "about": "", "patterns": ["test_known"]},
        {"name": "empty", "about": "", "patterns": ["test_empty"]},
    ])
    folder = _tests(tmp_path, "test_known", "test_hidden")
    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(["list", "unit", "--json"], config=config,
                           test_dir=folder, out=out, err=err)
    assert code == 2
    assert out.getvalue() == ""
    assert "complete tier list" in err.getvalue()

    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(["list", "--json"], config=config, test_dir=folder,
                           out=out, err=err)
    assert code == 2
    assert out.getvalue() == ""
    assert "placement is invalid" in err.getvalue()


def test_the_first_matching_tier_owns_a_file(tmp_path):
    tiers = [
        {"name": "security", "about": "", "patterns": ["test_upgrade_refuses_*"]},
        {"name": "workflow", "about": "", "patterns": ["test_upgrade*"]},
    ]
    folder = _tests(tmp_path, "test_upgrade", "test_upgrade_refuses_links")
    owner, unplaced, unused = tiers_tool.classify(sorted(folder.glob("test_*.py")), tiers)
    assert owner == {"test_upgrade": "workflow", "test_upgrade_refuses_links": "security"}
    assert unplaced == [] and unused == []


def test_a_test_file_in_a_subfolder_or_named_the_other_way_is_checked(tmp_path):
    config = _config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_known"]}])
    folder = _tests(tmp_path, "test_known")
    (folder / "deeper").mkdir()
    (folder / "deeper" / "test_hidden.py").write_text("", encoding="utf-8")
    (folder / "parser_test.py").write_text("", encoding="utf-8")
    code, err = _check(config, folder)
    assert code == 1
    assert "UNPLACED test_hidden.py" in err and "UNPLACED parser_test.py" in err


def test_a_tier_without_patterns_is_refused_plainly(tmp_path):
    folder = _tests(tmp_path, "test_a")
    for missing_or_empty in ({"name": "unit"}, {"name": "unit", "patterns": []}):
        config = _config(tmp_path, [missing_or_empty])
        code, err = _check(config, folder)
        assert code == 2
        assert "needs a name and a non-empty list of patterns" in err


def test_for_selects_imports_and_cited_paths_but_not_folder_sweepers(tmp_path):
    target = tmp_path / "tools" / "example.py"
    target.parent.mkdir()
    target.write_text("VALUE = 1\n", encoding="utf-8")
    template = tmp_path / "templates" / "core" / "policy.md"
    template.parent.mkdir(parents=True)
    template.write_text("rule\n", encoding="utf-8")
    tests = _tests(tmp_path, "test_imports_example", "test_imports_from_example",
                   "test_cites_agents", "test_sweeps_templates")
    (tests / "test_imports_example.py").write_text(
        "import tools.example\n", encoding="utf-8")
    (tests / "test_imports_from_example.py").write_text(
        "from example import VALUE\n", encoding="utf-8")
    (tests / "test_cites_agents.py").write_text(
        'PINNED = "templates/core/policy.md"\n', encoding="utf-8")
    (tests / "test_sweeps_templates.py").write_text(
        'for path in Path("templates").rglob("*.md"): pass\n',
        encoding="utf-8")

    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(
        ["for", "tools/example.py", "templates/core/policy.md"],
        config=_config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}]),
        test_dir=tests, root=tmp_path, out=out, err=err)
    assert code == 0
    assert out.getvalue().splitlines() == [
        "tests/test_cites_agents.py",
        "tests/test_imports_example.py",
        "tests/test_imports_from_example.py",
    ]
    assert "3 test files" in err.getvalue()


def test_for_matches_python_references_as_tokens_and_keeps_indirect_consumers(tmp_path):
    target = tmp_path / "bootstrap" / "_scaffold" / "upgrade.py"
    target.parent.mkdir(parents=True)
    target.write_text("VALUE = 1\n", encoding="utf-8")
    tests = _tests(tmp_path, "test_imports_upgrade", "test_cites_upgrade",
                   "test_runs_upgrade", "test_cites_upgrade_helper",
                   "test_parenthesized_import_upgrade",
                   "test_incidental_upgrade_words")
    (tests / "test_imports_upgrade.py").write_text(
        "from bootstrap._scaffold import upgrade as UP\n", encoding="utf-8")
    (tests / "test_cites_upgrade.py").write_text(
        'SOURCE = "bootstrap/_scaffold/upgrade.py"\n', encoding="utf-8")
    (tests / "test_runs_upgrade.py").write_text(
        'def test_public_command(project):\n    upgrade(project, "--apply")\n'
        'COMMAND = "scaffold.py upgrade --apply"\n',
        encoding="utf-8")
    (tests / "test_cites_upgrade_helper.py").write_text(
        'PROTECTED = "_apply_upgrade"\n', encoding="utf-8")
    (tests / "test_parenthesized_import_upgrade.py").write_text(
        "from bootstrap._scaffold import (\n"
        "    install,\n"
        "    upgrade as UP,\n"
        "    lockfile,\n"
        ")\n", encoding="utf-8")
    (tests / "test_incidental_upgrade_words.py").write_text(
        'NOTE = "the upgraded upgradeable upgrade_directory behavior"\n'
        "from package import (\n    upgradeable,\n)\n",
        encoding="utf-8")

    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(
        ["for", "bootstrap/_scaffold/upgrade.py"],
        config=_config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}]),
        test_dir=tests, root=tmp_path, out=out, err=err)
    assert code == 0
    assert out.getvalue().splitlines() == [
        "tests/test_cites_upgrade.py",
        "tests/test_cites_upgrade_helper.py",
        "tests/test_imports_upgrade.py",
        "tests/test_parenthesized_import_upgrade.py",
        "tests/test_runs_upgrade.py",
    ]


def test_for_includes_a_changed_test_module_itself(tmp_path):
    tests = _tests(tmp_path, "test_changed")
    changed_test = tests / "test_changed.py"
    changed_test.write_text("assert True\n", encoding="utf-8")
    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(
        ["for", "tests/test_changed.py"],
        config=_config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}]),
        test_dir=tests, root=tmp_path, out=out, err=err)
    assert code == 0
    assert out.getvalue().splitlines() == ["tests/test_changed.py"]


def test_for_rejects_paths_outside_project_root(tmp_path):
    tests = _tests(tmp_path, "test_a")
    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(
        ["for", "/outside/secret.py"],
        config=_config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}]),
        test_dir=tests, root=tmp_path, out=out, err=err)
    assert code == 2
    assert "outside project root" in err.getvalue()


def test_for_uses_full_reviewed_range_and_omits_only_above_guard(tmp_path):
    root = tmp_path / "project"
    tests = root / "tests"
    tests.mkdir(parents=True)
    agents = root / "AGENTS.md"
    agents.write_text("Boundary B runs before review.\n", encoding="utf-8")
    pinned = tests / "test_pins_boundary.py"
    pinned.write_text(
        'PATH = "AGENTS.md"\n'
        'RULE = "Boundary B runs after code review on the final commit"\n',
        encoding="utf-8")
    protected = tests / "test_protects_removed_boundary.py"
    protected.write_text(
        'PATH = "AGENTS.md"\n'
        'FORBIDDEN = "Boundary B runs before review"\n', encoding="utf-8")
    sweeper = tests / "test_sweeps_agents.py"
    sweeper.write_text('assert Path("AGENTS.md").exists()\n', encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "AGENTS.md", "tests"], check=True)
    subprocess.run([
        "git", "-C", str(root), "-c", "user.name=Test", "-c",
        "user.email=test@example.invalid", "commit", "-qm", "baseline",
    ], check=True)
    agents.write_text("Boundary B runs after code review on the final commit.\n",
                      encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "AGENTS.md"], check=True)
    subprocess.run([
        "git", "-C", str(root), "-c", "user.name=Test", "-c",
        "user.email=test@example.invalid", "commit", "-qm", "governing change",
    ], check=True)
    reviewed_range = "HEAD~2..HEAD"
    (root / "unrelated.txt").write_text("later unrelated commit\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "unrelated.txt"], check=True)
    subprocess.run([
        "git", "-C", str(root), "-c", "user.name=Test", "-c",
        "user.email=test@example.invalid", "commit", "-qm", "unrelated",
    ], check=True)

    omitted: list[Path] = []
    assert tiers_tool.tests_for_paths(
        ["AGENTS.md"], [pinned, protected, sweeper], root=root,
        reviewed_range=reviewed_range, broad_limit=2, omitted=omitted) == [pinned, protected]
    assert omitted == [sweeper]


def test_for_keeps_broad_agents_readers_when_under_guard(tmp_path):
    root = tmp_path / "project"
    tests = root / "tests"
    tests.mkdir(parents=True)
    (root / "AGENTS.md").write_text("A governing sentence with enough words here.\n",
                                    encoding="utf-8")
    readers = [tests / f"test_reader_{i}.py" for i in range(3)]
    for reader in readers:
        reader.write_text('PIN = "AGENTS.md"\n', encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "AGENTS.md", "tests"], check=True)
    subprocess.run([
        "git", "-C", str(root), "-c", "user.name=Test", "-c",
        "user.email=test@example.invalid", "commit", "-qm", "baseline",
    ], check=True)
    omitted: list[Path] = []
    assert tiers_tool.tests_for_paths(
        ["AGENTS.md"], readers, root=root, reviewed_range="HEAD..HEAD",
        broad_limit=40, omitted=omitted) == readers
    assert omitted == []

    broad = [tests / f"test_broad_reader_{i}.py" for i in range(42)]
    for reader in broad:
        reader.write_text('PIN = "AGENTS.md"\n', encoding="utf-8")
    omitted = []
    selected = tiers_tool.tests_for_paths(
        ["AGENTS.md"], readers + broad, root=root, reviewed_range="HEAD..HEAD",
        broad_limit=40, omitted=omitted)
    assert selected == []
    assert omitted == readers + broad

    err = io.StringIO()
    code = tiers_tool.main(
        ["for", "--range", "HEAD..HEAD", "AGENTS.md"],
        config=_config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}]),
        test_dir=tests, root=root, out=io.StringIO(), err=err)
    assert code == 0
    assert "45 AGENTS.md readers omitted above the guard" in err.getvalue()


@pytest.mark.parametrize(("direct_source", "changed_path"), [
    ('PIN = "docs/policy.md"\n', "docs/policy.md"),
    ("from tools import target\n", "tools/target.py"),
])
def test_for_guard_preserves_direct_readers_of_other_changed_paths(
        tmp_path, direct_source, changed_path):
    root = tmp_path / "project"
    tests = root / "tests"
    tests.mkdir(parents=True)
    (root / "AGENTS.md").write_text(
        "Boundary B runs after code review on the final commit.\n",
        encoding="utf-8")
    target = root / changed_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("VALUE = 1\n", encoding="utf-8")
    direct = tests / "test_direct_reader.py"
    direct.write_text(direct_source, encoding="utf-8")
    governing = [tests / f"test_governing_reader_{i}.py" for i in range(41)]
    for reader in governing:
        reader.write_text('PIN = "AGENTS.md"\n', encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "AGENTS.md", "tests", changed_path],
                   check=True)
    subprocess.run([
        "git", "-C", str(root), "-c", "user.name=Test", "-c",
        "user.email=test@example.invalid", "commit", "-qm", "baseline",
    ], check=True)

    omitted: list[Path] = []
    selected = tiers_tool.tests_for_paths(
        ["AGENTS.md", changed_path], [direct, *governing], root=root,
        reviewed_range="HEAD..HEAD", broad_limit=40, omitted=omitted)
    assert selected == [direct]
    assert omitted == governing


def test_for_cli_combined_selection_equals_per_path_union_above_guard(tmp_path):
    root = tmp_path / "project"
    tests = root / "tests"
    tests.mkdir(parents=True)
    (root / "AGENTS.md").write_text(
        "Boundary B runs after code review on the final commit.\n",
        encoding="utf-8")
    other = root / "docs" / "policy.md"
    other.parent.mkdir()
    other.write_text("policy\n", encoding="utf-8")
    direct = tests / "test_direct_reader.py"
    direct.write_text('PIN = "docs/policy.md"\nPIN = "AGENTS.md"\n',
                      encoding="utf-8")
    governing = [tests / f"test_governing_reader_{i}.py" for i in range(41)]
    for reader in governing:
        reader.write_text('PIN = "AGENTS.md"\n', encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "AGENTS.md", "docs", "tests"],
                   check=True)
    subprocess.run([
        "git", "-C", str(root), "-c", "user.name=Test", "-c",
        "user.email=test@example.invalid", "commit", "-qm", "baseline",
    ], check=True)
    config = _config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}])

    def run(paths):
        out, err = io.StringIO(), io.StringIO()
        code = tiers_tool.main(
            ["for", "--range", "HEAD..HEAD", *paths], config=config,
            test_dir=tests, root=root, out=out, err=err)
        assert code == 0, err.getvalue()
        return [root / path for path in out.getvalue().splitlines()]

    expected = [direct]
    assert run(["AGENTS.md", "docs/policy.md"]) == expected
    assert run(["AGENTS.md"]) == []
    assert run(["docs/policy.md"]) == expected


def test_for_requires_range_for_agents(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    tests = _tests(root, "test_reader")
    (root / "AGENTS.md").write_text("rule\n", encoding="utf-8")
    with pytest.raises(ValueError, match="requires --range BASE..HEAD"):
        tiers_tool.tests_for_paths(["AGENTS.md"], [tests / "test_reader.py"], root=root)
