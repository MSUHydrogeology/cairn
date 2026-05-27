"""Tests for the doc-drift-prevention tooling (Cairn v0.2 foldback).

Component D ships two stack-neutral, stdlib-only scripts under the
team-gated ``doc-drift-prevention`` module: ``link_check.py`` (the link /
anchor half) and ``sync_doc_snippets.py`` (the snippet half). The claim
half is intentionally *not* shipped here -- the default-on ``claim-check``
module already installs ``claim_check.py`` and the doc-drift gate composes
with it.

Covered:

* **install-path** -- both scripts land verbatim in ``scripts/`` under the
  module (1:many, the P1 pattern); the ``_MODULE_MAPPINGS`` entry is right.
* **link_check behavioral fixtures** (Codex P4) -- relative file links,
  same-file / cross-file anchors, missing file, missing anchor, and the
  external-link default (ignored unless opted in).
* **sync_doc_snippets behavioral fixtures** (Codex P3) -- clean check,
  drifted check (exit 1), ``--sync`` rewrites only the doc (not the
  source), and the path-safety contract (``..`` / absolute rejected,
  missing region a crisp error).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
_TEAM_GATED = TEMPLATES_ROOT / "modules" / "team-gated"

sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import _MODULE_MAPPINGS, main  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


link_check = _load("dd_link_check", _TEAM_GATED / "link_check.py")
snippets = _load("dd_sync_doc_snippets", _TEAM_GATED / "sync_doc_snippets.py")


def _scaffold(target: Path, modules: list[str]) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: DriftTest\ntest_command: pytest\nmodules:\n"
        + "".join(f"  - {m}\n" for m in modules)
    )
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    )


# ---------------------------------------------------------------------------
# Install-path
# ---------------------------------------------------------------------------

class TestInstallPath:
    def test_module_ships_both_tools_verbatim(self) -> None:
        specs = _MODULE_MAPPINGS["doc-drift-prevention"]
        dsts = {s.dst: s for s in specs}
        assert "dev/modules/doc-drift-prevention.md" in dsts
        assert dsts["scripts/link_check.py"].verbatim is True
        assert dsts["scripts/sync_doc_snippets.py"].verbatim is True
        # The claim half is NOT bundled here (composed from claim-check).
        assert "scripts/claim_check.py" not in dsts

    def test_tools_installed_verbatim(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, ["doc-drift-prevention"]) == 0
        for name in ("link_check.py", "sync_doc_snippets.py"):
            installed = tmp_path / "scripts" / name
            assert installed.is_file(), f"{name} not installed"
            assert installed.read_bytes() == (_TEAM_GATED / name).read_bytes(), (
                f"{name} differs from template -- not verbatim"
            )
        assert (tmp_path / "dev" / "modules"
                / "doc-drift-prevention.md").is_file()


# ---------------------------------------------------------------------------
# link_check behavioral fixtures
# ---------------------------------------------------------------------------

class TestLinkCheck:
    def _tree(self, root: Path) -> None:
        (root / "b.md").write_text("# B\n\n## target\n\nbody\n")
        (root / "a.md").write_text(
            "# A\n\n"
            "## A heading\n\n"
            "[rel](b.md)\n\n"             # ok: relative file
            "[self](#a-heading)\n\n"      # ok: same-file anchor
            "[cross](b.md#target)\n\n"    # ok: cross-file anchor
            "[ext](https://example.com)\n\n"  # external: ignored by default
            "[missing](nope.md)\n\n"      # broken: file
            "[badanchor](#no-such)\n"     # broken: anchor
        )

    def test_resolves_and_flags(self, tmp_path: Path) -> None:
        self._tree(tmp_path)
        res = link_check.check_tree(
            tmp_path, [tmp_path / "a.md", tmp_path / "b.md"])
        kinds = sorted(f.kind for f in res.flags)
        assert kinds == ["anchor", "link"], (
            f"expected exactly one broken link + one broken anchor, got "
            f"{[(f.kind, f.message) for f in res.flags]}"
        )
        assert res.external_links == 1, "external link should be counted"

    def test_main_exit_code(self, tmp_path: Path) -> None:
        self._tree(tmp_path)
        rc = link_check.main(
            ["--root", str(tmp_path),
             str(tmp_path / "a.md"), str(tmp_path / "b.md")])
        assert rc == 1
        # A clean tree exits 0.
        (tmp_path / "a.md").write_text("# A\n\n## A heading\n\n[ok](#a-heading)\n")
        rc = link_check.main(["--root", str(tmp_path), str(tmp_path / "a.md")])
        assert rc == 0

    def test_external_default_ignored(self, tmp_path: Path) -> None:
        (tmp_path / "x.md").write_text("# X\n\n[e](https://nope.invalid)\n")
        res = link_check.check_tree(tmp_path, [tmp_path / "x.md"])
        assert res.flags == [], "external link must not be probed by default"
        assert res.external_links == 1


# ---------------------------------------------------------------------------
# sync_doc_snippets behavioral fixtures
# ---------------------------------------------------------------------------

class TestSnippetSync:
    def _source(self, root: Path) -> None:
        (root / "src.py").write_text(
            "x = 1\n"
            "# snippet-start: demo\n"
            "model = Model(config)\n"
            "model.build()\n"
            "# snippet-end: demo\n"
            "y = 2\n"
        )

    def _doc(self, body: str) -> str:
        return (
            "# Doc\n\n"
            "<!-- snippet: src.py#demo -->\n"
            "```python\n"
            f"{body}"
            "```\n"
        )

    def test_clean_check_passes(self, tmp_path: Path) -> None:
        self._source(tmp_path)
        (tmp_path / "d.md").write_text(
            self._doc("model = Model(config)\nmodel.build()\n"))
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(tmp_path / "d.md")]) == 0

    def test_drift_detected_and_synced(self, tmp_path: Path) -> None:
        self._source(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text(self._doc("model = Model(config)  # stale\n"))
        src_before = (tmp_path / "src.py").read_bytes()
        # --check flags the drift.
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 1
        # --sync rewrites the doc, then --check is clean.
        assert snippets.main(
            ["--root", str(tmp_path), "--sync", str(doc)]) == 0
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 0
        assert "model.build()" in doc.read_text()
        assert "# stale" not in doc.read_text()
        # The source is never rewritten.
        assert (tmp_path / "src.py").read_bytes() == src_before

    def test_escaping_source_rejected(self, tmp_path: Path) -> None:
        doc = tmp_path / "d.md"
        doc.write_text(
            "# Doc\n\n<!-- snippet: ../evil.py#demo -->\n```\nx\n```\n")
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 1
        # Absolute paths are refused too.
        doc.write_text(
            "# Doc\n\n<!-- snippet: /etc/passwd#demo -->\n```\nx\n```\n")
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 1

    def test_missing_region_is_crisp_error(self, tmp_path: Path) -> None:
        self._source(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text(
            "# Doc\n\n<!-- snippet: src.py#absent -->\n```\nx\n```\n")
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 1
