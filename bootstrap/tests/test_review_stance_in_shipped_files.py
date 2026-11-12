"""Retained structure, copy, and install-template checks for review materials.

Fixed-wording retirements and their reader clearances are recorded in the
functional-prose plan. These checks cover roster slots, template
fields/placeholders, copy parity, roster fidelity, and the figure's accessible
structure and geometry.

Promises:
- Cairn's own copies of the model-selection module, session-start skill and
  onboarding pages match their shipped or public sources byte for byte.
- The fidelity manifest's sample roster names exactly the roles the review loop
  document defines.
- The review figure carries an accessible title and description, and its
  description opens with the title.
- The review figure keeps a 640 by 260 viewBox and no fixed width or height, so
  pages that embed it can scale it.
- Mergeable templates carry no one-word double-brace placeholder the engine
  cannot fill, so an upgrade can advance them.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent

#: The shipped copy is the load-bearing one (adopters receive it). Cairn's own
#: copy keeps Cairn bound by what it ships.
SHIPPED_AGENTS = "templates/core/AGENTS.md"
SHIPPED_LOOP = "templates/core/dev/agent_collaboration.md"
OWN_LOOP = "dev/agent_collaboration.md"

SHIPPED_PROPOSAL = "templates/core/dev/proposals/_template.md"
OWN_PROPOSAL = "dev/proposals/_template.md"
SHIPPED_PLAN = "templates/core/dev/plans/_template.md"
OWN_PLAN = "dev/plans/_template.md"

_PROPOSAL_TEMPLATES = (SHIPPED_PROPOSAL, OWN_PROPOSAL)
_PLAN_TEMPLATES = (SHIPPED_PLAN, OWN_PLAN)
_TEMPLATE_FILES = _PROPOSAL_TEMPLATES + _PLAN_TEMPLATES
_FILE_IDS = {
    SHIPPED_PROPOSAL: "shipped-proposal", OWN_PROPOSAL: "own-proposal",
    SHIPPED_PLAN: "shipped-plan", OWN_PLAN: "own-plan",
}

def _text(rel: str) -> str:
    return (CAIRN_ROOT / rel).read_text(encoding="utf-8")

def _section(text: str, heading: str) -> str:
    """The body of `## <heading>`, up to the next second-level heading."""
    match = re.search(rf"^## {re.escape(heading)}$(.*?)(?=^## |\Z)", text,
                      re.M | re.S)
    assert match, f"no '## {heading}' section"
    return match.group(1)

def test_team_roster_has_its_own_section_without_adding_roles() -> None:
    shipped = _section(_text(SHIPPED_LOOP), "The team")
    assert "<!-- cairn:slot team-roster -->" in shipped
    assert "<!-- cairn:end team-roster -->" in shipped

# --------------------------------------------------------------------------
# The authoring templates: the proposal and plan templates, each with Cairn's
# own copy. They are read while writing and while reviewing.
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Template field and skeleton checks.
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# The capability-floor copies and the session-start pair.
# --------------------------------------------------------------------------

SHIPPED_MODEL = "templates/modules/team-gated/model-selection.md"
OWN_MODEL = "dev/modules/model-selection.md"
SHIPPED_SKILL = "templates/skills/session-start/SKILL.md"
OWN_SKILL = ".agents/skills/session-start/SKILL.md"
FIDELITY = "bootstrap/fidelity-check.md"

def test_the_model_selection_pair_is_byte_identical() -> None:
    """The installed copy is a verbatim copy of the shipped module."""
    assert _text(SHIPPED_MODEL) == _text(OWN_MODEL)

def test_the_session_start_twins_are_byte_identical() -> None:
    assert _text(SHIPPED_SKILL) == _text(OWN_SKILL)

def _roster_names(text: str) -> list[str]:
    """Role names from the loop document's `## Team roles` bullets."""
    section = _section(text, "Team roles")
    return re.findall(r"(?m)^\* \*\*([^*]+)\*\*", section)

def _fidelity_roles() -> list[str]:
    match = re.search(r"(?m)^roles:\n((?:  - .+\n)+)", _text(FIDELITY))
    assert match, "no sample roster in the fidelity manifest"
    return [line[4:].strip() for line in match.group(1).splitlines()]

