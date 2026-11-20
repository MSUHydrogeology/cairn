# After v0.8: keep what accumulates in check

**Author**: Claude (Strategy)
**Model**: Claude Fable 5.2 (`claude-fable-5-2`); evidence sweeps by five Claude Sonnet subagents
**Date**: 2026-11-19
**Status**: revised
**Type**: product-strategy
**Surfaces this would feed**: the v0.9 and later sections of `dev/PLANNING.md`; the "Still open" list in the guide star; any proposal the Maintainer opens from the moves below.
**Length**: over the template's 1,500 words, with the Maintainer's permission (chat, 2026-11-19: "Go ahead and write a longer note").

## Summary

Cairn's subject is what happens when software built by agents grows. The Maintainer put it this way on 2026-11-19: Cairn solves "the problems that arise in going from a few vibe coded functions and modules into an entire suite--so that other scientists don't have to". Judged as that, Cairn is working on the right problem, and outside studies now measure the problem directly.

Three claims carry this note.

1. **Growth has one shape.** Agents add rules, tests, records and code cheaply and almost never remove any. What piles up is what costs tokens, test time and attention. Cairn and LHM both show it, and so do studies across hundreds of repositories.
2. **Cairn's answers are the right kind, but a person holds them in place.** A stronger model writes the plan and a cheaper one carries it out. The plan chooses the tests, not the implementer. Review is one pass. The rules every session loads are short. Outside studies support each of these; the one on review rounds is cited in the guide star. But the Maintainer sets each limit by hand, in chat, when it hurts, and the text that states the limits is scattered.
3. **Two kinds of evidence are missing.** No one outside the Maintainer's own projects has installed Cairn. And nothing yet shows which rules change what agents do.

I recommend that v0.9 set the controls, after it settles the defects: one ladder that says which tests run at each stage, a lifecycle that keeps rules in check, counts that show whether a plan written for a cheaper model is enough, and small trials that test a rule on the model that must obey it. These are also what unattended work needs before it widens. Removal should follow each release tag and stay out of the gate before it: archived plans retire to the tag once the proposal carries the outcome, and a pass that only removes then runs (idea 8). v0.10 then harvests the next stage of guidance from the Maintainer's other projects. Nothing here is accepted work.

## The question

After v0.8, does Cairn help people ship good software at a cost they will pay? "Good" here means neither polished without end nor generated without checks. The software is not only scientific models. The Maintainer builds a hydrology model, modflow_tools and Assai, "an agent based lab ecosystem", and wrote on 2026-11-19: "We build software for so many purposes." Cairn's aim, in the same message, is to "capture what's best about agentic coding alongside what's best about a scientist at the helm". What should v0.9 and v0.10 do to serve that?

## Method

I measured these on 2026-11-19 at tag v0.8.0, on a fresh Windows Server 2022 checkout with Python 3.13.5:

- a real `solo-greenfield` install into a scratch repository, following `docs/quickstart.md`, then the integrity check, session start, the board and the security dispatcher;
- read-only scripts over `git log` and the tracked tree: sizes, commits by kind, commits for each proposal and plan, and guidance words at each release tag.

Five Sonnet subagents read Cairn's records and searched outside sources. I mark their figures "reported". For the twenty-eight outside studies listed at the end, I read the abstract and the excerpts a search tool returned, not the full text. Twelve are preprints.

After the Maintainer's response on 2026-11-19 I read again the guide star, the collaboration guide from "Review rules" to "Verification", the plan template, the working agreements, the note of 16 November on projects that have grown, the principles for trimming rules, and the shipped rules README and testing module. Figures for LHM are that note's measurements, not mine. For idea 7, a read-only script measured the two archives, what cites them and which commits edited them. For idea 8 I read the commit messages and the plan record of the two cuts made in November, counted the test files that list their promises and the rule files that plans list, and searched outside studies of subtraction, rule growth and test-suite reduction. I also read the release process and the record of the 0.8 certifying runs.

My counts from Git look backward, and I made them with a question in mind. Measurement rule 4 in the guide star warns against exactly that. Treat them as a reason to measure forward, not as a result.

I did not run Cairn's test suite, test macOS or Linux, read the gate code, or look inside LHM, modflow_tools or Assai. The shares of code and tests by purpose are classed by file name and are approximate.

Three results would show this note wrong. The first is a trial in which agents with no testing rule run no more tests than agents with one. The second is a forward count in which rules, tests and review turns hold steady with no new control. The third is an outside adopter for whom staged guidance arrives too late, or is declined each time it is offered.

## What v0.8 got right

The direction since 0.5 has been right. Six results show it.

- Always-loaded rules fell from 6,114 words at 0.5 to 1,588 now.
- Median proposal length fell from about 10,800 words to 2,500.
- Guidance now arrives by stage. When an adopter's rules folder passes 5,000 words, session start offers a short guide once and records the answer (`templates/core/dev/rules/README.md`).
- Plan review checks that each chunk is specified for the model tier that will build it, and the plan names the rule files and the tests that apply.
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
| An adopter outside the Maintainer's own projects | None yet. LHM and modflow_tools use Cairn and have filed 31 open issues, #62 to #92 (the 16 November note's count). |

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

