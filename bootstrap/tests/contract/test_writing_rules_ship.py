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


ROOT = Path(__file__).resolve().parents[3]

SHIPPED_AGENTS = "templates/core/AGENTS.md"
OWN_AGENTS = "AGENTS.md"
SHIPPED_LOOP = "templates/core/dev/agent_collaboration.md"
OWN_LOOP = "dev/agent_collaboration.md"
PUBLIC_DOC = "docs/plain-language.md"
CHANGED_RULES = (2, 5, 13, 14, 17)

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
    assert "*Version 1.1." in section
    assert "Licensed CC BY 4.0" in _flat(section)
    for heading in _GROUP_HEADINGS:
        assert heading in section, heading
    numbers = [int(n) for n in re.findall(r"^(\d+)\. ", section, re.MULTILINE)]
    assert numbers == list(range(1, 18))


def _public_section(text: str) -> str:
    """The copyable standard inside the public page, not its surrounding guide."""
    match = re.search(
        r"^````markdown\n(## Cairn Plain Language\n.*?)(?=^````$)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    assert match, "no fenced Cairn Plain Language standard in public page"
    return match.group(1)


def _numbered_rule(section: str, number: int) -> str:
    """Return one numbered rule without its following group heading."""
    starts = list(re.finditer(r"^(\d+)\. ", section, re.MULTILINE))
    matches = [match for match in starts if int(match.group(1)) == number]
    assert len(matches) == 1, f"rule {number} occurs {len(matches)} times"
    start = matches[0].start()
    following = [match.start() for match in starts if match.start() > start]
    heading = re.search(r"^\*\*", section[start:], re.MULTILINE)
    ends = following[:]
    if heading:
        ends.append(start + heading.start())
    end = min(ends) if ends else len(section)
    return _flat(section[start:end])


def test_changed_rules_match_across_local_shipped_and_public_copies() -> None:
    """Versioned rule wording stays aligned while surrounding context can differ."""
    copies = {
        "local": _section((ROOT / OWN_LOOP).read_text(encoding="utf-8")),
        "shipped": _section((ROOT / SHIPPED_LOOP).read_text(encoding="utf-8")),
        "public": _public_section((ROOT / PUBLIC_DOC).read_text(encoding="utf-8")),
    }
    for number in CHANGED_RULES:
        rules = {name: _numbered_rule(section, number)
                 for name, section in copies.items()}
        assert len(set(rules.values())) == 1, f"rule {number} differs: {rules}"


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
    floor = agents.index("pause and say so.")
    assert agents.index(_POINTER) == floor + len("pause and say so. ")


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


# The installed template files retain their own and shipped source bytes.
_INSTALLED_PROMPT_SOURCES = {
    "dev/proposals/_template.md": (
        "templates/core/dev/proposals/_template.md",
    ),
    "dev/plans/_template.md": (
        "templates/core/dev/plans/_template.md",
    ),
    "dev/strategy/_template.md": (
        "templates/core/dev/strategy/_template.md",
    ),
}


def _copy_prompt_member(source_root: Path, rel: str, target_root: Path) -> Path:
    """Copy one named prompt member into an isolated physical test root."""
    source = source_root / rel
    target = target_root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    return target


@pytest.mark.parametrize("rel,sources", sorted(_INSTALLED_PROMPT_SOURCES.items()))
def test_installed_readable_prompt_and_contrary_mutation(
        installed: Path, rel: str, sources: tuple[str, ...]) -> None:
    """A real install preserves each shipped template at its destination."""
    output = (installed / rel).read_bytes()
    assert output == (ROOT / sources[0]).read_bytes()


_LOCAL_RETRY_LABEL = "Cairn-only execution retries."
_LOCAL_RETRY_OVERRIDE = (
    "This local budget overrides immediate escalation for ordinary execution; "
    "the shipped rule and broader methodology remain unchanged."
)
_ADOPTER_RETRY_LIMIT = (
    "allow up to two same-tier retries after the initial failed attempt"
)


def _assert_adopter_retry_guidance(root: Path, rel: str) -> None:
    """Read adopter guidance and distinguish its generic budget from local policy."""
    text = _flat((root / rel).read_text(encoding="utf-8"))
    assert _ADOPTER_RETRY_LIMIT in text, (
        f"{rel} lacks the adopter retry limit")
    assert _LOCAL_RETRY_LABEL not in text, (
        f"{rel} carries the Cairn-only retry label")
    assert _LOCAL_RETRY_OVERRIDE not in text, f"{rel} carries the local override"


def test_cairn_local_retry_markers_do_not_enter_adopter_guidance(
        installed: Path, tmp_path: Path) -> None:
    """The shipped and installed generic rule excludes only the local label and override."""
    local = _flat((ROOT / OWN_AGENTS).read_text(encoding="utf-8"))
    assert _LOCAL_RETRY_LABEL in local
    assert _LOCAL_RETRY_OVERRIDE in local

    surfaces = (
        ("shipped", ROOT, SHIPPED_AGENTS),
        ("installed", installed, "AGENTS.md"),
    )
    for surface, source_root, rel in surfaces:
        control_root = tmp_path / f"{surface}-control"
        control_file = _copy_prompt_member(source_root, rel, control_root)
        assert control_file.is_file()
        _assert_adopter_retry_guidance(control_root, rel)

        for marker_name, marker in (
            ("label", _LOCAL_RETRY_LABEL),
            ("override", _LOCAL_RETRY_OVERRIDE),
        ):
            mutant_root = tmp_path / f"{surface}-{marker_name}-mutant"
            mutant_file = _copy_prompt_member(control_root, rel, mutant_root)
            original = mutant_file.read_text(encoding="utf-8")
            assert marker not in original
            mutant_file.write_text(original + "\n\n" + marker + "\n",
                                   encoding="utf-8")
            assert mutant_file.read_text(encoding="utf-8") != original
            with pytest.raises(AssertionError, match=re.escape(marker_name)):
                _assert_adopter_retry_guidance(mutant_root, rel)
