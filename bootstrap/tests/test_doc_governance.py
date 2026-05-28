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
        assert "The descriptive layer (`docs/`)" in doc_text, (
            "doc-governance.md must declare the descriptive-layer "
            "tier-recognition section"
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
        """Per the maintainer's layer-prescriptiveness gradient (M1):
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
