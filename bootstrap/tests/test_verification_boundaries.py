"""Focused guards for the implementation verification boundaries.

These tests guard the prospective governing/template contract and the existing
quality-gate composition. They do not parse filled verification records or
select tests automatically; both are explicit v1 omissions.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


ROOT = Path(__file__).resolve().parents[2]
SELF_AGENTS = ROOT / "AGENTS.md"
ADOPTER_AGENTS = ROOT / "templates" / "core" / "AGENTS.md"
PLANS_DOCTRINE = ROOT / "doctrine" / "plans.md"
REVIEW_DOCTRINE = ROOT / "doctrine" / "dual-review.md"
QUALITY_GATE = ROOT / "scripts" / "quality_gate.py"
SELF_PLAN_TEMPLATE = ROOT / "dev" / "plans" / "_template.md"
ADOPTER_PLAN_TEMPLATE = ROOT / "templates" / "core" / "dev" / "plans" / "_template.md"
SELF_PROPOSAL_TEMPLATE = ROOT / "dev" / "proposals" / "_template.md"
ADOPTER_PROPOSAL_TEMPLATE = (
    ROOT / "templates" / "core" / "dev" / "proposals" / "_template.md"
)

FRESH_RUN_TRIGGERS = (
    "no valid Boundary B record exists",
    "unrecorded cross-surface dependency",
    "skip, xfail, or xpass",
    "review sharpening changes implementation, tests, executable templates, or",
    "trust ceremony that explicitly requires",
    "concrete reason to distrust or falsify",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_quality_gate(name: str = "_verification_boundaries_quality_gate") -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, QUALITY_GATE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _operational_violations(text: str) -> list[str]:
    text = " ".join(text.split())
    required = {
        "Boundary A": "scoped iteration",
        "Boundary B": "stable integration evidence",
        "Boundary C": "independent review",
        "full fallback": "cannot be bounded confidently",
        "record heading": "## Implementation verification -- <agent> -- YYYY-MM-DD",
        "invalidation": "implementation/test/executable-template/fixture bytes",
        "release separation": "separate strict ceremony",
    }
    return [label for label, token in required.items() if token not in text]


def test_both_operational_surfaces_fail_to_full() -> None:
    for path in (SELF_AGENTS, ADOPTER_AGENTS):
        assert _operational_violations(_read(path)) == [], path


def test_operational_guard_detects_removed_full_fallback() -> None:
    text = _read(SELF_AGENTS)
    mutated = text.replace("cannot be bounded confidently", "looks broad", 1)
    assert "full fallback" in _operational_violations(mutated)


def test_installed_operational_rule_is_project_general() -> None:
    text = _read(ADOPTER_AGENTS)
    cairn_only = (
        "bootstrap/tests",
        "scripts/quality_gate.py",
        "Python 3.13",
        "Cairn's ordinary pair",
    )
    assert not [token for token in cairn_only if token in text]
    assert "configured full suite" in text
    assert "configured interpreter/runtime" in text


def test_static_quality_composition_does_not_dispatch_pytest(monkeypatch) -> None:
    qg = _load_quality_gate()
    calls: list[str] = []

    def order(*_args, **_kwargs):
        calls.append("order-independence")
        return []

    def neutrality(*_args, **_kwargs):
        calls.append("neutrality")
        return []

    def redundancy(*_args, **_kwargs):
        calls.append("redundancy")
        return []

    monkeypatch.setattr(qg, "_run_order_independence", order)
    monkeypatch.setattr(qg, "_run_neutrality", neutrality)
    monkeypatch.setattr(qg, "_run_redundancy", redundancy)

    report = qg.run_gates(["neutrality", "redundancy"], ROOT)

    assert not report.failed
    assert calls == ["neutrality", "redundancy"]


def test_quality_gate_cli_default_still_selects_every_leg(monkeypatch, tmp_path) -> None:
    qg = _load_quality_gate("_verification_boundaries_quality_gate_default")
    selected: list[str] = []

    def capture(sub_gates, *_args, **_kwargs):
        selected.extend(sub_gates)
        return qg.GateReport()

    monkeypatch.setattr(qg, "run_gates", capture)
    monkeypatch.setattr(qg, "_print_report", lambda *_a, **_k: None)

    assert qg.main(["--root", str(tmp_path)]) == 0
    assert selected == ["order-independence", "neutrality", "redundancy"]


def _record_violations(text: str) -> list[str]:
    text = " ".join(text.split())
    required = (
        "## Implementation verification -- <agent> -- YYYY-MM-DD",
        "**Tested commit**",
        "**Reviewed range**",
        "**Interpreter/runtime**",
        "**Pre-run state**",
        "**Post-run state**",
        "**Non-pass disposition**",
        "**Plan-specific acceptance commands**",
        "**Known omissions**",
        "implementation, tests, executable templates, or fixtures",
        "never satisfies or shortens a release gate",
        "not a signed receipt or parser-enforced claim",
    )
    return [token for token in required if token not in text]


def test_plan_doctrine_binds_record_to_tested_range() -> None:
    assert _record_violations(_read(PLANS_DOCTRINE)) == []


def test_record_schema_guard_detects_removed_reviewed_range() -> None:
    text = _read(PLANS_DOCTRINE)
    mutated = text.replace("**Reviewed range**", "**Change description**", 1)
    assert "**Reviewed range**" in _record_violations(mutated)


def _review_violations(text: str) -> list[str]:
    text = " ".join(text.split())
    required = (
        "targeted falsification",
        "Copying the implementation's broad command does not satisfy",
        *FRESH_RUN_TRIGGERS,
        "not authentication, malicious-committer protection, or a",
        "release optimization",
    )
    return [token for token in required if token not in text]


def test_review_doctrine_requires_targeted_falsification_and_six_triggers() -> None:
    assert _review_violations(_read(REVIEW_DOCTRINE)) == []


def test_plan_and_review_doctrine_share_fresh_run_triggers() -> None:
    for path in (PLANS_DOCTRINE, REVIEW_DOCTRINE):
        normalized = " ".join(_read(path).split())
        assert not [token for token in FRESH_RUN_TRIGGERS if token not in normalized], path


def test_review_reuse_guard_detects_unconditional_reuse() -> None:
    text = _read(REVIEW_DOCTRINE)
    mutated = text.replace("no valid Boundary B record exists", "a record exists", 1)
    assert "no valid Boundary B record exists" in _review_violations(mutated)


RECORD_FIELDS = (
    "Tested commit",
    "Reviewed range",
    "Interpreter/runtime",
    "Pre-run state",
    "Post-run state",
    "Command",
    "Exit",
    "Outcomes",
    "Elapsed",
    "Non-pass disposition",
    "Plan-specific acceptance commands",
    "Known omissions",
)


def _plan_template_violations(text: str) -> list[str]:
    verification = text.split("<!-- cairn:slot verification-commands -->", 1)[1]
    verification = verification.split("<!-- cairn:end verification-commands -->", 1)[0]
    normalized_verification = " ".join(verification.split())
    normalized_all = " ".join(text.split())
    verification_required = (
        "Implementation verification -- <agent> -- YYYY-MM-DD",
        "reviewed mapping",
        "full suite",
        *RECORD_FIELDS,
    )
    review_required = (
        "targeted falsification",
        *FRESH_RUN_TRIGGERS,
    )
    return [
        *[token for token in verification_required if token not in normalized_verification],
        *[token for token in review_required if token not in normalized_all],
    ]


def test_both_plan_templates_carry_record_and_review_contract() -> None:
    for path in (SELF_PLAN_TEMPLATE, ADOPTER_PLAN_TEMPLATE):
        text = _read(path)
        assert _plan_template_violations(text) == [], path
        assert not any(
            line.startswith("## Implementation verification")
            for line in text.splitlines()
        ), path


def test_plan_template_guard_detects_removed_reviewed_range() -> None:
    text = _read(SELF_PLAN_TEMPLATE)
    mutated = text.replace("Reviewed range", "Change description", 1)
    assert "Reviewed range" in _plan_template_violations(mutated)


def test_both_proposal_templates_reject_speed_as_coverage() -> None:
    for path in (SELF_PROPOSAL_TEMPLATE, ADOPTER_PROPOSAL_TEMPLATE):
        normalized = " ".join(_read(path).split())
        required = (
            "speed alone does not establish affected coverage",
            "unknown or uncertain scope falls back to the full suite",
            "test homes",
            "public paths",
        )
        assert not [token for token in required if token not in normalized], path

    assert "There is no separate slow / networked tier" not in _read(
        SELF_PROPOSAL_TEMPLATE
    )
