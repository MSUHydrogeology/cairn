"""Chunk F -- the derived lifecycle board, its terminal encoder, and its
optional work-intent provider.

Source contract: accepted proposal
``dev/proposals/archive/2026-08-10-codex-lifecycle-status-vocabulary.md``.  The
operative board clauses are spread across three revisions and the delta
statements resolve them:

* **B0** Revision 2 -- purpose and authority boundary.
* **B1** Revision 3's *"B1 replacement"* -- the row contract, including
  ``active_intent``.  Revision 2's B1 is superseded.
* **B2** Revision 2 -- ``--format json``, the three filters, ``--explain``.
* **B3** Revision 2 (*"one parser, one pass, no cache"*) **plus** Revision 3's
  *"B3 addition"* (the optional provider).  Revision 3 says *addition*, so the
  Revision 2 clause is still binding.
* **B4** Revision 4's *"B4 final replacement"* -- ``isprintable()`` plus the
  explicit unsafe-range table.  It replaces Revision 3's category-only rule,
  which replaced Revision 2's.
* **B7** Revision 2 + Revision 3's *"B7 additions"*, with the Unicode bullet
  replaced by Revision 4's *"B7 final Unicode falsifier"*.

The load-bearing shape of this module is that the Unicode oracle is
**directional**: the expanded content-scan display-unsafe population must be a
**subset** of what the board escapes.  The board may escape more; it may never
emit raw a code point the scanner recognizes.  So adding a printable invisible to
the scanner reddens this file until the planner's range table follows, and
*narrowing* a detector cannot quietly weaken terminal output.

Unmarked by design: these nodes are always collectible, so their ids stay a
``COLLECTION-ADDED`` note for the gate manifest rather than a skip/xfail
re-anchor.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
_PLANNER_TEMPLATE = (
    CAIRN_ROOT / "templates" / "skills" / "_lib" / "lifecycle_planner.py"
)
_PLANNER_SOURCE = CAIRN_ROOT / "tools" / "lifecycle_planner.py"
_CONTENT_SCAN = CAIRN_ROOT / "scripts" / "content_scan.py"
_INTENT_CLI_SOURCE = CAIRN_ROOT / "tools" / "_intent" / "cli.py"
_INTENT_CLI_TEMPLATE = (
    CAIRN_ROOT / "templates" / "modules" / "team-gated" / "_intent" / "cli.py"
)


def _load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


#: The board is loaded from the **template** copy, like every other lifecycle
#: contract test: that copy is what ships to an adopter, so it is the one whose
#: behaviour a test must pin.  Twin byte identity is asserted separately below,
#: which is what makes reading one copy a claim about both.
planner = _load(_PLANNER_TEMPLATE, "cairn_lifecycle_board_planner")

#: The reviewed content scanner, imported **in the test environment only**.  The
#: board must not import it at runtime (it is a conditional module), which is
#: exactly why the drift guard lives here instead.
scan = _load(_CONTENT_SCAN, "cairn_content_scan_for_board")


# --- fixtures ----------------------------------------------------------------


def _git(args, cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True,
                   capture_output=True, text=True)


def _make_repo(tmp_path: Path, name: str = "repo") -> Path:
    repo = tmp_path / name
    repo.mkdir(parents=True)
    _git(["init", "-q"], repo)
    _git(["config", "user.email", "t@example.com"], repo)
    _git(["config", "user.name", "Test"], repo)
    (repo / "dev" / "proposals").mkdir(parents=True)
    (repo / "dev" / "plans").mkdir(parents=True)
    return repo


def _commit_all(repo: Path) -> None:
    _git(["add", "-A"], repo)
    _git(["commit", "-q", "-m", "fixture"], repo)


_BASIS = (
    "**Reviewed commit**: " + ("a" * 40) + "\n"
    "**Target**: the whole artifact\n"
    "**Prior findings**: none\n"
    "**Assurance path**: standard\n"
)


def _pass_block(kind: str, reviewer: str = "Reviewer A", date: str = "2026-05-02",
                tier: str = "Internal", findings: str = "none",
                obligation: str | None = None) -> str:
    obligation_line = "" if obligation is None else f"**Obligation**: {obligation}\n"
    return (
        f"\n## {kind} -- {reviewer} -- {date}\n\n"
        f"**Tier**: {tier}\n"
        f"**Findings**: {findings}\n"
        f"{obligation_line}"
        f"{_BASIS}\n"
        "body\n"
    )


def _write_proposal(repo: Path, stem: str, *, status: str,
                    author: str = "Author A", body: str = "",
                    assurance: str | None = "standard") -> Path:
    path = repo / "dev" / "proposals" / f"{stem}.md"
    declaration = "" if assurance is None else f"**Assurance path**: {assurance}\n"
    path.write_text(
        f"# {stem}\n\n"
        f"**Author**: {author} (Strategy)\n"
        f"**Date opened**: 2026-05-01\n"
        f"**Status**: {status}\n"
        f"{declaration}"
        f"**Plan review**: required — Internal\n\n"
        "## Context\n\nx\n"
        f"{body}",
        encoding="utf-8")
    return path


def _write_plan(repo: Path, stem: str, *, status: str,
                plan_review: str = "required(Internal)",
                blocked_by: str | None = None, body: str = "") -> Path:
    path = repo / "dev" / "plans" / f"{stem}.md"
    blocker = "" if blocked_by is None else f"**Blocked by**: {blocked_by}\n"
    path.write_text(
        f"# {stem}\n\n"
        f"**Status**: {status}\n"
        f"**Plan review**: {plan_review}\n"
        f"{blocker}\n"
        "## Scope\n\nx\n"
        f"{body}",
        encoding="utf-8")
    return path


def _board(monkeypatch, repo: Path, capsys, argv, module: ModuleType | None = None):
    """Run one board invocation -> ``(exit_status, stdout, stderr)``."""
    mod = module or planner
    monkeypatch.chdir(repo)
    status = mod.main(argv)
    captured = capsys.readouterr()
    return status, captured.out, captured.err


def _rows(out: str) -> list[list[str]]:
    """The compact data rows, split on the field delimiter (header excluded)."""
    prefix = planner._PREFIX + " "
    header = planner._BOARD_FIELD_DELIMITER.join(planner.BOARD_FIELDS)
    lines = [line[len(prefix):] for line in out.splitlines()
             if line.startswith(prefix)]
    if header not in lines:
        return []
    body = lines[lines.index(header) + 1:]
    return [line.split(planner._BOARD_FIELD_DELIMITER) for line in body
            if line.count(planner._BOARD_FIELD_DELIMITER)
            == len(planner.BOARD_FIELDS) - 1]


def _cells(out: str) -> list[dict]:
    return [dict(zip(planner.BOARD_FIELDS, row)) for row in _rows(out)]


# =============================================================================
# B1 -- the compact row contract
# =============================================================================


class TestCompactRows:

    def test_one_row_per_active_artifact_in_declared_order(
            self, tmp_path, monkeypatch, capsys):
        """B1: one line per active direct child, sorted by kind then stem, with
        templates and the archive tree excluded."""
        repo = _make_repo(tmp_path)
        _write_proposal(repo, "b-prop", status="awaiting-review")
        _write_proposal(repo, "a-prop", status="awaiting-review")
        _write_plan(repo, "z-plan", status="awaiting-plan-review")
        _write_plan(repo, "m-plan", status="awaiting-plan-review")
        (repo / "dev" / "plans" / "_template.md").write_text(
            "# t\n\n**Status**: open\n", encoding="utf-8")
        (repo / "dev" / "proposals" / "README.md").write_text("# r\n",
                                                             encoding="utf-8")
        (repo / "dev" / "plans" / "archive").mkdir()
        _write_plan(repo, "archived-one", status="archived")
        shutil.move(str(repo / "dev" / "plans" / "archived-one.md"),
                    str(repo / "dev" / "plans" / "archive" / "archived-one.md"))
        _commit_all(repo)

        _status, out, _err = _board(monkeypatch, repo, capsys,
                                    ["board", "--compact"])
        cells = _cells(out)
        assert [(row["kind"], row["artifact"]) for row in cells] == [
            ("proposal", "a-prop"), ("proposal", "b-prop"),
            ("plan", "m-plan"), ("plan", "z-plan"),
        ]

    def test_ordering_is_deterministic_across_runs(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        for stem in ("d", "a", "c", "b"):
            _write_plan(repo, stem, status="awaiting-plan-review")
        _commit_all(repo)
        first = _cells(_board(monkeypatch, repo, capsys, ["board"])[1])
        second = _cells(_board(monkeypatch, repo, capsys, ["board"])[1])
        assert first == second
        assert [row["artifact"] for row in first] == ["a", "b", "c", "d"]

    def test_every_row_carries_every_field_in_the_documented_order(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert planner.BOARD_FIELDS == (
            "kind", "artifact", "status", "owner", "active_intent", "review",
            "evidence", "blocked_by", "validity", "source")
        assert len(_rows(out)) == 1
        assert len(_rows(out)[0]) == len(planner.BOARD_FIELDS)

    def test_header_reports_full_head_dirty_state_and_intent_coverage(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(repo),
                              capture_output=True, text=True,
                              check=True).stdout.strip()
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert len(head) == 40
        assert head in out, "the header must name the FULL HEAD object id"
        assert "lifecycle files differ from HEAD: no" in out
        assert "intent coverage:" in out


class TestOwnerVocabulary:
    """B1's `owner` comes from the central vocabulary, and B3 forbids a
    consumer-local role table.  These nodes bind the new table to the state
    machine that already existed rather than to a hand-written expectation."""

    @pytest.mark.parametrize("kind", ["proposal", "plan"])
    def test_every_current_state_resolves_an_owner(self, kind):
        states = (planner.PROPOSAL_STATES if kind == "proposal"
                  else planner.PLAN_STATES)
        for state in states:
            owner = planner.next_owner(kind, state)
            assert owner in planner.NEXT_OWNERS, (kind, state, owner)
            assert owner != planner.NEXT_OWNER_UNKNOWN, (
                f"{kind} state {state!r} has no declared next owner")

    @pytest.mark.parametrize("kind", ["proposal", "plan"])
    def test_terminal_owner_agrees_with_the_transition_table(self, kind):
        """`terminal` is not a separate opinion: it must be exactly the set of
        states from which `_legal_transitions` offers nothing."""
        table = (planner.PROPOSAL_TRANSITIONS if kind == "proposal"
                 else planner.PLAN_TRANSITIONS)
        states = (planner.PROPOSAL_STATES if kind == "proposal"
                  else planner.PLAN_STATES)
        for state in states:
            terminal_by_owner = (
                planner.next_owner(kind, state) == planner.NEXT_OWNER_TERMINAL)
            terminal_by_table = not table.get(state, ())
            assert terminal_by_owner == terminal_by_table, state

    def test_an_unknown_or_absent_status_fails_closed_to_unknown(self):
        assert planner.next_owner("plan", "not-a-state") == \
            planner.NEXT_OWNER_UNKNOWN
        assert planner.next_owner("plan", "") == planner.NEXT_OWNER_UNKNOWN
        assert planner.next_owner("proposal", "") == planner.NEXT_OWNER_UNKNOWN

    def test_the_legacy_multi_successor_tokens_report_unresolved(self):
        """R7 maps `reviewed`, `revised` and `review` to more than one successor
        state whose owners differ, so the board says so instead of guessing --
        the same refusal B1 requires for `status`."""
        assert planner.next_owner("proposal", "reviewed") == \
            planner.NEXT_OWNER_UNRESOLVED
        assert planner.next_owner("proposal", "revised") == \
            planner.NEXT_OWNER_UNRESOLVED
        assert planner.next_owner("plan", "review") == \
            planner.NEXT_OWNER_UNRESOLVED

    def test_the_retained_historical_owner_rows_are_not_dead_weight(self):
        """The other three retained rows, which nothing else visits.

        Code review [C2]: after H1 retired the six tokens, `TestOwnerVocabulary`'s
        general coverage iterates the CURRENT tuples, so it stops visiting the
        historical rows entirely. The sibling node above pins `reviewed`,
        `revised` and `review` because they resolve to `unresolved`; these three
        resolve to a REAL owner and were pinned by nothing at all -- deleting
        them as dead weight passed the whole suite.

        Why they must stay ([C3] corrected the reason): not for archived
        artifacts -- none declares a historical token, and the archive tree is
        unreachable from `next_owner`'s only call site -- but for an artifact
        still ACTIVE on a retired token, mid-migration or hand-copied from an
        old record. That is exactly when an operator needs the board to say
        whose move it is, and without these rows it answers `unknown`.
        """
        assert planner.next_owner("proposal", "proposed") == "proposal-reviewer"
        assert planner.next_owner("plan", "open") == "plan-reviewer"
        assert planner.next_owner("plan", "executing") == "implementation"
        # ...and every one is a member of the closed owner vocabulary, so none
        # of them can be filterable in one place and unknown in the other.
        for kind, state in (("proposal", "proposed"), ("plan", "open"),
                            ("plan", "executing")):
            owner = planner.next_owner(kind, state)
            assert owner in planner.NEXT_OWNERS, (kind, state, owner)
            assert owner != planner.NEXT_OWNER_UNKNOWN, (kind, state)

    @pytest.mark.parametrize("kind,state", [
        ("proposal", state) for state in ("awaiting-review", "revising",
                                         "awaiting-decision", "accepted")
    ] + [
        ("plan", state) for state in ("awaiting-plan-review", "revising-plan",
                                      "ready-to-implement", "implementing",
                                      "awaiting-code-review", "revising-code",
                                      "ready-to-archive", "archived")
    ])
    def test_the_rendered_row_owner_matches_the_central_table(
            self, tmp_path, monkeypatch, capsys, kind, state):
        repo = _make_repo(tmp_path, name=f"repo-{kind}-{state}")
        if kind == "proposal":
            _write_proposal(repo, "art", status=state)
        else:
            _write_plan(repo, "art", status=state)
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        row = _cells(out)[0]
        assert row["status"] == state
        assert row["owner"] == planner.next_owner(kind, state)


class TestReviewAndEvidenceSummaries:

    def test_a_multi_obligation_plan_reports_its_obligation_count(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "multi", status="implementing",
                    plan_review="required(External + External Security Review)",
                    body=_pass_block("Plan review", tier="External",
                                     obligation="External")
                    + _pass_block("Plan review", reviewer="Reviewer B",
                                  date="2026-05-03", tier="External",
                                  obligation="External Security Review"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["review"] == "required(2)/clear"

    def test_an_unsatisfied_floor_reports_flagged_not_clear(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "unmet", status="implementing",
                    plan_review="required(External + External Security Review)",
                    body=_pass_block("Plan review", tier="External",
                                     obligation="External"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["review"] == "required(2)/flagged"

    def test_a_not_required_plan_says_so_rather_than_clear(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "nr", status="implementing",
                    plan_review="not required(doc-only)")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["review"] == "not-required"

    def test_a_proposal_reports_its_latest_review_tier_and_findings(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_proposal(repo, "prop", status="awaiting-decision",
                        body=_pass_block("Review", tier="External"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["review"] == "External/none"

    def test_a_proposal_with_no_review_record_says_no_review(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_proposal(repo, "prop", status="awaiting-review")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["review"] == "no-review"

    def test_boundary_b_and_a_blocking_code_review_both_appear(
            self, tmp_path, monkeypatch, capsys):
        """B1: *"The board does not compress a blocking finding into a clearing
        verdict."*  The verdict class is read through the shared
        `_parse_verdict`, so `blocking` reaches the row verbatim."""
        repo = _make_repo(tmp_path)
        _write_plan(
            repo, "blocked", status="awaiting-code-review",
            body=_pass_block("Plan review")
            + "\n## Implementation verification -- Agent -- 2026-05-04\n\nx\n"
            + "\n## Code review -- Reviewer C -- 2026-05-05\n\n"
            + "**Model**: test\n**Findings**: raised\n**Verdict**: REVISE\n"
            + _BASIS + "\nbody\n")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        evidence = _cells(out)[0]["evidence"]
        assert "bnd=2026-05-04" in evidence
        assert "cr=blocking@2026-05-05" in evidence
        assert "clearing" not in evidence

    def test_a_clearing_code_review_reads_clearing(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(
            repo, "clear", status="awaiting-code-review",
            body=_pass_block("Plan review")
            + "\n## Code review -- Reviewer C -- 2026-05-05\n\n"
            + "**Model**: test\n**Findings**: none\n**Verdict**: SHIP\n"
            + _BASIS + "\nbody\n")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert "cr=clearing@2026-05-05" in _cells(out)[0]["evidence"]

    def test_closeout_state_is_reported_for_plans(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert "close=unmet" in _cells(out)[0]["evidence"]


class TestBlockedByHasNoAuthority:
    """R4: the field *"never changes the legal state machine and never
    substitutes for status"*.  The board displays it and nothing more."""

    def test_the_exact_value_is_displayed(self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing",
                    blocked_by="the 2026-06 release ceremony")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["blocked_by"] == "the 2026-06 release ceremony"

    def test_absent_is_a_dash_not_a_state(self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["blocked_by"] == planner.BOARD_ABSENT

    def test_a_blocker_changes_neither_status_nor_owner_nor_validity(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "free", status="implementing")
        _write_plan(repo, "held", status="implementing", blocked_by="a release")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        free, held = _cells(out)
        for field in ("status", "owner", "validity", "review"):
            assert free[field] == held[field], field

    def test_a_duplicated_blocker_reads_ambiguous_and_reddens_validity(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        path = _write_plan(repo, "p", status="implementing", blocked_by="one",
                           body=_pass_block("Plan review"))
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "**Blocked by**: one\n",
                "**Blocked by**: one\n**Blocked by**: two\n"),
            encoding="utf-8")
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        row = _cells(out)[0]
        assert row["blocked_by"] == "ambiguous"
        assert row["validity"] == "blocked-by"
        assert status == 1


