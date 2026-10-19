# SPDX-License-Identifier: MIT
"""Contract and safety tests for tools/board.py and its JSON data mode."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]


def _load_board():
    path = CAIRN_ROOT / "tools" / "board.py"
    spec = importlib.util.spec_from_file_location("_cairn_board_contract", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


board = _load_board()


def _write(root: Path, rel: str, content: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _build_golden_main_tree(root: Path) -> None:
    """Build a no-symlink tree covering every header, status, wait, fence and
    roadmap row shape handled by the terminal board modes."""
    _write(
        root,
        "dev/proposals/2026-01-01-full.md",
        "# Proposal: Full header\n\n"
        "**Status**: awaiting-review\n"
        "**Review**: usual + Security Review\n"
        "**Plan review**: required(Internal)\n"
        "**Opened**: 2026-01-01\n"
        "**Source proposal**: none\n"
        "**In brief**: One plain sentence.\n\n"
        "## Context\nMAINTAINER-GATED in proposal body.\n",
    )
    _write(
        root,
        "dev/proposals/2026-01-02-quirks.md",
        "# Proposal: Quirks\n\n"
        "  **Status**: first-value\n"
        "##notaheading\n"
        "   **Status**: awaiting-decision \u2014 note after word\n"
        "**Opened**: 2026-01-02\n\n"
        "## First section\n"
        "**Status**: below-heading\n",
    )
    _write(
        root,
        "dev/proposals/2026-01-03-no-headers.md",
        "# Proposal without header fields\n\nPlain body before heading.\n\n## Section\n",
    )
    _write(
        root,
        "dev/proposals/2026-01-04-decide-plain.md",
        "# Decide plain\n\n**Status**: awaiting-decision\n\n## Body\n",
    )
    _write(
        root,
        "dev/proposals/2026-01-05-decide-hyphen.md",
        "# Decide hyphen\n\n**Status**: awaiting-decision-x\n\n## Body\n",
    )
    _write(
        root,
        "dev/proposals/2026-01-06-decide-s.md",
        "# Decide plural\n\n**Status**: awaiting-decisions\n\n## Body\n",
    )
    _write(
        root,
        "dev/proposals/2026-01-07-decide-under.md",
        "# Decide underscore\n\n**Status**: awaiting-decision_x\n\n## Body\n",
    )
    _write(
        root,
        "dev/proposals/2026-01-08-decide-digit.md",
        "# Decide digit\n\n**Status**: awaiting-decision2\n\n## Body\n",
    )
    _write(
        root,
        "dev/proposals/_template.md",
        "# Template\n\n**Status**: awaiting-decision\n\n## Body\n",
    )
    _write(
        root,
        "dev/proposals/_notes.md",
        "# Notes\n\n**Status**: awaiting-decision\n\n## Body\n",
    )
    _write(
        root,
        "dev/plans/wait-blank.md",
        "# Plan blank wait\n\n"
        "**Status**: implementing\n"
        "**Waiting on Maintainer**:\n\n"
        "## Body\n",
    )
    _write(
        root,
        "dev/plans/wait-space-field.md",
        "# Plan spaced field\n\n"
        "**Status**: implementing\n"
        "**Waiting on Maintainer **: spaced field name\n\n"
        "## Body\n",
    )
    _write(
        root,
        "dev/plans/wait-lower.md",
        "# Plan lower wait\n\n"
        "**Status**: implementing\n"
        "**waiting on maintainer**: lower case not read\n\n"
        "## Body\n",
    )
    _write(
        root,
        "dev/plans/wait-long.md",
        "# Plan long wait\n\n"
        "**Status**: implementing\n"
        "**Waiting on Maintainer**: "
        + ("L" * 60)
        + "\n\n## Body\n",
    )
    _write(
        root,
        "dev/plans/fence-only.md",
        "# Plan fence only\n\n"
        "**Status**: implementing\n\n"
        "## Body\nContains MAINTAINER-ONLY chunk.\n",
    )
    _write(
        root,
        "dev/plans/fence-gated.md",
        "# Plan fence gated\n\n"
        "**Status**: implementing\n\n"
        "## Body\nContains MAINTAINER-GATED chunk.\n",
    )
    _write(
        root,
        "dev/plans/archive/done-plain.md",
        "# Archived plain\n\n**Status**: archived\n\n## Body\n",
    )
    _write(
        root,
        "dev/plans/archive/done-wait.md",
        "# Archived wait\n\n"
        "**Status**: archived\n"
        "**Waiting on Maintainer**: old wait\n\n"
        "## Body\nMAINTAINER-ONLY\n",
    )
    _write(
        root,
        "dev/PLANNING.md",
        "# Planning\n\n"
        "**Waiting on Maintainer**: plain row\n"
        "  **Waiting on Maintainer**: indented row\n"
        "  * **Waiting on Maintainer**: sub-bullet row\n"
        "- **Waiting on Maintainer**: dash-bullet row\n"
        "* **Waiting on Maintainer **: spaced marker row\n"
        "* **waiting on maintainer**: lower marker row\n"
        "*\t**Waiting on Maintainer**: tab after bullet\n"
        "* * **Waiting on Maintainer**: double bullet\n"
        "A sentence mentioning **Waiting on Maintainer**: in prose.\n"
        "Line with\x0cform feed and\u2028line sep before\n"
        "* **Waiting on Maintainer**: after special breaks\n",
    )


_GOLDEN_MAIN = {
    (): (
        "board: kind | artifact | Status | Review | Plan review | Opened | Source proposal | Waiting on Maintainer\n"
        "board: proposal | 2026-01-01-full | awaiting-review | usual + Security Review | required(Internal) | 2026-01-01 | none | \n"
        "board: proposal | 2026-01-02-quirks | awaiting-decision \u2014 note after word |  |  | 2026-01-02 |  | \n"
        "board: proposal | 2026-01-04-decide-plain | awaiting-decision |  |  |  |  | \n"
        "board: proposal | 2026-01-05-decide-hyphen | awaiting-decision-x |  |  |  |  | \n"
        "board: proposal | 2026-01-06-decide-s | awaiting-decisions |  |  |  |  | \n"
        "board: proposal | 2026-01-07-decide-under | awaiting-decision_x |  |  |  |  | \n"
        "board: proposal | 2026-01-08-decide-digit | awaiting-decision2 |  |  |  |  | \n"
        "board: plan | fence-gated | implementing |  |  |  |  | \n"
        "board: plan | fence-only | implementing |  |  |  |  | \n"
        "board: plan | wait-blank | implementing |  |  |  |  | \n"
        "board: plan | wait-long | implementing |  |  |  |  | LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL\u2026\n"
        "board: plan | wait-lower | implementing |  |  |  |  | \n"
        "board: plan | wait-space-field | implementing |  |  |  |  | spaced field name\n"
        "board: 13 row(s). Derived from header blocks; the artifact is authoritative.\n"
    ),
    ("--archive",): (
        "board: kind | artifact | Status | Review | Plan review | Opened | Source proposal | Waiting on Maintainer | archived\n"
        "board: proposal | 2026-01-01-full | awaiting-review | usual + Security Review | required(Internal) | 2026-01-01 | none |  | \n"
        "board: proposal | 2026-01-02-quirks | awaiting-decision \u2014 note after word |  |  | 2026-01-02 |  |  | \n"
        "board: proposal | 2026-01-04-decide-plain | awaiting-decision |  |  |  |  |  | \n"
        "board: proposal | 2026-01-05-decide-hyphen | awaiting-decision-x |  |  |  |  |  | \n"
        "board: proposal | 2026-01-06-decide-s | awaiting-decisions |  |  |  |  |  | \n"
        "board: proposal | 2026-01-07-decide-under | awaiting-decision_x |  |  |  |  |  | \n"
        "board: proposal | 2026-01-08-decide-digit | awaiting-decision2 |  |  |  |  |  | \n"
        "board: plan | fence-gated | implementing |  |  |  |  |  | \n"
        "board: plan | fence-only | implementing |  |  |  |  |  | \n"
        "board: plan | wait-blank | implementing |  |  |  |  |  | \n"
        "board: plan | wait-long | implementing |  |  |  |  | LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL\u2026 | \n"
        "board: plan | wait-lower | implementing |  |  |  |  |  | \n"
        "board: plan | wait-space-field | implementing |  |  |  |  | spaced field name | \n"
        "board: plan | done-plain | archived |  |  |  |  |  | yes\n"
        "board: plan | done-wait | archived |  |  |  |  | old wait | yes\n"
        "board: 15 row(s). Derived from header blocks; the artifact is authoritative.\n"
    ),
    ("--maintainer",): (
        "board: kind | artifact | reason | text\n"
        "board: proposal | 2026-01-02-quirks | awaiting-decision | \n"
        "board: proposal | 2026-01-04-decide-plain | awaiting-decision | \n"
        "board: proposal | 2026-01-05-decide-hyphen | awaiting-decision | \n"
        "board: plan | wait-blank | declared | \n"
        "board: plan | wait-long | declared | LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL\u2026\n"
        "board: plan | wait-space-field | declared | spaced field name\n"
        "board: roadmap | dev/PLANNING.md:3 | declared | plain row\n"
        "board: roadmap | dev/PLANNING.md:4 | declared | indented row\n"
        "board: roadmap | dev/PLANNING.md:5 | declared | sub-bullet row\n"
        "board: roadmap | dev/PLANNING.md:6 | declared | dash-bullet row\n"
        "board: roadmap | dev/PLANNING.md:7 | declared | spaced marker row\n"
        "board: roadmap | dev/PLANNING.md:15 | declared | after special breaks\n"
        "board: 12 waiting on the Maintainer, as authors declared. The artifact or row is authoritative.\n"
        "board: advisory -- plans that mention a fence but declare no wait (open each): fence-gated, fence-only\n"
        "board: not listed -- pushes (git status shows them) and anything no artifact or row declares.\n"
    ),
    ("--maintainer", "--archive"): (
        "board: kind | artifact | reason | text\n"
        "board: proposal | 2026-01-02-quirks | awaiting-decision | \n"
        "board: proposal | 2026-01-04-decide-plain | awaiting-decision | \n"
        "board: proposal | 2026-01-05-decide-hyphen | awaiting-decision | \n"
        "board: plan | wait-blank | declared | \n"
        "board: plan | wait-long | declared | LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL\u2026\n"
        "board: plan | wait-space-field | declared | spaced field name\n"
        "board: roadmap | dev/PLANNING.md:3 | declared | plain row\n"
        "board: roadmap | dev/PLANNING.md:4 | declared | indented row\n"
        "board: roadmap | dev/PLANNING.md:5 | declared | sub-bullet row\n"
        "board: roadmap | dev/PLANNING.md:6 | declared | dash-bullet row\n"
        "board: roadmap | dev/PLANNING.md:7 | declared | spaced marker row\n"
        "board: roadmap | dev/PLANNING.md:15 | declared | after special breaks\n"
        "board: 12 waiting on the Maintainer, as authors declared. The artifact or row is authoritative.\n"
        "board: advisory -- plans that mention a fence but declare no wait (open each): fence-gated, fence-only\n"
        "board: not listed -- pushes (git status shows them) and anything no artifact or row declares.\n"
    ),
}

_GOLDEN_SMALL = {
    (): (
        "board: kind | artifact | Status\n"
        "board: proposal | 2026-01-01-a | awaiting-decision\n"
        "board: 1 row(s). Derived from header blocks; the artifact is authoritative.\n"
    ),
    ("--archive",): (
        "board: kind | artifact | Status\n"
        "board: proposal | 2026-01-01-a | awaiting-decision\n"
        "board: 1 row(s). Derived from header blocks; the artifact is authoritative.\n"
    ),
    ("--maintainer",): (
        "board: kind | artifact | reason | text\n"
        "board: proposal | 2026-01-01-a | awaiting-decision | \n"
        "board: 1 waiting on the Maintainer, as authors declared. The artifact or row is authoritative.\n"
        "board: advisory -- plans that mention a fence but declare no wait (open each): none\n"
        "board: not listed -- pushes (git status shows them) and anything no artifact or row declares.\n"
        "board: dev/PLANNING.md is missing -- no board rows were read.\n"
    ),
    ("--maintainer", "--archive"): (
        "board: kind | artifact | reason | text\n"
        "board: proposal | 2026-01-01-a | awaiting-decision | \n"
        "board: 1 waiting on the Maintainer, as authors declared. The artifact or row is authoritative.\n"
        "board: advisory -- plans that mention a fence but declare no wait (open each): none\n"
        "board: not listed -- pushes (git status shows them) and anything no artifact or row declares.\n"
        "board: dev/PLANNING.md is missing -- no board rows were read.\n"
    ),
}


class TestTerminalBoardIsUnchanged:
    """The terminal board and `--maintainer` outputs are byte-for-byte unchanged
    on trees with no symbolic links."""

    def test_terminal_modes_match_parent_golden_output(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """All four terminal flag combinations produce the exact parent bytes across
        the main tree, a tree missing `dev/PLANNING.md`, and a tree where
        `dev/PLANNING.md` is a directory."""
        main_tree = tmp_path / "main"
        _build_golden_main_tree(main_tree)
        for flags, expected in _GOLDEN_MAIN.items():
            rc = board.main([*flags, "--root", str(main_tree)])
            captured = capsys.readouterr()
            assert rc == 0
            assert captured.err == ""
            assert captured.out == expected

        no_planning = tmp_path / "no_planning"
        _write(
            no_planning,
            "dev/proposals/2026-01-01-a.md",
            "# A\n\n**Status**: awaiting-decision\n\n## Body\n",
        )
        for flags, expected in _GOLDEN_SMALL.items():
            rc = board.main([*flags, "--root", str(no_planning)])
            captured = capsys.readouterr()
            assert rc == 0
            assert captured.err == ""
            assert captured.out == expected

        dir_planning = tmp_path / "dir_planning"
        _write(
            dir_planning,
            "dev/proposals/2026-01-01-a.md",
            "# A\n\n**Status**: awaiting-decision\n\n## Body\n",
        )
        (dir_planning / "dev" / "PLANNING.md").mkdir(parents=True)
        for flags, expected in _GOLDEN_SMALL.items():
            rc = board.main([*flags, "--root", str(dir_planning)])
            captured = capsys.readouterr()
            assert rc == 0
            assert captured.err == ""
            assert captured.out == expected


def _build_ten_symlink_trees(base: Path) -> list[tuple[str, Path, list[str], bool]]:
    """Build the ten symlink test trees.

    Returns `(name, root, expected_skipped_paths, expects_planning_skipped)`.
    """
    outside = base / "outside"
    _write(
        outside,
        "secret-plan.md",
        "# Secret Plan\n\n"
        "**Status**: implementing\n"
        "**Waiting on Maintainer**: leaked-plan\n\n"
        "## Body\nMAINTAINER-ONLY\n",
    )
    _write(
        outside,
        "proposals-dir/2026-01-01-secret-prop.md",
        "# Secret Proposal\n\n**Status**: awaiting-decision\n\n## Body\n",
    )
    _write(
        outside,
        "secret-planning.md",
        "# Secret Planning\n\n* **Waiting on Maintainer**: leaked-roadmap\n",
    )
    _write(
        outside,
        "full-dev/plans/leaked-from-dev.md",
        "# Leaked from dev\n\n"
        "**Status**: implementing\n"
        "**Waiting on Maintainer**: leaked-dev\n\n"
        "## Body\n",
    )
    _write(
        outside,
        "full-dev/proposals/2026-01-01-leaked-from-dev.md",
        "# Leaked proposal\n\n**Status**: awaiting-decision\n\n## Body\n",
    )
    _write(
        outside,
        "full-dev/PLANNING.md",
        "# Leaked planning\n\n* **Waiting on Maintainer**: leaked-dev-roadmap\n",
    )
    _write(
        outside,
        "archive-dir/leaked-archive.md",
        "# Leaked archive\n\n"
        "**Status**: archived\n"
        "**Waiting on Maintainer**: leaked-arch\n\n"
        "## Body\n",
    )

    cases: list[tuple[str, Path, list[str], bool]] = []

    # 1. Plan leaf linked to file outside dev/
    r1 = base / "case_1_leaf_outside"
    _write(r1, "dev/plans/real.md", "# Real\n\n**Status**: implementing\n\n## Body\n")
    _write(r1, "dev/PLANNING.md", "# Board\n")
    (r1 / "dev" / "plans" / "linked-plan.md").symlink_to(outside / "secret-plan.md")
    cases.append(("leaf_outside", r1, ["dev/plans/linked-plan.md"], False))

    # 2. dev/proposals linked to folder outside dev/
    r2 = base / "case_2_proposals_outside"
    _write(r2, "dev/plans/real.md", "# Real\n\n**Status**: implementing\n\n## Body\n")
    _write(r2, "dev/PLANNING.md", "# Board\n")
    (r2 / "dev" / "proposals").symlink_to(outside / "proposals-dir")
    cases.append(("proposals_outside", r2, ["dev/proposals"], False))

    # 3. dev/PLANNING.md linked to file outside dev/
    r3 = base / "case_3_planning_outside"
    _write(r3, "dev/plans/real.md", "# Real\n\n**Status**: implementing\n\n## Body\n")
    (r3 / "dev" / "PLANNING.md").symlink_to(outside / "secret-planning.md")
    cases.append(("planning_outside", r3, ["dev/PLANNING.md"], True))

    # 4. dev itself linked
    r4 = base / "case_4_dev_linked"
    r4.mkdir(parents=True)
    (r4 / "dev").symlink_to(outside / "full-dev")
    cases.append(("dev_linked", r4, ["dev"], True))

    # 5. dev/plans/archive linked (tested with --archive)
    r5 = base / "case_5_archive_linked"
    _write(r5, "dev/plans/real.md", "# Real\n\n**Status**: implementing\n\n## Body\n")
    _write(r5, "dev/PLANNING.md", "# Board\n")
    (r5 / "dev" / "plans" / "archive").symlink_to(outside / "archive-dir")
    cases.append(("archive_linked", r5, ["dev/plans/archive"], False))

    # 6. Dangling folder link (dev/plans)
    r6 = base / "case_6_dangling_plans"
    _write(
        r6,
        "dev/proposals/2026-01-01-real.md",
        "# Real\n\n**Status**: awaiting-review\n\n## Body\n",
    )
    _write(r6, "dev/PLANNING.md", "# Board\n")
    (r6 / "dev" / "plans").symlink_to(outside / "does-not-exist")
    cases.append(("dangling_plans", r6, ["dev/plans"], False))

    # 7. Folder linked to itself (dev/plans -> plans)
    r7 = base / "case_7_loop_plans"
    _write(
        r7,
        "dev/proposals/2026-01-01-real.md",
        "# Real\n\n**Status**: awaiting-review\n\n## Body\n",
    )
    _write(r7, "dev/PLANNING.md", "# Board\n")
    os.symlink("plans", r7 / "dev" / "plans")
    cases.append(("loop_plans", r7, ["dev/plans"], False))

    # 8. Dangling dev/PLANNING.md
    r8 = base / "case_8_dangling_planning"
    _write(r8, "dev/plans/real.md", "# Real\n\n**Status**: implementing\n\n## Body\n")
    (r8 / "dev" / "PLANNING.md").symlink_to(outside / "missing-planning.md")
    cases.append(("dangling_planning", r8, ["dev/PLANNING.md"], True))

    # 9. Leaf linked to itself
    r9 = base / "case_9_loop_leaf"
    _write(r9, "dev/plans/real.md", "# Real\n\n**Status**: implementing\n\n## Body\n")
    _write(r9, "dev/PLANNING.md", "# Board\n")
    os.symlink("self.md", r9 / "dev" / "plans" / "self.md")
    cases.append(("loop_leaf", r9, ["dev/plans/self.md"], False))

    # 10. Link to a file inside dev/
    r10 = base / "case_10_leaf_inside_dev"
    _write(
        r10,
        "dev/proposals/2026-01-01-target.md",
        "# Target inside dev\n\n**Status**: awaiting-decision\n\n## Body\n",
    )
    _write(r10, "dev/plans/real.md", "# Real\n\n**Status**: implementing\n\n## Body\n")
    _write(r10, "dev/PLANNING.md", "# Board\n")
    (r10 / "dev" / "plans" / "inside-link.md").symlink_to(
        r10 / "dev" / "proposals" / "2026-01-01-target.md"
    )
    cases.append(("leaf_inside_dev", r10, ["dev/plans/inside-link.md"], False))

    return cases


class TestSymlinkedSourcesAreNotRead:
    """Every path component below the resolved root is checked with `lstat` /
    `is_symlink` before any link-following operation."""

    def test_symlinked_sources_are_skipped_and_named_in_all_modes(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """None of the ten symlink configurations is read in any terminal mode;
        each is named once on a skip line by its highest linked component, and a
        linked or dangling roadmap file is never also reported as missing."""
        cases = _build_ten_symlink_trees(tmp_path)
        for name, root, expected_skips, planning_skipped in cases:
            for flags in (
                (),
                ("--archive",),
                ("--maintainer",),
                ("--maintainer", "--archive"),
            ):
                rc = board.main([*flags, "--root", str(root)])
                captured = capsys.readouterr()
                assert rc == 0, f"{name} {flags}: rc={rc}, err={captured.err}"
                assert captured.err == ""
                out = captured.out
                non_skip_out = "\n".join(
                    line
                    for line in out.splitlines()
                    if not line.startswith(
                        "board: skipped (symbolic link, not read): "
                    )
                )
                for leaked in (
                    "linked-plan",
                    "2026-01-01-secret-prop",
                    "leaked-plan",
                    "leaked-roadmap",
                    "leaked-from-dev",
                    "2026-01-01-leaked-from-dev",
                    "leaked-dev",
                    "leaked-dev-roadmap",
                    "leaked-archive",
                    "leaked-arch",
                    "self",
                    "inside-link",
                ):
                    assert leaked not in non_skip_out, (
                        f"{name} {flags} leaked {leaked!r} in:\n{out}"
                    )

                skip_lines = [
                    line
                    for line in out.splitlines()
                    if line.startswith("board: skipped (symbolic link, not read): ")
                ]
                mode_expected: list[str] = []
                for s in expected_skips:
                    if s == "dev/plans/archive" and (
                        "--archive" not in flags or "--maintainer" in flags
                    ):
                        continue
                    if s == "dev/PLANNING.md" and "--maintainer" not in flags:
                        continue
                    mode_expected.append(
                        f"board: skipped (symbolic link, not read): {s}"
                    )
                assert skip_lines == mode_expected, (
                    f"{name} {flags}: got {skip_lines}, expected {mode_expected}"
                )
                if "--maintainer" in flags and planning_skipped:
                    assert "dev/PLANNING.md is missing" not in out, (
                        f"{name} {flags} called skipped roadmap missing:\n{out}"
                    )

        # Control-byte encoding in a skipped symlink path:
        esc = "\x1b"
        esc_root = tmp_path / "esc_link"
        _write(esc_root, "dev/PLANNING.md", "# Board\n")
        (esc_root / "dev" / "plans").mkdir(parents=True)
        try:
            (esc_root / "dev" / "plans" / f"evil{esc}.md").symlink_to(
                tmp_path / "outside" / "secret-plan.md"
            )
        except OSError:
            pass
        else:
            assert board.main(["--root", str(esc_root)]) == 0
            out = capsys.readouterr().out
            assert esc not in out
            assert (
                "board: skipped (symbolic link, not read): dev/plans/evil\\x1b.md"
                in out.splitlines()
            )

    def test_symlinked_root_or_parent_above_root_is_read_normally(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A repository reached through a symlinked parent folder, or `--root`
        given as a symlink itself, is read normally with no skip line; and the
        module docstring states the symlink rule."""
        assert board.__doc__ is not None
        assert "symbolic link is never read and is named in the output" in " ".join(
            board.__doc__.split()
        )

        real_repo = tmp_path / "real_volume" / "project"
        _write(
            real_repo,
            "dev/proposals/2026-01-01-open.md",
            "# Open\n\n**Status**: awaiting-decision\n\n## Body\n",
        )
        _write(
            real_repo,
            "dev/plans/active.md",
            "# Active\n\n**Status**: implementing\n\n## Body\n",
        )
        _write(
            real_repo,
            "dev/PLANNING.md",
            "# Board\n\n* **Waiting on Maintainer**: real wait\n",
        )

        linked_volume = tmp_path / "linked_volume"
        linked_volume.symlink_to(tmp_path / "real_volume")
        via_parent = linked_volume / "project"

        root_link = tmp_path / "root_link"
        root_link.symlink_to(real_repo)

        for target in (via_parent, root_link):
            assert board.main(["--root", str(target)]) == 0
            out = capsys.readouterr().out
            assert "skipped (symbolic link, not read)" not in out
            assert "2026-01-01-open" in out
            assert "active" in out

            assert board.main(["--maintainer", "--root", str(target)]) == 0
            maint_out = capsys.readouterr().out
            assert "skipped (symbolic link, not read)" not in maint_out
            assert "2026-01-01-open" in maint_out
            assert "real wait" in maint_out

    def test_non_regular_entries_fail_loudly_without_hanging(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A directory named `x.md`, `dev/plans` as a regular file, or a named pipe
        `x.md` causes the board to print one encoded error line on stderr and exit 1
        without a traceback or hang."""
        # 1. Directory named x.md in dev/plans
        dir_md = tmp_path / "dir_md"
        (dir_md / "dev" / "plans" / "x.md").mkdir(parents=True)
        for flags in ((), ("--maintainer",)):
            rc = board.main([*flags, "--root", str(dir_md)])
            captured = capsys.readouterr()
            assert rc == 1
            assert captured.out == ""
            err_lines = captured.err.splitlines()
            assert len(err_lines) == 1
            assert "dev/plans/x.md" in err_lines[0]
            assert "Traceback" not in captured.err

        # 2. dev/plans as a regular file
        file_plans = tmp_path / "file_plans"
        _write(file_plans, "dev/plans", "not a directory\n")
        for flags in ((), ("--maintainer",)):
            rc = board.main([*flags, "--root", str(file_plans)])
            captured = capsys.readouterr()
            assert rc == 1
            assert captured.out == ""
            err_lines = captured.err.splitlines()
            assert len(err_lines) == 1
            assert "dev/plans" in err_lines[0]

        # 3. Named pipe x.md in dev/plans (under a subprocess timeout)
        if not hasattr(os, "mkfifo"):
            pytest.skip("os.mkfifo is not available on this platform")
        fifo_root = tmp_path / "fifo_root"
        (fifo_root / "dev" / "plans").mkdir(parents=True)
        os.mkfifo(fifo_root / "dev" / "plans" / "x.md")
        for flags in ((), ("--maintainer",)):
            proc = subprocess.run(
                [
                    sys.executable,
                    str(CAIRN_ROOT / "tools" / "board.py"),
                    *flags,
                    "--root",
                    str(fifo_root),
                ],
                capture_output=True,
                text=True,
                timeout=3,
                check=False,
            )
            assert proc.returncode == 1
            assert proc.stdout == ""
            err_lines = proc.stderr.splitlines()
            assert len(err_lines) == 1
            assert "dev/plans/x.md" in err_lines[0]


class TestBoardLoadsOnlyItsOwnEncoder:
    """The terminal board loads `encode_display` from its own `tools/session.py`,
    never from the tree named by `--root`."""

    def test_planted_session_module_under_root_is_never_executed(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Running the terminal modes against a `--root` tree containing a planted
        `tools/session.py` never executes the planted file."""
        marker = tmp_path / "planted_marker"
        target_root = tmp_path / "stranger_tree"
        planted = _write(
            target_root,
            "tools/session.py",
            f"from pathlib import Path\n"
            f"Path({str(marker)!r}).write_text('ran', encoding='utf-8')\n"
            f"def encode_display(text, *, limit=None):\n"
            f"    return str(text)\n",
        )
        # Control: loading the planted module directly writes the marker.
        ctrl_spec = importlib.util.spec_from_file_location("_planted_ctrl", planted)
        ctrl_mod = importlib.util.module_from_spec(ctrl_spec)
        ctrl_spec.loader.exec_module(ctrl_mod)
        assert marker.is_file()
        marker.unlink()

        _write(
            target_root,
            "dev/plans/real.md",
            "# Real\n\n**Status**: implementing\n\n## Body\n",
        )
        _write(target_root, "dev/PLANNING.md", "# Board\n")
        (target_root / "dev" / "plans" / "linked.md").symlink_to(planted)

        for flags in (
            (),
            ("--archive",),
            ("--maintainer",),
            ("--maintainer", "--archive"),
        ):
            rc = board.main([*flags, "--root", str(target_root)])
            captured = capsys.readouterr()
            assert rc == 0
            assert not marker.exists()
            assert (
                "board: skipped (symbolic link, not read): dev/plans/linked.md"
                in captured.out.splitlines()
            )