def test_the_fidelity_sample_roster_agrees_with_the_loop_document() -> None:
    """The manifest's sample is read by people deciding whether an install is
    faithful, so it must not describe roles the install does not have."""
    roster = _roster_names(_text(SHIPPED_LOOP))
    assert _fidelity_roles() == roster
    assert _roster_names(_text(OWN_LOOP)) == roster


# --------------------------------------------------------------------------
# The figure and onboarding-copy checks retain accessible structure, geometry,
# source/install parity, and the explicit drift negative control.
# --------------------------------------------------------------------------

FIGURE = "docs/assets/dual-review-independence.svg"
DOCS_ONBOARDING = "docs/agent-team-onboarding.md"
INSTALLED_ONBOARDING = "dev/modules/onboarding/agent-team-onboarding.md"
DOCS_TOUR = "docs/dev-tour.md"
INSTALLED_TOUR = "dev/modules/onboarding/dev-tour.md"

#: Pin the contract, not its location, repetition count, or exact prose.

#: Literal sentences locate independent deletion controls and alternate wording.
#: Do not derive either from the obligation regex under test.

#: Wording the descriptive pages must not carry: a review that has to come from
#: a different model or person, a tier, a floor, or the old two-stage picture.

def test_the_review_figure_keeps_an_accessible_conclusion() -> None:
    import xml.etree.ElementTree as ET
    root = ET.fromstring(_text(FIGURE))
    ns = "{http://www.w3.org/2000/svg}"
    title = " ".join(root.find(ns + "title").text.split())
    desc = " ".join(root.find(ns + "desc").text.split())
    assert root.get("aria-labelledby") == "fig-title fig-desc"
    assert desc.startswith(title), "the description opens with the figure text"

def test_the_figure_parses_and_keeps_its_embed_geometry() -> None:
    import xml.etree.ElementTree as ET
    root = ET.fromstring(_text(FIGURE))
    assert root.get("viewBox") == "0 0 640 260"
    assert root.get("width") is None and root.get("height") is None

@pytest.mark.parametrize("page,copy", [(DOCS_ONBOARDING, INSTALLED_ONBOARDING),
                                       (DOCS_TOUR, INSTALLED_TOUR)])
def test_an_installed_onboarding_copy_equals_its_page(page: str, copy: str) -> None:
    """Both pages reach every install that selects a preset, byte for byte."""
    assert _text(page) == _text(copy), (
        f"{copy} differs from {page}; they are one document in two places.")


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# A placeholder written as one word between double braces is an install token
# to the engine. An upgrade plans a file that carries one the install never
# recorded as "needs a value", and the file never advances. So a mergeable
# template may carry such a placeholder only if it is a token the engine fills
# or one it knowingly leaves for the document's author. Prose placeholders in a
# template use angle brackets, or braces around more than one word.
# --------------------------------------------------------------------------

def _engine_token_rules():
    import sys
    sys.path.insert(0, str(CAIRN_ROOT))
    from bootstrap._scaffold.config import KNOWN_TOKENS
    from bootstrap._scaffold.slotmerge import find_unfilled_tokens
    return KNOWN_TOKENS, find_unfilled_tokens

def _mergeable_template_files() -> list[str]:
    """Every core template, plus Cairn's own copies of the two authoring ones."""
    core = sorted(p.relative_to(CAIRN_ROOT).as_posix()
                  for p in (CAIRN_ROOT / "templates" / "core").rglob("*")
                  if p.is_file() and p.suffix in {".md", ".yml", ".txt"})
    return core + [OWN_PROPOSAL, OWN_PLAN]

def _unknown_install_tokens(text: str) -> set[str]:
    known, unfilled = _engine_token_rules()
    return set(unfilled(text)) - set(known)

@pytest.mark.parametrize("rel", _mergeable_template_files(),
                         ids=lambda r: r.replace("/", "-"))
def test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill(
        rel: str) -> None:
    left = _unknown_install_tokens(_text(rel))
    assert not left, (
        f"{rel} carries {sorted(left)} between double braces. The engine reads "
        f"a one-word placeholder as an install token, so every adopter's "
        f"upgrade plans this file as needing a value and never advances it. "
        f"Write an angle-bracket placeholder instead.")
