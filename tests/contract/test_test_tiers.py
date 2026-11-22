# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
"""Every test file belongs to exactly one tier.

The shipped testing-discipline module tells adopters that a test's tier comes
from where it lives, and says Cairn's own suite is tiered. Ordinary tests are
grouped under ``unit/``, ``contract/``, ``integration/``, and ``security/``;
workflow tests and protected apparatus remain at their approved paths. The
recursively applied ``tests/test_tiers.json`` filename patterns assign tiers,
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
- The "system_independent" list in the configuration is checked: a pattern
  that places no file, matches a security-tier file or matches a file already
  in `RELEASE_EXCLUDED_TESTS` fails the check.
- `cert-files` lists the files Linux and Windows run at certification: every
  test file except the Cairn-only release exclusions, the release-only files
  and the system-independent files, so a new unlisted file is included.
  `--write` saves the same lines to a new absolute path and never replaces a
  file.
- `cert-files --host windows` keeps the release-only files listed for Windows
  and nothing else release-only; with no `--host` the selection is the one
  Linux and Windows share.
- The "release_only" groups in the configuration are checked: a pattern that
  places no file, a file two groups place, a file `system_independent` also
  lists, a malformed group, and a file of `RELEASE_EXCLUDED_TESTS` that no group
  places or that a group lists for Windows all fail the check.
- `release-only` prints the release-only files, one path per line, with the
  counts on standard error; `--host` keeps the files that host runs.
- `for` leaves a release-only test out unless a changed path is release
  machinery or is that test file; `--include-release-only` keeps it. The real
  configuration keeps every excluded file selectable from its own subject.
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

from tests._repo_root import repository_root

ROOT = repository_root(Path(__file__))
_spec = importlib.util.spec_from_file_location("_test_tiers_tool", ROOT / "tests" / "tier_inventory.py")
tiers_tool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tiers_tool)


def _config(tmp_path: Path, tiers: list[dict],
            independent: list[str] | None = None, *,
            release_only: object = None,
            release_paths: list[str] | None = None) -> Path:
    path = tmp_path / "tiers.json"
    data = {"tiers": tiers}
    if independent is not None or release_only is not None:
        data["hosts"] = {"about": "", "system_independent": independent or []}
        if release_only is not None:
            data["hosts"]["release_only"] = release_only
        if release_paths is not None:
            data["hosts"]["release_paths"] = release_paths
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _tests(tmp_path: Path, *stems: str) -> Path:
    folder = tmp_path / "tests"
    folder.mkdir()
    for stem in stems:
        (folder / f"{stem}.py").write_text("", encoding="utf-8")
    return folder


def _excluded(folder: Path, *paths: str) -> None:
    """Write the manifest's exclusion list, in its real shape, beside the tests."""
    rows = tuple((path, ("tool.py",), "Cairn-only.") for path in paths)
    (folder / "security_manifest.py").write_text(
        "RELEASE_EXCLUDED_TESTS: tuple[tuple[str, tuple[str, ...], str], ...] = "
        f"{rows!r}\n", encoding="utf-8")


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


_HOST_TIERS = [
    {"name": "security", "about": "", "patterns": ["test_hostile_*"]},
    {"name": "unit", "about": "", "patterns": ["test_*"]},
]


def test_a_system_independent_pattern_that_places_no_file_fails_the_check(tmp_path):
    folder = _tests(tmp_path, "test_prose")
    _excluded(folder)
    config = _config(tmp_path, _HOST_TIERS, ["test_prose", "test_gone"])
    code, err = _check(config, folder)
    assert code == 1
    assert "'test_gone' places no test file" in err
    assert "'test_prose'" not in err


def test_a_system_independent_pattern_matching_a_security_file_fails_the_check(tmp_path):
    folder = _tests(tmp_path, "test_hostile_links", "test_prose")
    _excluded(folder)
    config = _config(tmp_path, _HOST_TIERS, ["test_hostile_*", "test_prose"])
    code, err = _check(config, folder)
    assert code == 1
    assert "'test_hostile_*' matches test_hostile_links.py in the security tier" in err
    assert "test_prose" not in err


def test_a_system_independent_pattern_matching_an_excluded_file_fails_the_check(tmp_path):
    folder = _tests(tmp_path, "test_signing", "test_prose")
    _excluded(folder, "tests/test_signing.py")
    config = _config(tmp_path, _HOST_TIERS, ["test_signing", "test_prose"])
    code, err = _check(config, folder)
    assert code == 1
    assert "'test_signing' matches test_signing.py" in err
    assert "RELEASE_EXCLUDED_TESTS" in err
    assert "test_prose" not in err


