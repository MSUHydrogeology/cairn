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

* **The authoring templates carry it too.** An author reads the proposal or
  plan template while writing, and a reviewer reads the pass skeleton while
  reviewing, so each template states the stance, the questions for its kind of
  artifact, the called-read rules and (for plans) the security obligation, and
  its header and skeleton offer only the values the stance allows: `usual` and
  `usual + Security Review`; External only beside a line saying who called it.

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

SHIPPED_PROPOSAL = "templates/core/dev/proposals/_template.md"
OWN_PROPOSAL = "dev/proposals/_template.md"
SHIPPED_PLAN = "templates/core/dev/plans/_template.md"
OWN_PLAN = "dev/plans/_template.md"

_AGENTS_FILES = (SHIPPED_AGENTS, OWN_AGENTS)
_PROPOSAL_TEMPLATES = (SHIPPED_PROPOSAL, OWN_PROPOSAL)
_PLAN_TEMPLATES = (SHIPPED_PLAN, OWN_PLAN)
_TEMPLATE_FILES = _PROPOSAL_TEMPLATES + _PLAN_TEMPLATES
_LOOP_FILES = (SHIPPED_LOOP, OWN_LOOP)
_MODULE_FILES = (SHIPPED_MODULE, OWN_MODULE)
_CARRIER_FILES = _AGENTS_FILES + _LOOP_FILES
_FILE_IDS = {
    SHIPPED_AGENTS: "shipped-agents", OWN_AGENTS: "own-agents",
    SHIPPED_LOOP: "shipped-loop", OWN_LOOP: "own-loop",
    SHIPPED_MODULE: "shipped-module", OWN_MODULE: "own-module",
    SHIPPED_PROPOSAL: "shipped-proposal", OWN_PROPOSAL: "own-proposal",
    SHIPPED_PLAN: "shipped-plan", OWN_PLAN: "own-plan",
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


# --------------------------------------------------------------------------
# The authoring templates: the proposal and plan templates, each with Cairn's
# own copy. They are read while writing and while reviewing.
# --------------------------------------------------------------------------

#: Labels every template carries, taken from the stance obligations above:
#: the stance, the foundations block, and the whole called-read statement.
_COMMON_TEMPLATE_LABELS = (
    "one-stance-at-every-stage",
    "a-fresh-reviewer-on-the-works-side",
    "foundations-block-three-answers-each-with-its-evidence",
    "improve-means-recommend",
    "no-quota-of-findings",
    "a-clean-pass-needs-evidenced-answers-and-named-gaps",
    "external-means-the-maintainer-called-it",
    "a-call-names-one-artifact-that-exists-now",
    "a-standing-call-is-a-floor-and-returns-only-by-proposal",
    "a-roster-you-set-is-not-a-call",
    "distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so",
    "called-by-carries-the-maintainers-words-verbatim",
    "called-by-quote-is-repeated-in-the-commit-body",
    "called-by-names-where-the-words-live",
    "tier-external-needs-called-by-else-read-as-the-usual-review",
    "no-agent-declares-external-required-or-recommends-distance",
    "a-called-read-adds-and-replaces-nothing",
    "a-called-brief-adds-focus-and-removes-no-owed-answer",
    "a-called-read-discharges-no-security-review-by-distance-or-brief",
    "other-authority-lives-in-a-decision-or-a-plan-fence",
    "a-called-by-line-never-confers-authority",
    "nothing-checks-the-quote-a-reader-does",
)
_PROPOSAL_ONLY_LABELS = (
    "a-high-risk-surface-takes-a-security-review",
    "usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second",
)
_PLAN_ONLY_LABELS = (
    "code-review-floor-is-not-the-implementing-agent",
    "code-review-never-reopens-the-decision",
    "a-clean-code-review-shows-a-falsification-ledger",
    "a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line",
    "no-tool-reads-the-obligation-line-a-reader-does",
)

_PROPOSAL_TEMPLATE_OBLIGATIONS = {
    **{k: _STANCE_OBLIGATIONS[k]
       for k in _COMMON_TEMPLATE_LABELS + _PROPOSAL_ONLY_LABELS},
    "a-proposal-review-asks-whether-it-should-exist-as-framed":
        r"Should this happen as framed\? Should this exist as framed\? Is there "
        r"a better design, doing nothing included\?",
}
_PLAN_TEMPLATE_OBLIGATIONS = {
    **{k: _STANCE_OBLIGATIONS[k]
       for k in _COMMON_TEMPLATE_LABELS + _PLAN_ONLY_LABELS},
    "a-plan-review-asks-whether-the-plan-delivers-the-decision":
        r"Should this happen as framed\? The Decision settled the premise\. "
        r"Does the plan deliver it\?",
    "a-code-review-asks-whether-it-does-what-it-claims":
        r"Should this happen as framed\? Does it really do what it claims\? "
        r"Try to break it, in order to fix it",
}

#: The old two-stance description of a review, which the templates used to open
#: with. The shared vocabulary patterns above cover the External wording.
_TEMPLATE_FORBIDDEN = {
    **_FORBIDDEN,
    "internal-review-strengthens-the-change":
        r"internal review strengthens",
    "a-same-type-agent-in-an-independent-context-clears-the-floor":
        r"a same-type agent in an independent context",
    "a-plan-review-is-internal":
        r"a plan review is internal",
}
_TEMPLATE_FORBIDDEN_EXAMPLES = {
    **_FORBIDDEN_EXAMPLES,
    "internal-review-strengthens-the-change":
        "Internal review strengthens the change within the structure proposed.",
    "a-same-type-agent-in-an-independent-context-clears-the-floor":
        "Floor: a same-type agent in an independent context.",
    "a-plan-review-is-internal": "A plan review is Internal, fresh-context.",
}


def _template_obligations(rel: str) -> dict[str, str]:
    return (_PROPOSAL_TEMPLATE_OBLIGATIONS if rel in _PROPOSAL_TEMPLATES
            else _PLAN_TEMPLATE_OBLIGATIONS)


_TEMPLATE_CASES = [
    (rel, label) for rel in _TEMPLATE_FILES
    for label in sorted(_template_obligations(rel))
]
_TEMPLATE_CASE_IDS = [f"{label}-{_FILE_IDS[rel]}" for rel, label in _TEMPLATE_CASES]


def _section_from(text: str, heading_prefix: str) -> str:
    """The body of the `## <heading_prefix>...` section, to the next `## `."""
    match = re.search(rf"^## {re.escape(heading_prefix)}[^\n]*$(.*?)(?=^## |\Z)",
                      text, re.M | re.S)
    assert match, f"no '## {heading_prefix}' section"
    return match.group(1)


def _lines_starting(text: str, prefix: str) -> list[str]:
    return [line.strip() for line in text.splitlines()
            if line.strip().startswith(prefix)]


@pytest.mark.parametrize("rel,label", _TEMPLATE_CASES, ids=_TEMPLATE_CASE_IDS)
def test_template_review_section_carries_the_obligation(rel: str, label: str) -> None:
    obligations = _template_obligations(rel)
    review = _section(_text(rel), "Review")
    assert label not in _missing(review, obligations), (
        f"{rel} no longer carries {label!r} in its Review section. An author "
        f"reads this template while writing, and a reviewer while reviewing; "
        f"AGENTS.md alone is not where either looks.")


@pytest.mark.parametrize("rel,label", _TEMPLATE_CASES, ids=_TEMPLATE_CASE_IDS)
def test_removing_a_template_obligation_is_reported(rel: str, label: str) -> None:
    obligations = _template_obligations(rel)
    review = _section(_text(rel), "Review")
    assert _missing(review, obligations) == [], (
        f"{rel}: the unmutated Review section is missing obligations; no control.")
    stripped = re.sub(obligations[label], "", _normalize(review))
    assert label in _missing(stripped, obligations)


@pytest.mark.parametrize("rel", _TEMPLATE_FILES, ids=_FILE_IDS.get)
def test_template_omits_the_old_vocabulary(rel: str) -> None:
    found = _present(_text(rel), _TEMPLATE_FORBIDDEN)
    assert not found, f"{rel} {_FORBIDDEN_REASON} Found: {found}"


@pytest.mark.parametrize("rel", _TEMPLATE_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_TEMPLATE_FORBIDDEN))
def test_inserting_the_old_wording_into_a_template_is_reported(
        label: str, rel: str) -> None:
    intact = _text(rel)
    assert _present(intact, _TEMPLATE_FORBIDDEN) == [], (
        f"{rel}: the unmutated template already carries old wording; no control.")
    mutant = f"{intact}\n\n{_TEMPLATE_FORBIDDEN_EXAMPLES[label]}\n"
    assert label in _present(mutant, _TEMPLATE_FORBIDDEN)


