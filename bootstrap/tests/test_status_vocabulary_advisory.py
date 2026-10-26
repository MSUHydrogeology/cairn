# SPDX-License-Identifier: MIT
"""The board and `session-start` name a status that is outside the vocabulary.

A retired token (`proposed`, `executing`) or a value that is not a status at
all is listed like any other artifact and then named in one advisory line. The
failure these guard is the silent copy of an old example: both tools used to
list `proposed` with no sign it was retired. They warn and never refuse, so
every artifact stays on the listing and the exit code does not change.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]


def _load(rel: str, name: str):
    spec = importlib.util.spec_from_file_location(name, CAIRN_ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


board = _load("tools/board.py", "_cairn_board_vocab")
# The shipped twin; a separate test pins it byte-identical to tools/session.py.
session = _load("templates/skills/_lib/session.py", "_cairn_session_vocab")

PROPOSAL_WORDS = ("awaiting-review", "revising", "awaiting-decision",
                  "accepted", "rejected", "superseded")
PLAN_WORDS = ("awaiting-plan-review", "revising-plan", "ready-to-implement",
              "implementing", "awaiting-code-review", "revising-code",
              "ready-to-archive", "archived")


def _artifact(root: Path, rel: str, status: str) -> None:
    path = root / "dev" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# x\n\n**Status**: {status}\n\n## Body\n",
                    encoding="utf-8")


def _lines(out: str):
    return [ln for ln in out.splitlines() if "advisory" in ln]


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """A scratch git repo, which `session-start` needs."""
    root = tmp_path.resolve()
    for args in (("init", "-q"), ("config", "user.email", "t@example.com"),
                 ("config", "user.name", "T"),
                 ("config", "commit.gpgsign", "false")):
        subprocess.run(["git", *args], cwd=str(root), check=True,
                       capture_output=True)
    (root / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "add", "f.txt"], cwd=str(root), check=True,
                   capture_output=True)
    subprocess.run(["git", "commit", "-q", "-m", "initial"], cwd=str(root),
                   check=True, capture_output=True)
    return root


class TestTheBoardFlagsStatusesOutsideTheVocabulary:
    @staticmethod
    def _run(root: Path, capsys, *extra: str):
        rc = board.main([*extra, "--root", str(root)])
        out = capsys.readouterr().out
        return rc, out, _lines(out)

    def test_retired_and_unknown_statuses_are_named_and_still_listed(
            self, tmp_path, capsys) -> None:
        _artifact(tmp_path, "proposals/2026-10-23-x-retired.md", "proposed")
        _artifact(tmp_path, "plans/retired-plan.md", "executing")
        _artifact(tmp_path, "proposals/2026-10-23-x-garbage.md", "banana")

        rc, out, advisory = self._run(tmp_path, capsys)

        assert rc == 0
        assert "board: 3 row(s)." in out
        assert len(advisory) == 1
        assert "3 active artifacts" in advisory[0]
        assert "2026-10-23-x-retired (proposed: retired)" in advisory[0]
        assert "retired-plan (executing: retired)" in advisory[0]
        assert "2026-10-23-x-garbage (banana: unknown)" in advisory[0]

    def test_a_status_belonging_to_the_other_kind_is_unknown(
            self, tmp_path, capsys) -> None:
        """`implementing` is a plan word and `accepted` is a proposal word."""
        _artifact(tmp_path, "proposals/2026-10-23-x-wrong.md", "implementing")
        _artifact(tmp_path, "plans/wrong.md", "accepted")

        _, _, advisory = self._run(tmp_path, capsys)

        assert len(advisory) == 1
        assert "2026-10-23-x-wrong (implementing: unknown)" in advisory[0]
        assert "wrong (accepted: unknown)" in advisory[0]

    def test_every_allowed_status_passes_with_or_without_a_note(
            self, tmp_path, capsys) -> None:
        for i, word in enumerate(PROPOSAL_WORDS):
            note = " — a note" if i % 2 else ""
            _artifact(tmp_path, f"proposals/2026-10-23-x-p{i}.md",
                      f"{word}{note}")
        for i, word in enumerate(PLAN_WORDS):
            note = " (a note)" if i % 2 else ""
            _artifact(tmp_path, f"plans/p{i}.md", f"{word}{note}")

        rc, out, advisory = self._run(tmp_path, capsys)

        assert rc == 0
        assert f"board: {len(PROPOSAL_WORDS) + len(PLAN_WORDS)} row(s)." in out
        assert advisory == []

    def test_a_word_that_only_starts_like_an_allowed_one_is_unknown(
            self, tmp_path, capsys) -> None:
        for i, word in enumerate(("awaiting-decision2", "awaiting-decision_x",
                                  "awaiting-decision-x", "awaiting-decisions")):
            _artifact(tmp_path, f"proposals/2026-10-23-x-n{i}.md", word)

        _, _, advisory = self._run(tmp_path, capsys)

        assert "4 active artifacts" in advisory[0]

    def test_an_archived_record_keeps_its_old_token_unflagged(
            self, tmp_path, capsys) -> None:
        _artifact(tmp_path, "proposals/archive/2026-01-01-x-old.md", "revised")
        _artifact(tmp_path, "plans/archive/old.md", "executing")
        _artifact(tmp_path, "plans/live.md", "implementing")

        _, out, advisory = self._run(tmp_path, capsys, "--archive")

        assert "board: 3 row(s)." in out
        assert advisory == []

    def test_the_json_form_is_unchanged(self, tmp_path, capsys) -> None:
        _artifact(tmp_path, "proposals/2026-10-23-x-retired.md", "proposed")

        rc, out, _ = self._run(tmp_path, capsys, "--json")

        assert rc == 0
        assert "advisory" not in out
        assert json.loads(out)["artifacts"][0]["status"] == "proposed"


class TestSessionStartFlagsStatusesOutsideTheVocabulary:
    def test_retired_and_unknown_statuses_are_named_and_still_listed(
            self, repo, monkeypatch, capsys) -> None:
        for rel, status in (
            ("proposals/2026-10-23-x-retired.md", "proposed"),
            ("plans/retired-plan.md", "executing"),
            ("proposals/2026-10-23-x-garbage.md", "banana"),
            ("proposals/2026-10-23-x-fine.md", "awaiting-decision -- a note"),
            ("plans/fine.md", "implementing"),
            ("plans/archive/old.md", "executing"),
        ):
            _artifact(repo, rel, status)
        monkeypatch.chdir(repo)

        rc = session.main(["session-start"])

        out = capsys.readouterr().out
        assert rc == 0
        assert "proposals/2026-10-23-x-retired.md -- proposed" in out
        advisory = _lines(out)
        assert len(advisory) == 1
        assert "3 active artifacts" in advisory[0]
        assert ("proposals/2026-10-23-x-retired.md (proposed: retired)"
                in advisory[0])
        assert "plans/retired-plan.md (executing: retired)" in advisory[0]
        assert ("proposals/2026-10-23-x-garbage.md (banana: unknown)"
                in advisory[0])
        assert "fine.md" not in advisory[0] and "old.md" not in advisory[0]

    def test_it_is_quiet_when_every_status_is_allowed(
            self, repo, monkeypatch, capsys) -> None:
        _artifact(repo, "proposals/2026-10-23-x-ok.md", "accepted")
        _artifact(repo, "plans/ok.md", "ready-to-implement")
        monkeypatch.chdir(repo)

        session.main(["session-start"])

        assert _lines(capsys.readouterr().out) == []
