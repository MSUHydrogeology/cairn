# SPDX-License-Identifier: MIT
"""Keep the published writing standard aligned and verify shipped behavior.

Promises:
- The public plain-language page words the five changed numbered rules the same
  as the shipped standard.
- Cairn's own copy of the Cairn Plain Language section matches the shipped copy.
- A real install writes the Cairn Plain Language section as shipped.
- A real install writes the proposal, plan and strategy templates byte for byte
  as shipped.
"""
from pathlib import Path
import re
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[3]

SHIPPED_LOOP = "templates/core/dev/agent_collaboration.md"
OWN_LOOP = "dev/agent_collaboration.md"
PUBLIC_DOC = "docs/plain-language.md"
CHANGED_RULES = (2, 5, 13, 14, 17)


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


def test_cairns_own_copy_says_what_it_ships() -> None:
    """Cairn is bound by the standard it ships, so the two copies must agree."""
    shipped = _section((ROOT / SHIPPED_LOOP).read_text(encoding="utf-8"))
    own = _section((ROOT / OWN_LOOP).read_text(encoding="utf-8"))
    assert _flat(own) == _flat(shipped)


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


@pytest.mark.parametrize("rel,sources", sorted(_INSTALLED_PROMPT_SOURCES.items()))
def test_installed_readable_prompt_and_contrary_mutation(
        installed: Path, rel: str, sources: tuple[str, ...]) -> None:
    """A real install preserves each shipped template at its destination."""
    output = (installed / rel).read_bytes()
    assert output == (ROOT / sources[0]).read_bytes()
