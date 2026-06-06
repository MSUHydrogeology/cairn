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

class TestFilterSources:
    """Archive / ephemeral SOURCE exclusion -- parity with modflow_tools'
    verify_doc_links (the reference deployment).  Filters sources only:
    a live doc linking TO an archived file is still validated."""

    def _paths(self, root: Path) -> list[Path]:
        return [
            root / "AGENTS.md",
            root / "docs" / "guide.md",
            root / "docs" / "archive" / "old.md",          # docs/ stays gated
            root / "dev" / "proposals" / "live.md",
            root / "dev" / "proposals" / "archive" / "old.md",
            root / "dev" / "plans" / "archive" / "prog" / "deep.md",  # nested
            root / "dev" / "reflections" / "2026-05-29-x.md",
        ]

    def test_excludes_dev_archive_and_reflections(self, tmp_path: Path) -> None:
        kept = link_check.filter_sources(self._paths(tmp_path), tmp_path)
        rel = sorted(str(p.relative_to(tmp_path)) for p in kept)
        # docs/archive/ is KEPT: the rule is anchored to dev/ as the first
        # segment so docs/ stays fully link-gated.
        assert rel == sorted([
            "AGENTS.md",
            "docs/guide.md",
            "docs/archive/old.md",
            "dev/proposals/live.md",
        ]), rel

    def test_include_archives_returns_all(self, tmp_path: Path) -> None:
        allp = self._paths(tmp_path)
        assert link_check.filter_sources(
            allp, tmp_path, include_archives=True) == allp

    def test_link_to_archived_file_still_validated(self, tmp_path: Path) -> None:
        """Excluding archive sources does not stop a live doc's link to an
        archived file from being checked (SOURCES-only semantics)."""
        (tmp_path / "dev" / "archive").mkdir(parents=True)
        (tmp_path / "live.md").write_text(
            "# Live\n\n[gone](dev/archive/missing.md)\n")
        res = link_check.check_tree(tmp_path, [tmp_path / "live.md"])
        assert any(f.kind == "link" for f in res.flags), (
            "a broken link into dev/archive/ should still flag")


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

    def test_escaping_relative_link_flagged(self, tmp_path: Path) -> None:
        """A relative link to a real file *outside* the repo root is a flag,
        not a silent pass (Codex code-review finding 1)."""
        root = tmp_path / "repo"
        root.mkdir()
        (tmp_path / "outside.md").write_text("# Outside\n")  # exists, outside
        doc = root / "doc.md"
        doc.write_text("# Doc\n\n[escape](../outside.md)\n")
        res = link_check.check_tree(root, [doc])
        assert [f.kind for f in res.flags] == ["link"], (
            "escaping relative link should be flagged, got "
            f"{[(f.kind, f.message) for f in res.flags]}"
        )
        assert "escapes the repo root" in res.flags[0].message


# ---------------------------------------------------------------------------
# Fold 4: link_check explicit-anchor {#custom-id} regression (R3)
# ---------------------------------------------------------------------------

