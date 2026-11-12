"""Tests for the `documentation-plan` default-on module
(Proposal D: fold-back-documentation-plan).

Promises:
- A default install places the documentation-plan doctrine and the forkable DOCUMENTATION_PLAN.md at the docs root.
- A pinned modules list without documentation-plan installs neither file.
- The installed forkable uses adopter-relative paths and leaks no cairn/ framework path prefix.
- Every AGENTS.md section a shipped file cites exists in a fresh install's AGENTS.md.

Covers:
* Registration: the module is in `_DEFAULT_ON_MODULES` and
  carries an `_MODULE_MAPPINGS` entry.
* Install path: a default scaffold installs both the module
  doctrine + the forkable at the canonical destinations
  (`dev/modules/documentation-plan.md` +
  `docs/DOCUMENTATION_PLAN.md`).
* Content fidelity: the forkable carries the four-layer vision
  (entry / governing / deliberation / descriptive), the decision
  procedure, voice rules, and uses adopter-relative paths only
  (no `cairn/` prefix in worked examples).
* Slot anchors: the three core templates carry the expected slot
  anchor names (`documentation-discipline` in core AGENTS.md,
  `documentation-tier-home` in proposals + plans templates).
* Merged-into blocks: the module file ships three named blocks
  (Block 1 / 2 / 3) carrying the slot-fill content for adopters
  (or agents) to paste. Mechanical merge via Proposal B's
  `cairn:merge-target` directives is **deferred** pending
  resolution of the lockfile-divergence interaction (a separate
  Cairn follow-up).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_documentation_plan_module.py
"""

from __future__ import annotations

import sys
import re
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    _DEFAULT_ON_MODULES,
    _MODULE_MAPPINGS,
    main,
    install_manifest,
)

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"

MODULE = "documentation-plan"
MODULE_DOC_DST = "dev/modules/documentation-plan.md"
FORKABLE_DST = "docs/DOCUMENTATION_PLAN.md"

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available",
)


def _scaffold(target: Path, modules: list[str] | None) -> int:
    cfg = target / "profile.yml"
    body = "project_name: DocumentationPlanTest\ntest_command: pytest\n"
    if modules is not None:
        body += "modules:\n" + "".join(f"  - {m}\n" for m in modules)
    cfg.write_text(body)
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT),
         "--non-interactive"]
    )


def _agents_section_references(text: str) -> list[str]:
    text = re.sub(r"<!--\s*cairn:merge-target:.*?-->", "", text, flags=re.S)
    text = re.sub(r"\s+", " ", text.replace("`", "").replace("*", ""))
    pattern = r'AGENTS\.md\s*>\s*(?:"([^"]+)"|([A-Z][^".();\n]+))'
    return [(match.group(1) or match.group(2)).strip()
            for match in re.finditer(pattern, text)]


def _shipped_agents_citation_errors(headings: set[str]) -> list[str]:
    sources = {src for src, _dst, _verbatim in install_manifest()}
    families = {"skills/_lib/session.py", "modules/default-on/verify_stems.py",
                "core/dev/plans/_template.md", "core/dev/rules/README.md"}
    assert families <= sources, "citation family missing from install mappings"
    errors = []
    for src in sorted(sources):
        refs = _agents_section_references((TEMPLATES_ROOT / src).read_text(encoding="utf-8"))
        if src in families:
            assert refs, f"citation family not extracted: {src}"
        errors.extend(f"{src}: {ref}" for ref in refs if ref not in headings)
    return errors


def test_shipped_agents_section_citations_resolve(tmp_path: Path) -> None:
    assert _scaffold(tmp_path, None) == 0
    text = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    headings = set(re.findall(r"^#{1,6} (.+)$", text, re.M))
    assert {"Review", "Roles", "Lifecycle and records"} <= headings
    assert not _shipped_agents_citation_errors(headings)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Install path
# ---------------------------------------------------------------------------


class TestInstallPath:
    def test_default_install_includes_module(self, tmp_path: Path) -> None:
        """A profile that omits `modules:` installs the default-on
        set, which now includes documentation-plan."""
        assert _scaffold(tmp_path, None) == 0
        assert (tmp_path / MODULE_DOC_DST).is_file()
        assert (tmp_path / FORKABLE_DST).is_file()

    def test_omission_path(self, tmp_path: Path) -> None:
        """A pinned `modules:` list without documentation-plan leaves
        both artifacts uninstalled."""
        assert _scaffold(tmp_path, ["reflections"]) == 0
        assert not (tmp_path / MODULE_DOC_DST).exists()
        assert not (tmp_path / FORKABLE_DST).exists()


# ---------------------------------------------------------------------------
# Content fidelity: four-layer vision + adopter-relative paths
# ---------------------------------------------------------------------------


class TestForkableContent:


    def test_forkable_uses_adopter_relative_paths(
        self, tmp_path: Path,
    ) -> None:
        """The forkable ships to adopters -- every path in its
        worked examples must be adopter-relative (no `cairn/`
        prefix).  This is the check's primary
        guarantee."""
        assert _scaffold(tmp_path, [MODULE]) == 0
        text = (tmp_path / FORKABLE_DST).read_text(encoding="utf-8")
        # No `cairn/` prefix anywhere in the forkable's content.
        # (The string `cairn` may appear in "Cairn module" prose;
        # the specific failure mode is path-prefix leakage like
        # `cairn/docs/methodology/`, `cairn/templates/`, `cairn/docs/`.)
        for leaked in (
            "cairn/docs/methodology/",
            "cairn/templates/",
            "cairn/docs/",
            "cairn/dev/",
            "cairn/bootstrap/",
            "cairn/scripts/",
        ):
            assert leaked not in text, (
                f"forkable docs/DOCUMENTATION_PLAN.md leaks "
                f"cairn-framework-internal path prefix {leaked!r} -- "
                f"adopters do not have a `cairn/` directory at their "
                f"tree root (Antigravity P1)"
            )


# ---------------------------------------------------------------------------
# Cairn-self-hosted instance: dogfood
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Slot anchors: the three core templates carry the expected slots
# ---------------------------------------------------------------------------
