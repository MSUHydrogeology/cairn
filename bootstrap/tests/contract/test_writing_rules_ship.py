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


# These prompts are reading aids carried in the core templates. Each source
# copy and installed control has a positive assertion followed by one isolated
# contrary-wording mutation, so a missing prompt cannot be hidden by another
# copy or by a successful scaffold run.
_READABLE_PROMPTS = {
    "proposal-outputs-and-costs": {
        "sources": ("dev/proposals/_template.md",
                    "templates/core/dev/proposals/_template.md"),
        "installed": "dev/proposals/_template.md",
        "pattern": (r"issue people notice, what change is proposed, the material outputs "
                    r"being added, changed or removed, and their meaningful cost or tradeoff"),
        "anchor": "material outputs being added",
        "replacement": "technical details being considered",
    },
    "proposal-summary-follows-operative-text": {
        "sources": ("dev/proposals/_template.md",
                    "templates/core/dev/proposals/_template.md"),
        "installed": "dev/proposals/_template.md",
        "pattern": r"reading aid, not a second scope contract; correct a mismatch to the operative proposal text",
        "anchor": "not a second scope contract",
        "replacement": "a second scope contract",
    },
    "documentation-only-does-not-invent-a-tool": {
        "sources": ("dev/proposals/_template.md",
                    "templates/core/dev/proposals/_template.md"),
        "installed": "dev/proposals/_template.md",
        "pattern": r"a documentation-only change need not invent a tool",
        "anchor": "need not invent a tool",
        "replacement": "must invent a tool",
    },
    "proposal-trimming-preserves-explanation": {
        "sources": ("dev/proposals/_template.md",
                    "templates/core/dev/proposals/_template.md"),
        "installed": "dev/proposals/_template.md",
        "pattern": (r"cut repeatable detail available elsewhere before cutting explanation; "
                    r"shorten the Decision summary last"),
        "anchor": "cutting explanation",
        "replacement": "keeping explanation",
    },
    "proposal-modest-clarity-overrun": {
        "sources": ("dev/proposals/_template.md",
                    "templates/core/dev/proposals/_template.md"),
        "installed": "dev/proposals/_template.md",
        "pattern": r"modest clarity-preserving overrun is preferable to obscurity",
        "anchor": "preferable to obscurity",
        "replacement": "worse than obscurity",
    },
    "plan-build-summary": {
        "sources": ("dev/plans/_template.md",
                    "templates/core/dev/plans/_template.md"),
        "installed": "dev/plans/_template.md",
        "pattern": (r"## Build summary.{0,80}accepted result and the material outputs this plan "
                    r"will produce or change.{0,100}Do not repeat the technical inventory in Scope"),
        "anchor": "accepted result and the material outputs",
        "replacement": "unaccepted possibilities without outputs",
    },
    "plan-copy-includes-build-summary": {
        "sources": ("dev/plans/_template.md",
                    "templates/core/dev/plans/_template.md"),
        "installed": "dev/plans/_template.md",
        "pattern": r"operative headings \(`## Build summary` through `## Verification`\)",
        "anchor": "operative headings (`## Build summary` through `## Verification`)",
        "replacement": "operative headings (`## Source proposal` through `## Verification`)",
    },
    "plan-summary-corrects-to-accepted-scope": {
        "sources": ("dev/plans/_template.md",
                    "templates/core/dev/plans/_template.md"),
        "installed": "dev/plans/_template.md",
        "pattern": r"if it conflicts with operative Scope, correct the summary to match the accepted work",
        "anchor": "correct the summary to match",
        "replacement": "treat the summary as a new decision and",
    },
    "plan-trimming-preserves-explanation": {
        "sources": ("dev/plans/_template.md",
                    "templates/core/dev/plans/_template.md"),
        "installed": "dev/plans/_template.md",
        "pattern": r"cut repeatable detail before explanation and shorten the Build summary last",
        "anchor": "before explanation",
        "replacement": "after explanation",
    },
    "plan-modest-clarity-overrun": {
        "sources": ("dev/plans/_template.md",
                    "templates/core/dev/plans/_template.md"),
        "installed": "dev/plans/_template.md",
        "pattern": r"modest clarity-preserving overrun is preferable to obscure compression",
        "anchor": "preferable to obscure compression",
        "replacement": "worse than obscure compression",
    },
    "strategy-summary-question-recommendation-outputs": {
        "sources": ("dev/strategy/_template.md",
                    "templates/core/dev/strategy/_template.md"),
        "installed": "dev/strategy/_template.md",
        "pattern": (r"## Summary.{0,60}state the question, the current conclusion or "
                    r"recommendation, and the material outputs this exploration could lead to"),
        "anchor": "the question, the current conclusion",
        "replacement": "only the final decision,",
    },
    "strategy-summary-stays-exploratory": {
        "sources": ("dev/strategy/_template.md",
                    "templates/core/dev/strategy/_template.md"),
        "installed": "dev/strategy/_template.md",
        "pattern": r"Keep unsettled choices visibly exploratory; this summary does not accept work",
        "anchor": "this summary does not accept work",
        "replacement": "this summary accepts work",
    },
}