class TestExplicitAnchor:
    """Regression tests for the {#custom-id} anchor attribute fix.

    A heading ``### T {#t}`` previously slugged to ``t-t`` (the braces
    content fed into github_slug), so a link to ``#t`` silently resolved
    to nothing.  The fix registers the literal id (``t``) and the auto-slug
    of the heading text without the attribute (``t`` again in this case, or
    a distinct slug for longer headings).

    R3 (binding from the external reviewer): the regression test must cover
    leading/trailing whitespace in the attribute and the no-match / garbage
    cases.
    """

    def test_explicit_anchor_registered(self) -> None:
        """The literal id from {#custom-id} is in the anchor set."""
        text = "# Top\n\n## Section {#my-anchor}\n"
        anchors = link_check.file_anchors(text)
        assert "my-anchor" in anchors, f"expected 'my-anchor' in {anchors}"

    def test_auto_slug_without_attr_also_registered(self) -> None:
        """The auto-slug of the heading text WITHOUT the {#...} attr is also
        registered so both reference forms resolve."""
        text = "# Top\n\n## Section {#custom}\n"
        anchors = link_check.file_anchors(text)
        # 'section' is the slug of 'Section' (without the attr)
        assert "section" in anchors, f"auto-slug 'section' missing from {anchors}"
        assert "custom" in anchors, f"explicit id 'custom' missing from {anchors}"

    def test_no_double_slug_bug(self) -> None:
        """### T {#t} must NOT produce the doubled 't-t' slug."""
        text = "### T {#t}\n"
        anchors = link_check.file_anchors(text)
        assert "t-t" not in anchors, f"double-slug 't-t' must not appear in {anchors}"
        assert "t" in anchors, f"explicit id 't' must appear in {anchors}"

    def test_link_to_explicit_anchor_resolves(self, tmp_path: Path) -> None:
        """An intra-doc link to an explicit anchor must not be flagged."""
        (tmp_path / "doc.md").write_text(
            "# Doc\n\n"
            "## Reference {#ref-anchor}\n\n"
            "[see ref](#ref-anchor)\n"
        )
        res = link_check.check_tree(tmp_path, [tmp_path / "doc.md"])
        assert res.flags == [], (
            f"link to explicit anchor should resolve cleanly, got: "
            f"{[(f.kind, f.message) for f in res.flags]}"
        )

    def test_leading_trailing_whitespace_in_attr(self) -> None:
        """The {# id } form with spaces inside the braces is handled --
        the id is stripped and registered as 'id', not ' id '."""
        text = "## Title {#  spaced-id  }\n"
        anchors = link_check.file_anchors(text)
        assert "spaced-id" in anchors, (
            f"id with surrounding spaces should be stripped; anchors={anchors}"
        )
        assert "spaced-id" == "spaced-id"  # sanity

    def test_whitespace_before_brace(self) -> None:
        """The pattern handles extra spaces between heading text and '{'."""
        text = "## Title   {#whitespace-before}\n"
        anchors = link_check.file_anchors(text)
        assert "whitespace-before" in anchors, (
            f"whitespace before brace should be handled; anchors={anchors}"
        )

    def test_no_attr_unchanged(self) -> None:
        """A heading without {#...} still produces the normal github slug."""
        text = "## Normal Heading\n"
        anchors = link_check.file_anchors(text)
        assert "normal-heading" in anchors, (
            f"standard slug should still work; anchors={anchors}"
        )

    def test_garbage_brace_not_matched(self) -> None:
        """Braces that don't match the {#id} pattern are not treated as
        explicit anchors -- e.g. ``## Title {not-an-id}`` or empty ``{#}``."""
        # No leading '#' inside braces -> not an explicit anchor
        text_no_hash = "## Title {not-an-id}\n"
        anchors_no_hash = link_check.file_anchors(text_no_hash)
        # Should slug normally (no explicit anchor extracted)
        assert "title-not-an-id" in anchors_no_hash or "title" in anchors_no_hash, (
            f"garbage brace should not strip content; got {anchors_no_hash}"
        )

    def test_empty_explicit_id_skipped(self) -> None:
        """An empty {#} attribute contributes no anchor (empty id skipped)."""
        text = "## Title {#}\n"
        anchors = link_check.file_anchors(text)
        # The empty id must not be registered; the auto-slug of 'Title' should be
        assert "" not in anchors, f"empty string must not be in anchors: {anchors}"


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

    def test_outside_doc_rejected(self, tmp_path: Path) -> None:
        """--sync must refuse a directive-bearing doc outside the repo root,
        without rewriting it (Codex code-review finding 2)."""
        root = tmp_path / "repo"
        root.mkdir()
        (root / "src.py").write_text(
            "# snippet-start: demo\nnew\n# snippet-end: demo\n")
        doc = tmp_path / "outside.md"
        before = ("<!-- snippet: src.py#demo -->\n~~~\nold\n~~~\n")
        doc.write_text(before)
        rc = snippets.main(["--root", str(root), "--sync", str(doc)])
        assert rc == 1, "an outside doc must be refused"
        assert doc.read_text() == before, "the outside doc must not be rewritten"

    def test_longer_fence_wraps_shorter(self, tmp_path: Path) -> None:
        """A 4-fence block that contains a shorter same-char fence in its
        body is one block, not closed early (Codex code-review finding 3)."""
        (tmp_path / "src.py").write_text(
            "# snippet-start: fenced\na\n~~~\nb\n# snippet-end: fenced\n")
        doc = tmp_path / "d.md"
        # 4-tilde fences wrapping a body that contains a 3-tilde literal.
        doc.write_text(
            "# Doc\n\n<!-- snippet: src.py#fenced -->\n"
            "~~~~\na\n~~~\nb\n~~~~\n")
        # The body equals the region, so a correct parser sees no drift.
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 0


