"""
Tests pinning the doctrine sections in ``cairn/doctrine/doc-governance.md``.

The 2026-05-28 docs-architecture-cleanup adds three to four new
sections to ``doctrine/doc-governance.md`` (tier-recognition,
common-homes-for-vision, format-neutrality, style-conventions-
location), plus a coherence-pass rewrite of the opening taxonomy.
These tests pin the section headings against silent regression so
a future doc-governance edit cannot accidentally remove them.

The shape is the same as the D-2 finding from the v0.2 pre-release
sweep: doctrine claims a section exists; we test that it does.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_doc_governance.py
"""

from __future__ import annotations

from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
DOC_GOVERNANCE = CAIRN_ROOT / "doctrine" / "doc-governance.md"


@pytest.fixture(scope="module")
def doc_text() -> str:
    """The full text of ``doctrine/doc-governance.md``."""
    if not DOC_GOVERNANCE.is_file():
        pytest.fail(f"missing: {DOC_GOVERNANCE}")
    return DOC_GOVERNANCE.read_text(encoding="utf-8")


class TestTierRecognition:
    """Chunk 2 of the docs-architecture-cleanup plan adds tier-
    recognition for the descriptive layer."""

    def test_descriptive_layer_section_present(self, doc_text: str) -> None:
        # Post-coherence-pass (Chunk 8), the descriptive-layer
        # recognition lives under a top-level "Descriptive-layer
        # recognition" heading with a "Tier recognition" subsection.
        assert "Descriptive-layer recognition" in doc_text, (
            "doc-governance.md must declare the descriptive-layer "
            "recognition section"
        )
        assert "Tier recognition" in doc_text, (
            "doc-governance.md must declare the Tier recognition "
            "subsection under descriptive-layer recognition"
        )

    def test_names_the_four_conventional_tiers(self, doc_text: str) -> None:
        for tier in ("Quickstart", "User Guide", "Theory / Reference", "Developer"):
            assert tier in doc_text, (
                f"tier-recognition section must name {tier!r} as a "
                f"conventional descriptive-layer tier"
            )

    def test_uses_commonly_lives_in_framing_not_legislation(
        self, doc_text: str
    ) -> None:
        """Per the maintainer's layer-prescriptiveness gradient:
        tier-RECOGNITION holds; tier-LEGISLATION drops.  The phrasing
        must be 'commonly lives in', not 'must live in' or 'lives in'.

        The substring search is whitespace-normalized so a
        line-wrapped or markdown-bolded version of the phrase
        still matches (e.g., '**commonly\\nlives in**')."""
        import re
        normalized = re.sub(r"\s+", " ", doc_text)
        # Strip markdown emphasis chars so '**commonly lives in**'
        # also matches.
        normalized = normalized.replace("**", "").replace("*", "")
        assert "commonly lives in" in normalized, (
            "tier-recognition section must use the 'commonly lives in' "
            "framing (Decision M1 layer-prescriptiveness gradient)"
        )


class TestCommonHomesForVision:
    """Chunk 2 also adds the common-homes-for-vision paragraph."""

    def test_common_homes_section_present(self, doc_text: str) -> None:
        assert "Common homes for project vision / charter material" in doc_text, (
            "doc-governance.md must declare the common-homes-for-vision "
            "section"
        )

    def test_names_the_four_typical_homes(self, doc_text: str) -> None:
        """The section enumerates the four typical vision homes per
        the proposal Change (b.1) revised: docs/developer/vision.md,
        README.md, docs/-root vision page, and dev/vision.md."""
        for home in (
            "`docs/developer/vision.md`",
            "`README.md`",
            "`docs/vision.md`",
            "`dev/vision.md`",
        ):
            assert home in doc_text, (
                f"common-homes-for-vision section must name {home} as "
                f"a typical vision home"
            )

    def test_is_non_prescriptive(self, doc_text: str) -> None:
        """The section must not recommend among the homes.  The
        phrase 'The adopter picks' or equivalent must appear, and
        the section must NOT contain prescriptive language like
        'must be placed' / 'should be placed' for any specific
        home."""
        # Positive: explicit deference to the adopter.
        assert "adopter picks" in doc_text.lower(), (
            "common-homes section must explicitly defer to the "
            "adopter (Decision M1 layer-prescriptiveness gradient)"
        )
        # Negative: no prescriptive language steering toward one home.
        for prescription in (
            "vision.md must be placed",
            "vision.md should always",
            "the only correct home for vision",
        ):
            assert prescription.lower() not in doc_text.lower(), (
                f"common-homes section must not prescribe a specific "
                f"home: found phrase resembling {prescription!r}"
            )


