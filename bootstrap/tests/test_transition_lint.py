"""Tests for ``scripts/transition_lint.py``.

Two tiers.  **Synthetic** nodes build a throwaway git repository per test
and assert a behaviour.  **Corpus-regression** nodes (Chunk E) run the
committed script over SHA-pinned windows of Cairn's own history and
self-skip if that history is not present.

Every node here has a named perturbation recorded in the plan
(``dev/plans/transition-lint.md``), and each perturbation was run and
observed red at implementation.  A perturbation is on the *hazard* --
the code the node claims to guard -- never on the node's own fixture.
"""
from __future__ import annotations

import ast
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TL_SRC = REPO_ROOT / "scripts" / "transition_lint.py"

pytestmark = pytest.mark.skipif(
    shutil.which("git") is None or not TL_SRC.exists(),
    reason="git or transition_lint.py not available",
)

_IDENTITY = (
    "-c", "user.name=Cairn Test",
    "-c", "user.email=test@cairn.invalid",
    "-c", "commit.gpgsign=false",
)


def _load_tl(name: str = "_transition_lint_under_test") -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, TL_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def tl() -> ModuleType:
    return _load_tl()


@pytest.fixture(scope="module")
def tl_src() -> str:
    return TL_SRC.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Fixture helpers -- a throwaway repository, never the live tree
# ---------------------------------------------------------------------------


def _git(repo: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", *_IDENTITY, *args],
        cwd=str(repo), capture_output=True, check=True, text=True,
    )
    return out.stdout.strip()


