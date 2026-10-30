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
