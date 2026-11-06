# Say what the work will deliver

**Author**: Codex (ordinary proposal author; Medium floor; runtime model identifier unavailable)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy -- changes shipped methodology templates
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Make proposal, plan and strategy summaries say what people will receive without repeating the technical inventory.
**Elapsed**: approximately 10 minutes
**Tokens**: unknown

## Decision summary

Change six existing template files: the local and shipped proposal, plan and
strategy templates. Proposals will name the main things added, changed or
removed; plans will begin with a short Build summary; strategy notes will
summarize their question and recommended direction. This adds brief writing
guidance within the existing word budgets, with no new tool or review step.

## Context

The Maintainer requested this on 2026-11-06; board item 3a retains the wording.
The proposal template's Decision summary asks for the problem, change and
tradeoffs, but does not explicitly ask what will be built. Plans begin with
their source and scope, and strategy notes have no suggested Summary section.
All three have a one-line `In brief` field for board display; that field does
not replace the requested reading aid.

## Proposal

For v0.7, revise the existing Decision summary prompt to name the useful
deliverables in ordinary language: tools, documents, behavior or other outputs
being added, changed or removed. Name only material categories; a prose change
need not invent a tool or fill in an empty category. Keep the problem and
meaningful costs alongside them. For example: "Add one optional command for
finding similar functions and update the architecture guide."

Add `## Build summary` immediately after the plan header. In a few sentences,
state the accepted result and what the implementation will produce or change.
Keep paths, prerequisites and detailed acceptance checks in their existing
sections. Adjust the template's copy instructions to include the new heading.

Add a suggested `## Summary` after the strategy-note header. State the question,
main conclusion or recommendation, and the things it could lead to. Mark
unsettled choices as such: exploration is not an accepted commitment. Preserve
the strategy template's flexibility for different kinds of note.

Match each local template with its shipped counterpart. Keep the existing
one-line board fields, word budgets, lifecycle, authority and review duties.
The summary is a reading aid, not a second scope contract. If it disagrees
with the operative sections, correct the disagreement rather than choose a
second source of authority. Apply prospectively; do not retrofit archives or
rewrite active records merely to add a heading.

## Rationale

Readers should quickly see what they are deciding about or following. Reusing
short summaries costs a few sentences per new artifact; it needs no inventory,
parser, required human trial or separate document. Coordinate implementation
with the accepted readable-plans work after the current template writers finish.

## Alternatives considered

Keep the current prompts: no maintenance change, but the requested deliverables
remain easy to omit. Expand only `In brief`: less prose, but one board sentence
cannot reliably explain several material outputs and their costs. Add a file
table everywhere: more precise paths, but duplicates Scope and makes strategy
exploration look like a settled build contract. Recommend the short summaries.

## Documentation / doctrine surface

Domain-local template guidance lands in `dev/proposals/_template.md`,
`dev/plans/_template.md` and `dev/strategy/_template.md`, plus their counterparts
under `templates/core/dev/`. No new cross-cutting AGENTS rule is needed.

## Evidence / verification plan

### Tests required

Use the existing tier selector for all six changed files and trace their
template-copy, word-budget and installation readers. Preserve board parsing
and required operative headings. Use existing test homes; add a test only for
an uncovered plausible fault, not to pin every word of a prompt. No tests have
run for this proposed implementation.

### Examples / smoke checks

Prepare short proposal, plan and exploratory-strategy examples using the
revised templates. An independent agent reader must identify their material
outputs and distinguish a recommendation from accepted work, without a live
translation. Include a documentation-only example so empty tool categories
are not manufactured. Keep examples temporary; record the concise conclusion
here or in the implementation plan. Run claim, link, snippet and neutrality
gates and the mapped final change checks on committed bytes.

### Security preflight

**S1.** Authors supply summaries; only the existing Decision grants authority.
The summary cannot authorize itself or relax a criterion.
**S2.** A strategy example presenting an unaccepted recommendation as approved
work would fail the independent reading check. This proposed check has not run;
implementation must show the reader detects that negative control as well as
understanding a correct example.
**S3.** Existing reviewers read the templates and examples during their usual
stages. No automatic semantic checker is claimed or proposed.
**S4.** Missing or conflicting summaries require correction; no default grants
permission or silently removes accepted work.
**S5.** Misleading summaries remain possible, especially with a dishonest
author; this writing guidance is not an adversarial authorization boundary.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Readers mistake strategy exploration for approved implementation, writers copy
Scope into a second inventory, or summaries grow while useful outputs remain
unclear. Revise the prompts if the example reading shows those faults.

## Scope delta

**Scope delta**: preserved. All three artifact types, local and shipped templates,
existing budgets and authority preserved.

## Assurance path

**Assurance path**: high-assurance

Heavy because these are shipped methodology templates: usual and separate
Security proposal reviews, a reviewed plan after acceptance, Low implementation,
usual and separate Security code reviews, and final mapped verification. No
runtime boundary, dependency, telemetry or release operation is added.

## Review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed commit**: `cd57b3fabd9ecd031f37a1cc5d5c21d5d2b7f0d8`
**Tier**: Internal

**Foundations**:

1. **Should this happen as framed?** Yes. The board request calls for concrete outputs in proposals, plans and strategy notes; the proposed prompts address all three while preserving existing scope and Decision authority. The current plan copy rule starts at Source proposal, so changing it as proposed matters. -- `dev/PLANNING.md` item 3a; proposal and `dev/plans/_template.md` copy instructions.
2. **Best alternative.** Keep the short summaries within existing budgets as proposed. Expanding only `In brief` is simpler but a single board sentence cannot reliably describe multiple material outputs and costs; a file table duplicates Scope and can make exploration look committed. -- proposal Alternatives; proposal and plan template `In brief` rules; `dev/strategy/_template.md` suggested sections.
3. **What would show it wrong?** A reader who mistakes an exploratory recommendation for approval, cannot identify material outputs, or sees a documentation-only change forced into a tool category would falsify the benefit; test a misleading negative control alongside correct examples. A second inventory or disagreement with operative Scope would also show the prompts need revision. -- proposal Examples, Security preflight S2 and Signals.

**Findings**: none. **Verdict**: PROCEED to author response after the separate Security Review.

**Coverage**: Read the committed proposal, board request and local proposal, plan and strategy templates, including copy, word-budget and authority rules. Did not run the proposed examples or inspect all installed-template consumers; implementation must map and verify those. No implementation or Security Review was performed. **Elapsed**: approximately 2 minutes. **Tokens**: unknown.
