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
* The ``CheckResult.exempted`` field and the stdout-side audit lines
  from ``main``.
* The **retirement** of the category-D count soft-flag and its
  ``claim-check-allow-count`` directive (2026-06-05): counts never
  soft-flag, the directive parser is gone, and a stray directive is
  silently ignored.

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
        assert cc.allow_glob_error("dev/.cairn/cairn-lock.yml") is None

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
            "<!-- claim-check-allow: dev/.cairn/cairn-lock.yml -->\n"
            "see `dev/.cairn/cairn-lock.yml` here"
        )
        hard, _ = cc.check_text(text, tmp_path)
        assert hard == []

    def test_directive_records_exact_exemption(self, cc, tmp_path):
        # R2: the exempted token + matching glob are on the result.
        _make_repo(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text(
            "<!-- claim-check-allow: dev/.cairn/cairn-lock.yml -->\n"
            "see `dev/.cairn/cairn-lock.yml`"
        )
        result = cc.check_file(doc, tmp_path)
        assert result.hard_flags == []
        assert result.exempted == [
            ("dev/.cairn/cairn-lock.yml", "dev/.cairn/cairn-lock.yml")
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
            "see `dev/.cairn/cairn-lock.yml`"
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
            "<!-- claim-check-allow: dev/.cairn/cairn-lock.yml -->\n"
            "see `dev/.cairn/cairn-lock.yml`"
        )
        rc = cc.main([str(doc), "--root", str(tmp_path)])
        assert rc == 0  # exemptions are not flags
        # The exemption report is on STDOUT (the primary success
        # artifact), not stderr.
        out = capsys.readouterr().out
        assert "dev/.cairn/cairn-lock.yml" in out
        assert "exempted" in out

    def test_no_directive_behaviour_unchanged(self, cc, tmp_path):
        _make_repo(tmp_path)
        hard, _ = cc.check_text("see `dev/.cairn/cairn-lock.yml`", tmp_path)
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

    def test_default_exempt_runtime_path_does_not_hard_flag(
        self, cc, tmp_path
    ):
        # fold-back #42: dev/intents.jsonl is a gitignored framework runtime
        # path (created on first work-intent claim), so it is legitimately
        # absent from a clean tree and must never hard-flag -- even though
        # `dev` IS a real top-level dir here -- with no per-document
        # directive needed.
        _make_repo(tmp_path)
        assert not (tmp_path / "dev" / "intents.jsonl").exists()
        text = "the work-intent log lives at `dev/intents.jsonl`."
        hard, _soft = cc.check_text(text, tmp_path)
        assert hard == []


# ---------------------------------------------------------------------------
# Self-host: the framework machine-state exempt set (exact + /-terminated
# prefix).  Once a project self-hosts Cairn it has a real top-level dev/ tree,
# so doctrine / templates / changelog that cite dev/<machine-state> must not
# hard-flag -- but the matching must stay sharp (no sibling / suffix
# over-exemption).  Settled by Internal + cross-type External review of the
# 2026-06-12 check_cairn self-host-compat proposal.
# ---------------------------------------------------------------------------


class TestDefaultExemptFrameworkPaths:
    """``_DEFAULT_EXEMPT_PATHS`` / ``_DEFAULT_EXEMPT_PREFIXES`` -- framework
    runtime / generated paths a fresh scaffold lacks, exempt by the shipped
    tool (not per-document directives).  Exact or ``/``-terminated-prefix, so
    a sibling or a suffix is never over-exempted -- the gate stays sharp.
    """

    def test_exact_machine_state_path_exempt(self, cc, tmp_path):
        _make_repo(tmp_path)
        text = ("config `dev/.cairn/metrics-config.json`, "
                "log `dev/measurement/collision_log.md`")
        hard, _soft = cc.check_text(text, tmp_path)
        assert hard == []

    def test_generated_subtree_prefix_exempt(self, cc, tmp_path):
        _make_repo(tmp_path)
        text = "cache `dev/.cairn/base/` holds `dev/.cairn/base/ab12/manifest.json`"
        hard, _soft = cc.check_text(text, tmp_path)
        assert hard == []

    def test_prefix_match_is_slash_terminated(self, cc, tmp_path):
        # A sibling whose name merely *starts with* a prefix dir is NOT exempt.
        _make_repo(tmp_path)
        hard, _soft = cc.check_text("a stray `dev/.cairn-upgrade-bak/x.txt`", tmp_path)
        assert [f.token for f in hard] == ["dev/.cairn-upgrade-bak/x.txt"]

    def test_exact_path_does_not_exempt_suffix(self, cc, tmp_path):
        # R3 (External review): dev/intents.jsonl.bak must NOT inherit the
        # exemption of the exact entry dev/intents.jsonl.
        _make_repo(tmp_path)
        hard, _soft = cc.check_text("a stale `dev/intents.jsonl.bak`", tmp_path)
        assert [f.token for f in hard] == ["dev/intents.jsonl.bak"]

    def test_committed_lockfile_under_cairn_still_checked(self, cc, tmp_path):
        # The .cairn/ subtree is NOT blanket-exempt: a non-existent
        # committed-class file under it still hard-flags (R3 breadth concern).
        _make_repo(tmp_path)
        hard, _soft = cc.check_text("missing `dev/.cairn/cairn-lock.yml`", tmp_path)
        assert [f.token for f in hard] == ["dev/.cairn/cairn-lock.yml"]


# ---------------------------------------------------------------------------
# Category-D count soft-flag retired 2026-06-05 (0 catches across the
# verify-before-asserting instance log; the nag generated the
# ``claim-check-allow-count`` header bloat it was meant to silence).  The
# count detector, ``find_count_flags``, and the ``claim-check-allow-count``
# directive parser are gone; numeric drift is governed by the three-kind
# precision / ``as_of`` discipline + the code-side ``verify_counts``
# registry.  These tests pin the retirement: counts never soft-flag, and a
# stray directive left in an archived doc is silently ignored.
# ---------------------------------------------------------------------------


class TestCountSoftFlagRetired:
    """The category-D count soft-flag and its directive are gone."""

    def test_count_no_longer_soft_flags(self, cc, tmp_path):
        # What once produced a category-D soft flag now produces nothing.
        _make_repo(tmp_path)
        _hard, soft = cc.check_text("the repo has 728 tests.", tmp_path)
        assert soft == []

    def test_thousands_grouped_count_no_longer_flags(self, cc, tmp_path):
        _make_repo(tmp_path)
        _hard, soft = cc.check_text("the engine is 1,294 lines.", tmp_path)
        assert soft == []

    def test_stray_allow_count_comment_is_silently_ignored(
        self, cc, tmp_path
    ):
        # An archived doc may still carry an inert
        # ``claim-check-allow-count`` comment.  It must never hard-flag
        # (it is an HTML comment, stripped) and there is no count flag to
        # suppress -- it is simply a no-op now.
        _make_repo(tmp_path)
        text = (
            "<!-- claim-check-allow-count: 728 tests -->\n"
            'the "728 tests" baseline.'
        )
        hard, soft = cc.check_text(text, tmp_path)
        assert hard == []
        assert soft == []

    def test_count_directive_parser_is_removed(self, cc):
        # The retired directive parser and count detector are gone from
        # the public surface.
        assert not hasattr(cc, "parse_allow_count_directives")
        assert not hasattr(cc, "find_count_flags")

    def test_check_result_has_no_exempted_counts_field(self, cc, tmp_path):
        # The ``exempted_counts`` CheckResult field was removed with the
        # directive; the two-tuple ``check_text`` contract is preserved.
        _make_repo(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text("the repo has 728 tests.")
        result = cc.check_file(doc, tmp_path)
        assert not hasattr(result, "exempted_counts")
        assert result.soft_flags == []

    def test_main_clean_on_former_count_doc(self, cc, tmp_path, capsys):
        # A doc that once tripped the count soft-flag now reports clean.
        _make_repo(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text("the repo has 728 tests.")
        rc = cc.main([str(doc), "--root", str(tmp_path)])
        assert rc == 0
        assert "OK, no claim-check flags" in capsys.readouterr().out


# --- `path::node` node citations (board-drain-guards R1/R2) -------------------
#
# `doctrine/lifecycle.md` > "Archive precondition" mandates `path::node` as the
# citation form for a `guard` disposition. Before this fix the checker resolved
# the whole token and hard-flagged every such citation, so the token's mandated
# form was unwritable in any claim-checked file.
#
# The load-bearing assertion is NOT that valid citations pass -- it is
# `test_node_citation_with_absent_path_is_still_flagged`: the fix must not have
# become a bypass.


def _hard(cc: ModuleType, tmp_path: Path, body: str) -> list:
    """Scan a one-line doc against the REAL repo root; return hard flags."""
    doc = tmp_path / "probe.md"
    doc.write_text(body, encoding="utf-8")
    return cc.check_file(doc, CAIRN_ROOT).hard_flags


def test_node_citation_with_existing_path_is_not_flagged(cc, tmp_path):
    """`path::node` resolves on its path half -- the guard citation form."""
    hard = _hard(
        cc, tmp_path,
        "A guard cites `bootstrap/tests/test_claim_check_module.py::test_x`.\n",
    )
    assert hard == [], [f.message for f in hard]


def test_node_citation_with_absent_path_is_still_flagged(cc, tmp_path):
    """LOAD-BEARING: the fix must not become a bypass.

    A `::` suffix must not launder a path that does not exist.
    """
    hard = _hard(
        cc, tmp_path,
        "A guard cites `bootstrap/tests/no_such_file_here.py::test_x`.\n",
    )
    assert len(hard) == 1, [f.message for f in hard]
    assert "does not resolve" in hard[0].message


def test_line_bounds_citation_is_unchanged_by_the_node_fix(cc, tmp_path):
    """The `:N` dispatch branch stays intact and unswallowed."""
    ok = _hard(
        cc, tmp_path,
        "See `bootstrap/tests/test_claim_check_module.py:1`.\n",
    )
    assert ok == [], [f.message for f in ok]
    out_of_range = _hard(
        cc, tmp_path,
        "See `bootstrap/tests/test_claim_check_module.py:999999`.\n",
    )
    assert len(out_of_range) == 1, [f.message for f in out_of_range]


def test_parametrised_node_id_is_not_flagged(cc, tmp_path):
    """Guards plan-review [P7]: the first assertion must not be passing
    via the placeholder exemption. Brackets are NOT in
    ``_PLACEHOLDER_CHARS``, so a parametrised id genuinely reaches the
    check rather than being waived upstream."""
    assert not any(c in "[]" for c in cc._PLACEHOLDER_CHARS)
    hard = _hard(
        cc, tmp_path,
        "A guard cites `bootstrap/tests/test_claim_check_module.py::test_x[a-b]`.\n",
    )
    assert hard == [], [f.message for f in hard]
