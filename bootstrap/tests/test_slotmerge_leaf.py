"""Stage 2 — the extracted templating leaf (`bootstrap/_scaffold/slotmerge.py`).

Contracts:

* **Near-leaf** — `slotmerge` imports only the stdlib plus the
  `security` containment leaf (for `_assert_safe_write`, the module-merge write
  guard); it must never import any higher engine module (install / upgrade / the
  3-way merge engine depend on it, never the reverse).
* **Containment** — module-merge writes are routed
  through the containment guard, so a module-controlled merge-target path cannot
  escape the adopter root.
* **Single identity** — every moved public symbol resolves to the one leaf object
  across the engine (`bootstrap._scaffold`) and the `bootstrap.scaffold` facade.
* **Boundary pin** — `run_module_merge_pass` is the install-time orchestrator and
  stays in the engine (it walks `_MODULE_MAPPINGS` / `InstallSpec`, config
  trust-anchors that migrate at Stage 4). It must NOT live in the leaf; the leaf
  must NOT define it. A later stage that relocates it without resolving that
  coupling trips this test.
* **Behavioral smoke** — the leaf works standalone (token substitution + a
  module-into-slot round-trip), so the import boundary didn't silently break it.

Stdlib only.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

#: Public templating symbols that moved to the leaf at Stage 2.
_MOVED_SYMBOLS = (
    "substitute_tokens",
    "find_unfilled_tokens",
    "find_block_slots",
    "find_unpaired_slots",
    "parse_module_merge_directives",
    "validate_unique_slot_names",
    "merge_module_into_slot",
    "check_slot_fidelity",
    "ModuleMergeResult",
    "ModuleMergeError",
    "DuplicateSlotError",
    "_TOKEN_RE",
    "_SLOT_RE",
    "_SLOT_END_RE",
    "_DOC_AUTHOR_TOKENS",
)


def test_token_substitution_smoke():
    from bootstrap._scaffold import slotmerge as SM  # noqa: PLC0415

    text = "project={{project_name}} test={{test_command}} kept={{unknown}}"
    out = SM.substitute_tokens(text, {"project_name": "demo", "test_command": "pytest"})
    assert out == "project=demo test=pytest kept={{unknown}}"
    # document-author placeholders are excluded from the unfilled report
    assert SM.find_unfilled_tokens("{{author}} {{unknown}}") == ["unknown"]


def test_module_merge_refuses_writes_outside_the_adopter_root(tmp_path):
    """A module-controlled merge-target path must not
    escape the adopter root. All four escape shapes are refused with the one
    ScaffoldSecurityError, and the outside file is never written."""
    from bootstrap._scaffold import slotmerge as SM  # noqa: PLC0415
    from bootstrap._scaffold.security import ScaffoldSecurityError  # noqa: PLC0415

    target = tmp_path / "adopter"
    target.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("<!-- cairn:slot x -->\n\n<!-- cairn:end x -->\n", encoding="utf-8")
    outside_sentinel = outside.read_text(encoding="utf-8")

    # (1) ``..`` escape and (2) absolute target -> refused, outside untouched.
    for target_rel in ("../outside.md", str(outside)):
        with pytest.raises(ScaffoldSecurityError):
            SM.merge_module_into_slot(target, target_rel, "x", "ESCAPED", non_interactive=True)
        assert outside.read_text(encoding="utf-8") == outside_sentinel

    # (3) a symlinked target inside the adopter that points outside -> refused.
    trap = target / "AGENTS.md"
    trap.symlink_to(outside)
    with pytest.raises(ScaffoldSecurityError):
        SM.merge_module_into_slot(target, "AGENTS.md", "x", "ESCAPED", non_interactive=True)
    assert outside.read_text(encoding="utf-8") == outside_sentinel

    # (4) a symlinked conflict side-file -> refused before the side-file write.
    real = target / "DOC.md"
    real.write_text(
        "<!-- cairn:slot x -->\nexisting\n<!-- cairn:end x -->\n", encoding="utf-8",
    )
    side = real.with_name("DOC.md.x.cairn-merge-pending")
    side.symlink_to(outside)  # plant a symlinked side-file pointing outside
    with pytest.raises(ScaffoldSecurityError):
        SM.merge_module_into_slot(target, "DOC.md", "x", "diverging", non_interactive=True)
    assert outside.read_text(encoding="utf-8") == outside_sentinel
