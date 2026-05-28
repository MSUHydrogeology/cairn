"""Tests for the module-merge helper (Proposal B / audit gap #3).

Covers:
* Directive parsing: `cairn:merge-target` + `cairn:merge-content-*`
  blocks extract correctly.
* Parse-phase uniqueness validation: duplicate slot anchors in a
  target template raise `DuplicateSlotError` (Antigravity P3).
* Empty-slot insert: merge into a clean slot reports `inserted`.
* Already-current: re-merge against a populated slot reports
  `already-current`.
* Customized marker: a slot carrying `<!-- cairn:customized -->`
  is preserved + reported as `customized` (Antigravity P2).
* Conflict-deferred (non-interactive): writes the `<target>.cairn-
  merge-pending` side-file (Antigravity P1 author-modification:
  always defer, never silently keep, since keep loses the
  module's contributed prose).
* Fidelity check: declared merges that didn't land surface as
  warnings.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_module_merge.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    DuplicateSlotError,
    check_slot_fidelity,
    merge_module_into_slot,
    parse_module_merge_directives,
    validate_unique_slot_names,
)


def _make_target_with_slot(tmp_path: Path, body: str = "") -> Path:
    """Write a minimal target template with one named slot."""
    dst = tmp_path / "core.md"
    dst.write_text(
        "# Target template\n"
        "Pre-slot prose.\n"
        "\n"
        "<!-- cairn:slot test-slot -->\n"
        f"{body}\n"
        "<!-- cairn:end test-slot -->\n"
        "Post-slot prose.\n",
        encoding="utf-8",
    )
    return dst


# ---------------------------------------------------------------------------
# Directive parsing
# ---------------------------------------------------------------------------


class TestParseDirectives:
    def test_single_directive(self) -> None:
        module_text = (
            "# Module foo\n"
            "<!-- cairn:merge-target: core.md > test-slot -->\n"
            "<!-- cairn:merge-content-start -->\n"
            "Module-contributed line one.\n"
            "Module-contributed line two.\n"
            "<!-- cairn:merge-content-end -->\n"
        )
        result = parse_module_merge_directives(module_text)
        assert len(result) == 1
        target, slot, content = result[0]
        assert target == "core.md"
        assert slot == "test-slot"
        assert "Module-contributed line one." in content

    def test_multiple_directives(self) -> None:
        module_text = (
            "<!-- cairn:merge-target: a.md > slot-1 -->\n"
            "<!-- cairn:merge-content-start -->\n"
            "Body A.\n"
            "<!-- cairn:merge-content-end -->\n"
            "\nInterleaved prose.\n\n"
            "<!-- cairn:merge-target: b.md > slot-2 -->\n"
            "<!-- cairn:merge-content-start -->\n"
            "Body B.\n"
            "<!-- cairn:merge-content-end -->\n"
        )
        result = parse_module_merge_directives(module_text)
        assert [(t, s) for t, s, _ in result] == [
            ("a.md", "slot-1"), ("b.md", "slot-2"),
        ]

    def test_no_directives_returns_empty(self) -> None:
        result = parse_module_merge_directives(
            "# Plain module\nNo directives here.\n"
        )
        assert result == []


# ---------------------------------------------------------------------------
# Parse-phase uniqueness validation (Antigravity P3)
# ---------------------------------------------------------------------------


class TestValidateUnique:
    def test_unique_slots_pass(self) -> None:
        text = (
            "<!-- cairn:slot one -->\n<!-- cairn:end one -->\n"
            "<!-- cairn:slot two -->\n<!-- cairn:end two -->\n"
        )
        validate_unique_slot_names(text, src_label="x.md")

    def test_duplicate_raises_with_line_numbers(self) -> None:
        text = (
            "filler\n"
            "<!-- cairn:slot same -->\n"
            "<!-- cairn:end same -->\n"
            "filler\n"
            "<!-- cairn:slot same -->\n"  # duplicate
            "<!-- cairn:end same -->\n"
        )
        with pytest.raises(DuplicateSlotError) as excinfo:
            validate_unique_slot_names(text, src_label="x.md")
        msg = str(excinfo.value)
        assert "x.md" in msg and "same" in msg
        assert "2" in msg and "5" in msg


# ---------------------------------------------------------------------------
# Merge: empty-slot insert
# ---------------------------------------------------------------------------


class TestMergeInsert:
    def test_empty_slot_inserts(self, tmp_path: Path) -> None:
        _make_target_with_slot(tmp_path, body="")
        result = merge_module_into_slot(
            tmp_path, "core.md", "test-slot",
            "New body text",
            non_interactive=True,
        )
        assert result.status == "inserted"
        text = (tmp_path / "core.md").read_text(encoding="utf-8")
        assert "New body text" in text


# ---------------------------------------------------------------------------
# Merge: already-current
# ---------------------------------------------------------------------------


class TestMergeAlreadyCurrent:
    def test_already_current(self, tmp_path: Path) -> None:
        body = "Already in place."
        _make_target_with_slot(tmp_path, body=body)
        result = merge_module_into_slot(
            tmp_path, "core.md", "test-slot",
            body,
            non_interactive=True,
        )
        assert result.status == "already-current"


# ---------------------------------------------------------------------------
# Merge: customized marker (Antigravity P2)
# ---------------------------------------------------------------------------


class TestMergeCustomized:
    def test_customized_marker_preserves_existing(
        self, tmp_path: Path,
    ) -> None:
        body = (
            "<!-- cairn:customized -->\n"
            "Adopter customized this slot intentionally."
        )
        _make_target_with_slot(tmp_path, body=body)
        result = merge_module_into_slot(
            tmp_path, "core.md", "test-slot",
            "Module-contributed text that would have landed here.",
            non_interactive=True,
        )
        assert result.status == "customized"
        # Existing body preserved.
        text = (tmp_path / "core.md").read_text(encoding="utf-8")
        assert "Adopter customized" in text
        assert "Module-contributed text" not in text


# ---------------------------------------------------------------------------
# Merge: conflict-deferred (Antigravity P1)
# ---------------------------------------------------------------------------


class TestMergeConflictDeferred:
    def test_conflict_writes_side_file(self, tmp_path: Path) -> None:
        _make_target_with_slot(
            tmp_path, body="Existing body differs from module."
        )
        result = merge_module_into_slot(
            tmp_path, "core.md", "test-slot",
            "Module-contributed body.",
            non_interactive=True,
        )
        assert result.status == "conflict-deferred"
        side = Path(result.side_file)
        assert side.is_file()
        side_text = side.read_text(encoding="utf-8")
        assert "<<<<<<< Cairn" in side_text
        assert "Module-contributed body." in side_text
        assert ">>>>>>> existing" in side_text
        # Target file NOT modified.
        text = (tmp_path / "core.md").read_text(encoding="utf-8")
        assert "Existing body differs" in text
        assert "Module-contributed body." not in text


# ---------------------------------------------------------------------------
# Fidelity check
# ---------------------------------------------------------------------------


class TestFidelityCheck:
    def test_clean_slot_yields_no_warning(self, tmp_path: Path) -> None:
        _make_target_with_slot(tmp_path, body="exactly the expected content")
        warnings = check_slot_fidelity(
            tmp_path,
            [("core.md", "test-slot", "exactly the expected content")],
        )
        assert warnings == []

    def test_empty_slot_warns(self, tmp_path: Path) -> None:
        _make_target_with_slot(tmp_path, body="")
        warnings = check_slot_fidelity(
            tmp_path,
            [("core.md", "test-slot", "expected content")],
        )
        assert len(warnings) == 1
        assert warnings[0][2] == "empty"

    def test_stale_slot_warns(self, tmp_path: Path) -> None:
        _make_target_with_slot(tmp_path, body="unrelated existing content")
        warnings = check_slot_fidelity(
            tmp_path,
            [("core.md", "test-slot", "expected content")],
        )
        assert len(warnings) == 1
        assert warnings[0][2] == "stale-or-partial"

    def test_customized_slot_skipped(self, tmp_path: Path) -> None:
        _make_target_with_slot(
            tmp_path,
            body="<!-- cairn:customized -->\nadopter's own content",
        )
        warnings = check_slot_fidelity(
            tmp_path,
            [("core.md", "test-slot", "expected content")],
        )
        assert warnings == []