A rough model, not a measurement, shows why this matters for tokens. If each of 17 commits is one agent turn that reads the plan (5,000 words), the always-loaded rules (1,600) and a template or guide section (4,000), the turns read about 230,000 tokens of process before any code. Two numbers multiply: the turns, and what each turn loads.

### Cuts regrow

| What | History |
|---|---|
| `AGENTS.md`, words | 5,752 at 0.5; 1,047 at 0.8 |
| All working guidance, words | 16,772 at 0.5; 18,415 at 0.8. The text moved to the guide and the rules folder |
| Test functions | cut from 4,071 to 3,138 on 2026-11-10 (reported); 3,407 at 0.8 |
| Certifying run | about 25 minutes on 10-29 and 49 on 11-12 (both reported); 61 on 11-19 |

The records show the same diagnoses returning (reported): guidance too long eight times since June, test volume seven times, review loops six times. Targets that were set and not measured again include a two-minute inner loop, a ten-minute suite and 3.5 review commits per artifact.

LHM shows the same pattern (measured by the 16 November note). In three days its always-loaded files fell from 5,211 to 2,691 words while its rules folder grew from 2,327 to 10,523, so total rule text rose 75%. Its test suite holds 12,975 items, about 79% of them added in 47 days. In both projects a limit on the files every session loads was met, and the total still grew. An agent asked to shorten a file tends to move the text.

### The answers are scattered

Cairn already holds good answers on testing and on rules. They are hard to find and hard to hand on.

- **What to run when.** In Cairn's own tree a keyword search finds test-running instructions in 16 of 49 governing files: `RULES.md`, `AGENTS.md`, the guide, two templates, the session-end skill, two modules, two rules files and six methodology documents. An adopter receives them in five files. The adopter's guide names three stages Boundary A, B and C. It defines A and C in a clause each and uses B without defining it. The full definitions are in `docs/methodology/plans.md` and `docs/methodology/dual-review.md`, which adopters do not receive.
- **Which tests to keep.** The testing module is 1,583 words and well grounded. The two team profiles name it; the solo profile does not (a search of `install/profiles/`).
- **How to keep rules short.** The nine principles for trimming rules are in Cairn's own working agreements (`dev/rules/working-agreements.md`). An adopter receives a five-point guide for a rules folder, offered by the one trigger that exists. I searched the shipped files for four phrases from the working agreement and found none.
- **Reading before writing.** The shipped plan template is 3,919 words. The opening plan it produces is budgeted at 1,000.

As an adopter's agent for one session, I read 21,962 words of rules, templates and board to write a 1,349-word note within the rules.

## The diagnosis

### What accumulates

Agents make adding nearly free. Removing stays dear, because someone must judge what is safe to lose. So four stocks grow in any project built this way: rules, tests, records and code. Each cost the Maintainer named is one of them seen from the paying side.

- Token cost is the text an agent loads each turn, times the turns.
- Test time is the tests that run, times how often they run.
- Security burden is the amount of trusted code that writes into another person's repository.
- Platform cost is the number of lines that touch paths, links and line endings, times three systems.
- Stale text is the number of places one fact is written.
- The Maintainer's attention is the number of artifacts, times their steps.

Outside studies measure the same growth. After projects adopted coding agents, the gain in speed came early and faded, while static-analysis warnings rose about 18% and complexity about 39%, and stayed up [9]. Agents passed over chances to reuse code, and reviewers reacted no worse to that code than to people's [12]. Scoring one change at a time overstated success by up to 20 percentage points against chains of dependent changes [11]. Agents did worse when building on code that agents had written, with the rate of resolved tasks down by as much as 13.1% [13].

The two failures the Maintainer wants to avoid are this one failure seen twice. A vibe-coded mess is code and records that pile up with no one selecting. Endless iteration is checks and review rounds that pile up with no rule for stopping.

So a growing project needs two acts to be routine: **selecting** what one task reads, changes and runs, and **removing** what no longer earns its place. Cairn's best rules are already acts of selection. The plan names its scope. Its "Rules that apply" line names the rule files. The tests are those that name a changed file. Review is one pass.

### The ratchet, and who holds it

A ratchet turns one way.

**An incident becomes a rule, the rule a test, the test a pin.** Each step looks responsible. Undoing one needs a proposal, a review and sometimes a signing ceremony. Adding is cheap and removing is dear, so the total rises.

**That is how Cairn learns, and it is the point of the project.** Cairn's repository is far along the growth curve, so it meets these problems first. A rule written there after an incident is a lesson another scientist does not have to pay for. The cost is the missing second half. Without a step that removes, each lesson stays for good. Cairn's repository is also an unusual case: most of its code is an installer and its security machinery, so some of its lessons are ones a science project will never need.

