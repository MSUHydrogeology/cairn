"""The review stance and the Maintainer-called read must reach the adopter.

`doctrine/` is **not installed into an adopter tree**, so a rule that lives only
there binds nobody who adopts Cairn. The stance sits in `templates/core/AGENTS.md`
(the file every adopter receives and every agent loads each session) and in
Cairn's own root `AGENTS.md`; the roster sits in the review-loop document and
Cairn's copy of it.

What is pinned, and why:

* **One review at every stage.** No agent picks a kind of review. The stage sets
  three questions, every pass answers them with evidence and names what it did
  not cover, and a narrowing is a scope change only the Maintainer concedes.
* **More distance is the Maintainer's call, and only theirs.** A called read is
  per artifact, recorded with the Maintainer's words, adds to the usual review
  and replaces nothing, and confers no authority beyond its own read. Nothing
  checks the quoted words mechanically, and the shipped text says so: a reader
  does. A sentence that credited a tool with checking them would be worse than
  none, because it is silent.
* **A Security Review stays its own pass.** The usual pass never clears it, and
  a plan's security obligation is cleared only by an appended pass whose
  obligation line matches. No tool reads that line either.
* **The old vocabulary stays out.** A rule that makes an agent choose, require or
  recommend a more distant reviewer is the failure this guards against. The two
  copies of the dual-review module may keep their remaining wording, but not the
  clause that lets a more distant pass stand in for a falsification ledger.

Each obligation is an alternation matched against text with emphasis and code
markers removed and whitespace collapsed, so a rewording that keeps the
obligation passes and a deletion fails. Node IDs are the obligation labels,
never the patterns, so rewording a pattern renames nothing. Patterns are
literals, not derived from the files they check.

**Controls.** Every check that reports a loss has a control run on the unmutated
file first: the whole file must be clean before a deliberate break is expected to
make one named check fail. A break is made by deleting a sentence located by a
literal that is not the obligation's own pattern, so the control does not take
its mutation from the pattern under test.

Run from the Cairn repo root:
    python -m pytest bootstrap/tests/test_review_stance_in_shipped_files.py
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent

#: The shipped copy is the load-bearing one (adopters receive it). Cairn's own
#: copy keeps Cairn bound by what it ships.
SHIPPED_AGENTS = "templates/core/AGENTS.md"
OWN_AGENTS = "AGENTS.md"
SHIPPED_LOOP = "templates/core/dev/agent_collaboration.md"
OWN_LOOP = "dev/agent_collaboration.md"
SHIPPED_MODULE = "templates/modules/team-gated/dual-review.md"
OWN_MODULE = "dev/modules/dual-review.md"

_AGENTS_FILES = (SHIPPED_AGENTS, OWN_AGENTS)
_LOOP_FILES = (SHIPPED_LOOP, OWN_LOOP)
_MODULE_FILES = (SHIPPED_MODULE, OWN_MODULE)
_CARRIER_FILES = _AGENTS_FILES + _LOOP_FILES
_FILE_IDS = {
    SHIPPED_AGENTS: "shipped-agents", OWN_AGENTS: "own-agents",
    SHIPPED_LOOP: "shipped-loop", OWN_LOOP: "own-loop",
    SHIPPED_MODULE: "shipped-module", OWN_MODULE: "own-module",
}

#: label -> pattern, for the `## Review` section of both `AGENTS.md` copies.
_STANCE_OBLIGATIONS = {
    # One stance, three stage questions, and what every pass must show.
    "one-stance-at-every-stage":
        r"One stance at every stage",
    "a-fresh-reviewer-on-the-works-side":
        r"fresh reviewer who did not write the work, on the work's side",
    "the-stage-sets-three-questions":
        r"Should this exist as framed\? Is there a better design, doing "
        r"nothing included\?.*?The Decision settled the premise\. Does the "
        r"plan deliver it\?.*?Does it really do what it claims\? Try to "
        r"break it, in order to fix it",
    "foundations-block-three-answers-each-with-its-evidence":
        r"Foundations block of three lines, one answer per question, each "
        r"ending in the file, test, line or command that backs it",
    "improve-means-recommend":
        r"Improve means recommend",
    "no-quota-of-findings":
        r"There is no quota of findings",
    "a-clean-pass-needs-evidenced-answers-and-named-gaps":
        r"No defects found.{1,3} is allowed only with the three answers "
        r"evidenced and the gaps named",
    # Code review keeps its floor and never reopens the Decision.
    "code-review-floor-is-not-the-implementing-agent":
        r"floor is not the implementing agent",
    "code-review-never-reopens-the-decision":
        r"never reopens the Decision",
    "a-clean-code-review-shows-a-falsification-ledger":
        r"A clean code review shows a falsification ledger",
    # A narrowing is a scope change, whoever recommends it.
    "a-narrowing-is-a-scope-change-only-the-maintainer-concedes":
        r"recommends narrowing the work states what is lost and why the "
        r"narrower change still reaches the cause; only the Maintainer "
        r"concedes a loss",
    # A Security Review stays its own pass, and no tool reads its line.
    "a-high-risk-surface-takes-a-security-review":
        r"A high-risk surface takes a Security Review",
    "usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second":
        r"usual \+ Security Review in a header means two passes: the usual "
        r"pass and a Security Review pass that names its own obligation\. "
        r"The usual pass never clears the second",
    "a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line":
        r"Plan review: required\(Internal \+ Internal Security Review\)\. "
        r"Only an appended ## Plan review pass whose Obligation line matches "
        r"clears it, never an ordinary Internal pass",
    "no-tool-reads-the-obligation-line-a-reader-does":
        r"No tool reads that line: the next reviewer, the code reviewer and "
        r"the Maintainer check it",
    # What a Maintainer-called read is.
    "external-means-the-maintainer-called-it":
        r"An External read is a review the Maintainer asked for",
    "a-call-names-one-artifact-that-exists-now":
        r"on one named artifact that exists now",
    "a-standing-call-is-a-floor-and-returns-only-by-proposal":
        r"A call that covers artifacts not yet written is a standing floor.{0,80}"
        r"a standing floor returns only by proposal",
    "a-roster-you-set-is-not-a-call":
        r"A roster the Maintainer sets in dev/collaboration_agreement\.md.{0,80}"
        r"is the team's shape, not a call: it adds no read and upgrades none",
    "distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so":
        r"Distance is information, not a rule.{0,200}The staffing reviewer "
        r"follows the Maintainer's brief, answers the same three questions "
        r"from that distance, and says so",
    # How it is recorded.
    "called-by-carries-the-maintainers-words-verbatim":
        r"followed by the Maintainer's words, verbatim and set apart",
    "called-by-quote-is-repeated-in-the-commit-body":
        r"The same words go in the commit message, as for a scribed Decision",
    "called-by-names-where-the-words-live":
        r"Called by: Maintainer -- Decision at <commit>.{0,40}-- chat, <date>",
    "tier-external-needs-called-by-else-read-as-the-usual-review":
        r"Tier: External is valid only with that line, and a pass headed "
        r"External without it is read as the usual review",
    # What an agent never does, and what a called read never does.
    "no-agent-declares-external-required-or-recommends-distance":
        r"Declare External as a required review in a header, say a change "
        r"needs one, recommend more distance, head a pass External on its "
        r"own, or start one without those words",
    "a-called-read-adds-and-replaces-nothing":
        r"It adds to the usual review and replaces nothing",
    "a-called-brief-adds-focus-and-removes-no-owed-answer":
        r"Its brief may add focus; it removes no owed answer",
    "a-called-read-discharges-no-security-review-by-distance-or-brief":
        r"discharges no Security Review by its distance or its brief",
    "other-authority-lives-in-a-decision-or-a-plan-fence":
        r"takes effect only where Maintainer authorizations already live, a "
        r"Decision block or a plan's fence",
    "a-called-by-line-never-confers-authority":
        r"never from a Called by line",
    "nothing-checks-the-quote-a-reader-does":
        r"Nothing checks the quote mechanically, in the pass or in the commit "
        r"message: the next reviewer and the Maintainer at the Decision are "
        r"the check",
}

#: label -> pattern, for the review-loop document's roster (both copies).
_ROSTER_OBLIGATIONS = {
    "one-reviewer-role-on-the-works-side":
        r"Reviewer — a fresh reviewer who did not write the work, on the "
        r"work's side",
    "the-reviewer-carries-the-neutral-briefing":
        r"neutral briefing that lays out the decision space without steering it",
    "security-review-and-user-agent-stay-on-the-roster":
        r"Security Review — an adversarial read aimed at a high-risk surface"
        r".{0,400}User Agent — exercises",
    "a-fresh-session-is-every-reviews-floor":
        r"A fresh session is every review's floor, and no review requires a "
        r"different agent type",
    "distance-is-read-from-attribution-and-the-maintainer-may-ask-for-more":
        r"How far a reviewer stood from the author is read from its "
        r"attribution, and the Maintainer may ask for more distance",
}

#: label -> pattern that must NOT occur. Matched against normalized text,
#: ignoring case, so a capital letter or a line wrap cannot hide a phrase.
_FORBIDDEN = {
    "required-external-in-a-header": r"required\(external",
    "external-floor": r"external[ -]floor",
    "external-tier": r"external[ -]tier",
    "external-review": r"external[ -]review",
    "external-code-review": r"external[ -]code[ -]review",
    "external-independence": r"external[ -]independence",
    "external-stance": r"external[ -]stance",
    "declared-external": r"declared-external",
    "a-human-fills-a-tier": r"a human fills",
    "a-different-agent-type-pass-or-round":
        r"different-agent-type (pass|round)",
    "escalate-to-the-external-tier": r"escalate to the external",
    "external-review-norms-heading": r"External Review Norms",
    "code-review-is-not-external-by-default": r"external[- ]by[- ]default",
    "internal-reviewer-role": r"internal reviewer",
    "tiers-are-stances-sentence": r"tiers are stances",
    "across-structural-independence": r"across structural independence",
    "the-reviewer-tiers": r"reviewer tiers",
    "the-checker-cannot-parse": r"the checker cannot parse",
    # A sentence that credits a tool with checking the obligation line or the
    # quoted words. "No tool reads that line" is the honest statement and must
    # not match, hence the lookbehinds.
    "a-tool-is-credited-with-checking-the-quote":
        r"(?<!no )(?<!not )\b(tool|checker|hook|gate|script|linter) "
        r"(reads|checks|validates|verifies|parses) (the|that|this) "
        r"(called by|obligation|quote|line)",
}

#: label -> a string each forbidden pattern exists to keep out. Inserted into an
#: unmutated copy it must make exactly that label fire.
_FORBIDDEN_EXAMPLES = {
    "required-external-in-a-header":
        "Plan review: required(External) is declared in the header.",
    "external-floor": "The External floor lives at the proposal.",
    "external-tier": "A human fills the External tier.",
    "external-review": "A change touching a contract gets an External review.",
    "external-code-review": "An External code review is an escalation.",
    "external-independence": "External independence lives at the proposal.",
    "external-stance": "The External stance is make-it-prove-itself.",
    "declared-external": "A declared-External proposal wants a cross-type read.",
    "a-human-fills-a-tier": "Where the team is one agent type, a human fills it.",
    "a-different-agent-type-pass-or-round":
        "Or a second different-agent-type pass confirms it.",
    "escalate-to-the-external-tier":
        "Escalate to the External-review tier for scientific risk.",
    "external-review-norms-heading": "See External Review Norms.",
    "code-review-is-not-external-by-default":
        "Code review is External by default.",
    "internal-reviewer-role": "The Internal Reviewer strengthens the change.",
    "tiers-are-stances-sentence":
        "Tiers are stances, not staffing classes.",
    "across-structural-independence":
        "A Dual-Review model across structural independence.",
    "the-reviewer-tiers": "Other roles (Strategy, the reviewer tiers) are frames.",
    "the-checker-cannot-parse":
        "Never by a heading the checker cannot parse.",
    "a-tool-is-credited-with-checking-the-quote":
        "A checker reads the Obligation line and rejects a mismatch.",
}

#: Why each wording is wrong, shown when it comes back.
_FORBIDDEN_REASON = (
    "carries a phrasing that makes a kind of review something an agent picks, "
    "requires or recommends, or that describes the old two-stance review. More "
    "distance is the Maintainer's call on one named artifact; everything else "
    "is one review at every stage. Reword the sentence; do not widen the "
    "pattern's exemptions."
)

#: The module keeps its remaining wording for now. Only the clause that lets a
#: more distant pass stand in for a falsification ledger is held out.
_MODULE_FORBIDDEN = {
    "a-confirming-pass-never-stands-in-for-a-falsification-ledger":
        r"confirmed by a second independent different-agent-type pass",
}
_MODULE_FORBIDDEN_EXAMPLES = {
    "a-confirming-pass-never-stands-in-for-a-falsification-ledger":
        "It either carries a falsification ledger or is confirmed by a "
        "second independent different-agent-type pass.",
}


def _normalize(text: str) -> str:
    """Drop blockquote, emphasis and code markers; collapse whitespace.

    So bold, a code span or a line wrap cannot split a phrase, and a module's
    `> ` prefix on every wrapped line does not sit inside a sentence.
    """
    text = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    text = text.replace("*", "").replace("`", "")
    return " ".join(text.split())


def _text(rel: str) -> str:
    return (CAIRN_ROOT / rel).read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    """The body of `## <heading>`, up to the next second-level heading."""
    match = re.search(rf"^## {re.escape(heading)}$(.*?)(?=^## |\Z)", text,
                      re.M | re.S)
    assert match, f"no '## {heading}' section"
    return match.group(1)


def _missing(text: str, obligations: dict[str, str]) -> list[str]:
    """Labels of the obligations absent from *text*."""
    normalized = _normalize(text)
    return [label for label, pattern in obligations.items()
            if not re.search(pattern, normalized)]


def _present(text: str, forbidden: dict[str, str]) -> list[str]:
    """Labels of the forbidden phrasings present in *text*."""
    normalized = _normalize(text)
    return [label for label, pattern in forbidden.items()
            if re.search(pattern, normalized, re.IGNORECASE)]


def _delete_sentence(text: str, anchor: str) -> str:
    """Delete the sentence of *text* that contains the literal *anchor*.

    A sentence runs from the previous ". " (or paragraph start) to the next
    ". ". The anchor is a literal chosen by the caller, so the deletion is not
    located by the obligation's own pattern.
    """
    flat = " ".join(text.split())
    at = flat.find(anchor)
    assert at != -1, f"anchor {anchor!r} not found; the control is stale"
    start = max(flat.rfind(". ", 0, at) + 2, 0)
    end = flat.find(". ", at)
    end = len(flat) if end == -1 else end + 2
    return flat[:start] + flat[end:]


def _review_section(rel: str) -> str:
    return _section(_text(rel), "Review")


# --------------------------------------------------------------------------
# The stance, in the `## Review` section of both AGENTS.md copies.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_STANCE_OBLIGATIONS))
def test_review_section_carries_the_obligation(label: str, rel: str) -> None:
    assert label not in _missing(_review_section(rel), _STANCE_OBLIGATIONS), (
        f"{rel} no longer carries {label!r} inside '## Review'. The doctrine "
        f"holds the same rule, but adopters never receive doctrine/; placement "
        f"in Review is part of the rule, because a reviewer looks there first."
    )


@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_STANCE_OBLIGATIONS))
def test_removing_the_obligation_is_reported(label: str, rel: str) -> None:
    """The check above can fail: strip every match and it must report the loss.

    The control comes first: the unmutated section must carry every obligation,
    or a reported loss proves nothing about this one.
    """
    section = _review_section(rel)
    assert _missing(section, _STANCE_OBLIGATIONS) == [], (
        f"{rel}: the unmutated Review section is missing obligations, so this "
        f"control cannot show that {label!r} is checked.")
    stripped = re.sub(_STANCE_OBLIGATIONS[label], "", _normalize(section))
    assert label in _missing(stripped, _STANCE_OBLIGATIONS)


@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
def test_the_stance_sits_in_the_review_section_only_once(rel: str) -> None:
    """The three stage questions are stated once, in Review, not repeated."""
    text = _normalize(_text(rel))
    assert len(re.findall(r"The Decision settled the premise", text)) == 1


# --------------------------------------------------------------------------
# The roster, in the review-loop document.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_ROSTER_OBLIGATIONS))
def test_loop_document_roster_carries_the_obligation(label: str, rel: str) -> None:
    roster = _section(_text(rel), "Team roles")
    assert label not in _missing(roster, _ROSTER_OBLIGATIONS), (
        f"{rel} no longer carries {label!r} in its roster. There is one "
        f"Reviewer role; a reviewer tier or an Internal/External split is the "
        f"description this change retired."
    )


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_ROSTER_OBLIGATIONS))
def test_removing_a_roster_obligation_is_reported(label: str, rel: str) -> None:
    roster = _section(_text(rel), "Team roles")
    assert _missing(roster, _ROSTER_OBLIGATIONS) == [], (
        f"{rel}: the unmutated roster is missing obligations; no control.")
    stripped = re.sub(_ROSTER_OBLIGATIONS[label], "", _normalize(roster))
    assert label in _missing(stripped, _ROSTER_OBLIGATIONS)


# --------------------------------------------------------------------------
# The old vocabulary stays out of the four carrier files.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", _CARRIER_FILES, ids=_FILE_IDS.get)
def test_carrier_omits_the_old_vocabulary(rel: str) -> None:
    found = _present(_text(rel), _FORBIDDEN)
    assert not found, f"{rel} {_FORBIDDEN_REASON} Found: {found}"


@pytest.mark.parametrize("rel", _CARRIER_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_FORBIDDEN))
def test_inserting_the_old_wording_is_reported(label: str, rel: str) -> None:
    """The check above can fail: put the old wording back and it must fire.

    The control comes first: the unmutated file must be clean, so the label
    that fires is the one inserted and not a leftover.
    """
    intact = _text(rel)
    assert _present(intact, _FORBIDDEN) == [], (
        f"{rel}: the unmutated file already carries old wording; no control.")
    assert label in _present(f"{intact}\n\n{_FORBIDDEN_EXAMPLES[label]}\n",
                             _FORBIDDEN)


@pytest.mark.parametrize("variant", [
    "Code review is External by default.",
    "code review is EXTERNAL BY DEFAULT.",
    "Code review is External\n  by   default.",
    "Code review is External-by-default.",
], ids=["plain", "capitals", "wrapped", "hyphenated"])
def test_the_by_default_pin_ignores_case_and_wrapping(variant: str) -> None:
    """The pin guards the claim, not one spelling of it.

    A sync from an older copy brings the sentence back as it was, but a reflow
    or a capital letter must not hide it from the check. Run against the real
    shipped file first, so the pin is shown live and not only on a string.
    """
    assert _present(_text(SHIPPED_AGENTS), _FORBIDDEN) == []
    assert "code-review-is-not-external-by-default" in _present(
        f"{_text(SHIPPED_AGENTS)}\n\n{variant}\n", _FORBIDDEN)


def test_a_sentence_saying_no_tool_reads_the_line_is_not_flagged() -> None:
    """The honest statement must not trip the pattern that forbids its opposite."""
    honest = ("No tool reads that line: the next reviewer, the code reviewer "
              "and the Maintainer check it.")
    assert _present(_text(SHIPPED_AGENTS), _FORBIDDEN) == []
    assert "a-tool-is-credited-with-checking-the-quote" not in _present(
        honest, _FORBIDDEN)
    assert "a-tool-is-credited-with-checking-the-quote" in _present(
        "A tool reads that line and rejects a mismatch.", _FORBIDDEN)


# --------------------------------------------------------------------------
# The dual-review module: only the standing-in clause is held out for now.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", _MODULE_FILES, ids=_FILE_IDS.get)
def test_module_does_not_let_a_confirming_pass_stand_in_for_a_ledger(rel: str) -> None:
    assert _present(_text(rel), _MODULE_FORBIDDEN) == [], (
        f"{rel} lets a second pass from a different kind of agent stand in for "
        f"a falsification ledger. Only the ledger clears a clean code review; "
        f"a more distant pass is information, never a substitute for evidence.")


@pytest.mark.parametrize("rel", _MODULE_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_MODULE_FORBIDDEN))
def test_inserting_the_standing_in_clause_is_reported(label: str, rel: str) -> None:
    intact = _text(rel)
    assert _present(intact, _MODULE_FORBIDDEN) == [], (
        f"{rel}: the unmutated module already carries the clause; no control.")
    assert label in _present(f"{intact}\n\n{_MODULE_FORBIDDEN_EXAMPLES[label]}\n",
                             _MODULE_FORBIDDEN)


# --------------------------------------------------------------------------
# Mutants: delete one sentence from one copy and a named check must go red,
# beside an unmutated control that is green.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
def test_deleting_the_called_by_authority_sentence_is_reported(rel: str) -> None:
    section = _review_section(rel)
    assert _missing(section, _STANCE_OBLIGATIONS) == []
    mutant = _delete_sentence(section, "Maintainer authorizations already live")
    gone = _missing(mutant, _STANCE_OBLIGATIONS)
    assert "a-called-by-line-never-confers-authority" in gone
    assert "other-authority-lives-in-a-decision-or-a-plan-fence" in gone


@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
def test_deleting_the_plan_obligation_sentence_is_reported(rel: str) -> None:
    section = _review_section(rel)
    assert _missing(section, _STANCE_OBLIGATIONS) == []
    mutant = _delete_sentence(section, "calls for security treatment declares")
    assert "a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line" \
        in _missing(mutant, _STANCE_OBLIGATIONS)


@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
def test_deleting_the_two_pass_sentence_is_reported(rel: str) -> None:
    section = _review_section(rel)
    assert _missing(section, _STANCE_OBLIGATIONS) == []
    mutant = _delete_sentence(section, "means two passes")
    assert "usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second" \
        in _missing(mutant, _STANCE_OBLIGATIONS)


@pytest.mark.parametrize("rel", _CARRIER_FILES, ids=_FILE_IDS.get)
def test_adding_required_external_to_a_carrier_is_reported(rel: str) -> None:
    """The called-read paragraph does not spell the header value it forbids.

    So the unmutated control is green, and adding the value turns exactly the
    node that forbids it red.
    """
    intact = _text(rel)
    assert _present(intact, _FORBIDDEN) == []
    mutant = f"{intact}\n\nPlan review: required(External)\n"
    assert _present(mutant, _FORBIDDEN) == ["required-external-in-a-header"]
