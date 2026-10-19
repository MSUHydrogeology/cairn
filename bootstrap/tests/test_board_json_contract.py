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


import json

BASELINE_PATH = (
    CAIRN_ROOT / "bootstrap" / "tests" / "fixtures" / "board_json_v1_baseline.json"
)


def _json_type_name(val: object) -> str:
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "boolean"
    if isinstance(val, int):
        return "integer"
    if isinstance(val, str):
        return "string"
    if isinstance(val, list):
        return "array"
    if isinstance(val, dict):
        return "object"
    return type(val).__name__


def _matches_type(val: object, spec: str | list[str]) -> bool:
    actual = _json_type_name(val)
    if isinstance(spec, list):
        return actual in spec
    return actual == spec


def _run_json(root: Path, capsys: pytest.CaptureFixture[str], *extra: str) -> dict:
    rc = board.main(["--json", *extra, "--root", str(root)])
    captured = capsys.readouterr()
    assert rc == 0, f"rc={rc}, err={captured.err}"
    assert captured.err == ""
    return json.loads(captured.out)


class TestSchemaOneBaselineHolds:
    """The emitted JSON document matches the committed `cairn-board/1` baseline
    keys and types on both populated and minimal trees, with no derived or fence
    keys."""

    def test_schema_one_baseline_keys_and_types_hold(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Every baseline top-level, artifact-record and roadmap-wait key is
        present with its committed JSON type on both a full tree and an
        absent-fields tree; booleans are distinguished from integers; and no
        derived or fence key is emitted."""
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        assert baseline["schema"] == "cairn-board/1"

        full_tree = tmp_path / "full"
        _write(
            full_tree,
            "dev/proposals/2026-01-01-prop.md",
            "# Proposal title\n\n"
            "**Status**: awaiting-review\n"
            "**Review**: usual\n"
            "**Plan review**: required(Internal)\n"
            "**Opened**: 2026-01-01\n"
            "**Source proposal**: none\n"
            "**In brief**: Summary sentence.\n"
            "**Waiting on Maintainer**: decide\n\n"
            "## Body\n",
        )
        _write(
            full_tree,
            "dev/plans/archive/old-plan.md",
            "# Old plan\n\n"
            "**Status**: archived\n"
            "**Review**: usual\n"
            "**Plan review**: required(Internal)\n"
            "**Opened**: 2026-01-01\n"
            "**Source proposal**: `dev/proposals/archive/p.md`\n"
            "**In brief**: Done.\n"
            "**Waiting on Maintainer**: none\n\n"
            "## Body\n",
        )
        _write(
            full_tree,
            "dev/PLANNING.md",
            "# Board\n\n* **Waiting on Maintainer**: roadmap item\n",
        )
        outside = _write(tmp_path / "ext", "x.md", "# Ext\n")
        (full_tree / "dev" / "plans" / "skip.md").symlink_to(outside)

        full_doc = _run_json(full_tree, capsys, "--archive")
        assert full_doc["schema"] == "cairn-board/1"
        for key, spec in baseline["top_level"].items():
            assert key in full_doc, f"missing top-level key {key!r}"
            assert _matches_type(full_doc[key], spec), (
                f"top-level {key!r}: got {_json_type_name(full_doc[key])}, expected {spec}"
            )
        assert len(full_doc["artifacts"]) == 2
        for rec in full_doc["artifacts"]:
            for key, spec in baseline["artifact_record"].items():
                assert key in rec, f"missing record key {key!r}"
                assert _matches_type(rec[key], spec), (
                    f"record {key!r}: got {_json_type_name(rec[key])}, expected {spec}"
                )
                if isinstance(spec, list):
                    assert _json_type_name(rec[key]) == "string"
        assert len(full_doc["roadmap_waits"]) == 1
        for rw in full_doc["roadmap_waits"]:
            for key, spec in baseline["roadmap_wait"].items():
                assert key in rw, f"missing roadmap_wait key {key!r}"
                assert _matches_type(rw[key], spec), (
                    f"roadmap_wait {key!r}: got {_json_type_name(rw[key])}, expected {spec}"
                )

        # Absent-fields tree: no title line and no header lines.
        empty_tree = tmp_path / "empty_fields"
        _write(empty_tree, "dev/plans/bare.md", "Plain text only.\n\n## Section\n")
        empty_doc = _run_json(empty_tree, capsys)
        for key, spec in baseline["top_level"].items():
            assert key in empty_doc
            assert _matches_type(empty_doc[key], spec)
        assert len(empty_doc["artifacts"]) == 1
        bare_rec = empty_doc["artifacts"][0]
        for key, spec in baseline["artifact_record"].items():
            assert key in bare_rec
            assert _matches_type(bare_rec[key], spec)
            if isinstance(spec, list):
                assert bare_rec[key] is None

        # No derived or fence keys at any level:
        all_keys = set(full_doc.keys())
        for rec in full_doc["artifacts"]:
            all_keys.update(rec.keys())
        for rw in full_doc["roadmap_waits"]:
            all_keys.update(rw.keys())
        for forbidden in ("fence", "holder", "maintainer_waits"):
            assert not any(forbidden in k for k in all_keys), all_keys

        if (CAIRN_ROOT / "docs" / "build-a-board-view.md").is_file():
            gtext = (CAIRN_ROOT / "docs" / "build-a-board-view.md").read_text(
                encoding="utf-8"
            )
            g_top = {
                k.strip("`")
                for k, _ in _parse_markdown_table(
                    _guide_section(gtext, "### Top-level keys")
                )
            }
            g_art = {
                k.strip("`")
                for k, _ in _parse_markdown_table(
                    _guide_section(gtext, "### Artifact records")
                )
            }
            g_rw = {
                k.strip("`")
                for k, _ in _parse_markdown_table(
                    _guide_section(gtext, "### Roadmap waits")
                )
            }
            assert set(full_doc.keys()) - set(baseline["top_level"].keys()) <= g_top
            for rec in full_doc["artifacts"]:
                assert (
                    set(rec.keys()) - set(baseline["artifact_record"].keys()) <= g_art
                )
            for rw in full_doc["roadmap_waits"]:
                assert set(rw.keys()) - set(baseline["roadmap_wait"].keys()) <= g_rw


class TestRecordFactsComeFromWhereTheFileSits:
    """Location-derived keys (`kind`, `id`, `path`, `archived`), `title`, and
    top-level metadata cannot be forged from header lines inside an artifact."""

    def test_header_lines_cannot_forge_location_or_schema_fields(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Header lines named after location keys, schema keys or uncontracted
        fields never overwrite `kind`, `id`, `path`, `archived`, `title`,
        `schema` or `includes_archive`, and repeated fields use last-wins."""
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        _write(
            tmp_path,
            "dev/plans/real-plan.md",
            "# Authentic Title\n\n"
            "**Kind**: proposal\n"
            "**Id**: forged\n"
            "**Path**: javascript:alert(1)\n"
            "**Archived**: yes\n"
            "**Schema**: cairn-board/2\n"
            "**Title**: forged-title\n"
            "**Includes archive**: true\n"
            "**Assurance path**: high-assurance\n"
            "**Status**: first-status\n"
            "**Status**: awaiting-decision\n\n"
            "## Body\n",
        )
        doc = _run_json(tmp_path, capsys)
        assert doc["schema"] == "cairn-board/1"
        assert doc["includes_archive"] is False
        assert len(doc["artifacts"]) == 1
        rec = doc["artifacts"][0]
        assert set(rec.keys()) == set(baseline["artifact_record"].keys())
        assert rec["kind"] == "plan"
        assert rec["id"] == "real-plan"
        assert rec["path"] == "dev/plans/real-plan.md"
        assert rec["archived"] is False
        assert rec["title"] == "Authentic Title"
        assert rec["status"] == "awaiting-decision"

    def test_all_record_values_and_absent_vs_blank_and_headerless_files(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Each field comes from above the first `## ` heading, unescaped; absent
        is `None` while a present blank line is `""`; `title` and `in_brief`
        never stand in for each other; and a header-less artifact is included in
        `--json` while omitted from the plain board."""
        _write(
            tmp_path,
            "dev/proposals/2026-01-01-complete.md",
            "# First Title | Raw\n"
            "# Second Title Ignored\n\n"
            "**Status**: awaiting-review\n"
            "**Review**: usual + Security Review\n"
            "**Plan review**: required(Internal)\n"
            "**Opened**: 2026-01-01\n"
            "**Source proposal**: `dev/proposals/archive/p.md`\n"
            "**In brief**: Plain summary | unescaped.\n"
            "**Waiting on Maintainer**: check A | B\n\n"
            "## First heading\n"
            "# Heading below section\n"
            "**Status**: below-heading-ignored\n"
            "**Opened**: 1999-01-01\n",
        )
        _write(
            tmp_path,
            "dev/plans/blanks.md",
            "**Status**: implementing\n"
            "**In brief**:\n"
            "**Waiting on Maintainer**:   \n\n"
            "## Section\n"
            "# Late title\n"
            "**Review**: below-heading\n",
        )
        _write(
            tmp_path,
            "dev/plans/headerless.md",
            "# Only A Title\n\nNo bold header lines here.\n\n## Section\n",
        )

        doc = _run_json(tmp_path, capsys)
        by_id = {r["id"]: r for r in doc["artifacts"]}
        assert set(by_id.keys()) == {"2026-01-01-complete", "blanks", "headerless"}

        comp = by_id["2026-01-01-complete"]
        assert comp == {
            "archived": False,
            "id": "2026-01-01-complete",
            "in_brief": "Plain summary | unescaped.",
            "kind": "proposal",
            "opened": "2026-01-01",
            "path": "dev/proposals/2026-01-01-complete.md",
            "plan_review": "required(Internal)",
            "review": "usual + Security Review",
            "source_proposal": "`dev/proposals/archive/p.md`",
            "status": "awaiting-review",
            "title": "First Title | Raw",
            "waiting_on_maintainer": "check A | B",
        }

        blanks = by_id["blanks"]
        assert blanks["title"] is None
        assert blanks["in_brief"] == ""
        assert blanks["waiting_on_maintainer"] == ""
        assert blanks["review"] is None
        assert blanks["opened"] is None

        hdrless = by_id["headerless"]
        assert hdrless["title"] == "Only A Title"
        for k in (
            "in_brief",
            "status",
            "review",
            "plan_review",
            "opened",
            "source_proposal",
            "waiting_on_maintainer",
        ):
            assert hdrless[k] is None

        # Plain board still omits headerless.md:
        assert board.main(["--root", str(tmp_path)]) == 0
        plain_out = capsys.readouterr().out
        assert "headerless" not in plain_out


class TestOutputIsDeterministic:
    """The JSON output is deterministic, pure ASCII with sorted keys, and keys
    records uniquely by `path` across live and archived files."""

    def test_archives_unique_path_key_and_deterministic_ascii_json(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Live and archived files sharing a stem both appear under `--archive`
        with distinct `path`; two runs on identical content in different roots
        produce identical ASCII bytes with sorted keys; and an empty root still
        emits `schema: cairn-board/1`."""
        root_a = tmp_path / "root_a"
        root_b = tmp_path / "root_b"
        for r in (root_a, root_b):
            _write(
                r,
                "dev/plans/shared-name.md",
                "# Live Café \u2014 Δ\n\n**Status**: implementing\n\n## Body\n",
            )
            _write(
                r,
                "dev/plans/archive/shared-name.md",
                "# Archived Plan\n\n**Status**: archived\n\n## Body\n",
            )
            _write(r, "dev/PLANNING.md", "# Board\n")

        doc_live = _run_json(root_a, capsys)
        assert doc_live["includes_archive"] is False
        assert [a["path"] for a in doc_live["artifacts"]] == [
            "dev/plans/shared-name.md"
        ]
        assert all(a["archived"] is False for a in doc_live["artifacts"])

        assert board.main(["--json", "--archive", "--root", str(root_a)]) == 0
        out_a1 = capsys.readouterr().out
        assert board.main(["--json", "--archive", "--root", str(root_a)]) == 0
        out_a2 = capsys.readouterr().out
        assert board.main(["--json", "--archive", "--root", str(root_b)]) == 0
        out_b = capsys.readouterr().out

        assert out_a1 == out_a2 == out_b
        assert out_a1.isascii()

        parsed = json.loads(out_a1)
        reserialized = (
            json.dumps(parsed, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
        )
        assert out_a1 == reserialized
        assert parsed["includes_archive"] is True
        paths = [a["path"] for a in parsed["artifacts"]]
        assert paths == [
            "dev/plans/archive/shared-name.md",
            "dev/plans/shared-name.md",
        ]
        assert parsed["artifacts"][1]["title"] == "Live Café \u2014 Δ"

        # Empty tree with no dev/ directory:
        no_dev = tmp_path / "no_dev"
        no_dev.mkdir()
        empty_doc = _run_json(no_dev, capsys)
        assert empty_doc == {
            "artifacts": [],
            "includes_archive": False,
            "roadmap_read": False,
            "roadmap_waits": [],
            "schema": "cairn-board/1",
            "skipped_symlinks": [],
        }


class TestRoadmapWaitsAndSkippedSymlinksInJson:
    """`roadmap_waits`, `roadmap_read` and `skipped_symlinks` in `--json` share
    one reader with `--maintainer`, and failures write nothing to stdout."""

    def test_roadmap_waits_match_maintainer_and_share_one_reader(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """`roadmap_waits` on the golden tree matches `--maintainer`'s roadmap
        entries in line numbers and text; blank wait rows produce `""`; missing
        and linked roadmap files set `roadmap_read: False`; and `skipped_symlinks`
        matches the terminal skip lines on all ten symlink trees."""
        main_tree = tmp_path / "main"
        _build_golden_main_tree(main_tree)
        _write(
            main_tree,
            "dev/PLANNING.md",
            (main_tree / "dev" / "PLANNING.md").read_text(encoding="utf-8")
            + "* **Waiting on Maintainer**:\n",
        )
        doc = _run_json(main_tree, capsys)
        assert doc["roadmap_read"] is True

        assert board.main(["--maintainer", "--root", str(main_tree)]) == 0
        maint_lines = capsys.readouterr().out.splitlines()
        maint_roadmap = []
        for line in maint_lines[1:]:
            cells = line.removeprefix("board: ").split(" | ", 3)
            if len(cells) == 4 and cells[0] == "roadmap":
                _, art, _, txt = cells
                line_no = int(art.split(":", 1)[1])
                maint_roadmap.append({"line": line_no, "text": txt})
        assert doc["roadmap_waits"] == maint_roadmap
        assert doc["roadmap_waits"][-1]["text"] == ""

        # Present dev/PLANNING.md with no wait rows:
        quiet_tree = tmp_path / "quiet"
        _write(quiet_tree, "dev/PLANNING.md", "# Planning\n\nNo waits here.\n")
        quiet_doc = _run_json(quiet_tree, capsys)
        assert quiet_doc["roadmap_read"] is True
        assert quiet_doc["roadmap_waits"] == []

        # Ten symlink trees:
        for name, root, expected_skips, planning_skipped in _build_ten_symlink_trees(
            tmp_path / "links"
        ):
            extra = ("--archive",) if name == "archive_linked" else ()
            link_doc = _run_json(root, capsys, *extra)
            assert link_doc["skipped_symlinks"] == sorted(expected_skips), name
            if planning_skipped:
                assert link_doc["roadmap_read"] is False, name
            else:
                assert link_doc["roadmap_read"] is True, name

    def test_json_failures_and_usage_errors_write_nothing_to_stdout(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Non-UTF-8 files, directories named `x.md`, and named pipes exit 1 in
        `--json` with empty stdout and one `ascii()`-encoded stderr line without
        loading `tools/session.py`; `--json --maintainer` exits 2 with empty
        stdout; and `--help` cites `cairn/docs/build-a-board-view.md`."""
        board_src = (CAIRN_ROOT / "tools" / "board.py").read_text(encoding="utf-8")
        assert (
            "ascii() is used instead of the terminal encoder so that --json loads no other file"
            in board_src
        )

        # 1. Non-UTF-8 artifact:
        bad_art = tmp_path / "bad_art"
        (bad_art / "dev" / "plans").mkdir(parents=True)
        (bad_art / "dev" / "plans" / "broken.md").write_bytes(b"\xff\xfeinvalid")
        rc = board.main(["--json", "--root", str(bad_art)])
        captured = capsys.readouterr()
        assert rc == 1
        assert captured.out == ""
        assert len(captured.err.splitlines()) == 1
        assert "'dev/plans/broken.md'" in captured.err

        # 2. Non-UTF-8 dev/PLANNING.md:
        bad_plan = tmp_path / "bad_plan"
        (bad_plan / "dev").mkdir(parents=True)
        (bad_plan / "dev" / "PLANNING.md").write_bytes(b"\xff\xfeinvalid")
        rc = board.main(["--json", "--root", str(bad_plan)])
        captured = capsys.readouterr()
        assert rc == 1
        assert captured.out == ""
        assert len(captured.err.splitlines()) == 1
        assert "'dev/PLANNING.md'" in captured.err

        # 3. Directory named x.md (even after a valid artifact):
        dir_md = tmp_path / "dir_md"
        _write(dir_md, "dev/plans/a_first.md", "# A\n\n**Status**: implementing\n")
        (dir_md / "dev" / "plans" / "x.md").mkdir(parents=True)
        rc = board.main(["--json", "--root", str(dir_md)])
        captured = capsys.readouterr()
        assert rc == 1
        assert captured.out == ""
        assert len(captured.err.splitlines()) == 1
        assert "'dev/plans/x.md'" in captured.err

        # 4. Named pipe x.md:
        if hasattr(os, "mkfifo"):
            fifo_root = tmp_path / "fifo_json"
            (fifo_root / "dev" / "plans").mkdir(parents=True)
            os.mkfifo(fifo_root / "dev" / "plans" / "x.md")
            proc = subprocess.run(
                [
                    sys.executable,
                    str(CAIRN_ROOT / "tools" / "board.py"),
                    "--json",
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
            assert len(proc.stderr.splitlines()) == 1
            assert "'dev/plans/x.md'" in proc.stderr

        # 5. --json --maintainer exits 2 with empty stdout:
        with pytest.raises(SystemExit) as excinfo:
            board.main(["--json", "--maintainer", "--root", str(tmp_path)])
        assert excinfo.value.code == 2
        captured = capsys.readouterr()
        assert captured.out == ""

        # 6. --help text:
        with pytest.raises(SystemExit) as help_exc:
            board.main(["--help"])
        assert help_exc.value.code == 0
        help_out = capsys.readouterr().out
        assert "header blocks and nothing else" not in help_out
        assert "header blocks only" not in help_out
        normalized_help = " ".join(help_out.split())
        assert (
            "JSON form: --json prints the board as data (schema cairn-board/1). "
            "Field reference and worked example: Cairn's own cairn/docs/build-a-board-view.md "
            "(in the repository you adopted from, not in this tree)."
        ) in normalized_help


import re

GUIDE_PATH = CAIRN_ROOT / "docs" / "build-a-board-view.md"
LIFECYCLE_PATH = CAIRN_ROOT / "doctrine" / "lifecycle.md"


def _guide_section(text: str, heading: str) -> str:
    """Return the content of `heading` (`## ...` or `### ...`) up to the next
    heading of the same or higher level."""
    level = len(heading) - len(heading.lstrip("#"))
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.strip() == heading:
            start = idx + 1
            break
    assert start is not None, f"heading {heading!r} not found"
    out: list[str] = []
    for line in lines[start:]:
        if line.startswith("#"):
            hashes = len(line) - len(line.lstrip("#"))
            if hashes <= level and line[hashes:hashes + 1] == " ":
                break
        out.append(line)
    return "\n".join(out)


def _parse_markdown_table(section_text: str) -> list[tuple[str, str]]:
    """Return `(col1, col2)` from a Markdown table in `section_text`."""
    rows: list[tuple[str, str]] = []
    for line in section_text.splitlines():
        s = line.strip()
        if not s.startswith("|") or not s.endswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if all(set(c) <= {"-", ":"} and c for c in cells):
            continue
        rows.append((cells[0], cells[1]))
    assert len(rows) >= 2, f"no table rows found in:\n{section_text}"
    return rows[1:]


def _normalize_guide_type(type_cell: str) -> str | list[str]:
    cleaned = type_cell.strip("`").strip()
    if " or " in cleaned:
        return [part.strip() for part in cleaned.split(" or ")]
    return cleaned


class TestGuideAndOutputAgree:
    """`docs/build-a-board-view.md` opens in plain prose, its three field tables
    match the emitted JSON keys and baseline types in both directions, and its
    promise and trust sections carry the required standing phrases."""

    def test_guide_opening_section_is_plain_prose_and_defines_terms(self) -> None:
        """The first `## ` section after the title contains no table and no
        fenced code block, states that Cairn ships no view and pages are
        regenerated rather than hand-kept, and defines both `view` and `JSON`
        in the first sentence where each appears."""
        text = GUIDE_PATH.read_text(encoding="utf-8")
        lines = text.splitlines()
        first_h2 = next(i for i, l in enumerate(lines) if l.startswith("## "))
        heading = lines[first_h2].strip()
        sec = _guide_section(text, heading)
        assert "```" not in sec
        assert not any(l.strip().startswith("|") for l in sec.splitlines())
        collapsed = " ".join(sec.split())
        assert "regenerated" in collapsed and "never hand-kept" in collapsed
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", collapsed) if s.strip()]
        view_sent = next(s for s in sentences if "view" in s.lower())
        json_sent = next(s for s in sentences if "json" in s.lower())
        assert "web page" in view_sent.lower() or "table" in view_sent.lower()
        assert "plain-text" in json_sent.lower() or "data format" in json_sent.lower()

    def test_guide_field_tables_and_standing_phrases_match_output_and_baseline(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """The key sets and types under `### Top-level keys`, `### Artifact records`
        and `### Roadmap waits` equal the emitted key sets and the baseline
        fixture's types, and the standing phrases in `## What will not change`
        and `## What the data can and cannot show` are present."""
        text = GUIDE_PATH.read_text(encoding="utf-8")
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))

        for heading, base_section in (
            ("### Top-level keys", "top_level"),
            ("### Artifact records", "artifact_record"),
            ("### Roadmap waits", "roadmap_wait"),
        ):
            rows = _parse_markdown_table(_guide_section(text, heading))
            table_map = {
                col1.strip("`"): _normalize_guide_type(col2) for col1, col2 in rows
            }
            assert table_map == baseline[base_section], (
                f"{heading} mismatch: guide={table_map}, baseline={baseline[base_section]}"
            )

        # Compare against live emitted keys on a populated tree:
        _write(
            tmp_path,
            "dev/plans/p.md",
            "# Plan\n\n**Status**: implementing\n\n## Body\n",
        )
        _write(
            tmp_path,
            "dev/PLANNING.md",
            "# Board\n\n* **Waiting on Maintainer**: row\n",
        )
        doc = _run_json(tmp_path, capsys)
        top_rows = _parse_markdown_table(_guide_section(text, "### Top-level keys"))
        art_rows = _parse_markdown_table(_guide_section(text, "### Artifact records"))
        rw_rows = _parse_markdown_table(_guide_section(text, "### Roadmap waits"))
        assert set(doc.keys()) == {k.strip("`") for k, _ in top_rows}
        assert set(doc["artifacts"][0].keys()) == {k.strip("`") for k, _ in art_rows}
        assert set(doc["roadmap_waits"][0].keys()) == {k.strip("`") for k, _ in rw_rows}

        # Standing phrases in ## What will not change:
        promise_sec = " ".join(_guide_section(text, "## What will not change").split())
        for phrase in (
            "ignore keys",
            "cairn-board/2",
            "CHANGELOG.md",
            "live records only",
            "must not overwrite",
            "length",
        ):
            assert phrase in promise_sec, f"missing promise phrase {phrase!r}"

        # Standing phrases in ## What the data can and cannot show:
        cannot_sec = " ".join(
            _guide_section(text, "## What the data can and cannot show").split()
        )
        for phrase in (
            "never an approval record",
            "not that a Decision",
            "skipped_symlinks",
        ):
            assert phrase in cannot_sec, f"missing safety phrase {phrase!r}"


def _lifecycle_diagram_holders() -> tuple[dict[str, str], list[str]]:
    """Parse `doctrine/lifecycle.md` node labels per D11."""
    text = LIFECYCLE_PATH.read_text(encoding="utf-8")
    raw_labels = re.findall(r'\["([^"]+)"\]', text)
    mapping: dict[str, str] = {}
    for lbl in raw_labels:
        if "<br/>" in lbl:
            word, rest = lbl.split("<br/>", 1)
        else:
            word, rest = lbl, ""
        word = word.strip()
        holder = "none named"
        for role in ("Maintainer", "author", "reviewer", "implementer"):
            if role.lower() in rest.lower():
                holder = role
                break
        mapping[word] = holder
    return mapping, raw_labels


class TestGuideLookupMatchesLifecycle:
    """The lookup table in `docs/build-a-board-view.md` agrees with the two
    lifecycle diagrams in `doctrine/lifecycle.md`."""

    def test_guide_lookup_table_matches_lifecycle_diagrams(self) -> None:
        """Every status word in `doctrine/lifecycle.md`'s diagrams appears in
        `### The lookup` with the holder its label gives; the catch-all row names
        the retired words `proposed`, `reviewed` and `revised` and maps to
        `none named`; and no extra status word is listed."""
        diagram_map, raw_labels = _lifecycle_diagram_holders()
        assert len(diagram_map) >= 14, f"unexpectedly few labels: {raw_labels}"

        guide_text = GUIDE_PATH.read_text(encoding="utf-8")
        rows = _parse_markdown_table(_guide_section(guide_text, "### The lookup"))
        last_col1, last_col2 = rows[-1]
        assert (
            last_col1
            == "anything else, including the retired words `proposed`, `reviewed` and `revised`"
        ), f"unexpected catch-all row: {last_col1!r} (labels: {raw_labels})"
        assert last_col2.strip("`") == "none named"

        guide_map = {
            col1.strip("`"): col2.strip("`") for col1, col2 in rows[:-1]
        }
        assert guide_map == diagram_map, (
            f"guide lookup {guide_map} != lifecycle diagrams {diagram_map} "
            f"(read labels: {raw_labels})"
        )

        # First-word matching and unknown/retired fallback:
        def lookup_status(raw_status: str) -> str:
            m = re.match(r"^[a-z-]+", raw_status)
            first = m.group(0) if m else ""
            return guide_map.get(first, last_col2.strip("`"))

        assert lookup_status("archived -- C1-C9 all landed") == "none named"
        for retired in ("proposed", "reviewed", "revised", "unknown-state"):
            assert lookup_status(retired) == "none named"

    def test_view_example_lookup_matches_guide_table_and_lifecycle(self) -> None:
        """`HOLDER_BY_STATUS` inside the `view-example` block equals both the
        guide's lookup table and `doctrine/lifecycle.md`'s diagram labels."""
        diagram_map, raw_labels = _lifecycle_diagram_holders()
        guide_text = GUIDE_PATH.read_text(encoding="utf-8")
        rows = _parse_markdown_table(_guide_section(guide_text, "### The lookup"))
        guide_map = {col1.strip("`"): col2.strip("`") for col1, col2 in rows[:-1]}
        ns = _load_tagged_module("view-example")
        assert ns["HOLDER_BY_STATUS"] == guide_map == diagram_map, (
            f"example={ns['HOLDER_BY_STATUS']}, guide={guide_map}, "
            f"lifecycle={diagram_map} (labels: {raw_labels})"
        )


class TestFenceStaysInTheTerminalView:
    """The fence warning stays in `board.py --maintainer` only; the guide only
    points to the terminal view and no code block computes a fence check."""

    def test_fence_mentions_only_point_to_terminal_view_and_no_code_block_computes_one(
        self,
    ) -> None:
        text = GUIDE_PATH.read_text(encoding="utf-8")
        fenced_blocks = re.findall(r"```[^\n]*\n(.*?)```", text, flags=re.DOTALL)
        for block in fenced_blocks:
            for forbidden in ("MAINTAINER-GATED", "MAINTAINER-ONLY", "fences_without_wait"):
                assert forbidden not in block, (
                    f"fenced code block must not compute {forbidden!r}"
                )
            for line in block.splitlines():
                if "fence" in line.lower():
                    assert "--maintainer" in line, (
                        f"code line mentioning fence must only point to --maintainer: {line!r}"
                    )
        paragraphs = [p.strip() for p in text.split("\n\n") if "fence" in p.lower()]
        assert len(paragraphs) >= 1
        for p in paragraphs:
            assert "--maintainer" in p, (
                f"fence mention must point to --maintainer: {p!r}"
            )


class TestHelpCitesTheGuide:
    """`board.py --help` cites `cairn/docs/build-a-board-view.md` and the cited
    path resolves in Cairn's tree."""

    def test_help_cites_cairn_guide_path_and_token_resolves(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        with pytest.raises(SystemExit) as excinfo:
            board.main(["--help"])
        assert excinfo.value.code == 0
        help_out = capsys.readouterr().out
        assert "cairn/docs/build-a-board-view.md" in help_out
        assert "not in this tree" in help_out
        rel = "cairn/docs/build-a-board-view.md".removeprefix("cairn/")
        assert (CAIRN_ROOT / rel).is_file()


class TestGuideIsNotInstalled:
    """`docs/build-a-board-view.md` is documentation in Cairn's own repository
    and is never copied into adopter installs."""

    def test_guide_is_absent_from_scaffold_manifest(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(CAIRN_ROOT / "bootstrap" / "scaffold.py"), "--manifest"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert "build-a-board-view" not in proc.stdout


import ast
import shutil


def _extract_tagged_block(tag: str) -> str:
    text = GUIDE_PATH.read_text(encoding="utf-8")
    pattern = re.compile(rf"^```python {re.escape(tag)}\n(.*?)^```", re.MULTILINE | re.DOTALL)
    matches = pattern.findall(text)
    assert len(matches) == 1, f"expected exactly 1 block tagged {tag!r}, found {len(matches)}"
    return matches[0]


def _load_tagged_module(tag: str) -> dict[str, object]:
    code = _extract_tagged_block(tag)
    compiled = compile(code, f"<guide:{tag}>", "exec")
    ns: dict[str, object] = {"__name__": f"_guide_{tag.replace('-', '_')}"}
    exec(compiled, ns)
    return ns


def _git_env(**extra: str) -> dict[str, str]:
    env = os.environ.copy()
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env.update(extra)
    return env


def _git_run(repo: Path, *args: str, **env_extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "git",
            "-c",
            "user.name=Test User",
            "-c",
            "user.email=test@example.com",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        cwd=repo,
        env=_git_env(**env_extra),
        capture_output=True,
        text=True,
        check=True,
    )


class TestWaitsRecipeAgreesWithMaintainerView:
    """The `waiting_on_maintainer` recipe in `docs/build-a-board-view.md` agrees
    with `board.py --maintainer` across every status, header, blank-wait,
    archive, roadmap and symlink shape."""

    def test_waits_recipe_matches_maintainer_view_across_all_shapes(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        ns = _load_tagged_module("view-example")
        waits_fn = ns["waiting_on_maintainer"]
        diagram_map, _ = _lifecycle_diagram_holders()

        trees: list[tuple[str, Path, tuple[str, ...]]] = []

        # 1. Every lifecycle status word bare and with notes, plus awaiting-decision variants:
        t1 = tmp_path / "t1_statuses"
        idx = 0
        for word in sorted(diagram_map):
            for suffix in ("", " -- note", ": note", ", note"):
                idx += 1
                _write(
                    t1,
                    f"dev/proposals/2026-01-{idx:02d}-s.md",
                    f"# S {idx}\n\n**Status**: {word}{suffix}\n\n## Body\n",
                )
        for slug, st in (
            ("hyphen", "awaiting-decision-x"),
            ("plural", "awaiting-decisions"),
            ("under", "awaiting-decision_x"),
            ("digit", "awaiting-decision2"),
        ):
            _write(
                t1,
                f"dev/proposals/2026-02-01-{slug}.md",
                f"# {slug}\n\n**Status**: {st}\n\n## Body\n",
            )
        _write(t1, "dev/PLANNING.md", "# Board\n")
        trees.append(("statuses", t1, ()))

        # 2. Waiting lines, files, blanked waits, repeated lines, archive, roadmap shapes:
        t2 = tmp_path / "t2_waits_and_files"
        _write(
            t2,
            "dev/plans/wait-blank.md",
            "# Blank\n\n**Status**: implementing\n**Waiting on Maintainer**:\n\n## Body\n",
        )
        _write(
            t2,
            "dev/plans/wait-spaced.md",
            "# Spaced\n\n**Status**: implementing\n**Waiting on Maintainer **: spaced\n\n## Body\n",
        )
        _write(
            t2,
            "dev/plans/wait-lower.md",
            "# Lower\n\n**Status**: implementing\n**waiting on maintainer**: lower\n\n## Body\n",
        )
        _write(
            t2,
            "dev/plans/wait-below.md",
            "# Below\n\n**Status**: implementing\n\n## Body\n**Waiting on Maintainer**: below\n",
        )
        _write(
            t2,
            "dev/plans/wait-repeated.md",
            "# Repeated\n\n**Status**: implementing\n"
            "**Waiting on Maintainer**: first\n"
            "**Waiting on Maintainer**: second\n\n## Body\n",
        )
        _write(
            t2,
            "dev/proposals/2026-01-01-status-repeated.md",
            "# Status repeated\n\n  **Status**: awaiting-review\n"
            "  **Status**: awaiting-decision\n\n## Body\n",
        )
        _write(
            t2,
            "dev/proposals/2026-01-02-both.md",
            "# Both\n\n**Status**: awaiting-decision\n"
            "**Waiting on Maintainer**: both text\n\n## Body\n",
        )
        _write(t2, "dev/plans/headerless.md", "# No headers\n\nBody.\n\n## Section\n")
        _write(t2, "dev/plans/no-status.md", "# No status\n\n**Opened**: 2026-01-01\n\n## Section\n")
        _write(
            t2,
            "dev/plans/_template.md",
            "# Template\n\n**Status**: implementing\n**Waiting on Maintainer**: skip\n\n## Body\n",
        )
        _write(
            t2,
            "dev/plans/_notes.md",
            "# Notes\n\n**Status**: implementing\n**Waiting on Maintainer**: skip\n\n## Body\n",
        )
        _write(
            t2,
            "dev/plans/archive/arch-wait.md",
            "# Archived\n\n**Status**: archived\n**Waiting on Maintainer**: done\n\n## Body\n",
        )
        _write(
            t2,
            "dev/PLANNING.md",
            "# Planning\n\n"
            "**Waiting on Maintainer**: plain\n"
            "  **Waiting on Maintainer**: indented\n"
            "  * **Waiting on Maintainer**: sub-bullet\n"
            "- **Waiting on Maintainer**: dash-bullet\n"
            "* **Waiting on Maintainer**:\n"
            "Prose mentioning **Waiting on Maintainer**: inline.\n",
        )
        trees.append(("waits_live", t2, ()))
        trees.append(("waits_archive", t2, ("--archive",)))

        # 3. Missing dev/PLANNING.md:
        t3 = tmp_path / "t3_no_planning"
        _write(
            t3,
            "dev/proposals/2026-01-01-decide.md",
            "# Decide\n\n**Status**: awaiting-decision\n\n## Body\n",
        )
        trees.append(("no_planning", t3, ()))

        # 4. C1's ten symlink trees:
        for name, lroot, _, _ in _build_ten_symlink_trees(tmp_path / "links"):
            extra = ("--archive",) if name == "archive_linked" else ()
            trees.append((f"link_{name}", lroot, extra))

        for label, root, extra in trees:
            doc = _run_json(root, capsys, *extra)
            recipe_entries, caveats = waits_fn(doc)

            assert board.main(["--maintainer", *extra, "--root", str(root)]) == 0
            maint_lines = capsys.readouterr().out.splitlines()
            maint_entries = []
            for line in maint_lines[1:]:
                cells = line.removeprefix("board: ").split(" | ", 3)
                if len(cells) == 4:
                    maint_entries.append(tuple(cells))

            assert [(k, a, r) for k, a, r, _ in recipe_entries] == [
                (k, a, r) for k, a, r, _ in maint_entries
            ], f"{label}: entry keys/reasons differed"

            for (rk, ra, rr, rt), (mk, ma, mr, mt) in zip(recipe_entries, maint_entries):
                if rt.isascii() and len(rt) < 47:
                    assert rt == mt, f"{label} ({rk}, {ra}): text {rt!r} != {mt!r}"

            maint_missing = any(
                "dev/PLANNING.md is missing" in l for l in maint_lines
            )
            maint_skips = [
                l.removeprefix("board: ")
                for l in maint_lines
                if l.startswith("board: skipped (symbolic link, not read): ")
            ]
            if maint_missing:
                assert "dev/PLANNING.md was not read" in caveats, label
            for sk in maint_skips:
                assert sk in caveats, f"{label}: missing skip caveat {sk!r} in {caveats}"


class TestViewExample:
    """The `view-example` block in `docs/build-a-board-view.md` is concise, uses
    only two safe subprocesses, escapes HTML and category-C characters, matches
    `--maintainer` on the Maintainer group, reports skipped links and missing
    roadmap files, and never overwrites an existing page on failure."""

    def test_view_example_structure_lookup_and_ast(self) -> None:
        code = _extract_tagged_block("view-example")
        line_count = len(code.strip().splitlines())
        assert 75 <= line_count <= 110, f"view-example line count {line_count} outside [75, 110]"

        ns = _load_tagged_module("view-example")
        diagram_map, _ = _lifecycle_diagram_holders()
        assert ns["HOLDER_BY_STATUS"] == diagram_map

        tree = ast.parse(code)
        subproc_calls: list[ast.Call] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if (
                    isinstance(func, ast.Attribute)
                    and isinstance(func.value, ast.Name)
                    and func.value.id == "subprocess"
                ):
                    subproc_calls.append(node)
        assert len(subproc_calls) == 2, f"expected 2 subprocess calls, got {len(subproc_calls)}"
        for call in subproc_calls:
            for kw in call.keywords:
                if kw.arg == "shell":
                    assert isinstance(kw.value, ast.Constant) and kw.value.value is False
            assert len(call.args) >= 1 and isinstance(call.args[0], ast.List)
            elts = call.args[0].elts
            for elt in elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    assert elt.value != "python", "must not look up bare 'python' on PATH"
        first_elts = subproc_calls[0].args[0].elts
        assert (
            isinstance(first_elts[0], ast.Attribute)
            and isinstance(first_elts[0].value, ast.Name)
            and first_elts[0].value.id == "sys"
            and first_elts[0].attr == "executable"
        )

    def test_view_example_renders_groups_escaping_footer_and_preserves_page_on_failure(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ns = _load_tagged_module("view-example")
        build_view = ns["build_view"]
        render_page = ns["render_page"]

        repo = tmp_path / "repo"
        (repo / "tools").mkdir(parents=True)
        shutil.copy2(CAIRN_ROOT / "tools" / "board.py", repo / "tools" / "board.py")
        shutil.copy2(CAIRN_ROOT / "tools" / "session.py", repo / "tools" / "session.py")
        _git_run(repo, "init")

        esc = "\x1b"
        rlo = "\u202e"
        hangul_filler = "\u3164"
        long_brief = "B" * 1000

        _write(
            repo,
            "dev/proposals/2026-01-01-decide-note.md",
            "# Decide with note\n\n"
            "**Status**: awaiting-decision \u2014 scope question\n"
            "**In brief**: Ready for decision.\n\n## Body\n",
        )
        _write(
            repo,
            "dev/proposals/2026-01-02-decide-digit.md",
            "# Digit suffix\n\n**Status**: awaiting-decision2\n\n## Body\n",
        )
        _write(
            repo,
            "dev/proposals/2026-01-03-revising.md",
            f"# Author <script>alert(\"x\")</script> 'quote' {esc} {rlo} {hangul_filler}\n\n"
            "**Status**: revising\n\n## Body\n",
        )
        _write(
            repo,
            "dev/plans/waiting-impl.md",
            "# Implementing with wait\n\n"
            "**Status**: implementing\n"
            "**Waiting on Maintainer**: confirm threshold\n"
            f"**In brief**: {long_brief}\n\n## Body\n",
        )
        _write(
            repo,
            "dev/plans/review-plan.md",
            "# In code review\n\n**Status**: awaiting-code-review\n\n## Body\n",
        )
        _write(
            repo,
            "dev/plans/active-impl.md",
            "# Active implementation\n\n**Status**: implementing\n\n## Body\n",
        )
        _write(repo, "dev/plans/headerless.md", "# Headerless plan\n\nBody.\n\n## Section\n")
        _write(
            repo,
            "dev/plans/no-status.md",
            "# No status line\n\n**Opened**: 2026-01-05\n\n## Section\n",
        )
        _write(
            repo,
            "dev/PLANNING.md",
            "# Planning\n\n* **Waiting on Maintainer**: run release ceremony\n",
        )
        _git_run(repo, "add", ".")
        _git_run(repo, "commit", "-m", "initial")
        head_sha = _git_run(repo, "rev-parse", "HEAD").stdout.strip()

        monkeypatch.chdir(repo)
        out_html = tmp_path / "board-view.html"
        build_view(out_html)
        html_text = out_html.read_text(encoding="utf-8")

        # Group order and counts:
        headings = re.findall(r"<h2>([^<]+)</h2>", html_text)
        assert headings == [
            "Maintainer (3)",
            "author (1)",
            "reviewer (1)",
            "implementer (1)",
            "none named (3)",
        ]

        # Maintainer section members match board.py --maintainer:
        maint_sec = re.search(
            r"<h2>Maintainer \(3\)</h2><ul>(.*?)</ul>", html_text, flags=re.DOTALL
        ).group(1)
        maint_codes = re.findall(r"<li><code>([^<]+)</code>", maint_sec)
        assert board.main(["--maintainer", "--root", str(repo)]) == 0
        maint_cli = [
            l.removeprefix("board: ").split(" | ", 3)[1]
            for l in capsys.readouterr().out.splitlines()[1:]
            if len(l.removeprefix("board: ").split(" | ", 3)) == 4
        ]
        assert maint_codes == maint_cli
        assert "waiting-impl" in maint_codes
        assert "dev/PLANNING.md:3" in maint_codes

        # Headerless and no-status files are in "none named" with "status unknown":
        none_sec = re.search(
            r"<h2>none named \(3\)</h2><ul>(.*?)</ul>", html_text, flags=re.DOTALL
        ).group(1)
        assert "<code>headerless</code> (status unknown)" in none_sec
        assert "<code>no-status</code> (status unknown)" in none_sec
        assert "<code>2026-01-02-decide-digit</code> (awaiting-decision2)" in none_sec

        # Escaping and category-C replacement:
        assert "<script>" not in html_text
        assert "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;" in html_text
        assert "&#x27;quote&#x27;" in html_text
        assert esc not in html_text and "U+001B" in html_text
        assert rlo not in html_text and "U+202E" in html_text
        assert hangul_filler in html_text
        assert ("B" * 125) not in html_text
        assert ("B" * 119 + "\u2026") in html_text

        # Footer checks:
        assert head_sha in html_text
        assert "2 of 8 live rows carry an In brief line." in html_text
        assert "python tools/board.py --maintainer" in html_text
        assert "Page incomplete" not in html_text

        # Skipped symlinks and missing roadmap reach the page footer:
        for name, lroot, _, _ in _build_ten_symlink_trees(tmp_path / "view_links"):
            if name in ("leaf_outside", "dangling_plans", "dangling_planning"):
                doc = _run_json(lroot, capsys)
                rendered = render_page(doc, head_sha)
                assert "Page incomplete" in rendered
                for sk in doc["skipped_symlinks"]:
                    assert sk in rendered
                if not doc["roadmap_read"]:
                    assert "dev/PLANNING.md was not read" in rendered

        # Failure preservation: board fails (non-UTF-8 file) -> existing page untouched
        sentinel = "<!-- existing page must survive -->\n"
        out_html.write_text(sentinel, encoding="utf-8")
        (repo / "dev" / "plans" / "corrupt.md").write_bytes(b"\xff\xfe")
        with pytest.raises(subprocess.CalledProcessError):
            build_view(out_html)
        assert out_html.read_text(encoding="utf-8") == sentinel

        no_exist = tmp_path / "never_created.html"
        with pytest.raises(subprocess.CalledProcessError):
            build_view(no_exist)
        assert not no_exist.exists()
        (repo / "dev" / "plans" / "corrupt.md").unlink()

        # Failure preservation: git rev-parse fails (non-git directory) -> page untouched
        non_git = tmp_path / "non_git"
        (non_git / "tools").mkdir(parents=True)
        shutil.copy2(CAIRN_ROOT / "tools" / "board.py", non_git / "tools" / "board.py")
        shutil.copy2(CAIRN_ROOT / "tools" / "session.py", non_git / "tools" / "session.py")
        _write(non_git, "dev/plans/ok.md", "# OK\n\n**Status**: implementing\n")
        monkeypatch.chdir(non_git)
        with pytest.raises(subprocess.CalledProcessError):
            build_view(out_html)
        assert out_html.read_text(encoding="utf-8") == sentinel


class TestFinishedPlansRecipe:
    """The `finished-recipe` block reports archived plans only, ordered newest
    first by git author date (`%ad`), one entry per plan."""

    def test_finished_plans_recipe_uses_author_date_and_excludes_proposals_and_edits(
        self, tmp_path: Path
    ) -> None:
        ns = _load_tagged_module("finished-recipe")
        finished_plans = ns["finished_plans"]

        repo = tmp_path / "hist_repo"
        repo.mkdir()
        _git_run(repo, "init")

        # Plan alpha archived on 2026-01-10 (author date) with a later committer date:
        _write(repo, "dev/plans/archive/plan-alpha.md", "# Alpha\n")
        _git_run(repo, "add", ".")
        _git_run(
            repo,
            "commit",
            "-m",
            "archive alpha",
            GIT_AUTHOR_DATE="2026-01-10T12:00:00Z",
            GIT_COMMITTER_DATE="2026-03-01T12:00:00Z",
        )

        # Proposal archived on 2026-02-15 (must not appear):
        _write(repo, "dev/proposals/archive/2026-02-01-prop.md", "# Prop\n")
        _git_run(repo, "add", ".")
        _git_run(
            repo,
            "commit",
            "-m",
            "archive prop",
            GIT_AUTHOR_DATE="2026-02-15T12:00:00Z",
            GIT_COMMITTER_DATE="2026-02-15T12:00:00Z",
        )

        # Plan beta archived on 2026-01-20:
        _write(repo, "dev/plans/archive/plan-beta.md", "# Beta\n")
        _git_run(repo, "add", ".")
        _git_run(
            repo,
            "commit",
            "-m",
            "archive beta",
            GIT_AUTHOR_DATE="2026-01-20T12:00:00Z",
            GIT_COMMITTER_DATE="2026-01-20T12:00:00Z",
        )

        # Plan gamma archived on 2026-02-05:
        _write(repo, "dev/plans/archive/plan-gamma.md", "# Gamma\n")
        _git_run(repo, "add", ".")
        _git_run(
            repo,
            "commit",
            "-m",
            "archive gamma",
            GIT_AUTHOR_DATE="2026-02-05T12:00:00Z",
            GIT_COMMITTER_DATE="2026-02-05T12:00:00Z",
        )

        # Post-archive edit to plan-alpha on 2026-04-01 (must not change archive date or duplicate):
        _write(repo, "dev/plans/archive/plan-alpha.md", "# Alpha edited\n")
        _git_run(repo, "add", ".")
        _git_run(
            repo,
            "commit",
            "-m",
            "edit alpha",
            GIT_AUTHOR_DATE="2026-04-01T12:00:00Z",
            GIT_COMMITTER_DATE="2026-04-01T12:00:00Z",
        )

        result = finished_plans(repo)
        assert result == [
            ("plan-gamma", "2026-02-05"),
            ("plan-beta", "2026-01-20"),
            ("plan-alpha", "2026-01-10"),
        ]

        # Run on Cairn's own repository:
        live_result = finished_plans(CAIRN_ROOT)
        archived_files = [
            p.stem
            for p in (CAIRN_ROOT / "dev" / "plans" / "archive").glob("*.md")
            if not p.name.startswith("_")
        ]
        assert len(live_result) == len(archived_files)


class TestIntentJoinRecipe:
    """The `intent-recipe` block joins `cairn-intent-list/1` claims with live
    board artifacts by `stem` only, never by file overlap, and the guide carries
    the hook safety warning."""

    def test_intent_join_matches_by_stem_only_and_canned_shape_matches_real_tool(
        self, tmp_path: Path
    ) -> None:
        ns = _load_tagged_module("intent-recipe")
        join_intents = ns["join_intents"]

        # Verify canned shape against real tools/intent.py:
        scratch_log = tmp_path / "intents.jsonl"
        intent_tool = str(CAIRN_ROOT / "tools" / "intent.py")
        subprocess.run(
            [
                sys.executable,
                intent_tool,
                "--log-path",
                str(scratch_log),
                "claim",
                "--agent",
                "agent-1",
                "--files",
                "tools/board.py",
                "--action",
                "implement",
                "--stem",
                "board-as-basis",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                sys.executable,
                intent_tool,
                "--log-path",
                str(scratch_log),
                "claim",
                "--agent",
                "agent-2",
                "--files",
                "dev/plans/board-as-basis.md",
                "--action",
                "review",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        real_out = subprocess.run(
            [
                sys.executable,
                intent_tool,
                "--log-path",
                str(scratch_log),
                "list",
                "--format",
                "json",
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        real_doc = json.loads(real_out)
        assert real_doc["schema"] == "cairn-intent-list/1"
        assert len(real_doc["claims"]) == 2
        assert real_doc["claims"][0]["stem"] == "board-as-basis"
        assert real_doc["claims"][1]["stem"] == ""

        canned_claims = [
            {
                "action": "implement",
                "agent": "agent-1",
                "files": ["tools/board.py"],
                "id": "c1",
                "stem": "board-as-basis",
                "ts": "2026-10-19T10:00:00-04:00",
            },
            {
                "action": "edit",
                "agent": "agent-2",
                "files": ["dev/plans/board-as-basis.md"],
                "id": "c2",
                "stem": "",
                "ts": "2026-10-19T10:01:00-04:00",
            },
            {
                "action": "explore",
                "agent": "agent-3",
                "files": ["README.md"],
                "id": "c3",
                "stem": "nonexistent-artifact",
                "ts": "2026-10-19T10:02:00-04:00",
            },
        ]
        assert set(canned_claims[0].keys()) == set(real_doc["claims"][0].keys())

        canned_board = {
            "artifacts": [
                {
                    "archived": False,
                    "id": "board-as-basis",
                    "in_brief": None,
                    "kind": "plan",
                    "opened": "2026-10-18",
                    "path": "dev/plans/board-as-basis.md",
                    "plan_review": None,
                    "review": None,
                    "source_proposal": None,
                    "status": "implementing",
                    "title": "Plan",
                    "waiting_on_maintainer": None,
                },
                {
                    "archived": True,
                    "id": "archived-plan",
                    "in_brief": None,
                    "kind": "plan",
                    "opened": "2026-10-01",
                    "path": "dev/plans/archive/archived-plan.md",
                    "plan_review": None,
                    "review": None,
                    "source_proposal": None,
                    "status": "archived",
                    "title": "Old",
                    "waiting_on_maintainer": None,
                },
            ],
            "includes_archive": True,
            "roadmap_read": True,
            "roadmap_waits": [],
            "schema": "cairn-board/1",
            "skipped_symlinks": [],
        }

        attached, unattached = join_intents(
            canned_board, {"schema": "cairn-intent-list/1", "claims": canned_claims}
        )
        assert list(attached.keys()) == ["board-as-basis"]
        assert [c["id"] for c in attached["board-as-basis"]] == ["c1"]
        assert [c["id"] for c in unattached] == ["c2", "c3"]

        # Empty claims list gives no hints:
        assert join_intents(
            canned_board, {"schema": "cairn-intent-list/1", "claims": []}
        ) == ({}, [])

        # Unknown schemas are refused:
        with pytest.raises(ValueError):
            join_intents(canned_board, {"schema": "cairn-intent-list/2", "claims": []})
        with pytest.raises(ValueError):
            join_intents(
                {**canned_board, "schema": "cairn-board/2"},
                {"schema": "cairn-intent-list/1", "claims": []},
            )

        # Standing phrase in ## Keeping a page honest:
        honest_sec = " ".join(
            _guide_section(
                GUIDE_PATH.read_text(encoding="utf-8"), "## Keeping a page honest"
            ).split()
        )
        assert "whatever commit is checked out" in honest_sec