@pytest.mark.parametrize("rel", _PROPOSAL_TEMPLATES, ids=_FILE_IDS.get)
def test_proposal_header_offers_only_usual_values(rel: str) -> None:
    """The Review line records the one decision it still carries.

    `usual` and `usual + Security Review` only. A header that offered a kind of
    review would let an agent pick one; the word `standard` is not used because
    it already names the lifecycle's lane.
    """
    text = _text(rel)
    review_lines = _lines_starting(text, "**Review**:")
    assert review_lines == ["**Review**: {{usual | usual + Security Review}}"]
    tier_lines = [l for l in _lines_starting(text, "**Tier**:")
                  if "External" not in l]
    assert tier_lines == ["**Tier**: {{usual | Security Review}}"]
    assert not any("standard" in l.lower() for l in review_lines + tier_lines)
    # The Plan review line keeps the tokens it has always been ruled by.
    assert _lines_starting(text, "**Plan review**:")[0].startswith(
        "**Plan review**: {{required(Internal) | required(Internal + "
        "Internal Security Review)}}")


@pytest.mark.parametrize("rel", _PLAN_TEMPLATES, ids=_FILE_IDS.get)
def test_plan_templates_keep_their_ruled_review_tokens(rel: str) -> None:
    text = _text(rel)
    assert _lines_starting(text, "**Plan review**:") == [
        "**Plan review**: {{required(Internal) | required(Internal + "
        "Internal Security Review)}}"]
    assert "**Tier**: <Internal | Internal Security Review>" in text
    assert not any("standard" in l.lower()
                   for l in _lines_starting(text, "**Tier**:"))


