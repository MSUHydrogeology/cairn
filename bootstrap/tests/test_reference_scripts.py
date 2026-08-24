"""
Tests for the reference-script install + generalization.

Covers, per the executing plan (cairn-v0.2-p1-reference-scripts):
* install-path: scripts land verbatim in scripts/ + tools/; the .md
  doctrine lands in dev/modules/; skip-if-exists / --force respected.
* a verbatim-installed script produces no spurious unfilled-token /
  block-slot warnings.
* the install destination agrees with the default command token.
* generalization gate (load-bearing): both installed scripts RUN against
  a fresh non-modflow_tools target.
* E: the file-scoped external-path allowance exempts case-study-style
  files; a genuine broken local path still flags.
* the installed scripts are standard-library only.
* lifecycle_metrics degrades on no-git / main-branch targets.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

# Allow tests to import scaffold without installing a package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    _MODULE_MAPPINGS,
    install_modules,
    main,
    reference_script_token_defaults,
)

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"

# Default-on reference-script modules + their (verbatim src, dst).
_SCRIPT_MODULES = {
    "claim-check": (
        "default-on/claim_check.py", "scripts/claim_check.py",
    ),
    "lifecycle-metrics": (
        "default-on/lifecycle_metrics.py", "tools/lifecycle_metrics.py",
    ),
    # Active-surfacing scanner (ships alongside fold-back-ledger; see
    # 2026-05-28-claude-cairn-foldback-active-surfacing > Chunk 4).
    "fold-back-ledger": (
        "default-on/foldback_export_scan.py",
        "scripts/foldback_export_scan.py",
    ),
    # Active-surfacing helper (Chunk 8 of the same arc).  Optional
    # helper, but ships alongside the scanner via the same
    # fold-back-ledger module.  Note: this dict allows only one
    # (src,dst) tuple per module name, so the test parametrize
    # iterates over what's here; the second script under the same
    # module is covered by direct assertion in TestInstallPath /
    # TestGeneralizationGate where they verify both scripts install.
    # (The pattern lifecycle-metrics + coordination-tiers establish
    # is one mapping-entry per script; we deviate here only because
    # the fold-back-ledger module ships 2 verbatim scripts.  The
    # _SCRIPT_MODULES dict's parametrize-shape was designed for the
    # 1:1 case; for the 2-scripts-per-module case the test gains a
    # separate assertion below.)
}


# Multi-script modules: modules that ship more than one verbatim
# script.  Verified by an explicit test below (not by the
# _SCRIPT_MODULES parametrize machinery, which assumes 1:1).
_MULTI_SCRIPT_MODULES: dict[str, list[tuple[str, str]]] = {
    "fold-back-ledger": [
        ("default-on/foldback_export_scan.py",
         "scripts/foldback_export_scan.py"),
        ("default-on/foldback_suggest.py",
         "scripts/foldback_suggest.py"),
    ],
}

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _scaffold(target: Path, modules: list[str]) -> int:
    """Scaffold *modules* into *target* via the real CLI entry point."""
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: GenTest\ntest_command: pytest\nmodules:\n"
        + "".join(f"  - {m}\n" for m in modules)
    )
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT)]
    )


def _load_script(path: Path, name: str) -> ModuleType:
    """Import an installed script by file path.

    Registers the module in ``sys.modules`` before ``exec_module`` so
    its ``@dataclass`` definitions resolve (the documented
    spec_from_file_location gotcha)."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_SAMPLE_PROPOSAL = (
    "# Sample proposal\n\n"
    "**Author**: Alice (Strategy)\n"
    "**Date opened**: 2026-05-01\n"
    "**Status**: accepted\n\n"
    "## Review -- Bob (External Reviewer) -- 2026-05-02\n\n"
    "* **[P1]** a finding\n"
    "* **[P2]** another finding\n\n"
    "## Decision -- Carol -- 2026-05-03\n\n"
    "Accept.\n"
)


# ---------------------------------------------------------------------------
# Multi-script-module install assertion
# ---------------------------------------------------------------------------