**Agents obey, so wording is a control.** Left alone, agents repeat work. One study found repeated test runs, near-duplicate scripts and redundant searches in 79 to 98% of tasks, costing up to 23% of the task [18]. Another counted 8.8 test runs for each bug repair on average. Forbidding the runs changed success by 1.25 percentage points and saved 56 to 62% of tokens on one harness [17]. Those were single repairs, so the lesson is that runs should be chosen, not that they should stop. A short rule about what to run therefore pays, as the Maintainer has found. The same obedience makes every stale or doubled sentence costly. Agents given repository instruction files followed them, ran more tests and cost over 20% more, with no general gain in success [1], while a root instruction file went with 29% lower median run time in a second study [4]. Cairn's guidance tells reviewers to read as if a hidden bug exists, to treat a clean review of complex work with suspicion, and to hold nine lenses in mind. Later rules that say "one pass" sit beside those sentences and do not remove them.

**One person holds the ratchet back.** The working agreements record the Maintainer setting each limit in chat: test only what was written (2026-11-12), tools warn and do not block (2026-08-21, and again 2026-11-13), match security effort to the project's size (2026-11-13), keep rules short (2026-11-16), size a review to the change (2026-11-16). Each was needed because nothing else pushes back, and the regrowth table shows ground lost after most cuts.

### What kind of rule works

Three results sort rules by kind.

- **Facts beat procedures.** Giving an agent a map from code to its tests cut regressions from 6.08% to 1.82%. Telling it to follow test-driven steps, without the map, raised them to 9.94% [19]. That study is small: 100 tasks and 25.
- **A person's sentence beats an agent's elaboration.** Guidance a developer wrote in general terms cut cost by up to 42%, about twice the gain from guidance agents wrote from their own traces [18].
- **Committed rules go with lower quality cost.** In a study of 441 repositories, among those whose first AI tool was an agent, complexity rose 27% where the team had committed its AI configuration and 53% where it had not. The authors call this a hypothesis, since careful teams may differ in other ways. They also found that 73.8% of such files were committed once and never changed [10]. Almost no one maintains their rules, so a method for doing it is a gap in practice generally, not only here.

A plan is not a standing procedure. It is the process for one task, worked out by a capable model before the work, and reviewed. One study found that planning shifts from making weaker models accurate to making stronger ones cheaper, and that it changes where a run stops [14]. A benchmark of agent teams found mixed models on the best line of cost against accuracy, with the weak link sometimes the planner and sometimes the executor [15]. A third study found that general agents kept the structure of their own declared plan in only 22 to 45% of runs [16]. These support having one tier write for a lower one, and checking that the implementer kept to the plan. They also say what changes as models improve. A study of 9,374 agent runs found that the model, not the scaffolding around it, drives success, and that the scaffolding's effect shrinks with each generation [5]. Its job moves from getting the work right to keeping it cheap and making it stop.

The scientist's half rests on other studies. In one, 68 to 80% of two models' failing runs were wrong in the same way on each repeat, so agreement between runs looked healthy [3]. In another, on security repairs, passing tests and reviewer agents did not intercept the confirmed failures [7]. Of 78 novice programmers, those made to explain generated code before accepting it failed a later unaided task 39% of the time, against 77% without that step [2]. What an agent cannot supply is an expected answer from outside the code and a person who understands the result.

## Eight ideas

### 1. The plan is a loader

The stronger model decides once what the cheaper one reads, changes and runs, and where it stops. The plan template already has all four: "Rules that apply", Scope, Verification and Acceptance criteria. Plan review already checks that each chunk is specified for its tier, "with no design left to the implementer". Treat this as the centre of the method. Every part of it is a selection from a growing pile, made by the model best able to make it.

Give it a signal. The retry rule already defines two events: a retry at the same tier, and a rerun one tier up. Count them for each chunk. Few means the plan was enough, and its detail can be thinned as models improve. Many means the plan left design to the implementer, or the tier floor is wrong. I found no place where those events are recorded so that they can be counted. A keyword search of the 28 plans archived from 10 to 19 November finds 13 that mention the low tier and two that mention an escalation.

The criteria also tell the agent where to stop. One study found capable agents reaching the correct code and then overwriting it [8].

### 2. One ladder for tests

The Maintainer asked for "rules for what to run at each stage". The rules exist. They need one home and plain names. Each rung below is drawn from text Cairn already has.

| When | What runs | Who chooses | What it shows |
|---|---|---|---|
| Building a chunk | the tests the plan names for the changed files, and scratch probes | the plan, from the map of files to tests | the chunk meets its criterion |
| Plan complete | the permanent tests of each changed promise, once, on the committed revision | the plan | the promises hold |
| Code review | committed evidence, and one fresh probe for a named doubt | the reviewer | someone else tried to break it |
| Connected plans complete | one joined integration selection | the arc owner | the pieces work together |
| Session end | the fast smoke run, if the project has one | the handoff owner | nothing obvious is broken |
| Release | the whole suite and the security families, once on each certifying host | the release operator | the tree is certified |
| A model run | a named run that answers a stated question | the plan and the Maintainer | an answer about the model; it is not a test |

Three things would make the ladder better than the present text. Give each rung a time budget and its command, so the cheap rung is the easy one to run; Cairn's own suite already asks for an explicit override before a broad run (`tests/conftest.py`). Have the plan write the exact command for each chunk, so a low-tier implementer never chooses. Invest in the map from a changed file to its tests, since a map is the kind of guidance that worked in the study above [19]. The ladder replaces the names Boundary A, B and C in adopter text. By the swap rule it should shrink the text, not add to it.

