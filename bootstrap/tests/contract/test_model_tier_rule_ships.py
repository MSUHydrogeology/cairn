# SPDX-License-Identifier: MIT
"""The model-tier rule reaches every install, and the cost-rule edits hold.

Four properties, each read from the files an adopter receives:

* every `AGENTS.md` copy carries the same capability floors under `## Roles`,
  apart from Cairn's approved local execution-retry budget, and a profile that
  installs no model-selection module still receives the shipped rule;
* the "different maker" condition is gone from every place that stated it, and
  a model at the same tier as the author is still not a sufficient check;
* task floors control authorship, review, execution and authorized scribing;
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


ROOT = Path(__file__).resolve().parents[3]

SHIPPED_AGENTS = "templates/core/AGENTS.md"
OWN_AGENTS = "AGENTS.md"
ROLES = "docs/methodology/roles.md"
SHIPPED_MODULE = "templates/modules/team-gated/model-selection.md"
OWN_MODULE = "dev/modules/model-selection.md"
AGENTS_COPIES = [SHIPPED_AGENTS, OWN_AGENTS]
MODULE_COPIES = [SHIPPED_MODULE, OWN_MODULE]

_OLD_IMMEDIATE_ESCALATION = (
    "If lower-tier work fails its check, re-run once one tier up."
)
_RETRY_PARAGRAPH_LEADS = {
    "core": "**Execution retries.**",
    "roles": "**Escalation applies to every role, not only the fan-out.**",
}
_RETRY_PARAGRAPHS = {
    "core": (
        "**Execution retries.** For a correctable execution error in work at "
        "or above its capability floor, allow up to two same-tier retries "
        "after the initial failed attempt. Each retry uses concrete failure "
        "feedback, retains earlier failure evidence and reruns only the "
        "affected check during the correction loop. After two failed retries, "
        "re-run once one tier up. Escalate immediately if the failure shows "
        "the task exceeds the assigned tier; work below its capability floor "
        "is not eligible. Retries never replace independent review or Security "
        "Review, waive an accepted criterion or required check, expand "
        "authority, cross a plan fence or data-governance boundary, or change "
        "capability floors. Before repeating a potentially destructive "
        "operation, establish the previous attempt's effects. The correction-"
        "loop limit does not remove final Boundary B or any other required "
        "check. A review finding is not an execution retry."
    ),
    "roles": (
        "**Escalation applies to every role, not only the fan-out.** Work "
        "written below its floor, or a review blocked on a defect that tier "
        "should have caught, is re-run once one tier up; do not retry it at "
        "the same tier. For a correctable execution error in work at or above "
        "its floor, allow up to two same-tier retries after the initial failed "
        "attempt. Each retry uses concrete failure feedback, retains earlier "
        "failure evidence and reruns only the affected check during the "
        "correction loop. After two failed retries, re-run once one tier up. "
        "Escalate immediately if the failure shows the task exceeds the "
        "assigned tier. Retries never replace independent review or Security "
        "Review, waive an accepted criterion or required check, expand "
        "authority, cross a plan fence or data-governance boundary, or change "
        "capability floors. Before repeating a potentially destructive "
        "operation, establish the previous attempt's effects. Final Boundary "
        "B and all other required checks remain due. A review finding is not "
        "an execution retry."
    ),
}
_RETRY_CLAUSES = {
    "core": {
        "correctable-error-at-or-above-floor": (
            "For a correctable execution error in work at or above its capability floor"
        ),
        "two-retries-after-initial-failure": (
            "allow up to two same-tier retries after the initial failed attempt"
        ),
        "concrete-failure-feedback": "Each retry uses concrete failure feedback",
        "retain-earlier-failure-evidence": "retains earlier failure evidence",
        "rerun-only-affected-check": (
            "reruns only the affected check during the correction loop"
        ),
        "escalate-after-two-failures": (
            "After two failed retries, re-run once one tier up"
        ),
        "immediate-capability-mismatch-escalation": (
            "Escalate immediately if the failure shows the task exceeds the assigned tier"
        ),
        "below-floor-exclusion": (
            "work below its capability floor is not eligible"
        ),
        "independent-review-and-security-review": (
            "Retries never replace independent review or Security Review"
        ),
        "accepted-criteria-and-required-checks": (
            "waive an accepted criterion or required check"
        ),
        "authority-is-not-expanded": "expand authority",
        "plan-fence-is-not-crossed": "cross a plan fence",
        "data-governance-boundary-is-not-crossed": (
            "or data-governance boundary"
        ),
        "capability-floors-do-not-change": "change capability floors",
        "inspect-effects-before-repeat": (
            "Before repeating a potentially destructive operation, establish the previous attempt's effects"
        ),
        "final-boundary-b-remains-due": (
            "The correction-loop limit does not remove final Boundary B or any other required check"
        ),
        "review-finding-is-not-retry": (
            "A review finding is not an execution retry"
        ),
    },
    "roles": {
        "below-floor-work-or-review-defect-escalates": (
            "Work written below its floor, or a review blocked on a defect that tier "
            "should have caught, is re-run once one tier up; do not retry it at the same tier"
        ),
        "correctable-error-at-or-above-floor": (
            "For a correctable execution error in work at or above its floor"
        ),
        "two-retries-after-initial-failure": (
            "allow up to two same-tier retries after the initial failed attempt"
        ),
        "concrete-failure-feedback": "Each retry uses concrete failure feedback",
        "retain-earlier-failure-evidence": "retains earlier failure evidence",
        "rerun-only-affected-check": (
            "reruns only the affected check during the correction loop"
        ),
        "escalate-after-two-failures": (
            "After two failed retries, re-run once one tier up"
        ),
        "immediate-capability-mismatch-escalation": (
            "Escalate immediately if the failure shows the task exceeds the assigned tier"
        ),
        "independent-review-and-security-review": (
            "Retries never replace independent review or Security Review"
        ),
        "accepted-criteria-and-required-checks": (
            "waive an accepted criterion or required check"
        ),
        "authority-is-not-expanded": "expand authority",
        "plan-fence-is-not-crossed": "cross a plan fence",
        "data-governance-boundary-is-not-crossed": (
            "or data-governance boundary"
        ),
        "capability-floors-do-not-change": "change capability floors",
        "inspect-effects-before-repeat": (
            "Before repeating a potentially destructive operation, establish the previous attempt's effects"
        ),
        "final-boundary-b-remains-due": (
            "Final Boundary B and all other required checks remain due"
        ),
        "review-finding-is-not-retry": (
            "A review finding is not an execution retry"
        ),
    },
}
_RETRY_CLAUSE_CASES = (
    [("roles", label) for label in sorted(_RETRY_CLAUSES["roles"])]
    + [("solo", label) for label in sorted(_RETRY_CLAUSES["core"])]
    + [("collaborative", label)
       for label in sorted(_RETRY_CLAUSES["core"])]
)

#: label -> a clause the rule must carry. Each clause is matched on text with
#: whitespace collapsed, so a re-wrapped line does not hide it.
_RULE_CLAUSES = {
    "names-the-rule": "**Model tier.**",
    "task-sets-floor-lane-sets-process": (
        "The task sets the capability floor; the lane governs the process, "
        "not the tier."),
    "high-judgment-stays-high": (
        "High covers strategy, premise-checking, novel design, security or "
        "trust-boundary judgment, and Security Review."),
    "ordinary-authoring-and-reviews-are-medium": (
        "Medium covers ordinary proposal authoring and ordinary proposal, "
        "plan and code reviews."),
    "accepted-plan-execution-is-low-even-high-risk": (
        "Low covers execution of an accepted, reviewed plan, including "
        "high-risk chunks, trivial implementation"),
    "decision-scribing-needs-authorization": (
        "Decision scribing explicitly authorized by the Maintainer."),
    "low-execution-keeps-review-security-obligations": (
        "Execution at low does not lower its review or security obligations"),
    "no-downshift-across-data-governance": (
        "Never downshift across a data-governance boundary."),
    "name-the-model-at-every-spawn": "**Name the model at every spawn**",
    "author-and-reviewer-names-carry-the-model": (
        "Author and reviewer names carry the model."),
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


def _retry_paragraph_span(text: str, variant: str) -> tuple[int, int]:
    """Locate the exact retry paragraph, ending at its next blank line."""
    lead = _RETRY_PARAGRAPH_LEADS[variant]
    start = text.index(lead)
    end = text.find("\n\n", start)
    return start, len(text) if end == -1 else end


def _retry_paragraph(text: str, variant: str) -> str:
    start, end = _retry_paragraph_span(text, variant)
    return _flat(text[start:end])


def _assert_retry_paragraph(path: Path, variant: str) -> None:
    """Read and check one physical source or installed file."""
    text = path.read_text(encoding="utf-8")
    paragraph = _retry_paragraph(text, variant)
    missing = sorted(
        label for label, clause in _RETRY_CLAUSES[variant].items()
        if clause not in paragraph
    )
    assert not missing, f"{path} is missing retry safeguard clauses: {missing}"
    expected = _RETRY_PARAGRAPHS[variant]
    assert paragraph == expected, f"{path} has an altered retry paragraph"


def _remove_retry_clause(text: str, variant: str, label: str) -> str:
    """Delete one uniquely matched clause from an isolated retry paragraph."""
    start, end = _retry_paragraph_span(text, variant)
    paragraph = text[start:end]
    anchor = _RETRY_CLAUSES[variant][label]
    pattern = re.compile(r"\s+".join(re.escape(part) for part in anchor.split()))
    matches = list(pattern.finditer(paragraph))
    assert len(matches) == 1, (variant, label, len(matches))
    match = matches[0]
    mutated_paragraph = paragraph[:match.start()] + paragraph[match.end():]
    mutated = text[:start] + mutated_paragraph + text[end:]
    assert mutated != text
    return mutated


#: What the fan-out paragraph of `docs/methodology/roles.md` must say about the check.
_FAN_OUT_CLAUSES = (
    "a stronger model from the same maker counts",
    "a model at the same tier does not",
)


def _fan_out_gaps(roles_text: str) -> list[str]:
    """The `_FAN_OUT_CLAUSES` the fan-out paragraph does not carry.

    The paragraph ends where the next one starts, `**Escalation applies`, with
    its bold markers. A split string without them never matches, the slice runs
    to the end of the file, and the cost-rule paragraph below (which carries the
    same two phrases) answers for the fan-out one.
    """
    flat = _flat(roles_text)
    start = flat.index("Orchestrated work — the fan-out.")
    end = flat.index("**Escalation applies", start)
    paragraph = flat[start:end]
    return [clause for clause in _FAN_OUT_CLAUSES if clause not in paragraph]


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


def test_task_floors_reject_lane_based_assignment_and_unreviewed_low_authority() -> None:
    """Wrong task tiers or omitted safeguards fail beside the real rule control."""
    real = _flat(_roles_section(_read(OWN_AGENTS)))
    assert _missing_rule_clauses(real) == []  # control
    mutants = (
        real.replace("Low covers execution of an accepted, reviewed plan",
                     "Medium covers execution of an accepted, reviewed plan"),
        real.replace("including high-risk chunks", "only trivial chunks"),
        real.replace("explicitly authorized by the Maintainer", "at the agent's discretion"),
        real.replace("does not lower its review or security obligations",
                     "removes its review and security obligations"),
        real.replace("The task sets the capability floor; the lane governs the process",
                     "The lane sets the capability floor; the task governs the process"),
    )
    for mutant in mutants:
        assert _missing_rule_clauses(mutant), "wrong-property control survived"


def test_the_rule_reads_the_same_in_both_copies() -> None:
    """Only the Maintainer's Cairn-local retry exception may differ."""
    def rule(rel: str) -> str:
        return _model_tier_rule(_read(rel))
    shipped = rule(SHIPPED_AGENTS)
    assert _OLD_IMMEDIATE_ESCALATION not in shipped
    assert rule(OWN_AGENTS) == shipped.replace(_OLD_IMMEDIATE_ESCALATION, "")
    _assert_retry_paragraph(ROOT / SHIPPED_AGENTS, "core")
    local = _flat(_roles_section(_read(OWN_AGENTS)))
    for requirement in (
        "**Cairn-only execution retries.**",
        "up to two same-tier retries after the initial failed attempt",
        "retains earlier failure evidence",
        "reruns only the affected check",
        "After two failed retries, re-run once one tier up",
        "Escalate immediately if the failure shows the task exceeds the assigned tier",
        "work below its capability floor is not eligible",
        "Retries never replace an independent review or Security Review",
        "Before repeating a potentially destructive operation, establish the previous attempt's effects",
    ):
        assert requirement in local


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
    """The rule is in the core file, not the module a solo profile never gets."""
    assert not (solo_install / "dev/modules/model-selection.md").exists()
    installed_path = solo_install / "AGENTS.md"
    installed = installed_path.read_text(encoding="utf-8")
    assert _missing_rule_clauses(_roles_section(installed)) == []
    assert _OLD_IMMEDIATE_ESCALATION not in _flat(installed)
    _assert_retry_paragraph(installed_path, "core")