class TestMultiScriptModules:
    """A module that ships more than one verbatim script needs the
    scaffold to install ALL of them.  The standard parametrize over
    `_SCRIPT_MODULES` covers the 1:1 case only; this test covers
    fold-back-ledger's 2-script case (export_scan + suggest).
    """

    @pytest.mark.parametrize(
        "module_name", sorted(_MULTI_SCRIPT_MODULES)
    )
    def test_multi_script_module_installs_all_scripts(
        self, tmp_path: Path, module_name: str,
    ) -> None:
        assert _scaffold(tmp_path, [module_name]) == 0
        for src_rel, dst_rel in _MULTI_SCRIPT_MODULES[module_name]:
            installed = tmp_path / dst_rel
            source = TEMPLATES_ROOT / "modules" / src_rel
            assert installed.is_file(), (
                f"{dst_rel} not installed (module={module_name})"
            )
            assert installed.read_bytes() == source.read_bytes(), (
                f"{dst_rel} differs from template source -- not verbatim"
            )


# ---------------------------------------------------------------------------
# Install-path (verbatim): warning cleanliness + destination/token agreement
# ---------------------------------------------------------------------------

class TestInstallPath:
    @pytest.mark.parametrize("module_name", sorted(_SCRIPT_MODULES))
    def test_script_installed_verbatim(
        self, tmp_path: Path, module_name: str
    ) -> None:
        """The .py lands at its dst byte-identical to the template
        source; the .md lands in dev/modules/."""
        assert _scaffold(tmp_path, [module_name]) == 0
        src_rel, dst_rel = _SCRIPT_MODULES[module_name]
        installed = tmp_path / dst_rel
        source = TEMPLATES_ROOT / "modules" / src_rel
        assert installed.is_file(), f"{dst_rel} not installed"
        assert installed.read_bytes() == source.read_bytes(), (
            f"{dst_rel} differs from template source -- not verbatim"
        )
        assert (tmp_path / "dev" / "modules" / f"{module_name}.md").is_file()

    def test_verbatim_install_no_spurious_token_or_slot_warnings(
        self, tmp_path: Path
    ) -> None:
        """A verbatim-installed script's InstallResult carries empty
        unfilled-token and block-slot lists -- a code file's braces must
        not be scanned as template tokens / slots."""
        (tmp_path / "dev" / "modules").mkdir(parents=True)
        results = install_modules(
            TEMPLATES_ROOT, tmp_path, {}, ["claim-check", "lifecycle-metrics"]
        )
        script_results = [
            r for r in results if str(r[0]).endswith(".py")
        ]
        assert script_results, "no .py scripts installed"
        for dst, unfilled, slots, _status in script_results:
            assert unfilled == [], f"{dst} reported unfilled tokens {unfilled}"
            assert slots == [], f"{dst} reported block slots {slots}"

    def test_rerun_skips_existing_script(self, tmp_path: Path) -> None:
        """Skip-if-exists protects an edited script on re-scaffold."""
        assert _scaffold(tmp_path, ["claim-check"]) == 0
        installed = tmp_path / "scripts" / "claim_check.py"
        edited = installed.read_text() + "\n# adopter edit\n"
        installed.write_text(edited)
        assert _scaffold(tmp_path, ["claim-check"]) == 0
        assert installed.read_text() == edited, (
            "re-scaffold without --force clobbered an edited script"
        )

    def test_force_overwrites_script(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, ["claim-check"]) == 0
        installed = tmp_path / "scripts" / "claim_check.py"
        installed.write_text("# stale\n")
        cfg = tmp_path / "profile.yml"
        assert main(
            ["--config", str(cfg), "--target", str(tmp_path),
             "--cairn-root", str(CAIRN_ROOT), "--force"]
        ) == 0
        source = TEMPLATES_ROOT / "modules" / "default-on" / "claim_check.py"
        assert installed.read_bytes() == source.read_bytes()

    def test_command_token_agrees_with_install_dst(self) -> None:
        """The default command-token value points at the exact path
        the scaffold installs the script to."""
        defaults = reference_script_token_defaults(
            ["claim-check", "lifecycle-metrics"]
        )
        # claim-check
        cc_dst = next(
            s.dst for s in _MODULE_MAPPINGS["claim-check"] if s.verbatim
        )
        assert defaults["claim_check_command"] == f"python {cc_dst}"
        assert cc_dst == "scripts/claim_check.py"
        # lifecycle-metrics
        lm_dst = next(
            s.dst for s in _MODULE_MAPPINGS["lifecycle-metrics"] if s.verbatim
        )
        assert defaults["metrics_command"] == f"python {lm_dst}"
        assert lm_dst == "tools/lifecycle_metrics.py"


