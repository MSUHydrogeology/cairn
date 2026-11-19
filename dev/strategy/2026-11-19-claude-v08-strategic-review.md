# After v0.8: prove it and lighten it

**Author**: Claude (Strategy)
**Model**: Claude Fable 5.2 (`claude-fable-5-2`); evidence sweeps by five Claude Sonnet subagents
**Date**: 2026-11-19
**Status**: draft
**Type**: product-strategy
**Surfaces this would feed**: the v0.9 and later sections of `dev/PLANNING.md`; the "Still open" list in the guide star; any proposal the Maintainer opens from the moves below.
**Length**: over the template's 1,500 words, with the Maintainer's permission (chat, 2026-11-19: "Go ahead and write a longer note").

## Summary

Cairn's core bet is sound, and outside research supports it more strongly than when the guide star was written. The risk is everything around the core. One quantity explains the cost, the test time, the security burden, the platform gaps and the fights over procedure: how much there is.

Three claims carry this note.

1. **The valuable part is small and already written.** The practices that no better model or harness will make obsolete are about the science and the human: an expected answer that does not come from the code, a decision the Maintainer can follow, a short record of why, and a plain statement of what was not checked. They take about 1,500 of the 18,400 words of working guidance, and none of the code.
2. **The rest is perishable, and it grows by a ratchet.** Rules that manage this year's agents age with each model and harness release. Adding one is a local choice; removing one is a project. Most cuts since August have regrown, some within days.
3. **The evidence that would settle Cairn's value has not been gathered.** No outside user has installed it, and nothing counts the errors it has caught.

I recommend that v0.9 be the release that removes. It should settle the defects, lower the cost of a change, prove the first hour on three platforms, offer a small core that sits on any workflow, and turn the agents from elaborating the method to testing it. v0.10 then builds on the scientific core, where Cairn has no competitor. Nothing here is accepted work.

## The question

After v0.8, does Cairn help people ship good scientific code at a cost they will pay? "Good" here means neither polished without end nor generated without checks. What should v0.9 and v0.10 do about the answer?

## Method

I measured these on 2026-11-19 at tag v0.8.0, on a fresh Windows Server 2022 checkout with Python 3.13.5:

- a real `solo-greenfield` install into a scratch repository, following `docs/quickstart.md`, then the integrity check, session start, the board and the security dispatcher;
- read-only scripts over `git log` and the tracked tree: sizes, commits by kind, commits for each proposal and plan, and guidance words at each release tag.

Five Sonnet subagents read Cairn's records and searched outside sources. I mark their figures "reported". For the eight outside studies listed at the end, I read the abstract and the excerpts a search tool returned, not the full text. Six are preprints.

My counts from Git look backward, and I made them with a question in mind. Measurement rule 4 in the guide star warns against exactly that. Treat them as a reason to measure forward, not as a result.

I did not run Cairn's test suite, test macOS or Linux, read the gate code, or look inside LHM or modflow_tools. The shares of code and tests by purpose are classed by file name and are approximate.

Two results would show this note wrong. The first is a forward record from LHM or modflow_tools showing that the present lifecycle catches scientific errors at a cost per change the Maintainer accepts. The second is an outside adopter who tries both and prefers the full install to the small core.

## What v0.8 got right

The direction since 0.5 has been right. Four results show it.

- Always-loaded rules fell from 6,114 words at 0.5 to 1,588 now.
- Median proposal length fell from about 10,800 words to 2,500.
- The installer, the integrity check and session start ran correctly on a Windows machine new to Cairn.
- Security Review of the installer found real defects before release (reported), and the README says plainly what is not yet shown.

The findings below are about what the same effort has not reached.

## Findings

### It works where it is exercised

The install took 8.3 seconds and wrote 73 files. `install/verify_integrity.py` passed, and `dev/tools/session.py`, the board and the security dispatcher ran. The Mac certifying run recorded 5,894 passed and 1 failed in 60 minutes 41 seconds (`dev/measurement/certification-run-2026-11-19.md`). The failure is a pin that waits on the deferred re-anchor.

