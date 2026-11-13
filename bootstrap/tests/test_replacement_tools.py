# SPDX-License-Identifier: MIT
"""The three small tools that replace what the sweep removes.

Promises:
- The board's --maintainer view lists each declared waiting-on-Maintainer item once and nothing it infers; its footer names what it cannot see.
- The board lists active proposals and plans, shows archived ones only with --archive, and never lists templates.
- The board prints only header fields an author wrote, with every printed value escaped.
- The gauge sorts each path into one of its classes and prints unclassified paths rather than bucketing them.
- The audit sample is reproducible from its salt and does not depend on input order.
- The audit report marks independent review identity unknown, warns on a ledger with no numbers, and accepts pending as an outcome.
- The audit report summarizes the last real implementation-verification record and treats malformed benefit lines as unknown.
- Ambiguous review files stay orphaned in the pulse snapshot.
- The legacy review generator reads only the pinned commit tree and refuses a target-local git route.

Each carries one property the thing it replaces had, and these tests pin that
property rather than the output format. They import unconditionally: a tool
that has gone missing should error here, not skip.
"""

from __future__ import annotations

import importlib.util
import hashlib
import os
import subprocess
import sys
from types import SimpleNamespace
from pathlib import Path

import pytest
from tests.test_verify_counts import (
    _assert_public_route_triplet,
    _assert_bound_member_mutation,
    _assert_bound_member_positive,
    _BINDING_MUTATIONS,
)

CAIRN_ROOT = Path(__file__).resolve().parents[2]


def _load(name: str):
    path = CAIRN_ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_cairn_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


board = _load("board")
gauge = _load("gauge")
audit = _load("audit_report")


def _load_script(name: str):
    path = CAIRN_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_cairn_script_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


legacy_report = _load_script("gen_legacy_code_review_passes")


_LEGACY_ROUTE_HEADING = "## Code review -- Route Reviewer -- 2026-11-06"


def _seed_legacy_route_repo(root: Path) -> None:
    root.mkdir()
    (root / "dev/plans/archive").mkdir(parents=True)
    (root / "dev/plans/a.md").write_text(
        "# x\n\n" + _LEGACY_ROUTE_HEADING + "\n\nVerdict: Ship\n",
        encoding="utf-8")
    (root / "dev/plans/archive/keep.txt").write_text("keep\n", encoding="utf-8")
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
    subprocess.run(["git", "-C", str(root), "add", "dev/plans"], env=env,
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "seed plans"],
                   env=env, check=True, capture_output=True)
    (root / "dev/plans/a.md").unlink()
    subprocess.run(["git", "-C", str(root), "add", "-u", "dev/plans"], env=env,
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "empty plan tree"],
                   env=env, check=True, capture_output=True)


def _legacy_route_driver(selected: str, *, refusal: bool = False) -> str:
    digest = hashlib.sha256(_LEGACY_ROUTE_HEADING.encode("utf-8")).hexdigest()[:16]
    expected = ("git ls-tree --name-only HEAD~1:dev/plans unavailable"
                if selected == "ls-tree" else
                "git show HEAD~1:dev/plans/a.md unavailable")
    return f'''\
import os
import runpy
module = runpy.run_path(os.environ["CAIRN_TEST_CALLER"], run_name="_route_legacy")
root = os.environ["CAIRN_TEST_TARGET_ROOT"]
if {refusal!r}:
    try:
        module["main"](["--root", root, "--baseline", "HEAD~1"])
    except RuntimeError as exc:
        assert str(exc) == {expected!r}
        print("route-refused")
    else:
        raise AssertionError("hostile PATH became trusted Git")
else:
    import contextlib
    import io
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert module["main"](["--root", root, "--baseline", "HEAD~1"]) == 0
    assert "# 1 record(s) across 1 stem(s)." in out.getvalue()
    assert {('"a": {"' + digest + '": 1}')!r} in out.getvalue()
    print(out.getvalue(), end="")
    empty = io.StringIO()
    with contextlib.redirect_stdout(empty):
        assert module["main"](["--root", root, "--baseline", "HEAD"]) == 0
    assert "# 0 record(s) across 0 stem(s)." in empty.getvalue()
    try:
        module["main"](["--root", root, "--baseline", "missing-baseline"])
    except RuntimeError as exc:
        assert "git ls-tree" in str(exc) and "unavailable" in str(exc)
    else:
        raise AssertionError("invalid baseline produced a clean manifest")
    print("route-positive")
'''


