"""Focused guards for the implementation verification boundaries.

These tests guard the prospective governing/template contract and the existing
quality-gate composition. They do not parse filled verification records or
select tests automatically; both are explicit v1 omissions.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType

import pytest


ROOT = Path(__file__).resolve().parents[2]
SELF_AGENTS = ROOT / "AGENTS.md"
ADOPTER_AGENTS = ROOT / "templates" / "core" / "AGENTS.md"
PLANS_DOCTRINE = ROOT / "docs" / "methodology" / "plans.md"
REVIEW_DOCTRINE = ROOT / "docs" / "methodology" / "dual-review.md"
QUALITY_GATE = ROOT / "scripts" / "quality_gate.py"
SELF_PLAN_TEMPLATE = ROOT / "dev" / "plans" / "_template.md"
ADOPTER_PLAN_TEMPLATE = ROOT / "templates" / "core" / "dev" / "plans" / "_template.md"
SELF_PROPOSAL_TEMPLATE = ROOT / "dev" / "proposals" / "_template.md"
ADOPTER_PROPOSAL_TEMPLATE = (
    ROOT / "templates" / "core" / "dev" / "proposals" / "_template.md"
)
TESTING_MODULES = (
    ROOT / "dev" / "modules" / "testing-discipline.md",
    ROOT / "templates" / "modules" / "team-gated" / "testing-discipline.md",
)

REPLACEMENT_RECORD_TRIGGERS = (
    "no valid Boundary B record exists",
    "unrecorded cross-surface dependency",
    "skip, xfail, or xpass",
    "a later change is made after a valid final integration record",
    "trust ceremony explicitly requires",
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
        "Boundary A": "Boundary A is scoped iteration",
        "Boundary B mode": "Boundary B mode is `bounded | wide`",
        "Boundary C": "Boundary C is independent falsification",
        "wide owning coverage": "wide covers owning test families",
        "contract and ceremony fence": "Use `wide` for a contract or trust-ceremony surface",
        "known check blocks completion": "future certification cannot close it",
        "separate certification": "Change verification and tree certification are separate",
        "record heading": "## Implementation verification -- <agent> -- YYYY-MM-DD",
        "integration follows review": "after code review",
        "release separation": "Release verification is a separate strict ceremony",
    }
    return [label for label, token in required.items() if token not in text]


def test_both_operational_surfaces_separate_change_checks_from_tree_certification() -> None:
    for path in (SELF_AGENTS, ADOPTER_AGENTS):
        assert _operational_violations(_read(path)) == [], path


def test_operational_guard_detects_removed_wide_surface_fence() -> None:
    text = " ".join(_read(SELF_AGENTS).split())
    mutated = text.replace(
        "Use `wide` for a contract or trust-ceremony surface",
        "Use `bounded` for a contract or trust-ceremony surface", 1)
    assert "contract and ceremony fence" in _operational_violations(mutated)


def test_installed_operational_rule_is_project_general() -> None:
    text = " ".join(_read(ADOPTER_AGENTS).split())
    cairn_only = (
        "bootstrap/tests",
        "scripts/quality_gate.py",
        "Python 3.13",
        "Cairn's ordinary pair",
    )
    assert not [token for token in cairn_only if token in text]
    assert "Required project checks and ceremonies remain owed" in text
    assert "a whole suite runs when an applicable requirement calls for it" in text
    assert "configured interpreter/runtime" in text


def test_scoped_defaults_reach_core_templates_and_optional_module() -> None:
    surfaces = (
        SELF_AGENTS, ADOPTER_AGENTS, PLANS_DOCTRINE, REVIEW_DOCTRINE,
        SELF_PLAN_TEMPLATE, ADOPTER_PLAN_TEMPLATE, SELF_PROPOSAL_TEMPLATE,
        ADOPTER_PROPOSAL_TEMPLATE, *TESTING_MODULES,
    )
    for path in surfaces:
        text = " ".join(_read(path).split()).lower()
        for phrase in (
            "callers", "configuration", "public", "local",
            "shared", "uncertain", "review",
        ):
            assert phrase in text, (path, phrase)

    for path in (SELF_AGENTS, ADOPTER_AGENTS, PLANS_DOCTRINE,
                 SELF_PLAN_TEMPLATE, ADOPTER_PLAN_TEMPLATE):
        text = " ".join(_read(path).split()).lower()
        assert "unit checks" in text, path
        assert "contract checks" in text, path
        assert "integration checks" in text, path
        assert "small workflow" in text, path

    for path in (SELF_AGENTS, ADOPTER_AGENTS, PLANS_DOCTRINE):
        text = " ".join(_read(path).split()).lower()
        assert "routine project operations use affected checks" in text, path
        assert "representative cross-component workflow" in text, path


def test_optional_testing_module_copies_are_identical() -> None:
    assert _read(TESTING_MODULES[0]) == _read(TESTING_MODULES[1])


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
        "**Boundary B mode**",
        "**Boundary B mode**: bounded | wide",
        "Tree certification -- <tested SHA>",
        "existing evidence home",
        "shared project history",
        "git log --all --grep='Tree certification --'",
        "**Tested commit**",
        "**Reviewed range**",
        "**Interpreter/runtime**",
        "**Pre-run state**",
        "**Post-run state**",
        "**Non-pass disposition**",
        "**Plan-specific acceptance commands**",
        "**Known omissions**",
        "After code review, or after",
        "never satisfies or shortens a release gate",
        "not a signed receipt or parser-enforced claim",
    )
    return [token for token in required if token not in text]


def test_plan_doctrine_binds_record_to_tested_range() -> None:
    assert _record_violations(_read(PLANS_DOCTRINE)) == []


def test_actual_certification_has_one_discoverable_shared_record() -> None:
    text = " ".join(_read(PLANS_DOCTRINE).split())
    for token in (
        "Record each actual tree-certification run once",
        "release cut or re-anchor",
        "useful commit message in shared project history",
        "including failures",
        "Do not backfill archived plans",
        "An absent record does not prove a run passed",
    ):
        assert token in text, token
    for path in (SELF_AGENTS, ADOPTER_AGENTS, SELF_PLAN_TEMPLATE,
                 ADOPTER_PLAN_TEMPLATE, PLANS_DOCTRINE, REVIEW_DOCTRINE):
        assert "Certified by: pending" not in _read(path), path


def _shipped_record_guidance_violations(text: str) -> list[str]:
    text = " ".join(text.split())
    required = (
        "Record each actual tree-certification run once",
        "existing release or re-anchor evidence",
        "Tree certification -- <tested SHA>",
        "useful commit message in shared project history",
        "After fetching the relevant shared refs",
        "git log --all --grep='Tree certification --'",
        "any failures",
        "Do not create a commit just for this record",
        "An absent record does not show that a run passed",
    )
    return [phrase for phrase in required if phrase not in text]


def test_shipped_guidance_records_and_finds_actual_runs() -> None:
    for path in (ADOPTER_AGENTS, ADOPTER_PLAN_TEMPLATE):
        text = _read(path)
        assert _shipped_record_guidance_violations(text) == [], path

    control = " ".join(_read(ADOPTER_AGENTS).split())
    assert "After fetching the relevant shared refs" in control
    mutant = control.replace(
        "After fetching the relevant shared refs",
        "Search without fetching shared refs", 1)
    assert "After fetching the relevant shared refs" in (
        _shipped_record_guidance_violations(mutant))


def test_record_schema_guard_detects_removed_reviewed_range() -> None:
    text = _read(PLANS_DOCTRINE)
    mutated = text.replace("**Reviewed range**", "**Change description**", 1)
    assert "**Reviewed range**" in _record_violations(mutated)


def _review_violations(text: str) -> list[str]:
    text = " ".join(text.split())
    required = (
        "Falsification (targeted review before B)",
        "command alone does not show independent falsification",
        *REPLACEMENT_RECORD_TRIGGERS,
        "do not automatically call for a whole-tree run",
        "not authentication, malicious-committer protection, or a",
        "release optimization",
    )
    return [token for token in required if token not in text]


def test_review_doctrine_requires_targeted_falsification_and_replacement_triggers() -> None:
    assert _review_violations(_read(REVIEW_DOCTRINE)) == []


def test_plan_and_review_doctrine_share_record_replacement_triggers() -> None:
    for path in (PLANS_DOCTRINE, REVIEW_DOCTRINE):
        normalized = " ".join(_read(path).split())
        assert not [token for token in REPLACEMENT_RECORD_TRIGGERS if token not in normalized], path
        body = re.search(
            r"record-replacement triggers applies:(.*?)\n\nThese triggers require scoped",
            _read(path), re.S)
        assert body, path
        numbered = re.findall(r"^\s*(\d+)\.", body.group(1), re.M)
        assert numbered == ["1", "2", "3", "4", "5", "6"], (path, numbered)


#: The current scoped-evidence contract: bounded covers its reviewed map;
#: wide covers owning families and known paths when narrower bounds are weak.
_CHANGE_VERIFICATION_OBLIGATIONS = {
    "bounded records cover affected behavior and consumers": (
        "bounded", "affected behavior and consumers",
    ),
    "wide records cover owning families and known paths": (
        "wide", "owning test families", "integration and public paths",
        "standing gates",
    ),
    "contract and trust-ceremony surfaces use wide mode": (
        "Use `wide` for a contract or trust-ceremony surface",
    ),
    "the record declares bounded or wide mode": (
        "Boundary B mode", "bounded | wide",
    ),
}

#: Every surface carrying the change-verification contract. The two `AGENTS.md`
#: copies stay semantically parallel and lexically different -- Cairn names its
#: own commands, the adopter copy stays project-general.
_CHANGE_VERIFICATION_SURFACES = (
    SELF_AGENTS, ADOPTER_AGENTS, PLANS_DOCTRINE,
    REVIEW_DOCTRINE, SELF_PLAN_TEMPLATE, ADOPTER_PLAN_TEMPLATE,
)


@pytest.mark.parametrize("path", _CHANGE_VERIFICATION_SURFACES,
                         ids=lambda p: str(p.relative_to(ROOT)))
@pytest.mark.parametrize("label,tokens", sorted(_CHANGE_VERIFICATION_OBLIGATIONS.items()))
def test_change_verification_contract_reaches_every_surface(
        path, label: str, tokens) -> None:
    text = " ".join(_read(path).split())
    missing = [tok for tok in tokens if tok not in text]
    assert not missing, (
        f"{path} no longer carries the change-verification obligation {label!r} "
        f"(missing {missing}); a surface that loses the mode or coverage "
        f"contract ships a different rule than the rest."
    )


def _change_verification_violations(text: str) -> list[str]:
    """Labels of the change-verification obligations absent from *text*."""
    normalized = " ".join(text.split())
    return [label for label, tokens in _CHANGE_VERIFICATION_OBLIGATIONS.items()
            if [tok for tok in tokens if tok not in normalized]]


def test_change_verification_guard_detects_removed_wide_fence() -> None:
    """Replacing the required wide mode with bounded must fail the guard.

    This asserts the *violation function* reports the loss -- the pattern used
    by `test_operational_guard_detects_removed_wide_surface_fence` and
    `test_review_reuse_guard_detects_unconditional_reuse` above. An earlier
    version of this test asserted only that a token was absent from text it
    had just removed it from, which passed even against an empty file: a
    tautology wearing a mutant's docstring.
    """
    intact = " ".join(_read(SELF_AGENTS).split())
    assert _change_verification_violations(intact) == []

    mutated = intact.replace(
        "Use `wide` for a contract or trust-ceremony surface",
        "Use `bounded` for a contract or trust-ceremony surface", 1)
    assert "contract and trust-ceremony surfaces use wide mode" in \
        _change_verification_violations(mutated)


#: The three governing surfaces -- not the plan templates, which do not carry
#: the already-open-plan rule.
_APPLICABILITY_SURFACES = (SELF_AGENTS, ADOPTER_AGENTS, PLANS_DOCTRINE)


@pytest.mark.parametrize("path", _APPLICABILITY_SURFACES,
                         ids=lambda p: str(p.relative_to(ROOT)))
def test_already_open_plans_can_switch_by_one_line(path) -> None:
    """An open plan may opt into the new contract without rewriting its records."""
    normalized = " ".join(_read(path).split())
    assert "already-open plan may switch to this contract by one line in its record" in normalized, (
        f"{path} no longer states the one-line path for an already-open plan to "
        f"adopt this verification contract."
    )


def test_change_verification_guard_is_not_satisfied_by_an_empty_file() -> None:
    """An empty document carries none of the scoped-evidence obligations."""
    assert len(_change_verification_violations("")) == len(
        _CHANGE_VERIFICATION_OBLIGATIONS)


def test_boundary_c_adjudicates_a_scoped_record() -> None:
    """The independent reviewer accepts or sends the mapping back wider.

    The implementer picks the mapping, writes the bounding argument, and
    captures the saving; the reviewer captures nothing. That asymmetry is why
    the contract requires an adjudication rather than only a declaration.
    """
    for path in (REVIEW_DOCTRINE, SELF_AGENTS, ADOPTER_AGENTS):
        normalized = " ".join(_read(path).split())
        assert "Bounding" in normalized and "WIDER RUN REQUIRED" in normalized, path


def test_wider_run_verdict_invalidates_the_scoped_record() -> None:
    """`WIDER RUN REQUIRED` blocks acceptance until new B evidence exists."""
    normalized = " ".join(_read(REVIEW_DOCTRINE).split())
    assert "WIDER RUN REQUIRED" in normalized
    assert "returns it to the author before the final integration run" in normalized
    assert "do not automatically call for a whole-tree run" in normalized


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
        "for <paths>",
        "do not widen it by judgment",
        "after code review",
        "Boundary B mode",
        "bounded | wide",
        "change record is separate from tree-certification evidence",
        *RECORD_FIELDS,
    )
    review_required = (
        "before Boundary B",
        "WIDER RUN REQUIRED",
        "keeps the change open",
        "a separate authorized integration run",
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
            "Unknown dependencies are not claimed as covered",
            "test homes",
            "public paths",
        )
        assert not [token for token in required if token not in normalized], path
        if path == ADOPTER_PROPOSAL_TEMPLATE:
            assert "Broader certification is separate and does not replace a missing check" in normalized
        else:
            assert "Full tree certification is a separate authorized integration run" in normalized

    assert "There is no separate slow / networked tier" not in _read(
        SELF_PROPOSAL_TEMPLATE
    )
