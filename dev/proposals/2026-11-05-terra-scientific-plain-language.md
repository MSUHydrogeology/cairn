# Proposal: Plain language for technical and scientific writing

**Author**: Terra (Medium)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Clarify the writing rules so technical terms remain precise and scientific claims and citations say what was actually checked.

## Decision summary

Tighten four existing writing rules and clarify citation honesty without
adding a new rule or automated prose policing. Keep established technical
terms and compounds; identify model output as simulated rather than measured;
and disclose the limits of source checks in deliberation and result records.
The cost is a coordinated update to the standard's copies and version, plus
review of wording and existing install checks.

## Context

The current standard in `dev/agent_collaboration.md` asks writers to define
specialist terms and unpack stacked nouns (rule 5), but does not distinguish
an established compound from an opaque stack. Rule 13 distinguishes measured,
assumed and expected claims but does not name simulations. Rule 17 gives
first-person check disclosures under scientific and technical reasoning;
its scope could be mistaken for a requirement to put a work diary on a static
reference page. Rule 2 already excludes filler and vague praise, while rule
14 asks for a number's source. Neither explicitly addresses promotional
wording or the extent to which a cited source was read.

The [strategy](../strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md#part-3-the-specific-gaps-to-close-for-direct-use-in-assai)
identifies these risks; it says its cited citation-error research was checked
through abstracts and metadata, not full text. The strategy is evidence for
the proposal, not a new claim that its literature was independently verified
here. `docs/plain-language.md` now carries the rules and literature; the
strategy's older packaging gaps are not this proposal's work.

## Proposal

For v0.7, revise the existing numbered rules, preserving their numbers:

* **2:** exclude promotional wording when it adds no evidence; do not ban
  useful words merely because they appear on a list.
* **5:** retain standard domain and technical terms and established compounds;
  define unfamiliar or project-coined terms where first needed for the reader,
  and unpack noun stacks only when they obscure meaning.
* **13:** distinguish observed or measured results from simulated results,
  assumptions and expectations; do not present simulation as observation.
* **14/17:** cite sources actually checked for the claim; disclose when the
  check reached only an abstract or secondary account, and do not imply a
  full-text reading. If the primary source is unavailable, attribute the
  secondary account and state that limit rather than inventing a check.
* **17:** place relevant first-person disclosures of checks and limits in
  proposals, reviews, decisions and reports of results or deliberation. Static
  reference pages need accurate attribution and appropriate source limitations,
  not a first-person work diary.

Keep the standard's general writing-versus-artifact-template boundary. Update
its version and the existing changelog at the appropriate implementation
serialization point. The separate late-January 2027 evaluation remains with
the Maintainer and is not a prerequisite or part of this v0.7 outcome.

## Rationale

These are small clarifications to existing owners, not a new scientific
reporting protocol. Human reading remains the check: a word list would flag
legitimate technical terms and cannot establish citation support. The intended
gain is precision without adding a permanent enforcement tool.

## Alternatives considered

Leave the rules unchanged: no version or copy maintenance, but the ambiguity
around simulated results, compounds and partial source checks remains. A new
scanner or mandatory citation ledger would add ongoing maintenance and false
confidence without determining whether a source supports a claim; existing
review and source attribution are the proportionate choice.

## Documentation / doctrine surface

The governing writing standard lives in `dev/agent_collaboration.md` and its
shipped counterpart `templates/core/dev/agent_collaboration.md`; keep their
standard sections aligned. Update the reproduced standard and any affected
description in `docs/plain-language.md`. Check the existing pointer in
`AGENTS.md` and its shipped copy for consistency; change only if needed.
Follow the standard's version and changelog rule. These shipped templates are
protected surfaces, hence heavy tier and separate Security Review; no new
trust boundary or executable behavior is proposed.

## Evidence / verification plan

At implementation, map readers and byte pins for every changed file, then use
the existing path-scoped test selection and standing prose gates. A fresh
reviewer should examine examples of an established compound, an unfamiliar
coined term, a simulated value, an abstract-only citation and a static
reference page. The change fails if a reader must simplify a standard term,
mistakes a simulation for an observation, infers a full-text check that did
not happen, or must add a first-person diary to a reference page.

### Tests required

`bootstrap/tests/contract/test_writing_rules_ship.py` checks the installed
standard, source-copy agreement, numbered rules and version; update its
version expectation when the standard changes and exercise its real scaffold
install path. Search the other changed-file readers and pins at implementation
and run the resulting scoped selection. Add a test only for a plausible
uncovered failure, not to score prose or verify source meaning mechanically.

### Examples / smoke checks

Run the relevant claim, link, snippet and neutrality gates and
`python scripts/check_cairn.py`; inspect the installed standard and public
copy for consistency. The final change verification follows the applicable
wide Boundary B procedure for the protected template surface.

#### Security preflight

S1: The proposed change makes no automated admission or authorization decision;
writers and reviewers supply and assess prose and sources. S2: Existing copy
and install checks should fail if a standard copy or version expectation is
changed alone; verify the relevant mutations during implementation. S3: The
contract test invokes the scaffold on a fresh install; its exact selection and
coverage must be recorded at implementation, not claimed as measured here.
S4: No new default, parser or failure path is proposed. S5: A writer can still
misrepresent a source; human review cannot guarantee detection.

### Independent scientific check

N/A: no scientific assumption or result is changed; this changes how claims
are described, not a model or scientific finding.

## Signals the change is wrong

Withdraw or revise if review shows the wording weakens source honesty, loses
technical precision, burdens static reference pages with irrelevant disclosure,
or requires a new enforcement mechanism to work in practice.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance

## Review -- Codex Terra Medium -- 2026-11-05

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the bounded refinements preserve scientific precision and address source-check honesty without a new scanner; row 7b calls for these outcomes (`dev/PLANNING.md`, row 7b; proposal, Proposal and Rationale).
2. **Best alternative.** Leave the rules unchanged: it avoids copy and version maintenance, but rule 13 does not distinguish simulation from measurement and rule 5 unconditionally tells writers to unpack noun stacks (`dev/agent_collaboration.md`, rules 5 and 13).
3. **What would show it wrong?** An implementation example that forces a standard term to be simplified, a simulated value to appear observed, an abstract-only check to imply full-text reading, or a static reference page to become a work diary would warrant revision (proposal, Evidence / verification plan).

The proposal follows row 7b, including the separate late-January 2027 evaluation; it retains the writing-versus-template boundary identified in the cited strategy. The current standard already preserves field terms and scopes scientific reasoning to relevant records, so the benefit is clarification, not a new reporting protocol (`dev/agent_collaboration.md`, opening and rules 5, 13-17; strategy, Parts 1 and 3).

**Non-blocking:** The citation clause could be read as requiring a disclosure beside every citation, even when the limit cannot mislead the reader. During drafting, make the disclosure proportionate to the claim and avoid implying that an unchecked primary source supports it; an abstract-only and a secondary-source example would show the distinction. This preserves honesty without a recurring ledger (proposal, rules 14/17 and Rationale).

**Coverage:** Read the committed proposal, proposal template, row 7b, cited strategy and current standard, including the static-page boundary and human-reading check. Did not independently verify the strategy's literature, run install checks, or perform the separately owed Security Review.

## Review -- Codex Sol (Security Review) -- 2026-11-05

Reviewed commit: `36dc22b1`

**Model**: gpt-6.1-sol (high). **Tier**: Security Review.
**Findings**: none. **Verdict**: ACCEPT.
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the proposed wording strengthens source and simulation disclosures while leaving admission and authorization unchanged -- Proposal; `dev/agent_collaboration.md`, rules 13-17.
2. **Best alternative.** Keep version 1.0, avoiding copy maintenance but retaining the ambiguity between simulated and measured results -- Alternatives considered; `dev/agent_collaboration.md`, rule 13.
3. **What would show it wrong?** An installed copy that omits the clarification, or wording that implies a source was read beyond the actual abstract/secondary check, would defeat the benefit -- Evidence / verification plan; `bootstrap/tests/contract/test_writing_rules_ship.py`.

The security boundary is modest but real: these are protected shipped instructions that shape how agents report evidence. S1/S4 correctly claim no new executable gate, and S5 correctly says a dishonest writer can still misrepresent a source. Do not turn a prose test into a claim that citation meaning was verified. The proposed separate source-copy, installed-profile and version checks are appropriate for drift; the plan should make the source-only and shipped-only mutations go red. The ordinary review's proportionality advice is sound and does not require a new ledger.

**Coverage:** Committed proposal, current standard, installed-copy owner and stated limits. **Not covered:** independent literature verification, future wording, source-support accuracy, mutation execution, full suite or release/trust operations.
