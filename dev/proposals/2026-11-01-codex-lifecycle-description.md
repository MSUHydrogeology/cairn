# Align published lifecycle descriptions

**Author**: Codex (GPT-6)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy — published methodology is a named high-risk surface
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Correct the published lifecycle descriptions so readers can tell when a proposal needs a plan.

## Decision summary

Correct the README, its lifecycle diagram, the release process, and the published lifecycle method to describe the current rules. A light proposal has no plan; non-trivial standard or heavy proposals need one. This is a description correction, with no new process or changed obligations. The cost is updating and checking four existing surfaces.

## Context

`README.md` says non-trivial work gets a plan; its image and `docs/assets/three-lanes-of-change.svg` say the deliberate lane always includes one. `docs/release-process.md` likewise assigns a plan to every deliberate change. `docs/methodology/lifecycle.md` introduces the deliberate lane as carrying a proposal and plan and later calls the proposal and plan preconditions for implementation without distinguishing light work. These claims conflict with `AGENTS.md` under Lifecycle and records and Review: light proposals have no plan, including for multi-area or wide implementation.

The accepted [cut-the-apparatus proposal](archive/2026-10-30-claude-cut-the-apparatus.md) sets tiers on proposals and leaves the trivial lane untouched. The outer trivial, standard-note and deliberate lanes are distinct from proposal tiers; neither the README nor its diagram should imply that only heavy-tier proposals exist or that all deliberate work is heavy.

## Proposal

Align the four named surfaces with the operative lifecycle, including the diagram's visible labels, title, description and README alternative text. Retain the existing outer lanes and explain proposal tiers where needed: light is the default and has no plan; standard and heavy use plan triage; named high-risk surfaces or added or widened trust boundaries trigger heavy. Keep explanations short and consistent with the existing rules. Preserve all other current obligations, including review and checks. Do not alter `AGENTS.md`, shipped templates, enforcement, or add new process.

## Rationale

A reader should not infer a plan obligation that the accepted rules removed. Updating the underlying method and its public summaries together avoids leaving contradictory guidance. Reusing the existing lanes and tiers avoids inventing another classification.

## Alternatives considered

Leave the text as is: no implementation effort, but readers can follow an obsolete plan requirement. Correct only the README and diagram: less editing, but the release guidance and published method would continue to contradict the operative rules.

## Documentation / doctrine surface

The README, diagram and release process describe the existing workflow; the published method in `docs/methodology/lifecycle.md` is a protected doctrine surface. The operative prescription stays in `AGENTS.md`; this proposal changes no prescription. Coordinate the method file with its existing claim holder before any implementation.

## Evidence / verification plan

Compare each changed statement and diagram accessibility text against `AGENTS.md` and the accepted cut-the-apparatus Decision. Search for readers and byte pins of each changed file, testing negative searches against known-positive controls; run the mapped checks and relevant claim, link, snippet and neutrality gates. The plan must map those checks and applicable Boundary B selection before implementation. A remaining statement that requires a plan for light work, or changes the outer-lane or security rules, falsifies the correction.

### Tests required

Identify tests that read or pin the four named files and run the applicable mapped nodes. Determine exact nodes from the reader and tier-map search during planning; do not assume none exist.

### Examples / smoke checks

Run the relevant prose gates and inspect the rendered diagram and its accessible text. Record commands, results, omissions and the interpreter as required by the plan.

#### Security preflight — five questions, answered in writing

S1: The descriptions draw their rules from the committed operative `AGENTS.md` and accepted Decision; no untrusted input is admitted. S2: A deliberate text mutation that says light work needs a plan should be caught by comparison to `AGENTS.md`; this has not yet been run. S3: The plan must map readers and their triggers; prose gates check integrity, not semantic agreement. S4: No executable default or authorization changes. S5: A reader can still misunderstand a concise diagram; accessible text and review reduce, but cannot eliminate, that risk.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The revised descriptions disagree with the operative rules, obscure an existing safeguard, or require extra artifacts or reviews.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance

## Proposal review -- Codex (GPT-6) -- 2026-11-01

**Verdict**: Accept as framed; no blocking findings.

**Foundations**:

1. **Should it happen?** Yes. The README and release process describe a plan for the deliberate lane, while `AGENTS.md` says light proposals have no plan; the published lifecycle itself distinguishes light at its tier rules. The accepted cut-the-apparatus Decision makes light the default and leaves the outer trivial lane untouched (cut 2 and Decision, 2026-10-30).
2. **Best alternative.** Correct only the README and diagram: less work, but the release procedure and lifecycle explanation would retain conflicting descriptions. Four existing surfaces address the identified cause without new machinery.
3. **What would show it wrong?** A revised description requiring a plan for light, weakening the high-risk or new-boundary trigger, or confusing the outer lanes with proposal tiers; compare the text and diagram with the accepted cut 2 and `AGENTS.md`.

**Advice**: The quickstart introduction calls its illustrated deliberate process the “heavy lane” (`docs/quickstart.md`, note on the example), which can also blur lane and tier. Consider a separately scoped correction; this proposal's four-surface scope does not cover it.

**Coverage**: Read the proposal at `f8260cdb`, its cited accepted cut and Decision, committed lifecycle, README, release procedure and shipped rules; did not inspect implementation, run an install or tests, or perform Security Review. Elapsed time and token use: unknown.

## Security Review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commit: 61b43cf984cefc8ad6c2a65d9ac9811888b5ea84  
Target: proposed four-surface description alignment and retained security authority  
Prior findings: none in this separate Security pass  
Assurance path: high-assurance

**Tier**: Security Review  
**Findings**: none  
**Verdict**: ACCEPT as framed; recommendation only, not a Maintainer Decision.  
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The diagram and release procedure currently prescribe a plan throughout the deliberate lane, while the accepted cut 2 and governing Review rule exempt light proposals. Aligning descriptions removes that false obligation without weakening named high-risk or added/widened-boundary triggers, which the Proposal explicitly retains. -- Committed SVG title/description; release process, Method; accepted cut-the-apparatus, cut 2 and Decision; `AGENTS.md`, Review.
2. **Best alternative.** Correct the README and diagram alone. That costs fewer edits but leaves the same contradiction in release guidance and the published method; four existing surfaces address it without another artifact type or rule. -- Proposal, Context, Alternatives considered and Scope; lifecycle method, Three lanes.
3. **What would show it wrong?** Describing every deliberate change as heavy, allowing light to bypass an independent high-risk trigger, or treating proposal tiers as replacements for trivial and standard-note lanes. The proposed comparison against governing text and accepted cut 2 directly addresses those errors; diagram visible and accessible text must agree. -- Proposal, Proposal and Evidence / verification plan; accepted cut 2.

No blocking security finding. The four-surface limit and existing comparison/prose checks are proportionate; no additional classification apparatus is needed. This review grants no implementation or Decision authority.

Coverage: examined the committed proposal, ordinary review, current proposal template, governing tier rule, accepted cut and Decision, lifecycle triage, diagram and release passage. Did not inspect future wording, render a changed diagram, enumerate every reader or run checks or suites.