@pytest.mark.parametrize("rel", _TEMPLATE_FILES, ids=_FILE_IDS.get)
def test_a_template_offers_external_only_beside_called_by(rel: str) -> None:
    lines = [l.strip() for l in _text(rel).splitlines()]
    external = [i for i, l in enumerate(lines) if l == "**Tier**: External"]
    assert external, f"{rel} shows no way to record a called read"
    for i in external:
        following = next((l for l in lines[i + 1:] if l), "")
        assert following == "**Called by**: Maintainer -- Decision at <commit>", (
            f"{rel}: a Tier: External line is not followed by the Called by "
            f"line that says where the Maintainer's words live.")


@pytest.mark.parametrize("rel", _PROPOSAL_TEMPLATES, ids=_FILE_IDS.get)
def test_proposal_pass_skeleton_asks_the_proposal_questions(rel: str) -> None:
    skeleton = _normalize(_section_from(_text(rel), "Review --"))
    assert re.search(r"Should this happen as framed\? \{\{should this exist as "
                     r"framed", skeleton)
    assert "Best alternative." in skeleton
    assert "What would show it wrong." in skeleton


@pytest.mark.parametrize("rel", _PLAN_TEMPLATES, ids=_FILE_IDS.get)
def test_plan_pass_skeletons_ask_the_plan_and_code_questions(rel: str) -> None:
    text = _text(rel)
    plan = _normalize(_section_from(text, "Plan review --"))
    assert re.search(r"Should this happen as framed\? <the Decision settled "
                     r"the premise; does the plan deliver it>", plan)
    code = _normalize(_section_from(text, "Code review --"))
    assert re.search(r"Should this happen as framed\? <does it really do what "
                     r"it claims; try to break it, in order to fix it>", code)
    assert "see the falsification ledger" in code
    assert re.search(r"floor is not the implementing agent", code), (
        f"{rel}: the Code review skeleton lost the floor.")