### 3. Rules are tests in prose

The Maintainer's comparison carries a full lifecycle. The testing module already gives tests each item on the left. The shipped rules guide gives rules the first, second and last on the right.

| A test has | A rule should have |
|---|---|
| a promise it guards, named in the file | the decision or incident it came from, in the person's wording |
| a tier, set by where it lives | an "Applies when" line and a route that says when it is read |
| a time budget for the run | a word budget for what one kind of task reads |
| a failing case that proves it can fail | a case where an agent without the rule goes wrong |
| a review of the slowest at each release | a review of the longest, and of those no trial has tested, after each release |
| deletion when no promise needs it | a dated line when it leaves |

Four additions follow from the table.

- **Admit by kind.** A rule states a fact the agent cannot infer, a limit or a decision reserved for a person, or a procedure. Facts and limits enter in the person's wording. A standing procedure must show that it changes what agents do.
- **Budget the route, not the file.** A cap on the always-loaded files was met at Cairn and at LHM while the total grew. Budget what one kind of task must read, such as a light change or a plan chunk. The "Rules that apply" line already names the route.
- **Count by entry, not by file.** A count of the rule files a plan lists cannot tell rules apart. The 13 archived plans that carry the "Rules that apply" line each list three or four of Cairn's six rule files, and 12 list the same three. A file holds many rules. The unit is the entry, which the rules guide already gives one shape and an "Applies when" line. Until entries can be counted, the trial in step 5 of the recommendation is the test of whether a rule earns its place.
- **Review after each release**, in the pass that idea 8 describes.

Ship this with the nine trimming principles, which adopters do not yet receive.

### 4. Controls that report

Each limit today is a number someone remembers: a word cap, one review pass, a ten-minute suite. A control also needs a signal that says when to tighten or loosen. v0.8 built the mechanism once: session start reads an "Offered when" line and offers the rules-folder guide when the folder passes 5,000 words. Use the same reader for correction, not only for new modules. Candidates, each a condition a tool can read from the project's own files: the suite's recorded time passes its budget; the rule text one kind of task reads passes its word budget; review commits for a plan pass the target. Add one at a time and record whether the offer was accepted, as the 16 November note advises. Correction then becomes routine and stops depending on one person noticing.

### 5. Several laboratories

Cairn, LHM, modflow_tools and Assai differ in kind: a method with an installer, a legacy model, a new library and an agent-based ecosystem. That spread is an asset. The 16 November note set the rule for modules: harvest what two projects converged on, and let a module with one project's evidence wait for a second. Apply the same rule to the text every adopter receives. A lesson from one project stays in that project's rules folder. Assai matters most for the Maintainer's point that Cairn is not only for models. A lesson that holds in a model and in an agent ecosystem is a lesson about software built by agents.

### 6. The scientist's half

The agent brings speed and breadth. The scientist brings the expected answer and the judgment of what matters. Three practices keep that half strong.

- **Expectation first.** The scientist writes the expected result before the run, with its source: "drawdown at 100 metres after one day should be near half a metre, from the Theis solution with these values." It takes two minutes, it is independent of the code, and it builds the understanding that the comprehension floor protects. The testing module already says to state expected behaviour before results. Make it the first line of any change that touches a calculation.
- **Two questions for a person's attention.** Could we undo it, and would we notice if it were wrong? The working agreements already send work that can be undone to the lighter lane. The second question is the scientist's own risk: a sign, unit or index error that still runs and gives a plausible number. A change that would not be noticed needs an independent check. The same two questions say what may run unattended.
- **A record with a second job.** An essay on generated code names the two losses a decision record guards against: shared understanding and stated intent [6]. A table drawn from proposal closeouts (change, assumption, check, source of the expected answer, result) is a verification statement for a paper's methods section. I assume journals increasingly ask for one. I did not check.

The same economy applies to security. At this release the signing ceremony stopped three times and was deferred. Economy of mechanism, already cited under anchor 17, says the strongest control is fewer trusted lines. For the open re-anchor proposal, weigh a human-read diff of the protected files against more ceremony. I have not read the gate code, so that is a question for its review, not a finding.

### 7. The proposal is the history; the plan retires

The Maintainer's view (chat, 2026-11-19): "Once we are done with plans at a release they are generally done. But the proposal is the project history." The record agrees (measured from Git, looking backward).

| | Archived plans | Archived proposals |
|---|---|---|
| Files | 210 | 217 |
| Words | 2.02 million, 53% of tracked Markdown | 1.34 million, 35% |
| Median length | 4,805 words | 3,260 words |
| Commits since 0.7 that edited one after archive | 21, all to 7 plans opened in the 0.8 window | 1 |

No plan from an earlier release was edited. The method already calls an archived plan "a file that is about to stop being read" (`docs/methodology/plans.md`) and requires each lasting item to have a home outside it. All 210 are in the v0.8.0 tag, so removing them from the tree loses nothing and can be undone.

