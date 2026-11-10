"""Focused guards for the quality-gate composition and the optional testing module.

Wording of the verification doctrine is reviewed, not tested: the guards that
checked required phrases in AGENTS.md, the plan and proposal templates and the
doctrine files were retired on 2026-11-10 (Maintainer direction).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[3]
QUALITY_GATE = ROOT / "scripts" / "quality_gate.py"
TESTING_MODULES = (
    ROOT / "dev" / "modules" / "testing-discipline.md",
    ROOT / "templates" / "modules" / "team-gated" / "testing-discipline.md",
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