# ---------------------------------------------------------------------------
# Generalization gate (load-bearing): the installed scripts RUN against a
# fresh non-modflow_tools target.
# ---------------------------------------------------------------------------

class TestGeneralizationGate:
    def test_installed_claim_check_runs_on_target(
        self, tmp_path: Path
    ) -> None:
        assert _scaffold(tmp_path, ["claim-check"]) == 0
        cc = _load_script(
            tmp_path / "scripts" / "claim_check.py", "gen_claim_check")
        # A planted broken local path (dev/ exists in the scaffolded
        # target) must hard-flag.
        broken = tmp_path / "broken.md"
        broken.write_text("See `dev/does-not-exist.md` for details.\n")
        res = cc.check_file(broken, tmp_path)
        assert any(f.kind == "path" for f in res.hard_flags), (
            "installed claim_check did not flag a broken repo path"
        )
        # A marker-exempt forward reference must clear.
        marked = tmp_path / "marked.md"
        marked.write_text(
            "Proposed paths: `dev/future-thing.md`.\n"
        )
        res2 = cc.check_file(marked, tmp_path)
        assert res2.hard_flags == [], (
            f"marker-exempt path was flagged: {res2.hard_flags}"
        )

    def test_installed_lifecycle_metrics_runs_on_target(
        self, tmp_path: Path
    ) -> None:
        assert _scaffold(tmp_path, ["lifecycle-metrics"]) == 0
        lm = _load_script(
            tmp_path / "tools" / "lifecycle_metrics.py", "gen_lifecycle")
        (tmp_path / "dev" / "proposals" / "2026-05-01-alice-thing.md").write_text(
            _SAMPLE_PROPOSAL
        )
        rows = lm.proposal_rows(tmp_path)
        stems = [r["stem"] for r in rows]
        assert "2026-05-01-alice-thing" in stems, (
            f"lifecycle_metrics emitted no row for the sample proposal: "
            f"{stems}"
        )
        row = next(r for r in rows if r["stem"] == "2026-05-01-alice-thing")
        # retire-event-blocks (2026-08-24): review_rounds is sourced from
        # the artifact's own dated section headings, a pure function of the
        # text -- no git, no activation cutoff, no `git init` needed for
        # this scaffolded target to prove anything.  `_SAMPLE_PROPOSAL`
        # carries one genuine dated `## Review -- Bob (External
        # Reviewer) -- 2026-05-02` pass, so it counts here exactly as it
        # would over the real corpus history this replaces the event-block
        # reconciler to reach retroactively.
        assert row["review_rounds"] == 1
        assert row["reviewer_agents"] == "Bob"


# ---------------------------------------------------------------------------
# Mixed / upper-case author names in slug pairing
# ---------------------------------------------------------------------------

class TestProposalSlugPairing:
    def test_proposal_slug_strips_mixed_case_author(
        self, tmp_path: Path
    ) -> None:
        """The author segment must not be lowercase-only, else a mixed /
        upper-case author name (Codex, Alice) silently defeats the
        plan<->proposal slug pairing (the match would fail and return the
        whole stem)."""
        assert _scaffold(tmp_path, ["lifecycle-metrics"]) == 0
        lm = _load_script(
            tmp_path / "tools" / "lifecycle_metrics.py", "slug_lifecycle")
        for author in ("Codex", "Alice", "claude2", "claude"):
            stem = f"2026-05-26-{author}-my-thing"
            assert lm._proposal_slug(stem) == "my-thing", (
                f"author={author!r}: slug not stripped (got "
                f"{lm._proposal_slug(stem)!r})"
            )


# ---------------------------------------------------------------------------
# Line-bounds (path:N) negative / boundary coverage
# ---------------------------------------------------------------------------

