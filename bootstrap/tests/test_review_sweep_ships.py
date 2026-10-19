"""Every install receives the review sweep, not only teams that install a module.

The nine lenses a reviewer works through, the rule that a lens names what backs
it, the two-part coverage line that ends a review, and the falsification ledger
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
* **The ledger is defined once.** One definition, five items. A second, shorter
  list with a different item is how two versions of a rule drift apart.
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

import re
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

#: label -> pattern. The nine lenses, in the doctrine's order and under its
#: names. A lens is written as where a review's evidence comes from.
_LENSES = {
    "lens-1-claims":
        r"1\. Claims — probe every load-bearing claim",
    "lens-2-production-path-exercised-by-tests":
        r"2\. Production path exercised by tests —",
    "lens-3-design-completeness":
        r"3\. Design completeness —",
    "lens-4-silent-failure-fail-closed":
        r"4\. Silent failure / fail-closed —",
    "lens-5-cross-document-consistency":
        r"5\. Cross-document consistency —",
    "lens-6-drift":
        r"6\. Drift —",
    "lens-7-lifecycle-process-placement":
        r"7\. Lifecycle / process placement —",
    "lens-8-domain-scientific-validity-and-scope":
        r"8\. Domain / scientific validity & scope —",
    "lens-9-name-the-satisfier":
        r"9\. Name the satisfier —",
}

#: label -> pattern, for the sweep section of a review-loop document.
_SWEEP_OBLIGATIONS = {
    **_LENSES,
    "a-clean-pass-is-treated-with-skepticism":
        r"A review that finds nothing on a complex change is treated with "
        r"skepticism, not relief",
    "a-lens-is-where-the-evidence-for-the-three-answers-comes-from":
        r"where the evidence for a review's three answers comes from",
    "the-sweep-applies-to-the-reviews-the-lifecycle-calls-for":
        r"The sweep applies to the reviews the lifecycle calls for.{0,80}"
        r"A trivial change with no review owes none",
    "a-lens-names-the-file-test-line-or-command-that-backs-it":
        r"names the file path, test node, line or command output that backs it",
    "a-bare-checked-is-an-incomplete-review":
        r"A bare .#2: checked. is an incomplete review, not a pass",
    "coverage-line-covered-half":
        r"Covered — the lenses swept, each with its citation",
    "coverage-line-not-covered-half":
        r"Not covered / low confidence — the negative space",
    "coverage-line-does-not-end-in-a-recommendation-for-more-review":
        r"does not end in a recommendation for more review",
    "the-sweep-is-a-floor-never-a-downgrade-of-a-declared-tier":
        r"a floor, never a downgrade of a declared tier",
    "a-project-adds-its-own-probes-after-the-nine":
        r"A project adds its own probes after the nine",
    "a-clean-code-review-shows-a-falsification-ledger":
        r"A clean code review shows a falsification ledger",
    "ledger-surfaces-probed":
        r"Surfaces probed — what was actively examined or tried to break",
    "ledger-negative-or-edge-case-attempt":
        r"A negative or edge-case attempt — at least one",
    "ledger-verification-run-or-consciously-not":
        r"Verification — the commands run, with results; or an explicit "
        r"statement of what was not run and why",
    "ledger-residual-risk":
        r"Residual risk — what remains unverified",
    "ledger-mutation-when-a-claim-names-a-set":
        r"Mutation, when a claim names a set",
    "ledger-mutation-is-reported-against-an-unmutated-control":
        r"killed, survived or equivalent beside an unmutated control run, "
        r"never as a bare count",
    "a-reviewer-who-tried-to-break-it-has-cleared-the-gate":
        r"A reviewer who tried to break the change and reports honestly that "
        r"they could not has cleared the gate; a reviewer who only read it "
        r"has not",
}

#: label -> pattern, for the pointer paragraph in `AGENTS.md`.
_POINTER_OBLIGATIONS = {
    "pointer-names-the-sweep-in-the-loop-document":
        r"dev/agent_collaboration\.md > .The review sweep.",
    "pointer-says-the-answers-rest-on-nine-standing-lenses":
        r"rest on the nine standing lenses",
    "pointer-says-a-bare-checked-is-an-incomplete-review":
        r"a bare .checked. is an incomplete review",
    "pointer-says-the-coverage-line-names-what-was-not-covered":
        r"coverage line that ends the review says what the pass did not cover",
}

#: The pointer paragraph runs from its bold lead to the next blank line.
_POINTER_LEAD = "**Every review shows its evidence.**"


def _normalize(text: str) -> str:
    """Drop blockquote, emphasis and code markers; collapse whitespace."""
    text = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    text = text.replace("*", "").replace("`", "")
    return " ".join(text.split())


def _text(rel: str) -> str:
    return (CAIRN_ROOT / rel).read_text(encoding="utf-8")


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


def _delete_between(text: str, first: str, last: str) -> str:
    """Delete from the literal *first* up to, not including, the literal *last*."""
    flat = " ".join(text.split())
    a = flat.find(first)
    b = flat.find(last, a)
    assert a != -1 and b != -1, "anchors not found; the control is stale"
    return flat[:a] + flat[b:]


# --------------------------------------------------------------------------
# The two source copies of the review-loop document.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_SWEEP_OBLIGATIONS))
def test_source_sweep_carries_the_obligation(label: str, rel: str) -> None:
    assert label not in _missing(_sweep(_text(rel)), _SWEEP_OBLIGATIONS), (
        f"{rel} no longer carries {label!r} in 'The review sweep'. A solo team "
        f"receives this file and never the dual-review module, so removing it "
        f"here removes it for them.")


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_sweep_precedes_the_scope_reduction_trap(rel: str) -> None:
    """The trap opens by calling itself the mirror of the clean pass."""
    text = _text(rel)
    heading = re.search(r"^## The review sweep$", text, re.M)
    assert heading, f"{rel} has no 'The review sweep' heading"
    trap = text.find(f"**{_TRAP_OPENING}.**")
    assert trap != -1, f"{rel} lost the scope-reduction trap opening"
    assert heading.start() < trap, (
        f"{rel}: the sweep follows the trap, so 'the mirror' has no referent.")


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_lens_roster_is_exactly_nine_in_the_doctrines_order(rel: str) -> None:
    sweep = _normalize(_sweep(_text(rel)))
    positions = []
    for label, pattern in _LENSES.items():
        found = re.search(pattern, sweep)
        assert found, f"{rel} lost {label!r}"
        positions.append(found.start())
    assert positions == sorted(positions), f"{rel}: the lenses are out of order"
    numbered = re.findall(r"(?m)^(\d+)\. ", _sweep(_text(rel)))
    assert numbered == [str(n) for n in range(1, 10)], (
        f"{rel} lists lenses {numbered}; the roster is exactly nine and a "
        f"follower pins nine.")


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_anchors_a_follower_writes_against_are_present(rel: str) -> None:
    """Later work adds a sentence to a lens by its label, and to the sentence
    that says a finding is blocking or not, so all three are an interface:
    the sweep heading, the lens label, and that sentence, unchanged.
    """
    text = _text(rel)
    assert "Cross-document consistency" in _sweep(text)
    assert ("A finding is blocking or non-blocking, and says what evidence "
            "would close it.") in _normalize(text)


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_ledger_is_defined_once_with_five_items(rel: str) -> None:
    text = _normalize(_text(rel))
    assert len(re.findall(r"ledger of five items", text)) == 1, (
        f"{rel} must define the ledger exactly once, with five items.")
    assert not re.search(r"failure modes tested", text, re.I), (
        f"{rel} carries a sixth ledger item; there is one ledger.")


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_sweep_leaves_the_doctrines_reasoning_out(rel: str) -> None:
    sweep = _sweep(_text(rel))
    leaked = re.findall(r"telegraph|ritual|evidence bar is staged", sweep, re.I)
    assert not leaked, (
        f"{rel}: the sweep restates doctrine reasoning {leaked}. Installed "
        f"text states the rule; the argument for it stays in the doctrine.")


def test_the_leak_pattern_matches_the_doctrine_it_guards_against() -> None:
    """Confirm the instrument: it reads above zero where the reasoning lives."""
    doctrine = _text("doctrine/dual-review.md")
    assert re.findall(r"telegraph|ritual|evidence bar is staged", doctrine, re.I)
    assert not re.findall(r"telegraph|ritual|evidence bar is staged",
                          _sweep(_text(SHIPPED_LOOP)), re.I)


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_sweep_is_body_text_not_a_slot(rel: str) -> None:
    """A slot is frozen at its first fill, so the roster would stop updating."""
    assert "cairn:" not in _sweep(_text(rel))


# --------------------------------------------------------------------------
# The pointer in both AGENTS.md copies.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_POINTER_OBLIGATIONS))
def test_agents_md_pointer_carries_the_obligation(label: str, rel: str) -> None:
    assert label not in _missing(_pointer(_text(rel)), _POINTER_OBLIGATIONS), (
        f"{rel} lost {label!r} from the pointer. The full text lives in the "
        f"review-loop document; this is how an agent that reads only "
        f"AGENTS.md finds it.")


@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
def test_the_pointer_names_no_test_path(rel: str) -> None:
    """A shipped file must not name a Cairn-only path (the boundaries test)."""
    assert _missing(_pointer(_text(rel)), _POINTER_OBLIGATIONS) == []
    assert "bootstrap/tests" not in _pointer(_text(rel))


# --------------------------------------------------------------------------
# Through a real install, for every shipped profile.
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def installs(tmp_path_factory) -> dict[str, Path]:
    """Install each shipped profile once; return profile stem -> target tree.

    The profiles are globbed, so one added later is installed and checked
    without editing this file; the three that ship today must be among them,
    or a broken glob would pass by checking nothing.
    """
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
@pytest.mark.parametrize("label", sorted(_SWEEP_OBLIGATIONS))
def test_installed_loop_document_carries_the_obligation(
        installs: dict[str, Path], profile: Path, label: str) -> None:
    text = (installs[profile.stem] / "dev" / "agent_collaboration.md").read_text(
        encoding="utf-8")
    assert label not in _missing(_sweep(text), _SWEEP_OBLIGATIONS), (
        f"a {profile.stem} install lacks {label!r}. Everyone should get the "
        f"review sweep, whatever modules they selected.")


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
@pytest.mark.parametrize("label", sorted(_POINTER_OBLIGATIONS))
def test_installed_agents_md_carries_the_pointer(
        installs: dict[str, Path], profile: Path, label: str) -> None:
    text = (installs[profile.stem] / "AGENTS.md").read_text(encoding="utf-8")
    assert label not in _missing(_pointer(text), _POINTER_OBLIGATIONS), (
        f"a {profile.stem} install's AGENTS.md lost {label!r} from its pointer.")


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
def test_an_install_without_the_sweep_is_reported(
        installs: dict[str, Path], profile: Path) -> None:
    """The install check can fail: drop the section and every item goes missing."""
    text = (installs[profile.stem] / "dev" / "agent_collaboration.md").read_text(
        encoding="utf-8")
    assert _missing(_sweep(text), _SWEEP_OBLIGATIONS) == [], (
        f"the unmutated {profile.stem} install is missing items; no control.")
    gutted = text.replace(_sweep(text), "## The review sweep\n\n")
    assert sorted(_missing(_sweep(gutted), _SWEEP_OBLIGATIONS)) == \
        sorted(_SWEEP_OBLIGATIONS)


# --------------------------------------------------------------------------
# Mutants: delete one thing from a copy and a named check must go red, beside
# an unmutated control that is green.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_deleting_lens_4_is_reported(rel: str) -> None:
    sweep = _sweep(_text(rel))
    assert _missing(sweep, _SWEEP_OBLIGATIONS) == []
    mutant = re.sub(r"(?s)\b4\. .*?(?=\b5\. )", "", " ".join(sweep.split()))
    assert "lens-4-silent-failure-fail-closed" in _missing(mutant, _SWEEP_OBLIGATIONS)


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_deleting_the_not_covered_half_is_reported(rel: str) -> None:
    sweep = _sweep(_text(rel))
    assert _missing(sweep, _SWEEP_OBLIGATIONS) == []
    mutant = _delete_between(sweep, "Not covered / low confidence",
                             "The line does not end")
    assert "coverage-line-not-covered-half" in _missing(mutant, _SWEEP_OBLIGATIONS)


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_deleting_the_scope_sentence_is_reported(rel: str) -> None:
    sweep = _sweep(_text(rel))
    assert _missing(sweep, _SWEEP_OBLIGATIONS) == []
    mutant = _delete_sentence(sweep, "calls for")
    assert "the-sweep-applies-to-the-reviews-the-lifecycle-calls-for" in _missing(
        mutant, _SWEEP_OBLIGATIONS)


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_adding_a_sixth_ledger_item_is_reported(rel: str) -> None:
    """A second shape of the ledger is what the single definition guards against."""
    text = _text(rel)
    assert len(re.findall(r"ledger of five items", _normalize(text))) == 1
    mutant = text + "\n\nA ledger of five items, in a shorter form.\n"
    assert len(re.findall(r"ledger of five items", _normalize(mutant))) == 2


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
# The lens text exists once. The dual-review module used to hold the roster,
# the citation rule and the ledger; it is thinned to how a team staffs a read
# the Maintainer has called, and carries none of them. A second copy of the
# roster in the module is how two definitions drift apart, and a team that
# selected the module would merge both into its loop document.
# --------------------------------------------------------------------------

SHIPPED_MODULE = "templates/modules/team-gated/dual-review.md"
OWN_MODULE = "dev/modules/dual-review.md"
_MODULE_FILES = (SHIPPED_MODULE, OWN_MODULE)
_MODULE_IDS = {SHIPPED_MODULE: "shipped-module", OWN_MODULE: "own-module"}

#: label -> pattern for the text only the review-loop document may carry.
_MODULE_ABSENT = {
    **{f"module-has-{label}": pattern for label, pattern in _LENSES.items()},
    "module-has-the-citation-rule":
        r"Falsifiable coverage|names the file path, test node, line or command "
        r"output|bare .#2: checked.",
    "module-has-the-ledger-items":
        r"Surfaces probed|A negative or edge-case attempt|Residual risk — what "
        r"remains|Probed edge cases|Failure modes tested|Verification run "
        r"\(or consciously not\)",
    "module-has-a-second-ledger-definition":
        r"ledger of five items|lightweight four-part record|falsification ledger",
    "module-has-a-duplicate-scope-reduction-trap":
        r"scope-cut means claim correction|The scope-reduction trap — the "
        r"mirror of the clean pass|The outcome test\. Judge a narrowing",
}


def _module_carries(text: str) -> list[str]:
    normalized = _normalize(text)
    return [label for label, pattern in _MODULE_ABSENT.items()
            if re.search(pattern, normalized)]


def _sweep_part(rel: str, start: str, end: str) -> str:
    """A stretch of the sweep, between two literals, as the module once held it."""
    flat = _normalize(_sweep(_text(rel)))
    a = flat.index(start)
    return flat[a:flat.index(end, a)]


@pytest.mark.parametrize("rel", _MODULE_FILES, ids=_MODULE_IDS.get)
def test_the_module_carries_no_lens_citation_rule_or_ledger(rel: str) -> None:
    found = _module_carries(_text(rel))
    assert not found, (
        f"{rel} carries {found}. That text lives once, in the review-loop "
        f"document every install receives; a second copy drifts.")


@pytest.mark.parametrize("rel", _MODULE_FILES, ids=_MODULE_IDS.get)
def test_restoring_the_roster_into_the_module_is_reported(rel: str) -> None:
    assert _module_carries(_text(rel)) == [], "control: the module is clean"
    roster = _sweep_part(SHIPPED_LOOP, "1. Claims", "The sweep applies to")
    found = _module_carries(f"{_text(rel)}\n\n> {roster}\n")
    assert "module-has-lens-4-silent-failure-fail-closed" in found
    assert "module-has-lens-1-claims" in found


@pytest.mark.parametrize("rel", _MODULE_FILES, ids=_MODULE_IDS.get)
def test_restoring_the_citation_rule_into_the_module_is_reported(rel: str) -> None:
    assert _module_carries(_text(rel)) == [], "control: the module is clean"
    rule = _sweep_part(SHIPPED_LOOP, "Falsifiable coverage", "End with a two-part")
    assert "module-has-the-citation-rule" in _module_carries(
        f"{_text(rel)}\n\n> {rule}\n")


@pytest.mark.parametrize("rel", _MODULE_FILES, ids=_MODULE_IDS.get)
def test_restoring_the_ledger_into_the_module_is_reported(rel: str) -> None:
    assert _module_carries(_text(rel)) == [], "control: the module is clean"
    ledger = _sweep_part(SHIPPED_LOOP, "A clean code review shows a falsification "
                                       "ledger", "A reviewer who tried to break")
    found = _module_carries(f"{_text(rel)}\n\n> {ledger}\n")
    assert "module-has-the-ledger-items" in found
    assert "module-has-a-second-ledger-definition" in found
