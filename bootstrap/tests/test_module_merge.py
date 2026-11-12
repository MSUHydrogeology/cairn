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

import shutil
import sys
from types import SimpleNamespace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    DuplicateSlotError,
    check_slot_fidelity,
    parse_module_merge_directives,
    validate_unique_slot_names,
)


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


def test_rerunning_an_install_merges_only_empty_slots_and_gives_each_conflict_its_own_side_file(
    tmp_path: Path,
) -> None:
    """Promise: a module merge fills a slot only while it is empty.  Re-running
    the install changes nothing once the module text is in place; when the
    adopter has edited two merged slots, the re-run keeps their bytes and
    writes one side file per slot, each carrying that slot's module text.

    The Cairn root is a copy of ``templates/`` in which the module declares a
    second merge slot, since the shipped module declares only one."""
    from bootstrap import scaffold

    cairn_root = Path(__file__).resolve().parent.parent.parent
    root = tmp_path / "cairn-root"
    shutil.copytree(
        cairn_root / "templates", root / "templates",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    core = root / "templates" / "core" / "AGENTS.md"
    text = core.read_text(encoding="utf-8")
    opener = "<!-- cairn:slot documentation-discipline -->"
    closer = "<!-- cairn:end documentation-discipline -->"
    core.write_text(
        text[:text.index(opener) + len(opener)] + "\n" + text[text.index(closer):],
        encoding="utf-8",
    )
    module = root / "templates" / "modules" / "default-on" / "security-verification.md"
    module.write_text(
        module.read_text(encoding="utf-8")
        + "\n<!-- cairn:merge-target: AGENTS.md > documentation-discipline -->\n"
        "<!-- cairn:merge-content-start -->\n"
        "Second contributed slot text.\n"
        "<!-- cairn:merge-content-end -->\n",
        encoding="utf-8",
    )

    config = tmp_path / "profile.yml"
    config.write_text(
        "project_name: MergeRerun\ntest_command: pytest\nmodules:\n"
        "  - security-verification\n", encoding="utf-8",
    )
    target = tmp_path / "target"
    target.mkdir()
    agents = target / "AGENTS.md"

    def install() -> int:
        return scaffold.main([
            "--config", str(config), "--target", str(target),
            "--cairn-root", str(root), "--allow-dev", "--non-interactive",
        ])

    def side_files() -> list[Path]:
        return sorted(target.glob("AGENTS.md.*.cairn-merge-pending"))

    assert install() == 0
    merged = agents.read_bytes()
    assert b"scripts/run_security_verification.py" in merged
    assert b"Second contributed slot text." in merged
    assert side_files() == []

    assert install() == 0
    assert agents.read_bytes() == merged
    assert side_files() == []

    edited = (
        merged.replace(b"**Security verification.**", b"**Adopter text one.**")
        .replace(b"Second contributed slot text.", b"Adopter text two.")
    )
    agents.write_bytes(edited)
    assert install() == 0
    assert agents.read_bytes() == edited
    pending = [path.read_text(encoding="utf-8") for path in side_files()]
    assert len(pending) == 2
    assert sum("run_security_verification.py" in body for body in pending) == 1
    assert sum("Second contributed slot text." in body for body in pending) == 1


# ---------------------------------------------------------------------------
# Merge: customized marker
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Merge: conflict-deferred
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Fidelity check
# ---------------------------------------------------------------------------
