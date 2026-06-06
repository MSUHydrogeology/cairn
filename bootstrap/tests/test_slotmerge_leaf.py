"""Stage 2 — the extracted templating leaf (`bootstrap/_scaffold/slotmerge.py`).

Contracts:

* **Pure stdlib leaf (SR5 pattern)** — `slotmerge` imports only the stdlib; it
  must never import back into the engine package (install / upgrade / the 3-way
  merge engine depend on it, never the reverse).
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


def test_slotmerge_is_a_pure_stdlib_leaf():
    from bootstrap._scaffold import slotmerge as SM  # noqa: PLC0415

    tree = ast.parse(Path(SM.__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            assert not mod.startswith("bootstrap"), f"leaf imports engine module {mod!r}"
            assert node.level == 0, "leaf must not use package-relative imports"
        if isinstance(node, ast.Import):
            for a in node.names:
                assert not a.name.startswith("bootstrap"), f"leaf imports {a.name!r}"


def test_single_identity_across_consumers():
    import sys  # noqa: PLC0415

    from bootstrap._scaffold import slotmerge as SM  # noqa: PLC0415
    import bootstrap._scaffold as engine  # noqa: PLC0415
    import bootstrap.scaffold  # the facade (== engine)  # noqa: PLC0415

    facade = sys.modules["bootstrap.scaffold"]
    for name in _MOVED_SYMBOLS:
        leaf_obj = getattr(SM, name)
        assert getattr(engine, name) is leaf_obj, f"engine.{name} is not the leaf object"
        assert getattr(facade, name) is leaf_obj, f"facade.{name} is not the leaf object"


def test_run_module_merge_pass_stays_in_the_engine_not_the_leaf():
    # Boundary pin: the orchestrator stays in __init__ (it couples to
    # _MODULE_MAPPINGS / InstallSpec); the leaf must not define it.
    pkg = Path(__file__).resolve().parents[1] / "_scaffold"

    def _defines(py: Path, fn: str) -> bool:
        tree = ast.parse(py.read_text(encoding="utf-8"))
        return any(
            isinstance(n, ast.FunctionDef) and n.name == fn
            for n in ast.walk(tree)
        )

    assert _defines(pkg / "__init__.py", "run_module_merge_pass"), (
        "run_module_merge_pass must stay defined in the engine __init__"
    )
    assert not _defines(pkg / "slotmerge.py", "run_module_merge_pass"), (
        "run_module_merge_pass leaked into the leaf — but it couples to "
        "_MODULE_MAPPINGS / InstallSpec (resolve that before moving it)"
    )
    # and the engine still exposes a working callable
    import bootstrap._scaffold as engine  # noqa: PLC0415
    assert callable(engine.run_module_merge_pass)


def test_token_substitution_smoke():
    from bootstrap._scaffold import slotmerge as SM  # noqa: PLC0415

    text = "project={{project_name}} test={{test_command}} kept={{unknown}}"
    out = SM.substitute_tokens(text, {"project_name": "demo", "test_command": "pytest"})
    assert out == "project=demo test=pytest kept={{unknown}}"
    # document-author placeholders are excluded from the unfilled report
    assert SM.find_unfilled_tokens("{{author}} {{unknown}}") == ["unknown"]


def test_module_into_slot_roundtrip_smoke(tmp_path):
    from bootstrap._scaffold import slotmerge as SM  # noqa: PLC0415

    target = tmp_path / "AGENTS.md"
    target.write_text(
        "intro\n<!-- cairn:slot habits -->\n<!-- cairn:end habits -->\nouter\n",
        encoding="utf-8",
    )
    # empty slot -> inserted
    r1 = SM.merge_module_into_slot(
        tmp_path, "AGENTS.md", "habits", "be careful", non_interactive=True,
    )
    assert r1.status == "inserted"
    assert "be careful" in target.read_text(encoding="utf-8")
    # same content again -> already-current
    r2 = SM.merge_module_into_slot(
        tmp_path, "AGENTS.md", "habits", "be careful", non_interactive=True,
    )
    assert r2.status == "already-current"
    # divergent content -> conflict deferred to a per-slot side file
    r3 = SM.merge_module_into_slot(
        tmp_path, "AGENTS.md", "habits", "be reckless", non_interactive=True,
    )
    assert r3.status == "conflict-deferred"
    assert r3.side_file is not None and Path(r3.side_file).is_file()
