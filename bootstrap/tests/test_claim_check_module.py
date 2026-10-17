"""Direct unit coverage for the ``claim_check.py`` module's
document-scoped exemption directives.

Ported from modflow_tools' ``tests/unit/test_claim_check.py`` (the
reference implementation's adopter-side coverage) into Cairn at chunk 1
of the ``cairn-0.2.x-sweep-and-ledger-followups`` plan, where the
allow-directive family was ported into Cairn (commit pending).

Covers:

* ``claim-check-allow`` path-exemption directive -- narrow-glob
  validation (the ``allow_glob_error`` rules), exact-token reporting,
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
# ``claim-check-allow`` globs must be narrow.
# ---------------------------------------------------------------------------


class TestAllowGlobValidation:
    """A wildcard must be preceded by >= 2 literal path segments
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
    document-wide (narrow-glob validation, exact-token report),
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
        # The exempted token + matching glob are on the result.
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
        # `dev/*` is rejected -> a `directive` hard flag, AND the
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
        # main() names the exact exempted token in its output.
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
                "binding `dev/.cairn/local-env.json`, "
                "log `dev/measurement/collision_log.md`")
        hard, _soft = cc.check_text(text, tmp_path)
        assert hard == []

    def test_local_env_exemption_does_not_cover_a_suffix(self, cc, tmp_path):
        _make_repo(tmp_path)
        hard, _soft = cc.check_text(
            "stale backup `dev/.cairn/local-env.json.bak`", tmp_path
        )
        assert [f.token for f in hard] == ["dev/.cairn/local-env.json.bak"]

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
        # dev/intents.jsonl.bak must NOT inherit the
        # exemption of the exact entry dev/intents.jsonl.
        _make_repo(tmp_path)
        hard, _soft = cc.check_text("a stale `dev/intents.jsonl.bak`", tmp_path)
        assert [f.token for f in hard] == ["dev/intents.jsonl.bak"]

    def test_committed_lockfile_under_cairn_still_checked(self, cc, tmp_path):
        # The .cairn/ subtree is NOT blanket-exempt: a non-existent
        # committed-class file under it still hard-flags.
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


# --- `path::node` node citations -------------------------------------------
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
    """The first assertion must not be passing
    via the placeholder exemption. Brackets are NOT in
    ``_PLACEHOLDER_CHARS``, so a parametrised id genuinely reaches the
    check rather than being waived upstream."""
    assert not any(c in "[]" for c in cc._PLACEHOLDER_CHARS)
    hard = _hard(
        cc, tmp_path,
        "A guard cites `bootstrap/tests/test_claim_check_module.py::test_x[a-b]`.\n",
    )
    assert hard == [], [f.message for f in hard]


def test_node_citation_whose_path_half_is_a_directory_is_flagged(cc, tmp_path):
    """A node citation names a test node, which lives in
    a FILE. `.exists()` let a directory path half through, which is a
    fail-open widening the bare-path branch does not have."""
    hard = _hard(cc, tmp_path, "A guard cites `bootstrap/tests::test_x`.\n")
    assert len(hard) == 1, [f.message for f in hard]


def test_bare_directory_path_is_still_accepted(cc, tmp_path):
    """The fix must not spill onto the bare-path branch: a directory
    is a legitimate path claim when cited without a `::node`."""
    hard = _hard(cc, tmp_path, "See `bootstrap/tests`.\n")
    assert hard == [], [f.message for f in hard]


# ---------------------------------------------------------------------------
# Exact lifecycle active-to-archive resolution (accepted
# `claim-check-exemption-hygiene` proposal, Section 1).
#
# Scope note: this covers only the resolution
# mechanism itself (exact same-family fallback, direct-path priority, the
# archived-file line-bounds check, and claim-check's own defense-in-depth
# duplicate-identity refusal).  Typed-declaration registry exactness and
# unused-glob / archive-redundant-glob liveness classification are
# (Opus tier, not implemented here) -- see the plan's Chunk D table.
#
# `_make_lifecycle_repo` is deliberately self-contained rather than an
# extension of `_make_repo` above, to avoid coupling this chunk's fixture
# needs to whatever shape the registry/liveness tests end up wanting
# from the shared helper.
# ---------------------------------------------------------------------------