One gap comes first. Of the 26 proposals archived in the 0.8 window, the 17 that a plan cites all end at their Decision, and their outcome is written only in the plan's closeout. Eight of the nine with no plan end with their own implementation record. Remove the plans and most of the history loses its ending. Three rules close the gap and add no record.

1. Append the closeout to the source proposal, as a light proposal already does. It says what shipped, which checks ran and their results, anything dropped with the Maintainer's quoted allowance, and each deferral's home.
2. From then on the board and the changelog cite the proposal, not the plan.
3. After a release tag, remove each archived plan that the tag holds and whose work has no open board row. The folder's README says which tag holds them.

Offered to adopters, this is the first work after a release, outside the gate. The tag is the point where each stock lets go: plans retire, and the pass in idea 8 takes the tests and the rules.

The cost in Cairn's own tree comes once. Outside the archives, 295 citations in 37 files name the plans archive: 132 in the changelog, 59 in measurement records and 40 on the board. The shipped claim and stem checkers resolve a plan's name to its archived file. Two generators of 665 lines, named in the gate manifest, list both archives to exempt records older than today's schema; I did not read how the gate uses them. Archived proposals cite plans 186 times, and those links would dangle. The median archived plan is nearly five times today's opening budget, so the archive also holds 210 examples of the old length. I assume agents meet them when they search. I did not measure that.

### 8. A consumer

The Maintainer (chat, 2026-11-20): "I personally love the idea of a consumer of rules and tests, because everything else is a producer of them." Every role Cairn names produces. An implementer adds code and tests, a reviewer adds findings, and an incident adds a rule. People overlook changes that take something away unless they are cued to look for them [20]. A cue that named only removal drew more such ideas than one that named both [21], and two language models showed the bias more strongly than people did [22]. So the consumer is a separate pass whose brief has one verb. A question added to review would not do the same work.

Cairn has had a consumer on paper since its first cut. The release process names the gap, "The improvement loop adds but does not consolidate", and answers it with a seventh sweep inside the release gate that reports findings for the Maintainer to triage (`release/RELEASE_PROCESS.md`). The totals grew anyway. The Maintainer named both reasons on 2026-11-20: the gate "takes most of a working day", and "I cannot review a list of tests to drop. It's not my role in this collaboration. I am a scientist who codes, not a software engineer." The design below moves the work out of the gate and the decisions to agents.

Cairn has run that pass twice by hand. The record shows what was nearly lost and how it was found. The figures come from commit messages and the plan record; I reran nothing.

| | Test cut, 8 to 13 November | Rules trim, 10 November |
|---|---|---|
| Removed | test functions fell from 4,071 to 3,138 | guidance text for adopters fell from 8,012 to 7,238 words |
| Dropped in error and put back | 34 tests | 10 rules, then 3 more pieces of wording |
| How they were found | each removed name was searched for across the repository | a read-only comparison of old and new text by the low-tier model, then later reviews |
| Also | 51 public tests replaced 202 private ones and exposed five possible product defects | |

Three lessons follow.

- **Check after, not before.** The plan first required a comparison of old and new tests before each set of removals. The Maintainer moved it to one run afterwards on 2026-11-10: "there should be a test AFTER the cuts."
- **The checks that worked were cheap.** One was a search and the other a read-only comparison. The search was not a tool, and later rounds covered fewer files, so four tests were missed at first.
- **A campaign does not hold.** The plan for the cut ran to 26,430 words and 87 commits edited it. Seven days later the tree held about 270 more test functions.

**What it is.** A pass that follows each release tag. It also runs when a budget is passed (idea 4), and when a change that keeps behaviour breaks tests, since the testing module calls that failure a pin. It never runs in the gate, where the records name one exact commit, "so any commit added after them starts the records over" (`release/RELEASE_PROCESS.md`). After the tag, the tag holds everything it removes, and a whole window lies ahead for a wrong call to show. Its target is the gate itself. By my reading of the release process, a cut runs most or all of the suite at least five times: the certifying run, then both test orders on each of two hosts. A third host makes seven. I did not time those runs. Its licence has four lines.

1. It removes, merges, or moves a test to a later rung of the ladder (idea 2). It adds no rule and changes no behaviour. Replacing many private tests with a few public ones is plan work, which it may propose.
2. It never removes a failing test, and never works on files an open plan is changing.
3. It never touches what a person has declared must stay. In Cairn that is the tests that security and release records name as guards, refusal and hostile-state tests, Maintainer-only actions and data refusals. In a science project the list would hold results: the reference runs, their pass bands and the checks against outside answers. The testing module already reserves those to the Maintainer. It is the scientist's statement of what matters, in the scientist's terms, and it should fit on a page. It changes only by the Maintainer's Decision, or a Security Review where one applies now.
4. It decides for itself and records each call: the item, the evidence, and what would show the removal was a mistake. A second agent reviews the sweep in one pass. The Maintainer is not shown a list of tests or rules.

The checks are mechanical or low-tier work. Judgment calls go to a higher tier, as the testing module already says, and as six high-tier reviewers did in November. Cairn's rule is already that "Agents select routinely, reviewers challenge, and the Maintainer sets high-level needs and material exceptions" (`dev/agent_collaboration.md`, "Verification"). A sign-off the Maintainer cannot judge would not be a control.