class TestLineBoundsChecking:
    def _cc(self, tmp_path: Path) -> ModuleType:
        assert _scaffold(tmp_path, ["claim-check"]) == 0
        return _load_script(
            tmp_path / "scripts" / "claim_check.py", "lb_claim_check")

    def test_valid_line_citation_resolves(self, tmp_path: Path) -> None:
        cc = self._cc(tmp_path)
        (tmp_path / "dev" / "sample.md").write_text("a\nb\nc\n")
        doc = tmp_path / "doc.md"
        doc.write_text("See `dev/sample.md:2` for the rule.\n")
        res = cc.check_file(doc, tmp_path)
        assert res.hard_flags == [], (
            f"in-bounds line citation was flagged: {res.hard_flags}"
        )

    def test_out_of_bounds_line_citation_flags(self, tmp_path: Path) -> None:
        cc = self._cc(tmp_path)
        (tmp_path / "dev" / "sample.md").write_text("a\nb\nc\n")
        doc = tmp_path / "doc.md"
        doc.write_text("See `dev/sample.md:100`.\n")
        res = cc.check_file(doc, tmp_path)
        assert any(f.kind == "line-bounds" for f in res.hard_flags), (
            f"out-of-bounds line citation not flagged: {res.hard_flags}"
        )

    def test_missing_file_line_citation_flags(self, tmp_path: Path) -> None:
        cc = self._cc(tmp_path)
        doc = tmp_path / "doc.md"
        doc.write_text("See `dev/missing.md:1` for the rule.\n")
        res = cc.check_file(doc, tmp_path)
        assert any(f.kind == "line-bounds" for f in res.hard_flags), (
            f"line citation to a missing file not flagged: {res.hard_flags}"
        )


# ---------------------------------------------------------------------------
# E -- file-scoped external-path allowance
# ---------------------------------------------------------------------------

class TestExternalPathAllowance:
    def test_case_study_external_paths_exempt_with_allowance(
        self, tmp_path: Path
    ) -> None:
        assert _scaffold(tmp_path, ["claim-check"]) == 0
        cc = _load_script(
            tmp_path / "scripts" / "claim_check.py", "e_claim_check")
        (tmp_path / "case-studies").mkdir()
        # A path whose first segment collides with a real local
        # top-level dir (dev/) but does not resolve -- an external repo's
        # path described in a case study.
        cs = tmp_path / "case-studies" / "external.md"
        cs.write_text(
            "The other repo keeps its board at `dev/their-board.md`.\n"
        )
        flagged = cc.check_file(cs, tmp_path)
        assert any(f.kind == "path" for f in flagged.hard_flags), (
            "without the allowance, a colliding external path must flag"
        )
        cleared = cc.check_file(
            cs, tmp_path, external_allow=["case-studies/*.md"])
        assert cleared.hard_flags == [], (
            f"the allowance did not exempt the case-study path: "
            f"{cleared.hard_flags}"
        )

    def test_genuine_broken_path_still_flags_under_allowance(
        self, tmp_path: Path
    ) -> None:
        """A broken local path in a NON-allowed file still flags even
        when an allowance is set for another glob."""
        assert _scaffold(tmp_path, ["claim-check"]) == 0
        cc = _load_script(
            tmp_path / "scripts" / "claim_check.py", "e2_claim_check")
        normal = tmp_path / "normal.md"
        normal.write_text("See `dev/missing.md`.\n")
        res = cc.check_file(
            normal, tmp_path, external_allow=["case-studies/*.md"])
        assert any(f.kind == "path" for f in res.hard_flags), (
            "a genuine broken local path must still flag under an "
            "unrelated allowance"
        )


# ---------------------------------------------------------------------------
# Dependency gate (stdlib-only)
# ---------------------------------------------------------------------------

class TestDependencyGate:
    @pytest.mark.parametrize("module_name", sorted(_SCRIPT_MODULES))
    def test_installed_script_is_stdlib_only(
        self, tmp_path: Path, module_name: str
    ) -> None:
        """The installed script imports only the standard library, so it
        never fails with ModuleNotFoundError in a bare target.  If a
        third-party dep is ever introduced, this test forces the scaffold
        to declare / contribute it."""
        assert _scaffold(tmp_path, [module_name]) == 0
        _src_rel, dst_rel = _SCRIPT_MODULES[module_name]
        tree = ast.parse((tmp_path / dst_rel).read_text())
        top_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top_modules.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    top_modules.add(node.module.split(".")[0])
        stdlib = set(sys.stdlib_module_names)
        non_stdlib = {m for m in top_modules if m not in stdlib}
        assert non_stdlib == set(), (
            f"{dst_rel} imports non-stdlib module(s): {sorted(non_stdlib)}"
        )