@pytest.mark.parametrize("rel", _TEMPLATE_FILES, ids=_FILE_IDS.get)
def test_a_template_has_no_coverage_line_stanza(rel: str) -> None:
    """The coverage line is defined once, in the review-loop document.

    A scaffold that restated it would be a second definition to keep in step.
    """
    assert "Not covered" not in _text(rel)
    assert "Foundations" in _text(rel), "control: the template is the right file"


# Mutants: delete one sentence from one template and a named check goes red.

@pytest.mark.parametrize("rel", _PROPOSAL_TEMPLATES, ids=_FILE_IDS.get)
def test_deleting_the_two_pass_sentence_from_a_proposal_template_is_reported(
        rel: str) -> None:
    review = _section(_text(rel), "Review")
    obligations = _PROPOSAL_TEMPLATE_OBLIGATIONS
    assert _missing(review, obligations) == []
    mutant = _delete_sentence(review, "means two passes")
    assert "usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second" \
        in _missing(mutant, obligations)


@pytest.mark.parametrize("rel", _PLAN_TEMPLATES, ids=_FILE_IDS.get)
def test_deleting_the_obligation_sentence_from_a_plan_template_is_reported(
        rel: str) -> None:
    review = _section(_text(rel), "Review")
    obligations = _PLAN_TEMPLATE_OBLIGATIONS
    assert _missing(review, obligations) == []
    mutant = _delete_sentence(review, "calls for security treatment declares")
    assert "a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line" \
        in _missing(mutant, obligations)


# --------------------------------------------------------------------------
# The rest of the shipped text: the collaboration agreement, the capability
# floors, the security-review module, the legacy profile, the session-start
# skill, the fidelity manifest's sample roster, and two pages that describe
# the review module and a contributor's review duty.
# --------------------------------------------------------------------------

SHIPPED_AGREEMENT = "templates/core/dev/collaboration_agreement.md"
OWN_AGREEMENT = "dev/collaboration_agreement.md"
SHIPPED_MODEL = "templates/modules/team-gated/model-selection.md"
OWN_MODEL = "dev/modules/model-selection.md"
SHIPPED_SECURITY = "templates/modules/team-gated/security-review.md"
OWN_SECURITY = "dev/modules/security-review.md"
LEGACY_PROFILE = "templates/phase-0/project-profile-legacy.md"
SHIPPED_SKILL = "templates/skills/session-start/SKILL.md"
OWN_SKILL = ".agents/skills/session-start/SKILL.md"
FIDELITY = "bootstrap/fidelity-check.md"
MODULES_README = "templates/modules/README.md"
CONTRIBUTING = "templates/optional/CONTRIBUTING.md"

_REST_FILES = (
    SHIPPED_AGREEMENT, OWN_AGREEMENT, SHIPPED_MODEL, OWN_MODEL, SHIPPED_SECURITY,
    OWN_SECURITY, LEGACY_PROFILE, SHIPPED_SKILL, OWN_SKILL, FIDELITY,
    MODULES_README, CONTRIBUTING,
)
_REST_IDS = {
    SHIPPED_AGREEMENT: "shipped-agreement", OWN_AGREEMENT: "own-agreement",
    SHIPPED_MODEL: "shipped-model", OWN_MODEL: "own-model",
    SHIPPED_SECURITY: "shipped-security", OWN_SECURITY: "own-security",
    LEGACY_PROFILE: "legacy-profile", SHIPPED_SKILL: "shipped-skill",
    OWN_SKILL: "own-skill", FIDELITY: "fidelity", MODULES_README: "modules-readme",
    CONTRIBUTING: "contributing",
}

