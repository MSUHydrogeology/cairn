# SPDX-License-Identifier: MIT
"""Model-tier mappings and real installs preserve source-to-output behavior."""
from pathlib import Path
import re
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]

SHIPPED_AGENTS = "templates/core/AGENTS.md"
OWN_AGENTS = "AGENTS.md"
SHIPPED_MODULE = "templates/modules/team-gated/model-selection.md"
OWN_MODULE = "dev/modules/model-selection.md"

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

def _model_tier_rule(text: str) -> str:
    """Return only the complete Model tier paragraph under `## Roles`."""
    roles = _roles_section(text)
    match = re.search(
        r"(?ms)^\*\*Model tier\.\*\*.*?(?=\n[ \t]*\n|\Z)", roles
    )
    assert match, "no Model tier paragraph under '## Roles'"
    return _flat(match.group())

def _retry_paragraph_span(text: str) -> tuple[int, int]:
    """Locate the shipped retry paragraph, ending at its next blank line."""
    start = text.index("**Execution retries.**")
    end = text.find("\n\n", start)
    return start, len(text) if end == -1 else end

def _retry_paragraph(text: str) -> str:
    start, end = _retry_paragraph_span(text)
    return _flat(text[start:end])

def _remove_retry_clause(text: str) -> str:
    """Remove the retry limit from an isolated source copy."""
    start, end = _retry_paragraph_span(text)
    paragraph = text[start:end]
    anchor = "allow up to two same-tier retries after the initial failed attempt"
    pattern = re.compile(r"\s+".join(re.escape(part) for part in anchor.split()))
    matches = list(pattern.finditer(paragraph))
    assert len(matches) == 1, len(matches)
    match = matches[0]
    mutated_paragraph = paragraph[:match.start()] + paragraph[match.end():]
    mutated = text[:start] + mutated_paragraph + text[end:]
    assert mutated != text
    return mutated

def test_the_rule_reads_the_same_in_both_copies() -> None:
    """Cairn's own instruction copy matches the shipped core rule."""
    def rule(rel: str) -> str:
        return _model_tier_rule(_read(rel))
    assert rule(OWN_AGENTS) == rule(SHIPPED_AGENTS)

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

