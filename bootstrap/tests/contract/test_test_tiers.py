# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
"""Every test file belongs to exactly one tier.

The shipped testing-discipline module tells adopters that a test's tier comes
from where it lives, and says Cairn's own suite is tiered. Ordinary tests are
grouped under ``unit/``, ``contract/``, ``integration/``, and ``security/``;
workflow tests and protected apparatus remain at their approved paths. The
recursively applied ``tools/test_tiers.json`` filename patterns assign tiers,
and these checks keep every test placed exactly once.

Promises:
- Every test file is in exactly one tier from the configuration; an
  unmatched or shadowed file fails the check.
- The for command selects tests from changed paths, imports and cited paths,
  not folder sweepers, and refuses unbounded or option-shaped ranges.
- Two- and three-dot review ranges succeed on an empty diff.
- Editing a living file (`dev/PLANNING.md` or `CHANGELOG.md`) selects no
  tests, however many tests mention it: the tests build their own copies, and
  the certifying run covers the rest.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import re
import subprocess
import runpy
from pathlib import Path

import pytest
from tests.test_verify_counts import (
    _assert_public_route_triplet,
    _assert_bound_member_mutation,
    _assert_bound_member_positive,
    _assert_linked_caller_parent_positive,
    _BINDING_MUTATIONS,
)

ROOT = Path(__file__).resolve().parents[3]
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
        {"name": "unit", "about": "", "patterns": ["test_first"]},
        {"name": "contract", "about": "", "patterns": ["test_second*"]},
    ])
    folder = _tests(tmp_path, "test_first", "test_second_contract")
    (folder / "test_first.py").write_text("one\ntwo\n", encoding="utf-8")
    (folder / "test_second_contract.py").write_text("three\n", encoding="utf-8")
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


@pytest.mark.parametrize("living", ["dev/PLANNING.md", "CHANGELOG.md"])
def test_for_selects_no_tests_for_a_living_file(tmp_path, living):
    # The board and the changelog change in nearly every commit; the tests
    # that mention them build their own throwaway copies, so naming one must
    # not select them.
    changed = tmp_path / living
    changed.parent.mkdir(parents=True, exist_ok=True)
    changed.write_text("# Living\n", encoding="utf-8")
    target = tmp_path / "tools" / "example.py"
    target.parent.mkdir()
    target.write_text("VALUE = 1\n", encoding="utf-8")
    tests = _tests(tmp_path, "test_mentions_living_file", "test_imports_example")
    (tests / "test_mentions_living_file.py").write_text(
        f'LIVING = "{living}"\n', encoding="utf-8")
    (tests / "test_imports_example.py").write_text(
        "import tools.example\n", encoding="utf-8")
    config = _config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}])

    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(["for", living], config=config,
                           test_dir=tests, root=tmp_path, out=out, err=err)
    assert code == 0
    assert out.getvalue().splitlines() == []
    assert "0 test files" in err.getvalue()

    # Beside another changed file, a living file adds nothing to the selection.
    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(["for", living, "tools/example.py"],
                           config=config, test_dir=tests, root=tmp_path,
                           out=out, err=err)
    assert code == 0
    assert out.getvalue().splitlines() == ["tests/test_imports_example.py"]


def test_for_rejects_paths_outside_project_root(tmp_path):
    tests = _tests(tmp_path, "test_a")
    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(
        ["for", "/outside/secret.py"],
        config=_config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}]),
        test_dir=tests, root=tmp_path, out=out, err=err)
    assert code == 2
    assert "outside project root" in err.getvalue()


def test_for_uses_full_reviewed_range_and_omits_only_above_guard(
        tmp_path, monkeypatch):
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
    calls = []
    reader = tiers_tool._GIT_READ
    original = reader.run_git

    def observed(target, args, **kwargs):
        calls.append((target, args))
        return original(target, args, **kwargs)

    monkeypatch.setattr(reader, "run_git", observed)
    assert tiers_tool.tests_for_paths(
        ["AGENTS.md"], [pinned, protected, sweeper], root=root,
        reviewed_range=reviewed_range, broad_limit=2, omitted=omitted) == [pinned, protected]
    assert omitted == [sweeper]
    left = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD~2^{commit}"], text=True
    ).strip()
    right = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD^{commit}"], text=True
    ).strip()
    assert calls == [
        (str(root), ("rev-parse", "--verify", "--end-of-options",
                     "HEAD~2^{commit}")),
        (str(root), ("rev-parse", "--verify", "--end-of-options",
                     "HEAD^{commit}")),
        (str(root), ("diff", "--unified=0", left + ".." + right,
                     "--", "AGENTS.md")),
    ]


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


@pytest.mark.parametrize("value", [
    "..HEAD", "HEAD..", "-c core.hooksPath=/tmp..HEAD", "HEAD....HEAD",
    "HEAD..HEAD..HEAD", "HEAD\x00..HEAD", "H\nEAD..HEAD", "x" * 1025,
])
def test_for_refuses_unbounded_or_option_shaped_review_ranges(tmp_path, monkeypatch,
                                                               value):
    root = tmp_path / "project"
    root.mkdir()
    tests = _tests(root, "test_reader")
    (root / "AGENTS.md").write_text("rule\n", encoding="utf-8")
    calls = []

    def unexpected(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("invalid range reached Git")

    monkeypatch.setattr(tiers_tool._GIT_READ, "run_git", unexpected)
    with pytest.raises(ValueError, match="invalid reviewed range"):
        tiers_tool.tests_for_paths(
            ["AGENTS.md"], [tests / "test_reader.py"], root=root,
            reviewed_range=value)
    assert calls == []


def test_for_two_and_three_dot_ranges_preserve_empty_success(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    tests = _tests(root, "test_reader")
    (root / "AGENTS.md").write_text("rule\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "AGENTS.md", "tests"],
                   check=True)
    subprocess.run([
        "git", "-C", str(root), "-c", "user.name=Test", "-c",
        "user.email=test@example.invalid", "commit", "-qm", "baseline",
    ], check=True)
    for separator in ("..", "..."):
        out = tiers_tool._resolve_reviewed_range(root, "HEAD" + separator + "HEAD")
        assert re.fullmatch(r"[0-9a-f]{40}" + re.escape(separator) + r"[0-9a-f]{40}", out)
        assert tiers_tool.tests_for_paths(
            ["AGENTS.md"], [tests / "test_reader.py"], root=root,
            reviewed_range="HEAD" + separator + "HEAD") == []


class TestTestTiersPhysicalBinding:
    def test_real_cli_executes_its_pinned_helper(self, tmp_path: Path) -> None:
        _assert_bound_member_positive(tmp_path, "tools/test_tiers.py")

    def test_real_cli_resolves_linked_tools_parent_with_caller_and_helper(
            self, tmp_path: Path) -> None:
        _assert_linked_caller_parent_positive(tmp_path, "tools/test_tiers.py")

    @pytest.mark.parametrize("mutation", _BINDING_MUTATIONS)
    def test_real_cli_refuses_each_binding_mutation(
            self, mutation: str, tmp_path: Path) -> None:
        _assert_bound_member_mutation(tmp_path, "tools/test_tiers.py", mutation)


def _seed_tier_route_repo(root: Path) -> None:
    root.mkdir()
    (root / "tools").mkdir()
    (root / "bootstrap/tests").mkdir(parents=True)
    (root / "tools/test_tiers.json").write_text(
        json.dumps({"tiers": [{"name": "one", "patterns": ["test_*"]}]}),
        encoding="utf-8",
    )
    reader = root / "bootstrap/tests/test_reader.py"
    reader.write_text(
        'OLD = "old governance rule has several useful words here"\n'
        'NEW = "new governance sentence changed by enough distinct words"\n',
        encoding="utf-8",
    )
    agents = root / "AGENTS.md"
    agents.write_text(
        "old governance rule has several useful words here\n", encoding="utf-8")
    env = os.environ.copy()
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_AUTHOR_NAME": "Cairn route test",
        "GIT_AUTHOR_EMAIL": "route-test@example.invalid",
        "GIT_COMMITTER_NAME": "Cairn route test",
        "GIT_COMMITTER_EMAIL": "route-test@example.invalid",
    })
    subprocess.run(["git", "init", "-q", str(root)], env=env,
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "add", "AGENTS.md", "tools/test_tiers.json",
                    "bootstrap/tests/test_reader.py"], env=env,
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "baseline"],
                   env=env, check=True, capture_output=True)
    agents.write_text(
        "new governance sentence changed by enough distinct words\n",
        encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "AGENTS.md"], env=env,
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "update policy"],
                   env=env, check=True, capture_output=True)


def _tier_route_driver(reviewed_range: str, refusal: bool = False) -> str:
    return f'''\
import io
import os
import runpy
module = runpy.run_path(os.environ["CAIRN_TEST_CALLER"], run_name="_route_tiers")
if {refusal!r}:
    out, err = io.StringIO(), io.StringIO()
    code = module["main"](["for", "--range", "HEAD~1..missing", "AGENTS.md"],
                          out=out, err=err)
    assert code == 2 and "Git resolution unavailable" in err.getvalue()
    print("route-refused")
else:
    out, err = io.StringIO(), io.StringIO()
    code = module["main"](["for", "--range", "HEAD~1..HEAD", "AGENTS.md"],
                          out=out, err=err)
    assert code == 0 and out.getvalue().splitlines() == ["bootstrap/tests/test_reader.py"]
    assert "1 test files selected for the requested paths" in err.getvalue()
    out, err = io.StringIO(), io.StringIO()
    assert module["main"](["for", "--range", "HEAD..HEAD", "AGENTS.md"],
                          out=out, err=err) == 0
    assert out.getvalue() == "" and "0 test files selected" in err.getvalue()
    out, err = io.StringIO(), io.StringIO()
    assert module["main"](["for", "--range", "missing..HEAD", "AGENTS.md"],
                          out=out, err=err) == 2
    assert "Git resolution unavailable" in err.getvalue()
    print("route-positive")
'''


def test_tiers_governing_diff_refuses_target_local_path_git_route(tmp_path):
    clean, _safe, _unsafe = _assert_public_route_triplet(
        tmp_path / "tiers-agents-diff", "tools/test_tiers.py", "_resolve_reviewed_range",
        ("rev-parse", "--verify", "--end-of-options", "HEAD~1^{commit}"),
        _tier_route_driver("HEAD~1..HEAD"),
        _tier_route_driver("HEAD~1..HEAD", refusal=True),
        seed=_seed_tier_route_repo)
    assert clean.stdout == "route-positive\n"