#: Wording specific to these files that must not return. Each is the old
#: sentence or phrase, so the check fires on the wording that was removed.
_REST_FORBIDDEN = {
    **_FORBIDDEN,
    "a-different-agent-type-than-the-author":
        r"different agent type than the author",
    "a-structurally-independent-tier":
        r"structurally-independent tier",
    "reviewed-across-structural-independence":
        r"reviewed across structural independence",
    "a-constructive-internal-read-and-an-external-read":
        r"constructive internal read and",
    "internal-and-external-tiers":
        r"internal / external tiers",
    "a-review-tier-column":
        r"(plan-)?review tier,",
    "adversarial-premise-checking":
        r"adversarial premise",
    "a-different-model-family":
        r"different model famil",
    "the-diversity-within-tier-rule-applies":
        r"lets the diversity within tier rule",
}
_REST_FORBIDDEN_EXAMPLES = {
    **_FORBIDDEN_EXAMPLES,
    "a-different-agent-type-than-the-author":
        "External review is a read from a different agent type than the author.",
    "a-structurally-independent-tier":
        "The module adds the second, structurally-independent tier.",
    "reviewed-across-structural-independence":
        "It was reviewed across structural independence.",
    "a-constructive-internal-read-and-an-external-read":
        "A constructive internal read and, for some changes, an external read.",
    "internal-and-external-tiers":
        "The Internal / External tiers, the proposal-first lifecycle.",
    "a-review-tier-column":
        "Its fields: status, review tier, plan-review tier, opened date.",
    "adversarial-premise-checking":
        "Security Review, adversarial premise-checking, and novel design.",
    "a-different-model-family":
        "The reviewer is architecturally diverse (a different model family).",
    "the-diversity-within-tier-rule-applies":
        "This is what lets the diversity within tier rule apply.",
}

_FILE_OBLIGATIONS = {
    SHIPPED_AGREEMENT: {
        "review-honesty-questions-foundations":
            r"A reviewer improves a change by questioning its foundations",
    },
    OWN_AGREEMENT: {
        "review-honesty-questions-foundations":
            r"A reviewer improves a change by questioning its foundations",
        "the-roster-slot-states-the-teams-shape-only":
            r"More than one agent type works the tree\. Agents propose, review, "
            r"implement, and advise; they do not decide",
    },
    SHIPPED_MODEL: {},  # the capability-floor obligations are checked below
    OWN_MODEL: {},
    SHIPPED_SECURITY: {
        "the-reviewer-surfaces-the-list-the-author-decides":
            r"The reviewer surfaces the list; the author decides what to act on",
    },
    OWN_SECURITY: {
        "the-reviewer-surfaces-the-list-the-author-decides":
            r"The reviewer surfaces the list; the author decides what to act on",
    },
    LEGACY_PROFILE: {
        "peer-review-gates-are-a-fresh-reviewer-at-every-stage":
            r"peer-review gates — a fresh reviewer at every stage",
    },
    SHIPPED_SKILL: {
        "the-board-columns-are-named-by-what-they-are":
            r"status, the Review line, the Plan review line, opened date",
    },
    OWN_SKILL: {
        "the-board-columns-are-named-by-what-they-are":
            r"status, the Review line, the Plan review line, opened date",
    },
    FIDELITY: {},
    MODULES_README: {
        "the-kernel-review-is-a-fresh-reviewer-who-did-not-write-the-work":
            r"a fresh reviewer who did not write the work — runs without the "
            r"dual-review module",
        "the-module-adds-guidance-for-staffing-a-called-read":
            r"staffing a read the Maintainer has called",
    },
    CONTRIBUTING: {
        "a-change-is-reviewed-by-an-independent-reviewer-beside-its-author":
            r"reviewed by an independent reviewer beside its author",
        "every-change-is-reviewed-by-a-fresh-reviewer-who-did-not-write-it":
            r"reviewed by a fresh reviewer who did not write it",
        "the-maintainer-may-ask-for-more-distance-on-one-named-piece-of-work":
            r"The Maintainer may ask for more distance on one named piece of work",
    },
}

