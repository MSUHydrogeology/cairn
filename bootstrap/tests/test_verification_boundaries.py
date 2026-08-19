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
        "Boundary A": "Iteration (scoped)",
        "Boundary B": "Integration (stable evidence)",
        "Boundary C": "Falsification (independent)",
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
        "Falsification (targeted, after broad verification)",
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


#: The bounded-mode contract, from `2026-08-12-claude-boundary-b-bounding-clause`
#: (accepted 2026-08-12). Boundary B stopped being unconditional; these are the
#: obligations that make the cheaper path safe. Each surface is asserted for the
#: *obligation*, not one exact sentence, so a rewording passes and a deletion
#: fails.
_BOUNDED_OBLIGATIONS = {
    "the bounding clause itself": (
        "bounds the change's effects confidently",
    ),
    "the fence refuses on contract and trust-ceremony surfaces": (
        "contract surface",
        "trust-ceremony surface",
    ),
    "uncertainty resolves to full": (
        "Uncertainty resolves to",
    ),
    "the record declares its mode": (
        "Boundary B mode",
    ),
}

#: Every surface that must carry the bounded contract. The two `AGENTS.md`
#: copies stay semantically parallel and lexically different -- Cairn names its
#: own commands, the adopter copy stays project-general -- which is why this
#: asserts obligations rather than shared literal prose.
_BOUNDED_SURFACES = (
    SELF_AGENTS, ADOPTER_AGENTS, PLANS_DOCTRINE,
    SELF_PLAN_TEMPLATE, ADOPTER_PLAN_TEMPLATE,
)


@pytest.mark.parametrize("path", _BOUNDED_SURFACES,
                         ids=lambda p: str(p.relative_to(ROOT)))
@pytest.mark.parametrize("label,tokens", sorted(_BOUNDED_OBLIGATIONS.items()))
def test_bounded_boundary_b_contract_reaches_every_surface(
        path, label: str, tokens) -> None:
    text = " ".join(_read(path).split())
    missing = [tok for tok in tokens if tok not in text]
    assert not missing, (
        f"{path} no longer carries the bounded-Boundary-B obligation {label!r} "
        f"(missing {missing}). Boundary B is conditional as of "
        f"2026-08-12-claude-boundary-b-bounding-clause; a surface that loses "
        f"the fence or the mode field ships a different contract than the rest."
    )


def _bounded_violations(text: str) -> list[str]:
    """Labels of the bounded-contract obligations absent from *text*."""
    normalized = " ".join(text.split())
    return [label for label, tokens in _BOUNDED_OBLIGATIONS.items()
            if [tok for tok in tokens if tok not in normalized]]


def test_bounded_guard_detects_a_removed_fence() -> None:
    """The mutant for the test above: strip the fence, the guard must fire.

    This asserts the *violation function* reports the loss -- the pattern used
    by `test_operational_guard_detects_removed_full_fallback` and
    `test_review_reuse_guard_detects_unconditional_reuse` above. An earlier
    version of this test asserted only that a token was absent from text it
    had just removed it from, which passed even against an empty file: a
    tautology wearing a mutant's docstring.
    """
    intact = _read(SELF_AGENTS)
    assert _bounded_violations(intact) == []

    mutated = intact.replace("trust-ceremony surface", "surface")
    assert "the fence refuses on contract and trust-ceremony surfaces" in \
        _bounded_violations(mutated)


#: The three GOVERNING surfaces -- not the plan templates, which do not carry
#: this rule. Kept separate from `_BOUNDED_SURFACES` for that reason.
_APPLICABILITY_SURFACES = (SELF_AGENTS, ADOPTER_AGENTS, PLANS_DOCTRINE)


@pytest.mark.parametrize("path", _APPLICABILITY_SURFACES,
                         ids=lambda p: str(p.relative_to(ROOT)))
def test_already_open_plans_keep_their_written_contract(path) -> None:
    """An accepted term that first landed with no guard at all.

    Editing doctrine acts immediately; editing the plan templates acts
    prospectively. Without this rule an in-flight plan receives two answers
    about its own evidence obligation -- and two plans were executing when the
    clause landed. The rule was accepted in the Decision, shipped in the
    implementing commit, and was still deletable without any test
    noticing it.
    """
    normalized = " ".join(_read(path).split())
    assert "already-open plan keeps the verification contract" in normalized, (
        f"{path} no longer states that an already-open plan keeps the "
        f"verification contract written in it. Bounded mode then silently "
        f"becomes available to plans whose reviewed mapping never contemplated "
        f"it."
    )


def test_bounded_guard_is_not_satisfied_by_an_empty_file() -> None:
    """The floor the old mutant test silently sat below."""
    assert len(_bounded_violations("")) == len(_BOUNDED_OBLIGATIONS)


def test_boundary_c_adjudicates_a_bounded_record() -> None:
    """The saving must depend on an independent verdict, not self-exemption.

    The implementer picks the mapping, writes the bounding argument, and
    captures the saving; the reviewer captures nothing. That asymmetry is why
    the contract requires an adjudication rather than only a declaration.
    """
    for path in (REVIEW_DOCTRINE, SELF_AGENTS, ADOPTER_AGENTS):
        normalized = " ".join(_read(path).split())
        assert "Bounding" in normalized and "FULL RUN REQUIRED" in normalized, path


def test_full_run_required_routes_to_the_existing_first_trigger() -> None:
    """`FULL RUN REQUIRED` invalidates the record; it is not a seventh trigger.

    The six triggers are pinned identically across two doctrine files by
    `test_plan_and_review_doctrine_share_fresh_run_triggers`. If adjudication
    had added a seventh, that pairing would drift.
    """
    normalized = " ".join(_read(REVIEW_DOCTRINE).split())
    assert "invalidates" in normalized

    # Counted from the DOCTRINE, not from `FRESH_RUN_TRIGGERS` -- that tuple
    # lives in this file, so asserting its length can never fail on a doctrine
    # edit and the "six stay six" claim rested on nothing.
    # The list is the numbered items between the "six triggers" sentence
    # and the paragraph that follows it.
    body = re.search(
        r"required when any of these six triggers applies:(.*?)\n\nReview-only",
        _read(REVIEW_DOCTRINE), re.S)
    assert body, "the six-trigger list is no longer in its documented shape"
    numbered = re.findall(r"^\s*(\d+)\.", body.group(1), re.M)
    assert numbered == ["1", "2", "3", "4", "5", "6"], numbered


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