**The Maintainer's part** is in the project's own terms. The Maintainer sets what must stay and how long the gate may take, and sees three numbers after each pass: the gate's length, what left and what came back. A question reaches the Maintainer only when a promise itself looks out of date, such as "Does the model still need to reproduce this run?"

**How it knows what matters.** No one can judge a test or a rule alone, because each looks important alone. Importance is written once, one level up, in a person's words: the promise a test guards, and the decision a rule came from. 129 of Cairn's 135 test files already carry a `Promises:` line. After a sweep four checks run, and none needs judgment.

- Every promise still has a passing public check, and every decision still has its sentence.
- No document, roster or comment still names a removed item as its guard. A tool runs this search, so it covers the same files each time.
- Nothing is gone that the list does not name.
- One comparison on seeded faults, which are small deliberate breaks in the code, shows whether the new set misses what the old one caught.

A test whose promise still stands moves to a later rung before it leaves. It still runs at release, so a wrong call costs a later warning, not a missed fault. That step guards against a wrong call and does not shorten the gate. Only removal does, and the testing module already lets a test with no promise go directly. Studies of deletion show why the guard matters. Reduced suites missed faults in up to 52.2% of failed builds, across 1,478 real ones in 32 projects, and the usual measures did not predict the loss [27]. Other experiments found losses that were severe in one case [26] and about 12.5% on average in another [28]. A measure cannot pick what is safe to delete. A named promise can. Each removed item leaves one dated line saying what would show the mistake, and a restore adds a line. If restores stay at zero through several releases, the pass is too timid.

**What it cannot do alone.** In a model of administrative growth, pruning could not hold the total steady once creating was easy enough, and one-off cuts gave only short relief [23]. So entry needs a rule too. A new standing procedure (idea 3) is provisional until the pass after the next tag, where it is renewed on evidence, a trial or a recorded use, or it lapses. Facts, limits and the Maintainer's decisions do not lapse. The evidence on expiry reviews is mixed. A study of fifty states found them the most effective of the review tools it compared [24]. A later study reports that renewal has often passed by inertia, and suggests that a short horizon with an explicit renewal works better [25].

Two sweeps in one project are thin evidence. I found no later commit that traces a defect to a cut test, but I searched commit messages only.

## Options

1. **Continue the v0.9 board as written.** Its theme is monitoring, outside evidence and autonomy. Its case is real: the dashboard answers a stated need, and the release module and test records are guidance harvested from adopters. Its weakness is order. Unattended work comes before the controls that make it safe to leave.
2. **Cut Cairn to a small core for everyone.** This treats the guidance for grown projects as weight, when it is the product. A small start already exists as the first stage of staged guidance, and the evidence above favours committed rules over none.
3. **Set the controls, then widen.** I recommend this one.

## Recommendation

### v0.9: set the controls

Do these in order. Each makes the next cheaper.

1. **Settle the defects**, as already directed, including issues #97 and #98. Add the documented first-run and upgrade commands to each host's release verification. That check would have caught #97.
2. **Write the test ladder** (idea 2) as one table in the guide every adopter gets, and point the other files at it.
3. **Write the rule lifecycle** (idea 3) into the rules-folder guide, with the trimming principles. Apply it first to Cairn's own 18,400 words.
4. **Count the plan's events** (idea 1): retries and moves up a tier for each chunk, and from Git the commits, review commits and Maintainer decisions for each plan. Keep the proposal and the plan, and lower the number of turns around them. The hand-filled Tokens field read "unknown" in every sampled entry, and the board already ties its retirement to the meter comparison.
5. **Run the first rule trials.** Take four or five cases from battles already fought: the whole suite run on each chunk, a rule file rewritten wholesale, accepted scope quietly dropped, a review that will not close. Run each on the low-tier model, with the rule and without it. Declare the cases, the count and what is inconclusive before the first run. Report by case and never rank models. The first trial tests the Maintainer's own observation about tests, and the outside studies predict it will hold. A rule that changes nothing goes to the consumer's next pass (idea 8). The trials cost a handful of headless sessions for each case and need the Maintainer's go-ahead.
6. **Keep the rows that harvest from adopters**: the release module, test records once LHM's measurement is in, the adopter interview, the outside trial and verification on three hosts. Put the closeout on the proposal now, since that step removes nothing, and make plan retirement (idea 7) and the consumer's pass (idea 8) the first work after a tag, outside the gate. The v0.8.0 tag is cut, so the first pass can run in this window and the v0.9 gate can measure it.
7. **Ship one dashboard tab**, the development view, and show the counts from step 4 on it.

I would place four rows after the controls, or in v0.10: the budget guard and unattended loop, roadmap draining, the four-view comparison and the new dimension axis. An unattended agent needs the ladder, the route and the stopping criteria to be mechanical first.

**Suggested exit test.** The ladder and the lifecycle each have one home, and shipped guidance words fall. Plan events are counted through one release. The first-run check passes on three hosts. At least one rule trial has a recorded result. The consumer's pass has run once on Cairn's tree, and the Mac certifying run takes less than the 61 minutes of 0.8. One adopter outside the Maintainer's projects completes three changes.

