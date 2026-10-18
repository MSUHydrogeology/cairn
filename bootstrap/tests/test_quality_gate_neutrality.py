"""Neutrality sub-gate -- abuse-test coverage.

Pins the seven recovery signals from plan-review finding #3:

* Sanctioned exceptions pass with rationale echoed in the report.
* Unsanctioned vendor / project tokens fail.
* A line exemption does NOT bleed to the line after the target line.
* A block exemption WITH matching end works; orphan begin fails.
* Empty rationale fails (rationale required on every directive).
* ``<!-- case-study -->`` exempts a file under ``case-studies/`` but
  FAILS when placed elsewhere.
* ANY exemption directive inside ``templates/`` fails (templates ship
  to adopters; a leak there would propagate).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
QG_SRC = CAIRN_ROOT / "scripts" / "quality_gate.py"

pytestmark = pytest.mark.skipif(
    not QG_SRC.exists(), reason="quality_gate.py not available",
)


def _load_qg(name: str = "_quality_gate_neutrality_under_test") -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, QG_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def qg() -> ModuleType:
    return _load_qg()


def _run(qg: ModuleType, tmp_path: Path) -> list:
    return qg._run_neutrality(tmp_path)


def _failures(findings):
    return [f for f in findings if f.severity == "fail"]


def _infos(findings):
    return [f for f in findings if f.severity == "info"]


class TestNeutralityScanScope:
    def test_unsanctioned_vendor_token_fails(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "leak.md").write_text(
            "We talked about Claude during the review.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any("Claude" in f.message for f in fs), fs

    def test_unsanctioned_project_token_fails(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "leak.md").write_text(
            "Built first in modflow_tools, then ported.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any("modflow_tools" in f.message for f in fs), fs

    def test_clean_prose_no_findings(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "ok.md").write_text(
            "# Clean doctrine\n\nNothing vendor-flavoured here.\n"
        )
        assert _failures(_run(qg, tmp_path)) == []

    def test_dotpy_outside_templates_not_scanned(self, qg, tmp_path):
        # Code files outside templates/ should NOT trip the lint --
        # tests, scripts, etc. legitimately name the reference
        # deployment.
        (tmp_path / "bootstrap" / "tests").mkdir(parents=True)
        (tmp_path / "bootstrap" / "tests" / "test_x.py").write_text(
            "# Ported from modflow_tools' similar test.\n"
            "# Reviewed by Codex.\n"
        )
        assert _failures(_run(qg, tmp_path)) == []


class TestLineExemption:
    def test_vendor_ok_on_same_line_exempts(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "ok.md").write_text(
            "The Claude assistant <!-- vendor-ok: case study sentence -->\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert fs == [], fs
        infos = _infos(_run(qg, tmp_path))
        assert any("case study sentence" in i.message for i in infos)

    def test_vendor_ok_directive_only_above_exempts_next_line(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "ok.md").write_text(
            "<!-- vendor-ok: documented reason -->\n"
            "The Claude reference here is exempt.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert fs == [], fs

    def test_line_exempt_does_NOT_bleed_past_one_line(self, qg, tmp_path):
        # An exemption on line N does NOT exempt line N+2 (only the
        # *same* line or the *immediately next* line).
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "leak.md").write_text(
            "<!-- vendor-ok: only the next line -->\n"
            "Claude exempted by directive above.\n"
            "Claude on this line is NOT exempted.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert len(fs) == 1, [f.message for f in fs]
        assert fs[0].line == 3

    def test_empty_rationale_fails(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "bad.md").write_text(
            "<!-- vendor-ok: -->\n"
            "Claude here.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any(
            "empty rationale" in f.message for f in fs
        ), [f.message for f in fs]


class TestBlockExemption:
    def test_block_exempts_tokens_inside(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "ok.md").write_text(
            "<!-- vendor-ok-begin: section quotes a vendor doc -->\n"
            "Claude said X.  Codex said Y.\n"
            "<!-- vendor-ok-end -->\n"
            "Outside the block: Claude here is NOT exempted.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert len(fs) == 1, [f.message for f in fs]
        assert fs[0].line == 4

    def test_orphan_block_begin_fails(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "orphan.md").write_text(
            "<!-- vendor-ok-begin: forgot to close -->\n"
            "Claude here.\n"
            "End of file with no vendor-ok-end.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any(
            "orphan vendor-ok-begin" in f.message for f in fs
        ), [f.message for f in fs]

    def test_orphan_block_end_fails(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "orphan.md").write_text(
            "Some prose.\n"
            "<!-- vendor-ok-end -->\n"
            "More prose.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any(
            "vendor-ok-end without matching vendor-ok-begin" in f.message
            for f in fs
        ), [f.message for f in fs]

    def test_block_empty_rationale_fails(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "bad.md").write_text(
            "<!-- vendor-ok-begin: -->\n"
            "Claude.\n"
            "<!-- vendor-ok-end -->\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any(
            "empty rationale" in f.message for f in fs
        ), [f.message for f in fs]


class TestCaseStudyMarker:
    def test_case_study_in_case_studies_dir_exempts_file(self, qg, tmp_path):
        (tmp_path / "case-studies").mkdir()
        (tmp_path / "case-studies" / "modflow_tools.md").write_text(
            "<!-- case-study -->\n"
            "# modflow_tools as the reference deployment.\n\n"
            "Built with Claude and reviewed by Codex.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert fs == [], [f.message for f in fs]

    def test_case_study_outside_case_studies_dir_fails(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "leak.md").write_text(
            "<!-- case-study -->\n"
            "Claude here would be exempt if this marker were valid.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any(
            "case-study marker outside" in f.message for f in fs
        ), [f.message for f in fs]


class TestTemplatesDirectiveForbidden:
    def test_vendor_ok_in_templates_fails(self, qg, tmp_path):
        (tmp_path / "templates" / "modules" / "team-gated").mkdir(parents=True)
        (tmp_path / "templates" / "modules" / "team-gated" / "x.md").write_text(
            "<!-- vendor-ok: docs example -->\n"
            "Adopter docs.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any(
            "forbidden inside cairn/templates/" in f.message for f in fs
        ), [f.message for f in fs]

    def test_case_study_in_templates_fails(self, qg, tmp_path):
        (tmp_path / "templates" / "modules").mkdir(parents=True)
        (tmp_path / "templates" / "modules" / "x.md").write_text(
            "<!-- case-study -->\n"
            "Templated case study (would propagate to adopters).\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any(
            "forbidden inside cairn/templates/" in f.message for f in fs
        ), [f.message for f in fs]

    def test_clean_template_passes(self, qg, tmp_path):
        (tmp_path / "templates" / "modules").mkdir(parents=True)
        (tmp_path / "templates" / "modules" / "x.md").write_text(
            "# Clean template content\n\nNo directives, no vendor tokens.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert fs == [], [f.message for f in fs]

    def test_vendor_token_in_template_without_directive_fails(self, qg, tmp_path):
        """Regression: a vendor / project
        token inside `templates/` must fail even when no exemption
        directive is present.  Previously, the early-return after the
        directive-forbidden check silently let template token leaks
        through unscanned.

        Templates ship to adopter repos; a leaked vendor / project
        token in a template propagates downstream to every adopter,
        which is the worst-case impact for the neutrality lint.
        """
        (tmp_path / "templates" / "core").mkdir(parents=True)
        (tmp_path / "templates" / "core" / "AGENTS.md").write_text(
            "Claude should not ship in adopter template prose.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any(
            "Claude" in f.message and "templates/" in f.message for f in fs
        ), [f.message for f in fs]

    def test_project_token_in_template_without_directive_fails(self, qg, tmp_path):
        """Companion to the vendor-token regression: project tokens
        (`modflow_tools`, `LHM`) also propagate to adopters if leaked
        in a template, so they must fail there too.
        """
        (tmp_path / "templates" / "modules").mkdir(parents=True)
        (tmp_path / "templates" / "modules" / "leak.md").write_text(
            "Borrowed from modflow_tools' equivalent module.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any(
            "modflow_tools" in f.message for f in fs
        ), [f.message for f in fs]


class TestDirectiveShownInProseNotParsed:
    """Documentation that *shows* an exemption directive (inside
    backticks, or mid-prose) must not be parsed as a live directive --
    mirrors the existing claim_check.py rule.  Block + file markers
    require the line to be a directive-only HTML comment.
    """

    def test_block_marker_in_backticks_not_parsed(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "howto.md").write_text(
            "# Documenting the syntax\n\n"
            "Wrap a block in `<!-- vendor-ok-begin: ... -->` and "
            "`<!-- vendor-ok-end -->` -- shown here in backticks\n"
            "so the gate does not treat it as a live marker.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert fs == [], [f.message for f in fs]

    def test_case_study_marker_in_backticks_not_parsed(self, qg, tmp_path):
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "howto.md").write_text(
            "# Documenting the syntax\n\n"
            "A `<!-- case-study -->` marker at the file head exempts the\n"
            "whole file under cairn/case-studies/.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert fs == [], [f.message for f in fs]


class TestExemptionReporting:
    def test_exemption_rationale_appears_in_report(self, qg, tmp_path):
        (tmp_path / "doctrine").mkdir()
        (tmp_path / "doctrine" / "ok.md").write_text(
            "<!-- vendor-ok: cite of a real review -->\n"
            "Codex's pre-cut review was sharp.\n"
        )
        infos = _infos(_run(qg, tmp_path))
        # The reason text appears in an info finding for audit.
        assert any(
            "cite of a real review" in i.message for i in infos
        ), [i.message for i in infos]


class TestTemplatesScanComments:
    """Everything under ``templates/`` ships to adopters, so a vendor name
    in a comment line is a leak exactly as much as one in prose.  A comment
    line used to be skipped on the grounds that it carries no prose; that
    skip hid names credited to reviewers.
    """

    def test_vendor_name_in_a_whole_line_html_comment_fails(self, qg, tmp_path):
        (tmp_path / "templates" / "modules").mkdir(parents=True)
        (tmp_path / "templates" / "modules" / "x.md").write_text(
            "# A template\n"
            "<!-- reviewed by Claude -->\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any(
            "Claude" in f.message and f.line == 2 for f in fs
        ), [(f.line, f.message) for f in fs]

    def test_whole_line_directive_that_names_a_vendor_fails_twice(
        self, qg, tmp_path,
    ):
        (tmp_path / "templates" / "modules").mkdir(parents=True)
        (tmp_path / "templates" / "modules" / "x.md").write_text(
            "<!-- vendor-ok: Claude example -->\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert len(fs) == 2, [(f.line, f.message) for f in fs]
        assert any("forbidden inside cairn/templates/" in f.message for f in fs)
        assert any("token `Claude`" in f.message for f in fs)


class TestTemplatesScanFileTypes:
    """The file types read under ``templates/`` are the types the scaffold
    ships; ``.json`` and ``.txt`` ship, so they are read.
    """

    def test_vendor_name_in_a_txt_file_fails(self, qg, tmp_path):
        (tmp_path / "templates" / "core").mkdir(parents=True)
        (tmp_path / "templates" / "core" / "notes.txt").write_text(
            "Written with Claude.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any("Claude" in f.message for f in fs), fs

    def test_vendor_name_in_a_json_file_fails(self, qg, tmp_path):
        (tmp_path / "templates" / "core").mkdir(parents=True)
        (tmp_path / "templates" / "core" / "policy.json").write_text(
            '{"reviewer": "Claude"}\n'
        )
        fs = _failures(_run(qg, tmp_path))
        assert any("Claude" in f.message for f in fs), fs


class TestTemplatesScanNames:
    """Tool names that the routing table lists as supported harnesses are
    names an adopter-facing file must not carry either.
    """

    @pytest.mark.parametrize("name", ["Copilot", "Windsurf", "Cline", "OpenCode"])
    def test_added_tool_names_fail_in_a_template(self, qg, tmp_path, name):
        (tmp_path / "templates" / "modules").mkdir(parents=True)
        (tmp_path / "templates" / "modules" / "x.md").write_text(
            f"Works with {name} too.\n"
        )
        fs = _failures(_run(qg, tmp_path))
        assert any(f"`{name}`" in f.message for f in fs), [
            f.message for f in fs
        ]