def test_cert_files_omits_excluded_and_independent_files_and_keeps_a_new_one(tmp_path):
    folder = _tests(tmp_path, "test_signing", "test_prose", "test_hostile_links",
                    "test_brand_new")
    (folder / "deeper").mkdir()
    (folder / "deeper" / "test_nested.py").write_text("", encoding="utf-8")
    _excluded(folder, "tests/test_signing.py")
    config = _config(tmp_path, _HOST_TIERS, ["test_prose"])
    assert _check(config, folder) == (0, "")

    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(["cert-files"], config=config, test_dir=folder,
                           root=tmp_path, out=out, err=err)

    assert code == 0, err.getvalue()
    assert out.getvalue().splitlines() == [
        "tests/deeper/test_nested.py",
        "tests/test_brand_new.py",
        "tests/test_hostile_links.py",
    ]
    assert "3 of 5 test files" in err.getvalue()


def test_cert_files_write_refuses_an_existing_path_and_leaves_it_alone(tmp_path):
    folder = _tests(tmp_path, "test_one")
    _excluded(folder)
    config = _config(tmp_path, _HOST_TIERS, [])
    existing = tmp_path / "already.txt"
    existing.write_text("keep me\n", encoding="utf-8")
    out, err = io.StringIO(), io.StringIO()

    code = tiers_tool.main(["cert-files", "--write", str(existing)], config=config,
                           test_dir=folder, root=tmp_path, out=out, err=err)

    assert code == 2
    assert "already exists" in err.getvalue()
    assert existing.read_text(encoding="utf-8") == "keep me\n"


def test_cert_files_write_saves_the_printed_lines_to_a_new_absolute_path(
        tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    folder = _tests(tmp_path, "test_one", "test_two")
    _excluded(folder)
    config = _config(tmp_path, _HOST_TIERS, [])
    target = tmp_path / "cert-files.txt"
    out, err = io.StringIO(), io.StringIO()

    code = tiers_tool.main(["cert-files", "--write", str(target)], config=config,
                           test_dir=folder, root=tmp_path, out=out, err=err)

    assert code == 0, err.getvalue()
    assert target.read_text(encoding="utf-8") == "tests/test_one.py\ntests/test_two.py\n"
    assert out.getvalue() == target.read_text(encoding="utf-8")

    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(["cert-files", "--write", "relative.txt"], config=config,
                           test_dir=folder, root=tmp_path, out=out, err=err)
    assert code == 2
    assert "absolute" in err.getvalue()
    assert not (tmp_path / "relative.txt").exists()


def _group(patterns: list[str], hosts: tuple[str, ...] = ("mac",),
           reason: str = "Tests Cairn's own cut.") -> dict:
    return {"hosts": list(hosts), "reason": reason, "patterns": list(patterns)}


def _release_config(tmp_path: Path, groups: object, *,
                    independent: list[str] | None = None,
                    paths: list[str] | None = None) -> Path:
    return _config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}],
                   independent or [], release_only=groups, release_paths=paths)


def _posix_lines(out: io.StringIO) -> list[str]:
    """The lines written to *out* with `/` in every path; the tool names a file in
    the host's own spelling (`tests\\test_x.py` on Windows)."""
    return out.getvalue().replace(os.sep, "/").splitlines()


def _run(verb: list[str], config: Path, folder: Path,
         root: Path) -> tuple[int, list[str], str]:
    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(verb, config=config, test_dir=folder, root=root,
                           out=out, err=err)
    return code, out.getvalue().replace("\\", "/").splitlines(), err.getvalue()


def test_a_release_only_pattern_that_places_no_file_fails_the_check(tmp_path):
    folder = _tests(tmp_path, "test_cut", "test_prose")
    _excluded(folder)
    config = _release_config(tmp_path, [_group(["test_cut", "test_gone"])])
    code, err = _check(config, folder)
    assert code == 1
    assert "release_only pattern 'test_gone' places no test file" in err
    assert "'test_cut'" not in err


