# SPDX-License-Identifier: MIT
"""The model-tier rule reaches every install, and the cost-rule edits hold.

Four properties, each read from the files an adopter receives:

* every `AGENTS.md` copy carries the same "Model tier" rule, under `## Roles`,
  and a profile that installs no model-selection module still receives it;
* the "different maker" condition is gone from every place that stated it, and
  a model at the same tier as the author is still not a sufficient check;
* proposal authoring is a medium-tier task, with proposal review still high;
* the check that finds a missing clause is itself shown to fire on a mutant,
  beside a control run on the real text.

`test_review_stance_in_shipped_files.py` pins the sentences that also sit in its
tables. This file pins what that one does not: the rule under `## Roles` (its
table is read only inside `## Review`), and the places its patterns do not reach.
"""
from pathlib import Path
import re
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]

SHIPPED_AGENTS = "templates/core/AGENTS.md"
OWN_AGENTS = "AGENTS.md"
ROLES = "doctrine/roles.md"
SHIPPED_MODULE = "templates/modules/team-gated/model-selection.md"
OWN_MODULE = "dev/modules/model-selection.md"
AGENTS_COPIES = [SHIPPED_AGENTS, OWN_AGENTS]
MODULE_COPIES = [SHIPPED_MODULE, OWN_MODULE]

#: label -> a clause the rule must carry. Each clause is matched on text with
#: whitespace collapsed, so a re-wrapped line does not hide it.
_RULE_CLAUSES = {
    "names-the-rule": "**Model tier.**",
    "lowest-capability-model": (
        "Use the lowest-capability model that can do the task safely"),
    "the-lane-sets-the-tier": (
        "low for the trivial lane, medium for the standard lane, the role's "
        "floor for the deliberate lane"),
    "proposal-authoring-is-medium": "Proposal authoring is medium;",
    "bright-line-work-stays-high": (
        "Security Review, proposal review, premise-checking and other "
        "bright-line work stay high."),
    "no-downshift-across-data-governance": (
        "Never downshift across a data-governance boundary."),
    "name-the-model-at-every-spawn": "**Name the model at every spawn**",
    "escalate-one-tier": "re-run once one tier up",
    "reviewer-flags-work-below-its-floor": (
        "A reviewer who sees work written below its floor"),
}

#: Wordings of the retired condition. The shipped sentence is
#: "a stronger model from the same maker counts"; these say the opposite.
_RETIRED_CONDITION = {
    "same-maker-is-not-one": r"same maker is not one",
    "and-is-a-different-model-architecture": (
        r"\band is a different model architecture\b"
    ),
    "and-a-different-model-architecture-bold": (
        r"\*\*and\*\* (?:is )?a different model architecture"
    ),
}

#: The one sentence that says how a proposal's premise-check is tiered. It must
#: read the same in every place that states the proposal-authoring tier.
_PREMISE_CHECK = (
    "A premise-check inside a proposal is its own task, spawned at high, its "
    "result handed to the medium draft."
)


def _flat(text: str) -> str:
    """Collapse whitespace and blockquote markers so a re-wrap hides nothing."""
    text = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    return " ".join(text.split())


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _roles_section(text: str) -> str:
    """The `## Roles` section: from its heading to the next level-two heading."""
    heading = re.search(r"^## Roles$", text, re.MULTILINE)
    assert heading, "no level-two heading 'Roles'"
    end = text.find("\n## ", heading.end())
    return text[heading.start():] if end == -1 else text[heading.start():end]


def _missing_rule_clauses(text: str) -> list[str]:
    flat = _flat(text)
    return sorted(label for label, clause in _RULE_CLAUSES.items()
                  if clause not in flat)


def _retired_condition(text: str) -> list[str]:
    flat = _flat(text)
    return sorted(label for label, pattern in _RETIRED_CONDITION.items()
                  if re.search(pattern, flat))


@pytest.mark.parametrize("rel", AGENTS_COPIES, ids=["shipped-agents", "own-agents"])
def test_both_agents_copies_carry_the_model_tier_rule(rel: str) -> None:
    """Every project reads `AGENTS.md`, so the rule must be in each source copy."""
    assert _missing_rule_clauses(_roles_section(_read(rel))) == []


def test_the_rule_reads_the_same_in_both_copies() -> None:
    """Cairn is bound by the rule it ships, so the two copies must not drift."""
    def rule(rel: str) -> str:
        flat = _flat(_roles_section(_read(rel)))
        start = flat.index("**Model tier.**")
        return flat[start:]
    assert rule(OWN_AGENTS) == rule(SHIPPED_AGENTS)


