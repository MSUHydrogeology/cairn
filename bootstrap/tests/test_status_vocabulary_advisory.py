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
import re
import subprocess
import unicodedata
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


# --- one tool judges a file the way the other does -------------------------

def _board_flagged(root: Path, capsys) -> set:
    board.main(["--root", str(root)])
    out = capsys.readouterr().out
    return set(re.findall(r"(\S+) \([^()]*: (?:retired|unknown)\)",
                          "\n".join(_lines(out))))


def _session_flagged(root: Path, monkeypatch, capsys) -> set:
    monkeypatch.chdir(root)
    session.main(["session-start"])
    out = capsys.readouterr().out
    return {name.rsplit("/", 1)[1][:-3] for name in re.findall(
        r"(\S+) \([^()]*: (?:retired|unknown)\)", "\n".join(_lines(out)))}


class TestBothToolsReadOneStatusTheSameWay:
    # (status, is it flagged). A word ends at the end of the text, a space or
    # tab, or ASCII punctuation; a hyphen, underscore, digit, letter or any
    # non-ASCII or invisible character right after it makes a different word.
    CASES = (
        ("awaiting-decision", False),
        ("awaiting-decision -- a note", False),
        ("awaiting-decision (a note)", False),
        ("awaiting-decision: a note", False),
        ("awaiting-decision, a note", False),
        ("awaiting-decision.", False),
        ("awaiting-decision\tnote", False),
        ("`awaiting-decision`", False),
        ("**awaiting-decision**", False),
        ("*awaiting-decision*", False),
        ("awaiting-decision-x", True),
        ("awaiting-decision-", True),
        ("awaiting-decision--note", True),
        ("awaiting-decision_x", True),
        ("awaiting-decision2", True),
        ("awaiting-decision\u00e9", True),
        ("awaiting-decision\u200b", True),
        ("awaiting-decision\u00a0note", True),
        ("awaiting-decision\x00", True),
        ("**banana**", True),
        ("_awaiting-decision_", True),
    )

    def _chunks(self, root: Path):
        """The cases in groups of eight, each written alone and cleared after,
        because one advisory line names at most ten artifacts."""
        base = root / "dev" / "proposals"
        for start in range(0, len(self.CASES), 8):
            chunk = list(enumerate(self.CASES))[start:start + 8]
            for i, (status, _) in chunk:
                _artifact(root, f"proposals/2026-10-23-x-c{i:02d}.md", status)
            yield {f"2026-10-23-x-c{i:02d}" for i, (_, flagged) in chunk
                   if flagged}
            for path in base.glob("*.md"):
                path.unlink()

    def test_the_two_advisories_flag_the_same_artifacts(
            self, repo, monkeypatch, capsys) -> None:
        for expected in self._chunks(repo):
            assert _board_flagged(repo, capsys) == expected
            assert _session_flagged(repo, monkeypatch, capsys) == expected


class TestEveryRetiredWordIsNamedRetired:
    @pytest.mark.parametrize("word", ["proposed", "reviewed", "revised",
                                      "open", "executing", "review"])
    def test_a_retired_word_reads_retired_for_either_kind(self, word) -> None:
        assert session._status_problem("proposal", word) == "retired"
        assert session._status_problem("plan", word) == "retired"


# --- the four guards that keep the advisory from misfiring -------------------