### The promised avenues have gaps

| Avenue | State on 2026-11-19 |
|---|---|
| macOS | Certified by the full run. I did not test it. |
| Windows, the installer and tools | Work (measured). |
| Windows, the documented first run | Fails at quickstart steps 2 and 3 (measured; issue #97). |
| Windows, the first session | Four frictions (measured; issue #98). |
| Windows, upgrade from a default clone | Fails (issue #95; I did not retest it). |
| Linux | No release verification. I did not test it. |
| Usage meter | Reports Claude usage as unknown (issue #96; I did not retest it). |
| An outside adopter | None yet. |

About 3,400 test functions did not catch the quickstart defect. No check runs the documented commands on each platform. One of the first-session defects cannot appear in Cairn's own sessions at all: Cairn's tree lacks two files that every adopter's tree has.

### Where the mass sits

| Measure | Value |
|---|---|
| Tracked Markdown | 3.78 million words; 89% is proposals and plans, nearly all archived |
| Python | 61,800 unique lines of tools; 116,400 lines of tests |
| Test lines by purpose | pins and re-anchor 24%, installer 19%, security scans 14%, usage meter 11% |
| Smallest install | 117 files, about 41,000 words of live Markdown, 21,700 lines of Python |
| Reading before a first session | about 24,300 words (reported) |
| Science-specific code | one worked example |

The 0.8 layout move shows what this mass costs. One rename produced 195 failed tests and 18 errors across 46 files, about 29 repair commits by three agents, and two one-hour runs (`dev/measurement/certification-run-2026-11-19.md`). The release still shipped with a broken quickstart, about twenty stale references and one failing pin.

### The cost of a change has not fallen

Median proposal length fell from about 10,800 words in the 0.5 window to 2,000 in 0.6, then crept up to 2,500. Every window shows 7 to 8 commits and 3 to 5 review commits per proposal. Plans opened in the 0.8 window took a median 17 commits and 9 review commits, against the project's own target of 3.5.

The tiers do not separate cost. Authors proposed the heavy tier for 15 of 28 proposals in the 0.8 window, and 19 of the 28 carried a Security Review. A proposal whose author proposed the light tier cost as much as a heavy one: a median 7.5 commits against 8.

Since 0.3, 59 to 84% of commits in each release window touched only records. The manual Tokens field read "unknown" in 67 of 67 sampled entries (reported).

A rough model, not a measurement, shows why this matters for tokens. Suppose each commit on a plan is one agent turn. That turn reads the plan (5,000 words), the always-loaded rules (1,600) and a template or guide section (4,000). At about 1.3 tokens a word, 17 turns read about 230,000 tokens of process before any code. Two numbers multiply: the turns, and what each turn loads.

### Cuts regrow

| What | History |
|---|---|
| `AGENTS.md`, words | 5,752 at 0.5; 1,047 at 0.8 |
| All working guidance, words | 16,772 at 0.5; 18,415 at 0.8. The text moved to the guide and the rules folder |
| Test functions | cut from 4,071 to 3,138 on 2026-11-10 (reported); 3,407 at 0.8 |
| Certifying run | about 25 minutes on 10-29 and 49 on 11-12 (both reported); 61 on 11-19 |

The records show the same diagnoses returning (reported): guidance too long eight times since June, test volume seven times, review loops six times. Targets that were set and not measured again include a two-minute inner loop, a ten-minute suite and 3.5 review commits per artifact.

### What the rules cost me

I worked as an adopter's agent for one session. To write the first, 1,349-word version of this note within the rules, I read 21,962 words of rules, templates and board. Three gates ran in a few seconds. The rules that improved the note were plain language, the word budget and commit by path. The rules that cost effort and changed nothing were a claim on a new file in a solo session, 111 lines of doctrine above the template's rule, and 137 commit subjects printed at session start. This is one session with one model. It is the pattern in small: the durable rules paid, and the perishable ones did not.

## The diagnosis

### One quantity

Each complaint is the same quantity seen from a different side.

- Token cost is the text an agent loads each turn, times the turns.
- Test time is the code, times how tightly the tests pin it.
- Security burden is the amount of trusted code that writes into another person's repository.
- Platform cost is the number of lines that touch paths, links and line endings, times three systems.
- Stale text is the number of places one fact is written.
- The Maintainer's attention is the number of artifacts, times their steps.

So being nimble is not a property of the process. It is a property of the mass. No rule about speed outruns 180,000 lines of Python and 3.8 million words.

### The ratchet

A ratchet turns one way. Cairn's has three teeth.

**An incident becomes a rule, the rule a test, the test a pin.** Each step looks responsible. Undoing one needs a proposal, a review and sometimes a signing ceremony. Adding is cheap and removing is dear, so the total rises.

**The project is its own laboratory.** Cairn's product is process, so in Cairn's own repository each process hiccup is a product defect and earns a permanent fix. A science repository damps this, because the science has to ship. Cairn's repository is also an unusually heavy case: most of its code is installer and security machinery. That is why light is the stated default, yet most proposals there are heavy. Lessons from the heavy case have been written into the kernel every adopter gets.

**Agents obey, so the text is the cost.** In a study of repository instruction files, agents followed the instructions, ran more tests and explored more, and cost over 20% more, with no general gain in task success [1]. Its authors conclude that unnecessary requirements make tasks harder. A second study found that a root instruction file went with 29% lower median run time at similar completion [4]. Read together, they favour a short file of what an agent cannot infer. Cairn's guidance tells reviewers to read as if a hidden bug exists, to treat a clean review of complex work with suspicion, and to hold nine lenses in mind. They do. Later rules that say "one pass" or "test only what was written" sit beside those sentences and do not remove them. Part of the fight over procedure is agents faithfully obeying 18,400 words of procedure.

The only force working against the ratchet today is the Maintainer, by hand, in chat. The regrowth table shows that force losing ground after most cuts.

### Durable and perishable

Sort everything Cairn holds into two classes.

**Durable** rules are about the science and the human. The decision is the Maintainer's, and they must be able to follow it. A check needs an expected answer that does not come from the code. A short record says what was decided and why. A report separates what was measured from what was assumed, and names what was not checked. Credentials, data and publication stay with the human. These would hold for a human contractor, and they will hold for a model in 2030.

**Perishable** rules manage this year's agents and fill this year's gaps in harnesses: model tiers, retry limits, pass caps, file claims, session routines, usage meters, token fields, a commit for each step. Both targets are moving. Harnesses now supply on-demand skills, hooks that block an action, a model per subagent, spending caps, usage reports and built-in review (reported). A study of 9,374 agent runs found that the model, not the scaffolding around it, drives outcomes, and that the scaffolding's effect shrinks with each model generation [5].

Three studies bear on the durable class. In one, 68 to 80% of two models' failing runs were plausible patches that were wrong in the same way on each repeat, so that agreement between runs looked healthy [3]. A second, on security repairs, found that passing tests and reviewer agents did not intercept the confirmed failures [7]. In an experiment with 78 novice programmers, those made to explain generated code before accepting it failed a later unaided maintenance task 39% of the time, against 77% without that step [2]. These favour an outside expected answer and a human who understands. They do not favour more rounds of agents reviewing agents. Cairn spends the other way round: a plan carries a median nine review commits, while the independent scientific check is template guidance with one example.

The policy follows. Durable rules get investment, stable numbers and a version, as Cairn Plain Language already has. Perishable rules get an expiry date. Wherever a harness or platform does the job, Cairn deletes its own.

## Six ideas

### 1. Contracts, not choreography

The lifecycle prescribes steps: propose, review, decide, plan, review, build, review, verify, archive, each with its own commit. That is choreography. It is the part that ages as agents improve, that harnesses absorb, and that costs a turn for each step.

A contract states what must be true at the end and leaves the path to the agent. For a change that touches a scientific assumption, done could mean four things:

1. a decision note of 200 words or fewer that the Maintainer accepted, giving the claim, the assumption and the feared mistake;
2. an independent check whose expected answer was written before the result was seen, which fails when the feared mistake is made on purpose and passes on the real code;
3. one fresh reader who tried to break it and recorded the command and its output;
4. a plain report of what was measured, what was assumed and what was not checked.

Nothing there counts commits or requires a plan file. Two ordering rules survive: the human decides before work that cannot be undone, and the expected answer is written before the run.

A contract also tells the agent where to stop. One study found capable agents reaching the correct code and then overwriting it [8]. Iteration past done is not free.

### 2. Two questions in place of the tiers

Ask of any change: **could we undo it**, and **would we notice if it were wrong?**

| | We would notice | We would not notice |
|---|---|---|
| **We can undo it** | Make the change with its test. One commit. | Add the independent check. |
| **We cannot undo it** | Decision note, human decision, one fresh review. | All of these. |

"Cannot undo" covers leaked data, lost work, a release and a published result. "Would not notice" is the scientist's own risk: a sign, unit, index or boundary error that still runs and gives a plausible number. Security Review is the bottom row where the loss is data, credentials or another person's machine.

A scientist can use this table without reading a lifecycle. It also answers what may run unattended: the top-left cell.

### 3. A layer, not a framework

General spec-and-plan frameworks are crowded, with star counts reported from 50,000 to 290,000, and harnesses are building the same steps in. None targets scientists. Cairn's lifecycle competes there with one maintainer. Cairn's scientific layer competes with no one.

So offer the core as a layer that sits on whatever workflow a scientist already uses: a harness's plan mode, another framework, or none. The request changes from "switch your workflow" to "add a few files". Package it on open standards only: a short `AGENTS.md` and a handful of skills under `.agents/skills/`. A skill loads on demand, so it costs one line of context until used. Cairn already ships two. The present lifecycle remains as an optional layer for teams that want it, Cairn among them.

### 4. Expectation first

The cheapest independent check is the scientist's own expectation, written before the run. An example of the form: "drawdown at 100 metres after one day should be near half a metre, from the Theis solution with these values." It takes two minutes. It is independent of the code and of the model's reading of the task. It uses the one thing the agent lacks. It also builds the understanding that the comprehension floor protects.

Make it Cairn's signature move. Build v0.10 around a small library of such checks: an analytical solution, a conservation law, convergence under refinement, a unit round trip, reference data with a tolerance, and the deliberate fault that proves a check can fail.

### 5. A record that pays rent

The promise was that a colleague next spring can find why. That is a promise about finding, not about keeping. An essay on generated code names the two losses a decision record guards against: shared understanding and stated intent [6]. Apply plain-language rule 1 to each record: who reads it, and to do what?

| Record | Reader | Keep |
|---|---|---|
| Decision note | a colleague, or a paper's reviewer | yes, short and indexed |
| Check | the people and machines that run it | yes, as code |
| Review | the author, once | the two lines that changed the decision |
| Plan | the implementer, during the work | no; Git history holds it |

Archive the decision, not the deliberation.

Then give the record a second job that the scientist already owes. A table drawn from decision notes (change, assumption, check, source of the expected answer, result) is a verification statement for a paper's methods section. When a reviewer asks how the authors know the generated code is right, there is a table. I assume journals increasingly ask this. I did not check, and the adopter interview should.

### 6. Security by subtraction

The threat (reported) is a supply chain: Cairn installs instructions and Python that other people's agents load. That risk grows with the amount installed. The pins, the signing ceremony, the integrity check and the release records exist to make a large installer trustworthy. At this release the ceremony stopped three times and was deferred.

Economy of mechanism, already cited under anchor 17, says the strongest control is fewer trusted lines. A person can verify a core of a few Markdown files by reading it in ten minutes. It needs no installer, no upgrade engine and no lockfile, because its upgrade is a diff of a few files. So secure and nimble are not a trade here: one move buys both.

Keep fail-closed containment wherever code still writes into an adopter's tree. For Cairn's own release, weigh replacing pins and ceremony with a human-read diff of the protected files since the last tag. I have not read the gate code, so that is a question for the review of the open re-anchor proposal, not a finding.

## Options

1. **Continue the v0.9 board as written.** It has fourteen rows: one settles defects, two seek outside evidence, and most of the rest add a tool, module or rule. Its case is real. The lifecycle lets one person direct three vendors' agents on one tree, review has found real defects, and artifacts did shrink. But that capacity has mostly produced more apparatus.
2. **Stop and wait for an outside adopter.** This is honest, but it leaves the known defects and the daily cost in place.
3. **Consolidate: remove, prove, then build on the scientific core.** I recommend this one.

## Recommendation

### v0.9: the release that removes

Do these in order. Each makes the next cheaper.

1. **Settle the defects**, as already directed, including issues #97 and #98.
2. **Lower the cost of a change before making other changes.** Give the light lane three commits. At archive, report each change's commits, review commits and Maintainer decisions from Git, with no hand-filled field. Delete the Tokens, Elapsed and benefit-versus-cost fields. Keep archives out of agent searches: in my test a one-line ignore file removed a cached duplicate from this harness's search results. Hold the top of the board to ten plain lines.
3. **Prove the first hour on three platforms.** At each release, run the documented first-run and upgrade commands on macOS, Windows PowerShell and Linux. Let that define multi-host verification, in place of three full-suite runs.
4. **Offer the small core** beside the present profiles, with the two questions as its triage. Take the usage meter and its companion tools out of the default install, freeze work on them, and take usage from the harness where it reports it.
5. **Turn the agents on the method.** Build a seeded-fault trial: a small hydrology model with known solutions, about twenty realistic scientific faults, and three set-ups (a short instruction file, the small core, full Cairn). Declare the faults, the analysis and what counts as inconclusive before the first run. Record which faults each set-up catches and what it costs. Report by set-up and never rank models. The trial tests the six failure signs the board already lists, needs no human subjects, and can be rerun on each new model. From now on, log each real error that a review or check catches in LHM and modflow_tools, one line each. Run the adopter interview on the small core.
6. **Decide the re-anchor question** with subtraction on the table, and cut the release to five human operations.
7. **Ship one dashboard tab**, the development view.

Leave out of v0.9: the budget guard, drain mode, the release module, test records, the four-view pilot, four more tabs and a new dimension axis. Harness spending caps cover the first, where a harness has them. A smaller suite removes the need for the fourth.

**Suggested exit test.** Shipped lines and guidance words both fall. A light change measures at three commits. The first-hour check passes on three platforms. One outside adopter completes three changes. The seeded-fault trial has a recorded result.

**Suggested targets, for the Maintainer to set.** A light change takes 3 commits, 1 review and at most 1 Maintainer decision. A plan takes 8 commits and 4 review commits. The certifying run takes 20 minutes. The small core stays under 3,000 words. The per-change targets count events, not words, as measurement rule 1 asks: a cap on one file moved text to another, as the regrowth table shows.

### Two standing rules that cost nothing

- **The two-repository rule.** A rule enters the kernel only if a science repository needed it. A lesson from Cairn's own development goes to Cairn's own `dev/rules/`.
- **Expiry.** A rule added after an incident names the incident and lapses at the next release unless renewed. At each major model release, rerun the seeded-fault trial with one rule removed. If the result does not move, delete the rule. Procedure then earns its place by measurement, which settles more than arguing with agents does.

### v0.10: the scientific core

- the independent-check library and its skill;
- a worked example from a real project;
- issue #19 expressed as check presets;
- the verification table for papers;
- the January evaluation of Cairn Plain Language;
- the first round of rule removal by trial;
- the lifecycle repackaged as an optional layer;
- hooks offered as thin, optional adapters for the few bright lines.

### 1.0

Declare it on evidence: two outside adopters, a stated comparison against the lighter baseline, a core with stable numbered rules, and a release the Maintainer can cut in thirty minutes. For a scientist who maintains software, the natural form is a methods paper. Publishing a measurement needs the Maintainer's Decision.

### Pace

Cairn has 7,303 commits on 73 active days, a median of 54 a day, and five releases in the thirty days after 0.4. Each release asks adopters to follow an 8,300-word upgrade guide. The standing direction of 2026-07-22 puts science projects first. Let v0.9 land when its exit test passes, not on a date.

## Risks

- **A smaller default drops a safeguard that mattered.** The seeded-fault trial and the outside adopter are the tests, and the layers remain.
- **A contract without steps lets an agent skip the thinking.** The decision note and the fresh review stay as obligations wherever a change cannot be undone.
- **Leaning on harness features invites churn.** The usage meter stopped reading one harness's logs when that harness added eighteen record types (issue #96). Require only open standards, and keep adapters optional and thin.
- **The lifecycle may be what makes three-vendor work possible.** Keep it as a layer, and measure before removing anything from LHM or modflow_tools.
- **The seeded-fault trial is synthetic.** Pair it with real adopters.

## Open questions

1. Is v0.9 the release that removes, with the listed rows left out?
2. Which per-change targets does the Maintainer set?
3. Does the small core sit beside the smallest profile, or replace it?
4. Is the usage meter frozen now, and later retired or kept as an opt-in?
5. Is 1.0 declared on evidence, and is a paper its form?
6. Who is the second outside adopter?

## Outside sources

I read the abstract of each and the excerpts a search tool returned, not the full text. Sources 1, 2, 3, 5, 7 and 8 are preprints and not peer reviewed. Source 4 is a repository deposit whose review status I did not see. Source 6 is a magazine essay.

1. Gloaguen et al. (2026), *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* [doi:10.48550/arxiv.2602.11988](https://doi.org/10.48550/arxiv.2602.11988)
2. Sankaranarayanan (2026), *Mitigating "Epistemic Debt" in Generative AI-Scaffolded Novice Programming using Metacognitive Scripts.* [doi:10.48550/arxiv.2602.20206](https://doi.org/10.48550/arxiv.2602.20206)
3. Mehta (2026), *Confident and Wrong: Silent Semantic Failures in Coding Agents.* [doi:10.48550/arxiv.2603.25764](https://doi.org/10.48550/arxiv.2603.25764)
4. Lulla et al. (2026), *On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents.* [doi:10.5281/zenodo.18348506](https://doi.org/10.5281/zenodo.18348506)
5. Mehtiyev and Assunção (2026), *Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure.* [doi:10.48550/arxiv.2604.02547](https://doi.org/10.48550/arxiv.2604.02547)
6. Storey (2026), *From Technical Debt to Cognitive and Intent Debt.* ACM Queue. [doi:10.1145/3807966](https://doi.org/10.1145/3807966)
7. Bai et al. (2026), *When Passing Tests Hides Vulnerabilities: An Empirical Study of Silent Failures in Agentic Systems.* [doi:10.2139/ssrn.7269655](https://doi.org/10.2139/ssrn.7269655)
8. Kim et al. (2026), *Coherence Collapse: Diagnosing Why Code Agents Fail After Reaching the Right Code.* [doi:10.48550/arxiv.2603.24631](https://doi.org/10.48550/arxiv.2603.24631)