def _make_lifecycle_repo(root: Path) -> Path:
    """Build a synthetic repo with the two lifecycle families and their
    `archive/` siblings, plus one unrelated top-level dir with its own
    `archive/` subdirectory -- so the "outside the two lifecycle dirs"
    boundary is actually exercised against a real look-alike, not merely
    an absent path.
    """
    (root / "AGENTS.md").write_text("root file\n")
    (root / "dev" / "proposals" / "archive").mkdir(parents=True)
    (root / "dev" / "plans" / "archive").mkdir(parents=True)
    (root / "templates" / "archive").mkdir(parents=True)
    return root


def _write_lines(path: Path, n: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(f"line {i}" for i in range(1, n + 1)) + "\n")


class TestLifecycleArchiveResolution:
    """Exact `dev/{proposals,plans}/<file>.md` -> `.../archive/<file>.md`
    resolution, direct-path priority, and archived-file line bounds."""

    def test_exact_archive_sibling_resolves(self, cc, tmp_path):
        # Happy path: the active file is missing, its exact same-family
        # archived sibling exists -- resolves clean, no hard flag.
        _make_lifecycle_repo(tmp_path)
        (tmp_path / "dev" / "proposals" / "archive" / "foo.md").write_text(
            "# archived\n"
        )
        hard, _soft = cc.check_text("see `dev/proposals/foo.md`", tmp_path)
        assert hard == []

    def test_direct_path_authoritative_when_it_exists(self, cc, tmp_path):
        # The active file exists (no archived sibling at all) -- ordinary
        # resolution, unaffected by the new rule.
        _make_lifecycle_repo(tmp_path)
        (tmp_path / "dev" / "plans" / "bar.md").write_text("# active\n")
        hard, _soft = cc.check_text("see `dev/plans/bar.md`", tmp_path)
        assert hard == []

    def test_typo_in_filename_does_not_resolve(self, cc, tmp_path):
        # Mutation: filename.  A near-match archived stem must NOT
        # resolve a differently-spelled active citation -- this is an
        # identity rule, not a fuzzy search.
        _make_lifecycle_repo(tmp_path)
        (tmp_path / "dev" / "proposals" / "archive" / "foo.md").write_text(
            "# archived\n"
        )
        hard, _soft = cc.check_text("see `dev/proposals/fooo.md`", tmp_path)
        assert [f.token for f in hard] == ["dev/proposals/fooo.md"]
        assert "does not resolve" in hard[0].message

    def test_cross_family_archive_does_not_resolve(self, cc, tmp_path):
        # Mutation: family.  An archived plan of the same stem must not
        # resolve a missing active *proposal* -- never crosses families.
        _make_lifecycle_repo(tmp_path)
        (tmp_path / "dev" / "plans" / "archive" / "foo.md").write_text(
            "# archived plan\n"
        )
        hard, _soft = cc.check_text("see `dev/proposals/foo.md`", tmp_path)
        assert [f.token for f in hard] == ["dev/proposals/foo.md"]

    def test_cross_family_archive_does_not_resolve_reverse(self, cc, tmp_path):
        # Same-name independence in the other direction: an archived
        # proposal does not resolve a missing active plan.
        _make_lifecycle_repo(tmp_path)
        (tmp_path / "dev" / "proposals" / "archive" / "foo.md").write_text(
            "# archived proposal\n"
        )
        hard, _soft = cc.check_text("see `dev/plans/foo.md`", tmp_path)
        assert [f.token for f in hard] == ["dev/plans/foo.md"]

    def test_archive_at_wrong_nested_location_does_not_resolve(
        self, cc, tmp_path
    ):
        # Mutation: (archive) location.  The rule checks the *exact*
        # `.../archive/<file>.md` path -- a same-named file one level
        # deeper under `archive/` (a plausible slip, not a typo or a
        # family mismatch) must not resolve.
        _make_lifecycle_repo(tmp_path)
        nested = (
            tmp_path / "dev" / "proposals" / "archive" / "nested" / "foo.md"
        )
        nested.parent.mkdir(parents=True)
        nested.write_text("# wrong location\n")
        hard, _soft = cc.check_text("see `dev/proposals/foo.md`", tmp_path)
        assert [f.token for f in hard] == ["dev/proposals/foo.md"]

    def test_duplicate_active_and_archived_identity_hard_flags(
        self, cc, tmp_path
    ):
        # "Claim-check also fails closed if it encounters both
        # candidates while resolving a lifecycle token."  Direct-path
        # priority does not silently normalize a duplicate identity.
        _make_lifecycle_repo(tmp_path)
        (tmp_path / "dev" / "proposals" / "foo.md").write_text("# active\n")
        (tmp_path / "dev" / "proposals" / "archive" / "foo.md").write_text(
            "# archived\n"
        )
        hard, _soft = cc.check_text("see `dev/proposals/foo.md`", tmp_path)
        assert len(hard) == 1
        assert "lifecycle-state violation" in hard[0].message
        assert "duplicate identity" in hard[0].message

    def test_line_bounds_checked_against_archived_file_in_bounds(
        self, cc, tmp_path
    ):
        # "A fixture cites the final valid line and then one line
        # beyond it" (proposal Evidence/verification plan) -- in-bounds
        # half: the final valid line of the *archived* file.
        _make_lifecycle_repo(tmp_path)
        _write_lines(
            tmp_path / "dev" / "proposals" / "archive" / "foo.md", 5
        )
        hard, _soft = cc.check_text("see `dev/proposals/foo.md:5`", tmp_path)
        assert hard == []

    def test_line_bounds_checked_against_archived_file_out_of_bounds(
        self, cc, tmp_path
    ):
        # Out-of-bounds half: one line beyond the archived file's actual
        # count.  Moving a file to archive/ does not waive a stale bound.
        _make_lifecycle_repo(tmp_path)
        _write_lines(
            tmp_path / "dev" / "proposals" / "archive" / "foo.md", 5
        )
        hard, _soft = cc.check_text("see `dev/proposals/foo.md:6`", tmp_path)
        assert len(hard) == 1
        assert hard[0].kind == "line-bounds"
        assert "exceeds" in hard[0].message

    def test_archived_strategy_note_resolves(self, cc, tmp_path):
        # Strategy notes archive like proposals and plans, so a citation
        # to one that has since moved under `archive/` must keep resolving;
        # a note that exists nowhere still flags.
        _make_lifecycle_repo(tmp_path)
        (tmp_path / "dev" / "strategy" / "archive").mkdir(parents=True)
        (tmp_path / "dev" / "strategy" / "archive" / "note.md").write_text(
            "# archived note\n")
        hard, _soft = cc.check_text(
            "see `dev/strategy/note.md` and `dev/strategy/gone.md`", tmp_path)
        assert [f.token for f in hard] == ["dev/strategy/gone.md"]

    def test_archive_resolution_limited_to_lifecycle_dirs(self, cc, tmp_path):
        # The resolution rule is limited to exactly the three lifecycle
        # families -- `dev/proposals/`, `dev/plans/`, `dev/strategy/` -- so
        # a missing file under any OTHER directory must not resolve against
        # a same-shaped `<dir>/archive/<file>` sibling, even though one
        # concretely exists here, however plausible the look-alike.
        _make_lifecycle_repo(tmp_path)
        (tmp_path / "templates" / "archive" / "foo.md").write_text(
            "# archived-looking, but not a lifecycle dir\n"
        )
        hard, _soft = cc.check_text("see `templates/foo.md`", tmp_path)
        assert [f.token for f in hard] == ["templates/foo.md"]