class TestDevReadmeTemplate:
    """The Cairn dev-tree-additions paragraph in
    ``templates/core/dev/README.md`` must not mention vision.md as an
    optional dev/ addition (per proposal Change (b.1) revised)."""

    def test_dev_readme_does_not_mention_vision_md_in_optional_additions(
        self,
    ) -> None:
        path = CAIRN_ROOT / "templates" / "core" / "dev" / "README.md"
        text = path.read_text(encoding="utf-8")
        # The pre-revision line was: "A `vision.md` (the project's
        # north star), a `strategy/` directory ... are added when
        # the project needs them".  After Chunk 2, vision.md is
        # NOT mentioned in that optional-additions paragraph.
        assert "`vision.md`" not in text, (
            "templates/core/dev/README.md must NOT mention `vision.md` "
            "as an optional dev/-tree addition (per Change b.1 revised)"
        )

    def test_dev_readme_points_at_doc_governance_for_vision_home(
        self,
    ) -> None:
        """The dev-tree-additions paragraph should point at
        ``doc-governance.md > Common homes for project vision /
        charter material`` so an adopter following the template knows
        where to look."""
        path = CAIRN_ROOT / "templates" / "core" / "dev" / "README.md"
        text = path.read_text(encoding="utf-8")
        assert "doc-governance.md" in text, (
            "templates/core/dev/README.md must point at "
            "doctrine/doc-governance.md for the vision-home decision"
        )


class TestFormatNeutrality:
    """Chunk 3 of the docs-architecture-cleanup plan adds the format-
    neutrality statement (proposal Change c.1)."""

    def test_format_neutrality_section_present(self, doc_text: str) -> None:
        assert "Adopter `docs/` format-neutrality" in doc_text, (
            "doc-governance.md must declare the format-neutrality "
            "section"
        )

    def test_names_multiple_doc_formats(self, doc_text: str) -> None:
        """The section must explicitly name multiple non-Markdown
        formats so an adopter using e.g. reStructuredText is not
        steered toward `.md`."""
        for fmt in ("Markdown", "reStructuredText", "Asciidoc", "Quarto"):
            assert fmt in doc_text, (
                f"format-neutrality section must name {fmt!r} so "
                f"adopters know Cairn assumes nothing about format"
            )

    def test_disclaims_adopter_tree_assumptions(self, doc_text: str) -> None:
        """The section must explicitly state that Cairn's `.md`
        references point INTO Cairn, not into the adopter's tree."""
        import re
        normalized = re.sub(r"\s+", " ", doc_text)
        normalized = normalized.replace("**", "").replace("*", "")
        assert "point into the Cairn repository" in normalized, (
            "format-neutrality section must explicitly state that "
            "Cairn-shipped references point into the Cairn repo, "
            "not the adopter's tree"
        )


class TestModuleDisambiguation:
    """Chunk 3 also disambiguates further-reading cross-references in
    every team-gated module that ships one, per Antigravity-3 option
    (i) link-text disambiguation."""

    MODULES_WITH_FURTHER_READING = (
        "examples-gallery",
        "doc-drift-prevention",
        "testing-discipline",
    )

    @pytest.mark.parametrize("module", MODULES_WITH_FURTHER_READING)
    def test_module_uses_cairns_own_prefix(self, module: str) -> None:
        """Every team-gated module that references further-reading
        must carry the 'Cairn's own' link-text prefix so the
        reference target is unambiguously Cairn-owned."""
        path = (
            CAIRN_ROOT
            / "templates"
            / "modules"
            / "team-gated"
            / f"{module}.md"
        )
        text = path.read_text(encoding="utf-8")
        assert "further-reading" in text, (
            f"{module}.md must reference further-reading (sanity)"
        )
        # Every further-reading reference must carry the prefix.
        for line in text.splitlines():
            if "further-reading" in line and "](" in line:
                assert "Cairn's own" in line, (
                    f"{module}.md line containing a further-reading "
                    f"link must carry the 'Cairn's own' prefix:\n"
                    f"  {line}"
                )

    @pytest.mark.parametrize("module", MODULES_WITH_FURTHER_READING)
    def test_module_uses_cairn_prefixed_path(self, module: str) -> None:
        """Every team-gated module that references further-reading
        must use the `cairn/docs/further-reading.md` form in link
        text (not bare `docs/further-reading.md`) so the path itself
        carries the Cairn-tree origin."""
        path = (
            CAIRN_ROOT
            / "templates"
            / "modules"
            / "team-gated"
            / f"{module}.md"
        )
        text = path.read_text(encoding="utf-8")
        assert "[cairn/docs/further-reading.md]" in text, (
            f"{module}.md must use the [cairn/docs/further-reading.md] "
            f"form in link text (not bare [docs/further-reading.md]).  "
            f"Backticks around the link text removed per the style-guide "
            f"rule prohibiting backticks in link labels (Antigravity "
            f"code-review P2)."
        )