def _mutate_prompt(text: str, anchor: str, replacement: str) -> str:
    flat = _flat(text)
    assert anchor in flat, f"mutation anchor {anchor!r} is stale"
    return flat.replace(anchor, replacement, 1)


def _copy_prompt_member(source_root: Path, rel: str, target_root: Path) -> Path:
    """Copy one named prompt member into an isolated physical test root."""
    source = source_root / rel
    target = target_root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    return target


def _assert_readable_prompt(root: Path, rel: str, label: str) -> None:
    """The same file-reading assertion is used for source and mutant copies."""
    spec = _READABLE_PROMPTS[label]
    text = _flat((root / rel).read_text(encoding="utf-8"))
    assert re.search(spec["pattern"], text, re.I), f"{rel} lacks {label}"


_READABLE_SOURCE_CASES = [
    (label, source)
    for label, spec in _READABLE_PROMPTS.items()
    for source in spec["sources"]
]


@pytest.mark.parametrize("label,source", _READABLE_SOURCE_CASES,
                         ids=[f"{label}-{source.split('/')[0]}" for label, source in _READABLE_SOURCE_CASES])
def test_source_readable_prompt_and_contrary_mutation(
        label: str, source: str, tmp_path: Path) -> None:
    # Each source member gets an untouched physical control and a separate
    # physical mutant. The assertion reads the named file from each root.
    spec = _READABLE_PROMPTS[label]
    control_root = tmp_path / "control"
    control_file = _copy_prompt_member(ROOT, source, control_root)
    assert control_file.is_file()
    _assert_readable_prompt(control_root, source, label)

    mutant_root = tmp_path / "mutant"
    mutant_file = _copy_prompt_member(control_root, source, mutant_root)
    mutant_file.write_text(
        _mutate_prompt(mutant_file.read_text(encoding="utf-8"),
                       spec["anchor"], spec["replacement"]),
        encoding="utf-8",
    )
    assert mutant_file.read_text(encoding="utf-8") != control_file.read_text(
        encoding="utf-8")
    with pytest.raises(AssertionError, match=rf"{re.escape(source)} lacks {re.escape(label)}"):
        _assert_readable_prompt(mutant_root, source, label)


@pytest.mark.parametrize("label", sorted(_READABLE_PROMPTS))
def test_installed_readable_prompt_and_contrary_mutation(
        installed: Path, label: str, tmp_path: Path) -> None:
    spec = _READABLE_PROMPTS[label]
    rel = spec["installed"]
    control_root = tmp_path / "control"
    control_file = _copy_prompt_member(installed, rel, control_root)
    assert control_file.is_file()
    _assert_readable_prompt(control_root, rel, label)

    mutant_root = tmp_path / "mutant"
    mutant_file = _copy_prompt_member(control_root, rel, mutant_root)
    mutant_file.write_text(
        _mutate_prompt(mutant_file.read_text(encoding="utf-8"),
                       spec["anchor"], spec["replacement"]),
        encoding="utf-8",
    )
    assert mutant_file.read_text(encoding="utf-8") != control_file.read_text(
        encoding="utf-8")
    with pytest.raises(AssertionError,
                       match=rf"{re.escape(rel)} lacks {re.escape(label)}"):
        _assert_readable_prompt(mutant_root, rel, label)


def test_cairn_only_retry_budget_does_not_enter_adopter_guidance(
        installed: Path) -> None:
    """The local same-tier allowance stays local while the shared retry rule remains."""
    private_budget = "allow up to two same-tier retries"
    local = _flat((ROOT / OWN_AGENTS).read_text(encoding="utf-8")).lower()
    shipped = _flat((ROOT / SHIPPED_AGENTS).read_text(encoding="utf-8")).lower()
    output = _flat((installed / "AGENTS.md").read_text(encoding="utf-8")).lower()
    assert private_budget in local

    def assert_no_private_budget(text: str) -> None:
        assert private_budget not in text

    assert_no_private_budget(shipped)
    assert_no_private_budget(output)
    with pytest.raises(AssertionError):
        assert_no_private_budget(shipped + ". " + private_budget + ".")