class TestFencesFollowTheDocumentFormat:
    """In Markdown a `~~~` line opens a code fence; in reStructuredText it
    underlines a section heading.  Treating an RST underline as a fence
    skipped every line between two subsections, unchecked and unreported."""

    RST = (
        "Section\n-------\n\nSubsection one\n~~~~~~~~~~~~~~\n\n"
        "See `scripts/does_not_exist.py` for details.\n\n"
        "Subsection two\n~~~~~~~~~~~~~~\n\nText here.\n"
    )

    @staticmethod
    def _repo(tmp_path: Path) -> Path:
        # A `scripts/` directory makes `scripts/...` a repo path claim at all.
        _make_lifecycle_repo(tmp_path)
        (tmp_path / "scripts").mkdir()
        (tmp_path / "scripts" / "real.py").write_text("")
        return tmp_path

    def test_rst_underlines_do_not_hide_text(self, cc, tmp_path):
        repo = self._repo(tmp_path)
        hard, _ = cc.check_text(self.RST, repo, doc_rel="docs/guide.rst")
        assert [f.token for f in hard] == ["scripts/does_not_exist.py"]

    def test_markdown_tilde_fences_still_hide_code(self, cc, tmp_path):
        repo = self._repo(tmp_path)
        fenced = "~~~\nSee `scripts/does_not_exist.py`.\n~~~\n"
        plain = "See `scripts/does_not_exist.py`.\n"
        assert cc.check_text(fenced, repo, doc_rel="docs/guide.md")[0] == []
        # Control: the same line outside a fence is flagged, so the empty
        # result above is the fence at work, not an unrecognised path.
        assert [f.token for f in cc.check_text(
            plain, repo, doc_rel="docs/guide.md")[0]] == [
            "scripts/does_not_exist.py"]