**Suggested targets, for the Maintainer to set.** A light change takes 3 commits, 1 review and at most 1 Maintainer decision. A plan takes 8 commits and 4 review commits. The certifying run takes 20 minutes. These count events, not words, as measurement rule 1 asks.

### v0.10: the next stage, harvested

- one page that says what a project needs at each size, with the trigger that offers each piece;
- the second and third triggers (idea 4);
- the modules that two projects converged on: releases, and test records if LHM's saving is real;
- the scientist's half: the independent-check library and its skill, issue #19 expressed as check presets, a worked example from a real project, and the verification table;
- the consumer's first pass over the rules, with trial results;
- the January evaluation of Cairn Plain Language;
- Assai's frictions folded back as LHM's are, if the Maintainer wants that.

### 1.0

Declare it on evidence: each shipped lesson held in two projects, one adopter outside them, rule trials rerun on a new model generation, and a release the Maintainer can cut in thirty minutes. Cairn's own record is rare evidence: 7,303 commits on 73 active days, with each decision kept. Most published studies score single tasks, and the few that follow a project through time find the growth described above. A methods paper on what a project needs as it grows would fill that gap. Publishing a measurement needs the Maintainer's Decision.

### Pace

Cairn made five releases in the thirty days after 0.4, and each asks adopters to follow an 8,300-word upgrade guide. The standing direction of 2026-07-22 puts science projects first. Let v0.9 land when its exit test passes, not on a date.

## Risks

- **Controls become more apparatus.** Each one here reuses something the project already produces: the "Rules that apply" line, the retry rule, Git and the one trigger reader. A new tool still needs its own go-ahead under the standing direction.
- **A word budget is a measure of prose.** Measurement rule 1 warns that such a measure becomes the target. Use the route budget as a limit, checked by listing the files a task reads, and never as a score.
- **Gathering the test text into one ladder could drop a rule.** The review question for functional prose, "Does any rule weaken or disappear?", is the guard.
- **Rule trials are small and synthetic.** An agent in a trial is not an agent in a long session. Pair the trials with the counts from real work.
- **The lessons come from one Maintainer's projects.** LHM, modflow_tools and Assai share one person's habits. The outside adopter is the check.
- **A plan thinned too early.** Thin a plan's detail only when the count of retries shows the lower tier no longer needs it.
- **A sweep loses something no one notices.** The count of restores holds only the losses someone saw. Whatever fails silently, such as a wrong number that looks right, stays on the declared list and out of the sweep.
- **No person reads the consumer's calls.** That is the design, since the Maintainer cannot judge a list of tests. The guards are the declared list, the four checks, a second agent's pass and the tag. An agent that misjudges a promise is the risk that remains.

## Open questions

1. Does v0.9 open with the test ladder and the rule lifecycle, after the defects?
2. Which rows wait for the controls: the budget guard and unattended loop, roadmap draining, the four-view comparison, the dimension axis?
3. May the first rule trial run, on which low-tier model, and with what spending limit?
4. Which per-change targets does the Maintainer set?
5. Is Assai run under Cairn, and may its frictions be folded back?
6. Is 1.0 declared on evidence, and is a paper its form?
7. Do archived plans retire after each release tag, once the proposal carries the closeout? Are the 210 now in the tree removed in one step, or by release?
8. Is the consumer a named role with its own licence? Does it take over the rules and tests part of release sweep G, so the gate loses a step? What gate length does the Maintainer set as its target, and what goes on a science project's declared list?

## Outside sources

I read the abstract of each and the excerpts a search tool returned, not the full text. Sources 1, 2, 3, 5, 7, 8, 11, 14, 15, 16, 18 and 19 are preprints and not peer reviewed. Source 4 is a repository deposit whose review status I did not see. Source 6 is a magazine essay. Sources 9, 10, 12, 13, 17 and 20 to 28 appeared in conference proceedings or a journal. Source 23 is a mathematical model, not a field study.

