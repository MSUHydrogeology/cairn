"""Generated-output regression for the broad work-intent obligation.

Cairn v0.2 fold-back (cairn-v0.2-foldback-remaining-ledger, Component C):
the broadened work-intent requirement -- a required ``claim`` before
*every* nontrivial edit -- is the **Tier-2-enabled posture**, so
it must land in the team-gated
``coordination-tiers`` surface, **not** the always-on baseline that
every adopter (including solo / sequential teams) receives.

This pins that boundary against drift in the *generated* output -- the
artifact an adopter's agents actually read -- not just the source:

* a **minimal** install (no ``coordination-tiers``) must NOT carry the
  broad obligation anywhere in its generated tree;
* a **coordination-tiers** install must carry, in the installed module
  doctrine, the broad ``claim`` requirement, the coordination-surface
  ``list`` + ``claim`` clause, and the preserved "courtesy signal, not
  a lock" lock-semantics.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import main  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)

#: The imperative broad obligation -- the load-bearing string that must
#: be Tier-2-gated, never in the always-on baseline.
_BROAD = "required before every nontrivial edit"
#: A bold marker unique to the module's required-scope block.
_MARKER = "Required scope (this concurrent team)"


def _scaffold(target: Path, modules: list[str]) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: CoordBoundary\ntest_command: pytest\nmodules:\n"
        + "".join(f"  - {m}\n" for m in modules)
    )
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    )


def _all_markdown_text(target: Path) -> str:
    return "\n".join(
        md.read_text(encoding="utf-8", errors="replace")
        for md in sorted(target.rglob("*.md"))
    )


class TestBroadIntentBoundary:
    def test_minimal_install_omits_broad_obligation(
        self, tmp_path: Path
    ) -> None:
        """A kernel/default install (no coordination-tiers) must not carry
        the broad nontrivial-edit claim requirement anywhere."""
        assert _scaffold(tmp_path, []) == 0
        tree = _all_markdown_text(tmp_path)
        assert _BROAD not in tree, (
            "the broad work-intent obligation leaked into a minimal "
            "(solo/sequential) install -- it must be Tier-2-gated (I1/R1)"
        )
        assert _MARKER not in tree
        # The module doctrine file is simply not installed.
        assert not (tmp_path / "dev" / "modules"
                    / "coordination-tiers.md").is_file()

    def test_coordination_tiers_install_carries_broad_obligation(
        self, tmp_path: Path
    ) -> None:
        """A coordination-tiers install carries the broad requirement, the
        coordination-surface list+claim clause, and preserves the
        lock-semantics."""
        assert _scaffold(tmp_path, ["coordination-tiers"]) == 0
        module = tmp_path / "dev" / "modules" / "coordination-tiers.md"
        assert module.is_file(), "coordination-tiers doctrine not installed"
        text = module.read_text(encoding="utf-8")
        assert _BROAD in text, "broad claim requirement missing from module"
        # Coordination surfaces additionally require the read half.
        assert "additionally requires the" in text and "`list`" in text, (
            "coordination-surface list+claim clause missing"
        )
        # Lock-semantics preserved, not deleted.
        assert "courtesy signal, not a lock" in text
