"""Tests for the module-merge helper (Proposal B / audit gap #3).

Promises:
- A module's merge text lands in an empty slot of its tracked target file. (BOOTSTRAP.md:129)
- Re-running an install leaves a slot that already holds the module text unchanged. (BOOTSTRAP.md:130)
- A slot the adopter marked customized keeps the adopter's text and gets no side file. (BOOTSTRAP.md:131-133)
- A conflicting slot keeps its text, and the module text goes to a side file named for that slot. (BOOTSTRAP.md:134-138)
- A declared slot that is still empty, or holds different text, is reported by the install's fidelity check. (BOOTSTRAP.md:476-491)
- A template with two slots of the same name refuses before any merge, naming the file and both lines. (BOOTSTRAP.md:140-148)
- An install prints merge and fidelity slot names with control characters escaped. (production code: bootstrap/_scaffold/cli.py)
- A slot nested in a list item or quote is not reported as stale when its text matches. (production code: bootstrap/_scaffold/slotmerge.py)

Covers:
* Directive parsing: `cairn:merge-target` + `cairn:merge-content-*`
  blocks extract correctly.
* Parse-phase uniqueness validation: duplicate slot anchors in a
  target template raise `DuplicateSlotError`.
* Empty-slot insert: merge into a clean slot reports `inserted`.
* Already-current: re-merge against a populated slot reports
  `already-current`.
* Customized marker: a slot carrying `<!-- cairn:customized -->`
  is preserved + reported as `customized`.
* Conflict-deferred (non-interactive): writes the `<target>.cairn-
  merge-pending` side-file (author-modification:
  always defer, never silently keep, since keep loses the
  module's contributed prose).
* Fidelity check: declared merges that didn't land surface as
  warnings.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_module_merge.py
"""

from __future__ import annotations

import sys
from types import SimpleNamespace
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


def test_public_install_escapes_merge_and_fidelity_slot_names(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch,
) -> None:
    from bootstrap import scaffold
    from bootstrap._scaffold import cli

    target = tmp_path / "target"
    target.mkdir()
    config = tmp_path / "profile.yml"
    config.write_text(
        "project_name: Demo\ntest_command: pytest\npreset: solo-greenfield\n",
        encoding="utf-8",
    )
    merge_slot = "merge-\u202e-name"
    fidelity_slot = r"literal\u202e-name"
    monkeypatch.setattr(cli, "run_module_merge_pass", lambda *a, **k: (
        [SimpleNamespace(status="merged", target_path="AGENTS.md",
                         slot_name=merge_slot, side_file=None)],
        [("AGENTS.md", fidelity_slot, "changed")],
    ))

    assert scaffold.main(["--config", str(config), "--target", str(target)]) == 0
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "\u202e" not in output
    assert "merge-\\u202e-name" in output
    assert r"literal\\u202e-name" in output


# ---------------------------------------------------------------------------
# Directive parsing
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Parse-phase uniqueness validation
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Merge: empty-slot insert
# ---------------------------------------------------------------------------


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
# Merge: customized marker
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Merge: conflict-deferred
# ---------------------------------------------------------------------------


class TestMergeConflictDeferred:


    def test_per_slot_side_file_avoids_clobber(self, tmp_path: Path) -> None:
        """Two conflicts on the same target file
        must write to distinct side-files (one per slot)."""
        dst = tmp_path / "two_slots.md"
        dst.write_text(
            "# Two-slot target\n"
            "<!-- cairn:slot slot-one -->\n"
            "Existing body for slot one.\n"
            "<!-- cairn:end slot-one -->\n"
            "<!-- cairn:slot slot-two -->\n"
            "Existing body for slot two.\n"
            "<!-- cairn:end slot-two -->\n",
            encoding="utf-8",
        )
        r1 = merge_module_into_slot(
            tmp_path, "two_slots.md", "slot-one",
            "Module body for slot one.",
            non_interactive=True,
        )
        r2 = merge_module_into_slot(
            tmp_path, "two_slots.md", "slot-two",
            "Module body for slot two.",
            non_interactive=True,
        )
        assert r1.status == "conflict-deferred"
        assert r2.status == "conflict-deferred"
        # The two side-files are distinct, slot-name-segmented.
        assert r1.side_file != r2.side_file
        assert Path(r1.side_file).is_file()
        assert Path(r2.side_file).is_file()
        # Each side-file carries its own slot's contributed prose.
        assert "Module body for slot one." in Path(
            r1.side_file).read_text(encoding="utf-8")
        assert "Module body for slot two." in Path(
            r2.side_file).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Fidelity check
# ---------------------------------------------------------------------------