@pytest.mark.parametrize("rel", AGENTS_COPIES, ids=["shipped-agents", "own-agents"])
def test_the_rule_sits_under_roles(rel: str) -> None:
    """The rule belongs to the roles it tiers; moved elsewhere, it is found late."""
    text = _read(rel)
    assert "**Model tier.**" in _roles_section(text)
    assert _flat(text).count("**Model tier.**") == 1


def test_deleting_the_name_the_model_sentence_is_reported() -> None:
    """The clause check must fire on a mutant, beside a green control run."""
    real = _roles_section(_read(OWN_AGENTS))
    assert _missing_rule_clauses(real) == []          # control
    mutant = real.replace("**Name the model at every spawn**", "**Name it**")
    assert "name-the-model-at-every-spawn" in _missing_rule_clauses(mutant)


@pytest.fixture(scope="module")
def solo_install(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A real install of the smallest profile, which installs no module."""
    target = tmp_path_factory.mktemp("model-tier") / "project"
    target.mkdir()
    result = subprocess.run(
        [sys.executable, str(ROOT / "bootstrap/scaffold.py"),
         "--config", str(ROOT / "bootstrap/profiles/solo-greenfield.yml"),
         "--target", str(target), "--cairn-root", str(ROOT), "--allow-dev"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return target


def test_a_profile_with_no_module_still_installs_the_rule(solo_install: Path) -> None:
    """The rule is in the core file, not the module a solo profile never gets."""
    assert not (solo_install / "dev/modules/model-selection.md").exists()
    installed = (solo_install / "AGENTS.md").read_text(encoding="utf-8")
    assert _missing_rule_clauses(_roles_section(installed)) == []


def test_the_different_maker_condition_is_gone_and_same_tier_is_excluded() -> None:
    """A one-maker team may use a stronger model of its own as the check.

    The pinned patterns in the review-stance test hold the new sentence in the
    module copies and the roles paragraph on the cost rule's check. This pins the
    rest: the fan-out paragraph states it, no place still carries the old
    condition, and a model at the same tier as the author still does not count.
    """
    places = [ROLES, *MODULE_COPIES]
    texts = {rel: _read(rel) for rel in places}

    def violations(by_place: dict[str, str]) -> dict[str, list[str]]:
        found = {rel: _retired_condition(t) for rel, t in by_place.items()}
        return {rel: labels for rel, labels in found.items() if labels}

    assert violations(texts) == {}                     # control

    fan_out = _flat(texts[ROLES])
    start = fan_out.index("Orchestrated work — the fan-out.")
    paragraph = fan_out[start:].split(" Escalation applies", 1)[0]
    assert "a stronger model from the same maker counts" in paragraph
    assert "a model at the same tier does not" in paragraph
    for rel in MODULE_COPIES:
        flat = _flat(texts[rel])
        assert flat.count("a model at the same tier does not") == 2, rel

    mutant = dict(texts)
    mutant[SHIPPED_MODULE] = texts[SHIPPED_MODULE] + (
        "\n> author **and** is a different model architecture (a stronger model "
        "from the same maker is not one)\n")
    assert SHIPPED_MODULE in violations(mutant)


def test_proposal_authoring_is_medium_and_proposal_review_stays_high() -> None:
    """Authoring a proposal is medium; reviewing one, and a premise-check, stay high."""
    for rel in MODULE_COPIES:
        flat = _flat(_read(rel))
        assert re.search(r"\| Proposal authoring \| medium \|", flat), rel
        assert re.search(r"\| Proposal review \| high \|", flat), rel
        assert _PREMISE_CHECK in flat, rel
    assert _read(SHIPPED_MODULE) == _read(OWN_MODULE)

    roles = _read(ROLES)
    standard = re.search(
        r"\* \*\*Standard-stakes roles\*\*(.*?)\n\* \*\*Low-stakes", roles, re.S)
    high = re.search(
        r"\* \*\*High-stakes roles\*\*(.*?)\n\* \*\*Standard-stakes", roles, re.S)
    assert standard and high
    assert "proposal authoring" in _flat(standard.group(1))
    assert _PREMISE_CHECK in _flat(standard.group(1))
    assert "proposal review" in _flat(high.group(1))
    assert "proposal authoring is standard-stakes" in _flat(high.group(1))

    for rel in AGENTS_COPIES:
        assert "Proposal authoring is medium;" in _flat(_read(rel))