1. Gloaguen et al. (2026), *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* [doi:10.48550/arxiv.2602.11988](https://doi.org/10.48550/arxiv.2602.11988)
2. Sankaranarayanan (2026), *Mitigating "Epistemic Debt" in Generative AI-Scaffolded Novice Programming using Metacognitive Scripts.* [doi:10.48550/arxiv.2602.20206](https://doi.org/10.48550/arxiv.2602.20206)
3. Mehta (2026), *Confident and Wrong: Silent Semantic Failures in Coding Agents.* [doi:10.48550/arxiv.2603.25764](https://doi.org/10.48550/arxiv.2603.25764)
4. Lulla et al. (2026), *On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents.* [doi:10.5281/zenodo.18348506](https://doi.org/10.5281/zenodo.18348506)
5. Mehtiyev and Assunção (2026), *Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure.* [doi:10.48550/arxiv.2604.02547](https://doi.org/10.48550/arxiv.2604.02547)
6. Storey (2026), *From Technical Debt to Cognitive and Intent Debt.* ACM Queue. [doi:10.1145/3807966](https://doi.org/10.1145/3807966)
7. Bai et al. (2026), *When Passing Tests Hides Vulnerabilities: An Empirical Study of Silent Failures in Agentic Systems.* [doi:10.2139/ssrn.7269655](https://doi.org/10.2139/ssrn.7269655)
8. Kim et al. (2026), *Coherence Collapse: Diagnosing Why Code Agents Fail After Reaching the Right Code.* [doi:10.48550/arxiv.2603.24631](https://doi.org/10.48550/arxiv.2603.24631)
9. Agarwal, He and Vasilescu (2026), *AI IDEs or Autonomous Agents? Measuring the Impact of Coding Agents on Software Development.* MSR. [doi:10.1145/3793302.3793589](https://doi.org/10.1145/3793302.3793589)
10. Denisov-Blanch et al. (2026), *A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption.* ASE. [doi:10.1145/3832783.3837546](https://doi.org/10.1145/3832783.3837546)
11. Shastry et al. (2026), *Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution.* [doi:10.48550/arxiv.2604.03035](https://doi.org/10.48550/arxiv.2604.03035)
12. Huang et al. (2026), *More Code, Less Reuse: Investigation on Code Quality and Reviewer Sentiment towards AI-generated Pull Requests.* MSR. [doi:10.1145/3793302.3793622](https://doi.org/10.1145/3793302.3793622)
13. Patel et al. (2026), *Is Agent Code Less Maintainable Than Human Code?* EMNLP. [doi:10.18653/2026.emnlp-main.2528](https://doi.org/10.18653/2026.emnlp-main.2528)
14. Fan et al. (2026), *An Empirical Study of Harness Design for Coding Agents.* [doi:10.48550/arxiv.2609.20804](https://doi.org/10.48550/arxiv.2609.20804)
15. Jiang et al. (2026), *Specialize Roles, Mix Deployments: Pushing the Cost-Accuracy Frontier of LLM Agent Teams.* [doi:10.48550/arxiv.2606.20629](https://doi.org/10.48550/arxiv.2606.20629)
16. Oota et al. (2026), *Do LLM Agents Execute the Plans They Declare? From Planning-Mode Declaration to Pattern-Specific Execution.* [doi:10.48550/arxiv.2609.38108](https://doi.org/10.48550/arxiv.2609.38108)
17. Lin et al. (2026), *To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair.* Proceedings of the ACM on Software Engineering. [doi:10.1145/3832113](https://doi.org/10.1145/3832113)
18. Hu et al. (2026), *Analyzing and Mitigating Cost-Inefficient Behaviors in Coding Agents.* [doi:10.48550/arxiv.2609.30725](https://doi.org/10.48550/arxiv.2609.30725)
19. Alonso, Yovine and Braberman (2026), *TDAD: Test-Driven Agentic Development - Reducing Code Regressions in AI Coding Agents via Graph-Based Impact Analysis.* [doi:10.48550/arxiv.2603.17973](https://doi.org/10.48550/arxiv.2603.17973)
20. Adams et al. (2021), *People systematically overlook subtractive changes.* Nature. [doi:10.1038/s41586-021-03380-y](https://doi.org/10.1038/s41586-021-03380-y)
21. Fillon et al. (2025), *The Overlooking of Subtractive Changes: Replication and Extension to Stronger Cues and Social Norms.* The Journal of Creative Behavior. [doi:10.1002/jocb.1535](https://doi.org/10.1002/jocb.1535)
22. Uhler et al. (2026), *Influence of solution efficiency and valence of instruction on additive and subtractive solution strategies in humans, GPT-4, and GPT-4o.* Communications Psychology. [doi:10.1038/s44271-026-00403-0](https://doi.org/10.1038/s44271-026-00403-0)
23. Yang and Grenier (2026), *What leads to administrative bloat? A dynamic model of administrative cost and waste.* PNAS. [doi:10.1073/pnas.2527106123](https://doi.org/10.1073/pnas.2527106123)
24. Sobel and Dove (2014), *Analyzing the Effectiveness of State Regulatory Review.* Public Finance Review. [doi:10.1177/1091142114557723](https://doi.org/10.1177/1091142114557723)
25. Jones and Quandt (2025), *An iridescent sunset: An empirical analysis of sunset legislation.* Journal of Regulatory Economics. [doi:10.1007/s11149-025-09498-5](https://doi.org/10.1007/s11149-025-09498-5)
26. Rothermel et al. (1998), *An empirical study of the effects of minimization on the fault detection capabilities of test suites.* ICSM. [doi:10.1109/icsm.1998.738487](https://doi.org/10.1109/icsm.1998.738487)
27. Shi et al. (2018), *Evaluating test-suite reduction in real software evolution.* ISSTA. [doi:10.1145/3213846.3213875](https://doi.org/10.1145/3213846.3213875)
28. Nömmer and Haas (2019), *An Evaluation of Test Suite Minimization Techniques.* Lecture Notes in Business Information Processing. [doi:10.1007/978-3-030-35510-4_4](https://doi.org/10.1007/978-3-030-35510-4_4)