def test_a_file_two_release_only_groups_place_fails_the_check(tmp_path):
    folder = _tests(tmp_path, "test_cut", "test_other")
    _excluded(folder)
    config = _release_config(tmp_path, [
        _group(["test_cut"]),
        _group(["test_cu*"], hosts=("mac", "windows")),
    ])
    code, err = _check(config, folder)
    assert code == 1
    assert "release_only groups both place test_cut.py" in err
    assert "test_other" not in err


def test_a_file_on_both_release_only_and_system_independent_fails_the_check(tmp_path):
    folder = _tests(tmp_path, "test_cut", "test_prose")
    _excluded(folder)
    config = _release_config(tmp_path, [_group(["test_cut"])],
                             independent=["test_cut", "test_prose"])
    code, err = _check(config, folder)
    assert code == 1
    assert "test_cut.py is on both release_only and system_independent" in err
    assert "test_prose" not in err


def test_an_excluded_file_no_release_only_group_places_fails_the_check(tmp_path):
    folder = _tests(tmp_path, "test_signing", "test_cut")
    (folder / "deeper").mkdir()
    (folder / "deeper" / "test_nested.py").write_text("", encoding="utf-8")
    _excluded(folder, "tests/test_signing.py", "tests/deeper/test_nested.py")
    config = _release_config(tmp_path, [_group(["test_signing", "test_cut"])])
    code, err = _check(config, folder)
    assert code == 1
    assert ("RELEASE_EXCLUDED_TESTS lists tests/deeper/test_nested.py, but no "
            "release_only pattern places it") in err
    assert "tests/test_signing.py" not in err

    code, err = _check(_release_config(tmp_path, []), folder)
    assert code == 1
    assert "tests/test_signing.py" in err and "tests/deeper/test_nested.py" in err


def test_an_excluded_file_listed_for_windows_fails_the_check(tmp_path):
    folder = _tests(tmp_path, "test_signing", "test_strict")
    _excluded(folder, "tests/test_signing.py")
    config = _release_config(tmp_path, [
        _group(["test_signing"], hosts=("mac", "windows")),
        _group(["test_strict"], hosts=("mac", "windows")),
    ])
    code, err = _check(config, folder)
    assert code == 1
    assert ("RELEASE_EXCLUDED_TESTS keeps tests/test_signing.py to the Mac, "
            "but release_only lists it for windows") in err
    assert "test_strict" not in err


def test_a_consistent_release_only_list_passes_the_check(tmp_path):
    folder = _tests(tmp_path, "test_signing", "test_strict", "test_prose")
    _excluded(folder, "tests/test_signing.py")
    config = _release_config(tmp_path, [
        _group(["test_signing"]),
        _group(["test_strict"], hosts=("mac", "windows")),
    ], independent=["test_prose"])
    assert _check(config, folder) == (0, "")


@pytest.mark.parametrize("groups, message", [
    pytest.param({"hosts": ["mac"]}, "'release_only' must be a list", id="not-a-list"),
    pytest.param(["test_cut"], "group 1 must be an object", id="not-an-object"),
    pytest.param([_group(["test_cut"], hosts=("windows",))],
                 "group 1 needs a 'hosts' list", id="no-mac"),
    pytest.param([_group(["test_cut"], hosts=("mac", "linux"))],
                 "group 1 needs a 'hosts' list", id="unknown-host"),
    pytest.param([_group(["test_cut"], hosts=("mac", "mac"))],
                 "group 1 needs a 'hosts' list", id="repeated-host"),
    pytest.param([_group(["test_cut"], reason=" ")],
                 "group 1 needs a 'reason'", id="blank-reason"),
    pytest.param([_group([])], "group 1 needs a non-empty list of 'patterns'",
                 id="no-patterns"),
])
def test_a_malformed_release_only_group_is_refused_plainly(tmp_path, groups, message):
    folder = _tests(tmp_path, "test_cut")
    _excluded(folder)
    code, err = _check(_release_config(tmp_path, groups), folder)
    assert code == 2
    assert "invalid tier configuration" in err and message in err


def _cert_tree(tmp_path: Path) -> tuple[Path, Path]:
    folder = _tests(tmp_path, "test_signing", "test_cut", "test_strict",
                    "test_prose", "test_ordinary")
    (folder / "deeper").mkdir()
    (folder / "deeper" / "test_nested.py").write_text("", encoding="utf-8")
    _excluded(folder, "tests/test_signing.py")
    config = _release_config(tmp_path, [
        _group(["test_signing", "test_cut"]),
        _group(["test_strict"], hosts=("mac", "windows")),
    ], independent=["test_prose"])
    assert _check(config, folder) == (0, "")
    return config, folder