# ---------------------------------------------------------------------------
# The typed-declaration registry and liveness (accepted
# `claim-check-exemption-hygiene` proposal, Section 2).
#
# These are the two cells left by `4723107`:
# **registry exactness** and **liveness**.  Liveness is only decidable per
# artifact, so every node here goes through `check_file` with the document
# written *inside* the fixture repo -- `check_text`, which takes text and no
# path, deliberately does not evaluate liveness at all.
# ---------------------------------------------------------------------------


def _make_registry_repo(root: Path) -> Path:
    """A synthetic repo with both lifecycle families, their `archive/`
    siblings, and the ordinary top-level dirs the fixtures cite."""
    (root / "AGENTS.md").write_text("root file\n")
    (root / "dev" / "proposals" / "archive").mkdir(parents=True)
    (root / "dev" / "plans" / "archive").mkdir(parents=True)
    (root / "dev" / "measurement").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "bootstrap" / "tests").mkdir(parents=True)
    (root / "docs").mkdir()
    return root


def _artifact(root: Path, rel: str, body: str) -> Path:
    """Write *body* to *rel* inside the fixture repo and return the path."""
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


#: A non-terminal plan header -- `executing` is not a terminal status, so
#: liveness applies with its hard disposition.
_PLAN_HEADER = "# Plan: fixture\n\n**Status**: executing\n\n"


def _check(cc: ModuleType, root: Path, rel: str, body: str):
    return cc.check_file(_artifact(root, rel, body), root)