def _assert_legacy_route_output(result) -> None:
    digest = hashlib.sha256(_LEGACY_ROUTE_HEADING.encode("utf-8")).hexdigest()[:16]
    assert "# 1 record(s) across 1 stem(s)." in result.stdout
    assert f'"a": {{"{digest}": 1}}' in result.stdout


def test_legacy_ls_tree_refuses_target_local_path_git_route(tmp_path):
    clean, _safe, _unsafe = _assert_public_route_triplet(
        tmp_path / "legacy-ls-tree", "scripts/gen_legacy_code_review_passes.py",
        "_git", ("ls-tree", "--name-only", "HEAD~1:dev/plans"),
        _legacy_route_driver("ls-tree"),
        _legacy_route_driver("ls-tree", refusal=True),
        seed=_seed_legacy_route_repo)
    _assert_legacy_route_output(clean)


def test_legacy_show_refuses_target_local_path_git_route(tmp_path):
    clean, _safe, _unsafe = _assert_public_route_triplet(
        tmp_path / "legacy-show", "scripts/gen_legacy_code_review_passes.py",
        "_git", ("show", "HEAD~1:dev/plans/a.md"),
        _legacy_route_driver("show"),
        _legacy_route_driver("show", refusal=True),
        seed=_seed_legacy_route_repo)
    _assert_legacy_route_output(clean)


def _write_artifact(root: Path, rel: str, header: str = "", body: str = "") -> None:
    """One proposal or plan in a scratch tree: a header block, then a body."""
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# x\n\n{header}\n\n## Body\n{body}\n", encoding="utf-8")


