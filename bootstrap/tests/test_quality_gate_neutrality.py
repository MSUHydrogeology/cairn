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