def _write(repo: Path, rel: str, text: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _commit(repo: Path, subject: str) -> str:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", subject)
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q", "-b", "main")
    _write(r, "README.md", "seed\n")
    _commit(r, "seed")
    return r


def _last(repo: Path) -> str:
    """The range covering exactly the newest commit."""
    return "HEAD~1..HEAD"


# ---------------------------------------------------------------------------
# Chunk A -- plumbing: rev-range, enumeration, narrowing, exit contract
# ---------------------------------------------------------------------------


class TestExitContract:
    """AC-R10, the exit half: advisory means exit 0, always."""

    def test_main_returns_zero_on_a_repo_with_findings(
        self, tl: ModuleType, repo: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        # A9.  Perturbation: change main's tail to
        # ``return 1 if findings else 0``.  Run at implementation: red.
        _write(repo, "dev/plans/x.md", "# x\n\n**Status**: open\n")
        _commit(repo, "dev/plans: x -- seed")
        planted = [tl.Finding("0" * 40, "a", "dev/plans/x.md", "planted")]
        original = tl.scan
        try:
            tl.scan = lambda *a, **k: (1, 1, planted)  # type: ignore[assignment]
            rc = tl.main([_last(repo), "--root", str(repo)])
        finally:
            tl.scan = original  # type: ignore[assignment]
        out = capsys.readouterr().out
        assert rc == 0
        assert "1 findings" in out
        assert "planted" in out

    def test_unresolvable_but_parsable_range_exits_2(
        self, tl: ModuleType, repo: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        # A10.  Perturbation: delete the ``git rev-parse --verify`` call
        # in ``_validate_range``, leaving only the regex.  Red.
        rc = tl.main(["deadbeef000..HEAD", "--root", str(repo)])
        assert rc == 2
        assert capsys.readouterr().err.strip()

    def test_malformed_range_exits_2(
        self, tl: ModuleType, repo: Path,
        capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        # A11.  Perturbation: delete the regex guard in
        # ``_validate_range``.  Red.
        #
        # The plan's wording for this row -- "delete the regex guard;
        # git rev-list then errors and the degrade-quiet path swallows
        # it" -- does NOT redden a bare exit-code assertion in this
        # implementation, because the endpoint-resolution check catches
        # a malformed range too.  Verified at implementation: with only
        # ``assert rc == 2``, deleting the regex leaves this GREEN.  So
        # the node asserts the property the regex alone owns: the range
        # is rejected **before git is invoked at all**.
        def _explode(*_a: object, **_k: object) -> tuple[int, bytes]:
            raise AssertionError("git was invoked on a malformed rev-range")

        monkeypatch.setattr(tl, "_git", _explode)
        rc = tl.main(["not a range", "--root", str(repo)])
        assert rc == 2
        assert capsys.readouterr().err.strip()

    def test_missing_range_exits_2(
        self, tl: ModuleType, repo: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        # A12.  Perturbation: give the positional a ``HEAD~20..HEAD``
        # default -- i.e. restore the original proposal's behaviour,
        # which the revision overturned.  Red.
        #
        # A bare ``rc == 2`` assertion is NOT enough and this was
        # verified: a shallow fixture repo makes ``HEAD~20`` unresolvable,
        # so the perturbed build still exits 2 for an unrelated reason.
        # The node therefore asserts that argparse's own
        # required-positional error is what fired.
        assert tl.main(["--root", str(repo)]) == 2
        assert "required" in capsys.readouterr().err

    def test_census_prints_on_a_clean_run(
        self, tl: ModuleType, repo: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        # A13.  Perturbation: guard the census print behind ``if
        # findings:``.  Red -- a zero-finding run must be positive
        # evidence, not silence.
        _write(repo, "dev/plans/x.md", "# x\n")
        _commit(repo, "dev/plans: x -- seed")
        _write(repo, "dev/plans/x.md", "# x\n\ntidied\n")
        _commit(repo, "dev/plans: x -- tidy wording")
        assert tl.main([_last(repo), "--root", str(repo)]) == 0
        assert "scanned 1 commits, 1 triggered, 0 findings" in capsys.readouterr().out

    def test_empty_range_is_clean_and_zero(
        self, tl: ModuleType, repo: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        # A20.  Perturbation: make ``scan`` raise on an empty commit
        # list.  Red.
        assert tl.main(["HEAD..HEAD", "--root", str(repo)]) == 0
        assert "scanned 0 commits, 0 triggered, 0 findings" in capsys.readouterr().out


class TestNarrowing:
    """AC-R2 and AC-R3: what the tool will and will not look at."""

    def test_a_rename_into_archive_never_triggers(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # A14.  Traced to b064576, the tree's only supersession.
        # Perturbation: delete ``_EXCLUDE_SUBSTRING``.  Red.
        #
        # The fixture reproduces b064576's *real* shape -- the Decision
        # is appended in the same commit as the move, so similarity is
        # under 100% and the commit enumerates ``D`` + ``A .../archive/``
        # rather than ``R``.  Verified at implementation: a byte-identical
        # ``git mv`` enumerates ``R100``, rename-detection alone
        # suppresses it, and deleting ``_EXCLUDE_SUBSTRING`` leaves such a
        # fixture GREEN -- proving nothing.  This shape makes the archive
        # exclusion the only thing standing between the move and the
        # trigger set.
        body = "# thing\n\n**Status**: proposed\n\n" + "prose\n" * 30
        _write(repo, "dev/proposals/thing.md", body)
        _commit(repo, "dev/proposals: open thing")
        (repo / "dev/proposals/archive").mkdir(parents=True, exist_ok=True)
        _git(repo, "mv", "dev/proposals/thing.md",
             "dev/proposals/archive/thing.md")
        _write(repo, "dev/proposals/archive/thing.md",
               body + "\n## Decision -- Maintainer -- 2026-01-01\n\nSuperseded.\n")
        _commit(repo, "dev/proposals: Maintainer Decision -- SUPERSEDE thing")
        entries = tl._entries(repo, _git(repo, "rev-parse", "HEAD"))
        assert sorted(entries) == [
            ("A", "dev/proposals/archive/thing.md"),
            ("D", "dev/proposals/thing.md"),
        ]
        scanned, triggered, _ = tl.scan(_last(repo), repo, whitelist={})
        assert (scanned, triggered) == (1, 0)

    def test_a_plan_open_triggers_but_the_archived_proposal_does_not(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # A15.  Traced to 5140e21 and 57d1daf.  The plan records this
        # row as a must-not-regress assertion that *cannot* be made red,
        # because the bare enumeration's ``A dev/proposals/archive/...``
        # is still caught by ``_EXCLUDE_SUBSTRING``.  That is true of the
        # trigger-set assertion alone and was re-verified at
        # implementation.  This node therefore also asserts the
        # *enumeration*: the archive move must arrive as an ``R`` entry.
        # With that conjunct the named perturbation (drop
        # ``--find-renames=100%``) IS red, so A15 pins the
        # rename-detection half of AC-R2 and A16 pins the ``100%``
        # threshold half.
        body = "# thing\n\n**Status**: proposed\n\nbody\n"
        _write(repo, "dev/proposals/thing.md", body)
        _commit(repo, "dev/proposals: open thing")
        (repo / "dev/proposals/archive").mkdir(parents=True, exist_ok=True)
        _git(repo, "mv", "dev/proposals/thing.md",
             "dev/proposals/archive/thing.md")
        _write(repo, "dev/plans/thing.md", "# plan\n\n**Status**: open\n")
        _commit(repo, "dev/plans: open thing")
        entries = tl._entries(repo, _git(repo, "rev-parse", "HEAD"))
        assert any(s.startswith("R") for s, _ in entries)
        triggers = tl._triggers(entries)
        assert triggers == [("A", "dev/plans/thing.md")]

    def test_a_proposal_derived_plan_is_not_absorbed_into_a_rename(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # A16.  **Explicitly synthetic** -- the one node in Chunks A-C
        # that traces to no real commit, and AC-R9 carves out exactly
        # this row.  Measured across 898 commits, ``-M`` and
        # ``--find-renames=100%`` produce identical trigger sets on
        # 898/898, so the hazard has zero corpus instances; the fixture
        # is engineered above git's 50% default threshold to show the
        # flag does what it claims.
        # Perturbation: replace ``--find-renames=100%`` with bare ``-M``.
        # Red -- the trigger set becomes empty.
        source = "".join(f"line {n}\n" for n in range(200))
        _write(repo, "dev/proposals/p.md", source)
        _commit(repo, "dev/proposals: seed p")
        (repo / "dev/proposals/p.md").unlink()
        _write(repo, "dev/plans/q.md", source + "one appended line\n")
        _commit(repo, "dev/plans: derive q from p")
        triggers = tl._triggers(tl._entries(repo, _git(repo, "rev-parse", "HEAD")))
        assert triggers == [("A", "dev/plans/q.md")]

    def test_a_commit_with_no_lifecycle_A_or_M_never_triggers(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # A17.  Traced to 18707e9 / d0ba903 / ebb1d6e (the dev/strategy/
        # carve-in) and the goodnight-handoff shape.  Perturbation: add
        # ``dev/strategy/`` to ``_TRIGGER_ROOTS``.  Red.  This is AC-R3:
        # the *narrowing* discharges the approval carve-in, so the tool
        # needs no exception vocabulary.
        _write(repo, "dev/strategy/note.md", "# note\n")
        _commit(repo, "dev/strategy: open a note -- review, Decision")
        scanned, triggered, _ = tl.scan(_last(repo), repo, whitelist={})
        assert (scanned, triggered) == (1, 0)

        _write(repo, "dev/PLANNING.md", "board\n")
        _write(repo, "CHANGELOG.md", "log\n")
        _write(repo, "dev/NEXT_SESSION.md", "handoff\n")
        _commit(repo, "goodnight: handoff, open questions, Decision pending")
        scanned, triggered, _ = tl.scan(_last(repo), repo, whitelist={})
        assert (scanned, triggered) == (1, 0)


class TestScopeFence:
    """The bright line, asserted mechanically rather than in prose."""

    def test_the_tool_ships_no_exception_vocabulary(self, tl_src: str) -> None:
        # A18.  Perturbation: add a ``# transition-lint: skip`` opt-out
        # branch.  Red.  The assertion matches a directive *shape*, not
        # bare tokens -- a bare-substring rule would go red on the
        # module's own required prose ("the commit is passed over", the
        # "Exemption model" heading) and the pressure would be to relax
        # it until it asserted nothing.
        assert re.search(r"#\s*transition-lint:\s*\w+", tl_src) is None

        tree = ast.parse(tl_src)
        banned = ("skip", "exempt", "ignore", "no-lint")
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not (isinstance(func, ast.Attribute) and func.attr == "add_argument"):
                continue
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    low = arg.value.lower()
                    assert not any(b in low for b in banned), arg.value

        # No git argument vector reads the commit body or git notes.
        for vector in _git_vectors(tree):
            for token in vector:
                assert "%b" not in token, token
                assert token != "notes", token

    def test_no_import_crosses_the_scripts_templates_boundary(
        self, tl_src: str,
    ) -> None:
        # A19.  Perturbation: add an import of the intent module's
        # rename helper from ``templates/``.  Red.  The ``-z`` walk is
        # copied, never imported, because importing would couple a
        # repo-local script to a byte-frozen shipped file.
        tree = ast.parse(tl_src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.split(".")[0] == "templates", alias.name
            elif isinstance(node, ast.ImportFrom):
                assert not (node.module or "").split(".")[0] == "templates"
            elif isinstance(node, ast.Attribute):
                assert not (
                    node.attr in ("insert", "append")
                    and isinstance(node.value, ast.Attribute)
                    and node.value.attr == "path"
                ), "sys.path mutation"
        # No call argument names a path under templates/.
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            for arg in list(node.args) + [k.value for k in node.keywords]:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    assert "templates" not in arg.value, arg.value


def _git_vectors(tree: ast.AST) -> list[list[str]]:
    """Every string argument vector handed to git in the module."""
    vectors: list[list[str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.List) and node.elts:
            first = node.elts[0]
            if isinstance(first, ast.Constant) and first.value == "git":
                vectors.append([
                    e.value for e in node.elts
                    if isinstance(e, ast.Constant) and isinstance(e.value, str)
                ])
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "_git":
                vectors.append([
                    a.value for a in node.args
                    if isinstance(a, ast.Constant) and isinstance(a.value, str)
                ])
    return vectors


# ---------------------------------------------------------------------------
# Chunk B -- shape (a): the message claims a transition the diff lacks
# ---------------------------------------------------------------------------

_HEADER = "# p\n\n**Status**: open\n\nbody\n\n"


def _seed(repo: Path, rel: str, tail: str, subject: str) -> str:
    """Seed *rel* with ``_HEADER + tail`` and return the base rev."""
    _write(repo, rel, _HEADER + tail)
    _commit(repo, subject)
    return _git(repo, "rev-parse", "HEAD")


class TestShapeA:
    """AC-R4: the heuristics, re-pinned against the real corpus."""

    def test_case_insensitive_subjects_produce_the_same_finding(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # B7.  Perturbation: drop ``re.IGNORECASE`` from ``_CLAIM_RES``.
        # Red -- the uppercase fixture stops flagging.  The dogfood
        # cannot catch this: a case-sensitive build also scores zero
        # false positives, it just produces silent false negatives that
        # look like passes.  That is why this is a test, not a corpus row.
        base = _seed(repo, "dev/plans/p.md", "more\n", "dev/plans: p -- seed")
        _write(repo, "dev/plans/p.md", _HEADER + "more\nagain\n")
        _commit(repo, "dev/plans: p -- add gemini external review")
        _write(repo, "dev/plans/p.md", _HEADER + "more\nagain\nthird\n")
        _commit(repo, "dev/plans: p -- ADD GEMINI EXTERNAL REVIEW")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert len(findings) == 2
        assert len({(f.shape, f.message) for f in findings}) == 1

    def test_a_review_claim_with_no_added_body_flags(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # B8.  Reproduces f4a8308.  Perturbation: lower
        # ``_MIN_EVIDENCE_LINES`` from 3 to 0, i.e. accept
        # heading-presence.  Red -- the seeded placeholder counts.
        tail = "## Review -- Reviewer -- 2026-01-01\n\n(Awaiting the review.)\n"
        base = _seed(repo, "dev/proposals/p.md", tail, "dev/proposals: open p")
        _write(repo, "dev/proposals/p.md",
               "<!-- marker one -->\n<!-- marker two -->\n" + _HEADER + tail)
        _commit(repo, "dev/proposals: add Gemini External Review for p")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert [(f.shape, f.file) for f in findings] == [
            ("a", "dev/proposals/p.md"),
        ]

    def test_a_genuine_review_append_does_not_flag(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # B9.  Reproduces 3ae1d47 -> e31625c: an open commit seeds a
        # titled review section, then the review commit replaces the
        # placeholder body and adds **no** ``+## Review`` line.
        # Perturbation: require an added ``+## <kind>`` heading line.
        # Red -- the honest commit flags.  Run with B8: the pair is what
        # kills the naive heading rule.
        head = "## Review -- Reviewer -- 2026-01-01\n\n"
        base = _seed(repo, "dev/proposals/p.md", head + "(Awaiting.)\n",
                     "dev/proposals: open p")
        body = "".join(f"finding line {n}\n" for n in range(20))
        _write(repo, "dev/proposals/p.md", _HEADER + head + body)
        _commit(repo, "dev/proposals: add Internal Review for p")
        assert _git(repo, "show", "--format=", "--unified=0", "HEAD").count(
            "\n+## Review") == 0
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert findings == []

    def test_hyphen_compounds_do_not_claim(self, tl: ModuleType) -> None:
        # B10.  Traced to 2432f10.  Perturbation: replace the lookarounds
        # with a bare ``re.search("review")``.  Red -- all three claim.
        rules = tl.Rules()
        for subject in (
            "dev/plans: review-record-integrity -- Sharpening",
            "dev/proposals: automated-review-committer -- open",
            "dev/measurement: review-floor deviations",
        ):
            assert tl._claim(subject, rules) is None, subject
        # And the both-directions half: the bare word still claims.
        assert tl._claim("dev/plans: p -- add External review", rules) == "review"

    def test_open_is_positionally_anchored(self, tl: ModuleType) -> None:
        # B11.  The three subjects the Internal panel constructed.
        # Perturbation: remove the positional anchor, matching ``open``
        # anywhere.  Red on the first two.  (The plan says "all three";
        # measured, the third cannot go red under any anchoring, because
        # ``opening`` is not a token and ``open`` + optional ``s`` does
        # not match it.  The node is red under the perturbation
        # regardless -- recorded so the claim is not inherited.)
        rules = tl.Rules()
        for subject in (
            "dev/proposals: transition-lint -- resolve open questions "
            "from the Internal review",
            "dev/plans: X -- close out the open acceptance criteria",
            "dev/plans: transition-lint -- opening sequence step 1",
        ):
            assert tl._claim(subject, rules) != "open", subject
        # Both directions: a real open subject must still claim.
        assert tl._claim("dev/plans: open planner-line-semantics", rules) == "open"

    def test_a_security_review_section_counts_as_review_evidence(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # B12.  FP-1, traced to cc8a25d, d0102a6, 3da58c1.  Perturbation:
        # revert ``_heading_kind``'s exclusive branch to the three-prefix
        # ``startswith``.  Red -- the section becomes invisible and the
        # honest commit flags.
        head = "## Security Review -- Reviewer -- 2026-01-01\n\n"
        base = _seed(repo, "dev/plans/p.md", head + "(pending)\n",
                     "dev/plans: p -- seed")
        body = "".join(f"security finding {n}\n" for n in range(6))
        _write(repo, "dev/plans/p.md", _HEADER + head + body)
        _commit(repo, "dev/plans: p -- Add dedicated trust-root Security Review")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert findings == []

    def test_an_h3_response_inside_a_plan_review_counts_as_response_evidence(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # B13.  FP-2, traced to 31c40a0, 8900e46, 8abd453, 8d876e0,
        # eb4ec16, ce8e20e, e953095.  Perturbation: restrict
        # ``_section_spans`` to h2.  Red -- the response body then falls
        # inside the ``## Plan review`` span with no ``## Response`` h2
        # present.  The fixture deliberately reproduces the *pre*-
        # 2026-08-03 plan shape (h3 response, no ``## Response`` h2):
        # building it from a current plan would hand the test an h2 that
        # satisfies even the un-widened rule, and it would pass under both.
        head = ("## Plan review -- Reviewer -- 2026-01-01\n\n[R1] a finding\n\n"
                "### Response -- Author -- 2026-01-02\n\n")
        base = _seed(repo, "dev/plans/p.md", head + "(pending)\n",
                     "dev/plans: p -- seed")
        body = "".join(f"disposition {n}\n" for n in range(30))
        _write(repo, "dev/plans/p.md", _HEADER + head + body)
        _commit(repo, "dev/plans: p -- Response to External review")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert findings == []

    def test_respond_to_a_review_is_not_a_review_claim(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # B14.  FP-4, traced to 283be88 and to that commit only.  The
        # plan offers two candidate fixes and leaves the choice to the
        # plan review; this ships the first (``respond`` as a *response*
        # token), because it is native to leftmost-wins and does not
        # interact with B3's exclusive kind-match.  Perturbation: delete
        # the ``("respond", "response")`` entry.  Red -- the subject then
        # claims *review*, finds no review section, and flags.
        head = "## Response -- Author -- 2026-01-01\n\n"
        base = _seed(repo, "dev/plans/p.md", head + "(pending)\n",
                     "dev/plans: p -- seed")
        body = "".join(f"disposition {n}\n" for n in range(6))
        _write(repo, "dev/plans/p.md", _HEADER + head + body)
        _commit(repo, "portable-security-sweeps: respond to External security review")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert findings == []


# ---------------------------------------------------------------------------
# Chunk C -- shape (b): an open commit whose added file carries a review
# ---------------------------------------------------------------------------

#: Cairn's own history, pinned by full SHA.  Every corpus-tier range is
#: ``<40-hex>..<40-hex>`` or ``<40-hex>~1..<40-hex>``: a HEAD-relative
#: range is not a window, and this plan shipped one once already.
ROOT_SHA = "0f1fc68f48ab734ae1f619aeb0454c84c6fbace3"
SELF_HOST_SHA = "d6646a37a6166a4d7b65f326cb689d716617a798"
PROPOSAL_SHA = "57d1dafe7ca5b17e74a148b0d95e7b69ed79f939"
SNAPSHOT_SHA = "8f47c76618f65ff34e22f32c4d5de30c0c88c110"
REVIEW_APPEND_SHA = "e31625cdb4263e19f55b67834019d67170b1e3ab"
INCIDENT_SHA = "17b7e5c6b51fb1ad145921196f930f2a2137504e"
EMPTY_REVIEW_SHA = "f4a8308dedf4055d53d3a6f22867b64e7fbc1740"
SUPERSEDE_SHA = "b0645769e963e846b43e2bd9a662f8de4ea15967"
PLAN_ARCHIVE_SHA = "d789414f1bf975a3235ce7a1d1ed5bc6f21b8191"

_PINNED_SHAS = (
    ROOT_SHA, SELF_HOST_SHA, PROPOSAL_SHA, SNAPSHOT_SHA, REVIEW_APPEND_SHA,
    INCIDENT_SHA, EMPTY_REVIEW_SHA, SUPERSEDE_SHA, PLAN_ARCHIVE_SHA,
)


def _corpus_available() -> bool:
    """Cairn's own history, or not.

    The corpus tier **skips, never fails**, when it is absent: a history
    rewrite must not redden the suite for a reason unrelated to the code.
    """
    if not (REPO_ROOT / ".git").exists():
        return False
    for sha in _PINNED_SHAS:
        out = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", sha + "^{commit}"],
            cwd=str(REPO_ROOT), capture_output=True,
        )
        if out.returncode != 0:
            return False
    return True


requires_corpus = pytest.mark.skipif(
    not _corpus_available(), reason="Cairn's own history is not present",
)

#: The heuristics exactly as the accepted proposal pinned them.
PINNED_RULES = dict(
    h3_spans=False, exclusive_kind=False, respond_token=False,
    dated_heading=False,
)


class TestShapeB:
    """The chunk that reproduces the original incident."""

    def test_an_open_commit_with_a_baked_in_review_flags_once_per_section(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # C4.  Reproduces 17b7e5c.  The plan's named perturbation --
        # delete the grammar-marker check -- is a *widening*, so it
        # cannot redden a node that asserts a finding IS produced; run at
        # implementation, it leaves C4 green (and reddens C5, which is
        # the point of the pair).  C4's own single-property falsifiers,
        # both RUN and red: `break` after the first section (one Finding
        # per commit instead of per section -- this is what C3 pins), and
        # removing the `_shape_b` call from `scan`.
        base = _git(repo, "rev-parse", "HEAD")
        _write(repo, "dev/proposals/p.md", _HEADER.replace("open", "proposed")
               + "## Review -- Internal -- 2026-01-01\n\n[R1] a finding\n\n"
               + "## Review -- External -- 2026-01-02\n\n[E1] another\n")
        _commit(repo, "dev/proposals: open p")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert [f.shape for f in findings] == ["b", "b"]
        assert len({f.message for f in findings}) == 2

    def test_a_seeded_placeholder_review_at_open_does_not_flag(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # C5.  Reproduces 3ae1d47.  Perturbation: delete the
        # grammar-marker check, accepting any non-empty section.  Red.
        base = _git(repo, "rev-parse", "HEAD")
        _write(repo, "dev/proposals/p.md", _HEADER.replace("open", "proposed")
               + "## Review -- Reviewer -- 2026-01-01\n\n"
               + "(Awaiting the Internal review.)\n")
        _commit(repo, "dev/proposals: open p")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert findings == []

    def test_a_baked_in_plan_review_at_plan_open_flags(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # C6.  Perturbation: revert ``_OPEN_STATUSES`` to ``proposed``
        # only -- the original proposal's rule.  No plan ever carries
        # ``proposed``, so the exact analogue of the 17b7e5c incident
        # becomes undetectable.  Red.  Run with C10: C6 asserts a
        # genuinely baked-in *dated* plan review still flags, so the pair
        # distinguishes "the conjunct discriminates" from "the conjunct
        # disabled shape (b) on plans".
        base = _git(repo, "rev-parse", "HEAD")
        _write(repo, "dev/plans/p.md",
               "# p\n\n**Status**: awaiting-plan-review\n\n"
               "## Plan review -- Reviewer -- 2026-01-01\n\n[E1] a finding\n")
        _commit(repo, "dev/plans: open p")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert [(f.shape, f.file) for f in findings] == [("b", "dev/plans/p.md")]

    def test_a_placeholder_plan_review_at_plan_open_does_not_flag(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # C7.  Reproduces 5140e21 / 57d1daf.  Perturbation: delete the
        # marker check.  Red -- and this is the false positive C6's
        # widening would otherwise buy, so C6/C7 is the second
        # discriminating pair.
        base = _git(repo, "rev-parse", "HEAD")
        _write(repo, "dev/plans/p.md",
               "# p\n\n**Status**: awaiting-plan-review\n\n"
               "## Plan review -- 2026-01-01\n\n(Awaiting.)\n\n"
               "## Code review -- 2026-01-01\n\n(Awaiting.)\n")
        _commit(repo, "dev/plans: open p")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert findings == []

    def test_a_status_beyond_the_header_bound_is_not_read(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # C8.  Asserted in **both directions**: a bound test that only
        # ever asserts silence cannot distinguish "bounded correctly"
        # from "never fires".  Perturbation: raise ``_HEADER_BOUND`` to
        # the whole file.  Red on the first half.
        review = "## Review -- Reviewer -- 2026-01-01\n\n[R1] a finding\n"
        deep = "filler\n" * 79 + "**Status**: proposed\n\n" + review
        base = _git(repo, "rev-parse", "HEAD")
        _write(repo, "dev/proposals/deep.md", deep)
        _commit(repo, "dev/proposals: open deep")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert findings == []

        shallow = "filler\n" * 30 + "**Status**: proposed\n\n" + review
        base = _git(repo, "rev-parse", "HEAD")
        _write(repo, "dev/proposals/shallow.md", shallow)
        _commit(repo, "dev/proposals: open shallow")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert [f.shape for f in findings] == ["b"]

    def test_a_template_file_is_never_examined(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # C9.  Perturbation: delete ``_EXCLUDE_BASENAME``.  Red.  The
        # honest accounting: the *real* dev/proposals/_template.md
        # carries `**Status**: proposed` at line 123 and its review
        # heading at line 313 (7 grammar-marker instances, verified
        # 2026-08-04), so the 60-line header bound already excludes it
        # and the basename rule is defence in depth.  This fixture
        # deliberately puts the status inside the bound and dates the
        # heading, so the basename exclusion is the only thing standing
        # between the template and a finding.
        base = _git(repo, "rev-parse", "HEAD")
        _write(repo, "dev/proposals/_template.md",
               "# {{title}}\n\n**Status**: proposed\n\n"
               "## Review -- {{reviewer}} -- 2026-01-01\n\n[R1] {{finding}}\n")
        _commit(repo, "dev/proposals: refresh the template")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert findings == []

    def test_a_reviewer_brief_at_plan_open_does_not_flag(
        self, tl: ModuleType, repo: Path,
    ) -> None:
        # C10.  Reproduces 000e480, the shape-(b) false positive the
        # Internal plan review found by running rather than reading.
        # Perturbation: delete C2's dated-heading conjunct.  Red -- the
        # brief's [E1] then reads as a baked-in review.
        base = _git(repo, "rev-parse", "HEAD")
        _write(repo, "dev/plans/p.md",
               "# p\n\n" + "meta\n" * 8 + "**Status**: open\n\n"
               "## Plan review -- the brief, and why the tier is not discharged\n\n"
               "The round must engage [E1] before returning a recommendation.\n")
        _commit(repo, "dev/plans: open planner-line-semantics")
        _, _, findings = tl.scan(f"{base}..HEAD", repo, whitelist={})
        assert findings == []


@requires_corpus
class TestWideningIsNotCreating:
    """AC-R4 / the withdrawn one-directional claim, re-tested honestly.

    Both nodes quantify over a **corpus window**, never over this plan's
    own fixtures.  The old specification quantified over "every fixture
    in Chunks A-C" -- the author's own demonstration set -- and
    structurally could not contain the counterexample, which lives in the
    tree.  A property test whose domain is the author's examples is a
    green light, not a pin.
    """

    def test_the_evidence_widening_does_not_create_a_finding_over_the_corpus(
        self, tl: ModuleType,
    ) -> None:
        # B15.  Perturbations, both RUN and red: (1) delete C2's
        # dated-heading conjunct -- fd6be5a appears and the subset
        # property fails; (2) make an h3 truncate the enclosing h2 span
        # instead of adding beside it -- 16 new shape-(a) findings appear.
        window = f"{PROPOSAL_SHA}..{SNAPSHOT_SHA}"
        _, _, pinned = tl.scan(
            window, REPO_ROOT, whitelist={}, rules=tl.Rules(**PINNED_RULES),
        )
        _, _, shipped = tl.scan(window, REPO_ROOT, whitelist={})
        assert len(pinned) == 20
        assert len(shipped) == 10
        assert {(f.sha, f.shape, f.file) for f in shipped} <= {
            (f.sha, f.shape, f.file) for f in pinned
        }

    def test_the_span_widening_cannot_manufacture_a_shape_b_finding(
        self, tl: ModuleType,
    ) -> None:
        # C11.  Perturbation: delete C2's dated-heading conjunct and
        # re-run -- fd6be5a and the plan's own plan-open 6a88501 appear
        # as shape-(b) findings the un-widened rule does not produce.
        # Deliberately a **corpus** assertion, not a fixture one.
        window = f"{ROOT_SHA}..{SNAPSHOT_SHA}"
        _, _, pinned = tl.scan(
            window, REPO_ROOT, whitelist={}, rules=tl.Rules(**PINNED_RULES),
        )
        _, _, shipped = tl.scan(window, REPO_ROOT, whitelist={})
        pinned_b = {(f.sha, f.file, f.message) for f in pinned if f.shape == "b"}
        shipped_b = {(f.sha, f.file, f.message) for f in shipped if f.shape == "b"}
        assert len(pinned_b) == 2
        assert {sha for sha, _, _ in pinned_b} == {INCIDENT_SHA}
        assert shipped_b == pinned_b


# ---------------------------------------------------------------------------
# Chunk D -- the suppression whitelist, and its side-door hygiene
# ---------------------------------------------------------------------------

#: The window the whitelist is measured against.
PINNED_WINDOW = f"{SELF_HOST_SHA}..{PROPOSAL_SHA}"


@requires_corpus
class TestWhitelistHygiene:
    """Modelled on `scan-coverage`'s `_SCAN_EXCLUSIONS` guards.

    A whitelist is a fail-open side-door: it can only ever *hide* a
    finding, so every guard here is about the door not widening quietly.
    """

    def test_every_whitelist_entry_has_a_nonempty_rationale(
        self, tl: ModuleType,
    ) -> None:
        # D5.  Perturbation: add `{"<a real sha>": ""}`.  Red.
        assert tl.WHITELIST
        for sha, reason in tl.WHITELIST.items():
            assert isinstance(reason, str) and reason.strip(), sha

    def test_every_whitelist_entry_is_a_full_40_char_sha_that_resolves(
        self, tl: ModuleType,
    ) -> None:
        # D6.  Perturbation: add a plausible-looking but non-resolving
        # SHA.  Red.  Catches a typo'd or rebased-away entry, which is
        # how a suppression silently widens.
        for sha in tl.WHITELIST:
            assert re.fullmatch(r"[0-9a-f]{40}", sha), sha
            out = subprocess.run(
                ["git", "rev-parse", "--verify", "--quiet", sha + "^{commit}"],
                cwd=str(REPO_ROOT), capture_output=True,
            )
            assert out.returncode == 0, sha

    def test_no_whitelist_entry_is_stale(self, tl: ModuleType) -> None:
        # D7.  Perturbation: add an entry for a benign in-window SHA that
        # flags nothing.  Red.  **This is the "stale entries must trip
        # the suite" guard** -- an entry suppressing nothing is a latch
        # waiting to absorb a future regression on that commit.  It is
        # the direct analogue of scan-coverage's C3(e), and like C3(e) it
        # does **not** follow from D5/D6: an entry can have a rationale
        # and resolve and still suppress nothing.
        _, _, findings = tl.scan(PINNED_WINDOW, REPO_ROOT, whitelist={})
        flagged = {f.sha for f in findings}
        for sha in tl.WHITELIST:
            assert sha in flagged, f"{sha} suppresses nothing in {PINNED_WINDOW}"

    def test_the_whitelist_suppresses_and_the_bypass_restores(
        self, tl: ModuleType,
    ) -> None:
        # D8.  Both directions must be run -- a suppression test that
        # only checks silence cannot tell suppression from breakage.
        # Perturbations, both RUN: make `scan` ignore the whitelist
        # argument (red in the first direction); make it ignore the
        # bypass (red in the second).
        _, _, suppressed = tl.scan(PINNED_WINDOW, REPO_ROOT)
        assert suppressed == []
        _, _, bypassed = tl.scan(PINNED_WINDOW, REPO_ROOT, whitelist={})
        assert len(bypassed) == 3
        assert {f.sha for f in bypassed} == {INCIDENT_SHA, EMPTY_REVIEW_SHA}

    def test_a_whitelist_entry_cannot_suppress_a_different_commit(
        self, tl: ModuleType,
    ) -> None:
        # D9.  Perturbation: make the suppression check `if suppressed:`
        # -- i.e. any entry silences every commit.  Red.
        #
        # The plan names a different perturbation ("key the suppression
        # on the abbreviated SHA prefix instead of the full 40").  Run at
        # implementation, that one leaves this node GREEN: the keys are
        # full 40-hex and no two of Cairn's commits share a 7-character
        # prefix, so prefix-keying is behaviourally identical here.  The
        # over-broad mutation above is the reachable falsifier for the
        # same property, and it is the one that was run.
        one = {INCIDENT_SHA: "incident only"}
        _, _, findings = tl.scan(PINNED_WINDOW, REPO_ROOT, whitelist=one)
        assert [f.sha for f in findings] == [EMPTY_REVIEW_SHA]

        unrelated = {ROOT_SHA: "the root commit, which flags nothing"}
        _, _, findings = tl.scan(PINNED_WINDOW, REPO_ROOT, whitelist=unrelated)
        assert len(findings) == 3


# ---------------------------------------------------------------------------
# Chunk E -- the corpus-regression tier
# ---------------------------------------------------------------------------


@requires_corpus
class TestCorpusRegression:
    """AC-R4 and AC-R9, landing together.

    Cairn-repo-only and **self-skipping**: the guard above skips, never
    fails, if the root is not a git work tree or if any pinned SHA does
    not resolve, because a history rewrite must not redden the suite for
    a reason unrelated to the code.  Every figure below was re-derived
    from the **committed** script, not from a scratch prototype.
    """

    def test_window_one_reproduces_the_pinned_findings(
        self, tl: ModuleType,
    ) -> None:
        # E2.  The window the accepted proposal pinned, reproduced to the
        # digit nine months later -- the payoff for SHA-pinning it.
        # Perturbation, RUN: repoint at `<self-host>..HEAD`; it fails on
        # the scanned count, proving this node pins a *window* and not
        # merely a finding set.
        scanned, triggered, findings = tl.scan(
            PINNED_WINDOW, REPO_ROOT, whitelist={},
        )
        assert (scanned, triggered) == (120, 52)
        assert {(f.sha, f.shape) for f in findings} == {
            (INCIDENT_SHA, "b"), (EMPTY_REVIEW_SHA, "a"),
        }
        assert len([f for f in findings if f.sha == INCIDENT_SHA]) == 2

    def test_window_two_is_clean(self, tl: ModuleType) -> None:
        # E3.  The must-not-flag set is asserted **by construction** --
        # zero findings over a window containing all the named SHAs --
        # rather than by twenty separate lookups.
        scanned, triggered, findings = tl.scan(
            f"{REVIEW_APPEND_SHA}~1..{PROPOSAL_SHA}", REPO_ROOT, whitelist={},
        )
        assert (scanned, triggered, findings) == (45, 41, [])

    def test_the_archive_moves_are_never_examined(self, tl: ModuleType) -> None:
        # E4.  Must-SKIP, not must-not-flag.  A correction the plan
        # carries and this node re-verified: the accepted proposal
        # justifies this by quoting `-M` enumeration as a single `R091`
        # line, but under the pinned `--find-renames=100%` both commits
        # enumerate `D` + `A .../archive/...` -- 91% similarity is below
        # the threshold, because the Decision was appended in the same
        # commit.  The conclusion survives; **the mechanism is the
        # `/archive/` exclusion, not rename-blindness.**
        for sha in (SUPERSEDE_SHA, PLAN_ARCHIVE_SHA):
            entries = tl._entries(REPO_ROOT, sha)
            assert not any(s.startswith("R") for s, _ in entries), sha
            scanned, triggered, findings = tl.scan(
                f"{sha}~1..{sha}", REPO_ROOT, whitelist={},
            )
            assert (scanned, triggered, findings) == (1, 0, []), sha

    def test_window_three_pins_the_post_proposal_drift(
        self, tl: ModuleType,
    ) -> None:
        # E5.  SHA-pinned at **both** ends.  The plan shipped
        # `<proposal>..HEAD` here once, which three of its own criteria
        # forbid; measured, that range moved 332 -> 333 -> 335 -> 363
        # across four commits in two days.  A node asserting
        # `scanned == N` over a moving range is red on the next commit by
        # anyone.  Perturbation, RUN: repoint at `<proposal>..HEAD` --
        # fails on the scanned count.
        #
        # The number to beat is **not 0**: the residue is FP-3 (the
        # `accept` token, 5), FP-5 (2), FP-6 (2) and one FP-2 residue,
        # and all four classes are routed to the Maintainer fence rather
        # than fixed here.
        window = f"{PROPOSAL_SHA}..{SNAPSHOT_SHA}"
        scanned, triggered, shipped = tl.scan(window, REPO_ROOT, whitelist={})
        assert (scanned, triggered) == (332, 265)
        assert len(shipped) == 10
        _, _, pinned = tl.scan(
            window, REPO_ROOT, whitelist={}, rules=tl.Rules(**PINNED_RULES),
        )
        assert len(pinned) == 20


class TestSourceLevelBans:
    """Three separate criteria forbade a HEAD-relative corpus range and
    the plan shipped one anyway.  That is the argument for making the ban
    mechanical instead of repeated."""

    def test_no_corpus_node_carries_a_head_relative_range(self) -> None:
        # Perturbation: reintroduce `<proposal>..HEAD` anywhere inside a
        # corpus-tier class.  Red.
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        checked = 0
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            if not any(
                isinstance(d, ast.Name) and d.id == "requires_corpus"
                for d in node.decorator_list
            ):
                continue
            checked += 1
            for inner in ast.walk(node):
                if isinstance(inner, ast.Constant) and isinstance(inner.value, str):
                    assert "HEAD" not in inner.value, (node.name, inner.value)
        assert checked >= 3

    def test_every_pinned_sha_constant_is_a_full_40_hex(self) -> None:
        # The other half: a range built from abbreviated SHAs is not
        # pinned either.  Perturbation: abbreviate one constant.  Red.
        for name, value in globals().items():
            if name.endswith("_SHA") and isinstance(value, str):
                assert re.fullmatch(r"[0-9a-f]{40}", value), name
