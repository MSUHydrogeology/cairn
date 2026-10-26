# SPDX-License-Identifier: MIT
"""The writing standard reaches every install, and nothing tells agents to score prose.

Cairn Plain Language is a section of `dev/agent_collaboration.md`, which every
install receives; `AGENTS.md` carries a one-sentence pointer to it. Three
things are pinned, each against what a fresh install actually wrote, because a
test that read only the template would stay green if an install path dropped
the section:

* the section, its version line and its group headings are in the installed
  collaboration doc, and its rules are numbered 1 to 17 in order;
* the pointer sentence is in the installed `AGENTS.md` and in both source
  copies, so Cairn is bound by what it ships;
* no copy tells an agent to use a readability score: the only mentions are the
  rule that forbids one, and no named scoring formula appears.
"""
from pathlib import Path
import re
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]

SHIPPED_AGENTS = "templates/core/AGENTS.md"
OWN_AGENTS = "AGENTS.md"
SHIPPED_LOOP = "templates/core/dev/agent_collaboration.md"
OWN_LOOP = "dev/agent_collaboration.md"

_POINTER = (
    "Cairn Plain Language, in `dev/agent_collaboration.md`, gives the rules "
    "for writing plainly; in chat as everywhere, separate what you measured "
    "from what you assumed, give numbers with their sources, and say what "
    "you did not check."
)
_GROUP_HEADINGS = (
    "**Before you write**",
    "**Everything**",
    "**Instructions**",
    "**Scientific and technical reasoning**",
    "**Checking.**",
)
_SCORE_FORMULAS = re.compile(
    r"flesch|gunning|hemingway|smog index|coleman|grade[- ]level score",
    re.IGNORECASE,
)


def _flat(text: str) -> str:
    """Collapse whitespace so a re-wrapped line does not hide a match."""
    return " ".join(text.split())


def _section(text: str) -> str:
    """The standard's section: from its heading to the next level-two heading."""
    heading = re.search(r"^## Cairn Plain Language$", text, re.MULTILINE)
    assert heading, "no level-two heading 'Cairn Plain Language'"
    start = heading.start()
    end = text.find("\n## ", start + 1)
    return text[start:] if end == -1 else text[start:end]


def _assert_before_surfacing(text: str) -> None:
    """The standard sits just ahead of the Maintainer-escalation section."""
    standard = re.search(r"^## Cairn Plain Language$", text, re.MULTILINE)
    surfacing = re.search(
        r"^## Surfacing judgment calls to the Maintainer$", text, re.MULTILINE
    )
    assert standard and surfacing
    assert standard.start() < surfacing.start()
    between = text[standard.end():surfacing.start()]
    assert "\n## " not in between, "another level-two section sits between them"


@pytest.fixture(scope="module")
def installed(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A fresh install of the smallest configuration: core plus one module."""
    base = tmp_path_factory.mktemp("writing-rules")
    config = base / "profile.yml"
    config.write_text(
        "project_name: Writing-Rules-Test\ntest_command: pytest\n"
        "modules:\n  - issue-capture\n",
        encoding="utf-8",
    )
    target = base / "project"
    target.mkdir()
    result = subprocess.run(
        [sys.executable, str(ROOT / "bootstrap/scaffold.py"),
         "--config", str(config), "--target", str(target),
         "--cairn-root", str(ROOT), "--allow-dev"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return target


def test_standard_with_version_and_groups_reaches_install(installed: Path) -> None:
    """An adopter's agent must find the named, versioned standard where it is told to look."""
    doc = (installed / "dev/agent_collaboration.md").read_text(encoding="utf-8")
    section = _section(doc)
    assert section.startswith("## Cairn Plain Language")
    assert "*Version 1.0." in section
    assert "Licensed CC BY 4.0" in _flat(section)
    for heading in _GROUP_HEADINGS:
        assert heading in section, heading
    numbers = [int(n) for n in re.findall(r"^(\d+)\. ", section, re.MULTILINE)]
    assert numbers == list(range(1, 18))


def test_install_writes_the_shipped_standard_unchanged(installed: Path) -> None:
    """The install must not drop, reword or substitute any part of the section."""
    shipped = _section((ROOT / SHIPPED_LOOP).read_text(encoding="utf-8"))
    out = _section((installed / "dev/agent_collaboration.md").read_text(encoding="utf-8"))
    assert _flat(out) == _flat(shipped)


@pytest.mark.parametrize("source", [SHIPPED_LOOP, OWN_LOOP], ids=["shipped-loop", "own-loop"])
def test_standard_sits_just_before_surfacing_judgment_calls(source: str) -> None:
    """The place is part of the doc's order; a moved section changes what readers meet."""
    _assert_before_surfacing((ROOT / source).read_text(encoding="utf-8"))


def test_installed_standard_sits_just_before_surfacing_judgment_calls(installed: Path) -> None:
    """An install must keep the standard's place, not only its text."""
    _assert_before_surfacing(
        (installed / "dev/agent_collaboration.md").read_text(encoding="utf-8")
    )


def test_cairns_own_copy_says_what_it_ships() -> None:
    """Cairn is bound by the standard it ships, so the two copies must agree."""
    shipped = _section((ROOT / SHIPPED_LOOP).read_text(encoding="utf-8"))
    own = _section((ROOT / OWN_LOOP).read_text(encoding="utf-8"))
    assert _flat(own) == _flat(shipped)


def test_pointer_sentence_is_in_the_installed_agents_file(installed: Path) -> None:
    """The pointer is how an agent that reads only AGENTS.md meets the standard."""
    agents = _flat((installed / "AGENTS.md").read_text(encoding="utf-8"))
    assert _POINTER in agents


@pytest.mark.parametrize(
    "source", [SHIPPED_AGENTS, OWN_AGENTS], ids=["shipped-agents", "own-agents"]
)
def test_pointer_sentence_is_in_both_source_agents_files(source: str) -> None:
    """Cairn's own AGENTS.md and the shipped one must both carry the pointer."""
    agents = _flat((ROOT / source).read_text(encoding="utf-8"))
    assert _POINTER in agents
    floor = agents.index("as a **mandatory pause**.")
    assert agents.index(_POINTER) == floor + len("as a **mandatory pause**. ")


@pytest.mark.parametrize(
    "source", [SHIPPED_AGENTS, OWN_AGENTS, SHIPPED_LOOP, OWN_LOOP],
    ids=["shipped-agents", "own-agents", "shipped-loop", "own-loop"],
)
def test_no_copy_tells_agents_to_use_a_readability_score(source: str) -> None:
    """A score becomes the target; the standard is checked by reading instead."""
    text = _flat((ROOT / source).read_text(encoding="utf-8"))
    assert not _SCORE_FORMULAS.search(text)
    for match in re.finditer(r"readability", text, re.IGNORECASE):
        assert text[: match.start()].endswith("never by a "), text[match.start() - 40:match.end() + 20]


def test_installed_standard_forbids_a_readability_score(installed: Path) -> None:
    """The installed text must say the rules are checked by reading, never by a score."""
    doc = _flat(
        (installed / "dev/agent_collaboration.md").read_text(encoding="utf-8")
    )
    assert "checked by reading, never by a readability score" in doc
