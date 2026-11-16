# Guidance for projects that have grown: staged modules and triggers

**Author**: Claude Fable 5.2 (Strategy)
**Model**: Claude Fable 5.2 (`claude-fable-5-2`)
**Date**: 2026-11-16
**Status**: draft
**Type**: product-strategy
**Surfaces this would feed**: v0.8 rows in [`dev/PLANNING.md`](../PLANNING.md) ("Guidance for projects that have grown", "Better treatment of rules", "Trim bulk", "Offer new and unselected modules at upgrade"); the v0.9 release-module and test-records rows

## Summary

Cairn guides a project through starting: install, onboarding and the life of one change. It says little about what a project needs once it has grown. In three areas (rules, testing, releases) both adopters built their own answer. The recommendation is to match guidance to the project's stage: opt-in modules, each with a trigger that offers it to the adopter when the project reaches the need. The Maintainer agreed the direction on 2026-11-16: "Yeah we need to have triggers that offer new modules to the adopter". This is direction, not a Decision; each part goes through its own proposal.

## The question

The Maintainer, 2026-11-16, after reading the issues adopters filed: LHM's rules folder has "grown substantially. I feel like this is something that we didn't give adequate guidance for in Cairn"; then the testing ideas for large projects; then "we don't ship any guidance on releases. This points to a need for more sophistication in how we guide our adopters."

## Method

I read 31 open Cairn issues (#62 to #92) filed from LHM and modflow_tools. I read LHM's `RULES.md`, its rules folder README, its development start page, its testing and release entries and its test-records plan, at LHM commit `69580aae0`. Word counts are `wc -w`. A subagent read the Claude Code memory documentation on 2026-11-16. I searched Cairn's `templates/` for release guidance. Not done: I read modflow_tools only by file listing, from a local copy dated 2026-11-13; I ran no tests; I did not measure how much of LHM's rule text moved in from agent memory.

## Findings

**The same gap in three areas.**

| Area | What Cairn ships | What the adopters built |
|---|---|---|
| Rules | A 359-word README for the rules folder | LHM: 13 files, 10,523 words, two routers |
| Testing | One suite, one certifying run, timing targets up to 10 minutes | Testing by part and cost; model runs as evidence; test records |
| Releases | Nothing: no module and no rule | LHM: a 17-step release rule (945 words), a keep list and a cut script. modflow_tools: a releasing guide and a reconciliation rule |

**Rules (measured at LHM).** Between 2026-11-13 and 2026-11-16 the always-loaded files fell from 5,211 to 2,691 words, while the rules folder grew from 2,327 words in 3 files to 10,523 in 13. Total rule text grew 75 percent, from 7,538 to 13,214 words. LHM invented what Cairn does not describe: rules for running the software kept apart from rules for changing it (#74); a second router table inside the folder; an "Applies when" line opening each entry; and a rule for how a rule enters (the Maintainer's approval, never only agent memory, #70). The missing guidance shows: single entries reach 1,639 words; the testing entry states two rules twice; rules, procedures, an index and vendor habits sit side by side; and two test files (537 lines) pin the layout.

**Testing.** Cairn's testing text assumes one suite and one certifying run. LHM's model runs take weeks and its suite holds 12,975 items, about 79 percent of them added in 47 days (LHM's own measurement note). Its rules: the project is not one piece, so test each part where it lives and never run the whole suite by default; a model run is a named act with a question, made once at the end of a plan and compared with a standing Base run (#58, #59); a test never rebuilds inputs; a test slower than seconds is defended in a plan; and a passing test file counts until a file it depends on changes (#81; LHM's plan stops if the measured saving is small).

**Releases.** LHM's release rule covers when to cut, reconciling plans, the keep list, a check that nothing kept cites the development tree, third-party notices, verification from test records, the tag, publication and citation metadata. #82 and #83 ask Cairn to offer this as a module.

**Modules are chosen once.** Each shipped module states "Selected when", a condition on the profile given at install. Nothing looks again as the project changes. `upgrade --plan` prints one line naming modules the project lacks, with no description.

**The wrapper file.** By the Claude Code documentation, version 2.1.277 or later reads `AGENTS.md` directly when no `CLAUDE.md` exists in the working folder or above it. LHM removed its `CLAUDE.md` on 2026-11-14. Not confirmed by the documentation: the desktop app, IDE extensions and the SDK.

## Options

- **A. Do nothing.** Each adopter keeps inventing. The next adopter starts from nothing, and the fold-back issues keep arriving one rule at a time.
- **B. Add the guidance to the files every project loads.** Rejected: the v0.7 weight review and the trim row exist because that text was already too long, and a new project does not need release or large-suite rules.
- **C. Staged modules with triggers.** Guidance for a grown project ships as opt-in modules. Each names a trigger, and Cairn offers the module when the trigger is met.

## Recommendation

Option C, in four parts.

1. **A module names its trigger.** Beside "Selected when", a module states "Offered when": a condition a tool can read from the project's own files, cheaply and with no network. Candidates, to be settled per module: the rules folder passes a word count; a version tag or a released changelog section exists and the project has no release rule; recorded test time passes a threshold.
2. **Cairn offers; the person decides.** When a trigger is met, the agent says in plain language what the module does and what it costs, and asks. A yes runs the existing adopt step. Nothing installs itself, and a declined offer is remembered so it is not repeated every session. This extends the v0.8 row on offering modules at upgrade from "at upgrade" to "when the project reaches the need".
3. **Harvest, do not invent.** Each module generalizes what the two adopters converged on and leaves out what is specific to one project. A module with one adopter's evidence waits for a second.
4. **Three first modules.** Rules-folder guidance: entry shape, an applicability line, a size budget per entry, the run and development split, how a rule enters and leaves, and merging on a move (v0.8, with the rules and trim rows). Testing by part and cost: the principle goes into the v0.8 testing-text rewrite; the record tool waits for LHM's measured saving (v0.9). Releases: built in v0.9 for the next adopter, since both current adopters have their own rule; its structural prerequisite, leaving Cairn out of a release, is v0.8.

This applies the Maintainer's 2026-11-13 direction to match security effort to the project's size to guidance in general.

Residual risk: triggers are new mechanism, and a noisy or wrong offer costs trust. Start with one trigger, read by a tool that already runs, and measure whether the offer was accepted.

## Open questions

1. **Where a trigger is checked.** Session start runs often and already reads the tree; upgrade is rare. Which tool reads triggers, and how often may it speak?
2. **Where a declined offer is recorded,** so every agent and vendor sees it.
3. **Thresholds.** What rule-folder size, test time or release signal is the trigger? LHM and modflow_tools give two data points each.
4. **The engine.** If triggers live in the installer's module table they change an engine file, which is heavy and waits for the repository layout. A guidance-only first version would not.
5. **The wrapper.** Dropping the shipped Claude wrapper changes the accepted layout's scope and needs the Maintainer's word recorded on that proposal; its habits need a new home.
