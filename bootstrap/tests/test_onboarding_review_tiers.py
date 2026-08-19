"""Guard test for the review-record-integrity proposal's Part A: no shipped
onboarding preset may claim that fresh-session / same-vendor review fills
or staffs the External review tier (`doctrine/dual-review.md:46-47` -- the
External floor requires a different agent type or a human).

Two independent guards (plan `review-record-integrity` -- the
proposal's original bare "External" + "fresh-session" co-occurrence spec
false-positives on legitimate text in `collaborative-team.md` /
`high-rigor-legacy.md`, verified during plan authoring, so this splits into
a literal regression guard + a scoped semantic guard rather than one bare
rule):

* A curated, case-insensitive, whitespace-normalized forbidden-phrase list
  scanned across every `templates/onboarding/*.md` preset -- catches a
  regression of either wording the fix removed from `solo-greenfield.md`.
* A positive-predication check scoped to `solo-greenfield.md` only -- any
  paragraph naming "External" together with "tier" must also name its
  staffing ("human Maintainer" or a second/different agent type) in the
  same paragraph. Scoped narrowly (not applied to the other two presets,
  which already staff External correctly without always repeating a
  staffing token in the same paragraph) and keyed on "tier" specifically
  (not "review") so it does not false-positive on the file's unrelated
  "Per Codex External Review P2-3" authorship-credit line.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_onboarding_review_tiers.py
"""
from __future__ import annotations

import re
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
ONBOARDING_DIR = CAIRN_ROOT / "templates" / "onboarding"

# The two false-predication wordings the review-record-integrity fix
# removed from templates/onboarding/solo-greenfield.md.
# Matched case-insensitively against whitespace-normalized text so a
# reflow / line-wrap change can't dodge the guard.
_FORBIDDEN_PHRASES = (
    "external tier (currently filled by fresh-session same-vendor review)",
    "fresh-session external review tier reproducible",
)

_STAFFING_TOKENS = (
    "human maintainer",
    "different agent type",
    "second agent type",
)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _onboarding_files() -> list[Path]:
    return sorted(ONBOARDING_DIR.glob("*.md"))


def _paragraphs(text: str) -> list[str]:
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def test_onboarding_presets_exist() -> None:
    files = _onboarding_files()
    assert files, f"no onboarding presets found under {ONBOARDING_DIR}"


def test_no_forbidden_predication_in_any_preset() -> None:
    """Universal regression guard: neither removed wording may reappear in
    any shipped onboarding preset."""
    violations = []
    for path in _onboarding_files():
        normalized = _normalize(path.read_text(encoding="utf-8"))
        for phrase in _FORBIDDEN_PHRASES:
            if phrase in normalized:
                violations.append(f"{path.name}: contains forbidden phrase {phrase!r}")
    assert not violations, "\n".join(violations)


def test_solo_greenfield_external_tier_paragraphs_name_their_staffing() -> None:
    """Positive-predication check, scoped to solo-greenfield.md -- any
    paragraph naming "External" together with "tier" must name who staffs
    it. Not applied to the other two presets (see module docstring)."""
    path = ONBOARDING_DIR / "solo-greenfield.md"
    text = path.read_text(encoding="utf-8")
    checked = 0
    violations = []
    for para in _paragraphs(text):
        low = para.lower()
        if "external" not in low or "tier" not in low:
            continue
        checked += 1
        if not any(token in low for token in _STAFFING_TOKENS):
            violations.append(para.strip().splitlines()[0])
    assert checked == 3, (
        f"expected exactly the 3 corrected External-tier passages in "
        f"{path.name}, matched {checked} paragraph(s) -- guard may be "
        f"scanning the wrong file, or a passage moved/was added"
    )
    assert not violations, (
        "paragraph(s) name External+tier without naming staffing:\n"
        + "\n".join(violations)
    )


def test_positive_fixture_both_tiers_named_together_passes() -> None:
    """Synthetic positive fixture: a minimal snippet
    that correctly names both tiers in one passage must NOT trip the
    forbidden-phrase guard, even though it mentions "External" and
    "fresh-session" in the same paragraph -- this is exactly the shape
    Part A's own fix produces (Row 1's corrected text), and the original
    bare co-occurrence spec would have wrongly flagged it."""
    fixture = (
        "The roster makes the fresh-session Internal review tier "
        "reproducible; the External floor is filled by the human "
        "Maintainer's read."
    )
    normalized = _normalize(fixture)
    for phrase in _FORBIDDEN_PHRASES:
        assert phrase not in normalized, (
            f"positive fixture wrongly matched forbidden phrase {phrase!r}"
        )
    assert any(token in normalized for token in _STAFFING_TOKENS)


def test_negative_fixture_old_mislabel_wordings_are_caught() -> None:
    """Sanity check the forbidden-phrase list actually catches both known
    wordings (an empty/too-narrow list would make
    test_no_forbidden_predication_in_any_preset pass vacuously)."""
    old_wording_1 = (
        "strengthens Dual-Review's External tier (currently filled by "
        "fresh-session same-vendor review)."
    )
    old_wording_2 = (
        "The roster makes the fresh-session External review tier "
        "reproducible (the second session...)."
    )
    assert any(p in _normalize(old_wording_1) for p in _FORBIDDEN_PHRASES)
    assert any(p in _normalize(old_wording_2) for p in _FORBIDDEN_PHRASES)
