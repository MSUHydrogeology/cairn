# Align model floors with the current team roster

**Author**: Codex gpt-6-sol (Proposal)
**Status**: awaiting-review
**Review**: usual
**Plan review**: required(Internal)
**Opened**: 2026-10-28
**In brief**: Set model capability floors by the work each agent does so routine reviews and planned implementation use the intended tiers.

## Context

The current tables put proposal review and Maintainer Decision scribing at high,
non-trivial implementation at medium, and only trivial implementation at low
(`doctrine/roles.md`; `dev/modules/model-selection.md`;
`templates/modules/team-gated/model-selection.md`). `AGENTS.md` still says
proposal review stays high. Cairn's own mapping has only three Claude-family
rows (`dev/.cairn/model-selection-mapping.yml`), although the roster uses
other families (`dev/agent_collaboration.md`). The October 27 team measurement
records routine review work already moving to medium
(`dev/strategy/2026-10-27-antigravity-lightweight-team-measurement.md`).

The Maintainer has now directed, in chat on October 28: “Go ahead and use Sol
for proposal reviews”; “That's what the doctrine should say”; “Astra is just
security reviews and strategy, rigt?”; “Luna can handle non-trivial
implementation as well”; and “Move Maintainer Decision scribing down to low”.
The later clarification was: “Current-generation low models are extremely
capable of implementing a plan.” These are direction to propose a durable
rule, not a Decision on this artifact.

## Proposal

Set the default floors to high for Strategy/Research, premise-checking, novel
design, Security Review and other existing bright-line work; medium for proposal
authoring and ordinary proposal, plan and code review; low for implementation
of reviewed plans, including non-trivial and deliberate chunks, trivial work,
and explicitly authorized Maintainer Decision scribing. The low implementation
floor applies by role, without a special bounded-work exception. A fresh code
reviewer still cannot be the implementer. Security obligations, data-governance
and tool-parity gates, independent checks for *below-floor* generative work, and
escalation after failed checks retain their force. The existing scribing rule
still requires unambiguous Maintainer instruction, an isolated verbatim quote
in the Decision and commit body, and an exclusive Decision commit.

Carry the same floors through Cairn's governing and shipped copies and its
model-selection module. In Cairn's local mapping, retain the existing
Claude-family rows while updating their task families, and add high/medium/low
Astra/Sol/Luna family rows. The mapping checker accepts a non-empty list and
does not enforce tier uniqueness (`scripts/check_model_selection.py`); the
module prose should explicitly permit one row per *model family and tier*,
including several vendors at a tier. Record the Maintainer's assignment as
such, dated, without presenting it as benchmark evidence. Model names stay in
the local mapping and deliberation record, not shipped doctrine or templates.

## Rationale

This makes the written defaults match the Maintainer's current judgment about
the models and the existing review separation. Planned implementation already
has reviewed acceptance criteria and a separate code review. The ordinary
review floor remains above the implementation floor; the exceptional
below-floor cost rule remains a separate opt-in mechanism. The October 27
multi-artifact team measurement supplies evidence for the Maintainer to judge
the doctrine rate-limit at Decision (`doctrine/rationale.md`); this proposal
does not claim a single-incident exception.

## Alternatives considered

Keep medium for non-trivial implementation and high for proposal review. That
preserves the old caution but conflicts with the Maintainer's stated staffing
choice and leaves the mapping unable to describe the active roster clearly.
Use the below-floor cost rule for each low-tier plan chunk instead. That treats
the intended default as an exception and adds needless per-chunk justification.

## Documentation / doctrine surface

The cross-cutting rule belongs in `doctrine/roles.md`, with the operational
summary in `AGENTS.md` and its shipped `templates/core/AGENTS.md` copy. Mirror
the table and task-type guidance in `dev/modules/model-selection.md` and
`templates/modules/team-gated/model-selection.md`; update the local mapping at
`dev/.cairn/model-selection-mapping.yml`. Any lifecycle prose describing these
floors or scribing should agree. No new tool feature or schema is proposed.

## Evidence / verification plan

Compare the role table, operational summary, shipped module and local mapping
against the five stated floors. Check that the final text still distinguishes
ordinary review from Security Review, and low default implementation from a
below-floor generative downshift. Falsification: any shipped table still
requires high for ordinary proposal review, medium for a reviewed plan chunk,
or high for Decision scribing; or the mapping loses a current family.

### Tests required

Update and run `bootstrap/tests/test_model_tier_rule_ships.py::test_proposal_authoring_is_medium_and_proposal_review_stays_high`
for the new property, plus its copy/install tests. Run
`bootstrap/tests/test_model_selection_stub.py::TestThisRepositorysMappingIsFilled::test_cairn_mapping_passes_with_and_without_pyyaml`.
Search for other tests that read touched
files and run those nodes. The plan will map them precisely.

### Examples / smoke checks

Run `python scripts/claim_check.py` on changed Markdown, `python
scripts/check_cairn.py` on changed Markdown, `python
scripts/quality_gate.py --sub neutrality --sub redundancy`, and `python
scripts/check_model_selection.py` on the filled mapping. Open each trigger to
confirm what it checks. The implementation plan determines Boundary B mode;
the full suite is reserved for a certifying run under `AGENTS.md`.

#### Security preflight

N/A: no trust boundary added, moved, or widened; existing Security Review and
data-governance floors remain.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Ordinary reviews begin missing premise defects, or low-tier planned work
regularly fails its independent code review and escalates, despite scoped
acceptance criteria. A mapping row that claims measurement where only a
Maintainer assignment exists would also make this record misleading.

## Scope delta

N/A: opening baseline; no outcome removed.

## Assurance path

**Assurance path**: high-assurance

Governing doctrine and shipped authoring instructions change. The plan must
map every copy and test owner before implementation; this proposal makes no
doctrine or mapping edit.
