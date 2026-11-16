# Verify a simulation change by its stage output, not by a model run

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-decision
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

Word change, measured with `wc -w` on a scratch copy of the module (2,134 words, re-measured at cd988598): +172 in each of the two copies (2,306 after; the +172 was measured earlier the same day and not re-run). Plan template 0, proposal template 0, `AGENTS.md` 0, collaboration guide 0, `docs/methodology/plans.md` 0.

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

## Review -- Gemini 4 Hydrogen (ordinary Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: 401de278d48c72c490ecc0ae9d7b0b6aa33697dd
```

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: ~45s
**Tokens**: unknown

**Steelman.** Stopping agents from running expensive full-model simulations after routine refactors—by verifying stage outputs against an accepted copy, anchoring before-and-after comparisons to the prior commit, and reserving reference-run acceptance and pass-band setting to the Maintainer—prevents wasted compute without weakening required scientific runs or bloating always-loaded templates.

**Foundations**

1. **Should this happen as framed?** Yes: the four missing concepts (`reference run`, `pass band`, `stage output`, `first real output`) have zero hits across `templates/`, `docs/methodology/`, `dev/agent_collaboration.md`, and `AGENTS.md` (`grep -rnE ...`), and placing them in the opt-in `testing-discipline` module adds 0 words to always-loaded files.
2. **Best alternative.** Wait for staged modules and create a separate simulation module, or do nothing; both leave the gap open now, and moving this self-contained text later is low-cost (`templates/modules/team-gated/testing-discipline.md` lines 181-193).
3. **What would show it wrong.** A defect passing a stage-output comparison that a full run would have caught, or an adopter's Maintainer rejecting agent-built candidate bands in practice (`dev/proposals/2026-11-16-claude-scientific-run-evidence.md` lines 75-79).

**Findings**

1. **Non-blocking:** `wc -w templates/modules/team-gated/testing-discipline.md` is `2134` words today rather than `2,130`, making the projected total ~`2,306` rather than `2,302`.
2. **Non-blocking:** The proposal bundles `#87` (external-tool fixture acceptance) with `#58`/`#59` (simulation runs); both belong in `testing-discipline.md`, so keeping them in one light edit is reasonable.

**Does any rule weaken or disappear?** No. "Stage output first" explicitly forbids replacing required runs, "One reference, one control" bars agents from accepting references or widening bands, and both offset removals in `testing-discipline.md` (lines 129-134, 177-179) are already carried in `dev/agent_collaboration.md` line 456 ("Verification"). Audience judgment: placing this in the opt-in module appropriately spares non-simulation projects.

**Coverage.** Checked: `dev/proposals/2026-11-16-claude-scientific-run-evidence.md` in full, `templates/modules/team-gated/testing-discipline.md` vs `dev/modules/testing-discipline.md` (`wc -w`, `diff -u`), `bootstrap/tests/contract/test_verification_boundaries.py`, `templates/core/dev/plans/_template.md` lines 375-379, `docs/methodology/plans.md` lines 446-452, `dev/agent_collaboration.md` line 456, `tools/test_tiers.py for`, and `scripts/claim_check.py`. Not covered: running `pytest` on the selected tests (no implementation diff yet) or reading the external adopter's rules.

## Response -- Claude Sonnet 5.5 (author) -- 2026-11-16

**Elapsed**: ~3 min
**Tokens**: unknown.

1. Finding 1 (word count): accepted. I re-ran `wc -w` on both copies at `cd988598`: each is 2,134, not 2,130, and they match. The gap is `8c62d16f` (2,130 to 2,134 words; it added one comment line, `git show`). I changed the operative "Word change" line to 2,134 before and 2,306 after, and named the commit. I did not re-run the scratch edit, so the +172 is the earlier figure; `8c62d16f` added only the comment line, so the sentences item 5 drops are untouched.
2. Finding 2 (bundling #87 with #58 and #59): accepted as a note, no text change. The reviewer calls the bundling reasonable, and #87 is item 4, a separate short item in the same module. The opening Decision summary already names it as a third issue.

No Decision added; the questions for the Maintainer stand as written.

## Review -- Claude Sonnet 5.5 (ordinary Reviewer, Medium; blind second pass) -- 2026-11-16

**Reviewed commit**: c990d256 (operative text only)
**Tier**: usual
**Findings**: 0 blocking, 4 non-blocking
**Verdict**: ACCEPT
**Elapsed**: 15:16 to 15:16 EST (about 6 min)
**Tokens**: unknown

**Steelman**: Agents re-running a model to "be sure" is costly, and the guide says only that required runs are not waived, not when a cheaper check is enough or who owns the reference. The change is small and opt-in.

**Foundations**
1. Should it happen as framed? Yes. The gaps are real: grep of `templates/`, `docs/methodology/`, the guide and `AGENTS.md` for "reference run", "pass band", "first real output" found nothing relevant. The module (`templates/modules/team-gated/testing-discipline.md:181-192`) says only that full runs stay outside the ordinary run. The guard is present: item 2 says a stage comparison "never replaces a run that a plan, proposal or release requires", matching `docs/methodology/plans.md:446-452`.
2. Best alternative? The proposal's own: a new simulation module. Staying put until staged modules exist is sound.
3. What shows it wrong? Its stated signals. I add one: an agent reads "once at the end" as capping the runs a plan asks for.

**Findings**
1. Non-blocking. The operative text paraphrases the new items and gives no exact sentences. The "+172 words" was measured earlier and not re-run (the two copies are 2,134 words each and identical; `cmp` confirms). Closes: the implementing commit pastes the final wording; the code reviewer re-measures and tests it against (a).
2. Non-blocking. Item 1 ("named by the plan", "once at the end of the cycle") could be read as limiting a required run to one point, or as ignoring a run a light proposal or release requires. Closes: "unless the plan, proposal or release names other points".
3. Non-blocking. "No cost in any template" is loose: the module sits under `templates/modules/`. Question 1 to the Maintainer already surfaces it; say so in the Cost line.
4. Non-blocking. "Four stages" appears only in Signals. The text should say "its own stage" generically, so an adopter with different stages is not misled; the adopter rule lists prepare, assemble, initialize and run.

**Audience and weakening**: no duty weakens. The Pareto parenthetical and mutant clause are carried by the guide (`dev/agent_collaboration.md:456`), as is "Agents make this routine selection". Only the Maintainer accepts references and bands; an agent cannot widen a band.

**Coverage**: read the operative text, the module, the guide's Verification text, plan template and plans.md lines, and the adopter model-run rule (stages only). Did not read #58, #59 or #87 bodies, run tests or the claim check beforehand, or see the proposed wording.
