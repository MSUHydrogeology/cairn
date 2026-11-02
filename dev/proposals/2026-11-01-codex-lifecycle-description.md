# Align published lifecycle descriptions

**Author**: Codex (GPT-6)
**Status**: awaiting-review
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