class TestTheGuardsAroundTheMatcher:
    def test_a_blank_status_is_silent_in_both_tools(
            self, repo, monkeypatch, capsys) -> None:
        """A blank `**Status**:` has nothing to judge. The board must not trip
        on it, and session-start must not abort before the interpreter
        binding is resolved."""
        _artifact(repo, "proposals/2026-10-23-x-blank.md", "")
        _artifact(repo, "plans/blank.md", "   ")

        board_rc = board.main(["--root", str(repo)])
        board_out = capsys.readouterr().out
        monkeypatch.chdir(repo)
        session_rc = session.main(["session-start"])
        session_out = capsys.readouterr().out

        assert board_rc == 0 and session_rc == 0
        assert _lines(board_out) == [] and _lines(session_out) == []

    def test_an_artifact_with_no_status_line_is_silent_in_session_start(
            self, repo, monkeypatch, capsys) -> None:
        (repo / "dev" / "plans").mkdir(parents=True)
        (repo / "dev" / "plans" / "nostatus.md").write_text(
            "# x\n\n## Body\n", encoding="utf-8")
        monkeypatch.chdir(repo)

        rc = session.main(["session-start"])

        out = capsys.readouterr().out
        assert rc == 0
        assert "plans/nostatus.md -- (no status line)" in out
        assert _lines(out) == []

    def test_only_the_first_word_of_a_flagged_status_is_printed(
            self, repo, monkeypatch, capsys) -> None:
        _artifact(repo, "proposals/2026-10-23-x-old.md",
                  "proposed -- old note about why")

        board_advisory = self._board(repo, capsys)
        monkeypatch.chdir(repo)
        session.main(["session-start"])
        session_advisory = _lines(capsys.readouterr().out)

        for advisory in (board_advisory, session_advisory):
            assert len(advisory) == 1
            assert "(proposed: retired)" in advisory[0]
            assert "old note" not in advisory[0]

    def test_a_backticked_allowed_word_is_allowed(
            self, repo, monkeypatch, capsys) -> None:
        _artifact(repo, "proposals/2026-10-23-x-tick.md", "`awaiting-review`")
        _artifact(repo, "plans/tick.md", "`implementing` -- round 2")

        assert self._board(repo, capsys) == []
        monkeypatch.chdir(repo)
        session.main(["session-start"])
        assert _lines(capsys.readouterr().out) == []

    @staticmethod
    def _board(root: Path, capsys):
        board.main(["--root", str(root)])
        return _lines(capsys.readouterr().out)


# --- untrusted status text reaches the terminal inert -------------------------

HOSTILE = (
    "x\x1b[31mred",
    "x\x00y",
    "x\x07y",
    "x\u202ey",
    "x\u2066y\u2069",
    "x\U000e0041y",
    "x\u034fy",
    "y" * 10000,
    "y" * 10000 + " a note",
)


def _inert(text: str) -> bool:
    """No control, format, separator, private-use or tag character other than
    the line break that ends each line, and no combining grapheme joiner."""
    return not any(
        unicodedata.category(ch) in ("Cc", "Cf", "Zl", "Zp", "Co", "Cs")
        or ch == "\u034f"
        for ch in text.replace("\n", ""))


class TestStatusTextIsEncodedBeforeItIsPrinted:
    def _tree(self, root: Path) -> None:
        for i, status in enumerate(HOSTILE):
            _artifact(root, f"proposals/2026-10-23-x-h{i}.md", status)

    def test_the_board_prints_a_hostile_status_inert_and_bounded(
            self, tmp_path, capsys) -> None:
        self._tree(tmp_path)

        rc = board.main(["--root", str(tmp_path)])

        out = capsys.readouterr().out
        assert rc == 0
        advisory = _lines(out)
        assert len(advisory) == 1
        assert f"{len(HOSTILE)} active artifacts" in advisory[0]
        assert "\\x1b" in advisory[0]   # the escape is shown, not sent
        assert _inert(out)
        # each status is cut to 200 characters; ten names stay well under 10 KB
        assert len(advisory[0]) < 10000

    def test_session_start_prints_a_hostile_status_inert_and_bounded(
            self, repo, monkeypatch, capsys) -> None:
        self._tree(repo)
        monkeypatch.chdir(repo)

        rc = session.main(["session-start"])

        out = capsys.readouterr().out
        assert rc == 0
        advisory = _lines(out)
        assert len(advisory) == 1
        assert f"{len(HOSTILE)} active artifacts" in advisory[0]
        assert _inert(out)
        assert len(advisory[0]) < 10000


# --- the line names ten artifacts and counts the rest --------------------------

