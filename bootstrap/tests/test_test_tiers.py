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
    template = tmp_path / "templates" / "core" / "AGENTS.md"
    template.parent.mkdir(parents=True)
    template.write_text("rule\n", encoding="utf-8")
    tests = _tests(tmp_path, "test_imports_example", "test_imports_from_example",
                   "test_cites_agents", "test_sweeps_templates")
    (tests / "test_imports_example.py").write_text(
        "import tools.example\n", encoding="utf-8")
    (tests / "test_imports_from_example.py").write_text(
        "from example import VALUE\n", encoding="utf-8")
    (tests / "test_cites_agents.py").write_text(
        'PINNED = "templates/core/AGENTS.md"\n', encoding="utf-8")
    (tests / "test_sweeps_templates.py").write_text(
        'for path in Path("templates").rglob("*.md"): pass\n',
        encoding="utf-8")

    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(
        ["for", "tools/example.py", "templates/core/AGENTS.md"],
        config=_config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}]),
        test_dir=tests, root=tmp_path, out=out, err=err)
    assert code == 0
    assert out.getvalue().splitlines() == [
        "tests/test_cites_agents.py",
        "tests/test_imports_example.py",
        "tests/test_imports_from_example.py",
    ]
    assert "3 test files" in err.getvalue()


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


def test_for_narrows_agents_to_tests_pinning_changed_passages(tmp_path):
    root = tmp_path / "project"
    tests = root / "tests"
    tests.mkdir(parents=True)
    agents = root / "AGENTS.md"
    agents.write_text("Boundary B runs before review.\n", encoding="utf-8")
    pinned = tests / "test_pins_boundary.py"
    pinned.write_text(
        'RULE = "Boundary B runs after code review on the final commit"\n',
        encoding="utf-8")
    protected = tests / "test_protects_removed_boundary.py"
    protected.write_text(
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

    assert tiers_tool.tests_for_paths(
        ["AGENTS.md"], [pinned, protected, sweeper], root=root) == [pinned, protected]
