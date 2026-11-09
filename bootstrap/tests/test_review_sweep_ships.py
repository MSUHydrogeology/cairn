"""Every install receives a nine-lens reading aid, not only module teams.

The nine lenses as a reading aid, evidence and coverage rules, and concise falsification evidence
a clean code review must show used to live only in the `dual-review` module,
which installs for teams with two agent types. A solo team, and any team that did
not select the module, was asked for a coverage line it had never been shown.

They now sit in the review-loop document (`dev/agent_collaboration.md`), which
every install receives, under the heading "The review sweep" and ahead of the
scope-reduction trap that mirrors it. `AGENTS.md` carries a short pointer.

What is pinned, and why:

* **Through a real install, for every shipped profile.** The files an agent
  actually reads are the installed ones, so the check runs the scaffold CLI for
  each profile and reads what it wrote. A test that read only the template would
  stay green if an install path dropped or substituted the section.
* **The same obligations over both source copies.** The shipped file and Cairn's
  own copy must agree, so Cairn is bound by what it ships.
* **Nine lenses, in the doctrine's order, and no tenth.** A follower adds a
  sentence to one lens by its label, so the label and the count are an interface.
* **Evidence belongs in the review loop, not a second module.** The module
  supplies staffing guidance; repeatable probes stay in tests or scripts.
* **No reasoning from the doctrine leaks in.** The staged evidence bar, the
  going-through-the-motions signal and the do-not-telegraph rule are doctrine's
  reasoning; installed text states the rule, not the argument for it.
* **Body text, not a slot.** A slot is frozen at its first fill and never
  updates, so the roster would stop receiving upgrades.

Each obligation is an alternation matched against text with emphasis and code
markers removed and whitespace collapsed, so a rewording that keeps the
obligation passes and a deletion fails. Node IDs are the obligation labels,
never the patterns. Patterns are literals, not derived from the files they
check. A deliberate break (delete a lens, a coverage half, the scope sentence) is
made beside an unmutated control that must be green, and must turn a named check
red.

Run from the Cairn repo root:
    python -m pytest bootstrap/tests/test_review_sweep_ships.py
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
SCAFFOLD = CAIRN_ROOT / "bootstrap" / "scaffold.py"
PROFILES = sorted((CAIRN_ROOT / "bootstrap" / "profiles").glob("*.yml"))

SHIPPED_LOOP = "templates/core/dev/agent_collaboration.md"
OWN_LOOP = "dev/agent_collaboration.md"
SHIPPED_AGENTS = "templates/core/AGENTS.md"
OWN_AGENTS = "AGENTS.md"
_LOOP_FILES = (SHIPPED_LOOP, OWN_LOOP)
_AGENTS_FILES = (SHIPPED_AGENTS, OWN_AGENTS)
_FILE_IDS = {
    SHIPPED_LOOP: "shipped-loop", OWN_LOOP: "own-loop",
    SHIPPED_AGENTS: "shipped-agents", OWN_AGENTS: "own-agents",
}

_TRAP_OPENING = "The clean pass has a mirror: the scope-reduction trap"

#: The pointer paragraph runs from its bold lead to the next blank line.
_POINTER_LEAD = "**Every review shows its evidence.**"

_READABLE_WORK_RULES = {
    "AGENTS.md": {
        "finish-records-at-commit": (
            r"At the commit or archive that finishes work, update applicable roadmap and changelog records",
            "At the commit or archive that finishes work"),
        "session-end-checks-omissions": (
            r"Do not defer those entries to session end; the session-end routine checks for omissions",
            "Do not defer those entries to session end"),
        "assigned-tier-chunks-are-specified": (
            r"Plan review checks whether each chunk is specified for its assigned model tier without asking the implementer to make design decisions",
            "Plan review checks whether each chunk is specified"),
        "plan-review-returns-missing-design": (
            r"Name missing design in the existing three answers and return the chunk to its author for repair",
            "Name missing design in the existing three answers"),
        "cheap-follow-up-definition": (
            r"cheap follow-ups mean a few person-steps, no new Decision or public name beyond the plan, and a test in existing test files",
            "cheap follow-ups mean a few person-steps"),
        "cheap-follow-ups-fixed-or-authorized-deferral": (
            r"Code review identifies cheap findings and advice; before archive the response fixes each or uses an existing deferral reason with the Maintainer's verbatim authorization",
            "Code review identifies cheap findings and advice"),
        "cheapness-does-not-waive-checks": (
            r"Cheapness grants no scope, boundary or check waiver",
            "Cheapness grants no scope"),
        "non-cheap-advice-keeps-disposition": (
            r"Non-cheap advice keeps its existing disposition",
            "Non-cheap advice keeps its existing disposition"),
        "failed-required-check-stays-implementation-work": (
            r"Required failed checks remain implementation work",
            "Required failed checks remain implementation work"),
    },
    "templates/core/AGENTS.md": {
        "finish-records-at-commit": (
            r"At the commit or archive that finishes work, update applicable roadmap and changelog records",
            "At the commit or archive that finishes work"),
        "session-end-checks-omissions": (
            r"Do not defer those entries to session end; the session-end routine checks for omissions",
            "Do not defer those entries to session end"),
        "assigned-tier-chunks-are-specified": (
            r"Plan review checks whether each chunk is specified for its assigned model tier without asking the implementer to make design decisions",
            "Plan review checks whether each chunk is specified"),
        "plan-review-returns-missing-design": (
            r"Name missing design in the existing three answers and return the chunk to its author for repair",
            "Name missing design in the existing three answers"),
        "cheap-follow-up-definition": (
            r"cheap follow-ups mean a few person-steps, no new Decision or public name beyond the plan, and a test in existing test files",
            "cheap follow-ups mean a few person-steps"),
        "cheap-follow-ups-fixed-or-authorized-deferral": (
            r"Code review identifies cheap findings and advice; before archive the response fixes each or uses an existing deferral reason with the Maintainer's verbatim authorization",
            "Code review identifies cheap findings and advice"),
        "cheapness-does-not-waive-checks": (
            r"Cheapness grants no scope, boundary or check waiver",
            "Cheapness grants no scope"),
        "non-cheap-advice-keeps-disposition": (
            r"Non-cheap advice keeps its existing disposition",
            "Non-cheap advice keeps its existing disposition"),
        "failed-required-check-stays-implementation-work": (
            r"Required failed checks remain implementation work",
            "Required failed checks remain implementation work"),
    },
    "dev/agent_collaboration.md": {
        "proposal-cold-read": (
            r"For a proposal, read its title, one-line summary and Decision summary before the body or code",
            "For a proposal, read its title"),
        "proposal-gist-and-finding": (
            r"State the gist in one or two sentences; if understanding the top depends on the body, name that as a finding",
            "State the gist in one or two sentences"),
        "proposal-author-rereads-top": (
            r"After every proposal revision, the author rereads the top and revises it as a whole",
            "After every proposal revision"),
        "assigned-tier-chunks-are-specified": (
            r"Plan reviews use the same three questions to check whether every chunk can be executed at its assigned tier without implementer design decisions",
            "Plan reviews use the same three questions"),
        "plan-review-returns-missing-design": (
            r"Identify missing specification in the review and return it to the plan author",
            "Identify missing specification in the review"),
        "reviewer-disposes-non-cheap-advice": (
            r"Authors dispose of non-cheap advice in one line each",
            "Authors dispose of non-cheap advice"),
    },
    "templates/core/dev/agent_collaboration.md": {
        "proposal-cold-read": (
            r"For a proposal, read its title, one-line summary and Decision summary before the body or code",
            "For a proposal, read its title"),
        "proposal-gist-and-finding": (
            r"State the gist in one or two sentences; if understanding the top depends on the body, name that as a finding",
            "State the gist in one or two sentences"),
        "proposal-author-rereads-top": (
            r"After every proposal revision, the author rereads the top and revises it as a whole",
            "After every proposal revision"),
        "assigned-tier-chunks-are-specified": (
            r"Plan reviews use the same three questions to check whether every chunk can be executed at its assigned tier without implementer design decisions",
            "Plan reviews use the same three questions"),
        "plan-review-returns-missing-design": (
            r"Identify missing specification in the review and return it to the plan author",
            "Identify missing specification in the review"),
        "reviewer-disposes-non-cheap-advice": (
            r"Authors dispose of non-cheap advice in one line each",
            "Authors dispose of non-cheap advice"),
    },
    "dev/plans/_template.md": {
        "cheap-follow-up-definition": (
            r"Cheap follow-ups mean a few person-steps, no new Decision or public name beyond the plan, and a test that fits existing test files",
            "Cheap follow-ups mean a few person-steps"),
        "cheap-defect-exception-stays-narrow": (
            r"This is not the narrower cheap defect-fix exception in AGENTS.md",
            "not the narrower cheap defect-fix exception"),
        "cheap-follow-ups-fixed-or-authorized-deferral": (
            r"Code review identifies cheap findings and advice; in the code-review response, fix each before archive or use an existing deferral reason with the Maintainer's verbatim authorization",
            "Code review identifies cheap findings and advice"),
        "cheapness-does-not-waive-checks": (
            r"Cheapness grants no scope, boundary or required-check waiver",
            "Cheapness grants no scope"),
        "non-cheap-advice-keeps-disposition": (
            r"Non-cheap advice keeps its existing disposition",
            "Non-cheap advice keeps its existing disposition"),
        "failed-required-check-stays-implementation-work": (
            r"a required failed check remains implementation work",
            "a required failed check remains implementation work"),
    },
    "templates/core/dev/plans/_template.md": {
        "cheap-follow-up-definition": (
            r"Cheap follow-ups mean a few person-steps, no new Decision or public name beyond the plan, and a test that fits existing test files",
            "Cheap follow-ups mean a few person-steps"),
        "cheap-defect-exception-stays-narrow": (
            r"This is not the narrower cheap defect-fix exception in AGENTS.md",
            "not the narrower cheap defect-fix exception"),
        "cheap-follow-ups-fixed-or-authorized-deferral": (
            r"Code review identifies cheap findings and advice; in the code-review response, fix each before archive or use an existing deferral reason with the Maintainer's verbatim authorization",
            "Code review identifies cheap findings and advice"),
        "cheapness-does-not-waive-checks": (
            r"Cheapness grants no scope, boundary or required-check waiver",
            "Cheapness grants no scope"),
        "non-cheap-advice-keeps-disposition": (
            r"Non-cheap advice keeps its existing disposition",
            "Non-cheap advice keeps its existing disposition"),
        "failed-required-check-stays-implementation-work": (
            r"a required failed check remains implementation work",
            "a required failed check remains implementation work"),
    },
    "docs/methodology/proposals.md": {
        "proposal-cold-read": (
            r"Before the body or code, the reviewer reads the title, one-line summary and Decision summary",
            "Before the body or code"),
        "proposal-gist-and-finding": (
            r"then states the gist in one or two sentences. If the body is needed to understand the top, name that dependence as a finding",
            "then states the gist in one or two sentences"),
        "proposal-author-rereads-top": (
            r"After each revision, the author rereads the top and revises it as a whole",
            "After each revision"),
    },
    "docs/methodology/plans.md": {
        "assigned-tier-chunks-are-specified": (
            r"check that each chunk has enough design for its assigned model tier to execute without the implementer making design decisions",
            "check that each chunk has enough design"),
        "plan-review-returns-missing-design": (
            r"Name any missing specification and return the chunk to its author",
            "Name any missing specification"),
        "cheap-follow-up-definition": (
            r"A cheap follow-up is a few person-steps, needs no new Decision or public name beyond the plan, and has a test that fits existing test files",
            "A cheap follow-up is a few person-steps"),
        "cheap-follow-ups-fixed-or-authorized-deferral": (
            r"the author fixes each in the response before archive or uses an existing deferral reason with the Maintainer's verbatim authorization",
            "the author fixes each in the response"),
        "cheapness-does-not-waive-checks": (
            r"Cheapness grants no scope, boundary or required-check waiver",
            "Cheapness grants no scope"),
        "non-cheap-advice-keeps-disposition": (
            r"Non-cheap advice retains its existing disposition",
            "Non-cheap advice retains its existing disposition"),
        "failed-required-check-stays-implementation-work": (
            r"Required failed checks remain implementation work",
            "Required failed checks remain implementation work"),
    },
    "docs/methodology/session-routines.md": {
        "finish-records-at-commit": (
            r"Applicable roadmap and changelog entries belong at the commit or archive that finishes work",
            "Applicable roadmap and changelog entries belong"),
        "session-end-checks-omissions": (
            r"The session-end routine checks for omissions; it is not the normal time to rebuild entries due earlier",
            "The session-end routine checks for omissions"),
    },
    "templates/skills/session-end/SKILL.md": {
        "finish-records-at-commit": (
            r"Check that applicable roadmap and changelog entries were made at the commit or archive that finished the work",
            "Check that applicable roadmap and changelog entries"),
        "session-end-checks-omissions": (
            r"Session end checks for omissions; it is not the normal time to reconstruct entries that were due earlier",
            "Session end checks for omissions"),
    },
    ".agents/skills/session-end/SKILL.md": {
        "finish-records-at-commit": (
            r"Check that applicable roadmap and changelog entries were made at the commit or archive that finished the work",
            "Check that applicable roadmap and changelog entries"),
        "session-end-checks-omissions": (
            r"Session end checks for omissions; it is not the normal time to reconstruct entries that were due earlier",
            "Session end checks for omissions"),
    },
}

_INSTALLED_SMART_GOALS = {
    "AGENTS.md": "templates/core/AGENTS.md",
    "dev/proposals/_template.md": "templates/core/dev/proposals/_template.md",
    "dev/plans/_template.md": "templates/core/dev/plans/_template.md",
}

_INSTALLED_PLAN_COMPLETION = {
    "AGENTS.md": "AGENTS.md",
    "dev/plans/_template.md": "dev/plans/_template.md",
    "dev/PLANNING.md": "dev/PLANNING.md",
}

_INSTALLED_PLAN_COMPLETION_SOURCES = {
    "AGENTS.md": "templates/core/AGENTS.md",
    "dev/plans/_template.md": "templates/core/dev/plans/_template.md",
    "dev/PLANNING.md": "templates/core/dev/PLANNING.md",
}


def _section_between(text: str, start: str, end: str) -> str:
    """Select one complete source/output section by its neighboring headings."""
    first = text.index(start)
    last = text.index(end, first + len(start))
    return text[first:last]


def _source_output_projection(surface: str, text: str) -> str:
    """Select the delivered source region unaffected by install-time slots."""
    if surface == "AGENTS.md":
        return _section_between(text, "## Lifecycle and records", "## Review")
    if surface == "dev/PLANNING.md":
        return _section_between(text, "## Working rules (for agents)",
                                "## Archive preconditions")
    return text


def _missing_completion(text: str, patterns: dict[str, str]) -> list[str]:
    normalized = _normalize(text)
    return [label for label, pattern in patterns.items()
            if not re.search(pattern, normalized, re.I)]


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
@pytest.mark.parametrize("surface", sorted(_INSTALLED_SMART_GOALS))
def test_installed_smart_goal_guidance(
        installs: dict[str, Path], profile: Path, surface: str) -> None:
    roots = json.loads(os.environ.get("CAIRN_SMART_INSTALLED_ROOTS", "{}"))
    key = f"{profile.stem}::{surface}"
    root = Path(roots[key]) if key in roots else installs[profile.stem]
    source = _INSTALLED_SMART_GOALS[surface]
    installed_text = (root / surface).read_text(encoding="utf-8")
    source_text = (CAIRN_ROOT / source).read_text(encoding="utf-8")
    assert _source_output_projection(surface, installed_text) == \
        _source_output_projection(surface, source_text), (
            f"{profile.stem} installed {surface} differs from {source}")


def test_installed_smart_goal_mutations_fail_entrypoint(
        installs: dict[str, Path], tmp_path: Path) -> None:
    roots: dict[str, str] = {}
    expected = len(PROFILES) * len(_INSTALLED_SMART_GOALS)
    for profile in PROFILES:
        for surface in _INSTALLED_SMART_GOALS:
            original_root = installs[profile.stem]
            clone_root = tmp_path / f"{profile.stem}-{surface.replace('/', '-') }"
            shutil.copytree(original_root, clone_root)
            target = clone_root / surface
            text = target.read_text(encoding="utf-8")
            projection = _source_output_projection(surface, text)
            assert projection and text.count(projection) == 1
            mutant = text.replace(
                projection,
                projection + "\n<!-- isolated installed-output mutation -->\n",
                1,
            )
            target.write_text(mutant, encoding="utf-8")
            roots[f"{profile.stem}::{surface}"] = str(clone_root)

    env = os.environ.copy()
    env["CAIRN_SMART_INSTALLED_ROOTS"] = json.dumps(roots)
    result = subprocess.run(
        [sys.executable, "-m", "pytest",
         f"{Path(__file__)}::test_installed_smart_goal_guidance", "-q"],
        cwd=CAIRN_ROOT, env=env, capture_output=True, text=True, check=False,
        stdin=subprocess.DEVNULL)
    assert result.returncode != 0, "installed surface mutations survived"
    assert f"{expected} failed" in result.stdout, (
        "not every independently mutated installed surface failed its owning "
        f"entry point:\n{result.stdout}\n{result.stderr}")


def _normalize(text: str) -> str:
    """Drop blockquote, emphasis and code markers; collapse whitespace."""
    text = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    text = text.replace("*", "").replace("`", "")
    return " ".join(text.split())

def _text(rel: str) -> str:
    roots = json.loads(os.environ.get("CAIRN_SMART_SOURCE_ROOTS", "{}"))
    return (Path(roots.get(rel, CAIRN_ROOT)) / rel).read_text(encoding="utf-8")


def _sweep(text: str) -> str:
    """The raw text of the sweep: its heading to the scope-reduction trap."""
    start = re.search(r"^## The review sweep$", text, re.M)
    assert start, "no '## The review sweep' heading"
    end = text.find(f"**{_TRAP_OPENING}", start.end())
    assert end != -1, "the scope-reduction trap does not follow the sweep"
    return text[start.start():end]


def _pointer(text: str) -> str:
    """The pointer paragraph in the Review section of an `AGENTS.md`."""
    section = re.search(r"^## Review$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert section, "no '## Review' section"
    body = section.group(1)
    lead = body.find(_POINTER_LEAD)
    assert lead != -1, "no pointer paragraph in Review"
    return body[lead:].split("\n\n", 1)[0]


def _missing(text: str, obligations: dict[str, str]) -> list[str]:
    normalized = _normalize(text)
    return [label for label, pattern in obligations.items()
            if not re.search(pattern, normalized)]


def _delete_sentence(text: str, anchor: str) -> str:
    """Delete the sentence containing the literal *anchor* (not a pattern)."""
    flat = " ".join(text.split())
    at = flat.find(anchor)
    assert at != -1, f"anchor {anchor!r} not found; the control is stale"
    start = max(flat.rfind(". ", 0, at) + 2, 0)
    end = flat.find(". ", at)
    end = len(flat) if end == -1 else end + 2
    return flat[:start] + flat[end:]


_READABLE_WORK_CASES = [
    (rel, label)
    for rel, obligations in _READABLE_WORK_RULES.items()
    for label in obligations
]


def _assert_readable_work_obligation(root: Path, rel: str, label: str) -> None:
    pattern, _ = _READABLE_WORK_RULES[rel][label]
    text = (root / rel).read_text(encoding="utf-8")
    missing = _missing_completion(text, {label: pattern})
    assert not missing, f"{root / rel} lost {label}: {missing}"


_INSTALLED_READABLE_WORK_SURFACES = {
    "AGENTS.md": "templates/core/AGENTS.md",
    "dev/agent_collaboration.md": "templates/core/dev/agent_collaboration.md",
    ".agents/skills/session-end/SKILL.md": "templates/skills/session-end/SKILL.md",
}
@pytest.mark.parametrize("dest,source", _INSTALLED_READABLE_WORK_SURFACES.items(),
                         ids=[f"{dest}-source-parity"
                              for dest in _INSTALLED_READABLE_WORK_SURFACES])
@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
def test_installed_readable_work_matches_source(
        installs: dict[str, Path], profile: Path, dest: str,
        source: str) -> None:
    """Each profile install carries the corresponding source guidance."""
    installed_root = installs[profile.stem]
    installed_text = (installed_root / dest).read_text(encoding="utf-8")
    source_text = (CAIRN_ROOT / source).read_text(encoding="utf-8")
    assert _source_output_projection(dest, installed_text) == \
        _source_output_projection(dest, source_text), (
            f"{profile.stem} installed {dest} differs from {source}")


def _replace_sentence(text: str, anchor: str, replacement: str) -> str:
    flat = " ".join(text.split())
    at = flat.find(anchor)
    assert at != -1, f"anchor {anchor!r} not found; the control is stale"
    start = max(flat.rfind(". ", 0, at) + 2, 0)
    end = flat.find(". ", at)
    end = len(flat) if end == -1 else end + 2
    return flat[:start] + replacement + " " + flat[end:]


# --------------------------------------------------------------------------
# The two source copies of the review-loop document.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_sweep_is_body_text_not_a_slot(rel: str) -> None:
    """A slot is frozen at its first fill, so the roster would stop updating."""
    assert "cairn:" not in _sweep(_text(rel))


# --------------------------------------------------------------------------
# The pointer in both AGENTS.md copies.
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Through a real install, for every shipped profile.
# --------------------------------------------------------------------------

@pytest.fixture(scope="session")
def installs(tmp_path_factory) -> dict[str, Path]:
    """Install each shipped profile once; return profile stem -> target tree.

    The profiles are globbed, so one added later is installed and checked
    without editing this file; the three that ship today must be among them,
    or a broken glob would pass by checking nothing.
    """
    if os.environ.get("CAIRN_SMART_INSTALLED_ROOTS"):
        return {}
    assert {"solo-greenfield", "collaborative-team",
            "high-rigor-legacy"} <= {p.stem for p in PROFILES}
    out: dict[str, Path] = {}
    for profile in PROFILES:
        target = tmp_path_factory.mktemp(f"install-{profile.stem}")
        result = subprocess.run(
            [sys.executable, str(SCAFFOLD), "--config", str(profile),
             "--target", str(target)],
            capture_output=True, text=True, check=False,
            stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0, (
            f"installing {profile.name} exited {result.returncode}:\n"
            f"{result.stderr}")
        out[profile.stem] = target
    return out


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
def test_installed_loop_document_carries_the_obligation(
        installs: dict[str, Path], profile: Path) -> None:
    """Every profile receives the source review-loop document unchanged."""
    installed = installs[profile.stem] / "dev/agent_collaboration.md"
    source = (CAIRN_ROOT / SHIPPED_LOOP).read_text(encoding="utf-8")
    assert _sweep(installed.read_text(encoding="utf-8")) == _sweep(source), profile.stem


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
def test_installed_agents_md_carries_the_pointer(
        installs: dict[str, Path], profile: Path) -> None:
    """Every profile receives the source review pointer unchanged."""
    installed = (installs[profile.stem] / "AGENTS.md").read_text(encoding="utf-8")
    source = (CAIRN_ROOT / SHIPPED_AGENTS).read_text(encoding="utf-8")
    assert _pointer(installed) == _pointer(source), profile.stem


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
@pytest.mark.parametrize("surface", sorted(_INSTALLED_PLAN_COMPLETION))
def test_installed_plan_completion_and_surface_mutation(
        installs: dict[str, Path], profile: Path, surface: str) -> None:
    root = installs[profile.stem]
    output = root / _INSTALLED_PLAN_COMPLETION[surface]
    source = _INSTALLED_PLAN_COMPLETION_SOURCES[surface]
    installed_text = output.read_text(encoding="utf-8")
    source_text = (CAIRN_ROOT / source).read_text(encoding="utf-8")
    assert _source_output_projection(surface, installed_text) == \
        _source_output_projection(surface, source_text), (
        f"{profile.stem} installed {surface} differs from {source}")


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
def test_an_install_without_the_sweep_is_reported(
        installs: dict[str, Path], profile: Path) -> None:
    """A dropped installed sweep is detected by source/output comparison."""
    installed = installs[profile.stem] / "dev" / "agent_collaboration.md"
    source = (CAIRN_ROOT / SHIPPED_LOOP).read_text(encoding="utf-8")
    actual = installed.read_text(encoding="utf-8")
    expected = _sweep(source)
    assert _sweep(actual) == expected, f"the unmutated {profile.stem} install differs"
    gutted = actual.replace(expected, "## The review sweep\n\n", 1)
    assert _sweep(gutted) != expected, "a missing installed sweep matched its source"


# --------------------------------------------------------------------------
# Mutants: delete one thing from a copy and a named check must go red, beside
# an unmutated control that is green.
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# A fresh install must not leave a one-word `{{placeholder}}` the engine does
# not recognise: the next upgrade would plan the file as needing a value.
# --------------------------------------------------------------------------

def _installed_text_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*")
                  if p.is_file() and p.suffix in {".md", ".yml", ".txt"}
                  and ".git" not in p.parts)


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
def test_an_install_leaves_no_placeholder_the_engine_cannot_fill(
        installs: dict[str, Path], profile: Path) -> None:
    sys.path.insert(0, str(CAIRN_ROOT))
    from bootstrap._scaffold.config import KNOWN_TOKENS
    from bootstrap._scaffold.slotmerge import find_unfilled_tokens
    root = installs[profile.stem]
    files = _installed_text_files(root)
    assert any(f.name == "agent_collaboration.md" for f in files), (
        "control: the installed tree was read")
    bad = {}
    for path in files:
        left = set(find_unfilled_tokens(path.read_text(encoding="utf-8",
                                                       errors="replace")))
        left -= set(KNOWN_TOKENS)
        if left:
            bad[path.relative_to(root).as_posix()] = sorted(left)
    assert not bad, (
        f"a {profile.stem} install carries one-word placeholders the engine "
        f"cannot fill: {bad}. An upgrade plans each such file as needing a "
        f"value and never advances it.")


# --------------------------------------------------------------------------
# The lens text exists once. The dual-review module supplies staffing guidance
# for a called read and does not duplicate review-loop instructions. A second copy of the
# roster in the module is how two definitions drift apart, and a team that
# selected the module would merge both into its loop document.
# --------------------------------------------------------------------------

SHIPPED_MODULE = "templates/modules/team-gated/dual-review.md"
OWN_MODULE = "dev/modules/dual-review.md"

#: label -> pattern for the text only the review-loop document may carry.