#: The capability floors, in both copies of the model-selection module.
_MODEL_OBLIGATIONS = {
    "proposal-review-floor-is-high":
        r"\| Proposal review \| high \| The premise is still movable, and a "
        r"wrong one is cheapest to catch here\. \|",
    "plan-review-floor-is-medium":
        r"\| Plan review \| medium \|",
    "code-review-floor-is-medium-and-not-the-implementing-agent":
        r"\| Code review \| medium \| Floor is .not the implementing agent.",
    "security-review-floor-is-high":
        r"\| Security Review \| high \|",
    "cleanup-may-be-written-at-low":
        r"Docstring and comment cleanup, and related edits, may be written at "
        r"low\. This covers an edit that changes only docstrings, comments and "
        r"other non-executable wording: no executable token, and no bytes that "
        r"a test, manifest or attestation pins\. It lowers the writing step "
        r"only\.",
    "cleanup-keeps-the-reviews-stage-floor":
        r"The review keeps its stage's floor \(medium for code review\)",
    "cleanup-on-a-high-risk-surface-still-owes-its-security-review":
        r"it also owes the Security Review that surface already requires, at "
        r"high\. Nothing in this row lowers a review or removes a Security "
        r"Review",
    "the-cost-rule-check-is-not-a-review":
        r"The cost rule's check is not a review\. An orchestrator may run a "
        r"sub-agent's generative step on a cheaper model only when the model "
        r"that checks the output is at a tier strictly above it and is a "
        r"different model architecture; a stronger model from the same maker "
        r"is not one\. The check is the orchestrator's\. It is never filed as "
        r"a proposal, plan or code review pass and never counts toward one, "
        r"and no lifecycle review requires a different architecture\.",
    "the-data-governance-gate-applies-first":
        r"crosses the data-governance gate below, so that gate applies first",
    "condition-a-is-a-different-model-architecture":
        r"\(a\) the model that checks the output is at a tier strictly above "
        r"the downshifted author and is a different model architecture",
    "conditions-b-c-and-d-are-unchanged":
        r"\(b\) acceptance criteria are pre-declared; \(c\) the output is "
        r"falsifiable without trusting the author.{0,120}\(d\) a failed "
        r"review escalates the next attempt",
    "the-exclusion-list-is-unchanged":
        r"This does not apply to scientific assumptions, security-sensitive "
        r"changes, architecture decisions, irreversible migrations, or large "
        r"/ diffuse edits a reviewer would have to re-derive to check",
    "bright-line-keeps-the-high-risk-trust-boundaries":
        r"Security Review, the high-risk trust boundaries, premise-checking, "
        r"and genuinely novel design stay at the high floor",
    "the-cleanup-row-is-the-only-exception-and-only-for-the-writing-step":
        r"The one exception is the docstring-and-comment cleanup row above, "
        r"and only for its writing step",
    "diversity-within-tier-is-distance-on-request-not-a-default":
        r"Diversity within a tier \(doctrine/roles\.md\) is useful distance on "
        r"request, never a default an agent applies",
}


def _paragraph_after(text: str, lead: str) -> str:
    """The module paragraph (blockquote lines up to a blank one) starting at *lead*."""
    flat = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    start = flat.index(lead)
    return " ".join(flat[start:].split("\n\n", 1)[0].split())


def _rest_obligations(rel: str) -> dict[str, str]:
    return _MODEL_OBLIGATIONS if rel in (SHIPPED_MODEL, OWN_MODEL) \
        else _FILE_OBLIGATIONS[rel]


_REST_CASES = [(rel, label) for rel in _REST_FILES
               for label in sorted(_rest_obligations(rel))]
_REST_CASE_IDS = [f"{label}-{_REST_IDS[rel]}" for rel, label in _REST_CASES]


@pytest.mark.parametrize("rel,label", _REST_CASES, ids=_REST_CASE_IDS)
def test_shipped_text_carries_the_obligation(rel: str, label: str) -> None:
    obligations = _rest_obligations(rel)
    assert label not in _missing(_text(rel), obligations), (
        f"{rel} no longer carries {label!r}. This is text an adopter receives; "
        f"the doctrine holds the same rule but adopters never see doctrine/.")


@pytest.mark.parametrize("rel,label", _REST_CASES, ids=_REST_CASE_IDS)
def test_removing_a_shipped_text_obligation_is_reported(rel: str, label: str) -> None:
    obligations = _rest_obligations(rel)
    text = _text(rel)
    assert _missing(text, obligations) == [], (
        f"{rel}: the unmutated file is missing obligations; no control.")
    stripped = re.sub(obligations[label], "", _normalize(text))
    assert label in _missing(stripped, obligations)


@pytest.mark.parametrize("rel", _REST_FILES, ids=_REST_IDS.get)
def test_shipped_text_omits_the_old_wording(rel: str) -> None:
    found = _present(_text(rel), _REST_FORBIDDEN)
    assert not found, f"{rel} {_FORBIDDEN_REASON} Found: {found}"