def test_cert_files_leaves_out_release_only_files_and_host_windows_adds_one_back(
        tmp_path):
    config, folder = _cert_tree(tmp_path)
    shared = ["tests/deeper/test_nested.py", "tests/test_ordinary.py"]

    code, lines, err = _run(["cert-files"], config, folder, tmp_path)
    assert code == 0, err
    assert lines == shared
    assert "2 of 6 test files run on Linux and Windows" in err

    assert _run(["cert-files", "--host", "linux"], config, folder, tmp_path)[1] == shared

    code, lines, err = _run(["cert-files", "--host", "windows"], config, folder,
                            tmp_path)
    assert code == 0, err
    assert lines == shared + ["tests/test_strict.py"]
    assert "3 of 6 test files run on Windows" in err
    assert "release-only files listed for Windows and kept: 1" in err


def test_release_only_prints_the_files_with_counts_and_filters_by_host(tmp_path):
    config, folder = _cert_tree(tmp_path)

    code, lines, err = _run(["release-only"], config, folder, tmp_path)
    assert code == 0, err
    assert lines == ["tests/test_cut.py", "tests/test_signing.py",
                     "tests/test_strict.py"]
    assert "release-only: 3 of 6 test files (3 run on the Mac, 1 of them also on Windows)" in err

    code, lines, err = _run(["release-only", "--host", "windows"], config, folder,
                            tmp_path)
    assert code == 0, err
    assert lines == ["tests/test_strict.py"]
    assert "release-only: 1 of 6 test files run on windows" in err

    code, lines, err = _run(["release-only", "--host", "mac"], config, folder,
                            tmp_path)
    assert code == 0 and len(lines) == 3


def test_release_only_prints_nothing_when_the_configuration_has_no_list(tmp_path):
    folder = _tests(tmp_path, "test_one")
    _excluded(folder)
    config = _config(tmp_path, _HOST_TIERS, [])
    code, lines, err = _run(["release-only"], config, folder, tmp_path)
    assert code == 0 and lines == []
    assert "release-only: 0 of 1 test files" in err


def _for_tree(tmp_path: Path) -> tuple[Path, Path]:
    for rel in ("tools/example.py", "release/step.py"):
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("VALUE = 1\n", encoding="utf-8")
    folder = _tests(tmp_path, "test_cut", "test_plain")
    (folder / "test_cut.py").write_text(
        'import tools.example\nSTEP = "release/step.py"\n', encoding="utf-8")
    (folder / "test_plain.py").write_text(
        "import tools.example\n", encoding="utf-8")
    _excluded(folder)
    config = _release_config(tmp_path, [_group(["test_cut"])],
                             paths=["release/*"])
    return config, folder


def test_for_holds_back_a_release_only_test_an_ordinary_change_does_not_touch(
        tmp_path):
    config, folder = _for_tree(tmp_path)

    code, lines, err = _run(["for", "tools/example.py"], config, folder, tmp_path)
    assert code == 0, err
    assert lines == ["tests/test_plain.py"]
    assert "1 test files selected for the requested paths" in err
    assert "1 release-only test files held back" in err
    assert "tests/test_cut.py" in err


def test_for_keeps_a_release_only_test_when_a_changed_path_is_release_machinery(
        tmp_path):
    config, folder = _for_tree(tmp_path)

    code, lines, err = _run(["for", "release/step.py"], config, folder, tmp_path)
    assert code == 0, err
    assert lines == ["tests/test_cut.py"]
    assert "held back" not in err

    code, lines, err = _run(["for", "tools/example.py", "release/step.py"], config,
                            folder, tmp_path)
    assert code == 0, err
    assert lines == ["tests/test_cut.py", "tests/test_plain.py"]


def test_for_keeps_a_release_only_test_that_is_itself_the_changed_file(tmp_path):
    config, folder = _for_tree(tmp_path)

    code, lines, err = _run(["for", "tests/test_cut.py"], config, folder, tmp_path)
    assert code == 0, err
    assert lines == ["tests/test_cut.py"]


def test_for_include_release_only_keeps_what_an_ordinary_change_would_hold_back(
        tmp_path):
    config, folder = _for_tree(tmp_path)

    code, lines, err = _run(["for", "--include-release-only", "tools/example.py"],
                            config, folder, tmp_path)
    assert code == 0, err
    assert lines == ["tests/test_cut.py", "tests/test_plain.py"]
    assert "held back" not in err