# ---------------------------------------------------------------------------
# VCS robustness (lifecycle_metrics)
# ---------------------------------------------------------------------------

class TestVcsRobustness:
    def test_no_git_target_degrades(self, tmp_path: Path) -> None:
        """No .git in the target: the git-log commit-timestamp
        augmentation (``hours_*``/``stage_timestamp_reliability``) quietly
        degrades to ``Best-effort`` rather than raising, exactly as it
        always has for an unavailable-VCS target. Unlike that transition-
        kind data, ``review_rounds`` and the other review-pass-sourced
        columns (retire-event-blocks, 2026-08-24) need no git at all --
        they are a pure function of the artifact's own text -- so this
        no-git target does not change their population; see
        `test_installed_lifecycle_metrics_runs_on_target` for the
        review-pass columns this same fixture populates."""
        assert _scaffold(tmp_path, ["lifecycle-metrics"]) == 0
        lm = _load_script(
            tmp_path / "tools" / "lifecycle_metrics.py", "f4_lifecycle")
        (tmp_path / "dev" / "proposals" / "2026-05-01-alice-thing.md").write_text(
            _SAMPLE_PROPOSAL
        )
        # No exception, and the stage-timestamp reliability degrades.
        rows = lm.proposal_rows(tmp_path)
        assert rows, "no rows emitted on a no-git target"
        assert rows[0]["stage_timestamp_reliability"] == "Best-effort"

    def test_main_branch_target_runs(self, tmp_path: Path) -> None:
        """A git target whose default branch is 'main' (not 'master')
        runs cleanly -- no branch-name assumption. `proposal_rows` must
        not raise regardless of what the git-log commit-timestamp
        augmentation finds; review-pass columns (retire-event-blocks) read
        no git state at all, so this case is purely about the
        `hours_*`/`stage_timestamp_reliability` augmentation's own branch-
        name independence."""
        import subprocess
        assert _scaffold(tmp_path, ["lifecycle-metrics"]) == 0
        (tmp_path / "dev" / "proposals" / "2026-05-01-alice-thing.md").write_text(
            _SAMPLE_PROPOSAL
        )
        env_ok = True
        try:
            subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)],
                           check=True, capture_output=True)
            subprocess.run(["git", "-C", str(tmp_path), "add", "-A"],
                           check=True, capture_output=True)
            subprocess.run(
                ["git", "-C", str(tmp_path),
                 "-c", "user.email=t@t.t", "-c", "user.name=t",
                 "commit", "-qm", "Open proposal alice thing"],
                check=True, capture_output=True,
            )
        except (OSError, subprocess.CalledProcessError):
            env_ok = False
        if not env_ok:
            pytest.skip("git not available for the main-branch case")
        lm = _load_script(
            tmp_path / "tools" / "lifecycle_metrics.py", "f4b_lifecycle")
        rows = lm.proposal_rows(tmp_path)  # must not raise
        assert any(r["stem"] == "2026-05-01-alice-thing" for r in rows)


def test_lifecycle_metrics_csv_neutralizes_formula_injection() -> None:
    """format_csv prefixes a formula-leading cell (= + - @, tab, CR) with a
    single quote so a spreadsheet treats it as literal text, not a formula
    (security-hardening Chunk 9)."""
    lm = _load_script(
        TEMPLATES_ROOT / "modules" / "default-on" / "lifecycle_metrics.py",
        "lm_csvsafe")
    out = lm.format_csv([{"title": "=cmd|'/calc'!A1", "n": 3}], ["title", "n"])
    assert "'=cmd" in out, "formula-leading cell was not neutralized"
    # A benign cell is untouched (no spurious leading quote).
    benign = lm.format_csv([{"title": "ok title", "n": 3}], ["title", "n"])
    assert "'ok title" not in benign