# =============================================================================
# B1 / B3 -- validity, visibility, and exit status
# =============================================================================


_R6_CONTRADICTIONS = {
    "proposal-revising-with-clearing-review": (
        "proposal", "revising", lambda: _pass_block("Review")),
    "proposal-awaiting-decision-with-raised": (
        "proposal", "awaiting-decision",
        lambda: _pass_block("Review", findings="raised")
        + "\n## Response -- Author A -- 2026-05-03\n\nx\n"),
    "plan-implementing-without-a-cleared-floor": (
        "plan", "implementing", lambda: ""),
    "plan-archived-without-a-code-review": (
        "plan", "archived", lambda: _pass_block("Plan review")),
    "plan-ready-to-archive-without-closeout": (
        "plan", "ready-to-archive",
        lambda: _pass_block("Plan review")
        + "\n## Code review -- Reviewer C -- 2026-05-05\n\n"
        + "**Model**: test\n**Findings**: none\n**Verdict**: SHIP\n"
        + _BASIS + "\nbody\n"),
}


class TestOneReasonThroughEverySurface:
    """B7: *"every R6 contradiction producing the same stable reason through
    `scan`, `next`, compact board, and JSON"*."""

    @pytest.mark.parametrize("case", sorted(_R6_CONTRADICTIONS))
    def test_the_same_predicate_speaks_on_all_four_surfaces(
            self, tmp_path, monkeypatch, capsys, case):
        kind, state, body = _R6_CONTRADICTIONS[case]
        repo = _make_repo(tmp_path, name=f"repo-{case}")
        if kind == "proposal":
            _write_proposal(repo, "art", status=state, body=body())
        else:
            _write_plan(repo, "art", status=state, body=body())
        _commit_all(repo)

        monkeypatch.chdir(repo)
        art = planner._read_artifact(
            repo / "dev" / ("proposals" if kind == "proposal" else "plans")
            / "art.md")
        identity = planner._load_identity_model(repo)
        expected = planner.status_evidence_violations(art, state)
        assert expected, "the fixture must actually be contradictory"

        status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["validity"] == "status-evidence"
        assert status == 1

        status, out, _err = _board(monkeypatch, repo, capsys,
                                   ["board", "--format", "json"])
        payload = json.loads(out)
        assert payload["rows"][0]["validity"] == "status-evidence"
        assert payload["invalid_count"] == 1
        assert status == 1

        _status, out, _err = _board(monkeypatch, repo, capsys,
                                    ["board", "--explain", "art"])
        for message in expected:
            assert planner.encode_display(message) in out

        scan_status = planner.main(["scan"])
        scan_out = capsys.readouterr().out
        assert scan_status == 1
        for message in expected:
            assert message in scan_out
        assert planner._conformance_violations(art, identity)


