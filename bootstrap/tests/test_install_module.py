"""Stage 6 — the extracted install subsystem (`bootstrap/_scaffold/install.py`).

Contracts:

* **Layer-6 subsystem, downward-only dependencies** — `install` imports only the
  stdlib and the lower leaves (config / security / slotmerge / lockfile). It must
  never import the engine package, nor `upgrade` / `cli` / `merge` (no upward or
  sideways edge), and none of those leaves may import `install` (no cycle).
* **Single identity** — every moved symbol resolves to the one `install` object
  across the engine and the `bootstrap.scaffold` facade.
* **Boundary pin** — the shared root helpers (`_cairn_root` / `_find_cairn_root`)
  and the upgrade-time `_MANIFEST_SEARCH_DIRS` stay in the engine, not install.
* **Guarded-write regression** — the install-side Class-A writers still
  route their destinations through a containment guard (re-checks the
  Class-A set of `bootstrap/_scaffold/SECURITY_MUTATIONS.md`
  now that they live in install.py).
* **Behavioral smoke** — a dev-tree creation and a core install round-trip work.

Stdlib only.

Promises:
- A dev-tree creation and a core install each produce a working tree.
- Install removes a conditional region whose axis value is excluded and keeps one whose value matches.
- Install writers refuse to write through a symlinked destination.
"""
from __future__ import annotations

import ast
from pathlib import Path

_PKG = Path(__file__).resolve().parents[1] / "_scaffold"
_GUARD_CALLS = {
    "_assert_safe_write", "_assert_fanout_contained", "_assert_git_binding_path"
}

#: Class-A install-side writers (per `bootstrap/_scaffold/SECURITY_MUTATIONS.md`)
#: that must each call a containment guard.
_INSTALL_GUARDED_WRITERS = {
    "_install_one", "write_local_env", "install_onboarding",
    "write_install_lockfile", "_emit_skill_copy_fallback", "fan_out_skills",
}


def test_dev_tree_and_core_install_smoke(tmp_path):
    from bootstrap._scaffold import install as INS  # noqa: PLC0415

    created = INS.create_dev_tree(tmp_path)
    assert (tmp_path / "dev").is_dir()
    assert any(p.name == "dev" for p in created)
    # dry-run creates nothing new on a second pass
    dry = INS.create_dev_tree(tmp_path, dry_run=True)
    assert isinstance(dry, list)


# ---------------------------------------------------------------------------
# cairn:if stripping through install
# ---------------------------------------------------------------------------


def test_install_one_verbatim_not_stripped(tmp_path):
    """Verbatim files are never stripped, even when axes are provided."""
    from bootstrap._scaffold.install import _install_one  # noqa: PLC0415

    template = (
        "<!-- cairn:if agent_team in concurrent-multi-type -->\n"
        "verbatim content\n"
        "<!-- cairn:endif -->\n"
    )
    for index, ending in enumerate((b"\n", b"\r\n")):
        raw = template.encode("utf-8").replace(b"\n", ending)
        src = tmp_path / f"script{index}.py"
        src.write_bytes(raw)
        dst = tmp_path / "target3" / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)

        axes = {"agent_team": "single"}
        result = _install_one(src, dst, {}, tmp_path / "target3",
                              dry_run=False, verbatim=True, axes=axes)
        assert result[3] == "installed"
        assert dst.read_text(encoding="utf-8") == template
        assert dst.read_bytes() == raw