@pytest.fixture(scope="module")
def collaborative_install(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A real install of the collaborative profile with model-selection enabled."""
    target = tmp_path_factory.mktemp("model-tier-collaborative") / "project"
    target.mkdir()
    result = subprocess.run(
        [sys.executable, str(ROOT / "bootstrap/scaffold.py"),
         "--config", str(ROOT / "bootstrap/profiles/collaborative-team.yml"),
         "--target", str(target), "--cairn-root", str(ROOT), "--allow-dev"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return target

def test_a_profile_with_no_module_still_installs_the_rule(solo_install: Path) -> None:
    """The solo install carries its source rule and omits the optional module."""
    assert not (solo_install / "dev/modules/model-selection.md").exists()
    source = _model_tier_rule(_read(SHIPPED_AGENTS))
    installed = _model_tier_rule((solo_install / "AGENTS.md").read_text(encoding="utf-8"))
    assert installed == source

def test_collaborative_profile_installs_rule_and_module_copy(
        collaborative_install: Path) -> None:
    """The collaborative install carries its source rule and optional module."""
    installed_path = collaborative_install / "AGENTS.md"
    installed = installed_path.read_text(encoding="utf-8")
    assert _model_tier_rule(installed) == _model_tier_rule(_read(SHIPPED_AGENTS))

    module_path = collaborative_install / "dev/modules/model-selection.md"
    assert module_path.is_file()
    assert module_path.read_bytes() == (ROOT / SHIPPED_MODULE).read_bytes()

def _clone_cairn_root(destination: Path) -> Path:
    """Create a physical copy of the committed tree with its own Git admin."""
    status = subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "status", "--porcelain"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert status.returncode == 0, status.stdout + status.stderr
    assert not status.stdout.strip(), "mutation source tree must be clean"
    result = subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "clone", "--no-hardlinks",
         "--quiet", str(ROOT), str(destination)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    cloned = subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "rev-parse", "HEAD"],
        cwd=destination, capture_output=True, text=True, check=False,
    )
    source = subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "rev-parse", "HEAD"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert cloned.returncode == source.returncode == 0
    assert cloned.stdout.strip() == source.stdout.strip()

    binding = subprocess.run(
        [sys.executable, "-c",
         "from pathlib import Path; from bootstrap._scaffold.install import "
         "write_local_env; print(write_local_env(Path('.')))"],
        cwd=destination, capture_output=True, text=True, check=False,
    )
    assert binding.returncode == 0, binding.stdout + binding.stderr
    assert "'installed'" in binding.stdout, binding.stdout + binding.stderr
    return destination

@pytest.mark.parametrize(
    "profile,profile_path,has_module",
    (("solo", "solo-greenfield.yml", False),
     ("collaborative", "collaborative-team.yml", True)),
)
def test_core_source_retry_limit_mutation_reaches_each_real_install(
        profile: str, profile_path: str, has_module: bool,
        solo_install: Path, collaborative_install: Path,
        tmp_path: Path) -> None:
    """Both profiles install a source-only change to the core rule."""
    control = solo_install if profile == "solo" else collaborative_install
    assert _retry_paragraph((control / "AGENTS.md").read_text(
        encoding="utf-8")) == _retry_paragraph(_read(SHIPPED_AGENTS))
    assert ((control / "dev/modules/model-selection.md").is_file()) is has_module

    cairn_copy = _clone_cairn_root(tmp_path / f"cairn-{profile}")
    shipped_path = cairn_copy / SHIPPED_AGENTS
    original = shipped_path.read_text(encoding="utf-8")
    mutated = _remove_retry_clause(original)
    shipped_path.write_text(mutated, encoding="utf-8")
    changed = subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "diff", "--name-only"],
        cwd=cairn_copy, capture_output=True, text=True, check=False,
    )
    assert changed.returncode == 0, changed.stdout + changed.stderr
    assert changed.stdout.splitlines() == [SHIPPED_AGENTS]

    target = tmp_path / f"{profile}-mutated-project"
    target.mkdir()
    result = subprocess.run(
        [sys.executable, str(cairn_copy / "bootstrap/scaffold.py"),
         "--config", str(cairn_copy / "bootstrap/profiles" / profile_path),
         "--target", str(target), "--cairn-root", str(cairn_copy),
         "--allow-dev"],
        input="", capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert ((target / "dev/modules/model-selection.md").is_file()) is has_module
    assert _retry_paragraph((target / "AGENTS.md").read_text(
        encoding="utf-8")) == _retry_paragraph(
            shipped_path.read_text(encoding="utf-8"))

def test_proposal_authoring_and_ordinary_review_are_medium() -> None:
    """Task floors, rather than lifecycle lanes, determine each assignment."""
    expected = {
        "Strategy / Research": "high",
        "Security judgment / Security Review": "high",
        "Ordinary proposal authoring": "medium",
        "Ordinary proposal review": "medium",
        "Plan review": "medium",
        "Code review": "medium",
        "Accepted-plan execution": "low",
        "Trivial implementation": "low",
        "Authorized Decision scribing": "low",
        "User Agent (routine workflow)": "low",
        "Non-substantive doc tweaks": "low",
        "Docstring and comment cleanup, and related edits": "low",
    }

    def task_floors(text: str) -> dict[str, str]:
        flat = _flat(text)
        start = flat.index("**Default tier-by-task mapping:**")
        end = flat.index("**Docstring and comment cleanup", start)
        table = flat[start:end]
        return dict(re.findall(r"\| ([^|]+) \| (high|medium|low) \|", table))

    expected_fanout = {
        "Single search / retrieval": "low",
        "Single-source extraction / parsing": "low",
        "Mechanical transform / formatting": "low",
        "Authorized Decision scribing": "low",
        "Accepted, reviewed plan execution": "low",
        "Ordinary authoring or review": "medium",
        "Strategy, premise-checking or novel design": "high",
        "Security judgment or Security Review": "high",
    }

    def fanout_floors(text: str) -> dict[str, str]:
        flat = _flat(text)
        start = flat.index("| Task type (fan-out leaf) | Default floor |")
        end = flat.index("**Verification tier follows", start)
        table = flat[start:end]
        return dict(re.findall(r"\| ([^|]+) \| (low|medium|high)(?:[^|]*) \|", table))

    shipped, own = _read(SHIPPED_MODULE), _read(OWN_MODULE)
    assert task_floors(shipped) == expected
    assert task_floors(own) == expected
    assert fanout_floors(shipped) == expected_fanout
    assert fanout_floors(own) == expected_fanout
    assert shipped == own

    # Controls: the former stage-based floors, and low authorized scribing
    # without its authorization condition, each fail the semantic mapping.
    source = _read(OWN_MODULE)
    assert task_floors(source) == expected
    wrong_review = source.replace(
        "| Ordinary proposal review | medium |", "| Ordinary proposal review | high |")
    wrong_execution = source.replace(
        "| Accepted-plan execution | low |", "| Accepted-plan execution | medium |")
    assert task_floors(wrong_review) != expected
    assert task_floors(wrong_execution) != expected
    wrong_security = source.replace(
        "| Security judgment / Security Review | high |",
        "| Security judgment / Security Review | medium |",
    )
    assert task_floors(wrong_security) != expected
    wrong_fanout_execution = source.replace(
        "| Accepted, reviewed plan execution | low, including high-risk chunks |",
        "| Accepted, reviewed plan execution | medium, including high-risk chunks |",
    )
    assert fanout_floors(wrong_fanout_execution) != expected_fanout