class TestMalformedRecordsStayVisible:

    def test_an_unknown_status_is_visible_with_non_zero_exit(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "weird", status="not-a-real-state")
        _write_plan(repo, "sound", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        cells = {row["artifact"]: row for row in _cells(out)}
        assert cells["weird"]["status"] == "not-a-real-state"
        assert cells["weird"]["validity"] == "status-vocabulary"
        assert cells["weird"]["owner"] == planner.NEXT_OWNER_UNKNOWN
        assert cells["sound"]["validity"] == planner.BOARD_VALID, (
            "one malformed record must not hide the rest of the board")
        assert status == 1

    def test_a_status_less_proposal_is_status_vocabulary_not_valid(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        (repo / "dev" / "proposals" / "bare.md").write_text(
            "# bare\n\n**Author**: Author A (Strategy)\n\n## Context\n\nx\n",
            encoding="utf-8")
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        row = _cells(out)[0]
        assert row["status"] == planner.BOARD_ABSENT
        assert row["validity"] == "status-vocabulary"
        assert status == 1

    def test_a_reason_code_is_always_from_the_closed_set(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_proposal(repo, "no-assurance", status="awaiting-review",
                        assurance=None)
        _write_plan(repo, "no-floor", status="implementing",
                    plan_review="")
        _write_plan(repo, "ok", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        cells = {row["artifact"]: row for row in _cells(out)}
        for row in cells.values():
            assert row["validity"] in planner.BOARD_REASON_CODES, row
        assert cells["no-assurance"]["validity"] == "declaration"
        assert cells["no-floor"]["validity"] == "review-floor"

    def test_the_classifier_falls_back_to_other_never_to_valid(
            self, tmp_path, monkeypatch):
        """The drift guard on the classifier.  `_conformance_violations` alone
        decides whether a row is invalid, so a predicate this table does not know
        about must land on `other` -- if it could reach `valid`, a future
        conformance rule would be silently invisible on the board."""
        repo = _make_repo(tmp_path)
        path = _write_plan(repo, "p", status="implementing",
                           body=_pass_block("Plan review"))
        monkeypatch.chdir(repo)
        art = planner._read_artifact(path)
        identity = planner._load_identity_model(repo)
        assert planner._board_validity(art, identity)[0] == planner.BOARD_VALID
        monkeypatch.setattr(
            planner, "_conformance_violations",
            lambda _art, _identity: ["a rule invented after Chunk F"])
        code, violations = planner._board_validity(art, identity)
        assert code == "other"
        assert violations == ["a rule invented after Chunk F"]

    def test_an_unreadable_artifact_still_occupies_a_row(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "sound", status="implementing",
                    body=_pass_block("Plan review"))
        (repo / "dev" / "plans" / "broken.md").write_bytes(b"\xff\xfe\x00bad")
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        cells = {row["artifact"]: row for row in _cells(out)}
        assert cells["broken"]["validity"] == "unreadable"
        assert cells["sound"]["validity"] == planner.BOARD_VALID
        assert status == 1


# =============================================================================
# B1 -- source labels; B3 -- bounded git, no writes, no cache
# =============================================================================


class TestSourceLabels:

    def test_a_clean_artifact_is_labelled_head(self, tmp_path, monkeypatch,
                                               capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["source"] == planner.BOARD_SOURCE_HEAD

    def test_a_modified_artifact_is_labelled_dirty(self, tmp_path, monkeypatch,
                                                   capsys):
        repo = _make_repo(tmp_path)
        path = _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        path.write_text(path.read_text(encoding="utf-8") + "\nedited\n",
                        encoding="utf-8")
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["source"] == planner.BOARD_SOURCE_DIRTY
        assert "lifecycle files differ from HEAD: yes" in out

    def test_an_untracked_artifact_is_labelled_untracked(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "tracked", status="implementing")
        _commit_all(repo)
        _write_plan(repo, "fresh", status="implementing")
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        cells = {row["artifact"]: row for row in _cells(out)}
        assert cells["fresh"]["source"] == planner.BOARD_SOURCE_UNTRACKED
        assert cells["tracked"]["source"] == planner.BOARD_SOURCE_HEAD

    def test_git_unavailable_is_unbound_never_head(
            self, tmp_path, monkeypatch, capsys):
        """B4: *"it does not silently label working-tree content as HEAD"*.  An
        unborn HEAD is the reachable case -- a repository with no commit."""
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing")
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["source"] == planner.BOARD_SOURCE_UNBOUND
        assert "UNBOUND" in out
        assert planner.BOARD_SOURCE_HEAD not in _cells(out)[0]["source"]

    def test_every_emitted_source_label_is_from_the_closed_set(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "a", status="implementing")
        _commit_all(repo)
        _write_plan(repo, "b", status="implementing")
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        for row in _cells(out):
            assert row["source"] in planner.BOARD_SOURCES


class TestReadOnlyBoundedAndUncached:

    @staticmethod
    def _tree(repo: Path) -> dict:
        state = {}
        for path in sorted(repo.rglob("*")):
            if ".git" in path.parts or not path.is_file():
                continue
            state[str(path.relative_to(repo))] = hashlib.sha256(
                path.read_bytes()).hexdigest()
        return state

    @staticmethod
    def _porcelain(repo: Path) -> str:
        return subprocess.run(["git", "status", "--porcelain"], cwd=str(repo),
                              capture_output=True, text=True,
                              check=True).stdout

    @pytest.mark.parametrize("argv", [
        ["board"], ["board", "--compact"], ["board", "--format", "json"],
        ["board", "--invalid-only"], ["board", "--explain", "p"],
    ])
    def test_no_repository_mutation(self, tmp_path, monkeypatch, capsys, argv):
        repo = _make_repo(tmp_path, name="repo-" + "-".join(argv))
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        before_tree, before_status = self._tree(repo), self._porcelain(repo)
        _board(monkeypatch, repo, capsys, argv)
        assert self._tree(repo) == before_tree
        assert self._porcelain(repo) == before_status

    def test_an_edit_is_reflected_immediately_with_no_cache(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        path = _write_plan(repo, "p", status="implementing",
                           body=_pass_block("Plan review"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["status"] == "implementing"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "**Status**: implementing", "**Status**: awaiting-code-review"),
            encoding="utf-8")
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert _cells(out)[0]["status"] == "awaiting-code-review"

    def test_git_invocation_count_does_not_grow_with_rows(
            self, tmp_path, monkeypatch, capsys):
        """B3: *"Repository state is obtained in a bounded batch, not through one
        Git subprocess per row."*  Two fixture repos differing only in row count
        must cost the same number of git invocations."""
        counts = {}
        for name, rows in (("small", 2), ("large", 8)):
            repo = _make_repo(tmp_path, name=f"repo-{name}")
            for index in range(rows):
                _write_plan(repo, f"p{index}", status="implementing")
            _commit_all(repo)
            calls = []
            real = subprocess.run

            def counting(args, *rest, **kwargs):
                calls.append(list(args))
                return real(args, *rest, **kwargs)

            monkeypatch.setattr(planner.subprocess, "run", counting)
            _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
            monkeypatch.undo()
            assert len(_rows(out)) == rows
            counts[name] = sum(1 for call in calls
                               if Path(call[0]).name.startswith("git"))
        assert counts["small"] == counts["large"], counts
        assert counts["small"] <= 4, counts


# =============================================================================
# B2 -- filters, JSON contract, focused inspection
# =============================================================================


class TestFiltersAndJson:

    def test_exact_status_filter(self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "a", status="implementing")
        _write_plan(repo, "b", status="awaiting-plan-review")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys,
                                    ["board", "--status", "implementing"])
        assert [row["artifact"] for row in _cells(out)] == ["a"]

    def test_exact_owner_filter(self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "a", status="implementing")
        _write_plan(repo, "b", status="awaiting-plan-review")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys,
                                    ["board", "--owner", "plan-reviewer"])
        assert [row["artifact"] for row in _cells(out)] == ["b"]

    def test_invalid_only_filter(self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "sound", status="implementing",
                    body=_pass_block("Plan review"))
        _write_plan(repo, "broken", status="not-a-state")
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys,
                                   ["board", "--invalid-only"])
        assert [row["artifact"] for row in _cells(out)] == ["broken"]
        assert status == 1

    @pytest.mark.parametrize("argv", [
        ["board", "--status", "not-a-state"],
        ["board", "--owner", "nobody"],
        ["board", "--compact", "--format", "json"],
    ])
    def test_unknown_filter_values_fail_closed_with_usage_error(
            self, tmp_path, monkeypatch, capsys, argv):
        """B2: *"Unknown filter values fail closed with usage error."*  Never an
        empty board, which would read as "nothing matches"."""
        repo = _make_repo(tmp_path, name="repo-" + argv[1].strip("-"))
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        status, out, err = _board(monkeypatch, repo, capsys, argv)
        assert status == 2
        assert "USAGE ERROR" in err
        assert _rows(out) == []

    def test_json_carries_the_versioned_schema_and_full_values(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing",
                    blocked_by="a durable condition",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys,
                                    ["board", "--format", "json"])
        payload = json.loads(out)
        assert payload["schema"] == planner.BOARD_SCHEMA_VERSION
        assert payload["schema"] == "cairn-lifecycle-board/1"
        assert payload["fields"] == list(planner.BOARD_FIELDS)
        assert len(payload["head"]) == 40
        assert payload["rows"][0]["blocked_by"] == "a durable condition"
        assert set(payload["rows"][0]) == set(planner.BOARD_FIELDS)

    def test_json_is_deterministic_and_ascii_safe(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing",
                    blocked_by="caf\u00e9 \u4e2d\u6587 \u200b")
        _commit_all(repo)
        first = _board(monkeypatch, repo, capsys, ["board", "--format", "json"])[1]
        second = _board(monkeypatch, repo, capsys,
                        ["board", "--format", "json"])[1]
        assert first == second
        assert first.isascii(), "ensure_ascii=True must hold for the payload"
        # The full value survives in JSON (B2), escaped by the stdlib encoder --
        # the terminal encoder governs the compact projection, not this one.
        assert json.loads(first)["rows"][0]["blocked_by"] == \
            "caf\u00e9 \u4e2d\u6587 \u200b"

    def test_explain_expands_one_row_and_cites_headings_not_bodies(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review")
                    .replace("body\n", "SECRET-REVIEW-BODY-TEXT\n"))
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys,
                                   ["board", "--explain", "p"])
        assert status == 0
        assert "Plan review -- Reviewer A -- 2026-05-02" in out
        assert "SECRET-REVIEW-BODY-TEXT" not in out
        assert "unmet predicates per legal next transition" in out

    def test_explain_refuses_an_absent_stem(self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        status, _out, err = _board(monkeypatch, repo, capsys,
                                   ["board", "--explain", "q"])
        assert status == 1
        assert "refuses to select the nearest name" in err

    def test_explain_refuses_an_ambiguous_stem(self, tmp_path, monkeypatch,
                                               capsys):
        repo = _make_repo(tmp_path)
        _write_proposal(repo, "same", status="awaiting-review")
        _write_plan(repo, "same", status="implementing")
        _commit_all(repo)
        status, _out, err = _board(monkeypatch, repo, capsys,
                                   ["board", "--explain", "same"])
        assert status == 1
        assert "ambiguous" in err


# =============================================================================
# B4 (Revision 4) -- the terminal encoder, and B7's DIRECTIONAL drift oracle
# =============================================================================


def _scanner_display_unsafe_population() -> set[str]:
    """Expand **every** member and **every code point** of the reviewed
    content-scan inventory.

    Revision 4's B7: *"It imports the Cairn content scanner in the test
    environment, expands every member of the three sets, every code point in
    `_IGNORABLE_RANGES` and `_NONCHARACTER_RANGES`, the complete `_TAG_RANGE`,
    and `_ASCII_GUARD`."*  Not a hand-copied sample: the sets are read from the
    scanner, so a member added there enters this population automatically.
    """
    population: set[str] = set()
    population |= set(scan._ZERO_WIDTH)
    population |= set(scan._BIDI)
    population |= set(scan._LINE_SEPARATORS)
    for low, high in tuple(scan._IGNORABLE_RANGES) + tuple(
            scan._NONCHARACTER_RANGES):
        population |= {chr(code) for code in range(low, high + 1)}
    low, high = scan._TAG_RANGE
    population |= {chr(code) for code in range(low, high + 1)}
    population.add(scan._ASCII_GUARD)
    return population


class TestDirectionalDriftGuard:
    """The one-way coupling, stated as an assertion:

        expanded content-scan display-unsafe population <= board escaped population

    The board may escape more than the scanner flags.  It may never emit raw a
    code point the scanner recognizes.  So a newly added printable invisible
    reddens this class until `_DISPLAY_UNSAFE_RANGES` follows it, and narrowing a
    detector cannot silently weaken terminal output.
    """

    def test_the_population_under_test_is_not_a_token_sample(self):
        """A guard on the guard.  [F1] was raised because a three-set population
        *could not contain* its own counterexamples; if this population ever
        shrinks to a handful, the subset assertion below goes quietly green."""
        population = _scanner_display_unsafe_population()
        assert len(population) > 4000, (
            f"the expanded scanner population is only {len(population)} code "
            "points -- it must expand every range, not sample them")
        # The rows that make it big are the ones a category sweep misses.
        assert chr(0xE0041) in population, "the Tag block must be expanded"
        assert chr(0xFDD0) in population, "noncharacters must be expanded"
        assert chr(0x034F) in population, "the Mn residual must be present"

    def test_every_scanner_recognized_code_point_is_escaped(self):
        survivors = [
            char for char in sorted(_scanner_display_unsafe_population())
            if planner.encode_display(char) == char
        ]
        assert survivors == [], (
            f"{len(survivors)} scanner-recognized code point(s) survive raw "
            f"through the board encoder, first={survivors[:5]!r}")

    def test_the_range_table_covers_the_scanner_population_by_code_point(self):
        """The subset assertion at the *table* level, not only through the
        encoder: clause 2 must carry the population on its own, so a future
        change to clause 1 cannot silently become the only thing holding it."""
        uncovered = [
            char for char in sorted(_scanner_display_unsafe_population())
            if not planner._display_unsafe_code_point(ord(char))
        ]
        assert uncovered == [], (
            f"{len(uncovered)} scanner code point(s) are outside "
            f"_DISPLAY_UNSAFE_RANGES, first={uncovered[:5]!r}")

    def test_neither_planner_source_embeds_a_represented_invisible_raw(self):
        """*"The range form uses numeric endpoints only; no invisible source
        character is embedded raw."*  A table written with literal members would
        make the planner carry the very code points it exists to escape."""
        population = _scanner_display_unsafe_population()
        for path in (_PLANNER_SOURCE, _PLANNER_TEMPLATE):
            text = path.read_text(encoding="utf-8")
            present = sorted({char for char in population if char in text})
            assert present == [], (
                f"{path} embeds {len(present)} represented invisible(s) raw, "
                f"first={present[:5]!r}")

    def test_this_test_module_embeds_none_either(self):
        """The same property for the oracle, so the file that proves the planner
        clean is not itself a Trojan-source carrier."""
        population = _scanner_display_unsafe_population()
        text = Path(__file__).read_text(encoding="utf-8")
        assert sorted({char for char in population if char in text}) == []


class TestEncoderRule:

    def test_every_non_printable_code_point_is_escaped(self):
        """Revision 4's independent sweep: *"every code point for which
        `str.isprintable()` is false is escaped"* -- the whole space, not a
        sample, because clause 1 is the half that must not have holes."""
        survivors = []
        for code in range(0x110000):
            char = chr(code)
            if char.isprintable():
                continue
            if planner.encode_display(char) == char:
                survivors.append(code)
                if len(survivors) > 5:
                    break
        assert survivors == [], [hex(code) for code in survivors]

    @pytest.mark.parametrize("code,label", [
        (0x1B, "ANSI ESC"),
        (0x00A0, "NBSP"),
        (0x3000, "ideographic space"),
        (0x034F, "combining grapheme joiner"),
        (0x115F, "Hangul choseong filler"),
        (0x1160, "Hangul jungseong filler"),
        (0x3164, "Hangul filler"),
        (0xFE0F, "variation selector-16"),
        (0xE0041, "Tag block letter A"),
        (0xFDD0, "noncharacter"),
        (0x10FFFF, "plane-16 noncharacter"),
        (0x200B, "zero-width space"),
        (0x202E, "right-to-left override"),
        (0x2028, "line separator"),
    ])
    def test_focused_probe_is_escaped(self, code, label):
        char = chr(code)
        encoded = planner.encode_display(char)
        assert encoded != char, label
        assert encoded.isascii() and encoded.isprintable(), (label, encoded)
        assert "\x1b" not in encoded, "ANSI ESC must never survive"

    def test_both_ends_of_every_mirrored_range_are_escaped(self):
        for low, high in planner._DISPLAY_UNSAFE_RANGES:
            for code in (low, high):
                char = chr(code)
                assert planner.encode_display(char) != char, hex(code)

    def test_the_delimiters_and_backslash_are_escaped(self):
        """Clause 3.  A field value cannot add a column or a row."""
        for char in (planner._BOARD_FIELD_DELIMITER,
                     planner._BOARD_ROW_DELIMITER, "\\", "\r", "\t"):
            assert planner.encode_display(char) != char, repr(char)
            assert planner._BOARD_FIELD_DELIMITER not in \
                planner.encode_display(char)

    @pytest.mark.parametrize("value", [
        "ordinary ascii text",
        "Schr\u00f6dinger", "caf\u00e9", "\u03b1\u03b2\u03b3",
        "\u4e2d\u6587", "Na\u00efve r\u00e9sum\u00e9", "a b  c",
    ])
    def test_ordinary_printable_scientific_text_is_untouched(self, value):
        """*"Ordinary printable scientific text remains readable, including ASCII
        space, precomposed accented letters, Greek, and CJK."*"""
        assert planner.encode_display(value) == value

    def test_the_escape_is_a_printable_ascii_code_point_form(self):
        assert planner.encode_display("\x1b") == "\\x1b"
        assert planner.encode_display("\u200b") == "\\u200b"
        assert planner.encode_display(chr(0xE0041)) == "\\U000e0041"

    def test_the_floor_is_derived_from_the_table_not_a_literal(self):
        assert planner._DISPLAY_UNSAFE_FLOOR == min(
            low for low, _high in planner._DISPLAY_UNSAFE_RANGES)
        assert planner._DISPLAY_UNSAFE_FLOOR == ord(scan._ASCII_GUARD)


class TestInjectionThroughEveryCompactFieldPosition:

    def test_the_whole_scanner_population_cannot_escape_one_field(
            self, tmp_path, monkeypatch, capsys):
        """The end-to-end form of the directional guard: stuff **every** expanded
        code point into one free-text field, render the compact board, and
        require that the entire output is printable ASCII with exactly the
        expected row and column count."""
        population = "".join(sorted(_scanner_display_unsafe_population()))
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing", blocked_by=population)
        _write_plan(repo, "q", status="implementing")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        for char in out:
            assert char == "\n" or (0x20 <= ord(char) <= 0x7E), (
                f"raw {hex(ord(char))} reached the terminal")
        rows = _rows(out)
        assert len(rows) == 2, "an injected code point added or removed a row"
        for row in rows:
            assert len(row) == len(planner.BOARD_FIELDS)

    @pytest.mark.parametrize("payload,label", [
        ("\x1b[31mRED\x1b[0m", "ansi"),
        ("a\u202eb", "bidi override"),
        ("a\u200bb", "zero width"),
        ("a|b", "field delimiter"),
        ("a\nb", "row delimiter"),
        ("a\\b", "backslash"),
        ("a\u2028b", "line separator"),
    ])
    def test_injection_through_the_status_field(
            self, tmp_path, monkeypatch, capsys, payload, label):
        repo = _make_repo(tmp_path, name=f"repo-status-{label}".replace(" ", "-"))
        _write_plan(repo, "p", status=f"implementing{payload}")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert len(_rows(out)) == 1, label
        assert len(_rows(out)[0]) == len(planner.BOARD_FIELDS), label
        assert "\x1b" not in out and "\u202e" not in out and "\u200b" not in out

    @pytest.mark.parametrize("payload,label", [
        ("\x1b[31m", "ansi"), ("a|b", "delimiter"), ("a\u200bb", "zero width"),
    ])
    def test_injection_through_the_blocked_by_field(
            self, tmp_path, monkeypatch, capsys, payload, label):
        repo = _make_repo(tmp_path, name=f"repo-blocked-{label}".replace(" ", "-"))
        _write_plan(repo, "p", status="implementing", blocked_by=payload)
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert len(_rows(out)) == 1
        assert len(_rows(out)[0]) == len(planner.BOARD_FIELDS)
        assert "\x1b" not in out and "\u200b" not in out

    def test_injection_through_the_artifact_filename(
            self, tmp_path, monkeypatch, capsys):
        """The `artifact` field is a filename, which is attacker-adjacent in a
        shared checkout.  `|` is legal in a POSIX filename."""
        repo = _make_repo(tmp_path)
        (repo / "dev" / "plans" / "we|ird.md").write_text(
            "# x\n\n**Status**: implementing\n**Plan review**: "
            "not required(x)\n\n## Scope\n\nx\n", encoding="utf-8")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        rows = _rows(out)
        assert len(rows) == 1
        assert len(rows[0]) == len(planner.BOARD_FIELDS)
        assert rows[0][1] == "we\\x7cird"

    def test_the_closed_vocabulary_fields_are_always_ascii_printable(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing\u200b")
        _write_proposal(repo, "q", status="awaiting-review")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        for row in _cells(out):
            for field in ("kind", "owner", "validity", "source"):
                assert row[field].isascii() and row[field].isprintable(), field


# =============================================================================
# B3 (Revision 3 addition) -- the optional work-intent provider
# =============================================================================


#: The stub provider.  It records what the **child** actually saw -- its own
#: `sys.orig_argv` and interpreter flags -- so "invoked in isolated mode with a
#: fixed argv" is proven by the process itself rather than by inspecting the
#: caller's keyword arguments.
_STUB = '''\
import json
import sys

with open({record!r}, "a", encoding="utf-8") as handle:
    handle.write(json.dumps({{
        "argv": list(sys.orig_argv),
        "isolated": bool(sys.flags.isolated),
        "no_user_site": bool(sys.flags.no_user_site),
        "cwd_in_path": "" in sys.path or "." in sys.path,
    }}) + "\\n")
{extra}
sys.stdout.write({payload!r})
sys.exit({exit_code})
'''


def _provider_repo(tmp_path, name: str, *, payload: str = "",
                   exit_code: int = 0, extra: str = "",
                   launcher: str = "file") -> tuple[Path, Path, ModuleType]:
    """A fixture repo whose `tools/` holds a REAL planner copy + a stub launcher.

    Loading the planner from the temp directory is what makes the containment
    guards observable: the launcher path is derived from the planner's own
    ``__file__``, so the expected `tools/` directory is this temp one.
    """
    repo = _make_repo(tmp_path, name=name)
    tools = repo / "tools"
    tools.mkdir()
    planner_copy = tools / "lifecycle_planner.py"
    shutil.copy2(_PLANNER_TEMPLATE, planner_copy)
    record = repo / "provider-calls.jsonl"
    target = tools / "intent.py"
    if launcher == "file":
        target.write_text(
            _STUB.format(record=str(record), payload=payload,
                         exit_code=exit_code, extra=extra),
            encoding="utf-8")
    elif launcher == "symlink":
        real = repo / "outside-intent.py"
        real.write_text(
            _STUB.format(record=str(record), payload=payload,
                         exit_code=exit_code, extra=extra),
            encoding="utf-8")
        target.symlink_to(real)
    elif launcher == "symlink-in-directory":
        real = tools / "real-intent.py"
        real.write_text(
            _STUB.format(record=str(record), payload=payload,
                         exit_code=exit_code, extra=extra),
            encoding="utf-8")
        target.symlink_to(real)
    elif launcher == "broken-symlink":
        target.symlink_to(repo / "does-not-exist.py")
    elif launcher == "directory":
        target.mkdir()
    elif launcher == "absent":
        pass
    else:  # pragma: no cover - fixture guard
        raise AssertionError(launcher)
    module = _load(planner_copy, f"cairn_board_provider_{name}")
    return repo, record, module


def _payload(claims: list[dict], schema: str = "cairn-intent-list/1") -> str:
    return json.dumps({"schema": schema, "claims": claims})


def _claim(claim_id: str, files: list[str], agent: str = "agent-one",
           action: str = "editing", ts: str = "2026-05-05T10:00:00-04:00",
           **extra) -> dict:
    record = {"id": claim_id, "agent": agent, "ts": ts, "action": action,
              "stem": "", "files": files}
    record.update(extra)
    return record


class TestProviderInvocation:

    def test_exactly_one_subprocess_per_board_whatever_the_row_count(
            self, tmp_path, monkeypatch, capsys):
        """B3: *"The board obtains all active claims in one bounded query, not one
        subprocess per row."*"""
        repo, record, module = _provider_repo(
            tmp_path, "one-call", payload=_payload([]))
        for index in range(6):
            _write_plan(repo, f"p{index}", status="implementing")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert len(_rows(out)) == 6
        lines = [line for line in record.read_text(encoding="utf-8").splitlines()
                 if line.strip()]
        assert len(lines) == 1, f"{len(lines)} provider invocations for 6 rows"

    def test_explain_also_costs_exactly_one_query(
            self, tmp_path, monkeypatch, capsys):
        repo, record, module = _provider_repo(
            tmp_path, "explain-one-call", payload=_payload([]))
        _write_plan(repo, "p", status="implementing")
        _write_plan(repo, "q", status="implementing")
        _commit_all(repo)
        _board(monkeypatch, repo, capsys, ["board", "--explain", "p"], module)
        assert len([line for line in
                    record.read_text(encoding="utf-8").splitlines()
                    if line.strip()]) == 1

    def test_the_exact_argv_is_the_interpreter_isolated_mode_and_json(
            self, tmp_path, monkeypatch, capsys):
        """The full invocation clause: *"invokes it with the running interpreter
        in isolated mode"* and *"versioned JSON only, never scraped human
        output"*.  Read back from the child itself, not from a mock."""
        repo, record, module = _provider_repo(
            tmp_path, "argv", payload=_payload([]))
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        _board(monkeypatch, repo, capsys, ["board"], module)
        seen = json.loads(record.read_text(encoding="utf-8").splitlines()[0])
        launcher = str(repo / "tools" / "intent.py")
        assert seen["argv"] == [sys.executable, "-I", launcher, "list",
                                "--format", "json"]
        assert module._intent_argv(Path(launcher)) == seen["argv"]
        assert seen["isolated"] is True, "-I did not take effect in the child"
        assert seen["no_user_site"] is True
        assert seen["cwd_in_path"] is False, (
            "isolated mode must not put the working directory on sys.path")

    def test_no_shell_is_ever_used(self, tmp_path, monkeypatch, capsys):
        """Two independent proofs: the source never passes a truthy `shell`, and
        a shell metacharacter in the launcher path is not interpreted (the child
        still runs and reports its own argv)."""
        source = _PLANNER_TEMPLATE.read_text(encoding="utf-8")
        assert "shell=True" not in source
        assert "shell=False" in source
        repo, record, module = _provider_repo(
            tmp_path, "no-shell", payload=_payload([]))
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        captured = {}
        real = subprocess.run

        def watching(args, *rest, **kwargs):
            if "intent.py" in " ".join(str(part) for part in args):
                captured.update(kwargs)
                captured["args"] = list(args)
            return real(args, *rest, **kwargs)

        monkeypatch.setattr(module.subprocess, "run", watching)
        _board(monkeypatch, repo, capsys, ["board"], module)
        assert captured["shell"] is False
        assert isinstance(captured["args"], list), (
            "a list argv is what makes shell interpretation impossible")
        assert captured["timeout"] == module._INTENT_QUERY_TIMEOUT

    def test_the_timeout_is_enforced_by_a_real_slow_child(
            self, tmp_path, monkeypatch, capsys):
        repo, _record, module = _provider_repo(
            tmp_path, "timeout", payload=_payload([]),
            extra="import time\ntime.sleep(30)")
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        monkeypatch.setattr(module, "_INTENT_QUERY_TIMEOUT", 0.75)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        row = _cells(out)[0]
        assert row["active_intent"] == module.INTENT_ERROR
        assert "timeout" in out
        assert row["validity"] == module.BOARD_VALID, (
            "a provider failure must not hide or invalidate a lifecycle row")
        assert status == 1


class TestProviderContainment:

    def test_a_symlinked_launcher_is_refused_even_pointing_outside(
            self, tmp_path, monkeypatch, capsys):
        """A **real** symlink, not a monkeypatch: *"locates only a regular,
        non-symlinked `tools/intent.py` beside itself"*."""
        repo, record, module = _provider_repo(
            tmp_path, "symlink-out", payload=_payload([]), launcher="symlink")
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == module.INTENT_ERROR
        assert "launcher-symlink" in out
        assert status == 1
        assert not record.exists(), "a refused launcher must not be executed"

    def test_a_symlinked_launcher_is_refused_even_pointing_inside(
            self, tmp_path, monkeypatch, capsys):
        """The refusal is on the *link*, not on where it lands -- a symlink whose
        target is a sibling in the same directory is still refused, because
        `is_symlink` is the only check that sees a link at all."""
        repo, record, module = _provider_repo(
            tmp_path, "symlink-in", payload=_payload([]),
            launcher="symlink-in-directory")
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == module.INTENT_ERROR
        assert "launcher-symlink" in out
        assert not record.exists()

    def test_a_broken_symlink_is_an_error_not_not_installed(
            self, tmp_path, monkeypatch, capsys):
        """The ordering that matters: `is_symlink` runs before `exists`, so a
        planted broken link cannot launder itself into `not-installed` -- which
        would read as "the module simply is not here"."""
        repo, _record, module = _provider_repo(
            tmp_path, "broken-link", launcher="broken-symlink")
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == module.INTENT_ERROR
        assert "launcher-symlink" in out
        assert status == 1

    def test_a_non_regular_launcher_is_refused(self, tmp_path, monkeypatch,
                                               capsys):
        repo, _record, module = _provider_repo(
            tmp_path, "dir-launcher", launcher="directory")
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == module.INTENT_ERROR
        assert "launcher-not-regular" in out
        assert status == 1

    def test_a_symlinked_ancestor_is_not_a_false_refusal(
            self, tmp_path, monkeypatch, capsys):
        """The other direction, with a **real** directory symlink.  Containment
        compares RESOLVED forms precisely so that a symlinked ancestor -- macOS's
        `/tmp -> private/tmp` is the one every run of this suite crosses -- does
        not read as an out-of-directory launcher."""
        repo, record, module = _provider_repo(
            tmp_path, "real-tools", payload=_payload([]))
        link_root = tmp_path / "linked-root"
        link_root.symlink_to(repo, target_is_directory=True)
        linked_planner = link_root / "tools" / "lifecycle_planner.py"
        assert linked_planner.exists()
        assert not linked_planner.is_symlink(), (
            "the leaf must be reached through a symlinked ANCESTOR, not a "
            "symlinked leaf, or this proves the wrong thing")
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        through_link = _load(linked_planner, "cairn_board_via_symlinked_ancestor")
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"],
                                    through_link)
        assert _cells(out)[0]["active_intent"] == planner.BOARD_ABSENT
        assert "launcher-out-of-directory" not in out
        assert record.exists(), "the launcher should have been executed"

    def test_the_out_of_directory_arm_exists_and_refuses(
            self, tmp_path, monkeypatch, capsys):
        """The containment comparison, exercised directly.

        **Stated plainly rather than dressed up**: with the symlink refusal above
        in force, this arm is not independently reachable by a real filesystem
        construction -- a launcher that is not a symlink and whose parent chain
        resolves identically on both sides always lands inside the expected
        directory.  So the arm is asserted here by redirecting the resolution,
        which is an *observation* harness for an ordering property, not a
        substitute for the real-symlink proofs above.  It is kept because a
        future edit that removes the comparison should redden something."""
        repo, _record, module = _provider_repo(
            tmp_path, "out-of-dir", payload=_payload([]))
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        elsewhere = tmp_path / "elsewhere" / "intent.py"
        elsewhere.parent.mkdir(parents=True)
        elsewhere.write_text("x", encoding="utf-8")
        original = Path.resolve

        def redirect(self, *args, **kwargs):
            if self.name == "intent.py":
                return elsewhere
            return original(self, *args, **kwargs)

        monkeypatch.setattr(Path, "resolve", redirect)
        launcher, reason, detail = module._intent_launcher()
        assert launcher is None
        assert reason == "launcher-out-of-directory"
        assert "elsewhere" in detail

    def test_an_absent_launcher_is_not_installed_not_an_error(
            self, tmp_path, monkeypatch, capsys):
        repo, _record, module = _provider_repo(
            tmp_path, "absent", launcher="absent")
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == module.INTENT_NOT_INSTALLED
        assert "no claim is authoritative" in out
        assert status == 0, (
            "an absent optional module is not an error -- it is the documented "
            "default for an adopter without the coordination module")


class TestProviderFailureModesAreDistinct:
    """*"Timeout, non-zero exit, malformed JSON, duplicate claim ids, invalid
    paths, or a schema version mismatch are explicit provider errors."*  Each one
    gets its own reason code, and none of them may read as "no claim"."""

    CASES = {
        "nonzero-exit": {"payload": "", "exit_code": 3},
        "malformed-json": {"payload": "intent: no active intents.\n"},
        "schema-mismatch": {
            "payload": _payload([], schema="cairn-intent-list/2")},
        "duplicate-id": {"payload": _payload([
            _claim("dup", ["dev/plans/p.md"]),
            _claim("dup", ["dev/plans/q.md"], agent="agent-two")])},
        "invalid-path": {"payload": _payload([
            _claim("c1", ["../outside/p.md"])])},
        "invalid-record": {"payload": json.dumps({
            "schema": "cairn-intent-list/1",
            "claims": [{"id": "c1", "ts": "t", "action": "a",
                        "files": ["dev/plans/p.md"]}]})},
    }

    @pytest.mark.parametrize("reason", sorted(CASES))
    def test_each_mode_has_its_own_reason_code_and_keeps_rows_visible(
            self, tmp_path, monkeypatch, capsys, reason):
        repo, _record, module = _provider_repo(
            tmp_path, f"fail-{reason}", **self.CASES[reason])
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _write_plan(repo, "q", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        rows = _cells(out)
        assert len(rows) == 2, "a provider failure must not remove a row"
        for row in rows:
            assert row["active_intent"] == module.INTENT_ERROR
            assert row["active_intent"] != module.BOARD_ABSENT
            assert row["validity"] == module.BOARD_VALID
        assert reason in out, f"the {reason!r} reason code must be reported"
        assert reason in module.INTENT_REASON_CODES
        assert status == 1, "a broken provider exits non-zero"

    def test_the_human_list_form_is_never_scraped(
            self, tmp_path, monkeypatch, capsys):
        """The `malformed-json` case is the proof: the stub emits exactly what
        `intent list` prints for a real claim, and the board refuses it rather
        than extracting an id from it."""
        human = ("id='claude-x'\n  agent='claude-x'\n  ts='2026-05-05'\n"
                 "  files=['dev/plans/p.md']\n  action='editing'\n")
        repo, _record, module = _provider_repo(
            tmp_path, "no-scrape", payload=human)
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == module.INTENT_ERROR
        assert "malformed-json" in out
        assert "claude-x" not in out
        assert status == 1

    def test_validation_is_all_or_nothing_across_records(
            self, tmp_path, monkeypatch, capsys):
        """*"Complete field, type and path validation of every record before any
        is used."*  A valid record sharing a payload with an invalid one must not
        be rendered authoritative."""
        payload = _payload([
            _claim("good", ["dev/plans/p.md"], agent="agent-good"),
            _claim("bad", ["/etc/passwd"], agent="agent-bad"),
        ])
        repo, _record, module = _provider_repo(
            tmp_path, "all-or-nothing", payload=payload)
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == module.INTENT_ERROR
        assert "agent-good" not in out
        assert "invalid-path" in out
        assert status == 1

    @pytest.mark.parametrize("value", [
        "/absolute/p.md", "../escape.md", "dev/../../p.md", "dev\\plans\\p.md",
        "", "dev//p.md", "C:/p.md", "dev/./p.md",
    ])
    def test_the_path_predicate_refuses_every_unsafe_shape(self, value):
        assert planner._intent_valid_relative_path(value) is False

    @pytest.mark.parametrize("value", [
        "dev/plans/p.md", "tools/lifecycle_planner.py", "p.md",
    ])
    def test_the_path_predicate_admits_normalized_relative_paths(self, value):
        assert planner._intent_valid_relative_path(value) is True


class TestActiveIntentColumn:

    def test_no_claim_reads_dash_only_when_the_provider_worked(
            self, tmp_path, monkeypatch, capsys):
        repo, _record, module = _provider_repo(
            tmp_path, "no-claim", payload=_payload([]))
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == module.BOARD_ABSENT
        assert status == 0

    def test_one_intersecting_claim_names_its_agent(
            self, tmp_path, monkeypatch, capsys):
        repo, _record, module = _provider_repo(
            tmp_path, "one-claim",
            payload=_payload([_claim("c1", ["dev/plans/p.md"],
                                     agent="agent-alpha")]))
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == "agent-alpha"

    def test_multiple_claims_stay_visible_as_a_count(
            self, tmp_path, monkeypatch, capsys):
        """*"Multiple claims remain visible rather than last-writer-wins."*"""
        repo, _record, module = _provider_repo(
            tmp_path, "multi-claim",
            payload=_payload([
                _claim("c1", ["dev/plans/p.md"], agent="agent-alpha"),
                _claim("c2", ["dev/plans/p.md"], agent="agent-beta"),
                _claim("c3", ["dev/plans/p.md"], agent="agent-gamma"),
            ]))
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == "multiple:3"

    def test_an_unrelated_claim_does_not_touch_the_row(
            self, tmp_path, monkeypatch, capsys):
        repo, _record, module = _provider_repo(
            tmp_path, "unrelated",
            payload=_payload([_claim("c1", ["scripts/other.py"])]))
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == module.BOARD_ABSENT

    def test_a_released_claim_is_absent_from_the_provider_and_the_row(
            self, tmp_path, monkeypatch, capsys):
        """The stale release pair case.  Reduction is the intent engine's job and
        the board does not reimplement it -- so an already-reduced (released)
        claim simply is not in the payload, and the row must not invent it."""
        repo, _record, module = _provider_repo(
            tmp_path, "released", payload=_payload([]))
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        assert _cells(out)[0]["active_intent"] == module.BOARD_ABSENT

    def test_a_claim_changes_no_lifecycle_field(
            self, tmp_path, monkeypatch, capsys):
        """*"A claim does not change status, owner, validity, priority, or review
        readiness."*  Two identical plans, one claimed."""
        repo, _record, module = _provider_repo(
            tmp_path, "no-authority",
            payload=_payload([_claim("c1", ["dev/plans/claimed.md"])]))
        body = _pass_block("Plan review")
        _write_plan(repo, "claimed", status="implementing", body=body)
        _write_plan(repo, "free", status="implementing", body=body)
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"], module)
        rows = {row["artifact"]: row for row in _cells(out)}
        for field in ("status", "owner", "review", "evidence", "validity"):
            assert rows["claimed"][field] == rows["free"][field], field
        assert rows["claimed"]["active_intent"] != rows["free"]["active_intent"]

    def test_owner_and_active_intent_never_collapse(self):
        assert "owner" in planner.BOARD_FIELDS
        assert "active_intent" in planner.BOARD_FIELDS
        assert planner.BOARD_FIELDS.index("owner") + 1 == \
            planner.BOARD_FIELDS.index("active_intent")

    def test_explain_shows_each_claims_full_record_encoded(
            self, tmp_path, monkeypatch, capsys):
        """B1: *"`board --explain` shows each intersecting claim's id, recorded
        agent, timestamp, action, and files after the same terminal-safe
        encoding"*."""
        repo, _record, module = _provider_repo(
            tmp_path, "explain-claim",
            payload=_payload([_claim("c-1", ["dev/plans/p.md"],
                                     agent="agent\u200balpha",
                                     action="editing\x1b[31m")]))
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys,
                                    ["board", "--explain", "p"], module)
        assert "id=c-1" in out
        assert "agent=agent\\u200balpha" in out
        assert "action=editing\\x1b[31m" in out
        assert "files=dev/plans/p.md" in out
        assert "\x1b" not in out and "\u200b" not in out
        assert "a claim is not authority" in out

    def test_explain_says_provider_state_rather_than_no_claim(
            self, tmp_path, monkeypatch, capsys):
        repo, _record, module = _provider_repo(
            tmp_path, "explain-absent", launcher="absent")
        _write_plan(repo, "p", status="implementing",
                    body=_pass_block("Plan review"))
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys,
                                    ["board", "--explain", "p"], module)
        assert "not-installed" in out
        assert "does NOT mean nobody holds one" in out


# =============================================================================
# B8 -- the versioned intent JSON, and twin parity
# =============================================================================


class TestIntentListJsonContract:

    @staticmethod
    def _run(repo: Path, argv: list[str]):
        return subprocess.run(
            [sys.executable, "-I", str(CAIRN_ROOT / "tools" / "intent.py"),
             "--log-path", str(repo / "intents.jsonl"), *argv],
            cwd=str(repo), capture_output=True, text=True, check=False)

    def _log(self, repo: Path, records: list[dict]) -> None:
        repo.mkdir(parents=True, exist_ok=True)
        (repo / "intents.jsonl").write_text(
            "".join(json.dumps(record) + "\n" for record in records),
            encoding="utf-8")

    def test_the_schema_is_versioned_and_matches_the_board_reader(self):
        """The engine copy is a package leaf with relative imports, so its
        constant is read from source rather than by importing the module out of
        its package -- the value is what matters, and both sides must name the
        same literal for the board's refusal to be meaningful."""
        declaration = 'LIST_JSON_SCHEMA = "cairn-intent-list/1"'
        for path in (_INTENT_CLI_SOURCE, _INTENT_CLI_TEMPLATE):
            assert declaration in path.read_text(encoding="utf-8"), path
        assert planner.INTENT_LIST_SCHEMA == "cairn-intent-list/1"

    def test_an_empty_result_is_still_a_schema_bearing_payload(self, tmp_path):
        repo = tmp_path / "r"
        self._log(repo, [])
        proc = self._run(repo, ["list", "--format", "json"])
        assert proc.returncode == 0, proc.stderr
        payload = json.loads(proc.stdout)
        assert payload == {"schema": "cairn-intent-list/1", "claims": []}

    def test_output_is_deterministic_and_ascii_safe(self, tmp_path):
        repo = tmp_path / "r"
        self._log(repo, [
            {"event": "claim", "id": "b", "agent": "caf\u00e9",
             "ts": "2026-05-05", "action": "x\u200b", "files": ["a.md"]},
            {"event": "claim", "id": "a", "agent": "two", "ts": "2026-05-04",
             "action": "y", "files": ["b.md"]},
        ])
        first = self._run(repo, ["list", "--format", "json"]).stdout
        second = self._run(repo, ["list", "--format", "json"]).stdout
        assert first == second
        assert first.isascii()
        payload = json.loads(first)
        assert [claim["id"] for claim in payload["claims"]] == ["a", "b"]
        assert payload["claims"][1]["agent"] == "caf\u00e9"

    def test_the_projection_is_closed_and_drops_unknown_fields(self, tmp_path):
        """A "versioned" payload that passed through arbitrary log fields would
        not be versioned at all -- the first added log field would change the
        shape without a bump."""
        repo = tmp_path / "r"
        self._log(repo, [{
            "event": "claim", "id": "a", "agent": "one", "ts": "t",
            "action": "x", "files": ["a.md"], "future_field": "surprise",
        }])
        payload = json.loads(self._run(repo, ["list", "--format", "json"]).stdout)
        assert set(payload["claims"][0]) == {"id", "agent", "ts", "action",
                                            "stem", "files"}
        assert "surprise" not in json.dumps(payload)

    def test_the_board_reader_accepts_the_real_provider_output(self, tmp_path):
        """End-to-end schema agreement: the engine's real bytes through the
        board's real validator, so the two cannot drift apart silently."""
        repo = tmp_path / "r"
        self._log(repo, [{
            "event": "claim", "id": "a", "agent": "one", "ts": "t",
            "action": "x", "files": ["dev/plans/p.md"],
        }])
        proc = self._run(repo, ["list", "--format", "json"])
        reason, detail, claims = planner._intent_validate(
            json.loads(proc.stdout))
        assert reason is None, detail
        assert claims[0]["files"] == ["dev/plans/p.md"]

    def test_the_human_form_is_unchanged_and_still_the_default(self, tmp_path):
        repo = tmp_path / "r"
        self._log(repo, [{
            "event": "claim", "id": "a", "agent": "one", "ts": "t",
            "action": "x", "files": ["a.md"],
        }])
        default = self._run(repo, ["list"]).stdout
        explicit = self._run(repo, ["list", "--format", "text"]).stdout
        assert default == explicit
        assert default.startswith("id='a'")
        assert "schema" not in default

    def test_an_unknown_format_is_a_usage_error(self, tmp_path):
        repo = tmp_path / "r"
        self._log(repo, [])
        proc = self._run(repo, ["list", "--format", "yaml"])
        assert proc.returncode == 2
        assert "invalid choice" in proc.stderr

    def test_conflicts_with_still_filters_in_json_mode(self, tmp_path):
        repo = tmp_path / "r"
        self._log(repo, [
            {"event": "claim", "id": "a", "agent": "one", "ts": "t",
             "action": "x", "files": ["dev/plans/p.md"]},
            {"event": "claim", "id": "b", "agent": "two", "ts": "t",
             "action": "y", "files": ["scripts/other.py"]},
        ])
        payload = json.loads(self._run(
            repo, ["list", "--format", "json", "--conflicts-with",
                   "dev/plans/p.md"]).stdout)
        assert [claim["id"] for claim in payload["claims"]] == ["a"]


class TestTwinParity:
    """*"byte-identical in its source/template engine copies"* -- asserted here
    so a one-sided edit reddens in the same commit that makes it."""

    @pytest.mark.parametrize("left,right", [
        (_PLANNER_SOURCE, _PLANNER_TEMPLATE),
        (_INTENT_CLI_SOURCE, _INTENT_CLI_TEMPLATE),
    ])
    def test_the_twins_are_byte_identical(self, left, right):
        assert left.read_bytes() == right.read_bytes(), (
            f"{left} and {right} have diverged")

    def test_both_planner_copies_carry_the_same_range_table(self):
        """Revision 4: *"the planner and installed planner twin carry
        byte-identical range definitions"*.  Byte identity above implies it; this
        node names the specific clause so a future partial-file comparison cannot
        drop it."""
        marker = "_DISPLAY_UNSAFE_RANGES: Tuple[Tuple[int, int], ...] = ("
        blocks = []
        for path in (_PLANNER_SOURCE, _PLANNER_TEMPLATE):
            text = path.read_text(encoding="utf-8")
            start = text.index(marker)
            blocks.append(text[start:text.index("\n)\n", start)])
        assert blocks[0] == blocks[1]
        assert "\\u" not in blocks[0], (
            "the range table must use numeric endpoints, not escape forms of "
            "characters")


class TestBoardIsNotAuthority:
    """B0: *"It is not a new roadmap, queue, priority engine, review
    attestation, or source of lifecycle truth."*"""

    def test_the_board_writes_no_generated_file(self, tmp_path, monkeypatch,
                                                capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        before = {path for path in repo.rglob("*") if ".git" not in path.parts}
        _board(monkeypatch, repo, capsys, ["board"])
        _board(monkeypatch, repo, capsys, ["board", "--format", "json"])
        after = {path for path in repo.rglob("*") if ".git" not in path.parts}
        assert before == after

    def test_the_output_names_the_artifact_as_authoritative(
            self, tmp_path, monkeypatch, capsys):
        repo = _make_repo(tmp_path)
        _write_plan(repo, "p", status="implementing")
        _commit_all(repo)
        _status, out, _err = _board(monkeypatch, repo, capsys, ["board"])
        assert "The artifact is authoritative" in out
        assert "derived view" in out

    def test_the_board_contains_no_second_status_or_verdict_vocabulary(self):
        """B3: *"contains no consumer-local status, role, tier, verdict, or
        closeout vocabulary"*.  The board section is inside the planner, so the
        property is that it *reads* the central declarations rather than
        redefining them."""
        text = _PLANNER_TEMPLATE.read_text(encoding="utf-8")
        block = text[text.index("# Chunk F -- the derived orientation board"):]
        for name in ("PROPOSAL_STATES = (", "PLAN_STATES = (",
                     "CODE_REVIEW_CLEARING_VERDICTS = (",
                     "CODE_REVIEW_BLOCKING_VERDICTS = (",
                     "_TIERS = (", "PROPOSAL_NEXT_OWNERS = {",
                     "PLAN_NEXT_OWNERS = {"):
            assert name not in block, (
                f"the board section redeclares {name!r} instead of reading the "
                "central vocabulary")
        for reader in ("RECOGNIZED_STATES", "NEXT_OWNERS", "next_owner(",
                       "_parse_verdict(", "_conformance_violations("):
            assert reader in block, (
                f"the board section does not consume {reader!r}")
