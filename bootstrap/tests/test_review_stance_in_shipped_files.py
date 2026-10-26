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

The phrase pins below cannot detect every possible new sentence that grants
review authority. The broader Search B classification in the plan is a human
read to repeat when these carrier files change; green phrase pins alone do not
prove that no differently worded rule was added.

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

**Controls.** The independently located deletion probes first require the
unmutated file to be clean. The negative-pattern examples test one representative
file per pattern set; separate real-file checks cover every carrier. Removing a
pattern by applying that same pattern is not a useful control, so no such test
is counted as falsification.

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
    "no-agent-picks-a-kind-of-review":
        r"No agent picks a kind of review",
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
    "plan-review-is-fresh-context":
        r"A plan review is fresh-context",
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
        r"A roster the Maintainer sets \(which agent types work the tree\).{0,80}"
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
    "an-agent-may-name-a-risk-and-coverage-gap":
        r"It may name a risk and a gap in its coverage line",
    "a-called-read-adds-and-replaces-nothing":
        r"It adds to the usual review and replaces nothing",
    "a-called-brief-adds-focus-and-removes-no-owed-answer":
        r"Its brief may add focus; it removes no owed answer",
    "a-called-read-discharges-no-security-review-by-distance-or-brief":
        r"discharges no Security Review by its distance or its brief "
        r"\(a pass clears a Security Review only by being one\)",
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

#: The two module copies are under every phrasing pattern the carriers are, and
#: also may not bring back the clause that let a more distant pass stand in for
#: a falsification ledger, the "make it prove itself" stance, or a description
#: of the module as a second, structurally independent tier.
_MODULE_FORBIDDEN = {
    **_FORBIDDEN,
    "a-confirming-pass-never-stands-in-for-a-falsification-ledger":
        r"confirmed by a second independent different-agent-type pass",
    "make-it-prove-itself":
        r"make it prove itself",
    "a-structurally-independent-tier":
        r"structurally-independent (external )?tier|two-tier",
}
_MODULE_FORBIDDEN_EXAMPLES = {
    **_FORBIDDEN_EXAMPLES,
    "a-confirming-pass-never-stands-in-for-a-falsification-ledger":
        "It either carries a falsification ledger or is confirmed by a "
        "second independent different-agent-type pass.",
    "make-it-prove-itself":
        "The reviewer's stance is make it prove itself.",
    "a-structurally-independent-tier":
        "This module adds the second, structurally-independent tier.",
}