def test_collaborative_profile_installs_rule_and_preserves_module_safeguards(
        collaborative_install: Path) -> None:
    """The optional module keeps its independent-check policy beside core retries."""
    installed_path = collaborative_install / "AGENTS.md"
    installed = installed_path.read_text(encoding="utf-8")
    assert _missing_rule_clauses(_roles_section(installed)) == []
    assert _OLD_IMMEDIATE_ESCALATION not in _flat(installed)
    _assert_retry_paragraph(installed_path, "core")

    module_path = collaborative_install / "dev/modules/model-selection.md"
    assert module_path.is_file()
    module = _flat(module_path.read_text(encoding="utf-8"))
    assert "a model at the same tier does not" in module
    assert "a failed review **escalates** the next attempt" in module


@pytest.mark.parametrize(
    "surface,label", _RETRY_CLAUSE_CASES,
    ids=[f"{surface}-{label}" for surface, label in _RETRY_CLAUSE_CASES],
)
def test_each_retry_clause_fails_when_removed_from_a_physical_copy(
        surface: str, label: str, solo_install: Path,
        collaborative_install: Path, tmp_path: Path) -> None:
    """Every required clause is read from source roles and both real installs."""
    if surface == "roles":
        source = ROOT / ROLES
        rel = ROLES
        variant = "roles"
    elif surface == "solo":
        source = solo_install / "AGENTS.md"
        rel = "AGENTS.md"
        variant = "core"
    else:
        source = collaborative_install / "AGENTS.md"
        rel = "AGENTS.md"
        variant = "core"

    control_path = tmp_path / "control" / rel
    mutant_path = tmp_path / "mutant" / rel
    control_path.parent.mkdir(parents=True)
    mutant_path.parent.mkdir(parents=True)
    original = source.read_text(encoding="utf-8")
    control_path.write_text(original, encoding="utf-8")
    assert _retry_paragraph(control_path.read_text(encoding="utf-8"), variant)
    _assert_retry_paragraph(control_path, variant)

    mutated = _remove_retry_clause(original, variant, label)
    mutant_path.write_text(mutated, encoding="utf-8")
    assert mutant_path.read_text(encoding="utf-8") == mutated
    assert mutated != original
    with pytest.raises(AssertionError, match=re.escape(label)):
        _assert_retry_paragraph(mutant_path, variant)


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
    """Both profiles install and detect a source-only loss of the retry limit."""
    control = solo_install if profile == "solo" else collaborative_install
    _assert_retry_paragraph(control / "AGENTS.md", "core")
    assert ((control / "dev/modules/model-selection.md").is_file()) is has_module

    cairn_copy = _clone_cairn_root(tmp_path / f"cairn-{profile}")
    shipped_path = cairn_copy / SHIPPED_AGENTS
    original = shipped_path.read_text(encoding="utf-8")
    mutated = _remove_retry_clause(
        original, "core", "two-retries-after-initial-failure")
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
    with pytest.raises(AssertionError,
                       match="two-retries-after-initial-failure"):
        _assert_retry_paragraph(target / "AGENTS.md", "core")


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

    assert _fan_out_gaps(texts[ROLES]) == []           # control
    # Delete each clause from the fan-out paragraph only: the cost-rule paragraph
    # further down keeps its own copy, so a check that read past the fan-out
    # paragraph's end would still pass.
    flat_roles = _flat(texts[ROLES])
    for clause in _FAN_OUT_CLAUSES:
        assert flat_roles.index(clause) < flat_roles.index("**Escalation applies")
        assert _fan_out_gaps(flat_roles.replace(clause, "", 1)) == [clause]
    for rel in MODULE_COPIES:
        flat = _flat(texts[rel])
        assert flat.count("a model at the same tier does not") == 2, rel

    mutant = dict(texts)
    mutant[SHIPPED_MODULE] = texts[SHIPPED_MODULE] + (
        "\n> author **and** is a different model architecture (a stronger model "
        "from the same maker is not one)\n")
    assert SHIPPED_MODULE in violations(mutant)


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

    for rel in MODULE_COPIES:
        text = _read(rel)
        assert task_floors(text) == expected, rel
        flat = _flat(text)
        assert "A premise-check is a separate high-tier task" in flat, rel
        assert "low-tier execution floor grants no authority to decide" in flat, rel
        assert "Fresh reviewer who did not implement the work" in flat, rel
        assert fanout_floors(text) == expected_fanout, rel
        assert "High-judgment tasks never downshift" in flat, rel
    assert _read(SHIPPED_MODULE) == _read(OWN_MODULE)

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

    roles = _flat(_read(ROLES))
    assert "The task sets the default floor; the lane governs the process" in roles
    assert "**High-capability tier** — strategy and research, premise-checking" in roles
    assert "security or trust-boundary judgment, and Security Review" in roles
    assert "**Medium-capability tier** — ordinary proposal authoring and ordinary" in roles
    assert "**Low-capability tier** — executing an accepted, reviewed plan" in roles
    assert "including non-trivial and high-risk chunks" in roles
    assert "when the Maintainer has explicitly authorized the scribing" in roles

    for rel in AGENTS_COPIES:
        flat = _flat(_read(rel))
        assert _missing_rule_clauses(_roles_section(_read(rel))) == []
        assert "Medium covers ordinary proposal authoring and ordinary proposal, plan and code reviews." in flat