class TestTypedRegistryExactness:
    """A marker block is a document registry of **literal** paths --
    document-wide, exact, and reported with the authorizing declaration."""

    def test_declared_path_is_exempt_where_it_recurs_outside_its_block(
        self, cc, tmp_path,
    ):
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Proposed paths:\n"
            "- `scripts/future.py` -- created by chunk A.\n"
            "- `scripts/other.py` -- created by chunk B.\n"
            "\n"
            "Chunk A lands `scripts/future.py` and chunk B `scripts/other.py`.\n"
        ))
        assert result.hard_flags == [], [f.message for f in result.hard_flags]
        assert [t for t, _label in result.declared] == [
            "scripts/future.py", "scripts/other.py",
        ]

    def test_the_exemption_names_the_declaration_that_authorized_it(
        self, cc, tmp_path,
    ):
        # "claim-check reports every token it exempts together with the
        # declaration that authorized it" (proposal Section 2).
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Untracked paths:\n"
            "- `scripts/local.py` -- gitignored on purpose.\n"
            "- `scripts/other.py` -- also local.\n"
            "\n"
            "The runner reads `scripts/local.py` at start-up, then\n"
            "`scripts/other.py`.\n"
        ))
        assert result.hard_flags == [], [f.message for f in result.hard_flags]
        labels = [label for tok, label in result.declared
                  if tok == "scripts/local.py"]
        assert len(labels) == 1
        assert "Untracked paths:" in labels[0]
        assert "`scripts/local.py`" in labels[0]
        assert "line 6" in labels[0], labels[0]

    @pytest.mark.parametrize("cited", [
        "scripts/future_extra.py",      # look-alike prefix
        "scripts/future.py.bak",        # look-alike suffix
        "scripts/sub/future.py",        # same basename, different dir
        "scripts/future.py/inner.py",   # a descendant of the declared path
    ])
    def test_declaration_exempts_only_the_exact_path(self, cc, tmp_path, cited):
        # "it does not let one declared path exempt a sibling or
        # descendant" (proposal Section 2).
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Proposed paths:\n"
            "- `scripts/future.py` -- created by chunk A.\n"
            "- `scripts/other.py` -- created by chunk B.\n"
            "\n"
            f"Chunk A also touches `{cited}`.\n"
            "It lands `scripts/future.py` and `scripts/other.py` too.\n"
        ))
        assert [f.token for f in result.hard_flags] == [cited], [
            f.message for f in result.hard_flags
        ]

    def test_a_row_declares_its_leading_token_not_its_prose(self, cc, tmp_path):
        # A list row lists one path and then explains it: a path named
        # later in the row's prose is a reference, not a declaration.
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Proposed paths:\n"
            "- `scripts/future.py` -- installed as `scripts/installed.py`.\n"
            "- `scripts/other.py` -- created by chunk B.\n"
            "\n"
            "Chunk A lands `scripts/future.py`, `scripts/other.py`, and\n"
            "then `scripts/installed.py`.\n"
        ))
        assert [f.token for f in result.hard_flags] == [
            "scripts/installed.py"
        ], [f.message for f in result.hard_flags]

    def test_the_marker_line_itself_declares_every_token_on_it(
        self, cc, tmp_path,
    ):
        # The compact one-line form must keep working document-wide.
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Proposed paths: `scripts/a.py`, `scripts/b.py`\n"
            "- `scripts/c.py` -- and a row, so this is a registry block.\n"
            "\n"
            "Chunk A lands `scripts/a.py`, `scripts/b.py` and `scripts/c.py`.\n"
        ))
        assert result.hard_flags == [], [f.message for f in result.hard_flags]
        assert sorted({t for t, _ in result.declared}) == [
            "scripts/a.py", "scripts/b.py", "scripts/c.py",
        ]

    def test_a_glob_entry_is_malformed_and_grants_nothing(self, cc, tmp_path):
        # "Registry entries are literal paths, not globs" -- fail closed.
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Proposed paths:\n"
            "- `scripts/gen_*.py` -- one per generator.\n"
            "- `scripts/other.py` -- created by chunk B.\n"
            "\n"
            "Chunk A lands `scripts/gen_a.py` and `scripts/other.py`.\n"
        ))
        messages = [f.message for f in result.hard_flags]
        assert any("malformed typed declaration" in m for m in messages), messages
        assert any("scripts/gen_a.py" in m for m in messages), messages
        # ...and the well-formed sibling entry still works.
        assert [t for t, _ in result.declared] == ["scripts/other.py"]

    def test_same_keyword_redeclaration_is_idempotent_not_a_duplicate(
        self, cc, tmp_path,
    ):
        # An append-only record whose revision section restates its proposed
        # paths is doing the right thing -- it must not fail.
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Proposed paths:\n"
            "- `scripts/future.py` -- created by chunk A.\n"
            "\n"
            "## Revision 1\n"
            "\n"
            "Proposed paths:\n"
            "- `scripts/future.py` -- still created by chunk A.\n"
            "\n"
            "Chunk A lands `scripts/future.py`.\n"
        ))
        assert result.hard_flags == [], [f.message for f in result.hard_flags]

    def test_conflicting_keywords_for_one_path_fail_closed(self, cc, tmp_path):
        # Two incompatible reasons for the same path: the checker refuses to
        # pick one, so the path gets no registry authority at all.
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Proposed paths:\n"
            "- `scripts/future.py` -- created by chunk A.\n"
            "\n"
            "Untracked paths:\n"
            "- `scripts/future.py` -- never committed.\n"
            "\n"
            "Chunk A lands `scripts/future.py`.\n"
        ))
        messages = [f.message for f in result.hard_flags]
        assert any("conflicting typed declarations" in m for m in messages), messages
        # ...and the recurrence outside both blocks is NOT exempted.
        assert result.declared == []
        assert any("does not resolve" in m for m in messages), messages

    def test_registry_never_silences_a_flag_on_a_path_that_exists(
        self, cc, tmp_path,
    ):
        # Parity with the allow-directive: an out-of-range line-bounds
        # citation into a REAL file is the stale-anchor class claim_check
        # exists to catch, and no declaration may waive it.
        _make_registry_repo(tmp_path)
        _write_lines(tmp_path / "scripts" / "real.py", 5)
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Proposed paths:\n"
            "- `scripts/real.py` -- rewritten by chunk A.\n"
            "- `scripts/other.py` -- created by chunk B.\n"
            "\n"
            "The guard is at `scripts/real.py:99`, and chunk B lands\n"
            "`scripts/other.py`.\n"
        ))
        bounds = [f for f in result.hard_flags if f.kind == "line-bounds"]
        assert [f.token for f in bounds] == ["scripts/real.py:99"], [
            f.message for f in result.hard_flags
        ]
        assert "exceeds" in bounds[0].message
        # The same fixture also exercises liveness from the other side: a
        # declaration whose path exists is itself stale.
        assert [f.token for f in result.hard_flags if f.kind == "declaration"] \
            == ["scripts/real.py"]