@pytest.mark.parametrize("rel", _REST_FILES, ids=_REST_IDS.get)
@pytest.mark.parametrize("label", sorted(_REST_FORBIDDEN))
def test_inserting_old_wording_into_shipped_text_is_reported(
        label: str, rel: str) -> None:
    intact = _text(rel)
    assert _present(intact, _REST_FORBIDDEN) == [], (
        f"{rel}: the unmutated file already carries old wording; no control.")
    assert label in _present(f"{intact}\n\n{_REST_FORBIDDEN_EXAMPLES[label]}\n",
                             _REST_FORBIDDEN)


def test_the_model_selection_pair_is_byte_identical() -> None:
    """The installed copy is a verbatim copy of the shipped module."""
    assert _text(SHIPPED_MODEL) == _text(OWN_MODEL)
    assert _missing(_text(SHIPPED_MODEL), _MODEL_OBLIGATIONS) == []


def test_the_session_start_twins_are_byte_identical() -> None:
    assert _text(SHIPPED_SKILL) == _text(OWN_SKILL)
    assert _missing(_text(SHIPPED_SKILL),
                    _FILE_OBLIGATIONS[SHIPPED_SKILL]) == []


@pytest.mark.parametrize("rel", (SHIPPED_MODEL, OWN_MODEL), ids=_REST_IDS.get)
def test_the_cleanup_row_never_says_usual(rel: str) -> None:
    """`usual` is the header word for no Security Review, so the row that lowers
    only a writing step must not borrow it: read that way it would lower a review.
    """
    paragraph = _paragraph_after(_text(rel), "**Docstring and comment cleanup, "
                                              "and related edits, may be written")
    assert "stage's floor" in paragraph, "control: the paragraph was found"
    assert "usual" not in paragraph.lower()


@pytest.mark.parametrize("rel", (SHIPPED_MODEL, OWN_MODEL), ids=_REST_IDS.get)
def test_the_cleanup_row_sits_in_the_role_table(rel: str) -> None:
    row = [l for l in _text(rel).splitlines()
           if l.lstrip("> ").startswith("| Docstring and comment cleanup")]
    assert len(row) == 1 and "| low |" in row[0]
    assert "usual" not in row[0].lower()


@pytest.mark.parametrize("rel", (SHIPPED_MODEL, OWN_MODEL), ids=_REST_IDS.get)
def test_the_old_role_rows_are_gone(rel: str) -> None:
    rows = [l.lstrip("> ") for l in _text(rel).splitlines()]
    assert not any(l.startswith("| External Review") for l in rows)
    assert not any(l.startswith("| Internal Review") for l in rows)
    assert any(l.startswith("| Proposal review") for l in rows), (
        "control: the table has the new stage rows")


def _roster_names(text: str) -> list[str]:
    """Role names from the loop document's `## Team roles` bullets."""
    section = _section(text, "Team roles")
    return re.findall(r"(?m)^\* \*\*([^*]+)\*\*", section)


def _fidelity_roles() -> list[str]:
    match = re.search(r"(?m)^roles:\n((?:  - .+\n)+)", _text(FIDELITY))
    assert match, "no sample roster in the fidelity manifest"
    return [line[4:].strip() for line in match.group(1).splitlines()]


def test_the_fidelity_sample_roster_agrees_with_the_loop_document() -> None:
    """The manifest's sample is read by people deciding whether an install is
    faithful, so it must not describe roles the install does not have."""
    roster = _roster_names(_text(SHIPPED_LOOP))
    assert roster == ["Human Maintainer", "Strategy", "Implementation",
                      "Reviewer", "Security Review", "User Agent"]
    assert _fidelity_roles() == roster
    assert _roster_names(_text(OWN_LOOP)) == roster


def test_a_sample_roster_with_an_old_role_is_reported() -> None:
    """The comparison can fail: a roster that still lists the old role differs."""
    roster = _roster_names(_text(SHIPPED_LOOP))
    assert _fidelity_roles() == roster
    assert roster + ["External Reviewer"] != _fidelity_roles()