class TestTheAdvisoryNamesTenAndCountsTheRest:
    @staticmethod
    def _tree(root: Path, n: int) -> None:
        for i in range(n):
            _artifact(root, f"proposals/2026-10-23-x-b{i:02d}.md", "banana")

    def _check(self, advisory: str, total: int) -> None:
        assert f"{total} active artifacts" in advisory
        assert advisory.count("(banana: unknown)") == 10
        assert f"and {total - 10} more" in advisory
        assert "b09" in advisory and "b10" not in advisory

    def test_the_board_line_is_capped(self, tmp_path, capsys) -> None:
        self._tree(tmp_path, 25)

        board.main(["--root", str(tmp_path)])

        (advisory,) = _lines(capsys.readouterr().out)
        self._check(advisory, 25)

    def test_the_session_start_line_is_capped(
            self, repo, monkeypatch, capsys) -> None:
        self._tree(repo, 25)
        monkeypatch.chdir(repo)

        session.main(["session-start"])

        (advisory,) = _lines(capsys.readouterr().out)
        self._check(advisory, 25)

    def test_ten_or_fewer_are_all_named_with_no_tail(
            self, tmp_path, capsys) -> None:
        self._tree(tmp_path, 10)

        board.main(["--root", str(tmp_path)])

        (advisory,) = _lines(capsys.readouterr().out)
        assert advisory.count("(banana: unknown)") == 10
        assert "more" not in advisory


# --- the in-flight list and the advisory count the same files --------------------

class TestTheListAndTheAdvisoryWalkTheSameFiles:
    def test_a_template_is_in_neither_and_a_live_file_is_in_both(
            self, repo) -> None:
        _artifact(repo, "proposals/_template.md", "banana")
        _artifact(repo, "plans/_template.md", "banana")
        _artifact(repo, "plans/live.md", "banana")
        (repo / "dev" / "plans" / "notes.txt").write_text("x", encoding="utf-8")

        threads = session._in_flight(repo)
        advisory = session._in_flight_status_advisory(repo)

        assert threads == ["plans/live.md -- banana"]
        assert "plans/live.md (banana: unknown)" in advisory
        assert "_template" not in advisory and "1 active artifact " in advisory

    def test_the_helper_yields_kind_name_and_status(self, repo) -> None:
        _artifact(repo, "proposals/2026-10-23-x-a.md", "accepted")
        _artifact(repo, "plans/b.md", "implementing")

        assert session._in_flight_items(repo) == [
            ("proposal", "2026-10-23-x-a.md", "accepted"),
            ("plan", "b.md", "implementing"),
        ]


# --- the table agrees with the doctrine ------------------------------------------

def _diagram_words(rel: str) -> set:
    """The status words drawn as node labels (`ID["word<br/>(holder)"]`) in a
    doctrine page's flowcharts."""
    text = (CAIRN_ROOT / rel).read_text(encoding="utf-8")
    return {label.split("<br/>")[0].strip()
            for label in re.findall(r'\["([^"]+)"\]', text)}


class TestTheVocabularyMatchesTheDoctrineDiagrams:
    def test_lifecycle_diagrams_draw_exactly_the_words_in_the_table(
            self) -> None:
        """If the doctrine gains or drops a status and this table does not
        follow, every artifact carrying it would be flagged (or a dead word
        accepted) until someone noticed."""
        table = (set(session._STATUS_VOCABULARY["proposal"])
                 | set(session._STATUS_VOCABULARY["plan"]))
        drawn = _diagram_words("doctrine/lifecycle.md")

        assert len(drawn) >= 14, drawn
        assert drawn == table

    def test_the_plan_page_draws_exactly_the_plan_words(self) -> None:
        drawn = _diagram_words("doctrine/plans.md")

        assert drawn == set(session._STATUS_VOCABULARY["plan"])

    def test_no_retired_word_is_also_an_allowed_word(self) -> None:
        allowed = (set(session._STATUS_VOCABULARY["proposal"])
                   | set(session._STATUS_VOCABULARY["plan"]))

        assert not allowed & set(session._RETIRED_STATUSES)