# ---------------------------------------------------------------------------
# link_check --check-external SSRF guard (security-hardening Chunk 1)
# ---------------------------------------------------------------------------

class TestLinkCheckSSRF:
    """The external-link probe must refuse non-public destinations and
    validate every redirect hop (no live network: literal IPs resolve via
    getaddrinfo without DNS, and refused hosts never reach the opener)."""

    def test_host_public_classification(self) -> None:
        # Non-public literals -> blocked. Includes ranges that are
        # non-global but carry no single denylist flag, so only the
        # `not is_global` contract catches them (Codex finding 1):
        #   100.64.0.1  -> CGNAT shared space (100.64.0.0/10)
        #   2001:db8::1 -> IPv6 documentation range (non-global)
        #   fc00::1     -> IPv6 unique-local
        for ip in ("127.0.0.1", "10.0.0.1", "192.168.1.1",
                   "169.254.169.254", "100.64.0.1",
                   "::1", "fe80::1", "fc00::1", "2001:db8::1"):
            assert link_check._host_is_public(ip) is False, ip
        # A public literal -> allowed (no DNS needed).
        assert link_check._host_is_public("93.184.216.34") is True
        # Unresolvable / empty -> fail-closed.
        assert link_check._host_is_public("") is False

    def test_allow_host_bypass(self) -> None:
        # An explicitly allow-listed internal host passes without a public
        # classification; everything else still requires public.
        assert link_check._host_allowed("127.0.0.1", {"127.0.0.1"}) is True
        assert link_check._host_allowed("127.0.0.1", set()) is False

    def test_probe_refuses_non_public_host(self, tmp_path: Path) -> None:
        flags: list = []
        link_check._probe_external(
            tmp_path / "x.md", 1, "http://169.254.169.254/latest/meta-data/",
            flags, allow_hosts=set())
        assert any("SSRF guard" in f.message for f in flags), flags

    def test_probe_refuses_non_http_scheme(self, tmp_path: Path) -> None:
        flags: list = []
        link_check._probe_external(
            tmp_path / "x.md", 1, "ftp://example.com/x", flags,
            allow_hosts=set())
        assert any("non-http(s) scheme" in f.message for f in flags), flags

    def test_redirect_hop_to_private_is_refused(self, tmp_path, monkeypatch):
        """A public first hop that 302-redirects to a link-local address is
        refused at the second hop (manual, validated redirects)."""
        class _FakeOpener:
            def open(self, req, timeout=None):
                raise link_check.urllib.error.HTTPError(
                    req.full_url, 302, "Found",
                    {"Location": "http://169.254.169.254/"}, None)

        monkeypatch.setattr(link_check.urllib.request, "build_opener",
                            lambda *a, **k: _FakeOpener())
        flags: list = []
        # First hop is a public literal IP (passes), then the redirect target
        # is link-local (must be refused before contact).
        link_check._probe_external(
            tmp_path / "x.md", 1, "http://93.184.216.34/", flags,
            allow_hosts=set())
        assert any("SSRF guard" in f.message for f in flags), flags
