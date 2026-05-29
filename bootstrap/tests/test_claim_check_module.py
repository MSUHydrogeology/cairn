"""Direct unit coverage for the ``claim_check.py`` module's
document-scoped exemption directives.

Ported from modflow_tools' ``tests/unit/test_claim_check.py`` (the
reference implementation's adopter-side coverage) into Cairn at chunk 1
of the ``cairn-0.2.x-sweep-and-ledger-followups`` plan, where the
allow-directive family was ported into Cairn (commit pending).

Covers:

* ``claim-check-allow`` path-exemption directive -- R1 narrow-glob
  validation (the ``allow_glob_error`` rules), R2 exact-token reporting,
  matching vs. non-matching behavior, the "local-line-bounds not
  silenced" boundary, prose-shown-not-parsed.
* ``claim-check-allow-count`` count-exemption directive -- exact-token
  matching, normalization, multi-token directives, prose-shown-not-
  parsed, ``--fail-on-soft`` clean when exempted.
* The corresponding ``CheckResult.exempted`` / ``exempted_counts``
  fields and the stdout-side audit lines from ``main``.

The tests load the source module via the same ``_load_script`` import
helper the install-side tests use (see ``test_reference_scripts.py``);
that keeps the unit tests honest about the *shipped* file, not a
re-implementation.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_claim_check_module.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
CLAIM_CHECK_SRC = (
    CAIRN_ROOT / "templates" / "modules" / "default-on" / "claim_check.py"
)

pytestmark = pytest.mark.skipif(
    not CLAIM_CHECK_SRC.exists(),
    reason="Cairn claim_check template not available",
)


def _load_claim_check(name: str = "_cairn_claim_check_under_test") -> ModuleType:
    """Import the source ``claim_check.py`` template by file path.

    Registers the module in ``sys.modules`` before ``exec_module`` so its
    ``@dataclass`` definitions resolve (the documented
    spec_from_file_location gotcha).  See the parallel helper in
    ``test_reference_scripts.py``.
    """
    spec = importlib.util.spec_from_file_location(name, CLAIM_CHECK_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def cc() -> ModuleType:
    return _load_claim_check()


def _make_repo(root: Path) -> Path:
    """Build a synthetic repo: root files + a dev/ proposal tree.

    Mirrors the modflow_tools-side ``_make_repo`` so ported tests use
    identical fixtures.
    """
    (root / "AGENTS.md").write_text(
        "\n".join(f"line {n}" for n in range(1, 11))
    )
    (root / "CLAUDE.md").write_text("claude instructions\n")
    (root / "dev" / "proposals").mkdir(parents=True)
    (root / "dev" / "proposals" / "real.md").write_text(
        "# a real proposal\n"
    )
    (root / "tests" / "unit").mkdir(parents=True)
    (root / "examples").mkdir()
    return root


# ---------------------------------------------------------------------------
# R1 -- ``claim-check-allow`` globs must be narrow.
# ---------------------------------------------------------------------------


class TestAllowGlobValidation:
    """R1 -- a wildcard must be preceded by >= 2 literal path segments
    (or the glob must be fully literal), so a directive cannot exempt a
    whole top-level directory or everything; the final path segment
    must also carry a literal filename stem (no ``dir/sub/*``).
    """

    def test_whole_top_dir_glob_rejected(self, cc):
        assert cc.allow_glob_error("dev/*") is not None
        assert cc.allow_glob_error("scripts/*") is not None
        assert cc.allow_glob_error("dev/**") is not None

    def test_bare_wildcard_rejected(self, cc):
        assert cc.allow_glob_error("*") is not None
        assert cc.allow_glob_error("**") is not None

    def test_directory_wide_subtree_glob_rejected(self, cc):
        # A wildcard-leading final segment exempts a whole subtree
        # even with >= 2 literal segments -- refused.
        assert cc.allow_glob_error("dev/proposals/*") is not None
        assert cc.allow_glob_error("tests/unit/*") is not None
        assert cc.allow_glob_error("dev/proposals/*.md") is not None

    def test_filename_stem_globs_allowed(self, cc):
        # A literal filename stem in the final segment is specific.
        assert cc.allow_glob_error("dev/cairn*") is None
        assert cc.allow_glob_error("dev/cairn*.yml") is None
        assert cc.allow_glob_error("dev/.cairn/base*") is None

    def test_fully_literal_path_allowed(self, cc):
        assert cc.allow_glob_error("dev/cairn-lock.yml") is None

    def test_parse_multiple_globs_in_one_directive(self, cc):
        out = cc.parse_allow_directives(
            "<!-- claim-check-allow: dev/a/x, dev/b/y -->"
        )
        assert [g for _, g in out] == ["dev/a/x", "dev/b/y"]


# ---------------------------------------------------------------------------
# ``claim-check-allow`` -- document-scoped path exemption.
# ---------------------------------------------------------------------------


class TestClaimCheckAllowDirective:
    """Exempts matching would-be-hard path / line-bounds tokens
    document-wide (R1 narrow-glob validation, R2 exact-token report),
    without editing any append-only review block.
    """

    def test_directive_exempts_matching_token(self, cc, tmp_path):
        _make_repo(tmp_path)
        text = (
            "<!-- claim-check-allow: dev/cairn-lock.yml -->\n"
            "see `dev/cairn-lock.yml` here"
        )
        hard, _ = cc.check_text(text, tmp_path)
        assert hard == []

    def test_directive_records_exact_exemption(self, cc, tmp_path):
        # R2: the exempted token + matching glob are on the result.
        _make_repo(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text(
            "<!-- claim-check-allow: dev/cairn-lock.yml -->\n"
            "see `dev/cairn-lock.yml`"
        )
        result = cc.check_file(doc, tmp_path)
        assert result.hard_flags == []
        assert result.exempted == [
            ("dev/cairn-lock.yml", "dev/cairn-lock.yml")
        ]

    def test_filename_stem_glob_exempts_matching_token(self, cc, tmp_path):
        _make_repo(tmp_path)
        text = (
            "<!-- claim-check-allow: dev/.cairn/base* -->\n"
            "cache at `dev/.cairn/base/AGENTS.md`"
        )
        hard, _ = cc.check_text(text, tmp_path)
        assert hard == []

    def test_non_matching_token_still_flags(self, cc, tmp_path):
        # A valid (R1-clean) glob that does not match the cited token:
        # the unmatched broken path still hard-flags.
        _make_repo(tmp_path)
        text = (
            "<!-- claim-check-allow: dev/.cairn/base* -->\n"
            "see `dev/other-missing.md`"
        )
        hard, _ = cc.check_text(text, tmp_path)
        assert len(hard) == 1
        assert hard[0].token == "dev/other-missing.md"
        assert hard[0].kind == "path"

    def test_too_broad_glob_hard_flags_and_does_not_exempt(self, cc, tmp_path):
        # R1: `dev/*` is rejected -> a `directive` hard flag, AND the
        # path it would have exempted still hard-flags.
        _make_repo(tmp_path)
        text = (
            "<!-- claim-check-allow: dev/* -->\n"
            "see `dev/cairn-lock.yml`"
        )
        hard, _ = cc.check_text(text, tmp_path)
        kinds = sorted(f.kind for f in hard)
        assert kinds == ["directive", "path"]

    def test_exemption_reported_with_exact_token(
        self, cc, tmp_path, capsys
    ):
        # R2: main() names the exact exempted token in its output.
        _make_repo(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text(
            "<!-- claim-check-allow: dev/cairn-lock.yml -->\n"
            "see `dev/cairn-lock.yml`"
        )
        rc = cc.main([str(doc), "--root", str(tmp_path)])
        assert rc == 0  # exemptions are not flags
        # The exemption report is on STDOUT (the primary success
        # artifact), not stderr.
        out = capsys.readouterr().out
        assert "dev/cairn-lock.yml" in out
        assert "exempted" in out

    def test_no_directive_behaviour_unchanged(self, cc, tmp_path):
        _make_repo(tmp_path)
        hard, _ = cc.check_text("see `dev/cairn-lock.yml`", tmp_path)
        assert len(hard) == 1
        assert hard[0].kind == "path"

    def test_directive_does_not_silence_local_line_bounds(
        self, cc, tmp_path
    ):
        # A fully-literal directive for a real local file must NOT
        # exempt an out-of-range line citation -- that's the stale-
        # anchor class, not an unresolved-path problem.
        _make_repo(tmp_path)  # AGENTS.md has 10 lines
        text = (
            "<!-- claim-check-allow: AGENTS.md -->\nsee `AGENTS.md:9999`"
        )
        hard, _ = cc.check_text(text, tmp_path)
        assert len(hard) == 1
        assert hard[0].kind == "line-bounds"

    def test_directive_exempts_missing_file_line_citation(
        self, cc, tmp_path
    ):
        # The boundary's other side: a citation into a *non-existent*
        # file is an unresolved-path problem, so the directive may
        # exempt it.
        _make_repo(tmp_path)
        text = (
            "<!-- claim-check-allow: dev/gone.md -->\n"
            "stale `dev/gone.md:3`"
        )
        hard, _ = cc.check_text(text, tmp_path)
        assert hard == []

    def test_directive_shown_in_prose_is_not_parsed(self, cc, tmp_path):
        # Documentation that *shows* the directive (inside backticks /
        # a table cell) must not be parsed as a live directive -- only
        # a standalone HTML-comment line is.  Were it parsed, the
        # broad `dev/*` would raise a 'directive' hard flag.
        _make_repo(tmp_path)
        text = (
            "docs: use `<!-- claim-check-allow: dev/* -->` near the top."
        )
        hard, _ = cc.check_text(text, tmp_path)
        assert hard == []
        assert cc.parse_allow_directives(text) == []


# ---------------------------------------------------------------------------
# ``claim-check-allow-count`` -- document-scoped count exemption.
# ---------------------------------------------------------------------------


class TestClaimCheckAllowCountDirective:
    """Suppresses a count soft flag whose normalized token is named
    exactly -- the sibling of ``claim-check-allow`` for the
    category-D heuristic (prescriptive guidance numbers + deliberately-
    quoted historical mistakes the heuristic cannot tell from a
    memory-quoted fact).
    """

    def test_directive_suppresses_matching_count(self, cc, tmp_path):
        _make_repo(tmp_path)
        text = (
            "<!-- claim-check-allow-count: 728 tests -->\n"
            'the "728 tests" baseline was wrong.'
        )
        _hard, soft = cc.check_text(text, tmp_path)
        assert soft == []

    def test_records_exact_exemption(self, cc, tmp_path):
        _make_repo(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text(
            "<!-- claim-check-allow-count: 728 tests -->\n"
            'the "728 tests" baseline.'
        )
        result = cc.check_file(doc, tmp_path)
        assert result.soft_flags == []
        assert result.exempted_counts == [("728 tests", "728 tests")]

    def test_non_matching_count_still_soft_flags(self, cc, tmp_path):
        _make_repo(tmp_path)
        text = (
            "<!-- claim-check-allow-count: 728 tests -->\n"
            "but the repo has 999 commits today."
        )
        _hard, soft = cc.check_text(text, tmp_path)
        assert len(soft) == 1
        assert soft[0].token == "999 commits"

    def test_normalization_matches_extra_space_and_case(
        self, cc, tmp_path
    ):
        # The accepted token normalizes (single-spaced, lowercased),
        # so a declaration with odd spacing still matches the flagged
        # claim.
        _make_repo(tmp_path)
        text = (
            "<!-- claim-check-allow-count:  40   Proposals -->\n"
            'the "40 proposals" miscount.'
        )
        _hard, soft = cc.check_text(text, tmp_path)
        assert soft == []

    def test_multiple_counts_in_one_directive(self, cc):
        out = cc.parse_allow_count_directives(
            "<!-- claim-check-allow-count: 30 lines, 728 tests -->"
        )
        assert [c for _, c in out] == ["30 lines", "728 tests"]

    def test_thousands_grouped_count_can_be_named(self, cc, tmp_path):
        # fold-back #36: counts are extracted with the same detector the
        # body scan uses, so a thousands-grouped count is one token -- the
        # comma is part of the number, not the directive's list delimiter.
        _make_repo(tmp_path)
        text = (
            "<!-- claim-check-allow-count: 1,294 lines -->\n"
            'the "1,294 lines" total was a point-in-time snapshot.'
        )
        _hard, soft = cc.check_text(text, tmp_path)
        assert soft == []

    def test_count_directive_is_separator_agnostic(self, cc):
        # comma, semicolon, or whitespace between tokens are all just
        # non-matching gaps; a grouped count survives intact (#36).
        out = cc.parse_allow_count_directives(
            "<!-- claim-check-allow-count: 1,294 lines; 5 commits, 30 lines -->"
        )
        assert [c for _, c in out] == ["1,294 lines", "5 commits", "30 lines"]

    def test_main_reports_exempted_count_on_stdout(
        self, cc, tmp_path, capsys
    ):
        _make_repo(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text(
            "<!-- claim-check-allow-count: 728 tests -->\n"
            'the "728 tests" baseline.'
        )
        rc = cc.main([str(doc), "--root", str(tmp_path)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "728 tests" in out
        assert "exempted count" in out

    def test_directive_shown_in_prose_is_not_parsed(self, cc, tmp_path):
        # A non-standalone mention (inside backticks) is not a live
        # directive, so the count it names is NOT suppressed.
        _make_repo(tmp_path)
        text = (
            "docs: write "
            "`<!-- claim-check-allow-count: 728 tests -->`; "
            "the repo had 728 tests then."
        )
        _hard, soft = cc.check_text(text, tmp_path)
        assert any(f.token == "728 tests" for f in soft)
        assert cc.parse_allow_count_directives(text) == []

    def test_no_directive_behaviour_unchanged(self, cc, tmp_path):
        _make_repo(tmp_path)
        _hard, soft = cc.check_text(
            "the repo has 728 tests.", tmp_path
        )
        assert len(soft) == 1
        assert soft[0].token == "728 tests"

    def test_fail_on_soft_clean_when_count_exempted(
        self, cc, tmp_path
    ):
        # --fail-on-soft exits non-zero on a live count flag, but an
        # exempted count must not trip it.
        _make_repo(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text(
            "<!-- claim-check-allow-count: 728 tests -->\n"
            'the "728 tests" baseline.'
        )
        rc = cc.main(
            [str(doc), "--root", str(tmp_path), "--fail-on-soft"]
        )
        assert rc == 0