class TestInstalledAdopterWording:
    """Per Codex-3 of the proposal review: the test must read the
    **installed** team-gated module text (post-scaffold), not just
    the template source.  This guards against the adopter-facing
    surface drifting from the source via a substitution bug.
    """

    @pytest.fixture
    def scaffolded_target(self, tmp_path) -> Path:
        """Install the three team-gated modules into a fresh fixture
        tree using the same install path the scaffold uses."""
        import sys
        sys.path.insert(0, str(CAIRN_ROOT))
        from bootstrap.scaffold import (  # noqa: E402
            create_dev_tree,
            install_modules,
        )
        templates_root = CAIRN_ROOT / "templates"
        create_dev_tree(tmp_path)
        for module in TestModuleDisambiguation.MODULES_WITH_FURTHER_READING:
            install_modules(templates_root, tmp_path, {}, [module])
        return tmp_path

    @pytest.mark.parametrize(
        "module", TestModuleDisambiguation.MODULES_WITH_FURTHER_READING
    )
    def test_installed_module_carries_cairns_own_prefix(
        self, scaffolded_target: Path, module: str
    ) -> None:
        """The rendered installed module under
        ``dev/modules/<name>.md`` must carry the 'Cairn's own'
        prefix on every further-reading reference -- the adopter-
        facing surface, not just the source."""
        installed = scaffolded_target / "dev" / "modules" / f"{module}.md"
        assert installed.is_file(), (
            f"{module}.md must install to dev/modules/ on scaffold"
        )
        text = installed.read_text(encoding="utf-8")
        for line in text.splitlines():
            if "further-reading" in line and "](" in line:
                assert "Cairn's own" in line, (
                    f"installed {module}.md line containing a further-"
                    f"reading link must carry the 'Cairn's own' "
                    f"prefix (post-scaffold):\n  {line}"
                )

    @pytest.mark.parametrize(
        "module", TestModuleDisambiguation.MODULES_WITH_FURTHER_READING
    )
    def test_installed_module_does_not_assume_adopter_markdown(
        self, scaffolded_target: Path, module: str
    ) -> None:
        """The rendered installed module must NOT imply the
        adopter's `docs/` is Markdown.  Specifically: a bare
        `docs/further-reading.md` token (without the `cairn/`
        prefix in the link text) would suggest the adopter has
        such a file; with the disambiguation, the reference is
        explicitly Cairn-owned."""
        installed = scaffolded_target / "dev" / "modules" / f"{module}.md"
        text = installed.read_text(encoding="utf-8")
        # The presence of bare `docs/further-reading.md` in link
        # text (without the cairn/ prefix) is what Antigravity-3
        # was trying to remove.  After Chunk 3's disambiguation,
        # the link text uses `cairn/docs/further-reading.md`.
        assert "[cairn/docs/further-reading.md]" in text, (
            f"installed {module}.md must use the [cairn/docs/further-"
            f"reading.md] form in link text (cairn/-prefixed; not "
            f"backticked, per the style-guide rule prohibiting "
            f"backticks in link labels -- Antigravity code-review P2)."
        )


class TestStyleConventionsLocation:
    """Chunk 7 of the docs-architecture-cleanup plan adds the style-
    conventions-location paragraph (parallel to common-homes-for-
    vision)."""

    def test_style_conventions_section_present(self, doc_text: str) -> None:
        assert (
            "Common homes for project-specific style conventions" in doc_text
        ), (
            "doc-governance.md must declare the style-conventions-"
            "location section"
        )

    def test_names_descriptive_layer_as_principle(self, doc_text: str) -> None:
        """The section must explicitly state that style is
        descriptive-layer content, not governing doctrine."""
        import re
        normalized = re.sub(r"\s+", " ", doc_text)
        normalized = normalized.replace("**", "").replace("*", "")
        assert "descriptive layer is the right home" in normalized, (
            "style-conventions section must explicitly state the "
            "descriptive layer is the right home for style conventions"
        )

    def test_names_multiple_style_homes(self, doc_text: str) -> None:
        """The section enumerates multiple typical homes for style
        guides, per the recorded chat preference."""
        for home in (
            "`docs/developer/style.md`",
            "`docs/style.md`",
            "`STYLE_GUIDE.md`",
        ):
            assert home in doc_text, (
                f"style-conventions section must name {home} as a "
                f"typical style-guide home"
            )

    def test_is_non_prescriptive(self, doc_text: str) -> None:
        """The section must defer to the adopter, parallel to the
        common-homes-for-vision section."""
        assert "adopter picks" in doc_text.lower(), (
            "style-conventions section must explicitly defer to the "
            "adopter (parallel to common-homes-for-vision)"
        )