def _maintainer_view(root: Path, capsys, *extra: str):
    """Run `board --maintainer` on a scratch tree.

    Returns the listed entries as `(kind, artifact, reason, text)` and the
    printed lines, so a test can read the footer too.
    """
    assert board.main(["--maintainer", "--root", str(root), *extra]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "board: kind | artifact | reason | text"
    entries = []
    for line in lines[1:]:
        cells = line.removeprefix("board: ").split(" | ", 3)
        if len(cells) == 4:
            entries.append(tuple(cells))
    return entries, lines


class TestTheBoardReadsHeadersAndJudgesNothing:
    """The board it replaces derived status, obligations and blockers. This one
    reports header fields, because a derived judgment printed beside a fact
    reads as a fact."""

    @pytest.mark.parametrize("extra, expected", [
        pytest.param((), (
            ["kind", "artifact", "Status", "Opened"],
            [["proposal", "2026-01-01-a-open", "awaiting-review", ""],
             ["plan", "open-plan", "implementing", "2026-01-01"]],
        ), id="active-only"),
        pytest.param(("--archive",), (
            ["kind", "artifact", "Status", "Opened", "archived"],
            [["proposal", "2026-01-01-a-open", "awaiting-review", "", ""],
             ["plan", "open-plan", "implementing", "2026-01-01", ""],
             ["plan", "done-plan", "archived", "", "yes"]],
        ), id="with-archive"),
    ])
    def test_the_plain_board_lists_active_artifacts_and_only_authored_fields(
            self, tmp_path, capsys, extra, expected) -> None:
        """Open proposals and plans are listed; archived ones only with
        `--archive`; templates never. A column appears only for a header field
        some artifact wrote, a field an artifact did not write prints empty, and
        a field written below the first heading is not a header field. Built in a
        scratch tree, because an empty board is a valid state of the real
        repository and must not fail the suite."""
        _write_artifact(tmp_path, "dev/proposals/2026-01-01-a-open.md",
                        "**Status**: awaiting-review")
        _write_artifact(tmp_path, "dev/proposals/_template.md",
                        "**Status**: awaiting-review")
        _write_artifact(tmp_path, "dev/plans/open-plan.md",
                        "**Status**: implementing\n**Opened**: 2026-01-01",
                        "**Review**: below the first heading, so not a header field")
        _write_artifact(tmp_path, "dev/plans/archive/done-plan.md",
                        "**Status**: archived")

        assert board.main(["--root", str(tmp_path), *extra]) == 0

        table = [line.removeprefix("board: ").split(" | ")
                 for line in capsys.readouterr().out.splitlines()
                 if line.startswith("board: ") and " | " in line]
        assert (table[0], table[1:]) == expected


    def test_maintainer_lists_exactly_what_authors_declared(
            self, tmp_path, capsys) -> None:
        """`--maintainer` lists a proposal at `awaiting-decision`, an artifact
        carrying the Waiting line, and a marked board row -- each once -- and
        nothing it inferred. The failure this guards is a wait that drops off
        the list without a sound: a status with a note after it, a line with its
        text blanked, a row indented as a continuation line or as a sub-bullet."""
        wait = "**Waiting on Maintainer**:"
        _write_artifact(tmp_path, "dev/proposals/2026-01-01-a-decide.md",
                        "**Status**: awaiting-decision")
        _write_artifact(tmp_path, "dev/proposals/2026-01-02-b-noted.md",
                        "**Status**: awaiting-decision \u2014 note")
        _write_artifact(tmp_path, "dev/proposals/2026-01-03-c-both.md",
                        f"**Status**: awaiting-decision\n{wait} both ways")
        _write_artifact(tmp_path, "dev/plans/says-so.md",
                        f"**Status**: implementing\n{wait} run the ceremony")
        _write_artifact(tmp_path, "dev/plans/blanked.md",
                        f"**Status**: implementing\n{wait}")
        _write_artifact(tmp_path, "dev/proposals/2026-01-04-d-review.md",
                        "**Status**: awaiting-review")
        _write_artifact(tmp_path, "dev/plans/quiet.md", "**Status**: implementing")
        _write_artifact(tmp_path, "dev/plans/archive/old.md",
                        f"**Status**: archived\n{wait} stale")
        (tmp_path / "dev" / "PLANNING.md").write_text(
            "# Board\n\n"
            f"* A row.\n  {wait} indented\n"
            f"  * {wait} sub-bullet\n"
            f"- {wait} dash bullet\n", encoding="utf-8")

        expected = [
            ("proposal", "2026-01-01-a-decide", "awaiting-decision", ""),
            ("proposal", "2026-01-02-b-noted", "awaiting-decision", ""),
            ("proposal", "2026-01-03-c-both", "awaiting-decision", "both ways"),
            ("plan", "blanked", "declared", ""),
            ("plan", "says-so", "declared", "run the ceremony"),
            ("roadmap", "dev/PLANNING.md:4", "declared", "indented"),
            ("roadmap", "dev/PLANNING.md:5", "declared", "sub-bullet"),
            ("roadmap", "dev/PLANNING.md:6", "declared", "dash bullet"),
        ]
        entries, _ = _maintainer_view(tmp_path, capsys)
        assert entries == expected
        # The archives never count, with or without the flag.
        with_archive, _ = _maintainer_view(tmp_path, capsys, "--archive")
        assert with_archive == expected

    def test_a_fence_with_no_declared_wait_is_named_not_listed(
            self, tmp_path, capsys) -> None:
        """A plan that mentions a fence but declares no wait is named on the
        advisory line and is not listed as waiting: the board reports a lexical
        fact and never decides that a gate is open. The advisory reads live plans
        only -- an archive, a template, or a proposal that says the word is not
        a plan waiting on anyone."""
        fence = "A chunk marked MAINTAINER-ONLY."
        _write_artifact(tmp_path, "dev/plans/fenced.md",
                        "**Status**: implementing", fence)
        _write_artifact(tmp_path, "dev/plans/gated.md",
                        "**Status**: implementing", "MAINTAINER-GATED chunk.")
        _write_artifact(tmp_path, "dev/plans/declared.md",
                        "**Status**: implementing\n**Waiting on Maintainer**: go",
                        fence)
        _write_artifact(tmp_path, "dev/plans/archive/old.md",
                        "**Status**: archived", fence)
        _write_artifact(tmp_path, "dev/plans/_template.md",
                        "**Status**: awaiting-plan-review", fence)
        _write_artifact(tmp_path, "dev/proposals/2026-01-01-a-open.md",
                        "**Status**: awaiting-review", fence)

        for extra in ((), ("--archive",)):
            entries, lines = _maintainer_view(tmp_path, capsys, *extra)
            assert [e[:2] for e in entries] == [("plan", "declared")]
            advisory = [l for l in lines if l.startswith("board: advisory")]
            assert len(advisory) == 1
            assert advisory[0].endswith(": fenced, gated"), advisory[0]

        (tmp_path / "dev" / "plans" / "fenced.md").unlink()
        (tmp_path / "dev" / "plans" / "gated.md").unlink()
        _, lines = _maintainer_view(tmp_path, capsys)
        advisory = [l for l in lines if l.startswith("board: advisory")]
        assert len(advisory) == 1 and advisory[0].endswith(": none"), advisory

    def test_a_mention_of_the_marker_is_not_a_marker(
            self, tmp_path, capsys) -> None:
        """Only the row form lists. A sentence that names the marker, a mention
        in backticks, and a colon written inside the bold are not declarations;
        a matcher loosened to a substring search would list all of them and bury
        the real one. One real marker is included so the check can fire."""
        (tmp_path / "dev").mkdir()
        (tmp_path / "dev" / "PLANNING.md").write_text(
            "A row is marked with **Waiting on Maintainer**: when it waits.\n"
            "Write `**Waiting on Maintainer**: text` inside the row.\n"
            "`**Waiting on Maintainer**: starts with a backtick`\n"
            "**Waiting on Maintainer:** colon inside the bold\n"
            "  **Waiting on Maintainer**: the real one\n", encoding="utf-8")
        entries, _ = _maintainer_view(tmp_path, capsys)
        assert entries == [("roadmap", "dev/PLANNING.md:5", "declared",
                            "the real one")]

    def test_the_footer_names_what_the_list_cannot_see(
            self, tmp_path, capsys) -> None:
        """The list is what authors declared, so the footer says what it does
        not hold: pushes, and anything no artifact or row declares. A missing
        board file is named, never read as zero rows -- a list that is short
        because a file went missing must not look like a list that is empty."""
        _write_artifact(tmp_path, "dev/proposals/2026-01-01-a-decide.md",
                        "**Status**: awaiting-decision")
        entries, lines = _maintainer_view(tmp_path, capsys)
        assert [e[1] for e in entries] == ["2026-01-01-a-decide"]
        unlisted = [l for l in lines if l.startswith("board: not listed")]
        assert len(unlisted) == 1
        assert "pushes" in unlisted[0] and "no artifact or row declares" in unlisted[0]
        assert any("dev/PLANNING.md is missing" in l for l in lines)

        (tmp_path / "dev" / "PLANNING.md").write_text("# Board\n", encoding="utf-8")
        _, lines = _maintainer_view(tmp_path, capsys)
        assert not any("missing" in l for l in lines)

    def test_every_value_the_view_prints_is_encoded(
            self, tmp_path, capsys) -> None:
        """Header values, row values and artifact names all come out of files
        any contributor can edit, so each passes through the shared encoder.
        A raw escape in any one of the three would reach the terminal."""
        esc = "\x1b"
        _write_artifact(tmp_path, "dev/plans/says-so.md",
                        f"**Status**: implementing\n"
                        f"**Waiting on Maintainer**: header {esc}[31mred")
        (tmp_path / "dev" / "PLANNING.md").write_text(
            f"* **Waiting on Maintainer**: row {esc}[31mred\n", encoding="utf-8")
        # A name is a filename, which not every filesystem accepts.
        named = f"evil{esc}[31m"
        try:
            _write_artifact(tmp_path, f"dev/plans/{named}.md",
                            "**Status**: implementing", "MAINTAINER-ONLY")
            _write_artifact(tmp_path, f"dev/proposals/{named}.md",
                            "**Status**: awaiting-decision")
        except OSError:
            named = None

        entries, lines = _maintainer_view(tmp_path, capsys)
        assert esc not in "\n".join(lines)
        escaped = "\\x1b[31mred"  # the encoder's spelling of ESC
        assert ("plan", "says-so", "declared", f"header {escaped}") in entries
        assert ("roadmap", "dev/PLANNING.md:1", "declared", f"row {escaped}") in entries
        if named is not None:
            shown = "evil\\x1b[31m"
            assert any(e[1] == shown for e in entries), entries
            advisory = [l for l in lines if l.startswith("board: advisory")]
            assert advisory and advisory[0].endswith(shown), advisory


class TestTheGaugeNeverBucketsWhatItCannotClassify:
    """The hand-built table could not be reproduced by an independent reader,
    which is the whole reason a classifier is committed. A rule that silently
    absorbed unknown paths would reintroduce exactly that opacity."""

    def test_an_unknown_path_is_unclassified_not_product(self) -> None:
        assert gauge.classify("some/path/nobody/ruled/on.txt") is None

    @pytest.mark.parametrize("path,expected", [
        ("dev/plans/x.md", "dev"),
        ("bootstrap/security_check.py", "security-machinery"),
        ("bootstrap/_scaffold/install.py", "product"),
        ("bootstrap/_scaffold/config.py", "product"),
        ("bootstrap/scaffold.py", "product"),
        (".zenodo.json", "product"),
        ("docs/methodology/rationale.md", "product"),
        ("bootstrap/tests/test_upgrade.py", "other-machinery"),
    ])
    def test_representative_paths_land_in_their_class(self, path, expected) -> None:
        assert gauge.classify(path) == expected

    def test_security_rules_win_over_the_broader_machinery_prefix(self) -> None:
        """`bootstrap/` would claim these too. First match wins, so rule order
        is the rule -- and a reordering that quietly reclassified the security
        column would move the number the gauge exists to report."""
        assert gauge.classify("bootstrap/tests/test_security_lint.py") == "security-machinery"
        assert gauge.classify("bootstrap/tests/test_upgrade.py") == "other-machinery"

    def test_non_pulse_command_keeps_output_shape_and_reports_unmatched_paths(
            self, tmp_path, monkeypatch, capsys) -> None:
        rows = [
            ("2026-01-05", "bootstrap/scaffold.py", 4),
            ("2026-01-05", "bootstrap/_scaffold/install.py", 6),
            ("2026-01-05", "bootstrap/security_check.py", 2),
            ("2026-01-05", "bootstrap/tests/test_upgrade.py", 3),
            ("2026-01-05", ".zenodo.json", 1),
            ("2026-01-05", "unclassified/item.txt", 5),
        ]
        monkeypatch.setattr(gauge, "_numstat", lambda root, since: rows)
        assert gauge.main(["--root", str(tmp_path), "--since", "2026-01-01"]) == 0
        lines = capsys.readouterr().out.splitlines()
        assert lines[0] == "gauge: week | dev | security-machinery | other-machinery | product | product share"
        assert lines[1] == "gauge: 2026-01-05 | 0 | 2 | 3 | 11 | 68%"
        assert lines[2] == "gauge: UNCLASSIFIED (reported, never bucketed):"
        assert lines[3] == "gauge:   unclassified/ -- 5 line(s)"


@pytest.mark.parametrize("ledger, expected_state, falsification_output", [
    pytest.param(
        "**Author**: Same Name\n**Status**: archived\n**Risk**: low\n\n"
        "## Plan review -- Same Name -- 2026-01-01\n\n"
        "## Implementation verification -- Same Name -- 2026-01-02\n"
        "4596 passed, 3 failed\n",
        "unknown", "y", id="reviewer-with-the-authors-name"),
    pytest.param(
        "**Status**: archived\n**Risk**: low\n\n"
        "## Plan review -- someone -- 2026-01-01\n\n"
        "## Implementation verification -- someone -- 2026-01-02\n"
        "4596 passed, 3 failed\n",
        "unknown", "y", id="complete-change"),
    pytest.param(
        "**Status**: archived\n**Risk**: low\n\n"
        "## Plan review -- someone -- 2026-01-01\n\n"
        "## Implementation verification -- someone -- 2026-01-02\n"
        "Ran the full suite and it was fine.\n",
        "warn", "n", id="ledger-naming-no-numbers"),
    pytest.param(
        "**Status**: pending -- revisit after the next field season\n"
        "**Risk**: low\n\n## Plan review -- someone -- 2026-01-01\n\n"
        "## Implementation verification -- someone -- 2026-01-02\n"
        "12 passed\n",
        "unknown", "y", id="pending-is-an-accepted-outcome"),
])
def test_the_audit_report_never_claims_independent_review_and_flags_what_is_missing(
        tmp_path, capsys, ledger, expected_state, falsification_output) -> None:
    """Through the command line: whatever the ledger says, the report keeps the
    independence of the review unknown; a ledger that names no numbers is
    warned about; `pending` is an accepted outcome, so it draws no warning."""
    archive = tmp_path / "dev" / "plans" / "archive"
    archive.mkdir(parents=True)
    (archive / "change.md").write_text(ledger, encoding="utf-8")

    assert audit.main(["--root", str(tmp_path)]) == 0

    line = next(line for line in capsys.readouterr().out.splitlines()
                if line.startswith("audit: [") and " change -- " in line)
    state = line.split("]", 1)[0].removeprefix("audit: [")
    assert (state, "independent-review=unknown" in line,
            f"falsification-output={falsification_output}" in line) == (
                expected_state, True, True)


def test_public_audit_summary_uses_only_the_last_real_verification_record(
        tmp_path) -> None:
    """The release command reports one final record per plan, ignores examples,
    and tallies valid, absent, duplicate and malformed benefit lines."""
    archive = tmp_path / "dev" / "plans" / "archive"
    archive.mkdir(parents=True)
    records = {
        "earlier-only.md": (
            "## Implementation verification -- old -- 2026-01-01\n"
            "**Benefit versus cost**: worth it -- old; cost 1; remaining burden 0\n"
            "## Implementation verification -- final -- 2026-01-02\n"
        ),
        "historical-absence.md": "**Status**: archived\n",
        "duplicate.md": (
            "## Implementation verification -- final -- 2026-01-02\n"
            "**Benefit versus cost**: partly -- one; cost 2; remaining burden 3\n"
            "**Benefit versus cost**: worth it -- two; cost 1; remaining burden 0\n"
        ),
        "malformed.md": (
            "## Implementation verification -- final -- 2026-01-02\n"
            "**Benefit versus cost**: worth it -- missing fields\n"
        ),
        "quoted-example.md": (
            "```markdown\n## Implementation verification -- example\n"
            "**Benefit versus cost**: worth it -- example; cost 0; remaining burden 0\n"
            "```not-a-closing-fence\n## Implementation verification -- fake\n"
            "**Benefit versus cost**: worth it -- fake; cost 0; remaining burden 0\n```\n"
            "> ## Implementation verification -- quoted\n"
            "> **Benefit versus cost**: partly -- example; cost 0; remaining burden 0\n"
        ),
        "valid-not-worth-it.md": (
            "## Implementation verification -- final -- 2026-01-02\n"
            "**Benefit versus cost**: not worth it -- benefit lost; cost 8; remaining burden 5\n"
        ),
        "valid-worth-it.md": (
            "## Implementation verification -- final -- 2026-01-02\n"
            "**Benefit versus cost**: worth it -- benefit delivered; cost 2; remaining burden 0\n"
        ),
        "valid-partly.md": (
            "## Implementation verification -- final -- 2026-01-02\n"
            "**Benefit versus cost**: partly -- benefit mixed; cost 5; remaining burden 2\n"
        ),
        "valid-unknown.md": (
            "## Implementation verification -- final -- 2026-01-02\n"
            "**Benefit versus cost**: unknown -- evidence is incomplete; cost unknown; remaining burden unknown\n"
            "**Revisit condition**: when the missing integration evidence is available\n"
        ),
    }
    for name, content in records.items():
        (archive / name).write_text(content, encoding="utf-8")

    command = [sys.executable, str(CAIRN_ROOT / "tools" / "audit_report.py"),
               "--root", str(tmp_path)]
    run = subprocess.run(command, cwd=tmp_path, capture_output=True,
                         text=True, check=True)
    output = run.stdout
    rows = {line.split(" -- review-evidence=", 1)[0].rsplit(" ", 1)[-1]: line
            for line in output.splitlines() if line.startswith("audit: [")}
    assert 'benefit-versus-cost="no line"' in rows["earlier-only"]
    assert 'benefit-versus-cost="no line"' in rows["historical-absence"]
    assert 'benefit-versus-cost="unknown"' in rows["malformed"]
    assert "malformed current benefit-versus-cost line" in output
    assert 'benefit-versus-cost="unknown"' in rows["duplicate"]
    assert "duplicate current benefit-versus-cost lines" in output
    assert 'benefit-versus-cost="no line"' in rows["quoted-example"]
    assert 'benefit-versus-cost="not worth it"' in rows["valid-not-worth-it"]
    assert 'benefit-versus-cost="worth it"' in rows["valid-worth-it"]
    assert 'benefit-versus-cost="partly"' in rows["valid-partly"]
    assert 'benefit-versus-cost="unknown"' in rows["valid-unknown"]
    assert ("audit: benefit-versus-cost totals: worth it=1, partly=1, "
            "not worth it=1, unknown=3, no line=3") in output
    lines = output.splitlines()
    total_line = next(i for i, line in enumerate(lines)
                      if line.startswith("audit: benefit-versus-cost totals:"))
    assert all(i < total_line for i, line in enumerate(lines)
               if line.startswith("audit: ["))


def test_the_audit_sample_is_fixed_by_its_salt_not_by_input_order(
        tmp_path, capsys) -> None:
    """Whoever assembles an audit packet must not be able to choose the sample.
    The same salt draws the same sample on a rerun and when the files were
    created in the opposite order, another salt draws another, and the draw is
    the documented rule: sort by sha256(salt + stem), take the first k."""
    stems = [f"artifact-{i}" for i in range(40)]
    for name, order in (("forward", stems), ("backward", stems[::-1])):
        archive = tmp_path / name / "dev" / "plans" / "archive"
        archive.mkdir(parents=True)
        for stem in order:
            (archive / f"{stem}.md").write_text("**Status**: pending\n",
                                                 encoding="utf-8")

    def sample(name: str, salt: str) -> list:
        assert audit.main(["--root", str(tmp_path / name), "--sample", "5",
                           "--salt", salt]) == 0
        return sorted(line.split("] ", 1)[1].split(" -- ", 1)[0]
                      for line in capsys.readouterr().out.splitlines()
                      if line.startswith("audit: ["))

    rule = sorted(sorted(stems, key=lambda s: hashlib.sha256(
        ("s" + s).encode("utf-8")).hexdigest())[:5])
    first = sample("forward", "s")
    assert (first == rule, sample("forward", "s") == first,
            sample("backward", "s") == first, sample("forward", "t") != first
            ) == (True, True, True, True)


class TestTheAuditReportKeepsSidefileAttributionHonest:
    def test_real_entry_point_joins_unique_same_stem_and_reports_ambiguity(
            self, tmp_path, capsys) -> None:
        archive = tmp_path / "dev" / "plans" / "archive"
        parent = archive / "parent.md"
        parent.parent.mkdir(parents=True)
        parent.write_text(
            "**Status**: archived\n**Risk**: low\n"
            "## Code review -- Same Name -- 2026-01-01\n"
            "## Implementation verification -- author -- 2026-01-02\n"
            "12 passed\n", encoding="utf-8")
        (archive / "parent.code-review.md").write_text(
            "# Detached review\n## Code review -- Reviewer -- 2026-01-03\n",
            encoding="utf-8")
        (archive / "orphan.security-review.md").write_text(
            "# Detached review without parent evidence\n",
            encoding="utf-8")

        assert audit.main(["--root", str(tmp_path)]) == 0
        output = capsys.readouterr().out
        assert "parent -- review-evidence=2 independent-review=unknown" in output
        assert "parent.code-review.md -> parent" in output
        assert "orphan.security-review.md -> parent unresolved or ambiguous" in output
        assert "independent-review=unknown" in output
        assert "orphan.security-review.md" not in output.split("parent --", 1)[0]

    def test_explicit_parent_path_must_resolve_uniquely(self, tmp_path, capsys) -> None:
        archive = tmp_path / "dev" / "plans" / "archive"
        archive.mkdir(parents=True)
        (archive / "target.md").write_text("**Status**: pending\n", encoding="utf-8")
        review = archive / "standalone.code-review.md"
        review.write_text(
            "**Parent artifact**: dev/plans/archive/target.md\n"
            "## Code review -- Named Reviewer\n", encoding="utf-8")
        assert audit.main(["--root", str(tmp_path)]) == 0
        output = capsys.readouterr().out
        assert "review-evidence=1 independent-review=unknown" in output
        assert "standalone.code-review.md -> target" in output

    def test_conflicting_parent_links_are_reported_as_ambiguous(
            self, tmp_path, capsys) -> None:
        archive = tmp_path / "dev" / "plans" / "archive"
        archive.mkdir(parents=True)
        for stem in ("one", "two"):
            (archive / f"{stem}.md").write_text(
                "**Status**: archived\n", encoding="utf-8")
        (archive / "ambiguous.review.md").write_text(
            "**Parent artifact**: one.md\n**Parent plan**: two.md\n",
            encoding="utf-8")
        assert audit.main(["--root", str(tmp_path)]) == 0
        output = capsys.readouterr().out
        assert "ambiguous.review.md -> parent unresolved or ambiguous" in output
        assert "1 unresolved" in output


def test_public_pulse_attaches_multiple_explicit_sidefiles_and_leaves_ambiguous_orphans(
    tmp_path, capsys,
):
    import json

    root = tmp_path
    texts = {
        "dev/plans/p.md": (
            "# P\n## Scope\nOpening.\n## cOdE rEvIeW -- Reviewer -- 2026-11-06\n"
            "**Model**: Codex 5.3\n## Response -- Author -- 2026-11-06\nReply.\n"),
        "dev/plans/p.code-review.md": (
            "**Parent plan**: dev/plans/p.md\n"
            "## Security review -- Reviewer -- 2026-11-06\n**Model**: Sol\n"),
        "reviews/2026-11-06-code-review-return.md": (
            "**Parent plan**: dev/plans/p.md\n"
            "## Targeted code review return -- Reviewer\n"),
        "a/q.md": "## Scope\n",
        "b/q.md": "## Scope\n",
        "elsewhere/q.review.md": "## Code review\n",
    }
    for label, text in texts.items():
        _write_artifact(root, label, text)
    args = ["--pulse-input", "--root", str(root), "--week", "2026-W45",
            "--project-alias", "cairn", "--model-tier", "Codex 5.3=high",
            "--model-tier", "Sol=medium"]
    for label in texts:
        args.extend(("--artifact", label))
    assert audit.main(args) == 0
    bundle = root / "pulse-input.json"
    bundle.write_text(capsys.readouterr().out, encoding="utf-8")
    assert gauge.main(["--pulse", "--artifact-input", str(bundle), "--json"]) == 0
    result = json.loads(capsys.readouterr().out)
    metrics = result["artifacts"]
    parent = next(row for row in metrics["parents"] if row["artifact"] == "dev/plans/p.md")
    assert parent["sidefiles"] == [
        "dev/plans/p.code-review.md", "reviews/2026-11-06-code-review-return.md"]
    assert parent["review_passes"] == 3
    assert parent["other_appendices"]["words"] > 0
    assert metrics["orphan_labels"] == ["elsewhere/q.review.md"]
    assert metrics["model_records"]["by_tier"]["high"] == 1
    assert metrics["model_records"]["by_tier"]["medium"] == 1


class TestLegacyReviewGeneratorPhysicalBinding:
    def test_real_cli_executes_its_pinned_helper(self, tmp_path: Path) -> None:
        _assert_bound_member_positive(
            tmp_path, "scripts/gen_legacy_code_review_passes.py",
        )

    @pytest.mark.parametrize("mutation", _BINDING_MUTATIONS)
    def test_real_cli_refuses_each_binding_mutation(
            self, mutation: str, tmp_path: Path) -> None:
        _assert_bound_member_mutation(
            tmp_path, "scripts/gen_legacy_code_review_passes.py", mutation,
        )