def _real_release_rows() -> tuple[tuple[str, tuple[str, ...], str], ...]:
    spec = importlib.util.spec_from_file_location(
        "_real_security_manifest_for_release_only", ROOT / "tests" / "security_manifest.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.RELEASE_EXCLUDED_TESTS


def test_the_real_release_only_list_places_every_excluded_file_for_the_mac_only():
    files = tiers_tool.find_test_files()
    groups, _paths = tiers_tool.load_release_only()
    assert tiers_tool.release_only_problems(
        groups, files, tiers_tool.load_hosts(),
        tiers_tool.load_release_excluded(), tiers_tool.TEST_DIR) == []
    placed, _doubled = tiers_tool.release_only_files(groups, files)
    by_path = {tiers_tool._repo_path(p, tiers_tool.TEST_DIR): hosts
               for p, hosts in placed.items()}
    for path, _subjects, _reason in _real_release_rows():
        assert by_path[path] == ("mac",), path


def test_the_real_configuration_keeps_each_excluded_file_selectable_from_its_subject():
    files = tiers_tool.find_test_files()
    groups, machinery = tiers_tool.load_release_only()
    by_path = {tiers_tool._repo_path(p, tiers_tool.TEST_DIR): p for p in files}
    for path, subjects, _reason in _real_release_rows():
        for subject in subjects:
            kept, held = tiers_tool.drop_unrelated_release_only(
                [by_path[path]], [subject], groups, machinery, files, ROOT)
            assert kept == [by_path[path]] and held == [], (path, subject)
    kept, held = tiers_tool.drop_unrelated_release_only(
        [by_path["tests/test_repin.py"]], ["dev/tools/meter.py"], groups, machinery,
        files, ROOT)
    assert kept == [] and held == [by_path["tests/test_repin.py"]]


def test_the_real_cert_files_send_only_the_strict_native_check_to_windows():
    def listed(*verb):
        out, err = io.StringIO(), io.StringIO()
        assert tiers_tool.main(["cert-files", *verb], out=out, err=err) == 0, err.getvalue()
        return set(out.getvalue().splitlines())

    release_only = {tiers_tool._repo_path(p, tiers_tool.TEST_DIR)
                    for p in tiers_tool.release_only_files(
                        tiers_tool.load_release_only()[0],
                        tiers_tool.find_test_files())[0]}
    shared = listed()
    assert not shared & release_only
    assert listed("--host", "windows") - shared == {"tests/test_security_check.py"}
    assert (listed("--host", "windows") & release_only
            == {"tests/test_security_check.py"})
    assert "tests/test_security_check.py" not in shared


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
    assert _posix_lines(out) == [
        "tests/test_cites_agents.py",
        "tests/test_imports_example.py",
        "tests/test_imports_from_example.py",
    ]
    assert "3 test files" in err.getvalue()


def test_for_matches_python_references_as_tokens_and_keeps_indirect_consumers(tmp_path):
    target = tmp_path / "install" / "_scaffold" / "upgrade.py"
    target.parent.mkdir(parents=True)
    target.write_text("VALUE = 1\n", encoding="utf-8")
    tests = _tests(tmp_path, "test_imports_upgrade", "test_cites_upgrade",
                   "test_runs_upgrade", "test_cites_upgrade_helper",
                   "test_parenthesized_import_upgrade",
                   "test_incidental_upgrade_words")
    (tests / "test_imports_upgrade.py").write_text(
        "from install._scaffold import upgrade as UP\n", encoding="utf-8")
    (tests / "test_cites_upgrade.py").write_text(
        'SOURCE = "install/_scaffold/upgrade.py"\n', encoding="utf-8")
    (tests / "test_runs_upgrade.py").write_text(
        'def test_public_command(project):\n    upgrade(project, "--apply")\n'
        'COMMAND = "scaffold.py upgrade --apply"\n',
        encoding="utf-8")
    (tests / "test_cites_upgrade_helper.py").write_text(
        'PROTECTED = "_apply_upgrade"\n', encoding="utf-8")
    (tests / "test_parenthesized_import_upgrade.py").write_text(
        "from install._scaffold import (\n"
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
        ["for", "install/_scaffold/upgrade.py"],
        config=_config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}]),
        test_dir=tests, root=tmp_path, out=out, err=err)
    assert code == 0
    assert _posix_lines(out) == [
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
    assert _posix_lines(out) == ["tests/test_changed.py"]


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
    assert _posix_lines(out) == ["tests/test_imports_example.py"]


def test_for_keeps_named_readers_and_unions_other_changed_paths(tmp_path):
    root = tmp_path
    for rel in (
        "dev/.cairn/cairn-lock.yml",
        "dev/agent_collaboration.md",
        "templates/core/dev/agent_collaboration.md",
        "tools/example.py",
    ):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture\n", encoding="utf-8")

    tests = root / "tests"
    tests.mkdir(parents=True)
    sources = {
        "test_lock_mention.py": 'PATH = "dev/.cairn/cairn-lock.yml"\n',
        "test_portable_security_sweeps.py": (
            'LOCK = "dev/.cairn/cairn-lock.yml"\n'
            "read_lockfile(CAIRN_ROOT)\n"
        ),
        "contract/test_writing_rules_ship.py": (
            'SOURCE = "dev/agent_collaboration.md"\n'
            'SHIPPED = "templates/core/dev/agent_collaboration.md"\n'
        ),
        "test_review_stance_in_shipped_files.py": (
            'SOURCE = "dev/agent_collaboration.md"\n'
            'SHIPPED = "templates/core/dev/agent_collaboration.md"\n'
        ),
        "test_review_sweep_ships.py": (
            'SOURCE = "dev/agent_collaboration.md"\n'
            'SHIPPED = "templates/core/dev/agent_collaboration.md"\n'
        ),
        "test_fake_guide_reader.py": (
            'SOURCE = "dev/agent_collaboration.md"\n'
            'SHIPPED = "templates/core/dev/agent_collaboration.md"\n'
        ),
        "test_imports_example.py": "import tools.example\n",
    }
    for rel, source in sources.items():
        path = tests / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")

    config = _config(tmp_path, [{"name": "unit", "about": "", "patterns": ["test_*"]}])
    out, err = io.StringIO(), io.StringIO()
    code = tiers_tool.main(
        ["for", "dev/.cairn/cairn-lock.yml", "dev/agent_collaboration.md",
         "templates/core/dev/agent_collaboration.md", "tools/example.py"],
        config=config, test_dir=tests, root=root, out=out, err=err)

    assert code == 0, err.getvalue()
    assert _posix_lines(out) == [
        "tests/contract/test_writing_rules_ship.py",
        "tests/test_imports_example.py",
        "tests/test_portable_security_sweeps.py",
        "tests/test_review_stance_in_shipped_files.py",
        "tests/test_review_sweep_ships.py",
    ]


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
        _assert_bound_member_positive(tmp_path, "tests/tier_inventory.py")

    def test_real_cli_resolves_linked_tools_parent_with_caller_and_helper(
            self, tmp_path: Path) -> None:
        _assert_linked_caller_parent_positive(tmp_path, "tests/tier_inventory.py")

    @pytest.mark.parametrize("mutation", _BINDING_MUTATIONS)
    def test_real_cli_refuses_each_binding_mutation(
            self, mutation: str, tmp_path: Path) -> None:
        _assert_bound_member_mutation(tmp_path, "tests/tier_inventory.py", mutation)


def _seed_tier_route_repo(root: Path) -> None:
    root.mkdir()
    (root / "tools").mkdir()
    (root / "tests").mkdir(parents=True)
    (root / "tests/test_tiers.json").write_text(
        json.dumps({"tiers": [{"name": "one", "patterns": ["test_*"]}]}),
        encoding="utf-8",
    )
    reader = root / "tests/test_reader.py"
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
    subprocess.run(["git", "-C", str(root), "add", "AGENTS.md", "tests/test_tiers.json",
                    "tests/test_reader.py"], env=env,
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
    assert code == 0 and out.getvalue().splitlines() == ["tests/test_reader.py"]
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
        tmp_path / "tiers-agents-diff", "tests/tier_inventory.py", "_resolve_reviewed_range",
        ("rev-parse", "--verify", "--end-of-options", "HEAD~1^{commit}"),
        _tier_route_driver("HEAD~1..HEAD"),
        _tier_route_driver("HEAD~1..HEAD", refusal=True),
        seed=_seed_tier_route_repo)
    assert clean.stdout == "route-positive\n"