class TestLiveness:
    """On a non-terminal lifecycle artifact an exemption must still be
    doing work; an immutable artifact is grandfathered; and a redundancy
    *this change* created reports as a migration item, never a hard flag."""

    def test_unused_glob_hard_fails_on_a_non_terminal_plan(self, cc, tmp_path):
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", (
            "<!-- claim-check-allow: scripts/nothing.py -->\n" + _PLAN_HEADER
            + "Body with no citation of that path at all.\n"
        ))
        assert [f.kind for f in result.hard_flags] == ["directive"]
        assert "unused claim-check-allow glob" in result.hard_flags[0].message
        assert "scripts/nothing.py" in result.hard_flags[0].message

    def test_archive_redundant_glob_is_a_non_failing_migration_item(
        self, cc, tmp_path,
    ):
        # Section 1's resolver makes a glob redundant, and
        # Section 3's liveness must NOT then hard-fail it.  Both halves in
        # one node -- effective before the archived file exists, a reported
        # migration item after -- so the transition itself is the oracle.
        _make_registry_repo(tmp_path)
        body = (
            "<!-- claim-check-allow: dev/plans/moved.md -->\n" + _PLAN_HEADER
            + "Sequenced after `dev/plans/moved.md`.\n"
        )
        before = _check(cc, tmp_path, "dev/plans/host.md", body)
        assert before.hard_flags == [], [f.message for f in before.hard_flags]
        assert before.exempted == [("dev/plans/moved.md", "dev/plans/moved.md")]

        (tmp_path / "dev" / "plans" / "archive" / "moved.md").write_text("x\n")
        after = _check(cc, tmp_path, "dev/plans/host.md", body)
        assert after.hard_flags == [], [f.message for f in after.hard_flags]
        assert after.exempted == []
        assert [f.severity for f in after.diagnostics] == ["info"]
        assert "resolved-by-archive" in after.diagnostics[0].message
        assert "dev/plans/archive/moved.md" in after.diagnostics[0].message
        assert after.diagnostics[0].line == 1  # the directive's own line

    def test_registry_redundant_glob_is_a_non_failing_migration_item(
        self, cc, tmp_path,
    ):
        # The same argument applied to the registry landing in the same
        # change set: the declaration now authorizes what the glob used to.
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", (
            "<!-- claim-check-allow: scripts/future.py -->\n" + _PLAN_HEADER
            + "Proposed paths:\n"
            "- `scripts/future.py` -- created by chunk A.\n"
            "- `scripts/other.py` -- created by chunk B.\n"
            "\n"
            "Chunk A lands `scripts/future.py` and chunk B `scripts/other.py`.\n"
        ))
        assert result.hard_flags == [], [f.message for f in result.hard_flags]
        assert result.exempted == []
        assert len(result.diagnostics) == 1
        assert result.diagnostics[0].severity == "info"
        assert "resolved-by-registry" in result.diagnostics[0].message

    def test_a_materialized_declaration_hard_fails(self, cc, tmp_path):
        # "A proposed entry whose local path has materialized is unused"
        # (Revision 1).
        _make_registry_repo(tmp_path)
        (tmp_path / "scripts" / "landed.py").write_text("# landed\n")
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Proposed paths:\n"
            "- `scripts/landed.py` -- created by chunk A.\n"
            "- `scripts/other.py` -- created by chunk B.\n"
            "\n"
            "Chunk A lands `scripts/landed.py`, chunk B `scripts/other.py`.\n"
        ))
        assert [f.kind for f in result.hard_flags] == ["declaration"]
        assert "has materialized" in result.hard_flags[0].message
        assert result.hard_flags[0].token == "scripts/landed.py"

    def test_a_declaration_nothing_outside_its_block_cites_hard_fails(
        self, cc, tmp_path,
    ):
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Proposed paths:\n"
            "- `scripts/orphan.py` -- created by chunk A.\n"
            "- `scripts/other.py` -- created by chunk B.\n"
            "\n"
            "Chunk B lands `scripts/other.py`.\n"
        ))
        assert [f.token for f in result.hard_flags] == ["scripts/orphan.py"]
        assert "nothing outside its own block" in result.hard_flags[0].message

    def test_a_standalone_marker_line_carries_no_liveness_obligation(
        self, cc, tmp_path,
    ):
        # The mechanism's original line-local use, mid-prose.  Its
        # declaration is load-bearing for its OWN line, so demanding a
        # second citation is an obligation with no legal discharge:
        # deleting the marker hard-flags the very line it explains.
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/host.md", _PLAN_HEADER + (
            "Record location and format -- append-only JSONL.\n"
            "Proposed path: `dev/measurement/events.jsonl`. This mirrors the\n"
            "shape already in production.\n"
        ))
        assert result.hard_flags == [], [f.message for f in result.hard_flags]
        assert result.diagnostics == [], [
            f.message for f in result.diagnostics
        ]

    def test_an_archived_artifact_reports_but_does_not_fail(self, cc, tmp_path):
        # "Archive immutability wins over cosmetic cleanup" -- grandfathered
        # by LOCATION, with no status parse at all.
        _make_registry_repo(tmp_path)
        result = _check(cc, tmp_path, "dev/plans/archive/old.md", (
            "<!-- claim-check-allow: scripts/nothing.py -->\n"
            "# Plan: old\n\n**Status**: executing\n\n"
            "Body with no citation of that path at all.\n"
        ))
        assert result.hard_flags == [], [f.message for f in result.hard_flags]
        assert [f.severity for f in result.diagnostics] == ["info"]
        assert "unused claim-check-allow glob" in result.diagnostics[0].message
        assert "immutable" in result.diagnostics[0].message

    @pytest.mark.parametrize("status", ["accepted", "rejected", "superseded"])
    def test_terminal_status_grandfathers_a_non_archived_proposal(
        self, cc, tmp_path, status,
    ):
        # Grandfather on immutability, not on directory -- a proposal
        # still sitting in `dev/proposals/` is immutable once terminal.
        _make_registry_repo(tmp_path)
        result = _check(
            cc, tmp_path, "dev/proposals/2026-01-01-a-b.md",
            "<!-- claim-check-allow: scripts/nothing.py -->\n"
            f"# p\n\n**Status**: {status}\n\nNo citation here.\n",
        )
        assert result.hard_flags == [], [f.message for f in result.hard_flags]
        assert [f.severity for f in result.diagnostics] == ["info"]

    def test_a_plans_terminal_status_is_archived_not_accepted(
        self, cc, tmp_path,
    ):
        # The families do not share a terminal vocabulary: `accepted` is a
        # proposal status, so a PLAN carrying it is not grandfathered.
        _make_registry_repo(tmp_path)
        accepted = _check(cc, tmp_path, "dev/plans/host.md", (
            "<!-- claim-check-allow: scripts/nothing.py -->\n"
            "# Plan\n\n**Status**: accepted\n\nNo citation here.\n"
        ))
        assert [f.severity for f in accepted.hard_flags] == ["hard"]
        archived = _check(cc, tmp_path, "dev/plans/host2.md", (
            "<!-- claim-check-allow: scripts/nothing.py -->\n"
            "# Plan\n\n**Status**: archived\n\nNo citation here.\n"
        ))
        assert archived.hard_flags == []

    @pytest.mark.parametrize("header", [
        "# p\n\nNo status line at all.\n",                       # missing
        "# p\n\n**Status**: accepted\n**Status**: rejected\n",    # duplicate
        "# p\n\n**Status**: acceptd\n",                           # typo
        "# p\n\n## Section\n\n**Status**: accepted\n",            # not header
    ])
    def test_a_missing_duplicate_or_unrecognized_status_cannot_claim_the_grandfather(
        self, cc, tmp_path, header,
    ):
        # "A missing, duplicate, or unrecognized lifecycle status does not
        # silently gain grandfathering" (Revision 1).  Fail closed INTO
        # liveness.
        _make_registry_repo(tmp_path)
        result = _check(
            cc, tmp_path, "dev/proposals/2026-01-01-a-b.md",
            "<!-- claim-check-allow: scripts/nothing.py -->\n" + header
            + "\nNo citation of that path.\n",
        )
        assert [f.kind for f in result.hard_flags] == ["directive"], [
            f.message for f in result.hard_flags
        ]

    def test_liveness_does_not_run_on_a_non_lifecycle_surface(
        self, cc, tmp_path,
    ):
        # The scope fence: strategy / doctrine / module / changelog /
        # template surfaces keep their existing behavior by declaration.
        _make_registry_repo(tmp_path)
        for rel in ("docs/notes.md", "dev/plans/_template.md",
                    "dev/proposals/_template.md"):
            result = _check(cc, tmp_path, rel, (
                "<!-- claim-check-allow: scripts/nothing.py -->\n"
                "# doc\n\n**Status**: executing\n\nNo citation here.\n"
            ))
            assert result.hard_flags == [], (rel, [
                f.message for f in result.hard_flags
            ])
            assert result.diagnostics == [], (rel, [
                f.message for f in result.diagnostics
            ])

    def test_check_text_without_a_path_does_not_evaluate_liveness(
        self, cc, tmp_path,
    ):
        # Liveness is defined per artifact; a caller holding only text
        # cannot say which artifact it is, so the two-tuple contract keeps
        # exactly its old behavior.
        _make_registry_repo(tmp_path)
        body = (
            "<!-- claim-check-allow: scripts/nothing.py -->\n" + _PLAN_HEADER
            + "No citation here.\n"
        )
        hard, _soft = cc.check_text(body, tmp_path)
        assert hard == [], [f.message for f in hard]
        hard_scoped, _ = cc.check_text(
            body, tmp_path, doc_rel="dev/plans/host.md")
        assert [f.kind for f in hard_scoped] == ["directive"]