#: What the thinned module is now for, in the words an adopter reads.
_MODULE_OBLIGATIONS = {
    "the-module-is-for-staffing-a-read-the-maintainer-called":
        r"how a team with two agent types, or several people, staffs a read "
        r"the Maintainer has called",
    "agents-md-holds-the-one-definition-of-the-call":
        r"AGENTS\.md > .Review. holds the one definition of that call",
    "the-module-never-lets-an-agent-pick-a-reviewer":
        r"never lets an agent pick a reviewer or add a read",
    "the-sweep-and-the-trap-are-in-every-install":
        r"the one review, the sweep and the trap are in every install",
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
def test_plan_review_never_has_a_second_round(rel: str) -> None:
    """This rule lives in Lifecycle, outside the Review section."""
    lifecycle = _section(_text(rel), "The lifecycle")
    assert "Plan review never has a second round." in _normalize(lifecycle)


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


def test_team_roster_has_its_own_section_without_adding_roles() -> None:
    own = _section(_text(OWN_LOOP), "The team")
    shipped = _section(_text(SHIPPED_LOOP), "The team")
    own_flat = _normalize(own)
    assert "More than one agent type works the tree" in own_flat
    assert "they do not make the Decision" in own_flat
    assert "collaboration_agreement.md" not in own
    assert "<!-- cairn:slot team-roster -->" in shipped
    assert "The bootstrap records the team here" in shipped
    assert "<!-- cairn:end team-roster -->" in shipped
    assert "team-roster" not in _section(_text(SHIPPED_LOOP), "Team roles")


# --------------------------------------------------------------------------
# The old vocabulary stays out of the four carrier files.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", _CARRIER_FILES, ids=_FILE_IDS.get)
def test_carrier_omits_the_old_vocabulary(rel: str) -> None:
    found = _present(_text(rel), _FORBIDDEN)
    assert not found, f"{rel} {_FORBIDDEN_REASON} Found: {found}"


def test_carrier_forbidden_patterns_recognize_their_examples() -> None:
    intact = _text(SHIPPED_AGENTS)
    assert _present(intact, _FORBIDDEN) == []
    for label, example in _FORBIDDEN_EXAMPLES.items():
        assert label in _present(f"{intact}\n\n{example}\n", _FORBIDDEN), label


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
def test_module_omits_the_old_vocabulary(rel: str) -> None:
    found = _present(_text(rel), _MODULE_FORBIDDEN)
    assert not found, (
        f"{rel} {_FORBIDDEN_REASON} Found: {found}. The module is for staffing "
        f"a read the Maintainer has called; it selects no reviewer, and a "
        f"more distant pass never stands in for a falsification ledger.")


def test_module_forbidden_patterns_recognize_their_examples() -> None:
    intact = _text(SHIPPED_MODULE)
    assert _present(intact, _MODULE_FORBIDDEN) == []
    for label, example in _MODULE_FORBIDDEN_EXAMPLES.items():
        assert label in _present(f"{intact}\n\n{example}\n", _MODULE_FORBIDDEN), label


_MODULE_CASES = [(rel, label) for rel in _MODULE_FILES
                 for label in sorted(_MODULE_OBLIGATIONS)]
_MODULE_CASE_IDS = [f"{label}-{_FILE_IDS[rel]}" for rel, label in _MODULE_CASES]


@pytest.mark.parametrize("rel,label", _MODULE_CASES, ids=_MODULE_CASE_IDS)
def test_module_says_what_it_is_for(rel: str, label: str) -> None:
    assert label not in _missing(_text(rel), _MODULE_OBLIGATIONS), (
        f"{rel} no longer carries {label!r}.")


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
    "no-agent-picks-a-kind-of-review",
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
    "an-agent-may-name-a-risk-and-coverage-gap",
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
    "plan-review-is-fresh-context",
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


@pytest.mark.parametrize("rel", _TEMPLATE_FILES, ids=_FILE_IDS.get)
def test_template_omits_the_old_vocabulary(rel: str) -> None:
    found = _present(_text(rel), _TEMPLATE_FORBIDDEN)
    assert not found, f"{rel} {_FORBIDDEN_REASON} Found: {found}"


def test_template_forbidden_patterns_recognize_their_examples() -> None:
    intact = _text(SHIPPED_PROPOSAL)
    assert _present(intact, _TEMPLATE_FORBIDDEN) == []
    for label, example in _TEMPLATE_FORBIDDEN_EXAMPLES.items():
        assert label in _present(f"{intact}\n\n{example}\n",
                                 _TEMPLATE_FORBIDDEN), label


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


@pytest.mark.parametrize("rel", _PLAN_TEMPLATES, ids=_FILE_IDS.get)
def test_plan_review_skeleton_names_its_security_obligation(rel: str) -> None:
    skeleton = _section_from(_text(rel), "Plan review --")
    lines = [line.strip() for line in skeleton.splitlines()]
    assert "**Obligation**: <the one clause this pass clears>" in lines
    assert lines.index("**Obligation**: <the one clause this pass clears>") \
        < lines.index("**Tier**: <Internal | Internal Security Review>")


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
# The rest of the shipped text: the capability floors, the security-review
# module, the legacy profile, the session-start
# skill, the fidelity manifest's sample roster, and two pages that describe
# the review module and a contributor's review duty.
# --------------------------------------------------------------------------

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
    SHIPPED_MODEL, OWN_MODEL, SHIPPED_SECURITY,
    OWN_SECURITY, LEGACY_PROFILE, SHIPPED_SKILL, OWN_SKILL, FIDELITY,
    MODULES_README, CONTRIBUTING,
)
_REST_IDS = {
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
        r"that checks the output is at a tier strictly above it; a stronger "
        r"model from the same maker counts, and a model at the same tier does "
        r"not\. The check is the orchestrator's\. It is never filed as "
        r"a proposal, plan or code review pass and never counts toward one, "
        r"and no lifecycle review requires a different architecture\.",
    "the-data-governance-gate-applies-first":
        r"crosses the data-governance gate below, so that gate applies first",
    # The label keeps its old name so the node id does not change; the
    # pattern now pins condition (a) as stated: a stronger model from the same
    # maker counts, and the same tier does not.
    "condition-a-is-a-different-model-architecture":
        r"\(a\) the model that checks the output is at a tier strictly above "
        r"the downshifted author; a stronger model from the same maker counts, "
        r"and a model at the same tier does not",
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


@pytest.mark.parametrize("rel", _REST_FILES, ids=_REST_IDS.get)
def test_shipped_text_omits_the_old_wording(rel: str) -> None:
    found = _present(_text(rel), _REST_FORBIDDEN)
    assert not found, f"{rel} {_FORBIDDEN_REASON} Found: {found}"


def test_shipped_text_forbidden_patterns_recognize_their_examples() -> None:
    intact = _text(SHIPPED_MODEL)
    assert _present(intact, _REST_FORBIDDEN) == []
    for label, example in _REST_FORBIDDEN_EXAMPLES.items():
        assert label in _present(f"{intact}\n\n{example}\n", _REST_FORBIDDEN), label


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


# --------------------------------------------------------------------------
# The doctrine. Adopters never receive `doctrine/`, but the anchor, the
# standing call, the capability floors and the two privileges the old model
# carried are held here so the reasoning cannot drift from the shipped text.
# --------------------------------------------------------------------------

DOCTRINE_DUAL_REVIEW = "doctrine/dual-review.md"
DOCTRINE_PLANS = "doctrine/plans.md"
DOCTRINE_ROLES = "doctrine/roles.md"
DOCTRINE_RATIONALE = "doctrine/rationale.md"
DOCTRINE_LIFECYCLE = "doctrine/lifecycle.md"

#: The framework anchor's wording, as the Maintainer accepted it.
_ANCHOR_4 = (
    "The Dual-Review model. One review stance at every stage: a fresh "
    "reviewer, who did not write the work, on the work's side, who makes it "
    "better by questioning its foundations and answers in writing — should it "
    "exist as framed, what is the best alternative, what would show it wrong — "
    "executed asynchronously and commit-mediated (dual-review.md). It is a "
    "specialized variant of multi-agent debate (anchor 5) and a faithful "
    "instantiation of scientific peer review (anchor 6). Its sharpest point: "
    "independence is recorded, not claimed — every review names its reviewer, "
    "so how far that reviewer stood from the author is visible, and a "
    "different model architecture or a person is available whenever the "
    "Maintainer asks for more distance."
)

#: label -> (file, pattern): statements the doctrine must carry.
_DOCTRINE_OBLIGATIONS = {
    "one-standing-call-survives-and-it-is-the-maintainers": (
        DOCTRINE_DUAL_REVIEW,
        r"One standing call survives, and it is the Maintainer's\. The re-anchor "
        r"ceremony \(bootstrap/REANCHOR_RUNBOOK\.md\) requires its launcher to be "
        r"read by an External Security review\. The ceremony's own record sets "
        r"that requirement, the Maintainer chooses the reader each time, and no "
        r"agent selects or substitutes for it\. That review's record carries "
        r"Called by with the Maintainer's commissioning words, and it is a "
        r"Security Review: it clears the launcher obligation by being one, not "
        r"by its distance\. Nothing else in the procedure works this way"),
    "boundary-c-names-the-no-plan-accepted-proposal": (
        DOCTRINE_DUAL_REVIEW,
        r"a plan's Implementation verification section, or, where the "
        r"Maintainer asks for a review of a trivial change, its commit body"),
    "the-stage-questions-are-in-the-doctrine": (
        DOCTRINE_DUAL_REVIEW,
        r"Should this exist as framed\? Is there a better design, doing nothing "
        r"included\?.*?The Decision settled the premise\. Does the plan deliver "
        r"it\?.*?Does it really do what it claims\? Try to break it, in order "
        r"to fix it"),
    "a-clean-pass-with-evidenced-answers-does-not-deserve-skepticism": (
        DOCTRINE_DUAL_REVIEW,
        r"The thin clean pass deserves the skepticism; a clean pass whose three "
        r"answers are evidenced and whose gaps are named does not"),
    "the-sweep-and-the-trap-are-no-longer-team-gated": (
        DOCTRINE_DUAL_REVIEW,
        r"Every install receives the review sweep and the scope-reduction trap"
        r".{0,200}no longer team-gated"),
    "a-brief-may-state-the-stage-questions": (
        DOCTRINE_DUAL_REVIEW,
        r"A brief may state the stage's three questions"),
    "no-tool-reads-the-obligation-line": (
        DOCTRINE_DUAL_REVIEW,
        r"No tool reads that line: the next reviewer, the code reviewer and the "
        r"Maintainer check it"),
    "the-cost-rule-check-is-not-a-review": (
        DOCTRINE_ROLES,
        r"The cost rule's check is not a review\. An orchestrator may run a "
        r"sub-agent's generative step on a cheaper model only when the model "
        r"that checks the output is at a tier strictly above it; a stronger "
        r"model from the same maker counts, and a model at the same tier does "
        r"not\. The check is the orchestrator's\. It is never filed as "
        r"a proposal, plan or code review pass and never counts toward one, "
        r"and no lifecycle review requires a different architecture\. Sending "
        r"the context packet to a second maker's model crosses the "
        r"data-governance gate below, so that gate applies first"),
    "cleanup-may-be-written-at-low-and-no-review-is-lowered": (
        DOCTRINE_ROLES,
        r"Docstring and comment cleanup, and related edits, may be written at "
        r"low\..*?Nothing in this row lowers a review or removes a Security "
        r"Review"),
    "the-plan-obligation-is-cleared-only-by-a-matching-obligation-line": (
        DOCTRINE_LIFECYCLE,
        r"cleared only by an appended ## Plan review pass whose Obligation line "
        r"matches it, never by an ordinary pass"),
}

#: label -> (file, pattern, a string the pattern exists to keep out). The first
#: three are the privileges the old model carried: a more distant pass standing
#: in for evidence, and a more distant pass satisfying a required review.
_DOCTRINE_FORBIDDEN = {
    "a-confirming-second-different-agent-type-pass-clears-a-gate": (
        DOCTRINE_PLANS, r"confirming second different-agent-type pass",
        "Clears the gate with a falsification ledger or a confirming second "
        "different-agent-type pass."),
    "tier-ordering-lets-external-satisfy-a-required-internal": (
        DOCTRINE_PLANS, r"Tier ordering",
        "Tier ordering. Total order External > Internal."),
    "an-external-pass-satisfies-a-required-internal": (
        DOCTRINE_PLANS, r"External satisfies a required",
        "External satisfies a required Internal; Internal does not satisfy "
        "a required External."),
    "the-external-floor-lives-at-the-proposal": (
        DOCTRINE_DUAL_REVIEW, r"external floor",
        "The External floor on deliberate-lane proposal review."),
    "external-independence-lives-at-the-proposal": (
        DOCTRINE_DUAL_REVIEW, r"external independence",
        "External independence lives at the proposal."),
    "a-brief-narrows-the-pass": (
        DOCTRINE_DUAL_REVIEW, r"narrows the pass",
        "A try-to-kill brief narrows the pass to that."),
    "escalate-to-the-external-review-tier": (
        DOCTRINE_PLANS, r"escalate to the external",
        "Escalate to the External-review tier for scientific risk."),
    "recommended-wherever-it-can-be-staffed": (
        DOCTRINE_DUAL_REVIEW, r"recommended wherever it can be staffed",
        "A different agent type is recommended wherever it can be staffed."),
    "adversarial-premise-checking-in-the-bright-line-list": (
        DOCTRINE_ROLES, r"adversarial premise",
        "Bright-line work: Security Review, adversarial premise-checking."),
    "a-security-review-internal-record-satisfies-a-plan-obligation": (
        DOCTRINE_LIFECYCLE,
        r"satisfied only by an appended (## )?Security review \(Internal\)",
        "Satisfied only by an appended ## Security review (Internal) record."),
}

#: Files whose text a reader meets as live guidance, for the two repo-wide
#: greps below. Archives, records and the changelog are history.
_LIVE_ROOT_FILES = (SHIPPED_AGENTS, OWN_AGENTS, SHIPPED_LOOP, OWN_LOOP)
_LIVE_ROOT_DIRS = ("doctrine", "templates", "dev/modules", "docs", "dimensions")


def _live_files() -> list[str]:
    found = set(_LIVE_ROOT_FILES)
    for d in _LIVE_ROOT_DIRS:
        for path in (CAIRN_ROOT / d).rglob("*.md"):
            rel = path.relative_to(CAIRN_ROOT).as_posix()
            if "archive" not in rel.split("/"):
                found.add(rel)
    return sorted(found)


#: Headings that used to be cited and no longer exist anywhere; and the names
#: of a checker that was retired and so cannot be credited with reading a line.
_DANGLING = r"External Review Norms|Stage-to-role matrix|Review Expectations"
_RETIRED_CHECKER = (r"_pass_headings|normalize_required_obligations|"
                    r"the checker cannot parse")


def _doctrine_text(rel: str) -> str:
    return _normalize(_text(rel))


@pytest.mark.parametrize("label", sorted(_DOCTRINE_OBLIGATIONS))
def test_doctrine_carries_the_statement(label: str) -> None:
    rel, pattern = _DOCTRINE_OBLIGATIONS[label]
    assert re.search(pattern, _doctrine_text(rel)), (
        f"{rel} no longer carries {label!r}.")


@pytest.mark.parametrize("label", sorted(_DOCTRINE_FORBIDDEN))
def test_doctrine_omits_the_retired_privilege(label: str) -> None:
    rel, pattern, _example = _DOCTRINE_FORBIDDEN[label]
    assert not re.search(pattern, _doctrine_text(rel), re.IGNORECASE), (
        f"{rel} carries {label!r}. A more distant pass may inform a decision; "
        f"it may not stand in for evidence or satisfy a required review.")


@pytest.mark.parametrize("label", sorted(_DOCTRINE_FORBIDDEN))
def test_putting_a_retired_privilege_back_is_reported(label: str) -> None:
    rel, pattern, example = _DOCTRINE_FORBIDDEN[label]
    intact = _doctrine_text(rel)
    for other, (other_rel, other_pattern, _) in _DOCTRINE_FORBIDDEN.items():
        if other_rel == rel:
            assert not re.search(other_pattern, intact, re.IGNORECASE), (
                f"{rel}: the unmutated file already carries {other!r}.")
    assert re.search(pattern, f"{intact} {_normalize(example)}", re.IGNORECASE)


def test_the_anchor_equals_the_approved_wording() -> None:
    text = _doctrine_text(DOCTRINE_RATIONALE)
    start = text.index("The Dual-Review model. One review stance")
    end = text.index("Stigmergy as a deliberate choice", start)
    assert text[start:end].strip() == _ANCHOR_4, (
        "framework anchor 4 differs from the wording the Maintainer accepted.")


def test_a_reworded_anchor_is_reported() -> None:
    assert _ANCHOR_4.replace("recorded, not claimed", "recorded and claimed") \
        != _ANCHOR_4
    text = _doctrine_text(DOCTRINE_RATIONALE)
    assert _ANCHOR_4 in text, "control: the unmutated anchor is present"
    assert _ANCHOR_4.replace("recorded, not claimed", "recorded and claimed") \
        not in text


def test_the_two_trap_headings_are_adjacent_and_in_order() -> None:
    headings = re.findall(r"(?m)^## (.+)$", _text(DOCTRINE_DUAL_REVIEW))
    clean = "Review expectations — the clean-pass trap"
    trap = "Review expectations — the scope-reduction trap"
    assert clean in headings and trap in headings
    assert headings.index(trap) == headings.index(clean) + 1


def test_no_live_document_cites_a_heading_that_does_not_exist() -> None:
    hits = [rel for rel in _live_files()
            if re.search(_DANGLING, _text(rel))]
    assert hits == [], f"dangling heading cited in {hits}"
    # Confirm the instrument: it reads above zero where the headings are quoted.
    assert re.search(_DANGLING, "see External Review Norms")


def test_no_live_document_credits_a_checker_that_does_not_exist() -> None:
    hits = [rel for rel in _live_files()
            if re.search(_RETIRED_CHECKER, _text(rel))]
    assert hits == [], (
        f"{hits} name a checker that was retired. Nothing mechanical reads the "
        f"obligation line; the next reviewer and the Maintainer do.")
    assert re.search(_RETIRED_CHECKER, "the _pass_headings parser")


# --------------------------------------------------------------------------
# The dimensions pages, and the upgrade guide's plan-pass example. The pages
# say what each axis position drives. None of them may say a review "tier" is
# reserved, mandatory, wanted or filled: there is one review, and more distance
# is the Maintainer's call.
# --------------------------------------------------------------------------

DIM_COMPLEXITY = "dimensions/complexity.md"
DIM_README = "dimensions/README.md"
DIM_AGENT_TEAM = "dimensions/agent-team.md"
DIM_HUMAN_TEAM = "dimensions/human-team.md"
UPGRADE_GUIDE = "bootstrap/UPGRADE.md"
_DIM_FILES = (DIM_COMPLEXITY, DIM_README, DIM_AGENT_TEAM, DIM_HUMAN_TEAM)
_DIM_IDS = {DIM_COMPLEXITY: "complexity", DIM_README: "dimensions-readme",
            DIM_AGENT_TEAM: "agent-team", DIM_HUMAN_TEAM: "human-team",
            UPGRADE_GUIDE: "upgrade-guide"}

_DIM_FORBIDDEN = {
    **_FORBIDDEN,
    "external-review-is-reserved": r"reserved for genuinely",
    "external-review-is-mandatory": r"(review|tier) is mandatory",
    "the-make-it-prove-itself-tier": r"make-it-prove-itself",
    "the-two-tier-apparatus": r"two-tier",
    "the-review-tiers-still-hold": r"review tiers",
    "a-tier-the-agent-team-fills": r"tiers are filled",
    "a-tier-wanting-structural-independence": r"independence the external",
}
_DIM_FORBIDDEN_EXAMPLES = {
    **_FORBIDDEN_EXAMPLES,
    "external-review-is-reserved":
        "External review is reserved for genuinely contract-touching changes.",
    "external-review-is-mandatory": "External review is mandatory for a contract.",
    "the-make-it-prove-itself-tier": "The make-it-prove-itself tier is not optional.",
    "the-two-tier-apparatus": "The full two-tier Dual-Review apparatus.",
    "the-review-tiers-still-hold": "The review tiers still hold, filled by time.",
    "a-tier-the-agent-team-fills": "The review tiers are filled by the agent team.",
    "a-tier-wanting-structural-independence":
        "A different agent type supplies the independence the External tier wants.",
}

_DIM_OBLIGATIONS = {
    DIM_COMPLEXITY: {
        "simple-has-the-one-review-with-a-thinner-evidence-plan":
            r"The one review \(AGENTS\.md > .Review.\) asks the same three "
            r"questions here as anywhere, of a thinner evidence / verification "
            r"plan in each proposal",
        "complex-has-the-one-review-with-the-scientific-trust-lens":
            r"The one review carries the scientific-trust lens \(Domain / "
            r"scientific validity & scope, in the review sweep\)",
        "complex-proposal-names-the-contracts-and-assumptions-it-touches":
            r"a proposal names the contracts and scientific assumptions it "
            r"touches, so the Maintainer sees them before deciding",
        "complex-no-agent-adds-a-more-distant-read":
            r"No agent adds a more distant read on its own",
        "complex-keeps-the-independent-scientific-check":
            r"independent scientific check is expected of every change that "
            r"touches a scientific assumption",
    },
    DIM_README: {
        "the-complexity-cell-is-review-weight-and-verification-depth":
            r"Review weight and verification depth — how thin or thick the "
            r"evidence plan is, whether an unexplained .N/A. on the independent "
            r"scientific check is a review finding",
        "the-team-gated-bullet-says-what-the-module-adds":
            r"staffing guidance for a read the Maintainer has called, in the "
            r"Dual-Review module",
        "the-agent-team-cell-names-who-can-be-the-one-reviewer":
            r"who is available to be the one reviewer",
    },
    DIM_AGENT_TEAM: {
        "a-single-agent-has-the-one-review-filled-by-time":
            r"The one review still holds, filled by time rather than by agent",
        "more-distance-is-staffable":
            r"More distance is staffable\. A different agent type is there for "
            r"a read the Maintainer calls",
    },
    DIM_HUMAN_TEAM: {
        "other-humans-are-available-to-be-the-one-reviewer":
            r"are available to be the one reviewer, or the reader the "
            r"Maintainer asks for",
    },
}


@pytest.mark.parametrize("rel", _DIM_FILES, ids=_DIM_IDS.get)
def test_dimensions_omit_the_old_wording(rel: str) -> None:
    found = _present(_text(rel), _DIM_FORBIDDEN)
    assert not found, f"{rel} {_FORBIDDEN_REASON} Found: {found}"


def test_dimensions_forbidden_patterns_recognize_their_examples() -> None:
    intact = _text(_DIM_FILES[0])
    assert _present(intact, _DIM_FORBIDDEN) == []
    for label, example in _DIM_FORBIDDEN_EXAMPLES.items():
        assert label in _present(f"{intact}\n\n{example}\n", _DIM_FORBIDDEN), label


_DIM_CASES = [(rel, label) for rel in _DIM_OBLIGATIONS
              for label in sorted(_DIM_OBLIGATIONS[rel])]
_DIM_CASE_IDS = [f"{label}-{_DIM_IDS[rel]}" for rel, label in _DIM_CASES]


@pytest.mark.parametrize("rel,label", _DIM_CASES, ids=_DIM_CASE_IDS)
def test_dimensions_page_carries_the_obligation(rel: str, label: str) -> None:
    assert label not in _missing(_text(rel), _DIM_OBLIGATIONS[rel]), (
        f"{rel} no longer carries {label!r}.")


def test_the_complexity_cell_still_names_the_scientific_check() -> None:
    """Plan D asks the reworded cell to keep naming the check."""
    cell = [l for l in _text(DIM_README).splitlines()
            if l.startswith("| **Complexity**")]
    assert len(cell) == 1 and "independent scientific check" in cell[0]


def test_the_upgrade_guides_plan_pass_examples_are_not_external() -> None:
    """Only the two example rows changed: they resolve to `internal`.

    The stale text around them describes a retired planner and is left as it
    was, so the negation example (`not External`) stays.
    """
    text = _normalize(_text(UPGRADE_GUIDE))
    assert re.search(r"required\(Internal, security lens\) and "
                     r"required\(Internal \+ Internal Security Review\) both "
                     r"resolve to internal", text)
    assert not re.search(r"required\(External, security lens\)", text)
    assert not re.search(r"required\(External \+ External Security Review\)", text)
    assert "required(not External) is a violation" in text


def test_putting_an_external_example_back_in_the_upgrade_guide_is_reported() -> None:
    text = _normalize(_text(UPGRADE_GUIDE))
    assert not re.search(r"required\(External \+ External Security Review\)", text)
    mutant = text + " required(External + External Security Review) resolves to external."
    assert re.search(r"required\(External \+ External Security Review\)", mutant)


# --------------------------------------------------------------------------
# The README and descriptive pages explain the review contract. Presentation
# may change without requiring a repeated sales pitch or a particular figure;
# readers must still learn who reviews and who chooses any additional read.
# --------------------------------------------------------------------------

README = "README.md"
FIGURE = "docs/assets/dual-review-independence.svg"
ONRAMP = "on-ramp/README.md"
DOCS_ONBOARDING = "docs/agent-team-onboarding.md"
INSTALLED_ONBOARDING = "dev/modules/onboarding/agent-team-onboarding.md"
DOCS_TOUR = "docs/dev-tour.md"
INSTALLED_TOUR = "dev/modules/onboarding/dev-tour.md"
DOCUMENTATION_PLAN = "docs/DOCUMENTATION_PLAN.md"
DOCUMENTATION_PLAN_TEMPLATE = "templates/modules/default-on/documentation_plan_template.md"

_DESCRIPTIVE_FILES = (
    README, "docs/glossary.md", "docs/vision.md", DOCS_ONBOARDING,
    INSTALLED_ONBOARDING, "docs/quickstart.md", "docs/workflow-role.md",
    "docs/getting-started.md", DOCS_TOUR, INSTALLED_TOUR, "docs/tool-usage.md",
    ONRAMP, DOCUMENTATION_PLAN, DOCUMENTATION_PLAN_TEMPLATE, FIGURE,
)
_DESC_IDS = {rel: re.sub(r"[^a-z0-9]+", "-", rel.lower()).strip("-")
             for rel in _DESCRIPTIVE_FILES}

#: Pin the contract, not its location, repetition count, or exact prose.
_README_OBLIGATIONS = {
    "reviewer-is-fresh-and-not-the-author":
        r"fresh reviewer who did not write the work|"
        r"reviewer who did not author the change, working in a fresh session",
    "a-fresh-session-of-the-same-tool-is-enough":
        r"A fresh session of the same AI tool is sufficient|"
        r"The same tool can review in a fresh session",
    "the-maintainer-chooses-additional-distance":
        r"The Maintainer can request another model or a person for a particular review|"
        r"An additional model or human review is the Maintainer's choice",
    "review-author-and-evidence-are-recorded":
        r"Each review records who wrote it and the evidence it considered|"
        r"Reviews name their author and the evidence reviewed",
}

#: Literal sentences locate independent deletion controls and alternate wording.
#: Do not derive either from the obligation regex under test.
_README_WORDING_VARIANTS = {
    "reviewer-is-fresh-and-not-the-author": (
        "Review is by a fresh reviewer who did not write the work.",
        "Review is by a reviewer who did not author the change, working in a fresh session.",
    ),
    "a-fresh-session-of-the-same-tool-is-enough": (
        "A fresh session of the same AI tool is sufficient.",
        "The same tool can review in a fresh session.",
    ),
    "the-maintainer-chooses-additional-distance": (
        "The Maintainer can request another model or a person for a particular review.",
        "An additional model or human review is the Maintainer's choice.",
    ),
    "review-author-and-evidence-are-recorded": (
        "Each review records who wrote it and the evidence it considered.",
        "Reviews name their author and the evidence reviewed.",
    ),
}

#: Wording the descriptive pages must not carry: a review that has to come from
#: a different model or person, a tier, a floor, or the old two-stage picture.
_DESC_FORBIDDEN = {
    **_FORBIDDEN,
    "review-has-to-come-from-a-different-model-or-person":
        r"has to come from a different",
    "a-second-review-from-a-different-model":
        r"a second review from a",
    "independence-you-can-check-by-model-type":
        r"independence you can check",
    "two-review-tiers": r"two review tiers",
    "the-two-tier-description": r"two-tier",
    "the-second-tier": r"second tier",
    "a-review-tier": r"review[- ]tier",
    "structural-independence-tiers": r"structural-independence tiers",
    "a-reviewer-structurally-independent-of-the-author":
        r"structurally independent\*{0,2} of the author",
    "a-floor-of-a-different-agent-type":
        r"floor: a different agent type",
    "a-different-agent-type-or-a-human-as-the-floor":
        r"different agent type, or a human",
    "internal-review-as-a-kind":
        r"internal review",
    "structural-independence-as-process-content":
        r"structural independence, review norms",
    "a-second-reviewer-who-must-be-a-different-agent":
        r"a second reviewer \(a different agent",
}
_DESC_FORBIDDEN_EXAMPLES = {
    **_FORBIDDEN_EXAMPLES,
    "review-has-to-come-from-a-different-model-or-person":
        "The stronger review has to come from a different AI model.",
    "a-second-review-from-a-different-model":
        "A second review from a different AI model, or a person.",
    "independence-you-can-check-by-model-type":
        "Independence you can check: a different model.",
    "two-review-tiers": "Two review tiers: a first read and a stronger one.",
    "the-two-tier-description": "Two-tier review across structural independence.",
    "the-second-tier": "Higher-stakes changes get the second tier.",
    "a-review-tier": "Status, review tier, when it opened.",
    "structural-independence-tiers": "Changing the structural-independence tiers.",
    "a-reviewer-structurally-independent-of-the-author":
        "A reviewer structurally independent of the author.",
    "a-floor-of-a-different-agent-type":
        "Floor: a different agent type, or a human.",
    "a-different-agent-type-or-a-human-as-the-floor":
        "Needs a different agent type, or a human.",
    "internal-review-as-a-kind": "An Internal review helps a change land.",
    "structural-independence-as-process-content":
        "The process (roles, lifecycle, structural independence, review norms).",
    "a-second-reviewer-who-must-be-a-different-agent":
        "A second reviewer (a different agent, or a second human) appends it.",
}

_DESC_OBLIGATIONS = {
    "docs/glossary.md": {
        "review-is-one-stance-at-every-stage":
            r"Review — one stance at every stage: a fresh reviewer who did not "
            r"write the work",
        "a-called-read-is-the-maintainers-call":
            r"Called read — a review the Maintainer asked for on one named piece "
            r"of work, from more distance",
        "dual-review-is-an-independent-reviewer-beside-the-author":
            r"Dual-Review — an independent reviewer beside the author at every "
            r"stage, then the Maintainer's Decision",
        "structural-independence-is-recorded":
            r"every review names its reviewer, so how far they stood from the "
            r"author is on the record",
    },
    "docs/vision.md": {
        "the-vision-names-one-review-at-every-stage":
            r"The Dual-Review model — one review at every stage",
    },
    "docs/tool-usage.md": {
        "the-board-names-the-review-lines":
            r"status, the Review and Plan review lines, when it opened",
    },
    ONRAMP: {
        "more-distance-is-added-on-request":
            r"adds more distance whenever you ask for it; it is never required",
    },
}


@pytest.mark.parametrize("label", sorted(_README_OBLIGATIONS))
def test_readme_explains_the_review_contract(label: str) -> None:
    assert label not in _missing(_text(README), _README_OBLIGATIONS), (
        f"README.md no longer explains {label!r}.")


@pytest.mark.parametrize("label", sorted(_README_OBLIGATIONS))
def test_removing_a_readme_review_rule_is_detected(label: str) -> None:
    readme = _text(README)
    assert not _missing(readme, _README_OBLIGATIONS), "unmutated control"
    sentence, _ = _README_WORDING_VARIANTS[label]
    mutant = _delete_sentence(readme, sentence)
    assert mutant != readme
    assert label in _missing(mutant, _README_OBLIGATIONS)


@pytest.mark.parametrize("label", sorted(_README_OBLIGATIONS))
def test_equivalent_readme_wording_preserves_the_rule(label: str) -> None:
    readme = _normalize(_text(README))
    assert not _missing(readme, _README_OBLIGATIONS), "unmutated control"
    sentence, alternative = _README_WORDING_VARIANTS[label]
    assert readme.count(sentence) == 1, "literal sentence control"
    rewritten = readme.replace(sentence, alternative)
    assert rewritten != readme
    assert not _missing(rewritten, _README_OBLIGATIONS)


def test_the_review_figure_keeps_an_accessible_conclusion() -> None:
    import xml.etree.ElementTree as ET
    root = ET.fromstring(_text(FIGURE))
    ns = "{http://www.w3.org/2000/svg}"
    title = " ".join(root.find(ns + "title").text.split())
    desc = " ".join(root.find(ns + "desc").text.split())
    assert root.get("aria-labelledby") == "fig-title fig-desc"
    assert title.startswith("One review at every stage:")
    assert "reviewer who did not write the work" in title
    assert desc.startswith(title), "the description opens with the figure text"


def test_the_figure_parses_and_keeps_its_embed_geometry() -> None:
    import xml.etree.ElementTree as ET
    root = ET.fromstring(_text(FIGURE))
    assert root.get("viewBox") == "0 0 640 260"
    assert root.get("width") is None and root.get("height") is None


@pytest.mark.parametrize("phrase", [
    "two tiers", "Internal", "External", "different agent type or human"])
def test_the_figure_carries_no_old_phrase(phrase: str) -> None:
    assert phrase.lower() not in _text(FIGURE).lower(), (
        f"the figure still says {phrase!r}")


@pytest.mark.parametrize("rel", _DESCRIPTIVE_FILES, ids=_DESC_IDS.get)
def test_descriptive_page_omits_the_old_wording(rel: str) -> None:
    found = _present(_text(rel), _DESC_FORBIDDEN)
    assert not found, f"{rel} {_FORBIDDEN_REASON} Found: {found}"


def test_descriptive_forbidden_patterns_recognize_their_examples() -> None:
    intact = _text(_DESCRIPTIVE_FILES[0])
    assert _present(intact, _DESC_FORBIDDEN) == []
    for label, example in _DESC_FORBIDDEN_EXAMPLES.items():
        assert label in _present(f"{intact}\n\n{example}\n", _DESC_FORBIDDEN), label


_DESC_CASES = [(rel, label) for rel in _DESC_OBLIGATIONS
               for label in sorted(_DESC_OBLIGATIONS[rel])]
_DESC_CASE_IDS = [f"{label}-{_DESC_IDS[rel]}" for rel, label in _DESC_CASES]


@pytest.mark.parametrize("rel,label", _DESC_CASES, ids=_DESC_CASE_IDS)
def test_descriptive_page_carries_the_obligation(rel: str, label: str) -> None:
    assert label not in _missing(_text(rel), _DESC_OBLIGATIONS[rel]), (
        f"{rel} no longer carries {label!r}.")


@pytest.mark.parametrize("page,copy", [(DOCS_ONBOARDING, INSTALLED_ONBOARDING),
                                       (DOCS_TOUR, INSTALLED_TOUR)])
def test_an_installed_onboarding_copy_equals_its_page(page: str, copy: str) -> None:
    """Both pages reach every install that selects a preset, byte for byte."""
    assert _text(page) == _text(copy), (
        f"{copy} differs from {page}; they are one document in two places.")
    assert _present(_text(page), _DESC_FORBIDDEN) == []


def test_an_empty_carrier_satisfies_no_obligation_pattern() -> None:
    """A pattern matching an empty file would make its carrier pin vacuous."""
    groups = (
        _STANCE_OBLIGATIONS, _ROSTER_OBLIGATIONS, _MODULE_OBLIGATIONS,
        _PROPOSAL_TEMPLATE_OBLIGATIONS, _PLAN_TEMPLATE_OBLIGATIONS,
        _MODEL_OBLIGATIONS, *_FILE_OBLIGATIONS.values(),
        *_DIM_OBLIGATIONS.values(), *_DESC_OBLIGATIONS.values(),
    )
    for obligations in groups:
        assert set(_missing("", obligations)) == set(obligations), obligations


def test_a_copy_that_drifts_from_its_page_is_reported() -> None:
    page = _text(DOCS_ONBOARDING)
    assert page == _text(INSTALLED_ONBOARDING), "control: the pair is equal"
    assert page != page + " "


# --------------------------------------------------------------------------
# The onboarding presets and their installed copies. No preset may say that
# someone "fills" or "staffs" a review tier, and the two wordings an earlier,
# narrower guard existed to keep out stay out as literals. The earlier guard
# counted exactly three staffed paragraphs in one preset, which stopped being
# a property worth pinning once there is no tier to staff.
# --------------------------------------------------------------------------

PRESET_DIRS = ("templates/onboarding", "dev/modules/onboarding")
SHIPPED_PRESETS = ("templates/onboarding/solo-greenfield.md",
                   "templates/onboarding/collaborative-team.md",
                   "templates/onboarding/high-rigor-legacy.md")


def _preset_files() -> list[str]:
    """Every markdown file under the two preset folders, found by glob.

    A preset added later is therefore scanned without editing this list. The
    installed folder also holds the two onboarding pages that ship to every
    install, so those are scanned too.
    """
    found: list[str] = []
    for d in PRESET_DIRS:
        found.extend(path.relative_to(CAIRN_ROOT).as_posix()
                     for path in sorted((CAIRN_ROOT / d).glob("*.md")))
    return found


#: The two wordings the retired guard kept out of the solo preset, as literals.
_RETIRED_LITERALS = {
    "an-external-tier-currently-filled-by-a-fresh-session":
        "external tier (currently filled by fresh-session same-vendor review)",
    "a-fresh-session-external-review-tier":
        "fresh-session external review tier reproducible",
}
#: The full historic sentences the literals came out of. They are fixed strings,
#: not derived from the literals above, so inserting them into a real copy
#: tests the literals without taking the mutation from the pattern under test.
_RETIRED_SENTENCES = {
    "an-external-tier-currently-filled-by-a-fresh-session":
        "This strengthens Dual-Review's External tier (currently filled by "
        "fresh-session same-vendor review).",
    "a-fresh-session-external-review-tier":
        "The roster makes the fresh-session External review tier reproducible "
        "(the second session of your agent reviewing its own prior work).",
}
#: A sentence that names the review honestly and must not be flagged: it is the
#: shape the rewritten solo preset uses.
_CORRECT_SENTENCE = ("The roster makes the fresh-session review reproducible "
                     "-- real value, not a formality")


def _preset_flags(text: str) -> list[str]:
    flat = _normalize(text).lower()
    flags = _present(text, _FORBIDDEN)
    flags += [label for label, literal in _RETIRED_LITERALS.items()
              if literal in flat]
    return flags


def test_the_preset_glob_holds_every_shipped_preset() -> None:
    files = _preset_files()
    assert files, "the preset folders hold no markdown; the glob scans nothing"
    for preset in SHIPPED_PRESETS:
        assert preset in files, f"{preset} is missing from the preset glob"
    assert DOCS_ONBOARDING.replace("docs/", "dev/modules/onboarding/") in files


@pytest.mark.parametrize("rel", _preset_files(), ids=lambda r: r.replace("/", "-"))
def test_a_preset_names_no_review_tier_anyone_fills(rel: str) -> None:
    found = _preset_flags(_text(rel))
    assert not found, f"{rel} {_FORBIDDEN_REASON} Found: {found}"


@pytest.mark.parametrize("label", sorted(_RETIRED_LITERALS))
def test_each_retired_literal_matches_its_historic_sentence(label: str) -> None:
    """The literal is not vacuous: the sentence it came from contains it."""
    assert _preset_flags(_text(SHIPPED_PRESETS[0])) == []
    assert _RETIRED_LITERALS[label] in _normalize(_RETIRED_SENTENCES[label]).lower()


@pytest.mark.parametrize("rel", SHIPPED_PRESETS, ids=lambda r: r.split("/")[-1])
@pytest.mark.parametrize("label", sorted(_RETIRED_LITERALS))
def test_putting_a_retired_sentence_back_in_a_preset_is_reported(
        label: str, rel: str) -> None:
    """The control uses the whole historic sentence, not the literal's own text."""
    intact = _text(rel)
    assert _preset_flags(intact) == [], (
        f"{rel}: the unmutated preset is already flagged; no control.")
    assert label in _preset_flags(f"{intact}\n\n{_RETIRED_SENTENCES[label]}\n")


def test_a_correctly_worded_sentence_is_not_flagged() -> None:
    """The guard has no false positive on the shape the solo preset now uses."""
    solo = _normalize(_text(SHIPPED_PRESETS[0]))
    assert _CORRECT_SENTENCE in solo, "control: the sentence is in the preset"
    assert _preset_flags(_CORRECT_SENTENCE) == []


# --------------------------------------------------------------------------
# A placeholder written as one word between double braces is an install token
# to the engine. An upgrade plans a file that carries one the install never
# recorded as "needs a value", and the file never advances. So a mergeable
# template may carry such a placeholder only if it is a token the engine fills
# or one it knowingly leaves for the document's author. Prose placeholders in a
# template use angle brackets, or braces around more than one word.
# --------------------------------------------------------------------------

def _engine_token_rules():
    import sys
    sys.path.insert(0, str(CAIRN_ROOT))
    from bootstrap._scaffold.config import KNOWN_TOKENS
    from bootstrap._scaffold.slotmerge import find_unfilled_tokens
    return KNOWN_TOKENS, find_unfilled_tokens


def _mergeable_template_files() -> list[str]:
    """Every core template, plus Cairn's own copies of the two authoring ones."""
    core = sorted(p.relative_to(CAIRN_ROOT).as_posix()
                  for p in (CAIRN_ROOT / "templates" / "core").rglob("*")
                  if p.is_file() and p.suffix in {".md", ".yml", ".txt"})
    return core + [OWN_PROPOSAL, OWN_PLAN]


def _unknown_install_tokens(text: str) -> set[str]:
    known, unfilled = _engine_token_rules()
    return set(unfilled(text)) - set(known)


@pytest.mark.parametrize("rel", _mergeable_template_files(),
                         ids=lambda r: r.replace("/", "-"))
def test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill(
        rel: str) -> None:
    left = _unknown_install_tokens(_text(rel))
    assert not left, (
        f"{rel} carries {sorted(left)} between double braces. The engine reads "
        f"a one-word placeholder as an install token, so every adopter's "
        f"upgrade plans this file as needing a value and never advances it. "
        f"Write an angle-bracket placeholder instead.")


def test_the_mergeable_template_list_covers_the_authoring_templates() -> None:
    files = _mergeable_template_files()
    for rel in (SHIPPED_PROPOSAL, SHIPPED_PLAN, SHIPPED_AGENTS, SHIPPED_LOOP,
                OWN_PROPOSAL, OWN_PLAN):
        assert rel in files, f"{rel} is not scanned for one-word placeholders"
    assert len(files) > 10


@pytest.mark.parametrize("rel", _TEMPLATE_FILES, ids=_FILE_IDS.get)
def test_a_one_word_placeholder_in_an_authoring_template_is_reported(rel: str) -> None:
    """The guard can fail, and is not tripped by what the engine allows."""
    intact = _text(rel)
    assert _unknown_install_tokens(intact) == set(), (
        f"{rel}: the unmutated template already carries one; no control.")
    assert _unknown_install_tokens(f"{intact}\n1. Answer -- {{{{evidence}}}}\n") \
        == {"evidence"}
    allowed = "\n## Review -- {{reviewer}} -- {{YYYY-MM-DD}}\n{{project_name}}\n"
    assert _unknown_install_tokens(f"{intact}{allowed}") == set()


# --------------------------------------------------------------------------
# Completeness. Every pin above names its files, so a file nobody listed could
# bring the old phrasing back without turning anything red. This walks the same
# roots the phrasing search uses and requires that any file carrying a hit is
# in an explicit table of files that do not ship, each with its reason. A file
# an adopter receives can never be in that table: the table is for history and
# ceremony documents, not an exemption from the rule.
# --------------------------------------------------------------------------

_SEARCH_A_ROOT_FILES = (
    "AGENTS.md", "README.md", "dev/proposals/_template.md",
    "dev/plans/_template.md", "dev/agent_collaboration.md",
    "bootstrap/fidelity-check.md",
    "bootstrap/UPGRADE.md", "bootstrap/REANCHOR_RUNBOOK.md",
)
_SEARCH_A_ROOT_DIRS = ("doctrine", "templates", "dev/modules", "docs",
                       "dimensions", "on-ramp")
_SEARCH_A_SUFFIXES = {".md", ".yml", ".svg"}
#: The phrasing search the stance proposal pinned, as one pattern. It is checked
#: against emphasis-stripped, whitespace-collapsed text, case-insensitively.
_SEARCH_A = re.compile(
    r"required\(external"
    r"|external[ -](floor|tier|review|reviewer|independence|stance|code review)"
    r"|declared-external|a human fills|different-agent-type (pass|round)"
    r"|escalate to the external|External Review Norms",
    re.IGNORECASE)

#: Files with a hit that are not shipped as live guidance, and why. Every entry
#: must still carry a hit (a stale entry is reported), and none may be a file an
#: adopter receives.
_COMPLETENESS_EXEMPT = {
    "doctrine/lifecycle-contract.md":
        "history reference: one sentence, introduced by 'History:', about a "
        "plan-review tier that was retired",
}
_INSTALL_SET_PREFIXES = ("templates/", "dev/modules/")
_INSTALL_SET_FILES = frozenset(_AGENTS_FILES + _LOOP_FILES)


def _strip_for_search(text: str) -> str:
    return " ".join(re.sub(r"[*_`>]", "", text).split())


def _search_a_files(root: Path) -> dict[str, int]:
    """Search-A hit counts per file under *root*, archives excluded."""
    found: dict[str, int] = {}
    paths = [root / rel for rel in _SEARCH_A_ROOT_FILES]
    for d in _SEARCH_A_ROOT_DIRS:
        base = root / d
        if base.is_dir():
            paths.extend(p for p in sorted(base.rglob("*"))
                         if p.suffix in _SEARCH_A_SUFFIXES)
    for path in paths:
        rel = path.relative_to(root).as_posix()
        if not path.is_file() or "archive" in rel.split("/"):
            continue
        hits = len(_SEARCH_A.findall(_strip_for_search(
            path.read_text(encoding="utf-8", errors="replace"))))
        if hits:
            found[rel] = hits
    return found


def _unaccounted(hits: dict[str, int], exempt: dict[str, str]) -> list[str]:
    return sorted(set(hits) - set(exempt))


def _stale_exemptions(hits: dict[str, int], exempt: dict[str, str]) -> list[str]:
    return sorted(set(exempt) - set(hits))


def _exempt_install_files(exempt: dict[str, str]) -> list[str]:
    return sorted(rel for rel in exempt
                  if rel.startswith(_INSTALL_SET_PREFIXES)
                  or rel in _INSTALL_SET_FILES)


def test_every_file_with_a_phrasing_hit_is_exempt_for_a_reason() -> None:
    hits = _search_a_files(CAIRN_ROOT)
    assert not _unaccounted(hits, _COMPLETENESS_EXEMPT), (
        f"{_unaccounted(hits, _COMPLETENESS_EXEMPT)} carry the old phrasing and "
        f"are not scanned or exempt. Reword them; an exemption is only for a "
        f"file that does not ship.")


def test_no_exemption_is_stale() -> None:
    assert not _stale_exemptions(_search_a_files(CAIRN_ROOT), _COMPLETENESS_EXEMPT)


def test_no_file_an_adopter_receives_is_exempt() -> None:
    assert _exempt_install_files(_COMPLETENESS_EXEMPT) == []
    assert all(reason.strip() for reason in _COMPLETENESS_EXEMPT.values())


def test_removing_an_exemption_is_reported() -> None:
    hits = _search_a_files(CAIRN_ROOT)
    assert _unaccounted(hits, _COMPLETENESS_EXEMPT) == [], "control: all accounted"
    smaller = {k: v for k, v in _COMPLETENESS_EXEMPT.items()
               if k != "doctrine/lifecycle-contract.md"}
    assert _unaccounted(hits, smaller) == ["doctrine/lifecycle-contract.md"]


def test_a_phrase_inserted_into_a_scanned_copy_is_reported(tmp_path: Path) -> None:
    assert _unaccounted(_search_a_files(CAIRN_ROOT), _COMPLETENESS_EXEMPT) == []
    copy = tmp_path / "templates" / "core"
    copy.mkdir(parents=True)
    (copy / "AGENTS.md").write_text(_text(SHIPPED_AGENTS), encoding="utf-8")
    assert _search_a_files(tmp_path) == {}, "control: the unmutated copy is clean"
    (copy / "AGENTS.md").write_text(
        _text(SHIPPED_AGENTS) + "\nA human fills the External tier.\n",
        encoding="utf-8")
    assert _unaccounted(_search_a_files(tmp_path), _COMPLETENESS_EXEMPT) == [
        "templates/core/AGENTS.md"]


def test_exempting_an_installed_file_is_reported() -> None:
    assert _exempt_install_files(_COMPLETENESS_EXEMPT) == []
    for rel in (SHIPPED_AGENTS, OWN_MODULE, SHIPPED_PROPOSAL, SHIPPED_LOOP):
        assert _exempt_install_files({**_COMPLETENESS_EXEMPT, rel: "x"}) == [rel]


def test_the_walk_reaches_the_roots_it_claims() -> None:
    """Confirm the instrument: it finds a known hit and walks a known file."""
    assert _SEARCH_A.search("A human fills the External tier.")
    assert _search_a_files(CAIRN_ROOT).get("doctrine/lifecycle-contract.md", 0) >= 1
