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
