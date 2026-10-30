# Deliver useful work without accumulating avoidable burden

**Author**: Codex (runtime model identifier unavailable; Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Make unnecessary complexity and unfinished commitments count against delivery, without adding machinery.

## Context

The Maintainer reports ballooning work, with cases in issues
[#36](https://github.com/MSUHydrogeology/cairn/issues/36),
[#37](https://github.com/MSUHydrogeology/cairn/issues/37),
[#38](https://github.com/MSUHydrogeology/cairn/issues/38) and
[#39](https://github.com/MSUHydrogeology/cairn/issues/39).
These are adopter reports, not independently reproduced measurements.

[Consensus research](https://consensus.app/search/what-does-the-research-literature-say-about-balanc/PApQ_jgAQfKubGwIG5nnWw/)
provided discovery; selected primary sources were checked.
[SPACE](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/)
rejects single-metric productivity;
[multitask incentive theory](https://web.stanford.edu/~milgrom/publishedarticles/Multitask%20Principal%20Agent.pdf)
explains distorted effort allocation;
[debt research](https://doi.org/10.1016/j.jss.2019.06.004) documents reported maintenance burden;
[comprehension research](https://sscalabrino.github.io/files/2019/TSE2019AutomaticallyAssessingCode.pdf)
challenges simple proxies;
[SWE-Effi](https://arxiv.org/abs/2509.09853), a benchmark preprint, examines outcomes
alongside resources. These support the design, not validated policy thresholds.

## Proposal

Replace fragmented cost/reuse advice with this governing rule in both
`AGENTS.md` copies:

> **Deliver, with economy.** Finish the agreed useful outcome with the required
> assurance and least total lifecycle burden. Cost includes time, tokens,
> compute, delay, human attention and continuing maintenance. Complexity
> includes opacity, concepts, indirection, coupling, state, duplication and
> obligations in code, documentation and process. Every addition—including
> tests (construction and repeated execution), functions, class growth, files, folders
> and procedures—costs something. It must buy a current capability, clearer
> understanding or worthwhile protection; fewer lines are not inherently better.
>
> Authors and reviewers own the costs their choices induce. Prefer simpler
> adequate means, make ordinary decisions and continue independent authorized
> work around blockers.
> Reconsider ballooning approaches; stop optional polishing when the outcome
> and required evidence are adequate. Do not substitute more planning for
> authorized implementation. Cost constrains the means, not the agreed ambition.

**Make this bite in existing review.** Avoidable burden is a defect, not merely
a style preference: its finding names a concrete lower-burden adequate
alternative and preserves the outcome. No global-optimum proof or per-addition
essay. Reviewers price their remedies too.
Reuse when it helps; do not demand a framework to remove harmless duplication.
Keep existing reuse-search obligations.
Honor model capability floors and escalation; higher tiers are not blanket insurance.

**Unfinished work is not a saving.** Whittling proposed/accepted scope,
transferring work or archiving a local plan does not deliver the original
outcome or erase its cost. Only the Maintainer can concede scope.
An existing deferral reason must explain why delay beats completion now:
remaining effort, re-entry/re-review and delay consequences; unknown is not
zero. Retain the obligation and cumulative cost under the original work's
existing links, across successor plans; later budgets must not reset on transfer.
This adds no tracker or new scope-remainder format.
Unaccepted ideas may be declined outright.
The Maintainer may retire obsolete objectives; sunk costs do not justify continuation.

**Observe before budgeting.** At each existing authoring, review, revision,
implementation, verification and archive step, sample start/end clock time or
reuse host timing. Keep one cost sentence in its existing result record:
elapsed time and reported or defensibly estimated tokens, with source and
model when known. Separate operator waiting and parallel rollups; preserve
failed work. Missing usage is unknown, not zero; artifact size is not consumption.
Use existing session information, not transcript collection or new telemetry.
Later budgets follow observations; no hard caps or new approvals now.

**Resolve the four concrete pressures:**

- **#36:** at most two Security Review passes per obligation without further
  Maintainer authority; the second covers revisions and affected interactions.
  Reviewer changes or new findings do not reset the count. Unresolved work
  stays open for a recorded Maintainer disposition, never automatic clearance.
  Existing security capability floors remain.
- **#37:** distinguish changed trust exposure/guards/authority from ordinary use
  of unchanged reviewed boundaries. Same format alone proves neither safety
  nor widening. Keep named high-risk triggers; correct mistaken declarations
  through existing review reasoning, with no new field. Use bounded/wide
  verification for the actual change, not incidental file proximity.
- **#38:** reviews live inside/beside their artifact, never a separate reviews tree.
- **#39:** human-readable evidence summaries retain the tested commit,
  reproduction method and material omissions. Mutation summaries retain
  control, totals, killed count and every survivor/equivalent with reasons;
  equivalence stays measured. Versioned owning tests/scripts hold reproducible
  methods, not pasted logs or per-killed-mutant ledgers. Commit bodies have a
  normally wrapped 30-line ceiling.

## Rationale

Judge economy against delivered value and retained obligations, not minimum
activity. Necessary growth and justified deferral remain legitimate;
bureaucracy and under-delivery do not.

## Alternatives considered

“Do less” rewards omission; output quotas reward busywork; numerical complexity
prices reward code golf. A cost platform recreates the problem; existing
restraint leaves explicit growth permissions intact.

## Documentation / doctrine surface

Reconcile both `AGENTS.md` and agent-collaboration copies, related lifecycle,
review and verification doctrine, both proposal/plan template pairs, and
`templates/modules/team-gated/security-review.md`. Extend rationale anchor 17.
Replace conflicting prose; preserve consumed headings/fields. No new tools,
stores, folders, forms or recurring audits. Preserve history and the existing
doctrine-evolution gate; do not claim an incident-count exception.

## Evidence / verification plan

### Tests required

Map existing readers under `bootstrap/tests/`: review-stance, review-sweep,
verification-boundaries and stewardship families; reuse installation coverage.
Assert concepts and preserved safeguards, not every word. Existing protected-file
ceremonies remain.

### Examples / smoke checks

Run scoped `scripts/claim_check.py`, `scripts/check_cairn.py` and
`scripts/quality_gate.py` neutrality/redundancy checks. In ordinary review,
challenge needless tests/hierarchy, unreadable compression, a real security
defect, an unresolved second pass and a scope-cut disguised as economy.
No extra cost review or full suite for authoring this proposal.

#### Security preflight

S1: author claims are challenged, not authenticated; the Maintainer owns residual risk.
S2: no executable judgment checker is promised; prose presence cannot prove compliance.
S3: existing author/reviewer stages apply the rule.
S4: unresolved required work stays open; cost grants no waiver.
S5: mistaken or colluding judgments remain possible.

### Independent scientific check

N/A: no scientific assumption or result changed.

## Signals the change is wrong

More accounting appears; agreed work disappears; waste findings become taste
disputes; safety is weakened; or costs are shifted into successor plans.

## Scope delta

**Scope delta**: preserved; measurement, delivery and deferral accountability included
under the Maintainer's in-place rewrite instruction.

## Assurance path

**Assurance path**: high-assurance — governing doctrine and security-review rules.
