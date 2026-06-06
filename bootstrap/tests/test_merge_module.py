"""Stage 3 — the extracted 3-way merge engine (`bootstrap/_scaffold/merge.py`).

Contracts:

* **Second-layer module, correct dependency direction** — `merge` imports only
  the stdlib and the `slotmerge` leaf; it must never import back into the engine
  package (install / upgrade depend on it, never the reverse), and `slotmerge`
  must never import `merge` (no cycle).
* **Single identity** — every moved symbol resolves to the one `merge` object
  across the engine and the `bootstrap.scaffold` facade.
* **Boundary pin** — `classify_verbatim` (the verbatim hash policy, *never* a text
  merge; couples to `_sha256_hex`) stays in the engine, not the merge module.
* **Behavioral smoke** — strict slot parsing fails closed, and a token-/slot-aware
  3-way merge round-trips (clean / needs-value), so the import boundary didn't
  silently break the engine.

Stdlib only.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

_MOVED = (
    "SlotError",
    "Slot",
    "parse_slots",
    "MergeResult",
    "_transplant_slots",
    "_three_way_merge",
    "merge_file",
)


def _import_modules(pyfile: str) -> set[str]:
    tree = ast.parse(Path(pyfile).read_text(encoding="utf-8"))
    mods: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module)
        if isinstance(node, ast.Import):
            mods.update(a.name for a in node.names)
    return mods


def test_merge_depends_only_on_stdlib_and_the_slotmerge_leaf():
    from bootstrap._scaffold import merge as M  # noqa: PLC0415

    for node in ast.walk(ast.parse(Path(M.__file__).read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod.startswith("bootstrap") or node.level > 0:
                # the only engine-package import allowed is the slotmerge leaf
                assert mod.endswith("slotmerge"), f"merge imports {mod!r} (level={node.level})"
        if isinstance(node, ast.Import):
            for a in node.names:
                assert not a.name.startswith("bootstrap"), f"merge imports {a.name!r}"


def test_no_cycle_slotmerge_does_not_import_merge():
    from bootstrap._scaffold import slotmerge as SM  # noqa: PLC0415

    assert not any(
        "merge" in mod and not mod.endswith("slotmerge")
        for mod in _import_modules(SM.__file__)
    ), "slotmerge must not import the merge module (cycle)"


def test_single_identity_across_consumers():
    import sys  # noqa: PLC0415

    from bootstrap._scaffold import merge as M  # noqa: PLC0415
    import bootstrap._scaffold as engine  # noqa: PLC0415
    import bootstrap.scaffold  # noqa: PLC0415  (facade == engine)

    facade = sys.modules["bootstrap.scaffold"]
    for name in _MOVED:
        obj = getattr(M, name)
        assert getattr(engine, name) is obj, f"engine.{name} is not the merge object"
        assert getattr(facade, name) is obj, f"facade.{name} is not the merge object"


def test_classify_verbatim_is_not_in_merge():
    # classify_verbatim is the verbatim hash policy -- never a text merge. It must
    # not live in merge.py. (It moved to the lockfile module at Stage 5, where its
    # _sha256_hex coupling is owned.)
    pkg = Path(__file__).resolve().parents[1] / "_scaffold"

    def _defines(py: Path, fn: str) -> bool:
        return any(
            isinstance(n, ast.FunctionDef) and n.name == fn
            for n in ast.walk(ast.parse(py.read_text(encoding="utf-8")))
        )

    assert not _defines(pkg / "merge.py", "classify_verbatim"), (
        "classify_verbatim leaked into merge -- it is a hash policy, not a text merge"
    )
    assert _defines(pkg / "lockfile.py", "classify_verbatim"), (
        "classify_verbatim should be owned by the lockfile module (Stage 5)"
    )


def test_parse_slots_fails_closed_on_malformation():
    from bootstrap._scaffold import merge as M  # noqa: PLC0415

    with pytest.raises(M.SlotError):
        M.parse_slots("<!-- cairn:slot a -->\n<!-- cairn:slot b -->\n")  # nested
    with pytest.raises(M.SlotError):
        M.parse_slots("<!-- cairn:slot a -->\n")  # unclosed
    ok = M.parse_slots("x\n<!-- cairn:slot a -->\nbody\n<!-- cairn:end a -->\n")
    assert [s.name for s in ok] == ["a"] and ok[0].body == "body"


def test_three_way_merge_roundtrip_clean_and_needs_value():
    from bootstrap._scaffold import merge as M  # noqa: PLC0415

    # base/theirs share a slot; ours filled the slot body. No upstream prose
    # change + recorded tokens => clean.
    base_raw = "title {{project_name}}\n<!-- cairn:slot s -->\n<!-- cairn:end s -->\n"
    theirs_raw = base_raw
    ours = "title demo\n<!-- cairn:slot s -->\nmine\n<!-- cairn:end s -->\n"
    res = M.merge_file(base_raw, theirs_raw, ours, {"project_name": "demo"})
    assert res.status == "clean"
    assert "mine" in res.merged

    # a NEW upstream token with no recorded value => non-advancing needs-value.
    theirs_new = theirs_raw + "footer {{new_token}}\n"
    res2 = M.merge_file(base_raw, theirs_new, ours, {"project_name": "demo"})
    assert res2.status == "needs-value"
    assert "new_token" in res2.detail
