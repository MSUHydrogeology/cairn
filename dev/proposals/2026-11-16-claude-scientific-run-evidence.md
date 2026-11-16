# Verify a simulation change by its stage output, not by a model run

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
**Review**: usual
**Proposed tier**: light -- one shipped module and its byte-identical installed copy change, no engine file or template changes, and the Maintainer sets the tier
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-16
**In brief**: A project with a simulation model learns to check most changes by comparing one stage's output file with an accepted copy, and to keep one accepted reference run that only the Maintainer may replace.

## Decision summary

This is general guidance drawn from two open issues (#58, #59), one more (#87) and one adopter's working rules. No second project has confirmed it; see "Signals the change is wrong".

Agents on a simulation project run the whole model after refactors "to be sure". A run takes tens of minutes to hours and answers a question about the model, not whether a change kept its promises. Proposed: a project that works in stages checks a change by comparing the output file of its own stage with an accepted copy; a full run is a named act, taken once at the end of a plan that asks a model question. The control for a before-and-after comparison is the commit just before the change. One accepted reference run per model and mode is kept. The Maintainer accepts a new reference and sets pass bands; an agent may not.

Cost: about 172 added words in one opt-in module (measured, below), and none in any template, `AGENTS.md` or the collaboration guide. No required run changes.

## Context

Already covered (read in the current tree, not restated):

- `dev/agent_collaboration.md` > "Verification" (and the shipped copy), `templates/core/dev/plans/_template.md` lines 375-379 and `docs/methodology/plans.md` lines 446-452 say scientific evidence belongs with the work or release that requires it, and that subject or duration waives and reschedules no run.
- `templates/modules/team-gated/testing-discipline.md`, "Simulation models verify at three timescales", says full runs stay outside the ordinary run and a short summary is recorded.
- The `WIDER RUN REQUIRED` verdict that closed #33 is in the guide. #18 was closed as a duplicate of #19, postponed to v0.9; nothing here depends on it.

Missing (searched `templates/`, `docs/methodology/`, the guide and `AGENTS.md` for "reference run", "pass band", "stage output" and "first real output"; no hit): when a stage-output comparison is enough; the control for a before-and-after comparison; where a standing reference lives and who accepts it; who sets pass bands; and #87, how a reader of an external tool's output is accepted.

One adopter's rules cover the first four in about 390 words (read-only; not in this tree). I describe them generically; I have not tested them elsewhere.

## Proposal

Edit `templates/modules/team-gated/testing-discipline.md` and `dev/modules/testing-discipline.md` (a test requires them to match byte for byte):

1. Replace item 3, "Full runs": a full run answers a question about the model, is not a test, is named by the plan that asks it, and is taken once at the end of the cycle.
2. Add "Stage output first": compare a change's own stage output with the accepted copy; later stages need not run. That suffices when the output should not change, or changes only as the plan predicted. It never replaces a run that a plan, proposal or release requires.
3. Add "One reference, one control": the control is the commit just before the change; an older run is a cross-check only. Keep one accepted reference run per model and mode, with its commit and settings, in the run log. The Maintainer accepts a new reference and sets pass bands before the runs. An agent may build a candidate and report against the bands; it may not accept a reference or widen a band.
4. After "Test promises", add #87: the tool's first real output, small and with no private data, is the committed fixture; until then the test says the fixture is unverified.
5. Offsets in the same module: drop the sentence "Agents map routine coverage and reviewers challenge it..." (the guide says it) and the parenthetical and mutant-proof clause in the Pareto paragraph (the guide's "Verification" carries both).

Word change, measured with `wc -w` on a scratch copy of the module (2,130 words today): +172 in each of the two copies (2,302). Plan template 0, proposal template 0, `AGENTS.md` 0, collaboration guide 0, `docs/methodology/plans.md` 0.

Not proposed: a project's list of code areas that usually need a run (project-local), and any change to who gates a named run; #59 asks that a reviewed plan's run need no further gate, and I leave that as is.

## Rationale

Home: the testing-discipline module. It already holds the simulation paragraph, only projects that selected it load it, and no engine, template or dimension changes. The always-loaded files stay unchanged, in line with the Maintainer's 2026-11-10 direction against bloat.

## Alternatives considered

- A new opt-in simulation module: no growth in existing text, but it needs an install-contract change and the staged-module trigger design, both still open on the board, and a selection rule that would lean on #19. Revisit when staged modules exist; this text then moves whole.
- The guide, plan template or proposal template (what #58 and #59 ask): every project loads them, and the templates must not grow.
- Do nothing: agents keep running per-change identity runs; #59's stop-condition confusion repeats.

## Documentation / doctrine surface

No file under `docs/methodology/` changes, so no doctrine-evolution gate is claimed. The module is the shipped template layer. Not checked: whether `dev/modules/` is refreshed by tool or edited by hand.

## Evidence / verification plan

Falsified if the text can be read as allowing a stage comparison in place of a required run, or an agent's acceptance of a reference.

### Tests required

Promise: the two module copies stay identical (`bootstrap/tests/contract/test_verification_boundaries.py`). No test pins the new wording. Selection: `python tools/test_tiers.py for` the two files. Not run for this proposal; only the claim check was.

### Examples / smoke checks

N/A: guidance prose with no executable path.

### Independent scientific check

N/A: no scientific assumption or result touched; the text governs how evidence is gathered. A reviewer may disagree, since it sets who accepts a scientific reference.

## Signals the change is wrong

- A defect that a stage comparison passed and a full run would have caught.
- An adopter's Maintainer rejects an agent-built reference or band in practice.
- A second project finds the four stages or the commit-before control do not fit its model.

Evidence missing: a second project using this, and a defect history with stage comparisons.

## Scope delta

**Scope delta**: preserved. Named scientific runs and required checks are unchanged; the issues grant no exception.

## Assurance path

**Assurance path**: standard

For the Maintainer, with my defaults: (1) Does "templates must not grow" cover this module's +172 words? Default: no, accept them; the trim proposal owns the module's total. (2) Tier light. (3) Stay in this module until staged modules exist.
